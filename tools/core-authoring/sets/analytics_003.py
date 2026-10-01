"""TypeIcon Core: analytics (batch analytics_003).

Charts, spreadsheet tools and data-flow ideas drawn on the Core grid. Chart icons share the corner axis
used in `charts.py`; database cylinders, tables and map outlines use the small local helpers below.
"""
import math

from dsl import D, I, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "analytics"
AXES = [(3, 3), (3, 21), (21, 21)]


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def axes(S):
    return line(poly(AXES, r=S.r))


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def thick(d, w, S):
    """Solid outline of a stroke of width w along d."""
    return path_to_d(ST(d, w, S.cap, S.join))


def gear_pts(cx, cy, r0, r1, n, phase=0.0):
    a_base, a_tip = 360 / n * 0.3, 360 / n * 0.18
    pts = []
    for i in range(n):
        th = phase + i * 360 / n
        pts += [polar(cx, cy, r0, th - a_base), polar(cx, cy, r1, th - a_tip),
                polar(cx, cy, r1, th + a_tip), polar(cx, cy, r0, th + a_base)]
    return pts


def cyl(cx, top, bot, rx, ry=2.0):
    """Database cylinder silhouette."""
    return (f"M{fmt(cx - rx)} {fmt(top)}A{fmt(rx)} {fmt(ry)} 0 0 1 {fmt(cx + rx)} {fmt(top)}V{fmt(bot)}"
            f"A{fmt(rx)} {fmt(ry)} 0 0 1 {fmt(cx - rx)} {fmt(bot)}Z")


def cyl_band(cx, y, rx, ry=2.0):
    """Front curve of a cylinder ring at height y."""
    return f"M{fmt(cx - rx)} {fmt(y)}A{fmt(rx)} {fmt(ry)} 0 0 0 {fmt(cx + rx)} {fmt(y)}"


def database(cx, top, bot, rx, ry=2.0, bands=1):
    parts = [shell(cyl(cx, top, bot, rx, ry)), detail(cyl_band(cx, top, rx, ry))]
    for i in range(bands):
        parts.append(detail(cyl_band(cx, top + (bot - top) * (i + 1) / (bands + 1), rx, ry)))
    return parts


def wave(x0, x1, y, amp, n=2):
    """Smooth sine-like wave from x0 to x1 made of cubic curves, n full periods."""
    w = (x1 - x0) / (n * 2)
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n * 2):
        a = x0 + i * w
        s = -1 if i % 2 == 0 else 1
        d += f"C{fmt(a + w * 0.36)} {fmt(y + s * amp * 1.33)} {fmt(a + w * 0.64)} {fmt(y + s * amp * 1.33)} {fmt(a + w)} {fmt(y)}"
    return d


# ============================================================================ chunk 1

@icon("stream-processing", CAT, "Gear above a flowing wave with an arrow; continuous processing of a data stream",
      tags=["stream processing", "data stream", "real time", "pipeline", "event stream", "processing"])
def _(S):
    g = poly(gear_pts(12, 8.5, 4.75, 6.5, 8, phase=22.5), closed=True, r=S.r * 0.4)
    return [shell(g), detail(circle(12, 8.5, 2)),
            line(wave(3, 18.5, 19, 1.5, n=2)), line(poly([(16.5, 16), (19.5, 19), (16.5, 22)], r=S.r * 0.5))]


@icon("data-connector", CAT, "Database cylinder with a cable running to a two-pin plug",
      tags=["data connector", "database connection", "integration", "plug", "connect", "source"])
def _(S):
    return [*database(8, 4, 20, 5.5, 2), line(seg(13.5, 12, 15.5, 12)),
            shell(rect(15.5, 8.5, 3.5, 7, L(S, 0.5, 1.5))), line(seg(19, 10.5, 21.5, 10.5)), line(seg(19, 13.5, 21.5, 13.5))]


@icon("linear-gauge", CAT, "Horizontal scale with tick marks and a pointer above one position",
      tags=["linear gauge", "bullet gauge", "scale", "meter", "level", "indicator"])
def _(S):
    return [shell(rect(3, 12.5, 18, 7, L(S, 0.5, 2))),
            *[detail(seg(x, 12.5, x, 16)) for x in (7.5, 12, 16.5)],
            shell(poly([(12.5, 4), (17.5, 4), (15, 8)], closed=True, r=S.r * 0.4))]


def _ring_arc():
    return arc(12, 12, 8.5, -90, 180)


@icon("progress-ring", CAT, "Thick ring three quarters complete with a percent sign in the middle",
      tags=["progress ring", "progress circle", "percent complete", "completion", "radial progress", "loading"])
def _(S):
    track = arc(12, 12, 8.5, 180, 270)
    pct = [line(seg(14.5, 9, 9.5, 15)), dot(9.75, 9.75, 1.4), dot(14.25, 14.25, 1.4)]
    return [solid(thick(_ring_arc(), 3.5, S)), line(track), *pct]


@icon("survival-curve", CAT, "Descending staircase curve on a corner axis with small tick marks on some steps",
      tags=["survival curve", "kaplan meier", "survival analysis", "retention curve", "step chart", "statistics"])
def _(S):
    steps = [(6.5, 5.5), (9.5, 5.5), (9.5, 9.5), (13, 9.5), (13, 13), (16, 13), (16, 16.5), (20, 16.5)]
    return [axes(S), line(poly(steps, r=S.r * 0.5)), line(seg(11.25, 7.75, 11.25, 11.25)), line(seg(18, 14.75, 18, 18.25))]


@icon("pert-chart", CAT, "Network of event circles joined by arrows that split into two paths and rejoin",
      tags=["pert chart", "project network", "critical path", "dependencies", "schedule", "project planning"])
def _(S):
    nodes = [(4, 12), (12, 4.5), (12, 19.5), (20, 12)]
    parts = [shell(circle(x, y, 2.25)) for x, y in nodes]
    for (x0, y0), (x1, y1) in ((nodes[0], nodes[1]), (nodes[0], nodes[2]), (nodes[1], nodes[3]), (nodes[2], nodes[3])):
        a = math.atan2(y1 - y0, x1 - x0)
        ux, uy = math.cos(a), math.sin(a)
        nx, ny = -uy, ux
        sx, sy = x0 + 3.5 * ux, y0 + 3.5 * uy
        tx, ty = x1 - 3.5 * ux, y1 - 3.5 * uy
        bx, by = tx - 3 * ux, ty - 3 * uy
        parts.append(line(seg(sx, sy, bx + 0.5 * ux, by + 0.5 * uy)))
        tri = [(tx, ty), (bx + nx * 1.9, by + ny * 1.9), (bx - nx * 1.9, by - ny * 1.9)]
        parts.append(solid(poly(tri, closed=True, r=S.r * 0.2)))
    return parts


