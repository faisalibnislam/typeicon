"""Catalog build: pinned sources -> sanitized SVGs + font-ready outlines + catalog files.

Idempotent and resumable: outline conversion results are cached by the sanitized SVG's
sha256 and the toolchain version, so re-running only processes new or changed artwork.
`--dry-run` performs every check and writes the report, but leaves the registry and the
catalog output untouched.
"""
from __future__ import annotations

import hashlib
import json
import os
import uuid
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from dataclasses import asdict
from datetime import date
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen

from typeicon_fonts.compiler import TOOLCHAIN_VERSION
from typeicon_fonts.outline import OutlineError, svg_to_outline
from typeicon_fonts.svg_sanitize import SvgRejected, sanitize_svg

from .adapters import ADAPTERS, NAME_RE, RawIcon, kebab
from .registry import CodepointRegistry, NameRegistry
from .sources import Source, load_manifest, repo_root, source_dir

ID_NS = uuid.UUID("7b0b5a0e-5f7c-4d57-9a47-6f6e7469636f")  # fixed namespace for TypeIcon uuid5 ids
STYLE_ORDER = ["filled", "line", "rounded", "thin"]


def stable_id(kind: str, *parts: str) -> str:
    return str(uuid.uuid5(ID_NS, ":".join((kind, *parts))))


