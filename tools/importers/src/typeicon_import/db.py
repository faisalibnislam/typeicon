"""Transactional catalog load: build/catalog + release artifacts -> PostgreSQL + storage.

Everything is written in ONE transaction. Readers never observe a half-loaded catalog, and a
failure leaves the previous catalog intact. The load is idempotent (upserts keyed by stable
ids; per-namespace registries are replaced atomically). An outbox row records the publish
so derived systems (search index, CDN purge) can catch up recoverably.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import psycopg
from psycopg.types.json import Jsonb

from .build import load_designs
from .registry import CodepointRegistry
from .sources import load_manifest, repo_root
from .storage import content_type_for, get_storage

STYLES = [
    ("filled", "Filled", "Solid shapes with interior details knocked out.", 0, True),
    ("line", "Line", "2px outlines with crisp butt caps, miter joins and small corner radii.", 1, True),
    ("rounded", "Rounded", "2px outlines with round caps, round joins and softer corners. Not a container shape.", 2, True),
    ("thin", "Thin", "Line geometry with a 1px stroke: half the weight of Line, same butt caps and miter joins.", 3, True),
    ("brand", "Brand", "Brand logo in its single official form. Never redrawn as Filled, Line, Rounded or Thin.", 4, False),
]
LICENSE_NAMES = {
    "MIT": ("MIT License", "https://opensource.org/license/mit", True),
    "Apache-2.0": ("Apache License 2.0", "https://www.apache.org/licenses/LICENSE-2.0", True),
    "LicenseRef-TypeIcon-Core-Draft": ("TypeIcon Core License (draft, owner decision required)", None, False),
    "CC0-1.0": ("Creative Commons Zero v1.0 Universal", "https://creativecommons.org/publicdomain/zero/1.0/", False),
}
PLANS = [
    ("free", "Free", {"subsetBuildsPerHour": 20, "maxSubsetIcons": 500, "customIcons": 0, "kits": 3, "hostedKits": False}, True),
    ("pro", "Pro", {"subsetBuildsPerHour": 200, "maxSubsetIcons": 5000, "customIcons": 200, "kits": 50, "hostedKits": True}, False),
    ("team", "Team", {"subsetBuildsPerHour": 500, "maxSubsetIcons": 20000, "customIcons": 2000, "kits": 500, "hostedKits": True}, False),
]


def _search_names(d: dict) -> str:
    words = [d["name"], d["localName"], *d.get("aliases", [])]
    out: list[str] = []
    for w in words:
        for token in [w, *w.split("-")]:
            if token and token not in out:
                out.append(token)
    return " ".join(out)


def compute_stats(cur) -> dict:
    cur.execute("""
      SELECT count(*) FILTER (WHERE d.status='published'),
             count(*) FILTER (WHERE d.status='published' AND d.area='core'),
             count(*) FILTER (WHERE d.status='published' AND d.area='community'),
             count(*) FILTER (WHERE d.status='published' AND d.is_brand),
             count(DISTINCT d.concept_id) FILTER (WHERE d.status='published'),
             count(*) FILTER (WHERE d.status='published' AND d.area='core'
                               AND d.published_styles @> ARRAY['filled','line','rounded']),
             count(*) FILTER (WHERE d.status='published' AND d.area='core'
                               AND d.published_styles @> ARRAY['filled','line','rounded'] AND d.derived_from IS NULL),
             count(*) FILTER (WHERE d.status='published' AND d.area='core' AND d.attributes ? 'variantOf')
      FROM designs d""")
    total, core, community, brands, concepts, core_complete, core_counted, core_variants = cur.fetchone()
    cur.execute("""
      SELECT v.style, count(*), count(*) FILTER (WHERE v.font_supported), count(*) FILTER (WHERE v.route='svg-only')
      FROM variants v JOIN designs d ON d.id=v.design_id
      WHERE v.status='published' AND d.status='published' GROUP BY v.style""")
    by_style = {s: {"variants": n, "fontSupported": f, "svgOnly": so} for s, n, f, so in cur.fetchall()}
    cur.execute("""
      SELECT s.slug, s.display_name, s.area, count(DISTINCT d.id), count(v.id)
      FROM source_packs s LEFT JOIN designs d ON d.source_pack_id=s.id AND d.status='published'
      LEFT JOIN variants v ON v.design_id=d.id AND v.status='published'
      GROUP BY s.slug, s.display_name, s.area ORDER BY s.area, s.slug""")
    sources = [{"slug": a, "displayName": b, "area": c, "designs": n, "variants": v} for a, b, c, n, v in cur.fetchall()]
    cur.execute("SELECT count(*) FROM aliases a JOIN designs d ON d.id=a.design_id WHERE d.status='published'")
    alias_count = cur.fetchone()[0]
    variants_total = sum(v["variants"] for v in by_style.values())
    return {
        "designs": {"total": total, "core": core, "community": community, "brands": brands},
        "concepts": concepts,
        "variants": {"total": variants_total, "byStyle": by_style,
                     "fontSupported": sum(v["fontSupported"] for v in by_style.values()),
                     "svgOnly": sum(v["svgOnly"] for v in by_style.values())},
        "aliases": alias_count,
        "core": {"designs": core, "completeThreeStyle": core_complete, "countedTowardTarget": core_counted,
                 "transformDerived": core_complete - core_counted, "variants": core_variants, "base": core - core_variants},
        # Goal: 20,000 unique drawn Core concepts (rotations excluded); badge variants are counted separately.
        "target": {"uniqueCoreConcepts": 20000, "current": core_counted - core_variants,
                   "gap": max(0, 20000 - (core_counted - core_variants))},
        "sources": sources,
    }


def load_catalog(database_url: str | None = None, root: Path | None = None, release_version: str | None = "0.1.0",
                 actor: str = "system:catalog-loader", upload: bool = True, overwrite_release: bool = False,
                 prune_removed: bool = False) -> dict:
    root = root or repo_root()
    url = database_url or os.environ.get("DATABASE_URL")
    if not url:
        raise SystemExit("DATABASE_URL is required")
    manifest = {s.slug: s.raw for s in load_manifest(root)}
    designs = load_designs(root)
    registry = CodepointRegistry(root / "assets" / "registry" / "codepoints.json")
    summary: dict = {}

    with psycopg.connect(url, autocommit=False) as conn, conn.cursor() as cur:
        cur.execute("SET LOCAL statement_timeout = '15min'")
        if prune_removed:
            summary["pruned"] = _prune_removed(cur, set(manifest))
        cur.executemany(
            """INSERT INTO styles (slug, name, description, sort_order, is_core) VALUES (%s,%s,%s,%s,%s)
               ON CONFLICT (slug) DO UPDATE SET name=EXCLUDED.name, description=EXCLUDED.description, sort_order=EXCLUDED.sort_order,
                 is_core=EXCLUDED.is_core""",
            STYLES)
        for slug, name, caps, default in PLANS:
            cur.execute("""INSERT INTO plans (slug, name, capabilities, is_default) VALUES (%s,%s,%s,%s)
                           ON CONFLICT (slug) DO UPDATE SET name=EXCLUDED.name, capabilities=EXCLUDED.capabilities, is_default=EXCLUDED.is_default""",
                        (slug, name, Jsonb(caps), default))

        # licenses + source packs
        pack_ids: dict[str, str] = {}
        for slug, s in manifest.items():
            spdx = s["license"]["spdx"]
            lname, lurl, osi = LICENSE_NAMES.get(spdx, (spdx, None, False))
            cur.execute("""INSERT INTO licenses (id, name, url, text, osi_approved) VALUES (%s,%s,%s,%s,%s)
                           ON CONFLICT (id) DO UPDATE SET name=EXCLUDED.name, url=EXCLUDED.url, text=EXCLUDED.text, osi_approved=EXCLUDED.osi_approved""",
                        (spdx, lname, lurl, (root / s["license"]["file"]).read_text(), osi))
            dist = {k: s[k] for k in ("kind", "package", "tarball", "integrity", "distributionUrl", "path") if k in s}
            review = s.get("review", {})
            cur.execute(
                """INSERT INTO source_packs (slug, area, display_name, namespace, name_prefix, upstream_url, author, copyright,
                     version, distribution, retrieved_at, license_id, notices, attribution_required, attribution_text,
                     reserved_font_names, permissions, style_mapping, style_mapping_note, trademark_note, review_status,
                     reviewed_by, reviewed_at, review_note, modification_history)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   ON CONFLICT (slug) DO UPDATE SET area=EXCLUDED.area, display_name=EXCLUDED.display_name,
                     namespace=EXCLUDED.namespace, name_prefix=EXCLUDED.name_prefix, upstream_url=EXCLUDED.upstream_url,
                     author=EXCLUDED.author, copyright=EXCLUDED.copyright, version=EXCLUDED.version,
                     distribution=EXCLUDED.distribution, retrieved_at=EXCLUDED.retrieved_at, license_id=EXCLUDED.license_id,
                     notices=EXCLUDED.notices, attribution_required=EXCLUDED.attribution_required,
                     attribution_text=EXCLUDED.attribution_text, reserved_font_names=EXCLUDED.reserved_font_names,
                     permissions=EXCLUDED.permissions, style_mapping=EXCLUDED.style_mapping,
                     style_mapping_note=EXCLUDED.style_mapping_note, trademark_note=EXCLUDED.trademark_note,
                     review_status=EXCLUDED.review_status, reviewed_by=EXCLUDED.reviewed_by, reviewed_at=EXCLUDED.reviewed_at,
                     review_note=EXCLUDED.review_note, modification_history=EXCLUDED.modification_history, updated_at=now()
                   RETURNING id""",
                (slug, s["area"], s["displayName"], s["namespace"], s.get("namePrefix", ""), s.get("upstreamUrl"),
                 s.get("author"), s.get("copyright"), s["version"], Jsonb(dist), s.get("retrievedAt"), spdx,
                 Jsonb(s.get("notices", [])), s["attribution"].get("required", False), s["attribution"].get("text"),
                 Jsonb(s.get("reservedFontNames", [])), Jsonb(s.get("permissions", {})), Jsonb(s.get("styles", {})),
                 s.get("styleMappingNote"), s.get("trademarkNote"), review.get("status", "pending"), review.get("by"),
                 review.get("at"), review.get("note"), Jsonb(s.get("modificationHistory", []))))
            pack_ids[slug] = str(cur.fetchone()[0])

        # Per-icon licenses (e.g. brand logos under MIT or CC-BY) need license rows too.
        for spdx in sorted({d["license"] for d in designs if d.get("license")} - {s["license"]["spdx"] for s in manifest.values()}):
            lname, lurl, osi = LICENSE_NAMES.get(spdx, (spdx, f"https://spdx.org/licenses/{spdx}.html", False))
            cur.execute("""INSERT INTO licenses (id, name, url, text, osi_approved) VALUES (%s,%s,%s,%s,%s)
                           ON CONFLICT (id) DO NOTHING""",
                        (spdx, lname, lurl, f"Full license text: {lurl or 'https://spdx.org/licenses/' + spdx + '.html'}", osi))

        # concepts + categories
        concepts = {}
        for d in designs:
            concepts.setdefault(d["conceptId"], d["concept"])
        cur.executemany("""INSERT INTO concepts (id, slug, name) VALUES (%s,%s,%s)
                           ON CONFLICT (id) DO UPDATE SET slug=EXCLUDED.slug, name=EXCLUDED.name""",
                        [(cid, slug, slug.replace("-", " ")) for cid, slug in concepts.items()])
        cats = sorted({c for d in designs for c in d["categories"]})
        cur.executemany("""INSERT INTO categories (slug, name) VALUES (%s,%s) ON CONFLICT (slug) DO UPDATE SET name=EXCLUDED.name""",
                        [(c, c.replace("-", " ").title()) for c in cats])
        cur.execute("SELECT slug, id FROM categories")
        cat_ids = dict(cur.fetchall())

        # designs
        design_rows, variant_rows = [], []
        for d in designs:
            published = [v["style"] for v in d["variants"] if v["status"] == "published"]
            status = ("published" if published else "pending" if any(v["status"] == "pending" for v in d["variants"])
                      else "quarantined" if any(v["status"] == "quarantined" for v in d["variants"]) else "rejected")
            design_rows.append((
                d["id"], d["conceptId"], pack_ids[d["source"]], d["name"], d["localName"], d["nativeName"], d["namespace"],
                d["area"], d.get("description") or None, d["tags"], d["categories"], d["aliases"], published, d["isBrand"],
                Jsonb(d["derivedFrom"]) if d.get("derivedFrom") else None, status, d.get("codepoint"), d.get("bmpCodepoint"),
                d.get("license") or manifest[d["source"]]["license"]["spdx"], _search_names(d),
                " ".join(d["tags"] + d.get("keywords", []) + d["categories"]),
                Jsonb(d.get("extra") or {}), d.get("keywords", []), d.get("context") or None,
            ))
            for v in d["variants"]:
                o = v.get("outline") or {}
                variant_rows.append((
                    v["id"], d["id"], v["style"], v["nativeStyle"], v["nativeLabel"], v["status"],
                    "approved" if v["status"] == "published" else ("rejected" if v["status"] == "rejected" else "proposed"),
                    v["route"], v["reasons"], v.get("duplicateOf"), v.get("svg"), v.get("svgSha256"), v.get("viewBox"),
                    v["sourcePath"], v["sourceSha256"], o.get("key"), o.get("d"), o.get("advance"),
                    v["status"] == "published" and v["route"] == "font",
                ))
        cur.executemany(
            """INSERT INTO designs (id, concept_id, source_pack_id, name, local_name, native_name, namespace, area, description,
                 tags, category_slugs, alias_names, published_styles, is_brand, derived_from, status, codepoint, bmp_codepoint,
                 license_id, search_names, search_tags, attributes, keywords, context)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
               ON CONFLICT (id) DO UPDATE SET concept_id=EXCLUDED.concept_id, name=EXCLUDED.name, local_name=EXCLUDED.local_name,
                 description=EXCLUDED.description, tags=EXCLUDED.tags, category_slugs=EXCLUDED.category_slugs,
                 alias_names=EXCLUDED.alias_names, published_styles=EXCLUDED.published_styles, is_brand=EXCLUDED.is_brand,
                 derived_from=EXCLUDED.derived_from, status=EXCLUDED.status, codepoint=EXCLUDED.codepoint,
                 bmp_codepoint=EXCLUDED.bmp_codepoint, license_id=EXCLUDED.license_id, search_names=EXCLUDED.search_names,
                 search_tags=EXCLUDED.search_tags, attributes=EXCLUDED.attributes, keywords=EXCLUDED.keywords,
                 context=EXCLUDED.context, updated_at=now()""",
            design_rows)
        cur.executemany(
            """INSERT INTO variants (id, design_id, style, native_style, native_label, status, review_status, route, reasons,
                 duplicate_of_style, svg, svg_sha256, view_box, source_path, source_sha256, outline_key, outline_d,
                 outline_advance, font_supported)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
               ON CONFLICT (id) DO UPDATE SET style=EXCLUDED.style, native_label=EXCLUDED.native_label, status=EXCLUDED.status,
                 review_status=EXCLUDED.review_status, route=EXCLUDED.route, reasons=EXCLUDED.reasons,
                 duplicate_of_style=EXCLUDED.duplicate_of_style, svg=EXCLUDED.svg, svg_sha256=EXCLUDED.svg_sha256,
                 view_box=EXCLUDED.view_box, source_path=EXCLUDED.source_path, source_sha256=EXCLUDED.source_sha256,
                 outline_key=EXCLUDED.outline_key, outline_d=EXCLUDED.outline_d, outline_advance=EXCLUDED.outline_advance,
                 font_supported=EXCLUDED.font_supported, updated_at=now()""",
            variant_rows)

        # categories / tags join tables (replace for loaded designs)
        ids = [d["id"] for d in designs]
        cur.execute("DELETE FROM design_categories WHERE design_id = ANY(%s::uuid[])", (ids,))
        cur.executemany("INSERT INTO design_categories (design_id, category_id) VALUES (%s,%s)",
                        [(d["id"], cat_ids[c]) for d in designs for c in d["categories"]])
        all_tags = sorted({t for d in designs for t in d["tags"]})
        cur.executemany("INSERT INTO tags (slug) VALUES (%s) ON CONFLICT (slug) DO NOTHING", [(t,) for t in all_tags])
        cur.execute("SELECT slug, id FROM tags")
        tag_ids = dict(cur.fetchall())
        cur.execute("DELETE FROM design_tags WHERE design_id = ANY(%s::uuid[])", (ids,))
        with cur.copy("COPY design_tags (design_id, tag_id) FROM STDIN") as cp:
            for d in designs:
                for t in d["tags"]:
                    cp.write_row((d["id"], tag_ids[t]))

        # name registry + aliases: replace per namespace atomically
        namespaces = sorted({d["namespace"] for d in designs})
        cur.execute("DELETE FROM name_registry WHERE namespace = ANY(%s) OR namespace = 'global'", (namespaces,))
        cur.execute("DELETE FROM aliases WHERE namespace = ANY(%s)", (namespaces,))
        reg_rows, alias_rows = [], []
        for d in designs:
            reg_rows.append(("global", d["name"], d["id"], "canonical"))
            reg_rows.append((d["namespace"], d["name"], d["id"], "canonical"))
            if d["area"] != "core" and len(d["localName"]) >= 2 and d["localName"] != d["name"]:
                reg_rows.append((d["namespace"], d["localName"], d["id"], "pack-local"))
            for a in d["aliases"]:
                reg_rows.append((d["namespace"], a, d["id"], "alias"))
                alias_rows.append((d["id"], d["namespace"], a))
        cur.executemany("INSERT INTO name_registry (namespace, name, design_id, kind) VALUES (%s,%s,%s,%s)", reg_rows)
        cur.executemany("INSERT INTO aliases (design_id, namespace, name) VALUES (%s,%s,%s)", alias_rows)

        # codepoints (append-only: an existing different value is an error, never overwritten)
        conflicts = []
        for ns, space in registry.doc["namespaces"].items():
            for subject, cp in space["assignments"].items():
                bmp = registry.bmp_mirror(ns, cp)
                cur.execute("""INSERT INTO codepoint_assignments (namespace, subject, codepoint, bmp_codepoint)
                               VALUES (%s,%s,%s,%s) ON CONFLICT (namespace, subject) DO NOTHING RETURNING 1""",
                            (ns, subject, cp, bmp))
                if cur.fetchone() is None:
                    cur.execute("SELECT codepoint FROM codepoint_assignments WHERE namespace=%s AND subject=%s", (ns, subject))
                    existing = cur.fetchone()[0]
                    if existing != cp:
                        conflicts.append(f"{ns}/{subject}: db U+{existing:X} vs registry U+{cp:X}")
        if conflicts:
            raise RuntimeError("codepoint registry conflicts with database: " + "; ".join(conflicts[:10]))

        # release artifacts
        if release_version:
            summary["release"] = _load_release(cur, root, release_version, pack_ids, upload, overwrite_release)

        stats = compute_stats(cur)
        cur.execute("""INSERT INTO catalog_stats (id, data, computed_at) VALUES ('current', %s, now())
                       ON CONFLICT (id) DO UPDATE SET data=EXCLUDED.data, computed_at=now()""", (Jsonb(stats),))
        cur.execute("INSERT INTO outbox (topic, payload) VALUES ('catalog.published', %s)",
                    (Jsonb({"designs": len(designs), "release": release_version}),))
        cur.execute("INSERT INTO audit_events (actor_id, action, subject_type, subject_id, data) VALUES (%s,'catalog.load','catalog',%s,%s)",
                    (actor, release_version, Jsonb({"designs": len(designs), "variants": len(variant_rows)})))
        conn.commit()
    summary.update({"designs": len(designs), "variants": len(variant_rows), "stats": stats})
    return summary


def _prune_removed(cur, keep: set[str]) -> dict:
    """Delete sources that were removed from the manifest, with their designs and font bundles.
    Releases that contained them are deleted too (only allowed for never-published local releases)."""
    cur.execute("SELECT id, slug FROM source_packs WHERE NOT (slug = ANY(%s))", (sorted(keep),))
    gone = cur.fetchall()
    if not gone:
        return {"sources": []}
    ids = [g[0] for g in gone]
    cur.execute("SELECT DISTINCT r.version, r.published_at FROM releases r JOIN font_bundles fb ON fb.release_id = r.id WHERE fb.source_pack_id = ANY(%s)", (ids,))
    rels = cur.fetchall()
    versions = [r[0] for r in rels]
    cur.execute("DELETE FROM font_bundles WHERE source_pack_id = ANY(%s)", (ids,))
    cur.execute("DELETE FROM designs WHERE source_pack_id = ANY(%s)", (ids,))
    n = cur.rowcount
    # Clear references to the releases being deleted; the new release re-marks them on load.
    cur.execute("SELECT id FROM releases WHERE version = ANY(%s)", (versions,))
    rel_ids = [r[0] for r in cur.fetchall()]
    cur.execute("UPDATE designs SET first_release_id = NULL WHERE first_release_id = ANY(%s)", (rel_ids,))
    cur.execute("UPDATE variants SET first_release_id = NULL WHERE first_release_id = ANY(%s)", (rel_ids,))
    cur.execute("UPDATE variants SET updated_release_id = NULL WHERE updated_release_id = ANY(%s)", (rel_ids,))
    cur.execute("UPDATE kits SET pinned_release_id = NULL WHERE pinned_release_id = ANY(%s)", (rel_ids,))
    cur.execute("DELETE FROM releases WHERE id = ANY(%s)", (rel_ids,))
    cur.execute("DELETE FROM source_packs WHERE id = ANY(%s)", (ids,))
    cur.execute("DELETE FROM build_artifacts")  # cached builds may contain removed artwork
    cur.execute("INSERT INTO audit_events (actor_id, action, subject_type, data) VALUES ('system:catalog-loader','catalog.prune','source_pack',%s)",
                (Jsonb({"sources": [g[1] for g in gone], "designs": n, "releases": [r[0] for r in rels]}),))
    return {"sources": [g[1] for g in gone], "designs": n, "releasesDeleted": [r[0] for r in rels]}


class ReleaseImmutableError(RuntimeError):
    pass


def _put_immutable(storage, key: str, src: Path, overwrite: bool) -> bool:
    """Upload a versioned release object. Existing objects must be byte-identical unless overwrite is set."""
    import hashlib
    if storage.exists(key):
        if hashlib.sha256(storage.get_bytes(key)).hexdigest() == hashlib.sha256(src.read_bytes()).hexdigest():
            return False
        if not overwrite:
            raise ReleaseImmutableError(
                f"{key} already exists with different content. Published releases are immutable: bump the version "
                "(or pass --overwrite-release for an unpublished local build).")
    storage.put_file(key, src, content_type_for(src.name))
    return True


def _load_release(cur, root: Path, version: str, pack_ids: dict, upload: bool, overwrite: bool = False) -> dict:
    rel = root / "dist" / "releases" / version
    index_file = rel / "archives" / "index.json"
    if not index_file.exists():
        return {"skipped": f"{index_file} not found; run the release build first"}
    index = json.loads(index_file.read_text())
    manifest = json.loads((rel / "typeicon-release" / "metadata" / "manifest.json").read_text())
    storage = get_storage() if upload else None
    cur.execute(
        """INSERT INTO releases (version, release_date, status, toolchain, counts, manifest, archive_index)
           VALUES (%s,%s,'published',%s,%s,%s,%s)
           ON CONFLICT (version) DO UPDATE SET release_date=EXCLUDED.release_date, toolchain=EXCLUDED.toolchain,
             counts=EXCLUDED.counts, manifest=EXCLUDED.manifest, archive_index=EXCLUDED.archive_index
           RETURNING id""",
        (version, index["releaseDate"], manifest["toolchain"], Jsonb(index["counts"]), Jsonb(manifest), Jsonb(index)))
    release_id = cur.fetchone()[0]
    cur.execute("UPDATE releases SET published_at = coalesce(published_at, now()) WHERE id=%s", (release_id,))

    uploaded = 0
    cur.execute("DELETE FROM release_archives WHERE release_id=%s", (release_id,))
    for a in index["archives"]:
        key = f"releases/{version}/{a['file']}"
        if storage and _put_immutable(storage, key, rel / "archives" / a["file"], overwrite):
            uploaded += 1
        meta = {k: v for k, v in a.items() if k not in ("kind", "label", "file", "bytes", "sha256")}
        cur.execute("""INSERT INTO release_archives (release_id, kind, label, file, storage_key, bytes, sha256, meta)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (release_id, a["kind"], a["label"], a["file"], key, a["bytes"], a["sha256"], Jsonb(meta)))

    # Web fonts + CSS used by the site itself (keyword demo) and by the docs.
    out = rel / "typeicon-release"
    for sub in ("webfonts", "css"):
        for p in sorted((out / sub).iterdir()):
            key = f"releases/{version}/{sub}/{p.name}"
            if storage and _put_immutable(storage, key, p, overwrite):
                uploaded += 1

    cur.execute("SELECT id, design_id, style FROM variants")
    variant_of = {(str(did), st): str(vid) for vid, did, st in cur.fetchall()}
    cur.execute("SELECT name, id FROM designs")
    design_id_of = {n: str(i) for n, i in cur.fetchall()}
    cur.execute("DELETE FROM font_bundles WHERE release_id=%s", (release_id,))
    for fam in index["families"]:
        files = {}
        for fmt, f in fam["files"].items():
            sub = "desktop" if fmt in ("otf", "ttf") else "webfonts"
            key = f"releases/{version}/{sub}/{f['name']}"
            if sub == "desktop" and storage and _put_immutable(storage, key, out / sub / f["name"], overwrite):
                uploaded += 1
            files[fmt] = {**f, "storageKey": key}
        cur.execute(
            """INSERT INTO font_bundles (release_id, slug, family, postscript_name, source_pack_id, style, part, css_class,
                 glyph_count, keyword_count, files, validation, raster)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
            (release_id, fam["slug"], fam["family"], fam["postscriptName"], pack_ids[fam["source"]], fam["style"],
             fam["part"], fam["cssClass"], fam["glyphs"], fam["keywords"], Jsonb(files), Jsonb(fam["validation"]),
             Jsonb(fam["raster"])))
        bundle_id = cur.fetchone()[0]
        gm = json.loads((out / "metadata" / "glyph-maps" / f"{fam['slug']}.json").read_text())
        rows = []
        for g in gm["glyphs"]:
            vid = variant_of.get((design_id_of[g["name"]], fam["style"]))
            if vid:
                rows.append((bundle_id, vid, g["codepoints"][0], g["keywords"]))
        with cur.copy("COPY glyph_assignments (font_bundle_id, variant_id, codepoint, keywords) FROM STDIN") as cp:
            for r in rows:
                cp.write_row(r)
    cur.execute("""UPDATE variants v SET first_release_id = coalesce(v.first_release_id, %s), updated_release_id = %s
                   WHERE v.status = 'published'""", (release_id, release_id))
    cur.execute("UPDATE designs SET first_release_id = coalesce(first_release_id, %s) WHERE status='published'", (release_id,))
    return {"version": version, "archives": len(index["archives"]), "families": len(index["families"]), "uploaded": uploaded}


def pull_overrides(database_url: str | None = None, root: Path | None = None) -> dict:
    """Export admin metadata edits (metadata_overrides) to the committed overrides file."""
    root = root or repo_root()
    url = database_url or os.environ.get("DATABASE_URL")
    with psycopg.connect(url) as conn:
        rows = conn.execute("SELECT design_name, data, updated_by, updated_at FROM metadata_overrides ORDER BY design_name").fetchall()
    doc = {"$comment": "Generated by `typeicon-import pull-overrides` from admin edits. Applied by `typeicon-import build`.",
           "designs": {name: {**data, "_by": by, "_at": at.isoformat()} for name, data, by, at in rows}}
    path = root / "assets" / "registry" / "overrides.json"
    path.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
    return {"overrides": len(rows), "file": str(path.relative_to(root))}