@icon("galton-board", CAT, "Triangle of pegs above a row of bins holding balls, most in the middle",
      tags=["galton board", "bean machine", "normal distribution", "probability", "quincunx", "statistics"])
def _(S):
    pegs = [(12, 3.5), (9, 6.5), (15, 6.5), (6, 9.5), (12, 9.5), (18, 9.5)]
    return [*[dot(x, y, 1.1) for x, y in pegs],
            line(poly([(3, 13), (3, 21), (21, 21), (21, 13)], r=S.r)), line(seg(9, 15.5, 9, 21)), line(seg(15, 15.5, 15, 21)),
            dot(6, 18.25, 1.5), dot(12, 18.25, 1.5), dot(12, 14.25, 1.5), dot(18, 18.25, 1.5)]


@icon("active-users", CAT, "Two person busts above a pulse line; users active right now",
      tags=["active users", "live users", "online users", "daily active users", "concurrent users", "audience"])
def _(S):
    def bust(cx):
        return [shell(circle(cx, 5.25, 2.25)), shell(f"M{fmt(cx - 3.5)} 12.5A3.5 3.5 0 0 1 {fmt(cx + 3.5)} 12.5Z")]
    pulse = [(2.5, 18.5), (8, 18.5), (10, 15.5), (13, 21), (15, 18.5), (21.5, 18.5)]
    return [*bust(7), *bust(17), line(poly(pulse, r=S.r * 0.5))]


@icon("device-breakdown", CAT, "Desktop monitor and phone each above a bar of different height",
      tags=["device breakdown", "device share", "desktop vs mobile", "platform split", "device analytics", "traffic"])
def _(S):
    R = L(S, 0.5, 1.5)
    return [shell(rect(2.5, 3, 10.5, 7, R)), line(seg(5.5, 12.5, 10, 12.5)), line(seg(7.75, 10, 7.75, 12.5)),
            shell(rect(16.5, 3, 5, 9.5, R)),
            shell(rect(5.5, 15.5, 4.5, 6, L(S, 0.5, 1))), shell(rect(16.75, 18.5, 4.5, 3, L(S, 0.5, 1)))]


@icon("attribution-model", CAT, "Three touchpoint dots with lines of different weight converging on a target",
      tags=["attribution model", "marketing attribution", "touchpoints", "multi touch", "conversion credit", "channels"])
def _(S):
    cx, cy = 16.5, 12
    parts = [shell(circle(cx, cy, 5)), detail(circle(cx, cy, 2))]
    for (x, y), w in (((3.5, 4.5), 1.25), ((3.5, 12), 2.5), ((3.5, 19.5), 1.75)):
        parts.append(dot(x, y, 1.5))
        a = math.atan2(cy - y, cx - x)
        ex, ey = cx - 6.25 * math.cos(a), cy - 6.25 * math.sin(a)
        sx, sy = x + 2.25 * math.cos(a), y + 2.25 * math.sin(a)
        parts.append(solid(thick(seg(sx, sy, ex, ey), w, S)))
    return parts


@icon("share-of-voice", CAT, "Megaphone with a small pie chart in front of its mouth",
      tags=["share of voice", "brand mentions", "market share", "media share", "pr", "marketing"])
def _(S):
    cone = [(5.5, 9.5), (11.5, 5.5), (11.5, 18.5), (5.5, 14.5)]
    return [shell(rect(2.5, 9.5, 3, 5, L(S, 0.5, 1))), shell(poly(cone, closed=True, r=S.r * 0.5)),
            line(poly([(6.5, 15.5), (6.5, 19), (8.5, 19)], r=S.r * 0.5)),
            shell(circle(18, 12, 3.75)), Part("dot", "M18 12V8.25A3.75 3.75 0 0 1 21.75 12Z")]


@icon("gaze-plot", CAT, "Web page with a path of fixation circles of different sizes joined by lines",
      tags=["gaze plot", "eye tracking", "scan path", "fixations", "usability", "ux research"])
def _(S):
    return [shell(rect(2.5, 3, 19, 18, S.R)), detail(seg(2.5, 7.5, 21.5, 7.5)),
            detail(circle(7.5, 13, 2)), detail(circle(16, 12.5, 1.5)), detail(circle(11.5, 17, 1.25)),
            detail(poly([(9.5, 13), (14.5, 12.5)], r=0)), detail(seg(15, 13.75, 12.5, 16))]


@icon("query-builder", CAT, "Database cylinder beside three stacked condition blocks joined by a bracket",
      tags=["query builder", "filter builder", "conditions", "sql", "visual query", "rules"])
def _(S):
    R = L(S, 0.5, 1.5)
    return [*database(6.5, 5, 19, 4, 1.75),
            shell(rect(15, 3, 6.5, 3.5, R)), shell(rect(15, 10.25, 6.5, 3.5, R)), shell(rect(15, 17.5, 6.5, 3.5, R)),
            line(poly([(15, 4.75), (12.5, 4.75), (12.5, 19.25), (15, 19.25)], r=S.r * 0.5)), line(seg(12.5, 12, 15, 12))]


@icon("segmented-bar", CAT, "Long rounded bar divided into four segments of different widths",
      tags=["segmented bar", "stacked bar", "proportion", "breakdown", "composition", "percent split"])
def _(S):
    return [shell(rect(2.5, 8, 19, 8, L(S, 1, 4))),
            *[detail(seg(x, 8, x, 16)) for x in (9, 13, 18)]]


@icon("market-depth-chart", CAT, "Two stepped areas meeting in the middle, bids rising to the left and asks to the right",
      tags=["market depth", "depth chart", "order book", "bid ask", "trading", "liquidity"])
def _(S):
    k = S.r * 0.4
    bids = [(3, 21), (3, 5), (5.5, 5), (5.5, 9.5), (8, 9.5), (8, 14), (10.5, 14), (10.5, 21)]
    asks = [(13.5, 21), (13.5, 16), (16, 16), (16, 11), (18.5, 11), (18.5, 7), (21, 7), (21, 21)]
    return [shell(poly(bids, closed=True, r=k)), shell(poly(asks, closed=True, r=k))]


# ============================================================================ chunk 2

