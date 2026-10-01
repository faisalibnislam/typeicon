"""TypeIcon Core: notation (batch notation_006).

Packaging and handling marks, recycling marks, math curves and notation, hazard warning triangles,
mandatory signs and classroom maths manipulatives.
"""
from __future__ import annotations

import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt

CAT = "notation"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def head(S, x, y, dx, dy, s=2.5):
    """Open arrowhead chevron with its tip at (x, y) pointing along (dx, dy)."""
    n = math.hypot(dx, dy)
    dx, dy = dx / n, dy / n
    px, py = -dy, dx
    a = (x - dx * s + px * s, y - dy * s + py * s)
    b = (x - dx * s - px * s, y - dy * s - py * s)
    return poly([a, (x, y), b], r=S.r)


def tri(S, x, y, dx, dy, s=3.0, w=0.8):
    """Solid arrowhead triangle with its tip at (x, y) pointing along (dx, dy)."""
    n = math.hypot(dx, dy)
    dx, dy = dx / n, dy / n
    px, py = -dy, dx
    a = (x - dx * s + px * s * w, y - dy * s + py * s * w)
    b = (x - dx * s - px * s * w, y - dy * s - py * s * w)
    return solid(poly([a, (x, y), b], closed=True, r=S.r * 0.4))


def drop_d(cx, top, w, h):
    """Water drop with its point at (cx, top), width w, height h."""
    r = w / 2
    cy = top + h - r
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx)} {fmt(top)} {fmt(cx - r)} {fmt(cy - r * 0.9)} {fmt(cx - r)} {fmt(cy)}"
            f"A{fmt(r)} {fmt(r)} 0 0 0 {fmt(cx + r)} {fmt(cy)}C{fmt(cx + r)} {fmt(cy - r * 0.9)} {fmt(cx)} {fmt(top)} {fmt(cx)} {fmt(top)}Z")


def dash_details(p0, p1, n, dash=2.0):
    (x0, y0), (x1, y1) = p0, p1
    length = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / length, (y1 - y0) / length
    gap = (length - n * dash) / (n - 1) if n > 1 else 0
    return [detail(seg(x0 + ux * i * (dash + gap), y0 + uy * i * (dash + gap),
                       x0 + ux * (i * (dash + gap) + dash), y0 + uy * (i * (dash + gap) + dash))) for i in range(n)]


def person(x, y, s=1.0):
    """Tiny head circle path helper (center)."""
    return circle(x, y, 2 * s)


# ============================================================================ packaging and handling marks

@icon("humidity-limit-symbol", CAT, "An umbrella canopy over a water drop, the keep-dry handling mark.",
      tags=["keep dry", "umbrella", "humidity limit", "moisture", "packaging", "handling", "drop"])
def _(S):
    canopy = L(S, "M3 11A9 8 0 0 1 21 11Z",
               "M3 11A9 8 0 0 1 21 11A3 2.2 0 0 0 15 11A3 2.2 0 0 0 9 11A3 2.2 0 0 0 3 11Z")
    return [shell(canopy),
            line(seg(12, 12, 12, 14)),
            shell(drop_d(12, 14, L(S, 6.5, 7), 8))]


@icon("protect-from-light", CAT, "A box under a roof shape with a sun and rays above, the keep-away-from-sunlight mark.",
      tags=["keep away from sunlight", "light sensitive", "sun", "box", "packaging", "handling", "shade"])
def _(S):
    out = [shell(rect(9.75, 15.5, 10, 6, min(S.R, 1))),
           shell(poly([(8.5, 15.5), (14.75, 10.5), (21, 15.5)], closed=True, r=S.r)),
           dot(7.5, 7.5, 2)]
    for a in (180, 225, 270, 315, 0):
        x1, y1 = pt_on(7.5, 7.5, 3.75, a)
        x2, y2 = pt_on(7.5, 7.5, 5.5, a)
        out.append(line(seg(x1, y1, x2, y2)))
    return out


@icon("handle-with-care", CAT, "Two cupped hands holding a box, the fragile handling mark.",
      tags=["fragile", "careful", "hands", "box", "packaging", "handling", "support"])
