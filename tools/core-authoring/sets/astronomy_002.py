"""TypeIcon Core: astronomy (batch 002, crewed spaceflight, surface missions, hardware and sky watching).

Visual language (shared with sets/space.py): planets and bodies are circles, spacecraft are simple boxes and
cones, ground is a single line near y 21, stars are small four point sparkles or solid dots.
"""
from __future__ import annotations

import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "astronomy"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled shell."""
    return Part("dot", d)


def arrowhead(tip, deg, S, size=2.6, spread=40):
    """Open arrowhead at `tip` pointing along `deg` (0 = right, 90 = down)."""
    a = polar(tip[0], tip[1], size, deg + 180 - spread)
    b = polar(tip[0], tip[1], size, deg + 180 + spread)
    return line(poly([a, tip, b], r=S.r * 0.4))


def sparkle(cx, cy, r, S, k=0.3):
    """Four point star as a small solid mark (sharp in Line, softened in Rounded)."""
    pts = []
    for i in range(8):
        rr = r if i % 2 == 0 else r * k
        pts.append(polar(cx, cy, rr, -90 + i * 45))
    return solid(poly(pts, closed=True, r=S.r * 0.2))


def star5(cx, cy, ro, ri=None, start=-90):
    ri = ro * 0.45 if ri is None else ri
    return [polar(cx, cy, ro if i % 2 == 0 else ri, start + i * 36) for i in range(10)]


def visible_arcs(balls, gap=1.5, step=2.0):
    """Arcs of circles (front first) that are not hidden behind an earlier circle: [(cx, cy, r, a0, a1)]."""
    out = []
    for i, (cx, cy, r) in enumerate(balls):
        n = int(360 / step)
        vis = []
        for k in range(n):
            x, y = polar(cx, cy, r, k * step)
            vis.append(all(math.hypot(x - bx, y - by) > br + gap for bx, by, br in balls[:i]))
        if all(vis):
            out.append((cx, cy, r, None, None))
            continue
        if not any(vis):
            continue
        k0 = vis.index(False)
        cur = None
        for j in range(1, n + 1):
            k = (k0 + j) % n
            if vis[k] and cur is None:
                cur = k0 + j
            elif not vis[k] and cur is not None:
                out.append((cx, cy, r, cur * step, (k0 + j - 1) * step))
                cur = None
        if cur is not None:
            out.append((cx, cy, r, cur * step, (k0 + n) * step))
    return out


def arcs_d(arcs):
    return [circle(cx, cy, r) if a0 is None else arc(cx, cy, r, a0, a1) for cx, cy, r, a0, a1 in arcs]


def ground(y=20.0, x0=2.0, x1=22.0):
    """Thin ground slab to union with a shell (avoids a line lying exactly on a shell's flat bottom)."""
    return rect(x0, y - 0.25, x1 - x0, 0.5, 0)


# ============================================================================ crew life and training

@icon("space-dog", CAT, "Dog head inside a round space helmet with a small antenna",
      tags=["space dog", "animal astronaut", "dog", "helmet", "spaceflight", "pet"])
def _(S):
    ear_r = L(S, "L17.2 10.6L16.9 15.2L15.4 14", "L17.2 10.6Q17.4 15.2 15.4 14")
    ear_l = L(S, "L8.6 14L7.1 15.2L6.8 10.6", "L8.6 14Q6.6 15.2 6.8 10.6")
    dog = ("M9.3 10.2C10.8 9.2 13.2 9.2 14.7 10.2" + ear_r +
           "L15.4 16.2C15.4 18.2 13.8 19.2 12 19.2C10.2 19.2 8.6 18.2 8.6 16.2" + ear_l + "Z")
    return [
        shell(circle(12, 13, 8.5)),
        detail(dog),
        dot(10.5, 13.2, 0.85), dot(13.5, 13.2, 0.85),
        mark(ellipse(12, 16.4, 1.3, 0.9)),
        line(seg(17.5, 6.5, 19.2, 4)),
        dot(19.6, 3.3, 1.3),
    ]


@icon("space-sleeping-bag", CAT, "Sleeping bag strapped upright to a wall with a head poking out",
      tags=["sleeping bag", "crew quarters", "sleep", "astronaut", "space station", "rest"])
def _(S):
    rb = L(S, 2, 4)
    bag = (f"M6.5 8A6 6 0 0 0 17.5 8V{21.5 - rb}A{rb} {rb} 0 0 1 {17.5 - rb} 21.5H{6.5 + rb}"
           f"A{rb} {rb} 0 0 1 6.5 {21.5 - rb}Z")
    out = [shell(circle(12, 5, 2.75)), shell(bag)]
    for y in (13.5, 18):
        out += [detail(seg(6.5, y, 17.5, y)), line(seg(2.5, y, 6.5, y)), line(seg(17.5, y, 21.5, y))]
    return out


@icon("space-toilet", CAT, "Compact space toilet bowl with a suction hose and funnel",
      tags=["space toilet", "waste collection", "bathroom", "restroom", "space station", "hygiene"])
def _(S):
    bowl = L(S, "M3 11H15V12C15 14.8 13.4 16.6 11 17.1L11.5 21H5.5L6 17C4 16.2 3 14.4 3 12Z",
             "M4.5 11H13.5A1.5 1.5 0 0 1 15 12.5C15 14.8 13.4 16.6 11 17.1L11.5 21H5.5L6 17C4 16.2 3 14.4 3 12.5A1.5 1.5 0 0 1 4.5 11Z")
    return [
        shell(bowl),
        detail(seg(3, 11, 15, 11)),
        line(L(S, "M15 13.5H19V8", "M15 13.5H17A2 2 0 0 0 19 11.5V8")),
        shell(poly([(16, 2.5), (22, 2.5), (20, 6.5), (18, 6.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("astronaut-training-centrifuge", CAT, "Long spinning arm with a capsule at its end and motion arrows",
      tags=["centrifuge", "g-force", "astronaut training", "pilot training", "spin", "acceleration"])
def _(S):
    c = (8.5, 13)
    return [
        shell(circle(*c, 2.5)),
        line(seg(11, 13, 15, 13)),
        shell(rect(15, 10, 6.5, 6, min(S.R, 3))),
        line(arc(*c, 7, 200, 285)),
        arrowhead(polar(*c, 7, 285), 15, S, 2.4),
        line(arc(*c, 7, 45, 130)),
        arrowhead(polar(*c, 7, 130), 220, S, 2.4),
    ]


@icon("cryosleep-pod", CAT, "Upright sleep capsule with a window over the sleeper and a frost mark",
      tags=["cryosleep", "hibernation", "stasis", "sci-fi", "sleep pod", "frozen"])
def _(S):
    sf = [seg(12, 14.3, 12, 20.3), seg(9.4, 15.8, 14.6, 18.8), seg(9.4, 18.8, 14.6, 15.8)]
    return [
        shell(rect(5.5, 2, 13, 20, L(S, 3, 6.5))),
        detail(rect(8, 4.5, 8, 7, L(S, 1, 3.5))),
        dot(12, 8, 1.5),
        *[detail(s) for s in sf],
    ]



@icon("mission-control", CAT, "Wall screen showing an orbit above desks with monitors",
      tags=["mission control", "control room", "flight control", "operations", "launch", "ground station"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 9.5, S.R)),
        detail(ellipse(12, 7.25, 5.5, 2.25)),
        dot(17.5, 7.25, 1.1),
        shell(poly([(4, 16), (10, 16), (9.3, 19), (4.7, 19)], closed=True, r=S.r * 0.4)),
        shell(poly([(14, 16), (20, 16), (19.3, 19), (14.7, 19)], closed=True, r=S.r * 0.4)),
        line(seg(2.5, 21.5, 21.5, 21.5)),
    ]


@icon("mars-lander", CAT, "Three legged lander with two round solar panels and a robotic arm",
      tags=["mars lander", "lander", "stationary lander", "planetary probe", "mars", "solar panels"])
def _(S):
    return [
        shell(rect(9, 9, 6, 4.5, min(S.R, 1.5))),
        shell(circle(4.5, 11.25, 2.75)), shell(circle(19.5, 11.25, 2.75)),
        line(seg(7.25, 11.25, 9, 11.25)), line(seg(15, 11.25, 16.75, 11.25)),
        line(seg(10, 13.5, 7, 20)), line(seg(14, 13.5, 17, 20)), line(seg(12, 13.5, 12, 20)),
        line(poly([(10.5, 9), (9.5, 4.5), (6, 3.5)], r=S.r * 0.5)),
    ]


@icon("rover-sky-crane", CAT, "Hovering platform with thrusters lowering a wheeled rover on cables",
      tags=["sky crane", "rover landing", "descent stage", "mars rover", "cables", "landing"])
def _(S):
    return [
        shell(rect(6, 3, 12, 4, min(S.R, 1.5))),
        line(seg(6, 7, 3.5, 10)), line(seg(18, 7, 20.5, 10)),
        line(seg(9, 7, 9, 12.5)), line(seg(15, 7, 15, 12.5)),
        shell(rect(5, 12.5, 14, 4, min(S.R, 1.5))),
        shell(circle(7, 19.5, 1.75)), shell(circle(12, 19.5, 1.75)), shell(circle(17, 19.5, 1.75)),
    ]


_BAGS = [(12, 13.5, 3.6), (7.5, 11, 3.6), (16.5, 11, 3.6), (12, 7.5, 3.6)]


def _bags_filled():
    body = None
    for x, y, r in reversed(_BAGS):  # paint back to front, each ball cut clear of the ones behind
        disc = P(circle(x, y, r + 1))
        body = disc if body is None else U(D(body, P(circle(x, y, r + 2.4))), disc)
    return U(body, ST(seg(3, 20.5, 21, 20.5), 2.5), ST(seg(5.5, 17.5, 4.5, 18.5), 2.5), ST(seg(18.5, 17.5, 19.5, 18.5), 2.5))


@icon("airbag-landing", CAT, "Cluster of round airbags bouncing on the ground",
      tags=["airbags", "landing", "bounce", "mars landing", "cushion", "impact"], filled=_bags_filled)
def _(S):
    out = [line(d) for d in arcs_d(visible_arcs(_BAGS, gap=1.0))]
    out += [line(seg(3, 20.5, 21, 20.5)), line(seg(5.5, 17.5, 4.5, 18.5)), line(seg(18.5, 17.5, 19.5, 18.5))]
    return out


@icon("rover-sample-tube", CAT, "Slim sealed sample tube with a cap and a soil core inside",
      tags=["sample tube", "core sample", "mars sample", "soil sample", "sealed tube", "rover"])
def _(S):
    cap = rect(8.5, 2, 7, 4, min(S.R, 1))
    tube = rect(9.5, 8, 5, 14, L(S, 1, 2.5))
    return [
        shell(rot(cap, 40)),
        shell(rot(tube, 40)),
        mark(rot(rect(10.5, 14, 3, 6.5, L(S, 0, 1.5)), 40)),
    ]


@icon("sample-return-capsule", CAT, "Blunt return capsule holding a sample canister under a small parachute",
      tags=["sample return", "return capsule", "reentry", "parachute", "capsule", "recovery"])
def _(S):
    body = L(S, "M8 11H16L20.5 18Q12 22 3.5 18Z", "M9 11H15Q16 11 16.5 11.9L20.5 18Q12 22 3.5 18L7.5 11.9Q8 11 9 11Z")
    return [
        shell(L(S, "M7.5 6A4.5 4 0 0 1 16.5 6Z", "M8.3 6A0.8 0.8 0 0 1 7.5 5.2A4.5 3.6 0 0 1 16.5 5.2A0.8 0.8 0 0 1 15.7 6Z")),
        line(seg(8.5, 7, 9.5, 9.5)), line(seg(15.5, 7, 14.5, 9.5)),
        shell(body),
        detail(rect(10, 13.5, 4, 4, L(S, 0, 1))),
    ]


@icon("moon-base", CAT, "Dome modules linked together on the lunar ground with a flag",
      tags=["moon base", "lunar base", "outpost", "colony", "habitat", "settlement"])
def _(S):
    domes = union("M3 20A3.75 3.75 0 0 1 10.5 20Z", rect(9.5, 17.5, 2, 2.5, 0),
                  "M10 20A5 5 0 0 1 20 20Z", ground(20, 2, 22))
    return [
        shell(domes),
        detail(L(S, "M13.5 20V17.5H16.5V20", "M13.5 20V18.5A1.5 1.5 0 0 1 16.5 18.5V20")),
        line(seg(15, 15, 15, 3)),
        shell(rect(15, 3, 5, 3.5, min(S.R, 0.8))),
    ]


@icon("mars-habitat", CAT, "Tall dome habitat with a door and ribs on rocky ground",
      tags=["mars habitat", "martian base", "habitat", "colony", "dome", "settlement"])
def _(S):
    hab = union("M5.5 20V10.5A6.5 6.5 0 0 1 18.5 10.5V20Z", ground(20, 2, 22))
    return [
        shell(hab),
        detail(seg(5.5, 10.5, 18.5, 10.5)),
        detail(seg(5.5, 14, 18.5, 14)),
        detail(L(S, "M10.5 20V17H13.5V20", "M10.5 20V18A1 1 0 0 1 11.5 17H12.5A1 1 0 0 1 13.5 18V20")),
        dot(21, 17.5, 1),
        dot(3.5, 16.5, 0.9),
    ]


def _sprout(x, y0, h, S):
    """Stem with two leaves (line centrelines)."""
    top = y0 - h
    return [f"M{fmt(x)} {fmt(y0)}V{fmt(top + 1)}",
            f"M{fmt(x)} {fmt(top + 2.5)}Q{fmt(x - 0.3)} {fmt(top)} {fmt(x - 2.5)} {fmt(top)}",
            f"M{fmt(x)} {fmt(top + 2.5)}Q{fmt(x + 0.3)} {fmt(top)} {fmt(x + 2.5)} {fmt(top)}"]


@icon("space-greenhouse", CAT, "Glass dome with a young plant growing inside",
      tags=["space farming", "greenhouse", "grow plants", "habitat", "food", "life support"])
def _(S):
    dome = union("M3 20A9 9 0 0 1 21 20Z", ground(20, 2, 22))
    leaf_l = L(S, "M12 17.5Q8.5 17.8 7.5 14.5Q11 14 12 17.5Z", "M12 17.5Q8.5 17.8 7.5 14.5Q11 14 12 17.5Z")
    return [
        shell(dome),
        detail(seg(12, 20, 12, 14.5)),
        detail(leaf_l),
        detail("M12 15Q12.5 11.8 16 12Q15.5 15.2 12 15Z"),
    ]


@icon("inflatable-habitat", CAT, "Bulging segmented module inflated from a station docking port",
      tags=["inflatable module", "expandable habitat", "space station", "module", "habitat", "inflatable"])
def _(S):
    body = union(rect(2.5, 9.5, 6, 5, min(S.R, 1)), ellipse(14.5, 12, 7, 7))
    return [
        shell(body),
        detail("M12 5.6Q10.2 12 12 18.4"),
        detail("M17 5.6Q18.8 12 17 18.4"),
    ]


@icon("rotating-space-habitat", CAT, "Wheel shaped station with spokes to a central hub and spin arrows",
      tags=["space wheel", "rotating station", "artificial gravity", "torus", "habitat", "spin"])
def _(S):
    c = (12, 12)
    out = [line(circle(12, 12, 6.5)), shell(circle(12, 12, 2))]
    for a in (45, 135, 225, 315):
        p0, p1 = polar(12, 12, 3, a), polar(12, 12, 6.5, a)
        out.append(line(seg(*p0, *p1)))
    out += [line(arc(*c, 9.75, 195, 255)), arrowhead(polar(*c, 9.75, 255), 345, S, 2.4),
            line(arc(*c, 9.75, 15, 75)), arrowhead(polar(*c, 9.75, 75), 165, S, 2.4)]
    return out


@icon("dyson-sphere", CAT, "Star surrounded by a partly built ring of panels",
      tags=["dyson sphere", "megastructure", "star", "sci-fi", "energy", "kardashev"])
def _(S):
    a0, a1 = 20, 290
    rin, rout = 6, 9.5
    p = polar(12, 12, rout, a0)
    q = polar(12, 12, rin, a1)
    shape = (f"M{fmt(p[0])} {fmt(p[1])}" + arc(12, 12, rout, a0, a1)[arc(12, 12, rout, a0, a1).index("A"):] +
             f"L{fmt(q[0])} {fmt(q[1])}A{rin} {rin} 0 1 0 " + " ".join(fmt(v) for v in polar(12, 12, rin, a0)) + "Z")
    out = [shell(shape)]
    for a in (74, 128, 182, 236):
        out.append(detail(seg(*polar(12, 12, rin, a), *polar(12, 12, rout, a))))
    out.append(sparkle(12, 12, 3.2, S, 0.38))
    return out


_ROCK = "M4 14.5C3.5 12 5.5 10.2 8 10.5C9.5 9.2 12.5 9.3 14 10.5C16.5 10 18.8 12 18.4 14.5C19.5 16.8 17.8 20.3 14.5 20.3C12.5 21.3 9 21.2 7.5 20C4.8 20 3 17.3 4 14.5Z"


@icon("asteroid-mining", CAT, "Lumpy asteroid with a drilling rig standing on top",
      tags=["asteroid mining", "space mining", "drill", "resources", "minerals", "asteroid"])
def _(S):
    rock = poly([(3, 15.5), (5.5, 11.5), (13.5, 10.5), (18, 12), (20.5, 16.5), (17.5, 20.5), (11, 21.5), (5, 19.5)],
                closed=True, r=S.r)
    return [
        shell(rock),
        line(poly([(7, 11.2), (9.5, 3), (12, 10.8)], r=S.r * 0.3), stroke_miterlimit="2"),
        line(seg(8, 7, 11, 7)),
        detail(seg(9.5, 11, 9.5, 16)),
        sparkle(18.5, 5, 2.75, S),
    ]


@icon("asteroid-deflection", CAT, "Small spacecraft striking an asteroid that is pushed onto a new path",
      tags=["planetary defense", "asteroid impact", "deflection", "kinetic impactor", "asteroid", "mission"])
def _(S):
    rock = "M6 7.5C6.5 5 9 3.5 11.5 4C14 3.5 16.2 5.5 15.8 8C16.8 10.5 15 13 12.5 12.8C10.5 14 7.2 13 6.8 10.8C5.5 10 5.5 8.5 6 7.5Z"
    return [
        shell(rock),
        detail(arc(11, 8.5, 2, 200, 340)),
        shell(rect(3, 17.5, 3.5, 3.5, min(S.R, 1))),
        line(seg(6.5, 16.5, 7.8, 15)),
        line(L(S, "M17.5 8C20 10 21 13 20.5 17", "M17.5 8C20 10 21 13 20.5 17")),
        arrowhead((20.5, 17.5), 95, S, 2.6),
    ]


@icon("terraforming", CAT, "Planet split into a barren cratered half and a living half",
      tags=["terraforming", "planet", "colonization", "habitable", "transform", "mars"])
def _(S):
    out = [shell(circle(12, 12, 9)), detail(seg(12, 3, 12, 21)),
           detail(circle(7.5, 9, 1.5)), dot(8, 15.5, 1.1)]
    out.append(detail(L(S, "M15 10Q15.2 7.2 18 7Q17.8 9.8 15 10Z", "M15 10Q15.2 7.2 18 7Q17.8 9.8 15 10Z")))
    out.append(detail("M14.5 15.5Q15.75 14.5 17 15.5T19.5 15.5"))
    return out


@icon("rover-wheel-tracks", CAT, "Two parallel ridged tyre tracks across sandy ground beside a rock",
      tags=["tire tracks", "tyre tracks", "rover", "footprint", "trail", "mars"])
def _(S):
    out = []
    for x in (6, 13):
        for y in (3.5, 8.5, 13.5, 18.5):
            out.append(line(poly([(x - 2.5, y + 2), (x, y), (x + 2.5, y + 2)], r=S.r * 0.4)))
    out.append(shell(L(S, "M17 20.5L18 16.5L21 15.5L22 19L21 20.5Z", "M17.5 20.5C16.5 20.5 17 16.8 18.2 16.3C19.5 15.3 21.6 16 21.8 18.2C22 19.8 21.5 20.5 20.5 20.5Z")))
    return out


@icon("lunar-drill", CAT, "Tripod drill rig boring a core into the lunar ground",
      tags=["lunar drill", "core drill", "moon drilling", "regolith", "sample", "excavation"])
def _(S):
    return [
        shell(rect(9.5, 2.5, 5, 4, min(S.R, 1))),
        line(seg(10, 6.5, 5, 14)), line(seg(14, 6.5, 19, 14)),
        line(seg(2, 14, 22, 14)),
        line(seg(12, 6.5, 12, 18)),
        shell(poly([(10.25, 18), (13.75, 18), (12, 21.5)], closed=True, r=S.r * 0.3)),
    ]


@icon("moon-rock-sample", CAT, "Rock sealed in a sample bag with a numbered label",
      tags=["moon rock", "lunar sample", "rock sample", "specimen", "geology", "sample bag"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, S.R)),
        detail(seg(3.5, 6.5, 20.5, 6.5)),
        mark(L(S, "M6.5 17L7.5 13L10.5 11.5L13 13.5L13.5 17L11 18.5Z",
                  "M6.7 16.3C6.3 14.3 7.5 12.3 9.7 11.8C11.9 11.3 13.5 13 13.5 15C13.5 17.3 12.3 18.5 10.3 18.5C8.3 18.5 7 17.8 6.7 16.3Z")),
        detail(rect(15, 10, 3, 5.5, L(S, 0, 0.5))),
    ]


@icon("regolith-printer", CAT, "Gantry printer spraying layers into a small dome on the ground",
      tags=["3d printing", "regolith", "construction", "moon base", "printer", "additive"])
def _(S):
    return [
        line(poly([(3, 21), (3, 3.5), (21, 3.5), (21, 21)], r=S.r)),
        shell(rect(10, 6.5, 4, 3.5, min(S.R, 1))),
        line(seg(12, 3.5, 12, 6.5)),
        line(seg(12, 11, 12, 12.5)),
        shell(union("M6.5 20A5.5 5.5 0 0 1 17.5 20Z", rect(6.5, 19.75, 11, 0.5, 0))),
        detail(seg(7.5, 17, 16.5, 17)),
    ]


@icon("ice-moon-probe", CAT, "Torpedo shaped probe melting down through an ice sheet into water",
      tags=["cryobot", "ice probe", "europa", "ocean world", "melt probe", "subsurface ocean"])
def _(S):
    probe = L(S, "M10 5A2 2 0 0 1 14 5V13L12 16L10 13Z", "M10 5A2 2 0 0 1 14 5V13Q14 13.6 13.6 14.2L12.6 15.6Q12 16.2 11.4 15.6L10.4 14.2Q10 13.6 10 13Z")
    return [
        shell(probe),
        line(seg(2, 6, 7.5, 6)), line(seg(16.5, 6, 22, 6)),
        line(seg(2, 12, 7.5, 12)), line(seg(16.5, 12, 22, 12)),
        line("M3 18Q4.75 16.5 6.5 18T10 18T13.5 18T17 18T20.5 18"),
        line("M3 21.5Q4.75 20 6.5 21.5T10 21.5T13.5 21.5T17 21.5T20.5 21.5"),
    ]


def _cloud(x, y, w):
    """Small flat cloud centreline (open at the bottom edge closed by a line)."""
    h = w * 0.33
    return (f"M{fmt(x)} {fmt(y)}A{fmt(h)} {fmt(h)} 0 0 1 {fmt(x + w * 0.35)} {fmt(y - h)}"
            f"A{fmt(w * 0.3)} {fmt(w * 0.3)} 0 0 1 {fmt(x + w * 0.85)} {fmt(y - h * 0.6)}"
            f"A{fmt(h * 0.8)} {fmt(h * 0.8)} 0 0 1 {fmt(x + w)} {fmt(y)}Z")


@icon("aerobot-balloon", CAT, "Round research balloon with a small gondola drifting above clouds",
      tags=["aerobot", "venus balloon", "atmosphere probe", "balloon", "floating", "clouds"])
def _(S):
    return [
        shell(circle(12, 7.5, 5)),
        detail(ellipse(12, 7.5, 1.75, 5)),
        line(seg(12, 12.5, 12, 14.5)),
        shell(rect(10, 14.5, 4, 2.5, min(S.R, 0.8))),
        shell(_cloud(2.5, 21, 6.5)),
        shell(_cloud(15.5, 21, 6)),
    ]


@icon("tracked-rover", CAT, "Small rover on tank treads with a camera mast",
      tags=["tracked rover", "crawler", "treads", "robot", "exploration", "rover"])
def _(S):
    return [
        shell(rect(2.5, 15, 19, 6, 3 if S.name == "rounded" else 2)),
        dot(6, 18, 1.1), dot(12, 18, 1.1), dot(18, 18, 1.1),
        shell(rect(5, 8, 11, 4.5, min(S.R, 1.5))),
        line(seg(13.5, 8, 13.5, 5.5)),
        shell(rect(12, 2.5, 6.5, 3, min(S.R, 1))),
    ]


@icon("hopping-lander", CAT, "Small lander mid hop above the ground with a dashed arc and thruster puff",
      tags=["hopper", "hop", "lander", "comet", "asteroid", "jump"])
def _(S):
    out = [line(arc(10.5, 19.5, 7.5, a0, a0 + 12)) for a0 in (185, 208, 231)]
    out += [
        shell(union("M15.5 4.5A2 2 0 0 1 19.5 4.5Z", rect(13.5, 4.5, 8, 3.5, min(S.R, 1)))),
        line(seg(15, 8, 13.5, 11)), line(seg(20, 8, 21.5, 11)),
        shell(_cloud(14, 17.5, 7.5)),
        line(seg(2, 21.5, 22, 21.5)),
    ]
    return out

# ============================================================================ spacecraft hardware

@icon("space-station-module", CAT, "Long cylindrical station module with a docking ring and windows",
      tags=["station module", "space station", "habitat module", "docking port", "iss", "spacecraft"])
def _(S):
    body = L(S, "M5.5 7H16.5V17H5.5C3.8 17 2.5 14.8 2.5 12C2.5 9.2 3.8 7 5.5 7Z",
             "M5.5 7H15A1.5 1.5 0 0 1 16.5 8.5V15.5A1.5 1.5 0 0 1 15 17H5.5C3.8 17 2.5 14.8 2.5 12C2.5 9.2 3.8 7 5.5 7Z")
    return [
        shell(union(body, rect(16, 10, 3, 4, 0), rect(18.5, 8, 3, 8, min(S.R, 1)))),
        dot(7, 12, 1.2), dot(12, 12, 1.2),
    ]


@icon("space-station-cupola", CAT, "Observation cupola seen from above: a round top window ringed by six panes",
      tags=["cupola", "observation deck", "space station", "window", "view", "earth watching"])
def _(S):
    hexa = regular(12, 12, 9.5, 6, -90)
    out = [shell(poly(hexa, closed=True, r=S.r)), detail(circle(12, 12, 3.5))]
    for k in range(6):
        a = -60 + k * 60
        out.append(detail(seg(*polar(12, 12, 3.5, a), *polar(12, 12, 8.3, a))))
    return out


@icon("solar-array-wing", CAT, "Long folding solar wing of grid cells on a mast from a truss arm",
      tags=["solar array", "solar wing", "solar panel", "power", "spacecraft", "space station"])
def _(S):
    out = [shell(rect(2.5, 10, 3.5, 4, min(S.R, 1))), line(seg(6, 12, 21.5, 12))]
    for y in (3, 15):
        out.append(shell(rect(8, y, 13.5, 6, min(S.R, 1))))
        for x in (12.5, 17):
            out.append(detail(seg(x, y, x, y + 6)))
    return out


@icon("ion-engine", CAT, "Round ion thruster grid firing a beam of straight lines",
      tags=["ion thruster", "ion drive", "electric propulsion", "engine", "thrust", "spacecraft"])
def _(S):
    out = [shell(circle(8.5, 12, 6.5))]
    for x, y in ((8.5, 12), (8.5, 8.5), (8.5, 15.5), (5.5, 10.25), (11.5, 10.25), (5.5, 13.75), (11.5, 13.75)):
        out.append(dot(x, y, 0.95))
    out += [line(seg(17, 8, 21.5, 8)), line(seg(17, 12, 22, 12)), line(seg(17, 16, 21.5, 16))]
    return out


@icon("launch-escape-tower", CAT, "Crew capsule topped by a lattice tower with a small escape rocket",
      tags=["launch escape system", "abort tower", "escape rocket", "capsule", "crew safety", "abort"])
def _(S):
    return [
        shell(poly([(10.5, 15), (13.5, 15), (18, 21.5), (6, 21.5)], closed=True, r=S.r * 0.5)),
        line(seg(10.5, 15, 11, 9.5)), line(seg(13.5, 15, 13, 9.5)), line(poly([(10.8, 12.5), (13.2, 11), (13.2, 11)], r=0)),
        shell(L(S, "M10.5 9.5V5L12 2.5L13.5 5V9.5Z", "M10.5 9.5V5Q10.5 4.4 10.9 3.8L11.4 3.1Q12 2.3 12.6 3.1L13.1 3.8Q13.5 4.4 13.5 5V9.5Z")),
        line(seg(10.5, 8.5, 8.5, 10.5)), line(seg(13.5, 8.5, 15.5, 10.5)),
    ]


@icon("solid-rocket-booster", CAT, "Tall slim booster with a pointed nose, segment joints and a flared nozzle",
      tags=["booster", "solid rocket", "srb", "launch vehicle", "rocket", "propulsion"])
def _(S):
    body = L(S, "M9.5 7L12 2L14.5 7V18H9.5Z", "M9.5 7Q9.5 6.2 9.9 5.6L11.2 3.2Q12 1.8 12.8 3.2L14.1 5.6Q14.5 6.2 14.5 7V18H9.5Z")
    return [
        shell(union(body, poly([(9.5, 18), (14.5, 18), (16, 22), (8, 22)], closed=True, r=S.r * 0.3))),
        detail(seg(9.5, 7.5, 14.5, 7.5)),
        detail(seg(9.5, 12.5, 14.5, 12.5)),
    ]


@icon("rocket-engine-cluster", CAT, "Base of a rocket seen from below with a ring of engine nozzles",
      tags=["engines", "rocket engines", "first stage", "nozzles", "booster", "thrust"])
def _(S):
    out = [shell(circle(12, 12, 9.5))]
    out.append(detail(circle(12, 12, 1.75)))
    for k in range(7):
        x, y = polar(12, 12, 6, -90 + k * 360 / 7)
        out.append(detail(circle(x, y, 1.6) if S.name == "rounded" else poly(regular(x, y, 1.75, 6, 0), closed=True)))
    return out


@icon("rocket-nose-cone", CAT, "Pointed ogive nose cone with a seam ring at its base",
      tags=["nose cone", "fairing", "ogive", "rocket tip", "aerodynamics", "rocket"])
def _(S):
    tip = L(S, "M6.5 17C6.5 10 8.5 5 12 2C15.5 5 17.5 10 17.5 17Z",
            "M6.5 17C6.5 10 8.5 5.2 11.2 2.6Q12 1.9 12.8 2.6C15.5 5.2 17.5 10 17.5 17Z")
    return [
        shell(union(tip, rect(6, 17, 12, 4.5, min(S.R, 1)))),
        detail(seg(6, 17, 18, 17)),
    ]


@icon("orbital-refueling", CAT, "Two spacecraft side by side linked by a fuel transfer hose",
      tags=["refueling", "propellant transfer", "tanker", "docking", "fuel", "in-space servicing"])
def _(S):
    return [
        shell(rect(2.5, 10, 6, 6, min(S.R, 1.5))), line(seg(5.5, 10, 5.5, 7)), line(seg(3.5, 7, 7.5, 7)),
        shell(rect(15.5, 10, 6, 6, min(S.R, 1.5))), line(seg(18.5, 10, 18.5, 7)), line(seg(16.5, 7, 20.5, 7)),
        line("M8.5 14C10.5 19 13.5 19 15.5 14"),
        shell(L(S, "M12 3.5L14 7A2 2 0 1 1 10 7Z", "M12 3.5Q14 6 14 7A2 2 0 1 1 10 7Q10 6 12 3.5Z")),
    ]


@icon("space-tug", CAT, "Boxy tug spacecraft with thrusters pushing a satellite ahead of it",
      tags=["space tug", "orbital transfer", "tug", "satellite", "push", "spacecraft"])
def _(S):
    return [
        shell(rect(6, 8.5, 6, 7, min(S.R, 1.5))),
        shell(poly([(6, 10), (4, 9), (4, 15), (6, 14)], closed=True, r=S.r * 0.3)),
        line(seg(2.5, 10.5, 2.5, 13.5)),
        shell(rect(14, 9.5, 4, 5, min(S.R, 1))),
        line(seg(12, 12, 14, 12)),
        line(seg(16, 9.5, 16, 7)), solid(rect(14, 2.5, 4, 4.5, 0)),
        line(seg(16, 14.5, 16, 17)), solid(rect(14, 17, 4, 4.5, 0)),
    ]


@icon("satellite-servicing", CAT, "Servicing spacecraft with a robotic arm grasping a satellite's solar panel",
      tags=["satellite servicing", "robotic arm", "repair", "in-orbit servicing", "maintenance", "capture"])
def _(S):
    return [
        shell(rect(2.5, 14.5, 6.5, 6.5, min(S.R, 1.5))),
        line(poly([(5.75, 14.5), (5.75, 8), (10.5, 5.5)], r=S.r)),
        line(poly([(10, 3.5), (11.5, 5), (10, 7.5)], r=S.r * 0.3)),
        solid(rect(13, 2.5, 3.5, 7, 0)),
        line(seg(16.5, 6, 17.5, 6)),
        shell(rect(17.5, 3.5, 4, 5, min(S.R, 1))),
    ]


def _mini_sat(cx, cy, S, w=3.5, h=3.5, pw=3.5):
    """Small satellite: box body with solid panels either side."""
    return [shell(rect(cx - w / 2, cy - h / 2, w, h, min(S.R, 0.8))),
            solid(rect(cx - w / 2 - 1 - pw, cy - 1.5, pw, 3, 0)), solid(rect(cx + w / 2 + 1, cy - 1.5, pw, 3, 0))]


@icon("deployable-antenna", CAT, "Umbrella shaped mesh antenna dish opening on a boom from a satellite",
      tags=["deployable antenna", "mesh antenna", "reflector", "satellite", "communication", "dish"])
def _(S):
    dish = L(S, "M3 10A9 7 0 0 1 21 10Z", "M3.8 10A0.8 0.8 0 0 1 3 9.2A9 6.2 0 0 1 21 9.2A0.8 0.8 0 0 1 20.2 10Z")
    return [
        shell(dish),
        detail(seg(12, 10, 8, 4)), detail(seg(12, 10, 16, 4)), detail(seg(12, 10, 12, 3)),
        line(seg(12, 10, 12, 16)),
        *_mini_sat(12, 18.5, S, 4, 4, 3.5),
    ]


@icon("sunshield", CAT, "Kite shaped stack of thin sunshield layers under a honeycomb mirror",
      tags=["sunshield", "space telescope", "heat shield", "layers", "mirror", "infrared"])
def _(S):
    kite = [(3, 16), (12, 12.5), (21, 16), (12, 19.5)]
    out = [shell(poly(kite, closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
           line(poly([(4, 19), (12, 22), (20, 19)], r=S.r * 0.6))]
    for cx, cy in ((12, 5.2), (9.2, 8.8), (14.8, 8.8)):
        out.append(shell(poly(regular(cx, cy, 2.1, 6, 0), closed=True, r=S.r * 0.3)))
    return out


@icon("satellite-coverage", CAT, "Satellite above Earth casting a cone shaped footprint onto the globe",
      tags=["coverage", "footprint", "satellite", "beam", "earth observation", "signal area"])
def _(S):
    return [
        *_mini_sat(12, 4.5, S, 3.5, 3.5, 3),
        line(seg(10.5, 7.5, 6, 16.5)), line(seg(13.5, 7.5, 18, 16.5)),
        shell("M2.5 21.5Q12 13 21.5 21.5Z", stroke_miterlimit="2"),
        detail("M6.5 18.2Q12 20.5 17.5 18.2"),
    ]


@icon("satellite-deployer", CAT, "Open launcher box pushing out a small cube satellite",
      tags=["cubesat deployer", "launcher", "small satellite", "deploy", "spring", "release"])
def _(S):
    return [
        line(poly([(12, 4), (2.5, 4), (2.5, 20), (12, 20)], r=S.r)),
        line(seg(6, 8, 6, 16)), line(seg(6, 12, 9, 12)),
        shell(rect(11, 8.5, 7, 7, min(S.R, 1.5))),
        detail(seg(14.5, 8.5, 14.5, 15.5)),
        line(seg(19.5, 10, 21.5, 10)), line(seg(19.5, 14, 21.5, 14)),
    ]


def _bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def _dashes(ctrl, n, on=0.55):
    """Dashed version of a cubic: n dashes, each covering `on` of its slot (3 point polylines)."""
    out = []
    for i in range(n):
        t0 = i / n
        t1 = t0 + on / n
        out.append(poly([_bez(*ctrl, t0), _bez(*ctrl, (t0 + t1) / 2), _bez(*ctrl, t1)]))
    return out


@icon("sounding-rocket", CAT, "Slim research rocket with a dashed flight path rising and arcing back down",
      tags=["sounding rocket", "research rocket", "suborbital", "trajectory", "flight path", "launch"])
def _(S):
    rk = L(S, "M4 12L5.5 9L7 12V19H4Z", "M4 12Q4 11.4 4.3 10.9L5 9.6Q5.5 8.8 6 9.6L6.7 10.9Q7 11.4 7 12V19H4Z")
    ctrl = [(6, 7), (9, 0.5), (16, 0.5), (20, 15.5)]
    out = [shell(rk), line(seg(2.5, 21.5, 8.5, 21.5))]
    out += [line(d) for d in _dashes(ctrl, 5)]
    out.append(arrowhead((20.3, 17), 75, S, 2.4))
    return out


@icon("reaction-wheel", CAT, "Flat flywheel in a round housing with a curved spin arrow",
      tags=["reaction wheel", "flywheel", "momentum wheel", "attitude control", "gyroscope", "spin"])
def _(S):
    body = union(ellipse(12, 13, 8, 3.25), rect(4, 13, 16, 4.5, 0), ellipse(12, 17.5, 8, 3.25))
    out = [shell(body), detail("M4 13A8 3.25 0 0 0 20 13"), dot(12, 13, 1.1)]
    pts = [polar(12, 9.5, 1, 0)]
    del pts
    out.append(line("M4 8.5C6 4.5 18 4.5 20 8.5"))
    out.append(arrowhead((20, 8.5), 60, S, 2.4))
    return out


@icon("crop-circle", CAT, "Field with a chain of rings and circles pressed into the crop",
      tags=["crop circle", "field pattern", "ufo", "mystery", "alien", "farm"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, L(S, 1, 3))),
        detail(circle(8.5, 15.5, 3.25)),
        dot(8.5, 15.5, 1.1),
        detail(circle(15, 9, 1.75)),
        detail(seg(10.9, 13.1, 13.6, 10.4)),
        detail(seg(16.4, 7.6, 18, 6)),
        detail(seg(4.5, 5.5, 11, 5.5)), detail(seg(4.5, 8.5, 9, 8.5)),
    ]


@icon("alien-signal", CAT, "Radio dish receiving a wavy signal from a distant star",
      tags=["seti", "alien signal", "radio telescope", "extraterrestrial", "contact", "message"])
def _(S):
    dish = rot("M5 10A7 7 0 0 0 19 10Z", 45, 12, 10)
    return [
        shell(rot("M5 11A7 5 0 0 0 19 11Z", 40, 8.5, 14)),
        line(seg(8.5, 16.5, 8.5, 21.5)), line(seg(5, 21.5, 12, 21.5)),
        line("M11 10.5Q11.8 8.5 13.5 9.2T16 7.8"),
        sparkle(19, 5, 3.25, S),
    ] if False else [
        shell(rot("M3 11A7 5 0 0 0 17 11Z", 40, 10, 11)),
        line(seg(8.5, 17, 7.5, 21.5)), line(seg(4, 21.5, 11, 21.5)),
        line("M12.8 11.2Q13.2 9 15 9.4T17.2 7.2"),
        sparkle(19.5, 4.5, 3, S),
    ]


@icon("interstellar-plaque", CAT, "Rectangular plaque engraved with a starburst diagram and a row of planet dots",
      tags=["pioneer plaque", "space message", "engraving", "interstellar", "probe", "greeting"])
def _(S):
    out = [shell(rect(2.5, 4, 19, 16, S.R))]
    for a, ln in ((-150, 4), (-100, 3.2), (-30, 4.5), (20, 3.5), (160, 3.8)):
        out.append(detail(seg(*polar(8, 10, 1.2, a), *polar(8, 10, 1.2 + ln, a))))
    for x in (6, 9.5, 13, 16.5):
        out.append(dot(x, 16.5, 0.9 if x != 9.5 else 1.2))
    out.append(detail(seg(15, 7, 15, 12)))
    return out


@icon("spaceport", CAT, "Control tower beside a rocket standing on its launch pad",
      tags=["spaceport", "launch site", "cosmodrome", "space center", "launch complex", "control tower"])
def _(S):
    rocket = L(S, "M15.5 8L17.5 3L19.5 8V17H15.5Z", "M15.5 8Q15.5 7 15.9 6.2L16.9 3.9Q17.5 2.7 18.1 3.9L19.1 6.2Q19.5 7 19.5 8V17H15.5Z")
    return [
        shell(poly([(2.5, 6), (10.5, 6), (9.5, 10), (3.5, 10)], closed=True, r=S.r * 0.4)),
        line(seg(5, 10, 5, 19.5)), line(seg(8, 10, 8, 19.5)),
        shell(rocket),
        line(seg(15.5, 17, 14, 19.5)), line(seg(19.5, 17, 21, 19.5)),
        line(seg(2, 21.5, 22, 21.5)) if False else line(seg(2, 19.5, 22, 19.5)),
    ]


@icon("engine-test-stand", CAT, "Test stand holding a rocket engine firing down into a trench",
      tags=["test stand", "engine test", "static fire", "rocket engine", "propulsion test", "firing"])
def _(S):
    flame = L(S, "M12 20C9.5 18.5 9.5 16 10.5 13.5L12 15L13.5 13.5C14.5 16 14.5 18.5 12 20Z",
              "M12 20C9.5 18.5 9.5 16 10.5 13.5Q12 15.5 13.5 13.5C14.5 16 14.5 18.5 12 20Z")
    return [
        line(poly([(4, 15), (4, 3), (20, 3), (20, 15)], r=S.r)),
        line(seg(12, 3, 12, 5.5)),
        shell(poly([(10.5, 5.5), (13.5, 5.5), (15, 11), (9, 11)], closed=True, r=S.r * 0.4)),
        shell(flame),
        line(poly([(2, 15), (7.5, 15), (7.5, 21.5), (16.5, 21.5), (16.5, 15), (22, 15)], r=S.r * 0.6)),
    ]


@icon("vehicle-assembly-building", CAT, "Huge boxy assembly hall with a tall vertical door slot",
      tags=["assembly building", "rocket hangar", "hangar", "integration facility", "vab", "high bay"])
def _(S):
    return [
        shell(union(rect(4, 2.5, 13, 19, min(S.R, 1.5)), rect(15, 13, 5.5, 8.5, min(S.R, 1)))),
        detail(L(S, "M8.5 21.5V6H12.5V21.5", "M8.5 21.5V7.5A1.5 1.5 0 0 1 10 6H11A1.5 1.5 0 0 1 12.5 7.5V21.5")),
        detail(seg(17, 13, 17, 21.5)),
    ]


@icon("landing-barge", CAT, "Flat ship deck with a target where a booster lands on its legs",
      tags=["drone ship", "landing ship", "booster landing", "reusable rocket", "barge", "recovery"])
def _(S):
    rk = L(S, "M10.5 4.5L12 2.5L13.5 4.5V13H10.5Z", "M10.5 4.5Q10.5 4 10.9 3.5L11.5 2.9Q12 2.4 12.5 2.9L13.1 3.5Q13.5 4 13.5 4.5V13H10.5Z")
    return [
        shell(rk),
        line(seg(10.5, 11.5, 8, 15)), line(seg(13.5, 11.5, 16, 15)),
        shell(poly([(2, 17), (22, 17), (20, 21.5), (4, 21.5)], closed=True, r=S.r * 0.6)),
        detail(seg(8.5, 19.25, 15.5, 19.25)),
    ]


# ============================================================================ launch sites

@icon("launch-control-bunker", CAT, "Low mound bunker with a slit window facing a rocket on the pad",
      tags=["blockhouse", "launch control", "bunker", "control center", "launch site", "shelter"])
def _(S):
    rk = L(S, "M17.5 7.5L19.25 4L21 7.5V20H17.5Z", "M17.5 7.5Q17.5 6.8 17.8 6.2L18.6 4.8Q19.25 3.6 19.9 4.8L20.7 6.2Q21 6.8 21 7.5V20H17.5Z")
    return [
        shell(union("M2.5 20A6.25 6 0 0 1 15 20Z", rk, ground(20, 2, 22))),
        detail(seg(5.5, 16.5, 12, 16.5)),
    ]


@icon("water-deluge", CAT, "Rocket on its pad with water spraying from nozzles around the base",
      tags=["water deluge", "sound suppression", "launch pad", "water spray", "rocket launch", "pad"])
def _(S):
    rk = L(S, "M10.5 7L12 3L13.5 7V16H10.5Z", "M10.5 7Q10.5 6.2 10.8 5.6L11.4 4.2Q12 3 12.6 4.2L13.2 5.6Q13.5 6.2 13.5 7V16H10.5Z")
    return [
        shell(union(rk, rect(3, 17.5, 18, 3.5, min(S.R, 1)))),
        detail(seg(3, 17.5, 21, 17.5)),
        line("M3.5 14.5Q4.5 10 8.5 11.5"),
        line("M20.5 14.5Q19.5 10 15.5 11.5"),
        dot(4.5, 7.5, 1), dot(19.5, 7.5, 1), dot(7, 5.5, 1), dot(17, 5.5, 1),
    ]


@icon("rocket-transport-barge", CAT, "Barge carrying a long rocket stage lying on cradles",
      tags=["rocket barge", "stage transport", "shipping", "barge", "rocket stage", "logistics"])
def _(S):
    body = L(S, "M2.5 7H16.5L21.5 9.5L16.5 12H2.5Z", "M4 7H16.5L20.5 9L20.5 10L16.5 12H4A1.5 1.5 0 0 1 2.5 10.5V8.5A1.5 1.5 0 0 1 4 7Z")
    return [
        shell(body),
        detail(seg(12, 7, 12, 12)),
        line(seg(6, 12, 6, 15)), line(seg(15, 12, 15, 15)),
        shell(poly([(2, 15), (22, 15), (20, 20.5), (4, 20.5)], closed=True, r=S.r * 0.6)),
    ]


def _pencil(x, w, top, bottom, S):
    tip = top + w * 0.9
    if S.name == "line":
        return f"M{fmt(x)} {fmt(tip)}L{fmt(x + w / 2)} {fmt(top)}L{fmt(x + w)} {fmt(tip)}V{fmt(bottom)}H{fmt(x)}Z"
    return (f"M{fmt(x)} {fmt(tip)}Q{fmt(x + w / 2)} {fmt(top - 0.6)} {fmt(x + w)} {fmt(tip)}V{fmt(bottom)}H{fmt(x)}Z")


@icon("rocket-garden", CAT, "Several rockets of different heights standing side by side",
      tags=["rocket garden", "rocket display", "museum", "space center", "exhibit", "rockets"])
def _(S):
    return [
        shell(union(_pencil(3, 3.5, 9, 20, S), _pencil(10.25, 3.5, 2.5, 20, S), _pencil(17.5, 3.5, 6.5, 20, S), ground(20, 2, 22))),
        detail(seg(10.25, 8, 13.75, 8)),
        line(seg(10.25, 16.5, 8.5, 18.5)) if False else detail(seg(3, 13, 6.5, 13)),
        detail(seg(17.5, 11, 21, 11)),
    ]


# ============================================================================ sky watching

def _star5_shell(cx, cy, r, S):
    return shell(poly(star5(cx, cy, r, r * 0.48), closed=True, r=S.r * 0.3), stroke_miterlimit="2")


@icon("glow-in-the-dark-stars", CAT, "Star stickers stuck to a ceiling giving off a soft glow",
      tags=["glow stars", "ceiling stars", "stickers", "bedroom", "night", "kids room"])
def _(S):
    return [
        line(seg(2, 3, 22, 3)),
        _star5_shell(9, 12.5, 5.5, S),
        _star5_shell(18, 16.5, 3.25, S),
        line(seg(15.5, 8, 17, 6.5)), line(seg(17, 10.5, 19, 10)), line(seg(3, 20.5, 4.5, 19)),
    ]


@icon("planet-mobile", CAT, "Hanging mobile with planets dangling from two balanced bars",
      tags=["mobile", "nursery", "solar system toy", "planets", "hanging decoration", "crib"])
def _(S):
    return [
        line(seg(10, 2, 10, 5)), line(seg(3, 5, 19, 5)),
        line(seg(4.5, 5, 4.5, 9)), shell(circle(4.5, 11.75, 2.75)),
        line(seg(17.5, 5, 17.5, 11)), line(seg(12.5, 11, 21.5, 11)),
        line(seg(14, 11, 14, 14)), shell(circle(14, 17, 3)),
        line(seg(20.5, 11, 20.5, 15.5)), shell(circle(20.5, 17.5, 2)),
    ]


@icon("seasons-diagram", CAT, "Sun in the middle with Earth shown at four points of its orbit",
      tags=["seasons", "earth orbit", "solstice", "equinox", "axial tilt", "astronomy lesson"])
def _(S):
    sun = (poly([polar(12, 12, 3 if i % 2 == 0 else 2.1, -90 + i * 22.5) for i in range(16)], closed=True)
           if S.name == "line" else circle(12, 12, 2.6))
    out = [shell(sun)]
    pos = ((12, 3.5), (20.5, 12), (12, 20.5), (3.5, 12))
    for k, (x, y) in enumerate(pos):
        a0 = -90 + k * 90 + 16
        out.append(line(arc(12, 12, 8.5, a0, a0 + 58)))
        out.append(dot(x, y, 2))
    return out


@icon("sky-map-app", CAT, "Phone screen showing constellation lines and a compass pointer",
      tags=["star map", "sky app", "stargazing app", "planetarium app", "constellation finder", "phone"])
def _(S):
    pts = [(8.5, 12), (10.5, 7.5), (14, 9), (15.5, 5.5)]
    out = [shell(rect(5, 2, 14, 20, S.R)), detail(poly(pts, r=S.r * 0.3))]
    out += [dot(x, y, 1.1) for x, y in pts]
    out.append(mark(poly([(12, 15), (14, 19), (12, 18), (10, 19)], closed=True, r=S.r * 0.2)))
    return out


def _telescope(cx, S, flip=1):
    tube = rot(rect(cx - 4, 7.5, 8, 3, min(S.R, 1)), -30 * flip, cx, 9)
    return [shell(tube), line(seg(cx, 10.5, cx - 3, 20)), line(seg(cx, 10.5, cx + 3, 20)), line(seg(cx, 10.5, cx, 20))]


@icon("star-party", CAT, "Two telescopes on tripods set up together under the stars",
      tags=["star party", "stargazing", "astronomy club", "telescopes", "observing night", "amateur astronomy"])
def _(S):
    return [*_telescope(6, S), *_telescope(17.5, S, 1), sparkle(12, 4, 2.75, S), dot(21, 3.5, 1)]


@icon("dark-sky-reserve", CAT, "Row of pine trees under a dense field of stars and a crescent moon",
      tags=["dark sky", "stargazing", "night sky", "light pollution", "nature reserve", "national park"])
def _(S):
    parts = []
    for x, t in ((5, 10.5), (12, 8.5), (19, 11)):
        parts += [poly([(x - 2.5, 16), (x, t), (x + 2.5, 16)], closed=True), rect(x - 0.75, 15.5, 1.5, 4.5, 0)]
    trees = union(*parts, rect(2, 19.75, 20, 0.5, 0))
    moon = minus(circle(18.5, 5, 3.25), circle(20.1, 3.8, 2.8))
    return [
        shell(trees, stroke_miterlimit="2"),
        shell(moon, stroke_miterlimit="2"),
        dot(4, 4, 1), dot(9, 5.5, 1), dot(13, 2.5, 1), dot(4.5, 8, 0.9),
    ]


def star_dot(x, y, r, S):
    """Star marker: a small diamond in Line, a round dot in Rounded (solid in both)."""
    if S.name == "line":
        k = r * 1.3
        return mark(poly([(x, y - k), (x + k, y), (x, y + k), (x - k, y)], closed=True))
    return dot(x, y, r)


def _chain(pts, S, big=(), r=1.4, rb=2.0):
    out = [line(poly(pts, r=S.r * 0.4))]
    for i, (x, y) in enumerate(pts):
        out.append(star_dot(x, y, rb if i in big else r, S))
    return out


@icon("summer-triangle", CAT, "Three bright stars joined in a large triangle with faint stars nearby",
      tags=["summer triangle", "asterism", "vega", "deneb", "altair", "night sky"])
def _(S):
    a, b, c = (12.5, 4), (19.5, 11), (6, 19.5)
    return [
        line(poly([a, b, c], closed=True, r=S.r * 0.5)),
        sparkle(*a, 3.2, S, 0.35), sparkle(*b, 3.2, S, 0.35), sparkle(*c, 3.2, S, 0.35),
        dot(4.5, 7, 1), dot(18.5, 19, 1), dot(21, 4.5, 1),
    ]


@icon("cygnus-constellation", CAT, "Stars forming a long cross shaped like a swan with spread wings",
      tags=["cygnus", "northern cross", "swan", "constellation", "deneb", "star pattern"])
def _(S):
    out = _chain([(18, 5), (13, 10), (9.5, 14.5), (5, 19.5)], S, big=(0,))
    out.append(line(poly([(4.5, 7.5), (8.5, 7.5), (12.3, 9.6)], r=S.r * 0.4)))
    out.append(line(poly([(13.6, 10.6), (17, 14), (17.5, 19)], r=S.r * 0.4)))
    out += [star_dot(x, y, 1.4, S) for x, y in ((4.5, 7.5), (8.5, 7.5), (17, 14), (17.5, 19))]
    return out


@icon("scorpius-constellation", CAT, "Curved hook of stars ending in a scorpion's stinger",
      tags=["scorpius", "scorpion", "constellation", "antares", "zodiac", "star pattern"])
def _(S):
    body = [(17.5, 7), (16, 11), (14.5, 14.5), (12, 18), (8.5, 20), (5, 18.5), (4, 15), (6.5, 13)]
    out = _chain(body, S, big=(1,))
    out += [line(poly([(14.5, 3), (17.5, 7), (21, 4)], r=S.r * 0.4)), star_dot(14.5, 3, 1.4, S), star_dot(21, 4, 1.4, S)]
    return out


@icon("leo-constellation", CAT, "Backwards question mark of stars joined to a triangle, forming a lion",
      tags=["leo", "lion", "constellation", "sickle", "regulus", "zodiac"])
def _(S):
    sickle = [(10.5, 3.5), (6.5, 3), (4, 6), (5.5, 9.5), (9, 11), (8.5, 16)]
    tri = [(9, 11), (15.5, 9.5), (20.5, 15.5), (14.5, 16), (8.5, 16)]
    out = [line(poly(sickle, r=S.r * 0.4)), line(poly(tri, r=S.r * 0.4))]
    for i, (x, y) in enumerate(sickle + tri[1:4]):
        out.append(star_dot(x, y, 2 if (x, y) == (8.5, 16) else 1.4, S))
    return out


@icon("moon-illusion", CAT, "Huge moon rising on the horizon next to a small moon high in the sky",
      tags=["moon illusion", "optical illusion", "moonrise", "horizon", "perception", "full moon"])
def _(S):
    big = union(minus(circle(9, 14.5, 6.5), rect(0, 19, 24, 6, 0)), ground(19.25, 2, 22))
    return [
        shell(big),
        dot(6, 15.5, 1.1), dot(11.5, 11.5, 0.9), dot(9.5, 16, 0.8),
        shell(circle(18.5, 5, 2.25)),
    ]
