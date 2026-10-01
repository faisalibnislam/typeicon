"""TypeIcon Core: devices & hardware.

Generic devices only: no manufacturer's product design or logo. Variant badges sit in the
bottom-right (13–23), so identifying details are kept top/left where the object allows.
"""
from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "devices"


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell (like a dot)."""
    return Part("dot", rect(x, y, w, h, rx))


def rr(S, cap=None):
    """Container corner radius for the style, optionally capped for small shapes."""
    return S.R if cap is None else min(S.R, cap)


# ============================================================================ computers and displays

@icon("laptop", CAT, "Open laptop computer with its screen and keyboard base",
      tags=["notebook", "computer", "macbook", "pc", "portable", "work"], aliases=["notebook-computer"])
def _(S):
    return [
        shell(rect(4, 4, 16, 11, rr(S, 3))),
        line(seg(3, 19, 21, 19) if S.name == "rounded" else seg(2, 19, 22, 19)),
    ]


@icon("monitor", CAT, "Computer monitor on a stand",
      tags=["display", "screen", "desktop", "computer", "lcd", "pc"], aliases=["display", "screen"])
def _(S):
    return [
        shell(rect(3, 3, 18, 13, rr(S))),
        line(seg(12, 16, 12, 20)),
        line(seg(7, 20.5, 17, 20.5)),
    ]


@icon("desktop", CAT, "Desktop computer: a monitor beside a tower case",
      tags=["computer", "pc", "workstation", "office", "tower"], aliases=["desktop-computer"])
def _(S):
    return [
        shell(rect(3, 5, 9, 8, rr(S, 2.5))),
        line(seg(7.5, 13, 7.5, 18)),
        line(seg(4.5, 18.5, 10.5, 18.5)),
        shell(rect(15.5, 3, 5.5, 18, rr(S, 2))),
        dot(18.25, 7, 1.1),
        dot(18.25, 17, 1.1),
    ]


@icon("all-in-one", CAT, "All-in-one computer: a screen with a built-in chin on a wedge stand",
      tags=["computer", "imac", "desktop", "pc", "display", "aio"], aliases=["all-in-one-computer"])
def _(S):
    return [
        shell(rect(3, 3, 18, 14, rr(S))),
        detail(seg(3, 13.5, 21, 13.5)),
        line(poly([(10, 17), (9, 21), (15, 21), (14, 17)], r=S.r)),
    ]


@icon("desktop-tower", CAT, "Computer tower case with drive bays and a power button",
      tags=["pc", "case", "tower", "computer", "cpu", "workstation"], aliases=["pc-tower", "computer-case"])
def _(S):
    return [
        shell(rect(6, 3, 12, 18, rr(S))),
        detail(seg(9, 7, 15, 7)),
        detail(seg(9, 10.5, 15, 10.5)),
        dot(12, 16.5, 1.5) if S.name == "rounded" else sq(10.5, 15, 3, 3),
    ]


@icon("tablet", CAT, "Tablet computer in portrait",
      tags=["ipad", "tablet", "device", "touchscreen", "mobile", "reader"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 3))),
        detail(seg(10, 18, 14, 18)),
    ]


@icon("e-reader", CAT, "E-reader with lines of text on its screen",
      tags=["ebook", "kindle", "reader", "book", "reading", "device"], aliases=["ebook-reader"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 3))),
        detail(seg(8.5, 7, 15.5, 7)),
        detail(seg(8.5, 10.5, 15.5, 10.5)),
        detail(seg(8.5, 14, 13, 14)),
    ]


# ============================================================================ wearables

@icon("smartwatch", CAT, "Smartwatch with a square screen showing a pulse",
      tags=["wearable", "fitness", "tracker", "smart watch", "wrist", "health"], aliases=["smart-watch"])
def _(S):
    return [
        line(poly([(8.5, 6), (9, 2.5), (15, 2.5), (15.5, 6)], r=S.r)),
        line(poly([(8.5, 18), (9, 21.5), (15, 21.5), (15.5, 18)], r=S.r)),
        shell(rect(5.5, 6, 13, 12, rr(S, 3))),
        detail(poly([(8, 12), (10, 12), (11, 10), (13, 14), (14, 12), (16, 12)], r=S.r * 0.4)),
    ]


# ============================================================================ input

@icon("keyboard", CAT, "Computer keyboard with keys and a space bar",
      tags=["typing", "keys", "input", "type", "computer", "text"])
def _(S):
    keys = [dot(x, y, 1) for y in (8.5, 12) for x in (7, 10.33, 13.67, 17)]
    return [
        shell(rect(3, 5, 18, 14, rr(S, 3))),
        *keys,
        detail(seg(8, 15.5, 16, 15.5)),
    ]


@icon("mouse", CAT, "Computer mouse with a scroll wheel",
      tags=["computer mouse", "pointer", "click", "input", "scroll", "peripheral"], aliases=["computer-mouse"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 19, 5 if S.name == "line" else 6)),
        detail(seg(12, 6, 12, 9.5)),
    ]


# ============================================================================ office

@icon("printer", CAT, "Printer with a sheet of paper coming out",
      tags=["print", "document", "office", "paper", "output", "fax"])
def _(S):
    body = [(6, 17), (3, 17), (3, 8), (21, 8), (21, 17), (18, 17)]
    return [
        shell(rect(6, 3, 12, 5, rr(S, 1))),
        line(poly(body, r=S.R * 0.75)),
        shell(rect(6, 13, 12, 8, rr(S, 1))),
        detail(seg(9, 17, 15, 17)),
        dot(17.5, 10.75, 1),
    ]


@icon("scanner", CAT, "Flatbed scanner with its lid raised",
      tags=["scan", "flatbed", "document", "office", "copy", "digitize"])
def _(S):
    return [
        line(seg(4, 9.5, 20, 3.5)),
        shell(rect(3, 12, 18, 8, rr(S, 3))),
        detail(seg(5, 16, 13, 16)),
        dot(18, 16, 1),
    ]


# ============================================================================ storage and servers

@icon("server", CAT, "Server with two stacked units and status lights",
      tags=["hosting", "backend", "rack", "datacenter", "network", "computer"])
def _(S):
    out = []
    for y in (3, 13):
        out += [shell(rect(3, y, 18, 8, rr(S, 3))), dot(7, y + 4, 1.25), detail(seg(11, y + 4, 17, y + 4))]
    return out


@icon("database", CAT, "Database cylinder with stacked layers",
      tags=["storage", "data", "sql", "db", "table", "records"], aliases=["db"])
def _(S):
    # Line: flatter end arcs that meet the sides at corners; Rounded: true half-ellipses (smooth).
    rx, ry = (10.5, 3.5) if S.name == "line" else (8, 2.75)
    top = f"M4 6A{rx} {ry} 0 0 1 20 6"
    return [
        shell(f"M4 6A{rx} {ry} 0 0 1 20 6V18A{rx} {ry} 0 0 1 4 18Z"),
        detail(f"M4 6A{rx} {ry} 0 0 0 20 6"),
        detail(f"M4 12A{rx} {ry} 0 0 0 20 12"),
    ]


@icon("hard-drive", CAT, "Hard disk drive: a drive case with a platter and an activity light",
      tags=["hdd", "disk", "storage", "drive", "harddisk", "data"], aliases=["hdd", "hard-disk"])
def _(S):
    return [
        shell(rect(3, 5, 18, 14, rr(S, 3))),
        detail(circle(9.5, 12, 3.5)),
        dot(9.5, 12, 1),
        detail(seg(15.5, 15.5, 18, 15.5)),
    ]


@icon("ssd", CAT, "Solid-state drive card with memory chips and a connector",
      tags=["solid state drive", "m.2", "storage", "drive", "flash", "nvme"], aliases=["solid-state-drive"])
def _(S):
    return [
        shell(rect(3, 7, 18, 10, rr(S, 2.5))),
        sq(6, 10, 3.5, 4, 0.5),
        sq(11.5, 10, 3.5, 4, 0.5),
        detail(seg(18, 10, 18, 14)),
    ]


@icon("usb", CAT, "USB trident symbol",
      tags=["usb", "port", "connector", "universal serial bus", "cable", "flash drive"])
def _(S):
    tip = [(12, 2.5), (14.5, 6.5), (9.5, 6.5)]
    return [
        solid(poly(tip, closed=True)),
        line(seg(12, 6, 12, 17)),
        line(poly([(12, 15.5), (6.5, 12.5), (6.5, 10.5)], r=S.r)),
        line(poly([(12, 13), (17.5, 10), (17.5, 9)], r=S.r)),
        shell(circle(6.5, 8.75, 1.75)),
        shell(rect(16, 5.5, 3, 3)),
        shell(circle(12, 19.25, 1.75)),
    ]


@icon("cpu", CAT, "Processor chip with pins on every side",
      tags=["processor", "chip", "microchip", "cpu", "silicon", "hardware"], aliases=["processor", "microchip"])
def _(S):
    e = 3 if S.name == "rounded" else 2  # pin ends: round caps add 1 px
    pins = []
    for p in (10, 14):
        pins += [line(seg(p, e, p, 6)), line(seg(p, 18, p, 24 - e)), line(seg(e, p, 6, p)), line(seg(18, p, 24 - e, p))]
    return [
        shell(rect(7, 7, 10, 10, rr(S, 2.5))),
        sq(10, 10, 4, 4, 0.5),
        *pins,
    ]


@icon("memory-chip", CAT, "Memory module (RAM stick) with chips and contact pins",
      tags=["ram", "memory", "dimm", "module", "hardware", "chip"], aliases=["ram"])
def _(S):
    pins = [line(seg(x, 16, x, 19.5)) for x in (6, 9.5, 14.5, 18)]
    return [
        shell(rect(3, 5, 18, 11, rr(S, 2.5))),
        sq(6, 8, 3, 5, 0.5), sq(10.5, 8, 3, 5, 0.5), sq(15, 8, 3, 5, 0.5),
        *pins,
    ]


# ============================================================================ networking

@icon("router", CAT, "Network router with two antennas and status lights",
      tags=["network", "internet", "antenna", "wireless", "lan", "networking"])
def _(S):
    return [
        line(seg(6, 12, 4.5, 4)),
        line(seg(18, 12, 19.5, 4)),
        shell(rect(3, 12, 18, 8, rr(S, 3))),
        dot(7, 16, 1), dot(10.5, 16, 1), dot(14, 16, 1),
    ]


@icon("modem", CAT, "Upright modem box with a column of status lights on a stand",
      tags=["internet", "broadband", "dsl", "cable modem", "network", "isp"])
def _(S):
    return [
        shell(rect(7, 3, 10, 14.5, rr(S, 3))),
        dot(12, 7, 1.1), dot(12, 10.5, 1.1), dot(12, 14, 1.1),
        line(seg(6, 21, 18, 21) if S.name == "line" else seg(7, 21, 17, 21)),
    ]


# ============================================================================ power and cables

@icon("plug", CAT, "Electric plug with two prongs and a cord",
      tags=["power", "plug", "electric", "connect", "cord", "mains"], aliases=["power-plug"])
def _(S):
    return [
        line(seg(9, 2.5, 9, 7)),
        line(seg(15, 2.5, 15, 7)),
        shell(poly([(5, 7), (19, 7), (19, 11), (15, 16), (9, 16), (5, 11)], closed=True, r=S.r)),
        line(seg(12, 16, 12, 21.5)),
    ]


@icon("socket", CAT, "Wall power socket with two slots and a ground hole",
      tags=["outlet", "power", "wall socket", "electric", "mains", "receptacle"], aliases=["outlet", "power-outlet"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S))),
        detail(seg(9, 8, 9, 12)),
        detail(seg(15, 8, 15, 12)),
        dot(12, 16, 1.5),
    ]


@icon("cable", CAT, "Cable with a connector plug at each end",
      tags=["cord", "wire", "connector", "lead", "charging cable", "usb cable"], aliases=["cord"])
def _(S):
    wire = "M6 11V15A3 3 0 0 0 12 15V9A3 3 0 0 1 18 9V13"
    return [
        line(seg(6, 2.5, 6, 6)),
        shell(rect(4, 6, 4, 5, rr(S, 1))),
        line(wire),
        shell(rect(16, 13, 4, 5, rr(S, 1))),
        line(seg(18, 18, 18, 21.5)),
    ]


# ============================================================================ power

def _battery(S):
    """Battery body shared with the v0.1 battery icon (horizontal, terminal on the right)."""
    return [shell(rect(2, 7, 17, 10, S.R * 0.5)), line(seg(21.5, 10.5, 21.5, 13.5))]


@icon("battery-charging", CAT, "Battery with a lightning bolt; charging",
      tags=["charging", "charge", "power", "battery", "energy", "plugged in"], aliases=["charging"])
def _(S):
    bolt = [(12, 8.5), (7, 12.5), (10.5, 12.5), (9.5, 15.5), (14.5, 11.5), (11, 11.5)]
    return [*_battery(S), Part("dot", poly(bolt, closed=True))]


@icon("power", CAT, "Power symbol: a broken circle with a vertical line",
      tags=["on", "off", "power", "shutdown", "switch", "start"], aliases=["power-symbol"])
def _(S):
    e = 3 if S.name == "rounded" else 2.5
    return [line(arc(12, 12.5, 8, -58, 238)), line(seg(12, e, 12, 11))]


@icon("power-button", CAT, "Square push button with the power symbol",
      tags=["power", "switch", "on off", "button", "shutdown", "start"], aliases=["on-off-button"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S))),
        detail(arc(12, 12.5, 5, -55, 235)),
        detail(seg(12, 6.5, 12, 11.5)),
    ]


# ============================================================================ wireless

@icon("bluetooth", CAT, "Bluetooth wireless symbol",
      tags=["wireless", "pairing", "bluetooth", "connection", "headset", "bt"], aliases=["bt"])
def _(S):
    return [line(poly([(7, 7.5), (17, 16.5), (12, 21), (12, 3), (17, 7.5), (7, 16.5)], r=S.r), stroke_miterlimit="2")]


@icon("nfc", CAT, "Phone sending contactless waves; near-field communication",
      tags=["contactless", "tap", "near field", "tap to pay", "wireless", "rfid"], aliases=["near-field-communication"])
def _(S):
    return [
        shell(rect(3, 10, 9, 11.5, rr(S, 2.5))),
        detail(seg(6, 18.5, 9, 18.5)),
        line(arc(10, 12, 5.5, -80, -10)),
        line(arc(10, 12, 9, -80, -10)),
    ]


# ============================================================================ play

@icon("gamepad", CAT, "Game controller with a direction pad and buttons",
      tags=["controller", "game", "gaming", "joypad", "play", "console"], aliases=["game-controller", "controller"])
def _(S):
    body = [(7, 6), (17, 6), (19.5, 7.5), (21, 15.5), (20, 18.5), (17.5, 18.5), (15, 15.5),
            (9, 15.5), (6.5, 18.5), (4, 18.5), (3, 15.5), (4.5, 7.5)]
    return [
        shell(poly(body, closed=True, r=0.75 if S.name == "line" else 2)),
        detail(seg(6, 11, 10, 11)),
        detail(seg(8, 9, 8, 13)),
        dot(15, 11, 1.1),
        dot(18, 11, 1.1),
    ]


@icon("joystick", CAT, "Arcade joystick: a ball-top stick on a base with a button",
      tags=["arcade", "game", "gaming", "stick", "controller", "retro"])
def _(S):
    return [
        shell(circle(12, 6, 3)),
        line(seg(12, 9, 12, 16)),
        shell(rect(4, 16, 16, 5, 1 if S.name == "line" else 2.5)),
        sq(7, 17.5, 2, 2) if S.name == "line" else dot(8, 18.5, 1),
    ]


@icon("vr-headset", CAT, "Virtual-reality headset with a head strap",
      tags=["virtual reality", "vr", "goggles", "headset", "metaverse", "immersive"], aliases=["vr"])
def _(S):
    body = [(3, 7), (21, 7), (21, 17), (15.5, 17), (14, 14.5), (10, 14.5), (8.5, 17), (3, 17)]
    return [
        line(poly([(7, 7), (7, 4), (17, 4), (17, 7)], r=S.r)),
        shell(poly(body, closed=True, r=S.r)),
    ]


@icon("drone", CAT, "Quadcopter drone seen from above with four rotors",
      tags=["quadcopter", "uav", "aerial", "flying", "camera drone", "rotor"], aliases=["quadcopter"])
def _(S):
    # Body with a camera lens; each arm ends in a rotor hub with a two-blade propeller (not a node graph).
    out = [shell(rect(9.5, 9.5, 5, 5, 0.5 if S.name == "line" else 2)), dot(12, 12, 1.1)]
    for cx, cy in ((5.8, 5.8), (18.2, 5.8), (5.8, 18.2), (18.2, 18.2)):
        sx, sy = (1 if cx > 12 else -1), (1 if cy > 12 else -1)
        out.append(shell(circle(cx, cy, 3)))
        out.append(detail(seg(cx - 1.6, cy + 0.9 * sx * sy, cx + 1.6, cy - 0.9 * sx * sy)))
        out.append(line(seg(cx - sx * 2.1, cy - sy * 2.1, 12 + sx * 2.5, 12 + sy * 2.5)))
    return out


@icon("robot", CAT, "Robot head with an antenna, eyes and ears",
      tags=["bot", "android", "ai", "automation", "machine", "chatbot"], aliases=["bot"])
def _(S):
    return [
        dot(12, 3.5, 1.5),
        line(seg(12, 5, 12, 7)),
        shell(rect(5, 7, 14, 13, rr(S, 3))),
        line(seg(3, 11.5, 3, 15.5)), line(seg(21, 11.5, 21, 15.5)),
        dot(9.5, 12, 1.5), dot(14.5, 12, 1.5),
        detail(seg(9.5, 16, 14.5, 16)),
    ]


# ============================================================================ gadgets

@icon("calculator", CAT, "Pocket calculator with a display and keypad",
      tags=["calculate", "math", "accounting", "numbers", "arithmetic", "finance"])
def _(S):
    keys = [dot(x, y, 1) for y in (12, 15, 18) for x in (8, 12, 16)]
    return [shell(rect(4, 2.5, 16, 19, rr(S, 3))), sq(7, 5, 10, 4, 0.5), *keys]


@icon("security-camera", CAT, "Wall-mounted security camera",
      tags=["cctv", "surveillance", "camera", "monitoring", "security", "video"], aliases=["cctv"])
def _(S):
    body = [(3.46, 7.41), (16.98, 3.79), (18.54, 9.59), (5.02, 13.21)]
    return [
        shell(poly(body, closed=True, r=S.r)),
        detail(seg(5.87, 6.76, 7.43, 12.56)),
        line(poly([(13.5, 11.5), (14.5, 16), (19.5, 16)], r=S.r)),
        line(seg(20.5, 12.5, 20.5, 19.5)),
    ]


@icon("smart-speaker", CAT, "Smart speaker with a light ring, answering with sound waves",
      tags=["voice assistant", "speaker", "alexa", "home", "assistant", "audio"], aliases=["voice-assistant"])
def _(S):
    return [
        shell(rect(4, 8, 11, 13.5, rr(S, 4) if S.name == "rounded" else 2)),
        detail(seg(4, 12, 15, 12)),
        dot(9.5, 16.75, 1.25),
        line(arc(13, 8, 3.5, -85, -5)),
        line(arc(13, 8, 7, -85, -5)),
    ]


@icon("remote-control", CAT, "TV remote control with a power button, direction pad and keys",
      tags=["remote", "tv remote", "controller", "clicker", "television", "buttons"], aliases=["remote"])
def _(S):
    return [
        shell(rect(6.5, 2.5, 11, 19, rr(S, 3))),
        dot(12, 5.25, 1.1),
        detail(seg(9.5, 11, 14.5, 11)),
        detail(seg(12, 8.5, 12, 13.5)),
        dot(9.75, 17.25, 1), dot(14.25, 17.25, 1),
    ]


# ============================================================================ lighting and climate

@icon("lightbulb", CAT, "Light bulb with a screw base",
      tags=["light", "bulb", "idea", "lamp", "illumination", "electric"], aliases=["light-bulb", "bulb"])
def _(S):
    top = "C9.5 12.8 6.5 11.5 6.5 8.5A5.5 5.5 0 0 1 17.5 8.5C17.5 11.5 14.5 12.8 14.5 13.8"
    if S.name == "line":
        d = "M9.5 20.5V13.8" + top + "V20.5Z"
    else:
        d = "M11 20.5A1.5 1.5 0 0 1 9.5 19V13.8" + top + "V19A1.5 1.5 0 0 1 13 20.5Z"
    return [shell(d), detail(seg(9.5, 17, 14.5, 17))]


@icon("lamp", CAT, "Table lamp with a shade, stem and base",
      tags=["light", "table lamp", "shade", "desk", "lighting", "furniture"], aliases=["table-lamp"])
def _(S):
    return [
        shell(poly([(8, 3), (16, 3), (19.5, 11), (4.5, 11)], closed=True, r=S.r)),
        line(seg(12, 11, 12, 20.5)),
        line(seg(7, 20.5, 17, 20.5) if S.name == "line" else seg(8, 20.5, 16, 20.5)),
    ]


@icon("flashlight", CAT, "Handheld flashlight (torch) with its lens at the top",
      tags=["torch", "light", "beam", "lantern", "flash", "camping"], aliases=["torch"])
def _(S):
    return [
        shell(poly([(6, 3), (18, 3), (18, 6), (15, 10), (15, 21), (9, 21), (9, 10), (6, 6)], closed=True, r=S.r)),
        detail(seg(6, 6, 18, 6)),
        dot(12, 14, 1.25),
    ]


def _fan_blade(S, rot):
    """Pointed blade (a lens) set off-axis so the three blades read as a spinning pinwheel."""
    x1, y1 = polar(12, 12, 3.6, -110 + rot)
    x2, y2 = polar(12, 12, 8.8, -50 + rot)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    L = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    nx, ny = -(y2 - y1) / L, (x2 - x1) / L
    b = 3.1 * 2
    d = (f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx - nx * b)} {fmt(my - ny * b)} {fmt(x2)} {fmt(y2)}"
         f"Q{fmt(mx + nx * b * 0.55)} {fmt(my + ny * b * 0.55)} {fmt(x1)} {fmt(y1)}Z")
    return shell(d, stroke_miterlimit="2")


@icon("fan", CAT, "Three-bladed fan",
      tags=["ventilation", "cooling", "air", "blower", "propeller", "fan speed"], aliases=["ventilator"])
def _(S):
    return [_fan_blade(S, 0), _fan_blade(S, 120), _fan_blade(S, 240), dot(12, 12, 1.5)]


@icon("thermometer", CAT, "Thermometer with a bulb and a rising column",
      tags=["temperature", "heat", "fever", "weather", "degrees", "hot"], aliases=["temperature"])
def _(S):
    if S.name == "line":
        d = "M10 14.63V3H14V14.63A3.5 3.5 0 1 1 10 14.63Z"
    else:
        d = "M10 14.63V5A2 2 0 0 1 14 5V14.63A3.5 3.5 0 1 1 10 14.63Z"
    return [shell(d), detail(seg(12, 9, 12, 16)), dot(12, 17.5, 1.75)]


# ============================================================================ cards and media

@icon("sd-card", CAT, "SD memory card with a clipped corner and contacts",
      tags=["memory card", "sd", "storage", "camera card", "flash", "microsd"], aliases=["memory-card"])
def _(S):
    return [
        shell(poly([(5, 3), (15, 3), (19, 7), (19, 21), (5, 21)], closed=True, r=S.R * 0.5)),
        detail(seg(8.5, 6.5, 8.5, 9.5)),
        detail(seg(12, 6.5, 12, 9.5)),
        detail(seg(15.5, 7.5, 15.5, 9.5)),
    ]


@icon("sim-card", CAT, "SIM card with a clipped corner and a contact chip",
      tags=["sim", "mobile", "carrier", "cellular", "esim", "phone card"], aliases=["sim"])
def _(S):
    return [
        shell(poly([(5, 3), (14, 3), (19, 8), (19, 21), (5, 21)], closed=True, r=S.R * 0.5)),
        detail(rect(8, 11, 8, 7, rr(S, 1.5))),
        detail(seg(8, 14.5, 16, 14.5)),
        detail(seg(12, 11, 12, 18)),
    ]


@icon("floppy-disk", CAT, "Floppy disk with a metal shutter and a label",
      tags=["save", "diskette", "floppy", "disk", "storage", "retro"], aliases=["diskette", "save"])
def _(S):
    return [
        shell(poly([(3, 3), (17, 3), (21, 7), (21, 21), (3, 21)], closed=True, r=S.R * 0.5)),
        detail(poly([(7.5, 3), (7.5, 8), (15, 8), (15, 3)], r=S.r)),
        detail(poly([(7, 21), (7, 14), (17, 14), (17, 21)], r=S.r)),
    ]


@icon("cd", CAT, "Compact disc with a centre hole and a highlight",
      tags=["compact disc", "disc", "music", "cd-rom", "album", "optical"], aliases=["compact-disc", "disc"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(circle(12, 12, 2.5)), detail(arc(12, 12, 5.75, 195, 255))]


@icon("dvd", CAT, "Disc sliding out of its case",
      tags=["disc", "movie", "video", "blu-ray", "optical", "film"], aliases=["dvd-disc"])
def _(S):
    return [
        line(poly([(15, 3), (3, 3), (3, 21), (15, 21)], r=S.R * 0.5)),
        shell(circle(15, 12, 5.5)),
        detail(circle(15, 12, 1.75)),
    ]


# ============================================================================ audio

@icon("headset", CAT, "Headset: headphones with a microphone boom",
      tags=["headphones", "microphone", "support", "call center", "gaming", "voice chat"], aliases=["headset-mic"])
def _(S):
    return [
        line("M5 13V12A7 7 0 0 1 19 12V13"),
        shell(rect(3, 13, 4, 6.5, S.R * 0.5)),
        shell(rect(17, 13, 4, 6.5, S.R * 0.5)),
        line(poly([(5, 19.5), (5, 21), (11, 21)], r=S.r)),
        dot(12.5, 21, 1.25),
    ]


def _bud(S, side):
    """One stemmed earbud; side 1 = left bud, -1 = right bud (mirrored). Stems splay outward."""
    cx = 12 - side * 5
    return [shell(circle(cx, 7.5, 3.25)), dot(cx, 7.5, 1), line(seg(cx + side * 1.1, 10.9, cx - side * 0.5, 20.5))]


@icon("earbuds", CAT, "A pair of wireless earbuds with stems",
      tags=["earphones", "wireless", "buds", "in-ear", "audio", "tws"], aliases=["earphones"])
def _(S):
    return [
        *_bud(S, 1), *_bud(S, -1),
    ]


# ============================================================================ retro

@icon("tv-retro", CAT, "Old tube television with antenna, knobs and legs",
      tags=["television", "crt", "vintage", "old tv", "retro", "broadcast"], aliases=["old-tv", "crt-tv"])
def _(S):
    return [
        line(poly([(8, 2.5), (12, 6), (16, 2.5)], r=S.r)),
        shell(rect(3, 6, 18, 13, rr(S, 3))),
        detail(seg(15.5, 6, 15.5, 19)),
        dot(18.25, 10, 1.1), dot(18.25, 14, 1.1),
        line(seg(6.5, 19, 6.5, 21)), line(seg(17.5, 19, 17.5, 21)),
    ]


@icon("radio-retro", CAT, "Vintage table radio with an arched top, grille and dial",
      tags=["radio", "vintage", "old radio", "wireless", "broadcast", "retro"], aliases=["vintage-radio"])
def _(S):
    top = "C3 6 7 3.5 12 3.5C17 3.5 21 6 21 11"
    if S.name == "line":
        d = "M3 21V11" + top + "V21Z"
    else:
        d = "M5 21A2 2 0 0 1 3 19V11" + top + "V19A2 2 0 0 1 19 21Z"
    return [
        shell(d),
        detail(seg(8, 8.5, 16, 8.5)),
        detail(seg(6, 12, 18, 12)),
        detail(seg(3, 15.5, 21, 15.5)),
        dot(7.5, 18.25, 1),
        dot(11, 18.25, 1),
    ]


@icon("phone-retro", CAT, "Rotary telephone with its handset resting on top",
      tags=["telephone", "rotary", "landline", "vintage", "old phone", "call"], aliases=["rotary-phone", "telephone-retro"])
def _(S):
    return [
        line("M4.5 9V7.5C4.5 5.5 7.5 4 12 4C16.5 4 19.5 5.5 19.5 7.5V9"),
        sq(2.5, 8, 4, 2.5, rr(S, 1) * 0.5), sq(17.5, 8, 4, 2.5, rr(S, 1) * 0.5),
        shell(poly([(7, 12.5), (17, 12.5), (20.5, 21), (3.5, 21)], closed=True, r=S.r)),
        detail(circle(12, 16.75, 1.75)),
    ]


# ============================================================================ consoles and projection

@icon("game-console", CAT, "Home game console with a controller",
      tags=["console", "gaming", "video game", "playstation", "xbox", "games"], aliases=["video-game-console"])
def _(S):
    pad = [(8, 14), (16, 14), (18, 15.5), (19, 19.5), (17.5, 21), (15, 19.5), (9, 19.5), (6.5, 21), (5, 19.5), (6, 15.5)]
    return [
        shell(rect(3, 3, 18, 7, rr(S, 2.5))),
        detail(seg(6, 6.5, 12, 6.5)),
        dot(17, 6.5, 1.1),
        shell(poly(pad, closed=True, r=0.5 if S.name == "line" else 1.5)),
    ]


@icon("handheld-console", CAT, "Handheld game console with a screen between two sets of controls",
      tags=["handheld", "portable console", "gaming", "switch", "game boy", "games"], aliases=["portable-console"])
def _(S):
    return [
        shell(rect(3, 6, 18, 12, 3 if S.name == "line" else 5)),
        sq(8, 9, 8, 6, 0.5),
        dot(5.75, 10.5, 1),
        dot(18.25, 13.5, 1),
    ]


@icon("projector-device", CAT, "Projector with its lens casting rays of light",
      tags=["projector", "beamer", "presentation", "cinema", "slides", "light beam"], aliases=["beamer"])
def _(S):
    return [
        line(seg(14.5, 2.5, 14.5, 6.5)),
        line(seg(9.5, 4, 11.5, 7)),
        line(seg(19.5, 4, 17.5, 7)),
        shell(rect(3, 9.5, 18, 9, rr(S, 3))),
        dot(14.5, 14, 2.5),
        dot(7, 14, 1),
        line(seg(6.5, 18.5, 6.5, 21)), line(seg(17.5, 18.5, 17.5, 21)),
    ]


# ============================================================================ charging

@icon("charger", CAT, "Wall charger with prongs, a lightning bolt and a cable",
      tags=["charging", "adapter", "power adapter", "wall charger", "plug", "usb charger"], aliases=["power-adapter"])
def _(S):
    bolt = [(12.5, 8.5), (8.5, 13), (11.5, 13), (10.5, 16.5), (15, 12), (12, 12)]
    return [
        line(seg(9, 3, 9, 7)), line(seg(15, 3, 15, 7)),
        shell(rect(5, 7, 14, 11, rr(S, 3))),
        Part("dot", poly(bolt, closed=True)),
        line(seg(12, 18, 12, 21) if S.name == "line" else seg(12, 18, 12, 20.5)),
    ]


@icon("power-bank", CAT, "Portable power bank with a port and a charging bolt",
      tags=["battery pack", "portable charger", "powerbank", "charging", "battery", "travel"], aliases=["battery-pack"])
def _(S):
    bolt = [(12.5, 10), (8.5, 14.5), (11.5, 14.5), (10.5, 18), (15, 13.5), (12, 13.5)]
    return [
        shell(rect(6, 3, 12, 18, rr(S, 3))),
        detail(seg(10, 6.5, 14, 6.5)),
        Part("dot", poly(bolt, closed=True)),
    ]


# ============================================================================ ports and networking

@icon("ethernet-port", CAT, "Ethernet (RJ45) network socket with pins",
      tags=["lan", "rj45", "network", "wired", "port", "cable"], aliases=["lan-port", "rj45"])
def _(S):
    return [
        shell(poly([(3, 20), (3, 9), (7, 9), (7, 4.5), (17, 4.5), (17, 9), (21, 9), (21, 20)], closed=True, r=S.r)),
        detail(seg(8, 12, 8, 15)),
        detail(seg(12, 12, 12, 15)),
        detail(seg(16, 12, 16, 15)),
    ]


@icon("hdmi", CAT, "HDMI port: a wide socket with chamfered lower corners",
      tags=["hdmi", "video port", "display port", "cable", "tv", "connector"], aliases=["hdmi-port"])
def _(S):
    return [
        shell(poly([(3, 8), (21, 8), (21, 12), (18, 16), (6, 16), (3, 12)], closed=True, r=S.r)),
        detail(seg(7, 12, 17, 12)),
    ]


@icon("wifi-router", CAT, "Wireless router sending Wi-Fi signal",
      tags=["wifi", "wireless", "router", "internet", "hotspot", "network"], aliases=["wireless-router"])
def _(S):
    return [
        line(arc(12, 11, 3, 225, 315)),
        line(arc(12, 11, 7, 225, 315)),
        shell(rect(3, 13, 18, 7, rr(S, 3))),
        dot(7, 16.5, 1), dot(10.5, 16.5, 1),
    ]


def _rack_unit(S, y):
    """Solid server unit with a knocked-out status light (inverts in Filled)."""
    from geometry import path_to_d
    unit = D(P(rect(7, y, 10, 3, 0.5 if S.name == "line" else 1.5)), P(circle(9, y + 1.5, 0.8)))
    return Part("dot", path_to_d(unit))


@icon("server-rack", CAT, "Rack cabinet on feet holding three inset server units",
      tags=["rack", "datacenter", "servers", "hosting", "cabinet", "infrastructure"], aliases=["rack"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 17.5, rr(S, 2.5))),
        *[_rack_unit(S, y) for y in (5, 9.5, 14)],
        line(seg(6.5, 20, 6.5, 21.5)), line(seg(17.5, 20, 17.5, 21.5)),
    ]