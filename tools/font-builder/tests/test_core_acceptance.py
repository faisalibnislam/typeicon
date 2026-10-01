"""Critical acceptance demonstration on the real TypeIcon Core fonts.

A generated font renders home/search/settings/user/arrow-right as the intended glyphs; all three
Core styles share the keywords; a small subset works independently; SVGs visually match glyphs.
"""
import io

import pytest
from fontTools.ttLib import TTFont

from typeicon_fonts.raster import compare, mask_iou, render_svg_mask
from typeicon_fonts.subset import save_formats, subset_font
from typeicon_fonts.validate import Shaper, validate_font

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def core_meta():
    # Individually drawn designs; variants are generated from them (checked separately by sampling).
    icons = json.loads((ROOT / "assets/core/core-icons.json").read_text())["icons"]
    return sorted((m for m in icons if m.get("dir", "svg") == "svg"), key=lambda m: m["name"])


def core_codepoints():
    return json.loads((ROOT / "assets/registry/codepoints.json").read_text())["namespaces"]["core"]["assignments"]

DEMO = ["home", "search", "settings", "user", "arrow-right"]


@pytest.mark.parametrize("style", ["filled", "line", "rounded"])
def test_demo_keywords_render_as_intended_glyphs(core_fonts, style):
    cps = core_codepoints()
    for fmt in ("otf", "ttf"):
        s = Shaper(core_fonts[style][fmt])
        for kw in DEMO:
            assert s.glyph_names(kw) == [f"u{cps[kw]:X}"], (style, fmt, kw)


def test_all_styles_share_every_keyword_and_codepoint(core_fonts):
    cps = core_codepoints()
    for m in core_meta():
        for kw in [m["name"], *m["aliases"]]:
            got = {st: Shaper(core_fonts[st]["otf"]).glyph_names(kw) for st in ("filled", "line", "rounded")}
            assert all(v == [f"u{cps[m['name']]:X}"] for v in got.values()), (kw, got)


@pytest.mark.parametrize("style", ["filled", "line", "rounded"])
def test_full_validation(core_fonts, style):
    cps = core_codepoints()
    expected = {kw: f"u{cps[m['name']]:X}" for m in core_meta() for kw in [m["name"], *m["aliases"]]}
    for fmt in ("otf", "ttf", "woff2"):
        rep = validate_font(core_fonts[style][fmt], expected)
        assert rep.ok, rep.errors


def test_subset_works_independently(core_fonts, tmp_path):
    cps = core_codepoints()
    keep = [f"u{cps[n]:X}" for n in ("home", "search")]
    res = subset_font(core_fonts["line"]["otf"], keep, "TypeIcon Kit t 000000 Line", "TypeIconKit000000Line-Regular", "000000")
    out = save_formats(res.font, tmp_path, "kit", ["otf", "woff2"])
    s = Shaper(out["otf"])
    assert s.glyph_names("home") == [keep[0]] and s.glyph_names("house") == [keep[0]]
    assert s.glyph_names("magnify") == [keep[1]]
    for gone in ("settings", "user", "arrow-right", "gear"):
        assert len(s.glyph_names(gone)) == len(gone), gone
    f = TTFont(out["otf"])
    assert f["name"].getDebugName(1) == "TypeIcon Kit t 000000 Line"
    assert f["name"].getDebugName(13)  # license string preserved
    assert validate_font(out["woff2"], {"home": keep[0]}).ok


def _match(svg: str, font: str, cp: int) -> float:
    """Same rule as the release check: 96 px, and a shift-tolerant 384 px recheck for small edge-rounding differences."""
    from typeicon_fonts.raster import compare_aligned
    iou = compare(svg, font, cp, 96).iou
    return iou if iou >= 0.97 else compare_aligned(svg, font, cp, 384, 1)


@pytest.mark.parametrize("style", ["filled", "line", "rounded"])
def test_svg_and_font_glyphs_visually_match(core_fonts, style):
    cps = core_codepoints()
    worst = min(
        (_match((ROOT / f"assets/core/svg/{style}/{m['name']}.svg").read_text(), str(core_fonts[style]["otf"]), cps[m["name"]]), m["name"])
        for m in core_meta()
    )
    assert worst[0] >= 0.95, worst


def test_core_styles_are_not_identical_geometry():
    for m in core_meta():
        masks = {st: render_svg_mask((ROOT / f"assets/core/svg/{st}/{m['name']}.svg").read_text(), 48) for st in ("filled", "line", "rounded")}
        for a, b in (("filled", "line"), ("filled", "rounded"), ("line", "rounded")):
            assert mask_iou(masks[a], masks[b]) < 0.995, (m["name"], a, b)


@pytest.mark.parametrize("style", ["filled", "line", "rounded"])
def test_variant_sample_matches_release_font(style):
    """Generated variants (base + badge) render the same as their compiled glyphs in the release font."""
    import random
    rel = ROOT / "dist/releases/0.3.0/typeicon-release"
    if not rel.exists():
        pytest.skip("release 0.3.0 not built")
    fams = {f["slug"]: f for f in json.loads((rel / "metadata/families.json").read_text())}
    font = rel / "desktop" / fams[f"core-{style}"]["files"]["otf"]["name"]
    icons = json.loads((ROOT / "assets/core/core-icons.json").read_text())["icons"]
    variants = [m for m in icons if m.get("variantOf")]
    cps = core_codepoints()
    for m in random.Random(7).sample(variants, min(40, len(variants))):
        svg = (ROOT / f"assets/core/svg-variants/{style}/{m['name']}.svg").read_text()
        iou = _match(svg, str(font), cps[m["name"]])
        assert iou >= 0.95, (m["name"], iou)
