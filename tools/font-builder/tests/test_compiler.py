"""OpenType compiler: GSUB ligatures shaped independently by HarfBuzz, cmap, names, validation, determinism."""
import hashlib

import pytest
from fontTools.ttLib import TTFont
from pathops import Path as PPath

from typeicon_fonts.compiler import CompileError, FontSpec, GlyphSpec, compile_font
from typeicon_fonts.validate import Shaper, run_ots, validate_font


def box(i):
    p = PPath()
    pen = p.getPen()
    x = 100 + (i % 7) * 20
    pen.moveTo((x, 0)); pen.lineTo((x + 600, 0)); pen.lineTo((x + 600, 800)); pen.lineTo((x, 800)); pen.closePath()
    return p


def spec(entries, name="Test Icons"):
    glyphs = [GlyphSpec(f"u{cp:X}", cps, kws, box(i)) for i, (cp, cps, kws) in enumerate(entries)]
    return FontSpec(name, name.replace(" ", "") + "-Regular", "0.1.0", glyphs)


ENTRIES = [
    (0xF0000, [0xF0000, 0xE000], ["arrow"]),
    (0xF0001, [0xF0001, 0xE001], ["arrow-right", "arrow-forward"]),
    (0xF0002, [0xF0002, 0xE002], ["arrow-right-circle"]),
    (0xF0003, [0xF0003, 0xE003], ["home", "house"]),
    (0x100000, [0x100000], ["tabler-home"]),
]


@pytest.fixture(scope="module")
def fonts(tmp_path_factory):
    return compile_font(spec(ENTRIES), tmp_path_factory.mktemp("f"))


@pytest.mark.parametrize("fmt", ["otf", "ttf", "woff2", "woff"])
def test_longest_match_prefix_collisions(fonts, fmt):
    s = Shaper(fonts[fmt])
    assert s.glyph_names("arrow") == ["uF0000"]
    assert s.glyph_names("arrow-right") == ["uF0001"]
    assert s.glyph_names("arrow-right-circle") == ["uF0002"]
    assert s.glyph_names("arrow-right-circl") == ["uF0001", "hyphen", "c", "i", "r", "c", "l"]
    assert s.glyph_names("arrow-forward") == ["uF0001"]  # alias -> same glyph, not a duplicate


def test_aliases_do_not_duplicate_glyphs(fonts):
    f = TTFont(fonts["otf"])
    import re
    icon_glyphs = [g for g in f.getGlyphOrder() if re.fullmatch(r"u[0-9A-F]{4,6}", g)]
    assert sorted(icon_glyphs) == sorted(f"u{e[0]:X}" for e in ENTRIES)


def test_unknown_partial_and_case_stay_readable(fonts):
    s = Shaper(fonts["otf"])
    assert s.glyph_names("hom") == ["h", "o", "m"]
    assert s.glyph_names("Home") == ["H", "o", "m", "e"]
    assert s.glyph_names("zebra") == ["z", "e", "b", "r", "a"]
    # Documented limitation of ligature fonts: known names inside longer words still match.
    assert s.glyph_names("homework")[0] == "uF0003"


def test_space_separated_keywords_and_feature_off(fonts):
    s = Shaper(fonts["otf"])
    assert s.glyph_names("home arrow") == ["uF0003", "space", "uF0000"]
    # With both ligature features disabled, the keyword stays as text.
    assert s.glyph_names("home", {"liga": False, "rlig": False}) == ["h", "o", "m", "e"]


def test_cmap_formats_and_supplementary_pua(fonts):
    f = TTFont(fonts["ttf"])
    formats = {t.format for t in f["cmap"].tables}
    assert {4, 12} <= formats
    cmap = f.getBestCmap()
    assert cmap[0xF0003] == "uF0003" and cmap[0xE003] == "uF0003" and cmap[0x100000] == "u100000"
    s = Shaper(fonts["ttf"])
    assert s.glyph_names(chr(0xF0003)) == ["uF0003"]
    assert s.glyph_names(chr(0x100000)) == ["u100000"]
    # Supplementary characters survive a UTF-16 round trip without truncation.
    assert chr(0x100000).encode("utf-16-le").decode("utf-16-le") == chr(0x100000)


def test_names_metrics_and_validation(fonts):
    for fmt in ("otf", "ttf", "woff2"):
        rep = validate_font(fonts[fmt], {"home": "uF0003", "house": "uF0003"})
        assert rep.ok, rep.errors
    f = TTFont(fonts["otf"])
    n = f["name"]
    assert n.getDebugName(1) == "Test Icons" and n.getDebugName(6) == "TestIcons-Regular"
    assert n.getDebugName(13) and n.getDebugName(14)
    assert f["OS/2"].fsSelection & 0x80  # USE_TYPO_METRICS
    assert f["OS/2"].usWeightClass == 400
    ok, msg = run_ots(fonts["otf"])
    assert ok, msg


def test_deterministic_output(tmp_path):
    a = compile_font(spec(ENTRIES), tmp_path / "a")
    b = compile_font(spec(ENTRIES), tmp_path / "b")
    for fmt in a:
        assert hashlib.sha256(a[fmt].read_bytes()).hexdigest() == hashlib.sha256(b[fmt].read_bytes()).hexdigest(), fmt


@pytest.mark.parametrize("bad,match", [
    ([(0xF0000, [0xF0000], ["x"])], "invalid keyword"),
    ([(0xF0000, [0xF0000], ["Home"])], "invalid keyword"),
    ([(0xF0000, [0xF0000], ["home"]), (0xF0001, [0xF0001], ["home"])], "keyword collision"),
    ([(0xF0000, [0xF0000], ["home"]), (0xF0001, [0xF0000], ["house"])], "codepoint collision"),
])
def test_invalid_specs_are_refused(tmp_path, bad, match):
    with pytest.raises(CompileError, match=match):
        compile_font(spec(bad), tmp_path)


def test_large_font_uses_extension_lookups(tmp_path):
    entries = [(0x100000 + i, [0x100000 + i], [f"icon-{i:05d}", f"alias-{i:05d}"]) for i in range(3000)]
    out = compile_font(spec(entries, "Big Icons"), tmp_path, formats=("otf",))
    f = TTFont(out["otf"])
    lookups = f["GSUB"].table.LookupList.Lookup
    assert any(lk.LookupType == 7 for lk in lookups)  # Extension
    s = Shaper(out["otf"])
    for i in (0, 1234, 2999):
        assert s.glyph_names(f"icon-{i:05d}") == [f"u{0x100000 + i:X}"]
        assert s.glyph_names(f"alias-{i:05d}") == [f"u{0x100000 + i:X}"]
    assert run_ots(out["otf"])[0]
