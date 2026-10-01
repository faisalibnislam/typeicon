"""TypeIcon Core: notation (batch notation_004).

Schematic symbols, waveforms, chemistry notation, gender symbols, flowchart and UML shapes and zodiac glyphs.
Schematic symbols sit on a horizontal or vertical signal line with leads reaching the live-area edge.
"""
from __future__ import annotations

import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "notation"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


def lead(S, x1, y1, x2, y2):
    """Open stroke whose free end (x2, y2) stays inside the live area in both cap styles."""
    k = L(S, 0, 1)
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    return line(seg(x1, y1, x2 - dx / n * k, y2 - dy / n * k))


def head_pts(tip, frm, length=3.5, hw=2.0):
    dx, dy = tip[0] - frm[0], tip[1] - frm[1]
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    bx, by = tip[0] - ux * length, tip[1] - uy * length
    return [tip, (bx - uy * hw, by + ux * hw), (bx + uy * hw, by - ux * hw)]


def head(S, tip, frm, length=3.5, hw=2.0, kind="solid"):
    return Part("dot" if kind == "detail" else kind, poly(head_pts(tip, frm, length, hw), closed=True, r=L(S, 0, 0.6)))


def arrow(S, a, b, length=3.5, hw=2.0, kind="solid"):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    e = (b[0] - dx / n * (length - 0.5), b[1] - dy / n * (length - 0.5))
    shaft = line(seg(a[0], a[1], e[0], e[1])) if kind == "solid" else detail(seg(a[0], a[1], e[0], e[1]))
    return [shaft, head(S, b, a, length, hw, kind)]


def zigzag(x0, x1, cy, amp, n):
    s = (x1 - x0) / n
    pts = [(x0, cy)]
    for i in range(n):
        pts.append((x0 + s * (i + 0.5), cy - amp if i % 2 == 0 else cy + amp))
    pts.append((x1, cy))
    return pts


def plus(cx, cy, a=1.75, kind=detail):
    return [kind(seg(cx - a, cy, cx + a, cy)), kind(seg(cx, cy - a, cx, cy + a))]


def minus(cx, cy, a=1.75, kind=detail):
    return [kind(seg(cx - a, cy, cx + a, cy))]


# ============================================================================ electrical symbols

@icon("ground-symbol", CAT, "Ground symbol: a vertical lead ending in three horizontal bars that get shorter.",
      tags=["ground", "earth", "schematic", "circuit symbol", "electrical", "electronics", "0v"])
def _(S):
    return [lead(S, 12, 2, 12, 10.5), line(seg(3.5, 10.5, 20.5, 10.5)),
            line(seg(7, 15, 17, 15)), line(seg(9.5, 19.5, 14.5, 19.5))]


@icon("chassis-ground-symbol", CAT, "Chassis ground symbol: a vertical lead ending in a bar with three slanted teeth below.",
      tags=["chassis ground", "frame ground", "ground", "schematic", "circuit symbol", "electrical"])
def _(S):
    return [lead(S, 12, 2, 12, 11.5), line(seg(3.5, 11.5, 20.5, 11.5)),
            line(seg(8, 11.5, 5, 19.5)), line(seg(13.5, 11.5, 10.5, 19.5)), line(seg(19, 11.5, 16, 19.5))]


