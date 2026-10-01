"""TypeIcon Core: notation (batch notation_001).

Mathematical letters, operators, logic signs, number sets, graphs and geometric solids. Letters follow the
Greek letters in `math.py`: open strokes (line parts) whose Line and Rounded styles differ by caps, joins and
fillets; Filled makes the strokes heavier. Closed figures (solids, polygons) use shells so Filled is solid.
"""
from __future__ import annotations

import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d

CAT = "notation"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def mark(S, x, y, r=1.75):
    """Plotted point: square in Line, round in Rounded; knocked out of a Filled shell."""
    if S.name == "line":
        s = r * 1.77
        return Part("dot", rect(x - s / 2, y - s / 2, s, s))
    return dot(x, y, r)


def hidden(S, d, n, dash=2.0):
    """Hidden edge along path d: n dashes in Line, n dots in Rounded (evenly spaced along the path)."""
    from pathops import Path as _P  # noqa: F401
    from fontTools.pens.basePen import BasePen  # noqa: F401
    pts = _sample(d, 200)
    total = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
    acc = [0.0]
    for i in range(len(pts) - 1):
        acc.append(acc[-1] + math.dist(pts[i], pts[i + 1]))

    def at(s):
        for i in range(len(acc) - 1):
            if acc[i + 1] >= s:
                f = (s - acc[i]) / max(acc[i + 1] - acc[i], 1e-9)
                return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)
        return pts[-1]
    out = []
    step = (total - dash) / (n - 1)
    for k in range(n):
        s0 = k * step
        if S.name == "line":
            a, b = at(s0), at(s0 + dash)
            out.append(line(seg(*a, *b)))
        else:
            out.append(dot(*at(s0 + dash / 2), 1.1))
    return out


def _sample(d, n):
    from fontTools.pens.recordingPen import RecordingPen
    from fontTools.svgLib.path import parse_path
    rec = RecordingPen()
    parse_path(d, rec)
    pts, cur = [], None
    for op, args in rec.value:
        if op == "moveTo":
            cur = args[0]
            pts.append(cur)
        elif op == "lineTo":
            cur = args[0]
            pts.append(cur)
        elif op in ("curveTo", "qCurveTo"):
            ctrl = [cur, *args]
            for i in range(1, n + 1):
                t = i / n
                if len(ctrl) == 4:
                    p0, p1, p2, p3 = ctrl
                    u = 1 - t
                    pts.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                                u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
                else:
                    p0, p1, p2 = ctrl
                    u = 1 - t
                    pts.append((u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0], u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]))
            cur = args[-1]
    return pts


def dashes(p0, p1, n, dash=2.0):
    """n equal dashes spread evenly along p0 -> p1, first and last touching the ends (open line parts)."""
    (x0, y0), (x1, y1) = p0, p1
    length = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / length, (y1 - y0) / length
    gap = (length - n * dash) / (n - 1) if n > 1 else 0
    out = []
    for i in range(n):
        s = i * (dash + gap)
        out.append(line(seg(x0 + ux * s, y0 + uy * s, x0 + ux * (s + dash), y0 + uy * (s + dash))))
    return out


def integral_d(S, x, t=3.5, b=20.5, h=3.0):
    """One slender integral sign with its stem at x, from y=t to y=b."""
    if S.name == "line":
        return (f"M{fmt(x + h)} {fmt(t)}H{fmt(x + 1.8)}C{fmt(x + 0.7)} {fmt(t)} {fmt(x)} {fmt(t + 0.7)} {fmt(x)} {fmt(t + 1.8)}"
                f"V{fmt(b - 1.8)}C{fmt(x)} {fmt(b - 0.7)} {fmt(x - 0.7)} {fmt(b)} {fmt(x - 1.8)} {fmt(b)}H{fmt(x - h)}")
    return (f"M{fmt(x + h)} {fmt(t + 1.5)}C{fmt(x + h)} {fmt(t + 0.5)} {fmt(x + h - 0.8)} {fmt(t)} {fmt(x + 1.6)} {fmt(t)}"
            f"C{fmt(x + 0.5)} {fmt(t)} {fmt(x)} {fmt(t + 1)} {fmt(x)} {fmt(t + 3)}V{fmt(b - 3)}"
            f"C{fmt(x)} {fmt(b - 1)} {fmt(x - 0.5)} {fmt(b)} {fmt(x - 1.6)} {fmt(b)}"
            f"C{fmt(x - h + 0.8)} {fmt(b)} {fmt(x - h)} {fmt(b - 0.5)} {fmt(x - h)} {fmt(b - 1.5)}")


# ============================================================================ Greek and Hebrew letters

@icon("zeta", CAT, "Greek small letter zeta.", tags=["greek", "letter", "zeta function", "damping", "math"])
def _(S):
    return [line("M8 3.5H16.5C12 7 7 10.8 7 14.5C7 16.8 8.8 17.5 11.8 17.5C14.3 17.5 15.5 18.3 15.5 19.4C15.5 20.4 14.6 21 13.5 21",
                 stroke_miterlimit="8")]


@icon("eta-letter", CAT, "Greek small letter eta.", tags=["greek", "letter", "eta", "efficiency", "viscosity", "math"])
def _(S):
    return [line("M5.5 7.5C6.6 6.6 8 7 8 8.5V17.5"),
            line("M8 11C8 8.5 10 6.5 12.5 6.5C15 6.5 17 8.3 17 11V21")]


@icon("xi", CAT, "Greek small letter xi.", tags=["greek", "letter", "xi", "random variable", "math"])
def _(S):
    return [line(seg(8, 3.5, 16.5, 3.5)),
            line("M15.5 3.5C11 3.5 8.5 5 8.5 7C8.5 9 10.5 10.2 13.5 10.2"),
            line("M13.5 10.2C9.5 10.2 7 12 7 14.3C7 16.7 9.5 17.8 13 17.8C15 17.8 16 18.6 16 19.6C16 20.5 15.2 21 14.2 21")]


@icon("rho", CAT, "Greek small letter rho.", tags=["greek", "letter", "rho", "density", "correlation", "math"])
def _(S):
    return [line("M7.5 21V11.5A5.25 5.25 0 0 1 18 11.5A5.25 5.25 0 0 1 7.5 11.5")]


