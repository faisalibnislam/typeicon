"""TypeIcon Core: airport ground vehicles, rotorcraft, drones and watercraft (batch craft_002).

Visual language (shared with craft_001):
  * Side-view vehicles, aircraft and boats face right (bow or nose on the right, stern or tail on the left).
  * Water is a single wave line along the bottom (y about 20.5); hulls end at y 18 or above so the wave keeps
    its gap. Wheels are solid discs.
  * Line uses small corner radii and sharp joins; Rounded softens every corner (`L(S, line, rounded)`), and the
    Filled design is derived from the Line geometry.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    rect, regular, seg, shell, solid, pt_on,
)
from geometry import rotation, transform_path

CAT = "craft"
FILL = Style("filled", "butt", "miter", R=2.0, r=0.0)  # Line geometry for Filled designs


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Value for Line/Filled (a) or Rounded (b)."""
    return b if S.name == "rounded" else a


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def rot(d, deg, cx=12.0, cy=12.0):
    """Rotate a closed shape's d-string clockwise on screen."""
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpt(p, deg, c=(12.0, 12.0)):
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a)


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


def wave(y=20.5, x0=2.0, x1=22.0, h=4.5, a=1.0):
    """Wave line from x0 to about x1 (half period h, amplitude a)."""
    n = max(1, int(round((x1 - x0) / h)))
    h = (x1 - x0) / n
    out = [f"M{fmt(x0)} {fmt(y)}C{fmt(x0 + h / 3)} {fmt(y - a)} {fmt(x0 + 2 * h / 3)} {fmt(y - a)} {fmt(x0 + h)} {fmt(y)}"]
    for i in range(1, n):
        s = a if i % 2 else -a
        xe = x0 + (i + 1) * h
        out.append(f"S{fmt(xe - h / 3)} {fmt(y + s)} {fmt(xe)} {fmt(y)}")
    return "".join(out)


def hull(S, x0, x1, top, bot, bow=3.0, stern=1.5):
    """Side-view hull: flat deck from x0 to x1, raked bow on the right and a short raked stern."""
    return poly([(x0, top), (x1, top), (x1 - bow, bot), (x0 + stern, bot)], closed=True, r=S.r)


def place(d, deg, tx, ty):
    """Rotate a closed shape drawn around the origin by deg (clockwise) and move it to (tx, ty)."""
    a = math.radians(deg)
    c, s = round(math.cos(a), 12), round(math.sin(a), 12)
    return path_to_d(transform_path(P(d), (c, s, -s, c, tx, ty)))


def place_pts(pts, deg, tx, ty):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(tx + x * c - y * s, ty + x * s + y * c) for x, y in pts]


def quad_top(S, cx, cy, s, rr=1.4):
    """Tiny top-view quadcopter: X arms, a rotor disc at each end and a square (Line) or round (Rounded) body."""
    body = dot(cx, cy, 2) if S.name == "rounded" else Part("dot", poly([(cx, cy - 2.75), (cx + 2.75, cy), (cx, cy + 2.75), (cx - 2.75, cy)], closed=True))
    return [line(seg(cx - s, cy - s, cx + s, cy + s)), line(seg(cx - s, cy + s, cx + s, cy - s)), body,
            dot(cx - s, cy - s, rr), dot(cx + s, cy - s, rr), dot(cx - s, cy + s, rr), dot(cx + s, cy + s, rr)]


# =========================================================================== airport ground support

@C("evacuation-slide", "Aircraft door with an inflated escape slide angling down to the ground",
   ["escape slide", "emergency slide", "evacuation", "aircraft emergency", "cabin safety", "emergency exit"])
def _(S):
    fus = "M2 2.5H18C20.2 2.5 22 4.3 22 6.5S20.2 10.5 18 10.5H2Z"
    door = poly([(5, 10.5), (5, 5), (9, 5), (9, 10.5)], r=S.r * 0.5)
    slide = poly([(4.5, 12.5), (9.5, 12.5), (21.5, 19), (21.5, 21.5), (17.5, 21.5)], closed=True, r=S.r * 0.6)
    return [shell(fus), detail(door), sq(12, 5.5, 2, 2, L(S, 0, 0.8)), sq(16, 5.5, 2, 2, L(S, 0, 0.8)),
            shell(slide, stroke_miterlimit="2")]


@C("pushback-tug", "Low flat airport tug pushing an airliner by a tow bar on its nose wheel",
   ["pushback tractor", "aircraft tug", "tow tractor", "airport", "ground handling", "towbar", "ramp"])
def _(S):
    nose = "M2 3H7.5C11 3 14 5.5 14 8.5C14 9.3 13.3 10 12.5 10H2Z"
    tug = poly([(14.5, 17.5), (14.5, 15), (19, 15), (19.5, 13), (22, 13), (22, 17.5)], closed=True, r=S.r * 0.5)
    return [shell(nose), sq(3.5, 5, 2, 2, L(S, 0, 0.8)), sq(7, 5, 2, 2, L(S, 0, 0.8)),
            line(seg(8.5, 10, 8.5, 16)), dot(8.5, 18.5, 2.25),
            line(seg(10.5, 17.5, 14.5, 16.25)), shell(tug), dot(16.5, 20, 1.5), dot(20, 20, 1.5)]


@C("baggage-tractor", "Small open airport tractor pulling a train of covered baggage carts",
   ["baggage cart", "baggage train", "luggage tractor", "airport", "ground handling", "tug", "dolly"])
def _(S):
    k = L(S, 0.5, 1.5)
    cart = lambda x: union(rect(x, 9, 5.5, 2, L(S, 0.01, 1)), rect(x + 0.5, 10, 4.5, 6, k))
    tractor = poly([(16.5, 16), (16.5, 9), (18.5, 9), (18.5, 12.5), (22, 12.5), (22, 16)], closed=True, r=S.r * 0.6)
    return [shell(cart(2)), shell(cart(9)), line(seg(7.5, 14.5, 9.5, 14.5)), line(seg(14.5, 14.5, 16.5, 14.5)),
            shell(tractor), dot(4.75, 18.5, 1.5), dot(11.75, 18.5, 1.5), dot(18, 18.5, 1.6), dot(21, 18.5, 1.3)]


@C("belt-loader", "Small vehicle with an inclined conveyor belt carrying a suitcase up into an aircraft hold",
   ["baggage loader", "conveyor belt loader", "airport", "ground handling", "luggage", "cargo hold", "ramp"])
def _(S):
    ang, ox, oy = -32, 2.5, 17
    fus = "M14.5 2H22V11H14.5C12.6 11 11 9.4 11 7.5V5.5C11 3.6 12.6 2 14.5 2Z"
    belt = place(rect(0, 0, 15, 2.5, L(S, 0.3, 1.25)), ang, ox, oy)
    bag = place(rect(5.5, -4.5, 4.5, 3, L(S, 0.3, 1)), ang, ox, oy)
    return [shell(fus), detail(poly([(15, 11), (15, 7.5), (19.5, 7.5), (19.5, 11)], r=S.r * 0.4)),
            sq(13.5, 4, 2, 1.5, L(S, 0, 0.7)), sq(17, 4, 2, 1.5, L(S, 0, 0.7)), shell(belt), shell(bag),
            shell(rect(6, 17.5, 10, 2.5, L(S, 0.3, 1.25))), dot(8, 21, 1.4), dot(14, 21, 1.4)]


@C("catering-truck", "Catering truck with its box body raised high on a scissor lift",
   ["airline catering", "high loader", "scissor lift truck", "airport", "ground handling", "in-flight meals"])
def _(S):
    k = L(S, 0.5, 1.5)
    return [shell(rect(2.5, 2.5, 13, 6.5, k)),
            line(seg(4, 11, 13, 15)), line(seg(13, 11, 4, 15)),
            shell(union(rect(2.5, 15, 13, 3, k), rect(15, 11, 6.5, 7, k))),
            detail(seg(17.5, 11, 17.5, 14.5)), dot(6, 20.5, 1.6), dot(18, 20.5, 1.6)]


@C("aircraft-refueler", "Fuel tanker truck parked under an aircraft wing with a hose up to the wing",
   ["refueling truck", "refuelling", "fuel bowser", "into-plane fueling", "airport", "jet fuel", "ground handling"],
   aliases=["fuel-bowser"])
