"""TypeIcon Core: signage (batch 003): transport services, outdoor access, snow sports, water hazards and ride rules.

Scenes are reduced to a few strong shapes: vehicles are rounded boxes with solid wheels, people are a solid
head over 2 px limbs, dogs are one filleted silhouette with four leg strokes.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "signage"


def L(S, a, b):
    return a if S.name == "line" else b


def rr(S, cap):
    return min(S.R, cap)


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled shell."""
    return Part("dot", d)


def pl(S, pts, closed=False, k=1.0):
    return poly(pts, closed=closed, r=S.r * k)


def plane_pts(cx, cy, k):
    """Small airplane silhouette pointing up (centre cx, cy; half-size k)."""
    half = [(0, -1), (0.2, -0.7), (0.2, -0.15), (1, 0.35), (1, 0.62), (0.2, 0.3), (0.2, 0.7), (0.5, 0.92), (0.5, 1.0), (0, 0.9)]
    right = [(cx + x * k, cy + y * k) for x, y in half]
    left = [(cx - x * k, cy + y * k) for x, y in half[1:-1]][::-1]
    return right + left


def plane(cx, cy, k):
    return solid(poly(plane_pts(cx, cy, k), closed=True))


def dog(S, ox, oy, k=1.0, flip=False, w=14.0):
    """Standing dog silhouette (local box about 14 x 12, nose at the left) plus four legs and a tail."""
    sil = [(0, 3.2), (2.2, 1.2), (2.6, -1.6), (4.6, 0.4), (11.5, 0.6), (12.5, 2.6), (12, 6.6), (4.8, 6.6),
           (3.8, 5.2), (2.4, 5.2), (0, 5.2)]

    def m(p):
        x, y = p
        if flip:
            x = w - x
        return (ox + k * x, oy + k * y)
    parts = [shell(poly([m(p) for p in sil], closed=True, r=S.r * 0.7)),
             line(poly([m((4.4, 6.6)), m((4.4, 10.8))])),
             line(poly([m((11.3, 6.6)), m((11.3, 10.8))])),
             line(poly([m((12.2, 2.0)), m((14.2, -0.6))]))]
    return parts, m


def bus_wheels(xs, y=19.2, r=1.9):
    return [dot(x, y, r) for x in xs]


# ============================================================================ chunk 1: transport services

@icon("oversize-baggage", CAT, "A tall golf bag standing beside a small suitcase for scale.",
      tags=["oversize luggage", "golf bag", "sports bag", "large baggage", "special baggage", "airport", "luggage desk"])
def _(S):
    return [
        shell(rect(3, 8.5, 6, 12.5, rr(S, 2))),
        line(seg(4.5, 8.5, 4.5, 3.5)), line(seg(7.5, 8.5, 7.5, 5)),
        detail(seg(3, 13.5, 9, 13.5)),
        shell(rect(13.5, 12.5, 8, 8.5, rr(S, 2))),
        line(poly([(15.5, 12.5), (15.5, 10), (19.5, 10), (19.5, 12.5)])),
    ]


@icon("lost-baggage", CAT, "A suitcase with a question mark on its front.",
      tags=["lost luggage", "missing bag", "baggage claim", "lost property", "airport", "suitcase", "question"])
def _(S):
    return [
        shell(rect(3, 6, 18, 15, rr(S, 3))),
        line(poly([(9, 6), (9, 3), (15, 3), (15, 6)])),
        detail("M9.9 11.2a2.2 2.2 0 1 1 3.7 1.6c-.9.7-1.6 1.1-1.6 2.3"),
        dot(12, 17.6, 1.2),
    ]


@icon("airport-shuttle", CAT, "A minibus in side view with a small airplane above its roof.",
      tags=["airport bus", "airport transfer", "shuttle bus", "minibus", "van", "hotel shuttle", "transfer"])
def _(S):
    return [
        plane(12, 5.3, 3.4),
        shell(rect(2.5, 11, 19, 6.5, rr(S, 2.5))),
        detail(seg(2.5, 14.5, 21.5, 14.5)),
        detail(seg(8.5, 11, 8.5, 14.5)), detail(seg(15.5, 11, 15.5, 14.5)),
    ] + bus_wheels([7, 17], 19.6, 1.9)


@icon("kiss-and-ride", CAT, "A car at the curb with a passenger walking away carrying a bag.",
      tags=["drop off", "passenger drop-off", "pick up", "curbside", "car", "station drop off", "quick stop"])
def _(S):
    return [
        shell(poly([(1.5, 17), (1.5, 13.5), (4, 13.5), (6, 9.5), (11, 9.5), (13, 13.5), (14, 13.5), (14, 17)], closed=True, r=S.r)),
        detail(seg(8.5, 10, 8.5, 13.5)),
        dot(5, 18.4, 1.9), dot(11, 18.4, 1.9),
        dot(18.5, 5.5, 2),
        line(pl(S, [(18.5, 8.5), (18.5, 14.5)])),
        line(poly([(18.5, 14.5), (16.8, 20)])), line(poly([(18.5, 14.5), (20.2, 20)])),
        line(pl(S, [(18.5, 10.5), (20.5, 13.5)])),
        solid(rect(20, 14, 2.5, 3.5, 0.6)),
    ]


@icon("pet-relief-area", CAT, "A dog standing beside a small fire hydrant on a patch of grass.",
      tags=["dog park", "dog toilet", "pet area", "airport pet", "dog walk", "hydrant", "pets"])