@icon("tau", CAT, "Greek small letter tau.", tags=["greek", "letter", "tau", "torque", "time constant", "math"])
def _(S):
    return [line(L(S, "M4.5 7.5L6 6.5H19.5", "M4.5 7.8C5.5 7 6.5 6.5 8 6.5H19.5")),
            line("M12.5 6.5V15.5C12.5 17.4 13.5 18.2 15 18.2C16 18.2 16.8 17.8 17.5 17.2")]


@icon("chi", CAT, "Greek small letter chi.", tags=["greek", "letter", "chi", "chi squared", "statistics", "math"])
def _(S):
    return [line("M4.5 7C6.5 6.5 7.8 7.6 9 9.5L14.8 19C15.8 20.6 17 21.3 19.5 21"),
            line(seg(18.5, 7, 5.5, 21))]


@icon("psi", CAT, "Greek letter psi: a cup crossed by a tall stem.", tags=["greek", "letter", "psi", "wave function", "psychology", "math"])
def _(S):
    return [line("M5 6.5V10C5 13.9 8.1 16 12 16C15.9 16 19 13.9 19 10V6.5"), line(seg(12, 3.5, 12, 21))]


@icon("kappa-letter", CAT, "Greek small letter kappa.", tags=["greek", "letter", "kappa", "curvature", "math"])
def _(S):
    return [line(seg(7, 6.5, 7, 17.5)),
            line(L(S, "M7 13L17 6.5", "M7 13L14.8 7.6C15.5 7.1 16.2 6.8 17 6.8")),
            line(L(S, "M10.5 10.8L17.5 17.5", "M10.5 10.8L15.3 15.8C16 16.5 16.7 17 17.8 17.2"))]


@icon("aleph", CAT, "Hebrew letter aleph, the symbol for infinite cardinal numbers.",
      tags=["hebrew", "letter", "cardinal", "infinity", "set theory", "math"])
def _(S):
    return [line("M5.5 4.5C6.8 4.5 7.6 5 8.3 6L16 18.3C16.7 19.4 17.5 20 18.5 20"),
            line("M13.6 11.5C16.2 10.5 17.8 8.5 17.2 4.5"),
            line("M10.3 12.6C7.7 13.7 6.2 16 6.8 20")]


@icon("h-bar", CAT, "Reduced Planck constant: an h with a bar across its stem.",
      tags=["planck", "h bar", "dirac constant", "quantum", "physics"])
def _(S):
    return [line(seg(9, 3.5, 5.8, 20.5)),
            line("M7.2 13.3C8.4 10.6 10.4 9 12.6 9C14.6 9 15.6 10.4 15.1 12.4L13.9 17.3C13.5 19.1 14.2 20.5 15.6 20.5C16.6 20.5 17.5 19.9 18.2 19"),
            line(seg(4.5, 9, 13, 5.5))]


@icon("partial-derivative", CAT, "Partial derivative sign, a backward 6 with a curled top.",
      tags=["partial", "derivative", "calculus", "del", "differential", "math"])
def _(S):
    return [line("M6.5 6C7.5 4.4 8.9 3.5 10.8 3.5C14.6 3.5 17 7.5 17 14.5A5.5 5.5 0 0 1 6 14.5A5.5 5.5 0 0 1 11.5 9C13.8 9 15.8 10.3 16.8 12.3")]


@icon("double-integral", CAT, "Double integral sign: two integral signs side by side.",
      tags=["integral", "double", "area", "calculus", "math"])
def _(S):
    return [line(integral_d(S, 9)), line(integral_d(S, 15))]


@icon("triple-integral", CAT, "Triple integral sign: three slender integral signs.",
      tags=["integral", "triple", "volume", "calculus", "math"])
def _(S):
    return [line(integral_d(S, x, h=2.3)) for x in (6, 12, 18)]


@icon("contour-integral", CAT, "Contour integral: an integral sign threaded through a small circle.",
      tags=["integral", "closed", "line integral", "loop", "calculus", "math"])
def _(S):
    return [line(integral_d(S, 12, h=4.5)), line(circle(12, 12, 3.75))]


# ============================================================================ operators and relations

def _x(cx, cy, s=3.5):
    return [line(seg(cx - s, cy - s, cx + s, cy + s)), line(seg(cx + s, cy - s, cx - s, cy + s))]


@icon("absolute-value", CAT, "Absolute value: an x between two vertical bars.",
      tags=["absolute", "modulus", "magnitude", "norm", "bars", "math"])
def _(S):
    return [line(seg(4.5, 3.5, 4.5, 20.5)), line(seg(19.5, 3.5, 19.5, 20.5)), *_x(12, 12)]


@icon("floor-function", CAT, "Floor function: an x inside brackets with only bottom feet.",
      tags=["floor", "round down", "integer part", "brackets", "math"])
def _(S):
    return [line(poly([(4.5, 3.5), (4.5, 20.5), (8.5, 20.5)], r=S.r)),
            line(poly([(19.5, 3.5), (19.5, 20.5), (15.5, 20.5)], r=S.r)), *_x(12, 11.5)]


@icon("proportional-to", CAT, "Proportional-to sign: a sideways loop open to the right.",
      tags=["proportional", "varies as", "ratio", "relation", "math"])
def _(S):
    return [line("M20 7.5C16.3 7.5 14.2 9.7 12 12C9.8 14.3 8.7 16.5 6.5 16.5C4.8 16.5 3.5 14.5 3.5 12C3.5 9.5 4.8 7.5 6.5 7.5"
                 "C8.7 7.5 9.8 9.7 12 12C14.2 14.3 16.3 16.5 20 16.5")]


def _tilde(x0, x1, y):
    w = x1 - x0
    return (f"M{fmt(x0)} {fmt(y + 1)}C{fmt(x0 + w * 0.09)} {fmt(y - 1)} {fmt(x0 + w * 0.25)} {fmt(y - 1.8)} {fmt(x0 + w * 0.41)} {fmt(y - 0.3)}"
            f"C{fmt(x0 + w * 0.59)} {fmt(y + 1.3)} {fmt(x0 + w * 0.76)} {fmt(y + 1.8)} {fmt(x1)} {fmt(y - 1)}")


@icon("congruent", CAT, "Congruence sign: a tilde above two parallel bars.",
      tags=["congruent", "congruence", "same shape", "equal", "geometry", "math"])
def _(S):
    return [line(_tilde(5, 19, 6)), line(seg(5, 13, 19, 13)), line(seg(5, 19, 19, 19))]


@icon("similar-to", CAT, "Similarity: a small and a large triangle with a tilde above.",
      tags=["similar", "similarity", "same shape", "scale", "geometry", "math"])
