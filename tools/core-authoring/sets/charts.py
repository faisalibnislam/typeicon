"""TypeIcon Core: charts & data.

Bar-style charts follow the v0.1 `chart-bar`: 2 px bars in Line/Rounded and 4 px solid bars in Filled.
"""
from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, polar

CAT = "charts"
AXES = [(3, 3), (3, 21), (21, 21)]


def axes(S):
    return line(poly(AXES, r=S.r))


def hbars_filled(bars):
    """Filled design for horizontal 2 px bars: (y, x0, x1) -> 4 px solid bars."""
    return lambda: U(*(P(rect(x0 - 1, y - 2, x1 - x0 + 2, 4, 0.75)) for y, x0, x1 in bars))


def vbars_filled(bars):
    """Filled design for vertical 2 px bars: (x, y0, y1) -> 4 px solid bars."""
    return lambda: U(*(P(rect(x - 2, min(y0, y1) - 1, 4, abs(y1 - y0) + 2, 0.75)) for x, y0, y1 in bars))


def arc_pts(cx, cy, r, a0, a1, n=12):
    return [polar(cx, cy, r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]


# ============================================================================ bar-like charts

_HB = [(6, 3, 19), (12, 3, 14.5), (18, 3, 9.5)]


@icon("chart-bar-horizontal", CAT, "Horizontal bar chart",
      tags=["bar chart", "graph", "statistics", "ranking", "comparison", "data"], aliases=["bar-chart-horizontal"],
      filled=hbars_filled(_HB))
def _(S):
    return [line(seg(x0, y, x1, y)) for y, x0, x1 in _HB]


_HIST = [(3, 21), (3, 14), (7.5, 14), (7.5, 7), (12, 7), (12, 3.5), (16.5, 3.5), (16.5, 11), (21, 11), (21, 21)]


@icon("chart-histogram", CAT, "Histogram of adjoining bars showing a distribution",
      tags=["histogram", "distribution", "frequency", "statistics", "bins", "data"], aliases=["histogram"])
def _(S):
    return [shell(poly(_HIST, closed=True, r=S.r * 0.5)),
            detail(seg(7.5, 14, 7.5, 21)), detail(seg(12, 7, 12, 21)), detail(seg(16.5, 11, 16.5, 21))]


_WF = [(4, 20, 13), (9.33, 13, 5.5), (14.67, 5.5, 10), (20, 20, 10)]


@icon("chart-waterfall", CAT, "Waterfall chart of floating bars that add up to a total",
      tags=["waterfall", "bridge chart", "cumulative", "variance", "finance", "data"], aliases=["waterfall-chart"],
      filled=vbars_filled(_WF))
def _(S):
    return [line(seg(x, y0, x, y1)) for x, y0, y1 in _WF]


_GANTT = [(6, 7, 13), (12, 10, 17), (18, 14, 20.5)]


@icon("chart-gantt", CAT, "Gantt chart of staggered task bars along a timeline",
      tags=["gantt", "timeline", "schedule", "project", "roadmap", "tasks"], aliases=["gantt"],
      filled=lambda: U(hbars_filled(_GANTT)(), ST(seg(3, 2.5, 3, 21.5), 2.5)))
def _(S):
    return [line(seg(3, 2.5, 3, 21.5)), *[line(seg(x0, y, x1, y)) for y, x0, x1 in _GANTT]]


@icon("chart-funnel", CAT, "Funnel chart of narrowing stages",
      tags=["funnel", "conversion", "pipeline", "stages", "sales", "marketing"], aliases=["funnel-chart"])
def _(S):
    rr = S.r
    return [shell(rect(3, 3.5, 18, 3, rr)), shell(rect(6, 10.5, 12, 3, rr)), shell(rect(9, 17.5, 6, 3, rr))]


# ============================================================================ round charts

def _sector(a0, a1, r0=4.5, r1=9, cx=12, cy=12):
    return arc_pts(cx, cy, r1, a0, a1) + arc_pts(cx, cy, r0, a1, a0)


_DONUT = [(-90, 30), (30, 150), (150, 270)]


@icon("chart-donut", CAT, "Donut chart: a ring divided into segments",
      tags=["donut", "doughnut", "ring chart", "proportion", "share", "percentage"], aliases=["chart-doughnut", "donut-chart"])
def _(S):
    parts = [shell(poly(_sector(a0, a1), closed=True, r=S.r)) for a0, a1 in _DONUT]
    parts += [detail(seg(*polar(12, 12, 4.5, a), *polar(12, 12, 9, a))) for a in (-90, 30, 150)]
    return parts


@icon("chart-radar", CAT, "Radar chart: a data shape inside a pentagon web",
      tags=["radar", "spider chart", "web chart", "skills", "comparison", "polar"], aliases=["spider-chart"])
def _(S):
    web = [polar(12, 12.5, 9, -90 + i * 72) for i in range(5)]
    data = [polar(12, 12.5, r, -90 + i * 72) for i, r in enumerate((5.5, 5, 2.5, 3.5, 4.5))]
    return [shell(poly(web, closed=True, r=S.r)), detail(poly(data, closed=True, r=S.r * 0.5))]


@icon("gauge", CAT, "Round dial gauge with ticks and a needle",
      tags=["meter", "dial", "measure", "level", "pressure", "performance"], aliases=["dial"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(seg(5.5, 12, 7.5, 12)), detail(seg(12, 5.5, 12, 7.5)), detail(seg(16.5, 12, 18.5, 12)),
            detail(seg(12, 13, 15.5, 9)), dot(12, 13, 2)]


@icon("speed-gauge", CAT, "Arched speed dial with the needle near the top of the scale",
      tags=["speed", "speedometer", "performance", "fast", "benchmark", "speed test"], aliases=["speed-dial"])
def _(S):
    return [line(arc(12, 15, 9, 160, 20)), line(seg(*polar(12, 15, 6.5, 220), *polar(12, 15, 4.5, 220))), line(seg(12, 8.5, 12, 10.5)),
            line(seg(12, 15, 17.5, 10)), dot(12, 15, 2.25)]


# ============================================================================ plots

@icon("chart-scatter", CAT, "Scatter plot: dots between two axes",
      tags=["scatter plot", "correlation", "points", "distribution", "statistics", "xy"], aliases=["scatter-plot"])
def _(S):
    return [axes(S), *[dot(x, y, 1.5) for x, y in ((7.5, 15.5), (10.5, 9.5), (13, 14), (16.5, 6.5), (18.5, 11.5))]]


@icon("chart-bubble", CAT, "Bubble chart: circles of different sizes between two axes",
      tags=["bubble", "bubbles", "size", "comparison", "statistics", "xy"], aliases=["bubble-chart"])
def _(S):
    return [axes(S), shell(circle(9.5, 13, 3.25)), shell(circle(16.5, 7.5, 2.25)), shell(circle(17, 15.5, 1.5))]


@icon("chart-dots", CAT, "Line chart with a dot marking each data point",
      tags=["line chart", "data points", "markers", "trend", "graph", "series"], aliases=["line-chart-dots"])
def _(S):
    pts = [(6.5, 16), (10.5, 10.5), (14, 13.5), (18.5, 6.5)]
    return [axes(S), line(poly(pts, r=S.r)), *[dot(x, y, 2) for x, y in pts]]


@icon("chart-arrows", CAT, "Chart with one arrow rising and one falling",
      tags=["increase", "decrease", "up and down", "change", "variance", "trend"], aliases=["chart-up-down"])
def _(S):
    return [axes(S), line(seg(9, 17.5, 9, 7)), line(poly([(6, 10), (9, 7), (12, 10)], r=S.r * 0.5)),
            line(seg(16, 6, 16, 16.5)), line(poly([(13, 13.5), (16, 16.5), (19, 13.5)], r=S.r * 0.5))]


# ============================================================================ tables and panels

@icon("chart-treemap", CAT, "Treemap: a square divided into nested rectangles",
      tags=["treemap", "hierarchy", "proportion", "blocks", "area", "data"], aliases=["treemap"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(seg(11, 3, 11, 21)), detail(seg(3, 14, 11, 14)),
            detail(seg(11, 10.5, 21, 10.5)), detail(seg(16, 10.5, 16, 21))]


@icon("chart-sankey", CAT, "Sankey diagram: flows running between nodes",
      tags=["sankey", "flow", "allocation", "streams", "diagram", "energy flow"], aliases=["sankey"])
def _(S):
    def flow(y0, y1):
        return f"M5 {fmt(y0)}C12 {fmt(y0)} 12 {fmt(y1)} 19 {fmt(y1)}"
    rr = S.r * 0.66
    return [shell(rect(3, 3.5, 2, 8, rr)), shell(rect(3, 14.5, 2, 6, rr)),
            shell(rect(19, 3, 2, 5, rr)), shell(rect(19, 11, 2, 9.5, rr)),
            line(flow(5.5, 14)), line(flow(9.5, 5.5)), line(flow(17.5, 18))]


def _header_solid(S):
    R = S.R + 1
    return solid(f"M2 9.5V{fmt(3 + R)}A{fmt(R)} {fmt(R)} 0 0 1 {fmt(2 + R)} 3H{fmt(22 - R)}A{fmt(R)} {fmt(R)} 0 0 1 22 {fmt(3 + R)}V9.5Z")


_TABLE_LINES = [seg(3, 9.5, 21, 9.5), seg(3, 14.75, 21, 14.75), seg(9, 9.5, 9, 20), seg(15, 9.5, 15, 20)]


@icon("table-data", CAT, "Data table with a header row and columns",
      tags=["table", "grid", "rows", "columns", "dataset", "records"], aliases=["data-table"],
      filled=lambda: D(U(P(rect(2, 3, 20, 18, 3))), *[ST(d, 2) for d in _TABLE_LINES]))
def _(S):
    return [shell(rect(3, 4, 18, 16, S.R)), _header_solid(S), *[detail(d) for d in _TABLE_LINES]]


@icon("analytics", CAT, "Panel with rising bars; analytics dashboard",
      tags=["statistics", "insights", "metrics", "dashboard", "reporting", "data"], aliases=["insights"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(seg(8, 17, 8, 13.5)), detail(seg(12, 17, 12, 7.5)), detail(seg(16, 17, 16, 10.5))]


@icon("kpi", CAT, "Card with an upward trend arrow; a key performance indicator",
      tags=["key performance indicator", "metric", "target", "performance", "goal", "scorecard"], aliases=["metric"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, S.R)), detail(poly([(6, 15.5), (9.5, 11.5), (12, 14), (17, 9)], r=S.r)),
            detail(poly([(13.5, 9), (17, 9), (17, 12.5)], r=S.r * 0.5))]


@icon("report-chart", CAT, "Report sheet with a pie chart and summary lines",
      tags=["report", "summary", "pie chart", "results", "statistics", "document"], aliases=["chart-report"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, S.R)), detail(circle(12, 9.5, 3.5)), detail(poly([(12, 6), (12, 9.5), (15.5, 9.5)], r=S.r * 0.3)),
            detail(seg(8, 15.5, 16, 15.5)), detail(seg(8, 18.5, 13, 18.5))]
