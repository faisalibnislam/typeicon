"""TypeIcon Core: appliances (batch 002).

Home utilities, electrical fittings, plugs and sockets, lamps and light fittings. Drawn from the objects
themselves on the 24 px grid; plug and socket types are front views of the pin or hole pattern.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "appliances"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def knock(d) -> Part:
    """Small solid shape: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


def rot_pts(pts, deg, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c) for x, y in pts]


def rot_d(d, deg, cx=12.0, cy=12.0):
    """Rotate a closed path clockwise on screen."""
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rseg(x1, y1, x2, y2, deg):
    (a, b), (c, e) = rot_pts([(x1, y1), (x2, y2)], deg)
    return seg(a, b, c, e)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def bolt(cx, cy, s=1.0):
    pts = [(0.5, -3.75), (-2.5, 0.5), (0, 0.5), (-0.75, 3.75), (2.5, -0.75), (0, -0.75)]
    return poly([(cx + x * s, cy + y * s) for x, y in pts], closed=True)


def drop(cx, top, r, cy):
    """Water drop: tip at (cx, top), round bottom of radius r centred at (cx, cy)."""
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + r * 0.35)} {fmt(top + (cy - top) * 0.35)} {fmt(cx + r)} {fmt(cy - r * 0.55)} "
            f"{fmt(cx + r)} {fmt(cy)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx - r)} {fmt(cy)}"
            f"C{fmt(cx - r)} {fmt(cy - r * 0.55)} {fmt(cx - r * 0.35)} {fmt(top + (cy - top) * 0.35)} {fmt(cx)} {fmt(top)}Z")


def flame(cx, cy, s=1.0):
    """Small flame, about 4 x 5.5 px at s = 1, centred on (cx, cy)."""
    def p(x, y):
        return f"{fmt(cx + x * s)} {fmt(cy + y * s)}"
    return (f"M{p(0, -2.75)}C{p(1.2, -1.5)} {p(2, -0.5)} {p(2, 0.75)}A{fmt(2 * s)} {fmt(2 * s)} 0 0 1 {p(-2, 0.75)}"
            f"C{p(-2, -0.2)} {p(-1.4, -0.9)} {p(-0.8, -1.4)}C{p(-0.6, -0.6)} {p(-0.2, -0.3)} {p(0.2, -0.3)}"
            f"C{p(0.4, -1.2)} {p(0.2, -2)} {p(0, -2.75)}Z")


# ============================================================================ water and gas utilities

@icon("radiator-valve", CAT, "Thermostatic radiator valve with a ribbed head on a valve body between two pipes",
      tags=["trv", "thermostatic valve", "radiator", "heating", "thermostat", "valve"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 8, rr(S, 3))),
        detail(seg(10, 4.5, 10, 8.5)), detail(seg(14, 4.5, 14, 8.5)),
        line(seg(12, 10.5, 12, 14.5)),
        shell(rect(8.5, 14.5, 7, 6, rr(S, 2))),
        line(seg(2, 17.5, 8.5, 17.5)), line(seg(15.5, 17.5, 22, 17.5)),
    ]


@icon("water-heater", CAT, "Tall hot water tank with two pipes on top and a control box near the bottom",
      tags=["hot water tank", "boiler", "cylinder", "geyser", "hot water", "heater"])
def _(S):
    return [
        line(seg(9.5, 2, 9.5, 5)), line(seg(14.5, 2, 14.5, 5)),
        shell(rect(6, 5, 12, 16.5, L(S, 2.5, 5))),
        detail(rect(9, 14, 6, 3.5, rr(S, 1) * 0.5)),
    ]


@icon("tankless-water-heater", CAT, "Slim wall-mounted water heater box with a display, a flame and pipes below",
      tags=["on demand water heater", "instant water heater", "combi", "gas heater", "hot water", "wall heater"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 14.5, rr(S, 3))),
        detail(seg(9.5, 6, 14.5, 6)),
        knock(flame(12, 11.75, 0.95)),
        line(seg(9, 17, 9, 21.5)), line(seg(15, 17, 15, 21.5)),
    ]


@icon("solar-water-heater", CAT, "Solar water heater: a sloping collector panel of tubes with a tank above it",
      tags=["solar thermal", "solar collector", "hot water", "roof", "renewable", "evacuated tube"])
def _(S):
    top, bot = 11.0, 20.5
    xl_t, xl_b, xr_t, xr_b = 7.0, 3.0, 21.0, 17.0

    def at(fr):
        return xl_t + (xr_t - xl_t) * fr, xl_b + (xr_b - xl_b) * fr
    tubes = []
    for fr in (1 / 3, 2 / 3):
        a, b = at(fr)
        tubes.append(detail(seg(a, top, b, bot)))
    return [
        shell(rect(8, 3, 13, 4.5, 2.25)),
        shell(poly([(xl_b, bot), (xl_t, top), (xr_t, top), (xr_b, bot)], closed=True, r=S.r)),
        *tubes,
    ]


@icon("water-softener", CAT, "Water softener: a tall resin tank piped to a shorter salt tank",
      tags=["softener", "hard water", "limescale", "brine tank", "salt", "water treatment"])
def _(S):
    return [
        shell(rect(3, 3, 7.5, 18, rr(S, 3))),
        detail(seg(3, 7.5, 10.5, 7.5)),
        line(poly([(10.5, 5), (17.5, 5), (17.5, 10)], r=S.r)),
        shell(rect(13.5, 10, 8, 11, rr(S, 3))),
        knock(drop(17.5, 12.5, 1.8, 16.5)),
    ]


@icon("under-sink-water-filter", CAT, "Under-sink water filter: two canisters hanging from a bracket fed by pipes",
      tags=["water filter", "filtration", "drinking water", "purifier", "cartridge", "under sink"])
def _(S):
    return [
        line(poly([(2, 3.5), (7, 3.5), (7, 7)], r=S.r)),
        line(poly([(22, 3.5), (17, 3.5), (17, 7)], r=S.r)),
        line(seg(3, 7, 21, 7)),
        shell(rect(4, 9, 6, 12, rr(S, 2.5))),
        shell(rect(14, 9, 6, 12, rr(S, 2.5))),
    ]


@icon("sump-pump", CAT, "Sump pump sitting in a pit below the floor with a float and a discharge pipe",
      tags=["sump", "basement", "flood", "drainage", "pit pump", "water pump"])
def _(S):
    return [
        line(poly([(2, 8), (4, 8), (4, 21), (20, 21), (20, 8), (22, 8)], r=S.r)),
        shell(rect(6.5, 13, 5, 6.5, rr(S, 1.5))),
        line(seg(9, 13, 9, 3)),
        dot(16, 14.5, 1.5),
    ]


