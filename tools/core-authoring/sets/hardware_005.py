"""TypeIcon Core: hardware (batch 005): electrical fittings, HVAC, lumber, steel, masonry, roofing and finishing tools.

Drawn from the objects themselves, flat or in a light isometric view so each reads at 24 px.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "hardware"


def rot(pts, deg=45, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rp(pts, closed=True, r=0.0, deg=45):
    return poly(rot(pts, deg), closed=closed, r=r)


def rseg(x1, y1, x2, y2, deg=45):
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg)
    return seg(a, b, c, d)


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def rk(S, cap):
    """Square corners in Line, rounded (up to cap) in Rounded."""
    return 0 if S.name == "line" else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def kdot(d) -> Part:
    return Part("dot", d)


def diag_lines(x0, y0, x1, y1, step=6.0, minlen=2.5):
    """Diamond mesh: +-45 degree lines clipped to a rectangle, as d-strings."""
    out = []
    c = y0 - x1
    while c <= y1 - x0:
        a, b = max(x0, y0 - c), min(x1, y1 - c)
        if b - a > minlen:
            out.append(seg(a, a + c, b, b + c))
        c += step
    c = x0 + y0
    while c <= x1 + y1:
        a, b = max(x0, c - y1), min(x1, c - y0)
        if b - a > minlen:
            out.append(seg(a, c - a, b, c - b))
        c += step
    return out


def prism(face, v, r=0.0):
    """Silhouette (d-string) of a flat face swept along vector v; draw with shell() and add the front outline as detail()."""
    n = len(face)
    parts = [P(poly(face, closed=True))]
    for i in range(n):
        a, b = face[i], face[(i + 1) % n]
        parts.append(P(poly([a, b, (b[0] + v[0], b[1] + v[1]), (a[0] + v[0], a[1] + v[1])], closed=True)))
    parts.append(P(poly([(x + v[0], y + v[1]) for x, y in face], closed=True)))
    return path_to_d(U(*parts))


# ============================================================================ electrical fittings

@icon("conduit-bender", CAT, "Long-handled conduit bender with a curved shoe at the bottom",
      tags=["emt bender", "electrician", "pipe bending", "conduit", "tool", "wiring"])
def _(S):
    return [
        shell("M7 2.5H11V14A4 4 0 0 0 15 18V22A8 8 0 0 1 7 14Z" if S.name == "line" else
              "M8 2.5H10Q11 2.5 11 3.5V14A4 4 0 0 0 15 18V22A8 8 0 0 1 7 14V3.5Q7 2.5 8 2.5Z"),
        line(seg(15, 20, 22, 20)),
    ]


@icon("fish-tape", CAT, "Round reel case with a handle and a steel tape ending in a hook",
      tags=["electrician", "wire puller", "conduit", "pulling wire", "tool", "cable"])
def _(S):
    return [
        shell(circle(9, 14.5, 7)),
        dot(9, 14.5, 1.5),
        line(poly([(5.5, 8.5), (5.5, 3.5), (12.5, 3.5), (12.5, 8.5)], r=S.r)),
        line(poly([(16, 14.5), (21.5, 14.5), (21.5, 11)], r=S.r)),
    ]


@icon("terminal-block", CAT, "Row of wire terminal cells with a screw on top of each",
      tags=["wiring", "connector", "electrical", "screw terminal", "din rail", "electronics"])
def _(S):
    return [
        shell(rect(2, 7, 20, 11, rr(S, 2))),
        detail(seg(8.67, 7, 8.67, 18)),
        detail(seg(15.33, 7, 15.33, 18)),
        dot(5.33, 11, 1.4),
        dot(12, 11, 1.4),
        dot(18.67, 11, 1.4),
        line(seg(5.33, 18, 5.33, 22)),
        line(seg(12, 18, 12, 22)),
        line(seg(18.67, 18, 18.67, 22)),
    ]


@icon("ring-terminal", CAT, "Crimp connector with a round ring end and a wire barrel",
      tags=["lug", "crimp", "wiring", "battery cable", "electrical", "connector"])
def _(S):
    return [
        shell("M2 12A5 5 0 0 1 12 12H13V9H16V15H13V12" if False else circle(7, 12, 5.5)),
        detail(circle(7, 12, 2)),
        shell(poly([(12.5, 10), (17, 10), (17, 14), (12.5, 14)], closed=True, r=S.r * 0.4)),
        line(seg(17, 12, 22, 12)),
    ]


@icon("wire-strands", CAT, "Cable end with the jacket on one side and bare strands fanning out",
      tags=["stripped wire", "conductors", "electrician", "cable end", "copper", "wiring"])
def _(S):
    return [
        shell(rect(2, 8, 7, 8, rr(S, 1.5))),
        line(poly([(9, 10), (14, 10), (21, 6)], r=S.r)),
        line(seg(9, 12, 22, 12)),
        line(poly([(9, 14), (14, 14), (21, 18)], r=S.r)),
    ]


@icon("coaxial-cable", CAT, "Cross section of a coaxial cable with core, insulation ring and outer sheath",
      tags=["coax", "antenna cable", "tv cable", "rf", "shielded cable", "wiring"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(circle(12, 12, 4.5)),
        dot(12, 12, 1.5) if S.name == "rounded" else sq(10.5, 10.5, 3, 3),
    ]


@icon("utility-pole", CAT, "Power pole with two cross arms and insulators on top of each arm",
      tags=["telephone pole", "power line", "electric pole", "overhead line", "grid", "electricity"])
def _(S):
    return [
        line(seg(12, 2, 12, 22)),
        line(seg(3.5, 7.5, 20.5, 7.5)),
        line(seg(6.5, 14, 17.5, 14)),
        line(seg(3.5, 7.5, 3.5, 5)),
        line(seg(20.5, 7.5, 20.5, 5)),
        line(seg(8, 14, 8, 11.5)),
        line(seg(16, 14, 16, 11.5)),
        line(seg(12, 22, 7.5, 22)) if False else line(seg(8.5, 22, 15.5, 22)),
    ]


@icon("pole-transformer", CAT, "Cylindrical transformer can on a pole with two bushings on top",
      tags=["distribution transformer", "power line", "electric utility", "grid", "voltage", "electricity"])
def _(S):
    return [
        line(seg(4.5, 2, 4.5, 22)),
        line(seg(4.5, 9.5, 9, 9.5)),
        line(seg(4.5, 18, 9, 18)),
        shell(rect(9, 7, 11, 14, rr(S, 2))),
        detail(seg(9, 11, 20, 11)),
        line(seg(12.5, 7, 12.5, 3.5)),
        line(seg(16.5, 7, 16.5, 3.5)),
        dot(12.5, 3, 1.4),
        dot(16.5, 3, 1.4),
    ]


@icon("usb-wall-outlet", CAT, "Wall plate with a power socket and two small usb ports",
      tags=["charging outlet", "usb socket", "wall socket", "electrical", "charger", "home improvement"])
def _(S):
    return [
        shell(rect(3.5, 2, 17, 20, rr(S, 3))),
        sq(8, 5.5, 2, 4.5),
        sq(14, 5.5, 2, 4.5),
        sq(7, 14, 4, 2),
        sq(13, 14, 4, 2),
    ]


@icon("light-bulb-socket", CAT, "Threaded lamp holder cup with two wires coming out of the bottom",
      tags=["lamp holder", "lamp socket", "light fixture", "electrical", "e26", "wiring"])
def _(S):
    return [
        shell(rect(6.5, 2, 11, 13, rr(S, 3))),
        detail(seg(6.5, 6, 17.5, 6)),
        detail(seg(6.5, 10, 17.5, 10)),
        shell(rect(9, 15, 6, 3, rr(S, 1))),
        line(seg(10.5, 18, 10.5, 22)),
        line(seg(13.5, 18, 13.5, 22)),
    ]


@icon("clamp-light", CAT, "Cone reflector work lamp with a spring clamp on top",
      tags=["work light", "shop light", "reflector lamp", "clip light", "garage", "workshop"])
def _(S):
    return [
        line(poly([(9.5, 8), (9.5, 3), (16, 3), (16, 8)], r=S.r)),
        shell(poly([(9, 8), (15, 8), (21, 15.5), (3, 15.5)], closed=True, r=S.r)),
        dot(12, 19, 2),
    ]


@icon("mobile-light-tower", CAT, "Tall mast on a small trailer topped with four floodlights",
      tags=["portable lighting", "construction site light", "floodlights", "night work", "road works", "generator"])
def _(S):
    return [
        shell(rect(3.5, 2, 17, 5.5, rr(S, 1.5))),
        detail(seg(7.75, 2, 7.75, 7.5)),
        detail(seg(12, 2, 12, 7.5)),
        detail(seg(16.25, 2, 16.25, 7.5)),
        line(seg(12, 7.5, 12, 17)),
        line(seg(4, 17, 20, 17)),
        dot(8, 20.25, 1.75),
        dot(16, 20.25, 1.75),
    ]


@icon("grounding-rod", CAT, "Rod driven into the ground with a clamp and wire near the top",
      tags=["earth rod", "ground rod", "earthing", "electrical safety", "lightning", "copper rod"])
def _(S):
    return [
        line(seg(12, 3, 12, 22)),
        shell(rect(9.5, 5, 5, 3.5, rr(S, 1))),
        line(poly([(14.5, 6.75), (19, 6.75), (19, 12)], r=S.r)),
        line(seg(3, 12, 21, 12)),
    ]


@icon("battery-terminal", CAT, "Tapered battery post with a cable clamp and a bolt",
      tags=["car battery", "post", "clamp", "automotive", "cable end", "electrical"])
def _(S):
    return [
        line(seg(2, 21, 22, 21)),
        shell(poly([(9, 21), (10, 14.5), (14, 14.5), (15, 21)], closed=True)),
        shell(rect(7.5, 10, 9, 4.5, rr(S, 1.5))),
        line(seg(16.5, 12.25, 21, 12.25)),
        line(poly([(12, 10), (12, 5), (17, 5)], r=S.r)),
    ]


@icon("jumper-cables", CAT, "Two cables crossing between pairs of clamps at each end",
      tags=["booster cables", "jump start", "car battery", "automotive", "emergency", "roadside"])
def _(S):
    return [
        shell(rect(2, 3.5, 5, 5, rr(S, 3))),
        shell(rect(2, 15.5, 5, 5, rr(S, 3))),
        shell(rect(17, 3.5, 5, 5, rr(S, 3))),
        shell(rect(17, 15.5, 5, 5, rr(S, 3))),
        line("M7 6C12 6 12 18 17 18"),
        line("M7 18C12 18 12 6 17 6"),
    ]


@icon("alligator-clip", CAT, "Spring clip with two angled jaws and a wire lead",
      tags=["crocodile clip", "test lead", "electrical clamp", "electronics", "testing", "wire"])
def _(S):
    return [
        shell(poly([(7, 11), (21, 5), (21, 9)], closed=True)),
        shell(poly([(7, 13), (21, 19), (21, 15)], closed=True)),
        line(poly([(7, 12), (3, 12), (3, 21)], r=S.r)),
    ]


@icon("cable-tray", CAT, "Open ladder-style tray with two rails and cross rungs",
      tags=["cable ladder", "wire management", "conduit", "data center", "electrical", "cable run"])
def _(S):
    return [
        line(seg(2, 6.5, 22, 6.5)),
        line(seg(2, 17.5, 22, 17.5)),
        line(seg(6, 6.5, 6, 17.5)),
        line(seg(12, 6.5, 12, 17.5)),
        line(seg(18, 6.5, 18, 17.5)),
        line(poly([(2, 6.5), (2, 10)], r=S.r)),
        line(poly([(22, 6.5), (22, 10)], r=S.r)),
    ]


@icon("cable-gland", CAT, "Domed cap nut over a hex body with a cable passing through",
      tags=["cable entry", "strain relief", "waterproof fitting", "enclosure", "electrical", "connector"])
def _(S):
    return [
        line(seg(12, 2, 12, 5)),
        shell("M7.5 11V9.5A4.5 4.5 0 0 1 16.5 9.5V11Z"),
        shell(poly([(4.5, 13.5), (7, 11), (17, 11), (19.5, 13.5), (17, 16), (7, 16)], closed=True, r=S.r * 0.4)),
        shell(rect(8.5, 16, 7, 3.5)),
        line(seg(12, 19.5, 12, 22)),
    ]


@icon("air-duct", CAT, "Rectangular sheet metal duct with a ninety degree bend",
      tags=["hvac", "ductwork", "ventilation", "air handling", "heating", "cooling"])
def _(S):
    return [
        shell(poly([(3, 3), (11, 3), (11, 12), (21, 12), (21, 21), (3, 21)], closed=True, r=S.r)),
        detail(seg(3, 8, 11, 8)),
        detail(seg(16, 12, 16, 21)),
    ]


@icon("flexible-duct", CAT, "Ribbed round flexible hose bending in a quarter circle",
      tags=["flex duct", "hose", "hvac", "ventilation", "dryer vent", "ducting"])
def _(S):
    ribs = [detail(f"M{fmt(polar(3, 21, 7, a)[0])} {fmt(polar(3, 21, 7, a)[1])}L{fmt(polar(3, 21, 15, a)[0])} {fmt(polar(3, 21, 15, a)[1])}") for a in (-65, -40, -15)]
    return [shell("M3 6A15 15 0 0 1 18 21H10A7 7 0 0 0 3 14Z")] + ribs


@icon("air-vent-register", CAT, "Rectangular wall vent with horizontal louvre slats",
      tags=["air vent", "grille", "louvre", "hvac", "ventilation", "register cover"])
def _(S):
    return [
        shell(rect(2, 3.5, 20, 17, rr(S, 3))),
        detail(seg(6, 8, 18, 8)),
        detail(seg(6, 12, 18, 12)),
        detail(seg(6, 16, 18, 16)),
    ]


@icon("ac-condenser-unit", CAT, "Outdoor air conditioner box with a round fan grille",
      tags=["air conditioning", "heat pump", "hvac", "outdoor unit", "cooling", "condenser fan"])
def _(S):
    c = (12, 12)
    spokes = "".join(f"M12 12L{fmt(polar(12, 12, 3.6, a)[0])} {fmt(polar(12, 12, 3.6, a)[1])}" for a in (90, 210, 330))
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 4))),
        detail(circle(12, 12, 6.5)),
        detail(spokes),
    ]


@icon("chimney-cap", CAT, "Small pitched cap held above a flue pipe on short legs",
      tags=["flue cap", "chimney pot", "rain cap", "roofing", "vent pipe", "fireplace"])
def _(S):
    return [
        shell(poly([(4, 9.5), (12, 3.5), (20, 9.5)], closed=True, r=S.r)),
        line(seg(8, 9.5, 8, 15)),
        line(seg(12, 9.5, 12, 15)),
        line(seg(16, 9.5, 16, 15)),
        shell(rect(6, 15, 12, 6.5, rr(S, 2))),
    ]


@icon("lumber-stack", CAT, "Stack of boards seen from the end in three rows",
      tags=["timber", "wood pile", "lumber yard", "boards", "building supplies", "sawmill"])
def _(S):
    k = 0 if S.name == "line" else 2
    return [
        shell(rect(3, 3, 18, 4, k)),
        shell(rect(3, 10, 18, 4, k)),
        shell(rect(3, 17, 18, 4, k)),
        detail(seg(12, 3, 12, 7)),
        detail(seg(8, 10, 8, 14)),
        detail(seg(16, 10, 16, 14)),
        detail(seg(12, 17, 12, 21)),
    ]


@icon("wood-plank", CAT, "Long board running diagonally with two grain lines",
      tags=["board", "lumber", "timber", "carpentry", "wood", "floorboard"])
def _(S):
    return [
        shell(rp([(9, 0.5), (15, 0.5), (15, 23.5), (9, 23.5)], r=S.r * 0.5 if False else 0)),
        detail(rseg(12, 4, 12, 11.5)),
        detail(rseg(12, 14, 12, 20)),
    ]


@icon("plywood-sheet", CAT, "Thick flat sheet at an angle with a layered edge",
      tags=["wood panel", "board", "osb", "laminate", "sheet goods", "carpentry"])
def _(S):
    return [
        shell(poly([(2, 9), (12, 5), (22, 9), (22, 16), (12, 20), (2, 16)], closed=True, r=S.r * 0.5)),
        detail(poly([(2, 9), (12, 13), (22, 9)])),
        detail(poly([(2, 12.5), (12, 16.5), (22, 12.5)])),
        detail(seg(12, 13, 12, 20)),
    ]


@icon("wooden-beam", CAT, "Square timber beam in perspective with a knot on its end",
      tags=["timber", "joist", "lumber", "post", "carpentry", "structural wood"])
def _(S):
    face = [(3, 12), (11, 12), (11, 20), (3, 20)]
    return [
        shell(prism(face, (9, -9))),
        detail(poly([(3, 12), (11, 12), (11, 20)])),
        detail(seg(11, 12, 20, 3)),
        dot(7, 16, 1.25),
    ]


@icon("steel-i-beam", CAT, "Steel beam with an I shaped end profile in perspective",
      tags=["girder", "structural steel", "h-beam", "construction", "iron", "building frame"])
def _(S):
    face = [(2, 11), (13, 11), (13, 14), (9.5, 14), (9.5, 19), (13, 19), (13, 22), (2, 22), (2, 19), (5.5, 19), (5.5, 14), (2, 14)]
    return [
        shell(prism(face, (8, -8))),
        detail(poly(face, closed=True)),
    ]


@icon("angle-iron", CAT, "Long steel bar with an L shaped end profile in perspective",
      tags=["steel angle", "l-bar", "structural steel", "metal stock", "bracket", "fabrication"])
def _(S):
    face = [(2, 10), (6, 10), (6, 18), (14, 18), (14, 22), (2, 22)]
    return [
        shell(prism(face, (6, -6))),
        detail(poly(face, closed=True)),
        detail(seg(6, 18, 12, 12)),
        detail(seg(12, 12, 20, 12)),
    ]


@icon("c-channel", CAT, "Long steel bar with a C shaped end profile in perspective",
      tags=["steel channel", "u-channel", "structural steel", "metal stock", "strut", "fabrication"])
def _(S):
    face = [(2, 10), (14, 10), (14, 14), (6, 14), (6, 18), (14, 18), (14, 22), (2, 22)]
    return [
        shell(prism(face, (6, -6))),
        detail(poly(face, closed=True)),
    ]


@icon("square-tubing", CAT, "Short length of hollow square steel tube in perspective",
      tags=["box section", "hollow section", "steel tube", "metal stock", "fabrication", "frame"])
def _(S):
    face = [(2, 11), (13, 11), (13, 22), (2, 22)]
    return [
        shell(prism(face, (8, -8))),
        detail(poly(face, closed=True)),
        detail(poly([(5.5, 14.5), (9.5, 14.5), (9.5, 18.5), (5.5, 18.5)], closed=True)),
    ]


@icon("rebar", CAT, "Two crossing ribbed steel bars tied together with a wire twist",
      tags=["reinforcing bar", "reinforcement", "concrete", "steel rod", "construction", "tie wire"])
def _(S):
    k = 0 if S.name == "line" else 1.5
    return [
        shell(rp([(1, 9.5), (9.5, 9.5), (9.5, 13.5), (1, 13.5)], closed=True, r=k)),
        shell(rp([(14.5, 9.5), (23, 9.5), (23, 13.5), (14.5, 13.5)], closed=True, r=k)),
        shell(rp([(9.5, 1), (14.5, 1), (14.5, 23), (9.5, 23)], closed=True, r=k)),
        detail(rseg(5, 9.5, 5, 13.5)),
        detail(rseg(19, 9.5, 19, 13.5)),
        detail(rseg(9.5, 5.5, 14.5, 5.5)),
        detail(rseg(9.5, 18.5, 14.5, 18.5)),
        dot(12, 11.5, 1.25),
    ]


@icon("wire-mesh", CAT, "Square grid of welded wires seen at a slight angle",
      tags=["welded wire", "reinforcing mesh", "screen", "grid", "fencing", "construction"])
def _(S):
    parts = []
    for i in range(4):
        parts.append(line(seg(6 + 5.333 * i, 3, 2 + 5.333 * i, 21)))
    for y in (3, 9, 15, 21):
        x0 = 6 - 4 * (y - 3) / 18
        parts.append(line(seg(x0, y, x0 + 16, y)))
    return parts


@icon("cinder-block", CAT, "Concrete block seen from above with two large square holes",
      tags=["concrete block", "cmu", "masonry", "building block", "wall", "construction"])
def _(S):
    return [
        shell(rect(2, 5, 20, 14, rr(S, 3))),
        detail(rect(5.5, 9, 4.5, 6)),
        detail(rect(14, 9, 4.5, 6)),
    ]


@icon("single-brick", CAT, "One brick in perspective with three holes in its top face",
      tags=["clay brick", "masonry", "bricklayer", "building", "wall", "construction"])
def _(S):
    face = [(2, 13), (17, 13), (17, 21), (2, 21)]
    return [
        shell(prism(face, (5, -5))),
        detail(poly([(2, 13), (17, 13), (17, 21)])),
        detail(seg(17, 13, 22, 8)),
        dot(8.5, 10.5, 1.1),
        dot(12, 10.5, 1.1),
        dot(15.5, 10.5, 1.1),
    ]


@icon("cement-bag", CAT, "Paper sack with a folded top and a small heap of powder beside it",
      tags=["concrete mix", "mortar", "sack", "powder", "building supplies", "construction"])
def _(S):
    return [
        shell(poly([(4.5, 5), (15.5, 5), (16.5, 21), (3.5, 21)], closed=True, r=S.r * 0.6)),
        detail(poly([(4.5, 5), (7, 9), (13, 9), (15.5, 5)])),
        shell("M17.5 21Q19.75 13.5 22 21Z"),
    ]


@icon("concrete-slab", CAT, "Thick concrete slab in perspective with rebar ends sticking out of its side",
      tags=["foundation", "pad", "floor slab", "reinforced concrete", "construction", "rebar"])
def _(S):
    face = [(2, 12), (13, 12), (13, 19), (2, 19)]
    return [
        shell(prism(face, (5, -5))),
        detail(poly([(2, 12), (13, 12), (13, 19)])),
        detail(seg(13, 12, 18, 7)),
        line(seg(16, 11.5, 22, 11.5)),
        line(seg(16, 15, 22, 15)),
    ]


@icon("roof-shingles", CAT, "Rows of square shingle tabs with slits, each row offset from the last",
      tags=["asphalt shingles", "roofing", "roof covering", "tabs", "house", "construction"])
def _(S):
    parts = []
    rows = [(9, (8.67, 15.33)), (15, (5.33, 12, 18.67)), (21, (8.67, 15.33))]
    for y, xs in rows:
        parts.append(line(seg(2, y, 22, y)))
        for x in xs:
            parts.append(line(seg(x, y - 4.5, x, y)))
    parts.append(line(seg(2, 3, 22, 3)))
    return parts


@icon("roof-tiles", CAT, "Rows of overlapping curved clay roof tiles with wavy edges",
      tags=["clay tile", "terracotta", "spanish tile", "roofing", "barrel tile", "house"])
def _(S):
    return [
        line("M2 6q3.5 4 7 0t7 0t6 0"),
        line("M2 12q3.5 4 7 0t7 0t6 0"),
        line("M2 18q3.5 4 7 0t7 0t6 0"),
        line(seg(9, 6, 9, 9.5)) if False else line(seg(2, 2.5, 22, 2.5)),
    ]


@icon("drywall-sheet", CAT, "Large thin wallboard panel in perspective with a taped seam",
      tags=["gypsum board", "plasterboard", "sheetrock", "wall panel", "interior", "construction"])
def _(S):
    face = [(3, 5), (17, 5), (17, 22), (3, 22)]
    return [
        shell(prism(face, (4, -2.5))),
        detail(poly([(3, 5), (17, 5), (17, 22)])),
        detail(seg(17, 5, 21, 2.5)),
        detail(seg(10, 5, 10, 22)),
        Part("dot", circle(6.5, 10, 1.0)) if S.name == "rounded" else sq(5, 8.5, 3, 3),
        Part("dot", circle(13.5, 10, 1.0)) if S.name == "rounded" else sq(12, 8.5, 3, 3),
    ]


@icon("insulation-roll", CAT, "Roll of fluffy insulation batting partly unrolled with a wavy top edge",
      tags=["fiberglass", "thermal insulation", "batting", "attic", "energy saving", "building"])
def _(S):
    return [
        shell("M8 6Q11.5 3 15 6T22 6V18H8"),
        shell(circle(8, 12, 6)),
        detail(circle(8, 12, 2.2)),
    ]


@icon("floor-tiles", CAT, "Grid of square floor tiles in perspective with grout lines",
      tags=["tiling", "ceramic tile", "grout", "flooring", "bathroom", "kitchen"])
def _(S):
    def xl(y):
        return 6 - 4 * (y - 4) / 16

    def xr(y):
        return 18 + 4 * (y - 4) / 16
    return [
        shell(poly([(6, 4), (18, 4), (22, 20), (2, 20)], closed=True, r=S.r * 0.6)),
        detail(seg(xl(9), 9, xr(9), 9)),
        detail(seg(xl(14.5), 14.5, xr(14.5), 14.5)),
        detail(seg(10, 4, 8.67, 20)),
        detail(seg(14, 4, 15.33, 20)),
    ]


@icon("paving-stones", CAT, "Interlocking pavers laid in staggered rows in perspective",
      tags=["pavers", "patio", "driveway", "brick paving", "landscaping", "hardscape"])
def _(S):
    def xl(y):
        return 6 - 4 * (y - 4) / 16

    def xr(y):
        return 18 + 4 * (y - 4) / 16

    def at(y, f):
        return xl(y) + f * (xr(y) - xl(y))
    parts = [shell(poly([(6, 4), (18, 4), (22, 20), (2, 20)], closed=True, r=S.r * 0.6)),
             detail(seg(xl(9), 9, xr(9), 9)), detail(seg(xl(14.5), 14.5, xr(14.5), 14.5))]
    for y0, y1, fs in ((4, 9, (0.5,)), (9, 14.5, (0.25, 0.75)), (14.5, 20, (0.5,))):
        for f in fs:
            parts.append(detail(seg(at(y0, f), y0, at(y1, f), y1)))
    return parts


@icon("gravel-pile", CAT, "Heap of small stones in a mound",
      tags=["crushed stone", "aggregate", "rocks", "landscaping", "driveway", "construction material"])
def _(S):
    return [
        shell("M2 21Q6 21 8 14Q10 8 12 8Q14 8 16 14Q18 21 22 21Z" if S.name == "line" else
              "M2 21Q6 21 8 14Q10 8 12 8Q14 8 16 14Q18 21 22 21Z"),
        dot(8.5, 18, 1.2),
        dot(15.5, 18, 1.2),
        dot(12, 14, 1.2),
    ]


@icon("corrugated-sheet", CAT, "Wavy sheet metal panel with parallel ridges",
      tags=["corrugated iron", "roofing sheet", "metal panel", "galvanized", "cladding", "shed"])
def _(S):
    return [
        shell("M3 6q3-3 6 0t6 0t6 0V18q-3-3-6 0t-6 0t-6 0Z"),
        detail(seg(6, 4.5, 6, 16.5)),
        detail(seg(12, 7.5, 12, 19.5)),
        detail(seg(18, 4.5, 18, 16.5)),
    ]


@icon("roof-truss", CAT, "Triangular timber truss with a king post and two diagonal struts",
      tags=["rafters", "roof frame", "timber frame", "carpentry", "structure", "building"])
def _(S):
    return [
        line(poly([(3, 19), (12, 5.5), (21, 19)], closed=True, r=S.r)),
        line(seg(12, 5.5, 12, 19)),
        line(seg(12, 19, 7.2, 12.3)),
        line(seg(12, 19, 16.8, 12.3)),
    ]


@icon("wall-framing", CAT, "Stud wall frame with a top plate, bottom plate and evenly spaced studs",
      tags=["studs", "carpentry", "2x4", "house framing", "timber frame", "construction"])
def _(S):
    parts = [line(seg(2, 4, 22, 4)), line(seg(2, 20, 22, 20))]
    for x in (4.5, 9.5, 14.5, 19.5):
        parts.append(line(seg(x, 4, x, 20)))
    return parts


@icon("house-frame", CAT, "House outline built of bare studs and roof rafters",
      tags=["framing", "home construction", "building a house", "carpentry", "studs", "rafters"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 11), (12, 3), (21, 11), (21, 21)], closed=True, r=S.r)),
        detail(seg(8, 21, 8, 8)),
        detail(seg(12, 21, 12, 4)),
        detail(seg(16, 21, 16, 8)),
    ]


@icon("floor-joists", CAT, "Row of parallel joists resting on a sill beam and tied by a rim board",
      tags=["floor framing", "beams", "subfloor", "carpentry", "house frame", "timber"])
def _(S):
    parts = [shell(rect(2, 17, 20, 4, rr(S, 2)))]
    for i in range(4):
        x = 3.5 + 5 * i
        parts.append(line(seg(x, 17, x + 3, 5)))
    parts.append(line(seg(6.5, 5, 21.5, 5)))
    return parts


@icon("wooden-log", CAT, "Short round log lying on its side with bark lines and an end ring",
      tags=["firewood", "timber", "trunk", "lumber", "forestry", "campfire"])
def _(S):
    return [
        shell("M19 5H7A3 7 0 0 0 7 19H19A3 7 0 0 0 19 5Z"),
        detail("M19 5A3 7 0 0 0 19 19"),
        dot(19, 12, 1.25),
        detail(seg(7, 9.5, 12, 9.5)),
        detail(seg(7, 14.5, 12, 14.5)),
    ]


@icon("pallet", CAT, "Wooden shipping pallet seen from the side with three block supports",
      tags=["skid", "shipping", "warehouse", "freight", "forklift", "logistics"])
def _(S):
    k = rr(S, 1.5) if S.name == "rounded" else 0
    return [
        shell(rect(2, 4, 20, 3, k)),
        shell(rect(2, 17, 20, 3, k)),
        shell(rect(2, 7, 2.5, 10)),
        shell(rect(10.75, 7, 2.5, 10)),
        shell(rect(19.5, 7, 2.5, 10)),
    ]


@icon("sheet-metal-roll", CAT, "Coil of sheet metal with the loose end curling away along the ground",
      tags=["steel coil", "metal stock", "flashing", "aluminum roll", "fabrication", "hvac"])
def _(S):
    return [
        shell(circle(9, 11, 7)),
        detail(circle(9, 11, 3.2)),
        line("M9 18H19Q22 18 22 14.5"),
    ]


@icon("stone-wall", CAT, "Wall of irregular fitted stones with rounded corners",
      tags=["masonry", "rubble wall", "garden wall", "rock wall", "cobblestone", "landscaping"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, rr(S, 4))),
        detail(poly([(2, 9), (8, 9.5), (14, 8.5), (22, 9)])),
        detail(poly([(2, 15), (9, 15.5), (15, 14.5), (22, 15)])),
        detail(seg(8, 9.5, 7, 3)),
        detail(seg(15, 8.5, 16, 3)),
        detail(seg(5.5, 15.2, 5, 9.2)),
        detail(seg(12, 9, 12, 15)),
        detail(seg(18.5, 14.7, 18, 9)),
        detail(seg(9, 15.5, 10, 21)),
        detail(seg(15, 14.5, 16, 21)),
    ]


@icon("concrete-column", CAT, "Round concrete column with reinforcing bars poking out of the top",
      tags=["pillar", "pier", "rebar", "reinforced concrete", "structure", "building"])
def _(S):
    return [
        shell("M5 9.5V21.5H19V9.5A7 2.2 0 0 0 5 9.5Z"),
        detail("M5 9.5A7 2.2 0 0 0 19 9.5"),
        line(seg(8, 2.5, 8, 9)),
        line(seg(12, 2.5, 12, 9)),
        line(seg(16, 2.5, 16, 9)),
    ]


@icon("siding-panels", CAT, "Wall section of horizontal overlapping lap siding boards",
      tags=["cladding", "weatherboard", "clapboard", "exterior wall", "vinyl siding", "house"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, rr(S, 3))),
        detail(seg(2, 8.5, 22, 8.5)),
        detail(seg(2, 13, 22, 13)),
        detail(seg(2, 17.5, 22, 17.5)),
    ]


@icon("chain-link-fence", CAT, "Fence section with a diamond mesh between two posts and a top rail",
      tags=["wire fence", "cyclone fence", "security fence", "perimeter", "yard", "boundary"])
def _(S):
    parts = [line(seg(3, 2.5, 3, 22)), line(seg(21, 2.5, 21, 22)), line(seg(3, 5, 21, 5))]
    for d in diag_lines(3, 5, 21, 21, 6):
        parts.append(line(d))
    return parts


@icon("barbed-wire", CAT, "Wire strand with two sets of crossed barbs",
      tags=["razor wire", "fence", "security", "boundary", "farm", "prison"])
def _(S):
    return [
        line(seg(2, 12, 22, 12)),
        line(seg(4.5, 8, 9.5, 16)),
        line(seg(4.5, 16, 9.5, 8)),
        line(seg(14.5, 8, 19.5, 16)),
        line(seg(14.5, 16, 19.5, 8)),
    ]


@icon("vapor-barrier-roll", CAT, "Roll of thin plastic sheeting lying on its side with a wavy loose sheet hanging down",
      tags=["plastic sheeting", "moisture barrier", "poly sheet", "underlayment", "crawl space", "building wrap"])
def _(S):
    return [
        shell("M19 3H7A3 4 0 0 0 7 11H19A3 4 0 0 0 19 3Z"),
        detail(ellipse(7, 7, 3, 4)) if False else detail("M7 3A3 4 0 0 1 7 11"),
        shell("M9 11V17q2.5 3 5 0t5 0V11"),
    ]


@icon("tar-paper-roll", CAT, "Roll of roofing felt standing on end with the sheet unrolled flat beside it",
      tags=["roofing felt", "underlayment", "building paper", "asphalt paper", "roofing", "construction"])
def _(S):
    return [
        shell("M2 5A4.5 2 0 0 1 11 5V14A4.5 2 0 0 1 2 14Z"),
        detail("M2 5A4.5 2 0 0 0 11 5"),
        shell(poly([(8, 17.5), (22, 17.5), (22, 21), (8, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(8, 19.25, 22, 19.25)) if False else dot(18.5, 19.25, 0.9),
    ]


@icon("rain-gutter", CAT, "Half round gutter along the roof edge with a downspout pipe going down and rain falling in",
      tags=["eavestrough", "downspout", "drainage", "roof edge", "rainwater", "house"])
def _(S):
    return [
        line(seg(6, 2, 6, 4)),
        line(seg(11, 2, 11, 4)),
        shell(rect(2, 6.5, 20, 5, rr(S, 3))),
        detail(seg(5, 9, 15, 9)),
        shell(rect(17, 11.5, 4, 8, rr(S, 1.5))),
        line(poly([(19, 19.5), (19, 21.5), (22, 21.5)], r=S.r)),
    ]


@icon("skylight", CAT, "Sloped roof plane with a glass window set into it",
      tags=["roof window", "rooflight", "attic window", "daylight", "glazing", "roofing"])
def _(S):
    return [
        shell(poly([(2, 20), (6, 4), (22, 4), (18, 20)], closed=True, r=S.r * 0.6)),
        detail(poly([(8, 15), (10.5, 8.5), (17.5, 8.5), (15, 15)], closed=True)),
        detail(seg(12.75, 8.5, 12.25, 15)),
    ]


@icon("staircase-stringer", CAT, "Notched diagonal board cut in steps to carry stair treads",
      tags=["stair", "stairs", "carriage", "carpentry", "framing", "steps"])
def _(S):
    return [
        shell(poly([(3, 17), (8, 17), (8, 13), (13, 13), (13, 9), (18, 9), (18, 5), (22, 5), (22, 11), (3, 22)], closed=True, r=S.r * 0.5)),
    ]


@icon("expansion-joint", CAT, "Two concrete slabs with a gap between them filled with a wavy strip",
      tags=["control joint", "concrete", "slab", "sealant", "gap filler", "pavement"])
def _(S):
    return [
        shell(rect(2, 4, 6, 16, rr(S, 2))),
        shell(rect(16, 4, 6, 16, rr(S, 2))),
        line("M12 4q1.5 2.5 0 4t0 4t0 4t0 4"),
    ]


@icon("notched-trowel", CAT, "Flat trowel blade with square notches along its lower edge and a top handle",
      tags=["tile adhesive", "thinset", "comb trowel", "tiling", "spreader", "flooring"])
def _(S):
    return [
        shell(poly([(2, 11), (22, 11), (22, 20), (19.5, 20), (19.5, 17), (16.5, 17), (16.5, 20), (13.5, 20),
                    (13.5, 17), (10.5, 17), (10.5, 20), (7.5, 20), (7.5, 17), (4.5, 17), (4.5, 20), (2, 20)],
                   closed=True, r=S.r * 0.3)),
        line(seg(12, 11, 12, 6)),
        shell(rect(8.5, 2.5, 7, 3.5, rr(S, 1.75))),
    ]


@icon("grout-float", CAT, "Rectangular rubber float pad with a loop handle on top",
      tags=["tiling", "grouting", "tile tool", "rubber float", "bathroom", "finishing"])
def _(S):
    return [
        shell(rect(2, 14, 20, 6, rr(S, 3))),
        line(poly([(7.5, 14), (7.5, 7), (16.5, 7), (16.5, 14)], r=S.r)),
    ]


@icon("bull-float", CAT, "Wide flat blade at the end of a very long pole lying at an angle",
      tags=["concrete finishing", "smoothing", "slab", "concrete tool", "float", "screed"])
def _(S):
    return [
        shell(rect(2, 16.5, 16, 4, rr(S, 2))),
        line(seg(10, 16.5, 21, 3)),
        line(seg(7, 16.5, 7, 14)) if False else line(seg(12, 16.5, 8, 13.5)),
    ]


@icon("plastering-hawk", CAT, "Square hawk board with a short grip underneath and a mound of plaster on top",
      tags=["plasterer", "mortar board", "stucco", "render", "finishing", "trowel"])
def _(S):
    return [
        shell("M6 10Q8 4.5 12 4.5Q16 4.5 18 10"),
        shell(rect(2, 10, 20, 3.5, rk(S, 1.75))),
        line(seg(12, 13.5, 12, 16.5)),
        shell(rect(9.5, 16.5, 5, 5, rk(S, 2))),
    ]


@icon("mortar-tub", CAT, "Wide shallow tub with sloped sides and a mixing hoe resting inside",
      tags=["mixing tub", "cement", "plaster", "mud tub", "masonry", "bricklayer"])
def _(S):
    return [
        shell(poly([(2, 11), (22, 11), (19, 21), (5, 21)], closed=True, r=S.r)),
        line(seg(20, 2.5, 11, 15)),
        line(seg(8.6, 13.3, 13.4, 16.7)),
    ]


def _mixer_drum(deg=-30):
    def pt(p):
        q = rot([p], deg)[0]
        return f"{fmt(q[0])} {fmt(q[1])}"
    return ("M" + pt((9, 3)) + "L" + pt((15, 3)) + "L" + pt((19.5, 10)) + "Q" + pt((19.5, 16.5)) + " " + pt((14, 16.5))
            + "L" + pt((10, 16.5)) + "Q" + pt((4.5, 16.5)) + " " + pt((4.5, 10)) + "Z")


@icon("concrete-mixer", CAT, "Tilted rotating drum on a small wheeled stand",
      tags=["cement mixer", "portable mixer", "concrete", "mortar", "building site", "construction"])
def _(S):
    return [
        shell(_mixer_drum()),
        detail(rseg(9.6, 5.5, 14.4, 5.5, -30)),
        line(seg(12, 13, 8, 20)),
        line(seg(12, 13, 17, 20)),
        dot(8, 20.5, 1.6),
        dot(17, 20.5, 1.6),
    ]


@icon("tile-spacer", CAT, "Small cross shaped spacer set between the corners of four tiles",
      tags=["tiling", "grout line", "tile gap", "spacers", "flooring", "bathroom"])
def _(S):
    return [
        shell(rect(3, 3, 6, 6, rk(S, 1.5))),
        shell(rect(15, 3, 6, 6, rk(S, 1.5))),
        shell(rect(3, 15, 6, 6, rk(S, 1.5))),
        shell(rect(15, 15, 6, 6, rk(S, 1.5))),
        solid(poly([(10.75, 7), (13.25, 7), (13.25, 10.75), (17, 10.75), (17, 13.25), (13.25, 13.25),
                    (13.25, 17), (10.75, 17), (10.75, 13.25), (7, 13.25), (7, 10.75), (10.75, 10.75)], closed=True)),
    ]


@icon("brick-jointer", CAT, "S shaped steel bar with rounded ends for striking mortar joints",
      tags=["pointing tool", "jointing tool", "mortar", "bricklaying", "masonry", "tuckpointing"])
def _(S):
    return [
        line(poly([(3, 6.5), (8, 6.5), (11, 9), (11, 15), (14, 17.5), (21, 17.5)], r=S.r)),
        dot(2.5, 6.5, 1.75),
        dot(21.5, 17.5, 1.75),
    ]


@icon("masonry-line-blocks", CAT, "Two small line blocks on brick corners with a taut string between them",
      tags=["string line", "brick laying", "bricklayer", "alignment", "corner blocks", "masonry"])
def _(S):
    return [
        shell(rect(2, 14.5, 7, 6, rk(S, 1.5))),
        shell(rect(15, 14.5, 7, 6, rk(S, 1.5))),
        shell(rect(3.5, 8, 4, 5.5, rk(S, 1))),
        shell(rect(16.5, 8, 4, 5.5, rk(S, 1))),
        line(seg(7.5, 10.75, 16.5, 10.75)),
    ]


@icon("drywall-t-square", CAT, "Long T shaped ruler with a crossbar at the top and tick marks on the blade",
      tags=["t-square", "straightedge", "drywall", "cutting guide", "ruler", "plasterboard"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 3.5, rr(S, 1.75))),
        shell(rect(9.5, 6, 5, 16)),
        detail(seg(9.5, 10, 12.5, 10)),
        detail(seg(9.5, 14, 12.5, 14)),
        detail(seg(9.5, 18, 12.5, 18)),
    ]


@icon("mud-pan", CAT, "Long narrow pan with sloped ends and a taping knife lying across it",
      tags=["joint compound", "taping knife", "drywall", "plastering", "finishing", "hawk"])
def _(S):
    def sh(pts, dx, dy):
        return [(x + dx, y + dy) for x, y in pts]
    blade = sh(rot([(9.5, 2), (14.5, 2), (14.5, 9), (9.5, 9)], 65), -1, -2)
    grip = sh(rot([(10.5, 9), (13.5, 9), (13.5, 15), (10.5, 15)], 65), -1, -2)
    return [
        shell(poly([(2, 14), (22, 14), (19, 21), (5, 21)], closed=True, r=S.r * 0.6)),
        shell(poly(blade, closed=True)),
        shell(poly(grip, closed=True, r=S.r * 0.3)),
    ]


@icon("wallpaper-brush", CAT, "Wide flat smoothing brush with a ferrule, a bristle block and a bar handle",
      tags=["wallpapering", "paste brush", "smoothing brush", "decorating", "wall covering", "diy"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 3, rk(S, 1.5))),
        line(seg(12, 5.5, 12, 9)),
        shell(rect(3, 9, 18, 12)),
        detail(seg(3, 12.5, 21, 12.5)),
        detail(seg(8, 12.5, 8, 21)),
        detail(seg(12, 12.5, 12, 21)),
        detail(seg(16, 12.5, 16, 21)),
    ]


@icon("drop-cloth", CAT, "Fabric dust sheet with a wavy edge, a fold line and a few paint spots",
      tags=["painter", "dust sheet", "protective sheet", "paint cover", "decorating", "renovation"])
def _(S):
    return [
        shell("M3 5Q7 3 12 5T21 5V19Q17 21 12 19T3 19Z"),
        detail(seg(3, 11.5, 21, 11.5)),
        dot(8, 15.5, 1.2),
        dot(15.5, 8, 1.2),
        dot(16.5, 16, 1.2),
    ]


@icon("power-trowel", CAT, "Machine with a round blade ring on the ground, a motor and a long handle",
      tags=["concrete finishing", "helicopter trowel", "slab finishing", "screed", "floor machine", "construction"])
def _(S):
    return [
        shell(ellipse(12, 18.5, 9, 3)),
        detail(seg(6, 17, 18, 20)),
        shell(rect(8.5, 6, 7, 7, rr(S, 2))),
        line(seg(12, 13, 12, 16)),
        line(seg(15.5, 8, 21.5, 2.5)),
    ]


@icon("plate-compactor", CAT, "Flat steel base plate carrying an engine with a long handle behind",
      tags=["wacker plate", "vibratory plate", "soil compaction", "paving", "groundwork", "landscaping"])
def _(S):
    return [
        shell(rect(2, 17.5, 16, 3.5, rr(S, 1.75))),
        shell(rect(5, 8.5, 9, 8, rr(S, 2))),
        line(seg(14, 12, 21.5, 3)),
        line(seg(18.5, 2.5, 22, 5.5)) if False else line(seg(19, 4.8, 22, 7.2)),
    ]


@icon("concrete-vibrator", CAT, "Motor unit with a long flexible hose ending in a metal probe",
      tags=["poker vibrator", "concrete", "compaction", "pouring", "formwork", "construction"])
def _(S):
    return [
        shell(rect(2, 2.5, 7, 7, rr(S, 2))),
        line("M9 6H14Q19 6 19 11V14"),
        shell(poly([(17, 14), (21, 14), (21, 19), (19, 22), (17, 19)], closed=True, r=S.r * 0.4)),
    ]


@icon("rebar-tie-tool", CAT, "Long handled pliers turned on the diagonal with a spool of tie wire at the jaws",
      tags=["rebar tying", "tie wire", "reinforcing steel", "concrete work", "twist tool", "construction"])
def _(S):
    c = rot([(12, 5)], 45, 12, 12)[0]
    return [
        line(rp([(7.5, 21), (12, 14), (10.9, 9.5)], closed=False, r=S.r, deg=45)),
        line(rp([(16.5, 21), (12, 14), (13.1, 9.5)], closed=False, r=S.r, deg=45)),
        Part("dot", circle(*rot([(12, 14)], 45)[0], 1.3)),
        shell(circle(c[0], c[1], 3)),
    ]
