"""TypeIcon Core: vehicles (batch 004, specialty vehicles, parts and views).

Same conventions as sets/vehicles_001.py: side-view road vehicles face right, wheels are rings on a common
ground line, bodies are left open where they meet a wheel, and Filled cuts the body clear of solid wheels.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    pt_on, rect, regular, seg, shell, solid,
)
from geometry import rotation, transform_path

CAT = "vehicles"
FILL = Style("filled", "butt", "miter", R=2.0, r=0.0)  # pseudo-style: Line geometry for Filled designs


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line/Filled (a) or Rounded (b)."""
    return b if S.name == "rounded" else a


def isF(S):
    return S.name == "filled"


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpt(p, deg, c=(12.0, 12.0)):
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a)


def T(name, description, tags, aliases=()):
    """Register an icon whose Filled design is derived from its Line geometry."""
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases,
                    filled=lambda: filled_region(fn(FILL)))(fn)
    return deco


def wheel(x, y=18.0, r=2.0):
    """Side-view wheel: a ring in Line/Rounded; a solid disc cut 1 px clear of the body in Filled."""
    p = shell(circle(x, y, r))
    p.wheel = (x, y, r)
    return p


def hub(x, y, r=1.0):
    """Hub mark inside a big wheel: solid in Line/Rounded, a hole in the Filled disc."""
    p = dot(x, y, r)
    p.knock = True
    return p


def body(S, pts, ws, yb=None, r=None):
    """Side-view body. `pts` run clockwise from the bottom-left corner over the top to the bottom-right corner
    (both on y = yb); the bottom edge is left open where a wheel crosses it."""
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
    """Register a wheeled vehicle whose Filled design cuts the wheels clear of the body."""
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=veh_filled(fn))(fn)
    return deco


W2 = [(6.5, 18, 2), (17.5, 18, 2)]  # standard car wheels


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def wrap_belt(pulleys):
    """Closed belt path around pulleys (cx, cy, r, o); o = +1 wraps clockwise on screen, -1 counter-clockwise.
    Pulleys are listed in the order the belt visits them."""
    n = len(pulleys)
    links = []
    for i in range(n):
        a, b = pulleys[i], pulleys[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy)
        phi = math.atan2(dy, dx)
        pick = None
        for sg in (1, -1):
            si, sj = a[3] * sg, b[3] * sg
            c = (si * a[2] - sj * b[2]) / d
            if abs(c) > 1:
                continue
            for th in (phi + math.acos(c), phi - math.acos(c)):
                nx, ny = math.cos(th), math.sin(th)
                pi = (a[0] + si * a[2] * nx, a[1] + si * a[2] * ny)
                pj = (b[0] + sj * b[2] * nx, b[1] + sj * b[2] * ny)
                ti = (-a[3] * si * ny, a[3] * si * nx)
                if (pj[0] - pi[0]) * ti[0] + (pj[1] - pi[1]) * ti[1] > 0:
                    pick = (pi, pj)
        links.append(pick)
    out = []
    for i in range(n):
        c = pulleys[i]
        p_in = links[i - 1][1]
        p_out = links[i][0]
        a_in = math.atan2(p_in[1] - c[1], p_in[0] - c[0])
        a_out = math.atan2(p_out[1] - c[1], p_out[0] - c[0])
        sw = ((a_out - a_in) if c[3] > 0 else (a_in - a_out)) % (2 * math.pi)
        out.append(("M" if i == 0 else "L") + f"{fmt(p_in[0])} {fmt(p_in[1])}")
        out.append(f"A{fmt(c[2])} {fmt(c[2])} 0 {1 if sw > math.pi else 0} {1 if c[3] > 0 else 0} "
                   f"{fmt(p_out[0])} {fmt(p_out[1])}")
    return "".join(out) + "Z"


# =========================================================================== chunk 1

@icon("fifth-wheel-hitch", CAT, "Horseshoe-shaped coupling plate with a V slot and two mounting bolts",
      tags=["fifth wheel", "trailer hitch", "truck coupling", "semi hitch", "towing", "coupling plate"])
def _(S):
    if S.name == "line":
        plate = "M3 21V12A9 9 0 0 1 21 12V21H15L12 11.5L9 21Z"
    else:
        plate = "M3 19.5V12A9 9 0 0 1 21 12V19.5Q21 21 19.5 21H15.5Q14.7 21 14.4 20.2L12.6 12.6Q12 11 11.4 12.6L9.6 20.2Q9.3 21 8.5 21H4.5Q3 21 3 19.5Z"
    return [shell(plate), dot(12, 7, 1.5), dot(6, 16, 1.25), dot(18, 16, 1.25)]


