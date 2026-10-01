import json
from pathlib import Path

import pytest

from typeicon_fonts.compiler import FontSpec, GlyphSpec, compile_font
from typeicon_fonts.outline import svg_to_outline
from typeicon_fonts.svg_sanitize import sanitize_svg

ROOT = Path(__file__).resolve().parents[3]


SAMPLE_EVERY = 100  # the fixtures compile their own fonts; the full 22,800 are validated by the release build itself
ALWAYS = {"home", "search", "settings", "user", "arrow-right"}


def core_meta():
    # Individually drawn designs, sampled (every 100th by name, plus the icons the tests name); variants are
    # generated from them and checked separately by sampling. The release build validates every glyph.
    icons = json.loads((ROOT / "assets/core/core-icons.json").read_text())["icons"]
    bases = sorted((m for m in icons if m.get("dir", "svg") == "svg"), key=lambda m: m["name"])
    return [m for i, m in enumerate(bases) if i % SAMPLE_EVERY == 0 or m["name"] in ALWAYS]


def core_codepoints():
    reg = json.loads((ROOT / "assets/registry/codepoints.json").read_text())
    return reg["namespaces"]["core"]["assignments"]


@pytest.fixture(scope="session")
def core_fonts(tmp_path_factory):
    """Compile the three Core families from the canonical SVGs (independent of any release build)."""
    out = tmp_path_factory.mktemp("core-fonts")
    cps = core_codepoints()
    built = {}
    for style in ("filled", "line", "rounded"):
        glyphs = []
        for m in core_meta():
            o = svg_to_outline(sanitize_svg((ROOT / f"assets/core/svg/{style}/{m['name']}.svg").read_bytes()).svg)
            cp = cps[m["name"]]
            mirror = [0xE000 + cp - 0xF0000] if cp - 0xF0000 < 6400 else []  # BMP mirror: first 6,400 concepts only
            glyphs.append(GlyphSpec(f"u{cp:X}", [cp, *mirror], [m["name"], *m["aliases"]], o.path, o.advance))
        spec = FontSpec(f"TypeIcon {style.title()}", f"TypeIcon{style.title()}-Regular", "0.1.0", glyphs)
        built[style] = compile_font(spec, out / style)
    return built