@icon("protective-earth-symbol", CAT, "Protective earth symbol: a ground symbol of three shrinking bars inside a circle.",
      tags=["protective earth", "earth", "ground", "pe", "safety", "electrical", "class i"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(seg(12, 4, 12, 8)), detail(seg(7.5, 8, 16.5, 8)),
            detail(seg(9, 12, 15, 12)), detail(seg(10.5, 16, 13.5, 16))]


@icon("battery-cell-symbol", CAT, "Battery cell schematic symbol: a long plate and a short thick plate with plus and minus marks.",
      tags=["battery", "cell", "schematic", "circuit symbol", "power", "electrochemical", "polarity"])
def _(S):
    return [lead(S, 2, 12, 10, 12), lead(S, 17, 12, 22, 12), line(seg(10, 5, 10, 19)),
            sq(14, 8.5, 3, 7, L(S, 0, 1)), *plus(5, 5.5, 2, line), *minus(19, 5.5, 2, line)]


@icon("ac-source-symbol", CAT, "AC voltage source symbol: a circle holding one sine wave, with leads at the top and bottom.",
      tags=["ac source", "alternating current", "voltage source", "sine", "schematic", "mains"])
def _(S):
    return [shell(circle(12, 12, 7)), lead(S, 12, 2, 12, 5), lead(S, 12, 22, 12, 19),
            detail("M8 12q2-3.5 4 0t4 0")]


@icon("dc-source-symbol", CAT, "DC voltage source symbol: a circle with a plus above a minus and leads at the top and bottom.",
      tags=["dc source", "direct current", "voltage source", "plus minus", "schematic", "supply"])
def _(S):
    return [shell(circle(12, 12, 7)), lead(S, 12, 2, 12, 5), lead(S, 12, 22, 12, 19),
            *plus(12, 9, 1.75), *minus(12, 15.25, 1.75)]


@icon("current-source-symbol", CAT, "Current source symbol: a circle with an upward arrow inside and leads at the top and bottom.",
      tags=["current source", "constant current", "schematic", "circuit symbol", "amps", "source"])
def _(S):
    return [shell(circle(12, 12, 7)), lead(S, 12, 2, 12, 5), lead(S, 12, 22, 12, 19),
            *arrow(S, (12, 16.5), (12, 7.5), 4, 2.25, kind="detail")]


@icon("switch-symbol", CAT, "Open switch schematic symbol: two contact dots with a hinged blade lifted between them.",
      tags=["switch", "open switch", "schematic", "circuit symbol", "contact", "electrical"])
def _(S):
    return [lead(S, 2, 16, 6, 16), lead(S, 22, 16, 18, 16), dot(6, 16, 2), dot(18, 16, 2),
            line(seg(6, 16, 17, 8.5))]


@icon("push-button-symbol", CAT, "Push button schematic symbol: a bar above two contacts with a plunger stem on top.",
      tags=["push button", "pushbutton", "momentary switch", "schematic", "circuit symbol", "normally open"])
def _(S):
    return [lead(S, 2, 18, 8, 18), lead(S, 22, 18, 16, 18), dot(8, 18, 2), dot(16, 18, 2),
            line(seg(6, 12, 18, 12)), line(seg(12, 12, 12, 5)), line(seg(8, 5, 16, 5))]


@icon("fuse-symbol", CAT, "Fuse schematic symbol: a small rectangle with a line running through it lengthwise.",
      tags=["fuse", "overcurrent", "protection", "schematic", "circuit symbol", "electrical"])
def _(S):
    return [shell(rect(6, 8, 12, 8, rr(S, 2))), detail(seg(6, 12, 18, 12)),
            lead(S, 2, 12, 6, 12), lead(S, 22, 12, 18, 12)]


@icon("lamp-symbol", CAT, "Lamp schematic symbol: a circle with a looped filament inside and a lead on each side.",
      tags=["lamp", "bulb", "filament", "indicator lamp", "schematic", "circuit symbol"])
def _(S):
    return [shell(circle(12, 12, 7)), lead(S, 2, 12, 5, 12), lead(S, 22, 12, 19, 12),
            detail("M9 16L10 11.5A2 2 0 0 1 14 11.5L15 16")]


@icon("motor-symbol", CAT, "Motor schematic symbol: a circle with a capital M inside and a lead on each side.",
      tags=["motor", "electric motor", "schematic", "circuit symbol", "drive", "m"])
def _(S):
    return [shell(circle(12, 12, 7)), lead(S, 2, 12, 5, 12), lead(S, 22, 12, 19, 12),
            detail(poly([(9, 15), (9, 9), (12, 13), (15, 9), (15, 15)]))]


@icon("generator-symbol", CAT, "Generator schematic symbol: a circle with a capital G inside and a lead on each side.",
      tags=["generator", "alternator", "dynamo", "schematic", "circuit symbol", "g"])
def _(S):
    return [shell(circle(12, 12, 7)), lead(S, 2, 12, 5, 12), lead(S, 22, 12, 19, 12),
            detail("M14.4 9.6A3.4 3.4 0 1 0 15.4 12H12.4")]


@icon("op-amp-symbol", CAT, "Operational amplifier symbol: a triangle pointing right with plus and minus inputs at the left.",
      tags=["op amp", "operational amplifier", "amplifier", "schematic", "circuit symbol", "analog"])
def _(S):
    return [shell(poly([(5.5, 3), (5.5, 21), (21, 12)], closed=True, r=S.r * 0.5)),
            lead(S, 2, 8.5, 5.5, 8.5), lead(S, 2, 15.5, 5.5, 15.5),
            *plus(9.5, 8.5, 2), *minus(9.5, 15.5, 2)]


@icon("zener-diode-symbol", CAT, "Zener diode symbol: a triangle pointing at a bar whose ends bend into small hooks.",
      tags=["zener", "zener diode", "voltage reference", "breakdown", "schematic", "circuit symbol"])
def _(S):
    return [shell(poly([(6.5, 6.5), (6.5, 17.5), (14, 12)], closed=True, r=S.r * 0.5)),
            lead(S, 2, 12, 6.5, 12), lead(S, 22, 12, 15.5, 12),
            line(poly([(13, 7), (15.5, 5), (15.5, 19), (18, 17)], r=L(S, 0, 0.6)))]


@icon("photodiode-symbol", CAT, "Photodiode symbol: a diode triangle and bar with two small arrows pointing in toward it.",
      tags=["photodiode", "light sensor", "diode", "photo", "schematic", "circuit symbol"])
def _(S):
    return [shell(poly([(7, 11.5), (7, 20.5), (14, 16)], closed=True, r=S.r * 0.5)),
            lead(S, 2, 16, 7, 16), lead(S, 22, 16, 15, 16), line(seg(15, 11, 15, 21)),
            *arrow(S, (3.5, 3), (8.5, 8), 3.5, 2), *arrow(S, (9.5, 2.5), (14.5, 7.5), 3.5, 2)]


@icon("variable-resistor-symbol", CAT, "Variable resistor symbol: a zigzag line with a diagonal arrow crossing through it.",
      tags=["variable resistor", "rheostat", "adjustable", "resistance", "schematic", "circuit symbol"])
def _(S):
    return [line(poly([(L(S, 2, 3), 12)] + zigzag(5, 19, 12, 3, 4) + [(L(S, 22, 21), 12)], r=L(S, 0, 0.3))),
            *arrow(S, (6, 20), (18, 4), 4, 2.25)]


@icon("polarized-capacitor-symbol", CAT, "Polarized capacitor symbol: a straight plate facing a curved plate with a plus mark.",
      tags=["polarized capacitor", "electrolytic", "capacitor", "schematic", "circuit symbol", "polarity"])
def _(S):
    return [lead(S, 2, 12, 9, 12), lead(S, 22, 12, 16.5, 12), line(seg(9, 5, 9, 19)),
            line("M14 5Q18.5 12 14 19"), *plus(5, 6.5, 1.75, line)]


@icon("wire-crossover", CAT, "Wire crossover: a horizontal wire with a small hump that jumps over a vertical wire.",
      tags=["crossover", "wires cross", "no connection", "schematic", "circuit", "jump"])
def _(S):
    return [line(f"M2 13H8.5A3.5 3.5 0 0 1 15.5 13H22"), line(seg(12, 2, 12, 22))]


@icon("thermistor-symbol", CAT, "Thermistor symbol: a small rectangle crossed by a diagonal line that turns flat at the bottom.",
      tags=["thermistor", "ntc", "ptc", "temperature sensor", "schematic", "circuit symbol"])
def _(S):
    return [shell(rect(6, 8, 12, 8, rr(S, 2))), lead(S, 2, 12, 6, 12), lead(S, 22, 12, 18, 12),
            detail(seg(10, 16, 16, 8)),
            line(poly([(3, 20), (7, 20), (10, 16)], r=L(S, 0, 0.6))), line(seg(16, 8, 19.5, 3.5))]


@icon("solar-cell-symbol", CAT, "Solar cell schematic symbol: a battery cell inside a circle with two arrows pointing in.",
      tags=["solar cell", "photovoltaic", "pv", "schematic", "circuit symbol", "energy"])
def _(S):
    return [shell(circle(14, 14, 6.5)),
            detail(seg(11.5, 10.5, 11.5, 17.5)), sq(15, 11.5, 2.5, 5, 0),
            *arrow(S, (2.5, 5), (7, 9.5), 3.5, 2), *arrow(S, (6.5, 2.5), (11, 7), 3.5, 2)]


@icon("buzzer-symbol", CAT, "Buzzer schematic symbol: a half circle dome on a flat base with two leads.",
      tags=["buzzer", "beeper", "sounder", "alarm", "schematic", "circuit symbol"])
def _(S):
    dome = "M4 13A8 8 0 0 1 20 13Z" if S.name == "line" else "M4 12A8 8 0 0 1 20 12V12.5Q20 14.5 18 14.5H6Q4 14.5 4 12.5Z"
    return [shell(dome), lead(S, 9, 14.5, 9, 22), lead(S, 15, 14.5, 15, 22)]


@icon("direct-current-symbol", CAT, "Direct current symbol: a solid bar above a row of three short dashes.",
      tags=["direct current", "dc", "current type", "power supply", "marking", "electrical"])
def _(S):
    a, b = L(S, 3, 4), L(S, 21, 20)
    return [line(seg(a, 9, b, 9)), line(seg(L(S, 3, 4), 15.5, L(S, 7, 6), 15.5)),
            line(seg(L(S, 10, 11), 15.5, L(S, 14, 13), 15.5)), line(seg(L(S, 17, 18), 15.5, L(S, 21, 20), 15.5))]


# ============================================================================ waveforms

@icon("triangle-wave", CAT, "Triangle wave: a zigzag line whose rising and falling slopes are equal.",
      tags=["triangle wave", "waveform", "signal", "oscillator", "zigzag", "function generator"])
def _(S):
    return [line(poly([(3, 12), (6, 6), (12, 18), (18, 6), (21, 12)], r=L(S, 0, 0.3)))]


@icon("pulse-wave", CAT, "Pulse wave: a flat line broken by narrow rectangular pulses at regular intervals.",
      tags=["pulse wave", "pulse train", "waveform", "digital signal", "clock", "rectangular wave"])
def _(S):
    return [line(poly([(2, 17), (4, 17), (4, 7), (8, 7), (8, 17), (14, 17), (14, 7), (18, 7), (18, 17), (22, 17)], r=L(S, 0, 1)))]


# ============================================================================ chemistry notation

@icon("benzene-ring", CAT, "Benzene ring: a hexagon with a circle drawn inside it.",
      tags=["benzene", "aromatic", "ring", "hexagon", "organic chemistry", "molecule", "structure"])
def _(S):
    return [shell(poly(regular(12, 12, 9.75, 6), closed=True, r=S.r * 1.2)), detail(circle(12, 12, 4.5))]


def _chair_pts():
    pts = []
    for i, th in enumerate([180, 240, 300, 0, 60, 120]):
        z = -2 if i % 2 == 0 else 2
        x = 12 + 0.95 * 9.5 * math.cos(math.radians(th))
        y = 12 - z * 1.5 + 1.5 * 0.4 * 9.5 * math.sin(math.radians(th))
        pts.append((x, y))
    return pts


@icon("cyclohexane-chair", CAT, "Cyclohexane chair: a six sided ring drawn as a zigzag in the chair conformation.",
      tags=["cyclohexane", "chair conformation", "ring", "organic chemistry", "stereochemistry", "molecule"])
def _(S):
    return [line(poly(_chair_pts(), closed=True, r=S.r))]


@icon("lewis-dot-structure", CAT, "Lewis dot structure: a capital letter with pairs of dots on its four sides.",
      tags=["lewis structure", "electron dots", "valence electrons", "chemistry", "octet", "atom"])
def _(S):
    return [line(poly([(9, 16), (9, 8), (15, 16), (15, 8)], r=L(S, 0, 0.5))),
            dot(10, 3.75, 1.25), dot(14, 3.75, 1.25), dot(10, 20.25, 1.25), dot(14, 20.25, 1.25),
            dot(3.75, 10, 1.25), dot(3.75, 14, 1.25), dot(20.25, 10, 1.25), dot(20.25, 14, 1.25)]


def _c_letter(cx, cy, rx, ry, S):
    a = math.radians(50)
    sx, sy = cx + rx * math.cos(a), cy - ry * math.sin(a)
    ex, ey = cx + rx * math.cos(a), cy + ry * math.sin(a)
    return line(f"M{fmt(sx)} {fmt(sy)}A{fmt(rx)} {fmt(ry)} 0 1 0 {fmt(ex)} {fmt(ey)}")


@icon("double-bond", CAT, "Double bond: two letter C atoms joined by two parallel lines.",
      tags=["double bond", "alkene", "carbon", "chemical bond", "organic chemistry", "c=c"])
def _(S):
    return [_c_letter(5.5, 12, 3.25, 5, S), _c_letter(18.5, 12, 3.25, 5, S),
            line(seg(9, 10, 15, 10)), line(seg(9, 14, 15, 14))]


@icon("triple-bond", CAT, "Triple bond: two letter C atoms joined by three parallel lines.",
      tags=["triple bond", "alkyne", "carbon", "chemical bond", "organic chemistry", "c#c"])
def _(S):
    return [_c_letter(5.5, 12, 3.25, 6, S), _c_letter(18.5, 12, 3.25, 6, S),
            line(seg(9, 8, 15, 8)), line(seg(9, 12, 15, 12)), line(seg(9, 16, 15, 16))]


@icon("wedge-dash-bond", CAT, "Stereochemistry bonds: a central atom with a solid wedge bond and a hashed wedge bond.",
      tags=["wedge bond", "dash bond", "stereochemistry", "chirality", "organic chemistry", "3d structure"])
def _(S):
    tx, ty = 5.5, 12
    ux, uy = 0.894, -0.447
    px, py = 0.447, 0.894
    bx, by, hw = 19, 6, 2.6
    solid_wedge = Part("solid", poly([(tx, ty), (bx + px * hw, by + py * hw), (bx - px * hw, by - py * hw)], closed=True, r=L(S, 0, 0.5)))
    out = [solid_wedge, dot(tx, ty, 2), line(seg(2, 12, tx, 12))]
    ux2, uy2 = 0.894, 0.447
    px2, py2 = -0.447, 0.894
    for t in (6.5, 10.5, 14.5):
        cx, cy = tx + ux2 * t, ty + uy2 * t
        h = 0.5 + 2.1 * t / 14.5
        out.append(line(seg(cx + px2 * h, cy + py2 * h, cx - px2 * h, cy - py2 * h)))
    return out


@icon("orbital-box-diagram", CAT, "Orbital box diagram: three adjoining boxes each holding an electron spin arrow.",
      tags=["orbital diagram", "electron spin", "hund's rule", "chemistry", "electron configuration", "boxes"])
def _(S):
    parts = [shell(rect(2, 4, 20, 16, rr(S, 2))), detail(seg(8.67, 4, 8.67, 20)), detail(seg(15.33, 4, 15.33, 20))]
    for cx in (5.33, 12, 18.67):
        parts += arrow(S, (cx, 16.5), (cx, 7.5), 3.5, 1.6, kind="detail")
    return parts


@icon("bra-ket-notation", CAT, "Bra-ket notation: a psi between a vertical bar and a right angle bracket.",
      tags=["bra ket", "dirac notation", "quantum mechanics", "state vector", "psi", "physics"])
def _(S):
    return [line(seg(3, 4, 3, 20)), line(seg(11.5, 4.5, 11.5, 19.5)),
            line("M7.75 7.5V10.5A3.75 3.75 0 0 0 15.25 10.5V7.5"),
            line(poly([(17, 5), (20, 12), (17, 19)], r=L(S, 0, 1.5)))]


@icon("magnetic-field-dots", CAT, "Field out of the page notation: a grid of circles each with a dot at its centre.",
      tags=["magnetic field", "out of page", "field direction", "physics", "electromagnetism", "vector field"])
def _(S):
    parts = []
    for cx in (6.5, 17.5):
        for cy in (6.5, 17.5):
            parts += [shell(circle(cx, cy, 3.5)), (Part("dot", rect(cx - 1.3, cy - 1.3, 2.6, 2.6)) if S.name == "line" else dot(cx, cy, 1.3))]
    return parts


# ============================================================================ gender symbols

def _male_arrow(S, tip, frm):
    tx, ty = tip
    return [line(seg(frm[0], frm[1], tx - 0.4, ty + 0.4)),
            line(poly([(tx - 5.5, ty), (tx, ty), (tx, ty + 5.5)], r=L(S, 0, 1)))]


@icon("male-symbol", CAT, "Male symbol: a circle with an arrow pointing out from its upper right.",
      tags=["male", "man", "mars", "gender", "masculine", "boy"])
def _(S):
    return [shell(circle(9.5, 14.5, 6)), *_male_arrow(S, (20, 4), (13.3, 10.7))]


@icon("female-symbol", CAT, "Female symbol: a circle with a small cross extending straight down from its bottom.",
      tags=["female", "woman", "venus", "gender", "feminine", "girl"])
def _(S):
    return [shell(circle(12, 9, 6)), lead(S, 12, 15, 12, 22), line(seg(8.5, 18.5, 15.5, 18.5))]


@icon("transgender-symbol", CAT, "Transgender symbol: a circle with an arrow at the upper right, a cross below and a crossed stroke at the upper left.",
      tags=["transgender", "trans", "gender identity", "pride", "gender", "lgbtq"])
def _(S):
    return [shell(circle(12, 11.5, 4.5)), *_male_arrow(S, (20, 3.5), (15.2, 8.3)),
            line(seg(8.8, 8.3, 4.5, 4)), line(seg(3.5, 7.5, 7.5, 3.5)),
            lead(S, 12, 16, 12, 22), line(seg(9, 19.25, 15, 19.25))]


@icon("nonbinary-symbol", CAT, "Nonbinary symbol: a circle with a vertical stroke above it crossed by a small X.",
      tags=["nonbinary", "non-binary", "enby", "gender identity", "gender", "lgbtq"])
def _(S):
    return [shell(circle(12, 17, 4.5)), line(seg(12, 2.5, 12, 12.5)),
            line(seg(9.25, 4.25, 14.75, 9.75)), line(seg(9.25, 9.75, 14.75, 4.25))]


@icon("genderless-symbol", CAT, "Genderless symbol: a plain circle with a short straight line rising from its top.",
      tags=["genderless", "agender", "neutral", "gender", "no gender", "symbol"])
def _(S):
    return [shell(circle(12, 14.5, 6)), lead(S, 12, 8.5, 12, 2)]


@icon("intersex-symbol", CAT, "Intersex symbol: a circle with an arrow at the upper right and a short cross at the bottom.",
      tags=["intersex", "gender", "mars venus", "combined gender", "lgbtq", "symbol"])
def _(S):
    return [shell(circle(11, 11.5, 4.75)), *_male_arrow(S, (20, 3.5), (14.4, 8.1)),
            lead(S, 11, 16.25, 11, 22), line(seg(8, 19.5, 14, 19.5))]


# ============================================================================ flowchart shapes

@icon("flowchart-terminator", CAT, "Flowchart terminator: a wide stadium shape with fully rounded ends.",
      tags=["terminator", "start", "end", "flowchart", "process diagram", "stadium"])
def _(S):
    return [shell(rect(2, 6.5, 20, 11, L(S, 3.5, 5.5)))]


def _wave_bottom_doc(S, x0, x1, top, yb, amp, k):
    """Rectangle with a single wave along its bottom edge (path string)."""
    mid = (x0 + x1) / 2
    w = (x1 - x0) / 4
    return (f"M{fmt(x0 + k)} {fmt(top)}H{fmt(x1 - k)}" + (f"Q{fmt(x1)} {fmt(top)} {fmt(x1)} {fmt(top + k)}" if k else "")
            + f"V{fmt(yb)}C{fmt(x1 - w)} {fmt(yb - amp)} {fmt(mid + w)} {fmt(yb - amp)} {fmt(mid)} {fmt(yb)}"
            f"S{fmt(x0 + w)} {fmt(yb + amp)} {fmt(x0)} {fmt(yb)}V{fmt(top + k)}"
            + (f"Q{fmt(x0)} {fmt(top)} {fmt(x0 + k)} {fmt(top)}" if k else "") + "Z")


@icon("flowchart-document", CAT, "Flowchart document shape: a rectangle whose bottom edge is a single wave.",
      tags=["document", "flowchart", "report", "output", "process diagram", "wavy bottom"])
def _(S):
    return [shell(_wave_bottom_doc(S, 3, 21, 3.5, 17, 2.5, L(S, 0, 2)))]


@icon("flowchart-multiple-documents", CAT, "Flowchart multiple documents: a wavy bottomed page with two more pages stacked behind it.",
      tags=["multiple documents", "flowchart", "documents", "reports", "stack", "process diagram"])
def _(S):
    k = L(S, 0, 1.5)
    return [shell(_wave_bottom_doc(S, 2.5, 14.5, 10, 20, 1.75, k)),
            line(poly([(6, 10), (6, 6.5), (18, 6.5), (18, 15.5)], r=L(S, 0, 1.5))),
            line(poly([(9.5, 6.5), (9.5, 3), (21.5, 3), (21.5, 12)], r=L(S, 0, 1.5)))]


@icon("flowchart-predefined-process", CAT, "Flowchart predefined process: a rectangle with an extra vertical line inside each end.",
      tags=["predefined process", "subroutine", "flowchart", "function call", "process diagram", "module"])
def _(S):
    return [shell(rect(2.5, 5, 19, 14, S.R)), detail(seg(7, 5, 7, 19)), detail(seg(17, 5, 17, 19))]


@icon("flowchart-manual-input", CAT, "Flowchart manual input: a four sided shape whose top edge slopes up to the right.",
      tags=["manual input", "keyboard input", "flowchart", "user input", "process diagram", "data entry"])
def _(S):
    return [shell(poly([(2.5, 9.5), (21.5, 4.5), (21.5, 19.5), (2.5, 19.5)], closed=True, r=S.r))]


@icon("flowchart-off-page-connector", CAT, "Flowchart off page connector: a pentagon shaped like a home plate pointing down.",
      tags=["off page connector", "connector", "flowchart", "continue", "process diagram", "pentagon"])
def _(S):
    return [shell(poly([(4.5, 3.5), (19.5, 3.5), (19.5, 13.5), (12, 20.5), (4.5, 13.5)], closed=True, r=S.r))]


@icon("flowchart-delay", CAT, "Flowchart delay: a D shape with a flat left side and a rounded right side.",
      tags=["delay", "wait", "flowchart", "pause", "process diagram", "d shape"])
def _(S):
    if S.name == "line":
        d = "M3 5H14A7 7 0 0 1 14 19H3Z"
    else:
        d = "M5 5H14A7 7 0 0 1 14 19H5Q3 19 3 17V7Q3 5 5 5Z"
    return [shell(d)]


@icon("flowchart-display", CAT, "Flowchart display: a shape with a pointed left end and a rounded right end.",
      tags=["display", "screen output", "flowchart", "monitor", "process diagram", "output"])
def _(S):
    if S.name == "line":
        d = "M2.5 12L7 5H15A7 7 0 0 1 15 19H7Z"
    else:
        d = "M3.4 10.6L6.6 5.8Q7.2 5 8.2 5H15A7 7 0 0 1 15 19H8.2Q7.2 19 6.6 18.2L3.4 13.4Q2.4 12 3.4 10.6Z"
    return [shell(d)]


@icon("flowchart-punched-tape", CAT, "Flowchart punched tape: a flag shaped rectangle with wavy top and bottom edges.",
      tags=["punched tape", "paper tape", "flowchart", "flag", "process diagram", "wavy"])
def _(S):
    k = L(S, 0, 1.2)
    return [shell(f"M{fmt(3 + k)} 6.5C7 3.5 10 3.5 12 6.5S17 9.5 {fmt(21 - k)} 6.5" + (f"Q21 6.5 21 {fmt(6.5 + k)}" if k else "")
                  + f"V{fmt(17.5 - k)}" + (f"Q21 17.5 {fmt(21 - k)} 17.5" if k else "")
                  + f"C17 20.5 14 20.5 12 17.5S7 14.5 {fmt(3 + k)} 17.5" + (f"Q3 17.5 3 {fmt(17.5 - k)}" if k else "")
                  + f"V{fmt(6.5 + k)}" + (f"Q3 6.5 {fmt(3 + k)} 6.5" if k else "") + "Z")]


@icon("flowchart-decision-branch", CAT, "Flowchart decision: a diamond with one arrow leaving the bottom and another leaving the side.",
      tags=["decision", "branch", "yes no", "flowchart", "conditional", "process diagram"])
def _(S):
    return [shell(poly([(9, 2.5), (15.5, 9), (9, 15.5), (2.5, 9)], closed=True, r=S.r)),
            *arrow(S, (9, 15.5), (9, 22), 4, 2), *arrow(S, (15.5, 9), (22, 9), 4, 2)]


# ============================================================================ UML and diagram notation

@icon("uml-class-diagram", CAT, "UML class box: a rectangle split into three stacked compartments for name, fields and methods.",
      tags=["uml", "class diagram", "class box", "object oriented", "software design", "modeling"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15))]


