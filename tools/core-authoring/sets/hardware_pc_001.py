"""TypeIcon Core: hardware-pc (batch 001): cooling, drives, connectors, computers, peripherals and controllers.

Generic parts only: no brand shapes. Front or side views, flat to the grid.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "hardware-pc"


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def kdot(d) -> Part:
    return Part("dot", d)


def head(x, y, dx, dy, s=2.0):
    """Arrow head polyline at tip (x, y) pointing along (dx, dy)."""
    n = math.hypot(dx, dy)
    dx, dy = dx / n, dy / n
    px, py = -dy, dx
    return [(x - dx * s + px * s, y - dy * s + py * s), (x, y), (x - dx * s - px * s, y - dy * s - py * s)]


# ============================================================================ cooling

@icon("heat-pipe", CAT, "Two heat pipes rising from a flat base through a stack of fins",
      tags=["heatpipe", "cooler", "heatsink", "cpu cooler", "copper pipe", "thermal"])
def _(S):
    parts = [shell(rect(3, 18, 18, 3, rr(S, 1.5))),
             line("M8.5 18V6.5a3.5 3.5 0 0 1 7 0V18")]
    for y in (7.5, 11.5, 15):
        parts += [line(seg(3, y, 6.5, y)), line(seg(10.5, y, 13.5, y)), line(seg(17.5, y, 21, y))]
    return parts


@icon("blower-fan", CAT, "Blower fan housing with a ring of impeller blades and an open outlet on one side",
      tags=["centrifugal fan", "turbine fan", "cooler", "airflow", "ventilation", "laptop fan"])
def _(S):
    parts = [line(poly([(21, 8), (21, 4), (10, 4)], r=S.r)),
             line("M10 4A8 8 0 0 0 10 20"),
             line(poly([(10, 20), (21, 20), (21, 16)], r=S.r))]
    for a in (0, 90, 180, 270):
        x0, y0 = polar(10, 12, 2.5, a + 20)
        x1, y1 = polar(10, 12, 5.8, a - 10)
        parts.append(line(seg(x0, y0, x1, y1)))
    parts.append(shell(circle(10, 12, 2.5)))
    return parts


@icon("water-cooling-reservoir", CAT, "Upright coolant reservoir with a wavy liquid level and two tube fittings on top",
      tags=["liquid cooling", "coolant tank", "watercooling", "pc cooling", "loop", "custom loop"])
def _(S):
    return [
        shell(rect(7, 7, 10, 14, rr(S, 3))),
        detail("M7 13c1.7-1.6 3.3-1.6 5 0s3.3 1.6 5 0"),
        line(poly([(10, 7), (10, 3), (4, 3)], r=S.r)),
        line(poly([(14, 7), (14, 3), (20, 3)], r=S.r)),
    ]


@icon("cpu-water-block", CAT, "Square water block with a round window of fine channels and two tube fittings on top",
      tags=["waterblock", "liquid cooler", "cpu cooler", "water cooling", "cold plate", "loop"])
def _(S):
    return [
        shell(rect(2, 6, 20, 15, rr(S, 3))),
        line(seg(7, 2.5, 7, 6)),
        line(seg(17, 2.5, 17, 6)),
        detail(circle(12, 13.5, 5)),
        detail(seg(10.5, 11.5, 10.5, 15.5)),
        detail(seg(13.5, 11.5, 13.5, 15.5)),
    ]


@icon("thermal-pad", CAT, "Soft square thermal pad with a dotted texture and one corner peeled up",
      tags=["thermal paste", "heat transfer", "gap pad", "cooling", "vrm", "heatsink"])
def _(S):
    return [
        shell(poly([(4, 4), (20, 4), (20, 12), (12, 20), (4, 20)], closed=True, r=S.r)),
        detail(poly([(12, 20), (12, 12), (20, 12)], r=S.r * 0.5)),
        dot(8, 8, 1.1), dot(13, 8, 1.1), dot(8, 13, 1.1), dot(16, 8, 1.1),
    ]


@icon("fan-controller", CAT, "Small hub board with four pin headers and a cable running to a fan",
      tags=["fan hub", "pwm", "fan speed", "rgb hub", "pc cooling", "header"])
def _(S):
    return [
        shell(rect(2, 3, 15, 8, rr(S, 2))),
        sq(4.5, 5.5, 2, 3), sq(8, 5.5, 2, 3), sq(11.5, 5.5, 2, 3),
        line(poly([(9.5, 11), (9.5, 18), (14.5, 18)], r=S.r)),
        shell(circle(18, 18, 3.5)),
        dot(18, 18, 1),
    ]


@icon("pc-dust-filter", CAT, "Fine mesh filter in a thin frame pulled half out of a slot, with a pull tab",
      tags=["dust screen", "mesh filter", "intake filter", "case filter", "airflow", "cleaning"])
def _(S):
    return [
        line(seg(3, 3, 3, 21)),
        line(seg(3, 6, 8, 6)),
        line(seg(3, 18, 8, 18)),
        shell(rect(8, 6, 11, 12, rr(S, 1.5))),
        detail(seg(13.5, 6, 13.5, 18)),
        detail(seg(8, 12, 19, 12)),
        line(seg(19, 12, 22, 12)),
    ]


@icon("immersion-cooling-tank", CAT, "Open-top tank of liquid with server boards submerged and bubbles rising",
      tags=["liquid immersion", "dielectric", "data center cooling", "server cooling", "two phase", "coolant"])
def _(S):
    return [
        line(poly([(4, 3), (4, 21), (20, 21), (20, 3)], r=S.r)),
        detail("M4 8c2-1.5 4-1.5 6 0s4 1.5 6 0 3-1 4 0"),
        line(seg(8, 14, 8, 18)),
        line(seg(12, 14, 12, 18)),
        line(seg(16, 14, 16, 18)),
        dot(10, 11.5, 1), dot(14, 11.8, 1),
    ]


@icon("laptop-cooling-pad", CAT, "Sloped cooling stand with a round fan grille and a laptop resting on top",
      tags=["laptop stand", "cooler pad", "notebook cooler", "fan stand", "airflow", "heat"])
def _(S):
    return [
        shell(poly([(2, 21), (22, 21), (22, 17), (2, 11)], closed=True, r=S.r * 0.6)),
        detail(circle(12, 17.5, 2)),
        line(seg(4, 8.5, 18, 12)),
        line(seg(4, 8.5, 3.5, 2.5)),
    ]


@icon("cpu-temperature", CAT, "Processor chip with pins and a thermometer beside its lower right corner",
      tags=["cpu temp", "heat", "thermal monitoring", "processor", "overheating", "sensor"])
def _(S):
    parts = [shell(rect(5, 5, 10, 10, rr(S, 2)))]
    for v in (8, 12):
        parts += [line(seg(v, 2.5, v, 5)), line(seg(v, 15, v, 17.5)),
                  line(seg(2.5, v, 5, v)), line(seg(15, v, 16.8, v))]
    parts += [line(seg(19, 10, 19, 16.5)), solid(circle(19, 19, 2.5))]
    return parts


@icon("case-airflow", CAT, "Computer case in side view with arrows entering the front and leaving through the top and back",
      tags=["airflow", "ventilation", "case fans", "cooling", "intake", "exhaust", "pc cooling"])
def _(S):
    return [
        shell(rect(5, 7, 14, 14, rr(S, 2.5))),
        line(seg(1.5, 17.5, 10, 17.5)), line(poly(head(10, 17.5, 1, 0, 2), r=S.r * 0.5)),
        line(seg(12, 13, 12, 2)), line(poly(head(12, 2, 0, -1, 2), r=S.r * 0.5)),
        line(seg(15, 13.5, 22, 13.5)), line(poly(head(22, 13.5, 1, 0, 2), r=S.r * 0.5)),
    ]


@icon("overclocking", CAT, "Processor chip with pins and a speed gauge on its face with the needle at the far end",
      tags=["overclock", "oc", "boost clock", "cpu speed", "performance", "turbo"])
def _(S):
    parts = [shell(rect(5, 5, 14, 14, rr(S, 3)))]
    for v in (9, 15):
        parts += [line(seg(v, 2.5, v, 5)), line(seg(v, 19, v, 21.5)),
                  line(seg(2.5, v, 5, v)), line(seg(19, v, 21.5, v))]
    x, y = polar(12, 15, 4.2, -25)
    parts += [detail("M7.8 15A4.2 4.2 0 0 1 16.2 15"), detail(seg(12, 15, x, y)), dot(12, 15, 1.1)]
    return parts


@icon("laptop-overheating", CAT, "Open laptop in side view with three wavy heat lines rising from the keyboard",
      tags=["hot laptop", "overheat", "thermal throttling", "fan failure", "temperature warning", "heat"])
def _(S):
    return [
        shell(rect(3, 18, 18, 3, rr(S, 1.5))),
        line(seg(4.5, 18, 3, 6)),
        line("M10 14c-1.6-1.8 1.6-3 0-5s1.6-3 0-4.5"),
        line("M14 14c-1.6-1.8 1.6-3 0-5s1.6-3 0-4.5"),
        line("M18 14c-1.6-1.8 1.6-3 0-5s1.6-3 0-4.5"),
    ]


@icon("static-discharge", CAT, "Fingertip reaching toward a small chip with a jagged spark across the gap",
      tags=["esd", "static electricity", "electrostatic", "spark", "anti static", "chip safety"])
def _(S):
    return [
        line("M9 2V5.5a3 3 0 0 0 6 0V2"),
        solid(poly([(13.5, 10.3), (9.5, 13.5), (12, 13.5), (10, 16.2), (14.5, 12.5), (12.5, 12.5)], closed=True)),
        shell(rect(5, 16.5, 14, 5, rr(S, 1.5))),
        line(seg(2.5, 19, 5, 19)),
        line(seg(19, 19, 21.5, 19)),
    ]


@icon("hard-drive-internals", CAT, "Opened hard drive from above with a round platter, spindle and actuator arm",
      tags=["hdd internals", "platter", "actuator arm", "read head", "disk drive", "spindle"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, rr(S, 3))),
        detail(circle(10, 12, 5.5)),
        dot(10, 12, 1.1),
        line(seg(18.5, 17.5, 12.8, 8.8)),
        dot(18.5, 17.5, 1.3),
    ]


# ============================================================================ connectors, cards and adapters

@icon("atx-power-connector", CAT, "Wide power plug seen from the front with two rows of pin holes, a latch on top and wires behind",
      tags=["24 pin", "motherboard power", "psu cable", "power supply", "connector", "plug"])
def _(S):
    parts = [shell(rect(2, 7, 20, 10, rr(S, 2.5))),
             line(poly([(8, 7), (8, 4), (16, 4), (16, 7)], r=S.r))]
    for x in (5, 9, 13, 17):
        parts += [sq(x, 9.2, 2, 2), sq(x, 12.8, 2, 2)]
    for x in (6, 12, 18):
        parts.append(line(seg(x, 17, x, 21.5)))
    return parts


@icon("molex-connector", CAT, "Four-pin power plug from the front with chamfered top corners, four pin holes and four wires",
      tags=["4 pin", "peripheral power", "psu connector", "drive power", "power cable", "plug"])
def _(S):
    parts = [shell(poly([(3, 17), (3, 9), (6, 6), (18, 6), (21, 9), (21, 17)], closed=True, r=S.r))]
    for x in (6.5, 10.2, 13.8, 17.5):
        parts += [dot(x, 11.5, 1.25), line(seg(x, 18, x, 21.5))]
    return parts


@icon("laptop-memory-module", CAT, "Short wide memory stick with a notch in each side edge, two chips and contacts along the bottom",
      tags=["sodimm", "so-dimm", "ram stick", "notebook memory", "ram", "upgrade"])
def _(S):
    parts = [shell(poly([(2, 5), (22, 5), (22, 10), (20.5, 11.5), (22, 13), (22, 17), (2, 17), (2, 13),
                         (3.5, 11.5), (2, 10)], closed=True, r=S.r * 0.5)),
             sq(5.5, 7.5, 5, 3), sq(13.5, 7.5, 5, 3)]
    for x in (5, 8.5, 12, 15.5):
        parts.append(sq(x, 13.2, 2, 2))
    return parts


@icon("io-shield", CAT, "Rectangular back plate with cutouts for stacked USB ports, an ethernet port and audio jacks",
      tags=["back plate", "i/o plate", "motherboard", "rear ports", "backplate", "case"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, rr(S, 3.5))),
        sq(4.5, 6, 5, 3), sq(4.5, 11, 5, 3),
        sq(12, 6, 7, 6, 0.5 if S.name == "rounded" else 0),
        dot(7, 17.5, 1.3), dot(12, 17.5, 1.3), dot(17, 17.5, 1.3),
    ]


@icon("gpu-support-bracket", CAT, "Graphics card lying horizontally propped from below by an adjustable post on a flat base",
      tags=["gpu sag", "card holder", "graphics card prop", "support stand", "sagging", "video card"])
def _(S):
    return [
        line(seg(2.5, 2.5, 2.5, 13.5)),
        shell(rect(4.5, 3, 17.5, 9, rr(S, 3.5))),
        detail(circle(10, 7.5, 2.2)),
        detail(seg(16, 5.5, 16, 9.5)),
        detail(seg(19.5, 5.5, 19.5, 9.5)),
        line(seg(13.5, 12, 13.5, 19)),
        line(seg(9.5, 20.5, 17.5, 20.5)),
    ]


@icon("pcie-riser-cable", CAT, "Flat ribbon cable folded in an S bend with a slot connector at one end and a contact edge at the other",
      tags=["riser", "extension cable", "vertical gpu mount", "pci express", "ribbon", "flexible cable"])
def _(S):
    return [
        shell(rect(3, 2.5, 8, 4, rr(S, 1.5))),
        line("M5 7C5 13 15 11 15 17"),
        line("M9 7C9 13 19 11 19 17"),
        shell(rect(13, 18.5, 8, 3, rr(S, 1.2))),
    ]


@icon("pcie-wifi-card", CAT, "Small expansion card with a bracket carrying two tall antennas and contacts along its bottom edge",
      tags=["wireless card", "wifi adapter", "network card", "bluetooth", "antenna", "expansion card"])
def _(S):
    return [
        line(seg(8, 10, 8, 2.5)), line(seg(16, 10, 16, 2.5)),
        shell(rect(3, 10, 18, 8, rr(S, 2.5))),
        sq(9, 12.5, 6, 3),
        line(seg(8, 20, 8, 22)), line(seg(12, 20, 12, 22)), line(seg(16, 20, 16, 22)),
    ]


@icon("pin-grid-processor", CAT, "Square processor seen from below with a dense grid of pin dots and a marked corner",
      tags=["pga", "cpu pins", "socket pins", "underside", "processor", "pin array"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 3))), solid(poly([(5.5, 5.5), (8.5, 5.5), (5.5, 8.5)], closed=True))]
    for i in range(4):
        for j in range(4):
            if i == 0 and j == 0:
                continue
            parts.append(dot(7 + j * 3.4, 7 + i * 3.4, 1.05))
    return parts


@icon("chiplet-package", CAT, "Square chip substrate holding one large die in the centre and smaller dies around it",
      tags=["multi chip module", "mcm", "die", "processor package", "cpu design", "silicon"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(rect(8.5, 8.5, 7, 7, rr(S, 1.5) if S.name == "rounded" else 0)),
        sq(5, 5, 2.5, 2.5), sq(16.5, 5, 2.5, 2.5), sq(5, 16.5, 2.5, 2.5), sq(16.5, 16.5, 2.5, 2.5),
    ]


@icon("usb-wifi-adapter", CAT, "Small USB stick with a tall hinged antenna at its far end and signal arcs by the antenna tip",
      tags=["wifi dongle", "wireless adapter", "network adapter", "usb dongle", "antenna", "wlan"])
def _(S):
    return [
        shell(rect(2, 15.5, 5, 3, 0.5 if S.name == "rounded" else 0)),
        shell(rect(8, 14, 11, 7, rr(S, 2.5))),
        line(seg(16, 14, 16, 6)),
        line(arc(16, 6, 3, -55, 55)),
        line(arc(16, 6, 6, -55, 55)),
    ]


@icon("wireless-usb-receiver", CAT, "Tiny stub dongle with a short plug and a rounded cap, with two small signal arcs above it",
      tags=["nano receiver", "mouse dongle", "keyboard receiver", "2.4ghz", "usb dongle", "wireless"])
def _(S):
    return [
        shell(rect(2, 14, 6, 4, 0.5 if S.name == "rounded" else 0)),
        shell(rect(9, 12, 12, 8, rr(S, 3.5))),
        line(arc(15, 9, 3, 215, 325)),
        line(arc(15, 9, 6.5, 215, 325)),
    ]


@icon("cable-management", CAT, "Three parallel cables bundled by two straps and turning a right angle together",
      tags=["cable tidy", "cable ties", "wire routing", "cable bundle", "organize cables", "zip tie"])
def _(S):
    return [
        line(poly([(2, 5), (19, 5), (19, 21.5)], r=S.r)),
        line(poly([(2, 8.5), (15.5, 8.5), (15.5, 21.5)], r=S.r)),
        line(poly([(2, 12), (12, 12), (12, 21.5)], r=S.r)),
        shell(rect(5.5, 2.5, 3, 12, rr(S, 1))),
    ]


@icon("hard-drive-dock", CAT, "Low dock base with a bare hard drive standing upright in its slot and a small status light",
      tags=["drive dock", "usb dock", "sata dock", "docking station", "external storage", "hdd reader"])
def _(S):
    return [
        shell(rect(7, 2.5, 10, 12, rr(S, 3.5))),
        detail(circle(12, 8, 2.2)),
        shell(rect(2, 15.5, 20, 5.5, rr(S, 1.5))),
        dot(18.5, 18.25, 1),
    ]


@icon("drive-caddy", CAT, "Hot-swap drive tray: a flat sled with screw holes along its rails and a front bezel with a release lever",
      tags=["drive tray", "hot swap", "sled", "hdd tray", "server drive", "bay"])
def _(S):
    return [
        shell(rect(5, 3, 14, 10.5, rr(S, 3.5))),
        dot(8, 7, 1), dot(16, 7, 1), dot(8, 10, 1), dot(16, 10, 1),
        shell(rect(3, 15.5, 18, 5.5, rr(S, 1.5))),
        sq(6, 17.5, 8, 1.5), dot(17.5, 18.25, 0.9),
    ]


@icon("drive-cage", CAT, "Metal drive cage with three stacked bays and one drive pulled partly out of the middle bay",
      tags=["drive bay", "hdd cage", "storage bay", "hot swap", "server drive bay", "disk enclosure"])
def _(S):
    return [
        shell(rect(2, 3, 16, 18, rr(S, 2))),
        detail(seg(2, 8.5, 18, 8.5)),
        detail(seg(2, 15.5, 18, 15.5)),
        shell(rect(8, 10.75, 14, 2.5, 0.5 if S.name == "rounded" else 0)),
    ]


# ============================================================================ storage media and drives

@icon("compactflash-card", CAT, "Thick, nearly square memory card with a row of pin holes along one edge and a label area on its face",
      tags=["cf card", "compact flash", "camera memory", "flash card", "storage card", "professional camera"])
def _(S):
    parts = [shell(poly([(3, 2.5), (21, 2.5), (21, 17), (16.5, 21.5), (3, 21.5)], closed=True, r=S.r)),
             detail(rect(6.5, 11, 11, 7, rr(S, 1.5)))]
    for x in (6, 10, 14, 18):
        parts.append(dot(x, 6.2, 1))
    return parts


@icon("memory-card-wallet", CAT, "Open fold-out case with two panels of card pockets, some holding memory cards",
      tags=["sd card case", "card holder", "card organizer", "photographer", "storage case", "memory card holder"])
def _(S):
    return [
        shell(rect(3, 4, 7.5, 16, rr(S, 2.5))),
        shell(rect(13.5, 4, 7.5, 16, rr(S, 2.5))),
        sq(5.5, 7, 3, 4), sq(5.5, 13.5, 3, 4),
        sq(16, 7, 3, 4), sq(16, 14, 3, 3),
    ]


@icon("tape-library", CAT, "Tall cabinet with a glass front showing rows of tape cartridges and a picker arm on a rail",
      tags=["tape robot", "backup library", "data tape", "lto", "archive", "enterprise backup"])
def _(S):
    parts = [shell(rect(3, 2.5, 18, 19, rr(S, 2.5))),
             detail(seg(3, 15, 21, 15)), sq(9.5, 17, 5, 2)]
    for y in (5.2, 10):
        for x in (5.5, 10.5, 15.5):
            parts.append(sq(x, y, 3, 3))
    return parts


@icon("floppy-drive", CAT, "Front of a disk drive unit with a horizontal disk slot, a small eject button and an activity light",
      tags=["diskette drive", "fdd", "floppy reader", "disk slot", "legacy", "retro"])
def _(S):
    return [
        shell(rect(2, 6, 20, 12, rr(S, 3))),
        sq(4.5, 8.8, 15, 1.7),
        sq(14, 13.2, 5.5, 2),
        dot(6.5, 14.2, 1.1),
    ]


@icon("five-inch-floppy-disk", CAT, "Thin square flexible disk with a large centre hole, an oval read window and a notch on the side",
      tags=["5.25 inch", "floppy", "diskette", "legacy storage", "retro", "magnetic disk"])
def _(S):
    return [
        shell(poly([(3, 3), (21, 3), (21, 21), (3, 21), (3, 14.5), (5, 14.5), (5, 11.5), (3, 11.5)], closed=True, r=S.r * 0.6)),
        detail(circle(12, 9, 3.5)),
        kdot(rect(10.5, 15, 3, 5, 1.2)),
    ]


@icon("disk-pack", CAT, "Stack of platters on a shared spindle under a clear dome cover with a lifting handle",
      tags=["removable disk", "platter stack", "mainframe storage", "legacy storage", "retro", "disk cartridge"])
def _(S):
    return [
        line(poly([(9.5, 5.5), (9.5, 3), (14.5, 3), (14.5, 5.5)], r=S.r)),
        line("M3.5 16.5V15A8.5 8.5 0 0 1 20.5 15V16.5"),
        detail(seg(12, 8.5, 12, 16)),
        detail(seg(6, 11, 18, 11)),
        detail(seg(5.5, 14, 18.5, 14)),
        shell(rect(2, 16.5, 20, 4.5, rr(S, 2))),
    ]


@icon("data-cassette-recorder", CAT, "Low recorder box with a cassette door on top, piano-style keys on the front and a cable out the back",
      tags=["tape recorder", "datasette", "cassette storage", "retro computer", "tape drive", "home computer"])
def _(S):
    return [
        shell(rect(5, 3.5, 12, 5.5, rr(S, 2.5))),
        dot(9.5, 6.25, 1), dot(13.5, 6.25, 1),
        shell(rect(2, 10, 18, 10, rr(S, 3))),
        sq(4.5, 13.5, 3, 4), sq(9, 13.5, 3, 4), sq(13.5, 13.5, 3, 4),
        line("M20 15.5h.5a1.5 1.5 0 0 1 1.5 1.5v4"),
    ]


@icon("dna-data-storage", CAT, "Short double helix with square bit rungs ending in a hard drive outline",
      tags=["dna storage", "biological storage", "archive", "genetic data", "future storage", "helix"])
def _(S):
    return [
        line("M6 2.5C6 4.5 18 4.5 18 7.5S6 10.5 6 13"),
        line("M18 2.5C18 4.5 6 4.5 6 7.5S18 10.5 18 13"),
        sq(9, 7, 6, 1.4),
        shell(rect(3, 15, 18, 6.5, rr(S, 3))),
        dot(17.5, 18.25, 1),
        detail(seg(6, 18.25, 12, 18.25)),
    ]


@icon("disk-defragmentation", CAT, "Disk with scattered blocks on top and the blocks gathered into one solid row below, with an arrow between",
      tags=["defrag", "optimize drive", "fragmentation", "disk cleanup", "consolidate", "hard drive maintenance"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 6.5, rr(S, 2.5))),
        sq(4.8, 4.7, 2.5, 2.5), sq(10.2, 4.7, 2.5, 2.5), sq(16.7, 4.7, 2.5, 2.5),
        line(poly([(9.5, 11.5), (12, 14), (14.5, 11.5)], r=S.r * 0.5)),
        shell(rect(3, 16, 18, 5.5, rr(S, 2.5))),
        sq(5, 17.8, 9, 2),
    ]


@icon("disk-partition", CAT, "Hard drive outline split by a vertical divider into two unequal sections, one filled and one empty",
      tags=["partition", "disk split", "volume", "drive letter", "disk management", "storage"])
def _(S):
    return [
        shell(rect(2, 5, 20, 14, rr(S, 3.5))),
        detail(seg(15, 5, 15, 19)),
        sq(4.5, 7.5, 8, 9),
    ]


@icon("data-recovery", CAT, "Small hard drive inside a life ring",
      tags=["file recovery", "rescue data", "restore files", "undelete", "disk rescue", "lifebuoy"])
def _(S):
    parts = [line(circle(12, 12, 9.5)), line(circle(12, 12, 6.8))]
    for a in (45, 135, 225, 315):
        a0, a1 = a - 15, a + 15
        p0, p1 = polar(12, 12, 9.5, a0), polar(12, 12, 9.5, a1)
        q0, q1 = polar(12, 12, 6.8, a0), polar(12, 12, 6.8, a1)
        parts.append(solid(f"M{fmt(p0[0])} {fmt(p0[1])}A9.5 9.5 0 0 1 {fmt(p1[0])} {fmt(p1[1])}"
                           f"L{fmt(q1[0])} {fmt(q1[1])}A6.8 6.8 0 0 0 {fmt(q0[0])} {fmt(q0[1])}Z"))
    parts.append(shell(rect(8.5, 9, 7, 6, rr(S, 3))))
    return parts


# ============================================================================ computers

@icon("mini-itx-case", CAT, "Small cube-shaped computer case in three-quarter view with a mesh front and a round power button",
      tags=["small form factor", "sff", "itx", "compact pc", "cube case", "mini tower"])
def _(S):
    return [
        shell(poly([(3, 9), (8, 4), (20, 4), (15, 9)], closed=True, r=S.r * 0.5)),
        shell(poly([(15, 9), (20, 4), (20, 16), (15, 21)], closed=True, r=S.r * 0.5)),
        shell(rect(3, 9, 12, 12, rr(S, 2))),
        detail(seg(6.5, 11.5, 6.5, 15)),
        detail(seg(11.5, 11.5, 11.5, 15)),
        dot(9, 18.2, 1.1),
    ]


@icon("mini-pc", CAT, "Very low square box about the size of a hand with a round power button and two ports on its front",
      tags=["micro pc", "small computer", "compact desktop", "tiny pc"])
def _(S):
    return [
        shell(rect(2, 8, 20, 9, rr(S, 3.5))),
        dot(6.5, 12.5, 1.4),
        sq(12, 11.5, 3, 2), sq(16.5, 11.5, 3, 2),
    ]


@icon("retro-desktop-pc", CAT, "Wide low computer case with two floppy slots on the front and a bulky boxy monitor on top",
      tags=["vintage computer", "old pc", "beige box", "90s computer", "classic desktop", "crt desktop"])
def _(S):
    return [
        shell(rect(3, 4, 14, 9, rr(S, 3))),
        detail(seg(6, 8.5, 14, 8.5)),
        shell(rect(2, 15, 20, 6, rr(S, 2.5))),
        sq(5, 17.2, 5, 1.6), sq(12, 17.2, 5, 1.6), dot(19.5, 18, 0.9),
    ]


def rotpts(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def bar(x1, y1, x2, y2, w):
    """Closed rectangle of width w along the segment (x1, y1)-(x2, y2) for poly()."""
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    nx, ny = -dy / n * w / 2, dx / n * w / 2
    return [(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)]


# ============================================================================ vintage and portable computers

@icon("keyboard-computer", CAT, "Wedge-shaped home computer with the keyboard built in and a cartridge sticking out of the back edge",
      tags=["home computer", "8 bit", "retro computer", "vintage", "breadbin", "cartridge slot"])
def _(S):
    parts = [shell(rect(8, 3, 8, 5, rr(S, 1.5))),
             shell(poly([(2, 20), (2, 15), (5, 8), (19, 8), (22, 15), (22, 20)], closed=True, r=S.r))]
    for x in (7, 11, 15, 19):
        parts.append(dot(x, 12.5, 1))
    parts.append(detail(seg(8.5, 16.5, 15.5, 16.5)))
    return parts


@icon("luggable-computer", CAT, "Suitcase-shaped portable computer with a carry handle, a small built-in screen and drive slots",
      tags=["portable computer", "transportable", "suitcase pc", "vintage", "retro", "sewing machine computer"])
def _(S):
    return [
        line(poly([(8, 7), (8, 3.5), (16, 3.5), (16, 7)], r=S.r)),
        shell(rect(2, 7, 20, 14, rr(S, 3))),
        detail(rect(5.5, 10, 7, 6, rr(S, 1.5) if S.name == "rounded" else 0)),
        sq(15.5, 10.5, 4, 1.5), sq(15.5, 14.2, 4, 1.5),
    ]


@icon("front-panel-computer", CAT, "Early hobby computer box with a row of indicator lights above a row of small toggle switches",
      tags=["early hobby", "toggle switches", "blinkenlights", "hobby computer", "retro", "minicomputer"])
def _(S):
    parts = [shell(rect(2, 5, 20, 14, rr(S, 3)))]
    for x in (5.5, 9.8, 14.2, 18.5):
        parts += [dot(x, 8.8, 1.1), sq(x - 0.9, 12, 1.8, 4.2)]
    return parts


@icon("video-terminal", CAT, "Boxy terminal with a deep monitor showing a prompt and block cursor, with a keyboard at its base",
      tags=["dumb terminal", "text terminal", "console", "mainframe terminal", "command line"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 13, rr(S, 3.5))),
        detail(poly([(8, 6.5), (10.5, 8.8), (8, 11)], r=S.r * 0.5)),
        sq(12.5, 10, 4, 1.6),
        shell(rect(2, 17.5, 20, 4, rr(S, 1.8))),
    ]


@icon("convertible-laptop", CAT, "Laptop in tent mode seen from the side, folded into an upside-down V with the screen facing out",
      tags=["2 in 1", "tent mode", "foldable laptop", "flip laptop", "hybrid", "touchscreen laptop"])
def _(S):
    return [
        shell(poly(bar(3.5, 20, 11, 4.5, 5), closed=True, r=S.r * 0.6)),
        solid(circle(6.9, 15.8, 0.9)),
        line(seg(20.5, 20.5, 12.5, 5)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("rugged-laptop", CAT, "Closed thick laptop with rubber bumpers on every corner and a carry handle along its front edge",
      tags=["military laptop", "shockproof", "field computer", "industrial laptop", "durable"])
def _(S):
    return [
        shell(rect(5, 3, 14, 10.5, rr(S, 3))),
        solid(circle(5, 3, 2)), solid(circle(19, 3, 2)), solid(circle(5, 13.5, 2)), solid(circle(19, 13.5, 2)),
        shell(rect(2, 16.5, 20, 4.5, rr(S, 2.5))),
        sq(8, 18.3, 8, 1),
    ]


@icon("laptop-battery", CAT, "Removable flat battery pack with a chamfered corner and a row of gold contacts along one edge",
      tags=["notebook battery", "battery pack", "power", "replacement battery", "lithium", "laptop power"])
def _(S):
    parts = [shell(poly([(2, 4), (18, 4), (22, 8), (22, 19), (2, 19)], closed=True, r=S.r)),
             detail(seg(6, 8.5, 14, 8.5))]
    for x in (5, 9, 13, 17):
        parts.append(sq(x, 14, 2, 2.2))
    return parts


@icon("tablet-keyboard-case", CAT, "Tablet propped upright on a folding cover with a thin keyboard lying flat in front",
      tags=["folio keyboard", "tablet stand", "bluetooth keyboard", "detachable keyboard", "cover", "2 in 1 tablet"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 10, rr(S, 3))),
        shell(poly([(7.5, 13), (16.5, 13), (18.5, 15.5), (5.5, 15.5)], closed=True, r=S.r * 0.4)),
        shell(rect(2, 18, 20, 3.5, rr(S, 1.8))),
    ]

# ============================================================================ systems and workspaces

@icon("external-gpu-enclosure", CAT, "Box with a fan window showing a graphics card inside, connected by a cable to a small laptop",
      tags=["egpu", "graphics dock", "laptop gaming", "external graphics", "video card box"])
def _(S):
    return [
        shell(rect(2, 2.5, 12, 10.5, rr(S, 3.5))),
        detail(circle(8, 7.75, 2.6)),
        line(poly([(8, 13), (8, 16.5), (12, 16.5)], r=S.r)),
        shell(rect(13.5, 13.5, 8.5, 5, rr(S, 2.5))),
        line(seg(12, 21.5, 22.5, 21.5)),
    ]


@icon("pc-building", CAT, "Computer tower with its side panel removed showing boards inside and a screwdriver angled into the case",
      tags=["assemble pc", "build a computer", "custom pc", "diy computer", "installation", "open case"])
def _(S):
    return [
        shell(rect(2, 3, 11, 18, rr(S, 2.5))),
        sq(4.5, 6, 3, 3), sq(8.5, 6, 3, 3),
        detail(seg(4.5, 12.5, 10.5, 12.5)),
        detail(seg(4.5, 16.5, 10.5, 16.5)),
        line(seg(17.5, 8.5, 11, 14.5)),
        shell(poly(bar(17.5, 8.5, 20.3, 5.7, 3.4), closed=True, r=S.r * 0.4)),
    ]


@icon("computer-repair", CAT, "Open laptop with a wrench and a screwdriver crossed over its screen",
      tags=["fix computer", "pc service", "maintenance", "tech support", "troubleshooting", "laptop repair"])
def _(S):
    return [
        shell(rect(3, 4, 18, 12, rr(S, 3))),
        line(seg(2, 19.5, 22, 19.5)),
        line(seg(7.5, 13, 16, 6)),
        line(arc(17.2, 5, 2.1, 140, 40)),
        line(seg(7.5, 6.5, 14.5, 12.5)),
        shell(poly(bar(14, 12, 17, 14.5, 3), closed=True, r=S.r * 0.4)),
    ]


@icon("computer-cluster", CAT, "Three small towers side by side, each linked by a line to one switch box below them",
      tags=["server cluster", "compute nodes", "hpc", "beowulf", "distributed computing", "network"])
def _(S):
    k = 0.5 if S.name == "line" else 2.4
    parts = [shell(rect(2, 3, 5, 9, k)), shell(rect(9.5, 3, 5, 9, k)), shell(rect(17, 3, 5, 9, k))]
    for x in (4.5, 12, 19.5):
        parts += [line(seg(x, 12, x, 16)), dot(x, 5.8, 0.8), dot(x, 8.8, 0.8)]
    parts += [shell(rect(2, 16, 20, 5, rr(S, 2))), sq(5, 18, 2, 1.2), sq(9, 18, 2, 1.2), sq(13, 18, 2, 1.2)]
    return parts


@icon("sim-racing-rig", CAT, "Side view of a bucket seat on a low frame facing a steering wheel on a mount arm and a monitor",
      tags=["racing simulator", "driving rig", "cockpit", "sim rig", "steering wheel stand", "gaming seat"])
def _(S):
    return [
        line(seg(2, 21, 22, 21)),
        shell(poly([(3, 4), (6.5, 4), (7.5, 13), (12, 13.5), (12, 18), (3, 18)], closed=True, r=S.r)),
        shell(poly(bar(14, 7.5, 15.5, 14, 3), closed=True, r=S.r * 0.4)),
        line(seg(15.5, 14, 17.5, 21)),
        shell(rect(19.5, 3.5, 2.5, 8, 0.6 if S.name == "rounded" else 0)),
        line(seg(20.75, 11.5, 20.75, 21)),
    ]


@icon("desk-setup", CAT, "Desk with a monitor, keyboard and mouse on top and a tower standing on the floor beside a leg",
      tags=["workstation", "home office", "battlestation", "pc desk", "computer desk", "workspace"])
def _(S):
    return [
        shell(rect(3, 2.5, 9, 7, rr(S, 2.5))),
        line(seg(7.5, 9.5, 7.5, 11.5)),
        line(seg(14, 11, 18, 11)),
        dot(20.5, 10.5, 1),
        line(seg(2, 13.5, 22, 13.5)),
        line(seg(4, 13.5, 4, 21.5)),
        line(seg(20, 13.5, 20, 21.5)),
        shell(rect(8, 16, 5, 5, rr(S, 1.5))),
    ]


# ============================================================================ input devices

@icon("mechanical-key-switch", CAT, "Keyboard switch with a square housing, a cross-shaped stem on top and two metal pins below",
      tags=["keyboard switch", "clicky", "tactile", "linear switch", "hotswap"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 7)), line(seg(9, 5, 15, 5)),
        shell(poly([(3, 8), (21, 8), (21, 11), (19, 11), (19, 18), (5, 18), (5, 11), (3, 11)], closed=True, r=S.r)),
        line(seg(9, 18, 9, 21.5)), line(seg(15, 18, 15, 21.5)),
    ]


@icon("vertical-mouse", CAT, "Tall ergonomic mouse standing on its side like a handshake grip, with buttons on the slope and a thumb rest",
      tags=["ergonomic mouse", "handshake mouse", "wrist friendly", "rsi", "upright mouse", "comfort"])
def _(S):
    return [
        shell(poly([(9, 3), (15, 3), (18, 7), (18, 19), (15, 21.5), (9, 21.5), (9, 18.5), (5, 16.5), (5, 12), (9, 9)],
                   closed=True, r=S.r * 2)),
        detail(seg(9, 9.5, 18, 9.5)),
        detail(seg(13.5, 3, 13.5, 9.5)),
    ]


@icon("touchpad", CAT, "Standalone flat rounded pad with a fingertip pressing its surface",
      tags=["trackpad", "gesture pad", "input pad", "multi touch", "laptop pad", "pointing device"])
def _(S):
    return [
        shell(rect(2, 3, 20, 13, rr(S, 4))),
        line("M10 21.5V12.5a2 2 0 0 1 4 0V21.5"),
    ]


@icon("pen-display", CAT, "Monitor tilted back on a low stand with a stylus drawing a curved line on its screen",
      tags=["drawing tablet", "graphics tablet", "digital art", "stylus screen", "illustration"])
def _(S):
    return [
        shell(poly([(2, 16), (22, 16), (20, 4), (4, 4)], closed=True, r=S.r * 1.5)),
        line("M6 13C8 8.5 10 13.5 12.5 10.5"),
        shell(poly(bar(12.5, 10.5, 17.5, 6, 2.6), closed=True, r=S.r * 0.4)),
        line(seg(12, 16, 12, 21)),
        line(seg(8, 21, 16, 21)),
    ]


@icon("macro-keypad", CAT, "Small box with a three-by-three grid of keys and a round knob in one corner",
      tags=["deck keypad", "shortcut keys", "macro pad", "programmable keys", "numpad", "knob"])
def _(S):
    parts = [shell(rect(2, 3, 20, 18, rr(S, 3.5)))]
    for i in range(3):
        for j in range(3):
            parts.append(dot(6 + j * 3.7, 7 + i * 3.7, 1.25))
    parts.append(detail(circle(18, 15.5, 2.2)))
    return parts


@icon("foot-pedal-switch", CAT, "Low foot pedal with a hinged top plate and a cable leading out of the back",
      tags=["foot switch", "pedal", "hands free", "transcription pedal", "dictation", "control pedal"])
def _(S):
    return [
        shell(poly([(2, 20.5), (2, 16.5), (16, 10), (16, 20.5)], closed=True, r=S.r)),
        dot(13, 17, 1.1),
        line("M16 18.5h3.5a2.5 2.5 0 0 0 2.5-2.5V10"),
    ]

# ============================================================================ displays

@icon("portrait-monitor", CAT, "Monitor turned into a tall vertical orientation on a stand with a round base",
      tags=["vertical monitor", "pivot display", "rotated screen", "coding monitor", "tall screen", "pivot"])
def _(S):
    return [
        shell(rect(6.5, 2, 11, 15.5, rr(S, 3))),
        line(seg(12, 17.5, 12, 20)),
        line(seg(7.5, 21, 16.5, 21)),
    ]


@icon("triple-monitor", CAT, "Three monitors side by side on one stand with the outer two angled inward",
      tags=["multi monitor", "three screens", "surround", "wide desktop", "trading setup", "multiple displays"])
def _(S):
    return [
        shell(rect(9, 4, 6, 9.5, rr(S, 1.5))),
        shell(poly([(2, 6.5), (6.5, 5), (6.5, 12.5), (2, 14)], closed=True, r=S.r * 0.4)),
        shell(poly([(17.5, 5), (22, 6.5), (22, 14), (17.5, 12.5)], closed=True, r=S.r * 0.4)),
        line(seg(12, 13.5, 12, 18)),
        line(seg(7.5, 19.5, 16.5, 19.5)),
    ]


@icon("crt-monitor", CAT, "Deep boxy monitor in three-quarter view with a curved screen and a large bulging back casing",
      tags=["cathode ray", "old monitor", "vintage display", "tube monitor", "retro screen", "bulky"])
def _(S):
    return [
        shell(poly([(16, 7), (20.5, 9), (20.5, 15.5), (16, 17.5)], closed=True, r=S.r)),
        shell(rect(2, 4, 14, 14, rr(S, 3.5))),
        detail(rect(5, 7, 8, 8, rr(S, 3))),
        line(seg(5, 21, 13, 21)),
    ]


@icon("touchscreen-monitor", CAT, "Monitor with a fingertip pressing the screen and ripple arcs around the touch point",
      tags=["touch display", "multitouch", "tap", "interactive screen", "kiosk", "finger"])
def _(S):
    return [
        shell(rect(2, 3, 20, 14, rr(S, 3))),
        line("M10.5 21.5V11.5a2 2 0 0 1 4 0V21.5"),
        line(arc(12.5, 9, 5.2, 205, 335)),
    ]


@icon("portable-monitor", CAT, "Very thin monitor propped on a folding cover stand with one short cable leaving its side",
      tags=["travel monitor", "usb c monitor", "second screen", "slim display", "laptop extender", "portable screen"])
def _(S):
    return [
        shell(rect(2, 3, 16, 12, rr(S, 2.5))),
        line(poly([(7, 15), (4.5, 20.5), (15.5, 20.5), (13, 15)], r=S.r)),
        line("M18 9h2.5a1.5 1.5 0 0 1 1.5 1.5V16"),
    ]


@icon("privacy-screen-filter", CAT, "Monitor with a sheet of fine vertical louver lines half slid over its screen",
      tags=["screen protector", "privacy filter", "anti spy", "visual hacking", "confidential", "shield screen"])
def _(S):
    return [
        shell(rect(2, 3, 20, 14, rr(S, 3))),
        detail(seg(5.5, 6, 5.5, 14)),
        detail(seg(9.5, 6, 9.5, 14)),
        detail(seg(13.5, 6, 13.5, 14)),
        line(seg(12, 17, 12, 20)),
        line(seg(8, 21, 16, 21)),
    ]


# ============================================================================ controllers and adapters

@icon("flight-throttle", CAT, "Desktop throttle base with a thick lever handle tilted forward and buttons on its grip",
      tags=["throttle quadrant", "flight sim", "joystick throttle", "hotas", "aircraft controller", "thrust lever"])
def _(S):
    return [
        shell(rect(2, 15, 20, 6, rr(S, 3))),
        sq(6, 17.4, 12, 1.4),
        shell(poly(bar(12, 15, 15.5, 4.5, 5), closed=True, r=S.r * 0.8)),
        dot(14.9, 7.2, 0.9),
    ]


@icon("flight-yoke-controller", CAT, "Aircraft control yoke with horn-shaped handles on a shaft coming out of a box clamped to a desk edge",
      tags=["yoke", "flight simulator", "aircraft wheel", "pilot controller", "control column", "sim gear"])
def _(S):
    return [
        line("M4.5 3V6a4 4 0 0 0 4 4H15.5a4 4 0 0 0 4-4V3"),
        line(seg(12, 10, 12, 14.5)),
        shell(rect(6, 14.5, 12, 6.5, rr(S, 2.5))),
        line(poly([(18, 15.5), (21, 15.5), (21, 21.5), (18, 21.5)], r=S.r * 0.5)),
    ]


@icon("rudder-pedals", CAT, "Pair of flat foot pedals side by side on a low base joined by a pivoting bar",
      tags=["flight pedals", "sim pedals", "yaw pedals", "foot controls", "toe brakes", "flight simulator"])
def _(S):
    return [
        shell(rect(2, 17, 20, 4, rr(S, 1.8))),
        shell(rect(3, 3, 7, 11, rr(S, 2.5))),
        shell(rect(14, 5, 7, 11, rr(S, 2.5))),
        line(seg(10, 9.5, 14, 9.5)),
        dot(12, 9.5, 1.2),
    ]


@icon("3d-mouse", CAT, "Round puck-shaped cap on a wide heavy base with a curved arrow around the cap showing it twists and tilts",
      tags=["6dof", "cad controller", "navigation device", "3d navigation", "puck"])
def _(S):
    return [
        shell(rect(3, 15, 18, 6, rr(S, 3))),
        shell(rect(8, 8, 8, 7, rr(S, 3))),
        line(arc(12, 8, 7, 200, 335)),
        line(poly(head(18.9, 10.5, 0.5, 1, 2.2), r=S.r * 0.5)),
    ]


@icon("sheet-fed-scanner", CAT, "Compact document scanner with an angled paper tray at the back feeding a sheet in and an output slot at the front",
      tags=["document scanner", "adf", "feeder scanner", "paper scanner", "digitize documents", "office"])
def _(S):
    return [
        shell(poly([(8, 3), (16, 3), (17.5, 9), (6.5, 9)], closed=True, r=S.r * 0.5)),
        shell(rect(2, 9, 20, 11, rr(S, 3.5))),
        sq(5, 12.5, 14, 1.6),
        dot(18.5, 17, 1),
    ]


@icon("smart-card-reader", CAT, "Small box with a slot in its top edge and a chip card half inserted with its chip contacts visible",
      tags=["chip card reader", "id card reader", "cac reader", "authentication", "banking card", "security token"])
def _(S):
    return [
        line(poly([(7, 12), (7, 3.5), (17, 3.5), (17, 12)], r=S.r)),
        sq(9, 6, 3.5, 3),
        shell(rect(2, 12, 20, 9, rr(S, 3.5))),
        dot(18, 16.5, 1),
    ]


@icon("usb-c-multiport-adapter", CAT, "Small flat hub body with several port openings along its edge and a short cable ending in an oval plug",
      tags=["usb c hub", "dongle", "docking adapter", "hdmi adapter", "port expander", "laptop hub"])
def _(S):
    return [
        shell(rect(2, 6, 13, 9, rr(S, 3))),
        sq(4, 9.5, 2.5, 2.5), sq(7.5, 9.5, 2.5, 2.5), sq(11, 9.5, 2.5, 2.5),
        line(seg(15, 10.5, 18, 10.5)),
        solid(rect(18.5, 8, 3.5, 5, 1.7)),
    ]


@icon("eye-tracker", CAT, "Thin sensor bar under a monitor with a dotted line of sight from an eye to a point on the screen",
      tags=["gaze tracking", "eye tracking", "gaze control", "attention", "accessibility input", "sensor bar"])
def _(S):
    return [
        shell(rect(2, 2.5, 20, 10, rr(S, 3))),
        solid(rect(4, 14.5, 9, 2, 1)),
        dot(17.5, 7, 1.1),
        dot(17.5, 14.6, 0.8),
        line("M13.5 19.5Q17.5 16 21.5 19.5Q17.5 23 13.5 19.5Z"),
        dot(17.5, 19.5, 0.9),
    ]