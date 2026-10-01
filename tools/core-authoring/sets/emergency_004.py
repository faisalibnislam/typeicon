"""TypeIcon Core: emergency (batch 004).

Warning and prohibition signs, rescue and fire-safety kit, and rescue scenes, drawn from the objects themselves.
Signs put a simple glyph inside a triangle (shell) or a prohibition ring (line). Figures follow the stick-figure
style of sets/activities_002.py (solid head r 2.25 over 2 px limbs).
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

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


def rseg(x1, y1, x2, y2, deg, dx=0.0, dy=0.0):
    (a, b), (c, d) = rpts([(x1, y1), (x2, y2)], deg, dx, dy)
    return seg(a, b, c, d)


def rr(S, cap):
    return min(S.R, cap)


def head(x, y):
    return dot(x, y, 2.25)


def tri(S):
    """Warning triangle outline."""
    return shell(poly([(12, 2.5), (22.5, 21), (1.5, 21)], closed=True, r=L(S, 0.0, 2.0)), stroke_miterlimit="4")


SLASH = seg(5.5, 5.5, 18.5, 18.5)


def sk(d, w=1.6):
    """Solid stroked mark (knocked out of a Filled shell)."""
    return mark(path_to_d(ST(d, w, "round", "round")))


def nosign(S, *objs, gap=1.4):
    """Prohibition ring and slash, with the object drawn as solid marks cut clear of the slash."""
    cut = ST(SLASH, 2 + 2 * gap, "butt", "miter")
    out = [line(circle(12, 12, 9.25)), line(SLASH)]
    regs = [P(o) if isinstance(o, str) else o for o in objs]
    body = D(U(*regs), cut)
    out.append(solid(path_to_d(body)))
    return out


def ob(S, d, w=2.0):
    """Stroked object path as a region (butt and miter in Line, round in Rounded)."""
    return ST(d, w, S.cap, S.join, 4.0)


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


# ============================================================================ signs and hazards

@icon("falling-branches-sign", CAT, "Warning triangle with a snapped branch dropping toward a standing figure",
      tags=["falling branch", "tree hazard", "storm warning", "falling debris", "forest safety", "danger overhead"])
def _(S):
    return [
        tri(S),
        sk("M9.5 9.8L12.2 13.2", 1.8), sk("M10.8 11.5L9 12.3", 1.3), sk("M11.8 12.6L13 10.8", 1.3),
        mark(circle(15, 13.2, 1.2)),
        sk("M15 15L15 17", 1.6), sk("M13.6 18.6L15 17L16.4 18.6", 1.3),
    ]


@icon("open-mine-shaft-sign", CAT, "Warning triangle with a figure with raised arms above a dark shaft opening in the ground",
      tags=["mine shaft", "open shaft", "fall hazard", "abandoned mine", "danger hole", "warning"])
def _(S):
    return [
        tri(S),
        mark(circle(12, 10.3, 1.3)),
        sk("M9.3 9.5L12 12.6L14.7 9.5", 1.3), sk("M12 12.6V14.2", 1.3),
        mark(ellipse(12, 17.6, 4.3, 1.9)),
    ]


@icon("no-kites-sign", CAT, "Prohibition ring with a slash over a diamond kite and its tail",
      tags=["no kite flying", "kite ban", "power line safety", "prohibited", "no kites", "overhead lines"])
def _(S):
    kite = poly([(15.5, 4.5), (19, 8.5), (15.5, 13), (12, 8.5)], closed=True, r=S.r * 1.6)
    kite = rotd(kite, 35, 15.5, 8.75)
    tail = ob(S, "M13 12Q11 13 12 14.5Q13 16 10.5 17Q8 18 7.5 19.5", 1.4)
    return nosign(S, kite, tail, gap=0.9)


@icon("no-leaning-sign", CAT, "Prohibition ring with a slash over a figure leaning against a door",
      tags=["do not lean", "no leaning", "door safety", "lift door", "prohibited", "train door"])
def _(S):
    return nosign(
        S,
        ob(S, "M18 5.5V18.5", 1.6),
        circle(14, 7.5, 1.8),
        ob(S, "M14.5 10.5L12.5 14.5", 1.9), ob(S, "M12.5 14.5L10 18.5", 1.9), ob(S, "M12.5 14.5L14 18.5", 1.9),
        ob(S, "M14 11.5L10.8 13.2", 1.6),
        gap=0.9,
    )


@icon("no-strollers-sign", CAT, "Prohibition ring with a slash over a baby stroller seen from the side",
      tags=["no prams", "no buggies", "no pushchairs", "prohibited", "baby stroller ban", "stairs"])
def _(S):
    hood = "M7.5 12.5H19A6 6 0 0 0 13 6.5V12.5Z"
    return nosign(
        S,
        hood if S.name == "rounded" else poly([(7.5, 12.5), (19, 12.5), (17.5, 8.5), (13, 6.5), (13, 12.5)], closed=True),
        ob(S, "M7.5 12.5L6 7.5H4.5", 1.6),
        rect(6.9, 14.7, 3.2, 3.2, 0) if S.name == "line" else circle(8.5, 16.3, 1.7),
        rect(14.4, 14.7, 3.2, 3.2, 0) if S.name == "line" else circle(16, 16.3, 1.7),
        gap=0.9,
    )


@icon("bull-in-field-sign", CAT, "Warning triangle with a bull seen from the side with its head lowered and horns forward",
      tags=["bull", "livestock warning", "farm hazard", "field warning", "cattle", "dangerous animal"])
def _(S):
    body = poly([(17.5, 11.8), (14, 10.4), (11.5, 10.4), (9.8, 12), (8.2, 13.3), (7.2, 15.3), (8.6, 16.2), (10.6, 15.4), (17.3, 15.4)], closed=True, r=0)
    return [
        tri(S),
        mark(body),
        mark(rect(10.6, 15, 1.6, 3.6)), mark(rect(15.6, 15, 1.6, 3.6)),
        sk("M8.8 12.6Q6.6 12 7.2 9.8", 1.3), sk("M17.5 12.2L18.8 14.4", 1.0),
    ]


@icon("unsafe-structure-sign", CAT, "Warning triangle with a leaning building cut by a jagged crack",
      tags=["unsafe building", "collapse risk", "structural damage", "condemned", "keep out", "warning"])
def _(S):
    bld = poly([(6.8, 18.5), (9.6, 10.3), (16.8, 12), (16.3, 18.5)], closed=True, r=0)
    crack = ST("M12.5 10.5L11 13.5L14 14.8L12 18.6", 1.3, "butt", "miter")
    return [tri(S), mark(path_to_d(D(P(bld), crack)))]


# ============================================================================ tools and gear

@icon("hose-spanner-wrench", CAT, "Flat spanner with a curved hooked head and a tapered pry tip for hose couplings",
      tags=["hose wrench", "coupling wrench", "spanner", "fire hose tool", "storz key", "hose spanner"])
def _(S):
    head_ = minus(union(circle(12, 6.5, 5.25), rect(10.5, 9, 3, 6, 0)), circle(14.6, 4.5, 3.3))
    handle = poly([(10.25, 10), (13.75, 10), (13.75, 17), (12, 21.5), (10.25, 17)], closed=True, r=S.r * 0.3)
    return [shell(rotd(union(head_, handle), 45), stroke_miterlimit="3")]


@icon("roof-escape-hatch", CAT, "Vehicle roof section with a square hatch lid tilted open and an upward arrow",
      tags=["roof hatch", "emergency exit", "bus roof exit", "escape hatch", "evacuation", "vehicle exit"])
def _(S):
    k = rr(S, 1.5)
    return [
        shell(rect(2, 16, 20, 5, k)),
        shell(rotd(rect(5.5, 12, 9, 2.6, rr(S, 1.2)), -38, 5.5, 14.5)),
        line(seg(19.5, 13, 19.5, 5)),
        line(poly([(16.8, 7.5), (19.5, 4.8), (22.2, 7.5)], r=S.r)),
    ]


@icon("storm-damaged-roof", CAT, "House with a torn gap in the roof and pieces of roofing flying off",
      tags=["roof damage", "storm damage", "hurricane", "tornado damage", "missing shingles", "wind damage"])
def _(S):
    return [
        line(poly([(2.5, 12), (11, 4.5), (14.5, 7.5)], r=S.r * 0.5)),
        line(poly([(14.5, 7.5), (13, 10), (16, 10.5)], r=0)),
        line(poly([(19.5, 10), (21.5, 11.8)], r=0)),
        line(poly([(5, 13), (5, 21), (19, 21), (19, 14)], r=S.r)),
        mark(poly([(17, 4), (19.2, 3), (20, 5.2), (17.8, 6.2)], closed=True)),
        mark(rect(20, 7, 2, 2, 0)),
        mark(rect(14.5, 2.2, 2, 2, 0)),
    ]


@icon("litter-wheel", CAT, "Rescue stretcher bed with carry handles at both ends and one large wheel under its middle",
      tags=["wheeled litter", "stretcher wheel", "rough terrain", "mountain rescue", "wilderness rescue", "carry"])
def _(S):
    return [
        shell(rect(5, 5.5, 14, 4, rr(S, 2))),
        line(seg(1.5, 7.5, 5, 7.5)), line(seg(19, 7.5, 22.5, 7.5)),
        line(seg(12, 9.5, 12, 12.5)),
        shell(circle(12, 17, 4.5)),
        dot(12, 17, 1.2) if S.name == "rounded" else Part("dot", rect(11, 16, 2, 2, 0)),
    ]


@icon("lifeboat-davit", CAT, "Two curved davit arms on a deck holding a lifeboat on ropes",
      tags=["davit", "lifeboat", "ship safety", "abandon ship", "launch boat", "maritime"])
def _(S):
    return [
        line(seg(2, 21, 22, 21)),
        line("M3 21V9Q3 4 8 4"), line("M21 21V9Q21 4 16 4"),
        line(seg(8.5, 4, 8.5, 11)), line(seg(15.5, 4, 15.5, 11)),
        shell(poly([(7, 11), (17, 11), (15, 17), (9, 17)], closed=True, r=S.r * 0.8)),
    ]


@icon("scramble-net", CAT, "Rope net hanging from a ship rail down to the water",
      tags=["boarding net", "rope ladder", "man overboard", "ship rescue", "climb aboard", "cargo net"])
def _(S):
    ropes = ""
    for k in range(-2, 4):
        c = 6 * k
        ropes += f"M{5 + c} 5.5L{5 + c + 14} 19.5M{5 + c + 14} 5.5L{5 + c} 19.5"
    mesh = I(ST(ropes, 2, "butt", "miter", 4.0), P(rect(5, 5.5, 14, 10.5, 0)))
    return [
        shell(rect(2, 2.5, 20, 3, rr(S, 1.5))),
        solid(path_to_d(mesh)),
        line("M2 20Q4.5 18 7 20T12 20T17 20T22 20"),
    ]


@icon("mine-refuge-chamber", CAT, "Steel box shelter on skids inside a tunnel arch with a door and an air tank",
      tags=["refuge chamber", "mine safety", "underground shelter", "safe room", "tunnel shelter", "air supply"])
def _(S):
    return [
        line("M3 21V13A9 9 0 0 1 21 13V21"),
        shell(rect(7, 10.5, 10, 8.5, rr(S, 2))),
        detail(seg(11.5, 10.5, 11.5, 19)),
        dot(14.3, 14.8, 1.2),
        line(seg(6, 20.5, 18, 20.5)),
    ]


@icon("self-rescuer", CAT, "Small belt-worn canister on a belt clip with a short hose leading to a mouthpiece",
      tags=["escape respirator", "mine safety", "emergency breathing", "air canister", "smoke escape", "oxygen device"])
def _(S):
    return [
        line(seg(2, 5.5, 13, 5.5)), line(seg(7.5, 5.5, 7.5, 9)),
        shell(rect(3, 9, 9, 12, rr(S, 3.5))),
        detail(seg(3, 13.5, 12, 13.5)),
        line("M12 17H16Q19 17 19 14V9.5"),
        shell(rect(16, 3, 6, 6.5, rr(S, 2.5))),
    ]


@icon("bed-shaker-alarm", CAT, "Pillow with a flame mark resting on a round vibrating disc with shake lines",
      tags=["vibrating alarm", "deaf alarm", "smoke alarm pillow", "hearing impaired", "fire alert", "sleeping"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 8, rr(S, 3.5))),
        mark(flame(12, 4.2, 9, 3.6, S)),
        shell(circle(12, 17.3, 3.5)),
        line("M5.5 14.5Q4 17.3 5.5 20"), line("M18.5 14.5Q20 17.3 18.5 20"),
    ]


@icon("rogue-wave", CAT, "Huge curling wave towering over a small ship",
      tags=["giant wave", "freak wave", "tsunami", "sea danger", "ocean storm", "maritime hazard"])
def _(S):
    wave = "M2 21C2 12 5.5 4 12 4C17 4 19.5 7.5 18.5 10.5C17 8.5 14.5 9 13.5 11C12.5 13.5 13.5 18 14 21Z"
    return [
        shell(wave),
        shell(poly([(17, 17.5), (22.5, 17.5), (21, 21), (18.5, 21)], closed=True, r=S.r * 0.4)),
        line(seg(19.8, 17.5, 19.8, 13.5)),
    ]


@icon("emergency-food-bucket", CAT, "Lidded stackable bucket with a carry handle and a fork mark on its side",
      tags=["emergency rations", "survival food", "food storage", "prepper", "disaster supplies", "meal pouches"])
def _(S):
    return [
        line(poly([(6, 7), (6, 3), (18, 3), (18, 7)], r=S.r * 1.5)),
        shell(rect(4, 7, 16, 3, rr(S, 1.5))),
        shell(poly([(5.5, 10), (18.5, 10), (17, 21.5), (7, 21.5)], closed=True, r=S.r * 0.6)),
        mark(rect(9.6, 14.8, 4.8, 1.3)), mark(rect(11.3, 16, 1.4, 4.2)),
        mark(rect(9.6, 12.3, 1.2, 2.6)), mark(rect(11.4, 12.3, 1.2, 2.6)), mark(rect(13.2, 12.3, 1.2, 2.6)),
    ]


@icon("help-y-signal", CAT, "Person standing with both arms raised in a Y shape, the signal for needing help",
      tags=["y signal", "need help", "distress", "air rescue signal", "wilderness", "sos"])
def _(S):
    return [
        head(12, 4.6),
        line(poly([(5, 3), (12, 10), (19, 3)], r=S.r)),
        line(seg(12, 10, 12, 15.5)),
        line(poly([(8, 21.5), (12, 15.5), (16, 21.5)], r=S.r)),
    ]


# ============================================================================ fire safety and rescue kit

@icon("car-fire-blanket", CAT, "Large fire blanket draped over a car with its wheels showing below and a small flame escaping at the edge",
      tags=["vehicle fire", "electric vehicle fire", "fire blanket", "smother fire", "car fire", "suppression"])
def _(S):
    drape = ("M2.5 14.5C2.5 11.5 4.5 10.5 6.5 10C7.5 7.5 9.5 5.5 12 5.5C14.5 5.5 16 7.5 16.8 10C17.8 10.5 18.5 11.5 18.5 14.5"
             "Q17 16 15.5 14.5Q14 16 12.5 14.5Q11 16 9.5 14.5Q8 16 6.5 14.5Q5 16 3.5 14.5Z")
    return [
        shell(drape),
        shell(circle(6.5, 19.6, 2)), shell(circle(14.5, 19.6, 2)),
        mark(flame(21, 11, 19, 3.6, S)),
    ]


@icon("drain-cover-seal", CAT, "Square rubber mat laid over a drain grate with a spill puddle held back at its edge",
      tags=["drain seal", "spill control", "drain mat", "chemical spill", "stormwater protection", "spill kit"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 12.5, rr(S, 3))),
        detail(seg(9, 6, 9, 11.5)), detail(seg(12, 6, 12, 11.5)), detail(seg(15, 6, 15, 11.5)),
        line("M2.5 19.5Q5 17.5 7.5 19.5T12.5 19.5T17.5 19.5T21.5 19.5"),
    ]


@icon("aerosol-fire-extinguisher", CAT, "Small pressurised spray can with a nozzle cap misting a small flame",
      tags=["spray extinguisher", "kitchen fire", "car extinguisher", "mini extinguisher", "spray can", "fire safety"])
def _(S):
    return [
        shell(rect(3, 10.5, 7.5, 11, rr(S, 3))),
        shell(rect(4.75, 6, 4, 4.5, rr(S, 1.2))),
        line(seg(8.75, 7.8, 11.5, 7.8)),
        dot(14.2, 6.3, 1.05), dot(17, 8.3, 1.05), dot(14.8, 10, 1.05), dot(18.2, 4.8, 1.05),
        mark(flame(18.5, 12.5, 21.5, 5, S)),
    ]


@icon("safety-instruction-card", CAT, "Folded three-panel card showing a seat belt, a mask and an exit door",
      tags=["safety card", "briefing card", "airline card", "instructions", "evacuation guide", "passenger safety"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, rr(S, 2.5))),
        detail(seg(8.7, 4, 8.7, 20)), detail(seg(15.3, 4, 15.3, 20)),
        sk("M4.3 8L7 13", 1.3), mark(rect(4, 14, 3, 2)),
        mark(circle(12, 10.5, 1.4)), sk("M12 12.5V16", 1.3),
        mark(rect(17.3, 8, 3, 6)), sk("M17.8 16.5H20", 1.2),
    ]


@icon("lone-worker-alarm", CAT, "Small clip-on alarm device with a round SOS button and a lying-down figure mark",
      tags=["lone worker", "man down", "personal alarm", "panic button", "sos device", "worker safety"])
def _(S):
    return [
        shell(rect(6, 2, 12, 19.5, rr(S, 3.5))),
        detail(circle(12, 8, 2.6)),
        mark(circle(8.6, 15.8, 1.1)),
        sk("M10.8 15.8H15.6", 1.5),
    ]


@icon("ice-rescue-sled", CAT, "Flat rescue sled seen from above with two grab handles, lying on cracked ice",
      tags=["ice rescue", "rescue board", "thin ice", "water rescue", "frozen lake", "flotation sled"])
def _(S):
    return [
        shell(poly([(2.5, 3.5), (16, 3.5), (21.5, 8.5), (16, 13.5), (2.5, 13.5)], closed=True, r=S.r * 1.3)),
        detail(seg(6, 8.5, 12, 8.5)),
        line(poly([(2, 20), (6, 17.5), (9, 21), (13, 17.5), (16, 21), (22, 18.5)], r=S.r * 0.4)),
    ]


@icon("forestry-helmet", CAT, "Safety helmet with a flip-down mesh visor and ear defenders on both sides",
      tags=["chainsaw helmet", "logging helmet", "arborist", "tree work", "hearing protection", "face shield"])
def _(S):
    return [
        shell("M5.5 11.5C5.5 6 8 3 12 3C16 3 18.5 6 18.5 11.5Z"),
        shell(rect(6.5, 11.5, 11, 9.5, rr(S, 4.5))),
        detail(seg(12, 11.5, 12, 21)), detail(seg(6.5, 16, 17.5, 16)),
        shell(rect(1.8, 9, 3.6, 7, rr(S, 1.8))), shell(rect(18.6, 9, 3.6, 7, rr(S, 1.8))),
    ]


@icon("powered-air-respirator", CAT, "Loose hood with a clear visor joined by a hose to a belt-mounted battery blower",
      tags=["papr", "air hood", "blower respirator", "protective hood", "clean air", "respiratory protection"])
def _(S):
    return [
        shell("M3 12V9.5C3 5 5.5 2.5 9 2.5C12.5 2.5 15 5 15 9.5V12Z"),
        detail(rect(5.5, 5.8, 7, 3.4, rr(S, 1.4))),
        line("M9 12V15.5Q9 19 13.5 19"),
        shell(rect(13.5, 15.5, 8, 6, rr(S, 3))),
    ]


@icon("hot-work-permit", CAT, "Permit form on a clipboard with a flame mark and a signature line",
      tags=["welding permit", "fire watch", "work permit", "clipboard", "permit to work", "site safety"])
def _(S):
    return [
        shell(rect(4, 4, 16, 18, rr(S, 2.5))),
        shell(rect(8.5, 2, 7, 3.5, rr(S, 1.5))),
        mark(flame(12, 8, 15, 5.4, S)),
        detail(seg(8, 18.3, 16, 18.3)),
    ]


@icon("accident-report-book", CAT, "Bound logbook with a plus cross on its cover and a pen standing beside it",
      tags=["accident book", "incident log", "first aid log", "injury record", "health and safety", "logbook"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 13.5, 19, rr(S, 2.5))),
        detail(seg(6.3, 2.5, 6.3, 21.5)),
        mark(rect(9.75, 8, 1.6, 6)), mark(rect(7.5, 10.2, 6, 1.6)),
        shell(poly([(18.5, 3), (21.5, 3), (21.5, 16), (20, 20), (18.5, 16)], closed=True, r=S.r * 0.4)),
    ]


@icon("hypothermia-wrap", CAT, "Person lying wrapped in layered blankets with a hood, only the face showing",
      tags=["cold exposure", "blanket wrap", "warming", "first aid", "thermal blanket", "cold rescue"])
def _(S):
    return [
        shell(circle(6, 13.5, 4)),
        dot(6, 13.5, 1.3),
        shell(rect(10, 10, 12, 7, rr(S, 3.5))),
        detail(seg(14.5, 10, 13.5, 17)), detail(seg(18.5, 10, 17.5, 17)),
        line(seg(2, 20.5, 22, 20.5)),
    ]


# ============================================================================ tests, drills and rescues

@icon("smoke-alarm-tester", CAT, "Long pole with a cup on top pressed up against a smoke alarm on the ceiling",
      tags=["alarm test pole", "smoke detector tester", "ceiling alarm", "test alarm", "building maintenance", "fire safety check"])
def _(S):
    return [
        line(seg(2, 2.5, 22, 2.5)),
        shell("M4 3.5H20C20 6.5 16.5 8 12 8C7.5 8 4 6.5 4 3.5Z"),
        shell(poly([(9, 12), (15, 12), (13.6, 15.8), (10.4, 15.8)], closed=True, r=S.r * 0.4)),
        line(seg(12, 15.8, 12, 22)),
    ]


@icon("extinguisher-training", CAT, "Person aiming a fire extinguisher at a small fire burning in a metal tray",
      tags=["fire drill", "extinguisher practice", "fire marshal training", "pass method", "fire training", "workplace safety"])
def _(S):
    return [
        head(4.5, 5.5),
        line(seg(4.5, 8, 4.5, 14)),
        line(poly([(2.5, 21), (4.5, 14), (6.5, 21)], r=S.r)),
        line(seg(4.5, 9.5, 9, 11.5)),
        shell(rect(9, 10.5, 3.8, 7, rr(S, 1.9))),
        line(seg(12.8, 12, 15, 12)),
        mark(flame(18.5, 7.5, 16.5, 5.2, S)),
        line(poly([(15, 18.5), (16.5, 21), (21.5, 21), (23, 18.5)], r=S.r * 0.4)),
    ]


@icon("smother-pan-fire", CAT, "Frying pan with a lid being slid across it to smother the flames in it",
      tags=["pan fire", "kitchen fire", "chip pan fire", "put a lid on it", "cooking fire", "smother flames"])
def _(S):
    return [
        shell(rect(2.5, 15.5, 14, 5, rr(S, 2.5))),
        line(seg(16.5, 17.5, 22, 17.5)),
        shell("M7.5 13H18.5C18.5 9.5 16 8.2 13 8.2C10 8.2 7.5 9.5 7.5 13Z"),
        line(seg(13, 8.2, 13, 5.5)),
        mark(flame(4.6, 9, 14.3, 3.6, S)),
    ]


@icon("tyrolean-traverse", CAT, "Rope stretched between two cliffs with a person hanging from a pulley crossing it",
      tags=["rope traverse", "zip line rescue", "rope crossing", "cliff rescue", "high line", "technical rescue"])
def _(S):
    return [
        shell(poly([(2, 5.5), (4.5, 5.5), (5.3, 12), (6, 21.5), (2, 21.5)], closed=True, r=S.r * 0.4)),
        shell(poly([(22, 5.5), (19.5, 5.5), (18.7, 12), (18, 21.5), (22, 21.5)], closed=True, r=S.r * 0.4)),
        line("M5 6Q12 9.5 19 6"),
        shell(circle(12, 8.8, 1.4)),
        line(seg(12, 10.4, 12, 11.8)),
        head(12, 13.8),
        line(seg(12, 16, 12, 18.8)),
        line(poly([(10.3, 22), (12, 18.8), (13.7, 22)], r=S.r)),
    ]


@icon("raker-shore", CAT, "Diagonal timber brace propping up a leaning wall and anchored to the ground",
      tags=["wall shoring", "building collapse", "diagonal brace", "structural support", "urban search and rescue", "prop"])
def _(S):
    return [
        shell(rect(3, 2.5, 5, 19, rr(S, 1.5))),
        line(seg(2, 21.5, 22, 21.5)),
        line(seg(8, 7, 17.5, 18.5)),
        line(seg(8, 12.5, 12, 11.5)),
        line(seg(17.5, 18.5, 17.5, 21.5)),
    ]


@icon("ladder-rescue", CAT, "Firefighter climbing down a ladder with a person carried over one shoulder",
      tags=["aerial ladder", "fire rescue", "carry down", "firefighter carry", "evacuation", "fireman lift"])
def _(S):
    return [
        line(seg(15.5, 2, 15.5, 22)), line(seg(21, 2, 21, 22)),
        line(seg(15.5, 5, 21, 5)), line(seg(15.5, 10, 21, 10)), line(seg(15.5, 15, 21, 15)), line(seg(15.5, 20, 21, 20)),
        head(9.5, 4.5),
        line(seg(9.5, 7.2, 10, 14)),
        line(poly([(7, 21.5), (10, 14), (13, 21.5)], r=S.r)),
        line(seg(10, 9.5, 15.5, 11.5)),
        dot(3.2, 15.5, 1.3),
        line(seg(4.4, 14, 9.2, 8.5)),
    ]


@icon("car-extrication", CAT, "Car with its roof cut away and folded back and a hydraulic cutter at its pillar",
      tags=["vehicle extrication", "jaws of life", "roof removal", "crash rescue", "hydraulic cutter", "trapped in car"])
def _(S):
    return [
        shell("M2 17V14.5Q2 13 3.5 13H16.5Q18 13 18 14.5V17Z"),
        shell(circle(6.5, 19, 2)), shell(circle(14, 19, 2)),
        shell(rotd(rect(3, 9.5, 10, 2.4, rr(S, 1.2)), -62, 3, 12)),
        line(seg(22, 2, 19, 5.5)),
        line(poly([(15.8, 6.5), (19, 5.5), (17, 9.8)], r=S.r * 0.5)),
    ]


@icon("sandbagging", CAT, "Person lifting a sandbag onto a low wall of stacked sandbags",
      tags=["flood defence", "flood defense", "sandbag wall", "flood protection", "sand bag", "flood barrier"])
def _(S):
    return [
        head(5, 5),
        line(seg(5, 7.8, 6, 14)),
        line(poly([(3.5, 21.5), (6, 14), (8.5, 21.5)], r=S.r)),
        line(seg(5.5, 10, 8.8, 9)),
        shell(rect(8.5, 6, 6.5, 4, rr(S, 2))),
        shell(rect(10, 17, 6, 4, rr(S, 2))), shell(rect(16.5, 17, 5.5, 4, rr(S, 2))),
        shell(rect(13, 12.8, 6, 3.4, rr(S, 1.7))),
    ]


@icon("cable-protector-ramp", CAT, "Low ramped cover lying on a floor over three cables to stop people tripping",
      tags=["cable cover", "trip hazard", "floor cable ramp", "wire guard", "cord cover", "event safety"])
def _(S):
    return [
        shell(poly([(2, 20), (5.5, 12.5), (18.5, 12.5), (22, 20)], closed=True, r=S.r * 0.6)),
        dot(8.5, 16.5, 1.3), dot(12, 16.5, 1.3), dot(15.5, 16.5, 1.3),
    ]


@icon("cracked-wall", CAT, "Brick wall with a wide jagged crack splitting it from top to bottom",
      tags=["wall crack", "structural crack", "subsidence", "earthquake damage", "damaged building", "brickwork"])
def _(S):
    crack = poly([(10.5, 3), (11.8, 8), (10, 11.5), (12.5, 14.5), (10.5, 18), (11.6, 21),
                  (14.4, 21), (14.8, 17.5), (13, 14.5), (14.8, 11.5), (13, 8.2), (13.6, 3)], closed=True)
    return [
        shell(rect(3, 3, 18, 18, rr(S, 2.5))),
        detail(seg(3, 9, 7.5, 9)), detail(seg(3, 15, 7.5, 15)),
        detail(seg(17, 9, 21, 9)), detail(seg(17, 15, 21, 15)),
        mark(crack),
    ]


@icon("dry-hydrant", CAT, "Capped standpipe beside a pond with its intake pipe running under the water",
      tags=["rural water supply", "suction point", "pond hydrant", "fire water source", "static water", "intake"])
def _(S):
    return [
        shell(rect(3, 2.5, 6, 2.5, rr(S, 1.2))),
        shell(rect(4, 5, 4, 6, rr(S, 1))),
        line(seg(2, 11, 10.5, 11)),
        line("M12 11Q14 9.5 16 11T20 11T22 11"),
        line(poly([(6, 11), (6, 18), (16, 18)], r=S.r)),
        shell(rect(16, 15.8, 4.5, 4.4, rr(S, 1))),
    ]


@icon("hot-stick", CAT, "Long insulated pole whose hooked end catches an overhead power line",
      tags=["lineman tool", "insulated pole", "live line", "power line work", "utility tool", "electrical safety"])
def _(S):
    return [
        line("M2 6.5H22"),
        line("M3 21L15.5 8.5L17 3.8Q18.4 2.5 19.8 3.8L20.2 6"),
    ]


@icon("shock-absorbing-lanyard", CAT, "Fall-arrest lanyard with a snap hook at each end and a folded shock pack in the middle",
      tags=["fall arrest", "energy absorber", "safety harness", "working at height", "snap hook", "lanyard"])
def _(S):
    k = rr(S, 2.4)
    return [
        shell(rect(1.8, 8.5, 5, 7, k)),
        line(seg(6.8, 12, 9, 12)),
        shell(rect(9, 7.5, 6, 9, rr(S, 2.5))),
        detail(seg(9, 12, 15, 12)),
        line(seg(15, 12, 17.2, 12)),
        shell(rect(17.2, 8.5, 5, 7, k)),
    ]


@icon("manhole-ventilation-blower", CAT, "Portable blower with a flexible duct running down into an open manhole",
      tags=["confined space", "air blower", "manhole fan", "duct ventilation", "sewer work", "fresh air"])
def _(S):
    return [
        line(seg(2, 15, 5, 15)), line(seg(11, 15, 22, 15)),
        line(seg(5, 15, 5, 21.5)), line(seg(11, 15, 11, 21.5)),
        shell(circle(16.5, 9, 4)),
        dot(16.5, 9, 1.2),
        line("M12.5 9Q8 9 8 13V19"),
    ]


@icon("manhole-guard", CAT, "Square guard rail with corner posts standing around an open round manhole, seen from above",
      tags=["manhole barrier", "open hole guard", "confined space guard", "street works", "fall protection", "safety rail"])
def _(S):
    return [
        line(rect(3.5, 3.5, 17, 17, rr(S, 3))),
        dot(3.5, 3.5, 1.7), dot(20.5, 3.5, 1.7), dot(3.5, 20.5, 1.7), dot(20.5, 20.5, 1.7),
        shell(circle(12, 12, 4.5)),
    ]


@icon("portable-scene-light", CAT, "Tripod stand with two angled floodlight heads on top, lighting the ground below",
      tags=["scene lighting", "floodlight tripod", "emergency lighting", "work light", "night rescue", "lighting tower"])
def _(S):
    return [
        shell(rotd(rect(2.5, 2.5, 8, 4.5, rr(S, 1.8)), -18, 6.5, 4.75)),
        shell(rotd(rect(13.5, 2.5, 8, 4.5, rr(S, 1.8)), 18, 17.5, 4.75)),
        line(seg(12, 6.5, 12, 14)),
        line(poly([(7, 21.5), (12, 14), (17, 21.5)], r=S.r)),
        line(seg(12, 14, 12, 21.5)),
    ]


@icon("sea-dye-marker", CAT, "Swimmer's head in the water inside a bright spreading patch of marker dye",
      tags=["dye marker", "sea marker", "man overboard", "search and rescue", "survivor in water", "fluorescein"])
def _(S):
    return [
        shell("M6 16C2.5 16 2 11 5.5 9.8C5.5 5.5 10.5 4 13.5 6.3C17.5 4.8 20.5 8.8 18.5 11.3C21.5 12.3 21 16.3 17.5 16.5Z"),
        head(12, 10.3),
        line("M2 21Q4.5 19 7 21T12 21T17 21T22 21"),
    ]


@icon("radar-reflector", CAT, "Octahedral metal radar reflector with crossing plates hoisted on a mast",
      tags=["boat reflector", "marine safety", "radar target", "mast fitting", "visibility at sea", "octahedral"])
def _(S):
    return [
        shell(poly([(12, 2.5), (19.5, 10), (12, 17.5), (4.5, 10)], closed=True, r=S.r * 0.8), stroke_miterlimit="4"),
        detail(seg(4.5, 10, 19.5, 10)), detail(seg(12, 2.5, 12, 17.5)),
        line(seg(12, 17.5, 12, 22)),
    ]


@icon("tv-emergency-banner", CAT, "Television screen showing a warning triangle with a scrolling alert banner along the bottom",
      tags=["emergency broadcast", "tv alert", "weather warning", "news ticker", "public warning", "broadcast alert"])
def _(S):
    return [
        shell(rect(2, 3.5, 20, 14.5, rr(S, 3))),
        detail(poly([(12, 6), (15, 11), (9, 11)], closed=True, r=0)),
        mark(rect(5, 13.3, 14, 2, L(S, 0, 1))),
        line(seg(8, 21.5, 16, 21.5)),
    ]


@icon("evacuation-door-tag", CAT, "Door hanger tag with a hanging hole, a check mark and a small house below it",
      tags=["door hanger", "evacuation check", "house cleared", "search marking", "disaster response", "checked house"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 19, rr(S, 4))),
        dot(12, 6, 1.6),
        detail(poly([(8.8, 10.8), (11, 13), (15.2, 9.6)], r=0)),
        mark(poly([(12, 14.6), (16, 17.2), (16, 19.6), (8, 19.6), (8, 17.2)], closed=True)),
    ]


@icon("building-safety-placard", CAT, "Notice card posted on a door with a wide header bar and a building outline showing it is inspected",
      tags=["inspection placard", "building inspected", "safe to enter", "damage assessment", "structural inspection", "notice"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, rr(S, 2.5))),
        mark(rect(7.5, 5.5, 9, 2.6, L(S, 0, 1))),
        mark(poly([(8, 19), (8, 13.2), (12, 10.3), (16, 13.2), (16, 19)], closed=True)),
    ]


@icon("snow-emergency-route-sign", CAT, "Road sign on a post showing a snowflake, marking a snow emergency route",
      tags=["snow route", "winter road", "no parking snow", "emergency route", "road sign", "winter storm"])
def _(S):
    flake = [seg(12, 6.2, 12, 13.8), seg(8.7, 8.1, 15.3, 11.9), seg(8.7, 11.9, 15.3, 8.1)]
    return [
        shell(rect(2.5, 3, 19, 14.5, rr(S, 3))),
        *[detail(d) for d in flake],
        line(seg(12, 17.5, 12, 22)),
    ]


@icon("frozen-pipe", CAT, "Water pipe section coated with icicles hanging from it and a crack in its wall",
      tags=["burst pipe", "frozen water", "winter plumbing", "icicles", "freeze damage", "cold snap"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 19, 7, rr(S, 3))),
        detail(poly([(12, 5.5), (10.6, 8), (13.2, 9.4), (12, 12.5)], r=0)),
        mark(poly([(5.5, 12), (8.5, 12), (7, 19.5)], closed=True)),
        mark(poly([(15, 12), (18, 12), (16.5, 21)], closed=True)),
    ]


@icon("crevasse-rescue", CAT, "Person hanging on a rope inside a deep glacier crack with a rescuer at the edge above",
      tags=["glacier rescue", "ice crack", "rope rescue", "mountaineering", "fall into crevasse", "alpine rescue"])
def _(S):
    return [
        head(4.8, 3.2),
        line(seg(4.8, 5.4, 4.8, 9)),
        line("M6.5 6.8Q12 7 12 12"),
        head(12, 14.5),
        line(seg(12, 16.8, 12, 20.5)),
        line(poly([(2, 11), (6, 11), (7.5, 16), (7, 22)], r=S.r * 0.5)),
        line(poly([(22, 11), (18, 11), (16.5, 16), (17, 22)], r=S.r * 0.5)),
    ]


@icon("injured-person", CAT, "Standing person with a bandaged head and one arm held in a sling",
      tags=["casualty", "patient", "first aid", "injury", "wounded", "bandage"])
def _(S):
    return [
        shell(circle(11, 5, 3)),
        detail(seg(8, 4.2, 14, 4.2)),
        line(seg(11, 8.5, 11, 15)),
        line(poly([(8, 21.5), (11, 15), (14, 21.5)], r=S.r)),
        line(seg(11, 10.5, 7.5, 14)),
        shell(poly([(12.5, 9.5), (19, 12.5), (12.5, 15)], closed=True, r=S.r * 0.3)),
    ]


@icon("stretcher-carry", CAT, "Two rescuers carrying a patient lying on a stretcher between them",
      tags=["casualty carry", "medical evacuation", "rescue team", "carrying patient", "first responders", "stretcher bearers"])
def _(S):
    return [
        head(3.2, 4.5),
        line(seg(3.2, 7, 3.2, 14)),
        line(poly([(1.6, 21.5), (3.2, 14), (4.8, 21.5)], r=S.r)),
        head(20.8, 4.5),
        line(seg(20.8, 7, 20.8, 14)),
        line(poly([(19.2, 21.5), (20.8, 14), (22.4, 21.5)], r=S.r)),
        shell(rect(5, 11, 14, 2.6, rr(S, 1.3))),
        dot(7.5, 8.2, 1.4),
        line(seg(10, 8.2, 17, 8.2)),
    ]
