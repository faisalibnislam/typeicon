"""TypeIcon Core: maps & travel.

Visual language: places and journeys drawn from simple silhouettes. Signs stand on a 2 px post that
ends on the baseline (y 21.5); pins share one teardrop (`pin_d`) whose Line tip is sharp and whose
Rounded tip is softened; landscapes sit on a horizon line. Vehicles here (tour bus, camper) use the
transport set's wheel grammar: r 2 wheels on the y 18 baseline, cut clear of the body in Filled.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    rect, regular, seg, shell, solid,
)
from geometry import rotation, transform_path

CAT = "travel"
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
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def grow(d, g):
    """Region d expanded by g px."""
    return U(P(d), ST(d, 2 * g, "round", "round"))


def outline_region(d, miter=4.0):
    """Region covered by a closed outline filled to its outer stroke edge."""
    return U(P(d), ST(d, 2.0, "butt", "miter", miter))


def filled_from(fn):
    """Filled design built from the drawing called with the FILL pseudo-style."""
    return lambda: filled_region(fn(FILL))


def pin_d(S, cx, cy, r, h):
    """Map-pin teardrop: head circle (cx, cy, r) and a tip h below the centre. Rounded softens the tip."""
    phi = math.acos(r / h)
    lp = (cx - r * math.sin(phi), cy + r * math.cos(phi))
    rp = (cx + r * math.sin(phi), cy + r * math.cos(phi))
    tip = (cx, cy + h)
    arc_part = f"A{fmt(r)} {fmt(r)} 0 1 1 {_p(rp)}"
    if S.name != "rounded":
        return f"M{_p(tip)}L{_p(lp)}{arc_part}Z"
    t = 1.3
    ln = math.hypot(lp[0] - tip[0], lp[1] - tip[1])
    a = (tip[0] + (lp[0] - tip[0]) * t / ln, tip[1] + (lp[1] - tip[1]) * t / ln)
    b = (tip[0] + (rp[0] - tip[0]) * t / ln, tip[1] + (rp[1] - tip[1]) * t / ln)
    return f"M{_p(a)}L{_p(lp)}{arc_part}L{_p(b)}Q{_p(tip)} {_p(a)}Z"


def rpt(p, deg, c=(12.0, 12.0)):
    """Rotate a point about c (degrees, clockwise on screen)."""
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a)


def wave(x0, x1, y, amp=1.0, n=4):
    """Horizontal wave line from x0 to x1 with n half-waves."""
    w = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        sgn = -1 if i % 2 == 0 else 1
        d += f"Q{fmt(x0 + w * (i + 0.5))} {fmt(y + sgn * amp * 2)} {fmt(x0 + w * (i + 1))} {fmt(y)}"
    return d


# =========================================================================== maps and places

@icon("map", CAT, "Open paper map with a route leading to a marked spot",
      tags=["paper map", "route", "directions", "atlas", "navigation", "trip"])
def _(S):
    pin = pin_d(S, 15.5, 9, 2.75, 5)
    return [shell(rect(3, 4, 18, 16, S.R)), Part("dot", pin),
            dot(6.5, 16.5, 1), dot(9.5, 16.5, 1), dot(12.5, 16.2, 1)]


@icon("map-folded", CAT, "Paper map folded like an accordion into four panels",
      tags=["folded map", "atlas", "map", "travel", "guide", "brochure"])
def _(S):
    xs = [3, 7.5, 12, 16.5, 21]
    top = [(x, 4 if i % 2 else 6) for i, x in enumerate(xs)]
    bot = [(x, 18 if i % 2 else 20) for i, x in enumerate(xs)][::-1]
    return [shell(poly(top + bot, closed=True, r=S.r * 0.5)),
            *[detail(seg(x, y0 + (0 if i % 2 else 0), x, y1)) for i, (x, y0, y1) in
              enumerate([(7.5, 4, 18), (12, 6, 20), (16.5, 4, 18)])]]


@icon("pin-drop", CAT, "Map pin dropping onto a spot on the ground",
      tags=["drop pin", "location", "place", "marker", "set location", "point"], aliases=["drop-pin"])
def _(S):
    return [shell(pin_d(S, 12, 8, 5, 8.5)), detail(circle(12, 8, 1.75)),
            line("M6 17.5A6 2.75 0 0 0 18 17.5")]


@icon("globe-earth", CAT, "Globe with a meridian and the equator; the whole world",
      tags=["globe", "world", "earth", "international", "global", "planet"], aliases=["world"])
def _(S):
    meridian = ellipse(12, 12, 4, 9) if S.name == "rounded" else "M12 3A10.5 10.5 0 0 0 12 21A10.5 10.5 0 0 0 12 3Z"
    return [shell(circle(12, 12, 9)), detail(meridian), detail(seg(3, 12, 21, 12))]


@icon("world-map", CAT, "World map drawn as an oval projection with meridians and the equator",
      tags=["world", "projection", "atlas", "global", "geography", "earth map"])
def _(S):
    meridians = ellipse(12, 12, 4.5, 6.5) if S.name == "rounded" else "M12 5.5A9 9 0 0 0 12 18.5A9 9 0 0 0 12 5.5Z"
    return [shell(ellipse(12, 12, 9, 6.5)), detail(meridians), detail(seg(3, 12, 21, 12))]


@icon("route-pins", CAT, "Two map pins joined by a dashed route",
      tags=["route", "trip", "journey", "directions", "from to", "itinerary"], aliases=["trip-route"])
def _(S):
    return [shell(pin_d(S, 6.5, 11, 3.5, 6)), dot(6.5, 11, 1.25),
            shell(pin_d(S, 17.5, 6.5, 3.5, 6)), dot(17.5, 6.5, 1.25),
            line(seg(6.5, 20.5, 9, 20.5)), line(seg(11.5, 20.5, 14, 20.5)),
            line(poly([(16, 20.5), (17.5, 20.5), (17.5, 19)], r=S.r * 0.5)), line(seg(17.5, 16.5, 17.5, 15))]


# =========================================================================== signs and markers

@icon("signpost", CAT, "Signpost with two boards pointing opposite ways",
      tags=["signpost", "directions", "crossroads", "way", "choice", "fingerpost"], aliases=["fingerpost"])
def _(S):
    return [shell(poly([(5, 3), (17, 3), (19.5, 5.25), (17, 7.5), (5, 7.5)], closed=True, r=S.r * 0.5)),
            shell(poly([(19, 11.5), (7, 11.5), (4.5, 13.75), (7, 16), (19, 16)], closed=True, r=S.r * 0.5)),
            line(seg(12, 7.5, 12, 11.5)), line(seg(12, 16, 12, 21))]


@icon("milestone", CAT, "Roadside milestone with a painted top",
      tags=["milestone", "marker stone", "distance", "road", "kilometre", "mile marker"], aliases=["mile-marker"])
def _(S):
    top = "M6.5 20V10A5.5 5.5 0 0 1 17.5 10V20Z" if S.name == "rounded" else poly([(6.5, 20), (6.5, 9), (9, 5), (15, 5), (17.5, 9), (17.5, 20)], closed=True)
    return [shell(top), detail(seg(6.5, 11, 17.5, 11)), detail(seg(9.5, 15.5, 14.5, 15.5)),
            line(seg(3, 20, 21, 20))]


# =========================================================================== luggage and gear

@icon("luggage", CAT, "Travel case with a handle and two straps",
      tags=["baggage", "suitcase", "bags", "travel", "trip", "check-in"], aliases=["baggage"])
def _(S):
    return [shell(rect(3, 8, 18, 12, S.R)),
            line(poly([(9, 8), (9, 4.5), (15, 4.5), (15, 8)], r=S.r)),
            detail(seg(7.5, 8, 7.5, 20)), detail(seg(16.5, 8, 16.5, 20))]


@icon("suitcase-rolling", CAT, "Upright wheeled suitcase with a pull handle",
      tags=["trolley case", "roller bag", "carry-on", "luggage", "wheels", "travel"], aliases=["rolling-suitcase", "carry-on"])
def _(S):
    return [shell(rect(6, 7.5, 12, 11.5, S.R)),
            line(poly([(9.5, 7.5), (9.5, 3), (14.5, 3), (14.5, 7.5)], r=S.r)),
            detail(seg(10, 10.5, 10, 16)), detail(seg(14, 10.5, 14, 16)),
            dot(8.5, 20.75, 1.25), dot(15.5, 20.75, 1.25)]


@icon("binoculars", CAT, "Pair of binoculars",
      tags=["binoculars", "sightseeing", "look", "explore", "birdwatching", "view"], aliases=["field-glasses"])
def _(S):
    def barrel(cx, sgn):
        body = poly([(cx - 3.5, 16), (cx - 2.5 * 1, 6.5), (cx + 2.5, 6.5), (cx + 3.5, 16)], closed=True, r=S.r * 0.5)
        return union(body, circle(cx, 16, 3.75))
    return [shell(barrel(6.75, -1)), shell(barrel(17.25, 1)),
            line(seg(10.5, 10, 13.5, 10))]


@icon("travel-backpack", CAT, "Hiking backpack with a sleeping mat rolled on top",
      tags=["hiking", "rucksack", "backpacking", "trekking", "camping", "pack"], aliases=["hiking-backpack"])
def _(S):
    body = ("M6.5 21V8.5C6.5 6 8.5 5 12 5C15.5 5 17.5 6 17.5 8.5V21Z" if S.name == "rounded" else
            poly([(6.5, 21), (6.5, 7.5), (9, 5), (15, 5), (17.5, 7.5), (17.5, 21)], closed=True))
    return [shell(body), line("M10 5V3H14V5" if S.name != "rounded" else "M10 5.1V4A1 1 0 0 1 11 3H13A1 1 0 0 1 14 4V5.1"),
            shell(rect(3, 12, 3.5, 7.5, min(S.R, 1.25))), shell(rect(17.5, 12, 3.5, 7.5, min(S.R, 1.25))),
            detail("M6.5 9.5C9 11 15 11 17.5 9.5"), detail(seg(12, 10.6, 12, 14.5)), detail(seg(9, 17.5, 15, 17.5))]


# =========================================================================== outdoors

@icon("camping-tent", CAT, "A-frame camping tent with an open door",
      tags=["tent", "camping", "campsite", "outdoors", "camp", "shelter"], aliases=["campsite"])
def _(S):
    return [shell(poly([(12, 5.5), (20.5, 20), (3.5, 20)], closed=True, r=S.r), stroke_miterlimit="2"),
            line(seg(10.5, 3, 12, 5.5)), line(seg(13.5, 3, 12, 5.5)),
            detail(poly([(8.5, 20), (12, 12.5), (15.5, 20)], r=S.r * 0.5))]


@icon("campfire", CAT, "Campfire flame over two crossed logs",
      tags=["bonfire", "fire", "camping", "flame", "outdoors", "warmth"], aliases=["bonfire"])
def _(S):
    flame = ("M12 3.2C14.5 6 17 8.3 17 11.3A5 5 0 0 1 7 11.3C7 9.4 8 8 9.4 6.8"
             "C9.6 8.2 10.3 9.2 11.2 9.6C10.8 7.3 11.1 5 12 3.2Z")
    return [shell(flame, stroke_miterlimit="1.5"), line(seg(4.5, 17, 19.5, 21)), line(seg(4.5, 21, 19.5, 17))]


@icon("mountain", CAT, "Mountain range with a snow-capped peak",
      tags=["mountains", "peak", "hiking", "summit", "landscape", "alps"], aliases=["mountains"])
def _(S):
    return [shell(poly([(3.5, 20), (9.5, 6), (13.5, 13.2), (15.5, 10.5), (20.5, 20)], closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
            detail(poly([(7.1, 10.2), (8.6, 11.8), (10.2, 10.2), (11.6, 11.8)], r=S.r * 0.3))]


@icon("beach-umbrella", CAT, "Tilted beach umbrella planted in the sand",
      tags=["parasol", "beach", "summer", "holiday", "vacation", "sunshade"], aliases=["parasol"])
def _(S):
    canopy = ("M3.5 10.5A8.5 7 0 0 1 20.5 10.5"
              "A2.83 1.8 0 0 0 14.83 10.5A2.83 1.8 0 0 0 9.17 10.5A2.83 1.8 0 0 0 3.5 10.5Z")
    a, b = rpt((12, 11.5), -18), rpt((12, 21.5), -18)
    return [shell(rot(canopy, -18, 12, 12)), line(seg(*a, *b)),
            line(seg(3, 21, 21, 21))]


@icon("palm-tree", CAT, "Palm tree with drooping fronds",
      tags=["palm", "tropical", "beach", "holiday", "island", "summer"], aliases=[])
def _(S):
    return [line("M11 7.5C12.8 11.5 13.5 16 13 21"),
            line("M11 7.5C9 4.5 5.5 4 3 6.5"), line("M11 7.5C13 4.5 16.5 4 19 6.5"),
            line("M11 7.5C7.5 7.5 5 9.5 4.5 12.5"), line("M11 7.5C14.5 7.5 17 9.5 17.5 12.5"),
            line("M11 7.5C10.5 5.7 11 4.3 12.5 3"),
            line(seg(8, 21, 18, 21))]


@icon("island", CAT, "Small island with a palm tree surrounded by water",
      tags=["desert island", "tropical", "beach", "holiday", "ocean", "paradise"], aliases=["desert-island"])
def _(S):
    return [shell("M5 18.5C6.5 15.8 9 14.8 12 14.8C15 14.8 17.5 15.8 19 18.5Z"),
            line("M10.5 7C11.7 9.5 12.2 12 12 14.8"),
            line("M10.5 7C9 5 6.5 4.5 4.5 6.5"), line("M10.5 7C12 5 14.5 4.5 16.5 6.5"),
            line("M10.5 7C8 7.3 6.5 8.5 6 10.5"), line("M10.5 7C13 7.3 14.5 8.5 15 10.5"),
            line(wave(3, 21, 20.5, 0.5, 6))]


@icon("sunrise", CAT, "Half sun rising above the horizon with an upward arrow",
      tags=["sunrise", "dawn", "morning", "daybreak", "sun up", "east"], aliases=["dawn"])
def _(S):
    return [shell("M7 17A5 5 0 0 1 17 17Z"), line(seg(3, 17, 21, 17)), line(seg(7, 21, 17, 21)),
            line(seg(*_ray(215, 7.5), *_ray(215, 9.5))), line(seg(*_ray(325, 7.5), *_ray(325, 9.5))),
            line(seg(12, 9, 12, 3.5)), line(poly([(9.5, 6), (12, 3.5), (14.5, 6)], r=S.r * 0.5))]


@icon("sunset", CAT, "Half sun setting below the horizon with a downward arrow",
      tags=["sunset", "dusk", "evening", "sundown", "sun down", "west"], aliases=["dusk"])
def _(S):
    return [shell("M7 17A5 5 0 0 1 17 17Z"), line(seg(3, 17, 21, 17)), line(seg(7, 21, 17, 21)),
            line(seg(*_ray(215, 7.5), *_ray(215, 9.5))), line(seg(*_ray(325, 7.5), *_ray(325, 9.5))),
            line(seg(12, 3, 12, 9)), line(poly([(9.5, 6.5), (12, 9), (14.5, 6.5)], r=S.r * 0.5))]


def _ray(deg, r, c=(12, 17)):
    a = math.radians(deg)
    return c[0] + r * math.cos(a), c[1] + r * math.sin(a)


# --------------------------------------------------------------------------- vehicle grammar (shared with transport)

def wheel(x, y=18.0, r=2.0):
    """Side-view wheel: a ring in Line/Rounded; a solid disc cut 1 px clear of the body in Filled."""
    p = shell(circle(x, y, r))
    p.wheel = (x, y, r)
    return p


def vbody(S, pts, wheels, yb=18.0, r=2.0):
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


# =========================================================================== roads and street furniture

@icon("road", CAT, "Road stretching into the distance with a dashed centre line",
      tags=["street", "route", "drive", "lane", "journey", "asphalt"], aliases=["street"])
def _(S):
    return [line(seg(3, 21, 8.5, 3)), line(seg(21, 21, 15.5, 3)),
            line(seg(12, 3, 12, 6)), line(seg(12, 9.5, 12, 13.5)), line(seg(12, 17, 12, 21))]


@icon("highway", CAT, "Wide highway with two dashed lane lines",
      tags=["motorway", "freeway", "expressway", "lanes", "interstate", "road trip"], aliases=["motorway", "freeway"])
def _(S):
    def lane(x0, x1, y0, y1):
        return seg(x0 + (x1 - x0) * (21 - y0) / 18, y0, x0 + (x1 - x0) * (21 - y1) / 18, y1)
    return [line(seg(3.5, 21, 7.5, 3)), line(seg(20.5, 21, 16.5, 3)),
            *[line(lane(9, 10.7, a, b)) for a, b in ((21, 17.5), (14.5, 11), (8, 5))],
            *[line(lane(15, 13.3, a, b)) for a, b in ((21, 17.5), (14.5, 11), (8, 5))]]


@icon("traffic-light", CAT, "Traffic light with red, amber and green lamps",
      tags=["traffic signal", "stoplight", "signal", "intersection", "stop", "go"], aliases=["traffic-signal", "stoplight"])
def _(S):
    return [shell(rect(7.5, 3, 9, 15, S.R)), line(seg(12, 18, 12, 21)),
            dot(12, 7, 1.4), dot(12, 10.5, 1.4), dot(12, 14, 1.4)]


@icon("crosswalk", CAT, "Zebra crossing stripes between two kerbs",
      tags=["zebra crossing", "pedestrian crossing", "crossing", "walk", "street", "pedestrian"],
      aliases=["zebra-crossing", "pedestrian-crossing"])
def _(S):
    k = L(S, 0, 0.75)
    return [line(seg(3, 4, 21, 4)), line(seg(3, 20, 21, 20)),
            *[solid(rect(x, 7.5, 3, 9, k)) for x in (3, 8, 13, 18)]]


@icon("parking-meter", CAT, "Parking meter on a post",
      tags=["parking", "meter", "pay parking", "coin", "street", "car park"])
def _(S):
    head = ("M7 13V8A5 5 0 0 1 17 8V13Z" if S.name == "rounded" else
            poly([(7, 13), (7, 6), (9, 3), (15, 3), (17, 6), (17, 13)], closed=True))
    return [shell(head), detail(seg(10, 7.5, 14, 7.5)), dot(12, 10.5, 1),
            line(seg(12, 13, 12, 21)), line(seg(8.5, 21, 15.5, 21))]


@icon("toll-booth", CAT, "Toll booth with a raised barrier arm",
      tags=["toll", "tollgate", "barrier", "highway", "payment", "checkpoint"], aliases=["tollgate"])
def _(S):
    return [shell(rect(3.5, 7.5, 7, 13.5, S.R * 0.5)), line(seg(3, 4.5, 11, 4.5)),
            detail(seg(3.5, 12, 10.5, 12)),
            line(seg(10.5, 14, 21, 14)), line(seg(18.5, 14, 18.5, 21))]


@icon("street-sign", CAT, "Street name plate on a post",
      tags=["street name", "road name", "address", "sign", "avenue", "corner"], aliases=["street-name"])
def _(S):
    return [shell(rect(3, 3.5, 18, 6.5, S.R * 0.5)), detail(seg(6.5, 6.75, 17.5, 6.75)),
            line(seg(12, 10, 12, 21)), line(seg(9.5, 21, 14.5, 21))]


# =========================================================================== navigation and space

@icon("gps", CAT, "Satellite navigation unit on a mount showing a direction arrow",
      tags=["sat nav", "navigator", "navigation", "gps device", "directions", "car navigation"], aliases=["sat-nav", "satnav"])
def _(S):
    arrow = poly([(12, 7.3), (15.4, 14.5), (12, 12.6), (8.6, 14.5)], closed=True, r=S.r * 0.3)
    return [shell(rect(3, 4.5, 18, 13, S.R)), Part("dot", arrow),
            line(seg(12, 17.5, 12, 21)), line(seg(8, 21, 16, 21))]


@icon("satellite", CAT, "Orbiting satellite with two solar panels",
      tags=["satellite", "orbit", "space", "gps", "communication", "spacecraft"], aliases=["spacecraft"])
def _(S):
    def rr(x, y, w, h, r=0.0):
        return poly([rpt(p, -45) for p in ((x, y), (x + w, y), (x + w, y + h), (x, y + h))], closed=True, r=r)

    def sg(x1, y1, x2, y2):
        return seg(*rpt((x1, y1), -45), *rpt((x2, y2), -45))
    k = S.r * 0.5
    return [shell(rr(2.5, 9.25, 6, 5.5, k)), shell(rr(15.5, 9.25, 6, 5.5, k)), shell(rr(10, 8.5, 4, 7, k)),
            detail(sg(5.5, 9.25, 5.5, 14.75)), detail(sg(18.5, 9.25, 18.5, 14.75)),
            line(sg(8.5, 12, 10, 12)), line(sg(14, 12, 15.5, 12)),
            line(sg(12, 8.5, 12, 5.5)), dot(*rpt((12, 4.5), -45), 1.5)]


# =========================================================================== trips and documents

@veh("tour-bus", "Open-top double-decker sightseeing bus",
     ["sightseeing", "tour", "double decker", "coach", "city tour", "excursion"], aliases=["sightseeing-bus"])
def _(S):
    parts = vbody(S, [(3, 18), (3, 8), (21, 8), (21, 18)], [6.5, 17.5])
    return parts + [wheel(6.5), wheel(17.5),
                    line(poly([(3, 8), (3, 3.5), (21, 3.5), (21, 8)], r=S.r)),
                    line(seg(8.5, 3.5, 8.5, 8)), line(seg(15.5, 3.5, 15.5, 8)),
                    detail(seg(3, 12.5, 21, 12.5))]


@icon("cruise", CAT, "Cruise ship with stacked decks and a funnel",
      tags=["cruise ship", "liner", "ocean liner", "voyage", "sea", "holiday"], aliases=["cruise-ship"])
def _(S):
    hull = poly([(3.5, 13.5), (20.5, 13.5), (18.5, 20), (5.5, 20)], closed=True, r=S.r * 0.6)
    decks = poly([(4.5, 13.5), (4.5, 9.5), (7, 9.5), (7, 6.5), (17, 6.5), (17, 9.5), (19.5, 9.5), (19.5, 13.5)], closed=True, r=S.r * 0.6)
    return [shell(union(hull, decks)),
            shell(rect(10, 3, 3.5, 3.5, L(S, 0, 1))),
            detail(seg(4.5, 13.5, 19.5, 13.5)), dot(8, 16.75, 1), dot(12, 16.75, 1), dot(16, 16.75, 1)]


@icon("souvenir", CAT, "Souvenir keyring with a heart tag",
      tags=["keepsake", "keyring", "memento", "gift", "trinket", "holiday"], aliases=["keepsake"])
def _(S):
    tag = [rpt(p, -30, (14, 14)) for p in ((9, 8.5), (19, 8.5), (19, 19.5), (9, 19.5))]
    heart = ("M14 17.2C12 15.8 10.8 14.6 10.8 13.2C10.8 12.1 11.6 11.4 12.5 11.4C13.2 11.4 13.7 11.8 14 12.3"
             "C14.3 11.8 14.8 11.4 15.5 11.4C16.4 11.4 17.2 12.1 17.2 13.2C17.2 14.6 16 15.8 14 17.2Z")
    return [shell(poly(tag, closed=True, r=S.R * 0.6)), Part("dot", rot(heart, -30, 14, 14)),
            line(circle(6, 6, 3))]


@icon("postcard-travel", CAT, "Picture postcard with a sunset over the sea and a stamp",
      tags=["postcard", "holiday", "greetings", "wish you were here", "vacation", "mail"], aliases=["picture-postcard"])
def _(S):
    return [shell(rect(3, 5, 18, 14, S.R * 0.5)),
            dot(7.5, 10.25, 2.25), detail(wave(4.5, 11, 14.5, 0.5, 3)),
            detail(seg(13, 7.5, 13, 16.5)),
            Part("dot", rect(15.5, 8, 3.5, 3.5, L(S, 0, 0.75))), detail(seg(15.5, 14.5, 19, 14.5))]


@icon("visa", CAT, "Travel document with an approval stamp",
      tags=["visa", "entry permit", "immigration", "travel document", "approved", "border"], aliases=["entry-visa"])
def _(S):
    stamp = poly([rpt(p, -12, (12, 9)) for p in ((7.5, 6), (16.5, 6), (16.5, 12), (7.5, 12))], closed=True, r=S.r * 0.3)
    return [shell(rect(5, 3, 14, 18, S.R)), detail(stamp),
            detail(seg(*rpt((9.5, 9), -12, (12, 9)), *rpt((14.5, 9), -12, (12, 9)))),
            detail(seg(8, 15.5, 16, 15.5)), detail(seg(8, 18, 12.5, 18))]


@icon("currency-exchange-travel", CAT, "Two coins with arrows swapping one for the other; exchange money abroad",
      tags=["money exchange", "bureau de change", "foreign currency", "forex", "exchange", "travel money"],
      aliases=["bureau-de-change"])
def _(S):
    return [shell(rect(3, 3.5, 10.5, 7, min(S.R, 1.5))), dot(8.25, 7, 1.25), shell(circle(16, 17, 4)), detail(seg(16, 15, 16, 19)),
            line("M14 3.5C16.8 3.5 19 5.5 19 8.5"), line(poly([(17, 7.5), (19, 9.5), (21, 7.5)], r=S.r * 0.5)),
            line("M10 20.5C7.2 20.5 5 18.5 5 15.5"), line(poly([(3, 16.5), (5, 14.5), (7, 16.5)], r=S.r * 0.5))]


# =========================================================================== stays

@icon("hostel", CAT, "House with bunk beds inside; a hostel",
      tags=["hostel", "dormitory", "bunk beds", "backpackers", "budget stay", "accommodation"], aliases=["dormitory"])
def _(S):
    return [shell(poly([(3.5, 21), (3.5, 10.5), (12, 3.5), (20.5, 10.5), (20.5, 21)], closed=True, r=S.r)),
            detail(seg(7.5, 11, 7.5, 21)), detail(seg(16.5, 13.5, 16.5, 21)),
            detail(seg(7.5, 14, 16.5, 14)), detail(seg(7.5, 18.5, 16.5, 18.5))]


@icon("resort", CAT, "Holiday resort: a hotel block beside a palm tree",
      tags=["resort", "holiday", "vacation", "hotel", "beach resort", "getaway"], aliases=["holiday-resort"])
def _(S):
    return [shell(rect(12, 5, 8.5, 16, S.R * 0.5)),
            dot(14.75, 9, 1), dot(17.75, 9, 1), dot(14.75, 12.5, 1), dot(17.75, 12.5, 1), detail(seg(16.25, 16.5, 16.25, 21)),
            line("M6 9.5C7 12.5 7.3 17 7 21"),
            line("M6 9.5C5 7.5 4 7 3 7.5"), line("M6 9.5C7 7.5 8.3 7 9.5 7.5"),
            line("M6 9.5C4.5 9.8 3.3 10.8 3 12.3"), line("M6 9.5C7.5 9.8 8.7 10.8 9 12.3"),
            line(seg(3, 21, 10.5, 21))]


@veh("camper", "Camper van with a living box and a cab",
     ["camper van", "motorhome", "rv", "caravan", "road trip", "camping"], aliases=["motorhome", "rv"])
def _(S):
    pts = [(3, 18), (3, 5), (16.5, 5), (16.5, 8.5), (19, 8.5), (21, 12.5), (21, 18)]
    return vbody(S, pts, [6.5, 17.5]) + [wheel(6.5), wheel(17.5),
            detail(seg(5, 9.5, 10, 9.5)),
            detail(poly([(16.5, 8.5), (16.5, 12.5), (21, 12.5)], r=S.r * 0.5)),
            detail(seg(12.5, 9.5, 12.5, 15))]


# --------------------------------------------------------------------------- aircraft glyph (top view, nose up)

_PLANE_R = [(12.9, 2.7), (13.4, 4), (13.4, 9.2), (21, 13.6), (21, 15.6), (13.4, 13.6), (13.4, 18.2),
            (16.4, 20.2), (16.4, 21.8), (12, 20.9)]
PLANE = [(12, 2)] + _PLANE_R + [(24 - x, y) for x, y in reversed(_PLANE_R[:-1])]


def plane_pts(deg=0.0, s=1.0, cx=12.0, cy=12.0):
    """The shared top-view aircraft rotated by deg (clockwise), scaled by s and centred on (cx, cy)."""
    out = []
    for x, y in PLANE:
        rx, ry = rpt((x, y), deg, (12, 12))
        out.append((cx + (rx - 12) * s, cy + (ry - 12) * s))
    return out


@icon("plane-ticket", CAT, "Flight ticket with a plane and a tear-off stub",
      tags=["flight ticket", "air ticket", "airline", "booking", "flight", "e-ticket"], aliases=["flight-ticket", "air-ticket"])
def _(S):
    rr = min(S.R, 2.0)
    body = rect(3, 5.5, 18, 13, rr)
    return [shell(body), Part("dot", poly(plane_pts(90, 0.42, 9, 12), closed=True, r=S.r * 0.2)),
            detail(seg(16, 5.5, 16, 8)), detail(seg(16, 10.75, 16, 13.25)), detail(seg(16, 16, 16, 18.5))]


@icon("boarding-pass", CAT, "Boarding pass with a plane, flight details and a barcode",
      tags=["boarding card", "flight", "check-in", "gate", "airline", "mobile pass"], aliases=["boarding-card"])
def _(S):
    return [shell(rect(5, 3, 14, 18, S.R)),
            Part("dot", poly(plane_pts(0, 0.33, 12, 7.5), closed=True, r=S.r * 0.2)),
            detail(seg(5, 12, 19, 12)),
            detail(seg(8.5, 14.75, 8.5, 18)), detail(seg(12, 14.75, 12, 18)), detail(seg(15.5, 14.75, 15.5, 18))]
