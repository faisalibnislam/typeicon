"""TypeIcon Core: infrastructure 005 (rail and road equipment, signs, airport and mobility services)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "infrastructure"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def tri(pts) -> Part:
    """Small solid polygon: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", poly(pts, closed=True))


def cut(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def ground(x1=2, x2=22, y=21):
    return line(seg(x1, y, x2, y))


# ============================================================================ rail and road equipment

@icon("emergency-brake-handle", CAT, "Wall box with a pull handle hanging below it on two links and a down arrow on the box",
      tags=["emergency stop", "pull handle", "train", "alarm", "safety", "brake", "communication cord"])
def _(S):
    return [
        shell(rect(4, 2, 16, 9, S.R)),
        detail("M12 4.5V8.5"), detail("M10.25 6.75L12 8.5L13.75 6.75"),
        line(seg(9.5, 11, 9.5, 16)), line(seg(14.5, 11, 14.5, 16)),
        shell(rect(6, 16, 12, 5, L(S, 1, 2.5))),
    ]


@icon("tire-spikes", CAT, "Row of sharp steel teeth set in a low road strip",
      tags=["spike strip", "tyre killer", "one way", "traffic control", "barrier", "parking", "security"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 15), (6, 7), (9, 15), (12, 7), (15, 15), (18, 7), (21, 15), (21, 21)], closed=True, r=S.r)),
    ]


@icon("queue-stanchion", CAT, "Two posts with round tops and feet joined by a sagging belt",
      tags=["belt barrier", "crowd control", "line", "queue", "airport", "retractable", "rope"])
def _(S):
    return [
        line(seg(5, 7, 5, 20)), line(seg(19, 7, 19, 20)),
        dot(5, 5, 2), dot(19, 5, 2),
        line("M5 9Q12 17 19 9"),
        ground(2, 8, 21), ground(16, 22, 21),
    ]


@icon("wayfinding-totem", CAT, "Tall slim pillar sign with a small map panel above two direction arrows",
      tags=["directory", "signpost", "info pillar", "kiosk", "campus", "navigation", "stele"])
def _(S):
    return [
        shell(rect(6, 2, 12, 19, L(S, 1, 3))),
        sq(9, 5, 6, 4, 0.5),
        tri([(9, 12), (13, 12), (15, 13.75), (13, 15.5), (9, 15.5)]),
        tri([(15, 17), (11, 17), (9, 18.75), (11, 20.5), (15, 20.5)]) if False else tri([(15, 16.5), (11, 16.5), (9.5, 18.25), (11, 20), (15, 20)]),
    ]


@icon("breakdown-triangle", CAT, "Triangle outline with a solid reflective centre standing on two folded legs",
      tags=["warning triangle", "hazard", "roadside", "emergency", "reflector", "car trouble", "breakdown"])
def _(S):
    return [
        shell(poly([(12, 2), (21, 16), (3, 16)], closed=True, r=S.r)),
        tri([(12, 7.5), (15.5, 13), (8.5, 13)]),
        line(seg(6, 16, 4, 21)), line(seg(18, 16, 20, 21)),
    ]


@icon("bike-repair-station", CAT, "Post with an arm that holds a bicycle by its saddle, small tool head on the post",
      tags=["bicycle", "fix it", "pump", "tools", "cycling", "service stand", "public repair"])
def _(S):
    return [
        line(seg(20, 3, 20, 21)),
        line(seg(20, 4, 9, 4)),
        line(seg(9, 4, 9, 9)),
        line(poly([(4.5, 17), (8, 9), (13.5, 17)], r=S.r)),
        line(poly([(13.5, 17), (12, 9), (14.5, 8.5)], r=S.r)),
        shell(circle(4.5, 17.5, 2.5)), shell(circle(13.5, 17.5, 2.5)),
    ]


@icon("parking-fine", CAT, "Paper fine slip with a large P, a price line and a torn zigzag bottom edge",
      tags=["parking ticket", "penalty", "citation", "violation", "traffic warden", "fee", "receipt"])
def _(S):
    return [
        shell(poly([(5, 2), (19, 2), (19, 22), (16, 20), (13.5, 22), (10.5, 20), (8, 22), (5, 20)], closed=True, r=S.r)),
        detail("M9.5 12V6H12a2 2 0 0 1 0 4H9.5"),
        detail(seg(9.5, 15, 14.5, 15)),
    ]


@icon("airport-lounge", CAT, "Armchair with a small aeroplane above it",
      tags=["waiting area", "business class", "vip", "seating", "terminal", "departure lounge", "first class"])
