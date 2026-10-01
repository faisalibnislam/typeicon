"""TypeIcon Core: shapes.

Geometric primitives. Line keeps every corner sharp (miter joins); Rounded rounds the corners. Shapes made only
of curves (circle, oval) mark their centre with a square point in Line and a round point in Rounded, like
`circle-math`. Shapes carry no variant badges.
"""
from __future__ import annotations

import math

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path

from dsl import (  # noqa: F401
    D, I, LINE, P, Part, ST, U, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    pt_on, rect, regular, rotation, seg, shell, solid,
)

CAT = "shapes"


# --------------------------------------------------------------------------- helpers

def rnd(S, line_val, rounded_val):
    return line_val if S.name == "line" else rounded_val


def xd(d: str, m) -> str:
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def centre(S, x=12.0, y=12.0, s=2.75):
    """Centre point: square in Line, round in Rounded."""
    if S.name == "line":
        return solid(rect(x - s / 2, y - s / 2, s, s))
    return dot(x, y, s / 2 + 0.15)


def soften(region, r):
    """Round the convex corners of a boolean region by radius r (morphological opening)."""
    er = D(region, ST(path_to_d(region), 2 * r, "butt", "round"))
    return U(er, ST(path_to_d(er), 2 * r, "butt", "round"))


def closed(S, pts, k=2.5):
    return shell(poly(pts, closed=True, r=rnd(S, 0, k)))


def star(cx, cy, r_out, r_in, n, start=-90.0):
    pts = []
    for i in range(2 * n):
        pts.append(pt_on(cx, cy, r_out if i % 2 == 0 else r_in, start + i * 180 / n))
    return pts


# ============================================================================ flat shapes

@icon("circle", CAT, "Circle shape", tags=["round", "ring", "dot", "geometry", "shape"])
def _(S):
    return [shell(circle(12, 12, 9)), centre(S)]


@icon("square", CAT, "Square shape", tags=["box", "quadrilateral", "block", "geometry", "shape"])
def _(S):
    return [shell(rect(3.5, 3.5, 17, 17, rnd(S, 0, 3.5)))]


@icon("triangle", CAT, "Equilateral triangle shape", tags=["three sides", "delta", "pyramid", "geometry", "shape"])
def _(S):
    return [closed(S, [(12, 4), (20.5, 19), (3.5, 19)], 2)]


@icon("diamond-shape", CAT, "Diamond: a square standing on one corner", tags=["diamond", "lozenge", "rhombus", "suit", "geometry", "shape"])
def _(S):
    return [closed(S, [(12, 3.5), (19.5, 12), (12, 20.5), (4.5, 12)], 2)]


@icon("hexagon", CAT, "Regular hexagon shape", tags=["six sides", "honeycomb", "polygon", "geometry", "shape"])
def _(S):
    return [closed(S, regular(12, 12, 9.25, 6), 2.5)]


@icon("octagon", CAT, "Regular octagon shape", tags=["eight sides", "stop sign", "polygon", "geometry", "shape"])
def _(S):
    return [closed(S, regular(12, 12, 9.5, 8, -112.5), 2.5)]


@icon("pentagon", CAT, "Regular pentagon shape", tags=["five sides", "polygon", "geometry", "shape"])
def _(S):
    return [closed(S, regular(12, 12.75, 9.25, 5), 2.5)]


@icon("oval", CAT, "Oval (ellipse) shape", tags=["ellipse", "egg", "round", "geometry", "shape"], aliases=["ellipse"])
def _(S):
    return [shell(ellipse(12, 12, 9.5, 6.5)), centre(S)]


@icon("rectangle", CAT, "Rectangle shape", tags=["oblong", "box", "quadrilateral", "geometry", "shape"])
def _(S):
    return [shell(rect(2.5, 6, 19, 12, rnd(S, 0, 3)))]


@icon("rhombus", CAT, "Rhombus: four equal sides leaning to one side", tags=["rhomb", "diamond", "equilateral", "quadrilateral", "geometry", "shape"])
def _(S):
    return [closed(S, [(7.25, 9.25), (7.25, 20.25), (16.78, 14.75), (16.78, 3.75)], 1.75)]


@icon("parallelogram", CAT, "Parallelogram: a slanted rectangle", tags=["slanted", "skewed", "quadrilateral", "geometry", "shape"])
def _(S):
    return [closed(S, [(2.5, 16.5), (16.5, 16.5), (21.5, 7.5), (7.5, 7.5)], 1.75)]


@icon("trapezoid", CAT, "Trapezoid: a four-sided shape with one pair of parallel sides",
      tags=["trapezium", "quadrilateral", "geometry", "shape"], aliases=["trapezium"])
def _(S):
    return [closed(S, [(3, 18.5), (21, 18.5), (16.5, 5.5), (7.5, 5.5)], 2)]


def _crescent():
    return "M17.16 4.63A9 9 0 1 0 17.16 19.37A7.41 7.41 0 0 1 17.16 4.63Z"


@icon("crescent", CAT, "Crescent shape with points facing right", tags=["crescent", "moon", "half moon", "arc", "geometry", "shape"])
def _(S):
    if S.name == "line":
        return [shell(_crescent())]
    return [shell(path_to_d(soften(P(_crescent()), 1.25)))]