def _(S):
    return [line(_tilde(6, 18, 5)),
            shell(poly([(6, 14), (9.5, 20), (2.5, 20)], closed=True, r=L(S, 0, 1))),
            shell(poly([(16.5, 10), (21.5, 20), (11.5, 20)], closed=True, r=L(S, 0, 1.5)))]


@icon("perpendicular", CAT, "Perpendicular sign: an upright line on a base with a right-angle mark.",
      tags=["perpendicular", "right angle", "orthogonal", "up tack", "geometry", "math"])
def _(S):
    return [line(seg(12, 3, 12, 19.5)), line(seg(3, 20.5, 21, 20.5)),
            line(poly([(12, 15.5), (16, 15.5), (16, 19.5)], r=S.r * 0.5))]


@icon("parallel-lines-symbol", CAT, "Parallel sign: two slanted parallel strokes.",
      tags=["parallel", "parallel lines", "relation", "geometry", "math"])
def _(S):
    return [line(seg(11, 3.5, 5, 20.5)), line(seg(19, 3.5, 13, 20.5))]


def _letter_a(x0, y0, w, h):
    """Capital A as two lines (apex and legs, crossbar)."""
    return [line(poly([(x0, y0 + h), (x0 + w / 2, y0), (x0 + w, y0 + h)])),
            line(seg(x0 + w * 0.22, y0 + h * 0.62, x0 + w * 0.78, y0 + h * 0.62))]


def _letter_b(S, x0, y0, w, h):
    m = y0 + h * 0.46
    r1, r2 = (m - y0) / 2, (y0 + h - m) / 2
    return [line(f"M{fmt(x0)} {fmt(m)}H{fmt(x0 + w - r2)}A{fmt(r2)} {fmt(r2)} 0 0 1 {fmt(x0 + w - r2)} {fmt(y0 + h)}H{fmt(x0)}V{fmt(y0)}"
                 f"H{fmt(x0 + w - r2 - 0.5)}A{fmt(r1)} {fmt(r1)} 0 0 1 {fmt(x0 + w - r2 - 0.5)} {fmt(m)}")]


@icon("arc-notation", CAT, "Arc notation: letters A and B under a curved arc.",
      tags=["arc", "arc ab", "circle arc", "geometry", "notation", "math"])
def _(S):
    return [line("M3.5 8C7 3.5 17 3.5 20.5 8"), *_letter_a(3, 11, 8, 9.5), *_letter_b(S, 13.5, 11, 7, 9.5)]


@icon("line-segment-notation", CAT, "Line segment notation: letters A and B under a straight bar.",
      tags=["line segment", "segment ab", "bar", "geometry", "notation", "math"])
def _(S):
    return [line(seg(3, 5.5, 21, 5.5)), *_letter_a(3, 11, 8, 9.5), *_letter_b(S, 13.5, 11, 7, 9.5)]


# ============================================================================ number sets (blackboard bold)

@icon("natural-numbers", CAT, "Blackboard bold N, the set of natural numbers.",
      tags=["natural numbers", "counting numbers", "set", "blackboard bold", "math"])
def _(S):
    return [line(rect(4, 3.5, 4, 17, L(S, 0, 1.5))), line(seg(8, 3.5, 20, 20.5)), line(seg(20, 3.5, 20, 20.5))]


@icon("integers-set", CAT, "Blackboard bold Z, the set of integers.",
      tags=["integers", "whole numbers", "set", "blackboard bold", "math"])
def _(S):
    return [line(poly([(14.4, 3.5), (19, 3.5), (9.6, 20.5), (5, 20.5)], closed=True, r=L(S, 0, 0.8))),
            line(seg(5, 3.5, 14.4, 3.5)), line(seg(9.6, 20.5, 19, 20.5))]


@icon("rational-numbers", CAT, "Blackboard bold Q, the set of rational numbers.",
      tags=["rational numbers", "fractions", "set", "blackboard bold", "math"])
def _(S):
    dy = math.sqrt(8.5 ** 2 - 4 ** 2)
    return [line(circle(12, 11.5, 8.5)), line(seg(8, 11.5 - dy, 8, 11.5 + dy)), line(seg(14, 16.5, 19.5, 22))]


@icon("real-numbers", CAT, "Blackboard bold R, the set of real numbers.",
      tags=["real numbers", "reals", "set", "blackboard bold", "math"])
def _(S):
    return [line(rect(4.5, 3.5, 4, 17, L(S, 0, 1.5))),
            line("M8.5 3.5H14.25A4.5 4.5 0 0 1 14.25 12.5H8.5"), line(seg(13.5, 12.5, 19.5, 20.5))]


@icon("complex-numbers", CAT, "Blackboard bold C, the set of complex numbers.",
      tags=["complex numbers", "imaginary", "set", "blackboard bold", "math"])
def _(S):
    dy = math.sqrt(8.5 ** 2 - 4 ** 2)
    return [line(arc(12, 12, 8.5, 42, 318)), line(seg(8, 12 - dy, 8, 12 + dy))]


# ============================================================================ logic and algebra

@icon("logical-not", CAT, "Logical negation sign: a bar with a hook down at its right end.",
      tags=["not", "negation", "logic", "boolean", "math"])
def _(S):
    return [line(poly([(3.5, 8.5), (20, 8.5), (20, 16.5)], r=S.r))]


@icon("implies", CAT, "Implication sign: a double-stroke arrow pointing right.",
      tags=["implies", "implication", "then", "logic", "double arrow", "math"])
def _(S):
    return [line(seg(3.5, 9, 17, 9)), line(seg(3.5, 15, 17, 15)),
            line(poly([(13, 4.5), (20.5, 12), (13, 19.5)], r=S.r))]


@icon("if-and-only-if", CAT, "Biconditional sign: a double-stroke arrow with heads at both ends.",
      tags=["iff", "biconditional", "equivalent", "logic", "double arrow", "math"])
def _(S):
    return [line(seg(7, 9, 17, 9)), line(seg(7, 15, 17, 15)),
            line(poly([(15.5, 5), (21, 12), (15.5, 19)], r=S.r)),
            line(poly([(8.5, 5), (3, 12), (8.5, 19)], r=S.r))]


@icon("maps-to", CAT, "Maps-to sign: an arrow pointing right from a short bar.",
      tags=["maps to", "mapping", "function", "arrow", "math"])
def _(S):
    return [line(seg(4, 7, 4, 17)), line(seg(4, 12, 19.5, 12)), line(poly([(15, 7.5), (19.5, 12), (15, 16.5)], r=S.r))]