@icon("aerial-ladder-truck", CAT, "Fire truck with a long ladder raised diagonally from a turntable",
      tags=["fire truck", "ladder truck", "fire engine", "fire brigade", "rescue", "aerial ladder"])
def _(S):
    pts = [(2.5, 18), (2.5, 12.5), (13, 12.5), (13, 9), (17.5, 9), (21, 12.5), (21, 18)]
    bx, by, tx, ty = 4.5, 11.5, 14.5, 3.5
    L_ = math.hypot(tx - bx, ty - by)
    nx, ny = -(ty - by) / L_ * 2.0, (tx - bx) / L_ * 2.0
    rails = [line(seg(bx + nx, by + ny, tx + nx, ty + ny)), line(seg(bx - nx, by - ny, tx - nx, ty - ny))]
    rungs = [line(seg(bx + (tx - bx) * f + nx, by + (ty - by) * f + ny, bx + (tx - bx) * f - nx,
                      by + (ty - by) * f - ny)) for f in (0.4, 0.75)]
    return body(S, pts, W2) + [wheel(*w) for w in W2] + [detail(seg(13, 12.5, 13, 18))] + rails + rungs
@icon("rollback-tow-truck", CAT, "Tow truck with its flat bed tilted to the ground and a small car on it",
      tags=["tow truck", "flatbed tow", "car recovery", "breakdown", "wrecker", "roadside assistance"])
def _(S):
    pts = [(10.5, 18), (10.5, 14), (14, 14), (14, 8.5), (18, 8.5), (21.5, 13), (21.5, 18)]
    ws = [(13, 18, 1.5), (19, 18, 1.5)]
    ox, oy = 2.5, 19.0
    ex, ey = 10.5, 14.0
    ang = math.atan2(ey - oy, ex - ox)
    ca, sa = math.cos(ang), math.sin(ang)
    car = [(1.5, 0), (1.5, -2.5), (3, -3), (4, -4.8), (6.5, -4.8), (7.5, -3), (9, -2.5), (9, 0)]
    cp = [(ox + x * ca - y * sa, oy + x * sa + y * ca) for x, y in car]
    return (body(S, pts, ws) + [wheel(*w) for w in ws] +
            [line(seg(ox, oy, ex, ey)), line(poly(cp, r=S.r * 0.5)),
             detail(poly([(16.5, 8.5), (16.5, 13), (21.5, 13)], r=S.r * 0.5))])


@veh("kei-truck", "Tiny flat-nosed mini truck with a cab over the front wheels and a low drop-side bed",
     ["mini truck", "kei", "microtruck", "small pickup", "cab over", "japanese truck", "farm truck"],
     aliases=["mini-truck"])
def _(S):
    pts = [(3, 18), (3, 10.5), (12, 10.5), (12, 6), (18, 6), (21, 10.5), (21, 18)]
    return auto(S, pts, W2, detail(seg(3, 13.5, 12, 13.5)), detail(poly([(14.5, 6), (14.5, 10.5), (21, 10.5)], r=S.r * 0.5)))


@veh("utility-terrain-vehicle", "Two-seat off-road utility vehicle with a roll cage, big tires and a cargo bed",
     ["utv", "side by side", "off road", "buggy", "farm vehicle", "ranch", "atv", "rzr"], aliases=["utv"])
def _(S):
    ws = [(6.5, 17.5, 3), (17.5, 17.5, 3)]
    pts = [(3, 17.5), (3, 11), (14, 11), (15.5, 13), (21, 13), (21, 17.5)]
    return auto(S, pts, ws, line(poly([(9, 11), (9.8, 4.5), (15, 4.5), (15, 11)], r=S.r * 0.5)),
                line(poly([(3, 11), (3, 8), (6.5, 8), (6.5, 11)], r=S.r * 0.5)), hub(6.5, 17.5), hub(17.5, 17.5), yb=17.5)


@veh("solar-car", "Very flat wide race car covered in solar cells with a small canopy",
     ["solar vehicle", "solar powered", "eco car", "green energy", "electric", "race"],
      aliases=["solar-powered-car"])