@icon("uml-inheritance", CAT, "UML inheritance: two boxes joined by a line that ends in a hollow triangle at the upper box.",
      tags=["uml", "inheritance", "generalization", "extends", "class diagram", "subclass"])
def _(S):
    return [shell(rect(5, 3, 14, 4, rr(S, 1.5))), shell(rect(5, 17, 14, 4, rr(S, 1.5))),
            shell(poly([(12, 7.5), (8.5, 13.25), (15.5, 13.25)], closed=True, r=S.r * 0.5)),
            line(seg(12, 13, 12, 17))]


@icon("uml-composition", CAT, "UML composition: two boxes joined by a line that ends in a filled diamond at the upper box.",
      tags=["uml", "composition", "part of", "class diagram", "strong ownership", "diamond"])
def _(S):
    return [shell(rect(5, 3, 14, 4, rr(S, 1.5))), shell(rect(5, 17, 14, 4, rr(S, 1.5))),
            solid(poly([(12, 7), (15.5, 11), (12, 15), (8.5, 11)], closed=True, r=L(S, 0, 0.6))),
            line(seg(12, 14.5, 12, 17))]


@icon("uml-aggregation", CAT, "UML aggregation: two boxes joined by a line that ends in a hollow diamond at the upper box.",
      tags=["uml", "aggregation", "has a", "class diagram", "shared ownership", "diamond"])