def _(S):
    parts, _ = dog(S, 2, 7.5, 1.0)
    return parts + [
        solid(rect(18.5, 11.5, 3.5, 8.5, 0.6)), solid(rect(17.5, 14, 5.5, 1.8, 0.6)),
        solid(circle(20.25, 11, 2)),
        line(seg(2, 21, 15, 21)),
    ]


@icon("rail-replacement-bus", CAT, "A bus in side view with a small train front on its side panel.",
      tags=["replacement bus", "train bus", "rail bus", "bus instead of train", "track works", "service change", "transit"])
def _(S):
    train = D(P(rect(8.5, 7.5, 7, 7.5, 2.2)), P(rect(10, 9, 4, 2.8, 0.6)))
    return [
        shell(rect(1.5, 4.5, 21, 13, rr(S, 3))),
        mark(path_to_d(train)),
    ] + bus_wheels([6.5, 17.5], 19.6, 1.9)


@icon("bicycle-carriage", CAT, "A train carriage in side view with a bicycle shown in its window.",
      tags=["bike carriage", "bike on train", "cycle car", "train bike space", "bicycle coach", "rail", "cycling"])
def _(S):
    return [
        shell(rect(1.5, 2.5, 21, 16, rr(S, 3))),
        dot(7, 13, 2.1), dot(17, 13, 2.1),
        detail(poly([(7, 13), (11.5, 13), (15.5, 8.5)])),
        detail(poly([(7, 13), (10, 8.5), (15.5, 8.5), (17, 13)])),
        detail(seg(14, 7.2, 16.5, 7.2)),
    ] + bus_wheels([7, 17], 20.4, 1.6)


def trolley_frame(S, dx, dy=0):
    return [
        line(pl(S, [(2 + dx, 4 + dy), (5 + dx, 4 + dy), (8 + dx, 15 + dy), (14 + dx, 15 + dy)], k=0.6)),
        dot(9 + dx, 18 + dy, 1.5),
    ]


@icon("trolley-return", CAT, "Two luggage trolleys nested in a row with a curved return arrow above.",
      tags=["cart return", "trolley bay", "return trolleys here", "luggage cart", "baggage cart", "airport trolley", "nested carts"])
def _(S):
    return (trolley_frame(S, 0, 3) + trolley_frame(S, 5, 3) + [
        line("M10 6.5h6a3 3 0 0 1 3 3"),
        line(pl(S, [(16.5, 8), (19, 9.8), (21.5, 8)])),
    ])


@icon("unaccompanied-minor", CAT, "A small child with a pouch on a lanyard around the neck and a backpack beside them.",
      tags=["child traveling alone", "kids travel alone", "young traveler", "escort", "airline child", "lanyard", "backpack"])
def _(S):
    return [
        dot(10.5, 5, 2.8),
        shell(rect(5.5, 9.5, 10, 11.5, rr(S, 3))),
        detail(poly([(8.2, 9.5), (10.5, 14.2), (12.8, 9.5)])),
        mark(rect(9, 14.8, 3, 4.2, 0.7)),
        shell(rect(18, 11, 4, 8, rr(S, 1.5))),
    ]


@icon("clear-stadium-bag", CAT, "A see-through tote bag with short handles and small items visible inside.",
      tags=["transparent bag", "clear bag policy", "stadium security", "see through tote", "event bag", "concert", "bag rules"])
def _(S):
    return [
        shell(rect(4, 9, 16, 12, rr(S, 3))),
        line("M8.5 9V7a3.5 3.5 0 0 1 7 0v2"),
        dot(9, 16.5, 1.6),
        mark(rect(12.5, 13, 2.2, 6, 0.5)), mark(rect(16, 15.5, 1.8, 3.5, 0.5)),
    ]


@icon("playbill", CAT, "A slim theater program booklet with two drama masks on the cover.",
      tags=["theater program", "theatre programme", "show booklet", "cast list", "drama masks", "stage", "playbill"])
def _(S):
    def maskd(cx, cy, smile):
        r = D(P(circle(cx, cy, 3.3)), P(circle(cx - 1.2, cy - 0.9, 0.6)), P(circle(cx + 1.2, cy - 0.9, 0.6)))
        mouth = arc(cx, cy + (0.1 if smile else 2.5), 1.6, 25, 155) if smile else arc(cx, cy + 2.5, 1.6, 205, 335)
        return path_to_d(D(r, ST(mouth, 0.9, "round", "round")))
    return [
        shell(rect(4.5, 2.5, 15, 19, rr(S, 2.5))),
        mark(maskd(10.2, 8.3, True)), mark(maskd(13.8, 15.3, False)),
    ]


@icon("apron-bus", CAT, "A low wide airport bus with several doors in front of an airplane tail fin.",
      tags=["airside bus", "ramp bus", "passenger bus", "airport apron", "tarmac bus", "boarding bus", "aircraft"])
def _(S):
    fin = poly([(10, 10.5), (14.5, 2.5), (19, 2.5), (18, 10.5)], closed=True, r=S.r * 0.6)
    return [
        solid(fin),
        shell(rect(1.5, 11.5, 21, 6, rr(S, 2.5))),
        detail(seg(7, 11.5, 7, 17.5)), detail(seg(12, 11.5, 12, 17.5)), detail(seg(17, 11.5, 17, 17.5)),
    ] + bus_wheels([6, 18], 19.8, 1.8)


