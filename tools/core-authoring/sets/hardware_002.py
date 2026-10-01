"""TypeIcon Core: hardware (batch 002): workshop power tools, torches, drill bits, discs, clamps and gauges.

Drawn from the objects themselves. Handheld power tools and machines are shown in side view facing right.
Long slim tools (bits, pens, squares) follow the tools set: drawn upright and turned 45 degrees clockwise so
the handle points to the bottom-left and the working end to the top-right.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "hardware"
TILT = 45


# --------------------------------------------------------------------------- helpers

def rot(pts, deg=TILT, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rp(pts, closed=True, r=0.0, deg=TILT, c=(12.0, 12.0)):
    return poly(rot(pts, deg, *c), closed=closed, r=r)


def rpath(cmds, deg=TILT, c=(12.0, 12.0)) -> str:
    """Path from commands with rotated points: ("M", p) ("L", p) ("A", r, large, sweep, p) ("Q", c, p) ("C", c1, c2, p) ("Z",)."""
    out = []

    def pt(p):
        q = rot([p], deg, *c)[0]
        return f"{fmt(q[0])} {fmt(q[1])}"
    for k in cmds:
        op = k[0]
        if op in ("M", "L"):
            out.append(op + pt(k[1]))
        elif op == "A":
            out.append(f"A{fmt(k[1])} {fmt(k[1])} 0 {k[2]} {k[3]} " + pt(k[4]))
        elif op == "Q":
            out.append("Q" + pt(k[1]) + " " + pt(k[2]))
        elif op == "C":
            out.append("C" + pt(k[1]) + " " + pt(k[2]) + " " + pt(k[3]))
        elif op == "Z":
            out.append("Z")
    return "".join(out)


def rrect(x, y, w, h, rx=0.0, deg=TILT, c=(12.0, 12.0)) -> str:
    rx = max(0.0, min(rx, w / 2, h / 2))
    if rx == 0:
        return rp([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], deg=deg, c=c)
    return rpath([("M", (x + rx, y)), ("L", (x + w - rx, y)), ("A", rx, 0, 1, (x + w, y + rx)),
                  ("L", (x + w, y + h - rx)), ("A", rx, 0, 1, (x + w - rx, y + h)), ("L", (x + rx, y + h)),
                  ("A", rx, 0, 1, (x, y + h - rx)), ("L", (x, y + rx)), ("A", rx, 0, 1, (x + rx, y)), ("Z",)], deg, c)


def rseg(x1, y1, x2, y2, deg=TILT, c=(12.0, 12.0)) -> str:
    (a, b), (c2, d) = rot([(x1, y1), (x2, y2)], deg, *c)
    return seg(a, b, c2, d)


def rcircle(cx, cy, r, deg=TILT) -> str:
    (x, y), = rot([(cx, cy)], deg)
    return circle(x, y, r)


def rdot(cx, cy, r=1.25, deg=TILT) -> Part:
    (x, y), = rot([(cx, cy)], deg)
    return dot(x, y, r)


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds) -> str:
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs) -> str:
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def mark(d) -> Part:
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def _loops(x0, x1, y, n, amp):
    """Prolate trochoid: a row of n curly loops from x0 to x1 (centre line y)."""
    pts = []
    steps = n * 10
    for i in range(steps + 1):
        t = 2 * math.pi * n * i / steps
        pts.append((x0 + (x1 - x0) * i / steps - amp * 1.25 * math.sin(t), y - amp * math.cos(t)))
    return "M" + "L".join(f"{fmt(a)} {fmt(b)}" for a, b in pts)


# ============================================================================ hand-held guns and torches

@icon("cats-paw-nail-puller", CAT, "Cat's paw nail puller: a short steel bar with a curled claw at one end",
      tags=["nail puller", "pry bar", "demolition", "remove nails", "carpentry", "claw"])
def _(S):
    claw = rpath([("M", (10.5, 20)), ("L", (10.5, 11)), ("Q", (10.5, 7.5), (6, 6)), ("Q", (13.5, 4.5), (13.5, 9)),
                  ("L", (13.5, 20)), ("Z",)])
    return [
        shell(claw, stroke_miterlimit="2"),
        rdot(12, 17),
    ]


@icon("staple-gun", CAT, "Staple gun: a boxy body with a hinged lever handle on top and a nose at the front",
      tags=["stapler", "upholstery", "fasten", "diy", "tacker", "craft"])
def _(S):
    return [
        shell(poly([(3.5, 8), (8, 4.5), (20.5, 4.5), (20.5, 12)], closed=True, r=S.r)),
        shell(poly([(3, 12), (21, 12), (21, 17), (9, 17), (9, 20.5), (3, 20.5)], closed=True, r=S.r * 0.6)),
        dot(6, 16.25, 1),
    ]


@icon("rivet-gun", CAT, "Hand riveter with two long handles and a pop rivet in its nose",
      tags=["pop rivet", "riveter", "fastening", "metalwork", "repair", "hand tool"])
def _(S):
    return [
        shell(rect(9, 6, 9, 6, rr(S, 2.5))),
        line(seg(18, 9, 22, 9)),
        line(poly([(10, 12), (9.5, 14), (4, 20.5)], r=S.r)),
        line(poly([(10.5, 6), (9, 4.5), (3, 4.5)], r=S.r)),
        line(seg(13.5, 12, 13.5, 14.5)),
    ]


@icon("caulking-gun", CAT, "Caulking gun: an open frame holding a sealant tube, with a trigger grip and plunger rod",
      tags=["caulk", "sealant", "silicone", "cartridge", "sealing", "bathroom", "diy"])
def _(S):
    return [
        shell(rect(6, 4.5, 11, 6.5, rr(S, 3))),
        shell(poly([(17, 6), (21.5, 7.75), (17, 9.5)], closed=True, r=S.r * 0.4)),
        line(seg(2, 7.75, 6, 7.75)),
        shell(poly([(7, 11), (11, 11), (10, 21), (5.5, 21)], closed=True, r=S.r)),
        line(poly([(14, 11), (14, 14.5), (12.75, 17)], r=S.r * 0.5)),
    ]


@icon("grease-gun", CAT, "Grease gun: a cylinder barrel with a pistol grip, a trigger lever and a thin bent nozzle",
      tags=["lubrication", "grease", "zerk fitting", "mechanic", "maintenance", "lube"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 13, 7.5, rr(S, 3))),
        shell(poly([(6, 12), (10.5, 12), (9.5, 20.5), (5.5, 20.5)], closed=True, r=S.r)),
        line(poly([(12.5, 12), (12.5, 15.5), (11, 17.5)], r=S.r * 0.5)),
        line(poly([(15.5, 8.25), (19.5, 8.25), (19.5, 12.5)], r=S.r * 0.5)),
        solid(rect(18, 13.5, 3.5, 3)),
    ]


@icon("hot-glue-gun", CAT, "Pistol-shaped hot glue gun with a cone nozzle at the front and a glue stick at the back",
      tags=["glue gun", "craft", "adhesive", "hot melt", "diy", "crafting", "bonding"])
def _(S):
    body = poly([(6.5, 5), (15, 5), (17, 7), (17, 11), (13.5, 11), (12, 20.5), (8, 20.5), (9.5, 11), (6.5, 11)], closed=True, r=S.r)
    return [
        shell(body),
        line(seg(2, 8, 6.5, 8)),
        shell(poly([(17, 6.5), (22, 8), (17, 9.5)], closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        line(poly([(14, 13), (16.5, 14)], r=0)),
    ]


@icon("soldering-iron", CAT, "Soldering iron: a cushioned grip, a slim shaft and a fine pointed tip, with a cord",
      tags=["solder", "electronics", "circuit repair", "tip", "pcb", "hand tool", "workbench"])
def _(S):
    return [
        solid(rp([(10.5, 8), (12, 2.5), (13.5, 8)])),
        line(rseg(12, 8, 12, 11)),
        shell(rrect(9, 11, 6, 9.5, rr(S, 3))),
        detail(rseg(9, 14.5, 15, 14.5)),
        line(rpath([("M", (12, 20.5)), ("Q", (12, 22.5), (15.5, 22.5))])),
    ]


@icon("soldering-station", CAT, "Soldering station: a base unit with a dial and a soldering iron resting above it",
      tags=["solder", "electronics", "workbench", "rework", "stand", "temperature control"])
def _(S):
    return [
        shell(rect(2.5, 14.5, 19, 7, rr(S, 2.5))),
        dot(7.5, 18, 1.5),
        detail(seg(12, 18, 18, 18)),
        shell(rect(2.5, 5, 7, 4.5, rr(S, 2))),
        line(seg(9.5, 7.25, 16, 7.25)),
        solid(poly([(16, 5.5), (21.5, 7.25), (16, 9)])),
    ]


@icon("solder-wire-spool", CAT, "Small spool wound with thin solder wire and a loose end trailing off",
      tags=["solder", "wire", "reel", "electronics", "tin", "soldering supplies"])
def _(S):
    hub = circle(10, 10, 1.25) if S.name == "rounded" else rect(8.75, 8.75, 2.5, 2.5)
    return [
        shell(circle(10, 10, 8)),
        detail(circle(10, 10, 4.5)),
        mark(hub),
        line(poly([(16, 15.5), (18, 19), (22, 19)], r=S.r)),
    ]


@icon("heat-gun", CAT, "Heat gun: a pistol-shaped tool with a wide nozzle and wavy heat lines",
      tags=["hot air", "paint stripper", "shrink wrap", "thermal", "heating tool", "electronics rework"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 12, 7, rr(S, 3))),
        shell(rect(14.5, 4, 3, 10, rr(S, 1))),
        shell(poly([(6, 12.5), (11, 12.5), (10, 20.5), (6.5, 20.5)], closed=True, r=S.r)),
        line("M19.5 6.5Q20.75 5 22 6.5"),
        line("M19.5 11.5Q20.75 10 22 11.5"),
    ]


@icon("blowtorch", CAT, "Fuel canister with a torch head on top and a flame coming out of the nozzle",
      tags=["torch", "propane", "flame", "plumbing", "brazing", "creme brulee", "heat"])
def _(S):
    return [
        shell(rect(5.5, 14, 13, 7, rr(S, 3))),
        shell(rect(10, 9.5, 4, 4.5, rr(S, 1))),
        shell("M12 3C13 5.5 16 6 16 7.5C16 9 14.5 9 12 9C9.5 9 8 9 8 7.5C8 6 11 5.5 12 3Z", stroke_miterlimit="2"),
    ]


@icon("cutting-torch", CAT, "Long torch handle with two hose valves at the back and a bent head with a flame",
      tags=["oxy acetylene", "gas torch", "metal cutting", "welding", "plasma", "fabrication"])
def _(S):
    return [
        shell(rect(2.5, 12.5, 14, 4, rr(S, 2))),
        line(seg(4.5, 12.5, 4.5, 8)),
        line(seg(3, 8, 6, 8)),
        line(seg(10.5, 12.5, 10.5, 8)),
        line(seg(9, 8, 12, 8)),
        line(poly([(16.5, 14.5), (20, 14.5), (20, 11)], r=S.r * 0.5)),
        shell("M20 3Q22.5 6 20 9Q17.5 6 20 3Z"),
    ]


# ============================================================================ spraying, sanding and finishing


@icon("welding-helmet", CAT, "Front view of a welding mask covering the whole face with a dark viewing window",
      tags=["welder", "mask", "face shield", "safety", "protective gear", "fabrication"])
def _(S):
    if S.name == "line":
        outline = "M5 10A7 7 0 0 1 19 10V18L15 21H9L5 18Z"
    else:
        outline = "M5 10A7 7 0 0 1 19 10V17Q19 21 14 21H10Q5 21 5 17Z"
    return [
        shell(outline, stroke_miterlimit="4"),
        mark(rect(8, 9, 8, 4, rr(S, 1))),
    ]


@icon("welding-rod", CAT, "Bundle of three thin straight rods with bare metal ends and coated bodies",
      tags=["electrode", "stick welding", "filler", "metalwork", "welder", "fabrication"])
def _(S):
    parts = []
    for cx, top in ((6.5, 4.5), (12, 3.5), (17.5, 4.5)):
        parts.append(line(rseg(cx, top, cx, 7.5)))
        parts.append(shell(rrect(cx - 2, 7.5, 4, 12, rr(S, 1.5))))
    return parts


@icon("oil-can", CAT, "Oil can with a thumb pump lever and a long thin spout pointing up",
      tags=["oiler", "lubricant", "lubricate", "squeaky", "maintenance", "machine oil"])
def _(S):
    body = poly([(3.5, 21), (3.5, 14.5), (6, 11.5), (12, 11.5), (14.5, 14.5), (14.5, 21)], closed=True, r=S.r)
    return [
        shell(body),
        line(poly([(3, 8), (10, 8), (10, 11.5)], r=S.r * 0.5)),
        line(seg(14, 14.5, 21.5, 6.5)),
        detail(seg(3.5, 17, 14.5, 17)),
    ]


@icon("lubricant-spray", CAT, "Spray can with a thin straw nozzle sticking out of the actuator at the top",
      tags=["penetrating oil", "aerosol", "silicone spray", "squeaky hinge", "maintenance", "can"])
def _(S):
    return [
        shell(rect(4.5, 9.5, 10, 11.5, rr(S, 3))),
        shell(rect(7.5, 6, 4, 3.5, rr(S, 1))),
        line(seg(11.5, 7.75, 21.5, 7.75)),
        detail(seg(4.5, 15, 14.5, 15)),
    ]


@icon("paint-sprayer", CAT, "Spray gun with a trigger handle, a paint cup underneath and a mist cone from the nozzle",
      tags=["spray gun", "airbrush", "painting", "coating", "finishing", "auto paint", "spray paint"])
def _(S):
    return [
        shell(rect(3, 4.5, 12, 6, rr(S, 2.5))),
        shell(poly([(15, 6), (17.5, 7.5), (15, 9)], closed=True, r=S.r * 0.3)),
        shell(poly([(3, 10.5), (7.5, 10.5), (6.5, 20), (3, 20)], closed=True, r=S.r)),
        shell(rect(10, 11, 6, 6.5, rr(S, 2))),
        dot(20, 7.5, 1),
        dot(21.5, 4.5, 1),
        dot(21.5, 10.5, 1),
    ]


@icon("paint-tray", CAT, "Side view of a roller tray with a sloped ribbed ramp dropping into a deeper paint well",
      tags=["roller tray", "painting", "paint roller", "decorating", "diy", "wall painting"])
def _(S):
    return [
        shell(poly([(2.5, 5), (5.5, 5), (15, 13.5), (21.5, 13.5), (21.5, 19), (2.5, 19)], closed=True, r=S.r * 0.6)),
        detail(seg(6.5, 15.5, 9.5, 12.5)),
        detail(seg(10.5, 16, 13, 13.75)),
    ]


@icon("sanding-block", CAT, "Rounded sanding pad with a handle hump on top and sandpaper wrapped on the bottom",
      tags=["sandpaper", "sander", "hand sanding", "woodworking", "smooth", "finishing", "abrasive"])
def _(S):
    return [
        shell(poly([(6, 11.5), (7, 6.5), (17, 6.5), (18, 11.5)], closed=True, r=S.r)),
        shell(rect(3, 11.5, 18, 5.5, rr(S, 2))),
        dot(5, 20.5, 1),
        dot(9.5, 20.5, 1),
        dot(14.5, 20.5, 1),
        dot(19, 20.5, 1),
    ]


@icon("steel-wool", CAT, "Rounded pad of tangled curly steel wool",
      tags=["wire wool", "scouring pad", "polishing", "abrasive", "cleaning", "finishing", "scrub"])
def _(S):
    return [
        shell(rect(3, 5.5, 18, 13, rr(S, 5))),
        detail(_loops(7, 17, 12, 3, 2.2)),
    ]


# ============================================================================ power tools: drills and saws


@icon("dust-brush", CAT, "Flat bench brush with a short handle and long bristles",
      tags=["bench brush", "sweep", "cleaning", "workshop", "sawdust", "debris", "hand brush"])
def _(S):
    return [
        shell(rect(7.5, 3, 9, 5, rr(S, 2.5))),
        shell(poly([(3.5, 11), (20.5, 11), (20.5, 21), (3.5, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(8, 14.5, 8, 21)),
        detail(seg(12, 14.5, 12, 21)),
        detail(seg(16, 14.5, 16, 21)),
        line(seg(12, 8, 12, 11)),
    ]


@icon("impact-driver", CAT, "Compact pistol-shaped impact driver with a short hex collet and a battery under the grip",
      tags=["cordless driver", "power tool", "drill driver", "screws", "fastening", "diy", "battery tool"])
def _(S):
    return [
        shell(rect(2.5, 4, 12.5, 7.5, rr(S, 3))),
        shell(rect(15, 5.75, 3, 4, rr(S, 1))),
        line(seg(18, 7.75, 22, 7.75)),
        shell(poly([(5.5, 11.5), (11, 11.5), (11, 17), (13.5, 17), (13.5, 21), (4, 21), (4, 17), (6, 17)], closed=True, r=S.r * 0.6)),
        detail(seg(6, 7.75, 11, 7.75)),
    ]


@icon("hammer-drill", CAT, "Pistol-shaped drill with a side handle below the chuck and a masonry bit",
      tags=["rotary hammer", "masonry drill", "concrete", "power tool", "drilling", "sds", "diy"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 12, 7, rr(S, 3))),
        shell(rect(14.5, 5, 3.5, 4.5, rr(S, 1))),
        line(seg(18, 7.25, 19.5, 7.25)),
        solid(poly([(19.5, 5), (22.5, 7.25), (19.5, 9.5)])),
        shell(poly([(4.5, 10.5), (9.5, 10.5), (9, 19), (5, 19)], closed=True, r=S.r)),
        line(seg(16, 10.5, 19.5, 17)),
        dot(20, 18, 1.75),
    ]


@icon("drill-press", CAT, "Drill press: a tall column on a heavy base with a table and a drill head on top",
      tags=["pillar drill", "bench drill", "machine tool", "workshop", "drilling", "woodworking", "metalworking"])
def _(S):
    return [
        line(seg(19, 3, 19, 19)),
        shell(rect(3.5, 3.5, 14, 6.5, rr(S, 2.5))),
        line(seg(9, 10, 9, 14)),
        line(seg(6.5, 16, 17, 16)),
        shell(rect(3, 19, 18, 2.5, rr(S, 1))),
    ]


@icon("circular-saw", CAT, "Handheld circular saw with a blade under a curved guard, a top handle and a base plate",
      tags=["power saw", "cutting wood", "carpentry", "woodworking", "construction", "rip cut"])
def _(S):
    return [
        shell("M3.5 12A8 8 0 0 1 19.5 12Z"),
        line(seg(2, 13.5, 22, 13.5)),
        line(arc(11.5, 12, 7, 20, 160)),
        line(poly([(16, 6.5), (18, 3.5), (21.5, 3.5), (21.5, 12)], r=S.r)),
    ]


@icon("power-jigsaw", CAT, "Power jigsaw in side view with a closed handle on top and a short blade under the shoe",
      tags=["jig saw", "scroll cutting", "curve cutting", "power tool", "woodworking", "saber"])
def _(S):
    return [
        shell(poly([(3.5, 10), (20.5, 10), (20.5, 14.5), (22, 14.5), (22, 18), (2, 18), (2, 14.5), (3.5, 14.5)], closed=True, r=S.r * 0.5)),
        line(poly([(5.5, 10), (5.5, 4), (18.5, 4), (18.5, 10)], r=S.r)),
        line(seg(11.5, 18, 11.5, 22)),
    ]


@icon("reciprocating-saw", CAT, "Long power saw with a rear grip and a straight blade sticking out of the front",
      tags=["demolition saw", "sabre saw", "power tool", "cutting", "plumbing", "renovation"])
def _(S):
    a = -20
    return [
        shell(rrect(3.5, 8.5, 11.5, 6, rr(S, 3), deg=a)),
        shell(rp([(5, 15.5), (9.5, 15.5), (9, 19.5), (5.5, 19.5)], r=S.r, deg=a)),
        line(rseg(17, 8, 17, 17, deg=a)),
        line(rseg(15, 12.5, 21, 12.5, deg=a)),
    ]


# ============================================================================ power tools: grinders, sanders, routers


@icon("miter-saw", CAT, "Circular saw blade on a pivoting arm above a base with a fence",
      tags=["mitre saw", "chop saw", "crosscut", "trim", "woodworking", "angle cut", "power tool"])
def _(S):
    hub = circle(10, 11, 1.25) if S.name == "rounded" else rect(9, 10, 2, 2)
    return [
        shell(circle(10, 11, 5.5)),
        mark(hub),
        line(poly([(14, 7), (18, 3.5), (21.5, 3.5)], r=S.r * 0.5)),
        shell(rect(2.5, 18, 19, 3, rr(S, 1))),
        line(seg(19, 18, 19, 11)),
    ]


@icon("table-saw", CAT, "Flat table top with a round blade poking up through the middle and a fence rail",
      tags=["bench saw", "cabinet saw", "rip fence", "woodworking", "workshop", "sawmill", "cutting"])
def _(S):
    return [
        line(arc(11, 11, 5.5, 185, 355)),
        shell(rect(2.5, 11, 19, 3, rr(S, 1))),
        line(seg(5, 14, 5, 21)),
        line(seg(19, 14, 19, 21)),
        line(seg(19, 11, 19, 6)),
    ]


@icon("chainsaw", CAT, "Chainsaw in side view with a motor body, a top handle and a long bar with chain teeth",
      tags=["chain saw", "logging", "tree cutting", "forestry", "timber", "firewood", "power tool"])
def _(S):
    return [
        shell(rect(2.5, 8, 8.5, 9, rr(S, 3))),
        line(poly([(4.5, 8), (5, 4), (9.5, 4)], r=S.r)),
        shell(rect(11, 8.5, 10.5, 6, rr(S, 3))),
        line(poly([(12, 17), (13.75, 19.5), (15.5, 17), (17.25, 19.5), (19, 17)], r=0)),
        detail(seg(13.5, 11.5, 19, 11.5)),
    ]


@icon("band-saw", CAT, "Tall band saw with a casing housing two wheels and a vertical blade across a small table",
      tags=["bandsaw", "resaw", "woodworking", "metal cutting", "workshop", "machine tool", "blade"])
def _(S):
    return [
        shell(rect(3, 2.5, 10, 19, rr(S, 5))),
        dot(8, 7.5, 2),
        dot(8, 16.5, 2),
        line(seg(13, 4.5, 17.5, 4.5)),
        line(seg(13, 19.5, 17.5, 19.5)),
        line(seg(17.5, 4.5, 17.5, 19.5)),
        line(seg(14, 12, 22, 12)),
    ]


@icon("scroll-saw", CAT, "Low scroll saw with a long overhead arm and a thin vertical blade over a small table",
      tags=["fretsaw", "fretwork", "intarsia", "woodworking", "craft", "machine tool", "detail cutting"])
def _(S):
    return [
        shell(rect(3, 17.5, 18, 3.5, rr(S, 1.5))),
        line(poly([(6.5, 17.5), (6.5, 5), (18, 5), (18, 9)], r=S.r)),
        line(seg(18, 9, 18, 17.5)),
        line(seg(11, 13, 21.5, 13)),
    ]


@icon("angle-grinder", CAT, "Long motor body with a round disc and half guard at the front, set at a right angle",
      tags=["disc grinder", "cutting disc", "metalwork", "fabrication", "power tool", "grinding", "sparks"])
def _(S):
    return [
        shell(rect(2.5, 9, 13.5, 6.5, rr(S, 3))),
        line(seg(16, 12.25, 19, 12.25)),
        shell(rect(19, 4, 3, 16, rr(S, 1))),
        line(poly([(9, 15.5), (9, 20.5)], r=0)),
    ]


@icon("bench-grinder", CAT, "Central motor with a grinding wheel on each side under curved guards, on a small base",
      tags=["wheel grinder", "sharpening", "tool sharpening", "workshop", "machine tool", "metalwork"])
def _(S):
    return [
        shell(rect(8.5, 8, 7, 7, rr(S, 2))),
        shell(rect(3.5, 8, 4, 8, rr(S, 1.5))),
        shell(rect(16.5, 8, 4, 8, rr(S, 1.5))),
        line(poly([(2.5, 11), (2.5, 4.5), (8, 4.5)], r=S.r)),
        line(poly([(21.5, 11), (21.5, 4.5), (16, 4.5)], r=S.r)),
        shell(rect(5, 18.5, 14, 3, rr(S, 1))),
        line(seg(12, 15, 12, 18.5)),
    ]


@icon("orbital-sander", CAT, "Palm sander with a flat round pad at the bottom and a round dome grip on top",
      tags=["random orbit sander", "palm sander", "sanding", "woodworking", "finishing", "power tool", "abrasive"])
def _(S):
    if S.name == "line":
        d = "M2.5 19.5V15.5H5Q5 7 12 7Q19 7 19 15.5H21.5V19.5Z"
    else:
        d = "M4.5 19.5Q2.5 19.5 2.5 17.5V17.5Q2.5 15.5 4.5 15.5H5Q5 7 12 7Q19 7 19 15.5H19.5Q21.5 15.5 21.5 17.5Q21.5 19.5 19.5 19.5Z"
    return [
        shell(d),
        detail(seg(9, 12, 15, 12)),
    ]


@icon("detail-sander", CAT, "Palm sander with a dome grip and an iron-shaped pad that tapers to a point at the front",
      tags=["mouse sander", "corner sander", "iron sander", "tight spaces", "sanding", "finishing", "power tool"])
def _(S):
    if S.name == "line":
        d = "M2.5 19.5V15.5H5Q5 7 11 7Q17 7 17 15.5L21.5 19.5Z"
    else:
        d = "M4.5 19.5Q2.5 19.5 2.5 17.5Q2.5 15.5 4.5 15.5H5Q5 7 11 7Q17 7 17 15.5L21 18.5Q21.5 19.5 20 19.5Z"
    return [
        shell(d),
        detail(seg(8.5, 12, 13.5, 12)),
    ]


@icon("nail-gun", CAT, "Pneumatic nail gun in side view with a barrel body, a vertical nose and an angled nail magazine strip",
      tags=["nailer", "framing nailer", "pneumatic", "carpentry", "construction", "roofing", "power tool"])
def _(S):
    return [
        shell(rect(3, 3.5, 15, 6.5, rr(S, 3))),
        shell(rect(14, 10, 4, 8, rr(S, 1))),
        line(seg(16, 18, 16, 21.5)),
        shell(poly([(14, 14.5), (14, 18), (4, 21), (4, 17.5)], closed=True, r=S.r * 0.4)),
        line(poly([(6, 10), (6, 13)], r=0)),
    ]


@icon("air-compressor", CAT, "Horizontal air tank on small wheels with a motor on top and a round pressure gauge",
      tags=["compressor", "pneumatic", "tank", "pressure", "workshop", "garage", "tire inflation"])
def _(S):
    body = union(rect(2.5, 11, 18, 7.5, rr(S, 3.75)), rect(6, 5, 8, 7, rr(S, 1.5)))
    return [
        shell(body),
        shell(circle(18.5, 6.5, 2.5)),
        line(seg(18.5, 9, 18.5, 11)),
        dot(6.5, 20.5, 1.5),
        dot(16.5, 20.5, 1.5),
    ]


@icon("air-hose-coil", CAT, "Coiled air hose forming a spiral with a quick connect fitting on one end",
      tags=["pneumatic hose", "coil hose", "air line", "compressor", "airline", "garage", "spiral hose"])
def _(S):
    return [
        line(ellipse(10, 6.25, 7.25, 2.5)),
        line(ellipse(10, 11.5, 7.25, 2.5)),
        line(ellipse(10, 16.75, 7.25, 2.5)),
        line(poly([(17.25, 16.75), (19.5, 17.5)], r=0)),
        shell(rect(18.5, 14.5, 3.5, 6, rr(S, 3))),
    ]


@icon("rotary-tool", CAT, "Slim pen-shaped rotary power tool with a tiny round cutting bit at the front",
      tags=["engraver", "die grinder", "hobby tool", "carving", "polishing", "craft"])
def _(S):
    return [
        rdot(12, 3.5, 1.75),
        line(rseg(12, 5, 12, 7.5)),
        shell(rrect(10.5, 7.5, 3, 2.5, rr(S, 1))),
        shell(rrect(9, 10, 6, 10, rr(S, 3))),
        detail(rseg(9, 13.5, 15, 13.5)),
        detail(rseg(9, 16.5, 15, 16.5)),
    ]


@icon("oscillating-multitool", CAT, "Long-bodied power tool with a small flat fan-shaped blade attached at the front",
      tags=["multi tool", "multitool", "oscillating tool", "sanding", "plunge cut", "grout removal", "renovation"])
def _(S):
    return [
        shell(rect(2.5, 8, 12.5, 7, rr(S, 3.5))),
        shell(rect(15, 9.5, 3, 4, rr(S, 1))),
        solid(poly([(18, 11.5), (22.5, 7.5), (22.5, 15.5)])),
        detail(seg(6, 11.5, 11.5, 11.5)),
        line(poly([(6, 15), (6, 20)], r=0)),
    ]


@icon("wood-lathe", CAT, "Lathe with a long bed, a headstock on the left, a tailstock on the right and a spindle workpiece between",
      tags=["turning", "woodturning", "spindle", "bowl turning", "workshop", "machine tool", "carpentry"])
def _(S):
    bed = union(rect(2.5, 16, 19, 4, rr(S, 1)), rect(3, 8.5, 5, 8, rr(S, 1.5)), rect(17, 10, 4, 6.5, rr(S, 1.5)))
    work = poly([(8.5, 11.5), (10.5, 11.5), (11.5, 12.75), (13.5, 12.75), (14.5, 11.5), (16.5, 11.5), (16.5, 14.5), (14.5, 14.5), (13.5, 13.25), (11.5, 13.25), (10.5, 14.5), (8.5, 14.5)], closed=True)
    return [
        shell(bed),
        solid(work),
    ]


@icon("shop-vacuum", CAT, "Round drum shop vacuum on casters with a motor lid on top and a flexible hose from the side",
      tags=["wet dry vacuum", "workshop", "garage", "cleaning", "sawdust", "drum vacuum"])
def _(S):
    body = union(rect(3.5, 5.5, 14, 4, rr(S, 1.5)), rect(4.5, 9, 12, 10, rr(S, 2)), rect(8, 2.5, 5, 3.5, rr(S, 1)))
    return [
        shell(body),
        line(poly([(16.5, 13), (20, 13), (21.5, 15), (21.5, 20.5)], r=S.r)),
        dot(7, 21, 1.25),
        dot(14, 21, 1.25),
    ]


@icon("jackhammer", CAT, "Tall pneumatic breaker with handlebars at the top, a cylinder body and a long chisel point at the bottom",
      tags=["pneumatic drill", "breaker", "concrete", "demolition", "road work", "construction", "paving breaker"])
def _(S):
    return [
        line(poly([(3, 7), (5.5, 3.5), (18.5, 3.5), (21, 7)], r=S.r)),
        line(seg(12, 3.5, 12, 6)),
        shell(rect(8, 6, 8, 9, rr(S, 3))),
        shell(rect(9.5, 15, 5, 2.5, rr(S, 1))),
        solid(poly([(10.75, 17.5), (13.25, 17.5), (12, 22.5)])),
    ]


@icon("demolition-hammer", CAT, "Large power hammer with a rear D handle, a side handle and a pointed chisel bit at the front",
      tags=["breaker hammer", "chipping hammer", "concrete", "demolition", "heavy duty", "construction", "jack hammer"])
def _(S):
    a = 35
    return [
        shell(rrect(7, 7.5, 9.5, 7, rr(S, 3), deg=a)),
        line(rp([(8.5, 14.5), (4.5, 14.5), (2.5, 10.5), (7, 7.5)], closed=False, r=S.r, deg=a)),
        line(rp([(12, 7.5), (12, 3.5)], closed=False, deg=a)),
        line(rseg(9.5, 3.5, 14.5, 3.5, deg=a)),
        line(rseg(16.5, 11, 18.5, 11, deg=a)),
        solid(rp([(18.5, 9), (22, 11), (18.5, 13)], deg=a)),
    ]


@icon("tile-saw", CAT, "Small wet tile saw with a round blade rising through the table over a water tray",
      tags=["wet saw", "tile cutter", "ceramic", "porcelain", "masonry saw", "bathroom", "flooring"])
def _(S):
    return [
        line(arc(12, 10, 6.5, 185, 355)),
        shell(rect(2.5, 10, 19, 3.5, rr(S, 1.5))),
        shell(rect(5, 13.5, 14, 7, rr(S, 2))),
        detail("M8 17.25q1.3-1.5 2.6 0t2.6 0t2.6 0"),
    ]


@icon("cordless-tool-battery", CAT, "Rectangular battery pack with a slide rail on top and a row of charge bars on the front",
      tags=["battery pack", "power tool battery", "rechargeable", "lithium", "cordless", "charge level", "drill battery"])
def _(S):
    return [
        shell(rect(3.5, 9, 17, 11.5, rr(S, 2.5))),
        line(poly([(7, 9), (7, 5), (17, 5), (17, 9)], r=S.r)),
        detail(seg(8, 13, 8, 17)),
        detail(seg(12, 13, 12, 17)),
        detail(seg(16, 13, 16, 17)),
    ]


@icon("drill-chuck", CAT, "Knurled drill chuck with a ribbed ring and three jaws closing together at the front",
      tags=["chuck", "keyless chuck", "jaws", "drill part", "bit holder", "power tool part", "collet"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 13.5, 11, rr(S, 2.5))),
        detail(seg(7, 6.5, 7, 17.5)),
        detail(seg(11, 6.5, 11, 17.5)),
        shell(poly([(16, 9), (21.5, 10.5), (21.5, 13.5), (16, 15)], closed=True, r=S.r * 0.4)),
        line(seg(9, 17.5, 9, 21)),
    ]


def _gear(cx, cy, ro, ri, n=8):
    pts = []
    for i in range(n):
        a0 = i * 360 / n
        pts += [polar(cx, cy, ri, a0 - 360 / n * 0.25), polar(cx, cy, ro, a0 - 360 / n * 0.12),
                polar(cx, cy, ro, a0 + 360 / n * 0.12), polar(cx, cy, ri, a0 + 360 / n * 0.25)]
    return pts


@icon("chuck-key", CAT, "T-shaped chuck key with a small toothed gear at the end of its pin",
      tags=["drill key", "chuck tightening", "drill press", "tool part", "gear key", "t handle", "lathe key"])
def _(S):
    return [
        line(seg(6, 3.5, 18, 3.5)),
        line(seg(12, 3.5, 12, 14)),
        shell(poly(_gear(12, 17.75, 4, 2.9), closed=True, r=S.r * 0.15), stroke_miterlimit="2"),
        dot(12, 17.75, 1),
    ]


# ============================================================================ drill bits


@icon("twist-drill-bit", CAT, "Long straight drill bit with a spiral groove along its body and a pointed tip",
      tags=["drill bit", "hss bit", "metal drilling", "boring", "spiral flute", "power drill", "fluted"])
def _(S):
    return [
        shell(rp([(10, 16), (10, 7), (12, 2.5), (14, 7), (14, 16)], r=S.r * 0.3), stroke_miterlimit="2"),
        detail(rseg(10, 14, 14, 11.5)),
        detail(rseg(10, 10.5, 14, 8)),
        shell(rrect(10.5, 16, 3, 5.5, rr(S, 1))),
    ]


@icon("spade-bit", CAT, "Drill bit with a flat paddle-shaped blade and a sharp central point at the tip",
      tags=["paddle bit", "wood boring", "flat bit", "woodworking", "drill bit", "carpentry", "spade"])
def _(S):
    return [
        shell(rp([(6.5, 14), (6.5, 7), (12, 3), (17.5, 7), (17.5, 14)], r=S.r * 0.4), stroke_miterlimit="3"),
        line(rseg(12, 14, 12, 21.5)),
    ]


@icon("forstner-bit", CAT, "Short cylinder drill bit with a flat face, a toothed rim and a tiny centre spur",
      tags=["flat bottom bit", "hinge hole", "cabinet making", "woodworking", "drill bit", "clean hole", "boring"])
def _(S):
    return [
        line(rseg(12, 2.5, 12, 6.5)),
        shell(rp([(6.5, 13), (6.5, 4.5), (9.5, 7), (14.5, 7), (17.5, 4.5), (17.5, 13)], r=S.r * 0.4), stroke_miterlimit="3"),
        line(rseg(12, 13, 12, 21.5)),
    ]


@icon("auger-bit", CAT, "Long drill bit with a wide open corkscrew spiral and a threaded screw point",
      tags=["wood auger", "timber drill", "brace bit", "deep hole", "woodworking", "corkscrew bit", "boring"])
def _(S):
    return [
        line(rseg(12, 2.5, 12, 7)),
        shell(rrect(10, 7, 4, 11, rr(S, 1))),
        line(rseg(7.5, 11, 16.5, 8.5)),
        line(rseg(7.5, 15.5, 16.5, 13)),
        line(rseg(12, 18, 12, 22)),
    ]


@icon("step-drill-bit", CAT, "Cone-shaped bit built from stacked steps of growing diameter",
      tags=["cone bit", "sheet metal", "stepped bit", "hole enlarging", "drill bit", "metalwork"])
def _(S):
    prof = [(13.5, 3), (13.5, 7.5), (15.5, 7.5), (15.5, 12), (17.5, 12), (17.5, 16.5),
            (6.5, 16.5), (6.5, 12), (8.5, 12), (8.5, 7.5), (10.5, 7.5), (10.5, 3)]
    return [
        shell(rp(prof, r=0), stroke_miterlimit="3"),
        line(rseg(12, 16.5, 12, 21)),
    ]


@icon("countersink-bit", CAT, "Short drill bit with a cone-shaped cutting head that has a few flutes",
      tags=["countersink", "chamfer", "screw head", "woodworking", "drill bit", "deburring", "cone cutter"])
def _(S):
    return [
        shell(rp([(9, 3.5), (15, 3.5), (18, 13), (6, 13)], r=S.r * 0.3), stroke_miterlimit="4"),
        detail(rseg(10.5, 13, 11, 7.5)),
        detail(rseg(13.5, 13, 13, 7.5)),
        line(rseg(12, 13, 12, 21.5)),
    ]


@icon("masonry-drill-bit", CAT, "Straight spiral drill bit with a wider arrow-shaped carbide tip at the end",
      tags=["concrete bit", "brick drilling", "carbide tip", "wall drilling", "stone", "drill bit", "hammer drill bit"])
def _(S):
    return [
        solid(rp([(8.5, 7.5), (12, 2.5), (15.5, 7.5)])),
        shell(rrect(10, 7.5, 4, 9.5, rr(S, 1))),
        line(rseg(12, 17, 12, 21.5)),
    ]


# ============================================================================ abrasive discs and wheels


@icon("grinding-disc", CAT, "Flat round grinding disc with a raised centre hub and a hole in the middle",
      tags=["abrasive wheel", "grinder disc", "metal grinding", "cutting disc", "angle grinder", "fabrication", "round disc"])
def _(S):
    hub = poly(regular(12, 12, 5, 6), closed=True) if S.name == "line" else circle(12, 12, 5)
    return [
        shell(circle(12, 12, 9)),
        detail(hub),
        dot(12, 12, 1.25),
    ]


@icon("flap-disc", CAT, "Round disc covered in overlapping flaps arranged like fish scales around a centre hole",
      tags=["flap wheel", "sanding flap", "abrasive", "grinder accessory", "metal finishing", "louvred disc", "weld blending"])
def _(S):
    parts = [shell(circle(12, 12, 9)), dot(12, 12, 1.5)]
    for i in range(8):
        a = i * 45
        p0 = polar(12, 12, 3.5, a)
        p1 = polar(12, 12, 9, a + 28)
        parts.append(detail(seg(p0[0], p0[1], p1[0], p1[1])))
    return parts


@icon("sanding-disc", CAT, "Round sanding pad with a ring of small dust holes and a grainy dotted texture",
      tags=["sandpaper disc", "hook and loop", "orbital sander pad", "abrasive", "grit", "dust extraction", "finishing"])
def _(S):
    parts = [shell(circle(12, 12, 9))]
    for i in range(6):
        x, y = polar(12, 12, 5.5, i * 60 + 30)
        parts.append(dot(x, y, 1.25))
    parts.append(mark(rect(10.75, 10.75, 2.5, 2.5) if S.name == "line" else circle(12, 12, 1.4)))
    return parts


@icon("wire-wheel", CAT, "Round wheel of radiating bristle lines around a centre hub",
      tags=["wire brush", "rust removal", "paint stripping", "bench grinder", "cleaning wheel", "bristles", "deburring"])
def _(S):
    parts = []
    for i in range(10):
        a = i * 36
        p0, p1 = polar(12, 12, 6.25, a), polar(12, 12, 10, a)
        parts.append(line(seg(p0[0], p0[1], p1[0], p1[1])))
    parts.append(shell(poly(regular(12, 12, 3.5, 6), closed=True) if S.name == "line" else circle(12, 12, 3.5)))
    return parts


@icon("bench-vise", CAT, "Heavy bench vise with two jaws, a long screw and a sliding T-bar handle",
      tags=["vice", "workbench", "clamping", "metalworking", "holding", "woodworking", "workshop"])
def _(S):
    body = union(rect(2.5, 14, 15, 6.5, rr(S, 1.5)), rect(2.5, 4.5, 4.5, 10, rr(S, 1.5)), rect(13, 4.5, 4.5, 10, rr(S, 1.5)))
    return [
        shell(body),
        line(seg(17.5, 9.5, 21, 9.5)),
        line(seg(21, 5.5, 21, 13.5)),
    ]


@icon("bar-clamp", CAT, "Long flat bar with a fixed jaw at the top, a sliding jaw and a pistol grip at the bottom",
      tags=["quick clamp", "trigger clamp", "woodworking", "gluing", "holding", "clamping", "carpentry"])
def _(S):
    body = union(rect(4.5, 2.5, 3.5, 19, rr(S, 1)), rect(4.5, 2.5, 13.5, 3.5, rr(S, 1.75)), rect(4.5, 10.5, 13.5, 3.5, rr(S, 1.75)))
    return [
        shell(body),
        shell(poly([(11, 14), (18, 14), (18, 19), (16, 21.5), (11, 21.5)], closed=True, r=S.r)),
    ]


@icon("corner-clamp", CAT, "Right-angle clamp holding two boards together at a corner with two screw handles",
      tags=["mitre clamp", "miter clamp", "picture frame", "woodworking", "90 degree", "joinery", "corner holder"])
def _(S):
    return [
        shell(poly([(3, 3), (21, 3), (21, 9.5), (9.5, 9.5), (9.5, 21), (3, 21)], closed=True, r=S.r)),
        line(seg(17.5, 9.5, 17.5, 14)),
        line(seg(15, 14, 20, 14)),
        line(seg(9.5, 17.5, 14, 17.5)),
        line(seg(14, 15.5, 14, 19.5)),
    ]


@icon("f-clamp", CAT, "F-shaped clamp with a long bar, a fixed upper arm and a lower arm with a screw handle",
      tags=["bar clamp", "woodworking", "clamping", "holding", "gluing", "workshop", "carpentry"])
def _(S):
    body = union(rect(3.5, 3, 3.5, 18, rr(S, 1)), rect(3.5, 3, 14, 4, rr(S, 1.5)), rect(3.5, 13, 14, 4, rr(S, 1.5)))
    return [
        shell(body),
        line(seg(20, 11, 20, 19)),
        line(seg(17.5, 15, 20, 15)),
    ]


@icon("magnetic-pickup-tool", CAT, "Telescoping pen-shaped rod with a small horseshoe magnet at the tip lifting a screw",
      tags=["magnet pick up", "retrieval tool", "mechanic", "telescoping", "dropped screw", "garage", "magnetic wand"])
def _(S):
    return [
        solid(rp([(9, 2), (11, 2), (11, 4.5), (13, 4.5), (13, 2), (15, 2), (15, 6.5), (9, 6.5)])),
        line(rseg(12, 6.5, 12, 10)),
        shell(rrect(10.25, 10, 3.5, 5, rr(S, 1))),
        shell(rrect(9, 15, 6, 6.5, rr(S, 2.5))),
    ]


@icon("helping-hands", CAT, "Small weighted base with two jointed arms holding crocodile clips and a round magnifier",
      tags=["third hand", "soldering helper", "electronics", "crocodile clip", "magnifier", "workbench", "hobby"])
def _(S):
    return [
        shell(circle(12, 6.5, 3.75)),
        line(seg(12, 10.25, 12, 19)),
        line(poly([(7, 19), (7, 14), (3.5, 10.5)], r=S.r)),
        solid(poly([(2.5, 11.5), (2.5, 7.5), (5.5, 9.5)])),
        line(poly([(17, 19), (17, 14), (20.5, 10.5)], r=S.r)),
        solid(poly([(21.5, 11.5), (21.5, 7.5), (18.5, 9.5)])),
        shell(rect(3, 19, 18, 2.5, L(S, 0, 1.25))),
    ]


@icon("caliper", CAT, "Vernier caliper with a long graduated bar, one fixed jaw and a sliding jaw",
      tags=["vernier caliper", "measuring", "machinist", "precision", "thickness", "engineering", "gauge"])
def _(S):
    body = union(rect(2.5, 3.5, 19, 5, rr(S, 2.5)), rect(2.5, 3.5, 3.5, 17.5, L(S, 0, 1.5)), rect(10, 3.5, 4, 14, L(S, 0, 1.5)))
    return [
        shell(body),
        detail(seg(17, 3.5, 17, 8.5)),
        detail(seg(20, 3.5, 20, 8.5)),
    ]


@icon("digital-caliper", CAT, "Caliper with a long bar and a sliding head carrying a small rectangular digital display",
      tags=["electronic caliper", "measuring", "precision", "machinist", "lcd", "engineering", "gauge"])
def _(S):
    body = union(rect(2.5, 3.5, 19, 5, rr(S, 2.5)), rect(2.5, 3.5, 3.5, 17.5, L(S, 0, 1.5)), rect(9, 3.5, 11, 10.5, rr(S, 2)),
                 rect(9, 3.5, 3.5, 14, L(S, 0, 1.5)))
    return [
        shell(body),
        mark(rect(14, 6, 4.5, 3.5, rr(S, 0.75))),
    ]


@icon("micrometer", CAT, "C-shaped frame with an anvil on one side and a thick graduated barrel with a thimble on the other",
      tags=["outside micrometer", "measuring", "precision", "machinist", "thickness gauge", "engineering", "screw gauge"])
def _(S):
    return [
        line(poly([(4.5, 14), (4.5, 8), (7.5, 4.5), (18, 4.5), (18, 9.5)], r=S.r)),
        line(seg(4.5, 14, 8, 14)),
        line(seg(10.5, 14, 12.5, 14)),
        shell(rect(12.5, 10.5, 4.5, 7, rr(S, 1))),
        shell(rect(17, 9.5, 4.5, 9, rr(S, 1.5))),
        dot(14.75, 14, 0.75),
    ]


@icon("feeler-gauge", CAT, "Fan of thin metal blades pivoting from a common screw at one end",
      tags=["thickness gauge", "gap gauge", "spark plug gap", "valve clearance", "mechanic", "measuring", "engine"])
def _(S):
    parts = [shell(circle(5.5, 18.5, 2.6))]
    for a in (-78, -58, -38, -18):
        p0, p1 = polar(5.5, 18.5, 4.6, a), polar(5.5, 18.5, 16, a)
        parts.append(line(seg(p0[0], p0[1], p1[0], p1[1])))
    parts.append(mark(rect(4.75, 17.75, 1.5, 1.5) if S.name == "line" else circle(5.5, 18.5, 0.8)))
    return parts


@icon("dial-indicator", CAT, "Round gauge face with a needle and a long plunger rod sticking out of the bottom",
      tags=["dial gauge", "test indicator", "runout", "machinist", "measuring", "alignment", "precision"])
def _(S):
    hub = circle(12, 9, 1.2) if S.name == "rounded" else rect(10.9, 7.9, 2.2, 2.2)
    return [
        shell(circle(12, 9, 7.25)),
        line(seg(12, 9, 15.25, 5.75)),
        mark(hub),
        line(seg(12, 16.25, 12, 22)),
    ]


@icon("carpenter-square", CAT, "Large flat L-shaped steel square with ruler tick marks along both arms",
      tags=["framing square", "steel square", "rafter square", "carpentry", "layout", "right angle", "measuring"])
def _(S):
    return [
        shell(poly([(3, 3), (8.5, 3), (8.5, 15.5), (21, 15.5), (21, 21), (3, 21)], closed=True, r=S.r)),
        detail(seg(3, 7, 5.5, 7)),
        detail(seg(3, 11, 5.5, 11)),
        detail(seg(3, 15, 5.5, 15)),
        detail(seg(12.5, 21, 12.5, 18.5)),
        detail(seg(16.5, 21, 16.5, 18.5)),
    ]


@icon("speed-square", CAT, "Triangular rafter square with a thick lip on one edge and degree marks along the long side",
      tags=["rafter square", "roofing", "carpentry", "angle marking", "layout", "triangle square"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 4), (20, 21)], closed=True, r=S.r)),
        detail(seg(8.5, 10.5, 6.5, 12.5)),
        detail(seg(12, 14, 10, 16)),
        dot(6.5, 17, 1.25),
    ]


@icon("try-square", CAT, "Small L-shaped square with a thick stock and a thin steel blade at a right angle",
      tags=["engineer's square", "woodworking", "marking", "right angle", "joinery", "checking", "hand tool"])
def _(S):
    body = union(rect(3, 14.5, 18, 6.5, rr(S, 1.5)), rect(3, 3, 4, 12, rr(S, 1)))
    return [
        shell(body),
        detail(seg(11, 14.5, 11, 21)),
    ]


@icon("sliding-bevel", CAT, "Handle stock with a thin blade pivoting on a wing nut at an adjustable angle",
      tags=["bevel gauge", "t bevel", "angle marking", "woodworking", "carpentry", "joinery", "layout tool"])
def _(S):
    return [
        shell(rect(2.5, 14.5, 19, 5.5, rr(S, 1.5))),
        line(seg(7, 17.25, 19, 4)),
        dot(7, 17.25, 1.75),
    ]