def _(S):
    return [shell(rect(5, 3, 14, 4, rr(S, 1.5))), shell(rect(5, 17, 14, 4, rr(S, 1.5))),
            line(poly([(12, 7.5), (16, 11.25), (12, 15), (8, 11.25)], closed=True, r=L(S, 0, 0.6))),
            line(seg(12, 15, 12, 17))]


@icon("uml-use-case", CAT, "UML use case: a horizontal ellipse with a short line of text inside, linked to a stick figure.",
      tags=["uml", "use case", "actor", "requirements", "use case diagram", "software design"])
def _(S):
    return [shell(ellipse(16.5, 12, 5.5, 4.5)),
            dot(5, 5, 2), line(seg(5, 7.5, 5, 14)), line(seg(2.5, 10.5, 11.3, 10.5)),
            line(seg(5, 14, 2.5, 20.5)), line(seg(5, 14, 7.5, 20.5))]


@icon("uml-sequence-diagram", CAT, "UML sequence diagram: two boxes with lifelines down and message arrows between them.",
      tags=["uml", "sequence diagram", "messages", "lifeline", "interaction", "software design"])
def _(S):
    return [shell(rect(2.5, 3, 7, 4, rr(S, 1.5))), shell(rect(14.5, 3, 7, 4, rr(S, 1.5))),
            line(seg(6, 7, 6, 22)), line(seg(18, 7, 18, 22)),
            *arrow(S, (6, 12.5), (17, 12.5), 3.5, 1.75), *arrow(S, (18, 18.5), (7, 18.5), 3.5, 1.75)]


