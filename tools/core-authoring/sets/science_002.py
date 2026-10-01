"""TypeIcon Core: science (batch science_002).

Chemistry reactions and hazard diamonds, particles and nuclear physics, mechanics, heat, optics, waves,
magnetism and electricity. Drawn from the objects and textbook diagrams themselves.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar  # noqa: F401

CAT = "science"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def stroke_d(d, w=1.5, cap="round", join="round"):
    return path_to_d(ST(d, w, cap, join, 4.0))


def sdot(d):
    """Solid glyph: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def pts_d(pts, closed=False):
    d = "".join(("M" if i == 0 else "L") + f"{fmt(x)} {fmt(y)}" for i, (x, y) in enumerate(pts))
    return d + ("Z" if closed else "")


def arrow_head(tip, deg, size=2.0):
    """Open arrowhead at `tip` pointing along `deg` (0 = right, 90 = down)."""
    a = polar(tip[0], tip[1], size * 1.414, deg + 135)
    b = polar(tip[0], tip[1], size * 1.414, deg - 135)
    return poly([a, tip, b])


def arrow(x1, y1, x2, y2, size=2.0):
    """Line with an open arrowhead at (x2, y2)."""
    deg = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return seg(x1, y1, x2, y2) + arrow_head((x2, y2), deg, size)


def wavy(x, y0, y1, amp=1.2, n=2):
    """Vertical wavy line from y0 to y1 with n half waves."""
    h = (y1 - y0) / n
    d = f"M{fmt(x)} {fmt(y0)}"
    for i in range(n):
        s = amp if i % 2 == 0 else -amp
        d += f"C{fmt(x + s)} {fmt(y0 + h * (i + 0.25))} {fmt(x + s)} {fmt(y0 + h * (i + 0.75))} {fmt(x)} {fmt(y0 + h * (i + 1))}"
    return d


def sine(x0, x1, y, amp, cycles, steps=10, phase=0.0):
    """Polyline sine wave (explicit points, kept short)."""
    n = int(cycles * steps)
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append((x0 + (x1 - x0) * t, y - amp * math.sin(2 * math.pi * cycles * t + phase)))
    return pts


def wave_line(x0, x1, y, amp=1.0, n=4):
    """Smooth horizontal wave from x0 to x1 with n half waves."""
    h = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        s = -amp if i % 2 == 0 else amp
        d += f"Q{fmt(x0 + h * (i + 0.5))} {fmt(y + 2 * s)} {fmt(x0 + h * (i + 1))} {fmt(y)}"
    return d


def smooth(pts):
    """Open Catmull-Rom style path through points."""
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    n = len(pts)
    for i in range(n - 1):
        p0 = pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d


def drop_d(cx, top, w, h):
    """Solid teardrop: tip at the top, round bottom."""
    r = w / 2
    cy = top + h - r
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + r * 0.3)} {fmt(top + h * 0.3)} {fmt(cx + r)} {fmt(cy - r * 0.9)} {fmt(cx + r)} {fmt(cy)}"
            f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx - r)} {fmt(cy)}"
            f"C{fmt(cx - r)} {fmt(cy - r * 0.9)} {fmt(cx - r * 0.3)} {fmt(top + h * 0.3)} {fmt(cx)} {fmt(top)}Z")


def flame_d(cx, top, w, h):
    """Solid flame: pointed top with a lean, round bottom."""
    r = w / 2
    cy = top + h - r
    return (f"M{fmt(cx + w * 0.1)} {fmt(top)}C{fmt(cx + w * 0.15)} {fmt(top + h * 0.25)} {fmt(cx + r)} {fmt(cy - r * 1.2)} {fmt(cx + r)} {fmt(cy)}"
            f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx - r)} {fmt(cy)}"
            f"C{fmt(cx - r)} {fmt(cy - r * 0.9)} {fmt(cx - r * 0.6)} {fmt(cy - r * 1.4)} {fmt(cx - r * 0.2)} {fmt(cy - r * 1.7)}"
            f"C{fmt(cx - r * 0.1)} {fmt(cy - r * 1.4)} {fmt(cx)} {fmt(cy - r * 1.4)} {fmt(cx + r * 0.15)} {fmt(cy - r * 1.9)}"
            f"C{fmt(cx + w * 0.05)} {fmt(top + h * 0.15)} {fmt(cx + w * 0.08)} {fmt(top + h * 0.05)} {fmt(cx + w * 0.1)} {fmt(top)}Z")


def flask_pts(cx, top, bot, neck, base):
    """Conical (Erlenmeyer) flask outline points."""
    ny = top + (bot - top) * 0.34
    return [(cx - neck / 2, top), (cx + neck / 2, top), (cx + neck / 2, ny), (cx + base / 2, bot),
            (cx - base / 2, bot), (cx - neck / 2, ny)]


def star_pts(cx, cy, ro, ri, n, start=-90.0):
    return [polar(cx, cy, ro if i % 2 == 0 else ri, start + i * 180 / n) for i in range(2 * n)]


def diamond(S):
    """Hazard diamond frame, standing on its point."""
    return shell(poly([(12, 2), (22, 12), (12, 22), (2, 12)], closed=True, r=L(S, 0, 2.2)), stroke_miterlimit="3")


def warn_tri(S):
    return shell(poly([(12, 3), (22, 20.5), (2, 20.5)], closed=True, r=L(S, 0, 2)), stroke_miterlimit="3")


# ============================================================================ chemistry

def rot_about(cx, cy, deg):
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return lambda x, y: (cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c)


@icon("exothermic-reaction", CAT, "Flask with rising heat waves and arrows pointing out: a reaction that gives off heat",
      tags=["heat release", "chemistry", "reaction", "energy out", "hot flask", "lab"])
def _(S):
    f = poly(flask_pts(12, 11, 21, 5, 11), closed=True, r=S.r * 0.6)
    return [shell(f), detail(seg(9, 17, 15, 17)),
            line(wavy(12, 2, 8, 1.3)),
            line(arrow(6.5, 10, 2.5, 6, 2.2)), line(arrow(17.5, 10, 21.5, 6, 2.2))]


@icon("endothermic-reaction", CAT, "Flask with a snowflake above and arrows pointing in: a reaction that takes in heat",
      tags=["heat absorption", "chemistry", "reaction", "cold flask", "energy in", "lab"])
def _(S):
    f = poly(flask_pts(12, 11, 21, 5, 11), closed=True, r=S.r * 0.6)
    sn = []
    for a in (0, 60, 120):
        p, q = polar(12, 5.2, 3.2, a), polar(12, 5.2, 3.2, a + 180)
        sn.append(seg(p[0], p[1], q[0], q[1]))
    return [shell(f), detail(seg(9, 17, 15, 17)), line("".join(sn)),
            line(arrow(2.5, 6, 6.5, 10, 2.2)), line(arrow(21.5, 6, 17.5, 10, 2.2))]


@icon("chemical-spill", CAT, "Tipped-over beaker with liquid running out into a puddle",
      tags=["spill", "leak", "lab accident", "chemical", "liquid", "hazard", "cleanup"])
