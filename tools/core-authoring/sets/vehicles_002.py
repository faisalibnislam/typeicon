"""TypeIcon Core: vehicles (batch 002, car parts, bicycle parts and dashboard symbols).

Parts are drawn as simple front or side views on the 24 grid. Open frames use rings and strokes in every style;
closed housings are shells so Filled turns them solid with knocked-out details.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, icon, line, path_to_d, poly, rect,
    regular, seg, shell, solid,
)
from geometry import fmt, polar

CAT = "vehicles"


def ring(x, y, r):
    return line(circle(x, y, r))


def drop(x, y, s=1.0):
    """Small oil/fuel drop with its tip at (x, y - 3s) and round belly below."""
    return (f"M{fmt(x)} {fmt(y - 3 * s)}C{fmt(x)} {fmt(y - 3 * s)} {fmt(x - 2.2 * s)} {fmt(y - 0.4 * s)} "
            f"{fmt(x - 2.2 * s)} {fmt(y + 0.8 * s)}A{fmt(2.2 * s)} {fmt(2.2 * s)} 0 0 0 {fmt(x + 2.2 * s)} {fmt(y + 0.8 * s)}"
            f"C{fmt(x + 2.2 * s)} {fmt(y - 0.4 * s)} {fmt(x)} {fmt(y - 3 * s)} {fmt(x)} {fmt(y - 3 * s)}Z")


def sq(x, y, w, h, rx=0.0):
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


FILL = Style("filled", "butt", "miter", R=2.0, r=0.0)  # pseudo-style: Line geometry for Filled designs


def isF(S):
    return S.name == "filled"


def L(S, a, b):
    """Pick a value for Line/Filled (a) or Rounded (b)."""
    return b if S.name == "rounded" else a


def wheel(x, y=18.0, r=2.0):
    """Side-view wheel: a ring in Line/Rounded; a solid disc cut 1 px clear of the body in Filled."""
    p = shell(circle(x, y, r))
    p.wheel = (x, y, r)
    return p


def body(S, pts, ws, yb=None, r=None):
    """Side-view body; the bottom edge is left open where a wheel crosses it."""
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
        rest = [p for p in parts if not getattr(p, "wheel", None)]
        out = filled_region(rest) if rest else None
        if wh:
            cut = U(*[P(circle(x, y, r + 2)) for x, y, r in wh])
            discs = U(*[P(circle(x, y, r + 1)) for x, y, r in wh])
            out = U(D(out, cut), discs) if out is not None else discs
        return out
    return f


def veh(name, description, tags, aliases=()):
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=veh_filled(fn))(fn)
    return deco


def rbox(o, ang, a0, a1, hw):
    """Rotated box along an axis from point o at angle ang (degrees): axial a0..a1, half width hw."""
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))

    def pt(a, b):
        return (o[0] + a * c - b * s, o[1] + a * s + b * c)
    return [pt(a0, -hw), pt(a1, -hw), pt(a1, hw), pt(a0, hw)]


W2 = [(6.5, 18, 2), (17.5, 18, 2)]


# =========================================================================== chunk 1

@icon("step-through-bike", CAT, "City bicycle with a low dipping frame and a front basket",
      tags=["city bike", "dutch bike", "ladies bike", "commuter", "cycling", "bicycle", "basket"])
def _(S):
    R, F, B, St, H = (5.5, 17.5), (18, 17.5), (11.5, 17.5), (8.5, 10), (14, 10)
    return [ring(*R, 3.5), ring(*F, 3.5),
            line(poly([R, St, B], r=S.r * 0.5)), line(seg(*St, 8.5, 7.5)), line(seg(6.5, 7, 10.5, 7)),
            line("M14 10C13.5 13 12.5 15 11.5 17.5"), line(seg(*F, *H)),
            line(poly([(11.5, 6.5), (14, 6.5), (14, 10)], r=S.r * 0.5)),
            shell(rect(15.5, 4, 6, 4.5, L(S, 0.5, 1.5)))]


@icon("car-battery", CAT, "Rectangular battery box with two round terminal posts on top marked plus and minus",
      tags=["battery", "12 volt", "accumulator", "jump start", "car", "power", "terminals"])
def _(S):
    return [shell(rect(3, 9, 18, 11, S.R)), solid(rect(6, 5.5, 3.5, 3.5)), solid(rect(14.5, 5.5, 3.5, 3.5)),
            detail(seg(6, 14.5, 10, 14.5)), detail(seg(8, 12.5, 8, 16.5)), detail(seg(14, 14.5, 18, 14.5))]


@icon("car-radiator", CAT, "Car radiator with a finned core, a top tank and a round filler cap",
      tags=["radiator", "cooling", "coolant", "engine", "car", "overheating", "fins"])
def _(S):
    return [shell(rect(3, 6, 18, 14, S.R)), solid(rect(10, 3, 4, 3)),
            detail(seg(3.5, 10, 20.5, 10)),
            detail(seg(8, 13, 8, 18)), detail(seg(12, 13, 12, 18)), detail(seg(16, 13, 16, 18))]


@icon("exhaust-pipe", CAT, "Car tailpipe with a flared chrome tip and a wavy puff of exhaust gas",
      tags=["tailpipe", "muffler tip", "emissions", "exhaust", "car", "fumes", "pollution"])
def _(S):
    return [shell(poly([(2.5, 10), (10, 10), (10, 8), (15.5, 6), (15.5, 18), (10, 16), (10, 14), (2.5, 14)],
                       closed=True, r=S.r)),
            line("M19 8C21 9.5 21 10.5 19 12S17.5 14.5 19 16")]


@icon("catalytic-converter", CAT, "Flat oval canister with a pipe at each end and a honeycomb of cells inside",
      tags=["cat", "exhaust", "emissions", "converter", "car part", "muffler", "pipe"])
def _(S):
    rr = 3 if S.name == "line" else 5.5
    return [shell(rect(5.5, 5.5, 13, 13, rr)), line(seg(2, 12, 5.5, 12)), line(seg(18.5, 12, 22, 12)),
            dot(9.5, 9.5, 1.2), dot(14.5, 9.5, 1.2), dot(9.5, 14.5, 1.2), dot(14.5, 14.5, 1.2)]


@icon("oil-dipstick", CAT, "Long thin dipstick with a loop handle and fill marks, with an oil drop below the tip",
      tags=["dipstick", "oil level", "engine", "check oil", "car", "maintenance", "fluid"])
def _(S):
    return [shell(rect(3.5, 3.5, 5, 5, 2.4 if S.name == "rounded" else 1)), line(seg(8.5, 8.5, 15, 15)),
            line(seg(11, 11, 13, 9)), line(seg(13.5, 13.5, 15.5, 11.5)),
            shell(drop(17, 20, 1.0))]


@icon("motor-oil", CAT, "Tall engine oil bottle with a side handle, an off-centre spout and an oil drop label",
      tags=["engine oil", "lubricant", "oil bottle", "car care", "garage", "maintenance", "oil change"])
def _(S):
    return [shell(poly([(5.5, 21), (5.5, 11), (8.5, 8), (8.5, 3.5), (12.5, 3.5), (12.5, 8), (15.5, 11), (15.5, 21)],
                       closed=True, r=S.r)),
            line("M15.5 12h2.5a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2h-2.5"),
            Part("dot", drop(10.5, 17, 1.0))]


@icon("engine-air-filter", CAT, "Rectangular pleated air filter panel with zig-zag folds inside a rim",
      tags=["air filter", "pleated filter", "intake", "engine", "car part", "maintenance", "cabin filter"])
def _(S):
    return [shell(rect(3, 5, 18, 14, S.R)),
            detail(poly([(6, 9), (8.5, 15), (11, 9), (13.5, 15), (16, 9), (18, 15)], r=S.r * 0.3))]


@icon("brake-caliper", CAT, "Brake caliper clamped over the edge of a brake disc with two bolts",
      tags=["brake", "disc brake", "rotor", "caliper", "car part", "braking", "wheel"])
def _(S):
    return [line(arc(9.5, 13, 7.5, 55, 305)), ring(9.5, 13, 2),
            shell(rect(13, 6.5, 8, 13, S.R)), dot(17, 10, 1.1), dot(17, 16, 1.1)]


@icon("brake-pad", CAT, "Curved brake pad block on a metal backing plate with two rivets",
      tags=["brake pads", "friction", "disc brake", "car part", "braking", "garage", "replacement"])
def _(S):
    c = (12, 22)
    ro, ri = 15.5, 8.5
    a0, a1 = -125, -55
    pts = [polar(*c, ro, a0)]
    pts += [polar(*c, ro, a0 + (a1 - a0) * i / 6) for i in range(1, 7)]
    pts += [polar(*c, ri, a1 - (a1 - a0) * i / 6) for i in range(0, 7)]
    return [shell(poly(pts, closed=True, r=S.r * 0.6)), detail(arc(*c, 12, -108, -72))]


@icon("car-axle", CAT, "Straight axle bar with a wheel hub at each end and a round differential in the middle",
      tags=["axle", "differential", "drivetrain", "wheel hub", "car part", "chassis", "transmission"])
def _(S):
    return [line(seg(6, 12, 9, 12)), line(seg(15, 12, 18, 12)), shell(circle(12, 12, 3.5)),
            shell(rect(2.5, 7.5, 3.5, 9, min(S.R, 1.5))), shell(rect(18, 7.5, 3.5, 9, min(S.R, 1.5)))]


@icon("drive-shaft", CAT, "Long tube shaft with a universal joint cross yoke at each end",
      tags=["propeller shaft", "cardan", "u-joint", "driveshaft", "drivetrain", "car part", "torque"])
def _(S):
    return [shell(rect(8, 9.5, 8, 5, min(S.R, 1.5))),
            line(poly([(2.5, 8), (5, 8), (5, 16), (2.5, 16)], r=S.r * 0.5)), line(seg(5, 12, 8, 12)),
            line(poly([(21.5, 8), (19, 8), (19, 16), (21.5, 16)], r=S.r * 0.5)), line(seg(19, 12, 16, 12))]


@icon("automatic-shifter", CAT, "Automatic gear lever with a round knob on a base plate beside a column of mode marks",
      tags=["gear shift", "gear lever", "transmission", "automatic", "console", "car interior", "drive mode"])
def _(S):
    return [ring(7.5, 6.5, 3), line(seg(7.5, 9.5, 7.5, 14)),
            shell(rect(3.5, 14, 8, 6, S.R)),
            dot(17.5, 5, 1.3), dot(17.5, 9.5, 1.3), dot(17.5, 14, 1.3), dot(17.5, 18.5, 1.3)]


@icon("fuel-tank", CAT, "Flat rounded vehicle fuel tank with a filler neck on one corner and a fuel drop",
      tags=["gas tank", "petrol tank", "fuel", "refuel", "car part", "reservoir", "gasoline"])
def _(S):
    return [shell(rect(3, 10, 16, 10, S.R)), shell(poly([(14.5, 10), (14.5, 5), (19, 3.5)], r=S.r * 0.5)),
            Part("dot", drop(10, 16, 1.0))]


@icon("headlight", CAT, "Car headlamp seen from the front with a round reflector and light beams shining forward",
      tags=["headlamp", "front light", "lamp", "beam", "car part", "lighting", "bulb"])
def _(S):
    return [shell(poly([(2.5, 7), (12, 5), (12, 19), (2.5, 17)], closed=True, r=S.r)), ring(7.5, 12, 2),
            line(seg(15.5, 7, 21.5, 5.5)), line(seg(15.5, 12, 21.5, 12)), line(seg(15.5, 17, 21.5, 18.5))]


# =========================================================================== chunk 2

@icon("tail-light", CAT, "Tall rear brake light lens split into two segments with light rays glowing to the side",
      tags=["rear light", "brake light", "taillamp", "stop light", "car part", "lighting", "reverse light"])
def _(S):
    return [shell(rect(4, 3.5, 11, 17, S.R)), detail(seg(4, 12, 15, 12)),
            line(seg(18.5, 6.5, 21.5, 5)), line(seg(18.5, 12, 22, 12)), line(seg(18.5, 17.5, 21.5, 19))]


@icon("car-horn", CAT, "Round snail-shaped car horn with a spiral body, a flared mouth and a sound wave",
      tags=["horn", "klaxon", "honk", "beep", "car part", "sound", "signal"])
def _(S):
    return [shell(circle(8.5, 12.5, 6)), detail("M8.5 12.5a1.8 1.8 0 0 1 3.6 0a3.6 3.6 0 0 1-7.2 0"),
            shell(poly([(14, 10), (18.5, 6.5), (18.5, 18.5), (14, 15)], closed=True, r=S.r * 0.6)),
            line("M21 10Q22.5 12.5 21 15")]


@icon("rearview-mirror", CAT, "Wide interior mirror with rounded ends hanging from a short stem at the top",
      tags=["interior mirror", "mirror", "rear view", "car interior", "windshield", "driving", "reflection"])
def _(S):
    rr = 2 if S.name == "line" else 4
    return [line(seg(9.5, 3.5, 14.5, 3.5)), line(seg(12, 3.5, 12, 8.5)),
            shell(rect(3, 8.5, 18, 8, rr)), detail(seg(7.5, 13.5, 10, 11.5))]


@icon("side-mirror", CAT, "Wing mirror on its arm seen from behind, a rounded housing with glass beside the door edge",
      tags=["wing mirror", "door mirror", "mirror", "car part", "exterior", "blind spot", "driving"])
def _(S):
    rr = 3 if S.name == "line" else 5
    return [line(seg(3, 4, 3, 20)), line(seg(3, 14, 8, 13)),
            shell(rect(8, 5.5, 13, 12, rr)), detail(seg(11.5, 14, 14.5, 9))]


@icon("windshield-wiper", CAT, "Curved windshield with a wiper arm pivoting from the bottom and an arc of cleared glass",
      tags=["wiper", "windscreen", "rain", "washer", "car part", "visibility", "clean glass"])
def _(S):
    return [shell(poly([(2.5, 19), (5, 5.5), (19, 5.5), (21.5, 19)], closed=True, r=S.r)),
            line(seg(12, 19, 7.9, 11.4)), detail(arc(12, 19, 8.5, -162, -75))]


@icon("sunroof", CAT, "Car roof seen from above with a glass panel slid back and an open hatch in front of it",
      tags=["moonroof", "roof", "open roof", "car part", "glass roof", "top view", "ventilation"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, 6 if S.name == "rounded" else 3.5)),
            sq(8, 6, 8, 4), detail(rect(8, 12, 8, 6, 0))]


@icon("car-door", CAT, "Single car door seen from outside with a window frame on top, a handle and a hinge edge",
      tags=["door", "car part", "vehicle door", "window", "handle", "body panel", "side door"])
def _(S):
    return [shell(poly([(3.5, 20.5), (3.5, 10.5), (8, 4), (20.5, 4), (20.5, 20.5)], closed=True, r=S.r)),
            detail(poly([(7, 10), (10, 6.5), (17, 6.5), (17, 10)], closed=True)),
            detail(seg(13, 15, 18, 15))]


@icon("driver-seat", CAT, "Car seat in side view with a headrest, a reclined backrest and a cushion on a sliding rail",
      tags=["car seat", "seat", "driver", "recline", "car interior", "seating", "headrest"])
def _(S):
    return [shell(poly([(4, 3), (9, 3), (11, 13), (20, 14), (20, 17.5), (6, 17.5), (4, 7)], closed=True, r=S.r)),
            detail(seg(5, 6.5, 9, 6.5)), line(seg(3, 21, 21, 21))]


@icon("airbag", CAT, "Steering wheel rim with a large round airbag bursting out of its centre",
      tags=["safety", "crash", "steering wheel", "inflated", "car safety", "collision", "restraint"])
def _(S):
    return [line(arc(12, 12, 10, 35, 145)), line(seg(12, 14.5, 12, 21)),
            shell(circle(12, 9.5, 5.5)), line(seg(3.5, 4, 5.5, 5.5)), line(seg(20.5, 4, 18.5, 5.5)),
            line(seg(2.5, 10, 4.5, 10)), line(seg(19.5, 10, 21.5, 10))]


@icon("car-pedals", CAT, "Three pedals side by side from the driver's view: clutch, brake and a taller accelerator",
      tags=["pedal", "clutch", "brake", "accelerator", "gas pedal", "manual car", "driving"])
def _(S):
    k = 2 if S.name == "rounded" else 1
    return [shell(rect(3, 12, 4.5, 8, k)), line(seg(5.25, 12, 5.25, 4)),
            shell(rect(10.5, 12, 4.5, 8, k)), line(seg(12.75, 12, 12.75, 4)),
            shell(rect(18, 6, 3.5, 14, k))]


@icon("handbrake", CAT, "Car hand brake lever tilted up from a console with a grip on its tip",
      tags=["parking brake", "emergency brake", "e-brake", "lever", "car interior", "console", "handbrake lever"])
def _(S):
    return [shell(rect(3, 17, 18, 4, S.R)), line(seg(7.5, 17, 13.5, 9)),
            shell(poly([(12.2, 8), (16.2, 3), (18.8, 5), (14.8, 10)], closed=True, r=S.r * 0.5))]


@icon("car-key-fob", CAT, "Car remote key with an oval fob, buttons and a flip-out metal key blade",
      tags=["key fob", "remote key", "keyless", "lock", "unlock", "car key", "smart key"])
def _(S):
    rr = 3 if S.name == "line" else 5.5
    return [shell(rect(6, 9, 12, 12, rr)), line(seg(12, 9, 12, 3.5)), line(seg(12, 5, 14.5, 5)),
            line(seg(12, 7.5, 14.5, 7.5)), sq(9, 12.5, 6, 2, 1), sq(9, 16.5, 6, 2, 1)]


@icon("car-air-vent", CAT, "Dashboard air vent with horizontal slats and a small tab, air lines flowing out",
      tags=["vent", "air conditioning", "ventilation", "climate", "car interior", "airflow", "heater"])
def _(S):
    return [shell(rect(3, 5, 13, 14, S.R)), detail(seg(5.5, 9.5, 13.5, 9.5)), detail(seg(5.5, 14.5, 13.5, 14.5)),
            line(seg(19, 8, 22, 8)), line(seg(19, 12, 22, 12)), line(seg(19, 16, 22, 16))]


@icon("car-dashboard", CAT, "Car dashboard from the driver's seat with a steering wheel in front of two round dials",
      tags=["dashboard", "instrument panel", "cockpit", "steering wheel", "dials", "driving", "car interior"])
def _(S):
    d, w = L(S, 2, 2.4), L(S, 5, 5.3)
    return [ring(7, 5.5, d), ring(17, 5.5, d), ring(12, 16, w), line(seg(6.7, 16, 17.3, 16)), line(seg(12, 16, 12, 21.3))]


@icon("odometer", CAT, "Row of rolling number drums in a small window with a tiny speedometer arc above",
      tags=["mileage", "distance counter", "kilometres", "miles", "trip meter", "dashboard", "car"])
def _(S):
    return [shell(rect(3, 13.5, 18, 7, S.R)), detail(seg(7.5, 13.5, 7.5, 20.5)), detail(seg(12, 13.5, 12, 20.5)),
            detail(seg(16.5, 13.5, 16.5, 20.5)), line(arc(12, 10, 7.5, 195, 345)), line(seg(12, 10, 15, 5.5))]


# =========================================================================== chunk 3

@icon("license-plate", CAT, "Rectangular vehicle number plate with rounded corners, two screw holes and blank characters",
      tags=["number plate", "registration", "licence plate", "plate", "car", "tag", "vehicle id"])
def _(S):
    return [shell(rect(2.5, 6.5, 19, 11, S.R)), dot(5.2, 9, 0.9), dot(18.8, 9, 0.9),
            sq(7, 11, 1.8, 4), sq(10.2, 11, 1.8, 4), sq(13.4, 11, 1.8, 4), sq(16.6, 11, 1.8, 4)]


@icon("tow-hitch", CAT, "Rear bumper with a receiver tube and a tow ball on a short neck",
      tags=["tow bar", "towbar", "trailer hitch", "tow ball", "towing", "caravan", "vehicle rear"])
def _(S):
    return [shell(rect(2.5, 5, 3.5, 15, L(S, 0.5, 1.75))), shell(rect(6, 15, 14, 3.5, L(S, 0.5, 1.75))),
            line(seg(17, 12.5, 17, 15)), shell(circle(17, 9.5, 3))]


@veh("roof-rack", "Car in side view with two crossbars on the roof holding a strapped-down bundle of luggage",
     ["roof bars", "luggage", "cargo", "baggage", "holiday", "car", "roof carrier"])
def _(S):
    pts = [(3, 18), (3, 14.5), (6.5, 12), (15.5, 12), (18.5, 14.5), (21, 15.5), (21, 18)]
    return auto(S, pts, W2) + [shell(rect(5.5, 3.5, 11, 5.5, S.R * 0.5)), line(seg(8, 9, 8, 12)),
                               line(seg(14, 9, 14, 12)), detail(seg(11, 3.5, 11, 9))]


@veh("roof-box", "Car in side view with a long streamlined cargo box pod mounted on its roof",
     ["cargo box", "roof pod", "luggage box", "ski box", "holiday", "car", "roof carrier"])
def _(S):
    pts = [(3, 18), (3, 14.5), (6.5, 12), (15.5, 12), (18.5, 14.5), (21, 15.5), (21, 18)]
    return auto(S, pts, W2) + [shell(poly([(3.5, 9), (5.5, 4), (15, 4), (19.5, 9)], closed=True, r=S.r * 1.5)),
                               line(seg(8, 9, 8, 12)), line(seg(14, 9, 14, 12))]


@icon("car-bike-rack", CAT, "Car rear with a rack holding a bicycle upright above the trunk",
      tags=["bike carrier", "bicycle rack", "cycling", "transport bike", "car", "trunk rack", "holiday"])
def _(S):
    return [ring(6.5, 8, 4), ring(17.5, 8, 4), line(poly([(6.5, 8), (11, 3.5), (17.5, 8)], r=S.r * 0.5)),
            line(seg(6.5, 12, 6.5, 16)), line(seg(17.5, 12, 17.5, 16)),
            shell(poly([(2.5, 21), (2.5, 18), (5, 16.5), (19, 16.5), (21.5, 18), (21.5, 21)], closed=True, r=S.r))]


@icon("wheel-rim", CAT, "Alloy car wheel seen face on with five spokes around a centre hub and a thin tyre edge",
      tags=["alloy wheel", "rim", "hubcap", "spokes", "car wheel", "tyre", "mag wheel"])
def _(S):
    spokes = []
    rounded = S.name == "rounded"
    for i in range(5):
        a = -90 + i * 72
        p0, p1 = polar(12, 12, 2.8, a), polar(12, 12, 8.5, a + (16 if rounded else 0))
        if rounded:
            c = polar(12, 12, 5.5, a + 14)
            spokes.append(detail(f"M{fmt(p0[0])} {fmt(p0[1])}Q{fmt(c[0])} {fmt(c[1])} {fmt(p1[0])} {fmt(p1[1])}"))
        else:
            spokes.append(detail(seg(*p0, *p1)))
    return [shell(circle(12, 12, 9.5))] + spokes + [detail(circle(12, 12, 2.8))]


@icon("spare-tire", CAT, "Round tyre with a wheel inside, held by a cover strap across its lower part",
      tags=["spare tyre", "spare wheel", "backup tire", "puncture", "breakdown", "car", "wheel"])
def _(S):
    ri, rh = (6.5, 2.5) if S.name == "line" else (6, 3)
    return [shell(circle(12, 12, 9.5)), detail(circle(12, 12, ri)), dot(12, 12, rh * 0.5), detail(seg(4.5, 19, 19.5, 19))]


@icon("snow-chains", CAT, "Tyre seen from the side wrapped in a crisscross ladder of chain links",
      tags=["tire chains", "winter tyres", "traction", "snow", "ice", "driving", "wheel"])
def _(S):
    pts = [polar(12, 12, 6 if i % 2 else 8.9, i * 22.5 - 90) for i in range(16)]
    return [shell(circle(12, 12, 9.5)), detail(poly(pts, closed=True, r=S.r * 0.4)), detail(circle(12, 12, L(S, 2, 2.4)))]


@icon("tire-pressure-gauge", CAT, "Pencil-style tyre gauge with a short chuck on one end and a measuring stick popping out",
      tags=["tyre gauge", "pressure gauge", "psi", "air pressure", "inflate", "garage", "car care"])
def _(S):
    o, ang = (4, 18), -38
    c, s = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    tip = (o[0] + 19 * c, o[1] + 19 * s)
    return [shell(poly(rbox(o, ang, 0, 3, 1.4), closed=True, r=S.r * 0.4)),
            shell(poly(rbox(o, ang, 3, 13, 2.4), closed=True, r=S.r * 0.6)),
            line(seg(o[0] + 13 * c, o[1] + 13 * s, *tip)),
            line(seg(tip[0] - 1.8 * s, tip[1] + 1.8 * c, tip[0] + 1.8 * s, tip[1] - 1.8 * c))]


@icon("flat-tire", CAT, "Tyre in side view sagging flat at the bottom with a nail stuck in its tread",
      tags=["flat tyre", "puncture", "deflated", "blowout", "roadside", "nail", "breakdown"])
def _(S):
    return [shell("M6 15.6A8 8 0 1 1 18 15.6Q20.5 17.5 19 19.5H5Q3.5 17.5 6 15.6Z"),
            detail(circle(12, 10.5, 2.4)), line(seg(14.5, 6.5, 19, 2.8)), line(seg(17.5, 2.2, 20.5, 5.2))]


@icon("lug-nut", CAT, "Hex wheel nut in three-quarter view with a round hole in its top face",
      tags=["wheel nut", "bolt", "hex nut", "fastener", "tyre change", "wheel", "garage"])
def _(S):
    return [shell(poly([(3.5, 8), (8, 4), (16, 4), (20.5, 8), (20.5, 16), (16, 20), (8, 20), (3.5, 16)],
                       closed=True, r=S.r * 1.6)),
            detail(poly([(3.5, 8), (8, 12), (16, 12), (20.5, 8)])), detail(seg(8, 12, 8, 20)),
            detail(seg(16, 12, 16, 20)), Part("dot", ellipse(12, 8, L(S, 2.6, 3), 1.3))]


@icon("car-cover", CAT, "Car shape draped in a loose fabric cover with folds and a scalloped hem",
      tags=["vehicle cover", "protect car", "tarp", "parking", "storage", "dust cover", "weatherproof"])
def _(S):
    top = poly([(2.5, 18.5), (2.5, 14), (6, 11), (9, 7), (15, 7), (18.5, 11), (21.5, 13.5), (21.5, 18.5)], r=S.r)
    if S.name == "rounded":
        hem = "Q18.5 16.5 16 18.5Q13.5 20.5 11 18.5Q8.5 16.5 6 18.5Q4 20 2.5 18.5"
    else:
        hem = "L17.5 17L14 19.5L10.5 17L7 19.5L2.5 18.5"
    return [shell(top + hem + "Z"), detail("M9.5 10C10.5 12 10.5 14 9.5 16"), detail("M15 10.5C16 12 16 14 15 15.5")]


@icon("mud-flap", CAT, "Rubber mud flap hanging behind a truck tyre with dirt spraying beside it",
      tags=["mudflap", "splash guard", "truck", "fender", "spray", "dirt", "wheel arch"])
def _(S):
    return [ring(9, 13.5, 3.8), dot(9, 13.5, 1.1), line(arc(9, 13.5, 6.8, 190, 340)),
            shell(rect(14.5, 11, 4.5, 9.5, L(S, 0.5, 1.5))),
            dot(21.5, 13, 1), dot(21.5, 17, 1), dot(21, 20.5, 1)]


@icon("car-bumper", CAT, "Front of a car with a wide rounded bumper bar highlighted across the lower edge",
      tags=["bumper", "fender", "front end", "collision", "car body", "crash", "car part"])
def _(S):
    return [shell(poly([(7, 3.5), (17, 3.5), (20, 9), (21.5, 10), (21.5, 16), (2.5, 16), (2.5, 10), (4, 9)],
                       closed=True, r=S.r)),
            dot(6.5, 12, 1.5), dot(17.5, 12, 1.5), solid(rect(2, 17.5, 20, 3.5, L(S, 0, 1.75)))]


@icon("car-spoiler", CAT, "Rear of a car with a raised wing spoiler on two struts above the trunk",
      tags=["rear wing", "wing", "sports car", "aerodynamics", "downforce", "tuning", "car part"])
def _(S):
    return [solid(rect(2.5, 3, 19, 3, L(S, 0, 1.5))), line(seg(7, 6, 7, 10)), line(seg(17, 6, 17, 10)),
            shell(poly([(5, 10), (19, 10), (21.5, 13), (21.5, 19.5), (2.5, 19.5), (2.5, 13)], closed=True, r=S.r)),
            dot(6.5, 15, 1.5), dot(17.5, 15, 1.5), detail(seg(9.5, 15.5, 14.5, 15.5))]


# =========================================================================== chunk 4

@icon("radiator-grille", CAT, "Car front with a pattern of horizontal grille slats between two headlights",
      tags=["grille", "front grill", "car front", "headlights", "air intake", "car part", "badge"])
def _(S):
    return [shell(rect(2.5, 4, 19, 16, S.R)), sq(4.5, 8, 3, 8, 1.5), sq(16.5, 8, 3, 8, 1.5),
            detail(seg(9.5, 9, 14.5, 9)), detail(seg(9.5, 12.5, 14.5, 12.5)), detail(seg(9.5, 16, 14.5, 16))]


@icon("tow-strap", CAT, "Coiled flat recovery strap with a loop at the end of its free tail",
      tags=["recovery strap", "tow rope", "snatch strap", "towing", "off road", "rescue", "coil"])
def _(S):
    return [shell(circle(10.5, 13.5, L(S, 7.5, 7.9))), detail(circle(10.5, 13.5, L(S, 3.2, 3.8))),
            line("M16.5 8.5C17.5 6 19 5.5 20 5.5"), ring(20.2, 4.6, L(S, 1.9, 1.6))]


@icon("ev-charging-cable", CAT, "Chunky electric vehicle plug with round pin sockets on its face and a curling cable",
      tags=["ev charger", "charging plug", "electric car", "type 2", "connector", "charge point", "e-mobility"])
def _(S):
    return [shell(circle(12, 9, 7.5)), dot(8.8, 7, 1.2), dot(15.2, 7, 1.2), dot(8.8, 11.4, 1.2),
            dot(15.2, 11.4, 1.2), dot(12, 14, 1.2), line("M12 16.5V18Q12 20.5 8 20.5H4")]


@icon("dash-cam", CAT, "Small windshield camera with a round lens and a recording dot on a suction mount",
      tags=["dashboard camera", "car camera", "recording", "driving", "evidence", "windscreen", "video"])
def _(S):
    return [shell(rect(3, 3.5, 18, 10, S.R)), ring(9, 8.5, 2.5), dot(16.5, 6.8, 1.1),
            line(seg(12, 13.5, 12, 16.5)), shell(poly([(7.5, 21), (9.5, 17.5), (14.5, 17.5), (16.5, 21)], closed=True, r=S.r * 0.5))]


@icon("car-phone-mount", CAT, "Phone held in a cradle with side clamps attached to a car air vent",
      tags=["phone holder", "phone cradle", "smartphone", "navigation", "gps", "car accessory", "vent clip"])
def _(S):
    return [shell(rect(7.5, 2.5, 9, 14, S.R)),
            line(poly([(4.5, 11), (4.5, 17.5), (19.5, 17.5), (19.5, 11)], r=S.r * 0.5)),
            line(seg(12, 17.5, 12, 20.5)), line(seg(7, 20.5, 17, 20.5))]


@icon("reversing-camera", CAT, "Car rear with a small camera above the plate and a view cone pointing back and down",
      tags=["backup camera", "rear view camera", "parking", "reverse", "parking sensor", "car safety", "rearview"])
def _(S):
    return [shell(poly([(5, 3.5), (19, 3.5), (21.5, 8), (21.5, 13), (2.5, 13), (2.5, 8)], closed=True, r=S.r)),
            dot(12, 6.5, 1.3), sq(8.5, 9.5, 7, 2, 1), line(seg(12, 16, 6, 21.5)), line(seg(12, 16, 18, 21.5))]


@veh("car-alarm", "Car in side view with sound waves ringing out above its roof",
     ["car security", "alarm", "siren", "anti theft", "burglar", "vehicle security", "noise"])
def _(S):
    pts = [(3, 19), (3, 16), (6.5, 13), (16, 13), (18.5, 15.5), (21, 16.5), (21, 19)]
    ws = [(6.5, 19, 1.8), (17.5, 19, 1.8)]
    return auto(S, pts, ws) + [line(arc(12, 10.5, 4, -150, -30)), line(arc(12, 10.5, 8, -150, -30))]


@icon("cracked-windshield", CAT, "Car windshield seen from the front with a spider-web crack spreading from one impact point",
      tags=["broken glass", "windscreen", "chip", "crack", "repair", "glass damage", "car"])
def _(S):
    return [shell(poly([(2.5, 19), (5, 5), (19, 5), (21.5, 19)], closed=True, r=S.r)),
            detail(poly([(8, 7.5), (11, 10), (12.5, 12)])), detail(poly([(12.5, 12), (17.5, 8.5)])),
            detail(poly([(12.5, 12), (16, 14), (17.5, 17.5)])), detail(poly([(12.5, 12), (10.5, 15), (7, 15.5)])),
            dot(12.5, 12, 1.6)]


@icon("tire-stack", CAT, "Pile of stacked tyres seen from slightly above, three rings high like a race barrier",
      tags=["tyre stack", "tire barrier", "tire wall", "racing", "recycling", "tire pile", "rubber"])
def _(S):
    ry = L(S, 3.2, 3.6)
    return [shell(f"M4 6V{fmt(19.5)}A8 {fmt(ry)} 0 0 0 20 19.5V6"), shell(ellipse(12, 6, 8, ry)),
            detail(f"M4 10.8a8 {fmt(ry)} 0 0 0 16 0"), detail(f"M4 15.2a8 {fmt(ry)} 0 0 0 16 0"),
            Part("dot", ellipse(12, 6, 3.4, 0.9))]


def pill(c, ang, length, hw, k):
    return poly(rbox(c, ang, -length / 2, length / 2, hw), closed=True, r=hw * k)


@icon("bicycle-chain", CAT, "Short length of bicycle chain showing alternating outer and inner oval links",
      tags=["chain", "drivetrain", "links", "cycling", "bike repair", "lubricate", "roller chain"])
def _(S):
    k = L(S, 0.5, 0.95)
    return [shell(pill((6, 18), -45, 8, 2.4, k)), shell(pill((10, 14), -45, 8, 1.6, k)),
            shell(pill((14, 10), -45, 8, 2.4, k)), shell(pill((18, 6), -45, 8, 1.6, k))]


@icon("bike-chainring", CAT, "Toothed front chainring with five spider arms and a crank arm ending in a pedal",
      tags=["chainring", "crankset", "crank", "sprocket", "cycling", "drivetrain", "pedal"])
def _(S):
    c = (10, 10)
    pts = []
    for i in range(8):
        a = i * 45 - 90
        pts += [polar(*c, 6.9, a - 12), polar(*c, 8.5, a - 8), polar(*c, 8.5, a + 8), polar(*c, 6.9, a + 12)]
    arms = [detail(seg(*polar(*c, 2, a), *polar(*c, 6.2, a))) for a in (-90, -18, 54, 126, 198)]
    return [shell(poly(pts, closed=True, r=S.r * 0.3)), *arms, line(seg(10, 10, 19, 18.5)),
            line(seg(17, 21, 21.5, 16.5))]


@icon("derailleur", CAT, "Rear bicycle derailleur: a cage holding two jockey pulleys that hangs from a mounting bracket",
      tags=["rear derailleur", "gear changer", "gears", "shifting", "cycling", "bike part", "drivetrain"])
def _(S):
    c = (8.5, 9.5), (13, 18.5)
    return [shell(poly(rbox((10.75, 14), 63.4, -6.2, 6.2, 4), closed=True, r=L(S, 2, 3.8))),
            Part("dot", circle(*c[0], 1.9)), Part("dot", circle(*c[1], 1.9)),
            shell(rect(14.5, 2.5, 6, 4.5, L(S, 1, 2))), line(seg(17, 7, 12.5, 11))]


@icon("bike-pedal", CAT, "Flat bicycle pedal in side view with a crank end, a platform and grip pins above and below",
      tags=["pedal", "platform pedal", "cycling", "crank", "pins", "spindle", "bike part"])
def _(S):
    return [line(seg(3.5, 3.5, 3.5, 18.5)), line(seg(3.5, 11, 8, 11)),
            shell(rect(8, 9, 13.5, 4, L(S, 0.5, 2))),
            line(seg(11.5, 9, 11.5, 6)), line(seg(15, 9, 15, 6)), line(seg(18.5, 9, 18.5, 6)),
            line(seg(11.5, 13, 11.5, 16)), line(seg(15, 13, 15, 16)), line(seg(18.5, 13, 18.5, 16))]


@icon("bike-saddle", CAT, "Bicycle saddle in side view with a long narrow nose and a wider rear, on its seat post",
      tags=["bike seat", "saddle", "seat post", "cycling", "comfort", "bicycle part", "perch"])
def _(S):
    return [shell(poly([(2.5, 8.5), (10, 8), (16, 8), (21.5, 6.5), (21.5, 11), (16, 13), (9, 12.5), (2.5, 10.5)],
                       closed=True, r=S.r)),
            line(seg(14, 13, 14, 21)), line(seg(10.5, 21, 17.5, 21))]


@icon("bike-handlebar", CAT, "Bicycle handlebars seen from the front with a stem in the middle, grips and two brake levers",
      tags=["handlebars", "handle bar", "stem", "brake levers", "cycling", "steering", "bike part"])
def _(S):
    return [line(seg(6, 7.5, 18, 7.5)), shell(rect(2.5, 5.5, 4, 4, L(S, 0.5, 2))), shell(rect(17.5, 5.5, 4, 4, L(S, 0.5, 2))),
            line(seg(12, 7.5, 12, 17)), shell(rect(10, 17, 4, 4, L(S, 0.5, 1.5))),
            line(seg(7.5, 10, 5.5, 14)), line(seg(16.5, 10, 18.5, 14))]


# =========================================================================== chunk 5

@icon("bicycle-wheel", CAT, "Single bicycle wheel with a thin tyre, crossing spokes and a small hub",
      tags=["wheel", "spokes", "rim", "cycling", "bike part", "hub", "tire"])
def _(S):
    off = L(S, 40, 28)
    sp = []
    for i in range(8):
        a = i * 45 - 90
        sgn = 1 if i % 2 else -1
        sp.append(line(seg(*polar(12, 12, 2.6, a), *polar(12, 12, 8.8, a + sgn * off))))
    return [ring(12, 12, 9.5)] + sp + [shell(circle(12, 12, L(S, 2.4, 2.8)))]


@icon("bike-bell", CAT, "Round bicycle bell dome on a handlebar clamp with a thumb lever and a ring line",
      tags=["bell", "ring", "ding", "cycling", "warning", "handlebar", "bike accessory"])
def _(S):
    r = L(S, 7.8, 8.6)
    return [shell(f"M{fmt(12 - r)} 14A{fmt(r)} {fmt(r)} 0 0 1 {fmt(12 + r)} 14Z"), detail(arc(12, 14, 4, 180, 360)),
            line(seg(12, 14, 12, 19)), line(seg(2.5, 19.5, 21.5, 19.5)), line(seg(17.5, 19.5, 20.5, 15.5))]


@icon("bicycle-pump", CAT, "Floor pump standing upright with a T-handle, a pressure dial at the base and a hose",
      tags=["bike pump", "floor pump", "inflate", "tyre pump", "air pump", "cycling", "repair"])
def _(S):
    return [line(seg(7, 3.5, 17, 3.5)), line(seg(12, 3.5, 12, 6.5)),
            shell(rect(9.5, 6.5, 5, 11.5, L(S, 0.5, 1.5))), shell(rect(5.5, 18, 13, 3, L(S, 0.5, 1.5))),
            ring(4.8, 13, L(S, 2.1, 2.3)), line("M14.5 9Q20 9 20 14V18")]


@icon("bicycle-helmet", CAT, "Aerodynamic cycling helmet in side view with a tapered tail, vent slots and a chin strap",
      tags=["bike helmet", "cycling helmet", "head protection", "safety", "road bike", "ventilation", "protective gear"])
def _(S):
    return [shell(poly([(2.5, 15.5), (6, 8.5), (11, 5), (17, 5.5), (21, 10), (21.5, 15.5)], closed=True, r=S.r * 1.5)),
            detail(seg(8.5, 13, 11, 9)), detail(seg(12.5, 13, 15, 9)), detail(seg(16.5, 13, 18, 10.5)),
            line(poly([(8, 15.5), (9, 19.5), (17, 19.5), (18, 15.5)], r=S.r * 0.5))]


@icon("bike-basket", CAT, "Wicker basket with a woven grid mounted under the front handlebars",
      tags=["basket", "wicker", "shopping", "cargo", "cycling", "handlebar", "city bike"])
def _(S):
    return [line(seg(2.5, 4.5, 21.5, 4.5)), line(seg(8, 4.5, 8, 8)), line(seg(16, 4.5, 16, 8)),
            shell(poly([(2.5, 8), (21.5, 8), (19, 20), (5, 20)], closed=True, r=S.r)),
            detail(seg(9.5, 10.5, 8.8, 17.5)), detail(seg(14.5, 10.5, 15.2, 17.5)), detail(seg(5.5, 14, 18.5, 14))]


@icon("bike-cassette", CAT, "Rear cassette in side view: a stepped cone of toothed sprockets from large to small",
      tags=["sprockets", "gears", "cogs", "rear gears", "cycling", "drivetrain", "freewheel"])
def _(S):
    return [shell(poly([(3, 4), (7, 4), (7, 6), (11, 6), (11, 8), (15, 8), (15, 10), (19, 10), (19, 14), (15, 14),
                        (15, 16), (11, 16), (11, 18), (7, 18), (7, 20), (3, 20)], closed=True, r=S.r * 0.5)),
            detail(seg(3, 12, 19, 12))]


def _tube_filled():
    outer = P(circle(12, 12, 10.5))
    hole = P(circle(12, 12, 3.5))
    stem = ST(seg(12, 8, 12, 10.5), 2.5, "butt", "miter", 4.0)
    return U(D(outer, hole), stem)


@icon("inner-tube", CAT, "Rubber inner tube ring lying flat with a valve stem pointing out of its inside edge",
      tags=["bike tube", "tyre tube", "puncture repair", "valve", "inflatable", "ring", "cycling"],
      filled=_tube_filled)
def _(S):
    return [shell(circle(12, 12, 9.5)), shell(circle(12, 12, L(S, 4.5, 5))), line(seg(12, 8, 12, 10.5))]


# =========================================================================== chunk 6 (dashboard symbols)

def brackets(S, r=9.2):
    return [line(arc(12, 12, r, 135, 225)), line(arc(12, 12, r, -45, 45))]


@icon("check-engine-light", CAT, "Dashboard warning symbol: an engine block with a raised intake and pipe stubs on each side",
      tags=["engine warning", "malfunction", "dashboard light", "engine fault", "obd", "service engine", "warning symbol"])
def _(S):
    return [shell(poly([(7, 9), (10, 9), (10, 6), (15, 6), (15, 9), (18, 9), (18, 18), (7, 18)], closed=True, r=S.r)),
            line(poly([(7, 11), (3.5, 11), (3.5, 16), (7, 16)], r=S.r * 0.5)), line(seg(18, 13.5, 21.5, 13.5))]


@icon("oil-pressure-light", CAT, "Dashboard symbol of a long-spouted oil can with a single drop falling from the tip",
      tags=["oil warning", "low oil", "oil can", "dashboard light", "lubrication", "engine oil", "warning symbol"])
def _(S):
    return [shell(rect(3.5, 10, 12, 9.5, S.R)), line(seg(15.5, 13, 20.5, 8.5)),
            line(poly([(7, 10), (7, 6.5), (11.5, 6.5)], r=S.r * 0.5)),
            Part("dot", drop(20.5, 17.5, 0.9))]


@icon("coolant-temperature-light", CAT, "Dashboard symbol of a thermometer standing in two rows of wavy liquid",
      tags=["engine temperature", "overheating", "coolant warning", "temperature gauge", "dashboard light", "hot engine",
            "warning symbol"])
def _(S):
    return [shell("M10.5 11V5A1.5 1.5 0 0 1 13.5 5V11A3.8 3.8 0 1 1 10.5 11Z"),
            line("M2.5 13q1.25-1.5 2.5 0t2.5 0"), line("M21.5 13q-1.25-1.5-2.5 0t-2.5 0"),
            line("M2.5 18.5q1.25-1.5 2.5 0t2.5 0"), line("M21.5 18.5q-1.25-1.5-2.5 0t-2.5 0")]


@icon("tire-pressure-light", CAT, "Dashboard symbol of a horseshoe-shaped tyre cross-section with an exclamation mark inside",
      tags=["tpms", "low tyre pressure", "flat tyre warning", "dashboard light", "tire warning", "inflate", "warning symbol"])
def _(S):
    return [shell(poly([(3.5, 19), (3.5, 12), (7, 5.5), (17, 5.5), (20.5, 12), (20.5, 19), (16.5, 19), (16.5, 12.5),
                        (14.5, 9.5), (9.5, 9.5), (7.5, 12.5), (7.5, 19)], closed=True, r=S.r * 1.5)),
            line(seg(12, 11.5, 12, 14.5)), dot(12, 17, 1.2)]


@icon("brake-warning-light", CAT, "Dashboard symbol of an exclamation mark inside a circle with curved brackets on both sides",
      tags=["brake warning", "brake system", "brake fluid", "dashboard light", "braking fault", "handbrake", "warning symbol"])
def _(S):
    return [ring(12, 12, L(S, 5, 5.4)), line(seg(12, 9.5, 12, 12.5)), dot(12, 14.8, 1.05)] + brackets(S)


@icon("parking-brake-light", CAT, "Dashboard symbol of the letter P inside a circle with curved brackets on both sides",
      tags=["parking brake", "handbrake", "park", "dashboard light", "electronic parking brake", "epb", "warning symbol"])
def _(S):
    return [ring(12, 12, L(S, 5, 5.4)), line("M10.8 15V9H12.6a1.8 1.8 0 0 1 0 3.6H10.8")] + brackets(S)


def _dlamp(S):
    return shell(poly([(12, 5.5), (8.5, 5.5), (4.5, 8), (3.5, 12), (4.5, 16), (8.5, 18.5), (12, 18.5)], closed=True,
                      r=S.r))


@icon("high-beam-light", CAT, "Dashboard symbol of a D-shaped lamp with straight horizontal light lines pointing forward",
      tags=["main beam", "full beam", "headlight", "dashboard light", "lights on", "night driving", "indicator"])
def _(S):
    return [_dlamp(S), line(seg(15.5, 7, 21.5, 7)), line(seg(15.5, 12, 21.5, 12)), line(seg(15.5, 17, 21.5, 17))]


@icon("low-beam-light", CAT, "Dashboard symbol of a D-shaped lamp with light lines angled downward",
      tags=["dipped beam", "headlight", "passing beam", "dashboard light", "lights on", "night driving", "indicator"])
def _(S):
    return [_dlamp(S), line(seg(15.5, 6.5, 21.5, 9.5)), line(seg(15.5, 11.5, 21.5, 14.5)),
            line(seg(15.5, 16.5, 21.5, 19.5))]


@icon("fog-light", CAT, "Dashboard symbol of a D-shaped lamp with angled light lines and a wavy vertical line of fog in front",
      tags=["fog lamp", "front fog light", "foggy weather", "dashboard light", "visibility", "driving lights", "indicator"])
def _(S):
    lamp = shell(poly([(10, 5.5), (7, 5.5), (4, 8), (3, 12), (4, 16), (7, 18.5), (10, 18.5)], closed=True, r=S.r))
    return [lamp, line("M13.5 4q-1.4 2 0 4t0 4t0 4t0 4"), line(seg(17, 6.5, 21.5, 8.5)), line(seg(17, 12, 21.5, 14)),
            line(seg(17, 17.5, 21.5, 19.5))]


@icon("hazard-lights", CAT, "Button symbol of two nested triangles, a small one inside a larger one",
      tags=["hazard warning", "emergency flashers", "four way flashers", "breakdown", "dashboard button", "warning triangle",
            "indicator"])
def _(S):
    return [shell(poly([(12, 3.5), (21.5, 20), (2.5, 20)], closed=True, r=S.r * 1.2)),
            detail(poly([(12, 9.5), (16, 16.5), (8, 16.5)], closed=True, r=S.r * 0.4))]


@icon("traction-control-light", CAT, "Dashboard symbol of a car seen from behind with two wavy skid lines beneath it",
      tags=["stability control", "esp", "skid", "slip", "dashboard light", "anti skid", "warning symbol"])
def _(S):
    return [shell(poly([(7, 3.5), (17, 3.5), (19.5, 8), (21, 9), (21, 14), (3, 14), (3, 9), (4.5, 8)], closed=True,
                       r=S.r)),
            dot(6.5, 11, 1.2), dot(17.5, 11, 1.2),
            line("M8 16C5.5 17.5 10.5 19.5 8 21.5"), line("M16 16C13.5 17.5 18.5 19.5 16 21.5")]


def _coil_pts():
    n = 41
    pts = []
    a, b = 0.62, 2.9
    for i in range(n):
        t = i / (n - 1) * 3 * 2 * math.pi
        pts.append((a * t - b * math.sin(t), -b * math.cos(t)))
    xs = [p[0] for p in pts]
    x0, x1 = min(xs), max(xs)
    k = 19 / (x1 - x0)
    return [(2.5 + (x - x0) * k, 12 + y * k) for x, y in pts]


@icon("glow-plug-light", CAT, "Dashboard symbol of a coiled spring wire loop, the diesel glow plug indicator",
      tags=["diesel", "preheat", "glow plug", "coil", "dashboard light", "cold start", "warning symbol"])
def _(S):
    return [line(poly(_coil_pts(), r=0))]


@icon("washer-fluid-light", CAT, "Dashboard symbol of a windshield outline with a fountain spray of dots rising inside it",
      tags=["screen wash", "washer fluid", "windscreen washer", "wiper fluid", "dashboard light", "low fluid", "warning symbol"])
def _(S):
    return [shell(poly([(3, 16), (5.5, 4.5), (18.5, 4.5), (21, 16)], closed=True, r=S.r)),
            dot(12, 12.5, 1), dot(12, 8.5, 1), dot(8.7, 12.5, 1), dot(7.7, 8.5, 1), dot(15.3, 12.5, 1), dot(16.3, 8.5, 1),
            sq(10.5, 18.5, 3, 2.5, 1)]