@icon("crows-foot-notation", CAT, "Crow's foot notation: a line between two boxes ending in a three pronged fork with a small bar.",
      tags=["crows foot", "entity relationship", "erd", "one to many", "database design", "cardinality"])
def _(S):
    return [shell(rect(4, 3, 16, 4, rr(S, 1.5))), shell(rect(4, 17, 16, 4, rr(S, 1.5))),
            line(seg(12, 7, 12, 13.5)), line(seg(8.5, 10, 15.5, 10)),
            line(seg(12, 13.5, 6.5, 17)), line(seg(12, 13.5, 12, 17)), line(seg(12, 13.5, 17.5, 17))]


@icon("bpmn-gateway", CAT, "Process gateway: a diamond with a bold X inside, joined to an incoming and an outgoing arrow.",
      tags=["bpmn", "gateway", "exclusive gateway", "process", "workflow", "decision"])
def _(S):
    return [shell(poly([(12, 5), (19, 12), (12, 19), (5, 12)], closed=True, r=S.r)),
            detail(seg(9.75, 9.75, 14.25, 14.25)), detail(seg(9.75, 14.25, 14.25, 9.75)),
            *arrow(S, (1.5, 12), (5.7, 12), 3, 1.75), *arrow(S, (18.3, 12), (22, 12), 3, 1.75)]


