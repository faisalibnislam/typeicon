"""Quality gate + review sheets for Core icon modules.

Usage:
  .venv/bin/python tools/core-authoring/check.py sets/clothing.py [--sheet out.png] [--variants]

Checks every icon defined in the module:
  * names: lowercase kebab-case, unique across the whole library (incl. aliases)
  * all three styles render; sanitizer routes them to fonts; outlines convert
  * artwork stays inside the 24 x 24 canvas (0.3 px tolerance) and is not tiny
  * styles are genuinely different (pairwise raster IoU < 0.995 at 48 px)
  * not a near-copy of another icon in the library (Line IoU >= 0.97 warns)
Writes a review sheet: each icon in Line / Rounded / Filled at 48 px plus 24 and 16 px, light background.
Exit status 1 if any icon fails.
"""
from __future__ import annotations

import argparse
import importlib.util
import io
import json
import re
import sys
from pathlib import Path as FsPath

HERE = FsPath(__file__).resolve().parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parents[1]

# Mirrors typeicon_import.release.RESERVED_CLASS_NAMES (utility classes in the web font CSS).
RESERVED_CLASS_NAMES = {
    "filled", "line", "rounded", "thin", "spin", "pulse", "fw", "xs", "sm", "lg", "xl", "2x", "3x", "4x", "5x",
    "rotate-90", "rotate-180", "rotate-270", "flip-horizontal", "flip-vertical", "flip-both",
    "sr-only", "inverse", "stack", "border",
}
NAME_RE = re.compile(r"^(?=.{2,64}$)[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_module(path: FsPath):
    import dsl
    before = len(dsl.REGISTRY)
    spec = importlib.util.spec_from_file_location(f"sets.{path.stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return dsl.REGISTRY[before:]


def svg_for(ic, style):
    from export import filled_svg, stroke_svg
    from geometry import LINE, ROUNDED, path_to_d
    if style == "filled":
        return filled_svg(path_to_d(ic.filled()))
    S = LINE if style == "line" else ROUNDED
    return stroke_svg(ic.stroke(S), S, None)


def _other_designs(path: FsPath) -> list[tuple[str, list[str]]]:
    """(name, aliases) of every other Core design: v0.1 icons.py and all other sets modules (drawn in parallel)."""
    import subprocess
    code = (
        "import sys,json,importlib,pathlib; sys.path.insert(0,'.'); import dsl; from icons import ICONS\n"
        "for f in sorted(pathlib.Path('sets').glob('*.py')):\n"
        f"    if not f.name.startswith('_') and f.resolve() != pathlib.Path({str(path.resolve())!r}):\n"
        "        try: importlib.import_module('sets.'+f.stem)\n"
        "        except Exception as e: print('skip', f.name, e, file=sys.stderr)\n"
        "print(json.dumps([[i.name, i.aliases] for i in list(ICONS) + dsl.REGISTRY]))"
    )
    out = subprocess.run([sys.executable, "-c", code], cwd=HERE, capture_output=True, text=True, check=True)
    return [tuple(x) for x in json.loads(out.stdout)]


def _outline_iou(svg: str, path) -> float:
    """Render the converted font outline (font units, y up) and compare it with the SVG at 96 px."""
    from fontTools.pens.svgPathPen import SVGPathPen
    from typeicon_fonts.outline import ASCENT, UPM
    from typeicon_fonts.raster import mask_iou, render_svg_mask
    pen = SVGPathPen(None)
    path.draw(pen)
    glyph = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {UPM} {UPM}"><path fill="#000" '
             f'transform="matrix(1 0 0 -1 0 {ASCENT})" d="{pen.getCommands()}"/></svg>')
    return mask_iou(render_svg_mask(svg, 96), render_svg_mask(glyph, 96))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("module")
    ap.add_argument("--sheet")
    ap.add_argument("--variants", action="store_true", help="also render a sample of generated variants")
    args = ap.parse_args()
    from typeicon_fonts.outline import svg_to_outline
    from typeicon_fonts.raster import mask_iou, render_svg_mask
    from typeicon_fonts.svg_sanitize import sanitize_svg

    path = (HERE / args.module) if not FsPath(args.module).is_absolute() else FsPath(args.module)
    icons = load_module(path)
    others = _other_designs(path)  # excludes this module, so its own names never count as taken
    other_names = {n for n, _ in others}
    other_aliases = {a for _, al in others for a in al}
    plan = json.loads((HERE / "plan.json").read_text())
    planned = {n for c in plan["categories"].values() for n in c["concepts"]}
    for bf in (HERE / "plan20k" / "batches").glob("*.json"):  # the 20k programme's drawing batches
        planned |= {c["name"] for c in json.loads(bf.read_text())}

    problems: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
    rendered = {}
    for ic in icons:
        for n in [ic.name, *ic.aliases]:
            if not NAME_RE.match(n):
                problems.append(f"{ic.name}: invalid name/alias {n!r}")
            if n in seen or n in other_names or n in other_aliases:
                problems.append(f"{ic.name}: name/alias {n!r} already used")
            seen.add(n)
        if ic.name.startswith("brand-"):
            problems.append(f"{ic.name}: the brand- prefix is reserved for brand logos; rename the icon")
        if ic.name in RESERVED_CLASS_NAMES:
            problems.append(f"{ic.name}: name is reserved for a CSS utility class (typeicon-{ic.name}); rename it (an alias may keep the old name)")
        if ic.name not in planned:
            warnings.append(f"{ic.name}: not in plan.json (fine if intentional; add it to make_plan.py)")
        if not ic.description or not ic.tags:
            problems.append(f"{ic.name}: needs a description and tags")
        masks = {}
        for st in ("line", "rounded", "filled"):
            try:
                svg = svg_for(ic, st)
                san = sanitize_svg(svg)
                if san.route != "font":
                    problems.append(f"{ic.name}/{st}: routed to svg-only: {san.reasons}")
                o = svg_to_outline(san.svg)
                x0, y0, x1, y1 = o.path.bounds
                tol = 0.3 * 50
                if x0 < -tol or y0 < -150 - tol or x1 > 1200 + tol or y1 > 1050 + tol:
                    problems.append(f"{ic.name}/{st}: artwork leaves the 24 x 24 canvas")
                if (x1 - x0) < 6 * 50 and (y1 - y0) < 6 * 50:
                    problems.append(f"{ic.name}/{st}: artwork is tiny (< 6 px)")
                masks[st] = render_svg_mask(svg, 48)
                rt = _outline_iou(svg, o.path)
                if rt < 0.95:  # what the font will contain must look like the SVG (catches Skia stroke/union faults)
                    problems.append(f"{ic.name}/{st}: font outline differs from the SVG (IoU {rt:.3f}); simplify the geometry")
                rendered[(ic.name, st)] = svg
            except Exception as e:  # noqa: BLE001
                problems.append(f"{ic.name}/{st}: {type(e).__name__}: {e}")
        if len(masks) == 3:
            for a, b in (("line", "rounded"), ("line", "filled"), ("rounded", "filled")):
                iou = mask_iou(masks[a], masks[b])
                if iou >= 0.995:
                    problems.append(f"{ic.name}: {a} and {b} are visually identical (IoU {iou:.4f}); make the styles differ")
    # near-duplicates within the module
    names = [i.name for i in icons]
    line_masks = {n: render_svg_mask(rendered[(n, "line")], 32) for n in names if (n, "line") in rendered}
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if a in line_masks and b in line_masks and mask_iou(line_masks[a], line_masks[b]) >= 0.97:
                warnings.append(f"{a} and {b} look almost identical in Line")

    from transforms import detect
    for name, df in detect(icons).items():
        warnings.append(f"{name} is a {df['transform']} of {df['name']}: published, but not counted as a separate concept")
    if args.sheet:
        _sheet(icons, rendered, FsPath(args.sheet), args.variants)
    for w in warnings:
        print("WARN ", w)
    for p in problems:
        print("FAIL ", p)
    print(f"{len(icons)} icons checked: {len(problems)} problems, {len(warnings)} warnings")
    return 1 if problems else 0


def _sheet(icons, rendered, out: FsPath, variants: bool):
    import resvg_py
    from PIL import Image, ImageDraw

    def img(svg, px):
        png = bytes(resvg_py.svg_to_bytes(svg_string=svg.replace("currentColor", "#111"), width=px, height=px))
        return Image.open(io.BytesIO(png)).convert("RGBA")

    rows = []
    for ic in icons:
        rows.append((ic.name, [rendered.get((ic.name, s)) for s in ("line", "rounded", "filled")]))
    if variants:
        from modifiers import MODIFIERS, compose
        for ic in icons[:3]:
            for suf in ("plus", "off", "lock"):
                v = compose(ic, MODIFIERS[suf], f"{ic.name}-{suf}", ic.category, "", [])
                rows.append((v.name, [svg_for(v, s) for s in ("line", "rounded", "filled")]))
    cols = 4
    cw, ch = 3 * 56 + 2 * 28 + 24, 76
    sheet = Image.new("RGB", (cols * cw, ((len(rows) + cols - 1) // cols) * ch), "white")
    d = ImageDraw.Draw(sheet)
    for k, (name, svgs) in enumerate(rows):
        x0, y0 = (k % cols) * cw + 6, (k // cols) * ch + 4
        for j, svg in enumerate(svgs):
            if svg:
                sheet.alpha_composite(img(svg, 48), (x0 + j * 56, y0)) if sheet.mode == "RGBA" else sheet.paste(img(svg, 48), (x0 + j * 56, y0), img(svg, 48))
        if svgs[0]:
            sheet.paste(img(svgs[0], 24), (x0 + 3 * 56, y0 + 12), img(svgs[0], 24))
            sheet.paste(img(svgs[0], 16), (x0 + 3 * 56 + 30, y0 + 16), img(svgs[0], 16))
        d.text((x0, y0 + 52), name[:34], fill="#444")
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    print(f"sheet: {out}")


if __name__ == "__main__":
    sys.exit(main())