@icon("water-pump", CAT, "Centrifugal water pump: a round pump housing joined to a finned motor on a base",
      tags=["pump", "centrifugal pump", "booster pump", "motor", "water supply", "irrigation"])
def _(S):
    return [
        line(seg(7, 8.5, 7, 3)),
        shell(circle(7, 13, 4.5)),
        dot(7, 13, 1.5),
        shell(rect(12, 6, 9, 12, rr(S, 2))),
        detail(seg(12, 10, 21, 10)), detail(seg(12, 14, 21, 14)),
        line(seg(16.5, 18, 16.5, 21)),
        line(seg(3, 21, 21, 21) if S.name == "line" else seg(4, 21, 20, 21)),
    ]


@icon("stopcock", CAT, "Stopcock: an in-line water valve on a pipe with a round wheel handle",
      tags=["shut off valve", "water valve", "stop valve", "gate valve", "mains water", "plumbing"],
      aliases=["shutoff-valve"])
def _(S):
    return [
        shell(circle(12, 5.5, 3)),
        line(seg(12, 8.5, 12, 12.5)),
        shell(rect(8, 12.5, 8, 8, rr(S, 2))),
        line(seg(2, 14.5, 8, 14.5)), line(seg(2, 18.5, 8, 18.5)),
        line(seg(16, 14.5, 22, 14.5)), line(seg(16, 18.5, 22, 18.5)),
    ]


@icon("gas-valve", CAT, "Gas valve on a pipe with its flat lever handle lying along the pipe",
      tags=["gas shut off", "ball valve", "gas tap", "lever valve", "gas supply", "plumbing"])
def _(S):
    body = union(rect(2, 13.5, 20, 5, rr(S, 1)), rect(7, 11.5, 8, 9, rr(S, 2)))
    return [
        shell(rect(6.5, 3.5, 15, 3.5, L(S, 0.75, 1.75))),
        line(seg(9.5, 7, 9.5, 11.5)),
        shell(body),
    ]


@icon("water-meter", CAT, "Round water meter on a pipe with a counter window and a water drop",
      tags=["meter", "water usage", "utility", "consumption", "water bill", "reading"])
def _(S):
    return [
        line(seg(2, 12, 5, 12)), line(seg(19, 12, 22, 12)),
        shell(circle(12, 12, 7)),
        detail(rect(8.5, 7.5, 7, 3, L(S, 0, 1.5))),
        knock(drop(12, 12.25, 1.9, 15.75)),
    ]


@icon("gas-meter", CAT, "Gas meter box with a counter window, a flame mark and pipes entering the top",
      tags=["meter", "gas usage", "utility", "consumption", "gas bill", "reading"])
def _(S):
    return [
        line(seg(6.5, 2, 6.5, 7)), line(seg(17.5, 2, 17.5, 7)),
        shell(rect(3, 7, 18, 14, rr(S))),
        detail(rect(7, 10, 10, 3.5, rr(S, 1) * 0.5)),
        knock(flame(12, 17.25, 0.8)),
    ]


@icon("prepaid-meter", CAT, "Prepaid utility meter with a power bolt, a display and a small keypad",
      tags=["pay as you go", "token meter", "keypad meter", "top up", "electricity credit", "utility"])
def _(S):
    keys = [dot(x, y, 1) if S.name == "rounded" else sq(x - 1, y - 1, 2, 2) for y in (15, 18.5) for x in (8.5, 12, 15.5)]
    return [
        shell(rect(5, 2.5, 14, 19.5, rr(S, 3))),
        knock(bolt(9.75, 7.5, 0.7)),
        detail(seg(13.5, 6, 16, 6)), detail(seg(13.5, 9, 16, 9)),
        *keys,
    ]


@icon("propane-tank", CAT, "Propane gas cylinder with a collar ring and valve on top and a foot ring",
      tags=["propane", "lpg", "gas bottle", "gas cylinder", "bbq gas", "butane"], aliases=["gas-cylinder"])
def _(S):
    return [
        line(poly([(8.5, 7), (8.5, 3), (15.5, 3), (15.5, 7)], r=S.r)),
        dot(12, 5.25, 1.25),
        shell(rect(4.5, 7, 15, 12, L(S, 3.5, 5.5))),
        detail(seg(4.5, 13, 19.5, 13)),
        line(poly([(8, 19), (8, 21), (16, 21), (16, 19)], r=S.r * 0.5)),
    ]


@icon("heating-oil-tank", CAT, "Horizontal heating oil tank on legs with a fill pipe and a gauge",
      tags=["oil tank", "fuel tank", "heating oil", "kerosene", "storage tank", "boiler fuel"])
def _(S):
    return [
        line(seg(7.5, 3.5, 7.5, 9)), line(seg(5.5, 3.5, 9.5, 3.5) if S.name == "line" else seg(6, 3.5, 9, 3.5)),
        shell(circle(16, 5, 2)),
        shell(rect(2.5, 9, 19, 9, L(S, 3, 4.5))),
        knock(drop(12, 10.75, 1.7, 14.75)),
        line(seg(6, 18, 6, 21.5)), line(seg(18, 18, 18, 21.5)),
    ]


@icon("rainwater-tank", CAT, "Rainwater barrel fed by a downpipe with a small tap near the bottom",
      tags=["water butt", "rain barrel", "rainwater harvesting", "garden", "water saving", "downpipe"],
      aliases=["water-butt"])
def _(S):
    body = "M6.5 8.5H15.5C17.2 12 17.2 17.5 15.5 21H6.5C4.8 17.5 4.8 12 6.5 8.5Z"
    return [
        line(poly([(21, 2), (21, 5), (13, 5), (13, 8.5)], r=S.r)),
        shell(body),
        detail(seg(5.6, 12, 16.4, 12)), detail(seg(5.6, 17.5, 16.4, 17.5)),
        line(poly([(16.5, 19), (19.5, 19), (19.5, 21)], r=S.r * 0.5)),
    ]


@icon("electric-shower", CAT, "Electric shower unit with a dial, a hose and a hand-held shower head",
      tags=["shower", "instant shower", "shower unit", "bathroom", "hot water", "power shower"])
def _(S):
    return [
        shell(rect(2.5, 3, 10, 10.5, rr(S, 3))),
        detail(circle(7.5, 8.25, 2)),
        line("M7.5 13.5V17A3 3 0 0 0 10.5 20H15A3 3 0 0 0 18 17V9"),
        shell("M14 3.5H22A4 4 0 0 1 14 3.5Z" if S.name == "rounded" else "M14 3H22L20 7H16Z"),
        dot(15, 10.5, 1), dot(21, 10.5, 1),
    ]


