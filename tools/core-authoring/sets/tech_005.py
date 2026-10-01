"""TypeIcon Core: tech (batch 005): hardware parts, connectors, logic gates, storage media and computing concepts."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "tech"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle (knocked out of a Filled shell, like a dot)."""
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


def lead2(S, x1, y1, x2, y2):
    """Open stroke with both free ends kept inside the live area."""
    k = L(S, 0, 1)
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    return line(seg(x1 + ux * k, y1 + uy * k, x2 - ux * k, y2 - uy * k))


# --------------------------------------------------------------------------- chunk 1

@icon("liquid-cooling", CAT, "Radiator block joined by tubes to a round pump.",
      tags=["water cooling", "radiator", "pump", "coolant", "pc", "cooler"])
def _(S):
    return [shell(rect(2, 3, 9, 12, S.R)),
            detail(seg(6.5, 6, 6.5, 12)),
            shell(circle(17.5, 17.5, 4)),
            dot(17.5, 17.5, 1.2),
            line(poly([(11, 6.5), (17.5, 6.5), (17.5, 13.5)], r=S.r)),
            line(poly([(6.5, 15), (6.5, 17.5), (13.5, 17.5)], r=S.r))]


@icon("usb-flash-drive", CAT, "Thumb drive with a metal plug at one end and a keyring hole at the other.",
      tags=["usb stick", "thumb drive", "pen drive", "memory stick", "storage", "portable"])
def _(S):
    return [shell(rect(6, 9, 12, 13, rr(S, 3))),
            line(poly([(9.5, 9), (9.5, 3), (14.5, 3), (14.5, 9)], r=S.r)),
            detail(circle(12, 16.5, 2)),
            ]


@icon("external-hard-drive", CAT, "Rounded drive box with an activity light and a cable leading out.",
      tags=["portable drive", "backup drive", "storage", "hdd", "usb drive", "disk"])
def _(S):
    return [shell(rect(2, 4, 15, 15, S.R)),
            detail(seg(6, 8.5, 13, 8.5)),
            dot(6.5, 14.5, 1.3),
            line(poly([(17, 14), (20.5, 14), (20.5, 21)], r=S.r))]


@icon("memory-card-reader", CAT, "Small reader box with a memory card half inserted in its slot.",
      tags=["sd reader", "card reader", "flash card", "adapter", "usb", "storage"])
def _(S):
    return [shell(rect(2, 11, 20, 10, rr(S, 3))),
            line(poly([(8, 11), (8, 4), (14, 4), (17, 7), (17, 11)], r=S.r)),
            dot(18, 16, 1.2),
            detail(seg(6, 16, 12, 16))]


@icon("docking-station", CAT, "Laptop resting on a dock base with ports along its front.",
      tags=["laptop dock", "port replicator", "usb hub", "desk setup", "workstation"])
def _(S):
    return [shell(rect(6, 2.5, 12, 7, rr(S, 2))),
            line(seg(3, 12.5, 21, 12.5)),
            shell(rect(2, 16, 20, 5, rr(S, 2))),
            dot(15.5, 18.5, 1), dot(19, 18.5, 1),
            detail(seg(5, 18.5, 11, 18.5))]


@icon("kvm-switch", CAT, "Small switch box with a selector button wired to a monitor and a keyboard.",
      tags=["kvm", "keyboard video mouse", "switcher", "multi computer", "console switch"])
def _(S):
    return [shell(rect(2, 3, 8, 6, rr(S, 2))),
            shell(rect(14, 3, 8, 6, rr(S, 2))),
            detail(seg(17, 6, 19, 6)),
            shell(rect(6, 15, 12, 6, rr(S, 2))),
            dot(12, 18, 1.3),
            line(poly([(6, 9), (6, 12), (9, 12), (9, 15)], r=S.r)),
            line(poly([(18, 9), (18, 12), (15, 12), (15, 15)], r=S.r))]


@icon("blade-server", CAT, "Server chassis holding thin vertical blades side by side.",
      tags=["blade enclosure", "rack server", "data center", "chassis", "hosting"])
def _(S):
    return [shell(rect(2, 4, 20, 16, S.R)),
            detail(seg(7, 8, 7, 16)),
            detail(seg(12, 8, 12, 16)),
            detail(seg(17, 8, 17, 16))]


