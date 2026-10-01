"""TypeIcon Core: electronics (batch 001): schematic symbols, signals and board-level components.

Schematic symbols follow the usual textbook forms, drawn on a horizontal signal line where possible with
leads ending at the live-area edge. Physical parts are drawn front or side on with their legs pointing down.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "electronics"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    """Container corner radius for the style, optionally capped for small shapes."""
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell (like a dot)."""
    return Part("dot", rect(x, y, w, h, rx))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def lead(S, x1, y1, x2, y2):
    """Open stroke whose free end (x2, y2) stays inside the live area in both cap styles."""
    k = L(S, 0, 1)
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    return line(seg(x1, y1, x2 - dx / n * k, y2 - dy / n * k))


def rot_pts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def head_pts(tip, frm, length=3.5, hw=2.0):
    """Arrowhead triangle with its point at tip, aimed away from frm."""
    dx, dy = tip[0] - frm[0], tip[1] - frm[1]
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    bx, by = tip[0] - ux * length, tip[1] - uy * length
    return [tip, (bx - uy * hw, by + ux * hw), (bx + uy * hw, by - ux * hw)]


def head(S, tip, frm, length=3.5, hw=2.0, kind="solid"):
    d = poly(head_pts(tip, frm, length, hw), closed=True, r=L(S, 0, 0.6))
    return Part(kind, d)


