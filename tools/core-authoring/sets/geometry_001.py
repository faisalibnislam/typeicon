"""TypeIcon Core: geometry (batch 001).

Plane figures, solids, angles and classic textbook constructions. Line keeps corners sharp (miter joins) and
marks points with small squares; Rounded rounds the corners and marks points with round dots, following the
`shapes` module. Construction lines inside a figure are details, so the Filled style knocks them out of the
solid figure.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, I, P, Part, ST, U, arc, circle, detail, dot, ellipse, icon, line, path_to_d, poly, pt_on, rect, regular, seg,
    shell, solid,
)
from geometry import fmt, transform_path

CAT = "geometry"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def closed(S, pts, k=2.0):
    return shell(poly(pts, closed=True, r=L(S, 0, k)))


def pt(S, x, y, s=2.75):
    """A marked point: square in Line, round in Rounded; knocked out of a Filled figure."""
    if S.name == "line":
        return Part("dot", rect(x - s / 2, y - s / 2, s, s))
    return dot(x, y, s / 2 + 0.15)


def pt_dir(S, x, y, deg, s=3.5):
    """Marked point on a slanted line: square aligned with the line in Line, round in Rounded."""
    if S.name == "line":
        h = s / 2
        pts = [pt_on(x, y, h * math.sqrt(2), deg + 45 + 90 * i) for i in range(4)]
        return Part("dot", poly(pts, closed=True))
    return dot(x, y, s / 2 + 0.15)


def ins(S, p, q, d=1.25):
    """Endpoint p pulled toward q by d px in Rounded (keeps round caps inside rounded corners)."""
    if S.name == "line":
        return p
    u = unit(p, q)
    return (p[0] + u[0] * d, p[1] + u[1] * d)


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    return dx / n, dy / n


def ang(a, b):
    """Screen angle (degrees, 0 = right, 90 = down) of the direction a -> b."""
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))


def tick_d(a, b, t=0.5, half=2.0, offset=0.0):
    """Short stroke across segment a-b at parameter t, shifted along the segment by offset px."""
    ux, uy = unit(a, b)
    m = lerp(a, b, t)
    m = (m[0] + ux * offset, m[1] + uy * offset)
    return seg(m[0] - uy * half, m[1] + ux * half, m[0] + uy * half, m[1] - ux * half)


def ticks(a, b, n, t=0.5, half=2.0, gap=3.5, role=detail):
    return [role(tick_d(a, b, t, half, (i - (n - 1) / 2) * gap)) for i in range(n)]


def dashes(S, a, b, n, role=detail):
    """n equal dashes from a to b (ends included). Rounded dashes are shortened so round caps keep the gaps."""
    total = math.dist(a, b)
    step = total / (2 * n - 1)
    out = []
    for i in range(n):
        t0, t1 = 2 * i * step / total, (2 * i + 1) * step / total
        p, q = lerp(a, b, t0), lerp(a, b, t1)
        if S.name == "rounded":
            sh = min(0.95, (step - 0.1) / 2) / total
            p, q = lerp(a, b, t0 + sh), lerp(a, b, t1 - sh)
        out.append(role(seg(*p, *q)))
    return out


def corner_mark(S, c, p1, p2, s=3.0, role=detail):
    """Right-angle square mark at corner c between the directions to p1 and p2."""
    u1, u2 = unit(c, p1), unit(c, p2)
    a = (c[0] + u1[0] * s, c[1] + u1[1] * s)
    b = (c[0] + u2[0] * s, c[1] + u2[1] * s)
    m = (a[0] + u2[0] * s, a[1] + u2[1] * s)
    return role(poly([a, m, b], r=S.r * 0.4))


def star_pts(cx, cy, r_out, r_in, n, start=-90.0):
    return [pt_on(cx, cy, r_out if i % 2 == 0 else r_in, start + i * 180 / n) for i in range(2 * n)]


def soften(region, r):
    """Round the convex corners of a boolean region by radius r (morphological opening)."""
    er = D(region, ST(path_to_d(region), 2 * r, "butt", "round"))
    return U(er, ST(path_to_d(er), 2 * r, "butt", "round"))


def soft_shell(S, d, r=1.25):
    return shell(d if S.name == "line" else path_to_d(soften(P(d), r)))


def xsect(p1, p2, p3, p4):
    """Intersection of lines p1-p2 and p3-p4."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


# ============================================================================ polygons and plane figures

@icon("nonagon", CAT, "Regular nine-sided polygon standing on a flat edge",
      tags=["enneagon", "nine sides", "polygon", "shape", "geometry"], aliases=["enneagon"])
def _(S):
    return [closed(S, regular(12, 12.35, 9.5, 9), 2.5)]


@icon("dodecagon", CAT, "Regular twelve-sided polygon",
      tags=["twelve sides", "12-gon", "polygon", "shape", "geometry"])
def _(S):
    return [closed(S, regular(12, 12, 9.5, 12, -75), 2.5), pt(S, 12, 12)]


_ISO = [(12, 4), (19, 21), (5, 21)]


@icon("isosceles-triangle", CAT, "Tall triangle with tick marks on its two equal sides",
      tags=["isosceles", "equal sides", "triangle", "tick marks", "geometry"])
def _(S):
    a, b, c = _ISO
    return [closed(S, _ISO, 1.5), *ticks(a, c, 1, half=2.25), *ticks(a, b, 1, half=2.25)]


_SCA = [(7.5, 4), (21.5, 20), (2.5, 20)]


@icon("scalene-triangle", CAT, "Lopsided triangle with one, two and three tick marks on its unequal sides",
      tags=["scalene", "unequal sides", "triangle", "tick marks", "geometry"])
def _(S):
    a, b, c = _SCA
    return [closed(S, _SCA, 1.5), *ticks(c, a, 1, half=2), *ticks(c, b, 2, half=2, gap=4),
            *ticks(a, b, 3, t=0.52, half=1.75, gap=4)]


_OBT = [(4, 7), (9, 18.5), (20.5, 18.5)]


@icon("obtuse-triangle", CAT, "Long flat triangle with its wide obtuse angle marked by an arc",
      tags=["obtuse", "wide angle", "triangle", "angle", "geometry"])
def _(S):
    c, a, b = _OBT
    return [closed(S, _OBT, 1.25), detail(arc(*a, 4.5, ang(a, c) + 4, -4))]


_KITE = [(12, 2.5), (19.5, 8.5), (12, 21.5), (4.5, 8.5)]


@icon("kite-quadrilateral", CAT, "Kite shape with its two diagonals crossing at right angles",
      tags=["kite", "deltoid", "quadrilateral", "diagonals", "geometry"])