@icon("detection-dog", CAT, "A harnessed dog sniffing at a suitcase.",
      tags=["sniffer dog", "k9", "security dog", "drug dog", "airport security", "customs", "search dog"])
def _(S):
    parts, m = dog(S, 1.5, 9.5, 0.95, flip=True, w=14)
    a, b = m((7.2, 0.6)), m((7.2, 6.6))
    return parts + [
        detail(seg(a[0], a[1], b[0], b[1])),
        shell(rect(16.5, 13.5, 5.5, 7, rr(S, 1.5))),
        line(poly([(18, 13.5), (18, 11.5), (20.5, 11.5), (20.5, 13.5)])),
    ]


@icon("night-bus", CAT, "A bus in side view with a crescent moon and a small star above its roof.",
      tags=["night service", "late bus", "overnight bus", "after dark", "moon", "owl bus", "night route"])
def _(S):
    moon = D(P(circle(7, 5.5, 3.3)), P(circle(8.6, 4.5, 2.7)))
    star = poly([(15, 2.5), (15.9, 4.6), (18, 5.5), (15.9, 6.4), (15, 8.5), (14.1, 6.4), (12, 5.5), (14.1, 4.6)], closed=True)
    return [
        solid(path_to_d(moon)), solid(star),
        shell(rect(2, 10.5, 20, 7, rr(S, 2.5))),
        detail(seg(2, 14, 22, 14)),
        detail(seg(8.5, 10.5, 8.5, 14)), detail(seg(15.5, 10.5, 15.5, 14)),
    ] + bus_wheels([7, 17], 19.8, 1.8)


@icon("amnesty-bin", CAT, "A lidded bin with an apple being dropped in from above.",
      tags=["food amnesty", "biosecurity bin", "quarantine bin", "declare food", "customs bin", "fruit disposal", "border"])
def _(S):
    return [
        dot(11, 6.4, 2.5),
        line(seg(12.2, 3.9, 14.4, 2.6)),
        shell(poly([(6.5, 11), (17.5, 11), (16.5, 21), (7.5, 21)], closed=True, r=S.r * 0.6)),
        line(seg(4.5, 11, 19.5, 11)),
        detail(seg(10, 15, 14, 15)),
    ]


# ============================================================================ chunk 2: crossings, trails, snow

def _tilt(pt, c, deg):
    a = math.radians(deg)
    x, y = pt[0] - c[0], pt[1] - c[1]
    return [(c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))]


def skier(S, hx, hy, k=1.0, pole=True, tilt=0.0):
    """Upright skier (head at hx, hy): body, legs, skis and an optional pole. Returns parts."""
    def p(x, y):
        return (hx + k * x, hy + k * y)
    parts = [
        dot(hx, hy, 2.2 * max(k, 0.75)),
        line(poly([p(0, 3.2), p(0, 9)])),
        line(pl(S, [p(0, 9), p(-2.6, 15.2)], k=0.7)),
        line(pl(S, [p(0, 9), p(2.6, 15.2)], k=0.7)),
        line(poly(_tilt(p(-5.2, 16.4), p(0, 16.4), tilt) + _tilt(p(5.4, 16.4), p(0, 16.4), tilt))),
        line(poly([p(0, 4.8), p(3.6, 7.6)])),
    ]
    if pole:
        parts.append(line(poly([p(3.6, 7.6), p(7, 16.4)])))
    return parts


@icon("bus-bike-rack", CAT, "The front of a bus with a bicycle carried on a folding rack below the windshield.",
      tags=["bike rack bus", "bicycle on bus", "bus bike carrier", "cycle rack", "bike and ride", "front rack", "transit"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 11.5, rr(S, 3))),
        detail(seg(3, 9, 21, 9)),
        mark(circle(7, 11.8, 0.9)), mark(circle(17, 11.8, 0.9)),
        line(circle(7, 18.6, 2.6)), line(circle(17, 18.6, 2.6)),
        line(poly([(7, 18.6), (10.5, 16), (14.5, 16), (17, 18.6)])),
        line(poly([(10.5, 16), (12, 18.6)])) if False else line(poly([(12, 18.6), (14.5, 16)])),
    ]


@icon("car-shuttle-train", CAT, "A flat rail wagon carrying a car in side view.",
      tags=["motorail", "car transport train", "auto train", "car carrier", "vehicle shuttle", "tunnel shuttle", "rail"])
def _(S):
    return [
        shell(poly([(4, 13), (4, 10.5), (7.5, 10.5), (9.5, 6.5), (14.5, 6.5), (17, 10.5), (20, 10.5), (20, 13)], closed=True, r=S.r)),
        dot(8, 13.8, 1.9), dot(16, 13.8, 1.9),
        line(seg(1.5, 17.5, 22.5, 17.5)),
        dot(6, 20.4, 1.6), dot(18, 20.4, 1.6),
    ]


@icon("cable-ferry", CAT, "A flat ferry deck on water with a mast tied to a cable strung between two river banks.",
      tags=["reaction ferry", "chain ferry", "river ferry", "cable crossing", "ferry on rope", "river crossing", "water"])
