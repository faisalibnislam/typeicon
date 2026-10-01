"""TypeIcon Core: emergency (batch 001).

Fire service, wildland and technical-rescue equipment, buildings, scenes and people, drawn from the objects
themselves. Closed silhouettes are shells, inner lines are details, small solid marks stay solid in Line/Rounded
and are knocked out of Filled shells. Long tools are designed upright and turned with `rotd`/`rpts`.
Figures follow the stick-figure style of sets/activities_002.py (solid head r 2.25 over 2 px limbs).
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "emergency"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def grow(d, g):
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def cut(back, front, g=3.5):
    """Back region with the front region (grown by g) removed, leaving a clear gap."""
    return minus(back, grow(front, g))


def mark(d):
    return Part("dot", d)


def rotd(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpts(pts, deg, dx=0.0, dy=0.0, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s + dx, cy + (x - cx) * s + (y - cy) * c + dy) for x, y in pts]


def rseg(x1, y1, x2, y2, deg, dx=0.0, dy=0.0):
    (a, b), (c, d) = rpts([(x1, y1), (x2, y2)], deg, dx, dy)
    return seg(a, b, c, d)


def rpath(d, deg, dx=0.0, dy=0.0):
    """Rotate a closed path string about the centre, then shift it."""
    m = rotation(deg)
    return path_to_d(transform_path(P(d), (m[0], m[1], m[2], m[3], m[4] + dx, m[5] + dy)))


def flip(d):
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def head(x, y):
    return dot(x, y, 2.25)


def limb(S, *pts):
    return line(poly(pts, r=S.r))


def flame(cx, top, bottom, w, S):
    """Two-tongued flame; pointed tips in Line, softened tips in Rounded."""
    h = bottom - top
    t = L(S, 0.0, 0.07)
    u = [(.5, 1), (.2, 1, 0, .8, 0, .58), (0, .38, .12, .2, .3, t), (.34, .22, .42, .3, .5, .34),
         (.48, .2, .54, .08, .66, t), (.86, .22, 1, .4, 1, .62), (1, .84, .8, 1, .5, 1)]

    def P_(a, b):
        return f"{fmt(cx + (a - .5) * w)} {fmt(top + b * h)}"
    out = f"M{P_(*u[0])}"
    for c in u[1:]:
        out += "C" + " ".join([P_(c[0], c[1]), P_(c[2], c[3]), P_(c[4], c[5])])
    return out + "Z"


def rr(S, cap):
    return min(S.R, cap)


def heli(S):
    return [line(seg(3, 2.5, 16, 2.5)), line(seg(9.5, 2.5, 9.5, 5.5)), shell(ellipse(9.5, 8.5, 5.5, 3)),
            line(seg(15, 8, 21.5, 5.5))]


# ============================================================================ fire service tools

@icon("firefighter-helmet", CAT, "Side view of a firefighter helmet with a tall front shield and a long rear brim",
      tags=["fire helmet", "fire hat", "fireman", "firefighter", "fire service", "protective"])
def _(S):
    crown = "M6 15C6 8 9 4.5 13 4.5C17 4.5 19 8 19 15Z"
    brim = poly([(2, 20), (5, 15), (21, 15), (22, 19)], closed=True, r=S.r * 0.6)
    return [
        shell(union(crown, brim)),
        detail(seg(5.5, 15, 21, 15)),
        detail("M10 8.5H16V12.5L13 14.5L10 12.5Z"),
    ]


@icon("fire-axe", CAT, "Firefighter's axe with a curved blade on one side and a spike pick on the other",
      tags=["axe", "fireman axe", "forcible entry", "firefighting", "chop", "tool"])
def _(S):
    d, dx, dy = 45, 0.5, 1.5
    head = "M5.5 3L10 5H14L20.5 7.5L14 9.5H10L5.5 12Q3.5 7.5 5.5 3Z"
    return [
        shell(rpath(head, d, dx, dy), stroke_miterlimit="3"),
        line(rseg(12, 9.5, 12, 21.5, d, dx, dy)),
    ]


@icon("halligan-bar", CAT, "Long forcible-entry bar with a fork at one end and an adze blade and pick at the other",
      tags=["halligan", "forcible entry", "pry bar", "fire tool", "firefighter", "breaking in"])
def _(S):
    d, dx, dy = 45, 0.5, 1.5
    top = rpts([(5, 3.5), (11, 4.5), (13, 4.5), (20, 6.5), (13, 8), (11, 8), (5, 9.5)], d, dx, dy)
    fork = rpts([(9, 21.5), (12, 14.5), (15, 21.5)], d, dx, dy)
    return [
        shell(poly(top, closed=True, r=S.r * 0.4), stroke_miterlimit="3"),
        line(rseg(12, 8, 12, 15, d, dx, dy)),
        line(poly(fork, r=S.r * 0.4)),
    ]


@icon("pike-pole", CAT, "Long pole with a pointed tip and a curved hook just behind it",
      tags=["fire pole", "ceiling hook", "pull down", "firefighter", "overhaul", "tool"])
def _(S):
    d = 40
    tip = rpts([(12, 2), (14.5, 7), (9.5, 7)], d)
    hook = rpts([(12, 14), (17.5, 14), (17.5, 9.5)], d)
    return [
        shell(poly(tip, closed=True, r=S.r * 0.4), stroke_miterlimit="4"),
        line(rseg(12, 7, 12, 22, d)),
        line(poly(hook, r=S.r)),
    ]


@icon("fire-hose-coupling", CAT, "Two hose couplings facing each other with short hose stubs on the outer sides",
      tags=["hose connector", "hose fitting", "join hose", "hose", "fire service"])
def _(S):
    k = rr(S, 2)
    return [
        line(seg(2, 9, 5, 9)), line(seg(2, 15, 5, 15)),
        line(seg(22, 9, 19, 9)), line(seg(22, 15, 19, 15)),
        shell(rect(5, 6, 5, 12, k)),
        shell(rect(14, 6, 5, 12, k)),
    ]


@icon("rolled-fire-hose", CAT, "Flat fire hose rolled into a spiral disc with a coupling at the centre",
      tags=["hose roll", "hose reel", "coiled hose", "donut roll", "fire hose", "firefighting"])
def _(S):
    sp = "M11 12A1.5 1.5 0 0 1 14 12A3.5 3.5 0 0 1 7 12A5.5 5.5 0 0 1 18 12A7.5 7.5 0 0 1 3 12"
    return [
        line(sp),
        shell(rect(17, 15, 5, 5, rr(S, 1.5))),
    ]


@icon("fire-hose-wye", CAT, "Y-shaped hose fitting with one inlet splitting into two outlets with lever valves",
      tags=["wye", "gated wye", "hose splitter", "hose valve", "fire hose", "fitting"])
def _(S):
    k = rr(S, 1.5)
    return [
        line("M12 18V13L6.5 7"), line("M12 13L17.5 7"),
        shell(rect(9, 18, 6, 3.5, k)),
        shell(rotd(rect(4, 2.5, 5.5, 3, k), -42, 6.75, 4)),
        shell(rotd(rect(14.5, 2.5, 5.5, 3, k), 42, 17.25, 4)),
        line(seg(11, 9.5, 8.5, 12)),
    ]


@icon("fire-hose-spray", CAT, "Fire hose nozzle held level with a wide fan of water spraying from it",
      tags=["water spray", "nozzle", "hose stream", "firefighting", "extinguish", "water"])
def _(S):
    return [
        line(seg(2, 13, 6, 13)),
        shell(poly([(6, 9.5), (12, 11), (12, 15), (6, 16.5)], closed=True, r=S.r * 0.6)),
        line(seg(16, 11, 21, 6)), line(seg(16.5, 13, 21.5, 13)), line(seg(16, 15, 21, 20)),
    ]


@icon("fire-bucket", CAT, "Cone-bottomed fire bucket with a carry handle and a flame badge",
      tags=["sand bucket", "water bucket", "fire pail", "red bucket", "extinguish", "safety"])
def _(S):
    body = poly([(4.5, 8.5), (19.5, 8.5), (17, 16), (12, 21.5), (7, 16)], closed=True, r=S.r * 0.8)
    return [
        line("M7.5 8.5C7.5 2.5 16.5 2.5 16.5 8.5"),
        shell(body),
        mark(flame(12, 10.5, 16, 4, S)),
    ]


@icon("fire-beater", CAT, "Long-handled wildfire beater with a flat rubber mat",
      tags=["flapper", "swatter", "wildfire tool", "grass fire", "beat out flames", "fire fighting"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 10, rr(S, 3))),
        detail(seg(6, 7.5, 18, 7.5)),
        line(seg(12, 12.5, 12, 21.5)),
    ]


@icon("wildfire-backpack-pump", CAT, "Water bladder backpack with a hose running to a hand-held slide pump",
      tags=["backpack sprayer", "indian pump", "wildland", "water pack", "forest fire", "hose"])
def _(S):
    return [
        shell(rect(3, 5, 10, 16, rr(S, 4))),
        detail(seg(3, 10.5, 13, 10.5)),
        line("M13 17C16 17 15.5 15 17 15"),
        shell(rect(17, 8, 4, 10, rr(S, 1.5))),
        line(seg(19, 3, 19, 8)), line(seg(17, 3, 21, 3)),
    ]


@icon("pulaski-axe", CAT, "Wildland tool with an axe blade on one side of the head and a flat adze on the other",
      tags=["pulaski", "wildland axe", "fire line", "grubbing", "forestry", "hand tool"])
def _(S):
    d, dx, dy = -45, 1.2, 2.2
    head = "M5.5 4.5L10 5.5H14L19.5 5.5V10.5L14 9.5H10L5.5 12Q3.8 8 5.5 4.5Z"
    return [
        shell(rpath(head, d, dx, dy), stroke_miterlimit="3"),
        line(rseg(12, 9.5, 12, 21.5, d, dx, dy)),
    ]


@icon("fire-rake", CAT, "Wildland rake with a wide blade and a row of tines",
      tags=["mcleod", "fire line tool", "wildland", "rake", "scrape", "forestry"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 11)),
        shell(poly([(3, 11), (21, 11), (19, 16), (5, 16)], closed=True, r=S.r * 0.4)),
        line(seg(4.5, 16, 4.5, 21)), line(seg(9, 16, 9, 21)), line(seg(15, 16, 15, 21)), line(seg(19.5, 16, 19.5, 21)),
    ]


@icon("breathing-apparatus", CAT, "Air cylinder with a hose leading to a full-face mask",
      tags=["scba", "air tank", "respirator", "smoke mask", "firefighter gear", "self-contained"])
def _(S):
    return [
        line(seg(7, 2.5, 7, 4)),
        shell(rect(3, 4, 8, 17, rr(S, 4))),
        detail(seg(3, 9, 11, 9)),
        line("M11 6.5C16 6.5 17.5 8.5 17.5 11"),
        shell("M14 11H21V17C21 20 19.5 21.5 17.5 21.5C15.5 21.5 14 20 14 17Z"),
        mark(rect(15.5, 14, 4, 2.5, 1)),
    ]


@icon("turnout-coat", CAT, "Firefighter turnout coat with a high collar, front clasps and reflective bands",
      tags=["bunker coat", "fire jacket", "turnout gear", "firefighter", "protective clothing", "reflective"])
def _(S):
    return [
        shell(poly([(8, 3), (16, 3), (21, 6), (21, 19), (17, 19), (17, 21.5), (7, 21.5), (7, 19), (3, 19), (3, 6)], closed=True, r=S.r * 0.6)),
        detail("M8 3L12 7.5L16 3"),
        detail(seg(12, 7.5, 12, 13)),
        detail(seg(7, 15, 17, 15)),
        detail(seg(7, 8, 7, 19)), detail(seg(17, 8, 17, 19)),
    ]


# ============================================================================ alarms, doors and fixed equipment

@icon("fire-alarm-strobe", CAT, "Wall horn-and-strobe box with a speaker grille and a flashing lens with rays above",
      tags=["horn strobe", "fire alarm", "alarm horn", "warning light", "sounder", "alert"])
def _(S):
    return [
        shell(rect(3, 8, 18, 13, rr(S, 3))),
        dot(7.5, 12, 1.25), dot(7.5, 16.5, 1.25),
        detail(circle(15, 14.5, 3.25)),
        line(seg(15, 2.5, 15, 5)), line(seg(9.5, 3.5, 11.5, 5.5)), line(seg(20.5, 3.5, 18.5, 5.5)),
    ]


@icon("heat-detector", CAT, "Low round ceiling heat detector with a thermometer mark and wavy heat lines rising to it",
      tags=["heat alarm", "rate of rise", "fire detector", "ceiling sensor", "thermal detector", "temperature"])
def _(S):
    return [
        shell("M4 11.5H20C20 7.5 16.5 4.5 12 4.5C7.5 4.5 4 7.5 4 11.5Z"),
        mark(rect(11, 6.5, 2, 3, 0.8 if S.name == "rounded" else 0)),
        line("M7 15Q5.5 17 7 19Q8.5 21 7 22"), line("M12 15Q10.5 17 12 19Q13.5 21 12 22"), line("M17 15Q15.5 17 17 19Q18.5 21 17 22"),
    ]


@icon("carbon-monoxide-detector", CAT, "Wall detector box with the letters CO on its display and a vent row below",
      tags=["co alarm", "co detector", "gas alarm", "poison gas", "home safety", "sensor"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 4))),
        detail(arc(8.8, 9, 2.5, 40, 320)),
        detail(circle(15.5, 9, 2.5)),
        dot(8, 16, 1.25), dot(12, 16, 1.25), dot(16, 16, 1.25),
    ]


@icon("fire-door", CAT, "Heavy door with a small glass window, a handle and a flame badge on the leaf",
      tags=["fire exit door", "fire rated door", "self closing door", "flame badge", "building safety", "exit"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 2))),
        detail(rect(9, 6, 6, 4, 0)),
        mark(flame(11, 12.5, 19, 4.5, S)),
        dot(16, 16, 1.1),
    ]


@icon("co2-fire-extinguisher", CAT, "Extinguisher cylinder with a long flared discharge horn on a hose",
      tags=["carbon dioxide extinguisher", "co2 extinguisher", "horn", "electrical fire", "fire safety", "equipment"])
def _(S):
    return [
        shell(rect(3.5, 8, 9, 13.5, rr(S, 3.5))),
        line(seg(8, 8, 8, 4.5)),
        line("M8 4.5H14Q18.5 4.5 18.5 9"),
        shell(poly([(17.3, 10), (19.7, 10), (21.5, 18.5), (15.5, 18.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("wheeled-fire-extinguisher", CAT, "Large extinguisher cylinder on a two-wheeled trolley with a pull handle",
      tags=["trolley extinguisher", "wheeled unit", "big extinguisher", "industrial fire safety", "cart", "airport"])
def _(S):
    return [
        shell(rect(3.5, 3, 9, 10.5, rr(S, 3.5))),
        line(poly([(12.5, 7), (19, 7), (19, 21.5)], r=S.r)),
        shell(circle(8, 19, 2.5)),
    ]


@icon("fire-extinguisher-ball", CAT, "Round ball-shaped extinguisher with a flame symbol resting in a wall cradle",
      tags=["extinguishing ball", "throwable", "automatic extinguisher", "fire ball", "safety", "suppression"])
def _(S):
    return [
        shell(circle(12, 9.5, 7.25)),
        mark(flame(12, 5.5, 13, 5, S)),
        line(poly([(6, 18.5), (6, 21.5), (18, 21.5), (18, 18.5)], r=S.r)),
    ]


@icon("fire-hose-cabinet", CAT, "Wall cabinet with a glass door showing a coiled hose and a valve",
      tags=["hose reel cabinet", "fire station box", "hose box", "standpipe", "building safety", "wall cabinet"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 3))),
        detail("M11 12.5A1.5 1.5 0 0 1 14 12.5A3.5 3.5 0 0 1 7 12.5A5.5 5.5 0 0 1 18 12.5"),
    ]


@icon("fire-department-connection", CAT, "Siamese twin-inlet hose connection with two capped round inlets on a pipe",
      tags=["siamese connection", "fdc", "standpipe inlet", "sprinkler inlet", "hose inlet", "building"])
def _(S):
    return [
        shell(circle(6.75, 8.5, 3.5)), shell(circle(17.25, 8.5, 3.5)),
        dot(6.75, 8.5, 1), dot(17.25, 8.5, 1),
        line(poly([(6.75, 12), (6.75, 17), (17.25, 17), (17.25, 12)], r=S.r)),
        line(seg(12, 17, 12, 21.5)),
    ]


@icon("fire-hydrant-wrench", CAT, "Wrench with a pentagon socket head on a long straight handle",
      tags=["hydrant key", "spanner", "valve key", "hydrant tool", "fire service", "water main"])
def _(S):
    d, dx, dy = 45, 1, 0
    pent = rpts([polar(12, 6.5, 4.8, -90 + i * 72) for i in range(5)], d, dx, dy)
    cx, cy = rpts([(12, 6.5)], d, dx, dy)[0]
    return [
        shell(poly(pent, closed=True, r=S.r * 0.6)),
        dot(cx, cy, 1.3),
        line(rseg(12, 11.5, 12, 21.5, d, dx, dy)),
    ]


@icon("portable-fire-pump", CAT, "Small engine-driven pump on a tube frame with a discharge outlet on top",
      tags=["trash pump", "water pump", "engine pump", "firefighting pump", "wildfire", "portable"])
def _(S):
    body = union(rect(3, 10, 9, 8, rr(S, 2.5)), circle(16, 13.5, 4.5))
    return [
        shell(body),
        detail(seg(6, 14, 9, 14)),
        line(seg(16, 9, 16, 5)),
        shell(rect(13.5, 2.5, 5, 2.5, rr(S, 1))),
        line(poly([(3, 18), (3, 21.5), (19.5, 21.5), (19.5, 18)], r=S.r)),
    ]


@icon("fire-monitor-nozzle", CAT, "Deck-mounted water cannon on a riser with a long barrel and a straight jet",
      tags=["water cannon", "monitor", "deck gun", "master stream", "fire boat", "hose stream"])
def _(S):
    return [
        shell(rect(3, 19, 9, 3, rr(S, 1.2))),
        line(seg(7.5, 19, 7.5, 14)),
        shell(rotd(rect(5, 6.5, 11.5, 5, rr(S, 2.2)), -25, 7.5, 13)),
        line("M18.5 7.5Q21.5 7 22 10"), line("M17.5 12Q20.5 12 21 15"),
    ]


@icon("fire-alarm-control-panel", CAT, "Wall panel with a small screen, a row of zone lights and two buttons",
      tags=["facp", "alarm panel", "zone indicator", "fire panel", "building safety", "control"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 3))),
        detail(rect(6.5, 5.5, 11, 4.5, 0)),
        dot(7.5, 14, 1.25), dot(12, 14, 1.25), dot(16.5, 14, 1.25),
        mark(rect(6.5, 17, 4, 2, 0.6 if S.name == "rounded" else 0)), mark(rect(13.5, 17, 4, 2, 0.6 if S.name == "rounded" else 0)),
    ]


@icon("flammable-storage-cabinet", CAT, "Tall double-door safety cabinet with a flame symbol on the left door and short legs",
      tags=["safety cabinet", "chemical storage", "solvent cabinet", "fuel storage", "hazmat", "laboratory"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 16.5, rr(S, 2))),
        detail(seg(12, 2.5, 12, 19)),
        mark(flame(8, 6, 13.5, 4, S)),
        dot(15.5, 11, 1),
        line(seg(7, 19, 7, 21.5)), line(seg(17, 19, 17, 21.5)),
    ]


@icon("smoke-ejector-fan", CAT, "Portable fan in a square housing blowing three lines of air forward to clear smoke",
      tags=["smoke fan", "ppv fan", "ventilation fan", "blower", "positive pressure", "clear smoke"])
def _(S):
    return [
        shell(rect(3, 4, 11, 16, rr(S, 3))),
        detail(seg(8.5, 7.5, 8.5, 16.5)),
        dot(8.5, 12, 1.5),
        line(seg(17, 8, 22, 8)), line(seg(17, 12, 22, 12)), line(seg(17, 16, 22, 16)),
    ]


# ============================================================================ water supply and fixed systems

@icon("portable-water-tank", CAT, "Open-top folding water tank with water inside and a hose running in over the rim",
      tags=["drop tank", "pool tank", "water reservoir", "fire fighting water", "folding tank", "water supply"])
def _(S):
    return [
        shell(poly([(3, 8), (21, 8), (19, 20), (5, 20)], closed=True, r=S.r * 0.6)),
        detail("M6 13.5Q8.25 11.5 10.5 13.5T15 13.5T19 13.5"),
        line(poly([(21.5, 3), (15, 3), (15, 5.5)], r=S.r)),
    ]


@icon("sprinkler-riser", CAT, "Vertical sprinkler pipe with a pressure gauge and a handwheel valve beside it",
      tags=["riser", "sprinkler valve", "fire sprinkler", "standpipe", "water gauge", "plant room"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 4, 19, L(S, 0, 1.9))),
        line(seg(9.5, 7, 12.5, 7)), shell(circle(16.5, 7, 3.25)),
        dot(16.5, 7, 1),
        line(seg(9.5, 16, 12.5, 16)), shell(circle(16.5, 16, 3.25)),
        detail(seg(14.5, 16, 18.5, 16)),
    ]


@icon("street-fire-alarm-box", CAT, "Old street fire alarm box with a gabled top, a pull handle and a pedestal post",
      tags=["call box", "pull box", "fire call point", "alarm post", "emergency call", "street"])
def _(S):
    box = poly([(6, 13), (6, 7), (12, 2.5), (18, 7), (18, 13)], closed=True, r=S.r * 0.5)
    body = union(box, rect(10.5, 12, 3, 9.5), rect(7, 19.5, 10, 2))
    return [
        shell(body),
        detail(seg(9.5, 9.5, 14.5, 9.5)),
    ]


@icon("fire-engine-pump-panel", CAT, "Fire engine pump panel with two round gauges above a row of lever handles",
      tags=["pump panel", "engine panel", "pressure gauge", "discharge valves", "fire truck", "operator"])
def _(S):
    parts = [shell(circle(7, 6.5, 3.25)), shell(circle(17, 6.5, 3.25)), dot(7, 6.5, 0.9), dot(17, 6.5, 0.9)]
    for x in (6, 12, 18):
        parts.append(line(seg(x, 14, x, 19.5)))
        parts.append(line(seg(x - 2.25, 14, x + 2.25, 14)))
    parts.append(line(seg(2.5, 21.5, 21.5, 21.5)))
    return parts


@icon("fire-service-cross", CAT, "Eight-pointed cross with flared notched arms and a small centre disc",
      tags=["maltese cross", "fire department emblem", "fire badge", "service symbol", "firefighter badge", "insignia"])
def _(S):
    pts = [(8.5, 2.5), (12, 5), (15.5, 2.5), (13.5, 10.5), (21.5, 8.5), (19, 12), (21.5, 15.5), (13.5, 13.5),
           (15.5, 21.5), (12, 19), (8.5, 21.5), (10.5, 13.5), (2.5, 15.5), (5, 12), (2.5, 8.5), (10.5, 10.5)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.8), stroke_miterlimit="2"),
        dot(12, 12, 1.6),
    ]


@icon("helicopter-water-bucket", CAT, "Helicopter on a long line carrying a hanging bucket that pours water below",
      tags=["water drop", "aerial firefighting", "fire helicopter", "wildfire", "air attack"])
def _(S):
    return heli(S) + [
        line(seg(9.5, 11.5, 9.5, 14.5)),
        shell(poly([(6.5, 14.5), (12.5, 14.5), (11.5, 18.5), (7.5, 18.5)], closed=True, r=S.r * 0.6)),
        dot(8, 21.5, 0.9), dot(11, 21.5, 0.9),
    ]


@icon("fire-pole", CAT, "Vertical sliding pole passing through a gap in the floor above",
      tags=["sliding pole", "station pole", "fire station", "slide down", "brass pole", "firehouse"])
def _(S):
    k = rr(S, 1.5)
    return [
        line(seg(12, 2.5, 12, 21.5)),
        shell(rect(2.5, 8, 6, 4, k)), shell(rect(15.5, 8, 6, 4, k)),
        line(seg(7, 21.5, 17, 21.5)),
    ]


@icon("roof-ladder", CAT, "Straight ladder with two folding hooks at the top for hooking over a roof ridge",
      tags=["hook ladder", "roof hooks", "ridge ladder", "climb roof", "firefighter ladder", "rescue"])
def _(S):
    return [
        line(poly([(8.5, 21.5), (8.5, 4), (4, 4), (4, 7.5)], r=S.r)),
        line(poly([(15.5, 21.5), (15.5, 4), (20, 4), (20, 7.5)], r=S.r)),
        line(seg(8.5, 10, 15.5, 10)), line(seg(8.5, 14.5, 15.5, 14.5)), line(seg(8.5, 19, 15.5, 19)),
    ]


# ============================================================================ fire hazards

@icon("house-fire", CAT, "Small house with a flame inside and a larger flame rising behind its roof",
      tags=["burning house", "home fire", "structure fire", "blaze", "building fire", "emergency"])
def _(S):
    house = poly([(2.5, 11.5), (9.5, 5), (16.5, 11.5), (16.5, 21.5), (2.5, 21.5)], closed=True, r=S.r * 0.5)
    big = flame(17, 3, 21.5, 10, S)
    return [
        shell(house),
        mark(flame(9.5, 12, 19.5, 5, S)),
        shell(cut(big, house, 2.2), stroke_miterlimit="3"),
    ]


@icon("high-rise-fire", CAT, "Tall tower block with windows and a flame rising from its upper floors",
      tags=["tower fire", "skyscraper fire", "apartment fire", "burning building", "flames", "emergency"])
def _(S):
    tower = rect(3, 4, 12, 17.5, rr(S, 2))
    big = flame(17.5, 3, 14, 8, S)
    return [
        shell(tower),
        mark(rect(6, 8, 2.5, 2.5)), mark(rect(9.5, 8, 2.5, 2.5)),
        mark(rect(6, 13, 2.5, 2.5)), mark(rect(9.5, 13, 2.5, 2.5)),
        mark(rect(7.5, 18, 3, 3.5)),
        shell(cut(big, tower, 2.2), stroke_miterlimit="3"),
    ]


@icon("grease-fire", CAT, "Frying pan with a tall flame rising out of it and a burner flame below",
      tags=["kitchen fire", "pan fire", "cooking fire", "stove fire", "oil fire", "fry pan"])
def _(S):
    pan = "M3 14H16L15 19Q14.8 20 13.8 20H5.2Q4.2 20 4 19Z"
    return [
        shell(pan),
        line(seg(16, 15.5, 22, 15.5)),
        shell(flame(9.5, 3, 11.5, 8, S), stroke_miterlimit="3"),
    ]


@icon("electrical-fire", CAT, "Plug with two prongs and a flame rising from its connection",
      tags=["electrical blaze", "short circuit", "wiring fire", "plug fire", "overheating", "power fire"])
def _(S):
    return [
        shell(poly([(6, 14), (18, 14), (18, 17.5), (15, 20), (9, 20), (6, 17.5)], closed=True, r=S.r * 0.6)),
        line(seg(9.5, 14, 9.5, 11.5)), line(seg(14.5, 14, 14.5, 11.5)),
        line(seg(12, 20, 12, 22)),
        shell(flame(12, 3, 9.5, 7, S), stroke_miterlimit="3"),
    ]


@icon("lithium-battery-fire", CAT, "Swollen battery cell with a plus mark and a flame rising from its top",
      tags=["battery fire", "thermal runaway", "li-ion fire", "swollen battery", "e-bike battery", "overheating"])
def _(S):
    return [
        shell("M7.5 12.5Q5.5 17 7.5 21.5H16.5Q18.5 17 16.5 12.5Z"),
        detail(seg(9.5, 17, 14.5, 17)), detail(seg(12, 14.5, 12, 19.5)),
        shell(flame(12, 3, 10, 7, S), stroke_miterlimit="3"),
    ]


@icon("overloaded-socket", CAT, "Multi-plug adapter with three cords fanning out and a spark jumping from its edge",
      tags=["power strip", "too many plugs", "extension lead", "socket overload", "fire risk", "spark"])
def _(S):
    return [
        shell(rect(3, 4.5, 14, 8.5, rr(S, 2.5))),
        dot(6.75, 8.75, 1.25), dot(10, 8.75, 1.25), dot(13.25, 8.75, 1.25),
        line(seg(6.5, 13, 4.5, 21.5)), line(seg(10, 13, 10, 21.5)), line(seg(13.5, 13, 15.5, 21.5)),
        line(poly([(21, 2.5), (19.5, 6.5), (21.5, 7), (20, 11)])),
    ]


@icon("frayed-wire", CAT, "Electrical cord with torn insulation and three bare strands spreading from its end",
      tags=["exposed wire", "damaged cable", "broken cord", "electrical hazard", "bare wire", "shock risk"])
def _(S):
    return [
        shell(poly([(2, 9), (8.5, 9), (10, 10.5), (8.5, 12), (10, 13.5), (8.5, 15), (2, 15)], closed=True, r=S.r * 0.4)),
        line("M11 10.5Q16 9.5 19 5.5"), line("M11.5 12H21.5"), line("M11 13.5Q16 14.5 19 18.5"),
    ]


# ============================================================================ wildland fire

@icon("chimney-fire", CAT, "Roof with a brick chimney shooting a flame and sparks from its top",
      tags=["flue fire", "soot fire", "roof fire", "fireplace fire", "house fire", "sparks"])
def _(S):
    house = poly([(2.5, 21.5), (2.5, 15.5), (10.5, 9.5), (18.5, 15.5), (18.5, 21.5)], closed=True)
    body = union(house, rect(13.5, 9, 4, 6))
    return [
        shell(body, stroke_miterlimit="3"),
        shell(flame(15.5, 3, 8, 6.5, S), stroke_miterlimit="2"),
        dot(9.5, 6, 1.1), dot(21, 9, 1.0),
    ]


@icon("prescribed-burn", CAT, "Person with a drip torch behind a low line of flames moving across the ground",
      tags=["controlled burn", "planned fire", "backburn", "drip torch", "land management", "fuel reduction"])
def _(S):
    fl = union(flame(15, 12.5, 21, 6, S), flame(20, 15, 21, 5, S))
    return [
        head(5, 6),
        line(poly([(5, 9), (5, 15.5)])),
        line(poly([(5, 11), (9.5, 13.5), (11.5, 16)], r=S.r)),
        line(poly([(3.5, 21.5), (5, 15.5), (8, 21.5)], r=S.r)),
        mark(fl),
    ]


@icon("firebreak", CAT, "Flames on the left, a bare cleared strip in the middle and a tree on the right",
      tags=["fire line", "fuel break", "defensible space", "clearing", "wildfire barrier", "containment"])
def _(S):
    return [
        mark(flame(6, 7.5, 21, 7, S)),
        shell(poly([(14, 17), (17.5, 4.5), (21, 17)], closed=True, r=S.r * 0.5)),
        line(seg(17.5, 17, 17.5, 21.5)),
    ]


@icon("fire-shelter", CAT, "Low foil emergency shelter lying on the ground with crinkled folds",
      tags=["fire blanket tent", "emergency shelter", "foil shelter", "wildland survival", "last resort", "tent"])
def _(S):
    return [
        shell("M2.5 19.5C3 12.5 7 8.5 12 8.5C17 8.5 21 12.5 21.5 19.5Z"),
        detail("M12 9.5L10 13L12.5 15L10.5 19.5"),
        detail("M17 13L15.5 16.5L17.5 19.5"),
    ]


@icon("fire-tornado", CAT, "Spinning funnel of narrowing bands with a flame at its base",
      tags=["fire whirl", "firenado", "fire devil", "extreme fire behavior", "wildfire", "vortex"])
def _(S):
    return [
        line("M3.5 3.5Q12 6.5 20.5 3.5"), line("M6 8Q12 10.5 18 8"), line("M8.5 12.5Q12 14 15.5 12.5"),
        mark(flame(12, 15, 21.5, 6, S)),
    ]


@icon("burned-forest", CAT, "Three bare blackened trunks with broken branch stubs on scorched ground",
      tags=["wildfire aftermath", "scorched trees", "charred", "burnt trees", "fire damage", "deforestation"])
def _(S):
    return [
        line(seg(5, 21.5, 5, 10)), line(seg(5, 15, 3, 12.5)),
        line(seg(12, 21.5, 12, 3.5)), line(seg(12, 16, 9.5, 13.5)), line(seg(12, 11.5, 14.5, 9)),
        line(seg(19, 21.5, 19, 8)), line(seg(19, 14, 21.5, 11.5)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("flying-embers", CAT, "Glowing ember specks blown on wind lines toward the roof of a house",
      tags=["firebrands", "spot fires", "ember attack", "wildfire spread", "wind", "sparks"])
def _(S):
    return [
        shell(poly([(13.5, 13.5), (17.5, 9), (21.5, 13.5), (21.5, 21.5), (13.5, 21.5)], closed=True, r=S.r * 0.5)),
        dot(4, 6, 1.3), dot(9, 4, 1.3), dot(9.5, 9, 1.3), dot(3.5, 11.5, 1, ), dot(14, 5, 1.1),
        line(seg(2, 17, 8.5, 17)), line(seg(2, 21, 6.5, 21)),
    ]


@icon("fire-lane-sign", CAT, "Sign with two lines of lettering above a circle with a slash, marking a no-parking fire lane",
      tags=["no parking", "fire access", "keep clear", "emergency access", "road sign", "parking"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 11.5, rr(S, 2))),
        mark(rect(5.5, 6.5, 7, 1.75)), mark(rect(5.5, 9.75, 7, 1.75)),
        detail(circle(17, 8.75, 2.5)),
        detail(seg(15.4, 7.2, 18.6, 10.3)),
        line(seg(12, 14.5, 12, 21.5)), line(seg(8, 21.5, 16, 21.5)),
    ]


# ============================================================================ people

@icon("smokejumper", CAT, "Firefighter hanging under an open parachute canopy with a tool pack at the hip",
      tags=["parachute firefighter", "aerial firefighter", "wildfire crew", "remote fire", "paratrooper", "drop"])
def _(S):
    return [
        shell("M3.5 9A8.5 6.5 0 0 1 20.5 9Z"),
        line(seg(3.5, 9, 12, 12)), line(seg(20.5, 9, 12, 12)),
        head(12, 14.75),
        line(seg(12, 17, 12, 19.5)),
        line(poly([(10, 22), (12, 19.5), (14, 22)], r=S.r)),
    ]


@icon("fire-chief", CAT, "Front view of a firefighter in a white helmet with a crossed-trumpets badge, shoulders below",
      tags=["fire captain", "fire commander", "officer", "helmet badge", "incident commander", "fire service"])
def _(S):
    dome = union("M5.5 11.5A6.5 7 0 0 1 18.5 11.5Z", rect(3, 11, 18, 2.5, 1))
    return [
        shell(dome),
        mark(poly([(10.25, 5.5), (13.75, 5.5), (13.75, 8.5), (12, 9.75), (10.25, 8.5)], closed=True)),
        line(poly([(3.5, 21.5), (4.5, 18), (9, 16.5), (15, 16.5), (19.5, 18), (20.5, 21.5)], r=S.r)),
        line(poly([(9, 16.5), (12, 20), (15, 16.5)])),
    ]


@icon("fire-warden", CAT, "Person in a vest with a flame badge, holding a clipboard and pointing the way",
      tags=["fire marshal", "floor warden", "evacuation leader", "safety officer", "emergency coordinator", "vest"])
def _(S):
    return [
        head(11.5, 4.75),
        shell(rect(8, 8.5, 7, 9, rr(S, 2))),
        mark(flame(11.5, 10.5, 15.5, 3.2, S)),
        line(seg(15, 10, 21, 6.5)),
        line(seg(8, 10.5, 5.5, 13)),
        shell(rect(2.5, 12.5, 5, 7, rr(S, 1))),
        line(seg(10, 17.5, 10, 21.5)), line(seg(13, 17.5, 13, 21.5)),
    ]


@icon("fire-drill", CAT, "Two small figures walking toward an open door with a ringing bell above",
      tags=["evacuation drill", "practice evacuation", "alarm bell", "exit practice", "safety training", "assembly"])
def _(S):
    parts = [shell("M16 6.5Q16 2.5 19 2.5Q22 2.5 22 6.5Z")]
    for x in (4.5, 10.5):
        parts += [dot(x, 11.25, 1.9), line(seg(x, 13.75, x, 18)),
                  line(poly([(x - 1.9, 21.5), (x, 18), (x + 1.9, 21.5)]))]
    parts.append(line(poly([(15.5, 21.5), (15.5, 10), (21.5, 10), (21.5, 21.5)], r=S.r)))
    return parts


@icon("fire-evacuation-plan", CAT, "Framed floor plan with a wall outline, a you-are-here dot and a route arrow to the exit",
      tags=["escape plan", "exit map", "floor plan", "assembly point", "you are here", "evacuation route"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 2))),
        detail("M3 12.5H10.5V21"),
        dot(6.75, 7.5, 1.5),
        detail("M11 7.5H16.5V16M14.5 14L16.5 16.5L18.5 14"),
    ]


@icon("fireman-carry", CAT, "Rescuer standing with another person draped across the shoulders",
      tags=["carry rescue", "shoulder carry", "casualty carry", "rescue", "save a life", "evacuate"])
def _(S):
    return [
        head(12, 4.25),
        shell(rect(5.5, 8.5, 14, 4.5, 2.25)),
        dot(3.25, 13.5, 1.6),
        line(poly([(19.5, 11.5), (21.5, 16)])),
        line(seg(12, 15, 12, 17.5)),
        line(poly([(9.5, 21.5), (12, 17.5), (14.5, 21.5)], r=S.r)),
    ]


@icon("crawl-under-smoke", CAT, "Person crawling on hands and knees beneath two wavy layers of smoke",
      tags=["stay low", "smoke safety", "get down", "escape smoke", "evacuation", "crawl"])
def _(S):
    return [
        line("M3 4Q6 2 9 4T15 4T21 4"), line("M3 8.5Q6 6.5 9 8.5T15 8.5T21 8.5"),
        head(19, 13.5),
        line(seg(8, 15, 16.5, 15)),
        line(seg(15.5, 15, 16.5, 21.5)),
        line(poly([(8, 15), (9.5, 20), (5, 21.5)], r=S.r)),
    ]


# ============================================================================ technical rescue

@icon("hydraulic-rescue-spreader", CAT, "Rescue spreader with two long pointed jaw arms opening like a beak and a hose at the back",
      tags=["spreader", "extrication", "car crash rescue", "hydraulic tool", "prying"])
def _(S):
    left = poly([(8.5, 12), (5, 3.5), (7.5, 3), (12, 10.5)], closed=True)
    right = poly([(15.5, 12), (19, 3.5), (16.5, 3), (12, 10.5)], closed=True)
    body = union(left, right, rect(8.5, 10, 7, 7, rr(S, 2.5)))
    return [
        shell(body, stroke_miterlimit="3"),
        line("M12 17V19Q12 21.5 17 21.5H21.5"),
    ]


@icon("lifting-air-bag", CAT, "Flat inflatable cushion wedged under a heavy load with an air hose running off it",
      tags=["rescue airbag", "lifting bag", "pneumatic lift", "vehicle lift", "extrication", "inflate"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 4, rr(S, 1.5))),
        line(seg(12, 13, 12, 9.5)), line(poly([(9.75, 11.5), (12, 9.25), (14.25, 11.5)], r=S.r * 0.5)),
        shell("M4.5 20.5L3 17Q3.5 15 6 15H18Q20.5 15 21 17L19.5 20.5Z"),
    ]


@icon("confined-space-tripod", CAT, "Rescue tripod with a winch over a round opening and a rope hanging down the centre",
      tags=["manhole rescue", "tripod hoist", "winch", "confined space", "entry rescue", "rope"])
def _(S):
    return [
        line(seg(12, 4, 4.5, 20)), line(seg(12, 4, 19.5, 20)),
        shell(circle(12, 3.5, 1.6)),
        line(seg(12, 5.5, 12, 14)), shell(circle(12, 16, 1.6)),
        line(ellipse(12, 20.5, 8.5, 1.5)),
    ]


@icon("figure-eight-descender", CAT, "Metal figure-eight rappelling device with a large lower ring and a smaller upper ring",
      tags=["figure 8", "rappel", "abseil", "rope descender", "climbing", "rope rescue"])
def _(S):
    big = circle(12, 15.5, L(S, 5.5, 5.9))
    small = circle(12, 6, L(S, 3.25, 3.6))
    outer = union(big, small)
    return [
        shell(minus(outer, circle(12, 15.5, L(S, 2.3, 2.7)), circle(12, 6, 1.1))),
    ]


@icon("avalanche-probe", CAT, "Long jointed probe pole with a ring handle pushed down into a snow mound",
      tags=["snow probe", "avalanche rescue", "search pole", "backcountry", "ski patrol", "buried victim"])
def _(S):
    ax, ay, bx, by = 18, 5.5, 11.5, 18
    dx, dy = bx - ax, by - ay
    n = math.hypot(dx, dy)
    px, py = -dy / n, dx / n
    ticks = []
    for t in (0.3, 0.55):
        cx, cy = ax + dx * t, ay + dy * t
        ticks.append(line(seg(cx - px * 1.8, cy - py * 1.8, cx + px * 1.8, cy + py * 1.8)))
    return [
        shell(circle(19, 3.75, 1.75)),
        line(seg(18.3, 5.3, bx, by)),
        *ticks,
        line("M2.5 21.5Q3 16 12 16Q21 16 21.5 21.5"),
    ]


@icon("search-and-rescue-dog", CAT, "Dog in a cross-marked harness vest standing with its nose to the ground",
      tags=["rescue dog", "k9", "sniffer dog", "cadaver dog", "disaster dog", "search dog"])
def _(S):
    return [
        shell(rect(7, 7.5, 13, 7.5, rr(S, 3))),
        mark(rect(12.6, 8.75, 1.5, 4.5)), mark(rect(11.1, 10.25, 4.5, 1.5)),
        shell(circle(4.5, 15, 2.75)),
        line(seg(7.25, 10, 5.5, 12.5)),
        line(seg(9.5, 15, 9.5, 21.5)), line(seg(17.5, 15, 17.5, 21.5)),
        line(poly([(20, 9), (21.5, 5.5)])),
    ]


@icon("hoist-rescue", CAT, "Helicopter hovering with a winch cable lowering a rescuer who holds a second person",
      tags=["winch rescue", "helicopter rescue", "airlift", "sea rescue", "mountain rescue", "coast guard"])
def _(S):
    return heli(S) + [
        line(seg(9.5, 11.5, 9.5, 13.25)),
        dot(9.5, 15.5, 1.6), line(seg(9.5, 17.5, 9.5, 19.5)),
        line(poly([(7.75, 22), (9.5, 19.5), (11.25, 22)])),
        line(seg(9.5, 17.75, 15.5, 18)),
        dot(17.5, 16, 1.6), line(seg(17.5, 18, 17.5, 22)),
    ]


@icon("rescue-cutoff-saw", CAT, "Hand-held cut-off saw with a round blade under a guard, an engine body and a top handle",
      tags=["rescue saw", "power cutter", "disc cutter", "concrete saw", "demolition", "extrication"])
def _(S):
    return [
        shell(circle(7.5, 15.5, 3.5)), dot(7.5, 15.5, 0.9),
        line(arc(7.5, 15.5, 6.25, 200, 340)),
        line(seg(11, 15.5, 14, 15.5)),
        shell(rect(14, 9.5, 7.5, 9.5, rr(S, 3))),
        line(poly([(15.5, 9.5), (15.5, 5), (20, 5), (20, 9.5)], r=S.r)),
    ]


@icon("emergency-hammer", CAT, "Car escape hammer with a pointed steel tip on the head and a seat-belt cutter slot in the handle",
      tags=["window breaker", "escape tool", "car safety", "belt cutter", "spring punch", "glass breaker"])
def _(S):
    head = union(rect(4, 4, 9, 6, rr(S, 1.5)), poly([(13, 5), (21, 7), (13, 9)], closed=True))
    return [
        shell(head, stroke_miterlimit="3"),
        shell(rect(9, 10, 5, 11.5, rr(S, 2.5))),
        detail(seg(11.5, 14, 11.5, 19)),
    ]


@icon("head-immobilizer", CAT, "Head support board with two foam side blocks, a head shape and straps",
      tags=["spinal board", "cervical", "head blocks", "trauma", "paramedic", "neck support"])
def _(S):
    k = L(S, 0.5, 1.5)
    return [
        shell(rect(8, 2.5, 8, 19, k)),
        shell(rect(2, 4.5, 3, 9, k)), shell(rect(19, 4.5, 3, 9, k)),
        dot(12, 8.5, 2.3),
        detail(seg(8, 13, 16, 13)), detail(seg(8, 17, 16, 17)),
    ]


@icon("rubble-search-camera", CAT, "Small camera on a telescopic pole pushed into the gap between two slabs of rubble",
      tags=["search camera", "snake camera", "collapsed building", "urban search and rescue", "void search", "inspection"])
def _(S):
    return [
        line(seg(21, 2.5, 12.5, 13)),
        shell(circle(11.5, 16, 2.25)),
        shell(poly([(2.5, 21.5), (2.5, 14), (7, 12), (7, 21.5)], closed=True, r=S.r * 0.4)),
        shell(poly([(16, 21.5), (16, 12.5), (21.5, 15), (21.5, 21.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("rescue-toboggan", CAT, "Boat-shaped rescue sled with rope handles at both ends and a patient strapped in",
      tags=["rescue sled", "ski patrol", "mountain rescue", "stretcher sled", "snow rescue"])
def _(S):
    return [
        shell("M2.5 12Q3 20 10 20H14Q21 20 21.5 12Z"),
        line("M4 12Q2.5 7.5 6 7"), line("M20 12Q21.5 7.5 18 7"),
        dot(7.5, 9.5, 1.6), line(seg(9.5, 10, 17, 10)),
        detail(seg(12, 12, 12, 17)),
    ]


@icon("breeches-buoy", CAT, "Life ring hanging from a pulley that runs along a taut rope line",
      tags=["rescue line", "ship rescue", "zip line rescue", "pulley", "life ring", "sea rescue"])
def _(S):
    return [
        line(seg(2, 3.5, 22, 6)),
        shell(circle(12, 5.25, 1.6)),
        line(seg(12, 7, 12, 9.5)),
        shell(minus(circle(12, 15, 5.75), circle(12, 15, 2.5))),
    ]


@icon("trench-shoring", CAT, "Narrow trench in cross-section with two wall panels braced apart by screw struts",
      tags=["trench rescue", "shoring", "excavation safety", "cave-in", "trench box", "struts"])
def _(S):
    return [
        line(seg(2, 6, 4.5, 6)), line(seg(19.5, 6, 22, 6)),
        shell(rect(4.5, 4.5, 3, 16)), shell(rect(16.5, 4.5, 3, 16)),
        line(seg(7.5, 10, 16.5, 10)), line(seg(7.5, 16, 16.5, 16)),
        dot(12, 10, 1.5), dot(12, 16, 1.5),
    ]


@icon("mine-rescuer", CAT, "Rescuer in a hard hat with a head lamp and a breathing pack on the chest",
      tags=["mine rescue", "miner", "hard hat", "head lamp", "breathing pack", "underground rescue"])
def _(S):
    hat = union("M7.5 10.5A4.5 6 0 0 1 16.5 10.5Z", rect(5.5, 10, 13, 2.5, L(S, 0.3, 1.2)))
    return [
        shell(hat),
        dot(12, 6.75, 1.2),
        shell(rect(6.5, 15, 11, 6.5, L(S, 1, 3))),
        mark(rect(9.5, 16.75, 5, 3)),
    ]


@icon("first-aider", CAT, "Person with an armband carrying a small first-aid bag marked with a plus",
      tags=["first aid", "medic", "volunteer", "emergency care", "responder", "helper"])
def _(S):
    return [
        head(10, 4.5),
        shell(rect(7, 8, 6, 9, rr(S, 2))),
        line(seg(7, 9.5, 4.5, 14.5)),
        mark(rect(4.75, 10, 3.25, 1.75)),
        line(seg(13, 10, 15.5, 13)),
        shell(rect(15, 13, 7, 6.5, rr(S, 1.5))),
        mark(rect(17.75, 14.25, 1.5, 3.5)), mark(rect(16.75, 15.25, 3.5, 1.5)),
        line(seg(8.5, 17, 8.5, 21.5)), line(seg(11.5, 17, 11.5, 21.5)),
    ]


@icon("rescue-swimmer-tow", CAT, "Swimmer towing a second person on their back across the water by holding them under the arms",
      tags=["lifeguard tow", "water rescue", "swim rescue", "drowning", "save swimmer", "surf rescue"])
def _(S):
    return [
        dot(18.5, 8.5, 1.8),
        line(seg(16.5, 10.5, 9, 13)),
        dot(12.5, 15.5, 1.8),
        line(poly([(13.5, 16), (16.5, 11.5)])),
        line(seg(10.5, 16.5, 4, 18.75)),
        line("M2 21.5Q5 19.75 8 21.5T14 21.5T20 21.5"),
    ]


@icon("aed-wall-cabinet", CAT, "Wall cabinet with a glass door showing a heart with a lightning bolt",
      tags=["defibrillator cabinet", "aed box", "heart starter", "public access", "cardiac", "emergency equipment"])
def _(S):
    heart = "M12 18.5C5.5 14 6 8.5 9.2 8.5C10.8 8.5 12 9.7 12 11C12 9.7 13.2 8.5 14.8 8.5C18 8.5 18.5 14 12 18.5Z"
    return [
        shell(rect(3.5, 3, 17, 18, rr(S, 3))),
        detail(heart),
        mark(poly([(12.9, 10.8), (10.6, 13.8), (12.3, 13.8), (11.2, 16.3), (13.6, 13), (11.9, 13)], closed=True)),
    ]


@icon("air-ambulance-plane", CAT, "Small propeller plane in side view with a medical cross on its body",
      tags=["air ambulance", "medevac", "rescue plane", "flying doctor", "patient transport", "aircraft"])
def _(S):
    k, d = 0.62, 45
    pts = [(12, 2.5), (13.5, 6), (13.5, 10), (21.5, 14.5), (21.5, 16.5), (13.5, 14.5), (13.5, 18.5), (16.5, 20.5),
           (16.5, 22), (12, 21), (7.5, 22), (7.5, 20.5), (10.5, 18.5), (10.5, 14.5), (2.5, 16.5), (2.5, 14.5),
           (10.5, 10), (10.5, 6)]
    pts = [(12 + (x - 12) * k - 1.5, 12 + (y - 12) * k - 1.5) for x, y in pts]
    return [
        shell(poly(rpts(pts, d), closed=True, r=S.r * 0.3), stroke_miterlimit="3"),
        line("M18.5 15.5V22M15.5 18.75H21.5"),
    ]
