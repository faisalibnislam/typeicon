"""Readable ASCII fallback glyphs (original monoline design, no third-party font data).

These glyphs render partially typed or unknown keywords as legible text, so a typo shows
"hom" rather than blank space. Skeletons are authored y-down (like SVG) on a baseline at
y=0 with cap height 700 / x-height 520 / descender 200 in a 440-wide body, stroked with
round caps and joins, then scaled into the icon em (UPM 1200).
"""
from __future__ import annotations

from functools import lru_cache

from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path
from pathops import LineCap, LineJoin, Path, PathOp, op

SCALE = 1.2  # skeleton units -> font units
STROKE = 88
SIDEBEARING = 110
BODY = 440
ADVANCE = round((BODY + 2 * SIDEBEARING) * SCALE)  # 792: monospaced


def _o(cx, cy, rx, ry):
    return f"M{cx - rx} {cy}A{rx} {ry} 0 1 0 {cx + rx} {cy}A{rx} {ry} 0 1 0 {cx - rx} {cy}Z"


BOWL = _o(220, -260, 215, 260)
DOT = "dot"

# name -> (unicode, [skeleton d-strings | ("dot", x, y)])
GLYPHS: dict[str, tuple[int, list]] = {
    "a": (0x61, [BOWL, "M435 -520V0"]),
    "b": (0x62, ["M5 -740V0", BOWL]),
    "c": (0x63, ["M420 -420A215 260 0 1 0 420 -100"]),
    "d": (0x64, ["M435 -740V0", BOWL]),
    "e": (0x65, ["M10 -270H430A215 260 0 1 0 395 -90"]),
    "f": (0x66, ["M150 0V-570A160 160 0 0 1 410 -690", "M20 -510H370"]),
    "g": (0x67, [BOWL, "M435 -520V40A180 170 0 0 1 60 130"]),
    "h": (0x68, ["M5 -740V0", "M5 -300Q5 -520 220 -520Q435 -520 435 -300V0"]),
    "i": (0x69, ["M220 -520V0", (DOT, 220, -700)]),
    "j": (0x6A, ["M300 -520V60A160 150 0 0 1 20 140", (DOT, 300, -700)]),
    "k": (0x6B, ["M5 -740V0", "M420 -520L5 -200", "M150 -310L435 0"]),
    "l": (0x6C, ["M220 -740V-120Q220 0 340 0"]),
    "m": (0x6D, ["M5 -520V0", "M5 -380Q5 -520 112 -520Q220 -520 220 -380V0",
                 "M220 -380Q220 -520 328 -520Q435 -520 435 -380V0"]),
    "n": (0x6E, ["M5 -520V0", "M5 -320Q5 -520 220 -520Q435 -520 435 -320V0"]),
    "o": (0x6F, [BOWL]),
    "p": (0x70, ["M5 -520V200", BOWL]),
    "q": (0x71, ["M435 -520V200", BOWL]),
    "r": (0x72, ["M5 -520V0", "M5 -300Q5 -520 240 -520H400"]),
    "s": (0x73, ["M410 -450Q380 -520 220 -520Q30 -520 30 -395Q30 -270 220 -260Q415 -250 415 -125Q415 0 220 0Q40 0 10 -80"]),
    "t": (0x74, ["M170 -690V-110Q170 0 290 0H400", "M20 -510H400"]),
    "u": (0x75, ["M5 -520V-210Q5 0 220 0Q435 0 435 -210", "M435 -520V0"]),
    "v": (0x76, ["M5 -520L220 0L435 -520"]),
    "w": (0x77, ["M0 -520L105 0L220 -400L335 0L440 -520"]),
    "x": (0x78, ["M15 -520L425 0", "M425 -520L15 0"]),
    "y": (0x79, ["M5 -520L225 -10", "M435 -520L150 200"]),
    "z": (0x7A, ["M25 -520H415L25 0H420"]),
    "A": (0x41, ["M0 0L220 -700L440 0", "M75 -230H365"]),
    "B": (0x42, ["M10 0V-700H250Q420 -700 420 -530Q420 -365 250 -365H10",
                 "M250 -365Q440 -365 440 -180Q440 0 250 0H10"]),
    "C": (0x43, ["M425 -560A215 350 0 1 0 425 -140"]),
    "D": (0x44, ["M10 0V-700H170Q435 -700 435 -350Q435 0 170 0Z"]),
    "E": (0x45, ["M420 -700H10V0H420", "M10 -360H340"]),
    "F": (0x46, ["M420 -700H10V0", "M10 -360H340"]),
    "G": (0x47, ["M425 -560A215 350 0 1 0 435 -300H250"]),
    "H": (0x48, ["M5 -700V0", "M435 -700V0", "M5 -360H435"]),
    "I": (0x49, ["M70 -700H370", "M220 -700V0", "M70 0H370"]),
    "J": (0x4A, ["M380 -700V-200Q380 0 195 0Q10 0 10 -200"]),
    "K": (0x4B, ["M10 -700V0", "M420 -700L10 -260", "M155 -415L440 0"]),
    "L": (0x4C, ["M20 -700V0H420"]),
    "M": (0x4D, ["M0 0V-700L220 -290L440 -700V0"]),
    "N": (0x4E, ["M5 0V-700L435 0V-700"]),
    "O": (0x4F, [_o(220, -350, 218, 350)]),
    "P": (0x50, ["M10 0V-700H260Q435 -700 435 -505Q435 -310 260 -310H10"]),
    "Q": (0x51, [_o(220, -350, 218, 350), "M270 -170L440 30"]),
    "R": (0x52, ["M10 0V-700H260Q435 -700 435 -505Q435 -310 260 -310H10", "M250 -310L435 0"]),
    "S": (0x53, ["M410 -610Q370 -700 220 -700Q25 -700 25 -530Q25 -370 220 -355Q425 -340 425 -175Q425 0 220 0Q45 0 10 -100"]),
    "T": (0x54, ["M0 -700H440", "M220 -700V0"]),
    "U": (0x55, ["M5 -700V-230Q5 0 220 0Q435 0 435 -230V-700"]),
    "V": (0x56, ["M0 -700L220 0L440 -700"]),
    "W": (0x57, ["M0 -700L100 0L220 -500L340 0L440 -700"]),
    "X": (0x58, ["M10 -700L430 0", "M430 -700L10 0"]),
    "Y": (0x59, ["M0 -700L220 -340L440 -700", "M220 -340V0"]),
    "Z": (0x5A, ["M20 -700H420L20 0H425"]),
    "zero": (0x30, [_o(220, -350, 210, 350), "M90 -110L350 -590"]),
    "one": (0x31, ["M95 -560L245 -700V0", "M80 0H400"]),
    "two": (0x32, ["M30 -560Q65 -700 220 -700Q410 -700 410 -520Q410 -390 220 -255L20 0H425"]),
    "three": (0x33, ["M30 -640Q100 -700 220 -700Q405 -700 405 -540Q405 -375 205 -375Q425 -375 425 -190Q425 0 220 0Q60 0 15 -85"]),
    "four": (0x34, ["M330 0V-700L0 -215H440"]),
    "five": (0x35, ["M405 -700H65L40 -390Q120 -440 225 -440Q425 -440 425 -220Q425 0 210 0Q60 0 15 -80"]),
    "six": (0x36, ["M385 -655Q320 -700 235 -700Q20 -700 20 -330Q20 0 230 0Q430 0 430 -220Q430 -430 230 -430Q65 -430 20 -300"]),
    "seven": (0x37, ["M15 -700H425L155 0"]),
    "eight": (0x38, [_o(220, -535, 175, 165), _o(220, -190, 205, 190)]),
    "nine": (0x39, ["M55 -45Q120 0 205 0Q420 0 420 -370Q420 -700 210 -700Q10 -700 10 -480Q10 -270 210 -270Q375 -270 420 -400"]),
    "hyphen": (0x2D, ["M70 -300H370"]),
    "underscore": (0x5F, ["M0 130H440"]),
    "period": (0x2E, [(DOT, 220, -40)]),
    "comma": (0x2C, ["M245 -50L185 130"]),
    "colon": (0x3A, [(DOT, 220, -40), (DOT, 220, -470)]),
    "semicolon": (0x3B, ["M245 -50L185 130", (DOT, 220, -470)]),
    "exclam": (0x21, ["M220 -700V-220", (DOT, 220, -40)]),
    "question": (0x3F, ["M40 -560Q65 -700 220 -700Q400 -700 400 -545Q400 -425 220 -365V-220", (DOT, 220, -40)]),
    "slash": (0x2F, ["M410 -740L30 120"]),
    "parenleft": (0x28, ["M320 -760Q120 -560 120 -280Q120 0 320 200"]),
    "parenright": (0x29, ["M120 -760Q320 -560 320 -280Q320 0 120 200"]),
    "quotesingle": (0x27, ["M220 -740V-540"]),
    "quotedbl": (0x22, ["M140 -740V-540", "M300 -740V-540"]),
    "plus": (0x2B, ["M220 -520V-100", "M20 -310H420"]),
    "equal": (0x3D, ["M40 -410H400", "M40 -210H400"]),
    "numbersign": (0x23, ["M150 -640L110 -60", "M330 -640L290 -60", "M40 -450H420", "M20 -250H400"]),
}