@icon("upset-plot", CAT, "Bars above a matrix of dots where joined dots show which sets overlap",
      tags=["upset plot", "set intersections", "venn alternative", "overlap", "sets", "statistics"])
def _(S):
    cols = (5, 12, 19)
    parts = [line(seg(5, 10, 5, 3)), line(seg(12, 10, 12, 5.5)), line(seg(19, 10, 19, 8))]
    rows = (13.5, 17, 20.5)
    on = {5: (0, 1), 12: (1, 2), 19: (0, 1, 2)}
    for x in cols:
        idx = on[x]
        for i, y in enumerate(rows):
            parts.append(dot(x, y, 1.5) if i in idx else dot(x, y, 0.75))
        parts.append(line(seg(x, rows[idx[0]], x, rows[idx[-1]])))
    return parts


@icon("significance-bars", CAT, "Two bars of different height joined above by a bracket with an asterisk",
      tags=["statistical significance", "p value", "significant difference", "t test", "comparison", "bar chart"])
def _(S):
    R = L(S, 0.5, 1.5)
    c, r = (12, 4.25), 2.5
    star = [seg(*polar(*c, r, a), *polar(*c, r, a + 180)) for a in (-90, -30, 30)]
    return [shell(rect(4, 13, 5, 8, R)), shell(rect(15, 16.5, 5, 4.5, R)),
            line(poly([(6.5, 11), (6.5, 9), (17.5, 9), (17.5, 14)], r=S.r * 0.5)), *[line(d) for d in star]]


@icon("data-bottleneck", CAT, "Wide pipe narrowing into a thin neck with dots crowding at the narrow point",
      tags=["bottleneck", "data bottleneck", "throughput", "congestion", "constraint", "performance"])
def _(S):
    k = S.r * 0.6
    return [line(poly([(2.5, 5), (9, 5), (14, 9.5), (21.5, 9.5)], r=k)), line(poly([(2.5, 19), (9, 19), (14, 14.5), (21.5, 14.5)], r=k)),
            dot(5, 9, 1.5), dot(5, 15, 1.5), dot(8.5, 12, 1.5), dot(12, 12, 1.5), dot(18.5, 12, 1.25)]


@icon("chart-connected-scatter", CAT, "Dots on a corner axis joined in time order by a line that loops back on itself",
      tags=["connected scatter plot", "trajectory", "time path", "scatter", "sequence", "xy chart"])
def _(S):
    pts = [(7, 17), (10.5, 8), (17.5, 7.5), (17, 15), (8.5, 12)]
    return [axes(S), line(poly(pts, r=S.r * 0.5)), *[dot(x, y, 1.75) for x, y in pts]]


@icon("chart-scatter-3d", CAT, "Three axes meeting at a corner with dots floating in the space between them",
      tags=["3d scatter plot", "three dimensional", "xyz", "scatter", "point cloud", "chart"])
def _(S):
    o = (9, 14.5)
    parts = [line(poly([(9, 2.5), o, (21.5, 19.5)], r=S.r * 0.5)), line(seg(*o, 2.5, 20.5))]
    return parts + [dot(x, y, 1.6) for x, y in ((13.5, 7.5), (18, 12), (5, 11), (13.5, 13))]


@icon("chart-win-loss", CAT, "Row of equal bars along a centre line, some above it and some below",
      tags=["win loss chart", "sparkline", "binary chart", "wins and losses", "results", "streak"])
def _(S):
    ups = {4: True, 8: True, 12: False, 16: True, 20: False}
    parts = [line(seg(2.5, 12, 21.5, 12))]
    for x, up in ups.items():
        parts.append(line(seg(x, 3.5, x, 9.5) if up else seg(x, 14.5, x, 20.5)))
    return parts


def clip_sq(S, x, y, w, h, frame=(3, 3, 18, 18)) -> Part:
    """Solid mark clipped to the inside of a rounded frame (knocked out of the Filled frame)."""
    fx, fy, fw, fh = frame
    inner = P(rect(fx + 1, fy + 1, fw - 2, fh - 2, max(0.0, S.R - 1)))
    return Part("dot", path_to_d(I(P(rect(x, y, w, h)), inner)))


@icon("warming-stripes", CAT, "Square filled with vertical stripes that get wider and darker toward the right",
      tags=["warming stripes", "climate stripes", "temperature change", "global warming", "climate", "heat"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), clip_sq(S, 7.5, 3, 2, 18), clip_sq(S, 11.5, 3, 3, 18), clip_sq(S, 16.5, 3, 5, 18)]


@icon("flatten-the-curve", CAT, "Tall narrow peak and a low wide curve under a dashed capacity line",
      tags=["flatten the curve", "epidemic curve", "capacity", "peak", "outbreak", "public health"])
def _(S):
    tall = "M3 20C5.5 20 6 4.5 8.5 4.5C11 4.5 11.5 20 14 20"
    low = "M5 20C9 20 10.5 15 14 15C17.5 15 19 20 21.5 20"
    dashes = [seg(x, 11, x + 2.5, 11) for x in (2.5, 12.5, 17, 20)]
    base = line(seg(2.5, 20, 21.5, 20))
    return [line(tall), line(low), base, line(seg(12.5, 11, 15, 11)), line(seg(17, 11, 19.5, 11)), line(seg(2.5, 11, 4, 11))]


def _grid(S, xs=(9, 15), ys=(9, 15)):
    return [shell(rect(3, 3, 18, 18, S.R)), *[detail(seg(x, 3, x, 21)) for x in xs], *[detail(seg(3, y, 21, y)) for y in ys]]


@icon("cell-note", CAT, "Spreadsheet grid with a small filled triangle in the top corner of one cell",
      tags=["cell note", "cell comment", "spreadsheet", "annotation", "note", "comment indicator"])
def _(S):
    return [*_grid(S), Part("dot", poly([(16.5, 4), (20, 4), (20, 7.5)], closed=True, r=0))]


@icon("banded-rows", CAT, "Table with every other row shaded solid",
      tags=["banded rows", "zebra stripes", "alternating rows", "table style", "striped table", "rows"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), clip_sq(S, 3, 7.5, 18, 4.5), clip_sq(S, 3, 16.5, 18, 5),
            detail(seg(9, 3, 9, 7.5)), detail(seg(9, 12, 9, 16.5))]


@icon("table-totals", CAT, "Table with a heavy rule above the bottom row and a sigma sign in that row",
      tags=["totals row", "table total", "sum", "subtotal", "spreadsheet", "summary row"])