@icon("mainframe", CAT, "Tall computer cabinet with tape reels and a front panel.",
      tags=["big iron", "legacy computer", "enterprise computer", "tape drive", "cabinet"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail(seg(12, 3, 12, 21)),
            detail(circle(7.5, 8.5, 2.2)),
            detail(circle(16.5, 8.5, 2.2)),
            detail(seg(6, 16, 9, 16)),
            detail(seg(15, 16, 18, 16))]


@icon("supercomputer", CAT, "Three cabinets in a curved row, the outer two angled toward the viewer.",
      tags=["hpc", "high performance computing", "cluster", "compute", "science", "racks"])
def _(S):
    return [shell(rect(9, 4, 6, 16, rr(S, 1.5))),
            detail(seg(12, 8, 12, 12)),
            shell(poly([(6.5, 6), (2.5, 4), (2.5, 20), (6.5, 22 - 2)], closed=True, r=S.r * 0.6)),
            shell(poly([(17.5, 6), (21.5, 4), (21.5, 20), (17.5, 18)], closed=True, r=S.r * 0.6)),
            ]


@icon("quantum-computer", CAT, "Hanging tiers of plates joined by a central stem, like a quantum processor chandelier.",
      tags=["quantum", "dilution refrigerator", "chandelier", "qubits", "cryogenic"])
def _(S):
    return [line(seg(3, 3.5, 21, 3.5)),
            line(seg(6, 9, 18, 9)),
            line(seg(9, 14.5, 15, 14.5)),
            line(seg(12, 3.5, 12, 14.5)),
            line(poly([(7, 3.5), (7, 9)])), line(poly([(17, 3.5), (17, 9)])),
            shell(circle(12, 19, 2.2)) if S.name == "line" else shell(circle(12, 19, 2.2))]


@icon("qubit", CAT, "Sphere with an equator ring and an arrow pointing out from its centre.",
      tags=["bloch sphere", "quantum bit", "superposition", "quantum state", "physics"])
def _(S):
    k = L(S, 0, 0.5)
    ds = [shell(circle(12, 12, 9)),
          detail("M3 12A9 3.2 0 0 0 21 12"),
          detail(seg(12, 12, 15.5 - k, 8.5 + k)),
          Part("dot", poly([(17, 7), (13.6, 8.0), (16, 10.4)], closed=True, r=L(S, 0, 0.4)))]
    if S.name == "rounded":
        ds.append(dot(12, 12, 1.4))
    return ds


@icon("thin-client", CAT, "Slim box standing beside a small monitor.",
      tags=["terminal", "zero client", "virtual desktop", "diskless", "network computer"])
def _(S):
    return [shell(rect(2, 4, 12, 9, rr(S, 2))),
            line(seg(8, 13, 8, 17)),
            line(seg(4.5, 18.5, 11.5, 18.5)),
            shell(rect(18, 6, 3, 14, rr(S, 1))),
            ]


@icon("single-board-computer", CAT, "Compact board with a chip, a row of pins and ports on its edge.",
      tags=["maker board", "sbc", "dev board", "mini computer", "embedded", "maker"])
def _(S):
    return [shell(rect(2, 4, 20, 16, S.R)),
            detail(rect(5.5, 7.5, 6, 6, rr(S, 1))),
            dot(6, 17, 1), dot(9.5, 17, 1), dot(13, 17, 1),
            detail(poly([(22, 10.5), (17.5, 10.5), (17.5, 16.5), (22, 16.5)]))]


@icon("microcontroller", CAT, "Small chip with pins along its two long sides only.",
      tags=["mcu", "ic", "embedded", "dev kit", "chip", "dip"])
def _(S):
    return [shell(rect(6.5, 4, 11, 16, rr(S, 2))),
            dot(10, 7.5, 1.1),
            line(seg(2, 8, 6.5, 8)), line(seg(2, 12, 6.5, 12)), line(seg(2, 16, 6.5, 16)),
            line(seg(17.5, 8, 22, 8)), line(seg(17.5, 12, 22, 12)), line(seg(17.5, 16, 22, 16))]


@icon("breadboard", CAT, "Prototyping board with rows of tiny holes split by a centre channel.",
      tags=["prototyping", "solderless", "electronics", "maker", "circuit", "protoboard"])
def _(S):
    ds = [shell(rect(3, 3, 18, 18, S.R)), detail(seg(6, 12, 18, 12))]
    for y in (7, 17):
        for x in (7.5, 12, 16.5):
            ds.append(dot(x, y, 1.1))
    return ds


@icon("jumper-wire", CAT, "Flexible wire with a plastic housing and pin at each end.",
      tags=["breadboard wire", "patch wire", "connector", "prototyping", "cable", "lead"])
def _(S):
    return [solid(rect(4, 13, 4, 6, 0.6)), solid(rect(16, 5, 4, 6, 0.6)),
            line(seg(6, 19, 6, 22 - L(S, 0, 0))),
            line(seg(18, 2 + L(S, 0, 0), 18, 5)),
            line("M6 13C6 7 18 17 18 11")]


# --------------------------------------------------------------------------- chunk 2

@icon("pin-header", CAT, "Plastic strip with a row of short vertical metal pins.",
      tags=["header pins", "male header", "breakaway header", "connector", "electronics", "pcb"])
def _(S):
    return [shell(rect(2, 12, 20, 7, rr(S, 2.5))),
            line(seg(6, 3.5, 6, 12)), line(seg(10, 3.5, 10, 12)),
            line(seg(14, 3.5, 14, 12)), line(seg(18, 3.5, 18, 12))]


@icon("ribbon-cable", CAT, "Flat cable of parallel wires ending in a block connector.",
      tags=["flat cable", "ide cable", "multi wire", "data cable", "idc", "wiring"])
def _(S):
    return [line(seg(2, 8, 16, 8)), line(seg(2, 12, 16, 12)), line(seg(2, 16, 16, 16)),
            shell(rect(16, 4, 6, 16, rr(S, 2))),
            dot(19, 8, 1), dot(19, 12, 1), dot(19, 16, 1)]


@icon("sata-cable", CAT, "Thin data cable ending in a flat L shaped connector.",
      tags=["sata", "drive cable", "data cable", "hard drive cable", "ssd cable", "connector"])
def _(S):
    return [line(seg(2, 8, 8, 8)), line(seg(2, 14, 8, 14)),
            shell(poly([(8, 4), (15, 4), (15, 12), (22, 12), (22, 20), (8, 20)], closed=True, r=S.r)),
            detail(seg(11.5, 8, 11.5, 16))]


@icon("usb-c-connector", CAT, "Oval plug with a slim centre slot and a cable attached.",
      tags=["usb type c", "usbc", "plug", "charging cable", "data cable", "connector"])
def _(S):
    return [line(seg(2, 12, 9, 12)),
            shell(rect(9, 6.5, 13, 11, L(S, 3, 5.5))),
            detail(seg(13, 12, 18, 12))]


@icon("vga-connector", CAT, "Trapezoid video plug with rows of pins and a thumb screw on each side.",
      tags=["d-sub", "vga port", "analog video", "monitor cable", "15 pin", "legacy video"])
def _(S):
    ds = [shell(poly([(6, 5), (18, 5), (16.5, 18), (7.5, 18)], closed=True, r=S.r)),
          dot(3.2, 11.5, 1.4), dot(20.8, 11.5, 1.4)]
    for x in (9, 12, 15):
        ds.append(dot(x, 9, 1))
    for x in (10.2, 13.8):
        ds.append(dot(x, 12.2, 1))
    for x in (9.6, 12, 14.4):
        ds.append(dot(x, 15, 0.9))
    return ds


@icon("dvi-connector", CAT, "Wide video plug with a flat blade pin and a grid of pins.",
      tags=["dvi port", "digital video", "monitor cable", "display connector", "dvi-d"])
def _(S):
    ds = [shell(poly([(2, 6), (22, 6), (22, 15), (19.5, 18), (4.5, 18), (2, 15)], closed=True, r=S.r)),
          detail(seg(6, 9.5, 6, 14.5))]
    for x in (11.5, 15, 18.5):
        for y in (10, 14):
            ds.append(dot(x, y, 1))
    return ds


@icon("serial-port", CAT, "Flange plate holding a small trapezoid port with screw holes on each side.",
      tags=["rs-232", "com port", "db9", "d-sub", "legacy port", "serial connector"])
def _(S):
    return [shell(rect(2, 5, 20, 14, rr(S, 3))),
            detail(poly([(7.5, 9), (16.5, 9), (15, 15), (9, 15)], closed=True, r=S.r * 0.5)),
            dot(4.5, 12, 1), dot(19.5, 12, 1)]


@icon("ps2-port", CAT, "Round keyboard port with six pin holes and a key notch at the top.",
      tags=["ps/2", "keyboard port", "mouse port", "din", "legacy port", "mini din"])
def _(S):
    ds = [shell(circle(12, 12, 9)), detail(seg(12, 3, 12, 6.2))]
    for a in (0, 60, 120, 180, 240, 300):
        x, y = polar(12, 13, 4.6, a)
        ds.append(dot(x, y, 1))
    return ds


@icon("audio-jack-port", CAT, "Round socket with a centre hole and a headphone plug approaching it.",
      tags=["3.5mm", "headphone jack", "aux port", "audio socket", "mini jack", "plug"])
def _(S):
    return [shell(circle(6.5, 12, 4.6)), dot(6.5, 12, 1.3),
            line(seg(13.5, 12, 17.5, 12)),
            line(seg(15.5, 10, 15.5, 14)),
            shell(rect(17.5, 8.5, 4.5, 7, rr(S, 1.5)))]


@icon("gpio-pins", CAT, "Two rows of header pins along the edge of a board.",
      tags=["general purpose io", "header", "header strip", "pins", "expansion", "double row"])
def _(S):
    ds = [shell(rect(2, 6, 20, 12, S.R))]
    for x in (5.5, 9.25, 13, 16.75, 20.25 - 0.5):
        pass
    for x in (5.5, 9.5, 13.5, 17.5):
        ds.append(sq(x - 1.1, 8.9, 2.2, 2.2, 0.3)); ds.append(sq(x - 1.1, 12.9, 2.2, 2.2, 0.3))
    return ds


@icon("printed-circuit-board", CAT, "Board with copper traces ending in round pads around a chip.",
      tags=["pcb", "circuit board", "traces", "motherboard", "electronics", "layout"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R)),
            sq(9, 9, 6, 6, rr(S, 1)),
            detail(poly([(9, 12), (6, 12), (6, 8)], r=S.r * 0.5)), dot(6, 7, 1.2),
            detail(poly([(15, 12), (18, 12), (18, 16)], r=S.r * 0.5)), dot(18, 17, 1.2)]


