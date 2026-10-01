"""TypeIcon Core: rail, air and sea craft (batch craft_001).

Visual language:
  * Side-view rolling stock faces right. Bodies sit on y 15 or above, and bogie wheels are solid r 1.6 discs on
    the y 18.6 line in pairs, so rail vehicles read differently from buses and trucks (two ring wheels).
  * Side-view aircraft face right (nose on the right, tail on the left); top-view aircraft point up.
  * Line uses small corner radii and sharp joins; Rounded softens every corner (`L(S, line, rounded)`).
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    rect, regular, seg, shell, solid,
)
from geometry import I, rotation, transform_path

CAT = "craft"
FILL = Style("filled", "butt", "miter", R=2.0, r=0.0)  # Line geometry for Filled designs


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Value for Line/Filled (a) or Rounded (b)."""
    return b if S.name == "rounded" else a


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def rpt(p, deg, c=(12.0, 12.0)):
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a)


def rot(d, deg, cx=12.0, cy=12.0):
    """Rotate a closed shape's d-string."""
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle (window): solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def filled_from(fn):
    return lambda: filled_region(fn(FILL))


def C(name, description, tags, aliases=()):
    """Register a craft icon whose Filled design is derived from the Line geometry."""
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=filled_from(fn))(fn)
    return deco


# --------------------------------------------------------------------------- rail grammar

WY = 18.6


def bogies(xs=(5.5, 9, 15, 18.5), y=WY, r=1.6):
    return [dot(x, y, r) for x in xs]


def windows(S, xs, y, w=2.5, h=2.5):
    k = L(S, 0, 0.8)
    return [sq(x, y, w, h, k) for x in xs]


# =========================================================================== locomotives

@C("steam-locomotive", "Steam locomotive with a tall smokestack, boiler, cab and big driving wheels",
   ["steam train", "locomotive", "steam engine", "railway", "puffer", "heritage railway"])
def _(S):
    body = union(rect(3, 4, 6, 10), rect(8, 8, 13, 6), poly([(15, 3.5), (19, 3.5), (18.2, 8), (15.8, 8)], closed=True))
    return [shell(body), detail(seg(3, 8, 9, 8)),
            shell(circle(7.5, 18.5, 2.5)), shell(circle(15, 18.5, 2.5)), dot(20.3, 19, 1.2),
            line(seg(10.5, 18.5, 12, 18.5))]


@C("diesel-locomotive", "Diesel locomotive with a flat-nosed cab and a long engine hood with vents",
   ["diesel train", "locomotive", "diesel engine", "freight", "railway", "hood unit"])
def _(S):
    k = L(S, 0.5, 1.5)
    body = union(rect(3, 8, 12, 7, k), rect(14, 4, 7, 11, k))
    return [shell(body), detail(seg(14, 8.5, 21, 8.5)),
            detail(seg(6.5, 8, 6.5, 12)), detail(seg(9.5, 8, 9.5, 12)),
            *bogies()]


@C("electric-locomotive", "Electric locomotive with a diamond pantograph touching the overhead wire",
   ["electric train", "locomotive", "pantograph", "overhead line", "catenary", "railway"])
def _(S):
    k = L(S, 1, 2.5)
    return [line(seg(3, 3, 21, 3)),
            line(poly([(12, 9), (8.5, 6), (12, 3), (15.5, 6)], closed=True, r=S.r * 0.4)),
            shell(rect(3, 9, 18, 6, k)), *windows(S, (5.5, 16), 11), *bogies()]


@C("shunting-locomotive", "Small shunting locomotive with a tall cab, a low hood and a coupler",
   ["switcher", "shunter", "yard engine", "locomotive", "rail yard", "switch engine"])
def _(S):
    k = L(S, 0.5, 1.5)
    body = union(rect(3, 4, 7, 11, k), rect(9, 9.5, 10, 5.5, k))
    return [shell(body), detail(seg(3, 8.5, 10, 8.5)),
            line(poly([(19, 12.5), (21.5, 12.5), (21.5, 10.5)], r=S.r * 0.4)),
            *bogies((6, 10, 16))]


@C("streamlined-locomotive", "Streamlined steam locomotive with a smooth bullet casing and a skirt over the wheels",
   ["art deco train", "streamliner", "locomotive", "steam", "vintage train", "express"])
def _(S):
    body = ("M3 16.5V7.5H12.5C17.5 7.5 21 10.5 21 14.5V16.5Z" if S.name != "rounded" else
            "M4.5 16.5Q3 16.5 3 15V9Q3 7.5 4.5 7.5H12.5C17.5 7.5 21 10.5 21 14.5Q21 16.5 19.5 16.5Z")
    return [shell(body), detail(seg(3, 13, 19, 13)), detail(seg(8.5, 7.5, 8.5, 13)),
            dot(6, 19.8, 1.4), dot(10.5, 19.8, 1.4), dot(15, 19.8, 1.4)]


@C("maglev-train", "Maglev train nose hovering above a T-shaped guideway",
   ["maglev", "magnetic levitation", "high speed train", "bullet train", "levitating train", "guideway"])
def _(S):
    body = ("M3 13V6.5H11C16.5 6.5 21 9.5 21 13Z" if S.name != "rounded" else
            "M4.5 13Q3 13 3 11.5V8Q3 6.5 4.5 6.5H11C16.5 6.5 21 9.5 21 11.5Q21 13 19.5 13Z")
    guide = union(rect(3, 16, 18, 2.5, L(S, 0.01, 1)), rect(10.5, 17, 3, 5))
    return [shell(body), detail(seg(8, 6.5, 8, 10)), detail(seg(3, 10, 14.5, 10)), shell(guide)]


@C("vacuum-tube-train", "Passenger pod speeding through a raised tube on pillars",
   ["hyperloop", "tube train", "vactrain", "pod", "future transport", "high speed"])
def _(S):
    pod = (poly([(9, 9), (17, 9), (20, 11), (17, 13), (9, 13)], closed=True) if S.name != "rounded" else
           rect(9, 9, 11, 4, 2))
    return [line(seg(2, 6, 22, 6)), line(seg(2, 16, 22, 16)), shell(pod),
            line(seg(3.5, 9.5, 6.5, 9.5)), line(seg(3.5, 12.5, 6.5, 12.5)),
            line(seg(6, 16, 6, 21)), line(seg(18, 16, 18, 21))]


# =========================================================================== carriages

@C("double-decker-train", "Tall passenger rail carriage with two rows of windows",
   ["bilevel", "double deck", "double decker", "commuter train", "rail carriage", "coach"],
   aliases=["bilevel-car"])
def _(S):
    return [shell(rect(3, 3, 18, 12, L(S, 1, 2.5))),
            *windows(S, (5.5, 9.5, 13.5, 16.5), 5.25, w=2), *windows(S, (5.5, 9.5, 13.5, 16.5), 10.25, w=2),
            *bogies()]


@C("passenger-railcar", "Passenger rail carriage with a row of windows",
   ["rail carriage", "coach", "railcar", "passenger car", "train car", "wagon"])