@icon("home-battery", CAT, "Wall-mounted home battery with a charge bolt and a level bar",
      tags=["battery storage", "wall battery", "energy storage", "solar battery", "backup power", "house battery"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 3))),
        knock(bolt(12, 9, 0.95)),
        sq(7.75, 16, 2.25, 2.5, 0), sq(10.875, 16, 2.25, 2.5, 0), sq(14, 16, 2.25, 2.5, 0),
    ]


@icon("portable-generator", CAT, "Portable generator: an engine box with a pull starter and sockets under a carry frame",
      tags=["generator", "genset", "backup power", "power outage", "camping", "petrol generator"])
def _(S):
    return [
        line(poly([(5, 8), (5, 3.5), (19, 3.5), (19, 8)], r=S.r)),
        shell(rect(3, 8, 18, 11, rr(S, 3))),
        knock(bolt(8.75, 13.5, 0.85)),
        dot(15, 11.75, 1.1), dot(15, 15.25, 1.1),
        line(seg(6, 19, 6, 21.5)), line(seg(18, 19, 18, 21.5)),
    ]


@icon("ups-power-supply", CAT, "Tower UPS backup power unit with a battery display and a power button",
      tags=["ups", "uninterruptible power supply", "battery backup", "surge", "server", "power outage"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 19, rr(S, 3))),
        detail(rect(8.5, 5.5, 6, 3.5, L(S, 0, 0.75))),
        sq(14.5, 6.25, 1.5, 2, 0),
        detail(arc(12, 15.5, 3, -55, 235)),
        detail(seg(12, 11.5, 12, 14.5)),
    ]


@icon("power-inverter", CAT, "Power inverter symbol: a box split by a diagonal with direct current and a sine wave",
      tags=["inverter", "dc to ac", "converter", "solar inverter", "car inverter", "power supply"])
def _(S):
    c = L(S, 3.6, 4.2)
    return [
        shell(rect(3, 3, 18, 18, rr(S))),
        detail(seg(c, 24 - c, 24 - c, c)),
        detail(seg(6, 7, 11, 7)), detail(seg(6, 10.5, 8.5, 10.5)),
        detail("M12.5 16C13.8 14 15.2 14 16 16S18.2 18 19.5 16" if S.name == "rounded" else
               "M12.5 16L14.25 14.5L16 16L17.75 17.5L19.5 16"),
    ]


@icon("fuse-box", CAT, "Consumer unit (fuse box) panel with a row of breaker switches",
      tags=["consumer unit", "breaker panel", "distribution board", "electrical panel", "fuses", "mains"],
      aliases=["consumer-unit"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S))),
        detail(seg(3, 8.5, 21, 8.5)),
        *[sq(x, 12, 2, 5, L(S, 0, 1)) for x in (5.75, 9.25, 12.75, 16.25)],
    ]


@icon("circuit-breaker", CAT, "Single circuit breaker module with a toggle lever and terminals top and bottom",
      tags=["breaker", "mcb", "trip switch", "rcd", "overload", "din rail"], aliases=["mcb"])
def _(S):
    return [
        shell(rect(7, 2.5, 10, 19, rr(S, 3))),
        dot(12, 5.75, 1.25), dot(12, 18.25, 1.25),
        detail(seg(7, 12, 17, 12)),
        sq(10, 8.5, 4, 3.5, L(S, 0, 1)),
    ]


@icon("electrical-fuse", CAT, "Cartridge fuse with metal end caps and a wire filament inside",
      tags=["fuse", "cartridge fuse", "glass fuse", "blown fuse", "overcurrent", "electronics"])
def _(S):
    k = L(S, 0, 1.5)
    body = union(rect(2.5, 6.5, 5, 11, k), rect(7, 8.5, 10, 7, 0), rect(16.5, 6.5, 5, 11, k))
    return [
        shell(body),
        detail(seg(7.5, 8.5, 7.5, 15.5)), detail(seg(16.5, 8.5, 16.5, 15.5)),
        detail(seg(7.5, 12, 16.5, 12)),
    ]


@icon("junction-box", CAT, "Electrical junction box with a screwed lid and cables entering from two sides",
      tags=["junction box", "connection box", "wiring", "electrical box", "enclosure", "cables"])
def _(S):
    pts = [(8.5, 8.5), (15.5, 8.5), (8.5, 15.5), (15.5, 15.5)]
    return [
        shell(rect(5, 5, 14, 14, rr(S))),
        *[dot(x, y, 1.1) if S.name == "rounded" else sq(x - 1, y - 1, 2, 2) for x, y in pts],
        line(seg(2, 12, 5, 12)), line(seg(19, 12, 22, 12)),
    ]


@icon("power-strip", CAT, "Power strip with a row of sockets, an on-off switch and a cord",
      tags=["extension lead", "power board", "multi socket", "surge protector", "extension cord", "outlets"],
      aliases=["extension-lead", "power-board"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 8, rr(S, 3))),
        dot(6.5, 8.5, 1.4), dot(10.5, 8.5, 1.4), dot(14.5, 8.5, 1.4),
        sq(17.5, 7, 1.75, 3, 0),
        line("M6 12.5V16A3.5 3.5 0 0 0 9.5 19.5H21"),
    ]


@icon("extension-reel", CAT, "Cable extension reel: a round drum with a socket hub and a crank handle",
      tags=["cable reel", "cable drum", "extension cable", "extension cord", "outdoor power", "hose reel"])
def _(S):
    return [
        shell(circle(11, 11.5, 8)),
        detail(circle(11, 11.5, 3)),
        line(poly([(19, 11.5), (21.5, 11.5), (21.5, 15)], r=S.r * 0.5)),
        line(seg(6, 18, 4, 21.5)), line(seg(16, 18, 18, 21.5)),
    ]


@icon("travel-adapter", CAT, "Travel plug adapter cube with pins on two faces and a socket on the front",
      tags=["travel plug", "adapter", "universal adapter", "power adapter", "abroad", "international plug"],
      aliases=["plug-adapter"])
def _(S):
    return [
        line(seg(10, 2, 10, 7)), line(seg(15, 2, 15, 7)),
        line(seg(2, 12, 5.5, 12)), line(seg(2, 16.5, 5.5, 16.5)),
        shell(rect(5.5, 7, 14, 14, rr(S))),
        detail(seg(10.5, 12, 10.5, 16)), detail(seg(14.5, 12, 14.5, 16)),
    ]


@icon("multi-plug", CAT, "Multi-plug adapter with plug pins on top and three sockets on the front",
      tags=["adapter plug", "splitter", "double adapter", "socket adapter", "multiway", "outlets"],
      aliases=["socket-adapter"])