@icon("transistor", CAT, "Half round plastic transistor body with three legs below.",
      tags=["bjt", "mosfet", "to-92", "semiconductor", "component", "amplifier"])
def _(S):
    r = L(S, 0, 1.5)
    if r:
        d = f"M5 10A7 7 0 0 1 19 10V{15 - r}A{r} {r} 0 0 1 {19 - r} 15H{5 + r}A{r} {r} 0 0 1 5 {15 - r}Z"
    else:
        d = "M5 10A7 7 0 0 1 19 10V15H5Z"
    return [shell(d),
            detail(seg(8.5, 8.5, 15.5, 8.5)),
            line(seg(7.5, 15, 7.5, 21.5)), line(seg(12, 15, 12, 21.5)), line(seg(16.5, 15, 16.5, 21.5))]


@icon("resistor", CAT, "Capsule shaped resistor with colour bands and a wire lead at each end.",
      tags=["ohm", "resistance", "passive component", "electronics", "through hole", "component"])
def _(S):
    return [shell(rect(5.5, 7, 13, 10, L(S, 3, 5))),
            detail(seg(10, 7, 10, 17)), detail(seg(14, 7, 14, 17)),
            lead2(S, 2, 12, 5.5, 12), lead2(S, 18.5, 12, 22, 12)]


@icon("capacitor", CAT, "Upright can capacitor with a stripe down one side and two legs.",
      tags=["electrolytic", "cap", "farad", "passive component", "electronics", "component"])
def _(S):
    return [shell(rect(5, 3, 14, 15, rr(S, 3))),
            detail(seg(8.5, 3, 8.5, 18)),
            line(seg(9, 18, 9, 22)), line(seg(15, 18, 15, 22))]


@icon("inductor-coil", CAT, "Wire wound in loops around a short core with a lead at each end.",
      tags=["coil", "choke", "winding", "passive component", "electronics", "magnetic"])
def _(S):
    return [shell(rect(6, 9, 12, 6, rr(S, 2))),
            line(seg(8, 5.5, 9.5, 18.5)), line(seg(12, 5.5, 13.5, 18.5)), line(seg(16, 5.5, 17.5, 18.5)),
            lead2(S, 2, 12, 6, 12), lead2(S, 18, 12, 22, 12)]


# --------------------------------------------------------------------------- chunk 3

@icon("diode", CAT, "Slim cylindrical diode with a band at one end and a wire lead on each side.",
      tags=["rectifier", "semiconductor", "polarity", "1n4007", "electronics", "component"])
def _(S):
    return [shell(rect(6, 8.5, 12, 7, L(S, 2, 3.5))),
            solid(rect(14.5, 8.5, 3, 7, 0)),
            lead2(S, 2, 12, 6, 12), lead2(S, 18, 12, 22, 12)]


@icon("led-component", CAT, "Dome topped light emitting diode with one long leg and one short leg.",
      tags=["light emitting diode", "indicator light", "semiconductor", "electronics", "5mm led", "component"])