def _(S):
    return [shell(rect(7.5, 2.5, 9, 8.5, min(S.R, 1.5))),
            line("M2.5 10C2.5 16 7 19.5 12 20.5C17 19.5 21.5 16 21.5 10"),
            line("M2.5 10V12"), line("M21.5 10V12")]


@icon("open-here", CAT, "A box with a pull strip across its front and an arrow above pointing along the tear line.",
      tags=["tear", "open", "pull tab", "packaging", "arrow", "strip", "instruction"])
def _(S):
    return [shell(rect(3, 10, 18, 11, S.R)),
            detail(seg(3, 14.5, 21, 14.5)),
            line(seg(5, 5, 16, 5)), tri(S, 20.5, 5, 1, 0, 4.5, 0.6)]


@icon("tear-notch", CAT, "A pouch with a small V notch in its edge and a dashed tear line leading from it.",
      tags=["tear here", "pouch", "sachet", "notch", "packaging", "open", "easy open"])
def _(S):
    return [shell(poly([(4, 3), (20, 3), (20, 21), (4, 21), (4, 12.5), (8, 9.5), (4, 6.5)], closed=True, r=S.r * 0.6))] + \
        dash_details((11, 9.5), (17, 9.5), 2, 2.0)


@icon("keep-refrigerated", CAT, "A box with a snowflake beside a thermometer, the keep-cool storage mark.",
      tags=["chilled", "cold", "store cold", "fridge", "thermometer", "snowflake", "packaging"])
def _(S):
    return [shell(rect(2.5, 8, 12, 13.5, S.R)),
            detail(seg(8.5, 11.5, 8.5, 18)), detail(seg(5.7, 13, 11.3, 16.5)), detail(seg(5.7, 16.5, 11.3, 13)),
            shell("M17.5 15.3V5.5A1.5 1.5 0 0 1 20.5 5.5V15.3A3 3 0 1 1 17.5 15.3Z")]


@icon("tamper-evident-seal", CAT, "A jar lid above a jar neck with a torn seal band between them.",
      tags=["safety seal", "tamper", "sealed", "jar", "band", "packaging", "security"])
def _(S):
    return [shell(rect(4, 2.5, 16, 6.5, min(S.R, 2))),
            line(L(S, "M4 12.5H9L11 15L13 12L15 15H20", "M4 12.5H9L11 15L13 12L15 15H20")),
            line(seg(6.5, 16, 6.5, 21.5)), line(seg(17.5, 16, 17.5, 21.5))]


@icon("child-resistant-cap", CAT, "A bottle cap with a push-down arrow and a curved turn arrow, the push and turn mark.",
      tags=["push and turn", "childproof", "safety cap", "medicine bottle", "packaging", "lid"])
def _(S):
    ax, ay = pt_on(16, 9.5, 5, 340)
    return [shell(rect(3, 15, 18, 6.5, min(S.R, 2))),
            detail(seg(8, 15, 8, 21.5)), detail(seg(12, 15, 12, 21.5)), detail(seg(16, 15, 16, 21.5)),
            line(seg(6.5, 3, 6.5, 8)), tri(S, 6.5, 12, 0, 1, 4.5, 0.6),
            line(arc(16, 9.5, 5, 200, 336)), tri(S, ax, ay, 0.34, 0.94, 4.2, 0.6)]


@icon("small-parts-warning", CAT, "A crossed-out circle around a solid baby's head, the not suitable for small children mark.",
      tags=["toy warning", "choking hazard", "under three", "baby", "child", "age", "not for children"])
def _(S):
    r = L(S, 3.25, 3.75)
    return [shell(circle(12, 12, 9.75)),
            Part("dot", circle(12, 12.5, r)),
            detail(seg(5.6, 18.4, 18.4, 5.6))]


@icon("plastic-bag-suffocation-warning", CAT, "A plastic bag with a small head inside, crossed out to warn about suffocation.",
      tags=["suffocation", "plastic bag", "child safety", "warning", "keep away", "baby", "packaging"])
def _(S):
    return [shell(poly([(6.5, 6), (17.5, 6), (20, 21.5), (4, 21.5)], closed=True, r=S.r * 0.6)),
            line("M9 6V5A3 3 0 0 1 15 5V6"),
            detail(circle(12, 14.5, 3)),
            detail(seg(3, 22, 21, 2.5))]


