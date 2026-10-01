"""TypeIcon Core: electronics (batch 004): power hardware, circuit states, textbook circuits and antennas.

Drawn from the objects and from plain schematic conventions. Schematic icons keep their wires on whole
coordinates and leave at least 2 px between separate strokes.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d

CAT = "electronics"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def star(cx, cy, ro, ri, n, start=-90.0):
    pts = []
    for i in range(2 * n):
        r = ro if i % 2 == 0 else ri
        a = math.radians(start + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def along(p, q, t, off=0.0):
    """Point a fraction t along p->q, pushed off the line by off (to the left of travel)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    ln = math.hypot(dx, dy)
    nx, ny = dy / ln, -dx / ln
    return (p[0] + dx * t + nx * off, p[1] + dy * t + ny * off)


def box_on(p, q, t0, t1, hw):
    """Rectangle lying on the segment p->q between fractions t0 and t1, half-width hw (a resistor body)."""
    return [along(p, q, t0, hw), along(p, q, t1, hw), along(p, q, t1, -hw), along(p, q, t0, -hw)]


BOLT = [(12.5, 7.5), (9, 12.5), (11.75, 12.5), (11, 16.5), (15, 11.5), (12.25, 11.5)]


# ============================================================================ power hardware

@icon("din-rail-power-supply", CAT, "Narrow power supply box clipped to a mounting rail, with vents and screw terminals.",
      tags=["din rail", "power supply", "psu", "control cabinet", "industrial", "24v", "switch mode"])
def _(S):
    return [
        shell(rect(7, 2.5, 10, 19, rr(S, 2))),
        line(seg(2, 10, 7, 10)), line(seg(2, 15, 7, 15)),
        line(seg(17, 10, 22, 10)), line(seg(17, 15, 22, 15)),
        detail(seg(10, 6, 14, 6)),
        mark(poly(BOLT, closed=True)),
        dot(10, 18.5, 1.1), dot(14, 18.5, 1.1),
    ]


@icon("solar-charge-controller", CAT, "Controller box with a small display and terminals under a rising sun.",
      tags=["solar", "charge controller", "mppt", "pwm", "off grid", "battery charging", "regulator"])
def _(S):
    rays = [line(seg(*along((12, 9), (12 + 7 * math.cos(math.radians(a)), 9 + 7 * math.sin(math.radians(a))), 0.72),
                     *along((12, 9), (12 + 7 * math.cos(math.radians(a)), 9 + 7 * math.sin(math.radians(a))), 0.95)))
            for a in (-90, -145, -35)]
    return [
        line(arc(12, 9, 3, 180, 360)),
        *rays,
        shell(rect(3, 9, 18, 12.5, rr(S, 2))),
        detail(rect(6.5, 12.5, 11, 2, 0)),
        dot(8, 18, 1.1), dot(12, 18, 1.1), dot(16, 18, 1.1),
    ]


@icon("power-distribution-unit", CAT, "Rack-mounted power strip with a row of sockets and mounting ears.",
      tags=["pdu", "rack", "power strip", "server room", "data center", "outlets", "sockets"])
def _(S):
    parts = [shell(rect(2, 7.5, 20, 9, rr(S, 2))),
             detail(seg(5.5, 7.5, 5.5, 16.5)), detail(seg(18.5, 7.5, 18.5, 16.5))]
    for x in (9, 12, 15):
        parts.append(mark(rect(x - 0.75, 10, 1.5, 4, L(S, 0, 0.75))))
    return parts


@icon("battery-balancer", CAT, "Small balancing board wired to a row of battery cells.",
      tags=["battery balancer", "cell balancing", "bms", "lithium", "battery pack", "equalizer"])
def _(S):
    parts = [shell(rect(3, 2.5, 18, 5, L(S, 1, 2.5)))]
    for x in (3.5, 10, 16.5):
        parts.append(line(seg(x + 2, 7.5, x + 2, 11)))
        parts.append(shell(rect(x, 11, 4, 10.5, L(S, 0.75, 2))))
    return parts


# ============================================================================ circuit states

@icon("short-circuit", CAT, "Two wires touching with a spark at the contact point.",
      tags=["short circuit", "short", "spark", "fault", "electrical fault", "wiring fault"])
def _(S):
    return [
        line(poly([(2, 17), (6, 17), (8.5, 14.5)], r=S.r)),
        line(poly([(22, 7), (18, 7), (15.5, 9.5)], r=S.r)),
        shell(poly(star(12, 12, 5.5, 2.75, 7, -80), closed=True)),
    ]