def _(S):
    return [
        solid(rect(2, 2.5, 2.2, 7)), solid(rect(19.8, 2.5, 2.2, 7)),
        line("M3.5 4.5Q12 9 20.5 4.5"),
        line(seg(12, 6.8, 12, 13.2)),
        shell(poly([(5.5, 13.5), (18.5, 13.5), (16.5, 17.5), (7.5, 17.5)], closed=True, r=S.r * 0.6)),
        line("M2.5 20.8c1.9-1.4 3.4-1.4 5.1 0s3.2 1.4 4.9 0 3.2-1.4 4.9 0 3.2 1.4 4.1.2"),
    ]


@icon("firefighter-lift", CAT, "An elevator with a closed door and a firefighter helmet above it.",
      tags=["fire service elevator", "fireman lift", "fire lift", "emergency elevator", "firefighters elevator", "helmet", "fire safety"])
def _(S):
    dome = D(P("M6.5 8.5C6.5 4 9 2.5 12 2.5S17.5 4 17.5 8.5Z"), P(rect(11.3, 2, 1.4, 7)))
    return [
        solid(path_to_d(dome)),
        line(seg(3.5, 9.2, 20.5, 9.2)),
        shell(rect(4, 12.5, 16, 8.5, rr(S, 2))),
        detail(seg(12, 12.5, 12, 21)),
    ]


@icon("emergency-door-release", CAT, "A pull lever on a wall plate beside a door with a downward arrow.",
      tags=["door release handle", "emergency exit lever", "pull handle", "manual release", "train door release", "exit", "safety"])
def _(S):
    return [
        shell(rect(3, 3, 10, 18, rr(S, 2.5))),
        dot(7.5, 8, 1.5),
        detail(seg(7.5, 8, 8.5, 16)),
        mark(rect(6.5, 15.5, 4, 2.5, 1)),
        line(seg(18, 4, 18, 18)),
        line(pl(S, [(15.3, 15.5), (18, 18.2), (20.7, 15.5)])),
    ]


@icon("bridleway-sign", CAT, "A rider on a horse in profile.",
      tags=["horse riding trail", "equestrian route", "bridle path", "horse rider", "riders only", "trail marker", "rider"])
def _(S):
    body = [(4, 11.5), (14, 11), (16.8, 7), (17.5, 5.5), (19, 6.5), (21.5, 9.5), (20.3, 10.8), (18.2, 9.8), (17.5, 12.5),
            (16.5, 15), (5, 15)]
    return [
        shell(poly(body, closed=True, r=S.r * 0.8)),
        line(seg(6, 15, 6, 20.5)), line(seg(8.8, 15, 8.8, 20.5)),
        line(seg(13.2, 15, 13.2, 20.5)), line(seg(16, 15, 16, 20.5)),
        line(poly([(4, 11.8), (2.3, 15.5)])),
        dot(10.5, 3.6, 1.9),
        line(poly([(10.5, 6.2), (10.5, 9.3)])),
        line(poly([(10.5, 7.2), (13.8, 9)])),
    ]


@icon("boot-cleaning-station", CAT, "A muddy boot pressed against upright brushes on a low tray with spray.",
      tags=["boot wash", "biosecurity", "shoe brush", "disinfectant", "farm hygiene", "clean boots", "foot dip"])
def _(S):
    boot = [(3.5, 3), (9.5, 3), (9.8, 7.5), (14.5, 8.8), (17.2, 10.5), (17.2, 13), (3.5, 13)]
    return [
        shell(poly(boot, closed=True, r=S.r)),
        detail(seg(3.5, 10.5, 17.2, 10.5)),
        line(seg(6, 15.5, 6, 19.5)), line(seg(10.5, 15.5, 10.5, 19.5)), line(seg(15, 15.5, 15, 19.5)),
        line(seg(3, 21, 18, 21)),
        dot(20.5, 5.5, 1.1), dot(20.5, 9.5, 1.1), dot(20.5, 13.5, 1.1),
    ]


@icon("ground-nesting-birds-sign", CAT, "A small bird sitting on a nest in the grass.",
      tags=["nesting birds", "keep dogs on leads", "wildlife protection", "nature reserve", "bird nest", "ground nest", "conservation"])
def _(S):
    return [
        shell(ellipse(11.5, 11.5, 6, 4.2)),
        dot(17.5, 6.5, 2.4),
        solid("M19.6 5.8L22 6.8L19.8 8Z"),
        line(poly([(5.5, 10), (2.5, 8)])),
        line("M3.5 14.5C4.5 19 8 20 12 20S19.5 19 20.5 14.5"),
        line(seg(2, 21.8, 22, 21.8)) if False else line(seg(5, 21.8, 19, 21.8)),
    ]


@icon("tide-table", CAT, "A board showing a wavy tide curve above a row of time columns with a rising and a falling arrow.",
      tags=["tide times", "high tide low tide", "tide chart", "tidal schedule", "beach board", "sea", "coast"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 18, rr(S, 2.5))),
        detail("M5.5 9c1.8-3.2 3.4-3.2 5 0s3.2 3.2 5 0 1.6-1.6 3-2"),
        detail(seg(2.5, 13, 21.5, 13)),
        detail(seg(9, 13, 9, 21)), detail(seg(15, 13, 15, 21)),
        mark(poly([(5.8, 15), (7.8, 18.5), (3.8, 18.5)], closed=True)),
        mark(poly([(12, 18.5), (14, 15), (10, 15)], closed=True)),
        mark(poly([(18.2, 15), (20.2, 18.5), (16.2, 18.5)], closed=True)),
    ]


