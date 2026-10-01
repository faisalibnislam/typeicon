"""TypeIcon Core: aviation (flight operations, aircraft types, passenger journey), batch 002."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, U, fmt, path_to_d

CAT = "aviation"


def L(S, a, b):
    return a if S.name == "line" else b


def rc(S, cap):
    return min(S.R, cap)


def sd(x, y, w, h):
    """Small solid rectangle (knocked out of a Filled shell)."""
    return Part("dot", rect(x, y, w, h))


def rot_pts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


_TOP = [(0, -1.0), (0.22, -0.55), (0.22, -0.2), (1.0, 0.25), (1.0, 0.5), (0.22, 0.3), (0.2, 0.75), (0.5, 0.95),
        (0.5, 1.1), (0, 1.0), (-0.5, 1.1), (-0.5, 0.95), (-0.2, 0.75), (-0.22, 0.3), (-1.0, 0.5), (-1.0, 0.25),
        (-0.22, -0.2), (-0.22, -0.55)]


def tplane(cx, cy, s, deg, knock=False, r=0.0) -> Part:
    """Small top-view airplane silhouette, nose along deg (0 = up)."""
    pts = rot_pts([(cx + s * x, cy + s * y) for x, y in _TOP], deg, cx, cy)
    d = poly(pts, closed=True, r=r)
    return Part("dot", d) if knock else solid(d)


_SIDE = [(1.0, 0.0), (0.72, -0.3), (-0.55, -0.3), (-0.9, -0.95), (-1.0, -0.95), (-1.0, 0.1), (0.5, 0.2)]
_SWING = [(0.25, 0.05), (-0.4, 0.05), (-0.55, 0.8), (-0.25, 0.8)]


def splane(cx, cy, s, knock=False) -> list:
    """Small side-view airplane (nose right) as solid parts."""
    out = []
    for pts in (_SIDE, _SWING):
        d = poly([(cx + s * x, cy + s * y) for x, y in pts], closed=True)
        out.append(Part("dot", d) if knock else solid(d))
    return out


def star(cx, cy, R, knock=True) -> Part:
    pts = []
    for i in range(10):
        r = R if i % 2 == 0 else R * 0.45
        a = math.radians(-90 + 36 * i)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d = poly(pts, closed=True)
    return Part("dot", d) if knock else solid(d)


def dashes(pts, on=2.0, off=2.0):
    out, cur, pos, draw = [], [], 0.0, True
    seglen = on
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        ln = math.hypot(x1 - x0, y1 - y0)
        t = 0.0
        while t < ln - 1e-9:
            step = min(seglen - pos, ln - t)
            a = (x0 + (x1 - x0) * t / ln, y0 + (y1 - y0) * t / ln)
            b = (x0 + (x1 - x0) * (t + step) / ln, y0 + (y1 - y0) * (t + step) / ln)
            if draw:
                if not cur:
                    cur = [a]
                cur.append(b)
            t += step
            pos += step
            if pos >= seglen - 1e-9:
                if draw and len(cur) > 1:
                    out.append(poly(cur))
                cur, draw, pos = [], not draw, 0.0
                seglen = on if draw else off
    if draw and len(cur) > 1:
        out.append(poly(cur))
    return out


def wave(x, y, n=4, w=5, h=2.5):
    """Wavy line starting at (x, y): n half cycles alternating up/down."""
    d = f"M{fmt(x)} {fmt(y)}"
    for i in range(n):
        d += f"a{fmt(w / 2)} {fmt(h)} 0 0 {1 if i % 2 == 0 else 0} {fmt(w)} 0"
    return d


# ============================================================================ chunk 1

@icon("flight-plan", CAT, "Clipboard form with a small airplane at the top and a route joining two dots",
      tags=["flight planning", "route", "clipboard", "pilot", "itinerary", "dispatch", "preflight"])
def _(S):
    return [
        shell(rect(4, 4.5, 16, 17.5, rc(S, 2.5))),
        shell(rect(9, 2, 6, 4, rc(S, 1.5))),
        tplane(12, 11, 3, 90, knock=True),
        dot(8, 18, 1.3), dot(16, 18, 1.3),
        detail(seg(10.5, 18, 13.5, 18)),
    ]


@icon("notam", CAT, "Sheet of paper with a warning triangle and a small airplane above several text lines",
      tags=["notice to airmen", "flight notice", "aviation warning", "pilot briefing", "hazard notice", "airspace alert"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, rc(S, 2.5))),
        Part("dot", poly([(9.5, 6), (12, 10.5), (7, 10.5)], closed=True)),
        tplane(15.5, 8.5, 2.4, 90, knock=True),
        detail(seg(8, 14.5, 16, 14.5)),
        detail(seg(8, 18, 13, 18)),
    ]


@icon("metar-report", CAT, "Paper strip with a wind barb on the left and lines of coded weather text",
      tags=["weather report", "aviation weather", "airport weather", "wind", "taf", "observation", "pilot briefing"])
def _(S):
    return [
        shell(rect(3, 4, 18, 16, rc(S, 2.5))),
        detail(seg(7.5, 8, 7.5, 14.5)),
        detail(seg(7.5, 8, 10.5, 9.5)),
        dot(7.5, 16, 1.2),
        detail(seg(13, 9, 17.5, 9)),
        detail(seg(13, 13, 17.5, 13)),
        detail(seg(11, 17, 17.5, 17)),
    ]


@icon("go-around", CAT, "Airplane just above a runway climbing away along a curved upward path",
      tags=["missed approach", "aborted landing", "climb out", "balked landing", "overshoot", "approach"])
def _(S):
    return [
        line(seg(2, 20.5, 22, 20.5)),
        line("M3.5 17Q9.5 17 11.5 12.5"),
        tplane(16.5, 8, 4.2, 50),
    ]


@icon("touch-and-go", CAT, "Dashed flight path dipping down to touch a runway and rising again",
      tags=["circuit training", "practice landing", "pattern work", "bounce", "flight training", "landing"])
def _(S):
    pts = [(2 + 16 * i / 40, 17 - 11 * ((2 + 16 * i / 40 - 12) / 10) ** 2) for i in range(41)]
    return [
        line(seg(2, 20.5, 22, 20.5)),
        *[line(d) for d in dashes(pts, 2, 1.8)],
        tplane(20, 8, 3.4, 40),
    ]


@icon("flight-level", CAT, "Airplane in side view flying along a level line beside an altitude scale",
      tags=["altitude", "cruise", "fl", "cruising level", "height", "air traffic", "pressure altitude"])
def _(S):
    return [
        line(seg(4, 3.5, 4, 20.5)),
        line(seg(4, 6, 7.5, 6)), line(seg(4, 12, 7.5, 12)), line(seg(4, 18, 7.5, 18)),
        *splane(16, 11.5, 5.5),
        line(seg(10, 12.5, 11.2, 12.5)),
    ]


@icon("ditching", CAT, "Airplane in side view floating on water with waves around its fuselage",
      tags=["water landing", "sea landing", "emergency", "crash into water", "ocean", "sinking", "life raft"])
def _(S):
    return [
        *splane(12, 10, 8),
        line(wave(2, 17, 4, 5, 1.8)),
        line(wave(2, 21, 4, 5, 1.8)),
    ]


@icon("red-eye-flight", CAT, "Airplane flying past a crescent moon with a few small stars",
      tags=["night flight", "overnight flight", "late flight", "midnight", "nighttime", "sleep", "long haul"])
def _(S):
    cres = path_to_d(D(P(circle(9, 13.5, 6.5)), P(circle(12.5, 11, 5.7))))
    return [
        shell(cres),
        tplane(17.5, 7, 3.6, 60),
        star(18.5, 17, 2, knock=False),
        dot(13, 20, 0.9),
    ]


@icon("frequent-flyer", CAT, "Membership card with a small airplane emblem and a row of stars along the bottom",
      tags=["loyalty card", "miles", "rewards", "airline membership", "points", "status", "elite"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, rc(S, 3))),
        tplane(8, 9.5, 2.8, 90, knock=True),
        detail(seg(13, 8.5, 19, 8.5)),
        detail(seg(13, 11.5, 17, 11.5)),
        star(7, 16, 1.7), star(11, 16, 1.7), star(15, 16, 1.7),
    ]


@icon("seat-upgrade", CAT, "Airline seat in side view beside a thick upward arrow",
      tags=["upgrade", "business class", "premium seat", "better seat", "class change", "bump up", "first class"])
def _(S):
    return [
        shell(poly([(2.5, 3.5), (6.5, 3.5), (7.5, 10.5), (13.5, 10.5), (13.5, 15), (4, 15)], closed=True, r=S.r)),
        line(seg(8, 15, 8, 20.5)), line(seg(5, 20.5, 11, 20.5)),
        line(seg(19, 20, 19, 6)),
        line(poly([(15.5, 9.5), (19, 6), (22.5, 9.5)], r=S.r)),
    ]


@icon("fragile-baggage-tag", CAT, "Luggage tag on a looped strap printed with a wine glass symbol",
      tags=["fragile", "handle with care", "breakable", "glass", "luggage label", "baggage label", "special handling"])
def _(S):
    return [
        shell(rect(5, 8, 14, 13.5, rc(S, 2.5))),
        line("M9.5 8V5.5a2.5 2.5 0 0 1 5 0V8"),
        Part("dot", poly([(9.8, 11.5), (14.2, 11.5), (13.6, 14.5), (12, 15.8), (10.4, 14.5)], closed=True)),
        detail(seg(12, 15.5, 12, 18.5)),
        Part("dot", rect(10, 18.2, 4, 1.2)),
    ]


@icon("heavy-baggage-tag", CAT, "Luggage tag on a looped strap printed with a kettlebell weight symbol",
      tags=["heavy bag", "overweight", "weight limit", "luggage label", "baggage label", "lift with care", "two person lift"])
def _(S):
    return [
        shell(rect(3.5, 7, 17, 14.5, rc(S, 2.5))),
        line("M9 7V5a3 3 0 0 1 6 0V7"),
        dot(12, 16.3, 3.6),
        detail(poly([(9, 13), (9, 10.5), (15, 10.5), (15, 13)])),
    ]


@icon("restricted-airspace", CAT, "Map area bounded by a closed outline with short hatch ticks along its inside edge",
      tags=["controlled airspace", "no entry", "airspace boundary", "military zone", "danger area", "prohibited area"])
def _(S):
    return [
        shell(poly([(4, 8), (13, 3.5), (21, 9.5), (18, 20), (6.5, 19)], closed=True, r=S.r)),
        detail(seg(5.5, 12, 8.5, 12)),
        detail(seg(11, 7.5, 11.8, 10.5)),
        detail(seg(18, 14, 15, 14)),
        detail(seg(11, 19, 11, 16)),
    ]


@icon("no-fly-zone", CAT, "Dashed circular boundary with a bar across its centre and a small airplane outside it",
      tags=["drone ban", "flight prohibited", "exclusion zone", "restricted area", "airspace", "geofence"])
def _(S):
    cx, cy, r = 9.5, 14.5, 6.5
    return [
        *[line(arc(cx, cy, r, a, a + 28)) for a in range(0, 360, 45)],
        line(seg(5.5, 18.5, 13.5, 10.5)),
        tplane(18.5, 6, 3.2, 60),
    ]


@icon("flight-strip", CAT, "Long narrow paper strip in a holder divided into columns with short text marks",
      tags=["strip", "air traffic control", "callsign", "controller", "paper strip", "atc", "tower"])
def _(S):
    return [
        shell(rect(2, 6.5, 20, 11, rc(S, 2.5))),
        detail(seg(8, 6.5, 8, 17.5)),
        detail(seg(15.5, 6.5, 15.5, 17.5)),
        detail(seg(10.5, 12, 13, 12)),
        detail(seg(18, 12, 20, 12)),
    ]


# ============================================================================ chunk 2

@icon("remove-before-flight-tag", CAT, "Long streamer tag with a swallow tail, a hole at the top and bold lettering lines",
      tags=["pre-flight", "red tag", "pitot cover", "safety streamer", "ground crew", "maintenance", "preflight check"])
def _(S):
    return [
        shell(poly([(7, 2.5), (17, 2.5), (17, 21.5), (12, 18.5), (7, 21.5)], closed=True, r=S.r * 0.6)),
        dot(12, 6, 1.5),
        detail(seg(9.5, 11, 14.5, 11)),
        detail(seg(9.5, 15, 14.5, 15)),
    ]


@icon("air-traffic-control-console", CAT, "Desk console with two radar screens standing above it",
      tags=["atc", "radar screen", "controller desk", "tower", "air traffic controller", "workstation", "airport control"])
def _(S):
    return [
        shell(rect(2.5, 3, 8.5, 9, L(S, 1, 3.5))),
        shell(rect(13, 3, 8.5, 9, L(S, 1, 3.5))),
        dot(7, 7.5, 1.3), dot(17, 6.8, 1.1), dot(18.5, 9.2, 1.1),
        line(seg(6.75, 12, 6.75, 15)), line(seg(17.25, 12, 17.25, 15)),
        shell(rect(2, 15, 20, 6, rc(S, 2))),
    ]


@icon("airspace-classes", CAT, "Airspace shown as stepped layers, widest at the top, above a small airport tower",
      tags=["airspace", "controlled airspace", "class a", "class b", "layers", "altitude zones", "air traffic"])
def _(S):
    return [
        shell(poly([(2.5, 3), (21.5, 3), (21.5, 7), (18.5, 7), (18.5, 11), (15.5, 11), (15.5, 14),
                    (8.5, 14), (8.5, 11), (5.5, 11), (5.5, 7), (2.5, 7)], closed=True, r=S.r * 0.6)),
        line(poly([(10, 21), (10, 18), (14, 18), (14, 21)], r=S.r)),
        line(seg(2, 21, 22, 21)),
    ]


@icon("crosswind-landing", CAT, "Airplane angled into sideways wind arrows while approaching a runway",
      tags=["crab", "side wind", "gusty landing", "wind arrows", "approach", "runway", "weather"])
def _(S):
    out = [
        line(seg(14, 12, 14, 21.5)), line(seg(20.5, 12, 20.5, 21.5)),
        tplane(17.5, 6, 3.6, 160),
    ]
    for y in (8, 15):
        out += [line(seg(2.5, y, 9, y)), line(poly([(6.5, y - 2.2), (9, y), (6.5, y + 2.2)], r=S.r))]
    return out


@icon("emergency-landing", CAT, "Airplane descending toward a runway with a flame burning at its side",
      tags=["forced landing", "engine failure", "fire", "mayday", "crash landing", "safety", "incident"])
def _(S):
    flame = "M6 3.5C8.2 6.2 9.4 7.8 9.4 10a3.4 3.4 0 0 1-6.8 0C2.6 8 3.8 6.5 6 3.5Z"
    return [
        line(seg(2, 20.5, 22, 20.5)),
        solid(flame),
        tplane(16.5, 11, 4.6, 115),
    ]


@icon("mayday", CAT, "Large exclamation mark between curved radio wave arcs on both sides",
      tags=["distress call", "emergency radio", "sos", "radio call", "urgent", "pan-pan", "emergency"])
def _(S):
    return [
        line(seg(12, 4.5, 12, 13.5)),
        dot(12, 18.5, 1.6),
        line(arc(12, 12, 6, 145, 215)), line(arc(12, 12, 10, 150, 210)),
        line(arc(12, 12, 6, 325, 395)), line(arc(12, 12, 10, 330, 390)),
    ]


@icon("flight-diverted", CAT, "Dashed route forking where one branch is crossed out and the other ends at a new destination",
      tags=["diversion", "rerouted", "alternate airport", "flight change", "redirect", "detour", "re-route"])
def _(S):
    main = [(4, 19), (11, 12)]
    up = [(11, 12), (20, 3.5)]
    right = [(11, 12), (14, 12), (19, 15.5)]
    return [
        *[line(d) for d in dashes(main, 2, 1.8)],
        *[line(d) for d in dashes(up, 2, 1.8)],
        line(seg(14.5, 4.5, 18.5, 8.5)),
        line(seg(18.5, 4.5, 14.5, 8.5)),
        *[line(d) for d in dashes(right, 2, 1.8)],
        dot(20.5, 17.5, 2),
    ]


def uni(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


@icon("regional-jet", CAT, "Slim airliner in side view with a high T-shaped tail and engines on the rear fuselage",
      tags=["commuter jet", "small airliner", "short haul", "t-tail", "airplane", "rear engines", "airline"])
def _(S):
    body = uni(rect(2.5, 9, 19.5, 6, 3),
               poly([(2.5, 10), (3.5, 4.5), (6.5, 4.5), (8.5, 10)], closed=True, r=S.r * 0.4),
               rect(1.5, 3.5, 7.5, 2, L(S, 0, 1)),
               poly([(10, 14), (15, 14), (12.5, 20.5), (9.5, 20.5)], closed=True, r=S.r * 0.4))
    return [shell(body), shell(rect(4, 16.5, 4.5, 3, rc(S, 1.5)))]


@icon("trijet", CAT, "Airliner in side view with an engine under the wing and a third engine at the base of the tail fin",
      tags=["three engines", "tri-engine", "airliner", "airplane", "tail engine", "long haul", "jet"])
def _(S):
    body = uni(rect(2.5, 10.5, 19.5, 6, 3),
               poly([(2.5, 11), (3, 3.5), (6.5, 3.5), (9, 11)], closed=True, r=S.r * 0.4),
               rect(1.5, 6, 6, 4.5, rc(S, 2)),
               poly([(10.5, 15.5), (15.5, 15.5), (13, 21.5), (10, 21.5)], closed=True, r=S.r * 0.4))
    return [shell(body), shell(rect(16, 18, 4.5, 3, rc(S, 1.5)))]


@icon("bush-plane", CAT, "High-wing single propeller plane in side view with wing struts and fat tundra tires",
      tags=["backcountry", "tundra tires", "light aircraft", "single engine", "wilderness", "airplane", "stol"])
def _(S):
    return [
        shell(poly([(2, 6.5), (4.5, 6.5), (8, 10), (16, 10), (19.5, 11.5), (19.5, 15), (3, 15)], closed=True, r=S.r * 0.6)),
        line(seg(6, 4.5, 18, 4.5)),
        line(seg(10, 4.5, 12, 10)), line(seg(16, 4.5, 15, 10)),
        shell(circle(8, 19.5, 2.4)), shell(circle(15.5, 19.5, 2.4)),
        line(seg(8, 15, 8, 17.1)), line(seg(15.5, 15, 15.5, 17.1)),
        line(seg(22, 9.5, 22, 16.5)),
    ]


@icon("warbird", CAT, "Vintage single-seat propeller fighter seen from above with oval wings and a bubble canopy",
      tags=["fighter", "vintage aircraft", "ww2 plane", "propeller", "airshow", "historic aircraft", "warplane"])
def _(S):
    wing = ellipse(12, 11.5, 10, 3.2)
    fus = ellipse(12, 12, 2.4, 8)
    tail = poly([(7.5, 19.5), (12, 18), (16.5, 19.5), (16.5, 20.5), (7.5, 20.5)], closed=True, r=S.r * 0.6)
    both = path_to_d(U(P(wing), P(fus), P(tail)))
    return [
        shell(both),
        line(seg(8.5, 2, 15.5, 2)),
        Part("dot", ellipse(12, 11, 1.1, 2.2)),
    ]


@icon("twin-boom-aircraft", CAT, "Aircraft from above with a central pod and wing, two long tail booms joined by a horizontal tail",
      tags=["twin boom", "double tail", "pusher", "boom tail", "observation aircraft", "airplane", "top view"])
def _(S):
    pod = rect(9.5, 2.5, 5, 12, 2.5)
    wing = rect(2, 7.5, 20, 3.5, rc(S, 1.5))
    return [
        shell(path_to_d(U(P(pod), P(wing)))),
        line(seg(5.5, 11, 5.5, 20)), line(seg(18.5, 11, 18.5, 20)),
        line(seg(4, 20.5, 20, 20.5)),
    ]


# ============================================================================ chunk 3

def arrow(S, x, y, dx, dy, ln=4.5, hd=2.2):
    """Arrow from (x, y) of length ln along unit direction (dx, dy), head at the far end."""
    ex, ey = x + dx * ln, y + dy * ln
    px, py = -dy, dx
    bx, by = ex - dx * hd, ey - dy * hd
    return [line(seg(x, y, ex, ey)), line(poly([(bx + px * hd, by + py * hd), (ex, ey), (bx - px * hd, by - py * hd)], r=S.r))]


@icon("flight-booking", CAT, "Calendar page with a small airplane in one date and a check mark beside it",
      tags=["book flight", "reserve flight", "travel date", "schedule", "reservation", "ticket booking", "trip planner"])
def _(S):
    return [
        shell(rect(3, 5, 18, 16, rc(S, 2.5))),
        line(seg(8, 2.5, 8, 6.5)), line(seg(16, 2.5, 16, 6.5)),
        detail(seg(3, 10, 21, 10)),
        tplane(8.5, 15.5, 2.7, 90, knock=True),
        detail(poly([(13, 15.5), (15.5, 18), (19, 13.5)])),
    ]


@icon("four-forces-of-flight", CAT, "Small airplane from above with four arrows pointing up, down, forward and backward",
      tags=["lift", "weight", "thrust", "drag", "aerodynamics", "physics of flight", "flight forces"])
def _(S):
    return [
        tplane(12, 12, 3.2, 90),
        *arrow(S, 12, 7.5, 0, -1, 5, 2),
        *arrow(S, 12, 16.5, 0, 1, 5, 2),
        *arrow(S, 7.5, 12, -1, 0, 5, 2),
        *arrow(S, 16.5, 12, 1, 0, 5, 2),
    ]


@icon("afterburner", CAT, "Flared jet exhaust nozzle seen from the side with a long flame shooting out behind it",
      tags=["jet engine", "reheat", "thrust", "fighter jet", "exhaust", "afterburning", "supersonic"])
def _(S):
    return [
        shell(poly([(2.5, 8), (9, 6.5), (9, 17.5), (2.5, 16)], closed=True, r=S.r * 0.6)),
        detail(seg(6, 7.5, 6, 16.5)),
        solid("M11.5 8.5Q18 8.5 22.5 12Q18 15.5 11.5 15.5Z"),
    ]


@icon("boarding-pass-reader", CAT, "Slanted pedestal scanner with a boarding pass held above its glass window",
      tags=["gate scanner", "barcode scanner", "check in", "boarding gate", "scan pass", "ticket reader", "airport"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 6, rc(S, 1.5))),
        tplane(9, 5.5, 1.7, 90, knock=True),
        detail(seg(13, 5.5, 17, 5.5)),
        shell(poly([(2.5, 21.5), (2.5, 16), (6.5, 12.5), (17.5, 12.5), (21.5, 16), (21.5, 21.5)], closed=True, r=S.r)),
        detail(seg(8, 16.5, 16, 16.5)),
    ]


@icon("gate-podium", CAT, "Counter desk with a screen on top and a number sign on a post beside it",
      tags=["boarding gate", "gate agent", "check-in counter", "departure gate", "airline desk", "lectern", "gate number"])
def _(S):
    return [
        shell(poly([(2.5, 21.5), (3.5, 12), (14.5, 12), (15.5, 21.5)], closed=True, r=S.r * 0.6)),
        shell(rect(4.5, 4, 9, 6, rc(S, 1.5))),
        line(seg(19, 21.5, 19, 9)),
        shell(rect(16, 2.5, 6, 6.5, rc(S, 1.5))),
        detail(seg(19, 4.5, 19, 7)),
    ]


@icon("in-flight-map", CAT, "Seatback screen showing a dashed arc between two dots with a small airplane partway along it",
      tags=["flight tracker", "route map", "entertainment screen", "flight progress", "moving map", "seat screen", "journey"])
def _(S):
    arcpts = [(6 + 12 * t, 15.5 - 8 * (1 - (2 * t - 1) ** 2)) for t in [i / 24 for i in range(25)]]
    mid = arcpts[:10] + [arcpts[10]]
    rest = arcpts[14:]
    return [
        shell(rect(2, 3, 20, 14.5, rc(S, 2.5))),
        dot(6, 15, 1.4), dot(18, 15, 1.4),
        detail(poly(arcpts[:8])), detail(poly(arcpts[17:23])),
        tplane(12, 7.7, 2.1, 90, knock=True),
        line(seg(12, 17.5, 12, 21)), line(seg(8, 21, 16, 21)),
    ]


@icon("aircraft-lightning-strike", CAT, "Airplane in flight with a jagged lightning bolt touching its wing",
      tags=["thunderstorm", "storm", "weather hazard", "static discharge", "turbulence", "strike", "electrical"])
def _(S):
    return [
        tplane(8, 9.5, 5.2, 305),
        shell(poly([(17.5, 3), (11.5, 12.5), (15.5, 12.5), (13.5, 21), (21, 10), (17, 10), (20, 3)], closed=True, r=S.r * 0.5)),
    ]


@icon("formation-flight", CAT, "Three small jets flying in a V formation each trailing a straight line",
      tags=["air show", "flying team", "squadron", "v formation", "aerobatic team", "flypast", "display team"])
def _(S):
    return [
        tplane(12, 5, 2.6, 0), tplane(5.5, 11.5, 2.6, 0), tplane(18.5, 11.5, 2.6, 0),
        line(seg(12, 9, 12, 14)),
        line(seg(5.5, 15.5, 5.5, 21)), line(seg(18.5, 15.5, 18.5, 21)),
    ]


@icon("plane-spotting", CAT, "Person holding binoculars up to look at a small airplane flying overhead",
      tags=["aviation enthusiast", "watching planes", "hobby", "airport viewing", "binoculars", "spotter", "airplane watching"])
def _(S):
    return [
        shell(circle(7, 10, 2.6)),
        shell(poly([(2.5, 21.5), (2.5, 17), (4.5, 14), (9.5, 14), (11.5, 17), (11.5, 21.5)], closed=True, r=S.r)),
        solid(circle(11.2, 7.8, 1.4)), solid(circle(13.8, 6, 1.4)),
        tplane(18.5, 5.5, 3, 80),
    ]


@icon("baggage-handler", CAT, "Ground crew worker with ear defenders lifting a suitcase with both hands",
      tags=["ramp agent", "loader", "airport worker", "ground crew", "luggage", "porter", "suitcase lifting"])
def _(S):
    return [
        shell(circle(8, 5.5, 2.4)),
        line(arc(8, 5.5, 4, 195, 345)),
        line(seg(8, 8.5, 8, 15)),
        line(poly([(8, 10.5), (12.5, 12)], r=S.r)),
        line(poly([(8, 15), (5.5, 21)])), line(poly([(8, 15), (11, 21)])),
        shell(rect(12.5, 10, 8.5, 9.5, rc(S, 2))),
        line(poly([(15, 10), (15, 7.5), (18.5, 7.5), (18.5, 10)], r=S.r)),
    ]


@icon("pilot-logbook", CAT, "Open hardcover book with ruled lines on the left page and a small airplane on the right",
      tags=["flight log", "flight hours", "record book", "pilot record", "journal", "aviation hours", "training log"])
def _(S):
    return [
        shell(poly([(2.5, 5.5), (12, 7.5), (21.5, 5.5), (21.5, 19.5), (12, 21.5), (2.5, 19.5)], closed=True, r=S.r * 0.5)),
        detail(seg(12, 7.5, 12, 21.5)),
        detail(seg(5.5, 11.5, 9, 11.5)), detail(seg(5.5, 15.5, 9, 15.5)),
        tplane(17, 11.5, 2.4, 90, knock=True),
        detail(seg(15, 16, 18.5, 16)),
    ]


@icon("pilot-license", CAT, "Identification card with a small portrait square and a pair of wings emblem",
      tags=["pilot certificate", "aviator id", "licence", "flight school", "credential", "ppl", "airman"])
def _(S):
    return [
        shell(rect(2, 4.5, 20, 15, rc(S, 3))),
        sd(5, 8, 5.5, 6),
        tplane(17, 10.5, 2.8, 0, knock=True),
        detail(seg(13.5, 15.5, 20, 15.5)),
    ]


@icon("closed-runway-marking", CAT, "Runway strip seen from above with a large X painted across it",
      tags=["runway closed", "unusable runway", "airfield marking", "no landing", "cross", "airport hazard", "out of service"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rc(S, 2))),
        detail(seg(8.5, 7, 15.5, 17)),
        detail(seg(15.5, 7, 8.5, 17)),
    ]


@icon("passenger-manifest", CAT, "Clipboard with a small airplane at the top and rows of people listed below it",
      tags=["passenger list", "roster", "headcount", "boarding list", "crew list", "names", "flight manifest"])
def _(S):
    return [
        shell(rect(4, 4.5, 16, 17.5, rc(S, 2.5))),
        shell(rect(9, 2, 6, 4, rc(S, 1.5))),
        tplane(12, 9.5, 2.3, 90, knock=True),
        dot(8, 14, 1.2), detail(seg(11, 14, 16, 14)),
        dot(8, 18.3, 1.2), detail(seg(11, 18.3, 16, 18.3)),
    ]


# ============================================================================ chunk 4

@icon("baggage-claim-ticket", CAT, "Small sticker slip with bars of a barcode and a tear-off stub separated by a perforated line",
      tags=["luggage receipt", "bag tag", "lost baggage", "claim check", "barcode", "baggage receipt", "stub"])
def _(S):
    return [
        shell(rect(2, 5, 20, 14, rc(S, 2.5))),
        detail(seg(6, 8.5, 6, 15.5)), detail(seg(9.5, 8.5, 9.5, 15.5)), detail(seg(13, 8.5, 13, 15.5)),
        detail(seg(17, 6, 17, 8)), detail(seg(17, 11, 17, 13)), detail(seg(17, 16, 17, 18)),
    ]


@icon("damaged-baggage", CAT, "Hard shell suitcase with a zigzag crack across its face and a detached wheel",
      tags=["broken luggage", "lost and damaged", "baggage claim", "cracked suitcase", "airline complaint", "broken bag", "torn"])
def _(S):
    return [
        shell(rect(3.5, 7, 17, 11.5, rc(S, 2.5))),
        line(poly([(9, 7), (9, 3.5), (15, 3.5), (15, 7)], r=S.r)),
        detail(poly([(13.5, 7), (10.5, 11), (14, 13.5), (11, 18.5)])),
        dot(6.5, 21, 1.3), dot(20, 21.3, 1.2),
    ]


@icon("balloon-burner", CAT, "Hot air balloon burner on a frame above a basket rim with a tall flame rising from it",
      tags=["hot air balloon", "propane burner", "flame", "ballooning", "basket", "heat", "inflation"])
def _(S):
    return [
        solid("M12 1.8C14.6 4.8 15.7 6.6 15.7 8.6a3.7 3.7 0 0 1-7.4 0C8.3 6.6 9.4 4.8 12 1.8Z"),
        line(seg(7, 17, 7, 12.5)), line(seg(17, 17, 17, 12.5)),
        line(seg(7, 12.5, 17, 12.5)),
        shell(rect(4, 17, 16, 4.5, rc(S, 1.5))),
    ]


@icon("aisle-wheelchair", CAT, "Narrow upright transfer chair with a tall back, push handle and small wheels for an airplane aisle",
      tags=["accessibility", "mobility", "wheelchair", "reduced mobility", "assistance", "disabled passenger", "transfer chair"])
def _(S):
    return [
        shell(poly([(6, 2.5), (10, 2.5), (10.5, 12), (18, 12), (18, 16), (6.5, 16)], closed=True, r=S.r)),
        line(seg(6, 2.5, 3, 2.5)),
        shell(circle(7.5, 19.5, 2)), shell(circle(16.5, 19.5, 2)),
        detail(seg(8, 6.5, 8.3, 11)),
    ]


@icon("fuel-dumping", CAT, "Airliner seen from below with two spray trails streaming out behind its wing tips",
      tags=["fuel jettison", "emergency", "weight reduction", "landing prep", "wing spray", "overweight landing", "jettison"])
def _(S):
    return [
        tplane(12, 7.5, 5.2, 0),
        *[line(d) for d in dashes([(6.5, 10.5), (4.2, 21)], 2.2, 1.6)],
        *[line(d) for d in dashes([(17.5, 10.5), (19.8, 21)], 2.2, 1.6)],
    ]


def _roll_pts():
    pts = []
    for i in range(41):
        t = math.pi / 2 + 4 * math.pi * i / 40
        pts.append((1.0 * t + 2.9 * math.sin(t), 12 + 3.3 * math.cos(t)))
    x0 = min(p[0] for p in pts)
    return [(x - x0 + 2.5, y) for x, y in pts]


@icon("barrel-roll", CAT, "Small airplane trailing a looping corkscrew path behind it",
      tags=["aerobatics", "stunt", "air show", "roll", "loop", "acrobatic flight", "trick flying"])
def _(S):
    pts = _roll_pts()
    return [
        line(poly(pts)),
        tplane(20, 12, 3, 90),
    ]


@icon("aviation-obstruction-light", CAT, "Tall thin mast with a round lamp at its very top and short glow rays around it",
      tags=["tower light", "red beacon", "warning light", "mast", "chimney light", "obstacle light", "navigation hazard"])
def _(S):
    out = [shell(circle(12, 9.5, 2.6)), line(seg(12, 12.1, 12, 21.5)), line(seg(8.5, 21.5, 15.5, 21.5))]
    for a in (-90, -30, -150, 0, 180):
        out.append(line(seg(12 + 5 * math.cos(math.radians(a)), 9.5 + 5 * math.sin(math.radians(a)),
                            12 + 6.8 * math.cos(math.radians(a)), 9.5 + 6.8 * math.sin(math.radians(a)))))
    return out


@icon("runway-end-identifier-lights", CAT, "Runway end seen from above with a flashing light and arc on each side of it",
      tags=["reil", "threshold lights", "strobe", "runway lighting", "airport lights", "runway end", "flashing lights"])
def _(S):
    return [
        shell(rect(9.5, 6, 5, 15.5, rc(S, 1.5))),
        detail(seg(9.5, 18, 14.5, 18)),
        dot(5.5, 8.5, 1.7), dot(18.5, 8.5, 1.7),
        line(arc(5.5, 8.5, 3.6, 190, 260)), line(arc(18.5, 8.5, 3.6, 280, 350)),
    ]


@icon("weight-and-balance", CAT, "Small airplane and a weight block resting on opposite ends of a plank balanced on a triangle",
      tags=["load sheet", "centre of gravity", "payload", "loading", "balance", "seesaw", "aircraft loading"])
def _(S):
    return [
        shell(poly([(12, 13), (8, 20.5), (16, 20.5)], closed=True, r=S.r * 0.4)),
        line(seg(2.5, 12.2, 21.5, 12.2)),
        shell(rect(3, 6.5, 5.5, 4.2, rc(S, 1))),
        *splane(16.5, 8, 3),
    ]


@icon("overhead-panel", CAT, "Ceiling panel seen from below filled with rows of small toggle switches",
      tags=["cockpit", "switches", "flight deck", "systems panel", "overhead switches", "controls", "toggles"])
def _(S):
    out = [shell(rect(2, 3.5, 20, 17, rc(S, 2.5)))]
    for y in (6.5, 13):
        for x in (5, 9, 13, 17):
            out.append(Part("dot", rect(x, y, 2, 4.5, 1)))
    return out


@icon("flight-simulator", CAT, "Enclosed cockpit capsule with a windshield mounted on four angled hydraulic legs",
      tags=["training", "pilot training", "full motion", "simulator", "motion platform", "flight training", "cockpit trainer"])
def _(S):
    return [
        shell(poly([(3.5, 13), (3.5, 6.5), (9, 3), (20.5, 3), (20.5, 13)], closed=True, r=S.r * 0.6)),
        detail(seg(6.5, 8.5, 12, 8.5)),
        line(seg(6.5, 13, 3.5, 20.5)), line(seg(10, 13, 10, 20.5)), line(seg(14, 13, 14, 20.5)), line(seg(17.5, 13, 20.5, 20.5)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


