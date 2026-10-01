"""TypeIcon Core: industry and machinery (batch 001)."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, pt_on, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "industry"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rotd(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rotp(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def flame(cx, top, w, h):
    """Small teardrop flame path (closed), tip up."""
    b = top + h
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + w * 0.2)} {fmt(top + h * 0.4)} {fmt(cx + w / 2)} {fmt(top + h * 0.5)} "
            f"{fmt(cx + w / 2)} {fmt(b - w / 2)}A{fmt(w / 2)} {fmt(w / 2)} 0 0 1 {fmt(cx - w / 2)} {fmt(b - w / 2)}"
            f"C{fmt(cx - w / 2)} {fmt(top + h * 0.5)} {fmt(cx - w * 0.2)} {fmt(top + h * 0.4)} {fmt(cx)} {fmt(top)}Z")


def drop(cx, top, w, h):
    return flame(cx, top, w, h)


# ============================================================================ plants and vessels

@icon("industrial-storage-tank", CAT, "Squat storage tank with a domed roof and a side ladder",
      tags=["storage tank", "silo", "oil tank", "fuel storage", "industrial", "tank farm"])
def _(S):
    return [
        shell(f"M3 21V10Q8 5.5 13 10V21Z"),
        detail("M3 15.5H13"),
        line("M17.5 6V21M21 6V21"),
        line("M17.5 10H21M17.5 14H21M17.5 18H21"),
    ]


@icon("water-tower", CAT, "Elevated water tank with a cone roof on braced legs",
      tags=["water storage", "elevated tank", "municipal water", "utility", "tower", "supply"])
def _(S):
    return [
        shell(poly([(6, 11), (6, 6.5), (12, 2.5), (18, 6.5), (18, 11)], closed=True, r=S.r)),
        line("M8 11L5.5 21M16 11L18.5 21"),
        line("M7 15L17.5 19.5M17 15L6.5 19.5"),
    ]


@icon("gas-holder", CAT, "Gasometer drum rising inside a tall open frame of columns and rings",
      tags=["gasometer", "gas storage", "gasworks", "frame", "utility", "industrial"])
def _(S):
    return [
        line("M3.5 3V21M20.5 3V21"),
        line("M3.5 3H20.5M3.5 7.5H20.5"),
        shell("M7.5 21V13Q12 10 16.5 13V21Z"),
        detail("M7.5 17H16.5"),
    ]


@icon("oil-refinery", CAT, "Three distillation columns of different heights joined by pipes, with a flame",
      tags=["refinery", "petrochemical", "distillation", "oil plant", "crude oil", "industrial"])
def _(S):
    r = L(S, 0, 0.8)
    return [
        shell(poly([(3, 9), (6.5, 9), (6.5, 21), (3, 21)], closed=True, r=r)),
        shell(poly([(10, 3), (14, 3), (14, 21), (10, 21)], closed=True, r=r)),
        shell(poly([(17.5, 13), (21, 13), (21, 21), (17.5, 21)], closed=True, r=r)),
        line("M6.5 16H10M14 17H17.5"),
        solid(flame(19.25, 4.5, 4, 6.5)),
    ]


@icon("chemical-plant", CAT, "Two round-bottomed reactor vessels on legs joined by a pipe, beside a tall chimney",
      tags=["reactor", "chemical works", "processing plant", "factory", "vessel", "industrial"])
def _(S):
    def vessel(x):
        return poly([(x, 6), (x + 6, 6), (x + 6, 11)], closed=False, r=0) + f"A3 3 0 0 1 {x} 11Z"
    return [
        shell(vessel(2.5)),
        shell(vessel(11.5)),
        line("M4.5 13.5L3.5 21M6.5 13.5L7.5 21".replace("M6.5", "M7 ").replace("7.5 21", "8 21")),
        line("M13.5 13.5L12.5 21M16.5 13.5L17.5 21"),
        line("M8.5 8H11.5"),
        line("M21 3V21"),
    ]


@icon("blast-furnace", CAT, "Tall tapering furnace tower with a round-topped stove beside it and a pipe bridge",
      tags=["furnace", "iron smelting", "steelworks", "ironworks", "hot blast", "foundry"])
def _(S):
    return [
        shell(poly([(5.5, 21), (3.5, 14), (7.5, 3), (11.5, 3), (15.5, 14), (13.5, 21)], closed=True, r=S.r)),
        detail("M5.5 14.5H13.5"),
        shell("M18 21V12.5A1.75 1.75 0 0 1 21.5 12.5V21Z"),
        line("M11.5 5.5H19.75V10.75"),
    ]


@icon("bessemer-converter", CAT, "Egg-shaped steel converter tilted to pour a stream of molten metal from its mouth",
      tags=["steel converter", "steelmaking", "molten metal", "pouring", "foundry", "metallurgy"])
def _(S):
    body = "M9.5 3.5H12.5C13 7 17 8.5 17 13.5A6 6 0 0 1 5 13.5C5 8.5 9 7 9.5 3.5Z"
    return [
        shell(rotd(body, 50, 11, 14)),
        line("M20.5 10.5Q22.5 15 20 21"),
    ]


@icon("steel-ladle", CAT, "Bucket-shaped ladle hung from a crane hook by a bail, tipped to pour molten metal",
      tags=["ladle", "molten steel", "foundry", "crane", "pouring", "casting", "metal"])
def _(S):
    bucket = poly([(5, 9), (17, 9), (15, 19), (7, 19)], closed=True, r=S.r)
    return [
        shell(rotd(bucket, 20, 11, 13)),
        line("M6.5 8L11 3.5L17.5 12.5"),
        line("M11 3.5V2"),
        line("M20 15Q21.5 18 20.5 21"),
    ]


@icon("industrial-kiln", CAT, "Brick dome kiln with an arched fire opening and a short chimney",
      tags=["kiln", "oven", "firing", "ceramics", "brick", "furnace", "heat"])
def _(S):
    return [
        shell("M3 21V14A9 9 0 0 1 21 14V21Z"),
        detail("M9 21V16.5A3 3 0 0 1 15 16.5V21"),
        line("M10 7V2.5H14V7"),
    ]


@icon("rotary-kiln", CAT, "Long tilted tube resting on two rollers with a flame at the low end and a feed hopper at the high end",
      tags=["cement kiln", "rotating drum", "calcining", "furnace", "kiln", "industrial heat"])
def _(S):
    cx, cy, a = 13.5, 12, -12
    tube = poly(rotp([(6.5, 9), (20.5, 9), (20.5, 15), (6.5, 15)], a, cx, cy), closed=True, r=S.r)
    p1 = rotp([(10.5, 15)], a, cx, cy)[0]
    p2 = rotp([(17, 15)], a, cx, cy)[0]
    return [
        shell(tube),
        line(f"M{fmt(p1[0])} {fmt(p1[1] + 1.5)}V21M{fmt(p2[0])} {fmt(p2[1] + 1.5)}V21"),
        line("M2.5 21H21.5"),
        shell(poly([(16, 2.5), (21.5, 2.5), (20, 6), (17.5, 6)], closed=True)),
        solid(rotd(flame(3.25, 10.5, 3.5, 6.5), -90, 3.25, 14)),
    ]


@icon("flare-stack", CAT, "Tall thin pipe tower held by guy wires with a flame at the tip",
      tags=["gas flare", "flaring", "oil and gas", "burn off", "refinery", "stack"])
def _(S):
    return [
        shell(poly([(10, 9), (14, 9), (14, 21), (10, 21)], closed=True, r=S.r * 0.5)),
        solid(flame(12, 2, 5, 7)),
        line("M10 13L4 21M14 13L20 21"),
    ]


@icon("industrial-control-panel", CAT, "Tall control cabinet with round dial gauges, indicator lights and switches",
      tags=["control cabinet", "switchboard", "dials", "gauges", "scada", "machine control", "plc"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, S.R if S.name == "rounded" else 1)),
        detail(circle(8, 8, 2.5)),
        detail(circle(16, 8, 2.5)),
        dot(7, 13.5, 1.25), dot(12, 13.5, 1.25), dot(17, 13.5, 1.25),
        detail("M7 17V19.5M12 17V19.5M17 17V19.5"),
    ]


@icon("water-treatment-plant", CAT, "Two round open settling tanks seen at an angle with a water drop above",
      tags=["wastewater", "sewage works", "clarifier", "settling tank", "water utility", "purification"])
def _(S):
    ry = L(S, 3, 3.5)

    def tank(cx):
        x0, x1 = cx - 4.5, cx + 4.5
        return f"M{fmt(x0)} 13.5V17A4.5 {ry} 0 0 0 {fmt(x1)} 17V13.5"
    return [
        line(tank(7)), line(tank(17)),
        shell(ellipse(7, 13.5, 4.5, ry)),
        shell(ellipse(17, 13.5, 4.5, ry)),
        solid(drop(12, 1.5, *L(S, (4.5, 6.5), (5, 6)))),
    ]


@icon("shipyard", CAT, "Ship hull resting on cradles beside a tall gantry crane with a hook",
      tags=["shipbuilding", "dockyard", "dry dock", "boat building", "gantry", "maritime", "hull"])
def _(S):
    return [
        shell(poly([(2.5, 12.5), (11, 12.5), (9.5, 17.5), (4, 17.5)], closed=True, r=S.r)),
        line("M2.5 21H11.5M5.5 17.5V21M8.5 17.5V21"),
        line("M14.5 21V4.5H21.5V21M14.5 4.5H9.5M10 4.5V9"),
        line("M4.5 12.5V9.5H7V12.5"),
    ]


@icon("silicon-wafer", CAT, "Round disc with a grid of chips and one flat edge at the bottom",
      tags=["semiconductor", "chip", "microchip", "fab", "integrated circuit", "die", "electronics manufacturing"])
def _(S):
    r, cy = 9.25, 11
    fy = 17.75
    hw = math.sqrt(r * r - (fy - cy) ** 2)
    ang = math.degrees(math.atan2(fy - cy, hw))
    body = arc(12, cy, r, 180 - ang, ang + 360) + "Z"

    def xs(y):
        return math.sqrt(r * r - (y - cy) ** 2) - 0.5
    g = 0 if S.name == "line" else 2.0
    return [
        shell(body),
        detail(f"M9 {fmt(cy - math.sqrt(r*r-9) + g)}V{fmt(fy - g)}M15 {fmt(cy - math.sqrt(r*r-9) + g)}V{fmt(fy - g)}"),
        detail(f"M{fmt(12 - xs(8) + g)} 8H{fmt(12 + xs(8) - g)}M{fmt(12 - xs(14) + g)} 14H{fmt(12 + xs(14) - g)}"),
    ]


# ============================================================================ machine tools and process equipment

def star(cx, cy, ro, ri, n, start=-90.0):
    pts = []
    for i in range(n * 2):
        rad = ro if i % 2 == 0 else ri
        a = math.radians(start + i * 180 / n)
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return pts


@icon("lathe-chuck", CAT, "Round chuck face with three stepped jaws pointing at a central hole",
      tags=["chuck", "lathe", "jaws", "turning", "machining", "workholding", "metalworking"])
def _(S):
    parts = [shell(circle(12, 12, 9.25))]
    for ang in (-90, 30, 150):
        loc = [(-2.25, -8.2), (2.25, -8.2), (2.25, -5.6), (1, -5.6), (1, -3.6), (-1, -3.6), (-1, -5.6), (-2.25, -5.6)]
        pts = rotp([(12 + x, 12 + y) for x, y in loc], ang + 90, 12, 12)
        parts.append(Part("dot", poly(pts, closed=True, r=S.r * 0.5)))
    parts.append(detail(circle(12, 12, L(S, 1.0, 1.4))))
    return parts


@icon("cnc-machine", CAT, "Enclosed machine tool with a large window showing the spindle and a control screen",
      tags=["cnc", "machining centre", "milling machine", "machine tool", "manufacturing", "metalworking"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, S.R if S.name == "rounded" else 1)),
        detail(rect(5, 7, 9.5, 10, L(S, 0, 1))),
        solid(rect(8.75, 8.5, 2, 4.5)),
        detail(rect(17, 7, 2.5, 4)),
        dot(18.25, 15, 1.1),
    ]


@icon("hydraulic-press", CAT, "H-shaped press frame with a thick ram pushing a platen down onto the bed",
      tags=["press", "ram", "piston", "forming", "metal press", "workshop", "compress"])
def _(S):
    rr = L(S, 0, 1.5)
    return [
        shell(rect(3, 3, 18, 4, rr)),
        shell(rect(3, 17.5, 18, 3.5, rr)),
        line("M5 7V17.5M19 7V17.5"),
        shell(rect(10, 7, 4, 4.5)),
        shell(rect(7, 11.5, 10, 3.5, rr)),
    ]


@icon("steam-hammer", CAT, "A-frame with a steam cylinder on top driving a heavy hammer block down onto an anvil",
      tags=["power hammer", "forge hammer", "forging", "blacksmith", "drop hammer", "heavy industry"])
def _(S):
    return [
        line("M9.5 4L3.5 21M14.5 4L20.5 21"),
        shell(rect(9, 2.5, 6, 5, L(S, 0, 1.5))),
        line("M12 7.5V11"),
        shell(rect(9, 11, 6, 4, L(S, 0, 1.2))),
        shell(rect(7.5, 18, 9, 3, L(S, 0, 1.2))),
    ]


@icon("rolling-mill", CAT, "Two stacked rollers squeezing a thick slab into a thinner sheet",
      tags=["roller mill", "steel mill", "rolling", "flattening", "sheet metal", "metal forming"])
def _(S):
    return [
        shell(circle(13, 6.5, 3.75)),
        shell(circle(13, 17.5, 3.75)),
        shell(rect(2.5, 8.5, 5, 7, L(S, 0, 1.5))),
        line("M17.5 12H21.5"),
        dot(13, 6.5, 1.0), dot(13, 17.5, 1.0),
    ]


@icon("injection-molding-machine", CAT, "Long machine body with a feed hopper at one end and a boxy mold clamp at the other",
      tags=["injection moulding", "plastics", "plastic manufacturing", "moulding machine", "polymer", "factory"])
def _(S):
    return [
        shell(poly([(2.5, 2.5), (9.5, 2.5), (7.5, 8), (4.5, 8)], closed=True, r=S.r)),
        shell(rect(2.5, 8.5, 13, 6.5, L(S, 0, 2))),
        shell(rect(17, 5, 4.5, 11, L(S, 0, 1.5))),
        detail("M19.25 5V16" if False else "M17 10.5H21.5"),
        line("M2.5 20H21.5M5 15V20M19.25 16V20"),
    ]


@icon("laser-cutter", CAT, "Nozzle head shining a thin beam onto a flat sheet with sparks at the cut",
      tags=["laser cutting", "cnc laser", "sheet metal", "fabrication", "beam", "plasma", "cut"])
def _(S):
    return [
        shell(poly([(8.5, 2.5), (15.5, 2.5), (14, 8), (10, 8)], closed=True, r=S.r)),
        line("M12 9.5V14.5"),
        shell(rect(2.5, 14.5, 19, 4.5, L(S, 0, 1.5))),
        detail("M12 14.5V19"),
        line("M8 11L9.5 12.5M16 11L14.5 12.5"),
    ]


@icon("industrial-shredder", CAT, "Box with two interlocking toothed rotors inside and scraps falling out below",
      tags=["shredder", "recycling", "waste processing", "scrap", "grinder", "rotors", "granulator"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 13, L(S, 0, 2))),
        Part("dot", poly(star(8.5, 9, 4, 2.4, 6), closed=True)),
        Part("dot", poly(star(15.5, 9, 4, 2.4, 6, -60), closed=True)),
        dot(7, 19.5, 1.25), dot(12, 20.5, 1.25), dot(17, 19.5, 1.25),
    ]


@icon("jaw-crusher", CAT, "V-shaped chamber between a fixed jaw and a swinging jaw with rocks above and gravel below",
      tags=["rock crusher", "crusher", "quarry", "mining", "aggregate", "gravel", "crushing"])
def _(S):
    return [
        shell(poly([(2.5, 3), (6.5, 3), (11, 15.5), (8, 15.5)], closed=True, r=S.r * 0.5)),
        shell(poly([(21.5, 3), (17.5, 3), (13, 15.5), (16, 15.5)], closed=True, r=S.r * 0.5)),
        dot(12, 4.5, 1.5), dot(10.3, 8, 1.3),
        dot(10, 19.5, 1.25), dot(14, 19.5, 1.25), dot(12, 21, 1.0),
    ]


@icon("ball-mill", CAT, "Horizontal drum on two rollers cut open to show steel balls tumbling inside",
      tags=["grinding mill", "tumbler", "mineral processing", "milling", "drum", "steel balls", "pulverizer"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 12.5, L(S, 3, 5.5))),
        dot(8, 12, 1.6), dot(12.5, 9.5, 1.6), dot(15.5, 13, 1.6), dot(10.5, 14, 1.6),
        line("M6.5 19V21M17.5 19V21"),
    ]


@icon("filter-press", CAT, "Row of upright plates clamped between a fixed head and a hydraulic cylinder on a long frame",
      tags=["plate filter", "dewatering", "sludge", "filtration", "process equipment", "solids separation"])
def _(S):
    rr = L(S, 0, 1)
    return [
        line("M2.5 5H21.5"),
        shell(rect(3, 6.5, 2.5, 11.5, rr)),
        line("M9 7.5V17M12.5 7.5V17M16 7.5V17"),
        shell(rect(19, 9, 2.5, 6, rr)),
        line("M2.5 20.5H21.5"),
    ]


@icon("cyclone-separator", CAT, "Upright cylinder narrowing to a long cone with a side inlet pipe and a top outlet pipe",
      tags=["cyclone", "dust collector", "particle separation", "air pollution control", "hopper", "industrial filter"])
def _(S):
    return [
        shell(poly([(7, 6.5), (16, 6.5), (16, 12), (13.5, 21), (9.5, 21), (7, 12)], closed=True, r=S.r)),
        line("M10 6.5V2.5H13V6.5"),
        line("M21.5 9H16"),
    ]


@icon("agitator-tank", CAT, "Open tank with a motor on top turning a shaft and a mixing propeller",
      tags=["mixer", "mixing tank", "stirred tank", "blender", "process vessel", "impeller", "reactor"])
def _(S):
    return [
        shell(poly([(4, 9), (4, 20.5), (20, 20.5), (20, 9)], r=S.r)),
        line("M3 9H21"),
        shell(rect(9, 2.5, 6, 4.5, L(S, 0, 1.2))),
        detail("M12 7V14.5"),
        detail("M8 17.5L12 14.5L16 17.5"),
    ]


@icon("industrial-boiler", CAT, "Horizontal cylindrical boiler on legs with a chimney and a pressure gauge",
      tags=["steam boiler", "boiler", "heating plant", "pressure vessel", "steam", "boiler room"])
def _(S):
    return [
        shell(rect(2.5, 10.5, 19, 7.5, L(S, 2.5, 3.75))),
        shell(rect(5, 3, 3.5, 7.5)),
        dot(16, 6.5, 2.25),
        line("M16 8.5V10.5"),
        line("M6 18V21M18 18V21"),
    ]


@icon("heat-exchanger", CAT, "Horizontal shell with a zigzag tube inside and short nozzles on top and bottom",
      tags=["shell and tube", "heat transfer", "cooling", "exchanger", "process plant", "condenser"])
def _(S):
    return [
        shell(rect(2.5, 7.5, 19, 9, L(S, 1.5, 4))),
        detail(poly([(6.5, 12), (9, 10), (11.5, 14), (14, 10), (16.5, 14), (18, 12)])),
        line("M7.5 7.5V3M16.5 16.5V21"),
    ]


# ============================================================================ pumps, motors and drives

@icon("gear-pump", CAT, "Oval pump casing cut open to show two meshing gears with an inlet and an outlet port",
      tags=["pump", "hydraulic pump", "oil pump", "fluid", "gears", "positive displacement"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 19, 11, L(S, 4, 5.5))),
        Part("dot", poly(star(8.4, 12, 3.7, 3.0, 9), closed=True)),
        Part("dot", poly(star(15.6, 12, 3.7, 3.0, 9, -90 + 180 / 9), closed=True)),
        line("M6 6.5V3M18 17.5V21"),
    ]


@icon("submersible-pump", CAT, "Slim vertical pump with a strainer band near the bottom, a pipe and a cable leaving the top",
      tags=["borehole pump", "well pump", "sump pump", "water pump", "sewage pump", "dewatering"])
def _(S):
    return [
        shell(rect(7.5, 7.5, 9, 13.5, L(S, 1, 3))),
        detail("M7.5 16H16.5"),
        line("M10.5 7.5V2.5"),
        line("M14 7.5V5.5Q14 3.5 16 3.5H21.5"),
    ]


@icon("steam-turbine", CAT, "Cutaway rotor with rows of blades growing longer inside a widening casing",
      tags=["turbine", "power plant", "generator", "rotor", "blades", "energy", "thermal power"])
def _(S):
    return [
        shell(poly([(4, 7), (20, 4), (20, 20), (4, 17)], closed=True, r=S.r)),
        detail("M8 9.5V14.5M12 8.5V15.5M16 7V17"),
        line("M2 12H4M20 12H22"),
    ]


@icon("alternator", CAT, "Round alternator seen from the front with cooling slots around the body and a pulley in the centre",
      tags=["generator", "car alternator", "charging", "automotive", "belt drive", "engine part", "dynamo"])
def _(S):
    parts = [shell(circle(12, 12, 9.25))]
    for a in range(0, 360, 60):
        parts.append(detail(arc(12, 12, 6.6, a - 14 + 30, a + 14 + 30)))
    parts.append(shell(circle(12, 12, L(S, 2.6, 3.0))))
    return parts


@icon("electric-motor", CAT, "Cylindrical motor on its side with cooling fins, a mounting foot and a shaft",
      tags=["motor", "ac motor", "induction motor", "drive", "machine", "rotor", "horsepower"])
def _(S):
    return [
        shell(rect(3, 5.5, 14, 10.5, L(S, 1.5, 3.5))),
        detail("M7.5 8.5V13M10.5 8.5V13M13.5 8.5V13"),
        line("M17 10.75H22"),
        line("M6 16V20H14V16"),
    ]


@icon("servo-motor", CAT, "Small rectangular servo with mounting tabs on both sides and a cross-shaped horn on top",
      tags=["servo", "hobby servo", "actuator", "robotics", "rc", "arduino", "positioning"])
def _(S):
    return [
        shell(rect(6, 11, 12, 9.5, L(S, 1, 2.5))),
        line("M2.5 16H6M18 16H21.5"),
        line("M7 6.5H17M12 2.5V10"),
        detail("M9 15.5H15"),
    ]


@icon("flywheel", CAT, "Heavy spoked wheel with a thick rim resting on a base block",
      tags=["momentum wheel", "rotating mass", "inertia", "energy storage", "engine part", "spoked wheel"])
def _(S):
    parts = [line(circle(12, 9.5, 7.5)), shell(circle(12, 9.5, 2.25))]
    for a in range(0, 360, 60):
        x1, y1 = pt_on(12, 9.5, 2.25, a + 30)
        x2, y2 = pt_on(12, 9.5, 6.6, a + 30)
        parts.append(line(seg(x1, y1, x2, y2)))
    parts.append(shell(rect(6.5, 19, 11, 2.5, L(S, 0, 1.2))))
    return parts


@icon("centrifugal-governor", CAT, "Vertical spindle with two heavy balls on hinged arms swinging out from its top",
      tags=["flyball governor", "speed regulator", "steam engine", "watt governor", "spindle", "feedback control"])
def _(S):
    return [
        line("M12 3V21M8.5 21H15.5"),
        line("M12 4L5.5 12.5M12 4L18.5 12.5"),
        line("M8.8 8.2L12 13.5M15.2 8.2L12 13.5"),
        shell(circle(5.25, 14, 2.75)),
        shell(circle(18.75, 14, 2.75)),
    ]


@icon("steam-engine", CAT, "Horizontal cylinder whose piston rod drives a crank turning a large spoked flywheel",
      tags=["steam power", "piston engine", "locomotive", "industrial revolution", "boiler engine", "crank"])
def _(S):
    parts = [
        shell(rect(2.5, 10.5, 8.5, 5.5, L(S, 0, 1.5))),
        line("M11 13.25H15"),
        line(circle(17, 12.5, 4.75)),
        shell(circle(17, 12.5, 1.5)),
        line("M6 10.5V7H9V10.5"),
        line("M2.5 20H21.5M5 16V20M17 17.25V20"),
    ]
    for a in (0, 90, 180, 270):
        x1, y1 = pt_on(17, 12.5, 1.5, a + 45)
        x2, y2 = pt_on(17, 12.5, 4.75, a + 45)
        parts.append(line(seg(x1, y1, x2, y2)))
    return parts


@icon("toggle-clamp", CAT, "Lever clamp on a base with a hinged handle and a spindle pressing down on a pad",
      tags=["clamp", "latch clamp", "workholding", "jig", "fixture", "quick clamp", "hold down"])
def _(S):
    return [
        line("M2.5 21H21.5"),
        shell(rect(3.5, 9.5, 5, 10, L(S, 0, 1.5))),
        line("M6 9.5L9 2.5"),
        line("M8.5 12.5H16"),
        line("M16 12.5V16.5"),
        shell(rect(13.5, 16.5, 5, 2.5, L(S, 0, 1))),
    ]


@icon("paint-spray-gun", CAT, "Spray gun with a paint cup on top, a pistol grip and a cone of spray dots from the nozzle",
      tags=["airbrush", "sprayer", "painting", "spray paint", "coating", "finish", "auto body"])
def _(S):
    return [
        shell(rect(2.5, 9, 11, 5, L(S, 0, 2))),
        shell(rect(4.5, 2.5, 6, 4.5, L(S, 0, 1.2))),
        line("M6 14V21H9.5L10.5 14"),
        line("M13.5 11.5H16"),
        dot(19, 11.5, 1.1), dot(21.5, 8, 1.1), dot(21.5, 15, 1.1), dot(21.5, 11.5, 1.1), dot(19, 14.5, 1.0), dot(19, 8.5, 1.0),
    ]


@icon("roller-conveyor", CAT, "Row of round rollers on a rail with a box riding on top",
      tags=["conveyor", "rollers", "material handling", "warehouse", "packaging line", "logistics", "gravity roller"])
def _(S):
    parts = [shell(rect(5, 3.5, 14, 8, L(S, 0, 2)))]
    for x in (4, 8, 12, 16, 20):
        parts.append(shell(circle(x, 15, 1.5)))
    parts.append(line("M2.5 19.5H21.5"))
    return parts


@icon("screw-conveyor", CAT, "Horizontal tube cut open to show a spiral auger with a hopper at one end",
      tags=["auger", "screw feeder", "bulk material", "worm conveyor", "grain auger", "helix"])
def _(S):
    return [
        shell(poly([(2.5, 2.5), (9.5, 2.5), (8, 9), (4, 9)], closed=True, r=S.r)),
        shell(rect(2.5, 9.5, 19, 7, L(S, 0, 3))),
        detail("M7 10.5L9 15.5M11.5 10.5L13.5 15.5M16 10.5L18 15.5"),
        line("M18.5 16.5V20.5"),
    ]


@icon("bucket-elevator", CAT, "Tall vertical belt loop with small buckets, running over a top and a bottom wheel",
      tags=["grain elevator", "conveyor belt", "vertical conveyor", "lift", "bulk handling", "buckets"])
def _(S):
    parts = [shell(poly([(8, 2.5), (16, 2.5), (16, 21.5), (8, 21.5)], closed=True, r=L(S, 3, 4))),
             dot(12, 6.5, 1.5), dot(12, 17.5, 1.5)]
    for y in (8, 12, 16):
        parts.append(solid(rect(3.5, y - 1, 3, 2.5)))
    return parts


@icon("overhead-conveyor", CAT, "Horizontal rail with trolleys, each carrying a hook and a hanging part",
      tags=["trolley conveyor", "monorail", "hanging", "assembly line", "paint line", "factory", "hook"])
def _(S):
    return [
        line("M2.5 3.5H21.5"),
        shell(rect(5, 5.5, 4, 3, L(S, 0, 1))),
        line("M7 8.5V11"),
        shell(rect(4, 11, 6, 9.5, L(S, 0, 2))),
        shell(rect(15, 5.5, 4, 3, L(S, 0, 1))),
        line("M17 8.5V11"),
        shell(circle(17, 14.5, 3.5)),
    ]


# ============================================================================ lifting gear and mechanisms

@icon("gantry-crane", CAT, "Rectangular portal frame on wheeled legs with a trolley on the top beam and a hook",
      tags=["portal crane", "overhead crane", "container crane", "hoist", "lifting", "heavy lifting", "yard crane"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 3.5, L(S, 0, 1.5))),
        line("M5 6.5V18.5M19 6.5V18.5"),
        shell(circle(5, 20, 1.5)), shell(circle(19, 20, 1.5)),
        shell(rect(9.5, 6.5, 4, 2.5, L(S, 0, 1))),
        line("M11.5 9V15.5A2.25 2.25 0 0 0 16 15.5V14.5"),
    ]


@icon("jib-crane", CAT, "Vertical pillar with a horizontal arm swinging out from the top and a hoist hook hanging from it",
      tags=["pillar crane", "workshop crane", "swing arm crane", "hoist", "lifting", "davit", "cantilever"])
def _(S):
    return [
        line("M5 3V21M2.5 21H8.5"),
        line("M5 4H21.5"),
        line("M5 11.5L13 4"),
        shell(rect(15, 6.5, 4, 3, L(S, 0, 1))),
        line("M17 9.5V16A2.25 2.25 0 0 1 12.5 16V15"),
    ]


@icon("capstan", CAT, "Short flared drum with push bars sticking out of its head and a rope wound around it",
      tags=["windlass", "winch", "rope", "ship", "anchor", "nautical", "drum", "hauling"])
def _(S):
    return [
        shell("M8 9.5C9.5 12.5 9.5 17 8 21H16C14.5 17 14.5 12.5 16 9.5Z"),
        shell(rect(6.5, 6, 11, 3.5, L(S, 0, 1.2))),
        line("M6.5 7L2.5 3.5M17.5 7L21.5 3.5"),
        detail("M9.3 13.5L14.7 15.5M9.3 17.5L14.7 19.5" if False else "M9 13L15 14.5M8.8 17L15.2 18.5"),
        line("M16 18.5Q19.5 19 21.5 21.5" if False else "M15.6 18.5Q19.5 18.5 21 21"),
    ]


@icon("lifting-magnet", CAT, "Round flat electromagnet hanging from crane chains with scrap pieces stuck underneath",
      tags=["electromagnet", "scrap handling", "scrapyard", "crane magnet", "recycling", "steel", "hoist"])
def _(S):
    return [
        line("M7.5 8L12 2.5L16.5 8"),
        shell(rect(4.5, 8, 15, 5, L(S, 1.5, 2.5))),
        solid(poly([(6.5, 14.5), (11, 14.5), (9, 19.5)], closed=True)),
        solid(rect(12, 14.5, 3, 3.5)),
        solid(poly([(16, 14.5), (18.5, 14.5), (18, 20)], closed=True)),
    ]


@icon("clamshell-grab", CAT, "Grab bucket hanging from cables with two curved jaws meeting at the bottom",
      tags=["grab bucket", "dredging", "bulk handling", "crane attachment", "excavation", "scoop", "crane"])
def _(S):
    return [
        line("M12 2.5V4.5"),
        shell(rect(9, 4.5, 6, 3.5, L(S, 0, 1))),
        line("M9 8L4 12M15 8L20 12"),
        shell("M3 12.5A8 8 0 0 0 11 20.5V12.5Z"),
        shell("M13 20.5A8 8 0 0 0 21 12.5H13Z"),
    ]


@icon("planetary-gear", CAT, "Central sun gear with three planet gears inside a large surrounding ring gear",
      tags=["epicyclic gear", "gearbox", "transmission", "sun gear", "ring gear", "reduction gear", "drivetrain"])
def _(S):
    parts = [line(circle(12, 12, 9.25)), solid(poly(star(12, 12, 3.2, 2.2, 8), closed=True, r=S.r * 0.3))]
    for a in (-90, 30, 150):
        x, y = pt_on(12, 12, 5.9, a)
        parts.append(solid(circle(x, y, L(S, 1.9, 2.1))))
    return parts


@icon("herringbone-gear", CAT, "Gear seen from the side as a short cylinder with V-shaped chevron teeth across its face",
      tags=["double helical gear", "chevron gear", "gearbox", "transmission", "helical", "shaft", "drive"])
def _(S):
    return [
        shell(rect(5, 3, 14, 18, L(S, 1, 3))),
        detail("M5 7L12 10.5L19 7M5 12.5L12 16L19 12.5" if False else "M5 6.5L12 9.5L19 6.5M5 11.5L12 14.5L19 11.5M5 16.5L12 19.5L19 16.5"),
        line("M2.5 12H5M19 12H21.5"),
    ]


@icon("ratchet-and-pawl", CAT, "Wheel with slanted sawtooth teeth and a hinged pawl arm catching one tooth",
      tags=["ratchet", "pawl", "one-way", "locking mechanism", "sawtooth wheel", "winch", "mechanism"])
def _(S):
    cx, cy = 10.5, 13.8
    pts = []
    n = 8
    for k in range(n):
        a = k * 360 / n
        pts.append(pt_on(cx, cy, 5.8, a))
        pts.append(pt_on(cx, cy, 8.2, a + 330 / n))
    return [
        shell(poly(pts, closed=True, r=S.r * 0.4)),
        detail(circle(cx, cy, 1.4)),
        line("M20.5 5L12.8 6.2"),
        dot(20.5, 5, 1.6),
    ]


@icon("roller-chain", CAT, "Short diagonal section of chain with peanut-shaped side plates and pins",
      tags=["chain", "drive chain", "bicycle chain", "sprocket", "links", "transmission", "chain drive"])
def _(S):
    parts = []
    for c in ((6.5, 17.5), (12, 12), (17.5, 6.5)):
        d = poly([(c[0] - 4.6, c[1] - 1.9), (c[0] + 4.6, c[1] - 1.9), (c[0] + 4.6, c[1] + 1.9), (c[0] - 4.6, c[1] + 1.9)], closed=True, r=0) if False else rect(c[0] - 4.25, c[1] - 1.9, 8.5, 3.8, L(S, 1.0, 1.9))
        parts.append(shell(rotd(d, -45, c[0], c[1])))
    for c in ((9.25, 14.75), (14.75, 9.25)):
        parts.append(dot(c[0], c[1], L(S, 0.9, 1.1)))
    return parts


@icon("pillow-block-bearing", CAT, "Bearing housing on a flat base with a bolt hole on each side and a shaft through its round middle",
      tags=["bearing", "plummer block", "shaft support", "bearing housing", "mounted bearing", "bolt", "mechanical"])
def _(S):
    return [
        shell(poly([(2.5, 20.5), (2.5, 15.5), (6, 15.5), (6, 10.5)], closed=False) + "A6 6 0 0 1 18 10.5V15.5H21.5V20.5Z"),
        detail(circle(12, 10.75, L(S, 3.4, 3.1))),
        dot(12, 10.75, 1.3),
        dot(4.3, 18.25, 1.0), dot(19.7, 18.25, 1.0),
    ]


@icon("cam-and-follower", CAT, "Egg-shaped cam on a shaft with a vertical rod resting on its edge",
      tags=["cam", "follower", "camshaft", "lobe", "eccentric", "valve train", "linkage", "mechanism"])
def _(S):
    egg = "M12 8C15.3 8 18 11.5 18 15.2A6 6 0 0 1 6 15.2C6 11.5 8.7 8 12 8Z"
    return [
        shell(rotd(egg, 25, 12, 15)),
        dot(12, 15.4, 1.3),
        line("M9.5 4.5H14.5M12 4.5V2.5" if False else "M12 2.5V6M9 6H15"),
    ]


@icon("crank-handle", CAT, "Z-shaped crank arm fixed to a shaft with a rounded knob grip at the far end",
      tags=["crank", "hand crank", "winch handle", "turning handle", "manual drive", "rotate", "winding"])
def _(S):
    return [
        line("M2.5 19.5H9.5V8.5H14.5"),
        shell(rect(14.5, 5.75, 7, 5.5, 2.75)),
        shell(rect(2.5, 17.5, 3.5, 4, L(S, 0, 1))) if False else dot(9.5, 19.5, 1.4),
    ]


@icon("geneva-drive", CAT, "Drive wheel with a pin engaging one slot of a four-slotted wheel",
      tags=["geneva mechanism", "maltese cross", "intermittent motion", "indexing", "film projector", "mechanism"])
def _(S):
    cx, cy, r = 15.5, 11.5, 6.5
    parts = [shell(circle(cx, cy, r))]
    for a in (155, 245, 335, 65):
        x1, y1 = pt_on(cx, cy, 2.6, a)
        x2, y2 = pt_on(cx, cy, r + 0.3, a)
        parts.append(detail(seg(x1, y1, x2, y2)))
    parts.append(shell(circle(6.5, 17.5, 3.5)))
    parts.append(dot(8.9, 15.0, 1.25))
    return parts


@icon("clutch-plate", CAT, "Round disc with a friction ring, four spring windows and a splined centre hub",
      tags=["clutch", "friction disc", "driven plate", "transmission", "car part", "clutch disc", "drivetrain"])
def _(S):
    parts = [shell(circle(12, 12, 9.25)), detail(circle(12, 12, 6.6))]
    for a in (45, 135, 225, 315):
        x, y = pt_on(12, 12, 4.0, a)
        parts.append(dot(x, y, L(S, 0.95, 1.1)))
    parts.append(Part("dot", poly(star(12, 12, 2.0, 1.4, 6), closed=True, r=S.r * 0.3)))
    return parts


@icon("brake-disc", CAT, "Round disc rotor with drilled holes and a caliper clamped over one edge",
      tags=["rotor", "disc brake", "brake caliper", "car part", "braking", "motorcycle", "drilled disc"])
def _(S):
    parts = [shell(circle(10.5, 12, 8.25)), detail(circle(10.5, 12, 1.6))]
    for a in range(0, 360, 60):
        x, y = pt_on(10.5, 12, 4.4, a + 30)
        parts.append(dot(x, y, 0.95))
    parts.append(shell(rect(16, 7, 6, 10, L(S, 1, 2.5))))
    return parts


# ============================================================================ actuators, engine parts and fittings

def union_d(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus_d(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


@icon("solenoid", CAT, "Wire coil wound around a tube with a metal plunger part way inside one end",
      tags=["electromagnet", "coil", "actuator", "plunger", "relay", "valve actuator", "linear actuator"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 13, 11, L(S, 1, 3))),
        detail("M6.5 7L8.5 17M10.5 7L12.5 17" if False else "M6.5 7.5L8 16.5M10.5 7.5L12 16.5"),
        shell(rect(12, 10, 9.5, 4, L(S, 0, 1.5))),
    ]


@icon("lead-screw", CAT, "Long threaded rod with a nut block riding on it and a small motor at one end",
      tags=["threaded rod", "power screw", "linear motion", "screw drive", "cnc", "3d printer", "actuator"])
def _(S):
    return [
        shell(rect(2.5, 7.5, 5, 9, L(S, 1, 2))),
        line(poly([(7.5, 13.75), (9.5, 10.25), (11.5, 13.75), (13.5, 10.25), (15.5, 13.75), (17.5, 10.25), (19.5, 13.75), (21.5, 10.25)])),
        solid(rect(11, 5.5, 5, 13, L(S, 0, 1.5))),
    ]


@icon("ball-joint", CAT, "Ball held in a round socket cup with a threaded stud rising out of the ball",
      tags=["ball and socket", "suspension", "tie rod end", "swivel", "pivot", "linkage", "joint"])
def _(S):
    return [
        shell("M4 11.5A8 8 0 0 0 20 11.5Z"),
        shell(rect(10.25, 2.5, 3.5, 5.5, L(S, 0, 1))),
        shell(circle(12, 11.5, 3.4)),
    ]


@icon("lever-and-fulcrum", CAT, "Straight plank balanced on a small triangle with a heavy block on one end",
      tags=["lever", "fulcrum", "seesaw", "simple machine", "physics", "balance", "leverage"])
def _(S):
    plank = rect(2.5, 11, 19, 2.5, L(S, 0, 1.25))
    block = rect(3.5, 5, 5.5, 6.5, L(S, 0, 1.2))
    return [
        shell(rotd(union_d(plank, block), -9, 12, 12.25)),
        shell(poly([(12, 14), (8.5, 21), (15.5, 21)], closed=True, r=S.r)),
    ]


@icon("connecting-rod", CAT, "Rod with a large round split ring at one end and a small round eye at the other",
      tags=["con rod", "piston rod", "crankshaft link", "engine part", "automotive", "crank", "linkage"])
def _(S):
    big = circle(12, 16.25, 4.75)
    small = circle(12, 5.75, 2.6)
    shank = poly([(9.6, 6.5), (14.4, 6.5), (15.2, 15), (8.8, 15)], closed=True)
    body = union_d(big, small, shank)
    body = minus_d(body, circle(12, 16.25, L(S, 1.9, 2.15))) if True else body
    return [shell(body)]


@icon("camshaft", CAT, "Straight shaft with a row of egg-shaped cam lobes pointing in different directions",
      tags=["cam lobes", "engine", "valve timing", "automotive", "shaft", "cams", "engine part"])
def _(S):
    def lobe(x, sgn):
        return union_d(circle(x, 12, 1.9), circle(x, 12 + sgn * 5.2, 1.0), poly([(x - 1.9, 12), (x - 1.0, 12 + sgn * 5.2), (x + 1.0, 12 + sgn * 5.2), (x + 1.9, 12)], closed=True))
    return [
        line("M2.5 12H21.5"),
        shell(lobe(5.4, -1)), shell(lobe(12, 1)), shell(lobe(18.6, -1)),
    ]


@icon("engine-valve", CAT, "Poppet valve with a long stem, a flared mushroom head and a coil spring around the stem",
      tags=["poppet valve", "intake valve", "exhaust valve", "valve spring", "cylinder head", "engine part", "automotive"])
def _(S):
    return [
        line("M12 2.5V14"),
        shell("M10.75 14C10.75 16.5 8 17.5 4.5 18.5V20.5H19.5V18.5C16 17.5 13.25 16.5 13.25 14Z"),
        line(poly([(8, 5), (16, 6.75), (8, 8.5), (16, 10.25), (8, 12)])),
    ]


@icon("fuel-injector", CAT, "Slim cylinder with an electrical connector near the top and a fine spray from its tip",
      tags=["injector", "fuel system", "spray nozzle", "engine part", "automotive", "diesel", "petrol"])
def _(S):
    return [
        shell(rect(8.5, 2.5, 7, 11, L(S, 1, 2.5))),
        shell(rect(15.5, 4.5, 4.5, 4, L(S, 0, 1.2))),
        shell(poly([(10, 13.5), (14, 13.5), (13, 16.5), (11, 16.5)], closed=True)),
        line("M12 18.5V21.5M9 18.5L8 21.5M15 18.5L16 21.5"),
    ]


@icon("exhaust-muffler", CAT, "Oval canister with a thin pipe entering one end and leaving the other",
      tags=["silencer", "exhaust", "tailpipe", "car part", "automotive", "noise", "resonator"])
def _(S):
    return [
        shell(rect(5, 6.5, 14, 11, L(S, 4, 5.5))),
        detail("M10.5 9V15M13.5 9V15"),
        line("M2 15H5M19 9H22"),
    ]


@icon("oil-filter", CAT, "Cylindrical filter canister with grip ribs and a threaded centre stub on top",
      tags=["spin-on filter", "engine oil", "car maintenance", "automotive", "filter", "lubrication", "service"])
def _(S):
    return [
        shell(rect(5, 8.5, 14, 12.5, L(S, 1, 3))),
        shell(rect(10, 4, 4, 4.5)),
        detail("M5 15H19M5 18H19"),
        dot(7.75, 11.25, 0.9), dot(16.25, 11.25, 0.9),
    ]


@icon("v-engine", CAT, "Engine seen from the front with two cylinder banks angled apart in a V above the crankcase",
      tags=["v8", "v6", "engine block", "cylinders", "motor", "automotive", "internal combustion", "piston engine"])
def _(S):
    bank = union_d(rect(9.75, 6.5, 4.5, 9, L(S, 0, 1)), rect(8.5, 3.5, 7, 3.5, L(S, 0, 1.2)))
    return [
        shell(rotd(bank, -32, 12, 17)),
        shell(rotd(bank, 32, 12, 17)),
        shell(rect(5.5, 15.5, 13, 5.5, L(S, 1, 2.75))),
    ]


@icon("rotary-engine", CAT, "Rounded triangle rotor inside an oval housing pinched at the middle, with a small central shaft",
      tags=["wankel", "wankel engine", "rotor", "engine", "triangular rotor", "automotive", "combustion"])
def _(S):
    housing = "M12 7.5C10 3.5 2.5 4 2.5 12C2.5 20 10 20.5 12 16.5C14 20.5 21.5 20 21.5 12C21.5 4 14 3.5 12 7.5Z"
    r = 4.9
    v = [pt_on(12, 12, r, a) for a in (180, 60, 300)]
    rotor = f"M{fmt(v[0][0])} {fmt(v[0][1])}A6.4 6.4 0 0 1 {fmt(v[1][0])} {fmt(v[1][1])}A6.4 6.4 0 0 1 {fmt(v[2][0])} {fmt(v[2][1])}A6.4 6.4 0 0 1 {fmt(v[0][0])} {fmt(v[0][1])}Z"
    return [
        shell(housing),
        detail(rotor),
        dot(12, 12, 1.2),
    ]


@icon("radial-engine", CAT, "Seven cylinders arranged like a star around a round central hub",
      tags=["aircraft engine", "star engine", "piston engine", "aviation", "cylinders", "vintage", "warbird"])
def _(S):
    parts = []
    cyl = rect(10, 2.5, 4, 6.5, L(S, 0, 1.2))
    for k in range(7):
        parts.append(shell(rotd(cyl, k * 360 / 7, 12, 12)))
    parts.append(shell(circle(12, 12, 3.4)))
    parts.append(dot(12, 12, 1.1))
    return parts


@icon("turbofan-engine", CAT, "Jet engine cutaway hanging from a wing, with a large front fan, a tapering core and an exhaust nozzle",
      tags=["jet engine", "aircraft engine", "aviation", "fan blades", "nacelle", "airliner", "propulsion"])
def _(S):
    return [
        line("M2.5 3.5H21.5M13.5 3.5V7.5"),
        shell("M5.5 8.5C2.5 11 2.5 17.5 5.5 20L16 17L21.5 16V12.5L16 11Z"),
        detail("M8.5 10.5V18"),
        detail("M12 12.8V15.8M15.5 13.2V15.2"),
    ]


@icon("marine-propeller", CAT, "Three-bladed ship propeller seen from the front with broad curved blades around a round hub",
      tags=["ship propeller", "boat propeller", "screw", "prop", "maritime", "outboard", "thrust"])
def _(S):
    blade = "M10.5 9.5C8 7.5 8.3 3.8 12 2.5C15.7 3.8 16 7.5 13.5 9.5Z"
    parts = [shell(rotd(blade, a, 12, 12)) for a in (0, 120, 240)]
    parts.append(shell(circle(12, 12, 2.4)) if S.name == "rounded" else shell(poly(regular(12, 12, 2.8, 6), closed=True)))
    return parts


@icon("impeller", CAT, "Round disc with curved vanes spiralling out from a central hub",
      tags=["pump impeller", "centrifugal pump", "vanes", "fan wheel", "rotor", "blower", "turbine wheel"])
def _(S):
    parts = [line(circle(12, 12, 9.25)), shell(circle(12, 12, 1.9))]
    for a in range(0, 360, 60):
        x1, y1 = pt_on(12, 12, 2.4, a)
        x2, y2 = pt_on(12, 12, 8.2, a + 55)
        parts.append(line(f"M{fmt(x1)} {fmt(y1)}A7 7 0 0 1 {fmt(x2)} {fmt(y2)}"))
    return parts


@icon("pressure-regulator", CAT, "Valve body on a pipe with a round diaphragm dome on top and a small gauge on the side",
      tags=["regulator", "pressure reducing valve", "gas regulator", "diaphragm valve", "plumbing", "pressure control"])
def _(S):
    return [
        shell("M9.5 19V13.5H7.5A6 6 0 0 1 19.5 13.5H17.5V19Z"),
        line("M2.5 16.5H9.5M17.5 16.5H21.5"),
        shell(circle(4.5, 8, 2.4)),
        line("M4.5 10.4V16.5"),
    ]


@icon("float-valve", CAT, "Valve on a pipe end with a long arm ending in a round float ball",
      tags=["ballcock", "float", "tank fill valve", "cistern", "water level", "toilet", "level control"])
def _(S):
    return [
        line("M2.5 5.5H8.5"),
        shell(rect(8.5, 3, 5, 5, L(S, 0, 1.2))),
        line("M12 8L17.5 15.5"),
        shell(circle(18, 17.5, 3.5)),
        line("M2.5 19.5H11"),
    ]


@icon("y-strainer", CAT, "Pipe fitting with a slanted leg branching downward in a Y and ending in a capped end",
      tags=["strainer", "pipe filter", "plumbing", "pipe fitting", "inline filter", "valve", "debris screen"])
def _(S):
    body = union_d(rect(2.5, 3.5, 19, 5.5, L(S, 0, 1.5)), rotd(rect(9.5, 8, 5, 12), 38, 12, 8))
    return [
        shell(body),
        line(poly(rotp([(8.5, 20.5), (15.5, 20.5)], 38, 12, 8))),
    ]