def _(S):
    ws = [(6, 18.5, 2), (18, 18.5, 2)]
    return (body(S, [(2, 17), (2, 12.5), (22, 12.5), (22, 17)], ws, yb=17) + [wheel(*w) for w in ws] +
            [shell("M13 12.5A3.5 4 0 0 1 20 12.5Z"), detail(seg(6, 12.5, 6, 17)), detail(seg(10, 12.5, 10, 17))])


@icon("sleigh", CAT, "Horse sleigh with long curled runners and a curved seat with a high scrolled back",
      tags=["sleigh", "sled", "winter", "christmas", "santa", "snow", "horse drawn", "slay"])
def _(S):
    seat = "M5 5.5Q5 15 11 15H20Q20 11 16 11H9.5Q8.5 8 5 5.5Z"
    if S.name == "rounded":
        seat = "M5.5 5.5Q5 15 11 15H19.5Q20 11 16 11H9.5Q8.5 8 5.5 5.5Z"
    return [shell(seat), line("M2.5 16.5Q3 19.5 6 19.5H19Q22 19.5 22 16"),
            line(seg(8, 15, 8, 19.5)), line(seg(16.5, 15, 16.5, 19.5))]


@icon("semi-trailer", CAT, "Long box trailer on its own with rear wheels and folding landing legs at the front",
      tags=["trailer", "semi trailer", "freight", "haulage", "cargo", "lorry trailer", "container"])
def _(S):
    ws = [(12.5, 18.5, 1.75), (18.5, 18.5, 1.75)]
    pts = [(2.5, 15.5), (2.5, 4.5), (21, 4.5), (21, 15.5)]
    return (body(S, pts, ws, yb=15.5) + [wheel(*w) for w in ws] +
            [detail(seg(7.5, 4.5, 7.5, 15.5)), detail(seg(13, 4.5, 13, 15.5)), line(seg(5.5, 15.5, 5.5, 20)), line(seg(3.5, 20, 7.5, 20))])


@icon("car-ramps", CAT, "Stepped wedge ramp with a car tire resting on top",
      tags=["wheel ramps", "oil change", "garage", "car lift", "tire", "mechanic", "incline"])
def _(S):
    ramp = poly([(2, 20.5), (2, 18), (7, 18), (7, 15), (12, 15), (12, 12), (22, 12), (22, 20.5)], closed=True, r=S.r * 0.5)
    return [shell(ramp), shell(circle(17, 7.5, 4)), dot(17, 7.5, 1.25)]


@icon("oil-drain-pan", CAT, "Shallow drain pan with a drop of oil falling into it",
      tags=["oil change", "drain pan", "motor oil", "garage", "mechanic", "catch pan", "drip"])
def _(S):
    pan = poly([(2.5, 13.5), (21.5, 13.5), (19.5, 20), (4.5, 20)], closed=True, r=S.r)
    if S.name == "line":
        drop = "M12 2.5L8.5 7.8A3.5 3.5 0 1 0 15.5 7.8Z"
    else:
        drop = "M12 2.5Q10.5 4.5 8.5 7.8A3.5 3.5 0 1 0 15.5 7.8Q13.5 4.5 12 2.5Z"
    return [shell(pan), shell(drop), detail(seg(6, 16.8, 18, 16.8))]


@icon("ev-battery", CAT, "Flat electric vehicle battery pack divided into cell modules, with a plus sign",
      tags=["battery pack", "electric car", "traction battery", "lithium", "cells", "ev", "power"],
      aliases=["traction-battery"])
def _(S):
    return [shell(rect(2, 6, 20, 12, S.R)), detail(seg(8, 6, 8, 18)), detail(seg(14, 6, 14, 18)),
            detail(seg(2, 12, 14, 12)), detail(seg(18, 9.5, 18, 14.5)), detail(seg(15.5, 12, 20.5, 12))]


@icon("car-cup-holder", CAT, "Cup holder cradle in a car console with a takeaway cup sitting in it",
      tags=["cup holder", "drink holder", "coffee", "car interior", "console", "takeaway cup", "beverage"])
def _(S):
    u = "M3 12V17.5A3 3 0 0 0 6 20.5H18A3 3 0 0 0 21 17.5V12" if S.name == "rounded" else "M3 12V20.5H21V12"
    return [line(u), shell(poly([(7, 7), (17, 7), (15.5, 16.5), (8.5, 16.5)], closed=True, r=S.r * 0.5)),
            line(seg(6, 4.5, 18, 4.5))]