@icon("uml-state-diagram", CAT, "UML state diagram: a solid start dot, a rounded state box and a bullseye end state joined by arrows.",
      tags=["uml", "state diagram", "state machine", "initial state", "final state", "transition"])
def _(S):
    return [dot(5, 4, 1.75), *arrow(S, (5, 5.6), (5, 11), 3.5, 1.75),
            shell(rect(3, 12, 7, 8, rr(S, 3))),
            *arrow(S, (11, 16), (15.5, 16), 3.5, 1.75),
            shell(circle(19, 16, 2.25)), dot(19, 16, 0.75)]


# ============================================================================ zodiac glyphs

def _mirror(d_pts):
    return [(24 - x, y) for x, y in d_pts]


def _m_arches(x0=3.0, step=5.5, top=8.0, bottom=18.0, r=2.75):
    """The 'm' used by Virgo and Scorpio: a stem and two arches; returns the parts and the last leg x."""
    a = f"M{fmt(x0)} {fmt(bottom)}V{fmt(top)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + step)} {fmt(top)}V{fmt(bottom)}"
    b = f"M{fmt(x0 + step)} {fmt(top)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + 2 * step)} {fmt(top)}"
    return a, b


@icon("aries", CAT, "Aries glyph: two curled horns springing outward from a single central stem.",
      tags=["aries", "zodiac", "ram", "astrology", "horoscope", "fire sign"])
