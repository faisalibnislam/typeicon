"""OpenType compiler for TypeIcon icon fonts.

Produces, from one FontSpec:
  * OTF  - CFF (cubic) outlines, counter-clockwise outer contours
  * TTF  - glyf (quadratic via cu2qu, max error 1 unit = 1/1200 em), clockwise outer contours
  * WOFF2 / WOFF - web wrappers of the TTF

GSUB: a single ligature lookup (leftmost-longest across the whole name set), registered
under DFLT/dflt and latn/dflt for both `liga` and `rlig`. The lookup is emitted with
useExtension above EXTENSION_THRESHOLD rules so large fonts cannot overflow 16-bit offsets;
fontTools additionally splits subtables on overflow. Aliases map to the same output glyph.

cmap: format 4 (BMP) and format 12 (supplementary PUA) are built automatically.
"""
from __future__ import annotations

import hashlib
import io
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path as FsPath

from fontTools.fontBuilder import FontBuilder
from fontTools.misc.timeTools import timestampSinceEpoch
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, newTable
from pathops import Path

from .fallback import ADVANCE as FALLBACK_ADVANCE
from .fallback import GLYPHS as FALLBACK_GLYPHS
from .fallback import fallback_outline, notdef_outline
from .outline import ASCENT, DESCENT, UPM

TOOLCHAIN_VERSION = "typeicon-fonts/0.2.0"  # bump whenever outline conversion changes (invalidates the build cache)
EXTENSION_THRESHOLD = 1500
# Keywords: lowercase ASCII kebab-case, at least 2 characters. Single characters are refused
# because a ligature on one letter would replace that letter everywhere it is typed.
NAME_RE = re.compile(r"^(?=.{2,64}$)[a-z0-9]+(?:-[a-z0-9]+)*$")
CHAR_GLYPH = {chr(u): n for n, (u, _) in FALLBACK_GLYPHS.items()}


@dataclass
class GlyphSpec:
    glyph_name: str  # e.g. "uF0000"
    codepoints: list[int]  # primary PUA first, then permanent mirrors
    keywords: list[str]  # canonical name first, then explicit aliases
    outline: Path  # font units, y-up
    advance: int = UPM


@dataclass
class FontSpec:
    family: str  # "TypeIcon Line"
    ps_name: str  # "TypeIconLine-Regular"
    version: str  # semantic version "0.1.0"
    glyphs: list[GlyphSpec]
    copyright: str = "Copyright (c) TypeIcon contributors"
    license_description: str = "See licenses/ in the TypeIcon release for the licenses covering these glyphs."
    license_url: str = "https://typeicon.net/licenses"
    vendor_url: str = "https://typeicon.net"
    manufacturer: str = "TypeIcon"
    designer: str = "TypeIcon"
    description: str = "TypeIcon icon font. Type an icon name with ligatures enabled to render the icon."
    build_epoch: int = 1767225600  # 2026-01-01T00:00:00Z; overridden by SOURCE_DATE_EPOCH/release date
    style_name: str = "Regular"
    extra_notices: list[str] = field(default_factory=list)


class CompileError(ValueError):
    pass


# --------------------------------------------------------------------------- helpers

def _head_revision(version: str) -> tuple[float, str]:
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)", version)
    if not m:
        raise CompileError(f"version must be semver, got {version!r}")
    major, minor, patch = (int(x) for x in m.groups())
    if minor > 99 or patch > 9:
        raise CompileError("minor must be < 100 and patch < 10 to map into head.fontRevision")
    rev = f"{major}.{minor:02d}{patch}"
    return float(rev), rev


def _validate(spec: FontSpec) -> None:
    if not re.fullmatch(r"[A-Za-z0-9-]{1,63}", spec.ps_name):
        raise CompileError(f"invalid PostScript name {spec.ps_name!r}")
    seen_kw: dict[str, str] = {}
    seen_cp: dict[int, str] = {}
    seen_gn: set[str] = set()
    for g in spec.glyphs:
        if g.glyph_name in seen_gn or g.glyph_name in FALLBACK_GLYPHS or g.glyph_name in (".notdef", "space"):
            raise CompileError(f"duplicate glyph name {g.glyph_name}")
        seen_gn.add(g.glyph_name)
        for kw in g.keywords:
            if not NAME_RE.match(kw) or len(kw) > 64:
                raise CompileError(f"invalid keyword {kw!r}")
            if kw in seen_kw:
                raise CompileError(f"keyword collision {kw!r}: {seen_kw[kw]} vs {g.glyph_name}")
            seen_kw[kw] = g.glyph_name
        for cp in g.codepoints:
            if cp < 0x80 or cp > 0x10FFFF:
                raise CompileError(f"codepoint out of range U+{cp:X}")
            if cp in seen_cp:
                raise CompileError(f"codepoint collision U+{cp:X}")
            seen_cp[cp] = g.glyph_name


