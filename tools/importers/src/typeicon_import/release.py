"""Release builder: compile, validate and package a complete TypeIcon release.

Output layout (dist/releases/<version>/typeicon-release/):
  desktop/    OTF (CFF) + TTF per family
  webfonts/   WOFF2 + WOFF per family
  css/        typeicon.css (Core) and typeicon-<pack>.css
  svg/        sanitized SVGs: svg/<source>/<style>/<name>.svg
  sprites/    <source>-<style>.svg symbol sprites (ids: typeicon-<style>-<name>)
  metadata/   icons.json, families.json, glyph-maps/<family>.json, manifest.json, typeicon.d.ts
  licenses/   per-source LICENSE files, NOTICE, ATTRIBUTION.md
  examples/   ligatures.html, css-classes.html, svg-sprite.html, react/, vue/
  README.md
  checksums.sha256
Archives (dist/releases/<version>/archives/) are deterministic ZIPs with an index.json.
A release is refused if any family fails OTS, shaping, clipping or raster checks.
"""
from __future__ import annotations

import html
import json
import os
import shutil
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from typeicon_fonts.compiler import TOOLCHAIN_VERSION, FontSpec, compile_font
from typeicon_fonts.validate import validate_font

from .build import load_designs
from .families import Family, codepoints_for, glyph_spec, keywords_for, plan_families
from .packaging import sha256_file as _sha256
from .packaging import write_zip as _write_zip
from .sources import load_manifest, repo_root

RESERVED_CLASS_NAMES = {
    "filled", "line", "rounded", "thin", "spin", "pulse", "fw", "xs", "sm", "lg", "xl", "2x", "3x", "4x", "5x",
    "rotate-90", "rotate-180", "rotate-270", "flip-horizontal", "flip-vertical", "flip-both",
    "sr-only", "inverse", "stack", "border",
}


class ReleaseError(RuntimeError):
    pass


def _license_line(src: dict) -> str:
    return f"{src['displayName']} ({src['license']['spdx']}); {src['copyright']}"


def _compile_family(args) -> dict:
    """Worker: compile one family and validate every format."""
    fam_dict, entries, version, epoch, sources_by_slug, out_root = args
    fam = Family(**fam_dict, entries=[])
    src = sources_by_slug[fam.source]
    glyphs = [glyph_spec(d, v) for d, v in entries]
    notices = [f"Contains artwork from {_license_line(src)}."]
    if src["attribution"].get("required"):
        notices.append(f"Attribution: {src['attribution']['text']}.")
    spec = FontSpec(
        family=fam.family, ps_name=fam.ps_name, version=version, glyphs=glyphs,
        copyright=src["copyright"] + ("" if fam.area == "core" else "; font compilation (c) TypeIcon"),
        license_description=f"Icon artwork: {src['license']['spdx']}. See licenses/ in the TypeIcon release.",
        extra_notices=notices, build_epoch=epoch,
        description=(f"TypeIcon {fam.style} icon font ({src['displayName']}). "
                     "Type an icon keyword with ligatures enabled, or use the private-use codepoints."),
    )
    out_root = Path(out_root)
    written = compile_font(spec, out_root / "_fonts", fam.file_base)
    expected = {kw: g.glyph_name for g in glyphs for kw in g.keywords}
    results = {}
    for fmt, p in written.items():
        rep = validate_font(p, expected if fmt in ("otf", "ttf", "woff2") else None)
        results[fmt] = {"ok": rep.ok, "errors": rep.errors, "stats": rep.stats}
    return {"slug": fam.slug, "files": {k: str(v) for k, v in written.items()}, "validation": results,
            "glyphs": len(glyphs), "keywords": len(expected)}


RASTER_RECHECK_BELOW = 0.97


