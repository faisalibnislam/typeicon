"""TypeIcon Core: electronics (batch 003): bench tools, boards, modules, sensors, test gear and soldering kit.

Drawn from the objects themselves. Pen shaped tools (probes, pens, pumps) are designed upright and turned 45°
clockwise so the handle points to the bottom-left and the working end to the top-right, as in the tools set.
Boards and modules are drawn flat, seen from the top.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, rotation, transform_path

CAT = "electronics"
TILT = 45


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def mark(d) -> Part:
    """Small solid mark: solid in stroke styles, knocked out of a Filled shell."""
    return Part("dot", d)


def pip(S, x, y, s=2.0) -> Part:
    """A small square (Line) or round (Rounded) marker centred on (x, y)."""
    if S.name == "rounded":
        return dot(x, y, s / 2 + 0.1)
    return sq(x - s / 2, y - s / 2, s, s)


def thick(d, w, S):
    """Closed outline of a stroke of width w along d."""
    return path_to_d(ST(d, w, S.cap, S.join))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def turn(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


class Frame:
    """Upright design coordinates, turned clockwise by deg about (12, 12) and then moved by (dx, dy)."""

    def __init__(self, deg=TILT, dx=0.0, dy=0.0):
        a = math.radians(deg)
        self.c, self.s, self.dx, self.dy = math.cos(a), math.sin(a), dx, dy

    def p(self, x, y):
        return (12 + (x - 12) * self.c - (y - 12) * self.s + self.dx,
                12 + (x - 12) * self.s + (y - 12) * self.c + self.dy)

    def pts(self, pts):
        return [self.p(x, y) for x, y in pts]

    def poly(self, pts, closed=True, r=0.0):
        return poly(self.pts(pts), closed=closed, r=r)

    def seg(self, x1, y1, x2, y2):
        (a, b), (c, d) = self.pts([(x1, y1), (x2, y2)])
        return seg(a, b, c, d)

    def path(self, cmds):
        """("M", p) ("L", p) ("A", r, large, sweep, p) ("Q", c, p) ("C", c1, c2, p) ("Z",)"""
        out = []

        def q(p):
            x, y = self.p(*p)
            return f"{fmt(x)} {fmt(y)}"
        for k in cmds:
            op = k[0]
            if op in ("M", "L"):
                out.append(op + q(k[1]))
            elif op == "A":
                out.append(f"A{fmt(k[1])} {fmt(k[1])} 0 {k[2]} {k[3]} " + q(k[4]))
            elif op == "Q":
                out.append("Q" + q(k[1]) + " " + q(k[2]))
            elif op == "C":
                out.append("C" + q(k[1]) + " " + q(k[2]) + " " + q(k[3]))
            elif op == "Z":
                out.append("Z")
        return "".join(out)

    def rect(self, x, y, w, h, rx=0.0):
        rx = max(0.0, min(rx, w / 2, h / 2))
        if rx == 0:
            return self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])
        return self.path([("M", (x + rx, y)), ("L", (x + w - rx, y)), ("A", rx, 0, 1, (x + w, y + rx)),
                          ("L", (x + w, y + h - rx)), ("A", rx, 0, 1, (x + w - rx, y + h)), ("L", (x + rx, y + h)),
                          ("A", rx, 0, 1, (x, y + h - rx)), ("L", (x, y + rx)), ("A", rx, 0, 1, (x + rx, y)), ("Z",)])

    def circle(self, x, y, r):
        cx, cy = self.p(x, y)
        return circle(cx, cy, r)

    def dot(self, x, y, r=1.25):
        cx, cy = self.p(x, y)
        return dot(cx, cy, r)


def squiggle(x, y0, y1, amp=1.5):
    """Vertical wavy line from (x, y0) up or down to (x, y1): one S bend (heat or smoke)."""
    m = (y0 + y1) / 2
    k = (y1 - y0) / 4
    return (f"M{fmt(x)} {fmt(y0)}C{fmt(x - amp * 1.3)} {fmt(y0 + k)} {fmt(x - amp * 1.3)} {fmt(m - k * 0.2)} {fmt(x)} {fmt(m)}"
            f"C{fmt(x + amp * 1.3)} {fmt(m + k * 0.2)} {fmt(x + amp * 1.3)} {fmt(y1 - k)} {fmt(x)} {fmt(y1)}")


def drop(cx, top, bottom, S):
    """Teardrop pointing up: sharp tip in Line, softened tip in Rounded."""
    h = bottom - top
    r = h * 0.36
    cy = bottom - r
    t = L(S, 0.0, 0.6)
    a1 = pt(cx, cy, r, 210)
    a2 = pt(cx, cy, r, 330)
    if t:
        return (f"M{fmt(cx - t * 0.6)} {fmt(top + t)}Q{fmt(cx)} {fmt(top)} {fmt(cx + t * 0.6)} {fmt(top + t)}"
                f"L{fmt(a2[0])} {fmt(a2[1])}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(a1[0])} {fmt(a1[1])}Z")
    return f"M{fmt(cx)} {fmt(top)}L{fmt(a2[0])} {fmt(a2[1])}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(a1[0])} {fmt(a1[1])}Z"


def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


# ============================================================================ wiring and board making

@icon("tone-generator-probe", CAT, "Pen shaped tone probe with a pointed tip sending out sound waves.",
      tags=["tone probe", "cable tracer", "wire tracer", "toner", "network cable", "tracing"])
def _(S):
    f = Frame(TILT, -2.5, 2.5)
    tip = f.p(12, 3.5)
    return [
        shell(f.poly([(12, 3.5), (14.5, 8), (9.5, 8)], r=S.r * 0.4), stroke_miterlimit="3"),
        shell(f.rect(9.5, 8, 5, 11, rr(S, 2.5))),
        f.dot(12, 12.5, 1.1),
        line(f.seg(12, 19, 12, 21.5)),
        line(arc(tip[0], tip[1], 4, 285, 345)),
        line(arc(tip[0], tip[1], 7.5, 283, 347)),
    ]


def _gauge_disc():
    body = P(circle(12, 12, 9))
    cuts = []
    for k in range(8):
        slot = U(P(rect(10.25, 0, 3.5, 7)), P(circle(12, 7, 1.75)))
        cuts.append(transform_path(slot, rotation(k * 45 + 22.5, 12, 12)))
    return path_to_d(D(body, *cuts))


@icon("wire-gauge", CAT, "Round wire gauge disc with sizing slots cut into its edge and a centre hole.",
      tags=["awg", "wire size", "gauge plate", "measure wire", "wire thickness", "sheet gauge"])
def _(S):
    return [shell(_gauge_disc(), stroke_linejoin="round" if S.name == "rounded" else "miter"),
            detail(circle(12, 12, 2)) if S.name == "rounded" else detail(rect(10.25, 10.25, 3.5, 3.5))]


@icon("punchdown-tool", CAT, "Punch down tool pressing a wire into the slot of a terminal block.",
      tags=["punch down", "110 block", "network wiring", "keystone", "termination", "insertion tool"])
def _(S):
    block = poly([(3, 16), (9, 16), (9, 19.5), (15, 19.5), (15, 16), (21, 16), (21, 21.5), (3, 21.5)], closed=True, r=S.r * 0.5)
    return [
        shell(poly([(8.5, 2), (15.5, 2), (14.5, 11), (9.5, 11)], closed=True, r=S.r)),
        line(seg(12, 11, 12, 15.5)),
        dot(12, 17.75, 1.5),
        shell(block),
    ]


@icon("perfboard", CAT, "Square prototyping board filled with a grid of holes.",
      tags=["perf board", "protoboard", "prototype board", "dot board", "pcb", "holes", "diy electronics"])
def _(S):
    holes = [pip(S, x, y, 2) for x in (6.75, 10.25, 13.75, 17.25) for y in (6.75, 10.25, 13.75, 17.25)]
    return [shell(rect(3, 3, 18, 18, rr(S, 3))), *holes]


@icon("breakout-board", CAT, "Small breakout board with one chip in the middle and a row of pins along one edge.",
      tags=["breakout", "module", "adapter board", "sensor board", "pin header", "pcb"])
def _(S):
    pins = [line(seg(x, 17, x, 21.5)) for x in (6, 10, 14, 18)]
    return [
        shell(rect(3, 2.5, 18, 14.5, rr(S, 2.5))),
        detail(rect(8.5, 6, 7, 7, L(S, 0, 1.5))),
        *pins,
    ]


@icon("development-board", CAT, "Long narrow microcontroller board with pins down both sides and a USB port at one end.",
      tags=["dev board", "microcontroller", "maker board", "prototyping", "usb", "pins", "embedded"])
def _(S):
    e = L(S, 3, 4)
    pins = [line(seg(e, y, 7, y)) for y in (10.5, 14, 17.5)] + [line(seg(17, y, 24 - e, y)) for y in (10.5, 14, 17.5)]
    return [
        shell(rect(7, 6, 10, 16, rr(S, 2.5))),
        shell(rect(9.5, 2, 5, 4, L(S, 0, 1))),
        sq(10.5, 12, 3, 4, L(S, 0, 0.6)),
        *pins,
    ]


def _chip_pins(S, lo, hi, ps):
    e = 3 if S.name == "rounded" else 2
    out = []
    for p in ps:
        out += [line(seg(p, e, p, lo)), line(seg(p, hi, p, 24 - e)), line(seg(e, p, lo, p)), line(seg(hi, p, 24 - e, p))]
    return out


@icon("fpga-chip", CAT, "Programmable logic chip with a grid of cells inside and pins all around.",
      tags=["fpga", "programmable logic", "gate array", "logic chip", "hardware", "asic"])
def _(S):
    cells = [sq(x, y, 2.5, 2.5, L(S, 0, 0.6)) for x in (8.5, 13) for y in (8.5, 13)]
    return [shell(rect(5.5, 5.5, 13, 13, rr(S, 2.5))), *cells, *_chip_pins(S, 5.5, 18.5, (9.5, 14.5))]


@icon("system-on-chip", CAT, "Chip divided into several functional blocks, with pins around the edge.",
      tags=["soc", "system on a chip", "processor", "integrated", "mobile chip", "silicon"])
def _(S):
    return [
        shell(rect(5.5, 5.5, 13, 13, rr(S, 2.5))),
        detail(seg(11, 5.5, 11, 18.5)),
        detail(seg(11, 12, 18.5, 12)),
        *_chip_pins(S, 5.5, 18.5, (9, 15)),
    ]


@icon("silicon-die", CAT, "Bare silicon die with a central core and bond pads around its rim.",
      tags=["die", "wafer", "semiconductor", "bare chip", "bond pads", "silicon", "chip design"])
def _(S):
    pads = []
    for a in (6.25, 12, 17.75):
        pads += [pip(S, a, 6.25, 2), pip(S, a, 17.75, 2)]
    for a in (12,):
        pads += [pip(S, 6.25, a, 2), pip(S, 17.75, a, 2)]
    return [shell(rect(2.5, 2.5, 19, 19, rr(S, 2))), detail(rect(9.5, 9.5, 5, 5, L(S, 0, 1))), *pads]


@icon("pcb-panel", CAT, "Panel of four identical circuit boards joined by break away tabs.",
      tags=["panelized pcb", "pcb array", "break away tabs", "mouse bites", "v score", "manufacturing"])
def _(S):
    out = []
    for x in (3, 14):
        for y in (3, 14):
            out += [shell(rect(x, y, 7, 7, L(S, 0.75, 2.5))), pip(S, x + 3.5, y + 3.5, 2)]
    tabs = [seg(10, 6.5, 14, 6.5), seg(10, 17.5, 14, 17.5), seg(6.5, 10, 6.5, 14), seg(17.5, 10, 17.5, 14)]
    return out + [line(t) for t in tabs]


@icon("smd-reel", CAT, "Reel of surface mount parts with the carrier tape trailing off.",
      tags=["component reel", "tape and reel", "smd", "smt", "pick and place", "carrier tape"])
def _(S):
    tape = rect(9, 16, 13, 5, L(S, 0, 1.5))
    return [
        shell(union(circle(9.5, 9.5, 7.5), tape)),
        detail(circle(9.5, 9.5, 2.5)) if S.name == "rounded" else detail(rect(7, 7, 5, 5)),
        pip(S, 14.5, 18.5, 2), pip(S, 18.5, 18.5, 2),
    ]


@icon("reflow-oven", CAT, "Conveyor reflow oven with a circuit board riding in and heat rising above.",
      tags=["reflow", "smt oven", "soldering oven", "conveyor", "pcb assembly", "heat"])
def _(S):
    return [
        line(squiggle(9, 6.5, 2, 1.3)), line(squiggle(15, 6.5, 2, 1.3)),
        shell(rect(6, 9, 16, 9.5, rr(S, 2))),
        detail(seg(9, 13.75, 19, 13.75)),
        line(seg(2, 18.5, 6, 18.5)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("solder-paste-stencil", CAT, "Thin metal stencil with a row of pad cutouts and a squeegee blade resting on it.",
      tags=["stencil", "solder paste", "squeegee", "smt", "pcb assembly", "paste printing"])
def _(S):
    holes = [sq(x, 15.5, 2, 3.5, L(S, 0, 0.5)) for x in (5.5, 9.5, 13.5, 17.5)]
    return [
        shell(rect(10, 2.5, 4, 6.5, L(S, 0, 1.5))),
        shell(rect(3.5, 9, 17, 3.5, L(S, 0, 1.5))),
        shell(rect(2, 12.5, 20, 9, rr(S, 2))),
        *holes,
    ]


@icon("solder-paste-syringe", CAT, "Solder paste syringe with a bent needle squeezing out a small dab.",
      tags=["solder paste", "flux syringe", "dispenser", "paste", "rework", "smd soldering"])
def _(S):
    return [
        line(seg(7.5, 2.5, 16.5, 2.5)),
        line(seg(12, 2.5, 12, 5)),
        shell(rect(8.5, 5, 7, 10, rr(S, 1.5))),
        detail(seg(8.5, 8.5, 12, 8.5)),
        line(poly([(12, 15), (12, 18.5), (14.5, 21)], r=S.r)),
        dot(18.5, 20.5, 1.75),
    ]


@icon("etching-tank", CAT, "Tank of etching liquid with a circuit board hanging inside and bubbles rising.",
      tags=["pcb etching", "etchant", "ferric chloride", "bubble tank", "board making", "chemical"])
def _(S):
    wave = "M2 9Q5 7.5 8 9T14 9T20 9L22 9" if S.name == "rounded" else "M2 9L5 7.75L8 9L11 7.75L14 9L17 7.75L20 9L22 9"
    return [
        shell(rect(2, 4, 20, 18, rr(S, 2.5))),
        detail(wave),
        detail(rect(10, 12.5, 8, 6.5, L(S, 0, 1))),
        detail(seg(14, 9, 14, 12.5)),
        dot(6, 18.5, 1.1), dot(6, 13.5, 1.1),
    ]


@icon("pcb-holder", CAT, "Board holder with two clamp arms gripping the edges of a circuit board.",
      tags=["pcb vise", "board clamp", "helping hands", "soldering jig", "circuit board holder", "rework"])
def _(S):
    return [
        shell(rect(2, 5, 4.5, 10, rr(S, 1.5))),
        shell(rect(17.5, 5, 4.5, 10, rr(S, 1.5))),
        shell(rect(6.5, 6.5, 11, 7, L(S, 0, 1))),
        sq(10, 8.75, 4, 2.5, 0),
        line(seg(5, 15, 5, 18.5)), line(seg(19, 15, 19, 18.5)),
        shell(rect(2, 18.5, 20, 3.5, L(S, 0, 1.75))),
    ]


@icon("project-enclosure", CAT, "Plastic project box with screw holes in its corners and its lid lifted off.",
      tags=["project box", "enclosure", "case", "housing", "electronics box", "diy case"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 4, L(S, 0, 2))),
        shell(rect(3, 9, 18, 12.5, rr(S, 3))),
        pip(S, 6.75, 12.75, 2), pip(S, 17.25, 12.75, 2), pip(S, 6.75, 17.75, 2), pip(S, 17.25, 17.75, 2),
    ]


@icon("pcb-standoff", CAT, "Hexagonal threaded spacer with a screw stud at one end.",
      tags=["standoff", "spacer", "hex spacer", "pcb mount", "brass standoff", "mounting"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 9.5)),
        line(seg(L(S, 10, 10.5), 4.5, L(S, 14, 13.5), 4.5)),
        line(seg(L(S, 10, 10.5), 7.5, L(S, 14, 13.5), 7.5)),
        shell(poly([(6.5, 11), (7.5, 9.5), (16.5, 9.5), (17.5, 11), (17.5, 20), (16.5, 21.5), (7.5, 21.5), (6.5, 20)],
                   closed=True, r=S.r * 0.5)),
        detail(seg(10.25, 9.5, 10.25, 21.5)),
        detail(seg(13.75, 9.5, 13.75, 21.5)),
    ]


@icon("pcb-antenna", CAT, "Circuit board with a meandering zigzag copper antenna trace.",
      tags=["trace antenna", "meander antenna", "printed antenna", "wifi antenna", "rf", "pcb trace"])
def _(S):
    m = [(6, 21), (6, 6.5), (10, 6.5), (10, 16), (14, 16), (14, 6.5), (18, 6.5), (18, 16)]
    return [shell(rect(2, 2, 20, 20, rr(S, 2.5))), detail(poly(m, r=S.r * 0.8))]


@icon("rf-module", CAT, "Radio module board with a metal shield can and a coiled spring antenna.",
      tags=["radio module", "transceiver", "wireless module", "433 mhz", "spring antenna", "rf"])
def _(S):
    coil = [(15.5, 18.5), (19.5, 18.5), (19.5, 16), (21.5, 14), (17.5, 11), (21.5, 8), (17.5, 5), (19.5, 3.5), (19.5, 2)]
    return [
        shell(rect(2, 8, 13.5, 13.5, rr(S, 2.5))),
        detail(rect(5, 11, 7.5, 7.5, L(S, 0, 1))),
        line(poly(coil, r=S.r * 0.5)),
    ]


@icon("gps-module", CAT, "Small GPS board with a square ceramic patch antenna and signal arcs.",
      tags=["gps", "gnss", "satellite receiver", "patch antenna", "location module", "navigation"])
def _(S):
    return [
        shell(rect(2, 9.5, 12.5, 12.5, rr(S, 2.5))),
        detail(rect(5, 12.5, 6.5, 6.5, L(S, 0, 1))),
        line(arc(14.5, 9.5, 4, 270, 360)),
        line(arc(14.5, 9.5, 7.5, 270, 360)),
    ]


@icon("infrared-receiver", CAT, "Small infrared receiver with a domed lens on its face and three legs.",
      tags=["ir receiver", "ir sensor", "remote receiver", "infrared", "38 khz", "photodiode"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 11.5, rr(S, 3))),
        detail(circle(12, 8.25, 2.75)),
        line(seg(8, 14, 8, 21.5)), line(seg(12, 14, 12, 21.5)), line(seg(16, 14, 16, 21.5)),
    ]


@icon("real-time-clock-module", CAT, "Real time clock board with a coin cell battery holder and a clock chip.",
      tags=["rtc", "clock module", "coin cell", "timekeeping", "battery backup"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, rr(S, 2.5))),
        detail(circle(8.5, 12, 3.5)),
        dot(8.5, 12, 1.1),
        sq(15, 8.5, 4, 7, L(S, 0, 0.8)),
    ]


@icon("motor-driver-board", CAT, "Motor driver board with a tall finned heat sink and screw terminals.",
      tags=["motor driver", "h bridge", "stepper driver", "heat sink", "robotics"])
def _(S):
    fins = [line(seg(x, 2.5, x, 7)) for x in (7.5, 12, 16.5)]
    return [
        *fins,
        shell(union(rect(2, 10, 20, 11.5, rr(S, 2.5)), rect(6.5, 7, 11, 4, L(S, 0, 0.5)))),
        detail(seg(6, 13.5, 18, 13.5)),
        pip(S, 5.5, 17.5, 2), pip(S, 9.5, 17.5, 2), pip(S, 14.5, 17.5, 2), pip(S, 18.5, 17.5, 2),
    ]


@icon("relay-board", CAT, "Relay board with a row of boxed relays and screw terminals along one edge.",
      tags=["relay module", "relay", "switching", "home automation", "channel relay", "channel switch"])
def _(S):
    return [
        shell(rect(2, 2.5, 20, 19, rr(S, 2.5))),
        pip(S, 6, 6.25, 2), pip(S, 10, 6.25, 2), pip(S, 14, 6.25, 2), pip(S, 18, 6.25, 2),
        detail(rect(5.5, 10.5, 5, 7.5, L(S, 0, 1))),
        detail(rect(13.5, 10.5, 5, 7.5, L(S, 0, 1))),
    ]


@icon("breadboard-power-module", CAT, "Power module with a barrel jack whose pins plug into a breadboard rail.",
      tags=["breadboard power", "power supply module", "barrel jack", "3.3v 5v", "prototyping", "rail"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 10.5, rr(S, 2.5))),
        detail(circle(8, 7.75, 2.25)),
        sq(14, 6, 3.5, 3.5, L(S, 0, 0.8)),
        line(seg(7, 13, 7, 18.5)), line(seg(17, 13, 17, 18.5)),
        shell(rect(2, 18.5, 20, 3.5, L(S, 0, 1.75))),
    ]


@icon("usb-to-serial-adapter", CAT, "Small adapter board with a USB plug at one end and a row of pins at the other.",
      tags=["usb serial", "uart", "usb to ttl", "serial adapter", "programmer"])
def _(S):
    body = union(rect(2, 8.5, 8, 7, L(S, 0, 1)), rect(8, 5.5, 10.5, 13, rr(S, 2.5)))
    pins = [line(seg(18.5, y, L(S, 22, 21), y)) for y in (8.5, 12, 15.5)]
    return [shell(body), sq(3.5, 11, 3, 2, 0), sq(11, 9.5, 4, 5, L(S, 0, 0.8)), *pins]


@icon("debug-probe", CAT, "Debug probe box with a flat ribbon cable ending in a pin connector.",
      tags=["debugger", "jtag", "swd", "programmer", "ribbon cable", "embedded", "in circuit debugger"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 11, 9, rr(S, 2.5))),
        dot(6, 7, 1.25),
        shell(thick("M9 11.5V14.5Q9 17.5 12 17.5H14", 4, S)),
        shell(rect(14, 14.5, 7.5, 6, L(S, 0, 1.5))),
        pip(S, 17.75, 17.5, 2),
    ]


@icon("chip-programmer", CAT, "Chip programmer box with a lever socket on top holding a chip.",
      tags=["eprom programmer", "zif socket", "device programmer", "flash chip", "burner", "universal programmer"])
def _(S):
    return [
        shell(rect(4, 5.5, 11, 5.5, L(S, 0, 1.5))),
        sq(7, 7.5, 5, 1.5, 0),
        line(poly([(18.5, 11), (18.5, 4), (21, 4)], r=S.r)),
        shell(rect(2, 11, 20, 10.5, rr(S, 2.5))),
        dot(6, 16.25, 1.25), dot(10, 16.25, 1.25),
        detail(seg(13.5, 16.25, 18.5, 16.25)),
    ]


# ============================================================================ sensors and modules

@icon("el-wire", CAT, "Glowing electroluminescent wire looping out of a small battery pack.",
      tags=["electroluminescent wire", "glow wire", "neon wire", "light wire", "costume lighting", "cosplay"])
def _(S):
    return [
        shell(rect(2.5, 14, 7.5, 8, rr(S, 2))),
        detail(seg(5, 18, 7.5, 18)),
        line("M6.25 14V11C6.25 7 8.5 5 12.5 5"),
        line(circle(13.5, 9, 4)),
        line(seg(*pt(13.5, 9, 6.25, -25), *pt(13.5, 9, 8.25, -25))),
        line(seg(*pt(13.5, 9, 6.25, 20), *pt(13.5, 9, 8.25, 20))),
        line(seg(*pt(13.5, 9, 6.25, 65), *pt(13.5, 9, 8.25, 65))),
    ]


@icon("humidity-sensor", CAT, "Small humidity sensor box with a grid of vents on its face and three pins.",
      tags=["humidity", "hygrometer", "moisture in air", "climate sensor", "temperature humidity"])
def _(S):
    vents = [pip(S, x, y, 2) for x in (8.5, 12, 15.5) for y in (6.25, 10.25)]
    return [
        shell(rect(5, 2.5, 14, 12, rr(S, 2))),
        *vents,
        line(seg(8, 14.5, 8, 21.5)), line(seg(12, 14.5, 12, 21.5)), line(seg(16, 14.5, 16, 21.5)),
    ]


@icon("gas-sensor", CAT, "Round gas sensor with a mesh dome cap, mounted on a small board.",
      tags=["gas detector", "air quality", "smoke sensor", "gas module", "co2", "methane", "fumes"])
def _(S):
    cap = "M5.5 16.5V10.5A6.5 6.5 0 0 1 18.5 10.5V16.5Z"
    body = union(cap, rect(2, 16.5, 20, 5, L(S, 0, 1.75)))
    return [
        shell(body),
        detail(seg(9.5, 5, 9.5, 16.5)), detail(seg(14.5, 5, 14.5, 16.5)),
        detail(seg(5.5, 11, 18.5, 11)),
        detail(seg(5.5, 16.5, 18.5, 16.5)),
    ]


@icon("accelerometer", CAT, "Sensor chip with three axis arrows pointing up, right and diagonally.",
      tags=["acceleration", "motion", "tilt", "imu", "three axis", "g force", "orientation"])
def _(S):
    return [
        shell(rect(2.5, 12.5, 9, 9, rr(S, 2))),
        line(seg(7, 12.5, 7, 3.5)), line(poly([(4.5, 6), (7, 3.5), (9.5, 6)], r=S.r * 0.4)),
        line(seg(11.5, 17, 20.5, 17)), line(poly([(18, 14.5), (20.5, 17), (18, 19.5)], r=S.r * 0.4)),
        line(seg(11.5, 12.5, 19.5, 4.5)), line(poly([(15.75, 4.5), (19.5, 4.5), (19.5, 8.25)], r=S.r * 0.4)),
    ]


@icon("magnetometer", CAT, "Sensor chip with a compass needle drawn on top.",
      tags=["compass sensor", "magnetic field", "heading", "e compass", "magnetic sensor", "orientation"])
def _(S):
    ax, pp = (0.7071, -0.7071), (0.7071, 0.7071)
    h, w = 5.2, 1.9
    tipn = (12 + ax[0] * h, 12 + ax[1] * h)
    tips = (12 - ax[0] * h, 12 - ax[1] * h)
    s1 = (12 + pp[0] * w, 12 + pp[1] * w)
    s2 = (12 - pp[0] * w, 12 - pp[1] * w)
    return [
        shell(rect(5, 5, 14, 14, rr(S, 2.5))),
        mark(poly([tipn, s1, tips, s2], closed=True, r=S.r * 0.4)),
        *_chip_pins(S, 5, 19, (9, 15)),
    ]


@icon("hall-effect-sensor", CAT, "Flat three legged hall sensor beside a bar magnet, with a field line between them.",
      tags=["hall sensor", "magnetic switch", "magnet sensor", "proximity", "rpm sensor", "position"])
def _(S):
    return [
        line("M19 6.5C19 2.5 8 2 8 8"),
        shell(rect(2.5, 10, 11, 5.5, rr(S, 1.5))),
        line(seg(4.5, 15.5, 4.5, 21.5)), line(seg(8, 15.5, 8, 21.5)), line(seg(11.5, 15.5, 11.5, 21.5)),
        shell(rect(16.5, 8.5, 5.5, 13, rr(S, 1.5))),
        mark(rect(16.5, 8.5, 5.5, 6.5, 0) if S.name == "line" else "M16.5 15V10A1.5 1.5 0 0 1 18 8.5H20.5A1.5 1.5 0 0 1 22 10V15Z"),
    ]


@icon("flex-sensor", CAT, "Long thin flex sensor strip bent in a gentle curve, with two pins at one end.",
      tags=["bend sensor", "flex", "flexion", "glove sensor", "strain", "wearable"])
def _(S):
    return [
        shell(thick("M6.75 16.5C6.75 10 11 5 20 4", 5, S)),
        line(seg(5.25, 16.5, 5.25, 21.5)), line(seg(8.75, 16.5, 8.75, 21.5)),
    ]


@icon("force-sensor", CAT, "Round force sensing pad on a thin tail ending in two pins.",
      tags=["fsr", "pressure pad", "force sensitive resistor", "touch pressure", "weight", "squeeze"])
def _(S):
    return [
        shell(union(circle(12, 8.5, 6.5), rect(9, 13, 6, 5.5, L(S, 0, 1)))),
        detail(circle(12, 8.5, 2.75)) if S.name == "rounded" else detail(rect(9.25, 5.75, 5.5, 5.5)),
        line(seg(10, 18.5, 10, 22)), line(seg(14, 18.5, 14, 22)),
    ]


@icon("load-cell", CAT, "Rectangular load cell bar with a hole through its middle and a cable out one end.",
      tags=["weight sensor", "strain gauge", "scale sensor", "force", "weighing", "load sensor"])
def _(S):
    return [
        shell(rect(2, 7, 15, 10, rr(S, 2))),
        detail(rect(5.5, 10.5, 8, 3, 1.5 if S.name == "rounded" else 0)),
        line("M17 12H19Q21 12 21 14V20" if S.name == "rounded" else "M17 12H21V20"),
    ]


@icon("pressure-sensor", CAT, "Pressure transducer: a round sensor body on a threaded fitting with a cable out the top.",
      tags=["pressure transducer", "pressure transmitter", "barometric", "hydraulic", "pneumatic", "psi"])
def _(S):
    body = union(rect(6, 5, 12, 8.5, rr(S, 3)), rect(8, 13, 8, 4, 0), rect(10, 16.5, 4, 5, L(S, 0, 1)))
    return [
        line(seg(12, 1.75, 12, 5)),
        shell(body),
        detail(seg(8, 13.5, 16, 13.5)),
        detail(seg(10, 17, 14, 17)),
    ]


@icon("rain-sensor", CAT, "Rain sensor board with two interlocking comb traces and raindrops falling on it.",
      tags=["rain detector", "raindrop sensor", "water sensor", "weather", "wet", "moisture"])
def _(S):
    return [
        shell(drop(7.5, 2, 8.5, S)), shell(drop(16.5, 2, 8.5, S)),
        shell(rect(2, 11, 20, 10.5, rr(S, 2))),
        detail(seg(6, 11, 6, 17.5)), detail(seg(14, 11, 14, 17.5)),
        detail(seg(10, 21.5, 10, 15)), detail(seg(18, 21.5, 18, 15)),
    ]


@icon("sound-sensor", CAT, "Small sound sensor board with a round microphone capsule, a trim screw and sound waves.",
      tags=["microphone module", "sound detector", "noise sensor", "clap sensor", "audio", "decibel"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        detail(rect(9.5, 5, 5, 7.5, L(S, 1, 2.5))),
        detail("M7.25 11A4.75 4.75 0 0 0 16.75 11"),
        detail(seg(12, 15.75, 12, 18.5)),
    ]


@icon("color-sensor", CAT, "Colour sensor board with a central sensor chip surrounded by four small lights.",
      tags=["colour sensor", "rgb sensor", "light sensor", "color detection", "colour"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        sq(10, 10, 4, 4, L(S, 0, 0.8)),
        dot(12, 6.75, 1.5), dot(17.25, 12, 1.5), dot(12, 17.25, 1.5), dot(6.75, 12, 1.5),
    ]


@icon("image-sensor", CAT, "Image sensor chip with a glass window showing a grid of pixels.",
      tags=["camera sensor", "cmos", "ccd", "sensor chip", "pixels", "photography"])
def _(S):
    e = L(S, 2, 3)
    pins = []
    for y in (8.5, 12, 15.5):
        pins += [line(seg(e, y, 5, y)), line(seg(19, y, 24 - e, y))]
    px = [sq(x, y, 3, 3, L(S, 0, 0.6)) for x in (8.5, 12.5) for y in (8.5, 12.5)]
    return [shell(rect(5, 5, 14, 14, rr(S, 2.5))), *px, *pins]


@icon("water-level-sensor", CAT, "Thin water level sensor board with parallel traces, dipped into wavy water.",
      tags=["water level", "liquid level", "tank sensor", "depth sensor", "flood", "water detector"])
def _(S):
    if S.name == "rounded":
        waves = [f"M2 {y}Q4.5 {y - 2} 7 {y}T12 {y}T17 {y}T22 {y}" for y in (17.5, 21)]
    else:
        waves = [f"M2 {y}L4.5 {y - 1.5}L7 {y}L9.5 {y - 1.5}L12 {y}L14.5 {y - 1.5}L17 {y}L19.5 {y - 1.5}L22 {y}" for y in (17.5, 21)]
    return [
        shell(rect(7.5, 2, 9, 11.5, rr(S, 2))),
        detail(seg(10.5, 5, 10.5, 13.5)), detail(seg(13.5, 5, 13.5, 13.5)),
        *[line(w) for w in waves],
    ]


def _flame2(S):
    top = "M17.5 3.5" if S.name == "line" else "M17.3 3.7Q17.5 3.4 17.7 3.7"
    return (top + "C18.5 6.5 21.5 8.5 21.5 12.25A3.75 3.75 0 0 1 14 12.25C14 10.25 14.8 9 15.6 8.2"
            "C15.8 9.6 16.4 10.5 17.2 10.8C16.7 8.6 16.6 6 17.5 3.5Z")


@icon("flame-sensor", CAT, "Flame sensor board with a dark round infrared receiver facing a small flame.",
      tags=["fire sensor", "flame detector", "ir flame", "fire alarm", "heat", "burner"])
def _(S):
    return [
        shell(rect(2, 10, 9.5, 11.5, rr(S, 2))),
        dot(6.75, 15.75, 2.25),
        shell(_flame2(S)),
    ]


@icon("current-transformer", CAT, "Split ring current clamp around a cable, with two output leads.",
      tags=["ct clamp", "current sensor", "split core", "energy monitor", "amps", "clamp meter sensor"])
def _(S):
    return [
        shell(thick(arc(12, 10, 5.5, 300, 240), 3.5, S)),
        dot(12, 10, 1.75),
        line(seg(9.5, 15.5, 9.5, 21.5)), line(seg(14.5, 15.5, 14.5, 21.5)),
    ]


@icon("keypad-matrix", CAT, "Flat membrane keypad with a grid of keys and a ribbon tail.",
      tags=["membrane keypad", "matrix keypad", "keypad", "keys", "input", "pin pad", "4x4 keypad"])
def _(S):
    keys = [pip(S, x, y, 2) for x in (6.75, 10.25, 13.75, 17.25) for y in (6, 9.5, 13)]
    return [
        shell(union(rect(3, 2.5, 18, 14, rr(S, 2)), rect(9, 16, 6, 6, L(S, 0, 1)))),
        *keys,
        detail(seg(12, 18.5, 12, 22)),
    ]


@icon("spectrum-analyzer", CAT, "Instrument screen showing sharp peaks above a baseline, with knobs beside it.",
      tags=["spectrum", "rf analyzer", "frequency analysis", "signal analyzer", "fft", "test equipment"])
def _(S):
    peaks = [(4.5, 16.5), (6, 16.5), (7.5, 8), (9, 16.5), (10.25, 16.5), (11.5, 11.5), (12.75, 16.5), (14, 16.5)]
    return [
        shell(rect(2, 4, 20, 16, rr(S, 2.5))),
        detail(poly(peaks, r=S.r * 0.3), stroke_miterlimit="10"),
        detail(seg(16, 4, 16, 20)),
        dot(19, 8.5, 1.25), dot(19, 13, 1.25),
    ]


@icon("lcr-meter", CAT, "Handheld LCR meter with a coil symbol on its display and two clip leads.",
      tags=["lcr", "inductance meter", "capacitance meter", "component tester", "impedance", "test equipment"])
def _(S):
    coil = "M5.25 8.5A1.25 1.25 0 0 1 7.75 8.5A1.25 1.25 0 0 1 10.25 8.5A1.25 1.25 0 0 1 12.75 8.5"
    return [
        shell(rect(2.5, 2.5, 12.5, 19, rr(S, 2.5))),
        detail(coil),
        detail(circle(8.75, 15.5, 2.25)),
        line(seg(15, 7, 18.5, 7)), line(poly([(22, 4.5), (18.5, 7), (22, 9.5)], r=S.r * 0.4)),
        line(seg(15, 15, 18.5, 15)), line(poly([(22, 12.5), (18.5, 15), (22, 17.5)], r=S.r * 0.4)),
    ]


@icon("frequency-counter", CAT, "Bench frequency counter with a long row of digits and a round input connector.",
      tags=["frequency meter", "counter", "hertz", "hz", "timer counter", "test equipment"])
def _(S):
    digits = [sq(x, 7.5, 2, 4.5, L(S, 0, 0.5)) for x in (5, 8.5, 12, 15.5)]
    return [
        shell(rect(2, 4, 20, 16, rr(S, 2.5))),
        *digits,
        pip(S, 6, 16, 2), pip(S, 10, 16, 2),
        detail(circle(17, 15.5, 1.75)),
    ]


@icon("insulation-tester", CAT, "Handheld insulation tester with a large dial and a lightning bolt warning mark.",
      tags=["megohmmeter", "insulation resistance", "high voltage", "electrician", "test equipment"])
def _(S):
    bolt = [(13, 13.5), (10, 17.5), (12, 17.5), (11, 20.5), (14, 16.5), (12, 16.5)]
    return [
        shell(rect(4, 2, 16, 20, rr(S, 3))),
        detail(arc(12, 11, 5, 200, 340)),
        detail(seg(12, 10.5, 14.75, 7)),
        mark(poly(bolt, closed=True, r=S.r * 0.2)),
    ]


@icon("test-leads", CAT, "Pair of pointed test probes joined by their lead wires.",
      tags=["probe leads", "multimeter leads", "banana plug", "test probes", "wires", "measurement"])
def _(S):
    out = []
    for x in (6.5, 17.5):
        out += [
            shell(poly([(x, 2), (x + 1.75, 5.5), (x - 1.75, 5.5)], closed=True, r=S.r * 0.3), stroke_miterlimit="3"),
            shell(rect(x - 1.75, 5.5, 3.5, 8, L(S, 0, 1.25))),
            detail(seg(x - 1.75, 9, x + 1.75, 9)),
        ]
    out.append(line("M6.5 13.5V16.5A5 5 0 0 0 11.5 21.5H12.5A5 5 0 0 0 17.5 16.5V13.5" if S.name == "rounded"
                    else "M6.5 13.5V21.5H17.5V13.5"))
    return out


@icon("oscilloscope-probe", CAT, "Slim oscilloscope probe with a hook tip and a short ground clip lead.",
      tags=["scope probe", "10x probe", "hook tip", "ground clip", "oscilloscope", "measurement"])
def _(S):
    f = Frame(TILT, -1.25, 0.5)
    return [
        line(f.path([("M", (12, 8)), ("L", (12, 5)), ("A", 1.75, 0, 0, (8.5, 5)), ("L", (8.5, 5.5))])),
        shell(f.rect(9.5, 8, 5, 10, rr(S, 2))),
        detail(f.seg(9.5, 11, 14.5, 11)),
        line(f.seg(12, 18, 12, 20)),
        line(f.path([("M", (14.5, 13.5)), ("L", (18, 13.5)), ("L", (18, 15))])),
        line(f.poly([(16.5, 18), (18, 15), (19.5, 18)], closed=False, r=S.r * 0.4)),
    ]


@icon("logic-probe", CAT, "Pen shaped logic probe with two indicator lights and a clip lead.",
      tags=["logic tester", "digital probe", "high low", "ttl", "cmos", "debugging"])
def _(S):
    f = Frame(TILT, -1, 1)
    return [
        line(f.seg(12, 2, 12, 6)),
        shell(f.rect(9, 6, 6, 12, rr(S, 3))),
        f.dot(12, 9.75, 1.25), f.dot(12, 13.75, 1.25),
        line(f.path([("M", (12, 18)), ("L", (12, 19.5)), ("Q", (12, 21), (13.5, 21)), ("L", (16.5, 21))])),
    ]


@icon("test-lamp", CAT, "Test lamp with a long pointed metal probe and a clear handle holding a small bulb.",
      tags=["voltage tester", "test light", "circuit tester", "12v tester", "automotive", "electrician"])
def _(S):
    f = Frame(TILT, -1, 1)
    return [
        line(f.seg(12, 1.5, 12, 8)),
        shell(f.rect(8.5, 8, 7, 11.5, rr(S, 2.5))),
        detail(f.circle(12, 12.5, 1.75)),
        detail(f.seg(12, 14.25, 12, 16.5)),
        line(f.seg(12, 19.5, 12, 21.5)),
    ]


@icon("electronic-load", CAT, "Bench electronic load with a large fan vent, a display and a knob.",
      tags=["dc load", "dummy load", "load tester", "battery tester", "power testing", "test equipment"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, rr(S, 2.5))),
        detail(circle(8, 12, 4)),
        dot(8, 12, 1.25),
        sq(14.5, 7.5, 5, 3, L(S, 0, 0.6)),
        detail(circle(17, 15, 1.75)),
    ]


@icon("wattmeter", CAT, "Round analog wattmeter with a needle and a W below the pivot.",
      tags=["watt meter", "power meter", "watts", "analog meter", "energy", "power measurement"])
def _(S):
    w = [(7.5, 14), (9.25, 17.5), (12, 14.75), (14.75, 17.5), (16.5, 14)]
    return [
        shell(circle(12, 12, 9)),
        detail(seg(12, 11, 16, 6.5)),
        dot(12, 11, 1.25),
        detail(poly(w, r=S.r * 0.3)),
    ]


# ============================================================================ static control

@icon("esd-wrist-strap", CAT, "Anti static wrist band with a coiled ground cord ending in a clip.",
      tags=["esd strap", "anti static strap", "grounding strap", "static discharge", "wristband", "ground"])
def _(S):
    a, b = (9.5, 12.5), (16.5, 18.5)
    dx, dy = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux
    pts = [a]
    n = 6
    for k in range(1, n):
        t = k / n * ln
        sgn = 1.6 if k % 2 else -1.6
        pts.append((a[0] + ux * t + nx * sgn, a[1] + uy * t + ny * sgn))
    pts.append(b)
    return [
        line(ellipse(8, 6.5, 5.5, 4)),
        dot(8.5, 10.5, 1.9),
        line(poly(pts, r=S.r * 0.4)),
        shell(poly([(16, 17.5), (21.5, 15.5), (22, 18.5), (18.5, 21.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("anti-static-bag", CAT, "Resealable anti static bag with a crossed out warning triangle.",
      tags=["esd bag", "static shielding bag", "antistatic", "component bag", "packaging", "static safe"])
def _(S):
    return [
        shell(rect(4, 2, 16, 20, rr(S, 2))),
        detail(seg(4, 6.25, 20, 6.25)),
        detail(poly([(12, 9.5), (17, 18.5), (7, 18.5)], closed=True, r=S.r * 0.4)),
        dot(12, 15.5, 1.5),
    ]


@icon("anti-static-mat", CAT, "Anti static work mat with a snap stud in one corner and a cord to a ground symbol.",
      tags=["esd mat", "grounding mat", "antistatic mat", "workbench", "static safe", "ground"])
def _(S):
    return [
        shell(poly([(6.5, 3), (22, 3), (17.5, 12.5), (2, 12.5)], closed=True, r=S.r * 0.6)),
        dot(16.5, 6.25, 1.5),
        line(seg(6.5, 12.5, 6.5, 15.5)),
        line(seg(2.5, 15.5, 10.5, 15.5)),
        line(seg(4, 18.75, 9, 18.75)),
        line(seg(5.5, 22, 7.5, 22)),
    ]


def _(S):
    return [
        shell(rect(2, 2.5, 20, 11, rr(S, 2))),
        dot(17.75, 9, 1.5),
        line(seg(17.75, 13.5, 17.75, 16.5)),
        line(seg(13.5, 16.5, 22, 16.5)),
        line(seg(15, 19.5, 20.5, 19.5)),
        dot(17.75, 22, 1),
    ]


# ============================================================================ charts and diagrams

@icon("smith-chart", CAT, "Smith chart: a circle filled with arcs and circles that meet at its right edge.",
      tags=["impedance chart", "rf design", "matching", "reflection coefficient", "transmission line", "vswr"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(seg(3, 12, 21, 12)),
        detail(circle(16.5, 12, 4.5)),
        detail(arc(21, 3, 9, 90, 180)),
        detail(arc(21, 21, 9, 180, 270)),
        pip(S, 8, 8, 3) if S.name == "line" else dot(8, 8, 1.5),
    ]


@icon("bode-plot", CAT, "Bode plot: two stacked graphs, gain flat then falling above and phase dropping below.",
      tags=["frequency response", "gain", "phase", "filter", "control systems", "magnitude plot"])
def _(S):
    return [
        line(seg(3, 2, 3, 22)),
        line(seg(3, 11, 21.5, 11)),
        line(seg(3, 21, 21.5, 21)),
        line("M6 4.5H10.5Q13 4.5 20.5 8.5" if S.name == "rounded" else "M6 4.5H11.5L20.5 8.5"),
        line("M6 14H9C13 14 13 18.25 17 18.25H20.5" if S.name == "rounded" else "M6 14H10L15 18.25H20.5"),
    ]


@icon("eye-diagram", CAT, "Eye diagram: overlapping signal traces crossing to leave an open eye in the middle.",
      tags=["eye pattern", "signal integrity", "jitter", "serial data", "oscilloscope", "high speed"])
def _(S):
    if S.name == "rounded":
        t1 = "M2 6.5H4C7 6.5 7 17.5 10 17.5H14C17 17.5 17 6.5 20 6.5H22"
        t2 = "M2 17.5H4C7 17.5 7 6.5 10 6.5H14C17 6.5 17 17.5 20 17.5H22"
    else:
        t1 = "M2 6.5H4L8.5 17.5H15.5L20 6.5H22"
        t2 = "M2 17.5H4L8.5 6.5H15.5L20 17.5H22"
    return [line(t1), line(t2)]


@icon("timing-diagram", CAT, "Timing diagram: stacked square pulse traces lined up in time.",
      tags=["waveform", "digital signals", "clock", "logic analyzer", "protocol", "square wave"])
def _(S):
    r = S.r * 0.4
    t1 = [(2, 7), (4.5, 7), (4.5, 3), (8.5, 3), (8.5, 7), (12.5, 7), (12.5, 3), (16.5, 3), (16.5, 7), (20.5, 7), (20.5, 3), (22, 3)]
    t2 = [(2, 14.5), (6.5, 14.5), (6.5, 10.5), (14.5, 10.5), (14.5, 14.5), (22, 14.5)]
    t3 = [(2, 18), (10.5, 18), (10.5, 22), (18.5, 22), (18.5, 18), (22, 18)]
    return [line(poly(t1, r=r)), line(poly(t2, r=r)), line(poly(t3, r=r))]


# ============================================================================ soldering and rework

@icon("desoldering-pump", CAT, "Desoldering pump: a long plunger tube with a pointed nozzle and a release button.",
      tags=["solder sucker", "solder pump", "desolder", "vacuum pump", "rework", "solder removal"])
def _(S):
    f = Frame(TILT, -0.5, 0.5)
    return [
        shell(f.poly([(11.25, 1.5), (12.75, 1.5), (13.5, 5.5), (10.5, 5.5)], r=S.r * 0.3)),
        shell(union(f.rect(9, 5.5, 6, 12, rr(S, 1.5)), f.rect(14, 8, 2.5, 3, L(S, 0, 1)))),
        line(f.seg(12, 17.5, 12, 20.5)),
        line(f.seg(9.5, 21, 14.5, 21)),
    ]


@icon("desoldering-braid", CAT, "Small spool of flat braided copper wick with a length hanging down.",
      tags=["solder wick", "desoldering wick", "copper braid", "rework", "solder removal", "spool"])
def _(S):
    band = rect(12.5, 8, 5, 14, L(S, 0, 1.5))
    hatch = [seg(12.5, y + 1.5, 17.5, y - 1.5) for y in (15, 19)]
    return [
        shell(union(circle(9.5, 8.5, 6.5), band)),
        detail(circle(9.5, 8.5, 2)) if S.name == "rounded" else detail(rect(7.5, 6.5, 4, 4)),
        *[detail(h) for h in hatch],
    ]


def _(S):
    band = thick("M14 10.5L20 20", 4.5, S)
    hatch = [seg(*pt(x, y, 1.6, 148), *pt(x, y, 1.6, 328)) for x, y in ((16.25, 14.5), (18.25, 17.8))]
    return [
        shell(union(circle(9, 9, 6.5), band)),
        detail(circle(9, 9, 2)) if S.name == "rounded" else detail(rect(7, 7, 4, 4)),
        *[detail(h) for h in hatch],
    ]


def helix(a, b, turns, R, r2, per=14):
    """Side view of a coil spring along a to b: loops of radius R across the axis, r2 along it."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux
    pts = []
    n = turns * per
    for k in range(n + 1):
        t = k / n
        th = 2 * math.pi * turns * t
        along = t * ln + r2 * math.sin(th)
        across = R * math.cos(th)
        pts.append((a[0] + ux * along + nx * across, a[1] + uy * along + ny * across))
    return "M" + "L".join(f"{fmt(x)} {fmt(y)}" for x, y in pts)