def _(S):
    t = rot_about(8, 8, 125)
    beaker = poly([t(4.5, 2.5), t(4.5, 12.5), t(11.5, 12.5), t(11.5, 2.5)], closed=False, r=S.r * 0.6)
    return [shell(beaker), detail(seg(*t(4.5, 8), *t(11.5, 8))),
            sdot(drop_d(15.5, 10.5, 3.2, 4.2)),
            sdot(ellipse(13, 19.5, 8, 2.2))]


@icon("baking-soda-volcano", CAT, "Model volcano cone with foam bubbling over the crater",
      tags=["science fair", "volcano experiment", "baking soda", "vinegar", "eruption", "school project", "foam"])
def _(S):
    cone = poly([(3, 21), (8.5, 12), (15.5, 12), (21, 21)], closed=True, r=S.r * 0.7)
    foam = "M7.5 12a2.6 2.6 0 0 1 1.5-4.4 3 3 0 0 1 6 0 2.6 2.6 0 0 1 1.5 4.4"
    return [shell(cone), line(foam), sdot(circle(19.5, 8.5, 1.3)), sdot(circle(4.5, 8, 1.3)), sdot(circle(12, 3.6, 1.1))]


@icon("crystal-growing-jar", CAT, "Jar with a pencil across the rim and a string hanging into it, covered in crystals",
      tags=["grow crystals", "salt crystals", "sugar crystals", "science experiment", "string", "pencil", "jar"])
def _(S):
    jar = poly([(5.5, 8), (18.5, 8), (18.5, 21), (5.5, 21)], closed=True, r=S.r * 0.8)
    lump = poly([(8.5, 18.5), (8.5, 15.5), (10.2, 16.7), (12, 13), (13.8, 16.7), (15.5, 15.5), (15.5, 18.5)], closed=True)
    return [shell(jar), line(seg(2.5, 4.5, 21.5, 4.5)), line(seg(12, 4.5, 12, 8)), detail(seg(12, 8, 12, 13)),
            detail(lump)]


@icon("titration", CAT, "Burette dripping a drop into a conical flask",
      tags=["burette", "chemistry", "analysis", "lab", "drop", "flask", "endpoint", "acid base"])
def _(S):
    bur = rect(10.5, 2, 3, 6, min(S.R, 1))
    return [shell(bur), line(seg(13.5, 5, 16.5, 5)), sdot(drop_d(12, 9.2, 2.2, 2.8)),
            shell(poly(flask_pts(12, 13, 21.5, 4.5, 13), closed=True, r=S.r * 0.5)),
            detail(seg(8.5, 18, 15.5, 18))]


# ============================================================================ hazard diamonds

@icon("flammable-hazard", CAT, "Hazard diamond with a flame over a bar: flammable material",
      tags=["flammable", "fire hazard", "ghs", "nfpa", "warning", "label", "safety", "combustible"])
def _(S):
    return [diamond(S), sdot(flame_d(12, 7, 4.6, 7.2)), sdot(rect(8.7, 15.5, 6.6, 1.6))]


@icon("corrosive-hazard", CAT, "Hazard diamond with two drops falling on a bar that is being eaten away",
      tags=["corrosive", "acid", "ghs", "warning", "label", "safety", "chemical burn", "caustic"])
def _(S):
    bar = minus(rect(8, 13.5, 8, 2.5), circle(10.2, 13.5, 1.1))
    return [diamond(S), sdot(drop_d(10, 7.5, 2.6, 3.4)), sdot(drop_d(14.2, 8.8, 2.4, 3.2)), sdot(bar)]


@icon("toxic-hazard", CAT, "Hazard diamond with a skull and crossbones: toxic material",
      tags=["toxic", "poison", "skull", "ghs", "warning", "label", "safety", "deadly"])
def _(S):
    skull = union(circle(12, 10.2, 2.6), rect(10.6, 11.5, 2.8, 2.4))
    skull = minus(skull, circle(10.9, 10.3, 0.8), circle(13.1, 10.3, 0.8))
    bones = union(stroke_d(seg(8.8, 14.2, 15.2, 17.2), 1.3), stroke_d(seg(15.2, 14.2, 8.8, 17.2), 1.3))
    return [diamond(S), sdot(union(skull, bones))]


@icon("oxidizer-hazard", CAT, "Hazard diamond with a flame over a circle: oxidizing material",
      tags=["oxidizer", "oxidising", "ghs", "warning", "label", "safety", "flame over circle"])
def _(S):
    ring = minus(circle(12, 14.6, 2.7), circle(12, 14.6, 1.3))
    return [diamond(S), sdot(flame_d(12, 6.2, 4, 6)), sdot(ring)]


@icon("explosive-hazard", CAT, "Hazard diamond with a bursting ball and flying fragments: explosive material",
      tags=["explosive", "blast", "bomb", "ghs", "warning", "label", "safety", "detonation"])
def _(S):
    burst = poly(star_pts(12, 12.5, 5, 2.4, 8), closed=True)
    return [diamond(S), sdot(burst)]


@icon("compressed-gas-hazard", CAT, "Hazard diamond with a gas cylinder lying on its side: gas under pressure",
      tags=["compressed gas", "gas cylinder", "pressure", "ghs", "warning", "label", "safety", "tank"])
def _(S):
    body = union(rect(6.8, 10.6, 8.2, 4.4, 2.1), rect(14.6, 11.7, 2.8, 2.2, 0.4))
    body = minus(body, rect(12.6, 10, 0.9, 6))
    return [diamond(S), sdot(body)]


@icon("health-hazard", CAT, "Hazard diamond with a person's upper body and a star burst on the chest: health hazard",
      tags=["health hazard", "carcinogen", "ghs", "warning", "label", "safety", "body", "long term harm"])
def _(S):
    torso = union(circle(12, 8.2, 1.7), "M7.8 17A4.2 4.2 0 0 1 12 11.5 4.2 4.2 0 0 1 16.2 17Z")
    torso = minus(torso, poly(star_pts(12, 14.2, 1.5, 0.6, 4), closed=True))
    return [diamond(S), sdot(torso)]


@icon("environmental-hazard", CAT, "Hazard diamond with a bare tree and a dead fish: harmful to the environment",
      tags=["environmental hazard", "ecotoxic", "pollution", "ghs", "warning", "label", "dead fish", "tree"])
def _(S):
    tree = union(stroke_d(seg(9.2, 17, 9.2, 8.8), 1.3), stroke_d(seg(9.2, 13.2, 7.6, 11), 1.1), stroke_d(seg(9.2, 12, 11, 9.8), 1.1))
    fish = minus(union(ellipse(14.4, 15.2, 2.3, 1.3), "M16.4 15.2L18 13.9V16.5Z"), circle(13.4, 15, 0.45))
    return [diamond(S), sdot(union(tree, fish))]


@icon("irritant-hazard", CAT, "Hazard diamond with a bold exclamation mark: irritant or harmful material",
      tags=["irritant", "harmful", "exclamation", "ghs", "warning", "label", "safety", "attention"])
def _(S):
    bar = poly([(10.7, 7.2), (13.3, 7.2), (12.7, 13.8), (11.3, 13.8)], closed=True)
    return [diamond(S), sdot(bar), sdot(circle(12, 16.2, 1.2))]