def _(S):
    return [
        line(seg(9.5, 2, 9.5, 7)), line(seg(14.5, 2, 14.5, 7)),
        shell(poly([(3, 7), (21, 7), (21, 16), (17, 21), (7, 21), (3, 16)], closed=True, r=S.r)),
        dot(7.5, 12.5, 1.5), dot(12, 12.5, 1.5), dot(16.5, 12.5, 1.5),
    ]


@icon("timer-socket", CAT, "Plug-in timer socket with a round dial of timing pins",
      tags=["timer plug", "time switch", "plug timer", "24 hour timer", "schedule", "lamp timer"],
      aliases=["plug-timer"])
def _(S):
    ticks = [dot(*pt, 0.9) for pt in [(12 + 5.5 * math.cos(math.radians(a)), 12.5 + 5.5 * math.sin(math.radians(a))) for a in range(0, 360, 45)]]
    return [
        shell(rect(3, 3.5, 18, 18, rr(S))),
        *ticks,
        detail(poly([(12, 10), (12, 12.5), (14, 12.5)], r=S.r * 0.4)),
    ]


# ============================================================================ outlets, plugs and sockets

def _slots(x1, x2, y, h):
    return [detail(seg(x1, y, x1, y + h)), detail(seg(x2, y, x2, y + h))]


@icon("smart-plug", CAT, "Smart plug module with a socket face and a wireless signal above",
      tags=["wifi plug", "smart socket", "home automation", "connected plug", "remote control", "smart home"],
      aliases=["wifi-plug"])
def _(S):
    return [
        line(arc(12, 10, 3.5, 225, 315)), line(arc(12, 10, 7, 232, 308)),
        shell(rect(4.5, 10, 15, 11.5, rr(S))),
        *_slots(9.5, 14.5, 13, 3.5),
        dot(12, 18.75, 1),
    ]


@icon("usb-outlet", CAT, "Wall socket plate with one power outlet and two USB charging ports",
      tags=["usb socket", "usb charger", "wall charger", "charging port", "outlet", "phone charging"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, rr(S))),
        *_slots(9.5, 14.5, 5.5, 4),
        dot(12, 12, 1.1),
        sq(7.5, 15.5, 3.5, 2.5, L(S, 0, 0.75)), sq(13, 15.5, 3.5, 2.5, L(S, 0, 0.75)),
    ]


@icon("gfci-outlet", CAT, "GFCI outlet plate with two sockets and test and reset buttons between them",
      tags=["gfi outlet", "rcd socket", "ground fault", "safety outlet", "bathroom outlet", "receptacle"],
      aliases=["gfi-outlet"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, rr(S))),
        *_slots(9.5, 14.5, 5, 3),
        sq(7, 10.5, 4.25, 3, L(S, 0, 1)), sq(12.75, 10.5, 4.25, 3, L(S, 0, 1)),
        *_slots(9.5, 14.5, 16, 3),
    ]


@icon("outdoor-outlet", CAT, "Weatherproof outdoor socket with its hinged cover flipped up",
      tags=["weatherproof outlet", "outside socket", "garden socket", "exterior outlet", "waterproof socket", "patio"])
def _(S):
    return [
        shell(poly([(5.5, 8), (18.5, 8), (17, 3), (7, 3)], closed=True, r=S.r)),
        shell(rect(4, 10, 16, 11.5, rr(S))),
        *_slots(9.5, 14.5, 13, 3),
        dot(12, 18.5, 1),
    ]


@icon("floor-outlet", CAT, "Floor socket box set into the floor with its lid flipped open",
      tags=["floor box", "floor socket", "pop up outlet", "flush outlet", "office floor", "recessed outlet"])
def _(S):
    lid = [(6, 11), (8.2, 9.4), (4.2, 3.9), (2, 5.5)]
    return [
        line(seg(2, 12, 6, 12)), line(seg(18, 12, 22, 12)),
        line(poly([(6, 12), (6, 20.5), (18, 20.5), (18, 12)], r=S.r)),
        shell(poly(lid, closed=True, r=S.r * 0.5)),
        *_slots(10, 14, 14.5, 3),
    ]


def _cord(S):
    return line(seg(12, 17, 12, 22))


@icon("plug-type-a", CAT, "Type A plug face with two flat parallel blades",
      tags=["us plug", "nema 1-15", "american plug", "two prong", "japan plug", "plug type"])
def _(S):
    return [
        shell(rect(5, 3, 14, 14, rr(S))),
        sq(8.5, 6.5, 2, 7, 0), sq(13.5, 6.5, 2, 7, 0),
        _cord(S),
    ]


@icon("plug-type-c", CAT, "Type C Europlug face with two round pins",
      tags=["europlug", "european plug", "eu plug", "two pin", "round pins", "plug type"])
def _(S):
    face = ellipse(12, 10, 8.5, 6) if S.name == "rounded" else poly([(3.5, 10), (7, 4), (17, 4), (20.5, 10), (17, 16), (7, 16)], closed=True)
    return [
        shell(face),
        dot(8.5, 10, 1.6), dot(15.5, 10, 1.6),
        line(seg(12, 16, 12, 22)),
    ]


@icon("plug-type-g", CAT, "Type G plug face with three rectangular pins",
      tags=["uk plug", "british plug", "bs 1363", "three pin", "13 amp", "plug type"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 14.5, rr(S))),
        sq(11, 5.5, 2, 4.5, 0),
        sq(6.5, 12, 4, 2, 0), sq(13.5, 12, 4, 2, 0),
        _cord(S),
    ]


def _blade(x1, y1, x2, y2, w=2.0):
    a = math.atan2(y2 - y1, x2 - x1)
    nx, ny = -math.sin(a) * w / 2, math.cos(a) * w / 2
    return poly([(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)], closed=True)


def _type_i(cy):
    return [knock(_blade(10.2, cy - 3.5, 7.8, cy)), knock(_blade(13.8, cy - 3.5, 16.2, cy)),
            knock(_blade(12, cy + 1.75, 12, cy + 5.25))]


@icon("plug-type-i", CAT, "Type I plug face with two angled blades and a vertical earth blade",
      tags=["australian plug", "chinese plug", "as 3112", "angled pins", "three pin", "plug type"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 14.5, rr(S))),
        *_type_i(9),
        _cord(S),
    ]


@icon("socket-type-a", CAT, "Type A duplex wall outlet with two pairs of flat slots",
      tags=["us outlet", "american socket", "duplex outlet", "two prong outlet", "receptacle", "socket type"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S))),
        *_slots(9.5, 14.5, 5, 4),
        dot(12, 12, 1),
        *_slots(9.5, 14.5, 15, 4),
    ]


