"""TypeIcon Core: transport & vehicles.

Visual language:
  * Side-view road vehicles share one wheel grammar: r 2 wheels on the y 18 baseline at x 6.5 and 17.5, the
    body outline left open where the wheels sit (`vbody`), and in Filled the body cut 1 px clear of solid wheels
    (`veh_filled`). Bodies run 3–21 so every car, van and truck has the same length and weight.
  * Front-view vehicles (car, taxi, bus, train) stand on short solid tyres or rails at the bottom.
  * Two-wheelers draw their wheels as rings in every style (Filled makes them heavier), so frames stay readable.
  * Boats share a trapezoid hull sitting on y 19–20 with no water line.
  * Aircraft reuse one original top-view silhouette (`PLANE`), rotated per icon.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    rect, regular, seg, shell, solid,
)
from geometry import rotation, transform_path

CAT = "transport"
FILL = Style("filled", "butt", "miter", R=2.0, r=0.0)  # pseudo-style: Line geometry for Filled designs


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line/Filled (a) or Rounded (b)."""
    return b if S.name == "rounded" else a


def isF(S):
    return S.name == "filled"


def _p(p):
    return f"{fmt(p[0])} {fmt(p[1])}"


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def rot(d, deg, cx=12.0, cy=12.0):
    """Rotate a closed shape's d-string (open paths must be rotated point by point with rpt)."""
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpt(p, deg, c=(12.0, 12.0)):
    """Rotate a point about c (degrees, clockwise on screen)."""
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a)


def filled_from(fn):
    return lambda: filled_region(fn(FILL))


def T(name, description, tags, aliases=()):
    """Register a transport icon whose Filled design is built from `fn(FILL)`."""
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=filled_from(fn))(fn)
    return deco


# --------------------------------------------------------------------------- vehicle grammar

WX = (6.5, 17.5)  # standard wheel positions for side-view road vehicles


def wheel(x, y=18.0, r=2.0):
    """Side-view wheel: a ring in Line/Rounded; a solid disc cut 1 px clear of the body in Filled."""
    p = shell(circle(x, y, r))
    p.wheel = (x, y, r)
    return p


def vbody(S, pts, wheels=WX, yb=18.0, r=2.0):
    """Side-view body. `pts` run clockwise from the bottom-left corner over the top to the bottom-right corner;
    the bottom edge is left open where the wheels sit."""
    if isF(S):
        return [shell(poly(pts, closed=True))]
    xs = sorted(wheels)
    out = [shell(poly([(xs[0] - r, yb)] + list(pts) + [(xs[-1] + r, yb)], r=S.r))]
    for a, b in zip(xs, xs[1:]):
        out.append(line(seg(a + r, yb, b - r, yb)))
    return out


def veh_filled(fn):
    def f():
        parts = fn(FILL)
        wh = [p.wheel for p in parts if getattr(p, "wheel", None)]
        body = filled_region([p for p in parts if not getattr(p, "wheel", None)])
        cut = U(*[P(circle(x, y, r + 2)) for x, y, r in wh])
        discs = U(*[P(circle(x, y, r + 1)) for x, y, r in wh])
        return U(D(body, cut), discs)
    return f


def veh(name, description, tags, aliases=()):
    """Register a wheeled vehicle whose Filled design cuts the wheels clear of the body."""
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=veh_filled(fn))(fn)
    return deco


def car(S, pts, *extra):
    """Side-view car: body + the two standard wheels + extra parts."""
    return vbody(S, pts) + [wheel(WX[0]), wheel(WX[1]), *extra]


def tyres(S, xs=(4.5, 16), y=18.5, w=3.5, h=3.5):
    k = L(S, 0, 1)
    return [solid(rect(x, y, w, h, k)) for x in xs]


SEDAN = [(3, 18), (3, 12.5), (5, 11.5), (8, 7), (15, 7), (18, 11.5), (21, 12.5), (21, 18)]


# =========================================================================== cars

@T("car", "Car seen from the front", ["automobile", "vehicle", "drive", "auto", "motor", "road"], aliases=["automobile"])
def _(S):
    body = poly([(3, 19), (3, 12.5), (5, 11), (6.8, 5.5), (17.2, 5.5), (19, 11), (21, 12.5), (21, 19)], closed=True, r=S.r)
    return [shell(body), detail(seg(5, 11, 19, 11)), dot(7, 15, 1.25), dot(17, 15, 1.25), detail(seg(10, 15, 14, 15)),
            *tyres(S)]


@veh("car-side", "Saloon car seen from the side", ["sedan", "saloon", "automobile", "vehicle", "drive", "side view"],
     aliases=["sedan"])
def _(S):
    return car(S, SEDAN, detail(seg(5, 11.5, 18, 11.5)), detail(seg(11.5, 7, 11.5, 11.5)))


@T("taxi", "Taxi seen from the front with a roof sign", ["cab", "taxicab", "ride", "hail", "car", "rideshare"],
   aliases=["cab"])
def _(S):
    body = poly([(3, 19), (3, 13), (5, 11.5), (6.8, 7), (17.2, 7), (19, 11.5), (21, 13), (21, 19)], closed=True, r=S.r)
    return [shell(body), shell(rect(9, 3, 6, 3, min(S.R, 1))), detail(seg(5, 11.5, 19, 11.5)),
            dot(7, 15.25, 1.25), dot(17, 15.25, 1.25), *tyres(S)]