@icon("open-circuit", CAT, "Circuit loop with a battery and a gap where the wire is broken.",
      tags=["open circuit", "broken circuit", "gap", "disconnected", "break", "no current"])
def _(S):
    return [
        line(poly([(8.5, 4.5), (3, 4.5), (3, 17.5), (10.5, 17.5)], r=S.r)),
        line(poly([(15.5, 4.5), (21, 4.5), (21, 17.5), (13.5, 17.5)], r=S.r)),
        line(seg(10.5, 13.5, 10.5, 21.5)),
        line(seg(13.5, 15, 13.5, 20)),
        dot(9.5, 4.5, 1.6), dot(14.5, 4.5, 1.6),
    ]


@icon("arc-flash", CAT, "Electrical cabinet with a jagged arc jumping between two terminals.",
      tags=["arc flash", "electrical hazard", "arc fault", "high voltage", "danger", "switchgear"])
def _(S):
    zig = [(8.5, 12), (10.25, 9.5), (12, 14.5), (13.75, 9.5), (15.5, 12)]
    return [
        shell(rect(3, 3, 18, 18, rr(S))),
        dot(7, 12, 1.5), dot(17, 12, 1.5),
        detail(poly(zig, r=S.r * 0.3)),
        detail(seg(12, 6, 12, 7)),
        detail(seg(12, 17, 12, 18)),
    ]


# ============================================================================ textbook circuits

@icon("pn-junction", CAT, "Block split into a P side with plus charges and an N side with minus charges.",
      tags=["pn junction", "semiconductor", "diode", "p type", "n type", "depletion", "physics"])
def _(S):
    return [
        shell(rect(2, 5, 20, 14, rr(S))),
        detail(seg(12, 5, 12, 19)),
        detail(seg(5, 12, 9, 12)), detail(seg(7, 10, 7, 14)),
        detail(seg(15, 12, 19, 12)),
    ]


@icon("wheatstone-bridge", CAT, "Diamond of four resistors with a meter across the middle.",
      tags=["wheatstone bridge", "bridge circuit", "resistance", "measurement", "galvanometer", "physics"])
def _(S):
    top, rt, bot, lf = (12, 2.5), (21.5, 12), (12, 21.5), (2.5, 12)
    parts = [line(poly([top, rt, bot, lf], closed=True, r=S.r))]
    for p, q in ((lf, top), (top, rt), (rt, bot), (bot, lf)):
        parts.append(mark(poly(box_on(p, q, 0.3, 0.7, 1.5), closed=True, r=L(S, 0, 0.6))))
    parts += [line(seg(2.5, 12, 8.5, 12)), line(seg(15.5, 12, 21.5, 12)), shell(circle(12, 12, 2.5))]
    return parts


@icon("voltage-divider", CAT, "Two resistors in series with an output tap taken from between them.",
      tags=["voltage divider", "potential divider", "resistors", "series circuit", "tap", "schematic"])
def _(S):
    k = rr(S, 1)
    return [
        line(seg(9, 2, 9, 4)),
        shell(rect(6, 4, 6, 6, k)),
        line(seg(9, 10, 9, 14)),
        shell(rect(6, 14, 6, 6, k)),
        line(seg(9, 20, 9, 22)),
        dot(9, 12, 1.75),
        line(seg(9, 12, 16.5, 12)),
        shell(circle(18.5, 12, 2)),
    ]


@icon("h-bridge", CAT, "H-shaped circuit of four switches with a motor in the crossbar.",
      tags=["h bridge", "motor driver", "dc motor", "reversing", "switches", "schematic"])
def _(S):
    parts = []
    for x in (5, 19):
        parts += [line(seg(x, 2, x, 22))]
        for y in (6.5, 17.5):
            parts.append(mark(rect(x - 2, y - 2, 4, 4, L(S, 0, 1.25))))
    parts += [line(seg(5, 12, 9, 12)), line(seg(15, 12, 19, 12)), shell(circle(12, 12, 3))]
    return parts


@icon("farad-unit", CAT, "Capital letter F beside a capacitor symbol; the unit of capacitance.",
      tags=["farad", "capacitance", "unit", "capacitor", "si unit", "physics"])
def _(S):
    return [
        line(poly([(11, 5), (4, 5), (4, 19)], r=S.r)),
        line(seg(4, 12, 9.5, 12)),
        line(seg(13, 12, 15.5, 12)),
        line(seg(15.5, 7, 15.5, 17)),
        line(seg(19.5, 7, 19.5, 17)),
        line(seg(19.5, 12, 22, 12)),
    ]