def _(S):
    return [line("M12 10.5C12 5.5 9.75 3.5 7.5 3.5C4.75 3.5 3 5.75 3 9"),
            line("M12 10.5C12 5.5 14.25 3.5 16.5 3.5C19.25 3.5 21 5.75 21 9"),
            line(seg(12, 10.5, 12, 21))]


@icon("taurus", CAT, "Taurus glyph: a circle with a wide crescent of horns resting on top of it.",
      tags=["taurus", "zodiac", "bull", "astrology", "horoscope", "earth sign"])
def _(S):
    return [shell(circle(12, 16, 5)), line("M4.5 3.5A7.7 7.7 0 0 0 19.5 3.5")]


@icon("gemini", CAT, "Gemini glyph: two vertical pillars joined by curved bars at the top and bottom, like a Roman numeral two.",
      tags=["gemini", "zodiac", "twins", "astrology", "horoscope", "air sign"])
def _(S):
    return [line("M3.5 3.5Q12 8 20.5 3.5"), line("M3.5 20.5Q12 16 20.5 20.5"),
            line(seg(8.5, 5, 8.5, 19)), line(seg(15.5, 5, 15.5, 19))]


@icon("cancer-zodiac", CAT, "Cancer glyph: two small circles with curling tails, one at the upper left and one at the lower right.",
      tags=["cancer", "zodiac", "crab", "astrology", "horoscope", "water sign", "69"])
def _(S):
    return [shell(circle(6.5, 9.5, 2.5)), line("M8.3 7.7C12 4 18 4 21 9"),
            shell(circle(17.5, 14.5, 2.5)), line("M15.7 16.3C12 20 6 20 3 15")]


@icon("leo", CAT, "Leo glyph: a small circle at the lower left joined to a looping stroke that ends in a curled tail.",
      tags=["leo", "zodiac", "lion", "astrology", "horoscope", "fire sign"])
def _(S):
    return [shell(circle(6.5, 15.5, 3.25)),
            line("M8.75 13.2C8.75 7 10.5 3.5 14.5 3.5S19.5 7 19.5 11C19.5 16 16 17 16 20S20 22 21 19.5")]


@icon("virgo", CAT, "Virgo glyph: an m shape whose last leg loops back across itself at the bottom.",
      tags=["virgo", "zodiac", "maiden", "astrology", "horoscope", "earth sign"])
