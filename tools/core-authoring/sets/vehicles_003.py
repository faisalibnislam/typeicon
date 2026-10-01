"""TypeIcon Core: vehicles (batch 003, dashboard symbols, car parts, accessories and special vehicles).

Same visual language as sets/vehicles_001.py: side-view vehicles face right, wheels are rings (solid discs in
Filled) on a common ground line, and the body outline is left open where it meets a wheel.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    rect, regular, seg, shell, solid,
)
from geometry import rotation, transform_path

CAT = "vehicles"
FILL = Style("filled", "butt", "miter", R=2.0, r=0.0)


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    return b if S.name == "rounded" else a


def isF(S):
    return S.name == "filled"


def rpt(p, deg, c=(12.0, 12.0)):
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a)


def rpts(pts, deg, c=(12.0, 12.0)):
    return [rpt(p, deg, c) for p in pts]


def rotd(d, deg, c=(12.0, 12.0)):
    return path_to_d(transform_path(P(d), rotation(deg, c[0], c[1])))


def rotparts(parts, deg, c=(12.0, 12.0)):
    """Rotate finished parts about c, keeping wheel and knock-out markers."""
    out = []
    for p in parts:
        q = Part(p.kind, rotd(p.d, deg, c), dict(p.attrs))
        w = getattr(p, "wheel", None)
        if w:
            x, y = rpt((w[0], w[1]), deg, c)
            q.wheel = (x, y, w[2])
        if getattr(p, "knock", False):
            q.knock = True
        out.append(q)
    return out


def T(name, description, tags, aliases=()):
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases,
                    filled=lambda: filled_region(fn(FILL)))(fn)
    return deco


def wheel(x, y=18.0, r=2.0):
    p = shell(circle(x, y, r))
    p.wheel = (x, y, r)
    return p


def hub(x, y, r=1.0):
    p = dot(x, y, r)
    p.knock = True
    return p


def body(S, pts, ws, yb=None, r=None):
    yb = ws[0][1] if yb is None else yb
    rr = S.r if r is None else r
    if isF(S):
        return [shell(poly(pts, closed=True))]
    gaps = []
    for x, y, wr in ws:
        dy = yb - y
        if abs(dy) < wr:
            h = math.sqrt(wr * wr - dy * dy)
            gaps.append((x - h, x + h))
    gaps.sort()
    if not gaps:
        return [shell(poly(pts, closed=True, r=rr))]
    out = [shell(poly([(gaps[0][0], yb)] + list(pts) + [(gaps[-1][1], yb)], r=rr))]
    for a, b in zip(gaps, gaps[1:]):
        if b[0] - a[1] > 0.5:
            out.append(line(seg(a[1], yb, b[0], yb)))
    return out


def auto(S, pts, ws, *extra, yb=None, r=None):
    return body(S, pts, ws, yb, r) + [wheel(*w) for w in ws] + list(extra)


def veh_filled(fn):
    def f():
        parts = fn(FILL)
        wh = [p.wheel for p in parts if getattr(p, "wheel", None)]
        holes = [P(p.d) for p in parts if getattr(p, "knock", False)]
        rest = [p for p in parts if not getattr(p, "wheel", None) and not getattr(p, "knock", False)]
        out = filled_region(rest) if rest else None
        if wh:
            cut = U(*[P(circle(x, y, r + 2)) for x, y, r in wh])
            discs = U(*[P(circle(x, y, r + 1)) for x, y, r in wh])
            out = U(D(out, cut), discs) if out is not None else discs
        if holes:
            out = D(out, *holes)
        return out
    return f


def veh(name, description, tags, aliases=()):
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=veh_filled(fn))(fn)
    return deco


W2 = [(6.5, 18, 2), (17.5, 18, 2)]


def wave(x, y0, y1, a=1.2, role=line):
    """Vertical S-wave from (x, y0) up to y1 (one stroke, heat or smoke)."""
    s = (y0 - y1) / 4
    return role(f"M{fmt(x)} {fmt(y0)}Q{fmt(x + a)} {fmt(y0 - s)} {fmt(x)} {fmt(y0 - 2 * s)}"
                f"T{fmt(x)} {fmt(y1)}")


def ahead(tip, d, size=2.5, S=None, role=line):
    """Open arrowhead (chevron) with its tip at `tip`, pointing along angle d degrees."""
    a1, a2 = math.radians(d + 150), math.radians(d - 150)
    p1 = (tip[0] + size * math.cos(a1), tip[1] + size * math.sin(a1))
    p2 = (tip[0] + size * math.cos(a2), tip[1] + size * math.sin(a2))
    return role(poly([p1, tip, p2], r=0 if S is None else S.r * 0.5))


def tri(tip, d, size=3.0, half=1.8):
    """Solid triangle pointing along angle d degrees."""
    a = math.radians(d)
    bx, by = tip[0] - size * math.cos(a), tip[1] - size * math.sin(a)
    nx, ny = -math.sin(a) * half, math.cos(a) * half
    return solid(poly([tip, (bx + nx, by + ny), (bx - nx, by - ny)], closed=True))


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


# =========================================================================== dashboard symbols

@T("rear-defrost", "Rear window outline with three wavy heat lines rising through it",
   ["rear window", "heated window", "demister", "dashboard light", "car", "heat"], aliases=["rear-demister"])
def _(S):
    return [shell(poly([(3, 18), (5, 5), (19, 5), (21, 18)], closed=True, r=S.r)),
            wave(8.5, 15, 8, 1, detail), wave(12, 15, 8, 1, detail), wave(15.5, 15, 8, 1, detail)]


@T("front-defrost", "Curved windshield outline with three wavy heat lines rising through it",
   ["windshield", "front window", "demister", "dashboard light", "car", "heat"], aliases=["windshield-defrost"])
def _(S):
    d = "M3 19Q12 15 21 19L19 5Q12 3 5 5Z" if S.name == "rounded" else "M2.5 19Q12 14.5 21.5 19L19 5Q12 3 5 5Z"
    return [shell(d), wave(8.5, 14.5, 8, 1, detail), wave(12, 14.5, 8, 1, detail), wave(15.5, 14.5, 8, 1, detail)]


@T("door-ajar-light", "Car seen from above with one door swung open",
   ["open door", "door warning", "dashboard light", "car", "top view", "door open"], aliases=["door-open-light"])
def _(S):
    k = L(S, 2.5, 4)
    return [shell(rect(8, 2.5, 10, 19, k)), detail("M9.5 8.5Q13 7 16.5 8.5"), detail("M10 17Q13 18 16 17"),
            line(seg(8, 10, 3, 7)), line(seg(8, 15, 3, 12))]


@T("power-steering-light", "Steering wheel with an exclamation mark beside it",
   ["steering warning", "power steering", "eps", "dashboard light", "car", "fault"])
def _(S):
    return [shell(circle(9.5, 12, 8)), detail(seg(2, 11, 17, 11)),
            detail(seg(9.5, 11, 9.5, 20)), dot(9.5, 12, 2.25),
            line(seg(21.5, 5, 21.5, 13)), dot(21.5, 18, 1.2)]


@T("lane-departure", "Car seen from behind drifting over a dashed lane line",
   ["lane assist", "lane keeping", "swerve", "drift", "driver assistance", "road marking"], aliases=["lane-departure-warning"])
def _(S):
    c = (12, 12)
    pts = rpts([(6.5, 18.5), (6.5, 13), (8, 8), (16, 8), (17.5, 13), (17.5, 18.5)], 14, c)
    out = [shell(poly(pts, closed=True, r=S.r * 0.5))]
    out += [detail(poly(rpts([(7.5, 13), (16.5, 13)], 14, c), r=0))]
    out += [line(seg(21, 3, 21, 8)), line(seg(21, 11.5, 21, 16.5)), line(seg(21, 20, 21, 22))]
    out += [line(seg(3, 3, 3, 7)), line(seg(3, 10.5, 3, 14.5)), line(seg(3, 18, 3, 22))]
    return out


@T("cruise-control", "Speedometer dial with a marker above the arc at the set speed",
   ["set speed", "speed limiter", "speedometer", "dashboard light", "adaptive cruise", "driving"])
def _(S):
    cx, cy = 11, 19
    a = math.radians(-50)
    tip = (cx + 9.2 * math.cos(a), cy + 9.2 * math.sin(a))
    return [line(arc(cx, cy, 8.5, 180, 360)), line(seg(cx, cy, cx - 4.2, cy - 4.2)),
            dot(cx, cy, 1.5), tri(tip, 130, 3.2, 1.9)]


@T("seat-heater", "Side view of a car seat with three wavy heat lines rising from the cushion",
   ["heated seat", "car seat", "seat warmer", "comfort", "winter", "dashboard light"], aliases=["heated-seat"])
def _(S):
    return [shell(poly([(4, 3.5), (9, 3.5), (9, 14), (21, 14), (21, 20.5), (4, 20.5)], closed=True, r=S.r)),
            wave(13, 11, 4.5, 0.9), wave(16.75, 11, 4.5, 0.9), wave(20.5, 11, 4.5, 0.9)]


@T("auto-start-stop", "Letter A inside a circular arrow that almost closes on itself",
   ["stop start", "idle stop", "eco", "engine", "dashboard light", "start stop system"])
def _(S):
    end = (12 + 9 * math.cos(math.radians(235)), 12 + 9 * math.sin(math.radians(235)))
    return [line(arc(12, 12, 9, -45, 235)), ahead(end, -35, 3, S),
            line(poly([(8.5, 16.5), (12, 7.5), (15.5, 16.5)], r=S.r * 0.4)), line(seg(9.8, 13.5, 14.2, 13.5))]


@veh("hill-descent-control", "Car tilted down a slope with a ground line running under it",
     ["downhill", "slope", "descent", "off road", "dashboard light", "hdc", "steep hill"])
def _(S):
    pts = [(2.5, 14), (2.5, 9), (4.5, 8), (7, 4), (13.5, 4), (16, 8), (19, 9), (19, 14)]
    ws = [(6, 14, 2), (15.5, 14, 2)]
    c = (10.75, 14)
    g0, g1 = rpt((2, 18), 16, c), rpt((19.5, 18), 16, c)
    return rotparts(auto(S, pts, ws), 16, c) + [line(seg(*g0, *g1))]


@T("all-wheel-drive", "Chassis seen from above with two axles joined by a centre shaft and four wheels",
   ["awd", "4wd", "four wheel drive", "drivetrain", "transmission", "4x4", "axle"], aliases=["awd"])
def _(S):
    w = L(S, 0.5, 1)
    return [shell(rect(2, 3, 3.5, 6, w)), shell(rect(18.5, 3, 3.5, 6, w)),
            shell(rect(2, 15, 3.5, 6, w)), shell(rect(18.5, 15, 3.5, 6, w)),
            line(seg(5.5, 6, 18.5, 6)), line(seg(5.5, 18, 18.5, 18)),
            line(seg(12, 6, 12, 9.5)), line(seg(12, 14.5, 12, 18)), shell(circle(12, 12, 2.5))]


@T("blind-spot-monitor", "Car seen from above with radar arcs sweeping from its rear corner toward a second car",
   ["blind spot", "side radar", "lane change", "driver assistance", "adas", "mirror warning"],
   aliases=["blind-spot-warning"])
def _(S):
    k = L(S, 2, 3)
    return [shell(rect(2, 3.5, 8, 15, k)), detail("M3.5 9Q6 8 8.5 9"),
            line(arc(10.5, 11, 3.8, -45, 45)), line(arc(10.5, 11, 6.8, -45, 45)),
            shell(rect(19, 6.5, 3.5, 9, L(S, 1.2, 1.7)))]


@veh("air-recirculation", "Car in side view with a looping arrow circling inside the cabin",
     ["recirculate", "cabin air", "air conditioning", "ventilation", "climate control", "dashboard light"],
     aliases=["recirculation"])
def _(S):
    pts = [(2.5, 19), (2.5, 14), (4.5, 13), (7, 4.5), (17, 4.5), (19.5, 13), (21.5, 14), (21.5, 19)]
    ws = [(6.5, 19, 2), (17.5, 19, 2)]
    end = (12 + 3.3 * math.cos(math.radians(300)), 9.5 + 3.3 * math.sin(math.radians(300)))
    return auto(S, pts, ws, detail(arc(12, 9.5, 3.3, 0, 300)), ahead(end, 30, 2.3, S, detail), yb=19)


@veh("carpool", "Car in side view with three passenger heads in its windows",
     ["car share", "ride share", "passengers", "commute", "shared ride", "hov"], aliases=["car-share"])
def _(S):
    pts = [(2.5, 18), (2.5, 12.5), (4.5, 11.5), (6.5, 5.5), (17.5, 5.5), (19.5, 11.5), (21.5, 12.5), (21.5, 18)]
    return auto(S, pts, W2, detail(seg(3, 12, 20.5, 12)), dot(8.8, 8.4, 1.2), dot(12, 8.4, 1.2), dot(15.2, 8.4, 1.2))


def star(cx, cy, ro, ri, n=8, start=-90.0):
    pts = []
    for i in range(2 * n):
        r = ro if i % 2 == 0 else ri
        a = math.radians(start + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


@T("car-crash", "Two cars meeting nose to nose with a starburst above the impact",
   ["collision", "accident", "crash", "wreck", "fender bender", "insurance claim"], aliases=["car-accident"])
def _(S):
    r = S.r * 0.5
    left = [(1.5, 17), (1.5, 12.5), (3.5, 12), (5, 8.5), (8, 8.5), (9.5, 12.5), (10, 17)]
    right = [(24 - x, y) for x, y in left]
    return [shell(poly(left, closed=True, r=r)), shell(poly(right, closed=True, r=r)),
            dot(4.2, 17.2, 1.5), dot(8, 17.2, 1.5), dot(16, 17.2, 1.5), dot(19.8, 17.2, 1.5),
            solid(poly(star(12, 7, 4.2, 1.9), closed=True))]


@veh("car-breakdown", "Car with its hood raised and smoke rising from the engine",
     ["broken down", "engine trouble", "overheating", "roadside", "stalled", "car trouble"], aliases=["broken-down-car"])
def _(S):
    pts = [(2.5, 18), (2.5, 12.5), (5, 11.5), (7.5, 7), (13.5, 7), (14.5, 11.5), (21.5, 12.5), (21.5, 18)]
    return auto(S, pts, W2, line(seg(15, 10.5, 21, 7.5)), wave(16.5, 5.5, 1.8, 1), wave(20, 5.5, 1.8, 1))


@T("car-insurance", "Small car drawn inside a large shield",
   ["auto insurance", "vehicle cover", "protection", "claim", "policy", "car protection"], aliases=["auto-insurance"])
def _(S):
    sh = "M12 2.5L20.5 5.5V12C20.5 17 16.5 20 12 21.5C7.5 20 3.5 17 3.5 12V5.5Z"
    if S.name == "rounded":
        sh = "M12 2.5L20.5 5.5V12C20.5 17 16.5 20 12 21.5C7.5 20 3.5 17 3.5 12V5.5Z"
    car = [(6.5, 14), (6.5, 11.5), (8, 10.8), (9.5, 8), (14.5, 8), (16, 10.8), (17.5, 11.5), (17.5, 14)]
    return [shell(sh), detail(poly(car, closed=True, r=S.r * 0.3)), dot(9.3, 14.3, 1.3), dot(14.7, 14.3, 1.3)]


@veh("road-trip", "Car with a suitcase strapped to the roof",
     ["travel", "holiday", "vacation", "luggage", "journey", "car trip", "roof rack"], aliases=["roof-luggage"])
def _(S):
    pts = [(2.5, 19), (2.5, 15), (5, 14), (7.5, 10.5), (16.5, 10.5), (19, 14), (21.5, 15), (21.5, 19)]
    ws = [(6.5, 19, 2), (17.5, 19, 2)]
    return auto(S, pts, ws, shell(rect(6.5, 4.5, 11, 4.5, L(S, 0.5, 1.2))), line(poly([(10.5, 4.5), (10.5, 2.5), (13.5, 2.5), (13.5, 4.5)], r=S.r * 0.3)), yb=19)


@T("learner-driver-plate", "Square plate showing a bold capital L",
   ["learner plate", "l plate", "new driver", "student driver", "driving lesson", "driving school"], aliases=["l-plate"])
def _(S):
    return [shell(rect(3, 3, 18, 18, L(S, 1.5, 4))), Part("dot", "M8.5 6.5H11.8V14.2H16V17.5H8.5Z" if S.name != "rounded"
                                                             else "M8.5 6.5H11.8V14.2H16V17.5H8.5Z")]


@veh("oil-change", "Car with an oil drop and a small funnel above its hood",
     ["engine oil", "lube", "servicing", "maintenance", "oil service", "garage"], aliases=["oil-service"])
def _(S):
    pts = [(2.5, 19.5), (2.5, 15.5), (5, 14.5), (7, 11.5), (14, 11.5), (16.5, 14.5), (21.5, 15.5), (21.5, 19.5)]
    ws = [(6.5, 19.5, 1.9), (17.5, 19.5, 1.9)]
    drop = "M9.5 2.5C9.5 2.5 7 5.6 7 7.2A2.5 2.5 0 0 0 12 7.2C12 5.6 9.5 2.5 9.5 2.5Z"
    return auto(S, pts, ws, shell(drop), shell(poly([(15.5, 3), (21.5, 3), (19.5, 6.5), (19.5, 9.5), (17.5, 9.5), (17.5, 6.5)],
                                                    closed=True, r=S.r * 0.4)), yb=19.5)


@veh("truck-camper", "Pickup truck carrying a boxy camper unit that overhangs the cab roof",
     ["pickup camper", "slide in camper", "overlanding", "rv", "camping truck", "motorhome"], aliases=["pickup-camper"])
def _(S):
    pts = [(2.5, 18), (2.5, 4.5), (15.5, 4.5), (15.5, 9.5), (18, 9.5), (21.5, 13), (21.5, 18)]
    return auto(S, pts, W2, detail(rect(5.5, 7.5, 5, 3.5, 0)), detail(seg(15.5, 9.5, 15.5, 14)),
                detail(poly([(17.8, 9.5), (17.8, 13)], r=0)))


@veh("skip-loader-truck", "Truck with lifting arms carrying an open skip bin on its back",
     ["skip truck", "dumpster truck", "waste container", "rubbish skip", "builders skip", "roll off truck"],
     aliases=["skip-truck"])
def _(S):
    pts = [(2.5, 18), (2.5, 15.5), (14, 15.5), (14, 9), (17.5, 9), (21.5, 13), (21.5, 18)]
    skip = poly([(2.5, 4), (13, 4), (11.5, 12.5), (4, 12.5)], closed=True, r=S.r * 0.4)
    return auto(S, pts, W2, shell(skip), detail(poly([(16.2, 9.5), (16.2, 13), (21, 13)], r=S.r * 0.4)))


@veh("milk-float", "Small open electric delivery van with crates of milk bottles on its flat back",
     ["milk van", "milkman", "dairy delivery", "electric van", "bottles", "delivery"], aliases=["milk-van"])
def _(S):
    pts = [(2.5, 18), (2.5, 13.5), (11.5, 13.5), (11.5, 6.5), (18, 6.5), (21.5, 12), (21.5, 18)]
    return auto(S, pts, W2, sq(4, 8, 2.2, 4.5, L(S, 0, 1)), sq(7.3, 8, 2.2, 4.5, L(S, 0, 1)),
                detail(poly([(13.5, 10), (13.5, 13.5), (19.5, 13.5)], r=0)))


@veh("ice-resurfacer", "Rink machine with an operator cab on top and a squeegee trailing behind",
     ["ice machine", "ice rink", "rink maintenance", "skating rink", "hockey", "ice cleaning"], aliases=["ice-rink-machine"])
def _(S):
    pts = [(7, 18), (7, 10.5), (21.5, 10.5), (21.5, 18)]
    ws = [(11, 18, 2), (18, 18, 2)]
    cab = poly([(12, 10.5), (12, 4), (18.5, 4), (18.5, 10.5)], r=S.r * 0.5)
    return auto(S, pts, ws, line(cab), dot(15.25, 7.2, 1.3),
                line(poly([(7, 14.5), (3.5, 14.5), (3.5, 19.5)], r=S.r * 0.4)), line(seg(2, 19.5, 5.5, 19.5)))


@T("surrey-bike", "Four-wheeled pedal carriage with two riders under a canopy roof",
   ["quadricycle", "pedal carriage", "family bike", "surrey", "tourist bike", "four wheel bike"], aliases=["quadricycle"])
def _(S):
    return [line("M3 7Q12 1.5 21 7"), line(seg(5, 6, 5, 14)), line(seg(19, 6, 19, 14)),
            shell(circle(7, 18, 3)), shell(circle(17, 18, 3)), line(seg(4.5, 14, 19.5, 14)),
            dot(10, 9.5, 1.5), dot(14, 9.5, 1.5)]


@T("race-start-lights", "Gantry with a row of five round lights, all lit, above a track",
   ["f1 start", "starting lights", "grand prix", "motorsport", "lights out", "traffic light race"],
   aliases=["starting-lights"])
def _(S):
    return [shell(rect(2, 6.5, 20, 8, L(S, 1, 3))), line(seg(6.5, 2.5, 6.5, 6.5)), line(seg(17.5, 2.5, 17.5, 6.5)),
            dot(5.5, 10.5, 1.3), dot(8.75, 10.5, 1.3), dot(12, 10.5, 1.3), dot(15.25, 10.5, 1.3), dot(18.5, 10.5, 1.3),
            line(seg(2, 20, 22, 20))]


@T("race-track", "Closed looping circuit seen from above with a start line across one straight",
   ["circuit", "racetrack", "motorsport track", "grand prix circuit", "speedway", "lap"], aliases=["circuit-track"])
def _(S):
    outer = [(3, 16), (3, 8), (6.5, 4), (11, 4), (13, 8.5), (17.5, 8.5), (21, 11.5), (21, 16.5), (17.5, 20), (6.5, 20)]
    inner = [(7.5, 15.5), (7.5, 8.5), (8.5, 8.5), (10.5, 12.5), (17, 12.5), (17, 15.5)]
    return [line(poly(outer, closed=True, r=L(S, 2, 4))), line(poly(inner, closed=True, r=L(S, 1, 2))),
            line(seg(12, 15.5, 12, 20))]


@T("fuel-gauge", "Semicircle fuel dial with a needle near empty and a drop in the middle",
   ["fuel level", "petrol gauge", "gas gauge", "tank level", "empty", "dashboard"], aliases=["gas-gauge"])
def _(S):
    return [line(arc(12, 20, 10, 180, 360)), line(seg(12, 20, 5.5, 17.5)), dot(12, 20, 1.5),
            shell("M12 11.5C12 11.5 9.8 14 9.8 15.2A2.2 2.2 0 0 0 14.2 15.2C14.2 14 12 11.5 12 11.5Z"),
            line(seg(20.5, 20, 22, 20)), line(seg(2, 20, 3.5, 20))]


@T("car-radio", "Car stereo head unit with a small display, a round knob and a row of preset buttons",
   ["head unit", "car stereo", "audio", "dash radio", "infotainment", "am fm"], aliases=["car-stereo"])
def _(S):
    return [shell(rect(2, 5.5, 20, 13, L(S, 1.5, 3.5))), detail(rect(4.5, 8, 8, 3.5, 0)), detail(circle(17.5, 10, 2.3)),
            dot(6, 15, 1), dot(9.5, 15, 1), dot(13, 15, 1), dot(17.5, 15, 1)]


@T("car-sun-visor", "Flip-down sun visor panel hinged along the top with a small mirror on its face",
   ["visor", "vanity mirror", "sun shield", "windshield visor", "car interior", "sun glare"])
def _(S):
    return [shell(rect(3, 6, 18, 13.5, L(S, 1.5, 3.5))), line(seg(2.5, 3, 21.5, 3)), detail(rect(7, 9.5, 10, 6, 0))]


@T("windshield-sunshade", "Windshield outline filled by an accordion-folded shade with vertical pleats",
   ["sun shade", "windscreen cover", "car cooler", "heat shield", "parking shade", "sun protector"],
   aliases=["car-sunshade"])
def _(S):
    return [shell(poly([(2.5, 19.5), (5, 4.5), (19, 4.5), (21.5, 19.5)], closed=True, r=S.r)),
            detail(seg(8.5, 4.5, 8.5, 19.5)), detail(seg(12, 4.5, 12, 19.5)), detail(seg(15.5, 4.5, 15.5, 19.5))]


@T("turn-signal", "Two outlined arrowheads pointing away from each other like indicator lamps",
   ["indicator", "blinker", "hazard", "direction indicator", "flasher", "left right"], aliases=["indicator-lights"])
def _(S):
    r = S.r
    return [shell(poly([(2.5, 12), (10, 5.5), (10, 18.5)], closed=True, r=r)),
            shell(poly([(21.5, 12), (14, 5.5), (14, 18.5)], closed=True, r=r))]


@T("ignition-key", "Car key inserted into a round ignition barrel",
   ["car key", "ignition switch", "start car", "key lock", "keyhole", "turn key"], aliases=["ignition-switch-key"])
def _(S):
    return [shell(circle(9, 15, 6)), dot(9, 15, 1.3), line(seg(14.8, 9.2, 10, 14)), shell(circle(17.5, 6.5, 3.2)),
            dot(17.5, 6.5, 1)]


@T("engine-start-button", "Round push button with a power symbol in the centre",
   ["push start", "start stop button", "keyless start", "power button", "ignition button", "engine start"],
   aliases=["push-start-button"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(arc(12, 12.5, 4.2, -60, 240)), detail(seg(12, 6.5, 12, 12))]


@T("cv-joint", "Short drive shaft with a ribbed rubber boot at one end and a stub shaft",
   ["cv boot", "drive shaft", "axle", "constant velocity joint", "driveshaft", "mechanic"], aliases=["cv-boot"])
def _(S):
    return [line(seg(2, 12, 6.5, 12)), shell(poly([(6.5, 9.5), (16, 6), (16, 18), (6.5, 14.5)], closed=True, r=S.r * 0.6)),
            detail(seg(9.8, 8.5, 9.8, 15.5)), detail(seg(13, 7.3, 13, 16.7)), line(seg(16, 12, 22, 12))]


@T("obd-scanner", "Handheld diagnostic reader with a screen and buttons, its cable ending in a trapezoid connector",
   ["obd2", "car diagnostics", "code reader", "check engine", "scan tool", "fault codes"], aliases=["obd-reader"])
def _(S):
    return [shell(rect(2.5, 2.5, 10, 13, L(S, 1.5, 3))), detail(rect(5, 5, 5, 3.5, 0)), dot(5.5, 12, 1), dot(9.5, 12, 1),
            line(poly([(7.5, 15.5), (7.5, 19.5), (15.5, 19.5)], r=S.r)),
            shell(poly([(15, 16), (21.5, 16), (20, 21.5), (16.5, 21.5)], closed=True, r=S.r * 0.4))]


@T("bull-bar", "Head-on front of an off-road vehicle with a tubular guard frame across the grille",
   ["roo bar", "nudge bar", "grille guard", "4x4 accessory", "front guard", "off road"], aliases=["grille-guard"])
def _(S):
    return [shell(rect(3, 2.5, 18, 12.5, L(S, 1.5, 3))), detail(seg(3, 8, 21, 8)), dot(6.5, 11.7, 1.2), dot(17.5, 11.7, 1.2),
            line(poly([(4.5, 21.5), (4.5, 18), (19.5, 18), (19.5, 21.5)], r=S.r)), line(seg(12, 15, 12, 18))]


@T("winter-tire", "Tire seen from the side with a snowflake mark in its hub",
   ["snow tyre", "winter tyre", "snow tire", "cold weather", "tread", "icy roads"], aliases=["snow-tire"])
def _(S):
    arms = [seg(12 + 3.4 * math.cos(math.radians(a)), 12 + 3.4 * math.sin(math.radians(a)),
                12 - 3.4 * math.cos(math.radians(a)), 12 - 3.4 * math.sin(math.radians(a))) for a in (90, 30, 150)]
    return [shell(circle(12, 12, 9.5)), detail(circle(12, 12, 5.8))] + [detail(a) for a in arms]


@T("cycling-computer", "Small bike computer showing a speed readout, clipped to a handlebar",
   ["bike computer", "speedometer bike", "cyclocomputer", "gps bike", "cadence", "handlebar"], aliases=["bike-computer"])
def _(S):
    return [shell(rect(6, 3.5, 12, 11, L(S, 1.5, 3))), detail(rect(8.5, 6, 7, 3, 0)), dot(9, 12, 0.9), dot(15, 12, 0.9),
            line(seg(12, 14.5, 12, 18)), line(seg(2.5, 19, 21.5, 19))]


@T("bike-pannier", "Pannier bag with a rolled top hanging from a rack beside a bicycle wheel",
   ["bicycle bag", "rack bag", "touring bag", "bike luggage", "cycle touring", "saddle bag"], aliases=["bicycle-pannier"])
def _(S):
    return [shell(circle(6.5, 16.5, 4.5)),
            line(seg(10, 6, 22, 6)), line(seg(14, 6, 14, 8.5)), line(seg(19.5, 6, 19.5, 8.5)),
            shell(rect(11.5, 8.5, 10, 12.5, L(S, 1.5, 3))), detail(seg(11.5, 12.5, 21.5, 12.5)), dot(16.5, 16.5, 1)]


@T("bicycle-frame", "Diamond bicycle frame with saddle, handlebar and fork but no wheels",
   ["bike frame", "bicycle chassis", "frameset", "cycling", "bike parts", "diamond frame"], aliases=["bike-frame"])
def _(S):
    r = S.r * 0.4
    return [line(poly([(8.5, 16.5), (7.5, 7), (16, 8), (8.5, 16.5)], r=r)), line(poly([(8.5, 16.5), (2.5, 16.5), (7.5, 7)], r=r)),
            line(seg(16, 8, 19.5, 17)), line(seg(16, 8, 15.5, 4.5)), line(seg(14, 4.5, 19, 4.5)),
            line(seg(7.5, 7, 7, 4.5)), line(seg(4.5, 4.5, 9.5, 4.5)), shell(circle(8.5, 16.5, 1.6))]


@T("ride-hailing", "Smartphone showing a map pin above a small car",
   ["taxi app", "ride share app", "cab booking", "book a ride", "pickup location", "call a car"], aliases=["taxi-app"])
def _(S):
    pin = "M12 14C10 12 8.2 10.8 8.2 8.7A3.8 3.8 0 0 1 15.8 8.7C15.8 10.8 14 12 12 14Z"
    car = "M8.5 19V17.5L9.6 15.7H14.4L15.5 17.5V19Z"
    return [shell(rect(5.5, 2, 13, 20, L(S, 2, 4))), detail(pin), Part("dot", car)]


@T("hitchhiker", "Person at the roadside with an arm stretched out and thumb up, wearing a backpack",
   ["thumbs up ride", "hitchhiking", "travel", "roadside", "lift", "backpacker"], aliases=["hitchhiking"])
def _(S):
    return [shell(circle(10.5, 4.8, 2.3)), line(seg(10.5, 8.5, 10.5, 15)), line(seg(10.5, 15, 8, 21)),
            line(seg(10.5, 15, 13, 21)), line(poly([(10.5, 10), (17, 10), (17, 6)], r=S.r * 0.5)),
            shell(rect(4.5, 9, 4, 6.5, L(S, 0.5, 1.5)))]


@T("car-driver", "Person seen from the front behind a steering wheel",
   ["driving", "driver", "behind the wheel", "motorist", "chauffeur", "car seat"], aliases=["person-at-wheel"])
def _(S):
    return [shell(circle(12, 5, 2.8)), line("M5.5 13.5Q5.5 9 12 9Q18.5 9 18.5 13.5"),
            shell(circle(12, 16.5, 4.5)), detail(seg(7.5, 16.5, 16.5, 16.5)), detail(seg(12, 16.5, 12, 21)), dot(12, 16.5, 1.3)]


@veh("news-van", "Van with a satellite dish on a mast raised from its roof",
     ["tv van", "broadcast truck", "outside broadcast", "reporter", "live news", "satellite van"])
def _(S):
    pts = [(2.5, 18), (2.5, 9.5), (15, 9.5), (18.5, 13), (21.5, 13.5), (21.5, 18)]
    return auto(S, pts, W2, detail(poly([(15, 9.5), (15, 13), (18.5, 13)], r=0)),
                line(seg(8, 7.5, 8, 9.5)), shell("M4.5 3.5H11.5A3.5 3.5 0 0 1 4.5 3.5Z"), line(arc(12.5, 6.5, 3.2, -75, -15)))


@veh("tiny-house-trailer", "Small house with a pitched roof, door and window sitting on a two-wheeled trailer",
     ["tiny home", "mobile home", "house on wheels", "micro house", "trailer home", "park model"], aliases=["tiny-home"])
def _(S):
    pts = [(3.5, 17), (3.5, 9), (11.5, 3), (19.5, 9), (19.5, 17)]
    return auto(S, pts, [(11.5, 17.5, 2.5)], detail(rect(5.5, 10.5, 4, 3.5, 0)),
                detail(poly([(15, 17), (15, 11.5), (17, 11.5), (17, 17)], r=0)), line(seg(19.5, 17, 22, 17)), yb=17, r=S.r * 0.5)


@T("brake-pad-wear-light", "Circle flanked by dashed curved brackets like worn brake pads",
   ["brake wear", "brake warning", "dashboard light", "pads", "brake service", "brake fault"])
def _(S):
    c = (12, 12)
    return [shell(circle(12, 12, 4)), line(arc(12, 12, 8.5, 140, 170)), line(arc(12, 12, 8.5, 190, 220)),
            line(arc(12, 12, 8.5, -40, -10)), line(arc(12, 12, 8.5, 10, 40))]


@veh("trunk-open-light", "Car in side view with its rear trunk lid lifted open",
     ["boot open", "trunk ajar", "tailgate open", "dashboard light", "luggage compartment", "trunk warning"],
     aliases=["boot-open-light"])
def _(S):
    pts = [(2.5, 18), (2.5, 13), (7, 12.5), (9.5, 8), (15, 8), (18, 12.5), (21.5, 13.5), (21.5, 18)]
    return auto(S, pts, W2, line(seg(6.5, 11.5, 2.5, 5.5)), detail(seg(9.5, 8, 9.5, 12.5)))


@T("water-in-fuel-light", "Fuel pump with a water droplet beside it",
   ["diesel water", "fuel contamination", "fuel filter warning", "dashboard light", "water separator", "fuel fault"])
def _(S):
    drop = "M19.5 12.5C19.5 12.5 17 15.8 17 17.4A2.5 2.5 0 0 0 22 17.4C22 15.8 19.5 12.5 19.5 12.5Z"
    return [shell(rect(2.5, 3, 9.5, 18, L(S, 1.5, 3))), detail(rect(4.5, 5.5, 5.5, 4, 0)),
            line(poly([(12, 8), (15, 8), (15, 11)], r=S.r * 0.5)), shell(drop)]


@T("parking-lights", "Two D-shaped lamps back to back with short rays from each",
   ["side lights", "position lights", "sidelights", "dashboard light", "lamps", "parking lamps"])
def _(S):
    r = S.r
    left = [(10.5, 6), (8, 6), (6.5, 9), (6.5, 15), (8, 18), (10.5, 18)]
    right = [(24 - x, y) for x, y in left]
    return [shell(poly(left, closed=True, r=r)), shell(poly(right, closed=True, r=r)),
            line(seg(4.5, 8, 2.5, 6.5)), line(seg(4.5, 12, 2, 12)), line(seg(4.5, 16, 2.5, 17.5)),
            line(seg(19.5, 8, 21.5, 6.5)), line(seg(19.5, 12, 22, 12)), line(seg(19.5, 16, 21.5, 17.5))]


@T("heated-steering-wheel", "Steering wheel with three wavy heat lines rising above its rim",
   ["steering wheel heater", "warm wheel", "winter comfort", "car interior", "heat", "cold weather"])
def _(S):
    return [shell(circle(12, 15, 5.8)), detail(seg(6.2, 15, 17.8, 15)), detail(seg(12, 15, 12, 20.8)), dot(12, 15, 1.4),
            wave(8, 6.5, 2.3, 0.8), wave(12, 6.5, 2.3, 0.8), wave(16, 6.5, 2.3, 0.8)]


@T("head-up-display", "Windshield outline with an arrow and speed bars projected low in the middle",
   ["hud", "projected display", "windscreen display", "speed projection", "navigation arrow", "driver assistance"],
   aliases=["hud-display"])
def _(S):
    ws = "M3 18Q12 15 21 18L19 4.5Q12 3 5 4.5Z" if S.name == "rounded" else "M2.5 18.5Q12 14.5 21.5 18.5L19 4.5Q12 3 5 4.5Z"
    return [shell(ws), detail(seg(12, 8, 12, 12.5)), ahead((12, 7.5), -90, 2.4, S, detail), sq(7, 10.5, 2, 3.5), sq(15, 10.5, 2, 3.5)]


@T("surround-view-camera", "Car seen from above with camera view arcs on all four sides",
   ["360 camera", "around view", "birds eye view", "parking camera", "park assist", "cameras"])
def _(S):
    k = L(S, 2, 3)
    return [shell(rect(8, 6.5, 8, 11, k)), detail("M9.5 11Q12 10 14.5 11"),
            line(arc(12, 12, 9.5, -120, -60)), line(arc(12, 12, 9.5, 60, 120)),
            line(arc(12, 12, 9.5, 150, 210)), line(arc(12, 12, 9.5, -30, 30))]


@T("bike-bulb-horn", "Rubber squeeze bulb attached to a flared horn with a sound line",
   ["bicycle horn", "squeeze horn", "honk", "clown horn", "bike accessory", "bulb horn"], aliases=["bicycle-horn"])
def _(S):
    return [shell(circle(6, 16, 4)), line(seg(9.5, 13.5, 12, 11.5)),
            shell(poly([(12, 11.5), (14.5, 9), (19, 5), (19, 15), (14.5, 13.5)], closed=True, r=S.r * 0.5)),
            line(seg(22, 8, 22, 12))]


@T("fuzzy-dice", "Pair of dice with pips hanging from a string, like a rearview mirror charm",
   ["hanging dice", "mirror dice", "car charm", "retro", "lucky", "rearview mirror decoration"], aliases=["mirror-dice"])
def _(S):
    return [line(seg(12, 2.5, 12, 5)), line(poly([(6.5, 9), (12, 5), (17.5, 11)], r=0)),
            shell(rect(2.5, 9, 8, 8, L(S, 1, 2))), shell(rect(13.5, 11, 8, 8, L(S, 1, 2))),
            dot(6.5, 13, 1.1), dot(15.5, 13.5, 1), dot(19.5, 16.5, 1)]


@veh("overturned-car", "Car in side view lying upside down on its roof with its wheels in the air",
     ["rollover", "flipped car", "upside down", "crash", "accident", "wreck"], aliases=["car-rollover"])
def _(S):
    pts = [(3, 18), (3, 13.5), (5.5, 12.5), (8, 7), (16, 7), (18.5, 12.5), (21, 13.5), (21, 18)]
    return rotparts(auto(S, pts, W2), 170, (12, 12.5)) + [line(seg(2, 21.5, 22, 21.5))]


@veh("car-fire", "Car in side view with flames rising from the hood",
     ["burning car", "vehicle fire", "blaze", "engine fire", "emergency", "flames"], aliases=["burning-car"])
def _(S):
    pts = [(2.5, 18), (2.5, 13), (5, 12), (7.5, 8), (13.5, 8), (14.5, 12.5), (21.5, 13), (21.5, 18)]
    flame = "M17.5 11C15 11 14.2 9 15.3 7C15.7 8 16.5 8 16.5 8C16.2 5.5 17.2 4 18.5 3C18.7 5 21 6.5 21 9C21 10.3 19.5 11 17.5 11Z"
    return auto(S, pts, W2, solid(flame))


@veh("speeding-car", "Car in side view with horizontal speed lines streaming behind it",
     ["fast car", "speed", "racing", "overspeed", "rush", "velocity"], aliases=["fast-car"])
def _(S):
    pts = [(8, 18), (8, 13), (10, 12), (12, 8), (16.5, 8), (19, 12), (21.5, 13), (21.5, 18)]
    ws = [(11, 18, 2), (18.5, 18, 2)]
    return auto(S, pts, ws, detail(seg(10, 12, 19, 12)), line(seg(2, 9.5, 6, 9.5)), line(seg(3.5, 13, 6, 13)),
                line(seg(2, 16.5, 6, 16.5)))


@veh("cab-over-truck", "Truck with a flat vertical front where the cab sits directly over the engine",
     ["cabover", "flat nose truck", "forward control", "box truck", "lorry", "delivery truck"], aliases=["cabover-truck"])
def _(S):
    pts = [(2.5, 18), (2.5, 4.5), (14, 4.5), (14, 7), (21.5, 7), (21.5, 18)]
    return auto(S, pts, W2, detail(seg(14, 7, 14, 14)), detail(rect(16.5, 9.5, 3.5, 3.5, 0)))


@T("mechanics-creeper", "Low padded board on caster wheels with a raised headrest for sliding under cars",
   ["creeper", "garage creeper", "mechanic board", "workshop", "under car", "auto repair"], aliases=["garage-creeper"])
def _(S):
    return [shell(rect(2.5, 13.5, 19, 3.5, L(S, 0.5, 1.7))), line("M3 13.5Q3 9.5 8.5 10.5"), shell(circle(6, 19.5, 1.7)),
            shell(circle(18, 19.5, 1.7))]


@T("banana-seat-bike", "Retro bicycle with a long banana saddle, high-rise handlebars and a sissy bar",
   ["muscle bike", "retro bicycle", "chopper bicycle", "1970s", "kids bike", "bmx cruiser"], aliases=["chopper-bicycle"])
def _(S):
    return [shell(circle(5.5, 17, 4)), shell(circle(18.5, 17, 4)), line(poly([(5.5, 17), (10, 17), (8.5, 10)], r=S.r * 0.4)),
            line(poly([(10, 17), (16, 11), (18.5, 17)], r=S.r * 0.4)), shell(poly([(2.5, 8), (3.5, 6.5), (11, 7), (9.5, 9)], closed=True, r=S.r * 0.4)),
            line(poly([(16, 11), (15.5, 4.5), (19.5, 4.5)], r=S.r * 0.4)), line(seg(3, 17, 3, 11))]


@T("emergency-light-bar", "Roof light bar with two domed lamps and rays shooting out from each end",
   ["beacon", "siren", "police lights", "flashing lights", "strobe", "patrol"], aliases=["lightbar"])
def _(S):
    return [shell(rect(6, 14, 12, 4, L(S, 0.5, 1.5))), line(arc(9, 14, 3, 180, 360)), line(arc(15, 14, 3, 180, 360)),
            line(seg(2.5, 7.5, 4.5, 9.5)), line(seg(2, 13, 4.5, 13)), line(seg(21.5, 7.5, 19.5, 9.5)), line(seg(22, 13, 19.5, 13))]


@T("radar-speed-gun", "Handheld radar gun with a pistol grip and radio waves coming from its front",
   ["speed camera", "police radar", "speed trap", "lidar gun", "traffic enforcement", "speed check"],
   aliases=["speed-gun"])
def _(S):
    return [shell(rect(2.5, 5, 11, 7, L(S, 1.5, 3))), line(poly([(5, 12), (5.5, 21), (9.5, 21), (10, 12)], r=S.r * 0.5)),
            line(arc(14.5, 8.5, 4.2, -50, 50)), line(arc(14.5, 8.5, 7.5, -50, 50)), dot(11, 8.5, 1)]


@T("starter-motor", "Electric starter motor with a small solenoid on top and a pinion gear at the front",
   ["starter", "engine starter", "cranking", "car electrical", "solenoid", "auto part"], aliases=["car-starter"])
def _(S):
    return [shell(rect(2.5, 10, 13, 8, L(S, 1.5, 3))), shell(rect(5, 5, 7.5, 3.5, L(S, 0.5, 1.2))), line(seg(8.75, 3, 8.75, 5)),
            line(seg(15.5, 14, 17.5, 14)), shell(poly(star(19.8, 14, 3, 2, 6, -90), closed=True))]


@T("window-crank", "Old-style car window winder: a crank arm with a round knob over a round base plate",
   ["window winder", "window handle", "manual window", "door handle", "vintage car", "winder"], aliases=["window-winder"])
def _(S):
    return [shell(circle(8.5, 15.5, 5.5)), dot(8.5, 15.5, 1.4), detail(seg(8.5, 15.5, 15.5, 8.5)), shell(rect(15.2, 3.2, 5.6, 5.6, L(S, 0.5, 2.8)))]


@T("car-location-pin", "Map pin marker with a small car inside its round head",
   ["car finder", "parked car", "find my car", "car park", "vehicle location", "gps"], aliases=["find-my-car"])
def _(S):
    pin = ("M12 22C7 16.5 4.5 13 4.5 9.3A7.5 7.5 0 0 1 19.5 9.3C19.5 13 17 16.5 12 22Z" if S.name != "rounded" else
           "M13.4 20.6Q12 22.3 10.6 20.6C7 16.5 4.5 13 4.5 9.3A7.5 7.5 0 0 1 19.5 9.3C19.5 13 17 16.5 13.4 20.6Z")
    car = "M8 11.5V10L9.2 8H14.8L16 10V11.5Z"
    return [shell(pin), Part("dot", car), Part("dot", circle(9.6, 12.3, 0.9)), Part("dot", circle(14.4, 12.3, 0.9))]


@T("adult-tricycle", "Upright three-wheeled bicycle in side view with a large basket over the rear axle",
   ["trike", "three wheel bike", "senior bike", "cargo trike", "adult trike", "tricycle basket"])
def _(S):
    return [shell(circle(6.5, 17, 4)), shell(circle(18.5, 17, 4)), shell(rect(2, 7.5, 9, 5.5, L(S, 0.5, 1.2))),
            line(poly([(6.5, 17), (12, 17), (11, 7)], r=S.r * 0.4)), line(poly([(12, 17), (15.5, 8), (18.5, 17)], r=S.r * 0.4)),
            line(seg(15.5, 8, 15, 4.5)), line(seg(13.5, 4.5, 18.5, 4.5))]


@T("tire-tracks", "Two parallel trails of zig-zag tread marks narrowing into the distance",
   ["tyre tracks", "skid marks", "off road", "trail", "tread marks", "dirt road"], aliases=["tyre-tracks"])
def _(S):
    def zig(x0, x1):
        pts = []
        n = 7
        for i in range(n + 1):
            t = i / n
            y = 21 - 18 * t
            x = x0 + (x1 - x0) * t + (1.6 if i % 2 else -1.6) * (1 - 0.35 * t)
            pts.append((x, y))
        return pts
    return [line(poly(zig(5.5, 9.5), r=0)), line(poly(zig(18.5, 14.5), r=0))]


@veh("amphibious-car", "Boat-hulled car with wheels, driving into water with a wave line below",
     ["water crossing", "water car", "swimming car", "boat car", "floating car", "land and water"])
def _(S):
    pts = [(3, 16.5), (3, 12), (5, 11), (8, 7), (15, 7), (17.5, 11), (21, 12), (21, 16.5)]
    ws = [(7, 16.5, 2), (17, 16.5, 2)]
    return auto(S, pts, ws, line("M2 21Q4.5 19 7 21T12 21T17 21T22 21"), yb=16.5)


@veh("billboard-truck", "Truck carrying a big flat rectangular advertising billboard panel on its back",
     ["advertising truck", "mobile billboard", "ad truck", "promotion", "outdoor advertising", "marketing"],
     aliases=["advertising-truck"])
def _(S):
    pts = [(2.5, 18), (2.5, 15.5), (14, 15.5), (14, 10), (17.5, 10), (21.5, 13.5), (21.5, 18)]
    return auto(S, pts, W2, shell(rect(2.5, 2.5, 11.5, 9, L(S, 0.5, 1.5))), detail(seg(5, 7, 11.5, 7)))


@T("cb-radio", "Car CB radio box with a knob and display, and a handheld microphone on a cord",
   ["citizens band", "two way radio", "trucker radio", "walkie", "handset", "radio mic"], aliases=["citizens-band-radio"])
def _(S):
    return [shell(rect(2.5, 3.5, 13, 9, L(S, 1.5, 3))), detail(rect(4.5, 5.5, 5, 2.5, 0)), dot(12.5, 7.5, 1.3),
            line("M9 12.5V16Q9 18.5 12 18.5H18"), shell(rect(17.5, 10.5, 4.5, 10, L(S, 1, 2)))]


@veh("gullwing-car", "Low sports coupe in side view with its door raised high like a wing",
     ["gull wing", "supercar", "scissor doors", "sports car", "exotic car", "butterfly doors"], aliases=["gull-wing-car"])
def _(S):
    pts = [(3, 18), (3, 14.5), (8.5, 11), (15, 11), (18, 13.5), (21.5, 14.5), (21.5, 18)]
    return auto(S, pts, W2, shell(poly([(14.5, 11), (12.5, 3.5), (7, 5.5), (9, 11)], closed=True, r=S.r * 0.5)))