def _(S):
    return [
        line(seg(12, 2, 12, 8.5)),
        line(poly([(7, 7), (12, 4.5), (17, 7)], r=S.r)),
        shell(poly([(5, 12), (19, 12), (19, 15), (21, 15), (21, 19), (3, 19), (3, 15), (5, 15)], closed=True, r=S.r)),
        line(seg(6, 19, 6, 21)), line(seg(18, 19, 18, 21)),
    ]


@icon("car-rental", CAT, "Small car seen from the front beside a key with a round bow",
      tags=["rent a car", "hire car", "key", "vehicle hire", "booking", "rental car", "drive"])
def _(S):
    return [
        line(poly([(3.5, 11), (5, 6), (11, 6), (12.5, 11)], r=S.r)),
        shell(rect(2, 11, 12, 7, min(S.R, 2))),
        dot(5, 14.5, 1), dot(11, 14.5, 1),
        sq(3.5, 18, 2.5, 2.5), sq(10, 18, 2.5, 2.5),
        shell(circle(19, 5.5, 2.5)),
        line(seg(19, 8, 19, 21)),
        line(seg(19, 16.5, 21.5, 16.5)), line(seg(19, 19.5, 21.5, 19.5)),
    ]


@icon("signal-lever", CAT, "Tall railway lever with a grip and a latch rod rising from a floor frame",
      tags=["interlocking", "points lever", "signal box", "railway", "switch", "control", "frame"])
def _(S):
    return [
        shell(rect(4, 18, 16, 3, min(S.R, 1.5))),
        line(seg(10, 18, 10, 9)),
        shell(rect(8, 3, 4, 6, L(S, 0.5, 2))),
        line(seg(12, 5, 15, 5)), line(seg(15, 5, 15, 18)),
    ]


@icon("rail-profile", CAT, "Cross section of a railway rail with a rounded head, thin web and wide foot",
      tags=["railway", "track", "steel", "section", "permanent way", "iron rail", "engineering"])
def _(S):
    return [
        shell(poly([(7, 3), (17, 3), (17, 7), (14, 9.5), (14, 16), (21, 18.5), (21, 21), (3, 21), (3, 18.5), (10, 16), (10, 9.5), (7, 7)], closed=True, r=S.r)),
    ]


# ============================================================================ road signs and vehicles

def warn_tri(S):
    """Warning triangle sign outline (apex up)."""
    return shell(poly([(12, 3), (22, 20), (2, 20)], closed=True, r=S.r))


def no_sign():
    return [shell(circle(12, 12, 9)), line(seg(5.6, 5.6, 18.4, 18.4))]


@icon("tank-container", CAT, "Cylindrical tank held inside a rectangular steel frame",
      tags=["iso tank", "liquid cargo", "freight", "chemical", "shipping", "bulk", "intermodal"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, L(S, 0.5, 2.5))),
        detail(rect(6, 8, 12, 8, 4)),
        detail(seg(10, 8, 10, 16)), detail(seg(14, 8, 14, 16)),
    ]