@icon("laser-hazard", CAT, "Warning triangle with a starburst and a single ray: laser radiation",
      tags=["laser", "laser radiation", "warning", "beam", "safety sign", "optical hazard", "class 3", "class 4"])
def _(S):
    burst = poly(star_pts(9.5, 14.4, 3.2, 1.4, 6, start=-90), closed=True)
    ray = stroke_d(seg(12, 14.4, 17.5, 14.4), 1.5, cap="butt")
    return [warn_tri(S), sdot(union(burst, ray))]


# ============================================================================ particles and nuclear physics

def plus_d(cx, cy, h=2.2, t=1.4):
    return union(rect(cx - h, cy - t / 2, 2 * h, t), rect(cx - t / 2, cy - h, t, 2 * h))


def minus_d(cx, cy, h=2.2, t=1.4):
    return rect(cx - h, cy - t / 2, 2 * h, t)


def zero_d(cx, cy, rx=1.9, ry=3.0, t=1.3):
    return minus(ellipse(cx, cy, rx, ry), ellipse(cx, cy, rx - t, ry - t))


@icon("atomic-nucleus", CAT, "Tight cluster of four particles, two marked with plus signs and two plain",
      tags=["nucleus", "protons", "neutrons", "nucleon", "atom core", "physics", "chemistry"])
def _(S):
    return [shell(circle(12, 6.2, 3.4)), sdot(plus_d(12, 6.2, 1.6, 1.1)),
            shell(circle(12, 17.8, 3.4)), sdot(plus_d(12, 17.8, 1.6, 1.1)),
            shell(circle(6.2, 12, 3.4)), shell(circle(17.8, 12, 3.4))] + ([] if S.name == "line" else [sdot(circle(6.2, 12, 0.9)), sdot(circle(17.8, 12, 0.9))])


@icon("electron", CAT, "Small ball marked with a minus sign trailing a curved orbit line",
      tags=["negative charge", "particle", "orbit", "subatomic", "physics", "lepton", "atom"])
def _(S):
    return [shell(circle(15.5, 8.5, 5.5)), sdot(minus_d(15.5, 8.5, 2.3, 1.4)),
            line("M3 20.5C3 14 6.5 10.5 9 9.5")]


@icon("proton", CAT, "Ball marked with a plus sign and a small shine",
      tags=["positive charge", "particle", "nucleon", "subatomic", "physics", "hydrogen nucleus", "atom"])
def _(S):
    return [shell(circle(12, 12, 9)), sdot(plus_d(12.8, 12.8, 3, 1.5)), line(arc(12, 12, 5.4, 195, 255))]


@icon("neutron", CAT, "Ball marked with a zero: a neutral particle",
      tags=["neutral particle", "no charge", "nucleon", "subatomic", "physics", "atom", "zero"])
def _(S):
    return [shell(circle(12, 12, 9)), sdot(zero_d(12, 12, 2.1, 3.4, 1.4))] + ([] if S.name == "line" else [line(arc(12, 12, 6, 195, 250))])


@icon("photon", CAT, "Wavy light squiggle ending in an arrowhead with a small spark at the tip",
      tags=["light particle", "quantum", "light", "wave", "energy", "electromagnetic", "radiation"])
def _(S):
    w = smooth(sine(2.5, 12.5, 14, 3, 2, steps=6))
    return [line(w + "L21.5 14"), line(arrow_head((21.5, 14), 0, 2.6)),
            sdot(poly(star_pts(18, 5.5, 3, 1, 4), closed=True))]


@icon("quarks", CAT, "Circle holding three small dots joined by lines",
      tags=["quark", "hadron", "particle physics", "subatomic", "proton", "neutron", "strong force"])
def _(S):
    a, b, c = (12, 6.8), (7.4, 15), (16.6, 15)
    tri = poly([a, b, c], closed=True) if S.name == "line" else (
        f"M{a[0]} {a[1]}Q12 12.6 {c[0]} {c[1]}Q12 15.8 {b[0]} {b[1]}Q12 12.6 {a[0]} {a[1]}Z")
    return [shell(circle(12, 12, 9.5)), detail(tri),
            sdot(circle(*a, 2.2)), sdot(circle(*b, 2.2)), sdot(circle(*c, 2.2))]


@icon("nuclear-fission", CAT, "Small particle striking a nucleus that splits into two with three particles flying off",
      tags=["fission", "split atom", "chain reaction", "nuclear power", "uranium", "physics", "neutron"])
def _(S):
    return [sdot(circle(3.5, 12, 1.6)), line(seg(6, 12, 7.5, 12)),
            shell(circle(12.5, 6.3, 3.5)), shell(circle(12.5, 17.7, 3.5)),
            sdot(circle(20.5, 11, 1.4)), sdot(circle(20.5, 3.5, 1.4)), sdot(circle(20.5, 20.5, 1.4))]


@icon("nuclear-fusion", CAT, "Two small nuclei moving together and merging into a bright burst",
      tags=["fusion", "hydrogen", "star energy", "tokamak", "nuclear power", "physics", "merge", "sun"])
def _(S):
    return [shell(circle(4, 12, 2.4)), shell(circle(20, 12, 2.4)),
            sdot(poly(star_pts(12, 12, 6.3, 3, 8), closed=True)),
            line(arrow(7.5, 12, 8.3, 12, 1.4)), line(arrow(16.5, 12, 15.7, 12, 1.4))]


def ring_arc_dashes(cx, cy, r, a0, a1, on, off):
    """Dash arcs (degrees) between a0 and a1 clockwise."""
    out, a = [], a0
    while a + on <= a1 + 1e-6:
        out.append(arc(cx, cy, r, a, a + on))
        a += on + off
    return out


def tick(x, y, dx=0.35, dy=0.0):
    return seg(x - dx, y - dy, x + dx, y + dy)


@icon("half-life", CAT, "Decay curve on axes falling by half at each step, with dotted guide lines",
      tags=["radioactive decay", "decay curve", "isotope", "exponential decay", "nuclear", "physics", "chemistry", "graph"])
def _(S):
    pts = [(6 + t, 18.5 - 13 * 2 ** (-t / 5)) for t in (0, 2.5, 5, 10, 15)]
    return [line(poly([(3.5, 2.5), (3.5, 21.5), (21.5, 21.5)], r=S.r * 0.4)),
            line(smooth(pts)),
            line(seg(6.2, 12, 7.8, 12)),
            line(seg(11, 14.8, 11, 16.4))]


@icon("particle-accelerator", CAT, "Large ring with a small ball racing around it and a dotted trail behind",
      tags=["collider", "synchrotron", "cern", "hadron", "ring", "physics", "particle physics", "beam"])
def _(S):
    ball = polar(12, 12, 8.5, -40)
    return [line(arc(12, 12, 8.5, -20, 215)), line("".join(ring_arc_dashes(12, 12, 8.5, 229, 292, 7, 21))),
            sdot(circle(ball[0], ball[1], 2.6))]


@icon("particle-collision", CAT, "Burst of straight and curved tracks spreading from one central point",
      tags=["collision", "detector", "bubble chamber", "particle tracks", "physics", "collider", "event", "decay"])
