"""TypeIcon Core: hardware (batch 004): fixings, gears and drives, engine parts, workshop storage, ladders,
tapes and adhesives, plumbing fittings and valves, and electrical supplies.

Drawn from the objects themselves, in front or side view.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "hardware"


# --------------------------------------------------------------------------- helpers

def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def mark(d) -> Part:
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def union(*ds) -> str:
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs) -> str:
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def gear_pts(cx, cy, ro, rt, n, w_root, w_tip, start=-90.0, tilt=0.0):
    """Trapezoid gear outline points. Angles are half widths in degrees."""
    pts = []
    for i in range(n):
        c = start + i * 360.0 / n
        pts += [polar(cx, cy, rt, c - w_root), polar(cx, cy, ro, c - w_tip),
                polar(cx, cy, ro, c + w_tip), polar(cx, cy, rt, c + w_root)]
    return pts


def gear(S, cx, cy, ro, rt, n, wr, wt, start=-90.0, k=0.5):
    return poly(gear_pts(cx, cy, ro, rt, n, wr, wt, start), closed=True, r=S.r * k)


# ============================================================================ fixings, brackets and runners

@icon("block-and-tackle", CAT, "Two pulley wheels linked by rope, with a hook hanging from the lower block",
      tags=["pulley", "hoist", "lifting", "rigging", "rope", "sailing", "winch"])
def _(S):
    return [
        shell(circle(9, 6, 3.75)),
        shell(circle(9, 14, 3.75)),
        dot(9, 6, 1), dot(9, 14, 1),
        line(seg(5.25, 6, 5.25, 14)),
        line(seg(12.75, 6, 12.75, 14)),
        line(poly([(12.75, 6), (12.75, 2.5), (18.5, 2.5), (18.5, 10)], r=S.r)),
        line("M9 17.75v2a2 2 0 0 0 4 0"),
    ]


@icon("caster-wheel", CAT, "Swivel caster: a mounting plate on top, a fork on both sides and a small wheel between",
      tags=["wheel", "castor", "swivel", "trolley", "cart", "furniture", "roller"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 3.5, rr(S, 1.5))),
        line(poly([(6, 6), (6, 17.5)], r=0)),
        line(poly([(18, 6), (18, 17.5)], r=0)),
        shell(circle(12, 16.5, 4.5)),
        dot(12, 16.5, 1.25),
    ]


@icon("drawer-slide", CAT, "Two telescoping runner rails, one partly pulled out of the other, with screw holes",
      tags=["drawer runner", "rail", "glide", "telescopic", "cabinet", "furniture", "hardware"])
def _(S):
    return [
        shell(rect(2.5, 5, 14, 5.5, rr(S, 2.75))),
        shell(rect(8, 13.5, 13.5, 5.5, rr(S, 2.75))),
        dot(6, 7.75, 1),
        dot(12, 16.25, 1),
        dot(17.5, 16.25, 1),
    ]


@icon("drawer-pull", CAT, "Drawer front with a bar handle held by two posts",
      tags=["handle", "cabinet", "furniture", "kitchen", "pull", "drawer handle"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 15, rr(S, 3))),
        detail(seg(7.5, 12, 16.5, 12)),
        mark(circle(7, 12, 1.5)),
        mark(circle(17, 12, 1.5)),
    ]


@icon("cabinet-knob", CAT, "Round cabinet knob on a short neck and a mounting rosette, side view",
      tags=["knob", "handle", "cupboard", "furniture", "door knob", "pull"])
def _(S):
    return [
        line(seg(3.5, 6.5, 3.5, 17.5)),
        line(seg(3.5, 12, 9.5, 12)),
        shell(circle(15, 12, 5.5)),
    ]


@icon("shelf-bracket", CAT, "Right angle shelf bracket with a diagonal brace between wall arm and shelf arm",
      tags=["support", "shelf", "wall mount", "brace", "angle bracket", "diy"])
def _(S):
    return [
        line(poly([(5, 3), (5, 21)], r=0)),
        line(poly([(5, 6.5), (20.5, 6.5)], r=0)),
        line(seg(5, 19.5, 18, 6.5)),
    ]


@icon("l-bracket", CAT, "Flat L shaped angle plate with two screw holes on each leg",
      tags=["angle plate", "corner brace", "bracket", "metal", "fixing", "mounting"])
def _(S):
    return [
        shell(poly([(3.5, 3), (10.5, 3), (10.5, 14.5), (21, 14.5), (21, 21), (3.5, 21)], closed=True, r=S.r)),
        dot(7, 7, 1), dot(7, 11.5, 1), dot(13.5, 18, 1), dot(18, 18, 1),
    ]


@icon("mending-plate", CAT, "Flat straight metal strip with a row of screw holes",
      tags=["flat bracket", "repair plate", "joining plate", "metal strip", "fixing", "carpentry"])
def _(S):
    return [
        shell(rect(2.5, 8, 19, 8, rr(S, 2.5))),
        dot(6, 12, 1), dot(10, 12, 1), dot(14, 12, 1), dot(18, 12, 1),
    ]


@icon("joist-hanger", CAT, "U shaped metal hanger with side flanges cradling the end of a beam",
      tags=["beam hanger", "timber", "carpentry", "construction", "joist", "saddle", "framing"])
def _(S):
    return [
        line(poly([(2, 7), (5.5, 7), (5.5, 18.5), (18.5, 18.5), (18.5, 7), (22, 7)], r=S.r)),
        shell(rect(9, 2.5, 6, 11, rr(S, 1.5))),
    ]


@icon("ball-bearing", CAT, "Bearing seen from the front: outer ring, inner ring and a ring of balls between them",
      tags=["bearing", "rolling", "machine", "race", "engine", "mechanical", "spin"])
def _(S):
    balls = []
    for i in range(8):
        x, y = polar(12, 12, 6.25, i * 45 + 22.5)
        balls.append(mark(circle(x, y, 1.2)) if S.name == "rounded" else mark(rect(x - 1.1, y - 1.1, 2.2, 2.2)))
    return [shell(circle(12, 12, 9.5)), shell(circle(12, 12, 3.5))] + balls


@icon("gear-wheel", CAT, "Spur gear with square teeth around the rim and a hole in the hub",
      tags=["gear", "cog", "spur gear", "mechanism", "engineering", "machine", "teeth"])
def _(S):
    return [shell(gear(S, 12, 12, 10, 7.6, 8, 12, 8)), detail(circle(12, 12, 2.8))]


@icon("sprocket", CAT, "Flat chain wheel with pointed hooked teeth and a hole in the middle",
      tags=["chain wheel", "chainring", "bicycle", "drive", "teeth", "gear", "motorcycle"])
def _(S):
    pts = []
    n = 10
    for i in range(n):
        c = -90 + i * 36
        pts += [polar(12, 12, 7.2, c), polar(12, 12, 9.4, c + 10), polar(12, 12, 7.2, c + 20)]
    return [shell(poly(pts, closed=True, r=S.r * 0.4)), detail(circle(12, 12, 3))]


@icon("worm-gear", CAT, "Threaded worm screw meshing with a toothed wheel below it",
      tags=["worm drive", "gearbox", "screw", "mechanism", "reduction gear", "drive"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 5.5, rr(S, 2.5))),
        detail(seg(7, 2.5, 9, 8)),
        detail(seg(12, 2.5, 14, 8)),
        detail(seg(17, 2.5, 19, 8)),
        shell(gear(S, 12, 15.5, 6.5, 5, 10, 11, 7, k=0.3)),
        dot(12, 15.5, 1.1),
    ]


@icon("rack-and-pinion", CAT, "Small round gear meshing with a straight toothed bar",
      tags=["rack", "pinion", "steering", "linear motion", "gear", "mechanism", "drive"])
def _(S):
    pts = [(2.5, 21), (2.5, 17), (4.5, 17), (4.5, 14.5), (7.5, 14.5), (7.5, 17), (10.5, 17), (10.5, 14.5)]
    pts = [(2.5, 21), (2.5, 14.5), (4.5, 14.5), (4.5, 17), (7.5, 17), (7.5, 14.5), (10.5, 14.5), (10.5, 17),
           (13.5, 17), (13.5, 14.5), (16.5, 14.5), (16.5, 17), (19.5, 17), (19.5, 14.5), (21.5, 14.5), (21.5, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.3)),
        shell(gear(S, 12, 8, 6.2, 4.6, 8, 14, 9, k=0.3)),
        dot(12, 8, 1.25),
    ]


# ============================================================================ drives and engine parts

@icon("belt-drive", CAT, "A large and a small pulley joined by a belt loop",
      tags=["pulley", "belt", "transmission", "drive", "machine", "motor", "v-belt"])
def _(S):
    return [
        shell(circle(7, 12, 5)),
        shell(circle(18, 12, 3)),
        mark(circle(7, 12, 1.25)) if S.name == "rounded" else mark(rect(5.85, 10.85, 2.3, 2.3)),
        mark(circle(18, 12, 1)) if S.name == "rounded" else mark(rect(17, 11, 2, 2)),
        line(seg(7.9, 7.08, 18.55, 9.05)),
        line(seg(7.9, 16.92, 18.55, 14.95)),
    ]


@icon("piston", CAT, "Engine piston with a ring groove near the crown and a connecting rod below",
      tags=["engine", "cylinder", "combustion", "motor", "connecting rod", "automotive", "mechanic"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 10.5, rr(S, 3))),
        detail(seg(6, 6, 18, 6)),
        mark(circle(12, 10, 1.25)),
        line(seg(12, 10, 12, 15.5)),
        shell(circle(12, 18.5, 3)),
    ]


@icon("crankshaft", CAT, "Engine crankshaft with offset throws and round counterweights",
      tags=["engine", "shaft", "crank", "motor", "automotive", "cylinder", "rotation"])
def _(S):
    return [
        line(poly([(2.5, 12), (5.5, 12), (5.5, 6), (9.5, 6), (9.5, 12), (14.5, 12), (14.5, 18), (18.5, 18),
                   (18.5, 12), (21.5, 12)], r=S.r)),
        solid(circle(5.5, 17, 2.5)),
        solid(circle(18.5, 7, 2.5)),
    ]


@icon("spark-plug", CAT, "Spark plug with a ribbed insulator, a hex nut, a threaded body and a bent electrode",
      tags=["engine", "ignition", "automotive", "car part", "combustion", "mechanic", "plug"])
def _(S):
    return [
        line(seg(12, 1.5, 12, 3.5)),
        shell(rect(9.5, 3.5, 5, 6.5, rr(S, 1.5))),
        detail(seg(9.5, 6.75, 14.5, 6.75)),
        shell(rect(7, 10, 10, 4, rr(S, 1.5))),
        shell(rect(9.5, 14, 5, 4.5, rr(S, 1))),
        line(poly([(12, 18.5), (12, 22), (15, 22)], r=0)),
    ]


@icon("hydraulic-cylinder", CAT, "Hydraulic cylinder: a tube with a rod sticking out of one end and a mounting eye on each end",
      tags=["hydraulic ram", "actuator", "piston rod", "machinery", "excavator", "pneumatic", "linear"])
def _(S):
    return [
        shell(rect(6, 7.5, 10, 9, rr(S, 3))),
        detail(seg(13, 7.5, 13, 16.5)),
        solid(circle(3.5, 12, 1.9)),
        line(seg(16, 12, 19, 12)),
        solid(circle(20.25, 12, 2)),
    ]


@icon("shaft-coupling", CAT, "Short cylinder joining two shafts end to end, with two set screws",
      tags=["coupler", "shaft", "motor", "mechanical", "machine", "connector", "drive"])
def _(S):
    return [
        shell(rect(6, 7, 12, 10, rr(S, 2))),
        line(seg(2, 12, 6, 12)),
        line(seg(18, 12, 22, 12)),
        detail(seg(12, 7, 12, 17)),
        dot(9, 12, 1), dot(15, 12, 1),
    ]


@icon("shock-absorber", CAT, "Shock absorber: a coil spring around a damper with a mounting eye at each end",
      tags=["suspension", "damper", "spring", "strut", "automotive", "car part", "coilover"])
def _(S):
    return [
        solid(circle(12, 3.25, 1.75)),
        line(seg(12, 5, 12, 6)),
        shell(rect(7, 6, 10, 12, rr(S, 2.5))),
        detail(seg(7, 10.5, 17, 8.5)),
        detail(seg(7, 15, 17, 13)),
        line(seg(12, 18, 12, 19)),
        solid(circle(12, 20.75, 1.75)),
    ]


def _handwheel_filled():
    kx, ky = polar(12, 12, 6.0, 45)
    rim = D(P(circle(12, 12, 10)), P(circle(12, 12, 7)))
    spokes = [ST(seg(12, 6, 12, 18), 2.5), ST(seg(6, 12, 18, 12), 2.5)]
    hub = P(circle(12, 12, 3.25))
    knob = P(circle(kx, ky, 2))
    return U(rim, hub, knob, *spokes)


@icon("handwheel", CAT, "Round valve wheel with four spokes and a small crank knob on the rim",
      tags=["wheel", "hand crank", "valve wheel", "machine", "turn", "manual", "machining"],
      filled=_handwheel_filled)
def _(S):
    kx, ky = polar(12, 12, 6.0, 45)
    hub = shell(circle(12, 12, 3)) if S.name == "rounded" else shell(rect(9.25, 9.25, 5.5, 5.5))
    return [
        shell(circle(12, 12, 9)),
        hub,
        line(seg(12, 3, 12, 9)),
        line(seg(12, 15, 12, 21)),
        line(seg(3, 12, 9, 12)),
        line(seg(15, 12, 21, 12)),
        solid(circle(kx, ky, 1.75)),
    ]


# ============================================================================ keys and workshop storage

@icon("key-blank", CAT, "Uncut key blank with a round bow and a smooth straight blade",
      tags=["key", "locksmith", "duplicate", "copy key", "hardware store", "lock", "unfinished"])
def _(S):
    return [
        shell(circle(7, 12, 4.75)),
        dot(7, 12, 1.25),
        shell(poly([(11.75, 9.5), (20.5, 9.5), (20.5, 14.5), (11.75, 14.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("key-cutting", CAT, "Key held level while a round cutting wheel touches its blade, with a spark",
      tags=["key duplicating", "locksmith", "grinder", "copy key", "hardware store", "lock", "machine"])
def _(S):
    return [
        shell(circle(16, 8, 5)),
        dot(16, 8, 1.25),
        shell(circle(5.75, 18, 3)),
        line(seg(8.5, 18, 21.5, 18)),
        line(seg(10, 12.5, 8, 10.5)),
        line(seg(7.5, 14.5, 5, 13.5)),
    ]


@icon("pegboard", CAT, "Perforated board with rows of holes and a screwdriver hanging from a peg",
      tags=["tool wall", "workshop", "garage", "storage", "hooks", "organizer", "tool board"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 2.5))),
        mark(circle(7, 7, 1)), mark(circle(12, 7, 1)), mark(circle(17, 7, 1)),
        mark(circle(7, 12, 1)), mark(circle(17, 12, 1)),
        detail(seg(12, 11, 12, 14.5)),
        mark(rect(10.25, 14.5, 3.5, 4.5, 1)),
    ]


@icon("parts-organizer", CAT, "Small parts case with a grid of drawers, each with a tiny pull",
      tags=["storage", "screws", "fasteners", "drawers", "bin", "workshop", "compartments"])
def _(S):
    return [
        shell(rect(2.5, 4, 19, 16, rr(S, 2.5))),
        detail(seg(8.83, 4, 8.83, 20)),
        detail(seg(15.17, 4, 15.17, 20)),
        detail(seg(2.5, 12, 21.5, 12)),
        mark(circle(5.67, 9, 0.9)), mark(circle(12, 9, 0.9)), mark(circle(18.33, 9, 0.9)),
        mark(circle(5.67, 17, 0.9)), mark(circle(12, 17, 0.9)), mark(circle(18.33, 17, 0.9)),
    ]


@icon("rolling-tool-cabinet", CAT, "Tool chest with a lid, three wide drawers and small caster wheels",
      tags=["tool chest", "toolbox", "garage", "workshop", "storage", "mechanic", "drawers"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 15.5, rr(S, 2.5))),
        detail(seg(3, 6.5, 21, 6.5)),
        detail(seg(3, 10.5, 21, 10.5)),
        detail(seg(3, 14.5, 21, 14.5)),
        solid(circle(7, 20.25, 1.75)),
        solid(circle(17, 20.25, 1.75)),
    ]


@icon("tool-bag", CAT, "Open tool bag with a rounded handle arching over the top and tools poking out",
      tags=["toolbox", "carry", "tradesman", "kit bag", "mechanic", "plumber", "tote"])
def _(S):
    return [
        shell(poly([(3, 11), (21, 11), (19.5, 21), (4.5, 21)], closed=True, r=S.r)),
        line("M6.5 11a5.5 5.5 0 0 1 11 0"),
        line(seg(10, 11, 10, 7.5)),
        line(seg(14, 11, 14, 8.5)),
        detail(seg(3.75, 15.5, 20.25, 15.5)),
    ]


@icon("workbench", CAT, "Sturdy workbench with a thick top, a bench vise at one end and a lower shelf",
      tags=["work table", "carpentry", "garage", "workshop", "vise", "shop", "diy"])
def _(S):
    return [
        shell(rect(2, 8, 20, 3.5, rr(S, 1.75))),
        shell(rect(14.5, 2.5, 5, 5.5, rr(S, 1.5))),
        line(seg(19.5, 5.25, 22, 5.25)),
        line(seg(4.5, 11.5, 4.5, 21.5)),
        line(seg(19.5, 11.5, 19.5, 21.5)),
        line(seg(4.5, 16.5, 19.5, 16.5)),
    ]


@icon("sawhorse", CAT, "Sawhorse: a horizontal beam on two splayed pairs of legs",
      tags=["trestle", "carpentry", "support", "woodworking", "a frame", "construction", "cutting stand"])
def _(S):
    return [
        shell(rect(2, 4, 20, 4, rr(S, 2))),
        line(seg(7, 8, 4, 21.5)),
        line(seg(17, 8, 20, 21.5)),
        line(seg(9, 8, 12, 21.5)),
        line(seg(15, 8, 12, 21.5)),
        line(seg(5.6, 14.5, 18.4, 14.5)),
    ]


@icon("step-stool", CAT, "Two step folding stool seen from the side",
      tags=["steps", "kitchen stool", "reach", "household", "ladder", "foldable", "stepladder"])
def _(S):
    return [
        shell(rect(4, 3.5, 14, 3, rr(S, 1.5))),
        line(seg(6, 6.5, 3.5, 21.5)),
        line(seg(16, 6.5, 19.5, 21.5)),
        line(poly([(4.6, 14), (17.4, 14)], r=0)),
    ]


@icon("extension-ladder", CAT, "Two ladder sections side by side, the upper one slid up to extend the reach",
      tags=["ladder", "climb", "roofing", "painter", "construction", "telescoping ladder", "extended"])
def _(S):
    return [
        line(poly([(3.5, 9), (3.5, 21.5)], r=0)), line(poly([(9.5, 9), (9.5, 21.5)], r=0)),
        line(seg(3.5, 12.5, 9.5, 12.5)), line(seg(3.5, 16.5, 9.5, 16.5)), line(seg(3.5, 20.5, 9.5, 20.5)),
        line(poly([(14, 2.5), (14, 15)], r=0)), line(poly([(20, 2.5), (20, 15)], r=0)),
        line(seg(14, 6, 20, 6)), line(seg(14, 10, 20, 10)), line(seg(14, 14, 20, 14)),
    ]


@icon("scaffolding", CAT, "Scaffold frame with upright poles, a plank platform, a guard rail and cross braces",
      tags=["construction", "building site", "platform", "poles", "working at height", "formwork", "frame"])
def _(S):
    return [
        line(seg(5, 2.5, 5, 21.5)),
        line(seg(19, 2.5, 19, 21.5)),
        shell(rect(2.5, 7.5, 19, 3, rr(S, 1.5))),
        line(seg(5, 10.5, 19, 21)),
        line(seg(19, 10.5, 5, 21)),
    ]


@icon("scaffold-tower", CAT, "Narrow rolling scaffold tower with ladder rungs, a platform with a guard rail and caster wheels",
      tags=["mobile scaffold", "platform tower", "construction", "painting", "working at height", "rolling", "ladder frame"])
def _(S):
    return [
        line(poly([(7.5, 7), (7.5, 2.5), (16.5, 2.5), (16.5, 7)], r=S.r)),
        shell(rect(4.5, 7, 15, 2.5, rr(S, 1.25))),
        line(seg(7.5, 9.5, 7.5, 19)),
        line(seg(16.5, 9.5, 16.5, 19)),
        line(seg(7.5, 13, 16.5, 13)),
        line(seg(7.5, 17, 16.5, 17)),
        solid(circle(7.5, 20.75, 1.75)),
        solid(circle(16.5, 20.75, 1.75)),
    ]


# ============================================================================ tapes and adhesives

@icon("duct-tape", CAT, "Thick roll of wide tape with a torn strip hanging off the edge",
      tags=["gaffer tape", "adhesive", "repair", "fix", "sticky tape", "silver tape", "hardware"])
def _(S):
    return [
        shell(circle(10.5, 10, 7.5)),
        shell(circle(10.5, 10, 3)),
        shell(poly([(14, 16.5), (20.5, 16.5), (20.5, 21.5), (17.5, 20), (14.5, 21.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("electrical-tape", CAT, "Short wide roll of tape seen at an angle with a large hole in the middle",
      tags=["insulation tape", "vinyl tape", "wiring", "electrician", "black tape", "adhesive", "cable"])
def _(S):
    return [
        shell("M3 8.5v6a9 4.5 0 0 0 18 0v-6"),
        shell(ellipse(12, 8.5, 9, 4.5)),
        detail(ellipse(12, 8.5, *L(S, (4.5, 2), (4, 2.3)))),
    ]


@icon("thread-seal-tape", CAT, "Small spool of narrow thin tape wound on a core, with a short free end",
      tags=["ptfe tape", "plumber tape", "teflon tape", "pipe thread", "sealing", "plumbing", "leak"])
def _(S):
    return [
        shell(circle(10.5, 10.5, 7.5)),
        shell(circle(10.5, 10.5, 3)),
        line("M10.5 18q0 3.5 4 3.5h6"),
    ]


@icon("glue-bottle", CAT, "Squeeze glue bottle with a pointed nozzle cap and a label band",
      tags=["adhesive", "craft glue", "school glue", "pva", "stick", "paste", "bond"])
def _(S):
    return [
        shell(poly([(10, 9), (12, 3.5), (14, 9)], closed=True, r=S.r * 0.4)),
        shell(poly([(9.5, 9), (14.5, 9), (17.5, 12), (17.5, 21.5), (6.5, 21.5), (6.5, 12)], closed=True, r=S.r)),
        detail(seg(6.5, 14, 17.5, 14)),
        detail(seg(6.5, 18, 17.5, 18)),
    ]


@icon("super-glue-tube", CAT, "Small crimped glue tube with a long needle nozzle and a cap ring",
      tags=["cyanoacrylate", "instant glue", "adhesive", "repair", "bond", "fix", "craft"])
def _(S):
    return [
        line(seg(12, 1.5, 12, 8)),
        shell(poly([(10, 8), (14, 8), (16.5, 11), (17, 19.5), (7, 19.5), (7.5, 11)], closed=True, r=S.r)),
        detail(seg(7.5, 11.5, 16.5, 11.5)),
        line(seg(7, 21.5, 17, 21.5)),
    ]


@icon("epoxy-syringe", CAT, "Double barrel syringe with two parallel tubes, one plunger bar and a joined nozzle",
      tags=["two part epoxy", "adhesive", "resin", "glue", "mixing", "repair", "dual cartridge"])
def _(S):
    return [
        shell(rect(5, 6.5, 5.5, 11, rr(S, 1.5))),
        shell(rect(13.5, 6.5, 5.5, 11, rr(S, 1.5))),
        line(seg(7.75, 3, 7.75, 6.5)),
        line(seg(16.25, 3, 16.25, 6.5)),
        line(seg(5, 3, 19, 3)),
        line(poly([(7.75, 17.5), (7.75, 19), (11.5, 21.5)], r=0)),
        line(poly([(16.25, 17.5), (16.25, 19), (12.5, 21.5)], r=0)),
    ]


@icon("caulk-tube", CAT, "Sealant cartridge with a label band, a piston end and a truncated cone nozzle",
      tags=["caulking", "silicone", "sealant", "cartridge", "bathroom", "gap filler", "sealing"])
def _(S):
    return [
        shell(rect(2.5, 7.5, 13, 9, rr(S, 2.5))),
        detail(seg(6.5, 7.5, 6.5, 16.5)),
        shell(poly([(15.5, 9), (20.5, 10.75), (20.5, 13.25), (15.5, 15)], closed=True, r=S.r * 0.4)),
        line(seg(20.5, 12, 22, 12)),
    ]


@icon("spray-foam-can", CAT, "Aerosol can with a bent straw applicator and a puff of foam",
      tags=["expanding foam", "insulation", "gap filler", "aerosol", "sealant", "construction", "insulating foam"])
def _(S):
    return [
        shell(rect(5.5, 8.5, 9, 13, rr(S, 2.5))),
        shell(rect(8, 5, 4, 3.5, rr(S, 1))),
        line(poly([(10, 5), (10, 2.5), (17, 2.5)], r=S.r)),
        solid(circle(19.5, 3.5, 2)),
        solid(circle(20.25, 7.75, 1.25)),
        detail(seg(5.5, 14, 14.5, 14)),
    ]


@icon("wood-filler", CAT, "Open tub of filler with a putty knife resting against it",
      tags=["putty", "wood putty", "repair", "patching", "spackle", "restoration", "diy"])
def _(S):
    return [
        shell(rect(2.5, 12, 13, 9, rr(S, 2.5))),
        detail(seg(2.5, 15.5, 15.5, 15.5)),
        shell(poly([(11, 9), (19.5, 3), (22, 6), (14.5, 11.5)], closed=True, r=S.r * 0.5)),
    ]


# ============================================================================ pipes, fittings and valves

def _pipe_end_ellipse_d(cx, cy, rx, ry):
    return f"M{fmt(cx - rx)} {fmt(cy)}A{fmt(rx)} {fmt(ry)} 0 1 0 {fmt(cx + rx)} {fmt(cy)}A{fmt(rx)} {fmt(ry)} 0 1 0 {fmt(cx - rx)} {fmt(cy)}Z"


@icon("pipe-section", CAT, "Short length of pipe in perspective with an open round end",
      tags=["tube", "plumbing", "conduit", "pvc", "cylinder", "hollow", "pipework"])
def _(S):
    return [
        shell(ellipse(7, 12, *L(S, (3.5, 7.5), (4.25, 7.5)))),
        line(seg(7, 4.5, 17.5, 4.5)),
        line(seg(7, 19.5, 17.5, 19.5)),
        line("M17.5 4.5a3.75 7.5 0 0 1 0 15"),
        mark(ellipse(7, 12, 0.9, 3.5)),
    ]


@icon("pipe-elbow", CAT, "Ninety degree pipe elbow with a socket ring at each open end",
      tags=["plumbing", "fitting", "bend", "corner", "pvc", "pipework", "joint"])
def _(S):
    return [
        shell(poly([(7, 3), (14, 3), (14, 11), (21.5, 11), (21.5, 18), (7, 18)], closed=True, r=S.r)),
        detail(seg(7, 6.5, 14, 6.5)),
        detail(seg(17.5, 11, 17.5, 18)),
    ]


@icon("pipe-tee", CAT, "T shaped pipe fitting with three open socket ends",
      tags=["plumbing", "fitting", "branch", "junction", "three way", "pvc", "joint"])
def _(S):
    return [
        shell(poly([(2.5, 3.5), (21.5, 3.5), (21.5, 10.5), (15, 10.5), (15, 21), (9, 21), (9, 10.5), (2.5, 10.5)],
                   closed=True, r=S.r)),
        detail(seg(6.5, 3.5, 6.5, 10.5)),
        detail(seg(17.5, 3.5, 17.5, 10.5)),
        detail(seg(9, 17, 15, 17)),
    ]


@icon("pipe-coupling", CAT, "Short sleeve joining two pipe ends in a straight line",
      tags=["plumbing", "fitting", "connector", "joiner", "pvc", "pipework", "repair"])
def _(S):
    return [
        shell(rect(6.5, 5.5, 11, 13, rr(S, 3))),
        detail(seg(12, 5.5, 12, 18.5)),
        line(seg(2, 9, 6.5, 9)),
        line(seg(2, 15, 6.5, 15)),
        line(seg(17.5, 9, 22, 9)),
        line(seg(17.5, 15, 22, 15)),
    ]


@icon("pipe-reducer", CAT, "Fitting that steps from a wide pipe opening down to a narrow one",
      tags=["plumbing", "fitting", "adapter", "reducing coupling", "taper", "pvc", "pipework"])
def _(S):
    return [
        shell(poly([(2.5, 4.5), (9, 4.5), (15, 9), (21.5, 9), (21.5, 15), (15, 15), (9, 19.5), (2.5, 19.5)],
                   closed=True, r=S.r)),
        detail(seg(6, 4.5, 6, 19.5)),
        detail(seg(18.5, 9, 18.5, 15)),
    ]


@icon("pipe-union", CAT, "Pipe union: a hex nut collar between two threaded ends",
      tags=["plumbing", "fitting", "nut", "connector", "disconnect", "threaded", "pipework"])
def _(S):
    return [
        shell(rect(8, 5, 8, 14, rr(S, 3.5))),
        detail(seg(8, 9.5, 16, 9.5)),
        detail(seg(8, 14.5, 16, 14.5)),
        shell(rect(2.5, 8, 5.5, 8, rr(S, 2.75))),
        shell(rect(16, 8, 5.5, 8, rr(S, 2.75))),
    ]


@icon("pipe-flange", CAT, "Round flange plate with a ring of bolt holes and a pipe opening in the centre",
      tags=["plumbing", "fitting", "bolted joint", "disc", "industrial", "pipework", "connection"])
def _(S):
    holes = []
    for i in range(6):
        x, y = polar(12, 12, 6.6, i * 60 + 30)
        holes.append(mark(circle(x, y, 0.95)) if S.name == "rounded" else mark(rect(x - 0.85, y - 0.85, 1.7, 1.7)))
    return [shell(circle(12, 12, 9.5)), shell(circle(12, 12, 3.75))] + holes


@icon("pipe-cap", CAT, "Socket pipe cap with a rounded closed end",
      tags=["plumbing", "fitting", "end cap", "plug", "seal", "pvc", "pipework"])
def _(S):
    body = union(rect(2.5, 6, 11, 12, rr(S, 3)), circle(13.5, 12, 6))
    return [shell(body), detail(seg(7, 6, 7, 18))]


@icon("ball-valve", CAT, "Straight pipe valve with a round body and a flat lever handle on top",
      tags=["shutoff valve", "plumbing", "tap", "water", "control", "stopcock", "lever"])
def _(S):
    return [
        shell(circle(12, 14, 6)),
        shell(rect(2.5, 11, 5, 6, rr(S, 1.5))),
        shell(rect(16.5, 11, 5, 6, rr(S, 1.5))),
        line(seg(12, 8, 12, 5)),
        line(poly([(5, 5), (19, 5)], r=0)),
    ]


@icon("gate-valve", CAT, "Gate valve with a tall bonnet, a stem and a handwheel on top",
      tags=["plumbing", "shutoff valve", "water main", "industrial", "wheel valve", "control", "pipe"])
def _(S):
    return [
        shell(rect(8.5, 11, 7, 9.5, rr(S, 3.5))),
        shell(rect(2.5, 13.5, 6, 5, rr(S, 2.5))),
        shell(rect(15.5, 13.5, 6, 5, rr(S, 2.5))),
        line(seg(12, 11, 12, 5)),
        line(seg(6.5, 4, 17.5, 4)),
        solid(circle(6.5, 4, 1.25)),
        solid(circle(17.5, 4, 1.25)),
    ]


@icon("check-valve", CAT, "Pipe valve body with an arrow inside showing the single flow direction",
      tags=["non return valve", "one way valve", "plumbing", "backflow", "pipe", "flow direction", "water"])
def _(S):
    return [
        shell(rect(6, 6, 12, 12, rr(S, 3))),
        shell(rect(2.5, 9.5, 3.5, 5, rr(S, 1))),
        shell(rect(18, 9.5, 3.5, 5, rr(S, 1))),
        detail(seg(8.75, 12, 14.5, 12)),
        detail(poly([(12.25, 9.25), (15, 12), (12.25, 14.75)], r=S.r * 0.3)),
    ]


@icon("butterfly-valve", CAT, "Round wafer valve body with a disc on a stem and a lever on top",
      tags=["plumbing", "industrial valve", "flow control", "disc valve", "pipe", "lever", "hvac"])
def _(S):
    return [
        shell(circle(11, 13, 8)),
        detail(ellipse(11, 13, 2.25, 5)),
        line(seg(11, 5, 11, 2.5)),
        line(poly([(17, 7.5), (21.5, 3)], r=0)),
    ]


@icon("angle-stop-valve", CAT, "Small right angle shutoff valve with an oval handle, fed by a pipe from the wall",
      tags=["angle valve", "supply stop", "sink", "toilet", "plumbing", "shutoff", "isolation valve"])
def _(S):
    return [
        line(seg(2.5, 5, 2.5, 19)),
        shell(rect(2.5, 11, 8.5, 5, rr(S, 2.5))),
        shell(rect(10.5, 8.5, 7, 9, rr(S, 3))),
        shell(rect(11.75, 17.5, 4.5, 4, rr(S, 1.5))),
        line(seg(14, 8.5, 14, 6)),
        shell(ellipse(14, 4, 4.5, 2)),
    ]


@icon("pressure-relief-valve", CAT, "Relief valve with a spring bonnet, a lifting lever and a side outlet pipe",
      tags=["safety valve", "boiler", "water heater", "pressure", "plumbing", "release", "overpressure"])
def _(S):
    return [
        shell(rect(5.5, 12.5, 10, 8.5, rr(S, 3))),
        shell(rect(7.5, 5.5, 6, 7, rr(S, 2))),
        line(seg(13.5, 7.5, 20.5, 3.5)),
        shell(rect(15.5, 14.5, 6, 4.5, rr(S, 2))),
        detail(seg(7.5, 9, 13.5, 9)),
    ]


@icon("outdoor-spigot", CAT, "Wall mounted hose tap with a wheel handle on top and a threaded spout pointing down",
      tags=["hose bib", "garden tap", "faucet", "outside tap", "water", "hosepipe", "bibcock"])
def _(S):
    return [
        line(seg(2.5, 4, 2.5, 20)),
        shell(rect(2.5, 9.5, 11, 4.5, rr(S, 2.25))),
        shell(rect(9.5, 14, 6, 7, rr(S, 2))),
        detail(seg(9.5, 17.5, 15.5, 17.5)),
        line(seg(7.5, 9.5, 7.5, 6)),
        line(seg(3.5, 5, 11.5, 5)),
    ]


@icon("expansion-tank", CAT, "Small round bellied tank with a short pipe stub on top",
      tags=["water heater", "boiler", "pressure tank", "heating", "plumbing", "hvac", "vessel"])
def _(S):
    return [
        shell(rect(9.5, 2.5, 5, 5, rr(S, 2.5))),
        shell(ellipse(12, 14.5, 8.5, 7)),
        detail(poly([(4, 14.5), (20, 14.5)], r=0)),
    ]


@icon("manhole-cover", CAT, "Round cover with a grid of raised ridges and two small lift holes",
      tags=["drain cover", "sewer", "street", "utility", "inspection cover", "cast iron", "road"])
def _(S):
    holes = [mark(circle(10.25, 12, 0.9)), mark(circle(13.75, 12, 0.9))] if S.name == "rounded" else \
        [mark(rect(9.4, 11.15, 1.7, 1.7)), mark(rect(12.9, 11.15, 1.7, 1.7))]
    return [
        shell(circle(12, 12, 9.5)),
        detail(seg(3.2, 8.25, 20.8, 8.25)),
        detail(seg(3.2, 15.75, 20.8, 15.75)),
        detail(seg(8.25, 3.2, 8.25, 20.8)),
        detail(seg(15.75, 3.2, 15.75, 20.8)),
    ] + holes


@icon("water-filter-cartridge", CAT, "Tall pleated filter cartridge with a neck on top",
      tags=["filter", "water", "purifier", "replacement", "drinking water", "sediment", "housing"])
def _(S):
    return [
        shell(rect(8.5, 2.5, 7, 3.5, rr(S, 1.5))),
        shell(rect(5.5, 6, 13, 15.5, rr(S, 3))),
        detail(seg(9.5, 9.5, 9.5, 18.5)),
        detail(seg(12, 9.5, 12, 18.5)),
        detail(seg(14.5, 9.5, 14.5, 18.5)),
    ]


@icon("fire-sprinkler-head", CAT, "Ceiling sprinkler head with a glass bulb, two frame arms and a round deflector below",
      tags=["sprinkler", "fire safety", "suppression", "ceiling", "building", "water", "alarm"])
def _(S):
    return [
        line(seg(2.5, 2.5, 21.5, 2.5)),
        shell(rect(9.5, 2.5, 5, 4.5, rr(S, 1.5))),
        line(poly([(9.75, 7), (7.5, 14)], r=0)),
        line(poly([(14.25, 7), (16.5, 14)], r=0)),
        solid(ellipse(12, 10.5, 1.5, 2.75)),
        shell(rect(5.5, 14, 13, 3, rr(S, 1.5))),
        dot(8, 20.5, 0.9), dot(12, 21, 0.9), dot(16, 20.5, 0.9),
    ]


@icon("backflow-preventer", CAT, "Horizontal pipe assembly with valve bodies at each end, a chamber with test ports and a drain below",
      tags=["cross connection", "plumbing", "irrigation", "water supply", "check valve assembly", "safety", "pipework"])
def _(S):
    return [
        shell(rect(2.5, 10.5, 5, 7, rr(S, 2.5))),
        shell(rect(16.5, 10.5, 5, 7, rr(S, 2.5))),
        shell(rect(7.5, 8.5, 9, 11, rr(S, 3))),
        line(seg(10, 8.5, 10, 4.5)),
        line(seg(14, 8.5, 14, 4.5)),
        solid(circle(10, 3.75, 1.25)),
        solid(circle(14, 3.75, 1.25)),
        line(seg(12, 19.5, 12, 22)),
    ]


@icon("pipe-insulation", CAT, "Foam tube cut along its length wrapped around a pipe that sticks out of the end",
      tags=["pipe lagging", "foam sleeve", "thermal", "heating", "plumbing", "frost protection", "energy saving"])
def _(S):
    return [
        shell(ellipse(7, 12, 3.5, 7.5)),
        line(seg(7, 4.5, 16, 4.5)),
        line(seg(7, 19.5, 16, 19.5)),
        line("M16 4.5a3.5 7.5 0 0 1 0 15"),
        line(seg(16.5, 12, 22, 12)),
        detail(seg(7, 9, 14.5, 9)),
    ]


# ============================================================================ electrical supplies

@icon("wire-spool", CAT, "Cable reel seen from the side: two flanges with wire wound between them",
      tags=["cable drum", "copper wire", "electrician", "reel", "cable", "coil", "supplies"])
def _(S):
    return [
        shell(rect(3, 3.5, 3.5, 17, L(S, 0.5, 1.75))),
        shell(rect(17.5, 3.5, 3.5, 17, L(S, 0.5, 1.75))),
        shell(rect(6.5, 7, 11, 10, L(S, 0, 1.5))),
        detail(seg(9, 7, 11, 17)),
        detail(seg(13, 7, 15, 17)),
    ]


@icon("cord-reel", CAT, "Extension cord reel: a round drum with cable wound on it, a crank arm and a stand",
      tags=["extension cord", "power cable", "hose reel", "workshop", "garage", "electrician", "winder"])
def _(S):
    return [
        shell(circle(12, 10, 7.5)),
        detail(circle(12, 10, 4)),
        dot(12, 10, 1),
        line(poly([(19.5, 10), (21.5, 10), (21.5, 13.5)], r=S.r * 0.5)),
        line(poly([(5, 21.5), (5, 19), (19, 19), (19, 21.5)], r=S.r * 0.5)),
    ]


@icon("wire-nut", CAT, "Cone shaped twist on wire connector with ridges and two wires entering the base",
      tags=["wire connector", "electrical", "splice", "electrician", "wiring", "twist on", "joint"])
def _(S):
    return [
        shell(poly([(9.5, 3.5), (14.5, 3.5), (18, 18), (6, 18)], closed=True, r=S.r)),
        detail(seg(8.6, 8.5, 15.4, 8.5)),
        detail(seg(7.6, 13, 16.4, 13)),
        line(seg(9.5, 18, 9.5, 21.5)),
        line(seg(14.5, 18, 14.5, 21.5)),
    ]


@icon("breaker-panel", CAT, "Electrical panel box with two columns of small breaker switches",
      tags=["circuit breaker box", "fuse box", "distribution board", "consumer unit", "electrical", "mains", "switchboard"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, rr(S, 2.5))),
        detail(seg(12, 5.5, 12, 18.5)),
        mark(rect(6.5, 5.75, 3, 3, 0.5)), mark(rect(6.5, 10.5, 3, 3, 0.5)), mark(rect(6.5, 15.25, 3, 3, 0.5)),
        mark(rect(14.5, 5.75, 3, 3, 0.5)), mark(rect(14.5, 10.5, 3, 3, 0.5)), mark(rect(14.5, 15.25, 3, 3, 0.5)),
    ]


@icon("cartridge-fuse", CAT, "Glass cartridge fuse with a metal cap on each end and a thin wire inside",
      tags=["fuse", "glass fuse", "electrical protection", "overcurrent", "appliance", "electronics", "circuit"])
def _(S):
    return [
        shell(rect(6, 8, 12, 8, rr(S, 2))),
        shell(rect(2.5, 7, 4, 10, rr(S, 1.75))),
        shell(rect(17.5, 7, 4, 10, rr(S, 1.75))),
        detail(poly([(8, 12), (10, 10.5), (14, 13.5), (16, 12)], r=0)),
    ]


@icon("blade-fuse", CAT, "Flat plastic blade fuse with two metal prongs and a small window showing the wire",
      tags=["car fuse", "automotive fuse", "electrical protection", "circuit", "vehicle", "spare", "overcurrent"])
def _(S):
    return [
        shell(poly([(5, 14), (5, 5.5), (7.5, 3), (16.5, 3), (19, 5.5), (19, 14)], closed=True, r=S.r)),
        detail(poly([(9, 6), (9, 9.5), (15, 9.5), (15, 6)], r=0)),
        line(seg(8.5, 14, 8.5, 21.5)),
        line(seg(15.5, 14, 15.5, 21.5)),
    ]


@icon("electrical-conduit", CAT, "Rigid conduit tube with a coupling ring and a smooth sweeping bend up at one end",
      tags=["cable tube", "wiring", "electrician", "emt", "raceway", "pipe", "construction"])
def _(S):
    return [
        shell("M2.5 15.5H13a4 4 0 0 0 4-4V3.5H21V11.5A8 8 0 0 1 13 19.5H2.5Z"),
        detail(seg(8, 15.5, 8, 19.5)),
        detail(seg(17, 7, 21, 7)),
    ]