@icon("socket-type-f", CAT, "Type F Schuko socket: a round recess with two pin holes and earth clips",
      tags=["schuko", "german socket", "european socket", "eu outlet", "earth clips", "socket type"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S))),
        detail(circle(12, 12, 6)),
        dot(9, 12, 1.25), dot(15, 12, 1.25),
        sq(10.75, 7, 2.5, 1.75, 0), sq(10.75, 15.25, 2.5, 1.75, 0),
    ]


@icon("socket-type-g", CAT, "Type G switched socket with three rectangular holes and a rocker switch",
      tags=["uk socket", "british socket", "13 amp socket", "switched socket", "three pin socket", "socket type"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, rr(S))),
        sq(8, 6.5, 2, 4.5, 0),
        sq(4.75, 14, 3.5, 2, 0), sq(9.75, 14, 3.5, 2, 0),
        sq(16, 7.5, 2.75, 9, L(S, 0, 1.25)),
    ]


@icon("socket-type-i", CAT, "Type I wall socket with two angled slots and a vertical slot below",
      tags=["australian socket", "chinese socket", "angled outlet", "power point", "three pin socket", "socket type"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S))),
        *_type_i(11),
    ]


# ============================================================================ switches and small fittings

@icon("dimmer-switch", CAT, "Wall dimmer switch: a square plate with a round rotary knob",
      tags=["dimmer", "light dimmer", "rotary switch", "brightness", "light control", "wall switch"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S))),
        detail(circle(12, 12, 4.5)),
        dot(12, 9.75, 1) if S.name == "rounded" else sq(11, 8.75, 2, 2),
    ]


@icon("double-light-switch", CAT, "Wall plate with two rocker light switches side by side",
      tags=["two gang switch", "double switch", "light switch", "wall switch", "rocker", "lighting"],
      aliases=["two-gang-switch"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S))),
        detail(rect(6.5, 6.5, 4, 11, L(S, 0, 1))), detail(rect(13.5, 6.5, 4, 11, L(S, 0, 1))),
        sq(7.5, 7.5, 2, 4.5), sq(14.5, 12, 2, 4.5),
    ]


@icon("pull-cord-switch", CAT, "Ceiling pull cord switch with a hanging cord and bead",
      tags=["pull switch", "cord switch", "bathroom switch", "ceiling switch", "light pull", "string switch"])
def _(S):
    return [
        line(seg(3, 3, 21, 3) if S.name == "line" else seg(4, 3, 20, 3)),
        shell(rect(7, 4, 10, 6.5, rr(S, 2))),
        line(seg(12, 10.5, 12, 16.5)),
        shell(rect(10.25, 16.5, 3.5, 5, L(S, 0.5, 1.75))),
    ]


@icon("bulb-socket", CAT, "Threaded lamp holder hanging from its flex cord, with a skirt ring at the opening",
      tags=["lamp holder", "bulb holder", "light socket", "e27", "lampholder", "pendant fitting"],
      aliases=["lamp-holder"])
def _(S):
    body = union(poly([(9.5, 5), (14.5, 5), (16, 8.5), (8, 8.5)], closed=True), rect(8, 8, 8, 10, 0),
                 rect(6, 17, 12, 4.5, rr(S, 1.5)))
    return [
        line(seg(12, 2, 12, 5)),
        shell(body),
        detail(seg(8, 11.5, 16, 11.5)), detail(seg(8, 14.5, 16, 14.5)),
    ]


@icon("doorbell-chime", CAT, "Wall doorbell chime box with two tone bars and a music note",
      tags=["chime", "door chime", "bell", "ding dong", "doorbell receiver", "ringer"])
def _(S):
    return [
        shell(rect(2.5, 5, 11.5, 14, rr(S, 3))),
        detail(seg(6.5, 8, 6.5, 16)), detail(seg(10, 8, 10, 16)),
        dot(18.25, 17.25, 2),
        line(poly([(20, 17.5), (20, 5), (22, 7)], r=S.r * 0.5)),
    ]


def _handset(cx, cy):
    arc_d = f"M{fmt(cx - 3.2)} {fmt(cy + 0.6)}A4 4 0 0 1 {fmt(cx + 3.2)} {fmt(cy + 0.6)}"
    left = rot_d(rect(cx - 5.9, cy - 0.1, 4, 2.4, 1.1), -25, cx - 3.9, cy + 1.1)
    right = rot_d(rect(cx + 1.9, cy - 0.1, 4, 2.4, 1.1), 25, cx + 3.9, cy + 1.1)
    return path_to_d(U(ST(arc_d, 1.6, "butt", "miter"), P(left), P(right)))


@icon("telephone-socket", CAT, "Telephone wall socket plate with a small phone jack and a handset mark",
      tags=["phone socket", "phone jack", "rj11", "landline", "telephone point", "wall jack"],
      aliases=["phone-socket"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, rr(S))),
        knock(_handset(12, 7)),
        detail(rect(9, 13, 6, 5, L(S, 0, 1))),
    ]


@icon("coaxial-connector", CAT, "F-type coaxial connector with a hex nut, a threaded end and a centre pin",
      tags=["coax", "f connector", "tv aerial", "antenna cable", "cable tv", "satellite"],
      aliases=["coax-connector"])
def _(S):
    return [
        line(seg(2, 12, 3.5, 12)),
        shell(rect(3.5, 9, 5, 6, rr(S, 1.5))),
        shell(rect(9, 6, 5.5, 12, rr(S, 1))),
        detail(seg(9, 10, 14.5, 10)), detail(seg(9, 14, 14.5, 14)),
        shell(rect(15, 8.5, 4.5, 7, L(S, 0, 1))),
        line(seg(19.5, 12, 22, 12)),
    ]


@icon("audio-jack", CAT, "3.5 mm audio jack plug with banded tip, grip and cable",
      tags=["headphone jack", "aux cable", "3.5mm", "mini jack", "trs", "audio plug"],
      aliases=["headphone-jack"])
def _(S):
    deg = 45
    tip = rot_d(poly([(10, 12.5), (10, 5), (12, 2.5), (14, 5), (14, 12.5)], closed=True, r=S.r * 0.5), deg)
    return [
        shell(tip),
        detail(rseg(10, 6.5, 14, 6.5, deg)), detail(rseg(10, 9.75, 14, 9.75, deg)),
        shell(rot_d(rect(8.5, 12, 7, 6.5, rr(S, 2)), deg)),
        line(rseg(12, 18.5, 12, 22.5, deg)),
    ]