@icon("electron-flow", CAT, "Electrons marked with minus signs above an arrow showing their flow.",
      tags=["electron flow", "current", "electrons", "charge", "negative charge", "physics"])
def _(S):
    return [
        shell(circle(6.5, 8.5, 4)), detail(seg(4.5, 8.5, 8.5, 8.5)),
        shell(circle(17.5, 8.5, 4)), detail(seg(15.5, 8.5, 19.5, 8.5)),
        line(seg(3, 18, 20, 18)),
        line(poly([(17, 15), (20, 18), (17, 21)], r=S.r)),
    ]


@icon("pinout-diagram", CAT, "Chip outline with a label line beside each pin.",
      tags=["pinout", "pin diagram", "datasheet", "chip pins", "ic", "wiring reference"])
def _(S):
    parts = [shell(rect(9, 3.5, 6, 17, rr(S, 1.5))), detail(arc(12, 3.5, 1.5, 0, 180))]
    for y in (7.5, 12, 16.5):
        parts += [line(seg(6.5, y, 9, y)), line(seg(15, y, 17.5, y)),
                  line(seg(2, y, 4.5, y)), line(seg(19.5, y, 22, y))]
    return parts


@icon("dipole-antenna", CAT, "Two rods reaching out in opposite directions from a feed point on a mast.",
      tags=["dipole", "antenna", "aerial", "radio", "ham radio", "rabbit ears"])
def _(S):
    return [
        line(seg(2, 6.5, 9.5, 6.5)), line(seg(14.5, 6.5, 22, 6.5)),
        dot(2.5, 6.5, 1.5), dot(21.5, 6.5, 1.5),
        shell(rect(9.5, 4, 5, 5, rr(S, 1.5))),
        line(seg(12, 9, 12, 21.5)),
        line(seg(8, 21.5, 16, 21.5)),
    ]


@icon("helical-antenna", CAT, "Wire coil standing upright on a round ground plate.",
      tags=["helical antenna", "helix", "coil antenna", "satellite", "circular polarization", "aerial"])
def _(S):
    pts = [(12, 16.5), (16.5, 14.5), (7.5, 11.5), (16.5, 8.5), (7.5, 5.5), (16.5, 2.5)]
    return [
        line(poly(pts, r=L(S, 0, 0.8))),
        shell(ellipse(12, 19.5, 9, 2)),
    ]


@icon("ferrite-rod-antenna", CAT, "Ferrite rod with a coil of wire wound around its middle and two leads.",
      tags=["ferrite rod", "loopstick", "am radio", "antenna", "coil", "medium wave"])
def _(S):
    return [
        shell(rect(2, 9.5, 4.5, 5, L(S, 0, 2))), shell(rect(17.5, 9.5, 4.5, 5, L(S, 0, 2))),
        shell(rect(6.5, 7, 11, 10, rr(S, 1.5))),
        detail(seg(10, 7, 10, 17)), detail(seg(14, 7, 14, 17)),
        line(poly([(8.5, 17), (8.5, 21.5)], r=S.r)),
        line(poly([(15.5, 17), (15.5, 21.5)], r=S.r)),
    ]


@icon("waveguide", CAT, "Rectangular metal tube bent through a right angle with a flange at each end.",
      tags=["waveguide", "microwave", "radar", "rf", "flange", "transmission line"])
def _(S):
    k = S.r
    tube = poly([(4, 13), (11, 13), (11, 4), (18, 4), (18, 20), (4, 20)], closed=True, r=0)
    if S.name == "rounded":
        tube = f"M4 13L11 13L11 4L18 4L18 14A6 6 0 0 1 12 20L4 20Z"
    else:
        tube = poly([(4, 13), (11, 13), (11, 4), (18, 4), (18, 16), (14, 20), (4, 20)], closed=True, r=k)
    return [
        shell(tube),
        shell(rect(2, 11, 2, 11, 0)),
        shell(rect(9, 2, 11, 2, 0)),
    ]


@icon("crystal-earpiece", CAT, "Small round earpiece with an ear nozzle and a long thin cord.",
      tags=["crystal earpiece", "earphone", "crystal radio", "piezo", "listen", "vintage radio"])
def _(S):
    return [
        shell(poly([(8, 8), (9, 3), (13, 3), (14, 8)], closed=True, r=S.r * 0.5)),
        shell(rect(5.5, 8, 11, 7, rr(S, 3))),
        line("M11 15C11 19.5 14 20.5 16.5 20.5C19 20.5 20 19 22 19"),
    ]
