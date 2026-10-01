"""TypeIcon Core: geometry (batch 003).

Solids, constructions, curves and a few classic optical illusions. Follows the conventions of
`geometry_001`: Line keeps corners sharp (miter joins) and marks points with small squares; Rounded
rounds the corners and marks points with round dots. Edges and construction lines inside a figure are
details, so the Filled style knocks them out of the solid figure.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, I, P, Part, ST, U, arc, circle, detail, dot, ellipse, icon, line, path_to_d, poly, pt_on, rect, regular, seg,
    shell, solid,
)
from geometry import fmt

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


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


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


def arrow_head(S, tip, frm, size=3.5, role=line):
    """Open chevron at tip, pointing away from frm."""
    ux, uy = unit(frm, tip)
    bx, by = tip[0] - ux * size, tip[1] - uy * size
    a = (bx - uy * size, by + ux * size)
    b = (bx + uy * size, by - ux * size)
    return role(poly([a, tip, b], r=S.r * 0.5))


def soften(region, r):
    """Round the convex corners of a boolean region by radius r (morphological opening)."""
    er = D(region, ST(path_to_d(region), 2 * r, "butt", "round"))
    return U(er, ST(path_to_d(er), 2 * r, "butt", "round"))


def soft_shell(S, d, r=1.25):
    return shell(d if S.name == "line" else path_to_d(soften(P(d), r)))


def ell_pts(cx, cy, rx, ry, a0, a1, n=12):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def ellipse_dashes(S, cx, cy, rx, ry, a0, a1, n, role=detail):
    """n dashes along an elliptical arc from angle a0 to a1 (degrees)."""
    out = []
    step = (a1 - a0) / (2 * n - 1)
    trim = 0 if S.name == "line" else step * 0.28
    for i in range(n):
        s0, s1 = a0 + 2 * i * step + trim, a0 + (2 * i + 1) * step - trim
        out.append(role(poly(ell_pts(cx, cy, rx, ry, s0, s1, 4))))
    return out


def fill_minus(sil_d, *knock):
    """Filled override helper: silhouette grown by the stroke, minus 2 px knock-out strokes."""
    sil = P(sil_d)
    sil = U(sil, ST(path_to_d(sil), 2))
    for k in knock:
        sil = D(sil, ST(k, 2))
    return sil


def rimmed(outline_pts, knock_ds, rim=1.0):
    """Filled override: solid polygon with 2 px knock-outs that stop `rim` px inside its centre line,
    so a solid rim keeps the figure in one piece."""
    d = poly(outline_pts, closed=True)
    sil = U(P(d), ST(d, 2, "butt", "miter"))
    inner = D(P(d), ST(d, 2 * rim, "butt", "miter"))
    knock = U(*[ST(k, 2) for k in knock_ds])
    return D(sil, I(knock, inner))


def shorten(a, b, d0=0.0, d1=0.0):
    """Segment a-b with d0 px trimmed from a and d1 px from b."""
    u = unit(a, b)
    return seg(a[0] + u[0] * d0, a[1] + u[1] * d0, b[0] - u[0] * d1, b[1] - u[1] * d1)


# ============================================================================ solids and blocks

def _polycube():
    s, v = 7.0, (4.0, -4.0)
    x0, y0 = 3.0, 21.0
    F = lambda i, j: (x0 + i * s, y0 - j * s)  # noqa: E731  front-face lattice point
    B = lambda i, j: add(F(i, j), v)  # noqa: E731
    outline = [F(0, 0), F(2, 0), B(2, 0), B(2, 1), B(1, 1), B(1, 2), B(0, 2), F(0, 2)]
    inner = [
        poly([F(0, 2), F(1, 2), B(1, 2)]),        # front and right edges of the top of the stacked cube
        seg(*F(1, 2), *F(1, 1)),                  # right edge of stacked cube
        poly([F(1, 1), F(2, 1), B(2, 1)]),        # top front edge and right top edge of the end cube
        seg(*F(2, 1), *F(2, 0)),                  # front right edge of the end cube
        seg(*F(1, 1), *B(1, 1)),                  # where the stacked cube meets the end cube's top
        seg(*F(0, 1), *F(1, 1)),                  # joint between the stacked and the bottom cube
        seg(*F(1, 1), *F(1, 0)),                  # joint between the two bottom cubes
    ]
    return outline, inner


def _polycube_filled():
    outline, inner = _polycube()
    return rimmed(outline, inner)


@icon("polycube", CAT, "Three equal cubes joined face to face into an L-shaped block.",
      tags=["polycube", "tricube", "cubes", "blocks", "3d", "geometry"], filled=_polycube_filled)
def _(S):
    outline, inner = _polycube()
    if S.name == "rounded":
        s, v = 7.0, (4.0, -4.0)
        F = lambda i, j: (3.0 + i * s, 21.0 - j * s)  # noqa: E731
        B = lambda i, j: add(F(i, j), v)  # noqa: E731
        # keep the round caps of edges that end on a rounded outline corner inside that corner
        inner[0] = poly([F(0, 2), F(1, 2)]) + shorten(F(1, 2), B(1, 2), 0, 1.0)
        inner[2] = poly([F(1, 1), F(2, 1)]) + shorten(F(2, 1), B(2, 1), 0, 1.0)
    return [closed(S, outline, 1.25)] + [detail(d) for d in inner]


@icon("annular-sector", CAT, "Annular sector: a curved block cut from a ring between two arcs.",
      tags=["annular sector", "ring sector", "arch segment", "curved block", "geometry"])
def _(S):
    c, R, r, a0, a1 = (12, 12), 9.5, 4.25, 172, 298
    o0, o1 = pt_on(*c, R, a0), pt_on(*c, R, a1)
    i0, i1 = pt_on(*c, r, a0), pt_on(*c, r, a1)
    d = (f"M{fmt(o0[0])} {fmt(o0[1])}A{fmt(R)} {fmt(R)} 0 0 1 {fmt(o1[0])} {fmt(o1[1])}"
         f"L{fmt(i1[0])} {fmt(i1[1])}A{fmt(r)} {fmt(r)} 0 0 0 {fmt(i0[0])} {fmt(i0[1])}Z")
    return [soft_shell(S, d, 1.25), *ellipse_dashes(S, *c, R, R, a1 + 17, a0 + 360 - 17, 5, role=line),
            *ellipse_dashes(S, *c, r, r, a1 + 38, a0 + 360 - 38, 2, role=line)]


def _extrude():
    cx, rx, ry, yt, yb = 12, 9.0, 2.7, 13.0, 19.0
    hx = [(cx + rx * math.cos(math.radians(a)), ry * math.sin(math.radians(a))) for a in range(0, 360, 60)]
    top = [(x, yt + y) for x, y in hx]
    bot = [(x, yb + y) for x, y in hx]
    # hexagon order: 0 right, 1 lower right, 2 lower left, 3 left, 4 upper left, 5 upper right
    outline = [top[3], top[4], top[5], top[0], bot[0], bot[1], bot[2], bot[3]]
    return outline, top, bot


@icon("extrude", CAT, "Extrude: a hexagonal prism rising from a flat face with an arrow pointing up.",
      tags=["extrude", "extrusion", "3d modeling", "push pull", "prism", "geometry"])
def _(S):
    outline, top, bot = _extrude()
    return [closed(S, outline, 1.0), detail(poly([top[3], top[2], top[1], top[0]], r=S.r * 0.4)),
            detail(seg(*top[2], *bot[2])), detail(seg(*top[1], *bot[1])),
            line(seg(12, 13, 12, 3)), arrow_head(S, (12, 2.5), (12, 13), 3.2)]


_PLINE = [(3, 18.5), (7.5, 7), (13, 15.5), (17, 5.5), (21, 13)]


@icon("polyline", CAT, "Polyline: an open chain of straight segments with a point at every joint.",
      tags=["polyline", "polygonal chain", "path", "vertices", "segments", "geometry"])
def _(S):
    return [line(poly(_PLINE, r=S.r * 0.5))] + [pt(S, x, y, 4.25) for x, y in _PLINE]


def _frustum():
    L_, F_, R_ = (2.5, 16.5), (12, 21), (21.5, 16.5)
    tl, tf, tr, tb = (7.5, 7.5), (12, 9.5), (16.5, 7.5), (12, 5.5)
    return L_, F_, R_, tl, tf, tr, tb


@icon("pyramid-frustum", CAT, "Square pyramid frustum: a pyramid with its top sliced off flat.",
      tags=["frustum", "truncated pyramid", "square frustum", "3d", "solid", "geometry"])
def _(S):
    L_, F_, R_, tl, tf, tr, tb = _frustum()
    return [closed(S, [L_, tl, tb, tr, R_, F_], 1.25), detail(poly([tl, tf, tr], r=S.r * 0.4)),
            detail(seg(*tf, *F_))]


# ============================================================================ curves and constructions

def _para_y(x):
    return 21 - (x - 12) ** 2 / 28


@icon("parabolic-focus", CAT, "Parallel rays bouncing off a parabola and meeting at its focus.",
      tags=["parabola", "focus", "reflector", "dish", "optics", "geometry"])
def _(S):
    f = (12, 14)
    par = f"M2.5 {fmt(_para_y(2.5))}Q12 {fmt(2 * 21 - _para_y(2.5))} 21.5 {fmt(_para_y(21.5))}"
    out = [line(par)]
    for x in (6, 18):
        hit = (x, _para_y(x))
        out.append(line(poly([(x, 2.5), hit, lerp(hit, f, 0.66)], r=S.r * 0.6)))
    out.append(pt(S, *f, 4))
    return out


@icon("vector-projection", CAT, "Vector projection: one arrow dropped at a right angle onto another.",
      tags=["vector projection", "vectors", "dot product", "component", "linear algebra", "geometry"])
def _(S):
    o, b, a = (3, 20), (21.5, 20), (15, 4.5)
    foot = (a[0], o[1])
    return [line(seg(*o, b[0] - 0.8, b[1])), arrow_head(S, b, o, 3.2),
            line(seg(*o, *lerp(o, a, 0.97))), arrow_head(S, a, o, 3.2),
            *dashes(S, (a[0], 8.5), (a[0], 14.5), 2, role=line), corner_mark(S, foot, o, a, 3.0, role=line)]


def _miura():
    xs, ys, k = [3.0, 8.5, 14.0, 19.0], [3.0, 9.0, 15.0, 21.0], 2.5
    col = lambda x: [(x + (k if j % 2 else 0), y) for j, y in enumerate(ys)]  # noqa: E731
    cols = [col(x) for x in xs]
    return cols


def _miura_outline():
    cols = _miura()
    left, right = cols[0], cols[-1]
    return [left[0], right[0]] + right[1:] + [left[-1]] + left[-2:0:-1]


def _miura_filled():
    cols = _miura()
    left, right = cols[0], cols[-1]
    ks = [poly(c) for c in cols[1:-1]] + [seg(*left[j], *right[j]) for j in (1, 2)]
    return rimmed(_miura_outline(), ks, 1.25)


@icon("miura-fold", CAT, "Miura fold: a sheet creased into a zigzag grid of parallelograms.",
      tags=["miura ori", "fold", "origami", "crease pattern", "accordion", "geometry"], filled=_miura_filled)
def _(S):
    cols = _miura()
    left, right = cols[0], cols[-1]
    out = [closed(S, [left[0], right[0]] + right[1:] + [left[-1]] + left[-2:0:-1], 1.0)]
    for c in cols[1:-1]:
        out.append(detail(poly(c, r=S.r * 0.3)))
    for j in (1, 2):
        out.append(detail(seg(*left[j], *right[j])))
    return out


def _hcyl_filled():
    sil = "M3.5 6.5A8.5 4 0 0 1 20.5 6.5V17.5A8.5 4 0 0 1 3.5 17.5Z"
    return D(fill_minus(sil, "M3.5 6.5A8.5 4 0 0 0 20.5 6.5", "M7 13V17.5"), P(ellipse(12, 6.5, 4.5, 2)))


@icon("hollow-cylinder", CAT, "Hollow cylinder: an upright tube whose top face is a ring.",
      tags=["tube", "pipe", "annular cylinder", "hollow", "3d", "geometry"], filled=_hcyl_filled)
def _(S):
    return [shell(ellipse(12, 6.5, 8.5, 4)), line("M3.5 6.5V17.5A8.5 4 0 0 0 20.5 17.5V6.5"),
            Part("dot", ellipse(12, 6.5, 4.5, 2)), detail(seg(7, 13, 7, 17.5))]


@icon("quadtree", CAT, "Quadtree: a square split into four, with one quarter split into four again.",
      tags=["quadtree", "spatial index", "subdivision", "quadrants", "data structure", "geometry"])
def _(S):
    return [shell(rect(3, 3, 18, 18, min(S.R, 2.5))), detail(seg(12, 3, 12, 21)), detail(seg(3, 12, 21, 12)),
            detail(seg(16.5, 3, 16.5, 12)), detail(seg(12, 7.5, 21, 7.5)),
            pt(S, 7.5, 7.5, 3), pt(S, 7.5, 16.5, 3), pt(S, 16.5, 16.5, 3)]


@icon("unit-cell", CAT, "Unit cell: a wireframe cube with an atom at each of its eight corners.",
      tags=["unit cell", "crystal lattice", "cubic lattice", "crystal", "chemistry", "geometry"])
def _(S):
    s, v = 11.5, (6.0, -6.0)
    f = [(4, 20), (4 + s, 20), (4 + s, 20 - s), (4, 20 - s)]
    b = [add(p, v) for p in f]
    out = [line(poly(f, closed=True)), line(poly(b, closed=True))]
    out += [line(seg(*f[i], *b[i])) for i in range(4)]
    out += [pt(S, x, y, 4.5) for x, y in f + b]
    return out


# ============================================================================ oblique solids

def _ell_tangent_from(c, a, b, apex):
    """Parameters (radians) of the two tangent points on ellipse (c, a, b) seen from apex."""
    def g(t):
        ex, ey = c[0] + a * math.cos(t), c[1] + b * math.sin(t)
        dx, dy = -a * math.sin(t), b * math.cos(t)
        return (ex - apex[0]) * dy - (ey - apex[1]) * dx
    roots = []
    n = 720
    for i in range(n):
        t0, t1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
        if g(t0) == 0 or g(t0) * g(t1) < 0:
            for _ in range(60):
                tm = (t0 + t1) / 2
                if g(t0) * g(tm) <= 0:
                    t1 = tm
                else:
                    t0 = tm
            roots.append((t0 + t1) / 2)
    return roots


_OC = ((9.5, 18.5), 7.5, 2.75, (18.5, 2.5))


def _ocone_d():
    c, a, b, apex = _OC
    t = sorted(_ell_tangent_from(c, a, b, apex))
    # visible base arc: the one passing through the bottom of the ellipse (t = 90 deg)
    t0, t1 = t
    if not (t0 < math.pi / 2 < t1):
        t0, t1 = t1, t0 + 2 * math.pi
    pts = [(c[0] + a * math.cos(t0 + (t1 - t0) * i / 20), c[1] + b * math.sin(t0 + (t1 - t0) * i / 20))
           for i in range(21)]
    return poly([apex] + pts, closed=True)


@icon("oblique-cone", CAT, "Oblique cone: a cone whose tip leans to one side of its round base.",
      tags=["oblique cone", "slanted cone", "leaning cone", "3d", "solid", "geometry"])
def _(S):
    c, a, b, apex = _OC
    return [soft_shell(S, _ocone_d(), 1.0), *dashes(S, lerp(apex, c, 0.3), lerp(apex, c, 0.82), 3), pt(S, *c, 2.5)]


_OY = ((14.5, 6), (9.5, 18), 7, 2.75)


def _ocyl_geom():
    top, bot, a, b = _OY
    vx, vy = bot[0] - top[0], bot[1] - top[1]
    t = math.atan2(-b * vx, a * vy)
    p1 = (a * math.cos(t), b * math.sin(t))
    p2 = (-p1[0], -p1[1])
    return top, bot, a, b, p1, p2, t


def _ocyl_side_d():
    top, bot, a, b, p1, p2, t = _ocyl_geom()
    # choose tangent points so that the base arc runs through the bottom of the base ellipse
    s0, s1 = (p1, p2) if p1[0] < p2[0] else (p2, p1)
    A0, A1 = add(top, s0), add(bot, s0)
    B0, B1 = add(bot, s1), add(top, s1)
    return (f"M{fmt(A0[0])} {fmt(A0[1])}L{fmt(A1[0])} {fmt(A1[1])}"
            f"A{fmt(a)} {fmt(b)} 0 0 0 {fmt(B0[0])} {fmt(B0[1])}L{fmt(B1[0])} {fmt(B1[1])}"), A0, B1


def _ocyl_filled():
    top, bot, a, b, *_ = _ocyl_geom()
    side, A0, B1 = _ocyl_side_d()
    sil = U(P(ellipse(*top, a, b)), P(side + "Z"), P(ellipse(*bot, a, b)))
    sil = U(sil, ST(path_to_d(sil), 2))
    front = f"M{fmt(A0[0])} {fmt(A0[1])}A{fmt(a)} {fmt(b)} 0 0 0 {fmt(B1[0])} {fmt(B1[1])}"
    return D(sil, ST(front, 2))


@icon("oblique-cylinder", CAT, "Oblique cylinder: a cylinder whose top is shifted sideways from its base.",
      tags=["oblique cylinder", "slanted cylinder", "leaning cylinder", "3d", "solid", "geometry"],
      filled=_ocyl_filled)
def _(S):
    top, bot, a, b, *_ = _ocyl_geom()
    side, *_ = _ocyl_side_d()
    return [shell(ellipse(*top, a, b)), line(side),
            *ellipse_dashes(S, *bot, a, b, 192, 348, 4, role=line)]


# ============================================================================ plane constructions

_CQ = [pt_on(12, 12, 9.5, a) for a in (-118, -22, 68, 172)]


def _cq_filled():
    return D(P(circle(12, 12, 10.5)), ST(poly(_CQ, closed=True), 2, "butt", "miter"))


@icon("cyclic-quadrilateral", CAT, "Cyclic quadrilateral: a four-sided shape with every corner on a circle.",
      tags=["cyclic quadrilateral", "inscribed quadrilateral", "circle", "chords", "polygon", "geometry"],
      filled=_cq_filled)
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(poly(_CQ, closed=True, r=S.r * 0.5))] + [pt(S, x, y, 3.25) for x, y in _CQ]


_TRI = [(12, 3), (21.5, 20.5), (2.5, 20.5)]


@icon("triangle-midsegment", CAT, "Triangle with a midsegment joining the midpoints of two sides.",
      tags=["midsegment", "midline", "midpoints", "triangle", "parallel", "geometry"])
def _(S):
    a, b, c = _TRI
    mb, mc = lerp(a, b, 0.5), lerp(a, c, 0.5)
    return [closed(S, _TRI, 1.5), detail(seg(*mc, *mb)), pt(S, *mc, 4), pt(S, *mb, 4)]


_CUBE = (12.5, (6.0, -6.0), (2.5, 21.0))


def _cube_pts():
    s, v, o = _CUBE
    f = [o, (o[0] + s, o[1]), (o[0] + s, o[1] - s), (o[0], o[1] - s)]  # BL BR TR TL
    b = [add(p, v) for p in f]
    return f, b


def _cube_diag_filled():
    f, b = _cube_pts()
    sil = P(poly([f[0], f[1], b[1], b[2], b[3], f[3]], closed=True))
    sil = U(sil, ST(path_to_d(sil), 2, "butt", "miter"))
    for d in (poly([f[3], f[2], f[1]]), seg(*f[2], *b[2]), seg(*f[3], *b[1])):
        sil = D(sil, ST(d, 2))
    return sil


@icon("cube-space-diagonal", CAT, "See-through cube with a space diagonal running between opposite corners.",
      tags=["space diagonal", "body diagonal", "cube", "wireframe", "3d", "geometry"], filled=_cube_diag_filled)
def _(S):
    f, b = _cube_pts()
    out = [closed(S, [f[0], f[1], b[1], b[2], b[3], f[3]], 1.0),
           detail(poly([f[3], f[2], f[1]], r=S.r * 0.4)), detail(seg(*f[2], *b[2]))]
    out += [detail(seg(*f[3], *b[1]))]
    return out


# ============================================================================ curves

_FA, _FO = 5.8, (12, 15.0)


def _folium_pts(t0, t1, n):
    a, o = _FA, _FO
    out = []
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        x = 3 * a * t / (1 + t ** 3)
        y = 3 * a * t * t / (1 + t ** 3)
        u, v = (x - y) / math.sqrt(2), (x + y) / math.sqrt(2)
        out.append((o[0] + u, o[1] - v))
    return out


def _folium_path():
    o = _FO
    tail = [p for p in _folium_pts(-0.6, 0, 12) if p[0] >= 3.5]   # left tail, ends at the origin
    half = _folium_pts(0, 1, 14)                                   # right half of the loop, origin to tip
    mir = lambda ps: [(2 * o[0] - x, y) for x, y in ps]            # noqa: E731  mirror across the axis
    return tail[:-1] + half + mir(half[::-1])[1:] + mir(tail[::-1])[1:]


@icon("folium-of-descartes", CAT, "Folium of Descartes: a leaf-shaped loop whose two tails run toward a dashed asymptote.",
      tags=["folium", "descartes", "cubic curve", "loop", "asymptote", "geometry"])
def _(S):
    return [line(poly(_folium_path())), *dashes(S, (2.5, 21.5), (21.5, 21.5), 5, role=line)]


# ============================================================================ optical illusions

_ZR, _ZX, _ZH = (4.5, 12, 19.5), (5.5, 12, 18.5), (1.35, 2.3)


def _zollner_hatches():
    out = []
    for k, y in enumerate(_ZR):
        sgn = 1 if k % 2 == 0 else -1
        dx, dy = _ZH[0] * sgn, _ZH[1]
        out += [seg(x - dx, y + dy, x + dx, y - dy) for x in _ZX]
    return out


def _zollner_filled():
    rows = U(*[ST(seg(2.5, y, 21.5, y), 3, "butt") for y in _ZR])
    return U(rows, *[ST(h, 2, "butt") for h in _zollner_hatches()])


@icon("zollner-illusion", CAT, "Zollner illusion: parallel lines crossed by slanted hatches so they look tilted.",
      tags=["zollner", "optical illusion", "parallel lines", "hatching", "perception", "geometry"],
      filled=_zollner_filled)
def _(S):
    return [line(seg(2.5, y, 21.5, y)) for y in _ZR] + [line(h) for h in _zollner_hatches()]


@icon("sander-illusion", CAT, "Sander illusion: a parallelogram split in two, whose two equal diagonals look unequal.",
      tags=["sander illusion", "sander parallelogram", "optical illusion", "diagonals", "perception", "geometry"])
def _(S):
    # big and small parallelogram side by side; diagonals A-T and T-D are equal in length
    B, T, C = (2.5, 4.5), (13.5, 4.5), (18.5, 4.5)
    A, E, D = (5.5, 19.5), (16.5, 19.5), (21.5, 19.5)
    return [closed(S, [B, C, D, A], 1.25), detail(seg(*T, *E)),
            detail(shorten(A, T, L(S, 0, 1.0))), detail(shorten(T, D, 0, L(S, 0, 1.0)))]


# ============================================================================ spherical wedge

def _sw_geom(S=None):
    """Spherical wedge tilted like a lying orange slice: skin arc, flat face rim and the straight axis edge."""
    R, f, tilt = 9.0, 4.5, 35.0
    t0 = 0 if S is None or S.name == "line" else 9  # Rounded: face rim stops short of the rounded tips
    skin = [(-R * math.sin(math.radians(a)), -R * math.cos(math.radians(a))) for a in range(0, 181, 12)]
    face = [(-f * math.sin(math.radians(a)), -R * math.cos(math.radians(a))) for a in range(t0, 181 - t0, 12)]
    if t0:
        face.append((-f * math.sin(math.radians(180 - t0)), -R * math.cos(math.radians(180 - t0))))
    c, s_ = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
    rot = lambda ps: [(x * c - y * s_, x * s_ + y * c) for x, y in ps]  # noqa: E731
    skin, face = rot(skin), rot(face)
    xs, ys = [x for x, _ in skin], [y for _, y in skin]
    dx, dy = 12 - (min(xs) + max(xs)) / 2, 12 - (min(ys) + max(ys)) / 2
    mv = lambda ps: [(x + dx, y + dy) for x, y in ps]  # noqa: E731
    return mv(skin), mv(face)


def _sw_filled():
    skin, face = _sw_geom()
    return rimmed(skin, [poly(face)], 1.0)


@icon("spherical-wedge", CAT, "Spherical wedge: an orange-slice piece of a ball with a flat half-disc face.",
      tags=["spherical wedge", "ungula", "orange slice", "sphere segment", "3d", "geometry"], filled=_sw_filled)
def _(S):
    skin, face = _sw_geom(S)
    return [soft_shell(S, poly(skin, closed=True), 1.25), detail(poly(face))]


# ============================================================================ tiling

def _dodeca(c, a):
    R = a / (2 * math.sin(math.radians(15)))
    return [pt_on(c[0], c[1], R, 15 + 30 * i) for i in range(12)]


def _clip_seg(p, q, box):
    x0, y0, x1, y1 = box
    t0, t1 = 0.0, 1.0
    dx, dy = q[0] - p[0], q[1] - p[1]
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if abs(pp) < 1e-9:
            if qq < 0:
                return None
            continue
        t = qq / pp
        if pp < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
    if t0 >= t1 - 1e-6:
        return None
    return lerp(p, q, t0), lerp(p, q, t1)


def _trunc_hex(a=3.0, box=(3.0, 3.0, 21.0, 21.0)):
    """A patch of the 3.12.12 tiling: dodecagon edges clipped to the frame (merged into chains) + gap triangles."""
    s = a * (1 + math.sqrt(3) / 1.0) * 0 + a * 2 * (1 / (2 * math.tan(math.radians(15))))  # centre spacing
    ux, uy = (s, 0.0), (s / 2, s * math.sqrt(3) / 2)
    centres = []
    for i in range(-3, 4):
        for j in range(-3, 4):
            c = (12 + i * ux[0] + j * uy[0], 12 + i * ux[1] + j * uy[1])
            if math.dist(c, (12, 12)) < 2.2 * s:
                centres.append(c)
    edges = {}
    for c in centres:
        d = _dodeca(c, a)
        for k in range(12):
            p, q = d[k], d[(k + 1) % 12]
            key = tuple(sorted([(round(p[0], 2), round(p[1], 2)), (round(q[0], 2), round(q[1], 2))]))
            edges[key] = (p, q)
    segs = []
    for p, q in edges.values():
        cs = _clip_seg(p, q, box)
        if cs:
            segs.append(cs)
    tris = []
    for c in centres:
        for ang_ in (30, 90, 150, 210, 270, 330):
            g = pt_on(c[0], c[1], s / math.sqrt(3), ang_)
            if ang_ in (30, 150, 270) or True:
                rt = a / math.sqrt(3)
                tri = [pt_on(g[0], g[1], rt, ang_ + 180 + 120 * m + 60) for m in range(3)]
                if all(box[0] <= x <= box[2] and box[1] <= y <= box[3] for x, y in tri):
                    if not any(math.dist(g, pg) < 0.5 for pg, _ in tris):
                        tris.append((g, tri))
    return [t for _, t in tris], segs


def _chains(segs):
    """Merge segments that meet end to end (only where exactly two meet) into polylines."""
    key = lambda p: (round(p[0], 2), round(p[1], 2))  # noqa: E731
    adj = {}
    for i, (p, q) in enumerate(segs):
        adj.setdefault(key(p), []).append((i, 0))
        adj.setdefault(key(q), []).append((i, 1))
    used, chains = set(), []
    for i in range(len(segs)):
        if i in used:
            continue
        used.add(i)
        ch = [segs[i][0], segs[i][1]]
        for end in (1, 0):
            while True:
                tip = ch[-1] if end == 1 else ch[0]
                nxt = [e for e in adj[key(tip)] if e[0] not in used]
                if len(adj[key(tip)]) != 2 or not nxt:
                    break
                j, side = nxt[0]
                used.add(j)
                other = segs[j][1 - side]
                if end == 1:
                    ch.append(other)
                else:
                    ch.insert(0, other)
        chains.append(ch)
    return chains


def _thex_filled():
    _, segs = _trunc_hex()
    return rimmed([(3, 3), (21, 3), (21, 21), (3, 21)], [poly(ch) for ch in _chains(segs)], 1.25)


@icon("truncated-hexagonal-tiling", CAT, "Truncated hexagonal tiling: big dodecagons with a small triangle in the gap where three meet.",
      tags=["truncated hexagonal tiling", "dodecagon", "triangle", "tessellation", "tiling", "pattern"],
      filled=_thex_filled)
def _(S):
    tris, segs = _trunc_hex()
    out = [shell(rect(3, 3, 18, 18, L(S, 0, 2)))]
    for ch in _chains(segs):
        out.append(detail(poly(ch)))
    for t in tris:
        out.append(Part("dot", poly(t, closed=True, r=L(S, 0, 0.6))))
    return out
