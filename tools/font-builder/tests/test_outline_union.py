"""Skia can return a wrong union without raising when edges coincide exactly; the converter must catch it."""
from typeicon_fonts.outline import svg_to_outline

# A stroked rounded frame with a solid header band whose outer edges sit exactly on the stroke's outer edge
# (the shape of the Core icon table-data, which lost its header in the first 0.3.0 build).
FLUSH = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M5 4H19A2 2 0 0 1 21 6V18A2 2 0 0 1 19 20H5A2 2 0 0 1 3 18V6A2 2 0 0 1 5 4Z"/>
  <path d="M2 9.5V6A3 3 0 0 1 5 3H19A3 3 0 0 1 22 6V9.5Z" fill="currentColor" stroke="none"/>
  <path d="M3 9.5L21 9.5"/>
</svg>"""
HEADER_ONLY = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
  <path d="M2 9.5V6A3 3 0 0 1 5 3H19A3 3 0 0 1 22 6V9.5Z"/>
</svg>"""


def test_union_keeps_a_solid_band_flush_with_a_stroked_frame():
    full = abs(svg_to_outline(FLUSH).path.area)
    header = abs(svg_to_outline(HEADER_ONLY).path.area)
    # the header band (about 20 x 6.5 grid px) must be part of the glyph, not dropped
    assert full > header * 1.5
    assert full > 20 * 6 * 50 * 50
