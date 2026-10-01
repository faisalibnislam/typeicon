"""TypeIcon Core: emergency (batch 003).

Safety, rescue, hazard and relief scenes, equipment, buildings and people, drawn from the objects themselves.
Closed silhouettes are shells, inner lines are details, small solid marks stay solid in Line/Rounded and are
knocked out of Filled shells. Figures follow the stick-figure style of sets/activities_002.py.
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


def mark(d):
    return Part("dot", d)


def rotd(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpts(pts, deg, dx=0.0, dy=0.0, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s + dx, cy + (x - cx) * s + (y - cy) * c + dy) for x, y in pts]


def rr(S, cap):
    return min(S.R, cap)


def head(x, y, r=2.25):
    return dot(x, y, r)


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


def bolt(S, x, y, s=1.0):
    """Lightning bolt polygon with its top-left at (x, y), about 6s wide and 9s tall."""
    pts = [(x + 4 * s, y), (x, y + 5 * s), (x + 3 * s, y + 5 * s), (x + 1.5 * s, y + 9 * s),
           (x + 6 * s, y + 3.5 * s), (x + 3 * s, y + 3.5 * s)]
    return poly(pts, closed=True, r=S.r * 0.3)


# ============================================================================ chunk 1

@icon("gas-suppression-system", CAT, "Two tall gas cylinders joined by a manifold pipe to a discharge nozzle spraying gas",
      tags=["clean agent", "fire suppression", "gas cylinders", "server room fire", "nozzle", "extinguishing system"])
def _(S):
    k = rr(S, 3)
    return [
        line(poly([(5, 11), (5, 4.5), (19, 4.5), (19, 9.5)])),
        line(seg(12, 11, 12, 4.5)),
        shell(rect(2.5, 11, 5, 10, k)),
        shell(rect(9.5, 11, 5, 10, k)),
        shell(poly([(16.5, 9.5), (21.5, 9.5), (19, 14)], closed=True, r=S.r * 0.3)),
        line(seg(17.3, 17, 17.3, 20.5)), line(seg(20.7, 17, 20.7, 20.5)),
    ]


@icon("flame-detector", CAT, "Wall detector box with a round sensing lens above a small flame",
      tags=["fire sensor", "uv detector", "optical flame", "fire detection", "alarm", "industrial safety"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, S.R)),
        detail(circle(12, 8.5, 2.75)),
        mark(flame(12, 13.5, 19, 4.5, S)),
    ]


@icon("defensible-space", CAT, "House in the middle with cleared ground on both sides, trees far off and a distance arrow below",
      tags=["wildfire", "fire break", "clearance", "home protection", "cleared zone", "brush clearing"])
def _(S):
    return [
        shell(poly([(8, 16), (8, 11.5), (12, 7.5), (16, 11.5), (16, 16)], closed=True, r=S.r * 0.6)),
        shell(circle(3.8, 8.5, 2.2)), line(seg(3.8, 10.7, 3.8, 16)),
        shell(circle(20.2, 8.5, 2.2)), line(seg(20.2, 10.7, 20.2, 16)),
        line(seg(6, 20.5, 18, 20.5)),
        line(poly([(8, 19), (6, 20.5), (8, 22)])), line(poly([(16, 19), (18, 20.5), (16, 22)])),
    ]


@icon("cat-in-tree-rescue", CAT, "Ladder leaning against a tree with a cat sitting on a branch near the top",
      tags=["cat stuck in tree", "animal rescue", "fire department", "ladder", "pet rescue", "kitten"])
def _(S):
    return [
        line(seg(2.5, 22, 5.5, 10)), line(seg(7.5, 22, 10.5, 10)),
        line(seg(3.7, 17, 9.3, 17)), line(seg(4.6, 13.5, 9.6, 13.5)),
        line(seg(16.5, 14, 16.5, 22)),
        shell(circle(16.5, 8, 6)),
        head(16.5, 6.3, 1.5),
        mark(poly([(15, 5.3), (15.2, 3.4), (16.4, 4.6)], closed=True)),
        mark(poly([(17.6, 4.6), (17.8, 3.4), (18, 5.3)], closed=True)),
        mark(ellipse(16.5, 9.6, 2.3, 1.4)),
    ]


@icon("checking-breathing", CAT, "Rescuer leaning over a person lying down with cheek near the mouth and breath lines between",
      tags=["look listen feel", "first aid", "unresponsive", "airway", "cpr check", "breathing check"])
def _(S):
    return [
        head(19, 18.5),
        line(poly([(15.5, 18.5), (2.5, 18.5)], r=S.r)),
        head(14, 7.5),
        line(poly([(11.5, 9), (6.5, 8.5), (3, 13)], r=S.r)),
        line(seg(18.5, 11, 22, 11)),
        line(seg(18.5, 14.5, 21.5, 14.5)),
    ]


@icon("two-person-seat-carry", CAT, "Two rescuers with linked hands forming a seat that carries a seated person between them",
      tags=["four hand seat", "human chair", "casualty carry", "injured person", "first aid", "rescue"])
def _(S):
    return [
        head(12, 4.5),
        line(poly([(12, 7.5), (12, 14)], r=S.r)),
        head(3.5, 6.5),
        line(seg(3.5, 9.5, 3.5, 21)),
        line(poly([(3.5, 14.5), (8, 17.5), (16, 17.5), (20.5, 14.5)], r=S.r)),
        head(20.5, 6.5),
        line(seg(20.5, 9.5, 20.5, 21)),
    ]


@icon("rescue-drag", CAT, "Rescuer walking backwards and pulling a person who lies on the ground by the shoulders",
      tags=["drag carry", "casualty drag", "move injured", "emergency rescue", "first aid", "pull to safety"])
def _(S):
    return [
        head(5, 5.5),
        line(poly([(6.5, 8.5), (9, 14), (6, 21)], r=S.r)),
        line(poly([(9, 14), (12.5, 21)], r=S.r)),
        line(poly([(7.5, 10), (12, 13), (14.5, 15.5)], r=S.r)),
        head(16, 16),
        line(poly([(18.5, 18), (22, 19.5)], r=S.r)),
    ]


@icon("window-escape", CAT, "Person climbing out through an open window and stepping over the sill",
      tags=["fire escape", "exit through window", "evacuation", "emergency exit", "egress", "climb out"])
def _(S):
    return [
        shell(rect(2.5, 3, 10, 14, rr(S, 2))),
        detail(seg(7.5, 3, 7.5, 17)),
        line(seg(2.5, 19.5, 13, 19.5)),
        head(19, 6),
        line(poly([(18.5, 9), (16.5, 14.5)], r=S.r)),
        line(poly([(16.5, 14.5), (10.5, 13)], r=S.r)),
        line(poly([(16.5, 14.5), (18.5, 21)], r=S.r)),
        line(poly([(18, 10.5), (21.5, 13)], r=S.r)),
    ]


@icon("lightning-safety-position", CAT, "Person crouched low on the balls of the feet with hands over the ears under a lightning bolt",
      tags=["thunderstorm", "lightning crouch", "storm safety", "take cover", "outdoor safety", "thunder"])
def _(S):
    return [
        shell(bolt(S, 13.5, 1.5, 1.3)),
        head(9, 11),
        line(poly([(5.5, 15), (5.5, 10), (7, 8.5)], r=S.r * 0.5)),
        line(poly([(12.5, 15), (12.5, 10), (11, 8.5)], r=S.r * 0.5)),
        line(poly([(6, 21), (6, 18), (9, 14.5), (12, 18), (12, 21)], r=S.r)),
    ]


@icon("incident-command-post", CAT, "Small tent with a flag on top and a radio antenna standing beside it",
      tags=["command tent", "field headquarters", "emergency operations", "incident commander", "tent", "coordination"])
def _(S):
    return [
        shell(poly([(2.5, 20), (8.5, 9.5), (14.5, 20)], closed=True, r=S.r * 0.4)),
        detail(seg(8.5, 20, 8.5, 15)),
        line(seg(8.5, 9.5, 8.5, 2.5)),
        solid(poly([(8.5, 2.5), (13, 4.25), (8.5, 6)], closed=True)),
        line(seg(19, 9, 19, 20)),
        dot(19, 6.5, 1.5),
        line("M16 4.3C15 5.6 15 7.4 16 8.7"),
        line("M22 4.3C23 5.6 23 7.4 22 8.7"),
    ]


@icon("hazard-map", CAT, "Folded map with a shaded danger zone on one panel and a warning triangle on another",
      tags=["risk map", "danger zone", "hazard zones", "evacuation planning", "flood map", "warning"])
def _(S):
    return [
        shell(poly([(2, 6), (8, 4), (16, 6), (22, 4), (22, 18), (16, 20), (8, 18), (2, 20)], closed=True, r=S.r * 0.5)),
        detail(seg(8, 4, 8, 18)), detail(seg(16, 6, 16, 20)),
        mark(circle(12, 13, 2.25)),
        mark(poly([(19, 8.5), (20.6, 12), (17.4, 12)], closed=True)),
    ]


@icon("family-emergency-plan", CAT, "Clipboard with a small house at the top and lines of a checklist below",
      tags=["emergency plan", "preparedness", "meeting point", "home safety", "checklist", "disaster plan"])
def _(S):
    return [
        shell(rect(4, 4, 16, 18, rr(S, 3))),
        shell(rect(9, 2, 6, 4, rr(S, 1.5))),
        mark(poly([(12, 8), (16.5, 12), (15, 12), (15, 14.5), (9, 14.5), (9, 12), (7.5, 12)], closed=True)),
        detail(seg(8, 17.5, 16, 17.5)),
    ]


@icon("search-party", CAT, "Three people walking side by side in a search line, one shining a flashlight beam ahead",
      tags=["missing person", "ground search", "volunteers", "search and rescue", "flashlight", "line search"])
def _(S):
    def fig(x):
        return [head(x, 6, 2),
                line(seg(x, 9, x, 14)),
                line(poly([(x - 2, 21), (x, 14), (x + 2, 21)], r=S.r))]
    return fig(4) + fig(12) + fig(20)


@icon("search-pattern-map", CAT, "Map square with a zigzag sweep path that begins at a solid start dot",
      tags=["grid search", "search and rescue", "sweep pattern", "route plan", "missing person", "area search"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(poly([(7.5, 7.5), (16.5, 7.5), (16.5, 12), (7.5, 12), (7.5, 16.5), (16.5, 16.5)], r=S.r)),
        mark(circle(7.5, 7.5, 2.0)),
    ]


# ============================================================================ chunk 2

@icon("patrol-route", CAT, "Map square with a loop route and solid checkpoint dots along it",
      tags=["security round", "guard tour", "checkpoints", "route", "rounds", "patrol map"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(poly([(12, 8), (17.5, 16), (6.5, 16)], closed=True, r=S.r * 0.5)),
        mark(circle(12, 8, 2)), mark(circle(17.5, 16, 2)), mark(circle(6.5, 16, 2)),
    ]


@icon("security-desk", CAT, "Reception counter with a monitor on top and a guard cap sitting beside it",
      tags=["guard station", "front desk", "security guard", "lobby", "surveillance", "reception"])
def _(S):
    return [
        shell(rect(2.5, 14, 19, 7.5, rr(S, 2.5))),
        shell(rect(3.5, 3, 9, 7, rr(S, 1.5))),
        line(seg(8, 10, 8, 14)),
        shell("M15.5 11C15.5 6.5 21 6.5 21 11Z"),
        line(seg(14, 11.5, 22, 11.5)),
    ]


@icon("emergency-supplies-shelf", CAT, "Shelf unit stocked with a water jug, cans, a flashlight and a first-aid box",
      tags=["preparedness", "disaster kit", "stockpile", "water and food", "storage", "survival supplies"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, S.R)),
        detail(seg(2.5, 12, 21.5, 12)),
        mark(rect(5.5, 5, 4, 5, 1)),
        mark(rect(11, 6.5, 3.5, 3.5, 0.5)),
        mark(rect(16, 6.5, 2.5, 3.5, 0.5)),
        mark(rect(5.5, 14.5, 6, 5, 1)),
        mark(rect(14, 16, 5, 3, 1)),
    ]


@icon("taped-window", CAT, "Window with two strips of tape crossed over the panes and a sill below",
      tags=["storm prep", "hurricane", "window protection", "shatter", "boarded", "tape x"])
def _(S):
    return [
        shell(rect(4, 3, 16, 14, rr(S, 2))),
        detail(seg(6, 5, 18, 15)), detail(seg(18, 5, 6, 15)),
        line(seg(2.5, 20.5, 21.5, 20.5)),
    ]


@icon("tsunami-evacuation-tower", CAT, "Tall raised platform on two legs with a flight of stairs climbing up to it",
      tags=["vertical evacuation", "tsunami", "refuge", "high ground", "coast", "platform"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 4.5, rr(S, 2))),
        line(seg(4.5, 8, 4.5, 21.5)), line(seg(19.5, 8, 19.5, 21.5)),
        line(poly([(7.5, 21.5), (7.5, 18), (10.5, 18), (10.5, 15), (13.5, 15), (13.5, 12), (16.5, 12), (16.5, 8)], r=S.r * 0.5)),
    ]


@icon("flood-barrier-panels", CAT, "Stack of barrier panels slotted between two posts holding back a wavy water line",
      tags=["flood defense", "flood wall", "stop logs", "water barrier", "flood protection", "demountable"])
def _(S):
    return [
        shell(rect(2.5, 9, 3.5, 12.5, rr(S, 1.5))),
        shell(rect(18, 9, 3.5, 12.5, rr(S, 1.5))),
        shell(rect(6, 12, 12, 9.5, rr(S, 1.5))),
        detail(seg(6, 16.75, 18, 16.75)),
        line("M3 5.5C5.5 3 8 3 10.5 5.5S15.5 8 18 5.5"),
    ]


@icon("high-water-mark", CAT, "Wall plaque with a wave line marking a flood level, an arrow pointing to it and a date line",
      tags=["flood level", "flood marker", "water level", "historic flood", "flood height", "plaque"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, S.R)),
        detail("M6 9.5C7.5 7.5 9 7.5 10.5 9.5S13.5 11.5 15 9.5"),
        detail(poly([(18, 6), (18, 12)])),
        detail(seg(6.5, 16.5, 17.5, 16.5)),
    ]


@icon("seismic-bracing", CAT, "Building frame with crossed diagonal braces filling each of its two bays",
      tags=["earthquake", "structural brace", "shear brace", "retrofit", "steel frame", "quake-proofing"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 2.5))),
        detail(seg(3, 12, 21, 12)),
        detail(seg(3, 2.5, 21, 12)), detail(seg(21, 2.5, 3, 12)),
        detail(seg(3, 12, 21, 21.5)), detail(seg(21, 12, 3, 21.5)),
    ]


def _civic(S):
    return shell(poly([(2.5, 21.5), (2.5, 9.5), (12, 2.5), (21.5, 9.5), (21.5, 21.5)], closed=True, r=S.r * 0.6))


@icon("cooling-center", CAT, "Public building with a large snowflake over its door",
      tags=["heat relief", "heat wave", "air conditioned shelter", "hot weather", "snowflake", "community shelter"])
def _(S):
    return [
        _civic(S),
        detail(seg(12, 11, 12, 18.5)), detail(seg(8.6, 12.75, 15.4, 16.75)), detail(seg(15.4, 12.75, 8.6, 16.75)),
    ]


@icon("warming-center", CAT, "Public building with three wavy heat lines rising above a radiator bar",
      tags=["cold relief", "cold snap", "heated shelter", "winter", "radiator", "community shelter"])
def _(S):
    return [
        _civic(S),
        detail("M8.5 14.5C7.5 13 9.5 12 8.5 10.5"),
        detail("M12 14.5C11 13 13 12 12 10.5"),
        detail("M15.5 14.5C14.5 13 16.5 12 15.5 10.5"),
        detail(seg(7, 18, 17, 18)),
    ]


@icon("dam-breach", CAT, "Dam wall broken into two blocks with water gushing through the gap",
      tags=["dam failure", "flood wave", "burst", "reservoir", "catastrophe", "water release"])
def _(S):
    return [
        shell(rect(2.5, 3, 8, 9, rr(S, 2))),
        shell(rect(13.5, 3, 8, 9, rr(S, 2))),
        line(seg(12, 6, 12, 21.5)),
        line("M10 14C10 17.5 8.5 19 6.5 21.5"),
        line("M14 14C14 17.5 15.5 19 17.5 21.5"),
    ]


@icon("shark-barrier-net", CAT, "Net of floats and mesh hanging across a bay with a shark fin on the outer side",
      tags=["beach safety", "shark net", "swimming area", "netting", "ocean", "fin"])
def _(S):
    return [
        shell(rect(2.5, 7, 11, 12, rr(S, 2))),
        detail(seg(8, 7, 8, 19)), detail(seg(2.5, 13, 13.5, 13)),
        dot(5, 4.5, 1.5), dot(11, 4.5, 1.5),
        shell("M16.5 19C17 14 18.5 11 20.5 8.5C20 12 20.5 16 22 19Z"),
    ]


@icon("spill-kit", CAT, "Wheeled bin with a lid, absorbent pads sticking out the top and a drop on the front",
      tags=["chemical spill", "absorbent pads", "hazmat", "cleanup", "oil spill", "containment"])
def _(S):
    return [
        line(poly([(7, 8), (8, 3), (12, 4), (11, 8)], r=S.r * 0.5)),
        line(poly([(13, 8), (13.5, 3.5), (17.5, 3), (17, 8)], r=S.r * 0.5)),
        shell(rect(2.5, 8, 19, 3, rr(S, 1.5))),
        shell(rect(4, 11, 16, 8, rr(S, 2))),
        mark("M12 12.5C13.6 14.5 14.5 15.5 14.5 16.5A2.5 2.5 0 0 1 9.5 16.5C9.5 15.5 10.4 14.5 12 12.5Z"),
        dot(6.5, 21, 1.3), dot(17.5, 21, 1.3),
    ]




# ============================================================================ chunk 3

def thick(d, w, S):
    """Outline of a stroke of width w along d, used as a closed shell (tubes, hoses)."""
    return path_to_d(ST(d, w, "round", "round"))


@icon("two-hand-control-buttons", CAT, "Machine control box with two large round buttons set wide apart",
      tags=["two-hand control", "safety control", "press machine", "operator controls", "palm buttons", "industrial safety"])
def _(S):
    return [
        shell(rect(2.5, 7, 19, 13, rr(S, 3.5))),
        mark(circle(7.5, 13.5, 3.25)), mark(circle(16.5, 13.5, 3.25)),
        line(seg(7.5, 3, 7.5, 7)), line(seg(16.5, 3, 16.5, 7)),
    ]


@icon("emergency-pull-cord", CAT, "Switch box on the left with a taut cord pulled down into a V by a ring handle",
      tags=["pull wire", "trip wire switch", "conveyor safety", "e-stop cord", "rope switch", "machine guard"])
def _(S):
    return [
        shell(rect(2.5, 4, 6, 8, rr(S, 2))),
        mark(circle(5.5, 8, 1.5)),
        line(seg(21.5, 6, 21.5, 12)),
        line(poly([(8.5, 8), (15, 15), (21.5, 8)])),
        shell(circle(15, 18.5, 2.5)),
    ]


@icon("elevator-alarm-button", CAT, "Elevator button panel with a ringed alarm button showing a bell",
      tags=["lift alarm", "call for help", "elevator emergency", "stuck in lift", "panel", "bell button"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 3))),
        mark(rect(8, 5.5, 8, 1.75, 0.5)),
        detail(circle(12, 14, 4.5)),
        mark("M12 11C10.6 11 10 12.2 10 13.6V15.4H14V13.6C14 12.2 13.4 11 12 11Z"),
        mark(circle(12, 16.4, 0.9)),
    ]


@icon("bowline-knot", CAT, "Rope tied in a bowline with a fixed loop at the bottom, a knot collar above and a short tail",
      tags=["rope knot", "rescue knot", "sailing knot", "loop knot", "tying rope", "climbing"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 8)),
        shell(rect(9, 8, 6, 4, rr(S, 1.5))),
        line(seg(15, 9.5, 18.5, 7)),
        line(circle(12, 17, 4.75)),
    ]


@icon("evacuation-sled", CAT, "Padded sled mattress with straps and a pull handle sliding down a staircase",
      tags=["stair sled", "evacuation mattress", "disabled evacuation", "stairwell rescue", "carry down", "mobility"])
def _(S):
    a = math.radians(32)
    c, s = math.cos(a), math.sin(a)

    def R(x, y):
        return (12 + x * c - y * s, 10 + x * s + y * c)
    body = [R(-7.5, -2.25), R(7.5, -2.25), R(7.5, 2.25), R(-7.5, 2.25)]
    return [
        shell(poly(body, closed=True, r=S.r * 0.8)),
        detail(poly([R(-2.5, -2.25), R(-2.5, 2.25)])), detail(poly([R(2.5, -2.25), R(2.5, 2.25)])),
        line(poly([R(-7.5, 0), R(-10, -3)])),
        line(poly([(2, 11), (6, 11), (6, 13.5), (10, 13.5), (10, 16), (14, 16), (14, 18.5), (18, 18.5), (18, 21), (22, 21)], r=S.r * 0.4)),
    ]


@icon("controlled-descent-device", CAT, "Wall-mounted rope reel with a line running down to a person hanging in a harness",
      tags=["rope descender", "rescue descent", "high-rise escape", "abseil", "lowering device", "harness"])
def _(S):
    return [
        line(seg(2.5, 2.5, 21.5, 2.5)),
        shell(circle(12, 7.5, 3.5)),
        mark(circle(12, 7.5, 1.1)),
        line(seg(12, 11, 12, 14.5)),
        head(12, 16.5, 2),
        line(poly([(7.5, 15), (12, 18.5), (16.5, 15)], r=S.r)),
        line(seg(12, 18.5, 12, 22)),
    ]


@icon("escape-chute", CAT, "Tall building with a long fabric tube hanging from a window down to the ground",
      tags=["fire escape chute", "evacuation slide", "building escape", "tube slide", "high-rise escape", "emergency exit"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 9, 19, rr(S, 2))),
        mark(rect(5, 5.5, 3.5, 2.5, 0.5)), mark(rect(5, 10.5, 3.5, 2.5, 0.5)), mark(rect(5, 15.5, 3.5, 2.5, 0.5)),
        shell(poly([(11.5, 4), (14.5, 4), (21.5, 17), (21.5, 21.5), (17.5, 21.5), (11.5, 10)], closed=True, r=S.r * 0.8)),
    ]


@icon("coast-guard-cutter", CAT, "Patrol ship in side view with a bridge, a mast, a diagonal stripe on the hull and a flat rear deck",
      tags=["patrol boat", "coastguard", "rescue ship", "maritime", "vessel", "sea rescue"])
def _(S):
    return [
        line(seg(11, 6.5, 11, 2.5)),
        shell(rect(8, 6.5, 6, 6.5, rr(S, 1.5))),
        shell(poly([(2, 13), (20, 13), (22, 15), (18, 20.5), (4.5, 20.5)], closed=True, r=S.r * 0.6)),
        detail(seg(14, 13, 12, 20.5)),
        line(seg(3, 10, 6, 10)),
    ]


@icon("vandalism", CAT, "Smashed window with a crack pattern beside a zigzag scrawl of spray paint",
      tags=["graffiti", "broken window", "property damage", "criminal damage", "spray paint", "break-in"])
def _(S):
    return [
        shell(rect(2.5, 3, 11, 15, rr(S, 2))),
        detail(seg(8, 10.5, 4, 6)), detail(seg(8, 10.5, 12, 5)), detail(seg(8, 10.5, 12, 15)), detail(seg(8, 10.5, 4, 14.5)),
        line(poly([(16.5, 5), (21, 9), (16.5, 13), (21, 17)])),
        line(seg(2.5, 21.5, 21.5, 21.5)),
    ]


@icon("car-break-in", CAT, "Car in side view with a shattered side window and glass shards falling below",
      tags=["smashed window", "vehicle theft", "car crime", "broken glass", "theft from car", "vandal"])
def _(S):
    return [
        shell("M2.5 15V11.5L6.5 10.5L9.5 5.5H15L18 10.5L21.5 11.5V15Z"),
        mark(circle(7, 15.5, 2.5)), mark(circle(17, 15.5, 2.5)),
        detail(seg(12, 8.5, 10, 6.8)), detail(seg(12, 8.5, 14.3, 6.8)), detail(seg(12, 8.5, 12, 10.8)),
        mark(poly([(8.5, 19.8), (10.5, 19.8), (9.5, 22)], closed=True)),
        mark(poly([(12, 19.5), (14, 19.8), (12.5, 22)], closed=True)),
        mark(poly([(16, 19.8), (18, 19.5), (17.5, 22)], closed=True)),
    ]


@icon("snow-cave", CAT, "Rounded mound of snow with a small dark tunnel entrance and a snowflake above",
      tags=["snow shelter", "winter survival", "avalanche", "mountain emergency", "bivouac", "dig in"])
def _(S):
    return [
        shell("M2.5 21C2.5 14 7 9.5 12 9.5C17 9.5 21.5 14 21.5 21Z"),
        mark("M9.5 21V18.5A2.5 2.5 0 0 1 14.5 18.5V21Z"),
        line(seg(12, 2, 12, 6)), line(seg(10, 3.2, 14, 4.8)), line(seg(14, 3.2, 10, 4.8)),
    ]


@icon("hose-bridge", CAT, "Low ramp laid over a fire hose with a car tyre rolling up onto it",
      tags=["hose ramp", "hose protector", "drive over hose", "road crossing", "fire hose", "traffic"])
def _(S):
    return [
        shell(poly([(2, 21), (6, 14.5), (18, 14.5), (22, 21)], closed=True, r=S.r * 0.5)),
        mark(circle(12, 18, 1.75)),
        shell(circle(12, 7.5, 4.5)),
        mark(circle(12, 7.5, 1.25)),
    ]


@icon("foam-branch-nozzle", CAT, "Straight foam nozzle tube with air intake holes near the inlet and a cloud of foam at the tip",
      tags=["foam nozzle", "foam branchpipe", "firefighting foam", "aspirating nozzle", "hose", "fire service"])
def _(S):
    return [
        shell(rect(2.5, 8.5, 3, 7, rr(S, 1))),
        shell(poly([(5.5, 8.5), (15, 10.5), (15, 13.5), (5.5, 15.5)], closed=True, r=S.r * 0.6)),
        mark(circle(8.3, 12, 1)), mark(circle(11.3, 12, 1)),
        shell(union(circle(18.2, 12, 2.3), circle(20.3, 8.8, 1.8), circle(20.3, 15.2, 1.8))),
    ]


@icon("turnout-gear-locker", CAT, "Locker with a firefighter helmet on top, a coat in the middle and boots at the bottom",
      tags=["gear locker", "bunker gear", "fire station", "firefighter kit", "protective clothing", "storage"])
def _(S):
    return [
        shell(rect(3, 2, 18, 20, rr(S, 3))),
        mark("M8.5 7C8.5 4.2 10 3.8 12 3.8C14 3.8 15.5 4.2 15.5 7Z"),
        mark(rect(7.5, 7, 9, 1.2, 0.5)),
        mark(poly([(7.5, 11), (10, 9.8), (14, 9.8), (16.5, 11), (17, 15.5), (15, 15.5), (15, 17), (9, 17), (9, 15.5), (7, 15.5)], closed=True)),
        mark(rect(7.5, 18.3, 3.5, 2, 0.6)), mark(rect(13, 18.3, 3.5, 2, 0.6)),
    ]


@icon("fire-extinguisher-cabinet", CAT, "Wall cabinet with a window showing a fire extinguisher standing inside",
      tags=["extinguisher box", "fire point", "wall cabinet", "fire safety", "glass door", "break glass"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 3))),
        mark(union(rect(8.5, 11, 7, 8.5, 1.5), rect(10.5, 8, 3, 3.5), rect(9, 6.5, 6.5, 1.8, 0.6))),
        detail("M15.5 7.5C18 7.5 18 11 16.5 13"),
    ]


@icon("antique-hand-pumper", CAT, "Old two-wheeled fire cart with a long seesaw pump handle across the top",
      tags=["hand pump", "historic fire engine", "vintage firefighting", "manual pumper", "fire cart", "heritage"])
def _(S):
    return [
        line(seg(2.5, 3.5, 21.5, 7.5)),
        line(seg(12, 5.5, 12, 9.5)),
        shell(rect(4.5, 9.5, 15, 4, rr(S, 2))),
        shell(circle(7.5, 18, 3)), shell(circle(16.5, 18, 3)),
        mark(circle(7.5, 18, 1)), mark(circle(16.5, 18, 1)),
    ]


@icon("steam-fire-engine", CAT, "Antique fire engine with a tall vertical boiler, a smokestack and large spoked wheels",
      tags=["steamer", "steam pumper", "historic fire engine", "vintage", "antique", "boiler"])
def _(S):
    return [
        shell(rect(9, 2, 3.5, 4.5, rr(S, 1))),
        shell(rect(6, 6.5, 9.5, 8, rr(S, 3))),
        shell(rect(3, 14.5, 18, 3, rr(S, 1.5))),
        line(poly([(17, 14.5), (17, 11), (21.5, 11)], r=S.r * 0.5)),
        shell(circle(7, 19, 2.75)), shell(circle(17.5, 19, 2.75)),
    ]


@icon("fire-perimeter-map", CAT, "Map with a jagged fire boundary line enclosing a flame",
      tags=["wildfire map", "fire boundary", "burn area", "fire spread", "incident map", "containment line"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(poly([(7.5, 8), (11, 6.5), (13.5, 8), (17, 7.5), (16.5, 12), (17, 16.5), (12, 15), (8, 17), (8, 12.5)], closed=True)),
        mark(flame(12, 9, 14, 4, S)),
    ]


@icon("fire-training-tower", CAT, "Tall drill tower with rows of window openings and a ladder running up one side",
      tags=["drill tower", "training tower", "fire academy", "rescue training", "practice building", "fire service"])
def _(S):
    return [
        shell(rect(3, 2.5, 12.5, 19, rr(S, 1.5))),
        mark(rect(6, 5.5, 3, 3.5, 0.5)), mark(rect(10, 5.5, 3, 3.5, 0.5)),
        mark(rect(6, 11, 3, 3.5, 0.5)), mark(rect(10, 11, 3, 3.5, 0.5)),
        mark(rect(6, 16, 3, 3.5, 0.5)), mark(rect(10, 16, 3, 3.5, 0.5)),
        line(seg(21, 3, 21, 21.5)),
        line(seg(18, 6, 21, 6)), line(seg(18, 10, 21, 10)), line(seg(18, 14, 21, 14)), line(seg(18, 18, 21, 18)),
    ]


@icon("smoke-vent", CAT, "Roof hatch propped open on its hinge with smoke billowing out of the opening",
      tags=["roof vent", "heat and smoke vent", "ventilation", "smoke hatch", "fire ventilation", "skylight"])
def _(S):
    return [
        shell(rect(3, 15, 18, 6.5, rr(S, 2))),
        shell(poly([(3, 12), (3, 10), (10, 6), (10, 8)], closed=True, r=S.r * 0.3)),
        line(seg(10, 8, 11.5, 15)),
        line("M15.5 12.5C14 10.5 17 9.5 15.5 7.5C14 5.5 17 4.5 15.5 2.5"),
        line("M20 13C18.5 11.5 21.5 10.5 20 9"),
    ]


# ============================================================================ chunk 4

@icon("firefighter-switch", CAT, "Wall box with a flame label above a big lever switch set in the down, off position",
      tags=["fire service switch", "fireman's switch", "solar shutoff", "emergency cutoff", "power isolator", "lever"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 3))),
        mark(flame(12, 4.5, 10, 4.5, S)),
        detail(seg(12, 12.5, 8.5, 18)),
        mark(circle(8, 18.3, 2.2)),
        mark(circle(12.3, 12.3, 1.3)),
    ]


@icon("candle-fire-hazard", CAT, "Lit candle standing next to a hanging curtain whose edge has caught a small flame",
      tags=["home fire risk", "open flame", "curtain fire", "candle safety", "fire prevention", "unattended candle"])
def _(S):
    return [
        shell(rect(3.5, 13, 5.5, 8.5, rr(S, 1.5))),
        mark(flame(6.25, 4.5, 11, 4.5, S)),
        line(seg(13.5, 2.5, 22, 2.5)),
        shell("M14.5 2.5H21.5V19C20.3 20.5 19.5 20.5 18 19C16.5 20.5 15.7 20.5 14.5 19Z"),
        mark(flame(16.3, 9, 14, 3.2, S)),
    ]


@icon("oil-tank-fire", CAT, "Round industrial storage tank with tall flames rising from its roof",
      tags=["tank fire", "refinery fire", "industrial fire", "fuel storage", "petrochemical", "storage tank blaze"])
def _(S):
    return [
        shell(rect(6, 10, 12, 11.5, rr(S, 2))),
        detail(seg(6, 15.5, 18, 15.5)),
        mark(flame(9.5, 1.5, 9, 5, S)), mark(flame(15, 3, 9, 4.5, S)),
    ]


@icon("toxic-plume", CAT, "Factory chimney with a dark cloud drifting sideways from the top, marked by a skull",
      tags=["chemical release", "air pollution", "hazardous cloud", "poison gas", "industrial accident", "toxic smoke"])
def _(S):
    skull = path_to_d(D(P(union(circle(17, 8, 3), rect(15.2, 9.8, 3.6, 3, 0.5))), P(circle(15.7, 7.8, 0.95)), P(circle(18.3, 7.8, 0.95))))
    cloud = union(circle(13.5, 8, 3.5), circle(17.5, 6.5, 4.5), circle(20, 10.5, 3), circle(14, 11.5, 2.8))
    return [
        shell(poly([(2.5, 21.5), (4, 9), (9, 9), (10.5, 21.5)], closed=True, r=S.r * 0.4)),
        shell(cloud),
        mark(skull),
    ]


@icon("cribbing-blocks", CAT, "Criss-cross stack of blocks supporting a wide car underside above",
      tags=["wood blocks", "box crib", "vehicle support", "stabilisation", "technical rescue", "heavy lift"])
def _(S):
    return [
        line(seg(2, 4.5, 22, 4.5)),
        shell(rect(3, 8, 6, 4, rr(S, 1))), shell(rect(15, 8, 6, 4, rr(S, 1))),
        shell(rect(2.5, 12, 19, 4, rr(S, 1))),
        shell(rect(3, 16, 6, 4, rr(S, 1))), shell(rect(15, 16, 6, 4, rr(S, 1))),
    ]


@icon("windshield-saw", CAT, "Hand saw with a D-shaped grip, a long pointed blade and coarse teeth along its lower edge",
      tags=["glass saw", "car rescue tool", "extrication", "cutting windshield", "rescue saw", "hand tool"])
def _(S):
    return [
        shell(rect(2.5, 7, 6, 9, rr(S, 2.5))),
        shell(poly([(8.5, 8.5), (21.5, 14.5), (19, 14.5), (17.5, 17), (15.5, 14.5), (13.5, 17), (11.5, 14.5), (9.5, 16.5)], closed=True)),
    ]


@icon("scoop-stretcher", CAT, "Long stretcher made of two hinged halves side by side with hand holes in each",
      tags=["split stretcher", "rescue litter", "lift injured", "ambulance", "medical transport", "patient carry"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 6, rr(S, 3))),
        shell(rect(2.5, 13.5, 19, 6, rr(S, 3))),
        mark(rect(6, 6.6, 4, 1.8, 0.8)), mark(rect(14, 6.6, 4, 1.8, 0.8)),
        mark(rect(6, 15.6, 4, 1.8, 0.8)), mark(rect(14, 15.6, 4, 1.8, 0.8)),
    ]


@icon("traction-splint", CAT, "Leg with a long splint frame running past the foot and a cord pulling the ankle strap straight",
      tags=["leg splint", "femur fracture", "broken leg", "first aid", "paramedic", "immobilise"])
def _(S):
    return [
        line(poly([(2.5, 6.5), (21.5, 6.5), (21.5, 17.5), (2.5, 17.5)], r=S.r * 0.5)),
        shell(rect(3.5, 9.5, 12, 5, 2.5)),
        detail(seg(12.5, 9.5, 12.5, 14.5)),
        line(seg(15.5, 12, 21.5, 12)),
    ]


@icon("extrication-vest", CAT, "Short vertical board vest with side flaps wrapped around it and chest straps across the front",
      tags=["kendrick", "spinal immobiliser", "head neck support", "car crash rescue", "spine board", "trauma"])
def _(S):
    return [
        shell(rect(8, 2.5, 8, 19, rr(S, 2))),
        shell(poly([(8, 8), (2.5, 10), (2.5, 18), (8, 18)], closed=True, r=S.r * 0.5)),
        shell(poly([(16, 8), (21.5, 10), (21.5, 18), (16, 18)], closed=True, r=S.r * 0.5)),
        detail(seg(8, 11.5, 16, 11.5)), detail(seg(8, 15, 16, 15)),
    ]


@icon("check-door-heat", CAT, "Open hand pressed flat against a closed door with three heat waves rising above it",
      tags=["fire safety", "touch test", "back of hand", "feel door", "escape fire", "hot door"])
def _(S):
    return [
        shell(rect(10, 7, 11, 14.5, rr(S, 2))),
        mark(circle(18, 14.5, 1)),
        mark(poly([(2.5, 11), (5.5, 11), (5.5, 9.5), (8.5, 9.5), (8.5, 17), (5.5, 17), (2.5, 14)], closed=True)),
        line("M12.5 5C11.5 4 13.5 3 12.5 2"), line("M15.5 5C14.5 4 16.5 3 15.5 2"), line("M18.5 5C17.5 4 19.5 3 18.5 2"),
    ]


@icon("move-to-higher-ground", CAT, "Person climbing a slope with an arrow pointing up and a wavy water line rising at the foot of the hill",
      tags=["flood evacuation", "tsunami", "escape uphill", "seek high ground", "rising water", "evacuate"])
def _(S):
    return [
        line(poly([(8, 21.5), (21.5, 8.5)], r=S.r)),
        head(13, 6),
        line(poly([(14, 9), (15, 13.5), (11.5, 15.5)], r=S.r)),
        line("M2.5 17C4 15.5 5.5 15.5 7 17"), line("M2.5 21C4 19.5 5.5 19.5 7 21"),
        line(seg(5, 12, 5, 3.5)),
        line(poly([(2.5, 6), (5, 3.5), (7.5, 6)])),
    ]


# ============================================================================ chunk 5

@icon("relief-convoy", CAT, "Two box trucks driving one behind the other, the front one flying a small flag from its cab",
      tags=["aid convoy", "humanitarian aid", "supply trucks", "disaster relief", "delivery", "emergency transport"])
def _(S):
    return [
        shell(rect(2, 9, 7, 8, rr(S, 1.5))),
        shell(rect(11, 9, 6, 8, rr(S, 1.5))),
        shell(poly([(17, 12), (19.5, 12), (22, 15), (22, 17), (17, 17)], closed=True, r=S.r * 0.4)),
        dot(4.5, 19.3, 1.7), dot(7.5, 19.3, 1.7), dot(13, 19.3, 1.7), dot(19.5, 19.3, 1.7),
        line(seg(19, 12, 19, 4)),
        solid(poly([(19, 4), (15, 5.5), (19, 7)], closed=True)),
    ]


@icon("field-kitchen", CAT, "Trailer carrying two large cooking pots with steam rising from each",
      tags=["mobile kitchen", "disaster feeding", "relief meals", "soup kitchen", "catering trailer", "hot food"])
def _(S):
    return [
        shell(rect(2.5, 15, 19, 5, rr(S, 2))),
        shell(rect(4.5, 8.5, 6, 6.5, rr(S, 1.5))),
        shell(rect(13.5, 8.5, 6, 6.5, rr(S, 1.5))),
        dot(12, 21.3, 1.3),
        line("M7.5 6C6 5 9 4 7.5 2.5"), line("M16.5 6C15 5 18 4 16.5 2.5"),
    ]


@icon("hygiene-kit", CAT, "Zip bag with a toothbrush, a soap bar and a small towel sticking out of the top",
      tags=["toiletry bag", "sanitation kit", "wash kit", "personal care", "relief supplies", "toothbrush"])
def _(S):
    return [
        line(seg(6.5, 9, 6.5, 3)),
        mark(rect(5.4, 2, 2.2, 3.2, 0.6)),
        shell(rect(10, 4, 5.5, 4.5, rr(S, 1.5))),
        shell(rect(18, 4, 3.5, 5, rr(S, 1))),
        shell(rect(2.5, 9, 19, 12.5, rr(S, 3))),
        detail(seg(2.5, 13, 21.5, 13)),
    ]


@icon("water-bladder-tank", CAT, "Large flat pillow-shaped water bladder lying on the ground with a tap and outlet hose",
      tags=["pillow tank", "bladder tank", "emergency water", "water storage", "potable water", "relief"])
def _(S):
    return [
        shell("M2.5 13C2.5 10 6 8.5 11 8.5C15 8.5 19 10 19 13C19 16 15 17.5 11 17.5C6 17.5 2.5 16 2.5 13Z"),
        mark("M11 10.5C12.4 12.3 13.1 13.2 13.1 14A2.1 2.1 0 0 1 8.9 14C8.9 13.2 9.6 12.3 11 10.5Z"),
        line(poly([(19, 13), (21.5, 13), (21.5, 18)], r=S.r * 0.5)),
        line(seg(2, 21, 22, 21)),
    ]


@icon("emergency-shelter-sign", CAT, "Square sign showing a house outline with two people inside it",
      tags=["evacuation centre", "safe shelter", "refuge", "assembly point", "shelter in place", "relief camp"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, S.R)),
        detail(poly([(6, 12), (12, 6.5), (18, 12), (18, 18), (6, 18)], closed=True, r=S.r * 0.5)),
        mark(circle(9.7, 12.8, 1.2)), mark(rect(8.4, 14.4, 2.6, 2.8, 1)),
        mark(circle(14.3, 12.8, 1.2)), mark(rect(13, 14.4, 2.6, 2.8, 1)),
    ]


@icon("kill-switch-lanyard", CAT, "Boat engine cut-off switch with a coiled lanyard running to a wrist loop",
      tags=["engine cut-off", "boat safety", "stop switch", "outboard", "man overboard", "wrist strap"])
def _(S):
    return [
        shell(rect(14, 2.5, 7.5, 6.5, rr(S, 1.5))),
        mark(circle(17.75, 5.75, 1.2)),
        line(poly([(16, 9), (12, 10.5), (16, 12.5), (12, 14), (16, 15.5), (11, 17)], r=S.r * 0.4)),
        shell(circle(7, 19, 3)),
    ]


@icon("bilge-pump", CAT, "Manual boat pump with a vertical tube, a T-handle plunger on top and an outlet hose on the side",
      tags=["boat pump", "hand pump", "bail water", "sinking boat", "marine", "plunger"])
def _(S):
    return [
        line(seg(6, 3.5, 18, 3.5)),
        line(seg(12, 3.5, 12, 8)),
        shell(rect(8.5, 8, 7, 13.5, rr(S, 2))),
        line(poly([(15.5, 14), (19.5, 14), (21.5, 17), (21.5, 21.5)], r=S.r)),
    ]


@icon("fire-proximity-suit", CAT, "Front view of a reflective aluminised suit with a hood, a dark face visor and shine lines on the body",
      tags=["aluminised suit", "heat protective clothing", "firefighter", "foundry", "silver suit", "radiant heat"])
def _(S):
    return [
        shell(circle(12, 6.5, 4.5)),
        mark(rect(9.3, 5, 5.4, 3, 1.2)),
        shell(poly([(8, 12), (16, 12), (21.5, 15), (20, 21.5), (4, 21.5), (2.5, 15)], closed=True, r=S.r * 0.8)),
        detail(seg(9, 15.5, 7.5, 20)), detail(seg(13.5, 15.5, 12, 20)),
    ]


@icon("bomb-disposal-suit", CAT, "Front view of a bulky padded protective suit with a large boxy helmet and a flat visor slot",
      tags=["eod suit", "explosive ordnance", "blast protection", "bomb squad", "heavy armour", "padded suit"])
def _(S):
    return [
        shell(rect(6.5, 2, 11, 9, rr(S, 4))),
        mark(rect(8.5, 5, 7, 2.2, 0.8)),
        shell(rect(3.5, 12, 17, 9.5, rr(S, 3))),
        detail(seg(8.5, 12, 8.5, 21.5)), detail(seg(15.5, 12, 15.5, 21.5)),
    ]


@icon("crank-flashlight", CAT, "Flashlight with a folding hand crank arm on top for recharging without batteries",
      tags=["wind-up torch", "dynamo light", "hand crank", "emergency light", "no batteries", "power outage"])
def _(S):
    return [
        shell(poly([(2.5, 7.5), (8, 10), (8, 15), (2.5, 17.5)], closed=True, r=S.r * 0.5)),
        shell(rect(8, 10, 12.5, 5, rr(S, 2))),
        mark(circle(16.5, 12.5, 1)),
        line(poly([(12.5, 10), (12.5, 4.5), (18, 4.5)], r=S.r * 0.6)),
        mark(circle(19, 4.5, 1.7)),
    ]


@icon("no-sitting-sign", CAT, "Prohibition circle with a slash across a seated figure",
      tags=["do not sit", "no seating", "keep clear", "prohibited", "sit ban", "restriction"])
def _(S):
    return [
        line(circle(12, 12, 9)),
        head(10, 7.5, 2),
        line(poly([(10, 10.5), (10, 15), (15.5, 15), (15.5, 19)], r=S.r)),
        line(seg(5.6, 5.6, 18.4, 18.4)),
    ]


@icon("exit-door-alarm", CAT, "Door with a horizontal push bar and an alarm box above it with sound waves on both sides",
      tags=["emergency exit", "alarmed door", "panic bar", "fire exit", "door alert", "egress"])
def _(S):
    return [
        shell(rect(4, 2, 16, 5, rr(S, 1.5))),
        mark(circle(8, 4.5, 1.1)), mark(circle(12, 4.5, 1.1)), mark(circle(16, 4.5, 1.1)),
        shell(rect(6, 9.5, 12, 12, rr(S, 2))),
        detail(seg(8.5, 15.5, 15.5, 15.5)),
    ]


@icon("lifeboat-station", CAT, "Boathouse on the shore with a slipway running down from its door into wavy sea",
      tags=["rescue station", "rnli", "sea rescue", "boat launch", "slipway", "coast rescue"])
def _(S):
    return [
        shell(poly([(2.5, 16.5), (2.5, 9), (9, 4), (15.5, 9), (15.5, 16.5)], closed=True, r=S.r * 0.5)),
        mark(rect(6.5, 11, 5, 5.5, 0.8)),
        line(seg(12, 17.5, 21.5, 21.5)),
        line("M17 12C18.5 10.5 20 10.5 21.5 12"),
        line("M2.5 20.5H9"),
    ]


@icon("emergency-department", CAT, "Hospital building with a cross on top and an ambulance parked beneath its entrance canopy",
      tags=["er", "a and e", "accident and emergency", "hospital entrance", "casualty", "ambulance bay"])
def _(S):
    return [
        shell(rect(3, 2, 18, 8, rr(S, 2))),
        mark(union(rect(10.8, 3.6, 2.4, 4.8), rect(9.6, 4.8, 4.8, 2.4))),
        line(seg(2, 12, 22, 12)),
        shell(union(rect(4.5, 14.5, 10, 5, rr(S, 1.5)), poly([(14.5, 15.5), (17.5, 15.5), (20, 18), (20, 19.5), (14.5, 19.5)], closed=True))),
        mark(circle(8, 20.5, 1.5)), mark(circle(17, 20.5, 1.5)),
    ]


@icon("river-ice-jam", CAT, "Bridge over a river with broken ice slabs piled up against it and water lines below",
      tags=["ice dam", "frozen river", "flooding", "winter flood", "ice floes", "thaw"])
def _(S):
    return [
        line(seg(2, 6, 22, 6)),
        line(seg(6, 6, 6, 11)), line(seg(18, 6, 18, 11)),
        shell(poly([(3.5, 18), (7, 12.5), (12, 14), (10.5, 18.5)], closed=True)),
        shell(poly([(11, 13), (15.5, 9.5), (20.5, 12), (18, 17)], closed=True)),
        line("M2.5 21.5C4.5 20 6.5 20 8.5 21.5S12.5 23 14.5 21.5"),
    ]


@icon("quicksand-sign", CAT, "Warning triangle showing a figure sunk up to the waist in wavy sand with arms raised",
      tags=["sinking", "mud", "bog", "hazard sign", "trapped", "danger sand"])
def _(S):
    return [
        shell(poly([(12, 2.5), (22, 20), (2, 20)], closed=True, r=S.r * 0.8)),
        mark(circle(12, 8.3, 1.3)),
        detail(poly([(9.3, 8.5), (10.8, 11.5), (13.2, 11.5), (14.7, 8.5)])),
        detail(seg(12, 11.5, 12, 14.5)),
        detail("M6.5 15.8C8.5 14.3 10.5 14.3 12 15.8S15.5 17.3 17.5 15.8"),
    ]