def _(S):
    t, r, b, l_ = _KITE
    return [closed(S, _KITE, 1.75), detail(seg(12, L(S, 2.5, 3), 12, L(S, 21.5, 19.75))),
            detail(seg(L(S, 4.5, 5), 8.5, L(S, 19.5, 19), 8.5))]


def _squircle(r, k):
    c = 12
    return (f"M{fmt(c + r)} {fmt(c)}C{fmt(c + r)} {fmt(c + k)} {fmt(c + k)} {fmt(c + r)} {fmt(c)} {fmt(c + r)}"
            f"C{fmt(c - k)} {fmt(c + r)} {fmt(c - r)} {fmt(c + k)} {fmt(c - r)} {fmt(c)}"
            f"C{fmt(c - r)} {fmt(c - k)} {fmt(c - k)} {fmt(c - r)} {fmt(c)} {fmt(c - r)}"
            f"C{fmt(c + k)} {fmt(c - r)} {fmt(c + r)} {fmt(c - k)} {fmt(c + r)} {fmt(c)}Z")


@icon("squircle", CAT, "Squircle: a shape between a square and a circle with smooth corners",
      tags=["superellipse", "rounded square", "app icon shape", "shape", "geometry"])
def _(S):
    return [shell(_squircle(9, L(S, 8.4, 7.6)))]


def _ring(r1, r2):
    return circle(12, 12, r1) + f"M{fmt(12 + r2)} 12A{fmt(r2)} {fmt(r2)} 0 1 1 {fmt(12 - r2)} 12A{fmt(r2)} {fmt(r2)} 0 1 1 {fmt(12 + r2)} 12Z"


@icon("annulus", CAT, "Annulus: flat ring between two concentric circles",
      tags=["ring", "washer", "concentric circles", "band", "geometry"])
def _(S):
    return [shell(_ring(9.25, 4.75)), pt(S, 12, 12, 2.5)]


@icon("quarter-circle", CAT, "Quarter circle: two radii at a right angle joined by an arc",
      tags=["quadrant", "quarter", "sector", "90 degrees", "geometry"])
def _(S):
    o = (4, 20)
    return [shell(f"M4 20V4A16 16 0 0 1 20 20Z" if S.name == "line" else
                  path_to_d(soften(P("M4 20V4A16 16 0 0 1 20 20Z"), 1.5))), pt(S, 7.5, 16.5)]


def _deltoid():
    pts = []
    n = 72
    for i in range(n):
        t = 2 * math.pi * i / n
        x = 2 * math.cos(t) + math.cos(2 * t)
        y = 2 * math.sin(t) - math.sin(2 * t)
        # rotate so a cusp points up, scale so the cusps sit on radius 9.5
        a = -math.pi / 2
        xr, yr = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
        pts.append((12 + xr * 9.5 / 3, 13.2 + yr * 9.5 / 3))
    return poly(pts, closed=True)


@icon("deltoid-curve", CAT, "Deltoid curve: a curved triangle with three sharp cusps",
      tags=["deltoid", "tricuspoid", "steiner curve", "hypocycloid", "geometry"])
def _(S):
    return [soft_shell(S, _deltoid(), 1.0)]


def _lune():
    # circle A centre (9.5,12) r 7.5 minus circle B centre (14.5,12) r 7.5
    return path_to_d(D(P(circle(9, 12, 7)), P(circle(14, 12, 7))))


@icon("lune-shape", CAT, "Lune: the crescent left over where one circle overlaps another",
      tags=["lune", "crescent", "overlapping circles", "difference", "geometry"])
def _(S):
    y0 = 12 - math.sqrt(49 - 6.25)
    return [soft_shell(S, _lune(), 0.9), line(arc(14, 12, 7, ang((14, 12), (11.5, y0)), ang((14, 12), (11.5, 24 - y0))))]


_ARB = "M3 16A9 9 0 0 1 21 16A4 4 0 0 0 13 16A5 5 0 0 0 3 16Z"


@icon("arbelos", CAT, "Arbelos: a large semicircle with two smaller semicircles cut from its base",
      tags=["arbelos", "shoemaker's knife", "semicircles", "archimedes", "geometry"],
      filled=lambda: U(P(_ARB), ST(_ARB, 2, "butt", "miter"), ST(seg(1.5, 17.25, 22.5, 17.25), 1.5)))
def _(S):
    return [shell(_ARB), line(seg(L(S, 1.5, 2.5), 16, L(S, 22.5, 21.5), 16))]


_CONC = [(12, 3), (20.5, 20.5), (12, 15), (3.5, 20.5)]


@icon("concave-polygon", CAT, "Arrowhead-shaped concave polygon with its reflex angle marked",
      tags=["concave", "non-convex", "reflex angle", "dart", "polygon", "geometry"])
def _(S):
    v = (12, 15)
    return [closed(S, _CONC, 1.25), detail(arc(*v, 3.5, ang(v, _CONC[3]) + 14, ang(v, _CONC[1]) + 346))]


# ============================================================================ star polygons

def _star_with_core(S, cx, cy, r_out, r_in, n, k=1.0, start=-90.0):
    outer = star_pts(cx, cy, r_out, r_in, n, start)
    core = outer[1::2]
    return [closed(S, outer, k), detail(poly(core, closed=True, r=S.r * 0.4))]


@icon("pentagram", CAT, "Pentagram: five-pointed star of crossing lines around a pentagon",
      tags=["pentacle", "five pointed star", "star polygon", "pentagon", "geometry"])
def _(S):
    return _star_with_core(S, 12, 12.75, 9, 9 * 0.382, 5, 0.9)


@icon("heptagram", CAT, "Heptagram: seven-pointed star drawn with crossing straight lines",
      tags=["septagram", "seven pointed star", "star polygon", "heptagon", "geometry"])
def _(S):
    v = regular(12, 12.4, 9.5, 7)
    order = [v[(3 * i) % 7] for i in range(7)]
    return [line(poly(order, closed=True, r=S.r * 0.3))]


@icon("octagram", CAT, "Octagram: two overlapping squares forming an eight-pointed star",
      tags=["star of lakshmi", "eight pointed star", "two squares", "star polygon", "octagon", "geometry"])
def _(S):
    return _star_with_core(S, 12, 12, 9.75, 9.75 * 0.7654, 8, 1.0, -90)


# ============================================================================ solids

@icon("tetrahedron", CAT, "Tetrahedron: triangular pyramid with its hidden back edge dashed",
      tags=["triangular pyramid", "polyhedron", "platonic solid", "3d", "d4", "geometry"])
