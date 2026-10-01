"""TypeIcon Core: industry, batch 3 (heavy plant, machines, sensors and instruments)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "industry"


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def blob(S, x, y, r):
    """Small solid mark: a disc in Rounded, a square in Line."""
    if S.name == "rounded":
        return dot(x, y, r)
    return solid(rect(x - r, y - r, 2 * r, 2 * r))


@icon("spent-fuel-cask", CAT, "Tall ribbed storage cask with a bolted lid, standing on legs above a floor line",
      tags=["nuclear", "fuel cask", "dry cask", "radioactive waste", "storage", "container"])
def _(S):
    return [
        shell(rect(7, 3, 10, 14, rr(S, 4))),
        detail(seg(7, 7, 17, 7)),
        detail(seg(7, 10.5, 17, 10.5)),
        detail(seg(7, 14, 17, 14)),
        line(seg(9.5, 17, 9.5, 21)),
        line(seg(14.5, 17, 14.5, 21)),
        line(seg(4, 21, 20, 21)),
    ]


@icon("solar-tracker", CAT, "Tilted solar panel on a pole with a sun in the corner",
      tags=["solar", "sun tracker", "photovoltaic", "panel", "renewable", "energy"])
def _(S):
    return [
        shell(poly([(3.5, 11), (11, 4.5), (17, 9.5), (9.5, 16)], closed=True, r=S.r)),
        detail(seg(6.25, 13.5, 14, 7)),
        line(seg(13.5, 13.5, 13.5, 21)),
        line(seg(9, 21, 18, 21)),
        dot(19.5, 4.5, 2),
    ]


@icon("power-cable-cross-section", CAT, "Round cut end of a heavy cable with three insulated cores inside an armored ring",
      tags=["cable", "armoured cable", "power cable", "wire", "cross section", "core", "electrical"],
      filled=lambda: U(D(U(P(circle(12, 12, 10))), P(circle(12, 12, 6.5))), *[P(circle(*polar(12, 12, 2.9, a), 1.9)) for a in (-90, 30, 150)]))
def _(S):
    parts = [shell(circle(12, 12, 9)), detail(circle(12, 12, 6.5))]
    for a in (-90, 30, 150):
        x, y = polar(12, 12, 2.8, a)
        parts.append(blob(S, x, y, 1.65))
    return parts


@icon("pipeline-pig", CAT, "Cutaway pipe with a bullet-shaped cleaning plug carrying rubber discs",
      tags=["pig", "pipeline", "pipe cleaning", "inspection gauge", "oil and gas", "plug", "maintenance"])
def _(S):
    return [
        line(seg(2, 4, 22, 4)),
        line(seg(2, 20, 22, 20)),
        shell(poly([(6, 9), (14, 9), (19, 12), (14, 15), (6, 15)], closed=True, r=S.r)),
        line(seg(8.5, 7, 8.5, 17)),
        line(seg(12, 7, 12, 17)),
    ]


@icon("seismic-survey", CAT, "Ground surface with a source and a sensor, wave arcs spreading down to a rock layer",
      tags=["seismic", "geophysics", "exploration", "reflection", "survey", "sound waves", "oil exploration"])
def _(S):
    return [
        line(seg(2, 7, 22, 7)),
        blob(S, 8, 4, 1.6),
        blob(S, 18, 4, 1.6),
        line(arc(8, 7, 3.5, 25, 155)),
        line(arc(8, 7, 7.5, 40, 140)),
        line("M3 21q4.5 -3.5 9 0t9 0"),
    ]


@icon("dragline-excavator", CAT, "Boxy machine house with a long lattice boom and a bucket hanging from cables",
      tags=["dragline", "excavator", "mining", "earthmoving", "boom", "bucket", "open pit"])
def _(S):
    return [
        shell(rect(2, 14, 9, 6, rr(S, 2))),
        shell(poly([(6, 14), (19, 3.5), (21.5, 6.5), (11, 14)], closed=True, r=S.r * 0.4), stroke_miterlimit="3"),
        detail(seg(11.5, 11, 15, 7.5)),
        line(seg(17, 9, 17, 14)),
        shell(poly([(14, 14), (20, 14), (19, 19), (15, 19)], closed=True, r=S.r * 0.6)),
        line(seg(2, 22, 22, 22)),
    ]


@icon("continuous-miner", CAT, "Low tracked mining machine with a toothed cutting drum on an arm at the front",
      tags=["miner", "coal mining", "cutting drum", "underground", "machine", "mine"])
def _(S):
    body = poly([(3, 8), (13, 8), (13, 14), (15, 14), (15, 20), (2, 20), (2, 14), (3, 14)], closed=True, r=S.r * 0.5)
    return [
        shell(body),
        detail(seg(5, 17, 12, 17)),
        line(seg(13, 11, 17, 11)),
        shell(rect(17, 5, 5, 13, rr(S, 2))),
        detail(seg(17, 9, 22, 9)),
        detail(seg(17, 13.5, 22, 13.5)),
    ]


@icon("stamp-mill", CAT, "Three vertical stamps with heavy feet lifted by cams on a horizontal shaft",
      tags=["stamp battery", "ore crushing", "gold mining", "mill", "cam shaft", "crusher"])
def _(S):
    parts = [line(seg(2, 3, 22, 3))]
    for x, lift in ((5, 0), (12, 3), (19, 0)):
        parts.append(blob(S, x, 6.5, 1.75))
        parts.append(line(seg(x, 8.5, x, 15 - lift)))
        parts.append(shell(rect(x - 2, 15 - lift, 4, 5, rr(S, 1.5))))
    parts.append(line(seg(2, 22, 22, 22)))
    return parts


@icon("flotation-cell", CAT, "Square tank with rising bubbles and froth spilling over its front lip",
      tags=["froth flotation", "mineral processing", "ore", "bubbles", "tank", "mining", "concentrate"])
def _(S):
    return [
        shell(rect(4, 9, 16, 12, rr(S, 2))),
        line("M5 9a2 2 0 0 1 4 0a2 2 0 0 1 4 0a2 2 0 0 1 4 0a2 2 0 0 1 4 0"),
        dot(9, 18, 1.25),
        dot(13.5, 15, 1.25),
        dot(9.5, 13.5, 1.25),
        dot(16, 18.5, 1.25),
    ]


@icon("wrapped-pallet", CAT, "Pallet with a tall stack of boxes wrapped in film shown by diagonal lines",
      tags=["stretch wrap", "shrink wrap", "pallet", "freight", "warehouse", "shipping", "load"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 11.5, rr(S, 3.5))),
        detail(seg(5, 9, 11.5, 2.5)),
        detail(seg(6.5, 14, 18, 2.5)),
        detail(seg(13.5, 14, 19, 8.5)),
        shell(rect(3, 17, 18, 4.5, rr(S, 1.5))),
        detail(seg(9, 17, 9, 21.5)),
        detail(seg(15, 17, 15, 21.5)),
    ]


@icon("spiral-conveyor", CAT, "Conveyor track winding in a helix around a central column",
      tags=["helical conveyor", "spiral", "elevator conveyor", "material handling", "logistics", "warehouse"])
def _(S):
    return [
        line(seg(12, 2, 12, 22)),
        line("M4 4C4 7 20 7 20 10"),
        line("M20 10C20 13 4 13 4 16"),
        line("M4 16C4 19 20 19 20 22"),
    ]


@icon("gas-cylinder-trolley", CAT, "Two-wheeled upright cart holding two tall gas cylinders with a handle on top",
      tags=["cylinder cart", "gas bottle", "welding", "oxygen", "acetylene", "trolley", "bottle truck"])
def _(S):
    return [
        shell(rect(5, 5, 6, 10, rr(S, 3))),
        shell(rect(13, 5, 6, 10, rr(S, 3))),
        line(poly([(8, 5), (8, 2), (16, 2), (16, 5)], r=S.r * 0.5)),
        line(seg(3, 18, 21, 18)),
        dot(8, 20.5, 1.6),
        dot(16, 20.5, 1.6),
    ]


@icon("machine-vision-camera", CAT, "Industrial camera with a wide ring light shining down onto a part",
      tags=["vision system", "inspection camera", "quality control", "automation", "ring light", "imaging", "camera"])
def _(S):
    return [
        shell(rect(7, 2.5, 10, 7, rr(S, 2))),
        shell(rect(4, 10, 16, 4, rr(S, 2))),
        line(seg(7.5, 16.5, 7.5, 18.5)),
        line(seg(12, 16.5, 12, 18.5)),
        line(seg(16.5, 16.5, 16.5, 18.5)),
        line(seg(4, 21.5, 20, 21.5)),
    ]


@icon("hexapod-robot", CAT, "Six-legged walking robot from above with a round body and jointed legs",
      tags=["walking robot", "six legs", "legged robot", "insect robot", "robotics", "crawler"])
def _(S):
    legs = []
    for s in (1, -1):
        for pts in ([(9.5, 10), (6, 4.5), (3, 6)], [(8.5, 12), (3, 12), (3, 15)], [(9.5, 14), (6, 19.5), (3, 18)]):
            legs.append(line(poly([(12 + s * (x - 12), y) for x, y in pts], r=S.r * 0.8)))
    body = circle(12, 12, 4) if S.name == "rounded" else poly(regular(12, 12, 4.4, 6, 0), closed=True)
    return legs + [shell(body)]


@icon("pipe-inspection-robot", CAT, "Small tracked robot with a camera light on its front inside a round pipe cross section",
      tags=["pipe crawler", "sewer inspection", "pipeline", "camera robot", "duct", "inspection"],
      filled=lambda: U(D(P(circle(12, 12, 10)), P(circle(12, 12, 7.4))), P(rect(7, 12, 10, 5, 1.5)), P(rect(13.5, 9, 2, 4)), P(circle(14.5, 8.2, 1.9))))
def _(S):
    return [
        shell(circle(12, 12, 9)),
        shell(rect(7, 12, 10, 4.5, rr(S, 2))),
        line(seg(14.5, 9.5, 14.5, 12)),
        blob(S, 14.5, 8, 1.6),
    ]


@icon("telepresence-robot", CAT, "Tall pole on a small wheeled base with a screen showing a face at the top",
      tags=["remote presence", "video robot", "teleconference", "screen robot", "office robot", "remote work"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 9, rr(S, 3))),
        dot(9.5, 5.5, 1),
        dot(14.5, 5.5, 1),
        detail("M9.5 8q2.5 1.5 5 0"),
        line(seg(12, 11.5, 12, 18)),
        shell(rect(6, 18, 12, 3.5, rr(S, 1.75))),
    ]


@icon("rotary-encoder", CAT, "Slotted disc on a shaft turning through a U-shaped sensor fork",
      tags=["encoder", "optical encoder", "position sensor", "shaft", "slotted disc", "motion control", "angle sensor"])
def _(S):
    parts = [shell(circle(10, 12, 7)), dot(10, 12, 1.4)]
    for i in range(6):
        a = i * 60
        parts.append(detail(seg(*polar(10, 12, 3.8, a), *polar(10, 12, 7, a))))
    parts.append(line(poly([(14, 3.5), (20.5, 3.5), (20.5, 20.5), (14, 20.5)], r=S.r)))
    return parts


@icon("air-filter-regulator", CAT, "Three bowl units hanging from a shared manifold with a round gauge on the middle one",
      tags=["pneumatic", "air preparation", "frl", "compressed air", "regulator", "filter", "lubricator"])
def _(S):
    return [
        line(seg(2, 3.5, 22, 3.5)),
        line(seg(4.5, 3.5, 4.5, 7)),
        line(seg(19.5, 3.5, 19.5, 7)),
        line(seg(12, 3.5, 12, 6.5)),
        shell(rect(2.5, 7, 4, 13, rr(S, 2))),
        shell(rect(17.5, 7, 4, 13, rr(S, 2))),
        shell(circle(12, 9.5, 3)),
        shell(rect(10, 14, 4, 6.5, rr(S, 2))),
    ]


@icon("hmi-panel", CAT, "Industrial touchscreen with a thick bezel and a row of buttons below the screen",
      tags=["operator panel", "touch screen", "control panel", "hmi", "human machine interface", "scada", "automation"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, rr(S, 3))),
        detail(rect(5, 6, 14, 6.5, rr(S, 1))),
        dot(7, 16.5, 1.1),
        dot(12, 16.5, 1.1),
        dot(17, 16.5, 1.1),
    ]


@icon("foot-switch", CAT, "Floor pedal switch with a pedal under a curved protective hood and a cable at the back",
      tags=["foot pedal", "pedal switch", "machine control", "safety", "floor switch", "welding pedal"])
def _(S):
    return [
        shell(rect(2, 17, 17, 4, rr(S, 1.75))),
        line(poly([(4, 17), (4, 12), (8, 7.5), (15, 7.5), (19, 12), (19, 17)], r=S.r * 2)),
        solid(poly([(7, 16), (14.5, 11.5), (14.5, 16)], closed=True)),
        line("M19 19h3"),
    ]


@icon("linear-rail", CAT, "Straight profiled rail with a carriage block riding on it and mounting holes along the rail",
      tags=["linear guide", "slide rail", "motion", "cnc", "carriage", "bearing block", "automation"])
def _(S):
    return [
        shell(rect(2, 14, 20, 6, rr(S, 2))),
        shell(rect(7, 4, 10, 10, rr(S, 3))),
        dot(4.75, 17, 1),
        dot(19.25, 17, 1),
    ]


@icon("boxer-engine", CAT, "Front view of a flat engine with cylinders lying out to both sides of a central crankcase",
      tags=["flat engine", "horizontally opposed", "piston engine", "motor", "automotive", "aircraft engine"])
def _(S):
    body = [(2, 8), (9, 8), (9, 3.5), (15, 3.5), (15, 8), (22, 8), (22, 16), (15, 16), (15, 20.5), (9, 20.5), (9, 16), (2, 16)]
    return [
        shell(poly(body, closed=True, r=S.r)),
        detail(seg(5.5, 8, 5.5, 16)),
        detail(seg(18.5, 8, 18.5, 16)),
        dot(12, 12, 1.5),
    ]


@icon("inline-engine", CAT, "Side view of an engine block with four cylinders in a row under a long valve cover",
      tags=["straight four", "combustion engine", "motor", "cylinders", "automotive", "car engine"])
def _(S):
    parts = [shell(rect(3, 9, 18, 11, rr(S, 3))), shell(rect(4, 3, 16, 6, rr(S, 2)))]
    for x in (8, 12, 16):
        parts.append(detail(seg(x, 12, x, 20)))
    return parts


@icon("carburetor", CAT, "Boxy carburetor body with a flared air intake horn on top and a throttle lever at the side",
      tags=["carburettor", "fuel mixing", "engine part", "small engine", "air intake", "throttle"])
def _(S):
    return [
        shell(poly([(7, 2.5), (17, 2.5), (15, 9), (9, 9)], closed=True, r=S.r * 0.6)),
        shell(rect(6, 9, 12, 11, rr(S, 2.5))),
        detail(circle(12, 14.5, 2.2)),
        line(poly([(18, 13), (21, 13), (21, 18)], r=S.r * 0.5)),
    ]


@icon("t-slot-extrusion", CAT, "Square end of an aluminum profile bar with a T-slot on each side and a center hole",
      tags=["aluminium extrusion", "aluminum profile", "v-slot", "framing", "t-slot", "machine frame", "profile bar"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 4))), dot(12, 12, 1.8)]
    parts += [detail("M12 3V7M9 7H15"), detail("M12 21V17M9 17H15"), detail("M3 12H7M7 9V15"), detail("M21 12H17M17 9V15")]
    return parts


def _pipe_end(S, cx, cy):
    return poly(regular(cx, cy, 3.25, 8, 22.5), closed=True) if S.name == "line" else circle(cx, cy, 3.25)


@icon("pipe-stack", CAT, "Pile of pipes seen from their open ends, stacked in a triangle",
      tags=["pipes", "tubes", "stacked pipes", "pipe yard", "plumbing", "tube stock", "inventory"],
      filled=lambda: U(*[D(P(circle(cx, cy, 3.6)), P(circle(cx, cy, 1.3))) for cx, cy in ((12, 6.5), (8.75, 12.2), (15.25, 12.2), (5.5, 17.9), (12, 17.9), (18.5, 17.9))]))
def _(S):
    pts = [(12, 6.5), (8.75, 12.2), (15.25, 12.2), (5.5, 17.9), (12, 17.9), (18.5, 17.9)]
    parts = []
    for cx, cy in pts:
        parts.append(shell(_pipe_end(S, cx, cy)))
        parts.append(blob(S, cx, cy, 0.7))
    return parts


@icon("strain-gauge", CAT, "Small rectangular foil patch with a zigzag sensing grid and two lead wires",
      tags=["load cell", "strain sensor", "foil gauge", "stress", "measurement", "sensor", "engineering test"])
def _(S):
    return [
        shell(rect(2, 4, 15, 16, rr(S, 2.5))),
        detail(poly([(17, 8), (6, 8), (6, 12), (13, 12), (13, 16), (17, 16)], r=S.r * 0.5)),
        line(seg(17, 8, 22, 8)),
        line(seg(17, 16, 22, 16)),
    ]


@icon("borescope", CAT, "Handheld screen unit with a long flexible probe cable ending in a small camera tip",
      tags=["endoscope", "inspection camera", "snake camera", "pipe inspection", "flexible probe", "diagnostic tool"])
def _(S):
    return [
        shell(rect(2, 3, 12, 11, rr(S, 2.5))),
        dot(8, 8.5, 2),
        line("M8 14C8 19 15 14 15 19"),
        line(seg(15, 19, 17, 19)),
        shell(rect(17, 16.5, 4.5, 5, rr(S, 1.5))),
    ]


@icon("thermal-camera", CAT, "Pistol-grip camera with a lens at the front and a warm spot on its screen",
      tags=["infrared camera", "thermography", "heat camera", "inspection", "temperature", "thermal imager"])
def _(S):
    return [
        shell(rect(2, 4, 14, 9, rr(S, 2.5))),
        shell(rect(16, 5.5, 5, 6, rr(S, 1.5))),
        shell(poly([(5, 13), (11.5, 13), (10, 21), (5.5, 21)], closed=True, r=S.r * 0.6)),
        dot(9, 8.5, 2),
    ]


@icon("sound-level-meter", CAT, "Handheld meter with a round foam windscreen on a mic on top and a display below",
      tags=["decibel meter", "noise meter", "db meter", "acoustics", "noise measurement", "audio testing", "spl"])
def _(S):
    return [
        shell(circle(12, 5.5, 3.2)),
        shell(rect(7, 9.5, 10, 12.5, rr(S, 3))),
        detail(rect(9.5, 12, 5, 3.5, rr(S, 0.8))),
        dot(12, 18.5, 1.25),
    ]


@icon("rotameter", CAT, "Tapered upright glass tube with a small float inside and scale marks along its side",
      tags=["flow meter", "flowmeter", "variable area flow meter", "gas flow", "liquid flow", "instrument"])
def _(S):
    return [
        shell(poly([(6.5, 2.5), (17.5, 2.5), (14.5, 21.5), (9.5, 21.5)], closed=True, r=S.r * 0.6)),
        dot(12, 12, 1.75),
        line(seg(19.5, 6, 22, 6)),
        line(seg(19.5, 12, 22, 12)),
        line(seg(19.5, 18, 22, 18)),
    ]


@icon("circular-chart-recorder", CAT, "Round paper chart with a ring and a wavy trace drawn by a pen",
      tags=["chart recorder", "paper chart", "data logger", "temperature recorder", "pen recorder", "instrument", "trace"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(arc(12, 12, 4.5, 180, 360)),
        detail("M6 15.5q2 -3 4 0t4 0t4 0"),
    ]


@icon("tensile-testing-machine", CAT, "Tall test frame with two columns and a dog-bone test piece held between its grips",
      tags=["universal testing machine", "materials testing", "pull test", "laboratory", "strength test", "specimen"])
def _(S):
    dog = [(8.5, 8), (15.5, 8), (15.5, 10.5), (14, 11.5), (14, 14.5), (15.5, 15.5), (15.5, 18), (8.5, 18), (8.5, 15.5), (10, 14.5), (10, 11.5), (8.5, 10.5)]
    return [
        line(seg(2, 21.5, 22, 21.5)),
        line(seg(4, 3, 4, 21.5)),
        line(seg(20, 3, 20, 21.5)),
        shell(rect(3, 2, 18, 4, rr(S, 1.5))),
        line(seg(12, 6, 12, 8)),
        shell(poly(dog, closed=True, r=S.r * 0.4)),
        line(seg(12, 18, 12, 21.5)),
    ]


@icon("caged-ladder", CAT, "Fixed vertical ladder with a safety cage of hoops and bars around it",
      tags=["fall protection", "access ladder", "safety cage", "roof access", "tank ladder", "industrial ladder", "hoops"])
def _(S):
    parts = [line(seg(4.5, 2, 4.5, 22)), line(seg(19.5, 2, 19.5, 22)), line(seg(9.5, 2, 9.5, 22)), line(seg(14.5, 2, 14.5, 22))]
    for y in (8, 16):
        parts.append(line(seg(9.5, y, 14.5, y)))
    for y in (4, 12, 20):
        parts.append(line("M4.5 %d Q12 %d 19.5 %d" % (y - 1, y + 4, y - 1)) if S.name == "rounded" else line(poly([(4.5, y - 1), (12, y + 2), (19.5, y - 1)])))
    return parts


@icon("forestry-harvester", CAT, "Wheeled forestry machine with a boom whose head grips a log between rollers with a saw beneath",
      tags=["timber harvester", "logging machine", "forestry", "tree felling", "wood", "lumber", "processor head"])
def _(S):
    return [
        shell(rect(2, 11, 9, 6, rr(S, 2))),
        shell(circle(5, 20, 2)),
        shell(circle(10, 20, 2)),
        line(poly([(9, 11), (12, 3.5), (17, 3.5)], r=S.r * 0.5)),
        shell(rect(15, 5, 6, 6, rr(S, 1.5))),
        shell(rect(11, 14, 11, 4.5, rr(S, 2))),
        line(seg(18, 11, 18, 14)),
    ]


@icon("bulk-ship-loader", CAT, "Long boom conveyor reaching over a ship hold and pouring bulk material into it",
      tags=["ship loader", "port", "bulk cargo", "grain loading", "coal terminal", "conveyor boom", "harbor"],
      )
def _(S):
    return [
        line(seg(3, 21, 3, 7)),
        line(seg(3, 7, 17, 3.5)),
        dot(17, 9, 1.25),
        dot(18.5, 12.5, 1.25),
        line(poly([(7, 14), (9.5, 20), (20.5, 20), (23, 14)], r=S.r)),
        solid(poly([(10, 14), (15, 10.5), (20, 14)], closed=True)),
    ]


@icon("transformer-windings", CAT, "Square iron core with a coil of wire wound on the left leg and another on the right leg",
      tags=["transformer", "coil", "inductor", "electrical", "primary secondary", "power engineering", "windings"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 3))), shell(rect(8.5, 8.5, 7, 7, rr(S, 1)))]
    for y in (7, 12, 17):
        parts.append(detail(seg(3, y, 8.5, y)))
        parts.append(detail(seg(15.5, y, 21, y)))
    return parts


@icon("squirrel-cage-rotor", CAT, "Cylindrical cage of parallel bars joined by a ring at each end on a central shaft",
      tags=["induction motor", "rotor", "electric motor", "cage rotor", "armature", "motor part", "shaft"])
def _(S):
    return [
        shell(rect(5, 4, 3.5, 16, rr(S, 1.75))),
        shell(rect(15.5, 4, 3.5, 16, rr(S, 1.75))),
        line(seg(8, 8, 16, 8)),
        line(seg(8, 16, 16, 16)),
        line(seg(2, 12, 22, 12)),
    ]


@icon("analog-panel-meter", CAT, "Square panel meter with an arc scale, a needle and a pivot",
      tags=["ammeter", "voltmeter", "dial meter", "gauge", "panel meter", "analog", "measurement"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 4))),
        detail(arc(12, 15, 7, 205, 335)),
        line(seg(12, 15, 15.5, 9)),
        dot(12, 15.5, 1.5),
    ]


def tri(pts):
    """Small solid triangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", poly(pts, closed=True))