def _(S):
    wing = "M2 5.5C2 3.8 4.5 3 8.5 3.3L22 5L8.5 7.3C4.5 7.8 2 7.2 2 5.5Z"
    tank = rect(2.5, 12.5, 11, 5.5, L(S, 1.5, 2.75))
    cab = poly([(15.5, 18), (15.5, 12), (19.5, 12), (21.5, 15), (21.5, 18)], closed=True, r=S.r * 0.6)
    return [shell(wing), shell(tank), shell(cab), line("M9 12.5C9 10 12 11 12 8.5"),
            dot(5.5, 20.5, 1.5), dot(10.5, 20.5, 1.5), dot(18.5, 20.5, 1.5)]


# =========================================================================== rotorcraft

@C("tandem-rotor-helicopter", "Long helicopter with a big rotor at each end, the rear one raised on a tall pylon",
   ["tandem rotor", "twin rotor helicopter", "chinook style", "heavy lift helicopter", "rotorcraft", "military"])
def _(S):
    body = union("M3 16.5V11H17.5C20 11 21.5 12.5 21.5 14.5V16.5Z" if S.name != "rounded" else
                 "M4.5 16.5Q3 16.5 3 15V11H17.5C20 11 21.5 12.5 21.5 14.5Q21.5 16.5 19.5 16.5Z",
                 poly([(3, 12), (3.5, 6.5), (7, 6.5), (8.5, 12)], closed=True))
    return [line(seg(2, 3.5, 12, 3.5)), line(seg(5.25, 3.5, 5.25, 6.5)), line(seg(12, 7.5, 22, 7.5)),
            line(seg(18, 7.5, 18, 11)), shell(body), sq(10, 12.5, 2, 2, L(S, 0, 0.8)), sq(13.5, 12.5, 2, 2, L(S, 0, 0.8)),
            dot(6.5, 19.5, 1.6), dot(18, 19.5, 1.6)]


@C("rescue-helicopter", "Hovering helicopter lowering a rescue basket on a winch cable",
   ["air rescue", "search and rescue", "sar", "winch", "hoist", "air ambulance", "coast guard"])
def _(S):
    body = "M9 5.5H14.5C17 5.5 19 7.5 19 9.5C19 10.3 18.3 11 17.5 11H10.5C9.7 11 9 10.3 9 9.5Z"
    basket = poly([(8.5, 16.5), (16.5, 16.5), (15, 21.5), (10, 21.5)], closed=True, r=S.r * 0.6)
    return [line(seg(6, 2.5, 22, 2.5)), line(seg(14, 2.5, 14, 5.5)), shell(body),
            line(seg(2.5, 7.5, 9, 7.5)), line(seg(3, 5, 3, 10)), line(seg(12.5, 11, 12.5, 16.5)),
            shell(basket), detail(seg(9.5, 19, 15.5, 19))]


# =========================================================================== drones

@C("fixed-wing-drone", "Small unmanned plane seen from above with straight wings, a twin boom tail and a pusher propeller",
   ["uav", "unmanned aircraft", "survey drone", "fixed wing uav", "mapping drone", "reconnaissance"])
def _(S):
    k = L(S, 0.5, 1.5)
    body = union(rect(2, 8, 20, 3, k), rect(10.5, 3.5, 3, 11.5, L(S, 1, 1.5)))
    return [shell(body), line(seg(7, 11, 7, 19)), line(seg(17, 11, 17, 19)), shell(rect(5.5, 18.5, 13, 2.5, k)),
            line(seg(9.5, 16.5, 14.5, 16.5))]


@C("drone-remote", "Handheld drone controller with two thumbsticks, a phone clipped on top and two antennas",
   ["drone controller", "remote controller", "transmitter", "rc", "uav", "joystick", "pilot"])
def _(S):
    return [shell(rect(2.5, 10.5, 19, 9, L(S, 2, 4))), detail(circle(7.5, 15, 1.75)), detail(circle(16.5, 15, 1.75)),
            shell(rect(7.5, 2.5, 9, 5.5, L(S, 0.5, 1.5))), line(seg(12, 8, 12, 10.5)),
            line(seg(4, 10.5, 3, 5)), line(seg(20, 10.5, 21, 5))]


@C("fpv-goggles", "Boxy drone pilot goggles with a head strap and two short antennas on top",
   ["fpv", "first person view", "drone goggles", "video goggles", "drone racing", "headset"])
def _(S):
    body = rect(4.5, 9, 15, 9, L(S, 1.5, 3.5))
    return [shell(body), detail(seg(12, 9, 12, 13)), line(seg(2, 12, 4.5, 12)), line(seg(19.5, 12, 22, 12)),
            line(seg(2, 15.5, 4.5, 15.5)), line(seg(19.5, 15.5, 22, 15.5)),
            line(seg(8, 9, 7, 4.5)), line(seg(16, 9, 17, 4.5)), dot(7, 3.5, 1.5), dot(17, 3.5, 1.5)]


@C("drone-swarm", "Group of small quadcopters of different sizes flying together",
   ["drone fleet", "swarm", "multiple drones", "uav swarm", "formation", "autonomous"])
def _(S):
    return [*quad_top(S, 7.5, 7.5, 4, 1.75), *quad_top(S, 18.5, 6.5, 2.75, 1.4), *quad_top(S, 15.5, 17.5, 3.25, 1.5)]


@C("drone-light-show", "Night sky with drones forming a star of lights, one drone drawn at a point",
   ["light show", "drone show", "sky show", "fireworks alternative", "led drones", "night event", "formation"])
def _(S):
    outer = regular(12, 13, 9, 5)
    inner = regular(12, 13, 3.8, 5, start=-54)
    pts = []
    for i in range(5):
        pts.append(outer[i])
        pts.append(inner[i])
    parts = []
    for i, p in enumerate(pts):
        q = pts[(i + 1) % len(pts)]
        parts.append(dot((p[0] + q[0]) / 2, (p[1] + q[1]) / 2, 1))
        if i:
            parts.append(dot(p[0], p[1], 1.25))
    ox, oy = outer[0]
    parts += [shell(rect(ox - 1.5, oy - 1, 3, 2, L(S, 0.01, 1))), line(seg(ox - 4.5, oy - 2.75, ox + 4.5, oy - 2.75))]
    return parts


@C("drone-dock", "Drone docking station with its lid opened back and a quadcopter landing on the pad",
   ["drone box", "drone nest", "docking station", "drone in a box", "autonomous drone", "charging pad"])
def _(S):
    k = L(S, 0.5, 1.5)
    lid = poly([(5, 13.5), (2.3, 6), (4.6, 5.1), (7.35, 12.65)], closed=True, r=S.r * 0.4)
    return [shell(rect(4, 14.5, 17.5, 6.5, k)), detail(seg(4, 17, 21.5, 17)), shell(lid),
            shell(rect(13.5, 8, 4, 3, L(S, 0.5, 1.5))),
            line(poly([(13.5, 9.5), (11, 9.5), (11, 5)], r=S.r * 0.5)), line(poly([(17.5, 9.5), (20, 9.5), (20, 5)], r=S.r * 0.5)),
            line(seg(9, 4.5, 13, 4.5)), line(seg(18, 4.5, 22, 4.5)),
            line(seg(14, 11, 13, 12.5)), line(seg(17, 11, 18, 12.5))]


# =========================================================================== work boats and ships

WAVE = wave(20.5)


@C("tugboat", "Short stout tugboat with a tall wheelhouse, a big funnel and tyre fenders along the hull",
   ["tug", "tug boat", "towboat", "harbour tug", "harbor", "towing", "port"])
def _(S):
    body = union(poly([(2.5, 12.5), (17.5, 12.5), (21.5, 10), (19.5, 17.5), (4.5, 17.5)], closed=True, r=S.r),
                 rect(11, 5, 6, 8, L(S, 0.5, 1.5)), rect(5.5, 7, 3.5, 6))
    return [shell(body), sq(12.5, 6.5, 3, 2, L(S, 0, 0.8)), detail(seg(5.5, 9.5, 9, 9.5)),
            dot(7.5, 15, 1.1), dot(11.5, 15, 1.1), dot(15.5, 15, 1.1), line(WAVE)]


@C("trawler", "Fishing trawler with an A-frame gantry at the stern and a net hanging from it",
   ["fishing boat", "fishing vessel", "trawling", "net", "commercial fishing", "seafood"])