def _(S):
    apex, left, front, right = (11.5, 2.5), (2.5, 17.5), (13.5, 21.5), (21.5, 15)
    return [closed(S, [apex, right, front, left], 1.25), detail(seg(*ins(S, apex, front, 1.6), *ins(S, front, apex, 0.8))),
            *dashes(S, lerp(left, right, 0.12), lerp(left, right, 0.44), 2),
            *dashes(S, lerp(left, right, 0.64), lerp(left, right, 0.88), 1)]


@icon("cuboid", CAT, "Cuboid: long rectangular box showing its front, top and side",
      tags=["rectangular prism", "box", "block", "brick", "3d", "geometry"])
def _(S):
    x0, x1, y0, y1, v = 2.5, 16, 10, 20.5, (5.5, -5.5)
    out = [(x0, y0), (x0 + v[0], y0 + v[1]), (x1 + v[0], y0 + v[1]), (x1 + v[0], y1 + v[1]), (x1, y1), (x0, y1)]
    return [closed(S, out, 1.25), detail(poly([(x0, y0), (x1, y0), (x1, y1)], r=S.r * 0.4)),
            detail(seg(x1, y0, x1 + v[0], y0 + v[1]))]


def _hull(points):
    pts = sorted(set(points))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 1e-9:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 1e-9:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def prism(S, front, v, k=1.25):
    """Convex prism: front face (convex polygon) extruded by offset v. Returns shell + visible inner edges."""
    back = [(x + v[0], y + v[1]) for x, y in front]
    hull = _hull(front + back)
    hk = [(round(x, 6), round(y, 6)) for x, y in hull]

    def on_hull(a, b):
        a, b = (round(a[0], 6), round(a[1], 6)), (round(b[0], 6), round(b[1], 6))
        if a not in hk or b not in hk:
            return False
        i, j = hk.index(a), hk.index(b)
        return abs(i - j) in (1, len(hk) - 1)
    parts = [closed(S, hull, k)]
    n = len(front)
    for i in range(n):
        a, b = front[i], front[(i + 1) % n]
        if not on_hull(a, b):
            parts.append(detail(seg(*a, *b)))
    for i in range(n):
        bi = (round(back[i][0], 6), round(back[i][1], 6))
        if bi in hk and not on_hull(front[i], back[i]):
            parts.append(detail(seg(*front[i], *back[i])))
    return parts


@icon("parallelepiped", CAT, "Parallelepiped: slanted box whose faces are parallelograms",
      tags=["slanted box", "skewed prism", "oblique", "polyhedron", "3d", "geometry"])
def _(S):
    return prism(S, [(2.5, 19.5), (12.5, 19.5), (15.5, 10.5), (5.5, 10.5)], (6, -5.5))


@icon("pentagonal-prism", CAT, "Pentagonal prism with pentagon faces joined by rectangles",
      tags=["pentagon", "prism", "polyhedron", "3d", "solid", "geometry"])
def _(S):
    return prism(S, regular(9.5, 14, 7.5, 5), (6, -5.5), 2.5)


@icon("ellipsoid", CAT, "Ellipsoid: stretched sphere with a curved equator and meridian",
      tags=["spheroid", "egg", "oval solid", "3d", "quadric", "geometry"])
def _(S):
    return [shell(ellipse(12, 12, 9.5, 7)),
            detail(f"M{L(S, 2.5, 3.2)} 12A9.5 3.25 0 0 0 {L(S, 21.5, 20.8)} 12"),
            detail(f"M12 {L(S, 5, 5.7)}A4 7 0 0 1 12 {L(S, 19, 18.3)}")]


@icon("triangular-bipyramid", CAT, "Triangular bipyramid: two triangular pyramids joined base to base",
      tags=["dipyramid", "double pyramid", "polyhedron", "crystal", "3d", "geometry"])
def _(S):
    top, bot, left, right, front = (12, 2.5), (12, 21.5), (2.5, 12.5), (21.5, 11), (9.5, 14.5)
    return [closed(S, [top, right, bot, left], 2.25),
            detail(poly([ins(S, top, front, 1.6), front, ins(S, bot, front, 1.6)], r=S.r * 0.5)),
            detail(poly([ins(S, left, front, 1.6), front, ins(S, right, front, 1.6)], r=S.r * 0.5))]


def _truncated_cube(t=0.3, R=9.5):
    V = regular(12, 12, R, 6)
    C = (12, 12)
    outline = []
    for k in range(6):
        outline += [lerp(V[k], V[k - 1], t), lerp(V[k], V[(k + 1) % 6], t)]
    inner = []
    Q = [lerp(C, V[k], t) for k in (1, 3, 5)]
    inner.append((Q, True))
    for j, k in enumerate((1, 3, 5)):
        Pk = lerp(V[k], C, t)
        inner.append(([Q[j], Pk], False))
        inner.append(([lerp(V[k], V[k - 1], t), Pk, lerp(V[k], V[(k + 1) % 6], t)], False))
    return outline, inner


@icon("truncated-cube", CAT, "Truncated cube: a cube with every corner sliced off",
      tags=["archimedean solid", "cut corners", "polyhedron", "3d", "cube", "geometry"])
def _(S):
    outline, inner = _truncated_cube(0.3, 9.75)
    return [closed(S, outline, 2.5)] + [detail(poly(p, closed=c, r=S.r * (1.0 if c else 0.5))) for p, c in inner]


@icon("cuboctahedron", CAT, "Cuboctahedron: a solid of alternating square and triangular faces",
      tags=["archimedean solid", "vector equilibrium", "squares and triangles", "polyhedron", "3d", "geometry"])
def _(S):
    R = 9.75
    H = regular(12, 12, R, 6)
    T = [pt_on(12, 12, R / math.sqrt(3), a) for a in (-60, 60, 180)]
    parts = [closed(S, H, 2.5), detail(poly(T, closed=True, r=S.r * 0.5))]
    for p, (i, j) in zip(T, ((0, 1), (2, 3), (4, 5))):
        parts.append(detail(poly([ins(S, H[i], p, 1.0), p, ins(S, H[j], p, 1.0)], r=S.r * 0.4)))
    return parts


@icon("truncated-octahedron", CAT, "Truncated octahedron: a square face in front surrounded by hexagonal faces",
      tags=["archimedean solid", "space filling", "hexagons and squares", "polyhedron", "3d", "geometry"])