@icon("hazard-diamond", CAT, "Diamond divided into four smaller diamonds, each holding a dot for a rating",
      tags=["nfpa", "fire diamond", "hazmat", "chemical hazard", "safety rating", "warning sign", "hazard label"])
def _(S):
    return [
        shell(poly([(12, 2), (22, 12), (12, 22), (2, 12)], closed=True, r=S.r * 1.2)),
        detail(seg(7, 7, 17, 17)),
        detail(seg(17, 7, 7, 17)),
        dot(12, 7.3, 1.1),
        dot(16.7, 12, 1.1),
        dot(12, 16.7, 1.1),
        dot(7.3, 12, 1.1),
    ]


@icon("treadwheel-crane", CAT, "Medieval crane with a large walking wheel, a tower with a jib and a rope running to a hook",
      tags=["human powered crane", "medieval crane", "treadmill crane", "historic machine", "lifting", "hoist", "wooden crane"])
def _(S):
    return [
        shell(circle(7, 15, 6)),
        detail(seg(7, 9, 7, 21)),
        detail(seg(1, 15, 13, 15)),
        line(seg(16, 22, 16, 5)),
        line(seg(16, 5, 22, 8)),
        line(seg(7, 9, 16, 5)),
        line(seg(20.5, 7.3, 20.5, 14)),
        dot(20.5, 16.5, 1.6),
    ]