@icon("coolant-reservoir", CAT, "Translucent coolant overflow tank with a cap, min and max marks and a liquid level",
      tags=["coolant", "overflow tank", "antifreeze", "radiator", "engine", "expansion tank", "cooling system"])
def _(S):
    return [shell(rect(5, 6, 14, 15, min(S.R, 2))), shell(rect(9, 2, 6, 4, min(S.R, 1))),
            detail(seg(7.5, 10, 11, 10)), detail(seg(7.5, 18, 11, 18)),
            detail("M5 14Q8.5 12.5 12 14T19 14")]


BELT_PULLEYS = [(5.5, 6.5, 3.5, 1), (12, 8.5, 2.5, -1), (18.5, 6.5, 3.5, 1), (12, 18, 4, 1)]


def _belt_filled():
    d = wrap_belt(BELT_PULLEYS)
    return U(ST(d, 2.5, "round", "round"), P(circle(12, 18, 2)), P(circle(5.5, 6.5, 1.5)), P(circle(18.5, 6.5, 1.5)))


@icon("serpentine-belt", CAT, "One long belt winding around three pulleys and dipping under a small idler",
      tags=["drive belt", "engine belt", "fan belt", "accessory belt", "pulley", "alternator", "mechanic"],
      aliases=["fan-belt"], filled=_belt_filled)
def _(S):
    hub = shell(circle(12, 18, 1.5)) if S.name == "line" else dot(12, 18, 1.75)
    return [shell(wrap_belt(BELT_PULLEYS)), hub, dot(5.5, 6.5, 1.25), dot(18.5, 6.5, 1.25)]



# =========================================================================== chunk 2

@icon("head-gasket", CAT, "Flat engine head gasket plate with four round cylinder holes in a row and small bolt holes",
      tags=["engine gasket", "cylinder head", "blown head gasket", "engine repair", "seal", "mechanic", "motor"])
def _(S):
    parts = [shell(rect(2, 5, 20, 14, S.R))]
    parts += [dot(x, 12, 1.65) for x in (5.6, 9.9, 14.2, 18.5)]
    parts += [dot(x, y, 0.9) for x in (7.75, 12.05, 16.35) for y in (8, 16)]
    return parts


@icon("bike-bottle-cage", CAT, "Water bottle held in a wire cage mounted on a bicycle frame tube",
      tags=["bottle holder", "bicycle", "cycling", "water bottle", "bike accessory", "hydration", "cage"])
def _(S):
    bottle = "M10 5V7L8 9V14.5H16V9L14 7V5Z" if S.name == "line" else "M10 5V7L8 9V13.5Q8 14.5 9 14.5H15Q16 14.5 16 13.5V9L14 7V5Z"
    cage = "M4.5 9V17.5H19.5V9" if S.name == "line" else "M4.5 9V16.5Q4.5 17.5 5.5 17.5H18.5Q19.5 17.5 19.5 16.5V9"
    return [shell(bottle), shell(rect(10, 2.5, 4, 2.5, 0.5)), line(cage), line(seg(2, 21, 22, 21))]


@icon("cafe-racer-motorcycle", CAT, "Stripped-down retro motorcycle with a round headlight, low bars and a humped single seat",
      tags=["cafe racer", "retro motorcycle", "vintage bike", "motorbike", "custom bike", "ton up", "classic motorcycle"],
      aliases=["cafe-racer"])
def _(S):
    seat_tank = poly([(2.5, 11.5), (4, 8.5), (8, 9), (14, 9), (14.5, 12)], closed=True, r=S.r)
    return [shell(circle(5.75, 17, 3.25)), shell(circle(18.25, 17, 3.25)), dot(5.75, 17, 1), dot(18.25, 17, 1),
            shell(seat_tank), line(seg(18.25, 17, 16, 8.5)), line(seg(16, 8.5, 13.5, 7.5)),
            line(seg(5.75, 17, 8, 12)), line(poly([(10, 12.5), (12.5, 17)], r=0)), dot(19.5, 10, 1.5)]


@veh("safari-vehicle", "Open-sided four-by-four with raised tiered bench seats under a flat canvas roof",
     ["safari jeep", "game drive", "jeep", "4x4", "wildlife tour", "africa", "open truck", "tour vehicle"],
     aliases=["safari-jeep"])