def _fmt(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def _process(args: tuple[str, str]) -> dict:
    """Worker: sanitize one original file and convert it to a font outline (cached)."""
    path, cache_dir = args
    data = Path(path).read_bytes()
    out: dict = {"sourceSha256": hashlib.sha256(data).hexdigest()}
    try:
        san = sanitize_svg(data)
    except SvgRejected as e:
        return {**out, "route": "rejected", "reasons": [f"sanitize: {e}"]}
    svg_sha = hashlib.sha256(san.svg.encode()).hexdigest()
    out.update(svg=san.svg, svgSha256=svg_sha, viewBox=list(san.view_box), route=san.route,
               reasons=san.reasons, removed=san.removed)
    if san.route != "font":
        return out
    key = hashlib.sha256(f"{svg_sha}|{TOOLCHAIN_VERSION}".encode()).hexdigest()[:40]
    cache_file = Path(cache_dir) / key[:2] / f"{key}.json"
    if cache_file.exists():
        out["outline"] = json.loads(cache_file.read_text())
        return out
    try:
        o = svg_to_outline(san.svg)
    except (OutlineError, SvgRejected) as e:
        return {**out, "route": "svg-only", "reasons": [f"outline: {e}"]}
    except Exception as e:  # noqa: BLE001 - a geometry-library fault on one icon must not stop the whole build
        return {**out, "route": "svg-only", "reasons": [f"outline: {type(e).__name__}: {e}"]}
    pen = SVGPathPen(None, ntos=_fmt)
    o.path.draw(pen)
    outline = {"key": key, "d": pen.getCommands(), "advance": o.advance,
               "bounds": [round(b, 2) for b in o.path.bounds], "warnings": o.warnings}
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    tmp = cache_file.with_suffix(f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(outline))
    tmp.replace(cache_file)
    out["outline"] = outline
    return out


def geometry_signature(svg: str) -> str:
    """Signature of drawn geometry, ignoring root attributes that do not change shape."""
    import re
    body = re.sub(r"^<svg[^>]*>", "", svg)
    root_attrs = re.match(r"^<svg([^>]*)>", svg)
    paint = ""
    if root_attrs:
        attrs = dict(re.findall(r'([\w:-]+)="([^"]*)"', root_attrs.group(1)))
        paint = "|".join(f"{k}={attrs[k]}" for k in sorted(attrs) if k.startswith("stroke") or k in ("fill", "viewBox"))
    return hashlib.sha256((paint + body).encode()).hexdigest()


def build_catalog(root: Path | None = None, only: list[str] | None = None, offline: bool = False,
                  dry_run: bool = False, workers: int | None = None, log=print) -> dict:
    root = root or repo_root()
    sources = [s for s in load_manifest(root) if not only or s.slug in only]
    registry = CodepointRegistry(root / "assets" / "registry" / "codepoints.json")
    names = NameRegistry()
    cache_dir = root / ".cache" / "outlines"
    out_dir = root / "build" / "catalog"
    reserved_prefixes = {s.prefix for s in load_manifest(root) if s.prefix}

    raws: list[tuple[Source, RawIcon]] = []
    for src in sources:
        base = source_dir(src, root, offline=offline)
        count = 0
        for raw in ADAPTERS[src.slug](src, base):
            raws.append((src, raw))
            count += 1
        log(f"[{src.slug}] {count} original files from {base}")

    log(f"processing {len(raws)} SVGs with {workers or os.cpu_count()} workers ...")
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(_process, [(str(r.path), str(cache_dir)) for _, r in raws], chunksize=64))

    report: dict = {"generatedFor": TOOLCHAIN_VERSION, "sources": {}, "nameCollisions": [], "errors": []}
    designs: dict[tuple[str, str], dict] = {}
    for (src, raw), res in zip(raws, results):
        rep = report["sources"].setdefault(src.slug, defaultdict(int))
        rep["files"] += 1
        local = kebab(raw.native_name)
        if not NAME_RE.match(local) or (src.area == "core" and len(local) < 2):
            rep["rejectedName"] += 1
            report["errors"].append(f"{src.slug}: unusable name {raw.native_name!r}")
            continue
        name = local if src.area == "core" else f"{src.prefix}-{local}"
        key = (src.slug, local)
        d = designs.get(key)
        if d is None:
            if src.area == "core" and any(local.startswith(p + "-") for p in reserved_prefixes):
                report["errors"].append(f"core name {local!r} uses a reserved pack prefix")
                continue
            if not names.claim("global", name, f"{src.slug}/{raw.native_name}", "canonical name"):
                report["nameCollisions"].append(name)
                rep["nameCollision"] += 1
                continue
            d = designs[key] = {
                "id": stable_id("design", src.slug, raw.native_name),
                "source": src.slug, "area": src.area, "namespace": src.namespace,
                "name": name, "localName": local, "nativeName": raw.native_name,
                "concept": local, "conceptId": stable_id("concept", local),
                "description": raw.description, "tags": [], "categories": [], "aliases": list(raw.aliases),
                "isBrand": raw.is_brand, "derivedFrom": raw.derived_from, "variants": [],
                "license": raw.license or src["license"]["spdx"], "extra": raw.extra,
                "keywords": list(raw.keywords), "context": raw.context,
            }
        elif raw.native_name != d["nativeName"]:
            report["nameCollisions"].append(f"{src.slug}: {raw.native_name!r} and {d['nativeName']!r} both normalise to {local!r}")
            rep["nameCollision"] += 1
            continue
        for t in raw.tags:
            if t not in d["tags"]:
                d["tags"].append(t)
        for c in raw.categories:
            if c and c not in d["categories"]:
                d["categories"].append(c)
        status = "published" if src.approved else "pending"
        reasons_extra = []
        allowed = src.get("allowedLicenses")
        lic = raw.license or src["license"]["spdx"]
        if (allowed is not None and lic not in allowed) or lic in set(src.get("blockedLicenses", [])):
            # Allowlist: copyleft / share-alike / non-commercial / no-derivatives / custom artwork is never redistributed.
            status = "quarantined"
            reasons_extra.append(f"license {raw.license} is not compatible with TypeIcon redistribution")
        if res["route"] == "rejected":
            status = "rejected"
        variant = {
            "id": stable_id("variant", src.slug, raw.native_name, raw.native_style),
            "style": raw.style, "nativeStyle": raw.native_style,
            "nativeLabel": src["styles"][raw.native_style].get("nativeLabel", raw.native_style),
            "sourcePath": raw.rel_path, "sourceSha256": res["sourceSha256"],
            "svg": res.get("svg"), "svgSha256": res.get("svgSha256"), "viewBox": res.get("viewBox"),
            "route": res["route"], "reasons": res.get("reasons", []) + reasons_extra, "status": status,
            "outline": res.get("outline"), "duplicateOf": None,
        }
        if any(v["style"] == raw.style for v in d["variants"]):
            report["errors"].append(f"{name}: two source files map to style {raw.style}")
            continue
        d["variants"].append(variant)

    # Admin metadata overrides (exported from the database by `typeicon-import pull-overrides`).
    overrides_file = root / "assets" / "registry" / "overrides.json"
    if overrides_file.exists():
        overrides = json.loads(overrides_file.read_text()).get("designs", {})
        for d in designs.values():
            o = overrides.get(d["name"])
            if not o:
                continue
            for field in ("description", "tags", "categories", "aliases", "keywords", "context"):
                if field in o:
                    d[field] = o[field]
            report.setdefault("overridesApplied", 0)
            report["overridesApplied"] += 1

    # Identical geometry across styles of one design is published once, never as two styles.
    for d in designs.values():
        d["variants"].sort(key=lambda v: STYLE_ORDER.index(v["style"]) if v["style"] in STYLE_ORDER else 99)
        seen: dict[str, str] = {}
        pref = sorted(d["variants"], key=lambda v: {"line": 0, "rounded": 1, "filled": 2, "thin": 3}.get(v["style"], 9))
        for v in pref:
            if not v["svg"] or v["status"] == "rejected":
                continue
            sig = geometry_signature(v["svg"])
            if sig in seen:
                v["duplicateOf"] = seen[sig]
                v["status"] = "rejected"
                v["reasons"] = v["reasons"] + [f"identical geometry to {seen[sig]} style"]
                report["sources"][d["source"]]["identicalGeometry"] += 1
            else:
                seen[sig] = v["style"]

    # Names and aliases in each font namespace.
    for d in sorted(designs.values(), key=lambda d: (d["source"], d["name"])):
        ns = d["namespace"]
        names.claim(ns, d["name"], d["id"], "canonical")
        # Pack-local keywords shorter than 2 characters are never compiled (they would
        # replace a single letter everywhere); the namespaced canonical name still works.
        if d["area"] != "core" and len(d["localName"]) >= 2:
            names.claim(ns, d["localName"], d["id"], "pack-local keyword")
    for d in sorted(designs.values(), key=lambda d: (d["source"], d["name"])):
        ok_aliases = []
        for a in d["aliases"]:
            if NAME_RE.match(a) and len(a) >= 2 and names.claim(d["namespace"], a, d["id"], "alias"):
                ok_aliases.append(a)
        d["aliases"] = ok_aliases
    report["nameCollisions"] += names.errors

    # Codepoints: Core per concept (shared by the three style fonts); packs per design.
    by_ns: dict[str, list[dict]] = defaultdict(list)
    for d in designs.values():
        if any(v["status"] in ("published", "pending") for v in d["variants"]):
            by_ns[d["namespace"]].append(d)
    for ns, ds in by_ns.items():
        # New Core base designs are allocated before variants, so the limited BMP mirror goes to drawn concepts first.
        is_var = lambda d: bool((d.get("extra") or {}).get("variantOf"))  # noqa: E731
        subjects = [d["concept"] if ns == "core" else d["name"]
                    for d in sorted(ds, key=lambda d: (is_var(d), d["concept"] if ns == "core" else d["name"]))]
        assigned = registry.allocate(ns, subjects)
        for d in ds:
            cp = assigned[d["concept"] if ns == "core" else d["name"]]
            d["codepoint"] = cp
            d["bmpCodepoint"] = registry.bmp_mirror(ns, cp)

    for slug, rep in report["sources"].items():
        ds = [d for d in designs.values() if d["source"] == slug]
        rep["designs"] = len(ds)
        rep["variantsPublished"] = sum(v["status"] == "published" for d in ds for v in d["variants"])
        rep["variantsFontReady"] = sum(v["status"] == "published" and v["route"] == "font" for d in ds for v in d["variants"])
        rep["variantsSvgOnly"] = sum(v["status"] == "published" and v["route"] == "svg-only" for d in ds for v in d["variants"])
        rep["variantsRejected"] = sum(v["status"] == "rejected" for d in ds for v in d["variants"])
        rep["variantsQuarantined"] = sum(v["status"] == "quarantined" for d in ds for v in d["variants"])
        reasons: dict[str, int] = defaultdict(int)
        for d in ds:
            for v in d["variants"]:
                for r in v["reasons"]:
                    reasons[r.split(":")[0] if r.startswith(("outline", "sanitize")) else r] += 1
        rep["reasons"] = dict(sorted(reasons.items(), key=lambda kv: -kv[1]))
        report["sources"][slug] = dict(rep)
    report["newCodepoints"] = len(registry.new_assignments)
    report["totalDesigns"] = len(designs)

    if dry_run:
        log("dry run: registry and catalog not written")
        return report

    out_dir.mkdir(parents=True, exist_ok=True)
    if only and (out_dir / "designs.jsonl").exists():
        # Partial import: keep every other source's designs from the previous build.
        built = {d["source"] for d in designs.values()} | set(only)
        with (out_dir / "designs.jsonl").open() as fh:
            for line in fh:
                prev = json.loads(line)
                if prev["source"] not in built:
                    designs[(prev["source"], prev["localName"])] = prev
    with (out_dir / "designs.jsonl.tmp").open("w") as fh:
        for d in sorted(designs.values(), key=lambda d: (d["source"] != "typeicon-core", d["source"], d["name"])):
            fh.write(json.dumps(d, separators=(",", ":")) + "\n")
    (out_dir / "designs.jsonl.tmp").replace(out_dir / "designs.jsonl")
    (out_dir / "sources.json").write_text(json.dumps([s.raw for s in load_manifest(root)], indent=2))
    (out_dir / "report.json").write_text(json.dumps(report, indent=2, default=dict))
    (out_dir / "meta.json").write_text(json.dumps({
        "toolchain": TOOLCHAIN_VERSION, "builtOn": date.today().isoformat(),
        "sources": {s.slug: s.version for s in sources},
    }, indent=2))
    if registry.save():
        log(f"registry: {len(registry.new_assignments)} new codepoint assignments")
    return report


def load_designs(root: Path | None = None) -> list[dict]:
    root = root or repo_root()
    path = root / "build" / "catalog" / "designs.jsonl"
    with path.open() as fh:
        return [json.loads(line) for line in fh if line.strip()]


__all__ = ["build_catalog", "load_designs", "stable_id", "asdict"]
