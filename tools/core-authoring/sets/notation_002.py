"""TypeIcon Core: notation (batch notation_002).

Graph curves, arithmetic layouts, number systems, punctuation, typographic signs, diacritics, phonetic letters
and typeface specimens. Letters and marks are open strokes (line parts): Line and Rounded differ by caps, joins
and fillets, Filled makes the strokes heavier. Closed figures use shells.
"""
from __future__ import annotations

import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt

CAT = "notation"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def mark(S, x, y, r=1.75):
    """Dot: square in Line, round in Rounded; knocked out of a Filled shell."""
    if S.name == "line":
        s = r * 1.77
        return Part("dot", rect(x - s / 2, y - s / 2, s, s))
    return dot(x, y, r)


def axes(S, x=3.5, y=20.5, top=3, right=21):
    return line(poly([(x, top), (x, y), (right, y)], r=S.r))


def head(S, tip, deg, size=2.75):
    """Open arrowhead (chevron) with its tip at `tip`, pointing along `deg` (0 = right, 90 = down)."""
    a = math.radians(deg)
    pts = []
    for s in (-1, 1):
        b = a + math.pi + s * math.radians(42)
        pts.append((tip[0] + size * math.cos(b), tip[1] + size * math.sin(b)))
    return line(poly([pts[0], tip, pts[1]], r=S.r * 0.5))


def trim(p, q, r0, r1=0.0):
    """Shorten segment p->q by r0 at p and r1 at q."""
    d = math.dist(p, q)
    ux, uy = (q[0] - p[0]) / d, (q[1] - p[1]) / d
    return (p[0] + ux * r0, p[1] + uy * r0, q[0] - ux * r1, q[1] - uy * r1)


def dashed(p0, p1, n, dash=2.0):
    (x0, y0), (x1, y1) = p0, p1
    length = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / length, (y1 - y0) / length
    gap = (length - n * dash) / (n - 1) if n > 1 else 0
    return [line(seg(x0 + ux * i * (dash + gap), y0 + uy * i * (dash + gap),
                     x0 + ux * (i * (dash + gap) + dash), y0 + uy * (i * (dash + gap) + dash))) for i in range(n)]


# ============================================================================ graph curves

@icon("sigmoid-curve", CAT, "An S-shaped logistic curve rising from a low flat part to a high flat part on axes.",
      tags=["sigmoid", "logistic", "s-curve", "activation function", "growth curve", "graph", "math"])
def _(S):
    return [axes(S), line("M6.5 18C13 18 11 6 19 6")]


@icon("exponential-curve", CAT, "A curve on axes that starts almost flat and climbs steeply to the upper right.",
      tags=["exponential", "growth", "curve", "graph", "exponent", "rapid increase", "math"])
def _(S):
    return [axes(S), line("M6.5 18C12 17.5 16.5 14 19 4.5")]


@icon("logarithmic-curve", CAT, "A curve on axes that rises steeply at first and then levels off to the right.",
      tags=["logarithm", "log curve", "diminishing returns", "graph", "saturation", "math"])
def _(S):
    return [axes(S), line("M7 18.5C7.5 9 11.5 6 20 5.5")]


@icon("step-function", CAT, "A staircase of flat steps on axes with a closed dot at the start of each step.",
      tags=["step function", "staircase", "piecewise", "floor function", "discrete", "graph", "math"])
def _(S):
    return [axes(S),
            line(seg(7, 17, 10.5, 17)), line(seg(11.5, 12, 15, 12)), line(seg(16, 7, 19.5, 7)),
            dot(7, 17, 1.75), dot(11.5, 12, 1.75), dot(16, 7, 1.75)]


@icon("asymptote", CAT, "A curve bending toward a vertical dashed line without ever touching it.",
      tags=["asymptote", "approaches", "limit", "infinity", "hyperbola", "graph", "calculus", "math"])
def _(S):
    return [axes(S), line("M7 16.5C12 15.5 15 11 15.5 4"), *dashed((19.5, 3), (19.5, 17.5), 3, 3)]


# ============================================================================ fields, planes and diagrams

def _arrow(S, cx, cy, deg, ln=4.5):
    a = math.radians(deg)
    tail = (cx - math.cos(a) * ln / 2, cy - math.sin(a) * ln / 2)
    tip = (cx + math.cos(a) * ln / 2, cy + math.sin(a) * ln / 2)
    return [line(seg(*tail, *tip)), head(S, tip, deg, 2.25)]


@icon("vector-field", CAT, "A ring of small arrows that swirl around a central point.",
      tags=["vector field", "flow", "swirl", "curl", "arrows", "calculus", "physics", "math"])
def _(S):
    parts = [dot(12, 12, 1.5)]
    cells = [((5, 5), 135 + 0), ((12, 5), 0), ((19, 5), 45), ((19, 12), 90), ((19, 19), 135),
             ((12, 19), 180), ((5, 19), 225), ((5, 12), 270)]
    for (cx, cy), d in cells:
        parts += _arrow(S, cx, cy, d, 4.5)
    return parts


@icon("complex-plane", CAT, "Crossed real and imaginary axes with an arrow from the origin to a plotted point.",
      tags=["complex plane", "argand diagram", "imaginary axis", "real axis", "complex number", "vector", "math"])
def _(S):
    return [line(seg(2.5, 15, 21.5, 15)), line(seg(8, 2.5, 8, 21.5)),
            line(seg(8, 15, 17, 6)), head(S, (18, 5), -45, 3.5)]


