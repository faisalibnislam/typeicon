"""Thin is Line's geometry with half the stroke weight."""
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]


def core_meta():
    icons = json.loads((ROOT / "assets/core/core-icons.json").read_text())["icons"]
    return sorted((m for m in icons if m.get("dir", "svg") == "svg"), key=lambda m: m["name"])


def _svg(style: str, name: str) -> str | None:
    p = ROOT / f"assets/core/svg/{style}/{name}.svg"
    return p.read_text() if p.exists() else None


def test_thin_artwork_is_exported_for_every_base_icon():
    missing = [m["name"] for m in core_meta() if _svg("thin", m["name"]) is None]
    if len(missing) == len(core_meta()):
        pytest.skip("thin artwork not exported yet (run tools/core-authoring/export.py)")
    assert not missing[:5], missing[:5]


def test_thin_has_half_the_stroke_width_and_the_same_centre_lines_as_line():
    checked = 0
    for m in core_meta()[:400]:
        line, thin = _svg("line", m["name"]), _svg("thin", m["name"])
        if thin is None:
            pytest.skip("thin artwork not exported yet")
        assert 'stroke-width="2"' in line and 'stroke-width="1"' in thin, m["name"]
        assert 'stroke-linecap="butt"' in thin and 'stroke-linejoin="miter"' in thin, m["name"]
        # drawn parts keep their centre lines; only outlined regions (badge gaps, hidden-behind shapes) are
        # recomputed for the thinner stroke, so compare the stroked parts that exist in both
        stroked = lambda s: [d for d, rest in re.findall(r'<path d="([^"]+)"([^>]*)/>', s) if "fill=" not in rest]  # noqa: E731
        assert stroked(line) == stroked(thin), m["name"]
        checked += 1
    assert checked


def test_thin_is_not_a_filled_or_rounded_copy():
    for m in core_meta()[:200]:
        thin = _svg("thin", m["name"])
        if thin is None:
            pytest.skip("thin artwork not exported yet")
        assert 'stroke-linecap="round"' not in thin
