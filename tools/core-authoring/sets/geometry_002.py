"""TypeIcon Core: geometry (batch 002).

Constructions, graphs, curves, spirals, tilings, fractals, links and optical illusions. Follows geometry_001:
Line keeps corners sharp and marks points with small squares; Rounded rounds corners and marks points with round
dots. Figures are shells and their construction lines are details, so the Filled style knocks the lines out of a
solid figure. Tilings are drawn as one solid patch (shell) with the joints between tiles as details.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, I, LINE, P, Part, ST, U, arc, circle, detail, dot, ellipse, filled_region, icon, line, path_to_d, poly,
    pt_on, rect, regular, seg, shell, solid,
)
from geometry import fmt  # noqa: F401

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


def unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    return dx / n, dy / n


def ang(a, b):
    """Screen angle (degrees, 0 = right, 90 = down) of the direction a -> b."""
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))


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


def arrow_head(S, tip, deg, size=3.25, role=line):
    """Open arrowhead at tip pointing in screen direction deg."""
    a = pt_on(*tip, size, deg + 180 - 45)
    b = pt_on(*tip, size, deg + 180 + 45)
    return role(poly([a, tip, b], r=S.r * 0.4))


def soften(region, r):
    """Round the convex corners of a boolean region by radius r (morphological opening)."""
    er = D(region, ST(path_to_d(region), 2 * r, "butt", "round"))
    return U(er, ST(path_to_d(er), 2 * r, "butt", "round"))


def soft_shell(S, d, r=1.25):
    return shell(d if S.name == "line" else path_to_d(soften(P(d), r)))


def xform(pts, deg=0.0, s=1.0, dx=0.0, dy=0.0, cx=0.0, cy=0.0):
    """Rotate (clockwise on screen) and scale points about (cx, cy), then translate."""
    a = math.radians(deg)
    c, si = math.cos(a), math.sin(a)
    out = []
    for x, y in pts:
        x, y = (x - cx) * s, (y - cy) * s
        out.append((cx + x * c - y * si + dx, cy + x * si + y * c + dy))
    return out


def fit(pts, box=(3, 3, 21, 21)):
    """Scale and centre a point list uniformly into box (x0, y0, x1, y1)."""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    s = min((box[2] - box[0]) / max(w, 1e-9), (box[3] - box[1]) / max(h, 1e-9))
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    mx, my = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    return [(cx + (x - mx) * s, cy + (y - my) * s) for x, y in pts]


def filled_of(draw, drop=()):
    """Filled override: the standard derivation from the Line parts, leaving out parts whose index is in drop."""
    from geometry import LINE as _LINE
    parts = draw(_LINE)
    return filled_region([p for i, p in enumerate(parts) if i not in drop])


def axis_edges(rects):
    """Interior joints of axis-aligned rectangles (x0, y0, x1, y1): edge stretches shared by two tiles."""
    lines = {}
    for x0, y0, x1, y1 in rects:
        for key, a, b in ((("h", round(y0, 3)), x0, x1), (("h", round(y1, 3)), x0, x1),
                          (("v", round(x0, 3)), y0, y1), (("v", round(x1, 3)), y0, y1)):
            lines.setdefault(key, []).append((a, b))
    out = []
    for (kind, k), ivs in lines.items():
        cuts = sorted({round(v, 3) for iv in ivs for v in iv})
        runs = []
        for a, b in zip(cuts, cuts[1:]):
            m = (a + b) / 2
            if sum(1 for p, q in ivs if p <= m <= q) >= 2:
                if runs and abs(runs[-1][1] - a) < 1e-6:
                    runs[-1][1] = b
                else:
                    runs.append([a, b])
        out += [(kind, k, a, b) for a, b in runs]
    return [seg(a, k, b, k) if kind == "h" else seg(k, a, k, b) for kind, k, a, b in out]


def tiles(S, polys, soft=1.0, role=detail):
    """Solid patch of tiles: the union outline as a shell, every fully shared edge as a detail."""
    region = U(*[P(poly(p, closed=True)) for p in polys])
    count = {}
    for p in polys:
        for a, b in zip(p, p[1:] + p[:1]):
            k = tuple(sorted([(round(a[0], 2), round(a[1], 2)), (round(b[0], 2), round(b[1], 2))]))
            count[k] = count.get(k, 0) + 1
    parts = [soft_shell(S, path_to_d(region), soft)]
    parts += [role(seg(*a, *b)) for (a, b), v in count.items() if v > 1]
    return parts


def clipseg(p, q, box):
    """Clip segment p-q to box (x0, y0, x1, y1); None when outside."""
    x0, y0, x1, y1 = box
    t0, t1 = 0.0, 1.0
    dx, dy = q[0] - p[0], q[1] - p[1]
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if abs(pp) < 1e-12:
            if qq < 0:
                return None
            continue
        t = qq / pp
        if pp < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
    if t0 >= t1:
        return None
    return lerp(p, q, t0), lerp(p, q, t1)


def gapped_circle(c, r, gaps, half):
    """Circle as open arcs, leaving a gap of +/- half degrees around each angle in gaps."""
    gs = sorted(g % 360 for g in gaps)
    out = []
    for i, g in enumerate(gs):
        nxt = gs[(i + 1) % len(gs)] + (360 if i == len(gs) - 1 else 0)
        out.append(arc(*c, r, g + half, nxt - half))
    return out


def crossings(c1, r1, c2, r2):
    d = math.dist(c1, c2)
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(max(r1 * r1 - a * a, 0))
    ux, uy = (c2[0] - c1[0]) / d, (c2[1] - c1[1]) / d
    m = (c1[0] + ux * a, c1[1] + uy * a)
    return [(m[0] - uy * h, m[1] + ux * h), (m[0] + uy * h, m[1] - ux * h)]


# ============================================================================ polygon constructions

_HEX_FLAT = regular(12, 12, 9.5, 6, 0)


@icon("polygon-apothem", CAT, "Regular hexagon with its apothem drawn from the centre to the middle of a side.",
      tags=["apothem", "hexagon", "regular polygon", "inradius", "perpendicular", "polygon area"])
def _(S):
    foot = (12, 12 + 9.5 * math.cos(math.radians(30)))
    return [closed(S, _HEX_FLAT, 2.0), detail(seg(12, 12, *foot)), pt(S, 12, 12, 3.5)]


_HEX_PT = regular(12, 12, 9.5, 6, -90)


@icon("polygon-diagonals", CAT, "Hexagon with every diagonal from one corner fanning across it.",
      tags=["diagonals", "hexagon", "triangulation", "polygon", "fan", "interior angles"])
def _(S):
    top = _HEX_PT[0]
    return [closed(S, _HEX_PT, 2.0)] + [detail(seg(*top, *_HEX_PT[k])) for k in (2, 3, 4)]


def _osc_curve():
    pts = []
    for i in range(-40, 41):
        d = 9.5 * i / 40
        y = 19.5 - d * d / 12 - d ** 4 / 900
        if y >= 3:
            pts.append((12 + d, y))
    return pts


@icon("osculating-circle", CAT, "Circle nestled in the bend of a curve, with a radius drawn to the point where they touch.",
      tags=["osculating circle", "curvature", "radius of curvature", "kissing circle", "calculus", "differential geometry"])
def _(S):
    r = 6.0
    c = (12, 19.5 - r)
    return [line(poly(_osc_curve())), shell(circle(*c, r - 0.4)), detail(seg(c[0], c[1], c[0], 19.5 - 1.6)),
            pt(S, *c, 2.75)]


def _sq_circle_filled():
    s = 8.5 * math.sqrt(math.pi) / 2
    sq = rect(12 - s, 12 - s, 2 * s, 2 * s)
    return U(ST(circle(12, 12, 8.5), 2.5), ST(sq, 2.5), D(P(sq), P(circle(12, 12, 8.5))))


@icon("squaring-the-circle", CAT, "Circle and square of equal area drawn over each other on the same centre.",
      tags=["squaring the circle", "quadrature", "equal area", "pi", "impossible construction", "compass and straightedge"],
      filled=_sq_circle_filled)
def _(S):
    s = 8.5 * math.sqrt(math.pi) / 2
    return [line(rect(12 - s, 12 - s, 2 * s, 2 * s, L(S, 0, 1.5))), line(circle(12, 12, 8.5))]


def _apollo():
    R = 9.5
    r = R / (1 + 2 / math.sqrt(3))
    inner = [pt_on(12, 12, R - r, a) for a in (-90, 30, 150)]
    kR, ki = -1 / R, 1 / r
    k4 = kR + 2 * ki + 2 * math.sqrt(kR * ki * 2 + ki * ki)
    r4 = 1 / k4
    small = [pt_on(12, 12, R - r4, a) for a in (90, 210, 330)]
    return R, r, inner, r4, small


def _apollo_filled():
    R, r, inner, r4, small = _apollo()
    return U(ST(circle(12, 12, R), 2.5), *[P(circle(x, y, r - 1.1)) for x, y in inner],
             *[P(circle(x, y, 1.45)) for x, y in small])


@icon("apollonian-gasket", CAT, "Circle packed with three touching circles and smaller circles filling the gaps.",
      tags=["apollonian gasket", "circle packing", "fractal", "tangent circles", "descartes theorem", "kissing circles"],
      filled=_apollo_filled)
def _(S):
    R, r, inner, r4, small = _apollo()
    parts = [line(circle(12, 12, R))]
    parts += [line(circle(x, y, r)) for x, y in inner]
    parts += [pt(S, x, y, 3.0) if S.name == "line" else dot(x, y, 1.3) for x, y in small]
    return parts


@icon("nested-squares", CAT, "Square with a turned square inside touching its midpoints, and another square inside that.",
      tags=["nested squares", "inscribed square", "midpoints", "recursion", "square in square", "pattern"])
def _(S):
    k = L(S, 0, 1.0)
    return [shell(rect(3, 3, 18, 18, L(S, 0, 2))),
            detail(poly([(12, 3), (21, 12), (12, 21), (3, 12)], closed=True, r=k)),
            detail(poly([(7.5, 7.5), (16.5, 7.5), (16.5, 16.5), (7.5, 16.5)], closed=True, r=k))]


@icon("curve-stitching", CAT, "Two lines at a right angle joined by straight threads whose envelope forms a curve.",
      tags=["curve stitching", "string art", "envelope", "parabola", "straight lines", "mathematical art"])
def _(S):
    parts = [line(poly([(3.5, 2.5), (3.5, 20.5), (21.5, 20.5)], r=S.r))]
    for t in (0.25, 0.5, 0.75):
        parts.append(line(seg(3.5, 2.5 + 18 * t, 3.5 + 18 * t, 20.5)))
    return parts


# ============================================================================ transformations

_TRI = [(3, 21), (11, 21), (3, 13)]


@icon("geometric-translation", CAT, "Triangle slid to a new position, with an arrow from a corner to the matching corner.",
      tags=["translation", "slide", "transformation", "shift", "vector", "rigid motion"])
def _(S):
    t2 = [(x + 10, y - 10) for x, y in _TRI]
    return [closed(S, _TRI, 1.5), closed(S, t2, 1.5),
            line(seg(5.5, 10.5, 10.9, 5.1)), arrow_head(S, (11.1, 4.9), -45, 3.0)]


@icon("geometric-dilation", CAT, "Small triangle and an enlarged copy, with rays from the centre of enlargement through their corners.",
      tags=["dilation", "enlargement", "scale factor", "similar figures", "transformation", "centre of dilation"])
def _(S):
    c = (12, 13.5)
    big = regular(*c, 9.5, 3)
    small = regular(*c, 5.0, 3)
    parts = [closed(S, big, 1.5), detail(poly(small, closed=True, r=L(S, 0, 0.8)))]
    parts += [detail(seg(*p, *lerp(p, q, 0.8))) for p, q in zip(small, big)]
    parts.append(pt(S, *c, 2.25))
    return parts


@icon("glide-reflection", CAT, "Flag shapes stepping along a dashed line, flipping to the other side at every step.",
      tags=["glide reflection", "symmetry", "transformation", "frieze pattern", "mirror", "footprints"])
def _(S):
    parts = dashes(S, (2.5, 12), (21.5, 12), 5, role=line)
    for i, x in enumerate((3, 9.25, 15.5)):
        if i % 2 == 0:
            tri = [(x, 9.25), (x + 5.5, 9.25), (x, 3.5)]
        else:
            tri = [(x, 14.75), (x + 5.5, 14.75), (x, 20.5)]
        parts.append(closed(S, tri, 1.0))
    return parts


# ============================================================================ curves and graphs

def _limacon(n=90):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        r = 1 + 3.0 * math.cos(t)
        pts.append((r * math.cos(t), r * math.sin(t)))
    return pts


@icon("limacon", CAT, "Limacon: a looping closed curve with a smaller loop inside it, joined at one point.",
      tags=["limacon", "limacon of pascal", "polar curve", "inner loop", "snail curve", "polar graph"])
def _(S):
    box = (2.5, 3.5, 21.5, 20.5)
    raw = _limacon()
    pts = fit(raw + [(0, 0)], box)
    pole = pts[-1]
    return [line(poly(pts[:-1], closed=True)), pt(S, *pole, 4.0) if S.name == "line" else dot(*pole, 2.3)]


def _involute(r, t1, n=48):
    return [(r * (math.cos(t) + t * math.sin(t)), r * (math.sin(t) - t * math.cos(t)))
            for t in (t1 * i / n for i in range(n + 1))]


@icon("involute-curve", CAT, "Involute: a taut line unwinding from a circle, its free end tracing a widening curve.",
      tags=["involute", "unwinding string", "gear tooth", "spiral", "evolute", "curve"])
def _(S):
    r, t1 = 3.0, 1.45 * math.pi
    raw = _involute(r, t1)
    tan = (r * math.cos(t1), r * math.sin(t1))
    allp = xform(raw + [(0, 0), tan], 180)
    xs, ys = [p[0] for p in allp], [p[1] for p in allp]
    dx, dy = 12 - (min(xs) + max(xs)) / 2, 12 - (min(ys) + max(ys)) / 2
    allp = [(x + dx, y + dy) for x, y in allp]
    pts, c, tp = allp[:-2], allp[-2], allp[-1]
    end = pts[-1]
    return [shell(circle(*c, r - 0.5)), line(poly(pts)), line(seg(*tp, *end)), pt(S, *end, 3.0)]


@icon("cubic-curve", CAT, "S-shaped cubic curve rising through the crossing of two axes and flattening in the middle.",
      tags=["cubic", "cubic function", "x cubed", "polynomial", "inflection point", "function graph"])
def _(S):
    pts = []
    for i in range(-30, 31):
        u = i / 30
        pts.append((12 + 8.5 * u, 12 - 9 * (u ** 3 + 0.55 * u) / 1.55))
    return [detail(seg(2.5, 12, 21.5, 12)), detail(seg(12, 2.5, 12, 21.5)), line(poly(pts))]


@icon("absolute-value-graph", CAT, "Graph of absolute value: a sharp V with its point at the origin of crossed axes.",
      tags=["absolute value", "modulus", "v graph", "abs function", "piecewise", "function graph"])
def _(S):
    return [detail(seg(2.5, 19, 21.5, 19)), detail(seg(4, 2.5, 4, 21.5)),
            line(poly([(7, 5.5), (14, 19), (21, 5.5)], r=S.r * 0.6), stroke_miterlimit="6")]


def _tan_pts(x0, x1, xa, period, n=24):
    out = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        u = (x - xa) / period * math.pi
        y = 12 - 3.0 * math.tan(u)
        if 2.5 <= y <= 21.5:
            out.append((x, y))
    return out


@icon("tangent-graph", CAT, "Graph of the tangent function: steep repeating curves between dashed vertical asymptotes.",
      tags=["tangent", "tan", "trigonometry", "asymptote", "periodic function", "trig graph"])
def _(S):
    per = 11.0
    parts = [detail(seg(2.5, 12, 21.5, 12))]
    for x in (6.5, 17.5):
        parts += dashes(S, (x, 2.5), (x, 21.5), 4, role=detail)
    parts.append(line(poly(_tan_pts(8.3, 15.7, 12, per))))
    return parts


def _clothoid(smax, n=110):
    pts, x, y = [], 0.0, 0.0
    ds = 2 * smax / n
    s = -smax
    for _ in range(n + 1):
        pts.append((x, y))
        x += math.cos(s * s) * ds
        y += math.sin(s * s) * ds
        s += ds
    return pts


@icon("euler-spiral", CAT, "Euler spiral: an S-shaped curve with a straight middle that coils tighter at each end.",
      tags=["euler spiral", "clothoid", "cornu spiral", "transition curve", "track curve", "spiral"])
def _(S):
    pts = [(x, -y) for x, y in _clothoid(2.45)]
    pts = fit(xform(pts, 10), (2.5, 2.5, 21.5, 21.5))
    return [line(poly(pts))]


def _fermat(tmax, sign, n=40):
    a = 9.3 / math.sqrt(tmax)
    return [(12 + sign * a * math.sqrt(t) * math.cos(t), 12 + sign * a * math.sqrt(t) * math.sin(t))
            for t in (tmax * i / n for i in range(n + 1))]


@icon("fermat-spiral", CAT, "Fermat spiral: two spiral arms winding out of one centre, each between the turns of the other.",
      tags=["fermat spiral", "parabolic spiral", "double spiral", "spiral", "polar curve", "sunflower spiral"])
def _(S):
    tm = 1.6 * math.pi
    a, b = _fermat(tm, 1), _fermat(tm, -1)
    return [line(poly(list(reversed(a)) + b[1:])), pt(S, 12, 12, 2.5)]


@icon("square-spiral", CAT, "Square spiral: straight segments turning at right angles and growing longer at each turn.",
      tags=["square spiral", "rectangular spiral", "right angles", "maze", "spiral", "labyrinth"])
def _(S):
    p = (12, 12)
    pts = [p]
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for i, ln in enumerate((4, 4, 8, 8, 12, 12, 16, 16, 16)):
        dx, dy = dirs[i % 4]
        p = (p[0] + dx * ln, p[1] + dy * ln)
        pts.append(p)
    return [line(poly(pts, r=S.r))]


def _theodorus(n=12, u=3.0):
    pts = [(u, 0.0)]
    x, y = u, 0.0
    for _ in range(n):
        r = math.hypot(x, y)
        x, y = x - y / r * u, y + x / r * u
        pts.append((x, y))
    return pts


@icon("spiral-of-theodorus", CAT, "Spiral of Theodorus: right triangles joined around one point, growing like a snail shell.",
      tags=["spiral of theodorus", "square root spiral", "right triangles", "snail spiral", "pythagoras", "irrational numbers"])
def _(S):
    raw = [(-x, y) for x, y in _theodorus()]
    pts = fit(raw + [(0, 0)], (2.5, 2.5, 21.5, 21.5))
    o, outer = pts[-1], pts[:-1]
    parts = [shell(poly([o] + outer, closed=True, r=L(S, 0, 0.5)))]
    parts += [detail(seg(*lerp(o, p, 0.4), *p)) for p in outer[1:-1]]
    return parts


def _phyllo(rs):
    out = []
    n = 24
    for i in range(1, n + 1):
        r = 1.95 * math.sqrt(i)
        x, y = pt_on(12, 12, r, i * 137.508)
        out.append((x, y, rs(i / n)))
    return out


@icon("phyllotaxis-spiral", CAT, "Dots set in crossing spiral arms around a centre, like the seed head of a sunflower.",
      tags=["phyllotaxis", "sunflower", "golden angle", "fibonacci", "seed pattern", "spiral pattern"],
      filled=lambda: U(*[P(circle(x, y, r)) for x, y, r in _phyllo(lambda k: 0.75 + 0.6 * k)]))
def _(S):
    return [pt(S, x, y, 2 * r) if S.name == "line" else dot(x, y, r + 0.1)
            for x, y, r in _phyllo(lambda k: 0.55 + 0.5 * k)]


@icon("tractrix", CAT, "Tractrix: a curve falling from a vertical line and sweeping out toward a horizontal line.",
      tags=["tractrix", "pursuit curve", "dog curve", "asymptote", "pseudosphere", "towing curve"])
def _(S):
    a = 15.0
    pts = []
    for i in range(0, 41):
        t = 2.6 * i / 40
        x = 5 + a * (t - math.tanh(t))
        y = 20 - a / math.cosh(t)
        if x <= 21.5:
            pts.append((x, y))
    t = 0.8
    p = (5 + a * (t - math.tanh(t)), 20 - a / math.cosh(t))
    foot = (p[0] + (20 - p[1]) * math.sinh(t), 20)
    return [line(poly([(5, 2.5), (5, 20), (21.5, 20)], r=S.r)), line(poly(pts)),
            detail(seg(*p, *foot)), pt(S, *foot, 3.0)]


def _nephroid(n=80):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x = 3 * math.cos(t) - math.cos(3 * t)
        y = 3 * math.sin(t) - math.sin(3 * t)
        pts.append((x, y))
    return pts


@icon("nephroid", CAT, "Nephroid: a kidney-shaped closed curve with two cusps pointing inward from its sides.",
      tags=["nephroid", "kidney curve", "epicycloid", "cusps", "caustic", "plane curve"])
def _(S):
    pts = fit(_nephroid(), (2.5, 3, 21.5, 21))
    return [soft_shell(S, poly(pts, closed=True), 0.9)]


def _epicycloid(k=5, n=120):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x = (k + 1) * math.cos(t) - math.cos((k + 1) * t)
        y = (k + 1) * math.sin(t) - math.sin((k + 1) * t)
        pts.append((x, y))
    return pts


@icon("epicycloid", CAT, "Epicycloid: a curve with five sharp cusps traced by a circle rolling around a fixed circle.",
      tags=["epicycloid", "roulette curve", "cusps", "spirograph", "rolling circle", "plane curve"])
def _(S):
    s = 9.5 / 7
    pts = xform(_epicycloid(), -90, s, 12, 12)
    return [soft_shell(S, poly(pts, closed=True), 0.8), detail(circle(12, 12, 5 * s - 1.8))]


def _cassini(n=96, ratio=1.12):
    c = 1.0
    b = ratio * c
    pts = []
    for i in range(n):
        th = 2 * math.pi * i / n
        c2 = math.cos(2 * th)
        r2 = c * c * c2 + math.sqrt(c ** 4 * c2 * c2 + b ** 4 - c ** 4)
        r = math.sqrt(max(r2, 0))
        pts.append((r * math.cos(th), r * math.sin(th)))
    return pts


@icon("cassini-oval", CAT, "Cassini oval: a peanut-shaped closed curve pinched in the middle, with a focus in each lobe.",
      tags=["cassini oval", "peanut curve", "foci", "quartic curve", "lemniscate", "plane curve"])
def _(S):
    raw = _cassini()
    pts = fit(raw + [(-1, 0), (1, 0)], (2.5, 3, 21.5, 21))
    return [shell(poly(pts[:-2], closed=True)), pt(S, *pts[-2], 2.75), pt(S, *pts[-1], 2.75)]


@icon("full-angle", CAT, "Full angle: a ray from a point with an arrow sweeping all the way round it, 360 degrees.",
      tags=["full angle", "360 degrees", "complete angle", "full turn", "revolution", "round angle"])
def _(S):
    c = (12, 12)
    tip = pt_on(*c, 8.5, 338)
    return [line(seg(12, 12, 21.5, 12)), line(arc(*c, 8.5, 16, 338)), arrow_head(S, tip, 338 + 95, 3.25),
            pt(S, *c, 3.25)]


def tiles(S, polys, soft=1.0, role=detail):
    """Solid patch of tiles: the union outline as a shell, every shared edge as a detail."""
    region = U(*[P(poly(p, closed=True)) for p in polys])
    count = {}
    for p in polys:
        for a, b in zip(p, p[1:] + p[:1]):
            k = tuple(sorted([(round(a[0], 2), round(a[1], 2)), (round(b[0], 2), round(b[1], 2))]))
            count[k] = count.get(k, 0) + 1
    parts = [soft_shell(S, path_to_d(region), soft)]
    parts += [role(seg(*a, *b)) for (a, b), v in count.items() if v > 1]
    return parts


def _penrose():
    phi = (1 + math.sqrt(5)) / 2
    k = 9.5 / (1 + phi)
    c = (12, 12.9)
    O = c
    Dp = [pt_on(*c, k, -90 + 72 * i) for i in range(5)]
    A = [pt_on(*c, k * phi, -54 + 72 * i) for i in range(5)]
    K = [pt_on(*c, k * (1 + phi), -90 + 72 * i) for i in range(5)]
    darts = [[O, A[i - 1], Dp[i], A[i]] for i in range(5)]
    kites = [[Dp[i], A[i - 1], K[i], A[i]] for i in range(5)]
    return darts + kites


@icon("penrose-tiling", CAT, "Penrose tiling: kite and dart tiles meeting around a five-pointed star",
      tags=["penrose tiling", "kites and darts", "aperiodic", "quasicrystal", "five-fold", "tiling"])
def _(S):
    return tiles(S, _penrose(), 0.8)


def _rhombille():
    r = 5.2
    out = []
    for cx, cy in ((12 - 4.5, 15.9), (12 + 4.5, 15.9), (12, 15.9 - 7.8)):
        V = regular(cx, cy, r, 6)
        C = (cx, cy)
        out += [[C, V[5], V[0], V[1]], [C, V[1], V[2], V[3]], [C, V[3], V[4], V[5]]]
    return out


@icon("rhombille-tiling", CAT, "Rhombille tiling: hexagons split into three rhombuses so they read as stacked cubes",
      tags=["rhombille", "tumbling blocks", "cube pattern", "rhombus", "optical illusion", "tiling"])
def _(S):
    return tiles(S, _rhombille(), 0.8)


def _oct(cx, cy, h=4.5):
    a = 2 * h / (1 + math.sqrt(2))
    return [(cx - a / 2, cy - h), (cx + a / 2, cy - h), (cx + h, cy - a / 2), (cx + h, cy + a / 2),
            (cx + a / 2, cy + h), (cx - a / 2, cy + h), (cx - h, cy + a / 2), (cx - h, cy - a / 2)]


@icon("octagon-square-tiling", CAT, "Octagon and square tiling: four octagons with a small square in the gap between them",
      tags=["truncated square tiling", "octagons", "squares", "floor tiles", "pattern", "tiling"])
def _(S):
    h = 4.5
    a = 2 * h / (1 + math.sqrt(2))
    octs = [_oct(x, y, h) for y in (7.5, 16.5) for x in (7.5, 16.5)]
    sq = [(12, 12 - a / 2), (12 + a / 2, 12), (12, 12 + a / 2), (12 - a / 2, 12)]
    return tiles(S, octs + [sq], 2.2)


def _lines3(d, box=(3, 3, 21, 21), c=(12, 12)):
    out = []
    for deg in (0, 60, 120):
        ux, uy = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        nx, ny = -uy, ux
        for off in (-d, d):
            p = (c[0] + nx * off - ux * 30, c[1] + ny * off - uy * 30)
            q = (c[0] + nx * off + ux * 30, c[1] + ny * off + uy * 30)
            out.append((p, q))
    return out


def _clipseg(p, q, box):
    x0, y0, x1, y1 = box
    t0, t1 = 0.0, 1.0
    dx, dy = q[0] - p[0], q[1] - p[1]
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if pp == 0:
            if qq < 0:
                return None
            continue
        t = qq / pp
        if pp < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
    if t0 >= t1:
        return None
    return lerp(p, q, t0), lerp(p, q, t1)


@icon("trihexagonal-tiling", CAT, "Trihexagonal tiling: hexagons separated by small triangles in a woven star lattice",
      tags=["trihexagonal", "kagome", "hexagons", "triangles", "lattice", "tiling"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, L(S, 0, 2)))]
    for p, q in _lines3(3.4):
        cs = _clipseg(p, q, (3, 3, 21, 21))
        if cs:
            parts.append(detail(seg(*cs[0], *cs[1])))
    return parts


@icon("truchet-tiles", CAT, "Truchet tiles: a grid of square tiles with quarter-circle arcs joining into winding paths",
      tags=["truchet", "quarter circles", "tile pattern", "generative art", "maze", "tiling"])
def _(S):
    n, u = 3, 6.0
    flip = [[0, 1, 0], [1, 1, 0], [0, 0, 1]]
    parts = [shell(rect(3, 3, 18, 18, L(S, 0, 1.5)))]
    for j in range(n):
        for i in range(n):
            x, y = 3 + i * u, 3 + j * u
            if flip[j][i]:
                parts += [detail(arc(x + u, y, u / 2, 90, 180)), detail(arc(x, y + u, u / 2, 270, 360))]
            else:
                parts += [detail(arc(x, y, u / 2, 0, 90)), detail(arc(x + u, y + u, u / 2, 180, 270))]
    return parts


@icon("islamic-geometric-pattern", CAT, "Eight-pointed star set in a square with straps running from its points to the frame",
      tags=["islamic pattern", "eight-pointed star", "girih", "arabesque", "rosette", "geometric pattern"])
def _(S):
    star = [pt_on(12, 12, 7.0 if i % 2 == 0 else 3.9, -90 + i * 22.5) for i in range(16)]
    parts = [shell(rect(3, 3, 18, 18, L(S, 0, 2))), detail(poly(star, closed=True, r=L(S, 0, 0.6)))]
    for i in range(0, 16, 2):
        p = star[i]
        a = -90 + i * 22.5
        q = pt_on(12, 12, 9 / max(abs(math.cos(math.radians(a))), abs(math.sin(math.radians(a)))), a)
        parts.append(detail(seg(*p, *q)))
    return parts


@icon("fish-scale-pattern", CAT, "Fish scale pattern: rows of overlapping scallops stacked in offset layers",
      tags=["fish scale", "scallop", "shingles", "seigaiha", "overlapping circles", "pattern"])
def _(S):
    r = 4.5
    parts = [shell(rect(3, 3, 18, 18, L(S, 0, 2)))]
    for k in range(5):
        y = 3 + r * k
        for j in range(-1, 4):
            x = 3 + 2 * r * j + r * (k % 2)
            a0, a1 = 0, 180
            pts = [pt_on(x, y, r, a0 + (a1 - a0) * t / 24) for t in range(25)]
            pts = [p for p in pts if 3 <= p[0] <= 21 and 3 <= p[1] <= 21]
            if len(pts) >= 2:
                parts.append(detail(poly(pts)))
    return parts


@icon("basketweave-pattern", CAT, "Basketweave pattern: pairs of bars alternating between horizontal and vertical",
      tags=["basketweave", "parquet", "weave", "brick paving", "checkerboard", "pattern"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, L(S, 0, 2))), detail(seg(12, 3, 12, 21)), detail(seg(3, 12, 21, 12))]
    parts += [detail(seg(3, 7.5, 12, 7.5)), detail(seg(16.5, 3, 16.5, 12)),
              detail(seg(7.5, 12, 7.5, 21)), detail(seg(12, 16.5, 21, 16.5))]
    return parts


@icon("pentomino", CAT, "Pentomino: five equal squares joined edge to edge into a block shape",
      tags=["pentomino", "polyomino", "five squares", "tiling puzzle", "block", "geometry"])
def _(S):
    u = 6.0
    cells = [(1, 0), (2, 0), (0, 1), (1, 1), (1, 2)]
    polys = [[(3 + i * u, 3 + j * u), (3 + (i + 1) * u, 3 + j * u), (3 + (i + 1) * u, 3 + (j + 1) * u),
              (3 + i * u, 3 + (j + 1) * u)] for i, j in cells]
    return tiles(S, polys, 1.2)


@icon("hexaflexagon", CAT, "Hexaflexagon: a folded paper hexagon split into six triangles with every other face shaded",
      tags=["hexaflexagon", "flexagon", "paper folding", "hexagon", "puzzle", "geometry"])
def _(S):
    V = regular(12, 12, 9.5, 6, -90)
    parts = [closed(S, V, 2.0)] + [detail(seg(*V[i], *V[i + 3])) for i in range(3)]
    for i in (0, 2, 4):
        a, b = V[i], V[i + 1]
        g = [((a[0] + b[0] + 12) / 3), ((a[1] + b[1] + 12) / 3)]
        tri = [lerp(g, p, 1.0) for p in [lerp(g, a, 0.42), lerp(g, b, 0.42), lerp(g, (12, 12), 0.42)]]
        parts.append(Part("dot", poly(tri, closed=True)))
    return parts


def _dragon(n):
    t = []
    for _ in range(n):
        t = t + [1] + [-x for x in reversed(t)]
    x = y = 0
    d = 0
    pts = [(0, 0)]
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for k in [0] + t:
        d = (d + k) % 4
        x, y = x + dirs[d][0], y + dirs[d][1]
        pts.append((x, y))
    return pts


def _chamfer(pts, c=0.3):
    """Cut every corner of a unit-grid path so it never touches itself where two corners meet."""
    out = [pts[0]]
    for a, b, n in zip(pts, pts[1:], pts[2:]):
        out += [lerp(b, a, c), lerp(b, n, c)]
    out.append(pts[-1])
    return out


@icon("dragon-curve", CAT, "Dragon curve: a fractal line of right-angle turns folding into a curled dragon shape",
      tags=["dragon curve", "heighway dragon", "paper folding", "fractal", "space-filling curve", "geometry"])
def _(S):
    raw = _dragon(4)
    pts = fit(_chamfer(raw, L(S, 0.25, 0.4)), (2.5, 2.5, 21.5, 21.5))
    return [line(poly(pts, r=S.r * 0.4))]


@icon("cantor-set", CAT, "Cantor set: stacked bars, each row the one above with every middle third removed",
      tags=["cantor set", "cantor dust", "middle third", "fractal", "set theory", "geometry"])
def _(S):
    parts = []
    rows = [[(0.0, 1.0)]]
    for _ in range(3):
        nxt = []
        for a, b in rows[-1]:
            w = (b - a) / 3
            nxt += [(a, a + w), (b - w, b)]
        rows.append(nxt)
    x0, w = 2.5, 19.0
    cap = L(S, 0, 1.0)
    for k, row in enumerate(rows[:3]):
        y = 6 + k * 6
        for a, b in row:
            xa, xb = x0 + a * w + cap, x0 + b * w - cap
            if xb - xa < 0.05:
                xb = xa + 0.05
            parts.append(line(seg(xa, y, xb, y)))
    return parts


@icon("menger-sponge", CAT, "Menger sponge: a cube with a square hole punched through the middle of each face",
      tags=["menger sponge", "fractal cube", "sierpinski cube", "holes", "3d fractal", "geometry"])
def _(S):
    V = regular(12, 12, 9.5, 6)
    C = (12, 12)
    faces = [[C, V[5], V[0], V[1]], [C, V[1], V[2], V[3]], [C, V[3], V[4], V[5]]]
    parts = [shell(poly(V, closed=True, r=L(S, 0, 2))),
             detail(poly([V[1], C, V[5]], r=S.r * 0.5)), detail(seg(*C, *V[3]))]
    for f in faces:
        g = ((f[0][0] + f[2][0]) / 2, (f[0][1] + f[2][1]) / 2)
        hole = [lerp(g, p, 0.36) for p in f]
        parts.append(Part("dot", poly(hole, closed=True, r=L(S, 0, 0.5))))
    return parts


def _ptree(depth=2):
    squares, tris = [], []

    def grow(a, b, d):
        # square on segment a-b (outward to the left of a->b in screen coords)
        ux, uy = b[0] - a[0], b[1] - a[1]
        nx, ny = uy, -ux
        c, e = (b[0] + nx, b[1] + ny), (a[0] + nx, a[1] + ny)
        squares.append([a, b, c, e])
        if d == 0:
            return
        m = ((e[0] + c[0]) / 2 + nx / 2, (e[1] + c[1]) / 2 + ny / 2)
        tris.append([e, c, m])
        grow(e, m, d - 1)
        grow(m, c, d - 1)

    grow((9, 21), (15, 21), depth)
    return squares, tris


@icon("pythagoras-tree", CAT, "Pythagoras tree: squares stacked on right triangles, branching into smaller squares",
      tags=["pythagoras tree", "fractal tree", "squares", "right triangle", "recursion", "geometry"])
def _(S):
    sq, tr = _ptree(2)
    allp = [p for poly_ in sq + tr for p in poly_]
    xs, ys = [p[0] for p in allp], [p[1] for p in allp]
    s = min(19 / (max(xs) - min(xs)), 18.5 / (max(ys) - min(ys)))
    cx = (max(xs) + min(xs)) / 2
    tf = [[(12 + (x - cx) * s, 21 + (y - 21) * s) for x, y in p] for p in sq + tr]
    return tiles(S, tf, 0.6)


def _carpet_holes():
    u = 20 / 3
    holes = [(2 + u, 2 + u, u)]
    for j in range(3):
        for i in range(3):
            if i == 1 and j == 1:
                continue
            v = u / 3
            holes.append((2 + i * u + v, 2 + j * u + v, v))
    return holes


def _carpet_filled():
    return D(P(rect(1, 1, 22, 22)), *[P(rect(x, y, w, w)) for x, y, w in _carpet_holes()])


@icon("sierpinski-carpet", CAT, "Sierpinski carpet: a square with its middle ninth removed and the same done to every square left",
      tags=["sierpinski carpet", "fractal", "square", "self-similar", "recursion", "geometry"], filled=_carpet_filled)
def _(S):
    parts = [shell(rect(2, 2, 20, 20, L(S, 0, 1.5)))]
    for x, y, w in _carpet_holes():
        parts.append(Part("dot", rect(x, y, w, w, L(S, 0, min(1.0, w / 3)))))
    return parts


@icon("h-tree-fractal", CAT, "H tree: an H shape with smaller H shapes at each of its tips, two levels deep",
      tags=["h tree", "h-fractal", "fractal", "branching", "circuit layout", "geometry"])
def _(S):
    parts = []
    L1, L2 = 12.0, 12 / math.sqrt(2)
    parts.append(line(seg(12 - L1 / 2, 12, 12 + L1 / 2, 12)))
    for x in (12 - L1 / 2, 12 + L1 / 2):
        parts.append(line(seg(x, 12 - L2 / 2, x, 12 + L2 / 2)))
        for y in (12 - L2 / 2, 12 + L2 / 2):
            parts.append(line(seg(x - L1 / 4, y, x + L1 / 4, y)))
            for xx in (x - L1 / 4, x + L1 / 4):
                parts.append(line(seg(xx, y - L2 / 4, xx, y + L2 / 4)))
    return parts


def _gapped_circle(c, r, gaps, half):
    """Circle as open arcs, leaving a gap of +/- half degrees around each angle in gaps."""
    gs = sorted(g % 360 for g in gaps)
    out = []
    for i, g in enumerate(gs):
        nxt = gs[(i + 1) % len(gs)] + (360 if i == len(gs) - 1 else 0)
        out.append(arc(*c, r, g + half, nxt - half))
    return out


def _crossings(c1, r1, c2, r2):
    d = math.dist(c1, c2)
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(r1 * r1 - a * a)
    ux, uy = (c2[0] - c1[0]) / d, (c2[1] - c1[1]) / d
    m = (c1[0] + ux * a, c1[1] + uy * a)
    return [(m[0] - uy * h, m[1] + ux * h), (m[0] + uy * h, m[1] - ux * h)]


@icon("borromean-rings", CAT, "Borromean rings: three interlocked circles, each passing over one ring and under the other",
      tags=["borromean rings", "three rings", "interlocking", "knot theory", "link", "geometry"])
def _(S):
    r = 5.6
    cs = [pt_on(12, 12.6, 4.0, a) for a in (-90, 30, 150)]
    gaps = {0: [], 1: [], 2: []}
    for over, under in ((0, 1), (1, 2), (2, 0)):
        for p in _crossings(cs[over], r, cs[under], r):
            gaps[under].append(ang(cs[under], p))
    parts = []
    for i, c in enumerate(cs):
        parts += [line(d) for d in _gapped_circle(c, r, gaps[i], 21)]
    return parts


@icon("hopf-link", CAT, "Hopf link: two circles linked together like a pair of chain links",
      tags=["hopf link", "linked rings", "two rings", "knot theory", "chain link", "geometry"])
def _(S):
    r = 6.3
    a, b = (8.3, 12), (15.7, 12)
    top, bot = sorted(_crossings(a, r, b, r), key=lambda p: p[1])
    parts = [line(d) for d in _gapped_circle(a, r, [ang(a, bot)], 20)]
    parts += [line(d) for d in _gapped_circle(b, r, [ang(b, top)], 20)]
    return parts


def _arm(n=40):
    pts = []
    for i in range(n + 1):
        t = i / n
        th = math.radians(90 + 330 * t)
        r = 5.0 * (1 - 0.72 * t)
        pts.append((r * math.cos(th), -5.0 + r * math.sin(th)))
    return pts


@icon("triskelion", CAT, "Triskelion: three curved arms spiralling out from a shared centre",
      tags=["triskelion", "triskele", "triple spiral", "three arms", "celtic spiral", "symbol"])
def _(S):
    parts = []
    for k in range(3):
        pts = xform(_arm(), 120 * k, dx=12, dy=12.5)
        parts.append(line(poly(pts)))
    return parts


def _pac(c, r, facing, mouth=60):
    a0, a1 = facing + mouth / 2, facing - mouth / 2 + 360
    p0, p1 = pt_on(*c, r, a0), pt_on(*c, r, a1)
    return f"M{fmt(c[0])} {fmt(c[1])}L{fmt(p0[0])} {fmt(p0[1])}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(p1[0])} {fmt(p1[1])}Z"


@icon("kanizsa-triangle", CAT, "Kanizsa triangle: three notched discs whose gaps suggest a triangle that is not drawn",
      tags=["kanizsa triangle", "illusory contour", "optical illusion", "gestalt", "subjective contour", "perception"])
def _(S):
    c = (12, 13.2)
    V = regular(*c, 7.2, 3)
    return [soft_shell(S, _pac(v, 3.4, ang(v, c)), 0.7) for v in V]


@icon("muller-lyer-illusion", CAT, "Muller-Lyer illusion: two equal lines, one with arrowheads and one with outward fins",
      tags=["muller-lyer", "optical illusion", "arrows", "length illusion", "perception", "psychology"])
def _(S):
    k = S.r * 0.5
    return [line(seg(6.5, 7, 17.5, 7)), line(seg(6.5, 17, 17.5, 17)),
            line(poly([(9.5, 4), (6.5, 7), (9.5, 10)], r=k)), line(poly([(14.5, 4), (17.5, 7), (14.5, 10)], r=k)),
            line(poly([(3.5, 14), (6.5, 17), (3.5, 20)], r=k)), line(poly([(20.5, 14), (17.5, 17), (20.5, 20)], r=k))]


@icon("ebbinghaus-illusion", CAT, "Ebbinghaus illusion: two equal circles, one ringed by big circles and one by small ones",
      tags=["ebbinghaus illusion", "titchener circles", "size illusion", "optical illusion", "perception", "psychology"])
def _(S):
    a, b = (8, 8), (16.8, 16.8)
    parts = [shell(circle(*a, 1.5)), shell(circle(*b, 1.5))]
    for k in range(4):
        parts.append(shell(circle(*pt_on(*a, 5.0, 45 + 90 * k), 1.6)))
    for k in range(6):
        parts.append(pt(S, *pt_on(*b, 3.7, 30 + 60 * k), 1.9))
    return parts


@icon("cafe-wall-illusion", CAT, "Cafe wall illusion: rows of dark and light bricks shifted so the straight lines look tilted",
      tags=["cafe wall illusion", "munsterberg illusion", "bricks", "tilted lines", "optical illusion", "perception"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, L(S, 0, 1.5))), detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15))]
    for k, off in enumerate((0.0, 2.25, 4.5)):
        y0, y1 = 3 + 6 * k + (0 if k == 0 else 1), 3 + 6 * (k + 1) - (0 if k == 2 else 1)
        for j in range(-1, 3):
            x0 = 3 + off + 6 * j
            xa, xb = max(3.0, x0), min(21.0, x0 + 3)
            if xb - xa > 0.9:
                parts.append(Part("dot", rect(xa, y0, xb - xa, y1 - y0)))
    return parts


@icon("hering-illusion", CAT, "Hering illusion: two straight parallel lines crossing a fan of rays so they seem to bow",
      tags=["hering illusion", "bowing lines", "radiating lines", "optical illusion", "perception", "psychology"])
def _(S):
    parts = [line(seg(7.5, 2.5, 7.5, 21.5)), line(seg(16.5, 2.5, 16.5, 21.5))]
    for a in (0, 32, 62, 118, 148):
        p, q = pt_on(12, 12, 2.6, a), pt_on(12, 12, 10.5, a)
        cs = _clipseg(p, q, (2.5, 2.5, 21.5, 21.5))
        p2, q2 = pt_on(12, 12, 2.6, a + 180), pt_on(12, 12, 10.5, a + 180)
        cs2 = _clipseg(p2, q2, (2.5, 2.5, 21.5, 21.5))
        parts += [detail(seg(*cs[0], *cs[1])), detail(seg(*cs2[0], *cs2[1]))]
    return parts


@icon("spherical-coordinates", CAT, "Sphere with a point on its surface, the radius to it and the angle from the vertical axis",
      tags=["spherical coordinates", "polar angle", "azimuth", "radius", "3d coordinates", "geometry"])
def _(S):
    c = (12, 12)
    p = (17.6, 6.2)
    return [shell(circle(*c, 9.5)), detail("M2.5 12A9.5 3.2 0 0 0 21.5 12"), detail(seg(*c, 12, 2.5)),
            detail(seg(*c, *p)), detail(arc(*c, 4.2, -90, ang(c, p) - 2)), pt(S, *p, 3.0)]


@icon("orthographic-views", CAT, "Front, top and side views of a stepped block laid out in an L",
      tags=["orthographic projection", "multiview", "technical drawing", "front view", "plan view", "drafting"])
def _(S):
    k = L(S, 0, 1.2)
    front = [(3, 13), (7, 13), (7, 16.5), (11, 16.5), (11, 21), (3, 21)]
    return [shell(poly(front, closed=True, r=k)),
            shell(rect(3, 3, 8, 6, L(S, 0, 1))), detail(seg(7, 3, 7, 9)),
            shell(rect(14, 13, 7, 8, L(S, 0, 1))), detail(seg(14, 16.5, 21, 16.5))]


_DPTS = [(4, 4.5), (13, 3), (20.5, 7), (9, 12), (16.5, 14), (3.5, 17.5), (11.5, 20.5), (20.5, 20)]
_DEDGES = [(0, 3), (1, 3), (1, 4), (2, 4), (3, 4), (3, 5), (3, 6), (4, 6), (4, 7)]


@icon("delaunay-triangulation", CAT, "Delaunay triangulation: scattered points joined by straight lines into a mesh of triangles",
      tags=["delaunay", "triangulation", "triangle mesh", "point cloud", "computational geometry", "mesh"])
def _(S):
    hull = [_DPTS[i] for i in (0, 1, 2, 7, 6, 5)]
    parts = [shell(poly(hull, closed=True, r=L(S, 0, 0.6)))]
    parts += [detail(seg(*_DPTS[a], *_DPTS[b])) for a, b in _DEDGES]
    parts += [pt(S, *_DPTS[3], 3.25), pt(S, *_DPTS[4], 3.25)]
    return parts


@icon("convex-hull", CAT, "Convex hull: a polygon stretched around a scatter of points like a rubber band",
      tags=["convex hull", "rubber band", "point set", "boundary", "computational geometry", "polygon"])
def _(S):
    hull = [(4, 9), (10, 3.5), (19.5, 5.5), (21, 15), (14, 20.5), (4.5, 18)]
    parts = [shell(poly(hull, closed=True, r=L(S, 0, 2.5)))]
    parts += [pt(S, x, y, 3.0) for x, y in ((9, 10.5), (15, 10), (11, 15.5), (16.5, 15))]
    return parts


def _rf(x):
    return 16 - 0.05 * (x - 4) ** 2


@icon("riemann-sum", CAT, "Riemann sum: a curve on axes with a row of rectangles under it whose tops touch the curve",
      tags=["riemann sum", "rectangles", "integral", "approximation", "area", "calculus"])
def _(S):
    xs = [5.5, 10, 14.5, 19]
    bars = [[(a, _rf(a)), (b, _rf(a)), (b, 20), (a, 20)] for a, b in zip(xs, xs[1:])]
    curve = [(x / 4, _rf(x / 4)) for x in range(18, 86)]
    curve = [p for p in curve if p[1] >= 2.5]
    parts = [line(poly([(3, 3), (3, 20), (5.5, 20)], r=S.r)), line(seg(19, 20, 21.5, 20))]
    parts += tiles(S, bars, 0.6)
    parts.append(line(poly(curve)))
    return parts


def _af(x):
    return 11 - 5 * math.sin((x - 3) / 18 * math.pi * 1.4)


@icon("area-under-curve", CAT, "Area under a curve: the region between a curve and the horizontal axis shaded in",
      tags=["area under curve", "definite integral", "integration", "shaded region", "calculus", "graph"])
def _(S):
    x0, x1 = 7.0, 17.5
    top = [(x0 + (x1 - x0) * i / 24, _af(x0 + (x1 - x0) * i / 24)) for i in range(25)]
    region = top + [(x1, 20), (x0, 20)]
    curve = [(x / 4, _af(x / 4)) for x in range(18, 87)]
    parts = [line(poly([(3, 3), (3, 20), (x0, 20)], r=S.r)), line(seg(x1, 20, 21.5, 20)), line(poly(curve)),
             shell(poly(region, closed=True, r=L(S, 0, 0.8)))]
    for x in (10.5, 14):
        parts.append(detail(seg(x, _af(x) + 2.2, x, 17.8)))
    return parts


@icon("function-mapping-diagram", CAT, "Mapping diagram: arrows from points in one oval to points in another",
      tags=["mapping diagram", "function", "domain", "range", "relation", "set theory"])
def _(S):
    parts = [shell(ellipse(5.5, 12, 3.5, 9)), shell(ellipse(18.5, 12, 3.5, 9))]
    left, right = [(5.5, 7), (5.5, 12), (5.5, 17)], [(18.5, 8.5), (18.5, 15.5)]
    parts += [pt(S, *p, 2.5) for p in left + right]
    for a, b in ((0, 0), (1, 0), (2, 1)):
        p, q = left[a], right[b]
        s, e = lerp(p, q, 0.2), lerp(p, q, 0.8)
        parts += [line(seg(*s, *e)), arrow_head(S, e, ang(p, q), 2.4)]
    return parts


@icon("sphere-in-cylinder", CAT, "Sphere fitting exactly inside a cylinder, touching its top, bottom and sides",
      tags=["sphere in cylinder", "archimedes", "inscribed sphere", "volume ratio", "cylinder", "geometry"])
def _(S):
    if S.name == "line":
        return [shell(ellipse(12, 5, 8, 2.5)), line("M4 5V19A8 2.5 0 0 0 20 19V5"), detail(circle(12, 12.6, 6.4))]
    return [shell(ellipse(12, 5, 8, 2.5)), line("M4 5V18.2Q4 21.5 12 21.5T20 18.2V5"), detail(circle(12, 12.6, 6.4))]


def _rhombi(a=4.4):
    H = regular(12, 12, a, 6, -90)
    tiles_ = [H]
    ns = []
    for i in range(6):
        p, q = H[i], H[(i + 1) % 6]
        mx, my = (p[0] + q[0]) / 2 - 12, (p[1] + q[1]) / 2 - 12
        m = math.hypot(mx, my)
        n = (mx / m * a, my / m * a)
        ns.append(n)
        tiles_.append([p, q, (q[0] + n[0], q[1] + n[1]), (p[0] + n[0], p[1] + n[1])])
    for i in range(6):
        p = H[i]
        n0, n1 = ns[i - 1], ns[i]
        tiles_.append([p, (p[0] + n0[0], p[1] + n0[1]), (p[0] + n1[0], p[1] + n1[1])])
    return tiles_


@icon("rhombitrihexagonal-tiling", CAT, "Rhombitrihexagonal tiling: a hexagon ringed by alternating squares and triangles",
      tags=["rhombitrihexagonal", "hexagon", "squares", "triangles", "archimedean tiling", "tiling"])
def _(S):
    return tiles(S, _rhombi(), 0.8)


def _merge(segs):
    """Merge collinear axis-aligned segments; returns list of (p, q)."""
    hs, vs = {}, {}
    for (x1, y1), (x2, y2) in segs:
        if abs(y1 - y2) < 1e-6:
            hs.setdefault(round(y1, 3), []).append(tuple(sorted((x1, x2))))
        else:
            vs.setdefault(round(x1, 3), []).append(tuple(sorted((y1, y2))))
    out = []
    for key, ivs, horiz in [(k, v, True) for k, v in hs.items()] + [(k, v, False) for k, v in vs.items()]:
        ivs.sort()
        cur = list(ivs[0])
        merged = []
        for a, b in ivs[1:]:
            if a <= cur[1] + 1e-6:
                cur[1] = max(cur[1], b)
            else:
                merged.append(cur)
                cur = [a, b]
        merged.append(cur)
        for a, b in merged:
            out.append(((a, key), (b, key)) if horiz else ((key, a), (key, b)))
    return out


@icon("pythagorean-tiling", CAT, "Pythagorean tiling: large and small squares interlocking in a pinwheel paving",
      tags=["pythagorean tiling", "pinwheel tiling", "hopscotch", "two squares", "paving", "tiling"])
def _(S):
    A, B = 6.0, 3.0
    box = (3, 3, 21, 21)
    segs = []
    for m in range(-4, 6):
        for n in range(-4, 6):
            ox, oy = 1.5 + m * A - n * B, 1 + m * B + n * A
            for (x, y, w) in ((ox, oy, A), (ox + A, oy, B)):
                c = [(x, y), (x + w, y), (x + w, y + w), (x, y + w)]
                segs += list(zip(c, c[1:] + c[:1]))
    parts = [shell(rect(3, 3, 18, 18, L(S, 0, 1.5)))]
    for p, q in _merge(segs):
        cs = _clipseg(p, q, (3.01, 3.01, 20.99, 20.99))
        if cs and math.dist(*cs) > 0.8:
            parts.append(detail(seg(*cs[0], *cs[1])))
    return parts


@icon("vicsek-fractal", CAT, "Vicsek fractal: a plus-shaped cross of five small crosses",
      tags=["vicsek fractal", "box fractal", "cross", "plus", "self-similar", "geometry"])
def _(S):
    e = L(S, 0, 1.0)
    parts = []
    for cx, cy in ((12, 12), (6, 12), (18, 12), (12, 6), (12, 18)):
        parts += [line(seg(cx - 3 + e, cy, cx + 3 - e, cy)), line(seg(cx, cy - 3 + e, cx, cy + 3 - e))]
    return parts


def _euler_filled():
    return U(ST(circle(9.75, 9.75, 7.0), 2.5), P(circle(8.25, 11.25, 3.4)), P(circle(18.5, 18.5, 3.75)),
             P(circle(13.0, 6.6, 1.3)))


@icon("euler-diagram", CAT, "Euler diagram: a large circle holding a smaller circle, with a third circle standing apart.",
      tags=["euler diagram", "subset", "set theory", "sets", "disjoint sets", "containment", "logic diagram"],
      filled=_euler_filled)
def _(S):
    c = (9.75, 9.75)
    return [shell(circle(*c, 7.0)), shell(circle(8.25, 11.25, 2.75)), shell(circle(18.5, 18.5, 2.75)),
            pt(S, 13.0, 6.6, 2.25)]


def _venn3():
    r = 5.25
    cs = [(12, 8.5), (8.25, 15), (15.75, 15)]
    core = I(I(P(circle(*cs[0], r)), P(circle(*cs[1], r))), P(circle(*cs[2], r)))
    return r, cs, core


def _venn3_filled():
    r, cs, core = _venn3()
    return U(*[ST(circle(*c, r), 2.5) for c in cs], core)


def _venn3(d=6.4):
    r = 5.75
    cs = [(12, 12.5 - d / math.sqrt(3)), (12 - d / 2, 12.5 + d / (2 * math.sqrt(3))), (12 + d / 2, 12.5 + d / (2 * math.sqrt(3)))]
    core = I(I(P(circle(*cs[0], r)), P(circle(*cs[1], r))), P(circle(*cs[2], r)))
    return r, cs, core


def _venn3_filled():
    r, cs, core = _venn3()
    return U(*[ST(circle(*c, r), 2.5) for c in cs], core)


@icon("triple-venn-diagram", CAT, "Three overlapping circles with the region they all share filled in.",
      tags=["venn diagram", "three sets", "intersection", "set theory", "overlap", "common region", "logic"],
      filled=_venn3_filled)
def _(S):
    r, cs, core = _venn3(6.4 if S.name == "line" else 5.6)
    return [line(circle(*c, r)) for c in cs] + [solid(path_to_d(core))]


def _tri_dots(r):
    s = 3.3
    h = s * 0.866
    base = 12 + h
    out = []
    for n, xc in ((1, 3.2), (2, 9.0), (3, 17.5)):
        for row in range(n):
            for k in range(row + 1):
                out.append((xc + (k - row / 2) * s, base - (n - 1 - row) * h))
    return out


@icon("triangular-numbers", CAT, "Dots stacked into growing triangles of one, three and six.",
      tags=["triangular numbers", "figurate numbers", "dot triangle", "number pattern", "sequence", "dot pattern"],
      filled=lambda: U(*[P(circle(x, y, 1.5)) for x, y in _tri_dots(0)]))
def _(S):
    return [pt(S, x, y, 2.3) if S.name == "line" else dot(x, y, 1.3) for x, y in _tri_dots(0)]


@icon("polyiamond", CAT, "Polyiamond: four equal triangles joined edge to edge into a slanted zigzag strip.",
      tags=["polyiamond", "tetriamond", "triangle tiling", "triangles", "polyform", "puzzle", "tessellation"])
def _(S):
    h = math.sqrt(3) / 2
    B = [(0, h), (1, h), (2, h)]
    T = [(0.5, 0), (1.5, 0), (2.5, 0)]
    tris = [[B[0], B[1], T[0]], [T[0], T[1], B[1]], [B[1], B[2], T[1]], [T[1], T[2], B[2]]]
    flat = [p for t in tris for p in t]
    rot = xform(flat, -28, 1.0, 0, 0, 1.25, h / 2)
    fitted = fit(rot, (2.5, 2.5, 21.5, 21.5))
    polys = [fitted[i * 3:i * 3 + 3] for i in range(4)]
    return tiles(S, polys, 0.9)


@icon("lattice-polygon", CAT, "Polygon drawn on a square grid of dots with every corner sitting on a dot.",
      tags=["lattice polygon", "pick's theorem", "grid", "geoboard", "integer coordinates", "dot grid", "area"])
def _(S):
    xs = [4.5, 10, 15.5, 21]
    verts = [(4.5, 15.5), (10, 4.5), (21, 10), (15.5, 15.5)]
    parts = [closed(S, verts, 1.5)]
    for x in xs:
        for y in xs:
            if (x, y) in verts:
                continue
            near = min(abs((b[0] - a[0]) * (a[1] - y) - (a[0] - x) * (b[1] - a[1])) / math.dist(a, b)
                       for a, b in zip(verts, verts[1:] + verts[:1]))
            if near < 2.4:
                continue
            parts.append(pt(S, x, y, 1.9) if S.name == "line" else dot(x, y, 1.05))
    return parts


def _fev(S):
    k = L(S, 0, 0.9)
    sil = [(3, 9), (9, 3), (21, 3), (21, 15), (15, 21), (3, 21)]
    return [shell(poly(sil, closed=True, r=L(S, 0, 1.5))),
            detail(poly([(3, 9), (15, 9), (21 - k, 3 + k)], r=S.r * 0.5)), detail(seg(15, 9, 15, 21)),
            solid(poly([(3, 9), (9, 3), (21, 3), (15, 9)], closed=True)),
            pt(S, 3, 21, 3.5)]
@icon("faces-edges-vertices", CAT, "Cube with its top face shaded, its edges drawn and one corner marked with a dot.",
      tags=["faces edges vertices", "cube", "polyhedron", "solid geometry", "3d shape", "euler formula", "vertex"],
      filled=lambda: filled_region([p for i, p in enumerate(_fev(LINE)) if i != 3]))
def _(S):
    return _fev(S)


@icon("conical-spiral", CAT, "Conical spiral: a curve winding up around a cone, wide at the base and narrowing to the top.",
      tags=["conical spiral", "cone helix", "3d spiral", "helix", "spiral", "space curve", "cone"])
def _(S):
    parts = [shell("M12 2.5L3 18.5A9 3.2 0 0 0 21 18.5Z")]
    for u0 in (0.12, 0.52):
        pts = []
        for i in range(25):
            t = i / 24
            u = u0 + 0.2 * t
            w = 9 * (1 - u)
            pts.append((12 - w * math.cos(math.pi * t), 18.5 - 16 * u + 3.2 * (1 - u) * math.sin(math.pi * t)))
        parts.append(detail(poly(pts)))
    return parts


_HATS = [
    [(0.0, 0.0), (-1.5, -0.866), (-1.0, -1.7321), (1.0, -1.7321), (1.5, -0.866), (3.0, -1.7321), (4.5, -0.866),
     (4.0, 0.0), (3.0, 0.0), (3.0, 1.7321), (1.5, 2.5981), (1.0, 1.7321), (0.0, 1.7321)],
    [(6.0, 0.0), (7.5, -0.866), (8.0, 0.0), (7.0, 1.7321), (6.0, 1.7321), (6.0, 3.4641), (4.5, 4.3301),
     (4.0, 3.4641), (4.5, 2.5981), (3.0, 1.7321), (3.0, 0.0), (4.0, 0.0), (4.5, -0.866)],
    [(3.0, -5.1962), (4.5, -6.0622), (5.0, -5.1962), (4.0, -3.4641), (3.0, -3.4641), (3.0, -1.7321),
     (1.5, -0.866), (1.0, -1.7321), (1.5, -2.5981), (0.0, -3.4641), (0.0, -5.1962), (1.0, -5.1962),
     (1.5, -6.0622)],
    [(6.0, -3.4641), (6.0, -5.1962), (7.0, -5.1962), (8.0, -3.4641), (7.5, -2.5981), (9.0, -1.7321),
     (9.0, 0.0), (8.0, 0.0), (7.5, -0.866), (6.0, 0.0), (4.5, -0.866), (5.0, -1.7321), (4.5, -2.5981)],
]


_HATS = [
    [(0.0, 0.0), (-1.5, -0.866), (-1.0, -1.7321), (1.0, -1.7321), (1.5, -0.866), (3.0, -1.7321), (4.5, -0.866),
     (4.0, 0.0), (3.0, 0.0), (3.0, 1.7321), (1.5, 2.5981), (1.0, 1.7321), (0.0, 1.7321)],
    [(6.0, 0.0), (7.5, -0.866), (8.0, 0.0), (7.0, 1.7321), (6.0, 1.7321), (6.0, 3.4641), (4.5, 4.3301),
     (4.0, 3.4641), (4.5, 2.5981), (3.0, 1.7321), (3.0, 0.0), (4.0, 0.0), (4.5, -0.866)],
    [(3.0, -5.1962), (4.5, -6.0622), (5.0, -5.1962), (4.0, -3.4641), (3.0, -3.4641), (3.0, -1.7321),
     (1.5, -0.866), (1.0, -1.7321), (1.5, -2.5981), (0.0, -3.4641), (0.0, -5.1962), (1.0, -5.1962),
     (1.5, -6.0622)],
    [(6.0, -3.4641), (6.0, -5.1962), (7.0, -5.1962), (8.0, -3.4641), (7.5, -2.5981), (9.0, -1.7321),
     (9.0, 0.0), (8.0, 0.0), (7.5, -0.866), (6.0, 0.0), (4.5, -0.866), (5.0, -1.7321), (4.5, -2.5981)],
]


_HAT_KITES = [
    [(0.0, 0.0), (1.5, -0.866), (2.0, 0.0), (1.5, 0.866)],
    [(0.0, 0.0), (1.5, 0.866), (1.0, 1.7321), (0.0, 1.7321)],
    [(0.0, 0.0), (-1.5, -0.866), (-1.0, -1.7321), (-0.0, -1.7321)],
    [(0.0, 0.0), (-0.0, -1.7321), (1.0, -1.7321), (1.5, -0.866)],
    [(3.0, 1.7321), (1.5, 2.5981), (1.0, 1.7321), (1.5, 0.866)],
    [(3.0, 1.7321), (1.5, 0.866), (2.0, 0.0), (3.0, 0.0)],
    [(3.0, -1.7321), (4.5, -0.866), (4.0, 0.0), (3.0, 0.0)],
    [(3.0, -1.7321), (3.0, 0.0), (2.0, 0.0), (1.5, -0.866)],
]


_HAT_KITES = [
    [(0.0, 0.0), (1.5, -0.866), (2.0, 0.0), (1.5, 0.866)],
    [(0.0, 0.0), (1.5, 0.866), (1.0, 1.7321), (0.0, 1.7321)],
    [(0.0, 0.0), (-1.5, -0.866), (-1.0, -1.7321), (-0.0, -1.7321)],
    [(0.0, 0.0), (-0.0, -1.7321), (1.0, -1.7321), (1.5, -0.866)],
    [(3.0, 1.7321), (1.5, 2.5981), (1.0, 1.7321), (1.5, 0.866)],
    [(3.0, 1.7321), (1.5, 0.866), (2.0, 0.0), (3.0, 0.0)],
    [(3.0, -1.7321), (4.5, -0.866), (4.0, 0.0), (3.0, 0.0)],
    [(3.0, -1.7321), (3.0, 0.0), (2.0, 0.0), (1.5, -0.866)],
]


@icon("aperiodic-monotile", CAT, "Aperiodic monotile: the hat, a single thirteen-sided shape that can tile the plane without ever repeating.",
      tags=["aperiodic monotile", "hat tile", "einstein tile", "polykite", "tiling", "non repeating", "tessellation"])
def _(S):
    pts = fit([p for q in _HAT_KITES for p in q], (2.5, 4.5, 21.5, 19.5))
    region = U(*[P(poly(pts[i * 4:i * 4 + 4], closed=True)) for i in range(len(_HAT_KITES))])
    return [soft_shell(S, path_to_d(region), 0.7)]


_CAIRO = [
    [(-0.866, 0), (0.866, 0), (0.866, -1), (0, -1.5), (-0.866, -1)],
    [(0.866, 0.0), (-0.866, 0.0), (-0.866, 1.0), (0.0, 1.5), (0.866, 1.0)],
    [(-0.866, -1.0), (-2.5981, -1.0), (-2.5981, 0.0), (-1.7321, 0.5), (-0.866, 0.0)],
    [(0.866, 1.0), (2.5981, 1.0), (2.5981, 0.0), (1.7321, -0.5), (0.866, 0.0)],
    [(1.7321, -2.5), (-0.0, -2.5), (0.0, -1.5), (0.866, -1.0), (1.7321, -1.5)],
    [(-0.0, -2.5), (-1.7321, -2.5), (-1.7321, -1.5), (-0.866, -1.0), (-0.0, -1.5)],
]


_CAIRO = [
    [(-0.866, 0), (0.866, 0), (0.866, -1), (0, -1.5), (-0.866, -1)],
    [(0.866, 0.0), (-0.866, 0.0), (-0.866, 1.0), (0.0, 1.5), (0.866, 1.0)],
    [(-0.866, -1.0), (-2.5981, -1.0), (-2.5981, 0.0), (-1.7321, 0.5), (-0.866, 0.0)],
    [(0.866, 1.0), (2.5981, 1.0), (2.5981, 0.0), (1.7321, -0.5), (0.866, 0.0)],
    [(1.7321, -2.5), (-0.0, -2.5), (0.0, -1.5), (0.866, -1.0), (1.7321, -1.5)],
    [(-0.0, -2.5), (-1.7321, -2.5), (-1.7321, -1.5), (-0.866, -1.0), (-0.0, -1.5)],
]


def _inside(p, poly_pts):
    x, y = p
    c = False
    for (x1, y1), (x2, y2) in zip(poly_pts, poly_pts[1:] + poly_pts[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


@icon("cairo-pentagonal-tiling", CAT, "Cairo tiling: irregular pentagons paired at right angles, like the paving of a Cairo street.",
      tags=["cairo tiling", "pentagonal tiling", "pentagons", "street paving", "tessellation", "pattern", "floor tiles"])
def _(S):
    allp = fit([p for q in _CAIRO for p in q], (3, 3, 21, 21))
    polys = [allp[i * 5:i * 5 + 5] for i in range(len(_CAIRO))]
    parts = tiles(S, polys, 1.0, role=lambda d: None)
    unit = min(math.dist(a, b) for p in polys for a, b in zip(p, p[1:] + p[:1]))
    shared = {}
    for i, p in enumerate(polys):
        for a, b in zip(p, p[1:] + p[:1]):
            if math.dist(a, b) > unit * 1.2:
                continue
            m = lerp(a, b, 0.5)
            nx, ny = -(b[1] - a[1]), b[0] - a[0]
            n = math.hypot(nx, ny)
            for sgn in (1, -1):
                q = (m[0] + sgn * nx / n * 0.3, m[1] + sgn * ny / n * 0.3)
                if any(_inside(q, o) for j, o in enumerate(polys) if j != i) and _inside(q, p) is False:
                    key = tuple(sorted([(round(a[0], 1), round(a[1], 1)), (round(b[0], 1), round(b[1], 1))]))
                    shared[key] = (a, b)
    out = [parts[0]]
    done = set()
    for a, b in shared.values():
        out.append(detail(seg(*a, *b)))
    # joints between matching long edges
    for p in polys:
        for a, b in zip(p, p[1:] + p[:1]):
            if math.dist(a, b) > unit * 1.2:
                ka = tuple(sorted([(round(a[0], 1), round(a[1], 1)), (round(b[0], 1), round(b[1], 1))]))
                if ka in done:
                    continue
                cnt = sum(1 for o in polys for c, d in zip(o, o[1:] + o[:1])
                          if tuple(sorted([(round(c[0], 1), round(c[1], 1)), (round(d[0], 1), round(d[1], 1))])) == ka)
                if cnt > 1:
                    out.append(detail(seg(*a, *b)))
                    done.add(ka)
    return out


def _shell_filled():
    ring = D(P(circle(12, 12, 10.0)), P(circle(12, 12, 4.0)))
    wedge = P(poly([(12, 12), (12, -4), (28, -4), (28, 12)], closed=True))
    return D(ring, wedge)


@icon("spherical-shell", CAT, "Hollow sphere with a wedge cut away, showing the thin wall and the empty space inside.",
      tags=["spherical shell", "hollow sphere", "sphere cross section", "cutaway", "thick wall", "solid geometry", "volume"],
      filled=_shell_filled)
def _(S):
    return [line("M21 12A9 9 0 1 1 12 3"), line(seg(12, 3, 12, 7)), line(seg(17, 12, 21, 12)),
            line(circle(12, 12, 5))]


@icon("ponzo-illusion", CAT, "Ponzo illusion: two converging rail lines with two equal bars, the upper one looking longer.",
      tags=["ponzo illusion", "railway lines", "converging lines", "perspective", "optical illusion", "size perception"])
def _(S):
    return [line(seg(3, 21, 9, 3)), line(seg(21, 21, 15, 3)),
            line(seg(10, 8.5, 14, 8.5)), line(seg(10, 16, 14, 16))]


@icon("poggendorff-illusion", CAT, "Poggendorff illusion: a diagonal line broken by a vertical bar, the two halves looking out of line.",
      tags=["poggendorff illusion", "interrupted line", "misalignment", "diagonal", "optical illusion", "perception"])
def _(S):
    return [shell(rect(9, 3, 6, 18, L(S, 0, 1.5))), line(seg(3, 19, 9, 13)), line(seg(15, 10, 21, 4))]


@icon("jastrow-illusion", CAT, "Jastrow illusion: two identical curved bands stacked one above the other, the lower looking bigger.",
      tags=["jastrow illusion", "curved bands", "arcs", "size illusion", "optical illusion", "perception", "psychology"])
def _(S):
    def band(dy):
        R, r = 10.0, 5.6
        a0, a1 = 222, 318
        o0, o1 = pt_on(12, 14 + dy, R, a0), pt_on(12, 14 + dy, R, a1)
        i0, i1 = pt_on(12, 14 + dy, r, a0), pt_on(12, 14 + dy, r, a1)
        d = (f"M{fmt(o0[0])} {fmt(o0[1])}A{R} {R} 0 0 1 {fmt(o1[0])} {fmt(o1[1])}L{fmt(i1[0])} {fmt(i1[1])}"
             f"A{r} {r} 0 0 0 {fmt(i0[0])} {fmt(i0[1])}Z")
        return shell(d if S.name == "line" else path_to_d(soften(P(d), 0.8)))
    return [band(-0.5), band(9.5)]


def _hermann_filled():
    g, s = 2.0, (18 - 4.0) / 3
    block = P(rect(3, 3, 18, 18, 3.0))
    cuts = []
    for k in (1, 2):
        c = 3 + k * s + (k - 0.5) * g
        cuts += [P(rect(2, c - g / 2, 20, g)), P(rect(c - g / 2, 2, g, 20))]
    return D(block, U(*cuts))


@icon("hermann-grid-illusion", CAT, "Hermann grid illusion: a grid of black squares split by white lines, with ghost dots at the crossings.",
      tags=["hermann grid", "grid illusion", "ghost dots", "black squares", "optical illusion", "perception", "lateral inhibition"],
      filled=_hermann_filled)
def _(S):
    g, s = 2.0, (18 - 4.0) / 3
    r = L(S, 0, 1.1)
    return [solid(rect(3 + i * (s + g), 3 + j * (s + g), s, s, r)) for j in range(3) for i in range(3)]


@icon("four-color-map", CAT, "Map split into four irregular regions, each marked differently so no neighbours match.",
      tags=["four color theorem", "map coloring", "graph coloring", "regions", "borders", "topology", "cartography"])
def _(S):
    J = (12.5, 12)
    tl = [(3, 3), (11, 3), (13, 7.5), J, (7.5, 11), (3, 13.5)]
    inset = D(P(poly(tl, closed=True)), ST(poly(tl, closed=True), 4.0, "butt", "miter"))
    borders = [(11, 3), (13, 7.5), J, (17, 13), (21, 10.5)], [(3, 13.5), (7.5, 11), J, (11, 16.5), (13.5, 21)]
    return ([shell(rect(3, 3, 18, 18, L(S, 0, 3)))]
            + [detail(poly(b, r=S.r * 0.5)) for b in borders]
            + [solid(path_to_d(inset if S.name == "line" else soften(inset, 0.8))),
               detail(seg(15.2, 5.2, 18.8, 8.8)), pt(S, 7.5, 17, 2.75)])


def _kolam():
    lobes = [pt_on(12, 12, 5.4, a) for a in (-90, 0, 90, 180)]
    region = U(*[P(circle(x, y, 4.3)) for x, y in lobes], P(circle(12, 12, 4.3)))
    return lobes, region


@icon("kolam-pattern", CAT, "Kolam: a looping line wrapped around a diamond of dots, as in threshold drawings from South India.",
      tags=["kolam", "rangoli", "pulli", "dot pattern", "threshold art", "floor drawing", "south india"])
def _(S):
    lobes, region = _kolam()
    parts = [soft_shell(S, path_to_d(region), 0.6)]
    parts += [pt(S, x, y, 2.5) for x, y in lobes]
    parts.append(pt(S, 12, 12, 2.5))
    return parts


@icon("asanoha-pattern", CAT, "Asanoha: a six-pointed star cut into thin triangles by lines from its centre, the hemp-leaf pattern.",
      tags=["asanoha", "hemp leaf", "japanese pattern", "six pointed star", "geometric pattern", "hexagram", "textile pattern"])
def _(S):
    tips = regular(12, 12, 9.5, 6, -90)
    inn = regular(12, 12, 5.4, 6, -60)
    star = []
    for a, b in zip(tips, inn):
        star += [a, b]
    parts = [shell(poly(star, closed=True, r=L(S, 0, 0.8)))]
    parts += [detail(seg(*lerp((12, 12), v, 0.15), *lerp((12, 12), v, 0.8))) for v in tips]
    return parts