@icon("keep-out-of-reach-of-children", CAT, "A bottle on a high shelf with a small child reaching up from below.",
      tags=["child safety", "high shelf", "medicine", "store safely", "reach", "kid", "packaging"])
def _(S):
    return [line(seg(3, 8.5, 21, 8.5)),
            shell(rect(13.5, 2.5, 5, 6, min(S.R, 1.5))),
            shell(circle(7, 13, 2.25)),
            line("M7 15.5V19"), line("M4.5 21.5L7 19L9.5 21.5"),
            line("M7 17L11 11.5")]


@icon("stovetop-safe", CAT, "A pan resting on a burner line with flame strokes below it.",
      tags=["cookware", "hob", "stove", "pan", "heat", "flame", "cooking"])
def _(S):
    return [shell(rect(3, 4.5, 13, 6, min(S.R, 2))),
            line(seg(16, 7, 21.5, 7)),
            line(seg(3, 14, 19, 14)),
            line("M7 17.5C5.5 18.5 6.5 20 7 21.5"), line("M11 17C9.5 18.3 11 20 11 21.5"), line("M15 17.5C13.5 18.5 14.5 20 15 21.5")]



# ============================================================================ recycling and waste marks

def smooth_d(pts, closed=False):
    """Catmull-Rom spline through pts as a cubic Bezier path."""
    n = len(pts)
    g = (lambda i: pts[i % n]) if closed else (lambda i: pts[max(0, min(n - 1, i))])
    d = "M" + fmt(pts[0][0]) + " " + fmt(pts[0][1])
    last = n if closed else n - 1
    for i in range(last):
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d + ("Z" if closed else "")


def tri_pts(x, y, dx, dy, s, w):
    n = math.hypot(dx, dy)
    dx, dy = dx / n, dy / n
    px, py = -dy, dx
    return [(x - dx * s + px * s * w, y - dy * s + py * s * w), (x, y), (x - dx * s - px * s * w, y - dy * s - py * s * w)]


def chase_loop(S, cx, cy, r, knock=False, s=3.6):
    """Three chasing arrows around (cx, cy). knock=True uses detail arcs and knocked-out heads (for solid discs)."""
    out = []
    for a0 in (-85, 35, 155):
        a1 = a0 + 75
        d = arc(cx, cy, r, a0, a1)
        out.append(detail(d) if knock else line(d))
        x, y = pt_on(cx, cy, r, a1 + 6)
        dx, dy = -math.sin(math.radians(a1 + 6)), math.cos(math.radians(a1 + 6))
        pts = tri_pts(x + dx * 1.0, y + dy * 1.0, dx, dy, s, 0.85)
        pd = poly(pts, closed=True, r=S.r * 0.3)
        out.append(Part("dot", pd) if knock else solid(pd))
    return out


@icon("recyclable-carton", CAT, "A drink carton inside a loop of three chasing arrows.",
      tags=["carton recycling", "drink carton", "recycle", "juice box", "packaging", "loop", "waste"])
def _(S):
    return chase_loop(S, 12, 12, 9.25) + [
        shell(poly([(9.5, 10), (12, 7.5), (14.5, 10), (14.5, 16.5), (9.5, 16.5)], closed=True, r=S.r * 0.4))]


@icon("recycled-content", CAT, "A solid circle with a white loop of three chasing arrows inside it.",
      tags=["recycled material", "post consumer", "recycle", "loop", "badge", "eco label", "sustainable"])
def _(S):
    return [shell(circle(12, 12, 9.75))] + chase_loop(S, 12, 12, 5.25, knock=True, s=3.2)


@icon("refillable-symbol", CAT, "A bottle with a circular refill arrow on its body and a neck cap.",
      tags=["refill", "reusable bottle", "refillable", "packaging", "zero waste", "circular", "cycle"])
def _(S):
    a1 = 285
    ex, ey = pt_on(12, 15, 3.5, a1)
    dx, dy = -math.sin(math.radians(a1)), math.cos(math.radians(a1))
    return [shell(rect(10, 2.5, 4, 3, 0.5)),
            shell(rect(5.5, 6, 13, 15.5, S.R)),
            detail(arc(12, 15, 3.5, 330, a1)),
            Part("dot", poly(tri_pts(ex + dx * 1.2, ey + dy * 1.2, dx, dy, 3.4, 0.9), closed=True))]