def _(S):
    return [shell("M5 15H7V8.5A5 5 0 0 1 17 8.5V15H19Z"),
            line(seg(9.5, 15, 9.5, 22)), line(seg(14.5, 15, 14.5, 19))]


@icon("vacuum-tube", CAT, "Glass tube with internal plates and pins at the base.",
      tags=["thermionic valve", "tube amp", "retro electronics", "audio", "valve", "glass"])
def _(S):
    return [shell("M6 16.5V9A6 6 0 0 1 18 9V16.5Z"),
            detail(ellipse(12, 10.5, 2.2, 3.2)),
            line(seg(8.5, 16.5, 8.5, 22)), line(seg(12, 16.5, 12, 22)), line(seg(15.5, 16.5, 15.5, 22))]


@icon("crystal-oscillator", CAT, "Oval metal can with a wave line on top and two legs below.",
      tags=["quartz", "clock source", "resonator", "timing", "frequency", "component"])
def _(S):
    return [shell(rect(3, 4, 18, 11, L(S, 3, 5.5))),
            detail("M7 9.5Q8.75 6 10.5 9.5T14 9.5T17.5 9.5"),
            line(seg(9, 15, 9, 22)), line(seg(15, 15, 15, 22))]


@icon("relay-switch", CAT, "Box holding a coil and a switch arm that closes on a contact.",
      tags=["electromagnetic relay", "contactor", "switching", "coil", "electronics", "automation"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R)),
            detail("M5 16.5A2 2 0 0 1 9 16.5A2 2 0 0 1 13 16.5A2 2 0 0 1 17 16.5"),
            dot(5.5, 8.5, 1.3), dot(18.5, 9.5, 1.3),
            detail(seg(5.5, 8.5, 15.5, 6))]


@icon("potentiometer", CAT, "Square trimmer body with a round knob and three legs.",
      tags=["pot", "variable resistor", "trimmer", "volume knob", "rheostat", "component"])
def _(S):
    return [shell(rect(3, 3, 18, 15, S.R)),
            detail(circle(12, 10.5, 4.2)),
            detail(seg(12, 10.5, 12, 7.2)),
            line(seg(6, 18, 6, 22)), line(seg(12, 18, 12, 22)), line(seg(18, 18, 18, 22))]


def _gate_lines(S, n_in=2, x_in=2, x_to=5, out=None):
    ds = []
    for y in (9, 15)[:n_in]:
        ds.append(lead(S, x_in, y, x_to, y))
    if out:
        ds.append(lead(S, out[0], 12, out[1], 12))
    return ds


def _dgate(S, x0):
    r = L(S, 0, 1.5)
    if r:
        return (f"M{x0 + r} 6H{x0 + 5.5}A6 6 0 0 1 {x0 + 5.5} 18H{x0 + r}"
                f"A{r} {r} 0 0 1 {x0} {18 - r}V{6 + r}A{r} {r} 0 0 1 {x0 + r} 6Z")
    return f"M{x0} 6H{x0 + 5.5}A6 6 0 0 1 {x0 + 5.5} 18H{x0}Z"


@icon("and-gate", CAT, "D shaped logic gate with two input leads and one output lead.",
      tags=["logic gate", "boolean", "digital logic", "schematic", "conjunction", "circuit symbol"])
def _(S):
    return [shell(_dgate(S, 6)), *_gate_lines(S, 2, 2, 6, (17.5, 22))]


@icon("or-gate", CAT, "Curved shield shaped logic gate with two inputs and a pointed output.",
      tags=["logic gate", "boolean", "digital logic", "schematic", "disjunction", "circuit symbol"])
def _(S):
    return [shell("M4.5 6Q9 12 4.5 18Q13.5 18 19.5 12Q13.5 6 4.5 6Z"), *_gate_lines(S, 2, 2, 6.2, (19.5, 22))]


@icon("not-gate", CAT, "Triangle with a small circle at its tip and one input lead.",
      tags=["inverter", "logic gate", "boolean", "negation", "digital logic", "circuit symbol"])
def _(S):
    return [shell(poly([(5, 5), (5, 19), (15.5, 12)], closed=True, r=S.r)),
            shell(circle(17.7, 12, 2.2)),
            lead(S, 2, 12, 5, 12)]


@icon("xor-gate", CAT, "Curved logic gate with an extra curved line behind its inputs.",
      tags=["exclusive or", "logic gate", "boolean", "digital logic", "schematic", "circuit symbol"])
def _(S):
    return [shell("M8.5 6Q12.5 12 8.5 18Q15.5 18 20 12Q15.5 6 8.5 6Z"),
            line("M4.5 6Q8.5 12 4.5 18"),
            lead(S, 2, 9, 5.8, 9), lead(S, 2, 15, 5.8, 15),
            lead(S, 20, 12, 22, 12)]


@icon("nand-gate", CAT, "D shaped logic gate with a small circle at its output.",
      tags=["not and", "logic gate", "boolean", "digital logic", "schematic", "circuit symbol"])
def _(S):
    return [shell(_dgate(S, 3.5)),
            shell(circle(17.5, 12, 2)),
            lead(S, 2, 9, 3.5, 9), lead(S, 2, 15, 3.5, 15),
            lead(S, 19.5, 12, 22, 12)]


@icon("nor-gate", CAT, "Curved shield logic gate with a small circle at its output.",
      tags=["not or", "logic gate", "boolean", "digital logic", "schematic", "circuit symbol"])
def _(S):
    return [shell("M4.5 6Q8.5 12 4.5 18Q11.5 18 15.5 12Q11.5 6 4.5 6Z"),
            shell(circle(17.7, 12, 2.2)),
            lead(S, 2, 9, 5.6, 9), lead(S, 2, 15, 5.6, 15)]


@icon("logic-analyzer", CAT, "Instrument box showing a square wave with probe wires hanging below.",
      tags=["digital analyzer", "signal capture", "debugging", "waveform", "test equipment", "probe"])