def _(S):
    a, b = _m_arches(3, 5.5, 8, 18, 2.75)
    return [line(a), line(b + "V16C14 19.5 17 21 19.5 20C22 19 21.5 15.5 18 14.5C16 14 13.5 14.8 11.5 16.5")]


@icon("libra", CAT, "Libra glyph: a horizontal bar beneath a rounded hump that rises in the middle, like a sun on the horizon.",
      tags=["libra", "zodiac", "scales", "astrology", "horoscope", "air sign"])
def _(S):
    return [line("M3 15H8.3A4 4 0 1 1 15.7 15H21"), line(seg(3, 20, 21, 20))]


@icon("scorpio-zodiac", CAT, "Scorpio glyph: an m shape whose last leg ends in an upward pointing arrowhead tail.",
      tags=["scorpio", "zodiac", "scorpion", "astrology", "horoscope", "water sign"])
def _(S):
    a, b = _m_arches(3, 5.5, 8, 18, 2.75)
    return [line(a), line(b + "V15C14 19 19.5 19 19.5 13.5"),
            line(poly([(17.25, 15.25), (19.5, 12.5), (21.75, 15.25)], r=L(S, 0, 0.8)))]


@icon("sagittarius", CAT, "Sagittarius glyph: a diagonal arrow pointing to the upper right with a short crossbar on its shaft.",
      tags=["sagittarius", "zodiac", "archer", "astrology", "horoscope", "fire sign"])
def _(S):
    return [line(seg(4, 20, 19.6, 4.4)), line(poly([(11.5, 4), (20, 4), (20, 12.5)], r=L(S, 0, 1))),
            line(seg(5.5, 13.5, 10.5, 18.5))]


@icon("capricorn", CAT, "Capricorn glyph: a V shaped stroke flowing into a looped fish tail at the right.",
      tags=["capricorn", "zodiac", "goat", "astrology", "horoscope", "earth sign"])
def _(S):
    return [line(poly([(3, 4.5), (9, 17), (12.5, 7)], r=L(S, 0, 0.8))),
            line("M12.5 7C13.5 4.25 16.5 4.25 17 7.5L17.25 12.5"),
            shell(circle(17.25, 16.75, 4)) if False else line(circle(17.25, 16.75, 4))]


@icon("aquarius", CAT, "Aquarius glyph: two parallel zigzag lines stacked one above the other, like waves of water.",
      tags=["aquarius", "zodiac", "water bearer", "astrology", "horoscope", "air sign"])
def _(S):
    up = [(2.5, 9.5), (7.25, 5.5), (12, 9.5), (16.75, 5.5), (21.5, 9.5)]
    return [line(poly(up, r=L(S, 0, 0.4))), line(poly([(x, y + 8) for x, y in up], r=L(S, 0, 0.4)))]


@icon("pisces", CAT, "Pisces glyph: two outward curving arcs joined by a horizontal bar through their middle.",
      tags=["pisces", "zodiac", "fish", "astrology", "horoscope", "water sign"])
def _(S):
    return [line("M9 3.5A11 11 0 0 0 9 20.5"), line("M15 3.5A11 11 0 0 1 15 20.5"), line(seg(3.5, 12, 20.5, 12))]


@icon("ophiuchus", CAT, "Ophiuchus glyph: a wavy serpent line held above a straight horizontal bar.",
      tags=["ophiuchus", "zodiac", "serpent bearer", "astrology", "horoscope", "thirteenth sign"])
def _(S):
    return [line("M3 10q2.25-5 4.5 0t4.5 0 4.5 0 4.5 0", stroke_miterlimit="1"), line(seg(3, 18, 21, 18))]


@icon("zodiac-wheel", CAT, "Zodiac wheel: a circle divided into twelve equal segments around an inner ring.",
      tags=["zodiac wheel", "astrology", "horoscope", "twelve signs", "birth chart", "houses"])
def _(S):
    r0, r1 = L(S, 5, 5.75), L(S, 9, 8.25)
    spokes = [detail(seg(*polar(12, 12, r0, a), *polar(12, 12, r1, a))) for a in range(0, 360, 30)]
    return [shell(circle(12, 12, 9)), detail(circle(12, 12, L(S, 5, 4.5))), *spokes]


# ============================================================================ electrical markings (added)

@icon("double-insulation-symbol", CAT, "Double insulation symbol: a small square centred inside a larger square.",
      tags=["double insulation", "class ii", "appliance safety", "electrical safety", "marking", "square in square"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(rect(8, 8, 8, 8, L(S, 0, 1.5)))]


@icon("dc-polarity-symbol", CAT, "Center positive polarity symbol: a dot inside a C shape, with a plus and a minus on the open side.",
      tags=["polarity", "center positive", "dc plug", "power adapter", "barrel connector", "plus minus"])
def _(S):
    a = math.radians(50)
    cx, cy, r = 8.5, 12, 5.75
    sx, sy = cx + r * math.cos(a), cy - r * math.sin(a)
    ex, ey = cx + r * math.cos(a), cy + r * math.sin(a)
    return [line(f"M{fmt(sx)} {fmt(sy)}A{fmt(r)} {fmt(r)} 0 1 0 {fmt(ex)} {fmt(ey)}"), dot(cx, cy, 2),
            *plus(18.5, 7, 2.25, line), *minus(18.5, 17, 2.25, line)]