def _raster_check(fam: Family, font_file: Path, sample: int | None) -> dict:
    from typeicon_fonts.raster import compare, compare_aligned
    entries = fam.entries
    if sample and len(entries) > sample:
        step = len(entries) / sample
        entries = [entries[int(i * step)] for i in range(sample)]
    worst, total, rechecked = [], 0.0, 0
    for d, v in entries:
        iou = compare(v["svg"], str(font_file), d["codepoint"], px=96).iou
        if iou < RASTER_RECHECK_BELOW:
            # resvg and FreeType round partly covered edge pixels differently; for small shapes on fractional
            # coordinates that alone costs several % at 96 px. A real outline error persists at 384 px.
            iou = compare_aligned(v["svg"], str(font_file), d["codepoint"], px=384, max_shift=1)
            if iou < RASTER_RECHECK_BELOW:  # many tiny shapes: edge pixels weigh more, so look at twice the size
                iou = compare_aligned(v["svg"], str(font_file), d["codepoint"], px=768, max_shift=1)
            rechecked += 1
        total += iou
        worst.append((round(iou, 4), d["name"]))
    worst.sort()
    return {"checked": len(entries), "minIoU": worst[0][0] if worst else None,
            "meanIoU": round(total / max(1, len(entries)), 4), "worst": worst[:5], "px": 96,
            "recheckedAtLargerSize": rechecked}


def _css_for(families: list[Family], designs_by_family: dict[str, list[dict]], font_url: str, core: bool) -> str:
    out = ["/*! TypeIcon. Generated by typeicon-import release. Do not edit. */"]
    for fam in families:
        out.append(
            "@font-face {\n"
            f'  font-family: "{fam.family}";\n'
            f'  src: url("{font_url}/{fam.file_base}.woff2") format("woff2"),\n'
            f'       url("{font_url}/{fam.file_base}.woff") format("woff");\n'
            "  font-weight: 400;\n  font-style: normal;\n  font-display: block;\n}"
        )
    if core:
        out.append(
            ".typeicon {\n  display: inline-block;\n  font-style: normal;\n  font-weight: 400;\n  font-variant: normal;\n"
            "  line-height: 1;\n  letter-spacing: normal;\n  word-spacing: normal;\n  text-transform: none;\n"
            "  text-indent: 0;\n  white-space: nowrap;\n  word-wrap: normal;\n  overflow-wrap: normal;\n"
            "  direction: ltr;\n  vertical-align: -0.125em;\n"
            '  font-feature-settings: "liga" 1, "rlig" 1;\n  font-variant-ligatures: common-ligatures;\n'
            "  -webkit-font-smoothing: antialiased;\n  -moz-osx-font-smoothing: grayscale;\n"
            "  text-rendering: optimizeLegibility;\n  speak: never;\n}\n"
            ".typeicon::before { speak: never; }\n"
            ".typeicon-fw { width: 1.25em; text-align: center; }\n"
            ".typeicon-xs { font-size: .75em; } .typeicon-sm { font-size: .875em; } .typeicon-lg { font-size: 1.25em; }\n"
            ".typeicon-2x { font-size: 2em; } .typeicon-3x { font-size: 3em; } .typeicon-4x { font-size: 4em; } .typeicon-5x { font-size: 5em; }\n"
            ".typeicon-rotate-90 { transform: rotate(90deg); } .typeicon-rotate-180 { transform: rotate(180deg); }\n"
            ".typeicon-rotate-270 { transform: rotate(270deg); } .typeicon-flip-horizontal { transform: scaleX(-1); }\n"
            ".typeicon-flip-vertical { transform: scaleY(-1); } .typeicon-flip-both { transform: scale(-1, -1); }\n"
            ".typeicon-spin { animation: typeicon-spin 2s linear infinite; }\n"
            "@keyframes typeicon-spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }\n"
            "@media (prefers-reduced-motion: reduce) { .typeicon-spin { animation: none; } }\n"
            ".typeicon-sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden;"
            " clip: rect(0, 0, 0, 0); white-space: nowrap; border: 0; }"
        )
    for fam in families:
        out.append(f'.{fam.css_class} {{ font-family: "{fam.family}"; }}')
    seen = set()
    for fam in families:
        for d in designs_by_family[fam.slug]:
            if d["name"] in seen:
                continue
            seen.add(d["name"])
            out.append(f'.typeicon-{d["name"]}::before {{ content: "\\{d["codepoint"]:X}"; }}')
    return "\n".join(out) + "\n"