@icon("vinegar-station", CAT, "A post-mounted box with a gable roof holding a squeeze bottle, with a jellyfish on the box.",
      tags=["jellyfish sting", "beach first aid", "sting treatment", "vinegar bottle", "lifeguard post", "sea safety", "beach"])
def _(S):
    tent = ST("M6 12.5c0 1.5 1 2 1 3.2M8.8 12.5v3.4M11.4 12.5c0 1.5-1 2-1 3.2", 1.1, "round", "round")
    jelly = U(P("M4.2 11.5a3.4 3.4 0 0 1 6.8 0Z"), tent)
    return [
        shell(poly([(2.5, 8), (12, 2.5), (21.5, 8), (21.5, 18), (2.5, 18)], closed=True, r=S.r)),
        mark(path_to_d(jelly)),
        mark(rect(15, 10, 4, 5.5, 1)), mark(rect(16.3, 7.6, 1.4, 2.6)),
        line(seg(12, 18, 12, 22)),
    ]


@icon("avalanche-beacon-checkpoint", CAT, "A post with a round sensor and signal arcs reaching a skier wearing a chest pack.",
      tags=["transceiver check", "beacon test", "backcountry safety", "avalanche safety", "ski touring", "signal check", "snow safety"])
def _(S):
    return [
        shell(circle(5, 7, 3.2)),
        line(seg(5, 10.2, 5, 21)),
        line(arc(5, 7, 6.8, -40, 40)), line(arc(5, 7, 10.5, -32, 32)),
        dot(19.5, 5.5, 2),
        line(seg(19.5, 8.5, 19.5, 15)),
        solid(rect(17.8, 9, 3.4, 3.2, 0.8)),
        line(poly([(19.5, 15), (18, 20.5)])), line(poly([(19.5, 15), (21.2, 20.5)])),
    ]


@icon("ski-patrol", CAT, "A skier wearing a backpack marked with a cross.",
      tags=["ski rescue", "mountain rescue", "first aid skier", "piste patrol", "snow patrol", "medic", "ski safety"])
def _(S):
    bag = D(P(rect(4.5, 7, 7, 8.5, 1.5)), P(rect(7.3, 8.3, 1.4, 5.9)), P(rect(5.5, 10.2, 5.4, 1.4)))
    return skier(S, 13.5, 4.5, 1.0) + [solid(path_to_d(bag))]


@icon("ski-school", CAT, "A large skier followed by a small skier.",
      tags=["ski lessons", "learn to ski", "ski instructor", "beginners", "kids ski", "snow school", "winter sports"])
def _(S):
    return skier(S, 8, 4.5, 1.0) + skier(S, 18.3, 11.3, 0.6, pole=False)


@icon("magic-carpet-lift", CAT, "A small skier standing on a conveyor belt that rises up a short slope under a cover.",
      tags=["conveyor lift", "carpet lift", "beginner lift", "ski conveyor", "moving carpet", "ski slope", "snow"])
def _(S):
    return [
        shell(poly([(2, 17.5), (22, 9.5), (22, 12.5), (2, 20.5)], closed=True, r=S.r * 0.5)),
        line(poly([(12, 4.5), (22, 1.8)])) if False else line(poly([(13, 6.3), (22, 3.2)])),
    ] + skier(S, 9, 5.2, 0.5, pole=False)


def tri(S):
    """Warning triangle shell."""
    return shell(poly([(12, 2.5), (22, 19.5), (2, 19.5)], closed=True, r=S.r * 1.2))


# ============================================================================ chunk 3: lifts, water, ride rules

@icon("terrain-park", CAT, "A snowboarder in the air above a curved kicker jump.",
      tags=["snow park", "freestyle park", "jump", "snowboard jump", "kicker", "ski park", "tricks"])
def _(S):
    return [
        solid("M2 21.5C11 21.5 17 19 21.5 12.5V21.5Z"),
        dot(10.5, 4, 2),
        line(poly([(10.5, 6.5), (11, 11.5)])),
        line(poly([(6.5, 7.5), (10.5, 8), (15.5, 6)])),
        line(pl(S, [(11, 11.5), (9.5, 14.5)], k=0.5)), line(pl(S, [(11, 11.5), (13.5, 14)], k=0.5)),
        line(seg(6.5, 16, 16.5, 13.5)),
    ]


@icon("platter-lift", CAT, "A skier holding a pole with a round disc seat, hanging from an overhead cable.",
      tags=["button lift", "disc lift", "drag lift", "surface lift", "ski tow", "surface tow", "ski lift"])
def _(S):
    return skier(S, 8.5, 6.5, 0.9, pole=False) + [
        line(seg(2, 2.5, 22, 2.5)),
        line(seg(16, 2.5, 16, 13.5)),
        solid(ellipse(16, 14.2, 3.4, 1.2)),
        line(seg(8.5, 12, 16, 8.5)),
    ]


@icon("rope-tow", CAT, "A skier gripping a moving rope that runs up the slope between two pulley posts.",
      tags=["ski rope", "nursery tow", "beginner tow", "handle tow", "ski hill lift", "pulley", "snow"])
def _(S):
    return [
        line(seg(2.5, 14.5, 2.5, 21.5)), dot(2.5, 14.5, 1.7),
        line(seg(21.5, 4.5, 21.5, 21.5)), dot(21.5, 4.5, 1.7),
        line(seg(2.5, 14.5, 21.5, 4.5)),
    ] + skier(S, 12, 4.8, 0.72, pole=False, tilt=-27)