def _(S):
    body = ("M3 15V8.5Q3 6.5 5 6L12 5L19 6Q21 6.5 21 8.5V15Z" if S.name != "rounded" else
            "M5 15Q3 15 3 13V8.5Q3 6.5 5 6L12 5L19 6Q21 6.5 21 8.5V13Q21 15 19 15Z")
    return [shell(body), *windows(S, (5.5, 9.5, 13, 16.5), 8.5, w=2), *bogies()]


@C("observation-car", "Rail carriage with a glass dome on its roof",
   ["dome car", "vista dome", "scenic train", "panorama car", "rail carriage", "sightseeing"])
def _(S):
    dome = "M7 9.5C8 5.5 9.5 4.5 12 4.5H16C17.5 4.5 18 7 18 9.5Z"
    return [shell(union(rect(3, 9.5, 18, 5.5, L(S, 0.01, 2)), dome)),
            detail(seg(11.5, 4.5, 11.5, 9.5)), detail(seg(15, 4.5, 15, 9.5)),
            *windows(S, (5, 18.5), 11.5, w=1.5, h=2), *bogies()]


@C("sleeper-car", "Rail carriage with a crescent moon above its roof",
   ["sleeping car", "night train", "sleeper train", "couchette", "overnight", "berth"])
def _(S):
    moon = "M17.5 2.5A3 3 0 1 0 21 6.5A2.5 2.5 0 0 1 17.5 2.5Z"
    return [solid(moon), shell(rect(3, 9, 18, 6, L(S, 1, 2.5))),
            *windows(S, (5.5, 10.75, 16), 11, w=2.5, h=2), *bogies()]


@C("dining-car", "Rail carriage marked with a plate, fork and knife",
   ["restaurant car", "buffet car", "dining carriage", "train food", "catering", "meal"])
def _(S):
    return [shell(rect(3, 4.5, 18, 10.5, L(S, 1, 2.5))),
            detail(circle(12, 9.75, 2.25)), detail(seg(7.5, 7, 7.5, 12.5)), detail(seg(16.5, 7, 16.5, 12.5)),
            *bogies()]


# =========================================================================== freight

@C("flatcar", "Flat rail wagon with a long deck and upright stakes",
   ["flat wagon", "flatbed wagon", "freight car", "rail wagon", "lumber car", "goods wagon"],
   aliases=["flat-wagon"])
def _(S):
    return [shell(rect(2.5, 13, 19, 2, L(S, 0.01, 1))),
            line(seg(4, 13, 4, 8)), line(seg(9.33, 13, 9.33, 8)), line(seg(14.67, 13, 14.67, 8)), line(seg(20, 13, 20, 8)),
            *bogies()]


@C("container-wagon", "Low rail wagon carrying a ribbed shipping container",
   ["container car", "intermodal", "freight car", "shipping container", "rail freight", "well car"])
def _(S):
    k = L(S, 0.5, 1.5)
    return [shell(rect(3.5, 5, 17, 7.5, k)), detail(seg(8, 5, 8, 12.5)), detail(seg(12, 5, 12, 12.5)),
            detail(seg(16, 5, 16, 12.5)), line(seg(2.5, 14.5, 21.5, 14.5)), *bogies()]


@C("caboose", "Rail van with a cupola lookout on its roof and railed end platforms",
   ["brake van", "guard's van", "cabin car", "cupola", "freight train", "railroad"],
   aliases=["brake-van"])
def _(S):
    k = L(S, 0.5, 1.5)
    body = union(rect(6, 8.5, 12, 6.5, k), rect(9.5, 4, 5, 5, k))
    return [shell(body), dot(12, 6.5, 1), sq(8.5, 10.75, 2, 2), sq(13.5, 10.75, 2, 2),
            line(seg(2.5, 15.5, 21.5, 15.5)), line(seg(3.5, 10, 3.5, 15.5)), line(seg(20.5, 10, 20.5, 15.5)),
            *bogies()]


@C("car-carrier-wagon", "Two-level rail wagon carrying cars on each deck",
   ["autorack", "car transporter", "auto carrier", "vehicle wagon", "motorail", "freight car"],
   aliases=["autorack"])
def _(S):
    def car_(x, y):
        pts = [(x, y + 2.5), (x, y + 1.2), (x + 1.3, y + 1), (x + 2.1, y), (x + 3.9, y), (x + 4.7, y + 1),
               (x + 6, y + 1.2), (x + 6, y + 2.5)]
        return Part("dot", poly(pts, closed=True, r=S.r * 0.2))
    return [shell(rect(3, 3, 18, 12, L(S, 0.5, 2))), detail(seg(3, 9, 21, 9)),
            car_(5, 4.75), car_(13, 4.75), car_(5, 10.75), car_(13, 10.75), *bogies()]


@C("handcar", "Rail handcar with a seesaw pump handle on a central post",
   ["pump trolley", "draisine", "jigger", "hand trolley", "railway", "velocipede"],
   aliases=["pump-trolley"])
def _(S):
    return [line(seg(4.5, 5, 19.5, 11)), line(seg(12, 8, 12, 13)), dot(12, 8, 1.6),
            shell(rect(3.5, 13, 17, 2.5, L(S, 0.01, 1.25))), dot(7, 18.4, 1.75), dot(17, 18.4, 1.75),
            line(seg(2, 21, 22, 21))]


@C("suspended-monorail", "Monorail carriage hanging below a single overhead beam",
   ["hanging monorail", "suspension railway", "sky train", "elevated railway", "people mover"])
def _(S):
    k = L(S, 1, 2.5)
    return [shell(rect(2.5, 3, 19, 2.5, L(S, 0.01, 1.25))), line(seg(4, 5.5, 4, 21)), line(seg(2, 21, 6, 21)),
            line(seg(14, 5.5, 14, 9)), shell(rect(7.5, 9, 13.5, 8, k)), *windows(S, (10, 13, 16.5), 11.5, w=2, h=2.5)]


@C("cable-tram", "Open-sided cable tram climbing a steep street",
   ["cable car", "streetcar", "heritage tram", "hill tram", "grip car", "trolley"])
def _(S):
    deg = -13

    def R_(pts):
        return [rpt(p, deg) for p in pts]
    roof = poly(R_([(4, 5.5), (20, 5.5), (20, 7.5), (4, 7.5)]), closed=True, r=S.r * 0.4)
    base = poly(R_([(4, 12), (20, 12), (20, 15), (4, 15)]), closed=True, r=S.r * 0.6)
    posts = [line(seg(*rpt((x, 7.5), deg), *rpt((x, 12), deg))) for x in (5, 12, 19)]
    wheels = [dot(*rpt((x, 17.6), deg), 1.6) for x in (7.5, 16.5)]
    c = rpt((12, 19.5), deg)
    y = lambda x: c[1] + (x - c[0]) * math.tan(math.radians(deg))
    return [shell(roof), *posts, shell(base), *wheels, line(seg(3, y(3), 21, y(21)))]


