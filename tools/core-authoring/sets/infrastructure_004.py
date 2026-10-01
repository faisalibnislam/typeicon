"""TypeIcon Core: infrastructure (batch 004, road furniture, tolls, borders, signs, bridges, charging).

Conventions: anything drawn inside a closed sign or plate uses `detail` (strokes) or `mark` (small solids) so
that the Filled style knocks it out of the solid body instead of losing it.
"""
from __future__ import annotations

import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "infrastructure"


def mark(d: str) -> Part:
    """Small solid region: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def L(S, a, b):
    """Value for Line/Filled (a) or Rounded (b)."""
    return b if S.name == "rounded" else a


# ============================================================================ road furniture

@icon("pedestrian-guardrail", CAT, "Low railing of vertical bars between two rails along a kerb",
      tags=["railing", "barrier", "pavement", "kerb", "pedestrian safety", "fence", "crowd control"])
def _(S):
    return [line(seg(2, 7, 22, 7)), line(seg(2, 14.5, 22, 14.5)),
            *[line(seg(x, 7, x, 20.5)) for x in (4.5, 9.5, 14.5, 19.5)]]


@icon("speed-cushion", CAT, "Top view of a lane with a square raised pad in the middle and gaps at each side",
      tags=["traffic calming", "speed hump", "road pad", "slow down", "road safety", "lane"])
def _(S):
    return [line(seg(2.5, 2.5, 2.5, 21.5)), line(seg(21.5, 2.5, 21.5, 21.5)),
            shell(rect(8, 8.5, 8, 7, S.R * 0.5)), line(seg(12, 2.5, 12, 4.5)), line(seg(12, 19.5, 12, 21.5))]


@icon("chicane", CAT, "Top view of a road with offset kerb build outs that force the lane to weave",
      tags=["traffic calming", "road narrowing", "build out", "weave", "slow down", "bend", "street"])
def _(S):
    return [line(poly([(3, 2.5), (3, 5), (8, 5), (8, 11), (3, 11), (3, 21.5)], r=S.r)),
            line(poly([(21, 2.5), (21, 13), (16, 13), (16, 19), (21, 19), (21, 21.5)], r=S.r)),
            line("M14 3V6C14 10 10 10 10 14V21")]


@icon("gritting-bin", CAT, "Squat grit bin with a sloping lid and a shovel leaning against it",
      tags=["grit bin", "salt bin", "winter", "ice", "snow", "road maintenance", "shovel"])
def _(S):
    return [shell(poly([(3, 20.5), (3, 9.5), (14, 7), (14, 20.5)], closed=True, r=S.r)),
            detail(seg(3, 13, 14, 11)),
            line(seg(20, 2.5, 19.5, 13)),
            shell(poly([(17.5, 13), (21.5, 13), (20.5, 20.5), (18.5, 20.5)], closed=True, r=S.r * 0.5))]


@icon("weigh-station", CAT, "Truck standing on a flat scale platform",
      tags=["truck scale", "weighbridge", "axle weight", "freight", "inspection", "lorry", "load limit"],
      aliases=["weighbridge"])
def _(S):
    body = [(2.5, 14), (2.5, 5.5), (13, 5.5), (13, 8.5), (16.5, 8.5), (19.5, 11.5), (19.5, 14)]
    return [shell(poly(body, closed=True, r=S.r * 0.5)),
            dot(6.5, 14, 1.75), dot(15.5, 14, 1.75),
            shell(rect(2, 18, 20, 3, S.R * 0.4))]


@icon("toll-gantry", CAT, "Overhead frame across a road with readers and cameras pointing down",
      tags=["toll", "electronic tolling", "camera", "highway", "overhead gantry", "road charging", "anpr"])
def _(S):
    return [line(seg(3.5, 5, 3.5, 21)), line(seg(20.5, 5, 20.5, 21)),
            shell(rect(3, 3, 18, 4.5, S.R * 0.4)),
            mark(rect(7.5, 9, 3.5, 3.5, 0.5)), mark(rect(13, 9, 3.5, 3.5, 0.5)),
            line(seg(12, 14.5, 12, 16.5)), line(seg(12, 19, 12, 21))]


@icon("toll-tag", CAT, "Small transponder stuck to a windscreen sending signal waves",
      tags=["transponder", "e-tag", "electronic toll", "windshield", "rfid", "pass", "windscreen"],
      aliases=["transponder"])
def _(S):
    return [shell(poly([(3, 21), (5.5, 4), (18.5, 4), (21, 21)], closed=True, r=S.r)),
            mark(rect(9.5, 7, 5, 3, 0.5)),
            detail(arc(12, 11.5, 2.5, 50, 130)), detail(arc(12, 11.5, 5.5, 50, 130))]


@icon("toll-ticket", CAT, "Small ticket with a road symbol and a barcode strip",
      tags=["toll pass", "entry ticket", "motorway", "highway ticket", "barcode", "paper ticket", "road fee"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, S.R)),
            detail(seg(9, 11, 10.5, 6)), detail(seg(15, 11, 13.5, 6)),
            *[detail(seg(x, 14.5, x, 18)) for x in (8, 12, 16)]]


@icon("border-crossing", CAT, "Boundary line on the ground with a post on each side and a barrier between them",
      tags=["border", "frontier", "checkpoint", "boundary", "customs", "crossing point", "international"])
def _(S):
    return [line(seg(4, 4, 4, 21)), line(seg(20, 4, 20, 21)),
            shell(rect(4, 8, 16, 4, S.R * 0.4)),
            line(seg(12, 2.5, 12, 5)), line(seg(12, 15, 12, 21))]


@icon("customs-declaration", CAT, "Form with a small suitcase at the top and ruled lines below",
      tags=["customs form", "travel form", "import", "arrival card", "luggage", "border paperwork", "declaration"])
def _(S):
    return [shell(rect(4.5, 2, 15, 20, S.R)),
            mark(rect(8.5, 7, 7, 4.5, 1)), detail(poly([(10.5, 7), (10.5, 5.5), (13.5, 5.5), (13.5, 7)])),
            detail(seg(8, 15, 16, 15)), detail(seg(8, 18.5, 13, 18.5))]


@icon("duty-free", CAT, "Shopping bag with a small aeroplane on its front",
      tags=["airport shop", "tax free", "travel retail", "shopping", "departure", "plane", "bag"])
def _(S):
    return [shell(poly([(5, 8), (19, 8), (20, 21.5), (4, 21.5)], closed=True, r=S.r)),
            line("M9 8V6A3 3 0 0 1 15 6V8"),
            detail(seg(12, 11, 12, 19)), detail(poly([(8, 15.5), (12, 13), (16, 15.5)])),
            detail(poly([(10, 19), (12, 17.5), (14, 19)]))]


@icon("road-works-light", CAT, "Portable two light traffic signal on a wheeled base with a battery box",
      tags=["temporary traffic light", "roadworks", "stop go", "construction", "signal", "portable signal"])
def _(S):
    return [shell(rect(5.5, 2, 7, 10.5, S.R * 0.5)), mark(circle(9, 5.5, 1.4)), mark(circle(9, 9.5, 1.4)),
            line(seg(9, 12.5, 9, 14.5)),
            shell(rect(3, 14.5, 12, 3, S.R * 0.4)),
            mark(circle(6, 20.5, 1.25)), mark(circle(12, 20.5, 1.25)),
            shell(rect(17, 11, 4.5, 7.5, S.R * 0.4))]


@icon("crash-cushion", CAT, "Barrels bunched in front of a barrier end with a striped face",
      tags=["impact attenuator", "highway barrier", "barrels", "road safety", "crash barrier", "gore"])
def _(S):
    return [shell(rect(3, 13, 4, 7.5, S.R * 0.4)), shell(rect(10, 9, 4, 11.5, S.R * 0.4)),
            detail(seg(3, 16.5, 7, 16.5)), detail(seg(10, 12.5, 14, 12.5)), detail(seg(10, 16.5, 14, 16.5)),
            shell(rect(17, 5, 4, 15.5, S.R * 0.4)),
            detail(seg(17, 11, 21, 8)), detail(seg(17, 16, 21, 13))]


@icon("water-filled-barrier", CAT, "Long hollow plastic barrier block with a fill cap on top and water inside",
      tags=["plastic barrier", "road barrier", "traffic barrier", "temporary barrier", "jersey barrier", "blocker"])
def _(S):
    return [shell(poly([(2, 19), (3, 9.5), (21, 9.5), (22, 19)], closed=True, r=S.r)),
            shell(rect(10.5, 5, 3, 4.5, 0.5)),
            detail("M6 14.5Q8 12.5 10 14.5T14 14.5T18 14.5")]


@icon("road-plate", CAT, "Flat steel plate lying over a trench in the road",
      tags=["trench plate", "steel plate", "roadworks", "excavation cover", "temporary road", "utility works"])
def _(S):
    return [line(poly([(2, 14.5), (8, 14.5), (8, 21)], r=S.r)), line(poly([(22, 14.5), (16, 14.5), (16, 21)], r=S.r)),
            shell(rect(4, 10, 16, 3, S.R * 0.4))]


# ============================================================================ tunnels, stations, lifts

@icon("tunnel-fan", CAT, "Round jet fan with three blades hanging under a tunnel ceiling",
      tags=["jet fan", "ventilation", "tunnel", "air flow", "extractor", "road tunnel", "blower"])
def _(S):
    blades = [detail(seg(12, 14, *polar(12, 14, 5.5, a))) for a in (-90, 30, 150)]
    return [line(seg(2, 3, 22, 3)), line(seg(9, 3, 9.4, 8)), line(seg(15, 3, 14.6, 8)),
            shell(circle(12, 14, 6.5)), *blades, dot(12, 14, 1.75)]


@icon("platform-screen-doors", CAT, "Glass wall along a platform edge with a pair of sliding doors in the middle",
      tags=["platform doors", "train platform", "metro", "subway", "safety barrier", "station", "glass wall"])
def _(S):
    return [shell(rect(2, 3.5, 20, 14.5, S.R * 0.5)), detail(seg(7.5, 3.5, 7.5, 18)), detail(seg(16.5, 3.5, 16.5, 18)),
            mark(poly([(9.5, 10.75), (11.75, 8.5), (11.75, 13)], closed=True)),
            mark(poly([(14.5, 10.75), (12.25, 8.5), (12.25, 13)], closed=True)),
            line(seg(2, 21, 22, 21))]


@icon("moving-walkway", CAT, "Flat conveyor walkway with a handrail and a person standing on it",
      tags=["travelator", "moving sidewalk", "airport", "people mover", "conveyor", "autowalk", "accessibility"],
      aliases=["travelator"])
def _(S):
    return [shell(rect(2, 18, 20, 3.5, 1.75)),
            shell(circle(8, 4.5, 2)), line(seg(8, 8, 8, 13.5)),
            line(poly([(8, 13.5), (6.5, 17.5)])), line(poly([(8, 13.5), (9.5, 17.5)])),
            line(poly([(8, 9.5), (10.5, 12)])),
            line(poly([(14, 9), (21, 9), (21, 17)], r=S.r))]


def _rot(pts, deg, c=(12.0, 12.0)):
    a = math.radians(deg)
    return [(c[0] + (x - c[0]) * math.cos(a) - (y - c[1]) * math.sin(a),
             c[1] + (x - c[0]) * math.sin(a) + (y - c[1]) * math.cos(a)) for x, y in pts]


@icon("funicular", CAT, "Cable railway car riding up the sloping track of a hillside",
      tags=["cable railway", "incline", "mountain railway", "hill tram", "steep track", "tram", "tourist"])
def _(S):
    ux, uy = 20 / 25.6, -16 / 25.6
    nx, ny = -16 / 25.6, -20 / 25.6

    def P_(t, h):
        return (2 + ux * t + nx * h, 21 + uy * t + ny * h)
    car = [P_(9, 3.5), P_(18, 3.5), P_(18, 9.5), P_(9, 9.5)]
    w1, w2 = P_(11, 6.5), P_(16, 6.5)
    return [shell(poly([(2, 21), (22, 5), (22, 21)], closed=True, r=S.r), stroke_miterlimit="3"),
            shell(poly(car, closed=True, r=S.r * 0.5)), detail(seg(*w1, *w2))]


@icon("chairlift", CAT, "Two seat chair hanging from a cable on a single arm",
      tags=["ski lift", "chair lift", "ski resort", "mountain", "cable", "gondola", "snow"],
      aliases=["ski-lift"])
def _(S):
    return [line(seg(2, 3.5, 22, 3.5)), line(seg(12, 3.5, 12, 7.5)),
            shell(rect(4, 7.5, 16, 5.5, S.R * 0.5)), detail(seg(12, 7.5, 12, 13)),
            shell(rect(3, 16, 18, 3, S.R * 0.3)),
            line(seg(6, 13, 6, 16)), line(seg(18, 13, 18, 16))]


@icon("cargo-terminal", CAT, "Wide freight building with three loading doors and crates in front",
      tags=["freight terminal", "warehouse", "goods", "logistics", "shipping depot", "cargo", "distribution"])
def _(S):
    return [shell(rect(2, 3, 20, 11.5, S.R * 0.5)),
            mark(rect(4.5, 8, 4, 6.5)), mark(rect(10, 8, 4, 6.5)), mark(rect(15.5, 8, 4, 6.5)),
            shell(rect(3.5, 17, 4.5, 4, 0)), shell(rect(9.5, 17, 4.5, 4, 0)), shell(rect(16, 17, 4.5, 4, 0))]


@icon("loading-dock", CAT, "Raised dock building with a roll up door and a truck trailer backed up to it",
      tags=["dock door", "truck bay", "warehouse", "freight", "delivery", "unloading", "logistics"])
def _(S):
    return [shell(rect(2, 3, 6, 18, S.R * 0.4)), detail(seg(2, 9, 8, 9)), detail(seg(2, 13, 8, 13)),
            shell(rect(8, 8, 14, 9, S.R * 0.4)), dot(14, 19.5, 1.75), dot(19, 19.5, 1.75)]


@icon("intermodal-hub", CAT, "Gantry crane lifting a container down onto a truck",
      tags=["container transfer", "rail to road", "freight", "shipping container", "crane", "logistics", "terminal"])
def _(S):
    return [line(seg(2, 3.5, 22, 3.5)), line(seg(3, 3.5, 3, 21)), line(seg(21, 3.5, 21, 21)),
            line(seg(6, 3.5, 6, 8)), line(seg(10, 3.5, 10, 8)),
            shell(rect(5.5, 8, 6, 4, 0)),
            line(seg(5, 16, 18.5, 16)),
            shell(poly([(14.5, 16), (14.5, 12), (17, 12), (18.5, 14.5), (18.5, 16)], closed=True, r=S.r * 0.4)),
            dot(8, 18.75, 1.5), dot(16, 18.75, 1.5)]


@icon("marina-berth", CAT, "Top view of a floating dock with finger piers and small boats in the slips",
      tags=["marina", "boat slip", "jetty", "harbour", "yacht berth", "mooring", "pontoon"],
      aliases=["boat-slip"])
def _(S):
    def boat(cx):
        return solid(poly([(cx - 1.75, 8.5), (cx + 1.75, 8.5), (cx + 1.75, 15), (cx, 19), (cx - 1.75, 15)], closed=True))
    return [line(seg(2, 4, 22, 4)), line(seg(3.5, 4, 3.5, 20.5)), line(seg(12, 4, 12, 20.5)),
            line(seg(20.5, 4, 20.5, 20.5)), boat(7.75), boat(16.25)]


@icon("boat-lift", CAT, "Wheeled gantry frame with two slings lifting a boat out of the water",
      tags=["travel lift", "boat hoist", "boatyard", "slings", "marine lift", "haul out", "yacht"])
def _(S):
    return [line(seg(2, 3.5, 22, 3.5)), line(seg(3, 3.5, 3, 18.5)), line(seg(21, 3.5, 21, 18.5)),
            line(seg(9, 3.5, 9, 12.5)), line(seg(15, 3.5, 15, 12.5)),
            shell(poly([(6, 12.5), (18, 12.5), (15.5, 17), (8.5, 17)], closed=True, r=S.r * 0.5)),
            dot(3, 20.5, 1.5), dot(21, 20.5, 1.5)]


def _ring_filled():
    from geometry import P as _P
    body = D(_P(circle(12, 12, 10)), _P(circle(12, 12, 3.5)))
    for a in (45, 135, 225, 315):
        x1, y1 = polar(12, 12, 3, a)
        x2, y2 = polar(12, 12, 10.5, a)
        body = D(body, ST(seg(x1, y1, x2, y2), 2.0, "butt", "miter", 4.0))
    return body


@icon("life-ring", CAT, "Round buoy ring with four stripes",
      tags=["lifebuoy", "life preserver", "buoy", "rescue", "water safety", "swimming", "lifesaver"],
      aliases=["lifebuoy"], filled=_ring_filled)
def _(S):
    ri = L(S, 3.5, 4.5)
    st = [detail(seg(*polar(12, 12, ri, a), *polar(12, 12, 9, a))) for a in (45, 135, 225, 315)]
    return [shell(circle(12, 12, 9)), shell(circle(12, 12, ri)), *st]


# ============================================================================ signs (round, triangle, diamond, square)

def round_sign(S):
    return shell(circle(12, 12, 9))


def tri_sign(S):
    return shell(poly([(12, 2.75), (21.75, 20.5), (2.25, 20.5)], closed=True, r=S.r), stroke_miterlimit="2")


def diamond_sign(S):
    return shell(poly([(12, 2), (22, 12), (12, 22), (2, 12)], closed=True, r=S.r), stroke_miterlimit="2")


def square_sign(S):
    return shell(rect(3, 3, 18, 18, S.R * 0.6))


def wave(x0, x1, y, amp=1.2, n=2):
    """Smooth wave of n periods from x0 to x1 at height y (starts going up)."""
    h = (x1 - x0) / (2 * n)
    d = f"M{fmt(x0)} {fmt(y)}Q{fmt(x0 + h / 2)} {fmt(y - 2 * amp)} {fmt(x0 + h)} {fmt(y)}"
    for k in range(1, 2 * n):
        d += f"T{fmt(x0 + h * (k + 1))} {fmt(y)}"
    return d


@icon("end-of-restrictions-sign", CAT, "Round sign crossed by thin diagonal stripes",
      tags=["end of limit", "restriction ends", "cancel", "derestriction", "speed limit ends", "road sign", "all clear"])
def _(S):
    out = [round_sign(S)]
    for d in (-4, 0, 4):
        t = math.sqrt(L(S, 8.6, 7.3) ** 2 - d ** 2)
        cx, cy = 12 + d * 0.7071, 12 + d * 0.7071
        out.append(detail(seg(cx - t * 0.7071, cy + t * 0.7071, cx + t * 0.7071, cy - t * 0.7071)))
    return out


@icon("headlights-on-sign", CAT, "Round sign with a headlamp and three straight light beams",
      tags=["lights on", "dipped beam", "low beam", "tunnel lights", "drive with lights", "car light", "road sign"],
      aliases=["lights-on-sign"])
def _(S):
    lamp = "M12.5 7V17C15.8 17 18 14.8 18 12C18 9.2 15.8 7 12.5 7Z"
    return [round_sign(S), mark(lamp), detail(seg(5.5, 9.25, 9.5, 9.25)), detail(seg(5.5, 12, 9.5, 12)),
            detail(seg(5.5, 14.75, 9.5, 14.75))]


@icon("no-motorcycles-sign", CAT, "Round sign with a motorcycle in side view inside a ring",
      tags=["motorbike", "motorcycle ban", "no bikes", "prohibited", "road sign", "restriction", "moped"])
def _(S):
    return [round_sign(S), mark(circle(7.5, 14.5, 2.2)), mark(circle(16.5, 14.5, 2.2)),
            mark(poly([(9.5, 14.5), (10, 11), (14, 11), (14.5, 14.5)], closed=True)),
            detail(poly([(14, 11), (15.5, 8), (17, 8)])), detail(seg(7.5, 11, 10, 11))]


@icon("flooded-road-sign", CAT, "Triangle warning sign with a car half under wavy water",
      tags=["flood", "flooded road", "water on road", "ford", "deep water", "warning", "road sign"])
def _(S):
    return [tri_sign(S), mark(poly([(8, 14.5), (8, 12), (10, 12), (11, 9.75), (13.5, 9.75), (14.5, 12), (16, 12), (16, 14.5)],
                                   closed=True)),
            detail(wave(6.5, 17.5, 14.75, 1.1, 3)), detail(wave(6, 18, 18.25, 1.1, 3))]


@icon("fog-warning-sign", CAT, "Triangle warning sign with three wavy horizontal lines",
      tags=["fog", "mist", "low visibility", "haze", "warning", "road sign", "drive slowly"])
def _(S):
    return [tri_sign(S), detail(wave(9, 15, 11.25, 1, 2)), detail(wave(7.5, 16.5, 14.75, 1, 3)),
            detail(wave(6.5, 17.5, 18.25, 1, 3))]


@icon("humpback-bridge-sign", CAT, "Triangle warning sign with a sharply arched hump shaped road",
      tags=["hump bridge", "hump back", "steep bridge", "blind crest", "warning", "road sign", "canal bridge"])
def _(S):
    return [tri_sign(S), detail("M5.5 18.25H8.5C10 18.25 10 12 12 12S14 18.25 15.5 18.25H18.5")]


@icon("priority-over-oncoming-sign", CAT, "Square sign with a large up arrow and a small down arrow",
      tags=["priority", "right of way", "give way", "narrow road", "oncoming traffic", "road sign", "yield"])
def _(S):
    return [square_sign(S), detail(seg(9, 18.5, 9, 7.5)), detail(poly([(5.5, 11), (9, 7), (12.5, 11)])),
            detail(seg(16.5, 7, 16.5, 12.5)), detail(poly([(14.5, 11), (16.5, 14.5), (18.5, 11)]))]


@icon("ferry-crossing-sign", CAT, "Square sign with a ferry boat above waves",
      tags=["ferry", "boat crossing", "ferry terminal", "water crossing", "road sign", "ship", "sailing"])
def _(S):
    return [square_sign(S), mark(poly([(6, 12.5), (18, 12.5), (15.5, 15.5), (8.5, 15.5)], closed=True)),
            mark(rect(9, 8.5, 6, 3, 0.4)), detail(wave(6, 18, 18.25, 1, 3))]


@icon("hazmat-placard", CAT, "Diamond placard with a flame symbol above a hazard class number",
      tags=["dangerous goods", "hazard class", "flammable", "hazmat", "placard", "transport sign", "fire risk"])
def _(S):
    flame = ("M12 4.6C12 6.6 14.4 7.4 14.4 9.6C14.4 11 13.4 11.9 12 11.9C10.6 11.9 9.6 11 9.6 9.6"
             "C9.6 8.6 10.2 8 10.7 7.4C10.9 8.3 11.2 8.6 11.6 8.6C11.4 7 11.8 5.6 12 4.6Z")
    return [diamond_sign(S), mark(flame), detail(poly([(13, 14), (13, 18)])),
            detail(poly([(10, 14), (10, 16.25), (14.5, 16.25)]))]


@icon("radar-speed-sign", CAT, "Roadside display box showing speed digits on a pole",
      tags=["speed display", "your speed", "vehicle activated sign", "speed check", "traffic calming", "radar", "speed camera"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 12, S.R * 0.5)),
            detail(poly([(6.5, 6), (10, 6), (10, 11), (6.5, 11)])), detail(seg(8, 8.5, 10, 8.5)),
            detail(rect(13.5, 6, 3.5, 5)),
            line(seg(12, 14.5, 12, 21.5)), line(seg(9, 21.5, 15, 21.5))]


@icon("crossing-guard-sign", CAT, "Round hand held sign on a long pole showing two walking children",
      tags=["school crossing", "lollipop sign", "crossing patrol", "stop sign", "children", "school safety", "pedestrian"])
def _(S):
    return [shell(circle(12, 9.5, 7.5)), line(seg(12, 17, 12, 21.5)),
            mark(circle(9.25, 6.25, 1.25)), mark(circle(14.75, 6.25, 1.25)),
            detail(seg(9.25, 8.25, 9.25, 11)), detail(seg(14.75, 8.25, 14.75, 11)),
            detail(poly([(8, 13), (9.25, 11), (10.5, 13)])), detail(poly([(13.5, 13), (14.75, 11), (16, 13)]))]


# ============================================================================ street furniture and structures

@icon("traffic-signal-cabinet", CAT, "Metal cabinet with double doors beside a signal pole",
      tags=["signal controller", "traffic light box", "junction box", "roadside cabinet", "utility box", "traffic signals"])
def _(S):
    return [shell(rect(2.5, 9, 12, 12, S.R * 0.4)), detail(seg(8.5, 9, 8.5, 21)),
            mark(circle(11.5, 15, 1)), detail(seg(4.5, 12.5, 6.5, 12.5)), detail(seg(4.5, 15.5, 6.5, 15.5)),
            shell(rect(16.5, 2.5, 5, 8, S.R * 0.4)), mark(circle(19, 5.25, 1)), mark(circle(19, 8, 1)),
            line(seg(19, 10.5, 19, 21))]


@icon("traffic-mirror", CAT, "Round convex mirror on a tall pole",
      tags=["convex mirror", "blind corner", "safety mirror", "driveway mirror", "road mirror", "parabolic mirror"])
def _(S):
    return [shell(circle(12, 8.5, 6.5)), detail(arc(12, 8.5, 3, 185, 265)),
            line(seg(12, 15, 12, 21.5)), line(seg(8.5, 21.5, 15.5, 21.5))]


@icon("high-mast-light", CAT, "Very tall thin pole topped by a ring of lamps",
      tags=["stadium light", "floodlight", "street lighting", "mast", "highway lighting", "lamp post", "tall light"])
def _(S):
    return [line(ellipse(12, 4.5, 8, 2.5)), mark(rect(4.5, 8, 3, 2, 0.4)), mark(rect(10.5, 8, 3, 2, 0.4)),
            mark(rect(16.5, 8, 3, 2, 0.4)), line(seg(12, 10.5, 12, 21.5)), line(seg(9, 21.5, 15, 21.5))]


@icon("sidewalk", CAT, "Raised pavement strip with paving joints and a kerb edge beside the road",
      tags=["pavement", "footpath", "kerb", "curb", "walkway", "paving slabs", "pedestrian path"],
      aliases=["pavement"])
def _(S):
    return [shell(rect(10, 3, 11, 18, S.R * 0.3)), detail(seg(10, 9, 21, 9)), detail(seg(10, 15, 21, 15)),
            line(seg(5, 3.5, 5, 8)), line(seg(5, 16, 5, 20.5))]


@icon("alleyway", CAT, "Narrow gap between two tall buildings with a bin and a lamp at the far end",
      tags=["alley", "lane", "back street", "passage", "narrow street", "backstreet", "ginnel"],
      aliases=["alley"])
def _(S):
    return [shell(rect(2.5, 2.5, 6, 19, S.R * 0.3)), shell(rect(15.5, 2.5, 6, 19, S.R * 0.3)),
            mark(rect(4.25, 6, 2.5, 2.5)), mark(rect(4.25, 12, 2.5, 2.5)),
            mark(rect(17.25, 6, 2.5, 2.5)), mark(rect(17.25, 12, 2.5, 2.5)),
            mark(circle(12, 7, 1.4)), shell(rect(10.25, 16.5, 3.5, 5, 0.5))]


@icon("street-grid", CAT, "Top view of city blocks with buildings, separated by streets",
      tags=["city blocks", "urban plan", "street map", "town plan", "neighbourhood", "city layout", "roads"])
def _(S):
    rr = S.R * 0.4
    return [shell(rect(3, 3, 7, 8, rr)), shell(rect(14, 3, 7, 6, rr)),
            shell(rect(3, 15, 7, 6, rr)), shell(rect(14, 13, 7, 8, rr)),
            mark(rect(5.5, 5.5, 2, 3)), mark(rect(16.5, 16, 2, 3))]


@icon("ticket-office", CAT, "Booth with an awning, a service window and a ticket slot",
      tags=["ticket booth", "box office", "ticket counter", "kiosk", "tickets", "station", "theatre"],
      aliases=["ticket-booth"])
def _(S):
    return [shell(poly([(2, 8.5), (4.5, 3), (19.5, 3), (22, 8.5)], closed=True, r=S.r * 0.5)),
            shell(rect(4, 8.5, 16, 12.5, S.R * 0.3)), mark(rect(7, 11.5, 10, 4, 0.5)), detail(seg(9.5, 18, 14.5, 18))]


@icon("aircraft-de-icing", CAT, "Aircraft wing sprayed with fluid from a boom arm",
      tags=["deicing", "de-ice", "wing spray", "winter flight", "ground crew", "anti-icing fluid", "airport"],
      aliases=["de-icing"])
def _(S):
    wing = "M2.5 17.5C2.5 15 7 14 12 14.2L18 15.5V19.5H4.5C3.3 19.5 2.5 18.8 2.5 17.5Z"
    return [shell(wing), line(poly([(21, 21.5), (21, 7), (12, 5)], r=S.r)), mark(circle(12, 5, 1.5)),
            line(seg(9.5, 8, 8, 11)), line(seg(12, 8.5, 12, 11.5)), line(seg(14.5, 8, 16, 11))]


@icon("aircraft-marshaller", CAT, "Standing ground crew figure holding two lit wands raised in a V",
      tags=["ramp agent", "wing walker", "aircraft guide", "airport ground crew", "parking signal", "taxiing", "airport"])
def _(S):
    return [shell(circle(12, 6, 2.25)), line(seg(12, 9, 12, 15)), line(poly([(12, 15), (9.5, 21.5)])),
            line(poly([(12, 15), (14.5, 21.5)])), line(poly([(12, 10.5), (7.5, 7)])), line(poly([(12, 10.5), (16.5, 7)])),
            mark(circle(6, 5, 1.6)), mark(circle(18, 5, 1.6))]


@icon("tide-gauge", CAT, "Tall measuring post with tick marks standing in wavy water",
      tags=["tide staff", "water level", "sea level", "flood gauge", "harbour", "measuring post", "river level"])
def _(S):
    return [shell(rect(9, 2.5, 6, 18.5, S.R * 0.3)), detail(seg(10, 6, 12.5, 6)), detail(seg(10, 9.5, 12.5, 9.5)),
            line(wave(2, 22, 15, 1, 4))]


@icon("ship-lift", CAT, "Water filled trough holding a boat, raised on a frame",
      tags=["boat lift", "canal lift", "vessel elevator", "waterway", "inclined plane", "lock alternative", "canal"])
def _(S):
    return [line(poly([(3, 5), (3, 14), (21, 14), (21, 5)], r=S.r)),
            mark(poly([(8, 9.5), (16, 9.5), (14.5, 12), (9.5, 12)], closed=True)), mark(rect(10.5, 6.5, 3.5, 2.5)),
            line(seg(7, 14, 7, 21.5)), line(seg(17, 14, 17, 21.5)), line(seg(2, 21.5, 22, 21.5))]


@icon("dock-fender", CAT, "Tyre hung by chain against a quay wall",
      tags=["quay", "tire fender", "boat bumper", "harbour wall", "pier", "mooring", "port"])
def _(S):
    return [shell(rect(17.5, 2.5, 4, 19, S.R * 0.3)), shell(circle(9, 14.5, 5.5)), mark(circle(9, 14.5, 1.75)),
            line(poly([(17, 5), (13, 5), (9, 9)]))]


@icon("height-barrier", CAT, "Bar hanging between two posts over a road with a height limit arrow below",
      tags=["height limit", "headroom", "gate", "car park barrier", "low clearance", "maximum height", "bar"])
def _(S):
    return [line(seg(2.5, 3, 2.5, 21.5)), line(seg(21.5, 3, 21.5, 21.5)),
            shell(rect(4.5, 7.5, 15, 4.5, S.R * 0.3)),
            line(seg(12, 15.5, 12, 20.5)), detail(poly([(10, 17.5), (12, 15), (14, 17.5)])),
            line(poly([(10, 18.5), (12, 21), (14, 18.5)]))]


@icon("car-parking-lift", CAT, "Two level steel frame with one car raised above another",
      tags=["stack parking", "car stacker", "parking platform", "garage lift", "double parking", "car park", "hoist"])
def _(S):
    car = lambda y: mark(poly([(5.5, y + 5), (5.5, y + 2.5), (8, y + 2.5), (9.5, y), (14, y), (15.5, y + 2.5),
                               (18.5, y + 2.5), (18.5, y + 5)], closed=True))
    return [line(seg(3, 2, 3, 21.5)), line(seg(21, 2, 21, 21.5)), line(seg(3, 2.5, 21, 2.5)),
            line(seg(3, 11.5, 21, 11.5)), line(seg(2, 21.5, 22, 21.5)), car(5), car(15)]


# ============================================================================ vehicles at the kerb, charging, structures

@icon("wheel-stop", CAT, "Low concrete block on the ground with a car wheel next to it",
      tags=["parking block", "curb stop", "car park", "bumper block", "parking stop", "tyre stop", "bay"])
def _(S):
    return [shell(circle(8.5, 14.5, 6)), mark(circle(8.5, 14.5, 1.75)), shell(rect(17, 16.5, 5, 4.5, S.R * 0.3)),
            line(seg(2, 21.5, 15, 21.5))]


def _panel(S):
    return shell(rect(3, 3, 18, 18, S.R))


@icon("car-charging-port", CAT, "Car side panel with the flap open showing a round socket and a lightning bolt",
      tags=["ev socket", "electric vehicle", "charge inlet", "charging flap", "ev charging", "plug in", "charge port"])
def _(S):
    bolt = [(12.75, 8.25), (9.5, 12.5), (11.75, 12.5), (11.25, 15.75), (14.5, 11.5), (12.25, 11.5)]
    return [_panel(S), detail(circle(12, 12, 5.5)), mark(poly(bolt, closed=True))]


@icon("type-2-connector", CAT, "Front view of a round plug face with a flat top edge and seven pin holes",
      tags=["ev plug", "mennekes", "charging connector", "ac charging", "electric car plug", "socket", "iec 62196"])
def _(S):
    face = L(S, "M6 6.5H18A8.5 8.5 0 1 1 6 6.5Z", "M6.5 7H17.5A8.25 8.25 0 1 1 6.5 7Z")
    pins = [(9, 10), (15, 10), (8, 13.5), (12, 13.5), (16, 13.5), (10, 17), (14, 17)]
    return [shell(face), *[mark(circle(x, y, 1.15)) for x, y in pins]]


@icon("ccs-connector", CAT, "Front view of a fast charge plug with small pins above two large round pins",
      tags=["combo plug", "dc fast charging", "ev connector", "combined charging system", "rapid charger", "charging plug"])
def _(S):
    from dsl import path_to_d
    outline = path_to_d(U(P(circle(12, 9, 7)), P(rect(4.5, 14, 15, 7.5, L(S, 1.5, 3.75)))))
    return [shell(outline), mark(circle(9, 7.5, 1.1)), mark(circle(15, 7.5, 1.1)), mark(circle(12, 11, 1.1)),
            mark(circle(8.75, 17.75, 1.9)), mark(circle(15.25, 17.75, 1.9))]


@icon("solar-carport", CAT, "Car parked under a slanted canopy covered with solar panels",
      tags=["solar canopy", "pv shelter", "car park solar", "parking shade", "charging shelter", "renewable", "panel roof"])
def _(S):
    car = [(7, 20.5), (7, 18), (9, 18), (10.5, 16), (14, 16), (15.5, 18), (17.5, 18), (17.5, 20.5)]
    return [shell(poly([(2, 7.5), (22, 3.5), (22, 9), (2, 13)], closed=True, r=S.r * 0.5)),
            detail(seg(8, 6.3, 8, 11.7)), detail(seg(15, 4.9, 15, 10.3)),
            line(seg(3.5, 13.5, 3.5, 21.5)), line(seg(20.5, 9.5, 20.5, 21.5)),
            mark(poly(car, closed=True))]


@icon("car-vacuum-station", CAT, "Post with a hose hanging from it ending in a wide nozzle",
      tags=["car wash", "vacuum cleaner", "self service", "interior cleaning", "hose", "forecourt", "valet"])
def _(S):
    return [shell(rect(3, 2.5, 7, 19, S.R * 0.4)), detail(seg(5, 6, 8, 6)), detail(seg(5, 9, 8, 9)),
            line("M10 13C15 13 13.5 18 16 18"), mark(poly([(16, 16), (21.5, 14.5), (21.5, 21.5), (16, 20)], closed=True))]


@icon("rideshare-pickup", CAT, "Map pin with the front of a car inside it",
      tags=["ride hailing", "taxi pickup", "pick up point", "cab stand", "car share", "ride share", "meeting point"])
def _(S):
    pin = L(S, "M12 21.5C9 18 4.5 13.5 4.5 9.5A7.5 7.5 0 0 1 19.5 9.5C19.5 13.5 15 18 12 21.5Z",
            "M10.8 20C8.5 17.5 4.5 13.3 4.5 9.5A7.5 7.5 0 0 1 19.5 9.5C19.5 13.3 15.5 17.5 13.2 20Q12 21.5 10.8 20Z")
    return [shell(pin), mark(poly([(9.5, 9.5), (10.5, 6.5), (13.5, 6.5), (14.5, 9.5)], closed=True)),
            mark(rect(8, 9.5, 8, 3.5, 0.5))]


@icon("ferry-route", CAT, "Two piers either side of water joined by a dotted curved line with a boat",
      tags=["ferry crossing", "sea route", "boat route", "passage", "water transport", "timetable", "crossing"])
def _(S):
    dots = []
    for a in (215, 235, 255, 285, 305, 325):
        x, y = polar(12, 18, 9.5, a)
        dots.append(dot(x, y, 1))
    return [shell(rect(2, 13, 4, 6, S.R * 0.3)), shell(rect(18, 13, 4, 6, S.R * 0.3)), *dots,
            mark(poly([(8.5, 14), (15.5, 14), (14, 16.5), (10, 16.5)], closed=True)), mark(rect(10.5, 11.5, 3, 2)),
            ]


@icon("help-point", CAT, "Tall pillar with a question mark and a speaker grille",
      tags=["emergency point", "information pillar", "assistance", "intercom", "call point", "support post", "kiosk"])
def _(S):
    return [shell(rect(6, 2.5, 12, 19, S.R * 0.5)), detail("M9.75 7A2.25 2.25 0 1 1 12 9.25V10.5"), mark(circle(12, 12.6, 0.3)),
            detail(seg(9, 16, 15, 16)), detail(seg(9, 19, 15, 19))]


@icon("road-salt-dome", CAT, "Dome shaped storage shed with an arched door and a pile of salt beside it",
      tags=["salt barn", "winter maintenance", "grit store", "gritting", "de-icing salt", "depot", "snow plough"])
def _(S):
    dome = L(S, "M2.5 21V14A7 7 0 0 1 16.5 14V21Z", "M2.5 19.5V14A7 7 0 0 1 16.5 14V19.5Q16.5 21 15 21H4Q2.5 21 2.5 19.5Z")
    return [shell(dome), detail("M6.5 21V17A3 3 0 0 1 12.5 17V21"),
            mark(poly([(18, 21.5), (20, 17.5), (22, 21.5)], closed=True))]


@icon("moon-bridge", CAT, "Tall semicircular arched footbridge with its reflection completing a circle",
      tags=["arch bridge", "garden bridge", "footbridge", "reflection", "pond", "full moon", "arched"])
def _(S):
    return [shell("M3 13.5A9 9 0 0 1 21 13.5H17.5A5.5 5.5 0 0 0 6.5 13.5Z"),
            line(arc(12, 14, 7.5, 15, 55)), line(arc(12, 14, 7.5, 80, 100)), line(arc(12, 14, 7.5, 125, 165))]


@icon("log-bridge", CAT, "Single fallen log lying across a stream from bank to bank",
      tags=["fallen tree", "trail crossing", "footbridge", "stream crossing", "hiking", "rustic bridge", "woods"])
def _(S):
    return [shell(rect(2, 8.5, 20, 4.5, 2.25)), detail(seg(8, 10.75, 11, 10.75)), detail(seg(14, 10.75, 17, 10.75)),
            line(poly([(2, 16.5), (6, 16.5), (8, 21.5)], r=S.r)), line(poly([(22, 16.5), (18, 16.5), (16, 21.5)], r=S.r)),
            line(wave(9.5, 14.5, 19.5, 0.9, 1))]


@icon("transporter-bridge", CAT, "High girder between two tall towers with a gondola hanging on cables near the water",
      tags=["aerial ferry", "suspended ferry", "gondola bridge", "girder", "river crossing", "towers", "industrial bridge"])
def _(S):
    return [shell(rect(3, 2.5, 18, 3, S.R * 0.3)),
            line(seg(2.5, 21.5, 5, 6)), line(seg(7.5, 21.5, 5, 6)),
            line(seg(16.5, 21.5, 19, 6)), line(seg(21.5, 21.5, 19, 6)),
            line(seg(10.5, 5.5, 10.5, 14)), line(seg(13.5, 5.5, 13.5, 14)),
            shell(rect(8.5, 14, 7, 4, S.R * 0.3)), line(wave(8, 16, 21, 0.7, 2))]


@icon("trestle-bridge", CAT, "Railway track carried on a tall frame of crisscrossed timbers",
      tags=["railway trestle", "viaduct", "timber bridge", "rail bridge", "braced frame", "valley crossing", "train bridge"])
def _(S):
    return [shell(rect(2, 3, 20, 3, S.R * 0.3)),
            line(seg(4.5, 6, 4.5, 21.5)), line(seg(12, 6, 12, 21.5)), line(seg(19.5, 6, 19.5, 21.5)),
            line(seg(4.5, 8, 12, 19.5)), line(seg(12, 8, 4.5, 19.5)),
            line(seg(12, 8, 19.5, 19.5)), line(seg(19.5, 8, 12, 19.5))]


@icon("canal", CAT, "Straight waterway with parallel stone edges and a towpath on one side",
      tags=["waterway", "narrowboat", "towpath", "navigation", "inland waterway", "channel", "barge"])
def _(S):
    return [line(seg(8, 2.5, 8, 21.5)), line(seg(20, 2.5, 20, 21.5)),
            line(seg(3, 3.5, 3, 8)), line(seg(3, 10.5, 3, 15)), line(seg(3, 17.5, 3, 21)),
            line(wave(10.5, 17.5, 7, 0.8, 1)), line(wave(10.5, 17.5, 12, 0.8, 1)), line(wave(10.5, 17.5, 17, 0.8, 1))]


@icon("skybridge", CAT, "Enclosed glass walkway linking two tall buildings high above the ground",
      tags=["sky bridge", "skywalk", "pedestrian bridge", "building link", "overhead walkway", "corridor", "connector"])
def _(S):
    return [shell(rect(2.5, 2.5, 5.5, 19, S.R * 0.3)), shell(rect(16, 2.5, 5.5, 19, S.R * 0.3)),
            shell(rect(8, 8.5, 8, 5, S.R * 0.3)), detail(seg(12, 8.5, 12, 13.5)),
            mark(rect(4.25, 5.5, 2, 1.5)), mark(rect(17.75, 5.5, 2, 1.5)),
            mark(rect(4.25, 16.5, 2, 1.5)), mark(rect(17.75, 16.5, 2, 1.5))]


@icon("elevated-railway", CAT, "Train running on a track carried by a row of tall pillars above a street",
      tags=["el train", "viaduct", "overhead rail", "metro", "sky train", "rail viaduct", "city transit"])
def _(S):
    return [shell(rect(3, 4, 18, 8.5, S.R * 0.7)),
            mark(rect(5.5, 6.5, 3, 2.5, 0.4)), mark(rect(10.5, 6.5, 3, 2.5, 0.4)), mark(rect(15.5, 6.5, 3, 2.5, 0.4)),
            line(seg(2, 14.5, 22, 14.5)),
            line(seg(5, 15, 5, 21.5)), line(seg(12, 15, 12, 21.5)), line(seg(19, 15, 19, 21.5))]


@icon("scramble-crossing", CAT, "Top view of an intersection with crosswalk stripes on every side and two diagonals",
      tags=["pedestrian scramble", "diagonal crossing", "barnes dance", "all way crossing", "crosswalk", "intersection", "zebra"])
def _(S):
    st = [line(seg(x, 2.5, x, 6)) for x in (9.5, 14.5)] + [line(seg(x, 18, x, 21.5)) for x in (9.5, 14.5)]
    st += [line(seg(2.5, y, 6, y)) for y in (9.5, 14.5)] + [line(seg(18, y, 21.5, y)) for y in (9.5, 14.5)]
    return st + [line(seg(8.5, 8.5, 15.5, 15.5)), line(seg(15.5, 8.5, 8.5, 15.5))]


@icon("train-door-button", CAT, "Round push button with two arrows pointing apart, mounted on a door panel",
      tags=["door open", "open door", "push button", "carriage door", "passenger door", "tram", "rail"])
def _(S):
    return [shell(rect(3, 2.5, 18, 19, S.R * 0.6)), detail(circle(12, 12, 6)),
            mark(poly([(7.5, 12), (10.5, 9.5), (10.5, 14.5)], closed=True)),
            mark(poly([(16.5, 12), (13.5, 9.5), (13.5, 14.5)], closed=True))]