@icon("binomial-coefficient", CAT, "Binomial coefficient: n above k inside tall parentheses.",
      tags=["binomial", "n choose k", "combinations", "combinatorics", "math"])
def _(S):
    return [line("M6.5 3C4.5 5.5 3.5 8.5 3.5 12C3.5 15.5 4.5 18.5 6.5 21"),
            line("M17.5 3C19.5 5.5 20.5 8.5 20.5 12C20.5 15.5 19.5 18.5 17.5 21"),
            line(seg(9.5, 5.5, 9.5, 10.5)), line("M9.5 7.8C9.5 6.4 10.5 5.5 12 5.5C13.5 5.5 14.5 6.4 14.5 7.8V10.5"),
            line(seg(9.5, 13, 9.5, 20.5)), line(poly([(14.5, 15), (9.5, 18.3)])), line(seg(11.5, 17, 14.8, 20.5))]


@icon("basis-point", CAT, "Per ten thousand sign: a slash with one ring above and three rings below.",
      tags=["basis point", "bps", "per ten thousand", "permyriad", "finance", "math"])
def _(S):
    return [line(seg(12.5, 3, 5.5, 13.5)),
            shell(ellipse(5.5, 6, 1.75, 2.5)),
            shell(ellipse(4.5, 18, 1.5, 2.5)), shell(ellipse(12, 18, 1.5, 2.5)), shell(ellipse(19.5, 18, 1.5, 2.5))]


@icon("system-of-equations", CAT, "System of equations: two stacked equations joined by a curly brace.",
      tags=["simultaneous equations", "system", "brace", "algebra", "equations", "math"])
def _(S):
    brace = "M7.5 3.5C5.8 3.5 5 4.3 5 6V9.5C5 11 4.3 12 2.8 12C4.3 12 5 13 5 14.5V18C5 19.7 5.8 20.5 7.5 20.5"
    return [line(brace),
            *_x(12, 7.5, 2.5), line(seg(17, 5.5, 21, 5.5)), line(seg(17, 9.5, 21, 9.5)),
            line(seg(9.5, 14, 12, 17.5)), line("M14.5 14L11 20.5C10.6 21.2 10.1 21.5 9.5 21.5"),
            line(seg(17, 14.5, 21, 14.5)), line(seg(17, 18.5, 21, 18.5))]


@icon("quadratic-equation", CAT, "Quadratic: x squared beside the parabola it draws.",
      tags=["quadratic", "x squared", "parabola", "polynomial", "algebra", "math"])
def _(S):
    two = "M13.5 5.3C13.5 4.2 14.4 3.5 15.6 3.5C16.8 3.5 17.7 4.2 17.7 5.3C17.7 6.5 16.3 7.2 13.5 9H18"
    return [line(two, stroke_miterlimit="2"), *_x(9.5, 8.25, 2.25),
            line("M2.5 4Q12 37 21.5 4")]


def _vec_arrow(S, x0, x1, y):
    return [line(seg(x0, y, x1, y)), line(poly([(x1 - 2.5, y - 2.5), (x1, y), (x1 - 2.5, y + 2.5)], r=S.r * 0.5))]


@icon("dot-product", CAT, "Dot product: two vectors u and v separated by a centred dot.",
      tags=["dot product", "scalar product", "inner product", "vectors", "linear algebra", "math"])
def _(S):
    return [*_vec_arrow(S, 2.5, 9.5, 6.5), line("M3 11.5V15.5C3 17.5 4.2 19 6 19C7.8 19 9 17.5 9 15.5V11.5"),
            dot(12, 15, 1.6),
            *_vec_arrow(S, 14.5, 21.5, 6.5), line(poly([(15, 11.5), (18, 19), (21, 11.5)], r=S.r * 0.5))]


@icon("function-composition", CAT, "Function composition: f and g joined by a small ring.",
      tags=["composition", "compose", "f of g", "functions", "math"])
def _(S):
    return [line("M9.5 4.3C9 3.8 8.3 3.5 7.6 3.5C6.3 3.5 5.5 4.4 5.5 6V19.5"), line(seg(3, 9.5, 8.5, 9.5)),
            line(circle(12, 13.5, 1.75)),
            line(circle(17.75, 12.25, 2.75)),
            line("M20.5 9.5V18.5C20.5 20.3 19.4 21.3 17.8 21.3C16.8 21.3 16 21 15.4 20.5")]


@icon("transpose-matrix", CAT, "Matrix transpose: a bracketed matrix with a raised T.",
      tags=["transpose", "matrix", "linear algebra", "superscript t", "math"])
def _(S):
    return [line(poly([(5.5, 7.5), (3, 7.5), (3, 20.5), (5.5, 20.5)], r=S.r)),
            line(poly([(12.5, 7.5), (15, 7.5), (15, 20.5), (12.5, 20.5)], r=S.r)),
            dot(7, 11.5, 1.25), dot(11, 11.5, 1.25), dot(7, 16.5, 1.25), dot(11, 16.5, 1.25),
            line(seg(16, 3.5, 22, 3.5)), line(seg(19, 3.5, 19, 10))]


@icon("imaginary-unit", CAT, "Imaginary unit: the letter i beside the square root of minus one.",
      tags=["imaginary", "i", "square root of minus one", "complex", "math"])
def _(S):
    return [line(seg(4, 10, 4, 20.5)), dot(4, 5.5, 1.5),
            line(poly([(7, 14.5), (8.5, 13.5), (11, 20.5), (14, 5), (21.5, 5)], r=S.r * 0.5), stroke_miterlimit="2"),
            line(seg(13.5, 13.5, 16, 13.5)), line(poly([(17.5, 11), (19.5, 9.5), (19.5, 19)], r=S.r * 0.5))]


# ============================================================================ graphs and coordinates

@icon("parabola", CAT, "Parabola: a U-shaped curve on x and y axes with its vertex marked.",
      tags=["parabola", "quadratic", "curve", "graph", "vertex", "math"])
def _(S):
    return [line(seg(5, 2.5, 5, 21.5)), line(seg(2.5, 18.5, 21.5, 18.5)),
            line("M7.5 3.5Q14 25 20.5 3.5"), mark(S, 14, 14.25, 2)]


@icon("ellipse-foci", CAT, "Ellipse with its two foci and lines from each focus to one point on the curve.",
      tags=["ellipse", "foci", "focus", "conic", "orbit", "geometry", "math"])