@icon("carbon-fiber", CAT, "Square patch of woven fabric with an alternating checker weave pattern",
      tags=["carbon fibre", "composite", "woven", "weave", "cfrp", "fabric", "material", "texture"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 3))), detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
             detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15))]
    return parts


@icon("spreader-beam", CAT, "Horizontal beam hung from a crane hook by two slings with a lifting hook at each end below",
      tags=["lifting beam", "crane", "rigging", "hoist", "lifting gear", "sling", "load handling"])
def _(S):
    return [
        dot(12, 3, 1.5),
        line(poly([(5, 9), (12, 3.5), (19, 9)], r=S.r * 0.5)),
        shell(rect(2, 9, 20, 3.5, rr(S, 1.75))),
        line("M5 13v5a2.5 2.5 0 0 0 5 0"),
        line("M19 13v5a2.5 2.5 0 0 1 -5 0"),
    ]


@icon("chain-sling", CAT, "Oval master ring with two chains hanging down, each ending in a hook",
      tags=["lifting chain", "rigging", "crane sling", "hoist", "master link", "lifting gear", "chain"])
def _(S):
    return [
        shell(rect(8.5, 2.5, 7, 5, rr(S, 2.5))),
        line(seg(10.5, 7.5, 6, 16)),
        line(seg(13.5, 7.5, 18, 16)),
        line("M6 16v2.5a2.25 2.25 0 0 0 4.5 0"),
        line("M18 16v2.5a2.25 2.25 0 0 1 -4.5 0"),
    ]