def _(S):
    body = union(poly([(7, 12.5), (21.5, 12.5), (19.5, 17.5), (8.5, 17.5)], closed=True, r=S.r),
                 rect(15, 6, 5, 7, L(S, 0.5, 1.5)))
    net = poly([(2, 9.5), (6, 9.5), (4.5, 16.5), (3.5, 16.5)], closed=True, r=S.r * 0.4)
    return [shell(body), sq(16.5, 7.5, 2, 2, L(S, 0, 0.8)), line(poly([(10, 12.5), (7.5, 4), (4, 4), (4, 9.5)], r=S.r)),
            shell(net), detail(seg(4, 9.5, 4, 16.5)), line(WAVE)]


@C("shrimp-boat", "Fishing boat with two long outrigger booms raised from its mast and nets hanging from the tips",
   ["shrimper", "shrimp trawler", "outrigger trawler", "fishing boat", "prawn boat", "gulf coast"])
def _(S):
    body = union(poly([(3, 14), (21.5, 14), (19.5, 18), (5, 18)], closed=True, r=S.r), rect(13.5, 10, 5, 5))
    return [shell(body), line(seg(11, 14, 11, 3)), line(seg(11, 10, 3, 3)), line(seg(11, 10, 21, 3)),
            line(seg(3, 3, 3, 6)), line(seg(21, 3, 21, 6)),
            shell(poly([(2, 6.5), (4, 6.5), (3.6, 11), (2.4, 11)], closed=True, r=S.r * 0.3)),
            shell(poly([(20, 6.5), (22, 6.5), (21.6, 11), (20.4, 11)], closed=True, r=S.r * 0.3)),
            line(WAVE)]


@C("oil-tanker", "Long low tanker ship with a flat deck, a pipe manifold amidships and the bridge at the stern",
   ["tanker", "crude oil tanker", "supertanker", "petroleum", "shipping", "oil transport", "vlcc"])
def _(S):
    body = union(poly([(2, 12.5), (21.5, 12.5), (20, 17.5), (3.5, 17.5)], closed=True, r=S.r),
                 rect(3, 5.5, 5, 7.5, L(S, 0.5, 1.5)), rect(19, 10.5, 2.5, 2.5))
    return [shell(body), sq(4.5, 7, 2, 2, L(S, 0, 0.8)), line(seg(9.5, 12.5, 9.5, 10)),
            line(poly([(12, 12.5), (12, 9.5), (16, 9.5), (16, 12.5)], r=S.r * 0.5)), line(WAVE)]


@C("bulk-carrier", "Cargo ship with a row of deck hatches and tall deck cranes between them",
   ["bulker", "bulk cargo ship", "dry bulk", "freighter", "grain ship", "ore carrier", "shipping"])
def _(S):
    body = union(poly([(2, 13), (21.5, 13), (20, 17.5), (3.5, 17.5)], closed=True, r=S.r),
                 rect(2.5, 5.5, 4.5, 8, L(S, 0.5, 1.5)), rect(8, 11, 3, 2.5), rect(13.5, 11, 3, 2.5), rect(19, 11, 2.5, 2.5))
    return [shell(body), sq(4, 7, 2, 2, L(S, 0, 0.8)),
            line(poly([(12.25, 13), (12.25, 3.5), (15, 3.5), (15, 7.5)], r=S.r * 0.5)),
            line(poly([(17.75, 13), (17.75, 3.5), (20.5, 3.5), (20.5, 7.5)], r=S.r * 0.5)),
            line(WAVE)]


@C("vehicle-carrier-ship", "Tall boxy car carrier ship like a floating building, with a loading ramp lowered at the stern",
   ["car carrier", "ro-ro ship", "roll on roll off", "pctc", "vehicle transport", "car shipping", "shipping"],
   aliases=["ro-ro-ship"])
def _(S):
    body = poly([(6, 17.5), (6, 4), (18, 4), (21.5, 8), (20.5, 17.5)], closed=True, r=S.r)
    return [shell(body), detail(seg(6, 10.5, 20.8, 10.5)), sq(15, 5.5, 2, 2, L(S, 0, 0.8)), sq(18, 6, 1.5, 2, L(S, 0, 0.7)),
            line(seg(6, 15.5, 2, 19.5)), line(wave(20.5, 8, 22, 4.67))]


@C("heavy-lift-ship", "Low flat-decked semi-submersible ship carrying a smaller boat high on its deck",
   ["semi-submersible", "heavy lift vessel", "heavy transport ship", "cargo", "yacht transport", "project cargo"])
def _(S):
    ship = union(poly([(2, 15), (21.5, 15), (20, 18), (3.5, 18)], closed=True, r=S.r * 0.6), rect(18.5, 7, 3, 8.5))
    cargo = union(poly([(3, 9), (15.5, 9), (14, 12.5), (4.5, 12.5)], closed=True, r=S.r * 0.6), rect(6, 5.5, 5, 4))
    return [shell(ship), sq(19.25, 8.5, 1.5, 2, L(S, 0, 0.7)), shell(cargo), line(wave(21, 2, 22))]


@C("drillship", "Drilling ship with a tall lattice derrick rising from the middle of its deck",
   ["drill ship", "offshore drilling", "oil exploration", "derrick", "deepwater", "rig"])
def _(S):
    body = union(poly([(2, 13), (21.5, 13), (20, 17.5), (3.5, 17.5)], closed=True, r=S.r),
                 rect(17.5, 8.5, 4, 5, L(S, 0.5, 1.5)), rect(2.5, 9.5, 4, 4))
    return [shell(body), line(poly([(8.5, 13), (11.5, 3.5), (14.5, 13)], r=S.r * 0.5), stroke_miterlimit="2"),
            line(seg(9.7, 9, 13.3, 9)), line(seg(10.7, 5.5, 12.3, 5.5)), line(WAVE)]


@C("icebreaker", "Ship with a heavy sloped bow riding up onto cracked slabs of sea ice",
   ["ice breaker", "polar ship", "arctic", "antarctic", "sea ice", "frozen sea", "expedition"])
def _(S):
    body = union(poly([(2.5, 12), (15.5, 12), (21, 17), (4.5, 17)], closed=True, r=S.r),
                 rect(4.5, 5.5, 6.5, 7, L(S, 0.5, 1.5)))
    return [shell(body), sq(6, 7, 3.5, 2, L(S, 0, 0.8)),
            shell(poly([(12.5, 19.5), (16.5, 19.5), (15.5, 22), (12.5, 22)], closed=True, r=S.r * 0.4)),
            shell(poly([(18.5, 19), (22, 19.5), (22, 22), (17.5, 22)], closed=True, r=S.r * 0.4)),
            line(wave(20.5, 2, 10.5, 4.25))]


@C("hovercraft", "Hovercraft on a puffy rubber skirt with a big ducted fan at the back over a line of spray",
   ["air cushion vehicle", "acv", "hover craft", "amphibious", "ferry", "rescue"])
def _(S):
    body = union(rect(2, 13.5, 20, 5, 2.5 if S.name == "rounded" else 1.5),
                 poly([(9, 14), (10, 9), (18, 9), (21, 13), (21, 14)], closed=True, r=S.r * 0.6))
    return [shell(body), detail(seg(2, 14.5, 22, 14.5)), sq(12, 10.5, 2, 1.5, L(S, 0, 0.7)), sq(15.5, 10.5, 2, 1.5, L(S, 0, 0.7)),
            shell(circle(5, 7.5, 3.5)), dot(5, 7.5, 1), dot(4, 21.5, 1), dot(8, 21.5, 1), dot(12, 21.5, 1), dot(16, 21.5, 1),
            dot(20, 21.5, 1)]


@C("hydrofoil", "Fast boat lifted above the water on angled struts with underwater wings at the surface",
   ["hydrofoil boat", "foil boat", "hydrofoil ferry", "fast ferry", "high speed boat", "hydroplane"])
def _(S):
    body = union(poly([(2.5, 7.5), (18, 7.5), (21.5, 9.5), (19.5, 12), (4, 12)], closed=True, r=S.r),
                 rect(7, 4, 7, 4, L(S, 0.5, 1.5)))
    return [shell(body), sq(9, 5.5, 3, 1.5, L(S, 0, 0.7)), line(seg(6, 12, 7, 19)), line(seg(17.5, 12, 16.5, 19)),
            line(seg(4.5, 19, 9.5, 19)), line(seg(14, 19, 19, 19)), line(wave(16.5, 2, 22))]