def _(S):
    sigma = [(11, 15.5), (5.5, 15.5), (8.5, 17.75), (5.5, 20), (11, 20)]
    return [shell(rect(3, 2.5, 18, 19, S.R)), detail(seg(3, 7, 21, 7)), detail(seg(12, 2.5, 12, 10.5)),
            clip_sq(S, 3, 10.5, 18, 3, (3, 2.5, 18, 19)), detail(poly(sigma, r=S.r * 0.3)), detail(seg(14, 17.75, 18, 17.75))]


def _map_outline(S):
    return poly([(3, 5), (9, 3), (15, 5), (21, 3), (21, 19), (15, 21), (9, 19), (3, 21)], closed=True, r=S.r * 0.5)


@icon("geo-heatmap", CAT, "Folded map with a blotch of concentric rings over one region",
      tags=["geographic heat map", "heatmap", "density map", "hotspot", "location data", "map"])
def _(S):
    return [shell(_map_outline(S)), detail(circle(12, 12, 4)), dot(12, 12, 1.75),
            detail(seg(9, 3, 9, 7.5)), detail(seg(15, 16.5, 15, 21))]


@icon("gis-layers", CAT, "Three stacked map planes, the top one showing a location dot and a road",
      tags=["gis", "map layers", "geographic information system", "overlay", "spatial data", "layers"])
def _(S):
    k = S.r * 0.5
    top = [(12, 2.5), (21.5, 7.5), (12, 12.5), (2.5, 7.5)]
    return [shell(poly(top, closed=True, r=k)), detail(seg(8, 7.5, 12, 10)), dot(14, 6.5, 1.5),
            line(poly([(2.5, 12), (12, 17), (21.5, 12)], r=k)), line(poly([(2.5, 16.5), (12, 21.5), (21.5, 16.5)], r=k))]


# ============================================================================ chunk 3

@icon("floor-heatmap", CAT, "Floor plan of two rooms with heat blotches showing where people gather",
      tags=["floor heat map", "floor plan", "occupancy", "space utilisation", "indoor analytics", "hotspot"])
def _(S):
    return [shell(rect(2.5, 3, 19, 18, S.R)), detail(seg(10, 3, 10, 10.5)), detail(seg(10, 15, 10, 21)), detail(seg(2.5, 13, 6.5, 13)),
            detail(circle(15.75, 12, 3.25)), dot(15.75, 12, 1.5), dot(6.25, 8, 2)]


def _foot(cx, cy):
    return [shell(ellipse(cx, cy, 2.25, 3.5)), shell(ellipse(cx, cy + 6, 1.75, 1.75))]


@icon("foot-traffic", CAT, "Two shoe prints walking beside two bars of a visitor count",
      tags=["foot traffic", "footfall", "visitor count", "people counting", "store visits", "retail analytics"])
def _(S):
    def foot(cx, cy):
        return [shell(ellipse(cx, cy, 2.5, 3.75)), shell(rect(cx - 2, cy + 5.5, 4, 3, L(S, 0.5, 1.5)))]
    return [*foot(5, 6.25), *foot(11.5, 10.75), line(seg(16.5, 21, 16.5, 14)), line(seg(20.5, 21, 20.5, 8))]


@icon("spike-map", CAT, "Flat map with narrow spikes of different heights rising from several points",
      tags=["spike map", "map chart", "geographic data", "density", "values by location", "thematic map"])
def _(S):
    k = S.r * 0.5
    ground = poly([(2.5, 15), (8, 13), (16, 15), (21.5, 13), (21.5, 19.5), (16, 21.5), (8, 19.5), (2.5, 21.5)], closed=True, r=k)
    spikes = [(6.5, 17.5, 8), (12, 17, 3), (17.5, 18, 9.5)]
    return [shell(ground), *[solid(poly([(x - 1.75, y), (x, top), (x + 1.75, y)], closed=True, r=S.r * 0.2)) for x, y, top in spikes]]


@icon("principal-components", CAT, "Tilted oval cloud of dots crossed by a long axis arrow and a shorter one at right angles",
      tags=["principal component analysis", "pca", "dimensionality reduction", "eigenvectors", "variance", "statistics"])
def _(S):
    k = S.r * 0.4
    cloud = ((4.5, 19.5), (5, 14.5), (9, 19.5), (10, 9), (19, 13.5))
    return [line(seg(10, 14, 19, 5)), line(poly([(14.5, 5), (19, 5), (19, 9.5)], r=k)),
            line(seg(10, 14, 15, 19)), line(poly([(15, 14.5), (15, 19), (10.5, 19)], r=k)),
            dot(10, 14, 2), *[dot(x, y, 1.4) for x, y in cloud]]


@icon("rage-click", CAT, "Cursor arrow with jagged burst lines around its tip from repeated angry clicks",
      tags=["rage click", "frustration", "repeated clicks", "ux issue", "session replay", "user frustration"])
def _(S):
    cur = [(10.5, 10.5), (20.5, 14.5), (16, 16), (14.5, 20.5)]
    bursts = [((3, 10.5), (6.5, 10.5)), ((10.5, 3), (10.5, 6.5)), ((4.5, 4.5), (7, 7)), ((3.5, 16.5), (6.5, 14)), ((16.5, 3.5), (14, 6.5))]
    return [shell(poly(cur, closed=True, r=S.r * 0.4)), *[line(seg(*a, *b)) for a, b in bursts]]


@icon("form-analytics", CAT, "Form with three input fields, each followed by a bar of different length",
      tags=["form analytics", "field completion", "form drop off", "conversion", "input fields", "ux"])
def _(S):
    R = L(S, 0.5, 1.5)
    return [*[shell(rect(2.5, y, 10, 4, R)) for y in (3.5, 10, 16.5)],
            line(seg(16, 5.5, 21.5, 5.5)), line(seg(16, 12, 19.5, 12)), line(seg(16, 18.5, 17.5, 18.5))]


@icon("email-analytics", CAT, "Envelope with a small bar chart rising out of the top",
      tags=["email analytics", "open rate", "click rate", "campaign report", "newsletter stats", "email marketing"])
def _(S):
    return [shell(rect(2.5, 10.5, 19, 10.5, L(S, 1, 3))), detail(poly([(2.5, 11), (12, 16.5), (21.5, 11)], r=S.r * 0.5)),
            line(seg(8, 8.5, 8, 5)), line(seg(12, 8.5, 12, 2.5)), line(seg(16, 8.5, 16, 6))]


