import json
from pathlib import Path

import pytest

from typeicon_fonts.compiler import FontSpec, GlyphSpec, compile_font
from typeicon_fonts.outline import svg_to_outline
from typeicon_fonts.svg_sanitize import sanitize_svg

ROOT = Path(__file__).resolve().parents[3]


def core_meta():
    # Individually drawn designs; variants are generated from them (checked separately by sampling).
    icons = json.loads((ROOT / "assets/core/core-icons.json").read_text())["icons"]
    return sorted((m for m in icons if m.get("dir", "svg") == "svg"), key=lambda m: m["name"])


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
            glyphs.append(GlyphSpec(f"u{cp:X}", [cp, 0xE000 + cp - 0xF0000], [m["name"], *m["aliases"]], o.path, o.advance))
        spec = FontSpec(f"TypeIcon {style.title()}", f"TypeIcon{style.title()}-Regular", "0.1.0", glyphs)
        built[style] = compile_font(spec, out / style)
    return built
