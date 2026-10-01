"""TypeIcon Core: analytics (batch 002).

Statistics, research, web analytics, spreadsheets and data engineering. Charts keep the 2 px strokes of
`charts.py`; database cylinders follow `database` (flatter end arcs in Line, true half ellipses in Rounded).
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar  # noqa: F401

CAT = "analytics"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap):
    return min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid block: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def cyl_d(S, x, y, w, h, e=None):
    """Database cylinder: (outline, top front arc, band arc builder)."""
    e = e if e is not None else max(1.25, w * 0.18)
    if S.name == "line":
        rx = w * 0.66
        ry = e * 0.6 / (1 - math.sqrt(1 - (w / 2 / rx) ** 2))
    else:
        rx, ry = w / 2, e
    a = f"{fmt(rx)} {fmt(ry)} 0 0"
    out = (f"M{fmt(x)} {fmt(y + e)}A{a} 1 {fmt(x + w)} {fmt(y + e)}V{fmt(y + h - e)}"
           f"A{a} 1 {fmt(x)} {fmt(y + h - e)}Z")
    top = f"M{fmt(x)} {fmt(y + e)}A{a} 0 {fmt(x + w)} {fmt(y + e)}"

    def band(yy):
        return f"M{fmt(x)} {fmt(yy)}A{a} 0 {fmt(x + w)} {fmt(yy)}"
    return out, top, band


def cylinder(S, x, y, w, h, e=None, bands=()):
    out, top, band = cyl_d(S, x, y, w, h, e)
    return [shell(out), detail(top), *[detail(band(b)) for b in bands]]


def head_to(S, tip, deg, size=3.0, role=line):
    """Open arrowhead (chevron) with its tip at `tip`, pointing along `deg` (0 = right, 90 = down)."""
    a = polar(tip[0], tip[1], size, deg + 180 - 45)
    b = polar(tip[0], tip[1], size, deg + 180 + 45)
    return role(poly([a, tip, b], r=S.r * 0.4))


def arrow(S, x1, y1, x2, y2, size=3.0, role=line):
    """Straight arrow; use role=detail when it sits inside a shell (Filled knocks it out)."""
    deg = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return [role(seg(x1, y1, x2, y2)), head_to(S, (x2, y2), deg, size, role)]


def bust(S, cx, hy, hr, w, sy, h=None):
    """Small person: head disc and a shoulder arc (open stroke)."""
    h = h if h is not None else w * 0.9
    return [dot(cx, hy, hr), line(f"M{fmt(cx - w)} {fmt(sy)}A{fmt(w)} {fmt(h)} 0 0 1 {fmt(cx + w)} {fmt(sy)}")]


def window(S, x, y, w, h, bar=4.5, cap=None):
    """Browser or app window: outline plus a title bar line."""
    return [shell(rect(x, y, w, h, S.R if cap is None else min(S.R, cap))), detail(seg(x, y + bar, x + w, y + bar))]


def cursor_pts(x, y, k=1.0):
    """Mouse pointer with its tip at (x, y), pointing up-left."""
    pts = [(0, 0), (0, 8), (2, 6.25), (3.4, 9.2), (5.1, 8.4), (3.75, 5.5), (6.25, 5.5)]
    return [(x + px * k, y + py * k) for px, py in pts]


def cursor(S, x, y, k=1.0):
    return Part("dot", poly(cursor_pts(x, y, k), closed=True, r=L(S, 0, 0.5)))


def dots_along(d_pts, step):
    """Evenly spaced points along a polyline given as a list of points."""
    segs = list(zip(d_pts, d_pts[1:]))
    total = sum(math.dist(a, b) for a, b in segs)
    n = max(1, round(total / step))
    out = []
    for i in range(n + 1):
        t = total * i / n
        for a, b in segs:
            ln = math.dist(a, b)
            if t <= ln + 1e-9:
                out.append((a[0] + (b[0] - a[0]) * t / ln, a[1] + (b[1] - a[1]) * t / ln))
                break
            t -= ln
    return out


def bez_pts(p0, p1, p2, p3, n=24):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        pts.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return pts


def eye_d(cx, cy, w, h):
    return (f"M{fmt(cx - w)} {fmt(cy)}Q{fmt(cx)} {fmt(cy - 2 * h)} {fmt(cx + w)} {fmt(cy)}"
            f"Q{fmt(cx)} {fmt(cy + 2 * h)} {fmt(cx - w)} {fmt(cy)}Z")


def dashed(x1, y1, x2, y2, dash=2.0, gap=2.0, start=0.0):
    """Straight dashed stroke as separate segments (open lines)."""
    ln = math.dist((x1, y1), (x2, y2))
    ux, uy = (x2 - x1) / ln, (y2 - y1) / ln
    out, t = [], start
    while t < ln - 0.3:
        e = min(t + dash, ln)
        out.append(line(seg(x1 + ux * t, y1 + uy * t, x1 + ux * e, y1 + uy * e)))
        t = e + gap
    return out


# ============================================================================ statistics

@icon("hypothesis-test", CAT, "Two overlapping bell curves split by a dashed cutoff line",
      tags=["hypothesis", "significance", "p value", "null hypothesis", "statistics", "distribution"])
def _(S):
    b1 = "M1.5 19C4.25 19 4.5 8 7 8C9.5 8 9.75 19 13 19"
    b2 = "M11 19C14.25 19 14.5 8 17 8C19.5 8 19.75 19 22.5 19"
    dashes = [line(seg(12, y, 12, y + 2)) for y in (2.5, 7, 11.5)]
    return [line(b1), line(b2), *dashes]


_FOREST = [(5.5, 3.5, 10.5, 7), (12, 7.5, 20.5, 16.5), (18.5, 14.5, 21, 17.5)]


@icon("forest-plot", CAT, "Forest plot: rows of squares with whisker lines crossing a reference line",
      tags=["forest plot", "meta analysis", "confidence interval", "effect size", "odds ratio", "statistics"])
def _(S):
    out = [line(seg(12, 2.5, 12, 21.5))]
    for y, x0, x1, c in _FOREST:
        out += [line(seg(x0, y, x1, y)), sq(c - 2, y - 2, 4, 4, L(S, 0, 1))]
    return out


@icon("mean-x-bar", CAT, "Letter x with a bar above it, the symbol for a sample mean",
      tags=["mean", "average", "x bar", "sample mean", "statistics", "math"])
def _(S):
    return [line(seg(6, 9, 18, 21)), line(seg(18, 9, 6, 21)), line(seg(5, 4, 19, 4))]


@icon("probability-tree", CAT, "Tree diagram branching twice from one point",
      tags=["probability", "tree diagram", "outcomes", "branches", "decision", "statistics"])
def _(S):
    return [line(poly([(12, 6), (4, 12), (12, 18)], r=S.r)),
            line(poly([(20, 3), (12, 6), (20, 9)], r=S.r)),
            line(poly([(20, 15), (12, 18), (20, 21)], r=S.r)),
            dot(4, 12, 2)]


@icon("outlier-point", CAT, "Scatter plot with one lone point circled away from the cluster",
      tags=["outlier", "anomaly", "scatter", "deviation", "exception", "statistics"])
def _(S):
    return [line(poly([(3, 3), (3, 21), (21, 21)], r=S.r)),
            dot(7.5, 16.5), dot(12, 16), dot(9, 12),
            line(circle(17, 7, 4)), dot(17, 7, 1.5)]


@icon("data-sampling", CAT, "Large circle of dots with a small sample circle taken from it",
      tags=["sample", "sampling", "subset", "population", "survey", "statistics"])
def _(S):
    return [shell(circle(8.5, 8.5, 6.5)), dot(6, 7, 1.25), dot(11, 7, 1.25), dot(8.5, 11.25, 1.25),
            shell(circle(18, 18, 3.5)), dot(18, 18, 1.25),
            line("M16.5 4.5C19.5 5 20 8 20 11"),
            head_to(S, (20, 12), 90, 2.5)]


@icon("satisfaction-gauge", CAT, "Half-round gauge with a smile below the needle",
      tags=["satisfaction", "csat", "customer happiness", "gauge", "feedback", "score"])
def _(S):
    return [line(arc(12, 14, 9, 180, 360)), line(seg(12, 14, 16.5, 9.5)), dot(12, 14, 2),
            line("M8 18.5Q12 22 16 18.5")]


_RD = [21, 18.5, 16, 14.5, 13.5]


@icon("rating-distribution", CAT, "Star beside five bars of falling length, a breakdown of ratings",
      tags=["ratings", "reviews", "stars", "breakdown", "histogram", "feedback"])
def _(S):
    pts = []
    for i in range(10):
        pts.append(polar(5.5, 12.5, 4.25 if i % 2 == 0 else 1.9, -90 + i * 36))
    out = [solid(poly(pts, closed=True, r=L(S, 0, 0.5)))]
    out += [line(seg(12, 4 + 4 * i, x, 4 + 4 * i)) for i, x in enumerate(_RD)]
    return out


@icon("uptime-bars", CAT, "Row of status bars with two short bars marking downtime",
      tags=["uptime", "status page", "availability", "downtime", "outage", "monitoring"])
def _(S):
    out = []
    for i, x in enumerate((3, 6.5, 10, 13.5, 17, 20.5)):
        y0 = 12.5 if i in (2, 4) else 6.5
        out.append(line(seg(x, y0, x, 17.5)))
    return out


@icon("tally-marks", CAT, "Four strokes crossed by a fifth, with two more strokes beside them",
      tags=["tally", "count", "counting", "score", "marks", "five bar gate"])
def _(S):
    out = [line(seg(x, 5, x, 19)) for x in (2.5, 6, 9.5, 13, 17.5, 21)]
    out.append(line(seg(1.5, 15.5, 14, 8.5)))
    return out


@icon("tally-stick", CAT, "Wooden stick with a row of counting notches cut into its edge",
      tags=["tally stick", "notched stick", "count", "record", "history", "tally"])
def _(S):
    # upright stick with V notches down its left edge, turned 45 degrees like the long tools
    pts = [(9.5, 3)]
    for y in (6.5, 10.5, 14.5):
        pts += [(9.5, y - 1.5), (12, y), (9.5, y + 1.5)]
    pts += [(9.5, 21), (14.5, 21), (14.5, 3)]
    c, s_ = math.cos(math.radians(45)), math.sin(math.radians(45))
    pts = [(12 + (x - 12) * c - (y - 12) * s_, 12 + (x - 12) * s_ + (y - 12) * c) for x, y in pts]
    return [shell(poly(pts, closed=True, r=S.r * 0.4), stroke_miterlimit="2")]


_QUIPU = [(4.5, 17, (9, 14)), (9.5, 20.5, (12,)), (14.5, 15.5, (8.5,)), (19.5, 19, (10, 15))]


@icon("quipu", CAT, "Main cord with knotted cords hanging from it, an Andean record of numbers",
      tags=["quipu", "khipu", "knotted cords", "inca", "counting", "record"])
def _(S):
    out = [line(seg(2, 4.5, 22, 4.5))]
    for x, y1, knots in _QUIPU:
        out.append(line(seg(x, 4.5, x, y1)))
        out += [dot(x, k, 1.9) for k in knots]
    return out


@icon("census", CAT, "Clipboard form with a house and tick lines, a population census",
      tags=["census", "population count", "household", "survey", "form", "population"])
def _(S):
    return [shell(poly([(8.5, 4), (4, 4), (4, 21.5), (20, 21.5), (20, 4), (15.5, 4)], r=S.R)),
            shell(rect(8.5, 2.5, 7, 4, rr(S, 1.5))),
            detail(poly([(8, 14.5), (8, 11.5), (12, 9), (16, 11.5), (16, 14.5)], closed=True, r=S.r * 0.4)),
            detail(seg(8, 18, 16, 18))]


# ============================================================================ audiences and research

@icon("demographics", CAT, "Three people of different sizes above a pie chart",
      tags=["demographics", "population", "age groups", "audience", "breakdown", "statistics"])
def _(S):
    wedge = poly([(12, 16.5), *[polar(12, 16.5, 5, a) for a in range(-90, 1, 15)]], closed=True)
    return [*bust(S, 4, 4, 1.5, 2, 9, 2.5), *bust(S, 12, 3.5, 2, 3, 10), *bust(S, 20, 4, 1.5, 2, 9, 2.5),
            shell(circle(12, 16.5, 5)), Part("dot", wedge)]


@icon("market-research", CAT, "Magnifying glass over a small group of people",
      tags=["market research", "customer research", "study", "audience", "insight", "survey"])
def _(S):
    return [shell(circle(10, 10, 7.5)), line(seg(15.5, 15.5, 21, 21)),
            dot(10, 7.5, 2), detail("M6.5 14A3.5 3 0 0 1 13.5 14")]


@icon("audience-segments", CAT, "Circle cut into three segments, each holding a person",
      tags=["segments", "segmentation", "audience", "cohorts", "groups", "targeting"])
def _(S):
    out = []
    for a0 in (-90, 30, 150):
        # slices pulled 1.25 px apart so each segment reads on its own
        m = a0 + 60
        ox, oy = polar(0, 0, 1.25, m)
        pts = [(12 + ox, 12 + oy), *[polar(12 + ox, 12 + oy, 9.25, a0 + 7 + t) for t in range(0, 107, 13)]]
        out.append(shell(poly(pts, closed=True, r=S.r * 0.6)))
        hx, hy = polar(12 + ox, 12 + oy, 5.1, m)
        person = path_to_d(U(P(circle(hx, hy - 1.4, 1.5)),
                             P(f"M{fmt(hx - 2.4)} {fmt(hy + 2.6)}A2.4 2.3 0 0 1 {fmt(hx + 2.4)} {fmt(hy + 2.6)}Z")))
        out.append(Part("dot", person))
    return out


@icon("customer-churn", CAT, "Person inside an open ring with an arrow leaving through the gap",
      tags=["churn", "attrition", "lost customers", "cancel", "leave", "retention"])
def _(S):
    return [line(arc(10, 12, 8, 35, 325)), dot(10, 9.5, 2), line("M6.5 16A3.5 3 0 0 1 13.5 16"),
            *arrow(S, 14.5, 12, 22, 12, 3)]


@icon("retention-curve", CAT, "Curve that drops steeply then levels off, with a person marker",
      tags=["retention", "cohort", "churn curve", "survival", "users", "decay"])
def _(S):
    return [line(poly([(3, 3), (3, 21), (21, 21)], r=S.r)),
            line("M7 4C7.5 12 10 15.5 21 16"), *bust(S, 17, 4.5, 1.75, 3, 11)]


@icon("user-journey", CAT, "Dotted winding path from a person to a finish flag",
      tags=["user journey", "customer journey", "path", "experience", "onboarding", "steps"])
def _(S):
    pts = bez_pts((9, 20), (19, 20), (5, 12.5), (16, 12))
    out = [dot(x, y, 1.1) for x, y in dots_along(pts, 3.4)]
    return [*bust(S, 4.5, 14.5, 1.75, 2.75, 21), *out,
            line(seg(18, 2.5, 18, 13)), solid(poly([(18, 2.5), (22, 4.5), (18, 6.5)], closed=True, r=L(S, 0, 0.5)))]


@icon("user-flow", CAT, "Screen linked by arrows to two further screens",
      tags=["user flow", "screen flow", "navigation", "wireframe", "branching", "ux"])
def _(S):
    k = rr(S, 1.5)
    return [shell(rect(2, 8.5, 6, 7, k)), shell(rect(16, 2, 6, 7, k)), shell(rect(16, 15, 6, 7, k)),
            line(seg(8, 12, 10.5, 12)), line(poly([(13.5, 5.5), (10.5, 5.5), (10.5, 18.5), (13.5, 18.5)], r=S.r)),
            solid(poly([(13.5, 3.5), (15.5, 5.5), (13.5, 7.5)], closed=True)),
            solid(poly([(13.5, 16.5), (15.5, 18.5), (13.5, 20.5)], closed=True))]


# ============================================================================ web and product analytics

@icon("click-heatmap", CAT, "Web page with heat rings around a clicked spot and a pointer",
      tags=["heatmap", "click map", "clicks", "hotspot", "ux research", "web analytics"])
def _(S):
    return [*window(S, 2.5, 3, 19, 18),
            detail(circle(9.5, 13, 3.5)), dot(9.5, 13, 1.25), cursor(S, 14, 15, 0.65)]


@icon("scroll-depth", CAT, "Tall page with a scrollbar and a dashed line marking how far was read",
      tags=["scroll depth", "scroll tracking", "engagement", "fold", "page reading", "web analytics"])
def _(S):
    return [shell(rect(2.5, 2, 13, 20, rr(S, 3))), detail(seg(6, 5.5, 12, 5.5)), detail(seg(6, 9, 12, 9)),
            *[detail(seg(x, 14.5, x + 2, 14.5)) for x in (5.5, 9.5)],
            *arrow(S, 20, 2.5, 20, 14.5, 3)]


@icon("session-recording", CAT, "Browser window with a dotted pointer trail and a play button",
      tags=["session replay", "session recording", "screen recording", "user behavior", "playback", "ux research"])
def _(S):
    return [*window(S, 2, 3, 20, 18),
            dot(5, 18, 1), dot(6.75, 14.25, 1), cursor(S, 9.5, 10.5, 0.7),
            Part("dot", poly([(15.5, 11), (19.5, 14), (15.5, 17)], closed=True, r=L(S, 0, 0.6)))]


@icon("bounce-rate", CAT, "Arrow that hits a web page and bounces straight back out",
      tags=["bounce rate", "bounce", "exit", "single page visit", "leave", "web analytics"])
def _(S):
    return [*window(S, 12.5, 3, 9.5, 18, 4, cap=2.5),
            line(poly([(2.5, 4), (9.5, 12), (4, 19)], r=S.r)), head_to(S, (4, 19), math.degrees(math.atan2(7, -5.5)), 3)]


@icon("click-through-rate", CAT, "Pointer clicking a link bar with a percent sign beside it",
      tags=["click through rate", "ctr", "clicks", "link", "conversion", "percentage"])
def _(S):
    return [shell(rect(2, 3, 16, 6.5, rr(S, 3.25))), cursor(S, 9.5, 11, 1.0),
            line(seg(15.5, 21, 21, 12.5)), dot(16, 13.5, 1.5), dot(20.5, 20, 1.5)]


@icon("page-views", CAT, "Web page window with an eye in its centre",
      tags=["page views", "pageviews", "views", "visits", "traffic", "web analytics"])
def _(S):
    return [*window(S, 2, 3, 20, 18), detail(eye_d(12, 14, 6, 3)), dot(12, 14, 1.5)]


@icon("impressions", CAT, "Eye above three rising bars",
      tags=["impressions", "views", "reach", "ad views", "visibility", "marketing"])
def _(S):
    return [shell(eye_d(12, 7, 8.5, 4)), dot(12, 7, 2),
            line(seg(7, 21, 7, 17.5)), line(seg(12, 21, 12, 15.5)), line(seg(17, 21, 17, 13.5))]


@icon("web-analytics", CAT, "Browser window holding a small bar chart",
      tags=["web analytics", "site statistics", "traffic", "website", "dashboard", "visitors"])
def _(S):
    return [*window(S, 2, 3, 20, 18), detail(seg(7.5, 17.5, 7.5, 15)), detail(seg(12, 17.5, 12, 12)),
            detail(seg(16.5, 17.5, 16.5, 10.5))]


@icon("mobile-analytics", CAT, "Smartphone with a bar chart on its screen",
      tags=["mobile analytics", "app analytics", "phone", "app statistics", "usage", "dashboard"])
def _(S):
    return [shell(rect(4.5, 2, 15, 20, L(S, 2, 3.5))), detail(seg(8.5, 16, 8.5, 12.5)), detail(seg(12, 16, 12, 8.5)),
            detail(seg(15.5, 16, 15.5, 10.5)), detail(seg(10.5, 19, 13.5, 19))]


@icon("location-analytics", CAT, "Map pin beside a small bar chart",
      tags=["location analytics", "geo analytics", "store visits", "foot traffic", "regional data", "map"])
def _(S):
    pin = "M8 15.5C8 15.5 2.5 10.5 2.5 7.5A5.5 5.5 0 0 1 13.5 7.5C13.5 10.5 8 15.5 8 15.5Z"
    pin_l = "M8 16L3.2 10A5.5 5.5 0 1 1 12.8 10Z"
    return [shell(L(S, pin_l, pin)), dot(8, 7.5, 1.75),
            line(seg(2, 21, 22, 21)), line(seg(16, 18, 16, 12)), line(seg(20.5, 18, 20.5, 8))]


# ============================================================================ planning and strategy

@icon("ab-testing", CAT, "Two panels marked A and B with a tick under the winning one",
      tags=["a/b test", "split test", "experiment", "variant", "compare", "conversion"])
def _(S):
    k = rr(S, 2)
    b = "M15.5 12.5V5H18A1.9 1.9 0 0 1 18 8.75H15.5M18 8.75A1.9 1.9 0 0 1 18 12.5H15.5"
    return [shell(rect(2, 2, 9, 13.5, k)), shell(rect(13, 2, 9, 13.5, k)),
            detail(poly([(4.25, 12.5), (6.5, 5), (8.75, 12.5)], r=S.r * 0.3)), detail(seg(5.25, 10.25, 7.75, 10.25)),
            detail(b), line(poly([(4, 20), (6, 22), (9.5, 18.5)], r=S.r * 0.4))]


@icon("okr", CAT, "Target with a hit in the centre beside a list of key results",
      tags=["okr", "objectives", "key results", "goals", "targets", "planning"])
def _(S):
    k = L(S, 0, 0.6)
    return [line(circle(7.5, 7.5, 5.5)), dot(7.5, 7.5, 2),
            line(seg(16, 5.5, 21.5, 5.5)), line(seg(16, 9.5, 21.5, 9.5)),
            sq(2.5, 15, 3, 3, k), line(seg(9, 16.5, 21.5, 16.5)),
            sq(2.5, 19, 3, 3, k), line(seg(9, 20.5, 17, 20.5))]


@icon("scenario-analysis", CAT, "Line that splits into three dashed paths: upper, middle and lower",
      tags=["scenario", "what if", "forecast", "best case", "worst case", "planning"])
def _(S):
    out = [line(seg(2, 12, 8, 12)), dot(8, 12, 1.75)]
    for y in (3.5, 12, 20.5):
        out += dashed(8, 12, 21.5, y, 2, 2, start=3)
    return out


_WALKS = [
    [(3, 12), (7, 8.5), (10, 9.5), (14, 5.5), (17, 6.5), (21, 3)],
    [(3, 12), (7.5, 12.5), (11, 11), (14.5, 13), (18, 11.5), (21, 12.5)],
    [(3, 12), (7, 15.5), (10, 14.5), (13.5, 18.5), (17, 17.5), (21, 21)],
]


@icon("monte-carlo-simulation", CAT, "Random paths fanning out from one starting point",
      tags=["monte carlo", "simulation", "random walk", "probability", "risk", "forecast"])
def _(S):
    return [*[line(poly(w, r=S.r * 0.4)) for w in _WALKS], dot(3, 12, 2)]


def _letter_s(cx, cy, h=7.0, w=5.0):
    r = h / 4
    x0, x1 = cx - w / 2, cx + w / 2
    return (f"M{fmt(x1)} {fmt(cy - h / 2 + 0.6)}C{fmt(x1 - 1)} {fmt(cy - h / 2)} {fmt(x0)} {fmt(cy - h / 2 - 0.4)} {fmt(x0)} {fmt(cy - r)}"
            f"C{fmt(x0)} {fmt(cy + 0.2)} {fmt(x1)} {fmt(cy - 0.2)} {fmt(x1)} {fmt(cy + r)}"
            f"C{fmt(x1)} {fmt(cy + h / 2 + 0.4)} {fmt(x0 + 1)} {fmt(cy + h / 2)} {fmt(x0)} {fmt(cy + h / 2 - 0.6)}")


@icon("swot-matrix", CAT, "Two by two grid with the letters S, W, O and T",
      tags=["swot", "strengths", "weaknesses", "opportunities", "threats", "strategy"])
def _(S):
    return [line(seg(12, 2, 12, 22)), line(seg(2, 12, 22, 12)),
            line(_letter_s(6.5, 6.25, 6.5, 5)),
            line(poly([(14.75, 3), (16, 9.5), (17.5, 5.5), (19, 9.5), (20.25, 3)], r=S.r * 0.3)),
            line(ellipse(6.5, 17.75, 2.75, 3.25)),
            line(seg(14.5, 14.5, 20.5, 14.5)), line(seg(17.5, 14.5, 17.5, 21))]


@icon("risk-matrix", CAT, "Three by three grid shaded more heavily toward the top right",
      tags=["risk matrix", "risk assessment", "likelihood", "impact", "probability", "heat grid"])
def _(S):
    out = [shell(rect(3, 3, 18, 18, S.R)),
           detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)), detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15))]
    R = S.R
    out.append(Part("dot", f"M15 3H{fmt(21 - R)}A{fmt(R)} {fmt(R)} 0 0 1 21 {fmt(3 + R)}V9H15Z"))
    out += [dot(12, 6, 1.25), dot(18, 12, 1.25)]
    return out


@icon("chart-cycle-diagram", CAT, "Four curved arrows chasing each other round a circle",
      tags=["cycle diagram", "cycle", "process loop", "continuous improvement", "lifecycle", "iteration"])
def _(S):
    out = []
    for a in (-90, 0, 90, 180):
        a0, a1 = a + 14, a + 70
        out.append(line(arc(12, 12, 8.5, a0, a1)))
        tip = polar(12, 12, 8.5, a1 + 4)
        out.append(head_to(S, tip, a1 + 4 + 90, 2.75))
    return out


# ============================================================================ reports and monitoring

@icon("infographic", CAT, "Tall page with a pie chart, text lines and a row of bars",
      tags=["infographic", "visual report", "poster", "data story", "summary", "chart"])
def _(S):
    pie = poly([(8.5, 7.5), *[polar(8.5, 7.5, 3, a) for a in range(0, 271, 15)]], closed=True)
    return [shell(rect(3.5, 2, 17, 20, rr(S, 3))), Part("dot", pie),
            detail(seg(14, 5.5, 17, 5.5)), detail(seg(14, 9.5, 17, 9.5)),
            detail(seg(8, 18.5, 8, 16)), detail(seg(12, 18.5, 12, 13.5)), detail(seg(16, 18.5, 16, 15))]


@icon("annual-report", CAT, "Bound report with a bar chart on its cover and a ribbon bookmark",
      tags=["annual report", "yearly report", "financial report", "booklet", "results", "company report"])
def _(S):
    return [shell(rect(4, 2, 16, 20, rr(S, 2.5))), detail(seg(7.5, 2, 7.5, 22)),
            Part("dot", poly([(14.5, 2), (18, 2), (18, 8), (16.25, 6.5), (14.5, 8)], closed=True, r=L(S, 0, 0.4))),
            detail(seg(11, 18.5, 11, 15)), detail(seg(14.25, 18.5, 14.25, 12)), detail(seg(17.5, 18.5, 17.5, 13.5))]


@icon("live-data", CAT, "Pulse line ending in a dot that sends out broadcast arcs",
      tags=["live", "real time", "streaming data", "pulse", "live feed", "monitoring"])
def _(S):
    return [line(poly([(2, 14), (5, 14), (7, 9), (10, 19), (12, 14), (14, 14)], r=S.r * 0.4)),
            dot(17, 14, 2), line(arc(17, 14, 5, 210, 330))]


@icon("monitoring-wall", CAT, "Wall of four screens on a stand, each with a small chart",
      tags=["monitoring", "video wall", "control room", "dashboards", "noc", "screens"])
def _(S):
    k = rr(S, 1.5)
    out = []
    for x, y in ((2, 2), (13, 2), (2, 10.5), (13, 10.5)):
        out.append(shell(rect(x, y, 9, 6.5, k)))
    out += [detail(poly([(4.5, 6.5), (6.5, 4.75), (8.5, 6.5)], r=S.r * 0.3)),
            detail(seg(16, 6.5, 16, 5)), detail(seg(19, 6.5, 19, 4.5)),
            detail(seg(4.5, 13.75, 8.5, 13.75)),
            detail(poly([(15.5, 15), (17.5, 13), (19.5, 13)], r=S.r * 0.3)),
            line(seg(12, 17, 12, 21)), line(seg(7, 21.5, 17, 21.5))]
    return out


# ============================================================================ data structures

@icon("metadata", CAT, "Document with a label tag tied to it by a string",
      tags=["metadata", "tags", "properties", "attributes", "file info", "labels"])
def _(S):
    doc = [(2.5, 2), (8.5, 2), (12, 5.5), (12, 17.5), (2.5, 17.5)]
    tag = [(18.25, 10.5), (21.5, 13.5), (21.5, 21.5), (15, 21.5), (15, 13.5)]
    return [shell(poly(doc, closed=True, r=S.r)), detail(seg(5.5, 10, 9, 10)), detail(seg(5.5, 13.5, 8, 13.5)),
            shell(poly(tag, closed=True, r=S.r * 0.5)), dot(18.25, 14.5, 1.1),
            line("M18.25 10.5C18.25 7.5 17 5.5 14.5 5.5")]


@icon("array-data", CAT, "Row of adjoining cells with index marks beneath each one",
      tags=["array", "list", "index", "data structure", "vector", "elements"])
def _(S):
    out = [shell(rect(2, 7, 20, 6.5, rr(S, 1.5)))]
    out += [detail(seg(x, 7, x, 13.5)) for x in (6, 10, 14, 18)]
    out += [line(seg(x, 17, x, 19)) for x in (4, 8, 12, 16, 20)]
    return out


_DG = {"a": (5, 5), "b": (19, 5), "c": (5, 19), "d": (19, 19)}


def _edge_pts(p, q, cut):
    d = math.dist(p, q)
    ux, uy = (q[0] - p[0]) / d, (q[1] - p[1]) / d
    return (p[0] + ux * cut, p[1] + uy * cut), (q[0] - ux * cut, q[1] - uy * cut)


@icon("directed-graph", CAT, "Four nodes joined by one-way arrows",
      tags=["directed graph", "digraph", "nodes", "edges", "dependencies", "network"])
def _(S):
    out = [line(circle(x, y, 2.25)) for x, y in _DG.values()]
    for a, b in (("a", "b"), ("b", "d"), ("a", "c"), ("c", "d")):
        p, q = _edge_pts(_DG[a], _DG[b], 4.25)
        out += arrow(S, *p, *q, 2.5)
    return out


@icon("ring-buffer", CAT, "Ring split into segments, some full, with an arrow at the write position",
      tags=["ring buffer", "circular buffer", "queue", "data structure", "cyclic", "memory"])
def _(S):
    out = [line(circle(12, 12, 9)), line(circle(12, 12, 4.5))]
    out += [line(seg(*polar(12, 12, 4.5, a), *polar(12, 12, 9, a))) for a in range(-90, 270, 60)]
    for a in (-90, -30):
        pts = [*[polar(12, 12, 9, a + t) for t in range(0, 61, 10)], *[polar(12, 12, 4.5, a + 60 - t) for t in range(0, 61, 20)]]
        out.append(Part("dot", poly(pts, closed=True)))
    tip = polar(12, 12, 3.4, 60)
    out.append(solid(poly([tip, polar(12, 12, 2.6, 60 + 130), polar(12, 12, 2.6, 60 - 130)], closed=True, r=L(S, 0, 1.1))))
    return out


# ============================================================================ storage

_H = 9.5
_HEX = [polar(12, 12, _H, a) for a in (-90, -30, 30, 90, 150, 210)]


def _mid(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


@icon("olap-cube", CAT, "Cube split into smaller blocks on each face, with one slice picked out",
      tags=["olap", "data cube", "multidimensional", "slice and dice", "dimensions", "business intelligence"])
def _(S):
    t, ur, lr, b, ll, ul = _HEX
    c = (12, 12)
    out = [shell(poly(_HEX, closed=True, r=S.r)),
           detail(poly([ul, c, ur], r=S.r * 0.4)), detail(seg(*c, *b))]
    out += [detail(seg(*_mid(t, ul), *_mid(c, ur))), detail(seg(*_mid(t, ur), *_mid(c, ul))),
            detail(seg(*_mid(ul, c), *_mid(ll, b))), detail(seg(*_mid(ul, ll), *_mid(c, b))),
            detail(seg(*_mid(ur, c), *_mid(lr, b))), detail(seg(*_mid(ur, lr), *_mid(c, b)))]
    return out


@icon("data-warehouse", CAT, "Warehouse building with a database cylinder in its doorway",
      tags=["data warehouse", "dwh", "analytics store", "enterprise data", "database", "storage"])
def _(S):
    out, top, band = cyl_d(S, 7.5, 10.5, 9, 10.5, 1.75)
    return [shell(poly([(2, 21), (2, 9.5), (12, 3.5), (22, 9.5), (22, 21)], closed=True, r=S.r)),
            detail(out), detail(top), detail(band(16))]


@icon("data-silo", CAT, "Tall farm silo with a domed top, banded like stacked database discs",
      tags=["data silo", "isolated data", "siloed", "fragmented data", "department data", "storage"])
def _(S):
    r = L(S, 0, 2)
    body = (f"M6.5 9A5.5 5.5 0 0 1 17.5 9V{fmt(21 - r)}" + (f"A{r} {r} 0 0 1 {fmt(17.5 - r)} 21" if r else "")
            + f"H{fmt(6.5 + r)}" + (f"A{r} {r} 0 0 1 6.5 {fmt(21 - r)}" if r else "") + "Z")
    e = 1.5
    return [shell(body), *[detail(f"M6.5 {y}Q12 {y + 2 * e} 17.5 {y}") for y in (9, 13, 17)]]


@icon("graph-database", CAT, "Database cylinder with a small graph of linked nodes on its side",
      tags=["graph database", "nodes", "relationships", "knowledge graph", "network data", "database"])
def _(S):
    out = cylinder(S, 4, 2.5, 16, 19, 2.75)
    a, b, c = (8.5, 12.5), (15.5, 11), (12.5, 17.5)
    out += [detail(seg(*a, *b)), detail(seg(*a, *c)), detail(seg(*b, *c)), dot(*a, 1.75), dot(*b, 1.75), dot(*c, 1.75)]
    return out


# ============================================================================ collecting and preparing

@icon("data-entry", CAT, "Form sheet being filled in above a keyboard",
      tags=["data entry", "typing", "input", "form filling", "keying", "records"])
def _(S):
    return [shell(rect(5, 2, 14, 11, rr(S, 2))), detail(seg(8, 5.5, 16, 5.5)), detail(seg(8, 9, 12, 9)),
            shell(rect(2, 15.5, 20, 6.5, rr(S, 2))), *[dot(x, 18.75, 1) for x in (5.5, 9, 12.5, 16, 19.5)]]


@icon("data-snapshot", CAT, "Database cylinder framed by camera viewfinder corners",
      tags=["snapshot", "backup", "point in time", "capture", "database copy", "restore point"])
def _(S):
    corners = [[(2.5, 7.5), (2.5, 2.5), (7.5, 2.5)], [(16.5, 2.5), (21.5, 2.5), (21.5, 7.5)],
               [(21.5, 16.5), (21.5, 21.5), (16.5, 21.5)], [(7.5, 21.5), (2.5, 21.5), (2.5, 16.5)]]
    return [*[line(poly(c, r=S.r)) for c in corners], *cylinder(S, 7.5, 6.5, 9, 11, 1.75)]


@icon("data-collection", CAT, "Clipboard checklist with data dots dropping in from above",
      tags=["data collection", "gathering", "survey", "field data", "checklist", "records"])
def _(S):
    return [shell(poly([(6, 7.5), (2.5, 7.5), (2.5, 22), (16, 22), (16, 7.5), (12.5, 7.5)], r=S.R)),
            shell(rect(6, 6, 6.5, 3.5, rr(S, 1.5))),
            detail(poly([(5.5, 14), (7, 15.5), (9.5, 13)], r=S.r * 0.3)), detail(seg(11, 14.25, 13, 14.25)),
            detail(seg(5.5, 18.5, 13, 18.5)),
            dot(20.5, 13, 1.25), dot(20.5, 8.5, 1.25), dot(17.5, 3, 1.25)]


def _table(S, x, y, w, h, rows=(), k=1.5):
    return [shell(rect(x, y, w, h, rr(S, k))), *[detail(seg(x, yy, x + w, yy)) for yy in rows]]


@icon("data-split", CAT, "One table dividing into a larger and a smaller table",
      tags=["data split", "train test split", "partition", "subset", "divide data", "sampling"])
def _(S):
    k = L(S, 0, 0.4)
    return [*_table(S, 2, 7, 7, 10, (11.5,)), *_table(S, 16, 2, 6, 10, (6.5,)), *_table(S, 16, 16, 6, 6),
            line(seg(9, 12, 11, 12)), line(poly([(13, 7), (11, 7), (11, 19), (13, 19)], r=S.r)),
            solid(poly([(12.5, 5), (14.5, 7), (12.5, 9)], closed=True, r=k)),
            solid(poly([(12.5, 17), (14.5, 19), (12.5, 21)], closed=True, r=k))]


@icon("missing-data", CAT, "Table with one cell drawn dashed and holding a question mark",
      tags=["missing data", "null", "missing values", "gaps", "incomplete", "data quality"])
def _(S):
    shape = poly([(2, 2), (22, 2), (22, 11), (11, 11), (11, 22), (2, 22)], closed=True, r=S.r * 0.6)
    q = "M14.6 15.25A1.9 1.9 0 1 1 16.5 17.15V18.25"
    return [shell(shape), detail(seg(2, 6.5, 22, 6.5)), detail(seg(11, 2, 11, 11)), detail(seg(2, 16.5, 11, 16.5)),
            line(seg(22, 13.5, 22, 15.5)), line(poly([(22, 19), (22, 22), (19, 22)], r=S.r * 0.6)), line(seg(13.5, 22, 15.5, 22)),
            line(q), dot(16.5, 20.25, 1)]


@icon("pivot-table", CAT, "Table with a header row and column and a two-way arrow at its corner",
      tags=["pivot table", "pivot", "crosstab", "summarize", "spreadsheet", "rotate data"])
def _(S):
    return [shell(rect(8.5, 8.5, 13.5, 13.5, rr(S, 2))), detail(seg(8.5, 13, 22, 13)), detail(seg(13, 8.5, 13, 22)),
            line(f"M4 15V{fmt(L(S, 8, 9))}" + (f"A5 5 0 0 1 9 4" if S.name == "rounded" else "L8 4") + "H15"),
            head_to(S, (4, 16), 90, 2.5), head_to(S, (16, 4), 0, 2.5)]


@icon("freeze-panes", CAT, "Spreadsheet with its top row and first column locked, and a snowflake",
      tags=["freeze panes", "freeze rows", "lock header", "spreadsheet", "sticky header", "scrolling"])
def _(S):
    R = S.R
    band = path_to_d(I(P("M2 2H22V7.5H7.5V22H2Z"), P(rect(2, 2, 20, 20, R))))
    fl = [detail(seg(*polar(15, 15, 4, a), *polar(15, 15, 4, a + 180))) for a in (-90, -30, 30)]
    return [shell(rect(2, 2, 20, 20, R)), Part("dot", band), *fl]


@icon("merge-cells", CAT, "One wide cell with arrows pointing in from both sides",
      tags=["merge cells", "combine cells", "join cells", "spreadsheet", "table", "span"])
def _(S):
    return [shell(rect(2, 6, 20, 12, rr(S, 2.5))), *arrow(S, 4.5, 12, 10.5, 12, 2.5, detail), *arrow(S, 19.5, 12, 13.5, 12, 2.5, detail)]


@icon("split-cells", CAT, "Wide cell divided by a new line with arrows pointing outward",
      tags=["split cells", "divide cells", "unmerge", "spreadsheet", "table", "separate"])
def _(S):
    return [shell(rect(2, 6, 20, 12, rr(S, 2.5))), detail(seg(12, 6, 12, 18)),
            *arrow(S, 9.5, 12, 5.5, 12, 2.5, detail), *arrow(S, 14.5, 12, 18.5, 12, 2.5, detail)]


@icon("conditional-formatting", CAT, "Column of table cells holding data bars of different lengths",
      tags=["conditional formatting", "data bars", "highlight rules", "spreadsheet", "color scale", "cell rules"])
def _(S):
    k = L(S, 0, 1)
    out = [shell(rect(3, 2, 18, 20, rr(S, 2))), detail(seg(3, 8.5, 21, 8.5)), detail(seg(3, 15.5, 21, 15.5))]
    for yc, w in ((5.25, 12), (12, 6.5), (18.75, 9)):
        out.append(sq(5.5, yc - 1.25, w, 2.5, k))
    return out


def _grid(S, x, y, w, h, xs, ys):
    return [shell(rect(x, y, w, h, rr(S, 2.5))), *[detail(seg(xx, y, xx, y + h)) for xx in xs],
            *[detail(seg(x, yy, x + w, yy)) for yy in ys]]


@icon("table-row", CAT, "Table grid with one full row filled in",
      tags=["table row", "row", "record", "select row", "spreadsheet", "highlight row"])
def _(S):
    return [*_grid(S, 2, 4, 20, 16, (8.5, 15.5), (9.5, 14.5)), Part("dot", rect(2, 9.5, 20, 5))]


@icon("table-column", CAT, "Table grid with one full column filled in",
      tags=["table column", "column", "field", "select column", "spreadsheet", "highlight column"])
def _(S):
    return [*_grid(S, 2, 4, 20, 16, (8.5, 15.5), (9.5, 14.5)), Part("dot", rect(8.5, 4, 7, 16))]


@icon("transpose-table", CAT, "Tall one-column table and wide one-row table with a curved arrow between",
      tags=["transpose", "swap rows and columns", "rotate table", "pivot", "spreadsheet", "matrix"])
def _(S):
    k = rr(S, 1.5)
    return [shell(rect(2, 2, 6, 14, k)), detail(seg(2, 6.5, 8, 6.5)), detail(seg(2, 11.5, 8, 11.5)),
            shell(rect(8, 16, 14, 6, k)), detail(seg(12.5, 16, 12.5, 22)), detail(seg(17.5, 16, 17.5, 22)),
            line("M11.5 4.5C16.5 4.5 19.5 7 19.5 12"), head_to(S, (19.5, 12.5), 90, 2.5), head_to(S, (11, 4.5), 180, 2.5)]


@icon("spreadsheet-cell", CAT, "Grid with one selected cell framed in bold and a fill handle at its corner",
      tags=["cell", "selected cell", "fill handle", "spreadsheet", "active cell", "autofill"])
def _(S):
    frame = path_to_d(D(P(rect(7, 7, 10, 10, L(S, 0, 1.5))), P(rect(10, 10, 4, 4))))
    return [*_grid(S, 2, 2, 20, 20, (8.5, 15.5), (8.5, 15.5)), Part("dot", frame),
            Part("dot", rect(15.5, 15.5, 4, 4, L(S, 0, 1)))]


@icon("workbook-tabs", CAT, "Spreadsheet grid above a row of sheet tabs, the first one active",
      tags=["workbook", "sheet tabs", "worksheets", "spreadsheet", "tabs", "sheets"])
def _(S):
    k = S.r * 0.5
    return [*_grid(S, 2, 2, 20, 14, (8.5, 15.5), (9,)),
            sq(2, 18, 6.5, 4, L(S, 0, 1.25)),
            line(poly([(10.5, 18), (10.5, 21.5), (15, 21.5), (15, 18)], r=k)),
            line(poly([(17.5, 18), (17.5, 21.5), (22, 21.5), (22, 18)], r=k))]


# ============================================================================ sorting

def _letter_a(x, y, w, h):
    return [(x, y + h), (x + w / 2, y), (x + w, y + h)]


@icon("sort-alphabetical", CAT, "Letters A over Z beside a downward arrow",
      tags=["sort a to z", "alphabetical", "ascending", "order", "sort by name", "a-z"])
def _(S):
    return [*arrow(S, 5, 3, 5, 20.5, 3),
            line(poly(_letter_a(11.5, 3.5, 8, 7), r=S.r * 0.3)), line(seg(13.25, 8, 17.75, 8)),
            line(poly([(12, 14), (19.5, 14), (12, 21.5), (19.5, 21.5)], r=S.r * 0.3))]


@icon("sort-numeric", CAT, "Numbers 1 over 9 beside a downward arrow",
      tags=["sort numbers", "numeric", "ascending", "order", "sort by number", "1-9"])
def _(S):
    nine = "M19.5 17.25A3 3 0 1 1 19.5 17.1V19C19.5 21 18 22 16 22H14.5"
    return [*arrow(S, 5, 3, 5, 20.5, 3),
            line(poly([(13, 4), (15.5, 2.5), (15.5, 10.5)], r=S.r * 0.3)), line(seg(12.5, 10.5, 18.5, 10.5)),
            line(circle(15.75, 16, 3)), line("M18.75 16C18.75 19.5 17.5 21.5 14 21.5")]


# ============================================================================ pipelines

def cog(S, cx, cy, r_in, r_out, n=8, hole=1.25):
    """Small gear: trapezoid teeth around a disc, with a round hole."""
    pts = []
    step = 360 / n
    for i in range(n):
        a = -90 + i * step
        pts += [polar(cx, cy, r_in, a - step * 0.38), polar(cx, cy, r_out, a - step * 0.2),
                polar(cx, cy, r_out, a + step * 0.2), polar(cx, cy, r_in, a + step * 0.38)]
    return [shell(poly(pts, closed=True, r=S.r * 0.25), stroke_miterlimit="2"), dot(cx, cy, hole)]


@icon("data-flow-diagram", CAT, "Source box, process circle and open-ended data store joined by arrows",
      tags=["data flow diagram", "dfd", "process", "data store", "system design", "flowchart"])
def _(S):
    return [shell(rect(2, 4, 6, 5.5, rr(S, 1.5))), shell(circle(16.5, 6.75, 4)),
            *arrow(S, 8, 6.75, 11.25, 6.75, 2.25),
            *arrow(S, 16.5, 11.75, 16.5, 14.75, 2.25),
            line(poly([(21, 16), (7, 16), (7, 21.5), (21, 21.5)], r=S.r))]


@icon("etl-process", CAT, "Source and target databases with a gear and an arrow between them",
      tags=["etl", "extract transform load", "data pipeline", "transform", "integration", "elt"])
def _(S):
    return [*cylinder(S, 2, 8.5, 5.5, 13, 1.4), *cylinder(S, 16.5, 8.5, 5.5, 13, 1.4),
            *cog(S, 12, 6, 2.6, 3.8, 8, 1), *arrow(S, 9, 17, 14.75, 17, 2.25)]


@icon("data-integration", CAT, "Lines from two small databases merging into one larger database",
      tags=["data integration", "combine sources", "merge data", "consolidate", "pipeline", "unify"])
def _(S):
    return [*cylinder(S, 2, 2, 6, 7, 1.4), *cylinder(S, 2, 15, 6, 7, 1.4), *cylinder(S, 15, 5, 7, 14, 1.6),
            line(poly([(8, 5.5), (10.5, 5.5), (10.5, 18.5), (8, 18.5)], r=S.r)), line(seg(10.5, 12, 12, 12)),
            solid(poly([(12, 10), (14, 12), (12, 14)], closed=True, r=L(S, 0, 0.4)))]


@icon("data-migration", CAT, "Arrow arching from one database cylinder over to another",
      tags=["data migration", "move data", "transfer", "database migration", "copy", "move"])
def _(S):
    return [*cylinder(S, 2, 10, 7, 11.5, 1.6), *cylinder(S, 15, 10, 7, 11.5, 1.6),
            line("M5.5 7.5C5.5 1.5 18.5 1.5 18.5 6.5"), head_to(S, (18.5, 7.5), 90, 2.5)]


@icon("data-sync", CAT, "Two database cylinders joined by arrows running in both directions",
      tags=["data sync", "synchronization", "replication", "two way sync", "mirror", "database"])
def _(S):
    return [*cylinder(S, 2, 7.5, 7, 9, 1.5), *cylinder(S, 15, 7.5, 7, 9, 1.5),
            line("M5.5 5C6 1.75 18 1.75 18.5 4.5"), head_to(S, (18.5, 5.25), 85, 2.25),
            line("M18.5 19C18 22.25 6 22.25 5.5 19.5"), head_to(S, (5.5, 18.75), -95, 2.25)]


@icon("data-aggregation", CAT, "Several small points joined by lines into one larger point",
      tags=["aggregation", "aggregate", "combine", "roll up", "summarize", "group by"])
def _(S):
    ys = (3.5, 9.25, 14.75, 20.5)
    out = [dot(3.5, y, 1.5) for y in ys]
    out += [line(seg(5.5, y, 15, 12 + (y - 12) * 0.2)) for y in ys]
    return out + [shell(circle(18, 12, 3.25))]


@icon("data-ingestion", CAT, "Wide funnel over a database with data dots dropping into it",
      tags=["data ingestion", "ingest", "import data", "intake", "pipeline", "load"])
def _(S):
    return [dot(8, 3, 1.25), dot(12, 3, 1.25), dot(16, 3, 1.25),
            shell(poly([(3, 6.5), (21, 6.5), (14, 11.5), (10, 11.5)], closed=True, r=S.r * 0.5)),
            *cylinder(S, 5, 14, 14, 8, 1.75)]


@icon("data-hub", CAT, "Database cylinder in the centre with spokes out to four nodes",
      tags=["data hub", "central data", "hub and spoke", "data platform", "integration hub", "connected"])
def _(S):
    out = cylinder(S, 8.5, 8, 7, 8, 1.4)
    out += [line(seg(12, 6.5, 12, 4.5)), line(seg(12, 17.5, 12, 19.5)), line(seg(7, 12, 5, 12)), line(seg(17, 12, 19, 12))]
    out += [dot(12, 3, 1.75), dot(12, 21, 1.75), dot(3, 12, 1.75), dot(21, 12, 1.75)]
    return out


@icon("data-mesh", CAT, "Grid of small blocks, each linked to its neighbours",
      tags=["data mesh", "decentralized data", "domains", "federated", "architecture", "data products"])
def _(S):
    k = L(S, 0, 1)
    c = (4, 12, 20)
    out = [sq(x - 2, y - 2, 4, 4, k) for x in c for y in c]
    for y in c:
        out += [line(seg(6, y, 10, y)), line(seg(14, y, 18, y))]
    for x in c:
        out += [line(seg(x, 6, x, 10)), line(seg(x, 14, x, 18))]
    return out


@icon("batch-processing", CAT, "Stack of three boxes with an arrow feeding them into a gear",
      tags=["batch processing", "batch job", "bulk", "scheduled job", "pipeline", "queue"])
def _(S):
    k = rr(S, 1.25)
    return [shell(rect(2, 3, 6, 4.5, k)), shell(rect(2, 9.75, 6, 4.5, k)), shell(rect(2, 16.5, 6, 4.5, k)),
            *arrow(S, 9.5, 12, 12.75, 12, 2), *cog(S, 18, 12, 2.9, 4, 8, 1.1)]
