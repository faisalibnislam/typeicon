"""TypeIcon Core: notation (batch notation_005).

Astrological and alchemical glyphs, divination and esoteric diagrams, workplace hazard warning triangles,
mandatory (blue circle) safety signs, emergency equipment marks and cargo handling marks. Glyphs are open
strokes; closed figures are shells. Figures inside signs follow the small stick style of sets/emergency_002.py:
solid heads and 2 px limbs that are knocked out of the Filled shell.
"""
from __future__ import annotations

import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar  # noqa: F401

CAT = "notation"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def mark(d):
    """Small solid shape: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def head(x, y, r=1.3):
    return dot(x, y, r)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def warn(S, *content):
    """Warning triangle with content inside."""
    tri = poly([(12, 2.5), (22, 20.5), (2, 20.5)], closed=True, r=L(S, 0.0, 1.6))
    return [shell(tri), *content]


def ring(S, *content, r=9.5):
    """Mandatory sign: a ring (solid disc in Filled) with content knocked out."""
    return [shell(circle(12, 12, r)), *content]


def thin(S, d, w=1.5):
    """Fine stroked detail as a small solid mark (knocked out of Filled shells)."""
    return Part("dot", path_to_d(ST(d, w, S.cap, S.join, 4.0)))


def tp(*pts):
    """Polyline d-string through points."""
    return "M" + "L".join(f"{fmt(x)} {fmt(y)}" for x, y in pts)


def tip(S, pts):
    """Small solid arrow head triangle."""
    return solid(poly(pts, closed=True))


# ============================================================================ chunk 1: astrology and alchemy

@icon("natal-chart", CAT, "Birth chart wheel: an outer ring with house dividers and aspect lines across the middle",
      tags=["astrology", "horoscope", "birth chart", "zodiac wheel", "houses", "natal", "star chart"])
def _(S):
    parts = [line(circle(12, 12, 9.5))]
    for k in range(6):
        a = 30 + 60 * k
        x1, y1 = polar(12, 12, 9.5, a)
        x2, y2 = polar(12, 12, 6, a)
        parts.append(line(seg(x1, y1, x2, y2)))
    parts.append(line(poly([polar(12, 12, 4.6, -90), polar(12, 12, 4.6, 30), polar(12, 12, 4.6, 150)], closed=True, r=S.r * 0.5)))
    return parts


@icon("mercury-symbol", CAT, "Planet Mercury glyph: a circle with a bowl of horns on top and a cross below",
      tags=["mercury", "astrology", "planet symbol", "astronomy", "alchemy", "quicksilver", "zodiac"])
def _(S):
    return [line(arc(12, 5.6, 3.2, 0, 180)), line(circle(12, 12.3, 3.6)),
            line(seg(12, 15.9, 12, 21.5)), line(seg(9, 18.8, 15, 18.8))]


@icon("earth-symbol", CAT, "Planet Earth glyph: a circle with a cross standing on its top",
      tags=["earth", "astrology", "planet symbol", "astronomy", "globe cross", "terra", "world"])
def _(S):
    return [line(circle(12, 14.5, 6)), line(seg(12, 8.5, 12, 2.5)), line(seg(9, 5.2, 15, 5.2))]


@icon("jupiter-symbol", CAT, "Planet Jupiter glyph: a numeral four with a curved left arm",
      tags=["jupiter", "astrology", "planet symbol", "astronomy", "zodiac", "gas giant", "thursday"])
def _(S):
    return [line("M5 7.5C5 4.4 7 3 9 3C11.6 3 13 5 13 7.6C13 11.4 9.4 14.4 4.5 15.6"),
            line(seg(4.5, 15.6, 20, 15.6)), line(seg(15.5, 7.5, 15.5, 21.5))]


@icon("saturn-symbol", CAT, "Planet Saturn glyph: a small cross with a hooked tail like a lowercase h",
      tags=["saturn", "astrology", "planet symbol", "astronomy", "zodiac", "ringed planet", "saturday"])
def _(S):
    return [line(seg(8.5, 2.8, 8.5, 12.5)), line(seg(5.5, 5.5, 11.5, 5.5)),
            line("M8.5 9.2C12.6 7.4 16.6 9.6 15.8 13.4C15.2 16.4 12.8 18.6 15.4 20.8C16.4 21.6 17.8 21.4 18.6 20.4")]


@icon("uranus-symbol", CAT, "Planet Uranus glyph: a ring with a dot at its centre and an arrow rising from the top",
      tags=["uranus", "astrology", "planet symbol", "astronomy", "zodiac", "ice giant", "modern ruler"])
def _(S):
    return [line(circle(12, 16, 5)), dot(12, 16, 1.4), line(seg(12, 11, 12, 3.5)),
            line(poly([(9, 6.5), (12, 3.3), (15, 6.5)], r=S.r * 0.4))]


@icon("neptune-symbol", CAT, "Planet Neptune glyph: a trident with three prongs above a crossbar on its handle",
      tags=["neptune", "astrology", "planet symbol", "astronomy", "zodiac", "trident", "sea god"])
def _(S):
    return [line("M5.5 4.5V8.5A6.5 6.5 0 0 0 18.5 8.5V4.5"), line(seg(12, 4, 12, 21.5)),
            line(seg(8.5, 18.2, 15.5, 18.2)),
            tip(S, [(3.4, 7), (5.5, 2.6), (7.6, 7)]), tip(S, [(9.9, 6.6), (12, 2.4), (14.1, 6.6)]),
            tip(S, [(16.4, 7), (18.5, 2.6), (20.6, 7)])]


@icon("pluto-symbol", CAT, "Planet Pluto glyph: a small circle sitting in a crescent cup above a cross",
      tags=["pluto", "astrology", "planet symbol", "astronomy", "zodiac", "dwarf planet", "underworld"])
def _(S):
    return [line(circle(12, 6.6, 2.4)), line(arc(12, 8, 6.5, 0, 180)),
            line(seg(12, 14.5, 12, 21.5)), line(seg(8.5, 18.2, 15.5, 18.2))]


@icon("ceres-symbol", CAT, "Dwarf planet Ceres glyph: a sickle hook standing on a short cross",
      tags=["ceres", "astrology", "dwarf planet", "astronomy", "sickle", "harvest", "asteroid"])
def _(S):
    return [line("M16.5 4.2C10 2.6 6.6 9 11 13.2"), line(seg(11, 12.5, 11, 21.5)), line(seg(7.5, 18, 14.5, 18))]


@icon("chiron-symbol", CAT, "Chiron glyph: a small circle under a vertical stroke topped with a K shape",
      tags=["chiron", "astrology", "wounded healer", "centaur", "asteroid", "symbol", "zodiac"])
def _(S):
    return [line(seg(9.5, 3, 9.5, 14.6)), line(poly([(15.5, 3), (9.5, 8.6), (15.8, 13.4)], r=S.r * 0.4)),
            line(circle(9.5, 18, 3.4))]


@icon("conjunction-aspect", CAT, "Conjunction aspect glyph: a small circle with a line rising diagonally from its upper right",
      tags=["conjunction", "astrology", "aspect", "zero degrees", "alignment", "planets together", "symbol"])
def _(S):
    return [line(circle(8.5, 15.5, 3.6)), line(seg(11.3, 12.7, 19, 5))]


@icon("opposition-aspect", CAT, "Opposition aspect glyph: two small circles joined by a diagonal line",
      tags=["opposition", "astrology", "aspect", "180 degrees", "planets opposite", "polarity", "symbol"])
def _(S):
    k = L(S, 2.0, 3.0)
    return [line(rect(3.6, 14.4, 6, 6, k)), line(rect(14.4, 3.6, 6, 6, k)), line(seg(8.9, 15.1, 15.1, 8.9))]


@icon("quincunx-aspect", CAT, "Quincunx aspect glyph: a Y shape standing on a short bar",
      tags=["quincunx", "astrology", "aspect", "150 degrees", "inconjunct", "symbol", "planets"])
def _(S):
    return [line(poly([(5.5, 3.5), (12, 11), (18.5, 3.5)], r=S.r * 0.4)), line(seg(12, 11, 12, 20)),
            line(seg(8, 20, 16, 20))]


@icon("lunar-node", CAT, "Lunar node glyph: a horseshoe arch with a small circle at each foot",
      tags=["lunar node", "north node", "astrology", "eclipse point", "dragon head", "symbol", "moon"])
def _(S):
    return [line("M6.5 14.8V11A5.5 5.5 0 0 1 17.5 11V14.8"), line(rect(4, 15.1, 5, 5, L(S, 1.2, 2.5))), line(rect(15, 15.1, 5, 5, L(S, 1.2, 2.5)))]


@icon("black-moon-lilith", CAT, "Black Moon Lilith glyph: a solid crescent above a small cross",
      tags=["lilith", "black moon", "astrology", "lunar apogee", "crescent", "symbol", "dark moon"])
def _(S):
    cres = minus(circle(12, 8.2, 5.6), circle(14.6, 6.6, 4.7))
    return [solid(cres), line(seg(11.5, 15.6, 11.5, 21.5)), line(seg(8, 18.4, 15, 18.4))]


# ============================================================================ chunk 2: alchemy and esoteric diagrams

def tri_pts(cx, cy, w, h, up=True):
    if up:
        return [(cx, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]
    return [(cx, cy + h / 2), (cx + w / 2, cy - h / 2), (cx - w / 2, cy - h / 2)]


@icon("classical-elements", CAT, "Four alchemical element triangles: fire up, water down, air up with a bar and earth down with a bar",
      tags=["four elements", "fire water air earth", "alchemy", "classical elements", "triangles", "esoteric", "occult"])
def _(S):
    parts = []
    for (cx, cy, up, bar) in [(6.6, 6.4, True, False), (17.4, 6.4, False, False), (6.6, 17.6, True, True), (17.4, 17.6, False, True)]:
        parts.append(shell(poly(tri_pts(cx, cy, 8, 7.4, up), closed=True, r=S.r * 0.4)))
        if bar:
            y = cy + 1.0 if up else cy - 1.0
            parts.append(detail(seg(cx - 2.2, y, cx + 2.2, y)))
    return parts


@icon("sulfur-alchemy", CAT, "Alchemical sulfur sign: an upward triangle standing on a cross",
      tags=["sulfur", "sulphur", "brimstone", "alchemy", "esoteric", "triangle cross", "occult"])
def _(S):
    return [shell(poly([(12, 2.8), (17.6, 11.4), (6.4, 11.4)], closed=True, r=S.r * 0.6)),
            line(seg(12, 11.4, 12, 21.5)), line(seg(8.5, 16.8, 15.5, 16.8))]


@icon("salt-alchemy", CAT, "Alchemical salt sign: a circle cut by one horizontal line",
      tags=["salt", "alchemy", "esoteric", "circle bar", "occult", "element sign", "crystal"])
def _(S):
    return [shell(circle(12, 12, 8)), detail(seg(*L(S, (4, 12, 20, 12), (3.2, 12, 20.8, 12))))]


@icon("philosophers-stone", CAT, "A circle with an inscribed triangle and a small circle at its centre, the squared circle diagram",
      tags=["philosophers stone", "alchemy", "squared circle", "esoteric", "magnum opus", "triangle in circle", "occult"])
def _(S):
    return [line(circle(12, 12, 9.5)),
            line(poly([polar(12, 12, 9.5, -90), polar(12, 12, 9.5, 30), polar(12, 12, 9.5, 150)], closed=True, r=S.r * 0.6)),
            dot(12, 13.2, 1.5)]


@icon("i-ching-hexagram", CAT, "Six stacked horizontal lines, some solid and some broken in the middle",
      tags=["i ching", "hexagram", "divination", "book of changes", "yin yang lines", "chinese", "oracle"])
def _(S):
    parts = []
    pattern = [True, False, True, True, False, False]
    for i, solid_ in enumerate(pattern):
        y = 3.5 + 3.4 * i
        if solid_:
            parts.append(line(seg(3.5, y, 20.5, y)))
        else:
            parts.append(line(seg(3.5, y, 10, y)))
            parts.append(line(seg(14, y, 20.5, y)))
    return parts


@icon("ogham-script", CAT, "A vertical stem with short strokes branching off both sides in groups",
      tags=["ogham", "celtic", "irish", "ancient alphabet", "tree alphabet", "runes", "old writing"])
def _(S):
    return [line(seg(12, 2.5, 12, 21.5)),
            line(seg(5.5, 5, 12, 5)), line(seg(5.5, 8.6, 12, 8.6)),
            line(seg(12, 11.8, 18.5, 11.8)), line(seg(12, 15.2, 18.5, 15.2)),
            line(seg(6.5, 19, 17.5, 19))]


@icon("pendulum-dowsing", CAT, "Pointed crystal weight hanging on a chain above a small swing arc",
      tags=["pendulum", "dowsing", "divination", "crystal pendulum", "scrying", "mystic", "fortune"])
def _(S):
    return [line(seg(12, 2.5, 12, 7.8)),
            shell(poly([(12, 7.8), (15.2, 11.6), (12, 18), (8.8, 11.6)], closed=True, r=S.r * 0.6)),
            detail(seg(9.3, 11.6, 14.7, 11.6)),
            line("M4.5 19C8 22.6 16 22.6 19.5 19")]


# ============================================================================ chunk 3: hazard warning triangles

@icon("high-voltage-hazard", CAT, "Warning triangle with a jagged lightning bolt striking downward",
      tags=["high voltage", "electric shock", "electrical hazard", "danger", "warning sign", "live wire", "safety"])
def _(S):
    bolt = poly([(13.6, 8.8), (9.2, 14.4), (11.9, 14.4), (10.6, 18.8), (15, 12.8), (12.3, 12.8)], closed=True)
    return warn(S, mark(bolt))


@icon("slippery-surface-hazard", CAT, "Warning triangle with a figure slipping backward, one leg kicked up, above a wavy floor",
      tags=["slippery floor", "wet floor", "slip hazard", "caution", "warning sign", "fall risk", "safety"])
def _(S):
    return warn(S,
        head(8.8, 10.6, 1.2),
        thin(S, tp((9.6, 12), (12.2, 14.6))),
        thin(S, tp((12.2, 14.6), (15, 12.4))),
        thin(S, tp((12.2, 14.6), (10.6, 16.4))),
        thin(S, "M6.4 18.3Q8.2 16.9 10 18.3T13.6 18.3T17.2 18.3"))


@icon("trip-hazard", CAT, "Warning triangle with a figure stumbling forward over a low block on the floor",
      tags=["trip hazard", "stumble", "obstacle", "uneven floor", "warning sign", "fall risk", "safety"])
def _(S):
    return warn(S,
        head(8.6, 10.8, 1.2),
        thin(S, tp((9.3, 12.2), (12.2, 14.4))),
        thin(S, tp((10.4, 12.8), (13.6, 12.6))),
        thin(S, tp((12.2, 14.4), (9.4, 17.6))),
        thin(S, tp((12.2, 14.4), (15, 15.4))),
        mark(rect(13.6, 16.6, 4.4, 2.4)))


@icon("fall-from-height-hazard", CAT, "Warning triangle with a figure tumbling headfirst off the edge of a raised step",
      tags=["fall from height", "falling person", "edge", "drop", "working at height", "warning sign", "safety"])
def _(S):
    return warn(S,
        mark(rect(7.4, 14.6, 4, 4.4)),
        head(15.2, 15.6, 1.25),
        thin(S, tp((14.4, 14), (11.8, 10.8))),
        thin(S, tp((13.2, 12.6), (15.6, 11.6))),
        thin(S, tp((11.8, 10.8), (10.4, 11.4))))


@icon("overhead-load-hazard", CAT, "Warning triangle with a crate hanging from a hook and cable above the ground",
      tags=["overhead load", "suspended load", "crane", "hoist", "lifting", "warning sign", "safety"])
def _(S):
    return warn(S,
        thin(S, tp((12, 8.2), (12, 12))),
        mark(rect(8.8, 12, 6.4, 4.6)),
        thin(S, tp((6.8, 18.4), (17.2, 18.4))))


@icon("falling-objects-hazard", CAT, "Warning triangle with a small box dropping onto a figure's head",
      tags=["falling objects", "head injury", "drop zone", "overhead danger", "construction", "warning sign", "safety"])
def _(S):
    return warn(S,
        mark(rect(10.2, 9, 3.6, 3.4)),
        head(12, 15.2, 1.4),
        thin(S, "M8.6 19.2Q12 15.8 15.4 19.2"))


@icon("forklift-traffic-hazard", CAT, "Warning triangle with a side view forklift truck and raised forks",
      tags=["forklift", "lift truck", "warehouse traffic", "vehicle", "warning sign", "pallet truck", "safety"])
def _(S):
    return warn(S,
        thin(S, tp((8, 11.8), (8, 17.4))),
        thin(S, tp((5.8, 17.4), (9.4, 17.4))),
        mark(rect(9.6, 13.8, 7.2, 3.2)),
        thin(S, tp((11.4, 13.8), (11.4, 11.2), (15, 11.2))),
        dot(11.8, 18, 1.1), dot(15, 18, 1.1))


@icon("explosive-atmosphere-hazard", CAT, "Warning triangle with the capital letters EX inside",
      tags=["ex", "explosive atmosphere", "atex", "explosion risk", "flammable gas", "warning sign", "safety"])
def _(S):
    return warn(S,
        thin(S, tp((10.4, 12.6), (8.2, 12.6), (8.2, 17.4), (10.4, 17.4)), 1.4),
        thin(S, tp((8.2, 15), (10, 15)), 1.4),
        thin(S, tp((11.8, 12.6), (15.8, 17.4)), 1.4),
        thin(S, tp((15.8, 12.6), (11.8, 17.4)), 1.4))


@icon("loud-noise-hazard", CAT, "Warning triangle with an ear and curved sound waves beside it",
      tags=["loud noise", "hearing protection", "noise hazard", "sound waves", "ear", "warning sign", "safety"])
def _(S):
    return warn(S,
        thin(S, "M8.2 18V13.6A2.8 2.8 0 0 1 13.8 13.6C13.8 15.4 12 15.6 12 17.6"),
        thin(S, "M15.2 12.4Q16.4 13.6 15.2 14.8"),
        thin(S, "M16.4 10.8Q18.6 13.6 16.4 16.4"))


@icon("automatic-start-hazard", CAT, "Warning triangle with a machine gear inside a circular arrow",
      tags=["automatic start", "machine restart", "moving parts", "gear", "warning sign", "remote start", "safety"])
def _(S):
    teeth = []
    pts = []
    for i in range(12):
        pts.append(polar(12, 14.8, 2.4 if i % 2 == 0 else 1.6, -90 + 30 * i))
    return warn(S,
        mark(poly(pts, closed=True)),
        thin(S, arc(12, 14.8, 4.4, -60, 210)),
        mark(poly([(6.6, 13.4), (9.8, 14.2), (8, 17)], closed=True)))


@icon("steam-hazard", CAT, "Warning triangle with three wavy steam lines rising from a pipe outlet",
      tags=["steam", "hot vapor", "scald", "pipe", "burn hazard", "warning sign", "safety"])
def _(S):
    return warn(S,
        thin(S, "M9.2 16.4Q8 15 9.2 13.6T9.2 10.8"),
        thin(S, "M12 16.4Q10.8 15 12 13.6T12 10.8"),
        thin(S, "M14.8 16.4Q13.6 15 14.8 13.6T14.8 10.8"),
        mark(rect(7.6, 17.4, 8.8, 1.6)))


@icon("hazard-stripes", CAT, "A band of bold diagonal stripes alternating solid and empty, like hazard marking tape",
      tags=["hazard tape", "warning stripes", "caution tape", "barrier", "diagonal stripes", "marking", "safety"])
def _(S):
    rr_ = L(S, 1.0, 2.0)
    band = rect(2.5, 6.5, 19, 11, rr_)
    inner = P(rect(3.5, 7.5, 17, 9, 0))
    stripes = [mark(path_to_d(U(*[D(Pp, Pp) for Pp in []]))) for _ in []]
    parts = [shell(band)]
    for k in range(-1, 4):
        x = 3.5 + 5.6 * k
        par = P(poly([(x + 9, 7.5), (x + 9 + 2.8, 7.5), (x + 2.8, 16.5), (x, 16.5)], closed=True))
        from geometry import I as _I
        parts.append(mark(path_to_d(_I(par, inner))))
    return parts


def rot_pts(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def gear_pts(cx, cy, ro, ri, n=8, rot=0.0):
    out = []
    for i in range(2 * n):
        out.append(polar(cx, cy, ro if i % 2 == 0 else ri, rot + i * 180 / n))
    return out


@icon("entanglement-hazard", CAT, "Warning triangle with a hand reaching toward two meshing gear wheels",
      tags=["entanglement", "gears", "drawn in", "moving machinery", "pinch point", "warning sign", "safety"])
def _(S):
    return warn(S,
        mark(rect(6.6, 12.8, 3, 3.4, 0.8)),
        thin(S, tp((9.6, 13.6), (11.6, 13.6))), thin(S, tp((9.6, 15.4), (11.6, 15.4))),
        mark(poly(gear_pts(14, 12.8, 2.4, 1.7, 8), closed=True)),
        mark(poly(gear_pts(14, 17.4, 2.4, 1.7, 8, 22.5), closed=True)))


@icon("head-obstacle-hazard", CAT, "Warning triangle with a head bumping into a low horizontal bar",
      tags=["head injury", "low headroom", "duck your head", "overhead bar", "obstacle", "warning sign", "safety"])
def _(S):
    return warn(S,
        mark(rect(7.8, 10.8, 8.4, 1.8)),
        mark(circle(12, 15.8, 2.1)),
        thin(S, "M8.4 19.2Q12 16.8 15.6 19.2"),
        thin(S, tp((12, 8.6), (12, 9.6))))


@icon("flying-debris-hazard", CAT, "Warning triangle with small fragments flying outward toward a face",
      tags=["flying debris", "eye protection", "projectiles", "chips", "grinding", "warning sign", "safety"])
def _(S):
    return warn(S,
        thin(S, circle(14.6, 14.4, 2.3)),
        thin(S, tp((7.2, 12.2), (10, 13.2))),
        thin(S, tp((6.6, 15.4), (10.8, 15.4))),
        thin(S, tp((7.6, 18.2), (10.6, 17))))


@icon("guard-dog-warning", CAT, "Warning triangle with the side view of a barking dog",
      tags=["guard dog", "beware of dog", "dog warning", "aggressive dog", "property", "warning sign", "pet"])
def _(S):
    return warn(S,
        mark(rect(7, 13.4, 7.4, 3.4, 1.4)),
        mark(circle(14.6, 12.6, 1.8)),
        mark(rect(15, 13, 2.4, 1.3, 0.6)),
        thin(S, tp((8.4, 16.4), (8.4, 18.6))), thin(S, tp((13, 16.4), (13, 18.6))),
        thin(S, tp((7, 14), (5.8, 12.4))))


@icon("confined-space-hazard", CAT, "Warning triangle with a figure crouching inside a narrow shaft opening",
      tags=["confined space", "manhole", "tank entry", "shaft", "permit required", "warning sign", "safety"])
def _(S):
    return warn(S,
        thin(S, tp((8.4, 11.2), (8.4, 18.6), (15.6, 18.6), (15.6, 11.2))),
        head(12, 13.6, 1.3),
        mark(ellipse(12, 16.6, 2.3, 1.5)))


@icon("thin-ice-hazard", CAT, "Warning triangle with a figure breaking through a cracked ice sheet",
      tags=["thin ice", "ice warning", "frozen lake", "falling through", "cracks", "warning sign", "winter"])
def _(S):
    return warn(S,
        head(12, 11, 1.25),
        thin(S, "M8 11.4L9.8 13.8L14.2 13.8L16 11.4"),
        thin(S, tp((6.2, 17.6), (9, 16.2), (10.6, 18.4), (12.8, 15.8), (14.6, 18), (17.8, 16.4))))


@icon("electric-fence-warning", CAT, "Warning triangle with two fence wires between posts and a lightning bolt above them",
      tags=["electric fence", "live wire", "livestock fence", "shock", "farm", "warning sign", "safety"])
def _(S):
    bolt = poly([(12.9, 8.8), (10.4, 12.4), (12.1, 12.4), (11.2, 14.6), (13.8, 11.2), (12.1, 11.2)], closed=True)
    return warn(S,
        mark(bolt),
        thin(S, tp((7.4, 14.6), (7.4, 18.6))), thin(S, tp((16.6, 14.6), (16.6, 18.6))),
        thin(S, "M7.4 15.2Q12 18.6 16.6 15.2"))


@icon("wet-paint-warning", CAT, "Warning triangle with a paintbrush and a paint drip falling from its tip",
      tags=["wet paint", "fresh paint", "paintbrush", "drip", "decorating", "warning sign", "caution"])
def _(S):
    return warn(S,
        thin(S, tp((16, 9.8), (13.4, 12.2)), 1.6),
        mark(poly([(14.2, 11.6), (11, 14.6), (9.6, 13.4), (12.4, 10.2)], closed=True)),
        mark(poly([(9.4, 14.4), (10.8, 15.2), (7.8, 17.4), (7.4, 16.6)], closed=True)),
        mark("M12.8 15.6C13.6 16.8 14.2 17.4 14.2 18.2A1.4 1.4 0 0 1 11.4 18.2C11.4 17.4 12 16.8 12.8 15.6Z"))


@icon("pressure-vessel-hazard", CAT, "Warning triangle with a rounded gas tank and a pressure gauge on top",
      tags=["pressure vessel", "gas cylinder", "compressed gas", "gauge", "tank", "warning sign", "safety"])
def _(S):
    return warn(S,
        mark(rect(5.8, 13.4, 12.4, 4.8, 2.4)),
        thin(S, circle(12, 10.8, 1.6), 1.4),
        thin(S, tp((12, 12.4), (12, 13.4)), 1.4),
        thin(S, tp((8.2, 18.2), (8.2, 19)), 1.4), thin(S, tp((15.8, 18.2), (15.8, 19)), 1.4))


@icon("carbon-monoxide-hazard", CAT, "Warning triangle with the letters CO above a wavy gas line",
      tags=["carbon monoxide", "co gas", "poison gas", "gas leak", "silent killer", "warning sign", "safety"])
def _(S):
    return warn(S,
        thin(S, arc(10, 13.8, 2, 40, 320), 1.4),
        thin(S, circle(14.6, 13.8, 2), 1.4),
        thin(S, "M6.8 18Q8.6 16.6 10.4 18T14 18T17.4 18"))


@icon("hot-liquid-hazard", CAT, "Warning triangle with a tilted cup pouring hot liquid drops below it",
      tags=["hot liquid", "scald", "spill", "hot drink", "burn hazard", "warning sign", "safety"])
def _(S):
    cup = rot_pts([(7.6, 10.6), (13, 10.6), (12.2, 15.6), (8.4, 15.6)], 50, 10.4, 13)
    handle = rot_pts([(13.2, 11.8), (15, 12.6), (14.4, 14.4)], 50, 10.4, 13)
    return warn(S,
        mark(poly(cup, closed=True)),
        thin(S, tp(*handle), 1.3),
        mark(circle(15.4, 15.4, 0.95)), mark(circle(13.4, 17.6, 0.95)), mark(circle(16.6, 18, 0.85)))


# ============================================================================ chunk 4: mandatory signs

def pill(x, y, w, h):
    return rect(x, y, w, h, min(w, h) / 2)


@icon("wear-hard-hat-sign", CAT, "Round mandatory sign with a head and shoulders wearing a hard hat",
      tags=["hard hat", "helmet required", "head protection", "ppe", "construction site", "mandatory sign", "safety"])
def _(S):
    return ring(S,
        mark("M7.6 11A4.4 4.4 0 0 1 16.4 11Z"),
        mark(rect(6.4, 11.2, 11.2, 1.6, 0.8)),
        mark(rect(11.2, 6.4, 1.6, 4.4)),
        thin(S, "M9.6 13.6V14.4A2.4 2.4 0 0 0 14.4 14.4V13.6"),
        thin(S, "M6.6 18.4Q7.4 16.2 10 15.8M17.4 18.4Q16.6 16.2 14 15.8", 1.6))


@icon("wear-ear-protection-sign", CAT, "Round mandatory sign with a head wearing ear defenders joined by a headband",
      tags=["ear defenders", "hearing protection", "earmuffs", "noise", "ppe", "mandatory sign", "safety"])
def _(S):
    return ring(S,
        thin(S, arc(12, 12.8, 5.2, 180, 360), 1.6),
        mark(rect(5.8, 11.4, 2.8, 5.4, L(S, 0.6, 1.4))), mark(rect(15.4, 11.4, 2.8, 5.4, L(S, 0.6, 1.4))),
        thin(S, circle(12, 13.4, 3.2), 1.5))


@icon("wear-gloves-sign", CAT, "Round mandatory sign with a gloved hand showing fingers and a cuff",
      tags=["gloves", "hand protection", "work gloves", "ppe", "mandatory sign", "safety", "glove required"])
def _(S):
    return ring(S,
        mark(rect(8.4, 8.2, 1.6, 5, 0.8)), mark(rect(10.4, 7, 1.6, 6.2, 0.8)),
        mark(rect(12.4, 7.4, 1.6, 5.8, 0.8)), mark(rect(14.4, 8.6, 1.6, 4.6, 0.8)),
        mark(rect(8.4, 11.8, 7.6, 4.2, 1.4)),
        thin(S, tp((8.6, 14.4), (6.8, 12.4)), 1.7),
        mark(rect(8.2, 17, 8.2, 2)))


@icon("wear-safety-boots-sign", CAT, "Round mandatory sign with a pair of ankle safety boots on thick soles",
      tags=["safety boots", "steel toe", "foot protection", "work boots", "ppe", "mandatory sign", "safety shoes"])
def _(S):
    return ring(S,
        mark(poly([(5.6, 7), (8.4, 7), (8.4, 11.2), (11.6, 12.4), (11.6, 14.6), (5.6, 14.6)], closed=True, r=L(S, 0, 1.0))),
        mark(rect(5.6, 15.6, 6, 1.6)),
        mark(poly([(12.6, 7), (15.4, 7), (15.4, 11.2), (18.4, 12.4), (18.4, 14.6), (12.6, 14.6)], closed=True, r=L(S, 0, 1.0))),
        mark(rect(12.6, 15.6, 5.8, 1.6)))


@icon("wear-face-shield-sign", CAT, "Round mandatory sign with a head behind a full clear visor",
      tags=["face shield", "visor", "face protection", "grinding", "ppe", "mandatory sign", "safety"])
def _(S):
    return ring(S,
        mark(rect(7, 5.8, 10, 1.8, L(S, 0.3, 0.9))),
        mark(path_to_d(ST(poly([(7.8, 7.6), (7.8, 14.6), (16.2, 14.6), (16.2, 7.6)], r=L(S, 0, 1.6)), 1.5, S.cap, S.join))),
        thin(S, circle(12, 11.2, 2.5), 1.5),
        thin(S, "M6.8 19Q7.4 16.8 12 16.6Q16.6 16.8 17.2 19", 1.6))


@icon("wear-respirator-sign", CAT, "Round mandatory sign with a head wearing a half mask with two filter cartridges",
      tags=["respirator", "half mask", "dust mask", "breathing protection", "ppe", "mandatory sign", "safety"])
def _(S):
    return ring(S,
        thin(S, circle(12, 10.6, 4.4), 1.5),
        mark(poly([(8.8, 11.8), (15.2, 11.8), (13.8, 15.6), (10.2, 15.6)], closed=True, r=L(S, 0, 1.0))),
        mark(rect(6.2, 12, 3.2, 3.4, L(S, 0.6, 1.6))), mark(rect(14.6, 12, 3.2, 3.4, L(S, 0.6, 1.6))),
        thin(S, "M7 19Q7.6 17.4 12 17.2Q16.4 17.4 17 19", 1.6))


@icon("wear-safety-harness-sign", CAT, "Round mandatory sign with a figure in a harness clipped to a lanyard above",
      tags=["safety harness", "fall arrest", "lanyard", "work at height", "ppe", "mandatory sign", "safety"])
def _(S):
    return ring(S,
        head(11, 7.6, 1.5),
        thin(S, tp((11, 9.6), (11, 14.4))),
        thin(S, tp((8, 12.4), (11, 10.8), (14, 12.4))),
        thin(S, tp((9.4, 10.8), (12.6, 14.2))), thin(S, tp((12.6, 10.8), (9.4, 14.2))),
        thin(S, tp((11, 14.4), (8.6, 18.4))), thin(S, tp((11, 14.4), (13.4, 18.4))),
        thin(S, tp((13.6, 10.6), (16.2, 9.2), (16.2, 5.2))))


@icon("wear-hi-vis-vest-sign", CAT, "Round mandatory sign with a sleeveless vest crossed by reflective bands",
      tags=["hi vis", "high visibility vest", "reflective", "safety vest", "ppe", "mandatory sign", "visibility"])
def _(S):
    return ring(S,
        thin(S, tp((8.6, 5.8), (10.6, 5.8), (12, 8.8), (13.4, 5.8), (15.4, 5.8), (16.4, 18), (7.6, 18), (8.6, 5.8)), 1.5),
        mark(rect(8, 11.2, 8.2, 1.5)), mark(rect(7.9, 14.6, 8.4, 1.5)))


@icon("wash-hands-sign", CAT, "Round mandatory sign with two cupped hands under a falling water drop",
      tags=["wash hands", "hand washing", "hygiene", "clean hands", "mandatory sign", "sanitation", "water"])
def _(S):
    return ring(S,
        mark("M12 4.6C13.6 6.8 14.4 7.8 14.4 9A2.4 2.4 0 0 1 9.6 9C9.6 7.8 10.4 6.8 12 4.6Z"),
        thin(S, "M5.8 12.4Q6.6 18.2 12 18.2Q17.4 18.2 18.2 12.4", 1.7),
        thin(S, tp((8.6, 13.4), (8.6, 15.4))), thin(S, tp((15.4, 13.4), (15.4, 15.4))))


@icon("read-manual-sign", CAT, "Round mandatory sign with an open book and a small letter i above it",
      tags=["read the manual", "instructions", "read before use", "information", "mandatory sign", "guidance", "safety"])
def _(S):
    return ring(S,
        dot(12, 5.8, 1.15), thin(S, tp((12, 8), (12, 9.6))),
        thin(S, tp((12, 12), (5.8, 11), (5.8, 18), (12, 19), (12, 12)), 1.5),
        thin(S, tp((12, 12), (18.2, 11), (18.2, 18), (12, 19)), 1.5))


@icon("use-handrail-sign", CAT, "Round mandatory sign with a hand gripping a sloping rail above steps",
      tags=["handrail", "hold the rail", "stairs", "use the railing", "mandatory sign", "safety", "steps"])
def _(S):
    hand = rot_pts([(9.8, 7.8), (14.2, 7.8), (14.2, 10.6), (9.8, 10.6)], -24, 12, 9.2)
    return ring(S,
        thin(S, tp((5.4, 12.4), (18.6, 6.2)), 1.5),
        mark(poly(hand, closed=True, r=0.6)),
        thin(S, tp((5.8, 18.4), (9, 18.4), (9, 16), (12.2, 16), (12.2, 13.6), (15.4, 13.6), (15.4, 11.4), (18.4, 11.4)), 1.5))


@icon("disconnect-power-sign", CAT, "Round mandatory sign with a plug pulled away from a wall socket",
      tags=["unplug", "disconnect power", "isolate", "switch off", "mandatory sign", "electrical safety", "lockout"])
def _(S):
    return ring(S,
        thin(S, tp((8.6, 8.4), (5, 8.4), (5, 15.6), (8.6, 15.6)), 1.6),
        dot(6.9, 11, 0.9), dot(6.9, 13, 0.9),
        mark(rect(13, 9.4, 4.2, 5.2, 1.2)),
        thin(S, tp((9.4, 11), (13, 11))), thin(S, tp((9.4, 13), (13, 13))),
        thin(S, tp((17, 12), (20, 12))))


@icon("wear-life-jacket-sign", CAT, "Round mandatory sign with a figure wearing a buoyant life vest with straps",
      tags=["life jacket", "life vest", "flotation", "buoyancy aid", "mandatory sign", "water safety", "ppe"])
def _(S):
    return ring(S,
        head(12, 5.8, 1.6),
        mark(path_to_d(ST(poly([(8.2, 9), (10.4, 8.2), (12, 9.4), (13.6, 8.2), (15.8, 9), (16.8, 17.6), (7.2, 17.6)], closed=True, r=L(S, 0, 1.2)), 1.5, S.cap, S.join))),
        thin(S, tp((12, 9.8), (12, 17.6)), 1.5),
        mark(rect(7.4, 13.2, 9.2, 1.4)))


@icon("wear-protective-clothing-sign", CAT, "Round mandatory sign with a long sleeved coverall suit split by a zip",
      tags=["coverall", "protective clothing", "overalls", "boiler suit", "hazmat", "mandatory sign", "ppe"])
def _(S):
    left = poly([(9.4, 5.4), (11.6, 5.4), (11.6, 18.8), (9, 18.8), (8.8, 14), (6.4, 14.8), (5.2, 8.4)], closed=True, r=L(S, 0, 0.8))
    right = poly([(14.6, 5.4), (12.4, 5.4), (12.4, 18.8), (15, 18.8), (15.2, 14), (17.6, 14.8), (18.8, 8.4)], closed=True, r=L(S, 0, 0.8))
    return ring(S, mark(left), mark(right))


@icon("wear-welding-mask-sign", CAT, "Round mandatory sign with a head behind a welding helmet with a narrow dark window",
      tags=["welding mask", "welding helmet", "arc eye", "face protection", "mandatory sign", "ppe", "welder"])
def _(S):
    helmet = minus(rect(6.8, 5.6, 10.4, 12.4, L(S, 3.0, 4.2)), rect(8.4, 9.6, 7.2, 3, L(S, 0.3, 1.2)))
    return ring(S, mark(helmet))


@icon("keep-door-closed-sign", CAT, "Round mandatory sign with a door in its frame and a small arrow pushing it shut",
      tags=["keep closed", "close the door", "fire door", "door must be shut", "mandatory sign", "safety", "door"])
def _(S):
    return ring(S,
        thin(S, tp((6.6, 18.6), (6.6, 5.4), (13.4, 5.4), (13.4, 18.6)), 1.6),
        mark(rect(8, 6.8, 4, 11.8)),
        thin(S, tp((19.2, 12), (15.6, 12)), 1.6),
        thin(S, tp((17.2, 10), (15.2, 12), (17.2, 14)), 1.6))


# ============================================================================ chunk 5: emergency equipment and handling marks

def flame(cx, cy, s=1.0):
    """Small solid flame (bottom centre at cx, cy)."""
    pts = [(0, 0), (-2.2, -0.4), (-2.6, -2.6), (-1.2, -4.2), (-1.0, -3.0), (0.2, -5.4), (0.4, -3.8), (1.6, -4.6), (2.6, -2.4), (2.2, -0.4)]
    return poly([(cx + x * s, cy + y * s) for x, y in pts], closed=True)


@icon("refuge-point", CAT, "Square sign with a wheelchair user inside corner marks of a small safe zone",
      tags=["refuge point", "area of rescue", "evacuation assistance", "wheelchair", "accessible", "safe zone", "emergency"])
def _(S):
    return [
            shell(rect(2.5, 2.5, 19, 19, L(S, 2, 4))),
            head(10.6, 7.6, 1.4),
            thin(S, tp((10.6, 9.6), (10.6, 13.2), (14, 13.2), (15.2, 16.4)), 1.6),
            thin(S, arc(10.4, 14.8, 3, 40, 320), 1.5)]


@icon("fire-ladder-sign", CAT, "Square sign with a ladder leaning upward and a small flame at its foot",
      tags=["fire ladder", "fire escape ladder", "emergency ladder", "escape route", "fire safety", "evacuation", "sign"])
def _(S):
    return [
            shell(rect(2.5, 2.5, 19, 19, L(S, 2, 4))),
            thin(S, tp((7.2, 17.6), (11.2, 6.4)), 1.5), thin(S, tp((10.8, 18.8), (14.8, 7.6)), 1.5),
            thin(S, tp((8.6, 13.6), (12.6, 14.8)), 1.3), thin(S, tp((9.8, 10.2), (13.8, 11.4)), 1.3),
            mark(flame(17.4, 18.2, 0.85))]


@icon("fire-telephone-sign", CAT, "Square sign with a telephone handset beside a small flame",
      tags=["fire telephone", "emergency phone", "fire alarm call point", "fire safety", "call fire brigade", "sign", "handset"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, L(S, 2, 4))),
            mark(rect(6, 6.6, 3.4, 3, L(S, 0.6, 1.3))), mark(rect(10.8, 14.4, 3, 3.4, L(S, 0.6, 1.3))),
            thin(S, "M7.7 9.6Q7.7 16 11.6 16", 1.9),
            mark(flame(16.8, 12.6, 0.95))]


@icon("smoke-hood", CAT, "Head covered by a clear escape hood bag with a filter at the mouth and a neck seal",
      tags=["smoke hood", "escape hood", "fire escape", "respirator hood", "emergency breathing", "evacuation", "safety"])
def _(S):
    return [shell(rect(6, 3.5, 12, 14, L(S, 5, 6))),
            detail(seg(6.6, 15.2, 17.4, 15.2)),
            head(12, 8.2, 2.0),
            mark(circle(12, 12.4, 1.3)),
            shell(rect(8, 19, 8, 2.5, L(S, 0.8, 1.2)))]


@icon("stacking-limit", CAT, "Three stacked boxes beside a measuring line with a bar marking the maximum stack height",
      tags=["stacking limit", "max stack", "do not stack higher", "cargo marking", "packaging symbol", "handling mark", "warehouse"])
def _(S):
    return [shell(rect(3.5, 16.6, 9, 3.4, L(S, 0.6, 1.2))), shell(rect(3.5, 10.8, 9, 3.4, L(S, 0.6, 1.2))),
            shell(rect(3.5, 5, 9, 3.4, L(S, 0.6, 1.2))),
            line(seg(17.5, 4, 17.5, 20.5)), line(seg(14.6, 4, 20.4, 4))]


@icon("sling-here", CAT, "Short length of chain links hanging in a U shape, marking where to attach a sling",
      tags=["sling here", "lifting point", "chain sling", "rigging", "cargo marking", "handling mark", "crane"])
def _(S):
    parts = []
    n = 7
    for i in range(n):
        ang = 180 - 180 * i / (n - 1)
        a = math.radians(ang)
        cx, cy = 12 + 8.2 * math.cos(a), 7 + 10.5 * math.sin(math.radians(180 - ang))
        # tangent direction of the U curve
        tx, ty = -8.2 * math.sin(a), -10.5 * math.cos(math.radians(180 - ang)) * -1
        rot = math.degrees(math.atan2(-10.5 * math.cos(math.radians(180 - ang)) * (-math.pi / (n - 1)) * 0 + ty, tx))
        rx, ry = (2.5, 1.3) if i % 2 == 0 else (1.4, 1.4)
        pts = [(cx + rx * math.cos(t) * math.cos(math.radians(rot)) - ry * math.sin(t) * math.sin(math.radians(rot)),
                cy + rx * math.cos(t) * math.sin(math.radians(rot)) + ry * math.sin(t) * math.cos(math.radians(rot)))
               for t in [k * math.pi / 8 for k in range(16)]]
        parts.append(line(poly(pts, closed=True)))
    return parts


@icon("clamp-here", CAT, "A box squeezed between two arrows pressing on its sides, the clamp here handling mark",
      tags=["clamp here", "clamp", "squeeze", "forklift clamp", "cargo marking", "handling mark", "press"])
def _(S):
    return [shell(rect(8.6, 6, 6.8, 12, L(S, 1.2, 2.4))),
            line(seg(2.2, 12, 6.4, 12)), line(poly([(4.4, 9.8), (6.6, 12), (4.4, 14.2)], r=S.r * 0.4)),
            line(seg(21.8, 12, 17.6, 12)), line(poly([(19.6, 9.8), (17.4, 12), (19.6, 14.2)], r=S.r * 0.4))]


@icon("temperature-limit-symbol", CAT, "Thermometer with two short bars beside it marking the upper and lower temperature limits",
      tags=["temperature limit", "storage temperature", "keep cool", "keep warm", "packaging symbol", "handling mark", "thermometer"])
def _(S):
    body = union(rect(7.2, 2.8, 4.4, 13, L(S, 1.6, 2.2)), circle(9.4, 17.4, 3.6))
    return [shell(body), dot(9.4, 17.4, 1.5),
            line(seg(14.2, 6.4, 21, 6.4)), line(seg(14.2, 14, 21, 14))]