def _(S):
    ang = (-75, -10, 120, 195)
    straight = [seg(*polar(12, 12, 4, a), *polar(12, 12, 10, a)) for a in ang]
    curve = "M14.6 14.6Q19 14.5 20 19.5"
    return [dot(12, 12, 1.5), line("".join(straight)), line(curve)]


@icon("quantum-entanglement", CAT, "Two particles with opposite spin arrows linked by a wavy line",
      tags=["entangled", "quantum", "spin", "particles", "physics", "connected", "spooky action"])
def _(S):
    return [sdot(circle(4.8, 16, 2.6)), sdot(circle(19.2, 16, 2.6)),
            line(smooth(sine(9.6, 14.4, 16, 1.7, 1, steps=8))),
            line(arrow(4.8, 11, 4.8, 3.5, 2.2)), line(arrow(19.2, 3.5, 19.2, 11, 2.2))]


@icon("gravitational-wave", CAT, "Two small masses circling each other inside rings of spreading ripples",
      tags=["ligo", "spacetime", "ripples", "black holes merging", "binary", "physics", "astronomy", "einstein"])
def _(S):
    return [sdot(circle(10.2, 10.6, 1.6)), sdot(circle(13.8, 13.4, 1.6)),
            line(arc(12, 12, 6, 160, 200) + arc(12, 12, 6, -20, 20)),
            line(arc(12, 12, 9.5, 135, 225) + arc(12, 12, 9.5, -45, 45))]


@icon("cathode-ray-tube", CAT, "Glass tube with a narrow neck and wide end, a beam crossing to a glowing spot",
      tags=["crt", "electron beam", "vacuum tube", "old tv", "physics", "oscilloscope", "display", "monitor"])
def _(S):
    tube = "M2.5 9.5H8.5L18.5 4.5Q21.5 12 18.5 19.5L8.5 14.5H2.5Z"
    return [shell(tube, stroke_miterlimit="3"), detail(seg(5, 12, 13, 12)), sdot(circle(16.8, 12, 1.4))]


@icon("brownian-motion", CAT, "One highlighted particle with a jagged zigzag path among scattered smaller dots",
      tags=["random motion", "particles", "diffusion", "molecules", "physics", "chemistry", "random walk", "pollen"])
def _(S):
    path = poly([(3.5, 17.5), (7.5, 11), (10.5, 15.5), (14, 8.5), (16.5, 13), (19, 7.5)], r=S.r * 0.4)
    return [line(path), sdot(circle(19.5, 6, 2.4)), sdot(circle(4.5, 5, 1.2)), sdot(circle(10.5, 4.5, 1.2)),
            sdot(circle(20.5, 18.5, 1.2)), sdot(circle(13.5, 20, 1.2))]


# ============================================================================ mechanics

@icon("inclined-plane", CAT, "Ramp with a box resting on the slope and an arrow pointing up the slope",
      tags=["ramp", "slope", "simple machine", "physics", "force", "mechanics", "incline", "box"])
def _(S):
    ang = math.atan2(12, 19)
    ux, uy = math.cos(ang), -math.sin(ang)
    nx, ny = -uy * -1, ux * -1  # unit normal pointing up-left, away from the slope
    nx, ny = -math.sin(ang), -math.cos(ang)
    c = (10.5 + nx * 3.4, 14.4 + ny * 3.4)
    h = 2.2
    box = poly([(c[0] + a * ux * h + b * nx * h, c[1] + a * uy * h + b * ny * h) for a, b in ((-1, -1), (1, -1), (1, 1), (-1, 1))],
               closed=True, r=S.r * 0.3)
    tail = (c[0] + nx * 5.2 - ux * 2, c[1] + ny * 5.2 - uy * 2)
    head = (c[0] + nx * 5.2 + ux * 3.5, c[1] + ny * 5.2 + uy * 3.5)
    return [shell(poly([(2.5, 21), (21.5, 21), (21.5, 9)], closed=True, r=S.r * 0.7), stroke_miterlimit="3"), shell(box),
            line(arrow(tail[0], tail[1], head[0], head[1], 2.0))]


@icon("wheel-and-axle", CAT, "Large wheel on a narrow axle with a rope wound on the axle lifting a bucket",
      tags=["simple machine", "windlass", "well", "winch", "physics", "mechanics", "rope", "bucket"])
def _(S):
    bucket = poly([(8.2, 16.5), (14.8, 16.5), (13.6, 21.5), (9.4, 21.5)], closed=True, r=S.r * 0.4)
    return [shell(circle(9.5, 8.5, 7)), detail(circle(9.5, 8.5, 2.2)), line(seg(11.7, 8.5, 11.7, 16.5)),
            shell(bucket)]


@icon("free-body-diagram", CAT, "Small square with four force arrows pointing out up, down, left and right",
      tags=["forces", "physics", "mechanics", "newton", "vectors", "net force", "equilibrium", "diagram"])
def _(S):
    return [shell(rect(8.5, 8.5, 7, 7, min(S.R, 1.2))),
            line(arrow(12, 7, 12, 1.8, 2.0)), line(arrow(12, 17, 12, 22.2, 2.0)),
            line(arrow(7, 12, 1.8, 12, 2.0)), line(arrow(17, 12, 22.2, 12, 2.0))]


@icon("friction", CAT, "Block on a rough surface with a long push arrow forward and a short arrow pushing back",
      tags=["rough surface", "resistance", "force", "physics", "mechanics", "drag", "sliding", "grip"])
def _(S):
    rough = poly([(3, 15.5), (5, 13.5), (7, 15.5), (9.5, 13.5), (12, 15.5), (14.5, 13.5), (17, 15.5), (19, 13.5), (21, 15.5)], r=S.r * 0.3)
    return [shell(rect(3, 3, 9, 8, min(S.R, 1.5))), line(rough),
            line(arrow(14, 7, 21, 7, 2.2)), line(arrow(20, 20, 14.5, 20, 1.8))]


def dashed_curve(pts, on, off):
    """Dash segments (d-strings) along a polyline."""
    out, cur, draw, left = [], [pts[0]], True, on
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        ln = math.hypot(x1 - x0, y1 - y0)
        t = 0.0
        while t < ln - 1e-9:
            step = min(left, ln - t)
            t += step
            left -= step
            p = (x0 + (x1 - x0) * t / ln, y0 + (y1 - y0) * t / ln)
            if draw:
                cur.append(p)
            if left <= 1e-9:
                if draw and len(cur) > 1:
                    out.append(pts_d(cur))
                draw = not draw
                left = on if draw else off
                cur = [p] if draw else []
    if draw and len(cur) > 1:
        out.append(pts_d(cur))
    return out


@icon("projectile-motion", CAT, "Ball at the end of a dashed arc launched from the ground",
      tags=["trajectory", "parabola", "ballistics", "physics", "mechanics", "launch", "thrown ball", "arc"])
def _(S):
    pts = [(3.5 + 15.5 * t / 40, 18 - 13 * (1 - ((t / 20) - 1) ** 2)) for t in range(0, 41)]
    return [line("".join(dashed_curve(pts, 2.6, 3.3))), line(seg(2, 21.5, 22, 21.5)), sdot(circle(19.5, 17, 2.4))]