@icon("soldering-iron-stand", CAT, "Spiral coil holder for a soldering iron on a base with a sponge tray.",
      tags=["iron holder", "soldering stand", "iron rest", "sponge", "soldering station", "workbench"])
def _(S):
    return [
        line(helix((14, 14.5), (20, 3), 3, 2.5, 1.25, 16)),
        line(seg(14, 14.5, 14, 18)),
        shell(rect(2, 18, 20, 3.5, L(S, 0, 1.75))),
        shell(rect(3, 12.5, 7.5, 5.5, L(S, 0.5, 2))),
        dot(6.75, 15.25, 1),
    ]


def _(S):
    a, b = (13.5, 18), (20.5, 4)
    dx, dy = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux
    pts = [a]
    n = 7
    for k in range(1, n):
        t = k / n * ln
        sgn = 2 if k % 2 else -2
        pts.append((a[0] + ux * t + nx * sgn, a[1] + uy * t + ny * sgn))
    pts.append(b)
    return [
        line(poly(pts, r=S.r * 0.4)),
        shell(rect(2, 18, 20, 3.5, L(S, 0, 1.75))),
        shell(rect(3, 12.5, 7.5, 5.5, L(S, 0.5, 2))),
        dot(6.75, 15.25, 1),
    ]


@icon("tip-cleaner", CAT, "Round tip cleaner cup filled with coiled brass wool.",
      tags=["brass wool", "tip cleaning", "soldering tip", "brass sponge", "soldering", "cleaner"])
