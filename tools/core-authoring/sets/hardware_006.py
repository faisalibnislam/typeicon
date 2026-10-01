"""TypeIcon Core: hardware (batch 006): construction machines, lifting gear, site safety and protective equipment.

Drawn from the objects themselves in side or front view.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "hardware"


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def mark(d) -> Part:
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def wheel(cx, cy, r=2.75, hub=1.0):
    return [shell(circle(cx, cy, r)), dot(cx, cy, hub)]


# ============================================================================ digging and earth moving

@icon("post-hole-digger", CAT, "Post hole digger with two long handles meeting at a hinge above a split spade shaped scoop",
      tags=["fence post", "digging", "clamshell", "garden", "hole", "manual digger", "fencing"])
def _(S):
    return [
        line(seg(7, 2.5, 10.5, 11)),
        line(seg(17, 2.5, 13.5, 11)),
        shell(poly([(10.5, 11), (13.5, 11), (16, 15), (15, 19.5), (12, 21.5), (9, 19.5), (8, 15)], closed=True, r=S.r)),
        detail(seg(12, 13.5, 12, 21.5)),
    ]


@icon("earth-auger", CAT, "Powered earth auger with an engine head, two side handles and a long spiral bit",
      tags=["drill", "post hole", "digging", "fence", "planting", "spiral bit", "power tool"])
def _(S):
    return [
        shell(rect(9, 2.5, 6, 6, rr(S, 3))),
        line(seg(9, 5.5, 4, 5.5)),
        line(seg(15, 5.5, 20, 5.5)),
        line(seg(4, 3.5, 4, 7.5)),
        line(seg(20, 3.5, 20, 7.5)),
        line(seg(12, 8.5, 12, 21)),
        line(poly([(7.5, 12), (16.5, 14)], r=0)),
        line(poly([(7.5, 16.5), (16.5, 18.5)], r=0)),
    ]


@icon("backhoe-loader", CAT, "Wheeled tractor with a front loader bucket and a jointed digging arm at the back",
      tags=["digger", "jcb", "construction", "excavator", "earthmoving", "tractor", "heavy equipment"])
def _(S):
    return [
        shell(rect(6.5, 10.5, 9.5, 5.5, rr(S, 3))),
        shell(poly([(9, 10.5), (9, 5), (14, 5), (14, 10.5)])),
        line(poly([(6.5, 12), (3, 5.5), (2.5, 10.5)], r=S.r)),
        line(seg(16, 13, 19.5, 14)),
        shell(poly([(19.5, 10.5), (22, 10.5), (22, 16), (19.5, 16)], closed=True, r=S.r * 0.4)),
        *wheel(8.5, 17.5, 3.25),
        *wheel(17, 19, 2),
    ]


@icon("wheel-loader", CAT, "Four wheeled loader with a wide front bucket raised on two lift arms",
      tags=["front loader", "bucket loader", "construction", "earthmoving", "heavy equipment", "payloader"])
def _(S):
    return [
        shell(rect(3, 10, 11.5, 5.5, rr(S, 3))),
        shell(poly([(5.5, 10), (5.5, 4.5), (11.5, 4.5), (11.5, 10)])),
        line(seg(14.5, 12, 18, 10)),
        shell(poly([(17.5, 7.5), (22, 7.5), (21.5, 14.5), (17.5, 14.5)], closed=True, r=S.r * 0.4)),
        *wheel(7, 18, 3),
        *wheel(14, 18, 3),
    ]


@icon("skid-steer", CAT, "Compact loader with a caged cab, small wheels and a front bucket on two side arms",
      tags=["bobcat", "compact loader", "construction", "earthmoving", "small loader", "skid steer loader"])
def _(S):
    return [
        shell(rect(3.5, 12, 12, 5.5, rr(S, 3))),
        shell(poly([(5.5, 12), (5.5, 4.5), (12.5, 4.5), (12.5, 12)])),
        detail(seg(9, 4.5, 9, 12)),
        line(poly([(12.5, 10.5), (17.5, 10.5)], r=0)),
        shell(poly([(17.5, 8), (22, 8), (21.5, 14.5), (17.5, 14.5)], closed=True, r=S.r * 0.4)),
        *wheel(7.5, 18.5, 2.5, 0.8),
        *wheel(13, 18.5, 2.5, 0.8),
    ]


@icon("dump-truck", CAT, "Truck in side view with its tipping bed raised at the back",
      tags=["tipper", "lorry", "haulage", "construction", "mining", "gravel", "tipping truck"])
def _(S):
    return [
        shell(poly([(12.5, 14.5), (2.5, 9.3), (4.4, 5.8), (14.4, 11)], closed=True, r=S.r * 0.4)),
        shell(poly([(16, 16.5), (16, 9.5), (19, 9.5), (21.5, 13), (21.5, 16.5)], closed=True, r=S.r * 0.6)),
        line(seg(2.5, 16, 21.5, 16)),
        *wheel(7, 18.5, 2.75),
        *wheel(17, 18.5, 2.75),
    ]


@icon("articulated-dump-truck", CAT, "Off road hauler with a separate cab and open body joined at a pivot, on big tyres",
      tags=["hauler", "quarry", "mining", "earthmoving", "off road", "construction", "dumper"])
def _(S):
    return [
        shell(poly([(2.5, 6.5), (13, 6.5), (14, 13.5), (2.5, 13.5)], closed=True, r=S.r * 0.6)),
        shell(poly([(15.5, 14.5), (15.5, 9), (18.5, 9), (21.5, 12.5), (21.5, 14.5)], closed=True, r=S.r * 0.6)),
        line(seg(2.5, 14, 21.5, 14)),
        *wheel(8, 17.5, 3.5, 1.1),
        *wheel(18, 17.5, 3.5, 1.1),
    ]


@icon("road-roller", CAT, "Road roller with a large smooth drum at the front, a small cab on top and a rear wheel",
      tags=["steamroller", "compactor", "asphalt", "paving", "road works", "construction", "tarmac"])
def _(S):
    return [
        shell(rect(3, 10, 11.5, 4.5, rr(S, 3))),
        shell(rect(4.5, 4.5, 7, 5.5, rr(S, 2.5))),
        *wheel(7.5, 17.5, 3.5, 1.1),
        *wheel(17.5, 16.5, 4.5, 1.25),
    ]


@icon("motor-grader", CAT, "Long grading machine with a cab at the back, a long frame and a blade under the middle",
      tags=["road grader", "road building", "earthmoving", "levelling", "construction", "heavy equipment"])
def _(S):
    return [
        shell(rect(3, 10.5, 8, 4.5, rr(S, 3))),
        shell(poly([(4, 10.5), (4, 4.5), (9.5, 4.5), (9.5, 10.5)])),
        line(seg(11, 12.5, 20, 12.5)),
        line(seg(20, 12.5, 20, 15)),
        shell(rect(11.5, 15.5, 5.5, 3.5, rr(S, 1))),
        *wheel(6.5, 18.5, 2.5, 0.8),
        *wheel(20, 18, 2.25, 0.7),
    ]


@icon("asphalt-paver", CAT, "Low tracked paving machine with a hopper at the front and a wide screed at the back",
      tags=["road paver", "paving machine", "tarmac", "road works", "construction", "screed", "blacktop"])
def _(S):
    return [
        shell(rect(5, 9.5, 10.5, 5.5, rr(S, 3))),
        shell(poly([(15.5, 6.5), (22, 4.5), (22, 11), (15.5, 12.5)], closed=True, r=S.r * 0.4)),
        line(poly([(8, 4), (12.5, 4)], r=0)),
        line(seg(10, 4, 10, 9.5)),
        shell(rect(2.5, 13.5, 2.5, 7, rr(S, 1))),
        shell(rect(6, 16, 12, 4.5, 2.25)),
    ]


# ============================================================================ lifts and cranes

@icon("scissor-lift", CAT, "Railed work platform raised on a crossed X frame above a wheeled base",
      tags=["aerial work platform", "mewp", "access platform", "elevated work", "construction", "maintenance"])
def _(S):
    return [
        shell(rect(4, 7, 16, 2.25, rr(S, 1))),
        line(poly([(5, 7), (5, 3), (19, 3), (19, 7)], r=S.r)),
        line(seg(8, 9.5, 16, 16)),
        line(seg(16, 9.5, 8, 16)),
        shell(rect(4, 16, 16, 3.5, rr(S, 2.5))),
    ]


@icon("boom-lift", CAT, "Wheeled base with a long angled boom arm ending in a small railed basket",
      tags=["cherry picker", "aerial lift", "access platform", "bucket truck", "maintenance", "mewp"])
def _(S):
    return [
        shell(rect(2.5, 13.5, 11.5, 4, rr(S, 4))),
        line(poly([(6.5, 13.5), (10.5, 6.5), (15.5, 6.5)], r=S.r)),
        shell(rect(15.5, 3.5, 6, 5, rr(S, 3))),
        *wheel(5.5, 19, 2, 0.7),
        *wheel(11, 19, 2, 0.7),
    ]


@icon("telehandler", CAT, "Four wheeled machine with a long telescopic boom and forks on the front",
      tags=["telescopic handler", "forklift", "boom", "lifting", "construction", "farm", "reach truck"])
def _(S):
    return [
        shell(rect(3, 12, 16, 4.5, rr(S, 3))),
        shell(poly([(3, 12), (3, 6.5), (8.5, 6.5), (8.5, 12)])),
        line(seg(9.5, 11, 18, 5.5)),
        line(seg(18, 3.5, 18, 9.5)),
        line(seg(18, 9.5, 22, 9.5)),
        *wheel(7, 18, 2.75),
        *wheel(15.5, 18, 2.75),
    ]


@icon("trencher", CAT, "Tracked machine with a long angled digging chain boom reaching down behind it",
      tags=["trenching", "digger", "chain digger", "cable laying", "construction", "earthmoving", "ditch"])
def _(S):
    return [
        shell(poly([(10.6, 10.65), (5.1, 19.65), (2.9, 18.35), (8.4, 9.35)], closed=True, r=S.r * 0.5)),
        shell(rect(10, 7.5, 8.5, 6.5, rr(S, 3))),
        shell(rect(8.5, 14.5, 13, 5.5, 2.75)),
        dot(12, 17.25, 1),
        dot(18, 17.25, 1),
    ]


@icon("pile-driver", CAT, "Tracked rig with a tall mast, a heavy hammer and a pile being driven into the ground",
      tags=["piling", "foundation", "construction", "hammer", "driving rig", "civil engineering"])
def _(S):
    return [
        line(seg(17, 2.5, 17, 5)),
        shell(rect(14.5, 5, 5, 4.5, rr(S, 2.5))),
        shell(poly([(15.5, 11), (18.5, 11), (18.5, 18), (17, 20.5), (15.5, 18)], closed=True)),
        line(seg(9, 12.5, 17, 3)),
        shell(rect(3, 12, 7, 4, rr(S, 2.5))),
        shell(rect(2.5, 16.5, 11, 4.5, 2.25)),
    ]


@icon("concrete-pump-truck", CAT, "Truck with a long folded boom arm zigzagging along its top and a hose at the tip",
      tags=["concrete pump", "boom pump", "cement", "pouring", "construction", "truck mounted pump", "building site"])
def _(S):
    return [
        line(poly([(5, 13.5), (8, 5), (13.5, 10), (19, 4.5)], r=S.r)),
        line(seg(19, 4.5, 19, 9.5)),
        shell(rect(2.5, 13.5, 13, 3.5, rr(S, 1.5))),
        shell(poly([(16, 17), (16, 11.5), (19, 11.5), (21.5, 14.5), (21.5, 17)], closed=True, r=S.r * 0.6)),
        *wheel(6.5, 19, 2.25, 0.7),
        *wheel(17.5, 19, 2.25, 0.7),
    ]


@icon("cement-truck", CAT, "Truck with a large tilted rotating mixer drum marked with a spiral fin on its back",
      tags=["concrete mixer", "cement mixer", "ready mix", "construction", "transit mixer", "truck", "concrete"])
def _(S):
    return [
        shell(poly([(3.2, 9), (12.6, 4.6), (15.4, 9), (7.8, 16)], closed=True, r=S.r)),
        detail(seg(6.8, 7.3, 10.8, 13.3)),
        shell(poly([(16.5, 17), (16.5, 11), (19.5, 11), (21.5, 14), (21.5, 17)], closed=True, r=S.r * 0.6)),
        line(seg(2.5, 17, 21.5, 17)),
        *wheel(6.5, 19, 2.25, 0.7),
        *wheel(18, 19, 2.25, 0.7),
    ]


@icon("mobile-crane", CAT, "Wheeled truck crane with a cab at the front and a long angled boom with a hanging hook",
      tags=["truck crane", "lifting", "hoist", "construction", "boom", "heavy lift", "all terrain crane"])
def _(S):
    return [
        line(seg(11.5, 12.5, 20.5, 4)),
        line("M21 4V12a1.75 1.75 0 0 1-3.5 0"),
        shell(rect(8, 12.5, 14, 4, rr(S, 1.5))),
        shell(poly([(2.5, 16.5), (2.5, 14), (5, 10.5), (8, 10.5), (8, 16.5)], closed=True, r=S.r * 0.6)),
        *wheel(6, 19, 2.25, 0.7),
        *wheel(17.5, 19, 2.25, 0.7),
    ]


@icon("crawler-crane", CAT, "Tracked crane with a cab on a wide base and a tall lattice boom with a hook on its cable",
      tags=["track crane", "lattice boom crane", "lifting", "construction", "heavy lift", "hoist", "tower"])
def _(S):
    return [
        shell(poly([(9.9, 12.1), (8.1, 9.9), (17.1, 2.4), (18.9, 4.6)], closed=True)),
        line("M20.25 4.5V12.5a1.75 1.75 0 0 1-3.5 0"),
        shell(rect(3.5, 9.5, 7, 6.5, rr(S, 2))),
        shell(rect(2.5, 16.5, 14, 4.5, 2.25)),
    ]


@icon("mini-excavator", CAT, "Small tracked digger with a canopy cab, a bent boom and a bucket",
      tags=["digger", "compact excavator", "construction", "earthmoving", "landscaping", "trenching", "backhoe"])
def _(S):
    return [
        line(poly([(6, 11), (6, 5.5), (11.5, 5.5), (11.5, 11)], r=S.r)),
        line(poly([(12.5, 12), (15.5, 5), (20.5, 9)], r=S.r)),
        shell(poly([(19, 9.5), (22, 11), (21, 14.5), (18.5, 13)], closed=True, r=S.r * 0.4)),
        shell(rect(4, 11, 9.5, 5, rr(S, 2))),
        shell(rect(3, 16.5, 14, 4.5, 2.25)),
    ]


@icon("wrecking-ball", CAT, "Heavy ball swinging on a chain from the arm of a crane mast",
      tags=["demolition", "demolish", "crane", "swing", "construction", "knock down", "destroy"])
def _(S):
    return [
        line(seg(5, 21, 5, 4.5)),
        line(seg(5, 4.5, 14, 4.5)),
        line(seg(5, 11.5, 11, 4.5)),
        line(seg(14, 4.5, 17.5, 11)),
        shell(circle(18, 15, 3.75)),
        line(seg(2.5, 21, 8, 21)),
    ]


@icon("chain-hoist", CAT, "Hoist body hanging from a top hook with a hand chain loop and a lower lifting hook",
      tags=["chain block", "chain fall", "lifting", "rigging", "workshop", "pulley", "load", "manual hoist"])
def _(S):
    return [
        shell(circle(12, 4.5, 2)),
        line(seg(12, 6.5, 12, 8.5)),
        shell(rect(8, 8.5, 8, 5, rr(S, 2.5))),
        line("M9.25 13.5V18.5a1.75 1.75 0 0 1-3.5 0V13.5"),
        line("M14.25 13.5V18.5a2.25 2.25 0 0 0 4.5 0v-1.5"),
    ]


@icon("winch", CAT, "Cable drum between two side plates with a hand crank and a hook on the cable end",
      tags=["windlass", "hoist", "cable", "towing", "recovery", "lifting", "crank", "capstan"])
def _(S):
    return [
        shell(rect(3.5, 3.5, 3, 9, rr(S, 1))),
        shell(rect(15.5, 3.5, 3, 9, rr(S, 1))),
        shell(rect(6.5, 5, 9, 6, rr(S, 1.5))),
        detail(seg(9.5, 5, 9.5, 11)),
        detail(seg(12.5, 5, 12.5, 11)),
        line(poly([(18.5, 8), (21.5, 8), (21.5, 12.5)], r=S.r)),
        line("M11 11V18a2.25 2.25 0 0 0 4.5 0v-1"),
    ]


@icon("bottle-jack", CAT, "Short upright hydraulic jack with a lift saddle on top, a pump socket on the side and a base",
      tags=["hydraulic jack", "car jack", "lifting", "garage", "workshop", "vehicle", "lift", "tool"])
def _(S):
    return [
        shell(rect(7.5, 2.5, 7, 2.5, rr(S, 1))),
        line(seg(11, 5, 11, 8.5)),
        shell(rect(6.5, 8.5, 9, 9.5, rr(S, 3))),
        shell(rect(15.5, 12, 4.5, 3, rr(S, 1))),
        shell(rect(4, 18, 14, 3, rr(S, 1.5))),
    ]


@icon("floor-jack", CAT, "Low wheeled trolley jack with a lifting arm, a round saddle and a long handle",
      tags=["trolley jack", "garage jack", "car lift", "workshop", "vehicle", "hydraulic", "lifting"])
def _(S):
    return [
        line(seg(6.5, 15, 3.5, 3.5)),
        shell(rect(5, 15, 13, 3.5, rr(S, 2))),
        line(seg(9, 15, 18, 10.5)),
        shell(rect(15.5, 7, 6, 2.5, rr(S, 1))),
        *wheel(7, 19.5, 1.75, 0.5),
        *wheel(16, 19.5, 1.75, 0.5),
    ]


@icon("scissor-jack", CAT, "Diamond shaped screw jack with a threaded rod through the middle and flat pads top and bottom",
      tags=["car jack", "screw jack", "lifting", "tyre change", "vehicle", "emergency", "lift", "crank"])
def _(S):
    return [
        line(seg(8.5, 3, 15.5, 3)),
        line(seg(8.5, 21, 15.5, 21)),
        shell(poly([(12, 6.5), (21, 12), (12, 17.5), (3, 12)], closed=True, r=S.r)),
        detail(seg(3, 12, 21, 12)),
    ]


@icon("jack-stand", CAT, "Tripod axle stand with a notched centre post, a cup saddle on top and splayed legs",
      tags=["axle stand", "car stand", "support", "garage", "vehicle repair", "workshop", "safety"])
def _(S):
    return [
        line("M6.5 3Q12 8.5 17.5 3"),
        shell(rect(10, 7, 4, 8, rr(S, 1))),
        line(seg(10.5, 14, 5, 21)),
        line(seg(13.5, 14, 19, 21)),
        line(seg(7.5, 18, 16.5, 18)),
    ]


@icon("engine-hoist", CAT, "Folding workshop crane on wheels with a mast, a long boom, a hydraulic ram and a chain hook",
      tags=["engine crane", "cherry picker", "shop crane", "garage", "workshop", "lifting", "motor hoist"])
def _(S):
    return [
        line(seg(7, 18.5, 7, 7.5)),
        line(seg(7, 7.5, 19, 3.5)),
        line(seg(7, 16.5, 13, 5.5)),
        line("M19 3.5V14a2.25 2.25 0 0 1-4.5 0v-1"),
        line(seg(3, 18.5, 14, 18.5)),
        *wheel(4.5, 20, 1.5, 0.4),
        *wheel(12.5, 20, 1.5, 0.4),
    ]


@icon("stack-light", CAT, "Three stacked beacon segments with a domed top on a short pole and base",
      tags=["signal tower", "andon", "status light", "machine light", "beacon", "factory", "industrial", "warning light"])
def _(S):
    return [
        shell("M7.5 16V7.5a4.5 4.5 0 0 1 9 0V16Z"),
        detail(seg(7.5, 8, 16.5, 8)),
        detail(seg(7.5, 12, 16.5, 12)),
        line(seg(12, 16, 12, 20)),
        line(seg(7, 20.5, 17, 20.5)),
    ]


@icon("road-sweeper", CAT, "Compact street sweeping truck with a hopper at the back and a bristled round brush at the front",
      tags=["street sweeper", "street cleaning", "cleaning", "municipal", "brush", "sweep", "road"])
def _(S):
    star = []
    for i in range(20):
        star.append(polar(18.5, 16.5, 4 if i % 2 == 0 else 2.6, -90 + i * 18))
    return [
        shell(rect(2.5, 9, 9, 7.5, rr(S, 2))),
        shell(poly([(11, 16.5), (11, 8), (14.5, 8), (15.5, 12.5), (15.5, 16.5)], closed=True, r=S.r * 0.5)),
        *wheel(6, 19, 2.25, 0.7),
        *wheel(12.5, 19, 2.25, 0.7),
        shell(poly(star, closed=True), stroke_miterlimit="2"),
        dot(18.5, 16.5, 1),
    ]


@icon("water-truck", CAT, "Tank truck with a round tank on the back and spray droplets at the rear",
      tags=["water tanker", "dust control", "sprinkler truck", "construction", "road works", "spray", "bowser"])
def _(S):
    return [
        shell(rect(6, 6.5, 10, 8.5, rr(S, 4))),
        shell(poly([(16.5, 17), (16.5, 10.5), (19, 10.5), (21.5, 14), (21.5, 17)], closed=True, r=S.r * 0.6)),
        line(seg(6, 17, 21.5, 17)),
        dot(3.25, 10.5, 1),
        dot(3.25, 14, 1),
        dot(3.25, 17.5, 1),
        *wheel(9, 19, 2.25, 0.7),
        *wheel(18, 19, 2.25, 0.7),
    ]


@icon("compact-track-loader", CAT, "Small rubber tracked loader with a caged cab and a front bucket on a short arm",
      tags=["ctl", "track loader", "skid steer", "construction", "landscaping", "earthmoving", "bobcat"])
def _(S):
    return [
        shell(poly([(5.5, 15), (5.5, 4.5), (12.5, 4.5), (12.5, 15)], closed=True, r=S.r)),
        detail(seg(9, 4.5, 9, 15)),
        line(seg(12.5, 10, 17.5, 10)),
        shell(poly([(17.5, 7.5), (22, 7.5), (21.5, 14), (17.5, 14)], closed=True, r=S.r * 0.4)),
        shell(rect(2.5, 15.5, 14, 5.5, 2.75)),
        dot(6.5, 18.25, 1),
        dot(12.5, 18.25, 1),
    ]


@icon("tunnel-boring-machine", CAT, "Front view of a large round cutting wheel with spokes and a toothed rim",
      tags=["tbm", "tunnelling", "mining", "underground", "cutterhead", "construction", "metro", "boring"])
def _(S):
    pts = [polar(12, 12, 9.2 if i % 2 == 0 else 7.9, -90 + i * 15) for i in range(24)]
    sp = [detail(seg(*polar(12, 12, 2.5, a), *polar(12, 12, 7.8, a))) for a in range(-90, 270, 60)]
    return [shell(poly(pts, closed=True, r=S.r * 0.3)), *sp, dot(12, 12, 1.75)]


@icon("drilling-rig", CAT, "Tall lattice derrick with cross bracing standing on a raised deck with a drill pipe running down below",
      tags=["oil rig", "derrick", "oil well", "drilling", "mining", "energy", "petroleum", "borehole"])
def _(S):
    return [
        shell(rect(10, 2.5, 4, 2.5, rr(S, 1))),
        line(seg(10.6, 5, 6.5, 15)),
        line(seg(13.4, 5, 17.5, 15)),
        line(seg(9.4, 8, 17.1, 14)),
        line(seg(14.6, 8, 6.9, 14)),
        shell(rect(3, 15, 18, 2.5, rr(S, 1.25))),
        line(seg(12, 17.5, 12, 21.5)),
    ]


@icon("traffic-barrel", CAT, "Tall tapered drum with two reflective bands and a wide base ring",
      tags=["road drum", "safety drum", "construction", "road works", "traffic", "barrier", "channelizer"])
def _(S):
    return [
        shell(poly([(8, 3.5), (16, 3.5), (17.5, 18.5), (6.5, 18.5)], closed=True, r=S.r * 0.4)),
        detail(seg(7.5, 8, 16.5, 8)),
        detail(seg(7.2, 12.75, 16.8, 12.75)),
        shell(rect(4, 18, 16, 3.25, rr(S, 1.5))),
    ]


@icon("jersey-barrier", CAT, "End view of a concrete road barrier with a wide sloped base and a narrow top",
      tags=["concrete barrier", "road divider", "highway", "safety barrier", "median", "construction", "traffic"])
def _(S):
    return [
        shell(poly([(9.5, 3.5), (14.5, 3.5), (15.5, 11), (19.5, 20.5), (4.5, 20.5), (8.5, 11)], closed=True, r=S.r * 0.4)),
    ]


@icon("road-barricade", CAT, "Horizontal striped board held up by two A frame legs",
      tags=["barrier", "road closed", "roadwork", "construction", "traffic", "blockade", "barrier board"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 19, 6.5, rr(S, 2))),
        detail(seg(8.5, 12, 11, 5.5)),
        detail(seg(14, 12, 16.5, 5.5)),
        line(poly([(3.5, 21.5), (6, 12), (8.5, 21.5)], r=S.r * 0.5)),
        line(poly([(15.5, 21.5), (18, 12), (20.5, 21.5)], r=S.r * 0.5)),
    ]


@icon("caution-tape", CAT, "Wavy ribbon with diagonal stripes stretched between two posts",
      tags=["barrier tape", "warning tape", "police line", "hazard", "danger", "cordon", "safety"])
def _(S):
    return [
        line(seg(3, 3.5, 3, 21.5)),
        line(seg(21, 3.5, 21, 21.5)),
        shell("M5 9Q8.5 6 12 9T19 9V15Q15.5 18 12 15T5 15Z"),
        detail(seg(9.5, 8.3, 7.5, 13)),
        detail(seg(13.5, 9.6, 11.5, 14.6)),
        detail(seg(17.5, 11, 15.5, 16)),
    ]


@icon("road-work-sign", CAT, "Warning triangle sign showing a figure digging with a shovel beside a mound",
      tags=["men at work", "construction sign", "roadworks", "digging", "warning", "worker", "traffic sign"])
def _(S):
    return [
        shell(poly([(12, 3), (21.5, 19.5), (2.5, 19.5)], closed=True, r=S.r)),
        dot(9.5, 11.5, 1.15),
        detail(poly([(9.5, 13.5), (10.5, 17)], r=0)),
        detail(seg(11.5, 12.5, 15, 16.5)),
        detail("M13 17.25Q16 14.75 18.25 17.25"),
    ]


@icon("stop-slow-paddle", CAT, "Octagon sign on a short pole handle, the paddle used by flaggers to stop traffic",
      tags=["stop sign", "flagger", "traffic control", "road works", "lollipop", "crossing", "traffic marshal"])
def _(S):
    return [
        shell(poly(regular(12, 9, 7.75, 8, -67.5), closed=True, r=S.r * 0.4)),
        detail(seg(8.5, 9, 15.5, 9)),
        line(seg(12, 16.75, 12, 21.5)),
    ]


@icon("construction-fence", CAT, "Temporary mesh fence panel standing on two block feet",
      tags=["site fence", "heras fence", "temporary fence", "barrier", "construction", "security", "perimeter"])
def _(S):
    return [
        shell(rect(3, 3.5, 18, 13, rr(S, 4))),
        detail(seg(9, 3.5, 9, 16.5)),
        detail(seg(15, 3.5, 15, 16.5)),
        detail(seg(3, 10, 21, 10)),
        shell(rect(2.5, 17.5, 5, 3.5, rr(S, 1))),
        shell(rect(16.5, 17.5, 5, 3.5, rr(S, 1))),
    ]


@icon("dumpster", CAT, "Open topped tapered waste container with a wide rim and vertical ribs",
      tags=["skip", "waste bin", "rubbish", "trash", "garbage", "construction waste", "container", "bin"])
def _(S):
    return [
        shell(poly([(4, 9), (20, 9), (18.5, 19.5), (5.5, 19.5)], closed=True, r=S.r)),
        detail(seg(9.5, 9, 10, 19.5)),
        detail(seg(14.5, 9, 14, 19.5)),
        shell(rect(2.5, 5.5, 19, 3.5, rr(S, 1.75))),
    ]


@icon("site-office-trailer", CAT, "Long box shaped cabin on blocks with small windows and a door",
      tags=["portable cabin", "site cabin", "construction", "porta cabin", "temporary office", "portakabin", "mobile office"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 19, 10.5, rr(S, 3))),
        mark(rect(5.5, 9, 3.5, 3.5, 0.5)),
        mark(rect(10.75, 9, 3.5, 3.5, 0.5)),
        mark(rect(16, 9, 2.5, 7, 0.5)),
        shell(rect(4, 17.5, 3, 3, rr(S, 1))),
        shell(rect(17, 17.5, 3, 3, rr(S, 1))),
    ]


@icon("warning-beacon", CAT, "Domed flashing light on a small base with rays around it",
      tags=["flashing light", "amber light", "hazard light", "emergency", "construction", "safety", "rotating beacon"])
def _(S):
    rays = [line(seg(*polar(12, 11.5, 6.4, a), *polar(12, 11.5, 8.9, a))) for a in (-90, -45, -135, 0, 180)]
    return [
        shell("M8 16V11.5a4 4 0 0 1 8 0V16Z"),
        shell(rect(6, 16, 12, 3.5, rr(S, 1.75))),
        *rays,
    ]


@icon("sandbag-wall", CAT, "Pyramid of filled sandbags laid in offset rows",
      tags=["flood defence", "flood protection", "barricade", "sand", "emergency", "levee", "bags"])
def _(S):
    k = L(S, 1.25, 2.75)
    bags = [(2.5, 15.5), (8.75, 15.5), (15, 15.5), (5.6, 10.75), (11.9, 10.75), (8.75, 6)]
    return [shell(rect(x, y, 7, 5.5, k)) for x, y in bags]


# ============================================================================ site equipment

def union(*ds) -> str:
    return path_to_d(U(*[P(d) for d in ds]))


@icon("safety-net", CAT, "Sagging rectangular net with a grid pattern hung between two poles",
      tags=["fall protection", "catch net", "scaffold net", "construction", "netting", "debris net", "building site"])
def _(S):
    return [
        line(seg(3, 3.5, 3, 21.5)),
        line(seg(21, 3.5, 21, 21.5)),
        shell("M5 5Q12 10 19 5V14Q12 19 5 14Z"),
        detail(seg(9.5, 7.2, 9.5, 16.2)),
        detail(seg(14.5, 7.2, 14.5, 16.2)),
        detail("M5 9.5Q12 14.5 19 9.5"),
    ]


@icon("debris-chute", CAT, "Chain of stacked funnel tubes running down into a waste skip",
      tags=["rubble chute", "waste chute", "demolition", "construction", "building site", "skip", "refuse"])
def _(S):
    f = [(8, 2.5), (16, 2.5), (14.8, 7), (9.2, 7)]
    return [
        *[shell(poly([(x, y + k * 3.5) for x, y in f], closed=True, r=S.r * 0.5)) for k in range(3)],
        shell(poly([(4.5, 15.5), (19.5, 15.5), (18, 21), (6, 21)], closed=True, r=S.r)),
    ]


@icon("tarp", CAT, "Flat rectangular sheet with grommet holes at the corners and one corner folded over",
      tags=["tarpaulin", "cover", "sheet", "waterproof", "canvas", "camping", "protection", "groundsheet"])
def _(S):
    return [
        shell(poly([(3, 5), (21, 5), (21, 13), (15, 19), (3, 19)], closed=True, r=S.r)),
        detail(poly([(15, 19), (15, 13), (21, 13)], r=0)),
        dot(5.75, 7.75, 1),
        dot(18.25, 7.75, 1),
        dot(5.75, 16.25, 1),
    ]


@icon("ratchet-strap", CAT, "Load strap with a ratchet buckle in the middle and an open hook at each end",
      tags=["tie down", "cargo strap", "lashing", "transport", "trailer", "load securing", "ratchet"])
def _(S):
    return [
        line(arc(4.75, 12, 2.25, 20, 340)),
        line(arc(19.25, 12, 2.25, 200, 160)),
        line(seg(7, 12, 9, 12)),
        line(seg(15, 12, 17, 12)),
        shell(rect(9, 7.5, 6, 9, rr(S, 2.5))),
        detail(seg(12, 7.5, 12, 16.5)),
    ]


@icon("bungee-cord", CAT, "Stretchy coiled elastic cord with a curled hook at each end",
      tags=["shock cord", "elastic cord", "tie down", "stretch", "luggage", "cargo", "hooks", "rope"])
def _(S):
    return [
        line("M7 12H5a2.5 2.5 0 1 1 2.5-2.5"),
        line("M17 12H19a2.5 2.5 0 1 0-2.5-2.5"),
        line("M7 12C8.5 5.5 10 5.5 11 12S13.5 18.5 14 12S15.5 5.5 17 12"),
    ]


@icon("fuel-jerry-can", CAT, "Rectangular fuel can with a carrying handle on top, an embossed X and a pouring spout",
      tags=["gas can", "petrol can", "diesel", "gasoline", "fuel container", "jerrycan", "refuel"])
def _(S):
    return [
        shell(rect(4, 7, 13, 14, rr(S, 3))),
        line(poly([(6.5, 7), (6.5, 3.5), (12.5, 3.5), (12.5, 7)], r=S.r)),
        line(seg(15, 7.5, 19.5, 3.5)),
        line(seg(18, 3.5, 21.5, 5.5)),
        detail(seg(7.5, 11.5, 13.5, 17.5)),
        detail(seg(13.5, 11.5, 7.5, 17.5)),
    ]


@icon("first-aid-cabinet", CAT, "Wall cabinet with a cross on the door and an eyewash bottle standing beside it",
      tags=["first aid kit", "medical cabinet", "emergency", "safety", "workplace", "eye wash", "wall box"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 11.5, 17, rr(S, 3))),
        mark(rect(7.25, 8, 2.5, 8)),
        mark(rect(4.5, 10.75, 8, 2.5)),
        shell(rect(17, 11.5, 4.5, 9, rr(S, 2))),
        line(seg(19.25, 8, 19.25, 11.5)),
    ]


@icon("blueprint-table", CAT, "Tilted drafting table with a blueprint sheet laid out on its board",
      tags=["drafting table", "drawing board", "plans", "architect", "engineer", "design", "technical drawing"])
def _(S):
    return [
        shell(poly([(3, 12), (14, 5), (21, 9), (10, 16)], closed=True, r=S.r * 0.4)),
        detail(seg(8.15, 12.95, 15.85, 8.05)),
        line(seg(6.5, 14, 6.5, 21.5)),
        line(seg(16, 12.2, 16, 21.5)),
    ]


@icon("demolition-site", CAT, "Partly collapsed building with a jagged broken top and pieces of debris falling beside it",
      tags=["demolish", "wrecked", "collapse", "rubble", "knock down", "construction", "destruction"])
def _(S):
    return [
        shell(poly([(4.5, 21), (4.5, 7), (8, 9.5), (10, 5), (12.5, 10), (15, 7.5), (15, 21)], closed=True, r=S.r * 0.4)),
        mark(rect(7, 13, 2, 2.5, 0.4)),
        mark(rect(10.5, 13, 2, 2.5, 0.4)),
        dot(19, 9, 1.25),
        dot(20.5, 14, 1.25),
        dot(18.5, 18.5, 1.25),
    ]


@icon("excavation-pit", CAT, "Cross section of a rectangular hole in the ground with a ladder standing in it",
      tags=["trench", "dig", "hole", "groundwork", "foundation", "construction", "ladder", "earthworks"])
def _(S):
    return [
        line(poly([(2.5, 7), (6, 7), (6, 20), (18, 20), (18, 7), (21.5, 7)], r=S.r)),
        line(seg(10.5, 3.5, 10.5, 17)),
        line(seg(14.5, 3.5, 14.5, 17)),
        line(seg(10.5, 10, 14.5, 10)),
        line(seg(10.5, 14, 14.5, 14)),
    ]


@icon("foundation-footing", CAT, "Cross section of an inverted T shaped concrete footing carrying a wall above",
      tags=["concrete footing", "strip foundation", "groundwork", "building", "construction", "structural", "civil engineering"])
def _(S):
    return [
        shell(poly([(9, 3), (15, 3), (15, 13.5), (21, 13.5), (21, 20.5), (3, 20.5), (3, 13.5), (9, 13.5)], closed=True, r=S.r * 0.4)),
        line(seg(2.5, 9.5, 6.5, 9.5)),
        line(seg(17.5, 9.5, 21.5, 9.5)),
    ]


# ============================================================================ personal protective equipment

@icon("safety-goggles", CAT, "Wide single lens safety goggles with side vents and an elastic strap",
      tags=["ppe", "eye protection", "lab goggles", "workshop", "chemical splash", "protective eyewear", "safety"])
def _(S):
    return [
        shell(poly([(4.5, 7.5), (19.5, 7.5), (19.5, 15), (14.5, 15), (12, 12.75), (9.5, 15), (4.5, 15)], closed=True, r=S.r)),
        line(seg(4.5, 11.25, 2.5, 11.25)),
        line(seg(19.5, 11.25, 21.5, 11.25)),
        dot(7.75, 10.5, 1),
        dot(16.25, 10.5, 1),
    ]


@icon("safety-glasses", CAT, "Wraparound safety glasses with one curved lens and side shields",
      tags=["ppe", "eye protection", "protective glasses", "workshop", "lab", "impact resistant", "shield glasses"])
def _(S):
    return [
        shell(poly([(3.5, 8.5), (12, 6.5), (20.5, 8.5), (20, 13.5), (16, 16.5), (13.5, 13), (10.5, 13), (8, 16.5), (4, 13.5)], closed=True, r=S.r)),
        detail(seg(7, 7.8, 7, 12.5)),
        detail(seg(17, 7.8, 17, 12.5)),
    ]


@icon("ear-muffs-safety", CAT, "Two large round ear cups joined by a headband arching over the top",
      tags=["ear defenders", "hearing protection", "noise", "ppe", "headphones", "earmuffs", "shooting range"])
def _(S):
    return [
        line("M5.75 11a6.25 6.25 0 0 1 12.5 0"),
        shell(rect(2.5, 11, 6, 9.5, rr(S, 3))),
        shell(rect(15.5, 11, 6, 9.5, rr(S, 3))),
    ]


@icon("respirator-mask", CAT, "Half face respirator with two round filter cartridges on the sides and a centre valve",
      tags=["gas mask", "dust mask", "ppe", "filter", "breathing protection", "painting", "hazmat"])
def _(S):
    return [
        shell(poly([(7.5, 6.5), (16.5, 6.5), (18, 12.5), (15.5, 18), (12, 20), (8.5, 18), (6, 12.5)], closed=True, r=S.r)),
        shell(circle(5, 14, 2.5)),
        shell(circle(19, 14, 2.5)),
        dot(12, 14.5, 1.5),
    ]


@icon("face-shield", CAT, "Clear curved visor hanging down from a headband",
      tags=["visor", "splash guard", "ppe", "protective", "face protection", "grinding", "medical"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 3.5, rr(S, 1.75))),
        shell("M5.5 6V16.5Q12 21.5 18.5 16.5V6"),
        detail(seg(9.5, 9.5, 9.5, 13)),
    ]


@icon("safety-harness", CAT, "Full body harness with shoulder straps, a chest ring, a waist strap and two leg loops",
      tags=["fall arrest", "fall protection", "climbing", "work at height", "ppe", "rope access", "straps"])
def _(S):
    return [
        line(seg(8, 2.5, 12, 8.5)),
        line(seg(16, 2.5, 12, 8.5)),
        line(seg(12, 8.5, 12, 14)),
        line(seg(7, 14, 17, 14)),
        shell(circle(8.25, 18, 3)),
        shell(circle(15.75, 18, 3)),
        dot(12, 8.5, 1.5),
    ]


@icon("lanyard-hook", CAT, "Short webbing lanyard with a large snap hook at each end",
      tags=["safety lanyard", "fall arrest", "carabiner", "work at height", "ppe", "tether", "snap hook"])
def _(S):
    return [
        line(arc(5.5, 12, 3.25, 200, 160)),
        line(arc(18.5, 12, 3.25, 20, 340)),
        line(seg(8.75, 12, 15.25, 12)),
    ]


@icon("steel-toe-boot", CAT, "Work boot in side view with a thick sole and a rounded toe cap",
      tags=["safety boot", "work boot", "ppe", "footwear", "construction", "protective shoe", "steel cap"])
def _(S):
    return [
        shell(poly([(5, 3), (13, 3), (13, 9), (17, 11), (21.5, 13.5), (21.5, 19.5), (5, 19.5)], closed=True, r=S.r)),
        detail(seg(5, 16.5, 21.5, 16.5)),
        detail("M15.5 16.5C15.5 14 16.5 12.5 18.25 12"),
    ]


@icon("hard-hat-headlamp", CAT, "Hard hat with a small lamp on its front and light rays shining upward",
      tags=["helmet", "miner", "head torch", "ppe", "construction", "caving", "work light"])
def _(S):
    rays = [line(seg(*polar(12, 16, 9.5, a), *polar(12, 16, 12.2, a))) for a in (-90, -50, -130)]
    return [
        shell("M5 18V16a7 7 0 0 1 14 0v2Z"),
        shell(rect(3, 18, 18, 3, rr(S, 1.5))),
        dot(12, 15, 1.5),
        *rays,
    ]


@icon("eyewash-station", CAT, "Two water jets arcing up from a pair of nozzles over a small basin",
      tags=["eye wash", "emergency wash", "first aid", "lab safety", "rinse", "workplace safety", "fountain"])
def _(S):
    return [
        line("M8 11Q8.5 5.5 11 3.5"),
        line("M16 11Q15.5 5.5 13 3.5"),
        dot(8, 12.5, 1.25),
        dot(16, 12.5, 1.25),
        shell("M4.5 14.5H19.5Q19 20.5 12 20.5T4.5 14.5Z"),
    ]


@icon("fall-arrest-block", CAT, "Round self retracting lifeline housing with its cable and a hook hanging below",
      tags=["self retracting lifeline", "srl", "fall protection", "work at height", "safety line", "ppe", "retractable"])
def _(S):
    return [
        shell(circle(12, 8.5, 5.5)),
        dot(12, 8.5, 1.5),
        line(seg(12, 14, 12, 17.5)),
        line("M12 17.5v.5a2.25 2.25 0 0 0 4.5 0v-1.5"),
    ]


@icon("building-permit", CAT, "Document with a folded corner, a solid house at the top and a round stamp at the bottom",
      tags=["planning permission", "approval", "license", "construction", "certificate", "authorization", "building consent"])
def _(S):
    return [
        shell(poly([(5, 2.5), (14, 2.5), (19, 7.5), (19, 21.5), (5, 21.5)], closed=True, r=S.r)),
        mark(poly([(8.25, 12), (8.25, 9.5), (11.75, 6.5), (15.25, 9.5), (15.25, 12)], closed=True)),
        detail(circle(12, 17, 2)),
    ]


@icon("knee-pads", CAT, "Padded knee cup with a strap on each side",
      tags=["knee protection", "kneepads", "flooring", "tiling", "ppe", "workwear", "protective gear"])
def _(S):
    return [
        shell(poly([(6.5, 4), (17.5, 4), (18.5, 12), (12, 20.5), (5.5, 12)], closed=True, r=S.r)),
        line(seg(2.5, 8.5, 6, 8.5)),
        line(seg(18, 8.5, 21.5, 8.5)),
        line(seg(2.5, 14.5, 5.5, 14.5)),
        line(seg(18.5, 14.5, 21.5, 14.5)),
        detail(seg(9, 9.5, 15, 9.5)),
    ]


@icon("lockout-tag", CAT, "Padlock with a large hanging tag beside it, used to lock out machinery",
      tags=["loto", "lock out tag out", "padlock", "maintenance", "isolation", "safety tag", "do not operate"])
def _(S):
    return [
        line("M5.5 11V7.75a2.75 2.75 0 0 1 5.5 0V11"),
        shell(rect(3, 11, 10, 9.5, rr(S, 2.5))),
        dot(8, 15, 1.25),
        shell(poly([(16, 4.5), (21.5, 4.5), (21.5, 20.5), (16, 20.5)], closed=True, r=S.r * 0.5)),
        dot(18.75, 8, 1),
    ]


@icon("site-hoarding", CAT, "Tall solid panel wall with two posts rising above it and a door in the middle",
      tags=["site fence", "plywood wall", "construction", "boundary", "temporary wall", "barrier", "frontage"])
def _(S):
    return [
        line(seg(5.5, 2.5, 5.5, 5)),
        line(seg(18.5, 2.5, 18.5, 5)),
        shell(rect(2.5, 5, 19, 15.5, rr(S, 3))),
        detail(poly([(8.5, 20.5), (8.5, 10), (15.5, 10), (15.5, 20.5)], r=0)),
        dot(13, 15.25, 0.9),
    ]


def glove(dx=0.0, dy=0.0, k=1.0, cuff=True):
    def X(v): return dx + (v - 12) * k + 12
    def Y(v): return dy + (v - 12) * k + 12
    def R(x, y, w, h, rx): return rect(X(x), Y(y), w * k, h * k, rx * k)
    parts = [R(7, 5, 2.6, 8, 1.3), R(9.6, 3, 2.6, 10, 1.3), R(12.2, 3.5, 2.6, 9.5, 1.3), R(14.8, 5.5, 2.6, 7.5, 1.3),
             R(7, 10, 10.4, 9, 2),
             poly([(X(7.2), Y(16)), (X(3.5), Y(12)), (X(5.4), Y(10.3)), (X(9), Y(13.5))], closed=True)]
    if cuff:
        parts.append(R(7.5, 18, 9.5, 3.5, 1))
    return union(*parts)


@icon("cut-resistant-glove", CAT, "Knit work glove with a cross hatched weave and a knife blade glancing off it",
      tags=["protective glove", "safety glove", "ppe", "kitchen", "glass handling", "blade", "workwear", "cut proof"])
def _(S):
    return [
        shell(glove(-2.5, 1.5, 0.92), stroke_miterlimit="2"),
        detail(seg(8, 15, 11, 18)),
        detail(seg(11, 15, 8, 18)),
        shell(poly([(21.5, 3.5), (21.5, 7.5), (15.5, 10)], closed=True)),
    ]


@icon("welding-gloves", CAT, "Long flared gauntlet glove with a thick seam across the palm",
      tags=["gauntlet", "welder", "heat resistant", "leather", "ppe", "foundry", "workwear", "fireproof glove"])
def _(S):
    g = union(glove(0, -1.5, 1.0, cuff=False),
              poly([(7.5, 14), (16.9, 14), (19, 21.5), (5.5, 21.5)], closed=True))
    return [shell(g, stroke_miterlimit="2"), detail(seg(6.6, 17.5, 17.9, 17.5))]


@icon("welding-apron", CAT, "Heavy full length apron with a neck strap, waist ties and a pocket line, shown flat",
      tags=["leather apron", "welder", "workwear", "blacksmith", "protective clothing", "ppe", "forge"])
def _(S):
    return [
        line("M9 6Q12 1.75 15 6"),
        shell(poly([(9, 6), (15, 6), (15, 11), (18.5, 12), (18.5, 21.5), (5.5, 21.5), (5.5, 12), (9, 11)], closed=True, r=S.r * 0.5)),
        line(seg(5.5, 12.5, 2.5, 15.5)),
        line(seg(18.5, 12.5, 21.5, 15.5)),
        detail(seg(9, 16, 15, 16)),
    ]


@icon("safety-shower", CAT, "Overhead shower head on a bent pipe with a pull ring hanging down and water drops below",
      tags=["emergency shower", "deluge", "decontamination", "lab safety", "chemical spill", "eyewash", "workplace"])
def _(S):
    return [
        line(poly([(4, 21.5), (4, 3.5), (15.5, 3.5), (15.5, 7.5)], r=S.r)),
        shell(poly([(12.5, 7.5), (18.5, 7.5), (21, 10.5), (10, 10.5)], closed=True, r=S.r * 0.4)),
        line(seg(7, 3.5, 7, 8)),
        shell(circle(7, 10.75, 1.75)),
        dot(12.5, 14.5, 1),
        dot(16, 14.5, 1),
        dot(19.5, 14.5, 1),
        dot(14.25, 18.5, 1),
        dot(17.75, 18.5, 1),
    ]


@icon("ppe-kit", CAT, "Hard hat, safety goggles and a glove grouped together as a set of protective gear",
      tags=["protective equipment", "safety gear", "workwear", "construction", "health and safety", "hard hat", "kit"])
def _(S):
    return [
        shell("M6 9.5V8a6 6 0 0 1 12 0v1.5Z"),
        shell(rect(4, 9.5, 16, 2.75, rr(S, 1.4))),
        shell(rect(2.5, 15, 9, 6, rr(S, 3))),
        shell(poly([(14.5, 21.5), (14.5, 16.5), (16, 15), (21.5, 15), (21.5, 21.5)], closed=True, r=S.r)),
        line(seg(14.5, 17.5, 12.5, 16)),
    ]


@icon("fire-extinguisher", CAT, "Upright cylinder extinguisher with a valve and squeeze lever on top and a hose curling down",
      tags=["fire safety", "fire fighting", "emergency", "safety equipment", "extinguish", "flame", "red cylinder"])
def _(S):
    return [
        shell(rect(6.5, 9.5, 8.5, 12, rr(S, 4))),
        shell(rect(8.5, 5.5, 4.5, 4, rr(S, 1))),
        line(poly([(8.5, 3.5), (13.5, 3.5), (16.5, 5)], r=S.r * 0.5)),
        line("M13 7.5H16.5a2.5 2.5 0 0 1 2.5 2.5V17"),
        detail(seg(6.5, 13.5, 15, 13.5)),
    ]


@icon("fire-hose-reel", CAT, "Wall mounted round reel with a spiral of coiled hose and a nozzle end hanging from the rim",
      tags=["fire hose", "fire fighting", "wall reel", "emergency", "fire safety", "hose", "building safety"])
def _(S):
    sp = [polar(11, 11, 1.25 + 5.25 * i / 36, -90 + i * 15) for i in range(37)]
    return [
        shell(circle(11, 11, 9)),
        detail(poly(sp)),
        line("M17.5 17.5Q21 18 21 21"),
    ]
