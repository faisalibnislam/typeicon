"""Subset and kit builds: selected icons -> small, uniquely named font package ZIP.

Catalog icons are subset from the released fonts with fontTools (explicit glyph set), one
family per (source, style) because pack codepoints are only unique within a pack. Private
custom icons (kits) are compiled with the same OpenType compiler into their own
"Custom <Style>" families. Every output is validated:
  * OpenType Sanitizer + structural checks,
  * HarfBuzz shaping of every selected keyword and alias,
  * a negative check: keywords that were NOT selected stay plain letters, proving the subset
    works on its own without the original font.
The package (fonts, CSS, SVG, metadata, licenses, README, checksums) is zipped
deterministically and stored under builds/public/... or builds/private/<owner>/...
"""
from __future__ import annotations

import json
import re
import shutil
import tempfile
from pathlib import Path

import psycopg
from fontTools.svgLib.path import parse_path
from pathops import Path as PathopsPath
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from typeicon_fonts.compiler import FontSpec, GlyphSpec, compile_font
from typeicon_fonts.subset import save_formats, subset_font
from typeicon_fonts.validate import Shaper, validate_font
from typeicon_import.packaging import write_checksums, write_zip
from typeicon_import.storage import get_storage

from .queue import Job, PermanentError

STYLE_TITLE = {"filled": "Filled", "line": "Line", "rounded": "Rounded", "thin": "Thin", "brand": "Brands"}
PACK_TITLE = {"typeicon-core": "", "simple-icons": "", "custom": "Custom"}
FONT_FORMATS = ("otf", "ttf", "woff2", "woff")


def _keywords(row: dict) -> list[str]:
    kws = [row["name"]]
    if row.get("area") != "core" and len(row["local_name"]) >= 2 and row["local_name"] != row["name"]:
        kws.append(row["local_name"])
    kws += [a for a in (row.get("alias_names") or []) if a not in kws]
    return kws


def load_variants(conn, variant_ids: list[str]) -> list[dict]:
    return conn.execute(
        """SELECT v.id::text AS variant_id, v.style, v.native_label, v.route, v.font_supported, v.svg, v.svg_sha256,
                  v.view_box, d.id::text AS design_id, d.name, d.local_name, d.area, d.alias_names, d.codepoint,
                  d.bmp_codepoint, d.license_id, sp.slug AS source, sp.display_name AS source_name
           FROM variants v JOIN designs d ON d.id = v.design_id JOIN source_packs sp ON sp.id = d.source_pack_id
           WHERE v.id = ANY(%s::uuid[]) AND v.status = 'published' AND d.status = 'published'
           ORDER BY sp.slug, v.style, d.codepoint""", (variant_ids,)).fetchall()


def _family_names(slug: str, hash6: str, source: str, style: str) -> tuple[str, str]:
    pack = PACK_TITLE.get(source, source.title())
    family = " ".join(x for x in ("TypeIcon Kit", slug, hash6, pack, STYLE_TITLE[style]) if x)
    ps = re.sub(r"[^A-Za-z0-9]", "", f"TypeIconKit{hash6}{pack}{STYLE_TITLE[style]}")[:55] + "-Regular"
    return family, ps


