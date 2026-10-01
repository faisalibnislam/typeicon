"""TypeIcon Core: sports gear, batch 006 (venues, apparel and training kit)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "sports-gear"


def pick(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


# ============================================================================ chunk 1

@icon("reaction-ball", CAT, "Lumpy ball with six rounded bumps and a small centre ring.",
      tags=["reaction ball", "agility", "training", "bounce", "hand-eye", "coordination", "drill"])
def _(S):
    n = 6
    r0 = 7.4
    ar = pick(S, 4.2, 4.8)
    pts = [polar(12, 12, r0, -90 + i * 60) for i in range(n)]
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(1, n + 1):
        p = pts[i % n]
        d += f"A{fmt(ar)} {fmt(ar)} 0 0 1 {fmt(p[0])} {fmt(p[1])}"
    d += "Z"
    return [shell(d), detail(circle(12, 12, pick(S, 2.0, 2.4)))]


def _ring_filled():
    ring = D(P(circle(12, 11.5, 9.5)), P(circle(12, 11.5, 4.0)))
    ground = ST("M3 21.5H21", 2.0, "butt", "miter", 4)
    return U(ring, ground)


@icon("tackle-wheel", CAT, "Large padded ring standing upright on the ground.",
      tags=["tackle wheel", "tackling", "football", "rugby", "training", "padded ring", "drill"], filled=_ring_filled)
def _(S):
    return [shell(circle(12, 11.5, 9)), shell(circle(12, 11.5, pick(S, 4.5, 4.0))), line(seg(3, 21.5, 21, 21.5))]


@icon("ski-jump-hill", CAT, "Steep in-run ramp with a takeoff lip and a jumper in the air above the landing slope.",
      tags=["ski jumping", "ramp", "hill", "winter sports", "takeoff", "landing slope", "nordic"])
def _(S):
    return [
        shell(poly([(3, 4), (9.5, 11.5), (13, 11.5), (16.5, 13.5), (19, 16.5), (21, 20), (21, 21), (3, 21)], closed=True, r=S.r)),
        dot(16.5, 7, 1.75),
    ]


@icon("spinnaker-sail", CAT, "Sailboat with a large ballooning front sail and a small jib.",
      tags=["spinnaker", "sailing", "yacht", "regatta", "sail", "boat", "downwind"])
def _(S):
    return [
        shell("M12 3C22 3.5 22.5 11 19 15H12Z"),
        shell(poly([(8, 7), (8, 15), (3.5, 15)], closed=True, r=S.r)),
        line(seg(12, 15, 12, 18)),
        shell(poly([(3, 18.5), (21, 18.5), (18, 21.5), (6, 21.5)], closed=True, r=S.r)),
    ]


@icon("mountainboard", CAT, "Short board with two bindings and big air tires at each end.",
      tags=["mountainboard", "all-terrain board", "off-road", "extreme sports", "tires", "bindings", "dirtboard"])
def _(S):
    return [
        shell(rect(2.5, 9.5, 19, 3, pick(S, 1, 1.5))),
        line(poly([(6, 9.5), (6, 6), (10, 6), (10, 9.5)], r=S.r)),
        line(poly([(14, 9.5), (14, 6), (18, 6), (18, 9.5)], r=S.r)),
        shell(circle(7, 17.5, 3.5)), shell(circle(17, 17.5, 3.5)),
        dot(7, 17.5, pick(S, 1.0, 1.25)), dot(17, 17.5, pick(S, 1.0, 1.25)),
    ]


@icon("bobsleigh-track", CAT, "Curving ice channel with steep banked walls seen from above.",
      tags=["bobsled", "bobsleigh", "luge", "skeleton", "ice track", "winter sports", "bank", "turn"])
def _(S):
    return [
        line("M3.5 21.5V12A8.5 8.5 0 0 1 20.5 12V21.5"),
        line("M9 21.5V12A3 3 0 0 1 15 12V21.5"),
        dot(6.25, 15.5, 1.0), dot(17.75, 15.5, 1.0),
    ]


@icon("equestrian-arena", CAT, "Fenced sand rectangle with letter markers around the edge.",
      tags=["riding arena", "dressage", "horse", "manege", "paddock", "show jumping", "equestrian", "ring"])
def _(S):
    return [
        shell(rect(2.5, 5, 19, 14, pick(S, 1, 3))),
        dot(12, 8.25, 1.0), dot(12, 15.75, 1.0), dot(6.25, 12, 1.0), dot(17.75, 12, 1.0),
    ]


@icon("fencing-piste", CAT, "Long narrow strip with a centre line and two en garde lines.",
      tags=["fencing", "strip", "piste", "sabre", "foil", "epee", "court", "en garde"])
def _(S):
    return [
        shell(rect(2.5, 8.5, 19, 7, pick(S, 1, 2.5))),
        detail(seg(12, 8.5, 12, 15.5)),
        detail(seg(7.5, 8.5, 7.5, 15.5)),
        detail(seg(16.5, 8.5, 16.5, 15.5)),
        line(seg(12, 5, 12, 8.5)), line(seg(12, 15.5, 12, 19)),
    ]


@icon("cycling-jersey", CAT, "Fitted short-sleeve jersey with a front zip and three pockets across the hem.",
      tags=["bike jersey", "cycling", "cyclist", "bicycle", "road bike", "zip", "pockets", "kit"])
def _(S):
    return [
        shell(poly([(9, 3.5), (3, 6.5), (4.5, 11), (6, 10.5), (6, 20.5), (18, 20.5), (18, 10.5), (19.5, 11), (21, 6.5), (15, 3.5)], closed=True, r=S.r)),
        detail("M9 3.5Q12 6.5 15 3.5"),
        detail(seg(12, 6, 12, 11.5)),
        detail(seg(6, 15.5, 18, 15.5)),
        detail(seg(10, 15.5, 10, 20.5)), detail(seg(14, 15.5, 14, 20.5)),
    ]


@icon("ski-suit", CAT, "One-piece snowsuit with a front zip, belt and long legs.",
      tags=["snowsuit", "snow gear", "skiing", "winter", "coverall", "jumpsuit", "snowboard", "overalls"])
def _(S):
    return [
        shell(poly([(9, 2.5), (15, 2.5), (19.5, 5), (20.5, 14), (17.5, 14), (17, 9), (16.5, 21.5), (12.9, 21.5),
                    (12, 16.5), (11.1, 21.5), (7.5, 21.5), (7, 9), (6.5, 14), (3.5, 14), (4.5, 5)], closed=True, r=S.r)),
        detail(seg(12, 4.5, 12, 11.5)),
        detail(seg(7, 12.5, 17, 12.5)),
    ]


@icon("riding-boots", CAT, "Tall smooth knee-high boot with a small heel.",
      tags=["riding boots", "equestrian", "horse riding", "tall boot", "jodhpur", "leather", "footwear", "dressage"])
def _(S):
    return [
        shell(poly([(7, 2.5), (14, 2.5), (14.5, 14.5), (19.5, 16), (21, 18.5), (21, 21), (7, 21)], closed=True, r=S.r)),
        detail(seg(7, 6, 14, 6)),
        detail(seg(7, 18, 11.5, 18)),
    ]


@icon("golf-shoes", CAT, "Low saddle-style shoe with small cleats on the sole.",
      tags=["golf shoe", "cleats", "spikes", "golfer", "footwear", "saddle shoe", "golf course"])
def _(S):
    return [
        shell(poly([(3, 6.5), (8.5, 6.5), (9, 10.5), (15, 12), (21, 14.5), (21, 17.5), (3, 17.5)], closed=True, r=S.r)),
        detail(seg(3, 14.5, 20.5, 14.5)),
        detail(poly([(11.5, 11), (12.5, 14.5)])),
        dot(6, 20, 1.1), dot(12, 20, 1.1), dot(18, 20, 1.1),
    ]


@icon("wrestling-singlet", CAT, "One-piece sleeveless wrestling suit with deep arm openings and short legs.",
      tags=["singlet", "wrestling", "uniform", "mat", "combat sports", "bodysuit", "athlete", "kit"])
def _(S):
    return [
        shell(poly([(8, 3), (10.5, 3), (11, 6.5), (13, 6.5), (13.5, 3), (16, 3), (17, 9), (17, 12), (19, 18.5),
                    (14.5, 18.5), (12, 14.5), (9.5, 18.5), (5, 18.5), (7, 12), (7, 9)], closed=True, r=S.r)),
    ]


@icon("boxing-robe", CAT, "Hooded satin robe with a V front, long sleeves and a tied belt.",
      tags=["fight robe", "boxing", "hooded robe", "ring walk", "boxer", "gown", "mma", "cover-up"])
def _(S):
    return [
        shell(poly([(9, 4.5), (15, 4.5), (20, 7), (21, 17.5), (18, 17.5), (17.5, 10), (17, 21.5), (7, 21.5),
                    (6.5, 10), (6, 17.5), (3, 17.5), (4, 7)], closed=True, r=S.r)),
        detail(poly([(9, 4.5), (12, 12), (15, 4.5)])),
        detail(seg(6.7, 15, 17.3, 15)),
        line("M8 4.5C8 1 16 1 16 4.5"),
    ]


@icon("back-protector", CAT, "Segmented armored plate along the spine with shoulder straps.",
      tags=["spine protector", "motorcycle", "mountain bike", "ski", "armor", "body armour", "safety", "vest"])
def _(S):
    return [
        shell(poly([(8.5, 3), (15.5, 3), (16.5, 9), (15, 21), (9, 21), (7.5, 9)], closed=True, r=S.r)),
        detail(seg(8, 8, 16, 8)), detail(seg(8, 12.5, 16, 12.5)), detail(seg(8.5, 17, 15.5, 17)),
        line(poly([(7.5, 5), (3.5, 8.5)])), line(poly([(16.5, 5), (20.5, 8.5)])),
    ]


# ============================================================================ chunk 2

def capsule_pts(a, b, hw):
    """Corners of a rectangle of half-width hw along the segment a-b."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    nx, ny = -dy / n * hw, dx / n * hw
    return [(a[0] + nx, a[1] + ny), (b[0] + nx, b[1] + ny), (b[0] - nx, b[1] - ny), (a[0] - nx, a[1] - ny)]