def _(S):
    k = 4.75
    out = [(12 + x * k, 12 + y * k) for x, y in ((1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2))]
    dia = [(12, 12 - k), (12 + k, 12), (12, 12 + k), (12 - k, 12)]
    mids = [(12, 12 - 2 * k), (12 + 2 * k, 12), (12, 12 + 2 * k), (12 - 2 * k, 12)]
    return [closed(S, out, 2.0), detail(poly(dia, closed=True, r=S.r * 0.5))] + [
        detail(seg(*a, *ins(S, b, a, 0.6))) for a, b in zip(dia, mids)]


@icon("stellated-octahedron", CAT, "Stellated octahedron: two interlocking tetrahedra forming a star solid",
      tags=["stella octangula", "star tetrahedron", "compound", "polyhedron", "3d", "geometry"])
def _(S):
    pts = star_pts(12, 12, 9.75, 9.75 / math.sqrt(3), 6)
    return [closed(S, pts, 0.8)] + [detail(seg(12, 12, *ins(S, pts[i], (12, 12), 1.2))) for i in (0, 4, 8)]


@icon("stellated-dodecahedron", CAT, "Stellated dodecahedron: a spiky star-shaped polyhedron",
      tags=["spiky ball", "star polyhedron", "kepler poinsot", "stellation", "3d", "geometry"])
def _(S):
    cx, cy = 12, 12.6
    out, inner = [], []
    for j in range(5):
        a = -90 + 72 * j
        tip = pt_on(cx, cy, 9.5, a)
        k0 = pt_on(cx, cy, 3.6, a + 36)       # core pentagon corner between this spike and the next
        nxt = pt_on(cx, cy, 9.5, a + 72)
        x0, y0 = lerp(tip, k0, 0.62), lerp(nxt, k0, 0.62)
        short = pt_on(cx, cy, 7.4, a + 36)    # spike behind, peeking out between the front ones
        out += [tip, x0, short, y0]
        inner.append(poly([x0, k0, y0], r=S.r * 0.3))
    return [closed(S, out, 0.6)] + [detail(d) for d in inner]


@icon("square-antiprism", CAT, "Square antiprism: two twisted squares joined by a band of triangles",
      tags=["antiprism", "twisted", "triangles", "polyhedron", "3d", "geometry"])
def _(S):
    r, e, y0, y1 = 9, 0.33, 6.5, 18.2

    def top(a):
        x, y = pt_on(12, y0, r, a)
        return (x, y0 + (y - y0) * e)

    def bot(a):
        x, y = pt_on(12, y1, r, a)
        return (x, y1 + (y - y1) * e)
    t0, t90, t180, t270 = top(0), top(90), top(180), top(270)
    b45, b135 = bot(45), bot(135)
    return [closed(S, [t180, t270, t0, b45, b135], 1.0), detail(poly([t180, t90, t0], r=S.r * 0.4)),
            detail(poly([b135, t90, b45], r=S.r * 0.4))]


@icon("bicone", CAT, "Bicone: two cones joined at their round bases",
      tags=["double cone", "spinning top", "dicone", "3d", "solid", "geometry"])
def _(S):
    return [closed(S, [(12, 2.5), (21.5, 12), (12, 21.5), (2.5, 12)], 1.5), detail("M2.5 12A9.5 3.25 0 0 0 21.5 12")]


def _ellipse_arc_pts(cx, cy, rx, ry, a0, a1, n=8):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def ellipse_dashes(S, cx, cy, rx, ry, a0, a1, n, role=detail):
    """n dashes along an elliptical arc from angle a0 to a1 (degrees)."""
    out = []
    step = (a1 - a0) / (2 * n - 1)
    trim = 0 if S.name == "line" else step * 0.28
    for i in range(n):
        s0, s1 = a0 + 2 * i * step + trim, a0 + (2 * i + 1) * step - trim
        out.append(role(poly(_ellipse_arc_pts(cx, cy, rx, ry, s0, s1, 4))))
    return out


@icon("spherical-cap", CAT, "Spherical cap: a dome sliced from a sphere with a flat round base",
      tags=["dome", "cap", "segment of sphere", "3d", "solid", "geometry"])
def _(S):
    y = 15
    return [shell(f"M2.5 {y}A9.77 9.77 0 0 1 21.5 {y}A9.5 2.75 0 0 1 2.5 {y}Z"),
            *ellipse_dashes(S, 12, y, 9.5, 2.75, 197, 343, 4)]


@icon("paraboloid", CAT, "Paraboloid: bowl-shaped surface with an elliptical rim",
      tags=["bowl", "parabolic dish", "quadric surface", "3d", "reflector", "geometry"])
def _(S):
    rim = 6.5
    return [soft_shell(S, f"M3 {rim}A9 2.75 0 0 1 21 {rim}Q12 34 3 {rim}Z", 1.25),
            detail(f"M{L(S, 3, 3.3)} {rim}A9 2.75 0 0 0 {L(S, 21, 20.7)} {rim}"),
            detail("M5.6 13.5A6.4 2 0 0 0 18.4 13.5")]


@icon("hyperboloid", CAT, "Hyperboloid: hourglass tower surface made of straight crossing lines",
      tags=["cooling tower", "hourglass", "ruled surface", "quadric", "3d", "geometry"])
def _(S):
    return [soft_shell(S, "M4.5 4.5A7.5 2 0 0 1 19.5 4.5Q14 12 19.5 19.5A7.5 2 0 0 1 4.5 19.5Q10 12 4.5 4.5Z", 1.0),
            detail(f"M{L(S, 4.5, 4.9)} 4.5A7.5 2 0 0 0 {L(S, 19.5, 19.1)} 4.5"),
            detail(seg(*ins(S, (5.6, 5.5), (18.4, 20.5), 0.6), *ins(S, (18.4, 20.5), (5.6, 5.5), 0.6))),
            detail(seg(*ins(S, (18.4, 5.5), (5.6, 20.5), 0.6), *ins(S, (5.6, 20.5), (18.4, 5.5), 0.6)))]


def _hypar_raw(u, v, az=45, el=70, k=0.8):
    z = k * (u * u - v * v)
    a, e = math.radians(az), math.radians(el)
    x = u * math.cos(a) - v * math.sin(a)
    y = u * math.sin(a) + v * math.cos(a)
    return x, -z * math.cos(e) + y * math.sin(e)


def _hypar_fit():
    pts = [_hypar_raw(-1 + 2 * i / 20, -1 + 2 * j / 20) for i in range(21) for j in range(21)]
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    s = min(19 / (x1 - x0), 19 / (y1 - y0))
    return s, (x0 + x1) / 2, (y0 + y1) / 2


_HYP = _hypar_fit()


def _hypar(u, v):
    s, mx, my = _HYP
    x, y = _hypar_raw(u, v)
    return (12 + (x - mx) * s, 12 + (y - my) * s)


