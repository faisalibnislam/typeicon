"""TypeIcon Core: energy & environment."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "energy"


def knock(d) -> Part:
    """Small solid shape: solid in Line/Rounded, knocked out of a Filled shell (like a dot)."""
    return Part("dot", d)


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def bolt(cx, cy, s=1.0):
    """Lightning-bolt polygon centred near (cx, cy), about 5 x 7.5 px at s = 1."""
    pts = [(0.5, -3.75), (-2.5, 0.5), (0, 0.5), (-0.75, 3.75), (2.5, -0.75), (0, -0.75)]
    return poly([(cx + x * s, cy + y * s) for x, y in pts], closed=True)


def drop_d(cx, top, bottom_r, cy):
    """Water drop: pointed tip at (cx, top), round bottom of radius bottom_r centred at (cx, cy)."""
    r = bottom_r
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + r * 0.35)} {fmt(top + (cy - top) * 0.35)} {fmt(cx + r)} {fmt(cy - r * 0.55)} "
            f"{fmt(cx + r)} {fmt(cy)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx - r)} {fmt(cy)}"
            f"C{fmt(cx - r)} {fmt(cy - r * 0.55)} {fmt(cx - r * 0.35)} {fmt(top + (cy - top) * 0.35)} {fmt(cx)} {fmt(top)}Z")


def leaf_d(x1, y1, x2, y2, bulge):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    L = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / L, (x2 - x1) / L
    b = bulge * 2
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx * b)} {fmt(my + ny * b)} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(mx - nx * b)} {fmt(my - ny * b)} {fmt(x1)} {fmt(y1)}Z")


# ============================================================================ batteries
# Same body as the v0.1 battery (devices): 17 x 10 at (2, 7), terminal at x 21.5.
# Filled follows the v0.1 battery: the charged part is solid, the empty part is knocked out.

def _battery_parts(S, level_w):
    parts = [shell(rect(2, 7, 17, 10, S.R * 0.5)), line(seg(21.5, 10.5, 21.5, 13.5))]
    if level_w:
        parts.append(solid(rect(5, 10, level_w, 4, 0.5)))
    return parts


def _battery_filled(level_w):
    def f():
        body = P(rect(1, 6, 19, 12, 2))
        x0 = 5 + level_w + 1.5 if level_w else 3.5
        if x0 < 17.5:
            body = D(body, P(rect(x0, 8.5, 17.5 - x0, 7, 0.5)))
        return U(body, P(rect(20.5, 9.5, 2.5, 5, 1)))
    return f


@icon("battery-full", CAT, "Fully charged battery",
      tags=["battery", "charged", "full", "power", "energy", "100%"], filled=_battery_filled(11))
def _(S):
    return _battery_parts(S, 11)


@icon("battery-low", CAT, "Battery with a low charge",
      tags=["battery", "low", "drained", "power", "energy", "warning"], filled=_battery_filled(3))
def _(S):
    return _battery_parts(S, 3)


@icon("battery-empty", CAT, "Empty battery with no charge",
      tags=["battery", "empty", "dead", "flat", "no power", "0%"], filled=_battery_filled(0))
def _(S):
    return _battery_parts(S, 0)


# ============================================================================ generation

@icon("solar-panel", CAT, "Solar panel with a cell grid on a stand",
      tags=["solar", "photovoltaic", "pv", "renewable", "sun", "clean energy"], aliases=["photovoltaic"])
def _(S):
    panel = [(6, 3.5), (18, 3.5), (21, 15), (3, 15)]
    return [
        shell(poly(panel, closed=True, r=S.r * 0.5)),
        detail(seg(12, 3.5, 12, 15)),
        detail(seg(4.3, 9.25, 19.7, 9.25)),
        line(seg(12, 15, 12, 20.5)),
        line(seg(7, 20.5, 17, 20.5) if S.name == "line" else seg(8, 20.5, 16, 20.5)),
    ]


@icon("wind-turbine", CAT, "Wind turbine with three blades on a tower",
      tags=["wind", "turbine", "windmill", "renewable", "wind power", "clean energy"], aliases=["wind-power"])
def _(S):
    hub = (12, 9.5)
    up, down = (7, 8) if S.name == "line" else (6, 7.5)  # round caps add 1 px
    blades = [line(seg(*polar(*hub, 3, a), *polar(*hub, up if a < 0 else down, a))) for a in (-90, 30, 150)]
    return [
        *blades,
        shell(circle(*hub, 1.5)),
        line(seg(12, 12.5, 12, 21)),
        line(seg(7.5, 21, 16.5, 21) if S.name == "line" else seg(8.5, 21, 15.5, 21)),
    ]


@icon("hydro-power", CAT, "Water drop with a lightning bolt; hydroelectric power",
      tags=["hydro", "hydroelectric", "water power", "dam", "renewable", "clean energy"], aliases=["hydroelectric"])
def _(S):
    tip = 2.5 if S.name == "line" else 3
    return [shell(drop_d(12, tip, 7, 14), stroke_miterlimit="2"), knock(bolt(12, 14.5, 1.1))]


@icon("nuclear", CAT, "Radiation trefoil; nuclear power",
      tags=["radiation", "radioactive", "atomic", "nuclear power", "hazard", "reactor"], aliases=["radiation", "radioactive"])
def _(S):
    parts = [dot(12, 12, 1.75)]
    for a in (-90, 30, 150):
        pts = [polar(12, 12, 3.75, a - 30 + 60 * i / 8) for i in range(9)]
        pts += [polar(12, 12, 8.5, a + 30 - 60 * i / 12) for i in range(13)]
        parts.append(shell(poly(pts, closed=True, r=S.r * 0.66)))
    return parts


@icon("power-plant", CAT, "Cooling tower with steam and a lightning bolt",
      tags=["power station", "cooling tower", "plant", "electricity", "energy", "industry"], aliases=["power-station"])
def _(S):
    tower = "M4.5 21C6.5 17.5 7 14 6 10H18C17 14 17.5 17.5 19.5 21Z"
    if S.name == "rounded":
        tower = "M6.3 21C5.5 21 5 20.6 5.3 20C6.8 17 7.2 13.8 6.3 11.2C6.1 10.5 6.4 10 7.1 10H16.9C17.6 10 17.9 10.5 17.7 11.2C16.8 13.8 17.2 17 18.7 20C19 20.6 18.5 21 17.7 21Z"
    return [
        shell(tower),
        knock(bolt(12, 15.5, 1.0)),
        line("M7.5 6A2.25 2.25 0 0 1 12 5A2.25 2.25 0 0 1 16.5 6"),
    ]


# ============================================================================ fuels

@icon("oil-drop", CAT, "Drop of oil with a glossy highlight",
      tags=["oil", "petroleum", "fuel", "crude", "fossil fuel", "lubricant"], aliases=["oil"])
def _(S):
    tip = 2.5 if S.name == "line" else 3
    return [shell(drop_d(12, tip, 7, 14), stroke_miterlimit="2"), detail(arc(12, 14, 3.75, 95, 165))]


@icon("gas-flame", CAT, "Gas flame with an inner flame",
      tags=["gas", "natural gas", "flame", "fire", "burner", "heating"], aliases=["natural-gas"])
def _(S):
    tip = 2.5 if S.name == "line" else 3
    outer = (f"M12 {tip}C13 6 17.5 8.5 18 13.5C18.4 17.6 15.6 21 12 21C8.7 21 6 18.3 6 15C6 12.7 6.8 10.8 8.3 9.3"
             f"C8.6 10.6 9.3 11.6 10.3 12.2C10 8.8 10.5 5.5 12 {tip}Z")
    inner = "M12 12.5C13.2 14 14.5 15.2 14.5 17A2.5 2.5 0 0 1 9.5 17C9.5 15.2 10.8 14 12 12.5Z"
    return [shell(outer, stroke_miterlimit="2"), knock(inner)]


# ============================================================================ electricity

@icon("energy-plug", CAT, "Electric plug with a lightning bolt and a curling cord",
      tags=["electricity", "power", "plug", "electric", "energy", "mains"], aliases=["electric-plug"])
def _(S):
    head = [(6, 7.5), (18, 7.5), (18, 10.5), (15, 15.5), (9, 15.5), (6, 10.5)]
    return [
        line(seg(9.5, 2.5, 9.5, 7.5)), line(seg(14.5, 2.5, 14.5, 7.5)),
        shell(poly(head, closed=True, r=S.r)),
        knock(bolt(12, 11.25, 0.85)),
        line("M12 15.5V17A3.5 3.5 0 0 1 8.5 20.5H3" if S.name == "line" else "M12 15.5V17A3.5 3.5 0 0 1 8.5 20.5H4"),
    ]


@icon("charging-station", CAT, "Electric-vehicle charging station with a cable and nozzle",
      tags=["ev charger", "electric car", "charging", "ev", "station", "charge point"], aliases=["ev-charger", "ev-charging"])
def _(S):
    return [
        shell(rect(3, 3, 10, 18, rr(S, 3))),
        knock(bolt(8, 12, 1.1)),
        line(poly([(13, 7), (17, 7), (19, 9), (19, 14)], r=S.r)),
        solid(rect(17, 14, 4, 4.5, 1)),
    ]


@icon("electricity-meter", CAT, "Electricity meter with a display and a bolt",
      tags=["meter", "electric meter", "utility", "kwh", "consumption", "smart meter"], aliases=["power-meter"])
def _(S):
    return [
        shell(rect(4, 3, 16, 18, rr(S))),
        detail(rect(7, 6, 10, 5, rr(S, 1.5) * 0.5)),
        knock(bolt(12, 16, 0.85)),
    ]


@icon("power-grid", CAT, "Electricity transmission tower (pylon)",
      tags=["pylon", "transmission", "power line", "grid", "electricity", "tower"], aliases=["pylon", "transmission-tower"])
def _(S):
    return [
        line(poly([(6, 21), (10, 6), (12, 3), (14, 6), (18, 21)], r=S.r), stroke_miterlimit="1.5"),
        line(seg(4, 7, 20, 7)),
        line(seg(6, 12, 18, 12)),
        line(poly([(8.7, 12), (15.2, 17.5)], r=0)),
        line(poly([(15.3, 12), (8.8, 17.5)], r=0)),
    ]


@icon("thermostat", CAT, "Wall thermostat: a temperature dial with a thermometer",
      tags=["temperature", "heating", "climate", "hvac", "smart home", "thermostat"], aliases=["temperature-control"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S))),
        detail(circle(12, 12, 5.5)),
        detail(seg(12, 9.5, 12, 12.5)),
        dot(12, 14, 1.6),
    ]


# ============================================================================ environment

@icon("leaf-eco", CAT, "Leaf with a stem and a vein; eco-friendly",
      tags=["eco", "green", "leaf", "sustainable", "environment", "nature"], aliases=["eco", "eco-friendly"])
def _(S):
    if S.name == "line":
        d = "M5.5 18.5C5.5 9.5 10 4 20 4C20 14 14.5 18.5 5.5 18.5Z"
    else:
        d = "M6.5 18.5C5.9 18.5 5.5 18.1 5.5 17.5C5.5 9.5 10 4 19 4C19.6 4 20 4.4 20 5C20 14 14.5 18.5 6.5 18.5Z"
    return [shell(d), detail(seg(5.5, 18.5, 14, 10)), line(seg(3, 21, 5.5, 18.5))]


def _arrow_side(a, b, S):
    """Recycling arrow along a triangle side from vertex a to vertex b (gap at both corners)."""
    ax, ay = a
    bx, by = b
    L = math.hypot(bx - ax, by - ay)
    ux, uy = (bx - ax) / L, (by - ay) / L
    nx, ny = -uy, ux
    s0 = (ax + ux * 3, ay + uy * 3)
    s1 = (bx - ux * 6.5, by - uy * 6.5)
    tip = (bx - ux * 3, by - uy * 3)
    base = (bx - ux * 7, by - uy * 7)
    head = [tip, (base[0] + nx * 2.6, base[1] + ny * 2.6), (base[0] - nx * 2.6, base[1] - ny * 2.6)]
    return [line(seg(*s0, *s1)), solid(poly(head, closed=True))]


@icon("recycle", CAT, "Three bent arrows chasing each other around a triangle; recycling",
      tags=["recycling", "reuse", "eco", "environment", "waste", "green"], aliases=["recycling"])
def _(S):
    v = [(12, 4.5), (20.5, 19.5), (3.5, 19.5)]

    def at(a, b, t):
        return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

    out = []
    for i in range(3):
        p, c, n = v[i - 1], v[i], v[(i + 1) % 3]
        tail, neck, tip = at(p, c, 0.58), at(c, n, 0.26), at(c, n, 0.46)
        L = ((n[0] - c[0]) ** 2 + (n[1] - c[1]) ** 2) ** 0.5
        ux, uy = (n[0] - c[0]) / L, (n[1] - c[1]) / L
        base = at(c, n, 0.25)
        head = [tip, (base[0] - uy * 2.75, base[1] + ux * 2.75), (base[0] + uy * 2.75, base[1] - ux * 2.75)]
        out += [line(poly([tail, c, neck], r=S.r * 1.5), stroke_miterlimit="2"), solid(poly(head, closed=True))]
    return out


@icon("earth-eco", CAT, "Globe with a leaf growing from it; a green planet",
      tags=["earth", "planet", "eco", "green", "environment", "climate", "world"], aliases=["green-earth"])
def _(S):
    if S.name == "line":
        meridian = "M10 7A9.5 9.5 0 0 0 10 21A9.5 9.5 0 0 0 10 7Z"
        leaf = leaf_d(14.95, 9.05, 21, 3, 1.8)
    else:
        meridian = ellipse(10, 14, 3, 7)
        leaf = "M14.95 9.05C14.5 5.5 16.5 3 20.3 3A0.7 0.7 0 0 1 21 3.7C21 7.5 18.5 9.5 14.95 9.05Z"
    return [
        shell(circle(10, 14, 7)),
        detail(meridian, stroke_miterlimit="1.5"),
        detail(seg(3, 14, 17, 14)),
        shell(leaf, stroke_miterlimit="2"),
    ]


@icon("water-saving", CAT, "Tap with a single falling drop; save water",
      tags=["water", "save water", "faucet", "tap", "conservation", "drop"], aliases=["save-water"])
def _(S):
    spout = [(3, 7), (11, 7), (14, 10), (14, 13), (10, 13), (10, 11), (3, 11)]
    return [
        line(seg(7, 7, 7, 4)),
        line(seg(4, 3.5, 10, 3.5) if S.name == "line" else seg(4.5, 3.5, 9.5, 3.5)),
        shell(poly(spout, closed=True, r=S.r)),
        shell(drop_d(12, 15.5 if S.name == "line" else 16, 2.75, 19), stroke_miterlimit="2"),
    ]


@icon("carbon-footprint", CAT, "Footprint with a leaf; carbon footprint",
      tags=["co2", "carbon", "emissions", "footprint", "climate", "sustainability"], aliases=["co2-footprint"])
def _(S):
    sole = "M8 11.5C11 11.5 12 14 11.5 16.5C11 19.5 9.8 21 7.5 21C5.2 21 4 19.5 4 17C4 14 5.2 11.5 8 11.5Z"
    toes = [dot(4.3, 8.8, 1), dot(6.6, 7.3, 1.15), dot(9.4, 7, 1.25), dot(11.8, 8.2, 1)]
    if S.name == "line":
        leaf = leaf_d(15, 9.5, 21, 3.5, 1.8)
    else:
        leaf = "M15 9.5C14.55 5.95 16.55 3.45 20.35 3.45A0.7 0.7 0 0 1 21.05 4.15C21.05 7.95 18.55 9.95 15 9.5Z"
    return [shell(sole), *toes, shell(leaf, stroke_miterlimit="2")]