def _(S):
    return [shell(rect(2, 3, 20, 12, S.R)),
            detail(poly([(5.5, 11), (5.5, 7.5), (10, 7.5), (10, 11), (14.5, 11), (14.5, 7.5), (18.5, 7.5)], r=S.r * 0.5)),
            line(seg(6, 15, 6, 21)), line(seg(10, 15, 10, 21)), line(seg(14, 15, 14, 21)), line(seg(18, 15, 18, 21))]


# --------------------------------------------------------------------------- chunk 4

@icon("mechanical-keyboard", CAT, "Keyboard with separate raised keycaps, a long space bar and a coiled cable behind it.",
      tags=["clicky keyboard", "gaming keyboard", "keycaps", "switches", "typing", "coiled cable"])
def _(S):
    ds = [shell(rect(2, 8, 20, 13, S.R)),
          line("M4 4.2Q5.5 1.7 7 4.2T10 4.2T13 4.2T16 4.2T19 4.2")]
    for x in (3.4, 8.2, 13, 17.8):
        ds.append(sq(x, 10.2, 2.8, 3, 0.4))
    ds.append(sq(6.5, 15.8, 11, 2.8, 0.4))
    return ds


@icon("numeric-keypad", CAT, "Narrow block of keys in a grid of three columns and four rows.",
      tags=["numpad", "number pad", "ten key", "keys", "calculator keys", "input device"])
def _(S):
    ds = [shell(rect(4, 3, 16, 18, S.R))]
    for y in (7, 10.5, 14, 17.5):
        for x in (8, 12, 16):
            ds.append(dot(x, y, 1.1))
    return ds


@icon("trackball", CAT, "Mouse body cradling a large ball on top.",
      tags=["trackball mouse", "pointing device", "ball mouse", "input device", "cursor", "ergonomic"])
def _(S):
    body = minus(rect(3, 10, 18, 11, S.R), circle(12, 8.5, 7.5))
    return [shell(body),
            shell(circle(12, 8.5, 5))]


@icon("light-pen", CAT, "Pen with a trailing cable whose tip touches the corner of a monitor screen.",
      tags=["light gun", "stylus", "crt", "retro computing", "input device", "touch screen"])
def _(S):
    T = (12.4, 11.2)
    u = (0.707, 0.707)
    n = (-0.707, 0.707)
    tail = (T[0] + u[0] * 10.2, T[1] + u[1] * 10.2)
    mid = (T[0] + u[0] * 3.0, T[1] + u[1] * 3.0)
    w = 1.8
    pts = [T, (mid[0] + n[0] * w, mid[1] + n[1] * w), (tail[0] + n[0] * w, tail[1] + n[1] * w),
           (tail[0] - n[0] * w, tail[1] - n[1] * w), (mid[0] - n[0] * w, mid[1] - n[1] * w)]
    return [shell(rect(2, 3, 10, 8, rr(S, 2.5))),
            detail(seg(5, 7, 9, 7)),
            shell(poly(pts, closed=True, r=S.r * 0.4)),
            line("M19 19.8C18 22 14 22 9 21")]


@icon("punch-tape", CAT, "Long paper tape with a row of feed holes and punched data holes.",
      tags=["paper tape", "teletype", "retro data", "punched tape", "storage", "history"])
def _(S):
    ds = [shell(rect(2, 6, 20, 12, rr(S, 3)))]
    for x in (5, 8.5, 12, 15.5, 19):
        ds.append(dot(x, 12, 0.8))
    for x in (5, 12, 15.5):
        ds.append(dot(x, 9.2, 0.9))
    for x in (8.5, 12, 19):
        ds.append(dot(x, 14.8, 0.9))
    return ds


@icon("magnetic-tape-reel", CAT, "Open spool reel with three windows and a ribbon of tape trailing away.",
      tags=["reel to reel", "tape drive", "data tape", "mainframe storage", "backup", "audio tape"])
def _(S):
    ds = [shell(circle(9.5, 9.5, 7)), dot(9.5, 9.5, 1.1),
          line(poly([(9.5, 16.5), (9.5, 21), (22, 21)], r=S.r))]
    for a in (90, 210, 330):
        x, y = polar(9.5, 9.5, 3.9, a)
        ds.append(dot(x, y, 1.3))
    return ds