@icon("sharps-disposal", CAT, "A box with a slotted lid and a syringe pushed needle first into the slot.",
      tags=["needle disposal", "syringe", "sharps bin", "medical waste", "biohazard", "waste sorting", "safety"])
def _(S):
    return [shell(rect(3.5, 13, 17, 8.5, min(S.R, 2))),
            line(seg(8.5, 2.5, 15.5, 2.5)), line(seg(12, 2.5, 12, 4.5)),
            shell(rect(9.75, 4.5, 4.5, 6)),
            line(seg(12, 10.5, 12, 15.5))]


@icon("oil-recycling", CAT, "A single oil drop inside a loop of three chasing arrows.",
      tags=["used oil", "cooking oil", "motor oil", "recycle", "drop", "waste sorting", "loop"])
def _(S):
    return chase_loop(S, 12, 12, 9.25) + [shell(drop_d(12, 7, 5, 8.5))]


@icon("litter-bin-symbol", CAT, "A figure dropping a piece of litter into a bin beside it.",
      tags=["dispose tidily", "put litter in bin", "rubbish", "trash", "keep clean", "tidy", "person"])
def _(S):
    return [shell(circle(6, 4.75, 2.25)),
            line("M6 8V14"), line("M3.5 21.5L6 14L8.5 21.5"),
            line("M6 9.5L10.5 7.5"),
            solid(poly([(13.5, 3.5), (16, 6), (13.5, 8.5), (11, 6)], closed=True)),
            shell(poly([(13, 12), (21, 12), (20, 21.5), (14, 21.5)], closed=True, r=S.r * 0.5)),
            line(seg(12, 12, 22, 12))]


# ============================================================================ math symbols and curves

@icon("austral-sign", CAT, "The austral currency sign: a capital A crossed by two bars through its legs.",
      tags=["currency", "argentina", "austral", "money symbol", "a with bars", "old currency", "finance"])
def _(S):
    return [line(poly([(4.5, 21), (12, 3.5), (19.5, 21)], r=S.r)),
            line(seg(3, 12.5, 21, 12.5)), line(seg(3, 17, 21, 17))]


@icon("degrees-minutes-seconds", CAT, "A degree ring, a prime and a double prime above an angle wedge.",
      tags=["angle", "arc minute", "arc second", "coordinates", "latitude", "longitude", "sexagesimal", "degree"])
def _(S):
    return [shell(circle(5.5, 7, 2.75)),
            line(seg(13, 4, 11.5, 10.5)),
            line(seg(18, 4, 16.5, 10.5)), line(seg(21.5, 4, 20, 10.5)),
            line(poly([(3, 15.5), (3, 21), (21, 21)], r=0)),
            line(seg(3, 21, 12, 15.5))]


@icon("power-set-symbol", CAT, "The Weierstrass script p with a looped tail, used for the power set.",
      tags=["power set", "weierstrass p", "script p", "set theory", "elliptic function", "subsets", "math"])
def _(S):
    return [line("M9 9C9 5.8 11 4 14 4C17.3 4 19 6.2 19 9C19 12.6 16.2 15 12.5 14.7C10.2 14.5 8.8 13 9 11"),
            line(L(S, "M9 9C8.3 12.5 7 16.5 6.2 19C5.5 21 3.5 21 3.5 19.2C3.5 17.8 5 17.5 6.2 18.2",
                   "M9 9C8.6 12.5 7.6 15.5 6.6 18C5.9 19.8 3.6 20.6 3.3 19C3 17.6 4.6 17 6 17.4"))]


@icon("laplace-transform", CAT, "The script capital L used for the Laplace transform.",
      tags=["laplace", "script l", "transform", "differential equations", "control systems", "engineering", "math"])
def _(S):
    return [line("M14 4.5C12.5 3 9.5 2.8 9 6C8.7 9 10.2 13 9.8 16.5C9.5 19.5 6.5 20 5.5 18.5C4.8 17 6.5 16 8.5 16.8C12 18.3 16.5 19 20 17")]