@C("railway-snowplow", "Rail vehicle with a rotary snow blower throwing an arc of snow",
   ["rotary snowplow", "snow blower", "rail snow plough", "winter railway", "snow clearing", "snowplough"],
   aliases=["rotary-snowplow"])
def _(S):
    vanes = [detail(f"M{fmt(16.5)} {fmt(11.5)}Q{fmt(rpt((19.5, 10), a, (16.5, 11.5))[0])} "
                    f"{fmt(rpt((19.5, 10), a, (16.5, 11.5))[1])} {fmt(rpt((20, 12.5), a, (16.5, 11.5))[0])} "
                    f"{fmt(rpt((20, 12.5), a, (16.5, 11.5))[1])}") for a in (0, 120, 240)]
    return [shell(rect(3, 8, 8, 7, L(S, 1, 2.5))), shell(circle(16.5, 11.5, 4.5)), *vanes,
            line("M15 5C13.5 3 11 2.5 8.5 3"), dot(5.5, 4, 1.1), dot(3.5, 6, 1.1),
            dot(5, WY, 1.6), dot(9, WY, 1.6), dot(14, WY, 1.6), dot(18, WY, 1.6)]


@C("rail-crane", "Rail wagon with a crane jib and a hanging hook",
   ["railway crane", "breakdown crane", "crane wagon", "maintenance", "lifting", "track work"])
def _(S):
    k = L(S, 0.5, 1.5)
    base = union(rect(2.5, 13, 19, 2, 0.01), rect(4, 8.5, 6.5, 4.5))
    return [shell(base), line(seg(9.5, 9.5, 19, 4)), line(seg(19, 4, 19, 9)),
            line("M19 9V10.3A1.4 1.4 0 0 1 16.2 10.3"), *bogies()]


@C("train-wheel", "Railway wheel with a flanged rim sitting on a rail",
   ["rail wheel", "wheelset", "flanged wheel", "bogie", "railway", "axle"])
def _(S):
    spokes = [detail(seg(*rpt((12, 8.5), a, (12, 11)), *rpt((12, 5), a, (12, 11)))) for a in range(0, 360, 60)]
    return [shell(circle(12, 11, 8)), dot(12, 11, 2), *spokes, line(seg(2.5, 21, 21.5, 21))]


@C("cowcatcher", "Front of an old steam locomotive with a slatted cowcatcher below the smokebox",
   ["pilot", "cattle guard", "steam locomotive", "wild west train", "old train", "railroad"],
   aliases=["train-pilot"])
def _(S):
    top = union(rect(10, 2, 4, 3.5, L(S, 0.01, 1)), circle(12, 9, 4.5), rect(3, 12.5, 18, 2.5, L(S, 0.01, 1.25)))
    grille = poly([(3.5, 15.5), (20.5, 15.5), (16, 21.5), (8, 21.5)], closed=True, r=L(S, 0, 1))
    return [shell(top), dot(12, 9, 1.5), shell(grille),
            detail(seg(10, 15.5, 11, 21.5)), detail(seg(14, 15.5, 13, 21.5))]


@C("water-crane", "Railway water column with a swinging arm and a drooping hose",
   ["water column", "water tower", "steam era", "railway", "locomotive watering", "standpipe"],
   aliases=["water-column"])
def _(S):
    k = L(S, 0.01, 1.5)
    return [shell(union(rect(5, 5, 3, 14.5, k), rect(3.5, 18, 6, 3, k))),
            line(seg(8, 5, 17, 5)), line("M17 5C19 5 19.5 6.5 19.5 8.5V13"), line(seg(13, 21, 22, 21))]


@C("railway-lantern", "Handheld railway guard lamp with a wire handle and a round lens",
   ["guard lamp", "signal lamp", "railroad lantern", "brakeman lantern", "hand lamp", "railway signal"],
   aliases=["guard-lamp"])
def _(S):
    k = L(S, 0.5, 2)
    body = union(rect(4, 10, 11, 9, k), poly([(5.5, 10.5), (13.5, 10.5), (12, 7), (7, 7)], closed=True),
                 rect(3, 18, 13, 3, L(S, 0.01, 1.2)))
    return [shell(body), detail(circle(9.5, 14, 2.25)), line("M7 7.5C7 1.5 12 1.5 12 7.5"),
            line(seg(18, 14, 21.5, 14)), line(seg(17.5, 10, 20.5, 8)), line(seg(17.5, 18, 20.5, 20))]


# =========================================================================== aircraft, side and front views

def airliner(top=9.5, bot=13.5, fin_top=4, hump=False, nose=21.5):
    """Side-view airliner fuselage with its tail fin, nose on the right."""
    mid = (top + bot) / 2 + 0.5
    if hump:
        crown = f"H11C12 {top - 1.5} 13.5 {top - 2.5} 15.5 {top - 2.5}C18.5 {top - 2.5} {nose} {top} {nose} {mid}"
    else:
        crown = f"H{nose - 4}C{nose - 1.5} {top} {nose} {top + 1.2} {nose} {mid}"
    return (f"M3 {bot - 3}L2.5 {fin_top}H4.5L8.5 {top}{crown}"
            f"C{nose} {bot - 0.5} {nose - 0.8} {bot} {nose - 2} {bot}H7Z")


def swept_wing(x=10.5, y=12, w=4.5, drop=5, back=2.5):
    return poly([(x, y), (x + w, y), (x + w - back - 1, y + drop), (x - back, y + drop)], closed=True)


@C("jumbo-jet", "Wide-body airliner with a raised hump over the front upper deck",
   ["jumbo", "wide body", "airliner", "long haul", "passenger jet", "double deck plane"],
   aliases=["wide-body-jet"])
def _(S):
    body = ("M3.5 13.5L2.5 5.5H4.5L8.5 11H13C14 9.3 15.5 8.5 17.5 8.5C20 8.5 21.5 11 21.5 13"
            "C21.5 14.3 20.8 15 19.5 15H6.5Z")
    wing = poly([(10, 14), (14, 14), (10, 19), (7.5, 19)], closed=True, r=L(S, 0, 0.8))
    return [shell(union(body, wing)), detail(seg(15.5, 11, 19, 11))]


@C("private-jet", "Small business jet with engines on the rear fuselage and a T-shaped tail",
   ["business jet", "bizjet", "corporate jet", "executive jet", "charter", "luxury travel"],
   aliases=["business-jet"])
def _(S):
    body = "M4.5 13.5L3.5 5.5H5L9 10.5H17C19.5 10.5 21 11.5 21 12.5C21 13.3 20.3 14 19 14H7Z"
    return [shell(union(body, swept_wing(12, 13, 3.5, 4, 2))),
            line(seg(2, 5, 7, 5)), shell(rect(6.5, 7, 5, 2.5, L(S, 0.5, 1.25))),
            dot(15.5, 12.25, 0.9), dot(18, 12.25, 0.9)]