@icon("pump-out-station", CAT, "A dockside post with a hose and nozzle reaching the deck fitting of a small boat.",
      tags=["sewage pump out", "boat waste", "marina", "holding tank", "boat toilet", "dock", "boating"])
def _(S):
    return [
        solid(rect(2.5, 3, 3, 18)),
        line("M5.5 7.5c4 0 6.5 1.5 9 5"),
        solid(rect(14, 11.5, 3.2, 2.4, 0.5)),
        shell(poly([(8, 15.5), (22, 15.5), (19.5, 20), (10.5, 20)], closed=True, r=S.r * 0.6)),
        line(seg(15.6, 14, 15.6, 15.5)),
    ]


@icon("fishing-line-recycling-bin", CAT, "A narrow upright tube bin on a post with a tangle of fishing line.",
      tags=["fishing line recycle", "line disposal", "angler bin", "monofilament", "wildlife protection", "pier bin", "tackle waste"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 7, 15, rr(S, 2.5))),
        mark(rect(6.5, 5, 3, 1.6, 0.5)),
        line(seg(8, 17.5, 8, 21.5)), line(seg(4.5, 21.5, 11.5, 21.5)),
        line("M20.5 5.5c-3.5-1.5-6 1-3.5 3s5 .5 3.5 3.5-5 1.5-3.5 4.5 4 1.5 3-1"),
    ]


@icon("fish-cleaning-station", CAT, "A counter with a tap and sink and a fish lying flat on top.",
      tags=["fish cleaning", "gutting table", "filleting table", "angler sink", "boat ramp", "fishing", "fish prep"])
def _(S):
    fish = U(P(ellipse(16.5, 9.5, 3.8, 1.9)), P(poly([(19.8, 9.5), (22, 7.7), (22, 11.3)], closed=True)))
    return [
        line(seg(2, 13, 22, 13)),
        line(seg(4, 13, 4, 21.5)), line(seg(20, 13, 20, 21.5)),
        line(poly([(8, 13), (8, 6.5), (11.5, 6.5), (11.5, 9)])),
        line(pl(S, [(6.5, 16), (7, 18.5), (13, 18.5), (13.5, 16)], k=0.4)),
        solid(path_to_d(fish)),
    ]


@icon("pilgrim-route-marker", CAT, "A square marker plate showing a scalloped shell with radiating ribs.",
      tags=["scallop shell", "way marker", "camino", "pilgrimage trail", "waymark", "long distance path", "route sign"])
def _(S):
    c = (12, 16.5)
    pts = [polar(c[0], c[1], 7, a) for a in (180, 216, 252, 288, 324, 360)]
    d = f"M{fmt(c[0])} {fmt(c[1])}L{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for q in pts[1:]:
        d += f"A2.4 2.4 0 0 1 {fmt(q[0])} {fmt(q[1])}"
    d += "Z"
    ribs = [detail(seg(c[0], c[1], q[0], q[1])) for q in pts[1:-1]]
    return [shell(rect(2.5, 2.5, 19, 19, rr(S, 2.5))), detail(d)] + ribs


@icon("hang-gliding", CAT, "A triangular delta wing glider with a pilot hanging beneath it.",
      tags=["hang glider", "delta wing", "air sports", "paragliding", "flying", "cliff launch", "aerial sport"])
def _(S):
    return [
        shell(poly([(2, 9.5), (12, 3), (22, 9.5), (12, 7.5)], closed=True, r=S.r)),
        line(seg(12, 7.5, 12, 14.5)),
        dot(16.5, 16, 1.9),
        line(poly([(14.5, 16.4), (8, 16.6)])),
        line(pl(S, [(8, 16.6), (5, 19)], k=0.6)),
        line(poly([(12, 14.5), (14.5, 16.4)])) if False else line(poly([(12, 14.5), (12.5, 16.3)])),
    ]


@icon("windsurfing", CAT, "A sailboard with a tilted triangular sail and a surfer leaning back holding the boom.",
      tags=["windsurf", "sailboard", "water sports", "board sailing", "wind sport", "surfing", "watersports"])
def _(S):
    return [
        shell(poly([(10, 17.5), (13, 2.5), (4, 14)], closed=True, r=S.r * 0.8)),
        line(poly([(2.5, 19), (8, 20.5), (18, 20.5), (21.5, 19)])),
        dot(19.2, 8, 1.9),
        line(poly([(18.8, 10.7), (17, 16)])),
        line(poly([(18.4, 11.6), (11.5, 11)])),
        line(pl(S, [(17, 16), (17.5, 19.2)], k=0.4)),
    ]


@icon("outdoor-fitness-station", CAT, "A park exercise frame with parallel bars and a figure doing a dip.",
      tags=["park gym", "calisthenics", "outdoor gym", "exercise bars", "dip bars", "workout park", "fitness trail"])
def _(S):
    return [
        line(seg(2.5, 11.5, 21.5, 11.5)),
        line(seg(4, 11.5, 4, 21.5)), line(seg(20, 11.5, 20, 21.5)),
        dot(12, 4.5, 2),
        line(poly([(12, 7.5), (12, 14)])),
        line(pl(S, [(8.5, 11.2), (12, 7.5), (15.5, 11.2)], k=0.6)),
        line(pl(S, [(12, 14), (10, 18.5)], k=0.5)), line(pl(S, [(12, 14), (14.5, 18.5)], k=0.5)),
    ]


