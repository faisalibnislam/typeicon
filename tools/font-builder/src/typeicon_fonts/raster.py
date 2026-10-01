"""Raster comparison of canonical SVGs (resvg) against compiled font glyphs (FreeType).

Two independent renderers are used on purpose: resvg paints the original stroke-based SVG,
FreeType rasterises the compiled OTF/TTF outline. Agreement (IoU of coverage masks) proves
stroke expansion, transform flattening, y-inversion, overlap removal and hole handling.
"""
from __future__ import annotations

import io
from dataclasses import dataclass

import freetype
import resvg_py
from PIL import Image, ImageChops

from .outline import ASCENT, UPM


@dataclass
class Comparison:
    iou: float
    svg_px: int
    font_px: int
    diff_px: int


def render_svg_mask(svg: str, px: int) -> Image.Image:
    """Coverage mask (L mode) of an SVG rendered to px em height."""
    from .svg_sanitize import parse_view_box, safe_parse
    root = safe_parse(svg.encode())
    _, _, vw, vh = parse_view_box(root)
    w = max(1, round(px * vw / vh))
    png = bytes(resvg_py.svg_to_bytes(svg_string=svg.replace("currentColor", "#000"), width=w, height=px))
    img = Image.open(io.BytesIO(png)).convert("RGBA")
    return img.getchannel("A")


def render_glyph_mask(font_path: str, codepoint: int, px: int, width_px: int | None = None) -> Image.Image:
    face = freetype.Face(str(font_path))
    face.set_pixel_sizes(0, px)
    face.load_char(chr(codepoint), freetype.FT_LOAD_RENDER | freetype.FT_LOAD_NO_HINTING | freetype.FT_LOAD_TARGET_NORMAL)
    g = face.glyph
    bm = g.bitmap
    width_px = width_px or px
    canvas = Image.new("L", (width_px, px), 0)
    if bm.width and bm.rows:
        glyph_img = Image.frombytes("L", (bm.width, bm.rows), bytes(bm.buffer)) if bm.pitch == bm.width else \
            Image.frombytes("L", (bm.width, bm.rows), b"".join(bytes(bm.buffer[r * bm.pitch:r * bm.pitch + bm.width]) for r in range(bm.rows)))
        baseline = px * ASCENT / UPM
        canvas.paste(glyph_img, (g.bitmap_left, round(baseline - g.bitmap_top)))
    return canvas


def compare(svg: str, font_path: str, codepoint: int, px: int = 96, threshold: int = 128) -> Comparison:
    a = render_svg_mask(svg, px)
    b = render_glyph_mask(font_path, codepoint, px, a.width)
    ma = a.point(lambda v: 255 if v >= threshold else 0)
    mb = b.point(lambda v: 255 if v >= threshold else 0)
    inter = ImageChops.multiply(ma, mb).histogram()[255]
    union = ImageChops.lighter(ma, mb).histogram()[255]
    diff = ImageChops.difference(ma, mb).histogram()[255]
    return Comparison(iou=(inter / union) if union else 1.0, svg_px=ma.histogram()[255],
                      font_px=mb.histogram()[255], diff_px=diff)


def compare_aligned(svg: str, font_path: str, codepoint: int, px: int = 384, max_shift: int = 1) -> float:
    """Best IoU when the font mask may be off by up to max_shift pixels. Font coordinates are whole units, so a
    shape placed on half units moves by up to 0.5 unit (1 px at 384 px is 1/16 of a grid pixel): invisible,
    but enough to cost a tiny dot several percent of IoU. Real outline errors are not rescued by this."""
    a = render_svg_mask(svg, px).point(lambda v: 255 if v >= 128 else 0)
    b = render_glyph_mask(font_path, codepoint, px, a.width).point(lambda v: 255 if v >= 128 else 0)
    best = 0.0
    for dx in range(-max_shift, max_shift + 1):
        for dy in range(-max_shift, max_shift + 1):
            bs = ImageChops.offset(b, dx, dy)
            inter = ImageChops.multiply(a, bs).histogram()[255]
            union = ImageChops.lighter(a, bs).histogram()[255]
            best = max(best, inter / union if union else 1.0)
    return best


def mask_iou(a: Image.Image, b: Image.Image, threshold: int = 128) -> float:
    ma = a.point(lambda v: 255 if v >= threshold else 0)
    mb = b.point(lambda v: 255 if v >= threshold else 0)
    inter = ImageChops.multiply(ma, mb).histogram()[255]
    union = ImageChops.lighter(ma, mb).histogram()[255]
    return (inter / union) if union else 1.0