@icon("no-idling-sign", CAT, "Round prohibition sign with a car tailpipe puffing smoke, crossed by a slash",
      tags=["engine off", "exhaust", "pollution", "emissions", "turn off engine", "anti idling", "no smoke"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        sq(5.5, 13, 5, 3, L(S, 0, 1)),
        tri([(10.5, 13), (13, 11), (13, 18), (10.5, 16)]),
        dot(16, 10.5, L(S, 1.25, 1.5)), dot(18, 13.5, L(S, 1.25, 1.5)),
        detail(seg(5.6, 5.6, 18.4, 18.4)),
    ]


@icon("no-phone-driving-sign", CAT, "Round prohibition sign with a phone and a steering wheel on either side of a slash",
      tags=["distracted driving", "no mobile", "hands free", "texting", "road safety", "cell phone", "driver"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        sq(14.5, 6.5, 3.5, 6.5, L(S, 0.5, 1.5)),
        detail(circle(9, 15, 3)),
        detail(seg(5.6, 5.6, 18.4, 18.4)),
    ]


@icon("car-sharing", CAT, "Car front with two heads joined by a link line above its roof",
      tags=["carpool", "ride share", "passengers", "shared ride", "rideshare", "share a car", "commute"])
def _(S):
    return [
        dot(7, 4.5, 2), dot(17, 4.5, 2), line(seg(9.5, 4.5, 14.5, 4.5)),
        line(poly([(5, 13), (7, 9), (17, 9), (19, 13)], r=S.r)),
        shell(rect(3, 13, 18, 7, min(S.R, 2))),
        dot(7, 16.5, 1.25), dot(17, 16.5, 1.25),
    ]


@icon("vertiport", CAT, "Top view of a round landing pad with a large V and four corner lights",
      tags=["evtol", "air taxi", "landing pad", "drone port", "urban air mobility", "helipad", "vtol"])
def _(S):
    return [
        shell(circle(12, 12, 8)),
        detail(poly([(8.5, 8.5), (12, 15.5), (15.5, 8.5)], r=S.r)),
        dot(3.5, 3.5, 1.25), dot(20.5, 3.5, 1.25), dot(3.5, 20.5, 1.25), dot(20.5, 20.5, 1.25),
    ]


@icon("driving-license", CAT, "Card with a portrait on the left and a small car over text lines on the right",
      tags=["driver licence", "drivers license", "id card", "permit", "dmv", "driving permit", "identity"])
def _(S):
    return [
        shell(rect(2, 5, 20, 14, S.R)),
        dot(7, 10, 1.75), detail("M4.5 16a2.5 2.5 0 0 1 5 0"),
        detail(seg(13, 9, 19, 9)), detail(seg(13, 12, 17, 12)),
        sq(13, 14.5, 6, 2, 0.5),
    ]


@icon("bike-stair-ramp", CAT, "Flight of steps with a narrow wheeling groove beside it and a bicycle wheel on the groove",
      tags=["wheeling ramp", "stairs", "bicycle", "cycling", "accessibility", "channel", "underpass"])
def _(S):
    return [
        shell(poly([(2, 21), (2, 17), (7, 17), (7, 13), (12, 13), (12, 9), (17, 9), (17, 5), (22, 5), (22, 21)], closed=True, r=S.r)),
        line(seg(3, 12.5, 12, 5.5)),
        shell(circle(5.5, 6, 2.5)),
    ]


@icon("ropeway-pylon", CAT, "Tall tower with a crossbar on top carrying two rollers under a cable",
      tags=["cable car", "gondola", "aerial tramway", "support tower", "lift", "mountain", "ski lift"])
def _(S):
    return [
        line(seg(2, 2.5, 22, 2.5)),
        dot(7, 5.25, 1.75), dot(17, 5.25, 1.75),
        line(seg(4, 8.5, 20, 8.5)),
        line(seg(9, 8.5, 6, 21)), line(seg(15, 8.5, 18, 21)),
        line(seg(7.4, 15, 16.6, 15)),
        line(seg(7.4, 15, 18, 21)), line(seg(16.6, 15, 6, 21)),
    ]


@icon("luggage-scale", CAT, "Round hanging scale with a hook lifting a suitcase by its handle",
      tags=["baggage weight", "suitcase", "weigh", "travel", "airline", "hanging scale", "bag allowance"])
def _(S):
    return [
        shell(circle(12, 6, 4)),
        detail(seg(12, 6, 14, 4.5)),
        line(seg(12, 10, 12, 12)),
        line(poly([(9.5, 14), (9.5, 12), (14.5, 12), (14.5, 14)], r=S.r)),
        shell(rect(4, 14, 16, 7, S.R)),
        detail(seg(9, 16.5, 9, 18.5)), detail(seg(15, 16.5, 15, 18.5)),
    ]


@icon("e-passport-gate", CAT, "Cabinet with a camera lens and passport slot beside a glass door panel with shine lines",
      tags=["border control", "automated gate", "immigration", "passport control", "biometric", "airport", "smart gate"])
def _(S):
    return [
        shell(rect(2, 3, 8, 18, L(S, 1, 3))),
        dot(6, 7, 1.75),
        sq(4, 13, 4, 2, 0.5),
        shell(rect(14, 6, 8, 15, L(S, 0, 2))),
        detail(seg(16.5, 16, 19.5, 11)),
    ]


@icon("security-wand", CAT, "Handheld metal detector with a wide paddle head, a row of lights and a short grip",
      tags=["metal detector", "airport security", "screening", "scanner", "checkpoint", "search", "paddle"])
def _(S):
    return [
        shell(rect(3, 3, 18, 8, L(S, 2, 4))),
        dot(8, 7, 1), dot(12, 7, 1), dot(16, 7, 1),
        shell(rect(10, 11, 4, 10, L(S, 0.5, 1.5))),
    ]


@icon("overhead-cables-sign", CAT, "Warning triangle with a lightning bolt under a line of hanging wires",
      tags=["power lines", "electric hazard", "overhead wires", "high voltage", "road sign", "low clearance", "danger"])
def _(S):
    return [
        warn_tri(S),
        detail(seg(8.5, 11.5, 15.5, 11.5)),
        tri([(13, 13), (9.5, 16.25), (11.5, 16.25), (10.5, 18.5), (14.5, 14.75), (12.5, 14.75)]),
    ]


@icon("farm-vehicles-sign", CAT, "Warning triangle with a tractor in side view, big rear wheel and small front wheel",
      tags=["tractor", "agricultural", "slow vehicle", "farm machinery", "road sign", "rural", "caution"])
def _(S):
    return [
        warn_tri(S),
        dot(9.5, 15.5, 3), dot(15.5, 17, 1.5),
        detail(poly([(9.5, 15.5), (10, 11.5), (13, 11.5), (13, 14.5), (16, 14.5), (15.5, 17)], r=S.r)),
    ]


@icon("radar-scope", CAT, "Round radar screen with a range ring, a sweeping line and two blips",
      tags=["radar screen", "sweep", "air traffic", "sonar", "detection", "scanner", "ping"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(circle(12, 12, L(S, 4.5, 5))),
        line(seg(12, 12, 18, 6)),
        dot(8, 9, 1.25), dot(15.5, 16.5, 1.25),
    ]


@icon("flight-path", CAT, "Two end dots joined by a dashed arc with a small aeroplane above the middle of the arc",
      tags=["route", "flight route", "trajectory", "airline", "travel", "plane", "itinerary"])
def _(S):
    return [
        dot(3, 20, 2), dot(21, 20, 2),
        line(arc(12, 20, 9, 196, 220)), line(arc(12, 20, 9, 232, 248)),
        line(arc(12, 20, 9, 292, 308)), line(arc(12, 20, 9, 320, 344)),
        solid(poly([(16.25, 7.5), (13.28, 6.39), (11.57, 3.25), (10.3, 3.25), (11.15, 6.48), (9.45, 6.48), (8.77, 5.29), (7.92, 5.29), (8.6, 7.5), (7.92, 9.71), (8.77, 9.71), (9.45, 8.52), (11.15, 8.52), (10.3, 11.75), (11.57, 11.75), (13.28, 8.61)], closed=True, r=S.r * 0.3)),
    ]


@icon("traffic-control-room", CAT, "Wall of four screens above a long operator desk",
      tags=["command center", "monitoring", "cctv", "operator", "highway control", "dispatch", "surveillance"])
def _(S):
    return [
        shell(rect(2, 2, 20, 12, S.R)),
        detail(seg(12, 2, 12, 14)), detail(seg(2, 8, 22, 8)),
        shell(rect(4, 17, 16, 3, min(S.R, 1.5))),
        line(seg(6, 20, 6, 21.5)), line(seg(18, 20, 18, 21.5)),
    ]


@icon("traffic-map", CAT, "Map panel with one thick busy road, one thin side road and a dotted slow road",
      tags=["congestion", "live traffic", "route map", "navigation", "road network", "delays", "gps"])
def _(S):
    thick = path_to_d(ST(seg(3, 14, 21, 14), 3.5, "butt", "miter", 4))
    return [
        shell(rect(2, 2, 20, 20, S.R)),
        Part("dot", thick),
        detail(seg(8, 2, 8, 22)),
        dot(14, 7, 1), dot(17, 7, 1), dot(20, 7, 1) if False else dot(14, 10, 1),
    ]


@icon("emergency-vehicles-sign", CAT, "Ambulance seen from the front with a light bar and flashing rays above it",
      tags=["ambulance", "fire engine", "police", "siren", "rescue", "first responders", "station"])
def _(S):
    return [
        shell(rect(3, 10, 18, 11, min(S.R, 3))),
        sq(6, 12.5, 12, 3, 0.5),
        dot(7, 18.25, 1.25), dot(17, 18.25, 1.25),
        sq(9.5, 6.5, 5, 3.5, 1),
        line(seg(7, 5.5, 5, 3.5)), line(seg(17, 5.5, 19, 3.5)), line(seg(12, 4, 12, 2.5)),
    ]


@icon("divided-highway-sign", CAT, "Diamond warning sign with two carriageways split by a narrow median island",
      tags=["dual carriageway", "median", "road sign", "two way", "central reservation", "highway", "end of divided road"])
def _(S):
    return [
        shell(poly([(12, 1.5), (22.5, 12), (12, 22.5), (1.5, 12)], closed=True, r=S.r)),
        detail(seg(8.5, 8.5, 8.5, 16.5)), detail(seg(15.5, 8.5, 15.5, 16.5)),
        sq(11, 9.5, 2, 5),
    ]


@icon("crossroads-sign", CAT, "Warning triangle with a bold plus shaped cross",
      tags=["intersection", "junction", "four way", "road sign", "crossing", "cross road", "caution"])
def _(S):
    return [
        warn_tri(S),
        detail(seg(8.5, 14, 15.5, 14)), detail(seg(12, 10.5, 12, 17.5)),
    ]
