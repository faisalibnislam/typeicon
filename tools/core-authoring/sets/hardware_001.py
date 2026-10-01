"""TypeIcon Core: hardware (batch 001): hammers, axes, drivers, wrenches, pliers, cutters, saws, chisels and bars.

Drawn from the objects themselves. Long hand tools follow the tools set: designed upright (working end at the
top, handle at the bottom) and turned 45° clockwise so the handle points to the bottom-left and the working end
to the top-right. Flat objects seen from the top (screw heads, cases, saw blades) stay square to the grid.
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
    """Rotated polygon or polyline."""
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
    """Rotated rounded rectangle."""
    rx = max(0.0, min(rx, w / 2, h / 2))
    if rx == 0:
        return rp([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], deg=deg, c=c)
    return rpath([("M", (x + rx, y)), ("L", (x + w - rx, y)), ("A", rx, 0, 1, (x + w, y + rx)),
                  ("L", (x + w, y + h - rx)), ("A", rx, 0, 1, (x + w - rx, y + h)), ("L", (x + rx, y + h)),
                  ("A", rx, 0, 1, (x, y + h - rx)), ("L", (x, y + rx)), ("A", rx, 0, 1, (x + rx, y)), ("Z",)], deg, c)


def rseg(x1, y1, x2, y2, deg=TILT, c=(12.0, 12.0)) -> str:
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg, *c)
    return seg(a, b, c, d)


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


# ============================================================================ hammers and mallets

@icon("sledgehammer", CAT, "Sledgehammer with a heavy double-faced head on a long handle",
      tags=["sledge", "demolition", "heavy hammer", "smash", "construction", "breaking"], aliases=["sledge-hammer"])
def _(S):
    k = S.r * 0.5
    head = rp([(7, 3), (17, 3), (18.5, 4.5), (18.5, 9), (17, 10.5), (7, 10.5), (5.5, 9), (5.5, 4.5)], r=k)
    return [
        shell(head),
        shell(rrect(10.5, 10.5, 3, 12, rr(S, 1.5))),
    ]


@icon("ball-peen-hammer", CAT, "Ball-peen hammer with a flat face on one end and a round ball on the other",
      tags=["machinist hammer", "engineer hammer", "metalwork", "peening", "hammer", "workshop"],
      aliases=["ball-pein-hammer"])
def _(S):
    head = union(rrect(4.5, 5, 4.5, 7, L(S, 0, 1.75)), rrect(8, 6.75, 7.5, 3.5, L(S, 0, 1.25)), rcircle(17.25, 8.5, 3.25))
    return [
        shell(head),
        shell(rrect(10.5, 10.25, 3, 11.5, rr(S, 1.5))),
    ]


@icon("rubber-mallet", CAT, "Rubber mallet with a fat barrel-shaped head on a short handle",
      tags=["mallet", "soft hammer", "tile setting", "assembly", "knock", "diy"])
def _(S):
    return [
        shell(rrect(4, 3.5, 16, 9.5, L(S, 3.5, 4.75))),
        shell(rrect(10.5, 13, 3, 7.5, rr(S, 1.5))),
    ]


@icon("wooden-mallet", CAT, "Carpenter's wooden mallet with a tapered block head and the handle end showing on top",
      tags=["carpenter mallet", "joiner mallet", "woodwork", "chisel", "beetle", "carpentry"],
      aliases=["carpenters-mallet"])
def _(S):
    k = S.r * 0.6
    head = union(rp([(4.5, 4.5), (19.5, 4.5), (18, 12), (6, 12)], r=k), rrect(10.5, 2.5, 3, 3, rr(S, 1)))
    return [
        shell(head, stroke_miterlimit="2"),
        shell(rp([(10.25, 12), (13.75, 12), (13.25, 21.5), (10.75, 21.5)], r=k)),
    ]


@icon("club-hammer", CAT, "Club hammer: a heavy square double-faced head on a short stubby handle",
      tags=["lump hammer", "mash hammer", "masonry", "chisel", "heavy", "demolition"], aliases=["lump-hammer"])
def _(S):
    return [
        shell(rrect(5, 4.5, 14, 8.5, L(S, 0, 1))),
        detail(rseg(8.5, 4.5, 8.5, 13)),
        detail(rseg(15.5, 4.5, 15.5, 13)),
        shell(rrect(9.5, 13, 5, 6.5, rr(S, 2.5))),
    ]


@icon("rock-hammer", CAT, "Geologist's rock hammer with a square face and a long pointed pick",
      tags=["geology hammer", "rock pick", "geologist", "fossil", "prospecting", "field trip"],
      aliases=["rock-pick", "geologist-hammer"])
def _(S):
    k = S.r * 0.5
    head = union(rrect(4.5, 5, 4.5, 7.5, rr(S, 1)), rp([(8.5, 6.5), (14, 6.5), (20.5, 9), (14, 10.5), (8.5, 10.5)], r=k))
    return [
        shell(head, stroke_miterlimit="2"),
        shell(rrect(10.5, 10.5, 3, 11, rr(S, 1.5))),
    ]


@icon("brick-hammer", CAT, "Mason's brick hammer with a square face and a flat chisel blade",
      tags=["mason hammer", "bricklaying", "masonry", "bricklayer", "chisel", "construction"],
      aliases=["mason-hammer"])
def _(S):
    k = S.r * 0.5
    head = union(rrect(4.5, 5, 4.5, 7.5, rr(S, 1)), rp([(8.5, 6.5), (20, 6.5), (20, 12), (14, 10.5), (8.5, 10.5)], r=k))
    return [
        shell(head, stroke_miterlimit="2"),
        shell(rrect(10.5, 10.5, 3, 11, rr(S, 1.5))),
    ]


@icon("tack-hammer", CAT, "Slim tack hammer with a long narrow head, a split end and a thin handle",
      tags=["upholstery hammer", "tacks", "upholstery", "small hammer", "pins", "craft"],
      aliases=["upholstery-hammer"])
def _(S):
    k = S.r * 0.4
    head = rp([(5.5, 6.5), (19.5, 6.5), (17.5, 8.25), (19.5, 10), (5.5, 10)], r=k)
    return [
        shell(head, stroke_miterlimit="2"),
        line(rseg(12, 10, 12, 21.5)),
    ]


# ============================================================================ axes and digging tools

@icon("splitting-maul", CAT, "Splitting maul: a heavy wedge head with a hammer poll on a long handle",
      tags=["maul", "log splitter", "firewood", "splitting axe", "wood", "chop"], aliases=["maul"])
def _(S):
    k = S.r * 0.6
    head = rp([(5, 4.5), (11, 4.5), (18.5, 3.5), (19.5, 8.25), (18.5, 13), (11, 11), (5, 11)], r=k)
    return [
        shell(head, stroke_miterlimit="2"),
        detail(rseg(9, 4.5, 9, 11)),
        shell(rrect(10.5, 11, 3, 10.5, rr(S, 1.5))),
    ]


@icon("double-bit-axe", CAT, "Double-bit axe with two matching curved blades on a long handle",
      tags=["double axe", "two blade axe", "felling", "lumberjack", "forestry", "wood"],
      aliases=["double-bladed-axe"])
def _(S):
    k = S.r * 0.6
    ts = [i / 8 for i in range(1, 8)]
    left = [(5.5 - 8 * t * (1 - t), 4 + 9 * t) for t in ts]
    right = [(18.5 + 8 * t * (1 - t), 13 - 9 * t) for t in ts]
    head = rp([(10, 7), (5.5, 4)] + left + [(5.5, 13), (10, 10), (14, 10), (18.5, 13)] + right + [(18.5, 4), (14, 7)], r=k)
    return [
        shell(head, stroke_miterlimit="2"),
        shell(rrect(10.5, 10, 3, 11.5, rr(S, 1.5))),
    ]


@icon("adze", CAT, "Adze: a curved blade set at a right angle to the handle",
      tags=["adz", "woodworking", "hewing", "carving", "timber", "shaping"], aliases=["adz"])
def _(S):
    k = S.r * 0.6
    blade = rpath([("M", (13, 3.5)), ("L", (16, 3.5)), ("Q", (20.5, 4), (20.5, 11)), ("L", (17.5, 11)),
                   ("Q", (17.5, 7), (13, 7)), ("Z",)])
    return [
        shell(union(blade, rrect(8.5, 2.5, 5.5, 5.5, rr(S, 1.5))), stroke_miterlimit="2"),
        shell(rrect(9.75, 8, 3.5, 13.5, rr(S, 1.75))),
    ]


@icon("mattock", CAT, "Mattock with a flat digging blade on one side and a pick on the other",
      tags=["pick mattock", "grub hoe", "digging", "roots", "garden", "earthwork"], aliases=["pick-mattock"])
def _(S):
    k = S.r * 0.5
    head = rp([(10, 5), (14, 5), (20, 6), (20.5, 13), (14, 9.5), (10, 9.5), (3.5, 11.5)], r=k)
    return [
        shell(head, stroke_miterlimit="2"),
        shell(rrect(10.5, 9.5, 3, 12, rr(S, 1.5))),
    ]


@icon("hand-tamper", CAT, "Hand tamper: a tall pole with a T-grip and a flat square plate at the bottom",
      tags=["tamper", "compactor", "tamping", "soil", "paving", "landscaping"], aliases=["tamper"])
def _(S):
    k = S.r * 0.6
    plate = union(rect(9.5, 12.5, 5, 5, rr(S, 1)), rect(3, 16, 18, 4.5, rr(S, 1.5)))
    return [
        line(seg(7.5, 3, 16.5, 3)),
        line(seg(12, 3, 12, 12.5)),
        shell(plate),
    ]


# ============================================================================ screwdrivers and bits

@icon("phillips-screwdriver", CAT, "Phillips screwdriver with a grip handle and a pointed cross tip",
      tags=["cross head screwdriver", "crosshead", "screwdriver", "screw", "repair", "assemble"],
      aliases=["crosshead-screwdriver"])
def _(S):
    tip = [(12, 1.5), (13.75, 4.5), (13, 7), (11, 7), (10.25, 4.5)]
    return [
        solid(rp(tip, r=L(S, 0, 0.6))),
        line(rseg(12, 6.5, 12, 10)),
        shell(rrect(9.5, 10, 5, 2.5, rr(S, 1))),
        shell(rrect(8.5, 12.5, 7, 9, rr(S, 3))),
        detail(rseg(12, 15, 12, 19)),
    ]


@icon("bit-set-case", CAT, "Open bit case holding a row of screwdriver bits in slots",
      tags=["bit set", "bit holder", "driver bits", "screwdriver bits", "bit box", "kit"], aliases=["bit-set"])
def _(S):
    parts = [shell(rect(2, 4, 20, 16, rr(S, 3)))]
    for x in (6, 10, 14, 18):
        parts.append(mark(poly([(x - 1, 16.5), (x - 1, 9.5), (x, 7.5), (x + 1, 9.5), (x + 1, 16.5)], closed=True)))
    return parts


# ============================================================================ screw heads (top view)

def _head(S, recess):
    return [shell(circle(12, 12, 9)), mark(recess)]


@icon("phillips-screw-head", CAT, "Top view of a screw head with a cross-shaped Phillips recess",
      tags=["phillips", "cross head", "screw head", "crosshead", "screw", "drive type"], aliases=["phillips-head"])
def _(S):
    w, a, d = 1.1, 5.5, 4  # arm half-width, arm reach, centre diamond half-diagonal
    pts = [(12 + w, 12 - a), (12 + w, 12 - d + w), (12 + d - w, 12 - w), (12 + a, 12 - w), (12 + a, 12 + w),
           (12 + d - w, 12 + w), (12 + w, 12 + d - w), (12 + w, 12 + a), (12 - w, 12 + a), (12 - w, 12 + d - w),
           (12 - d + w, 12 + w), (12 - a, 12 + w), (12 - a, 12 - w), (12 - d + w, 12 - w), (12 - w, 12 - d + w),
           (12 - w, 12 - a)]
    return _head(S, poly(pts, closed=True, r=L(S, 0, 0.9)))


@icon("slotted-screw-head", CAT, "Top view of a screw head with a single straight slot",
      tags=["slotted", "flat head", "slot head", "screw head", "screw", "drive type"], aliases=["slot-screw-head"])
def _(S):
    pts = rot([(5.5, 10.5), (18.5, 10.5), (18.5, 13.5), (5.5, 13.5)], -25)
    return _head(S, poly(pts, closed=True, r=L(S, 0, 1.4)))


@icon("torx-screw-head", CAT, "Top view of a screw head with a six-lobed star recess",
      tags=["star drive", "hexalobular", "six lobe", "screw head", "star screw", "drive type"], aliases=["star-drive-screw-head"])
def _(S):
    pts = []
    for i in range(6):
        pts += [polar(12, 12, 5, -90 + i * 60), polar(12, 12, 2.75, -60 + i * 60)]
    return _head(S, poly(pts, closed=True, r=L(S, 0, 1.1)))


@icon("hex-socket-screw-head", CAT, "Top view of a screw head with a hexagonal socket",
      tags=["hex socket", "allen screw", "socket head", "screw head", "hex drive", "drive type"],
      aliases=["allen-screw-head"])
def _(S):
    return _head(S, poly(regular(12, 12, 5, 6, start=0), closed=True, r=L(S, 0, 2.5)))


@icon("square-drive-screw-head", CAT, "Top view of a screw head with a small square recess",
      tags=["square drive", "robertson", "square recess", "screw head", "screw", "drive type"],
      aliases=["robertson-screw-head"])
def _(S):
    return _head(S, rect(8.75, 8.75, 6.5, 6.5, L(S, 0, 1.5)))


# ============================================================================ wrenches and keys

@icon("adjustable-wrench", CAT, "Adjustable wrench with an angled open jaw and a worm-screw adjuster",
      tags=["adjustable spanner", "shifter", "wrench", "bolt", "repair", "plumbing"],
      aliases=["adjustable-spanner"])
def _(S):
    k = S.r * 0.6
    head = [(10, 13), (6.5, 10.5), (6, 5.5), (8, 2.5), (10.5, 2.5), (10.5, 7), (13.5, 7), (13.5, 4.5), (16.5, 4.5),
            (18, 7), (17.5, 10.5), (14, 13)]
    return [
        shell(union(rp(head, r=k), rrect(10, 12, 4, 9.5, rr(S, 2))), stroke_miterlimit="2"),
        detail(rseg(13.5, 9.75, 17.5, 9.75)),
    ]


@icon("box-end-wrench", CAT, "Double box-end wrench with a closed ring at each end",
      tags=["ring spanner", "box wrench", "ring wrench", "spanner", "bolt", "mechanic"],
      aliases=["ring-spanner"])
def _(S):
    body = union(rcircle(12, 5, 4.75), rcircle(12, 19, 4.25), rrect(10.5, 5, 3, 14, L(S, 0, 1.5)))
    holes = [rp(regular(12, 5, 2.5, 6, start=0), r=L(S, 0, 0.8)), rp(regular(12, 19, 2.1, 6, start=0), r=L(S, 0, 0.8))]
    return [shell(minus(body, *holes))]


@icon("pipe-wrench", CAT, "Pipe wrench with a hooked toothed jaw, an adjusting nut and a long handle",
      tags=["plumber wrench", "monkey wrench", "plumbing", "pipe", "grip", "wrench"])
def _(S):
    k = S.r * 0.5
    hook = [(9.5, 11), (9.5, 3.5), (17.5, 3.5), (17.5, 5.75), (16.5, 7), (15.5, 5.75), (14.5, 7), (13.5, 5.75),
            (12, 5.75), (12, 11)]
    jaw = [(12, 13), (12, 11.5), (13, 10.25), (14, 11.5), (15, 10.25), (16, 11.5), (17, 10.25), (17, 13), (14, 15),
           (14, 21.5), (10, 21.5), (10, 13)]
    return [
        shell(union(rp(hook, r=k), rrect(7, 7.5, 5, 3.5, L(S, 0, 1))), stroke_miterlimit="2"),
        shell(rp(jaw, r=k), stroke_miterlimit="2"),
    ]


@icon("wrench-socket", CAT, "Wrench socket: a short cylinder with a hexagonal opening on top",
      tags=["socket", "hex socket", "drive socket", "ratchet socket", "mechanic", "bolt"], aliases=["drive-socket"])
def _(S):
    body = "M5 7.5L5 17A7 3.5 0 0 0 19 17L19 7.5A7 3.5 0 0 0 5 7.5Z"
    hexa = [(8, 7.5), (10, 5.5), (14, 5.5), (16, 7.5), (14, 9.5), (10, 9.5)]
    return [
        shell(body),
        detail("M5 7.5A7 3.5 0 0 0 19 7.5"),
        mark(poly(hexa, closed=True, r=L(S, 0, 0.9))),
        detail("M5 13.5A7 3.5 0 0 0 19 13.5"),
    ]


@icon("allen-key", CAT, "L-shaped hex key with a long and a short leg",
      tags=["hex key", "allen wrench", "hex wrench", "furniture assembly", "flat pack", "diy"],
      aliases=["hex-key", "allen-wrench"])
def _(S):
    pts = [(10.5, 20.5), (10.5, 3.5), (18.5, 3.5), (18.5, 6.5), (13.5, 6.5), (13.5, 20.5)]
    return [shell(rp(pts, r=L(S, 0, 1.5)))]


@icon("lug-wrench", CAT, "Cross-shaped lug wrench with a socket on the end of each arm",
      tags=["wheel brace", "tire iron", "cross wrench", "wheel nut", "flat tire", "car"],
      aliases=["wheel-brace", "cross-wrench"])
def _(S):
    parts = [line(seg(6.5, 6.5, 17.5, 17.5)), line(seg(17.5, 6.5, 6.5, 17.5))]
    for deg, w in ((45, 3.5), (135, 4), (225, 4.5), (315, 5)):
        parts.append(shell(rrect(12 - w / 2, 1.5, w, 4, L(S, 0, 1.5), deg=deg)))
    return parts


# ============================================================================ pliers and cutters

def _pivot(S, y=13.5, r=2.5):
    return shell(rpath([("M", (12 - r, y)), ("A", r, 1, 1, (12 + r, y)), ("A", r, 0, 1, (12 - r, y)), ("Z",)]))


def _handles(S, y0=15.5, spread=4.5, bow=2.0, end=21.5):
    """Two curved handle strokes below the pivot."""
    return [line(rpath([("M", (12 - 1.5, y0)), ("Q", (12 - 1.5 - bow, (y0 + end) / 2 + 1), (12 - spread, end))])),
            line(rpath([("M", (12 + 1.5, y0)), ("Q", (12 + 1.5 + bow, (y0 + end) / 2 + 1), (12 + spread, end))]))]


@icon("diagonal-cutters", CAT, "Diagonal cutters with short pointed cutting jaws and curved handles",
      tags=["side cutters", "wire cutters", "snips", "nippers", "electrician", "cut wire"],
      aliases=["side-cutters", "wire-cutters"])
def _(S):
    return [
        shell(rp([(9.25, 11), (9.75, 7.5), (12, 4), (14.25, 7.5), (14.75, 11)], r=S.r * 0.6), stroke_miterlimit="2"),
        detail(rseg(12, 5.5, 12, 11)),
        _pivot(S),
        *_handles(S),
    ]


@icon("lineman-pliers", CAT, "Heavy lineman's pliers with blunt square jaws",
      tags=["linesman pliers", "combination pliers", "electrician", "heavy pliers", "twist wire", "grip"],
      aliases=["linesman-pliers", "combination-pliers"])
def _(S):
    return [
        shell(rrect(9, 3.5, 6, 7.5, L(S, 0, 1.5))),
        detail(rseg(12, 3.5, 12, 11)),
        _pivot(S),
        line(rseg(10.5, 15.5, 9, 21.5)),
        line(rseg(13.5, 15.5, 15, 21.5)),
    ]


@icon("snap-ring-pliers", CAT, "Snap ring pliers with two thin jaws ending in bent pin tips",
      tags=["circlip pliers", "retaining ring", "circlip", "snap ring", "mechanic", "pliers"],
      aliases=["circlip-pliers"])
def _(S):
    return [
        line(rp([(10.5, 11), (9.5, 5), (7, 3.5)], closed=False, r=S.r * 0.6)),
        line(rp([(13.5, 11), (14.5, 5), (17, 3.5)], closed=False, r=S.r * 0.6)),
        _pivot(S),
        *_handles(S),
    ]


@icon("wire-stripper", CAT, "Wire stripper with long straight jaws and a row of graduated notches",
      tags=["wire strippers", "strip wire", "electrician", "insulation", "cable", "gauge"], aliases=["wire-strippers"])
def _(S):
    return [
        shell(rrect(9.25, 2.5, 5.5, 9, L(S, 0.5, 2.25))),
        mark(rcircle(12, 5, 0.9)), mark(rcircle(12, 8.75, 1.2)),
        _pivot(S),
        *_handles(S),
    ]


@icon("bolt-cutters", CAT, "Bolt cutters with short heavy jaws and two very long handles",
      tags=["bolt cutter", "chain cutter", "lock cutter", "cut padlock", "heavy cutter", "security"],
      aliases=["bolt-cutter"])
def _(S):
    return [
        shell(rp([(10, 7.5), (12, 1.5), (14, 7.5)], r=S.r * 0.4), stroke_miterlimit="2"),
        shell(rrect(9.5, 7.5, 5, 4, L(S, 0, 1.5))),
        line(rseg(10.5, 11.5, 7.5, 22)),
        line(rseg(13.5, 11.5, 16.5, 22)),
    ]


@icon("tin-snips", CAT, "Tin snips with short thick curved blades and long cushioned handles",
      tags=["aviation snips", "metal shears", "sheet metal", "snips", "shears", "cut metal"],
      aliases=["aviation-snips", "metal-shears"])
def _(S):
    k = S.r * 0.5
    return [
        shell(rpath([("M", (12, 11)), ("L", (10, 11)), ("Q", (9.5, 5.5), (12.5, 2.5)), ("Q", (12.5, 7), (12, 11)), ("Z",)])),
        shell(rpath([("M", (12.5, 11)), ("L", (14, 11)), ("Q", (15, 6), (13.5, 4.5)), ("Q", (13.5, 8), (12.5, 11)), ("Z",)])),
        dot(*rot([(12, 12.5)])[0], 1.25),
        shell(rp([(9.5, 14.5), (11, 15), (8.5, 21.5), (6.5, 21)], r=L(S, 0, 1))),
        shell(rp([(14.5, 14.5), (13, 15), (15.5, 21.5), (17.5, 21)], r=L(S, 0, 1))),
    ]


@icon("glass-cutter", CAT, "Glass cutter: a slim handle with a tiny cutting wheel at the tip and a ball at the end",
      tags=["glass cutting", "score glass", "glazier", "window", "tile", "stained glass"])
def _(S):
    return [
        shell(rp([(9.5, 3.5), (14.5, 3.5), (13.5, 7), (10.5, 7)], r=S.r * 0.5)),
        dot(*rot([(12, 1.75)])[0], 1.1),
        shell(rrect(10.5, 7, 3, 11, L(S, 0, 1.5))),
        shell(rcircle(12, 20, 2)),
    ]


# ============================================================================ saws and blades

def _teeth(x0, x1, y, n, depth=1.25, down=True):
    """Sawtooth points from x0 to x1 along y (teeth pointing down when down=True)."""
    pts = []
    step = (x1 - x0) / n
    sgn = 1 if down else -1
    for i in range(n):
        pts += [(x0 + i * step, y), (x0 + (i + 0.5) * step, y + sgn * depth)]
    pts.append((x1, y))
    return pts


@icon("hacksaw", CAT, "Hacksaw: a metal frame holding a thin toothed blade, with a pistol grip",
      tags=["hack saw", "metal saw", "cut metal", "pipe", "bolt", "saw"], aliases=["hack-saw"])
def _(S):
    teeth = _teeth(21, 9, 14.5, 6, 1.25)
    return [
        line(poly([(9, 12.5), (9, 4.5), (21, 4.5), (21, 12.5)], r=S.r)),
        shell(poly([(9, 12.5), (21, 12.5)] + teeth, closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        shell(poly([(4, 9.5), (8.5, 9.5), (8.5, 14), (7, 20.5), (3, 20.5)], closed=True, r=S.r)),
    ]


@icon("coping-saw", CAT, "Coping saw: a deep U-shaped frame with a very thin blade and a straight handle",
      tags=["fret saw", "scroll saw", "curved cuts", "woodwork", "joinery", "saw"], aliases=["fret-saw"])
def _(S):
    return [
        line(rp([(14.5, 3.5), (6.5, 3.5), (6.5, 13.5), (14.5, 13.5)], closed=False, r=L(S, 0, 3))),
        line(rseg(14.5, 3.5, 14.5, 13.5)),
        shell(rrect(12.75, 13.5, 3.5, 8, rr(S, 1.75))),
    ]


@icon("bow-saw", CAT, "Bow saw: a curved tubular frame with a wide toothed blade across its open side",
      tags=["buck saw", "pruning saw", "firewood", "logs", "camping", "saw"], aliases=["buck-saw"])
def _(S):
    teeth = _teeth(21, 3, 16, 7, 1.5)
    return [
        line("M21 14C18.5 8.5 11 4 5.5 4C3.5 4 3 8 3 14"),
        shell(poly([(3, 14), (21, 14)] + teeth, closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
    ]


@icon("keyhole-saw", CAT, "Keyhole saw: a narrow pointed toothed blade sticking out of a grip handle",
      tags=["jab saw", "drywall saw", "compass saw", "plasterboard", "hole cutting", "saw"],
      aliases=["jab-saw", "drywall-saw"])
def _(S):
    edge = [(9.75 + 0.25 * t, 13 - 10.5 * t) for t in (i / 8 for i in range(9))]
    zig = []
    for i in range(8):
        (xa, ya), (xb, yb) = edge[i], edge[i + 1]
        zig += [(xa, ya), ((xa + xb) / 2 - 1.2, (ya + yb) / 2)]
    blade = [(14, 13), (13.5, 8), (10.25, 2)] + [p for p in zig[::-1]]
    return [
        shell(rp(blade, r=S.r * 0.3), stroke_miterlimit="2"),
        shell(rrect(9, 13, 6, 8.5, rr(S, 3))),
        detail(rseg(12, 15.75, 12, 18.75)),
    ]


@icon("pull-saw", CAT, "Pull saw: a thin straight blade with fine teeth on a long cord-wrapped handle",
      tags=["japanese saw", "ryoba", "dozuki", "flush cut", "woodwork", "saw"], aliases=["japanese-saw"])
def _(S):
    teeth = [(10.5, 11)]
    for i in range(6):
        y = 11 - i * 1.5
        teeth += [(9.5 + 0.1 * i, y - 0.75), (10.5 - 0.1 * i, y - 1.5)]
    blade = [(13.5, 11), (14.5, 2.5), (9.5, 2)] + teeth[::-1]
    return [
        shell(rp(blade, r=S.r * 0.3), stroke_miterlimit="2"),
        shell(rrect(10.5, 11, 3, 11, rr(S, 1.5))),
        *[detail(rseg(10.5, y, 13.5, y)) for y in (14.5, 18)],
    ]


@icon("hole-saw", CAT, "Hole saw: a toothed cup with a pilot drill bit through its centre",
      tags=["hole cutter", "core bit", "drill attachment", "cut holes", "downlight", "plumbing"],
      aliases=["hole-cutter"])
def _(S):
    teeth = _teeth(19, 5, 16, 6, 1.5)
    return [
        line(seg(12, 2.5, 12, 7)),
        shell(poly([(5, 7), (19, 7)] + teeth, closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
        line(seg(12, 16, 12, 19.5)),
        solid(poly([(11, 19.4), (13, 19.4), (12, 21.75)], closed=True)),
    ]


@icon("circular-saw-blade", CAT, "Circular saw blade: a round disc with hooked teeth and a centre hole",
      tags=["saw blade", "circular saw", "disc blade", "cutting disc", "power saw", "woodwork"],
      aliases=["saw-blade"])
def _(S):
    pts = []
    n = 12
    for i in range(n):
        a = i * 360 / n
        pts += [polar(12, 12, 7.5, a), polar(12, 12, 10, a + 8), polar(12, 12, 9, a + 26)]
    return [
        shell(poly(pts, closed=True, r=L(S, 0, 0.6)), stroke_miterlimit="2"),
        detail(circle(12, 12, 2.25)),
    ]


@icon("jigsaw-blade", CAT, "Jigsaw blade: a short narrow toothed blade with a notched tang at the top",
      tags=["jig saw blade", "sabre saw blade", "t shank", "power tool", "blade", "scroll cut"],
      aliases=["jig-saw-blade"])
def _(S):
    zig = []
    for i in range(5):
        y = 9.5 + i * 2.3
        zig += [(9.75, y), (8.5, y + 1.15)]
    blade = [(9, 2), (15, 2), (15, 4.5), (13.75, 4.5), (13.75, 7), (14.25, 9.5), (14.25, 19.5), (12, 21.5),
             (9.75, 21.5)] + zig[::-1] + [(10.25, 7), (10.25, 4.5), (9, 4.5)]
    return [shell(rp(blade, r=S.r * 0.3), stroke_miterlimit="2")]


# ============================================================================ chisels, planes and files

@icon("wood-chisel", CAT, "Wood chisel: a flat bevelled steel blade set into a wooden handle",
      tags=["chisel", "bench chisel", "woodwork", "carpentry", "joinery", "mortise"], aliases=["bench-chisel"])
def _(S):
    return [
        shell(rrect(9.5, 2, 5, 9, L(S, 0, 1))),
        detail(rseg(9.5, 4.75, 14.5, 4.75)),
        line(rseg(12, 11, 12, 12.5)),
        shell(rrect(9, 12.5, 6, 9, rr(S, 3))),
    ]


@icon("cold-chisel", CAT, "Cold chisel: a short thick steel bar with a wedge edge and a mushroomed striking end",
      tags=["chisel", "masonry chisel", "metal chisel", "cut rivet", "demolition", "hammer and chisel"],
      aliases=["masonry-chisel"])
def _(S):
    k = S.r * 0.5
    pts = [(11, 2.5), (13, 2.5), (14, 7.5), (14, 17.5), (16.5, 19.5), (16, 21.5), (8, 21.5), (7.5, 19.5), (10, 17.5), (10, 7.5)]
    return [shell(rp(pts, r=k), stroke_miterlimit="2")]


@icon("hand-plane", CAT, "Hand plane in side view: a low body with a front knob, a rear handle and an angled blade",
      tags=["block plane", "jack plane", "wood plane", "planing", "smoothing", "carpentry"],
      aliases=["wood-plane"])
def _(S):
    k = S.r * 0.6
    return [
        shell(poly([(2.5, 20), (21.5, 20), (21.5, 16.5), (19.5, 15), (4.5, 15), (2.5, 16.5)], closed=True, r=k)),
        shell(rect(16.5, 10.5, 4, 4.5, L(S, 1, 2))),
        shell(poly([(4, 15), (5.5, 7.5), (9.5, 7.5), (8.5, 15)], closed=True, r=k)),
        line(seg(11.5, 15, 13.5, 8.5)),
    ]


@icon("wood-rasp", CAT, "Wood rasp: a flat file covered with raised teeth, on a wooden handle",
      tags=["rasp", "file", "shaping", "woodwork", "smoothing", "farrier"])
def _(S):
    parts = [shell(rrect(8.5, 1.5, 7, 12, L(S, 1, 3.5))), line(rseg(12, 13.5, 12, 15)),
             shell(rrect(9.5, 15, 5, 7, rr(S, 2.5)))]
    for y in (5, 8, 11):
        parts += [mark(rcircle(10.75, y, 0.75)), mark(rcircle(13.25, y - 1.5, 0.75))]
    return parts


@icon("metal-file", CAT, "Metal file: a long flat tapering blade with diagonal teeth and a handle",
      tags=["file", "hand file", "flat file", "deburr", "metalwork", "sharpening"], aliases=["hand-file"])
def _(S):
    k = S.r * 0.4
    return [
        shell(rp([(9, 13.5), (10, 2), (14, 2), (15, 13.5)], r=k)),
        *[detail(rseg(9.4, y + 1.5, 14.6, y - 1.5)) for y in (6, 10.5)],
        line(rseg(12, 13.5, 12, 15)),
        shell(rrect(9.5, 15, 5, 7, rr(S, 2.5))),
    ]


# ============================================================================ knives, punches and bars

@icon("putty-knife", CAT, "Putty knife: a flat wide flexible blade on a short fat handle",
      tags=["filling knife", "scraper", "spackle", "filler", "decorating", "plaster"], aliases=["filling-knife"])
def _(S):
    k = S.r * 0.6
    return [
        shell(rp([(7.5, 3), (16.5, 3), (14.5, 11), (9.5, 11)], r=L(S, 0, 2))),
        line(rseg(12, 11, 12, 13)),
        shell(rrect(9, 13, 6, 8.5, rr(S, 3))),
    ]


@icon("awl", CAT, "Awl: a round bulb handle with a thin sharp steel spike",
      tags=["scratch awl", "bradawl", "pierce", "leatherwork", "punch hole", "marking"], aliases=["bradawl"])
def _(S):
    return [
        solid(rp([(11, 5), (13, 5), (12, 1.5)], r=0)),
        line(rseg(12, 4.5, 12, 10.5)),
        shell(rrect(10.5, 10.5, 3, 2, L(S, 0, 0.75))),
        shell(rpath([("M", (10, 12.5)), ("L", (14, 12.5)), ("C", (17, 14), (16.5, 21.5), (12, 21.5)),
                     ("C", (7.5, 21.5), (7, 14), (10, 12.5)), ("Z",)]) if S.name == "rounded" else
              rp([(10, 12.5), (14, 12.5), (16, 15), (15.5, 21.5), (8.5, 21.5), (8, 15)])),
    ]


@icon("nail-set", CAT, "Nail set: a short knurled rod with a cupped tip placed on a nail head",
      tags=["nail punch", "countersink nail", "finish nails", "trim", "carpentry", "punch"], aliases=["nail-punch"])
def _(S):
    k = S.r * 0.5
    return [
        shell(poly([(9, 2.5), (15, 2.5), (15, 9.5), (13, 13.5), (11, 13.5), (9, 9.5)], closed=True, r=k)),
        detail(seg(9, 6, 15, 6)),
        line(seg(7.5, 16, 16.5, 16)),
        line(seg(12, 16, 12, 21.5)),
    ]


@icon("crowbar", CAT, "Crowbar: a long steel bar with a curved hook at one end and a bent tip at the other",
      tags=["wrecking bar", "pry bar", "gooseneck", "demolition", "lever", "pry"], aliases=["wrecking-bar"])
def _(S):
    return [
        line("M4 21L15.5 9.5A3.5 3.5 0 0 1 20.5 14.5"),
        line(poly([(4.5, 20.5), (3, 20.5), (2.5, 18)], r=S.r * 0.6)),
    ]