def _(S):
    p = (12 + 10 * math.cos(math.radians(-90)), 12 + 7.5 * math.sin(math.radians(-90)))
    return [shell(ellipse(12, 12, 10, 7.5)),
            detail(seg(6.5, 13.5, 11, 6.5)), detail(seg(17.5, 13.5, 13, 6.5)),
            mark(S, 6.5, 13.5, 1.75), mark(S, 17.5, 13.5, 1.75)]


@icon("unit-circle", CAT, "Unit circle on crossed axes with a radius to a point and its angle marked.",
      tags=["unit circle", "trigonometry", "sine", "cosine", "angle", "radius", "math"])
def _(S):
    p = pt_on(12, 12, 8, -45)
    return [line(seg(2.5, 12, 21.5, 12)), line(seg(12, 2.5, 12, 21.5)), line(circle(12, 12, 8)),
            line(seg(12, 12, *p)), mark(S, *p, 2), line(arc(12, 12, 4.5, -45, 0))]


@icon("polar-grid", CAT, "Polar coordinate grid: concentric rings, radial spokes and one plotted point.",
      tags=["polar", "coordinates", "polar grid", "radius", "angle", "graph", "math"])
def _(S):
    o = (3.5, 20.5)
    parts = [line(poly([(3.5, 3), o, (21, 20.5)], r=S.r)),
             line(arc(*o, 8.5, -90, 0)), line(arc(*o, 16.5, -90, 0))]
    for a in (-30, -60):
        parts.append(line(seg(*o, *pt_on(*o, 17.5, a))))
    parts.append(mark(S, *pt_on(*o, 12.5, -45), 2))
    return parts


@icon("three-d-axes", CAT, "Three coordinate axes from one origin: x, y and z with arrowheads.",
      tags=["3d axes", "xyz", "three dimensions", "coordinate system", "cartesian", "math"])
def _(S):
    o = (9.5, 14)
    return [line(seg(*o, 9.5, 3.5)), line(poly([(7, 6), (9.5, 3.5), (12, 6)], r=S.r * 0.5)),
            line(seg(*o, 21, 14)), line(poly([(18.5, 11.5), (21, 14), (18.5, 16.5)], r=S.r * 0.5)),
            line(seg(*o, 3.5, 20)), line(poly([(3.5, 16.5), (3.5, 20), (7, 20)], r=S.r * 0.5))]


@icon("slope-triangle", CAT, "Slope: a rising line with a right triangle beneath it showing rise over run.",
      tags=["slope", "gradient", "rise over run", "incline", "linear", "graph", "math"])
def _(S):
    return [line(poly([(3.5, 3.5), (3.5, 20.5), (20.5, 20.5)], r=S.r)),
            line(seg(6, 17.5, 20.5, 3.5)),
            line(poly([(9.5, 14.2), (16.3, 14.2), (16.3, 7.6)], r=S.r * 0.5))]


# ============================================================================ fractals and topology

def smooth(pts, closed=False, k=1.0) -> str:
    """Catmull-Rom spline through pts as cubic Beziers (k = tension)."""
    n = len(pts)
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[(i + 1) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) * k / 6, p1[1] + (p2[1] - p0[1]) * k / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) * k / 6, p2[1] - (p3[1] - p1[1]) * k / 6)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d + ("Z" if closed else "")


def _shrink(tri, by):
    cx, cy = sum(p[0] for p in tri) / 3, sum(p[1] for p in tri) / 3
    return [(cx + (x - cx) * by, cy + (y - cy) * by) for x, y in tri]


def _sierpinski(level):
    top, left, right = (12, 3.4), (2, 20.72), (22, 20.72)
    tris = [(top, left, right)]
    for _ in range(level):
        nxt = []
        for a, b, c in tris:
            ab, bc, ca = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), ((b[0] + c[0]) / 2, (b[1] + c[1]) / 2), ((c[0] + a[0]) / 2, (c[1] + a[1]) / 2)
            nxt += [(a, ab, ca), (ab, b, bc), (ca, bc, c)]
        tris = nxt
    return tris


def _sierpinski_filled():
    return U(*[P(poly(_shrink(t, 0.9), closed=True)) for t in _sierpinski(2)])


@icon("sierpinski-triangle", CAT, "Sierpinski triangle: a triangle split into smaller triangles with the middles left empty.",
      tags=["sierpinski", "fractal", "triangle", "self similar", "recursion", "math"], filled=_sierpinski_filled)
def _(S):
    return [solid(poly(_shrink(t, 0.8), closed=True, r=L(S, 0, 0.6))) for t in _sierpinski(2)]


def _koch(level=2, r=10.0):
    pts = regular(12, 12.6, r, 3, -90)
    for _ in range(level):
        out = []
        for i in range(len(pts)):
            a, b = pts[i], pts[(i + 1) % len(pts)]
            dx, dy = (b[0] - a[0]) / 3, (b[1] - a[1]) / 3
            p1, p3 = (a[0] + dx, a[1] + dy), (a[0] + 2 * dx, a[1] + 2 * dy)
            # outward bump: rotate the middle third by -60 degrees (screen coordinates, clockwise outline)
            c, s = math.cos(math.radians(-60)), math.sin(math.radians(-60))
            p2 = (p1[0] + dx * c - dy * s, p1[1] + dx * s + dy * c)
            out += [a, p1, p2, p3]
        pts = out
    return pts


@icon("koch-snowflake", CAT, "Koch snowflake: a six-pointed fractal outline with smaller bumps on every edge.",
      tags=["koch", "snowflake", "fractal", "self similar", "recursion", "math"])
def _(S):
    return [shell(poly(_koch(), closed=True, r=L(S, 0, 0.4)), stroke_miterlimit="2")]


def _mandelbrot_d():
    k, ox, oy = 12.4, 2.8 + 1.25 * 12.4, 12.0  # scale and screen position of c = 0
    card = []
    for i in range(28):
        t = 2 * math.pi * i / 28
        x = 0.5 * math.cos(t) - 0.25 * math.cos(2 * t)
        y = 0.5 * math.sin(t) - 0.25 * math.sin(2 * t)
        card.append((ox + x * k, oy + y * k))
    body = P(smooth(card, closed=True))
    bulb = P(circle(ox - 1.0 * k, oy, 0.27 * k))
    buds = [P(circle(ox - 0.12 * k, oy - 0.62 * k, 1.9)), P(circle(ox - 0.12 * k, oy + 0.62 * k, 1.9))]
    return path_to_d(U(body, bulb, *buds))