def _plus_pts(h, reach):
    a, b = 12 - h, 12 + h
    lo, hi = 12 - reach, 12 + reach
    return [(a, lo), (b, lo), (b, a), (hi, a), (hi, b), (b, b), (b, hi), (a, hi), (a, b), (lo, b), (lo, a), (a, a)]


@icon("cross", CAT, "Diagonal cross (X) shape", tags=["x", "saltire", "multiply", "cross", "geometry", "shape"], aliases=["x-shape"])
def _(S):
    return [shell(xd(poly(_plus_pts(2.75, 9.25), closed=True, r=rnd(S, 0, 1.25)), rotation(45)))]


@icon("plus-shape", CAT, "Plus shape: a cross with four equal arms", tags=["plus", "greek cross", "add", "cross", "geometry", "shape"])
def _(S):
    return [shell(poly(_plus_pts(3, 9), closed=True, r=rnd(S, 0, 1.75)))]


@icon("star-4", CAT, "Four-pointed star", tags=["four point star", "sparkle", "twinkle", "star", "geometry", "shape"], aliases=["four-pointed-star"])
def _(S):
    return [closed(S, star(12, 12, 8.5, 4, 4), 1)]


@icon("star-6", CAT, "Six-pointed star", tags=["six point star", "hexagram", "star", "geometry", "shape"], aliases=["six-pointed-star"])
def _(S):
    return [closed(S, star(12, 12, 8.75, 4.9, 6), 1)]


# ============================================================================ lines and freeform

@icon("spiral", CAT, "Spiral winding out from the centre", tags=["swirl", "coil", "vortex", "hypnotic", "geometry", "shape"])
def _(S):
    b = 4 / (2 * math.pi)
    pts = []
    th = math.pi * 0.75
    while th <= 4.5 * math.pi + 1e-6:
        r = b * th
        pts.append((12 + r * math.cos(th - math.pi / 2), 12.5 + r * math.sin(th - math.pi / 2)))
        th += math.radians(6)
    return [line(poly(pts))]


def _wave_pts(y0, x0=3.0, x1=21.0, amp=2.25, n=36, flip=False):
    pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append((x, y0 - amp * math.sin(2 * math.pi * (x - x0) / 9)))
    return pts[::-1] if flip else pts


@icon("wave-shape", CAT, "Band with wavy top and bottom edges", tags=["wave", "wavy", "ripple", "banner", "geometry", "shape"])
def _(S):
    pts = _wave_pts(7.5) + _wave_pts(16.5, flip=True)
    return [shell(poly(pts, closed=True, r=rnd(S, 0, 2)))]


@icon("zigzag", CAT, "Zigzag line", tags=["zig zag", "jagged", "sawtooth", "lightning", "line", "shape"])
def _(S):
    xs = [2.5 + 3.8 * i for i in range(6)]
    pts = [(x, 16 if i % 2 == 0 else 8) for i, x in enumerate(xs)]
    return [line(poly(pts, r=S.r * 0.4))]


@icon("squiggle", CAT, "Looping squiggle line", tags=["scribble", "doodle", "loop", "curly", "freehand", "shape"])
def _(S):
    pts = []
    n = 90
    t0, t1 = -0.35 * math.pi, 4.35 * math.pi
    raw = []
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        raw.append((1.35 * t - 3.4 * math.sin(t), -3.4 * math.cos(t) + 0.0 * t))
    xmin = min(p[0] for p in raw)
    xmax = max(p[0] for p in raw)
    k = 18 / (xmax - xmin)
    for x, y in raw:
        pts.append((3 + (x - xmin) * k, 12 + y * 1.5))
    return [line(poly(pts))]


def _smooth_closed(pts, tension=1 / 6):
    """Closed Catmull-Rom curve through pts as cubic Béziers."""
    n = len(pts)
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) * tension, p1[1] + (p2[1] - p0[1]) * tension)
        c2 = (p2[0] - (p3[0] - p1[0]) * tension, p2[1] - (p3[1] - p1[1]) * tension)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d + "Z"


@icon("blob", CAT, "Soft organic blob with a highlight", tags=["organic", "amoeba", "fluid", "freeform", "splat", "shape"])
def _(S):
    pts = [(11.5, 3.5), (18, 4.5), (20.5, 11), (18.5, 18.5), (11, 20.5), (4.5, 17), (3.5, 9.5)]
    hl = "M7.5 11.5C7.5 9.3 8.8 7.9 10.8 7.5"
    return [shell(_smooth_closed(pts)), detail(hl)]


_POLY = [(5, 5), (14.5, 3.5), (20.5, 10), (18, 19.5), (8.5, 20.5), (3.5, 13.5)]


@icon("polygon", CAT, "Irregular polygon with its corner points marked", tags=["polygon", "vertices", "nodes", "path", "geometry", "shape"],
      filled=lambda: filled_region([shell(poly(_POLY, closed=True))]))
def _(S):
    pts = _POLY
    return [shell(poly(pts, closed=True, r=rnd(S, 0, 1.5)))] + [centre(S, x, y, 3.5) for x, y in pts]