@veh("police-car", "Police car with a light bar on the roof", ["police", "patrol car", "cop car", "emergency", "siren", "law"],
     aliases=["patrol-car"])
def _(S):
    pts = [(3, 18), (3, 12.5), (5, 11.5), (8, 8), (15, 8), (18, 11.5), (21, 12.5), (21, 18)]
    return car(S, pts, detail(seg(5, 11.5, 18, 11.5)), detail(seg(11.5, 8, 11.5, 11.5)),
               shell(rect(9.5, 4.5, 4.5, 2.5, min(S.R, 0.75))), line(seg(5.5, 5.75, 7.5, 5.75)), line(seg(16, 5.75, 18, 5.75)))


@veh("convertible", "Open-top convertible car with a raked windscreen",
     ["cabriolet", "roadster", "open top", "sports car", "car", "drive"], aliases=["cabriolet", "roadster"])
def _(S):
    pts = [(3, 18), (3, 12), (4, 11), (14.5, 11), (21, 12.5), (21, 18)]
    return car(S, pts, line(seg(14.5, 11, 12, 6.5)), line(seg(7.5, 11, 6.5, 7.5)))


@veh("race-car", "Low racing car with a rear spoiler",
     ["racing", "formula", "motorsport", "speed", "grand prix", "sports car"], aliases=["racing-car"])
def _(S):
    pts = [(3, 18), (3, 8), (6, 8), (6.5, 11.5), (8.5, 11.5), (11, 8.5), (14.5, 8.5), (21, 13.5), (21, 18)]
    return car(S, pts, detail(seg(8.5, 11.5, 16.5, 11.5)))


@veh("pickup-truck", "Pickup truck with a cab and an open load bed",
     ["pickup", "ute", "truck", "load bed", "utility", "4x4"], aliases=["pickup", "ute"])
def _(S):
    pts = [(3, 18), (3, 11), (11, 11), (11, 6.5), (15.5, 6.5), (18.5, 11), (21, 11.5), (21, 18)]
    return car(S, pts, detail(seg(11, 11, 18.5, 11)))


@veh("minivan", "Minivan with a long roof and three side windows",
     ["mpv", "people carrier", "family car", "van", "carpool", "multi-purpose vehicle"], aliases=["mpv", "people-carrier"])
def _(S):
    pts = [(3, 18), (3, 8), (4.5, 6), (13, 6), (18, 10.5), (21, 11.5), (21, 18)]
    return car(S, pts, detail(seg(3, 10.5, 18, 10.5)), detail(seg(7.5, 6, 7.5, 10.5)), detail(seg(12.5, 6, 12.5, 10.5)))


@veh("van", "Panel van with a tall cargo body", ["cargo van", "panel van", "vehicle", "transit", "delivery", "work van"],
     aliases=["panel-van"])
def _(S):
    pts = [(3, 18), (3, 5), (14.5, 5), (18.5, 10), (21, 11), (21, 18)]
    return car(S, pts, detail(poly([(13, 5), (13, 10), (18.5, 10)], r=S.r * 0.5)))


@veh("delivery-van", "Delivery van speeding along with motion lines",
     ["delivery", "courier", "shipping", "parcel", "express", "dispatch"], aliases=["courier-van"])
def _(S):
    pts = [(6.5, 18), (6.5, 5), (15.5, 5), (18.5, 10), (21, 11), (21, 18)]
    body = vbody(S, pts, wheels=(9.5, 17.5))
    return body + [wheel(9.5), wheel(17.5), detail(poly([(14.5, 5), (14.5, 10), (18.5, 10)], r=S.r * 0.5)),
                   line(seg(3, 8, 5, 8)), line(seg(3, 12, 5, 12))]


@veh("wheelchair-transport", "Accessible van marked with a wheelchair",
     ["accessible transport", "wheelchair van", "paratransit", "mobility", "disability", "accessible taxi"],
     aliases=["accessible-van"])
def _(S):
    pts = [(3, 18), (3, 5), (15.5, 5), (18.5, 10), (21, 11), (21, 18)]
    return car(S, pts, detail(circle(10.5, 12, 2.75)),
               detail(poly([(7.3, 5.5), (8.2, 9.25), (12.8, 9.25), (14, 13.5), (16, 13.5)], r=S.r * 0.4)))


# =========================================================================== buses and trucks

@T("bus", "Bus seen from the front", ["coach", "public transport", "transit", "school bus", "city bus", "commute"],
   aliases=["coach"])
def _(S):
    return [shell(rect(4.5, 3, 15, 16, S.R)), detail(seg(4.5, 6, 19.5, 6)), detail(seg(4.5, 11.5, 19.5, 11.5)),
            dot(8, 15.25, 1.25), dot(16, 15.25, 1.25),
            line(poly([(4.5, 5), (3, 5), (3, 8.5)], r=S.r * 0.5)), line(poly([(19.5, 5), (21, 5), (21, 8.5)], r=S.r * 0.5)),
            *tyres(S, xs=(6, 15), y=19, w=3, h=3)]


@veh("truck", "Box lorry with a cab", ["lorry", "freight", "haulage", "cargo", "delivery truck", "hgv"], aliases=["lorry"])
def _(S):
    pts = [(3, 18), (3, 4.5), (14, 4.5), (14, 8), (18, 8), (21, 12), (21, 18)]
    return car(S, pts, detail(seg(14, 8, 14, 18)), detail(poly([(16, 8), (16, 12), (21, 12)], r=S.r * 0.5)))