@icon("light-cone", CAT, "Two cones meeting tip to tip at a point, the future cone above and the past cone below.",
      tags=["light cone", "spacetime", "relativity", "minkowski", "causality", "physics", "cone"])
def _(S):
    return [shell(ellipse(12, 5, 7, 2.25)), shell(ellipse(12, 19, 7, 2.25)),
            line(seg(5.2, 6.2, 11.2, 11.2)), line(seg(18.8, 6.2, 12.8, 11.2)),
            line(seg(5.2, 17.8, 11.2, 12.8)), line(seg(18.8, 17.8, 12.8, 12.8)),
            dot(12, 12, 1.25)]


@icon("feynman-diagram", CAT, "Two lines meeting at a point joined by a wavy line to a second point where two lines leave.",
      tags=["feynman diagram", "particle physics", "photon", "vertex", "interaction", "quantum", "physics"])
def _(S):
    return [line(seg(2.5, 6.5, 7, 12)), line(seg(2.5, 17.5, 7, 12)),
            line("M7 12Q9.25 7 11.5 12T16 12"),
            line(seg(21.5, 6.5, 17, 12)), line(seg(21.5, 17.5, 17, 12)),
            dot(7, 12, 1.6), dot(16, 12, 1.6)]


# ============================================================================ arithmetic layouts

@icon("long-division", CAT, "The long division bracket with a quotient above the bar and digits beside and beneath it.",
      tags=["long division", "division", "divide", "dividend", "divisor", "quotient", "arithmetic", "math"])
def _(S):
    return [line("M10 9.5H21"), line("M10 9.5C7.5 13 7.5 18 10 21.5"),
            dot(4, 15.5, 1.6), dot(14, 15.5, 1.6), dot(18.5, 15.5, 1.6), dot(16, 4.5, 1.6)]


@icon("column-addition", CAT, "Two numbers stacked with a plus sign, a rule beneath them and the total below.",
      tags=["column addition", "add", "sum", "plus", "arithmetic", "vertical addition", "math", "total"])
def _(S):
    return [line(seg(11, 4.5, 21, 4.5)), line(seg(11, 9.5, 21, 9.5)),
            line(seg(3, 7.5, 7.5, 7.5)), line(seg(5.25, 5.25, 5.25, 9.75)),
            line(seg(3, 14.5, 21, 14.5)), line(seg(11, 19.5, 21, 19.5))]


@icon("factor-tree", CAT, "A number ring at the top branching into smaller numbers, ending in solid prime dots.",
      tags=["factor tree", "prime factors", "factorisation", "factorization", "branches", "primes", "arithmetic", "math"])
def _(S):
    a, b, c, d, e = (12, 5), (6, 13), (18, 13), (14.5, 20.5), (21, 20.5)
    return [line(circle(*a, 2.25)), dot(*b, 2), line(circle(*c, 2.25)), dot(*d, 1.6), dot(*e, 1.6),
            line(seg(*trim(a, b, 3.6, 3.2))), line(seg(*trim(a, c, 3.6, 3.6))),
            line(seg(*trim(c, d, 3.6, 2.7))), line(seg(*trim(c, e, 3.6, 2.7)))]


@icon("ten-frame", CAT, "A two by five frame of cells with counters filling the top row.",
      tags=["ten frame", "counters", "early maths", "counting", "number sense", "primary school", "math"])
def _(S):
    parts = [shell(rect(2, 6.5, 20, 11, L(S, 1, 2.5)))]
    for x in (6, 10, 14, 18):
        parts.append(detail(seg(x, 6.5, x, 17.5)))
    parts.append(detail(seg(2, 12, 22, 12)))
    for x in (4, 8, 12, 16):
        parts.append(dot(x, 9.25, 0.95))
    return parts


@icon("number-bond", CAT, "Three circles joined by lines, one whole at the top and two parts beneath it.",
      tags=["number bond", "part whole", "addition facts", "decompose", "primary school", "arithmetic", "math"])
def _(S):
    a, b, c = (12, 5.5), (5.5, 18), (18.5, 18)
    def node(p):
        return shell(rect(p[0] - 3, p[1] - 3, 6, 6, L(S, 0.75, 3)))
    return [node(a), node(b), node(c),
            line(seg(*trim(a, b, 4, 4))), line(seg(*trim(a, c, 4, 4)))]


def _pascal_filled():
    out = None
    for r in range(4):
        for k in range(r + 1):
            c = P(circle(12 + (k - r / 2) * 5.5, 5 + r * 5, 1.95))
            out = c if out is None else U(out, c)
    return out


@icon("pascals-triangle", CAT, "A triangle outline with dots along its edges and inside, in rows one, two, three and four wide.",
      tags=["pascal's triangle", "binomial", "combinatorics", "triangular numbers", "rows", "pattern", "math"],
      filled=lambda: _pascal_filled())
def _(S):
    parts = [shell(poly([(12, 5), (3.75, 20), (20.25, 20)], closed=True, r=S.r * 0.5))]
    for r in range(4):
        for k in range(r + 1):
            parts.append(mark(S, 12 + (k - r / 2) * 5.5, 5 + r * 5, 1.6))
    return parts


@icon("magic-square", CAT, "A three by three grid with dots on both diagonals, like the lines that share a total.",
      tags=["magic square", "grid", "puzzle", "sudoku", "number puzzle", "3x3", "math"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, L(S, 1, 3)))]
    for v in (9, 15):
        parts.append(detail(seg(v, 3, v, 21)))
        parts.append(detail(seg(3, v, 21, v)))
    for x, y in ((6, 6), (18, 6), (12, 12), (6, 18), (18, 18)):
        parts.append(dot(x, y, 1.1))
    return parts