@icon("zip-disk", CAT, "Square cartridge with a wide metal shutter at the top and a label line.",
      tags=["zip drive", "zip cartridge", "removable disk", "retro storage", "cartridge", "magnetic disk"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail(poly([(7.5, 3), (7.5, 10), (16.5, 10), (16.5, 3)])),
            detail(circle(12, 16, 2.2))]


@icon("laser-disc", CAT, "Large video disc with ring lines and a small centre hole.",
      tags=["laserdisc", "video disc", "optical disc", "retro media", "movie disc", "ld"])
def _(S):
    ds = [shell(circle(12, 12, 9)), detail(circle(12, 12, 5.2))]
    if S.name == "line":
        ds.append(detail(circle(12, 12, 1.4)))
    else:
        ds.append(dot(12, 12, 1.6))
    return ds


@icon("mini-disc", CAT, "Square cartridge with a round disc window and a slider.",
      tags=["minidisc", "md", "audio disc", "retro music", "cartridge", "portable audio"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail(circle(11.5, 10.5, 4)),
            dot(11.5, 10.5, 1.2),
            detail(seg(8, 18, 16, 18))]


@icon("cpu-socket", CAT, "Square processor socket with a grid of pin holes and a locking lever.",
      tags=["lga", "pga", "motherboard", "processor slot", "pins", "lever"])
def _(S):
    ds = [shell(rect(3, 5, 15, 15, S.R)),
          line(poly([(18, 17), (21, 17), (21, 6)], r=S.r))]
    for x in (7.5, 10.5, 13.5):
        for y in (9, 12.5, 16):
            ds.append(dot(x, y, 1.1))
    return ds


def _card(S, ports):
    return [line(seg(9.5, 3, 9.5, 21)),
            shell(rect(12, 4, 10, 11, rr(S, 2))),
            line(seg(15, 15, 15, 20)), line(seg(19, 15, 19, 20))] + ports


@icon("expansion-card", CAT, "Add-in card with a metal bracket, a chip and gold edge fingers.",
      tags=["pcie card", "add-in card", "slot card", "motherboard", "peripheral", "hardware"])
def _(S):
    return [line(seg(5, 3, 5, 21)),
            shell(rect(7.5, 4, 14.5, 11, rr(S, 2))),
            sq(11, 7, 7, 4, 0.5),
            line(seg(10.5, 15, 10.5, 20)), line(seg(14.5, 15, 14.5, 20)), line(seg(18.5, 15, 18.5, 20))]


@icon("sound-card", CAT, "Add-in card whose bracket carries two round audio jacks.",
      tags=["audio card", "pcie audio", "audio expansion", "jacks", "soundcard", "hardware"])
def _(S):
    return _card(S, [shell(circle(5.5, 7.5, 2.3)), shell(circle(5.5, 15.5, 2.3))])


@icon("network-card", CAT, "Add-in card whose bracket carries an ethernet port.",
      tags=["nic", "ethernet card", "lan card", "network adapter", "rj45", "hardware"])
def _(S):
    return _card(S, [shell(rect(2.5, 8, 5, 8, rr(S, 1.5)))])


@icon("bios-chip", CAT, "Small chip with pins on one side and a round coin battery beside it.",
      tags=["cmos", "firmware chip", "flash chip", "motherboard", "rom", "coin cell"])
def _(S):
    return [shell(rect(5, 4, 8, 16, rr(S, 2))),
            dot(9, 7.5, 1.1),
            line(seg(2, 8, 5, 8)), line(seg(2, 12, 5, 12)), line(seg(2, 16, 5, 16)),
            shell(circle(18, 12, 4)), dot(18, 12, 1.2)]


@icon("computer-fan", CAT, "Square fan frame with four curved blades around a hub.",
      tags=["case fan", "cooling fan", "cpu cooler", "airflow", "pc cooling", "blower"])
def _(S):
    ds = [shell(rect(2.5, 2.5, 19, 19, S.R)), dot(12, 12, 1.6)]
    for a in (-90, -18, 54, 126, 198):
        x1, y1 = polar(12, 12, 2.6, a)
        x2, y2 = polar(12, 12, 7.2, a + 40)
        cx, cy = polar(12, 12, 5.8, a - 15)
        ds.append(detail(f"M{fmt(x1)} {fmt(y1)}Q{fmt(cx)} {fmt(cy)} {fmt(x2)} {fmt(y2)}"))
    return ds


def _cells(x0, y0, cw, ch, gap, cols, rows):
    return [[(x0 + c * (cw + gap), y0 + r * (ch + gap)) for c in range(cols)] for r in range(rows)]


def _pixel_icon(name, desc, tags, outer, grid, filled_cells):
    """Grid of square cells in an outlined frame; some cells filled."""
    x, y, w, h = outer
    cols, rows, cw, ch = grid

    @icon(name, CAT, desc, tags=tags, filled=lambda: _pixel_filled(outer, grid, filled_cells))
    def _(S):
        ds = [shell(rect(x, y, w, h, rr(S, 3)))]
        for c in range(1, cols):
            ds.append(detail(seg(x + 1 + c * (cw + 2) - 1 + (0), y, x + 1 + c * (cw + 2) - 1, y + h)))
        for r_ in range(1, rows):
            ds.append(detail(seg(x, y + 1 + r_ * (ch + 2) - 1, x + w, y + 1 + r_ * (ch + 2) - 1)))
        for (c, r_) in filled_cells:
            ds.append(solid(rect(x + 1 + c * (cw + 2), y + 1 + r_ * (ch + 2), cw, ch, 0)))
        return ds
    return _


def _pixel_filled(outer, grid, filled_cells):
    x, y, w, h = outer
    cols, rows, cw, ch = grid
    body = P(rect(x - 1, y - 1, w + 2, h + 2, 3))
    holes = []
    for r_ in range(rows):
        for c in range(cols):
            if (c, r_) not in filled_cells:
                holes.append(P(rect(x + 1.6 + c * (cw + 2), y + 1.6 + r_ * (ch + 2), cw - 1.2, ch - 1.2, 0.4)))
    return D(body, *holes)


_pixel_icon("pixel-grid", "Square grid of cells with a few of them filled in.",
            ["pixels", "bitmap", "raster", "pixel art", "resolution", "mosaic"],
            (3, 3, 18, 18), (3, 3, 4, 4), {(0, 0), (2, 1), (1, 2)})


# --------------------------------------------------------------------------- chunk 5

@icon("screen-resolution", CAT, "Monitor with four arrows in its corners pointing outward.",
      tags=["display size", "pixels", "dpi", "scaling", "fullscreen", "1080p", "4k"])
def _(S):
    ds = [shell(rect(2, 3, 20, 15, S.R)),
          line(seg(12, 18, 12, 21)), line(seg(8, 21, 16, 21))]
    c = (12, 10.5)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = 12 + sx * 5.5, 10.5 + sy * 3.2
            ds.append(detail(seg(12 + sx * 1.8, 10.5 + sy * 1.2, cx, cy)))
            ds.append(detail(poly([(cx - sx * 2.6, cy), (cx, cy), (cx, cy - sy * 2.6)])))
    return ds


@icon("dual-monitor", CAT, "Two monitors side by side, each on its own stand.",
      tags=["two screens", "multi monitor", "extended desktop", "workstation", "displays", "setup"])
def _(S):
    ds = []
    for x in (2.5, 13.5):
        ds.append(shell(rect(x, 4, 7.5, 9, rr(S, 2))))
        ds.append(line(seg(x + 3.75, 13, x + 3.75, 18)))
        ds.append(line(seg(x + 0.75, 19, x + 6.75, 19)))
    return ds


def _curve(p0, c, p1, n=14):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        pts.append((u * u * p0[0] + 2 * u * t * c[0] + t * t * p1[0], u * u * p0[1] + 2 * u * t * c[1] + t * t * p1[1]))
    return pts


@icon("ultrawide-monitor", CAT, "Very wide curved monitor on a short stand.",
      tags=["curved monitor", "21:9", "widescreen", "gaming monitor", "display", "super wide"])
def _(S):
    top = _curve((2, 5), (12, 8.5), (22, 5))
    bot = _curve((22, 14), (12, 17.5), (2, 14))
    return [shell(poly(top + bot, closed=True, r=S.r * 0.5)),
            line(seg(12, 16, 12, 19.5)), line(seg(8, 20.5, 16, 20.5))]


@icon("chip-wafer", CAT, "Round silicon wafer with a flat edge, divided into a grid of dies.",
      tags=["silicon wafer", "semiconductor", "die", "fab", "foundry", "lithography"])
def _(S):
    cx = math.sqrt(81 - 49)
    ds = [shell(f"M{fmt(12 - cx)} 19A9 9 0 1 1 {fmt(12 + cx)} 19Z")]
    xs = (7, 12, 17) if S.name == "line" else (8.5, 15.5)
    for x in xs:
        h = math.sqrt(81 - (x - 12) ** 2) - 1
        ds.append(detail(seg(x, 12 - h, x, min(12 + h, 19 - 0.01))))
    for y in xs:
        w = math.sqrt(81 - (y - 12) ** 2) - 1
        ds.append(detail(seg(12 - w, y, 12 + w, y)))
    return ds


@icon("hardware-wallet", CAT, "Small key shaped device with a tiny screen, two buttons and a key ring loop.",
      tags=["crypto wallet", "cold storage", "hardware device", "cryptocurrency", "security key", "self custody"])
def _(S):
    return [shell(rect(6, 8.5, 12, 13, S.R)),
            line(poly([(9.5, 8.5), (9.5, 5.5), (14.5, 5.5), (14.5, 8.5)], r=S.r + 1)) if S.name == "rounded" else
            line(poly([(9.5, 8.5), (9.5, 3.5), (14.5, 3.5), (14.5, 8.5)])),
            detail(seg(9, 12.5, 15, 12.5)),
            dot(9.5, 17.5, 1.2), dot(14.5, 17.5, 1.2)]


@icon("mining-rig", CAT, "Open frame holding a row of graphics cards on a shelf.",
      tags=["gpu rig", "crypto mining", "graphics cards", "hash rate", "farm", "open air frame"])
def _(S):
    ds = [line(seg(2, 4.5, 22, 4.5)), line(seg(2, 19.5, 22, 19.5)),
          line(seg(3, 4.5, 3, 19.5)), line(seg(21, 4.5, 21, 19.5))]
    for x in (7.5, 12, 16.5):
        ds.append(shell(rect(x - 1.25, 8.5, 2.5, 8, 0.6)))
    return ds


# --------------------------------------------------------------------------- chunk 6

@icon("smart-contract", CAT, "Document page with a small cube stamped into its lower corner.",
      tags=["blockchain", "agreement", "web3", "dapp", "on-chain", "contract code"])
def _(S):
    page = minus(poly([(3, 3), (12, 3), (17, 8), (17, 21), (3, 21)], closed=True, r=S.r), circle(16.5, 17, 6.3))
    hx = regular(16.5, 17, 4.6, 6)
    ds = [shell(page),
          detail(seg(6.5, 9, 11, 9)), detail(seg(6.5, 13, 9.5, 13)),
          shell(poly(hx, closed=True, r=S.r * 0.5))]
    return ds


@icon("distributed-ledger", CAT, "Three small ledger books joined to each other in a triangle.",
      tags=["blockchain", "shared ledger", "dlt", "nodes", "peer to peer", "consensus"])
def _(S):
    ds = []
    for (x, y) in ((9, 2.5), (2.5, 14.5), (15.5, 14.5)):
        ds.append(shell(rect(x, y, 6.5, 7, rr(S, 3))))
    ds.append(line(seg(10.2, 9.5, 6.5, 14.5)))
    ds.append(line(seg(13.8, 9.5, 17.5, 14.5)))
    ds.append(line(seg(9, 18, 15.5, 18)))
    return ds


@icon("bit-byte", CAT, "Block of eight binary cells, some filled and some empty.",
      tags=["binary", "bits", "eight bits", "octet", "data size", "memory unit"],
      filled=lambda: _bits_filled())
def _(S):
    ds = [shell(rect(2, 6, 20, 12, rr(S, 3)))]
    for x in (7, 12, 17):
        ds.append(detail(seg(x, 6, x, 18)))
    ds.append(detail(seg(2, 12, 22, 12)))
    for (c, r) in _BITS:
        ds.append(solid(rect(3 + c * 5, 7 if r == 0 else 13, 3, 4, 0)))
    return ds


_BITS = {(0, 0), (2, 0), (3, 0), (1, 1), (3, 1)}


def _bits_filled():
    body = P(rect(1, 5, 22, 14, 3))
    holes = []
    for r in (0, 1):
        for c in range(4):
            if (c, r) not in _BITS:
                x0 = 3 + c * 5 + 0.6
                y0 = (7 if r == 0 else 13) + 0.6
                holes.append(P(rect(x0, y0, 1.8, 2.8, 0.3)))
    return D(body, *holes)


@icon("hexadecimal", CAT, "Hash sign followed by two letter f characters, the prefix and digits of a hex value.",
      tags=["hex", "base 16", "color code", "0xff", "number system", "hex code"])
def _(S):
    return [line(seg(4, 5, 4, 19)), line(seg(8, 5, 8, 19)),
            line(seg(2, 9, 10, 9)), line(seg(2, 15, 10, 15)),
            line("M14 19V8Q14 5 17 5"), line(seg(11.5, 10.5, 16, 10.5)),
            line("M19.5 19V8Q19.5 5 22 5"),
            line(seg(17.5, 10.5, 22, 10.5))]


@icon("unicode-character", CAT, "Square holding the letter U followed by a plus sign, the notation for a code point.",
      tags=["u+", "code point", "utf-8", "glyph", "text encoding", "character map"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)),
            detail("M7.5 8V13A2.5 2.5 0 0 0 12.5 13V8"),
            detail(seg(14.5, 12, 18.5, 12)), detail(seg(16.5, 10, 16.5, 14))]


@icon("character-encoding", CAT, "Letter A with an arrow pointing to the binary digits one and zero.",
      tags=["ascii", "utf", "charset", "text to binary", "encode", "text encoding"])
def _(S):
    return [line(poly([(2.5, 19), (6.5, 5), (10.5, 19)], r=S.r * 0.4)), line(seg(4.2, 14, 8.8, 14)),
            line(seg(11.8, 12, 14.2 - L(S, 0, 0), 12)),
            Part("solid", poly([(15.4, 12), (12.8, 10.2), (12.8, 13.8)], closed=True, r=L(S, 0, 0.3))),
            line(poly([(17.3, 7), (19.3, 5), (19.3, 11)])),
            line(ellipse(19, 17.5, 1.6, 2.6))]


@icon("checksum", CAT, "Document page with a hash sign and a check mark confirming its contents.",
      tags=["hash check", "file integrity", "md5", "sha256", "verify", "digest"])
def _(S):
    return [shell(poly([(4, 2.5), (14, 2.5), (20, 8.5), (20, 21.5), (4, 21.5)], closed=True, r=S.r)),
            detail(seg(8.5, 6, 8.5, 12.5)), detail(seg(12.5, 6, 12.5, 12.5)),
            detail(seg(6.5, 8, 14.5, 8)), detail(seg(6.5, 11, 14.5, 11)),
            detail(poly([(9.5, 17), (12, 19.2), (16.5, 14.5)]))]


@icon("public-key", CAT, "Key whose round bow is drawn as a globe with a meridian and an equator.",
      tags=["asymmetric encryption", "pki", "ssh key", "certificate", "crypto key", "shared key"])
def _(S):
    return [shell(circle(9, 9, 6.2)),
            detail(ellipse(9, 9, 2.4, 6.2)), detail(seg(2.8, 9, 15.2, 9)),
            line(seg(13.4, 13.4, 20.5, 20.5)),
            line(seg(17.5, 17.5, 19.8, 15.2)), line(seg(20, 20, 22 - L(S, 0.3, 0.8), 18 + L(S, 0.3, 0.8)))]


@icon("root-user", CAT, "Person with a small crown above the head and a hash sign beside the shoulders.",
      tags=["superuser", "administrator", "admin", "privileged", "linux", "sudo"])
def _(S):
    return [shell(poly([(5, 8), (5, 3.5), (7.2, 5.6), (9, 3), (10.8, 5.6), (13, 3.5), (13, 8)], closed=True, r=S.r * 0.4)),
            shell(circle(9, 12.5, 2.6)),
            line("M3.5 21.5V20.5Q3.5 17 9 17Q14.5 17 14.5 20.5V21.5"),
            line(seg(18, 11, 17.2, 21)), line(seg(21, 11, 20.2, 21)),
            line(seg(15.5, 14.5, 22.5, 14.5)), line(seg(15, 18, 22, 18))]


@icon("sudo-command", CAT, "Command prompt chevron and cursor line with a small crown above them.",
      tags=["superuser do", "elevated", "administrator command", "terminal", "shell", "privilege"])
def _(S):
    return [shell(poly([(7, 9), (7, 4), (9.5, 6.4), (12, 3.5), (14.5, 6.4), (17, 4), (17, 9)], closed=True, r=S.r * 0.4)),
            line(poly([(3.5, 13), (9, 16.5), (3.5, 20)], r=S.r * 0.6)),
            line(seg(12, 20, 20, 20))]


@icon("os-kernel", CAT, "Small solid nut at the centre of two concentric rings.",
      tags=["core", "operating system", "system core", "layers", "ring zero", "linux kernel"])
def _(S):
    return [shell(circle(12, 12, 9)),
            detail(circle(12, 12, 5.6)),
            Part("dot", poly(regular(12, 12, L(S, 3, 3.3), 6), closed=True, r=L(S, 0, 1.0)))]


@icon("device-driver", CAT, "Chip with pins on all sides and a steering wheel drawn on its face.",
      tags=["hardware driver", "software driver", "peripheral", "driver update", "controller", "system software"])
def _(S):
    ds = [shell(rect(5, 5, 14, 14, rr(S, 3)))]
    for v in (9, 15):
        ds += [line(seg(2, v, 5, v)), line(seg(19, v, 22, v)), line(seg(v, 2, v, 5)), line(seg(v, 19, v, 22))]
    ds += [detail(circle(12, 12, 4)), detail(seg(8, 12, 16, 12)), detail(seg(12, 12, 12, 16))]
    return ds


@icon("firmware", CAT, "Chip with pins on both sides and a download arrow pointing into it.",
      tags=["flash update", "embedded software", "firmware update", "rom", "device update", "flash"])
def _(S):
    ds = [shell(rect(5, 4, 14, 16, rr(S, 3)))]
    for v in (8, 12, 16):
        ds += [line(seg(2, v, 5, v)), line(seg(19, v, 22, v))]
    ds += [detail(seg(12, 8, 12, 15)), detail(poly([(9, 12.5), (12, 15.5), (15, 12.5)]))]
    return ds


@icon("bootloader", CAT, "Boot with a power symbol on its shaft, the first code that runs at start up.",
      tags=["boot", "startup", "bios", "uefi", "first stage", "power on"])
def _(S):
    return [shell(poly([(4.5, 3), (15, 3), (15, 10), (20, 12.5), (21.5, 16), (21.5, 21), (4.5, 21)], closed=True, r=S.r)),
            detail(arc(9.75, 9.5, 2.9, -55, 235)), detail(seg(9.75, 5.8, 9.75, 9.5))]
