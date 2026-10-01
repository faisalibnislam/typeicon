"""Transform-derived Core designs (rotations, mirrors, copies) are detected from the artwork itself."""
import sys
from pathlib import Path

AUTHORING = Path(__file__).resolve().parents[2] / "core-authoring"
sys.path.insert(0, str(AUTHORING))

from dsl import DslIcon, line, poly, rect, seg, shell  # noqa: E402
from transforms import detect  # noqa: E402


def _icon(name, draw):
    return DslIcon(name, "test", "test", ["t"], [], draw)


def _arrow(pts_head, shaft):
    return lambda S: [line(seg(*shaft)), line(poly(pts_head, r=S.r))]


RIGHT = _icon("t-right", _arrow([(13, 6), (19, 12), (13, 18)], (5, 12, 18.5, 12)))
DOWN = _icon("t-down", _arrow([(6, 13), (12, 19), (18, 13)], (12, 5, 12, 18.5)))   # RIGHT rotated 90°
LEFT = _icon("t-left", _arrow([(11, 6), (5, 12), (11, 18)], (19, 12, 5.5, 12)))    # RIGHT mirrored
BOX = _icon("t-box", lambda S: [shell(rect(4, 6, 16, 12, S.R)), line(seg(8, 10, 16, 10))])
BOX_COPY = _icon("t-box-copy", lambda S: [shell(rect(4, 6, 16, 12, S.R)), line(seg(8, 10, 16, 10))])


def test_rotations_mirrors_and_copies_are_detected():
    d = detect([RIGHT, DOWN, LEFT, BOX, BOX_COPY])
    assert d["t-down"] == {"name": "t-right", "transform": "rotated 90°"}
    assert d["t-left"]["name"] == "t-right"
    assert d["t-box-copy"] == {"name": "t-box", "transform": "identical artwork"}
    assert "t-right" not in d and "t-box" not in d  # the first-drawn design stays the original


def test_distinct_designs_are_not_flagged():
    assert detect([RIGHT, BOX]) == {}


def test_authoring_check_reserves_the_same_css_names_as_the_release():
    import check
    from typeicon_import.release import RESERVED_CLASS_NAMES
    assert check.RESERVED_CLASS_NAMES == RESERVED_CLASS_NAMES


def test_every_badge_has_search_wording():
    from modifiers import MODIFIERS, SEARCH
    assert set(SEARCH) == set(MODIFIERS)
    for use, phrases in SEARCH.values():
        assert "{n}" in use and phrases and all("{n}" in p for p in phrases)