@icon("truth-table", CAT, "A small grid with a header row and rows of true and false marks under three columns.",
      tags=["truth table", "boolean", "logic", "true false", "propositions", "discrete math", "table"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, L(S, 1, 3))), detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
             detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15))]
    for (x, y) in ((6, 12), (12, 12), (6, 18), (18, 18)):
        parts.append(mark(S, x, y, 1.2))
    for (x, y) in ((18, 12), (12, 18)):
        parts.append(Part("dot", rect(x - 1.25, y - 0.5, 2.5, 1)))
    return parts


@icon("roman-numerals", CAT, "The Roman numerals I, V and X drawn as plain capitals side by side.",
      tags=["roman numerals", "roman numbers", "i v x", "ancient numbers", "latin", "numeral system", "clock face"])
def _(S):
    return [line(seg(3.5, 5.5, 3.5, 18.5)),
            line(poly([(7.5, 5.5), (11.25, 18.5), (15, 5.5)], r=S.r * 0.5)),
            line(seg(18.5, 5.5, 22.5, 18.5)), line(seg(22.5, 5.5, 18.5, 18.5))]


@icon("mayan-numerals", CAT, "A Mayan number: two dots above two bars.",
      tags=["mayan numerals", "maya", "dots and bars", "ancient numbers", "base twenty", "number system", "twelve"])
def _(S):
    return [shell(rect(3.5, 10, 17, 4.5, L(S, 0.5, 2.25))), shell(rect(3.5, 16.5, 17, 4.5, L(S, 0.5, 2.25))),
            mark(S, 8.5, 5, 1.75), mark(S, 15.5, 5, 1.75)]


@icon("cuneiform-numerals", CAT, "Babylonian number wedges: three upright wedges over two more, like marks pressed in clay.",
      tags=["cuneiform", "babylonian numerals", "wedge", "clay tablet", "ancient numbers", "mesopotamia", "sumerian"])
def _(S):
    parts = []
    for cx, y0 in ((6, 3), (12, 3), (18, 3), (9, 13.5), (15, 13.5)):
        parts.append(solid(poly([(cx - 3, y0), (cx + 3, y0), (cx, y0 + 5.5)], closed=True)))
        parts.append(line(seg(cx, y0 + 4, cx, y0 + 8)))
    return parts


@icon("place-value-chart", CAT, "A three column chart with one counter in the first column, two in the second and three in the third.",
      tags=["place value", "hundreds tens ones", "counters", "columns", "primary school", "number sense", "math"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, L(S, 1, 3))), detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
             detail(seg(3, 8.5, 21, 8.5))]
    for x, n in ((6, 1), (12, 2), (18, 3)):
        for k in range(n):
            parts.append(mark(S, x, 18 - k * 3.2, 1.0))
    return parts


@icon("decimal-point", CAT, "The number 3.14 with its decimal point drawn as a large dot.",
      tags=["decimal point", "decimal", "3.14", "pi", "fraction", "number", "full stop", "period"])
def _(S):
    return [line("M2.5 6.5C3.3 5.4 4.5 5 5.5 5C7.2 5 8 6.2 8 7.5C8 9.2 6.5 10.2 5 10.2C6.7 10.2 8.2 11 8.2 13.2C8.2 15.3 6.8 16.5 5.2 16.5C4 16.5 3 16 2.5 15.2"),
            dot(11.5, 16, 1.75),
            line(seg(15, 5, 15, 16.5)), line(seg(13.5, 6.5, 15, 5)),
            line(poly([(21, 5), (17.5, 12.5), (22, 12.5)], r=S.r * 0.4)), line(seg(21, 5, 21, 16.5))]


@icon("ordinal-number", CAT, "The number 1 followed by a small raised st, the ordinal first.",
      tags=["ordinal", "1st", "first", "ranking", "position", "superscript", "number suffix"])
def _(S):
    return [line(seg(6, 9, 6, 20.5)), line(seg(6, 9, 3, 11.5)),
            line("M16 5.5C15.4 4.6 14.4 4.2 13.4 4.2C12.3 4.2 11.5 4.8 11.5 5.6C11.5 7.4 16 6.6 16 8.8C16 9.9 15 10.6 13.6 10.6C12.4 10.6 11.6 10.2 11 9.5"),
            line(seg(20, 3, 20, 10)), line(seg(18, 5.5, 22, 5.5))]


@icon("odd-and-even", CAT, "Counters in rings of two: an even row of two pairs above a row with one left over.",
      tags=["odd", "even", "parity", "pairs", "counters", "leftover", "primary school", "math"])
def _(S):
    def pair(cx, cy):
        return [shell(rect(cx - 4.6, cy - 3.6, 9.2, 7.2, L(S, 1.5, 3.6))), mark(S, cx - 1.9, cy, 1.3), mark(S, cx + 1.9, cy, 1.3)]
    return pair(6.6, 7) + pair(17.4, 7) + pair(6.6, 17) + [mark(S, 17.4, 17, 1.8)]


@icon("function-machine", CAT, "A box with an arrow going in on the left, an arrow coming out on the right and an f on the box.",
      tags=["function machine", "input output", "function", "f of x", "mapping", "algebra", "math"])
