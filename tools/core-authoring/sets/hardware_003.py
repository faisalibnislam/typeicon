"""TypeIcon Core: hardware (batch 003): measuring instruments, fasteners, springs, hooks, hinges, latches and rigging.

Drawn from the objects themselves, flat and square to the grid unless a diagonal reads better (pens, pegs).
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


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def kdot(d) -> Part:
    """Small solid shape that is knocked out of a Filled shell."""
    return Part("dot", d)


# ============================================================================ measuring and testing

@icon("plumb-bob", CAT, "Pointed plumb bob hanging from a vertical string",
      tags=["plumb line", "vertical", "surveying", "builder", "masonry", "tool"])
def _(S):
    return [
        line(seg(12, 2, 12, 8)),
        shell(poly([(9, 8), (15, 8), (16, 11.5), (12, 21.5), (8, 11.5)], closed=True, r=S.r)),
        detail(seg(8.5, 12, 15.5, 12)),
    ]


@icon("chalk-line-reel", CAT, "Teardrop chalk line reel with a crank and a string",
      tags=["chalk line", "snap line", "string line", "layout", "marking", "carpentry"])
def _(S):
    return [
        shell("M3.75 13.84A6.5 6.5 0 1 1 14.25 13.84L9 21Z" if S.name == "line" else
              "M3.75 13.84A6.5 6.5 0 1 1 14.25 13.84L10.1 19.4Q9 20.9 7.9 19.4Z"),
        dot(9, 10, 1.25),
        line(seg(9, 10, 16.5, 4.5)),
        dot(17.5, 3.7, 1.6),
        line(seg(12, 20.5, 21.5, 20.5)),
    ]


@icon("laser-level", CAT, "Laser level on a tripod projecting crossing beams",
      tags=["line laser", "cross line laser", "levelling", "alignment", "construction", "tool"])
def _(S):
    return [
        shell(rect(8, 9, 8, 5, rr(S, 2))),
        line(seg(12, 2, 12, 6)),
        line(seg(2, 11.5, 6, 11.5)),
        line(seg(18, 11.5, 22, 11.5)),
        line(seg(10.5, 14, 6.5, 22)),
        line(seg(13.5, 14, 17.5, 22)),
        line(seg(12, 14, 12, 22)),
    ]


@icon("laser-distance-meter", CAT, "Handheld laser distance meter with a screen and a dashed beam",
      tags=["laser measure", "distance measure", "range finder", "room measuring", "construction", "tool"])
def _(S):
    return [
        shell(rect(6.5, 10, 11, 12, rr(S, 3))),
        detail(seg(9.5, 13.5, 14.5, 13.5)),
        dot(12, 18, 1.5),
        line(seg(12, 2, 12, 4)),
        line(seg(12, 6, 12, 7)),
    ]


@icon("stud-finder", CAT, "Handheld stud finder with indicator lights and a sensor window",
      tags=["wall scanner", "stud sensor", "joist", "drywall", "diy", "tool"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, 5 + S.R * 0.5)),
        dot(8.5, 6.5, 1.0),
        dot(12, 6.5, 1.0),
        dot(15.5, 6.5, 1.0),
        detail(circle(12, 14, 3.5)),
    ]


@icon("measuring-wheel", CAT, "Measuring wheel on a long handle with a counter box",
      tags=["distance wheel", "surveyor wheel", "trundle wheel", "odometer", "length", "tool"])
def _(S):
    return [
        shell(circle(8, 17, 4)),
        dot(8, 17, 1.25),
        line(seg(8, 17, 16.5, 7.5)),
        shell(rect(14, 2.5, 7, 5, 2.5 if S.name == "rounded" else 0)),
    ]


@icon("folding-ruler", CAT, "Folding ruler with two hinged segments opened at an angle and tick marks",
      tags=["carpenter rule", "zigzag rule", "measure", "length", "woodworking", "tool"])
def _(S):
    hx, hy = 12.5, 17.5
    a = [(2, hy - 3), (hx, hy - 3), (hx, hy + 3), (2, hy + 3)]
    b = rot([(hx, hy - 3), (hx + 11, hy - 3), (hx + 11, hy + 3), (hx, hy + 3)], -55, hx, hy)
    body = U(P(poly(a, closed=True)), P(poly(b, closed=True)))
    t1 = [seg(5.5, hy - 3, 5.5, hy), seg(9, hy - 3, 9, hy - 0.5)]
    (x1, y1), (x2, y2) = rot([(hx + 4, hy - 3), (hx + 4, hy - 0.5)], -55, hx, hy)
    (x3, y3), (x4, y4) = rot([(hx + 7.5, hy - 3), (hx + 7.5, hy)], -55, hx, hy)
    return [
        shell(path_to_d(body)),
        detail(t1[0]), detail(t1[1]),
        detail(seg(x1, y1, x2, y2)), detail(seg(x3, y3, x4, y4)),
    ]


@icon("moisture-meter", CAT, "Handheld moisture meter with a screen and two metal pins",
      tags=["damp meter", "humidity probe", "wood moisture", "water damage", "inspection", "tool"])
def _(S):
    return [
        line(seg(9, 2, 9, 7)),
        line(seg(15, 2, 15, 7)),
        shell(rect(6, 7, 12, 15, rr(S, 3))),
        detail(seg(9, 11, 15, 11)),
        dot(12, 17, 1.5),
    ]


@icon("infrared-thermometer", CAT, "Pistol-shaped infrared thermometer with a display and a dashed beam",
      tags=["temperature gun", "laser thermometer", "non-contact", "heat", "scan", "tool"])
def _(S):
    return [
        shell(poly([(2, 5), (12, 5), (16, 7.5), (16, 10.5), (12, 12), (11, 12), (9, 21), (4, 21), (6, 12), (2, 12)], closed=True, r=S.r)),
        detail(seg(4.5, 8.5, 9, 8.5)),
        line(seg(19, 9, 22, 9)),
    ]


@icon("pressure-gauge", CAT, "Round pressure gauge with a needle and a threaded stem",
      tags=["manometer", "psi", "dial gauge", "plumbing", "air pressure", "tool"])
def _(S):
    return [
        shell(circle(12, 9.5, 7.5)),
        line(seg(12, 9.5, 15.5, 6)),
        dot(12, 9.5, 1.5),
        shell(rect(9, 17, 6, 3, rr(S, 1))),
        line(seg(12, 20, 12, 22)),
    ]


@icon("multimeter", CAT, "Multimeter with a display, a selector dial and two test leads",
      tags=["voltmeter", "electrical tester", "volt meter", "electronics", "circuit test", "tool"])
def _(S):
    return [
        shell(rect(4, 2, 16, 15, rr(S, 3))),
        detail(seg(7.5, 6, 16.5, 6)),
        detail(circle(12, 12, 2.2)),
        line(poly([(8, 17), (8, 20), (5, 22)], r=S.r * 0.5)),
        line(poly([(16, 17), (16, 20), (19, 22)], r=S.r * 0.5)),
    ]


@icon("clamp-meter", CAT, "Clamp meter with an open jaw ring around a wire and a display body",
      tags=["current clamp", "amp meter", "ammeter", "electrician", "circuit test", "tool"])
def _(S):
    return [
        line(arc(12, 7, 5.5, -60, 240)),
        dot(12, 7, 1.5),
        shell(rect(8, 12.5, 8, 9.5, rr(S, 2))),
        detail(seg(10.5, 16, 13.5, 16)),
    ]


@icon("voltage-tester-pen", CAT, "Pen-shaped voltage tester with a pointed tip, a clip and a lightning mark",
      tags=["non-contact tester", "voltage detector", "electrician pen", "live wire", "electrical", "tool"])
def _(S):
    bolt = rot([(13.2, 10), (10.6, 14.2), (12.4, 14.2), (10.8, 18.2), (13.6, 13.6), (11.8, 13.6)])
    return [
        shell(rp([(12, 1.5), (15, 7), (15, 21.5), (9, 21.5), (9, 7)], r=S.r * 0.4)),
        line(rp([(15, 10), (17.5, 10), (17.5, 16)], closed=False, r=S.r * 0.4)),
        kdot(poly(bolt, closed=True)),
    ]


@icon("contour-gauge", CAT, "Contour gauge: a bar holding parallel pins shaped to a wavy profile",
      tags=["profile gauge", "shape duplicator", "template tool", "copy profile", "flooring", "tool"])
def _(S):
    return [
        shell(rect(2, 2.5, 20, 4, rr(S, 1.5))),
        line(seg(4, 6.5, 4, 15)),
        line(seg(8, 6.5, 8, 20)),
        line(seg(12, 6.5, 12, 21.5)),
        line(seg(16, 6.5, 16, 17)),
        line(seg(20, 6.5, 20, 12.5)),
    ]


@icon("angle-finder", CAT, "Angle finder with two hinged arms and a round dial at the joint",
      tags=["angle gauge", "bevel gauge", "protractor rule", "mitre", "carpentry", "tool"])
def _(S):
    ox, oy = 6.5, 17
    tip = polar(ox, oy, 15, -50)
    st = polar(ox, oy, 3.5, -50)
    return [
        shell(circle(ox, oy, 3.5)),
        dot(ox, oy, 1.25),
        line(seg(10, oy, 22, oy)),
        line(arc(ox, oy, 9.5, -42, -12)),
        line(seg(st[0], st[1], tip[0], tip[1])),
    ]


@icon("marking-gauge", CAT, "Marking gauge: a fence block with a beam and a small marking pin at the end",
      tags=["scratch gauge", "woodworking", "layout", "joinery", "carpentry", "marking tool"])
def _(S):
    return [
        shell(rect(2, 5.5, 7, 13, rr(S, 2))),
        shell(rect(9, 10, 13, 4, 2 if S.name == "rounded" else 0)),
        dot(5.5, 12, 1.25),
        line(seg(19.5, 14, 19.5, 20)),
    ]


@icon("carpenter-pencil", CAT, "Flat carpenter pencil with a chisel-shaped lead point",
      tags=["flat pencil", "woodworking", "marking", "layout", "joiner", "builder"])
def _(S):
    return [
        shell(rp([(9, 21.5), (9, 8), (13, 2.5), (15, 4.5), (15, 21.5)], r=S.r * 0.4), stroke_miterlimit="2"),
        detail(rseg(9, 8.5, 15, 8.5)),
        detail(rseg(12, 13, 12, 18.5)),
    ]


@icon("scribe-tool", CAT, "Slim scribe with a fine point at one end and a bent point at the other",
      tags=["scriber", "marking tool", "metalwork", "layout", "engraving", "scratch awl"])
def _(S):
    return [
        shell(rp([(12, 1.5), (14.5, 6), (14.5, 16), (9.5, 16), (9.5, 6)], r=S.r * 0.4)),
        detail(rseg(9.5, 10.5, 14.5, 10.5)),
        line(rp([(12, 16), (12, 21), (16.5, 21)], closed=False, r=S.r * 0.5)),
    ]


def _zig(ox, oy, deg, r0, r1, n, amp):
    """Sawtooth polyline from radius r0 to r1 along direction deg, teeth on one side."""
    a = math.radians(deg)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    pts = [(ox + ux * r0, oy + uy * r0)]
    step = (r1 - r0) / n
    for i in range(n):
        t0 = r0 + i * step
        pts.append((ox + ux * (t0 + step * 0.75) + nx * amp, oy + uy * (t0 + step * 0.75) + ny * amp))
        pts.append((ox + ux * (t0 + step) , oy + uy * (t0 + step)))
    return pts


@icon("thread-gauge", CAT, "Thread gauge: a fan of thin leaves with toothed edges pivoting on one pin",
      tags=["screw pitch gauge", "pitch gauge", "thread checker", "metric", "bolt size", "measuring"])
def _(S):
    ox, oy = 4.5, 19.5
    parts = [shell(circle(ox, oy, 2.7))]
    for deg in (0, -36, -72):
        a = math.radians(deg)
        ux, uy = math.cos(a), math.sin(a)
        nx, ny = uy, -ux   # toward the next leaf (counter-clockwise on screen)
        s0 = (ox + 2.7 * ux, oy + 2.7 * uy)
        e0 = (ox + 18 * ux, oy + 18 * uy)
        parts.append(line(seg(s0[0], s0[1], e0[0], e0[1])))
        for r in (10, 14, 18):
            parts.append(line(seg(ox + r * ux, oy + r * uy, ox + r * ux + 2.6 * nx, oy + r * uy + 2.6 * ny)))
    return parts


@icon("inspection-mirror", CAT, "Small round inspection mirror on a telescoping rod with a handle",
      tags=["telescoping mirror", "mechanic mirror", "hidden areas", "engine bay", "check behind", "tool"])
def _(S):
    return [
        shell(circle(*rot([(12, 6)])[0], 4.5)),
        line(rseg(12, 10.5, 12, 14)),
        shell(poly(rot([(10, 14), (14, 14), (14, 21.5), (10, 21.5)]), closed=True, r=S.r * 0.6)),
        detail(rseg(10, 17, 14, 17)),
    ]


@icon("theodolite", CAT, "Surveying theodolite: a telescope between two supports on a tripod",
      tags=["surveying instrument", "total station", "land survey", "transit", "site measuring", "construction"])
def _(S):
    return [
        shell(rect(3, 4.5, 18, 5, rr(S, 2))),
        detail(seg(16.5, 4.5, 16.5, 9.5)),
        line(poly([(7, 9.5), (7, 13.5), (17, 13.5), (17, 9.5)], r=S.r)),
        line(seg(10, 13.5, 6.5, 22)),
        line(seg(14, 13.5, 17.5, 22)),
        line(seg(12, 13.5, 12, 22)),
    ]


@icon("surveyor-rod", CAT, "Tall striped surveyor rod with alternating marking blocks and a pointed foot",
      tags=["leveling staff", "level rod", "grade rod", "survey staff", "height measure", "construction"])
def _(S):
    return [
        shell(poly([(8, 2), (16, 2), (16, 18.5), (12, 22), (8, 18.5)], closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
        detail(seg(8, 6, 16, 6)),
        detail(seg(8, 10, 16, 10)),
        detail(seg(8, 14, 16, 14)),
        sq(9, 7, 6, 2),
        sq(9, 15, 6, 2),
    ]


@icon("survey-stake", CAT, "Wooden survey stake in the ground with a ribbon flag near the top",
      tags=["marker stake", "grade stake", "land surveying", "construction marker", "flagging tape", "layout"])
def _(S):
    return [
        shell(poly([(10, 2.5), (14, 2.5), (14, 16), (12, 21), (10, 16)], closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
        shell(poly([(14, 4.5), (21, 4.5), (18.5, 7.5), (21, 10.5), (14, 10.5)], closed=True, r=S.r * 0.5)),
        line(seg(3, 17, 7, 17)),
        line(seg(17, 17, 21, 17)),
    ]


@icon("lag-screw", CAT, "Lag screw with a hex head, a thick shank and coarse threads to a point",
      tags=["lag bolt", "coach screw", "heavy timber", "deck screw", "wood fastener", "hardware"])
def _(S):
    return [
        shell(rect(6.5, 2.5, 11, 4, rr(S, 1.5))),
        shell(poly([(9, 6.5), (15, 6.5), (15, 17), (12, 22), (9, 17)], closed=True, r=S.r * 0.5)),
        detail(seg(9, 10, 15, 11.5)),
        detail(seg(9, 14, 15, 15.5)),
    ]


@icon("machine-screw", CAT, "Machine screw with a round slotted head and a threaded shank",
      tags=["slotted screw", "fine thread", "small fastener", "electronics screw", "round head screw", "hardware"])
def _(S):
    return [
        shell("M6 8A6 6 0 0 1 18 8Z" if S.name == "line" else "M6 8A6 6 0 0 1 18 8Q18 9 17 9H7Q6 9 6 8Z"),
        detail(seg(12, 2, 12, 6)),
        shell(rect(9, 9, 6, 12.5, rr(S, 1))),
        detail(seg(9, 13, 15, 13)),
        detail(seg(9, 17, 15, 17)),
    ]


@icon("thumbscrew", CAT, "Thumbscrew with a wide flat grooved head and a threaded shank",
      tags=["hand screw", "knurled screw", "tool-free", "finger screw", "adjustment knob", "hardware"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 5, 2.5 if S.name == "rounded" else 0)),
        detail(seg(9, 2.5, 9, 7.5)),
        detail(seg(15, 2.5, 15, 7.5)),
        shell(rect(9, 7.5, 6, 14, rr(S, 1))),
        detail(seg(9, 12, 15, 12)),
        detail(seg(9, 16.5, 15, 16.5)),
    ]


@icon("set-screw", CAT, "Headless set screw: a short threaded cylinder with a hex socket in the top",
      tags=["grub screw", "headless screw", "shaft collar", "allen screw", "locking screw", "hardware"])
def _(S):
    return [
        shell(rect(7, 3.5, 10, 17, S.R)),
        detail(poly([(10.5, 3.5), (10.5, 8.5), (13.5, 8.5), (13.5, 3.5)], r=S.r * 0.5)),
        detail(seg(7, 13, 17, 13)),
        detail(seg(7, 17, 17, 17)),
    ]


@icon("eyebolt", CAT, "Eyebolt with a closed ring at the top and a threaded shank",
      tags=["eye bolt", "lifting eye", "rigging", "anchor point", "ring bolt", "hardware"])
def _(S):
    return [
        shell(circle(12, 6.5, 4.5)),
        shell(rect(9.5, 11, 5, 10.5, S.R * 0.5)),
        detail(seg(9.5, 15, 14.5, 15)),
        detail(seg(9.5, 19, 14.5, 19)),
    ]


@icon("u-bolt-clamp", CAT, "U-bolt clamp: a U-shaped rod through a flat plate held by two nuts",
      tags=["u bolt", "pipe clamp", "exhaust clamp", "mounting bracket", "saddle clamp", "hardware"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 4.5, 2.25 if S.name == "rounded" else 0)),
        line("M8 7V15.5a4 4 0 0 0 8 0V7"),
        solid(rect(5.5, 8.5, 5, 3, 0.5 if S.name == "rounded" else 0)),
        solid(rect(13.5, 8.5, 5, 3, 0.5 if S.name == "rounded" else 0)),
    ]


@icon("carriage-bolt-and-nut", CAT, "Carriage bolt with a domed head and square neck, fitted with a nut",
      tags=["coach bolt", "round head bolt", "timber bolt", "bolt and nut", "fence bolt", "hardware"])
def _(S):
    return [
        shell("M6 7.5A6 6 0 0 1 18 7.5Z" if S.name == "line" else "M6 7.5A6 6 0 0 1 18 7.5Q18 8.5 17 8.5H7Q6 8.5 6 7.5Z"),
        shell(rect(9, 8.5, 6, 2.5, 0)),
        line(seg(12, 11, 12, 13.5)),
        shell(rect(7.5, 13.5, 9, 4.5, rr(S, 1.5))),
        line(seg(12, 18, 12, 21.5)),
    ]


@icon("toggle-anchor", CAT, "Toggle bolt with its spring wings spread open under the bolt head",
      tags=["toggle bolt", "butterfly anchor", "hollow wall anchor", "drywall anchor", "spring toggle", "fastener"])
def _(S):
    return [
        shell(rect(7, 2.5, 10, 3.5, rr(S, 1.5))),
        line(seg(12, 6, 12, 10)),
        shell(poly([(2, 17), (12, 10), (22, 17), (22, 21), (12, 14), (2, 21)], closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
    ]


@icon("wall-anchor", CAT, "Ribbed plastic wall anchor with a top flange and barbs along its sides",
      tags=["plastic plug", "rawl plug", "wall plug", "expansion anchor", "drywall plug", "fastener"])
def _(S):
    pts = [(9, 5.5), (15, 5.5), (15, 8.5), (17.5, 11), (15, 11), (15, 14), (17.5, 16.5), (15, 16.5), (15, 21),
           (9, 21), (9, 16.5), (6.5, 16.5), (9, 14), (9, 11), (6.5, 11), (9, 8.5)]
    return [
        shell(rect(5, 2.5, 14, 3, rr(S, 1))),
        shell(poly(pts, closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        detail(seg(12, 9, 12, 21)),
    ]


@icon("threaded-rod", CAT, "Long threaded rod with thread lines along its length and a nut on it",
      tags=["all thread", "stud rod", "threaded bar", "hex nut", "fastener", "hardware"])
def _(S):
    k = S.R * 0.4
    return [
        shell(poly(rot([(9.5, 1.5), (14.5, 1.5), (14.5, 12), (9.5, 12)]), closed=True, r=S.r * 0.5)),
        detail(rseg(9.5, 5, 14.5, 5)),
        detail(rseg(9.5, 9, 14.5, 9)),
        shell(poly(rot([(7, 12), (17, 12), (17, 16.5), (7, 16.5)]), closed=True, r=S.r)),
        shell(poly(rot([(9.5, 16.5), (14.5, 16.5), (14.5, 22.5), (9.5, 22.5)]), closed=True, r=S.r * 0.5)),
        detail(rseg(9.5, 20, 14.5, 20)),
    ]


@icon("wing-nut", CAT, "Wing nut with two flat wings on opposite sides of the hub",
      tags=["butterfly nut", "thumb nut", "hand tighten", "fastener", "hex nut", "hardware"])
def _(S):
    return [
        shell(poly([(8, 21.5), (8, 14.5), (3, 11.5), (3.5, 4.5), (9, 9.5), (15, 9.5), (20.5, 4.5), (21, 11.5), (16, 14.5),
                    (16, 21.5)], closed=True, r=S.r * 0.7), stroke_miterlimit="2"),
        detail(seg(8, 17.5, 16, 17.5)),
    ]


@icon("cap-nut", CAT, "Cap nut: a hex nut capped with a smooth dome, side view",
      tags=["acorn nut", "dome nut", "blind nut", "decorative nut", "hex nut", "fastener"])
def _(S):
    rb = 0 if S.name == "line" else 2
    d = (f"M5 {21 - rb}V11A7 7 0 0 1 19 11V{21 - rb}" + (f"Q19 21 {19 - rb} 21H{5 + rb}Q5 21 5 {21 - rb}Z" if rb else "V21H5Z"))
    return [
        shell(d),
        detail(seg(5, 15.5, 19, 15.5)),
        detail(seg(9.5, 15.5, 9.5, 21)),
        detail(seg(14.5, 15.5, 14.5, 21)),
    ]


@icon("lock-nut", CAT, "Lock nut: a hex nut with a narrower nylon collar ring on top, side view",
      tags=["nyloc nut", "nylon insert nut", "locknut", "self locking", "hex nut", "fastener"])
def _(S):
    k = 2.5 if S.name == "rounded" else 0
    return [
        shell(rect(4.5, 12, 15, 9, k)),
        shell(rect(7.5, 4.5, 9, 7.5, k)),
        detail(seg(9.5, 12, 9.5, 21)),
        detail(seg(14.5, 12, 14.5, 21)),
        detail(seg(7.5, 8, 16.5, 8)),
    ]


@icon("t-nut", CAT, "T-nut: a round flange with a threaded barrel underneath and small prongs",
      tags=["tee nut", "furniture nut", "blind nut", "woodworking", "insert nut", "fastener"])
def _(S):
    return [
        shell(rect(3, 3, 18, 4, rr(S, 1.5))),
        shell(poly([(3.5, 7), (6, 7), (4.75, 12)], closed=True, r=0), stroke_miterlimit="2"),
        shell(poly([(18, 7), (20.5, 7), (19.25, 12)], closed=True, r=0), stroke_miterlimit="2"),
        shell(rect(9, 7, 6, 14, rr(S, 1.5))),
        detail(seg(9, 11.5, 15, 11.5)),
        detail(seg(9, 15.5, 15, 15.5)),
    ]


@icon("flange-nut", CAT, "Flange nut: a hex nut on a wide round washer flange, side view",
      tags=["serrated flange nut", "washer nut", "hex nut", "fastener", "automotive", "hardware"])
def _(S):
    return [
        shell(rect(6, 4, 12, 12, 2.5 if S.name == "rounded" else 0)),
        shell(rect(3, 16, 18, 4.5, 2.25 if S.name == "rounded" else 0)),
        detail(seg(9.5, 4, 9.5, 16)),
        detail(seg(14.5, 4, 14.5, 16)),
    ]


@icon("flat-washer", CAT, "Flat washer with a round hole, seen from above at a slight angle",
      tags=["plain washer", "spacer ring", "fastener", "bolt washer", "hardware", "ring"])
def _(S):
    t = 2.5 if S.name == "line" else 3.5
    return [
        shell(f"M2.5 10A9.5 6 0 0 1 21.5 10V{10 + t}A9.5 6 0 0 1 2.5 {10 + t}Z"),
        detail(ellipse(12, 10, 3.4, 2)),
        detail(f"M2.5 10A9.5 6 0 0 0 21.5 10"),
    ]


@icon("split-lock-washer", CAT, "Split lock washer: a thick ring with a slanted cut through one side",
      tags=["spring washer", "helical washer", "lock washer", "fastener", "bolt washer", "hardware"])
def _(S):
    from geometry import LINE, ROUNDED
    if S.name == "line":
        body = D(D(P(circle(12, 12, 9.5)), P(circle(12, 12, 4.5))), P(poly([(14, 10.5), (24, 7), (24, 12.5), (14, 16)], closed=True)))
        return [shell(path_to_d(body))]
    band = ST(arc(12, 12, 7, 38, 322), 5.0, ROUNDED.cap, ROUNDED.join, 4.0)
    return [shell(path_to_d(band))]


@icon("rivet", CAT, "Solid rivet with a rounded head and a straight shank",
      tags=["solid rivet", "domed head", "metal joining", "riveting", "fastener", "hardware"])
def _(S):
    if S.name == "line":
        d = "M4.5 9A7.5 7.5 0 0 1 19.5 9H14.5V21.5H9.5V9Z"
    else:
        d = "M4.5 9A7.5 7.5 0 0 1 19.5 9H14.5V20A1.5 1.5 0 0 1 13 21.5H11A1.5 1.5 0 0 1 9.5 20V9Z"
    return [shell(d)]


@icon("pop-rivet", CAT, "Blind pop rivet with a flange head and a long mandrel pin through the middle",
      tags=["blind rivet", "mandrel rivet", "rivet gun", "sheet metal", "fastener", "hardware"])
def _(S):
    return [
        line(seg(12, 2, 12, 7)),
        shell(rect(5, 7, 14, 3, rr(S, 1.5))),
        shell(rect(9, 10, 6, 10, rr(S, 1.5))),
        line(seg(12, 20, 12, 22)),
    ]


@icon("cotter-pin", CAT, "Cotter pin: a wire folded into a round eye with two parallel legs",
      tags=["split pin", "cotter key", "retaining pin", "castle nut", "axle pin", "fastener"])
def _(S):
    return [
        line("M10 10A4 4 0 1 1 14 10"),
        line(poly([(10, 10), (10, 17), (8, 21.5)], r=S.r * 0.5)),
        line(poly([(14, 10), (14, 17), (16, 21.5)], r=S.r * 0.5)),
    ]


@icon("hitch-pin-clip", CAT, "R-clip hitch pin: a straight leg with a wavy curved leg looping over it",
      tags=["r clip", "r-pin", "tractor pin", "spring clip", "retaining clip", "fastener"])
def _(S):
    cmds = [("M", (8, 21.5)), ("L", (8, 6)), ("C", (8, 2), (16, 2), (16, 7)), ("C", (16, 12), (10.5, 11), (10.5, 15)),
            ("C", (10.5, 18), (13.5, 19), (15, 21))]
    out = []
    for c in cmds:
        pts = rot(list(c[1:]), 30)
        out.append(c[0] + " ".join(f"{fmt(x)} {fmt(y)}" for x, y in pts))
    return [line("".join(out))]


@icon("clevis-pin", CAT, "Clevis pin: a short round pin with a flat head and a cross hole near the tip",
      tags=["pin with head", "headed pin", "hitch pin", "linkage pin", "cross hole", "fastener"])
def _(S):
    return [
        shell(poly(rot([(3, 6.5), (6.5, 6.5), (6.5, 17.5), (3, 17.5)], -45), closed=True, r=S.r)),
        shell(poly(rot([(6.5, 9), (20.5, 9), (20.5, 15), (6.5, 15)], -45), closed=True, r=S.r)),
        kdot(circle(*rot([(16.5, 12)], -45)[0], 1.3)),
    ]


@icon("wooden-dowel", CAT, "Round wooden dowel peg with a flute along it, turned at an angle",
      tags=["dowel pin", "wood peg", "fluted dowel", "joinery", "furniture assembly", "woodworking"])
def _(S):
    from geometry import rotation, transform_path
    body = transform_path(P("M8 6A4 1.7 0 0 1 16 6V18A4 1.7 0 0 1 8 18Z"), rotation(45))
    front = [(12 + 4 * math.cos(math.radians(t)), 6 + 1.7 * math.sin(math.radians(t))) for t in range(0, 181, 30)]
    return [
        shell(path_to_d(body)),
        detail(poly(rot(front), closed=False)),
        detail(rseg(12, 10, 12, 16)),
    ]


@icon("upholstery-tack", CAT, "Upholstery tack with a large domed head and a short sharp spike",
      tags=["furniture tack", "decorative nail", "pin", "sofa", "chair repair", "fastener"])
def _(S):
    if S.name == "line":
        d = "M4 9.5A8 8 0 0 1 20 9.5H13.5L12 21L10.5 9.5Z"
    else:
        d = "M4 9.5A8 8 0 0 1 20 9.5Q20 11 18.5 11H13.5L12.6 19.8Q12 21 11.4 19.8L10.5 11H5.5Q4 11 4 9.5Z"
    return [
        shell(d),
        kdot(circle(8.5, 6.5, 1.0)),
    ]


@icon("hose-clamp", CAT, "Round worm-drive hose clamp with a screw housing on one side",
      tags=["jubilee clip", "pipe clamp", "worm gear clamp", "tube clamp", "plumbing", "automotive"])
def _(S):
    from geometry import LINE, ROUNDED
    st = LINE if S.name == "line" else ROUNDED
    band = ST(arc(10.5, 12, 7, 38, 322), 4.0, st.cap, st.join, 4.0)
    housing = P(rect(14.5, 7.5, 7.5, 9, S.R * 0.75))
    return [
        shell(path_to_d(U(band, housing))),
        detail(seg(14.5, 12, 22, 12)),
    ]


@icon("snap-ring", CAT, "Open C-shaped snap ring with two small eyelet holes at its ends",
      tags=["circlip", "retaining ring", "e-clip", "seeger ring", "shaft ring", "fastener"])
def _(S):
    from geometry import LINE, ROUNDED
    st = LINE if S.name == "line" else ROUNDED
    band = ST(arc(12, 12, 7, 26, 334), 5.0, st.cap, st.join, 4.0)
    return [
        shell(path_to_d(band)),
        kdot(circle(*polar(12, 12, 7, 58), 0.9)),
        kdot(circle(*polar(12, 12, 7, -58), 0.9)),
    ]


@icon("o-ring", CAT, "Thick rubber O-ring with a shading mark on its curve",
      tags=["rubber seal", "sealing ring", "gasket ring", "hydraulic seal", "plumbing", "hardware"])
def _(S):
    hole = 4.4 if S.name == "rounded" else 3.8
    return [
        shell(circle(12, 12, 9.5)),
        detail(circle(12, 12, hole)),
        line(arc(12, 12, 6.9, 200, 255)),
    ]


@icon("gasket", CAT, "Flat gasket plate with a large central opening and bolt holes around the edge",
      tags=["seal plate", "head gasket", "flange gasket", "engine part", "plumbing seal", "hardware"])
def _(S):
    return [
        shell(poly([(2, 8), (5, 5), (19, 5), (22, 8), (22, 16), (19, 19), (5, 19), (2, 16)], closed=True, r=S.r * 3.5)),
        detail(circle(12, 12, 4.2)),
        kdot(circle(6, 9, 1.2)),
        kdot(circle(18, 9, 1.2)),
        kdot(circle(6, 15, 1.2)),
        kdot(circle(18, 15, 1.2)),
    ]


@icon("grommet", CAT, "Metal grommet eyelet with a rolled edge set in a piece of fabric",
      tags=["eyelet", "tarp hole", "banner ring", "curtain ring", "sewing hardware", "canvas"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, rr(S, 3))),
        detail(circle(12, 12, 5.8)),
        detail(circle(12, 12, 2.6)),
    ]


@icon("compression-spring", CAT, "Compression spring drawn as a zigzag of coils with straight ends",
      tags=["coil spring", "helical spring", "shock absorber", "bounce", "mechanical", "suspension"])
def _(S):
    return [
        line(poly([(12, 2), (12, 4), (18, 6.5), (6, 10), (18, 13.5), (6, 17), (12, 19.5), (12, 22)], r=S.r * 0.4)),
    ]


@icon("extension-spring", CAT, "Tight extension spring coil with a hook loop at each end",
      tags=["tension spring", "pull spring", "coil spring", "trampoline", "mechanical", "hooked spring"])
def _(S):
    return [
        line(circle(12, 4.2, 2.2)),
        line(poly([(12, 6.4), (17, 9), (7, 12), (17, 15), (12, 17.6)], r=S.r * 0.5)),
        line(circle(12, 19.8, 2.2)),
    ]


@icon("torsion-spring", CAT, "Torsion spring: a round coil with two straight legs leaving in opposite directions",
      tags=["twist spring", "clothespin spring", "mousetrap spring", "coil spring", "mechanical", "hinge spring"])
def _(S):
    return [
        shell(circle(11.5, 12.5, 6.5)),
        detail(circle(11.5, 12.5, 2.7 if S.name == "line" else 3.0)),
        line(seg(11.5, 6, 21.5, 6)),
        line(seg(11.5, 19, 2.5, 19)),
    ]


@icon("s-hook", CAT, "Metal S-hook with two open curls",
      tags=["hanging hook", "pot hook", "hanger hook", "meat hook", "chain hook", "hardware"])
def _(S):
    return [
        line("M15.9 9.2A4.5 4.5 0 1 0 12 11.5A4.5 4.5 0 1 1 8.1 18.8"),
    ]


@icon("screw-hook", CAT, "Screw hook: a J-shaped hook on a short pointed threaded shank",
      tags=["cup hook", "ceiling hook", "hanging hook", "plant hanger", "wood screw hook", "hardware"])
def _(S):
    return [
        shell(poly([(12, 1.5), (14.5, 4), (14.5, 10.5), (9.5, 10.5), (9.5, 4)], closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
        detail(seg(9.5, 6, 14.5, 7.5)),
        line("M12 10.5V16A4 4 0 0 0 20 16V14"),
    ]


@icon("picture-hanger", CAT, "Picture hanger plate with a hook and a slim nail driven through it",
      tags=["picture hook", "frame hook", "wall hook", "hanging art", "nail hanger", "decor"])
def _(S):
    return [
        shell(rect(9, 3, 10, 10, rr(S, 2))),
        line("M14 13V18A3.5 3.5 0 0 0 21 18V16"),
        line(seg(3, 4, 13, 9.5)),
        dot(3.5, 4.3, 1.4),
    ]


@icon("magnetic-hook", CAT, "Magnet disc on a wall with a hook reaching out from its centre",
      tags=["magnet hook", "fridge hook", "strong magnet", "steel surface", "hanging", "hardware"])
def _(S):
    return [
        shell(rect(2, 4.5, 4, 15, rr(S, 2))),
        line("M6 12H14A4 4 0 0 0 18 8V5.5"),
    ]


# ============================================================================ hinges, latches and door hardware

@icon("butt-hinge", CAT, "Butt hinge with two flat leaves joined by a knuckle pin and screw holes",
      tags=["door hinge", "cabinet hinge", "leaf hinge", "pivot", "carpentry", "door hardware"])
def _(S):
    k = 1.5 if S.name == "rounded" else 0
    return [
        shell(rect(2, 3, 8, 18, k)),
        shell(rect(14, 3, 8, 18, k)),
        shell(rect(10, 3, 4, 18, 0)),
        detail(seg(10, 9, 14, 9)),
        detail(seg(10, 15, 14, 15)),
        dot(6, 7.5, 1.2),
        dot(6, 16.5, 1.2),
        dot(18, 7.5, 1.2),
        dot(18, 16.5, 1.2),
    ]


@icon("strap-hinge", CAT, "Strap hinge with a long tapered strap leaf, a knuckle and a short leaf",
      tags=["gate hinge", "barn door hinge", "shed hinge", "tee hinge", "pivot", "door hardware"])
def _(S):
    return [
        shell(poly([(14, 6.5), (3, 10), (3, 14), (14, 17.5)], closed=True, r=S.r * 0.8)),
        shell(rect(14, 4, 4, 16, 0)),
        shell(rect(18, 5, 4, 14, 1.5 if S.name == "rounded" else 0)),
        dot(8, 12, 1.1),
        dot(20, 8.5, 1.0),
        dot(20, 15.5, 1.0),
    ]


@icon("piano-hinge", CAT, "Long piano hinge with a continuous knuckle tube and a row of screw holes",
      tags=["continuous hinge", "lid hinge", "long hinge", "cabinet hardware", "piano lid", "door hardware"])
def _(S):
    k = 1.5 if S.name == "rounded" else 0
    return [
        shell(rect(2, 3.5, 20, 6, k)),
        shell(rect(2, 9.5, 20, 5, 0)),
        shell(rect(2, 14.5, 20, 6, k)),
        dot(6, 6.5, 1.0),
        dot(10, 6.5, 1.0),
        dot(14, 6.5, 1.0),
        dot(18, 6.5, 1.0),
        dot(6, 17.5, 1.0),
        dot(10, 17.5, 1.0),
        dot(14, 17.5, 1.0),
        dot(18, 17.5, 1.0),
    ]


@icon("barrel-bolt-latch", CAT, "Barrel bolt: a round rod sliding in a housing with a knob and a keeper",
      tags=["door bolt", "slide bolt", "gate bolt", "sliding latch", "lock", "door hardware"])
def _(S):
    return [
        shell(rect(2, 10, 12, 6, rr(S, 2.5))),
        line(seg(6, 13, 20, 13)),
        line(seg(8.5, 10, 8.5, 6)),
        dot(8.5, 4.5, 1.6),
        shell(rect(18.5, 8, 3.5, 10, rr(S, 1.5))),
    ]


@icon("gate-latch", CAT, "Thumb latch: a pivoting lever bar dropping into a hooked catch",
      tags=["thumb latch", "gate catch", "lever latch", "fence gate", "garden gate", "door hardware"])
def _(S):
    return [
        shell(rect(2, 8, 5, 8, rr(S, 2))),
        shell(rect(7, 10, 12, 4, rr(S, 1.5))),
        dot(4.5, 12, 1.1),
        line(poly([(16, 7), (21, 7), (21, 17), (16, 17)], r=S.r)),
    ]


@icon("door-chain", CAT, "Door chain with a track plate, a slide knob and hanging links",
      tags=["security chain", "door guard", "safety chain", "privacy lock", "front door", "door hardware"])
def _(S):
    return [
        shell(rect(2, 7, 6, 10, 2.5 if S.name == "rounded" else 0)),
        dot(5, 12, 1.2),
        shell(ellipse(11.5, 12, 3.2, 2.2)),
        shell(ellipse(15.5, 12, 2.2, 3.2)),
        shell(ellipse(19.2, 12, 2.8, 2.0)),
    ]


@icon("door-stopper", CAT, "Rubber wedge door stopper jammed under the bottom edge of a door",
      tags=["door wedge", "door stop", "doorstop", "prop open", "holding door", "door hardware"])
def _(S):
    return [
        shell(rect(10, 2, 12, 8, rr(S, 1.5))),
        shell(poly([(2, 20), (22, 20), (22, 13), (20.5, 13)], closed=True, r=S.r * 0.8), stroke_miterlimit="2"),
        detail(seg(12, 20, 12, 18)),
        detail(seg(16, 20, 16, 16)),
    ]


@icon("door-closer", CAT, "Door closer: a hydraulic cylinder on the door top with a jointed arm",
      tags=["hydraulic closer", "automatic door", "door arm", "overhead closer", "fire door", "door hardware"])
def _(S):
    return [
        shell(rect(2, 4, 11, 6, rr(S, 2))),
        line(seg(2, 12.5, 14, 12.5)),
        line(poly([(13, 7), (17, 7), (20, 14)], r=S.r)),
        dot(20, 15.5, 1.5),
    ]


@icon("peephole", CAT, "Door with a small round viewer lens set into its centre",
      tags=["door viewer", "spy hole", "door eye", "security", "front door", "door hardware"])
def _(S):
    return [
        shell(rect(4, 2, 16, 20, 4 if S.name == "rounded" else 0)),
        detail(circle(12, 9, 4.2)),
        dot(12, 9, 1.3),
        dot(16.5, 16, 1.2),
    ]


@icon("mail-slot", CAT, "Letterbox plate with a horizontal hinged flap slot",
      tags=["letterbox", "letter plate", "letter flap", "post slot", "mailbox door", "door hardware"])
def _(S):
    return [
        shell(rect(2, 5, 20, 14, rr(S, 3))),
        detail(rect(6.5, 9.5, 11, 5, 0)),
    ]


@icon("combination-padlock", CAT, "Padlock with a round numbered dial on its front and a shackle on top",
      tags=["dial lock", "number lock", "locker lock", "code lock", "security", "lock"])
def _(S):
    return [
        line("M8 10.5V7A4 4 0 0 1 16 7V10.5"),
        shell(rect(4, 10.5, 16, 11, rr(S, 3))),
        detail(circle(12, 16, 3.3)),
        dot(12, 12.6, 0.0 + 0.001) if False else dot(12, 16, 1.0),
    ]


@icon("shackle-hardware", CAT, "U-shaped metal shackle with a headed screw pin across the open end",
      tags=["bow shackle", "d shackle", "rigging shackle", "lifting shackle", "clevis", "chain hardware"])
def _(S):
    return [
        shell(rect(2, 2.5, 3.5, 5, rr(S, 1.5))),
        line(seg(5.5, 5, 21, 5)),
        line("M7.5 5V14A4.5 4.5 0 0 0 16.5 14V5"),
    ]


@icon("turnbuckle", CAT, "Turnbuckle: an open frame with a threaded eye screwed into each end",
      tags=["rigging screw", "tensioner", "wire tensioner", "eye and eye", "cable tightener", "rigging hardware"])
def _(S):
    return [
        shell(circle(3.8, 12, 2.3)),
        line(seg(6.1, 12, 7.5, 12)),
        shell(rect(7.5, 8, 9, 8, rr(S, 2.5))),
        detail(seg(10.5, 12, 13.5, 12)),
        line(seg(16.5, 12, 17.9, 12)),
        shell(circle(20.2, 12, 2.3)),
    ]


@icon("carabiner", CAT, "D-shaped carabiner clip tilted to one side with a straight spring gate that stops short of the nose",
      tags=["climbing clip", "snap hook", "spring clip", "keychain clip", "belay", "rigging hardware"])
def _(S):
    def pt(p, deg=24):
        x, y = rot([p], deg)[0]
        return f"{fmt(x)} {fmt(y)}"
    frame = (f"M{pt((16, 5))}L{pt((11, 5))}A6.5 6.5 0 0 0 {pt((11, 18))}L{pt((17, 18))}")
    gate = f"M{pt((17, 18))}L{pt((17, 8.5))}"
    return [line(frame), line(gate)]


@icon("d-ring", CAT, "Metal D-ring with a flat straight side and a rounded back, hanging at a tilt",
      tags=["d shaped ring", "strap ring", "harness ring", "belt ring", "rigging ring", "hardware"])
def _(S):
    from geometry import LINE, ROUNDED, rotation, transform_path
    st = LINE if S.name == "line" else ROUNDED
    band = ST("M6.5 6H11A6 6 0 0 1 17 12A6 6 0 0 1 11 18H6.5Z", 4.0, st.cap, st.join, 4.0)
    band = transform_path(band, rotation(-30))
    return [shell(path_to_d(band))]


def _stadium(cx, cy, length, width, deg):
    from geometry import rotation, transform_path
    body = P(rect(cx - width / 2, cy - length / 2, width, length, width / 2))
    return path_to_d(transform_path(body, rotation(deg, cx, cy)))


@icon("chain-links", CAT, "Three interlocking chain links running along a diagonal",
      tags=["chain", "link chain", "metal chain", "anchor chain", "hardware store", "rigging hardware"])
def _(S):
    return [
        shell(_stadium(7.5, 7.5, 9.5, 5.5, -45)),
        shell(_stadium(16.5, 16.5, 9.5, 5.5, -45)),
        line(seg(10, 10, 14, 14)),
    ]


@icon("wire-rope", CAT, "Twisted wire rope with slanted strands ending in a looped thimble",
      tags=["steel cable", "cable rope", "rigging wire", "winch cable", "strand", "rigging hardware"])
def _(S):
    return [
        shell(rect(9, 2, 6, 11, 2.5 if S.name == "rounded" else 0)),
        detail(seg(9, 5, 15, 8)),
        detail(seg(9, 9, 15, 12)),
        shell(circle(12, 17.5, 3.6)),
    ]


@icon("pulley", CAT, "Pulley block: a wheel with a hook on top and a rope hanging from both sides",
      tags=["block and tackle", "sheave", "lifting", "hoist", "rope wheel", "rigging hardware"])
def _(S):
    return [
        line("M12 7.5V4.5A2.5 2.5 0 0 1 17 4.5V6.5"),
        shell(circle(12, 13.5, 6)),
        dot(12, 13.5, 1.4),
        line(seg(6, 13.5, 6, 22)),
        line(seg(18, 13.5, 18, 22)),
    ]
