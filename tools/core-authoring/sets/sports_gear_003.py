"""TypeIcon Core: sports gear and activities (batch 003).

Athletes are stick figures in the style of the sports set: a solid head (r 2.25) over 2 px limbs, faceted in
Line and filleted in Rounded. Water is a zigzag in Line and a smooth wave in Rounded.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from dsl import D, I, P, ST, U
from geometry import fmt, path_to_d, polar

CAT = "sports-gear"


# --------------------------------------------------------------------------- helpers

def pick(S, a, b):
    return a if S.name == "line" else b


def _pp(p):
    return f"{fmt(round(p[0], 3))} {fmt(round(p[1], 3))}"


def smooth(pts, closed=False):
    n = len(pts)
    d = "M" + _pp(pts[0])
    segs = n if closed else n - 1
    for i in range(segs):
        p1, p2 = pts[i], pts[(i + 1) % n]
        p0 = pts[i - 1] if (i > 0 or closed) else p1
        p3 = pts[(i + 2) % n] if (i + 2 < n or closed) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += "C" + _pp(c1) + " " + _pp(c2) + " " + _pp(p2)
    return d + ("Z" if closed else "")


def seam(S, pts, closed=False):
    return poly(pts, closed=closed) if S.name == "line" else smooth(pts, closed)


def wave(S, x0, x1, y, step=3.0, amp=1.0):
    pts, x, up = [], x0, True
    while x <= x1 + 0.01:
        pts.append((x, y - amp if up else y + amp))
        up = not up
        x += step
    return line(seam(S, pts))


def head(x, y):
    return dot(x, y, 2.25)


def close_d(d, g):
    """Fill concave corners of region d with radius g (morphological closing)."""
    a = U(P(d), ST(d, 2 * g, "round", "round"))
    return path_to_d(D(a, ST(path_to_d(a), 2 * g, "round", "round")))


def union_d(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def chord(cx, cy, r, deg, off):
    """Chord of the circle at distance off from the centre, running along direction deg."""
    a = math.radians(deg)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    h = math.sqrt(max(r * r - off * off, 0))
    mx, my = cx + nx * off, cy + ny * off
    return seg(mx - dx * h, my - dy * h, mx + dx * h, my + dy * h)


# ============================================================================ aquatic

@icon("platform-diving", CAT, "Diver in a straight head first dive from a high platform",
      tags=["diving", "dive", "high dive", "platform", "swimming pool", "olympic", "springboard"])
def _(S):
    return [
        line(seg(2.5, 4.5, 9, 4.5)), line(seg(4, 4.5, 4, 20)),
        line(seg(9.5, 7.5, 14.5, 13)), head(16.8, 15.8),
        wave(S, 9, 22, 20.5),
    ]


@icon("synchronized-diving", CAT, "Two divers in mirrored head first dives",
      tags=["synchro diving", "pair diving", "duo", "diving", "olympic", "pool", "team"])
def _(S):
    return [
        line(seg(3.5, 3, 6.7, 12.7)), head(7.7, 16.3),
        line(seg(20.5, 3, 17.3, 12.7)), head(16.3, 16.3),
        wave(S, 3, 21, 21, step=3, amp=0.9),
    ]


@icon("snorkeling", CAT, "Swimmer floating face down with a snorkel tube above the water",
      tags=["snorkel", "snorkelling", "mask", "reef", "swim", "water", "holiday"], aliases=["snorkelling"])
def _(S):
    return [
        line(poly([(3, 12.5), (9, 12.5), (12.5, 13)], r=S.r)),
        head(16, 13.5),
        line(poly([(16, 10.5), (16, 4.5), (20, 4.5)], r=S.r)),
        wave(S, 3, 21, 19),
    ]


@icon("artistic-swimming", CAT, "Two legs with pointed toes rising out of the water",
      tags=["synchronized swimming", "synchro", "legs", "pool", "water ballet", "olympic", "swimming"],
      aliases=["synchronized-swimming"])
def _(S):
    return [
        line(poly([(9, 17), (9, 8.5), (10.5, 3.5)], r=S.r)),
        line(poly([(14.5, 17), (14.5, 8.5), (16, 3.5)], r=S.r)),
        wave(S, 3, 21, 20.5),
    ]


@icon("open-water-swimming", CAT, "Swimmer in the water beside a round marker buoy",
      tags=["open water", "sea swimming", "lake", "triathlon", "buoy", "marathon swim", "swim"])
def _(S):
    return [
        head(6, 10.5),
        line(poly([(2.5, 14.5), (7, 14.5), (11.5, 10.5)], r=S.r)),
        shell("M14.5 18A4 4 0 0 1 22.5 18Z"), line(seg(18.5, 14, 18.5, 8)),
        wave(S, 2.5, 21.5, 19), wave(S, 2.5, 21.5, 22, amp=0.8),
    ]


@icon("backstroke", CAT, "Swimmer on their back with one arm raised overhead",
      tags=["back crawl", "swim stroke", "swimming", "pool", "lap", "water", "race"], aliases=["back-crawl"])
def _(S):
    return [
        head(5, 14.5),
        line(poly([(9, 14.5), (21, 14.5)], r=S.r)),
        line(seg(9, 13.5, 7, 4.5)),
        wave(S, 3, 21, 20),
    ]


@icon("breaststroke", CAT, "Swimmer with head lifted and arms sweeping out",
      tags=["swim stroke", "swimming", "pool", "lap", "frog kick", "water", "race"])
def _(S):
    return [
        head(17.5, 8.5),
        line(poly([(3, 14.5), (11, 14), (14.5, 11.5)], r=S.r)),
        line(poly([(11.5, 14), (14.5, 16.5), (19.5, 16)], r=S.r)),
        wave(S, 3, 21, 20.5),
    ]


@icon("butterfly-stroke", CAT, "Swimmer with both arms swinging forward over the water",
      tags=["butterfly", "swim stroke", "swimming", "dolphin kick", "pool", "water", "race"], aliases=["butterfly-swim"])
def _(S):
    return [
        head(14.5, 12.5),
        line(poly([(3, 15), (9, 13.5)], r=S.r)),
        line("M9.5 13C9 6.5 15 3.5 20 7.5"),
        wave(S, 3, 21, 20),
    ]


@icon("freediving", CAT, "Diver with fins descending head first along a rope",
      tags=["free diving", "apnea", "breath hold", "dive", "fins", "ocean", "underwater"])
def _(S):
    return [
        line(seg(19.5, 2.5, 19.5, 17.5)), dot(19.5, 20, 1.5),
        line(seg(10.5, 7, 10.5, 15)), head(10.5, 18.8),
        line(poly([(7.5, 2.5), (10.5, 7), (13.5, 2.5)], r=S.r)),
    ]


@icon("kickboard", CAT, "Foam swim board with a notch cut in the front",
      tags=["kick board", "swim board", "float", "pool", "training", "swimming", "lesson"])
def _(S):
    return [
        shell(path_to_d(D(P(rect(5.5, 3, 13, 18, pick(S, 2, 5))), P(rect(9.2, 1, 5.6, 6.5, 2.8))))),
        detail(seg(9, 14, 15, 14)),
    ]


@icon("pull-buoy", CAT, "Figure-eight shaped foam float held between the legs",
      tags=["float", "swim aid", "pool", "training", "legs", "swimming", "foam"])
def _(S):
    d = union_d(circle(12, 7.5, 5), circle(12, 16.5, 5))
    if S.name != "line":
        d = close_d(d, 2.5)
    return [shell(d), detail(seg(10, 12, 14, 12))]


@icon("pool-lane-rope", CAT, "Row of floats strung along a rope over the water",
      tags=["lane divider", "lane line", "pool", "swimming", "float", "race", "water"], aliases=["lane-divider"])
def _(S):
    r = min(S.R, 1.5)
    return [
        line(seg(2, 10.5, 22, 10.5)),
        shell(rect(3, 7, 4, 7, r)), shell(rect(10, 7, 4, 7, r)), shell(rect(17, 7, 4, 7, r)),
        wave(S, 3, 21, 19),
    ]


def _coil(n=2):
    pts = []
    for i in range(n * 8 + 1):
        t = i * math.pi / 4
        pts.append((9.5 + 1.0 * t - 2.4 * math.sin(t), 12 + 3.6 * math.cos(t)))
    return pts


@icon("surf-leash", CAT, "Coiled cord with a cuff at one end",
      tags=["surfboard leash", "leg rope", "ankle strap", "coil", "surfing", "board", "cord"], aliases=["leg-rope"])
def _(S):
    return [
        shell(rect(2.5, 7.5, 5, 9, min(S.R, 2))), detail(seg(2.5, 12, 7.5, 12)),
        line(seg(7.5, 12, 9.5, 12)),
        line(seam(S, [(9.5, 12), (12, 7), (14.5, 17), (17, 7), (19.5, 17), (21.5, 12)])),
    ]


@icon("surf-wax", CAT, "Round puck of board wax with cross-hatched marks",
      tags=["wax", "surfboard wax", "grip", "puck", "surfing", "board", "traction"])
def _(S):
    r = pick(S, 0, 3.5)
    return [
        shell(poly(regular(12, 12, 9.5, 10, -90), closed=True, r=r)),
        detail(chord(12, 12, 8, 45, -3)), detail(chord(12, 12, 8, 45, 3)),
        detail(chord(12, 12, 8, -45, -3)), detail(chord(12, 12, 8, -45, 3)),
    ]


@icon("water-polo-goal", CAT, "Floating goal frame with a net and a float bar below",
      tags=["goal", "net", "water polo", "pool", "float", "frame", "team sport"])
def _(S):
    return [
        line(poly([(5, 17), (5, 5), (19, 5), (19, 17)], r=S.r)),
        line(seg(9.7, 5, 9.7, 17)), line(seg(14.3, 5, 14.3, 17)), line(seg(5, 11, 19, 11)),
        shell(rect(2.5, 17.5, 19, 4, 2)),
    ]


@icon("pool-starting-block", CAT, "Angled starting platform at the pool edge with a lane number",
      tags=["starting block", "swim start", "platform", "pool", "race", "lane", "competition"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 11), (14, 8), (14, 21)], closed=True, r=S.r)),
        detail(poly([(6.5, 14.5), (8.5, 13), (8.5, 19)], r=S.r)),
    ]


@icon("wave-pool", CAT, "Swimming pool with a large curling wave at one end",
      tags=["wave pool", "water park", "surf pool", "swimming", "waves", "pool", "leisure"])
def _(S):
    return [
        line(poly([(2.5, 21), (21.5, 21)], r=S.r)),
        line("M2.5 17H7C10 17 12 15 12 11C12 7.5 14.5 5.5 17.5 5.5C20 5.5 21.5 7.5 21.5 10C21.5 12 20 13 18.5 13C17 13 16 12 16 10.8"),
    ]


@icon("skimboarding", CAT, "Rider balancing on a thin round board over shallow water",
      tags=["skim board", "beach", "shore", "wave", "board sport", "summer", "surf"], aliases=["skimboard"])
def _(S):
    return [
        head(13, 4.5),
        line(poly([(12, 8), (11.5, 13)], r=S.r)),
        line(poly([(5.5, 10), (12, 9), (18.5, 11.5)], r=S.r)),
        line(poly([(11.5, 13), (8.5, 17)], r=S.r)), line(poly([(11.5, 13), (15, 17)], r=S.r)),
        line(seg(4, 18.5, 20, 18.5)),
        wave(S, 3, 21, 21.5, amp=0.7),
    ]


@icon("spearfishing", CAT, "Diver in fins aiming a spear gun at a fish",
      tags=["spear fishing", "underwater hunting", "spear gun", "diver", "fish", "sea", "freediving"])
def _(S):
    fish = union_d(ellipse(16.5, 18, 3.5, 2.2), poly([(19.5, 18), (22, 15.8), (22, 20.2)], closed=True))
    return [
        head(5.5, 6.5),
        line(poly([(5.5, 10), (5, 15), (2.5, 19)], r=S.r)),
        line(poly([(5.5, 11), (8.5, 11), (20, 6.5)], r=S.r)),
        line(poly([(18, 4.5), (20.5, 6.5), (18, 8.5)], r=S.r)),
        shell(fish),
    ]


@icon("boat-fishing", CAT, "Angler in a small boat holding a bent fishing rod",
      tags=["fishing", "angler", "rowboat", "lake", "rod", "boat", "hobby"])
def _(S):
    return [
        shell(poly([(2.5, 15), (21.5, 15), (18.5, 20), (5.5, 20)], closed=True, r=S.r)),
        head(7.5, 6),
        line(seg(7.5, 9.5, 7.5, 14)),
        line(poly([(7.5, 10.5), (12, 11)], r=S.r)),
        line("M11.5 11C16.5 10.5 20 8 20.5 4"),
        line(seg(20.5, 4, 20.5, 9.5)),
    ]


@icon("cross-country-skiing", CAT, "Skier striding forward on long thin skis with poles pushing behind",
      tags=["nordic skiing", "xc ski", "ski", "winter sports", "classic", "skating", "snow"], aliases=["nordic-skiing"])
def _(S):
    return [
        head(13.5, 4),
        line(poly([(13, 7.5), (12, 13)], r=S.r)),
        line(poly([(12, 13), (16.5, 15.5), (16, 19)], r=S.r)),
        line(poly([(12, 13), (8, 16), (5.5, 19)], r=S.r)),
        line(poly([(12.5, 8.5), (9.5, 12.5), (4.5, 19.5)], r=S.r)),
        line(seg(13, 20.5, 22, 20.5)), line(seg(2, 20.5, 9, 20.5)),
    ]


@icon("ski-jumping", CAT, "Ski jumper flying forward with skis spread in a V",
      tags=["ski jump", "flying", "winter sports", "olympic", "hill", "jump", "skis"])
def _(S):
    return [
        head(16.5, 6.5),
        line(seg(8.5, 15.5, 13.8, 8.8)),
        line(seg(4, 17.5, 20, 11.5)), line(seg(4, 17.5, 20, 20.5)),
    ]


@icon("freestyle-skiing", CAT, "Skier flipping in the air with crossed skis above a kicker",
      tags=["aerials", "freeski", "trick", "flip", "winter sports", "olympic", "skis"], aliases=["aerial-skiing"])
def _(S):
    return [
        line(seg(4, 3.5, 20, 9.5)), line(seg(4, 9.5, 20, 3.5)),
        line(seg(12, 7, 12, 13.5)), head(12, 17.3),
        shell(poly([(2.5, 21.5), (8, 21.5), (8, 16.5)], closed=True, r=S.r)),
    ]


@icon("biathlon", CAT, "Cross-country skier with a rifle below a row of five targets",
      tags=["shooting", "rifle", "targets", "skiing", "winter sports", "olympic", "nordic"])
def _(S):
    return [
        dot(3.5, 3.5, 1.4), dot(8, 3.5, 1.4), dot(12.5, 3.5, 1.4), dot(17, 3.5, 1.4), dot(21.5, 3.5, 1.4),
        head(11, 8),
        line(poly([(10.5, 11.5), (9.5, 15.5)], r=S.r)),
        line(poly([(9.5, 15.5), (13.5, 17.5), (13, 19.5)], r=S.r)),
        line(poly([(9.5, 15.5), (6.5, 18), (4.5, 19.5)], r=S.r)),
        line(seg(8, 12.5, 18, 10)),
        line(seg(3, 21, 11, 21)), line(seg(13, 21, 21, 21)),
    ]


@icon("bobsleigh", CAT, "Streamlined bobsled with three helmeted riders tucked inside",
      tags=["bobsled", "bobsleigh", "sled", "winter sports", "olympic", "ice track", "team"], aliases=["bobsled"])
def _(S):
    return [
        head(7, 8.5), head(12, 8.5), head(17, 8.5),
        shell(poly([(2.5, 17), (4, 12.5), (17, 12.5), (21.5, 15), (21.5, 17)], closed=True, r=S.r)),
        line(seg(6.5, 17, 6.5, 20.5)), line(seg(17.5, 17, 17.5, 20.5)),
        line(seg(3, 21, 21, 21)),
    ]


@icon("luge", CAT, "Rider lying on their back feet first on a small sled",
      tags=["sled", "sledding", "ice track", "winter sports", "olympic", "toboggan", "slide"])
def _(S):
    return [
        head(5, 13),
        line(poly([(8.5, 14.5), (15.5, 14.5), (20.5, 12)], r=S.r)),
        line(poly([(2.5, 19.5), (19, 19.5), (21.5, 16.5)], r=S.r)),
    ]


@icon("skeleton-sled", CAT, "Rider lying face down head first on a flat sled",
      tags=["skeleton", "sled", "sledding", "ice track", "winter sports", "olympic", "head first"])
def _(S):
    return [
        head(18.5, 13),
        line(poly([(3, 11.5), (7.5, 14.5), (14.5, 14.5)], r=S.r)),
        line(poly([(2.5, 19.5), (19, 19.5), (21.5, 16.5)], r=S.r)),
    ]


@icon("curling-stone", CAT, "Round curling stone with a handle on top",
      tags=["curling", "granite", "stone", "rock", "ice", "winter sports", "handle"])
def _(S):
    return [
        shell(rect(3, 12.5, 18, 7.5, pick(S, 2, 3.7))),
        line(poly([(8.5, 12.5), (8.5, 7.5), (15.5, 7.5), (15.5, 12.5)], r=S.r)),
    ]


def obox(cx, cy, hl, hw, deg):
    a = math.radians(deg)
    ux, uy = math.cos(a), math.sin(a)
    vx, vy = -uy, ux
    return [(cx + ux * hl * sl + vx * hw * sw, cy + uy * hl * sl + vy * hw * sw)
            for sl, sw in ((1, 1), (1, -1), (-1, -1), (-1, 1))]


@icon("curling-broom", CAT, "Long handle ending in a flat sweeping pad",
      tags=["curling", "broom", "brush", "sweeping", "ice", "winter sports", "sweep"])
def _(S):
    return [
        line(seg(21, 3, 10.5, 13.5)),
        shell(poly(obox(8.5, 15.5, 6, 2.6, 45), closed=True, r=S.r)),
    ]


@icon("curling", CAT, "Curler sliding low and releasing a stone with a broom in the other hand",
      tags=["curling", "slide", "delivery", "stone", "broom", "ice", "winter sports"])
def _(S):
    return [
        head(7, 7.5),
        line(poly([(8, 11), (10.5, 15)], r=S.r)),
        line(poly([(8.5, 11.5), (13, 14), (15.5, 15.5)], r=S.r)),
        line(poly([(10.5, 15), (13.5, 16), (12.5, 19.5)], r=S.r)),
        line(poly([(10.5, 15), (6, 17.5), (2.5, 18.5)], r=S.r)),
        line(seg(7.5, 11.5, 3.5, 4.5)),
        shell(rect(16, 15.5, 6, 4, 1.5)),
    ]


def epoly(cx, cy, rx, ry, n=12, start=0.0):
    return [(cx + rx * math.cos(math.radians(start + i * 360 / n)),
             cy + ry * math.sin(math.radians(start + i * 360 / n))) for i in range(n)]


def ring(S, cx, cy, r, n=12):
    """Circle in Rounded, a regular polygon in Line (so the two styles differ)."""
    return circle(cx, cy, r) if S.name != "line" else poly(regular(cx, cy, r, n, -90), closed=True)


@icon("curling-house", CAT, "Top view of concentric target rings with a stone at the end of the ice",
      tags=["curling", "house", "target", "rings", "button", "ice sheet", "bullseye"], aliases=["curling-target"])
def _(S):
    return [
        shell(ring(S, 12, 10.5, 8.5)), detail(ring(S, 12, 10.5, 4.2, 10)),
        dot(12, 10.5, 1.3),
        line(seg(3, 22, 21, 22)),
    ]


@icon("speed-skating", CAT, "Skater crouched low with one arm behind the back",
      tags=["speed skater", "ice", "race", "winter sports", "olympic", "oval", "skates"])
def _(S):
    return [
        head(16, 6.5),
        line(poly([(14, 9.5), (8, 12.5)], r=S.r)),
        line(poly([(8, 12.5), (11.5, 16), (10, 19)], r=S.r)),
        line(poly([(8, 12.5), (5.5, 16.5), (2.5, 17.5)], r=S.r)),
        line(seg(12.5, 10.5, 6.5, 8.5)),
        line(seg(7.5, 20.5, 14.5, 20.5)),
    ]


@icon("figure-skating", CAT, "Skater gliding on one skate with the other leg extended behind and arms out",
      tags=["figure skater", "ice skating", "spiral", "rink", "winter sports", "olympic", "glide"])
def _(S):
    return [
        head(10, 4.5),
        line(poly([(10, 8), (11, 14)], r=S.r)),
        line(poly([(3, 11.5), (10.5, 9.5), (19, 7)], r=S.r)),
        line(seg(11, 14, 11, 19.5)), line(seg(7, 21, 17, 21)),
        line(poly([(11, 14), (6.5, 15.5), (2.5, 14)], r=S.r)),
    ]


@icon("snowshoeing", CAT, "Walker with wide oval snowshoes and trekking poles",
      tags=["snow shoe", "winter hiking", "trekking", "snow", "walk", "poles", "winter sports"])
def _(S):
    return [
        head(11, 4.5),
        line(poly([(11, 8), (11, 13)], r=S.r)),
        line(poly([(11, 13), (15, 16), (15.5, 18)], r=S.r)),
        line(poly([(11, 13), (7.5, 16.5), (7, 18)], r=S.r)),
        line(poly([(11, 9), (14.5, 11.5), (19, 19)], r=S.r)),
        shell(ellipse(17, 20.5, 3.5, 1)), shell(ellipse(7, 20.5, 3.5, 1)),
    ]


@icon("snow-tubing", CAT, "Rider sitting in a large inner tube sliding down a slope",
      tags=["tube", "sledding", "snow", "slope", "winter fun", "inner tube", "sled"])
def _(S):
    return [
        head(12, 4.5),
        line(poly([(6.5, 5.5), (12, 9.5), (17.5, 5.5)], r=S.r)),
        line(seg(12, 9.5, 12, 14)),
        shell(path_to_d(P(ellipse(12, 16.5, 9, 4.5))) if S.name != "line" else poly(epoly(12, 16.5, 9, 4.5, 12), closed=True)),
    ]


@icon("ski-poles", CAT, "Pair of ski poles with round baskets and strap handles",
      tags=["poles", "ski", "baskets", "grips", "skiing", "winter sports", "gear"], aliases=["ski-pole"])
def _(S):
    r = min(S.R, 1.5)
    return [
        line(seg(6, 6.5, 9.5, 21)), line(seg(15, 6.5, 18.5, 21)),
        shell(rect(3.7, 2.5, 3.6, 4.5, r)), shell(rect(12.7, 2.5, 3.6, 4.5, r)),
        line(seg(5.3, 16.5, 10.3, 16.5)), line(seg(14.3, 16.5, 19.3, 16.5)),
    ]


@icon("t-bar-lift", CAT, "T-bar hanging from a cable over a ski slope",
      tags=["ski lift", "drag lift", "cable", "slope", "skiing", "mountain", "resort"])
def _(S):
    return [
        line(seg(2, 3.5, 22, 3.5)),
        line(seg(8, 3.5, 8, 13)), line(seg(4, 13, 12, 13)),
        head(17, 8), line(poly([(17, 11.5), (17, 16), (14.5, 20)], r=S.r)),
        line(seg(16.5, 12, 12, 13)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("ski-trail-difficulty", CAT, "Circle, square and diamond marking ski trail difficulty",
      tags=["trail map", "piste", "slope grading", "ski run", "signs", "skiing", "difficulty"], aliases=["piste-grades"])
def _(S):
    rr = pick(S, 0, 2)
    return [
        shell(circle(12, 6.5, 3.4)),
        shell(rect(3, 14.5, 7, 7, rr)),
        shell(poly([(17.5, 13), (21.5, 17.5), (17.5, 22), (13.5, 17.5)], closed=True, r=rr)),
    ]


@icon("ski-helmet", CAT, "Rounded ski helmet with goggles strapped on the front",
      tags=["helmet", "goggles", "skiing", "snowboard", "winter sports", "safety", "head protection"])
def _(S):
    dome = (poly([(4, 17), (4, 11.5)] + [polar(12, 11.5, 8, 180 + k * 30) for k in range(1, 6)] + [(20, 11.5), (20, 17)],
                 closed=True, r=0)
            if S.name == "line" else "M4 17V11.5A8 8 0 0 1 20 11.5V17Q20 18 19 18H5Q4 18 4 17Z")
    return [
        shell(dome),
        shell(rect(5.5, 10, 13, 6.5, pick(S, 1.5, 3.2))),
        detail(seg(12, 10, 12, 16.5)),
        detail(seg(9.5, 6.8, 14.5, 6.8)),
    ]


@icon("ski-wax", CAT, "Block of wax held above the base of an upturned ski",
      tags=["wax", "glide wax", "ski tuning", "ski base", "waxing", "winter sports", "maintenance"])
def _(S):
    return [
        line(poly([(2.5, 13.5), (4.5, 18.5), (21.5, 18.5)], r=S.r)),
        shell(rect(8.5, 4.5, 9, 7, min(S.R, 1.5))),
        detail(seg(11, 8, 15, 8)),
    ]


@icon("ski-rack", CAT, "Rack holding two upright pairs of skis",
      tags=["ski storage", "ski holder", "skis", "wall rack", "gear room", "winter sports", "stand"])
def _(S):
    parts = [shell(rect(2.5, 9, 19, 4, min(S.R, 2)))]
    for x in (6, 10, 14, 18):
        parts.append(line(poly([(x, 8.5), (x, 4.5), (x + 1.8, 2.8)], r=S.r)))
        parts.append(line(seg(x, 13.5, x, 21)))
    return parts


@icon("snow-kiting", CAT, "Skier on skis pulled by a large curved kite",
      tags=["snowkite", "kite", "skiing", "wind", "winter sports", "powerkite", "snow"], aliases=["snowkite"])
def _(S):
    return [
        shell("M4 8.5C8 3 16 3 20 8.5C16 6.3 8 6.3 4 8.5Z"),
        line(seg(5, 8, 12, 15)), line(seg(19, 8, 12, 15)),
        head(12, 11.8),
        line(poly([(12, 15), (11, 18.5)], r=S.r)),
        line(seg(5, 21.5, 18, 20)),
    ]


@icon("hockey-puck", CAT, "Black hockey puck seen from slightly above",
      tags=["puck", "ice hockey", "disc", "rink", "winter sports", "nhl", "sports gear"])
def _(S):
    def ell(cx, cy):
        return poly(epoly(cx, cy, 8, 3.5, 12), closed=True) if S.name == "line" else path_to_d(P(ellipse(cx, cy, 8, 3.5)))
    body = path_to_d(U(P(ell(12, 9)), P(rect(4, 9, 16, 6)), P(ell(12, 15))))
    return [shell(body), detail(ell(12, 9))]


@icon("goalie-mask", CAT, "Front of a goalie mask with a wire cage over the face opening",
      tags=["hockey", "goaltender", "face mask", "helmet", "cage", "protection", "ice hockey"], aliases=["goalie-helmet"])
def _(S):
    mask = poly([(5, 6), (8, 3), (16, 3), (19, 6), (19, 15), (16, 21), (8, 21), (5, 15)], closed=True, r=S.r)
    return [
        shell(mask),
        detail(rect(8, 8.5, 8, 6, pick(S, 0.5, 2))),
        detail(seg(10.7, 8.5, 10.7, 14.5)), detail(seg(13.3, 8.5, 13.3, 14.5)),
    ]


@icon("hockey-goal", CAT, "Low hockey goal frame with its net seen at an angle",
      tags=["goal", "net", "ice hockey", "frame", "rink", "goaltender", "winter sports"])
def _(S):
    return [
        line(poly([(3, 20), (3, 9), (15, 9), (15, 20)], r=S.r)),
        line(poly([(3, 9), (8, 4.5), (20, 4.5), (20, 15), (15, 20)], r=S.r)),
        line(seg(15, 9, 20, 4.5)), line(seg(3, 14.5, 15, 14.5)),
    ]


@icon("ice-rink", CAT, "Top view of a rounded rink with a center line and center circle",
      tags=["rink", "hockey rink", "skating rink", "ice", "arena", "face-off", "winter sports"])
def _(S):
    return [
        shell(rect(2.5, 5, 19, 14, pick(S, 2, 6))),
        detail(seg(12, 5, 12, 19)), detail(circle(12, 12, 3.2)),
        detail(seg(6.5, 5, 6.5, 19)), detail(seg(17.5, 5, 17.5, 19)),
    ]


@icon("bandy-stick", CAT, "Curved bandy stick with a small ball on the ice",
      tags=["bandy", "stick", "ball", "ice", "winter sports", "rink", "hockey"])
def _(S):
    return [
        line("M18.5 3L10.5 17.5C9.6 19.3 7.6 19.8 5 19.5"),
        dot(17, 19, 2.2),
    ]


@icon("floorball-stick", CAT, "Floorball stick with a flat blade and a perforated ball",
      tags=["floorball", "unihockey", "stick", "ball", "indoor", "school sport", "hockey"], aliases=["unihockey-stick"])
def _(S):
    return [
        line(seg(12.5, 3, 8, 16.5)),
        shell(rect(2.5, 16.5, 9.5, 4.5, min(S.R, 1.5))),
        shell(circle(18, 17.5, 3.5)), dot(18, 17.5, 0.9),
    ]


@icon("ringette-ring", CAT, "Rubber ring on the ice with a straight stick tip inside it",
      tags=["ringette", "ring", "stick", "ice", "winter sports", "team sport", "rink"])
def _(S):
    return [
        line(poly(epoly(10, 17, 7, 3.6, 12), closed=True) if S.name == "line" else path_to_d(P(ellipse(10, 17, 7, 3.6)))),
        line(seg(21, 3, 10.5, 16.5)),
    ]


@icon("broomball", CAT, "Player swinging a broom-headed stick at a ball on the ice",
      tags=["broom ball", "ice", "winter sports", "broom", "ball", "team sport", "rink"])
def _(S):
    return [
        head(7, 5),
        line(poly([(7.5, 8.5), (8.5, 14)], r=S.r)),
        line(poly([(8.5, 14), (12, 16.5), (12, 20.5)], r=S.r)),
        line(poly([(8.5, 14), (5, 17), (3.5, 20.5)], r=S.r)),
        line(poly([(8, 9.5), (13.5, 11.5), (17, 15)], r=S.r)),
        shell(poly(obox(18.5, 17, 3.2, 1.6, -45), closed=True, r=0)),
        dot(21, 8, 1.6),
    ]


@icon("underwater-hockey", CAT, "Swimmer with a snorkel pushing a puck along the pool floor",
      tags=["octopush", "snorkel", "puck", "pool", "stick", "swimming", "team sport"], aliases=["octopush"])
def _(S):
    return [
        line(poly([(2.5, 12), (9, 11.5), (11, 11)], r=S.r)),
        head(13.5, 10.5),
        line(poly([(13.5, 8), (13.5, 3.5), (17.5, 3.5)], r=S.r)),
        line(poly([(10, 12.5), (13, 16), (17, 17)], r=S.r)),
        shell(rect(18.5, 16.5, 3.5, 2.2, 0.8)),
        line(seg(2.5, 21.5, 21.5, 21.5)),
    ]


@icon("gaelic-football", CAT, "Runner solo-bouncing a round ball off the hand",
      tags=["gaelic", "football", "ball", "solo", "field sport", "ireland", "running"])
def _(S):
    return [
        head(13, 4.5),
        line(poly([(12.5, 8), (11, 14)], r=S.r)),
        line(poly([(11, 14), (15, 16), (16.5, 20)], r=S.r)),
        line(poly([(11, 14), (7.5, 16), (4.5, 19.5)], r=S.r)),
        line(poly([(12, 9), (16, 11)], r=S.r)),
        shell(circle(20, 9, 2.2)),
    ]


@icon("sepak-takraw", CAT, "Player in an overhead scissor kick at a ball above the net",
      tags=["kick volleyball", "takraw", "net", "ball", "acrobatic", "southeast asia", "team sport"])
def _(S):
    return [
        head(4.5, 9),
        line(poly([(7.5, 8.5), (13, 6)], r=S.r)),
        line(poly([(13, 6), (16, 4.5), (17.5, 3.5)], r=S.r)), shell(circle(20.5, 3.5, 1.5)),
        line(poly([(13, 6), (16.5, 8.5), (20, 8)], r=S.r)),
        line(seg(2.5, 14.5, 21.5, 14.5)),
        line(seg(2.5, 14.5, 2.5, 21.5)), line(seg(21.5, 14.5, 21.5, 21.5)),
        line(seg(9, 14.5, 9, 21.5)), line(seg(15, 14.5, 15, 21.5)),
    ]


@icon("mountaineering", CAT, "Climber with a backpack planting an ice axe",
      tags=["alpine", "ice axe", "backpack", "summit", "expedition", "climbing", "mountain"])
def _(S):
    return [
        head(10, 4.5),
        line(poly([(10, 8), (10, 14)], r=S.r)),
        line(poly([(10, 14), (7, 17.5), (7, 21)], r=S.r)),
        line(poly([(10, 14), (13, 17.5), (13.5, 21)], r=S.r)),
        shell(rect(4.5, 8, 3.2, 6, 1)),
        line(poly([(10, 9.5), (15, 11)], r=S.r)),
        line(seg(16, 8, 16, 21)), line(seg(13.5, 7.8, 18.5, 8.4)),
    ]


def star_pts(cx, cy, ro, ri):
    out = []
    for i in range(10):
        r = ro if i % 2 == 0 else ri
        out.append(polar(cx, cy, r, -90 + i * 36))
    return out


# ============================================================================ land sports

@icon("orienteering", CAT, "Runner with a map in hand beside a hanging control marker",
      tags=["orienteer", "map", "control flag", "navigation", "running", "compass", "outdoor sport"])
def _(S):
    return [
        head(6, 6),
        line(poly([(6, 9.5), (6.5, 14.5)], r=S.r)),
        line(poly([(6.5, 14.5), (10, 17), (10.5, 21)], r=S.r)),
        line(poly([(6.5, 14.5), (3.5, 17.5), (3, 21)], r=S.r)),
        line(poly([(6, 10.5), (9.5, 12)], r=S.r)),
        shell(rect(9.5, 9, 4, 5, min(S.R, 1))),
        shell(rect(16.5, 3.5, 5, 5, 0)), detail(seg(16.5, 8.5, 21.5, 3.5)),
        line(seg(19, 8.5, 19, 21)),
    ]


@icon("trail-running", CAT, "Runner on a winding trail with a hill behind",
      tags=["trail run", "running", "off road", "hill", "path", "ultra", "outdoor"], aliases=["trail-run"])
def _(S):
    return [
        head(8, 5),
        line(poly([(8, 8.5), (8.5, 13.5)], r=S.r)),
        line(poly([(8.5, 13.5), (12, 15.5), (12.5, 18.5)], r=S.r)),
        line(poly([(8.5, 13.5), (5, 15.5), (3.5, 18.5)], r=S.r)),
        line(poly([(8, 9.5), (11.5, 11.5)], r=S.r)),
        line(poly([(3.5, 21.5), (11.5, 21.5)], r=S.r)),
        line(poly([(14, 20), (17.5, 9), (21.5, 20)], r=S.r)),
    ]


@icon("parkour", CAT, "Athlete vaulting a wall with one hand planted on top",
      tags=["free running", "vault", "wall", "urban", "freerunning", "jump", "obstacle"], aliases=["freerunning"])
def _(S):
    return [
        head(6, 6.5),
        line(poly([(9, 8.5), (15, 9.5)], r=S.r)),
        line(seg(9.5, 9, 11.5, 12.5)),
        line(poly([(15, 9.5), (18.5, 7.5), (21.5, 4.5)], r=S.r)),
        line(poly([(15, 9.5), (19, 12.5), (20.5, 16)], r=S.r)),
        shell(rect(8, 13, 7, 8, min(S.R, 1.5))),
    ]


@icon("belay", CAT, "Climber on a rock face with a partner below holding the rope",
      tags=["belaying", "climbing", "rope", "partner", "rock face", "safety", "climber"], aliases=["belaying"])
def _(S):
    return [
        line(seg(21.5, 2.5, 21.5, 21.5)),
        head(16, 5), line(poly([(16, 8.5), (16, 13.5)], r=S.r)),
        line(poly([(13, 4), (16, 9)], r=S.r)),
        line(poly([(16, 13.5), (13.5, 17)], r=S.r)),
        head(6, 12),
        line(poly([(6, 15.5), (6, 19)], r=S.r)),
        line(poly([(6, 19), (4, 21.5)], r=S.r)), line(poly([(6, 19), (8.5, 21.5)], r=S.r)),
        line(poly([(15.5, 11.5), (11.5, 14), (8, 16)], r=S.r)),
    ]


@icon("skateboarding", CAT, "Skater riding a skateboard with arms out for balance",
      tags=["skater", "skate", "board", "street", "trick", "ride", "skatepark"])
def _(S):
    return [
        head(12, 4.5),
        line(poly([(12, 8), (12, 13.5)], r=S.r)),
        line(poly([(4.5, 12), (12, 9), (19.5, 12)], r=S.r)),
        line(poly([(12, 13.5), (9, 17)], r=S.r)), line(poly([(12, 13.5), (15, 17)], r=S.r)),
        line(poly([(2.5, 17.5), (4.5, 19.5), (19.5, 19.5), (21.5, 17.5)], r=S.r)),
        dot(7, 21.3, 1.2), dot(17, 21.3, 1.2),
    ]


@icon("half-pipe", CAT, "U-shaped ramp with a flat bottom and rounded copings at both lips",
      tags=["halfpipe", "ramp", "skatepark", "snowboard", "vert", "skate", "bmx"])
def _(S):
    pts = [(3.5, 5), (3.5, 11.5), (6, 16.5), (9.5, 19), (14.5, 19), (18, 16.5), (20.5, 11.5), (20.5, 5)]
    return [
        line(seam(S, pts)),
        dot(3.5, 4, 1.6), dot(20.5, 4, 1.6),
    ]


@icon("inline-skate", CAT, "Skate boot with a single line of four wheels underneath",
      tags=["rollerblade", "inline skates", "roller", "wheels", "boot", "skating", "fitness"], aliases=["rollerblade"])
def _(S):
    return [
        shell(poly([(5, 3), (11, 3), (11.5, 8.5), (17.5, 10.5), (20.5, 13), (20.5, 16.5), (5, 16.5)], closed=True, r=S.r)),
        detail(seg(5.5, 7, 11, 7)),
        dot(6.3, 20, 1.7), dot(10.5, 20, 1.7), dot(14.7, 20, 1.7), dot(18.9, 20, 1.7),
    ]


@icon("roller-skating", CAT, "Skater gliding on quad skates with arms swinging",
      tags=["roller skater", "quad skates", "disco", "rink", "skate", "glide", "fitness"])
def _(S):
    return [
        head(12, 4.5),
        line(poly([(12, 8), (12, 13.5)], r=S.r)),
        line(poly([(5.5, 12.5), (12, 9.5), (18.5, 6.5)], r=S.r)),
        line(poly([(12, 13.5), (16, 16), (16.5, 18.5)], r=S.r)),
        line(poly([(12, 13.5), (8, 16), (6.5, 18.5)], r=S.r)),
        dot(14.8, 21, 1.2), dot(18.2, 21, 1.2), dot(4.8, 21, 1.2), dot(8.2, 21, 1.2),
    ]


@icon("roller-derby", CAT, "Crouched skater with a star on the helmet and knee pads",
      tags=["derby", "skater", "helmet", "knee pads", "quad skates", "contact sport", "rink"])
def _(S):
    return [
        shell(circle(15, 6, 4)), Part("dot", poly(star_pts(15, 6, 2.5, 1.1), closed=True)),
        line(seg(12.5, 10.5, 8.5, 14)),
        line(poly([(8.5, 14), (12.5, 16.5), (12.5, 19)], r=S.r)),
        line(poly([(8.5, 14), (5.5, 16.5), (4, 19)], r=S.r)),
        dot(12.5, 16.5, 1.8), dot(5.5, 16.5, 1.8),
        line(seg(11.5, 11.5, 17, 14)),
        dot(11.5, 21.3, 1.1), dot(14.5, 21.3, 1.1), dot(2.5, 21.3, 1.1), dot(5.5, 21.3, 1.1),
    ]


@icon("skate-ramp", CAT, "Wedge ramp with a flat top and a long sloping face",
      tags=["ramp", "kicker", "jump", "skatepark", "wedge", "launch", "bmx"], aliases=["kicker-ramp"])
def _(S):
    return [
        shell(poly([(3, 20), (3, 9), (11, 9), (21, 20)], closed=True, r=S.r)),
        detail(seg(7, 12.5, 7, 20)), detail(seg(11, 13, 11, 20)),
    ]


# ============================================================================ wheels and motors

@icon("bmx-trick", CAT, "Rider in the air lifting a small bike over a dirt jump",
      tags=["bmx", "freestyle", "jump", "air", "stunt", "bike", "dirt"])
def _(S):
    return [
        line(ring(S, 9, 14, 3, 10)), line(ring(S, 20, 10.5, 3, 10)),
        line(poly([(9, 14), (12.5, 11), (20, 10.5)], r=S.r)),
        head(12.5, 4), line(poly([(12.5, 7.5), (12.5, 11)], r=S.r)),
        line(seg(13, 8.5, 18, 8)),
        shell(poly([(2.5, 21.5), (8, 21.5), (8, 19)], closed=True, r=S.r)),
    ]


@icon("track-cycling", CAT, "Rider tucked low on a track bike beside a banked curve",
      tags=["velodrome", "fixed gear", "track bike", "sprint", "cycling", "race", "banked track"])
def _(S):
    return [
        line(ring(S, 6.5, 14, 3.5, 10)), line(ring(S, 17.5, 14, 3.5, 10)),
        line(poly([(6.5, 14), (10, 9.5), (15.5, 9.5), (17.5, 14)], r=S.r)),
        head(17.5, 4.8),
        line(poly([(10, 8.5), (14, 6.5)], r=S.r)),
        line(seg(14, 6.5, 16.5, 9.5)),
        line(seg(2.5, 21.5, 21.5, 19.5)),
    ]


@icon("peloton", CAT, "Tight pack of cyclists riding together",
      tags=["pack", "group ride", "cycling", "road race", "tour", "bunch", "cyclists"])
def _(S):
    return [
        head(5, 5.5), line(poly([(2.5, 10), (5, 9), (7.5, 10)], r=S.r)), line(seg(5, 12.5, 5, 19)),
        head(19, 5.5), line(poly([(16.5, 10), (19, 9), (21.5, 10)], r=S.r)), line(seg(19, 12.5, 19, 19)),
        head(12, 9), line(poly([(8, 14), (12, 12.5), (16, 14)], r=S.r)), line(seg(12, 15.5, 12, 21.5)),
    ]


@icon("cyclocross", CAT, "Runner carrying a bike on one shoulder",
      tags=["cyclo-cross", "bike carry", "run with bike", "mud", "off road", "cycling", "race"], aliases=["cyclo-cross"])
def _(S):
    return [
        head(8, 5),
        line(poly([(8, 8.5), (8, 14)], r=S.r)),
        line(poly([(8, 14), (11.5, 16.5), (11.5, 21)], r=S.r)),
        line(poly([(8, 14), (5, 17), (4, 21)], r=S.r)),
        line(poly([(8, 9.5), (13, 9), (16.5, 11.5)], r=S.r)),
        line(ring(S, 13.5, 7, 3, 10)), line(ring(S, 19, 16.5, 3, 10)),
        line(seg(13.5, 7, 19, 16.5)),
    ]


@icon("bike-trainer", CAT, "Rear bike wheel clamped on an indoor trainer stand",
      tags=["indoor cycling", "turbo trainer", "stand", "rollers", "workout", "bicycle", "training"])
def _(S):
    return [
        line(ring(S, 12, 9.5, 6.5, 12)), dot(12, 9.5, 1.3),
        line(seg(12, 9.5, 18.5, 3.5)),
        shell(ring(S, 12, 19.2, 1.8, 8)),
        line(poly([(3.5, 21.5), (12, 19.2), (20.5, 21.5)], r=S.r)),
    ]


@icon("cycling-shoes", CAT, "Low stiff shoe with a cleat plate under the sole and a dial closure",
      tags=["clipless", "cleats", "road shoes", "bike shoes", "dial", "cycling", "footwear"], aliases=["cycling-shoe"])
def _(S):
    return [
        shell(poly([(3, 6.5), (9, 6.5), (10, 10), (17, 11.5), (21, 14), (21, 17), (3, 17)], closed=True, r=S.r)),
        dot(6.5, 10.8, 1.3),
        detail(seg(11.5, 12, 14, 15)),
        shell(rect(9, 17.5, 6, 3, min(S.R, 1))),
    ]


@icon("racing-helmet", CAT, "Full-face racing helmet with a wide visor, side view",
      tags=["motorsport", "full face", "visor", "race driver", "karting", "safety", "crash helmet"], aliases=["full-face-helmet"])
def _(S):
    shape = poly([(3, 13), (4, 8), (9, 4), (15, 3.5), (20, 6.5), (21.5, 11.5), (21.5, 18), (17, 20), (10, 20), (5, 17.5)],
                 closed=True, r=S.r)
    shape = poly([(3, 15), (3.5, 10), (7, 5.5), (12, 3.5), (17, 4.5), (20.5, 8), (21.5, 12.5), (21.5, 19), (17, 20), (8, 20), (4.5, 18.5)],
                 closed=True, r=S.r)
    return [
        shell(shape),
        Part("dot", rect(10.5, 8.5, 9, 5.5, pick(S, 0.5, 2.2))),
        detail(seg(11, 17, 17, 17)),
    ]


@icon("pit-stop", CAT, "Wheel with a wheel gun held against the hub nut",
      tags=["pit crew", "tire change", "wheel nut", "impact wrench", "motorsport", "racing", "garage"])
def _(S):
    return [
        shell(ring(S, 8, 13, 6.5, 12)), detail(ring(S, 8, 13, 2.4, 8)),
        line(seg(10, 13, 15, 13)),
        shell(rect(15.5, 9.5, 6.5, 6, min(S.R, 1.5))),
        line(poly([(19, 15.5), (18, 20.5)], r=S.r)),
    ]


@icon("motocross", CAT, "Rider on a dirt bike flying nose up over a jump",
      tags=["dirt bike", "motorbike", "mx", "jump", "off road", "freestyle", "motorsport"])
def _(S):
    return [
        line(ring(S, 8, 15.5, 3.2, 10)), line(ring(S, 19.5, 10, 3.2, 10)),
        line(poly([(8, 15.5), (12, 13), (16, 12), (19.5, 10)], r=S.r)),
        head(12.5, 5), line(poly([(12.5, 8.5), (11.5, 12.5)], r=S.r)),
        line(seg(12.5, 9.5, 17, 9)),
        shell(poly([(2.5, 21.5), (7, 21.5), (7, 19.5)], closed=True, r=S.r)),
    ]


# ============================================================================ riding

def F(k, ox, oy):
    return lambda x, y: (ox + k * x, oy + k * y)


def T(f, pts):
    return [f(*p) for p in pts]


HORSE = [(4, 11), (10, 10.5), (14, 10.5), (15.5, 6.5), (18.5, 4.5), (21.5, 8.5), (20, 10), (18, 9.5), (17, 13),
         (15, 15.5), (6.5, 15.5), (4, 13.5)]
WALK = [[(5.5, 15), (4.5, 21.5)], [(8.5, 15), (9.5, 21.5)], [(13.5, 15), (12.5, 21.5)], [(16, 15), (18, 21)]]


def horse_parts(S, f, legs, body=HORSE):
    parts = [shell(poly(T(f, body), closed=True, r=pick(S, 0.8, 1.8)))]
    for lg in legs:
        parts.append(line(poly(T(f, lg), r=S.r)))
    return parts


@icon("horse-riding", CAT, "Rider sitting upright on a walking horse, side view",
      tags=["equestrian", "horseback", "rider", "pony", "stable", "trail ride", "saddle"], aliases=["horseback-riding"])
def _(S):
    f = F(1, 0, 0)
    return horse_parts(S, f, WALK) + [
        head(9.5, 4.5), line(poly([(9.5, 8), (9.5, 10)], r=S.r)),
        line(poly([(9.5, 8.5), (13, 9), (15, 8)], r=S.r)),
    ]


@icon("show-jumping", CAT, "Horse and rider leaping over a fence of horizontal poles",
      tags=["jumping", "equestrian", "fence", "horse", "rider", "hurdle", "competition"], aliases=["horse-jumping"])
def _(S):
    f = F(1, 0, -3)
    legs = [[(5.5, 15), (3.5, 17.5), (2.5, 16.5)], [(8.5, 15), (6.5, 18.5)],
            [(13.5, 15), (17.5, 15.5), (19, 14)], [(16, 15), (20, 16.5)]]
    return horse_parts(S, f, legs) + [
        head(9.5, 4), line(poly([(9.5, 7.5), (9.5, 8.5)], r=S.r)),
        line(seg(2.5, 18.5, 21.5, 18.5)),
        line(seg(2.5, 18.5, 2.5, 21.5)), line(seg(21.5, 18.5, 21.5, 21.5)),
    ]


DRESS = [(4, 11.5), (10, 11), (14, 11), (14.5, 6.5), (17, 4), (20, 5.5), (20.5, 8.5), (21.5, 11.5), (19.5, 12), (18.5, 9),
         (17.5, 9.5), (17, 13), (15, 15.5), (6.5, 15.5), (4, 14)]


@icon("dressage", CAT, "Horse with an arched neck high stepping with a rider in a top hat",
      tags=["equestrian", "horse", "rider", "top hat", "high step", "arena", "competition"])
def _(S):
    f = F(1, 0, 0.5)
    legs = [[(5.5, 15), (4.5, 20.5)], [(8.5, 15), (9.5, 20.5)], [(13.5, 15), (12.5, 20.5)], [(16, 15), (19.5, 14.5), (20, 17.5)]]
    return horse_parts(S, f, legs, DRESS) + [
        head(9.5, 6.2), line(seg(7.2, 3.6, 11.8, 3.6)), solid(rect(8.3, 1.8, 2.4, 2)),
        line(poly([(9.5, 9.5), (9.5, 10.5)], r=S.r)),
        line(poly([(9.5, 9.5), (13, 10), (15, 9.5)], r=S.r)),
    ]


BULL = [(4, 11.5), (9, 10), (13, 8.5), (16, 10), (19, 11.5), (21.5, 15), (20.5, 17.5), (18.5, 15.5), (16.5, 15.5),
        (6.5, 15.5), (4, 14)]


@icon("rodeo", CAT, "Rider with one arm raised on a bucking bull",
      tags=["bull riding", "cowboy", "bucking", "western", "bull", "arena", "stampede"], aliases=["bull-riding"])
def _(S):
    f = F(1, 0, 0)
    legs = [[(5.5, 15), (3, 18.5), (2.5, 16)], [(9, 15), (8.5, 21)], [(14, 15), (15.5, 21)],
            [(19, 11.5), (22, 9)]]
    return horse_parts(S, f, legs, BULL) + [
        head(9.5, 3.8), line(poly([(9.5, 7), (9.5, 9)], r=S.r)),
        line(poly([(9.5, 7.5), (12.5, 4.5), (15, 3)], r=S.r)), line(poly([(9.5, 8), (13, 8.5)], r=S.r)),
    ]


@icon("barrel-racing", CAT, "Horse and rider turning tightly around a barrel",
      tags=["barrel", "rodeo", "western", "horse", "rider", "turn", "arena"])
def _(S):
    f = F(0.7, 0.5, 5.5)
    legs = [[(5.5, 15), (3.5, 21.5)], [(10, 15), (10, 21.5)], [(15, 15), (17, 21.5)]]
    x = f(9.5, 0)[0]
    return horse_parts(S, f, legs) + [
        head(x, 5.2), line(poly([(x, 8.5), (x, 12)], r=S.r)),
        shell(rect(17, 11, 4.5, 10, min(S.R, 1.5))), detail(seg(17, 16, 21.5, 16)),
    ]


@icon("harness-racing", CAT, "Trotting horse pulling a driver in a light two-wheeled cart",
      tags=["trotting", "sulky", "horse racing", "cart", "driver", "trotter", "race"])
def _(S):
    f = F(0.65, 8, 7.5)
    legs = [[(5.5, 15), (3.5, 21.5)], [(10, 15), (10, 21.5)], [(15, 15), (18, 21)]]
    return horse_parts(S, f, legs) + [
        line(ring(S, 6, 18, 3.2, 10)),
        line(poly([(2.5, 13), (8.5, 13), (12.5, 14)], r=S.r)),
        head(5, 6.5), line(poly([(5, 10), (5, 13)], r=S.r)),
    ]


CAMEL = [(4, 11.5), (9, 11), (10.5, 7.5), (13, 7.5), (14.5, 11), (16, 11), (17, 6), (19, 4), (21.5, 5.5), (21.5, 7.5),
         (19.5, 7), (19, 12), (17.5, 13.5), (15.5, 15.5), (6.5, 15.5), (4, 14)]


@icon("camel-racing", CAT, "Jockey crouched on a galloping camel",
      tags=["camel", "desert", "jockey", "gallop", "race", "arabia", "animal sport"])
def _(S):
    f = F(1, 0, 0)
    legs = [[(6, 15), (3.5, 18.5), (2.5, 20.5)], [(8.5, 15), (6.5, 19), (5, 21.5)],
            [(13.5, 15), (16.5, 18.5), (19.5, 19.5)], [(15.5, 15), (18, 19), (20, 21)]]
    return horse_parts(S, f, legs, CAMEL) + [
        head(14.5, 3.8), line(poly([(11, 6), (13, 5.5)], r=S.r)),
    ]