@icon("mandelbrot-set", CAT, "Mandelbrot set: a heart-shaped cardioid with a round bulb on its left and small buds.",
      tags=["mandelbrot", "fractal", "complex plane", "chaos", "math"])
def _(S):
    return [shell(_mandelbrot_d(), stroke_miterlimit="2")]


@icon("fractal-tree", CAT, "Fractal tree: a trunk that splits into two branches, each splitting again.",
      tags=["fractal tree", "binary tree", "branching", "recursion", "fractal", "math"])
def _(S):
    n0, nl, nr = (12, 14.5), (7, 9.5), (17, 9.5)
    return [line(seg(12, 21.5, *n0)),
            line(poly([nl, n0, nr], r=S.r)),
            line(poly([(3.5, 6), nl, (8.5, 3)], r=S.r)),
            line(poly([(15.5, 3), nr, (20.5, 6)], r=S.r))]


def _seg_cross(a, b, c, d):
    r, q = (b[0] - a[0], b[1] - a[1]), (d[0] - c[0], d[1] - c[1])
    den = r[0] * q[1] - r[1] * q[0]
    if abs(den) < 1e-12:
        return False
    t = ((c[0] - a[0]) * q[1] - (c[1] - a[1]) * q[0]) / den
    u = ((c[0] - a[0]) * r[1] - (c[1] - a[1]) * r[0]) / den
    return 0 <= t < 1 and 0 <= u < 1


def _trefoil_strands(scale=3.3, cx=12.0, cy=10.45, gap=2.6, step=10):
    """Trefoil centreline split into three strands, with a gap where each strand passes under another."""
    n = 360
    pts = [(cx + scale * (math.sin(t) + 2 * math.sin(2 * t)), cy - scale * (math.cos(t) - 2 * math.cos(2 * t)))
           for t in (2 * math.pi * i / n for i in range(n))]
    hits = []
    for i in range(n):
        for j in range(i + 2, n):
            if (j + 1) % n != i and _seg_cross(pts[i], pts[(i + 1) % n], pts[j], pts[(j + 1) % n]):
                hits += [i, j]
    hits.sort()
    under = hits[1::2]  # crossings alternate over / under along the curve
    keep = [all(not (math.dist(pts[k], pts[u]) < gap and min(abs(k - u), n - abs(k - u)) < 30) for u in under) for k in range(n)]
    start = next(k for k in range(n) if not keep[k] and keep[(k + 1) % n]) + 1
    strands, cur = [], []
    for m in range(n):
        k = (start + m) % n
        if keep[k]:
            cur.append(pts[k])
        elif cur:
            strands.append(cur)
            cur = []
    if cur:
        strands.append(cur)
    out = []
    for st in strands:
        sel = st[::step]
        if sel[-1] != st[-1]:
            sel.append(st[-1])
        out.append(smooth(sel))
    return out


@icon("trefoil-knot", CAT, "Trefoil knot: a closed three-lobed loop that crosses over and under itself.",
      tags=["trefoil", "knot", "knot theory", "topology", "loop", "math"])
def _(S):
    return [line(d) for d in _trefoil_strands()]


# ============================================================================ solids

@icon("tesseract", CAT, "Tesseract: a small cube inside a larger one with their corners joined.",
      tags=["tesseract", "hypercube", "4d", "fourth dimension", "geometry", "math"])
def _(S):
    return [shell(rect(3, 3, 18, 18, L(S, 0, 2))), detail(rect(8.5, 8.5, 7, 7, L(S, 0, 1))),
            detail(seg(3.6, 3.6, 8.5, 8.5)), detail(seg(20.4, 3.6, 15.5, 8.5)),
            detail(seg(3.6, 20.4, 8.5, 15.5)), detail(seg(20.4, 20.4, 15.5, 15.5))]


@icon("octahedron", CAT, "Octahedron: two square pyramids joined base to base, with visible edges.",
      tags=["octahedron", "polyhedron", "platonic solid", "d8", "geometry", "3d"])
def _(S):
    top, bot, lft, rgt, frt = (12, 2.5), (12, 21.5), (3, 11), (21, 11), (8.5, 15)
    return [shell(poly([top, rgt, bot, lft], closed=True, r=L(S, 0, 1.2)), stroke_miterlimit="2"),
            detail(poly([lft, frt, rgt], r=S.r * 0.5)), detail(seg(*top, *frt)), detail(seg(*frt, *bot))]


@icon("dodecahedron", CAT, "Dodecahedron: a pentagon face surrounded by five more inside a ten-sided outline.",
      tags=["dodecahedron", "polyhedron", "platonic solid", "d12", "pentagon", "geometry"])
def _(S):
    outer = regular(12, 12, 10, 10, -90)
    inner = regular(12, 12.2, 4.8, 5, -90)
    parts = [shell(poly(outer, closed=True, r=L(S, 0, 2.5))), detail(poly(inner, closed=True, r=L(S, 0, 1.8)))]
    for i in range(5):
        a, b = pt_on(12, 12.2, 4.8 + L(S, 0, 0.6), -90 + 72 * i), pt_on(12, 12, 10 - L(S, 0, 0.7), -90 + 72 * i)
        parts.append(detail(seg(*a, *b)))
    return parts


@icon("icosahedron", CAT, "Icosahedron: triangular faces in a hexagonal outline around a central triangle.",
      tags=["icosahedron", "polyhedron", "platonic solid", "d20", "triangles", "geometry"])
def _(S):
    H = {a: pt_on(12, 12, 10, a) for a in (-90, -30, 30, 90, 150, 210)}
    T = {a: pt_on(12, 12.5, 4.6, a) for a in (-90, 30, 150)}
    parts = [shell(poly([H[a] for a in (-90, -30, 30, 90, 150, 210)], closed=True, r=L(S, 0, 3))),
             detail(poly([T[-90], T[30], T[150]], closed=True, r=L(S, 0, 1.6)))]
    for t, hs in ((-90, (-90, -30, 210)), (30, (-30, 30, 90)), (150, (90, 150, 210))):
        for h in hs:
            parts.append(detail(seg(*T[t], *pt_on(12, 12, 10 - L(S, 0, 0.6), h))))
    return parts


def _frustum_filled():
    sil = U(P(ellipse(12, 6, 5, 2.5)), P(poly([(7, 6), (17, 6), (21, 18), (3, 18)], closed=True)), P(ellipse(12, 18, 9, 3.5)))
    sil = U(sil, ST(path_to_d(sil), 2))
    return D(sil, ST("M7 6A5 2.5 0 0 0 17 6", 2))