def _(S):
    ws = [(7, 18, 2.5), (17, 18, 2.5)]
    pts = [(3, 18), (3, 13.5), (21, 13.5), (21, 18)]
    return auto(S, pts, ws, line(seg(2.5, 4.5, 17.5, 4.5)), line(seg(4, 4.5, 4, 13.5)), line(seg(10.5, 4.5, 10.5, 13.5)),
                line(seg(17.5, 4.5, 17.5, 13.5)), sq(5.5, 8, 2, 5.5), sq(12, 10, 2, 3.5))


@veh("bucket-truck", "Utility truck with a folding boom arm rising from its bed to a small worker bucket",
     ["cherry picker", "boom truck", "lineman", "utility truck", "aerial work platform", "power line repair", "lift truck"],
     aliases=["cherry-picker-truck"])
def _(S):
    pts = [(2.5, 18), (2.5, 13), (12.5, 13), (12.5, 10.5), (17.5, 10.5), (21, 13.5), (21, 18)]
    return auto(S, pts, W2, detail(seg(12.5, 13, 12.5, 18)),
                line(poly([(5, 13), (9.5, 6.5), (14.5, 5)], r=S.r * 0.5)),
                shell(poly([(14, 3), (20, 3), (19, 7), (15, 7)], closed=True, r=S.r * 0.3)))


@veh("land-yacht", "Three-wheeled sail cart with a tall triangular sail and a low seat",
     ["sand yacht", "land sailing", "beach buggy", "wind powered", "sail cart", "kite buggy", "beach sailing"],
     aliases=["sand-yacht"])
def _(S):
    ws = [(6, 19.5, 1.75), (18, 19.5, 1.75)]
    return [wheel(*ws[0]), wheel(*ws[1]), line(seg(2.5, 15, 21.5, 15)),
            shell(poly([(9, 3), (9, 11.5), (20, 11.5)], closed=True, r=S.r * 0.5)), line(seg(9, 11.5, 9, 15)),
            line(seg(4, 15, 4, 11))]


@icon("traction-boards", CAT, "Two ribbed recovery boards wedged under a tire stuck in sand",
      tags=["recovery boards", "off road", "stuck", "sand", "mud", "4x4", "self recovery", "maxtrax"])
def _(S):
    def plank(a, b, w, ribs):
        L_ = math.hypot(b[0] - a[0], b[1] - a[1])
        nx, ny = -(b[1] - a[1]) / L_ * w, (b[0] - a[0]) / L_ * w
        pts = [(a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny), (b[0] - nx, b[1] - ny), (a[0] - nx, a[1] - ny)]
        out = [shell(poly(pts, closed=True, r=S.r * 0.3))]
        for f in ribs:
            cx, cy = a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
            out.append(detail(seg(cx + nx, cy + ny, cx - nx, cy - ny)))
        return out
    return ([shell(circle(12, 8, 5)), dot(12, 8, 1.4)] + plank((3.5, 19.5), (10, 16.5), 2.2, (0.35, 0.7)) +
            plank((20.5, 19.5), (14, 16.5), 2.2, (0.35, 0.7)))


@icon("forward-collision-warning", CAT, "Car seen from behind with a starburst warning mark just ahead of it",
      tags=["collision warning", "crash alert", "adas", "driver assistance", "safety", "brake warning", "car safety"],
      aliases=["fcw"])
def _(S):
    car = poly([(4, 21), (4, 16.5), (6.5, 13), (17.5, 13), (20, 16.5), (20, 21)], closed=True, r=S.r)
    star = regular(12, 6.5, 4.5, 8)
    star = [pt_ for i in range(8) for pt_ in (pt_on(12, 6.5, 4.5, -90 + i * 45), pt_on(12, 6.5, 2.2, -67.5 + i * 45))]
    return [shell(car), detail(seg(4, 16.5, 20, 16.5)), sq(6.5, 18, 3, 1.5), sq(14.5, 18, 3, 1.5),
            solid(poly(star, closed=True))]


@icon("bus-side", CAT, "City bus seen from the side with a row of windows, doors and two wheels",
      tags=["bus", "city bus", "public transport", "transit", "coach", "side view", "commuter"],
      aliases=["city-bus-side"])
def _(S):
    pts = [(2, 18), (2, 5.5), (19.5, 5.5), (21.5, 9), (21.5, 18)]
    ws = [(6.5, 18, 2), (17.5, 18, 2)]
    return (body(S, pts, ws) + [wheel(*w) for w in ws] +
            [detail(seg(2, 11, 21.5, 11)), sq(4, 7.5, 3, 1.8), sq(8.5, 7.5, 3, 1.8), sq(13, 7.5, 3, 1.8), sq(17.5, 7.5, 2.2, 1.8),
             detail(seg(10.5, 11, 10.5, 16)), detail(seg(13.5, 11, 13.5, 16))])