@icon("helmet-camera", CAT, "Helmet with a small box camera and lens mounted on top.",
      tags=["helmet cam", "action camera", "head camera", "pov", "cycling", "skiing", "recording", "gopro-style"])
def _(S):
    return [
        shell("M3.5 18.5V14.5C3.5 10 7.5 7.5 12 7.5C16.5 7.5 20.5 10 20.5 14.5V18.5Z"),
        shell(rect(9, 2.5, 8, 5, pick(S, 0.5, 1.5))),
        dot(14.5, 5, 1.0),
        detail(poly([(3.5, 14.5), (11, 14.5), (13, 18.5)])),
    ]


@icon("ball-hopper", CAT, "Wire basket on folding legs full of tennis balls.",
      tags=["ball basket", "tennis", "ball collector", "ball pickup", "tennis balls", "coach", "practice", "hopper"])
def _(S):
    return [
        dot(7.5, 6.2, 2.0), dot(12, 5.2, 2.0), dot(16.5, 6.2, 2.0),
        shell(poly([(3.5, 9), (20.5, 9), (18.5, 16.5), (5.5, 16.5)], closed=True, r=S.r)),
        detail(seg(9, 9, 9.5, 16.5)), detail(seg(15, 9, 14.5, 16.5)),
        line(seg(8, 16.5, 5.5, 21.5)), line(seg(16, 16.5, 18.5, 21.5)),
    ]