def _(S):
    return [shell(rect(7.5, 4.5, 9, 15, L(S, 1, 2.5))),
            line(seg(2, 12, 5.5, 12)), head(S, (6, 12), 0, 2.25),
            line(seg(18, 12, 22, 12)), head(S, (22, 12), 0, 2.25),
            detail("M9.5 12C10.5 8.8 11.5 8.8 12 12C12.5 15.2 13.5 15.2 14.5 12")]


@icon("turing-machine", CAT, "A strip of tape cells with a read and write head pointing down at one cell.",
      tags=["turing machine", "tape", "head", "computation", "automaton", "computer science", "cells"])
def _(S):
    parts = [shell(rect(2, 15.5, 20, 5, L(S, 1, 2.5)))]
    for x in (7, 12, 17):
        parts.append(detail(seg(x, 15.5, x, 20.5)))
    parts.append(shell(poly([(8.5, 3.5), (15.5, 3.5), (15.5, 8.5), (12, 12), (8.5, 8.5)], closed=True, r=S.r * 0.6)))
    return parts


@icon("probability-scale", CAT, "A line scale from 0 to 1 with an arrow pointing down at the halfway mark.",
      tags=["probability scale", "likelihood", "chance", "zero to one", "half", "number line", "statistics"])
def _(S):
    return [line(seg(3, 18, 21, 18)), line(seg(3, 15, 3, 21)), line(seg(21, 15, 21, 21)),
            line(seg(12, 3.5, 12, 14.5)), head(S, (12, 15), 90, 3.2),
            line(ellipse(3.6, 8.5, 1.4, 2.2)), line(seg(20.5, 6, 20.5, 11))]


@icon("reuleaux-triangle", CAT, "A rounded triangle of constant width, made of three circular arcs.",
      tags=["reuleaux triangle", "constant width", "curved triangle", "guitar pick", "geometry", "shape", "arc triangle"])
def _(S):
    R = 10.0
    s = R * math.sqrt(3)
    cy = 13.0
    V = [pt_on(12, cy, R, a) for a in (-90, 30, 150)]
    delta = L(S, 0.0, 2.6 / s)
    f = lambda q: f"{fmt(q[0])} {fmt(q[1])}"
    segs = []
    for i in range(3):
        c = V[(i + 2) % 3]
        a0 = math.atan2(V[i][1] - c[1], V[i][0] - c[0])
        p0 = (c[0] + s * math.cos(a0 + delta), c[1] + s * math.sin(a0 + delta))
        p1 = (c[0] + s * math.cos(a0 + math.pi / 3 - delta), c[1] + s * math.sin(a0 + math.pi / 3 - delta))
        segs.append((p0, p1))
    d = f"M{f(segs[0][0])}"
    for i in range(3):
        d += f"A{fmt(s)} {fmt(s)} 0 0 1 {f(segs[i][1])}"
        nxt = segs[(i + 1) % 3][0]
        d += f"Q{f(V[(i + 1) % 3])} {f(nxt)}" if delta else f"L{f(nxt)}"
    return [shell(d + "Z")]


# ============================================================================ punctuation

def _bang(S, x, top=4, end=14.5, dot_y=19.5):
    return [line(seg(x, top, x, end)), mark(S, x, dot_y, 1.75)]


def _qmark(S, x, flip=False):
    """Question mark centred on x (8 wide); flip turns it upside down about y = 12."""
    hook = (f"M{fmt(x - 4)} 8.5C{fmt(x - 4)} 5.8 {fmt(x - 2.2)} 4 {fmt(x)} 4C{fmt(x + 2.2)} 4 {fmt(x + 4)} 5.6 {fmt(x + 4)} 7.8"
            f"C{fmt(x + 4)} 11 {fmt(x)} 11.5 {fmt(x)} 14.5")
    if not flip:
        return [line(hook), mark(S, x, 19.5, 1.75)]
    hook = (f"M{fmt(x + 4)} 15.5C{fmt(x + 4)} 18.2 {fmt(x + 2.2)} 20 {fmt(x)} 20C{fmt(x - 2.2)} 20 {fmt(x - 4)} 18.4 {fmt(x - 4)} 16.2"
            f"C{fmt(x - 4)} 13 {fmt(x)} 12.5 {fmt(x)} 9.5")
    return [line(hook), mark(S, x, 4.5, 1.75)]


@icon("interrobang", CAT, "An exclamation mark and a question mark overlaid: a hooked top over one straight stem and a shared dot.",
      tags=["interrobang", "question exclamation", "surprise", "disbelief", "punctuation", "?!", "incredulity"])
def _(S):
    return [line("M7.5 8.5C7.5 5.8 9.3 4 12 4C14.7 4 16.5 5.6 16.5 7.8C16.5 10.4 15 11.3 12 11.8"),
            line(seg(12, 4, 12, 14.5)), mark(S, 12, 19.5, 1.75)]


@icon("inverted-question-mark", CAT, "An upside-down question mark with its dot on top, as opening punctuation in Spanish.",
      tags=["inverted question mark", "spanish", "upside down", "question", "punctuation", "opening question", "spanish punctuation"])
def _(S):
    return _qmark(S, 12, flip=True)


@icon("inverted-exclamation-mark", CAT, "An upside-down exclamation mark with a dot on top and a bar below, as opening punctuation in Spanish.",
      tags=["inverted exclamation mark", "spanish", "upside down", "exclamation", "punctuation", "opening exclamation", "spanish punctuation"])
def _(S):
    return [mark(S, 12, 4.5, 1.75), line(seg(12, 9.5, 12, 20))]