def _(S):
    return [
        line(circle(8, 10, 3)), line(circle(16, 10, 3)), line(circle(12, 8, 3.5)),
        shell(poly([(3.5, 13), (20.5, 13), (18.5, 21.5), (5.5, 21.5)], closed=True, r=S.r)),
    ]


@icon("flux-pen", CAT, "Flux pen with a felt tip and a drop of flux falling from it.",
      tags=["flux", "flux marker", "soldering flux", "no clean flux", "rework", "soldering"])
def _(S):
    f = Frame(225, 1.5, -1.5)
    return [
        shell(f.poly([(10.5, 3), (13.5, 3), (14.5, 6), (9.5, 6)], r=S.r * 0.4)),
        shell(f.rect(8.5, 6, 7, 15, rr(S, 2))),
        detail(f.seg(8.5, 10.5, 15.5, 10.5)),
        shell(drop(4.5, 16, 22, S)),
    ]


@icon("hot-air-station", CAT, "Hot air rework station: a box with a display and a handheld hot air wand.",
      tags=["hot air gun", "rework station", "smd rework", "heat gun", "desoldering", "reflow"])
def _(S):
    return [
        shell(rect(2, 9, 12, 12.5, rr(S, 2))),
        sq(4.5, 11.5, 7, 3, L(S, 0, 0.6)),
        dot(5.5, 18, 1.25), dot(10.5, 18, 1.25),
        line(seg(19, 2.5, 19, 7)),
        shell(rect(16.5, 7, 5, 9.5, rr(S, 2.5))),
        line("M19 16.5V18.5Q19 20.5 17 20.5H14" if S.name == "rounded" else "M19 16.5V20.5H14"),
    ]


