"""TypeIcon Core: utilities (power, water and grid infrastructure), batch 001."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, transform_path

CAT = "utilities"


def knock(d) -> Part:
    """Small solid shape: solid in Line/Rounded, knocked out of a Filled shell (like a dot)."""
    return Part("dot", d)


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def uni(*ds) -> str:
    """Union of several closed d-strings into one silhouette."""
    return path_to_d(U(*[P(d) for d in ds]))


def bolt(cx, cy, s=1.0, r=0.0):
    pts = [(0.5, -3.75), (-2.5, 0.5), (0, 0.5), (-0.75, 3.75), (2.5, -0.75), (0, -0.75)]
    return poly([(cx + x * s, cy + y * s) for x, y in pts], closed=True, r=r)


def drop_d(cx, top, bottom_r, cy):
    r = bottom_r
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + r * 0.35)} {fmt(top + (cy - top) * 0.35)} {fmt(cx + r)} {fmt(cy - r * 0.55)} "
            f"{fmt(cx + r)} {fmt(cy)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx - r)} {fmt(cy)}"
            f"C{fmt(cx - r)} {fmt(cy - r * 0.55)} {fmt(cx - r * 0.35)} {fmt(top + (cy - top) * 0.35)} {fmt(cx)} {fmt(top)}Z")


def flame_d(cx, top, bot, w):
    """Small flame (solid mark) centred on cx between y=top and y=bot, half width w."""
    h = bot - top
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + w * 0.3)} {fmt(top + h * 0.3)} {fmt(cx + w)} {fmt(top + h * 0.5)} {fmt(cx + w)} {fmt(bot - w)}"
            f"A{fmt(w)} {fmt(w)} 0 0 1 {fmt(cx - w)} {fmt(bot - w)}C{fmt(cx - w)} {fmt(top + h * 0.55)} {fmt(cx - w * 0.2)} {fmt(top + h * 0.4)} {fmt(cx)} {fmt(top)}Z")


# ============================================================================ generation

@icon("coal-power-plant", CAT, "Power plant building with a tall smokestack and a heap of coal on a conveyor",
      tags=["coal", "power station", "fossil fuel", "smokestack", "thermal plant", "electricity", "generation"])
def _(S):
    body = uni(rect(2, 12, 11, 9, rr(S, 2)), rect(4.5, 3, 5, 10))
    return [
        shell(body),
        shell(poly([(14.5, 21), (18.5, 14.5), (22.5, 21)], closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
        line(seg(13, 11.5, 17, 13)),
    ]


@icon("gas-fired-power-plant", CAT, "Low power plant with two slim exhaust stacks and a flame on its front wall",
      tags=["gas plant", "natural gas", "power station", "ccgt", "exhaust stack", "electricity", "generation"])
def _(S):
    body = uni(rect(2.5, 11, 19, 10, rr(S, 2)), rect(5.5, 3.5, 3, 8.5), rect(15.5, 3.5, 3, 8.5))
    return [shell(body), knock(flame_d(12, 13.5, 19.5, 2.6))]


@icon("waste-to-energy-plant", CAT, "Plant building with a chimney, a bolt on the wall and a trash bag at the door",
      tags=["incinerator", "waste", "energy from waste", "garbage", "recycling plant", "electricity", "chimney"])
def _(S):
    body = uni(rect(2, 11, 13, 10, rr(S, 2)), rect(8, 3, 4, 9))
    bag = uni(circle(19, 17.8, 3.4), rect(17.9, 13.5, 2.2, 3))
    return [shell(body), knock(bolt(8.5, 16.5, 0.85)), shell(bag)]


@icon("tidal-barrage", CAT, "Low dam wall with a turbine in it, higher water on one side and a crescent moon above",
      tags=["tidal power", "tide", "barrage", "marine energy", "sea", "moon", "renewable"])
def _(S):
    return [
        shell(rect(9.5, 7, 5, 14, rr(S, 1.5))),
        detail(circle(12, 14, 1.5)),
        line(seg(2, 12.5, 7, 12.5)),
        line(seg(2, 16.5, 7, 16.5)),
        line(seg(17, 18, 22, 18)),
        shell(path_to_d(D(P(circle(18, 6.5, 3.75)), P(circle(20.2, 5.3, 3.2))))),
    ]


@icon("diesel-generator", CAT, "Enclosed generator set on a skid base with a vented end and an exhaust pipe",
      tags=["generator", "genset", "backup power", "standby", "diesel", "engine", "emergency power"])
def _(S):
    return [
        line(poly([(16.5, 8), (16.5, 3.5), (20, 3.5)], r=S.r * 0.6)),
        shell(rect(2, 8, 20, 9, rr(S, 2))),
        detail(seg(5.5, 11, 5.5, 14)),
        detail(seg(8.5, 11, 8.5, 14)),
        line(seg(2, 20.5, 22, 20.5)),
    ]


@icon("gas-turbine", CAT, "Cutaway of a horizontal gas turbine with a narrow intake, blade stages and a flared exhaust",
      tags=["turbine", "jet engine", "compressor", "combustion turbine", "power generation", "engine", "exhaust"])
def _(S):
    outline = [(2, 10.5), (8, 8), (15, 8), (22, 4.5), (22, 19.5), (15, 16), (8, 16), (2, 13.5)]
    return [
        shell(poly(outline, closed=True, r=S.r * 0.6)),
        detail(seg(8.5, 8.5, 8.5, 15.5)),
        detail(seg(12, 8.5, 12, 15.5)),
        detail(seg(15.5, 8.5, 15.5, 15.5)),
    ]


@icon("heliostat", CAT, "Tilted flat mirror on a post bouncing a sun ray, as used in solar tower plants",
      tags=["solar mirror", "concentrated solar", "csp", "solar tower", "reflector", "sun tracking", "renewable"])
def _(S):
    a = math.radians(-20)
    c, s_ = math.cos(a), math.sin(a)
    hw, ht = 7.5, 1.6
    pts = [(12 + x * c - y * s_, 14.5 + x * s_ + y * c) for x, y in [(-hw, -ht), (hw, -ht), (hw, ht), (-hw, ht)]]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.6)),
        line(seg(12, 16, 12, 21)),
        line(seg(8.5, 21, 15.5, 21)),
        line(seg(3, 3, 8.5, 8.5)),
        line(seg(15.5, 8.5, 21, 3)),
    ]


@icon("solar-dish-collector", CAT, "Large round parabolic dish on a pedestal with a receiver held at its focus by struts",
      tags=["parabolic dish", "concentrated solar", "stirling dish", "solar thermal", "reflector", "renewable", "sun"])
def _(S):
    return [
        shell("M3 10Q12 21 21 10Z", stroke_miterlimit="2"),
        shell(rect(9.5, 2.5, 5, 3.5, rr(S, 1))),
        line(seg(4.5, 9.5, 10, 6)),
        line(seg(19.5, 9.5, 14, 6)),
        line(seg(12, 15.5, 12, 21)),
        line(seg(8.5, 21, 15.5, 21)),
    ]


@icon("wind-turbine-nacelle", CAT, "Side view of a wind turbine housing on its tower with the rotor hub and blade roots",
      tags=["nacelle", "wind turbine", "gearbox", "hub", "rotor", "wind power", "renewable", "maintenance"])
def _(S):
    body = uni(rect(10.5, 9.5, 11, 6, rr(S, 2)), rect(13.5, 14, 4, 7.5))
    return [
        shell(body),
        shell(circle(6.5, 12.5, 2.5)),
        detail(seg(13, 11.5, 19, 11.5)),
        line(seg(6.5, 2.5, 6.5, 9)),
        line(seg(6.5, 16, 6.5, 21.5)),
    ]


@icon("floating-wind-turbine", CAT, "Wind turbine on a floating platform at the waterline with slanted mooring lines",
      tags=["offshore wind", "floating platform", "mooring", "sea", "wind power", "renewable", "ocean"])
def _(S):
    hub = (12, 7.5)
    blades = [line(seg(*polar(*hub, 2.2, a), *polar(*hub, 5.5, a))) for a in (-90, 30, 150)]
    return [
        *blades,
        shell(circle(*hub, 1.4)),
        line(seg(12, 9, 12, 13)),
        shell(rect(9, 13, 6, 3.5, rr(S, 1.5))),
        line(seg(2, 14.5, 6, 14.5)),
        line(seg(18, 14.5, 22, 14.5)),
        line(seg(10, 16.5, 6, 21.5)),
        line(seg(14, 16.5, 18, 21.5)),
    ]


@icon("bladeless-wind-turbine", CAT, "Tall slim tapered cone on a small base with curved lines showing it swaying",
      tags=["vortex", "wind", "oscillating", "no blades", "wind power", "renewable", "tower"])
def _(S):
    cone = poly([(11, 3), (13, 3), (15, 17), (9, 17)], closed=True, r=S.r * 0.6)
    return [
        shell(cone),
        line(seg(7, 20.5, 17, 20.5)),
        line("M5.5 7Q3.5 10 5.5 13"),
        line("M18.5 7Q20.5 10 18.5 13"),
    ]


@icon("airborne-wind-kite", CAT, "Tethered kite high in the air with a long line to a ground winch",
      tags=["kite power", "high altitude wind", "tether", "wind energy", "renewable", "flying", "winch"])
def _(S):
    return [
        shell(poly([(16, 2.5), (20.5, 7), (16, 11.5), (11.5, 7)], closed=True, r=S.r * 0.5)),
        line("M16 11.5Q15 17 9 18.5"),
        shell(rect(3, 17.5, 7, 4, rr(S, 1.5))),
    ]


@icon("gravity-energy-storage", CAT, "Crane tower lifting a heavy block above a stack of blocks with an up and down arrow",
      tags=["gravity battery", "energy storage", "crane", "weight lifting", "block", "grid storage", "renewable"])
def _(S):
    return [
        line(poly([(4, 21), (4, 3.5), (13, 3.5)], r=S.r)),
        line(seg(9.5, 3.5, 9.5, 7)),
        shell(rect(6.5, 7, 6, 4, rr(S, 1))),
        shell(rect(6.5, 16, 10, 5, rr(S, 1.5))),
        detail(seg(11.5, 16, 11.5, 21)),
        line(seg(19.5, 5, 19.5, 13)),
        line(poly([(17.5, 7), (19.5, 5), (21.5, 7)])),
        line(poly([(17.5, 11), (19.5, 13), (21.5, 11)])),
    ]


@icon("flow-battery", CAT, "Two upright electrolyte tanks joined by pipes to a cell stack between them",
      tags=["redox", "electrolyte", "vanadium", "grid storage", "energy storage", "tank", "battery"])
def _(S):
    return [
        shell(rect(2, 2.5, 6, 10, rr(S, 3))),
        shell(rect(16, 2.5, 6, 10, rr(S, 3))),
        shell(rect(9, 15, 6, 6, rr(S, 2))),
        line(poly([(5, 12.5), (5, 18), (9, 18)], r=S.r * 0.7)),
        line(poly([(19, 12.5), (19, 18), (15, 18)], r=S.r * 0.7)),
    ]


@icon("compressed-air-storage", CAT, "Ground cross section with a compressor house at the surface and a pipe down to an underground cavern",
      tags=["caes", "energy storage", "cavern", "compressor", "underground", "grid storage", "air"])
def _(S):
    return [
        shell(rect(3, 6, 6, 6, rr(S, 1.5))),
        line(seg(9, 12, 22, 12)),
        line(seg(6, 12, 6, 16.5)),
        shell(ellipse(13.5, 18, 8, 3.5)),
    ]


# ============================================================================ hydro, heat and off-grid

def _rot_rect(cx, cy, length, width, deg):
    a = math.radians(deg)
    c, s_ = math.cos(a), math.sin(a)
    hl, hw = length / 2, width / 2
    return [(cx + x * c - y * s_, cy + x * s_ + y * c) for x, y in [(-hl, -hw), (hl, -hw), (hl, hw), (-hl, hw)]]


@icon("penstock", CAT, "Thick pipe running down a hillside from a reservoir into a small powerhouse",
      tags=["hydro", "pipe", "hydroelectric", "water pipe", "powerhouse", "reservoir", "hillside"])
def _(S):
    return [
        line(seg(2, 3.5, 9, 3.5)),
        shell(poly(_rot_rect(10, 10.5, 12, 3.6, 45), closed=True, r=S.r * 0.4)),
        shell(rect(14.5, 14, 7.5, 7, rr(S, 1.5))),
    ]


@icon("francis-turbine", CAT, "Snail-shaped spiral casing wrapped around a round runner with curved vanes",
      tags=["hydro turbine", "volute", "runner", "water turbine", "hydropower", "spiral case", "generator"])
def _(S):
    return [
        shell("M12 3H21V12A9 9 0 1 1 12 3Z" if S.name == "line" else "M12 3H18.5Q21 3 21 5.5V12A9 9 0 1 1 12 3Z"),
        detail(circle(12, 12, 4.5)),
        dot(12, 12, 1.25),
    ]


@icon("district-heating-pipes", CAT, "Two parallel pipes feeding a row of houses, a shared heat network",
      tags=["district heating", "heat network", "central heating", "pipes", "heating", "homes", "utility"])
def _(S):
    h1 = poly([(3, 12.5), (3, 8.5), (6.5, 5), (10, 8.5), (10, 12.5)], closed=True, r=S.r * 0.5)
    h2 = poly([(14, 12.5), (14, 8.5), (17.5, 5), (21, 8.5), (21, 12.5)], closed=True, r=S.r * 0.5)
    return [
        shell(h1), shell(h2),
        line(seg(2, 17, 22, 17)),
        line(seg(2, 21, 22, 21)),
        line(seg(6.5, 12.5, 6.5, 17)),
        line(seg(17.5, 12.5, 17.5, 17)),
    ]


@icon("pedal-generator", CAT, "Bicycle on a stand with its rear wheel turning a small generator that lights a bulb",
      tags=["bike generator", "human powered", "dynamo", "exercise bike", "off grid", "cycling", "light bulb"])
def _(S):
    return [
        shell(circle(7, 15.5, 5)),
        dot(7, 15.5, 1.1),
        line(seg(5.5, 10.5, 5.5, 7.5)),
        line(seg(2.5, 7.5, 8.5, 7.5)),
        shell(rect(14, 14, 6.5, 6, rr(S, 1.5))),
        shell(circle(17.25, 6, 2.75)),
        line(seg(17.25, 9.5, 17.25, 14)),
    ]


@icon("balcony-solar-panel", CAT, "Solar panel hung from a balcony railing with a short cable and plug",
      tags=["plug-in solar", "balcony power station", "apartment solar", "renewable", "rail", "mini pv", "home energy"])
def _(S):
    return [
        line(seg(2, 3.5, 22, 3.5)),
        line(seg(7.5, 3.5, 7.5, 8)),
        line(seg(16.5, 3.5, 16.5, 8)),
        shell(rect(3.5, 8, 17, 9, rr(S, 1.5))),
        detail(seg(12, 8, 12, 17)),
        line(poly([(12, 17), (12, 19)])),
        solid(rect(10.5, 19, 3, 2.5, 0.5)),
    ]


@icon("solar-home-kit", CAT, "Small solar panel wired to a battery box and a hanging light bulb, an off-grid starter set",
      tags=["off grid", "solar kit", "starter kit", "solar lighting", "battery", "light bulb", "rural electrification"])
def _(S):
    return [
        shell(poly([(2.5, 10.5), (5, 3.5), (13, 3.5), (10.5, 10.5)], closed=True, r=S.r * 0.4)),
        line(seg(7.5, 10.5, 7.5, 14.5)),
        shell(rect(2.5, 14.5, 10, 6.5, rr(S, 1.5))),
        line(poly([(12.5, 18), (18.5, 18), (18.5, 14)])),
        line(seg(18.5, 2.5, 18.5, 6)),
        shell(circle(18.5, 10.2, 3.6)),
    ]


@icon("solar-still", CAT, "Glass pyramid over a basin of water under the sun, collecting clean drinking water",
      tags=["desalination", "distillation", "drinking water", "solar distiller", "evaporation", "condensation", "survival"])
def _(S):
    return [
        shell(rect(3, 16, 18, 5, rr(S, 1.5))),
        line(poly([(5, 15), (12, 6.5), (19, 15)], r=S.r * 0.4)),
        knock(drop_d(12, 9.5, 1.6, 13.4)),
        dot(20, 4, 1.75),
    ]


@icon("solar-updraft-tower", CAT, "Very tall slim chimney rising from the middle of a wide low glass roof with rising air arrows",
      tags=["solar chimney", "updraft", "thermal tower", "greenhouse", "renewable", "airflow", "power tower"])
def _(S):
    body = uni(poly([(2, 20.5), (2, 18), (9, 15.5), (15, 15.5), (22, 18), (22, 20.5)], closed=True), rect(10.5, 2.5, 3, 14))
    return [
        shell(body),
        line(seg(5.5, 13, 5.5, 8)),
        line(poly([(4, 9.5), (5.5, 8), (7, 9.5)])),
        line(seg(18.5, 13, 18.5, 8)),
        line(poly([(17, 9.5), (18.5, 8), (20, 9.5)])),
    ]


@icon("space-solar-power", CAT, "Satellite with solar wings beaming a wavy ray down to a receiver dish on the ground",
      tags=["orbital solar", "satellite", "microwave beam", "wireless power", "renewable", "space", "receiver"])
def _(S):
    return [
        shell(rect(10, 2.5, 4, 4.5, rr(S, 1))),
        shell(rect(2, 3, 6, 3.5, rr(S, 1))),
        shell(rect(16, 3, 6, 3.5, rr(S, 1))),
        line("M12 9.5Q10 11.25 12 13T12 16.5"),
        shell("M6 17.5Q12 24 18 17.5Z", stroke_miterlimit="2"),
    ]


# ============================================================================ power equipment

@icon("portable-power-station", CAT, "Compact battery box with a carry handle, a level display and a row of outlets",
      tags=["power bank", "camping power", "battery generator", "solar generator", "outlets", "backup power", "portable"])
def _(S):
    return [
        line(poly([(8, 7), (8, 3.5), (16, 3.5), (16, 7)], r=S.r * 0.6)),
        shell(rect(3, 7, 18, 14, rr(S, 3))),
        knock(rect(6.5, 10, 11, 3, 0.5 if S.name == "rounded" else 0)),
        dot(8, 17.5, 1.25), dot(12, 17.5, 1.25), dot(16, 17.5, 1.25),
    ]


@icon("pad-mounted-transformer", CAT, "Low metal cabinet on a concrete pad with vent slots and a bolt on its door",
      tags=["green box", "utility box", "electrical transformer", "distribution", "substation", "underground power", "hazard"])
def _(S):
    return [
        shell(rect(3, 5, 18, 12, rr(S, 2))),
        detail(seg(6.5, 9, 10.5, 9)),
        detail(seg(6.5, 13, 10.5, 13)),
        knock(bolt(15.5, 11, 0.8)),
        line(seg(2, 20.5, 22, 20.5)),
    ]


@icon("switchgear-cabinet", CAT, "Row of three tall metal cabinets, each with a window, a switch and a meter",
      tags=["switchboard", "control cabinet", "electrical panel", "distribution board", "substation", "medium voltage", "breaker"])
def _(S):
    parts = [shell(rect(2, 3, 20, 18, rr(S, 4))), detail(seg(8.67, 3, 8.67, 21)), detail(seg(15.33, 3, 15.33, 21))]
    for cx in (5.3, 12, 18.7):
        parts += [knock(rect(cx - 1.4, 6, 2.8, 3, 0.7 if S.name == 'rounded' else 0)), dot(cx, 13, 1.1), knock(rect(cx - 1.2, 16.5, 2.4, 1.6))]
    return parts


@icon("underground-power-cable", CAT, "Ground cross section with a buried round cable, warning tape above it and grass on top",
      tags=["buried cable", "underground", "trench", "warning tape", "power line", "electrical", "dig safe"])
def _(S):
    return [
        line(seg(2, 8.5, 22, 8.5)),
        line(seg(5, 8.5, 5, 5)), line(seg(12, 8.5, 12, 4.5)), line(seg(19, 8.5, 19, 5)),
        line(seg(3, 12.5, 7, 12.5)), line(seg(10, 12.5, 14, 12.5)), line(seg(17, 12.5, 21, 12.5)),
        shell(circle(12, 18, 3.25)),
        dot(12, 18, 1),
    ]


@icon("industrial-cable-spool", CAT, "Large cable reel seen from the front with wound cable and a loose end trailing out",
      tags=["cable drum", "reel", "wire", "cable roll", "wound cable", "electrician", "construction"])
def _(S):
    body = uni(rect(2.5, 3, 3.5, 17, rr(S, 1.5)), rect(18, 3, 3.5, 17, rr(S, 1.5)), rect(5, 6, 14, 11))
    return [
        shell(body),
        detail(seg(9.75, 6, 9.75, 17)),
        detail(seg(14.25, 6, 14.25, 17)),
        line("M8 17V19Q8 21.5 11 21.5H15"),
    ]



@icon("bird-flight-diverter", CAT, "Power line with two spiral coils wrapped around it and a small bird flying above",
      tags=["bird diverter", "wildlife", "power line marker", "avian protection", "wire marker", "coil", "conservation"])
def _(S):
    return [
        line(seg(2, 16, 22, 16)),
        line(seg(4.5, 13, 6.5, 19)), line(seg(7.5, 13, 9.5, 19)),
        line(seg(14.5, 13, 16.5, 19)), line(seg(17.5, 13, 19.5, 19)),
        line("M8 8Q10 4.5 12 8Q14 4.5 16 8"),
    ]


@icon("power-line-marker-ball", CAT, "Power line strung between two poles with a large round marker ball on the middle",
      tags=["aviation marker", "warning ball", "overhead line", "cable marker", "visibility", "aircraft safety", "wire"])
def _(S):
    return [
        line(seg(3, 3.5, 3, 21)),
        line(seg(21, 3.5, 21, 21)),
        line(seg(3, 7, 9.5, 11)),
        line(seg(14.5, 11, 21, 7)),
        shell(circle(12, 12.5, 3.5)),
    ]


def smooth(pts) -> str:
    """Smooth open path through points (Catmull-Rom converted to cubic Beziers)."""
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    n = len(pts)
    for i in range(n - 1):
        p0 = pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d


def sine(x0, x1, cy, amp, cycles, phase=0.0, n=24):
    return smooth([(x0 + (x1 - x0) * i / n, cy - amp * math.sin(2 * math.pi * (cycles * i / n) + phase)) for i in range(n + 1)])


def head(tip, frm, size=2.6, spread=40):
    """Arrow head chevron at tip for a stroke arriving from frm."""
    a = math.atan2(tip[1] - frm[1], tip[0] - frm[0])
    pts = []
    for sgn in (1, -1):
        b = a + math.pi + sgn * math.radians(spread)
        pts.append((tip[0] + size * math.cos(b), tip[1] + size * math.sin(b)))
    return poly([pts[0], tip, pts[1]])


# ============================================================================ grid equipment and events

@icon("surge-arrester", CAT, "Upright ribbed insulator column with a cap and a ground connection, with a bolt beside it",
      tags=["lightning arrester", "surge protector", "overvoltage", "insulator", "substation", "protection", "grounding"])
def _(S):
    return [
        shell(rect(8.5, 2.5, 7, 15.5, rr(S, 2.5))),
        detail(seg(8.5, 7, 15.5, 7)),
        detail(seg(8.5, 11, 15.5, 11)),
        detail(seg(8.5, 15, 15.5, 15)),
        line(seg(12, 18, 12, 21)),
        line(seg(8.5, 21.5, 15.5, 21.5)),
        solid(bolt(20, 9, 0.8)),
    ]


@icon("h-frame-power-pole", CAT, "Two wooden poles joined near the top by a crossbar carrying three hanging insulators",
      tags=["utility pole", "transmission structure", "crossarm", "insulators", "power line", "overhead", "wooden pole"])
def _(S):
    parts = [line(seg(4.5, 3, 4.5, 21.5)), line(seg(19.5, 3, 19.5, 21.5)), line(seg(4.5, 5.5, 19.5, 5.5))]
    for x in (8.5, 12, 15.5):
        parts += [line(seg(x, 5.5, x, 8)), solid(rect(x - 1.5, 8, 3, 4.5, 0.6 if S.name == "rounded" else 0))]
    return parts


@icon("grid-control-room", CAT, "Operator desk with two monitors in front of a wide wall screen showing a network",
      tags=["control centre", "control center", "scada", "dispatch", "operator", "monitoring", "power grid"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 9.5, rr(S, 2))),
        detail(poly([(6, 9.5), (9.5, 6), (13.5, 9), (18, 5.5)])),
        shell(rect(4.5, 15, 6, 3.5, rr(S, 1))),
        shell(rect(13.5, 15, 6, 3.5, rr(S, 1))),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("brownout", CAT, "Light bulb with one dimmed half and a down arrow, showing reduced voltage",
      tags=["low voltage", "dim lights", "voltage drop", "power sag", "reduced power", "electricity", "utility"])
def _(S):
    bulb = uni(circle(9, 9, 5.5), rect(6.5, 12, 5, 6))
    return [
        shell(bulb),
        knock("M9 5.2A3.8 3.8 0 0 1 9 12.8Z"),
        line(seg(7, 20.5, 11, 20.5)),
        line(seg(19.5, 4.5, 19.5, 17)),
        line(poly([(17.5, 15), (19.5, 17), (21.5, 15)])),
    ]


@icon("load-shedding", CAT, "Row of three small houses with the middle one dark and a clock above for a scheduled cut",
      tags=["rolling blackout", "power cut", "scheduled outage", "electricity rationing", "blackout", "schedule", "demand"])
def _(S):
    def house(x):
        return poly([(x, 21), (x, 16.5), (x + 2.25, 14), (x + 4.5, 16.5), (x + 4.5, 21)], closed=True, r=S.r * 0.3)
    return [
        shell(circle(12, 6.5, 4.5)),
        detail(poly([(12, 4), (12, 6.5), (14, 7.5)])),
        shell(house(2.5)), shell(house(9.75)), shell(house(17)),
        knock(rect(4.1, 17.2, 1.3, 1.3)), knock(rect(18.6, 17.2, 1.3, 1.3)),
    ]


@icon("outage-map", CAT, "Folded map with bolt pins on the side panels and a cross marking an outage area in the middle",
      tags=["power outage", "blackout map", "service area", "grid status", "map", "outage tracker", "utility"])
def _(S):
    outline = [(2, 6), (8.67, 4), (15.33, 6), (22, 4), (22, 18), (15.33, 20), (8.67, 18), (2, 20)]
    return [
        shell(poly(outline, closed=True, r=S.r * 0.3)),
        detail(seg(8.67, 4, 8.67, 18)),
        detail(seg(15.33, 6, 15.33, 20)),
        knock(bolt(5.3, 12.3, 0.65)),
        detail(seg(10.5, 9.5, 13.5, 14.5)),
        detail(seg(13.5, 9.5, 10.5, 14.5)),
        knock(bolt(18.7, 11.5, 0.65)),
    ]


@icon("power-surge", CAT, "Line graph with a sharp spike above a wall plug",
      tags=["voltage spike", "overvoltage", "transient", "surge", "electrical damage", "plug", "protection"])
def _(S):
    return [
        line(poly([(2.5, 7), (7.5, 7), (10, 4), (12.5, 9.5), (14.5, 7), (21.5, 7)], r=S.r * 0.5)),
        shell(rect(6, 13, 12, 5, rr(S, 2))),
        line(seg(9.5, 18, 9.5, 21.5)),
        line(seg(14.5, 18, 14.5, 21.5)),
    ]


@icon("three-phase-power", CAT, "Three stacked sine waves each shifted along the axis from the others",
      tags=["3 phase", "polyphase", "ac power", "sine waves", "phase shift", "industrial power", "electrical"])
def _(S):
    return [
        line(sine(2, 22, 5, 2, 1.5, 0.0)),
        line(sine(2, 22, 12, 2, 1.5, 2.1)),
        line(sine(2, 22, 19, 2, 1.5, 4.2)),
    ]


@icon("alternating-current-symbol", CAT, "Single sine wave inside a circle, the symbol for alternating current",
      tags=["ac", "sine", "tilde", "alternating current", "mains", "electrical symbol", "wave"])
def _(S):
    return [
        shell(circle(12, 12, 9.25)),
        detail(sine(6.5, 17.5, 12, 2.6, 1, 0.0, 12)),
    ]


# ============================================================================ energy markets and metering

@icon("vehicle-to-grid", CAT, "Electric car and a pylon linked by a two-way arrow with a bolt in the middle",
      tags=["v2g", "ev", "bidirectional charging", "electric vehicle", "grid storage", "smart grid", "battery"])
def _(S):
    car = poly([(2, 13), (2, 9.5), (4, 9.5), (5.5, 6), (9, 6), (10.5, 9.5), (12, 9.5), (12, 13)], closed=True, r=S.r * 0.5)
    return [
        shell(car),
        dot(4.75, 13, 1.6), dot(9.5, 13, 1.6),
        line(poly([(15.5, 13.5), (18.5, 4.5), (21.5, 13.5)], r=S.r * 0.3), stroke_miterlimit="1.5"),
        line(seg(16.2, 7, 20.8, 7)),
        line(seg(4.5, 18.5, 9, 18.5)), line(poly([(6.5, 16.5), (4.5, 18.5), (6.5, 20.5)])),
        line(seg(15, 18.5, 19.5, 18.5)), line(poly([(17.5, 16.5), (19.5, 18.5), (17.5, 20.5)])),
        solid(bolt(12, 18.5, 0.75)),
    ]


@icon("net-metering", CAT, "Round meter dial above two opposing arrows, power flowing both ways",
      tags=["feed in", "solar export", "meter", "bidirectional", "grid", "credits", "rooftop solar"])
def _(S):
    return [
        shell(circle(12, 7.5, 5.5)),
        detail(seg(12, 7.5, 14.5, 5)),
        dot(12, 7.5, 1.2),
        line(seg(4, 16.5, 20, 16.5)), line(head((20, 16.5), (4, 16.5), 2.2, 45)),
        line(seg(4, 20.5, 20, 20.5)), line(head((4, 20.5), (20, 20.5), 2.2, 45)),
    ]


@icon("time-of-use-pricing", CAT, "Clock with a lightning bolt at its centre and a price tag hanging from its side",
      tags=["tariff", "peak pricing", "off peak", "electricity rate", "dynamic pricing", "energy cost", "schedule"])
def _(S):
    tag = poly([(14, 18.5), (17, 15), (22, 15), (22, 22), (17, 22)], closed=True, r=S.r * 0.4)
    return [
        shell(circle(8.5, 8.5, 6.5)),
        knock(bolt(8.5, 8.5, 0.8, S.r * 0.3)),
        shell(tag),
        dot(18, 18.5, 1.1),
    ]


def _small_flame():
    d = ("M12 3C13 6 17.5 8.5 18 13.5C18.4 17.6 15.6 21 12 21C8.7 21 6 18.3 6 15C6 12.7 6.8 10.8 8.3 9.3"
         "C8.6 10.6 9.3 11.6 10.3 12.2C10 8.8 10.5 5.5 12 3Z")
    k = 0.58
    return path_to_d(transform_path(P(d), (k, 0, 0, k, 6.2 - 12 * k, 16.8 - 12 * k)))


def _cloud():
    return uni(circle(8, 7.5, 3), circle(12.5, 6, 3.5), circle(16.5, 8, 2.75), rect(8, 8, 8.5, 2.75))


@icon("virtual-power-plant", CAT, "Cloud linked by lines to two houses and a battery, many small sources acting as one plant",
      tags=["vpp", "distributed energy", "aggregated", "smart grid", "home battery", "demand response", "cloud"])
def _(S):
    h1 = poly([(2, 21), (2, 18), (5, 15), (8, 18), (8, 21)], closed=True, r=S.r * 0.3)
    h2 = poly([(16, 21), (16, 18), (19, 15), (22, 18), (22, 21)], closed=True, r=S.r * 0.3)
    return [
        shell(_cloud()),
        shell(h1), shell(h2),
        shell(rect(10, 16, 4, 5, rr(S, 1))),
        line(seg(5, 10.5, 5, 15)), line(seg(12, 10.5, 12, 16)), line(seg(19, 10.5, 19, 15)),
    ]


@icon("peer-to-peer-energy", CAT, "Two houses side by side with a curved arrow carrying a bolt from one roof to the other",
      tags=["energy sharing", "p2p trading", "community solar", "prosumer", "neighbours", "microgrid", "electricity trading"])
def _(S):
    h1 = poly([(2, 21), (2, 15), (6, 11.5), (10, 15), (10, 21)], closed=True, r=S.r * 0.4)
    h2 = poly([(14, 21), (14, 15), (18, 11.5), (22, 15), (22, 21)], closed=True, r=S.r * 0.4)
    return [
        shell(h1), shell(h2),
        line("M6 8.5Q12 -0.5 18 8.5"),
        line(head((18, 8.5), (12, -0.5), 2.4, 40)),
        solid(bolt(12, 6.8, 0.6)),
    ]


@icon("heat-meter", CAT, "Compact meter body on a pipe with a small display and a thermometer mark on its face",
      tags=["thermal meter", "heating", "energy meter", "calorimeter", "district heating", "pipe", "utility"])
def _(S):
    body = uni(rect(4, 3, 16, 11, rr(S, 3)), rect(10, 13, 4, 5), rect(2, 17.5, 20, 4, rr(S, 1.5)))
    return [
        shell(body),
        knock(rect(7, 6.5, 6, 3.5)),
        knock(rect(15.2, 5.5, 1.6, 4)),
        dot(16, 11.3, 1.3),
    ]


@icon("coin-meter", CAT, "Boxy prepayment meter with a round dial and a coin slot with a coin going in",
      tags=["prepaid meter", "pay as you go", "slot meter", "coin operated", "gas meter", "electricity meter", "old style"])
def _(S):
    return [
        line(seg(12, 1.5, 12, 6)),
        shell(rect(3, 6, 18, 15, rr(S, 2))),
        knock(rect(8.5, 9, 7, 1.6)),
        detail(circle(12, 15.5, 2.5)),
    ]


@icon("power-pedestal", CAT, "Short post with a hooded top holding two outlets and a small meter, as at marinas and campsites",
      tags=["marina", "campsite", "rv hookup", "shore power", "electric post", "outlet", "utility post"])
def _(S):
    body = uni(rect(6, 3, 12, 4.5, rr(S, 1.5)), rect(8, 6.5, 8, 14.5))
    k = 0.6 if S.name == "rounded" else 0
    return [
        shell(body),
        knock(rect(9.4, 9.5, 2, 2.6, k)), knock(rect(12.6, 9.5, 2, 2.6, k)),
        knock(rect(9.5, 14.5, 5, 3.5, k)),
    ]


@icon("home-utilities", CAT, "Water drop, gas flame and lightning bolt arranged together in a triangle",
      tags=["utilities", "bills", "water gas electricity", "household services", "energy", "supply", "home"])
def _(S):
    return [
        shell(drop_d(12, 2, 3.75, 8), stroke_miterlimit="2"),
        shell(_small_flame()),
        shell(bolt(17.5, 17, 1.3)),
    ]


@icon("line-inspection-drone", CAT, "Quadcopter hovering beside a hanging string of insulators on a power line",
      tags=["uav", "power line inspection", "utility drone", "lineman", "maintenance", "overhead line", "survey"])
def _(S):
    return [
        shell(rect(3.5, 10.5, 8, 4.5, rr(S, 1.5))),
        line(seg(4.5, 10.5, 4.5, 7)), line(seg(10.5, 10.5, 10.5, 7)),
        line(seg(2, 6.5, 7, 6.5)), line(seg(8, 6.5, 13, 6.5)),
        line(seg(2, 3, 22, 3)),
        line(seg(18, 3, 18, 20)),
        solid(rect(15.5, 8, 5, 2)), solid(rect(15.5, 12, 5, 2)), solid(rect(15.5, 16, 5, 2)),
    ]


# ============================================================================ crews and equipment

@icon("arc-flash-suit", CAT, "Front view of a protective hood with a wide dark visor over a thick protective jacket",
      tags=["electrical ppe", "protective clothing", "electrician", "safety suit", "hood", "visor", "high voltage"])
def _(S):
    body = uni(rect(7, 2.5, 10, 10, rr(S, 4)), poly([(3, 21), (3, 16), (7, 12.5), (17, 12.5), (21, 16), (21, 21)], closed=True, r=S.r * 0.5))
    return [
        shell(body),
        knock(rect(8.75, 5, 6.5, 3.5, 1 if S.name == "rounded" else 0)),
        detail(seg(12, 14.5, 12, 21)),
    ]


@icon("insulated-gloves", CAT, "Thick rubber glove with a long cuff and a small lightning bolt marked on the cuff",
      tags=["electrical gloves", "rubber gloves", "lineman", "ppe", "protection", "high voltage", "safety"])
def _(S):
    glove = uni(rect(5, 2.5, 10, 12, rr(S, 5)), rect(13.5, 8, 4.5, 5.5, 2.2), rect(4, 13, 12, 8, rr(S, 2)))
    return [
        shell(glove),
        knock(bolt(10, 17.2, 0.8, S.r * 0.3)),
        detail(seg(7.5, 5.5, 7.5, 9)) if False else detail(seg(10, 6, 10, 9.5)),
    ]


@icon("digger-derrick", CAT, "Utility truck with a boom arm that ends in a vertical auger drilling into the ground",
      tags=["pole setter", "auger truck", "utility truck", "drilling", "post hole", "boom truck", "line crew"])
def _(S):
    truck = poly([(2, 19), (2, 14), (5, 14), (7, 11), (12, 11), (12, 19)], closed=True, r=S.r * 0.4)
    return [
        shell(truck),
        solid(circle(5.5, 19.5, 2)), solid(circle(9.5, 19.5, 2)),
        line(poly([(10, 11), (16, 4), (16, 9)])),
        shell(poly([(14, 9.5), (18, 9.5), (16, 19)], closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        line(seg(13.5, 21.5, 22, 21.5)),
    ]


@icon("utility-van", CAT, "Boxy van with a ladder on the roof and a bolt and a water drop on its side panel",
      tags=["service van", "work van", "maintenance vehicle", "ladder", "engineer", "electric and water", "call out"])
def _(S):
    body = poly([(2, 17), (2, 8.5), (15.5, 8.5), (20, 12.5), (22, 14), (22, 17)], closed=True, r=S.r * 0.4)
    return [
        line(seg(3.5, 4.5, 14.5, 4.5)),
        line(seg(5.5, 4.5, 5.5, 8.5)), line(seg(12.5, 4.5, 12.5, 8.5)),
        shell(body),
        knock(bolt(6.5, 12.7, 0.7)),
        knock(drop_d(11.2, 10.4, 1.7, 13.4)),
        solid(circle(6.5, 18, 2.3)), solid(circle(17, 18, 2.3)),
    ]


@icon("plug-in-timer", CAT, "Plug-through socket timer with a round dial ringed by small push pins",
      tags=["socket timer", "mains timer", "programmable plug", "outlet timer", "schedule", "energy saving", "lights timer"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 4))), detail(circle(12, 12, 2.8))]
    for i in range(8):
        x, y = polar(12, 12, 6.2, i * 45)
        parts.append(dot(x, y, 0.85))
    return parts


# ============================================================================ water supply

@icon("borehole", CAT, "Ground cross section with a narrow pipe drilled down through the layers into groundwater and a pump on top",
      tags=["well", "water well", "groundwater", "hand pump", "aquifer", "drilling", "rural water"])
def _(S):
    return [
        shell(rect(9, 2.5, 6, 5, rr(S, 1.5))),
        line(seg(15, 4.5, 19, 4.5)),
        line(seg(2, 8.5, 9, 8.5)), line(seg(15, 8.5, 22, 8.5)),
        line(seg(12, 7.5, 12, 18)),
        line("M2 19Q4.5 17.5 7 19T12 19T17 19T22 19"),
    ]


@icon("water-pumping-station", CAT, "Small flat-roofed building with a pipe entering one side and leaving the other and a drop on the wall",
      tags=["pump house", "booster station", "waterworks", "water supply", "pipeline", "utility building", "lift station"])
def _(S):
    body = uni(rect(6, 9, 12, 11, rr(S, 1)), rect(4, 6.5, 16, 3.5))
    return [
        shell(body),
        knock(drop_d(12, 11, 2.4, 15.8)),
        line(seg(2, 18, 6, 18)),
        line(seg(18, 13, 22, 13)),
    ]


@icon("water-main", CAT, "Large pipe in a trench under the road with a smaller branch pipe rising to a house",
      tags=["water pipe", "mains", "service line", "buried pipe", "street", "plumbing", "supply"])
def _(S):
    house = poly([(14, 9), (14, 6), (18, 2.5), (22, 6), (22, 9)], closed=True, r=S.r * 0.4)
    return [
        shell(house),
        line(seg(2, 9, 14, 9)),
        line(seg(18, 9, 18, 14)),
        shell(rect(2, 14, 20, 6.5, rr(S, 3))),
    ]


@icon("reverse-osmosis-system", CAT, "Three upright filter canisters in a row joined by thin tubes at the bottom",
      tags=["ro filter", "water purifier", "membrane", "drinking water", "filtration", "under sink", "desalination"])
def _(S):
    return [
        shell(rect(2, 3, 4.5, 10, rr(S, 2))),
        shell(rect(9.75, 3, 4.5, 10, rr(S, 2))),
        shell(rect(17.5, 3, 4.5, 10, rr(S, 2))),
        line(poly([(4.25, 13), (4.25, 17.5), (12, 17.5), (12, 13)], r=S.r * 0.7)),
        line(poly([(12, 17.5), (19.75, 17.5), (19.75, 13)], r=S.r * 0.7)),
    ]


@icon("aeration-basin", CAT, "Open tank with a wavy water surface and rows of bubbles rising through it",
      tags=["wastewater", "sewage treatment", "oxygen", "bubbles", "activated sludge", "treatment plant", "tank"])
def _(S):
    return [
        shell(rect(3, 5, 18, 16, rr(S, 4))),
        detail("M3 9Q5.25 7.5 7.5 9T12 9T16.5 9T21 9"),
        dot(8, 17.5, 1.2), dot(12, 18.5, 1.2), dot(16, 17, 1.2),
        dot(10, 13.5, 1.1), dot(14.5, 13.2, 1.1),
    ]


@icon("trickling-filter", CAT, "Round bed of stones seen at an angle with a rotating sprinkler arm spraying drops across it",
      tags=["biofilter", "sewage treatment", "sprinkler", "rotary distributor", "wastewater", "stone bed", "bio filter"])
def _(S):
    return [
        line(seg(3, 6.5, 21, 6.5)),
        line(seg(12, 6.5, 12, 13.5)),
        dot(6, 10, 1.2), dot(9, 10, 1.2), dot(15, 10, 1.2), dot(18, 10, 1.2),
        shell(ellipse(12, 17, 9.5, 4)),
        dot(8, 17.2, 0.9), dot(12, 18.2, 0.9), dot(16, 17.2, 0.9),
    ]


@icon("reed-bed-filter", CAT, "Cross section of a gravel bed with tall reeds growing from it and water filtering through",
      tags=["constructed wetland", "phytoremediation", "natural filter", "reeds", "grey water", "wastewater", "gravel"])
def _(S):
    return [
        shell(rect(2, 14, 20, 7, rr(S, 1.5))),
        dot(6, 18.5, 1), dot(10, 17.5, 1), dot(14, 18.5, 1), dot(18, 17.5, 1),
        line("M7 14Q7 9 5.5 4"),
        line(seg(12, 14, 12, 3)),
        line("M17 14Q17 9 18.5 4"),
    ]


@icon("grease-trap", CAT, "Box tank with an inlet pipe, an inner baffle wall and a layer of floating grease at the top",
      tags=["fat trap", "interceptor", "kitchen drain", "fog", "restaurant plumbing", "baffle", "sewer"])
def _(S):
    return [
        line(seg(7, 2.5, 7, 12)),
        shell(rect(3, 8, 18, 13, rr(S, 2))),
        detail(seg(3, 12, 21, 12)),
        detail(seg(14, 12, 14, 18)),
    ]


@icon("fatberg", CAT, "Lumpy blob of congealed fat and wipes blocking the inside of a sewer pipe cross section",
      tags=["sewer blockage", "clog", "wipes", "grease", "drain blockage", "sewage", "pipe"])
def _(S):
    blob = [(7, 14), (6.5, 10.5), (9, 8.5), (11.5, 9.5), (14, 8), (17, 10), (17.5, 13.5), (15, 16.5), (11, 17), (8.5, 16.5)]
    return [
        shell(circle(12, 12, 9.25)),
        knock(poly(blob, closed=True, r=S.r * 1.2)),
    ]


@icon("sewer-tunnel", CAT, "Arched brick tunnel seen end on with a channel of water flowing along its floor",
      tags=["sewer", "culvert", "drain", "storm drain", "brick arch", "underground", "wastewater"])
def _(S):
    return [
        shell("M2.5 21.5V12A9.5 9.5 0 0 1 21.5 12V21.5Z" if S.name == "line" else "M2.5 19.5V12A9.5 9.5 0 0 1 21.5 12V19.5Q21.5 21.5 19.5 21.5H4.5Q2.5 21.5 2.5 19.5Z"),
        detail("M7.5 21.5V12.5A4.5 4.5 0 0 1 16.5 12.5V21.5"),
        detail("M7.5 18Q9.75 16.5 12 18T16.5 18"),
    ]


@icon("utility-tunnel", CAT, "Rectangular service tunnel seen end on with pipes along one wall and cable trays along the other",
      tags=["service tunnel", "utilidor", "pipe gallery", "cable tray", "underground services", "infrastructure", "campus tunnel"])
def _(S):
    k = 0.6 if S.name == "rounded" else 0
    return [
        shell(rect(2, 3, 20, 18, rr(S, 3))),
        detail(seg(2, 17.5, 22, 17.5)),
        dot(6.5, 7.5, 1.9), dot(6.5, 13, 1.9),
        knock(rect(14, 6.7, 5.5, 1.6, k)), knock(rect(14, 12.2, 5.5, 1.6, k)),
    ]


@icon("water-intake-tower", CAT, "Tall round tower standing in a reservoir with a narrow footbridge running to it from the shore",
      tags=["reservoir tower", "draw off tower", "dam tower", "water supply", "bridge", "lake", "valve tower"])
def _(S):
    body = uni(rect(9, 5, 6, 14, rr(S, 1)), rect(8, 2.5, 8, 4))
    return [
        shell(body),
        knock(rect(11.2, 10, 1.6, 2.5)),
        line(seg(2, 9, 9, 9)),
        line(seg(2, 16, 7, 16)), line(seg(17, 16, 22, 16)),
        line(seg(2, 20.5, 22, 20.5)),
    ]


@icon("spillway", CAT, "Stepped concrete chute running down from the top of a dam wall with water spilling over the steps",
      tags=["dam spillway", "overflow", "weir", "flood release", "water cascade", "reservoir", "hydraulic structure"])
def _(S):
    steps = [(2, 2.5), (8, 2.5), (8, 7), (12, 7), (12, 11.5), (16, 11.5), (16, 16), (22, 16), (22, 21.5), (2, 21.5)]
    return [
        shell(poly(steps, closed=True, r=S.r * 0.3)),
        dot(11, 4.5, 1.1), dot(15, 9, 1.1), dot(19, 13.5, 1.1),
    ]


@icon("embankment-dam", CAT, "Trapezoid earth dam in side view holding water on one side, with a rock-lined slope",
      tags=["earth dam", "rockfill dam", "reservoir", "levee", "water storage", "dyke", "civil engineering"])
def _(S):
    return [
        shell(poly([(5, 21), (9, 6), (15, 6), (22, 21)], closed=True, r=S.r * 0.4)),
        dot(12.5, 10, 1), dot(11, 15, 1), dot(15.5, 14.5, 1), dot(18, 18, 1), dot(13, 18.5, 1),
        line(seg(2, 11, 6.5, 11)),
        line(seg(2, 16, 4.5, 16)),
    ]


# ============================================================================ water service points

@icon("water-outage", CAT, "Tap with nothing coming out and an empty drop outline below the spout",
      tags=["no water", "dry tap", "supply cut", "water shortage", "interruption", "faucet", "drought"])
def _(S):
    return [
        line(poly([(2.5, 9), (14, 9), (14, 12.5)], r=S.r * 0.6)),
        line(seg(8, 9, 8, 5)), line(seg(5.5, 5, 10.5, 5)),
        shell(drop_d(14, 14.5, 3, 19), stroke_miterlimit="2") if False else shell(drop_d(14, 14.5, 3, 19.2), stroke_miterlimit="2"),
    ]


@icon("water-vending-machine", CAT, "Upright kiosk with a water drop sign on top, a coin slot and a dispensing bay",
      tags=["water atm", "refill station", "drinking water kiosk", "purified water", "dispenser", "coin operated", "jug refill"])
def _(S):
    k = 0.6 if S.name == "rounded" else 0
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 2.5))),
        knock(drop_d(12, 5, 2.2, 8.8)),
        knock(rect(14.5, 11, 2, 3.5, k)),
        knock(rect(7.5, 15.5, 7, 3.5, k)),
        knock(rect(10, 11.7, 2, 2.2)),
    ]


@icon("handwashing-station", CAT, "Water container on a stand with a tap over a basin and a bar of soap",
      tags=["hand wash", "tippy tap", "hygiene", "sanitation", "portable sink", "wash basin", "soap"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 9, 8.5, rr(S, 2.5))),
        line(poly([(11.5, 7.5), (15, 7.5), (15, 11)])),
        line(seg(4.5, 11, 4.5, 21.5)), line(seg(9.5, 11, 9.5, 21.5)),
        shell("M11.5 16H21Q21 20.5 16.25 20.5Q11.5 20.5 11.5 16Z" if S.name == "line" else "M12 16H21Q21 20.5 16.5 20.5Q12 20.5 12 16Z"),
        solid(rect(18, 12.5, 3.5, 2.2, 0.8)),
    ]


@icon("composting-toilet", CAT, "Wooden box toilet with a lid and a small leaf on its front and a vent pipe rising behind",
      tags=["dry toilet", "eco toilet", "off grid", "sanitation", "vent pipe", "outhouse", "waterless toilet"])
def _(S):
    body = uni(rect(5.5, 6.5, 10, 6), rect(3.5, 11, 14, 10, rr(S, 2)))
    leaf = "M9.5 19C9.2 16.3 11 14.8 14 14.8C14 17.4 12.2 19 9.5 19Z"
    return [
        line(seg(19.5, 21.5, 19.5, 3)),
        shell(body),
        knock(leaf),
    ]


@icon("limescale", CAT, "Water drop above a pipe cross section narrowed by a thick crusty inner layer",
      tags=["hard water", "calcium", "scale buildup", "kettle scale", "blocked pipe", "deposit", "plumbing"])
def _(S):
    parts = [shell(drop_d(12, 1.8 if S.name == 'line' else 2.4, 2.5, 5.8), stroke_miterlimit="2"), shell(circle(12, 16.5, 5.75)), detail(circle(12, 16.5, 2.0))]
    for a in (30, 100, 170, 240, 310):
        x, y = polar(12, 16.5, 4.25, a)
        parts.append(dot(x, y, 0.7))
    return parts


@icon("dry-riser-inlet", CAT, "Wall-mounted box with two round hose connectors inside, as fitted on buildings for firefighters",
      tags=["fire hydrant", "firefighting", "riser", "hose connection", "fire safety", "wall box", "building services"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 2.5))),
        detail(circle(8.25, 13.5, 2.2)),
        detail(circle(15.75, 13.5, 2.2)),
        knock(rect(8, 6, 8, 1.8, 0.6 if S.name == "rounded" else 0)),
    ]


@icon("storm-surge-barrier", CAT, "Row of piers across a river with curved gates between them and water below",
      tags=["flood barrier", "tidal barrier", "sea gate", "flood defence", "river", "weir", "coastal protection"])
def _(S):
    return [
        shell(rect(2, 3, 3.5, 14, rr(S, 1.5))),
        shell(rect(10.25, 3, 3.5, 14, rr(S, 1.5))),
        shell(rect(18.5, 3, 3.5, 14, rr(S, 1.5))),
        solid("M5.5 7H10.25A2.375 4.5 0 0 1 5.5 7Z"),
        solid("M13.75 7H18.5A2.375 4.5 0 0 1 13.75 7Z"),
        line("M2 20.5Q4.5 19 7 20.5T12 20.5T17 20.5T22 20.5"),
    ]


@icon("shadoof", CAT, "Upright post with a long pivoting pole, a counterweight at one end and a bucket hanging at the other over water",
      tags=["well sweep", "irrigation", "ancient water lifting", "lever", "bucket", "counterweight", "traditional"])
def _(S):
    return [
        line(seg(4.5, 8, 19.5, 5)),
        line(seg(9, 7, 9, 21.5)),
        shell(circle(4.5, 11, 2.4)),
        line(seg(19.5, 5, 19.5, 11)),
        shell(poly([(17, 11), (22, 11), (21, 16), (18, 16)], closed=True, r=S.r * 0.3)),
        line(seg(13, 20.5, 22, 20.5)),
    ]


@icon("qanat", CAT, "Ground cross section with a gently sloping underground channel and a row of vertical shafts rising to the surface",
      tags=["kariz", "aqueduct", "underground channel", "ancient irrigation", "desert water", "access shaft", "persian"])
def _(S):
    parts = [line(seg(2, 7.5, 22, 7.5)), line(seg(2, 13, 22, 19))]
    for x, y in ((6.5, 14.3), (12.5, 16.5), (18.5, 18.4)):
        parts += [line(seg(x, 4.5, x, y)), line(seg(x - 2, 4.5, x + 2, 4.5))]
    return parts


@icon("leak-listening-stick", CAT, "Long metal rod pressed to the ground with an earpiece on top and sound waves rising from a buried pipe",
      tags=["leak detection", "acoustic", "water leak", "listening rod", "pipe locator", "plumber", "survey"])
def _(S):
    return [
        shell(rect(8.5, 2.5, 7, 4, rr(S, 1.5))),
        line(seg(12, 6.5, 12, 13)),
        line(seg(2, 13.5, 8, 13.5)), line(seg(16, 13.5, 22, 13.5)),
        line(arc(12, 13.5, 4.5, 40, 140)),
        line(seg(2, 21, 22, 21)),
    ]


@icon("water-valve-key", CAT, "Tall T-shaped bar with a socket at its bottom end reaching into a small valve box in the ground",
      tags=["stop tap key", "valve key", "t-bar", "shut off", "water meter box", "utility key", "curb key"])
def _(S):
    return [
        line(seg(6, 3.5, 18, 3.5)),
        line(seg(12, 3.5, 12, 14)),
        shell(rect(7.5, 14.5, 9, 6.5, rr(S, 1.5))),
        knock(rect(10.5, 16.5, 3, 2.5)),
        line(seg(2, 14.5, 6.5, 14.5)), line(seg(17.5, 14.5, 22, 14.5)),
    ]
