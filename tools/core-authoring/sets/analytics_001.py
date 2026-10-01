"""TypeIcon Core: analytics (batch 001).

Chart types, statistical plots and distribution curves. Bar-like charts follow `chart-bar`: 2 px bars in
Line/Rounded and 4 px solid bars in Filled. Plots that need axes use the shared corner axis of `charts.py`.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, LINE, P, ST, U, fmt, polar

CAT = "analytics"
AXES = [(3, 3), (3, 21), (21, 21)]


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def axes(S):
    return line(poly(AXES, r=S.r))


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def block(x, y, w, h, S, cap=1.0) -> Part:
    """Solid bar segment; square in Line, softened in Rounded."""
    return solid(rect(x, y, w, h, L(S, 0, min(cap, w / 2, h / 2))))


def mark(S, x, y, r=1.75) -> Part:
    """Data marker: a square in Line, a disc in Rounded."""
    if S.name == "line":
        a = r * 0.9
        return Part("dot", rect(x - a, y - a, 2 * a, 2 * a))
    return dot(x, y, r)


def vbars_filled(bars, w=4.0):
    """Filled design for vertical 2 px bars: (x, y0, y1) -> solid bars w px wide."""
    return lambda: U(*(P(rect(x - w / 2, min(y0, y1) - 1, w, abs(y1 - y0) + 2, 0.75)) for x, y0, y1 in bars))


def dash_pts(points, S, on=2.5, off=2.0):
    """Dashes along a polyline as separate segments. Rounded uses short dashes so round caps keep the gaps."""
    if S.name == "rounded":
        on, off = on - 2 + 0.5, off + 2 - 0.5
    out = []
    drawing, left = True, on
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        seg_len = math.hypot(x1 - x0, y1 - y0)
        t = 0.0
        while t < seg_len - 1e-6:
            step = min(left, seg_len - t)
            if drawing:
                a, b = t / seg_len, (t + step) / seg_len
                out.append(((x0 + (x1 - x0) * a, y0 + (y1 - y0) * a), (x0 + (x1 - x0) * b, y0 + (y1 - y0) * b)))
            t += step
            left -= step
            if left <= 1e-6:
                drawing = not drawing
                left = on if drawing else off
    # merge consecutive pieces of one dash that crossed a vertex
    merged = []
    for p, q in out:
        if merged and math.dist(merged[-1][-1], p) < 1e-6:
            merged[-1].append(q)
        else:
            merged.append([p, q])
    return [poly(m) for m in merged]


# ============================================================================ bar-like charts

_SB = [(6, 21, 13.5, 11), (12, 21, 8, 16), (18, 21, 11, 14)]  # x, base, top, split


@icon("chart-stacked-bar", CAT, "Stacked bar chart with each bar split into two segments.",
      tags=["stacked bar", "stacked column", "bar chart", "composition", "segments", "breakdown"],
      filled=lambda: D(U(*(P(rect(x - 2, top - 1, 4, base - top + 1, 0.75)) for x, base, top, sp in _SB)),
                       *(P(rect(x - 3, sp - 1, 6, 1.5)) for x, base, top, sp in _SB)))
def _(S):
    parts = []
    for x, base, top, sp in _SB:
        parts.append(block(x - 2, sp + 1, 4, base - sp - 1, S))
        parts.append(line(seg(x, sp - 1, x, top)))
    return parts


_GB = [(3.5, 21, 11), (6.75, 21, 6), (10, 21, 14), (14, 21, 9), (17.25, 21, 4.5), (20.5, 21, 12)]


@icon("chart-grouped-bar", CAT, "Grouped bar chart with two pairs of side by side bars.",
      tags=["grouped bar", "clustered column", "side by side bars", "bar chart", "comparison", "series"],
      filled=lambda: vbars_filled([(x, b - 1, t) for x, b, t in _GB], 2.75)())
def _(S):
    return [line(seg(x, b - 1, x, t)) for x, b, t in _GB]


_PB = [(4, 12), (9.33, 8), (14.67, 14), (20, 10)]


@icon("chart-percent-stacked-bar", CAT, "Percent stacked bar chart of equal height bars split at different points.",
      tags=["100 percent stacked", "percent stacked", "proportion", "share", "composition", "bar chart"],
      filled=lambda: D(U(*(P(rect(x - 1.75, 3, 3.5, 18, 0.75)) for x, sp in _PB)),
                       *(P(rect(x - 3, sp - 1, 6, 1.5)) for x, sp in _PB)))
def _(S):
    parts = []
    for x, sp in _PB:
        parts.append(block(x - 1.75, sp + 1, 3.5, 20 - sp, S))
        parts.append(line(seg(x, sp - 1, x, 3)))
    return parts


_DV = [(5, 12, 19.5), (9.67, 12, 6), (14.33, 12, 17), (19, 12, 4.5)]  # y, from, to


@icon("chart-diverging-bar", CAT, "Diverging bar chart with bars running left and right of a centre axis.",
      tags=["diverging bar", "butterfly chart", "tornado chart", "positive negative", "likert", "comparison"])
def _(S):
    return [line(seg(12, 2.5, 12, 21.5)), *[line(seg(a, y, b, y)) for y, a, b in _DV]]


_LP = [(4.5, 9), (9.5, 5), (14.5, 12), (19.5, 8)]


@icon("chart-lollipop", CAT, "Lollipop chart of thin stems topped with round markers.",
      tags=["lollipop chart", "dot stem", "ranking", "comparison", "bar alternative", "markers"])
def _(S):
    parts = [line(seg(2.5, 21, 21.5, 21))]
    for x, y in _LP:
        parts += [line(seg(x, 20, x, y)), dot(x, y, 2.25)]
    return parts


_DB = [(5.5, 7, 15), (12, 10.5, 19.5), (18.5, 7.5, 14)]  # y, x0, x1


@icon("chart-dumbbell", CAT, "Dumbbell chart of rows joining two markers each.",
      tags=["dumbbell chart", "dot plot", "range", "before and after", "gap", "comparison"])
def _(S):
    parts = [line(seg(2.5, 2.5, 2.5, 21.5))]
    for y, a, b in _DB:
        parts += [line(seg(a, y, b, y)), mark(S, a, y, 2.25), mark(S, b, y, 2.25)]
    return parts


@icon("chart-bullet", CAT, "Bullet chart: a measure bar and a target tick inside a range band.",
      tags=["bullet chart", "bullet graph", "target", "goal", "kpi", "progress against target"])
def _(S):
    return [shell(rect(2.5, 7.5, 19, 9, min(S.R, 2.5))),
            sq(4.5, 10.75, 10, 2.5, L(S, 0, 1)), line(seg(17, 5, 17, 19))]


@icon("chart-marimekko", CAT, "Marimekko chart: columns of different widths split into stacked cells.",
      tags=["marimekko", "mekko chart", "mosaic plot", "variable width", "market map", "share"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(seg(11, 3, 11, 21)), detail(seg(16, 3, 16, 21)),
            detail(seg(3, 13.5, 11, 13.5)), detail(seg(11, 8, 16, 8)), detail(seg(11, 15.5, 16, 15.5)),
            detail(seg(16, 10.5, 21, 10.5))]


_WAF_EMPTY = [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1)]
_WAF_FULL = [(2, 1), (0, 2), (1, 2), (2, 2)]
_WAF_GRID = [seg(9, 3, 9, 21), seg(15, 3, 15, 21), seg(3, 9, 21, 9), seg(3, 15, 21, 15)]


def _waffle_filled():
    cells = [P(rect(2 + 7.25 * c, 2 + 7.25 * r, 5.5, 5.5, 1)) for c in range(3) for r in range(3)]
    return D(U(*cells), *[P(rect(3.5 + 7.25 * c, 3.5 + 7.25 * r, 2.5, 2.5)) for c, r in _WAF_EMPTY])


@icon("chart-waffle", CAT, "Waffle chart: a square grid with the lower cells filled in.",
      tags=["waffle chart", "square pie", "grid chart", "percentage", "proportion", "unit chart"],
      filled=_waffle_filled)
def _(S):
    parts = [shell(rect(3, 3, 18, 18, S.R)), *[detail(d) for d in _WAF_GRID]]
    parts += [sq(5 + 6 * c, 5 + 6 * r, 2, 2, L(S, 0, 0.6)) for c, r in _WAF_FULL]
    return parts


def _person(x, y, S, w=2.5):
    """Small person: head disc and a body (square shoulders in Line, round in Rounded), centred on x."""
    head = circle(x, y, 1.6)
    if S.name == "line":
        body = rect(x - w, y + 2.75, 2 * w, 3.25, 1.25)
    else:
        body = f"M{fmt(x - w)} {fmt(y + 6)}V{fmt(y + 2 + w)}A{fmt(w)} {fmt(w)} 0 0 1 {fmt(x + w)} {fmt(y + 2 + w)}V{fmt(y + 6)}Z"
    return head, body


@icon("chart-pictogram", CAT, "Pictogram chart: rows of person figures, most filled and a few outlined.",
      tags=["pictogram", "isotype", "icon chart", "people chart", "population", "proportion"])
def _(S):
    parts = []
    for row, y in enumerate((4.5, 14)):
        for col, x in enumerate((5, 12, 19)):
            head, body = _person(x, y, S)
            if row == 1 and col == 2:
                parts += [line(circle(x, y, 1.1)), shell(_person(x, y + 0.5, S, 2)[1])]
            else:
                parts += [solid(head), solid(body)]
    return parts


_SA_TOP = [(6, 11.5), (10, 8), (14, 10.5), (20, 5)]
_SA_MID = [(6, 15), (10, 13), (14, 14.5), (20, 11)]


@icon("chart-stacked-area", CAT, "Stacked area chart: two layered areas rising over two axes.",
      tags=["stacked area", "area chart", "cumulative", "layers", "composition", "trend"])
def _(S):
    area = _SA_TOP + [(20, 17), (6, 17)]
    return [axes(S), shell(poly(area, closed=True, r=S.r)), detail(poly(_SA_MID, r=S.r))]


def smooth(points, closed=False):
    """Smooth curve through points (Catmull-Rom converted to cubic Beziers)."""
    pts = list(points)
    n = len(pts)
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d + ("Z" if closed else "")


_SX = [2.5, 7.25, 12, 16.75, 21.5]
_ST_TOP = list(zip(_SX, [8, 5, 7.5, 4, 6]))
_ST_MID = list(zip(_SX, [11.5, 9.5, 12.5, 9.5, 10.5]))
_ST_MID2 = list(zip(_SX, [15, 14, 16.5, 14.5, 15]))
_ST_BOT = list(zip(_SX, [18, 18.5, 20.5, 19.5, 19]))


@icon("chart-streamgraph", CAT, "Streamgraph: flowing bands of changing thickness around a wavy centre.",
      tags=["streamgraph", "stream graph", "theme river", "flowing area", "stacked area", "trend over time"])
def _(S):
    if S.name == "line":
        top, bot = _ST_TOP, _ST_BOT
    else:  # Rounded: the stream ends curve round instead of being cut square
        top = [(3.5, _ST_TOP[0][1] + 0.5)] + _ST_TOP[1:-1] + [(20.5, _ST_TOP[-1][1] + 0.5)]
        bot = [(3.5, _ST_BOT[0][1] - 0.5)] + _ST_BOT[1:-1] + [(20.5, _ST_BOT[-1][1] - 0.5)]
    t, b = smooth(top), smooth(bot[::-1])
    if S.name == "line":
        outline = t + "L" + b[1:] + "Z"
    else:
        (x1, y1), (x0, y0) = top[-1], bot[-1]
        (x2, y2), (x3, y3) = bot[0], top[0]
        outline = (t + f"Q21.5 {fmt((y1 + y0) / 2)} {fmt(x0)} {fmt(y0)}" + b[b.index("C"):]
                   + f"Q2.5 {fmt((y2 + y3) / 2)} {fmt(x3)} {fmt(y3)}Z")
    return [shell(outline, stroke_miterlimit="2"), detail(smooth(_ST_MID)), detail(smooth(_ST_MID2))]


def _ridge(y, xc, h=5.0, w=3.5):
    return (f"M2.5 {fmt(y)}H{fmt(xc - w * 1.6)}C{fmt(xc - w * 0.7)} {fmt(y)} {fmt(xc - w * 0.6)} {fmt(y - h)} {fmt(xc)} {fmt(y - h)}"
            f"C{fmt(xc + w * 0.6)} {fmt(y - h)} {fmt(xc + w * 0.7)} {fmt(y)} {fmt(xc + w * 1.6)} {fmt(y)}H21.5")


@icon("chart-ridgeline", CAT, "Ridgeline plot: three hill shaped curves stacked on offset baselines.",
      tags=["ridgeline", "joy plot", "joyplot", "density", "distribution", "stacked curves"])
def _(S):
    return [line(_ridge(8, 13, 4.5)), line(_ridge(14, 8.5, 4.5)), line(_ridge(20, 15.5, 4.5))]


def _violin(cx, top, bot, bulge_t, w):
    """Closed violin outline: tip at top and bottom, widest (half-width w) at bulge_t (0..1 from top)."""
    yb = top + (bot - top) * bulge_t
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + 1.5)} {fmt(top + 2)} {fmt(cx + w)} {fmt(yb - 3)} {fmt(cx + w)} {fmt(yb)}"
            f"C{fmt(cx + w)} {fmt(yb + 3)} {fmt(cx + 1.5)} {fmt(bot - 2)} {fmt(cx)} {fmt(bot)}"
            f"C{fmt(cx - 1.5)} {fmt(bot - 2)} {fmt(cx - w)} {fmt(yb + 3)} {fmt(cx - w)} {fmt(yb)}"
            f"C{fmt(cx - w)} {fmt(yb - 3)} {fmt(cx - 1.5)} {fmt(top + 2)} {fmt(cx)} {fmt(top)}Z")


@icon("chart-violin", CAT, "Violin plot: two symmetrical violin shapes with a median line.",
      tags=["violin plot", "distribution", "density", "statistics", "spread", "comparison"])
def _(S):
    parts = []
    for cx, top, bot, t, w in ((7, 3, 21, 0.62, 3.5), (17, 3, 21, 0.38, 3.5)):
        yb = top + (bot - top) * t
        if S.name == "line":
            parts.append(shell(_violin(cx, top, bot, t, w), stroke_miterlimit="10"))
        else:
            parts.append(shell(_violin(cx, top + 0.5, bot - 0.5, t, w)))
        parts.append(detail(seg(cx - 1.5, yb, cx + 1.5, yb)))
    return parts


@icon("chart-box-plot", CAT, "Box plot: two boxes with median lines and whiskers above and below.",
      tags=["box plot", "box and whisker", "quartiles", "median", "statistics", "distribution"])
def _(S):
    rr = min(S.R, 1.5)
    parts = []
    for cx, t0, b0, t1, b1, med in ((7, 3.5, 20.5, 8, 15.5, 12), (17, 3.5, 17, 6.5, 12.5, 9)):
        parts += [line(seg(cx, t0, cx, t1)), line(seg(cx, b1, cx, b0)),
                  line(seg(cx - 2, t0, cx + 2, t0)), line(seg(cx - 2, b0, cx + 2, b0)),
                  shell(rect(cx - 3, t1, 6, b1 - t1, rr)), detail(seg(cx - 3, med, cx + 3, med))]
    return parts


# ============================================================================ lines and combinations

@icon("chart-sparkline", CAT, "Sparkline: a small jagged line ending in a dot inside a slim frame.",
      tags=["sparkline", "mini chart", "inline chart", "trend", "micro chart", "kpi"])
def _(S):
    pts = [(5.5, 13.5), (8, 11), (10.5, 14), (13, 10.5), (15.5, 12.5)]
    return [shell(rect(2.5, 6, 19, 12, min(S.R, 3))), detail(poly(pts + [(17.5, 10)], r=S.r * 0.5)), dot(17.75, 10, 1.75)]


_CB = [(6, 12.5), (12, 9), (18, 14.5)]
_CL = [(3.5, 11), (6, 8), (12, 5), (18, 10.5), (20.5, 8)]


@icon("chart-combo", CAT, "Combination chart: bars with a line of markers running across them.",
      tags=["combo chart", "combination chart", "bar and line", "mixed chart", "overlay", "dual series"])
def _(S):
    return [*[line(seg(x, 21, x, y)) for x, y in _CB], line(poly(_CL[1:4], r=S.r)),
            *[dot(x, y, 2) for x, y in _CL[1:4]]]


_PAR = [(4.5, 9.5), (9, 13), (13.5, 16), (18, 18)]


@icon("chart-pareto", CAT, "Pareto chart: bars falling in height under a rising cumulative curve.",
      tags=["pareto", "80/20", "cumulative", "quality", "root cause", "sorted bars"],
      filled=lambda: U(vbars_filled([(x, 21, y) for x, y in _PAR], 3.5)(), ST("M4.5 6C10 3.5 13 3 20.5 3", 2.5)))
def _(S):
    return [*[line(seg(x, 21, x, y)) for x, y in _PAR], line("M4.5 6C10 3.5 13 3 20.5 3")]


# ============================================================================ round charts

_PA = [9, 6, 8, 5, 7.5, 5.5]  # radius per 60 degree wedge, from the top clockwise


def _polar_outline():
    pts = []
    for i, r in enumerate(_PA):
        a0, a1 = -90 + 60 * i, -30 + 60 * i
        pts += [polar(12, 12, r, a0 + (a1 - a0) * k / 6) for k in range(7)]
    return pts


@icon("chart-polar-area", CAT, "Polar area chart: equal angle wedges with different lengths.",
      tags=["polar area", "rose chart", "nightingale chart", "coxcomb", "radial", "proportion"])
def _(S):
    d = ""
    for i, r in enumerate(_PA):
        a0, a1 = -90 + 60 * i, -30 + 60 * i
        p0, p1 = polar(12, 12, r, a0), polar(12, 12, r, a1)
        d += ("M" if i == 0 else "L") + f"{fmt(p0[0])} {fmt(p0[1])}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(p1[0])} {fmt(p1[1])}"
    d += "Z"
    spokes = [detail(seg(12, 12, *polar(12, 12, min(_PA[i], _PA[i - 1]), -90 + 60 * i))) for i in range(6)]
    return [shell(d, stroke_miterlimit="10" if S.name == "line" else "4"), *spokes]


@icon("chart-radial-bar", CAT, "Radial bar chart: concentric arcs of different lengths starting at the top.",
      tags=["radial bar", "circular bar", "progress rings", "activity rings", "radial progress", "goals"])
def _(S):
    return [line(arc(12, 12, 9, -90, 180)), line(arc(12, 12, 5.5, -90, 90)), line(arc(12, 12, 2, -90, 0))]


def arc_pts(cx, cy, r, a0, a1, n=12):
    return [polar(cx, cy, r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]


@icon("chart-sunburst", CAT, "Sunburst chart: an inner ring of segments with a finer outer ring around it.",
      tags=["sunburst", "multilevel pie", "radial treemap", "hierarchy", "nested", "breakdown"])
def _(S):
    outline = arc_pts(12, 12, 9, -90, 150, 16) + arc_pts(12, 12, 5.5, 150, 270, 8)
    parts = [shell(poly(outline, closed=True, r=S.r)), detail(arc(12, 12, 5.5, -90, 150))]
    parts += [detail(seg(12, 12, *polar(12, 12, 5.5, a))) for a in (-90, 30, 150)]
    parts += [detail(seg(*polar(12, 12, 5.5, a), *polar(12, 12, 9, a))) for a in (-30, 30, 90)]
    return parts


def _chord(a, b, r=9, pull=0.35):
    p, q = polar(12, 12, r - 1.5, a), polar(12, 12, r - 1.5, b)
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    cx, cy = mx + (12 - mx) * pull, my + (12 - my) * pull
    return f"M{fmt(p[0])} {fmt(p[1])}Q{fmt(cx)} {fmt(cy)} {fmt(q[0])} {fmt(q[1])}"


@icon("chart-chord", CAT, "Chord diagram: arc segments on a circle joined by curved ribbons.",
      tags=["chord diagram", "relationships", "flows", "connections", "matrix", "network"])
def _(S):
    rim = [line(arc(12, 12, 9, a0, a1)) for a0, a1 in ((-80, 10), (25, 115), (130, 265))]
    return [*rim, line(_chord(-30, 75, pull=0.1)), line(_chord(-60, 200, pull=0.5)), line(_chord(100, 225, pull=0.1))]


@icon("chart-arc-diagram", CAT, "Arc diagram: dots on a line joined by arcs of different sizes.",
      tags=["arc diagram", "network", "links", "connections", "relationships", "nodes"])
def _(S):
    xs = [3.5, 9, 14, 20.5]
    y = 18
    arcs = [line(arc((xs[0] + xs[2]) / 2, y, (xs[2] - xs[0]) / 2, 180, 360)),
            line(arc((xs[1] + xs[3]) / 2, y, (xs[3] - xs[1]) / 2, 180, 360)),
            line(arc((xs[2] + xs[3]) / 2, y, (xs[3] - xs[2]) / 2, 180, 360))]
    return [line(seg(2, y, 22, y)), *arcs, *[dot(x, y, 2) for x in xs]]


_PC_X = [3, 9, 15, 21]


@icon("chart-parallel-coordinates", CAT, "Parallel coordinates plot: zigzag lines crossing four vertical axes.",
      tags=["parallel coordinates", "multivariate", "multidimensional", "profiles", "axes", "comparison"])
def _(S):
    return [*[line(seg(x, 3, x, 21)) for x in _PC_X],
            line(poly(list(zip(_PC_X, (5.5, 11, 6, 13))), r=S.r)),
            line(poly(list(zip(_PC_X, (13.5, 18.5, 17, 6.5))), r=S.r))]


@icon("chart-slope", CAT, "Slope chart: lines joining values on two vertical axes.",
      tags=["slope chart", "slopegraph", "before and after", "change", "ranking", "comparison"])
def _(S):
    pairs = [(5.5, 12), (12, 18), (18.5, 5.5)]
    parts = [line(seg(4, 3, 4, 21)), line(seg(20, 3, 20, 21))]
    for a, b in pairs:
        parts += [line(seg(4, a, 20, b)), dot(4, a, 2), dot(20, b, 2)]
    return parts


_BUMP_X = [3.5, 12, 20.5]
_BUMP = [(5, 18, 11.5), (11.5, 5, 18), (18, 11.5, 5)]


@icon("chart-bump", CAT, "Bump chart: ranked lines crossing each other with a dot at every step.",
      tags=["bump chart", "rank chart", "ranking over time", "positions", "league table", "standings"])
def _(S):
    parts = []
    for ys in _BUMP:
        pts = list(zip(_BUMP_X, ys))
        parts += [line(poly(pts, r=S.r)), *[mark(S, x, y, 2) for x, y in pts]]
    return parts


_HM = ["2102", "1210", "0121", "2012"]  # per row: 2 full cell, 1 medium cell, 0 empty


def _heat_filled():
    cuts = []
    for r, row in enumerate(_HM):
        for c, v in enumerate(row):
            x, y = 6 + 4 * c, 6 + 4 * r
            if v == "1":
                cuts.append(P(rect(x - 1, y - 1, 2, 2)))
            elif v == "0":
                cuts.append(P(rect(x - 1.75, y - 1.75, 3.5, 3.5, 0.5)))
    return D(P(rect(2, 2, 20, 20, 3)), *cuts)


@icon("chart-heatmap", CAT, "Heat map: a grid of cells, some solid, some half toned, some empty.",
      tags=["heat map", "heatmap", "matrix", "intensity", "density", "grid"], filled=_heat_filled)
def _(S):
    parts = [shell(rect(3, 3, 18, 18, min(S.R, 2.5)))]
    rr = L(S, 0, 0.5)
    for r, row in enumerate(_HM):
        for c, v in enumerate(row):
            x, y = 6 + 4 * c, 6 + 4 * r
            if v == "2":
                parts.append(sq(x - 1.5, y - 1.5, 3, 3, rr))
            elif v == "1":
                parts.append(sq(x - 0.75, y - 0.75, 1.5, 1.5, 0))
    return parts


@icon("chart-circle-packing", CAT, "Circle packing chart: small circles of different sizes inside a large circle.",
      tags=["circle packing", "packed bubbles", "bubble hierarchy", "nested circles", "hierarchy", "proportion"])
def _(S):
    k = L(S, 0, 0.3)  # Rounded: plumper inner circles
    return [shell(circle(12, 12, 9)), dot(9.25, 10, 2.75 + k), dot(15.25, 11, 2 + k), dot(11.5, 16.25, 1.75 + k)]


@icon("chart-dendrogram", CAT, "Dendrogram: square brackets joining leaves into branches up to one root.",
      tags=["dendrogram", "cluster tree", "hierarchical clustering", "tree diagram", "taxonomy", "clusters"])
def _(S):
    r = S.r * 0.66
    return [line(poly([(3.5, 21), (3.5, 14.5), (9, 14.5), (9, 21)], r=r)),
            line(poly([(15, 21), (15, 17), (20.5, 17), (20.5, 21)], r=r)),
            line(poly([(6.25, 14.5), (6.25, 8), (17.75, 8), (17.75, 17)], r=r)),
            line(seg(12, 8, 12, 3))]


@icon("chart-quadrant", CAT, "Quadrant chart: crossed axes dividing a square into four parts with dots.",
      tags=["quadrant chart", "2x2 matrix", "priority matrix", "magic quadrant", "scatter", "positioning"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(seg(12, 3, 12, 21)), detail(seg(3, 12, 21, 12)),
            dot(7, 7.5, 1.75), dot(15.5, 6.5, 1.5), dot(18, 9.5, 1.5), dot(8, 17, 1.5), dot(16.5, 16, 1.75)]


# ============================================================================ matrices and statistics

@icon("scatter-plot-matrix", CAT, "Scatter plot matrix: a grid of panels with dots, bars on the diagonal.",
      tags=["scatter plot matrix", "splom", "pair plot", "pairs", "correlation", "multivariate"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, min(S.R, 2.5))), detail(seg(12, 3, 12, 21)), detail(seg(3, 12, 21, 12))]
    parts += [sq(5.5, 7.5, 1.75, 3), sq(8.25, 5.5, 1.75, 5), sq(14.5, 15.5, 1.75, 3), sq(17.25, 14, 1.75, 4.5)]
    parts += [dot(15.5, 9, 1.1), dot(18.25, 6.25, 1.1), dot(6.5, 18, 1.1), dot(9, 15, 1.1)]
    return parts


_CM_CELLS = [(0, 0, 1.75), (0, 1, 1.0), (1, 1, 1.75), (0, 2, 1.25), (1, 2, 0.75), (2, 2, 1.75)]


@icon("correlation-matrix", CAT, "Correlation matrix: a staircase of cells holding circles of different sizes.",
      tags=["correlation matrix", "correlogram", "correlation", "coefficients", "statistics", "matrix"])
def _(S):
    outline = [(3, 3), (9, 3), (9, 9), (15, 9), (15, 15), (21, 15), (21, 21), (3, 21)]
    parts = [shell(poly(outline, closed=True, r=S.r * 0.66)),
             detail(seg(3, 9, 9, 9)), detail(seg(3, 15, 15, 15)), detail(seg(9, 9, 9, 21)), detail(seg(15, 15, 15, 21))]
    parts += [dot(6 + 6 * c, 6 + 6 * r, rad) for c, r, rad in _CM_CELLS]
    return parts


@icon("chart-control", CAT, "Control chart: a zigzag of points between two dashed limit lines and a centre line.",
      tags=["control chart", "shewhart chart", "spc", "process control", "limits", "quality"])
def _(S):
    pts = [(3, 13.5), (7.5, 9), (12, 15), (16.5, 8.5), (21, 12)]
    return [*[line(d) for d in dash_pts([(2, 4), (22, 4)], S)], *[line(d) for d in dash_pts([(2, 20), (22, 20)], S)],
            line(poly(pts, r=S.r)), *[dot(x, y, 1.75) for x, y in pts[1:4]]]


@icon("chart-ohlc", CAT, "OHLC chart: price bars with open ticks to the left and close ticks to the right.",
      tags=["ohlc", "open high low close", "price bars", "stock chart", "trading", "market"])
def _(S):
    bars = [(5, 6, 17, 14, 9), (12, 3.5, 13, 11, 5.5), (19, 8, 20.5, 10, 17.5)]
    parts = []
    for x, top, bot, o, c in bars:
        parts += [line(seg(x, top, x, bot)), line(seg(x - 3, o, x, o)), line(seg(x, c, x + 3, c))]
    return parts


_RENKO = [(3, 15), (7.5, 10.5), (12, 6)]  # rising bricks (hollow)
_RENKO_DOWN = (16.5, 10.5)  # falling brick (solid)


@icon("chart-renko", CAT, "Renko chart: equal bricks stepping diagonally up, then one stepping down.",
      tags=["renko", "brick chart", "price bricks", "trading", "trend", "stock chart"],
      filled=lambda: U(*[D(P(rect(x - 1, y - 1, 6, 6, 0.75)), P(rect(x + 1, y + 1, 2, 2))) for x, y in _RENKO],
                       P(rect(_RENKO_DOWN[0] - 0.25, _RENKO_DOWN[1] - 0.25, 5.5, 5.5, 0.75))))
def _(S):
    rr = L(S, 0, 1)
    parts = [shell(rect(x, y, 4, 4, rr)) for x, y in _RENKO]
    x, y = _RENKO_DOWN
    parts.append(solid(rect(x + 0.25, y + 0.25, 4.75, 4.75, L(S, 0, 1.25))))
    return parts


def _xmark(x, y, h=1.75):
    return [line(seg(x - h, y - h, x + h, y + h)), line(seg(x - h, y + h, x + h, y - h))]


@icon("chart-point-and-figure", CAT, "Point and figure chart: columns of stacked X marks and O marks.",
      tags=["point and figure", "p&f chart", "x and o", "trading", "price chart", "technical analysis"])
def _(S):
    parts = []
    for y in (9, 14.5, 20):
        parts += _xmark(5, y)
    for y in (5.5, 12):
        parts.append(line(circle(12, y, 2)))
    for y in (4, 9.5, 15):
        parts += _xmark(19, y)
    return parts


@icon("chart-confidence-band", CAT, "Confidence band: a centre line inside a shaded band that widens to the right.",
      tags=["confidence interval", "confidence band", "uncertainty", "error band", "range", "prediction"])
def _(S):
    band = [(7, 12), (11.5, 9.5), (16, 7.5), (20.5, 3.5), (20.5, 16), (16, 15), (11.5, 15.5), (7, 17)]
    mid = [(7, 14.5), (11.5, 12.5), (16, 11.25), (20.5, 9.75)]
    return [axes(S), shell(poly(band, closed=True, r=S.r)), detail(poly(mid, r=S.r))]


_EB = [(5, 13), (12, 8), (19, 11)]


@icon("chart-error-bars", CAT, "Bar chart with an error whisker on top of each bar.",
      tags=["error bars", "whiskers", "uncertainty", "standard error", "confidence", "bar chart"],
      filled=lambda: U(vbars_filled([(x, 21, y) for x, y in _EB], 3.5)(),
                       *[ST(poly([(x - 2, y - 3.5), (x + 2, y - 3.5)]), 2.5) for x, y in _EB],
                       *[ST(seg(x, y - 3.5, x, y), 2.5) for x, y in _EB]))
def _(S):
    parts = []
    for x, y in _EB:
        parts += [line(seg(x, 21, x, y + 3)), line(seg(x, y - 3.5, x, y + 3)),
                  line(seg(x - 2.25, y - 3.5, x + 2.25, y - 3.5)), line(seg(x - 2.25, y + 3, x + 2.25, y + 3))]
    return parts


@icon("chart-regression", CAT, "Regression plot: scattered dots around a straight trend line on two axes.",
      tags=["regression", "trend line", "line of best fit", "linear regression", "correlation", "scatter"])
def _(S):
    return [axes(S), line(seg(6, 18, 20.5, 5)), dot(8.5, 13, 1.5), dot(11.5, 16.5, 1.5), dot(13.5, 10, 1.5),
            dot(17, 13, 1.5), dot(18, 5, 1.5)]


@icon("chart-density", CAT, "Density plot: a smooth hill shaped area rising from a baseline.",
      tags=["density plot", "kernel density", "kde", "distribution", "area", "probability"])
def _(S):
    j = L(S, "miter", "round")
    hill = "M2.5 19.5C6.5 19.5 6.5 5.5 10.5 5.5C14.5 5.5 14 13 17 15.5C19 17.5 20.5 19.5 21.5 19.5Z"
    return [shell(hill, stroke_miterlimit="10" if j == "miter" else "4")]


@icon("chart-timeline", CAT, "Timeline: a line with dated points and labels above and below.",
      tags=["timeline", "chronology", "milestones", "history", "events", "roadmap"])
def _(S):
    r = S.r * 0.5
    return [line(seg(2, 12, 22, 12)), line(poly([(5, 12), (5, 5), (10, 5)], r=r)), line(poly([(12, 12), (12, 19), (17, 19)], r=r)),
            line(poly([(19, 12), (19, 5), (14, 5)], r=r)), dot(5, 12, 2.25), dot(12, 12, 2.25), dot(19, 12, 2.25)]


# ============================================================================ process and planning diagrams

@icon("chart-fishbone", CAT, "Fishbone diagram: a spine to a head box with bones branching above and below.",
      tags=["fishbone", "ishikawa", "cause and effect", "root cause analysis", "problem solving", "quality"])
def _(S):
    return [line(seg(2.5, 12, 16, 12)), shell(rect(16, 8.5, 5.5, 7, min(S.R, 1.5))),
            line(seg(4, 4.5, 7.5, 12)), line(seg(9.5, 4.5, 13, 12)), line(seg(4, 19.5, 7.5, 12)), line(seg(9.5, 19.5, 13, 12))]


@icon("chart-burnup", CAT, "Burn up chart: a jagged line climbing towards a dashed scope line.",
      tags=["burn up chart", "burnup", "sprint", "agile", "scope", "progress"])
def _(S):
    work = [(6, 18), (9, 15), (12, 15.5), (15, 11), (18, 10.5), (20.5, 8.5)]
    return [axes(S), *[line(d) for d in dash_pts([(6.5, 5), (21.5, 5)], S)], line(poly(work, r=S.r))]


_COH = ["210", "10", "1"]


def _cohort_filled():
    cells = []
    for r, row in enumerate(_COH):
        for c, v in enumerate(row):
            x, y = 2 + 7 * c, 2 + 7 * r
            cell = P(rect(x, y, 6, 6, 1))
            if v == "1":
                cell = D(cell, P(rect(x + 2, y + 2, 2, 2)))
            elif v == "0":
                cell = D(cell, P(rect(x + 1.5, y + 1.5, 3, 3)))
            cells.append(cell)
    return U(*cells)


@icon("chart-cohort", CAT, "Cohort table: a staircase of cells that fade from solid to empty to the right.",
      tags=["cohort analysis", "cohort table", "retention", "churn", "triangle table", "customer cohorts"],
      filled=_cohort_filled)
def _(S):
    outline = [(3, 3), (21, 3), (21, 9), (15, 9), (15, 15), (9, 15), (9, 21), (3, 21)]
    parts = [shell(poly(outline, closed=True, r=S.r * 0.66)),
             detail(seg(3, 9, 15, 9)), detail(seg(3, 15, 9, 15)), detail(seg(9, 3, 9, 15)), detail(seg(15, 3, 15, 9))]
    rr = L(S, 0, 0.6)
    for r, row in enumerate(_COH):
        for c, v in enumerate(row):
            x, y = 6 + 6 * c, 6 + 6 * r
            if v == "2":
                parts.append(sq(x - 2, y - 2, 4, 4, 0))
            elif v == "1":
                parts.append(sq(x - 1, y - 1, 2, 2, rr))
    return parts


def _cloud(S):
    if S.name == "line":
        return "M5.5 19.5H18.5A3.5 3.5 0 0 0 19 12.55A5.5 5.5 0 0 0 8.8 9.4A4.5 4.5 0 0 0 5.5 19.5Z"
    return "M6 19.5H18A3.5 3.5 0 0 0 19 12.65A5.5 5.5 0 0 0 8.8 9.4A4.5 4.5 0 0 0 6 19.5Z"


@icon("chart-word-cloud", CAT, "Word cloud: word bars of different weights packed inside a cloud.",
      tags=["word cloud", "tag cloud", "text analysis", "keywords", "frequency", "text mining"])
def _(S):
    rr = L(S, 0, 1)
    return [shell(_cloud(S), stroke_miterlimit="10"), sq(7.5, 12.5, 7, 3, rr), detail(seg(8, 17, 11, 17)),
            detail(seg(13.5, 17, 17, 17)), detail(seg(16.5, 13.5, 18, 13.5))]


_BEE = [(4, [12]), (7.5, [10, 14]), (11, [8.25, 12, 15.75]), (14.5, [10, 14]), (18, [8.25, 12, 15.75]), (21, [12])]


@icon("chart-beeswarm", CAT, "Beeswarm plot: dots packed along a line, bulging where values cluster.",
      tags=["beeswarm", "swarm plot", "jitter plot", "distribution", "dots", "clusters"],
      filled=lambda: U(*[P(circle(x, y, 1.75)) for x, ys in _BEE for y in ys]))
def _(S):
    return [dot(x, y, 1.5) if S.name == "rounded" else mark(S, x, y, 1.5) for x, ys in _BEE for y in ys]


_DOTS = [(4.5, 2), (9.5, 4), (14.5, 3), (19.5, 1)]


@icon("chart-dot-plot", CAT, "Dot plot: columns of stacked dots of different heights on a baseline.",
      tags=["dot plot", "dot histogram", "tally", "frequency", "counts", "distribution"])
def _(S):
    parts = [line(seg(2, 21, 22, 21))]
    for x, n in _DOTS:
        parts += [dot(x, 17 - 4.25 * i, 1.9) for i in range(n)]
    return parts


_SP_CY = 11.5


def _spiral_d():
    """Spiral of half-turn arcs, radius growing by 2 each half turn (arms 4 px apart)."""
    ca, cb, cy = 12.0, 14.0, _SP_CY
    d = f"M{fmt(ca + 1)} {fmt(cy)}"
    for i, r in enumerate((1, 3, 5, 7)):
        c = ca if i % 2 == 0 else cb
        end = c - r if i % 2 == 0 else c + r
        d += f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(end)} {fmt(cy)}"
    return d + f"A9 9 0 0 1 {fmt(ca)} {fmt(cy + 9)}"


@icon("chart-spiral", CAT, "Spiral plot: a line winding out from the centre with dots along it.",
      tags=["spiral plot", "spiral chart", "time spiral", "cyclical data", "seasonality", "periodic"])
def _(S):
    cy = _SP_CY
    return [line(_spiral_d()), dot(14, cy - 7, 2), dot(12, cy + 5, 2), dot(12, cy + 9, 2)]


def _tri(t, u):
    """Point in the ternary triangle from barycentric-like coordinates (t along the base, u up)."""
    A, B, C = (3, 20), (21, 20), (12, 4.41)
    return (A[0] + (B[0] - A[0]) * t + (C[0] - A[0]) * u, A[1] + (B[1] - A[1]) * t + (C[1] - A[1]) * u)


@icon("chart-ternary", CAT, "Ternary plot: a triangle with an inner grid and a few dots.",
      tags=["ternary plot", "triangle plot", "simplex", "three variables", "composition", "phase diagram"])
def _(S):
    tri = [(3, 20), (21, 20), (12, 4.41)]
    grid = [seg(*_tri(0, 0.4), *_tri(0.6, 0.4)), seg(*_tri(0.36, 0), *_tri(0.36, 0.64)), seg(*_tri(0.75, 0), *_tri(0, 0.75))]
    return [shell(poly(tri, closed=True, r=S.r), stroke_miterlimit="10"), *[detail(g) for g in grid],
            dot(*_tri(0.14, 0.14), 1.25), dot(*_tri(0.62, 0.12), 1.25)]




# ============================================================================ 3D and round variants

_B3 = [(3, 14), (8.5, 10), (14, 5.5)]  # front-left x, front top y (bars rise left to right)
_B3_W, _B3_DX, _B3_DY, _B3_BASE = 5.5, 2, 2.5, 21


def _b3_filled():
    w, dx, dy, base = _B3_W, _B3_DX, _B3_DY, _B3_BASE
    shells = [p.d for p in _b3_parts(LINE)]
    body = U(*[U(P(d), ST(d, 2, "butt", "miter", 10)) for d in shells])
    cuts = []
    for i, (x, top) in enumerate(_B3):
        x2 = x + w
        cuts.append(ST(seg(x, top, x2 + (dx if i == len(_B3) - 1 else 0), top), 1.5))
        cuts.append(ST(seg(x2, top, x2, base), 1.5))
    return D(body, *cuts)


@icon("chart-3d-bar", CAT, "3D bar chart: three box shaped bars rising in height.",
      tags=["3d bar chart", "3d column chart", "isometric bars", "bar chart", "perspective", "statistics"],
      filled=lambda: _b3_filled())
def _b3_parts(S):
    w, dx, dy, base = _B3_W, _B3_DX, _B3_DY, _B3_BASE
    parts = []
    for i, (x, top) in enumerate(_B3):
        x2 = x + w
        parts.append(shell(poly([(x, base), (x, top), (x2, top), (x2, base)], closed=True, r=0)))
        if i < len(_B3) - 1:
            face = [(x, top), (x + dx, top - dy), (x2, top - dy), (x2, top)]
        else:
            face = [(x, top), (x + dx, top - dy), (x2 + dx, top - dy), (x2 + dx, base - dy), (x2, base), (x2, top)]
        parts.append(shell(poly(face, closed=True, r=0), stroke_miterlimit="10" if S.name == "line" else "4"))
    return parts


@icon("chart-pie-3d", CAT, "3D pie chart: a tilted pie with visible thickness and slice lines.",
      tags=["3d pie chart", "tilted pie", "pie chart", "perspective", "proportion", "share"])
def _(S):
    cx, cy, rx, ry, t = 12, 9.5, 9.5, L(S, 5.5, 6), 5
    outline = (f"M{fmt(cx - rx)} {fmt(cy)}A{fmt(rx)} {fmt(ry)} 0 0 1 {fmt(cx + rx)} {fmt(cy)}V{fmt(cy + t)}"
               f"A{fmt(rx)} {fmt(ry)} 0 0 1 {fmt(cx - rx)} {fmt(cy + t)}Z")
    rim = f"M{fmt(cx - rx)} {fmt(cy)}A{fmt(rx)} {fmt(ry)} 0 0 0 {fmt(cx + rx)} {fmt(cy)}"
    a = math.radians(60)
    px, py = cx + rx * math.cos(a), cy + ry * math.sin(a)
    parts = [shell(outline, stroke_miterlimit="10" if S.name == "line" else "4"), detail(rim),
             detail(seg(cx, cy, cx - 5, cy - ry * 0.83)), detail(seg(cx, cy, px, py)), detail(seg(px, py, px, py + t))]
    return parts


@icon("chart-dual-axis", CAT, "Dual axis chart: bars and a line between left and right scales with ticks.",
      tags=["dual axis", "two axes", "secondary axis", "combo chart", "bar and line", "two scales"])
def _(S):
    frame = [(3, 3), (3, 21), (21, 21), (21, 3)]
    ticks = [line(seg(3, y, 5.5, y)) for y in (7, 14)] + [line(seg(18.5, y, 21, y)) for y in (7, 14)]
    return [line(poly(frame, r=S.r)), *ticks, line(seg(9, 20, 9, 13)), line(seg(15, 20, 15, 16.5)),
            line(poly([(7, 12), (12, 8.5), (17, 5)], r=S.r))]


def _ring_sectors(cx, cy, r0, r1, angles):
    return [arc_pts(cx, cy, r1, a0, a1, 8) + arc_pts(cx, cy, r0, a1, a0, 6) for a0, a1 in zip(angles, angles[1:])]


@icon("chart-half-donut", CAT, "Half donut chart: a semicircular ring split into three segments.",
      tags=["half donut", "semi circle donut", "half pie", "gauge chart", "proportion", "progress"])
def _(S):
    cx, cy = 12, 17.5
    outline = arc_pts(cx, cy, 9.5, 180, 360, 16) + arc_pts(cx, cy, 4.5, 360, 180, 10)
    parts = [shell(poly(outline, closed=True, r=S.r), stroke_miterlimit="10")]
    parts += [detail(seg(*polar(cx, cy, 4.5, a), *polar(cx, cy, 9.5, a))) for a in (235, 300)]
    return parts


@icon("chart-nested-donut", CAT, "Nested donut chart: two rings, each split into segments at different angles.",
      tags=["nested donut", "multi level donut", "double donut", "concentric rings", "comparison", "proportion"])
def _(S):
    g = L(S, 12, 16)  # gap in degrees; Rounded caps need a wider gap
    outer = [(-90, 40), (40, 160), (160, 270)]
    inner = [(-30, 120), (120, 330)]
    parts = [line(arc(12, 12, 9, a0 + g / 2, a1 - g / 2)) for a0, a1 in outer]
    parts += [line(arc(12, 12, 4.75, a0 + g * 0.9, a1 - g * 0.9)) for a0, a1 in inner]
    return parts


def _seats():
    seats = []
    for r, n in ((9, 9), (5, 5)):
        for i in range(n):
            a = 180 + 180 * i / (n - 1)
            seats.append(polar(12, 17.5, r, a))
    return seats


@icon("parliament-chart", CAT, "Parliament chart: seats as dots arranged in a semicircle of curved rows.",
      tags=["parliament chart", "seat chart", "hemicycle", "election results", "seats", "legislature"])
def _(S):
    return [mark(S, x, y, 1.5) for x, y in _seats()] + [line(seg(2, 21, 22, 21))]


@icon("chart-proportional-area", CAT, "Proportional area chart: three squares of increasing size on one baseline.",
      tags=["proportional area", "area chart", "size comparison", "scale", "squares", "magnitude"])
def _(S):
    return [sq(2, 17, 3, 3, L(S, 0, 0.75)), shell(rect(8, 15.5, 3.5, 3.5, L(S, 0, 1))), shell(rect(15, 13, 6, 6, L(S, 0, 2)))]


# ============================================================================ annotated and derived line charts

_SM_LINES = [[(0, 3), (1.5, 1), (3, 2.5), (4.5, 0.5)], [(0, 0.5), (1.5, 2), (3, 1.5), (4.5, 3.5)],
             [(0, 3.5), (2, 2.5), (4.5, 0)], [(0, 1.5), (1.5, 3), (3, 0.5), (4.5, 2)]]


@icon("chart-small-multiples", CAT, "Small multiples: a two by two grid of frames, each with a tiny line graph.",
      tags=["small multiples", "trellis chart", "facet grid", "panel chart", "lattice", "sparklines"])
def _(S):
    parts = []
    rr = L(S, 0.5, 1.5)
    for k, (x, y) in enumerate(((3, 3), (14, 3), (3, 14), (14, 14))):
        parts.append(shell(rect(x, y, 7, 7, rr)))
        pts = [(x + 1.25 + px, y + 1.75 + py) for px, py in _SM_LINES[k]]
        parts.append(detail(poly(pts, r=S.r * 0.3)))
    return parts


@icon("chart-radial-tree", CAT, "Radial tree: a central node branching out to child and grandchild nodes.",
      tags=["radial tree", "radial dendrogram", "hierarchy", "mind map", "tree", "network"])
def _(S):
    parts = []
    kids = [-90, 30, 150]
    for a in kids:
        k = polar(12, 12, 5, a)
        parts.append(line(seg(12, 12, *k)))
        for da in (-28, 28):
            g = polar(12, 12, 9.25, a + da)
            parts += [line(seg(*k, *g)), mark(S, *g, 1.6)]
        parts.append(mark(S, *k, 1.6))
    parts.append(dot(12, 12, 2.25))
    return parts


@icon("chart-positive-negative", CAT, "Positive and negative area chart: a solid rise above a zero line and an outlined dip below it.",
      tags=["positive negative", "above and below", "gain and loss", "surplus deficit", "zero line", "area chart"])
def _(S):
    up = "M3 12C5.5 12 5.5 4 8 4C10.5 4 10.5 12 12.5 12Z"
    return [line(seg(2, 12, 22, 12)), solid(up),
            shell(smooth([(12.5, 12), (16, 19.5), (19.5, 16), (21, 12)]) + "Z")]


@icon("chart-annotation", CAT, "Annotated chart: a line chart with one point marked and a note box pointing to it.",
      tags=["annotation", "chart note", "callout", "insight", "highlight", "comment"])
def _(S):
    pts = [(2.5, 20.5), (7, 16), (11, 19), (15, 15.5), (21.5, 19)]
    bubble = [(8.5, 3), (21.5, 3), (21.5, 9.5), (17, 9.5), (15, 11.5), (13, 9.5), (8.5, 9.5)]
    return [line(poly(pts, r=S.r)), dot(15, 15.5, 2.25),
            shell(poly(bubble, closed=True, r=S.r)), detail(seg(11.5, 6.25, 18.5, 6.25))]


@icon("chart-drilldown", CAT, "Drilldown chart: one tall bar expanding into three smaller bars.",
      tags=["drill down", "drilldown", "breakdown", "detail view", "zoom in", "explore data"])
def _(S):
    rr = L(S, 0, 1.25)
    parts = [shell(rect(3, 4, 4.5, 16.5, rr))]
    parts += [line(d) for d in dash_pts([(9.5, 5), (13, 8.5)], S, 2, 1.5)]
    parts += [line(d) for d in dash_pts([(9.5, 20.5), (13, 20.5)], S, 2, 1.5)]
    parts += [line(seg(15, 20.5, 15, 11)), line(seg(18, 20.5, 18, 14.5)), line(seg(21, 20.5, 21, 17))]
    return parts


@icon("chart-forecast", CAT, "Forecast chart: a solid line that continues as a dashed line inside a widening cone.",
      tags=["forecast", "prediction", "projection", "estimate", "future trend", "confidence cone"])
def _(S):
    hist = [(2.5, 18), (6, 14.5), (9, 16), (12.5, 12)]
    cone = [(12.5, 12), (21.5, 4), (21.5, 16)]
    parts = [line(poly(hist, r=S.r)), shell(poly(cone, closed=True, r=S.r * 0.5), stroke_miterlimit="10")]
    parts += [detail(d) for d in dash_pts([(15.5, 10.5), (21.5, 8)], S, 2, 1.75)]
    return parts


@icon("chart-moving-average", CAT, "Moving average: a jagged zigzag line with a smooth curve running through it.",
      tags=["moving average", "rolling average", "smoothing", "trend line", "sma", "signal and noise"])
def _(S):
    zig = [(2.5, 17), (5.5, 11), (8.5, 17.5), (11.5, 9), (14.5, 14.5), (17.5, 5), (21.5, 9)]
    return [line(poly(zig, r=S.r * 0.5)), line("M2.5 15C8 15.5 12 13 15 10.5S19.5 7.5 21.5 7.5")]


_GT_ROUND = "M8.5 13.15V5.5A3 3 0 0 1 14.5 5.5V13.15A4.5 4.5 0 1 1 8.5 13.15Z"
_GT_LINE = "M8.5 13.15V2.5H14.5V13.15A4.5 4.5 0 1 1 8.5 13.15Z"
_GT_TICKS = [(4.5, 21), (8.5, 19.5), (12.5, 19.5)]


@icon("goal-thermometer", CAT, "Goal thermometer: a tube filled two thirds up with tick marks for a target.",
      tags=["goal thermometer", "fundraising", "donation goal", "target", "progress", "campaign"],
      filled=lambda: U(D(U(P(_GT_ROUND), ST(_GT_ROUND, 2)), P(rect(10.5, 4.5, 2, 4))),
                       *[ST(seg(17.5, y, x1, y), 2.5) for y, x1 in _GT_TICKS]))
def _(S):
    return [shell(_GT_LINE if S.name == "line" else _GT_ROUND), sq(10.5, 8.5, 2, 7), dot(11.5, 16.5, 2.25),
            *[line(seg(17.5, y, x1, y)) for y, x1 in _GT_TICKS]]


@icon("chart-period-comparison", CAT, "Period comparison: this period as a solid line over last period as a dashed line.",
      tags=["period over period", "year over year", "compare periods", "previous period", "yoy", "benchmark"])
def _(S):
    cur = [(6, 15), (10, 9.5), (13.5, 12), (17, 6.5), (20.5, 4)]
    prev = [(6, 18), (10, 15), (13.5, 16.5), (17, 13), (20.5, 11.5)]
    return [axes(S), line(poly(cur, r=S.r)), *[line(d) for d in dash_pts(prev, S, 2, 1.75)]]


# ============================================================================ economics and growth curves

@icon("break-even-chart", CAT, "Break even chart: a rising revenue line crossing a flatter cost line at a dot.",
      tags=["break even", "breakeven point", "cost volume profit", "revenue and cost", "profit", "finance"])
def _(S):
    # revenue (6,19)->(21,4); cost (6,13.5)->(21,9.5); crossing at x where both meet
    r0, r1, c0, c1 = (6, 19), (21, 4), (6, 13), (21, 9)
    t = (c0[1] - r0[1]) / ((r1[1] - r0[1]) - (c1[1] - c0[1]))
    ix, iy = r0[0] + (r1[0] - r0[0]) * t, r0[1] + (r1[1] - r0[1]) * t
    return [axes(S), line(seg(*r0, *r1)), line(seg(*c0, *c1)), dot(ix, iy, 2.5)]


@icon("supply-demand-curve", CAT, "Supply and demand curves crossing in an X at an equilibrium dot.",
      tags=["supply and demand", "equilibrium", "economics", "market price", "curves", "price and quantity"])
def _(S):
    return [axes(S), line("M6.5 18.5C11 17 16 12 20 4"), line("M6.5 4C8.5 12 13 17 20.5 18"), dot(12.9, 13.4, 2.5)]


@icon("long-tail-distribution", CAT, "Long tail distribution: a curve that drops steeply and then trails off low to the right.",
      tags=["long tail", "power law", "pareto distribution", "niche", "zipf", "distribution"])
def _(S):
    bars = [(4, 7), (7, 12), (10, 14.5), (13, 16), (16, 17), (19, 17.5)]
    return [line("M2.5 3C4.5 10 8 11.5 12 12.5C15 13.2 18 13.5 21.5 13.5"),
            *[line(seg(x, 21, x, y + 3)) for x, y in bars]]


@icon("s-curve", CAT, "S curve: a logistic curve starting flat, rising steeply and levelling off.",
      tags=["s curve", "logistic curve", "sigmoid", "adoption curve", "growth curve", "saturation"])
def _(S):
    return [axes(S), line("M6.5 18C13 18 12 6 20.5 6")]


@icon("exponential-growth", CAT, "Exponential growth: a curve that starts nearly flat and shoots up steeply.",
      tags=["exponential growth", "hockey stick", "compound growth", "rapid growth", "viral", "curve"])
def _(S):
    return [axes(S), line("M6.5 18C13 18 17.5 15 20 4")]


_BL = 20.5  # distribution baseline


def _baseline():
    return line(seg(2, _BL, 22, _BL))


@icon("normal-distribution", CAT, "Normal distribution: a symmetrical bell curve with a line at its peak.",
      tags=["normal distribution", "bell curve", "gaussian", "mean", "statistics", "probability"])
def _(S):
    return [_baseline(), line("M2.5 17.5C7 17.5 8.5 5 12 5C15.5 5 17 17.5 21.5 17.5"), line(seg(12, 8.5, 12, 19.5))]


@icon("skewed-distribution", CAT, "Skewed distribution: a lopsided curve with its peak to the left and a long right tail.",
      tags=["skewed distribution", "skewness", "right skewed", "positive skew", "asymmetric", "statistics"])
def _(S):
    return [_baseline(), line("M2.5 17.5C5 17.5 5.5 5 8.5 5C12 5 13 15.5 21.5 17.5")]


@icon("bimodal-distribution", CAT, "Bimodal distribution: a curve with two humps separated by a dip.",
      tags=["bimodal", "two peaks", "double hump", "distribution", "modes", "statistics"])
def _(S):
    return [_baseline(), line("M2.5 17.5C5 17.5 5.5 6 8 6C10.5 6 10 12 12 12C14 12 13.5 5 16 5C18.5 5 19 17.5 21.5 17.5")]


@icon("standard-deviation", CAT, "Standard deviation: a bell curve divided into bands, with a sigma sign above.",
      tags=["standard deviation", "sigma", "variance", "spread", "bell curve", "statistics"])
def _(S):
    r = S.r * 0.3
    sigma = poly([(15.5, 2.5), (9, 2.5), (12.5, 5.5), (9, 8.5), (15.5, 8.5)], r=r)
    bell = "M2.5 19C6.5 19 8.5 11 12 11C15.5 11 17.5 19 21.5 19"
    return [line(seg(2, 21.5, 22, 21.5)), line(bell), line(sigma, stroke_miterlimit="10"),
            line(seg(8.5, 16.5, 8.5, 20)), line(seg(15.5, 16.5, 15.5, 20))]