@icon("video-analytics", CAT, "Video frame with a play button and a declining line along the bottom",
      tags=["video analytics", "audience retention", "watch time", "drop off", "viewer stats", "video"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 17, S.R)), detail(poly([(10, 6.5), (15, 9.75), (10, 13)], closed=True, r=S.r * 0.4)),
            detail(poly([(5.5, 15.5), (10, 16), (13.5, 17.5), (18.5, 17.5)], r=S.r * 0.5))]


@icon("social-analytics", CAT, "Speech bubble containing three rising bars",
      tags=["social analytics", "social media metrics", "engagement", "mentions", "social listening", "community"])
def _(S):
    bubble = poly([(2.5, 3), (21.5, 3), (21.5, 17), (10, 17), (5, 21), (5, 17), (2.5, 17)], closed=True, r=S.r)
    return [shell(bubble), detail(seg(8, 13.5, 8, 11)), detail(seg(12, 13.5, 12, 8.5)), detail(seg(16, 13.5, 16, 6.5))]


@icon("bipartite-graph", CAT, "Two columns of nodes with crossing lines linking left nodes to right nodes",
      tags=["bipartite graph", "two mode network", "matching", "graph theory", "links", "network"])
def _(S):
    ys = (4.5, 12, 19.5)
    links = [(0, 1), (0, 2), (1, 0), (2, 1)]

    def node(x, y):
        return dot(x, y, 2.25) if S.name == "rounded" else sq(x - 2, y - 2, 4, 4)
    return [*[line(seg(4, ys[a], 20, ys[b])) for a, b in links], *[node(4, y) for y in ys], *[node(20, y) for y in ys]]


@icon("data-feedback-loop", CAT, "Two curved arrows forming a loop around a small bar chart",
      tags=["feedback loop", "iteration", "continuous improvement", "data loop", "learning cycle", "optimise"])
def _(S):
    k = S.r * 0.4
    a1, a2 = arc(12, 12, 9, 200, 330), arc(12, 12, 9, 20, 150)
    h1 = poly([(*polar(12, 12, 9, 330),), (polar(12, 12, 9, 330)[0] - 3.5, polar(12, 12, 9, 330)[1] - 0.25)], r=0)
    tip1, tip2 = polar(12, 12, 9, 330), polar(12, 12, 9, 150)
    head1 = poly([(tip1[0] - 3.5, tip1[1] - 0.5), tip1, (tip1[0] + 0.5, tip1[1] - 3.5)], r=k)
    head2 = poly([(tip2[0] + 3.5, tip2[1] + 0.5), tip2, (tip2[0] - 0.5, tip2[1] + 3.5)], r=k)
    return [line(a1), line(a2), line(head1), line(head2),
            line(seg(8.5, 15.5, 8.5, 12)), line(seg(12, 15.5, 12, 8.5)), line(seg(15.5, 15.5, 15.5, 10.5))]


