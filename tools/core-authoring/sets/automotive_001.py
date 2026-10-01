"""TypeIcon Core: automotive (batch 001): dashboard pictograms, cabin controls, engine bay, drivetrain and wheel parts.

Dashboard symbols are drawn as plain pictograms (lamp domes with beam lines, gauges, a steering wheel). Mechanical
parts are drawn flat from the side or front so each reads at 24 px. Side-view cars face right with their wheels on one
ground line and the body left open where a wheel crosses it (Filled cuts the body clear of the solid wheels).
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    rect, regular, seg, shell, solid,
)
from geometry import polar

CAT = "automotive"
FILL = Style("filled", "butt", "miter", R=2.0, r=0.0)  # pseudo-style: Line geometry for Filled designs


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def L(S, a, b):
    """Value for Line/Filled (a) or Rounded (b)."""
    return b if S.name == "rounded" else a


def rk(S, cap):
    """Square corners in Line, rounded (up to cap) in Rounded and Filled."""
    return 0 if S.name == "line" else min(S.R, cap)


def pip(S, x, y, r=1.2):
    """Small solid mark: square in Line, round otherwise."""
    if S.name == "line":
        return Part("dot", rect(x - r, y - r, 2 * r, 2 * r))
    return dot(x, y, r)


def isF(S):
    return S.name == "filled"


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def knock(d):
    """Solid mark that becomes a hole where it sits inside a Filled shell."""
    return Part("dot", d)


def head(tip, deg, size=2.6, spread=40):
    """Open arrowhead polyline whose tip is `tip` and which points toward `deg` (0 = right, 90 = down)."""
    a = polar(tip[0], tip[1], size, deg + 180 - spread)
    b = polar(tip[0], tip[1], size, deg + 180 + spread)
    return [a, tip, b]


def arrow(S, pts_line, tip, deg, size=2.6, spread=40, kind=line):
    return [kind(pts_line), kind(poly(head(tip, deg, size, spread), r=S.r * 0.5))]


def gear_pts(cx, cy, ro, ri, n, hw_out=9.0, hw_in=12.0, start=0.0):
    pts = []
    for i in range(n):
        a = start + i * 360.0 / n
        for rad, off in ((ri, -hw_in), (ro, -hw_out), (ro, hw_out), (ri, hw_in)):
            pts.append(polar(cx, cy, rad, a + off))
    return pts


def lamp(S, x0=3.0, x1=12.0, y0=5.0, y1=19.0):
    """Headlamp dome: D shape, flat on the right."""
    ym = (y0 + y1) / 2
    k = (x1 - x0) * 0.62
    return f"M{fmt(x1)} {fmt(y0)}C{fmt(x1 - k)} {fmt(y0)} {fmt(x0)} {fmt(ym - 3.5)} {fmt(x0)} {fmt(ym)}C{fmt(x0)} {fmt(ym + 3.5)} {fmt(x1 - k)} {fmt(y1)} {fmt(x1)} {fmt(y1)}Z"


# ------------------------------------------------------------------ wheeled cars (copied technique from vehicles)

def wheel(x, y, r=2.0):
    p = shell(circle(x, y, r))
    p.wheel = (x, y, r)
    return p


def car_parts(S, pts, ws, yb=None, T=None, s=1.0):
    """Side-view car body (open where wheels cross it) plus wheels. T maps local points to the grid."""
    T = T or (lambda p: p)
    yb = ws[0][1] if yb is None else yb
    if isF(S):
        out = [shell(poly([T(p) for p in pts], closed=True))]
    else:
        gaps = []
        for x, y, wr in ws:
            dy = yb - y
            if abs(dy) < wr:
                h = math.sqrt(wr * wr - dy * dy)
                gaps.append((x - h, x + h))
        gaps.sort()
        out = [shell(poly([T((gaps[0][0], yb))] + [T(p) for p in pts] + [T((gaps[-1][1], yb))], r=S.r))]
        for a, b in zip(gaps, gaps[1:]):
            if b[0] - a[1] > 0.5:
                out.append(line(seg(*T((a[1], yb)), *T((b[0], yb)))))
    for x, y, r in ws:
        cx, cy = T((x, y))
        out.append(wheel(cx, cy, r * s))
    return out


def veh_filled(fn):
    def f():
        parts = fn(FILL)
        wh = [p.wheel for p in parts if getattr(p, "wheel", None)]
        rest = [p for p in parts if not getattr(p, "wheel", None)]
        out = filled_region(rest) if rest else None
        if wh:
            cut = U(*[P(circle(x, y, r + 2)) for x, y, r in wh])
            discs = U(*[P(circle(x, y, r + 1)) for x, y, r in wh])
            out = U(D(out, cut), discs) if out is not None else discs
        return out
    return f


def vcar(name, description, tags, aliases=()):
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=veh_filled(fn))(fn)
    return deco


def T_(name, description, tags, aliases=()):
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=lambda: filled_region(fn(FILL)))(fn)
    return deco


CAR = [(2.5, 17.5), (2.5, 13), (5.5, 11.5), (8, 6), (15, 6), (18.5, 11), (21.5, 12.5), (21.5, 17.5)]
CARW = [(7, 17.5, 2.5), (17, 17.5, 2.5)]


# =========================================================================== dashboard lights, part 1

@T_("dpf-warning-light", "Exhaust filter box with a pipe at each end and a grid of dots inside",
    ["diesel particulate filter", "dpf", "exhaust filter", "soot", "dashboard light", "warning lamp", "diesel"])
def _(S):
    return [shell(rect(6, 6.5, 12, 11, rr(S, 2.5))), line(seg(2, 12, 6, 12)), line(seg(18, 12, 22, 12)),
            dot(9.5, 10, 0.9), dot(12, 10, 0.9), dot(14.5, 10, 0.9),
            dot(9.5, 14, 0.9), dot(12, 14, 0.9), dot(14.5, 14, 0.9)]


@T_("diesel-exhaust-fluid-light", "Small fluid tank with a filler neck and a droplet, with an exhaust pipe below",
    ["def", "adblue", "urea", "scr", "diesel exhaust fluid", "dashboard light", "warning lamp", "diesel"])
def _(S):
    drop = "M8.5 10.5C8.5 10.5 6 13.3 6 15A2.5 2.5 0 0 0 11 15C11 13.3 8.5 10.5 8.5 10.5Z"
    return [shell(union(rect(3, 7, 12, 10, rr(S, 2)), rect(5.5, 3, 5, 5, 0.5))),
            knock(drop),
            line(poly([(9, 17), (9, 21), (21, 21)], r=S.r))]


@T_("transmission-temperature-light", "Gear cog with a small thermometer standing in its center",
    ["gearbox temperature", "transmission overheating", "gear oil", "dashboard light", "warning lamp", "atf", "overheat"])
def _(S):
    return [shell(poly(gear_pts(12, 12, 9.5, 7.5, 8, 9, 12), closed=True, r=S.r * 0.4)),
            detail(seg(10.5, 7.5, 10.5, 13)), knock(circle(10.5, 15.3, 2.3)),
            detail(seg(13, 8.5, 16, 8.5)), detail(seg(13, 12, 16, 12))]


@T_("immobilizer-light", "Car side silhouette with a small key inside the cabin",
    ["immobiliser", "anti theft", "key light", "security light", "car key", "dashboard light", "ignition"])
def _(S):
    pts = [(2.5, 17.5), (2.5, 13.5), (5, 12.5), (7.5, 5), (15.5, 5), (19, 11), (21.5, 12.5), (21.5, 17.5)]
    key = union(circle(10.5, 8.8, 1.7), rect(11.5, 8.2, 5, 1.2), rect(14, 9, 1.1, 1.8))
    return car_parts(S, pts, CARW, 17.5) + [knock(key)]


@vcar("hood-open-light", "Side-view car with its front hood propped open at an angle above the engine bay",
      ["bonnet open", "hood ajar", "bonnet ajar", "dashboard light", "warning lamp", "engine cover", "car"])
def _(S):
    pts = [(2.5, 17.5), (2.5, 13), (5, 12), (7.5, 6.5), (13, 6.5), (15.5, 11.5), (21.5, 11.5), (21.5, 17.5)]
    return car_parts(S, pts, CARW, 17.5) + [line(seg(15.8, 9.8, 21.5, 3.5))]


@T_("hill-start-assist", "Car on an uphill slope with a curved hold arrow below the slope line",
    ["hill hold", "hsa", "uphill start", "rollback prevention", "slope", "dashboard light", "incline"])
def _(S):
    th = math.atan2(-9, 20)
    c, sn = math.cos(th), math.sin(th)
    sc = 0.7

    def T(p):
        x, y = (p[0] - 12) * sc, (p[1] - 24) * sc
        return (12.6 + x * c - y * sn, 12.8 + x * sn + y * c)

    pts = [(3, 17.5), (3, 12.5), (6, 7.5), (14, 7.5), (17, 11), (21, 12), (21, 17.5)]
    ws = [(6.5, 17.5, 2.8), (17.5, 17.5, 2.8)]
    return (car_parts(S, pts, ws, 17.5, T, sc) + [line(seg(2, 19.5, 22, 10.5))] +
            [line("M6 21.5H19"), line(poly(head((19.8, 21.5), 0, 2.4, 45), r=S.r * 0.4))])


# =========================================================================== lamps

def beams(S, ys, x0=14.5, x1=21.5):
    return [line(seg(x0, y, x1, y)) for y in ys]


A_GLYPH = path_to_d(D(P(poly([(4.2, 16), (7.2, 7.5), (9.8, 7.5), (12.8, 16), (10.6, 16), (10, 14.2), (7, 14.2), (6.4, 16)], closed=True)),
                      P(poly([(7.6, 12.4), (8.5, 9.6), (9.4, 12.4)], closed=True))))


@T_("automatic-high-beam", "Headlamp dome with beam lines and a capital A inside the lamp",
    ["auto high beam", "high beam assist", "automatic main beam", "dashboard light", "headlight", "auto lights", "full beam"])
def _(S):
    return [shell(lamp(S, 2, 15, 4, 20)), knock(A_GLYPH)] + beams(S, (7, 12, 17), 18, 22)


@T_("adaptive-headlights", "Headlamp dome with a curved double-headed arrow sweeping across its beam lines",
    ["cornering lights", "swivel headlights", "afs", "adaptive front lighting", "dashboard light", "bending lights", "headlight"])
def _(S):
    cx, cy, r = 8, 12, 12.5
    t1, t2 = polar(cx, cy, r, -40), polar(cx, cy, r, 40)
    return [shell(lamp(S, 2, 9, 6, 18))] + beams(S, (9, 12, 15), 12, 16.5) + [
        line(arc(cx, cy, r, -40, 40)),
        line(poly(head(t1, -130, 2.6), r=S.r * 0.4)), line(poly(head(t2, 130, 2.6), r=S.r * 0.4))]


@T_("headlight-leveling", "Headlamp dome with slanted beam lines and a vertical up and down arrow beside it",
    ["headlight levelling", "headlamp leveling", "beam height", "headlight aim", "dashboard light", "beam adjust", "lamp tilt"])
def _(S):
    return [shell(lamp(S, 2, 10, 6, 18)),
            line(seg(13, 8, 17, 10.5)), line(seg(13, 12, 17, 14.5)), line(seg(13, 16, 17, 18.5)),
            line(seg(21, 5, 21, 19)),
            line(poly(head((21, 4), -90, 2.4), r=S.r * 0.4)), line(poly(head((21, 20), 90, 2.4), r=S.r * 0.4))]


@T_("daytime-running-lights", "Headlamp dome with short beam lines below a small sun",
    ["drl", "day running lamps", "daylight running lights", "dashboard light", "headlight", "auto lights", "sun"])
def _(S):
    sx, sy = 17, 6
    sun = [dot(sx, sy, 1.8)] + [line(seg(*polar(sx, sy, 3.5, a), *polar(sx, sy, 4.9, a))) for a in range(0, 360, 45)]
    return [shell(lamp(S, 2, 11, 10, 21))] + beams(S, (12.5, 15.5, 18.5), 14, 20) + sun


@T_("regenerative-braking", "Wheel with a circular arrow around it and a small lightning bolt at the hub",
    ["regen braking", "energy recovery", "electric car brake", "ev", "kinetic recovery", "hybrid", "dashboard light"])
def _(S):
    bolt = poly([(13.2, 8.4), (10, 12.6), (11.9, 12.6), (10.8, 15.8), (14, 11.4), (12.1, 11.4)], closed=True)
    e = polar(12, 12, 9, -60)
    return [shell(circle(12, 12, 4.8)), knock(bolt),
            line(arc(12, 12, 9, 30, 300)), line(poly(head(e, 30, 2.8), r=S.r * 0.4))]


# =========================================================================== driver assistance

@T_("adaptive-cruise-control", "Small speedometer dial with a car ahead of it, separated by a column of distance dots",
    ["acc", "radar cruise control", "following distance", "distance control", "smart cruise", "driver assist", "dashboard light"])
def _(S):
    car = poly([(6.5, 7.5), (6.5, 5.5), (8.5, 2.5), (15.5, 2.5), (17.5, 5.5), (17.5, 7.5)], closed=True, r=S.r * 0.5)
    return [shell(car), dot(8.8, 8.6, 1.2), dot(15.2, 8.6, 1.2),
            dot(12, 11.3, 0.9), dot(12, 13.6, 0.9),
            line(arc(12, 21.5, 5.5, 180, 360)), line(seg(12, 21.5, 15, 18.3))]


@T_("speed-limiter", "Round speed dial with the needle stopped against a short bar across the scale",
    ["speed limit", "speed governor", "max speed", "intelligent speed", "limiter", "dashboard light", "cruise limit"])
def _(S):
    cx, cy = 12, 12
    ang = -50
    n0, n1 = polar(cx, cy, 0, ang), polar(cx, cy, 4.2, ang)
    b = polar(cx, cy, 6.9, ang)
    ux, uy = math.cos(math.radians(ang + 90)), math.sin(math.radians(ang + 90))
    return [line(arc(12, 12, 9, 120, 60)), line(seg(*n0, *n1)), dot(12, 12, 1.7),
            line(seg(b[0] - 2.1 * ux, b[1] - 2.1 * uy, b[0] + 2.1 * ux, b[1] + 2.1 * uy))]


def wheel_disc(S, r=9.0):
    return shell(circle(12, 12, r))


@T_("driver-fatigue-warning", "Steering wheel disc with a steaming coffee cup in its center",
    ["drowsiness", "take a break", "tiredness alert", "attention assist", "coffee", "sleepy driver", "dashboard light"])
def _(S):
    cup = poly([(8.8, 11.2), (15.2, 11.2), (14.4, 16.6), (9.6, 16.6)], closed=True, r=S.r * 0.3)
    return [wheel_disc(S), detail(cup), detail("M15 12.4C17.6 12.4 17.6 15.6 14.8 15.6"),
            detail("M10.6 9.5C9.6 8.4 11.6 7.6 10.6 6.5"), detail("M13.4 9.5C12.4 8.4 14.4 7.6 13.4 6.5")]


@T_("traffic-sign-recognition", "Car side silhouette with a small round road sign above its hood",
    ["tsr", "speed sign detection", "road sign reader", "sign assist", "camera", "driver assist", "dashboard light"])
def _(S):
    k = 0.82

    def T(p):
        return (10.6 + (p[0] - 12) * k, 20 + (p[1] - 20) * k)
    pts = [(2.5, 17.5), (2.5, 13), (5.5, 11.5), (8, 6), (15, 6), (18.5, 11), (21.5, 12.5), (21.5, 17.5)]
    ws = [(7, 17.5, 2.6), (17, 17.5, 2.6)]
    return car_parts(S, pts, ws, 17.5, T, k) + [shell(circle(18.4, 5.4, 3.0)), knock(circle(18.4, 5.4, 0.9))]


@T_("pedestrian-detection", "Front of a car with a person walking ahead of it inside two scan arcs",
    ["pedestrian alert", "aeb", "collision avoidance", "person ahead", "emergency braking", "driver assist", "dashboard light"])
def _(S):
    car = poly([(4, 21), (4, 18), (6.5, 14.5), (17.5, 14.5), (20, 18), (20, 21)], closed=True, r=S.r)
    return [dot(12, 3.4, 1.6), line(seg(12, 5.8, 12, 9.2)),
            line(seg(9.6, 7.6, 14.4, 7.6)),
            line(poly([(10, 12.6), (12, 9.2), (14, 12.6)])),
            line("M7 4Q5.2 7.5 7 11"), line("M17 4Q18.8 7.5 17 11"),
            shell(car), dot(7.8, 18, 1.1), dot(16.2, 18, 1.1)]


@T_("park-assist", "Steering wheel with a bold capital P in its center",
    ["parking assist", "auto park", "parking aid", "self parking", "parking sensor", "driver assist", "dashboard light"])
def _(S):
    return [wheel_disc(S), detail("M10.2 17V7.5H13A2.9 2.9 0 0 1 13 13.3H10.2")]


def seat_side(extra_back=None, lumbar=False):
    if lumbar:
        return "M3.5 4L8.2 3.2L9 7.5Q11.8 10 9.8 12H21V17H3.5Z"
    return "M3.5 4L8.2 3.2L9.6 12H21V17H3.5Z"


def up_arrow(S, x, y0, y1):
    return [line(seg(x, y0, x, y1)), line(poly(head((x, y1), -90, 2.4), r=S.r * 0.4))]


@T_("ventilated-seat", "Side view of a car seat with two airflow arrows rising above the cushion",
    ["seat ventilation", "cooled seat", "seat cooling", "air seat", "climate seat", "car comfort", "cooling"])
def _(S):
    return ([shell(seat_side()), line(seg(6, 20.5, 18, 20.5))] +
            up_arrow(S, 14.5, 9.5, 4) + up_arrow(S, 19, 9.5, 4))


@T_("lumbar-support", "Side view of a car seat with an arrow pushing out from the lower backrest",
    ["lumbar adjust", "lower back support", "seat back support", "backrest bulge", "ergonomic seat", "car comfort", "seat adjust"])
def _(S):
    return [shell(seat_side(lumbar=True)), line(seg(6, 20.5, 18, 20.5)),
            line(poly([(13.5, 7), (19, 7)])), line(poly(head((19.5, 7), 0, 2.4), r=S.r * 0.4))]


@T_("fresh-air-intake", "Side-view car with a curved arrow entering the cabin from outside at the front",
    ["fresh air mode", "outside air", "air intake", "recirculation off", "cabin air", "ventilation", "climate control"])
def _(S):
    k = 0.8

    def T(p):
        return (12 + (p[0] - 12) * k, 20.5 + (p[1] - 20.5) * k)
    pts = [(2.5, 17.5), (2.5, 13), (5.5, 11.5), (8, 6), (15, 6), (18.5, 11), (21.5, 12.5), (21.5, 17.5)]
    ws = [(7, 17.5, 2.6), (17, 17.5, 2.6)]
    return car_parts(S, pts, ws, 17.5, T, k) + [line("M22 3.5Q16 3.5 14.2 11"), line(poly(head((14.2, 11.6), 105, 2.6), r=S.r * 0.4))]


@T_("climate-airflow-mode", "Seated person in side view with one arrow blowing at the face and one at the feet",
    ["air direction", "vent mode", "face and feet", "airflow selector", "hvac mode", "climate control", "blower"])
def _(S):
    return [dot(7, 4.5, 1.8), line(seg(7, 7.5, 7, 14.5)), line(poly([(7, 14.5), (13, 14.5), (13, 20.5), (15.5, 20.5)])),
            line(seg(22, 4.5, 12.5, 4.5)), line(poly(head((12, 4.5), 180, 2.4), r=S.r * 0.4)),
            line(seg(22, 20.5, 18.5, 20.5)), line(poly(head((18, 20.5), 180, 2.4), r=S.r * 0.4))]


def a_glyph(cx, cy, k):
    def m(pts):
        return [(cx + (x - 8.5) * k, cy + (y - 11.75) * k) for x, y in pts]
    outer = poly(m([(4.2, 16), (7.2, 7.5), (9.8, 7.5), (12.8, 16), (10.6, 16), (10, 14.2), (7, 14.2), (6.4, 16)]), closed=True)
    inner = poly(m([(7.6, 12.4), (8.5, 9.6), (9.4, 12.4)]), closed=True)
    return path_to_d(D(P(outer), P(inner)))


@T_("auto-brake-hold", "Ring with a capital A inside and curved brackets on both sides",
    ["brake hold", "auto hold", "autohold", "parking brake auto", "hold function", "brake light", "dashboard light"])
def _(S):
    return [shell(circle(12, 12, 6)), knock(a_glyph(12, 12.2, 0.8)),
            line(arc(12, 12, 9.4, 148, 212)), line(arc(12, 12, 9.4, -32, 32))]


@T_("drive-mode-dial", "Round rotary knob seen from above with a pointer and a row of mode dots around its rim",
    ["driving mode selector", "mode knob", "terrain select", "sport eco dial", "rotary selector", "drive select", "console dial"])
def _(S):
    dots = [pip(S, *polar(12, 14, 9.2, a), 1.2) for a in (-180, -135, -90, -45, 0)]
    return [shell(circle(12, 14, 5.6)), detail(seg(12, 14, *polar(12, 14, 4.4, -45))), pip(S, 12, 14, 1.0)] + dots


def strip_marks():
    box = P(rect(8, 14.8, 8, 5.2, 1.0))
    glyph = ST("M10.2 16.2V18.6H11.3A1.2 1.2 0 0 0 11.3 16.2Z", 1.0, "butt", "miter", 4)
    return path_to_d(D(box, glyph))


@T_("prnd-gear-indicator", "Vertical gear strip with three small marks above a highlighted box for drive",
    ["gear selector", "park reverse neutral drive", "shift indicator", "automatic transmission", "gear display", "prnd", "shifter"])
def _(S):
    return [shell(rect(6.5, 2.5, 11, 19, rr(S, 3))), dot(12, 6.2, 1.0), dot(12, 9.4, 1.0), dot(12, 12.6, 1.0),
            knock(strip_marks())]


@T_("paddle-shifters", "Steering wheel front view with a paddle standing behind the rim on each side",
    ["steering wheel paddles", "gear paddles", "flappy paddles", "manual shift", "sequential shift", "race car", "gear change"])
def _(S):
    return [line(circle(12, 12.5, 6.2)), line(seg(5.8, 12.5, 18.2, 12.5)), line(seg(12, 12.5, 12, 18.7)),
            line("M3 7Q1.8 12.5 3 18"), line("M21 7Q22.2 12.5 21 18")]


@T_("power-window-switch", "Door panel with a rocker switch below a window outline that has an up and down arrow",
    ["window control", "window button", "electric window", "window lifter", "car door switch", "window up down", "door panel"])
def _(S):
    return [shell(poly([(3.5, 3), (14, 3), (17, 9.5), (3.5, 9.5)], closed=True, r=S.r * 0.5)),
            line(seg(20, 4, 20, 9)), line(poly(head((20, 3.4), -90, 2.2), r=S.r * 0.4)),
            shell(rect(3, 13, 18, 8, rr(S, 2.5))), detail(rect(6.5, 15.3, 11, 3.4, 0.6))]


@T_("power-seat-control", "Seat-shaped switch panel with a vertical backrest slot and a horizontal cushion slot",
    ["seat adjust switch", "electric seat", "seat memory", "seat position", "seat switch", "car seat control", "adjust seat"])
def _(S):
    return [shell(poly([(3.5, 3), (10, 3), (10.5, 12), (20.5, 12.5), (20.5, 21), (3.5, 21)], closed=True, r=S.r * 0.6)),
            detail(seg(6.7, 6.5, 6.7, 10.5)), detail(seg(12.5, 16.7, 17.5, 16.7)), dot(6.7, 15.5, 1.1)]


@T_("center-console", "Top view of the space between two seats with a padded armrest lid and a gear lever ahead of it",
    ["armrest", "storage box", "console box", "gear lever", "cup holder area", "car interior", "between seats"])
def _(S):
    return [shell(rect(2, 6, 4.5, 15, rk(S, 2.2))), shell(rect(17.5, 6, 4.5, 15, rk(S, 2.2))),
            shell(rect(9, 3, 6, 18, rk(S, 3))), detail(seg(9, 11.5, 15, 11.5)), pip(S, 12, 7, 1.5)]


@T_("car-12v-socket", "Round accessory power socket with a center pin and a lid flipped up on a strap",
    ["cigarette lighter socket", "power outlet", "12 volt outlet", "accessory socket", "car charger port", "dc socket", "car power"])
def _(S):
    return [shell(circle(12, 15, 6.5)), pip(S, 12, 15, 2.0), shell(rect(8.5, 2.5, 7, 3.5, rk(S, 1.7))), line(seg(12, 6, 12, 8.5))]


@T_("car-headrest", "Rounded headrest pad sitting on two metal posts",
    ["head restraint", "seat headrest", "neck rest", "car seat part", "seat pillow", "upholstery", "whiplash"])
def _(S):
    return [shell(rect(5.5, 3, 13, 9, rr(S, 4))), line(seg(9, 12, 9, 21)), line(seg(15, 12, 15, 21))]


@T_("car-floor-mat", "Rubber floor mat outline with a cut corner and diagonal groove lines across it",
    ["footwell mat", "rubber mat", "carpet mat", "all weather mat", "interior protection", "car carpet", "floor liner"])
def _(S):
    return [shell(poly([(9, 3), (19, 3), (19, 21), (4.5, 21), (4.5, 7.5)], closed=True, r=S.r * 0.5)),
            detail(seg(8, 18, 16, 10)), detail(seg(8, 13.5, 14, 7.5))]


@T_("vent-clip-air-freshener", "Car air vent with a round air freshener clipped on and scent wave lines beside it",
    ["car freshener", "vent freshener", "scent clip", "car fragrance", "diffuser", "air vent clip", "car smell"])
def _(S):
    return [shell(rect(3, 12, 18, 9, rr(S, 2))), detail(seg(6, 15, 18, 15)), detail(seg(6, 18, 18, 18)),
            shell(circle(12, 7, 3.2)), line("M17.5 3.5Q19.5 6 17.5 8.5"), line("M6.5 3.5Q4.5 6 6.5 8.5")]


# =========================================================================== engine bay

def mirror_x(pts):
    return [(24 - x, y) for x, y in pts]


@T_("cylinder-head", "Flat engine head casting with a row of spark plug holes above a row of valve holes",
    ["engine head", "head casting", "valve head", "combustion chamber", "engine block part", "motor", "head gasket"])
def _(S):
    xs = (6, 10, 14, 18)
    return ([shell(rect(2.5, 6.5, 19, 11, rr(S, 2.5)))] + [dot(x, 10.5, 1.5) for x in xs] + [dot(x, 14.6, 0.85) for x in xs])


def belt_geom(c1, r1, c2, r2):
    """Outer-tangent loop around two circles (r1 >= r2). Returns (path d, list of arc/line pieces)."""
    dx, dy = c2[0] - c1[0], c2[1] - c1[1]
    d = math.hypot(dx, dy)
    phi = math.degrees(math.atan2(dy, dx))
    al = math.degrees(math.acos((r1 - r2) / d))
    p1a, p2a = polar(c1[0], c1[1], r1, phi + al), polar(c2[0], c2[1], r2, phi + al)
    p2b, p1b = polar(c2[0], c2[1], r2, phi - al), polar(c1[0], c1[1], r1, phi - al)
    dpath = (f"M{fmt(p1a[0])} {fmt(p1a[1])}L{fmt(p2a[0])} {fmt(p2a[1])}A{fmt(r2)} {fmt(r2)} 0 0 0 {fmt(p2b[0])} {fmt(p2b[1])}"
             f"L{fmt(p1b[0])} {fmt(p1b[1])}A{fmt(r1)} {fmt(r1)} 0 1 0 {fmt(p1a[0])} {fmt(p1a[1])}")
    pieces = [("L", p1a, p2a), ("A", c2, r2, phi + al, phi - al), ("L", p2b, p1b), ("A", c1, r1, phi - al, phi + al - 360)]
    return dpath, pieces


def sample_loop(pieces, n):
    """n points evenly spaced along the loop."""
    lens = []
    for pc in pieces:
        lens.append(math.dist(pc[1], pc[2]) if pc[0] == "L" else pc[2] * math.radians(abs(pc[4] - pc[3])))
    total = sum(lens)
    out = []
    for i in range(n):
        t = (i + 0.5) * total / n
        for pc, ln in zip(pieces, lens):
            if t <= ln:
                f = t / ln
                if pc[0] == "L":
                    out.append((pc[1][0] + (pc[2][0] - pc[1][0]) * f, pc[1][1] + (pc[2][1] - pc[1][1]) * f))
                else:
                    out.append(polar(pc[1][0], pc[1][1], pc[2], pc[3] + (pc[4] - pc[3]) * f))
                break
            t -= ln
    return out


BELT_C1, BELT_C2 = (8.5, 14), (17, 8.5)


def sprocket(S, c, ro, ri, n):
    return poly(gear_pts(c[0], c[1], ro, ri, n, 100.0 / n, 150.0 / n), closed=True, r=S.r * 0.3)


@T_("timing-belt", "Toothed belt looped around two round pulleys, one large and one small",
    ["cam belt", "cambelt", "engine belt", "drive belt", "toothed belt", "pulley belt", "engine timing"])
def _(S):
    dpath, _p = belt_geom(BELT_C1, 5.6, BELT_C2, 3.8)
    return [line(dpath), shell(sprocket(S, BELT_C1, 3.0, 2.2, 8)), shell(sprocket(S, BELT_C2, 1.9, 1.3, 6))]


@T_("timing-chain", "Link chain looped around two sprockets of different sizes",
    ["cam chain", "engine chain", "roller chain", "sprocket chain", "chain drive", "engine timing", "chain loop"])
def _(S):
    _d, pieces = belt_geom(BELT_C1, 5.6, BELT_C2, 3.8)
    pts = sample_loop(pieces, 15)
    return [shell(sprocket(S, BELT_C1, 3.0, 2.2, 8)), shell(sprocket(S, BELT_C2, 1.9, 1.3, 6))] + [dot(x, y, 1.15) for x, y in pts]


@T_("ignition-coil", "Pencil-shaped ignition coil with a connector block on top and a long boot below",
    ["coil pack", "spark coil", "coil on plug", "ignition", "engine part", "spark plug coil", "petrol engine"])
def _(S):
    return [shell(union(rect(7, 2.5, 10, 5, rr(S, 1.5)), rect(8.5, 7.5, 7, 8, 0.5), rect(10.5, 15.5, 3, 6, 0.5))),
            detail(seg(8.5, 11.5, 15.5, 11.5)), dot(12, 5, 1.0)]


@T_("supercharger", "Rectangular blower case with a belt pulley on its front end and an intake scoop on top",
    ["blower", "roots blower", "forced induction", "compressor drive", "engine boost", "belt driven blower", "performance engine"])
def _(S):
    return [shell(union(rect(8, 9.5, 13, 10, rr(S, 2.5)), rect(11.5, 3.5, 6, 6.5, rr(S, 1)))),
            shell(circle(4.6, 14.5, 2.3)), line(seg(6.9, 14.5, 8, 14.5)), detail(seg(11, 14.5, 18, 14.5))]


@T_("intercooler", "Wide flat finned radiator core with a pipe stub at each end",
    ["charge air cooler", "turbo cooler", "air cooler", "heat exchanger", "boost cooler", "radiator core", "turbo"])
def _(S):
    return [shell(rect(5, 7, 14, 10, rr(S, 2))), detail(seg(8.5, 9, 8.5, 15)), detail(seg(12, 9, 12, 15)), detail(seg(15.5, 9, 15.5, 15)),
            line(seg(2, 9.5, 5, 9.5)), line(seg(19, 14.5, 22, 14.5))]


@T_("intake-manifold", "Horizontal plenum with four curved runner pipes dropping down side by side",
    ["inlet manifold", "air manifold", "plenum", "runners", "engine air intake", "intake runners", "induction"])
def _(S):
    runs = [("M6.5 8V12Q6.5 16 3.8 21", None), ("M10 8V13Q10 17 8 21", None),
            ("M14 8V13Q14 17 16 21", None), ("M17.5 8V12Q17.5 16 20.2 21", None)]
    return [shell(rect(2.5, 3, 19, 5, rr(S, 2.5)))] + [line(d) for d, _ in runs]


@T_("exhaust-manifold", "Four curved pipes merging into a single collector pipe",
    ["header", "exhaust header", "exhaust pipes", "collector", "engine exhaust", "manifold", "tuning"])
def _(S):
    return [line(seg(2.5, 3, 21.5, 3)), line("M4.5 3V7Q4.5 13 12 14.5"), line("M9 3V7Q9 12 12 14.5"),
            line("M15 3V7Q15 12 12 14.5"), line("M19.5 3V7Q19.5 13 12 14.5"), line(seg(12, 14.5, 12, 21.5))]


def rot_d(d, deg, cx=12.0, cy=12.0):
    from geometry import rotation, transform_path
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


@T_("throttle-body", "Round tube housing with a leaf-shaped butterfly valve inside and a lever on its side",
    ["butterfly valve", "air throttle", "throttle valve", "intake throttle", "engine air control", "drive by wire", "carburetor"])
def _(S):
    return [shell(circle(10.5, 13.5, 7.5)), detail(ellipse(10.5, 13.5, 2.3, 5.1)),
            line("M18 13.5H21.5V8")]


@T_("fuel-filter", "Small canister with a hose barb at each end and an arrow marking the flow direction",
    ["petrol filter", "diesel filter", "inline filter", "fuel line filter", "fuel system", "filter cartridge", "gas filter"])
def _(S):
    return [shell(rect(7, 6, 10, 12, rr(S, 3))), line(seg(2.5, 12, 7, 12)), line(seg(17, 12, 21.5, 12)),
            line(seg(4, 9.8, 4, 14.2)), line(seg(20, 9.8, 20, 14.2)),
            detail(seg(9.5, 12, 14, 12)), detail(poly([(12.4, 9.8), (14.8, 12), (12.4, 14.2)]))]


@T_("radiator-cap", "Round pressure cap seen from above with a ridged ring and two short ear tabs at its sides",
    ["coolant cap", "pressure cap", "radiator lid", "expansion tank cap", "cooling system", "antifreeze cap", "engine cooling"])
def _(S):
    ring = path_to_d(D(P(circle(12, 12, 3.2)), P(circle(12, 12, 1.7))))
    return [shell(union(circle(12, 12, 6.8), rect(2.5, 10, 19, 4, rr(S, 1.5)))), knock(ring)] + \
        [dot(*polar(12, 12, 5.0, a), 0.6) for a in (45, 135, 225, 315)]


def blade(S, deg):
    if S.name == "line":
        return rot_d("M12 10.3C8.4 9.4 8.6 6 12 3.8C15.4 6 15.6 9.4 12 10.3Z", deg)
    return rot_d("M12 10.3C8.6 9 8.6 5.2 11.6 4.2C14.4 4.8 14.8 8.8 12 10.3Z", deg)


@T_("radiator-fan", "Round shroud with a five-bladed fan and a motor hub at its center",
    ["cooling fan", "engine fan", "electric fan", "fan shroud", "radiator cooling", "blower fan", "car cooling"])
def _(S):
    return [line(circle(12, 12, 9.2))] + [shell(blade(S, i * 72)) for i in range(5)] + [pip(S, 12, 12, 1.5)]


@T_("radiator-hose", "Curved rubber hose bent in an S shape with a clamp band near each end",
    ["coolant hose", "rubber hose", "cooling hose", "water hose", "heater hose", "hose clamp", "engine cooling"])
def _(S):
    hose = path_to_d(ST("M4.5 7H8C14 7 10 17 16 17H19.5", 5.2, "butt", "round", 4))
    return [shell(hose), line(seg(6.8, 2.5, 6.8, 11.5)), line(seg(17.4, 12.5, 17.4, 21.5))]


@T_("brake-fluid-reservoir", "Small translucent tank with a screw cap, MIN and MAX marks and a ring symbol on its side",
    ["brake fluid tank", "master cylinder reservoir", "fluid level", "brake fluid", "dot 4", "brake system", "hydraulic reservoir"])
def _(S):
    ring = path_to_d(D(P(circle(9.5, 15.2, 2.5)), P(circle(9.5, 15.2, 1.4))))
    return [shell(union(rect(3.5, 8, 14, 13, rr(S, 2.5)), rect(6.5, 3.5, 8, 4.5, rr(S, 1.5)))),
            knock(ring), detail(seg(13.5, 12, 16, 12)), detail(seg(13.5, 17.5, 16, 17.5)), line(seg(17.5, 19, 22, 19))]


@T_("power-steering-pump", "Round pump body with a pulley on its front and a small fluid reservoir with a cap on top",
    ["steering pump", "hydraulic pump", "power steering fluid", "pump pulley", "engine accessory", "steering system", "psf"])
def _(S):
    return [shell(rect(8, 10, 12, 11, rr(S, 3.5))), shell(rect(2.5, 12, 3.2, 7, rr(S, 1))), line(seg(5.7, 15.5, 8, 15.5)),
            shell(rect(10, 5, 8, 5, rr(S, 1.5))), line(seg(11, 2.8, 17, 2.8)), dot(14, 15.5, 1.7)]


@T_("ac-compressor", "Cylindrical compressor body with a clutch pulley on its front and two pipe ports on top",
    ["air conditioning compressor", "a/c compressor", "aircon compressor", "refrigerant pump", "clutch pulley", "climate system", "hvac"])
def _(S):
    return [shell(rect(9, 8.5, 12, 11.5, rr(S, 3))), shell(rect(3, 10, 4.5, 8, rr(S, 1.5))), line(seg(7.5, 14, 9, 14)),
            line(seg(13, 3.5, 13, 8.5)), line(seg(18, 3.5, 18, 8.5)), detail(seg(12, 14, 18, 14))]


@T_("belt-tensioner", "Idler pulley on a pivoting arm with a coil spring curling around the pivot",
    ["tensioner pulley", "idler pulley", "serpentine belt tensioner", "belt idler", "drive belt tensioner", "engine accessory", "spring tensioner"])
def _(S):
    return [shell(circle(15.5, 8.5, 4.5)), dot(15.5, 8.5, 1.3), shell(circle(6.5, 16.5, 2.0)),
            line(seg(8.2, 15.4, 12.4, 11.6)), line(arc(6.5, 16.5, 5.0, 150, 340))]


@T_("engine-mount", "Rubber block sandwiched between two metal brackets with a bolt stud sticking out of each",
    ["motor mount", "engine bushing", "rubber mount", "vibration damper", "engine support", "mounting block", "dampener"])
def _(S):
    body = union(rect(4, 6, 16, 3, rr(S, 1)), "M7 9L17 9L15.5 15L8.5 15Z", rect(4, 15, 16, 3, rr(S, 1)))
    return [shell(body), line(seg(12, 2.5, 12, 6)), line(seg(12, 18, 12, 21.5))]


@T_("valve-cover", "Long rounded engine cover with a row of bolts along its edge and a filler cap on top",
    ["rocker cover", "cam cover", "engine cover", "tappet cover", "oil filler", "engine top", "motor part"])
def _(S):
    return [shell(union(rect(2.5, 8.5, 19, 10, rr(S, 3)), rect(14, 4.5, 5, 4.5, rr(S, 1.5)))),
            dot(5.5, 12, 1.0), dot(5.5, 15.2, 1.0), dot(18.5, 12, 1.0), dot(18.5, 15.2, 1.0), dot(12, 12, 1.0), dot(12, 15.2, 1.0)]


@T_("rocker-arm", "Tilted pivoting lever with a round pivot hole in the middle resting on a small fulcrum post",
    ["valve rocker", "rocker lever", "valvetrain", "pushrod engine", "engine valve", "pivot arm", "lever arm"])
def _(S):
    arm = rot_d(poly([(2.5, 7.5), (5, 4.5), (19, 4.5), (21.5, 7.5), (19, 10.5), (5, 10.5)], closed=True, r=S.r * 0.6), -9, 12, 7.5)
    return [shell(arm), knock(circle(12, 7.5, 1.3)),
            line(seg(12, 12, 12, 20.5)), line(seg(8, 20.5, 16, 20.5))]


@T_("engine-oil-pan", "Shallow tray-shaped sump with a wide flange rim on top and a drain plug at its lowest point",
    ["sump", "oil sump", "oil pan", "drain plug", "engine oil", "oil change", "crankcase"])
def _(S):
    return [shell(union(rect(2.5, 5, 19, 3.5, rr(S, 1)), "M4.5 8.5L19.5 8.5L18 15L6 15Z")),
            shell(rect(14.5, 15, 4, 3.5, rr(S, 0.8))), line(seg(16.5, 18.5, 16.5, 21))]


@T_("oil-filler-cap", "Round screw cap seen from above with a grip bar across it and an oil drop engraved below",
    ["oil cap", "engine oil cap", "filler cap", "oil fill", "screw cap", "oil can symbol", "engine top"])
def _(S):
    drop = "M12 12.8C12 12.8 9.6 15.6 9.6 17.1A2.4 2.4 0 0 0 14.4 17.1C14.4 15.6 12 12.8 12 12.8Z"
    return [shell(circle(12, 12, 9)), detail(seg(6.5, 8, 17.5, 8)), knock(drop)]


@T_("oxygen-sensor", "Threaded sensor with a hex nut, a slotted protective tip below and a wire leaving its top",
    ["o2 sensor", "lambda sensor", "air fuel sensor", "exhaust sensor", "emissions sensor", "catalytic converter sensor", "oxygen probe"])
def _(S):
    return [shell(union(rect(9.5, 6.5, 5, 5, rr(S, 1)), rect(7, 11.5, 10, 3.5, rr(S, 1)), rect(9.5, 15, 5, 6.5, rr(S, 2)))),
            detail(seg(12, 17.2, 12, 20.5)), line("M12 6.5V4.5Q12 2.8 15 2.8H21.5")]


@T_("egr-valve", "Round valve body on a bolted flange with a small actuator dome and connector lead on top",
    ["exhaust gas recirculation", "egr", "emissions valve", "recirculation valve", "engine emissions", "nox control", "exhaust valve"])
def _(S):
    dome = "M8 9.5C8 5 9.5 3.5 12 3.5C14.5 3.5 16 5 16 9.5Z"
    return [shell(union(dome, rect(5, 9, 14, 6.5, rr(S, 2)), rect(3, 15.5, 18, 4.5, rr(S, 1.5)))),
            dot(5.8, 17.8, 0.9), dot(18.2, 17.8, 0.9), line(seg(16, 6, 21.5, 6))]


@T_("exhaust-resonator", "Straight exhaust pipe with an oval bulge in the middle perforated by small holes",
    ["resonator", "muffler section", "exhaust silencer", "exhaust pipe", "sound damper", "exhaust system", "tailpipe"])
def _(S):
    return [shell(ellipse(12, 12, 7, 5.5)), line(seg(2, 12, 5, 12)), line(seg(19, 12, 22, 12)),
            dot(9.5, 12, 0.9), dot(12, 12, 0.9), dot(14.5, 12, 0.9)]


@T_("clutch-pressure-plate", "Round clutch cover with a diaphragm spring of radiating fingers at its center",
    ["clutch cover", "pressure plate", "clutch assembly", "diaphragm spring", "manual transmission", "clutch", "flywheel cover"])
def _(S):
    fingers = [detail(seg(*polar(12, 12, 2.4, a), *polar(12, 12, 5.2, a))) for a in range(30, 390, 60)]
    bolts = [dot(*polar(12, 12, 7.0, a), 0.9) for a in range(0, 360, 60)]
    return [shell(circle(12, 12, 9))] + fingers + bolts


@T_("car-differential", "Pumpkin-shaped axle housing with an axle tube on each side and a driveshaft flange at the front",
    ["diff", "rear axle", "axle housing", "final drive", "drivetrain", "differential gear", "pumpkin"])
def _(S):
    return [shell(union(circle(12, 11, 5.6), rect(2.5, 9.6, 19, 2.8, rk(S, 1.4)), rect(10.5, 15, 3, 3.5, 0))),
            shell(rect(8.5, 18.5, 7, 3, rk(S, 1.5))), pip(S, 12, 11, 1.5)]


@T_("transfer-case", "Compact gearbox housing with one input shaft on the left and an output shaft at the top and bottom",
    ["transfer box", "4x4 gearbox", "four wheel drive", "4wd", "awd drivetrain", "drivetrain", "power split"])
def _(S):
    return [shell(rect(6.5, 7, 11, 10, rr(S, 2.5))), line(seg(2, 12, 6.5, 12)), line(seg(14, 2.5, 14, 7)),
            line(seg(14, 17, 14, 21.5)), dot(11, 12, 1.6), line(seg(2.5, 9.8, 2.5, 14.2))]


@T_("macpherson-strut", "Tall shock absorber wrapped in a slanted coil spring with a top mount plate",
    ["strut", "shock absorber", "coil spring strut", "suspension strut", "damper", "car suspension", "spring and shock"])
def _(S):
    return [shell(rect(5.5, 2.5, 13, 2.5, rr(S, 1))), line(seg(12, 5, 12, 8)), shell(rect(10, 8, 4, 13, rr(S, 1))),
            line(seg(6.5, 8.5, 17.5, 11.5)), line(seg(6.5, 13, 17.5, 16)), line(seg(6.5, 17.5, 17.5, 20.5))]


@T_("tie-rod", "Straight rod with a ball joint end on the left and a threaded adjuster sleeve on the right",
    ["track rod", "steering link", "tie rod end", "ball joint rod", "steering linkage", "suspension part", "toe adjust"])
def _(S):
    return [shell(circle(5, 12, 3.2)), dot(5, 12, 1.0), line(seg(8.2, 12, 11, 12)), shell(rect(11, 9.5, 7, 5, rr(S, 1.5))),
            detail(seg(13.5, 10.5, 13.5, 13.5)), detail(seg(15.5, 10.5, 15.5, 13.5)), line(seg(18, 12, 22, 12))]


@T_("sway-bar", "U-shaped anti-roll bar with two bushings on the straight part and an end link at each tip",
    ["anti roll bar", "stabilizer bar", "stabiliser bar", "roll bar", "suspension bar", "anti sway bar", "chassis part"])
def _(S):
    return [line(poly([(4, 7), (6.5, 17), (17.5, 17), (20, 7)], r=S.r)), shell(rect(8.5, 14.5, 3, 5, rr(S, 0.8))),
            shell(rect(12.5, 14.5, 3, 5, rr(S, 0.8))), line(seg(4, 7, 4, 3)), line(seg(20, 7, 20, 3))]


@T_("steering-rack", "Long horizontal tube with a rubber boot at each end and a pinion stub on top",
    ["rack and pinion", "steering gear", "rack pinion", "steering box", "steering system", "car steering", "boots"])
def _(S):
    return [shell(rect(8.5, 10.5, 7, 5, rr(S, 1.5))),
            shell(poly([(8.5, 9.5), (8.5, 16.5), (4.8, 14.8), (4.8, 11.2)], closed=True, r=S.r * 0.3)),
            shell(poly([(15.5, 9.5), (15.5, 16.5), (19.2, 14.8), (19.2, 11.2)], closed=True, r=S.r * 0.3)),
            line(seg(2, 13, 4.8, 13)), line(seg(19.2, 13, 22, 13)), line(seg(12, 5, 12, 10.5)), shell(rect(10, 2.5, 4, 2.5, rr(S, 0.8)))]


# =========================================================================== wheels and chassis

@T_("wheel-hub", "Round hub flange with five wheel studs around a center bearing cap",
    ["hub assembly", "wheel studs", "lug studs", "wheel flange", "axle hub", "wheel mount", "bearing hub"])
def _(S):
    return [shell(circle(12, 12, 9))] + [pip(S, *polar(12, 12, 6.0, -90 + 72 * k), 1.2) for k in range(5)] + [detail(circle(12, 12, 2.9))]


@T_("wheel-bearing", "Double ring bearing with a row of balls visible between the inner and outer races",
    ["ball bearing", "hub bearing", "bearing race", "roller bearing", "axle bearing", "bearings", "wheel hub bearing"])
def _(S):
    return [line(circle(12, 12, 9)), line(circle(12, 12, 4.4))] + [pip(S, *polar(12, 12, 6.7, 360 / 8 * k + 11), 1.1) for k in range(8)]


@T_("brake-master-cylinder", "Horizontal cylinder body with a small fluid reservoir on top and two brake line ports",
    ["master cylinder", "brake cylinder", "hydraulic brake", "brake pump", "brake system", "brake lines", "pedal cylinder"])
def _(S):
    return [shell(union(rect(5, 11, 15, 6.5, rr(S, 2.5)), rect(8.5, 5, 6, 6.5, rr(S, 1.5)))), line(seg(2, 14.2, 5, 14.2)),
            line(seg(14, 17.5, 14, 21.5)), line(seg(18, 17.5, 18, 21.5))]


@T_("brake-booster", "Large round flat canister seen from the side with a master cylinder poking out of its front face",
    ["brake servo", "vacuum booster", "power brake booster", "servo", "brake assist", "brake system", "vacuum servo"])
def _(S):
    return [shell(rect(2.5, 3.5, 11, 17, rr(S, 4))), detail(seg(8, 5, 8, 19)), shell(rect(13.5, 9, 8, 6, rr(S, 1.5)))]


@T_("ecu-module", "Flat metal box with cooling ribs and a wide multi-pin connector on one side",
    ["engine control unit", "ecm", "engine computer", "car computer", "control module", "ecu", "powertrain module"])
def _(S):
    return [shell(rect(2.5, 6.5, 14.5, 11, rr(S, 2))), detail(seg(6, 9.5, 6, 14.5)), detail(seg(9.5, 9.5, 9.5, 14.5)),
            detail(seg(13, 9.5, 13, 14.5)), shell(rect(17, 8.5, 4.5, 7, rr(S, 1))), dot(19.25, 10.6, 0.7), dot(19.25, 13.4, 0.7)]


@T_("headlight-bulb", "Automotive halogen bulb with a glass capsule, a round metal flange base and three flat pins",
    ["halogen bulb", "h4 bulb", "car lamp", "headlamp bulb", "xenon bulb", "car bulb", "lamp replacement"])
def _(S):
    return [shell(rect(8.5, 2.5, 7, 9, rr(S, 3.5))), detail(seg(12, 5.5, 12, 8.5)), shell(rect(6.5, 11.5, 11, 3.2, rr(S, 0.8))),
            shell(rect(8.5, 14.7, 7, 2.5, 0)), line(seg(9.5, 17.5, 9.5, 21.5)), line(seg(12, 17.5, 12, 21.5)), line(seg(14.5, 17.5, 14.5, 21.5))]


@T_("fuel-rail", "Long tube with a row of fuel injectors hanging below it",
    ["injector rail", "fuel injectors", "common rail", "fuel manifold", "injection system", "engine fuel", "fuel line"])
def _(S):
    inj = [shell(poly([(c - 1.6, 9), (c + 1.6, 9), (c + 1.1, 17), (c - 1.1, 17)], closed=True)) for c in (6, 12, 18)]
    return [shell(rect(2.5, 4.5, 19, 4.5, rr(S, 2.2)))] + inj + [line(seg(6, 17, 6, 20.5)), line(seg(12, 17, 12, 20.5)), line(seg(18, 17, 18, 20.5))]


@T_("tread-depth-gauge", "Pen-style gauge with a scale and a thin probe pin pushed into a tire tread groove",
    ["tire gauge", "tyre depth gauge", "tread gauge", "tire tread tester", "tire inspection", "tyre check", "tread depth"])
def _(S):
    return [shell(rect(6.5, 2.5, 6, 12.5, rr(S, 2))), detail(seg(8.6, 6, 10.4, 6)), detail(seg(8.6, 9.5, 10.4, 9.5)),
            line(seg(9.5, 15, 9.5, 19.5)), shell(rect(2, 16.5, 4.5, 5, rr(S, 1))), shell(rect(12.5, 16.5, 9.5, 5, rr(S, 1)))]


@T_("tire-valve-stem", "Short rubber valve stem with a threaded metal tip and a small screw-on cap",
    ["tyre valve", "valve cap", "schrader valve", "air valve", "inflation valve", "tire valve", "tire air"])
def _(S):
    return [shell(union(rect(9.5, 2.5, 5, 5.5, rr(S, 1.5)), rect(10.5, 8, 3, 5, 0), "M6.5 21L8.5 13L15.5 13L17.5 21Z")),
            detail(seg(10, 8.2, 14, 8.2)), detail(seg(8.5, 17.2, 15.5, 17.2))]


@T_("hubcap", "Round flat wheel cover with radiating spoke ridges and a small emblem circle at the center",
    ["wheel cover", "wheel trim", "center cap", "hub cap", "rim cover", "wheel hub cover", "car wheel"])
def _(S):
    return [shell(circle(12, 12, 9))] + [detail(seg(*polar(12, 12, 4.4, a), *polar(12, 12, 8.2, a))) for a in range(-90, 270, 72)] + [dot(12, 12, 1.8)]


@T_("wire-spoke-wheel", "Wheel with a narrow tire and many crossing thin spokes meeting a center hub with a knock-off nut",
    ["spoked wheel", "classic wheel", "wire wheel", "vintage wheel", "knock off wheel", "chrome wire wheel", "retro car wheel"])
def _(S):
    sp = [line(seg(*polar(12, 12, 2.4, a), *polar(12, 12, 8.0, a + 40))) for a in range(0, 360, 90)]
    sp += [line(seg(*polar(12, 12, 2.4, a), *polar(12, 12, 8.0, a - 40))) for a in range(45, 405, 90)]
    return [line(circle(12, 12, 9.4))] + sp + [dot(12, 12, 2.0)]


@T_("steel-wheel", "Plain pressed steel wheel with a ring of round vent holes around a flat center",
    ["steelie", "steel rim", "pressed steel rim", "plain wheel", "winter wheel", "car rim", "wheel with holes"])
def _(S):
    return [line(circle(12, 12, 9.4)), shell(circle(12, 12, 6.2))] + [pip(S, *polar(12, 12, 3.6, -90 + 72 * k), 1.1) for k in range(5)] + [pip(S, 12, 12, 0.9)]


@T_("locking-wheel-nut", "Wheel nut with a wavy key pattern on its face next to a matching socket key",
    ["wheel lock", "anti theft wheel nut", "security wheel nut", "lock nut key", "lug nut lock", "wheel security", "locking bolt"])
def _(S):
    nut = poly(regular(7.2, 12, 5.6, 6, 0), closed=True, r=S.r * 0.4)
    pat_n = poly(gear_pts(7.2, 12, 2.5, 1.5, 5, 20, 30), closed=True)
    pat_k = poly(gear_pts(18, 12, 2.5, 1.5, 5, 20, 30), closed=True)
    return [shell(nut), knock(pat_n), shell(rect(14, 8, 8, 8, rr(S, 2))), knock(pat_k)]


@T_("tire-iron", "L-shaped lug wrench with a socket on the short end and a flat pry tip on the long end",
    ["lug wrench", "wheel wrench", "tire wrench", "tyre iron", "wheel brace", "spare tire tool", "roadside tool"])
def _(S):
    return [shell(circle(5.5, 5.5, 3.2)), knock(circle(5.5, 5.5, 1.1)), line(poly([(5.5, 8.7), (5.5, 18.5), (17, 18.5)], r=S.r)),
            shell(poly([(16.5, 16), (21.5, 17), (21.5, 20.5), (16.5, 21)], closed=True))]


@T_("tire-lever", "Short flat curved lever with a hooked spoon tip",
    ["tyre lever", "tire spoon", "bead breaker lever", "tire changer tool", "rim lever", "pry bar", "tire repair"])
def _(S):
    body = path_to_d(ST("M4.5 20L13.5 11Q16.5 8 20 6.5Q21 8.5 18.5 11", 3.4, "round", "round", 4))
    return [shell(body)]