def arrow(S, a, b, length=3.5, hw=2.0, kind="solid"):
    """Straight arrow from a to the point b: shaft (as a line) plus a solid head."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    e = (b[0] - dx / n * (length - 0.5), b[1] - dy / n * (length - 0.5))
    shaft = line(seg(a[0], a[1], e[0], e[1])) if kind == "solid" else detail(seg(a[0], a[1], e[0], e[1]))
    return [shaft, head(S, b, a, length, hw, kind)]


def tri(S, base_x, tip_x, cy, h):
    """Diode triangle pointing along x from base_x to a vertex at tip_x (outline shell)."""
    return shell(poly([(base_x, cy - h), (tip_x, cy), (base_x, cy + h)], closed=True, r=S.r * 0.5))


def zigzag(x0, x1, cy, amp, n):
    """Resistor zigzag from x0 to x1 with n peaks (half steps at both ends)."""
    s = (x1 - x0) / n
    pts = [(x0, cy)]
    for i in range(n):
        pts.append((x0 + s * (i + 0.5), cy - amp if i % 2 == 0 else cy + amp))
    pts.append((x1, cy))
    return pts


def humps_h(x0, y, r, n, up=True, ry=None):
    """Path segment of n (semi-elliptical) humps along a horizontal line starting at (x0, y)."""
    out = ""
    ry = r if ry is None else ry
    for i in range(n):
        out += f"A{fmt(r)} {fmt(ry)} 0 0 {1 if up else 0} {fmt(x0 + 2 * r * (i + 1))} {fmt(y)}"
    return out


def humps_v(x, y0, r, n, right=True):
    out = ""
    for i in range(n):
        out += f"A{fmt(r)} {fmt(r)} 0 0 {1 if right else 0} {fmt(x)} {fmt(y0 + 2 * r * (i + 1))}"
    return out


# ============================================================================ passive symbols

@icon("resistor-symbol", CAT, "Resistor schematic symbol: a zigzag line with a lead on each end.",
      tags=["resistor", "resistance", "schematic", "circuit symbol", "ohm", "electronics"])
def _(S):
    return [line(poly([(L(S, 2, 3), 12)] + zigzag(5, 19, 12, 4, 4) + [(L(S, 22, 21), 12)], r=L(S, 0, 0.3)))]


@icon("potentiometer-symbol", CAT, "Potentiometer schematic symbol: a zigzag resistor with an arrow wiper pointing at its middle.",
      tags=["potentiometer", "variable resistor", "wiper", "schematic", "pot", "circuit symbol"])
def _(S):
    return [line(poly([(L(S, 2, 3), 15)] + zigzag(5, 19, 15, 3.5, 4) + [(L(S, 22, 21), 15)], r=L(S, 0, 0.3))),
            lead(S, 12, 7, 12, 2), head(S, (12, 9.5), (12, 2), 3.5, 2.5)]


@icon("capacitor-symbol", CAT, "Capacitor schematic symbol: two parallel plates with a lead on each side.",
      tags=["capacitor", "capacitance", "schematic", "circuit symbol", "farad", "electronics"])
def _(S):
    return [lead(S, 9.5, 12, 2, 12), lead(S, 14.5, 12, 22, 12),
            line(seg(9.5, 5, 9.5, 19)), line(seg(14.5, 5, 14.5, 19))]


@icon("variable-capacitor-symbol", CAT, "Variable capacitor schematic symbol: two plates with a diagonal arrow through them.",
      tags=["variable capacitor", "tuning capacitor", "trimmer", "schematic", "circuit symbol", "adjustable"])
def _(S):
    return [lead(S, 9.5, 12, 2, 12), lead(S, 14.5, 12, 22, 12),
            line(seg(9.5, 6, 9.5, 18)), line(seg(14.5, 6, 14.5, 18)),
            *arrow(S, (L(S, 5, 5.7), L(S, 21, 20.3)), (19.5, 3), 4, 2.25)]


@icon("inductor-symbol", CAT, "Inductor schematic symbol: a row of four coil humps with a lead on each end.",
      tags=["inductor", "coil", "choke", "inductance", "schematic", "henry"])
def _(S):
    return [line(f"M{L(S, 2, 3)} 14.5H4" + humps_h(4, 14.5, 2, 4, ry=3.5) + f"H{L(S, 22, 21)}", stroke_miterlimit="1")]


@icon("iron-core-inductor-symbol", CAT, "Iron core inductor symbol: coil humps with two straight core lines above them.",
      tags=["iron core", "inductor", "choke", "coil", "schematic", "ferromagnetic"])
def _(S):
    return [line(f"M{L(S, 2, 3)} 17H4" + humps_h(4, 17, 2, 4) + f"H{L(S, 22, 21)}", stroke_miterlimit="1"),
            line(seg(L(S, 4, 5), 7, L(S, 20, 19), 7)), line(seg(L(S, 4, 5), 11, L(S, 20, 19), 11))]


@icon("transformer-symbol", CAT, "Transformer schematic symbol: two facing coils with two core lines between them.",
      tags=["transformer", "coils", "windings", "schematic", "step down", "isolation"])
def _(S):
    a, b = L(S, 2, 3), L(S, 22, 21)
    left = f"M{a} 4H4.5" + humps_v(4.5, 4, 2, 4, True) + f"H{a}"
    right = f"M{b} 4H19.5" + humps_v(19.5, 4, 2, 4, False) + f"H{b}"
    return [line(left, stroke_miterlimit="1"), line(right, stroke_miterlimit="1"),
            line(seg(10, 4, 10, 20)), line(seg(14, 4, 14, 20))]


# ============================================================================ diodes

@icon("diode-symbol", CAT, "Diode schematic symbol: a triangle pointing at a bar on a signal line.",
      tags=["diode", "rectifier", "semiconductor", "schematic", "anode", "cathode"])
def _(S):
    return [tri(S, 7, 14, 12, 6), line(seg(15, 6, 15, 18)),
            lead(S, 7, 12, 2, 12), lead(S, 15, 12, 22, 12)]


@icon("led-symbol", CAT, "LED schematic symbol: a diode with two small arrows pointing away from it.",
      tags=["led", "light emitting diode", "diode", "schematic", "indicator", "light"])
def _(S):
    return [tri(S, 5, 12, 15, 5), line(seg(13, 10, 13, 20)),
            lead(S, 5, 15, 2, 15), lead(S, 13, 15, 22, 15),
            *arrow(S, (8.5, 8), (13.5, 3), 3, 1.75), *arrow(S, (14, 9.5), (19, 4.5), 3, 1.75)]


@icon("schottky-diode-symbol", CAT, "Schottky diode symbol: a diode triangle pointing at a bar with small hooked ends.",
      tags=["schottky", "diode", "fast diode", "schematic", "semiconductor", "low drop"])
def _(S):
    bar = poly([(17.5, 7.5), (17.5, 5), (15, 5), (15, 19), (12.5, 19), (12.5, 16.5)], r=S.r * 0.5)
    return [tri(S, 6, 14, 12, 5), line(bar),
            lead(S, 6, 12, 2, 12), lead(S, 15, 12, 22, 12)]


@icon("tunnel-diode-symbol", CAT, "Tunnel diode symbol: a diode triangle pointing at a bar with flags that form a bracket.",
      tags=["tunnel diode", "esaki diode", "diode", "schematic", "semiconductor", "negative resistance"])
def _(S):
    bar = poly([(11.5, 5), (15, 5), (15, 19), (11.5, 19)], r=S.r * 0.5)
    return [tri(S, 5, 14, 12, 5.5), line(bar),
            lead(S, 5, 12, 2, 12), lead(S, 15, 12, 22, 12)]


@icon("varactor-diode-symbol", CAT, "Varactor diode symbol: a diode triangle and bar followed by a capacitor plate.",
      tags=["varactor", "varicap", "tuning diode", "diode", "schematic", "capacitance"])
def _(S):
    return [tri(S, 4.5, 11.5, 12, 5.5), line(seg(12.5, 6.5, 12.5, 17.5)), line(seg(16.5, 6.5, 16.5, 17.5)),
            lead(S, 4.5, 12, 2, 12), lead(S, 16.5, 12, 22, 12)]


@icon("tvs-diode-symbol", CAT, "Bidirectional TVS diode symbol: two triangles pointing at one bar with bent tips.",
      tags=["tvs diode", "transient voltage suppressor", "surge protection", "esd", "schematic", "diode"])
def _(S):
    bar = poly([(10, 4), (12, 5.5), (12, 18.5), (14, 20)], r=S.r * 0.5)
    return [tri(S, 4.5, 11, 12, 4.5), tri(S, 19.5, 13, 12, 4.5), line(bar),
            lead(S, 4.5, 12, 2, 12), lead(S, 19.5, 12, 22, 12)]


# ============================================================================ transistors

def _bjt(S, pnp=False, base=True, cx=12.0, cy=12.0, R=9.0, bx=9.0):
    """Bipolar transistor in a circle: base bar, collector and emitter legs, arrow on the emitter."""
    top = cy - math.sqrt(R * R - 9)  # circle at x = cx + 3
    bot = cy + math.sqrt(R * R - 9)
    ex = cx + 3
    parts = [shell(circle(cx, cy, R)), detail(seg(bx, cy - 5, bx, cy + 5)),
             detail(poly([(bx, cy - 2), (ex, cy - 5.5), (ex, top)], r=S.r * 0.6)),
             detail(poly([(bx, cy + 2), (ex, cy + 5.5), (ex, bot)], r=S.r * 0.6))]
    if base:
        parts.append(detail(seg(cx - R, cy, bx, cy)))
    a, b = (bx, cy + 2), (ex, cy + 5.5)
    if pnp:
        t = 0.12
        tip = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        parts.append(head(S, tip, b, 4.5, 2.6, "dot"))
    else:
        t = 1.0
        tip = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        parts.append(head(S, tip, a, 4.5, 2.6, "dot"))
    return parts


@icon("npn-transistor-symbol", CAT, "NPN transistor symbol: base bar, collector and emitter in a circle, arrow pointing out.",
      tags=["npn", "transistor", "bjt", "bipolar", "schematic", "amplifier"])
def _(S):
    return _bjt(S)


@icon("pnp-transistor-symbol", CAT, "PNP transistor symbol: base bar, collector and emitter in a circle, arrow pointing in.",
      tags=["pnp", "transistor", "bjt", "bipolar", "schematic", "amplifier"])
def _(S):
    return _bjt(S, pnp=True)


@icon("mosfet-symbol", CAT, "MOSFET symbol: a gate plate beside a broken channel with drain, source and a body arrow.",
      tags=["mosfet", "field effect transistor", "fet", "transistor", "schematic", "power switch"])
def _(S):
    e = L(S, 0, 1)
    return [line(poly([(L(S, 2, 3), 17.5), (6.5, 17.5), (6.5, 6.5)], r=S.r * 0.5)),
            line(seg(10.5, 4.5, 10.5, 8)), line(seg(10.5, 10.25, 10.5, 13.75)), line(seg(10.5, 16, 10.5, 19.5)),
            line(poly([(10.5, 6.25), (17, 6.25), (17, 2 + e)], r=S.r * 0.5)),
            line(poly([(10.5, 17.75), (17, 17.75), (17, 22 - e)], r=S.r * 0.5)),
            line(poly([(14, 12), (17, 12), (17, 17.75)], r=S.r * 0.5)),
            head(S, (11.8, 12), (17, 12), 3.6, 2.3)]


@icon("jfet-symbol", CAT, "JFET symbol: a channel bar with drain and source leads and a gate arrow meeting it, in a circle.",
      tags=["jfet", "junction fet", "field effect transistor", "transistor", "schematic", "n channel"])
def _(S):
    top, bot = 12 - math.sqrt(81 - 16), 12 + math.sqrt(81 - 16)
    gl = 12 - math.sqrt(81 - 3.5 ** 2)
    return [shell(circle(12, 12, 9)),
            detail(seg(11, 6, 11, 18)),
            detail(poly([(11, 8), (16, 8), (16, top)], r=S.r * 0.5)),
            detail(poly([(11, 16), (16, 16), (16, bot)], r=S.r * 0.5)),
            detail(seg(gl, 15.5, 7, 15.5)),
            head(S, (10.2, 15.5), (5, 15.5), 3.5, 2.2, "dot")]


@icon("igbt-symbol", CAT, "IGBT symbol: an insulated gate plate beside a transistor bar with an arrow on the emitter.",
      tags=["igbt", "insulated gate", "bipolar transistor", "power electronics", "schematic", "inverter"])
def _(S):
    top, bot = 12 - math.sqrt(81 - 3.5 ** 2), 12 + math.sqrt(81 - 3.5 ** 2)
    gl = 12 - math.sqrt(81 - 16)
    a, b = (10, 14), (15.5, 17.5)
    return [shell(circle(12, 12, 9)),
            detail(poly([(gl, 16), (6, 16), (6, 8)], r=S.r * 0.5)),
            detail(seg(10, 7, 10, 17)),
            detail(poly([(10, 10), (15.5, 6.5), (15.5, top)], r=S.r * 0.5)),
            detail(poly([a, b, (15.5, bot)], r=S.r * 0.5)),
            head(S, b, a, 4.2, 2.4, "dot")]


# ============================================================================ thyristors and light sensitive parts

@icon("thyristor-symbol", CAT, "Thyristor (SCR) symbol: a diode triangle and bar with a gate lead angled off the bar.",
      tags=["thyristor", "scr", "silicon controlled rectifier", "gate", "schematic", "power control"])
def _(S):
    return [tri(S, 6, 13, 11, 5.5), line(seg(14, 5.5, 14, 16.5)),
            lead(S, 6, 11, 2, 11), lead(S, 14, 11, 22, 11),
            lead(S, 14, 16, 19.5, 21.5)]


def _triac(S, gate):
    parts = [line(seg(4.5, 7, 19.5, 7)), line(seg(4.5, 17, 19.5, 17)),
             line(poly([(5, 7), (8.25, 16.6), (11.5, 7)], r=S.r * 0.3), stroke_miterlimit="1.5"),
             line(poly([(12.5, 17), (15.75, 7.4), (19, 17)], r=S.r * 0.3), stroke_miterlimit="1.5"),
             lead(S, 12, 7, 12, 2), lead(S, 12, 17, 12, 22)]
    if gate:
        parts.append(lead(S, 16.5, 17, 21, 21.5))
    return parts


@icon("triac-symbol", CAT, "Triac symbol: two opposing diode triangles between two bars, with a gate lead.",
      tags=["triac", "ac switch", "thyristor", "dimmer", "schematic", "gate"])
def _(S):
    return _triac(S, True)


@icon("diac-symbol", CAT, "Diac symbol: two opposing diode triangles between two bars, without a gate.",
      tags=["diac", "trigger diode", "bidirectional", "dimmer", "schematic", "breakover"])
def _(S):
    return _triac(S, False)


@icon("phototransistor-symbol", CAT, "Phototransistor symbol: a transistor in a circle with two light arrows pointing at its base.",
      tags=["phototransistor", "light sensor", "optical", "transistor", "schematic", "photo"])
def _(S):
    c, R = (14.0, 14.0), 7.5
    top = c[1] - math.sqrt(R * R - 6.25)
    bot = c[1] + math.sqrt(R * R - 6.25)
    parts = [shell(circle(c[0], c[1], R)), detail(seg(11.5, 10, 11.5, 18)),
             detail(poly([(11.5, 12), (16.5, 9), (16.5, top)], r=S.r * 0.5)),
             detail(poly([(11.5, 16), (16.5, 19), (16.5, bot)], r=S.r * 0.5)),
             head(S, (16.6, 19.1), (11.5, 16), 3.5, 2.1, "dot")]
    for th in (212, 252):
        tip = polar(c[0], c[1], 8.9, th)
        parts += arrow(S, (tip[0] - 4.2, tip[1] - 4.2), tip, 3, 1.75)
    return parts


@icon("optocoupler-symbol", CAT, "Optocoupler symbol: a box holding an LED and a phototransistor with light arrows between them.",
      tags=["optocoupler", "optoisolator", "isolation", "led", "phototransistor", "schematic"])
def _(S):
    return [shell(rect(2, 3, 20, 18, rr(S, 2.5))),
            detail(poly([(4.5, 9), (9.5, 9), (7, 13.5)], closed=True, r=S.r * 0.4)),
            detail(seg(4.5, 14.5, 9.5, 14.5)),
            detail(seg(7, 3, 7, 9)), detail(seg(7, 14.5, 7, 21)),
            *arrow(S, (10.5, 12), (14.5, 12), 2.8, 1.8, "detail"),
            detail(seg(16, 8, 16, 16)),
            detail(poly([(16, 10), (20, 7.5), (20, 3)], r=S.r * 0.5)),
            detail(poly([(16, 14), (20, 16.5), (20, 21)], r=S.r * 0.5))]


@icon("photoresistor-symbol", CAT, "Photoresistor (LDR) symbol: a resistor box in a circle with two light arrows pointing at it.",
      tags=["photoresistor", "ldr", "light dependent resistor", "light sensor", "photocell", "schematic"])
def _(S):
    c, R = (12.0, 15.0), 6.5
    parts = [shell(circle(c[0], c[1], R)), detail(rect(8.5, 13, 7, 4, L(S, 0, 0.5))),
             detail(seg(c[0] - R, 15, 8.5, 15)), detail(seg(15.5, 15, c[0] + R, 15)),
             lead(S, c[0] - R, 15, 2, 15), lead(S, c[0] + R, 15, 22, 15)]
    for th in (232, 282):
        tip = polar(c[0], c[1], R + 1.8, th)
        parts += arrow(S, (tip[0] - 3.8, tip[1] - 3.8), tip, 3, 1.75)
    return parts


@icon("varistor-symbol", CAT, "Varistor symbol: a resistor box crossed by a diagonal line with a flat tail.",
      tags=["varistor", "mov", "surge protector", "voltage dependent resistor", "schematic", "overvoltage"])
def _(S):
    t0, t1 = 4 / 14, 10 / 14
    p0, p1 = (7 + 10 * t0, 19 - 14 * t0), (7 + 10 * t1, 19 - 14 * t1)
    return [shell(rect(6, 9, 12, 6, rr(S, 1.5))), lead(S, 6, 12, 2, 12), lead(S, 18, 12, 22, 12),
            detail(seg(p0[0], p0[1], p1[0], p1[1])),
            line(poly([(L(S, 3, 4), 19), (7, 19), p0], r=S.r * 0.5)), line(seg(p1[0], p1[1], 17, 5))]


# ============================================================================ switches and relays

@icon("spdt-switch-symbol", CAT, "SPDT changeover switch symbol: a lever on a pivot touching one of two contacts.",
      tags=["spdt", "changeover switch", "toggle switch", "single pole double throw", "schematic", "selector"])
def _(S):
    return [lead(S, 5.5, 12, 2, 12), dot(5.5, 12, 2), line(seg(5.5, 12, 17, 6.9)),
            dot(18.5, 6.5, 1.9), dot(18.5, 17.5, 1.9),
            lead(S, 18.5, 6.5, 22, 6.5), lead(S, 18.5, 17.5, 22, 17.5)]


@icon("dpdt-switch-symbol", CAT, "DPDT switch symbol: two changeover switches whose levers are linked by a dashed line.",
      tags=["dpdt", "double pole double throw", "changeover", "reversing switch", "schematic", "ganged switch"])
def _(S):
    parts = []
    for y in (6.5, 17.5):
        parts += [lead(S, 5, y, 2, y), dot(5, y, 1.75), line(seg(5, y, 17.8, y - 2.75)),
                  dot(19.5, y - 3, 1.6), dot(19.5, y + 3, 1.6)]
    parts += [line(seg(12, 7.5, 12, 9.5)), line(seg(12, 11.5, 12, 13.5))]
    return parts


@icon("reed-switch-symbol", CAT, "Reed switch symbol: an open switch drawn inside a glass capsule outline.",
      tags=["reed switch", "magnetic switch", "schematic", "sensor", "door contact", "capsule"])
def _(S):
    return [shell(rect(4.5, 6, 15, 12, 6)),
            lead(S, 4.5, 14.5, 2, 14.5), lead(S, 19.5, 14.5, 22, 14.5),
            detail(poly([(4.8, 14.5), (8.5, 14.5), (13.8, 9.3)], r=S.r * 0.5)), detail(seg(15, 14.5, 19.2, 14.5))]


@icon("relay-coil-symbol", CAT, "Relay symbol: a coil box linked by a dashed line to a switch contact.",
      tags=["relay", "coil", "contactor", "switch", "schematic", "electromagnet"])
def _(S):
    return [shell(rect(3, 7, 6, 10, rr(S, 1.5))), lead(S, 6, 7, 6, 2), lead(S, 6, 17, 6, 22),
            lead(S, 19, 7.5, 19, 2), line(poly([(19, L(S, 22, 21)), (19, 16), (14.8, 7.6)], r=S.r * 0.5)),
            line(seg(11, 12, 13, 12)), line(seg(15, 12, 16.9, 12))]


@icon("circuit-breaker-symbol", CAT, "Circuit breaker symbol: a switch lever lifted off its contact with a hook arc over the gap.",
      tags=["circuit breaker", "breaker", "trip", "overcurrent", "schematic", "protection"])
def _(S):
    return [lead(S, 6, 16, 2, 16), line(seg(6, 16, 14.5, 9)), lead(S, 17, 16, 22, 16),
            dot(6, 16, 1.6), line(arc(17, 12, 3, 200, 360))]


# ============================================================================ transducers and meters

@icon("speaker-symbol", CAT, "Loudspeaker schematic symbol: a small box joined to a flared cone, with two leads.",
      tags=["speaker", "loudspeaker", "audio output", "schematic", "transducer", "sound"])
def _(S):
    body = poly([(7.5, 8), (11.5, 8), (18.5, 3), (18.5, 21), (11.5, 16), (7.5, 16)], closed=True, r=S.r * 0.5)
    return [shell(body), detail(seg(11.5, 8, 11.5, 16)),
            lead(S, 7.5, 10, 2, 10), lead(S, 7.5, 14, 2, 14)]


@icon("microphone-symbol", CAT, "Microphone schematic symbol: a circle with a straight bar along one side and two leads.",
      tags=["microphone", "mic", "audio input", "schematic", "transducer", "sound"])
def _(S):
    return [shell(circle(14.5, 12, 6.5)), line(seg(8, 4.5, 8, 19.5)),
            lead(S, 8, 6.5, 2, 6.5), lead(S, 8, 17.5, 2, 17.5)]


@icon("antenna-symbol", CAT, "Antenna schematic symbol: a vertical lead topped by an upside down triangle.",
      tags=["antenna", "aerial", "radio", "rf", "schematic", "wireless"])
def _(S):
    return [shell(poly([(4.5, 3), (19.5, 3), (12, 12)], closed=True, r=S.r * 0.5)),
            detail(seg(12, 3, 12, 11)), lead(S, 12, 12, 12, 22)]


def _meter(S, glyph):
    parts = [shell(circle(12, 12, 8)), lead(S, 4, 12, 2, 12), lead(S, 20, 12, 22, 12)]
    if glyph == "A":
        t = 3 / 9
        parts += [detail(poly([(8.8, 16.5), (12, 7.5), (15.2, 16.5)], r=S.r * 0.4), stroke_miterlimit="2"),
                  detail(seg(8.8 + 3.2 * t, 13.5, 15.2 - 3.2 * t, 13.5))]
    else:
        parts.append(detail(poly([(8.8, 7.5), (12, 16.5), (15.2, 7.5)], r=S.r * 0.4), stroke_miterlimit="2"))
    return parts


@icon("ammeter-symbol", CAT, "Ammeter schematic symbol: a circle with a letter A and a lead on each side.",
      tags=["ammeter", "current meter", "amps", "amperes", "schematic", "measurement"])
def _(S):
    return _meter(S, "A")


@icon("voltmeter-symbol", CAT, "Voltmeter schematic symbol: a circle with a letter V and a lead on each side.",
      tags=["voltmeter", "voltage meter", "volts", "potential difference", "schematic", "measurement"])
def _(S):
    return _meter(S, "V")


@icon("signal-ground-symbol", CAT, "Signal ground symbol: a vertical lead ending in a downward pointing triangle.",
      tags=["signal ground", "ground", "reference", "common", "schematic", "0v"])
def _(S):
    return [lead(S, 12, 13, 12, 2), shell(poly([(5.5, 13), (18.5, 13), (12, 20.5)], closed=True, r=S.r * 0.5))]


# ============================================================================ logic and signal blocks

@icon("xnor-gate", CAT, "XNOR logic gate: an OR gate shape with a doubled back curve and an output bubble.",
      tags=["xnor", "logic gate", "exclusive nor", "equivalence", "digital", "boolean"])
def _(S):
    tipx = L(S, 16.5, 16.8)
    body = (f"M8 5C12.5 5 15 8 {tipx} 12C15 16 12.5 19 8 19Q11 12 8 5Z")
    return [shell(body), line("M4 5Q7 12 4 19"), shell(circle(19, 12, 1.9)),
            lead(S, 9.2, 8.5, 2, 8.5), lead(S, 9.2, 15.5, 2, 15.5)]


@icon("buffer-gate", CAT, "Logic buffer symbol: a plain triangle pointing right with one input and one output.",
      tags=["buffer", "logic gate", "driver", "digital", "repeater", "schematic"])
def _(S):
    return [shell(poly([(6, 5), (6, 19), (17.5, 12)], closed=True, r=S.r * 0.5)),
            lead(S, 6, 12, 2, 12), lead(S, 17.5, 12, 22, 12)]


@icon("schmitt-trigger-symbol", CAT, "Schmitt trigger symbol: a buffer triangle with a small hysteresis loop inside.",
      tags=["schmitt trigger", "hysteresis", "buffer", "logic", "debounce", "schematic"])
def _(S):
    return [shell(poly([(2.5, 2.5), (2.5, 21.5), (21.5, 12)], closed=True, r=S.r * 0.5)),
            detail(poly([(4.5, 14.5), (10.5, 14.5), (10.5, 9.5)], r=S.r * 0.4)),
            detail(poly([(12.5, 9.5), (6.5, 9.5), (6.5, 14.5)], r=S.r * 0.4))]


@icon("tri-state-buffer-symbol", CAT, "Tri-state buffer symbol: a buffer triangle with an enable line entering from the top.",
      tags=["tri-state", "three state buffer", "enable", "bus driver", "logic", "schematic"])
def _(S):
    return [shell(poly([(5, 6), (5, 20), (17, 13)], closed=True, r=S.r * 0.5)),
            lead(S, 5, 13, 2, 13), lead(S, 17, 13, 22, 13), lead(S, 11, 9.5, 11, 2)]


@icon("d-flip-flop", CAT, "D flip-flop block: a box with D and clock inputs, a clock wedge and two outputs.",
      tags=["flip-flop", "d type", "latch", "register", "clock", "digital logic"])
def _(S):
    return [shell(rect(5, 3, 14, 18, rr(S, 2))),
            detail("M10.5 5.5H12A3.5 4.5 0 0 1 12 14.5H10.5Z"),
            detail(poly([(5, 14), (7.5, 16.5), (5, 19)], r=S.r * 0.4)),
            lead(S, 5, 7.5, 2, 7.5), lead(S, 5, 16.5, 2, 16.5),
            lead(S, 19, 7.5, 22, 7.5), lead(S, 19, 16.5, 22, 16.5)]


@icon("multiplexer-symbol", CAT, "Multiplexer symbol: a trapezoid wider on the left with three inputs, a select line and one output.",
      tags=["multiplexer", "mux", "selector", "data switch", "digital logic", "schematic"])
def _(S):
    return [shell(poly([(7, 3), (17, 7), (17, 17), (7, 21)], closed=True, r=S.r * 0.5)),
            lead(S, 7, 7, 2, 7), lead(S, 7, 12, 2, 12), lead(S, 7, 17, 2, 17),
            lead(S, 17, 12, 22, 12), lead(S, 12, 19, 12, 22)]


@icon("comparator-symbol", CAT, "Comparator symbol: a triangle with two inputs and a step waveform inside.",
      tags=["comparator", "voltage comparator", "threshold", "op amp", "analog", "schematic"])
def _(S):
    return [shell(poly([(5, 2.5), (5, 21.5), (21.5, 12)], closed=True, r=S.r * 0.5)),
            lead(S, 5, 7.5, 2, 7.5), lead(S, 5, 16.5, 2, 16.5),
            detail(poly([(7.5, 14.5), (11, 14.5), (11, 10.5), (13.8, 10.5)], r=S.r * 0.4))]


@icon("adc-converter", CAT, "Analog to digital converter block: a box split diagonally with a sine wave and a staircase.",
      tags=["adc", "analog to digital", "converter", "sampling", "digitize", "signal"])
def _(S):
    R = rr(S, 3)
    k = R * (1 - math.sqrt(0.5))
    return [shell(rect(2.5, 4, 19, 16, R)),
            detail(seg(21.5 - k, 4 + k, 2.5 + k, 20 - k)),
            detail("M5 9.5C6 7 7 7 8 9.5C9 12 10 12 11 9.5"),
            detail(poly([(12, 17), (14.5, 17), (14.5, 14.5), (17, 14.5), (17, 12), (19.5, 12)], r=S.r * 0.3))]


@icon("voltage-regulator-symbol", CAT, "Voltage regulator block: a box with input and output leads, a ripple turning flat, and a ground.",
      tags=["voltage regulator", "linear regulator", "ldo", "power supply", "schematic", "stabilizer"])
def _(S):
    return [shell(rect(5, 3, 14, 10, rr(S, 2))),
            lead(S, 5, 8, 2, 8), lead(S, 19, 8, 22, 8),
            detail("M7.5 8C8.25 6 9 6 9.75 8C10.5 10 11.25 10 12 8L16.5 8"),
            line(seg(12, 13, 12, 17)), line(seg(8, 17, 16, 17)), line(seg(10.5, 21, 13.5, 21))]


@icon("wire-junction-symbol", CAT, "Wire junction symbol: two crossing wires with a solid dot where they connect.",
      tags=["junction", "node", "connection", "wires", "schematic", "net"])
def _(S):
    return [lead(S, 12, 12, 2, 12), lead(S, 12, 12, 22, 12), lead(S, 12, 12, 12, 2), lead(S, 12, 12, 12, 22),
            dot(12, 12, 3.2)]


@icon("test-point-symbol", CAT, "Test point symbol: a wire ending in a small open circle for a probe.",
      tags=["test point", "probe point", "tp", "measurement", "schematic", "pcb"],
      filled=lambda: U(ST(circle(15, 9, 4.5), 3.4, "butt", "miter"),
                       ST(poly([(10.5, 9), (5.5, 9), (5.5, 22)]), 2.5, "butt", "miter")))
def _(S):
    return [shell(circle(15, 9, 4.5)), line(poly([(10.5, 9), (5.5, 9), (5.5, L(S, 22, 21))], r=S.r))]


@icon("thermocouple-symbol", CAT, "Thermocouple symbol: two wires of different weight meeting in a V at a dot, with plus and minus marks.",
      tags=["thermocouple", "temperature sensor", "junction", "seebeck", "schematic", "probe"])
def _(S):
    cap = "butt" if S.name == "line" else "round"
    e = L(S, 0, 1.2)
    thick = path_to_d(ST(seg(12, 17, 18, 3 + e), 3.6, cap, "miter"))
    return [lead(S, 12, 17, 6, 3), solid(thick), dot(12, 17.5, 2.6),
            line(seg(3.5, 17, 7.5, 17)), line(seg(5.5, 15, 5.5, 19)), line(seg(16.5, 17, 20.5, 17))]


@icon("spark-gap-symbol", CAT, "Spark gap symbol: two leads ending in points that face each other across a gap.",
      tags=["spark gap", "arc gap", "surge arrester", "discharge", "schematic", "overvoltage"])
def _(S):
    return [lead(S, 8, 12, 2, 12), head(S, (10.8, 12), (2, 12), 4, 3.2),
            lead(S, 16, 12, 22, 12), head(S, (13.2, 12), (22, 12), 4, 3.2)]


@icon("neon-lamp-symbol", CAT, "Neon lamp symbol: a circle holding two parallel electrodes and a dot for the gas.",
      tags=["neon lamp", "glow lamp", "indicator", "gas discharge", "schematic", "neon"])
def _(S):
    return [shell(circle(12, 12, 8.5)),
            detail(seg(7, 9.5, 14, 9.5)), detail(seg(7, 14.5, 14, 14.5)),
            detail(seg(10.5, 3.5, 10.5, 9.5)), detail(seg(10.5, 14.5, 10.5, 20.5)),
            dot(17, 12, 1.5)]


@icon("crystal-symbol", CAT, "Crystal schematic symbol: a small block between two parallel plates with a lead on each side.",
      tags=["crystal", "quartz", "oscillator", "resonator", "clock", "schematic"])
def _(S):
    return [line(seg(6, 6, 6, 18)), line(seg(18, 6, 18, 18)), shell(rect(10, 5, 4, 14, L(S, 0, 1))),
            lead(S, 6, 12, 2, 12), lead(S, 18, 12, 22, 12)]


@icon("hall-sensor-symbol", CAT, "Hall effect sensor symbol: a square crossed by an X with a lead on each side.",
      tags=["hall sensor", "hall effect", "magnetic sensor", "magnetometer", "schematic", "position sensor"])
def _(S):
    return [shell(rect(6, 6, 12, 12, rr(S, 2))),
            detail(seg(9, 9, 15, 15)), detail(seg(15, 9, 9, 15)),
            lead(S, 6, 12, 2, 12), lead(S, 18, 12, 22, 12), lead(S, 12, 6, 12, 2), lead(S, 12, 18, 12, 22)]


# ============================================================================ signals

def wave(f, df, x0, x1, n):
    """Smooth path through y = f(x) from x0 to x1 as n cubic Hermite segments."""
    h = (x1 - x0) / n
    out = f"M{fmt(x0)} {fmt(f(x0))}"
    for i in range(n):
        a, b = x0 + i * h, x0 + (i + 1) * h
        c1 = (a + h / 3, f(a) + df(a) * h / 3)
        c2 = (b - h / 3, f(b) - df(b) * h / 3)
        out += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(b)} {fmt(f(b))}"
    return out


def _sine(phase, amp=6.5, x0=3.0, x1=21.0, cy=12.0):
    w = 2 * math.pi / (x1 - x0)
    return (lambda x: cy - amp * math.sin(w * (x - x0) + phase),
            lambda x: -amp * w * math.cos(w * (x - x0) + phase))


@icon("pwm-signal", CAT, "PWM signal: a pulse train whose flat topped pulses change width.",
      tags=["pwm", "pulse width modulation", "duty cycle", "square wave", "signal", "motor control"])
def _(S):
    pts = [(L(S, 2, 3), 18), (4, 18), (4, 6), (8, 6), (8, 18), (11.5, 18), (11.5, 6), (18.5, 6), (18.5, 18),
           (L(S, 22, 21), 18)]
    return [line(poly(pts, r=S.r))]


@icon("signal-noise", CAT, "Signal noise: a flat line broken by a jagged, random spiky trace.",
      tags=["noise", "interference", "static", "jitter", "signal", "random"])
def _(S):
    pts = [(L(S, 2, 3), 12), (4.5, 12), (6, 8.5), (8, 16), (10, 5.5), (12, 17.5), (14, 8), (16, 15), (17.5, 9.5),
           (19, 12), (L(S, 22, 21), 12)]
    return [line(poly(pts, r=L(S, 0, 0.4)), stroke_miterlimit="2")]


@icon("am-modulation", CAT, "Amplitude modulation: a fast carrier wave whose peaks swell and shrink with a slow envelope.",
      tags=["am", "amplitude modulation", "radio", "carrier wave", "envelope", "signal"])
def _(S):
    x0, x1, per = 2.0, 22.0, 5.0

    def A(x):
        return 1.2 + 6.3 * math.sin(math.pi * (x - x0) / (x1 - x0)) ** 2

    def dA(x):
        t = math.pi * (x - x0) / (x1 - x0)
        return 6.3 * 2 * math.sin(t) * math.cos(t) * math.pi / (x1 - x0)

    w = 2 * math.pi / per
    f = lambda x: 12 - A(x) * math.sin(w * (x - x0))  # noqa: E731
    df = lambda x: -(dA(x) * math.sin(w * (x - x0)) + A(x) * w * math.cos(w * (x - x0)))  # noqa: E731
    return [line(wave(f, df, x0, x1, 20))]


@icon("fm-modulation", CAT, "Frequency modulation: a wave of constant height whose cycles bunch up in the middle.",
      tags=["fm", "frequency modulation", "radio", "carrier wave", "chirp", "signal"])
def _(S):
    x0, x1 = 2.0, 22.0
    k0, k1, sd = 0.7, 0.95, 2.6

    def ph(x):  # integral of k0 + k1 * gaussian
        return k0 * (x - 12) + k1 * sd * math.sqrt(math.pi / 2) * math.erf((x - 12) / (sd * math.sqrt(2)))

    def dph(x):
        return k0 + k1 * math.exp(-((x - 12) / sd) ** 2 / 2)

    base = ph(x0)
    f = lambda x: 12 - 5.5 * math.sin(ph(x) - base)  # noqa: E731
    df = lambda x: -5.5 * math.cos(ph(x) - base) * dph(x)  # noqa: E731
    return [line(wave(f, df, x0, x1, 24))]


# ============================================================================ passive components

@icon("smd-resistor", CAT, "Surface mount resistor: a flat rectangular chip with metal end caps and a printed code.",
      tags=["smd resistor", "chip resistor", "surface mount", "0805", "pcb", "component"])
def _(S):
    return [shell(rect(2.5, 7.5, 19, 9, rr(S, 3))), detail(seg(7, 7.5, 7, 16.5)), detail(seg(17, 7.5, 17, 16.5)),
            dot(9.5, 12, 1.1), dot(12, 12, 1.1), dot(14.5, 12, 1.1)]


@icon("resistor-network", CAT, "Resistor network: a flat single row package with pins along its bottom and a pin one dot.",
      tags=["resistor network", "resistor array", "sip", "pull up", "component", "package"])
def _(S):
    pins = [lead(S, x, 14, x, 22) for x in (4.5, 8.25, 12, 15.75, 19.5)]
    return [shell(rect(2.5, 5, 19, 9, rr(S, 2))), dot(6, 9.5, 1.4), *pins]


@icon("ceramic-disc-capacitor", CAT, "Ceramic disc capacitor: a flat round disc with two thin legs below.",
      tags=["ceramic capacitor", "disc capacitor", "capacitor", "component", "through hole", "decoupling"])
def _(S):
    e = L(S, 22, 21)
    return [shell(circle(12, 9, 6.5)),
            line(poly([(9.5, 14.5), (9.5, 17), (7.5, 19), (7.5, e)], r=S.r)),
            line(poly([(14.5, 14.5), (14.5, 17), (16.5, 19), (16.5, e)], r=S.r))]


@icon("film-capacitor", CAT, "Film capacitor: a boxy block with rounded corners, a printed capacitor mark and two legs below.",
      tags=["film capacitor", "box capacitor", "polyester capacitor", "capacitor", "component", "through hole"])
def _(S):
    e = L(S, 22, 21)
    return [shell(rect(3.5, 3, 17, 12.5, rr(S, 3))),
            detail(seg(10, 6, 10, 12.5)), detail(seg(14, 6, 14, 12.5)),
            detail(seg(6.5, 9.25, 10, 9.25)), detail(seg(14, 9.25, 17.5, 9.25)),
            line(seg(8.5, 15.5, 8.5, e)), line(seg(15.5, 15.5, 15.5, e))]


@icon("tantalum-capacitor", CAT, "Tantalum capacitor: a small teardrop bead with a plus mark and two legs.",
      tags=["tantalum capacitor", "bead capacitor", "polarized", "capacitor", "component", "through hole"])
def _(S):
    e = L(S, 22, 21)
    body = "M12 17.5C9 15.5 5.5 12.5 5.5 9A6.5 6.5 0 0 1 18.5 9C18.5 12.5 15 15.5 12 17.5Z"
    return [shell(body), detail(seg(9.5, 9, 14.5, 9)), detail(seg(12, 6.5, 12, 11.5)),
            line(poly([(10, 16.2), (8.5, 18.5), (8.5, e)], r=S.r)),
            line(poly([(14, 16.2), (15.5, 18.5), (15.5, e)], r=S.r))]


@icon("supercapacitor", CAT, "Supercapacitor: a wide squat coin shaped can with a large plus sign and two legs.",
      tags=["supercapacitor", "ultracapacitor", "supercap", "energy storage", "capacitor", "component"])
def _(S):
    e = L(S, 22, 21)
    body = "M3 6A9 2.5 0 0 1 21 6V14A9 2.5 0 0 1 3 14Z"
    return [shell(body), detail("M3 6A9 2.5 0 0 0 21 6"),
            detail(seg(9.5, 12.5, 14.5, 12.5)), detail(seg(12, 10.5, 12, 14.5)),
            line(seg(8, 16, 8, e)), line(seg(16, 16, 16, e))]


@icon("trimmer-potentiometer", CAT, "Trimmer potentiometer: a small square block with a slotted round adjuster and three pins.",
      tags=["trimmer", "trim pot", "preset", "potentiometer", "adjustable resistor", "component"])
def _(S):
    e = L(S, 22, 21)
    a, b = polar(12, 10, 4.5, 135), polar(12, 10, 4.5, -45)
    return [shell(rect(4.5, 2.5, 15, 15, rr(S, 3))), detail(circle(12, 10, 4.5)), detail(seg(a[0], a[1], b[0], b[1])),
            line(seg(8, 17.5, 8, e)), line(seg(12, 17.5, 12, e)), line(seg(16, 17.5, 16, e))]


@icon("slide-potentiometer", CAT, "Slide potentiometer: a long body with a lever and square knob sliding along it, and pins below.",
      tags=["slide potentiometer", "fader", "slider", "linear pot", "mixer", "component"])
def _(S):
    e = L(S, 22, 21)
    return [shell(rect(2, 12, 20, 5, rr(S, 2))), shell(rect(8, 3, 8, 5.5, rr(S, 2))), line(seg(12, 8.5, 12, 12)),
            line(seg(5, 17, 5, e)), line(seg(19, 17, 19, e))]


# ============================================================================ switches

@icon("rotary-switch", CAT, "Rotary switch: a round knob with a pointer and a ring of position dots.",
      tags=["rotary switch", "selector", "multi position", "knob", "band switch", "component"])
def _(S):
    parts = [shell(circle(12, 13.5, 5.5)), detail(seg(12, 13.5, 12, 9.5))]
    for a in (-162, -126, -90, -54, -18):
        x, y = polar(12, 13.5, 9, a)
        parts.append(dot(x, y, 1.3))
    return parts


@icon("dip-switch", CAT, "DIP switch: a small block with a row of slide toggles, some up and some down.",
      tags=["dip switch", "configuration", "jumper", "toggle", "settings", "component"])
def _(S):
    parts = [shell(rect(2, 6, 20, 12, rr(S, 2.5)))]
    for x, up in ((6, True), (10, False), (14, True), (18, True)):
        parts.append(sq(x - 1.2, 8.5 if up else 11.5, 2.4, 4, L(S, 0, 0.8)))
    return parts


@icon("tactile-switch", CAT, "Tactile switch: a small square base with four legs and a round push button.",
      tags=["tactile switch", "push button", "tact switch", "momentary", "button", "component"])
def _(S):
    return [shell(rect(5, 5, 14, 14, rr(S, 2.5))), detail(circle(12, 12, 3.2)),
            lead(S, 5, 8, 2, 8), lead(S, 5, 16, 2, 16), lead(S, 19, 8, 22, 8), lead(S, 19, 16, 22, 16)]


@icon("slide-switch", CAT, "Slide switch: a small box with a sliding nub on top and three pins below.",
      tags=["slide switch", "on off switch", "toggle", "power switch", "spdt", "component"])
def _(S):
    e = L(S, 22, 21)
    body = poly([(3, 8), (6.5, 8), (6.5, 3.5), (11, 3.5), (11, 8), (21, 8), (21, 15), (3, 15)], closed=True, r=S.r * 0.5)
    return [shell(body), line(seg(7, 15, 7, e)), line(seg(12, 15, 12, e)), line(seg(17, 15, 17, e))]


@icon("reed-switch", CAT, "Reed switch: a glass capsule with two overlapping metal reeds and a lead out of each end.",
      tags=["reed switch", "magnetic sensor", "door sensor", "glass", "reed", "component"])
def _(S):
    body = ("M8.5 6.5H15.5C18 6.5 18.5 10.5 20 12C18.5 13.5 18 17.5 15.5 17.5H8.5"
            "C6 17.5 5.5 13.5 4 12C5.5 10.5 6 6.5 8.5 6.5Z")
    return [shell(body), lead(S, 4, 12, 2, 12), lead(S, 20, 12, 22, 12),
            detail(poly([(4.5, 12), (7, 12), (8.5, 10), (14.5, 10)], r=S.r * 0.4)),
            detail(poly([(19.5, 12), (17, 12), (15.5, 14), (9.5, 14)], r=S.r * 0.4))]


@icon("tilt-switch", CAT, "Tilt switch: a leaning can with a metal ball resting in its lower corner and two legs.",
      tags=["tilt switch", "ball switch", "tilt sensor", "orientation", "vibration", "component"])
def _(S):
    th, cx, cy = -18.0, 12.0, 15.0  # can leans left, pivoting about its bottom centre
    c, s = math.cos(math.radians(th)), math.sin(math.radians(th))

    def w(u, v):
        return (cx + u * c - v * s, cy + u * s + v * c)
    body = poly([w(-4.5, -12), w(4.5, -12), w(4.5, 0), w(-4.5, 0)], closed=True, r=L(S, 2, 3.5))
    bx, by = w(-1.3, -3.0)
    parts = [shell(body), dot(bx, by, 1.85)]
    for u in (-2.2, 2.2):
        x, y = w(u, 0)
        parts.append(line(seg(x, y - 0.5, x, L(S, 22, 21))))
    return parts


@icon("selector-switch", CAT, "Selector switch: a round panel switch with a bar handle across its face and two position marks.",
      tags=["selector switch", "panel switch", "hand off auto", "rotary selector", "control panel", "industrial"])
def _(S):
    hl, hw = 5.5, 2.2
    pts = [(12 - hl, 13 - hw), (12 + hl, 13 - hw), (12 + hl, 13 + hw), (12 - hl, 13 + hw)]
    pts = rot_pts(pts, -45, 12, 13)
    a, b = polar(12, 13, 10, -135), polar(12, 13, 10, -45)
    return [shell(circle(12, 13, 8)), detail(poly(pts, closed=True, r=L(S, 0, 1.5))),
            dot(a[0], a[1], 1.4), dot(b[0], b[1], 1.4)]


@icon("panel-indicator-light", CAT, "Panel indicator light: a domed lens on a flange and threaded body, with short light rays.",
      tags=["indicator light", "pilot light", "panel lamp", "signal lamp", "status light", "control panel"])
def _(S):
    body = ("M6 13A6 6 0 0 1 18 13" + poly([(18, 13), (19.5, 13), (19.5, 16), (16, 16), (16, 21), (8, 21), (8, 16),
                                               (4.5, 16), (4.5, 13), (6, 13)], r=S.r * 0.4)[len("M18 13"):] + "Z")
    parts = [shell(body), detail(seg(6, 13, 18, 13)), detail(seg(8, 18.5, 16, 18.5))]
    for a in (-90, -140, -40):
        x1, y1 = polar(12, 13, 8.3, a)
        x2, y2 = polar(12, 13, 10.3, a)
        parts.append(line(seg(x1, y1, x2, y2)))
    return parts


# ============================================================================ chip packages

@icon("dip-chip", CAT, "DIP chip: a rectangular chip seen from above with a notch at one end and legs along both long sides.",
      tags=["dip", "integrated circuit", "ic", "chip", "through hole", "microchip"])
def _(S):
    parts = [shell(rect(7, 3, 10, 18, rr(S, 2))), detail(arc(12, 3, 2, 0, 180))]
    for y in (6.5, 10.5, 14.5, 18.5):
        parts += [lead(S, 7, y, 3, y), lead(S, 17, y, 21, y)]
    return parts


@icon("soic-chip", CAT, "SOIC chip: a low, wide surface mount chip with short legs along its two long sides and a pin one dot.",
      tags=["soic", "surface mount", "smd", "integrated circuit", "chip", "gull wing"])
def _(S):
    parts = [shell(rect(3, 7.5, 18, 9, rr(S, 2))), dot(6, 10.5, 1.3)]
    for x in (6, 10, 14, 18):
        parts += [lead(S, x, 7.5, x, 4), lead(S, x, 16.5, x, 20)]
    return parts


@icon("qfp-chip", CAT, "QFP chip: a square flat chip with legs along all four sides and a dot in one corner.",
      tags=["qfp", "quad flat package", "surface mount", "microcontroller", "integrated circuit", "chip"])
def _(S):
    parts = [shell(rect(5, 5, 14, 14, rr(S, 2))), dot(8.5, 8.5, 1.4)]
    for p in (8.5, 12, 15.5):
        parts += [lead(S, p, 5, p, 2), lead(S, p, 19, p, 22), lead(S, 5, p, 2, p), lead(S, 19, p, 22, p)]
    return parts


@icon("bga-chip", CAT, "BGA chip seen from below: a square with a grid of round solder balls and a cut pin one corner.",
      tags=["bga", "ball grid array", "solder balls", "surface mount", "integrated circuit", "chip"])
def _(S):
    body = poly([(3, 8), (8, 3), (21, 3), (21, 21), (3, 21)], closed=True, r=L(S, 0, 2.5))
    parts = [shell(body)]
    for i, x in enumerate((7, 10.33, 13.67, 17)):
        for j, y in enumerate((7, 10.33, 13.67, 17)):
            if i == 0 and j == 0:
                continue
            parts.append(dot(x, y, 1.15))
    return parts


@icon("metal-can-transistor", CAT, "Metal can transistor: a short round can with a small tab on its rim and three legs below.",
      tags=["to-18", "to-39", "metal can", "transistor", "through hole", "component"])
def _(S):
    e = L(S, 22, 21)
    body = poly([(6.5, 12), (6.5, 3.5), (17.5, 3.5), (17.5, 12), (21.5, 12), (21.5, 15), (4.5, 15), (4.5, 12)],
                closed=True, r=S.r * 0.6)
    return [shell(body), line(seg(8, 15, 8, e)), line(seg(12, 15, 12, e)), line(seg(16, 15, 16, e))]


@icon("ic-socket", CAT, "IC socket: an open rectangular frame with a row of contact holes along both long sides.",
      tags=["ic socket", "dip socket", "chip socket", "through hole", "component", "pcb"])
def _(S):
    parts = [shell(rect(4, 2.5, 16, 19, rr(S, 2))), detail(rect(10, 6, 4, 12, L(S, 0, 1)))]
    for y in (6, 10, 14, 18):
        parts += [dot(7, y, 1.2), dot(17, y, 1.2)]
    return parts