@C("houseboat", "Flat boat carrying a small house with a pitched roof, a window and a door",
   ["house boat", "floating home", "canal living", "liveaboard", "floating house", "lake"])
def _(S):
    house = poly([(5.5, 12.5), (5.5, 7.5), (12, 3), (18.5, 7.5), (18.5, 12.5)], closed=True, r=S.r)
    return [shell(house), detail(poly([(9, 12.5), (9, 9), (11.5, 9), (11.5, 12.5)], r=S.r * 0.4)),
            sq(14, 8.5, 2.5, 2, L(S, 0, 0.8)),
            shell(poly([(2, 14.5), (22, 14.5), (20.5, 18), (3.5, 18)], closed=True, r=S.r * 0.6)), line(WAVE)]


@C("narrowboat", "Long narrow canal boat with a low cabin, round portholes and a tiller at the stern",
   ["canal boat", "narrow boat", "barge", "canal", "waterways", "liveaboard", "inland boat"])
def _(S):
    body = union(poly([(4, 14), (21.5, 14), (20.5, 17.5), (5, 17.5)], closed=True, r=S.r * 0.6),
                 rect(6.5, 9.5, 13, 5, L(S, 0.5, 1.5)))
    return [shell(body), dot(9.5, 12, 1.1), dot(13, 12, 1.1), dot(16.5, 12, 1.1),
            line(poly([(5, 14), (5, 10.5), (2, 9)], r=S.r * 0.5)), line(WAVE)]


@C("barge", "Long flat open cargo barge riding low in the water, heaped with sand",
   ["cargo barge", "hopper barge", "river barge", "sand", "gravel", "bulk cargo", "inland shipping"])
def _(S):
    body = union(poly([(2, 14), (22, 14), (20.5, 17.5), (3.5, 17.5)], closed=True, r=S.r * 0.6),
                 "M4 14.5C6 10.5 9 8 12 8S18 10.5 20 14.5Z")
    return [shell(body), detail(seg(2, 14, 22, 14)), line(WAVE)]


@C("solar-boat", "Low flat boat under a canopy roof made of a grid of solar panels on thin posts",
   ["solar powered boat", "electric boat", "solar ferry", "green boat", "eco boat", "renewable energy"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 4, L(S, 0.5, 1.5))), detail(seg(7, 3.5, 7, 7.5)), detail(seg(12, 3.5, 12, 7.5)),
            detail(seg(17, 3.5, 17, 7.5)), line(seg(5, 7.5, 5, 13)), line(seg(19, 7.5, 19, 13)),
            shell(poly([(2, 13), (22, 13), (20.5, 17.5), (3.5, 17.5)], closed=True, r=S.r * 0.6)), line(WAVE)]


# =========================================================================== sailing ships and historic craft

def billow(x, y, w, h):
    """Square sail bellying forward (to the right)."""
    b = w * 0.3
    return f"M{fmt(x)} {fmt(y)}H{fmt(x + w)}Q{fmt(x + w + b)} {fmt(y + h / 2)} {fmt(x + w)} {fmt(y + h)}H{fmt(x)}Q{fmt(x + b)} {fmt(y + h / 2)} {fmt(x)} {fmt(y)}Z"


@C("junk-ship", "Traditional Chinese junk with a high stern and ribbed, fan-like battened sails",
   ["junk", "chinese junk", "sailing ship", "battened sail", "traditional boat", "asia", "harbour"])
def _(S):
    hull = poly([(2, 9), (5, 9.5), (7, 13.5), (21.5, 13.5), (19.5, 17.5), (5.5, 17.5)], closed=True, r=S.r * 0.6)
    main = poly([(8.5, 3), (14, 2), (15.5, 11), (8, 11)], closed=True, r=S.r * 0.4)
    fore = poly([(17, 5), (20, 4.5), (21.5, 11), (17, 11)], closed=True, r=S.r * 0.4)
    return [shell(hull), shell(main), detail(seg(8.3, 5.5, 14.4, 4.5)), detail(seg(8.1, 8.25, 15, 7.5)),
            shell(fore), detail(seg(17, 8, 21, 7.5)), line(WAVE)]


@C("dhow", "Wooden sailing boat with a raked mast and one large triangular lateen sail on a long angled yard",
   ["lateen sail", "arab dhow", "felucca", "sailing boat", "traditional boat", "indian ocean", "red sea"])
def _(S):
    hull = poly([(3, 13.5), (19, 13.5), (21.5, 11), (19, 17.5), (6, 17.5)], closed=True, r=S.r * 0.6)
    sail = poly([(4, 10.5), (19, 2.5), (15.5, 11)], closed=True, r=S.r * 0.4)
    return [shell(hull), shell(sail, stroke_miterlimit="2"), line(seg(2.5, 11.3, 20.5, 1.7)), line(seg(12, 13.5, 11, 8)),
            line(WAVE)]


@C("longship", "Long narrow Norse ship with a curled dragon prow, a striped square sail and a row of round shields",
   ["viking ship", "norse ship", "drakkar", "longboat", "vikings", "history", "saga"])
def _(S):
    hull = ("M2.5 7.5C3 11 4.5 14.5 7 17.5H17C19.5 14.5 21 11 21.5 7.5C20.5 11 18 13.5 15 13.5H9C6 13.5 3.5 11 2.5 7.5Z")
    return [shell(hull), dot(9, 15.5, 1), dot(12, 15.5, 1), dot(15, 15.5, 1),
            dot(21.5, 6, 1.5), dot(2.5, 6, 1.5),
            shell(rect(7, 2.5, 10, 7.5, L(S, 0.5, 1.5))), detail(seg(10.3, 2.5, 10.3, 10)), detail(seg(13.7, 2.5, 13.7, 10)),
            line(seg(12, 10, 12, 13.5)), line(WAVE)]


@C("galleon", "Large wooden sailing ship with a towering stern castle, three masts and billowing square sails",
   ["tall ship", "spanish galleon", "sailing ship", "age of sail", "treasure fleet", "history", "man of war"])
def _(S):
    hull = poly([(2.5, 8), (7, 8), (7, 12.5), (19, 12.5), (21.5, 10.5), (19.5, 17.5), (5, 17.5)], closed=True, r=S.r * 0.6)
    return [shell(hull), dot(9.5, 15, 1), dot(13, 15, 1), dot(16.5, 15, 1),
            shell(billow(9, 2.5, 3.5, 7.5)), shell(billow(15.5, 4, 3, 6)), line(seg(10.75, 10, 10.75, 12.5)),
            line(seg(17, 10, 17, 12.5)), line(seg(4.5, 8, 4.5, 3)), line(seg(4.5, 3, 7, 4)), line(WAVE)]


@C("pirate-ship", "Wooden sailing ship with square sails and a skull and crossbones flag at the masthead",
   ["pirates", "buccaneer", "jolly roger", "sailing ship", "treasure", "adventure", "caribbean"])
def _(S):
    hull = poly([(2.5, 12), (21.5, 12), (19, 17.5), (5, 17.5)], closed=True, r=S.r * 0.6)
    return [shell(hull), shell(billow(4.5, 5.5, 5, 5)), shell(billow(13, 6.5, 4, 4)),
            line(seg(7, 10.5, 7, 12)), line(seg(15, 10.5, 15, 12)), line(seg(15, 6.5, 15, 2)),
            shell(rect(15, 1.5, 6.5, 4.5, L(S, 0.01, 1))), detail(seg(16.5, 3, 20, 4.5)), detail(seg(16.5, 4.5, 20, 3)),
            line(WAVE)]


@C("clipper-ship", "Sleek three-masted sailing ship with stacks of square sails and a long pointed bowsprit",
   ["clipper", "tall ship", "tea clipper", "sailing ship", "windjammer", "age of sail", "fast ship"])
def _(S):
    hull = poly([(2.5, 13.5), (19.5, 13.5), (17.5, 17.5), (4, 17.5)], closed=True, r=S.r * 0.6)
    parts = [shell(hull), line(seg(19.5, 13.5, 22.5, 10.5))]
    for x, top in ((3, 5.5), (9, 2.5), (15, 4.5)):
        parts += [shell(poly([(x, 11.5), (x + 4, 11.5), (x + 3, top), (x + 1, top)], closed=True, r=S.r * 0.3)),
                  detail(seg(x, (top + 11.5) / 2 + 0.5, x + 4, (top + 11.5) / 2 + 0.5))]
    return parts + [line(WAVE)]