def _hypar_line(fixed, along_u, n=10):
    return [_hypar(-1 + 2 * i / n, fixed) if along_u else _hypar(fixed, -1 + 2 * i / n) for i in range(n + 1)]


@icon("hyperbolic-paraboloid", CAT, "Hyperbolic paraboloid: saddle surface drawn with a grid of curved lines",
      tags=["saddle", "hypar", "pringle", "quadric surface", "3d", "geometry"])
def _(S):
    edge = (_hypar_line(-1, True) + _hypar_line(1, False)[1:] + _hypar_line(1, True)[::-1][1:]
            + _hypar_line(-1, False)[::-1][1:-1])
    parts = [closed(S, edge, 1.25)]
    for f in (-1 / 3, 1 / 3):
        parts.append(detail(poly(_hypar_line(f, True))))
        parts.append(detail(poly(_hypar_line(f, False))))
    return parts


def _torus_knot(n=160, p=2, q=5, gap=2.6):
    """(p,q) torus knot projected flat, split into strands with gaps at the under-crossings."""
    pts = []
    for i in range(n):
        t = 2 * math.pi * p * i / n
        r = 2 + math.cos(q * t / p)
        pts.append((12 + 3.15 * r * math.cos(t - math.pi / 2), 12 + 3.15 * r * math.sin(t - math.pi / 2)))
    segs = [(pts[i], pts[(i + 1) % n]) for i in range(n)]

    def inter(a, b, c, d):
        den = (a[0] - b[0]) * (c[1] - d[1]) - (a[1] - b[1]) * (c[0] - d[0])
        if abs(den) < 1e-12:
            return None
        t = ((a[0] - c[0]) * (c[1] - d[1]) - (a[1] - c[1]) * (c[0] - d[0])) / den
        u = -((a[0] - b[0]) * (a[1] - c[1]) - (a[1] - b[1]) * (a[0] - c[0])) / den
        if 0 <= t < 1 and 0 <= u < 1:
            return t, u
        return None
    events = []  # (curve parameter in segment units, crossing id)
    cid = 0
    for i in range(n):
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            r = inter(*segs[i], *segs[j])
            if r:
                events.append((i + r[0], cid))
                events.append((j + r[1], cid))
                cid += 1
    events.sort()
    under = [e[0] for k, e in enumerate(events) if k % 2 == 1]
    # arc-length parameter per sample
    cum = [0.0]
    for a, b in segs:
        cum.append(cum[-1] + math.dist(a, b))
    total = cum[-1]

    def s_of(u):
        i = int(u)
        return cum[i] + (u - i) * (cum[i + 1] - cum[i])

    cuts = sorted(s_of(u) for u in under)

    def point_at(s):
        s %= total
        lo = 0
        while cum[lo + 1] < s:
            lo += 1
        f = (s - cum[lo]) / (cum[lo + 1] - cum[lo])
        return lerp(segs[lo][0], segs[lo][1], f)
    strands = []
    for k in range(len(cuts)):
        s0 = cuts[k] + gap
        s1 = cuts[(k + 1) % len(cuts)] - gap
        if s1 <= s0:
            s1 += total
        m = max(3, int((s1 - s0) / 1.2))
        strands.append([point_at(s0 + (s1 - s0) * i / m) for i in range(m + 1)])
    return strands


@icon("torus-knot", CAT, "Torus knot: a closed loop winding around a ring with over and under crossings",
      tags=["knot", "cinquefoil", "knot theory", "topology", "loop", "geometry"])
def _(S):
    return [line(poly(s)) for s in _torus_knot(gap=L(S, 2.9, 3.3))]


def _scaled(d_pts, s, cx, cy):
    return [(cx + (x - 12) * s, cy + (y - 12) * s) for x, y in d_pts]


@icon("double-torus", CAT, "Double torus: a pretzel-like solid with two holes",
      tags=["genus two", "two holes", "pretzel", "topology", "surface", "3d", "geometry"])
def _(S):
    body = path_to_d(U(P(ellipse(7.5, 12, 5.5, 7.5)), P(ellipse(16.5, 12, 5.5, 7.5))))
    parts = [soft_shell(S, body, 1.5) if S.name == "rounded" else shell(body)]
    for cx in (7.5, 16.5):
        parts.append(detail(f"M{fmt(cx - 3.5)} 10.8C{fmt(cx - 2.2)} 14 {fmt(cx + 2.2)} 14 {fmt(cx + 3.5)} 10.8"))
        parts.append(detail(f"M{fmt(cx - 2.1)} 12.6C{fmt(cx - 1.1)} 11.3 {fmt(cx + 1.1)} 11.3 {fmt(cx + 2.1)} 12.6"))
    return parts


_CUBE_F = (2.5, 8.5, 15.5, 21.5)  # front square x0, y0, x1, y1
_CUBE_V = (6, -6)


@icon("wireframe-cube", CAT, "See-through cube with all twelve edges drawn",
      tags=["wireframe", "transparent cube", "necker cube", "3d model", "mesh", "geometry"])
def _(S):
    x0, y0, x1, y1 = _CUBE_F
    vx, vy = _CUBE_V
    bx0, by0, bx1, by1 = x0 + vx, y0 + vy, x1 + vx, y1 + vy
    k = S.r * 0.6
    return [line(poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], closed=True, r=k)),
            line(poly([(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)], closed=True, r=k)),
            line(seg(x0, y0, bx0, by0)), line(seg(x1, y0, bx1, by0)), line(seg(x1, y1, bx1, by1)),
            line(seg(x0, y1, bx0, by1))]


@icon("cylinder-net", CAT, "Net of a cylinder: a rectangle with a circle above and below",
      tags=["net", "unfolded cylinder", "surface area", "template", "papercraft", "geometry"])
def _(S):
    return [shell(rect(2.5, 8.5, 19, 7, L(S, 0, 2))), shell(circle(12, 5.5, 3)), shell(circle(12, 18.5, 3))]


@icon("cone-net", CAT, "Net of a cone: a curved fan-shaped sector with a small circle for the base",
      tags=["net", "unfolded cone", "sector", "surface area", "template", "geometry"])
def _(S):
    a, b = pt_on(12, 2.5, 12.5, 45), pt_on(12, 2.5, 12.5, 135)
    sector = f"M12 2.5L{fmt(a[0])} {fmt(a[1])}A12.5 12.5 0 0 1 {fmt(b[0])} {fmt(b[1])}Z"
    return [soft_shell(S, sector, 1.25), shell(circle(12, 18.25, 3.25))]


