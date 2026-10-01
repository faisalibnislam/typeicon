"""TypeIcon Core: culture and belief.

Religious and cultural symbols drawn respectfully and in their conventional form and orientation.
This category takes no variant badges, so the symbols may use the whole live area.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, polar

CAT = "culture"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def fillets(regions, f=1.25):
    """Concave fillets (radius f) where strokes meet: morphological closing minus the original shape.
    Used by Rounded designs whose strokes butt into a ring, so the junctions are softened like
    the polyline fillets elsewhere in the Rounded style."""
    region = U(*regions)
    grown = U(region, ST(path_to_d(region), 2 * f, "round", "round"))
    closed = D(grown, ST(path_to_d(grown), 2 * f, "round", "round"))
    core = D(region, ST(path_to_d(region), 0.5, "round", "round"))  # overlap the strokes slightly: no seams
    return path_to_d(D(closed, core))


def star5(cx, cy, ro, ri=None, rot=-90.0):
    ri = ro * 0.42 if ri is None else ri
    pts = []
    for i in range(5):
        pts.append(polar(cx, cy, ro, rot + 72 * i))
        pts.append(polar(cx, cy, ri, rot + 36 + 72 * i))
    return poly(pts, closed=True)


# ============================================================================ symbols of harmony

_YY_S = "M12 3A4.5 4.5 0 0 0 12 12A4.5 4.5 0 0 1 12 21"


def _yin_yang_filled():
    ring = ST(circle(12, 12, 9), 2)
    half = P("M12 4A8 8 0 0 1 12 20Z")
    dark = D(U(half, P(circle(12, 8, 4))), P(circle(12, 16, 4)), P(circle(12, 8, 1.5)))
    return U(ring, dark, P(circle(12, 16, 1.5)))


@icon("yin-yang", CAT, "Yin and yang: a circle divided by an S-curve into two halves, each with a dot",
      tags=["taoism", "tao", "balance", "harmony", "duality", "chinese"], aliases=["taijitu"], filled=_yin_yang_filled)
def _(S):
    if S.name == "line":
        s_curve = line(_YY_S)
    else:  # Rounded: the dividing curve ends in round terminals just inside the ring
        s_curve = line("M11.1 4.9A4.5 4.5 0 0 0 12 12A4.5 4.5 0 0 1 12.9 19.1")
    return [shell(circle(12, 12, 9)), s_curve, dot(12, 7.5, 1.5), dot(12, 16.5, 1.5)]


@icon("peace-sign", CAT, "Peace symbol: a circle with a vertical line and two lower diagonals",
      tags=["peace", "cnd", "anti-war", "hippie", "pacifism", "harmony"], aliases=["peace-symbol"])
def _(S):
    ll, lr = polar(12, 12, 9, 135), polar(12, 12, 9, 45)
    parts = [
        shell(circle(12, 12, 9)),
        detail(seg(12, 3, 12, 21)),
        detail(poly([ll, (12, 12), lr], r=L(S, 0, 3))),
    ]
    if S.name == "rounded":
        strokes = [ST(circle(12, 12, 9), 2, "round", "round"), ST(seg(12, 3, 12, 21), 2, "round", "round"),
                   ST(poly([ll, (12, 12), lr], r=3), 2, "round", "round")]
        parts.append(solid(fillets(strokes, 1.0)))
    return parts


@icon("hamsa", CAT, "Hamsa: an open hand with symmetrical thumbs and an eye in the palm",
      tags=["hand of fatima", "khamsa", "amulet", "protection", "evil eye", "luck"], aliases=["hand-of-fatima", "khamsa"])
def _(S):
    tip = L(S, 1.2, 1.8)
    w = 3.6
    xs = [6.6, 6.6 + w, 6.6 + 2 * w, 6.6 + 3 * w]
    tops = [4, 2.5, 4]
    fingers = [rect(xs[i], tops[i], w, 10, tip) for i in range(3)]
    palm = "M6.6 11H17.4V15.5C17.4 18.8 15 21.2 12 21.2C9 21.2 6.6 18.8 6.6 15.5Z"
    thumb_l = "M7 18.5C4.4 17.8 3 15.6 3 12.3C3 11.2 4.2 10.9 4.8 11.8C5.4 12.9 6.1 13.6 7 13.8Z"
    thumb_r = "M17 18.5C19.6 17.8 21 15.6 21 12.3C21 11.2 19.8 10.9 19.2 11.8C18.6 12.9 17.9 13.6 17 13.8Z"
    body = union(palm, thumb_l, thumb_r, *fingers)
    return [
        shell(body),
        detail(seg(xs[1], 5.2, xs[1], 11.5)), detail(seg(xs[2], 5.2, xs[2], 11.5)),
        detail("M6.6 14.2C6.9 15.6 7.2 16.6 7.8 17.6"), detail("M17.4 14.2C17.1 15.6 16.8 16.6 16.2 17.6"),
        detail("M8.8 16.2Q12 13.2 15.2 16.2Q12 19.2 8.8 16.2Z" if S.name == "line" else
               "M9.1 16.6Q8.8 16.2 9.1 15.8Q12 13.2 14.9 15.8Q15.2 16.2 14.9 16.6Q12 19.2 9.1 16.6Z"),
        dot(12, 16.2, 1),
    ]


# ============================================================================ religious symbols

@icon("cross-christian", CAT, "Latin cross; the Christian cross",
      tags=["christian", "christianity", "church", "faith", "religion", "crucifix"], aliases=["latin-cross"])
def _(S):
    pts = [(10, 3), (14, 3), (14, 7.5), (18.5, 7.5), (18.5, 11.5), (14, 11.5), (14, 21), (10, 21),
           (10, 11.5), (5.5, 11.5), (5.5, 7.5), (10, 7.5)]
    return [shell(poly(pts, closed=True, r=S.r * 0.5))]


@icon("star-of-david", CAT, "Star of David: two interlaced equilateral triangles",
      tags=["magen david", "jewish", "judaism", "hexagram", "israel", "religion"], aliases=["magen-david"])
def _(S):
    up = regular(12, 12, 8, 3, -90)
    down = regular(12, 12, 8, 3, 90)
    return [shell(poly(up, closed=True, r=S.r * 0.4)), shell(poly(down, closed=True, r=S.r * 0.4))]


_CRESCENT = minus(circle(11, 12, 8), circle(14.2, 10.6, 6.6))


@icon("crescent-star", CAT, "Crescent moon with a five-pointed star",
      tags=["islam", "muslim", "hilal", "crescent", "star and crescent", "religion"], aliases=["star-and-crescent"])
def _(S):
    return [
        shell(_CRESCENT, stroke_miterlimit="2"),
        Part("dot", star5(17.2, 10.8, 3, 1.3, -90 + 18 * 0)),
    ]


@icon("om", CAT, "Om (Aum), the sacred syllable of Hinduism, Buddhism and Jainism",
      tags=["aum", "hindu", "hinduism", "mantra", "yoga", "meditation"], aliases=["aum"])
def _(S):
    return [
        line("M4 5.8C5.6 4.3 9 4.3 9 7C9 8.9 7.4 10.1 5.5 10.1"),
        line("M5.5 10.1C9 10.1 11 12.4 11 15.2C11 18.6 8.6 20.5 6.1 20.5C4.9 20.5 3.8 20 3 19.2"),
        line("M8.6 10.8C11.3 10.3 14 10.2 16 11.6C18.8 13.6 19 17.4 16.6 19.8C16 20.4 15.2 20.8 14.3 20.9"),
        line("M12.5 5C13.8 7.3 17.2 7.3 18.5 5"),
        dot(15.5, 3.1, 1.2),
    ]


@icon("dharma-wheel", CAT, "Dharma wheel (dharmachakra): an eight-spoked wheel with a hub",
      tags=["dharmachakra", "buddhism", "buddhist", "wheel of dharma", "eightfold path", "religion"],
      aliases=["dharmachakra", "wheel-of-dharma"])
def _(S):
    parts = [line(circle(12, 12, 6.5)), shell(circle(12, 12, 1.75))]
    for k in range(8):
        a = -90 + 45 * k
        parts.append(line(seg(*polar(12, 12, 2.75, a), *polar(12, 12, 6.5, a))))
        parts.append(line(seg(*polar(12, 12, 6.5, a), *polar(12, 12, L(S, 9.5, 8.75), a))))
    return parts


@icon("khanda", CAT, "Khanda: a double-edged sword through a chakkar, flanked by two kirpans crossed below",
      tags=["sikh", "sikhism", "khalsa", "sword", "chakkar", "religion"], aliases=["sikh-khanda"])
def _(S):
    blade = poly([(12, 2), (13.4, 4.2), (13.4, 15), (10.6, 15), (10.6, 4.2)], closed=True, r=S.r * 0.3)
    return [
        line(circle(12, 10.5, 4.6)),
        shell(blade),
        line(seg(9.5, 16.25, 14.5, 16.25)),
        line(seg(12, 16.25, 12, 18)),
        line("M5.5 2.5C2.6 6.8 2.8 12.3 6.2 15.6L16.5 21"),
        line("M18.5 2.5C21.4 6.8 21.2 12.3 17.8 15.6L7.5 21"),
    ]


@icon("torii", CAT, "Torii gate: two pillars under a curved lintel and a crossbeam",
      tags=["shinto", "shrine gate", "japan", "japanese", "gate", "religion"], aliases=["torii-gate"])
def _(S):
    top = ("M3 3.2C8 4.6 16 4.6 21 3.2L20.6 6.3C15.8 7.4 8.2 7.4 3.4 6.3Z" if S.name == "line" else
           "M4 3.5C8.6 4.7 15.4 4.7 20 3.5C20.7 3.3 21.1 3.6 21 4.3L20.8 5.6C20.7 6 20.4 6.3 20 6.4C15.4 7.4 8.6 7.4 4 6.4C3.6 6.3 3.3 6 3.2 5.6L3 4.3C2.9 3.6 3.3 3.3 4 3.5Z")
    return [
        shell(top),
        line(seg(3.5, 11, 20.5, 11)),
        line(seg(12, 7.3, 12, 11)),
        line(seg(7, 7.2, 6.5, 21)), line(seg(17, 7.2, 17.5, 21)),
    ]


@icon("prayer-beads", CAT, "Loop of prayer beads with a larger bead and a tassel",
      tags=["mala", "rosary", "misbaha", "tasbih", "meditation", "prayer"], aliases=["mala", "rosary"])
def _(S):
    parts = []
    for k in range(12):
        if k == 6:
            continue
        x, y = polar(12, 8.5, 6, -90 + 30 * k)
        parts.append(dot(x, y, 1.4))
    parts += [
        dot(12, 15.6, 1.7),
        line(seg(12, 17, 12, 18.5)),
        shell(poly([(10.5, 18.5), (13.5, 18.5), (15, 21.5), (9, 21.5)], closed=True, r=S.r * 0.5)),
    ]
    return parts
