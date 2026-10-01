"""TypeIcon Core: aviation (airports, cockpit, ground equipment), batch 001."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt

CAT = "aviation"


def L(S, a, b):
    return a if S.name == "line" else b


def rc(S, cap):
    return min(S.R, cap)


def sd(x, y, w, h):
    """Small solid rectangle (knocked out of a Filled shell)."""
    return Part("dot", rect(x, y, w, h))


# ============================================================================ chunk 1

@icon("baggage-dolly", CAT, "Low open baggage cart on small wheels with a tow bar and suitcases on its deck",
      tags=["baggage cart", "luggage trolley", "airport", "ground crew", "tug cart", "apron"])
def _(S):
    return [
        shell(rect(3, 13, 15, 2.5, rc(S, 1))),
        shell(rect(4.5, 6, 6.5, 7, rc(S, 1.5))),
        shell(rect(12, 8.5, 4.5, 4.5, rc(S, 1))),
        shell(circle(7, 19.5, 1.75)), shell(circle(14.5, 19.5, 1.75)),
        line(poly([(18, 14.25), (21.5, 14.25), (21.5, 19)], r=S.r)),
    ]


@icon("underseat-bag", CAT, "Airline seat in side view with a small soft bag stowed on the floor beneath it",
      tags=["under seat", "carry-on", "personal item", "cabin baggage", "stow", "airline seat"])
def _(S):
    return [
        shell(poly([(4, 3), (8, 3), (9.5, 10), (19.5, 10), (19.5, 14), (5.5, 14)], closed=True, r=S.r)),
        line(seg(9, 14, 9, 21)),
        shell(rect(12.5, 17, 8.5, 4, rc(S, 2))),
    ]


@icon("explosive-trace-swab", CAT, "Paddle with a round swab pad held up beside a carry-on bag with its handle",
      tags=["security", "screening", "swab", "explosives", "airport security", "trace detection"])
def _(S):
    return [
        shell(rect(2.5, 12, 10, 9, rc(S, 2.5))),
        line(poly([(5.5, 12), (5.5, 9), (9.5, 9), (9.5, 12)], r=S.r)),
        shell(circle(18, 6.5, 3.5)),
        shell(rect(16, 10, 4, 11, rc(S, 1.5))),
    ]


@icon("security-pat-down", CAT, "Standing person with arms out sideways while a smaller figure runs a hand down the side",
      tags=["pat down", "body search", "security check", "frisk", "screening", "checkpoint"])
def _(S):
    return [
        shell(circle(15.5, 4.5, 2.25)),
        line(seg(9, 9.5, 22, 9.5)),
        line(seg(15.5, 9.5, 15.5, 15)),
        line(poly([(15.5, 15), (12, 21.5)])), line(poly([(15.5, 15), (19, 21.5)])),
        shell(circle(4.5, 12, 1.75)),
        line(poly([(4.5, 14.5), (4.5, 19.5)])),
        line(poly([(4.5, 19.5), (2.5, 22)])), line(poly([(4.5, 19.5), (6.5, 22)])),
        line(poly([(4.5, 16), (10, 11.5)])),
    ]


@icon("ambulift", CAT, "Truck with its passenger cabin raised on a scissor lift up to an aircraft door",
      tags=["ambulance lift", "wheelchair lift", "reduced mobility", "accessible boarding", "high loader", "airport"])
def _(S):
    return [
        shell(rect(8.5, 2.5, 13, 5, rc(S, 1.5))),
        line(poly([(10, 8), (15, 14)])), line(poly([(15, 8), (10, 14)])),
        shell(poly([(2, 14), (15, 14), (15, 18), (2, 18)], closed=True, r=S.r * 0.5)),
        shell(poly([(15, 15), (18.5, 15), (21.5, 17.5), (21.5, 18)], closed=True, r=S.r * 0.4)),
        shell(circle(6, 19.5, 1.5)), shell(circle(17, 19.5, 1.5)),
    ]


@icon("cabin-reading-light", CAT, "Ceiling panel lamp casting a cone of light downward onto a passenger seat",
      tags=["reading lamp", "overhead light", "passenger service unit", "cabin", "airplane light", "seat light"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 3.5, rc(S, 1.5))),
        shell(circle(12, 10, 2.5)),
        line(seg(8, 12.5, 4.5, 19.5)), line(seg(16, 12.5, 19.5, 19.5)),
        line(seg(12, 15, 12, 20)),
    ]


@icon("overhead-air-vent", CAT, "Round swivel air nozzle in a ceiling panel with three curved air lines flowing out",
      tags=["gasper", "air vent", "cabin air", "ventilation", "airflow", "overhead nozzle"])
def _(S):
    def wave(x):
        return f"M{x} 13Q{x + 1.5} 15 {x} 17Q{x - 1.5} 19 {x} 21"
    return [
        shell(rect(3, 2.5, 18, 3, rc(S, 1))),
        shell(f"M7.5 5.5A4.5 4.5 0 0 0 16.5 5.5Z"),
        line(wave(8)), line(wave(12)), line(wave(16)),
    ]


@icon("aircraft-lavatory", CAT, "Narrow aircraft toilet cubicle with a compact toilet and a tiny sink on the wall",
      tags=["toilet", "restroom", "washroom", "bathroom", "airplane toilet", "wc", "cabin"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rc(S, 2.5))),
        detail(rect(6.5, 6, 4, 5, rc(S, 1))),
        detail(poly([(6.5, 14.5), (13.5, 14.5), (12.5, 18), (7.5, 18)], closed=True, r=S.r * 0.4)),
        detail(poly([(16.5, 11), (16.5, 8), (19, 8)], r=S.r * 0.4)),
    ]


@icon("cabin-crew-jumpseat", CAT, "Fold-down cabin crew seat on a wall with a shoulder harness across its back",
      tags=["flight attendant seat", "crew seat", "folding seat", "harness", "cabin crew", "door seat"])
def _(S):
    return [
        line(seg(3, 2.5, 3, 21.5)),
        shell(rect(6, 3, 7, 10, rc(S, 2.5))),
        shell(rect(6, 15, 12, 2.5, rc(S, 1))),
        detail(seg(7.5, 4.5, 11.5, 11.5)),
        line(poly([(10, 17.5), (14, 21.5)])),
    ]


@icon("cockpit-door", CAT, "Reinforced flight deck door with a peephole and handle, and a keypad beside it",
      tags=["flight deck door", "secure door", "pilot door", "keypad", "locked", "security"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 12.5, 19, rc(S, 2))),
        dot(8.75, 7.5, 1.5),
        detail(seg(5.5, 14, 8, 14)) if False else line(seg(10, 14, 12, 14)),
        shell(rect(17, 8, 4.5, 8, rc(S, 1))),
        dot(19.25, 10.75, 0.8), dot(19.25, 13.25, 0.8),
    ]


@icon("cockpit", CAT, "Flight deck view with angled windshield panes above a glare shield and two instrument screens",
      tags=["flight deck", "pilot view", "windshield", "instrument panel", "airplane cockpit", "cabin front"])
def _(S):
    return [
        shell(poly([(3, 11), (6, 3), (18, 3), (21, 11)], closed=True, r=S.r)),
        detail(seg(12, 3, 12, 11)),
        shell(rect(4, 14.5, 6.5, 7, rc(S, 3))),
        shell(rect(13.5, 14.5, 6.5, 7, rc(S, 3))),
    ]


@icon("pilot-wings", CAT, "Pilot badge with a small central shield and a swept feathered wing on each side",
      tags=["wings badge", "pilot badge", "aviator", "captain", "flight crew", "insignia"])
def _(S):
    ls = [((7.5, 8.5), (2.5, 5)), ((7.5, 12), (3, 9.5)), ((7.5, 15.5), (5, 14))]
    out = [shell("M9.5 6.5H14.5V12Q14.5 15 12 17Q9.5 15 9.5 12Z")]
    for a, b in ls:
        out.append(line(seg(a[0], a[1], b[0], b[1])))
        out.append(line(seg(24 - a[0], a[1], 24 - b[0], b[1])))
    return out


@icon("pilot-flight-bag", CAT, "Boxy hard-sided pilot case with a top carry handle and a front flap held by two latches",
      tags=["flight case", "pilot case", "headset bag", "briefcase", "aviator bag", "crew luggage"])
def _(S):
    return [
        shell(rect(3, 8.5, 18, 12, rc(S, 2.5))),
        line(poly([(9, 8.5), (9, 5), (15, 5), (15, 8.5)], r=S.r)),
        detail(seg(3, 13.5, 21, 13.5)),
        dot(8, 13.5, 1.1), dot(16, 13.5, 1.1),
    ]


@icon("kneeboard", CAT, "Small clipboard strapped to a thigh by an elastic band, holding a notepad and pencil",
      tags=["knee board", "pilot notes", "clipboard", "flight notes", "thigh strap", "writing"])
def _(S):
    return [
        shell(rect(6, 3, 12, 18, rc(S, 2.5))),
        line(seg(2, 8, 6, 8)), line(seg(18, 8, 22, 8)),
        line(seg(2, 17, 6, 17)), line(seg(18, 17, 22, 17)),
        detail(seg(9, 11, 15, 11)),
        detail(seg(9, 14, 13, 14)),
    ]


@icon("electronic-flight-bag", CAT, "Tablet showing a small airplane symbol, held in a clamp mount below it",
      tags=["efb", "tablet", "flight tablet", "digital charts", "pilot tablet", "yoke mount"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 13, rc(S, 2.5))),
        detail(seg(12, 6.5, 12, 12.5)),
        detail(seg(9, 9, 15, 9)),
        detail(seg(10.5, 12.5, 13.5, 12.5)),
        line(seg(12, 16, 12, 19.5)),
        line(seg(8, 20.5, 16, 20.5)),
    ]

def plane_pts(cx, cy, size, deg=0.0):
    """Small original top-view aircraft, nose up at deg=0, fitted to roughly size x size."""
    base = [(12, 2), (13.2, 6), (21, 12), (21, 14), (13.2, 12.5), (12.8, 18), (15.5, 20), (15.5, 21.5),
            (12, 20.7), (8.5, 21.5), (8.5, 20), (11.2, 18), (10.8, 12.5), (3, 14), (3, 12), (10.8, 6)]
    a = math.radians(deg)
    out = []
    for x, y in base:
        x, y = (x - 12) / 20 * size, (y - 11.75) / 20 * size
        out.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    return out


# ============================================================================ chunk 2

@icon("aeronautical-chart", CAT, "Folded map sheet with an airport mark on its middle panel",
      tags=["sectional chart", "flight map", "navigation chart", "airspace", "pilot map", "charts"])
def _(S):
    return [
        shell(poly([(3, 5), (9, 3), (15, 5), (21, 3), (21, 19), (15, 21), (9, 19), (3, 21)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        detail(seg(9, 3, 9, 19)), detail(seg(15, 5, 15, 21)),
        dot(12, 12, 1.4),
    ]


@icon("e6b-flight-computer", CAT, "Round circular slide rule with a rotating inner disc and a window in the middle",
      tags=["flight computer", "slide rule", "wind calculator", "pilot calculator", "dead reckoning", "manual computer"])
def _(S):
    return [
        shell(circle(12, 12, 9.5)),
        detail(circle(12, 12, 5.6)),
        detail(rect(9.5, 10, 5, 4, L(S, 0, 1))),
    ]


@icon("preflight-checklist", CAT, "Card with a small airplane mark at the top and a column of ticked boxes",
      tags=["checklist", "pre-flight", "checks", "pilot card", "inspection", "tick list"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, rc(S, 2.5))),
        detail(seg(12, 5, 12, 8)), detail(seg(10, 6.5, 14, 6.5)),
        detail(poly([(7.5, 11.5), (8.7, 12.8), (10.8, 10.5)], r=S.r * 0.3)), detail(seg(13, 11.5, 16.5, 11.5)),
        detail(poly([(7.5, 16), (8.7, 17.3), (10.8, 15)], r=S.r * 0.3)), detail(seg(13, 16, 16.5, 16)),
    ]


@icon("sidestick", CAT, "Short control stick with a rounded grip rising from a side console, with an armrest behind it",
      tags=["joystick", "flight control", "control stick", "cockpit", "fly by wire", "pilot input"])
def _(S):
    return [
        shell(rect(2.5, 15.5, 19, 6, rc(S, 2))),
        shell(rect(5.5, 2.5, 5, 8, L(S, 1.5, 2.5))),
        line(seg(8, 10.5, 8, 15.5)),
        shell(rect(14.5, 10.5, 7, 5, rc(S, 2))),
        dot(8, 5.5, 0.8),
    ]


@icon("flap-lever", CAT, "Cockpit lever with a flat handle sliding in a slotted gate with notches beside it",
      tags=["flaps", "flap selector", "throttle quadrant", "detent", "cockpit control", "slot"])
def _(S):
    return [
        shell(rect(9, 2.5, 6, 19, L(S, 2, 3))),
        line(seg(4.5, 11, 19.5, 11)),
        line(seg(2, 5.5, 5, 5.5)), line(seg(2, 16.5, 5, 16.5)),
    ]


@icon("landing-gear-lever", CAT, "Cockpit panel with a round wheel-shaped knob above a vertical slot",
      tags=["gear lever", "undercarriage", "wheel knob", "cockpit control", "gear selector", "retract"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rc(S, 2.5))),
        detail(circle(12, 8.5, 3)),
        detail(seg(12, 13, 12, 18.5)),
    ]


@icon("trim-wheel", CAT, "Tall ridged wheel set into a console beside a pointer scale",
      tags=["pitch trim", "trim", "cockpit wheel", "center console", "stabilizer trim", "elevator trim"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rc(S, 2.5))),
        detail(ellipse(9, 12, 3, 6.5)),
        dot(9, 12, 1.0),
        line(seg(15, 7, 18.5, 7)), line(seg(15, 12, 18.5, 12)), line(seg(15, 17, 18.5, 17)),
    ]


@icon("airspeed-indicator", CAT, "Round gauge with a needle and a curved colored arc band around the edge",
      tags=["asi", "speed gauge", "knots", "instrument", "cockpit dial", "flight instrument"])
def _(S):
    return [
        shell(circle(12, 12, 9.5)),
        detail(arc(12, 12, 6, 135, 405)),
        detail(seg(12, 12, 15.5, 8.5)),
        dot(12, 12, 1.4),
    ]


@icon("vertical-speed-indicator", CAT, "Round gauge with a needle resting at the nine o'clock zero and tick marks above and below",
      tags=["vsi", "climb rate", "rate of climb", "variometer", "instrument", "gauge"])
def _(S):
    def tick(deg):
        a = math.radians(deg)
        return seg(12 + 5.2 * math.cos(a), 12 + 5.2 * math.sin(a), 12 + 7.2 * math.cos(a), 12 + 7.2 * math.sin(a))
    return [
        shell(circle(12, 12, 9.5)),
        detail(seg(12, 12, 6.5, 12)),
        dot(12, 12, 1.4),
        detail(tick(235)), detail(tick(305)), detail(tick(125)), detail(tick(55)),
    ]


@icon("horizontal-situation-indicator", CAT, "Round compass gauge with a small airplane in the center and a course arrow with a deviation bar",
      tags=["hsi", "compass card", "course", "heading", "instrument", "navigation gauge"])
def _(S):
    return [
        shell(circle(12, 12, 9.5)),
        detail(seg(12, 5.5, 12, 18.5)),
        detail(poly([(9.5, 8), (12, 5.5), (14.5, 8)], r=S.r * 0.4)),
        detail(seg(9.5, 12.5, 14.5, 12.5)),
        detail(seg(16.8, 9, 16.8, 15)),
    ]


@icon("turn-coordinator", CAT, "Round gauge with a small banked airplane seen from behind and a ball in a curved tube below",
      tags=["turn and slip", "slip ball", "bank", "gyro instrument", "inclinometer", "cockpit gauge"])
def _(S):
    return [
        shell(circle(12, 12, 9.5)),
        detail(seg(5.5, 8.5, 18.5, 12.5)),
        dot(11.5, 10.7, 1.4),
        detail("M6.5 16.5Q12 19 17.5 16.5"),
        dot(12, 17.2, 1.2),
    ]


@icon("whiskey-compass", CAT, "Small liquid compass housing on a stem, its window showing a card with the letter N",
      tags=["magnetic compass", "wet compass", "heading", "standby compass", "cockpit compass", "direction"])
def _(S):
    return [
        shell(rect(3, 3.5, 18, 13, rc(S, 3))),
        detail(poly([(9.2, 13), (9.2, 7.5), (14.8, 13), (14.8, 7.5)], r=S.r * 0.3)),
        line(seg(12, 16.5, 12, 20.5)),
        line(seg(7.5, 20.5, 16.5, 20.5)),
    ]


@icon("primary-flight-display", CAT, "Screen with a horizon line in the middle and a speed tape and an altitude tape on each side",
      tags=["pfd", "glass cockpit", "artificial horizon", "attitude display", "avionics screen", "flight screen"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, rc(S, 2.5))),
        detail(seg(7.5, 7.5, 7.5, 16.5)), detail(seg(16.5, 7.5, 16.5, 16.5)),
        detail(seg(10.5, 12, 13.5, 12)),
    ]


@icon("navigation-display", CAT, "Screen with a curved compass arc, a route line and a small airplane triangle at the bottom",
      tags=["nd", "moving map", "route display", "waypoints", "avionics screen", "glass cockpit"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, rc(S, 2.5))),
        detail(arc(12, 15.5, 7, 205, 335)),
        detail(seg(12, 12.5, 14.5, 9.5)),
        Part("dot", poly([(12, 14.5), (10, 18.5), (14, 18.5)], closed=True)),
    ]


@icon("autopilot", CAT, "Control strip with an airplane mark in the center and a round knob on each side",
      tags=["auto pilot", "flight control panel", "mode control", "fcu", "cockpit panel", "autoflight"])
def _(S):
    return [
        shell(rect(2.5, 6, 19, 12, rc(S, 2.5))),
        dot(6, 12, 1.2), dot(18, 12, 1.2),
        detail(seg(12, 8.5, 12, 15.5)), detail(seg(9.2, 11, 14.8, 11)), detail(seg(10.4, 15, 13.6, 15)),
    ]


# ============================================================================ chunk 3

@icon("ground-proximity-warning", CAT, "Mountain peak with a warning triangle beside it",
      tags=["gpws", "terrain warning", "pull up", "egpws", "terrain alert", "mountain"])
def _(S):
    return [
        shell(poly([(2, 21), (8, 10.5), (11.5, 16), (14, 13), (20, 21)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        shell(poly([(17, 2.5), (22, 11.5), (12, 11.5)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        Part("dot", rect(16.2, 6.2, 1.6, 2.4)), dot(17, 9.8, 0.8),
    ]


@icon("collision-avoidance-display", CAT, "Round screen with a small airplane at the center, a dashed range ring and a diamond traffic mark ahead",
      tags=["tcas", "traffic display", "traffic alert", "airborne collision", "intruder", "proximity"])
def _(S):
    return [
        shell(circle(12, 12, 9.5)),
        detail(arc(12, 14, 5, 215, 255)), detail(arc(12, 14, 5, 285, 325)),
        detail(arc(12, 14, 5, 35, 75)), detail(arc(12, 14, 5, 105, 145)),
        dot(12, 14, 1.2),
        Part("dot", poly([(12, 4.2), (14, 6.2), (12, 8.2), (10, 6.2)], closed=True)),
    ]


@icon("stall-warning", CAT, "Steeply tilted wing cross section with airflow curling into a swirl above it and an exclamation mark",
      tags=["stall", "angle of attack", "aerodynamic stall", "lift loss", "airflow separation", "stick shaker"])
def _(S):
    a = math.radians(-28)
    n = 10
    top = [((i / n) - 0.5, -0.17 * math.sin(math.pi * (i / n)) ** 0.6) for i in range(n + 1)]
    bot = [((i / n) - 0.5, 0.04 * math.sin(math.pi * (i / n))) for i in range(n - 1, 0, -1)]
    pts = []
    for x, y in top + bot:
        x, y = x * 16, y * 16
        pts.append((11.5 + x * math.cos(a) - y * math.sin(a), 16.5 + x * math.sin(a) + y * math.cos(a)))
    return [
        shell(poly(pts, closed=True, r=S.r * 0.3)),
        line("M3 9Q3 4.5 7 4.5Q11 4.5 10.5 8"),
        line(seg(19, 2.5, 19, 8)), dot(19, 11.5, 1.1),
    ]


@icon("master-caution", CAT, "Square cockpit push button with glow lines around it and a bold bar across its face",
      tags=["caution light", "warning light", "annunciator", "alert button", "master warning", "indicator"])
def _(S):
    return [
        shell(rect(7, 7, 10, 10, rc(S, 2))),
        sd(9.5, 11, 5, 2),
        line(seg(12, 2.5, 12, 4.5)), line(seg(12, 19.5, 12, 21.5)),
        line(seg(2.5, 12, 4.5, 12)), line(seg(19.5, 12, 21.5, 12)),
        line(seg(4.3, 4.3, 5.6, 5.6)), line(seg(19.7, 4.3, 18.4, 5.6)),
        line(seg(4.3, 19.7, 5.6, 18.4)), line(seg(19.7, 19.7, 18.4, 18.4)),
    ]


@icon("flight-management-computer", CAT, "Cockpit keypad unit with a small screen on top, side keys and a grid of keys below",
      tags=["fmc", "cdu", "fms", "flight plan", "keypad", "route entry"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rc(S, 2.5))),
        detail(rect(8, 5, 8, 5, rc(S, 1))),
        dot(5.6, 6.2, 0.8), dot(5.6, 9.2, 0.8), dot(18.4, 6.2, 0.8), dot(18.4, 9.2, 0.8),
        dot(7.5, 14.5, 1), dot(12, 14.5, 1), dot(16.5, 14.5, 1),
        dot(7.5, 18, 1), dot(12, 18, 1), dot(16.5, 18, 1),
    ]


@icon("pitot-tube", CAT, "Straight probe pointing forward from a curved fuselage skin with a small opening at its tip",
      tags=["pitot", "airspeed probe", "air data", "sensor", "static port", "probe"])
def _(S):
    return [
        line("M19 2.5Q23.5 12 19 21.5"),
        shell(rect(2.5, 9.5, 15, 5, rc(S, 2.5))),
        dot(5.5, 12, 1),
        line(seg(17.5, 12, 20.5, 12)),
    ]


@icon("angle-of-attack-vane", CAT, "Small wedge shaped weather vane on a round base",
      tags=["aoa", "alpha vane", "air data sensor", "weather vane", "nose sensor", "incidence"])
def _(S):
    return [
        shell(circle(16, 12, 4.5)),
        shell(poly([(2.5, 12), (12, 8.5), (12, 15.5)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        dot(16, 12, 1.3),
    ]


@icon("winglet", CAT, "Wing seen from the front with its tip turning sharply upward into a tall swept fin",
      tags=["wingtip", "sharklet", "blended winglet", "wing tip device", "fuel saving", "airliner wing"])
def _(S):
    return [
        shell(poly([(2.5, 17), (15.5, 17), (19, 3.5), (21.5, 4.5), (21, 19.5), (2.5, 19.5)], closed=True, r=S.r * 0.5), stroke_miterlimit="3"),
    ]


@icon("aileron", CAT, "Swept wing from above with the outer trailing panel shaded and a curved arrow showing it hinge",
      tags=["roll control", "control surface", "wing panel", "hinge", "flight control", "bank"])
def _(S):
    return [
        shell(poly([(2, 10), (21, 4), (21, 9), (2, 20)], closed=True, r=S.r * 0.4), stroke_miterlimit="3"),
        Part("dot", poly([(12.5, 13.9), (20.5, 9.3), (20.5, 7), (12.5, 10.5)], closed=True)),
        line("M14 20Q19.5 19 21 14.5"),
    ]


@icon("wing-flap", CAT, "Wing cross section with a curved flap panel lowered down and back from the trailing edge",
      tags=["flaps", "high lift device", "trailing edge", "slat", "approach", "airfoil"])
def _(S):
    return [
        shell(poly([(2.5, 12), (3.5, 8.5), (9, 7.5), (14.5, 9.5), (14, 13), (8, 14)], closed=True, r=S.r * 1.5), stroke_miterlimit="2"),
        shell(poly([(15, 10.5), (21, 14), (19.5, 17.5), (14.5, 13.8)], closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
    ]


@icon("thrust-reverser", CAT, "Jet engine pod with its rear cowl slid back and curved arrows blowing air forward",
      tags=["reverse thrust", "engine cowl", "nacelle", "landing deceleration", "braking", "jet engine"])
def _(S):
    return [
        shell(poly([(3, 9), (14, 9), (14, 15.5), (3, 15.5)], closed=True, r=S.r)),
        shell(poly([(18, 9.5), (22, 10.5), (22, 14), (18, 15)], closed=True, r=S.r * 0.4)),
        line("M16 7.5Q15.5 4 9.5 4.5"), line(poly([(11.5, 2.5), (9.5, 4.5), (11.5, 6.5)], r=0)),
        line("M16 17Q15.5 20.5 9.5 20"), line(poly([(11.5, 18.5), (9.5, 20), (11.5, 21.5)], r=0)),
    ]


@icon("auxiliary-power-unit", CAT, "Tapered airliner tail cone with a small exhaust at the tip and heat lines coming out",
      tags=["apu", "tail cone", "onboard generator", "ground power", "exhaust", "aircraft engine"])
def _(S):
    return [
        shell(poly([(2, 5), (15, 9), (15, 15), (2, 19)], closed=True, r=S.r)),
        detail(seg(11.5, 9.5, 11.5, 14.5)),
        line(seg(18, 12, 22, 12)), line(seg(18, 8.5, 21, 6.5)), line(seg(18, 15.5, 21, 17.5)),
    ]


@icon("cargo-door", CAT, "Side of a fuselage with a large rectangular hatch hinged open upward above the cargo compartment",
      tags=["freight door", "cargo hatch", "belly hold", "loading", "baggage compartment", "aircraft hatch"])
def _(S):
    return [
        shell(rect(2.5, 10.5, 19, 10.5, rc(S, 2))),
        detail(rect(6, 13.5, 12, 4.5, rc(S, 1))),
        shell(poly([(7, 2.5), (17, 2.5), (19, 7.5), (5, 7.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("aircraft-door", CAT, "Tall plug door with rounded top corners, a small round window and a lift handle",
      tags=["cabin door", "boarding door", "emergency exit", "plug door", "fuselage door", "airliner"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, L(S, 3, 6))),
        detail(circle(12, 8, 2.2)),
        detail(seg(9.5, 15, 14.5, 15)),
    ]


# ============================================================================ chunk 4

@icon("cargo-hold", CAT, "Round fuselage cross section with passengers on the upper deck and two cargo containers below",
      tags=["belly cargo", "freight", "unit load device", "baggage hold", "fuselage section", "ulds"])
def _(S):
    return [
        shell(circle(12, 12, 9.5)),
        detail(poly([(7.5, 4.5), (7.5, 9.5), (11, 9.5)], r=S.r * 0.3)), detail(poly([(13, 4.5), (13, 9.5), (16.5, 9.5)], r=S.r * 0.3)),
        detail(poly([(6.5, 13.5), (11, 13.5), (11, 18.5), (8.5, 18.5), (6.5, 16.5)], closed=True, r=S.r * 0.3)),
        detail(poly([(13, 13.5), (17.5, 13.5), (17.5, 16.5), (15.5, 18.5), (13, 18.5)], closed=True, r=S.r * 0.3)),
    ]


@icon("airplane-wing", CAT, "Single swept airliner wing seen from above with an engine pod under its front edge",
      tags=["wing", "airliner wing", "engine pod", "aircraft part", "swept wing", "top view"])
def _(S):
    return [
        shell(poly([(2.5, 3), (21.5, 14.5), (21.5, 19), (2.5, 12.5)], closed=True, r=S.r * 0.4), stroke_miterlimit="3"),
        shell(rect(9, 3.5, 5, 10, rc(S, 2.5))),
    ]


@icon("glide-slope", CAT, "Airplane descending along a straight dashed line down to a runway",
      tags=["approach path", "descent angle", "glidepath", "final approach", "landing path", "ils beam"])
def _(S):
    return [
        solid(poly(plane_pts(8, 8, 12, 125), closed=True)),
        line(seg(13.5, 13, 15, 14.5)), line(seg(17, 16, 18.5, 17.5)),
        line(seg(2.5, 21.5, 21.5, 21.5)),
    ]


@icon("instrument-landing-system", CAT, "Antenna masts standing at the end of a runway with radio wave arcs spreading from one",
      tags=["ils", "localizer", "glideslope antenna", "precision approach", "runway radio", "navaid"])
def _(S):
    def wave(r):
        return arc(12, 10, r, 235, 305)
    return [
        line(seg(2.5, 21.5, 21.5, 21.5)),
        line(seg(5, 21.5, 5, 13)), line(seg(12, 21.5, 12, 11.5)), line(seg(19, 21.5, 19, 13)),
        dot(12, 10, 1.2),
        line(wave(4)), line(wave(7.5)),
    ]


@icon("vor-beacon", CAT, "Cone shaped ground station topped with a short spike and ringed by small antennas",
      tags=["vor", "vhf omnidirectional range", "navaid", "radio beacon", "navigation station", "ground station"])
def _(S):
    return [
        shell(poly([(6.5, 17), (9.5, 9), (14.5, 9), (17.5, 17)], closed=True, r=S.r * 0.5)),
        line(seg(12, 9, 12, 3.5)),
        dot(3, 18.5, 1.1), dot(21, 18.5, 1.1), dot(7.5, 21.5, 1.1), dot(16.5, 21.5, 1.1),
    ]


@icon("non-directional-beacon", CAT, "Tall radio mast held by guy wires with radio waves arcing out from its top",
      tags=["ndb", "radio mast", "navaid", "adf", "antenna tower", "beacon tower"])
def _(S):
    return [
        line(seg(12, 8, 12, 21.5)),
        line(seg(12, 12, 5, 21.5)), line(seg(12, 12, 19, 21.5)),
        dot(12, 7.5, 1.4),
        line(arc(12, 7.5, 4.5, 145, 215)), line(arc(12, 7.5, 4.5, 325, 395)),
        line(arc(12, 7.5, 8.5, 145, 215)), line(arc(12, 7.5, 8.5, 325, 395)),
    ]


@icon("papi-lights", CAT, "Row of four square light units beside a runway, two solid and two outlined",
      tags=["precision approach path indicator", "approach lights", "glide path lights", "runway lights", "red white lights", "landing aid"])
def _(S):
    return [
        Part("solid", rect(2.5, 7, 4, 4)), Part("solid", rect(7.5, 7, 4, 4)),
        shell(rect(13.5, 8, 2, 2, L(S, 0, 0.5))), shell(rect(18.5, 8, 2, 2, L(S, 0, 0.5))),
        line(seg(2.5, 17, 21.5, 17)),
    ]

# ============================================================================ chunk 5

@icon("runway-edge-lights", CAT, "Runway seen in perspective with rows of raised light dots down both sides",
      tags=["edge lights", "runway lighting", "night landing", "airfield lighting", "airport lights", "approach"])
def _(S):
    return [
        dot(9.5, 4.5, 0.9), dot(8.2, 9, 1.15), dot(6.4, 14, 1.45), dot(4, 19.5, 1.8),
        dot(14.5, 4.5, 0.9), dot(15.8, 9, 1.15), dot(17.6, 14, 1.45), dot(20, 19.5, 1.8),
        line(seg(8.5, 21.5, 15.5, 21.5)),
    ]


@icon("runway-centerline-lights", CAT, "Runway in perspective with a single line of glowing lights growing larger down its center",
      tags=["centreline lights", "center lights", "runway lighting", "night landing", "airfield lighting", "taxi line"])
def _(S):
    return [
        line(seg(10, 3, 3, 21)), line(seg(14, 3, 21, 21)),
        dot(12, 5, 0.9), dot(12, 9.5, 1.1), dot(12, 15, 1.4), dot(12, 20.5, 1.7),
    ]


@icon("touchdown-zone-markings", CAT, "Top view of a runway with pairs of short parallel bars on both sides of the centerline",
      tags=["tdz", "runway markings", "touchdown bars", "landing zone", "runway paint", "airfield markings"])
def _(S):
    out = [line(seg(3, 2.5, 3, 21.5)), line(seg(21, 2.5, 21, 21.5))]
    for y in (4, 12):
        for x in (6, 9, 15, 18):
            out.append(sd(x - 0.75, y, 1.5, 6))
    return out


@icon("aiming-point-markings", CAT, "Top view of a runway with two long thick blocks either side of a dashed centerline",
      tags=["aiming point", "runway markings", "landing target", "runway paint", "airfield markings", "fixed distance"])
def _(S):
    return [
        line(seg(3, 2.5, 3, 21.5)), line(seg(21, 2.5, 21, 21.5)),
        sd(6, 4, 4.5, 11), sd(13.5, 4, 4.5, 11),
        sd(11.25, 17, 1.5, 4), sd(11.25, 4, 1.5, 3), sd(11.25, 9, 1.5, 3),
    ]


@icon("runway-holding-position-sign", CAT, "Airport ground sign on short legs with a pair of runway numbers split by a dash",
      tags=["hold short", "runway sign", "taxiway sign", "mandatory sign", "airport signage", "runway number"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 9, rc(S, 2))),
        sd(6, 7.5, 1.5, 3), sd(8.5, 7.5, 1.5, 3), sd(10.6, 8.7, 2.8, 1.6),
        sd(14, 7.5, 1.5, 3), sd(16.5, 7.5, 1.5, 3),
        line(seg(6.5, 13.5, 6.5, 20)), line(seg(17.5, 13.5, 17.5, 20)),
        line(seg(3, 20.5, 21, 20.5)),
    ]


@icon("runway-distance-remaining-sign", CAT, "Square airport sign on short legs showing one large digit",
      tags=["distance remaining", "runway sign", "thousands of feet", "airfield sign", "landing roll", "marker"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 14, rc(S, 2.5))),
        detail("M9.5 6.5H14L11.2 10Q15 10 15 12.3Q15 14 12 14H9.5"),
        line(seg(8.5, 16.5, 8.5, 21.5)), line(seg(15.5, 16.5, 15.5, 21.5)),
    ]


@icon("stop-bar-lights", CAT, "Top view of a taxiway entrance with a straight row of in-ground lights across it",
      tags=["stop bar", "red lights", "taxiway", "runway incursion", "hold line", "ground lights"])
def _(S):
    return [
        line(seg(2.5, 2.5, 2.5, 21.5)), line(seg(21.5, 2.5, 21.5, 21.5)),
        line(seg(12, 3, 12, 7)), line(seg(12, 17, 12, 21)),
        dot(5.5, 12, 1.2), dot(9, 12, 1.2), dot(12.5, 12, 1.2), dot(16, 12, 1.2), dot(19.5, 12, 1.2),
    ]


@icon("runway-guard-lights", CAT, "Pair of round lamps on a short post, with flash rays beside one lamp",
      tags=["wig wag", "hold lights", "runway entrance lights", "flashing lights", "incursion warning", "taxiway lights"])
def _(S):
    return [
        shell(circle(8.5, 9, 2.4)), shell(circle(15.5, 9, 2.4)),
        line(seg(8.5, 13.5, 15.5, 13.5)),
        line(seg(12, 13.5, 12, 21.5)),
        line(seg(4.3, 4.3, 5.6, 5.6)), line(seg(2.3, 9, 3.8, 9)),
    ]


@icon("wind-tee", CAT, "Airplane shaped wind indicator seen from above, with a hub at its pivot",
      tags=["wind indicator", "wind direction", "airfield", "landing tee", "weather indicator", "airport"])
def _(S):
    return [
        shell(poly([(10.5, 3), (13.5, 3), (13.5, 7), (21, 7), (21, 10), (13.5, 10), (13.5, 17), (16.5, 17), (16.5, 20), (7.5, 20), (7.5, 17), (10.5, 17), (10.5, 10), (3, 10), (3, 7), (10.5, 7)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
    ]


@icon("landing-tetrahedron", CAT, "Pyramid shaped wind indicator with a pointed nose on a pivot stand",
      tags=["wind direction", "tetrahedron", "airfield wind", "landing direction", "wind cone alternative", "airport"])
def _(S):
    return [
        shell(poly([(2.5, 10), (19, 5), (19, 15)], closed=True, r=S.r * 0.4), stroke_miterlimit="3"),
        detail(seg(5, 10, 19, 10)),
        line(seg(11, 13.5, 11, 21)), line(seg(7, 21.5, 15, 21.5)),
    ]


@icon("signal-square", CAT, "Square ground panel at an airfield with a painted cross in the middle",
      tags=["signal area", "airfield marker", "ground signals", "landing panel", "airstrip", "visual signal"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rc(S, 2))),
        detail(seg(6.5, 12, 17.5, 12)), detail(seg(6.5, 8.5, 6.5, 15.5)), detail(seg(17.5, 8.5, 17.5, 15.5)),
    ]


@icon("light-gun", CAT, "Handheld signal lamp with a flared head, a pistol grip and straight light beams",
      tags=["signal lamp", "aldis lamp", "tower signal", "radio failure", "light signal", "beam"])
def _(S):
    return [
        shell(poly([(2.5, 8.5), (14, 5), (14, 16), (2.5, 12.5)], closed=True, r=S.r * 0.4)),
        shell(rect(5.5, 13, 4, 8, rc(S, 1.5))),
        line(seg(17, 6, 21.5, 4.5)), line(seg(17.5, 10.5, 22, 10.5)), line(seg(17, 15, 21.5, 16.5)),
    ]


@icon("airport-beacon", CAT, "Short tower with a rotating lamp on top casting two opposite beams",
      tags=["rotating beacon", "aerodrome beacon", "green and white light", "airfield light", "lighthouse", "night marker"])
def _(S):
    return [
        shell(poly([(8.5, 21.5), (10.5, 13.5), (13.5, 13.5), (15.5, 21.5)], closed=True, r=S.r * 0.4)),
        shell(circle(12, 9.5, 2.6)),
        line(seg(8.5, 8, 2.5, 4.5)), line(seg(8.5, 11, 2.5, 14.5)),
        line(seg(15.5, 8, 21.5, 4.5)), line(seg(15.5, 11, 21.5, 14.5)),
    ]


@icon("runway-visual-range", CAT, "Two sensor heads on posts facing each other across a gap with fog lines between them",
      tags=["rvr", "visibility sensor", "transmissometer", "fog", "low visibility", "weather sensor"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 5, 7, rc(S, 1.5))), shell(rect(16.5, 4.5, 5, 7, rc(S, 1.5))),
        line(seg(5, 11.5, 5, 21.5)), line(seg(19, 11.5, 19, 21.5)),
        line(seg(10, 6.5, 14, 6.5)), line(seg(10, 10, 14, 10)), line(seg(10, 14, 14, 14)),
    ]


# ============================================================================ chunk 6

@icon("arresting-gear", CAT, "Jet seen from above hooking a cable stretched across the runway so it pulls into a V",
      tags=["arrestor cable", "tail hook", "carrier landing", "military runway", "aircraft arrest", "barrier"])
def _(S):
    return [
        solid(poly(plane_pts(12, 7, 11, 0), closed=True)),
        line(seg(12, 12.5, 12, 18)),
        line(poly([(2.5, 13.5), (12, 18), (21.5, 13.5)])),
        
    ]


@icon("arrestor-bed", CAT, "Aircraft nose wheel on a strut sinking into a textured block bed at the end of a runway",
      tags=["engineered materials arrestor system", "emas", "overrun", "runway end", "crushable bed", "safety area"])
def _(S):
    return [
        line("M5 7Q6 2.5 12 2.5"),
        line(seg(12, 2.5, 12, 8)),
        shell(circle(12, 11.5, 3)),
        shell(rect(2.5, 14.5, 19, 7, rc(S, 1.5))),
        dot(6, 18, 0.9), dot(10, 19.5, 0.9), dot(14, 18, 0.9), dot(18, 19.5, 0.9),
    ]


@icon("blast-fence", CAT, "Curved slatted barrier wall on the right with exhaust lines blowing toward it",
      tags=["jet blast deflector", "jet blast", "engine exhaust", "deflector", "airport barrier", "run up"])
def _(S):
    return [
        shell("M13 3Q19 12 13 21L18 21Q24 12 18 3Z"),
        detail(seg(15.25, 7.5, 20.25, 7.5)), detail(seg(16, 12, 21, 12)), detail(seg(15.25, 16.5, 20.25, 16.5)),
        line(seg(2.5, 5, 9, 4)), line(seg(2.5, 12, 11, 12)), line(seg(2.5, 19, 9, 20)),
    ]


@icon("bird-scarer", CAT, "Gas cannon with a flared barrel on a tripod and a bird flying away",
      tags=["bird control", "wildlife hazard", "propane cannon", "scare device", "bird strike prevention", "airfield safety"])
def _(S):
    return [
        shell(poly([(6.5, 12.5), (8.5, 15), (19.5, 9), (15.5, 5)], closed=True, r=S.r * 0.4)),
        line(seg(8, 15, 4.5, 21.5)), line(seg(8, 15, 11.5, 21.5)),
        line("M2.5 6Q4 3.5 6 6Q8 3.5 9.5 6"),
        line(seg(20.5, 4, 22, 2.5)),
    ]


@icon("foreign-object-debris", CAT, "Broken tire tread piece lying on pavement with a loose bolt and small fragments beside it",
      tags=["fod", "runway debris", "loose object", "sweeping", "tire fragment", "airfield hazard"])
def _(S):
    return [
        shell("M1.65 16A7 7 0 0 1 14.35 16L11.2 17.5A3.5 3.5 0 0 0 4.8 17.5Z"),
        shell(poly(regular(19, 14, 2.6, 6), closed=True, r=S.r * 0.4)),
        dot(13.5, 19.5, 0.9), dot(8, 19.8, 0.8),
        line(seg(16, 20.5, 21.5, 20.5)),
    ]


@icon("follow-me-car", CAT, "Small car side view with a checkered sign on its roof",
      tags=["airport car", "guide vehicle", "apron escort", "taxi guidance", "marshal vehicle", "airfield vehicle"])
def _(S):
    return [
        shell(rect(7, 2.5, 10, 5, rc(S, 1))),
        sd(9, 4.3, 1.4, 1.4), sd(11.3, 4.3, 1.4, 1.4), sd(13.6, 4.3, 1.4, 1.4),
        shell(poly([(2.5, 17.5), (2.5, 14), (7, 13), (8.5, 10), (15.5, 10), (18, 13), (21.5, 14), (21.5, 17.5)], closed=True, r=S.r * 0.6)),
        shell(circle(7, 18, 1.8)), shell(circle(17, 18, 1.8)),
    ]


@icon("aircraft-tow-bar", CAT, "Long bar on two small wheels with a ring towing eye at one end and a forked head at the other",
      tags=["towbar", "pushback", "tug bar", "aircraft towing", "ground handling", "nose gear tow"])
def _(S):
    return [
        shell(circle(3.8, 12.5, 2)),
        shell(rect(6.5, 11, 10, 3, rc(S, 1))),
        line(poly([(16.5, 12.5), (21, 8)])), line(poly([(16.5, 12.5), (21, 17)])),
        shell(circle(9, 18.5, 1.8)), shell(circle(14, 18.5, 1.8)),
    ]


@icon("ground-power-unit", CAT, "Boxy wheeled cart with a coiled cable on its side and a thick cable ending in a large plug",
      tags=["gpu", "ground power", "external power", "aircraft power cart", "generator", "400hz"])
def _(S):
    return [
        shell(rect(2.5, 6, 13, 12, rc(S, 3.5))),
        detail(circle(9, 12, 3)),
        shell(circle(6, 19.5, 1.8)), shell(circle(12, 19.5, 1.8)),
        line("M15.5 9H18.5Q20 9 20 11V14"),
        shell(rect(18, 14, 4, 6, rc(S, 1.5))),
    ]


@icon("preconditioned-air-unit", CAT, "Corrugated hose rising from a box unit up toward the belly of a fuselage",
      tags=["pca", "ground air conditioning", "cabin cooling", "jet bridge air", "air hose", "pre-conditioned air"])
def _(S):
    return [
        line("M9 4Q16 7 22 3.5"),
        shell(rect(2.5, 13, 8, 8, rc(S, 1.5))),
        line(arc(10.5, 8, 6.5, 0, 22)), line(arc(10.5, 8, 6.5, 34, 56)), line(arc(10.5, 8, 6.5, 68, 90)),
    ]


@icon("lavatory-service-truck", CAT, "Small service truck with a round waste tank on its back and a hose reaching up toward a fuselage",
      tags=["lav truck", "waste service", "toilet service", "ground servicing", "honey wagon", "aircraft servicing"])
def _(S):
    return [
        shell(poly([(2, 18), (2, 12.5), (6, 12.5), (8, 15), (8, 18)], closed=True, r=S.r * 0.4)),
        shell(rect(9.5, 9.5, 12, 8.5, L(S, 3, 4))),
        shell(circle(5, 19.5, 1.7)), shell(circle(16, 19.5, 1.7)),
        line(poly([(15.5, 9.5), (15.5, 5.5), (20, 2.5)], r=S.r)),
    ]


@icon("fuel-hydrant-pit", CAT, "Open pit in the apron pavement with a lid raised and a fuel hose connected to the valve",
      tags=["hydrant", "aircraft refueling", "fuel pit", "apron fuel", "fuel hose", "jet fuel"])
def _(S):
    return [
        line(seg(2, 10, 5.5, 10)), line(seg(18.5, 10, 22, 10)),
        shell(rect(5.5, 10, 13, 11, rc(S, 1.5))),
        detail(circle(12, 15.5, 2)),
        line(seg(5.5, 10, 3, 4.5)),
        line(poly([(12, 13.5), (12, 6), (18, 3.5)], r=S.r)),
    ]


@icon("wing-walker", CAT, "Ground crew figure in a vest holding a raised baton beside a wing tip",
      tags=["marshaller", "wing walker", "ground crew", "aircraft guide", "apron safety", "taxi signal"])
def _(S):
    return [
        shell(circle(9, 4.5, 2.2)),
        shell(poly([(7, 8), (11, 8), (10.5, 15), (7.5, 15)], closed=True, r=S.r * 0.5)),
        line(poly([(11, 9), (15, 5.5)])), line(poly([(15, 5.5), (17.5, 2.5)])),
        line(poly([(7, 9.5), (4.5, 13.5)])),
        line(poly([(8, 15), (7, 21.5)])), line(poly([(10, 15), (11, 21.5)])),
        shell(poly([(15, 14.5), (22, 12.5), (22, 17), (15, 18.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("aircraft-maintenance-dock", CAT, "Airplane tail rising in the middle of a scaffold platform with posts and railings",
      tags=["hangar", "maintenance stand", "scaffold", "mro", "aircraft hangar dock", "repair bay"])
def _(S):
    return [
        line(seg(3, 3, 3, 21.5)), line(seg(21, 3, 21, 21.5)),
        line(seg(2.5, 17, 21.5, 17)),
        line(seg(3, 9, 6, 9)), line(seg(18, 9, 21, 9)),
        shell(poly([(8.5, 17), (9.5, 4), (12.5, 4), (15.5, 17)], closed=True, r=S.r * 0.4)),
    ]


@icon("aircraft-jack", CAT, "Tripod jack with a vertical ram lifting the underside of a wing",
      tags=["jacking", "lift aircraft", "tripod jack", "maintenance", "wing lift", "hydraulic jack"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 4, rc(S, 2))),
        line(seg(12, 6.5, 12, 11)),
        shell(rect(9.5, 11, 5, 5, rc(S, 1))),
        line(seg(12, 16, 4.5, 21.5)), line(seg(12, 16, 19.5, 21.5)),
    ]
