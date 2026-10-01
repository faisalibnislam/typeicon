"""TypeIcon Core: tools & construction.

Generic hand and power tools drawn from the objects themselves (no brand shapes). Long hand tools are
designed upright and turned 45° so the handle points to the bottom-left and the working end to the top-right;
that keeps the bottom-right corner (13–23) free for variant badges and gives every tool the same diagonal.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "tools"
TILT = 45  # upright designs are turned clockwise by this much (handle to the bottom-left)


def rot(pts, deg=TILT, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rp(pts, closed=True, r=0.0, deg=TILT):
    """Rotated polygon/polyline."""
    return poly(rot(pts, deg), closed=closed, r=r)


def rpath(cmds, deg=TILT) -> str:
    """Path from commands with rotated points: ("M", p) ("L", p) ("A", r, large, sweep, p) ("Q", c, p) ("C", c1, c2, p) ("Z",)."""
    out = []

    def pt(p):
        q = rot([p], deg)[0]
        return f"{fmt(q[0])} {fmt(q[1])}"
    for c in cmds:
        op = c[0]
        if op in ("M", "L"):
            out.append(op + pt(c[1]))
        elif op == "A":
            out.append(f"A{fmt(c[1])} {fmt(c[1])} 0 {c[2]} {c[3]} " + pt(c[4]))
        elif op == "Q":
            out.append("Q" + pt(c[1]) + " " + pt(c[2]))
        elif op == "C":
            out.append("C" + pt(c[1]) + " " + pt(c[2]) + " " + pt(c[3]))
        elif op == "Z":
            out.append("Z")
    return "".join(out)


def rrect(x, y, w, h, rx=0.0, deg=TILT) -> str:
    """Rotated rounded rectangle (corner arcs are rotation invariant)."""
    rx = max(0.0, min(rx, w / 2, h / 2))
    if rx == 0:
        return rp([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], deg=deg)
    return rpath([("M", (x + rx, y)), ("L", (x + w - rx, y)), ("A", rx, 0, 1, (x + w, y + rx)),
                  ("L", (x + w, y + h - rx)), ("A", rx, 0, 1, (x + w - rx, y + h)), ("L", (x + rx, y + h)),
                  ("A", rx, 0, 1, (x, y + h - rx)), ("L", (x, y + rx)), ("A", rx, 0, 1, (x + rx, y)), ("Z",)], deg)


def rseg(x1, y1, x2, y2, deg=TILT) -> str:
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg)
    return seg(a, b, c, d)


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


# ============================================================================ striking and turning

@icon("hammer", CAT, "Claw hammer with its head and handle",
      tags=["claw hammer", "build", "construction", "diy", "repair", "nail", "carpentry"])
def _(S):
    k = S.r * 0.6
    face = rp([(9.5, 5), (5.5, 5), (5.5, 11.5), (9.5, 11.5)], closed=False, r=k)
    # striking face (filleted in Rounded) continuing into the neck and a claw that curls toward the handle
    head = face + rpath([("L", (9.5, 10)), ("L", (14.5, 10)), ("C", (17, 10), (19, 11), (20, 12.5)),
                         ("C", (20, 9), (18, 6.5), (14.5, 6.5)), ("L", (9.5, 6.5)), ("Z",)])
    return [
        shell(head, stroke_miterlimit="2"),
        shell(rrect(10.5, 10, 3, 11.5, rr(S, 1.5))),
    ]


def _wrench_cmds():
    cy, R, hw, sw = 6.0, 5.0, 1.75, 2.0  # jaw centre y, jaw radius, slot half-width, shaft half-width
    ys = cy - math.sqrt(R * R - hw * hw)
    yj = cy + math.sqrt(R * R - sw * sw)
    return [("M", (12 - hw, ys)), ("L", (12 - hw, cy)), ("A", hw, 0, 0, (12 + hw, cy)), ("L", (12 + hw, ys)),
            ("A", R, 0, 1, (12 + sw, yj)), ("L", (12 + sw, 19.5)), ("A", sw, 0, 1, (12 - sw, 19.5)),
            ("L", (12 - sw, yj)), ("A", R, 0, 1, (12 - hw, ys)), ("Z",)]


@icon("wrench", CAT, "Open-end wrench (spanner)",
      tags=["spanner", "repair", "fix", "maintenance", "mechanic", "tool", "settings"], aliases=["spanner"])
def _(S):
    parts = [shell(rpath(_wrench_cmds()))]
    # Line: a square hang hole in the handle; Rounded: a round one.
    c = rot([(12, 17.5)])[0]
    parts.append(dot(c[0], c[1], 1.1) if S.name == "rounded" else Part("dot", rp([(11, 16.5), (13, 16.5), (13, 18.5), (11, 18.5)])))
    return parts


@icon("screwdriver", CAT, "Flat-blade screwdriver with a grip handle",
      tags=["screw", "fix", "repair", "assemble", "diy", "tool"])
def _(S):
    return [
        line(rseg(12, 2.5, 12, 10)),
        shell(rrect(9.5, 10, 5, 2.5, rr(S, 1))),
        shell(rrect(8.5, 12.5, 7, 9, rr(S, 3))),
        detail(rseg(12, 15, 12, 19)),
    ]


@icon("saw", CAT, "Hand saw with a toothed blade and a closed grip",
      tags=["handsaw", "cut", "wood", "carpentry", "woodwork", "tool"], aliases=["handsaw"])
def _(S):
    teeth = []
    x0, x1, n = 10.5, 8.0, 4  # the toothed front edge runs from (10.5, 4) down to (8, 14)
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        ya, yb = 4 + 10 * t0, 4 + 10 * t1
        xa, xb = x0 + (x1 - x0) * t0, x0 + (x1 - x0) * t1
        teeth += [(xa, ya), (xb - 1.4, (ya + yb) / 2 + 0.6)]
    blade = [(15, 14), (15, 2.5)] + teeth + [(8, 14)]
    return [
        shell(rp(blade, r=S.r * 0.3), stroke_miterlimit="2"),
        shell(rrect(7.5, 14, 8.5, 7.5, rr(S, 3))),
        detail(rseg(10.25, 17.75, 13.25, 17.75)),
    ]


# ============================================================================ power tools

@icon("drill", CAT, "Cordless power drill with a bit, grip and battery",
      tags=["power drill", "cordless", "drilling", "diy", "bore", "tool"], aliases=["power-drill"])
def _(S):
    return [
        shell(rect(3, 4, 13, 7, rr(S, 3))),
        solid(poly([(16, 5.5), (18.5, 6.5), (18.5, 8.5), (16, 9.5)], closed=True)),
        line(seg(18.5, 7.5, 22, 7.5)),
        shell(poly([(6, 11), (11, 11), (10, 17.5), (6, 17.5)], closed=True, r=S.r)),
        shell(rect(3.5, 17.5, 9, 3.5, rr(S, 1.5))),
        detail(seg(5.5, 7.5, 10, 7.5)),
    ]


# ============================================================================ gripping

@icon("pliers", CAT, "Pliers with tapered jaws and two handles",
      tags=["plier", "grip", "pinch", "electrician", "repair", "tool"], aliases=["plier"])
def _(S):
    return [
        shell(rp([(10, 11), (10.75, 4.5), (12, 2.5), (13.25, 4.5), (14, 11)], r=S.r * 0.6), stroke_miterlimit="2"),
        detail(rseg(12, 5, 12, 10)),
        shell(rpath([("M", (9.5, 13.5)), ("A", 2.5, 1, 1, (14.5, 13.5)), ("A", 2.5, 0, 1, (9.5, 13.5)), ("Z",)])),
        line(rpath([("M", (10.5, 15.5)), ("Q", (8.5, 18), (7.5, 21))])),
        line(rpath([("M", (13.5, 15.5)), ("Q", (15.5, 18), (16.5, 21))])),
    ]


# ============================================================================ storage and measuring

@icon("toolbox", CAT, "Toolbox with a carrying handle and a latch",
      tags=["tool box", "tool kit", "toolkit", "repair", "maintenance", "case", "tools"], aliases=["toolkit"])
def _(S):
    return [
        line(poly([(8.5, 8), (8.5, 4.5), (15.5, 4.5), (15.5, 8)], r=S.r)),
        shell(rect(3, 8, 18, 12, rr(S, 3))),
        detail(seg(3, 12.5, 21, 12.5)),
        sq(10.5, 11, 3, 3.5, 0.5 if S.name == "rounded" else 0),
    ]


@icon("tape-measure", CAT, "Tape measure: a round-cornered case with the tape pulled out",
      tags=["measuring tape", "measure", "length", "tape", "dimension", "tool"], aliases=["measuring-tape"])
def _(S):
    return [
        shell(rect(3, 3, 14, 14, rr(S, 4))),
        detail(circle(10, 10, 3)),
        line(poly([(17, 15.5), (20.5, 15.5), (20.5, 18.5)], r=S.r * 0.5)),
    ]


@icon("spirit-level", CAT, "Spirit level: a bar with a bubble vial",
      tags=["level", "bubble level", "leveller", "horizontal", "construction", "tool"], aliases=["bubble-level"])
def _(S):
    return [
        shell(rect(2, 7.5, 20, 9, rr(S, 2.5))),
        detail(seg(8.5, 10.5, 8.5, 13.5)),
        detail(seg(15.5, 10.5, 15.5, 13.5)),
        dot(12, 12, 1.5) if S.name == "rounded" else sq(10.5, 10.5, 3, 3),
    ]


@icon("paint-can", CAT, "Open paint can with a wire handle and paint running down its side",
      tags=["paint tin", "paint", "decorating", "painting", "can", "diy"], aliases=["paint-tin"])
def _(S):
    return [
        line("M5 9A7 7 0 0 1 19 9"),
        shell(poly([(4, 7.5), (20, 7.5), (20, 10.5), (4, 10.5)], closed=True, r=S.r * 0.5)),
        shell(poly([(5.5, 10.5), (18.5, 10.5), (18.5, 21), (5.5, 21)], closed=True, r=S.r)),
        detail("M5.5 14C7 14 7.5 16.5 9 16.5C10.5 16.5 10.5 13.5 12 13.5C13.5 13.5 14 15.5 15.5 15.5C17 15.5 17.3 14 18.5 14"),
    ]


# ============================================================================ digging and masonry

@icon("trowel", CAT, "Pointed masonry trowel with a handle",
      tags=["masonry", "bricklaying", "plaster", "cement", "construction", "garden"])
def _(S):
    return [
        shell(rp([(5, 11.5), (19, 11.5), (12, 21.5)], r=S.r), stroke_miterlimit="2"),
        line(rseg(12, 11.5, 12, 8.5)),
        shell(rrect(10, 2, 4, 6.5, rr(S, 2))),
    ]


@icon("shovel", CAT, "Spade with a pointed blade and a T-grip",
      tags=["spade", "dig", "digging", "garden", "construction", "earth"], aliases=["spade"])
def _(S):
    return [
        line(rseg(9, 3, 15, 3)),
        line(rseg(12, 3, 12, 11)),
        shell(rp([(8, 11), (16, 11), (16, 17), (12, 21.5), (8, 17)], r=S.r)),
    ]


@icon("pickaxe", CAT, "Pickaxe with a curved double-pointed head",
      tags=["pick", "mining", "dig", "mine", "rock", "construction"], aliases=["pick"])
def _(S):
    head = rpath([("M", (3.5, 9.5)), ("Q", (12, -0.5), (20.5, 9.5)), ("Q", (12, 3.5), (3.5, 9.5)), ("Z",)])
    return [
        shell(head, stroke_miterlimit="2"),
        shell(rrect(10.25, 6, 3.5, 15.5, rr(S, 1.75))),
    ]


@icon("axe", CAT, "Axe with a curved blade on a long handle",
      tags=["hatchet", "chop", "wood", "lumberjack", "firewood", "camping"], aliases=["hatchet"])
def _(S):
    edge = [(4 - 1.25 * (1 - (2 * t - 1) ** 2), 5.5 + 9.5 * t) for t in (i / 8 for i in range(9))]
    blade = [(11.5, 8)] + edge + [(11.5, 12)]
    return [
        shell(rp(blade, r=S.r), stroke_miterlimit="2"),
        shell(rrect(11.5, 5, 3, 16.5, rr(S, 1.5))),
    ]


# ============================================================================ site safety and access

@icon("hard-hat", CAT, "Safety hard hat with a ridge and a brim",
      tags=["helmet", "safety", "construction", "builder", "worker", "site"], aliases=["safety-helmet"])
def _(S):
    return [
        shell("M4.5 16C4.5 10 7.5 5.5 12 5.5C16.5 5.5 19.5 10 19.5 16Z"),
        shell(rect(2, 16, 20, 3.5, rr(S, 1.75))),
        detail(seg(10, 6.2, 10, 11.5)),
        detail(seg(14, 6.2, 14, 11.5)),
    ]


@icon("ladder", CAT, "Ladder with two rails and rungs",
      tags=["steps", "climb", "stepladder", "access", "construction", "diy"])
def _(S):
    def xl(y):
        return 7.5 - 2 * (y - 2.5) / 19

    def xr(y):
        return 16.5 + 2 * (y - 2.5) / 19
    rungs = [line(seg(xl(y), y, xr(y), y)) for y in (6.5, 11, 15.5)]
    return [line(seg(7.5, 2.5, 5.5, 21.5)), line(seg(16.5, 2.5, 18.5, 21.5)), *rungs]


@icon("brick-wall", CAT, "Wall of bricks laid in a running bond",
      tags=["bricks", "wall", "masonry", "building", "construction", "firewall"], aliases=["bricks"])
def _(S):
    joints = [seg(12, 4, 12, 8), seg(7.5, 8, 7.5, 12), seg(16.5, 8, 16.5, 12),
              seg(12, 12, 12, 16), seg(7.5, 16, 7.5, 20), seg(16.5, 16, 16.5, 20)]
    return [
        shell(rect(3, 4, 18, 16, rr(S, 2.5))),
        *[detail(seg(3, y, 21, y)) for y in (8, 12, 16)],
        *[detail(j) for j in joints],
    ]


# ============================================================================ machines

@icon("bulldozer", CAT, "Bulldozer with a front blade, cab and crawler tracks",
      tags=["dozer", "construction", "earthmoving", "machine", "site", "vehicle"], aliases=["dozer"])
def _(S):
    return [
        shell(rect(8, 15.5, 13.5, 5.5, 2.75)),
        dot(11, 18.25, 1), dot(14.75, 18.25, 1), dot(18.5, 18.25, 1),
        shell(poly([(9, 15.5), (9, 10.5), (13, 10.5), (13, 4.5), (18.5, 4.5), (19.5, 10.5), (21, 10.5), (21, 15.5)], closed=True, r=S.r)),
        shell("M3 10C5 12.5 5 18.5 3 21H6C7.8 18.5 7.8 12.5 6 10Z"),
        line(seg(7.2, 15.5, 9, 13.5)),
    ]


# ============================================================================ fasteners

@icon("nut-bolt", CAT, "Hex bolt beside a hex nut",
      tags=["bolt", "nut", "hardware", "fastener", "hex", "assembly", "mechanical"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 9, 4.5, rr(S, 1.5))),
        detail(seg(5.5, 2.5, 5.5, 7)), detail(seg(8.5, 2.5, 8.5, 7)),
        shell(rect(4.5, 7, 5, 14.5, rr(S, 1.5) if S.name == "rounded" else 0)),
        *[detail(seg(4.5, y + 0.75, 9.5, y - 0.75)) for y in (11.5, 15.5)],
        shell(poly(regular(16.75, 9.5, 5.5, 6, start=-90), closed=True, r=S.r * 0.6)),
        detail(circle(16.75, 9.5, 2)),
    ]


@icon("screw", CAT, "Wood screw with a countersunk head and a threaded point",
      tags=["wood screw", "fastener", "hardware", "thread", "fix", "diy"])
def _(S):
    body = [(5, 3), (19, 3), (14, 7.5), (14, 16), (12, 21.5), (10, 16), (10, 7.5)]
    return [
        shell(poly(body, closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
        *[line(seg(8, y + 1, 16, y - 1)) for y in (10.5, 14.5)],
    ]


@icon("nail", CAT, "Nail with a flat head and a sharp point",
      tags=["nails", "fastener", "hammer", "hardware", "carpentry", "fix"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 3.5, 1.75 if S.name == "rounded" else 0)),
        line(seg(12, 6, 12, 17)),
        solid(poly([(10.75, 16.5), (13.25, 16.5), (12, 21.5)], closed=True)),
    ]


# ============================================================================ mechanical

def _gear(cx, cy, r0, r1, n, phase=0.0, a_base=None, a_tip=None):
    a_base = a_base if a_base is not None else 360 / n * 0.33
    a_tip = a_tip if a_tip is not None else 360 / n * 0.2
    pts = []
    for i in range(n):
        th = phase + i * 360 / n
        pts += [polar(cx, cy, r0, th - a_base), polar(cx, cy, r1, th - a_tip),
                polar(cx, cy, r1, th + a_tip), polar(cx, cy, r0, th + a_base)]
    return pts


def _cogs_paths(S=None):
    r = S.r if S else 0
    big = poly(_gear(8.75, 15.25, 4.75, 6.5, 8, phase=22.5), closed=True, r=r * 0.5)
    small = poly(_gear(17.25, 6.75, 3.25, 4.75, 6, phase=15), closed=True, r=r * 0.4)
    return big, small


def _cogs_filled():
    big, small = _cogs_paths()
    b = D(U(P(big), ST(big, 2)), P(circle(8.75, 15.25, 2.25)))
    sm = D(U(P(small), ST(small, 2)), P(circle(17.25, 6.75, 1.25)), ST(big, 7))
    return U(b, sm)


@icon("cogs", CAT, "Two gears, one in front of the other; machinery or mechanism",
      tags=["gears", "cogwheels", "mechanism", "machine", "engineering", "process"], aliases=["gears"], filled=_cogs_filled)
def _(S):
    from geometry import path_to_d
    big, small = _cogs_paths(S)
    # The small gear sits behind: its outline stops 2 px short of the big gear's outline.
    behind = D(ST(small, 2, S.cap, S.join), U(P(big), ST(big, 6)))
    return [shell(big), detail(circle(8.75, 15.25, 2)), solid(path_to_d(behind)), dot(17.25, 6.75, 1.25)]


def _rope_path():
    pts = []
    turns, r0, r1, a0 = 1.5, 2.25, 8.5, -90.0
    n = 72
    for i in range(n + 1):
        t = i / n
        pts.append(polar(12, 10.5, r0 + (r1 - r0) * t, a0 + 360 * turns * t))
    return pts


@icon("rope", CAT, "Coiled rope with its frayed end trailing off",
      tags=["coil", "cord", "climbing", "tie", "lasso", "sailing"], aliases=["rope-coil"])
def _(S):
    d = poly(_rope_path())
    tail = "L3.5 20.5" if S.name == "line" else "Q5 18.8 3.5 20.5"
    return [line(d + tail)]


@icon("hook", CAT, "Crane hook hanging from an eye",
      tags=["crane hook", "lifting", "hoist", "hanger", "rigging", "construction"], aliases=["crane-hook"])
def _(S):
    tip = [(5, 16), (5, 12), (7.5, 14.5)] if S.name == "line" else [(5, 16), (5, 12.5)]
    return [
        line(circle(13, 5, 2.5)),
        line("M13 7.5V16A4 4 0 0 1 5 16"),
        line(poly(tip, r=S.r)),
    ]


@icon("anvil", CAT, "Blacksmith's anvil with a horn and a stepped base",
      tags=["blacksmith", "forge", "metalwork", "smith", "iron", "heavy"])
def _(S):
    pts = [(2, 5.5), (7, 5), (21.5, 5), (21.5, 9.5), (17, 10.5), (15.5, 15), (18.5, 17), (18.5, 20.5),
           (5.5, 20.5), (5.5, 17), (8.5, 15), (8, 10.5), (5.5, 9.8), (3.5, 8.2)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.8), stroke_miterlimit="2"),
        detail(seg(5.5, 17, 18.5, 17)),
    ]


@icon("welding", CAT, "Welding torch with a burst of sparks at its tip",
      tags=["welder", "weld", "torch", "sparks", "metalwork", "fabrication"], aliases=["welder"])
def _(S):
    sc = (7, 17)
    sparks = [line(seg(*polar(*sc, 1.75, a), *polar(*sc, 4.25, a))) for a in (90, 135, 180, 225)]
    return [
        shell(rrect(9.5, 2, 5, 9.5, rr(S, 2.5))),
        detail(rseg(9.5, 5.5, 14.5, 5.5)),
        line(rseg(12, 11.5, 12, 15.5)),
        *sparks,
    ]


@icon("sandpaper", CAT, "Sheet of sandpaper with grit and a turned-up corner",
      tags=["sanding", "sand", "abrasive", "grit", "smooth", "woodwork"], aliases=["sanding-paper"])
def _(S):
    sheet = [(3, 4), (21, 4), (21, 20), (8, 20), (3, 15)]
    grit = [(7.5, 8), (12, 7.5), (17, 8.5), (9.5, 11.5), (14.5, 12), (17.5, 15.5), (12.5, 16)]
    return [
        shell(poly(sheet, closed=True, r=S.r)),
        detail(poly([(8, 20), (8, 15), (3, 15)], r=S.r * 0.5)),
        *[dot(x, y, 1.1) for x, y in grit],
    ]


@icon("clamp", CAT, "C-clamp with a screw and a T-handle",
      tags=["c-clamp", "g-clamp", "vice", "hold", "woodwork", "grip"], aliases=["c-clamp"])
def _(S):
    cx, cy = 13, 10.25
    outer = [polar(cx, cy, 7.25, a) for a in range(-90, 91, 10)]
    inner = [polar(cx, cy, 3.75, a) for a in range(90, -91, -15)]
    frame = [(6, 3)] + outer + [(6, 17.5), (6, 14)] + inner + [(6, 6.5)]
    return [
        shell(poly(frame, closed=True, r=S.r)),
        line(seg(9.5, 10.25, 9.5, 21)),
        line(seg(7, 10.25, 12, 10.25)),
        line(seg(6.5, 21, 12.5, 21)),
    ]


@icon("utility-knife", CAT, "Utility knife (box cutter) with a snap-off blade",
      tags=["box cutter", "cutter", "knife", "blade", "cut", "craft"], aliases=["box-cutter"])
def _(S):
    return [
        shell(rp([(10, 9.5), (14, 9.5), (14, 3), (10, 6.5)], r=S.r * 0.5), stroke_miterlimit="2"),
        shell(rrect(9, 9.5, 6, 12, rr(S, 2.5))),
        detail(rseg(12, 12.5, 12, 15.5)),
    ]


@icon("blueprint-roll", CAT, "Blueprint unrolling from its roll, showing a floor plan",
      tags=["blueprint", "plan", "architecture", "drawing", "construction", "design"], aliases=["plan-roll"])
def _(S):
    return [
        shell(poly([(6, 2.5), (21, 2.5), (21, 21), (2.5, 21), (2.5, 6)], closed=True, r=S.r)),
        shell(circle(6, 6, 3.5)),
        dot(6, 6, 1.1),
        detail(poly([(11.5, 7), (17.5, 7), (17.5, 17.5), (6, 17.5), (6, 12), (11.5, 12)], closed=True, r=S.r * 0.5)),
        detail(seg(11.5, 14.5, 11.5, 17.5)),
    ]