@icon("shoe-locker", CAT, "A grid of small lockers with a pair of shoes in one compartment.",
      tags=["shoe storage", "shoe cubby", "footwear locker", "shoe rack", "temple", "spa", "entrance"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 2.5))),
        detail(seg(12, 3, 12, 21)), detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15)),
        mark(ellipse(6.4, 18, 1.3, 1.9)), mark(ellipse(9.4, 18, 1.3, 1.9)),
        mark(circle(15, 6, 0.8)), mark(circle(18.8, 12, 0.8)), mark(circle(15, 18, 0.8)),
    ]


@icon("foot-shower", CAT, "A low outdoor tap spraying water over a bare foot on a slatted platform.",
      tags=["beach shower", "feet wash", "sand rinse", "foot rinse", "outdoor tap", "pool entrance", "beach"])
def _(S):
    foot = U(P("M10 15.5c0-3 1.4-4.6 4-4.6 2.4 0 3.7 1.4 4.3 3.2l.7 1.4v.3Z"))
    return [
        line(poly([(5, 21), (5, 4.5), (11, 4.5)])),
        line(seg(11, 4.5, 11, 6.2)),
        line(seg(9, 8.5, 9, 10)), line(seg(12.5, 8.5, 12.5, 10)),
        solid(path_to_d(foot)),
        line(seg(2.5, 19, 21.5, 19)),
        line(seg(8, 19, 8, 21.5)), line(seg(13, 19, 13, 21.5)), line(seg(18, 19, 18, 21.5)),
    ]


@icon("holy-water-font", CAT, "A shallow stone basin on a wall bracket with a fingertip dipping into it.",
      tags=["stoup", "holy water stoup", "church entrance", "blessing basin", "wall basin", "chapel", "water basin"])
def _(S):
    return [
        line(seg(3, 3, 3, 21)),
        shell("M5.5 11h13c0 3.6-2.6 6.4-6.5 6.4S5.5 14.6 5.5 11Z"),
        line(poly([(3, 20), (12, 17.4)])),
        solid(path_to_d(ST(seg(15, 2.5, 15, 8.2), 2.4, "round", "round"))),
        detail("M11.5 13.5h4"),
    ]


@icon("priority-queue-sign", CAT, "Three small figures at the front of a lane: a wheelchair user, an expectant person and a person with a cane.",
      tags=["priority lane", "priority seating", "accessible queue", "elderly priority", "pregnant priority", "disabled priority", "fast track"])
def _(S):
    return [
        dot(5, 5, 1.7),
        line(seg(5, 8, 5, 12.5)), line(seg(5, 12.5, 8.5, 12.5)),
        line(circle(5.8, 16.6, 3.1)),
        dot(12.5, 5, 1.7),
        line(seg(12, 8, 12, 14)),
        dot(14, 11.2, 2.2),
        line(pl(S, [(12, 14), (11.2, 20.5)], k=0.5)), line(pl(S, [(12, 14), (13.8, 20.5)], k=0.5)),
        dot(19.2, 5, 1.7),
        line(poly([(19.2, 8), (18.7, 14)])),
        line(pl(S, [(18.7, 14), (18, 20.5)], k=0.5)),
        line(poly([(21.5, 10.5), (21.5, 20.5)])),
        line(poly([(19.4, 10.5), (21.5, 10.5)])),
    ]


@icon("fare-box", CAT, "A pedestal fare box with a coin slot on top and a card reader panel on its face.",
      tags=["bus fare", "coin box", "ticket validator", "fare collection", "tap card", "bus driver box", "pay here"])
def _(S):
    return [
        shell(poly([(6, 8.5), (9, 3), (15, 3), (18, 8.5), (18, 21), (6, 21)], closed=True, r=S.r)),
        mark(rect(9.5, 5.2, 5, 1.4, 0.5)),
        mark(rect(8.5, 9.8, 7, 4.2, 0.8)),
        mark(circle(10.5, 17.6, 1)), mark(circle(13.5, 17.6, 1)),
    ]


@icon("rapid-water-rise-sign", CAT, "Warning triangle with a rising arrow above flood waves.",
      tags=["flash flood", "rising water", "flood warning", "dam release", "river level", "water hazard", "danger"])
def _(S):
    return [
        tri(S),
        detail(seg(12, 9.2, 12, 13)),
        detail(pl(S, [(10.2, 11), (12, 9.2), (13.8, 11)], k=0.3)),
        detail("M6.6 17.1c1.2-1.2 2.4-1.2 3.7 0s2.6 1.2 3.7 0 2.4-1.2 3.4 0"),
    ]


@icon("swift-water-sign", CAT, "Warning triangle with a swimmer's head and arm swept along by current lines.",
      tags=["strong current", "river danger", "fast water", "rip", "undertow", "no swimming", "water hazard"])
def _(S):
    return [
        tri(S),
        dot(10.5, 12.2, 1.6),
        detail(poly([(12, 13), (15.5, 11.8)])),
        detail("M6.6 16.6c1.2-1.2 2.4-1.2 3.7 0s2.6 1.2 3.7 0 2.4-1.2 3.4 0"),
    ]


@icon("remain-seated-sign", CAT, "A rider seated in a ride car with a lap bar across the thighs and a downward arrow.",
      tags=["stay seated", "ride safety", "lap bar", "roller coaster", "amusement park", "keep seated", "ride rule"])
