"""TypeIcon Core: infrastructure 002 (transit gates and stops, ports, airports, parking and fuel)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path

CAT = "infrastructure"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def cut(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def front(x, y, w, h, rx=1.0):
    """Small solid vehicle front (bus, car): a block with a windscreen cut out."""
    body = rect(x, y, w, h, rx)
    win = rect(x + 1, y + 1, w - 2, max(1.0, h * 0.35))
    return Part("dot", cut(body, win))


def ground(x1=2, x2=22, y=21):
    return line(seg(x1, y, x2, y))


def head(x, y, deg, n=3.5, spread=42):
    """Arrowhead arms for a stroke that ends at (x, y) heading `deg` (0 = right, 90 = down)."""
    a = polar(x, y, n, deg + 180 - spread)
    b = polar(x, y, n, deg + 180 + spread)
    return poly([a, (x, y), b])


def circle_ring(x, y, r):
    return line(circle(x, y, r))


def wave(x0, y, n, w=5.0, h=2.5):
    """Smooth wave across n half periods."""
    d = f"M{fmt(x0)} {fmt(y)}"
    up = True
    for _ in range(n):
        d += f"q{fmt(w / 2)} {fmt(-h if up else h)} {fmt(w)} 0"
        up = not up
    return d


def plane(cx, cy, k=1.0, deg=0.0, knock=False):
    """Solid top-view aeroplane silhouette (nose to the right at deg 0)."""
    half = [(4, 0), (1, -1.2), (-1.5, -4.5), (-2.8, -4.5), (-1.2, -1.2), (-3.2, -1.2), (-3.8, -2.4), (-4.6, -2.4), (-3.8, 0)]
    pts = half + [(x, -y) for x, y in reversed(half[1:-1])]
    a = math.radians(deg)
    out = []
    for x, y in pts:
        out.append((cx + k * (x * math.cos(a) - y * math.sin(a)), cy + k * (x * math.sin(a) + y * math.cos(a))))
    d = poly(out, closed=True)
    return Part("dot", d) if knock else solid(d)


def car_mini(x, yb, w=6.0):
    """Tiny side-view car sitting on y=yb (solid silhouette)."""
    body = rect(x, yb - 2.6, w, 2.6, 0.9)
    roof = rect(x + w * 0.22, yb - 4.2, w * 0.56, 2, 0.8)
    return Part("dot", path_to_d(U(P(body), P(roof))))


def p_d(x, y, h=10, w=6):
    """Path of a letter P: stem and bowl; (x, y) is the top of the stem."""
    b = h * 0.55
    r = b / 2
    return f"M{fmt(x)} {fmt(y + h)}V{fmt(y)}H{fmt(x + w - r)}a{fmt(r)} {fmt(r)} 0 0 1 0 {fmt(b)}H{fmt(x)}"


def letter_p(x, y, h=10, w=6):
    return line(p_d(x, y, h, w))


def p_solid(x, y, h=6, w=4, sw=1.6):
    """Small solid letter P (outer box about (w + sw) x (h + sw))."""
    return Part("dot", path_to_d(ST(p_d(x, y, h, w), sw)))


# ============================================================================ transit gates, vehicles, stops

@icon("departure-board", CAT, "Information board on a post with rows of times and destinations",
      tags=["timetable", "schedule", "arrivals", "flights", "trains", "display", "airport"])
def _(S):
    return [
        shell(rect(3, 3, 18, 12, S.R)),
        detail(seg(6, 7, 8, 7)), detail(seg(11, 7, 18, 7)),
        detail(seg(6, 11, 8, 11)), detail(seg(11, 11, 18, 11)),
        line(seg(12, 15, 12, 21)), line(seg(8, 21, 16, 21)),
    ]


@icon("ticket-machine", CAT, "Freestanding ticket kiosk with a screen, keypad dots and a ticket slot",
      tags=["kiosk", "vending", "fare", "transit", "buy ticket", "station"])
def _(S):
    return [
        shell(rect(5, 3, 14, 18, S.R)),
        sq(8, 6, 8, 4, 0.5),
        dot(8.75, 13.5, 1), dot(12, 13.5, 1), dot(15.25, 13.5, 1),
        sq(8, 16.5, 8, 2),
    ]


@icon("turnstile", CAT, "Post with three metal arms fanning out like a tripod gate",
      tags=["gate", "entry", "access control", "barrier", "subway", "stadium", "tripod"])
def _(S):
    return [
        shell(rect(3, 3, 5, 18, min(S.R, 2))),
        line(seg(8, 8, 21, 4)),
        line(seg(8, 10, 21, 14)),
        line(seg(8, 11, 14, 20)),
    ]


@icon("fare-gate", CAT, "Two narrow cabinets with paddle doors between them",
      tags=["ticket gate", "barrier", "station", "entry", "access control", "transit", "paddle"])
def _(S):
    return [
        shell(rect(2, 7, 6, 14, min(S.R, 2))), shell(rect(16, 7, 6, 14, min(S.R, 2))),
        dot(5, 11, 1), dot(19, 11, 1),
        line(seg(8, 14, 11, 14)), line(seg(13, 14, 16, 14)),
    ]


@icon("ticket-validator", CAT, "Small box on a pole with a card reader and a ticket slot",
      tags=["validate", "tap", "stamp", "punch", "bus", "transit", "card reader"])
def _(S):
    return [
        shell(rect(5, 2, 14, 12, S.R)),
        dot(12, 6, 1.25),
        detail(seg(8, 10, 16, 10)),
        line(seg(12, 14, 12, 21)), line(seg(8, 21, 16, 21)),
    ]


@icon("transit-card", CAT, "Plastic fare card with a contactless wave symbol and a small bus",
      tags=["smart card", "fare card", "contactless", "tap", "public transport", "pass"])
def _(S):
    return [
        shell(rect(2, 5, 20, 14, S.R)),
        detail(arc(6.5, 12, 2.5, -50, 50)), detail(arc(6.5, 12, 5.5, -50, 50)),
        front(14, 9, 5, 6, 1),
    ]


@icon("metro-entrance", CAT, "Stairway leading down into the ground beside a round station sign",
      tags=["subway", "underground", "station", "stairs down", "tube", "entrance", "sign"])
def _(S):
    return [
        line(poly([(2, 10), (6, 10), (6, 14), (10, 14), (10, 18), (14, 18), (14, 21), (22, 21)], r=S.r)),
        shell(circle(18, 6, 3.5)),
        line(seg(18, 9.5, 18, 21)),
    ]


@icon("transit-map", CAT, "Three lines crossing with round station dots and one interchange circle",
      tags=["metro map", "subway map", "network", "route map", "lines", "stations", "diagram"])
def _(S):
    def st(x, y):
        return dot(x, y, 2) if S.name == "rounded" else sq(x - 1.75, y - 1.75, 3.5, 3.5)
    k = 3 / math.hypot(6, 10)
    dx, dy = 6 * k, 10 * k
    return [
        line(circle(12, 12, 3)),
        line(poly([(4, 18), (9, 18), (12 - dx, 12 + dy)], r=0)),
        line(poly([(12 + dx, 12 - dy), (15, 6), (20, 6)], r=0)),
        line(poly([(4, 6), (9, 6), (12 - dx, 12 - dy)], r=0)),
        line(poly([(12 + dx, 12 + dy), (15, 18), (20, 18)], r=0)),
        st(4, 18), st(20, 6), st(4, 6), st(20, 18),
    ]


@icon("transfer-station", CAT, "Two station dots inside a pill, the interchange symbol on a transit map",
      tags=["interchange", "connection", "change trains", "transfer", "hub", "metro", "link"])
def _(S):
    return [
        shell(rect(2, 7, 20, 10, L(S, 4, 5))),
        dot(7, 12, 2), dot(17, 12, 2),
    ]


@icon("stop-request-button", CAT, "Round push button mounted on a vertical grab pole",
      tags=["bus stop button", "request stop", "bell", "push button", "public transport", "hold"])
def _(S):
    return [
        line(seg(6, 2, 6, 22)),
        line(seg(6, 12, 9, 12)),
        shell(circle(15, 12, 6)),
        sq(12, 11, 6, 2, L(S, 0, 1)),
    ]


@icon("grab-handle", CAT, "Triangular hand strap hanging from a rail inside a bus or train",
      tags=["strap", "hand hold", "standing", "commuter", "rail", "handle", "subway"])
def _(S):
    return [
        line(seg(2, 3, 22, 3)),
        line(seg(8, 3, 8, 9)), line(seg(16, 3, 16, 9)),
        shell(poly([(5.5, 9), (18.5, 9), (12, 21)], closed=True, r=S.r)),
    ]


@icon("priority-seat", CAT, "Seat with a standing figure who uses a walking cane beside it",
      tags=["reserved seat", "elderly", "disabled", "accessible", "cane", "courtesy seat", "transit"])
def _(S):
    return [
        line(poly([(4, 3), (4, 13), (10, 13)], r=S.r)),
        line(seg(8, 13, 8, 21)),
        dot(17, 4.5, 2),
        line(poly([(17, 8.5), (16, 14), (16, 21)], r=S.r)),
        line(poly([(17, 10.5), (20, 12), (20, 21)], r=S.r)),
    ]


@icon("tram-stop", CAT, "Short pole with a round tram sign above a raised platform",
      tags=["tram", "streetcar", "light rail", "platform", "halt", "sign"])
def _(S):
    return [
        shell(circle(12, 8, 6)),
        sq(9.5, 7, 5, 4, 1),
        line(seg(12, 14, 12, 18)),
        shell(rect(2, 18, 20, 3, 0)),
    ]


@icon("bus-stop-pole", CAT, "Tall pole with a round bus flag and a timetable panel below it",
      tags=["flag", "sign post", "bus", "timetable", "route sign", "pickup", "transit"])
def _(S):
    return [
        line(seg(7, 2, 7, 22)),
        line(seg(7, 6.5, 10, 6.5)),
        shell(circle(15, 6.5, 4.5)),
        sq(12.5, 5, 5, 3, 0.8),
        shell(rect(11, 13, 10, 7, min(S.R, 1.5))),
        detail(seg(13.5, 16.5, 18.5, 16.5)),
    ]


@icon("bus-station", CAT, "Wide canopy over three buses parked in bays",
      tags=["terminal", "coach station", "depot", "bays", "interchange", "transit hub"])
def _(S):
    return [
        shell(poly([(2, 10), (4, 3), (20, 3), (22, 10)], closed=True, r=S.r)),
        front(2.5, 13, 5, 7, 1), front(9.5, 13, 5, 7, 1), front(16.5, 13, 5, 7, 1),
    ]


@icon("bus-depot", CAT, "Large shed with three tall doors and a bus parked in the middle one",
      tags=["garage", "bus garage", "yard", "storage", "fleet", "transit", "shed"])
def _(S):
    return [
        shell(poly([(2, 21), (2, 8), (12, 3), (22, 8), (22, 21)], closed=True, r=S.r)),
        detail(seg(8, 11, 8, 21)), detail(seg(16, 11, 16, 21)), detail(seg(8, 11, 16, 11)),
        front(10, 14, 4, 7, 0.8),
    ]


@icon("taxi-rank", CAT, "Taxi sign on a post with cars lined up beside it",
      tags=["taxi stand", "cab rank", "cab stand", "queue", "pickup", "hail", "cars"])
def _(S):
    return [
        shell(rect(2, 2, 12, 9, min(S.R, 2))),
        sq(5, 4.5, 6, 2), sq(7, 6.5, 2, 2.5),
        line(seg(8, 11, 8, 21)),
        front(12.5, 14, 4.5, 7, 1), front(18, 14, 4, 7, 1),
    ]


@icon("bike-share-dock", CAT, "Bicycle locked into a docking post at a rental station",
      tags=["bike rental", "bike sharing", "docking station", "cycle hire", "bicycle", "city bike", "kiosk"])
def _(S):
    return [
        circle_ring(7, 15.5, 4.5),
        line(seg(7, 15.5, 11, 6)), line(seg(9.5, 5.5, 14, 5.5)),
        line(seg(11, 9, 18, 13)),
        shell(rect(18, 10, 4, 11, min(S.R, 2))),
        dot(20, 14, 0.9),    ]


@icon("bike-rack", CAT, "Two bent steel hoops set in the ground for locking bicycles",
      tags=["bicycle parking", "cycle stand", "bike stand", "hoop", "lock up", "cycling", "parking"])
def _(S):
    return [
        line(f"M4 21V11a2.5 2.5 0 0 1 5 0V21"), line(f"M15 21V11a2.5 2.5 0 0 1 5 0V21"),
        ground(2, 22),
    ]


@icon("bike-locker", CAT, "Tall cabinet with a sloped roof and a bicycle on its door",
      tags=["bike box", "cycle locker", "secure storage", "bicycle parking", "cabinet", "lockup", "cycling"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 9), (21, 5), (21, 21)], closed=True, r=S.r)),
        dot(8, 17, 1.5), dot(16, 17, 1.5),
        detail(poly([(8, 17), (11, 13), (16, 17)])),
    ]


@icon("scooter-parking", CAT, "Painted parking bay with a kick scooter standing inside",
      tags=["scooter bay", "e-scooter", "micromobility", "drop zone", "kick scooter", "rental", "parking"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, S.R)),
        dot(8, 17, 1.5), dot(16, 17, 1.5),
        detail(seg(8, 14, 16, 14)), detail(seg(16, 14, 15, 8)), detail(seg(13, 8, 17, 8)),
    ]


@icon("park-and-ride", CAT, "Car and bus side by side with a curved arrow from the car to the bus",
      tags=["p+r", "commuter parking", "transfer", "car park", "public transport", "interchange", "suburban"])
def _(S):
    return [
        front(2.5, 14, 6.5, 6.5, 1.2), front(14.5, 11, 7, 9.5, 1.2),
        line("M5.5 11Q8 4 15 5.5"),
        line(head(17, 6, 12)),
    ]


@icon("ferry-terminal", CAT, "Terminal building on a pier with a ferry docked alongside",
      tags=["ferry port", "boat dock", "ferry landing", "harbour", "ferry building", "embarkation", "waterfront"])
def _(S):
    return [
        shell(poly([(2, 20), (2, 10), (5.5, 6), (9, 10), (9, 20)], closed=True, r=S.r)),
        sq(4, 14, 3, 6),
        shell(poly([(11, 15), (22, 15), (20, 20), (13, 20)], closed=True, r=S.r)),
        shell(rect(13.5, 9, 6, 6, 0)),
    ]


@icon("gangway", CAT, "Sloping walkway with a handrail from a quay up to a ship's side door",
      tags=["gangplank", "boarding ramp", "ship access", "walkway", "embark", "cruise", "quayside"])
def _(S):
    return [
        shell(rect(2, 16, 6, 5, 0)),
        line(seg(8, 16, 15, 11)),
        line(seg(8, 11, 15, 6)),
        line(seg(8, 11, 8, 16)),
        shell(rect(15, 3, 7, 18, min(S.R, 2))),
        sq(17.5, 9, 2, 4),
    ]


@icon("cruise-terminal", CAT, "Long low terminal building in front of a large cruise ship",
      tags=["cruise port", "passenger terminal", "ocean liner", "ship dock", "harbour", "embarkation", "port"])
def _(S):
    return [
        shell(poly([(3, 14), (6, 14), (6, 9), (9, 9), (9, 4), (15, 4), (15, 9), (18, 9), (18, 14), (21, 14), (18, 19), (6, 19)],
                   closed=True, r=S.r)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("pier", CAT, "Long wooden deck on stilts stretching out over wavy water",
      tags=["boardwalk", "seaside", "dock", "wharf", "waterfront", "promenade", "stilts"])
def _(S):
    return [
        line(seg(2, 8, 22, 8)),
        line(seg(5, 8, 5, 16)), line(seg(12, 8, 12, 16)), line(seg(19, 8, 19, 16)),
        line(wave(2, 19, 4)),
    ]


@icon("jetty", CAT, "Short narrow walkway on posts with a small sailboat tied at the end",
      tags=["landing stage", "mooring", "small boat", "lake dock", "boardwalk", "marina", "moored"])
def _(S):
    return [
        line(seg(2, 9, 13, 9)),
        line(seg(4, 9, 4, 20)), line(seg(10, 9, 10, 20)),
        shell(poly([(13, 16), (22, 16), (20, 20), (15, 20)], closed=True, r=S.r)),
        line(seg(17.5, 16, 17.5, 6)),
        shell(poly([(17.5, 6), (21, 13), (17.5, 13)], closed=True, r=S.r * 0.5)),
    ]


@icon("quay", CAT, "Straight stone harbour wall with a bollard on top beside a ship's hull",
      tags=["wharf", "harbour wall", "quayside", "waterfront", "dock", "embankment", "mooring"])
def _(S):
    return [
        shell(rect(2, 11, 9, 10, 0)),
        detail(seg(2, 16, 11, 16)),
        sq(5, 7, 3, 4),
        shell(poly([(14, 10), (22, 10), (21, 17), (18, 21), (14, 21)], closed=True, r=S.r)),
    ]


@icon("mooring-bollard", CAT, "Short thick iron post with a flared cap and a rope wound around it",
      tags=["bollard", "dock post", "tie up", "rope", "harbour", "ship", "moor"])
def _(S):
    return [
        shell(poly([(8, 21), (8, 11), (6, 11), (6, 5), (18, 5), (18, 11), (16, 11), (16, 21)], closed=True, r=S.r)),
        detail(seg(8, 14, 16, 12)), detail(seg(8, 19, 16, 17)),
    ]


@icon("mooring-cleat", CAT, "Horn-shaped metal cleat on a short pedestal bolted to a deck",
      tags=["cleat", "boat cleat", "dock cleat", "tie off", "horn cleat", "marina", "deck hardware"])
def _(S):
    return [
        shell(poly([(2, 7), (5, 7), (8, 10), (16, 10), (19, 7), (22, 7), (20, 12.5), (16, 13), (8, 13), (4, 12.5)],
                   closed=True, r=S.r * 0.5)),
        shell(rect(9.5, 13, 5, 5, 0)),
        line(seg(2, 20.5, 22, 20.5)),
    ]


@icon("lock-gate", CAT, "Pair of canal lock gates meeting in a point with balance beams behind them",
      tags=["canal", "waterway", "navigation lock", "sluice", "barge", "boat lift", "inland water"])
def _(S):
    return [
        line(poly([(6, 3), (6, 15)], r=0)), line(poly([(18, 3), (18, 15)], r=0)),
        line(poly([(6, 15), (12, 9), (18, 15)], r=S.r)),
        line(seg(6, 15, 2.5, 21)), line(seg(18, 15, 21.5, 21)),
    ]


@icon("weir", CAT, "Low wall across a river with water pouring over it in a smooth curve",
      tags=["dam", "river", "waterfall", "spillway", "overflow", "water level", "barrage"])
def _(S):
    return [
        line(seg(2, 7, 7, 7)),
        shell(rect(7, 7, 4, 14, 0)),
        line("M11 7H12Q15 7 15 11V16"),
        line(wave(13, 19, 2, 4.5, 2)),
    ]


@icon("slipway", CAT, "Concrete ramp sloping into the water with a small boat at the top",
      tags=["boat ramp", "launch", "boat launch", "trailer", "harbour", "marina", "shipyard"])
def _(S):
    return [
        shell(poly([(2, 21), (2, 11), (9, 11), (22, 19), (22, 21)], closed=True, r=S.r)),
        shell(poly([(2, 4), (10, 4), (9, 8), (3, 8)], closed=True, r=S.r)),
        line(wave(14, 13, 3, 2.7, 1.3)),
    ]


@icon("dry-dock", CAT, "Ship resting on blocks inside an empty dock basin",
      tags=["graving dock", "shipyard", "ship repair", "maintenance", "basin", "hull", "drained"])
def _(S):
    return [
        line(poly([(2, 5), (2, 20), (22, 20), (22, 5)], r=0)),
        shell(poly([(5, 8), (19, 8), (16, 14), (8, 14)], closed=True, r=S.r)),
        line(seg(10, 14, 10, 20)), line(seg(14, 14, 14, 20)),
        line(seg(12, 8, 12, 3)),
    ]


@icon("container-crane", CAT, "Tall gantry crane on legs with a long boom and a hanging container",
      tags=["gantry crane", "port crane", "ship to shore", "harbour", "cargo", "docks", "freight"])
def _(S):
    return [
        line(seg(4, 5, 4, 21)), line(seg(9, 5, 9, 21)),
        line(seg(2, 5, 22, 5)),
        line(seg(17.5, 5, 17.5, 9)),
        shell(rect(14.5, 9, 6, 5, 0)),
        shell(poly([(12, 16), (22, 16), (20, 21), (14, 21)], closed=True, r=S.r * 0.5)),
        line(seg(4, 13, 9, 13)),
    ]


@icon("container-stack", CAT, "Shipping containers stacked in a pyramid of three rows",
      tags=["cargo", "freight", "shipping", "intermodal", "port", "yard", "boxes"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 16), (6, 16), (6, 11), (9, 11), (9, 6), (15, 6), (15, 11), (18, 11), (18, 16), (21, 16), (21, 21)],
                   closed=True, r=S.r * 0.5)),
        detail(seg(6, 16, 18, 16)), detail(seg(9, 11, 15, 11)),
        detail(seg(9, 16, 9, 21)), detail(seg(15, 16, 15, 21)), detail(seg(12, 11, 12, 16)),
    ]


@icon("port-terminal", CAT, "Quayside gantry crane and a container stack beside a ship",
      tags=["container port", "harbour", "docks", "cargo terminal", "shipping", "freight", "wharf"])
def _(S):
    return [
        line(seg(5, 5, 5, 20)), line(seg(2, 5, 21, 5)),
        line(seg(2, 20, 9, 20)),
        shell(poly([(10, 15), (22, 15), (20, 20), (12, 20)], closed=True, r=S.r)),
        sq(12, 10, 4, 5), sq(17, 10, 4, 5),
    ]


@icon("runway", CAT, "Top view of a runway with a dashed centre line and threshold stripes",
      tags=["airstrip", "landing strip", "airport", "tarmac", "takeoff", "landing", "aerodrome"])
def _(S):
    return [
        shell(poly([(9, 3), (15, 3), (21, 21), (3, 21)], closed=True, r=S.r)),
        detail(seg(12, 6, 12, 8)), detail(seg(12, 11, 12, 14)), detail(seg(12, 17, 12, 21)),
    ]


@icon("taxiway-sign", CAT, "Low airfield sign with a letter and an arrow in a box",
      tags=["airport sign", "apron", "guidance", "taxi", "aerodrome", "signage", "directions"])
def _(S):
    return [
        shell(rect(2, 4, 20, 12, min(S.R, 2))),
        detail(poly([(5, 13), (7.5, 7), (10, 13)], r=0)), detail(seg(6, 11.5, 9, 11.5)),
        detail(seg(13, 10, 19, 10)), detail(head(19, 10, 0, 2.5)),
        line(seg(6, 16, 6, 21)), line(seg(18, 16, 18, 21)),
    ]


@icon("helipad", CAT, "Top view of a circular landing pad marked with a large letter H",
      tags=["heliport", "helicopter landing", "rooftop", "landing pad", "rescue", "air ambulance", "h"])
def _(S):
    r = L(S, 9, 9.5)
    return [
        shell(circle(12, 12, r)),
        detail(seg(9, 7.5, 9, 16.5)), detail(seg(15, 7.5, 15, 16.5)), detail(seg(9, 12, 15, 12)),
    ]


@icon("hangar", CAT, "Curved-roof building with a wide open door and an aeroplane tail inside",
      tags=["aircraft shed", "airport", "plane storage", "maintenance", "airfield", "aviation", "garage"])
def _(S):
    return [
        shell("M2 21V12Q2 4 12 4Q22 4 22 12V21Z" if S.name == "line"
              else "M2 19Q2 21 4 21H20Q22 21 22 19V12Q22 4 12 4Q2 4 2 12Z"),
        plane(12, 14, 1.15, -90, knock=True),
    ]


@icon("jet-bridge", CAT, "Enclosed telescopic walkway from a terminal wall to an aeroplane door",
      tags=["boarding bridge", "air bridge", "passenger bridge", "airport", "gate", "boarding", "terminal"])
def _(S):
    return [
        shell(rect(2, 3, 4, 18, 0)),
        shell(rect(6, 8, 7.5, 3.5, 0)),
        plane(16, 13, 1.25, -90),
    ]


@icon("air-stairs", CAT, "Wheeled staircase on a small vehicle with steps up to an aircraft door",
      tags=["boarding stairs", "passenger steps", "airstair", "mobile steps", "apron", "plane", "airport"])
def _(S):
    return [
        shell(poly([(2, 18), (2, 15), (6, 15), (6, 12), (10, 12), (10, 9), (14, 9), (14, 18)], closed=True, r=S.r * 0.5)),
        dot(5, 19.5, 1.75), dot(11.5, 19.5, 1.75),
        shell(rect(16, 3, 6, 15, min(S.R, 2.5))),
        sq(18, 9, 2, 4),
    ]


@icon("baggage-carousel", CAT, "Oval conveyor belt loop with two suitcases riding on it",
      tags=["baggage claim", "luggage belt", "conveyor", "arrivals", "airport", "bags", "reclaim"])
def _(S):
    return [
        shell(rect(2, 10, 20, 11, L(S, 4, 5.5))),
        detail(rect(7, 13.5, 10, 4, 2)),
        solid(rect(4, 4, 6, 6, 1)), solid(rect(14, 5, 6, 5, 1)),
    ]


@icon("baggage-scanner", CAT, "X-ray machine with a conveyor belt and a suitcase entering the tunnel",
      tags=["x-ray", "security check", "airport security", "screening", "luggage scan", "checkpoint", "inspection"])
def _(S):
    return [
        shell(rect(10, 3, 12, 15, min(S.R, 2))),
        sq(10, 8, 4, 7),
        line(seg(2, 16, 10, 16)),
        shell(rect(2, 9, 6, 7, 1)),
        line(seg(12, 18, 12, 21)), line(seg(20, 18, 20, 21)),
    ]


@icon("security-tray", CAT, "Shallow tray holding a phone, keys and a belt",
      tags=["airport security", "screening", "bin", "checkpoint", "belongings", "x-ray tray", "luggage check"])
def _(S):
    return [
        shell(poly([(2, 8), (22, 8), (20, 20), (4, 20)], closed=True, r=S.r)),
        sq(6, 11, 4, 6, 1),
        dot(14, 12.5, 1.6),
        detail(seg(14, 14, 14, 17)),
        detail(poly([(17, 15), (20, 15)], r=0)),
    ]


@icon("walk-through-scanner", CAT, "Rectangular metal detector frame with a person walking through it",
      tags=["metal detector", "security gate", "airport security", "screening", "checkpoint", "arch", "body scan"])
def _(S):
    return [
        shell(poly([(2, 21), (2, 2), (22, 2), (22, 21), (19, 21), (19, 5), (5, 5), (5, 21)], closed=True, r=S.r * 0.5)),
        dot(12, 9, 1.75),
        line(seg(12, 12, 12, 17)), line(seg(9.5, 13.5, 14.5, 13.5)),
        line(poly([(10, 21), (12, 17), (14, 21)], r=0)),
    ]


def _passport_filled():
    box = rect(3, 2, 13, 18, 2.5)
    body = U(P(box), ST(box, 2.0))
    body = D(body, P(circle(17, 16, 6.5)), P(circle(9.5, 8, 2.5)), ST(seg(6.5, 14, 12.5, 14), 2.0))
    return U(body, ST(circle(17, 16, 4.5), 2.5), ST(poly([(15, 16), (16.5, 18), (19.5, 14)]), 2.5))


@icon("passport-control", CAT, "Booth with a window and a passport and stamp at the counter",
      tags=["immigration", "border control", "border", "checkpoint", "visa", "arrivals", "officer booth"],
      filled=_passport_filled)
def _(S):
    return [
        shell(rect(3, 2, 13, 18, min(S.R, 2.5))),
        dot(9.5, 8, 2.5), detail(seg(6.5, 14, 12.5, 14)),
        line(circle(17, 16, 4.5)),
        line(poly([(15, 16), (16.5, 18), (19.5, 14)], r=0)),
    ]


@icon("customs-inspection", CAT, "Open suitcase on a counter with a magnifying glass over it",
      tags=["customs check", "baggage search", "border", "declaration", "luggage inspection", "airport", "officer"])
def _(S):
    return [
        shell(rect(2, 12, 12, 8, min(S.R, 2))),
        line(poly([(4, 12), (6, 5), (12, 5), (14, 12)], r=S.r)),
        circle_ring(16.5, 13, 3.2),
        line(seg(18.9, 15.3, 21.5, 18)),
    ]


@icon("check-in-desk", CAT, "Airline counter with a screen on top and a suitcase on a scale beside it",
      tags=["airport", "check in", "baggage drop", "counter", "airline desk", "departures", "luggage scale"])
def _(S):
    return [
        shell(rect(2, 12, 12, 9, 0)),
        shell(rect(3, 3, 10, 6, 0)), line(seg(8, 9, 8, 12)),
        shell(rect(17, 10, 5, 8, 1)), line(seg(18, 7.5, 21, 7.5)),
        line(seg(15, 20, 22, 20)),
    ]


@icon("check-in-kiosk", CAT, "Self service kiosk with a tilted screen and a boarding pass coming out",
      tags=["self check-in", "airport", "boarding pass", "automated", "terminal", "departures", "print ticket"])
def _(S):
    return [
        shell(rect(3, 3, 12, 18, S.R)),
        Part("dot", poly([(6, 6), (12, 6), (12, 11), (6, 11)], closed=True)),
        shell(rect(16, 13, 6, 4, 0)),
        dot(9, 16, 1),
    ]


@icon("boarding-gate", CAT, "Gate sign with a letter and a number above a small podium desk",
      tags=["departure gate", "airport", "gate number", "terminal", "flight", "boarding", "desk"])
def _(S):
    return [
        shell(rect(2, 2, 20, 10, min(S.R, 2))),
        detail(poly([(6, 10), (8.5, 4), (11, 10)], r=0)), detail(seg(7, 8.5, 10, 8.5)),
        detail(seg(16, 4, 16, 10)), detail(seg(14.5, 5.5, 16, 4)),
        shell(poly([(5, 21), (6, 15), (18, 15), (19, 21)], closed=True, r=S.r * 0.5)),
    ]


@icon("luggage-trolley", CAT, "Flat wheeled airport cart with a tall push handle and a suitcase on it",
      tags=["baggage cart", "airport trolley", "luggage cart", "porter", "carry", "travel", "terminal"])
def _(S):
    return [
        line(seg(2, 3, 7, 3)), line(seg(5, 3, 6.5, 17)),
        line(seg(5.5, 17, 22, 17)),
        dot(9, 20, 1.6), dot(19, 20, 1.6),
        shell(rect(10, 7, 10, 10, min(S.R, 2))),
        detail(seg(10, 12, 20, 12)),
    ]


@icon("luggage-tag", CAT, "Luggage tag with a hole, written lines and a looped strap",
      tags=["baggage tag", "name tag", "suitcase label", "travel", "identification", "airport", "strap"])
def _(S):
    return [
        shell(poly([(9, 7), (21, 7), (21, 17), (9, 17), (4, 12)], closed=True, r=S.r)),
        dot(8.5, 12, 1.25),
        detail(seg(12.5, 10.5, 18, 10.5)), detail(seg(12.5, 13.5, 18, 13.5)),
        line("M6.5 12Q3 12 3 8.5Q3 5 6.5 5Q9 5 10 7"),
    ]


@icon("luggage-locker", CAT, "Grid of small locker doors each with a keyhole",
      tags=["left luggage", "storage lockers", "baggage storage", "station", "key", "coin locker", "safe storage"])
def _(S):
    return [
        shell(rect(2, 2, 20, 19, S.R)),
        detail(seg(12, 2, 12, 21)),
        detail(seg(2, 8.33, 22, 8.33)), detail(seg(2, 14.67, 22, 14.67)),
        dot(7, 5.3, 1), dot(17, 5.3, 1), dot(7, 11.5, 1), dot(17, 11.5, 1), dot(7, 17.8, 1), dot(17, 17.8, 1),
    ]


@icon("airport-radar", CAT, "Curved radar dish on a rotating mount on a short tower",
      tags=["air traffic control", "radar dish", "surveillance", "antenna", "tower", "aviation", "scanner"])
def _(S):
    return [
        shell("M4 7A9 9 0 0 0 13 16Z"),
        line(seg(8, 12, 16, 4)), dot(17, 3.5, 1.25),
        shell(poly([(10, 17), (16, 17), (18, 21), (8, 21)], closed=True, r=S.r * 0.5)),
    ]


@icon("approach-lights", CAT, "Row of lamps on poles shrinking toward the end of a runway",
      tags=["runway lights", "airfield lighting", "landing lights", "aviation", "night landing", "beacons", "airport"])
def _(S):
    return [
        dot(4, 6, 2), line(seg(4, 8, 4, 21)),
        dot(10, 9, 2), line(seg(10, 11, 10, 21)),
        dot(16, 12, 2), line(seg(16, 14, 16, 21)),
        dot(21, 15, 1.75), line(seg(21, 17, 21, 21)),
        ground(2, 22, 21),
    ]


@icon("flight-connection", CAT, "Two small aeroplanes joined by a curved row of dots",
      tags=["layover", "transfer", "connecting flight", "stopover", "route", "itinerary", "travel"])
def _(S):
    return [
        plane(6, 18, 0.95, -90), plane(18, 6, 0.95, 0),
        line(seg(5.6, 12, 5.8, 10)), line(seg(7, 7.6, 8.6, 6.4)), line(seg(10.6, 5.4, 12, 5.2)),
    ]


@icon("airstrip", CAT, "Short grass strip with a small propeller plane and a windsock beside it",
      tags=["airfield", "landing strip", "bush plane", "windsock", "light aircraft", "aerodrome", "runway"])
def _(S):
    return [
        plane(8, 13, 1.1, 0),
        line(seg(19, 5, 19, 21)),
        shell(poly([(19, 5), (19, 11), (12, 9.5), (12, 6.5)], closed=True, r=S.r * 0.5)),
        detail(seg(15.5, 5.8, 15.5, 10.2)),
        line(seg(2, 20, 15, 20)),
    ]


@icon("parking-garage", CAT, "Multi-storey car park with open floors and a car on each level",
      tags=["car park", "multi-storey", "parking structure", "parking deck", "parking lot", "ramp", "vehicles"])
def _(S):
    return [
        line(seg(2, 4, 22, 4)), line(seg(2, 11.5, 22, 11.5)), line(seg(2, 19, 22, 19)),
        line(seg(3.5, 4, 3.5, 19)), line(seg(20.5, 4, 20.5, 19)),
        car_mini(7, 10.5), car_mini(12, 18),
    ]


@icon("underground-parking", CAT, "Ramp sloping down into the ground with a parking sign above it",
      tags=["basement parking", "car park", "subterranean", "garage entrance", "ramp", "below ground", "parking"])
def _(S):
    return [
        shell(rect(7, 2, 10, 9, min(S.R, 2))),
        p_solid(10.5, 4.3, 3.4, 2.4, 1.5),
        shell(rect(2, 13, 20, 8, min(S.R, 2))),
        detail(seg(12, 15.5, 12, 18.5)), detail(head(12, 19.2, 90, 2.5)),
    ]


@icon("parking-ticket", CAT, "Paper ticket with a parking symbol, a barcode and a torn edge",
      tags=["parking receipt", "pay and display", "stub", "barcode", "car park", "fee", "slip"])
def _(S):
    return [
        shell(poly([(5, 2), (19, 2), (19, 21), (16, 18.5), (12, 21), (8, 18.5), (5, 21)], closed=True, r=S.r * 0.5)),
        p_solid(9, 5, 4, 2.6, 1.6),
        sq(8, 13, 1.5, 3), sq(10.75, 13, 1.5, 3), sq(13.5, 13, 1.5, 3),
    ]


@icon("parking-barrier", CAT, "Striped barrier arm across a lane beside a ticket post",
      tags=["boom gate", "car park gate", "entry barrier", "toll gate", "access", "arm", "gate"])
def _(S):
    return [
        shell(rect(2, 6, 6, 15, min(S.R, 2))),
        sq(4, 9, 2, 3),
        shell(rect(8, 9, 14, 4, 0)),
        detail(seg(12, 9, 14, 13)), detail(seg(16, 9, 18, 13)),
        ground(8, 22, 21),
    ]


@icon("parking-disc", CAT, "Square card with a round clock dial window and a parking symbol in the corner",
      tags=["parking clock", "time limit", "blue zone", "arrival time", "dashboard card", "timer", "car park"])
def _(S):
    return [
        shell(rect(2, 2, 20, 20, S.R)),
        p_solid(5, 5, 4, 2.6, 1.5),
        detail(circle(14, 14, 5)),
        detail(seg(14, 14, 14, 11.5)), detail(seg(14, 14, 16.5, 14)),
    ]


@icon("parking-permit", CAT, "Hanging card with a hook at the top and a parking symbol on the front",
      tags=["parking pass", "resident permit", "mirror hanger", "badge", "licence", "access card", "windshield"])
def _(S):
    return [
        line(poly([(7.5, 7), (12, 2.5), (16.5, 7)], r=S.r)),
        shell(rect(4, 7, 16, 14, S.R)),
        Part("detail", p_d(9.5, 10.5, 5, 4.5)),
    ]


@icon("wheel-clamp", CAT, "Car wheel with a heavy clamp locked across it",
      tags=["wheel boot", "denver boot", "immobiliser", "parking enforcement", "locked wheel", "fine", "car"])
def _(S):
    return [
        line(circle(10, 13, 8)),
        line(circle(10, 13, L(S, 3.2, 3.6))),
        shell(rect(14.5, 2.5, 7.5, 8, min(S.R, 2))),
        dot(18.25, 6.5, 1.1),
    ]


@icon("valet-parking", CAT, "Car key hanging beside the front of a car",
      tags=["valet service", "key handover", "attendant", "hotel parking", "car keys", "chauffeur", "service"])
def _(S):
    return [
        line(circle(6.5, 6.5, 3)),
        line(seg(6.5, 9.5, 6.5, 20)),
        line(seg(6.5, 15, 10, 15)), line(seg(6.5, 18, 9, 18)),
        front(13, 11, 9, 9, 1.5),
        dot(15, 17, 1), dot(20, 17, 1),
    ]


@icon("loading-zone", CAT, "Delivery truck at the kerb with an arrow pointing down into its cargo box",
      tags=["delivery bay", "unloading", "freight", "kerbside", "curbside", "goods", "loading bay"])
def _(S):
    return [
        line(seg(9, 2, 9, 5.5)), line(head(9, 6.5, 90, 3)),
        shell(rect(3, 9, 11, 8, 0)),
        shell(poly([(14, 11), (18, 11), (21, 14), (21, 17), (14, 17)], closed=True, r=S.r * 0.5)),
        dot(7, 19, 1.6), dot(17.5, 19, 1.6),
        ground(2, 22, 21.5),
    ]


@icon("tow-away-zone-sign", CAT, "Sign showing a tow truck lifting the front of a car",
      tags=["towing", "no parking", "impound", "tow truck", "vehicle removal", "restriction", "street sign"])
def _(S):
    car = rect(8, 10, 11, 4.5, 1.3)
    roof = rect(10.5, 7, 6.5, 3.5, 1)
    tilted = path_to_d(transform_path(U(P(car), P(roof)), rotation(-18, 13.5, 12)))
    return [
        shell(rect(2, 2, 20, 15, min(S.R, 2))),
        Part("dot", tilted),
        detail(poly([(5, 15), (5, 8), (9, 7)], r=0)),
        line(seg(12, 17, 12, 21)),
    ]


@icon("ev-parking-space", CAT, "Top view of a parking bay with a charging plug painted inside",
      tags=["charging bay", "electric vehicle", "ev charging", "plug in", "reserved space", "charger", "car park"])
def _(S):
    return [
        line(poly([(3, 22), (3, 3), (21, 3), (21, 22)], r=S.r)),
        line(seg(10, 6, 10, 9)), line(seg(14, 6, 14, 9)),
        shell(rect(8, 9, 8, 5, L(S, 0, 1.5))),
        line(seg(12, 14, 12, 19)),
    ]


@icon("parking-sensor", CAT, "Rear bumper with round sensors and curved signal waves behind it",
      tags=["reversing sensor", "proximity", "backup sensor", "park assist", "obstacle detection", "ultrasonic", "car"])
def _(S):
    return [
        shell(rect(3, 2, 18, 7, S.R)),
        dot(7, 5.5, 1.2), dot(12, 5.5, 1.2), dot(17, 5.5, 1.2),
        line(arc(12, 6, 7, 55, 125)), line(arc(12, 6, 12, 60, 120)),
    ]


@icon("parking-space-counter", CAT, "Roadside display board with a parking symbol and a count of free spaces",
      tags=["free spaces", "availability", "car park sign", "capacity", "occupancy", "smart parking", "vacancies"])
def _(S):
    return [
        shell(rect(2, 2, 20, 14, min(S.R, 2))),
        Part("detail", p_d(5, 5, 5, 3.5)),
        detail(rect(13.5, 6, 4.5, 4, 0)),
        line(seg(12, 16, 12, 21)), line(seg(8, 21, 16, 21)),
    ]


@icon("motorcycle-parking", CAT, "Painted parking bay with a motorcycle standing inside it",
      tags=["motorbike bay", "moped", "two-wheeler", "scooter parking", "bike space", "reserved", "car park"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, S.R)),
        dot(8, 16.5, 2), dot(16.5, 16.5, 2),
        Part("dot", poly([(9, 14), (10, 10), (15.5, 10), (16, 14)], closed=True)),
        detail(seg(15, 10, 14, 7)), detail(seg(12, 7, 15.5, 7)),
    ]


@icon("fuel-nozzle", CAT, "Fuel pump nozzle with a trigger grip and a curved hose",
      tags=["petrol", "gas pump", "refuel", "filling", "diesel", "gasoline", "pump handle"])
def _(S):
    return [
        shell(poly([(6, 5), (16, 5), (16, 9), (14, 9), (12, 19), (8, 19), (9, 9), (6, 9)], closed=True, r=S.r)),
        line(seg(16, 7, 21.5, 3.5)),
        line("M6 7Q2 7 2 11V21"),
    ]


@icon("fuel-price-sign", CAT, "Tall roadside pylon sign with three rows of price digits",
      tags=["gas prices", "petrol prices", "pylon", "forecourt", "fuel cost", "station sign", "pricing"])
def _(S):
    rows = []
    for y in (6, 10.5, 15):
        rows += [detail(seg(6.5, y, 10, y)), dot(12, y + 0.8, 0.8), detail(seg(14, y, 17.5, y))]
    return [
        shell(rect(3, 2, 18, 19, min(S.R, 2))),
        *rows,
    ]


@icon("jerrycan", CAT, "Rectangular fuel can with an X on its side, a cap and a carrying handle",
      tags=["petrol can", "gas can", "fuel container", "spare fuel", "gasoline", "jerry can", "emergency fuel"])
def _(S):
    return [
        shell(rect(3, 7, 16, 14, min(S.R, 2))),
        line(poly([(6, 7), (6, 3), (13, 3), (13, 7)], r=S.r)),
        sq(16, 3, 3, 4, 0),
        detail(seg(7, 11, 15, 18)), detail(seg(15, 11, 7, 18)),
    ]


@icon("air-pump-station", CAT, "Tyre inflation post with a coiled air hose and a pressure gauge",
      tags=["tire inflator", "tyre pressure", "air compressor", "inflate", "forecourt", "psi", "garage"])
def _(S):
    return [
        shell(rect(3, 3, 12, 18, S.R)),
        detail(circle(9, 8, 2.5)), dot(9, 8, 0.8),
        detail(seg(6, 14, 12, 14)),
        line(poly([(15, 9), (20, 10.5), (15, 12.5), (20, 14.5), (15, 16.5), (20, 18.5)], r=S.r * 0.6), stroke_miterlimit="1.2"),
    ]


@icon("hydrogen-station", CAT, "Fuel pump with a large H and a small 2 on its front and a hose",
      tags=["h2", "hydrogen fuel", "fuel cell", "refuelling", "clean energy", "alternative fuel", "pump"])
def _(S):
    return [
        shell(rect(2, 2, 13, 19, S.R)),
        Part("detail", "M5.5 6V13"), Part("detail", "M9.5 6V13"), Part("detail", "M5.5 9.5H9.5"),
        Part("dot", path_to_d(ST("M11 13.5Q11 12 12.3 12Q13.6 12 13.6 13.2Q13.6 14 11 16.5H13.8", 1.1))),
        line("M15 11H18Q20 11 20 14V19"),
    ]