@C("supersonic-airliner", "Slender supersonic airliner with a drooped needle nose and delta wings on tall landing gear",
   ["supersonic", "sst", "delta wing", "mach 2", "fast airliner", "droop nose"],
   aliases=["sst"])
def _(S):
    body = "M3 12L3 5.5H4.5L9.5 10H17L21.5 13L17 12Z"
    delta = poly([(7, 12), (16, 12), (5.5, 14)], closed=True)
    return [shell(union(body, delta), stroke_miterlimit="2"),
            line(seg(9, 13.5, 9, 18)), line(seg(16, 12, 16, 18)), dot(9, 19.5, 1.5), dot(16, 19.5, 1.5)]


@C("radar-aircraft", "Airliner-shaped plane carrying a disc radar dome on struts",
   ["awacs", "early warning", "radar plane", "surveillance aircraft", "rotodome", "military"],
   aliases=["awacs"])
def _(S):
    return [shell(union(airliner(top=11, bot=15, fin_top=6), swept_wing(10.5, 13.5, 4.5, 4.5))),
            shell(ellipse(13.5, 4.5, 5, 1.5)), line(seg(12, 6, 12, 11)), line(seg(15, 6, 15, 11))]


@C("cargo-plane", "Bulky transport plane with a T-tail and a lowered rear loading ramp",
   ["cargo aircraft", "freighter", "airlift", "military transport", "air freight", "loading ramp"],
   aliases=["transport-plane"])
def _(S):
    body = "M9.5 14H18.5C20.5 14 21.5 12.5 21.5 11C21.5 9.5 20.5 7.5 18 7.5H10.5L6.5 3.5H4.5L6 11.5Z"
    wing = poly([(12, 13), (16, 13), (12, 17.5), (9.5, 17.5)], closed=True, r=L(S, 0, 0.8))
    return [shell(union(body, wing)), line(seg(2.5, 3.5, 8.5, 3.5)),
            line(seg(8.5, 13.5, 4, 20)), line(seg(2, 21, 22, 21)), dot(19, 18.5, 1.5)]


@C("turboprop-plane", "Regional plane seen from above with straight wings and a propeller on each engine",
   ["turboprop", "regional plane", "propeller plane", "commuter plane", "prop plane", "twin engine"],
   aliases=["prop-plane"])
def _(S):
    fus = ("M10 20V6C10 3.5 10.8 2.5 12 2.5S14 3.5 14 6V20Z" if S.name != "rounded" else
           "M10 19V6C10 3.5 10.8 2.5 12 2.5S14 3.5 14 6V19Q14 20.5 12 20.5T10 19Z")
    return [shell(fus), line(seg(2, 11, 10, 11)), line(seg(14, 11, 22, 11)),
            solid(rect(5.5, 7, 3, 5, L(S, 0, 1))), solid(rect(15.5, 7, 3, 5, L(S, 0, 1))),
            line(seg(4.5, 5, 9, 5)), line(seg(15, 5, 19.5, 5)),
            line(seg(7, 19.5, 10, 19.5)), line(seg(14, 19.5, 17, 19.5))]


@C("light-aircraft", "Small single-engine high-wing plane with a nose propeller and fixed wheels",
   ["light plane", "small plane", "general aviation", "flying lessons", "private pilot", "single engine"],
   aliases=["light-plane"])
def _(S):
    body = "M3 13L2.5 7H4L7.5 11H11L12.5 8.5H18Q19.5 8.5 19.5 10.5V13Q19.5 14.5 18 14.5H6.5Z"
    return [shell(union(body, rect(10, 7, 9, 1.5))), line(seg(21.5, 8.5, 21.5, 16.5)),
            line(seg(15.5, 14.5, 15.5, 17.5)), dot(15.5, 19.2, 1.75), line(seg(4.5, 14, 4.5, 17.5)), dot(4.5, 19, 1.25)]


def _front_plane(S, wings, gear_top):
    k = L(S, 0.01, 1)
    parts = [shell(rect(2, y - 1, 20, 2, k)) for y in wings]
    parts += [line(seg(5, wings[0], 5, wings[-1])), line(seg(19, wings[0], 19, wings[-1]))]
    return parts


@C("biplane", "Vintage biplane seen from the front with two stacked wings, struts and a propeller",
   ["vintage plane", "barnstormer", "crop duster", "stunt plane", "old plane", "two wings"])
def _(S):
    return [*_front_plane(S, (5.5, 13), 13), shell(circle(12, 9.25, 2.75)), dot(12, 9.25, 1),
            line(seg(10, 14, 7.5, 18)), line(seg(14, 14, 16.5, 18)), dot(7, 19.5, 1.6), dot(17, 19.5, 1.6)]


@C("triplane", "Vintage triplane seen from the front with three stacked wings and struts",
   ["three wings", "stacked wings", "ww1 plane", "vintage plane", "fighter", "old aircraft"])
def _(S):
    return [*_front_plane(S, (4, 9.5, 15), 15), shell(circle(12, 12.25, 2)),
            line(seg(10.5, 16, 8, 19)), line(seg(13.5, 16, 16, 19)), dot(7.5, 20.2, 1.5), dot(16.5, 20.2, 1.5)]


@C("seaplane", "Small propeller plane on two pontoon floats above the water",
   ["floatplane", "float plane", "water plane", "pontoon plane", "bush plane", "lake"],
   aliases=["floatplane"])
def _(S):
    body = "M3.5 10.5L2.5 3.5H4.5L7.5 7H17Q19.5 7 19.5 9Q19.5 11 17 11H7Z"
    return [shell(union(body, rect(9.5, 5, 9, 2))), line(seg(21.5, 5, 21.5, 13)),
            line(seg(10, 11, 10, 14.5)), line(seg(16, 11, 16, 14.5)),
            shell(rect(6, 14.5, 14, 2, L(S, 0.01, 1))),
            line("M2 20.5C3.5 19.5 5 19.5 6.5 20.5S9.5 21.5 11 20.5S14 19.5 15.5 20.5S18.5 21.5 20 20.5")]


@C("flying-boat", "Flying boat resting on the water on its boat-shaped hull, with a high wing on struts",
   ["seaplane", "amphibian", "water landing", "boat plane", "patrol plane", "sea plane"],
   aliases=["amphibious-plane"])
def _(S):
    hull = "M3.5 12.5L2.5 6H4.5L8 10.5H17C19.5 10.5 21.5 12 21.5 13.5L19 17H9.5Z"
    return [shell(hull), line(seg(7.5, 3, 21, 3)), shell(rect(12, 3, 6, 3, L(S, 0.01, 1.5))),
            line(seg(15, 6, 15, 10.5)),
            line("M2 21C3.5 20 5 20 6.5 21S9.5 22 11 21S14 20 15.5 21S18.5 22 20 21")]


@C("glider-plane", "Sailplane seen from above with very long thin wings, a bubble canopy and no engine",
   ["glider", "sailplane", "gliding", "soaring", "unpowered flight", "motorless plane"],
   aliases=["sailplane"])
