"""SVG -> font outline conversion: transforms, strokes, holes, clip paths, y inversion, viewBox."""
import math

import pytest

from typeicon_fonts.outline import ASCENT, DESCENT, UPM, OutlineError, svg_to_outline

S = 1200 / 24  # font units per grid unit
W = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">{}</svg>'


def area(o):
    return abs(o.path.area) / (S * S)


def test_rect_area_and_y_inversion():
    o = svg_to_outline(W.format('<rect x="2" y="2" width="4" height="6" fill="#000"/>'))
    assert area(o) == pytest.approx(24, rel=1e-3)
    xmin, ymin, xmax, ymax = o.path.bounds
    # SVG y=2 (top) maps to font y = ASCENT - 2*S (near the top of the em)
    assert ymax == pytest.approx(ASCENT - 2 * S, abs=0.5)
    assert ymin == pytest.approx(ASCENT - 8 * S, abs=0.5)
    assert xmin == pytest.approx(2 * S, abs=0.5)
    assert o.advance == UPM


def test_transforms_are_flattened():
    plain = svg_to_outline(W.format('<rect x="10" y="10" width="4" height="2"/>'))
    moved = svg_to_outline(W.format('<g transform="translate(10 10)"><rect width="4" height="2"/></g>'))
    assert plain.path.bounds == pytest.approx(moved.path.bounds, abs=0.5)
    rot = svg_to_outline(W.format('<rect x="10" y="11" width="4" height="2" transform="rotate(90 12 12)"/>'))
    b = rot.path.bounds
    assert (b[2] - b[0]) == pytest.approx(2 * S, abs=0.5) and (b[3] - b[1]) == pytest.approx(4 * S, abs=0.5)
    scaled = svg_to_outline(W.format('<g transform="matrix(2 0 0 2 0 0)"><rect width="3" height="3"/></g>'))
    assert area(scaled) == pytest.approx(36, rel=1e-3)


def test_stroke_expansion_uses_transformed_width():
    o = svg_to_outline(W.format('<line x1="2" y1="12" x2="22" y2="12" stroke="#000" stroke-width="2"/>'))
    assert area(o) == pytest.approx(40, rel=1e-3)  # 20 long x 2 wide, butt caps
    o2 = svg_to_outline(W.format('<g transform="scale(0.5)"><line x1="4" y1="24" x2="44" y2="24" stroke="#000" stroke-width="4"/></g>'))
    assert area(o2) == pytest.approx(40, rel=1e-3)
    rc = svg_to_outline(W.format('<line x1="2" y1="12" x2="22" y2="12" stroke="#000" stroke-width="2" stroke-linecap="round"/>'))
    assert area(rc) == pytest.approx(40 + math.pi, rel=2e-3)


def test_non_uniform_transform_under_stroke_is_refused():
    with pytest.raises(OutlineError, match="non-uniform"):
        svg_to_outline(W.format('<g transform="scale(2 1)"><circle cx="6" cy="6" r="3" fill="none" stroke="#000"/></g>'))


def test_holes_preserved_nonzero_and_evenodd():
    ring = svg_to_outline(W.format('<path fill-rule="evenodd" d="M2 2h20v20H2z M7 7h10v10H7z"/>'))
    assert area(ring) == pytest.approx(400 - 100, rel=1e-3)
    # Same winding direction + nonzero = filled; opposite direction + nonzero = hole.
    filled = svg_to_outline(W.format('<path d="M2 2h20v20H2z M7 7h10v10H7z"/>'))
    assert area(filled) == pytest.approx(400, rel=1e-3)
    hole = svg_to_outline(W.format('<path d="M2 2h20v20H2z M7 7v10h10V7z"/>'))
    assert area(hole) == pytest.approx(300, rel=1e-3)


def test_overlaps_removed():
    o = svg_to_outline(W.format('<rect x="2" y="2" width="10" height="10"/><rect x="7" y="7" width="10" height="10"/>'))
    assert area(o) == pytest.approx(175, rel=1e-3)
    assert len(list(o.path.contours)) == 1


def test_clip_path_intersection():
    o = svg_to_outline(W.format('<defs><clipPath id="c"><rect x="0" y="0" width="12" height="24"/></clipPath></defs>'
                                '<rect x="2" y="2" width="20" height="20" clip-path="url(#c)"/>'))
    assert area(o) == pytest.approx(200, rel=1e-3)


def test_negative_viewbox_and_wide_artwork():
    m = svg_to_outline('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960"><path d="M0 -960h960v960H0z"/></svg>')
    xmin, ymin, xmax, ymax = m.path.bounds
    assert (ymin, ymax) == pytest.approx((-DESCENT, ASCENT), abs=0.5)
    wide = svg_to_outline('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 24"><rect width="48" height="24"/></svg>')
    assert wide.advance == 2 * UPM  # aspect ratio kept, not squashed


def test_invisible_and_empty():
    with pytest.raises(OutlineError, match="no painted"):
        svg_to_outline(W.format('<path d="M0 0h24v24H0z" fill="none" stroke="none"/>'))
    o = svg_to_outline(W.format('<path d="M0 0h24v24H0z" fill="none" stroke="none"/><rect x="2" y="2" width="2" height="2"/>'))
    assert area(o) == pytest.approx(4, rel=1e-3)
