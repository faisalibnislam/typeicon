"""Subset a released TypeIcon font to selected icons with fontTools.subset.

Why explicit glyph lists: with GSUB closure enabled, keeping the ASCII letters (needed to
type keywords) would pull in *every* ligature output glyph. We therefore disable layout
closure and pass the exact glyph set: .notdef, space, the ASCII fallback glyphs and the
selected icon glyphs. The subsetter then prunes ligature rules whose output glyph was
dropped and keeps the rest. Canonical names and aliases for the selected icons survive,
as do their cmap entries (formats 4 + 12) and all name-table license strings.

The subset is renamed (family, full name, PostScript name, unique id, CFF names) so a
subset never shares a family name with the full font or with a different subset.
"""
from __future__ import annotations

import io
from dataclasses import dataclass
from pathlib import Path

from fontTools import subset as ft_subset
from fontTools.ttLib import TTFont

from .fallback import GLYPHS as FALLBACK_GLYPHS

KEEP_TABLES_EXTRA = ["gasp"]


@dataclass
class SubsetResult:
    font: TTFont
    kept_glyphs: list[str]
    dropped_icons: int


def subset_font(src: str | Path | bytes, icon_glyphs: list[str], family: str, ps_name: str,
                unique_suffix: str) -> SubsetResult:
    data = Path(src).read_bytes() if not isinstance(src, (bytes, bytearray)) else bytes(src)
    font = TTFont(io.BytesIO(data), recalcTimestamp=False)
    order = set(font.getGlyphOrder())
    missing = [g for g in icon_glyphs if g not in order]
    if missing:
        raise KeyError(f"glyphs not in source font: {missing[:5]}")
    base = [".notdef", "space", *FALLBACK_GLYPHS.keys()]
    keep = sorted(set(base) | set(icon_glyphs))
    total_icons = len(order) - len([g for g in order if g in base])

    opts = ft_subset.Options()
    opts.layout_features = ["liga", "rlig"]
    opts.layout_scripts = ["*"]
    opts.layout_closure = False
    opts.name_IDs = ["*"]
    opts.name_languages = ["*"]
    opts.name_legacy = True
    opts.notdef_glyph = True
    opts.notdef_outline = True
    opts.glyph_names = True
    opts.legacy_kern = False
    opts.recalc_timestamp = False
    opts.recalc_bounds = True
    opts.drop_tables = [t for t in opts.drop_tables if t not in KEEP_TABLES_EXTRA]
    opts.passthrough_tables = False
    opts.hinting = True
    sub = ft_subset.Subsetter(opts)
    sub.populate(glyphs=keep)
    sub.subset(font)
    rename_font(font, family, ps_name, unique_suffix)
    return SubsetResult(font=font, kept_glyphs=keep, dropped_icons=total_icons - len(icon_glyphs))


def rename_font(font: TTFont, family: str, ps_name: str, unique_suffix: str) -> None:
    name = font["name"]
    version = name.getDebugName(5) or ""
    for rec in list(name.names):
        if rec.nameID in (1, 4, 16, 18, 21):
            name.removeNames(nameID=rec.nameID)
    for nid, value in ((1, family), (4, family), (6, ps_name), (3, f"{ps_name};{unique_suffix};{version.split(';')[0]}")):
        name.setName(value, nid, 3, 1, 0x409)
    for rec in list(name.names):
        if rec.platformID == 1:  # drop stale Mac-platform records rather than leave old names behind
            name.removeNames(platformID=1)
            break
    if "CFF " in font:
        cff = font["CFF "].cff
        top = cff.topDictIndex[0]
        cff.fontNames = [ps_name]
        top.FullName = family
        top.FamilyName = family


def save_formats(font: TTFont, out_dir: Path, base: str, formats: list[str]) -> dict[str, Path]:
    """Save a subset in requested formats. OTF/TTF outline type follows the source font."""
    out_dir.mkdir(parents=True, exist_ok=True)
    buf = io.BytesIO()
    font.flavor = None
    font.save(buf, reorderTables=True)
    raw = buf.getvalue()
    is_cff = "CFF " in font
    written: dict[str, Path] = {}
    ext = "otf" if is_cff else "ttf"
    if ext in formats:
        p = out_dir / f"{base}.{ext}"
        p.write_bytes(raw)
        written[ext] = p
    for flavor in ("woff2", "woff"):
        if flavor in formats:
            f = TTFont(io.BytesIO(raw), recalcTimestamp=False)
            f.flavor = flavor
            p = out_dir / f"{base}.{flavor}"
            f.save(p)
            written[flavor] = p
    return written