@icon("crane-pendant-control", CAT, "Long control box hanging from a cable with paired up and down arrow buttons and a stop button",
      tags=["pendant", "hoist control", "crane remote", "push button station", "up down buttons", "industrial control"])
def _(S):
    parts = [line(seg(12, 1.5, 12, 4)), shell(rect(6.5, 4, 11, 18, rr(S, 3)))]
    for y in (8, 13.5):
        parts.append(tri([(8, y + 3), (11, y + 3), (9.5, y)]))
        parts.append(tri([(13, y), (16, y), (14.5, y + 3)]))
    parts.append(dot(12, 19, 1.3))
    return parts


@icon("bucket-ladder-dredge", CAT, "Floating barge with a long inclined ladder carrying a chain of buckets down into the water",
      tags=["dredger", "dredging", "gold dredge", "mining barge", "underwater digging", "buckets", "river"])
def _(S):
    hull = [(2, 14), (4, 14), (4, 8), (9, 8), (9, 14), (14, 14), (12, 18.5), (4, 18.5)]
    return [
        shell(poly(hull, closed=True, r=S.r * 0.5)),
        line(seg(11, 11, 21, 17)),
        dot(15, 13.4, 1.4),
        dot(18.5, 15.5, 1.4),
        line("M2 21q2.5 -2.5 5 0t5 0t5 0t5 0"),
    ]