@icon("gravity", CAT, "Apple falling with a downward arrow above the ground",
      tags=["falling", "newton", "apple", "physics", "mechanics", "weight", "drop", "gravitational force"])
def _(S):
    apple = ("M9.5 7.8C7 6.6 3.5 8.2 3.5 12.4 3.5 16 6 18.5 8 18.5 8.8 18.5 9.2 18.2 9.5 18.2 9.8 18.2 10.2 18.5 11 18.5 13 18.5 15.5 16 15.5 12.4 15.5 8.2 12 6.6 9.5 7.8Z")
    return [shell(apple), line("M9.5 7.8C9.5 6 10 4.5 11 3.3"), line("M10.5 5Q13 3 14.8 4.6"),
            line(arrow(20, 3, 20, 15, 2.4)), line(seg(2, 21.5, 22, 21.5))]


# ============================================================================ toys, fluids and heat

@icon("balancing-bird", CAT, "Toy bird with long drooping wings balancing its beak on a fingertip",
      tags=["balancing toy", "center of gravity", "physics", "equilibrium", "toy", "parrot", "balance", "fingertip"])
def _(S):
    wings = poly([(12, 3.5), (21.5, 13.5), (21.5, 18), (12, 8.5), (2.5, 18), (2.5, 13.5)], closed=True, r=S.r * 0.5)
    beak = poly([(9.5, 8), (14.5, 8), (12, 13.5)], closed=True, r=S.r * 0.4)
    return [shell(union(wings, beak)), line("M9.5 22V18.5a2.5 2.5 0 0 1 5 0V22")]


@icon("drinking-bird", CAT, "Glass toy bird with a top hat dipping its beak into a glass of water",
      tags=["dipping bird", "toy", "heat engine", "physics", "novelty", "evaporation", "desk toy", "thermodynamics"])
def _(S):
    return [shell(circle(6, 17, 3.8)), line(seg(7, 13.3, 9.5, 7)),
            shell(circle(10.5, 5, 2.6)), line(seg(7.5, 1.8, 13.5, 1.8)),
            line(seg(13, 6.5, 15.5, 12)), line(seg(12.5, 10, 12.5, 21.5)),
            line(poly([(16, 14.5), (16, 21.5), (22, 21.5), (22, 14.5)]))]


@icon("hookes-law-spring", CAT, "Coiled spring hanging from a bar, stretched by a weight with a length arrow",
      tags=["hooke", "spring", "elasticity", "physics", "stretch", "extension", "force", "mass on spring"])
def _(S):
    zig = poly([(9, 3), (9, 5), (5.5, 6.5), (12.5, 9), (5.5, 11.5), (12.5, 14), (9, 15.5), (9, 16.5)], r=S.r * 0.3)
    return [line(seg(3, 3, 15, 3)), line(zig), shell(rect(5.5, 16.5, 7, 5, min(S.R, 1.5))),
            line(arrow(19.5, 3.5, 19.5, 21, 1.8)), line(arrow(19.5, 20.5, 19.5, 3, 1.8))]


@icon("buoyancy", CAT, "Block floating in water with a large upward arrow below and a small downward arrow above",
      tags=["floating", "archimedes", "upthrust", "physics", "density", "fluid", "float", "displacement"])
def _(S):
    water = wave_line(2, 22, 10.5, 1.0, 4)
    return [shell(rect(7, 3, 8, 8, min(S.R, 1.5))), line(water),
            line(arrow(11, 21.5, 11, 14.5, 2.2)), line(arrow(19.5, 3.5, 19.5, 7.5, 1.5))]


@icon("density-column", CAT, "Tall cylinder with stacked liquid layers and a ball floating in one layer",
      tags=["density tower", "liquid layers", "science experiment", "chemistry", "physics", "layered liquids", "floating ball"])
def _(S):
    return [shell(rect(6.5, 2, 11, 20, S.R)), detail(seg(6.5, 7, 17.5, 7)), detail(seg(6.5, 16, 17.5, 16)),
            detail(seg(6.5, 19.5, 17.5, 19.5)), sdot(circle(12, 11.5, 2.2))]


@icon("siphon", CAT, "Bent tube running from a higher container over the rim down into a lower container",
      tags=["siphoning", "tube", "liquid transfer", "physics", "pressure", "drain", "fluid", "gravity feed"])
def _(S):
    return [shell(rect(2.5, 8, 9, 7, min(S.R, 2))), shell(rect(13.5, 16.5, 8, 5.5, min(S.R, 2))),
            line(poly([(6.5, 8), (6.5, 3), (17.5, 3), (17.5, 16.5)], r=S.r)),
            detail(seg(6.5, 8, 6.5, 12.5)), detail(seg(17.5, 16.5, 17.5, 19.5))]


@icon("capillary-action", CAT, "Three thin tubes of different widths in water with the liquid highest in the narrowest",
      tags=["capillarity", "tubes", "water rise", "surface tension", "physics", "chemistry", "wicking", "narrow tube"])
def _(S):
    walls = [line(poly([(x, 2.5), (x, 18.5)])) for x in (4.5, 10.5, 15.5, 19.5)]
    return walls + [line(poly([(2, 13.5), (2, 21.5), (22, 21.5), (22, 13.5)])), line(wave_line(2.5, 21.5, 17.5, 0.8, 2)),
                    sdot(rect(5.5, 14.5, 4, 2)), sdot(rect(11.5, 10, 3, 6)), sdot(rect(16.5, 5.5, 2, 10.5))]


@icon("meniscus", CAT, "Close view of a graduated tube with a curved liquid surface and a dashed eye-level line",
      tags=["liquid surface", "reading volume", "burette reading", "graduated cylinder", "chemistry", "measurement", "eye level", "curved surface"])
def _(S):
    return [line(seg(7, 2.5, 7, 21.5)), line(seg(17, 2.5, 17, 21.5)),
            line("M7.5 9.5C8.5 13 10 13.5 12 13.5C14 13.5 15.5 13 16.5 9.5"),
            line(seg(1.5, 13.5, 3.5, 13.5)), line(seg(20.5, 13.5, 22.5, 13.5)),
            sdot(rect(8.5, 17, 3, 1.5)), sdot(rect(12.5, 17, 3, 1.5)), sdot(rect(8.5, 20, 1.5, 1.2))]


@icon("convection-current", CAT, "Pot over a flame with an arrow rising in the middle and arrows falling at the sides",
      tags=["convection", "heat transfer", "boiling water", "physics", "thermal", "rising heat", "circulation", "currents"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 11.5, S.R)), detail(arrow(12, 11, 12, 5.5, 1.8)),
            detail(arrow(6.5, 5.5, 6.5, 11, 1.8)), detail(arrow(17.5, 5.5, 17.5, 11, 1.8)),
            sdot(flame_d(12, 15.3, 5, 6.7))]


@icon("bimetallic-strip", CAT, "Two-layer metal strip bending upward over a small flame",
      tags=["thermostat", "heat expansion", "thermal expansion", "physics", "metal", "bending", "temperature switch"])