@C("schooner", "Two-masted sailing ship with large fore-and-aft gaff sails and a triangular jib at the bow",
   ["gaff rigged", "sailing ship", "yacht", "fore and aft rig", "tall ship", "sailing"])
def _(S):
    hull = poly([(3, 13.5), (20, 13.5), (21.5, 12), (19, 17.5), (5, 17.5)], closed=True, r=S.r * 0.6)
    main = poly([(11, 4), (11, 11.5), (3.5, 11.5), (5.5, 2.5)], closed=True, r=S.r * 0.4)
    fore = poly([(16, 5), (16, 11.5), (13, 11.5), (13.5, 4.5)], closed=True, r=S.r * 0.4)
    jib = poly([(18, 4), (21.5, 11.5), (18, 11.5)], closed=True, r=S.r * 0.4)
    return [shell(hull), shell(main), shell(fore), shell(jib, stroke_miterlimit="2"), line(WAVE)]


@C("oared-galley", "Ancient warship with a single square sail and a long row of oars sweeping down into the water",
   ["galley", "trireme", "bireme", "rowing ship", "ancient ship", "roman ship", "greek ship"])
def _(S):
    hull = poly([(2.5, 10), (5, 12), (19, 12), (22, 14.5), (19, 15.5), (5, 15.5)], closed=True, r=S.r * 0.5)
    parts = [shell(hull), shell(billow(8, 3, 7, 6)), line(seg(7, 2.5, 17, 2.5)), line(seg(12, 9, 12, 12))]
    for x in (7, 10.5, 14, 17.5):
        parts.append(line(seg(x, 15.5, x - 3, 20.5)))
    return parts


@C("warship", "Grey naval ship with a sloped bow, stepped superstructure, a mast and gun turrets fore and aft",
   ["navy", "destroyer", "frigate", "battleship", "naval vessel", "military", "cruiser"])
def _(S):
    body = union(poly([(2, 13), (19, 13), (22, 10.5), (19.5, 17.5), (3.5, 17.5)], closed=True, r=S.r * 0.6),
                 rect(8, 9, 7, 4.5), rect(10, 6, 3.5, 3.5))
    return [shell(body), line(seg(11.75, 6, 11.75, 2)), line(seg(10, 3.5, 13.5, 3.5)),
            shell(rect(4, 10.5, 2.5, 2.5)), line(seg(4, 11.5, 2, 11.5)),
            shell(rect(16.5, 10.5, 2.5, 2.5)), line(seg(19, 11.5, 21.5, 10)), line(WAVE)]


@C("aircraft-carrier", "Large ship with a long flat flight deck, an island tower and small jets parked on deck",
   ["carrier", "flattop", "navy", "flight deck", "naval aviation", "military", "warship"])
def _(S):
    body = union(rect(2, 12.5, 20, 2), poly([(4, 13), (21, 13), (19, 17.5), (5.5, 17.5)], closed=True),
                 rect(14, 7, 4, 6))
    jet = lambda x: solid(f"M{x} 11.5V8.5L{x + 1.2} 10.3H{x + 4}L{x + 4.5} 11.5Z")
    return [shell(body), sq(15, 8.5, 2, 1.5, L(S, 0, 0.7)), line(seg(16, 7, 16, 3.5)), jet(3), jet(8.5), line(WAVE)]


@C("landing-craft", "Flat-bottomed boxy boat with its front ramp lowered onto a beach",
   ["landing ship", "amphibious assault", "beach landing", "military", "ferry", "barge"])
def _(S):
    body = union(rect(2.5, 9.5, 12, 7, L(S, 0.5, 1.5)), rect(3.5, 5, 4, 5))
    return [shell(body), detail(seg(2.5, 12, 14.5, 12)), sq(4.5, 6.5, 2, 1.5, L(S, 0, 0.7)),
            line(seg(14.5, 16, 20.5, 18.2)), line(seg(12.5, 21.5, 22, 17.5)), line(wave(20.5, 2, 11, 4.5))]


@C("patrol-boat", "Fast patrol boat with a raised wheelhouse, a radar mast and a diagonal stripe on the hull",
   ["coast guard", "police boat", "patrol vessel", "border patrol", "rescue boat", "navy"])
def _(S):
    body = union(poly([(2.5, 12.5), (21.5, 12.5), (18, 17.5), (4, 17.5)], closed=True, r=S.r * 0.6),
                 poly([(7, 13), (7, 7.5), (14, 7.5), (16.5, 13)], closed=True, r=S.r * 0.6))
    return [shell(body), sq(9, 9, 2, 2, L(S, 0, 0.8)), sq(12, 9, 2, 2, L(S, 0, 0.8)),
            line(seg(10.5, 7.5, 10.5, 3)), line(seg(8.5, 4, 12.5, 4)),
            detail(seg(13.5, 17.5, 16.5, 12.5)), detail(seg(16.5, 17.5, 19.5, 12.5)), line(WAVE)]


@C("fireboat", "Fireboat with water cannons on deck shooting high arcs of water",
   ["fire boat", "firefighting boat", "water cannon", "harbour fire", "marine firefighting", "celebration spray"])
def _(S):
    body = union(poly([(2.5, 14), (21.5, 14), (19.5, 18), (4.5, 18)], closed=True, r=S.r * 0.6),
                 rect(9.5, 10, 5.5, 4.5, L(S, 0.5, 1.5)))
    return [shell(body), sq(11, 11.5, 2.5, 1.5, L(S, 0, 0.7)),
            line("M13.5 10C15 4 19.5 2 21.5 8"), line("M11 10C9.5 4 5 2 3 8"), dot(21.5, 11, 1), dot(3, 11, 1),
            line(WAVE)]


@C("gondola-boat", "Long slim gondola with an upswept toothed prow and a gondolier at the stern holding a long oar",
   ["gondola", "gondolier", "venice", "canal", "romantic", "italy", "boat ride"])
def _(S):
    hull = "M2 13C4 15.5 6.5 16.5 10 16.5H15.5C18 16.5 19.5 14.5 19.5 12V6H21V12.5C21 16 18.5 18.5 15.5 18.5H10C6 18.5 3.5 17 2 13Z"
    return [shell(hull), line(seg(21, 8, 22.5, 8)), line(seg(21, 11, 22.5, 11)),
            dot(6.5, 3.5, 1.75), line(seg(6.5, 6, 6.5, 14)), line(seg(4.5, 7, 12, 21.5)), line(wave(21, 14, 22, 4))]


@C("log-raft", "Raft of lashed logs with a small mast and a square sail",
   ["raft", "log boat", "kon-tiki", "castaway", "survival", "adventure", "balsa raft"])
def _(S):
    logs = union(*[circle(x, 16, 2) for x in (4, 8, 12, 16, 20)])
    return [shell(rect(6, 3, 10, 7, L(S, 0.5, 1.5))), line(seg(11, 10, 11, 14)), shell(logs),
            detail(seg(2, 16, 22, 16)) if S.name == "rounded" else detail(seg(2.5, 16, 21.5, 16)), line(wave(21, 2, 22))]


# =========================================================================== small boats and river craft

@C("whitewater-raft", "Inflatable rubber raft with paddlers bouncing over waves, paddles out on both sides",
   ["rafting", "white water", "river rafting", "inflatable raft", "rapids", "adventure", "outdoor"])
def _(S):
    tube = rot(rect(3.5, 12, 17, 5, 2.5 if S.name == "rounded" else 1.5), -8, 12, 14.5)
    return [shell(tube), dot(9, 8.5, 1.75), dot(15, 7.5, 1.75), line(seg(7.5, 9, 3, 19)), line(seg(16.5, 8.5, 21, 18)),
            line(wave(20.8, 5, 18, 4.33))]


@C("life-raft", "Round inflatable rescue raft with a tent-like canopy and an entrance flap, floating on the water",
   ["liferaft", "survival raft", "inflatable raft", "abandon ship", "sea survival", "emergency", "marine safety"])
def _(S):
    body = union(rect(2.5, 13, 19, 5, 2.5 if S.name == "rounded" else 1.5), "M5.5 13.5C5.5 8 8.5 4.5 12 4.5S18.5 8 18.5 13.5Z")
    return [shell(body), detail(seg(2.5, 14, 21.5, 14)), detail(poly([(10, 14), (10, 10.5), (14, 10.5), (14, 14)], r=S.r * 0.5)),
            line(WAVE)]