@icon("pyramid-net", CAT, "Net of a square pyramid: a square with a triangle folded out from each side",
      tags=["net", "unfolded pyramid", "fold lines", "template", "papercraft", "geometry"])
def _(S):
    out = [(8, 8), (12, 2.5), (16, 8), (21.5, 12), (16, 16), (12, 21.5), (8, 16), (2.5, 12)]
    return [closed(S, out, 1.25), detail(rect(8, 8, 8, 8))]


@icon("triangular-prism-net", CAT, "Net of a triangular prism: three rectangles with a triangle above and below",
      tags=["net", "unfolded prism", "fold lines", "template", "papercraft", "geometry"])
def _(S):
    h = 3 * math.sqrt(3)
    out = [(3, 8), (9, 8), (12, 8 - h), (15, 8), (21, 8), (21, 16), (15, 16), (12, 16 + h), (9, 16), (3, 16)]
    return [closed(S, out, 1.25), detail(rect(9, 8, 6, 8))]


@icon("spherical-triangle", CAT, "Sphere with a curved triangle drawn on its surface",
      tags=["spherical geometry", "great circle", "curved triangle", "non-euclidean", "sphere", "geometry"])
def _(S):
    A, B, C = (12, 5.5), (18, 15.5), (6, 15.5)
    tri = (f"M{A[0]} {A[1]}A11 11 0 0 1 {B[0]} {B[1]}A11 11 0 0 1 {C[0]} {C[1]}A11 11 0 0 1 {A[0]} {A[1]}Z")
    return [shell(circle(12, 12, 9.5)), detail(tri), pt(S, *A, 2.5), pt(S, *B, 2.5), pt(S, *C, 2.5)]


def _geodesic(R, a0, a1, cx=12, cy=12):
    """Hyperbolic line in the Poincare disk between boundary angles a0 and a1 (a1 - a0 < 180)."""
    beta = math.radians((a1 - a0) / 2)
    rho = R * math.tan(beta)
    p, q = pt_on(cx, cy, R, a0), pt_on(cx, cy, R, a1)
    return f"M{fmt(p[0])} {fmt(p[1])}A{fmt(rho)} {fmt(rho)} 0 0 0 {fmt(q[0])} {fmt(q[1])}"


@icon("poincare-disk", CAT, "Poincare disk: circle filled with curved lines meeting its edge at right angles",
      tags=["hyperbolic geometry", "poincare", "non-euclidean", "disk model", "tessellation", "geometry"])
def _(S):
    R = 9.5
    parts = [shell(circle(12, 12, R))]
    for a in (-90, 30, 150):
        parts.append(detail(_geodesic(R, a, a + 120)))
        parts.append(detail(_geodesic(R, a, a + 60)))
        parts.append(detail(_geodesic(R, a + 60, a + 120)))
        parts.append(pt(S, *pt_on(12, 12, R, a), 3.25))
    return parts


@icon("sphere-packing", CAT, "Equal balls stacked in a triangle: three, then two, then one",
      tags=["packing", "stacked balls", "cannonballs", "kepler conjecture", "spheres", "geometry"])
def _(S):
    r = 3
    parts = []
    y0 = 17
    dy = 2 * r * math.sqrt(3) / 2
    for row, n in enumerate((3, 2, 1)):
        for i in range(n):
            x = 12 + (i - (n - 1) / 2) * 2 * r
            parts.append(shell(circle(x, y0 - row * dy, r)))
    parts.append(line(seg(2.5, 21, 21.5, 21)))
    return parts


@icon("cavalieri-principle", CAT, "Two stacks of coins, one straight and one leaning, with equal volume",
      tags=["cavalieri", "equal volume", "stacked coins", "shear", "cross sections", "geometry"])
def _(S):
    ys = [3.5, 7.75, 12, 16.25, 20.5]
    parts = [shell(rect(2.5, 3.5, 7, 17, L(S, 0, 1.5)))]
    parts += [detail(seg(2.5, y, 9.5, y)) for y in ys[1:-1]]

    def xl(y):
        return 11.5 + (20.5 - y) * 3.5 / 17
    parts.append(closed(S, [(xl(20.5), 20.5), (xl(20.5) + 7, 20.5), (xl(3.5) + 7, 3.5), (xl(3.5), 3.5)], 1.5))
    parts += [detail(seg(xl(y), y, xl(y) + 7, y)) for y in ys[1:-1]]
    return parts


# ============================================================================ angles

@icon("right-angle", CAT, "Right angle: two rays meeting at 90 degrees with a square corner mark",
      tags=["90 degrees", "perpendicular", "square corner", "angle", "geometry"])
def _(S):
    return [line(poly([(4.5, 3.5), (4.5, 19.5), (20.5, 19.5)], r=S.r)),
            line(poly([(4.5, 13), (11, 13), (11, 19.5)], r=S.r * 0.4))]


@icon("obtuse-angle", CAT, "Obtuse angle: two rays spread wider than a right angle with an arc",
      tags=["obtuse", "wide angle", "more than 90 degrees", "angle", "geometry"])
def _(S):
    v, a, b = (11, 18), (3.5, 6), (21.5, 18)
    return [line(poly([a, v, b], r=S.r)), line(arc(*v, 5.5, ang(v, a), 0))]


@icon("straight-angle", CAT, "Straight angle: a straight line with a half-circle arc marking 180 degrees",
      tags=["180 degrees", "straight line", "half turn", "angle", "geometry"])
def _(S):
    y = 15.5
    return [line(seg(2.5, y, 21.5, y)), line(arc(12, y, 7, 180, 360)), pt(S, 12, y, 3.5)]


@icon("reflex-angle", CAT, "Reflex angle: a long arc sweeping around the outside of two rays",
      tags=["reflex", "more than 180 degrees", "major angle", "angle", "geometry"])
def _(S):
    v, a, b = (9.5, 13.5), (21.5, 13.5), (17.5, 4.5)
    return [line(poly([b, v, a], r=S.r)), line(arc(*v, 5.5, 0, ang(v, b)))]


@icon("complementary-angles", CAT, "Complementary angles: a right angle split in two by a middle ray",
      tags=["complementary", "adds to 90", "right angle", "angle pair", "geometry"])
def _(S):
    c = (4, 20)
    return [line(poly([(4, 3.5), c, (20.5, 20)], r=S.r)), line(seg(*c, 16.5, 7.5)),
            line(arc(*c, 6.5, -90, -45)), line(arc(*c, 11, -45, 0))]