def _(S):
    center = "M3.5 8.5C10 8.5 15 8 19.5 3.5"
    band = stroke_d(center, 6.5, "butt", "round")
    return [shell(band), detail(center), line(seg(3, 3, 3, 14)), sdot(flame_d(14, 14.3, 5, 7.7))]


@icon("galileo-thermometer", CAT, "Tall sealed glass cylinder holding floating glass balls at different heights",
      tags=["glass thermometer", "floating spheres", "temperature", "density", "decor", "room thermometer", "physics", "weather"])
def _(S):
    return [shell(rect(6.5, 2, 11, 17.5, S.R)), sdot(circle(10.5, 6.5, 1.8)), sdot(circle(13.5, 10.5, 1.8)),
            sdot(circle(10.5, 15, 1.8)), line(seg(6, 22, 18, 22))]


@icon("calorimeter", CAT, "Insulated cup with a lid, a thermometer and a stirrer poking through",
      tags=["heat measurement", "chemistry lab", "specific heat", "energy", "insulated cup", "physics", "thermometer", "stirrer"])
def _(S):
    cup = poly([(5, 13), (19, 13), (17.5, 21.5), (6.5, 21.5)], closed=True, r=S.r * 0.5)
    return [shell(cup), line(seg(3, 9, 21, 9)), line(seg(9, 2.5, 9, 9)), detail(seg(9, 9, 9, 17)),
            line(seg(15, 2.5, 15, 9)), detail(seg(15, 9, 15, 17)), line(seg(13, 2.5, 17, 2.5))]


@icon("gas-piston", CAT, "Cylinder with a movable piston on top, gas particles below and an upward pressure arrow",
      tags=["pressure", "gas law", "boyle", "compression", "physics", "syringe", "particles", "thermodynamics", "volume"])
def _(S):
    return [line(poly([(3, 4), (3, 21.5), (16, 21.5), (16, 4)])), line(seg(3.5, 9.5, 15.5, 9.5)),
            line(seg(9.5, 9.5, 9.5, 1.5)), line(seg(6.5, 1.8, 12.5, 1.8)),
            sdot(circle(7, 14, 1.2)), sdot(circle(12, 13.5, 1.2)), sdot(circle(9.5, 18, 1.2)),
            line(arrow(20, 19.5, 20, 11, 1.8))]


@icon("convex-lens", CAT, "Lens thicker in the middle with parallel rays entering and meeting at a focal point",
      tags=["converging lens", "optics", "focus", "focal point", "magnifier", "physics", "light rays", "glass lens"])
def _(S):
    lens = "M9 2.5C14 7 14 17 9 21.5C4 17 4 7 9 2.5Z"
    return [shell(lens), line(poly([(1.5, 7.5), (9, 7.5), (21, 12)])), line(seg(1.5, 12, 21, 12)),
            line(poly([(1.5, 16.5), (9, 16.5), (21, 12)])), sdot(circle(21, 12, 1.1))]


@icon("concave-lens", CAT, "Lens thinner in the middle with parallel rays spreading outward after passing through",
      tags=["diverging lens", "optics", "spreading rays", "physics", "light", "glass lens", "myopia", "refraction"])
def _(S):
    lens = poly([(5.5, 2.5), (12.5, 2.5)], r=0)
    body = "M5 2.5H13C11 9 11 15 13 21.5H5C7 15 7 9 5 2.5Z"
    return [shell(body), line(poly([(1.5, 8), (9, 8), (21.5, 3.5)])), line(seg(1.5, 12, 21.5, 12)),
            line(poly([(1.5, 16), (9, 16), (21.5, 20.5)]))]


# ============================================================================ optics and waves

@icon("light-refraction", CAT, "Ray entering a glass block at an angle, bending inside and leaving parallel to its first path",
      tags=["refraction", "bending light", "optics", "glass block", "physics", "snell", "light ray", "prism experiment"])
def _(S):
    return [shell(rect(2.5, 8.5, 19, 7, min(S.R, 2))), line(seg(3, 1.5, 8.5, 8.5)),
            detail(seg(8.5, 8.5, 11.5, 15.5)), line(arrow(11.5, 15.5, 17, 22, 2.0))]


@icon("light-reflection", CAT, "Ray striking a flat mirror and bouncing off at an equal angle with a dashed normal line",
      tags=["reflection", "mirror", "optics", "angle of incidence", "physics", "light ray", "bounce", "law of reflection"])
def _(S):
    return [line(seg(2, 19.5, 22, 19.5)), line(seg(4, 3.5, 12, 18.5)), line(arrow(12, 18.5, 20, 3.5, 2.0)),
            line(seg(12, 2.5, 12, 6)), line(seg(12, 9, 12, 12))]


@icon("periscope", CAT, "Z-shaped tube with angled mirrors at the two bends for seeing over an obstacle",
      tags=["submarine", "optics", "mirror", "see over", "physics", "tube", "light path", "viewing tube"])
def _(S):
    tube = poly([(3, 2.5), (15, 2.5), (15, 16), (21, 16), (21, 21.5), (9, 21.5), (9, 8), (3, 8)], closed=True, r=S.r * 0.4)
    return [shell(tube), detail(seg(9.8, 3.5, 14.2, 7.5)), detail(seg(9.8, 20.5, 14.2, 16.5))]


@icon("camera-obscura", CAT, "Dark box with a pinhole on one side and an upside-down tree projected on the far wall",
      tags=["pinhole camera", "optics", "inverted image", "projection", "light", "physics", "early photography", "dark room"])
def _(S):
    box = poly([(2.5, 9.5), (2.5, 4.5), (21.5, 4.5), (21.5, 19.5), (2.5, 19.5), (2.5, 14.5)], r=S.r * 0.6)
    return [shell(box), detail(seg(2.5, 12, 11, 12)), detail(seg(17, 7.5, 17, 11)),
            detail(poly([(14, 11), (20, 11), (17, 16.5)], closed=True))]


@icon("laser", CAT, "Rectangular emitter shooting a straight beam that ends in a small star",
      tags=["laser beam", "light", "optics", "photonics", "pointer", "physics", "ray", "beam"])
def _(S):
    return [shell(rect(2, 8, 8, 8, S.R * 0.5)), detail(seg(10, 12, 12, 12)), line(seg(10, 12, 16.5, 12)),
            sdot(poly(star_pts(19.5, 12, 3.4, 1.1, 4), closed=True))]


@icon("double-slit-experiment", CAT, "Waves passing a barrier with two slits and spreading as overlapping arcs",
      tags=["young", "interference", "wave", "slits", "quantum", "physics", "diffraction", "light experiment"])
def _(S):
    return [line(seg(8, 2, 8, 6)), line(seg(8, 10, 8, 14)), line(seg(8, 18, 8, 22)),
            line(seg(2.5, 3, 2.5, 21)), line(arc(8, 8, 5.5, -55, 55)), line(arc(8, 16, 5.5, -55, 55)),
            line(arc(8, 8, 10.5, -40, 40)), line(arc(8, 16, 10.5, -40, 40))]


@icon("mass-energy-equivalence", CAT, "The equation E equals m c squared set in bold strokes",
      tags=["einstein", "e=mc2", "relativity", "equation", "physics", "formula", "energy", "mass"])