@icon("soldering-gun", CAT, "Pistol shaped soldering gun with a trigger and a loop shaped tip.",
      tags=["solder gun", "soldering pistol", "trigger", "heavy soldering", "wire joining", "soldering"])
def _(S):
    body = [(9, 5), (21, 5), (21, 12), (18.5, 12), (17.5, 20.5), (12.5, 20.5), (13.5, 12), (9, 12)]
    loop = "M9 7H4.75A1.75 1.75 0 0 0 4.75 10.5H9" if S.name == "rounded" else "M9 7H3V10.5H9"
    return [
        shell(poly(body, closed=True, r=S.r)),
        line(loop),
        line("M11 12V13.5Q11 15.5 12.5 15.5" if S.name == "rounded" else "M11 12V15.5H12.5"),
        detail(seg(11.5, 8.5, 18.5, 8.5)),
    ]


@icon("solder-joint", CAT, "Solder joint: a component lead through a board pad with a smooth cone of solder around it.",
      tags=["solder fillet", "through hole", "joint", "pad", "soldering", "pcb"])
def _(S):
    cone = "M5.5 15C9.5 15 10.25 11.5 10.75 8H13.25C13.75 11.5 14.5 15 18.5 15Z"
    return [
        line(seg(12, 2, 12, 8)),
        shell(cone),
        shell(rect(2, 15, 20, 4, L(S, 0, 1.5))),
        line(seg(12, 19, 12, 22)),
    ]