@icon("nabla", CAT, "An upside down triangle, the del operator, with a small f beside it.",
      tags=["del", "gradient", "divergence", "curl", "vector calculus", "operator", "math"])
def _(S):
    return [line(poly([(2.5, 4.5), (14.5, 4.5), (8.5, 19.5)], closed=True, r=S.r)),
            line("M19 21V8.5C19 5.8 20.3 4.5 22 4.5"), line(seg(16.5, 11, 21.5, 11))]


def cycloid_pts(x0, base, r, t0, t1, n):
    return [(x0 + r * (t - math.sin(t)), base - r * (1 - math.cos(t)))
            for t in [t0 + (t1 - t0) * i / n for i in range(n + 1)]]


@icon("cycloid", CAT, "A circle resting on a flat line under the arch traced by a point on its rim.",
      tags=["rolling circle", "arch curve", "brachistochrone", "roulette", "geometry", "parametric", "curve"])
def _(S):
    r = 3.4
    pts = cycloid_pts(1.3, 17, r, 0, 2 * math.pi, 12)
    return [line(seg(1.3, 17, 22.7, 17)),
            line(smooth_d(pts)),
            shell(circle(1.3 + r * math.pi, 17 - r, r)),
            detail(seg(1.3 + r * math.pi, 17 - r, 1.3 + r * math.pi, 17 - 2 * r)),
            dot(1.3 + r * math.pi, 17 - 2 * r, 1.25)]


@icon("lissajous-curve", CAT, "A smooth closed curve that crosses itself in a knotted figure, traced by two waves.",
      tags=["lissajous", "oscilloscope", "parametric", "harmonic", "knot", "wave", "curve"])
def _(S):
    ph = L(S, 0.0, 0.5)
    pts = [(12 + 8.5 * math.cos(3 * t + ph), 12 + 8.5 * math.sin(2 * t)) for t in [2 * math.pi * i / 36 for i in range(36)]]
    return [line(smooth_d(pts, closed=True))]


def petal(cx, cy, ang, L_, w):
    u = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
    n = (-u[1], u[0])
    def P_(a, b):
        return (cx + u[0] * L_ * a + n[0] * L_ * b, cy + u[1] * L_ * a + n[1] * L_ * b)
    p = [P_(0.15, w), P_(0.8, w * 1.1), P_(1, 0), P_(0.8, -w * 1.1), P_(0.15, -w)]
    return (f"M{fmt(cx)} {fmt(cy)}C{fmt(p[0][0])} {fmt(p[0][1])} {fmt(p[1][0])} {fmt(p[1][1])} {fmt(p[2][0])} {fmt(p[2][1])}"
            f"C{fmt(p[3][0])} {fmt(p[3][1])} {fmt(p[4][0])} {fmt(p[4][1])} {fmt(cx)} {fmt(cy)}Z")


@icon("rose-curve", CAT, "A four petal flower traced by one curve, all petals meeting at the centre.",
      tags=["rhodonea", "polar curve", "petals", "flower", "parametric", "trigonometry", "curve"])
def _(S):
    return [line(petal(12, 12, a, 9.5, L(S, 0.26, 0.36))) for a in (-45, 45, 135, 225)]


@icon("catenary", CAT, "A chain hanging in a smooth U curve between the tops of two posts.",
      tags=["hanging chain", "cable", "sag", "curve", "hyperbolic cosine", "suspension", "power line"])
def _(S):
    return [line(seg(4, 4, 4, 21)), line(seg(20, 4, 20, 21)),
            line("M4 4C6.5 17 17.5 17 20 4"),
            line(seg(2, 21, 22, 21))]