def _(S):
    return [shell(ellipse(12, 6, 2, 3.5) if S.name == "rounded" else poly([(12, 2.5), (14, 5.5), (13, 9.5), (11, 9.5), (10, 5.5)], closed=True)),
            line(seg(12, 9.5, 12, 21)), line(seg(2, 11.5, 22, 11.5)), line(seg(8.5, 20, 15.5, 20))]


@C("hang-glider", "Delta hang glider wing with a pilot hanging in the triangular control bar",
   ["hang gliding", "delta wing", "free flight", "soaring", "adventure sport", "kite"],
   aliases=["hang-gliding-wing"])
def _(S):
    return [shell(poly([(2, 11.5), (12, 3.5), (22, 11.5), (12, 9)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
            line(poly([(12, 9.5), (7, 19), (17, 19)], closed=True, r=S.r * 0.5)), dot(12, 15, 1.75)]


@C("paraglider", "Curved paraglider canopy with lines running down to a seated pilot",
   ["paragliding", "parapente", "canopy", "free flight", "adventure sport", "soaring"],
   aliases=["parapente"])
def _(S):
    canopy = "M2.5 9C5 5 8.5 3 12 3S19 5 21.5 9L19 10.5C17 8.5 14.5 7.5 12 7.5S7 8.5 5 10.5Z"
    return [shell(canopy), line(seg(5.5, 10.5, 11, 17)), line(seg(18.5, 10.5, 13, 17)), line(seg(12, 8, 12, 15)),
            dot(12, 18.8, 2)]


@C("paramotor", "Paraglider pilot wearing a caged propeller on the back under a curved wing",
   ["powered paraglider", "ppg", "paramotoring", "motor paraglider", "backpack motor", "powered paragliding"],
   aliases=["powered-paraglider"])
def _(S):
    canopy = "M3 7C5.5 4 8.5 2.5 12 2.5S18.5 4 21 7L19 8.5C17 6.8 14.5 6 12 6S7 6.8 5 8.5Z"
    return [shell(canopy), line(seg(5.5, 8.5, 9.5, 12.5)), line(seg(18.5, 8.5, 12.5, 12.5)),
            dot(9, 14, 1.5), line(seg(9, 15.5, 9, 20)), shell(circle(15.5, 16.5, 4.5)),
            detail(seg(15.5, 13, 15.5, 20))]


# =========================================================================== aircraft, top views

@C("fighter-jet", "Jet fighter seen from above with swept delta wings, twin tail fins and a pointed nose",
   ["fighter", "military jet", "combat aircraft", "air force", "warplane", "jet"],
   aliases=["fighter-plane", "warplane"])
def _(S):
    rh = [(13, 5.5), (13.5, 9), (21, 15.5), (21, 17), (14, 16), (14, 19), (16.5, 21), (13, 21)]
    pts = [(12, 2)] + rh + [(24 - x, y) for x, y in reversed(rh)]
    return [shell(poly(pts, closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
            detail(seg(10.5, 12.5, 10.5, 16.5)), detail(seg(13.5, 12.5, 13.5, 16.5))]


@C("flying-wing", "Tailless flying wing seen from above with a sawtooth trailing edge",
   ["stealth bomber", "tailless aircraft", "flying wing", "blended wing", "military aircraft", "boomerang wing"],
   aliases=["stealth-bomber"])
def _(S):
    pts = [(12, 6), (22, 15), (20.5, 17), (17, 15), (14.5, 17.5), (12, 15.5), (9.5, 17.5), (7, 15), (3.5, 17), (2, 15)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 1.2)), stroke_miterlimit="2"), dot(12, 10.5, 1.1)]


# =========================================================================== aircraft, special

@C("jump-jet", "Jet fighter hovering in place with two nozzles blasting air straight down",
   ["hovering jet", "vtol", "vertical takeoff", "hover", "stovl", "jump jet"],
   aliases=["vtol-jet"])
def _(S):
    body = "M3 11L2.5 4.5H4L7.5 9H13L15 7.5H17L21.5 10.5L17 12.5H4Z"
    return [shell(body, stroke_miterlimit="2"), line(seg(8.5, 13.5, 8.5, 21)), line(seg(13, 13.5, 13, 21)),
            line(seg(5.5, 17, 5.5, 21)), line(seg(16, 17, 16, 21))]


@C("firefighting-aircraft", "Propeller plane dropping a curtain of water onto flames below",
   ["water bomber", "air tanker", "firefighting plane", "wildfire", "forest fire", "aerial firefighting"],
   aliases=["water-bomber"])
def _(S):
    body = "M3 7.5L2.5 2.5H4L7 5.5H17.5C19.5 5.5 20.5 6.5 20.5 7.5C20.5 8.5 19.5 9 18.5 9H6Z"
    flame = ("M12 21.5C8.8 21.5 7.5 19.5 8.5 17.2C9.2 18.3 10.2 18.5 10.4 17.3C10.6 15.8 11.4 15 12.6 14.5"
             "C12.5 16.2 15.5 17 15.5 19C15.5 20.6 14 21.5 12 21.5Z")
    return [shell(body), line(seg(21.8, 5, 21.8, 10)),
            line(seg(8.5, 10.5, 8.5, 12.5)), line(seg(11.5, 10.5, 11.5, 12.5)), line(seg(14.5, 10.5, 14.5, 12.5)),
            shell(flame)]


@C("tiltrotor", "Tiltrotor aircraft seen from the front with a big rotor on top of each wingtip engine",
   ["tilt rotor", "tilt wing", "vtol", "convertiplane", "military aircraft", "rotorcraft"],
   aliases=["convertiplane"])
def _(S):
    k = L(S, 0.5, 1.5)
    return [shell(rect(9.5, 10, 5, 8, L(S, 1, 2.5))), line(seg(9.5, 13, 7.5, 13)), line(seg(14.5, 13, 16.5, 13)),
            shell(rect(4.5, 9.5, 3, 7, k)), shell(rect(16.5, 9.5, 3, 7, k)),
            line(seg(6, 9.5, 6, 6)), line(seg(18, 9.5, 18, 6)), line(seg(2, 5, 10, 5)), line(seg(14, 5, 22, 5))]


@C("autogyro", "Small open gyroplane with a free-spinning rotor on a mast and a pusher propeller",
   ["gyroplane", "gyrocopter", "rotorcraft", "autogiro", "light aircraft", "rotor"],
   aliases=["gyrocopter", "gyroplane"])
def _(S):
    pod = "M8 13C8 11 10 10 12.5 10H15C17.5 10 18.5 12 18.5 13.5C18.5 15 17.5 16 15.5 16H10C8.8 16 8 14.8 8 13Z"
    return [line(seg(3, 5, 21, 5)), line(seg(12, 5, 12, 10)), shell(pod), line(seg(5.5, 9.5, 5.5, 17)),
            line(seg(8, 13, 5.5, 13)), line(seg(11, 16, 10, 18)), line(seg(16, 16, 17, 18)),
            dot(9.5, 19.5, 1.5), dot(17.5, 19.5, 1.5)]


@C("airship", "Cigar-shaped airship with tail fins and a gondola under its belly",
   ["blimp", "zeppelin", "dirigible", "balloon", "lighter than air", "advertising"],
   aliases=["blimp", "dirigible"])
def _(S):
    env = ellipse(13, 10, 8.5, 4.5)
    fins = [poly([(2.5, 4.5), (5, 4.5), (8.5, 8), (5, 9)], closed=True), poly([(2.5, 15.5), (5, 15.5), (8.5, 12), (5, 11)], closed=True)]
    return [shell(union(env, *fins)), detail(seg(9, 10, 19, 10)), shell(rect(11, 16.5, 5, 3, L(S, 0.5, 1.5))),
            line(seg(13.5, 14.5, 13.5, 16.5))]


@C("weather-balloon", "Weather balloon rising on a string with a parachute and an instrument box below",
   ["radiosonde", "sounding balloon", "meteorology", "weather forecast", "high altitude balloon", "atmosphere"],
   aliases=["radiosonde"])
def _(S):
    chute = "M9 14.5A3 2.5 0 0 1 15 14.5Z"
    return [shell(circle(12, 6.5, 4.5)), line(seg(12, 11, 12, 13)), shell(chute),
            line(seg(12, 14.5, 12, 18)), shell(rect(10, 18, 4, 3.5, L(S, 0.01, 1)))]


@C("jetpack", "Jetpack with twin rocket tubes blasting flames downward",
   ["jet pack", "rocket pack", "rocket belt", "personal flight", "sci-fi", "future"],
   aliases=["rocket-pack"])
def _(S):
    tube = lambda x: f"M{x} 15V6.5A2.75 2.75 0 0 1 {x + 5.5} 6.5V15Z" if S.name != "rounded" else \
        f"M{x + 1} 15Q{x} 15 {x} 14V6.5A2.75 2.75 0 0 1 {x + 5.5} 6.5V14Q{x + 5.5} 15 {x + 4.5} 15Z"
    fl = lambda x: f"M{x - 1.8} 17L{x} 21.5L{x + 1.8} 17Z"
    return [shell(union(tube(4.5), tube(14), rect(9, 7, 6, 6))), detail(seg(12, 7, 12, 13)),
            solid(fl(7.25)), solid(fl(16.75))]


@C("flying-car", "Car with a raised rotor at each corner of its roof",
   ["flying car", "air car", "evtol", "future car", "roadable aircraft", "sci-fi car"],
   aliases=["air-car"])
def _(S):
    body = poly([(3, 17), (3, 13.5), (5, 12.5), (8, 9.5), (16, 9.5), (19, 12.5), (21, 13.5), (21, 17)], closed=True, r=S.r)
    return [shell(body), detail(seg(5, 12.5, 19, 12.5)), dot(7, 19, 2), dot(17, 19, 2),
            line(seg(6, 9.5, 6, 5.5)), line(seg(18, 9.5, 18, 5.5)), line(seg(2.5, 5, 9.5, 5)), line(seg(14.5, 5, 21.5, 5))]


@C("air-taxi", "Passenger air taxi pod with rotors on arms, hovering on its skids",
   ["evtol", "urban air mobility", "passenger drone", "air taxi", "flying taxi", "vertiport"],
   aliases=["passenger-drone"])
def _(S):
    return [shell(rect(8, 9, 8, 8, L(S, 2, 4))), detail(seg(8, 12.5, 16, 12.5)),
            line(seg(8, 10, 4.5, 7)), line(seg(16, 10, 19.5, 7)), line(seg(2, 5.5, 8, 5.5)), line(seg(16, 5.5, 22, 5.5)),
            line(seg(10, 17, 9, 20.5)), line(seg(14, 17, 15, 20.5)), line(seg(6.5, 20.5, 17.5, 20.5))]


# =========================================================================== small silhouettes for scenes

def xf(d, s=1.0, tx=0.0, ty=0.0, deg=0.0):
    """Scale a closed shape by s about the origin, rotate by deg about the origin, then move it by (tx, ty)."""
    a = math.radians(deg)
    c, n = math.cos(a) * s, math.sin(a) * s
    return path_to_d(transform_path(P(d), (c, n, -n, c, tx, ty)))


# Side-view jet facing right, 10 units long, origin at the fin tip.
JET = "M0 0H1.6L3.6 2.2H8.4C9.6 2.2 10.3 2.8 10.3 3.4C10.3 4 9.6 4.6 8.4 4.6H1.2Z"


def top_plane(r=0.0):
    """Top-view airliner pointing up, centred on the origin, about 10 units long and 10 wide."""
    half = [(0, -5), (0.9, -3.8), (0.9, -1), (5, 1.2), (5, 2.2), (0.9, 1.2), (0.9, 3.6), (2.4, 4.6), (2.4, 5.2),
            (0, 4.8)]
    pts = half + [(-x, y) for x, y in reversed(half[1:-1])]
    return poly(pts, closed=True, r=r)


# =========================================================================== rail extras

@C("road-rail-truck", "Pickup truck riding on railway track on small lowered rail wheels",
   ["hi-rail truck", "road rail vehicle", "track inspection", "rail maintenance", "two way vehicle", "pickup"],
   aliases=["hi-rail-truck"])
def _(S):
    k = L(S, 0.5, 1.5)
    body = union(rect(2.5, 10, 10, 5, k), rect(11, 6, 5, 9, k),
                 poly([(15, 6), (17.5, 10), (21.5, 10), (21.5, 15), (15, 15)], closed=True, r=L(S, 0, 1)))
    return [shell(body), detail(seg(12, 10, 16.5, 10)),
            shell(circle(7, 16, 2)), shell(circle(17.5, 16, 2)),
            dot(3.5, 19.25, 1.25), dot(13, 19.25, 1.25), line(seg(2, 21.5, 22, 21.5))]


# =========================================================================== aircraft extras

@C("microlight", "Microlight trike with a pusher propeller hanging under a delta wing",
   ["ultralight", "flex wing", "trike", "weight shift", "microlight aircraft", "light aviation"],
   aliases=["ultralight-trike"])
def _(S):
    wing = poly([(2.5, 6.5), (21.5, 3), (17, 7)], closed=True, r=L(S, 0, 0.8))
    pod = ("M8.5 16V14Q8.5 11.5 11 11.5H14L19.5 16Z" if S.name != "rounded" else
           "M10 16Q8.5 16 8.5 14.5V14Q8.5 11.5 11 11.5H14L18.8 15.3Q19.5 16 18.5 16Z")
    return [shell(wing, stroke_miterlimit="2"), line(seg(12.5, 6, 12.5, 11.5)),
            shell(pod), line(seg(5, 11.5, 5, 20)), line(seg(8.5, 14.5, 5, 14.5)),
            dot(10.5, 19.5, 1.75), dot(17, 19.5, 1.75)]


@C("banner-towing-plane", "Small plane towing a long advertising banner behind it",
   ["banner plane", "aerial advertising", "sky banner", "tow plane", "aerial banner", "beach advert"],
   aliases=["banner-plane"])
def _(S):
    plane = "M13.5 11.5L13 5.5H14.5L17 9H20Q22 9 22 10.5Q22 12 20 12H14Z"
    wing = poly([(16.5, 11), (19, 11), (16.5, 16), (15, 16)], closed=True, r=L(S, 0, 0.6))
    return [shell(union(plane, wing)), line(seg(13.5, 11.5, 10, 11.5)),
            shell(rect(2, 8.5, 8, 6, L(S, 0.01, 1.5))), detail(seg(4.5, 11.5, 7.5, 11.5))]


@C("aerial-refueling", "Tanker plane passing fuel down a boom to a smaller jet flying behind it",
   ["air refuelling", "aerial refuelling", "tanker", "inflight refueling", "boom", "military aviation"],
   aliases=["air-refueling"])
def _(S):
    k = L(S, 0, 0.4)
    return [solid(xf(top_plane(k), 1.0, 15.5, 8.5, 45)), line(seg(12.1, 11.9, 9.4, 14.6)),
            solid(xf(top_plane(k), 0.7, 6.5, 17.5, 45))]


@C("solar-powered-aircraft", "Aircraft seen from above with very long wings covered in solar cells and small propellers",
   ["solar plane", "solar aircraft", "solar powered", "renewable flight", "electric aircraft", "high altitude"],
   aliases=["solar-plane"])
def _(S):
    k = L(S, 0.01, 1.5)
    return [shell(rect(2, 9, 20, 5, k)), detail(seg(7, 9, 7, 14)), detail(seg(12, 9, 12, 14)), detail(seg(17, 9, 17, 14)),
            line(seg(12, 3, 12, 9)), line(seg(12, 14, 12, 20.5)), line(seg(8.5, 20.5, 15.5, 20.5)),
            line(seg(5.5, 6, 8.5, 6)), line(seg(15.5, 6, 18.5, 6))]


@C("air-show", "Small jet trailing a smoke trail that curls into a loop",
   ["airshow", "aerobatics", "stunt flying", "loop the loop", "smoke trail", "display team"],
   aliases=["aerobatics"])
def _(S):
    trail = "M2 20C9 20 14.5 17 14.5 11.5C14.5 8 12.5 5.5 9.5 5.5C6.5 5.5 5 8 5 10.5C5 13.5 8 15 11.5 15H14"
    return [line(trail), solid(xf(top_plane(L(S, 0, 0.4)), 0.8, 18, 15, 90))]


@C("contrail", "Airliner seen from below trailing two long vapor trails",
   ["vapour trail", "vapor trail", "condensation trail", "jet trail", "jet stream", "sky"],
   aliases=["vapor-trail"])
def _(S):
    return [solid(xf(top_plane(L(S, 0, 0.5)), 1.0, 12, 6.5)),
            line(seg(9.5, 11.5, 9.5, 21.5)), line(seg(14.5, 11.5, 14.5, 21.5))]


@C("sonic-boom", "Jet breaking the sound barrier inside nested shock wave arcs",
   ["supersonic", "sound barrier", "shock wave", "mach", "breaking the sound barrier", "fast jet"],
   aliases=["sound-barrier"])
def _(S):
    return [solid(xf(JET, 1.5, 6, 6.9)),
            line(arc(21.5, 12, 6, 200, 245)), line(arc(21.5, 12, 6, 115, 160)),
            line(arc(21.5, 12, 10.5, 205, 235)), line(arc(21.5, 12, 10.5, 125, 155))]


@C("air-turbulence", "Tilted airliner bumping over wavy lines of rough air",
   ["turbulence", "bumpy flight", "rough air", "fasten seatbelt", "clear air turbulence", "flight"],
   aliases=["turbulence"])
def _(S):
    body = xf("M3.5 8.5L2.5 3H4.5L7.5 6.5H18C20 6.5 21.5 7.5 21.5 8.5C21.5 9.5 20 10.5 18 10.5H6Z", 1, 0, 0)
    wave = lambda y: f"M2 {y}C3.5 {y - 1.2} 5 {y - 1.2} 6.5 {y}S9.5 {y + 1.2} 11 {y}S14 {y - 1.2} 15.5 {y}S18.5 {y + 1.2} 20 {y}S21.5 {y - 1.2} 22 {y - 0.6}"
    return [shell(rot(body, -8, 12, 7)), line(wave(15.5)), line(wave(20.5))]


# =========================================================================== aircraft parts

@C("aircraft-propeller", "Three-blade aircraft propeller around a pointed spinner",
   ["propeller", "prop", "airscrew", "blades", "aviation", "engine"],
   aliases=["airscrew"])
def _(S):
    blade = "M12 12C14 9.5 14.2 5.5 12.8 2.2C12.5 1.9 12 1.9 11.6 2.3C10.8 5.5 10.6 9 12 12Z"
    blades = union(*(rot(blade, a) for a in (0, 120, 240)), circle(12, 12, 3))
    return [shell(blades), dot(12, 12, 1.2)]


@C("landing-gear", "Aircraft landing gear leg with a shock absorber and two wheels",
   ["undercarriage", "landing gear", "wheels down", "aircraft wheel", "strut", "touchdown"],
   aliases=["undercarriage"])
def _(S):
    k = L(S, 0.01, 1.5)
    return [line(seg(3, 3, 21, 3)), shell(rect(10.5, 3, 3, 7, k)), line(seg(12, 10, 12, 18)),
            line(seg(13.5, 7, 19, 3)), line(seg(7, 18, 17, 18)),
            shell(circle(7, 18, 3)), shell(circle(17, 18, 3))]


@C("aircraft-tail", "Airliner tail with a swept fin, a rudder and a horizontal stabilizer",
   ["tail fin", "vertical stabilizer", "empennage", "rudder", "tailplane", "livery"],
   aliases=["tail-fin"])
def _(S):
    fin = poly([(5, 13), (7.5, 2.5), (11, 2.5), (19, 13)], closed=True, r=L(S, 0, 1.2))
    return [shell(fin), detail(seg(10, 5.5, 8.5, 13)), line(poly([(22, 13), (5.5, 13), (2.5, 16.5), (5.5, 20), (22, 20)], r=S.r)),
            line(seg(5.5, 16.5, 13, 16.5))]


@C("control-yoke", "Aircraft control yoke with two grips on a column",
   ["yoke", "control column", "flight controls", "cockpit", "pilot", "steering"],
   aliases=["flight-yoke"])
def _(S):
    k = L(S, 0.5, 1.5)
    horn = "M5 5V9.5Q5 12.5 8 12.5H16Q19 12.5 19 9.5V5"
    return [line(horn), shell(rect(2.5, 3.5, 3.5, 6, k)), shell(rect(18, 3.5, 3.5, 6, k)),
            line(seg(12, 12.5, 12, 21))]


@C("aircraft-throttle", "Cockpit throttle quadrant with two levers pushed forward",
   ["throttle", "thrust lever", "power lever", "cockpit", "engine power", "takeoff thrust"],
   aliases=["thrust-lever"])
def _(S):
    base = ("M3 21V16Q12 11 21 16V21Z" if S.name != "rounded" else
            "M4.5 21Q3 21 3 19.5V16Q12 11 21 16V19.5Q21 21 19.5 21Z")
    return [shell(base), line(seg(9, 16, 10.5, 7)), line(seg(15, 16, 16.5, 7)),
            dot(10.75, 5.25, 2.25), dot(16.75, 5.25, 2.25)]


@C("flight-recorder", "Crash-proof flight recorder box with a carrying handle and a memory module",
   ["black box", "flight data recorder", "cockpit voice recorder", "crash investigation", "fdr", "cvr"],
   aliases=["black-box"])
def _(S):
    k = L(S, 1, 2.5)
    return [shell(rect(9, 8.5, 12, 11.5, k)), shell(rect(3, 10.5, 6, 7.5, L(S, 0.5, 2))),
            detail(seg(12, 20, 16, 8.5)), detail(seg(16, 20, 20, 8.5)),
            line(poly([(12, 8.5), (12, 5), (18, 5), (18, 8.5)], r=S.r))]


@C("ejection-seat", "Pilot seat shooting upward on a rocket flame under a small parachute",
   ["eject", "ejection", "bail out", "escape seat", "fighter pilot", "emergency escape"],
   aliases=["eject-seat"])
def _(S):
    seat = poly([(7, 7), (11, 7), (11, 13), (17, 13), (17, 16.5), (7, 16.5)], closed=True, r=L(S, 0, 1.5))
    chute = "M5 4.5A4.5 3 0 0 1 14 4.5Z" if S.name != "rounded" else "M5.5 4.5A4.5 3 0 0 1 13.5 4.5Q13.5 5 13 5H6Q5.5 5 5.5 4.5Z"
    flame = "M9.5 18.5H14.5C14.5 20.2 13.5 21.5 12 22C10.5 21.5 9.5 20.2 9.5 18.5Z"
    return [shell(seat), shell(chute), line(seg(9.5, 5, 9.5, 7)), solid(flame),
            line(seg(3.5, 10, 3.5, 16)), line(seg(20.5, 11, 20.5, 17))]


@C("pilot-helmet", "Jet pilot helmet in side view with the visor down and an oxygen mask hose",
   ["flight helmet", "fighter pilot", "aviator", "visor", "oxygen mask", "jet pilot"],
   aliases=["flight-helmet"])
def _(S):
    dome = ("M4 16V11C4 6 8 3 12.5 3C17 3 20.5 6 20.5 10.5V12H13.5V16Z" if S.name != "rounded" else
            "M5.5 16Q4 16 4 14.5V11C4 6 8 3 12.5 3C17 3 20.5 6 20.5 10.5Q20.5 12 19 12H13.5V14.5Q13.5 16 12 16Z")
    mask = poly([(15, 14), (20.5, 14), (19.5, 18.5), (16, 18.5)], closed=True, r=L(S, 0, 1))
    return [shell(dome), detail(seg(13, 7.5, 20.5, 7.5)), shell(mask), line("M16 18.5C14 21 10 21 7.5 21.5")]


@C("aircraft-window", "Oval airplane cabin window with the shade half lowered and a cloud outside",
   ["plane window", "window seat", "cabin window", "porthole", "window shade", "flight"],
   aliases=["plane-window"])
def _(S):
    inner = P(rect(7, 4.5, 10, 15, L(S, 3.5, 5)))
    shade = path_to_d(I(P(rect(7, 4.5, 10, 5.5)), inner))
    cloud = "M9.5 17H14.5A2 2 0 0 0 14 13.1A2.5 2.5 0 0 0 9.6 14.1A1.5 1.5 0 0 0 9.5 17Z"
    return [shell(rect(5, 2.5, 14, 19, L(S, 5.5, 7))), Part("dot", shade), detail(cloud)]


@C("airplane-seat", "Reclining airline seat with a headrest, armrest and a fold-down tray table",
   ["plane seat", "aircraft seat", "economy seat", "recline", "tray table", "cabin"],
   aliases=["aircraft-seat"])
def _(S):
    back = poly([(9, 2.5), (13.5, 2.5), (14, 16), (9.5, 16)], closed=True, r=L(S, 0, 1.5))
    pan = rect(9.5, 13, 11, 4, L(S, 0.5, 2))
    return [shell(union(back, pan)), detail(seg(9.1, 6.5, 13.6, 6.5)),
            line(seg(14, 11, 19.5, 11)), line(seg(3, 10, 9.3, 10)), line(seg(5, 10, 7, 12.5)),
            line(seg(12, 17, 11, 21)), line(seg(18, 17, 19, 21))]


@C("overhead-bin", "Airplane overhead luggage bin with its door swung open and a bag inside",
   ["overhead locker", "luggage bin", "overhead compartment", "carry on", "cabin baggage", "hand luggage"],
   aliases=["overhead-locker"])
def _(S):
    k = L(S, 0.5, 1.5)
    return [line(poly([(3, 9), (3, 20), (21, 20), (21, 9)], r=S.r)), line(seg(2, 9, 22, 9)),
            line("M3 9C5 5 10 3 16 3"), shell(rect(7, 14, 10, 6, k)),
            line(poly([(10, 14), (10, 12), (14, 12), (14, 14)], r=S.r * 0.4))]


@C("airline-trolley", "Narrow airline service cart with drawers, a bottle and cups on top",
   ["drinks trolley", "service cart", "galley cart", "in flight service", "catering trolley", "cabin crew"],
   aliases=["drinks-trolley"])
def _(S):
    bottle = "M8.5 7V4.5L9.25 3.5V2H10.75V3.5L11.5 4.5V7Z"
    cup = lambda x: poly([(x, 4.5), (x + 3, 4.5), (x + 2.5, 7), (x + 0.5, 7)], closed=True, r=L(S, 0, 0.3))
    return [shell(rect(6, 8, 12, 12, L(S, 1, 2.5))), detail(seg(6, 12, 18, 12)), detail(seg(6, 16, 18, 16)),
            solid(bottle), solid(cup(13)), dot(8.5, 21.2, 1.3), dot(15.5, 21.2, 1.3)]


@C("airsickness-bag", "Paper sick bag with a folded top and a queasy face printed on it",
   ["sick bag", "barf bag", "motion sickness", "nausea", "air sickness", "travel sickness"],
   aliases=["sick-bag"])
def _(S):
    bag = poly([(5, 21), (5, 6), (7, 3), (17, 3), (19, 6), (19, 21)], closed=True, r=L(S, 0, 1.5))
    mouth = "M9 17.5C10 16.3 11 16.3 12 17.5S14 18.7 15 17.5"
    return [shell(bag), detail(seg(5, 7, 19, 7)), dot(9.75, 12.5, 1.25), dot(14.25, 12.5, 1.25), detail(mouth)]