@icon("rca-connector", CAT, "Pair of RCA phono plugs with round collars and centre pins on cables",
      tags=["phono plug", "rca cable", "composite", "stereo cable", "audio video", "cinch"],
      aliases=["phono-plug"])
def _(S):
    out = []
    for x in (6.5, 17.5):
        out += [
            line(seg(x, 2, x, 5)),
            shell(rect(x - 2.75, 5, 5.5, 5, rr(S, 1.5))),
            shell(rect(x - 2, 10.5, 4, 6, rr(S, 1))),
            line(seg(x, 16.5, x, 22)),
        ]
    return out


@icon("optical-audio-connector", CAT, "Optical digital audio plug with a light dot at its tip",
      tags=["optical cable", "spdif", "digital audio", "fibre optic", "soundbar", "audio cable"])
def _(S):
    return [
        shell(poly([(7, 13), (7, 6), (9, 4), (15, 4), (17, 6), (17, 13)], closed=True, r=S.r * 0.6)),
        dot(12, 8.5, 1.5),
        shell(rect(9.5, 13, 5, 4.5, rr(S, 1))),
        line(seg(12, 17.5, 12, 22)),
    ]


# ============================================================================ bulbs and lamps

@icon("led-bulb", CAT, "LED bulb with a dome, a tapered heat sink neck, a screw base and an LED chip",
      tags=["led", "led lamp", "energy saving", "light bulb", "low energy", "lighting"], aliases=["led-lamp"])
def _(S):
    top = "M5 11A7 7 0 0 1 19 11L15.5 17H8.5Z" if S.name == "line" else "M5 11A7 7 0 0 1 19 11C19 12 16 15.5 15.5 17H8.5C8 15.5 5 12 5 11Z"
    return [
        shell(top),
        detail(seg(5, 11, 19, 11)),
        sq(11, 6.5, 2, 2) if S.name == "line" else dot(12, 7.5, 1.25),
        shell(rect(9.5, 17.5, 5, 4, rr(S, 1.5))),
    ]


@icon("fluorescent-tube", CAT, "Straight fluorescent tube with pin end caps, shining downward",
      tags=["fluorescent", "tube light", "t8", "strip light", "neon tube", "office light"],
      aliases=["tube-light"])
def _(S):
    k = L(S, 0, 1.25)
    body = union(rect(2.5, 7, 3.5, 7, k), rect(5.5, 8, 13, 5, 0), rect(18, 7, 3.5, 7, k))
    return [
        shell(body),
        line(seg(8, 16.5, 7, 20)), line(seg(12, 16.5, 12, 20.5)), line(seg(16, 16.5, 17, 20)),
    ]


@icon("cfl-bulb", CAT, "Compact fluorescent bulb with a spiral tube, a neck and a screw base",
      tags=["cfl", "energy saving bulb", "compact fluorescent", "spiral bulb", "low energy", "light bulb"])
def _(S):
    return [
        line("M9 14.5V13.5A1.5 1.5 0 0 1 10.5 12H15.5A2 2 0 0 0 15.5 8H8.5A2 2 0 0 1 8.5 4H14"),
        shell(poly([(6.5, 14.5), (17.5, 14.5), (15.5, 17.5), (8.5, 17.5)], closed=True, r=S.r * 0.5)),
        shell(rect(9.5, 18, 5, 3.5, rr(S, 1.5))),
    ]


@icon("halogen-bulb", CAT, "Small halogen capsule bulb with a filament and two wire pins",
      tags=["halogen", "g9", "g4", "capsule bulb", "pin bulb", "lamp"], aliases=["capsule-bulb"])
def _(S):
    return [
        shell(rect(6.5, 2.5, 11, 13.5, L(S, 3, 5.5))),
        detail(poly([(10, 13.5), (10, 9), (11, 7), (12, 9), (13, 7), (14, 9), (14, 13.5)], r=S.r * 0.2)),
        line(seg(10, 16, 10, 21.5)), line(seg(14, 16, 14, 21.5)),
    ]


@icon("edison-bulb", CAT, "Vintage Edison bulb with a looping filament and a screw base",
      tags=["filament bulb", "vintage bulb", "retro bulb", "squirrel cage", "antique", "light bulb"],
      aliases=["filament-bulb"])
def _(S):
    body = ("M9.5 21.5V16C6.8 14.6 5.5 12 5.5 9A6.5 6.5 0 0 1 18.5 9C18.5 12 17.2 14.6 14.5 16V21.5Z" if S.name == "line" else
            "M11 21.5A1.5 1.5 0 0 1 9.5 20V16C6.8 14.6 5.5 12 5.5 9A6.5 6.5 0 0 1 18.5 9C18.5 12 17.2 14.6 14.5 16V20A1.5 1.5 0 0 1 13 21.5Z")
    return [
        shell(body),
        detail(seg(9.5, 17.75, 14.5, 17.75)),
        detail(poly([(10, 15), (10, 11), (8.5, 7), (12, 10), (15.5, 7), (14, 11), (14, 15)], r=S.r * 0.3)),
    ]


@icon("spotlight-bulb", CAT, "Reflector spotlight bulb: a cone with a round lens face and two pins",
      tags=["gu10", "mr16", "reflector bulb", "spot bulb", "downlight bulb", "halogen spot"],
      aliases=["reflector-bulb"])
def _(S):
    cone = ("M3.5 5.5A8.5 2.75 0 0 1 20.5 5.5L14.5 14.5V17H9.5V14.5Z" if S.name == "line" else
            "M3.5 5.5A8.5 2.75 0 0 1 20.5 5.5C20.5 8 14.5 12 14.5 14.5V17H9.5V14.5C9.5 12 3.5 8 3.5 5.5Z")
    return [
        shell(cone),
        detail("M3.5 5.5A8.5 2.75 0 0 0 20.5 5.5"),
        line(seg(10.5, 17, 10.5, 21.5)), line(seg(13.5, 17, 13.5, 21.5)),
    ]


@icon("led-strip", CAT, "Flexible LED strip ribbon with evenly spaced light chips",
      tags=["led tape", "strip light", "light strip", "rgb strip", "under cabinet", "ribbon light"],
      aliases=["led-tape"])
def _(S):
    c = "M4 18C10 18 14 6 20 6"
    band = path_to_d(ST(c, 6, S.cap, S.join))
    pts = [(5.5, 18), (8.9, 16.5), (12, 12), (15.1, 7.5), (18.5, 6)]
    return [shell(band), *[sq(x - 1, y - 1, 2, 2, L(S, 0, 0.6)) for x, y in pts]]