@icon("supplementary-angles", CAT, "Supplementary angles: a ray rising from a straight line, both angles marked",
      tags=["supplementary", "adds to 180", "linear pair", "angle pair", "geometry"])
def _(S):
    v, top = (11, 18.5), (15.5, 5)
    return [line(seg(2.5, 18.5, 21.5, 18.5)), line(seg(*v, *top)),
            line(arc(*v, 5, ang(v, top), 0)), line(arc(*v, 7.5, 180, ang(v, top) + 360))]


@icon("vertical-angles", CAT, "Vertical angles: two crossing lines with matching arcs on opposite angles",
      tags=["vertically opposite", "opposite angles", "crossing lines", "angle pair", "geometry"])
def _(S):
    a = math.degrees(math.atan2(5.5, 9))
    return [line(seg(3, 6.5, 21, 17.5)), line(seg(3, 17.5, 21, 6.5)),
            line(arc(12, 12, 5, -a, a)), line(arc(12, 12, 5, 180 - a, 180 + a))]


@icon("exterior-angle", CAT, "Triangle with one side extended and the outside angle marked by an arc",
      tags=["exterior angle", "outside angle", "extended side", "triangle", "geometry"])
def _(S):
    A, B, C = (2.5, 19.5), (13.5, 19.5), (7, 5)
    return [closed(S, [A, B, C], 1.25), line(seg(*B, 21.5, 19.5)), line(arc(*B, 5, ang(B, C), 0))]


@icon("dihedral-angle", CAT, "Dihedral angle: two planes meeting along an edge like an open book, with an arc",
      tags=["dihedral", "angle between planes", "open book", "3d angle", "geometry"])
def _(S):
    top, hinge, lb, lt, rb, rt = (12, 2.5), (12, 14), (2.5, 17.5), (2.5, 6), (21.5, 17.5), (21.5, 6)
    out = [top, rt, rb, hinge, lb, lt]
    return [closed(S, out, 1.25), detail(seg(*ins(S, top, hinge, 1.2), *hinge)),
            line(arc(*hinge, 6, ang(hinge, rb) + 6, ang(hinge, lb) - 6))]


@icon("solid-angle", CAT, "Solid angle: a cone of rays from the centre of a sphere to a patch on its surface",
      tags=["steradian", "solid angle", "cone", "sphere", "3d angle", "geometry"])
def _(S):
    A, R = (4.5, 19.5), 15.5
    e1, e2 = pt_on(*A, R, -78), pt_on(*A, R, -12)
    cap = f"M{fmt(e1[0])} {fmt(e1[1])}A{fmt(R)} {fmt(R)} 0 0 1 {fmt(e2[0])} {fmt(e2[1])}"
    m = lerp(e1, e2, 0.5)
    bow = pt_on(*m, 3.2, -45 + 180)
    return [shell(f"M{fmt(A[0])} {fmt(A[1])}L{fmt(e1[0])} {fmt(e1[1])}" + cap[cap.index("A"):] + "Z"),
            detail(f"M{fmt(e1[0])} {fmt(e1[1])}Q{fmt(bow[0])} {fmt(bow[1])} {fmt(e2[0])} {fmt(e2[1])}"),
            pt(S, *A, 3.5)]


@icon("angle-of-elevation", CAT, "Angle of elevation: a sight line rising from the ground to the top of a flagpole",
      tags=["elevation", "line of sight", "trigonometry", "height", "angle", "geometry"])
def _(S):
    eye, top = (4, 19.5), (17, 4.5)
    return [line(seg(2.5, 19.5, 21.5, 19.5)), line(seg(17, 19.5, *top)),
            shell(poly([top, (21.5, 6.5), (17, 8.5)], closed=True, r=L(S, 0, 0.8))),
            line(seg(*eye, *ins(S, top, eye, 0.5))), line(arc(*eye, 7, ang(eye, top), 0))]


# ============================================================================ points, lines and planes

@icon("intersecting-lines", CAT, "Two straight lines crossing at a single marked point",
      tags=["intersection", "crossing lines", "meet", "point", "geometry"])
def _(S):
    a1, a2, b1, b2 = (2.5, 8.5), (21.5, 16), (8.5, 21.5), (15.5, 2.5)
    x = xsect(a1, a2, b1, b2)
    return [line(seg(*a1, *a2)), line(seg(*b1, *b2)), pt(S, *x, 4)]


@icon("segment-midpoint", CAT, "Line segment with its endpoints and midpoint marked, each half ticked",
      tags=["midpoint", "segment", "bisect", "half", "equal parts", "geometry"])
def _(S):
    a, b = (4.5, 19.5), (19.5, 4.5)
    return [line(seg(*a, *b)), pt(S, *a, 3.5), pt(S, *b, 3.5), pt(S, 12, 12, 3.5),
            *ticks(a, b, 1, t=0.25, half=2.5, role=line), *ticks(a, b, 1, t=0.75, half=2.5, role=line)]


@icon("collinear-points", CAT, "Three points lying on one straight line",
      tags=["collinear", "points on a line", "aligned", "straight line", "geometry"])
def _(S):
    a, b = (2.5, 17), (21.5, 7)
    return [line(seg(*a, *b))] + [pt_dir(S, *lerp(a, b, t), ang(a, b), 3.75) for t in (0.2, 0.5, 0.8)]


@icon("geometric-plane", CAT, "Flat plane drawn in perspective with a point on it",
      tags=["plane", "flat surface", "2d space", "point", "geometry"])
def _(S):
    return [closed(S, [(2, 17), (16.5, 17), (22, 8), (7.5, 8)], 1.5), pt(S, 12, 12.5, 3)]


@icon("normal-vector", CAT, "Normal vector: an arrow standing straight up from a flat plane",
      tags=["normal", "perpendicular", "surface normal", "vector", "3d", "geometry"])
def _(S):
    f = (11.5, 18.5)
    return [closed(S, [(2.5, 21.5), (15, 21.5), (21.5, 14), (9, 14)], 1.25),
            line(seg(f[0], 3.5, f[0], 14)), detail(seg(f[0], 14, *f)),
            line(poly([(8, 7), (f[0], 3.5), (15, 7)], r=S.r * 0.5))]


@icon("skew-lines", CAT, "Skew lines: two lines that pass one behind the other without meeting",
      tags=["skew", "non-intersecting", "non-parallel", "3d lines", "geometry"])
def _(S):
    a1, a2, b1, b2 = (2.5, 8.5), (21.5, 15.5), (7, 21.5), (16, 2.5)
    x = xsect(a1, a2, b1, b2)
    g = 3.25
    u = unit(b1, b2)
    return [line(seg(*a1, *a2)), line(seg(*b1, x[0] - u[0] * g, x[1] - u[1] * g)),
            line(seg(x[0] + u[0] * g, x[1] + u[1] * g, *b2))]