@veh("fire-truck", "Fire engine with a ladder and a warning light",
     ["fire engine", "firefighters", "emergency", "rescue", "ladder", "fire brigade"], aliases=["fire-engine"])
def _(S):
    pts = [(3, 18), (3, 11), (14.5, 11), (14.5, 7), (18.5, 7), (21, 11.5), (21, 18)]
    return car(S, pts, detail(seg(14.5, 11, 14.5, 18)), detail(poly([(16.5, 7), (16.5, 11.5), (21, 11.5)], r=S.r * 0.5)),
               line(seg(3, 7.5, 12.5, 7.5)), line(seg(5.5, 7.5, 5.5, 11)), line(seg(9.5, 7.5, 9.5, 11)),
               dot(16.5, 4.5, 1.25))


@veh("tow-truck", "Tow truck with a lifting boom and hook",
     ["tow", "breakdown", "recovery", "roadside assistance", "wrecker", "towing"], aliases=["wrecker", "breakdown-truck"])
def _(S):
    pts = [(3, 18), (3, 13), (12, 13), (12, 7), (16.5, 7), (19, 11), (21, 11.5), (21, 18)]
    return car(S, pts, detail(seg(12, 11, 19, 11)),
               line(seg(10, 13, 4.5, 4.5)), line("M4.5 4.5V8.5A1.5 1.5 0 0 0 7.5 8.5"))


@veh("garbage-truck", "Refuse truck with a ribbed container and a cab",
     ["refuse truck", "rubbish", "waste", "bin lorry", "trash", "recycling"], aliases=["refuse-truck", "bin-lorry"])
def _(S):
    pts = [(3, 18), (3, 11), (5, 5), (14, 5), (14, 8.5), (18, 8.5), (21, 12.5), (21, 18)]
    return car(S, pts, detail(seg(14, 8.5, 14, 18)), detail(seg(8, 5, 8, 14)), detail(seg(11, 5, 11, 14)),
               detail(poly([(16, 8.5), (16, 12.5), (21, 12.5)], r=S.r * 0.5)))


# =========================================================================== two wheels and boards

@T("bicycle", "Bicycle with a diamond frame", ["bike", "cycling", "cycle", "pedal", "ride", "commute"], aliases=["bike"])
def _(S):
    return _bike(S)


def _bike(S, bar=(17.5, 7.5)):
    R, F, B, St, H = (6.5, 16.5), (17.5, 16.5), (11.5, 16.5), (9.5, 10), (15.5, 10)
    return [line(circle(*R, 3.5)), line(circle(*F, 3.5)),
            line(poly([R, St, H, B], closed=True, r=S.r * 0.5)), line(seg(*B, *St)),
            line(poly([F, H, (15, 7.5), bar], r=S.r * 0.5)),
            line(seg(7.5, 7.5, 11, 7.5)), line(seg(*St, 9.25, 7.5))]


@T("e-bike", "Electric bicycle with a lightning bolt", ["electric bike", "ebike", "pedelec", "e-cycle", "bike", "battery"],
   aliases=["electric-bike", "ebike"])
def _(S):
    bolt = poly([(19.5, 1.8), (17, 6), (19, 6), (18.2, 9.2), (21.6, 4.6), (19.6, 4.6)], closed=True, r=S.r * 0.2)
    return _bike(S, bar=(13, 7.5)) + [solid(bolt)]


@T("motorcycle", "Motorcycle seen from the side", ["motorbike", "bike", "rider", "moped", "chopper", "biker"],
   aliases=["motorbike"])
def _(S):
    return [line(circle(6, 17, 3)), line(circle(18, 17, 3)),
            shell(poly([(4, 11.5), (8.5, 11.5), (10, 10), (14, 10), (15, 12.5), (12.5, 15.5), (9.5, 15.5), (8, 13.5), (4, 13.5)],
                       closed=True, r=S.r * 0.5)),
            line(poly([(18, 17), (15.5, 8.5), (13.5, 8)], r=S.r * 0.5)), line(seg(6, 17, 9.5, 15))]


@T("scooter", "Motor scooter with a step-through floor", ["moped", "vespa style", "motor scooter", "commute", "city", "two-wheeler"],
   aliases=["moped"])
def _(S):
    body = poly([(3, 16), (3.5, 13), (6, 11), (11.5, 11), (12.5, 15), (15.5, 15), (16.5, 8), (18.5, 8), (17.5, 16)], closed=True, r=S.r * 0.5)
    return [line(circle(6, 18.5, 2.5)), line(circle(18, 18.5, 2.5)), shell(body),
            line(seg(17.5, 8, 17.5, 5)), line(seg(15.5, 5, 19.5, 5))]


@T("kick-scooter", "Kick scooter with a low deck and tall handlebar",
   ["push scooter", "scooter", "kick", "e-scooter", "micromobility", "ride"], aliases=["push-scooter"])
def _(S):
    return [line(circle(5.5, 19, 2)), line(circle(18.5, 19, 2)),
            line(seg(7.5, 16.5, 17, 16.5)),
            line(seg(18.5, 19, 16, 4.5)), line(seg(13.5, 4.5, 18.5, 4.5))]


