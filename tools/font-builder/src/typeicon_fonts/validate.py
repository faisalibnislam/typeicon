"""Font validation: OpenType Sanitizer, structural checks, and HarfBuzz shaping."""
from __future__ import annotations

import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import uharfbuzz as hb
from fontTools.ttLib import TTFont

REQUIRED = {"cmap", "head", "hhea", "hmtx", "maxp", "name", "OS/2", "post", "GSUB"}


@dataclass
class ValidationReport:
    path: str
    ok: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    stats: dict = field(default_factory=dict)


def run_ots(path: str | Path) -> tuple[bool, str]:
    """Run OpenType Sanitizer (the validator used by Chrome and Firefox)."""
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "sanitized"
        proc = subprocess.run(
            [sys.executable, "-m", "ots", str(path), str(out)],
            capture_output=True, text=True, timeout=300,
        )
        msg = (proc.stdout + proc.stderr).strip()
        return proc.returncode == 0, msg


def sfnt_bytes(font_path: str | Path) -> bytes:
    """Raw sfnt bytes; WOFF/WOFF2 are unwrapped (HarfBuzz reads only sfnt)."""
    data = Path(font_path).read_bytes()
    if data[:4] in (b"wOFF", b"wOF2"):
        import io
        f = TTFont(io.BytesIO(data))
        f.flavor = None
        buf = io.BytesIO()
        f.save(buf)
        return buf.getvalue()
    return data


class Shaper:
    """Shape text with HarfBuzz, an engine independent of fontTools."""

    def __init__(self, font_path: str | Path):
        blob = hb.Blob(sfnt_bytes(font_path))
        self.face = hb.Face(blob)
        self.font = hb.Font(self.face)

    def glyph_names(self, text: str, features: dict | None = None) -> list[str]:
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.font, buf, features if features is not None else {})
        return [self.font.glyph_to_string(i.codepoint) for i in buf.glyph_infos]

    def shape_one(self, text: str, features: dict | None = None) -> str | None:
        names = self.glyph_names(text, features)
        return names[0] if len(names) == 1 else None


def validate_font(path: str | Path, expected: dict[str, str] | None = None, run_sanitizer: bool = True) -> ValidationReport:
    """Validate a compiled font. `expected` maps keyword -> glyph name to verify by shaping."""
    path = Path(path)
    rep = ValidationReport(path=str(path), ok=True)
    font = TTFont(path)
    tables = set(font.keys())
    outline = "CFF " if "CFF " in tables else "glyf"
    missing = (REQUIRED | {outline}) - tables
    if outline == "glyf":
        missing |= {"loca"} - tables
    if missing:
        rep.errors.append(f"missing tables: {sorted(missing)}")

    name = font["name"]
    ps = name.getDebugName(6) or ""
    if not ps or len(ps) > 63 or any(c in ps for c in " []{}()<>/%"):
        rep.errors.append(f"invalid PostScript name {ps!r}")
    for nid in (1, 2, 3, 4, 5, 6, 13):
        if not name.getDebugName(nid):
            rep.errors.append(f"name ID {nid} missing")

    num_glyphs = font["maxp"].numGlyphs
    rep.stats["numGlyphs"] = num_glyphs
    if num_glyphs > 65535:
        rep.errors.append("glyph count exceeds 65535")
    glyph_order = font.getGlyphOrder()
    if glyph_order[0] != ".notdef":
        rep.errors.append(".notdef is not glyph 0")

    # Clipping: every glyph must sit within usWinAscent/usWinDescent.
    os2 = font["OS/2"]
    gs = font.getGlyphSet()
    from fontTools.pens.boundsPen import BoundsPen
    worst = 0
    for gname in glyph_order:
        bp = BoundsPen(gs)
        gs[gname].draw(bp)
        if bp.bounds:
            _, ymin, _, ymax = bp.bounds
            over = max(ymax - os2.usWinAscent, -ymin - os2.usWinDescent)
            worst = max(worst, over)
    if worst > 0:
        rep.errors.append(f"glyph outlines exceed win metrics by {worst:.0f} units (clipping risk)")
    if gs[".notdef"] is not None:
        bp = BoundsPen(gs)
        gs[".notdef"].draw(bp)
        if not bp.bounds:
            rep.errors.append(".notdef is blank; it must be visible")

    cmap = font.getBestCmap()
    rep.stats["cmapEntries"] = len(cmap)
    subtables = {(t.platformID, t.platEncID, t.format) for t in font["cmap"].tables}
    if any(cp > 0xFFFF for cp in cmap) and not any(f == 12 for _, _, f in subtables):
        rep.errors.append("supplementary codepoints present but no cmap format 12")
    rep.stats["cmapFormats"] = sorted({f for _, _, f in subtables})

    gsub = font["GSUB"].table if "GSUB" in font else None
    if gsub:
        feats = {fr.FeatureTag for fr in gsub.FeatureList.FeatureRecord}
        rep.stats["gsubFeatures"] = sorted(feats)
        if "liga" not in feats:
            rep.errors.append("GSUB has no liga feature")
        scripts = {sr.ScriptTag for sr in gsub.ScriptList.ScriptRecord}
        rep.stats["gsubScripts"] = sorted(scripts)
        if not {"DFLT", "latn"} <= scripts:
            rep.errors.append("GSUB must register DFLT and latn scripts")
        rep.stats["gsubLookups"] = len(gsub.LookupList.Lookup)
        rep.stats["gsubSubtables"] = sum(len(lk.SubTable) for lk in gsub.LookupList.Lookup)

    if run_sanitizer:
        ok, msg = run_ots(path)
        rep.stats["ots"] = "pass" if ok else "fail"
        if not ok:
            rep.errors.append(f"OTS: {msg[:2000]}")
        elif msg:
            rep.warnings.append(f"OTS: {msg[:500]}")

    if expected:
        shaper = Shaper(path)
        failures = []
        for kw, gname in expected.items():
            got = shaper.glyph_names(kw)
            if got != [gname]:
                failures.append(f"{kw!r} -> {got} (expected [{gname!r}])")
        rep.stats["shapingChecked"] = len(expected)
        if failures:
            rep.errors.append(f"{len(failures)} shaping failures: " + "; ".join(failures[:20]))

    rep.ok = not rep.errors
    return rep