def feature_code(glyphs: list[GlyphSpec]) -> str:
    """OpenType feature source: one ligature lookup shared by liga and rlig."""
    rules = []
    for g in glyphs:
        for kw in g.keywords:
            comps = " ".join(CHAR_GLYPH[c] for c in kw)
            rules.append((kw, f"    sub {comps} by {g.glyph_name};"))
    rules.sort(key=lambda r: (-len(r[0]), r[0]))  # longest first; feaLib also orders by length
    ext = " useExtension" if len(rules) > EXTENSION_THRESHOLD else ""
    body = "\n".join(r[1] for r in rules)
    return (
        "languagesystem DFLT dflt;\nlanguagesystem latn dflt;\n\n"
        f"lookup FI_KEYWORDS{ext} {{\n{body}\n}} FI_KEYWORDS;\n\n"
        "feature liga {\n    lookup FI_KEYWORDS;\n} liga;\n\n"
        "feature rlig {\n    lookup FI_KEYWORDS;\n} rlig;\n"
    )


_TRANSLIT = str.maketrans({"ł": "l", "Ł": "L", "đ": "d", "Đ": "D", "ø": "o", "Ø": "O", "ß": "ss",
                           "æ": "ae", "Æ": "AE", "œ": "oe", "Œ": "OE", chr(0x2014): "-", "–": "-", "’": "'"})


def _latin1(s: str) -> str:
    """CFF Top DICT strings must be Latin-1; the name table keeps the full Unicode text."""
    import unicodedata
    try:
        s.encode("latin-1")
        return s
    except UnicodeEncodeError:
        pass
    s = unicodedata.normalize("NFKD", s.translate(_TRANSLIT))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.encode("latin-1", "replace").decode("latin-1")


def _oriented(p: Path, clockwise: bool) -> Path:
    q = Path(p)
    q.simplify(fix_winding=True, keep_starting_points=False, clockwise=clockwise)
    return q


def _glyph_table(spec: FontSpec):
    """Glyph order + (name -> (advance, outline)) including .notdef, space, fallbacks."""
    table: dict[str, tuple[int, Path | None]] = {
        ".notdef": (UPM, notdef_outline(UPM, ASCENT, DESCENT)),
        "space": (FALLBACK_ADVANCE, None),
    }
    cmap: dict[int, str] = {0x20: "space", 0xA0: "space"}
    for name, (uni, _) in sorted(FALLBACK_GLYPHS.items(), key=lambda kv: kv[1][0]):
        table[name] = (FALLBACK_ADVANCE, fallback_outline(name))
        cmap[uni] = name
    for g in sorted(spec.glyphs, key=lambda g: g.codepoints[0]):
        table[g.glyph_name] = (g.advance, g.outline)
        for cp in g.codepoints:
            cmap[cp] = g.glyph_name
    return list(table.keys()), table, cmap


