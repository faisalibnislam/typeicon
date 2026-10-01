"""TypeIcon Core: industry, batch 2 (machinery, robots, power plants, process equipment)."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, pt_on, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "industry"


def cap(S, v):
    """Corner radius that stays small on small shapes but still differs between Line and Rounded."""
    if v > 2:
        return min(S.R, v)
    return v * (0.5 if S.name == "line" else 1.0)


def wedge(cx, cy, r0, r1, a0, a1):
    """Annular sector between radii r0 and r1 from angle a0 to a1 (degrees, clockwise on screen)."""
    p = polar(cx, cy, r1, a0)
    q = polar(cx, cy, r1, a1)
    s = polar(cx, cy, r0, a1)
    t = polar(cx, cy, r0, a0)
    return (f"M{fmt(p[0])} {fmt(p[1])}A{fmt(r1)} {fmt(r1)} 0 0 1 {fmt(q[0])} {fmt(q[1])}"
            f"L{fmt(s[0])} {fmt(s[1])}A{fmt(r0)} {fmt(r0)} 0 0 0 {fmt(t[0])} {fmt(t[1])}Z")


def trefoil(cx, cy, r):
    parts = [dot(cx, cy, r * 0.22)]
    for c in (-90, 30, 150):
        parts.append(Part("dot", wedge(cx, cy, r * 0.42, r, c - 30, c + 30)))
    return parts


# ============================================================================ piping, tanks, containers

@icon("pipe-manifold", CAT, "Horizontal header pipe with three branch pipes, each with a valve",
      tags=["manifold", "header pipe", "piping", "valves", "plumbing", "process plant"])
def _(S):
    parts = [shell(rect(2, 3, 20, 5, cap(S, 2)))]
    for x in (5, 12, 19):
        parts.append(line(seg(x, 8, x, 11.5)))
        parts.append(solid(poly([(x, 11.5), (x + 2.7, 14.25), (x, 17), (x - 2.7, 14.25)], closed=True)))
        parts.append(line(seg(x, 17, x, 21)))
    return parts


@icon("oil-pipeline", CAT, "Pipeline on H-shaped supports running across the ground into the distance",
      tags=["pipeline", "oil", "gas", "pipe", "supports", "energy transport"])
def _(S):
    return [
        shell(poly([(2, 3), (22, 8), (22, 13), (2, 8)], closed=True, r=S.r * 0.5)),
        line(seg(4, 9.5, 4, 20.5)), line(seg(8, 10.5, 8, 19.8)), line(seg(4, 15, 8, 15.2)),
        line(seg(15, 12, 15, 18.4)), line(seg(19, 13, 19, 17.6)), line(seg(15, 15.3, 19, 15.4)),
        line(seg(2, 21, 22, 17)),
    ]


@icon("venturi-tube", CAT, "Tube that narrows in the middle with two upright gauge tubes at different heights",
      tags=["venturi", "flow", "pressure", "fluid", "nozzle", "physics", "pipe"])
def _(S):
    return [
        shell(poly([(2, 8), (7, 8), (10, 11), (14, 11), (17, 8), (22, 8), (22, 19), (17, 19), (14, 16),
                    (10, 16), (7, 19), (2, 19)], closed=True, r=S.r)),
        line(seg(5, 8, 5, 2.5)),
        line(seg(12, 11, 12, 6.5)),
    ]


@icon("spherical-storage-tank", CAT, "Large sphere tank standing on straight legs",
      tags=["sphere tank", "gas storage", "lng", "pressure vessel", "refinery", "storage"])
def _(S):
    cy = 9.5
    eq = "M5.2 11A7 3 0 0 0 18.8 11"
    return [
        shell(circle(12, cy, 7)),
        detail(eq),
        line(seg(8, 15, 6, 21)), line(seg(16, 15, 18, 21)), line(seg(12, 16.5, 12, 21)),
    ]


@icon("oil-drum", CAT, "Upright steel drum with two raised rings and a bung on the lid",
      tags=["drum", "barrel", "oil barrel", "steel drum", "container", "chemicals", "fuel"])
def _(S):
    return [
        shell(rect(5, 2, 14, 20, cap(S, 3))),
        detail(seg(5, 9, 19, 9)), detail(seg(5, 15, 19, 15)),
        dot(15, 5.5, 1),
    ]


@icon("ibc-tote", CAT, "Cube tank inside a metal grid cage on a pallet",
      tags=["ibc", "tote", "intermediate bulk container", "liquid storage", "cage", "pallet", "chemicals"])
def _(S):
    return [
        shell(rect(4, 2, 16, 14, cap(S, 2))),
        detail(seg(12, 2, 12, 16)), detail(seg(4, 9, 20, 9)),
        dot(16, 12.5, 1.2),
        line(seg(3, 20, 21, 20)),
        line(seg(5, 16, 5, 20)), line(seg(19, 16, 19, 20)),
    ]


@icon("bulk-bag", CAT, "Large square woven sack with a lifting loop at each top corner",
      tags=["bulk bag", "fibc", "big bag", "sack", "sand", "grain", "tonne bag"])
def _(S):
    loops = [line(poly([(x0, 7), (x0, 4), (x1, 4), (x1, 7)], closed=False, r=S.r)) for x0, x1 in ((3, 6), (18, 21))]
    return [
        shell(rect(3, 7, 18, 14, cap(S, 3))),
        detail(seg(3, 11, 21, 11)),
    ] + loops


@icon("air-cargo-container", CAT, "Aircraft cargo container with a slanted top corner and a curtain door",
      tags=["uld", "air freight", "cargo", "luggage container", "unit load device", "airport"])
def _(S):
    return [
        shell(poly([(2, 10), (7, 4), (22, 4), (22, 20), (2, 20)], closed=True, r=S.r)),
        detail(seg(12, 4, 12, 20)), detail(seg(17, 4, 17, 20)),
    ]


@icon("rail-tank-car", CAT, "Railway wagon with a long cylindrical tank, a dome and two wheel sets",
      tags=["tanker wagon", "train", "rail freight", "oil train", "liquid transport", "tank"])
def _(S):
    return [
        shell(rect(2, 6, 20, 7, 3.5)),
        line(poly([(9, 6), (9, 3.5), (15, 3.5), (15, 6)], closed=False, r=S.r)),
        line(seg(2, 16, 22, 16)),
        dot(7, 20, 1.75), dot(17, 20, 1.75),
    ]


@icon("hopper-wagon", CAT, "Open railway wagon with sloping sides narrowing to two chutes",
      tags=["hopper car", "bulk freight", "coal wagon", "grain wagon", "train", "rail freight"])
def _(S):
    return [
        shell(poly([(2, 4), (22, 4), (22, 9), (18, 14), (14, 14), (12, 10), (10, 14), (6, 14), (2, 9)],
                   closed=True, r=S.r)),
        dot(7, 19.5, 2), dot(17, 19.5, 2),
    ]


@icon("radioactive-waste-drum", CAT, "Steel drum marked with a radiation trefoil",
      tags=["nuclear waste", "radioactive", "hazardous waste", "barrel", "radiation", "drum"])
def _(S):
    return [
        shell(rect(5, 2, 14, 20, cap(S, 3))),
        detail(seg(5, 5.5, 19, 5.5)), detail(seg(5, 18.5, 19, 18.5)),
    ] + trefoil(12, 12, 4.2)


# ============================================================================ robots

@icon("robotic-arm", CAT, "Industrial robot arm on a base with two jointed segments and a claw",
      tags=["robot arm", "manipulator", "automation", "factory robot", "assembly", "manufacturing"])
def _(S):
    return [
        shell(rect(3, 18, 11, 4, cap(S, 1.5))),
        line(poly([(8, 18), (8, 10), (16, 6)], closed=False, r=S.r)),
        dot(8, 10, 1.9),
        line(seg(16, 6, 16, 9.5)),
        line(poly([(13.5, 13.5), (13.5, 9.5), (18.5, 9.5), (18.5, 13.5)], closed=False, r=S.r)),
    ]


@icon("robotic-gripper", CAT, "Two-finger parallel gripper closing on a small cube",
      tags=["gripper", "end effector", "pick", "grasp", "robot tool", "automation"])
def _(S):
    return [
        shell(rect(4, 3.5, 16, 2, cap(S, 1))),
        shell(rect(4, 8, 4, 11, cap(S, 1.5))),
        shell(rect(16, 8, 4, 11, cap(S, 1.5))),
        shell(rect(10, 12, 4, 4, cap(S, 1))),
    ]


@icon("vacuum-gripper", CAT, "Robot wrist with a row of suction cups lifting a flat box",
      tags=["suction gripper", "vacuum cup", "pick and place", "end effector", "robot tool", "packaging"])
def _(S):
    cups = [solid(poly([(x - 1.8, 10), (x + 1.8, 10), (x + 2.5, 13.5), (x - 2.5, 13.5)], closed=True))
            for x in (6, 12, 18)]
    return [
        line(seg(12, 2, 12, 6)),
        shell(rect(3, 6, 18, 3, cap(S, 1))),
        shell(rect(3, 16, 18, 5, cap(S, 2))),
    ] + cups


@icon("robotic-hand", CAT, "Mechanical hand with jointed fingers and a pivot dot on each knuckle",
      tags=["robot hand", "humanoid", "prosthetic", "dexterous", "fingers", "automation"])
def _(S):
    parts = [shell(rect(3, 13, 18, 8, cap(S, 3)))]
    for x, top in ((7, 6), (11, 3.5), (15, 4.5), (19, 7)):
        parts.append(line(seg(x, 13, x, top)))
        parts.append(dot(x, top + 3.8, 1.3))
    return parts


@icon("scara-robot", CAT, "Robot with a short column and two horizontal links hinged end to end carrying a vertical spindle",
      tags=["scara", "assembly robot", "selective compliance arm", "pick and place", "factory", "automation"])
def _(S):
    return [
        shell(rect(3, 8, 5, 13, cap(S, 1.5))),
        shell(rect(3, 3, 11, 4, cap(S, 1.5))),
        shell(rect(14, 3, 8, 4, cap(S, 1.5))),
        line(seg(18, 8, 18, 20)),
        dot(14, 5, 1.2),
    ]


@icon("delta-robot", CAT, "Delta robot with a top plate, three thin arms and a small tool plate",
      tags=["parallel robot", "delta", "picker", "food packaging", "high speed", "automation"])
def _(S):
    return [
        shell(rect(3, 2, 18, 3, cap(S, 1))),
        line(seg(4.5, 5, 8.5, 15)), line(seg(12, 5, 12, 15)), line(seg(19.5, 5, 15.5, 15)),
        shell(rect(7, 15, 10, 3, cap(S, 1))),
        line(seg(12, 18, 12, 21.5)),
    ]


@icon("automated-guided-vehicle", CAT, "Low flat robot cart on small wheels carrying a box, with a sensor on the front",
      tags=["agv", "warehouse robot", "autonomous cart", "transport", "logistics", "driverless"])
def _(S):
    return [
        shell(rect(5, 2, 10, 6, cap(S, 2))),
        shell(rect(2, 10, 20, 6, cap(S, 2))),
        dot(19.5, 13, 1),
        dot(6.5, 19.5, 1.9), dot(17.5, 19.5, 1.9),
    ]


@icon("delivery-robot", CAT, "Small six-wheeled box robot with a lid and a flag on a thin antenna",
      tags=["sidewalk robot", "last mile", "courier robot", "autonomous delivery", "food delivery", "rover"])
def _(S):
    return [
        shell(rect(3, 8, 18, 8, cap(S, 2))),
        detail(seg(3, 11.5, 21, 11.5)),
        line(seg(16, 8, 16, 2.5)),
        solid(poly([(16, 2.5), (21, 4), (16, 5.5)], closed=True)),
        dot(6, 19.5, 1.7), dot(12, 19.5, 1.7), dot(18, 19.5, 1.7),
    ]


@icon("robot-dog", CAT, "Four-legged robot with a boxy body, a sensor head and bent legs",
      tags=["quadruped", "legged robot", "inspection robot", "robotic pet", "walking robot", "mobile robot"])
def _(S):
    return [
        shell(rect(3, 6, 14, 6, cap(S, 2))),
        shell(rect(18, 3, 4, 6, cap(S, 1.5))),
        line(poly([(5.5, 12), (4, 16), (5.5, 21)], closed=False, r=S.r)),
        line(poly([(9.5, 12), (8, 16), (9.5, 21)], closed=False, r=S.r)),
        line(poly([(12.5, 12), (14, 16), (12.5, 21)], closed=False, r=S.r)),
        line(poly([(16.5, 12), (18, 16), (16.5, 21)], closed=False, r=S.r)),
    ]


@icon("teach-pendant", CAT, "Handheld robot controller with a screen, keys and a round emergency stop button",
      tags=["robot controller", "pendant", "programming", "cnc", "remote", "handheld"])
def _(S):
    return [
        shell(rect(4, 8, 16, 14, cap(S, 3))),
        Part("dot", rect(7, 11, 10, 4, 0.5)),
        dot(8, 18.5, 1.2), dot(12, 18.5, 1.2), dot(16, 18.5, 1.2),
        dot(16.5, 4.7, 2.3),
    ]


@icon("programmable-logic-controller", CAT, "Rail-mounted controller module with terminal screws top and bottom and status lights",
      tags=["plc", "controller", "automation", "din rail", "control panel", "industrial computer"])
def _(S):
    parts = [shell(rect(3, 2, 18, 16, cap(S, 2))), line(seg(2, 21, 22, 21))]
    for x in (7, 12, 17):
        parts += [dot(x, 5.5, 1), dot(x, 14.5, 1)]
    parts += [dot(8, 10, 1), dot(12, 10, 1)]
    return parts


@icon("proximity-sensor", CAT, "Threaded cylindrical sensor with lock nuts, a rear cable and sensing waves in front",
      tags=["inductive sensor", "detector", "switch", "automation", "sensing", "factory"])
def _(S):
    return [
        shell(rect(4, 7.5, 9, 9, cap(S, 1.5))),
        detail(seg(7.5, 7.5, 7.5, 16.5)), detail(seg(10.5, 7.5, 10.5, 16.5)),
        line(seg(2, 12, 4, 12)),
        line(arc(13.5, 12, 4, -40, 40)), line(arc(13.5, 12, 7, -36, 36)),
    ]


@icon("limit-switch", CAT, "Small box switch with a pivoting lever arm and a roller wheel at its tip",
      tags=["end stop", "roller lever", "position switch", "machine safety", "contact", "automation"])
def _(S):
    return [
        shell(rect(3, 13, 11, 8, cap(S, 2))),
        line(seg(8, 13, 14.5, 8)),
        shell(circle(17, 6, 2.6)),
        dot(8, 16.5, 1),
    ]


@icon("emergency-stop-button", CAT, "Large mushroom-head push button on a round plate",
      tags=["e-stop", "kill switch", "panic button", "machine safety", "red button", "shutdown"])
def _(S):
    if S.name == "line":
        head = "M3 14C3 7 7 4 12 4C17 4 21 7 21 14Z"
    else:
        head = "M3 12.5C3 7 7 4 12 4C17 4 21 7 21 12.5Q21 14 19.5 14H4.5Q3 14 3 12.5Z"
    return [
        shell(head),
        line(seg(12, 14, 12, 17)),
        shell(rect(3, 17, 18, 4, cap(S, 2))),
    ]


@icon("start-stop-buttons", CAT, "Control box with a solid start button marked I above a ring-shaped stop button marked O",
      tags=["start stop", "push buttons", "control station", "motor control", "on off", "industrial panel"])
def _(S):
    return [
        shell(rect(3, 2, 18, 20, cap(S, 3))),
        dot(9, 7.5, 2.8),
        detail(circle(9, 16.5, 2.4)),
        detail(seg(16, 5.5, 16, 9.5)),
        detail(circle(16, 16.5, 1.8)),
    ]


@icon("safety-light-curtain", CAT, "Two vertical posts facing each other with horizontal beams between them",
      tags=["light curtain", "safety barrier", "machine guarding", "optical sensor", "beam", "danger zone"])
def _(S):
    parts = [shell(rect(3, 2, 4, 20, cap(S, 1.5))), shell(rect(17, 2, 4, 20, cap(S, 1.5)))]
    for y in (6, 10, 14, 18):
        parts.append(line(seg(8, y, 16, y)))
    return parts


@icon("rfid-tag", CAT, "Thin card with a coiled antenna around a tiny chip",
      tags=["rfid", "tag", "transponder", "nfc", "tracking", "inventory", "identification"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, cap(S, 3))),
        detail(poly([(17, 13.5), (17, 8), (7, 8), (7, 16), (17, 16)], closed=False, r=S.r)),
        Part("dot", rect(10.5, 10.5, 4, 3, 0.5)),
    ]


@icon("offshore-wind-turbine", CAT, "Three-blade wind turbine on a tall tower standing in waves",
      tags=["wind farm", "sea", "renewable energy", "ocean wind", "green power", "turbine"])
def _(S):
    parts = [line(seg(12, 7, 12, 20))]
    for a in (-90, 30, 150):
        p = pt_on(12, 7, 5.5, a)
        parts.append(line(seg(12, 7, p[0], p[1])))
    parts.append(dot(12, 7, 1.7))
    parts.append(line("M2 20.5q2.5-2 5 0t5 0t5 0t5 0"))
    return parts


@icon("vertical-axis-wind-turbine", CAT, "Tall mast with curved blades bowing out from top and bottom like an eggbeater",
      tags=["darrieus", "eggbeater turbine", "urban wind", "renewable energy", "rotor", "wind power"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 21.5)),
        line(seg(8.5, 6, 15.5, 6)), line(seg(8.5, 16, 15.5, 16)),
        line("M8.5 6C3 8.5 3 13.5 8.5 16"), line("M15.5 6C21 8.5 21 13.5 15.5 16"),
        line(seg(8, 21.5, 16, 21.5)),
    ]


# ============================================================================ power generation and electrical

def rev_ellipse(cx, cy, rx, ry):
    """Ellipse drawn counter-clockwise so it cuts a hole when combined with a clockwise outer ellipse."""
    return (f"M{fmt(cx - rx)} {fmt(cy)}A{fmt(rx)} {fmt(ry)} 0 1 1 {fmt(cx + rx)} {fmt(cy)}"
            f"A{fmt(rx)} {fmt(ry)} 0 1 1 {fmt(cx - rx)} {fmt(cy)}Z")


@icon("solar-power-tower", CAT, "Tall tower with a round receiver on top and tilted mirrors on posts facing it",
      tags=["concentrated solar", "heliostat", "solar thermal", "csp", "renewable energy", "mirror field"])
def _(S):
    parts = [shell(circle(12, 5.5, 3.2)), line(seg(12, 9, 12, 21.5))]
    for cx in (3.8, 8.3):
        parts.append(line(seg(cx - 2.2, 16.3, cx + 2.2, 18.7)))
        parts.append(line(seg(cx, 18.5, cx, 21.5)))
        parts.append(line(seg(24 - cx - 2.2, 18.7, 24 - cx + 2.2, 16.3)))
        parts.append(line(seg(24 - cx, 18.5, 24 - cx, 21.5)))
    return parts


@icon("pelton-wheel", CAT, "Water wheel with cup buckets around its rim and a jet hitting one bucket",
      tags=["hydro turbine", "impulse turbine", "water jet", "hydroelectric", "bucket wheel", "renewable energy"])
def _(S):
    cx, cy = 9.5, 12
    parts = [shell(circle(cx, cy, 3.3)), dot(cx, cy, 1.2)]
    for i in range(6):
        p = pt_on(cx, cy, 5.9, i * 60)
        if S.name == "line":
            parts.append(Part("dot", poly(regular(p[0], p[1], 2.3, 4, start=i * 60 + 45), closed=True)))
        else:
            parts.append(dot(p[0], p[1], 1.9))
    parts.append(solid(poly([(22.5, 9.8), (22.5, 14.2), (18.7, 12)], closed=True)))
    return parts


@icon("tidal-turbine", CAT, "Two-blade turbine on a pillar standing on the seabed beneath wave lines",
      tags=["tidal energy", "underwater turbine", "marine power", "ocean energy", "renewable energy", "seabed"])
def _(S):
    return [
        line("M2 4q2.5-2 5 0t5 0t5 0t5 0"),
        line(seg(5, 8, 5, 18)),
        shell(rect(7, 10, 11, 4, cap(S, 1.5))),
        line(seg(14, 14, 14, 21)), line(seg(9, 21, 19, 21)),
    ]


@icon("geothermal-plant", CAT, "Low power plant building with steam plumes and pipes running down into the ground",
      tags=["geothermal", "steam", "heat from earth", "renewable energy", "power station", "vents"])
def _(S):
    return [
        shell(rect(3, 9, 14, 7, cap(S, 2))),
        line("M7 7C5 5.5 9 4.5 7 2.5"), line("M13 7C11 5.5 15 4.5 13 2.5"),
        line(seg(2, 18, 22, 18)),
        line(seg(8, 18, 8, 22)), line(seg(13, 18, 13, 22)),
        line(poly([(19, 15), (19, 6.5), (21.5, 6.5), (21.5, 15)], closed=False, r=S.r)),
    ]


@icon("nuclear-reactor", CAT, "Domed containment building with a radiation trefoil on its front",
      tags=["nuclear power", "reactor", "containment dome", "atomic energy", "power plant", "fission"])
def _(S):
    return [
        shell("M3 21V14A9 9 0 0 1 21 14V21Z" if S.name == "line" else "M3 19V14A9 9 0 0 1 21 14V19Q21 21 19 21H5Q3 21 3 19Z"),
    ] + trefoil(12, 14.6, 4.1)


@icon("nuclear-fuel-rods", CAT, "Bundle of long thin rods held together by two horizontal grid spacers",
      tags=["fuel assembly", "nuclear fuel", "reactor core", "uranium", "fission", "atomic"])
def _(S):
    parts = [line(seg(x, 3, x, 21)) for x in (6, 10, 14, 18)]
    parts += [shell(rect(3, 7, 18, 2, cap(S, 1))), shell(rect(3, 15, 18, 2, cap(S, 1)))]
    return parts


@icon("tokamak", CAT, "Donut-shaped fusion chamber seen at an angle, wrapped in evenly spaced coils",
      tags=["fusion reactor", "plasma", "magnetic confinement", "torus", "stellarator", "fusion energy"])
def _(S):
    parts = [shell(ellipse(12, 12, 10, 6.5) + rev_ellipse(12, 12, 4.2, 2.3))]
    n = 8 if S.name == "line" else 6
    for k in range(n):
        t = math.radians(180 / n + 360 / n * k)
        k0, k1 = 0, 1
        a = (12 + (4.2 + 5.8 * k0) * math.cos(t), 12 + (2.3 + 4.2 * k0) * math.sin(t))
        b = (12 + (4.2 + 5.8 * k1) * math.cos(t), 12 + (2.3 + 4.2 * k1) * math.sin(t))
        parts.append(detail(seg(a[0], a[1], b[0], b[1])))
    return parts


@icon("hydrogen-fuel-cell", CAT, "Stack of plates between two thick end plates with a gas arrow going in and a water drop coming out",
      tags=["fuel cell", "hydrogen power", "pem", "electrolyte stack", "clean energy", "zero emission"])
def _(S):
    return [
        shell(rect(4, 10, 3, 11, cap(S, 1.5))), shell(rect(17, 10, 3, 11, cap(S, 1.5))),
        line(seg(10, 10, 10, 21)), line(seg(14, 10, 14, 21)),
        line(seg(5.5, 2, 5.5, 7)),
        line(poly([(3, 5), (5.5, 7.5), (8, 5)], closed=False, r=S.r)),
        solid("M18.5 2.5C17.3 4.2 16.3 5 16.3 6.3A2.2 2.2 0 0 0 20.7 6.3C20.7 5 19.7 4.2 18.5 2.5Z"),
    ]


@icon("hydrogen-tank", CAT, "Tall capsule-shaped pressure tank with a valve on top and the letter H on its side",
      tags=["h2", "gas cylinder", "pressure vessel", "hydrogen storage", "fuel tank", "clean fuel"])
def _(S):
    return [
        shell(rect(5, 5, 14, 16, 7)),
        line(seg(12, 5, 12, 2.5)), line(seg(9.5, 2.5, 14.5, 2.5)),
        detail(seg(9.5, 9, 9.5, 16)), detail(seg(14.5, 9, 14.5, 16)), detail(seg(9.5, 12.5, 14.5, 12.5)),
    ]


@icon("grid-battery-storage", CAT, "Container-sized box with a vent grille on one end and a battery symbol on its side",
      tags=["energy storage", "bess", "battery container", "grid scale", "megapack style", "power storage"])
def _(S):
    return [
        shell(rect(2, 6, 20, 12, cap(S, 3))),
        detail(seg(7.5, 6, 7.5, 18)),
        detail(seg(3, 10, 6, 10)), detail(seg(3, 14, 6, 14)),
        detail(rect(11, 9, 7, 6, cap(S, 1))),
        Part("dot", rect(18.6, 11, 1.4, 2)),
    ]


@icon("biofuel", CAT, "Oil drop with a small leaf growing from its side",
      tags=["biodiesel", "ethanol", "renewable fuel", "green fuel", "plant oil", "bioenergy"])
def _(S):
    if S.name == "line":
        drop = "M9 3C9 3 3 9.5 3 14.5a6 6 0 0 0 12 0C15 9.5 9 3 9 3Z"
    else:
        drop = "M9 3.8Q10 3.8 10.8 4.8C13 7.5 15 10.8 15 14.5A6 6 0 0 1 3 14.5C3 10.8 5 7.5 7.2 4.8Q8 3.8 9 3.8Z"
    return [
        shell(drop),
        shell("M15 16C15 11.5 17.5 8.5 21 8.5C21 13 18.5 16 15 16Z"),
    ]


@icon("power-transformer", CAT, "Utility transformer tank with cooling fins on both sides and three bushings on top",
      tags=["transformer", "high voltage", "electric utility", "grid equipment", "radiator", "power station"])
def _(S):
    parts = [shell(rect(6, 9, 12, 12, cap(S, 2))),
             line(seg(3, 11, 3, 19)), line(seg(21, 11, 21, 19))]
    for x in (8.5, 12, 15.5):
        parts += [line(seg(x, 9, x, 5)), dot(x, 4, 1.4)]
    return parts


@icon("electrical-substation", CAT, "Fenced yard with two gantry posts, a transformer between them and wires strung overhead",
      tags=["substation", "switchyard", "grid", "high voltage", "electric utility", "power lines"])
def _(S):
    return [
        line(seg(4, 21, 4, 5)), line(seg(2, 5, 6.5, 5)),
        line(seg(20, 21, 20, 5)), line(seg(17.5, 5, 22, 5)),
        line("M5 6.5Q12 11.5 19 6.5"),
        shell(rect(8, 13, 8, 7, cap(S, 2))),
    ]


@icon("ceramic-insulator", CAT, "Vertical string of ribbed disc insulators hanging from a bracket with a clamp at the bottom",
      tags=["insulator string", "power line", "high voltage", "porcelain", "transmission", "pylon"])
def _(S):
    parts = [line(seg(12, 2.5, 12, 19)), line(seg(8, 2.5, 16, 2.5))]
    for y in (6.5, 11, 15.5):
        parts.append(shell(rect(5.5, y - 1, 13, 2, cap(S, 1))))
    parts.append(dot(12, 20, 2))
    return parts


@icon("knife-switch", CAT, "Hinged metal blade lever on an insulating base, swinging toward a spring clip",
      tags=["disconnect switch", "blade switch", "isolator", "open circuit", "electric switch", "power"])
def _(S):
    return [
        shell(rect(2, 17, 20, 4, cap(S, 1.5))),
        line(seg(5, 17, 5, 12)),
        line(seg(5, 12, 15, 4.5)),
        dot(16.3, 3.6, 1.6),
        line(seg(16.5, 17, 16.5, 12)), line(seg(20, 17, 20, 12)),
    ]


@icon("three-phase-plug", CAT, "Round industrial plug with a thick collar and five pins arranged in a circle",
      tags=["industrial plug", "three phase", "cee plug", "power connector", "400v", "socket", "electrical"])
def _(S):
    parts = [shell(circle(12, 12, 9.5)), detail(circle(12, 12, 6.8))]
    for i in range(5):
        p = pt_on(12, 12, 3.6, -90 + i * 72)
        if S.name == "line":
            parts.append(Part("dot", poly(regular(p[0], p[1], 1.7, 4, start=45), closed=True)))
        else:
            parts.append(dot(p[0], p[1], 1.3))
    return parts


@icon("tesla-coil", CAT, "Tall coil tower topped by a ring with jagged lightning arcing out",
      tags=["high voltage", "lightning", "spark", "physics demo", "resonant transformer", "electricity"])
def _(S):
    parts = [
        shell(ellipse(12, 5, 4.5, 1.8)),
        shell(rect(9.5, 10, 5, 9, cap(S, 1.5))),
        detail(seg(9.5, 13, 14.5, 13)), detail(seg(9.5, 16, 14.5, 16)),
        line(seg(6, 21, 18, 21)),
    ]
    for sx in (1, -1):
        pts = [(7.6, 4.6), (5.4, 6.4), (5.6, 3.6), (2.6, 4.8)]
        parts.append(line(poly([(12 + sx * (12 - x), y) for x, y in pts], closed=False, r=0)))
    return parts


@icon("geiger-counter", CAT, "Handheld box with a dial meter, connected by a cable to a wand probe",
      tags=["radiation detector", "dosimeter", "radioactivity", "nuclear", "survey meter", "measurement"])
def _(S):
    return [
        shell(rect(2, 9, 11, 13, cap(S, 3))),
        detail("M5 17.5a3 3 0 0 1 6 0"),
        detail(seg(8, 17.5, 9.6, 14)) if False else detail(seg(8, 17.5, 8, 13.5)),
        shell(rect(15, 3, 6, 11, cap(S, 2))),
        line(poly([(13, 19), (18, 19), (18, 14)], closed=False, r=S.r)),
    ]


@icon("thermocouple", CAT, "Thin probe with two wires twisted together at the tip and a flat two-pin plug at the other end",
      tags=["temperature probe", "sensor", "type k", "thermometer", "temperature measurement", "wires"])
def _(S):
    return [
        dot(2.8, 12, 1.6),
        line(seg(2.8, 12, 8, 12)),
        line("M8 12C10 9 12 15 14 12"), line("M8 12C10 15 12 9 14 12"),
        line(seg(14, 12, 16, 12)),
        shell(rect(16, 8, 4, 8, cap(S, 1.5))),
        line(seg(20, 10, 22.5, 10)), line(seg(20, 14, 22.5, 14)),
    ]


@icon("mine-headframe", CAT, "Tall A-frame steel tower with two wheels on top over a vertical shaft",
      tags=["winding tower", "pithead", "colliery", "mining", "shaft", "coal mine", "hoist"])
def _(S):
    return [
        line(seg(4, 21, 9.3, 7.5)), line(seg(20, 21, 14.7, 7.5)),
        line(seg(6.6, 14.5, 17.4, 14.5)),
        shell(circle(9.3, 5.5, 2)), shell(circle(14.7, 5.5, 2)),
        solid(rect(10, 16.5, 4, 4.5)),
    ]


@icon("miner-safety-lamp", CAT, "Old flame safety lamp with a mesh cage, a solid base and a ring on top",
      tags=["davy lamp", "flame lamp", "mining", "coal mine", "lantern", "gas detection"])
def _(S):
    return [
        shell(circle(12, 4, 1.4)),
        shell(rect(7, 8, 10, 8, cap(S, 2))),
        detail(seg(12, 8, 12, 16)), detail(seg(7, 12, 17, 12)),
        shell(rect(6, 17, 12, 4, cap(S, 1.5))),
    ]


@icon("sluice-box", CAT, "Sloping trough with riffle bars across its floor and water drops falling on it",
      tags=["gold panning", "placer mining", "prospecting", "riffles", "gold mining", "water channel"])
def _(S):
    return [
        shell(poly([(2, 9), (22, 16), (22, 20), (2, 13)], closed=True, r=S.r * 0.5)),
        detail(seg(7, 10.6, 7, 14.6)), detail(seg(12, 12.4, 12, 16.4)), detail(seg(17, 14.1, 17, 18.1)),
        dot(5, 4.5, 1.2), dot(11, 6.5, 1.2), dot(17, 9, 1.2),
    ]


@icon("bucket-wheel-excavator", CAT, "Crawler machine with a long boom carrying a large wheel of buckets at its tip",
      tags=["mining machine", "surface mining", "lignite", "digger", "heavy equipment", "earth moving"])
def _(S):
    cx, cy = 16.5, 8.3
    parts = [shell(circle(cx, cy, 2.8)), shell(rect(2, 17, 14, 4, cap(S, 2))), line(seg(6, 17, 13.8, 10.4))]
    for i in range(8):
        p = pt_on(cx, cy, 5, i * 45 + 22)
        parts.append(dot(p[0], p[1], 1.1))
    return parts


@icon("metal-ingot", CAT, "Stack of three trapezoid metal bars, two below and one on top",
      tags=["gold bars", "steel", "aluminium", "smelting", "bullion", "foundry", "metal"])
def _(S):
    return [
        shell(poly([(2, 21), (3.5, 15), (9, 15), (10.5, 21)], closed=True, r=S.r * 0.7)),
        shell(poly([(13.5, 21), (15, 15), (20.5, 15), (22, 21)], closed=True, r=S.r * 0.7)),
        shell(poly([(7.3, 12), (8.8, 6), (15.2, 6), (16.7, 12)], closed=True, r=S.r * 0.7)),
    ]


@icon("pump-jack", CAT, "Nodding oil pump with a walking beam on an A-frame, a horse head and a crank wheel",
      tags=["oil well", "nodding donkey", "beam pump", "oil field", "petroleum", "rocking pump"])
def _(S):
    return [
        line(seg(3.5, 9.5, 19, 5.5)),
        line("M3.6 9.5C2 12 3 13.5 5 14"), line(seg(5, 14, 5, 21.5)),
        line(seg(8, 21.5, 11.2, 7.6)), line(seg(14.4, 21.5, 11.2, 7.6)),
        line(seg(19, 6, 19, 11.5)),
        shell(circle(19, 15, 2.5)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("offshore-oil-platform", CAT, "Platform deck on tall legs standing in water with a derrick and a flare boom",
      tags=["oil rig", "drilling platform", "north sea", "petroleum", "offshore drilling", "gas flare"])
def _(S):
    return [
        shell(rect(3, 12, 18, 3, cap(S, 1))),
        line(seg(7, 15, 7, 21)), line(seg(17, 15, 17, 21)),
        line("M2 18.5q2.5-2 5 0t5 0t5 0t5 0"),
        line(poly([(6.5, 12), (9.5, 4.5), (12.5, 12)], closed=False, r=S.r * 0.5)),
        line(seg(18, 12, 20, 6)), dot(20.4, 4.6, 1.5),
    ]


@icon("wellhead", CAT, "Valve stack on a pipe rising from the ground with handwheels branching to the sides",
      tags=["christmas tree", "oil well", "gas well", "valve assembly", "drilling", "petroleum"])
def _(S):
    return [
        line(seg(12, 3, 12, 21)), line(seg(10, 3, 14, 3)),
        line(seg(6, 8, 18, 8)),
        shell(circle(4.6, 8, 1.6)), shell(circle(19.4, 8, 1.6)),
        line(seg(12, 13, 17, 13)), shell(circle(19.4, 13, 1.6)),
        solid(poly([(12, 15), (14.8, 18), (12, 21), (9.2, 18)], closed=True)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("tricone-drill-bit", CAT, "Drill bit with three toothed cones at the bottom of a threaded shank",
      tags=["rock bit", "drilling", "roller cone", "oil drilling", "mining drill", "borehole"])
def _(S):
    return [
        shell(poly([(9, 2), (15, 2), (15, 8), (20, 8), (20, 12.5), (4, 12.5), (4, 8), (9, 8)], closed=True, r=S.r * 0.6), stroke_miterlimit="1.5"),
        detail(seg(9, 5, 15, 5)),
        shell(poly([(4.5, 13.5), (9.5, 13.5), (6.3, 21)], closed=True, r=S.r * 0.6), stroke_miterlimit="1.5"),
        shell(poly([(9.8, 13.5), (14.2, 13.5), (12, 21.5)], closed=True, r=S.r * 0.6), stroke_miterlimit="1.5"),
        shell(poly([(14.5, 13.5), (19.5, 13.5), (17.7, 21)], closed=True, r=S.r * 0.6), stroke_miterlimit="1.5"),
    ]


@icon("roll-cage", CAT, "Tall wire mesh cage cart with shelves, open sides and four casters",
      tags=["roll container", "warehouse trolley", "cage trolley", "distribution", "retail logistics", "cart"])
def _(S):
    return [
        shell(rect(4, 2, 16, 15, cap(S, 2))),
        detail(seg(4, 7, 20, 7)), detail(seg(4, 12, 20, 12)), detail(seg(12, 2, 12, 17)),
        dot(6.5, 20, 1.7), dot(17.5, 20, 1.7),
    ]


@icon("stacking-bin", CAT, "Open-fronted plastic storage bin with a hand slot in its lip, stacked on a second bin",
      tags=["storage bin", "parts bin", "tote", "crate", "warehouse", "plastic container", "picking bin"])
def _(S):
    return [
        shell(poly([(3, 2.5), (21, 2.5), (20, 10.5), (4, 10.5)], closed=True, r=S.r)),
        shell(poly([(3, 13), (21, 13), (20, 21), (4, 21)], closed=True, r=S.r)),
        Part("dot", rect(9.5, 5.2, 5, 2, 1)),
        Part("dot", rect(9.5, 15.7, 5, 2, 1)),
    ]


# ============================================================================ cargo handling, measuring and process plant

def sector(r, quadrant, cx=12.0, cy=12.0):
    """Quarter disc path: quadrant 0 top-right, 1 top-left, 2 bottom-left, 3 bottom-right."""
    ends = [((cx + r, cy), (cx, cy - r)), ((cx, cy - r), (cx - r, cy)),
            ((cx - r, cy), (cx, cy + r)), ((cx, cy + r), (cx + r, cy))]
    a, b = ends[quadrant]
    return f"M{fmt(cx)} {fmt(cy)}L{fmt(a[0])} {fmt(a[1])}A{fmt(r)} {fmt(r)} 0 0 0 {fmt(b[0])} {fmt(b[1])}Z"


@icon("straddle-carrier", CAT, "Tall narrow frame on wheels carrying a shipping container between its legs",
      tags=["container carrier", "port vehicle", "shipping container", "terminal", "harbour", "intermodal"])
def _(S):
    return [
        line(seg(4, 4, 20, 4)),
        line(seg(4, 4, 4, 18)), line(seg(20, 4, 20, 18)),
        shell(rect(8, 8, 8, 7, cap(S, 1.5))),
        detail(seg(12, 8, 12, 15)),
        dot(4, 20, 2), dot(20, 20, 2),
    ]


@icon("reach-stacker", CAT, "Heavy wheeled vehicle with a long angled boom holding a container from above at its tip",
      tags=["container handler", "port equipment", "terminal vehicle", "lift truck", "shipping", "intermodal"])
def _(S):
    return [
        shell(rect(2, 12, 14, 5, cap(S, 2))),
        shell(rect(3, 8, 5, 3, cap(S, 1))),
        line(seg(8, 12, 17, 5)),
        shell(rect(13.5, 8, 7, 4.5, cap(S, 1.5))),
        dot(6, 20, 2), dot(13, 20, 2),
    ]


@icon("stretch-wrap-roll", CAT, "Roll of clear plastic film on a core with handles, film unwinding to one side",
      tags=["stretch film", "pallet wrap", "shrink wrap", "packaging", "cling film", "shipping"])
def _(S):
    return [
        shell(rect(5, 6, 9, 12, cap(S, 2))),
        line(seg(9.5, 2.5, 9.5, 6)), line(seg(9.5, 18, 9.5, 21.5)),
        shell("M14 8C16.5 6.5 18.5 10 21.5 8.5V19C18.5 20.5 16.5 17 14 18.5"),
    ]


@icon("packing-tape-gun", CAT, "Handheld tape dispenser with a pistol grip, a large tape roll and a serrated cutting edge",
      tags=["tape dispenser", "box sealing", "parcel", "packaging", "shipping", "sealing tape"])
def _(S):
    return [
        shell(circle(9, 8.5, 6)),
        dot(9, 8.5, 1.4),
        shell(poly([(7.5, 15), (13, 15), (12, 22), (7, 22)], closed=True, r=S.r)),
        line(seg(15, 10.5, 18, 10.5)), dot(19, 10.5, 1.6),
        line(poly([(15.5, 16.5), (17, 14.5), (18.5, 16.5), (20, 14.5), (21.5, 16.5)], closed=False, r=0)),
    ]


@icon("this-way-up", CAT, "Packaging handling mark of two upward arrows standing on a base line",
      tags=["fragile", "keep upright", "cargo label", "handling mark", "shipping symbol", "orientation"])
def _(S):
    parts = [line(seg(3, 21.5, 21, 21.5))]
    for x in (7.5, 16.5):
        parts += [line(seg(x, 19, x, 6)), line(poly([(x - 3.5, 9.5), (x, 5.5), (x + 3.5, 9.5)], closed=False, r=S.r))]
    return parts


def _cog_filled():
    from geometry import D, P, ST, U
    from dsl import circle as _c
    body = P(_c(12, 12, 10))
    holes = []
    for q in (1, 3):
        holes.append(D(P(sector(8, q)), ST("M12 4V20M4 12H20", 2, "butt", "miter", 4)))
    return D(body, *holes)


@icon("center-of-gravity", CAT, "Circle divided into four quarters with two opposite quarters filled",
      tags=["centre of gravity", "center of mass", "balance point", "target marker", "load symbol", "physics"],
      aliases=["centre-of-gravity"], filled=_cog_filled)
def _(S):
    r = 8 if S.name == "line" else 7
    return [
        shell(circle(12, 12, 9)),
        detail(seg(12, 3, 12, 21)), detail(seg(3, 12, 21, 12)),
        solid(sector(r, 0)), solid(sector(r, 2)),
    ]


@icon("flow-meter", CAT, "Short pipe section with flanges at both ends and a round dial display on top",
      tags=["flowmeter", "flow sensor", "pipe gauge", "fluid measurement", "water meter", "process instrument"])
def _(S):
    return [
        shell(rect(5, 14, 14, 6, cap(S, 1.5))),
        line(seg(3, 12.5, 3, 21.5)), line(seg(21, 12.5, 21, 21.5)),
        shell(circle(12, 7, 3.6)),
        line(seg(12, 10.6, 12, 14)),
        detail(seg(12, 7, 13.4, 5.6)),
    ]


@icon("u-tube-manometer", CAT, "U-shaped glass tube with liquid standing at different heights in each arm",
      tags=["manometer", "pressure gauge", "liquid column", "differential pressure", "physics lab", "measurement"])
def _(S):
    return [
        shell("M5 3V15A7 7 0 0 0 19 15V3H14V15A2 2 0 0 1 10 15V3Z" if S.name == "line" else
              "M5 4.5V15A7 7 0 0 0 19 15V4.5Q19 3 17.5 3H15.5Q14 3 14 4.5V15A2 2 0 0 1 10 15V4.5Q10 3 8.5 3H6.5Q5 3 5 4.5Z"),
        Part("dot", "M5.5 9H9.5V15A2.5 2.5 0 0 0 14.5 15V6H18.5V15A6.5 6.5 0 0 1 5.5 15Z"),
    ]


@icon("sight-glass", CAT, "Vertical glass tube between two small valves on a tank wall showing a liquid level",
      tags=["level gauge", "gauge glass", "liquid level", "tank level", "boiler", "process instrument"])
def _(S):
    return [
        line(seg(3, 2, 3, 22)),
        line(poly([(3, 4), (12.5, 4), (12.5, 6.5)], closed=False, r=S.r)),
        line(poly([(3, 20), (12.5, 20), (12.5, 17.5)], closed=False, r=S.r)),
        solid(poly([(7, 1.9), (9.5, 4), (7, 6.1), (4.5, 4)], closed=True)),
        solid(poly([(7, 17.9), (9.5, 20), (7, 22.1), (4.5, 20)], closed=True)),
        shell(rect(10, 7, 5, 10, cap(S, 1.5))),
        Part("dot", rect(11, 12, 3, 4)),
    ]


@icon("coordinate-measuring-machine", CAT, "Granite table with a bridge frame over it and a vertical probe ending in a ball tip",
      tags=["cmm", "metrology", "precision measuring", "quality inspection", "probe", "manufacturing"])
def _(S):
    return [
        shell(rect(2, 17, 20, 4, cap(S, 1.5))),
        shell(rect(4, 3, 16, 4, cap(S, 1.5))),
        line(seg(5, 7, 5, 16)), line(seg(19, 7, 19, 16)),
        line(seg(12, 7, 12, 12.6)), dot(12, 13.8, 1.5),
    ]


@icon("circular-knitting-machine", CAT, "Round rack of thread cones above a cylinder, with a knitted fabric tube coming out beneath",
      tags=["knitting", "textile machine", "fabric", "yarn", "weaving", "garment manufacturing"])
def _(S):
    parts = []
    for cx in (6, 12, 18):
        parts.append(shell(poly([(cx - 2.5, 8), (cx - 1.4, 2.5), (cx + 1.4, 2.5), (cx + 2.5, 8)], closed=True, r=S.r * 0.6)))
    parts += [
        shell(rect(4, 10, 16, 4, cap(S, 1.5))),
        shell(rect(7, 14, 10, 7, cap(S, 1.5))),
        detail(seg(12, 15, 12, 21)),
    ]
    return parts


@icon("pick-and-place-machine", CAT, "Circuit board on a bed with a gantry head above it holding a tiny chip on a suction nozzle",
      tags=["smt", "chip mounter", "electronics assembly", "pcb", "surface mount", "gantry"])
def _(S):
    return [
        line(seg(2, 3.5, 22, 3.5)),
        shell(rect(9, 5.5, 6, 4, cap(S, 1.5))),
        line(seg(12, 9.5, 12, 12)),
        solid(rect(10.5, 12, 3, 2)),
        shell(rect(5, 16, 14, 2, cap(S, 1))),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("electric-arc-furnace", CAT, "Round furnace vessel with a domed lid and three thick electrodes through it, with sparks below",
      tags=["steel making", "foundry", "melting", "smelting", "electrodes", "scrap metal", "furnace"])
def _(S):
    parts = [
        shell("M4 13V14A8 6 0 0 0 20 14V13Z"),
        shell("M5 13A7 5 0 0 1 19 13Z"),
    ]
    for x in (8.5, 12, 15.5):
        parts.append(line(seg(x, 2, x, 12)))
    parts += [dot(8.5, 16, 1), dot(12, 17.5, 1), dot(15.5, 16, 1)]
    return parts


@icon("parabolic-trough-collector", CAT, "Curved mirror trough on a stand with a receiver pipe at its focal line",
      tags=["solar thermal", "concentrated solar power", "csp", "mirror", "renewable energy", "solar field"])
def _(S):
    return [
        line("M2.5 5Q12 25 21.5 5"),
        shell(circle(12, 8.5, 1.9)),
        line(seg(12, 14.6, 12, 21)), line(seg(8, 21, 16, 21)),
    ]


@icon("wave-energy-converter", CAT, "Chain of jointed floating tube segments riding over wave lines",
      tags=["wave power", "ocean energy", "pelamis style", "marine renewable", "sea", "floating generator"])
def _(S):
    return [
        shell(rect(2, 9, 5.5, 4, cap(S, 2))),
        shell(rect(9.3, 5.5, 5.5, 4, cap(S, 2))),
        shell(rect(16.5, 9, 5.5, 4, cap(S, 2))),
        line("M2 18q2.5-2 5 0t5 0t5 0t5 0"),
        line("M2 21.5q2.5-2 5 0t5 0t5 0t5 0"),
    ]


@icon("pumped-hydro-storage", CAT, "High reservoir and low reservoir joined by a pipe through a small turbine house",
      tags=["pumped storage", "hydroelectric", "energy storage", "dam", "reservoir", "grid storage"])
def _(S):
    return [
        line(poly([(2, 2.5), (3.5, 8), (10.5, 8), (12, 2.5)], closed=False, r=S.r)),
        line(seg(5, 5.3, 9, 5.3)),
        line(seg(7, 8, 7, 14)),
        shell(rect(3.5, 15, 7, 5, cap(S, 1.5))),
        line(seg(10.5, 17.5, 14, 17.5)),
        line(poly([(13.5, 12.5), (14.5, 20), (21.5, 20), (22, 12.5)], closed=False, r=S.r)),
        line(seg(16, 16, 20, 16)),
    ]


@icon("kaplan-turbine", CAT, "Propeller-like runner with broad blades at the bottom of a vertical shaft",
      tags=["water turbine", "hydropower", "propeller turbine", "runner", "dam", "hydroelectric"])
def _(S):
    return [
        line(seg(12, 2, 12, 9)),
        shell(rect(9.5, 9, 5, 6, cap(S, 2))),
        shell(poly([(9, 10.5), (3, 8), (2.5, 12.5), (9, 14)], closed=True, r=S.r * 0.6)),
        shell(poly([(15, 10.5), (21, 8), (21.5, 12.5), (15, 14)], closed=True, r=S.r * 0.6)),
        shell(poly([(10, 16), (14, 16), (12, 21)], closed=True, r=S.r * 0.6), stroke_miterlimit="1.5"),
    ]


@icon("carbon-capture", CAT, "Chimney with an arrow leading down through ground layers into underground storage",
      tags=["co2 storage", "ccs", "emissions", "sequestration", "climate", "industrial chimney", "net zero"])
def _(S):
    return [
        shell(rect(3, 3, 5, 7, cap(S, 1.5))),
        line(poly([(8, 6), (15, 6), (15, 17)], closed=False, r=S.r)),
        line(poly([(12.5, 14.8), (15, 17.3), (17.5, 14.8)], closed=False, r=S.r)),
        line("M2 12.5q2.5-1.5 5 0t5 0t5 0t5 0"),
        line(poly([(9, 18), (9, 21.5), (21, 21.5), (21, 18)], closed=False, r=S.r)),
    ]


@icon("electrolyzer", CAT, "Tank of water with two electrodes, rising bubbles and two gas pipes leaving the top",
      tags=["electrolysis", "hydrogen production", "green hydrogen", "water splitting", "electrolyser", "gas pipes"])
def _(S):
    return [
        shell(rect(3, 8, 18, 13, cap(S, 2.5))),
        line(poly([(8, 12), (8, 3), (5, 3)], closed=False, r=S.r)),
        line(poly([(16, 12), (16, 3), (19, 3)], closed=False, r=S.r)),
        line(seg(8, 12, 8, 18)), line(seg(16, 12, 16, 18)),
        dot(12, 17, 1.1), dot(11, 13.5, 1.1), dot(13, 11.5, 1.1),
    ]


@icon("wood-pellets", CAT, "Small heap of short cylindrical wood pellets with two loose pellets in front",
      tags=["biomass", "pellet fuel", "heating fuel", "sawdust", "bioenergy", "stove pellets"])
def _(S):
    return [
        shell("M3 15C5 10 9 6 12 6C15 6 19 10 21 15Z"),
        detail(seg(9, 11.5, 11.5, 11.5)), detail(seg(13.5, 9.5, 15.5, 9.5)), detail(seg(14, 12.8, 16.5, 12.8)),
        shell(rect(5, 18, 5, 2, 1)), shell(rect(13.5, 18.5, 5, 2, 1)),
    ]
