"""TypeIcon Core: railway (batch 1) - track parts, switches, signals, tools and rail vehicles."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt

CAT = "railway"


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


# ============================================================================ track parts

@icon("fishplate", CAT, "Two rail ends joined by a bolted plate across the gap",
      tags=["rail joint", "track", "bolt", "splice", "railway", "connector"])
def _(S):
    return [
        shell(rect(2, 5, 20, 14, S.R)),
        detail(seg(12, 5, 12, 8)), detail(seg(12, 16, 12, 19)),
        detail(rect(5, 8, 14, 8, 1 if S.name == "line" else 3)),
        dot(8.5, 12, 1) if S.name == "line" else dot(8.5, 12, 1.2), dot(15.5, 12, 1),
    ]


@icon("railroad-tie", CAT, "Wooden railway sleeper with a rail resting on each end",
      tags=["sleeper", "crosstie", "track", "wood", "railway", "rail"], aliases=["railway-sleeper"])
def _(S):
    return [
        shell(rect(2, 13, 20, 8, min(S.R, 2))),
        line(poly([(6, 3), (6, 13)], r=0)), line(poly([(18, 3), (18, 13)], r=0)),
        detail(seg(8, 17, 11, 17)), detail(seg(13, 17, 16, 17)),
    ]


@icon("rail-spike", CAT, "Iron railroad spike with a hooked head and a pointed tip",
      tags=["nail", "track", "fastener", "railroad", "iron", "railway"])
def _(S):
    return [
        shell(poly([(6, 3), (18, 3), (18, 7), (14, 7), (14, 18), (12, 22), (10, 18), (10, 7), (6, 7)], closed=True, r=S.r * 0.6)),
    ]


@icon("rail-fastening-clip", CAT, "Rail foot held to a sleeper by two spring clips",
      tags=["rail clip", "track", "fastener", "sleeper", "spring clip", "railway"])
def _(S):
    prof = [(8, 2.5), (16, 2.5), (16, 6.5), (13.5, 8), (13.5, 12), (17, 13.5), (17, 17), (7, 17), (7, 13.5),
            (10.5, 12), (10.5, 8), (8, 6.5)]
    return [
        shell(poly(prof, closed=True, r=S.r * 0.5)),
        line(poly([(3, 21), (3, 11), (6.5, 11)], r=S.r)),
        line(poly([(21, 21), (21, 11), (17.5, 11)], r=S.r)),
    ]


@icon("tie-plate", CAT, "Steel base plate with a rail seat and four spike holes",
      tags=["base plate", "track", "railway", "rail seat", "spike", "steel"])
def _(S):
    return [
        shell(rect(3, 4, 18, 16, S.R)),
        detail(seg(10, 4, 10, 20)), detail(seg(14, 4, 14, 20)),
        sq(5, 6, 2, 2), sq(17, 6, 2, 2), sq(5, 16, 2, 2), sq(17, 16, 2, 2),
    ]


@icon("track-ballast", CAT, "Railway track cross section on a mound of stones",
      tags=["gravel", "crushed stone", "track bed", "sleeper", "railway", "rails"])
def _(S):
    return [
        line(seg(8, 3, 8, 8.5)), line(seg(16, 3, 16, 8.5)),
        line(seg(4, 9, 20, 9)),
        shell(poly([(2, 21), (6, 13), (18, 13), (22, 21)], closed=True, r=S.r)),
        dot(9, 17.5, 1), dot(14.5, 16.8, 1), dot(17, 19, 1), dot(12, 19.2, 0.9),
    ]


@icon("check-rail", CAT, "Curved track with a guard rail running along its inner side",
      tags=["guard rail", "curve", "track", "railway", "safety rail", "derailment"])
def _(S):
    return [
        line(arc(22, 22, 18, 180, 270)),
        line(arc(22, 22, 11, 190, 260)),
        line(seg(*_pt(22, 22, 12.2, 205), *_pt(22, 22, 16.5, 205))),
        line(seg(*_pt(22, 22, 12.2, 245), *_pt(22, 22, 16.5, 245))),
    ]


def _pt(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


@icon("turnout-frog", CAT, "V-shaped crossing piece where two rails meet with wing rails beside it",
      tags=["frog", "crossing nose", "points", "track", "railway", "switch", "turnout"])
def _(S):
    return [
        shell(poly([(12, 3), (14.5, 13), (14.5, 21), (9.5, 21), (9.5, 13)], closed=True, r=S.r * 0.6)),
        line(poly([(3, 3), (3, 8), (5, 21)], r=S.r)),
        line(poly([(21, 3), (21, 8), (19, 21)], r=S.r)),
    ]


@icon("switch-point-blade", CAT, "Tapered movable rail tongue beside a straight rail with a swing arrow",
      tags=["points", "switch rail", "turnout", "track", "railway", "tongue"])
def _(S):
    return [
        line(seg(21, 3, 21, 21)),
        shell(poly([(15, 4), (15, 21), (10, 21), (10, 15)], closed=True, r=S.r * 0.4)),
        line(seg(2, 9, 7, 9)),
        line(poly([(4.5, 6.5), (7, 9), (4.5, 11.5)], r=S.r)),
    ]


@icon("diamond-crossing", CAT, "Two tracks crossing at a shallow angle to form a diamond",
      tags=["track crossing", "rail crossing", "junction", "railway", "x crossing"])
def _(S):
    parts = []
    for off in (-4, 4):
        parts.append(line(seg(2, 12 - 3.5 + off, 22, 12 + 3.5 + off)))
        parts.append(line(seg(2, 12 + 3.5 + off, 22, 12 - 3.5 + off)))
    return parts


@icon("scissors-crossover", CAT, "Two parallel tracks joined by a pair of crossing diagonal links",
      tags=["crossover", "track layout", "junction", "railway", "x switch", "points"])
def _(S):
    return [
        line(seg(2, 5, 22, 5)), line(seg(2, 19, 22, 19)),
        line(seg(7, 5, 17, 19)), line(seg(17, 5, 7, 19)),
    ]


@icon("three-way-switch", CAT, "Single track splitting into left, straight and right tracks",
      tags=["triple points", "three way points", "junction", "split", "railway", "turnout"])
def _(S):
    return [
        line(seg(2, 12, 22, 12)),
        line(poly([(8, 12), (13, 5), (22, 5)], r=S.r)),
        line(poly([(8, 12), (13, 19), (22, 19)], r=S.r)),
    ]


@icon("derailer", CAT, "Wedge block clamped on a rail with a flag sign on a post",
      tags=["track safety", "derail", "rail block", "yard", "railway", "wedge"])
def _(S):
    return [
        line(seg(2, 20.5, 22, 20.5)),
        shell(poly([(5, 16.5), (13, 16.5), (13, 10)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        line(seg(17, 3, 17, 17)),
        shell(rect(17, 3, 4, 5) if S.name == "line" else rect(17, 3, 4, 5, 1)),
    ]


@icon("rail-expansion-joint", CAT, "Two rail ends cut on a diagonal and overlapping so they can slide",
      tags=["expansion gap", "rail joint", "thermal", "track", "railway", "slide"])
def _(S):
    return [
        shell(poly([(2, 4), (16, 4), (10, 11), (2, 11)], closed=True, r=S.r * 0.5)),
        shell(poly([(22, 13), (22, 20), (8, 20), (14, 13)], closed=True, r=S.r * 0.5)),
    ]


def _rail_section(x, top, bot, hw=3.0, fw=3.5):
    """Small rail cross section drawn from three open strokes: head, web and foot."""
    return [line(seg(x - hw, top, x + hw, top)), line(seg(x, top, x, bot)), line(seg(x - fw, bot, x + fw, bot))]


@icon("third-rail", CAT, "Track cross section with two running rails and a covered power rail",
      tags=["electric rail", "live rail", "power rail", "traction", "subway", "railway"])
def _(S):
    return [
        *_rail_section(5, 5, 17), *_rail_section(13, 5, 17),
        line(seg(2, 21, 22, 21)),
        shell(rect(18, 11, 4, 5)) if S.name == "line" else shell(rect(18, 11, 4, 5, 1.5)),
        line(seg(16.5, 7.5, 23, 7.5)),
    ]


@icon("catenary-tensioner", CAT, "Mast with a pulley wheel and hanging weights that keep an overhead wire tight",
      tags=["overhead line", "weights", "pulley", "electrification", "wire tension", "railway"])
def _(S):
    return [
        line(seg(5, 3, 5, 21)),
        line(seg(5, 6, 10.5, 6)),
        shell(circle(14, 6, 3)),
        line(seg(14, 9, 14, 13)),
        shell(rect(9.5, 13, 9, 8, min(S.R, 2))),
        detail(seg(9.5, 17, 18.5, 17)),
    ]


@icon("track-gauge", CAT, "Two rails with a measuring arrow between their inner edges",
      tags=["gauge", "rail width", "measure", "distance", "railway", "track"])
def _(S):
    return [
        shell(rect(2, 3, 6, 6, min(S.R, 2))), line(seg(5, 9, 5, 21)),
        shell(rect(16, 3, 6, 6, min(S.R, 2))), line(seg(19, 9, 19, 21)),
        line(seg(7, 15, 17, 15)),
        line(poly([(10, 12.5), (7, 15), (10, 17.5)], r=S.r)),
        line(poly([(14, 12.5), (17, 15), (14, 17.5)], r=S.r)),
    ]


@icon("dual-gauge-track", CAT, "Three rails on shared sleepers carrying both a narrow and a wide gauge",
      tags=["mixed gauge", "three rail track", "gauge", "railway", "track", "sleepers"])
def _(S):
    return [
        line(seg(3, 2.5, 3, 21.5)), line(seg(10, 2.5, 10, 21.5)), line(seg(21, 2.5, 21, 21.5)),
        line(seg(1.5, 7, 22.5, 7)),
        line(seg(1.5, 17, 22.5, 17)),
    ]


@icon("point-motor", CAT, "Trackside box driving a switch blade through a rod",
      tags=["switch machine", "points", "actuator", "turnout", "railway", "drive rod"])
def _(S):
    return [
        shell(rect(2, 7, 9, 10, S.R)),
        dot(6.5, 12, 1.25),
        line(seg(11, 12, 16, 12)),
        line(seg(16, 4, 16, 20)),
        line(seg(22, 3, 22, 21)),
    ]


@icon("switch-stand", CAT, "Ground lever with a post topped by a round target disc",
      tags=["points indicator", "switch lever", "turnout", "railway", "target", "signal"])
def _(S):
    return [
        shell(circle(14, 6, 3.5)),
        line(seg(14, 9.5, 14, 21)),
        line(poly([(14, 18), (6, 13)], r=S.r)),
        dot(5, 12.5, 1.6),
    ]


@icon("balise", CAT, "Beacon box fixed between two rails on the track",
      tags=["track beacon", "transponder", "eurobalise", "train control", "railway", "sensor"])
def _(S):
    return [
        line(seg(2, 3, 22, 3)), line(seg(2, 21, 22, 21)),
        shell(rect(7, 7, 10, 10, S.R)),
        detail(seg(10, 12, 14, 12)),
    ]


@icon("axle-counter", CAT, "Rail with a sensor clamped under the head and a wheel passing above",
      tags=["wheel sensor", "train detection", "track", "railway", "counter", "signalling"])
def _(S):
    return [
        shell(circle(12, 6.5, 4.5)),
        dot(12, 6.5, 1.2),
        line(seg(2, 15, 22, 15)),
        shell(rect(8, 17, 8, 4, min(S.R, 1.5))),
    ]


@icon("track-circuit", CAT, "Two rails joined by a battery at one end and a relay at the other",
      tags=["train detection", "signalling", "circuit", "battery", "relay", "railway"])
def _(S):
    return [
        line(seg(2, 3, 22, 3)), line(seg(2, 21, 22, 21)),
        line(seg(5, 3, 5, 9)), line(seg(2.5, 9, 7.5, 9)), line(seg(3.5, 14, 6.5, 14)), line(seg(5, 14, 5, 21)),
        line(seg(19, 3, 19, 7)), shell(rect(16, 7, 6, 8, min(S.R, 2))), line(seg(19, 15, 19, 21)),
    ]


@icon("trackside-cabinet", CAT, "Tall double-door equipment cabinet with a cable running into the ground",
      tags=["equipment case", "signalling", "relay room", "cabinet", "railway", "cable duct"])
def _(S):
    return [
        shell(rect(4, 2, 16, 14, min(S.R, 2))),
        detail(seg(12, 2, 12, 16)),
        detail(seg(7, 6, 9, 6)), detail(seg(15, 6, 17, 6)),
        dot(10, 11, 0.9), dot(14, 11, 0.9),
        line(poly([(12, 16), (12, 21), (22, 21)], r=S.r)),
    ]


@icon("railway-milepost", CAT, "Short trackside post with a slanted face showing a number",
      tags=["mile marker", "kilometre post", "distance marker", "railway", "trackside", "marker"])
def _(S):
    return [
        shell(poly([(7, 7), (17, 3), (17, 18), (7, 18)], closed=True, r=S.r * 0.5)),
        detail(seg(12, 8, 12, 15)),
        line(seg(2, 21, 22, 21)),
    ]


@icon("gradient-post", CAT, "Trackside post with one arm sloping up and one sloping down",
      tags=["slope marker", "incline", "grade", "railway", "gradient", "trackside"])
def _(S):
    return [
        line(seg(5, 3, 5, 21)),
        line(seg(5, 9, 20, 4)), dot(20, 4, 1.6),
        line(seg(5, 14, 20, 19)), dot(20, 19, 1.6),
    ]


@icon("speed-restriction-board", CAT, "Trackside speed limit sign on a post showing a large number",
      tags=["speed limit", "sign", "trackside", "railway", "restriction", "slow"])
def _(S):
    return [
        shell(rect(4, 2, 16, 14, min(S.R, 2))),
        detail(poly([(13, 5.5), (8.5, 11.5), (15.5, 11.5)], r=S.r * 0.5)),
        detail(seg(12.5, 6, 12.5, 13)),
        line(seg(12, 16, 12, 22)),
    ]


@icon("whistle-post", CAT, "Trackside sign on a post marked with a letter W for the horn",
      tags=["horn sign", "sound horn", "trackside", "railway", "w board", "warning"])
def _(S):
    return [
        shell(rect(3, 3, 18, 11, min(S.R, 2))),
        detail(poly([(6.5, 6.5), (9, 11), (12, 7.5), (15, 11), (17.5, 6.5)], r=0)),
        line(seg(12, 14, 12, 21)),
    ]


@icon("station-name-board", CAT, "Long station sign held between two posts with a line of text",
      tags=["station sign", "name board", "platform", "railway", "signage", "stop"])
def _(S):
    return [
        shell(rect(2, 4, 20, 11, S.R)),
        detail(seg(6, 9.5, 11, 9.5)), detail(seg(13, 9.5, 18, 9.5)),
        line(seg(6, 15, 6, 21)), line(seg(18, 15, 18, 21)),
    ]


# ============================================================================ platforms, crossings and signals

@icon("platform-number-sign", CAT, "Square sign with a large number hanging from a canopy by two rods",
      tags=["platform sign", "track number", "station", "railway", "hanging sign", "canopy"])
def _(S):
    return [
        line(seg(2, 3, 22, 3)),
        line(seg(8, 3, 8, 7)), line(seg(16, 3, 16, 7)),
        shell(rect(4, 7, 16, 14, S.R)),
        detail(poly([(10.5, 11.5), (13.5, 9.5), (13.5, 18)], r=S.r * 0.5)),
    ]


@icon("island-platform", CAT, "Top view of a narrow platform between two tracks with a canopy line down its middle",
      tags=["platform", "station", "tracks", "railway", "boarding", "layout"])
def _(S):
    return [
        line(seg(3, 2, 3, 22)), line(seg(21, 2, 21, 22)),
        shell(rect(8, 2, 8, 20, min(S.R, 2))),
        detail(seg(12, 6, 12, 18)),
    ]


@icon("train-boarding-ramp", CAT, "Ramp bridging the gap from a platform edge to a train door",
      tags=["wheelchair ramp", "accessible", "boarding", "platform", "station", "access"])
def _(S):
    return [
        shell(rect(2, 14, 7, 7, S.R)),
        line(seg(9, 14, 14.5, 11)),
        shell(rect(15, 3, 7, 18, S.R)),
        dot(18.5, 12, 0.9),
    ]


@icon("dispatch-paddle", CAT, "Round signal disc on a short handle held up to send a train off",
      tags=["lollipop", "guard signal", "departure", "railway", "station staff", "go"])
def _(S):
    return [
        shell(circle(12, 8, 6)),
        detail(seg(7, 8, 17, 8)),
        shell(rect(9.5, 15, 5, 7, 0.5 if S.name == "line" else 2.5)),
    ]


@icon("track-detonator", CAT, "Small disc strapped to the top of a rail with straps folded under the head",
      tags=["fog signal", "warning charge", "railway", "explosive", "rail", "emergency"])
def _(S):
    return [
        shell(rect(2, 15, 20, 5, min(S.R, 2))),
        shell(rect(8, 8, 8, 7, S.R)),
        line(poly([(8, 11), (4, 11), (4, 15)], r=S.r)), line(poly([(16, 11), (20, 11), (20, 15)], r=S.r)),
    ]


@icon("crossing-bell", CAT, "Round bell with sound arcs on a post above a crossed warning sign",
      tags=["level crossing", "alarm", "warning", "railway", "ring", "crossbuck"])
def _(S):
    return [
        shell(circle(12, 6, 3.5)),
        line(arc(12, 6, 7.5, -40, 40)), line(arc(12, 6, 7.5, 140, 220)),
        line(seg(12, 9.5, 12, 15)),
        line(seg(5, 15, 19, 21)), line(seg(19, 15, 5, 21)),
    ]


@icon("gated-level-crossing", CAT, "Road crossing a railway with a closed barrier on each side of the tracks",
      tags=["level crossing", "barrier", "boom gate", "railway", "road", "crossing"])
def _(S):
    return [
        line(seg(9.5, 2, 9.5, 22)), line(seg(14.5, 2, 14.5, 22)),
        shell(rect(3, 8, 3, 12, min(S.R, 1.5))), dot(4.5, 4, 1.4),
        shell(rect(18, 8, 3, 12, min(S.R, 1.5))), dot(19.5, 4, 1.4),
    ]


@icon("pedestrian-level-crossing", CAT, "Footpath crossing railway tracks with zigzag barriers at both sides",
      tags=["footpath crossing", "pedestrians", "walkway", "railway", "tracks", "crossing"])
def _(S):
    return [
        line(seg(2, 10, 22, 10)), line(seg(2, 14, 22, 14)),
        line(poly([(5, 6), (8, 3), (11, 6), (14, 3), (17, 6), (19, 4)], r=S.r * 0.4)),
        line(poly([(5, 20), (8, 17), (11, 20), (14, 17), (17, 20), (19, 18)], r=S.r * 0.4)),
    ]


@icon("dwarf-signal", CAT, "Squat ground-level signal box with two lamps in its face",
      tags=["ground signal", "shunting signal", "low signal", "railway", "yard", "lamp"])
def _(S):
    return [
        shell(rect(3, 3, 18, 12, S.R)),
        dot(8.5, 9, 2), dot(15.5, 9, 2),
        line(seg(12, 15, 12, 21)), line(seg(7, 21, 17, 21)),
    ]


@icon("distant-signal", CAT, "Semaphore signal post with a fishtail arm that has a V notch in its end",
      tags=["semaphore", "signal arm", "caution", "railway", "fishtail", "warning"])
def _(S):
    return [
        line(seg(5, 2, 5, 22)),
        shell(poly([(5, 5), (22, 5), (18.5, 9), (22, 13), (5, 13)], closed=True, r=S.r * 0.5)),
    ]


@icon("position-light-signal", CAT, "Round signal target on a post with three lamps in a line",
      tags=["colour light", "signal", "lamps", "railway", "target", "light signal"])
def _(S):
    return [
        shell(circle(12, 9, 6.5)),
        dot(8.5, 12, 1.1), dot(12, 9, 1.1), dot(15.5, 6, 1.1),
        line(seg(12, 15.5, 12, 22)),
    ]


@icon("route-indicator", CAT, "Signal head with a diagonal row of lamps showing a diverging route",
      tags=["junction indicator", "feather", "diverging route", "signal", "railway", "lamps"])
def _(S):
    return [
        shell(rect(3, 11, 10, 11, S.R)),
        dot(8, 16.5, 1.7),
        dot(14.5, 9, 1.1), dot(17, 6.7, 1.1), dot(19.5, 4.4, 1.1),
    ]


@icon("banner-repeater-signal", CAT, "Round signal window on a post with a single dark bar across its centre",
      tags=["repeater", "signal", "railway", "banner", "caution", "post"])
def _(S):
    return [
        shell(circle(12, 9.5, 7)),
        detail(seg(6, 9.5, 18, 9.5)),
        line(seg(12, 16.5, 12, 22)),
    ]


@icon("signal-gantry", CAT, "Overhead frame spanning the tracks with signal heads hanging above each line",
      tags=["signal bridge", "overhead", "gantry", "railway", "signals", "tracks"])
def _(S):
    return [
        line(seg(2, 3.5, 22, 3.5)),
        line(seg(3, 3.5, 3, 21)), line(seg(21, 3.5, 21, 21)),
        line(seg(8, 3.5, 8, 8)), line(seg(16, 3.5, 16, 8)),
        dot(8, 10, 2.2), dot(16, 10, 2.2),
        line(seg(8, 16, 8, 21)),
        line(seg(16, 16, 16, 21)),
    ]


# ============================================================================ signalling equipment

@icon("cab-signal-display", CAT, "Driver's cab screen showing a speed dial beside a signal lamp",
      tags=["train cab", "speed dial", "driver display", "signal aspect", "railway", "dashboard"])
def _(S):
    return [
        shell(rect(2, 3, 20, 14, S.R)),
        detail(arc(8.5, 12.5, 3.5, 180, 360)),
        detail(seg(8.5, 12.5, 10.5, 9.5)),
        dot(16.5, 10, 2.2),
        line(seg(12, 17, 12, 21)), line(seg(8, 21, 16, 21)),
    ]


@icon("signal-post-telephone", CAT, "Signal post box with a telephone handset symbol on its door",
      tags=["emergency phone", "trackside phone", "call", "signalman", "railway", "help point"])
def _(S):
    return [
        shell(rect(4, 2, 16, 13, S.R)),
        detail(poly([(8, 10), (8, 6.5), (16, 6.5), (16, 10)], r=S.r * 0.5)),
        line(seg(12, 15, 12, 22)),
    ]


@icon("signaling-panel", CAT, "Control panel with a track diagram of lines and switches above a row of buttons",
      tags=["control panel", "interlocking", "signal box", "track diagram", "railway", "dispatcher"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, S.R)),
        detail(poly([(5, 7), (9, 7), (12, 11), (19, 11)], r=S.r * 0.4)),
        detail(seg(12, 7, 19, 7)),
        dot(6.5, 16.5, 1.1), dot(10.5, 16.5, 1.1), dot(14.5, 16.5, 1.1), dot(18, 16.5, 1.1),
    ]


@icon("single-line-token", CAT, "Round metal token with a centre hole resting in a leather pouch",
      tags=["staff", "token", "single track", "authority", "railway", "pouch"])
def _(S):
    return [
        shell(circle(12, 6, 3.8)),
        dot(12, 6, 1.2),
        line(seg(12, 9.8, 12, 12)),
        shell(rect(4, 12, 16, 10, S.R)),
        detail(seg(4, 15.5, 20, 15.5)), dot(12, 18.7, 1.1),
    ]


@icon("block-instrument", CAT, "Wooden instrument box with a half dial and needle above a handle knob",
      tags=["block signalling", "signal box", "line clear", "train on line", "railway", "telegraph"])
def _(S):
    return [
        shell(rect(4, 2, 16, 20, S.R)),
        detail(arc(12, 11, 5, 180, 360)),
        detail(seg(12, 11, 14.5, 7.5)),
        dot(12, 17, 1.5),
    ]


@icon("ground-frame", CAT, "Small lever frame with three levers, one of them pulled over",
      tags=["lever frame", "points lever", "signal box", "railway", "trackside", "interlocking"])
def _(S):
    return [
        shell(rect(2, 16, 20, 5, S.R if S.name == "line" else 2.5)),
        line(seg(6, 16, 6, 6)), dot(6, 4.5, 1.6),
        line(seg(12, 16, 12, 6)), dot(12, 4.5, 1.6),
        line(seg(18, 16, 20.5, 8)), dot(20.7, 6.5, 1.6),
    ]


# ============================================================================ hand tools and track equipment

def rot(pts, deg=45, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rp(pts, closed=True, r=0.0, deg=45):
    return poly(rot(pts, deg), closed=closed, r=r)


def rseg(x1, y1, x2, y2, deg=45):
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg)
    return seg(a, b, c, d)


@icon("spike-maul", CAT, "Long-handled hammer with a slim double-ended head for driving rail spikes",
      tags=["sledgehammer", "railroad hammer", "track tool", "spike driving", "railway", "maintenance"])
def _(S):
    return [
        shell(rp([(6.5, 4), (17.5, 4), (17.5, 9), (6.5, 9)], r=S.r * 0.6), stroke_miterlimit="2"),
        shell(rp([(10.5, 9), (13.5, 9), (13.5, 22), (10.5, 22)], r=S.r * 0.4)),
    ]


@icon("rail-claw-bar", CAT, "Long steel bar with a forked claw end for pulling spikes",
      tags=["spike puller", "claw bar", "pry bar", "track tool", "railway", "crowbar"])
def _(S):
    return [
        line(rseg(12, 2, 12, 12)),
        shell(rp([(8, 11), (16, 11), (16, 16), (14.5, 22), (12, 18), (9.5, 22), (8, 16)], r=S.r * 0.3), stroke_miterlimit="2"),
    ]


@icon("rail-tongs", CAT, "Hinged tongs with curved jaws gripping a short length of rail",
      tags=["rail lifting", "tongs", "track tool", "railway", "lifting", "grip"])
def _(S):
    return [
        line(poly([(7, 3), (17, 16), (17, 21)], r=S.r)),
        line(poly([(17, 3), (7, 16), (7, 21)], r=S.r)),
        sq(10, 16, 4, 5),
    ]


@icon("track-wrench", CAT, "Very long open-ended spanner for fishplate bolts",
      tags=["spanner", "bolt", "fishplate", "track tool", "railway", "maintenance"])
def _(S):
    cy, R, hw, sw = 5.5, 5.0, 1.75, 2.0
    ys = cy - math.sqrt(R * R - hw * hw)
    yj = cy + math.sqrt(R * R - sw * sw)
    pts = [(12 - hw, ys), (12 - hw, cy), (12 + hw, cy), (12 + hw, ys), (12 + sw, yj), (12 + sw, 22), (12 - sw, 22), (12 - sw, yj)]
    return [shell(rp(pts, r=S.r * 0.5), stroke_miterlimit="2")]


@icon("track-jack", CAT, "Squat jack with a toe plate under a rail and a ratchet handle on top",
      tags=["lifting jack", "rail lift", "track tool", "railway", "ratchet", "maintenance"])
def _(S):
    return [
        line(seg(2, 13, 9, 13)),
        line(poly([(9, 19), (3, 19)], r=0)),
        shell(rect(9, 10, 8, 11, S.R)),
        line(seg(13, 10, 21, 3)),
        dot(13, 15, 1.2),
    ]


@icon("rail-saw", CAT, "Portable cutting saw with a round abrasive disc over a rail",
      tags=["cutoff saw", "rail cutter", "abrasive", "track tool", "railway", "cutting"])
def _(S):
    return [
        shell(circle(15, 9, 6)),
        dot(15, 9, 1.2),
        shell(rect(2, 4, 5, 9, S.R if S.name == "line" else 2.5)),
        line(seg(7, 8.5, 9, 9)),
        shell(rect(3, 18, 18, 4, min(S.R, 1.5))),
    ]


@icon("rail-drill", CAT, "Drill machine clamped beside a rail with its bit pointing into the web",
      tags=["drilling", "rail web", "track tool", "railway", "bolt hole", "machine"])
def _(S):
    return [
        line(seg(15, 3, 22, 3)), line(seg(18.5, 3, 18.5, 21)), line(seg(15, 21, 22, 21)),
        shell(rect(2, 7, 9, 10, S.R)),
        line(seg(11, 12, 18, 12)),
        line(seg(6.5, 7, 6.5, 3)),
    ]


@icon("rail-bender", CAT, "Heavy frame with a screw and handle bending a rail into a curve",
      tags=["rail curving", "jim crow", "track tool", "railway", "screw press", "bend"])
def _(S):
    return [
        line(seg(7, 3, 17, 3)), line(seg(12, 3, 12, 9)),
        shell(rect(3, 9, 18, 12, S.R)),
        detail("M6.5 17.5Q12 12.5 17.5 17.5"),
    ]


@icon("tamping-pick", CAT, "Track pick with one pointed end and one flat paddle end for packing ballast",
      tags=["ballast tool", "beater pick", "sleeper packing", "railway", "maintenance", "hand tool"])
def _(S):
    return [
        shell(poly([(2, 7), (9, 4.5), (16, 4.5), (16, 2.5), (21, 2.5), (21, 9.5), (16, 9.5), (16, 8), (9, 8)], closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
        shell(rect(10, 9.5, 4, 12.5, min(S.R, 2))),
    ]


@icon("ballast-fork", CAT, "Wide fork with many long straight tines and a D-shaped handle",
      tags=["stone fork", "ballast tool", "track tool", "railway", "rake", "maintenance"])
def _(S):
    return [
        line(seg(4, 2.5, 4, 12)), line(seg(8, 2.5, 8, 12)), line(seg(12, 2.5, 12, 12)),
        line(seg(16, 2.5, 16, 12)), line(seg(20, 2.5, 20, 12)),
        line(seg(3, 12.5, 21, 12.5)),
        line(seg(12, 12.5, 12, 17.5)),
        shell(rect(8, 17.5, 8, 4.5, S.R)),
    ]


@icon("rail-thermometer", CAT, "Round dial thermometer with a magnetic base stuck to a rail",
      tags=["rail temperature", "dial gauge", "heat", "expansion", "railway", "measure"])
def _(S):
    return [
        shell(circle(12, 8, 6)),
        detail(seg(12, 8, 15, 5)), dot(12, 8, 1),
        shell(rect(9, 14.5, 6, 3.5, min(S.R, 1.5))),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("thermite-welding", CAT, "Crucible pouring a stream of molten metal into the gap between two rail ends",
      tags=["rail welding", "molten metal", "crucible", "joint", "railway", "weld"])
def _(S):
    return [
        shell(poly([(5, 2.5), (19, 2.5), (15, 10), (9, 10)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        dot(12, 13.2, 1.1),
        shell(rect(2, 17, 8, 4, min(S.R, 1.5))), shell(rect(14, 17, 8, 4, min(S.R, 1.5))),
    ]


@icon("rerailing-ramp", CAT, "Steel ramp on a rail with a wheel climbing up it back onto the track",
      tags=["derailment", "recovery", "wheel", "ramp", "railway", "rerail"])
def _(S):
    return [
        shell(poly([(3, 17), (17, 17), (17, 8)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        shell(circle(7.5, 8.5, 3.5)), dot(7.5, 8.5, 0.9),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("track-trolley", CAT, "Small flat trolley on rails with a push handle at one end",
      tags=["hand trolley", "inspection", "rail cart", "railway", "maintenance", "push"])
def _(S):
    return [
        shell(rect(2, 9, 17, 5, S.R if S.name == "line" else 2.5)),
        shell(circle(7, 17.5, 2)), shell(circle(15, 17.5, 2)),
        line(seg(19, 11, 19, 3)), dot(19, 3, 1.6),
        line(seg(2, 22, 22, 22)),
    ]


@icon("rail-speeder", CAT, "Small motorised rail car with a boxy cab, windscreen and flanged wheels",
      tags=["inspection car", "motor car", "track car", "railway", "maintenance", "cab"])
def _(S):
    return [
        shell(poly([(3, 16), (3, 10), (8, 10), (10, 5), (19, 5), (21, 10), (21, 16)], closed=True, r=S.r * 0.6)),
        detail(seg(12, 8.5, 17, 8.5)),
        shell(circle(7, 18.8, 2)), shell(circle(17, 18.8, 2)),
        line(seg(2, 22.5, 22, 22.5)),
    ]


@icon("rail-flaw-detector", CAT, "Walking trolley on one rail with a push handle and a screen showing a pulse trace",
      tags=["ultrasonic", "rail inspection", "crack detection", "waveform", "railway", "testing"])
def _(S):
    return [
        shell(rect(9, 2, 13, 9, S.R)),
        detail(poly([(11.5, 7), (14, 7), (15.5, 4.5), (17, 9), (18.5, 7), (20, 7)], r=0)),
        line(seg(14, 11, 11, 16)),
        shell(circle(7, 18, 2.2)),
        shell(circle(15, 18, 2.2)),
        line(seg(2, 22.5, 22, 22.5)),
    ]


@icon("track-geometry-car", CAT, "Rail coach with a sensor beam under its middle sending laser lines down to the rails",
      tags=["measuring car", "track inspection", "laser", "survey", "railway", "sensor"])
def _(S):
    return [
        shell(rect(2, 3, 20, 10, S.R)),
        detail(seg(5, 8, 8, 8)), detail(seg(10.5, 8, 13.5, 8)), detail(seg(16, 8, 19, 8)),
        line(seg(8, 16, 16, 16)),
        line(seg(8, 16, 8, 20)), line(seg(16, 16, 16, 20)),
        line(seg(2, 22.5, 22, 22.5)),
    ]


@icon("tamping-machine", CAT, "Long track machine with a cab at each end and tines plunging into the ballast",
      tags=["track maintenance", "ballast packing", "tines", "machine", "railway", "tamper"])
def _(S):
    return [
        shell(rect(2, 4, 20, 9, S.R)),
        detail(seg(5, 8.5, 7, 8.5)), detail(seg(17, 8.5, 19, 8.5)),
        line(seg(8, 13, 8, 19.5)), line(seg(12, 13, 12, 19.5)), line(seg(16, 13, 16, 19.5)),
        line(seg(2, 22, 22, 22)),
    ]


@icon("ballast-regulator", CAT, "Short track vehicle with a plough blade at the front and a rotary brush at the back",
      tags=["ballast plough", "track maintenance", "brush", "machine", "railway", "stone"])
def _(S):
    return [
        shell(rect(6, 4, 11, 11, S.R)),
        line(poly([(5, 9), (2, 19)], r=0)),
        shell(circle(19.5, 16.5, 3)),
        dot(9, 18.5, 1.5), dot(14, 18.5, 1.5),
    ]


@icon("track-laying-machine", CAT, "Gantry vehicle lowering a ready-made panel of rails and sleepers onto the ground",
      tags=["track panel", "construction", "crane", "gantry", "railway", "new track"])
def _(S):
    return [
        line(poly([(3, 21), (3, 3.5), (21, 3.5), (21, 21)], r=S.r)),
        line(seg(8, 3.5, 8, 9)), line(seg(16, 3.5, 16, 9)),
        shell(rect(5, 9, 14, 7, min(S.R, 2))),
        detail(seg(9, 9, 9, 16)), detail(seg(15, 9, 15, 16)),
    ]


@icon("overhead-line-vehicle", CAT, "Rail vehicle with a raised railed work platform reaching an overhead wire",
      tags=["catenary", "wire maintenance", "cherry picker", "electrification", "railway", "platform"])
def _(S):
    return [
        line(seg(2, 2.5, 22, 2.5)),
        line(poly([(11, 6), (11, 10), (20, 10), (20, 6)], r=S.r * 0.5)),
        line(seg(8, 14.5, 13, 10)),
        shell(rect(2, 14, 20, 5, S.R if S.name == "line" else 2.5)),
        line(seg(2, 22.5, 22, 22.5)),
    ]


@icon("rail-grinding-train", CAT, "Rail vehicle with grinding stones under its body throwing sparks onto the rail",
      tags=["rail grinder", "sparks", "maintenance", "machine", "railway", "polishing"])
def _(S):
    return [
        shell(rect(2, 3, 20, 10, S.R)),
        detail(seg(5, 7, 8, 7)), detail(seg(16, 7, 19, 7)),
        dot(8, 16.5, 1.8), dot(12, 16.5, 1.8), dot(16, 16.5, 1.8),
        line(seg(2, 21.5, 22, 21.5)),
        dot(20.5, 17.5, 0.9), dot(3.5, 17.5, 0.9),
    ]


# ============================================================================ travel items

@icon("rail-pass", CAT, "Folding booklet pass with a train front on its cover",
      tags=["train pass", "travel pass", "ticket booklet", "railcard", "railway", "season ticket"])
def _(S):
    return [
        shell(rect(3, 2, 18, 20, S.R)),
        detail(seg(8, 2, 8, 22)),
        detail(rect(11, 5, 7, 6, 1)),
        dot(12.5, 15.5, 1), dot(16.5, 15.5, 1),
    ]


@icon("train-timetable", CAT, "Printed sheet with a train front above a grid of departure times",
      tags=["schedule", "departures", "times", "railway", "station", "arrivals"])
def _(S):
    return [
        shell(rect(4, 2, 16, 20, S.R)),
        detail(rect(8, 5, 8, 3.5, 1) if S.name == "line" else rect(8, 5, 8, 3.5, 1.7)),
        detail(seg(5, 13.5, 19, 13.5)), detail(seg(5, 17.5, 19, 17.5)), detail(seg(12, 13.5, 12, 22)),
    ]


@icon("quiet-carriage", CAT, "Train carriage with a hushing face symbol, a finger held to the lips",
      tags=["quiet zone", "silent", "shh", "railway", "carriage", "coach"])
def _(S):
    return [
        shell(rect(2, 3, 20, 14, S.R)),
        detail(circle(12, 10, 3.5)),
        detail(seg(12, 9.5, 12, 12.5)),
        dot(7, 20, 1.6), dot(17, 20, 1.6),
    ]


@icon("first-class-carriage", CAT, "Train carriage with a numeral 1 above its windows and a stripe along its body",
      tags=["first class", "premium", "coach", "railway", "carriage", "upgrade"])
def _(S):
    return [
        shell(rect(2, 3, 20, 14, S.R)),
        detail(poly([(5.5, 8), (7.5, 6), (7.5, 11)], r=0)),
        detail(seg(11, 8, 19, 8)),
        detail(seg(3, 13.5, 21, 13.5)),
        dot(7, 20, 1.6), dot(17, 20, 1.6),
    ]


@icon("reserved-seat-tag", CAT, "Seat headrest with a small reservation card clipped into a holder",
      tags=["seat reservation", "booking", "headrest", "railway", "seat number", "card"])
def _(S):
    return [
        shell(rect(3, 2, 18, 14, S.R)),
        detail(rect(8, 6, 8, 8, min(S.R, 1.5))),
        line(seg(8, 16, 8, 22)), line(seg(16, 16, 16, 22)),
    ]


@icon("train-seat", CAT, "Two upholstered train seats side by side with tall backs and a shared armrest",
      tags=["passenger seat", "seating", "carriage", "railway", "chair", "armrest"])
def _(S):
    return [
        shell(rect(2, 2, 8, 12, S.R)), shell(rect(14, 2, 8, 12, S.R)),
        shell(rect(10.5, 10, 3, 9, min(S.R, 1.5))),
        shell(rect(2, 17, 20, 5, S.R)),
    ]