def hilbert_pts(order, x0, y0, size):
    n = 2 ** order

    def d2xy(d):
        x = y = 0
        t = d
        s = 1
        while s < n:
            rx = 1 & (t // 2)
            ry = 1 & (t ^ rx)
            if ry == 0:
                if rx == 1:
                    x, y = s - 1 - x, s - 1 - y
                x, y = y, x
            x += s * rx
            y += s * ry
            t //= 4
            s *= 2
        return x, y
    cell = size / n
    return [(x0 + (x + 0.5) * cell, y0 + (y + 0.5) * cell) for x, y in (d2xy(d) for d in range(n * n))]


@icon("hilbert-curve", CAT, "A single line folding through a square in right angle turns, the Hilbert space filling curve.",
      tags=["space filling curve", "fractal", "maze", "recursive", "geometry", "curve", "hilbert"])
def _(S):
    return [line(poly(hilbert_pts(2, 2, 2, 20), r=S.r * 0.7))]


@icon("voronoi-diagram", CAT, "A square divided into irregular polygon cells, each with one seed dot.",
      tags=["voronoi", "tessellation", "cells", "nearest neighbour", "partition", "geometry", "seeds"])
def _(S):
    A, B = (11, 9), (15, 14)
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail(poly([(3, 11), A, (14, 3)])), detail(poly([A, B])),
            detail(poly([(21, 11.5), B, (10, 21)])),
            dot(7, 6.5, 1.25), dot(17.5, 7, 1.25), dot(17, 17.5, 1.25), dot(6.5, 16, 1.25)]


# ============================================================================ hazard warning triangles

def warn(S):
    return shell(poly([(12, 2.5), (22, 20.5), (2, 20.5)], closed=True, r=S.r * 1.2))


@icon("optical-radiation-hazard", CAT, "A warning triangle with a small sun and bold rays at its centre.",
      tags=["laser warning", "optical radiation", "uv", "light hazard", "sign", "safety", "eye hazard"])
def _(S):
    out = [warn(S), dot(12, 14.5, 1.75)]
    for a in (180, 225, 270, 315, 0):
        x1, y1 = pt_on(12, 14.5, 3.2, a)
        x2, y2 = pt_on(12, 14.5, 4.8, a)
        out.append(detail(seg(x1, y1, x2, y2)))
    return out


@icon("lightning-strike-hazard", CAT, "A warning triangle with a lightning bolt striking down toward a small standing figure.",
      tags=["lightning", "storm", "outdoor work", "thunder", "warning sign", "safety", "electric"])
def _(S):
    return [warn(S),
            detail(poly([(14.5, 9), (11.5, 13), (14.5, 13), (12, 17.5)])),
            dot(8, 15, 1.2), detail(seg(8, 16.5, 8, 18.5))]


@icon("fragile-roof-hazard", CAT, "A warning triangle with a figure falling through a broken gap in a roof sheet.",
      tags=["fragile roof", "fall", "roof work", "skylight", "warning sign", "safety", "construction"])
def _(S):
    return [warn(S),
            detail(seg(5.5, 17, 9, 17)), detail(seg(15, 17, 18.5, 17)),
            dot(12, 10.5, 1.3), detail(seg(12, 12, 12, 14.5)), detail("M10.3 17.3L12 14.5L13.7 17.3")]


@icon("door-finger-trap-hazard", CAT, "A warning triangle with fingers reaching into the hinge gap beside a door edge.",
      tags=["finger trap", "door hinge", "crush hazard", "trapped fingers", "warning sign", "safety", "pinch point"])
def _(S):
    return [warn(S),
            detail(seg(15.5, 10, 15.5, 18.5)),
            detail(seg(7, 13, 13, 13)), detail(seg(7, 16.5, 13, 16.5))]


@icon("robot-arm-hazard", CAT, "A warning triangle with a jointed robot arm reaching out from a base.",
      tags=["robot", "industrial arm", "automation", "moving machinery", "warning sign", "safety", "factory"])
def _(S):
    return [warn(S),
            detail(poly([(8, 17.5), (10.5, 12.5), (15.5, 14.5)])),
            dot(8, 17.5, 1.5), dot(10.5, 12.5, 1.25), dot(15.5, 14.5, 1.25)]


@icon("high-pressure-jet-hazard", CAT, "A warning triangle with a nozzle and a straight jet of liquid ending in drops.",
      tags=["high pressure", "water jet", "spray", "pressurised", "warning sign", "safety", "injection hazard"])
def _(S):
    return [warn(S),
            dot(7.5, 14.5, 1.5),
            detail(seg(9, 14.5, 14, 14.5)),
            dot(16, 12.5, 0.9), dot(16, 16.5, 0.9)]