def _(S):
    e = "M8.5 2.5H4V8.5H8.5M4 5.5H7.5"
    eq = seg(11.5, 4, 17, 4) + seg(11.5, 7, 17, 7)
    m = "M3 21V15.5M3 17.5Q3 15.5 5.2 15.5Q7.4 15.5 7.4 17.5V21M7.4 17.5Q7.4 15.5 9.6 15.5Q11.8 15.5 11.8 17.5V21"
    c = arc(16.3, 18.3, 2.8, 40, 320)
    two = "M18.5 11.5Q18.5 10.3 19.8 10.3Q21.1 10.3 21.1 11.5Q21.1 12.4 18.5 14.8H21.4"
    return [line(e), line(eq), line(m), line(c), line(two)]


@icon("electromagnetic-spectrum", CAT, "One wave whose peaks bunch closer together from left to right",
      tags=["wavelength", "frequency", "radio waves", "light", "x-ray", "physics", "chirp", "spectrum of light"])
def _(S):
    pts = []
    n = 44
    for i in range(n + 1):
        t = i / n
        cyc = 0.45 * t + 2.3 * t * t
        pts.append((2 + 20 * t, 12 - 7 * math.sin(2 * math.pi * cyc)))
    return [line(smooth(pts))]


@icon("emission-spectrum", CAT, "Baseline with a few sharp bright lines of different heights at uneven spacing",
      tags=["spectral lines", "atomic spectrum", "chemistry", "physics", "wavelengths", "spectroscopy", "element fingerprint"])
def _(S):
    return [line(seg(2, 20, 22, 20)), line(seg(5.5, 20, 5.5, 5)), line(seg(10, 20, 10, 11)), line(seg(16.5, 20, 16.5, 7.5))]


@icon("spectroscope", CAT, "Handheld tube with a slit at one end and an eyepiece, with a small rainbow arch above",
      tags=["spectrometer", "light analysis", "diffraction grating", "physics", "chemistry", "rainbow", "optics tool"])
def _(S):
    return [shell(rect(2.5, 12, 14, 7, min(S.R, 2))), shell(rect(16.5, 13.5, 5, 4, 1)), detail(seg(5.5, 13.5, 5.5, 17.5)),
            line(arc(9.5, 8.5, 2, 180, 360)), line(arc(9.5, 8.5, 5, 180, 360))]


@icon("doppler-effect", CAT, "Moving dot with sound waves bunched close in front and spread out behind",
      tags=["wave shift", "frequency change", "siren", "physics", "sound waves", "moving source", "pitch", "acoustics"])
def _(S):
    return [sdot(circle(10, 12, 2.0)), line(arc(10, 12, 4.3, -45, 45)), line(arc(10, 12, 7.8, -42, 42)),
            line(arc(10, 12, 11.3, -40, 40)), line(arc(10, 12, 5.5, 140, 220))]


@icon("wavelength", CAT, "Sine wave with a double-headed arrow measuring the distance from one crest to the next",
      tags=["wave", "crest", "period", "physics", "measure", "oscillation", "distance", "sine wave"])
def _(S):
    pts = [(2 + 20 * i / 20, 16 - 4.2 * math.sin(2 * math.pi * 2 * i / 20 - 0.3 * math.pi)) for i in range(21)]
    return [line(smooth(pts)), line(arrow(7, 5, 17, 5, 2.0)), line(arrow(17, 5, 7, 5, 2.0)),
            line(seg(7, 3, 7, 8)), line(seg(17, 3, 17, 8))]


@icon("longitudinal-wave", CAT, "Horizontal coil with bunched and stretched sections and a direction arrow below",
      tags=["compression wave", "sound wave", "slinky", "physics", "rarefaction", "spring wave", "acoustics", "wave types"])
def _(S):
    zig = poly([(2.5, 12), (4.5, 6), (6.5, 14.5), (8.5, 6), (10.5, 14.5), (15, 6), (19, 14.5), (21.5, 9)], r=S.r * 0.2)
    return [line(zig), line(arrow(5, 20.5, 19, 20.5, 2.0))]


@icon("light-meter", CAT, "Handheld meter with a white dome sensor on top and a digital readout",
      tags=["lux meter", "exposure meter", "photography", "light measurement", "luminance", "sensor", "illuminance"])
def _(S):
    return [shell(rect(5.5, 9, 13, 13, S.R)), shell("M8 9A4 4 0 0 1 16 9Z"),
            sdot(rect(8.5, 12.5, 7, 3.2, 0.6)), sdot(circle(12, 19, 1.4))]


@icon("radiometer", CAT, "Glass bulb on a stand with four vanes spinning on a pivot inside",
      tags=["crookes", "light mill", "vacuum bulb", "physics", "radiation", "spinning vanes", "science toy", "solar"])
def _(S):
    body = "M9.4 18.2A8 8 0 1 1 14.6 18.2Z"
    parts = [shell(body)]
    cx, cy = 12, 10.3
    for a in (45, 135, 225, 315):
        e = polar(cx, cy, 4.2, a)
        v = polar(0, 0, 1.7, a + 90)
        parts.append(detail(seg(cx, cy, *e)))
        parts.append(sdot(stroke_d(seg(e[0] - v[0], e[1] - v[1], e[0] + v[0], e[1] + v[1]), 1.5, "butt")))
    return parts + [line(seg(12, 18.2, 12, 20.5)), line(seg(8, 22, 16, 22))]


# ============================================================================ electricity and magnetism

@icon("electric-circuit", CAT, "Rectangle of wire joining a bulb, a battery and an open switch",
      tags=["circuit diagram", "wiring", "battery", "switch", "bulb", "physics", "electronics", "current", "simple circuit"])
def _(S):
    r = S.r * 0.8
    left = poly([(8.8, 5), (3, 5), (3, 19), (10, 19)], r=r)
    top = poly([(15.2, 5), (21, 5), (21, 9)], r=r)
    right = poly([(21, 15.5), (21, 19), (14, 19)], r=r)
    return [line(left), line(top), line(right), line(seg(21, 15.5, 17.8, 10.5)),
            line(seg(10, 15.5, 10, 22)), line(seg(14, 17, 14, 21)),
            shell(circle(12, 5, 3.2))]


@icon("electromagnet", CAT, "Iron nail wrapped in coiled wire joined to a battery",
      tags=["magnet", "coil", "solenoid", "iron core", "physics", "science project", "battery", "magnetism", "paper clips"])
def _(S):
    nail = poly([(3, 6), (17, 6), (21, 8.5), (17, 11), (3, 11)], closed=True, r=S.r * 0.3)
    coil = [detail(seg(6.5, 13.5, 8, 3.5)), detail(seg(11, 13.5, 12.5, 3.5)), detail(seg(15.5, 13.5, 17, 3.5))]
    return [shell(nail)] + coil + [
        line(seg(6.5, 13.5, 6.5, 17)), line(seg(15.5, 13.5, 15.5, 17)),
        shell(rect(4, 17, 14, 5, min(S.R, 1.5)))]


@icon("bar-magnet", CAT, "Rectangular bar magnet divided into two halves marked N and S",
      tags=["magnet", "north pole", "south pole", "magnetism", "physics", "polarity", "magnetic", "school science"])
