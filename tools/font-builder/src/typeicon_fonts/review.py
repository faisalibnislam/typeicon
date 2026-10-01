"""Design review sheets: canonical SVG (resvg) next to the compiled font glyph (FreeType).

For each icon and style: two rows (light and dark background), each showing the SVG render and
the font render at 16, 20, 24, 32 and 48 px. Reviewers check optical consistency, small-size
legibility and that the font reproduces the SVG.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

from .raster import render_glyph_mask, render_svg_mask

SIZES = [16, 20, 24, 32, 48]
BG = {"light": ((255, 255, 255), (22, 22, 26)), "dark": ((17, 17, 19), (237, 237, 240))}


def _tint(mask: Image.Image, bg, fg) -> Image.Image:
    return Image.composite(Image.new("RGB", mask.size, fg), Image.new("RGB", mask.size, bg), mask)


def review_sheet(items: list[dict], out: Path, title: str) -> Path:
    """items: [{name, style, svg, font, codepoint}]"""
    cell_w = sum(s + 10 for s in SIZES) + 20
    row_h = 58
    width = 180 + 2 * cell_w
    height = 40 + len(items) * 2 * row_h
    img = Image.new("RGB", (width, height), (247, 247, 245))
    d = ImageDraw.Draw(img)
    d.text((10, 10), title + "   (left: SVG via resvg · right: font glyph via FreeType)", fill=(60, 60, 60))
    y = 40
    for it in items:
        for mode in ("light", "dark"):
            bg, fg = BG[mode]
            d.rectangle([180, y, width - 10, y + row_h - 6], fill=bg)
            d.text((10, y + 18), f"{it['name']} · {it['style']} · {mode}", fill=(80, 80, 80))
            for col, kind in enumerate(("svg", "font")):
                x = 190 + col * cell_w
                for s in SIZES:
                    m = render_svg_mask(it["svg"], s) if kind == "svg" else render_glyph_mask(it["font"], it["codepoint"], s)
                    tile = _tint(m, bg, fg)
                    img.paste(tile, (x, y + (row_h - 6 - s) // 2))
                    x += s + 10
            y += row_h
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out