@T("skateboard", "Skateboard seen from the side", ["skate", "board", "skating", "skater", "deck", "ollie"], aliases=["skate"])
def _(S):
    return [line(poly([(3, 10.5), (4.5, 13.5), (19.5, 13.5), (21, 10.5)], r=S.r)),
            shell(circle(7.5, 17.5, 2)), shell(circle(16.5, 17.5, 2))]


# =========================================================================== rail

@T("train", "Train seen from the front on its rails", ["railway", "rail", "locomotive", "commute", "station", "intercity"],
   aliases=["railway"])
def _(S):
    body = ("M5 17.5V8.5A5.5 5.5 0 0 1 10.5 3H13.5A5.5 5.5 0 0 1 19 8.5V17.5Z" if S.name == "rounded" else
            "M5 17.5V6.5A3.5 3.5 0 0 1 8.5 3H15.5A3.5 3.5 0 0 1 19 6.5V17.5Z")
    return [shell(body), detail(seg(5, 10, 19, 10)), dot(8.5, 13.75, 1.25), dot(15.5, 13.75, 1.25),
            line(seg(8, 17.5, 6.25, 21)), line(seg(16, 17.5, 17.75, 21))]


@T("tram", "Tram seen from the front with its pantograph on the overhead wire",
   ["streetcar", "trolley", "light rail", "tramway", "public transport", "city"], aliases=["streetcar"])
def _(S):
    return [shell(rect(4.5, 7.5, 15, 10.5, S.R)), detail(seg(4.5, 12, 19.5, 12)), dot(8, 15, 1.25), dot(16, 15, 1.25),
            line(poly([(9, 7.5), (12, 4.5), (15, 7.5)], r=S.r * 0.5)), line(seg(9.5, 3, 14.5, 3)),
            line(seg(8, 18, 6.75, 21)), line(seg(16, 18, 17.25, 21))]


@T("subway", "Metro train emerging from a tunnel", ["metro", "underground", "tube", "rapid transit", "subway train", "commute"],
   aliases=["metro", "underground"])
def _(S):
    return [line("M3 21V12A9 9 0 0 1 21 12V21"),
            shell(rect(7, 7, 10, 11, S.R * 0.75)), detail(seg(7, 11, 17, 11)), dot(9.5, 14.5, 1), dot(14.5, 14.5, 1),
            line(seg(9, 18, 8.25, 21)), line(seg(15, 18, 15.75, 21))]


@T("freight-train", "Freight train: a locomotive pulling a wagon on rails",
   ["cargo train", "goods train", "locomotive", "wagon", "railway freight", "rail"], aliases=["goods-train", "cargo-train"])
def _(S):
    k = S.R * 0.5
    loco = [(12.5, 16), (12.5, 5), (16.5, 5), (16.5, 9.5), (18.5, 9.5), (18.5, 5.5), (20.5, 5.5), (20.5, 9.5), (21, 9.5), (21, 16)]
    return [shell(rect(3, 8, 7.5, 8, k)), detail(seg(6.75, 8, 6.75, 16)),
            shell(poly(loco, closed=True, r=S.r * 0.4)), detail(seg(12.5, 9.5, 16.5, 9.5)),
            line(seg(10.5, 13, 12.5, 13)),
            dot(5, 17.75, 1.25), dot(8.5, 17.75, 1.25), dot(15.5, 17.75, 1.25), dot(19, 17.75, 1.25),
            line(seg(3, 21, 21, 21))]


@T("monorail", "Monorail car running on a single elevated beam", ["monorail", "elevated rail", "skytrain", "people mover", "rail", "airport train"],
   aliases=["skytrain"])
def _(S):
    car_ = poly([(3, 13), (3, 4.5), (15.5, 4.5), (21, 10), (21, 13)], closed=True, r=S.r)
    return [shell(car_), detail(seg(3, 9, 17, 9)), detail(seg(9, 4.5, 9, 9)),
            shell(rect(3, 15.5, 18, 1.5, 0.01 if S.name == "line" else 0.75)), line(seg(12, 17, 12, 21)),
            line(seg(8.5, 21, 15.5, 21))]


@T("cable-car", "Cable car cabin hanging from an aerial cable",
   ["gondola", "aerial tramway", "ropeway", "ski lift", "cableway", "mountain"], aliases=["gondola"])
def _(S):
    return [line(seg(3, 6, 21, 3)), line(seg(12, 4.5, 12, 8.5)),
            shell(rect(5.5, 8.5, 13, 12.5, S.R)), detail(seg(5.5, 14, 18.5, 14)), detail(seg(12, 8.5, 12, 14))]


# =========================================================================== air and space

_PLANE_R = [(12.9, 2.7), (13.4, 4), (13.4, 9.2), (21, 13.6), (21, 15.6), (13.4, 13.6), (13.4, 18.2),
            (16.4, 20.2), (16.4, 21.8), (12, 20.9)]
PLANE = [(12, 2)] + _PLANE_R + [(24 - x, y) for x, y in reversed(_PLANE_R[:-1])]


def plane_fit(deg, box):
    """The shared top-view aircraft rotated by deg (clockwise, 0 = nose up), scaled to fit box (x0, y0, x1, y1)."""
    pts = [rpt(p, deg) for p in PLANE]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    s = min((box[2] - box[0]) / (max(xs) - min(xs)), (box[3] - box[1]) / (max(ys) - min(ys)))
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    bx, by = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    return [(bx + (x - cx) * s, by + (y - cy) * s) for x, y in pts]