@C("lifeboat", "Enclosed rescue lifeboat with a rounded covered roof, small windows and a hatch on top",
   ["enclosed lifeboat", "survival craft", "rescue boat", "ship lifeboat", "abandon ship", "marine safety"])
def _(S):
    body = union(poly([(2.5, 12.5), (21.5, 12.5), (19.5, 17.5), (4.5, 17.5)], closed=True, r=S.r * 0.6),
                 "M4 13C4 9.5 6 7.5 9 7.5H15C18 7.5 20.5 9.5 20.5 13Z", rect(11, 4.5, 3, 3.5))
    return [shell(body), detail(seg(2.5, 13.5, 21.5, 13.5)), dot(7.5, 10.5, 1), dot(11, 10.5, 1), dot(14.5, 10.5, 1),
            dot(18, 10.5, 1), line(WAVE)]


@C("pedalo", "Swan-shaped pedal boat with a curved neck at the front and two seats inside",
   ["pedal boat", "paddle boat", "swan boat", "lake", "park", "leisure", "boating"])
def _(S):
    body = poly([(2.5, 9.5), (5, 12.5), (17, 12.5), (19.5, 14), (18, 17.5), (5, 17.5)], closed=True, r=S.r * 0.6)
    return [shell(body), line("M17.5 12.5C21 10.5 21 7 18.5 5"), dot(17.5, 4.5, 1.75), line(seg(18.5, 4, 21.5, 5)),
            line(seg(8.5, 12.5, 7.5, 8.5)), line(seg(13, 12.5, 12, 8.5)), line(WAVE)]


@C("paddle-steamer", "Steamboat with a big paddle wheel in a half-round housing on its side and two tall funnels",
   ["paddle boat", "side wheeler", "steamboat", "paddle wheel", "heritage boat", "lake steamer", "river cruise"])
def _(S):
    body = union(poly([(2.5, 14), (21.5, 14), (19.5, 18), (4.5, 18)], closed=True, r=S.r * 0.6),
                 "M10 14.5A5.25 5.25 0 0 1 20.5 14.5Z")
    return [shell(body), detail(seg(15.25, 14, 15.25, 10.5)), detail(seg(15.25, 14, 12, 11.5)), detail(seg(15.25, 14, 18.5, 11.5)),
            line(seg(4.5, 14, 4.5, 4)), line(seg(8, 14, 8, 4)), line(WAVE)]


@C("sternwheeler", "Flat riverboat with two tall thin smokestacks, stacked decks and a big paddle wheel at the stern",
   ["stern wheeler", "riverboat", "showboat", "mississippi steamboat", "paddle wheel", "river cruise", "steamboat"])
def _(S):
    body = union(poly([(10.5, 14.5), (21.5, 14.5), (20.5, 17.5), (10.5, 17.5)], closed=True, r=S.r * 0.4),
                 rect(11, 10.5, 10, 4.5), rect(12.5, 7, 7, 4))
    return [shell(body), detail(seg(11, 14.5, 21, 14.5)), detail(seg(11, 10.5, 21, 10.5)),
            line(seg(15, 7, 15, 2)), line(seg(18, 7, 18, 2)),
            shell(circle(5.5, 13.5, 3.75)), detail(seg(2.5, 13.5, 8.5, 13.5)) if S.name == "rounded" else dot(5.5, 13.5, 1.25),
            line(wave(20.5, 2, 22))]


@C("trimaran", "Sailboat seen from the front with a central hull and two slim outer hulls joined by beams, under a tall sail",
   ["multihull", "tri hull", "racing yacht", "sailing", "outrigger", "catamaran"])