@icon("truck-front", CAT, "Lorry cab seen straight from the front with a tall windshield, grille, mirrors and headlights",
      tags=["lorry", "truck front", "cab", "hgv", "freight", "haulage", "head on view"])
def _(S):
    return [shell(rect(5.5, 3, 13, 15.5, min(S.R, 3))), detail(seg(5.5, 10, 18.5, 10)),
            sq(9.5, 13, 5, 3), dot(7.5, 14.5, 1.1), dot(16.5, 14.5, 1.1),
            line(seg(3, 5, 3, 11)), line(seg(3, 8, 5.5, 8)), line(seg(21, 5, 21, 11)), line(seg(21, 8, 18.5, 8)),
            solid(rect(6.5, 18.5, 3, 3.5)), solid(rect(14.5, 18.5, 3, 3.5))]


@icon("car-rear", CAT, "Car seen straight from behind with a rear window, two tail lights, a license plate and tire bottoms",
      tags=["rear view", "back of car", "tail lights", "number plate", "license plate", "car behind", "vehicle"],
      aliases=["car-back"])
def _(S):
    body_ = poly([(3, 18), (3, 12.5), (5, 12.5), (7, 6.5), (17, 6.5), (19, 12.5), (21, 12.5), (21, 18)], closed=True, r=S.r)
    return [shell(body_), sq(8.8, 8.5, 6.4, 2.5), sq(4.5, 13.5, 3, 2), sq(16.5, 13.5, 3, 2), sq(9.5, 14, 5, 2.4),
            solid(rect(5, 18.5, 3.5, 3)), solid(rect(15.5, 18.5, 3.5, 3))]


@icon("tall-bike", CAT, "Bicycle built from two frames stacked on top of each other with a very high seat and handlebars",
      tags=["tall bike", "stacked bike", "bicycle", "cycling", "custom bike", "festival", "high bike"])
def _(S):
    return [shell(circle(5.5, 18.5, 2.75)), shell(circle(18.5, 18.5, 2.75)), dot(5.5, 18.5, 0.8), dot(18.5, 18.5, 0.8),
            line(poly([(5.5, 18.5), (10, 12), (15.5, 12), (18.5, 18.5)], r=S.r * 0.5)),
            line(seg(5.5, 18.5, 12, 18.5)), line(seg(12, 18.5, 15.5, 12)),
            line(poly([(10, 12), (9, 5), (16, 5), (15.5, 12)], r=S.r * 0.5)),
            line(seg(5.5, 5, 9, 5)), line(seg(16, 5, 19.5, 5))]


@icon("car-fuse-box", CAT, "Open fuse box with a grid of small plug-in fuses and a raised hinged lid",
      tags=["fuse box", "fuse panel", "car electrics", "fuses", "relay box", "wiring", "mechanic"])
def _(S):
    return ([shell(rect(3, 10, 18, 11.5, min(S.R, 2))),
             shell(poly([(5.5, 2.5), (18.5, 2.5), (21, 7), (3, 7)], closed=True, r=S.r * 0.5))] +
            [Part("dot", rect(x, y, 2, 2.5)) for x in (6.2, 10, 13.8, 17.6) for y in (13, 17)])


@icon("control-arm", CAT, "A-shaped suspension wishbone arm with round bushings at the two inner ends and a ball joint at the tip",
      tags=["wishbone", "suspension arm", "a arm", "bushing", "ball joint", "chassis", "car repair"],
      aliases=["wishbone-arm"])
def _(S):
    tip = (17, 12)
    ends = [(5.5, 5.5), (5.5, 18.5)]
    parts = []
    rr = 2.75
    for e in ends:
        dx, dy = tip[0] - e[0], tip[1] - e[1]
        d = math.hypot(dx, dy)
        parts.append(line(seg(e[0] + dx / d * rr, e[1] + dy / d * rr, tip[0], tip[1])))
        parts.append(shell(circle(e[0], e[1], rr)))
        parts.append(dot(e[0], e[1], 1.1))
    parts.append(dot(tip[0], tip[1], 2.2))
    parts.append(line(seg(tip[0], tip[1], 22, 12)))
    parts.append(line(seg(11, 8.7, 11, 15.3)))
    return parts