@icon("plane", CAT, "Aeroplane seen from above, heading up and to the right",
      tags=["airplane", "aeroplane", "flight", "airport", "travel", "airline"], aliases=["airplane", "aeroplane"])
def _(S):
    return [shell(poly(plane_fit(45, (3.5, 3.5, 20.5, 20.5)), closed=True, r=S.r * 0.5), stroke_miterlimit="2")]


@icon("plane-takeoff", CAT, "Aeroplane climbing away from the runway", 
      tags=["departure", "take off", "departing", "flight", "airport", "outbound"], aliases=["departure", "plane-departure"])
def _(S):
    return [shell(poly(plane_fit(65, (3.5, 3.5, 20.5, 16.5)), closed=True, r=S.r * 0.5), stroke_miterlimit="2"), line(seg(3, 20.5, 21, 20.5))]


@icon("plane-landing", CAT, "Aeroplane descending towards the runway",
      tags=["arrival", "landing", "arriving", "flight", "airport", "inbound"], aliases=["arrival", "plane-arrival"])
def _(S):
    return [shell(poly(plane_fit(115, (3.5, 3.5, 20.5, 16.5)), closed=True, r=S.r * 0.5), stroke_miterlimit="2"), line(seg(3, 20.5, 21, 20.5))]


@T("helicopter", "Helicopter with a main rotor, tail rotor and skids",
   ["chopper", "heli", "rotorcraft", "air ambulance", "flight", "rescue"], aliases=["chopper"])
def _(S):
    cabin = "M9 9.5H15C18 9.5 20.5 11.8 20.5 14.5C20.5 16.3 19.2 17.5 17 17.5H10.5C9.7 17.5 9 16.8 9 16Z"
    return [shell(cabin), detail(poly([(15, 9.5), (15, 13.5), (20.3, 13.5)], r=S.r * 0.5)),
            line(seg(9, 12.5, 3.5, 12.5)), line(seg(3.5, 9.5, 3.5, 15)),
            line(seg(4.5, 5.5, 21, 5.5)), line(seg(14, 5.5, 14, 9.5)),
            line(seg(8.5, 21, 20, 21)), line(seg(11.5, 17.5, 11.5, 21)), line(seg(17, 17.5, 17, 21))]


@T("rocket", "Rocket with fins and a round window", ["spaceship", "launch", "space", "startup", "missile", "boost"],
   aliases=["spaceship"])
def _(S):
    body = "M12 3C14.8 5.2 16 8.5 16 12V17.5H8V12C8 8.5 9.2 5.2 12 3Z"
    return [shell(body, stroke_miterlimit="1.5"), detail(circle(12, 10, 1.75)),
            shell(poly([(8, 12.5), (5, 15.5), (5, 19.5), (8, 17.5)], closed=True, r=S.r * 0.5)),
            shell(poly([(16, 12.5), (19, 15.5), (19, 19.5), (16, 17.5)], closed=True, r=S.r * 0.5)),
            line(seg(10.5, 19.5, 10.5, 21)), line(seg(13.5, 19.5, 13.5, 21))]


@T("hot-air-balloon", "Hot-air balloon with a basket", ["balloon ride", "hot air", "aerostat", "flight", "adventure", "sky"],
   aliases=["balloon-ride"])
def _(S):
    env = "M12 3C16.4 3 19.5 6.2 19.5 10C19.5 12.8 16.8 14.4 14.5 15.5H9.5C7.2 14.4 4.5 12.8 4.5 10C4.5 6.2 7.6 3 12 3Z"
    return [shell(env), detail("M12 3C9.8 5 9.2 11 10.2 15.5"), detail("M12 3C14.2 5 14.8 11 13.8 15.5"),
            line(seg(9.8, 15.5, 10.2, 18.5)), line(seg(14.2, 15.5, 13.8, 18.5)),
            shell(rect(9.5, 18.5, 5, 2.5, L(S, 0, 1.25)))]


@T("parachute", "Parachute canopy carrying a crate", ["skydiving", "airdrop", "paragliding", "drop", "descent", "chute"],
   aliases=["chute"])
def _(S):
    canopy = ("M3 11.5A9 8.5 0 0 1 21 11.5"
              "A3 1.75 0 0 0 15 11.5A3 1.75 0 0 0 9 11.5A3 1.75 0 0 0 3 11.5Z")
    return [shell(canopy), line(seg(3.5, 12.5, 10, 18)), line(seg(20.5, 12.5, 14, 18)), line(seg(12, 13, 12, 17.5)),
            shell(rect(10, 17.5, 4, 3.5, min(S.R, 1)))]



# =========================================================================== water

def hull(S, pts, *extra):
    """Hull and superstructure merged into one outline."""
    return union(poly(pts, closed=True, r=S.r * 0.6), *extra)


@T("ship", "Ship with a cabin, a funnel and a mast", ["steamship", "vessel", "boat", "maritime", "sea", "shipping"],
   aliases=["steamship"])
def _(S):
    return [shell(hull(S, [(3.5, 14), (20.5, 12), (18.5, 19.5), (5.5, 19.5)], rect(6, 9, 7.5, 5.5))),
            shell(rect(8, 4, 3, 5, L(S, 0, 1.2))), line(seg(17.5, 12.5, 17.5, 6))]