@icon("radio-frequency-hazard", CAT, "A warning triangle with a mast antenna sending curved waves to both sides.",
      tags=["radio waves", "antenna", "rf", "radiation", "transmitter", "warning sign", "safety"])
def _(S):
    return [warn(S),
            detail(seg(12, 12.5, 12, 18.5)), dot(12, 12, 1.3),
            detail(arc(12, 12.5, 3.25, 145, 215)), detail(arc(12, 12.5, 3.25, -35, 35))]


# ============================================================================ mandatory signs

@icon("wear-face-mask-sign", CAT, "A solid round sign with a head wearing a face mask over its nose and mouth.",
      tags=["mandatory sign", "face mask", "mask required", "ppe", "hygiene", "health", "protective"])
def _(S):
    rh = L(S, 5.25, 5.5)
    return [shell(circle(12, 12, 9.75)),
            detail(circle(12, 11, rh)),
            Part("dot", rect(L(S, 8.25, 7.5), 11.5, L(S, 7.5, 9), L(S, 4.5, 4.5), L(S, 0.5, 2))),
            detail(seg(9.5, 13.75, 14.5, 13.75)),
            dot(10, 8.6, 0.9), dot(14, 8.6, 0.9)]


@icon("use-hand-sanitizer-sign", CAT, "A solid round sign with a pump bottle dispensing a drop onto a hand.",
      tags=["mandatory sign", "hand sanitiser", "hand sanitizer", "hygiene", "clean hands", "pump", "health"])
def _(S):
    return [shell(circle(12, 12, 9.75)),
            Part("dot", rect(6.5, 11.5, 4.5, 6.5, 0.5)),
            detail(poly([(8.75, 11.5), (8.75, 8.5), (14, 8.5)])),
            Part("dot", drop_d(14, 10.5, 2.4, 3.4)),
            detail(seg(12, 18, 18, 18))]


# ============================================================================ packaging marks and symbols

@icon("shake-well", CAT, "An upright bottle with curved motion lines on both sides showing shaking.",
      tags=["shake before use", "shake bottle", "mix", "motion", "packaging", "instruction", "liquid"])
def _(S):
    return [shell(poly([(10, 2.5), (14, 2.5), (14, 6.5), (16.5, 9), (16.5, 21.5), (7.5, 21.5), (7.5, 9), (10, 6.5)], closed=True, r=S.r * 0.6)),
            detail(seg(7.5, 13, 16.5, 13)),
            line("M4.5 8C3 11 3 15 4.5 18.5"), line("M19.5 8C21 11 21 15 19.5 18.5")]


@icon("peel-here", CAT, "A tray with a film lid whose corner is peeling back and an arrow pointing to the flap.",
      tags=["peel", "film lid", "pull corner", "packaging", "open", "ready meal", "instruction"])
def _(S):
    return [shell(rect(3, 9.5, 18, 11.5, min(S.R, 3))),
            shell(poly([(14, 9.5), (21, 9.5), (21, 3)], closed=True, r=S.r * 0.4)),
            line(seg(4, 4.5, 9, 4.5)), tri(S, 12.5, 4.5, 1, 0, 4, 0.6)]


@icon("resealable-pack", CAT, "A pouch with a zip seal track across its top and a closing arrow pointing up to it.",
      tags=["zip lock", "reclosable", "resealable", "pouch", "packaging", "seal", "bag"])
def _(S):
    return [shell(poly([(4, 3), (20, 3), (20, 21), (4, 21)], closed=True, r=S.r * 0.5)),
            detail(seg(4, 7.5, 20, 7.5)),
            detail(seg(12, 18, 12, 11.5)), detail(poly([(9.5, 13.5), (12, 11), (14.5, 13.5)]))]


@icon("pierce-film-lid", CAT, "A shallow tray covered with film and a three tined fork piercing down into it.",
      tags=["pierce lid", "prick film", "microwave", "ready meal", "packaging", "fork", "vent"])
def _(S):
    return [shell(poly([(2.5, 15.5), (21.5, 15.5), (20, 21.5), (4, 21.5)], closed=True, r=S.r * 0.4)),
            line(seg(8, 8, 8, 13.5)), line(seg(12, 2.5, 12, 13.5)), line(seg(16, 8, 16, 13.5)), line(seg(8, 8, 16, 8))]