@icon("double-exclamation-mark", CAT, "Two exclamation marks side by side, each a bar above a dot.",
      tags=["double exclamation", "two exclamation marks", "!!", "emphasis", "shout", "punctuation", "excited"])
def _(S):
    return _bang(S, 7) + _bang(S, 17)


@icon("exclamation-question-mark", CAT, "An exclamation mark followed by a question mark.",
      tags=["exclamation question", "!?", "surprise", "confusion", "punctuation", "what", "shock"])
def _(S):
    return _bang(S, 6) + _qmark(S, 15.5)


@icon("semicolon", CAT, "A semicolon: a round dot above a comma with a short curved tail.",
      tags=["semicolon", "punctuation", "clause", "pause", "grammar", "writing", ";"])
def _(S):
    return [mark(S, 12.5, 7.5, 2), mark(S, 12.5, 15.5, 2), line("M12.5 16C12.5 19 11.5 20.5 9.5 21.5")]


@icon("colon-punctuation", CAT, "A colon: two round dots stacked vertically.",
      tags=["colon", "punctuation", "list", "ratio", "grammar", "writing", ":"],
      filled=lambda: U(P(circle(12, 7, 2.75)), P(circle(12, 17, 2.75))))
def _(S):
    return [mark(S, 12, 7, 2.25), mark(S, 12, 17, 2.25)]


@icon("comma-punctuation", CAT, "A single large comma: a round dot with a curved tail sweeping down and left.",
      tags=["comma", "punctuation", "pause", "separator", "grammar", "writing", ","])
def _(S):
    return [mark(S, 13, 10.5, 2.75), line("M13.5 12C13.5 16 12 18.5 8.5 20.5")]


@icon("guillemets", CAT, "Double angle quotation marks, a pair of chevrons pointing left beside a pair pointing right.",
      tags=["guillemets", "angle quotes", "french quotes", "chevron quotes", "quotation marks", "punctuation", "double angle"])
def _(S):
    r = S.r * 0.5
    return [
        line(poly([(6, 6.5), (2.5, 12), (6, 17.5)], r=r)), line(poly([(10, 6.5), (6.5, 12), (10, 17.5)], r=r)),
        line(poly([(14, 6.5), (17.5, 12), (14, 17.5)], r=r)), line(poly([(18, 6.5), (21.5, 12), (18, 17.5)], r=r))]


@icon("lenticular-brackets", CAT, "Two thick curved brackets facing each other, like a pair of crescents.",
      tags=["lenticular brackets", "black lenticular", "cjk brackets", "title brackets", "asian punctuation", "crescent brackets", "quote"])
def _(S):
    left = "M8.5 4C3.5 7 3.5 17 8.5 20Z"
    right = "M15.5 4C20.5 7 20.5 17 15.5 20Z"
    return [shell(left), shell(right)]


@icon("dagger", CAT, "A dagger mark: a long vertical stroke with one short crossbar near the top.",
      tags=["dagger", "obelus", "footnote", "obelisk", "cross", "reference mark", "died"])
def _(S):
    return [line(seg(12, 3, 12, 21)), line(seg(7, 8, 17, 8))]


@icon("double-dagger", CAT, "Double dagger mark: a vertical stroke with two short crossbars, one near the top and one near the bottom.",
      tags=["double dagger", "diesis", "footnote", "reference mark", "third footnote", "obelisk", "double obelisk"])
def _(S):
    return [line(seg(12, 3, 12, 21)), line(seg(7, 8, 17, 8)), line(seg(7, 15.5, 17, 15.5))]


def _asterisk(cx, cy, r=3.3):
    return [line(seg(*pt_on(cx, cy, r, a), *pt_on(cx, cy, r, a + 180))) for a in (90, 30, 150)]


@icon("asterism-mark", CAT, "Asterism: three small asterisks arranged in a triangle, two below and one above.",
      tags=["asterism", "section break", "three asterisks", "scene break", "typography", "fleuron", "divider"],
      filled=lambda: _asterism_filled())
def _(S):
    return _asterisk(12, 6.5) + _asterisk(6, 17) + _asterisk(18, 17)


def _asterism_filled():
    out = None
    for cx, cy in ((12, 6.5), (6, 17), (18, 17)):
        for a in (90, 30, 150):
            r = ST(seg(*pt_on(cx, cy, 3.3, a), *pt_on(cx, cy, 3.3, a + 180)), 2.25, "butt", "miter")
            out = r if out is None else U(out, r)
    return out


@icon("hedera", CAT, "Hedera ivy leaf dingbat: a heart-shaped leaf with a curling stem.",
      tags=["hedera", "ivy leaf", "fleuron", "floral heart", "dingbat", "ornament", "typography"])
def _(S):
    tip = L(S, "L", "L")
    leaf = "M21.5 12C17.5 7 14 3.5 10.5 5.5C8.2 7 8.6 10.5 11.5 12C8.6 13.5 8.2 17 10.5 18.5C14 20.5 17.5 17 21.5 12Z"
    stem = "M11.5 12H7.5C5 12 3.2 10.4 3.2 8.4C3.2 6.8 4.5 6 5.6 6.6"
    return [shell(leaf), detail(stem)]


@icon("numero-sign", CAT, "Numero sign: a capital N followed by a small raised o with a bar under it.",
      tags=["numero", "number sign", "no.", "numero symbol", "abbreviation", "cyrillic", "ordinal indicator"])
def _(S):
    return [line(poly([(3.5, 19), (3.5, 6), (11.5, 19), (11.5, 6)], r=S.r * 0.6)),
            line(circle(17.75, 8.5, 2.75)), line(seg(14.5, 16, 21, 16))]