def _(S):
    return [
        dot(14, 5.5, 2),
        line(seg(14, 8.5, 14, 15)),
        line(pl(S, [(14, 15), (19.5, 15), (19.5, 20.5)], k=0.7)),
        line(seg(15.5, 11.8, 19.5, 11.8)),
        line(seg(19.5, 11.8, 19.5, 15)),
        line(seg(10, 4.5, 10, 21)),
        line(seg(4.5, 3.5, 4.5, 12.5)),
        line(pl(S, [(2.3, 10.2), (4.5, 12.5), (6.7, 10.2)], k=0.3)),
    ]


@icon("keep-arms-inside-sign", CAT, "A rider in a ride car with one arm reaching out of the car, struck through.",
      tags=["arms inside", "hands inside ride", "ride safety", "do not reach out", "amusement park", "ride rule", "no reaching"])
def _(S):
    return [
        shell(rect(2.5, 13, 13, 7.5, rr(S, 2.5))),
        dot(8.5, 6.5, 2),
        line(seg(8.5, 9.3, 8.5, 13)),
        line(poly([(8.5, 10.4), (14.5, 9.4), (21.5, 10.4)])),
        line(seg(15, 3, 22, 13)),
    ]


@icon("ride-height-requirement", CAT, "A child standing beside a tall measuring post with a bar at head height.",
      tags=["height limit", "minimum height", "must be this tall", "height check", "ride rule", "amusement park", "child height"])
def _(S):
    return [
        line(seg(19, 2.5, 19, 21.5)),
        line(seg(3.5, 4.2, 19, 4.2)),
        line(seg(15.5, 9.5, 19, 9.5)), line(seg(16.5, 13.5, 19, 13.5)), line(seg(15.5, 17.5, 19, 17.5)),
        dot(8, 8.8, 2.2),
        line(seg(8, 11.5, 8, 16.5)),
        line(pl(S, [(5, 14.5), (8, 12), (11, 14.5)], k=0.5)),
        line(pl(S, [(8, 16.5), (6.3, 21.5)], k=0.5)), line(pl(S, [(8, 16.5), (9.7, 21.5)], k=0.5)),
    ]


@icon("splash-zone-sign", CAT, "A curling wave with flying droplets heading toward a seated rider.",
      tags=["splash zone", "get wet", "water ride", "log flume", "wet seats", "amusement park", "soaked"])
def _(S):
    return [
        line("M2.5 20C2.5 13.5 6 9 10.5 9c2.2 0 3.2 1.6 2.7 3-.5 1.3-2.5 1.1-2.6-.3"),
        line(seg(2.5, 21, 12.5, 21)),
        dot(13.8, 4.5, 1), dot(16.8, 3.8, 1), dot(15.5, 7.2, 1), dot(12, 5.2, 1),
        dot(19.5, 11.5, 2),
        line(seg(19.5, 14.3, 19.5, 18.7)),
        line(pl(S, [(19.5, 18.7), (15.8, 18.7), (15.8, 21.5)], k=0.7)),
    ]


@icon("snack-vending-machine", CAT, "A tall vending cabinet with shelves of snack packets and a dispense slot.",
      tags=["vending", "snack machine", "crisps", "candy machine", "coil vending", "dispenser", "food machine"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, rr(S, 2.5))),
        detail(seg(16, 2.5, 16, 15)),
        detail(seg(3.5, 8, 16, 8)), detail(seg(3.5, 13, 16, 13)),
        detail(seg(3.5, 17, 20.5, 17)),
        mark(rect(6, 4.8, 3, 2.2, 0.4)), mark(rect(11, 4.8, 3, 2.2, 0.4)),
        mark(rect(6, 9.8, 3, 2.2, 0.4)), mark(rect(11, 9.8, 3, 2.2, 0.4)),
        mark(rect(18, 5.5, 0.1, 0.1)) if False else mark(circle(18.2, 6, 0.8)), mark(circle(18.2, 9.6, 0.8)), mark(circle(18.2, 13.2, 0.8)),
    ]


@icon("beach-clean-station", CAT, "An upright board holding a litter picker and a roll of bags beside a small bin.",
      tags=["litter picker", "beach cleanup", "bin bags", "litter pick", "trash grabber", "volunteer", "sand"])
def _(S):
    return [
        shell(rect(2.5, 3, 11.5, 17, rr(S, 2.5))),
        detail(seg(6, 17, 10.5, 7)),
        mark(circle(9.5, 14.2, 1.5)),
        shell(poly([(16.5, 12.5), (21.5, 12.5), (20.5, 20), (17.5, 20)], closed=True, r=S.r * 0.5)),
        line(seg(15.5, 11, 22.5, 11)) if False else line(seg(15.5, 12.5, 22.5, 12.5)),
    ]


@icon("dog-tie-up-point", CAT, "A metal ring on a wall bracket with a leash clipped to it and a small bowl below.",
      tags=["dog hitch", "leash ring", "dog parking", "tether point", "pet friendly", "cafe dog", "water bowl"])
def _(S):
    return [
        solid(rect(2, 2.5, 2.4, 19)),
        line(seg(4.4, 8, 6, 8)),
        line(circle(9, 8, 3)),
        line("M12 9.5c4 .8 7 3 7.5 6.5"),
        dot(19.5, 16.5, 1.5),
        shell(poly([(9, 18), (18, 18), (16.5, 21.5), (10.5, 21.5)], closed=True, r=S.r * 0.6)),
    ]