@icon("racing-slick", CAT, "Wide smooth tire seen at an angle, with no tread pattern.",
      tags=["slick tire", "racing tyre", "motorsport", "smooth tire", "track day", "wheel", "grip", "formula"])
def _(S):
    return [
        shell("M8 3H16A5 9 0 0 1 16 21H8A5 9 0 0 1 8 3Z"),
        detail("M8 3A5 9 0 0 1 8 21"),
        dot(8, 12, pick(S, 1.4, 1.8)),
    ]


@icon("dojo", CAT, "Training hall with a sweeping curved roof, a doorway and a hanging banner.",
      tags=["martial arts", "karate", "judo", "training hall", "gym", "school", "tiled roof", "dojang"])
def _(S):
    return [
        shell("M12 2.5L17 5C18.2 8 19.5 9 22 9.5H2C4.5 9 5.8 8 7 5Z"),
        shell(rect(5, 9.5, 14, 11.5, 0)),
        sq(7.5, 14.5, 4, 6.5),
        detail(rect(14.5, 13, 3, 5.5, 0)),
    ]


@icon("cheer-sticks", CAT, "Two long inflatable noise sticks crossed in an X.",
      tags=["thunder sticks", "noise makers", "cheering", "fans", "supporters", "clapper sticks", "spectator", "crowd"])
def _(S):
    hw = pick(S, 2.0, 2.2)
    u = math.sqrt(0.5)
    g = 4.3
    a = capsule_pts((4.5, 4.5), (19.5, 19.5), hw)
    p1 = capsule_pts((19.5, 4.5), (12 + g * u, 12 - g * u), hw)
    p2 = capsule_pts((12 - g * u, 12 + g * u), (4.5, 19.5), hw)
    return [shell(poly(a, closed=True, r=S.r)), shell(poly(p1, closed=True, r=S.r)), shell(poly(p2, closed=True, r=S.r))]


@icon("racing-suit", CAT, "Driver's one-piece overalls with a high collar and a front zip, arms angled out.",
      tags=["race suit", "driver", "motorsport", "fireproof", "coveralls", "karting", "pit crew", "overalls"])
def _(S):
    return [
        shell(poly([(9.5, 3), (14.5, 3), (21.5, 9.5), (19.5, 12), (16.5, 9.5), (16.5, 13.5), (18, 21.5), (13.5, 21.5),
                    (12, 15.5), (10.5, 21.5), (6, 21.5), (7.5, 13.5), (7.5, 9.5), (4.5, 12), (2.5, 9.5)], closed=True, r=S.r)),
        detail(poly([(9.5, 5.8), (14.5, 5.8)])),
        detail(seg(12, 5.8, 12, 12)),
    ]


@icon("sports-commentator", CAT, "Broadcaster in a headset with a boom mic, sitting behind a commentary desk.",
      tags=["commentator", "announcer", "broadcaster", "play-by-play", "headset", "radio", "tv", "pundit"])
def _(S):
    return [
        shell(circle(12, 9.5, 3.7)),
        line("M5.5 10.5A6.5 7.5 0 0 1 18.5 10.5"),
        sq(4.2, 9.5, 2.4, 4.5, pick(S, 0, 1)), sq(17.4, 9.5, 2.4, 4.5, pick(S, 0, 1)),
        line("M18.6 14Q18.6 16.2 14.6 15.4"),
        dot(14.4, 15.4, 1.0),
        shell(rect(3, 18, 18, 3.5, pick(S, 0.5, 1.75))),
    ]
