"""TypeIcon Core: environment (batch 002).

Time and calendar situations, then climate change and pollution. Composite icons cut the object behind
an overlay by 2 px. Line and Rounded differ through S.r / S.R and per-style tips.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, LINE, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "environment"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def xf(d, s=1.0, dx=0.0, dy=0.0):
    """Scale a d-string about the origin then move it."""
    return path_to_d(transform_path(P(d), (s, 0, 0, s, dx, dy)))


def flipx(d, cx=12.0):
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 2 * cx, 0)))


def region(d):
    return U(P(d), ST(d, 2))


def grow(p, g):
    return U(p, ST(path_to_d(p), 2 * g, "round", "round"))


def sil(parts):
    """Covered area of a list of parts (closed shells count as filled)."""
    regs = []
    for p in parts:
        if p.kind == "shell":
            regs.append(region(p.d))
        elif p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        else:
            regs.append(ST(p.d, 2, "round", "round"))
    return U(*regs)


def comp(base, over, gap=2.0):
    """(draw, filled) for `base` seen behind `over` (both take a style and return parts)."""
    def draw(S):
        o = over(S)
        cutter = grow(sil(o), gap)
        out = []
        for p in base(S):
            reg = P(p.d) if p.kind in ("dot", "solid") else ST(p.d, 2, S.cap, S.join)
            out.append(solid(path_to_d(D(reg, cutter))))
        return out + o

    def filled():
        return U(D(filled_region(base(LINE)), grow(sil(over(LINE)), gap)), filled_region(over(LINE)))
    return draw, filled


def sq(x, y, w, h, rx=0.0):
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def digit(ch, x, y, w, h):
    """Stroke path of a numeral in the box x, y, w, h."""
    x2, y2, cx, cy = x + w, y + h, x + w / 2, y + h / 2
    if ch == "0":
        return rect(x, y, w, h, w / 2)
    if ch == "1":
        return f"M{fmt(x + w * 0.1)} {fmt(y + h * 0.25)}L{fmt(cx + 0.5)} {fmt(y)}V{fmt(y2)}"
    if ch == "2":
        return (f"M{fmt(x)} {fmt(y + h * 0.3)}C{fmt(x)} {fmt(y - h * 0.1)} {fmt(x2)} {fmt(y - h * 0.1)} {fmt(x2)} {fmt(y + h * 0.3)}"
                f"C{fmt(x2)} {fmt(y + h * 0.6)} {fmt(x)} {fmt(y + h * 0.65)} {fmt(x)} {fmt(y2)}H{fmt(x2)}")
    if ch == "3":
        return (f"M{fmt(x)} {fmt(y + h * 0.15)}C{fmt(x + w * 0.3)} {fmt(y - h * 0.08)} {fmt(x2)} {fmt(y)} {fmt(x2)} {fmt(y + h * 0.27)}"
                f"C{fmt(x2)} {fmt(y + h * 0.45)} {fmt(x + w * 0.6)} {fmt(cy)} {fmt(cx - 0.3)} {fmt(cy)}"
                f"C{fmt(x2 + 0.5)} {fmt(cy)} {fmt(x2 + 0.5)} {fmt(y + h * 1.06)} {fmt(x + w * 0.4)} {fmt(y2)}C{fmt(x + w * 0.2)} {fmt(y2)} {fmt(x)} {fmt(y + h * 0.92)} {fmt(x)} {fmt(y + h * 0.85)}")
    if ch == "4":
        return f"M{fmt(x + w * 0.75)} {fmt(y2)}V{fmt(y)}L{fmt(x)} {fmt(y + h * 0.65)}H{fmt(x2)}"
    return ""


def cal(S, x=3, y=5, w=18, h=16):
    """Calendar page: body, header rule, two rings."""
    return [shell(rect(x, y, w, h, S.R * 0.75)), detail(seg(x, y + 5, x + w, y + 5)),
            line(seg(x + 5, y - 2, x + 5, y + 2)), line(seg(x + w - 5, y - 2, x + w - 5, y + 2))]


def clock(S, cx, cy, r, hands=None):
    hands = hands or [(cx, cy - r * 0.6), (cx, cy), (cx + r * 0.42, cy + r * 0.24)]
    return [shell(circle(cx, cy, r)), detail(poly(hands, r=S.r * 0.5))]


def moon_d(cx, cy, s):
    """The Core crescent moon, scaled by s and centred on (cx, cy)."""
    return xf("M20.5 14.5A8.5 8.5 0 1 1 9.5 3.5A7 7 0 0 0 20.5 14.5Z", s, cx - 12 * s, cy - 9 * s)


# ============================================================================ calendar and clock situations

@icon("calendar-quarter", CAT, "Calendar page with the letter Q and the number 1 in its body.",
      tags=["quarter", "q1", "three months", "fiscal quarter", "calendar", "financial period", "reporting"])
def _(S):
    q = [detail(circle(9, 15.5, 2.25)), detail(seg(10.6, 17.1, 12.4, 18.9)),
         detail(digit("1", 15.5, 13, 3, 5.5))]
    return cal(S) + q


_dt_base = lambda S: [shell(rect(3, 5, 14, 13, S.R * 0.75)), detail(seg(3, 9.5, 17, 9.5)),
                      line(seg(7, 3, 7, 7)), line(seg(13, 3, 13, 7))]
_dt_over = lambda S: clock(S, 16, 16, 5, [(16, 13), (16, 16), (18.2, 17.5)])
_d, _f = comp(_dt_base, _dt_over)
icon("date-time", CAT, "Calendar page with a small clock face over its lower corner.",
     tags=["date and time", "datetime", "timestamp", "schedule", "calendar clock", "appointment"], filled=_f)(_d)


@icon("shift-schedule", CAT, "Chart frame with staggered horizontal bars like work shifts.",
      tags=["shift", "roster", "rota", "work schedule", "timetable", "staff schedule", "gantt"])
def _(S):
    return [shell(rect(3, 4, 18, 16, S.R * 0.75)),
            detail(seg(6.5, 9, 12, 9)), detail(seg(9.5, 13, 17.5, 13)), detail(seg(12.5, 17, 17.5, 17))]


@icon("night-shift", CAT, "Crescent moon beside a hard hat.",
      tags=["night shift", "graveyard shift", "late shift", "night work", "hard hat", "construction", "moon"])
def _(S):
    return [shell(moon_d(7, 7, 0.5)),
            shell("M9.5 21V19.5H11V17A5 5 0 0 1 20 17V19.5H22V21Z" if False else "M9 21V19.5H10.5V17.5A5.25 5.25 0 0 1 20.5 17.5V19.5H22V21Z"),
            detail(seg(15.5, 12.25, 15.5, 15.5))]


_tt_base = lambda S: clock(S, 10.5, 10.5, 7.5)
_tt_over = lambda S: [line(seg(14.5, 21, 14.5, 18)), line(seg(18, 21, 18, 14.5)), line(seg(21, 21, 21, 16.5))]
_d, _f = comp(_tt_base, _tt_over)
icon("time-tracking", CAT, "Clock face with a small bar chart at its lower corner.",
     tags=["time tracking", "timesheet", "hours logged", "productivity", "work hours", "clock", "chart"], filled=_f)(_d)


_tm_base = lambda S: [shell(rect(10, 3, 11, 15, S.R * 0.5)), detail(seg(14, 7.5, 17.5, 7.5)), detail(seg(14, 11, 17.5, 11))]
_tm_over = lambda S: clock(S, 9, 15.5, 5.5, [(9, 12.5), (9, 15.5), (11.2, 16.8)])
_d, _f = comp(_tm_base, _tm_over)
icon("time-management", CAT, "Clock face in front of a checklist sheet.",
     tags=["time management", "planning", "prioritise", "productivity", "to do", "schedule", "organise"], filled=_f)(_d)


@icon("pomodoro-timer", CAT, "Tomato-shaped kitchen timer with a leafy top and clock hands.",
      tags=["pomodoro", "tomato timer", "focus timer", "study timer", "kitchen timer", "25 minutes", "productivity"])
def _(S):
    return [shell(ellipse(12, 14.5, 9, 6.75)),
            line("M12 7.75C10.5 5 8.5 5 6.5 6.25"), line("M12 7.75C13.5 5 15.5 5 17.5 6.25"), line(seg(12, 7.75, 12, 4)),
            detail(poly([(12, 11.5), (12, 14.5), (15, 16)], r=S.r * 0.5))]


@icon("time-blocking", CAT, "Day column with a time axis and three solid blocks of different heights.",
      tags=["time blocking", "time boxing", "day planner", "calendar blocks", "focus blocks", "schedule", "agenda"])
def _(S):
    return [line(seg(4, 3, 4, 21)),
            sq(8, 3.5, 12, 6, L(S, 0, 1.5)), sq(8, 12, 8, 3.5, L(S, 0, 1.5)), sq(8, 17.5, 12, 3, L(S, 0, 1.5))]


def _wedge(S, cx, cy, r, a0, a1, n=5):
    pts = [(cx, cy)] + [polar(cx, cy, r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]
    return poly(pts, closed=True, r=S.r * 2)


@icon("time-slot", CAT, "Clock face with a highlighted wedge between two hands.",
      tags=["time slot", "time window", "appointment slot", "booking", "interval", "clock", "availability"])
def _(S):
    return [shell(circle(12, 12, 9)), Part("dot", _wedge(S, 12, 12, 6.5, -90, 30))]


@icon("estimated-arrival", CAT, "Map pin with clock hands inside its head.",
      tags=["eta", "estimated arrival", "arrival time", "delivery time", "arrives at", "map pin", "travel time"], aliases=["eta"])
def _(S):
    pin = "M12 21.5C12 21.5 5 15 5 9.5A7 7 0 0 1 19 9.5C19 15 12 21.5 12 21.5Z"
    return [shell(pin), detail(poly([(12, 5.5), (12, 9.5), (15, 11)], r=S.r * 0.5))]


_tim_base = lambda S: [shell("M12 13V19.5A5 2 0 0 0 22 19.5V13"), shell(ellipse(17, 13, 5, 2)),
                       detail("M12 16.3A5 2 0 0 0 22 16.3")]
_tim_over = lambda S: clock(S, 8.5, 8.5, 5.5, [(8.5, 5.5), (8.5, 8.5), (10.7, 9.8)])
_d, _f = comp(_tim_base, _tim_over)
icon("time-is-money", CAT, "Clock face overlapping a stack of coins.",
     tags=["time is money", "billable hours", "hourly rate", "pay per hour", "cost of time", "coins", "clock"], filled=_f)(_d)


_mn_base = lambda S: [shell(circle(10.5, 13.5, 7.5)), detail(seg(10.5, 13.5, 10.5, 8.5))]
_mn_over = lambda S: [shell(moon_d(18, 6.5, 0.42))]
_d, _f = comp(_mn_base, _mn_over)
icon("midnight", CAT, "Clock face with its hands at twelve and a small crescent moon.",
     tags=["midnight", "12 am", "twelve o'clock", "night", "end of day", "witching hour", "late night"], filled=_f)(_d)


@icon("decade", CAT, "Calendar page with the number 10 in its body.",
      tags=["decade", "ten years", "10 years", "anniversary", "long term", "era", "calendar"])
def _(S):
    return cal(S) + [detail(digit("1", 6.5, 13, 3, 5.5)), detail(digit("0", 12, 13, 4, 5.5))]


@icon("clock-radio", CAT, "Bedside clock radio with a display, a speaker grille and an antenna.",
      tags=["clock radio", "alarm radio", "bedside clock", "wake up radio", "speaker", "morning", "radio alarm"])
def _(S):
    return [shell(rect(2.5, 8.5, 19, 11, S.R * 0.75)), sq(5.5, 11.5, 6, 3.5, L(S, 0, 1)),
            detail(seg(14.5, 12, 19, 12)), detail(seg(14.5, 16, 19, 16)), line(seg(17, 8.5, 20.5, 4))]


@icon("open-24-hours", CAT, "Circle with the number 24 and an arrow wrapping around it.",
      tags=["24 hours", "open all day", "around the clock", "always open", "24/7", "all day service", "non stop"], aliases=["open-24-7"])
def _(S):
    e = polar(12, 12, 9, -30)
    th = math.radians(-30)
    t = (-math.sin(th), math.cos(th))
    def back(a):
        c, sn = math.cos(math.radians(a)), math.sin(math.radians(a))
        return (e[0] - 3.2 * (t[0] * c - t[1] * sn), e[1] - 3.2 * (t[0] * sn + t[1] * c))
    return [line(arc(12, 12, 9, 30, 330)), line(poly([back(42), e, back(-42)])),
            detail(digit("2", 6.5, 9, 3.2, 6)), detail(digit("4", 12.5, 9, 3.6, 6))]


@icon("streak-counter", CAT, "Flame with a number in its centre.",
      tags=["streak", "day streak", "on fire", "consecutive days", "winning streak", "daily streak", "flame counter"])
def _(S):
    flame = "M12 3C12.5 6.5 18 8.5 18 14.5A6 6 0 0 1 6 14.5C6 11.5 7.5 10 8.5 8.5C9.5 10 10 10.5 11 10.5C11 7.5 11.5 5 12 3Z"
    return [shell(flame), detail(digit("3", 9.75, 12, 4, 5))]


# ============================================================================ climate

def cloud_d(s=1.0, cx=12.0, cy=12.0, S=LINE):
    """The Core cloud scaled by s about its own centre and moved to (cx, cy)."""
    d = "M4.5 19H19.5A3.8 3.8 0 0 0 18 11.7A6 6 0 0 0 6.5 10A4.7 4.7 0 0 0 4.5 19Z" if S.name == "line" else \
        "M7 19H17.5A4.5 4.5 0 0 0 18 10.03A6 6 0 0 0 6.34 9.1A5 5 0 0 0 7 19Z"
    return xf(d, s, cx - 12 * s, cy - 11.5 * s)


_gw_base = lambda S: [shell(circle(9.5, 13.5, 7)), detail(ellipse(9.5, 13.5, 3, 7)), detail(seg(2.5, 13.5, 16.5, 13.5))]
_gw_over = lambda S: [line(seg(19, 4.5, 19, 16.5)), dot(19, 18.4, 2.6)]
_d, _f = comp(_gw_base, _gw_over)
icon("global-warming", CAT, "Globe with a thermometer standing in front of it.",
     tags=["global warming", "rising temperatures", "heating planet", "climate crisis", "earth", "thermometer", "hot planet"], filled=_f)(_d)


@icon("melting-ice-cap", CAT, "Ice peaks dripping two droplets into the water below.",
      tags=["melting ice", "ice cap", "polar ice", "iceberg melting", "sea level rise", "thaw", "drip"])
def _(S):
    return [shell(poly([(4, 11.5), (8, 5), (11, 8.5), (14.5, 3.5), (20, 11.5)], closed=True, r=S.r * 0.5)),
            solid("M8.5 13.5Q7.3 15.5 7.3 16.3A1.2 1.2 0 0 0 9.7 16.3Q9.7 15.5 8.5 13.5Z"),
            solid("M15 14.5Q13.8 16.5 13.8 17.3A1.2 1.2 0 0 0 16.2 17.3Q16.2 16.5 15 14.5Z"),
            line("M3 20.5Q5.25 18.5 7.5 20.5Q9.75 22.5 12 20.5Q14.25 18.5 16.5 20.5Q18.75 22.5 21 20.5")]


@icon("temperature-anomaly", CAT, "Line chart with a dashed zero baseline and a jagged curve climbing above it.",
      tags=["temperature anomaly", "warming trend", "climate chart", "global temperature", "deviation", "baseline", "graph"])
def _(S):
    return [line(poly([(3, 3), (3, 21), (21, 21)], r=S.r * 0.5)),
            detail(seg(6, 15, 8, 15)), detail(seg(11, 15, 13, 15)),
            line(poly([(6, 18), (9, 14.5), (11.5, 16.5), (14.5, 10), (17, 12), (20, 5.5)], r=S.r * 0.6))]


@icon("carbon-tax", CAT, "Price tag with a solid cloud on it.",
      tags=["carbon tax", "emissions price", "pollution tax", "green tax", "carbon price", "levy", "tag"])
def _(S):
    return [shell(poly([(3, 12), (9.5, 5), (21, 5), (21, 19), (9.5, 19)], closed=True, r=S.r)),
            Part("dot", P(cloud_d(0.52, 14.5, 12.25)).__class__ and cloud_d(0.52, 14.5, 12.25))]


@icon("climate-protest-sign", CAT, "Placard on a stick showing a leaf.",
      tags=["climate protest", "climate strike", "placard", "demonstration", "activism", "sign", "green march"])
def _(S):
    return [shell(rect(3, 3, 18, 13, S.R * 0.75)), line(seg(12, 16, 12, 21.5)),
            detail("M8 12.5C7.5 8.5 10 6.5 16 6C16 10 14 12.5 8 12.5Z")]


@icon("sea-ice-loss", CAT, "Two ice floes of different sizes with open water between them.",
      tags=["sea ice", "ice loss", "ice floe", "arctic melt", "polar ice", "shrinking ice", "floating ice"])
def _(S):
    return [shell(poly([(2.5, 14.5), (4, 7.5), (11, 7.5), (12.5, 14.5)], closed=True, r=S.r)),
            shell(poly([(16.5, 14.5), (17.5, 11), (20.5, 11), (21.5, 14.5)], closed=True, r=S.r)) if False else
            shell(poly([(16, 14.5), (17, 11.5), (20.5, 11.5), (21.5, 14.5)], closed=True, r=S.r)),
            line("M2.5 19Q5 17 7.5 19Q10 21 12.5 19Q15 17 17.5 19Q20 21 21.5 19")]


@icon("air-pollution", CAT, "Factory with a chimney and a solid cloud of smoke above it.",
      tags=["air pollution", "smog", "factory smoke", "emissions", "industrial pollution", "dirty air", "chimney"])
def _(S):
    return [shell(poly([(3, 20.5), (3, 14), (7.5, 17), (7.5, 14), (12, 17), (12, 20.5)], closed=True, r=S.r * 0.5)),
            shell(rect(15, 12, 5, 8.5, L(S, 0, 1))), Part("dot", cloud_d(0.68, 13, 6.5))]


@icon("smokestack-pollution", CAT, "Two tapered chimneys with round smoke puffs drifting away.",
      tags=["smokestack", "chimney smoke", "power station", "industrial emissions", "smoke puffs", "pollution", "stack"])
def _(S):
    return [shell(poly([(3.5, 21), (5, 11), (10, 11), (11.5, 21)], closed=True, r=S.r * 0.5)), detail(seg(4.6, 15, 10.4, 15)),
            shell(poly([(14, 21), (15, 14), (19, 14), (20, 21)], closed=True, r=S.r * 0.5)),
            Part("dot", circle(6.5, 7.5, 2.25)), Part("dot", circle(11.5, 5.25, 1.75)), Part("dot", circle(17, 10, 1.75)),
            Part("dot", circle(20, 6.5, 1.5))]


_ex_base = lambda S: [shell(poly([(7, 16.5), (7, 12.5), (10.5, 12.5), (12.5, 8), (17.5, 8), (20, 12.5), (21.5, 12.5), (21.5, 16.5)],
                                 closed=True, r=S.r))]
_ex_over = lambda S: [shell(circle(11.5, 16.5, 2.25)), shell(circle(18, 16.5, 2.25))]
_exd, _exf = comp(_ex_base, _ex_over, gap=1.5)
_PUFFS = [(3.25, 15, 1.5), (4.25, 10.5, 1.9), (2.75, 19.25, 1.0)]


def _exhaust_draw(S):
    return _exd(S) + [Part("dot", circle(*p)) for p in _PUFFS]


icon("exhaust-fumes", CAT, "Car seen from the side with puffs of smoke behind its tailpipe.",
     tags=["exhaust", "car fumes", "tailpipe", "vehicle emissions", "traffic pollution", "car smoke", "fumes"],
     filled=lambda: U(_exf(), *[P(circle(*p)) for p in _PUFFS]))(_exhaust_draw)


@icon("water-pollution", CAT, "Pipe spout dripping into the water below it.",
      tags=["water pollution", "pipe discharge", "contaminated water", "dirty water", "waste water", "drip", "spill"])
def _(S):
    return [shell(poly([(2.5, 3.5), (15, 3.5), (15, 10), (11, 10), (11, 7.5), (2.5, 7.5)], closed=True, r=S.r * 0.5)),
            solid("M13 12.5Q11.5 15 11.5 15.6A1.5 1.5 0 0 0 14.5 15.6Q14.5 15 13 12.5Z"),
            line("M3 19.5Q5.25 17.5 7.5 19.5Q9.75 21.5 12 19.5Q14.25 17.5 16.5 19.5Q18.75 21.5 21 19.5")]


@icon("dead-fish", CAT, "Fish floating belly up with a crossed-out eye.",
      tags=["dead fish", "fish kill", "belly up", "polluted water", "dying fish", "toxic water", "algae bloom"])
def _(S):
    return [shell("M3 12C6 7.5 12 7.5 15 12C12 16.5 6 16.5 3 12Z"),
            shell(poly([(15, 12), (20.5, 8.5), (20.5, 15.5)], closed=True, r=S.r)),
            detail(poly([(8.5, 14.5), (10, 19), (12.5, 15)], r=S.r * 0.5)),
            detail(seg(5.6, 10.6, 7.4, 12.4)), detail(seg(7.4, 10.6, 5.6, 12.4))]


@icon("plastic-pollution", CAT, "Plastic bottle floating on rippling water.",
      tags=["plastic pollution", "ocean plastic", "floating bottle", "marine litter", "sea rubbish", "waste in sea", "bottle"])
def _(S):
    return [shell("M9.5 2.5H14.5V6.5C14.5 8 17.5 8.5 17.5 11.5V16.5H6.5V11.5C6.5 8.5 9.5 8 9.5 6.5Z"),
            detail(seg(6.5, 12.5, 17.5, 12.5)),
            line("M3 20Q5.25 18 7.5 20Q9.75 22 12 20Q14.25 18 16.5 20Q18.75 22 21 20")]


@icon("plastic-bag", CAT, "Carrier bag with a handle arch and crumple lines.",
      tags=["plastic bag", "carrier bag", "shopping bag", "single use plastic", "polybag", "litter", "grocery bag"])
def _(S):
    return [shell(poly([(5, 8), (19, 8), (20.5, 21), (3.5, 21)], closed=True, r=S.r)),
            line("M8.5 8V6.5A3.5 3.5 0 0 1 15.5 6.5V8"),
            detail(poly([(8, 12), (10.5, 14.5)])), detail(poly([(14, 16), (16, 18.5)]))]


@icon("toxic-waste-barrel", CAT, "Steel drum with rim bands, a hazard mark and a leaking drip.",
      tags=["toxic waste", "hazardous waste", "barrel", "drum", "chemical spill", "contamination", "leak", "hazmat"])
def _(S):
    return [shell(rect(5, 2.5, 14, 15.5, L(S, 1, 2.5))), detail(seg(5, 6.5, 19, 6.5)), detail(seg(5, 14, 19, 14)),
            detail(seg(12, 8.25, 12, 10.5)), dot(12, 12.25, 0.85),
            solid("M12 18.75Q10.5 20.75 10.5 21A1.5 1.5 0 0 0 13.5 21Q13.5 20.75 12 18.75Z")]


@icon("particulate-matter", CAT, "Cloud with a scatter of tiny specks of different sizes beneath it.",
      tags=["particulate matter", "pm2.5", "pm10", "fine dust", "soot", "air quality", "smog particles", "haze"])
def _(S):
    cl = cloud_d(0.78, 12, 9.5, S)
    return [shell(cl), dot(9.5, 9.5, 0.9), dot(13.5, 10.5, 1.1),
            dot(5, 19, 1.25), dot(9, 21, 0.9), dot(12.75, 18.75, 1.4), dot(17, 20.5, 1), dot(20.25, 17.75, 1.2)]


@icon("fracking-rig", CAT, "Tall derrick on the ground with drilling lines fanning out beneath.",
      tags=["fracking", "drilling rig", "derrick", "oil well", "gas extraction", "shale gas", "hydraulic fracturing"])
def _(S):
    return [shell(poly([(8, 13), (12, 3), (16, 13)], closed=True, r=S.r * 0.6)), detail(seg(10, 8.5, 14, 8.5)),
            line(seg(3, 13.5, 21, 13.5)), line(seg(12, 13.5, 12, 18.5)),
            line(poly([(12, 18.5), (6, 21)])), line(poly([(12, 18.5), (18, 21)]))]


@icon("cigarette-butt-litter", CAT, "Cigarette butt lying on the ground with a thin curl of smoke.",
      tags=["cigarette butt", "litter", "smoking litter", "stub", "dropped cigarette", "ash", "street litter"])
def _(S):
    return [shell(rect(3.5, 14.5, 14, 4, L(S, 0.5, 2))), detail(seg(9, 14.5, 9, 18.5)),
            line("M19 14C21 12 17 10 19 7.5"), line(seg(2.5, 21.25, 21.5, 21.25))]


_cb_base = lambda S: [shell("M3.5 11V19A2 2 0 0 0 5.5 21H10.5A2 2 0 0 0 12.5 19V11Z"), line("M12.5 13H14.5A2 2 0 0 1 14.5 18H12.5"),
                      line(seg(6, 3, 6, 7)), line(seg(10, 3, 10, 7))]
_cb_over = lambda S: clock(S, 17, 8, 4.5, [(17, 5.5), (17, 8), (18.8, 9.2)])
_d, _f = comp(_cb_base, _cb_over)
icon("coffee-break", CAT, "Coffee cup with steam and a small clock face beside it.",
     tags=["coffee break", "tea break", "rest time", "pause", "break time", "office break", "cup and clock"], filled=_f)(_d)


@icon("habit-tracker", CAT, "Frame holding a grid of small squares, some solid and some still empty dots.",
      tags=["habit tracker", "habit streak", "daily habits", "progress grid", "routine", "consistency", "goal tracking"])
def _(S):
    k = L(S, 0, 0.75)
    xs, ys = (6, 10.5, 15), (6.25, 10.75, 15.25)
    done = {(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (0, 2)}
    parts = [shell(rect(3, 3, 18, 18, S.R * 0.75))]
    for r, y in enumerate(ys):
        for c, x in enumerate(xs):
            parts.append(sq(x, y, 3, 3, k) if (c, r) in done else dot(x + 1.5, y + 1.5, 0.75))
    return parts
