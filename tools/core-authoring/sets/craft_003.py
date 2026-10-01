"""TypeIcon Core: craft (batch 003): harbour and deck gear, launch vehicles, spacecraft, old and unusual boats,
and a few aircraft.

Visual language (shared with sets/craft_001.py and sets/astronomy_002.py):
  * Side views face right (bow or nose on the right). Water is a single wave line near y 21.
  * Rockets are slim bodies with a pointed nose (`nose_body`); flames are small drops (`flame`).
  * Line keeps sharp joins and small radii; Rounded softens corners and tips (`L(S, line, rounded)`).
"""
from __future__ import annotations

import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "craft"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12.0, cy=12.0):
    """Rotate a d-string clockwise on screen about (cx, cy)."""
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def move(d, dx, dy):
    return path_to_d(transform_path(P(d), (1, 0, 0, 1, dx, dy)))


def rpts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rseg(x1, y1, x2, y2, deg, cx=12.0, cy=12.0):
    (a, b), (c, d) = rpts([(x1, y1), (x2, y2)], deg, cx, cy)
    return seg(a, b, c, d)


def mark(d):
    """Small solid mark: solid in Line and Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def nose_body(S, x0, x1, top, shoulder, bottom):
    """Slim rocket body: pointed nose from `top` down to `shoulder`, straight sides down to `bottom`."""
    cx = (x0 + x1) / 2
    h = shoulder - top
    if S.name == "line":
        return (f"M{fmt(x0)} {fmt(bottom)}V{fmt(shoulder)}Q{fmt(x0)} {fmt(top + h * 0.35)} {fmt(cx)} {fmt(top)}"
                f"Q{fmt(x1)} {fmt(top + h * 0.35)} {fmt(x1)} {fmt(shoulder)}V{fmt(bottom)}Z")
    k = 0.6
    return (f"M{fmt(x0)} {fmt(bottom)}V{fmt(shoulder)}Q{fmt(x0)} {fmt(top + h * 0.3)} {fmt(cx - k)} {fmt(top + k * 0.8)}"
            f"Q{fmt(cx)} {fmt(top - 0.2)} {fmt(cx + k)} {fmt(top + k * 0.8)}"
            f"Q{fmt(x1)} {fmt(top + h * 0.3)} {fmt(x1)} {fmt(shoulder)}V{fmt(bottom)}Z")


def flame(S, cx, top, bottom, w):
    """Flame drop hanging from `top` to a tip at `bottom` (sharp tip in Line, soft in Rounded)."""
    h = bottom - top
    if S.name == "line":
        return (f"M{fmt(cx - w / 2)} {fmt(top)}H{fmt(cx + w / 2)}C{fmt(cx + w / 2)} {fmt(top + h * 0.45)} "
                f"{fmt(cx + w * 0.15)} {fmt(top + h * 0.7)} {fmt(cx)} {fmt(bottom)}"
                f"C{fmt(cx - w * 0.15)} {fmt(top + h * 0.7)} {fmt(cx - w / 2)} {fmt(top + h * 0.45)} {fmt(cx - w / 2)} {fmt(top)}Z")
    return (f"M{fmt(cx - w / 2)} {fmt(top)}H{fmt(cx + w / 2)}C{fmt(cx + w / 2)} {fmt(top + h * 0.5)} "
            f"{fmt(cx + w * 0.3)} {fmt(bottom)} {fmt(cx)} {fmt(bottom)}"
            f"C{fmt(cx - w * 0.3)} {fmt(bottom)} {fmt(cx - w / 2)} {fmt(top + h * 0.5)} {fmt(cx - w / 2)} {fmt(top)}Z")


def wave(x0, x1, y, n, amp=1.0):
    """Gentle wave line from x0 to x1 made of n half waves."""
    w = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        xa = x0 + i * w
        d += f"Q{fmt(xa + w / 2)} {fmt(y - amp * (2 if i % 2 == 0 else -2))} {fmt(xa + w)} {fmt(y)}"
    return d


def lattice(x0, x1, y0, y1, n):
    """Zigzag bracing between two tower legs from y0 down to y1 (n diagonals): a list of line parts."""
    pts = [(x0 if i % 2 == 0 else x1, y0 + (y1 - y0) * i / n) for i in range(n + 1)]
    return [line(seg(*pts[i], *pts[i + 1])) for i in range(n)]


# ============================================================================ harbour and deck gear

@icon("gangplank", CAT, "Plank with a rope railing sloping from the quay up to the side of a ship",
      tags=["gangway", "boarding ramp", "embark", "boarding", "ship", "quay"])
def _(S):
    hull = L(S, "M15.5 3.5H21.5V15.5L19 18.5H15.5Z",
             "M17 3.5H20A1.5 1.5 0 0 1 21.5 5V15.3Q21.5 16 21 16.6L19.7 18Q19.3 18.5 18.6 18.5H17A1.5 1.5 0 0 1 15.5 17V5A1.5 1.5 0 0 1 17 3.5Z")
    return [
        shell(hull),
        dot(18.5, 8, 1.2),
        line(wave(14, 22.5, 21.5, 2, 0.7)),
        shell(rect(2, 17.5, 6, 4, L(S, 0, 1.5))),
        line(seg(6, 17.5, 15.5, 11)),
        line(seg(4.5, 12.5, 4.5, 17.5)), line(seg(10, 9.5, 10, 14.2)),
        line(seg(4.5, 12.5, 15.5, 5.5)),
    ]


@icon("boat-trailer", CAT, "Small motorboat resting on a two-wheeled road trailer with a hitch at the front",
      tags=["boat trailer", "trailer", "towing", "launch", "motorboat", "haul"])
def _(S):
    return [
        shell(poly([(5.5, 5.5), (17, 5.5), (21.5, 9.5), (17.5, 13), (6, 13)], closed=True, r=S.r * 0.6)),
        solid(rect(1.8, 5, 3, 5.5, 0 if S.name == "line" else 0.8)),
        line(seg(3.3, 10.5, 3.3, 13.5)),
        line(seg(9, 13, 9, 16.5)), line(seg(15, 13, 15, 16.5)),
        line(seg(3, 16.5, 21.5, 16.5)),
        shell(circle(11.5, 19.5, 2)),
    ]


@icon("bosun-whistle", CAT, "Bosun's call: a tapered pipe ending in a round ball, with a lanyard looped above it",
      tags=["boatswain pipe", "bosun call", "whistle", "navy", "piping aboard", "sailor"],
      aliases=["boatswain-pipe"])
def _(S):
    tube = L(S, "M2.5 14.5L13 10.5V15.5Z", "M3.5 14.6L13 10.5V15.5L3.5 15.4A0.4 0.4 0 0 1 3.5 14.6Z")
    return [
        shell(union(tube, circle(16.5, 13, 4.5))),
        dot(17, 12, 1.2),
        line(L(S, "M4.5 12.5C4.5 6 9 3.5 15 5", "M4.5 12.5C4.5 6 9 3.5 15 5")),
        dot(15.5, 5.3, 1.2),
    ]


@icon("maritime-signal-flags", CAT, "Line of square and pointed signal flags hanging from a rope",
      tags=["signal flags", "nautical flags", "code flags", "dressed ship", "bunting", "sailing"],
      aliases=["nautical-flags"])
def _(S):
    k = S.r * 0.5
    return [
        line(seg(1.5, 3.5, 22.5, 3.5)),
        shell(rect(3, 4.5, 6, 8, L(S, 0, 1))),
        solid(poly([(11, 4.5), (16.5, 4.5), (13.75, 14)], closed=True)),
        shell(poly([(18, 4.5), (22, 4.5), (22, 12.5), (18, 12.5)], closed=True, r=k)),
        line(seg(12, 15, 12, 15)) if False else line(seg(1.5, 3.5, 1.5, 3.5)),
    ]


@icon("foghorn", CAT, "Flared horn on a post sending out curved sound waves",
      tags=["fog horn", "fog signal", "horn", "lighthouse", "warning", "sound"])
def _(S):
    horn = L(S, "M2.5 10H6.5C9.5 10 11 8 12.5 5V18C11 15 9.5 13 6.5 13H2.5Z",
             "M4 10H6.5C9.5 10 11 8 11.8 5.8Q12.5 4.5 12.5 6V17Q12.5 18.5 11.8 17.2C11 15 9.5 13 6.5 13H4A1.5 1.5 0 0 1 4 10Z")
    return [
        shell(horn),
        line(seg(5.5, 13, 5.5, 21)),
        line(seg(2.5, 21, 8.5, 21)),
        line(arc(12.5, 11.5, 4, -40, 40)),
        line(arc(12.5, 11.5, 8, -40, 40)),
    ]


@icon("engine-telegraph", CAT, "Ship's engine order telegraph: a round dial with speed marks and a lever on a pedestal",
      tags=["ship telegraph", "engine order", "bridge", "full ahead", "throttle", "helm"])
def _(S):
    cx, cy = 12, 9.5
    out = [
        shell(circle(cx, cy, 7)),
        shell(union(rect(10.5, 16.5, 3, 3.5, 0), rect(7, 19.5, 10, 2.5, min(S.R, 1.25)))),
        detail(seg(5, cy, 7.5, cy)), detail(seg(16.5, cy, 19, cy)),
    ]
    for a in (-150, -120, -60, -30, 150, 30):
        out.append(detail(seg(*polar(cx, cy, 4.3, a), *polar(cx, cy, 6, a))))
    out.append(line(seg(cx, cy, *polar(cx, cy, 8.5, -70))))
    out.append(dot(cx, cy, 1.5))
    return out


# ============================================================================ launch vehicles

@icon("heavy-lift-rocket", CAT, "Tall core rocket with two slim strap-on side boosters, all firing flames",
      tags=["heavy lift", "launch vehicle", "side boosters", "rocket", "launch", "space"])
def _(S):
    core = nose_body(S, 9.5, 14.5, 2, 7, 15.5)
    lb = nose_body(S, 5.5, 10, 8, 11, 15.5)
    rb = nose_body(S, 14, 18.5, 8, 11, 15.5)
    return [
        shell(union(core, lb, rb)),
        detail(seg(9.5, 11.5, 9.5, 15.5)), detail(seg(14.5, 11.5, 14.5, 15.5)),
        shell(flame(S, 7.5, 18, 21.5, 2.5), stroke_miterlimit="2"),
        shell(flame(S, 12, 18, 21.5, 2.5), stroke_miterlimit="2"),
        shell(flame(S, 16.5, 18, 21.5, 2.5), stroke_miterlimit="2"),
    ]


@icon("launch-pad", CAT, "Rocket standing on a flat pad beside a lattice service tower with an access arm",
      tags=["launchpad", "launch site", "service tower", "liftoff", "countdown", "spaceport"],
      aliases=["launchpad"])
def _(S):
    return [
        shell(nose_body(S, 13, 18, 2.5, 7.5, 17.5)),
        detail(seg(13, 14, 18, 14)),
        line(seg(4, 3, 4, 21)), line(seg(8, 3, 8, 21)),
        *lattice(4, 8, 5, 19, 4),
        line(seg(8, 9, 13, 9)),
        line(seg(2, 21, 22, 21)),
        line(seg(15.5, 17.5, 15.5, 21)),
    ]


@icon("crawler-transporter", CAT, "Flat tracked platform carrying an upright rocket and its launch tower",
      tags=["crawler", "rocket transporter", "tracked vehicle", "rollout", "launch", "spaceport"])
def _(S):
    return [
        shell(nose_body(S, 12.5, 16.5, 2, 6, 12.5)),
        line(seg(5.5, 3, 5.5, 12.5)), line(seg(9, 3, 9, 12.5)),
        *lattice(5.5, 9, 4.5, 11, 2),
        shell(rect(2.5, 12.5, 19, 3, min(S.R, 1))),
        line(seg(7, 15.5, 7, 18.5)), line(seg(17, 15.5, 17, 18.5)),
        shell(rect(2.5, 18.5, 8.5, 3.5, 1.75)), shell(rect(13, 18.5, 8.5, 3.5, 1.75)),
    ]


@icon("rocket-engine", CAT, "Rocket engine: a combustion chamber with a feed pipe on top of a flared nozzle, firing a flame",
      tags=["rocket motor", "nozzle", "thruster", "propulsion", "combustion", "engine"])
def _(S):
    nozzle = "M10.5 8.5H13.5L18.5 15A6.5 2.5 0 0 1 5.5 15Z"
    return [
        shell(union(rect(9, 2.5, 6, 6, min(S.R, 1.5)), nozzle)),
        detail(seg(9, 8.5, 15, 8.5)),
        detail("M6.5 14.5A6 2 0 0 1 17.5 14.5"),
        line(poly([(15, 5), (18.5, 5), (18.5, 9), (15.5, 10.5)], r=S.r)),
        line(poly([(9, 5), (5.5, 5), (5.5, 9), (8.5, 10.5)], r=S.r)),
        shell(flame(S, 12, 19.5, 22.5, 5), stroke_miterlimit="2"),
    ]


@icon("reusable-booster", CAT, "Rocket stage landing upright on a flame with its legs unfolded above a landing pad",
      tags=["booster landing", "propulsive landing", "reusable rocket", "first stage", "landing legs", "recovery"])
def _(S):
    body = L(S, "M10 2.5H14V14.5H10Z", "M11 2.5H13A1 1 0 0 1 14 3.5V14.5H10V3.5A1 1 0 0 1 11 2.5Z")
    return [
        shell(body),
        line(seg(7, 5, 10, 5)), line(seg(14, 5, 17, 5)),
        line(poly([(10, 10.5), (5.5, 16), (4, 16)], r=S.r * 0.5)),
        line(poly([(14, 10.5), (18.5, 16), (20, 16)], r=S.r * 0.5)),
        shell(flame(S, 12, 16.5, 19.5, 3), stroke_miterlimit="2"),
        line(seg(3, 21.5, 21, 21.5)),
    ]


@icon("stage-separation", CAT, "Rocket splitting in two: the spent lower stage drops away as the upper stage fires",
      tags=["staging", "stage sep", "multistage rocket", "upper stage", "jettison", "launch"])
def _(S):
    lower = rect(10, 14.5, 5, 7.5, min(S.R, 1.5))
    return [
        shell(nose_body(S, 10, 15, 2, 6.5, 10)),
        shell(flame(S, 12.5, 10, 13.5, 3), stroke_miterlimit="2"),
        shell(rot(lower, -25, 12.5, 18.25)),
        detail(rseg(10, 17, 15, 17, -25, 12.5, 18.25)),
    ]


# ============================================================================ capsules, satellites and stations

@icon("atmospheric-reentry", CAT, "Cone capsule plunging base first inside a teardrop of flame with a fiery trail",
      tags=["reentry", "re-entry", "heat shield", "capsule", "return", "plasma"], aliases=["reentry"])
def _(S):
    # designed diving straight down, then turned so it plunges toward the bottom-left
    fire = L(S, "M12 3C14 8 18.5 10 18.5 15A6.5 6.5 0 0 1 5.5 15C5.5 10 10 8 12 3Z",
             "M11.6 4.2Q12 3 12.4 4.2C14.3 8.6 18.5 10.3 18.5 15A6.5 6.5 0 0 1 5.5 15C5.5 10.3 9.7 8.6 11.6 4.2Z")
    cap = poly([(10.75, 11.5), (13.25, 11.5), (15, 16.5), (9, 16.5)], closed=True, r=S.r * 0.4)
    return [
        shell(rot(fire, 40)),
        detail(rot(cap, 40)),
        line(rseg(7.5, 2, 7.5, 6, 40)), line(rseg(16.5, 2, 16.5, 6, 40)),
    ]


@icon("capsule-splashdown", CAT, "Cone space capsule floating on waves under three round parachutes",
      tags=["splashdown", "parachutes", "capsule", "recovery", "ocean landing", "return"])
def _(S):
    def chute(cx, cy, r, deg):
        return rot(f"M{fmt(cx - r)} {fmt(cy)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx + r)} {fmt(cy)}Z", deg, cx, cy)
    cap = poly([(10.5, 14.5), (13.5, 14.5), (15, 18.5), (9, 18.5)], closed=True, r=S.r * 0.5)
    return [
        shell(chute(12, 6.5, 4, 0)),
        shell(chute(4.75, 9.5, 2.75, -30)), shell(chute(19.25, 9.5, 2.75, 30)),
        line(seg(12, 6.5, 12, 14.5)),
        line(seg(6.2, 11.9, 10.5, 14.5)), line(seg(17.8, 11.9, 13.5, 14.5)),
        shell(cap),
        line(wave(2.5, 21.5, 21.5, 4, 0.7)),
    ]


@icon("cubesat", CAT, "Small cube satellite with gridded solar cell faces and a thin antenna",
      tags=["cube satellite", "nanosatellite", "smallsat", "satellite", "solar cells", "space"],
      aliases=["nanosatellite"])
def _(S):
    outline = poly([(3, 10), (7, 6), (18.5, 6), (18.5, 17.5), (14.5, 21.5), (3, 21.5)], closed=True, r=S.r)
    return [
        shell(outline),
        detail(poly([(3, 10), (14.5, 10), (14.5, 21.5)])),
        detail(seg(14.5, 10, 18.5, 6)),
        detail(seg(8.75, 10, 8.75, 21.5)), detail(seg(3, 15.75, 14.5, 15.75)),
        line(seg(17, 6, 17, 3)),
        dot(17, 2.5, 1.35) if S.name == "rounded" else solid(rect(15.75, 1.5, 2.5, 2.5)),
    ]


@icon("spaceplane", CAT, "Side view of a winged orbiter with a blunt nose, a delta wing, a tail fin and engine nozzles",
      tags=["space shuttle", "orbiter", "shuttle", "reusable spacecraft", "space plane", "glider"])
def _(S):
    body = L(S, "M5 9H15.5C19 9 21.5 11 21.5 13.5V14.5H5Z",
             "M6.5 9H15.5C19 9 21.5 11 21.5 13.5A1 1 0 0 1 20.5 14.5H6.5A1.5 1.5 0 0 1 5 13V10.5A1.5 1.5 0 0 1 6.5 9Z")
    fin = poly([(5, 9), (5, 3), (7, 3), (11, 9)], closed=True, r=S.r * 0.5)
    wing = poly([(7, 14.5), (16.5, 14.5), (9, 18.5), (7, 18.5)], closed=True, r=S.r * 0.5)
    return [
        shell(union(body, fin, wing), stroke_miterlimit="2"),
        detail(seg(5, 9, 11, 9)),
        detail(seg(7, 14.5, 16.5, 14.5)),
        dot(17.5, 11.25, 1.1),
        shell(poly([(2.5, 9.5), (3.5, 10.5), (3.5, 13), (2.5, 14)], closed=True, r=S.r * 0.3)),
    ]


@icon("spacecraft-docking", CAT, "Two spacecraft modules closing in nose to nose with their docking ports lined up",
      tags=["docking", "rendezvous", "berthing", "spacecraft", "space station", "dock"])
def _(S):
    rr = min(S.R, 1.5)
    return [
        shell(rect(2, 9, 7, 8, rr)), shell(rect(9, 11, 1.5, 4, 0)),
        shell(rect(15, 9, 7, 8, rr)), shell(rect(13.5, 11, 1.5, 4, 0)),
        detail(seg(5.5, 9, 5.5, 17)), detail(seg(18.5, 9, 18.5, 17)),
        line(seg(3, 4.5, 9, 4.5)), line(poly([(7, 2.5), (9, 4.5), (7, 6.5)], r=S.r * 0.4)),
        line(seg(21, 4.5, 15, 4.5)), line(poly([(17, 2.5), (15, 4.5), (17, 6.5)], r=S.r * 0.4)),
        dot(12, 13, 1),
    ]


@icon("space-elevator", CAT, "Tether rising from the curve of the Earth to a station in orbit, with a climber pod on it",
      tags=["space elevator", "tether", "orbital tower", "climber", "megastructure", "orbit"])
def _(S):
    return [
        shell("M2 22A26 26 0 0 1 22 22Z" if S.name == "line" else "M2.6 21.2A26 26 0 0 1 21.4 21.2Q22 22 21 22H3Q2 22 2.6 21.2Z"),
        line(seg(12, 19, 12, 15.5)), line(seg(12, 11.5, 12, 7.5)),
        shell(rect(9.5, 11.5, 5, 4, min(S.R, 1))),
        shell(circle(12, 5, 2.5)),
        shell(rect(2.5, 3.5, 5.5, 3, 0 if S.name == "line" else 1)), shell(rect(16, 3.5, 5.5, 3, 0 if S.name == "line" else 1)),
    ]


@icon("space-robotic-arm", CAT, "Jointed robotic arm anchored to a spacecraft hull, reaching out with its end gripper",
      tags=["robotic arm", "space arm", "manipulator", "remote arm", "space station", "grapple"])
def _(S):
    return [
        shell(rect(2, 19, 20, 3, min(S.R, 1.5))),
        shell(rect(4, 16, 4, 3, min(S.R, 1))),
        line(seg(6, 16, 9, 6)),
        line(seg(9, 6, 17, 11)),
        shell(circle(9, 6, 2)),
        shell(circle(17, 11, 1.75)),
        line(poly([(18.5, 13.5), (19, 16), (17.5, 17)], r=S.r * 0.5)),
        line(poly([(19, 11), (21.5, 12), (21.5, 14.5)], r=S.r * 0.5)),
    ]


@icon("airlock", CAT, "Round spacecraft hatch door with a central handwheel and hinges, set in a square bulkhead frame",
      tags=["hatch", "space hatch", "bulkhead door", "pressure door", "spacecraft", "space station"])
def _(S):
    out = [
        shell(rect(2.5, 2.5, 19, 19, S.R)),
        detail(circle(12.5, 12, 6.5)),
        detail(circle(12.5, 12, 2.5)),
        detail(seg(4, 9, 6, 9)), detail(seg(4, 15, 6, 15)),
    ]
    for a in (0, 90, 180, 270):
        out.append(detail(seg(*polar(12.5, 12, 2.5, a), *polar(12.5, 12, 4.75, a))))
    return out


@icon("astronaut-bootprint", CAT, "Deep ridged bootprint pressed into powdery lunar soil, seen from above",
      tags=["bootprint", "moon footprint", "lunar footprint", "moon landing", "boot tread", "first step"])
def _(S):
    pts = [(9, 2.5), (15, 2.5), (17, 6), (16.5, 11), (15, 14), (15.5, 18), (14.5, 21.5), (9.5, 21.5),
           (8.5, 18), (9, 14), (7.5, 11), (7, 6)]
    sole = poly(pts, closed=True, r=L(S, 0, 2.2))
    return [
        shell(rot(sole, -12)),
        detail(rseg(7.5, 7, 16.5, 7, -12)),
        detail(rseg(8.5, 11, 16, 11, -12)) if False else detail(rseg(9, 17.5, 15, 17.5, -12)),
    ]


# ============================================================================ boats

@icon("dugout-canoe", CAT, "Canoe carved from a single hollowed log, with its round log end and blunt rounded bow",
      tags=["dugout", "log boat", "pirogue", "canoe", "traditional boat", "river"], aliases=["log-canoe"])
def _(S):
    body = L(S, "M5 9.5H18.5A3.5 3.5 0 0 1 18.5 16.5H5Z", "M5 9.5H18.5A3.5 3.5 0 0 1 18.5 16.5H5Z")
    return [
        shell(body),
        shell(ellipse(5, 13, 2.5, 3.5)),
        dot(5, 13, 1),
        detail(L(S, "M9.5 12H19", "M9.5 12Q14.5 13 19 12")),
        line(wave(3, 21, 20.5, 4, 0.7)),
    ]


@icon("felucca", CAT, "Small wooden sailboat with one tall slanted yard carrying a huge triangular sail",
      tags=["felucca", "lateen sail", "nile boat", "sailboat", "traditional boat", "river"])
def _(S):
    sail = poly([(3, 2.5), (21.5, 15.5), (8, 15.5)], closed=True, r=S.r * 0.5)
    hull = poly([(7, 18), (18, 18), (16, 21.5), (8.5, 21.5)], closed=True, r=S.r * 0.6)
    return [
        shell(sail, stroke_miterlimit="2"),
        detail(seg(12.5, 9.2, 12.5, 15.5)),
        shell(hull, stroke_miterlimit="2"),
        line(seg(12.5, 15.5, 12.5, 18)),
    ]


@icon("racing-hydroplane", CAT, "Long narrow racing boat skimming on its tail with a tall rooster tail of spray behind it",
      tags=["hydroplane", "powerboat racing", "speedboat", "race boat", "rooster tail", "unlimited hydroplane"])
def _(S):
    hull = L(S, "M9 14H18L21.5 15.5V17H9Z",
             "M9.8 14H18L21 15.3Q21.5 15.5 21.5 16V16.2Q21.5 17 20.7 17H9.8A0.8 0.8 0 0 1 9 16.2V14.8A0.8 0.8 0 0 1 9.8 14Z")
    return [
        shell(hull),
        shell(L(S, "M12 14V11.5H15.5L17 14", "M12 14V12.5Q12 11.5 13 11.5H15L17 14")),
        line(L(S, "M7.5 16.5C5 13 3.5 9 3.5 3", "M7.5 16.5C5 13 3.5 9 3.5 3")),
        line(L(S, "M7.5 12.5C6.8 11 6.5 9.5 6.5 7.5", "M7.5 12.5C6.8 11 6.5 9.5 6.5 7.5")),
        dot(7.5, 4, 1.1), dot(9.5, 8.5, 1.1),
        line(seg(3, 20, 21.5, 20)),
    ]


@icon("towboat", CAT, "Square-bowed river towboat with a tall wheelhouse pushing a line of flat barges",
      tags=["pushboat", "push boat", "river barge", "barge tow", "inland shipping", "tug"])
def _(S):
    rr = min(S.R, 1)
    return [
        shell(rect(2, 13.5, 8, 3.5, rr)),
        shell(rect(3, 9, 5.5, 4.5, rr)),
        shell(rect(4, 4, 4, 5, rr)),
        detail(seg(4, 6.5, 8, 6.5)),
        line(seg(3.5, 2.5, 3.5, 4)) if False else line(seg(5, 2, 5, 4)),
        shell(rect(11, 13.5, 11, 3.5, rr)),
        detail(seg(16.5, 13.5, 16.5, 17)),
        line(wave(2.5, 21.5, 20.5, 4, 0.7)),
    ]


# ============================================================================ more space hardware and aircraft

def ell_arc(cx, cy, rx, ry, rot_deg, t0, t1):
    """Arc of a rotated ellipse from parameter angle t0 to t1 (degrees, clockwise on screen)."""
    x0, y0 = ell_pt(cx, cy, rx, ry, rot_deg, t0)
    x1, y1 = ell_pt(cx, cy, rx, ry, rot_deg, t1)
    large = 1 if (t1 - t0) % 360 > 180 else 0
    return f"M{fmt(x0)} {fmt(y0)}A{fmt(rx)} {fmt(ry)} {fmt(rot_deg)} {large} 1 {fmt(x1)} {fmt(y1)}"


def ell_pt(cx, cy, rx, ry, rot_deg, t):
    a = math.radians(rot_deg)
    u, v = rx * math.cos(math.radians(t)), ry * math.sin(math.radians(t))
    return cx + u * math.cos(a) - v * math.sin(a), cy + u * math.sin(a) + v * math.cos(a)


def thick(d, w=1.3):
    """Solid region of a stroked open path (for small solid marks such as horns and needles)."""
    return path_to_d(ST(d, w, "round", "round"))


@icon("sky-crane-helicopter", CAT, "Helicopter with a thin open spine and no cabin, lifting a large crate on cables beneath it",
      tags=["sky crane", "heavy lift helicopter", "flying crane", "cargo helicopter", "sling load", "aviation"],
      aliases=["skycrane"])
def _(S):
    cockpit = L(S, "M15 5.5H19C20.7 5.5 21.5 6.7 21.5 8.5V10H15Z",
                "M16.5 5.5H18.6Q21.5 5.5 21.5 8.5V8.5A1.5 1.5 0 0 1 20 10H16.5A1.5 1.5 0 0 1 15 8.5V7A1.5 1.5 0 0 1 16.5 5.5Z")
    return [
        line(seg(4, 2, 20, 2)),
        line(seg(11.5, 2, 11.5, 5)),
        shell(cockpit),
        shell(rect(8, 5, 7, 5, min(S.R, 1.25))),
        line(seg(8, 7.5, 2.5, 7.5)),
        line(seg(2.5, 3.5, 2.5, 7.5)),
        line(seg(9.5, 10, 8.5, 16)), line(seg(13.5, 10, 14.5, 16)),
        shell(rect(6.5, 16, 10, 5.5, min(S.R, 1.5))),
    ]



def gauge(cx, cy, r, needle_deg):
    """Solid disc with a knocked-out needle, as a single region."""
    tip = polar(cx, cy, r + 0.5, needle_deg)
    return path_to_d(D(P(circle(cx, cy, r)), ST(seg(cx, cy, *tip), 1.1, "butt", "miter")))


def gauge(cx, cy, r, needle_deg):
    """Solid disc with a knocked-out needle slit, as a single region."""
    tip = polar(cx, cy, r * 0.7, needle_deg)
    return path_to_d(D(P(circle(cx, cy, r)), ST(seg(cx, cy, *tip), 1.0, "round", "round")))


@icon("flight-instrument-panel", CAT, "Aircraft instrument panel with two rows of three round gauges",
      tags=["cockpit", "gauges", "dashboard", "flight deck", "avionics", "six pack"],
      aliases=["cockpit-panel"])
def _(S):
    out = [shell(rect(2, 3.5, 20, 17, S.R))]
    angs = [(-60, -90, -130), (-40, -80, -115)]
    for row, y in enumerate((9.25, 14.75)):
        for k, x in enumerate((6.5, 12, 17.5)):
            out.append(mark(gauge(x, y, 2.4, angs[row][k])))
    return out


@icon("livestock-railcar", CAT, "Rail wagon with slatted open sides and a cow's head looking out between the slats",
      tags=["cattle car", "stock car", "cattle wagon", "freight train", "livestock transport", "rail"],
      aliases=["cattle-car"])
def _(S):
    return [
        shell(rect(2, 4, 20, 11.5, L(S, 0.5, 3))),
        detail(seg(6.5, 4, 6.5, 15.5)), detail(seg(17.5, 4, 17.5, 15.5)),
        mark(ellipse(12, 11.6, 2.4, 3.0)),
        mark(ellipse(8.9, 9.3, 1.6, 0.8)), mark(ellipse(15.1, 9.3, 1.6, 0.8)),
        mark(thick("M10.4 9.2Q9.6 7.8 10.3 6.9", 1.1)), mark(thick("M13.6 9.2Q14.4 7.8 13.7 6.9", 1.1)),
        shell(circle(6.5, 19.25, 1.4)), shell(circle(17.5, 19.25, 1.4)),
    ]


@icon("mars-helicopter", CAT, "Small cube-bodied rotorcraft with two stacked rotors on a mast and splayed legs",
      tags=["mars rotorcraft", "planetary drone", "coaxial rotor", "space helicopter", "mars", "rover companion"],
      aliases=["mars-rotorcraft"])
def _(S):
    return [
        line(seg(3, 3.5, 21, 3.5)), line(seg(3.5, 6.5, 20.5, 6.5)),
        line(seg(12, 6.5, 12, 9.5)),
        shell(rect(8.5, 9.5, 7, 5.5, min(S.R, 1.25))),
        line(seg(9.25, 15, 4.5, 20)), line(seg(14.75, 15, 19.5, 20)),
        line(seg(2.5, 20, 6.5, 20)), line(seg(17.5, 20, 21.5, 20)),
    ]


@icon("amphibious-vehicle", CAT, "Boat-hulled bus on wheels driving down a ramp into the water with a splash at its bow",
      tags=["duck boat", "amphibious bus", "land and water", "tour boat", "amphibian", "ramp"],
      aliases=["duck-boat"])
def _(S):
    deg = 16
    hull = L(S, "M2.5 5.3H15.5L20.5 9.8V12.8H2.5Z",
             "M4 5.3H15.5Q16.2 5.3 16.8 5.8L19.7 8.6Q20.5 9.3 20.5 10.3V11.3A1.5 1.5 0 0 1 19 12.8H4A1.5 1.5 0 0 1 2.5 11.3V6.8A1.5 1.5 0 0 1 4 5.3Z")
    cx, cy = 11.5, 9.8
    (w1, w2) = rpts([(6.5, 15.5), (15.5, 15.5)], deg, cx, cy)
    d = (math.cos(math.radians(deg)), math.sin(math.radians(deg)))
    n = (-d[1], d[0])
    off = 4.0
    a = (w1[0] - d[0] * 2.6 + n[0] * off, w1[1] - d[1] * 2.6 + n[1] * off)
    b = (w2[0] + d[0] * 2 + n[0] * off, w2[1] + d[1] * 2 + n[1] * off)
    return [
        shell(rot(hull, deg, cx, cy)),
        detail(rseg(2.5, 9.3, 20.5, 9.3, deg, cx, cy)),
        shell(circle(w1[0], w1[1], 1.5)), shell(circle(w2[0], w2[1], 1.5)),
        line(seg(*a, *b)),
        line(wave(b[0] - 1, 22.5, b[1] + 0.5, 2, 0.8)),
        dot(21.4, 16.4, 1.1), dot(19.2, 18.2, 1.0),
    ]


@icon("caravel", CAT, "Small high-sided wooden sailing ship with a raised stern and two masts carrying triangular lateen sails",
      tags=["sailing ship", "explorer ship", "age of discovery", "lateen sail", "old ship", "voyage"])
def _(S):
    hull = poly([(3, 10), (7, 13), (21.5, 13), (18.5, 18.5), (7, 18.5), (3, 15)], closed=True, r=S.r * 0.6)
    return [
        shell(hull),
        line(seg(10, 13, 10, 2.5)), line(seg(17, 13, 17, 4)),
        shell(poly([(10, 3), (10, 10.5), (4.5, 10.5)], closed=True, r=S.r * 0.4), stroke_miterlimit="3"),
        shell(poly([(17, 4.5), (17, 10.5), (12.5, 10.5)], closed=True, r=S.r * 0.4), stroke_miterlimit="3"),
        line(wave(2, 22, 21.5, 4, 0.7)),
    ]


@icon("ironclad-ship", CAT, "Low armored steamship barely above the waterline with one round gun turret and a short funnel",
      tags=["ironclad", "warship", "monitor ship", "armored ship", "civil war", "naval history"],
      aliases=["monitor-ship"])
def _(S):
    hull = poly([(2.5, 14.5), (21.5, 14.5), (18.5, 19), (5.5, 19)], closed=True, r=S.r * 0.6)
    return [
        shell(hull),
        shell(rect(9, 8.5, 6.5, 6, min(S.R, 2))),
        line(seg(15.5, 11, 20.5, 11)),
        shell(rect(4.5, 9, 2.5, 5.5, 0)),
        line(wave(2, 22, 21.5, 4, 0.7)),
    ]


@icon("air-launch-rocket", CAT, "Large jet carrier plane with a slim winged rocket slung beneath its fuselage",
      tags=["air launch", "airborne launch", "carrier aircraft", "rocket plane", "small satellite launch", "drop launch"],
      aliases=["airborne-launch"])
def _(S):
    body = L(S, "M3 7.5H16C19.5 7.5 21.5 8.6 21.5 9.5C21.5 10.4 19.5 11.5 16 11.5H3Z",
             "M4.5 7.5H16C19.5 7.5 21.5 8.6 21.5 9.5C21.5 10.4 19.5 11.5 16 11.5H4.5A1.5 1.5 0 0 1 3 10V9A1.5 1.5 0 0 1 4.5 7.5Z")
    fin = poly([(3, 7.5), (3, 3), (6.5, 7.5)], closed=True, r=S.r * 0.4)
    rocket = L(S, "M6 15H14.5L19 17.25L14.5 19.5H6Z", "M7 15H14.5L18.4 16.9Q19 17.25 18.4 17.6L14.5 19.5H7A1 1 0 0 1 6 18.5V16A1 1 0 0 1 7 15Z")
    return [
        shell(union(body, fin, poly([(9.5, 7.5), (15.5, 7.5), (12, 2.5), (9.5, 2.5)], closed=True, r=S.r * 0.4))),
        line(seg(10, 11.5, 10, 13)),
        line(seg(14, 11.5, 14, 13)),
        shell(rocket),
        line(poly([(6, 15), (4.5, 13.5)], r=0)),
        line(poly([(6, 19.5), (4.5, 21)], r=0)),
    ]