@icon("drill-jumbo", CAT, "Tracked mining rig with two long drill booms reaching forward toward a rock face",
      tags=["drilling rig", "tunnel drilling", "mining", "rock drill", "jumbo", "underground", "blasting"])
def _(S):
    return [
        shell(rect(2, 14, 11, 6, rr(S, 3))),
        shell(rect(3, 7.5, 6, 6.5, rr(S, 1.5))),
        line(seg(9, 9.5, 20, 4)),
        line(seg(9, 11.5, 20, 11.5)),
        line(seg(21.5, 2, 21.5, 14)),
    ]


@icon("car-body-shell", CAT, "Bare car body without wheels or doors resting on a stand",
      tags=["body in white", "car frame", "automotive", "chassis", "car manufacturing", "coachwork", "vehicle body"])
def _(S):
    body = "M2 14V11.5L6 10.5L9 6H16L19 10.5L22 11.5V14H19.5A2.5 2.5 0 0 0 14.5 14H9.5A2.5 2.5 0 0 0 4.5 14Z"
    return [
        shell(body),
        detail(seg(12.5, 6, 12.5, 10.5)),
        line(seg(3.5, 14, 3.5, 21)),
        line(seg(20.5, 14, 20.5, 21)),
        line(seg(2, 21, 22, 21)),
    ]


@icon("crash-test-dummy", CAT, "Seated jointed dummy figure with a target marking on its head and round markings on its joints",
      tags=["vehicle safety", "crash test", "car safety", "impact test", "mannequin", "safety testing", "ncap"])
def _(S):
    return [
        shell(circle(14, 5, 3)),
        dot(14, 5, 1),
        line(seg(12.5, 9, 10, 16)),
        line(seg(10, 16, 18, 16)),
        line(seg(18, 16, 18, 22)),
        line(seg(12, 11, 16, 14)),
        blob(S, 10, 16, 1.6),
        blob(S, 18, 16, 1.6),
    ]


@icon("wind-tunnel", CAT, "Car silhouette inside a rectangular test tunnel with flow lines curving over its roof",
      tags=["aerodynamics", "airflow test", "drag", "automotive testing", "flow visualization", "aerospace test"])
