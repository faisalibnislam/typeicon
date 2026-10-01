"""TypeIcon Core: time & calendar.

Calendars share the v0.1 `calendar` page (18 x 16 body, header rule at y 10, two binding rings) and
put their content in the body (y 12–20). Clocks share the v0.1 `clock` face (circle r 9). Composite
icons (calendar + clock, globe + clock) cut the base clear of the overlay by 2 px.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import LINE, fmt, polar

CAT = "time"


# ============================================================================ shared parts

def _cal(S):
    return [shell(rect(3, 5, 18, 16, S.R * 0.75)), detail(seg(3, 10, 21, 10)), line(seg(8, 3, 8, 7)), line(seg(16, 3, 16, 7))]


def _cal_base_filled():
    """Filled calendar page (as the v0.1 calendar): head with ring notches, a rule gap, then the body."""
    head = D(P(rect(2, 4, 20, 5.25, 2)), P(rect(6, 2, 4, 5.5)), P(rect(14, 2, 4, 5.5)))
    head = U(head, P(rect(7, 2, 2, 4.5)), P(rect(15, 2, 2, 4.5)))
    return U(head, P(rect(2, 11, 20, 11, 2)), P(rect(2, 8, 20, 1.25)))


def _knock(parts):
    regions = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regions.append(P(p.d))
        elif p.kind in ("detail", "line"):
            regions.append(ST(p.d, 2.0, "butt", "miter"))
    return regions


def _cal_filled(content):
    return lambda: D(_cal_base_filled(), *_knock(content(LINE)))


def square(x, y, s):
    """Small solid square mark (a 'dot' part: knocked out of Filled shells)."""
    return Part("dot", rect(x, y, s, s))


def _clock_face(S, cx=12.0, cy=12.0, r=9.0, hands=None):
    hands = hands or [(cx, cy - r * 0.55), (cx, cy), (cx + r * 0.4, cy + r * 0.22)]
    return [shell(circle(cx, cy, r)), detail(poly(hands, r=S.r * 0.5))]


def _runs(pts, keep):
    """Split a sampled polyline into runs of points where keep(pt) is true."""
    runs, cur = [], []
    for p in pts:
        if keep(p):
            cur.append(p)
        else:
            if len(cur) > 1:
                runs.append(cur)
            cur = []
    if len(cur) > 1:
        runs.append(cur)
    return runs


def _circle_pts(cx, cy, r, rx=None, ry=None, n=360):
    rx, ry = (r, r) if rx is None else (rx, ry)
    return [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in range(n + 1)]


def _poly_d(pts):
    return "".join(("M" if i == 0 else "L") + f"{fmt(x)} {fmt(y)}" for i, (x, y) in enumerate(pts))


def _trimmed_closed(pts, keep):
    """Runs of a closed sampled curve (merging the run that wraps round the start)."""
    runs = _runs(pts, keep)
    if len(runs) > 1 and keep(pts[0]) and keep(pts[-1]):
        runs[0] = runs[-1] + runs[0][1:]
        runs.pop()
    return runs


def _away(cx, cy, clr):
    return lambda p: math.hypot(p[0] - cx, p[1] - cy) >= clr


# ============================================================================ clocks

@icon("clock-analog", CAT, "Clock face with hour marks and hands at ten past ten.",
      tags=["clock", "analog", "time", "hour", "watch face", "dial"], aliases=["analog-clock"])
def _(S):
    marks = [dot(12, 5.75, 1.2), dot(18.25, 12, 1.2), dot(12, 18.25, 1.2), dot(5.75, 12, 1.2)]
    return [shell(circle(12, 12, 9)), *marks, detail(poly([(8.75, 9.75), (12, 12), (15, 8.75)], r=S.r * 0.5))]


@icon("clock-digital", CAT, "Digital clock display showing digits and a colon.",
      tags=["digital clock", "clock", "display", "time", "alarm clock", "led"], aliases=["digital-clock"])
def _(S):
    return [shell(rect(2, 6, 20, 12, min(S.R, 3))),
            detail(rect(5.5, 9.5, 3, 5, 0.5 if S.name == "line" else 1.5)),
            detail(rect(15.5, 9.5, 3, 5, 0.5 if S.name == "line" else 1.5)),
            dot(12, 10, 1.1), dot(12, 14, 1.1)]


@icon("alarm-clock", CAT, "Alarm clock with two bells and little feet.",
      tags=["alarm", "alarm clock", "wake up", "morning", "reminder", "ring"])
def _(S):
    cx, cy, r = 12, 13, 7.5
    return [*_clock_face(S, cx, cy, r, [(12, 9.5), (12, 13), (14.5, 14.75)]),
            line(arc(6, 6.75, 3.25, 180, 270)), line(arc(18, 6.75, 3.25, 270, 360)),
            line(seg(7.2, 18.8, 5.5, 20.5)), line(seg(16.8, 18.8, 18.5, 20.5))]


@icon("timer", CAT, "Stopwatch with a top button; time an activity.",
      tags=["timer", "stopwatch", "duration", "lap", "chronometer", "stop watch"], aliases=["stopwatch"])
def _(S):
    return [shell(circle(12, 13.5, 7.5)), detail(seg(12, 13.5, 12, 9)),
            line(seg(9.5, 3, 14.5, 3)), line(seg(12, 3, 12, 5)),
            line(seg(17.8, 7.7, 19.5, 6))]


THREE = ("M8.8 8.6C9.5 7.6 10.6 7 12 7C13.9 7 15.2 8.1 15.2 9.6C15.2 11.1 13.9 12 12 12"
         "C14.2 12 15.5 13 15.5 14.6C15.5 16.2 14 17.3 12 17.3C10.5 17.3 9.3 16.7 8.6 15.7")


@icon("countdown", CAT, "Numeral 3 inside a ring; a countdown.",
      tags=["countdown", "time left", "remaining", "3 2 1", "launch", "timer"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(THREE)]


@icon("history", CAT, "Clock face inside an arrow turning back anticlockwise; history.",
      tags=["history", "recent", "past", "log", "time machine", "undo"], aliases=["recent"])
def _(S):
    cx, cy, r = 13, 12, 8
    start = polar(cx, cy, r, -150)
    d = (-0.5, math.sqrt(3) / 2)          # anticlockwise tangent at the start
    n = (d[1], -d[0])
    tip = (start[0] + d[0] * 1.0, start[1] + d[1] * 1.0)
    head = [(tip[0] - 3.5 * d[0] + 3.5 * n[0], tip[1] - 3.5 * d[1] + 3.5 * n[1]), tip,
            (tip[0] - 3.5 * d[0] - 3.5 * n[0], tip[1] - 3.5 * d[1] - 3.5 * n[1])]
    return [line(arc(cx, cy, r, -150, 150)), line(poly(head, r=S.r * 0.5)),
            line(poly([(13, 8), (13, 12), (16, 14)], r=S.r * 0.5))]


@icon("hourglass", CAT, "Hourglass with sand gathered in the lower bulb.",
      tags=["hourglass", "sand timer", "wait", "loading", "time", "egg timer"], aliases=["sand-timer"])
def _(S):
    glass = [(6, 3), (18, 3), (18, 6.5), (13.5, 12), (18, 17.5), (18, 21), (6, 21), (6, 17.5), (10.5, 12), (6, 6.5)]
    return [shell(poly(glass, closed=True, r=S.r * 0.5)), line(seg(4, 3, 20, 3)), line(seg(4, 21, 20, 21)),
            Part("dot", poly([(9, 19), (12, 16), (15, 19)], closed=True))]


GNOMON = [(8.5, 12.5), (8.5, 4.5), (16, 12.5)]


def _in_gnomon(p, pad):
    x, y = p
    if x < 8.5 - pad or y > 12.5 + pad or y < 4.5 - pad:
        return False
    nx, ny = 8.0, -7.5   # normal of the hypotenuse (8.5, 4.5) -> (16, 12.5)
    return ((x - 8.5) * nx + (y - 4.5) * ny) / math.hypot(nx, ny) <= pad


@icon("sundial", CAT, "Garden sundial: a triangular gnomon on a round dial plate atop a pedestal.",
      tags=["sundial", "sun clock", "ancient", "shadow", "time", "garden"],
      filled=lambda: U(P(poly(GNOMON, closed=True)), ST(poly(GNOMON, closed=True), 2.0), P(ellipse(12, 12.5, 10, 4)),
                       ST("M12 16V20", 2.5), ST("M7 20.5H17", 2.5)))
def _(S):
    runs = _trimmed_closed(_circle_pts(12, 12.5, 0, 9, 3), lambda p: not _in_gnomon(p, 1.2) or p[1] > 12.5)
    return [shell(poly(GNOMON, closed=True, r=S.r * 0.4)), *(line(_poly_d(rn)) for rn in runs),
            line(seg(12, 15.5, 12, 20)), line(seg(7, 20.5, 17, 20.5))]


@icon("deadline", CAT, "Clock face beside an exclamation mark; a deadline.",
      tags=["deadline", "due", "due date", "overdue", "urgent", "time limit"], aliases=["due-date"])
def _(S):
    return [*_clock_face(S, 10, 12, 7, [(10, 8.5), (10, 12), (12.5, 13.5)]),
            line(seg(20.5, 5, 20.5, 14)), dot(20.5, 18.5, 1.5)]


# ============================================================================ composites (cut clear of an overlay)

def _snooze_z():
    return poly([(15.5, 3), (21, 3), (15.5, 9), (21, 9)])


@icon("snooze", CAT, "Clock face with a letter Z; snooze an alarm.",
      tags=["snooze", "sleep", "later", "remind later", "alarm", "zz"],
      filled=lambda: U(D(P(circle(10.5, 13.5, 8.5)), ST("M10.5 9.5V13.5L13 15", 2.0), ST(_snooze_z(), 6.5, "round", "round")),
                       ST(_snooze_z(), 2.5, "butt", "miter", 2)))
def _(S):
    cx, cy, r = 10.5, 13.5, 7.5
    zpts = [(15.5, 3), (21, 3), (15.5, 9), (21, 9)]

    def keep(p):
        best = 99.0
        for (ax, ay), (bx, by) in zip(zpts, zpts[1:]):
            t = max(0, min(1, ((p[0] - ax) * (bx - ax) + (p[1] - ay) * (by - ay)) / ((bx - ax) ** 2 + (by - ay) ** 2)))
            best = min(best, math.hypot(p[0] - ax - t * (bx - ax), p[1] - ay - t * (by - ay)))
        return best >= 5.0
    runs = _trimmed_closed(_circle_pts(cx, cy, r), keep)
    return [*(line(_poly_d(rn)) for rn in runs), line(poly([(10.5, 9.5), (10.5, 13.5), (13, 15)], r=S.r * 0.5)),
            line(_snooze_z(), stroke_miterlimit="2")]


CLK = (17.0, 17.0, 4.0)  # overlay clock / loop in the lower-right of a calendar


def _cut_cal(S):
    """The standard calendar page trimmed 2 px clear of the overlay circle CLK."""
    cx, cy, r = CLK
    clr = r + 4 + (1 if S.name != "line" else 0)
    y_end = cy - math.sqrt(max(0, clr ** 2 - (21 - cx) ** 2))
    x_bot = cx - math.sqrt(max(0, clr ** 2 - (21 - cy) ** 2))
    x_rule = cx - math.sqrt(max(0, clr ** 2 - (10 - cy) ** 2))
    return [line(poly([(21, y_end), (21, 5), (3, 5), (3, 21), (x_bot, 21)], r=S.R * 0.75)),
            line(seg(3, 10, x_rule, 10)), line(seg(8, 3, 8, 7)), line(seg(16, 3, 16, 7))]


def _cut_cal_filled(overlay):
    cx, cy, r = CLK
    return U(D(_cal_base_filled(), P(circle(cx, cy, r + 3.25))), overlay)


def _agenda(S):
    return [dot(7, 14, 1.25), detail(seg(10, 14, 17, 14)), dot(7, 18, 1.25), detail(seg(10, 18, 15, 18))]


@icon("schedule", CAT, "Calendar page listing timed entries; a schedule or agenda.",
      tags=["schedule", "agenda", "appointments", "planner", "timetable", "itinerary"], aliases=["agenda"],
      filled=_cal_filled(_agenda))
def _(S):
    return [*_cal(S), *_agenda(S)]


def _loop(S, cx, cy, r):
    a0, a1 = 30, 300
    end = polar(cx, cy, r, a1)
    t = (-math.sin(math.radians(a1)), math.cos(math.radians(a1)))  # clockwise tangent
    n = (-t[1], t[0])
    tip = (end[0] + t[0] * 0.8, end[1] + t[1] * 0.8)
    h = 2.5
    head = [(tip[0] - h * t[0] + h * n[0], tip[1] - h * t[1] + h * n[1]), tip,
            (tip[0] - h * t[0] - h * n[0], tip[1] - h * t[1] - h * n[1])]
    return [arc(cx, cy, r, a0, a1), poly(head, r=S.r * 0.5)]


@icon("recurring", CAT, "Calendar page with a looping arrow over its corner; a recurring event.",
      tags=["recurring", "repeat", "repeating event", "every week", "routine", "cycle"], aliases=["repeat-event"],
      filled=lambda: _cut_cal_filled(U(*(ST(d, 2.5, "butt") for d in _loop(LINE, *CLK)))))
def _(S):
    return [*_cut_cal(S), *(line(d) for d in _loop(S, *CLK))]


@icon("time-zone", CAT, "Globe with a small clock over its lower right; time zones.",
      tags=["time zone", "timezone", "world clock", "utc", "gmt", "global time"], aliases=["timezone"],
      filled=lambda: U(D(P(circle(10, 10, 8)), P(circle(*CLK[:2], CLK[2] + 3.25)),
                         ST(ellipse(10, 10, 3, 7), 2.0), ST("M2 10H18", 2.0)),
                       D(P(circle(*CLK[:2], CLK[2] + 1)), ST("M17 14.75V17L18.5 18", 1.75))))
def _(S):
    cx, cy, r = CLK
    keep = _away(cx, cy, r + 4 + (1 if S.name != "line" else 0))
    globe = _trimmed_closed(_circle_pts(10, 10, 7), keep)
    meridian = _trimmed_closed(_circle_pts(10, 10, 0, 3, 7), keep)
    equator = _runs([(3 + i * 0.25, 10) for i in range(57)], keep)
    out = [line(_poly_d(rn)) for rn in globe + meridian + equator]
    return [*out, shell(circle(cx, cy, r)), detail(poly([(17, 14.75), (17, 17), (18.5, 18)], r=S.r * 0.5))]


# ============================================================================ calendars

def _dots6(S):
    return [dot(x, y, 1.25) for y in (14, 18) for x in (8, 12, 16)]


@icon("calendar-days", CAT, "Calendar page with a grid of days.",
      tags=["calendar", "days", "month", "date grid", "planner", "dates"], aliases=["calendar-month"],
      filled=_cal_filled(_dots6))
def _(S):
    return [*_cal(S), *_dots6(S)]


@icon("calendar-week", CAT, "Calendar page with one highlighted week row.",
      tags=["week", "calendar", "weekly", "7 days", "planner", "row"], aliases=["weekly"],
      filled=_cal_filled(lambda S: [Part("dot", rect(6, 13, 12, 4, 1))]))
def _(S):
    return [*_cal(S), Part("dot", rect(6, 13, 12, 4, 0 if S.name == "line" else 2))]


def _range(S):
    return [dot(7.5, 15.5, 2), detail(seg(9.5, 15.5, 14.5, 15.5)), dot(16.5, 15.5, 2)]


@icon("calendar-range", CAT, "Calendar page with a start and end day joined; a date range.",
      tags=["date range", "range", "period", "from to", "duration", "calendar"], aliases=["date-range"],
      filled=_cal_filled(_range))
def _(S):
    return [*_cal(S), *_range(S)]


def _event(S):
    return [Part("dot", rect(6, 13, 5.5, 5, 0 if S.name == "line" else 1.25))]


@icon("calendar-event", CAT, "Calendar page with one day blocked out for an event.",
      tags=["event", "appointment", "calendar", "booking", "meeting", "date"], aliases=["event"],
      filled=_cal_filled(_event))
def _(S):
    return [*_cal(S), *_event(S)]


def _today(S):
    return [detail(circle(12, 15.5, 2.5))]


@icon("calendar-today", CAT, "Calendar page with today's date ringed.",
      tags=["today", "current date", "now", "calendar", "day", "date"], aliases=["today"],
      filled=_cal_filled(_today))
def _(S):
    return [*_cal(S), *_today(S)]


def _weekend(S):
    return [dot(7, 14, 1.25), dot(7, 18, 1.25), dot(11, 14, 1.25), dot(11, 18, 1.25),
            Part("dot", rect(14, 12.5, 4.5, 7, 0 if S.name == "line" else 1.25))]


@icon("weekend", CAT, "Calendar page with the last two days of the week highlighted.",
      tags=["weekend", "saturday", "sunday", "days off", "calendar", "holiday"],
      filled=_cal_filled(_weekend))
def _(S):
    return [*_cal(S), *_weekend(S)]


def _picker(S):
    return [detail(poly([(8, 5), (6, 7), (8, 9)], r=S.r * 0.5)), detail(poly([(16, 5), (18, 7), (16, 9)], r=S.r * 0.5)),
            detail(seg(11, 7, 13, 7)),
            dot(7.5, 13, 1.25), dot(12, 13, 1.25), dot(16.5, 13, 1.25), dot(7.5, 17, 1.25), square(10.5, 15.5, 3),
            dot(16.5, 17, 1.25)]


@icon("date-picker", CAT, "Month panel with previous and next arrows and a selected day; pick a date.",
      tags=["date picker", "datepicker", "choose date", "calendar input", "select date", "form"], aliases=["datepicker"],
      filled=lambda: D(P(rect(2, 2, 20, 20, 2)), *_knock(_picker(LINE))))
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), *_picker(S)]