@T("boat", "Motorboat with a windscreen and a seat", ["motorboat", "speedboat", "dinghy", "boating", "lake", "fishing boat"],
   aliases=["motorboat", "speedboat"])
def _(S):
    return [shell(poly([(3.5, 14), (20.5, 12), (17.5, 18.5), (5.5, 18.5)], closed=True, r=S.r * 0.6)),
            line(poly([(15, 12.8), (13, 8.5), (9.5, 8.5)], r=S.r * 0.5)), line(seg(5.5, 13.7, 5.5, 9.5))]


@T("sailboat", "Sailing boat with a mainsail and a jib", ["sailing", "yacht", "sail", "regatta", "dinghy", "wind"],
   aliases=["sailing-boat"])
def _(S):
    return [shell(poly([(4, 16.5), (20, 16.5), (17.5, 20.5), (6.5, 20.5)], closed=True, r=S.r * 0.6)),
            line(seg(12, 3, 12, 16.5)),
            shell(poly([(10.5, 4), (10.5, 13.5), (4.5, 13.5)], closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
            shell(poly([(13.5, 5.5), (19.5, 13.5), (13.5, 13.5)], closed=True, r=S.r * 0.6), stroke_miterlimit="2")]


@T("ferry", "Ferry with a long passenger deck and a wheelhouse", ["car ferry", "passenger ship", "crossing", "harbour", "boat", "water taxi"],
   aliases=["car-ferry"])
def _(S):
    return [shell(hull(S, [(3.5, 15), (20.5, 15), (19, 19.5), (5, 19.5)], rect(4.5, 9.5, 15, 5.5), rect(9, 5.5, 6, 4))),
            detail(seg(4.5, 15, 19.5, 15)), detail(seg(6.5, 12.25, 17.5, 12.25)), line(seg(12, 5.5, 12, 3))]


@T("yacht", "Motor yacht with a sleek stepped superstructure", ["superyacht", "luxury boat", "cruiser", "marina", "boat", "sea"],
   aliases=["motor-yacht"])
def _(S):
    top = poly([(5, 14), (7, 10.5), (12, 10.5), (13.5, 7.5), (16.5, 7.5), (19.5, 12.5)], closed=True)
    return [shell(hull(S, [(3.5, 14), (20.5, 12), (18.5, 18.5), (5.5, 18.5)], top)),
            detail(seg(8.5, 12.3, 16.5, 12.3)), line(seg(15, 7.5, 15, 3.5))]


@T("container-ship", "Container ship stacked with cargo containers", ["cargo ship", "freighter", "shipping", "logistics", "port", "freight"],
   aliases=["cargo-ship", "freighter"])
def _(S):
    stack = poly([(8.5, 14), (8.5, 10), (10.5, 10), (10.5, 6), (18, 6), (18, 10), (20, 10), (20, 14)], closed=True)
    return [shell(hull(S, [(3.5, 14), (20.5, 14), (19, 19.5), (5, 19.5)], stack, rect(4, 6, 3, 8))),
            detail(seg(3, 14, 21, 14)), detail(seg(10.5, 10, 18, 10)),
            detail(seg(12.5, 10, 12.5, 14)), detail(seg(16, 10, 16, 14)), detail(seg(14.25, 6, 14.25, 10))]


@T("submarine", "Submarine with a conning tower and periscope", ["sub", "u-boat", "underwater", "navy", "deep sea", "periscope"],
   aliases=["sub"])
def _(S):
    body = "M6 14C6 11.8 7.8 10.5 10 10.5H17.5C19.5 10.5 21 12 21 14C21 16 19.5 17.5 17.5 17.5H10C7.8 17.5 6 16.2 6 14Z"
    return [shell(union(body, rect(11, 7, 4.5, 4))), line(poly([(13.5, 7), (13.5, 3.5), (16, 3.5)], r=S.r * 0.5)),
            dot(11, 14, 1), dot(14.5, 14, 1), dot(18, 14, 1),
            line(seg(3.5, 11.5, 3.5, 16.5)), line(seg(3.5, 14, 6, 14))]


@T("jet-ski", "Jet ski with a handlebar and seat", ["personal watercraft", "waverunner", "water scooter", "pwc", "watersports", "beach"],
   aliases=["personal-watercraft", "water-scooter"])
def _(S):
    body = poly([(3.5, 15), (8, 15), (9.5, 12.5), (13, 12.5), (20.5, 16), (18.5, 19.5), (5, 19.5)], closed=True, r=S.r * 0.6)
    return [shell(body), line(poly([(14, 13), (13, 7.5), (16.5, 7.5)], r=S.r * 0.5)),
            line("M3 9.5C3.8 10.5 4.2 11.5 4.3 12.8"), line("M6 7.5C6.8 8.8 7.2 10 7.3 11.2")]


@T("canoe", "Open canoe seen from above with two seats and a single-blade paddle",
   ["canoeing", "paddle", "rowing", "river", "lake", "outdoors"])
def _(S):
    body = "M3 14C6.5 9.2 17.5 9.2 21 14C17.5 18.8 6.5 18.8 3 14Z"
    if S.name == "rounded":
        body = "M3.7 13.2C7.5 9.2 16.5 9.2 20.3 13.2Q21 14 20.3 14.8C16.5 18.8 7.5 18.8 3.7 14.8Q3 14 3.7 13.2Z"
    return [shell(body, stroke_miterlimit="1.5"), detail(seg(8.5, 10.5, 8.5, 17.5)), detail(seg(15.5, 10.5, 15.5, 17.5)),
            line(seg(3.5, 4.5, 14, 4.5)), shell(ellipse(17.5, 4.5, 3.5, 1.5))]


@T("kayak", "Kayak seen from above with a double-bladed paddle", ["kayaking", "paddle", "sea kayak", "watersports", "river", "canoe"])
def _(S):
    body = "M3 12C7 8.5 17 8.5 21 12C17 15.5 7 15.5 3 12Z"
    if S.name == "rounded":
        body = "M3.8 11.3C8 8.3 16 8.3 20.2 11.3Q21 12 20.2 12.7C16 15.7 8 15.7 3.8 12.7Q3 12 3.8 11.3Z"
    b1 = rot(ellipse(5.5, 18.5, 1.5, 3), 45, 5.5, 18.5)
    b2 = rot(ellipse(18.5, 5.5, 1.5, 3), 45, 18.5, 5.5)
    return [shell(body, stroke_miterlimit="1.5"), detail(seg(10, 12, 14, 12)),
            line(seg(7.2, 16.8, 16.8, 7.2)), shell(b1), shell(b2)]


@T("anchor", "Ship's anchor with a ring, stock and curved arms", ["marine", "nautical", "harbour", "port", "moor", "sailor"])
def _(S):
    return [line(circle(12, 5, 2)), line(seg(12, 7, 12, 21)), line(seg(8, 9.5, 16, 9.5)),
            line("M5 14.5C5 18.5 8 21 12 21C16 21 19 18.5 19 14.5"),
            line(poly([(3, 16.5), (5, 14), (7, 16.5)], r=S.r * 0.5)), line(poly([(17, 16.5), (19, 14), (21, 16.5)], r=S.r * 0.5))]


# =========================================================================== vehicle parts

@T("steering-wheel", "Steering wheel with three spokes", ["steering", "drive", "driver", "wheel", "car control", "driving"])
def _(S):
    return [line(circle(12, 12, 8.75)), shell(rect(9, 9.5, 6, 5, S.R * 0.6)),
            line(seg(3.25, 12, 9, 12)), line(seg(15, 12, 20.75, 12)), line(seg(12, 14.5, 12, 20.75))]


@T("fuel", "Fuel pump with a display and a hose", ["petrol", "gas", "gasoline", "diesel", "refuel", "filling station"],
   aliases=["petrol", "gas-pump", "fuel-pump"])
def _(S):
    return [shell(rect(3, 3, 10.5, 18, S.R)), detail(seg(3, 9.5, 13.5, 9.5)),
            line(poly([(13.5, 13), (17.5, 13), (17.5, 18.5), (20.5, 18.5), (20.5, 8.5), (18, 6)], r=S.r))]


@T("tire", "Tyre with tread blocks around a wheel rim", ["tyre", "wheel", "rubber", "puncture", "tire change", "garage"],
   aliases=["tyre"])
def _(S):
    r1 = 9.5 if S.name != "rounded" else 8.6
    treads = [detail(seg(*_polar(12, 12, 6.8, a), *_polar(12, 12, r1, a))) for a in range(0, 360, 45)]
    return [shell(circle(12, 12, 9)), detail(circle(12, 12, 4)), dot(12, 12, 1.25), *treads]


def _polar(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


@T("engine", "Car engine block with a cover, fan and exhaust", ["motor", "engine block", "check engine", "mechanic", "service", "horsepower"],
   aliases=["motor"])
def _(S):
    pts = [(5.5, 18), (5.5, 9.5), (8.5, 9.5), (8.5, 6.5), (15.5, 6.5), (15.5, 9.5), (18, 9.5), (18, 11.5),
           (20.5, 11.5), (20.5, 16), (18, 16), (18, 18)]
    return [shell(poly(pts, closed=True, r=S.r * 0.5)), line(seg(12, 3.5, 12, 6.5)), line(seg(10, 3.5, 14, 3.5)),
            line(seg(3, 10.5, 3, 17)), line(seg(3, 13.75, 5.5, 13.75)), detail(seg(8.5, 13.5, 15, 13.5))]


@T("gear-shift", "Gearbox shift pattern with six positions", ["gearbox", "manual", "transmission", "stick shift", "gears", "clutch"],
   aliases=["gearbox", "stick-shift"])
def _(S):
    def pip(x, y):
        if isF(S):
            return Part("dot", circle(x, y, 2.25))
        if S.name == "line":
            return Part("dot", rect(x - 1.75, y - 1.75, 3.5, 3.5))
        return Part("dot", circle(x, y, 2))
    return [line(seg(6, 4, 6, 20)), line(seg(12, 4, 12, 20)), line(seg(18, 4, 18, 20)), line(seg(6, 12, 18, 12)),
            *[pip(x, y) for x in (6, 12, 18) for y in (4, 20)]]


@T("seatbelt", "Seated person with a seat belt across the chest", ["seat belt", "buckle up", "safety", "passenger", "car safety", "restraint"],
   aliases=["seat-belt"])
def _(S):
    torso = "M4.5 21V18.5C4.5 15 7.5 13 12 13C16.5 13 19.5 15 19.5 18.5V21Z"
    if S.name != "rounded":
        torso = poly([(4.5, 21), (4.5, 17), (8, 13), (16, 13), (19.5, 17), (19.5, 21)], closed=True)
    return [shell(circle(12, 6.5, 3.5)), shell(torso), detail(seg(8, 14, 16, 21))]


@T("traffic-cone", "Striped traffic cone on a square base", ["cone", "roadworks", "construction", "safety", "pylon", "detour"],
   aliases=["road-cone"])
def _(S):
    pts = [(10, 3), (14, 3), (17.5, 17.5), (20.5, 17.5), (20.5, 21), (3.5, 21), (3.5, 17.5), (6.5, 17.5)]
    return [shell(poly(pts, closed=True, r=S.r * 0.6)), detail(seg(9, 8, 15, 8)), detail(seg(7.8, 13, 16.2, 13))]


@T("road-sign", "Triangular warning sign on a post", ["warning sign", "traffic sign", "caution", "hazard", "road", "sign"],
   aliases=["warning-sign"])
def _(S):
    return [shell(poly([(12, 3.5), (20.5, 16), (3.5, 16)], closed=True, r=S.r), stroke_miterlimit="2"),
            detail(seg(12, 8, 12, 11)), dot(12, 13.4, 1.1), line(seg(12, 16, 12, 21))]


# =========================================================================== work vehicles

@veh("tractor", "Farm tractor with a big rear wheel", ["farm", "agriculture", "farming", "field", "harvest", "rural"])
def _(S):
    return [shell(poly([(4, 11), (5, 3.5), (11, 3.5), (12, 11)], closed=True, r=S.r * 0.5)),
            shell(rect(12, 8.5, 8.5, 6, S.R * 0.5)), line(seg(17.5, 8.5, 17.5, 4.5)),
            detail(poly([(6.2, 11), (6.8, 5.8), (9.4, 5.8)], r=S.r * 0.5)),
            wheel(7.5, 16.5, 3.5), wheel(18.5, 19, 2)]


@veh("forklift", "Forklift with a mast and forks", ["fork lift", "warehouse", "pallet", "lift truck", "logistics", "loading"],
     aliases=["lift-truck"])
def _(S):
    pts = [(3, 18), (3, 11), (5.5, 11), (6.5, 4.5), (12.5, 4.5), (12.5, 18)]
    return vbody(S, pts, wheels=(5.5, 11)) + [wheel(5.5), wheel(11),
            line(seg(15, 3, 15, 20)), line(seg(15, 20, 21, 20)), detail(seg(7.5, 11, 12.5, 11))]


@T("crane", "Tower crane with a jib and a hook", ["construction", "tower crane", "building site", "lifting", "hoist", "industry"],
   aliases=["tower-crane"])
def _(S):
    return [line(seg(5.5, 6.5, 5.5, 21)), line(seg(10.5, 6.5, 10.5, 21)),
            line(poly([(5.5, 10), (10.5, 14), (5.5, 18)], r=0)),
            line(seg(3, 6.5, 21, 6.5)), line(poly([(3.5, 6.5), (8, 3.5), (19, 6.5)], r=S.r * 0.5)),
            line(seg(17.5, 6.5, 17.5, 12)), line("M17.5 12V14.2A1.6 1.6 0 0 1 14.3 14.2"),
            line(seg(3.5, 21, 12.5, 21))]


@T("excavator", "Tracked excavator with a boom and bucket", ["digger", "backhoe", "construction", "earthmover", "building site", "dig"],
   aliases=["digger"])
def _(S):
    tracks = rect(3, 16, 12.5, 5, 2.5 if S.name == "rounded" else 1.5)
    cab = poly([(3.5, 14.5), (3.5, 9), (6, 6.5), (10, 6.5), (10, 10), (13, 10), (13, 14.5)], closed=True, r=S.r * 0.5)
    bucket = poly([(18, 10), (21, 10), (21, 14.5), (17.5, 13.5)], closed=True, r=S.r * 0.5)
    return [shell(tracks), dot(6.25, 18.5, 1), dot(9.25, 18.5, 1), dot(12.25, 18.5, 1), shell(cab),
            line(poly([(12, 11), (16, 4.5), (19.5, 10)], r=S.r * 0.5)), shell(bucket)]


@T("horse-carriage", "Horse pulling a small carriage",
   ["carriage", "stagecoach", "horse-drawn", "coach", "buggy", "cart"], aliases=["stagecoach", "horse-drawn-carriage"])
def _(S):
    horse = poly([(14.5, 14.5), (14.5, 10.5), (18, 10.5), (19, 5.5), (21, 7.5), (21, 9.5), (20.5, 9.5), (20.5, 14.5)],
                 closed=True, r=S.r * 0.5)
    return [shell(poly([(3, 5), (11, 5), (11, 12.5), (9.5, 14), (4, 14), (3, 12.5)], closed=True, r=S.r)),
            detail(seg(5, 8.5, 8.5, 8.5)),
            line(circle(6.75, 18, 3)), dot(6.75, 18, 1),
            line(seg(11, 11.5, 14.5, 11.5)), shell(horse),
            line(seg(15.5, 14.5, 15.5, 21)), line(seg(19.5, 14.5, 19.5, 21))]
