"""TypeIcon Core: railway (batch 2) - rolling stock, layouts, equipment, crew and trackside gear."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt

CAT = "railway"


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def wheels(*xs, y=20.0, r=2.0):
    return [dot(x, y, r) for x in xs]


def rot(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rail_icon_pt(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


# ============================================================================ rolling stock

@icon("gangway-bellows", CAT, "Two carriage ends joined by a folded rubber tunnel between them",
      tags=["gangway", "vestibule", "carriage connection", "train", "accordion", "passage"])
def _(S):
    return [
        shell(poly([(2, 4), (6, 4), (6, 20), (2, 20)], closed=True, r=S.r * 0.8)),
        shell(poly([(18, 4), (22, 4), (22, 20), (18, 20)], closed=True, r=S.r * 0.8)),
        shell(poly([(6, 7), (18, 7), (18, 17), (6, 17)], closed=True, r=S.r)),
        detail(seg(10, 7, 10, 17)), detail(seg(14, 7, 14, 17)),
    ]


@icon("coach-position-indicator", CAT, "Strip of three carriage sections above a platform line with a pointer",
      tags=["coach position", "platform display", "carriage order", "train", "boarding", "station"])
def _(S):
    return [
        shell(rect(2, 3, 20, 9, min(S.R, 3))),
        detail(seg(8.7, 3, 8.7, 12)), detail(seg(15.3, 3, 15.3, 12)),
        dot(5.3, 7.5, 1.1), dot(12, 7.5, 1.1), dot(18.7, 7.5, 1.1),
        solid(poly([(12, 14.5), (9, 19), (15, 19)], closed=True)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("car-stop-marker", CAT, "Numbered board on a post at a platform edge beside two rails",
      tags=["stopping marker", "platform", "carriage stop", "train", "board", "station sign"])
def _(S):
    return [
        shell(rect(2, 3, 10, 10, min(S.R, 2))),
        detail(poly([(5.5, 7), (7, 5.5), (7, 10.5)])),
        line(seg(7, 13, 7, 21)),
        line(seg(17, 9, 17, 21)), line(seg(21, 9, 21, 21)),
        line(seg(17, 13, 21, 13)), line(seg(17, 18, 21, 18)),
    ]


@icon("train-destination-display", CAT, "Train front with a wide text sign above the windshield",
      tags=["destination sign", "headsign", "led display", "train front", "route", "rail"])
def _(S):
    return [
        shell(rect(3, 2, 18, 6, min(S.R, 2))),
        dot(7, 5, 0.9), dot(10.5, 5, 0.9), dot(14, 5, 0.9), dot(17, 5, 0.9),
        shell(rect(4, 10, 16, 10, min(S.R, 3))),
        sq(7, 12, 10, 3),
        dot(8, 17.2, 1.1), dot(16, 17.2, 1.1),
    ]


@icon("portable-ticket-printer", CAT, "Handheld printer with a small screen and keypad and a ticket coming out of the top",
      tags=["ticket machine", "handheld", "conductor", "fare", "receipt", "rail ticket"])
def _(S):
    return [
        shell(rect(5, 9, 14, 13, S.R)),
        sq(8, 11.5, 8, 3),
        dot(9, 18, 1.1), dot(12, 18, 1.1), dot(15, 18, 1.1),
        line(poly([(9, 9), (9, 3), (15, 3), (15, 9)], r=S.r * 0.6)),
    ]


@icon("refrigerator-car", CAT, "Enclosed freight wagon with a snowflake on its side and a cooling unit at one end",
      tags=["reefer", "cold chain", "freight", "wagon", "chilled", "rail"])
def _(S):
    cx, cy, r = 9.5, 10.5, 3.8
    spokes = []
    for a in (0, 60, 120):
        p1 = rail_icon_pt(cx, cy, r, a)
        p2 = rail_icon_pt(cx, cy, r, a + 180)
        spokes.append(detail(seg(*p1, *p2)))
    return [
        shell(rect(2, 3, 20, 14, min(S.R, 3))),
        *spokes,
        detail(seg(17, 3, 17, 17)),
        dot(19.5, 8, 0.9), dot(19.5, 12, 0.9),
        *wheels(6.5, 17.5),
    ]


@icon("centerbeam-car", CAT, "Flat freight wagon with a tall central spine and end walls carrying stacks of lumber",
      tags=["lumber", "timber", "freight", "flatcar", "wagon", "wood"])
def _(S):
    return [
        line(seg(2, 16.5, 22, 16.5)),
        line(seg(3, 6, 3, 16)), line(seg(21, 6, 21, 16)),
        line(seg(12, 2.5, 12, 16)),
        sq(5.5, 7.5, 4, 2.5), sq(5.5, 11, 4, 2.5), sq(14.5, 7.5, 4, 2.5), sq(14.5, 11, 4, 2.5),
        *wheels(6.5, 17.5, y=20.5, r=1.5),
    ]


@icon("mail-car", CAT, "Rail carriage with an envelope on its side and a wide sliding door",
      tags=["post", "postal", "mail train", "parcel", "carriage", "letters"])
def _(S):
    return [
        shell(rect(2, 4, 20, 13, min(S.R, 3))),
        detail(rect(5.5, 7.5, 6, 5)),
        detail(poly([(5.5, 8), (8.5, 10.7), (11.5, 8)])),
        detail(seg(15, 4, 15, 17)),
        dot(18, 10.5, 1),
        *wheels(6.5, 17.5),
    ]


@icon("baggage-car", CAT, "Windowless rail carriage with two wide sliding doors and a suitcase on its side",
      tags=["luggage", "baggage van", "train", "carriage", "suitcase", "cargo"])
def _(S):
    return [
        shell(rect(2, 4, 20, 13, min(S.R, 3))),
        detail(seg(12, 4, 12, 17)),
        sq(5, 10, 4, 4, 1),
        line(poly([(6, 10), (6, 8.5), (8, 8.5), (8, 10)])),
        dot(14.5, 10.5, 1),
        *wheels(6.5, 17.5),
    ]


@icon("side-dump-car", CAT, "Rail wagon with its box tilted sideways on a piston and rocks tumbling out",
      tags=["dump wagon", "ballast", "tipping", "freight", "rocks", "maintenance"])
def _(S):
    box = rot([(3, 5), (17, 5), (17, 13), (3, 13)], 18, 17, 13)
    return [
        shell(poly(box, closed=True, r=S.r * 0.6)),
        line(seg(2, 17, 22, 17)),
        line(seg(10, 17, 10, 12.5)),
        dot(21, 11, 1.3), dot(20, 14.5, 1.1),
        *wheels(6, 19.5, y=20.5, r=1.5),
        *wheels(14, y=20.5, r=1.5),
    ]


@icon("compartment-coach", CAT, "Old rail carriage with a row of narrow doors along its side, each with a window",
      tags=["passenger coach", "vintage", "heritage", "carriage", "doors", "slam door"])
def _(S):
    return [
        shell(rect(2, 5, 20, 12, min(S.R, 3))),
        detail(seg(8, 5, 8, 17)), detail(seg(12, 5, 12, 17)), detail(seg(16, 5, 16, 17)),
        sq(4.5, 8, 2, 3), sq(9.5, 8, 1, 3), sq(13.5, 8, 1, 3), sq(18, 8, 2, 3),
        *wheels(6.5, 17.5),
    ]


@icon("diesel-multiple-unit", CAT, "Two-car passenger train with a driving cab at each end and an exhaust stack on the roof",
      tags=["dmu", "railcar", "diesel train", "commuter", "regional train", "passenger"])
def _(S):
    body = [(5, 5), (19, 5), (22, 9), (22, 16), (2, 16), (2, 9)]
    return [
        shell(poly(body, closed=True, r=S.r * 0.6)),
        detail(seg(12, 5, 12, 16)),
        sq(7, 8, 3, 3), sq(14, 8, 3, 3),
        sq(3.5, 9.5, 1.5, 2.5), sq(19, 9.5, 1.5, 2.5),
        solid(rect(7.5, 2, 3, 3)),
        *wheels(5.5, 9.5, 14.5, 18.5, y=19.2, r=1.5),
    ]


@icon("railbus", CAT, "Small single rail car with a bus-shaped body, large windows and two axles",
      tags=["rail car", "light rail", "branch line", "diesel", "bus", "single car"])
def _(S):
    return [
        shell(rect(2, 4, 20, 13, S.R + 1)),
        sq(5, 7.5, 4, 3.5), sq(10, 7.5, 4, 3.5), sq(15, 7.5, 4, 3.5),
        dot(5, 14, 1), dot(19, 14, 1),
        *wheels(7, 17, y=19.8, r=1.7),
    ]


@icon("locomotive-tender", CAT, "Small wagon heaped with coal above a water tank, coupled behind a steam engine",
      tags=["steam", "coal", "tender", "water tank", "locomotive", "heritage"])
def _(S):
    return [
        shell(rect(2, 11, 20, 6, min(S.R, 2))),
        shell(poly([(4, 10), (6, 7), (9, 5), (12, 6), (15, 4), (18, 7), (20, 10)], closed=True, r=S.r)),
        *wheels(6.5, 17.5, y=20.5, r=1.5),
    ]


@icon("open-excursion-car", CAT, "Rail carriage with a roof on posts, open sides and benches visible",
      tags=["scenic", "tourist", "heritage", "open carriage", "bench seats", "excursion"])
def _(S):
    return [
        shell(rect(3, 4, 18, 3, min(S.R, 1.5))),
        line(seg(4, 7, 4, 15)), line(seg(12, 7, 12, 15)), line(seg(20, 7, 20, 15)),
        line(poly([(7.5, 9), (7.5, 13), (10, 13)], r=S.r * 0.6)),
        line(poly([(15.5, 9), (15.5, 13), (18, 13)], r=S.r * 0.6)),
        line(seg(2, 16.5, 22, 16.5)),
        *wheels(6.5, 17.5, y=20.5, r=1.5),
    ]


@icon("wagon-brake-wheel", CAT, "Large spoked hand wheel on a vertical shaft mounted at the end of a freight wagon",
      tags=["handbrake", "hand wheel", "freight", "wagon", "brake", "shunting"])
def _(S):
    cx, cy, r = 12, 9, 7
    spokes = []
    for a in (0, 60, 120):
        spokes.append(detail(seg(*rail_icon_pt(cx, cy, r, a), *rail_icon_pt(cx, cy, r, a + 180))))
    return [
        shell(circle(cx, cy, r) if S.name == "rounded" else poly(regular(cx, cy, r + 0.3, 10, start=-90), closed=True)),
        *spokes,
        dot(cx, cy, 1.8),
        line(seg(12, 16, 12, 21)),
        line(seg(7, 21.5, 17, 21.5)),
    ]


@icon("trolley-pole", CAT, "Diagonal pole rising from a tram roof with a small wheel at its tip touching an overhead wire",
      tags=["tram", "streetcar", "overhead wire", "pole", "electric", "trolleybus"])
def _(S):
    return [
        shell(rect(2, 12, 15, 8, S.R)),
        sq(5, 14.5, 3, 2), sq(10, 14.5, 3, 2),
        line(seg(8, 12, 17, 5)),
        dot(18, 4.5, 1.6),
        line(seg(10, 3, 22, 3)),
    ]


@icon("train-ferry", CAT, "Ship hull with a train carriage on rails shown inside it",
      tags=["rail ferry", "ship", "boat", "crossing", "freight", "transport"])
def _(S):
    return [
        shell(poly([(2, 9), (22, 9), (19.5, 18), (17, 21), (5, 21), (2, 17)], closed=True, r=S.r)),
        sq(6, 11.5, 11, 3.5),
        detail(seg(5, 17.5, 19, 17.5)),
        line(poly([(15, 9), (15, 4), (20, 4), (20, 9)], r=S.r * 0.6)),
    ]


@icon("railway-roundhouse", CAT, "Top view of a semicircular engine shed with stalls fanning out from a central turntable",
      tags=["engine shed", "turntable", "locomotive depot", "steam", "stalls", "train depot"])
def _(S):
    spokes = [detail(seg(*rail_icon_pt(12, 20, 5, a), *rail_icon_pt(12, 20, 10, a))) for a in (210, 240, 270, 300, 330)]
    return [
        shell("M2 20A10 10 0 0 1 22 20Z"),
        *spokes,
        dot(12, 20, 2.5),
    ]


@icon("coaling-tower", CAT, "Tall tower on legs standing over a railway track with a chute tilted down and coal falling",
      tags=["coal", "locomotive", "steam", "fuelling", "depot", "railway yard"])
def _(S):
    return [
        shell(poly([(5, 2), (14, 2), (14, 11), (5, 11)], closed=True, r=S.r * 0.6)),
        line(seg(6, 11, 6, 21)), line(seg(13, 11, 13, 21)),
        line(seg(2, 21.5, 22, 21.5)),
        line(seg(14, 7, 19.5, 11.5)),
        dot(20, 15, 1.1), dot(21, 18.3, 1),
    ]


@icon("train-shed", CAT, "Front view of a large arched glass roof with ribs fanning out over the station platforms",
      tags=["station", "terminus", "arched roof", "glass roof", "platforms", "concourse"])
def _(S):
    ribs = [line(seg(*rail_icon_pt(12, 13, 4, a), *rail_icon_pt(12, 13, 9, a))) for a in (225, 270, 315)]
    return [
        line("M3 21V13A9 9 0 0 1 21 13V21"),
        *ribs,
        line(seg(2, 21.5, 22, 21.5)),
        line(seg(8, 21, 8, 16.5)), line(seg(16, 21, 16, 16.5)),
    ]


@icon("hump-yard", CAT, "Track rising over a small hill with a single wagon rolling down the far slope into fanning tracks",
      tags=["marshalling yard", "classification yard", "freight", "shunting", "gravity", "wagon"])
def _(S):
    wag = rot([(-2.5, -1.8), (2.5, -1.8), (2.5, 1.8), (-2.5, 1.8)], 58, 0, 0)
    wag = [(x + 16.6, y + 10.6) for x, y in wag]
    return [
        line(poly([(2, 20), (9, 9), (12, 9), (17, 17)], r=S.r)),
        line(seg(17, 17, 22, 13.5)), line(seg(17, 17, 22, 17)), line(seg(17, 17, 22, 20.5)),
        solid(poly(wag, closed=True)),
    ]


@icon("loading-gauge", CAT, "Hoop-shaped frame standing over a railway track marking the largest load that may pass",
      tags=["clearance", "height limit", "width limit", "structure gauge", "tunnel", "freight"])
def _(S):
    return [
        line(poly([(4, 21), (4, 10), (8, 4), (16, 4), (20, 10), (20, 21)], r=S.r)),
        line(seg(9, 21, 9, 12)), line(seg(15, 21, 15, 12)),
        line(seg(9, 15, 15, 15)), line(seg(9, 19, 15, 19)),
    ]


@icon("transfer-table", CAT, "Top view of a movable bridge section that slides sideways on rails between parallel tracks",
      tags=["traverser", "shed", "sliding platform", "rail yard", "parallel tracks", "workshop"])
def _(S):
    return [
        line(seg(2, 4, 22, 4)), line(seg(2, 20, 22, 20)),
        line(seg(5, 4, 5, 20)), line(seg(19, 4, 19, 20)),
        shell(poly([(9, 7), (15, 7), (15, 17), (9, 17)], closed=True, r=S.r * 0.6)),
        detail(seg(12, 7, 12, 17)),
    ]


@icon("train-wash", CAT, "Train front passing between two tall rotating brushes with water drops",
      tags=["carriage wash", "cleaning", "depot", "brushes", "maintenance", "wash plant"])
def _(S):
    return [
        shell(rect(2, 7, 3, 12, min(S.R, 1.5))),
        shell(rect(19, 7, 3, 12, min(S.R, 1.5))),
        shell(rect(8, 5, 8, 14, min(S.R, 3))),
        sq(10, 7.5, 4, 3),
        dot(10.5, 15.5, 1), dot(13.5, 15.5, 1),
        dot(3.5, 3.5, 1), dot(20.5, 3.5, 1),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("wye-junction", CAT, "Three tracks joined in a triangle used to turn trains around",
      tags=["triangle junction", "turning", "reverse", "track layout", "railway", "wye"])
def _(S):
    return [
        line(poly([(12, 6), (4, 17), (20, 17)], closed=True, r=S.r)),
        line(seg(12, 6, 12, 2.5)),
        line(seg(4, 17, 2.5, 21)), line(seg(20, 17, 21.5, 21)),
    ]


@icon("passing-loop", CAT, "Single track that splits into two parallel tracks for a short length and then rejoins",
      tags=["passing place", "crossing loop", "track layout", "single track", "railway", "overtaking"])
def _(S):
    return [
        line(seg(2, 12, 6, 12)), line(seg(18, 12, 22, 12)),
        line(poly([(6, 12), (9, 7), (15, 7), (18, 12)], r=S.r)),
        line(poly([(6, 12), (9, 17), (15, 17), (18, 12)], r=S.r)),
    ]


@icon("balloon-loop", CAT, "Track ending in a large round loop that lets trains turn back without reversing",
      tags=["turning loop", "reversing loop", "terminus", "tram", "track layout", "railway"])
def _(S):
    return [
        line("M12 22V18Q4 16 4 9.5A8 8 0 0 1 20 9.5Q20 16 12 18"),
    ]


@icon("railway-siding", CAT, "Main track with a short branch that leads off it and ends at a buffer stop",
      tags=["side track", "spur", "branch", "buffer stop", "track layout", "railway"])
def _(S):
    return [
        line(seg(2, 17, 22, 17)),
        line(poly([(6, 17), (10, 9), (20, 9)], r=S.r)),
        line(seg(21, 5.5, 21, 12.5)),
    ]


@icon("railway-junction", CAT, "One straight track with a second track curving away from it to one side like a Y",
      tags=["branch line", "fork", "points", "track layout", "diverging", "railway"])
def _(S):
    return [
        line(seg(9, 22, 9, 2)),
        line(poly([(9, 18), (9, 13), (19, 3)], r=S.r)) if False else line(poly([(9, 17), (9, 14), (19, 4)], r=S.r)),
    ]


# ---------------------------------------------------------------------------- track layout and earthworks

@icon("track-crossover", CAT, "Two parallel tracks joined by a single diagonal track between them",
      tags=["crossover", "track layout", "points", "cross connection", "railway", "switch"])
def _(S):
    return [
        line(seg(2, 6, 22, 6)), line(seg(2, 18, 22, 18)),
        line("M5 6H8Q12 6 12 12T16 18H19") if False else line("M7 6Q12 6 12 12T17 18"),
    ]


@icon("railway-cutting", CAT, "Cross section of a railway track at the bottom of a V-shaped cut with sloping sides",
      tags=["excavation", "trench", "earthworks", "slope", "track", "embankment"])
def _(S):
    return [
        line(poly([(2, 3), (6, 19), (18, 19), (22, 3)], r=S.r)),
        line(seg(9, 6, 9, 15.5)), line(seg(15, 6, 15, 15.5)),
        line(seg(9, 9.5, 15, 9.5)),
    ]


@icon("railway-embankment", CAT, "Cross section of a railway track on top of a tall flat-topped mound of earth",
      tags=["raised track", "earthworks", "mound", "fill", "slope", "ground"])
def _(S):
    return [
        shell(poly([(3, 21), (7, 13.5), (17, 13.5), (21, 21)], closed=True, r=S.r)),
        sq(9.5, 4.5, 2, 5), sq(12.5, 4.5, 2, 5),
        line(seg(8, 9.5, 16, 9.5)),
    ]


# ============================================================================ trackside equipment

@icon("mail-bag-catcher", CAT, "Trackside post with an arm holding a mail sack ready to be snatched by a passing train",
      tags=["mail pickup", "postal", "sack", "post office", "steam era", "trackside"])
def _(S):
    return [
        line(seg(4, 21, 4, 3)),
        line(seg(4, 4, 13, 4)),
        line(seg(12, 4, 12, 8)),
        shell(poly([(9.5, 8), (14.5, 8), (16, 17), (8, 17)], closed=True, r=S.r)),
        line(seg(20, 3, 20, 21)),
    ]


@icon("train-horn", CAT, "Cluster of three trumpet-shaped air horns of different lengths on a bracket",
      tags=["air horn", "locomotive", "signal", "sound", "warning", "klaxon"])
def _(S):
    parts = [line(seg(3, 3, 3, 21))]
    for y, L in ((5, 21), (12, 17.5), (19, 14)):
        parts.append(shell(poly([(5, y - 0.6), (L - 6, y - 0.6), (L, y - 2), (L, y + 2), (L - 6, y + 0.6), (5, y + 0.6)],
                                closed=True, r=S.r * 0.4)))
    return parts


@icon("locomotive-bell", CAT, "Bell hanging in a U-shaped yoke with a pull rope, as mounted on a locomotive",
      tags=["bell", "steam", "warning", "yoke", "alarm", "rope"])
def _(S):
    return [
        line(poly([(4, 16), (4, 3), (20, 3), (20, 16)], r=S.r)),
        line(seg(12, 3, 12, 6)),
        shell("M12 6C9.5 6 9.5 10 9 13L7 17H17L15 13C14.5 10 14.5 6 12 6Z"),
        line(seg(12, 17, 12, 20.5)),
        dot(12, 21, 1.1),
    ]


@icon("train-tail-lamp", CAT, "Rear end of a train carriage with a window and a single round lamp at the bottom center",
      tags=["rear light", "last carriage", "red lamp", "rear of train", "marker lamp", "end of train"])
def _(S):
    return [
        shell(poly([(5, 21), (5, 7), (8, 3), (16, 3), (19, 7), (19, 21)], closed=True, r=S.r)),
        sq(8.5, 8, 7, 4),
        dot(12, 16.5, 2.2),
    ]


@icon("end-of-train-device", CAT, "Small box with a flashing light on top clamped to the coupler at the end of a freight wagon",
      tags=["eot", "ftd", "rear marker", "freight", "flashing light", "telemetry"])
def _(S):
    parts = [dot(12, 8.5, 2.2)]
    for a in (225, 270, 315):
        parts.append(line(seg(*rail_icon_pt(12, 8.5, 4, a), *rail_icon_pt(12, 8.5, 6, a))))
    parts += [
        shell(rect(5, 13, 14, 8, S.R)),
        sq(8, 16, 3, 2), dot(15, 17, 1),
    ]
    return parts


@icon("train-cab", CAT, "Train driver's desk seen from behind with a curved windshield, a dial and a throttle lever",
      tags=["driver", "cockpit", "control desk", "driving cab", "locomotive", "dashboard"])
def _(S):
    return [
        shell(poly([(3, 11), (6, 3), (18, 3), (21, 11)], closed=True, r=S.r)),
        shell(rect(2, 13, 20, 8, min(S.R, 3))),
        dot(7, 17.2, 1.8),
        detail(seg(12, 18.5, 16, 15.5)),
        dot(17, 15, 1.2),
    ]


@icon("dead-mans-handle", CAT, "Train throttle handle with a spring-loaded button on top that must be held down",
      tags=["deadman", "vigilance", "driver safety", "throttle", "control", "locomotive"])
def _(S):
    return [
        shell(rect(6, 9, 8, 12, min(S.R, 3))),
        shell(rect(8, 3, 4, 4, min(S.R, 1.5))),
        detail(seg(6, 13, 14, 13)), detail(seg(6, 17, 14, 17)),
        line(seg(19, 3, 19, 10)),
        line(poly([(16.5, 7.5), (19, 10.5), (21.5, 7.5)], r=S.r)),
    ]


@icon("wheelset", CAT, "Front view of two flanged rail wheels joined by an axle and resting on two short rails",
      tags=["axle", "bogie", "wheels", "undercarriage", "rolling stock", "flange"])
def _(S):
    return [
        shell(poly([(3, 4), (6, 4), (6, 17), (3, 17)], closed=True, r=S.r * 0.8)),
        shell(poly([(18, 4), (21, 4), (21, 17), (18, 17)], closed=True, r=S.r * 0.8)),
        line(seg(6, 10.5, 18, 10.5)),
        sq(2, 18.5, 5, 3), sq(17, 18.5, 5, 3),
    ]


@icon("train-buffers", CAT, "Carriage end with two round spring buffers on either side of a coupling hook",
      tags=["buffer", "bumper", "coupling", "shock absorber", "rolling stock", "end beam"])
def _(S):
    return [
        shell(poly([(2, 3), (22, 3), (22, 10), (2, 10)], closed=True, r=S.r)),
        shell(circle(6.5, 15.5, 3.2)),
        shell(circle(17.5, 15.5, 3.2)),
        line("M12 10V17Q12 20 15 20"),
    ]


@icon("brake-hose-coupling", CAT, "Two flexible air brake hoses hanging down with their metal heads locked together",
      tags=["air brake", "pneumatic", "glad hand", "hose", "coupling", "freight"])
def _(S):
    return [
        line("M6 2Q6 11 10 13"), line("M18 2Q18 11 14 13"),
        shell(poly([(8, 13), (16, 13), (16, 19), (8, 19)], closed=True, r=S.r * 0.6)),
        detail(seg(12, 13, 12, 19)),
    ]


@icon("hand-signal-flags", CAT, "Two flags on short sticks crossed at the handles",
      tags=["flag signal", "red flag", "green flag", "all clear", "stop", "guard"])
def _(S):
    return [
        line(seg(14, 21, 8, 4)), line(seg(10, 21, 16, 4)),
        shell(poly([(8, 4), (2.5, 4.5), (2.5, 10.5), (10, 10)], closed=True, r=S.r * 0.5)),
        shell(poly([(16, 4), (21.5, 4.5), (21.5, 10.5), (14, 10)], closed=True, r=S.r * 0.5)),
    ]


@icon("train-derailment", CAT, "Rail carriage tilted off the track with its wheels in the air above the rails",
      tags=["accident", "crash", "off the rails", "incident", "wreck", "disaster"])
def _(S):
    body = rot([(4, 3), (20, 3), (20, 12), (4, 12)], -14, 12, 9)
    wh = rot([(8, 14.5), (16, 14.5)], -14, 12, 9)
    return [
        shell(poly(body, closed=True, r=S.r * 0.6)),
        *[dot(x, y, 1.7) for x, y in wh],
        line(seg(2, 21, 8, 21)), line(seg(12, 21, 22, 21)),
    ]


# ============================================================================ crew and people

def _torso(cx, w=7, top=11.5, bottom=21, S=None):
    k = S.r if S else 0
    return poly([(cx - w, bottom), (cx - w, top + 2), (cx - w + 2.5, top), (cx + w - 2.5, top), (cx + w, top + 2), (cx + w, bottom)],
                closed=True, r=k)


@icon("track-worker", CAT, "Figure in a hard hat and striped safety vest holding a spike maul",
      tags=["rail worker", "maintenance", "gandy dancer", "high visibility", "hard hat", "section hand"])
def _(S):
    return [
        shell(circle(9, 7.5, 2.4)),
        line(arc(9, 6.2, 3.8, 180, 360)),
        line(seg(4.2, 6.2, 13.8, 6.2)),
        shell(_torso(9, 5.5, 11.5, 21, S)),
        detail(seg(7, 11.5, 7, 21)), detail(seg(11, 11.5, 11, 21)),
        line(seg(14.5, 14, 19, 7)),
        solid(poly([(17, 7), (19.5, 4.5), (22, 6.5), (19.5, 9)], closed=True)),
    ]


@icon("station-master", CAT, "Figure in a peaked cap with a badge and a buttoned jacket holding a pocket watch",
      tags=["stationmaster", "railway official", "uniform", "pocket watch", "conductor", "dispatcher"])
def _(S):
    return [
        shell(circle(10, 8, 2.6)),
        solid(poly([(6.6, 6.2), (13.4, 6.2), (12.6, 3), (7.4, 3)], closed=True)),
        line(seg(6, 6.4, 14.5, 6.4)),
        shell(_torso(10, 6, 12, 21, S)),
        detail(seg(10, 12.5, 10, 21)),
        dot(13, 16, 0.9), dot(13, 19, 0.9),
        shell(circle(19.4, 17.5, 1.6)),
        line(seg(16, 16, 18, 16.8)),
    ]


@icon("train-guard", CAT, "Figure in a cap with a whistle at the lips raising a small flag",
      tags=["conductor", "whistle", "flag", "railway staff", "departure", "guard"])
def _(S):
    return [
        shell(circle(9, 8, 2.6)),
        solid(poly([(5.6, 6.2), (12.4, 6.2), (11.6, 3), (6.4, 3)], closed=True)),
        line(seg(5, 6.4, 13.5, 6.4)),
        dot(13.6, 9, 1),
        shell(_torso(9, 6, 12, 21, S)),
        line(poly([(15, 14.5), (18, 11), (18, 3)], r=S.r)),
        shell(poly([(18, 3), (22, 4.5), (18, 7)], closed=True, r=S.r * 0.4)),
    ]


@icon("railway-porter", CAT, "Figure in a cap pushing a flat two-wheeled barrow loaded with suitcases",
      tags=["luggage", "baggage handler", "station", "trolley", "suitcases", "attendant"])
def _(S):
    return [
        shell(circle(6, 7.5, 2.4)),
        solid(poly([(3, 5.8), (9, 5.8), (8.3, 3), (3.7, 3)], closed=True)),
        shell(_torso(6, 3.5, 11, 21, S)),
        line(seg(8.5, 14, 12, 16.5)),
        line(seg(11, 16.5, 22, 16.5)),
        shell(rect(13.5, 10.5, 8, 5, 1)),
        shell(rect(14.5, 6, 6, 3.2, 1)),
        line(poly([(16.5, 6), (16.5, 4), (18.5, 4), (18.5, 6)])),
        dot(17, 19.6, 2.2),
    ]


@icon("platform-mirror", CAT, "Large round convex mirror on a tall post at the end of a platform",
      tags=["convex mirror", "safety mirror", "guard", "dispatch", "station", "dispatch mirror"])
def _(S):
    return [
        shell(circle(12, 8.5, 6.5) if S.name == "rounded" else poly(regular(12, 8.5, 6.8, 12, start=-90), closed=True)),
        detail(arc(12, 8.5, 3.2, 200, 290)),
        line(seg(12, 15, 12, 21)),
        line(seg(7, 21.5, 17, 21.5)),
    ]


@icon("trainspotting", CAT, "Train front above a notebook and a pair of binoculars",
      tags=["train spotter", "hobby", "enthusiast", "observing", "notebook", "binoculars"])
def _(S):
    return [
        shell(rect(7, 2, 10, 7, min(S.R, 2))),
        sq(9, 4, 6, 2),
        shell(poly([(3, 12), (11, 12), (11, 21), (3, 21)], closed=True, r=S.r)),
        detail(seg(5.5, 16, 8.5, 16)),
        shell(circle(15.3, 17, 2.2)), shell(circle(19, 17, 2.2)),
        line(seg(15.3, 14.8, 15.3, 12)), line(seg(19, 14.8, 19, 12)),
    ]


@icon("screw-coupling", CAT, "Hook at each end of a short chain with a central turnbuckle and a weighted handle",
      tags=["turnbuckle", "buffer coupling", "wagon coupling", "link", "chain", "shunting"])
def _(S):
    return [
        line(poly([(8, 12), (4, 12), (2, 9.5)], r=S.r)),
        line(poly([(16, 12), (20, 12), (22, 9.5)], r=S.r)),
        shell(poly([(8, 9), (16, 9), (16, 15), (8, 15)], closed=True, r=S.r * 0.6)),
        detail(seg(12, 9, 12, 15)),
        line(seg(12, 15, 12, 18)),
        dot(12, 20, 1.8),
    ]


@icon("hot-box-detector", CAT, "Low trackside box aiming wavy heat lines up at the axle of a passing wheel",
      tags=["axle box", "overheat", "wayside detector", "bearing", "sensor", "safety"])
def _(S):
    return [
        shell(circle(16.5, 8, 4.2)),
        dot(16.5, 8, 1.3),
        line(seg(11, 15.5, 22, 15.5)),
        shell(rect(2, 17.5, 9, 4, min(S.R, 1.5))),
        line("M5 15.5Q3.5 13.5 5 11.5T5 7.5"), line("M8.5 15.5Q7 13.5 8.5 11.5T8.5 7.5"),
    ]


@icon("shunting-pole", CAT, "Long pole with a curved metal hook at its tip lifting a chain between two wagon ends",
      tags=["coupling pole", "hook", "yard", "chain", "uncoupling", "tool"])
def _(S):
    return [
        line(seg(2, 21, 16, 7)),
        line("M16 7Q16 3 20 4Q22.5 5 21 8"),
        dot(20.5, 12, 1.2), dot(20.5, 15.5, 1.2), dot(20.5, 19, 1.2),
    ]


@icon("wagon-weighbridge", CAT, "Rail wagon standing on a short track section over a platform scale with a dial beside it",
      tags=["scale", "weighing", "freight", "load", "dial gauge", "weight"])
def _(S):
    return [
        shell(rect(2, 4, 13, 8, min(S.R, 2))),
        dot(5.5, 14.3, 1.5), dot(11.5, 14.3, 1.5),
        line(seg(2, 18, 15, 18)),
        line(seg(4, 18, 4, 21)), line(seg(13, 18, 13, 21)),
        shell(circle(18, 8, 2.8)),
        detail(seg(18, 8, 19.5, 6.5)),
        line(seg(18, 11, 18, 21)),
    ]


@icon("rotary-car-dumper", CAT, "Large ring cradle holding a wagon upside down with coal pouring out below",
      tags=["coal", "tippler", "unloading", "bulk", "port", "wagon tipper"])
def _(S):
    return [
        line(circle(12, 9.5, 7.3) if S.name == "rounded" else poly(regular(12, 9.5, 7.5, 12, start=-90), closed=True)),
        shell(poly([(8.5, 8), (15.5, 8), (15.5, 12.5), (8.5, 12.5)], closed=True, r=S.r * 0.7)),
        dot(10.5, 18.6, 0.9), dot(13.5, 18.6, 0.9),
        solid(poly([(6, 22), (10, 20.5), (14, 20.5), (18, 22)], closed=True)),
    ]


@icon("tank-locomotive", CAT, "Small steam engine with flat water tanks along its boiler and a cab, with no tender",
      tags=["steam", "shunter", "saddle tank", "engine", "heritage", "locomotive"])
def _(S):
    return [
        solid(poly([(4, 2.5), (9, 2.5), (8, 8), (5, 8)], closed=True)),
        shell(rect(3, 8, 12, 8, min(S.R, 3))),
        shell(rect(15, 5, 6, 11, min(S.R, 3))),
        sq(16.5, 7.5, 3, 3),
        *wheels(6, 11, 18, y=19.5, r=2),
    ]