# ============================================================================ solids

@icon("cube-shape", CAT, "Cube drawn in three-quarter view", tags=["cube", "box", "3d", "block", "hexahedron", "solid"])
def _(S):
    V = regular(12, 12, 9.25, 6)
    return [shell(poly(V, closed=True, r=rnd(S, 0, 2))),
            detail(poly([V[1], (12, 12), V[5]], r=S.r * 0.5)), detail(seg(12, 12, *V[3]))]


@icon("sphere", CAT, "Shaded sphere with a tilted equator and a highlight", tags=["ball", "globe", "3d", "orb", "round", "solid"])
def _(S):
    eq = xd("M3 12A9 3.5 0 0 0 21 12", rotation(-20))
    return [shell(circle(12, 12, 9)), detail(eq), detail(arc(12, 12, 5.5, 195, 245))]


def _cyl_filled():
    sil = U(P(ellipse(12, 6, 7.5, 2.75)), P(rect(4.5, 6, 15, 12)), P(ellipse(12, 18, 7.5, 2.75)))
    sil = U(sil, ST(path_to_d(sil), 2))
    return D(sil, ST("M4.5 6A7.5 2.75 0 0 0 19.5 6", 2), ST(seg(8, 11, 8, 17), 2))


@icon("cylinder", CAT, "Cylinder with a highlight down its side", tags=["tube", "can", "3d", "database", "pipe", "solid"],
      filled=_cyl_filled)
def _(S):
    return [shell(ellipse(12, 6, 7.5, 2.75)), line("M4.5 6V18A7.5 2.75 0 0 0 19.5 18V6"), detail(seg(8, 11, 8, 17))]


@icon("cone", CAT, "Cone standing on its round base", tags=["cone", "3d", "funnel", "traffic cone", "solid"])
def _(S):
    return [shell("M12 3L4 18A8 2.75 0 0 0 20 18Z")]


@icon("pyramid-shape", CAT, "Square pyramid in three-quarter view", tags=["pyramid", "3d", "tetrahedron", "egypt", "solid"])
def _(S):
    return [shell(poly([(12, 3), (21, 15.5), (13, 21), (3, 17)], closed=True, r=rnd(S, 0, 1.5))),
            detail(seg(12, rnd(S, 3, 4.5), 13, 21))]


_SMILE = "M6.5 10.5C8.5 14 15.5 14 17.5 10.5"
_FROWN = "M8.5 12.2C10.2 10.3 13.8 10.3 15.5 12.2"


def _torus_filled():
    lens = I(P(_SMILE + "L17.5 5L6.5 5Z"), P(_FROWN + "L15.5 20L8.5 20Z"))
    body = U(P(ellipse(12, 12, 9.5, 6.5)), ST(ellipse(12, 12, 9.5, 6.5), 2))
    return D(body, U(lens, ST(path_to_d(lens), 2.5, "butt", "round")))


@icon("torus", CAT, "Torus (ring doughnut) in perspective", tags=["donut", "doughnut", "ring", "3d", "solid"], filled=_torus_filled)
def _(S):
    return [shell(ellipse(12, 12, 9.5, 6.5)),
            detail(_SMILE), detail(_FROWN)]


@icon("prism", CAT, "Triangular prism in three-quarter view", tags=["prism", "3d", "wedge", "triangular", "solid"])
def _(S):
    F1, F2, F3 = (3, 19.5), (13, 19.5), (8, 11)
    v = (8, -6.5)
    B2, B3 = (F2[0] + v[0], F2[1] + v[1]), (F3[0] + v[0], F3[1] + v[1])
    return [shell(poly([F1, F2, B2, B3, F3], closed=True, r=rnd(S, 0, 1.5))), detail(seg(*F2, *F3))]


# ============================================================================ emblems

def _heart():
    c = 12.6
    sq = P(poly([(12, c - 7.07), (19.07, c), (12, c + 7.07), (4.93, c)], closed=True))
    return U(sq, P(circle(12 - 3.535, c - 3.535, 5)), P(circle(12 + 3.535, c - 3.535, 5)))


@icon("heart-outline-shape", CAT, "Geometric heart built from a square and two circles", tags=["heart", "love", "valentine", "geometry", "shape"])
def _(S):
    h = _heart()
    if S.name == "rounded":
        h = soften(h, 1.75)
    return [shell(path_to_d(h))]


_SHIELD = "M4 3.5H20V10.5C20 15.5 16.5 19 12 21C7.5 19 4 15.5 4 10.5Z"


@icon("shield-shape", CAT, "Heater shield shape with a flat top", tags=["shield", "crest", "emblem", "badge", "heraldry", "shape"])
def _(S):
    return [shell(_SHIELD if S.name == "line" else path_to_d(soften(P(_SHIELD), 2)))]


@icon("badge-shape", CAT, "Serrated seal badge", tags=["seal", "rosette", "sticker", "certified", "award", "shape"])
def _(S):
    return [shell(poly(star(12, 12, 9.25, 7.5, 12), closed=True, r=rnd(S, 0, 1)))]