@icon("care-of-sign", CAT, "Care of sign: a small c above a diagonal slash above a small o.",
      tags=["care of", "c/o", "address", "mail", "abbreviation", "letter", "postal"])
def _(S):
    return [line(arc(5.5, 14.5, 3.5, 40, 320)), line(seg(13.5, 4, 10.5, 21)), line(circle(18.5, 14.5, 2.75))]


@icon("sound-recording-copyright", CAT, "Sound recording copyright symbol: a capital P inside a circle.",
      tags=["phonogram", "sound recording copyright", "p in circle", "record rights", "music licence", "audio copyright", "legal"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(seg(10, 7.5, 10, 17)),
            detail(poly([(10, 7.5), (13.8, 7.5), (15.5, 9), (15.5, 11.4), (13.8, 13), (10, 13)], r=S.r))]


@icon("service-mark", CAT, "Service mark: a small raised SM in superscript beside a short line of text.",
      tags=["service mark", "sm", "trademark", "superscript", "brand service", "legal", "unregistered"])
def _(S):
    return [line("M15.5 5C14.9 4.2 14 3.8 13 3.8C11.8 3.8 11 4.4 11 5.3C11 7 15.5 6.3 15.5 8.4C15.5 9.5 14.6 10.2 13.2 10.2C12 10.2 11.2 9.8 10.6 9"),
            line(poly([(18, 10.2), (18, 3.8), (20.25, 7), (22.5, 3.8), (22.5, 10.2)], r=S.r * 0.4)),
            line(seg(2.5, 14.5, 14, 14.5)), line(seg(2.5, 20, 9.5, 20))]


@icon("copyleft", CAT, "Copyleft symbol: a reversed capital C inside a circle, opening to the left.",
      tags=["copyleft", "reversed c", "free software", "open license", "share alike", "gpl", "open source"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(arc(12, 12, 4.25, -135, 135))]


@icon("ditto-mark", CAT, "Ditto mark: two short slanted strokes placed under a word in a list.",
      tags=["ditto", "same as above", "repeat", "quotation mark", "list", "duplicate"])
def _(S):
    return [line(seg(4, 5, 20, 5)), line(seg(10, 11.5, 8, 20)), line(seg(16, 11.5, 14, 20))]


@icon("tilde", CAT, "A single large tilde: a smooth horizontal wave with one rise and one dip.",
      tags=["tilde", "squiggle", "approximately", "home directory", "swung dash", "wave", "punctuation"])
def _(S):
    return [line("M2.8 14.5C4.5 8 8.5 7.2 12 12C15.5 16.8 19.5 16 21.2 9.5")]


@icon("backslash", CAT, "A backslash: a single stroke leaning from top left to bottom right.",
      tags=["backslash", "reverse slash", "escape character", "windows path", "directory separator", "slash", "code"])
def _(S):
    return [line(seg(6, 3.5, 18, 20.5))]


@icon("vertical-bar", CAT, "A vertical bar, also called a pipe: two tall strokes with a small gap between them.",
      tags=["vertical bar", "pipe", "broken bar", "separator", "or operator", "divider", "shell pipe"])
def _(S):
    return [line(seg(12, 3, 12, 10)), line(seg(12, 14, 12, 21))]


@icon("tironian-et", CAT, "Tironian et: a shape like a 7 with a short foot, the old Latin sign for and.",
      tags=["tironian et", "ampersand", "and sign", "old irish", "medieval shorthand", "seven shape", "gaelic typography"])
def _(S):
    return [line(poly([(5.5, 5), (18.5, 5), (11, 20)], r=S.r * 0.6)), line(seg(6.5, 20, 13.5, 20))]


@icon("prime-marks", CAT, "A number 1 with a single tick and another 1 with a double tick, for feet and inches.",
      tags=["prime", "double prime", "feet and inches", "minutes seconds", "tick marks", "measurement", "arcminute"])
def _(S):
    return [line(seg(5, 7, 5, 19)), line(seg(5, 7, 2.5, 9.2)), line(seg(9.5, 4.5, 8, 9.5)),
            line(seg(14.5, 7, 14.5, 19)), line(seg(14.5, 7, 12, 9.2)), line(seg(18.5, 4.5, 17, 9.5)), line(seg(22, 4.5, 20.5, 9.5))]


@icon("estimated-sign", CAT, "Estimated sign: a wide lowercase e with a flat crossbar, used on packaging to mark average contents.",
      tags=["estimated sign", "e mark", "average quantity", "packaging", "eu label", "weight marking", "lowercase e"])
def _(S):
    return [line("M3.5 12H20.5C20.5 7.8 16.8 5 12 5C7.2 5 3.5 7.8 3.5 12C3.5 16.2 7.2 19 12 19C15 19 17.6 17.8 19.2 16")]


# ============================================================================ letters with marks

def _e(cx, cy, r=5.0):
    """Lowercase e: a crossbar and an open bowl."""
    p = pt_on(cx, cy, r, 40)
    return line(f"M{fmt(cx - r)} {fmt(cy)}H{fmt(cx + r)}A{fmt(r)} {fmt(r)} 0 1 0 {fmt(p[0])} {fmt(p[1])}")


def _a(cx, cy):
    """Single-storey a: a round bowl with a right-hand stem."""
    return [line(circle(cx - 0.75, cy, 4.25)), line(seg(cx + 3.5, cy - 4.75, cx + 3.5, cy + 4.75))]


def _n(x0, top=10.5, bot=20.5):
    return [line(seg(x0, top, x0, bot)),
            line(f"M{fmt(x0)} {fmt(top + 5)}C{fmt(x0)} {fmt(top + 1.5)} {fmt(x0 + 2)} {fmt(top)} {fmt(x0 + 5)} {fmt(top)}"
                 f"C{fmt(x0 + 8)} {fmt(top)} {fmt(x0 + 10)} {fmt(top + 1.5)} {fmt(x0 + 10)} {fmt(top + 4.5)}V{fmt(bot)}")]


@icon("acute-accent", CAT, "The letter e with a short slanted acute accent stroke above it.",
      tags=["acute accent", "e acute", "accented letter", "diacritic", "french", "spanish"])
def _(S):
    return [_e(12, 15.5), line(seg(10.5, 7.5, 14.5, 3.5))]


@icon("circumflex-accent", CAT, "The letter e with a small caret-shaped circumflex above it.",
      tags=["circumflex", "e circumflex", "hat accent", "diacritic", "french", "accented letter"])
def _(S):
    return [_e(12, 15.5), line(poly([(8.5, 7.5), (12, 3.5), (15.5, 7.5)], r=S.r * 0.7))]


@icon("diaeresis", CAT, "The letter e with two dots side by side above it.",
      tags=["diaeresis", "umlaut", "e diaeresis", "two dots", "diacritic", "accented letter"])
def _(S):
    return [_e(12, 15.5), mark(S, 8.5, 5.5, 1.6), mark(S, 15.5, 5.5, 1.6)]


@icon("cedilla", CAT, "The letter c with a small hooked cedilla tail below it.",
      tags=["cedilla", "c cedilla", "french", "portuguese", "turkish", "diacritic"])
def _(S):
    return [line(arc(12, 10, 5.25, 40, 320)),
            line("M12 15.8C12 17.5 14 17.6 14 19.4C14 20.8 12.6 21.5 10.8 21.2")]


@icon("macron", CAT, "The letter a with a short flat bar above it.",
      tags=["macron", "long vowel", "a macron", "diacritic", "bar accent", "latin"])
def _(S):
    return [*_a(12, 16), line(seg(8.5, 5.5, 15.5, 5.5))]


@icon("breve", CAT, "The letter a with a small cup-shaped breve above it.",
      tags=["breve", "short vowel", "a breve", "diacritic", "cup accent", "romanian"])
def _(S):
    return [*_a(12, 16), line("M8 3.5C8 6.3 9.8 7.5 12 7.5C14.2 7.5 16 6.3 16 3.5")]


@icon("ring-above", CAT, "The letter a with a small circle sitting above it.",
      tags=["ring above", "a ring", "swedish", "norwegian", "danish", "diacritic"])
def _(S):
    return [*_a(12, 16.25), line(circle(12, 5, 2.25))]


@icon("tilde-accent", CAT, "The letter n with a small wavy tilde above it.",
      tags=["tilde accent", "n tilde", "spanish", "portuguese", "diacritic", "squiggle accent"])
def _(S):
    return [*_n(7), line("M7 7C8.3 3.5 10 3.5 12 5C14 6.5 15.7 6.5 17 3")]


@icon("ogonek", CAT, "The letter e with a small hooked tail curling to the right at its base.",
      tags=["ogonek", "nasal hook", "polish", "lithuanian", "diacritic", "little tail"])
def _(S):
    return [_e(11, 10.5, 5), line("M12.8 15.8C11.6 17.8 12.2 20 14.3 20.6C15.6 21 16.8 20.6 17.6 19.8")]


@icon("double-acute-accent", CAT, "The letter o with two short slanted strokes above it.",
      tags=["double acute", "o double acute", "hungarian", "diacritic", "two accents", "long umlaut"])
def _(S):
    return [line(circle(12, 15.5, 4.5)), line(seg(8, 7.5, 10.5, 3.5)), line(seg(13, 7.5, 15.5, 3.5))]


@icon("schwa", CAT, "Schwa: an upside-down lowercase e, the neutral vowel of phonetics.",
      tags=["schwa", "neutral vowel", "upside down e", "phonetics", "ipa", "linguistics"])
def _(S):
    return [_schwa()]


def _schwa():
    r, cx, cy = 6, 12, 12
    # e turned half a revolution about its centre
    p = pt_on(cx, cy, r, 40 + 180)
    return line(f"M{fmt(cx + r)} {fmt(cy)}H{fmt(cx - r)}A{fmt(r)} {fmt(r)} 0 1 0 {fmt(p[0])} {fmt(p[1])}")


@icon("eszett", CAT, "Eszett sharp s: a tall German letter like a B with an open lower bowl and a long left stem.",
      tags=["eszett", "sharp s", "german", "scharfes s", "ss letter", "beta shape"])
def _(S):
    return [line("M7 21V8C7 5.2 8.8 3.5 11.5 3.5C14 3.5 15.7 4.8 15.7 7C15.7 9.2 14 10.7 11.5 11"
                 "C14.6 11.3 17 12.8 17 15.7C17 18.8 14.7 20.5 11.5 20.5C10.1 20.5 8.9 20.2 8 19.6")]


@icon("thorn-letter", CAT, "Thorn letter: a tall vertical stem with a small bowl attached midway on the right.",
      tags=["thorn", "old english", "icelandic", "runic", "th letter", "alphabet"])
def _(S):
    return [line(seg(7, 3, 7, 21)),
            line("M7 8.5H11.5C14.8 8.5 17 10.3 17 13C17 15.7 14.8 17.5 11.5 17.5H7")]


@icon("eth-letter", CAT, "Eth letter: a round bowl with a curved ascender crossed by a short bar.",
      tags=["eth", "edh", "icelandic", "old english", "voiced th", "alphabet"])
def _(S):
    return [line(circle(10.5, 15.5, 4.75)),
            line("M15.25 15.5V6.5C15.25 4.7 16.3 3.5 18.5 3.5"), line(seg(10, 7.5, 18, 7.5))]


@icon("ae-ligature", CAT, "Ae ligature: a lowercase a and e joined into one glyph sharing a stroke.",
      tags=["ae ligature", "ash", "latin letter", "danish", "norwegian", "joined letters"])
def _(S):
    return [line("M3.5 12.6C4.6 11.5 6 11 7.6 11C10.2 11 12 12.4 12 15V20.5"),
            line("M12 15.5C9 15.3 3.5 15.4 3.5 18.1C3.5 19.8 5 20.4 7 20.4C9.2 20.4 11.3 19.3 12 17.3"),
            line("M12 15.5H21C21 12.8 19 11 16.5 11C14 11 12 12.8 12 15.5C12 18.2 14 20 16.5 20C18 20 19.5 19.4 20.5 18.2")]


@icon("oe-ligature", CAT, "Oe ligature: a lowercase o and e joined into one glyph sharing a stroke.",
      tags=["oe ligature", "french", "latin letter", "joined letters", "ethel", "typography"])
def _(S):
    return [line(circle(7.75, 15.5, 4.5)),
            line("M12.25 15.5H21.25C21.25 12.8 19.25 11 16.75 11C14.25 11 12.25 12.8 12.25 15.5C12.25 18.2 14.25 20 16.75 20C18.25 20 19.75 19.4 20.75 18.2")]


@icon("fi-ligature", CAT, "Fi ligature: an f whose hooked top joins the dot of the i in one connected glyph.",
      tags=["fi ligature", "f i", "typography", "joined letters", "opentype", "ligature"])
def _(S):
    return [line("M8 21V8.5C8 5.4 9.8 3.8 12.6 3.8C14.4 3.8 15.9 4.2 17 4.8"), line(seg(4.5, 11, 12, 11)),
            line(seg(17, 10.5, 17, 21)), dot(17, 4.8, 1.5)]


@icon("ipa-glottal-stop", CAT, "Glottal stop symbol: a question mark shape without the dot, sitting on the baseline.",
      tags=["glottal stop", "ipa", "phonetics", "linguistics", "stop consonant", "question mark without dot"])
def _(S):
    return [line("M7.5 7C8.3 5 10 3.8 12 3.8C14.6 3.8 16.5 5.4 16.5 8C16.5 12 12 12.5 12 16.5V21")]


@icon("ipa-eng", CAT, "Eng letter: a lowercase n whose right leg continues down below the baseline into a hook.",
      tags=["eng", "ng sound", "ipa", "velar nasal", "phonetics", "linguistics"])
def _(S):
    return [line(seg(6.5, 7.5, 6.5, 17.5)),
            line("M6.5 12.5C6.5 9 8.5 7.5 11.5 7.5C14.5 7.5 16.5 9 16.5 12V17.5C16.5 19.8 15.6 21 13.6 21")]


# ============================================================================ typefaces

@icon("serif-font", CAT, "A capital A in a serif typeface with clear serifs at its feet and apex.",
      tags=["serif", "serif font", "typeface", "classic book type", "roman type", "typography", "letter a"])
def _(S):
    return [line(poly([(6.5, 20), (12, 4.5), (17.5, 20)], r=S.r * 0.5)), line(seg(8.5, 14, 15.5, 14)),
            line(seg(3.5, 20, 9, 20)), line(seg(15, 20, 20.5, 20))]


@icon("sans-serif-font", CAT, "A capital A in a plain sans serif typeface with flat stroke ends.",
      tags=["sans serif", "sans-serif font", "typeface", "plain type", "modern type", "typography", "letter a"])
def _(S):
    return [line(poly([(5, 20.5), (12, 3.5), (19, 20.5)], r=S.r * 0.5)), line(seg(8, 14.5, 16, 14.5))]


@icon("monospace-font", CAT, "Three letters in a fixed-width typeface, each sitting in its own equal-width cell.",
      tags=["monospace", "fixed width", "typewriter", "code font", "typewriter style", "typography", "terminal"])
def _(S):
    return [line(seg(2.5, 21, 7.5, 21)), line(seg(9.5, 21, 14.5, 21)), line(seg(16.5, 21, 21.5, 21)),
            line(seg(5, 10, 5, 17)), mark(S, 5, 5.5, 1.5), line(seg(3.5, 17, 6.5, 17)),
            shell(circle(12, 14.5, 2.5)),
            line(seg(19, 4.5, 19, 17)), line(seg(17.5, 4.5, 19, 4.5))]


@icon("script-font", CAT, "A flowing handwritten capital letter with a looped swash tail.",
      tags=["script", "script font", "cursive", "calligraphy", "handwriting", "swash", "typography"])
def _(S):
    return [line("M15 4C11 4 8.5 6.5 10 10C11.5 13.5 14.5 15.5 12.5 18.5C11 20.8 7.5 20.5 6 18.6C4.8 17 6.2 15.4 8.4 16.3C12.5 17.9 17.5 19 21.5 17")]