def _(S):
    return [line(seg(12, 2.5, 12, 15)), shell(poly([(12.5, 3), (19, 12.5), (12.5, 12.5)], closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
            line("M3 16.5Q12 13 21 16.5"),
            shell(poly([(9.5, 15), (14.5, 15), (12, 19.5)], closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
            shell(poly([(2, 17), (5, 17), (3.5, 19.5)], closed=True, r=S.r * 0.3)), shell(poly([(19, 17), (22, 17), (20.5, 19.5)], closed=True, r=S.r * 0.3)),
            line(wave(22, 2, 22))]


@C("outrigger-canoe", "Narrow canoe seen from above with a single float held parallel to it on two curved crossbeams",
   ["outrigger", "va'a", "waka ama", "polynesian canoe", "paddling", "pacific", "canoe"])
def _(S):
    canoe = "M7.5 2Q12 12 7.5 22Q3 12 7.5 2Z" if S.name != "rounded" else "M7.5 3C10.5 6 10.5 18 7.5 21C4.5 18 4.5 6 7.5 3Z"
    return [shell(canoe, stroke_miterlimit="2"), dot(7.5, 8.5, 1.1), dot(7.5, 12, 1.1), dot(7.5, 15.5, 1.1),
            shell("M19.5 7Q21 12 19.5 17Q18 12 19.5 7Z", stroke_miterlimit="2"),
            line(seg(10.5, 9, 18.5, 9)), line(seg(10.5, 15, 18.5, 15))]


@C("coracle", "Small round bowl-shaped boat with a single paddle resting over the rim",
   ["round boat", "basket boat", "wicker boat", "traditional boat", "river", "fishing"])
def _(S):
    bowl = "M3 10.5H21C21 15 17 18 12 18S3 15 3 10.5Z"
    blade = place(ellipse(0, 0, 3, 1.5) if S.name == "rounded" else poly([(-3, 0), (0, -1.5), (3, 0), (0, 1.5)], closed=True), 40, 5, 4.5)
    return [shell(bowl), detail("M8 10.5C8 13.5 9 16 10.5 17.5"), detail("M16 10.5C16 13.5 15 16 13.5 17.5"),
            shell(blade), line(seg(7, 6.2, 12.5, 10.5)), line(wave(21, 2, 22))]


@C("dragon-boat", "Long narrow boat with a dragon head at the prow, a curled tail at the stern and a row of paddlers",
   ["dragon boat racing", "duanwu", "dragon boat festival", "paddling", "team sport", "racing", "chinese festival"])
def _(S):
    body = union(poly([(4, 13), (18.5, 13), (17.5, 16), (5, 16)], closed=True, r=S.r * 0.4),
                 poly([(17.5, 13.5), (19, 7.5), (21.5, 7.5), (22, 10), (20.5, 10.5), (20, 13.5)], closed=True, r=S.r * 0.4))
    parts = [shell(body), line("M4.5 13C2.5 12.5 2 10.5 3 9.5S5.5 9.5 5 11")]
    for x in (7.5, 11, 14.5):
        parts += [dot(x, 10.5, 1.3), line(seg(x + 1, 16, x - 1.5, 20.5))]
    return parts


@C("longtail-boat", "Slim wooden boat with an upswept prow and an engine on a very long propeller shaft at the stern",
   ["long tail boat", "thai boat", "river taxi", "longtail", "southeast asia", "island hopping", "boat"])
def _(S):
    hull = "M9 12.5H17C19.5 12.5 21 10.5 21.5 6.5H22.5C22.5 12.5 20.5 16.5 16.5 16.5H10.5Z"
    return [shell(hull, stroke_miterlimit="2"), shell(rect(6, 7.5, 4, 3, L(S, 0.5, 1.2))), line(seg(8, 10.5, 2.5, 19)), dot(2.5, 19.5, 1.6),
            line(wave(20.5, 8, 22, 4.67))]


@C("reed-boat", "Boat made of bundled reeds curving up sharply at both ends and tied with bands",
   ["reed raft", "totora boat", "papyrus boat", "balsa", "lake titicaca", "traditional boat", "ancient"])
def _(S):
    hull = "M2 5C3 12 6.5 16.5 12 16.5S21 12 22 5C20.5 10 17 12.5 12 12.5S3.5 10 2 5Z"
    return [shell(hull), detail(seg(7, 11, 5.5, 14.5)), detail(seg(12, 12.5, 12, 16.5)), detail(seg(17, 11, 18.5, 14.5)),
            line(wave(20.5, 2, 22))]


@C("sampan", "Small flat wooden boat with an arched canopy over the middle and a long stern oar",
   ["sampan boat", "river boat", "chinese boat", "fishing boat", "water taxi", "traditional boat", "asia"])
def _(S):
    body = union(poly([(4.5, 13), (19.5, 13), (21.5, 11), (19.5, 17.5), (6, 17.5)], closed=True, r=S.r * 0.6),
                 "M8 13.5C8 8.5 10 6.5 13 6.5S18 8.5 18 13.5Z")
    return [shell(body), detail(seg(8, 13, 18, 13)), detail("M11 13V10.5A2 2 0 0 1 15 10.5V13"),
            line(seg(6.5, 13, 2.5, 21))]


@C("punt-boat", "Flat square-ended boat with a person standing at the back pushing a long pole into the water",
   ["punt", "punting", "pole boat", "river", "oxford", "cambridge", "leisure"])
def _(S):
    return [shell(rect(3, 14.5, 19, 3, L(S, 0.3, 1.25))), dot(7.5, 4, 1.75),
            line(poly([(7.5, 6.5), (7.5, 11), (6, 14.5)], r=S.r * 0.4)), line(seg(7.5, 11, 9, 14.5)),
            line(seg(7.5, 8, 5, 9.5)), line(seg(3.5, 2.5, 5, 21.5)), line(wave(20.5, 8, 22, 4.67))]


@C("airboat", "Flat-bottomed swamp boat with a big caged propeller fan mounted upright at the back",
   ["swamp boat", "fanboat", "everglades", "wetlands", "bayou", "airboat tour", "fan boat"])
def _(S):
    return [shell(circle(7, 7.5, 5)), detail(seg(7, 2.5, 7, 12.5)), detail(seg(2, 7.5, 12, 7.5)),
            line(seg(7, 12.5, 7, 14)), line(poly([(15, 14), (15, 9.5), (17.5, 9.5)], r=S.r * 0.4)),
            shell(poly([(2.5, 14), (21.5, 14), (20, 17.5), (3, 17.5)], closed=True, r=S.r * 0.6)), line(WAVE)]



@C("rowing-scull", "Very long narrow racing shell with a rower and long thin oars reaching out over the water",
   ["rowing boat", "racing shell", "single scull", "rowing", "crew", "regatta", "sculling", "sport"])
def _(S):
    hull = poly([(2, 15), (22, 15), (20, 17.5), (4, 17.5)], closed=True, r=S.r * 0.3)
    return [shell(hull), dot(9, 4, 1.7),
            line(poly([(9, 6.5), (8, 11), (12.5, 11.5)], r=S.r * 0.5)), line(seg(9, 7.5, 14, 8)),
            line(seg(10, 5, 19, 19.5)), line(wave(20.5, 2, 22))]


@C("iceboat", "Sailboat frame with a triangular sail sitting on skate runners on flat ice",
   ["ice yacht", "ice sailing", "ice skate boat", "winter sailing", "frozen lake", "runner sled", "winter sport"])
def _(S):
    return [line(seg(11, 2.5, 11, 13.5)),
            shell(poly([(11.5, 3.5), (11.5, 11), (19, 11)], closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
            shell(rect(4.5, 13, 15, 2.5, L(S, 0.3, 1.25))),
            line(seg(7, 15.5, 7, 18.5)), line(seg(17.5, 15.5, 17.5, 18.5)),
            line(seg(3, 19, 11, 19)), line(poly([(13.5, 19), (20, 19), (22, 17)], r=S.r * 0.3))]


@C("pontoon-boat", "Flat deck boat resting on a long tube float, with a canopy and railings on deck",
   ["pontoon", "party barge", "deck boat", "lake boat", "leisure boat", "tritoon", "canopy boat"])
def _(S):
    return [shell(rect(2.5, 14.5, 19, 3, L(S, 1.5, 1.5))), shell(rect(3, 3, 18, 3, L(S, 0.5, 1.5))),
            line(seg(5, 6, 5, 14.5)), line(seg(19, 6, 19, 14.5)), line(seg(12, 6, 12, 14.5)),
            line(seg(5, 10.5, 19, 10.5)), line(wave(20.5, 2, 22))]


@C("glass-bottom-boat", "Boat with a window panel in its hull and a small fish swimming in view below",
   ["glass bottom boat", "reef tour", "snorkel tour", "underwater viewing", "sightseeing boat", "coral reef", "tour boat"])
def _(S):
    hull = union(poly([(3, 7), (21, 7), (18.5, 12.5), (5.5, 12.5)], closed=True, r=S.r * 0.6), rect(8, 3, 8, 4.5, L(S, 0.5, 1.5)))
    fish = solid(union(ellipse(10, 19.5, 3.5, 2.2), poly([(12.5, 19.5), (16, 17.5), (16, 21.5)], closed=True)))
    return [shell(hull), sq(9.5, 8.75, 5, 1.75, L(S, 0, 0.8)), line(wave(15.5, 2, 22)), fish]


@C("parasail", "Motorboat on the water towing a line up to a person hanging under a wide round parasail canopy",
   ["parasailing", "paraflying", "towed parachute", "beach activity", "water sport", "sea adventure", "tow rope"])
def _(S):
    canopy = "M2.5 8C2.5 4 6 2.5 10 2.5S17.5 4 17.5 8Z"
    boat = poly([(14, 16), (22, 16), (20, 19), (16, 19)], closed=True, r=S.r * 0.5)
    return [shell(canopy), line(seg(5, 8, 10, 12.5)), line(seg(15, 8, 10, 12.5)), dot(10, 14.5, 1.6),
            line(seg(11, 15, 15, 16)), shell(boat), line(wave(21.5, 2, 22))]


@C("windsurf-board", "Surfboard with a mast and a tall curved triangular sail attached at its middle",
   ["windsurfing", "sailboard", "board sailing", "water sport", "sail", "wind sport", "beach sport"])
def _(S):
    board = "M2.5 16Q12 18.5 21.5 15Q12 13.5 2.5 16Z" if S.name != "rounded" else "M3.5 16Q12 18.5 20.5 15.2Q12 13.5 3.5 16Z"
    return [line(seg(11, 15.5, 14, 2.5)), shell("M14 3.5C8 6 6 11 7 14.3H11.4Z", stroke_miterlimit="2"),
            shell(board, stroke_miterlimit="2"), line(wave(21, 2, 22))]
@C("paddleboard", "Long flat stand-up paddleboard seen from the side with a single-blade paddle standing upright beside it",
   ["sup", "stand up paddle board", "paddle boarding", "water sport", "lake", "surf paddle", "sup board"])
def _(S):
    board = poly([(3, 15.5), (14, 15.5), (16.5, 17.5), (3, 17.5)], closed=True, r=S.r * 0.3)
    blade = poly([(17.75, 9), (21.25, 9), (20.5, 18), (18.5, 18)], closed=True, r=S.r * 0.6)
    return [shell(board), line(seg(17.5, 2.5, 21.5, 2.5)), line(seg(19.5, 2.5, 19.5, 9)), shell(blade), line(wave(20.5, 2, 22))]
@C("foil-board", "Board lifted above the water on a tall thin mast ending in a small underwater wing",
   ["hydrofoil board", "foil surfing", "wing foil", "efoil", "kite foil", "water sport", "hydrofoiling"])
def _(S):
    board = "M2.5 6Q12 8 21.5 5Q12 3.5 2.5 6Z" if S.name != "rounded" else "M3.5 6Q12 8 20.5 5.2Q12 3.5 3.5 6Z"
    wing = "M11 19.5Q16 17 21.5 19.5Q16 22 11 19.5Z" if S.name != "rounded" else "M11.5 19.5Q16 17.3 21 19.5Q16 21.7 11.5 19.5Z"
    return [shell(board, stroke_miterlimit="2"), line(seg(14.5, 6.5, 14.5, 19)), line(seg(14.5, 19.5, 3, 19.5)),
            shell(wing, stroke_miterlimit="2"), line(wave(12, 2, 22, 5, 1))]
@C("diving-bell", "Open-bottomed bell-shaped chamber with a small round window, lowered on a cable below the water surface",
   ["bathysphere", "underwater chamber", "submersible", "deep sea", "diving chamber", "salvage", "ocean exploration"])
def _(S):
    bell = "M4.5 19.5V14.5C4.5 10 7.5 7 12 7S19.5 10 19.5 14.5V19.5H16.5V16.5H7.5V19.5Z"
    return [line(seg(12, 2, 12, 7)), shell(bell), detail(circle(12, 11.5, 1.8)), line(wave(4.5, 2, 22, 4, 0.8))]


@C("underwater-scooter", "Diver-held torpedo-shaped propulsion unit with a caged propeller at the back and a grip handle",
   ["diver propulsion vehicle", "sea scooter", "dpv", "underwater propulsion", "snorkel scooter", "scuba", "water toy"])
def _(S):
    body = "M8 8H17C20 8 21.5 10 21.5 11S20 14 17 14H8Z" if S.name != "rounded" else "M9.5 8H17C20 8 21.5 10 21.5 11S20 14 17 14H9.5Q8 14 8 12.5V9.5Q8 8 9.5 8Z"
    return [shell(body), shell(ellipse(4.5, 11, 2.25, 4.5)), line(seg(4.5, 6.5, 4.5, 15.5)),
            line(poly([(11, 14), (11, 18.5), (18, 18.5), (18, 14)], r=S.r * 0.5)),
            dot(2.5, 19, 1), dot(5, 21, 1)]


@C("diving-helmet", "Round brass deep-sea diving helmet with a round front window, a bolted collar and an air hose fitting",
   ["deep sea diver", "brass helmet", "antique diving helmet", "scuba", "underwater work", "salvage diver", "air hose"])
def _(S):
    k = L(S, 0.5, 1.5)
    body = union(circle(10.5, 9, 6.5), circle(16.5, 9.5, 4.5), rect(5, 13, 12, 7, k), rect(2, 7, 3.5, 4, L(S, 0.3, 1)))
    return [shell(body), detail(circle(16.5, 9.5, 1.8)), detail(seg(5, 16, 17, 16)), line("M3.75 11V15Q3.75 20 8 20")]


@C("man-overboard", "Person in the water with raised arms calling for help next to a floating life ring",
   ["person in water", "overboard", "drowning", "water rescue", "help at sea", "emergency", "life ring"])
def _(S):
    return [dot(8, 10, 1.8), line(seg(5, 14, 2.5, 5)), line(seg(11, 14, 13.5, 5)),
            shell(circle(18, 14, 4)), detail(circle(18, 14, 1.4)) if S.name != "rounded" else dot(18, 14, 1.4),
            line(wave(16.5, 2, 13, 4.33, 1))]


@C("ship-wheel", "Wooden ship steering wheel with eight spokes ending in round handles around a central hub",
   ["helm", "ship's wheel", "steering wheel", "captain", "nautical", "sailing", "boat wheel", "yacht helm"])
def _(S):
    parts = [shell(circle(12, 12, 5.5)), detail(circle(12, 12, 1.6)) if S.name != "rounded" else dot(12, 12, 1.6)]
    for k in range(8):
        a = k * 45
        x1, y1 = pt_on(12, 12, 5.5, a)
        x2, y2 = pt_on(12, 12, 8.3, a)
        x3, y3 = pt_on(12, 12, 8.6, a)
        parts += [line(seg(x1, y1, x2, y2)), dot(x3, y3, 1.5)]
    return parts


@C("porthole", "Round ship window with a thick bolted metal rim and a glass pane showing a small wave inside",
   ["ship window", "round window", "boat window", "cabin window", "nautical window", "cruise cabin", "bulkhead window"])
def _(S):
    parts = [shell(circle(12, 12, 9)), detail(circle(12, 12, 5))]
    for k in range(4):
        x, y = pt_on(12, 12, 7.0, 45 + k * 90)
        parts.append(dot(x, y, 0.9) if S.name == "rounded" else sq(x - 0.8, y - 0.8, 1.6, 1.6))
    return parts + [line(wave(12.5, 9.5, 14.5, 2.5, 0.7))]


@C("life-jacket", "Front view of a buoyant vest with two thick padded front panels, a collar and a buckled strap",
   ["life vest", "pfd", "personal flotation device", "buoyancy vest", "boating safety", "water safety", "flotation jacket"])
def _(S):
    body = poly([(7, 3), (10, 3), (12, 5.5), (14, 3), (17, 3), (17.5, 8), (19.5, 9.5), (19.5, 20), (4.5, 20), (4.5, 9.5), (6.5, 8)],
                closed=True, r=S.r * 0.5)
    return [shell(body), detail(seg(12, 5.5, 12, 11)), detail(seg(12, 16.5, 12, 20)),
            detail(seg(4.5, 14, 19.5, 14)), sq(10.5, 12.5, 3, 3, L(S, 0, 0.8))]
@C("rudder", "Boat stern with a flat blade rudder hinged below the waterline and a tiller arm on deck",
   ["boat rudder", "steering", "tiller", "helm", "sailing", "stern", "boat steering gear"])
def _(S):
    hull = poly([(2.5, 9), (15.5, 9), (15.5, 13.5), (5, 13.5)], closed=True, r=S.r * 0.6)
    blade = rect(17.5, 13, 4, 8, L(S, 0.5, 1.5))
    return [shell(hull), line(seg(19.5, 4, 19.5, 13)), line(seg(19.5, 4, 12, 4)), shell(blade), line(wave(16.5, 2, 15.5, 4.5, 0.9))]


@C("ship-bell", "Brass ship bell hanging from a bracket with a knotted rope tied to the clapper",
   ["bell", "brass bell", "nautical bell", "ships bell", "watch bell", "sailing", "marine", "boat bell"])
def _(S):
    bell = "M5.5 15.5C7 14.5 7.5 13 7.5 10.5C7.5 7.5 9.5 5.5 12 5.5S16.5 7.5 16.5 10.5C16.5 13 17 14.5 18.5 15.5Z"
    return [line(seg(4.5, 3, 19.5, 3)), line(seg(12, 3, 12, 5.5)), shell(bell), dot(12, 18.5, 1.4), dot(12, 21.3, 0.8)]


@C("crows-nest", "Top of a ship mast with a round lookout barrel near the tip, rope rigging below and a small flag above",
   ["crow's nest", "lookout", "mast top", "masthead", "sailing ship", "pirate", "watch tower at sea", "barrel"])
def _(S):
    barrel = poly([(5.5, 9), (18.5, 9), (17, 15), (7, 15)], closed=True, r=S.r * 0.4)
    flag = poly([(12, 2.5), (19, 4.5), (12, 6.5)], closed=True, r=S.r * 0.3)
    return [shell(flag, stroke_miterlimit="2"), line(seg(12, 2.5, 12, 9)), shell(barrel), detail(seg(6.3, 12, 17.7, 12)),
            line(seg(12, 15, 12, 22)), line(seg(8, 15, 4.5, 21.5)), line(seg(16, 15, 19.5, 21.5))]


@C("ship-funnel", "Tall ship smokestack with two horizontal bands and a puff of smoke rising from the top",
   ["smokestack", "ship chimney", "steamship", "cruise ship", "exhaust stack", "steamer", "marine funnel"])
def _(S):
    body = union(poly([(8, 9.5), (16, 9.5), (17.5, 21), (6.5, 21)], closed=True, r=S.r * 0.4), rect(7, 7.5, 10, 3, L(S, 0.3, 1.25)))
    return [shell(body), detail(seg(7.2, 14, 16.8, 14)), detail(seg(6.9, 17.5, 17.1, 17.5)),
            dot(10, 4, 1.8), dot(14, 3.5, 1.5), dot(17.5, 4.5, 1)]
@C("outboard-motor", "Outboard boat engine with a rounded cowling on top, a long shaft and a propeller at the bottom",
   ["boat engine", "outboard engine", "marine motor", "boat motor", "propeller", "dinghy motor", "fishing boat engine"])
def _(S):
    k = L(S, 0.5, 1.75)
    body = union("M6.5 10.5V7C6.5 4.3 8.5 2.5 11 2.5H14C16.3 2.5 18 4.3 18 7V10.5Z", rect(9.5, 10, 5.5, 7, 0), rect(8, 15.5, 11, 4, k))
    return [shell(body), line(seg(4.5, 14, 4.5, 21)), line(seg(4.5, 17.5, 8, 17.5)),
            line(poly([(18, 6), (21.5, 6), (21.5, 15)], r=S.r * 0.3))]


@C("oar", "Single wooden rowing oar drawn diagonally with a grip at one end and a flat blade at the other",
   ["paddle", "rowing oar", "row boat", "rowing", "boating", "canoe paddle", "sweep oar", "water sport"])
def _(S):
    blade = place(rect(0, -3, 9, 6, L(S, 0.5, 2.5)), 45, 11.5, 11.5)
    grip = place(rect(0, -1.5, 4.5, 3, L(S, 0.3, 1.5)), 45, 2.8, 2.8)
    return [shell(grip), line(seg(6, 6, 12, 12)), shell(blade)]