@icon("solder-pot", CAT, "Small solder pot on legs holding molten solder, with heat rising above.",
      tags=["solder bath", "tinning pot", "molten solder", "dip soldering", "heat", "soldering"])
def _(S):
    pot = "M4.5 9.5H19.5V13.5A5 5 0 0 1 14.5 18.5H9.5A5 5 0 0 1 4.5 13.5Z" if S.name == "rounded" else \
        "M4.5 9.5H19.5V15.5L16.5 18.5H7.5L4.5 15.5Z"
    return [
        line(squiggle(9, 7, 2, 1.2)), line(squiggle(15, 7, 2, 1.2)),
        shell(pot),
        detail(seg(4.5, 12.5, 19.5, 12.5)),
        line(seg(8, 18.5, 6.5, 22)), line(seg(16, 18.5, 17.5, 22)),
    ]


def hsquig(x0, x1, y, amp=1.3):
    m = (x0 + x1) / 2
    k = (x1 - x0) / 4
    return (f"M{fmt(x0)} {fmt(y)}C{fmt(x0 + k)} {fmt(y - amp * 1.3)} {fmt(m - k * 0.2)} {fmt(y - amp * 1.3)} {fmt(m)} {fmt(y)}"
            f"C{fmt(m + k * 0.2)} {fmt(y + amp * 1.3)} {fmt(x1 - k)} {fmt(y + amp * 1.3)} {fmt(x1)} {fmt(y)}")


@icon("fume-extractor", CAT, "Small fume extractor with a fan grille drawing in wisps of solder smoke.",
      tags=["fume absorber", "smoke absorber", "solder smoke", "extractor fan", "air filter", "ventilation"])
def _(S):
    return [
        line(hsquig(2, 7.5, 8)), line(hsquig(2, 7.5, 15)),
        shell(rect(10, 3, 12, 18, rr(S, 2.5))),
        detail(circle(16, 11.5, 3.75)),
        dot(16, 11.5, 1.25),
        detail(seg(12.5, 18, 19.5, 18)),
    ]


@icon("spudger", CAT, "Spudger: a thin prying stick with a flat tip at one end and a point at the other.",
      tags=["pry tool", "opening tool", "nylon spudger", "phone repair", "pry", "electronics repair"])
def _(S):
    f = Frame(TILT, 0, 0)
    return [shell(f.poly([(10, 2), (14, 2), (13.75, 7), (13.75, 16), (12, 22), (10.25, 16), (10.25, 7)], r=S.r * 0.6)),
            detail(f.seg(10.25, 7, 13.75, 7))]