@icon("frustum", CAT, "Frustum: a cone with its top sliced off flat, showing elliptical top and base.",
      tags=["frustum", "truncated cone", "solid", "geometry", "3d"], filled=_frustum_filled)
def _(S):
    return [shell(ellipse(12, 6, 5, 2.5)), line("M7 6L3 18A9 3.5 0 0 0 21 18L17 6"),
            *hidden(S, "M5 15.8A9 3.5 0 0 1 19 15.8", 4, 1.6)]


@icon("cube-net", CAT, "Cube net: six squares in a cross, the flat pattern that folds into a cube.",
      tags=["cube net", "net", "unfolded cube", "template", "geometry", "3d"])
def _(S):
    s, x0, y0 = 5.5, 3.75, 1.0
    X = [x0 + i * s for i in range(4)]
    Y = [y0 + j * s for j in range(5)]
    outline = [(X[1], Y[0]), (X[2], Y[0]), (X[2], Y[1]), (X[3], Y[1]), (X[3], Y[2]), (X[2], Y[2]), (X[2], Y[4]),
               (X[1], Y[4]), (X[1], Y[2]), (X[0], Y[2]), (X[0], Y[1]), (X[1], Y[1])]
    return [shell(poly(outline, closed=True, r=L(S, 0, 0.8))),
            detail(seg(X[1], Y[1], X[2], Y[1])), detail(seg(X[1], Y[2], X[2], Y[2])), detail(seg(X[1], Y[3], X[2], Y[3])),
            detail(seg(X[1], Y[1] + 0.01, X[1], Y[2] - 0.01)), detail(seg(X[2], Y[1] + 0.01, X[2], Y[2] - 0.01))]


@icon("hexagonal-prism", CAT, "Hexagonal prism: an upright prism with hexagonal ends in perspective.",
      tags=["hexagonal prism", "prism", "hexagon", "solid", "geometry", "3d"])
def _(S):
    top = [(20.5, 5.5), (16.25, 8.3), (7.75, 8.3), (3.5, 5.5), (7.75, 2.7), (16.25, 2.7)]
    h = 13.5
    outline = [(3.5, 5.5), (7.75, 2.7), (16.25, 2.7), (20.5, 5.5), (20.5, 5.5 + h), (16.25, 8.3 + h), (7.75, 8.3 + h), (3.5, 5.5 + h)]
    return [shell(poly(outline, closed=True, r=L(S, 0, 3))),
            detail(poly(top[:4], r=L(S, 0, 2))), detail(seg(7.75, 8.3, 7.75, 8.3 + h)), detail(seg(16.25, 8.3, 16.25, 8.3 + h))]


def _hemisphere_filled():
    sil = U(P("M2.5 15.5A9.5 9.5 0 0 1 21.5 15.5Z"), P(ellipse(12, 15.5, 9.5, 3.5)))
    sil = U(sil, ST(path_to_d(sil), 2))
    return D(sil, ST("M2.5 15.5A9.5 3.5 0 0 1 21.5 15.5", 2))


@icon("hemisphere", CAT, "Hemisphere: half a sphere resting on its flat round base.",
      tags=["hemisphere", "half sphere", "dome", "solid", "geometry", "3d"], filled=_hemisphere_filled)
def _(S):
    return [line("M2.5 15.5A9.5 9.5 0 0 1 21.5 15.5A9.5 3.5 0 0 1 2.5 15.5"), *hidden(S, "M4.5 13.35A9.5 3.5 0 0 1 19.5 13.35", 4, 1.6)]


# ============================================================================ circles, polygons and constructions