def _build(spec: FontSpec, ttf: bool) -> TTFont:
    _validate(spec)
    order, table, cmap = _glyph_table(spec)
    revision, rev_str = _head_revision(spec.version)
    fb = FontBuilder(UPM, isTTF=ttf)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)

    metrics = {}
    if ttf:
        glyphs = {}
        for name in order:
            adv, outline = table[name]
            pen = TTGlyphPen(None)
            if outline is not None:
                _oriented(outline, clockwise=True).draw(Cu2QuPen(pen, max_err=1.0, reverse_direction=False))
            glyphs[name] = pen.glyph()
        fb.setupGlyf(glyphs)
        glyf = fb.font["glyf"]
        for name in order:
            g = glyf[name]
            g.recalcBounds(glyf)
            metrics[name] = (table[name][0], getattr(g, "xMin", 0))
    else:
        charstrings = {}
        for name in order:
            adv, outline = table[name]
            pen = T2CharStringPen(adv, None)
            if outline is not None:
                _oriented(outline, clockwise=False).draw(pen)
            charstrings[name] = pen.getCharString()
        fb.setupCFF(
            spec.ps_name,
            {"FullName": _latin1(spec.family), "FamilyName": _latin1(spec.family), "Weight": "Regular",
             "Copyright": _latin1(spec.copyright), "Notice": _latin1(spec.license_description), "version": rev_str},
            charstrings, {},
        )
        cff_glyphs = fb.font["CFF "].cff.topDictIndex[0].CharStrings
        for name in order:
            bounds = cff_glyphs[name].calcBounds(cff_glyphs)
            metrics[name] = (table[name][0], round(bounds[0]) if bounds else 0)

    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=ASCENT, descent=-DESCENT, lineGap=0)

    ymin, ymax = -DESCENT, ASCENT
    for name in order:
        outline = table[name][1]
        if outline is not None and outline.bounds:
            b = outline.bounds
            ymin, ymax = min(ymin, b[1]), max(ymax, b[3])
    win_ascent, win_descent = int(round(ymax)) + 1, int(round(-ymin)) + 1

    unique = hashlib.sha256(
        (spec.family + spec.version + "".join(sorted(k for g in spec.glyphs for k in g.keywords))).encode()
    ).hexdigest()[:12]
    names = {
        "copyright": spec.copyright,
        "familyName": spec.family,
        "styleName": spec.style_name,
        "uniqueFontIdentifier": f"{spec.version};NONE;{spec.ps_name};{unique}",
        "fullName": spec.family if spec.style_name == "Regular" else f"{spec.family} {spec.style_name}",
        "version": f"Version {rev_str};{TOOLCHAIN_VERSION}",
        "psName": spec.ps_name,
        "manufacturer": spec.manufacturer,
        "designer": spec.designer,
        "description": spec.description,
        "vendorURL": spec.vendor_url,
        "licenseDescription": " ".join([spec.license_description, *spec.extra_notices]),
        "licenseInfoURL": spec.license_url,
    }
    fb.setupNameTable(names, mac=False)
    fb.setupOS2(
        version=4, usWeightClass=400, usWidthClass=5, fsType=0, achVendID="NONE",
        fsSelection=0x40 | 0x80,  # REGULAR | USE_TYPO_METRICS
        sTypoAscender=ASCENT, sTypoDescender=-DESCENT, sTypoLineGap=0,
        usWinAscent=win_ascent, usWinDescent=win_descent,
        sxHeight=round(520 * 1.2), sCapHeight=round(700 * 1.2),
        usDefaultChar=0, usBreakChar=0x20, usMaxContext=max((len(k) for g in spec.glyphs for k in g.keywords), default=1),
        ulCodePageRange1=1,  # Latin 1
    )
    fb.setupPost(keepGlyphNames=True, underlinePosition=-100, underlineThickness=60, isFixedPitch=0)
    fb.addOpenTypeFeatures(feature_code(spec.glyphs), filename="typeicon.fea")
    if ttf:
        gasp = newTable("gasp")
        gasp.version = 1
        gasp.gaspRange = {0xFFFF: 0x000F}
        fb.font["gasp"] = gasp

    font = fb.font
    font["OS/2"].recalcUnicodeRanges(font)
    ts = timestampSinceEpoch(spec.build_epoch)
    font["head"].created = ts
    font["head"].modified = ts
    font["head"].fontRevision = revision
    font["head"].flags |= 1 << 3  # force ppem to integer
    font.recalcTimestamp = False
    return font


def compile_font(spec: FontSpec, out_dir: str | FsPath, basename: str | None = None,
                 formats=("otf", "ttf", "woff2", "woff")) -> dict[str, FsPath]:
    """Compile spec into the requested formats. Returns {format: path}."""
    out_dir = FsPath(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    base = basename or spec.ps_name
    written: dict[str, FsPath] = {}
    if "otf" in formats:
        p = out_dir / f"{base}.otf"
        _build(spec, ttf=False).save(p, reorderTables=True)
        written["otf"] = p
    ttf_font = None
    if any(f in formats for f in ("ttf", "woff2", "woff")):
        ttf_font = _build(spec, ttf=True)
        buf = io.BytesIO()
        ttf_font.save(buf, reorderTables=True)
        ttf_bytes = buf.getvalue()
        if "ttf" in formats:
            p = out_dir / f"{base}.ttf"
            p.write_bytes(ttf_bytes)
            written["ttf"] = p
        for flavor in ("woff2", "woff"):
            if flavor in formats:
                f = TTFont(io.BytesIO(ttf_bytes))
                f.recalcTimestamp = False
                f.flavor = flavor
                p = out_dir / f"{base}.{flavor}"
                f.save(p)
                written[flavor] = p
    return written


def build_epoch_from_date(iso_date: str) -> int:
    return int(datetime.fromisoformat(iso_date).replace(tzinfo=timezone.utc).timestamp())