@icon("recessed-light", CAT, "Recessed ceiling downlight with a flush trim ring and a cone of light",
      tags=["downlight", "can light", "pot light", "ceiling spotlight", "recessed lighting", "spot"],
      aliases=["downlight", "pot-light"])
def _(S):
    return [
        line(seg(2, 5.5, 5, 5.5)), line(seg(19, 5.5, 22, 5.5)),
        shell(ellipse(12, 6.5, 7, 3) if S.name == "rounded" else poly([(5, 5.5), (19, 5.5), (16.5, 9.5), (7.5, 9.5)], closed=True)),
        line(seg(7, 12.5, 4.5, 20.5)), line(seg(12, 13, 12, 21)), line(seg(17, 12.5, 19.5, 20.5)),
    ]


def _head(cx, cy, w, h, deg, S):
    """Small cylindrical lamp head (w x h) centred on (cx, cy), turned clockwise by deg."""
    return rot_d(rect(cx - w / 2, cy - h / 2, w, h, rr(S, 1.25)), deg, cx, cy)


@icon("track-light", CAT, "Ceiling track rail with three spot heads angled downward",
      tags=["track lighting", "spotlights", "rail lights", "ceiling spots", "gallery lighting", "spot"])
def _(S):
    heads = [(5, 11.5, 25), (12, 12, 0), (19, 11.5, -25)]
    out = [line(seg(2, 4, 22, 4) if S.name == "line" else seg(2.5, 4, 21.5, 4))]
    for cx, cy, deg in heads:
        top = rot_pts([(cx, cy - 3.25)], deg, cx, cy)[0]
        out.append(line(seg(top[0], 4, top[0], top[1])))
        out.append(shell(_head(cx, cy, 4, 6.5, deg, S)))
    return out


@icon("wall-sconce", CAT, "Wall sconce: a backplate with a curved arm holding an upturned shade",
      tags=["wall light", "sconce", "wall lamp", "uplighter", "hallway light", "lighting"],
      aliases=["wall-light"])
def _(S):
    return [
        shell(rect(2.5, 9, 3.5, 11.5, rr(S, 1.5))),
        line("M6 17C11 17 14.5 16.5 14.5 12.5"),
        shell(poly([(9, 7.5), (20, 7.5), (17.5, 12.5), (11.5, 12.5)], closed=True, r=S.r * 0.6)),
        line(seg(11, 4.75, 10.25, 2.5)), line(seg(14.5, 4.75, 14.5, 2.25)), line(seg(18, 4.75, 18.75, 2.5)),
    ]


@icon("floodlight", CAT, "Outdoor floodlight with a flat lens in a U bracket, shining downward",
      tags=["flood light", "security light", "outdoor light", "led floodlight", "yard light", "spotlight"],
      aliases=["flood-light"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 9.5, rr(S, 2.5))),
        detail(rect(8, 5, 8, 4.5, L(S, 0, 1))),
        line(poly([(3, 6.5), (3, 14), (21, 14), (21, 6.5)], r=S.r)),
        line(seg(7.5, 17, 6, 21)), line(seg(12, 17, 12, 21.5)), line(seg(16.5, 17, 18, 21)),
    ]


def _crescent(cx, cy, r):
    return path_to_d(D(P(circle(cx, cy, r)), P(circle(cx + r * 0.55, cy - r * 0.4, r * 0.85))))


@icon("night-light", CAT, "Plug-in night light with a glowing crescent moon lens",
      tags=["nightlight", "plug in light", "nursery light", "kids room", "sleep", "dark"],
      aliases=["nightlight"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 19, L(S, 3, 6.5))),
        knock(_crescent(11.5, 12.5, 4.25)),
    ]


@icon("string-lights", CAT, "String of small bulbs hanging from a sagging wire",
      tags=["fairy lights", "festoon lights", "party lights", "christmas lights", "garden lights", "decoration"],
      aliases=["fairy-lights"])
def _(S):
    def y_at(x):
        t = (x - 2) / 20
        return (1 - t) ** 2 * 4 + 2 * t * (1 - t) * 12 + t * t * 4
    out = [line("M2 4Q12 12 22 4" if S.name == "line" else "M2.5 4.4Q12 12 21.5 4.4")]
    for x in (5, 12, 19):
        y = y_at(x)
        out.append(line(seg(x, y, x, y + 2.5)))
        out.append(shell(drop(x, y + 3, 2, y + 8)))
    return out


@icon("lava-lamp", CAT, "Lava lamp: a tapered glass bottle with floating blobs on a cone base",
      tags=["lava lamp", "retro lamp", "mood light", "motion lamp", "groovy", "decor"])
def _(S):
    pts = [(10.5, 2.5), (13.5, 2.5), (14.5, 5.5), (17, 13.5), (14.5, 17), (17, 21.5), (7, 21.5), (9.5, 17), (7, 13.5), (9.5, 5.5)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.5)),
        detail(seg(9.5, 5.5, 14.5, 5.5)), detail(seg(9.5, 17, 14.5, 17)),
        dot(11.25, 9.5, 1.1), dot(13, 13, 1.5),
    ]


@icon("ring-light", CAT, "Ring light on a tripod stand with a phone held in the centre",
      tags=["ring lamp", "selfie light", "vlogging", "streaming", "makeup light", "content creator"],
      aliases=["selfie-light"])
def _(S):
    ring = path_to_d(D(P(circle(12, 9, 7)), P(circle(12, 9, 4))))
    return [
        shell(ring),
        sq(10.75, 7, 2.5, 4, L(S, 0, 0.75)),
        line(seg(12, 16, 12, 19)),
        line(poly([(8, 21.5), (12, 18.5), (16, 21.5)], r=S.r)),
    ]


@icon("emergency-light", CAT, "Emergency light box with twin angled lamps on top and an indicator light",
      tags=["emergency lighting", "twin spot", "power failure", "exit light", "backup light", "safety"])
def _(S):
    return [
        shell(_head(7.5, 7, 4.5, 6, -35, S)), shell(_head(16.5, 7, 4.5, 6, 35, S)),
        shell(rect(3.5, 11.5, 17, 9.5, rr(S))),
        dot(12, 16.25, 1.5),
    ]


@icon("salt-lamp", CAT, "Himalayan salt lamp: a rough crystal rock on a small wooden base",
      tags=["himalayan salt lamp", "salt rock", "crystal lamp", "mood light", "wellness", "decor"])
def _(S):
    rock = [(8, 17.5), (5.5, 12.5), (7, 7.5), (10, 3.5), (13.5, 4.5), (17.5, 8), (18.5, 13), (16, 17.5)]
    return [
        shell(poly(rock, closed=True, r=S.r * 0.6)),
        detail(poly([(10, 8), (12.5, 11.5), (11.5, 15)])),
        shell(rect(5.5, 17.5, 13, 4, rr(S, 1.5))),
    ]