# ============================================================================ triangle constructions

_EQ = [(12, 3), (21.5, 19.5), (2.5, 19.5)]


@icon("triangle-medians", CAT, "Triangle with its three medians meeting at the centroid",
      tags=["median", "centroid", "centre of mass", "triangle centre", "geometry"])
def _(S):
    A, B, C = _EQ
    parts = [closed(S, _EQ, 1.5)]
    for v, p, q in ((A, B, C), (B, C, A), (C, A, B)):
        m = lerp(p, q, 0.5)
        parts.append(detail(seg(*ins(S, v, m, 1.6), *m)))
    parts.append(pt(S, 12, (3 + 19.5 * 2) / 3, 3.25))
    return parts


@icon("triangle-altitude", CAT, "Triangle with a dashed altitude dropped from the top corner to the base",
      tags=["altitude", "height", "perpendicular", "triangle", "area", "geometry"])
def _(S):
    A, B, C = (9, 3), (21.5, 19.5), (2.5, 19.5)
    return [closed(S, [A, B, C], 1.25), detail(seg(*ins(S, A, (9, 19.5), 1.6), 9, 19.5)),
            detail(poly([(9, 15.5), (13, 15.5), (13, 19.5)], r=S.r * 0.3))]


def _incircle_filled():
    body = U(P(poly(_EQ, closed=True)), ST(poly(_EQ, closed=True), 2, "butt", "miter"))
    r = 19 * math.sqrt(3) / 6
    return D(body, ST(circle(12, 19.5 - r, r - 1.1), 2))


@icon("triangle-incircle", CAT, "Triangle with a circle drawn inside touching all three sides",
      tags=["incircle", "inscribed circle", "incentre", "incenter", "triangle", "geometry"], filled=_incircle_filled)
def _(S):
    r = 19 * math.sqrt(3) / 6
    return [closed(S, _EQ, 1.5), detail(circle(12, 19.5 - r, r))]


_CIRC = [pt_on(12, 12, 9.5, a) for a in (-100, 25, 150)]


def _circum_filled():
    inner = [pt_on(12, 12, 8.1, a) for a in (-100, 25, 150)]
    return D(P(circle(12, 12, 10.5)), ST(poly(inner, closed=True), 2, "butt", "miter"), P(circle(12, 12, 1.75)))


@icon("triangle-circumcircle", CAT, "Triangle with a circle drawn around it through all three corners",
      tags=["circumcircle", "circumscribed circle", "circumcentre", "circumcenter", "triangle", "geometry"],
      filled=_circum_filled)
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(poly(_CIRC, closed=True, r=S.r * 0.4), stroke_miterlimit=1),
            pt(S, 12, 12, 3.5)]


def _tri(x, base, w, h, lean=0.3):
    return [(x, base), (x + w, base), (x + lean * w, base - h)]


@icon("similar-triangles", CAT, "A small and a large triangle of the same shape with matching angle arcs",
      tags=["similar", "similarity", "scale", "proportional", "triangles", "geometry"])
def _(S):
    t1 = [(2.5, 20.5), (9, 20.5), (2.5, 12)]
    t2 = [(11.5, 20.5), (21, 20.5), (11.5, 8)]
    a1, a2 = ang(t1[1], t1[2]), ang(t2[1], t2[2])
    return [closed(S, t1, 1.0), closed(S, t2, 1.5),
            detail(arc(*t1[1], 3.25, 186, a1 + 354)), detail(arc(*t2[1], 5, 183, a2 + 357))]


@icon("congruent-triangles", CAT, "Two identical triangles with matching tick marks on corresponding sides",
      tags=["congruent", "congruence", "identical", "equal", "triangles", "geometry"])
def _(S):
    parts = []
    t1 = [(2.5, 19.5), (10.5, 19.5), (4, 5)]
    t2 = [(x + 11, y) for x, y in t1]
    for t in (t1, t2):
        parts += [closed(S, t, 1.25), *ticks(t[1], t[2], 1, t=0.5, half=2.25)]
    return parts


@icon("thales-theorem", CAT, "Thales' theorem: a triangle in a semicircle with a right angle on the arc",
      tags=["thales", "semicircle", "right angle", "inscribed angle", "diameter", "geometry"])
def _(S):
    y, R = 17, 9.5
    a, b, p = (12 - R, y), (12 + R, y), pt_on(12, y, R, -118)
    return [shell(f"M{fmt(a[0])} {y}A{R} {R} 0 0 1 {fmt(b[0])} {y}Z"),
            detail(poly([ins(S, a, p, 1.2), p, ins(S, b, p, 1.2)], r=S.r * 0.3)),
            corner_mark(S, p, a, b, 3.5)]


# ============================================================================ circle constructions

@icon("circle-chord", CAT, "Circle with a chord joining two points on its edge",
      tags=["chord", "secant segment", "circle", "line segment", "geometry"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(seg(*pt_on(12, 12, 9.5, 195), *pt_on(12, 12, 9.5, 305))), pt(S, 12, 12, 3)]


@icon("circle-diameter", CAT, "Circle with a diameter through its centre, both ends and the centre marked",
      tags=["diameter", "centre", "center", "circle", "through the middle", "geometry"])
def _(S):
    p, q = pt_on(12, 12, 9.5, 150), pt_on(12, 12, 9.5, -30)
    return [shell(circle(12, 12, 9.5)), detail(seg(*p, *q)), pt(S, *p, 3.25), pt(S, *q, 3.25), pt(S, 12, 12, 3.25)]


@icon("tangent-circles", CAT, "Two circles of different sizes touching at a single point",
      tags=["tangent", "touching circles", "kissing circles", "point of contact", "geometry"])
def _(S):
    return [shell(circle(8.5, 12, 6)), shell(circle(18, 12, 3.5)), pt(S, 14.5, 12, 3.25)]


def _inscribed_filled():
    return D(P(circle(12, 12, 10.5)), ST(poly(regular(12, 12, 8.1, 6), closed=True), 2, "butt", "miter"),
             P(circle(12, 12, 1.5)))


@icon("inscribed-polygon", CAT, "Regular hexagon drawn inside a circle with every corner touching it",
      tags=["inscribed", "cyclic polygon", "hexagon in circle", "circumscribed", "geometry"], filled=_inscribed_filled)
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(poly(regular(12, 12, 9.4, 6), closed=True, r=S.r * 0.4), stroke_miterlimit=1),
            pt(S, 12, 12, 3)]