def build_package(job: Job, database_url: str, *, name: str, slug: str, formats: list[str], release: str,
                  variant_ids: list[str], custom_icon_ids: list[str], owner_id: str | None,
                  hosted_embed: tuple[str, int] | None = None) -> dict:
    if not re.fullmatch(r"[a-z0-9-]{1,32}", slug):
        raise PermanentError("invalid project slug")
    formats = [f for f in formats if f in (*FONT_FORMATS, "svg", "css")]
    hash6 = (job.cache_key or "000000")[:6]
    storage = get_storage()
    with psycopg.connect(database_url, row_factory=dict_row) as conn:
        rows = load_variants(conn, variant_ids)
        if len(rows) != len(variant_ids):
            raise PermanentError(f"{len(variant_ids) - len(rows)} selected variants are no longer published")
        custom = []
        if custom_icon_ids:
            # Ownership is enforced again here: a job can only package its owner's custom icons.
            custom = conn.execute(
                """SELECT id::text, name, style, svg, svg_sha256, outline_d, outline_advance, codepoint, route
                   FROM custom_icons WHERE id = ANY(%s::uuid[]) AND owner_id = %s AND status = 'ready' AND archived_at IS NULL
                   ORDER BY style, codepoint""", (custom_icon_ids, owner_id)).fetchall()
            if len(custom) != len(custom_icon_ids):
                raise PermanentError("some custom icons are missing, not ready, or not owned by this user")
        rel = conn.execute("SELECT id FROM releases WHERE version = %s", (release,)).fetchone()
        if not rel:
            raise PermanentError(f"release {release} not found")
        bundles = conn.execute(
            """SELECT fb.id, fb.slug, fb.family, fb.style, fb.css_class, fb.files, sp.slug AS source
               FROM font_bundles fb JOIN source_packs sp ON sp.id = fb.source_pack_id WHERE fb.release_id = %s""",
            (rel["id"],)).fetchall()
        selected_ids = [r["variant_id"] for r in rows] or ["00000000-0000-0000-0000-000000000000"]
        unselected = {b["slug"]: [x["kw"] for x in conn.execute(
            """SELECT ga.keywords[1] AS kw FROM glyph_assignments ga
               WHERE ga.font_bundle_id = %s AND ga.variant_id <> ALL(%s::uuid[]) ORDER BY ga.codepoint LIMIT 8""",
            (b["id"], selected_ids)).fetchall()] for b in bundles}
        licenses = {r["id"]: r for r in conn.execute("SELECT id, name, text FROM licenses").fetchall()}
        sources = {r["slug"]: r for r in conn.execute(
            "SELECT slug, display_name, copyright, attribution_text, attribution_required, license_id FROM source_packs").fetchall()}

    work = Path(tempfile.mkdtemp(prefix="typeicon-kit-"))
    root = work / f"typeicon-kit-{slug}-{hash6}"
    try:
        root.mkdir()
        groups: dict[tuple[str, str], list[dict]] = {}
        svg_only = []
        for r in rows:
            if r["font_supported"] and r["route"] == "font":
                groups.setdefault((r["source"], r["style"]), []).append(r)
            else:
                svg_only.append(r)
        want_fonts = [f for f in formats if f in FONT_FORMATS]
        need = set(want_fonts) | ({"woff2", "woff"} if "css" in formats else set())
        families = []

        def place(written: dict[str, Path], expected: dict[str, str]) -> dict[str, str]:
            out = {}
            for fmt, path in written.items():
                dest_dir = root / ("desktop" if fmt in ("otf", "ttf") else "webfonts")
                dest_dir.mkdir(exist_ok=True)
                dest = dest_dir / path.name
                shutil.move(str(path), dest)
                rep = validate_font(dest, expected)
                if not rep.ok:
                    raise RuntimeError(f"{dest.name} failed validation: {rep.errors[:3]}")
                out[fmt] = f"{dest_dir.name}/{dest.name}"
            return out

        def negative_check(files: dict[str, str], probes: list[str], expected: dict[str, str]) -> int:
            probe_file = root / (files.get("otf") or files.get("ttf") or files.get("woff2"))
            shaper = Shaper(probe_file)
            checked = 0
            for probe in probes:
                if probe in expected:
                    continue
                checked += 1
                if len(shaper.glyph_names(probe)) == 1:  # keywords are >= 2 chars: one glyph means a ligature fired
                    raise RuntimeError(f"subset leaked unselected keyword {probe!r}")
            return checked

        if need:
            for (source, style), items in sorted(groups.items()):
                bundle = next((b for b in bundles if b["source"] == source and b["style"] == style), None)
                if bundle is None:
                    raise PermanentError(f"no released font for {source}/{style}")
                family, ps = _family_names(slug, hash6, source, style)
                glyphs = [f"u{r['codepoint']:X}" for r in items]
                expected = {kw: f"u{r['codepoint']:X}" for r in items for kw in _keywords(r)}
                files: dict[str, str] = {}
                for src_fmt, outs in (("otf", [f for f in need if f == "otf"]),
                                      ("ttf", [f for f in need if f in ("ttf", "woff2", "woff")])):
                    if not outs:
                        continue
                    res = subset_font(storage.get_bytes(bundle["files"][src_fmt]["storageKey"]), glyphs, family, ps, hash6)
                    files |= place(save_formats(res.font, root / "_tmp", ps, outs), expected)
                families.append({
                    "family": family, "postscriptName": ps, "source": source, "style": style,
                    "cssClass": f"typeicon-kit-{hash6}-{source}-{style}", "files": files, "method": "fonttools-subset",
                    "negativeChecks": negative_check(files, unselected.get(bundle["slug"], []), expected),
                    "glyphs": [{"name": r["name"], "keywords": _keywords(r), "codepoint": r["codepoint"],
                                "codepointHex": f"U+{r['codepoint']:X}"} for r in items],
                })
            custom_font = [c for c in custom if c["route"] == "font" and c["outline_d"]]
            for style in sorted({c["style"] for c in custom_font}):
                items = [c for c in custom_font if c["style"] == style]
                family, ps = _family_names(slug, hash6, "custom", style)
                specs = []
                for c in items:
                    p = PathopsPath()
                    parse_path(c["outline_d"], p.getPen())
                    specs.append(GlyphSpec(f"u{c['codepoint']:X}", [c["codepoint"]], [c["name"]], p, c["outline_advance"]))
                spec = FontSpec(family=family, ps_name=ps, version="0.1.0", glyphs=specs,
                                copyright="Custom icons: copyright their uploader. Font compilation: TypeIcon.",
                                license_description="Custom icons uploaded by the kit owner; the owner is responsible for their rights.",
                                description="TypeIcon kit font with private custom icons.")
                expected = {c["name"]: f"u{c['codepoint']:X}" for c in items}
                files = place(compile_font(spec, root / "_tmp", ps, formats=tuple(sorted(need))), expected)
                families.append({
                    "family": family, "postscriptName": ps, "source": "custom", "style": style,
                    "cssClass": f"typeicon-kit-{hash6}-custom-{style}", "files": files, "method": "compiled",
                    "glyphs": [{"name": c["name"], "keywords": [c["name"]], "codepoint": c["codepoint"],
                                "codepointHex": f"U+{c['codepoint']:X}"} for c in items],
                })
            shutil.rmtree(root / "_tmp", ignore_errors=True)

        css_text = None
        if "css" in formats:
            css = ["/*! TypeIcon kit. Generated file. */"]
            for f in families:
                srcs = [f'url("../{f["files"][x]}") format("{x}")' for x in ("woff2", "woff") if x in f["files"]]
                css.append(f'@font-face {{ font-family: "{f["family"]}"; src: {", ".join(srcs)}; font-weight: 400; '
                           'font-style: normal; font-display: block; }')
            css.append('.fi { display: inline-block; font-style: normal; font-weight: 400; line-height: 1; letter-spacing: normal; '
                       'text-transform: none; white-space: nowrap; direction: ltr; vertical-align: -0.125em; '
                       'font-feature-settings: "liga" 1, "rlig" 1; -webkit-font-smoothing: antialiased; }')
            css.append("@media (prefers-reduced-motion: reduce) { .fi { animation: none !important; } }")
            for f in families:
                css.append(f'.{f["cssClass"]} {{ font-family: "{f["family"]}"; }}')
                for g in f["glyphs"]:
                    css.append(f'.{f["cssClass"]}.typeicon-{g["name"]}::before {{ content: "\\{g["codepoint"]:X}"; }}')
            css_text = "\n".join(css) + "\n"
            (root / "css").mkdir(exist_ok=True)
            (root / "css" / "kit.css").write_text(css_text)

        if "svg" in formats:
            for r in [*rows, *custom]:
                if not r.get("svg"):
                    continue
                d = root / "svg" / r["style"]
                d.mkdir(parents=True, exist_ok=True)
                svg = r["svg"] if "xmlns=" in r["svg"] else r["svg"].replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
                (d / f"{r['name']}.svg").write_text(svg + "\n")

        used_sources = sorted({r["source"] for r in rows})
        lic_dir = root / "licenses"
        lic_dir.mkdir()
        attribution = ["# Licenses and attribution", ""]
        for s in used_sources:
            src = sources[s]
            lic = licenses[src["license_id"]]
            (lic_dir / s).mkdir()
            (lic_dir / s / "LICENSE").write_text(lic["text"])
            attribution += [f"## {src['display_name']}", f"- License: {lic['id']} ({lic['name']})", f"- Copyright: {src['copyright']}"]
            if src["attribution_required"] and src["attribution_text"]:
                attribution.append(f"- Attribution: {src['attribution_text']}")
            attribution.append("")
        if custom:
            attribution += ["## Custom icons", "- Uploaded privately by the kit owner, who is responsible for having the right to use them.", ""]
        if "typeicon-core" not in used_sources and families:
            core = sources["typeicon-core"]
            (lic_dir / "typeicon-core").mkdir(exist_ok=True)
            (lic_dir / "typeicon-core" / "LICENSE").write_text(licenses[core["license_id"]]["text"])
            attribution += ["## TypeIcon fallback letterforms", "- Covered by the TypeIcon Core license.", ""]
        (lic_dir / "ATTRIBUTION.md").write_text("\n".join(attribution))

        manifest = {
            "kind": "typeicon-kit" if custom_icon_ids or hosted_embed else "typeicon-subset",
            "name": name, "slug": slug, "hash": hash6, "release": release, "formats": formats,
            "families": families,
            "svgOnly": [{"name": r["name"], "style": r["style"]} for r in svg_only] +
                       [{"name": c["name"], "style": c["style"]} for c in custom if c["route"] != "font"],
            "items": [{"name": r["name"], "style": r["style"], "variantId": r["variant_id"], "source": r["source"],
                       "license": r["license_id"], "svgSha256": r["svg_sha256"]} for r in rows] +
                     [{"name": c["name"], "style": c["style"], "customIconId": c["id"], "source": "custom",
                       "svgSha256": c["svg_sha256"]} for c in custom],
        }
        (root / "metadata").mkdir()
        (root / "metadata" / "kit.json").write_text(json.dumps(manifest, indent=1) + "\n")
        readme = [f"# {name}: TypeIcon {'kit' if manifest['kind'] == 'typeicon-kit' else 'subset'}", "",
                  f"Built from TypeIcon release {release}. {len(rows) + len(custom)} icon styles.", ""]
        if families:
            readme += ["## Font families", "", "Install the OTF files in `desktop/` for Figma and other desktop apps,",
                       "then choose exactly one of these family names:", "", "| Family | Icons |", "|---|---:|"]
            readme += [f"| {f['family']} | {len(f['glyphs'])} |" for f in families]
            readme += ["", "Family names include this build's hash so they never collide with the full TypeIcon fonts",
                       "or another subset in font caches. Type a keyword with ligatures enabled; see metadata/kit.json.", ""]
        if manifest["svgOnly"]:
            readme += ["Some icons are SVG-only (they cannot be represented as font outlines) and are in `svg/` only.", ""]
        readme += ['Web: link `css/kit.css` and use `<span class="typeicon <family class>" aria-hidden="true">keyword</span>`.',
                   "Verify files with `shasum -a 256 -c checksums.sha256`. Licenses are in `licenses/`.", ""]
        (root / "README.md").write_text("\n".join(readme))
        write_checksums(root)

        zip_name = f"typeicon-kit-{slug}-{hash6}.zip"
        info = write_zip(work / zip_name, root, [x for x in root.rglob("*") if x.is_file()], root.name)
        scope_path = "public" if job.scope == "public" else f"private/{owner_id}"
        key = f"builds/{scope_path}/{job.cache_key}/{zip_name}"
        storage.put_file(key, work / zip_name, "application/zip")

        hosted = False
        if hosted_embed and css_text:
            embed_id, version = hosted_embed
            flat = css_text.replace('url("../webfonts/', 'url("./')
            for f in families:
                for fmt in ("woff2", "woff"):
                    if fmt in f["files"]:
                        storage.put_file(f"kits/{embed_id}/v{version}/{Path(f['files'][fmt]).name}", root / f["files"][fmt], f"font/{fmt}")
            storage.put_bytes(f"kits/{embed_id}/v{version}/kit.css", flat.encode(), "text/css; charset=utf-8")
            hosted = True

        summary = {k: manifest[k] for k in ("name", "slug", "hash", "release", "formats", "svgOnly")} | {
            "families": [{k: f[k] for k in ("family", "postscriptName", "source", "style", "cssClass", "method")} |
                         {"glyphs": len(f["glyphs"]), "negativeChecks": f.get("negativeChecks", 0)} for f in families]}
        result = {"storageKey": key, "fileName": zip_name, "bytes": info["bytes"], "sha256": info["sha256"],
                  "manifest": summary, "hosted": hosted}
        with psycopg.connect(database_url) as conn:
            conn.execute(
                """INSERT INTO build_artifacts (scope, cache_key, storage_key, file_name, bytes, sha256, manifest, job_id)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (scope, cache_key) DO NOTHING""",
                (job.scope, job.cache_key, key, zip_name, info["bytes"], info["sha256"], Jsonb(summary), job.id))
        return result
    finally:
        shutil.rmtree(work, ignore_errors=True)


def run_subset_build(job: Job, database_url: str) -> dict:
    p = job.payload
    if job.scope != "public":
        raise PermanentError("subset builds contain public catalog assets only")
    return build_package(job, database_url, name=p["name"], slug=p["slug"], formats=p["formats"], release=p["release"],
                         variant_ids=[i["variantId"] for i in p["items"]], custom_icon_ids=[], owner_id=job.owner_id)
