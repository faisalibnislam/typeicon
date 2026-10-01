"""TypeIcon Core: electronics (batch 002): components, displays, power parts, connectors and cabling.

Drawn from the parts themselves as a hobbyist or technician sees them on the bench: components mostly in
front or side view with their legs pointing down, connectors side on with the cable leaving to one side.
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


def ring(cx, cy, ro, ri):
    """Annulus as one closed shape (outer circle minus inner circle)."""
    return minus(circle(cx, cy, ro), circle(cx, cy, ri))


def vseg(S, x, y1, y2):
    """Vertical open stroke whose far end (y2) stays inside the live area in both cap styles."""
    k = L(S, 0, 1) * (1 if y2 > y1 else -1)
    return line(seg(x, y1, x, y2 - k))


def hseg(S, x1, x2, y):
    k = L(S, 0, 1) * (1 if x2 > x1 else -1)
    return line(seg(x1, y, x2 - k, y))


# ============================================================================ sockets and inductive parts

@icon("zif-socket", CAT, "Zero insertion force chip socket with a grid of holes and its lever raised",
      tags=["zif", "chip socket", "ic socket", "programmer", "cpu socket", "eeprom"])
def _(S):
    holes = [dot(x, y, 1) for x in (6.5, 10, 13.5) for y in (8.5, 12, 15.5)]
    return [
        shell(rect(3, 5, 14, 14, rr(S, 2))),
        *holes,
        line(poly([(17, 17), (20.5, 17), (20.5, L(S, 2.5, 3.5))], r=S.r)),
    ]


@icon("toroidal-inductor", CAT, "Ring shaped core wound with wire and two leads",
      tags=["toroid", "inductor", "coil", "choke", "ferrite ring", "winding"])
def _(S):
    c, ro, ri = (12, 10.5), 8, 3.5
    spokes = []
    for k in range(8):
        a = 22.5 + k * 45
        x1, y1 = polar(c[0], c[1], ri + 1, a)
        x2, y2 = polar(c[0], c[1], ro - 1, a)
        spokes.append(detail(seg(x1, y1, x2, y2)))
    parts = [shell(ring(c[0], c[1], ro, ri)), *spokes]
    parts += [vseg(S, 8.5, 17.7, 22), vseg(S, 15.5, 17.7, 22)]
    if S.name == "rounded":
        parts = [shell(ring(c[0], c[1], ro, ri)), *spokes, vseg(S, 8.5, 17.7, 22), vseg(S, 15.5, 17.7, 22)]
    return parts


@icon("ferrite-bead", CAT, "Short ferrite tube threaded on a wire",
      tags=["ferrite", "bead", "emi", "noise filter", "suppressor", "rf"])
def _(S):
    body = "M8 7H16A2.5 5 0 0 1 16 17H8A2.5 5 0 0 1 8 7Z"
    if S.name == "rounded":
        body = "M8 7H15A3 5 0 0 1 15 17H8A2.5 5 0 0 1 8 7Z"
    return [
        shell(body),
        detail("M8 7A2.5 5 0 0 1 8 17"),
        hseg(S, 8, 2, 12),
        hseg(S, L(S, 18.5, 18), 22, 12),
    ]


@icon("ferrite-choke", CAT, "Clip-on ferrite choke in two halves clamped around a cable",
      tags=["ferrite", "clip-on", "choke", "emi", "cable filter", "snap-on"])
def _(S):
    r = L(S, 1, 3)
    n = 3.5  # radius of the channel the cable sits in
    x = math.sqrt(n * n - 2 * 2)
    top = (f"M6 10V{3 + r}A{r} {r} 0 0 1 {6 + r} 3H{18 - r}A{r} {r} 0 0 1 18 {3 + r}V10H{fmt(12 + x)}"
           f"A{n} {n} 0 0 0 {fmt(12 - x)} 10Z")
    bottom = (f"M6 14V{21 - r}A{r} {r} 0 0 0 {6 + r} 21H{18 - r}A{r} {r} 0 0 0 18 {21 - r}V14H{fmt(12 + x)}"
              f"A{n} {n} 0 0 1 {fmt(12 - x)} 14Z")
    return [
        shell(top),
        shell(bottom),
        line(seg(L(S, 2, 3), 12, L(S, 22, 21), 12)),
    ]


# ============================================================================ displays and lights

@icon("seven-segment-display", CAT, "Display showing a figure eight made of seven segments and a decimal point",
      tags=["7 segment", "digit", "numeric display", "led display", "counter", "digital number"])
def _(S):
    e = L(S, 0, 1)
    xl, xr, g = 7.5, 14.5, 1.25
    ys = (5.5, 12, 18.5)
    parts = [shell(rect(3, 2, 18, 20, rr(S, 3)))]
    parts += [detail(seg(xl + g + e, y, xr - g - e, y)) for y in ys]
    for y1, y2 in zip(ys, ys[1:]):
        parts += [detail(seg(x, y1 + g + e, x, y2 - g - e)) for x in (xl, xr)]
    parts.append(dot(17.75, 18.5, 1.1))
    return parts


@icon("led-matrix", CAT, "Square board covered in a grid of round LEDs",
      tags=["dot matrix", "led grid", "led panel", "pixel display", "scrolling sign", "8x8"])
def _(S):
    pts = (6.5, 10, 13.5, 17)
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        *[dot(x, y, 1.05) for x in pts for y in pts],
    ]


@icon("character-lcd", CAT, "Wide LCD module with two rows of characters and header pins on top",
      tags=["lcd", "16x2", "text display", "alphanumeric", "lcd module", "lcd display"])
def _(S):
    pins = [vseg(S, x, 5, 2) for x in (6, 10, 14, 18)]
    chars = [sq(x, y, 2, 2, L(S, 0, 0.5)) for x in (7, 10, 13, 16) for y in (10.5, 14)]
    return [
        *pins,
        shell(rect(2, 5, 20, 15, rr(S, 2))),
        detail(rect(5, 8, 14, 9, L(S, 0, 1))),
        *chars,
    ]


@icon("oled-display-module", CAT, "Small display board with a dark square screen and four pins on top",
      tags=["oled", "display module", "screen", "breakout", "i2c display", "tiny screen"])
def _(S):
    pins = [vseg(S, x, 6, 2) for x in (7.5, 10.5 + 0.5, 13 + 0.5, 16.5)]
    pins = [vseg(S, x, 6, 2) for x in (6.75, 10.25, 13.75, 17.25)]
    return [
        *pins,
        shell(rect(4, 6, 16, 16, rr(S, 2))) if S.name != "rounded" else shell(rect(4, 6, 16, 15.5, 3)),
        sq(7, 10, 10, 8, L(S, 0, 1)),
    ]


@icon("e-paper-display", CAT, "Thin e-paper panel with lines of text and a flat ribbon tail",
      tags=["e-ink", "epaper", "electronic paper", "eink display", "e-reader screen", "low power display"])
def _(S):
    outline = [(3, 2.5), (21, 2.5), (21, 16.5), (15, 16.5), (15, 21.5), (9, 21.5), (9, 16.5), (3, 16.5)]
    return [
        shell(poly(outline, closed=True, r=S.r)),
        detail(seg(6.5, 6, 17.5, 6)),
        detail(seg(6.5, 9.5, 17.5, 9.5)),
        detail(seg(6.5, 13, 13, 13)),
    ]


@icon("led-bar-graph", CAT, "LED bar graph block with a row of lit and unlit segments",
      tags=["bar graph", "led bar", "level meter", "vu meter", "segment bar", "indicator"])
def _(S):
    return [
        shell(rect(2.5, 4, 19, 16, rr(S, 3))),
        *[sq(x - 1, 7.5, 2, 9, L(S, 0, 0.8)) for x in (6.5, 10, 13.5, 17)],
    ]


@icon("rgb-led", CAT, "Domed LED with four legs of different lengths",
      tags=["rgb", "led", "colour led", "color led", "multicolor", "diode"])
def _(S):
    outline = [(7, 13), (7, 8)]
    d = "M7 13V8A5 5 0 0 1 17 8V13H18.5V15.5H5.5V13Z"
    if S.name == "rounded":
        d = "M7 13V8A5 5 0 0 1 17 8V13H17.5A1 1 0 0 1 18.5 14V14.5A1 1 0 0 1 17.5 15.5H6.5A1 1 0 0 1 5.5 14.5V14A1 1 0 0 1 6.5 13Z"
    return [
        shell(d),
        vseg(S, 7.5, 15.5, 20),
        vseg(S, 10.5, 15.5, 22),
        vseg(S, 13.5, 15.5, 19),
        vseg(S, 16.5, 15.5, 21),
    ]


@icon("addressable-led-ring", CAT, "Ring board carrying a circle of small square LED chips",
      tags=["led ring", "pixel ring", "smart led", "circular led", "rgb ring", "addressable led"])
def _(S):
    chips = []
    for k in range(8):
        a = k * 45
        x, y = polar(12, 12, 7, a)
        if S.name == "line":
            chips.append(Part("dot", poly([polar(x, y, 1.6, a + 45 + 90 * i) for i in range(4)], closed=True)))
        else:
            chips.append(dot(x, y, 1.2))
    return [shell(ring(12, 12, 9.5, 4.5)), *chips]


@icon("laser-diode-module", CAT, "Small cylindrical laser module with a lens, two wires and a beam",
      tags=["laser", "laser diode", "laser pointer", "beam", "laser module", "optics"])
def _(S):
    body = [(9.5, 10), (12, 10), (12, 8), (18.5, 8), (18.5, 16), (12, 16), (12, 14), (9.5, 14)]
    return [
        shell(poly(body, closed=True, r=L(S, 0, 0.8))),
        hseg(S, 18.5, 22, 10),
        hseg(S, 18.5, 22, 14),
        line(seg(L(S, 2, 3), 12, 7, 12)),
    ]


@icon("photoresistor", CAT, "Light dependent resistor: a round disc with a winding track and two legs",
      tags=["ldr", "light sensor", "photocell", "light dependent resistor", "cds cell", "light detector"])
def _(S):
    track = poly([(8.5, 14), (8.5, 7), (12, 7), (12, 14), (15.5, 14), (15.5, 7)], r=S.r)
    return [
        shell(circle(12, 10.5, 7.5)),
        detail(track),
        vseg(S, 9.5, 17.6, 22),
        vseg(S, 14.5, 17.6, 22),
    ]


@icon("nixie-tube", CAT, "Tall glass nixie tube with a glowing numeral inside and pins at the base",
      tags=["nixie", "vacuum tube", "numeral tube", "retro display", "glow tube", "valve"])
def _(S):
    tube = "M6.5 18V8A5.5 5.5 0 0 1 17.5 8V18Z"
    if S.name == "rounded":
        tube = "M6.5 16V8A5.5 5.5 0 0 1 17.5 8V16A2 2 0 0 1 15.5 18H8.5A2 2 0 0 1 6.5 16Z"
    two = "M9.75 9.25A2.25 2.25 0 1 1 13.9 10.7L9.75 15H14.5"
    return [
        shell(tube),
        detail(two, stroke_miterlimit="2"),
        vseg(S, 8.5, 18, 22),
        vseg(S, 12, 18, 22),
        vseg(S, 15.5, 18, 22),
    ]


# ============================================================================ sound, motion and heat

@icon("piezo-disc", CAT, "Thin round piezo disc with a smaller ceramic disc on top and two wires",
      tags=["piezo", "piezoelectric", "transducer", "contact mic", "disc element", "knock sensor"])
def _(S):
    return [
        shell(circle(10, 10, 7.5)),
        detail(circle(10, 10, 3.5)),
        line("M10 12V18.5Q10 21 12.5 21H21.5" if S.name == "line" else "M10 12V18.5Q10 21 12.5 21H20.5"),
        line("M16.5 13.75Q18 17 21.5 17" if S.name == "line" else "M16.5 13.75Q18 17 20.5 17"),
        dot(10, 11, 1.4),
    ]


@icon("piezo-buzzer", CAT, "Short cylindrical buzzer with a sound hole on top and two legs",
      tags=["buzzer", "beeper", "piezo", "alarm", "beep", "sounder"])
def _(S):
    rx, ry = 7.5, 3
    body = f"M{12 - rx} 8V15A{rx} {ry} 0 0 0 {12 + rx} 15V8A{rx} {ry} 0 0 0 {12 - rx} 8Z"
    return [
        shell(body),
        detail(f"M{12 - rx} 8A{rx} {ry} 0 0 0 {12 + rx} 8"),
        dot(12, 8, 1),
        vseg(S, 9.5, 18, 22),
        vseg(S, 14.5, 18, 22),
    ]


@icon("electret-microphone", CAT, "Small round microphone capsule with a mesh face and two pins",
      tags=["electret", "mic capsule", "condenser mic", "microphone element", "sound sensor", "mic"])
def _(S):
    holes = [dot(12 + dx, 10 + dy, 0.95) for dx in (-3, 0, 3) for dy in (-3, 0, 3)]
    return [
        shell(circle(12, 10, 7.5)),
        *holes,
        vseg(S, 10, 17.5, 22),
        vseg(S, 14, 17.5, 22),
    ]


@icon("vibration-motor", CAT, "Flat coin vibration motor with two thin wires and buzz marks",
      tags=["vibration", "haptic", "coin motor", "vibrate", "rumble", "erm motor"])
def _(S):
    rx, ry, cy = 6.5, 3, 8.5
    body = f"M{12 - rx} {cy}V{cy + 2.5}A{rx} {ry} 0 0 0 {12 + rx} {cy + 2.5}V{cy}A{rx} {ry} 0 0 0 {12 - rx} {cy}Z"
    return [
        shell(body),
        detail(f"M{12 - rx} {cy}A{rx} {ry} 0 0 0 {12 + rx} {cy}"),
        vseg(S, 10, 14, 22),
        vseg(S, 14, 14, 22),
        line(seg(2.5, L(S, 6, 7), 2.5, L(S, 12, 11))),
        line(seg(21.5, L(S, 6, 7), 21.5, L(S, 12, 11))),
    ]


@icon("gear-motor", CAT, "Small cylindrical motor joined to a gearbox with an output shaft",
      tags=["gearmotor", "geared motor", "dc motor", "gearbox", "robot motor", "reduction gear"])
def _(S):
    body = union(rect(2.5, 7, 10, 10, rr(S, 2)), rect(11, 4, 8, 16, rr(S, 2)))
    return [
        shell(body),
        detail(seg(6, 7, 6, 17)),
        hseg(S, 19, 22, 12),
    ]


@icon("linear-actuator", CAT, "Long actuator tube with a motor housing at one end and a push rod",
      tags=["actuator", "linear motor", "push rod", "electric ram", "extend", "retract"])
def _(S):
    body = union(rect(2.5, 5.5, 7, 13, rr(S, 2)), rect(8, 8.5, 9, 7, L(S, 0, 1)))
    return [
        shell(body),
        detail(seg(6, 5.5, 6, 18.5)),
        line(seg(17, 12, 20, 12)),
        line(seg(20.5, 9, 20.5, 15) if S.name == "line" else seg(20.5, 10, 20.5, 14)),
    ]


@icon("peltier-module", CAT, "Thermoelectric cooler: two ceramic plates sandwiching a row of pellets, with two wires",
      tags=["peltier", "thermoelectric", "tec", "cooler", "heat pump", "cooling module"])
def _(S):
    pellets = [line(seg(x, 7.5, x, 11.5)) for x in (5.5, 9.5, 13.5, 17.5)]
    return [
        shell(rect(2.5, 4, 18, 3.5, L(S, 0, 1.25))),
        *pellets,
        shell(rect(2.5, 11.5, 18, 3.5, L(S, 0, 1.25))),
        vseg(S, 8, 15, 22),
        vseg(S, 13, 15, 22),
    ]


@icon("case-fan", CAT, "Square computer case fan with corner screw holes, a hub and curved blades",
      tags=["pc fan", "cooling fan", "computer fan", "cooler", "airflow", "chassis fan"])
def _(S):
    blades = []
    for k in range(4):
        a = k * 90 + 20
        x1, y1 = polar(12, 12, 3, a)
        x2, y2 = polar(12, 12, 7, a + 55)
        blades.append(detail(f"M{fmt(x1)} {fmt(y1)}A6 6 0 0 1 {fmt(x2)} {fmt(y2)}"))
    holes = [dot(x, y, 1) for x in (6, 18) for y in (6, 18)]
    return [shell(rect(2.5, 2.5, 19, 19, rr(S, 3))), *blades, *holes, dot(12, 12, 1.75)]


# ============================================================================ switching and power

@icon("solid-state-relay", CAT, "Solid state relay block with four screw terminals and an indicator light",
      tags=["ssr", "relay", "solid state", "switch", "ac switch", "control"])
def _(S):
    screws = [dot(x, y, 1.75) for x in (6.5, 17.5) for y in (8.5, 15.5)]
    return [
        shell(rect(2.5, 4.5, 19, 15, rr(S, 3))),
        *screws,
        dot(12, 8.5, 1.1),
        detail(seg(10 + L(S, 0, 1), 14.5, 14 - L(S, 0, 1), 14.5)),
    ]


@icon("contactor", CAT, "Contactor block with rows of screw terminals top and bottom and a window",
      tags=["contactor", "motor starter", "magnetic switch", "power relay", "switchgear", "control panel"])
def _(S):
    screws = [dot(x, y, 1.25) for x in (7, 12, 17) for y in (5.75, 18.25)]
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 2.5))),
        *screws,
        detail(rect(7.5, 10, 9, 4, L(S, 0, 1))),
    ]


@icon("toroidal-transformer", CAT, "Thick donut transformer with a mounting bolt and wires",
      tags=["toroidal", "transformer", "toroid", "power supply", "mains transformer", "audio transformer"])
def _(S):
    hexa = poly(regular(12, 10, 2, 6, start=L(S, 0, 30)), closed=True)
    return [
        shell(ring(12, 10, 8, 3.75)),
        Part("dot", hexa),
        vseg(S, 7, 16, 22),
        vseg(S, 10.33, 17.9, 22),
        vseg(S, 13.67, 17.9, 22),
        vseg(S, 17, 16, 22),
    ]


# ============================================================================ batteries

@icon("lipo-battery", CAT, "Flat lithium polymer pouch cell with two wires and a small plug",
      tags=["lipo", "li-po", "lithium polymer", "pouch cell", "rc battery", "drone battery"])
def _(S):
    e = L(S, 0, 1)
    return [
        shell(rect(2.5, 5, 12, 14, rr(S, 2))),
        detail(seg(6.5 + e, 12, 10.5 - e, 12)),
        detail(seg(8.5, 10 + e, 8.5, 14 - e)),
        line(seg(14.5, 10, 17.5, 10)),
        line(seg(14.5, 14, 17.5, 14)),
        shell(rect(17.5, 8, 4, 8, L(S, 0, 1))),
    ]


@icon("battery-holder", CAT, "Battery holder tray with two cylindrical cells side by side and wires",
      tags=["battery holder", "battery box", "aa holder", "cell holder", "battery pack", "battery case"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 14.5, rr(S, 2))),
        detail(rect(6.5, 6, 4, 7.5, L(S, 0, 2))),
        detail(rect(13.5, 6, 4, 7.5, L(S, 0, 2))),
        vseg(S, 9.5, 17, 22),
        vseg(S, 14.5, 17, 22),
    ]


@icon("battery-snap", CAT, "Nine volt battery snap with a round and a hexagonal stud and two wires",
      tags=["9v snap", "battery clip", "battery connector", "9 volt", "snap connector", "pp3 clip"])
def _(S):
    hexa = poly(regular(15.5, 9.5, 2.6, 6, start=L(S, 0, 30)), closed=True)
    return [
        shell(rect(3, 4.5, 18, 10, rr(S, 3))),
        detail(circle(8.5, 9.5, 2.25)),
        detail(hexa),
        vseg(S, 10, 14.5, 22),
        vseg(S, 14, 14.5, 22),
    ]


@icon("battery-tester", CAT, "Battery tester with a needle dial above a slot holding a cell",
      tags=["battery checker", "battery meter", "cell tester", "charge level", "test battery", "voltage check"])
def _(S):
    x1, y1 = polar(12, 12, 6, 205)
    x2, y2 = polar(12, 12, 6, 335)
    nx, ny = polar(12, 12, 5.5, 295)
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 3))),
        detail(f"M{fmt(x1)} {fmt(y1)}A6 6 0 0 1 {fmt(x2)} {fmt(y2)}"),
        detail(seg(12, 11.5, nx, ny)),
        sq(6.5, 15.5, 10, 3, L(S, 0, 1)),
        sq(16.5, 16.25, 1.5, 1.5),
    ]


@icon("buck-converter", CAT, "Small DC to DC converter board with a round coil, a chip and screw terminals",
      tags=["buck converter", "dc-dc", "step down", "voltage converter", "power module", "regulator board"])
def _(S):
    terms = [dot(x, y, 1.25) for x in (5.75, 18.25) for y in (9, 15)]
    return [
        shell(rect(2.5, 5, 19, 14, rr(S, 2.5))),
        *terms,
        detail(circle(12, 12, 3.25)),
    ]


@icon("voltage-regulator", CAT, "Three legged voltage regulator with a metal tab, mounting hole and V label",
      tags=["regulator", "linear regulator", "to-220", "ldo", "power ic"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 15, rr(S, 2))),
        detail(seg(6, 8.5, 18, 8.5)),
        dot(12, 5.5, 1.3),
        detail(poly([(10, 11), (12, 15), (14, 11)], r=L(S, 0, 0.5)), stroke_miterlimit="3"),
        vseg(S, 8.5, 17.5, 22),
        vseg(S, 12, 17.5, 22),
        vseg(S, 15.5, 17.5, 22),
    ]


@icon("bridge-rectifier", CAT, "Square bridge rectifier block with four legs and AC plus and minus marks",
      tags=["rectifier", "diode bridge", "ac to dc", "full wave", "power supply", "bridge"])
def _(S):
    e = L(S, 0, 0.75)
    return [
        shell(rect(4, 3, 16, 14, rr(S, 2.5))),
        detail(seg(6.5 + e, 7.5, 10.5 - e, 7.5)), detail(seg(8.5, 5.5 + e, 8.5, 9.5 - e)),
        detail(seg(13.5 + e, 7.5, 17.5 - e, 7.5)),
        detail("M9.5 13.5C10.5 11.5 11.5 11.5 12 13S13.5 14.5 14.5 12.5"),
        *[vseg(S, x, 17, 22) for x in (6.5, 10, 14, 17.5)],
    ]


@icon("capacitor-bank", CAT, "Row of three tall capacitors joined by a bus bar across their tops",
      tags=["capacitors", "capacitor array", "power factor", "energy storage", "filter bank", "cap bank"])
def _(S):
    caps = [shell(rect(x, 6, 4, 15, L(S, 0.5, 2))) for x in (3, 10, 17)]
    return [line(seg(L(S, 2.5, 3.5), 4, L(S, 21.5, 20.5), 4)), *caps]


@icon("busbar", CAT, "Flat metal bus bar with a row of evenly spaced bolt holes",
      tags=["bus bar", "copper bar", "power distribution", "conductor", "switchboard", "earth bar"])
def _(S):
    return [
        shell(rect(2.5, 8.5, 19, 7, rr(S, 3))),
        *[dot(x, 12, 1.3) for x in (6, 10, 14, 18)],
    ]


@icon("din-rail", CAT, "Length of top hat DIN rail with slotted mounting holes",
      tags=["din rail", "top hat rail", "mounting rail", "rail", "control panel", "35mm rail"])
def _(S):
    e = L(S, 0, 1)
    return [
        shell(rect(2, 5.5, 20, 13, L(S, 0, 1))),
        detail(seg(2, 9, 22, 9)),
        detail(seg(2, 15, 22, 15)),
        *[detail(seg(x + e, 12, x + 4 - e, 12)) for x in (4.5, 10, 15.5)],
    ]


@icon("slip-ring", CAT, "Slip ring cylinder with stacked rings and wires out of each end",
      tags=["slip ring", "rotary joint", "rotating connector", "commutator", "swivel", "rotary electrical"])
def _(S):
    wires = []
    for y in (8, 12, 16):
        wires += [hseg(S, 6.5, 2, y), hseg(S, 17.5, 22, y)]
    return [
        shell(rect(6.5, 4, 11, 16, rr(S, 2))),
        detail(seg(10.25, 4, 10.25, 20)),
        detail(seg(13.75, 4, 13.75, 20)),
        *wires,
    ]


@icon("rheostat", CAT, "Wire wound rheostat coil with a sliding contact on a bar above it",
      tags=["rheostat", "variable resistor", "slide resistor", "potentiometer", "resistance", "dimmer"])
def _(S):
    return [
        line(seg(L(S, 2.5, 3.5), 4.5, L(S, 21.5, 20.5), 4.5)),
        sq(12, 2.5, 5, 4, L(S, 0, 1.25)),
        line(seg(14.5, 6.5, 14.5, 10)),
        shell(rect(3, 11, 18, 9, rr(S, 2.5))),
        *[detail(seg(x, 11, x, 20)) for x in (7, 11, 15, 19)[:3]],
    ]


@icon("decade-resistance-box", CAT, "Decade resistance box with a row of dials and two terminals",
      tags=["decade box", "resistance box", "resistor substitution", "lab instrument", "calibration", "test equipment"])
def _(S):
    return [
        line(seg(7, L(S, 2.5, 3.5), 7, 7)),
        line(seg(17, L(S, 2.5, 3.5), 17, 7)),
        shell(rect(2.5, 7, 19, 13, rr(S, 2.5))),
        *[detail(circle(x, 13.5, 1.5)) for x in (7, 12, 17)],
    ]


@icon("heating-cartridge", CAT, "Cartridge heater rod with two wires out of one end and heat waves above",
      tags=["cartridge heater", "heater", "heating element", "3d printer heater", "hot end", "resistive heater"])
def _(S):
    waves = [line(f"M{x} 9.5C{x - 1.5} 8 {x + 1.5} 6 {x} 4" + ("" if S.name == "line" else "")) for x in (5.5, 9.5, 13.5)]
    return [
        *waves,
        shell(rect(2.5, 12.5, 13.5, 7, rr(S, 2))),
        hseg(S, 16, 22, 14.25),
        hseg(S, 16, 22, 17.75),
    ]


@icon("tube-socket", CAT, "Vacuum tube socket with a ring of pin holes, a centre key and mounting ears",
      tags=["valve socket", "tube socket", "octal socket", "vacuum tube", "amplifier", "valve base"])
def _(S):
    body = union(circle(12, 12, 7.5), rect(2.5, 9, 19, 6, L(S, 0, 3)))
    holes = [dot(*polar(12, 12, 4.5, 22.5 + k * 45), 0.9) for k in range(8)]
    return [shell(body), *holes, dot(12, 12, 1.2), dot(4.75, 12, 1), dot(19.25, 12, 1)]


@icon("shield-can", CAT, "Metal shield can with vent holes soldered onto a circuit board",
      tags=["rf shield", "emi shield", "shielding can", "faraday cage", "shield cover", "pcb shield"])
def _(S):
    return [
        shell(rect(4.5, 5, 15, 13, rr(S, 2))),
        *[dot(x, y, 1) for x in (8.5, 12, 15.5) for y in (9, 13.5)],
        line(seg(L(S, 2, 3), 20, L(S, 22, 21), 20)),
    ]


# ============================================================================ sensors, headers and connectors

@icon("slot-optical-sensor", CAT, "U shaped slotted optical sensor with a gap between two uprights and legs below",
      tags=["photo interrupter", "optical switch", "slot sensor", "opto interrupter", "encoder sensor", "beam break"])
def _(S):
    body = [(3, 3.5), (9, 3.5), (9, 10.5), (15, 10.5), (15, 3.5), (21, 3.5), (21, 16.5), (3, 16.5)]
    return [
        shell(poly(body, closed=True, r=L(S, 0, 1.5))),
        *[vseg(S, x, 16.5, 22) for x in (6, 10, 14, 18)],
    ]


@icon("female-header", CAT, "Female pin header strip with a row of square sockets and pins below",
      tags=["pin header", "socket header", "female connector", "breadboard", "header socket", "jumper wire"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 19, 9, rr(S, 1.5))),
        *[sq(x - 1, 9, 2, 2, L(S, 0, 0.5)) for x in (6, 10, 14, 18)],
        *[vseg(S, x, 14.5, 21.5) for x in (6, 10, 14, 18)],
    ]


@icon("jumper-cap", CAT, "Small jumper cap bridging two header pins",
      tags=["jumper", "shunt", "jumper shunt", "header jumper", "configuration", "bridge pins"])
def _(S):
    return [
        *[line(seg(x, 6, x, 14)) for x in (5, 9.5)],
        shell(rect(11.5, 3.5, 9.5, 9, rr(S, 2))),
        shell(rect(2.5, 14, 19, 4, L(S, 0, 1.5))),
        *[vseg(S, x, 18, 22) for x in (5, 9.5, 14, 18.5)],
    ]


@icon("wire-to-board-connector", CAT, "Small keyed plug with a latch and a row of wires entering the back",
      tags=["wire connector", "board connector", "plug", "crimp housing", "pcb connector", "cable connector"])
def _(S):
    body = union(rect(3, 5, 11, 14, rr(S, 1.5)), poly([(5.5, 5.5), (5.5, 2.5), (10.5, 2.5), (12, 5.5)], closed=True))
    return [
        shell(body),
        *[dot(6.5, y, 1) for y in (8.5, 12, 15.5)],
        *[hseg(S, 14, 22, y) for y in (8, 12, 16)],
    ]


@icon("banana-plug", CAT, "Banana plug with a grip body, a cable and a slotted spring pin tip",
      tags=["banana plug", "test lead", "4mm plug", "multimeter lead", "binding post", "probe plug"])
def _(S):
    tip = "M9 9.5C6 9.5 3 10 2.5 12C3 14 6 14.5 9 14.5Z"
    return [
        shell(tip),
        shell(rect(9, 7.5, 9, 9, rr(S, 2.5))),
        hseg(S, 18, 22, 12),
    ]


@icon("bnc-connector", CAT, "BNC plug with a bayonet collar and its slot, a body and a cable",
      tags=["bnc", "coax connector", "oscilloscope", "video connector", "rf connector", "bayonet connector"])
def _(S):
    body = union(rect(2.5, 8.5, 5, 7, L(S, 0, 1)), rect(7, 5, 8, 14, rr(S, 2)), rect(14.5, 8, 4, 8, L(S, 0, 1)))
    return [
        shell(body),
        detail(poly([(7, 9), (11, 9), (11, 12.5)], r=L(S, 0, 1))),
        hseg(S, 18.5, 22, 12),
    ]


@icon("test-hook-clip", CAT, "Test hook clip: a pen shaped grabber with a thin hook out of its tip",
      tags=["test hook", "grabber", "ic clip", "probe clip", "test clip", "hook probe"])
def _(S):
    body = poly([(10.5, 9), (13.5, 9), (15, 12), (15, 22), (9, 22), (9, 12)], closed=True, r=L(S, 0, 1))
    if S.name == "rounded":
        body = "M10.5 9H13.5L15 12V20A1.5 1.5 0 0 1 13.5 21.5H10.5A1.5 1.5 0 0 1 9 20V12Z"
    return [
        shell(body),
        line("M12 9V5A2 2 0 0 0 8 5V6" if S.name == "line" else "M12 9V5A2 2 0 0 0 8 5V5.5"),
        detail(seg(9, 16, 15, 16)),
    ]


@icon("spade-terminal", CAT, "Crimp spade terminal with a forked tip, a barrel and a wire",
      tags=["spade connector", "fork terminal", "crimp terminal", "wire terminal", "u terminal", "crimp"])
def _(S):
    fork = [(2.5, 6), (10, 6), (10, 18), (2.5, 18), (2.5, 14), (6.5, 14), (6.5, 10), (2.5, 10)]
    body = union(poly(fork, closed=True, r=L(S, 0, 1)), rect(9.5, 8.5, 8.5, 7, rr(S, 2)))
    return [
        shell(body),
        detail(seg(13.5, 8.5, 13.5, 15.5)),
        hseg(S, 18, 22, 12),
    ]


@icon("butt-splice-connector", CAT, "Butt splice connector tube with a wire entering each end",
      tags=["butt connector", "splice", "crimp connector", "wire joint", "inline connector", "wire splice"])
def _(S):
    return [
        shell(rect(6, 8, 12, 8, rr(S, 2.5))),
        detail(seg(12, 8, 12, 16)),
        hseg(S, 6, 2, 12),
        hseg(S, 18, 22, 12),
    ]


@icon("bullet-connector", CAT, "Pair of male and female bullet crimp connectors about to join",
      tags=["bullet connector", "banana connector", "crimp connector", "rc connector", "male female", "wire connector"])
def _(S):
    return [
        shell(rect(2.5, 8, 6.5, 8, rr(S, 2))),
        line(seg(9, 12, 11, 12)),
        dot(11.5, 12, 1.75),
        shell(rect(15, 8, 6.5, 8, rr(S, 2))),
        detail(seg(15, 12, 18.5, 12)),
    ]


@icon("circular-connector", CAT, "Round multi-pin connector face with a threaded coupling ring",
      tags=["circular connector", "mil spec", "aviation plug", "multi pin", "panel connector", "round connector"])
def _(S):
    pts = [polar(12, 12, 3.25, -54 + k * 72) for k in range(5)] + [(12, 12)]
    if S.name == "line":
        pins = [sq(x - 0.9, y - 0.9, 1.8, 1.8) for x, y in pts]
    else:
        pins = [dot(x, y, 1) for x, y in pts]
    return [
        shell(ring(12, 12, 9.5, 6.5)),
        *pins,
        sq(11, 5.5, 2, 2) if S.name == "line" else dot(12, 6.25, 1.1),
    ]


# ============================================================================ plugs, jacks and slots

def _usb_plug(S, tip, body, extra=()):
    return [shell(union(tip, body)), *extra, vseg(S, 12, 18, 22)]


@icon("micro-usb-connector", CAT, "Micro USB plug with a small trapezoid tip, a grip and a short cable",
      tags=["micro usb", "micro-b", "usb plug", "phone charger", "charging cable", "android charger"])
def _(S):
    tip = poly([(8.5, 5), (15.5, 5), (15.5, 8.5), (14, 11), (10, 11), (8.5, 8.5)], closed=True, r=L(S, 0, 0.6))
    return _usb_plug(S, tip, rect(7, 11, 10, 7, rr(S, 2)))


@icon("usb-type-b-connector", CAT, "USB type B plug with a square tip with bevelled top corners and a cable",
      tags=["usb b", "type b", "printer cable", "usb plug", "square usb", "usb-b"])
def _(S):
    tip = poly([(8, 5.5), (10, 3), (14, 3), (16, 5.5), (16, 11), (8, 11)], closed=True, r=L(S, 0, 0.6))
    return _usb_plug(S, tip, rect(6.5, 11, 11, 7, rr(S, 2)), [detail(seg(10.5, 7, 13.5, 7))])


@icon("usb-type-a-connector", CAT, "USB type A plug with a flat metal tip, two square holes and a cable",
      tags=["usb a", "type a", "usb plug", "usb cable", "flash drive plug", "usb-a"])
def _(S):
    tip = rect(7, 2.5, 10, 8.5, L(S, 0, 1))
    holes = [sq(9, 5.5, 2, 2, L(S, 0, 0.5)), sq(13, 5.5, 2, 2, L(S, 0, 0.5))]
    return _usb_plug(S, tip, rect(6, 11, 12, 7, rr(S, 2)), holes)


@icon("fiber-optic-connector", CAT, "Square fibre optic plug with a thin ferrule tip, a boot and a cable",
      tags=["fiber optic", "fibre optic", "sc connector", "lc connector", "optical fiber", "patch cord"])
def _(S):
    body = union(rect(7.5, 6, 9, 12, rr(S, 2)), poly([(16, 8.5), (20, 10.5), (20, 13.5), (16, 15.5)], closed=True))
    return [
        shell(body),
        line(seg(L(S, 2.5, 3.5), 12, 7.5, 12)),
        detail(seg(10.5, 6, 10.5, 18)),
        hseg(S, 20, 22, 12),
    ]


@icon("keystone-jack", CAT, "Snap-in keystone jack module with a network port on its face and wire slots on top",
      tags=["keystone", "rj45 jack", "network jack", "ethernet jack", "wall jack", "cat6"])
def _(S):
    port = [(8, 10.5), (16, 10.5), (16, 15.5), (14, 15.5), (14, 17.5), (10, 17.5), (10, 15.5), (8, 15.5)]
    return [
        *[vseg(S, x, 6.5, 2.5) for x in (8, 12, 16)],
        shell(rect(4.5, 6.5, 15, 15, rr(S, 2.5))),
        detail(poly(port, closed=True, r=L(S, 0, 0.6))),
    ]


@icon("pcie-slot", CAT, "Long expansion slot with a short and a long section and a latch at one end",
      tags=["pcie", "pci express", "expansion slot", "graphics card slot", "motherboard", "x16 slot"])
def _(S):
    e = L(S, 0, 1)
    return [
        shell(union(rect(2, 8.5, 17, 7, rr(S, 1.5)), rect(17.5, 6, 4.5, 12, rr(S, 1.5)))),
        detail(seg(4.5 + e, 12, 6.5 - e, 12)),
        detail(seg(9.5 + e, 12, 15.5 - e, 12)),
    ]


@icon("dimm-slot", CAT, "Long memory slot with a key and clips at both ends",
      tags=["dimm slot", "ram slot", "memory slot", "motherboard", "ddr slot", "memory socket"])
def _(S):
    e = L(S, 0, 1)
    body = union(rect(2, 6, 4, 12, rr(S, 1.5)), rect(5.5, 8.5, 13, 7, L(S, 0, 1)), rect(18, 6, 4, 12, rr(S, 1.5)))
    return [
        shell(body),
        detail(seg(6 + e, 12, 9.5 - e, 12)),
        detail(seg(12.5 + e, 12, 18 - e, 12)),
    ]


# ============================================================================ cables and cable management

def _wave(x0, x1, y, amp, half, phase=1):
    """Sine-like wave from x0 to x1 built from cubic half waves (half = half period)."""
    d = f"M{fmt(x0)} {fmt(y)}"
    x, s = x0, phase
    k = 1.27 * amp
    while x < x1 - 1e-6:
        h = min(half, x1 - x)
        d += (f"C{fmt(x + h * 0.35)} {fmt(y - s * k * h / half)} {fmt(x + h * 0.65)} {fmt(y - s * k * h / half)} "
              f"{fmt(x + h)} {fmt(y)}")
        x += h
        s = -s
    return d


@icon("twisted-pair-cable", CAT, "Two insulated wires twisted around each other in a regular helix",
      tags=["twisted pair", "network cable", "cat5", "cat6", "utp", "ethernet cable"])
def _(S):
    x0, x1 = L(S, 2, 3), L(S, 22, 21)
    return [
        line(_wave(x0, x1, 12, 4, (x1 - x0) / 4, 1)),
        line(_wave(x0, x1, 12, 4, (x1 - x0) / 4, -1)),
    ]


def _loops(x0, y, n, pitch, b, r):
    """Coiled cord drawn as a row of overlapping loops (prolate cycloid), sampled into smooth cubics.

    Starts at (x0, y); pitch = advance per loop, b = horizontal loop radius, r = vertical loop radius."""
    pts = []
    steps = 10 * n
    a = pitch / (2 * math.pi)
    span = 2 * math.pi * (n - 1) + math.pi  # finish on the far side of the last loop, at mid height
    for i in range(steps + 1):
        t = span * i / steps + math.pi / 2
        pts.append((x0 + a * (t - math.pi / 2) - b * (math.sin(t) - 1), y - r * math.cos(t)))
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(len(pts) - 1):
        p0 = pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(i + 2, len(pts) - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d


@icon("coiled-cable", CAT, "Cable wound into a tight spring coil between two plugs",
      tags=["coiled cord", "spiral cable", "curly cord", "telephone cord", "coil cable", "stretch cable"])
def _(S):
    return [
        sq(2, 8.5, 3, 7, L(S, 0, 1.2)),
        line(_loops(4.5, 12, 3, 3.4, 2.6, 4.5)),
        sq(19, 8.5, 3, 7, L(S, 0, 1.2)),
    ]


@icon("y-splitter-cable", CAT, "Y splitter cable: one plug whose cable splits into two branches with plugs",
      tags=["y cable", "splitter", "y adapter", "cable splitter", "one to two", "branch cable"])
def _(S):
    return [
        shell(rect(2.5, 9.5, 5, 5, L(S, 0, 1.5))),
        line("M7.5 12H10C12.5 12 12.5 6 15 6H16"),
        line("M10 12C12.5 12 12.5 18 15 18H16"),
        shell(rect(16, 3.5, 5.5, 5, L(S, 0, 1.5))),
        shell(rect(16, 15.5, 5.5, 5, L(S, 0, 1.5))),
    ]


@icon("heat-shrink-tubing", CAT, "Heat shrink tube over a wire joint with heat waves rising above it",
      tags=["heat shrink", "shrink tube", "heatshrink", "insulation", "wire repair", "sleeving"])
def _(S):
    waves = [line(f"M{x} 9.5C{x - 1.5} 8 {x + 1.5} 6 {x} 4") for x in (9.5, 14.5)]
    return [
        *waves,
        hseg(S, 7, 2, 16.5),
        shell(rect(7, 13, 10, 7, rr(S, 2))),
        hseg(S, 17, 22, 16.5),
    ]


@icon("braided-cable-sleeve", CAT, "Braided sleeve with a woven crosshatch covering a bundle of wires",
      tags=["braided sleeve", "cable sleeve", "expandable sleeving", "cable management", "wire loom", "mesh sleeve"])
def _(S):
    return [
        hseg(S, 6, 2, 10), hseg(S, 6, 2, 14),
        shell(rect(6, 6.5, 12, 11, rr(S, 2))),
        detail(poly([(6.5, 7), (12, 17), (17.5, 7)])),
        detail(poly([(6.5, 17), (12, 7), (17.5, 17)])),
        hseg(S, 18, 22, 10), hseg(S, 18, 22, 14),
    ]


@icon("cable-ferrule", CAT, "Wire end ferrule: a metal tube with a plastic collar crimped onto a wire",
      tags=["ferrule", "wire ferrule", "bootlace ferrule", "crimp", "wire end", "end sleeve"])
def _(S):
    body = union(rect(2.5, 9.5, 9, 5, L(S, 0, 1)), poly([(11, 7), (17.5, 8.5), (17.5, 15.5), (11, 17)], closed=True, r=L(S, 0, 1)))
    return [
        shell(body),
        detail(seg(11, 9.5, 11, 14.5)),
        hseg(S, 17.5, 22, 12),
    ]


@icon("cable-harness", CAT, "Wiring harness: a tied bundle of wires branching out to three connectors",
      tags=["wire harness", "wiring loom", "cable assembly", "loom", "automotive wiring", "cable bundle"])
def _(S):
    return [
        shell(rect(2.5, 10, 7.5, 4, L(S, 0, 1.5))),
        line("M10 12C13 12 13 5 16 5"),
        line(seg(10, 12, 16, 12)),
        line("M10 12C13 12 13 19 16 19"),
        *[shell(rect(16, y - 2, 5.5, 4, L(S, 0, 1.5))) for y in (5, 12, 19)],
    ]


@icon("cable-comb", CAT, "Cable comb plate with wires passing straight through its holes",
      tags=["cable comb", "wire comb", "cable organiser", "cable organizer", "dressing tool", "cable management"])
def _(S):
    ys = (6, 10, 14, 18)
    parts = [shell(rect(9.5, 2.5, 5, 19, rr(S, 2)))]
    for y in ys:
        parts += [hseg(S, 9.5, 2, y), hseg(S, 14.5, 22, y)]
    parts += [dot(12, y, 1) for y in ys]
    return parts


@icon("wire-marker", CAT, "Printed wire marker sleeve with a number slipped over a wire",
      tags=["wire label", "cable marker", "wire number", "cable label", "ferrule marker", "identification"])
def _(S):
    return [
        hseg(S, 6, 2, 12),
        shell(rect(6, 6, 12, 12, rr(S, 2))),
        detail(poly([(10.5, 10), (12.5, 9), (12.5, 15)], r=L(S, 0, 0.5)), stroke_miterlimit="3"),
        hseg(S, 18, 22, 12),
    ]


def _rot(pts, deg, c=(12, 12)):
    a = math.radians(deg)
    return [(c[0] + (x - c[0]) * math.cos(a) - (y - c[1]) * math.sin(a),
             c[1] + (x - c[0]) * math.sin(a) + (y - c[1]) * math.cos(a)) for x, y in pts]


@icon("ground-strap", CAT, "Flat braided ground strap with a ring terminal at each end",
      tags=["ground strap", "earth strap", "bonding strap", "braided strap", "grounding", "earth bond"])
def _(S):
    strap = poly(_rot([(6, 9.5), (18, 9.5), (18, 14.5), (6, 14.5)], 45), closed=True)
    body = union(strap, circle(5.5, 5.5, 3.5), circle(18.5, 18.5, 3.5))
    cross = [detail(poly(_rot([(x, 9.5), (x, 14.5)], 45))) for x in (10.5, 13.5)]
    return [shell(body), *cross, dot(5.5, 5.5, 1.2), dot(18.5, 18.5, 1.2)]


@icon("grounding-clamp", CAT, "Ground clamp around a pipe with a wire from its bolt to an earth symbol",
      tags=["ground clamp", "earth clamp", "pipe clamp", "bonding", "earthing", "grounding"])
def _(S):
    e = L(S, 0, 1)
    body = union(circle(8, 8, 5.5), rect(11, 5.5, 8, 5, L(S, 0, 1.5)))
    return [
        shell(body),
        detail(circle(8, 8, 2)),
        dot(16, 8, 1.1),
        line(seg(16, 10.5, 16, 14.5)),
        line(seg(11.5 + e, 14.5, 20.5 - e, 14.5)),
        line(seg(13 + e, 17.5, 19 - e, 17.5)),
        line(seg(14.5 + e * 0.5, 20.5, 17.5 - e * 0.5, 20.5)),
    ]


@icon("cable-tester", CAT, "Network cable tester: a main unit and a remote, each with a jack and a row of lights",
      tags=["cable tester", "network tester", "lan tester", "continuity tester", "rj45 tester", "wire tester"])
def _(S):
    return [
        shell(rect(2.5, 3, 11, 18.5, rr(S, 2.5))),
        sq(5.5, 6, 5, 4, L(S, 0, 1)),
        *[dot(x, y, 1) for x in (6, 10) for y in (13.5, 17.5)],
        shell(rect(15.5, 8, 6, 13.5, rr(S, 2))),
        sq(17, 11, 3, 3, L(S, 0, 0.8)),
        dot(18.5, 17.5, 1),
    ]