@icon("heat-lamp", CAT, "Infrared heat lamp bulb with a wide domed face and heat waves below",
      tags=["infrared lamp", "heat bulb", "brooder lamp", "reptile lamp", "warming", "red light"],
      aliases=["infrared-lamp"])
def _(S):
    return [
        shell(rect(10, 2.5, 4, 3.5, rr(S, 1))),
        shell("M9.5 6H14.5L19.5 11A7.5 3 0 0 1 4.5 11Z" if S.name == "line" else
              "M10 6H14C15.5 6 19.5 9 19.5 11A7.5 3 0 0 1 4.5 11C4.5 9 8.5 6 10 6Z"),
        *[line(f"M{x} 16.5C{x - 1.2} 17.6 {x + 1.2} 19.4 {x} 20.5") for x in (8, 12, 16)],
    ]


@icon("bug-zapper", CAT, "Hanging bug zapper lantern with a hook, a caged grid and a base",
      tags=["insect killer", "mosquito killer", "fly zapper", "uv trap", "pest control", "electric trap"],
      aliases=["insect-zapper"])
def _(S):
    return [
        line("M12 5.5V4A1.5 1.5 0 1 1 13.5 2.5"),
        shell(poly([(8, 5.5), (16, 5.5), (18, 8), (6, 8)], closed=True, r=S.r * 0.5)),
        shell(rect(6, 8, 12, 10.5, L(S, 0, 1))),
        detail(seg(10, 8, 10, 18.5)), detail(seg(14, 8, 14, 18.5)),
        shell(poly([(6, 18.5), (18, 18.5), (16, 21), (8, 21)], closed=True, r=S.r * 0.5)),
    ]


@icon("grow-light", CAT, "Grow light panel shining on a seedling in a pot",
      tags=["plant light", "grow lamp", "indoor garden", "hydroponics", "seedling", "horticulture"],
      aliases=["plant-light"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 4, rr(S, 1.5))),
        line(seg(6, 9.5, 5, 12)), line(seg(18, 9.5, 19, 12)),
        shell("M12 15C12 12.5 10 10.75 7.5 10.75C7.5 13.25 9.5 15 12 15Z"),
        shell("M12 13.5C12 11 14 9.25 16.5 9.25C16.5 11.75 14.5 13.5 12 13.5Z"),
        line(seg(12, 13.5, 12, 17)),
        shell(poly([(7.5, 17), (16.5, 17), (15, 21.5), (9, 21.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("solar-garden-light", CAT, "Solar garden stake light with a small solar panel cap and a lit globe",
      tags=["solar light", "garden light", "path light", "stake light", "outdoor light", "lawn light"],
      aliases=["solar-path-light"])
def _(S):
    return [
        shell(poly([(6.5, 6), (17.5, 6), (16, 3), (8, 3)], closed=True, r=S.r * 0.5)),
        shell(rect(9, 7, 6, 6, rr(S, 3))),
        line(seg(12, 13, 12, 21.5)),
        line(seg(5.5, 10, 3.5, 10)), line(seg(18.5, 10, 20.5, 10)),
        line(seg(5, 18, 19, 18)),
    ]


@icon("porch-light", CAT, "Outdoor wall lantern with glass panes and a peaked cap on a wall bracket",
      tags=["outdoor wall light", "porch lamp", "wall lantern", "coach light", "front door light", "exterior light"],
      aliases=["wall-lantern"])
def _(S):
    return [
        shell(poly([(4, 7), (10, 3), (16, 7)], closed=True, r=S.r * 0.6)),
        shell(rect(5.5, 8, 9, 10, rr(S, 1.5))),
        detail(seg(10, 8, 10, 18)),
        line(seg(10, 18, 10, 21)),
        line(seg(14.5, 11, 18.5, 11)),
        shell(rect(18.5, 6.5, 3, 10, rr(S, 1))),
    ]


@icon("arc-floor-lamp", CAT, "Arc floor lamp with a weighted base and a long curved arm to a hanging dome shade",
      tags=["arc lamp", "arched lamp", "floor lamp", "overhead lamp", "living room", "reading light"],
      aliases=["arc-lamp"])
def _(S):
    return [
        shell(rect(3, 18.5, 7, 3, rr(S, 1.5))),
        line("M6.5 18.5V9A6 6 0 0 1 12.5 3H14A4 4 0 0 1 18 7V9.5"),
        shell("M14 13.5A4 4 0 0 1 22 13.5Z" if S.name == "rounded" else "M14 13.5L15.5 9.5H20.5L22 13.5Z"),
    ]


@icon("led-candle", CAT, "Flameless LED pillar candle with a flame-shaped bulb and a switch",
      tags=["flameless candle", "battery candle", "electric candle", "fake candle", "tea light", "decor"],
      aliases=["flameless-candle"])
def _(S):
    fl = drop(12, 2.5, 2.25, 7.5) if S.name == "rounded" else "M12 2.5L14.25 7.5A2.25 2.25 0 0 1 9.75 7.5Z"
    return [
        shell(fl, stroke_miterlimit="2"),
        shell(rect(6.5, 11.5, 11, 10, rr(S, 2.5))),
        sq(10.5, 16.5, 3, 2, L(S, 0, 0.75)),
    ]


@icon("vanity-mirror", CAT, "Rectangular vanity mirror framed by a row of round bulbs",
      tags=["makeup mirror", "hollywood mirror", "dressing table", "lighted mirror", "bulb mirror", "beauty"],
      aliases=["hollywood-mirror"])
def _(S):
    pts = [(6, y) for y in (6, 10, 14, 18)] + [(18, y) for y in (6, 10, 14, 18)] + [(10, 6), (14, 6)]
    return [
        shell(rect(3, 2.5, 18, 19, rr(S))),
        *[dot(x, y, 1.2) for x, y in pts],
        detail(seg(10, 16, 14, 12)),
    ]


@icon("automatic-soap-dispenser", CAT, "Touch-free soap dispenser with a spout, a sensor and a drop of soap",
      tags=["soap dispenser", "touchless", "sensor", "hand wash", "hygiene", "sanitizer"],
      aliases=["touchless-soap-dispenser"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 10, 19, rr(S, 3))),
        detail(seg(3.5, 7, 13.5, 7)),
        line(poly([(13.5, 10), (18.5, 10), (18.5, 11.5)], r=S.r * 0.5)),
        dot(8.5, 14.5, 1.25),
        shell(drop(18.5, 14, 1.9, 18.25)),
    ]