@icon("data-anonymization", CAT, "Table whose identifying column is blacked out cell by cell",
      tags=["data anonymisation", "anonymization", "masking", "pseudonymisation", "privacy", "redaction"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(seg(3, 8, 21, 8)), detail(seg(12, 3, 12, 21)),
            detail(seg(5.5, 11.5, 9.5, 11.5)), detail(seg(5.5, 15, 9.5, 15)), detail(seg(5.5, 18.5, 8, 18.5)),
            sq(14, 10, 5, 3), sq(14, 16, 5, 3)]


@icon("geocoding", CAT, "Address card with text lines and an arrow pointing to a map pin",
      tags=["geocoding", "address lookup", "coordinates", "location", "address to map", "geolocation"])
def _(S):
    pin = "M17.5 15.5C15.5 13 13.75 11 13.75 8.25A3.75 3.75 0 0 1 21.25 8.25C21.25 11 19.5 13 17.5 15.5Z"
    return [shell(rect(2.5, 9.5, 11, 11.5, L(S, 1, 2.5))), detail(seg(5.5, 13.5, 10.5, 13.5)), detail(seg(5.5, 17, 9, 17)),
            line(seg(3.5, 5, 8.5, 5)), line(poly([(6.5, 2.5), (9, 5), (6.5, 7.5)], r=S.r * 0.5)),
            shell(pin), dot(17.5, 8.25, 1.25)]


# ============================================================================ chunk 4

def arrow_head(tip, deg, size=3.0, S=None):
    """Open chevron arrow head at tip pointing along deg (0 = right, 90 = down)."""
    a = math.radians(deg)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    bx, by = tip[0] - size * ux, tip[1] - size * uy
    return poly([(bx + nx * size, by + ny * size), tip, (bx - nx * size, by - ny * size)], r=(S.r * 0.4 if S else 0))


@icon("decimal-places", CAT, "Decimal point followed by two zeros with an arrow beneath",
      tags=["decimal places", "increase decimal", "precision", "number format", "rounding", "spreadsheet"])
def _(S):
    def zero(cx):
        return line(rect(cx - 2.5, 5, 5, 9.5, 2.5) if S.name == "rounded" else rect(cx - 2.5, 5, 5, 9.5, 1.5))
    return [dot(4.5, 13.5, 1.6), zero(10.5), zero(18.5),
            line(seg(8, 19, 21, 19)), line(arrow_head((21, 19), 0, 2.5, S))]


@icon("text-to-columns", CAT, "Long line of text above an arrow pointing down into a row of three cells",
      tags=["text to columns", "split text", "delimiter", "split cells", "parse", "spreadsheet"])
def _(S):
    return [line(seg(3, 4, 21, 4)), line(seg(12, 7, 12, 11.5)), line(arrow_head((12, 11.5), 90, 2.5, S)),
            shell(rect(2.5, 15, 19, 6, L(S, 0.5, 2))), detail(seg(8.83, 15, 8.83, 21)), detail(seg(15.17, 15, 15.17, 21))]


@icon("deduplicate", CAT, "Two identical table rows merging into a single row",
      tags=["deduplicate", "remove duplicates", "dedupe", "unique values", "data cleaning", "merge rows"])
def _(S):
    R = L(S, 0.5, 1.5)

    def row(x, y, w):
        return [shell(rect(x, y, w, 4.5, R)), detail(seg(x + 3, y, x + 3, y + 4.5))]
    return [*row(2.5, 3.5, 8), *row(2.5, 16, 8),
            line(poly([(10.5, 5.75), (12.5, 5.75), (12.5, 18.25), (10.5, 18.25)], r=S.r * 0.5)), line(seg(12.5, 12, 14, 12)),
            *row(15, 9.75, 6.5)]


@icon("uniform-distribution", CAT, "Flat topped rectangular plateau with straight sides on a corner axis",
      tags=["uniform distribution", "rectangular distribution", "flat distribution", "probability", "equal chance", "statistics"])
def _(S):
    return [axes(S), line(poly([(7.5, 21), (7.5, 9), (17.5, 9), (17.5, 21)], r=S.r))]


@icon("logarithmic-scale", CAT, "Vertical axis with tick marks bunching toward the top of each decade and a rising curve",
      tags=["logarithmic scale", "log scale", "log axis", "exponential", "orders of magnitude", "chart axis"])
def _(S):
    parts = [line(seg(5, 2.5, 5, 21.5))]
    for y0 in (21, 12):
        parts.append(line(seg(5, y0, 9, y0)))
        for f in (0.3, 0.7):
            y = y0 - 9 * f
            parts.append(line(seg(5, y, 7.5, y)))
    parts.append(line(seg(5, 3, 9, 3)))
    parts.append(line("M11.5 20C15.5 19.5 19 15 20.5 4"))
    return parts


@icon("cloud-analytics", CAT, "Cloud outline with three rising bars inside",
      tags=["cloud analytics", "cloud data", "saas analytics", "hosted reporting", "cloud dashboard", "online metrics"])
def _(S):
    cloud = "M7 19.5A4.75 4.75 0 0 1 5.9 10.1A6.5 6.5 0 0 1 18 9.25A5.1 5.1 0 0 1 17 19.5Z"
    return [shell(cloud), detail(seg(8.5, 16.5, 8.5, 14)), detail(seg(12, 16.5, 12, 11.5)), detail(seg(15.5, 16.5, 15.5, 12.5))]


@icon("random-walk", CAT, "Jagged path of short straight steps wandering away from a start dot",
      tags=["random walk", "brownian motion", "stochastic", "drunkard's walk", "simulation", "path"])
def _(S):
    pts = [(4, 19.5), (7, 15.5), (5, 11.5), (10, 10), (12, 14), (15, 8.5), (12.5, 4.5), (17.5, 4), (20.5, 8)]
    return [line(poly(pts, r=S.r * 0.5)), dot(4, 19.5, 2.25), dot(20.5, 8, 1.5)]


@icon("data-mart", CAT, "Small shop front with a striped awning and a database cylinder in the window",
      tags=["data mart", "data store", "subject database", "data warehouse", "department data", "bi"])
def _(S):
    awn = ("M2.5 8.5L4 3H20L21.5 8.5A2.375 2.375 0 0 1 16.75 8.5A2.375 2.375 0 0 1 12 8.5"
           "A2.375 2.375 0 0 1 7.25 8.5A2.375 2.375 0 0 1 2.5 8.5Z")
    return [shell(awn), detail(seg(7.25, 3, 7.25, 8.5)), detail(seg(12, 3, 12, 8.5)), detail(seg(16.75, 3, 16.75, 8.5)),
            line(poly([(4, 12.5), (4, 21), (20, 21), (20, 12.5)], r=S.r)),
            shell(cyl(12, 13.5, 17.5, 3.25, 1.25)), detail(cyl_band(12, 13.5, 3.25, 1.25))]


@icon("leaderboard", CAT, "Crown above three ranked rows that get shorter down the list",
      tags=["leaderboard", "ranking", "top players", "high scores", "standings", "league table"])
def _(S):
    crown = [(3, 7.5), (3, 2.5), (6, 5), (9, 2.5), (12, 5), (15, 2.5), (15, 7.5)]
    return [shell(poly(crown, closed=True, r=S.r * 0.3)),
            dot(4, 11.5, 1.6), line(seg(8, 11.5, 21, 11.5)),
            dot(4, 16, 1.6), line(seg(8, 16, 18, 16)),
            dot(4, 20.5, 1.6), line(seg(8, 20.5, 15, 20.5))]


@icon("comparison-table", CAT, "Table with a label column and two value columns of check marks and crosses",
      tags=["comparison table", "feature comparison", "pricing table", "compare", "checklist", "versus"])
def _(S):
    k = S.r * 0.3
    return [shell(rect(2.5, 3, 19, 18, S.R)), detail(seg(2.5, 8, 21.5, 8)), detail(seg(9, 3, 9, 21)), detail(seg(15.25, 3, 15.25, 21)),
            detail(poly([(10.5, 12), (11.75, 13.25), (14, 10.75)], r=k)), detail(seg(17, 10.5, 19.75, 13.25)), detail(seg(19.75, 10.5, 17, 13.25)),
            detail(poly([(10.5, 17), (11.75, 18.25), (14, 15.75)], r=k)), detail(poly([(16.75, 17), (18, 18.25), (20.25, 15.75)], r=k))]


@icon("gap-analysis", CAT, "Short bar and tall bar with a double arrow measuring the gap between their tops",
      tags=["gap analysis", "shortfall", "variance", "target vs actual", "difference", "benchmark"])
def _(S):
    R = L(S, 0.5, 1.5)
    return [shell(rect(3, 14, 5.5, 7, R)), shell(rect(15.5, 3, 5.5, 18, R)),
            line(seg(11.75, 5, 11.75, 12)), line(arrow_head((11.75, 3.5), -90, 2, S)), line(arrow_head((11.75, 13.5), 90, 2, S))]


@icon("value-stream-map", CAT, "Two process boxes joined by an arrow above a stepped timeline",
      tags=["value stream map", "vsm", "lean", "process flow", "lead time", "cycle time"])
def _(S):
    R = L(S, 0.5, 1.5)
    return [shell(rect(2.5, 3.5, 7, 6.5, R)), shell(rect(14.5, 3.5, 7, 6.5, R)),
            line(seg(10.5, 6.75, 12.5, 6.75)), solid(poly([(12, 4.75), (14, 6.75), (12, 8.75)], closed=True)),
            line(poly([(2.5, 15), (8, 15), (8, 20), (16, 20), (16, 15), (21.5, 15)], r=S.r))]


@icon("one-to-many-relation", CAT, "Relationship line with a single bar at one end and a crow's foot at the other",
      tags=["one to many", "crow's foot", "entity relationship", "erd", "cardinality", "database relation"])
def _(S):
    return [line(seg(2.5, 12, 21.5, 12)), line(seg(6, 8, 6, 16)),
            line(poly([(21.5, 6.5), (16, 12), (21.5, 17.5)], r=S.r * 0.5))]


@icon("color-scale", CAT, "Legend bar divided into bands from light to dark with tick marks below",
      tags=["color scale", "colour scale", "legend", "gradient legend", "heat map key", "color ramp"])
def _(S):
    frame = (2.5, 5, 19, 8)
    return [shell(rect(*frame, L(S, 0.5, 2))), detail(seg(8.83, 5, 8.83, 13)), detail(seg(15.17, 5, 15.17, 13)),
            dot(12, 7.75, 1.1), dot(12, 10.25, 1.1),
            clip_sq(S, 15.17, 5, 7, 8, frame),
            *[line(seg(x, 16, x, 19)) for x in (3.5, 12, 20.5)]]


# ============================================================================ chunk 5

@icon("crosstab", CAT, "Table whose header row and column are shaded, with the corner cell split by a diagonal",
      tags=["crosstab", "cross tabulation", "contingency table", "pivot table", "two way table", "matrix"])
def _(S):
    frame = (3, 3, 18, 18)
    return [shell(rect(*frame, S.R)), clip_sq(S, 10, 3, 11, 6.5, frame), clip_sq(S, 3, 10, 6.5, 11, frame),
            detail(seg(4.25, 4.25, 10, 10)), detail(seg(15.5, 9.5, 15.5, 21)), detail(seg(9.5, 15.5, 21, 15.5))]


@icon("regression-residuals", CAT, "Dots above and below a straight fitted line, each joined to it by a short vertical stroke",
      tags=["residuals", "regression", "linear regression", "errors", "fitted line", "least squares"])
def _(S):
    def fit(x):
        return 19.5 - (x - 2.5) * 15 / 19
    pts = [(6, 11.5), (10.5, 18.5), (15, 5), (19, 12.5)]
    parts = [line(seg(2.5, 19.5, 21.5, 4.5))]
    for x, y in pts:
        f = fit(x)
        parts.append(dot(x, y, 1.75))
        parts.append(line(seg(x, y + (1.5 if y < f else -1.5), x, f + (-2 if y < f else 2))))
    return parts


@icon("data-journalism", CAT, "Newspaper page with a masthead, text lines and a small bar chart in one column",
      tags=["data journalism", "news graphic", "infographic", "data story", "newspaper", "reporting"])
def _(S):
    return [shell(rect(3, 3, 18, 18, L(S, 1, 3))), detail(seg(3, 8, 21, 8)),
            detail(seg(6, 12, 10.5, 12)), detail(seg(6, 15, 10.5, 15)), detail(seg(6, 18, 10.5, 18)),
            detail(seg(14, 18, 14, 14.5)), detail(seg(17.5, 18, 17.5, 11.5))]


@icon("swingometer", CAT, "Semicircular dial split into two halves with the needle swung toward one side",
      tags=["swingometer", "election swing", "polling", "vote swing", "political", "dial"])
def _(S):
    half = "M3 18A9 9 0 0 1 21 18Z"
    body = D(P(half), ST(half, 2))
    left = Part("dot", path_to_d(I(body, P(rect(0, 0, 11, 24)))))
    tip = polar(12, 18, 7, -55)
    return [shell(half), left,
            detail(seg(12, 18, *tip)), dot(12, 18, 2)]


@icon("lorenz-curve", CAT, "Corner axis with a straight diagonal and a curve sagging below it",
      tags=["lorenz curve", "inequality", "gini coefficient", "income distribution", "wealth", "economics"])
def _(S):
    return [axes(S), line(seg(3, 21, 21, 3)), line("M7 21C14.5 20.5 19.5 16 21 7")]


@icon("qq-plot", CAT, "Dots lined up along a diagonal reference line, curling away from it at both ends",
      tags=["qq plot", "quantile quantile", "normality test", "probability plot", "distribution check", "statistics"])
def _(S):
    return [line(seg(5.5, 18.5, 18.5, 5.5)), *[dot(x, y, 1.75) for x, y in ((8.5, 15.5), (12, 12), (15.5, 8.5))],
            dot(3.5, 14.5, 1.75), dot(20.5, 9.5, 1.75)]


@icon("raincloud-plot", CAT, "Half violin shape above a small box plot with a row of scattered dots below",
      tags=["raincloud plot", "violin plot", "distribution", "box plot", "jitter", "statistics"])
def _(S):
    cloud = "M3 9.5C6 9.5 7.5 3 11 3C14.5 3 16 9.5 21 9.5Z"
    return [shell(cloud), line(seg(3, 13.75, 8, 13.75)), line(seg(15.5, 13.75, 21, 13.75)),
            shell(rect(8, 12, 7.5, 3.5, L(S, 0, 1))),
            *[dot(x, y, 1.2) for x, y in ((4, 19.5), (7.5, 21), (10.5, 19), (13.5, 21), (16.5, 19.5), (20, 21))]]


@icon("cell-range", CAT, "Spreadsheet grid with a block of cells selected inside a heavy border",
      tags=["cell range", "selection", "selected cells", "range", "spreadsheet", "block"])
def _(S):
    ring = ST(rect(7.5, 7.5, 9, 9), 3, S.cap, S.join)
    lines = [seg(7.5, 3, 7.5, 7.5), seg(16.5, 3, 16.5, 7.5), seg(7.5, 16.5, 7.5, 21), seg(16.5, 16.5, 16.5, 21),
             seg(3, 7.5, 7.5, 7.5), seg(3, 16.5, 7.5, 16.5), seg(16.5, 7.5, 21, 7.5), seg(16.5, 16.5, 21, 16.5),
             seg(12, 8.5, 12, 15.5), seg(8.5, 12, 15.5, 12)]
    return [shell(rect(3, 3, 18, 18, S.R)), *[detail(d) for d in lines], Part("dot", path_to_d(ring))]


@icon("table-autofilter", CAT, "Table header with a small dropdown triangle in each header cell",
      tags=["autofilter", "filter dropdown", "table filter", "column filter", "sort and filter", "spreadsheet"])
def _(S):
    tri = [Part("dot", poly([(x - 2, 5.25), (x + 2, 5.25), (x, 7.5)], closed=True, r=S.r * 0.2)) for x in (8.5, 18)]
    return [shell(rect(2.5, 2.5, 19, 19, S.R)), detail(seg(2.5, 10, 21.5, 10)), detail(seg(12, 2.5, 12, 21.5)),
            detail(seg(2.5, 15.75, 21.5, 15.75)), *tri]


@icon("group-rows", CAT, "Table rows with a bracket joining three of them and a minus box at the bracket end",
      tags=["group rows", "outline", "collapse rows", "row grouping", "subtotal", "spreadsheet"])
def _(S):
    rows = [line(seg(10.5, y, 21.5, y)) for y in (4.5, 10, 15, 20)]
    return [shell(rect(2.5, 2.5, 5, 5, L(S, 0, 1.5))), detail(seg(3.75, 5, 6.25, 5)),
            line(poly([(5, 10), (5, 20), (7.5, 20)], r=S.r * 0.5)), *rows]


@icon("circular-reference", CAT, "Three cells in a triangle linked by arrows that loop back to the first",
      tags=["circular reference", "formula loop", "circular dependency", "spreadsheet error", "cycle", "loop"])
def _(S):
    R = L(S, 0, 1)
    cells = [shell(rect(9, 2.5, 6, 4.5, R)), shell(rect(2.5, 16.5, 6, 4.5, R)), shell(rect(15.5, 16.5, 6, 4.5, R))]
    return [*cells,
            line("M16.5 5C18.5 7 19.5 10 19 13.5"), line(arrow_head((19, 14), 95, 2, S)),
            line("M14 19H10.5"), line(arrow_head((10.25, 19), 180, 2, S)),
            line("M5 14C4.5 10 5.5 7 7.5 5"), line(arrow_head((7.75, 4.75), -45, 2, S))]


@icon("trace-precedents", CAT, "Two cells each sending an arrow from a dot into one target cell",
      tags=["trace precedents", "formula auditing", "cell dependencies", "arrows", "spreadsheet", "audit"])
def _(S):
    R = L(S, 0, 1)
    return [shell(rect(2.5, 2.5, 6.5, 5, R)), shell(rect(2.5, 16.5, 6.5, 5, R)), shell(rect(15.5, 8, 6, 8, R)),
            dot(5.75, 5, 1.25), dot(5.75, 19, 1.25),
            line(seg(9.5, 6.5, 11.5, 8.5)), line(arrow_head((13.5, 10.5), 45, 2, S)),
            line(seg(9.5, 17.5, 11.5, 15.5)), line(arrow_head((13.5, 13.5), -45, 2, S))]


def _slicer_filled():
    return U(ST(seg(3, 3, 21, 3), 2.5), P(rect(2.5, 5.75, 19, 4.25, 1.5)), ST(rect(4, 12.25, 16, 3.5, 1.75), 2.5),
             P(rect(2.5, 18, 19, 4, 1.5)))


@icon("data-slicer", CAT, "Header bar above a column of pill buttons, two of them selected",
      tags=["slicer", "data slicer", "filter buttons", "dashboard filter", "segment picker", "pivot filter"],
      filled=_slicer_filled)
def _(S):
    R = L(S, 0.5, 1.75)
    return [line(seg(3, 3, 21, 3)), sq(3, 6, 18, 3.5, R), shell(rect(4, 12, 16, 4, R)), sq(3, 18.5, 18, 3.5, R)]


@icon("data-source", CAT, "Database cylinder with three short arrows pointing out of its right side",
      tags=["data source", "source database", "feed", "input data", "origin", "export"])
def _(S):
    parts = database(7.5, 4, 20, 5, 2)
    for y in (6.5, 12, 17.5):
        parts += [line(seg(14.5, y, 20.5, y)), line(arrow_head((21, y), 0, 2.25, S))]
    return parts


@icon("data-transformation", CAT, "Square turning into a circle through a gear, joined by an arrow",
      tags=["data transformation", "etl", "transform", "conversion", "processing", "mapping"])
def _(S):
    g = poly(gear_pts(12, 16, 3.5, 5.25, 8, phase=22.5), closed=True, r=S.r * 0.3)
    return [shell(rect(2.5, 2.5, 6, 6, L(S, 0.5, 1.5))), shell(circle(18.5, 5.5, 3)),
            line(seg(10.5, 5.5, 13, 5.5)), line(arrow_head((13.5, 5.5), 0, 2, S)),
            shell(g), detail(circle(12, 16, 1.5))]


@icon("weighted-graph", CAT, "Three nodes joined by edges of different thickness for their weights",
      tags=["weighted graph", "edge weights", "network", "graph theory", "shortest path", "costs"])
def _(S):
    a, b, c = (5, 6), (19, 6), (12, 18.5)
    return [solid(thick(seg(*a, *b), 2, S)), solid(thick(seg(*b, *c), 4, S)), solid(thick(seg(*c, *a), 3, S)),
            shell(circle(*a, 2.5)), shell(circle(*b, 2.5)), shell(circle(*c, 2.5))]


@icon("pie-chart-map", CAT, "Folded map with two small pie charts over different regions",
      tags=["pie chart map", "map chart", "regional share", "geographic breakdown", "proportions by region", "thematic map"])
def _(S):
    def pie(cx, cy, r):
        return [detail(circle(cx, cy, r)), Part("dot", f"M{fmt(cx)} {fmt(cy)}V{fmt(cy - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx + r)} {fmt(cy)}Z")]
    return [shell(_map_outline(S)), *pie(8.5, 9, 2.75), *pie(15.5, 15, 2.75)]


@icon("conversion-rate", CAT, "Funnel with a percent sign beneath its narrow spout",
      tags=["conversion rate", "funnel conversion", "percent converted", "sales funnel", "cro", "marketing"])
def _(S):
    funnel = [(2.5, 2.5), (21.5, 2.5), (14, 9.5), (14, 12.5), (10, 12.5), (10, 9.5)]
    return [shell(poly(funnel, closed=True, r=S.r * 0.4)),
            line(seg(15.5, 15.5, 8.5, 21.5)), dot(9.25, 16.25, 1.5), dot(14.75, 20.75, 1.5)]


@icon("tracking-pixel", CAT, "Envelope with a tiny square at its corner sending out signal arcs",
      tags=["tracking pixel", "email tracking", "open tracking", "web beacon", "spy pixel", "analytics tag"])
def _(S):
    return [shell(rect(2.5, 10, 13, 10.5, L(S, 0.5, 2.5))), detail(poly([(2.5, 10.5), (9, 15.5), (15.5, 10.5)], r=S.r * 0.5)),
            sq(14, 8.5, 3.5, 3.5), line(arc(15.75, 10.25, 4, -80, -10)),
            line(arc(15.75, 10.25, 6.5, -80, -10))]