@lru_cache(maxsize=None)
def fallback_outline(name: str) -> Path:
    """Return the stroked outline for a fallback glyph in font units (y-up)."""
    _, parts = GLYPHS[name]
    m = (SCALE, 0, 0, -SCALE, SIDEBEARING * SCALE, 0)
    out: Path | None = None
    for part in parts:
        p = Path()
        if isinstance(part, tuple):
            _, x, y = part
            r = STROKE * 0.62
            d = f"M{x - r} {y}A{r} {r} 0 1 0 {x + r} {y}A{r} {r} 0 1 0 {x - r} {y}Z"
            parse_path(d, TransformPen(p.getPen(), m))
        else:
            parse_path(part, TransformPen(p.getPen(), m))
            p.stroke(STROKE * SCALE, LineCap.ROUND_CAP, LineJoin.ROUND_JOIN, 4)
            p.convertConicsToQuads()
        p.simplify(fix_winding=True)
        out = p if out is None else op(out, p, PathOp.UNION, fix_winding=True)
    assert out is not None
    return out


def notdef_outline(advance: int, ascent: int, descent: int) -> Path:
    """A visible .notdef: box with a diagonal cross, so missing glyphs are never blank."""
    w = 70
    x0, x1 = 120, advance - 120
    y0, y1 = -descent + 60, ascent - 60
    outer = Path()
    pen = outer.getPen()
    pen.moveTo((x0, y0)); pen.lineTo((x1, y0)); pen.lineTo((x1, y1)); pen.lineTo((x0, y1)); pen.closePath()
    inner = Path()
    pen = inner.getPen()
    pen.moveTo((x0 + w, y0 + w)); pen.lineTo((x1 - w, y0 + w)); pen.lineTo((x1 - w, y1 - w)); pen.lineTo((x0 + w, y1 - w)); pen.closePath()
    box = op(outer, inner, PathOp.DIFFERENCE, fix_winding=True)
    cross = Path()
    pen = cross.getPen()
    pen.moveTo((x0 + w, y0 + w)); pen.lineTo((x1 - w, y1 - w))
    pen.moveTo((x1 - w, y0 + w)); pen.lineTo((x0 + w, y1 - w))
    cross.stroke(w * 0.8, LineCap.BUTT_CAP, LineJoin.MITER_JOIN, 4)
    cross.simplify(fix_winding=True)
    return op(box, cross, PathOp.UNION, fix_winding=True)
