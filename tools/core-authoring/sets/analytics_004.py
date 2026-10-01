"""TypeIcon Core: analytics (batch 004).

Research, statistics and domain analytics symbols. Charts follow `sets/charts.py`: corner axes as an open
line, 2 px bars in Line/Rounded that become 4 px solid bars in Filled.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar, rotation, transform_path

CAT = "analytics"
AXES = [(3, 3), (3, 21), (21, 21)]


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def axes(S):
    return line(poly(AXES, r=S.r))


def block(x, y, w, h, rx=0.0):
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def scaled(d, s, ox=0.0, oy=0.0):
    """Region d scaled by s about the origin, then moved by (ox, oy)."""
    return path_to_d(transform_path(P(d), (s, 0, 0, s, ox, oy)))


def bars_filled(bars, extra=()):
    """Filled design: vertical 2 px bars (x, y0, y1) become 4 px solid bars; extra d-strings get a 2.5 px stroke."""
    def f():
        items = [P(rect(x - 2, min(y0, y1) - 1, 4, abs(y1 - y0) + 2, 0.75)) for x, y0, y1 in bars]
        items += [ST(d, 2.5) for d in extra]
        return U(*items)
    return f


def dashes(S, x0, y0, x1, y1, dash=2.0, gap=2.0):
    """A dashed straight line as separate short segments (Rounded shortens them so the round caps keep the gaps)."""
    n = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / n, (y1 - y0) / n
    k = 0.0 if S.name == "line" else min(1.0, dash / 2 - 0.05)
    out, t = [], 0.0
    while t + dash <= n + 1e-6:
        a, b = t + k, t + dash - k
        out.append(seg(x0 + ux * a, y0 + uy * a, x0 + ux * b, y0 + uy * b))
        t += dash + gap
    return out


def wave(x0, y0, half, amp, n, first_up=True):
    """Smooth sine-like wave from (x0, y0): n half periods of width `half` and height `amp`."""
    d = f"M{fmt(x0)} {fmt(y0)}"
    x = x0
    k = amp * 4 / 3
    for i in range(n):
        sgn = -1 if (i % 2 == 0) == first_up else 1
        d += (f"C{fmt(x + half * 0.35)} {fmt(y0 + sgn * k)} {fmt(x + half * 0.65)} {fmt(y0 + sgn * k)} "
              f"{fmt(x + half)} {fmt(y0)}")
        x += half
    return d


# ============================================================================ research and methods

@icon("focus-group", CAT, "Four people seated around a round table under a speech bubble",
      tags=["focus group", "research", "discussion", "panel", "interview", "qualitative"])
def _(S):
    bubble = poly([(8, 2.5), (16, 2.5), (16, 7), (13.5, 7), (12, 8.75), (10.5, 7), (8, 7)], closed=True, r=S.r * 0.5)
    return [shell(bubble), shell(circle(12, 16, 2.75)),
            dot(5.5, 12.5, 1.75), dot(18.5, 12.5, 1.75), dot(5.5, 19.5, 1.75), dot(18.5, 19.5, 1.75)]


@icon("data-profiling", CAT, "Table column with a small histogram above its header",
      tags=["data profiling", "column statistics", "data quality", "distribution", "dataset", "summary"])
def _(S):
    rx = L(S, 0, 0.75)
    return [block(7, 5, 2.75, 3, rx), block(10.63, 2.5, 2.75, 5.5, rx), block(14.25, 4, 2.75, 4, rx),
            shell(rect(7, 10, 10, 11.5, rr(S, 3))), detail(seg(7, 13.5, 17, 13.5)), detail(seg(7, 17.5, 17, 17.5))]


@icon("nomogram", CAT, "Three parallel scales crossed by one straight reading line",
      tags=["nomogram", "nomograph", "alignment chart", "scale", "calculation", "reading line"])
def _(S):
    parts = [line(seg(x, 3, x, 21)) for x in (4, 12, 20)]
    ticks = {4: (6, 11), 12: (5.5, 18.5), 20: (13.5, 18.5)}
    for x, ys in ticks.items():
        parts += [line(seg(x, y, x + 2.5, y)) for y in ys]
    parts.append(line(seg(2, 19, 22, 5)))
    return parts


_AB_BARS = [(10, 19, 14), (15, 19, 5), (19.5, 19, 10)]
_AB_LINES = [seg(4, 3, 4, 7.5), poly([(4, 13.5), (4, 21), (21, 21)]), seg(2, 9.25, 6, 7.25), seg(2, 13.75, 6, 11.75)]


@icon("axis-break", CAT, "Chart axis interrupted by two slanted marks that show a break in scale",
      tags=["axis break", "broken axis", "scale break", "truncated axis", "chart", "graph"],
      filled=bars_filled(_AB_BARS, _AB_LINES))
def _(S):
    return [line(seg(4, 3, 4, 7.5)), line(poly([(4, 13.5), (4, 21), (21, 21)], r=S.r)),
            line(seg(2, 9.25, 6, 7.25)), line(seg(2, 13.75, 6, 11.75)),
            *[line(seg(x, y0, x, y1)) for x, y0, y1 in _AB_BARS]]


def _bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


_CH_CURVE = [(6.5, 18), (10, 18), (11, 9.5), (20.5, 6.5)]
_CH = _bez(*_CH_CURVE, 0.45)


@icon("chart-crosshair", CAT, "Line chart with a crosshair meeting at one highlighted point",
      tags=["crosshair", "cursor", "data point", "hover", "readout", "tooltip"])
def _(S):
    cx, cy = _CH
    c = _CH_CURVE
    parts = [axes(S), line(f"M{fmt(c[0][0])} {fmt(c[0][1])}C{fmt(c[1][0])} {fmt(c[1][1])} {fmt(c[2][0])} {fmt(c[2][1])} {fmt(c[3][0])} {fmt(c[3][1])}"),
             dot(cx, cy, 2.5)]
    parts += [line(d) for d in dashes(S, cx, 3, cx, cy - 4.5)]
    parts += [line(d) for d in dashes(S, cx, cy + 4.5, cx, cy + 6.5)]
    parts += [line(d) for d in dashes(S, cx - 4.5, cy, cx - 6.5, cy)]
    parts += [line(d) for d in dashes(S, cx + 4.5, cy, 21, cy)]
    return parts


@icon("dimensionality-reduction", CAT, "Cube with an arrow leading to a flat square",
      tags=["dimensionality reduction", "pca", "projection", "3d to 2d", "embedding", "machine learning"])
def _(S):
    cube = [(2.5, 6), (6, 2.5), (13, 2.5), (13, 9.5), (9.5, 13), (2.5, 13)]
    return [shell(poly(cube, closed=True, r=S.r * 0.5)),
            detail(poly([(2.5, 6), (9.5, 6), (9.5, 13)])), detail(seg(9.5, 6, 13, 2.5)),
            line(poly([(15.5, 6), (18.5, 6), (18.5, 11)], r=S.r * 0.5)),
            line(poly([(16.5, 9), (18.5, 11), (20.5, 9)], r=S.r * 0.5)),
            shell(rect(14, 14, 7, 7, rr(S, 1.5)))]


@icon("seasonality", CAT, "Repeating wave over a baseline with dashed marks between cycles",
      tags=["seasonality", "seasonal pattern", "cycle", "periodic", "time series", "recurring"])
def _(S):
    parts = [line(wave(3, 8, 3, 3, 6)), line(seg(3, 21, 21, 21))]
    for x in (9, 15):
        parts += [line(d) for d in dashes(S, x, 13, x, 19)]
    return parts


@icon("change-point", CAT, "Line that steps from a low level to a higher one at a dashed marker",
      tags=["change point", "shift", "breakpoint", "regime change", "anomaly", "time series"])
def _(S):
    parts = [axes(S), line(seg(6, 16.5, 9.5, 16.5)), line(seg(14.5, 8, 20.5, 8))]
    parts += [line(d) for d in dashes(S, 12, 3.5, 12, 18)]
    return parts


def _cv(S):
    parts = []
    xs = [2.5 + i * 3.9 for i in range(5)]
    for row, y in enumerate((5, 12, 19)):
        for i, x in enumerate(xs):
            if i == row:
                parts.append(block(x, y - 2.5, 3.1, 5, L(S, 0, 1)))
            else:
                parts.append(line(seg(x + L(S, 0, 1), y, x + 3.1 - L(S, 0, 1), y)))
    return parts


@icon("cross-validation", CAT, "Three rows of five blocks with the held-out block moving one step each row",
      tags=["cross validation", "k-fold", "folds", "model validation", "machine learning", "resampling"])
def _(S):
    return _cv(S)


# ============================================================================ domain analytics

@icon("sports-analytics", CAT, "Ball beside three rising bars",
      tags=["sports analytics", "sports statistics", "match stats", "performance", "team", "scouting"])
def _(S):
    cx, cy, r = 6.75, 16, 4.75
    return [shell(circle(cx, cy, r)), detail(arc(cx - 6.25, cy, 4.5, -58, 58)), detail(arc(cx + 6.25, cy, 4.5, 122, 238)),
            line(seg(14.5, 21, 14.5, 16)), line(seg(18, 21, 18, 11.5)), line(seg(21.5, 21, 21.5, 7))]


@icon("retail-analytics", CAT, "Shopping bag with a bar chart on its front",
      tags=["retail analytics", "sales data", "shop metrics", "store performance", "ecommerce", "commerce"])
def _(S):
    return [shell(rect(4, 8, 16, 13, rr(S, 3))), line("M9 8V6.5A3 3 0 0 1 15 6.5V8"),
            detail(seg(8.5, 17.5, 8.5, 15)), detail(seg(12, 17.5, 12, 13)), detail(seg(15.5, 17.5, 15.5, 11.5))]


@icon("people-analytics", CAT, "Person beside a small pie chart",
      tags=["people analytics", "hr analytics", "workforce", "employee data", "demographics", "human resources"])
def _(S):
    return [shell(circle(6.5, 7, 3)),
            shell(f"M2 21V19A4.5 4.5 0 0 1 6.5 14.5A4.5 4.5 0 0 1 11 19V21Z" if S.name == "rounded"
                  else "M2 21V19A4.5 4.5 0 0 1 6.5 14.5A4.5 4.5 0 0 1 11 19V21Z"),
            shell(circle(17.5, 12, 3.75)), detail(poly([(17.5, 8.25), (17.5, 12), (21.25, 12)], r=S.r * 0.3))]


@icon("empathy-map", CAT, "Square split into four quadrants around a small head",
      tags=["empathy map", "user research", "persona", "ux", "says thinks does feels", "customer insight"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(circle(12, 12, 3.5)),
            detail(seg(12, 3, 12, 8.5)), detail(seg(12, 15.5, 12, 21)), detail(seg(3, 12, 8.5, 12)), detail(seg(15.5, 12, 21, 12))]


@icon("card-sorting", CAT, "Three columns of cards with one card moving between them",
      tags=["card sorting", "information architecture", "ux research", "categorise", "categorize", "grouping"])
def _(S):
    rx = L(S, 0, 0.75)
    parts = [line(seg(x0 + L(S, 0, 1), 3, x0 + 5 - L(S, 0, 1), 3)) for x0 in (2.5, 9.5, 16.5)]
    for x0, ys in ((2.5, (6.5, 11.5, 16.5)), (9.5, (6.5, 11.5)), (16.5, (6.5,))):
        parts += [block(x0, y, 5, 3, rx) for y in ys]
    card = path_to_d(transform_path(P(rect(15.5, 13.25, 5, 3, rx)), rotation(-18, 18, 14.75)))
    parts += [Part("dot", card), line(poly([(10.5, 18.5), (14, 18.5)], r=S.r)), line(poly([(12.5, 16.5), (14.5, 18.5), (12.5, 20.5)], r=S.r * 0.5))]
    return parts


# ============================================================================ gauges and radial charts

def soften(d, k):
    """Round the corners of region d by k px (shrink then grow with round joins)."""
    reg = P(d)
    inner = D(reg, ST(d, 2 * k, "round", "round"))
    di = path_to_d(inner)
    return path_to_d(U(inner, ST(di, 2 * k, "round", "round")))


@icon("data-usage", CAT, "Smartphone showing a ring gauge about two thirds full",
      tags=["data usage", "mobile data", "data plan", "usage meter", "bandwidth", "quota"])
def _(S):
    return [shell(rect(5.5, 2, 13, 20, rr(S, 3))), detail(arc(12, 10.5, 3.75, -90, 150)), detail(seg(10.5, 18.5, 13.5, 18.5))]


def _sector_d(cx, cy, r0, r1, a0, a1, n=10):
    pts = [polar(cx, cy, r1, a0 + (a1 - a0) * i / n) for i in range(n + 1)]
    pts += [polar(cx, cy, r0, a1 + (a0 - a1) * i / n) for i in range(n + 1)]
    return poly(pts, closed=True)


@icon("radial-heatmap", CAT, "Circle split into rings and sectors with a few cells shaded",
      tags=["radial heatmap", "circular heatmap", "polar heatmap", "calendar heatmap", "rings", "density"])
def _(S):
    parts = [shell(circle(12, 12, 9)), detail(circle(12, 12, 4.5))]
    parts += [detail(seg(*polar(12, 12, 4.5, a), *polar(12, 12, 9, a))) for a in (-90, -30, 30, 90, 150, 210)]
    cells = [_sector_d(12, 12, 5.5, 8, -84, -36), _sector_d(12, 12, 5.5, 8, 96, 144)]
    parts += [Part("dot", c if S.name == "line" else soften(c, 1.0)) for c in cells]
    parts.append(block(10.5, 10.5, 3, 3) if S.name == "line" else dot(12, 12, 1.6))
    return parts


def _liquid(S):
    region = wave(2.5, 11.5, 3.2, 0.9, 6) + "L22 22L2 22Z"
    d = path_to_d(I(P(circle(12, 12, 6.5)), P(region)))
    return d if S.name == "line" else soften(d, 0.9)


@icon("liquid-fill-gauge", CAT, "Circle half filled with liquid under a wavy surface",
      tags=["liquid gauge", "fill level", "progress", "percentage", "tank level", "water level"])
def _(S):
    return [shell(circle(12, 12, 9)), Part("dot", _liquid(S))]


_FB = [(8, 9.5, 16), (13, 5, 12), (18, 10, 17.5)]


@icon("chart-floating-bar", CAT, "Bars floating above the axis, each spanning a low to high range",
      tags=["floating bar", "range bar", "range chart", "min max", "span", "interval"],
      filled=bars_filled(_FB, [poly(AXES)]))
def _(S):
    return [axes(S), *[line(seg(x, y0, x, y1)) for x, y0, y1 in _FB]]


# ============================================================================ tables and mapping

@icon("field-mapping", CAT, "Two narrow tables with lines linking rows across them",
      tags=["field mapping", "data mapping", "schema mapping", "column mapping", "etl", "integration"])
def _(S):
    parts = []
    for x in (2.5, 16.5):
        parts += [shell(rect(x, 3, 5, 18, rr(S, 2))), detail(seg(x, 9, x + 5, 9)), detail(seg(x, 15, x + 5, 15))]
    parts += [line(seg(9.5, 6, 14.5, 12)), line(seg(9.5, 12, 14.5, 6)), line(seg(9.5, 18, 14.5, 18))]
    return parts


@icon("market-basket-analysis", CAT, "Shopping basket under three linked item dots",
      tags=["market basket analysis", "association rules", "affinity analysis", "cross sell", "bought together", "retail"])
def _(S):
    tri = [(5.5, 8.25), (12, 3.25), (18.5, 8.25)]
    return [shell(poly([(3.5, 13), (20.5, 13), (18.5, 21), (5.5, 21)], closed=True, r=S.r)),
            detail(seg(9.5, 15.5, 9.5, 18.5)), detail(seg(14.5, 15.5, 14.5, 18.5)),
            line(poly(tri, closed=True, r=S.r)), *[dot(x, y, 1.9) for x, y in tri]]


@icon("frequency-table", CAT, "Two column table whose right column holds tally marks",
      tags=["frequency table", "tally", "tally chart", "count", "statistics", "frequency"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(seg(9, 3, 9, 21)), detail(seg(3, 12, 21, 12)),
            dot(6, 7.5, 1.25), dot(6, 16.5, 1.25),
            detail(seg(12.5, 5.5, 12.5, 9.5)), detail(seg(15.5, 5.5, 15.5, 9.5)), detail(seg(18.5, 5.5, 18.5, 9.5)),
            detail(seg(12.5, 14.5, 12.5, 18.5)), detail(seg(15.5, 14.5, 15.5, 18.5))]


@icon("probability-spinner", CAT, "Circle in four sectors with a centre pin and pointer",
      tags=["spinner", "probability", "chance", "random", "game spinner", "outcome"])
def _(S):
    tip = polar(12, 12, 6.75, -45)
    a, b = polar(tip[0], tip[1], 3, 135 - 42), polar(tip[0], tip[1], 3, 135 + 42)
    parts = [shell(circle(12, 12, 9))]
    parts += [detail(seg(*polar(12, 12, 3.5, ang), *polar(12, 12, 9, ang))) for ang in (-90, 0, 90, 180)]
    cells = [_sector_d(12, 12, 4.25, 7, 9, 81), _sector_d(12, 12, 4.25, 7, 189, 261)]
    parts += [Part("dot", c if S.name == "line" else soften(c, 0.8)) for c in cells]
    parts += [detail(seg(12, 12, *tip)), detail(poly([a, tip, b], r=S.r * 0.3)), dot(12, 12, 1.75)]
    return parts


# ============================================================================ plots

_BG = [(8, 4.5, 1), (13.5, 4.5, 2), (19, 4.5, 1.25),
       (8, 10, 2.25), (13.5, 10, 1.25), (19, 10, 1.75),
       (8, 15.5, 1.5), (13.5, 15.5, 2.25), (19, 15.5, 1)]


@icon("bubble-grid-chart", CAT, "Grid of circles in rows and columns, sized by value",
      tags=["bubble grid", "punch card chart", "matrix bubble chart", "dot matrix", "comparison", "table chart"])
def _(S):
    return [axes(S), *[dot(x, y, r) for x, y, r in _BG]]


@icon("sparkline-table", CAT, "Three table rows, each ending in a tiny line graph",
      tags=["sparkline", "sparklines", "table", "mini chart", "trend", "dashboard"])
def _(S):
    parts = []
    for y, zz in ((5, (1, -1.5, 0.5, -0.5, -2)), (12, (-1, 1, -1.5, 1.5, 0)), (19, (1.5, 0, 1, -1, -1.5))):
        parts.append(line(seg(3, y, 8, y)))
        xs = (11.5, 14, 16.5, 18.75, 21)
        parts.append(line(poly([(x, y + dz) for x, dz in zip(xs, zz)], r=S.r * 0.5)))
    return parts


@icon("diminishing-returns", CAT, "Axes with a curve that rises steeply and then levels off",
      tags=["diminishing returns", "saturation curve", "plateau", "law of diminishing returns", "economics", "concave"])
def _(S):
    return [axes(S), line("M6.5 18C8 10 11.5 6.5 20.5 6.5")]


# ============================================================================ sport

@icon("shot-chart", CAT, "Half court with the hoop, the three point arc and scattered shot marks",
      tags=["shot chart", "basketball", "shooting", "court map", "sports analytics", "makes and misses"])
def _(S):
    x = [detail(seg(9.25, 14.25, 12.75, 17.75)), detail(seg(9.25, 17.75, 12.75, 14.25))]
    return [shell(rect(3, 3, 18, 18, rr(S, 2))), detail("M7 3V6.5A5 5 0 0 0 17 6.5V3"), dot(12, 5.75, 1.4),
            dot(6.5, 17.5, 1.5), dot(17, 15, 1.5), dot(6.75, 12.5, 1.25), *x]


# ============================================================================ domain analytics (continued)

_TA_BARS = [(15.25, 21, 16), (18.5, 21, 12), (21.75, 21, 8)]


@icon("text-analytics", CAT, "Document with lines of text beside a small bar chart",
      tags=["text analytics", "text mining", "nlp", "document analysis", "sentiment analysis", "word frequency"])
def _(S):
    page = [(3, 3), (9, 3), (12.5, 6.5), (12.5, 21), (3, 21)]
    return [shell(poly(page, closed=True, r=S.r)), detail(poly([(9, 3), (9, 6.5), (12.5, 6.5)], r=S.r * 0.5)),
            detail(seg(5.5, 10.5, 10, 10.5)), detail(seg(5.5, 14, 10, 14)), detail(seg(5.5, 17.5, 8, 17.5)),
            *[line(seg(x, y0, x, y1)) for x, y0, y1 in _TA_BARS]]


_HANDSET_R = ("M5.2 3.5H8.6L10.4 8L8.1 9.5A11 11 0 0 0 14.5 15.9L16 13.6L20.5 15.4V18.8"
              "A1.7 1.7 0 0 1 18.8 20.5A15.5 15.5 0 0 1 3.5 5.2A1.7 1.7 0 0 1 5.2 3.5Z")
_HANDSET_L = "M3.5 3.5H8.6L10.4 8L8.1 9.5A11 11 0 0 0 14.5 15.9L16 13.6L20.5 15.4V20.5H19A15.5 15.5 0 0 1 3.5 5Z"


@icon("call-analytics", CAT, "Telephone handset beside three rising bars",
      tags=["call analytics", "call tracking", "call center metrics", "phone statistics", "call volume", "contact center"])
def _(S):
    s = 0.62
    d = _HANDSET_L if S.name == "line" else _HANDSET_R
    hs = scaled(d, s, 3 * (1 - s), 21 * (1 - s))
    return [shell(hs), line(seg(14.5, 13, 14.5, 9.5)), line(seg(18, 13, 18, 6)), line(seg(21.5, 13, 21.5, 2.5))]


@icon("data-product", CAT, "Open box with a bar chart rising out of it",
      tags=["data product", "data as a product", "dataset package", "analytics product", "data delivery", "data mesh"])
def _(S):
    lo, hi = L(S, 8.5, 7.5), L(S, 0, 1)
    return [shell(rect(5, 11, 14, 10, rr(S, 2))), line(seg(5, 11, 2.5, 7.5)), line(seg(19, 11, 21.5, 7.5)),
            line(seg(8.5, lo, 8.5, 6.5 + hi)), line(seg(12, lo, 12, 4.5 + hi)), line(seg(15.5, lo, 15.5, 2.5 + hi))]


# ============================================================================ statistical plots

@icon("marginal-histogram", CAT, "Scatter plot with small histograms along its top and right edges",
      tags=["marginal histogram", "joint plot", "scatter histogram", "distribution", "statistics", "marginal plot"])
def _(S):
    return [line(poly([(3, 9), (3, 21), (15, 21)], r=S.r)),
            dot(7, 17, 1.4), dot(9.5, 12.5, 1.4), dot(12.5, 16, 1.4),
            line(seg(6.5, 6.5, 6.5, 4.5)), line(seg(10, 6.5, 10, 2.5)), line(seg(13.5, 6.5, 13.5, 4)),
            line(seg(17.5, 11, 20, 11)), line(seg(17.5, 14.5, 21.5, 14.5)), line(seg(17.5, 18, 19.5, 18))]
