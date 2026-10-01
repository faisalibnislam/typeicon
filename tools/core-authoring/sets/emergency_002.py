"""TypeIcon Core: emergency (batch 002).

Police, civil-protection, evacuation, disaster-relief, water-rescue and safety-sign concepts, drawn from the
objects themselves. Closed silhouettes are shells, inner lines are details, small solid marks stay solid in
Line/Rounded and are knocked out of Filled shells. Prohibition and warning signs use the shared helpers below.
Figures follow the stick-figure style of sets/emergency_001.py (solid head r 2.25 over 2 px limbs).
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


def cut(back, front, g=2.5):
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


def head(x, y, r=2.25):
    return dot(x, y, r)


def rr(S, cap):
    return min(S.R, cap)


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


def star(cx, cy, ro, ri, n=5):
    pts = []
    for i in range(2 * n):
        pts.append(polar(cx, cy, ro if i % 2 == 0 else ri, -90 + i * 180 / n))
    return poly(pts, closed=True)


def plus(cx, cy, w, t):
    return union(rect(cx - t / 2, cy - w / 2, t, w), rect(cx - w / 2, cy - t / 2, w, t))


def prohibit(S, *content):
    """Prohibition sign: ring, content and a diagonal slash from top-left to bottom-right."""
    return [shell(circle(12, 12, 9)), *content, detail(seg(5.6, 5.6, 18.4, 18.4))]


def warn(S, *content):
    """Warning triangle with content inside."""
    tri = poly([(12, 2.5), (22, 20.5), (2, 20.5)], closed=True, r=L(S, 0.0, 1.6))
    return [shell(tri), *content]


# ============================================================================ chunk 1

@icon("bleeding-control", CAT, "Gauze pad with a cross pressed onto a forearm, with a downward arrow showing firm pressure",
      tags=["stop the bleed", "pressure", "wound", "first aid", "gauze", "direct pressure", "trauma"])
def _(S):
    pad = rect(8, 9, 8, 7, rr(S, 1.5))
    arm = cut(rect(2, 11, 20, 10.5, rr(S, 3.5)), pad, 2.2)
    return [
        shell(arm),
        shell(pad),
        mark(plus(12, 12.5, 4, 1.4)),
        line(poly([(9, 4.5), (12, 7.2), (15, 4.5)], r=S.r * 0.4)),
        line(seg(12, 2.5, 12, 6.5)),
    ]


@icon("cooling-a-burn", CAT, "Hand held under a running tap with water streaming over it",
      tags=["burn", "cool running water", "tap", "scald", "first aid", "flush", "treatment"])
def _(S):
    return [
        line(seg(2, 5.5, 9, 5.5)),
        shell(rect(9, 3, 10, 5, rr(S, 2))),
        line(seg(11, 10.5, 11, 12.5)), line(seg(14, 10.5, 14, 12.5)), line(seg(17, 10.5, 17, 12.5)),
        shell(rect(2.5, 15.5, 19, 6, rr(S, 3))),
        detail(seg(15.5, 15.5, 15.5, 21.5)), detail(seg(18.5, 15.5, 18.5, 21.5)),
    ]


@icon("first-aid-sign", CAT, "Square safety sign with a solid white cross in the centre",
      tags=["first aid", "medical", "cross", "safety sign", "aid station", "health", "green cross"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 4))),
        mark(plus(12, 12, 11, 4)),
    ]


@icon("custodian-helmet", CAT, "Tall domed police helmet with a top knob, a star badge and a flat brim",
      tags=["police helmet", "bobby", "custodian", "police hat", "officer", "uk police", "constable"])
def _(S):
    dome = "M5.5 16C5.5 8.5 8 5.5 12 5.5C16 5.5 18.5 8.5 18.5 16Z"
    brim = poly([(2.5, 16), (21.5, 16), (21.5, 20.5), (2.5, 20.5)], closed=True, r=S.r)
    return [
        shell(union(dome, brim)),
        mark(star(12, 11.3, 3.6, 1.6)),
        dot(12, 3.4, 1.4),
    ]


@icon("traffic-wand", CAT, "Illuminated traffic baton with a handle and glow lines along its length",
      tags=["baton", "light wand", "traffic control", "marshal", "signal", "airport marshal", "flashlight"])
def _(S):
    d, dx, dy = 45, 0.5, 0.5
    return [
        shell(rotd(rect(10, 2.5, 4, 12, rr(S, 2)), d)),
        line(rseg(12, 14.5, 12, 21.5, d)),
        line(rseg(6.5, 5, 6.5, 11, d)), line(rseg(17.5, 5, 17.5, 11, d)),
    ]


@icon("police-bicycle", CAT, "Bicycle with a rear pannier bag and a headlight beam",
      tags=["police bike", "patrol bike", "bike patrol", "cycle officer", "bicycle", "community policing"])
def _(S):
    return [
        shell(circle(5.5, 17, 3.5)), shell(circle(18.5, 17, 3.5)),
        line(poly([(5.5, 17), (11, 17), (10, 9), (16, 9), (18.5, 17)], r=S.r * 0.5)),
        line(seg(11, 17, 16, 9)),
        shell(rect(2.5, 6, 6, 4.5, rr(S, 1.5))),
        line(seg(14, 7, 17.5, 7)),
        line(seg(20.5, 9, 22, 10)),
    ]


@icon("police-blue-lamp", CAT, "Old square lantern with glass panels hanging from a wall bracket",
      tags=["blue lamp", "police station", "lantern", "police box", "station light", "bracket"])
def _(S):
    return [
        line(seg(3, 2.5, 3, 21.5)),
        line(seg(3, 12, 7, 12)),
        shell(poly([(6.5, 8), (9, 3.5), (15, 3.5), (17.5, 8)], closed=True, r=S.r * 0.5)),
        shell(rect(7, 8, 10, 11, rr(S, 1.5))),
        detail(seg(12, 8, 12, 19)),
        line(seg(20, 8, 21.5, 7)), line(seg(20, 13.5, 22, 13.5)), line(seg(20, 19, 21.5, 20)),
    ]


@icon("missing-person-poster", CAT, "Paper notice with a header bar and a portrait of a head and shoulders",
      tags=["missing", "wanted poster", "lost person", "notice", "search", "flyer", "have you seen"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 2))),
        detail(seg(8, 6, 16, 6)),
        head(12, 11, 2.25),
        detail("M8 18Q8 14.5 12 14.5Q16 14.5 16 18"),
    ]


@icon("shoulder-radio-mic", CAT, "Shoulder speaker microphone with a grille, a push button and a curly cord",
      tags=["radio", "speaker mic", "walkie talkie", "lapel mic", "comms", "push to talk", "officer radio"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 10, 11, rr(S, 3.5))),
        dot(10.5, 6, 1.1), dot(10.5, 10, 1.1),
        mark(rect(18, 5.5, 3, 5, L(S, 0, 1))),
        line("M10.5 13.5C4 14.5 4 17.5 10.5 17.5C17 17.5 17 21 10.5 21.5"),
    ]


@icon("traffic-police-podium", CAT, "Raised traffic stand with a small umbrella canopy on a pole",
      tags=["traffic stand", "point duty", "traffic box", "canopy", "traffic officer", "intersection", "umbrella"])
def _(S):
    return [
        shell("M2.5 10.5C2.5 5 7 2.5 12 2.5C17 2.5 21.5 5 21.5 10.5Z"),
        line(seg(12, 10.5, 12, 16.5)),
        shell(poly([(6.5, 16.5), (17.5, 16.5), (19.5, 21.5), (4.5, 21.5)], closed=True, r=S.r)),
    ]


@icon("lost-child", CAT, "Small child standing alone next to a large question mark",
      tags=["missing child", "lost kid", "separated", "child alone", "amber alert", "find parents", "question"])
def _(S):
    return [
        head(8, 10.5, 2.25),
        line(seg(8, 13, 8, 18)),
        line(poly([(4.5, 15.5), (8, 14), (11.5, 15.5)], r=S.r)),
        line(poly([(5, 21.5), (8, 18), (11, 21.5)], r=S.r)),
        line("M14.5 8.5C14.5 4.5 17 3.5 18.5 3.5C20.5 3.5 21.5 5 21.5 6.8C21.5 9.5 18 10 18 13"),
        dot(18, 16.8, 1.25),
    ]


@icon("safety-officer", CAT, "Person in a hard hat and vest holding a clipboard with a checkmark",
      tags=["site safety", "inspector", "hi-vis", "hard hat", "compliance", "audit", "hse"])
def _(S):
    return [
        shell("M5 8C5 4.2 6.5 2.5 8.5 2.5C10.5 2.5 12 4.2 12 8Z"),
        line(seg(3, 8, 14, 8)),
        head(8.5, 11.8, 2.25),
        shell(poly([(2.5, 21.5), (2.5, 18.5), (5.5, 15.5), (11.5, 15.5), (14.5, 18.5), (14.5, 21.5)], closed=True, r=S.r * 0.6)),
        shell(rect(16, 10, 6, 11.5, rr(S, 1.5))),
        detail(poly([(17.8, 15.8), (19, 17.2), (20.4, 14.6)])),
    ]


@icon("exterior-alarm-box", CAT, "Wall siren box with a flashing lamp on top and sound lines either side",
      tags=["siren", "alarm sounder", "strobe", "outdoor alarm", "burglar alarm", "warning light", "horn"])
def _(S):
    body = union(rect(4.5, 11, 15, 10.5, rr(S, 2.5)), "M8.5 11.5V8A3.5 3.5 0 0 1 15.5 8V11.5Z")
    return [
        shell(body),
        detail(seg(8, 15.5, 16, 15.5)),
        dot(12, 18.5, 1.1),
        line(seg(5, 6, 2.5, 4.5)), line(seg(19, 6, 21.5, 4.5)),
    ]


@icon("wedge-barrier", CAT, "Steel wedge barrier tilted up out of the road surface",
      tags=["road blocker", "vehicle barrier", "anti ram", "security barrier", "bollard", "checkpoint", "hostile vehicle"])
def _(S):
    plate = poly([(5, 16), (17.5, 6), (20.5, 9.5), (8.5, 19)], closed=True, r=S.r * 0.6)
    return [
        shell(plate),
        line(seg(15.5, 21.5, 15.5, 12.5)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("key-control-cabinet", CAT, "Wall cabinet with its door swung open and keys hanging on hooks",
      tags=["key cabinet", "key safe", "key box", "key storage", "lockbox", "hooks", "keys"])
def _(S):
    return [
        shell(rect(9, 2.5, 12.5, 19, rr(S, 2))),
        shell(poly([(2, 5), (6, 3.5), (6, 20.5), (2, 19)], closed=True, r=S.r * 0.4)),
        line(seg(12.5, 6, 12.5, 8.5)), dot(12.5, 10.2, 1.5),
        line(seg(18, 6, 18, 8.5)), dot(18, 10.2, 1.5),
        line(seg(12.5, 13, 12.5, 15.5)), dot(12.5, 17.2, 1.5),
        line(seg(18, 13, 18, 15.5)), dot(18, 17.2, 1.5),
    ]


# ============================================================================ chunk 2

@icon("bomb-disposal-robot", CAT, "Tracked robot with a camera on its body and a jointed arm ending in a gripper claw",
      tags=["eod robot", "bomb squad", "unmanned", "remote vehicle", "explosive ordnance", "tracked robot", "gripper"])
def _(S):
    body = union(rect(2.5, 16.5, 14, 5, rr(S, 2.5)), rect(4.5, 11, 9, 7, rr(S, 2)))
    return [
        shell(body),
        dot(9, 14, 1.25),
        dot(6, 19, 0.9), dot(13, 19, 0.9),
        line(poly([(11.5, 11), (11.5, 5.5), (17.5, 5.5)], r=S.r)),
        line(poly([(21, 2.5), (17.5, 3), (17.5, 8), (21, 8.5)], r=S.r * 0.5)),
    ]


@icon("emergency-exit-sign", CAT, "Rectangular exit sign with a running figure heading towards a doorway",
      tags=["exit", "fire exit", "way out", "evacuation", "escape route", "running man", "egress"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 15, rr(S, 3))),
        dot(8.5, 8.8, 1.4),
        detail(poly([(6, 11.5), (9, 10.8), (10.8, 13)], r=S.r * 0.3)),
        detail(poly([(8.5, 11), (7.5, 14), (10.5, 15.8)], r=S.r * 0.3)),
        detail(poly([(7.5, 14), (5.5, 16)], r=S.r * 0.3)),
        detail(poly([(14.5, 16), (14.5, 8), (18.5, 8), (18.5, 16)])),
    ]


@icon("break-glass-key-box", CAT, "Wall box with a glass front holding a key, and a small hammer on a chain below",
      tags=["break glass", "emergency key", "key box", "glass fronted", "fire alarm key", "hammer", "access"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 2.5))),
        detail(circle(8, 14, 2.25)),
        detail(seg(10.25, 14, 17.5, 14)),
        detail(seg(15, 14, 15, 16.5)),
        detail(poly([(17, 2.5), (14, 6), (16, 8.5), (13.5, 10)], r=0)),
    ]


@icon("keep-exit-clear-sign", CAT, "Doorway with a stack of boxes in front of it crossed out by a prohibition slash",
      tags=["do not block", "clear exit", "no obstruction", "fire door", "emergency exit", "keep clear", "egress"])
def _(S):
    return prohibit(S,
        line(poly([(8.5, 16), (8.5, 7.5), (15.5, 7.5), (15.5, 16)])),
        mark(rect(9.5, 12, 5, 4)),
    )


@icon("shelter-in-place", CAT, "House outline with a person standing inside and the doors and windows closed",
      tags=["stay inside", "lockdown", "stay indoors", "hazard", "civil defence", "indoors", "safe at home"])
def _(S):
    return [
        shell(poly([(2.5, 11), (12, 3), (21.5, 11), (21.5, 21.5), (2.5, 21.5)], closed=True, r=S.r)),
        head(12, 12, 2),
        line(seg(12, 14.5, 12, 18.5)),
        line(poly([(9, 16), (12, 14.8), (15, 16)], r=S.r * 0.5)),
        detail(poly([(9.5, 21.5), (12, 18.5), (14.5, 21.5)])),
    ]


@icon("stairwell-evacuation", CAT, "Two figures walking down a zigzag staircase one after another",
      tags=["stairs", "evacuate", "fire escape", "stairwell", "walk down", "egress", "escape route"])
def _(S):
    return [
        line(poly([(2.5, 12), (8.5, 12), (8.5, 16), (13, 16), (13, 20.5), (21.5, 20.5)], r=S.r * 0.5)),
        head(5.5, 3.6, 2),
        line(seg(5.5, 6.2, 5.5, 8.6)),
        line(poly([(3.5, 10.8), (5.5, 8.6), (7.5, 10.8)])),
        head(15.5, 11.2, 2),
        line(seg(15.5, 13.8, 15.5, 16)),
        line(poly([(13.5, 19), (15.5, 16), (17.5, 19)])),
    ]


@icon("emergency-exit-window", CAT, "Vehicle window with a pull handle along its lower edge and a curved arrow showing it opens",
      tags=["escape hatch", "bus window", "rail carriage", "pull handle", "push out", "evacuate vehicle", "safety window"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 15, rr(S, 5))),
        detail("M7.5 12.5A5 5 0 0 1 16 9"),
        mark(poly([(14, 6.2), (17.6, 8.6), (13.6, 11.2)], closed=True)),
        mark(rect(7, 15.2, 10, 1.8, L(S, 0, 0.9))),
    ]


@icon("brace-position", CAT, "Seated person bent forward with head down and arms over the head behind a seat back",
      tags=["crash position", "brace", "impact", "flight safety", "air safety card", "bend over", "landing"])
def _(S):
    return [
        line(seg(2.5, 3.5, 2.5, 14.5)),
        head(8.5, 13, 2.25),
        line(poly([(18, 16.5), (11.8, 11)], r=S.r * 0.5)),
        line(poly([(11.5, 10.5), (6.5, 8.5), (5, 11)], r=S.r * 0.5)),
        line(poly([(18, 16.5), (18, 21.5)])),
        line(poly([(18, 16.5), (10, 16.5), (10, 21.5)], r=S.r)),
    ]


@icon("emergency-cot", CAT, "Low folding camp cot with a pillow and a folded blanket on top",
      tags=["camp bed", "relief bed", "shelter bed", "folding bed", "refugee", "sleeping", "stretcher bed"])
def _(S):
    return [
        shell(rect(2.5, 10, 19, 5, rr(S, 2))),
        shell(rect(4.5, 5.5, 6, 3, rr(S, 1.2))),
        detail(seg(15, 10, 15, 15)),
        line(seg(5, 15, 9, 21.5)), line(seg(9, 15, 5, 21.5)),
        line(seg(15, 15, 19, 21.5)), line(seg(19, 15, 15, 21.5)),
    ]


@icon("collapsed-building", CAT, "Building floors pancaked and tilted on top of each other after a collapse",
      tags=["earthquake damage", "rubble", "disaster", "structural failure", "pancake collapse", "debris", "ruins"])
def _(S):
    return [
        shell(rect(2.5, 18.5, 19, 3, rr(S, 1.2))),
        shell(poly([(3.5, 14), (20, 11.5), (20.5, 14.5), (4, 16.8)], closed=True, r=S.r * 0.3)),
        shell(poly([(4, 6), (17, 3.8), (17.5, 6.6), (4.6, 8.8)], closed=True, r=S.r * 0.3)),
        dot(20.5, 6.2, 1.1),
    ]


@icon("stranded-on-roof", CAT, "Roof ridge poking out of flood water with a person on top waving an arm",
      tags=["flood rescue", "trapped", "help", "flood victim", "waving", "disaster", "rooftop"])
def _(S):
    return [
        head(12, 3.8, 2),
        line(seg(12, 6.3, 12, 10.5)),
        line(poly([(12, 7.5), (15.5, 5), (17, 2.5)], r=S.r * 0.4)),
        line(poly([(12, 8), (9.5, 10)])),
        line(poly([(4.5, 18.5), (12, 11.5), (19.5, 18.5)], r=S.r * 0.4)),
        line("M2 20.5Q4.5 19 7 20.5T12 20.5T17 20.5T22 20.5"),
    ]


@icon("flooded-car", CAT, "Car sunk in water up to its windows with ripple lines across it",
      tags=["flood", "submerged vehicle", "water damage", "flash flood", "drive through water", "stuck car", "drowned car"])
def _(S):
    car = poly([(3, 15), (3, 12), (6, 10.5), (8.5, 5.5), (15.5, 5.5), (18, 10.5), (21, 12), (21, 15)], closed=True, r=S.r)
    return [
        shell(car),
        detail(seg(8.5, 10.5, 15.5, 10.5)),
        line("M2 18Q4.5 16.5 7 18T12 18T17 18T22 18"),
        line("M2 21.5Q4.5 20 7 21.5T12 21.5T17 21.5T22 21.5"),
    ]


@icon("fallen-tree", CAT, "Uprooted tree lying across a road with a round root ball at one end",
      tags=["storm damage", "blocked road", "tree down", "windthrow", "hurricane", "debris", "obstruction"])
def _(S):
    return [
        shell(union(circle(6.5, 12.5, 4), rect(9, 10.5, 12.5, 4.5, rr(S, 2.25)))),
        line(seg(2, 7.5, 4, 9.5)), line(seg(2, 17.5, 4, 15.5)),
        line(poly([(13.5, 10.5), (13.5, 5.5)])), line(poly([(13.5, 8), (17, 5)])),
        line(poly([(19, 10.5), (21, 7.5)])),
        line(seg(2, 21, 22, 21)),
    ]


@icon("gas-leak", CAT, "Pipe with a hand wheel valve and a cloud of gas puffing out of a crack",
      tags=["gas escape", "natural gas", "propane", "smell gas", "evacuate", "leak", "hazard"])
def _(S):
    cloud = union(circle(14, 9.5, 2.75), circle(18, 7.5, 3.5), circle(20.5, 10.5, 2), rect(14, 10, 6.5, 2.5))
    return [
        shell(cloud),
        shell(rect(2, 14.5, 20, 5.5, rr(S, 2))),
        line(seg(6, 14.5, 6, 10)), line(seg(3, 10, 9, 10)),
        detail(poly([(15, 14.5), (16.5, 17.3), (15, 20)])),
    ]


@icon("burst-pipe", CAT, "Pipe broken in two with water spraying up from the gap in several jets",
      tags=["pipe break", "water leak", "plumbing emergency", "flood", "spraying", "broken pipe", "main break"])
def _(S):
    return [
        shell(rect(2, 14, 7.5, 5.5, rr(S, 2))),
        shell(rect(14.5, 14, 7.5, 5.5, rr(S, 2))),
        line(seg(12, 11, 12, 4)),
        line(seg(10.5, 12, 6.5, 6.5)), line(seg(13.5, 12, 17.5, 6.5)),
        dot(9, 3.8, 1),
        dot(15, 3.8, 1),
    ]


# ============================================================================ chunk 3

def ring_dots(cx, cy, rx, ry, n, r, start=0.0):
    out = []
    for i in range(n):
        a = math.radians(start + i * 360 / n)
        out.append(dot(cx + rx * math.cos(a), cy + ry * math.sin(a), r))
    return out


def wave(y, x0=2.0, x1=22.0, step=5.0, amp=1.5):
    d = f"M{fmt(x0)} {fmt(y)}"
    x = x0
    first = True
    while x < x1 - 0.01:
        if first:
            d += f"Q{fmt(x + step / 2)} {fmt(y - amp)} {fmt(x + step)} {fmt(y)}"
            first = False
        else:
            d += f"T{fmt(x + step)} {fmt(y)}"
        x += step
    return d


@icon("oil-spill-boom", CAT, "Ring of floats around a dark oil slick on the water",
      tags=["oil spill", "containment boom", "spill response", "marine pollution", "slick", "clean up", "floating barrier"])
def _(S):
    return [
        *ring_dots(12, 12, 9, 6.5, 10, 1.7, 18),
        mark(ellipse(12, 12, 4.8, 2.6)),
        line("M2 21Q4.5 19.5 7 21T12 21T17 21T22 21"),
    ]


@icon("capsized-boat", CAT, "Small boat floating upside down with its hull above wavy water",
      tags=["boat overturned", "upside down", "sinking", "water rescue", "maritime emergency", "hull", "shipwreck"])
def _(S):
    return [
        shell("M3 14.5C4 9.5 8 7 12 7C16 7 20 9.5 21 14.5Z"),
        detail("M6.5 12.5Q12 10 17.5 12.5"),
        line("M2 17.5Q4.5 16 7 17.5T12 17.5T17 17.5T22 17.5"),
        line("M2 21.5Q4.5 20 7 21.5T12 21.5T17 21.5T22 21.5"),
    ]


@icon("person-drowning", CAT, "Head and both raised arms just above wavy water lines",
      tags=["drowning", "swimmer in distress", "help", "water danger", "lifeguard", "sinking", "rescue"])
def _(S):
    return [
        head(12, 11.5, 2.25),
        line(poly([(9.8, 14), (6, 9), (5.5, 4.5)], r=S.r * 0.5)),
        line(poly([(14.2, 14), (18, 9), (18.5, 4.5)], r=S.r * 0.5)),
        line("M2 17.5Q4.5 16 7 17.5T12 17.5T17 17.5T22 17.5"),
        line("M2 21.5Q4.5 20 7 21.5T12 21.5T17 21.5T22 21.5"),
    ]


@icon("fallen-through-ice", CAT, "Person up to the chest in a jagged hole in an ice sheet with arms on the edge",
      tags=["ice rescue", "thin ice", "frozen lake", "cold water", "ice hole", "winter danger", "stuck"])
def _(S):
    return [
        head(12, 6, 2.25),
        line(seg(12, 9, 12, 14)),
        line(poly([(6.5, 13.5), (9.5, 10.5), (12, 10)], r=S.r * 0.5)),
        line(poly([(17.5, 13.5), (14.5, 10.5), (12, 10)], r=S.r * 0.5)),
        line(poly([(2, 14), (5, 14), (7, 17.5), (9, 20)])),
        line(poly([(22, 14), (19, 14), (17, 17.5), (15, 20)])),
        line("M9.5 21Q12 19 14.5 21"),
    ]


@icon("hot-car-danger", CAT, "Parked car with heat waves rising above it and a thermometer beside it",
      tags=["heatstroke", "child in car", "pets in cars", "overheating", "summer danger", "high temperature", "hot vehicle"])
def _(S):
    car = poly([(2, 20), (2, 15), (4.5, 13.5), (6.5, 10), (11.5, 10), (13.5, 13.5), (15, 15), (15, 20)], closed=True, r=S.r)
    thermo = union(rect(17.5, 3, 4, 12, rr(S, 2)), circle(19.5, 17.5, 3.25))
    return [
        shell(car),
        detail(seg(7.5, 13, 11, 13)),
        line("M6 6.5Q4.5 5 6 3.5"), line("M11 6.5Q9.5 5 11 3.5"),
        shell(thermo),
        dot(19.5, 17.5, 1.25),
        detail(seg(19.5, 8.5, 19.5, 17)),
    ]


@icon("emergency-broadcast", CAT, "Radio mast sending signal waves, with a small warning triangle beside it",
      tags=["alert system", "public warning", "radio alert", "eas", "siren broadcast", "transmitter", "notification"])
def _(S):
    return [
        line(seg(8, 9.5, 8, 21.5)),
        line(seg(8, 15, 4.5, 21.5)), line(seg(8, 15, 11.5, 21.5)),
        dot(8, 7, 1.3),
        line(arc(8, 7, 3.3, 225, 315)), line(arc(8, 7, 5.6, 225, 315)),
        shell(poly([(18, 12), (22, 20.5), (14, 20.5)], closed=True, r=L(S, 0, 1))),
    ]


@icon("phone-emergency-warning", CAT, "Smartphone with a large warning triangle on its screen",
      tags=["alert", "cell broadcast", "wireless emergency alert", "amber alert", "mobile warning", "push notification", "smartphone"])
def _(S):
    tri = poly([(12, 6), (17.6, 15.6), (6.4, 15.6)], closed=True)
    bang = minus(tri, rect(11, 9.6, 2, 3), circle(12, 14, 0.9))
    return [
        shell(rect(3.5, 2, 17, 20, rr(S, 4))),
        mark(bang),
        mark(rect(10, 18.6, 4, 1.4, L(S, 0, 0.7))),
    ]


@icon("orange-smoke-canister", CAT, "Handheld smoke canister with a pull ring and a thick plume rising from the top",
      tags=["signal smoke", "distress signal", "flare", "marine signal", "rescue marker", "smoke grenade", "visual signal"])
def _(S):
    plume = union(circle(9, 6, 2.75), circle(13.5, 5, 3), circle(17, 7, 2), rect(9, 6, 8, 2.5))
    return [
        shell(plume),
        shell(rect(6, 11, 10, 10.5, rr(S, 3))),
        detail(seg(6, 15.5, 16, 15.5)),
        line(seg(16, 13, 17.5, 13)),
        line(circle(19.5, 13, 2)),
    ]


@icon("ration-pack", CAT, "Sealed food ration pouch with a tear notch at the side and a fork printed on it",
      tags=["meal ready to eat", "mre", "emergency food", "survival food", "food pouch", "relief food", "army ration"])
def _(S):
    pouch = poly([(4, 2.5), (20, 2.5), (20, 9.5), (17.8, 11), (20, 12.5), (20, 21.5), (4, 21.5)], closed=True, r=S.r * 0.4)
    return [
        shell(pouch),
        detail(seg(4, 5.5, 18, 5.5)),
        detail("M9.5 9V12.2Q9.5 14 12 14Q14.5 14 14.5 12.2V9"),
        detail(seg(12, 14, 12, 19)),
    ]


@icon("water-purification-tablets", CAT, "Blister strip of round tablets with a water drop above it",
      tags=["water treatment", "purify water", "chlorine tablets", "safe drinking water", "iodine", "camping", "relief supplies"])
def _(S):
    drop = L(S, "M18 7C18 7 14.5 11.5 14.5 14.5A3.5 3.5 0 0 0 21.5 14.5C21.5 11.5 18 7 18 7Z",
             "M16.8 9Q18 6.8 19.2 9C20.4 10.8 21.5 12.6 21.5 14.5A3.5 3.5 0 0 1 14.5 14.5C14.5 12.6 15.6 10.8 16.8 9Z")
    return [
        shell(circle(7.5, 7.5, 4)),
        detail(seg(4.5, 7.5, 10.5, 7.5)),
        shell(circle(8.5, 17.5, 4)),
        detail(seg(5.5, 17.5, 11.5, 17.5)),
        shell(drop),
    ]


@icon("relief-supplies-box", CAT, "Taped cardboard box with a heart on the front and a water bottle beside it",
      tags=["aid box", "humanitarian aid", "donation", "care package", "charity", "disaster relief", "supplies"])
def _(S):
    heart = "M8.5 19.5C6 17.5 5 16.5 5 15.3C5 14.3 5.8 13.7 6.6 13.7C7.4 13.7 8.2 14.2 8.5 14.9C8.8 14.2 9.6 13.7 10.4 13.7C11.2 13.7 12 14.3 12 15.3C12 16.5 11 17.5 8.5 19.5Z"
    bottle = "M18.3 3H20.2V6C21.2 7 21.5 8 21.5 9V21.5H17V9C17 8 17.3 7 18.3 6Z"
    return [
        shell(rect(2.5, 8, 12, 13.5, rr(S, 2))),
        detail(seg(2.5, 11.5, 14.5, 11.5)),
        mark(heart),
        shell(bottle),
    ]


@icon("food-aid-sack", CAT, "Tied grain sack printed with a wheat ear",
      tags=["grain sack", "flour", "rice sack", "food relief", "famine relief", "humanitarian", "wheat"])
def _(S):
    sack = "M8.5 6.5L7 3.5H17L15.5 6.5C19.5 9 21 13 21 17C21 20.5 18.5 21.5 12 21.5C5.5 21.5 3 20.5 3 17C3 13 4.5 9 8.5 6.5Z"
    return [
        shell(sack),
        detail(seg(8.5, 6.5, 15.5, 6.5)),
        detail(seg(12, 18.5, 12, 11)),
        detail(poly([(9.5, 12.5), (12, 14.5), (14.5, 12.5)])),
        mark(ellipse(12, 10, 1.1, 1.7)),
    ]


@icon("supply-airdrop", CAT, "Crate hanging beneath an open parachute canopy",
      tags=["parachute drop", "air delivery", "humanitarian airlift", "aid drop", "cargo drop", "relief supplies", "descending"])
def _(S):
    return [
        shell(poly([(3, 10.5), (4.8, 6), (9, 2.8), (15, 2.8), (19.2, 6), (21, 10.5)], closed=True, r=S.r * 1.6)),
        line(seg(3.8, 10.5, 9.3, 16.5)), line(seg(20.2, 10.5, 14.7, 16.5)), line(seg(12, 10.5, 12, 16.5)),
        shell(rect(8.5, 16.5, 7, 5, rr(S, 1.5))),
    ]


@icon("water-distribution-point", CAT, "Standpipe with taps along it and a jerry can filling beneath one",
      tags=["water point", "standpipe", "tap stand", "jerry can", "clean water", "relief camp", "refugee camp"])
def _(S):
    can = union(rect(13.5, 13, 8, 8.5, rr(S, 2)), rect(14.5, 10.5, 3, 3))
    return [
        shell(rect(2.5, 3, 19, 4.5, rr(S, 2))),
        line(seg(6, 7.5, 6, 10.5)), line(seg(17.5, 7.5, 17.5, 10.5)),
        dot(6, 14.5, 1.2), dot(6, 19, 1.2),
        shell(can),
    ]


@icon("bucket-toilet", CAT, "Bucket with a toilet seat fitted on top and its lid raised",
      tags=["emergency toilet", "portable toilet", "camping toilet", "sanitation", "disaster toilet", "latrine", "loo"])
def _(S):
    body = union(poly([(5, 12), (19, 12), (17.5, 21.5), (6.5, 21.5)], closed=True, r=S.r), rect(3, 8.5, 18, 4, rr(S, 2)))
    return [
        shell(body),
        detail(seg(5.7, 16.5, 18.3, 16.5)),
        shell(poly([(7, 2.5), (17, 2.5), (17, 6), (7, 6)], closed=True, r=S.r)),
    ]


# ============================================================================ chunk 4

@icon("fallout-shelter-sign", CAT, "Round sign with three downward-pointing triangles arranged inside a ring",
      tags=["civil defense", "nuclear shelter", "bunker", "atomic shelter", "cold war", "radiation refuge", "safe room"])
def _(S):
    return [
        shell(circle(12, 12, 9.25)),
        mark(poly([(6.6, 8), (11, 8), (8.8, 12.4)], closed=True, r=L(S, 0, 0.3))),
        mark(poly([(13, 8), (17.4, 8), (15.2, 12.4)], closed=True, r=L(S, 0, 0.3))),
        mark(poly([(9.8, 13.6), (14.2, 13.6), (12, 18)], closed=True, r=L(S, 0, 0.3))),
    ]


@icon("furniture-anti-tip-strap", CAT, "Tall bookcase fixed to the wall by a short strap at the top",
      tags=["earthquake safety", "bookshelf anchor", "tip over", "child safety", "wall anchor", "secure furniture", "baby proofing"])
def _(S):
    return [
        line(seg(2.5, 2.5, 2.5, 21.5)),
        shell(rect(9, 3, 12.5, 18.5, rr(S, 2))),
        detail(seg(9, 9.5, 21.5, 9.5)), detail(seg(9, 15.5, 21.5, 15.5)),
        line(seg(2.5, 6, 9, 6)),
        mark(rect(4.8, 4.5, 2, 3, 0)),
    ]


@icon("gas-shutoff-wrench", CAT, "Flat open-ended utility wrench with a small flame mark beside it",
      tags=["gas valve", "meter key", "shut off gas", "utility key", "turn off gas", "earthquake kit", "gas meter"])
def _(S):
    d = 40
    head = minus(circle(11, 7, 5), rect(9, 0, 4, 7.5))
    handle = rect(9, 8, 4, 13, rr(S, 2))
    body = union(head, handle)
    return [
        shell(rotd(body, d, 11, 12)),
        mark(flame(18.5, 14, 21.5, 5.5, S)),
    ]


@icon("rescue-board", CAT, "Long rescue paddle board with a pointed nose, a cross on the deck and a grab handle",
      tags=["lifeguard board", "surf rescue", "paddle board", "surf lifesaving", "beach rescue", "water rescue", "rescue sled"])
def _(S):
    d = 40
    board = L(S, "M12 1.5C15.5 4.5 16.5 9.5 16.5 14.5C16.5 19 14.5 22 12 22C9.5 22 7.5 19 7.5 14.5C7.5 9.5 8.5 4.5 12 1.5Z",
              "M12 2C14.4 2 16.5 8 16.5 14.5C16.5 19 14.5 22 12 22C9.5 22 7.5 19 7.5 14.5C7.5 8 9.6 2 12 2Z")
    return [
        shell(rotd(board, d)),
        mark(rotd(plus(12, 12.5, 6, 2), d)),
        detail(rotd(seg(9.8, 18, 14.2, 18), d)),
    ]


@icon("pool-rescue-hook", CAT, "Long pole ending in a large curved shepherd's crook hook above water",
      tags=["reaching pole", "lifeguard hook", "shepherd crook", "swimming pool safety", "drowning rescue", "reach assist", "pole"])
def _(S):
    pts = rpts([(9.5, 19), (9.5, 10), (13, 4.5), (18, 6), (18.5, 10.5)], 12, -1, 0)
    return [
        line(poly(pts, r=L(S, 3, 4.5))),
        line("M2 21.5Q4.5 20 7 21.5T12 21.5T17 21.5T22 21.5"),
    ]


@icon("ice-rescue-picks", CAT, "Pair of ice picks with grip handles and steel spikes joined by a cord",
      tags=["ice safety", "self rescue", "ice awls", "thin ice", "winter safety", "frozen lake", "spikes"])
def _(S):
    ang = 13

    def rot(pts, a):
        return rpts(pts, a, 0, 0, 12, 21.5)
    out = []
    tops = []
    for a in (-ang, ang):
        hp = [(x + (3.6 if a > 0 else -3.6), y) for x, y in rot([(10.2, 5), (13.8, 5), (13.8, 14), (10.2, 14)], a)]
        out.append(shell(poly(hp, closed=True, r=S.r * 0.8)))
        (x1, y1), (x2, y2) = [(x + (3.6 if a > 0 else -3.6), y) for x, y in rot([(12, 14), (12, 21.5)], a)]
        out.append(line(seg(x1, y1, x2, y2)))
        tx, ty = rot([(12, 5)], a)[0]
        tops.append((tx + (3.6 if a > 0 else -3.6), ty))
    (ax, ay), (bx, by) = tops
    out.append(line(f"M{fmt(ax)} {fmt(ay)}Q12 {fmt(ay - 5)} {fmt(bx)} {fmt(by)}"))
    return out


@icon("dan-buoy", CAT, "Man-overboard marker pole with a flag on top, a float in the middle and a weight at the bottom",
      tags=["man overboard", "marker buoy", "pole buoy", "horseshoe buoy", "boat safety", "mob", "dan buoy"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 10)),
        shell(poly([(12, 2.5), (19.5, 5), (12, 7.5)], closed=True, r=S.r * 0.4)),
        shell(rect(7.5, 10, 9, 6, rr(S, 3))),
        line(seg(12, 16, 12, 19)),
        shell(rect(9.5, 19, 5, 2.5, rr(S, 1.2))),
    ]


@icon("immersion-suit", CAT, "One-piece survival suit with a hood, mitts and boots and a zip down the front",
      tags=["survival suit", "exposure suit", "cold water suit", "gumby suit", "abandon ship", "thermal protection", "marine safety"])
def _(S):
    body = poly([(7.5, 9.5), (16.5, 9.5), (20, 13), (19.5, 19), (16.5, 19), (16, 21.5), (13, 21.5), (12, 18),
                 (11, 21.5), (8, 21.5), (7.5, 19), (4.5, 19), (4, 13)], closed=True, r=S.r * 0.7)
    return [
        shell(union(circle(12, 5.5, 3.75), body)),
        mark(ellipse(12, 5.6, 1.8, 1.5)),
        detail(seg(12, 10, 12, 16.5)),
    ]


@icon("rescue-strop", CAT, "Padded horseshoe-shaped rescue sling hanging from two straps and a hoist hook",
      tags=["rescue sling", "helicopter rescue", "hoist", "lifting strop", "horseshoe", "winch rescue", "air sea rescue"])
def _(S):
    u = "M4.5 8V14A7.5 7.5 0 0 0 19.5 14V8H15V14A3 3 0 0 1 9 14V8Z"
    return [
        shell(u),
        line(seg(6.75, 8, 12, 3.6)), line(seg(17.25, 8, 12, 3.6)),
        dot(12, 3.4, 1.5),
    ]


@icon("no-diving-sign", CAT, "Prohibition sign with a slash over a diver entering the water head first",
      tags=["no dive", "shallow water", "swimming pool rules", "diving forbidden", "pool safety", "spinal injury", "keep out of water"])
def _(S):
    return prohibit(S,
        head(14.6, 6.6, 1.4),
        line(poly([(13.8, 8.5), (11.5, 13)])),
        line(seg(11.5, 13, 9.5, 14.5)), 
        line("M6.8 16.5Q8.7 15.3 10.5 16.5T14.2 16.5T17.5 16.5"),
    )


@icon("arc-flash-hood", CAT, "Heavy protective hood with a wide dark face window and a cape over the shoulders",
      tags=["electrical safety", "arc flash suit", "face shield", "ppe", "electrician", "high voltage", "protective hood"])
def _(S):
    cape = poly([(2.5, 21.5), (3.5, 17), (8, 14.5), (16, 14.5), (20.5, 17), (21.5, 21.5)], closed=True, r=S.r * 0.6)
    return [
        shell(union(rect(5.5, 2.5, 13, 13, rr(S, 4)), cape)),
        mark(rect(8, 6, 8, 5, L(S, 0, 1.2))),
        detail(seg(12, 15.5, 12, 21.5)),
    ]


@icon("reflective-armband", CAT, "Wide band with reflective stripes wrapped around an upper arm",
      tags=["slap band", "hi vis band", "night visibility", "safety band", "runner safety", "cycling", "reflector"])
def _(S):
    return [
        line(seg(8, 2.5, 8, 8)), line(seg(16, 2.5, 16, 8)),
        line(seg(8, 16, 8, 21.5)), line(seg(16, 16, 16, 21.5)),
        shell(rect(4.5, 8, 15, 8, rr(S, 2.5))),
        detail(seg(9.5, 8, 9.5, 16)), detail(seg(14.5, 8, 14.5, 16)),
    ]


@icon("no-smoking-sign", CAT, "Prohibition sign with a slash over a lit cigarette",
      tags=["smoking ban", "no cigarettes", "smoke free", "tobacco", "no vaping", "forbidden", "health"])
def _(S):
    return prohibit(S,
        mark(rect(6.3, 12.6, 7, 2.6, L(S, 0, 0.6))),
        mark(rect(14.6, 12.6, 2.6, 2.6, 0)),
        line("M14 10Q12.8 8.8 14.2 7.4"),
    )


@icon("no-water-on-fire-sign", CAT, "Prohibition sign with a slash over a bucket pouring water onto flames",
      tags=["electrical fire", "oil fire", "do not use water", "grease fire", "fire safety", "extinguisher class", "water forbidden"])
def _(S):
    bucket = rotd(poly([(6.5, 6), (12, 6), (10.8, 10.5), (7.7, 10.5)], closed=True), -35, 9, 8)
    return prohibit(S,
        mark(bucket),
        dot(10.5, 13.2, 0.9), dot(11.6, 16, 0.9),
        mark(flame(15, 10.5, 17.5, 4.4, S)),
    )


@icon("no-elevator-in-fire-sign", CAT, "Prohibition sign with a slash over an elevator door beside flames",
      tags=["do not use lift", "use stairs", "fire evacuation", "fire safety", "lift ban", "elevator", "stairs only"])
def _(S):
    return prohibit(S,
        detail(poly([(5.3, 7), (11.9, 7), (11.9, 16.5), (5.3, 16.5)], closed=True, r=S.r)),
        detail(seg(8.6, 7, 8.6, 16.5)),
        mark(flame(15.6, 9.5, 17, 3.8, S)),
    )


# ============================================================================ chunk 5

def sq_poly(x, y, w, h, S, k=1.0):
    """Rectangle as a polygon so Rounded gets fillets and Line stays sharp."""
    return poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], closed=True, r=S.r * k)


@icon("boil-water-notice", CAT, "Pot of boiling water with bubbles rising, beside a small notice card marked with a water drop",
      tags=["boil water advisory", "unsafe tap water", "drinking water warning", "water alert", "purify", "contaminated water", "boil before drinking"])
def _(S):
    drop = "M18.5 4.2C18.5 4.2 16.6 6.4 16.6 7.4A1.9 1.9 0 0 0 20.4 7.4C20.4 6.4 18.5 4.2 18.5 4.2Z"
    return [
        shell(sq_poly(4.5, 12.5, 10.5, 9, S, 1.2)),
        detail(seg(4.5, 15.6, 15, 15.6)),
        line(seg(1.8, 15.5, 4.5, 15.5)), line(seg(15, 15.5, 17.5, 15.5)),
        dot(6, 8.2, 1.2), dot(10, 5.6, 1.2), dot(11.5, 9.2, 1.2),
        shell(rect(15.5, 2.5, 6.5, 8, rr(S, 1.5))),
        mark(drop),
    ]


@icon("pacemaker-prohibited-sign", CAT, "Prohibition sign with a slash over a torso carrying a pacemaker on the chest",
      tags=["pacemaker warning", "implant", "magnetic field", "medical device", "no entry heart device", "strong magnet", "cardiac"])
def _(S):
    return prohibit(S,
        head(12, 7.6, 1.8),
        detail("M7.5 17V14.3Q7.5 11 12 11Q16.5 11 16.5 14.3V17"),
        mark(rect(13.3, 13.2, 2.6, 2, L(S, 0, 0.6))),
    )


@icon("no-metal-objects-sign", CAT, "Prohibition sign with a slash over a key and a watch",
      tags=["no metal", "metal detector", "mri safety", "strong magnet", "remove jewellery", "no keys", "security check"])
def _(S):
    return prohibit(S,
        dot(7.6, 9, 1.9),
        line(seg(9.5, 9, 16.5, 9)), line(seg(14.5, 9, 14.5, 11.6)),
        dot(11.5, 15.8, 1.8),
    )


@icon("keep-out-sign", CAT, "Rectangular sign with a raised open palm and a heading bar",
      tags=["stop", "no entry", "restricted area", "authorised personnel only", "halt", "private", "do not enter"])
def _(S):
    hand = union(rect(6.8, 13, 10.4, 5.5, rr(S, 2)), rect(6.8, 8.5, 2, 6, 0), rect(9.6, 6, 2, 8, 0),
                 rect(12.4, 7, 2, 7, 0), rect(15.2, 9.5, 2, 5, 0))
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        mark(hand),
    ]


@icon("falling-ice-sign", CAT, "Warning triangle with icicles hanging from an edge and small pieces of ice falling",
      tags=["icicles", "ice warning", "roof ice", "winter hazard", "falling ice", "overhead danger", "snow slide"])
def _(S):
    return warn(S,
        mark(poly([(8.4, 11.4), (11.2, 11.4), (9.8, 16.4)], closed=True)),
        mark(poly([(12.4, 11.4), (15.2, 11.4), (13.8, 17.6)], closed=True)),
        dot(16.2, 15.6, 0.9),
    )


@icon("cliff-edge-sign", CAT, "Warning triangle with a figure slipping off the edge of a cliff",
      tags=["steep drop", "precipice", "fall hazard", "danger edge", "hiking warning", "unstable ground", "keep back"])
def _(S):
    return warn(S,
        detail(poly([(6.6, 18.8), (6.6, 14), (11.2, 14)])),
        head(14, 11, 1.3),
        detail(poly([(14, 13), (14.8, 16.5)])),
    )


@icon("asbestos-warning-sign", CAT, "Warning triangle with a bold letter A and loose fibre strands",
      tags=["asbestos", "hazardous fibres", "insulation", "demolition danger", "toxic dust", "construction hazard", "building material"])
def _(S):
    return warn(S,
        detail(poly([(8.8, 18.5), (12, 11), (15.2, 18.5)])),
        detail(seg(10, 16, 14, 16)),
    )


@icon("ladder-hazard-sign", CAT, "Warning triangle with a leaning ladder starting to tip over",
      tags=["ladder safety", "fall from height", "unstable ladder", "working at height", "tipping", "climbing danger", "construction hazard"])
def _(S):
    return warn(S,
        detail(seg(8.2, 18.6, 12, 10.8)),
        detail(seg(12.8, 18.6, 16.6, 10.8)),
        detail(seg(9.2, 16.1, 13.2, 17.7)),
        detail(seg(10.7, 13, 14.7, 14.6)),
    )


@icon("danger-sign", CAT, "Rectangular notice with a solid header band over blank lines of text",
      tags=["danger notice", "hazard notice", "warning board", "site sign", "caution", "keep away", "safety notice"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        mark(sq_poly(5, 5, 14, 5, S, 0.5)),
        detail(seg(6, 14, 18, 14)), detail(seg(6, 18, 14, 18)),
    ]


@icon("safety-record-board", CAT, "Standing scoreboard with a heading bar and one large digit for days without an incident",
      tags=["days without incident", "accident free", "safety scoreboard", "workplace safety", "zero harm", "tally", "record board"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 15.5, rr(S, 2.5))),
        detail(seg(6.5, 6, 17.5, 6)),
        detail(poly([(9, 9.5), (15, 9.5), (11.5, 14.5)], r=S.r * 0.5)),
        line(seg(7, 18, 7, 21.5)), line(seg(17, 18, 17, 21.5)),
    ]


# ============================================================================ chunk 6

def wheels(*xs, y=18.6, r=2.4):
    out = []
    for x in xs:
        out.append(shell(circle(x, y, r)))
    return out


def hubs(*xs, y=18.6):
    return [dot(x, y, 0.8) for x in xs]


@icon("airport-fire-truck", CAT, "Long crash tender in side view with a roof water cannon and three axles",
      tags=["crash tender", "aircraft rescue", "arff", "airfield fire engine", "runway", "foam truck", "fire engine"])
def _(S):
    body = poly([(2, 17), (2, 9.5), (15, 9.5), (16.5, 6.5), (19, 6.5), (22, 11.5), (22, 17)], closed=True, r=S.r * 0.6)
    return [
        shell(body),
        detail(poly([(17.5, 8.5), (19, 8.5), (20.5, 11), (17.5, 11)], closed=True)),
        detail(seg(2, 13.5, 14.5, 13.5)),
        line(poly([(7, 9.5), (7, 5.5), (11.5, 5.5)], r=S.r * 0.5)),
        *wheels(5.5, 11, 18),
        *hubs(5.5, 11, 18),
    ]


@icon("brush-fire-truck", CAT, "Pickup-style fire truck with a water tank and hose reel on the flatbed",
      tags=["wildland engine", "forest fire truck", "bush fire", "type 6 engine", "tanker", "grass fire", "fire engine"])
def _(S):
    cab = poly([(14, 17), (14, 8.5), (17.5, 8.5), (20, 12), (22, 13), (22, 17)], closed=True, r=S.r * 0.6)
    body = union(rect(2, 12.5, 12.5, 4.5, rr(S, 1.2)), rect(3, 6, 9.5, 7.5, rr(S, 3)), cab)
    return [
        shell(body),
        dot(7.7, 9.8, 1.3),
        detail(poly([(16, 10), (18, 10), (19, 12), (16, 12)], closed=True)),
        *wheels(6.5, 18),
        *hubs(6.5, 18),
    ]


@icon("heavy-rescue-truck", CAT, "Boxy rescue truck with roll-up compartment doors along its side and a light bar on the cab",
      tags=["rescue squad", "technical rescue", "extrication", "rescue unit", "fire rescue", "equipment truck", "emergency vehicle"])
def _(S):
    cab = poly([(17, 17), (17, 8), (20, 8), (22, 12), (22, 17)], closed=True, r=S.r * 0.6)
    return [
        shell(union(rect(2, 6, 15.5, 11, rr(S, 2)), cab)),
        detail(rect(4.5, 9, 4.5, 5.5, 0)), detail(rect(10.5, 9, 4.5, 5.5, 0)),
        mark(rect(17.8, 5, 3, 1.6, 0)),
        *wheels(6.5, 18),
        *hubs(6.5, 18),
    ]


@icon("mobile-command-vehicle", CAT, "Large bus-shaped vehicle with antennas and a satellite dish on its roof",
      tags=["command post", "incident command", "mobile operations", "communications van", "emergency control", "satellite truck", "field office"])
def _(S):
    body = poly([(2, 17), (2, 9.5), (19, 9.5), (22, 13), (22, 17)], closed=True, r=S.r * 0.6)
    return [
        shell(body),
        detail(rect(4.5, 11.5, 3.5, 2.5, 0)), detail(rect(9.5, 11.5, 3.5, 2.5, 0)), detail(rect(14.5, 11.5, 3.5, 2.5, 0)),
        shell("M4.5 3.6Q8.5 9 12.5 3.6Z"),
        line(seg(8.5, 7, 8.5, 9.5)),
        line(seg(17, 9.5, 17, 3.5)),
        *wheels(6.5, 17.5),
        *hubs(6.5, 17.5),
    ]


@icon("pedestrian-walkway-sign", CAT, "Round mandatory sign with a walking figure on a marked footpath",
      tags=["pedestrians", "footpath", "walk here", "sidewalk", "walking route", "foot traffic", "mandatory sign"])
def _(S):
    return [
        shell(circle(12, 12, 9.25)),
        head(11.5, 7.2, 1.5),
        detail(poly([(10.3, 10.2), (11.5, 9.4), (13, 10.6)], r=S.r * 0.3)),
        detail(seg(11.4, 9.6, 11, 13.8)),
        detail(poly([(8.8, 17), (11, 13.8), (13.6, 17)], r=S.r * 0.3)),
        mark(rect(6.5, 18.1, 11, 1.4, 0)),
    ]


@icon("team-lift-sign", CAT, "Round mandatory sign with two figures lifting one heavy box together",
      tags=["two person lift", "heavy load", "manual handling", "lifting safety", "share the load", "team lift", "mandatory sign"])
def _(S):
    return [
        shell(circle(12, 12, 9.25)),
        head(7.4, 7.8, 1.3), head(16.6, 7.8, 1.3),
        detail(seg(7.6, 9.6, 8.3, 14.6)), detail(seg(16.4, 9.6, 15.7, 14.6)),
        detail(seg(7.8, 11.2, 10.4, 12.4)), detail(seg(16.2, 11.2, 13.6, 12.4)),
        mark(rect(10, 11.4, 4, 4, 0)),
    ]


@icon("incoming-tide-sign", CAT, "Warning triangle with a small figure and wave lines closing in from below",
      tags=["rising tide", "tidal flats", "cut off by sea", "beach safety", "sandbar", "coastal warning", "sea level"])
def _(S):
    return warn(S,
        head(12, 9.6, 1.25),
        detail(seg(12, 11.6, 12, 13.6)),
        detail("M6.2 16.2Q8.1 14.8 10 16.2T13.8 16.2T17.6 16.2"),
        detail("M5.6 18.8Q7.6 17.4 9.6 18.8T13.6 18.8T17.6 18.8"),
    )


@icon("submerged-rocks-sign", CAT, "Warning triangle with a water line over jagged rocks hidden below the surface",
      tags=["hidden rocks", "shallow water", "underwater hazard", "reef", "swimming danger", "boating hazard", "shoals"])
def _(S):
    return warn(S,
        head(12, 9.8, 1.25),
        detail("M7.4 13.4Q9 12 10.6 13.4T13.8 13.4T16.6 13.4"),
        mark(poly([(6.4, 19), (9, 16), (11, 18), (13.4, 15.6), (17.6, 19)], closed=True)),
    )


@icon("max-occupancy-sign", CAT, "Rectangular sign with a group of figures above the number ten",
      tags=["capacity limit", "maximum people", "crowd limit", "occupancy", "lift capacity", "room limit", "headcount"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        head(7.2, 6.8, 1.4), head(12, 6.8, 1.4), head(16.8, 6.8, 1.4),
        mark(rect(5.8, 9, 2.8, 2.4, L(S, 0, 1))), mark(rect(10.6, 9, 2.8, 2.4, L(S, 0, 1))), mark(rect(15.4, 9, 2.8, 2.4, L(S, 0, 1))),
        detail(poly([(6.8, 15.8), (8.6, 14.3), (8.6, 19.4)])),
        detail(ellipse(14.2, 16.8, 2.2, 2.6)),
    ]


@icon("hydrant-marker-plate", CAT, "Small wall plate with a large letter H and number marks above and below its crossbar",
      tags=["hydrant sign", "fire hydrant marker", "water main plate", "hydrant locator", "fire service sign", "distance plate", "h plate"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, rr(S, 2.5))),
        detail(seg(8.8, 6.5, 8.8, 17.5)), detail(seg(15.2, 6.5, 15.2, 17.5)), detail(seg(8.8, 12, 15.2, 12)),
        mark(rect(10.8, 7.6, 2.4, 2.4, 0)), mark(rect(10.8, 14, 2.4, 2.4, 0)),
    ]