def xd(d: str, m) -> str:
    """Transform a d-string by an affine matrix (a, b, c, d, e, f), keeping open paths open."""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.svgLib.path import parse_path
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def rot_m(deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return (c, s, -s, c, cx - c * cx + s * cy, cy - s * cx - c * cy)


def _arrow_arc(S, cx, cy, r, a0, a1, head=2.8):
    """Clockwise arc from a0 to a1 with an arrowhead at a1."""
    end = pt_on(cx, cy, r, a1)
    t = math.radians(a1)
    tx, ty = -math.sin(t), math.cos(t)  # clockwise tangent
    nx, ny = math.cos(t), math.sin(t)
    back = (end[0] - tx * head, end[1] - ty * head)
    return [line(arc(cx, cy, r, a0, a1)),
            line(poly([(back[0] + nx * head, back[1] + ny * head), end, (back[0] - nx * head, back[1] - ny * head)], r=S.r * 0.5))]


@icon("circle-circumference", CAT, "Circumference: a circle with a curved arrow running around its edge.",
      tags=["circumference", "perimeter", "circle", "distance around", "geometry", "math"])
def _(S):
    return [shell(circle(12, 12, 4.5)), *_arrow_arc(S, 12, 12, 8.75, 35, 312, 2.6)]


@icon("sector-of-circle", CAT, "Sector of a circle: a pie-slice region between two radii and their arc.",
      tags=["sector", "circle sector", "pie slice", "arc", "area", "geometry", "math"])
def _(S):
    a0, a1 = -90, -30
    wedge = f"M12 12L{fmt(pt_on(12, 12, 9, a0)[0])} {fmt(pt_on(12, 12, 9, a0)[1])}" + arc(12, 12, 9, a0, a1)[arc(12, 12, 9, a0, a1).index("A"):] + "Z"
    return [line(arc(12, 12, 9, a1, a0 + 360)), shell(wedge.replace("Z", "") + "Z" if False else wedge, stroke_miterlimit="2")]


@icon("inscribed-angle", CAT, "Inscribed angle: two chords meeting at a point on a circle, with the angle marked.",
      tags=["inscribed angle", "chord", "circle theorem", "angle", "geometry", "math"])
def _(S):
    p, a, b = pt_on(12, 12, 9, 100), pt_on(12, 12, 9, -150), pt_on(12, 12, 9, -30)
    ang_a = math.degrees(math.atan2(a[1] - p[1], a[0] - p[0]))
    ang_b = math.degrees(math.atan2(b[1] - p[1], b[0] - p[0]))
    wedge = f"M{fmt(p[0])} {fmt(p[1])}L{fmt(pt_on(*p, 6, ang_a)[0])} {fmt(pt_on(*p, 6, ang_a)[1])}" + \
        arc(*p, 6, ang_a, ang_b)[arc(*p, 6, ang_a, ang_b).index("A"):] + "Z"
    return [line(circle(12, 12, 9)), line(poly([a, p, b], r=S.r), stroke_miterlimit="2"), solid(wedge),
            mark(S, *a, 2.1), mark(S, *b, 2.1)]


@icon("heptagon", CAT, "Regular heptagon: a seven-sided polygon.",
      tags=["heptagon", "septagon", "seven sides", "polygon", "geometry", "shape"])
def _(S):
    return [shell(poly(regular(12, 12.6, 10, 7), closed=True, r=L(S, 0, 2)))]


@icon("decagon", CAT, "Regular decagon: a ten-sided polygon.",
      tags=["decagon", "ten sides", "polygon", "geometry", "shape"])
def _(S):
    return [shell(poly(regular(12, 12, 10, 10, -90), closed=True, r=L(S, 0, 2.5)))]


@icon("angle-bisector", CAT, "Angle bisector: a dashed ray splitting an angle into two equal marked parts.",
      tags=["angle bisector", "bisect", "angle", "construction", "geometry", "math"])
def _(S):
    v = (3, 19.5)
    parts = [line(poly([pt_on(*v, 18, -60), v, (21, 19.5)], r=S.r * 0.5)),
             line(arc(*v, 7, -60, -38)), line(arc(*v, 7, -22, 0))]
    parts += dashes(pt_on(*v, 10, -30), pt_on(*v, 18.5, -30), 3, 2)
    return parts


@icon("perpendicular-bisector", CAT, "Perpendicular bisector: a dashed line crossing a segment at its midpoint at a right angle.",
      tags=["perpendicular bisector", "midpoint", "bisect", "construction", "geometry", "math"])
def _(S):
    return [line(seg(4, 13, 20, 13)), mark(S, 4, 13, 1.9), mark(S, 20, 13, 1.9),
            line(poly([(12, 8.5), (16.5, 8.5), (16.5, 13)], r=S.r * 0.5)),
            line(seg(12, 2.5, 12, 4.5)), line(seg(12, 6.5, 12, 13)), line(seg(12, 15.5, 12, 17.5)), line(seg(12, 19.5, 12, 21.5))]


_LEAF = "M12 3C17.5 6.5 18.5 14.5 12 21C5.5 14.5 6.5 6.5 12 3Z"


@icon("line-of-symmetry", CAT, "Line of symmetry: a leaf split into mirror halves by a dashed line.",
      tags=["symmetry", "line of symmetry", "mirror line", "reflection", "axis", "geometry"])
def _(S):
    return [shell(_LEAF), *[Part("detail", p.d) for p in dashes((12, 1), (12, 23), 6, 2)]]


@icon("rotational-symmetry", CAT, "Rotational symmetry: a three-bladed pinwheel with a curved arrow around it.",
      tags=["rotational symmetry", "rotation", "turn", "pinwheel", "symmetry", "geometry"])
def _(S):
    blade = ("M12 13C10.2 10.4 10.4 6.9 13.9 4.8C16.6 7.6 15.6 11.4 12 13Z" if S.name == "line" else
             "M12 13C10.4 10.4 10.6 7.4 13.2 5.2C14 4.6 14.5 4.7 15 5.4C16.4 8 15.4 11.5 12 13Z")
    parts = [solid(xd(blade, rot_m(a, 12, 13))) for a in (0, 120, 240)]
    return parts + _arrow_arc(S, 12, 13, 10, 215, 325, 2.6)


def _honeycomb(x0=3.0, y0=3.0, x1=21.0, y1=21.0, r=4.1):
    """Edges of a pointy-top hexagon tiling clipped to a square (list of segments)."""
    w = math.sqrt(3) * r
    edges = set()
    for row in range(-2, 8):
        for col in range(-2, 8):
            cx = 12 + (col - 2) * w + (w / 2 if row % 2 else 0)
            cy = 12 + (row - 2) * 1.5 * r
            vs = [pt_on(cx, cy, r, -90 + 60 * k) for k in range(6)]
            for k in range(6):
                a, b = vs[k], vs[(k + 1) % 6]
                key = tuple(sorted([(round(a[0], 2), round(a[1], 2)), (round(b[0], 2), round(b[1], 2))]))
                edges.add(key)
    out = []
    for a, b in edges:
        # Liang-Barsky clip
        dx, dy = b[0] - a[0], b[1] - a[1]
        t0, t1 = 0.0, 1.0
        ok = True
        for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
            if abs(p) < 1e-9:
                if q < 0:
                    ok = False
            else:
                t = q / p
                if p < 0:
                    t0 = max(t0, t)
                else:
                    t1 = min(t1, t)
        if ok and t1 - t0 > 0.12:
            pa = (a[0] + dx * t0, a[1] + dy * t0)
            pb = (a[0] + dx * t1, a[1] + dy * t1)
            on_edge = (abs(pa[0] - pb[0]) < 1e-6 and pa[0] in (x0, x1)) or (abs(pa[1] - pb[1]) < 1e-6 and pa[1] in (y0, y1))
            if not on_edge:
                out.append((pa, pb))
    return out


@icon("tessellation-pattern", CAT, "Tessellation: hexagon tiles fitting together with no gaps inside a square.",
      tags=["tessellation", "tiling", "honeycomb", "pattern", "hexagons", "geometry"])
def _(S):
    return [shell(rect(3, 3, 18, 18, L(S, 0, 2.5)))] + [detail(seg(*a, *b)) for a, b in _honeycomb(3, 3, 21, 21, 5.4)]


def _wave_pts(phase, amp=6.5, x0=2.5, x1=21.5, n=40):
    return [(x0 + (x1 - x0) * i / n, 12 - amp * math.sin(2 * math.pi * i / n + phase)) for i in range(n + 1)]


@icon("sine-cosine-waves", CAT, "Sine and cosine: a solid sine wave and a dashed cosine wave shifted by a quarter period.",
      tags=["sine", "cosine", "wave", "trigonometry", "phase shift", "oscillation", "math"])
def _(S):
    sine = smooth(_wave_pts(0)[::4])
    cos = _wave_pts(math.pi / 2, n=200)
    parts = [line(sine)]
    for f in (0.0, 0.24, 0.35, 0.46, 0.75, 0.86, 0.97):
        i = int(f * 200)
        a, b = cos[i], cos[min(i + 6, 200)]
        if S.name == "line":
            parts.append(line(seg(*a, *b)))
        else:
            m = cos[min(i + 3, 200)]
            parts.append(dot(*m, 1.15))
    return parts
