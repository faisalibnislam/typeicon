"""TypeIcon Core: finance & business.

Generic signs and objects only: no bank, card network, payment provider or cryptocurrency logo.
Finance takes the full variant badge set in the bottom-right (box 13–23), so identifying details sit
top/left where the object allows. Currency signs are symbols and take no badges (modifiers="none").
Charts reuse the axes of the charts category (3,3 → 3,21 → 21,21).
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import SCALE, fmt, path_to_d, polar

CAT = "finance"
AXES = [(3, 3), (3, 21), (21, 21)]


# ============================================================================ helpers

def rr(S, cap=None):
    """Container corner radius for the style, optionally capped for small shapes."""
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def axes(S):
    return line(poly(AXES, r=S.r))


def head(tip, deg, size=2.5):
    """Open arrowhead at tip; deg is the direction the arrow points (0 = right, 90 = down)."""
    a = polar(tip[0], tip[1], size * math.sqrt(2), deg + 180 - 45)
    b = polar(tip[0], tip[1], size * math.sqrt(2), deg + 180 + 45)
    return [a, tip, b]


def pct(cx, cy, k=3.0, r=1.25):
    """Percent sign: two dots and a slash, sized so the dots clear the slash by 2 px."""
    a = k + 0.75
    return [dot(cx - k, cy - k, r), dot(cx + k, cy + k, r), detail(seg(cx + a, cy - a, cx - a, cy + a))]


def arc_avoid(cx, cy, r, keep_out, step=0.5):
    """Longest arc of circle (cx, cy, r) whose points lie outside a pathops region (grid units)."""
    n = int(360 / step)
    ok = [not keep_out.contains(tuple(v * SCALE for v in polar(cx, cy, r, i * step))) for i in range(n)]
    best, start = (0, 0), None
    for i in range(2 * n):
        if ok[i % n]:
            start = i if start is None else start
            if i - start > best[1] - best[0]:
                best = (start, i)
        else:
            start = None
    return arc(cx, cy, r, best[0] * step, best[1] * step)


def runs_outside(pts, keep_out, n=200):
    """Pieces of the polyline pts that lie outside a pathops region, as d-strings."""
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        cur = []
        for i in range(n + 1):
            t = i / n
            p = (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)
            if keep_out.contains((p[0] * SCALE, p[1] * SCALE)):
                if len(cur) > 1:
                    out.append(cur)
                cur = []
            else:
                cur.append(p)
        if len(cur) > 1:
            out.append(cur)
    # merge runs that continue across a polyline corner
    merged = []
    for r in out:
        if merged and math.dist(merged[-1][-1], r[0]) < 1e-6:
            merged[-1] = merged[-1] + r[1:]
        else:
            merged.append(r)
    return merged


def transformed_d(d, deg, dx, dy):
    """Rotate a closed d-string about the origin by deg (clockwise on screen) and move it by (dx, dy)."""
    from geometry import transform_path
    a = math.radians(deg)
    c, s_ = math.cos(a), math.sin(a)
    return path_to_d(transform_path(P(d), (c, s_, -s_, c, dx, dy)))


def tp(pt, deg, dx, dy):
    a = math.radians(deg)
    c, s_ = math.cos(a), math.sin(a)
    return (pt[0] * c - pt[1] * s_ + dx, pt[0] * s_ + pt[1] * c + dy)


def union_d(*ds):
    """Outline of the union of closed shapes (grid-unit d-strings)."""
    return path_to_d(U(*(P(d) for d in ds)))


def bar(S, x, y0, y1):
    """Vertical bar of a currency sign: butt ends reach further in Line, round caps in Rounded."""
    return line(seg(x, y0, x, y1) if S.name == "line" else seg(x, y0 + 0.5, x, y1 - 0.5))


# ============================================================================ currency signs

@icon("dollar", CAT, "Dollar sign", tags=["usd", "money", "currency", "price", "cost", "cash"],
      aliases=["usd", "dollar-sign"], modifiers="none")
def _(S):
    s = ("M16.5 7.75C16.1 5.8 14.4 4.5 12 4.5C9.3 4.5 7.5 5.9 7.5 8C7.5 10.2 9.4 11.1 12 11.75"
         "C14.7 12.4 16.5 13.5 16.5 15.9C16.5 18.1 14.6 19.5 12 19.5C9.3 19.5 7.6 18.2 7.25 16.25")
    return [line(s), bar(S, 12, 2, 22)]


@icon("euro", CAT, "Euro sign", tags=["eur", "money", "currency", "europe", "price", "cash"],
      aliases=["eur", "euro-sign"], modifiers="none")
def _(S):
    return [line(arc(13.5, 12, 7.5, 42, 318)), line(seg(4, 10, 13, 10)), line(seg(4, 14, 12, 14))]


@icon("pound", CAT, "Pound sterling sign", tags=["gbp", "sterling", "money", "currency", "uk", "price"],
      aliases=["gbp", "pound-sterling"], modifiers="none")
def _(S):
    stem = "M17 7.25C16.5 5.4 15 4.5 13.25 4.5C11 4.5 9.5 6 9.5 8.5V14.5C9.5 17 8.75 18.6 6.5 19.5H17.5"
    return [line(stem), line(seg(6.5, 12, 14, 12))]


@icon("yen", CAT, "Yen sign, also used for the yuan", tags=["jpy", "yuan", "cny", "money", "currency", "japan"],
      aliases=["jpy", "yuan"], modifiers="none")
def _(S):
    return [
        line(poly([(6, 3.5), (12, 11.5), (18, 3.5)], r=S.r), stroke_miterlimit="2"),
        bar(S, 12, 11.5, 21),
        line(seg(7, 13.5, 17, 13.5)), line(seg(7, 17.5, 17, 17.5)),
    ]


@icon("rupee", CAT, "Indian rupee sign", tags=["inr", "india", "money", "currency", "price", "cash"],
      aliases=["inr", "rupee-sign"], modifiers="none")
def _(S):
    return [
        line(seg(6.5, 4, 17.5, 4)), line(seg(6.5, 8.5, 17.5, 8.5)),
        line("M9 4A4.5 4.5 0 0 1 9 13H7L15.5 21", stroke_miterlimit="2"),
    ]


# ============================================================================ money

@icon("crypto-coin", CAT, "Coin marked with a cube; a generic cryptocurrency or token",
      tags=["cryptocurrency", "token", "blockchain", "digital currency", "coin", "web3"], aliases=["cryptocurrency"])
def _(S):
    hexa = [polar(12, 12, 4.75, -90 + i * 60) for i in range(6)]
    c = (12, 12)
    return [
        shell(circle(12, 12, 9)),
        detail(poly(hexa, closed=True, r=0 if S.name == "line" else 2)),
        detail(poly([hexa[5], c, hexa[1]], r=S.r)),
        detail(seg(12, 12, *hexa[3]) if S.name == "line" else seg(12, 12, 12, 15.5)),
    ]


@icon("currency-exchange", CAT, "Two coins swapping places along curved arrows; currency exchange",
      tags=["exchange rate", "forex", "convert", "swap", "money", "transfer"], aliases=["forex"])
def _(S):
    return [
        shell(circle(7, 7, 4)), dot(7, 7, 1.25),
        shell(circle(17, 17, 4)), dot(17, 17, 1.25),
        line("M13.5 4.5H16A3 3 0 0 1 19 7.5V9.5"),
        line(poly(head((19, 10.5), 90, 2), r=S.r * 0.5)),
        line("M10.5 19.5H8A3 3 0 0 1 5 16.5V14.5"),
        line(poly(head((5, 13.5), -90, 2), r=S.r * 0.5)),
    ]


# ============================================================================ charts

@icon("chart-line", CAT, "Line chart: a smooth curve over two axes",
      tags=["line graph", "trend", "time series", "statistics", "analytics", "graph"], aliases=["line-chart"])
def _(S):
    return [axes(S), line("M7 16C9.5 16 9.5 9 12 9C14.5 9 14.25 13 16.5 13C18.5 13 18.75 7.5 20.5 6.5")]


@icon("chart-pie", CAT, "Pie chart with one slice pulled out",
      tags=["pie graph", "proportion", "share", "percentage", "breakdown", "statistics"], aliases=["pie-chart"])
def _(S):
    return [
        shell("M10 7A7 7 0 1 0 17 14H10Z"),
        shell("M14 3A7 7 0 0 1 21 10H14Z"),
    ]


@icon("chart-area", CAT, "Area chart: a shaded region rising over two axes",
      tags=["area graph", "volume", "trend", "cumulative", "statistics", "graph"], aliases=["area-chart"])
def _(S):
    area = [(7, 17), (7, 12.5), (10.5, 9), (14, 12.5), (20, 6.5), (20, 17)]
    return [axes(S), shell(poly(area, closed=True, r=S.r))]


@icon("chart-candlestick", CAT, "Candlestick chart: three candles with wicks, one solid",
      tags=["candlestick", "stock chart", "trading", "ohlc", "market", "price action"], aliases=["candlestick-chart"])
def _(S):
    cap = 0 if S.name == "line" else 1
    return [
        line(seg(5, 5.5, 5, 10)), shell(rect(3, 10, 4, 6, cap)), line(seg(5, 16, 5, 20)),
        line(seg(12, 3, 12, 5)), sq(10.5, 5, 3, 8, cap * 0.75), line(seg(12, 13, 12, 17)),
        line(seg(19, 3, 19, 6)), shell(rect(17, 6, 4, 5, cap)), line(seg(19, 11, 19, 14)),
    ]


@icon("stock-up", CAT, "Rising price line ending in an arrow over two axes; a stock gaining",
      tags=["stocks", "market up", "gain", "bull", "increase", "growth"], aliases=["stocks-up"])
def _(S):
    return [
        axes(S),
        line(poly([(7, 15), (10.5, 11.5), (13, 14), (19.5, 7.5)], r=S.r)),
        line(poly(head((20, 7), -45, 3), r=S.r * 0.5)),
    ]


@icon("stock-down", CAT, "Falling price line ending in an arrow over two axes; a stock losing",
      tags=["stocks", "market down", "loss", "bear", "decrease", "decline"], aliases=["stocks-down"])
def _(S):
    return [
        axes(S),
        line(poly([(7, 6), (10.5, 9.5), (13, 7), (19.5, 13.5)], r=S.r)),
        line(poly(head((20, 14), 45, 3), r=S.r * 0.5)),
    ]


# ============================================================================ planning

@icon("budget", CAT, "Envelope with a banknote sticking out; money set aside",
      tags=["budgeting", "allowance", "envelope", "spending plan", "cash", "salary"], aliases=["money-envelope"])
def _(S):
    return [
        line(poly([(6.5, 10), (6.5, 3), (17.5, 3), (17.5, 10)], r=S.r)),
        dot(12, 6.5, 1.25),
        shell(rect(3, 10, 18, 11, rr(S, 3))),
        detail(poly([(3.5, 10.5), (12, 16), (20.5, 10.5)], r=S.r)),
    ]


PAGE = [(5, 2.5), (14, 2.5), (19, 7.5), (19, 21.5), (5, 21.5)]
FOLD = [(14, 2.5), (14, 7.5), (19, 7.5)]


def page(S):
    """Document page with a folded corner, matching the files category."""
    return [shell(poly(PAGE, closed=True, r=S.r)), detail(poly(FOLD, r=S.r * 0.5))]


@icon("tax", CAT, "Document page with a percent sign; a tax form or rate",
      tags=["taxes", "tax form", "vat", "tax return", "percent", "duty"], aliases=["tax-form"])
def _(S):
    return [*page(S), *pct(12, 14.5)]


@icon("loan", CAT, "Open hand with a coin above it; lending or borrowing money",
      tags=["borrow", "lend", "credit", "mortgage", "debt", "finance"], aliases=["lending"])
def _(S):
    hand = ("M6 14H10C11.4 14 12.5 15.1 12.5 16.5H15.5L19.3 14.6C20.4 14 21.6 15.2 20.8 16.2"
            "L17 20.2C16.5 20.7 15.8 21 15 21H6Z")
    return [
        sq(2, 13, 2.5, 9, 0 if S.name == "line" else 1),
        shell(hand if S.name == "line" else hand),
        detail(seg(8.5, 17.5, 12.5, 17.5)),
        shell(circle(15, 7, 4)), dot(15, 7, 1.25),
    ]


@icon("briefcase", CAT, "Briefcase with a handle and a clasp",
      tags=["business", "work", "job", "office", "case", "career"], aliases=["attache-case"])
def _(S):
    return [
        line(poly([(9, 7), (9, 4), (15, 4), (15, 7)], r=S.r)),
        shell(rect(3, 7, 18, 13, rr(S))),
        detail(seg(3, 12.5, 10, 12.5)), detail(seg(14, 12.5, 21, 12.5)),
        sq(10.5, 11, 3, 3, 0 if S.name == "line" else 0.75),
    ]


@icon("portfolio", CAT, "Briefcase with a small bar chart on it; an investment portfolio",
      tags=["investments", "holdings", "assets", "allocation", "diversification", "wealth"], aliases=["investment-portfolio"])
def _(S):
    return [
        line(poly([(9, 7), (9, 4), (15, 4), (15, 7)], r=S.r)),
        shell(rect(3, 7, 18, 13, rr(S))),
        detail(seg(8, 16.5, 8, 13.5)), detail(seg(12, 16.5, 12, 10.5)), detail(seg(16, 16.5, 16, 12)),
    ]


# ============================================================================ valuables

@icon("gold-bar", CAT, "Three gold ingots stacked in a pyramid",
      tags=["gold", "bullion", "ingot", "precious metal", "wealth", "reserve"], aliases=["bullion"])
def _(S):
    def ingot(x0, x1, y0, y1, inset=1.5):
        return shell(poly([(x0 + inset, y0), (x1 - inset, y0), (x1, y1), (x0, y1)], closed=True, r=S.r * 0.5))
    return [ingot(7, 17, 5.5, 11), ingot(3, 11, 15, 20.5), ingot(13, 21, 15, 20.5)]


# ============================================================================ office and meetings

@icon("presentation", CAT, "Projection screen on a stand showing a rising chart",
      tags=["slideshow", "slides", "pitch", "keynote", "projector screen", "talk"], aliases=["projector-screen"])
def _(S):
    return [
        line(seg(2, 3.5, 22, 3.5) if S.name == "line" else seg(3, 3.5, 21, 3.5)),
        shell(rect(4, 3.5, 16, 11.5, rr(S, 2.5))),
        detail(poly([(7.5, 11.5), (10.5, 8.5), (13, 10.5), (16.5, 7)], r=S.r)),
        line(seg(12, 15, 12, 17.5)),
        line(poly([(8, 21), (12, 17.5), (16, 21)], r=S.r)),
    ]


@icon("whiteboard", CAT, "Wall whiteboard with a scribble and a marker tray",
      tags=["dry-erase board", "board", "brainstorm", "classroom", "meeting room", "markers"], aliases=["dry-erase-board"])
def _(S):
    return [
        shell(rect(3, 3, 18, 13, rr(S))),
        detail("M7 11C8 8 9.5 7.5 10.5 9.5C11.5 11.5 13 11.5 14 9C14.6 7.6 15.5 7.2 17 7.5"),
        line(seg(5, 20, 19, 20)),
    ]


@icon("flip-chart", CAT, "Flip chart: a paper pad clamped to an easel",
      tags=["flipchart", "easel", "workshop", "brainstorm", "training", "paper pad"], aliases=["flipchart"])
def _(S):
    return [
        line(seg(3, 4, 21, 4)),
        shell(rect(5, 4, 14, 12, rr(S, 2.5))),
        detail(seg(8, 8.5, 16, 8.5)), detail(seg(8, 12, 13, 12)),
        line(seg(8, 16, 6.5, 21)), line(seg(16, 16, 17.5, 21)), line(seg(12, 16, 12, 21)),
    ]


@icon("meeting", CAT, "Three people seated behind a table",
      tags=["team meeting", "conference", "discussion", "board meeting", "group", "colleagues"], aliases=["conference"])
def _(S):
    return [
        shell(circle(12, 5.5, 2.5)),
        line("M8 14.5V14A4 4 0 0 1 16 14"),
        shell(circle(5, 8.5, 2)), line("M2.5 14.5A3 3 0 0 1 5.5 12"),
        shell(circle(19, 8.5, 2)), line("M21.5 14.5A3 3 0 0 0 18.5 12"),
        line(seg(2, 17.5, 22, 17.5) if S.name == "line" else seg(3, 17.5, 21, 17.5)),
        line(seg(6, 17.5, 6, 21)), line(seg(18, 17.5, 18, 21)),
    ]


@icon("stapler", CAT, "Desk stapler seen from the side",
      tags=["staple", "office", "stationery", "fasten", "paper", "desk"])
def _(S):
    arm = ("M3.5 11V9A3 3 0 0 1 6.5 6H16.5C18.5 6 20 7.5 20.5 11Z" if S.name == "line" else
           "M5 11A1.5 1.5 0 0 1 3.5 9.5V9A3 3 0 0 1 6.5 6H16.5C18.5 6 20 7.5 20.4 10.2A0.7 0.7 0 0 1 19.7 11Z")
    return [
        shell(arm),
        line(seg(5.5, 11, 5.5, 16)),
        shell(rect(3, 16, 18, 3.5, rr(S, 1.75))),
    ]


@icon("org-chart", CAT, "Organisation chart: a manager linked to two team members",
      tags=["organization chart", "org structure", "team", "reporting line", "management", "company"],
      aliases=["organization-chart"])
def _(S):
    return [
        dot(12, 4.25, 2.25),
        line("M8.5 11.5A3.5 3.5 0 0 1 15.5 11.5"),
        line(poly([(5.5, 17), (5.5, 14.5), (18.5, 14.5), (18.5, 17)], r=S.r)),
        dot(5.5, 19.75, 2), dot(18.5, 19.75, 2),
    ]


@icon("hierarchy", CAT, "Pyramid divided into three tiers; levels of a hierarchy",
      tags=["pyramid", "levels", "tiers", "ranking", "structure", "priority"], aliases=["pyramid-chart"])
def _(S):
    k = 9.5 / 17.5
    xs = lambda y: (12 - k * (y - 3), 12 + k * (y - 3))  # noqa: E731
    return [
        shell(poly([(12, 3), (21.5, 20.5), (2.5, 20.5)], closed=True, r=S.r * 0.66), stroke_miterlimit="2"),
        detail(seg(xs(9.5)[0], 9.5, xs(9.5)[1], 9.5)),
        detail(seg(xs(15)[0], 15, xs(15)[1], 15)),
    ]


@icon("workflow", CAT, "Two process steps joined by an elbow arrow",
      tags=["process", "flow", "automation", "steps", "procedure", "pipeline"], aliases=["process-flow"])
def _(S):
    return [
        shell(rect(3, 13, 7, 7, rr(S, 2.5))),
        shell(rect(14, 3, 7, 7, rr(S, 2.5))),
        line(poly([(6.5, 13), (6.5, 6.5), (11, 6.5)], r=S.r)),
        line(poly(head((11.75, 6.5), 0, 2.5), r=S.r * 0.5)),
    ]


# ============================================================================ goals and ideas

@icon("goal", CAT, "Flag planted on a mountain summit; a goal reached",
      tags=["goal", "objective", "summit", "achievement", "target", "ambition"], aliases=["summit-flag"])
def _(S):
    return [
        shell(poly([(2.5, 20.5), (10, 9), (13.5, 14), (16, 11), (21.5, 20.5)], closed=True, r=S.r), stroke_miterlimit="2"),
        line(seg(10, 9, 10, 2.5)),
        solid(poly([(11, 2.5), (15.5, 4.5), (11, 6.5)], closed=True)),
    ]


@icon("lightbulb-idea", CAT, "Light bulb with rays; a bright idea",
      tags=["idea", "innovation", "insight", "inspiration", "creative", "tip"], aliases=["idea"])
def _(S):
    bulb = "M9.5 17.5V16.2C8.3 15.3 7.5 13.9 7.5 12.3A4.5 4.5 0 0 1 16.5 12.3C16.5 13.9 15.7 15.3 14.5 16.2V17.5Z"
    rays = [line(seg(*polar(12, 12.3, 7, a), *polar(12, 12.3, 9, a))) for a in (-90, -135, -45, 180, 0)]
    return [shell(bulb), line(seg(10, 20.5, 14, 20.5)), *rays]


@icon("rocket-launch", CAT, "Rocket taking off at an angle with exhaust flame",
      tags=["launch", "startup", "go live", "boost", "take off", "release"], aliases=["launch"])
def _(S):
    deg, dx, dy = 45, 12.5, 11.5
    body = "M0 -8.5C2.8 -6.5 3.25 -3.5 3.25 -1V4H-3.25V-1C-3.25 -3.5 -2.8 -6.5 0 -8.5Z"
    fr = 0 if S.name == "line" else 1
    fin_l = poly([(-3.25, 0), (-6, 3), (-6, 6), (-3.25, 4)], closed=True, r=fr)
    fin_r = poly([(3.25, 0), (6, 3), (6, 6), (3.25, 4)], closed=True, r=fr)
    flame = [tp(p, deg, dx, dy) for p in [(-1.5, 6.25), (0, 10), (1.5, 6.25)]]
    return [
        shell(transformed_d(union_d(body, fin_l, fin_r), deg, dx, dy)),
        dot(*tp((0, -2.5), deg, dx, dy), 1.25),
        line(poly(flame, r=S.r * 0.5)),
    ]


@icon("award", CAT, "Award rosette with two ribbon tails",
      tags=["prize", "rosette", "achievement", "winner", "recognition", "badge"], aliases=["rosette"])
def _(S):
    pts = [polar(12, 8.5, 6.5 if i % 2 == 0 else 5.4, -90 + i * 360 / 28) for i in range(28)]
    return [
        shell(poly([(8.5, 13), (11, 14.5), (10, 21), (8.25, 19.5), (6.5, 20.5)], closed=True, r=S.r * 0.4)),
        shell(poly([(15.5, 13), (13, 14.5), (14, 21), (15.75, 19.5), (17.5, 20.5)], closed=True, r=S.r * 0.4)),
        shell(poly(pts, closed=True, r=S.r * 0.2)),
        detail(circle(12, 8.5, 2.25)),
    ]


@icon("signature", CAT, "Handwritten signature above a baseline",
      tags=["sign", "autograph", "handwriting", "e-signature", "approve", "sign here"], aliases=["autograph"])
def _(S):
    scrawl = ("M3.5 15.5C5.3 11.2 6.8 6 8.8 6C10.3 6 9.9 9.6 8.6 12.4C7.6 14.6 8 16.3 9.6 15.2"
              "C11.1 14.2 11.9 11.5 13.4 11.5C14.6 11.5 14.1 14 15.6 14C17 14 18.4 12.3 20.5 11")
    return [line(scrawl), line(seg(3, 20, 21, 20) if S.name == "line" else seg(4, 20, 20, 20))]


@icon("seal-stamp", CAT, "Rubber stamp with a round handle over its imprint",
      tags=["rubber stamp", "company seal", "approved", "stamp", "certify", "official"], aliases=["rubber-stamp"])
def _(S):
    rx = 0 if S.name == "line" else 2
    knob = circle(12, 6, 3)
    neck = poly([(10.5, 8), (13.5, 8), (14.5, 12), (9.5, 12)], closed=True)
    base = rect(4, 12, 16, 5.5, rx)
    return [
        shell(union_d(knob, neck, base)),
        line(seg(5, 20.5, 19, 20.5)),
    ]


@icon("atm", CAT, "Cash machine with a screen dispensing a banknote",
      tags=["cash machine", "cashpoint", "withdraw", "bank", "cash", "automated teller"], aliases=["cash-machine", "cashpoint"])
def _(S):
    return [
        shell(rect(4, 3, 16, 13, rr(S, 3))),
        detail(rect(8, 7, 8, 3, 0 if S.name == "line" else 1)),
        line(poly([(8, 16), (8, 21), (16, 21), (16, 16)], r=S.r)),
        dot(12, 18.5, 1),
    ]


@icon("cheque", CAT, "Bank cheque with written lines and a signature",
      tags=["check", "bank check", "payment", "pay", "cheque book", "draft"], aliases=["bank-cheque"])
def _(S):
    return [
        shell(rect(3, 6, 18, 12, rr(S, 3))),
        detail(seg(6, 9.5, 11, 9.5)), detail(seg(14, 9.5, 18, 9.5)),
        detail("M6 15C7.2 12.6 8.3 12.6 9 14.3C9.7 16 10.8 16 12 13.8"),
    ]


@icon("savings", CAT, "Jar holding a coin; money saved up",
      tags=["save", "savings jar", "money jar", "nest egg", "deposit", "reserve"], aliases=["money-jar"])
def _(S):
    jar = ("M8 6.5H16V8C18.6 8.6 20 10.6 20 13.2V19A2 2 0 0 1 18 21H6A2 2 0 0 1 4 19V13.2"
           "C4 10.6 5.4 8.6 8 8Z")
    return [
        shell(rect(7, 3, 10, 3.5, rr(S, 1.5) if S.name == "line" else 1.75)),
        shell(jar),
        detail(circle(12, 15, 2.5)),
    ]


@icon("investment", CAT, "Seedling sprouting from a coin; money that grows",
      tags=["invest", "growth", "returns", "interest", "grow money", "compound"], aliases=["grow-money"])
def _(S):
    return [
        shell(circle(12, 16.5, 4.5)), dot(12, 16.5, 1.25),
        line(seg(12, 12, 12, 7.5)),
        shell("M12 9C12 6.5 10 4.5 7 4.5C7 7 9 9 12 9Z" if S.name == "line" else
              "M12 9C12 6.5 10 4.5 7.6 4.5Q7 4.5 7 5.1C7 7.3 9 9 12 9Z", stroke_miterlimit="2"),
        shell("M12 7.5C12 5 14 3 17 3C17 5.5 15 7.5 12 7.5Z" if S.name == "line" else
              "M12 7.5C12 5 14 3 16.4 3Q17 3 17 3.6C17 5.8 15 7.5 12 7.5Z", stroke_miterlimit="2"),
    ]


@icon("calculator-money", CAT, "Calculator beside a stack of coins; costs and budgeting sums",
      tags=["accounting", "calculate cost", "bookkeeping", "expenses", "sum", "pricing"], aliases=["cost-calculator"])
def _(S):
    return [
        shell(circle(6.5, 6.5, 3.25)), dot(6.5, 6.5, 1),
        shell(rect(3, 13, 7, 8, rr(S, 2.5))), detail(seg(3, 17, 10, 17)),
        shell(rect(12, 3, 9, 18, rr(S, 3))),
        detail(seg(14.5, 7, 18.5, 7)),
        dot(14.75, 11.5, 1), dot(18.25, 11.5, 1), dot(14.75, 15.25, 1), dot(18.25, 15.25, 1),
    ]


@icon("ledger", CAT, "Account ledger book with ruled columns",
      tags=["accounts", "bookkeeping", "account book", "records", "journal", "accounting"], aliases=["account-book"])
def _(S):
    return [
        shell(rect(4, 3, 16, 18, rr(S, 3))),
        detail(seg(8, 3, 8, 21)),
        detail(seg(11, 8, 17, 8)), detail(seg(11, 12, 17, 12)), detail(seg(11, 16, 14, 16)),
    ]


AUDIT_LENS = ((15.5, 14.5), 4.5)
AUDIT_PAGE = [(12, 3), (4, 3), (4, 20), (15, 20), (15, 3), (12, 3)]
AUDIT_LINES = [[(7, 7.5), (12, 7.5)], [(7, 11.5), (10, 11.5)]]


def _audit_tick():
    (cx, cy), _ = AUDIT_LENS
    return [(cx - 2.25, cy), (cx - 0.5, cy + 1.75), (cx + 2.25, cy - 1.5)]


def _audit_filled():
    (cx, cy), r = AUDIT_LENS
    page = U(P(rect(3, 2, 13, 19)))
    page = D(page, P(circle(cx, cy, r + 2.5)), *(ST(poly(ln), 2.0) for ln in AUDIT_LINES))
    lens = D(P(circle(cx, cy, r + 1)), ST(poly(_audit_tick()), 2.0))
    handle = ST(seg(cx + 3.3, cy + 3.3, 21, 20.3), 2.5)
    return U(page, lens, handle)


@icon("audit", CAT, "Document examined under a magnifying glass with a tick",
      tags=["review", "inspection", "compliance", "verify", "check", "examine"], aliases=["inspection"],
      filled=_audit_filled)
def _(S):
    (cx, cy), r = AUDIT_LENS
    keep_out = P(circle(cx, cy, r + 3.5))
    parts = [line(poly(run, r=S.r)) for run in runs_outside(AUDIT_PAGE, keep_out)]
    for ln in AUDIT_LINES:
        parts += [line(poly(run)) for run in runs_outside(ln, keep_out)]
    parts += [
        shell(circle(cx, cy, r)),
        detail(poly(_audit_tick(), r=S.r * 0.5)),
        line(seg(cx + 3.3, cy + 3.3, 21, 20.3)),
    ]
    return parts