def _(S):
    return [
        line(seg(2, 3, 22, 3)),
        line(seg(2, 21, 22, 21)),
        line("M2.5 10Q12 4.5 21.5 10"),
        shell(poly([(5.5, 19.5), (5.5, 17), (9, 16), (11, 13), (15, 13), (17.5, 16), (18.5, 17), (18.5, 19.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("photolithography", CAT, "Lamp shining down through a patterned mask and a lens onto a wafer below",
      tags=["chip manufacturing", "semiconductor", "lithography", "wafer", "euv", "mask", "microchip fabrication"])
def _(S):
    return [
        dot(12, 3.5, 2),
        line(seg(8, 7, 8, 9.5)),
        line(seg(12, 7, 12, 9.5)),
        line(seg(16, 7, 16, 9.5)),
        line(seg(3, 11.5, 9.5, 11.5)),
        line(seg(14.5, 11.5, 21, 11.5)),
        shell("M7.5 15.5Q12 12.5 16.5 15.5Q12 18.5 7.5 15.5Z", stroke_miterlimit="3"),
        shell(rect(4, 19, 16, 3, rr(S, 1.5))),
    ]


@icon("silicon-ingot", CAT, "Long cylindrical crystal boule with a pointed cone at one end",
      tags=["boule", "wafer", "semiconductor", "crystal", "czochralski", "silicon", "monocrystal"])
def _(S):
    cone = "M2 12L6 7" if S.name == "line" else "M3.2 10.8L6 7"
    tail = "L2 12Z" if S.name == "line" else "L3.2 13.2Q2 12 3.2 10.8Z"
    return [
        shell(cone + "H19A2.5 5 0 0 1 19 17H6" + tail, stroke_miterlimit="3"),
        detail("M19 7A2.5 5 0 0 0 19 17"),
        detail(seg(10, 7, 10, 17)),
    ]


@icon("baling-press", CAT, "Tall machine with a press plate squeezing cardboard into a strapped cube bale",
      tags=["baler", "cardboard baler", "recycling", "compactor", "waste", "bale", "compress"])
def _(S):
    return [
        line(seg(3, 5, 3, 22)),
        line(seg(21, 5, 21, 22)),
        shell(rect(2, 2, 20, 3, rr(S, 1.5))),
        line(seg(12, 5, 12, 9)),
        shell(rect(6, 9, 12, 2.5, rr(S, 1))),
        shell(rect(6, 13.5, 12, 8, rr(S, 2))),
        detail(seg(10, 13.5, 10, 21.5)),
        detail(seg(14, 13.5, 14, 21.5)),
    ]


@icon("rail-bogie", CAT, "Rail wheel truck from the side with two wheels, a frame above and coil springs over the axles",
      tags=["railway", "train wheels", "wheelset", "truck", "rolling stock", "suspension", "locomotive"])
def _(S):
    return [
        shell(rect(3, 3.5, 18, 4, rr(S, 2))),
        line(poly([(7, 7.5), (9.5, 8.8), (4.5, 10.6), (7, 12)])),
        line(poly([(17, 7.5), (19.5, 8.8), (14.5, 10.6), (17, 12)])),
        shell(circle(7, 17, 3.5)),
        shell(circle(17, 17, 3.5)),
        dot(7, 17, 1),
        dot(17, 17, 1),
        line(seg(2, 22, 22, 22)),
    ]


@icon("savonius-wind-turbine", CAT, "Vertical rotor made of two half cylinders offset like an S, on a short mast",
      tags=["vertical axis wind turbine", "vawt", "wind power", "renewable energy", "rotor", "wind generator"])
def _(S):
    if S.name == "line":
        a = poly([(12, 3), (9, 3), (6.5, 7.5), (9, 12), (12, 12)], closed=True)
        b = poly([(12, 8), (15, 8), (17.5, 12.5), (15, 17), (12, 17)], closed=True)
    else:
        a = "M12 3H10A5 4.5 0 0 0 10 12H12Z"
        b = "M12 8H14A5 4.5 0 0 1 14 17H12Z"
    return [shell(a), shell(b), line(seg(12, 17, 12, 22)), line(seg(8, 22, 16, 22))]


@icon("noria", CAT, "Large water wheel with pots on its rim lifting water from a river into a raised channel",
      tags=["water wheel", "irrigation", "historic machine", "hama", "water lifting", "pots", "river"])
def _(S):
    parts = [shell(circle(11, 12.5, 6)), detail(seg(11, 6.5, 11, 18.5)), detail(seg(5, 12.5, 17, 12.5))]
    for i in range(8):
        x, y = polar(11, 12.5, 7.9, 22.5 + i * 45)
        parts.append(blob(S, x, y, 1.3))
    parts.append(line(poly([(17, 3), (22, 3)])))
    parts.append(line("M2 22q2.5 -2 5 0t5 0t5 0t5 0"))
    return parts


@icon("peristaltic-pump", CAT, "Round rotor with three rollers pressing a U-shaped tube against a curved housing",
      tags=["tube pump", "hose pump", "dosing pump", "laboratory", "medical pump", "rollers", "fluid"],
      filled=lambda: U(D(P(circle(12, 12, 10)), P(circle(12, 12, 8.3))),
                       ST("M5.5 6V12A6.5 6.5 0 0 0 18.5 12V6", 2.2, "butt", "miter", 4),
                       *[P(circle(*polar(12, 12, 3.6, a), 1.7)) for a in (90, 210, 330)], P(circle(12, 12, 1.8))))
def _(S):
    body = circle(12, 12, 9) if S.name == "rounded" else poly(regular(12, 12, 9.4, 8, 22.5), closed=True)
    parts = [shell(body), detail("M5.5 6V12A6.5 6.5 0 0 0 18.5 12V6"), dot(12, 12, 1.4)]
    for a in (90, 210, 330):
        x, y = polar(12, 12, 4.2, a)
        parts.append(blob(S, x, y, 1.3))
    return parts


@icon("turbine-blade", CAT, "Single twisted turbine blade on a fir tree shaped root",
      tags=["gas turbine", "jet engine", "aerofoil", "airfoil", "fan blade", "power plant", "aerospace"])
def _(S):
    pts = [(11, 2.5), (16, 8), (15.5, 13.5), (16.8, 15.5), (15.5, 17), (17, 19), (14.8, 21.5), (9.2, 21.5), (7, 19), (8.5, 17), (7.2, 15.5), (8.5, 13.5), (8, 8)]
    return [shell(poly(pts, closed=True, r=S.r)), detail("M11.5 6L12.5 13.5")]


@icon("overhead-bridge-crane", CAT, "Bridge beam spanning two high runway walls with a hoist and hook hanging from its middle",
      tags=["gantry crane", "factory crane", "eot crane", "hoist", "workshop", "lifting", "industrial crane"])
def _(S):
    return [
        line(seg(2.5, 3, 2.5, 22)),
        line(seg(21.5, 3, 21.5, 22)),
        shell(rect(2.5, 6, 19, 3.5, rr(S, 1.75))),
        shell(rect(9, 9.5, 6, 4, rr(S, 1.5))),
        line(seg(12, 13.5, 12, 17)),
        line("M12 17v2.5a2 2 0 0 0 4 0"),
    ]


@icon("cryogenic-tank", CAT, "Tall slim vertical tank with frost lines beside a bank of vaporizer tubes",
      tags=["lng tank", "liquid nitrogen", "cryo", "dewar", "vaporizer", "industrial gas", "storage tank"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 8, 18.5, rr(S, 4))),
        detail(seg(2.5, 8, 10.5, 8)),
        detail(seg(2.5, 13, 10.5, 13)),
        line(seg(14.5, 6, 14.5, 19)),
        line(seg(18, 6, 18, 19)),
        line(seg(21.5, 6, 21.5, 19)),
        line(seg(10.5, 19.5, 21.5, 19.5)),
    ]


@icon("photoelectric-sensor", CAT, "Small box sensor sending a dashed beam across to a square reflector",
      tags=["light barrier", "proximity sensor", "optical sensor", "reflector", "retro reflective", "automation", "beam sensor"])
def _(S):
    return [
        shell(rect(2, 7, 6.5, 10, rr(S, 2))),
        dot(5.25, 12, 1.2),
        line(seg(10.5, 12, 12.5, 12)),
        line(seg(14, 12, 16, 12)),
        shell(rect(18.5, 7, 3, 10, rr(S, 1))),
    ]


@icon("ultrasonic-sensor", CAT, "Small circuit board with two round mesh transducer eyes side by side",
      tags=["distance sensor", "sonar", "range finder", "hobby electronics", "echo sensor", "proximity", "electronics"],
      filled=lambda: U(D(P(rect(1, 4, 22, 16, 4)), P(circle(7.5, 12, 4.2)), P(circle(16.5, 12, 4.2))),
                       P(circle(7.5, 12, 2.4)), P(circle(16.5, 12, 2.4))))
def _(S):
    return [
        shell(rect(2, 5, 20, 14, rr(S, 3))),
        shell(circle(7.5, 12, 3)),
        shell(circle(16.5, 12, 3)),
        blob(S, 7.5, 12, 0.9),
        blob(S, 16.5, 12, 0.9),
    ]


@icon("lidar-sensor", CAT, "Short cylindrical puck sensor with a window band and beam arcs spreading out from its sides",
      tags=["laser scanner", "range sensor", "autonomous vehicle", "3d scanning", "mapping", "time of flight", "robotics"])
def _(S):
    return [
        shell(rect(8, 6.5, 8, 11, rr(S, 2))),
        detail(seg(8, 12, 16, 12)),
        line(arc(12, 12, 6.8, 150, 210)),
        line(arc(12, 12, 10, 150, 210)),
        line(arc(12, 12, 6.8, 330, 30)),
        line(arc(12, 12, 10, 330, 30)),
    ]


@icon("wind-up-key", CAT, "Clockwork wind-up key with a figure-eight bow and a short shaft",
      tags=["clockwork", "toy key", "winding key", "mechanical toy", "music box", "mechanism", "wind up"])
def _(S):
    def lobe(cx):
        return circle(cx, 8, 3.2) if S.name == "rounded" else poly(regular(cx, 8, 3.4, 8, 22.5), closed=True)
    return [
        shell(lobe(7)),
        shell(lobe(17)),
        line(seg(10.2, 8, 13.8, 8)),
        shell(rect(10, 12, 4, 10, rr(S, 1.5))),
    ]


@icon("spiral-spring", CAT, "Flat metal strip coiled into a spiral with a hooked outer end",
      tags=["clock spring", "hairspring", "coil", "power spring", "mainspring", "tension", "mechanical"])
def _(S):
    return [
        line("M12 11A1 1 0 0 1 14 11A3 3 0 0 1 8 11A5 5 0 0 1 18 11A8 8 0 0 1 2 11"),
        line(poly([(2, 11), (2, 7), (5, 7)], r=S.r * 0.6)),
    ]


@icon("oil-gusher", CAT, "Lattice oil derrick with a fountain of oil spraying up from its top",
      tags=["oil well", "gusher", "petroleum", "drilling", "crude oil", "spray", "oil field"])
def _(S):
    return [
        shell(poly([(6.5, 22), (10.5, 10), (13.5, 10), (17.5, 22)], closed=True, r=S.r * 0.5)),
        detail(seg(8, 17.5, 16, 17.5)),
        line(seg(12, 10, 12, 2.5)),
        line("M12 9C12 4 7 3 4.5 6"),
        line("M12 9C12 4 17 3 19.5 6"),
        dot(3.5, 11, 1.25),
        dot(20.5, 11, 1.25),
    ]


@icon("stepper-motor", CAT, "Square-bodied motor seen from the front with a round shaft and a wire bundle out the side",
      tags=["stepping motor", "nema", "cnc", "3d printer", "actuator", "electric motor", "motion control"],
      filled=lambda: U(D(P(rect(1, 1.5, 18, 18, 3.5)), P(circle(10, 10.5, 4.8)), *[P(circle(x, y, 1)) for x, y in ((5, 5.5), (15, 5.5), (5, 15.5), (15, 15.5))]),
                       P(circle(10, 10.5, 3)), ST("M18 14H22V21", 2.5, "butt", "miter", 4)))
def _(S):
    return [
        shell(rect(2, 2.5, 16, 16, rr(S, 3))),
        shell(circle(10, 10.5, 3.3)),
        dot(10, 10.5, 1),
        dot(5.5, 6, 0.9),
        dot(14.5, 6, 0.9),
        dot(5.5, 15, 0.9),
        dot(14.5, 15, 0.9),
        line(poly([(18, 14), (22, 14), (22, 21)], r=S.r * 0.6)),
    ]


@icon("brushless-motor", CAT, "Short wide motor can with slots showing the windings and a shaft on top",
      tags=["bldc", "drone motor", "electric motor", "outrunner", "rc motor", "copper windings", "rotor"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 8)),
        shell(rect(3, 8, 18, 12, rr(S, 4))),
        detail(seg(8, 12, 8, 20)),
        detail(seg(12, 12, 12, 20)),
        detail(seg(16, 12, 16, 20)),
    ]


@icon("dynamo", CAT, "Vintage generator with a horseshoe magnet frame around a turning armature with a belt pulley",
      tags=["generator", "horseshoe magnet", "vintage generator", "armature", "electricity", "electromagnetic", "faraday"])
def _(S):
    return [
        shell("M7 4H14A8 8 0 0 1 14 20H7V15H14A3 3 0 0 0 14 9H7Z"),
        line(seg(3.5, 12, 12, 12)),
        dot(12, 12, 1.4),
        dot(3.5, 12, 2),
    ]


@icon("steam-whistle", CAT, "Brass whistle with a bell cylinder on a valve with a pull lever and a puff of steam above",
      tags=["train whistle", "steam engine", "locomotive", "factory whistle", "steam", "signal", "valve"])
def _(S):
    return [
        line("M9.5 5Q8 3.5 9.5 2"),
        line("M14.5 5Q16 3.5 14.5 2"),
        shell(rect(9, 7, 6, 9, rr(S, 2))),
        detail(seg(9, 11, 15, 11)),
        shell(rect(7.5, 16, 9, 4.5, rr(S, 2))),
        line(poly([(16.5, 18.25), (20, 18.25), (20, 22)], r=S.r * 0.6)),
    ]


@icon("gear-puller", CAT, "Three-jawed style puller with a central forcing screw and hex head gripping the edge of a gear",
      tags=["bearing puller", "pulley puller", "extractor", "mechanic", "garage tool", "repair", "removal tool"])
def _(S):
    return [
        shell(poly(regular(12, 4.3, 2.6, 6, 0), closed=True, r=S.r * 0.5)),
        line(seg(12, 6.9, 12, 13)),
        line(poly([(7.5, 18.5), (4.5, 18.5), (4.5, 9.5), (19.5, 9.5), (19.5, 18.5), (16.5, 18.5)], r=S.r)),
        shell(circle(12, 17, 3)),
    ]


@icon("two-post-lift", CAT, "Two tall posts with lifting arms holding a car raised above the floor",
      tags=["car lift", "vehicle hoist", "garage lift", "auto repair", "mechanic", "workshop", "automotive service"])
def _(S):
    return [
        line(seg(3, 2, 3, 22)),
        line(seg(21, 2, 21, 22)),
        line(seg(3, 17.5, 8.5, 17.5)),
        line(seg(15.5, 17.5, 21, 17.5)),
        shell(poly([(6, 14.5), (6, 12), (9, 11), (10.5, 7.5), (14, 7.5), (16, 11), (18, 12), (18, 14.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("drum-pump", CAT, "Hand-crank pump inserted in an upright drum with a spout for decanting liquid",
      tags=["barrel pump", "oil drum", "siphon", "fuel transfer", "decanting", "chemical drum", "hand pump"])
def _(S):
    return [
        shell(rect(3, 11, 11, 11, rr(S, 2.5))),
        detail(seg(3, 14.5, 14, 14.5)),
        line(seg(8.5, 3, 8.5, 11)),
        line(seg(5.5, 3, 11.5, 3)),
        line(poly([(8.5, 7), (17, 7), (17, 10.5)], r=S.r * 0.6)),
    ]


@icon("jack-up-rig", CAT, "Offshore platform standing in the sea on three tall legs that rise high above its deck",
      tags=["offshore platform", "oil rig", "drilling platform", "sea", "legs", "offshore wind installation", "marine"])
def _(S):
    return [
        line(seg(5.5, 2, 5.5, 21)),
        line(seg(12, 2, 12, 21)),
        line(seg(18.5, 2, 18.5, 21)),
        shell(rect(2.5, 9, 19, 3.5, rr(S, 1.75))),
        line(seg(2, 16.5, 22, 16.5)),
    ]


@icon("lng-carrier", CAT, "Tanker ship in side view with four large round domes in a row along its deck",
      tags=["gas tanker", "liquefied natural gas", "cargo ship", "marine", "shipping", "energy transport", "vessel"])
def _(S):
    parts = [shell(poly([(2, 13.5), (22, 13.5), (19, 20.5), (5, 20.5)], closed=True, r=S.r * 0.6))]
    for x in (5.5, 10, 14.5, 19):
        parts.append(dot(x, 11, 2))
    return parts


@icon("hydraulic-fracturing", CAT, "Cross section of a well pipe going down and turning sideways through rock with small cracks radiating from it",
      tags=["fracking", "shale gas", "well", "oil and gas", "horizontal drilling", "rock layer", "cracks"])
def _(S):
    parts = [line(seg(2, 3, 22, 3)), line(poly([(6, 3), (6, 14), (21, 14)], r=S.r * 1.5))]
    for x in (11, 15.5, 20):
        parts.append(line(seg(x, 11.5, x - 1.5, 7.5)))
        parts.append(line(seg(x, 16.5, x + 1.5, 20.5)))
    return parts


@icon("four-bar-linkage", CAT, "Four bars pinned into a quadrilateral with pivot circles at the corners, the bottom two fixed to hatched ground",
      tags=["linkage", "mechanism", "kinematics", "mechanical engineering", "crank rocker", "pivot", "machine design"])
def _(S):
    parts = [line(poly([(6, 16), (8, 6.5), (17, 8.5), (18, 16)], r=S.r * 0.6)), line(seg(6, 16, 6, 19.5)), line(seg(18, 16, 18, 19.5)),
             line(seg(3, 19.5, 21, 19.5))]
    for x in (7, 12, 17):
        parts.append(line(seg(x, 19.5, x - 2, 22)))
    for x, y in ((6, 16), (8, 6.5), (17, 8.5), (18, 16)):
        parts.append(blob(S, x, y, 1.9))
    return parts


@icon("drum-brake", CAT, "Round drum with two curved brake shoes inside and a coil spring stretched between their tops",
      tags=["brake", "car brake", "brake shoe", "automotive", "braking system", "wheel", "mechanic"],
      filled=lambda: U(D(P(circle(12, 12, 10)), P(circle(12, 12, 7.8))),
                       ST(arc(12, 12, 5.4, 120, 240), 2.8, "butt", "miter", 4), ST(arc(12, 12, 5.4, 300, 60), 2.8, "butt", "miter", 4),
                       ST("M9.3 7.5L10.4 5.5L12 9L13.6 5.5L14.7 7.5", 2.2, "butt", "miter", 4), P(circle(12, 13, 1.7))))
def _(S):
    body = circle(12, 12, 9) if S.name == "rounded" else poly(regular(12, 12, 9.6, 10, 18), closed=True)
    return [
        shell(body),
        line(arc(12, 12, 5.6, 120, 240)),
        line(arc(12, 12, 5.6, 300, 60)),
        line(poly([(9.3, 7.5), (10.4, 5.5), (12, 9), (13.6, 5.5), (14.7, 7.5)])),
        dot(12, 13, 1.5),
    ]