def _standalone_svg(svg: str, view_box) -> str:
    w, h = view_box[2], view_box[3]
    width = round(24 * w / h, 3)
    width_s = f"{width:g}"
    return svg.replace("<svg ", f'<svg width="{width_s}" height="24" ', 1) + "\n"


def _symbol(svg: str, symbol_id: str) -> str:
    import re
    m = re.match(r"^<svg([^>]*)>(.*)</svg>$", svg, re.S)
    if not m:
        raise ReleaseError(f"cannot build symbol for {symbol_id}")
    attrs = dict(re.findall(r'([\w:-]+)="([^"]*)"', m.group(1)))
    vb = attrs.pop("viewBox")
    attrs.pop("xmlns", None)
    g_attrs = " ".join(f'{k}="{html.escape(v)}"' for k, v in sorted(attrs.items()))
    return f'<symbol id="{symbol_id}" viewBox="{vb}"><g {g_attrs}>{m.group(2)}</g></symbol>'


def build_release(version: str, release_date: str, root: Path | None = None, workers: int | None = None,
                  raster_sample: int = 40, only_sources: list[str] | None = None, log=print) -> dict:
    root = root or repo_root()
    epoch = int(datetime.fromisoformat(release_date).replace(tzinfo=timezone.utc).timestamp())
    sources = {s.slug: s.raw for s in load_manifest(root)}
    designs = [d for d in load_designs(root) if not only_sources or d["source"] in only_sources]
    for d in designs:
        if d["area"] == "core" and d["name"] in RESERVED_CLASS_NAMES:
            raise ReleaseError(f"Core icon name {d['name']!r} is reserved for CSS utilities")
    families, unsupported = plan_families(designs)

    rel_root = root / "dist" / "releases" / version
    out = rel_root / "typeicon-release"
    if out.exists():
        shutil.rmtree(out)
    for sub in ("desktop", "webfonts", "css", "svg", "sprites", "metadata/glyph-maps", "licenses", "examples"):
        (out / sub).mkdir(parents=True, exist_ok=True)

    # ---- fonts (parallel), validation
    log(f"compiling {len(families)} families ...")
    jobs = []
    for fam in families:
        fam_dict = {k: getattr(fam, k) for k in ("slug", "family", "ps_name", "source", "area", "style", "css_class", "part")}
        jobs.append((fam_dict, fam.entries, version, epoch, sources, str(rel_root)))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        compiled = {r["slug"]: r for r in pool.map(_compile_family, jobs)}
    failures = []
    for fam in families:
        res = compiled[fam.slug]
        for fmt, v in res["validation"].items():
            if not v["ok"]:
                failures.append(f"{fam.family} {fmt}: {v['errors'][:3]}")
    if failures:
        raise ReleaseError("font validation failed:\n" + "\n".join(failures))
    for fam in families:
        files = compiled[fam.slug]["files"]
        for fmt, p in files.items():
            dest = out / ("desktop" if fmt in ("otf", "ttf") else "webfonts") / Path(p).name
            shutil.copyfile(p, dest)
    shutil.rmtree(rel_root / "_fonts", ignore_errors=True)

    log("raster comparisons ...")
    raster = {}
    for fam in families:
        sample = None if fam.area == "core" else raster_sample
        raster[fam.slug] = _raster_check(fam, out / "desktop" / f"{fam.file_base}.otf", sample)
        min_ok = 0.95 if fam.area == "core" else 0.85
        if raster[fam.slug]["minIoU"] is not None and raster[fam.slug]["minIoU"] < min_ok:
            raise ReleaseError(f"{fam.family}: raster mismatch {raster[fam.slug]}")

    # ---- CSS
    designs_by_family = {fam.slug: [d for d, _ in fam.entries] for fam in families}
    core_fams = [f for f in families if f.area == "core"]
    if core_fams:
        (out / "css" / "typeicon.css").write_text(_css_for(core_fams, designs_by_family, "../webfonts", True))
    for slug in sorted({f.source for f in families if f.area != "core"}):
        fams = [f for f in families if f.source == slug]
        (out / "css" / f"typeicon-{slug}.css").write_text(_css_for(fams, designs_by_family, "../webfonts", False))

    # ---- SVGs and sprites
    log("writing SVGs and sprites ...")
    sprites: dict[tuple[str, str], list[str]] = {}
    for d in designs:
        for v in d["variants"]:
            if v["status"] != "published" or not v.get("svg"):
                continue
            p = out / "svg" / d["source"] / v["style"] / f"{d['name']}.svg"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(_standalone_svg(v["svg"], v["viewBox"]))
            sprites.setdefault((d["source"], v["style"]), []).append(_symbol(v["svg"], f"typeicon-{v['style']}-{d['name']}"))
    for (source, style), symbols in sorted(sprites.items()):
        (out / "sprites" / f"{source}-{style}.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">\n' + "\n".join(symbols) + "\n</svg>\n")

    # ---- metadata
    fam_of: dict[tuple[str, str], Family] = {}
    for fam in families:
        for d, v in fam.entries:
            fam_of[(d["id"], v["style"])] = fam
    icons = []
    for d in sorted(designs, key=lambda d: (d["area"] != "core", d["name"])):
        styles = {}
        for v in d["variants"]:
            if v["status"] != "published":
                continue
            fam = fam_of.get((d["id"], v["style"]))
            styles[v["style"]] = {
                "variantId": v["id"], "nativeStyle": v["nativeStyle"], "nativeLabel": v["nativeLabel"],
                "svg": f"svg/{d['source']}/{v['style']}/{d['name']}.svg",
                "sprite": f"sprites/{d['source']}-{v['style']}.svg#typeicon-{v['style']}-{d['name']}",
                "fontFamily": fam.family if fam else None, "fontSupported": fam is not None,
                "svgSha256": v["svgSha256"], "sourceSha256": v["sourceSha256"],
            }
        if not styles:
            continue
        icons.append({
            "name": d["name"], "id": d["id"], "source": d["source"], "area": d["area"], "concept": d["concept"],
            "keywords": keywords_for(d), "aliases": d["aliases"], "tags": d["tags"], "categories": d["categories"],
            "searchTerms": d.get("keywords") or [], "context": d.get("context"),
            "isBrand": d["isBrand"], "codepoint": d.get("codepoint"),
            "codepointHex": f"U+{d['codepoint']:X}" if d.get("codepoint") else None,
            "bmpCodepoint": d.get("bmpCodepoint"), "license": d.get("license") or sources[d["source"]]["license"]["spdx"],
            "attributes": d.get("extra") or {},
            "derivedFrom": d.get("derivedFrom"), "styles": styles,
        })
    (out / "metadata" / "icons.json").write_text(json.dumps(icons, indent=1, ensure_ascii=False) + "\n")
    fam_meta = []
    for fam in families:
        res = compiled[fam.slug]
        glyph_map = {
            "family": fam.family, "postscriptName": fam.ps_name, "style": fam.style, "source": fam.source,
            "files": {fmt: Path(p).name for fmt, p in res["files"].items()},
            "glyphs": [{"name": d["name"], "keywords": keywords_for(d), "codepoints": codepoints_for(d),
                        "codepointsHex": [f"U+{c:X}" for c in codepoints_for(d)]} for d, _ in fam.entries],
        }
        (out / "metadata" / "glyph-maps" / f"{fam.slug}.json").write_text(json.dumps(glyph_map, indent=1) + "\n")
        fam_meta.append({
            "slug": fam.slug, "family": fam.family, "postscriptName": fam.ps_name, "source": fam.source,
            "area": fam.area, "style": fam.style, "cssClass": fam.css_class, "part": fam.part,
            "glyphs": res["glyphs"], "keywords": res["keywords"],
            "files": {fmt: {"name": Path(p).name, "bytes": (out / ("desktop" if fmt in ("otf", "ttf") else "webfonts") / Path(p).name).stat().st_size,
                            "sha256": _sha256(out / ("desktop" if fmt in ("otf", "ttf") else "webfonts") / Path(p).name)}
                      for fmt, p in res["files"].items()},
            "validation": {fmt: {"ok": v["ok"], "stats": v["stats"]} for fmt, v in res["validation"].items()},
            "raster": raster[fam.slug],
        })
    (out / "metadata" / "families.json").write_text(json.dumps(fam_meta, indent=1) + "\n")
    core_names = sorted(i["name"] for i in icons if i["area"] == "core")
    (out / "metadata" / "typeicon.d.ts").write_text(
        "// Generated by typeicon-import release.\n"
        "export type TypeIconStyle = 'filled' | 'line' | 'rounded' | 'thin';\n"
        "export type TypeIconCoreIconName =\n" + "\n".join(f"  | '{n}'" for n in core_names) + ";\n"
        "export interface TypeIconIconStyle { variantId: string; nativeStyle: string; nativeLabel: string; svg: string;"
        " sprite: string; fontFamily: string | null; fontSupported: boolean; svgSha256: string; sourceSha256: string }\n"
        "export interface TypeIconIcon { name: string; id: string; source: string; area: 'core' | 'community';"
        " concept: string; keywords: string[]; aliases: string[]; tags: string[]; categories: string[]; searchTerms: string[]; context: string | null; isBrand: boolean;"
        " codepoint: number | null; codepointHex: string | null; bmpCodepoint: number | null; license: string;"
        " derivedFrom: { name: string; transform: string } | null; styles: Partial<Record<string, TypeIconIconStyle>> }\n"
    )

    # ---- licenses
    used_sources = sorted({d["source"] for d in designs})
    attribution = ["# Attribution and licenses", "",
                   "TypeIcon releases combine separately licensed icon collections. Each collection keeps its",
                   "own license. TypeIcon does not relicense third-party artwork.", ""]
    notice = [f"TypeIcon {version}", ""]
    for slug in used_sources:
        s = sources[slug]
        lic_src = root / s["license"]["file"]
        dest = out / "licenses" / slug / Path(s["license"]["file"]).name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(lic_src, dest)
        attribution += [f"## {s['displayName']} ({s['area']})", "",
                        f"- License: {s['license']['spdx']} (`licenses/{slug}/{dest.name}`)",
                        f"- Copyright: {s['copyright']}", f"- Upstream: {s['upstreamUrl']}",
                        f"- Version: {s['version']}" + (f" (npm {s['package']}, integrity {s['integrity']})" if s.get("package") else ""),
                        f"- Attribution: {s['attribution']['text']}"]
        for n in s.get("notices", []):
            attribution.append(f"- Notice: {n}")
        if s.get("trademarkNote"):
            attribution.append(f"- Trademark: {s['trademarkNote']}")
        attribution += [f"- Modifications: {'; '.join(s.get('modificationHistory') or ['none'])}", ""]
        notice.append(f"This release contains {s['displayName']} under {s['license']['spdx']}. {s['copyright']}.")
    attribution += ["## TypeIcon fallback letterforms", "",
                    "The readable ASCII fallback glyphs in every font are original TypeIcon designs and are covered",
                    "by the TypeIcon Core license (see licenses/typeicon-core/).", ""]
    if "typeicon-core" not in used_sources:
        dest = out / "licenses" / "typeicon-core" / "LICENSE.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / sources["typeicon-core"]["license"]["file"], dest)
    # Logos/icons whose own license differs from their source's (e.g. MIT or CC-BY brand logos).
    for slug in used_sources:
        own = [d for d in designs if d["source"] == slug and d.get("license") and d["license"] != sources[slug]["license"]["spdx"]
               and any(v["status"] == "published" for v in d["variants"])]
        if own:
            rows = ["# Per-icon licenses", "", f"These {sources[slug]['displayName']} items carry their own license. Keep this file with the artwork.", "",
                    "| Icon | License | License URL | Source |", "|---|---|---|---|"]
            rows += [f"| {d['name']} | {d['license']} | {(d.get('extra') or {}).get('licenseUrl') or 'https://spdx.org/licenses/' + d['license'] + '.html'} | {(d.get('extra') or {}).get('sourceUrl') or ''} |" for d in sorted(own, key=lambda d: d["name"])]
            (out / "licenses" / slug / "PER-ICON-LICENSES.md").write_text("\n".join(rows) + "\n")
            attribution.append(f"- {slug}: {len(own)} items have individual licenses. See `licenses/{slug}/PER-ICON-LICENSES.md`.")
    (out / "licenses" / "ATTRIBUTION.md").write_text("\n".join(attribution))
    (out / "licenses" / "NOTICE").write_text("\n".join(notice) + "\n")

    # ---- examples + README
    _write_examples(out, families, icons)
    _write_readme(out, version, families, sources, used_sources, len(icons))

    # ---- manifest + checksums
    manifest = {
        "name": "typeicon-release", "version": version, "releaseDate": release_date,
        "toolchain": TOOLCHAIN_VERSION,
        "sources": {slug: {"version": sources[slug]["version"], "license": sources[slug]["license"]["spdx"]}
                    for slug in used_sources},
        "counts": {
            "icons": len(icons),
            "coreIcons": sum(i["area"] == "core" for i in icons),
            "brandIcons": sum(i["area"] == "brands" for i in icons),
            "variants": sum(len(i["styles"]) for i in icons),
            "fontGlyphs": sum(compiled[f.slug]["glyphs"] for f in families),
            "svgOnlyVariants": len(unsupported),
        },
        "families": [f.family for f in families],
        "unsupportedInFonts": unsupported,
    }
    (out / "metadata" / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    files = sorted(p for p in out.rglob("*") if p.is_file() and p.name != "checksums.sha256")
    (out / "checksums.sha256").write_text("".join(f"{_sha256(p)}  {p.relative_to(out).as_posix()}\n" for p in files))

    # ---- archives
    log("writing archives ...")
    arch = rel_root / "archives"
    if arch.exists():
        shutil.rmtree(arch)
    everything = [p for p in out.rglob("*") if p.is_file()]
    common = [p for p in everything if p.relative_to(out).parts[0] in ("licenses",) or p.name in ("README.md",)]
    prefix = f"typeicon-{version}"
    archives = [{"kind": "complete", "label": "Complete release", **_write_zip(arch / f"{prefix}-complete.zip", out, everything, prefix)}]

    def sel(*tops, pred=lambda p: True):
        return [p for p in everything if p.relative_to(out).parts[0] in tops and pred(p)]

    archives.append({"kind": "desktop", "label": "Desktop fonts (all families, OTF + TTF)",
                     **_write_zip(arch / f"{prefix}-desktop.zip", out, sel("desktop") + common, prefix)})
    archives.append({"kind": "web", "label": "Web fonts + CSS + examples",
                     **_write_zip(arch / f"{prefix}-web.zip", out, sel("webfonts", "css", "examples") + common, prefix)})
    archives.append({"kind": "svg", "label": "SVG files + sprites",
                     **_write_zip(arch / f"{prefix}-svg.zip", out, sel("svg", "sprites") + common, prefix)})
    archives.append({"kind": "metadata", "label": "Metadata (names, aliases, glyph maps)",
                     **_write_zip(arch / f"{prefix}-metadata.zip", out, sel("metadata") + common, prefix)})
    for fam in families:
        members = [out / "desktop" / f"{fam.file_base}.otf", out / "desktop" / f"{fam.file_base}.ttf",
                   out / "metadata" / "glyph-maps" / f"{fam.slug}.json"] + common
        archives.append({"kind": "family-desktop", "family": fam.family, "slug": fam.slug, "source": fam.source,
                         "style": fam.style, "label": f"{fam.family} (desktop OTF + TTF)",
                         **_write_zip(arch / f"{prefix}-{fam.slug}-desktop.zip", out, members, prefix)})
    for slug in used_sources:
        members = [p for p in sel("svg") if p.relative_to(out).parts[1] == slug] + \
                  [p for p in sel("sprites") if p.name.startswith(slug + "-")] + common
        archives.append({"kind": "source-svg", "source": slug, "label": f"{sources[slug]['displayName']} SVGs",
                         **_write_zip(arch / f"{prefix}-{slug}-svg.zip", out, members, prefix)})
    index = {"version": version, "releaseDate": release_date, "archives": archives,
             "families": fam_meta, "counts": manifest["counts"]}
    (arch / "index.json").write_text(json.dumps(index, indent=1) + "\n")
    log(f"release {version}: {len(families)} families, {len(icons)} icons, {len(archives)} archives")
    return index


def _write_examples(out: Path, families: list[Family], icons: list[dict]) -> None:
    core = [f for f in families if f.area == "core"]
    demo = [n for n in ("home", "search", "settings", "user", "arrow-right") if any(i["name"] == n for i in icons)]
    by_name = {i["name"]: i for i in icons}
    rows = "\n".join(
        f'      <tr><th scope="row">{f.family}</th>' + "".join(
            f'<td><span class="typeicon {f.css_class}" aria-hidden="true">{n}</span></td>' for n in demo) + "</tr>"
        for f in core)
    (out / "examples" / "ligatures.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>TypeIcon ligature example</title>
<link rel="stylesheet" href="../css/typeicon.css">
<style>body{{font:16px/1.5 system-ui,sans-serif;margin:2rem}} td,th{{padding:.5rem 1rem;text-align:left}} .typeicon{{font-size:32px}}</style>
</head><body>
<h1>Ligatures</h1>
<p>Each cell contains the plain text keyword. The font's OpenType <code>liga</code> feature replaces it with the icon.
Icons are decorative here, so they carry <code>aria-hidden="true"</code> and the keyword is not announced.</p>
<table><thead><tr><th scope="col">Family</th>{''.join(f'<th scope="col"><code>{n}</code></th>' for n in demo)}</tr></thead>
<tbody>
{rows}
</tbody></table>
<h2>Meaningful icon with a label</h2>
<p><button type="button"><span class="typeicon typeicon-line" aria-hidden="true">search</span><span class="typeicon-sr-only">Search</span></button></p>
</body></html>
""")
    cls_rows = "\n".join(
        f'  <li><span class="typeicon typeicon-line typeicon-{n}" aria-hidden="true"></span> <code>typeicon typeicon-line typeicon-{n}</code> '
        f'({by_name[n]["codepointHex"]})</li>' for n in demo)
    (out / "examples" / "css-classes.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>TypeIcon CSS class example</title>
<link rel="stylesheet" href="../css/typeicon.css">
<style>body{{font:16px/1.5 system-ui,sans-serif;margin:2rem}} .typeicon{{font-size:28px}}</style>
</head><body>
<h1>Named classes (codepoint mapping)</h1>
<p>These use <code>::before</code> with the icon's permanent private-use codepoint, so they work even where ligatures are disabled.</p>
<ul>
{cls_rows}
</ul>
</body></html>
""")
    uses = "\n".join(
        f'  <svg width="32" height="32" role="img" aria-label="{n}"><use href="../sprites/typeicon-core-line.svg#typeicon-line-{n}"/></svg>'
        for n in demo)
    (out / "examples" / "svg-sprite.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>TypeIcon SVG sprite example</title>
<style>body{{font:16px/1.5 system-ui,sans-serif;margin:2rem;color:#1d4ed8}}</style>
</head><body>
<h1>SVG sprite</h1>
<p>Serve this page over HTTP (for example <code>npx serve ..</code>); browsers block external <code>&lt;use&gt;</code> references from <code>file://</code>.</p>
{uses}
</body></html>
""")
    (out / "examples" / "react").mkdir(exist_ok=True)
    (out / "examples" / "react" / "App.tsx").write_text(
        "// npm install @typeicon/react  (local workspace package until an npm scope is registered)\n"
        "import Home from '@typeicon/react/line/home';\n"
        "import Search from '@typeicon/react/rounded/search';\n\n"
        "export default function App() {\n"
        "  return (\n    <nav>\n      <a href=\"/\"><Home size={20} aria-hidden /> Home</a>\n"
        "      <button type=\"button\" aria-label=\"Search\"><Search size={20} /></button>\n    </nav>\n  );\n}\n")
    (out / "examples" / "vue").mkdir(exist_ok=True)
    (out / "examples" / "vue" / "App.vue").write_text(
        "<!-- npm install @typeicon/vue  (local workspace package until an npm scope is registered) -->\n"
        "<script setup lang=\"ts\">\nimport Home from '@typeicon/vue/line/home';\n"
        "import Search from '@typeicon/vue/rounded/search';\n</script>\n\n"
        "<template>\n  <nav>\n    <a href=\"/\"><Home :size=\"20\" aria-hidden=\"true\" /> Home</a>\n"
        "    <button type=\"button\" aria-label=\"Search\"><Search :size=\"20\" /></button>\n  </nav>\n</template>\n")


def _write_readme(out: Path, version: str, families: list[Family], sources: dict, used: list[str], n_icons: int) -> None:
    lines = [f"# TypeIcon {version}", "",
             f"This archive contains {n_icons} icons across {len(families)} font families, plus SVGs, sprites,",
             "web fonts, CSS and metadata. Counts come from `metadata/manifest.json`.", "",
             "## Desktop fonts (keyword ligatures)", "",
             "1. Install the `.otf` files from `desktop/` (macOS: double-click → Install; Windows: right-click → Install for all users).",
             "2. Restart the application you design in (Figma desktop, Sketch, Illustrator, Word …).",
             "3. Choose the exact family below, make sure ligatures are enabled, and type a keyword such as `home`.",
             "4. Switch the family to change style; the keyword stays the same.", "",
             "Keywords are case-sensitive lowercase names. Unknown words stay as readable letters.",
             "A ligature font substitutes a known name wherever it occurs, including inside longer words;",
             "put icon keywords in their own text layer or text run.", "",
             "| Family | Style | Source | Glyphs | Files |", "|---|---|---|---:|---|"]
    for f in families:
        lines.append(f"| {f.family} | {f.style} | {sources[f.source]['displayName']} | {len(f.entries)} | `desktop/{f.file_base}.otf`, `.ttf` |")
    lines += ["", "## Web", "",
              "```html", '<link rel="stylesheet" href="css/typeicon.css">',
              '<span class="typeicon typeicon-line" aria-hidden="true">home</span>        <!-- ligature -->',
              '<span class="typeicon typeicon-line typeicon-home" aria-hidden="true"></span>    <!-- codepoint class -->', "```", "",
              "For new web interfaces, prefer inline SVG or the React/Vue components; use the web font where",
              "you need text-like icons.", "",
              "## Licenses", ""]
    for slug in used:
        s = sources[slug]
        lines.append(f"- {s['displayName']}: {s['license']['spdx']} (`licenses/{slug}/`)")
    lines += ["", "See `licenses/ATTRIBUTION.md` for required attribution and modification notes.",
              "Verify file integrity with `shasum -a 256 -c checksums.sha256`.", ""]
    (out / "README.md").write_text("\n".join(lines))