@icon("manufacturer-symbol", CAT, "A solid factory outline with a sawtooth roof and a chimney.",
      tags=["factory", "manufacturer", "made by", "medical device", "industry", "production", "label symbol"])
def _(S):
    return [shell(poly([(3, 21.5), (3, 9.5), (8.5, 13.5), (8.5, 9.5), (14, 13.5), (14, 3.5), (20, 3.5), (20, 21.5)], closed=True, r=S.r * 0.4)),
            detail(seg(7, 18, 16.5, 18))]


@icon("lot-number-symbol", CAT, "The letters L O T standing for a batch code.",
      tags=["lot", "batch", "batch code", "production lot", "label", "traceability", "medical device"])
def _(S):
    return [line(poly([(2.5, 6.5), (2.5, 17.5), (7.5, 17.5)], r=S.r)),
            line(rect(9.5, 6.5, 5, 11, L(S, 1.5, 2.5))),
            line(seg(16.5, 6.5, 22, 6.5)), line(seg(19.25, 6.5, 19.25, 17.5))]


@icon("single-use-symbol", CAT, "A numeral 2 in a crossed-out circle, the do not reuse mark.",
      tags=["do not reuse", "single use", "disposable", "medical device", "label symbol", "one time", "discard"])
def _(S):
    return [shell(circle(12, 12, 9.75)),
            detail("M8.5 9.5C8.5 7.6 10 6.5 12 6.5C14 6.5 15.5 7.7 15.5 9.5C15.5 11.5 13.5 12.8 12 14.3L8.5 17.5H15.5"),
            detail(seg(5.6, 18.4, 18.4, 5.6))]


@icon("pattern-blocks", CAT, "A hexagon divided into a trapezoid, a rhombus and two triangles, like classroom pattern blocks.",
      tags=["hexagon", "tangram", "manipulatives", "geometry", "tiles", "classroom", "shapes"])
def _(S):
    hexa = regular(12, 12, 9.75, 6, start=0)
    return [shell(poly(hexa, closed=True, r=L(S, 0, 2.5))),
            detail(seg(2.25, 12, 21.75, 12)),
            detail(seg(*hexa[4], 12, 12)),
            detail(seg(12, 12, *hexa[1]))]


@icon("fraction-strips", CAT, "Three stacked bars of equal length split into one whole, two halves and three thirds.",
      tags=["fractions", "manipulatives", "halves", "thirds", "math", "classroom", "bars"])
def _(S):
    rx = L(S, 0, 1.5)
    return [shell(rect(3, 3.5, 18, 3, rx)),
            shell(rect(3, 10.5, 18, 3, rx)), detail(seg(12, 10.5, 12, 13.5)),
            shell(rect(3, 17.5, 18, 3, rx)), detail(seg(9, 17.5, 9, 20.5)), detail(seg(15, 17.5, 15, 20.5))]


def _dots_filled():
    from dsl import P, U
    return U(*[P(circle(x, y, 1.9)) for y in (5.5, 12, 18.5) for x in (4.5, 9.5, 14.5, 19.5)])


def grid_mark(S, x, y, r=1.5):
    if S.name == "line":
        return Part("dot", rect(x - r, y - r, 2 * r, 2 * r))
    return dot(x, y, r)


@icon("multiplication-array", CAT, "A grid of dots in three rows of four for counting a times table.",
      filled=lambda: _dots_filled(),
      tags=["times table", "multiplication", "array", "rows and columns", "math", "classroom", "dots"])
def _(S):
    return [grid_mark(S, x, y, 1.6) for y in (5.5, 12, 18.5) for x in (4.5, 9.5, 14.5, 19.5)]


@icon("bar-model", CAT, "A long bar split into three parts with a bracket above showing the total.",
      tags=["bar diagram", "tape diagram", "part whole", "word problems", "math", "classroom", "total"])
def _(S):
    return [line(poly([(3, 9.5), (3, 7.5), (21, 7.5), (21, 9.5)])), line(seg(12, 7.5, 12, 4)),
            shell(rect(3, 12.5, 18, 8, min(S.R, 2))),
            detail(seg(9, 12.5, 9, 20.5)), detail(seg(15, 12.5, 15, 20.5))]