def _(S):
    n = stroke_d("M5 14.5V9.5L8.6 14.5V9.5", 1.4, "butt", "miter")
    sl = stroke_d("M18.4 9.5H15.4V12H18.4V14.5H15.4", 1.4, "butt", "miter")
    return [shell(rect(2.5, 6.5, 19, 11, min(S.R, 2.5))), detail(seg(12, 6.5, 12, 17.5)), sdot(n), sdot(sl)]


@icon("magnetic-field-lines", CAT, "Bar magnet in the middle with curved lines looping from one pole around to the other",
      tags=["magnetic field", "flux lines", "magnet", "physics", "poles", "force field", "iron filings", "magnetism"])
def _(S):
    return [shell(rect(8, 9.5, 8, 5, S.R)), detail(seg(12, 9.5, 12, 14.5)),
            line("M16 10.5C21.5 8.5 19 2.8 12 2.8C5 2.8 2.5 8.5 8 10.5"),
            line("M16 13.5C21.5 15.5 19 21.2 12 21.2C5 21.2 2.5 15.5 8 13.5")]


@icon("electric-field-lines", CAT, "Plus charge and minus charge circles with curved lines arcing between them",
      tags=["electric field", "charges", "physics", "electrostatics", "dipole", "positive negative", "field lines"])
def _(S):
    return [shell(circle(5, 12, 3.4)), shell(circle(19, 12, 3.4)),
            sdot(plus_d(5, 12, 1.6, 1.2)), sdot(minus_d(19, 12, 1.6, 1.2)),
            line(seg(9.4, 12, 14.6, 12)), line(arrow_head((14.6, 12), 0, 1.5)),
            line("M7.5 8Q12 1.5 16.5 8"), line("M7.5 16Q12 22.5 16.5 16")]


@icon("right-hand-rule", CAT, "Fist with the thumb up beside a wire with a curved arrow showing the loop direction",
      tags=["physics", "current direction", "magnetic field direction", "thumb", "electromagnetism", "hand", "ampere", "grip rule"])
def _(S):
    hand = union(rect(2.5, 11, 10, 9, 3), rect(4, 2.5, 3.6, 11, 1.8))
    return [shell(hand), detail(seg(8, 15, 12.5, 15)), line(seg(18, 2, 18, 22)),
            line("M14.8 13.8Q18 18 21.4 13.8"), line(arrow_head((21.4, 13.8), -50, 1.6))]


@icon("leyden-jar", CAT, "Glass jar with a foil band at the bottom and a rod with a ball on top through the lid",
      tags=["capacitor", "early battery", "static charge", "electricity history", "physics", "storage", "electrostatics"])
def _(S):
    return [shell(rect(5, 9, 14, 13, S.R)), detail(seg(5, 15.5, 19, 15.5)), line(seg(12, 9, 12, 5)),
            sdot(circle(12, 3.8, 1.9)), sdot(rect(6, 16.5, 12, 4.5))]


@icon("electrostatic-generator", CAT, "Large metal sphere on a column and base, with a spark jumping to a small ball",
      tags=["van de graaff", "static charge", "hair raising", "physics", "high voltage", "science museum", "spark"])
def _(S):
    return [shell(circle(10, 8.5, 6.2)), line(seg(10, 14.7, 10, 18)),
            shell(poly([(5, 21.5), (6.5, 18), (13.5, 18), (15, 21.5)], closed=True, r=S.r * 0.3)),
            line(poly([(16.4, 8.5), (18.6, 10.4), (17.4, 11.6), (19.6, 13.4)])), sdot(circle(20.2, 16.5, 1.7))]


@icon("faraday-cage", CAT, "Wire mesh cage with a lightning bolt striking beside it",
      tags=["shielding", "electromagnetic shield", "lightning protection", "physics", "mesh", "grounded", "safety", "enclosure"])
def _(S):
    bolt = poly([(21, 2), (16, 11), (19.4, 11), (17, 21)], closed=True)
    return [shell(rect(2.5, 6, 12, 15, min(S.R, 2.5))), detail(seg(8.5, 6, 8.5, 21)), detail(seg(2.5, 13.5, 14.5, 13.5)),
            sdot(bolt)]


@icon("static-electricity", CAT, "Balloon beside a head whose hair stands up toward it",
      tags=["static charge", "balloon", "hair", "rubbing", "physics", "attraction", "electrostatic", "science experiment"])
def _(S):
    return [shell(circle(8, 16, 4.6)), line(seg(5.5, 11.5, 4, 7.5)), line(seg(8, 11, 8.3, 6.5)), line(seg(10.5, 11.5, 12.5, 8)),
            shell(ellipse(17.5, 8, 3.8, 4.6)), sdot(poly([(17.5, 12.8), (16.3, 14.4), (18.7, 14.4)], closed=True)),
            line("M17.5 14.4Q19.5 17.5 17 21.5")]


@icon("ohms-law", CAT, "Triangle divided into three parts with V on top and I and R below",
      tags=["voltage", "current", "resistance", "v=ir", "electronics", "physics", "formula", "triangle", "circuit law"])
def _(S):
    v = stroke_d("M10 8.6L12 12L14 8.6", 1.3, "butt", "miter")
    i = stroke_d("M7.2 16.4V19.8", 1.3, "butt", "miter")
    r = stroke_d("M15.6 19.8V16.4H17.3Q18.5 16.4 18.5 17.5Q18.5 18.6 17.3 18.6H15.6M17.3 18.6L18.6 19.8", 1.2, "butt", "round")
    return [shell(poly([(12, 2.5), (22, 21), (2, 21)], closed=True, r=L(S, 0, 1.6)), stroke_miterlimit="3"),
            detail(seg(6.4, 14, 17.6, 14)), detail(seg(12, 14, 12, 21)), sdot(v), sdot(i), sdot(r)]


@icon("transformer-coil", CAT, "Square iron core with few coil turns on one side and many turns on the other",
      tags=["transformer", "windings", "voltage", "inductor", "electricity", "physics", "power", "primary secondary"])
def _(S):
    ring = minus(rect(5, 3, 14, 18, S.R), rect(10, 7.5, 4, 9, min(S.R, 1.5)))
    return [shell(ring), line("M5 5A3 3 0 0 0 5 11"), line("M5 11A3 3 0 0 0 5 17"),
            line("M19 5A2 2 0 0 1 19 9"), line("M19 9A2 2 0 0 1 19 13"), line("M19 13A2 2 0 0 1 19 17")]


@icon("voltmeter", CAT, "Analog dial meter with a needle across a scale arc and a large V on its face",
      tags=["voltage meter", "gauge", "analog meter", "electronics", "measure volts", "test equipment", "physics", "dial"])
def _(S):
    needle_end = polar(12, 12, 5.6, -52)
    v = stroke_d("M8 15H10.6M13.4 15H16M9.4 15L12 19.6L14.6 15", 1.5, "butt", "miter")
    return [shell(rect(2.5, 2.5, 19, 19, S.R)), detail(arc(12, 12, 6.8, 205, 335)),
            detail(seg(12, 12, *needle_end)), sdot(circle(12, 12, 1.4)), sdot(v)]
