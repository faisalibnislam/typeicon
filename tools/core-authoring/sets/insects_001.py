"""TypeIcon Core: insects (batch 001).

Bees and beekeeping, ants and wasps, moths and butterflies, life stages, beetles, flies and dragonflies.
Top views are symmetric with the head up; side views face left.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "insects"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def clip(a, b):
    return path_to_d(I(P(a), P(b)))


def rot(d, deg, cx=12, cy=12):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpts(pts, deg, cx=12, cy=12):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def thick(d, w, S):
    return path_to_d(ST(d, w, S.cap, S.join))


def flip(d):
    """Mirror a d-string across the vertical centre line."""
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def fpts(pts):
    return [(24 - x, y) for x, y in pts]


def grow(d, g):
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled body."""
    return Part("dot", d)


def _p(p):
    return f"{fmt(p[0])} {fmt(p[1])}"


def tip(a, p, b, r):
    """Corner at p (from a, towards b): sharp when r == 0, softened with a quadratic when r > 0."""
    if r <= 0:
        return "L" + _p(p)
    la = math.hypot(a[0] - p[0], a[1] - p[1])
    lb = math.hypot(b[0] - p[0], b[1] - p[1])
    t = min(r, la / 2, lb / 2)
    s = (p[0] + (a[0] - p[0]) * t / la, p[1] + (a[1] - p[1]) * t / la)
    e = (p[0] + (b[0] - p[0]) * t / lb, p[1] + (b[1] - p[1]) * t / lb)
    return "L" + _p(s) + "Q" + _p(p) + " " + _p(e)


def tri(S, pts, r=0.8):
    return poly(pts, closed=True, r=L(S, 0, r))


def wing(cx, cy, rx, ry, deg):
    return rot(ellipse(cx, cy, rx, ry), deg, cx, cy)


def lens(S, cx, cy, rx, ry, deg=0):
    """Wing shape: pointed lens in Line, ellipse in Rounded (rotated deg about its centre)."""
    if S.name == "line":
        d = (f"M{fmt(cx - rx)} {fmt(cy)}Q{fmt(cx)} {fmt(cy - 2 * ry)} {fmt(cx + rx)} {fmt(cy)}"
             f"Q{fmt(cx)} {fmt(cy + 2 * ry)} {fmt(cx - rx)} {fmt(cy)}Z")
    else:
        d = ellipse(cx, cy, rx, ry)
    return rot(d, deg, cx, cy)


def cut_wing(w, *bodies, g=1.0):
    """Wing outline with the part hidden under the body removed (clean join)."""
    return minus(w, *[grow(b, g) for b in bodies])


def pair(d):
    return [d, flip(d)]


def band(body, y0, y1):
    """Solid stripe across a body between two y values."""
    return mark(clip(body, rect(0, y0, 24, y1 - y0)))


def dots_on(pts_fn, n, skip=lambda x, y: False, r=0.9):
    out = []
    for i in range(n):
        x, y = pts_fn(i / n)
        if not skip(x, y):
            out.append(dot(x, y, r))
    return out


def bee_side(S, cx, cy, k=1.0, wings=True):
    """Small side view bee facing left: solid striped body with an outlined wing (parts list)."""
    body = union(ellipse(cx, cy, 4.3 * k, 2.9 * k), circle(cx - 4.5 * k, cy + 0.1 * k, 1.8 * k))
    body = minus(body, rect(cx - 1.6 * k, cy - 4, 1.0 * k, 8), rect(cx + 1.2 * k, cy - 4, 1.0 * k, 8))
    parts = [solid(body)]
    if wings:
        w = cut_wing(wing(cx + 2.0 * k, cy - 4.2 * k, 1.5 * k, 2.8 * k, 32), union(ellipse(cx, cy, 4.3 * k, 2.9 * k)), g=1.6)
        parts.insert(0, shell(w))
    return parts


def hexagon(cx, cy, r, start=-90):
    return poly(regular(cx, cy, r, 6, start), closed=True)


# ============================================================================ bees, wasps, beekeeping

@icon("wasp", CAT, "Top view of a wasp with a pinched waist and a striped pointed abdomen",
      tags=["hornet", "yellowjacket", "sting", "insect", "stinging insect", "pest"])
def _(S):
    head = circle(12, 5.2, 2)
    thorax = ellipse(12, 9.6, 2.4, 2.2)
    abd = L(S, "M12 12.4C15.6 12.8 16 17 12 21.8C8 17 8.4 12.8 12 12.4Z",
            "M12 12.4C15.6 12.8 16 17 13.3 21C12.6 21.8 11.4 21.8 10.7 21C8 17 8.4 12.8 12 12.4Z")
    w = cut_wing(wing(6.4, 11.2, 4.4, 1.7, -30), thorax)
    return [shell(w), shell(flip(w)), shell(union(head, thorax)), shell(abd), band(abd, 15.2, 16.8), band(abd, 18.2, 19.4),
            line(poly([(11, 3.6), (9.2, 1.8)], r=S.r)), line(poly([(13, 3.6), (14.8, 1.8)], r=S.r))]


@icon("queen-bee", CAT, "Top view of a long-bodied bee with a small crown above its head",
      tags=["queen", "hive", "royal", "bee", "crown", "insect", "honey"])
def _(S):
    r = L(S, 0, 0.5)
    crown = poly([(8.6, 5.2), (8, 2.4), (10.4, 3.8), (12, 2), (13.6, 3.8), (16, 2.4), (15.4, 5.2)], closed=True, r=r)
    head = circle(12, 8, 1.9)
    thorax = ellipse(12, 12, 2.6, 2.1)
    abd = ellipse(12, 17.6, 3.2, 4.6)
    w = cut_wing(wing(6.6, 12.6, 4, 1.6, -28), thorax)
    return [shell(crown), shell(w), shell(flip(w)), shell(union(head, thorax)), shell(abd), band(abd, 16.2, 17.8), band(abd, 19.4, 20.6)]


@icon("bee-swarm", CAT, "Teardrop cluster of bees hanging from a branch",
      tags=["swarm", "bees", "cluster", "hive", "branch", "colony", "insects"])
def _(S):
    cl = L(S, "M6.8 4C5.4 9.5 7 15 12 21.4C17 15 18.6 9.5 17.2 4Z",
           "M6.8 4C5.4 9.5 7 15 10.8 20.4C11.5 21.4 12.5 21.4 13.2 20.4C17 15 18.6 9.5 17.2 4Z")
    return [line(poly([(2.5, 3), (21.5, 3)])), shell(cl), dot(9.6, 8, 1), dot(14.4, 8, 1), dot(12, 11.3, 1),
            dot(10.3, 14.3, 1), dot(13.7, 14.3, 1), dot(12, 17.3, 0.9),
            dot(3.6, 10, 1), dot(20.4, 12, 1), dot(4.6, 16.2, 1), dot(19.4, 18, 1)]


@icon("wild-honeycomb", CAT, "Three long sheets of honeycomb hanging from a tree branch",
      tags=["comb", "wild hive", "honey", "branch", "bees", "nest", "beeswax"])
def _(S):
    sheets = [rect(2.8, 4.5, 3.6, 11.5, L(S, 1.4, 1.8)), rect(10.2, 4.5, 3.6, 15.5, L(S, 1.4, 1.8)), rect(17.6, 4.5, 3.6, 12.5, L(S, 1.4, 1.8))]
    parts = [line(seg(2, 3, 22, 3))] + [shell(s) for s in sheets]
    for x, ys in ((4.6, (8.6, 12.4)), (12, (8.6, 12.4, 16.2)), (19.4, (8.6, 12.8))):
        for y in ys:
            parts.append(dot(x, y, 0.75))
    return parts


@icon("hive-box", CAT, "Stacked wooden bee hive with a flat lid and an entrance slot at the base",
      tags=["beehive", "apiary", "langstroth", "bees", "beekeeping", "honey", "box"])
def _(S):
    body = rect(4.5, 8.5, 15, 11, L(S, 1, 2))
    return [shell(rect(2.5, 3.5, 19, 3.5, L(S, 1, 1.8))), shell(body), detail(seg(4.5, 14, 19.5, 14)), mark(rect(9, 16.3, 6, 1.4, 0.5)),
            line(seg(2.5, 21.6, 21.5, 21.6))]


@icon("hive-frame", CAT, "Wooden hive frame with hexagonal comb cells and lugs at both top corners",
      tags=["frame", "comb", "hexagon", "honey", "beekeeping", "super", "cells"])
def _(S):
    outer = rect(4, 7, 16, 14, L(S, 1, 2))
    bar = rect(1.5, 3.5, 21, 3, L(S, 0.5, 1.4))
    cells = [hexagon(9.3, 11.3, 2.6, 0), hexagon(14.9, 11.3, 2.6, 0), hexagon(12.1, 16.1, 2.6, 0)]
    return [shell(bar), shell(outer)] + [mark(c) if False else detail(c) for c in cells]


@icon("top-bar-hive", CAT, "Side view of a trapezoid bee hive on legs with a pitched roof and an entrance hole",
      tags=["kenyan hive", "beehive", "apiary", "bees", "beekeeping", "legs", "roof"])
def _(S):
    box = poly([(4, 10), (20, 10), (17.4, 17), (6.6, 17)], closed=True, r=S.r)
    return [line(poly([(2, 8), (12, 2.8), (22, 8)], r=S.r)), shell(box), dot(12, 13.4, 1.4),
            line(seg(7.5, 17, 6.3, 21.6)), line(seg(16.5, 17, 17.7, 21.6))]


@icon("bee-smoker", CAT, "Metal smoker can with a conical spout puffing smoke and a small bellows on the side",
      tags=["beekeeping", "smoke", "apiary", "bellows", "calm bees", "tool", "hive tool"])
def _(S):
    can = union(rect(3.5, 13, 9, 7.5, L(S, 1, 2)), poly([(3.5, 13.5), (6.2, 9), (9.8, 9), (12.5, 13.5)], closed=True))
    bel = poly([(12.5, 13.6), (21.5, 11.5), (21.5, 19), (12.5, 18.5)], closed=True, r=S.r)
    return [shell(union(can, bel)), detail(seg(16.2, 12.6, 16.2, 18.6)), detail(seg(19, 12.1, 19, 18.8)),
            detail(seg(3.5, 13.5, 12.5, 13.5)),
            line("M8 7C4.6 6.4 5.6 3 9 3.4C12 3.8 12.6 1.6 10.2 1.8")]


@icon("beekeeper-veil", CAT, "Wide brimmed hat with a bell-shaped mesh veil hanging from it",
      tags=["bee veil", "beekeeping", "protective", "hat", "mesh", "apiary", "netting"])
def _(S):
    veil = "M5 8C4 13 3.6 17 4 21.5L20 21.5C20.4 17 20 13 19 8Z"
    return [shell("M7 8C7 2.4 17 2.4 17 8Z"), line(seg(2.2, 8, 21.8, 8)),
            shell(veil), detail(seg(7.2, 12, 16.8, 20)), detail(seg(16.8, 12, 7.2, 20))]


@icon("beekeeper", CAT, "Person in a round hat with a mesh face veil and a puffy suit, with a small bee beside them",
      tags=["apiarist", "bee keeper", "protective suit", "honey farmer", "person", "bees", "veil"])
def _(S):
    shoulders = poly([(1.8, 22), (2.2, 19.6), (6, 17.8), (14, 17.8), (17.8, 19.6), (18.2, 22)], closed=True, r=L(S, 0, 2))
    veil = "M4.6 6.4C4.3 10 4.2 12.6 4.6 14.6C5 16.2 15 16.2 15.4 14.6C15.8 12.6 15.7 10 15.4 6.4Z"
    bee = ellipse(20.2, 12.4, 1.9, 1.3)
    bw = cut_wing(wing(20.8, 9.8, 1.0, 1.9, 30), bee, g=0.3)
    return [shell("M6.5 6.4C6.5 1.4 13.5 1.4 13.5 6.4Z"), line(seg(2.2, 6.4, 17.8, 6.4)),
            shell(veil), detail(seg(7.5, 9.2, 12.5, 13.6)), detail(seg(12.5, 9.2, 7.5, 13.6)), shell(shoulders),
            mark(bee), mark(bw)]


@icon("honey-extractor", CAT, "Tall drum on three legs with a crank on top and a tap near the bottom",
      tags=["honey", "centrifuge", "spinner", "harvest", "beekeeping", "crank", "apiary"])
def _(S):
    drum = rect(5.5, 8.5, 12, 8.5, L(S, 1, 2.5))
    return [shell(drum), detail(seg(5.5, 11, 17.5, 11)), line(seg(11.5, 8.5, 11.5, 4.2)), line(poly([(11.5, 4.2), (17.5, 4.2)], r=S.r)),
            dot(17.8, 4.2, 1.2), line(poly([(17.5, 14.5), (21, 14.5), (21, 17.5)], r=S.r)),
            line(seg(7, 17, 5, 21.5)), line(seg(11.5, 17, 11.5, 21.5)), line(seg(16, 17, 18, 21.5))]


@icon("hive-tool", CAT, "Flat steel pry bar with a bent hook at one end and a wide scraper blade at the other",
      tags=["beekeeping", "pry bar", "scraper", "frame lifter", "apiary", "tool", "hive"])
def _(S):
    pts = [(4, 18), (4, 9.5), (17, 9.5), (21.5, 7.5), (21.5, 16.5), (17, 14.5), (8, 14.5), (8, 18)]
    return [shell(rot(poly(pts, closed=True, r=S.r), -35)), mark(rot(circle(12.4, 12, 0.9), -35))]


def _liss(t, cx=12, cy=12, a=9.6, b=8.6):
    s = math.sin(t)
    d = 1 + s * s
    return cx + a * math.cos(t) / d, cy + b * 2 * s * math.cos(t) / d


@icon("waggle-dance", CAT, "Small bee at the crossing of a dotted figure-eight path showing the waggle dance",
      tags=["bee dance", "communication", "honeybee", "navigation", "figure eight", "foraging", "dance"])
def _(S):
    body = L(S, "M12 7.6C15 8.4 15 14 12 17.2C9 14 9 8.4 12 7.6Z", ellipse(12, 12.4, 2.5, 4.6))
    parts = []
    n = 22
    for i in range(n):
        x, y = _liss(2 * math.pi * (i + 0.5) / n)
        if math.hypot(x - 12, y - 12) > 5.2:
            parts.append(dot(x, y, 0.85))
    w = cut_wing(wing(14.6, 10.2, 1.0, 1.9, 35), body, g=0.4)
    w2 = cut_wing(wing(9.4, 10.2, 1.0, 1.9, -35), body, g=0.4)
    return parts + [shell(body), detail(seg(9.6, 12.4, 14.4, 12.4)), mark(w), mark(w2)]


@icon("pollination", CAT, "Bee flying between two flowers along a dotted arc with pollen dots",
      tags=["pollinate", "pollen", "flowers", "bee", "garden", "nature", "fertilize"])
def _(S):
    parts = bee_side(S, 12.5, 7.6, 0.9)
    for cx in (5, 19):
        petals = union(*[circle(cx + 2.1 * math.cos(math.radians(a)), 16.3 + 2.1 * math.sin(math.radians(a)), 1.7) for a in (0, 90, 180, 270)])
        parts.append(shell(petals))
        parts.append(line(seg(cx, 19.6, cx, 22)))
        parts.append(mark(circle(cx, 16.3, 0.8)))
    for i in range(1, 4):
        t = i / 4
        parts.append(dot(5 + 0 * t + (t * 4.2), 11.8 - 6 * math.sin(t * 1.9) + 0 * t, 0.7)) if False else None
    parts += [dot(5.2, 11.6, 0.75), dot(6.4, 8.8, 0.75), dot(18.6, 11.8, 0.75), dot(17.6, 9, 0.75)]
    return parts


@icon("bee-on-flower", CAT, "Side view of a bee landed on the top of an open daisy flower head",
      tags=["daisy", "pollen", "pollinator", "garden", "spring", "bee", "blossom"])
def _(S):
    petals = union(*[circle(12 + 4.7 * math.cos(math.radians(a)), 16.4 + 4.0 * math.sin(math.radians(a)), 2.1) for a in range(0, 360, 45)])
    parts = bee_side(S, 12.5, 8.6, 0.95)
    return parts + [shell(petals), mark(ellipse(12, 16.4, 2.4, 2))]


# ============================================================================ ants, termites, wasps

def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def legs_pair(S, *chains):
    out = []
    for c in chains:
        out.append(line(poly(c, r=S.r)))
        out.append(line(poly(fpts(c), r=S.r)))
    return out


@icon("flying-ant", CAT, "Top view of an ant with three body segments, bent antennae and two long clear wings on its back",
      tags=["winged ant", "alate", "swarm", "insect", "nuptial flight", "ant", "wings"])
def _(S):
    head = ellipse(12, 5.4, 1.9, 1.7)
    thorax = ellipse(12, 9.4, 1.9, 2.2)
    abd = ellipse(12, 16.8, 2.6, 4.2)
    w = cut_wing(wing(6.2, 14.2, 5.6, 1.7, -66), thorax, abd, g=1.4)
    return [shell(w), shell(flip(w)), shell(head), shell(thorax), shell(abd)] + legs_pair(S, [(10.4, 8.4), (7.6, 6.4), (6.4, 3.8)]) + [
        line(poly([(11, 3.8), (9.8, 2.4), (8, 2.2)], r=S.r)), line(poly([(13, 3.8), (14.2, 2.4), (16, 2.2)], r=S.r))]


def sthick(d, w=1.3):
    """Thin solid stroke (tiny limbs), identical in all three styles."""
    return solid(path_to_d(ST(d, w, "round", "round")))


@icon("leafcutter-ant", CAT, "Side view of an ant carrying a large half-moon leaf piece raised above its back",
      tags=["leaf", "carrying", "fungus farmer", "tropical ant", "insect", "worker", "foraging"])
def _(S):
    leaf = "M5 10C5 4.6 8.6 2.6 12.4 2.6C16.2 2.6 19 4.8 19 10Z"
    body = [solid(circle(5.2, 15, 2.1)), solid(ellipse(10.4, 15.2, 2.5, 1.9)), solid(ellipse(17.6, 15.8, 4, 3.2))]
    return [shell(leaf), detail(seg(12, 10, 12.4, 5)), sthick(seg(5.2, 13.2, 6.4, 10.4)), *body,
            sthick("M9 16.6L7.6 19L6.4 21.5"), sthick("M10.8 17L11.2 19.4L11.6 21.6"), sthick("M13 16.8L15 19.2L16.8 21.6")]


def _ant_mini(S, cx, cy, ang):
    """Tiny top view ant heading along angle (radians) made of solid pieces."""
    head = circle(2.7, 0, 1.0)
    thorax = ellipse(0.7, 0, 1.15, 0.95)
    abd = L(S, "M-0.9 0C-1.2 -1.7 -3.2 -1.9 -4.8 0C-3.2 1.9 -1.2 1.7 -0.9 0Z", ellipse(-2.9, 0, 1.9, 1.5))
    legs = []
    for k, (a, b) in enumerate(((1.3, 2.0), (0.6, 2.3), (-0.1, 2.0))):
        for sgn in (1, -1):
            tx = a + (0.9 if k == 0 else (0 if k == 1 else -1.0))
            legs.append(seg(a, sgn * 0.3, tx, sgn * b))
    c, sn = math.cos(ang), math.sin(ang)
    m = (c, sn, -sn, c, cx, cy)
    out = []
    for d in (head, thorax, abd):
        out.append(solid(path_to_d(transform_path(P(d), m))))
    for lg in legs:
        out.append(solid(path_to_d(transform_path(ST(lg, 0.7, "round", "round"), m))))
    return out


@icon("ant-trail", CAT, "Four small ants marching one after another along a curving dotted path",
      tags=["ants", "line", "march", "colony", "pest", "insects", "path"])
def _(S):
    ctrl = ((2.5, 21), (2.5, 9), (21.5, 15), (21.5, 3))
    parts = []
    for t in (0.1, 0.35, 0.6, 0.86):
        cx, cy = bez(*ctrl, t)
        x2, y2 = bez(*ctrl, t + 0.02)
        x1, y1 = bez(*ctrl, t - 0.02)
        parts += _ant_mini(S, cx, cy, math.atan2(y2 - y1, x2 - x1))
    for t in (0.225, 0.475, 0.73):
        x, y = bez(*ctrl, t)
        parts.append(dot(x, y, 0.65))
    return parts


@icon("ant-colony", CAT, "Soil cross section with a mound on top and branching tunnels leading to two oval chambers",
      tags=["anthill", "ant hill", "nest", "underground", "tunnels", "chambers", "ants"])
def _(S):
    r = L(S, 0, 2)
    soil = ("M2.5 10.5C6.5 10.5 8.3 3 12 3C15.7 3 17.5 10.5 21.5 10.5" + tip((21.5, 10.5), (21.5, 21), (2.5, 21), r)
            + tip((21.5, 21), (2.5, 21), (2.5, 10.5), r) + "Z")
    return [shell(soil), detail(seg(12, 8, 12, 18)), detail(seg(12, 13, 7.5, 13)), detail(seg(12, 18, 16.5, 18)),
            mark(ellipse(6, 13, 2, 1.6)), mark(ellipse(18, 18, 2, 1.6))]


@icon("ant-farm", CAT, "Thin glass frame on a stand filled with sand and a winding ant tunnel",
      tags=["formicarium", "terrarium", "ants", "tunnels", "science", "kids", "habitat"])
def _(S):
    frame = rect(4.5, 2.5, 15, 15, L(S, 1, 2.5))
    return [shell(frame), detail(seg(4.5, 6.5, 19.5, 6.5)), detail(poly([(9.5, 6.5), (9.5, 10.6), (14.5, 12.4)], r=S.r)),
            mark(ellipse(14.6, 14.2, 1.7, 1)), shell(rect(3, 19, 18, 3, L(S, 0.5, 1.5))), line(seg(8, 17.5, 8, 19)), line(seg(16, 17.5, 16, 19))]


@icon("honeypot-ant", CAT, "Side view of an ant with a hugely swollen round abdomen like a grape",
      tags=["honey ant", "repletes", "desert ant", "insect", "storage", "swollen", "ant"])
def _(S):
    return [shell(circle(16.2, 13.8, 6.2)), detail(arc(16.2, 13.8, 3.6, 200, 265)),
            solid(circle(4.6, 11.4, 1.8)), solid(ellipse(8.6, 12, 2.2, 1.7)),
            sthick("M7.6 13.4L5.8 17.4L4.6 21.4"), sthick("M9.2 13.8L9.4 17.6L9.8 21.4"), sthick("M11 13.4L12.2 17L14 20.8"),
            sthick("M3.8 10L2.6 7")]


@icon("termite", CAT, "Top view of a pale soft-bodied termite with a large rounded head, short straight antennae and six legs",
      tags=["white ant", "wood pest", "insect", "pest control", "infestation", "colony", "bug"])
def _(S):
    body = union(circle(12, 5.7, 2.8), ellipse(12, 10.6, 3.2, 2.4), ellipse(12, 16.8, 4, 4.4))
    return [shell(body), detail(seg(8.6, 15.4, 15.4, 15.4)), detail(seg(8.8, 18.6, 15.2, 18.6)),
            line(seg(10.6, 3.2, 9.4, 1.6)), line(seg(13.4, 3.2, 14.6, 1.6))] + legs_pair(S,
                [(9, 9.4), (6, 7.8), (4.6, 5.4)], [(8.8, 10.8), (5, 11.6), (3.2, 10)], [(9.2, 12.2), (6, 14.6), (5, 18.2)])


@icon("termite-mound", CAT, "Tall knobbly earth tower with several spires rising from the ground and small holes",
      tags=["termitary", "anthill", "savanna", "africa", "earth tower", "nest", "insects"])
def _(S):
    r = L(S, 0, 1.4)
    tower = union(poly([(8, 21), (9.4, 10), (10.6, 4.4), (12, 2.6), (13.4, 4.4), (14.6, 10), (16, 21)], closed=True, r=r),
                  poly([(3, 21), (4.4, 13.5), (6.2, 9.4), (8, 13.5), (9.6, 21)], closed=True, r=r),
                  poly([(14.4, 21), (16, 14.5), (18, 10.8), (19.6, 14.5), (21, 21)], closed=True, r=r))
    return [shell(tower), line(seg(2, 21.8, 22, 21.8)), mark(circle(12, 9.8, 0.9)), mark(circle(11.3, 14.6, 0.9)), mark(circle(13.4, 17.6, 0.9)),
            mark(circle(6, 16.6, 0.8)), mark(circle(18, 16.8, 0.8))]


@icon("wasp-nest", CAT, "Round papery nest hanging from a twig by a short stalk with layered bands and an entrance hole",
      tags=["hornet nest", "paper nest", "wasps", "pest", "hanging", "stinging insects", "nest"])
def _(S):
    nest = ellipse(12, 12.6, 6.8, 7.4)
    return [line(seg(5.5, 2.4, 18.5, 2.4)), line(seg(12, 2.4, 12, 5.2)), shell(nest),
            detail("M5.4 9.2C8.4 11.6 15.6 11.6 18.6 9.2"), detail("M6.2 13.2C9 15.4 15 15.4 17.8 13.2"), mark(ellipse(12, 17.9, 1.6, 1.2))]


@icon("ichneumon-wasp", CAT, "Side view of a slender wasp with a very long thin ovipositor trailing behind its body",
      tags=["parasitoid", "parasitic wasp", "stinger", "insect", "egg layer", "wood wasp", "wasp"])
def _(S):
    head = circle(4.4, 11, 1.8)
    thorax = ellipse(8.2, 11, 2.3, 1.9)
    abd = rot(ellipse(15, 13.2, 3.8, 1.3), 14, 15, 13.2)
    w = cut_wing(wing(11.4, 7, 4, 1.3, -16), thorax, g=1.5)
    return [shell(w), shell(union(head, thorax)), shell(abd), line(seg(10.4, 11.7, 11.8, 12.3)), sthick("M18.4 14.6C20.6 16 21.2 18.6 21.6 21.4", 1.2),
            line(poly([(3.6, 9.4), (2.6, 6.4)], r=S.r)), sthick("M7.2 12.8L6 17L5.6 20.6"), sthick("M8.8 13L9.4 17L9.8 20.6"), sthick("M10 12.6L12.4 16.6L13.6 20.2")]


# ============================================================================ moths and butterflies

def sym_shells(*ds):
    out = []
    for d in ds:
        out += [shell(d), shell(flip(d))]
    return out


def sym_lines(S, *chains):
    out = []
    for c in chains:
        out += [line(poly(c, r=S.r)), line(poly(fpts(c), r=S.r))]
    return out


def feathers(S, c):
    """Feathery antenna: a curved stalk with short side ticks (mirrored pair)."""
    return sym_lines(S, c)


@icon("moth", CAT, "Top view of a moth with broad triangular wings held flat, a fuzzy body and feathery antennae",
      tags=["night", "insect", "lamp", "nocturnal", "flying insect", "wings", "clothes moth"])
def _(S):
    r = L(S, 0, 2)
    fore = "M11.2 9.8L2.6 6.8" + tip((2.6, 6.8), (3, 13.4), (11.2, 13.6), r) + "L3 13.4C3.8 13.6 8 13.6 11.2 13.6Z"
    fore = poly([(11.2, 9.8), (2.6, 6.6), (3.4, 12.6), (11.2, 13.8)], closed=True, r=L(S, 0, 2.2))
    hind = "M11.2 14.2C8 14.2 5.4 15.6 5.6 18C5.8 19.8 8 20.4 11.2 19.8Z"
    return sym_shells(fore, hind) + [mark(ellipse(12, 14.2, 1.1, 4.8)), shell(circle(12, 6.4, 1.5))] + sym_lines(S, [(11.2, 5.4), (9.4, 3), (7.4, 2.4)]) + [
        line(seg(9.4, 3, 8.6, 4.6)), line(seg(14.6, 3, 15.4, 4.6))]


@icon("luna-moth", CAT, "Top view of a pale moth with rounded forewings, eyespots and two long curling tails on the hindwings",
      tags=["lunar moth", "actias luna", "green moth", "night", "insect", "tails", "silk moth"])
def _(S):
    fore = "M11.2 9.6C9.4 5 6 3.4 3.6 4.6C2.6 7.6 4.8 11.4 11.2 12.6Z"
    hind = L(S, "M11.2 12.4C7.6 12.2 6.2 13.8 6.2 16C6.2 18 6.8 19.6 5.4 22L8.4 21.2C10.4 19.2 11.2 16.8 11.2 14.6Z",
             "M11.2 12.4C7.6 12.2 6.2 13.8 6.2 16C6.2 18 6.8 19.6 5.6 21.6C5.8 22 7 21.8 8.4 21C10.4 19.2 11.2 16.8 11.2 14.6Z")
    return sym_shells(fore, hind) + [mark(ellipse(6.8, 8, 1.1, 1.3)), mark(ellipse(17.2, 8, 1.1, 1.3)), line(seg(12, 8.6, 12, 18)),
                                     shell(circle(12, 6.6, 1.5))] + sym_lines(S, [(11.3, 5.4), (9.6, 3), (8, 2.4)])


@icon("atlas-moth", CAT, "Top view of a huge moth whose forewing tips curl into hooked shapes, with a triangular window on each wing",
      tags=["giant moth", "attacus atlas", "snake head", "silk moth", "largest moth", "insect", "wings"])
def _(S):
    fore = "M11.2 9.8C8.6 7 5.8 4.6 3 4C2.4 5 3.2 6 4.4 6.2C3.4 7.4 3.4 8.8 4.4 9.6C3.6 11 3.2 12.6 3.8 14.4C6 15.6 8.6 15.4 11.2 13.6Z"
    hind = "M11.2 14C8.4 14 5.8 15.6 5.6 18C6 20 8.4 20.6 11.2 19.4Z"
    tri = poly([(6.2, 9), (9.4, 10.6), (6.4, 12.6)], closed=True)
    return sym_shells(fore, hind) + [mark(tri), mark(flip(tri)), line(seg(12, 8.4, 12, 19.4)), shell(circle(12, 6.6, 1.4))] + sym_lines(S, [(11.3, 5.6), (9.6, 3.4)])


@icon("hawk-moth", CAT, "Top view of a streamlined moth with narrow swept-back wings and a thick tapered body like a jet",
      tags=["sphinx moth", "hornworm moth", "fast flyer", "hovering", "insect", "night", "moth"])
def _(S):
    body = L(S, "M12 3.4C14.8 5 15.2 9 14.6 13C14 17 12.8 19.6 12 21.6C11.2 19.6 10 17 9.4 13C8.8 9 9.2 5 12 3.4Z",
            "M12 3.4C14.8 5 15.2 9 14.6 13C14 17 13 19.4 12 20.6C11 19.4 10 17 9.4 13C8.8 9 9.2 5 12 3.4Z")
    fw = poly([(10.4, 8.4), (2.4, 14.4), (2.8, 16.6), (10.8, 13.6)], closed=True, r=L(S, 0, 1))
    hw = poly([(10.8, 14.2), (6.6, 17.2), (10.8, 18)], closed=True, r=L(S, 0, 0.8))
    return [shell(fw), shell(flip(fw)), shell(hw), shell(flip(hw)), shell(body), detail(seg(12, 9, 12, 16)),
            line(poly([(11.4, 4.8), (10.2, 2.4)], r=S.r)), line(poly([(12.6, 4.8), (13.8, 2.4)], r=S.r))]


@icon("deaths-head-moth", CAT, "Top view of a moth with wings folded back and a small skull pattern on its thorax",
      tags=["skull", "hawk moth", "acherontia", "halloween", "spooky", "insect", "night"])
def _(S):
    wings = L(S, "M7.4 10C4 14 3.4 18 12 22C20.6 18 20 14 16.6 10Z", "M7.4 10C4 14 3.4 17.6 9.6 21C11 21.6 13 21.6 14.4 21C20.6 17.6 20 14 16.6 10Z")
    skull = minus(union(circle(12, 9.2, 2.2), rect(10.8, 10, 2.4, 2.4)), circle(10.9, 9.2, 0.7), circle(13.1, 9.2, 0.7))
    return [shell(union(wings, ellipse(12, 9.4, 4.8, 3.8))), shell(circle(12, 3.8, 1.5)), mark(skull),
            line(poly([(11.2, 2.7), (9.6, 1.8)], r=S.r)), line(poly([(12.8, 2.7), (14.4, 1.8)], r=S.r)),
            ]


@icon("plume-moth", CAT, "T-shaped moth with narrow rolled wings held straight out sideways and long thin legs",
      tags=["feather moth", "pterophoridae", "insect", "tiny", "night", "thin wings", "moth"])
def _(S):
    body = union(ellipse(12, 14.4, 1.6, 6), circle(12, 6.2, 1.6))
    return [solid(ellipse(12, 10, 10, 1.1)), shell(body), sthick("M11.6 17L9 19.6L8 22", 1.4), sthick("M12.4 17L15 19.6L16 22", 1.4),
            line(poly([(11.4, 5), (10, 2.2)], r=S.r)), line(poly([(12.6, 5), (14, 2.2)], r=S.r))]


@icon("hummingbird-hawk-moth", CAT, "Side view of a stout moth hovering at a flower with a long straight proboscis reaching into it",
      tags=["hovering", "hummingbird moth", "nectar", "flower", "pollinator", "insect", "proboscis"])
def _(S):
    body = union(ellipse(14.2, 14.2, 4.4, 3.2), circle(9.8, 13.8, 1.9))
    tail = poly([(18.4, 13.2), (22.4, 11.8), (22.4, 16.6), (18.4, 15.6)], closed=True, r=L(S, 0, 0.8))
    w1 = cut_wing(wing(13.2, 7.6, 1.9, 4.6, 12), body, g=1.6)
    w2 = cut_wing(wing(17.8, 8.6, 1.7, 3.8, 48), body, g=1.6)
    return [shell(w1), shell(w2), shell(union(body, tail)), line(seg(8, 13.8, 5.8, 13.8)), shell(circle(3.8, 13.8, 2.3)), mark(circle(3.8, 13.8, 0.8)),
            line(seg(3.8, 16.1, 3.8, 21.6))]


@icon("swallowtail-butterfly", CAT, "Top view of a butterfly with large forewings and hindwings that end in a pair of long pointed tails",
      tags=["papilio", "butterfly", "tails", "insect", "spring", "garden", "wings"])
def _(S):
    fore = "M11.4 11C10.2 6 7 3.2 3 3.6C2.6 7.6 4.8 11 11.4 12.6Z"
    hind = L(S, "M11.4 12.8C8 12.4 5.6 13.4 5 15.6C4.6 17.4 5.6 18.4 7 18.2L5.6 21L9.6 19.2C10.8 18.6 11.3 17 11.4 15Z",
             "M11.4 12.8C8 12.4 5.6 13.4 5 15.6C4.6 17.4 5.6 18.4 7 18.2C6.4 19.2 5.8 20 5.8 20.6C6.8 20.8 8.6 20 9.6 19.2C10.8 18.6 11.3 17 11.4 15Z")
    return sym_shells(fore, hind) + [line(seg(12, 8, 12, 17))] + sym_lines(S, [(11.4, 7.2), (9.6, 3.6)])


@icon("monarch-butterfly", CAT, "Top view of a butterfly with bold dark vein lines across the wings and a dotted border edge",
      tags=["danaus", "orange butterfly", "migration", "milkweed", "insect", "veins", "wings"])
def _(S):
    fore = "M11.4 10C10 5.4 6.6 3.4 3 3.8C2.4 8 5 11 11.4 12.2Z"
    hind = "M11.4 12.8C8.6 12.4 4.8 13.4 4.2 16.4C3.8 19.2 6.8 20.6 9.4 19.4C10.8 18.6 11.3 17 11.4 15Z"
    parts = sym_shells(fore, hind)
    for ch in ((10.8, 10.4, 6.6, 7.4), (10.8, 14.4, 7.4, 16.8)):
        parts += [detail(seg(*ch)), detail(seg(24 - ch[0], ch[1], 24 - ch[2], ch[3]))]
    return parts + [line(seg(12, 8, 12, 18))] + sym_lines(S, [(11.4, 7.2), (9.6, 3.8)])


@icon("owl-butterfly", CAT, "Top view of a butterfly with one big round owl eye spot on each hindwing",
      tags=["caligo", "eyespot", "rainforest", "butterfly", "insect", "tropical", "camouflage"])
def _(S):
    fore = "M11.4 10C10 6 7 3.8 3.4 4.2C2.8 8 5 11 11.4 12.2Z"
    hind = "M11.4 12.4C7.4 11.8 3.6 13 3.4 16.4C3.4 19.6 7 21.2 9.6 20C10.8 19.2 11.3 17.4 11.4 15Z"
    return sym_shells(fore, hind) + [mark(circle(7.4, 16.6, 2.1)), mark(circle(16.6, 16.6, 2.1)), line(seg(12, 8, 12, 19))] + sym_lines(S, [(11.4, 7.2), (9.6, 3.8)])


@icon("glasswing-butterfly", CAT, "Top view of a butterfly whose wings are clear outlines with dark borders and a few veins",
      tags=["greta oto", "transparent", "clear wings", "butterfly", "insect", "tropical", "see-through"])
def _(S):
    r = L(S, 0, 1.4)
    fore = "M11.2 10.4C10 6.2 7 3.8 3.6 4.4" + tip((4.6, 4.2), (3, 4.6), (3.4, 8), r) + "L3.4 8C3.8 11 6 12 11.2 12.6Z"
    hind = "M11.2 13.2C8.4 12.8 5.4 13.6 4.8 16.2C4.4 18.8 7 20 9.4 19C10.8 18.2 11.1 16.6 11.2 15Z"
    parts = []
    for d in (fore, hind):
        parts += [line(d), line(flip(d))]
    for seg_ in ((10.6, 11.4, 6, 8), (10.6, 15.4, 7.4, 17.4)):
        parts += [detail(seg(*seg_)), detail(seg(24 - seg_[0], seg_[1], 24 - seg_[2], seg_[3]))]
    return parts + [solid(ellipse(12, 12.6, 1, 5.6)), line(seg(12, 7.4, 12, 8.2))] + sym_lines(S, [(11.4, 7.4), (9.6, 3.8)])


@icon("butterfly-wing", CAT, "A single detached forewing and hindwing pair seen from one side with vein lines, as a specimen",
      tags=["wing", "specimen", "butterfly", "lepidoptera", "veins", "collection", "entomology"])
def _(S):
    fore = "M11.4 10C10 5.4 6.6 3.4 3 3.8C2.4 8 5 11 11.4 12.2Z"
    hind = "M11.4 12.8C8.6 12.4 4.8 13.4 4.2 16.4C3.8 19.2 6.8 20.6 9.4 19.4C10.8 18.6 11.3 17 11.4 15Z"
    m = (1.8, 0, 0, 1, -0.6, 0)
    f = path_to_d(transform_path(P(fore), m))
    h = path_to_d(transform_path(P(hind), m))
    return [shell(f), shell(h), detail(seg(19, 10.6, 8.4, 6.4)), detail(seg(19, 14.4, 9.4, 17))]


@icon("butterfly-specimen", CAT, "Butterfly with its wings spread flat, pinned through the body to a small board with a label",
      tags=["pinned butterfly", "collection", "museum", "entomology", "display", "mounted", "lepidoptera"])
def _(S):
    fore = "M11.4 9.6C10.2 6 7.4 4 3.6 4.4C3.2 7.8 5.2 9.8 11.4 11.2Z"
    hind = "M11.4 11.8C8.4 11.6 5.8 12.2 5.4 14C5.2 15.8 6.8 16.4 8.6 15.6C10.2 14.8 11.3 13.8 11.4 12.4Z"
    return sym_shells(fore, hind) + [line(seg(12, 6.4, 12, 17)), shell(rect(2.5, 18.5, 19, 3.5, L(S, 0.6, 1.4))), dot(12, 2.6, 1.1)]


@icon("caterpillar", CAT, "Side view of a caterpillar made of a row of round segments with a round head, antennae and stubby legs",
      tags=["larva", "butterfly larva", "crawling", "garden pest", "insect", "worm", "metamorphosis"])
def _(S):
    segs = [circle(9.6, 12.6, 2.6), circle(13.6, 11.8, 2.6), circle(17.4, 12, 2.6), circle(20.4, 13.6, 2)]
    head = circle(5, 12.2, 3)
    body = union(head, *segs)
    return [shell(body), dot(4.2, 11.4, 0.85), line(poly([(4.6, 9.4), (3.6, 6.6)], r=S.r)), line(poly([(6.6, 9.6), (7.8, 6.8)], r=S.r)),
            line(seg(8.8, 15.4, 8.8, 18.4)), line(seg(12.8, 14.6, 12.8, 17.6)), line(seg(16.6, 14.8, 16.6, 17.8))]


@icon("inchworm", CAT, "Side view of a thin caterpillar arched into a tall loop with both ends on a twig",
      tags=["measuring worm", "looper", "geometer", "caterpillar", "larva", "garden", "insect"])
def _(S):
    ctrl = ((4.4, 19), (2.4, 1.6), (21.6, 1.6), (19.6, 19))
    d = "M4.4 19C2.4 1.6 21.6 1.6 19.6 19"
    cuts = []
    for t in (0.18, 0.34, 0.5, 0.66, 0.82):
        x, y = bez(*ctrl, t)
        x2, y2 = bez(*ctrl, t + 0.01)
        x1, y1 = bez(*ctrl, t - 0.01)
        a = math.atan2(y2 - y1, x2 - x1) + math.pi / 2
        cuts.append(path_to_d(ST(seg(x - 2.2 * math.cos(a), y - 2.2 * math.sin(a), x + 2.2 * math.cos(a), y + 2.2 * math.sin(a)), 0.9)))
    body = minus(thick(d, 3.2, S), *cuts)
    head = minus(circle(19.8, 19.6, 2.1), circle(20.4, 19, 0.5))
    return [solid(body), solid(head), line(seg(1.8, 22, 22.2, 22)) if False else line(seg(2, 22.2, 22, 22.2))]


@icon("hornworm", CAT, "Side view of a plump segmented caterpillar with diagonal stripes and a curved horn on its tail end",
      tags=["tomato hornworm", "sphinx moth larva", "caterpillar", "garden pest", "insect", "larva", "horn"])
def _(S):
    body = rect(3, 8.5, 17, 7.5, L(S, 3, 3.75))
    parts = [shell(body), dot(6, 11.4, 0.9)]
    for x in (9.6, 12.6, 15.6):
        parts.append(detail(seg(x, 15.6, x + 2, 9)))
    parts += [line("M19.6 10C21.4 8.4 21.8 6.4 21.2 4.4"), line(seg(7, 16, 7, 19)), line(seg(12, 16, 12, 19)), line(seg(16.4, 16, 16.4, 19))]
    return parts


# ============================================================================ life stages and moth things

@icon("woolly-bear-caterpillar", CAT, "Fuzzy caterpillar curled into a C shape with a bristly outline and a dark band at each end",
      tags=["woolly worm", "fuzzy", "tiger moth larva", "isabella", "autumn", "winter forecast", "caterpillar"])
def _(S):
    arcd = arc(12, 12, 6.2, 50, 310)
    body = thick(arcd, 5.8, S)
    parts = [shell(body)]
    for a in range(68, 300, 24):
        x0, y0 = pt_on(12, 12, 9.2, a)
        x1, y1 = pt_on(12, 12, 11, a)
        parts.append(sthick(seg(x0, y0, x1, y1), 1.1))
    parts.append(mark(clip(body, path_to_d(ST(arc(12, 12, 6.2, 50, 88), 7)))))
    parts.append(mark(clip(body, path_to_d(ST(arc(12, 12, 6.2, 272, 310), 7)))))
    parts.append(dot(16.2, 18.4, 0.0001)) if False else None
    return [p for p in parts if p]


@icon("processionary-caterpillars", CAT, "Three fuzzy caterpillars following each other nose to tail in a single line",
      tags=["procession", "oak processionary", "pine", "pest", "nose to tail", "larvae", "caterpillars"])
def _(S):
    parts = []
    for x0 in (2.2, 9.2, 16.2):
        parts.append(shell(rect(x0, 9.2, 5.8, 5.6, L(S, 1.6, 2.8))))
        for dx in (1.2, 2.9, 4.6):
            parts.append(sthick(seg(x0 + dx, 8.4, x0 + dx, 6.4), 1.0))
            parts.append(sthick(seg(x0 + dx, 15.6, x0 + dx, 17.6), 1.0))
    parts.append(dot(19.4, 11, 0.7)) if False else None
    return [p for p in parts if p]


@icon("silkworm", CAT, "Side view of a smooth pale segmented larva with a small tail horn, resting on a mulberry leaf",
      tags=["bombyx mori", "sericulture", "silk", "larva", "caterpillar", "mulberry", "farm"])
def _(S):
    leaf = "M2.5 21C5.5 15.4 15 14.6 21.5 17.4C19.4 21 10 22 2.5 21Z"
    body = union(circle(5.6, 9.2, 3.2), rect(7.4, 6, 12.4, 6.4, L(S, 2.4, 3.2)))
    return [shell(leaf), detail(seg(5, 19.6, 17, 18)), shell(body), detail(seg(10.4, 6, 10.4, 12.4)), detail(seg(13.8, 6, 13.8, 12.4)),
            detail(seg(17.2, 6, 17.2, 12.4)), dot(4.6, 8.4, 0.8), line(poly([(19.4, 6.4), (21, 3.8)], r=S.r))]


@icon("silk-cocoon", CAT, "Oval white cocoon with a single silk thread unwinding from it to a small reel",
      tags=["silk", "spinning", "thread", "silkworm", "textile", "reeling", "cocoon"])
def _(S):
    cocoon = rot(L(S, "M7.4 2.6C11 4 12.6 8 12 11.6C11.6 14.4 9.6 14.8 7.4 14.8C5 14.8 3 14 3 10.8C3 6.4 5 3.6 7.4 2.6Z", ellipse(7.8, 8.8, 4.6, 6)), -18, 7.6, 8.8)
    return [shell(cocoon), detail("M4.8 7.6C6.4 9 8.6 9 10.4 7.4"), line("M11 13C13 14 13.4 14.6 14 15.6"), shell(circle(17, 17.4, 4.4)), mark(circle(17, 17.4, 1.3))]


@icon("chrysalis", CAT, "Green teardrop pupa hanging from a twig by a short tip, with a dotted band across it",
      tags=["pupa", "butterfly", "metamorphosis", "hanging", "transformation", "insect", "jade"])
def _(S):
    body = L(S, "M12 5.5C16.6 7 17.6 12 15 16.5C14 18.6 13 20.4 12 21.6C11 20.4 10 18.6 9 16.5C6.4 12 7.4 7 12 5.5Z",
            "M12 5.5C16.6 7 17.6 12 15 16.5C14 18.6 13.2 20 12 20.6C10.8 20 10 18.6 9 16.5C6.4 12 7.4 7 12 5.5Z")
    return [line(seg(5, 2.8, 19, 2.8)), line(seg(12, 2.8, 12, 6)), shell(body), mark(circle(9.8, 11.4, 0.85)), mark(circle(12, 11.4, 0.85)), mark(circle(14.2, 11.4, 0.85))]


@icon("cocoon", CAT, "Fuzzy spindle-shaped cocoon wrapped in wavy silk lines and fixed along a twig",
      tags=["moth", "pupa", "silk", "twig", "metamorphosis", "insect", "wrapped"])
def _(S):
    spindle = L(S, "M2.8 11.6C7 6.8 17 6.8 21.2 11.6C17 16.4 7 16.4 2.8 11.6Z", ellipse(12, 11.6, 9.4, 4.4))
    return [shell(spindle), detail("M8.6 7.6C10 10 7.2 12 8.6 15.6"), detail("M12.4 7C13.8 10 11 12.6 12.4 16.2"), detail("M16.2 8C17.6 10.4 15 12.4 16.2 15.2"),
            line(seg(2, 19.4, 22, 19.4)), line(seg(12, 16.2, 12, 19.4))]


@icon("butterfly-emerging", CAT, "Split chrysalis hanging from a twig with a butterfly climbing out and its crumpled wings unfolding",
      tags=["eclosion", "hatching", "metamorphosis", "pupa", "butterfly", "transformation", "new life"])
def _(S):
    husk = "M12 5C14.8 6 15.2 9 14 11.4L12 12.6L10 11.4C8.8 9 9.2 6 12 5Z"
    wl = "M11 12.8C8 12.4 4 14.2 3.6 17.6C3.4 20 6 21 8.2 19.8C10 18.8 11 16.4 11 12.8Z"
    return [line(seg(6, 2.8, 18, 2.8)), line(seg(12, 2.8, 12, 5.4)), shell(husk), shell(wl), shell(flip(wl)), line(seg(12, 11.6, 12, 19.4))]


def _arrow_arc(S, cx, cy, r, a0, a1):
    d = arc(cx, cy, r, a0, a1)
    ex, ey = pt_on(cx, cy, r, a1)
    th = math.radians(a1 + 90)
    ux, uy = math.cos(th), math.sin(th)
    nx, ny = -uy, ux
    head = poly([(ex + ux * 1.6, ey + uy * 1.6), (ex - ux * 0.5 + nx * 1.7, ey - uy * 0.5 + ny * 1.7), (ex - ux * 0.5 - nx * 1.7, ey - uy * 0.5 - ny * 1.7)], closed=True)
    return [line(d), solid(head)]


@icon("metamorphosis", CAT, "Four life stages in a circle joined by arrows: egg, caterpillar, chrysalis and butterfly",
      tags=["life cycle", "butterfly life cycle", "stages", "transformation", "egg", "larva", "pupa"])
def _(S):
    parts = [solid(ellipse(5.6, 5.4, 1.6, 2)),
             solid(circle(15.6, 6, 1.35)), solid(circle(18, 6.2, 1.35)), solid(circle(20.4, 6.4, 1.35)),
             solid("M18.4 16C20.8 17.4 20.8 20 18.4 22.4C16 20 16 17.4 18.4 16Z"),
             solid("M5.6 19.6L2.2 16.8L2.8 21.4Z"), solid("M5.6 19.6L9 16.8L8.4 21.4Z")]
    parts += _arrow_arc(S, 12, 12, 8.6, -118, -80)[0:2]
    parts += _arrow_arc(S, 12, 12, 8.6, -28, 10)
    parts += _arrow_arc(S, 12, 12, 8.6, 62, 100)
    parts += _arrow_arc(S, 12, 12, 8.6, 152, 190)
    return parts


@icon("bagworm", CAT, "Tapered case covered with small twig pieces hanging from a branch by a silk thread",
      tags=["bag worm", "psychidae", "evergreen pest", "case moth", "larva", "twigs", "tree pest"])
def _(S):
    case = poly([(8, 6.4), (16, 6.4), (14.2, 19.4), (9.8, 19.4)], closed=True, r=L(S, 0, 1.6))
    return [line(seg(3, 2.8, 21, 2.8)), line(seg(12, 2.8, 12, 6.4)), shell(case), detail(seg(9.2, 10, 13, 8.6)), detail(seg(11.4, 13.6, 14.6, 12.2)),
            detail(seg(9.6, 16.6, 12.8, 15.4)), dot(12, 21, 1.2)]


@icon("moth-to-flame", CAT, "Small moth circling a lit candle flame along a dotted spiral flight path",
      tags=["attracted", "light", "candle", "fire", "danger", "obsession", "moth"])
def _(S):
    flame = "M12 5C14.4 7.6 15 9.4 15 11C15 12.8 13.6 14 12 14C10.4 14 9 12.8 9 11C9 9.4 9.6 7.6 12 5Z"
    parts = [shell(flame), shell(rect(9.4, 15.6, 5.2, 6, L(S, 0.6, 1.6)))]
    for i, (a, r) in enumerate(((20, 7.2), (-30, 7.4), (-80, 7), (-130, 6.8), (180, 7), (140, 6.6), (100, 6.4))):
        if i < 6:
            pass
    pts = [(5.6, 9.4), (4.6, 13.6), (6.4, 17.8), (3.8, 6)]
    parts += [dot(4.4, 7.2, 0.8), dot(3.8, 10.8, 0.8), dot(4.6, 14.4, 0.8), dot(7.6, 17.2, 0.8), dot(7.2, 4.4, 0.8)]
    parts += [solid(poly([(18, 6), (14.6, 3.2), (15, 8.8)], closed=True)), solid(poly([(18, 6), (21.4, 3.2), (21, 8.8)], closed=True)),
              solid(ellipse(18, 6.2, 0.8, 2.2))]
    return parts


@icon("moth-trap", CAT, "Lamp on an arm shining over an open box lined with egg-tray cones where moths land",
      tags=["light trap", "moth survey", "entomology", "nocturnal insects", "lamp", "monitoring", "egg tray"])
def _(S):
    box = poly([(3, 14.4), (3, 21.4), (16.6, 21.4), (16.6, 14.4)], r=S.r)
    return [line(box), line(poly([(20.4, 21.4), (20.4, 3), (10, 3), (10, 4.4)], r=S.r)), shell(circle(10, 7.6, 2.4)),
            solid(poly([(4.6, 21), (7, 17.2), (9.4, 21)], closed=True)), solid(poly([(10, 21), (12.4, 17.2), (14.8, 21)], closed=True)),
            dot(15, 9.8, 0.8), dot(5.2, 10.4, 0.8)]


# ============================================================================ beetles

def burst(cx, cy, ro, ri, n, r=0.0, start=-90):
    pts = []
    for i in range(2 * n):
        rad = ro if i % 2 == 0 else ri
        pts.append(pt_on(cx, cy, rad, start + i * 180 / n))
    return poly(pts, closed=True, r=r)


@icon("stag-beetle", CAT, "Top view of a beetle with huge branched antler-like jaws in front of its head",
      tags=["lucanus", "antlers", "mandibles", "horned beetle", "insect", "wood", "male stag"])
def _(S):
    body = union(circle(12, 8.4, 2), ellipse(12, 11.6, 3.4, 2.2), ellipse(12, 17, 4.4, 5))
    jaw = [(10.8, 7.4), (6.8, 6.2), (5.8, 2.4)]
    tine = [(6.8, 6.2), (8.8, 3.8)]
    parts = [shell(union(circle(12, 8.4, 2), ellipse(12, 11.6, 3.4, 2.2))), shell(ellipse(12, 17, 4.4, 5)), detail(seg(12, 13, 12, 21))]
    parts += sym_lines(S, jaw, tine)
    parts += legs_pair(S, [(9, 11), (5.6, 12.4), (4, 14.6)], [(8, 15), (4.6, 17.4)], [(8.6, 19.4), (5.6, 21.4)])
    return parts


@icon("rhinoceros-beetle", CAT, "Side view of a domed beetle with one big upward curved horn on its head",
      tags=["hercules beetle", "horn", "dynastinae", "insect", "strong", "tropical", "scarab"])
def _(S):
    body = L(S, "M7.4 17.4C7.2 10.6 11 8.2 15 8.6C19 9 21 12.6 21 17.4Z", "M7.4 17.4C7.2 10.6 11 8.2 15 8.6C19 9 21 12.6 21 17.4Z")
    head = union(circle(5.6, 14.2, 2.2), poly([(5, 12.2), (9.4, 10.8), (9.4, 17.4), (4, 17.4)], closed=True))
    return [shell(union(body, head)), line("M4.8 12.2C2.4 8.8 3.6 4.6 8.2 3.4"), detail("M13.4 9C15.6 11 16 14 15.6 17"),
            line(seg(9, 17.4, 7.4, 21.6)), line(seg(14, 17.4, 14, 21.6)), line(seg(19, 17.4, 20.6, 21.6))]


@icon("dung-beetle", CAT, "Side view of a beetle on its front legs pushing a large round dung ball with its back legs",
      tags=["scarab", "ball", "rolling", "manure", "ecology", "insect", "scarabaeus"])
def _(S):
    body = rot(ellipse(18, 12.6, 4.8, 3.2), 62, 18, 12.6)
    return [shell(circle(6.8, 14.4, 5.2)), detail("M4.4 12.2C5.2 11 6.4 10.4 7.8 10.6"), solid(body), solid(circle(20.8, 18.4, 1.7)),
            line(seg(2, 22.2, 22, 22.2)), sthick("M15.2 9.8L12.8 10.4", 1.5), sthick("M15 13.6L13.2 15.4", 1.5), sthick("M21 19.6L20.8 22", 1.5)]


@icon("scarab", CAT, "Front view of a stylised sacred scarab with outspread wings holding a sun disk above its head",
      tags=["egyptian", "khepri", "sun disk", "ancient egypt", "amulet", "beetle", "sacred"])
def _(S):
    wl = "M8.2 12.8C5.6 10.8 3 11 2.2 12.8C2.4 15 5 16.4 8.2 15.8Z"
    return [shell(circle(12, 4.4, 2.4)), shell(wl), shell(flip(wl)), shell(ellipse(12, 15.6, 4.2, 5.2)), detail(seg(12, 11.2, 12, 20.4)),
            shell(poly([(9.6, 11), (12, 8.2), (14.4, 11)], closed=True, r=L(S, 0, 1))),
            line(poly([(10.2, 9.2), (9.2, 7.6)], r=S.r)), line(poly([(13.8, 9.2), (14.8, 7.6)], r=S.r)),
            line(seg(7.8, 19, 5.6, 21.8)), line(seg(16.2, 19, 18.4, 21.8))]


@icon("firefly", CAT, "Side view of a small flying beetle with a glowing tail end and short light rays",
      tags=["lightning bug", "glow worm", "bioluminescent", "night", "summer", "insect", "light"])
def _(S):
    body = union(circle(3.8, 12.6, 1.8), ellipse(7.6, 12.4, 2.4, 2.1), ellipse(12.6, 12.8, 4.2, 3))
    glow = clip(ellipse(12.6, 12.8, 4.2, 3), rect(14.4, 8, 8, 10))
    w = cut_wing(wing(10.6, 7.6, 1.8, 3.8, 30), body, g=1.6)
    parts = [shell(w), shell(body), mark(glow)]
    for a in (-55, -20, 20, 55):
        x0, y0 = pt_on(17.6, 12.8, 2.9, a)
        x1, y1 = pt_on(17.6, 12.8, 4.3, a)
        parts.append(line(seg(x0, y0, x1, y1)))
    parts += [sthick("M6.6 14.2L5.8 17.6", 1.2), sthick("M8.8 14.4L9.6 17.8", 1.2)]
    return parts


@icon("weevil", CAT, "Side view of an oval beetle with a long curved down-pointing snout and elbowed antennae",
      tags=["snout beetle", "curculionidae", "boll weevil", "grain pest", "crop pest", "insect", "rostrum"])
def _(S):
    body = union(ellipse(14.4, 11.6, 6.4, 5), circle(7.8, 10.6, 2.2))
    return [shell(body), detail("M12.8 7C14.6 9 14.8 13 12.8 16"), line("M6.6 11.8C4.2 13.6 3.6 16.8 4.8 19.6"),
            line(poly([(5.6, 14.6), (8.4, 15.6), (8.8, 18.2)], r=S.r)), line(seg(11, 16.6, 10, 21.2)), line(seg(15, 16.8, 15, 21.2)), line(seg(19, 16, 20.4, 20.6))]


@icon("giraffe-weevil", CAT, "Side view of a small beetle with an extremely long thin neck held up and angled forward",
      tags=["trachelophorus", "madagascar", "long neck", "leaf roller", "weevil", "insect", "giraffe"])
def _(S):
    body = ellipse(14.6, 15.2, 5.6, 4)
    return [shell(body), detail("M12.6 11.6C14.4 13.6 14.4 16.8 12.6 18.8"), sthick("M10 14L4.6 6.4", 2.2), solid(circle(4, 5, 2)),
            line(seg(11.6, 19, 10.6, 22)), line(seg(15.6, 19.2, 15.6, 22)), line(seg(19.4, 18.4, 20.8, 21.6))]


@icon("longhorn-beetle", CAT, "Top view of an elongated beetle with two antennae much longer than its body curving back",
      tags=["cerambycidae", "long horned", "antennae", "wood borer", "insect", "timber pest", "capricorn"])
def _(S):
    body = union(circle(12, 5.4, 1.8), ellipse(12, 9.2, 2.3, 1.8))
    el = L(S, "M9.4 11.2C8.6 14 9 18 12 21.6C15 18 15.4 14 14.6 11.2Z", "M9.4 11.2C8.6 14 9 17.6 10.8 20.4C11.4 21.2 12.6 21.2 13.2 20.4C15 17.6 15.4 14 14.6 11.2Z")
    return [shell(body), shell(el), detail(seg(12, 12, 12, 19))] + sym_lines(S, [(10.8, 4.4), (6, 3.4), (3.6, 8), (3.2, 14), (4, 19.6)]) + legs_pair(S, [(9.8, 9.6), (7.4, 11.6)], [(9.4, 13), (7.2, 15.4)])


@icon("bombardier-beetle", CAT, "Side view of a beetle with its abdomen tip spraying a burst cloud backwards",
      tags=["chemical defense", "spray", "explosion", "carabidae", "insect", "boiling", "defense"])
def _(S):
    body = union(circle(3.8, 12.6, 1.6), ellipse(9.4, 12.6, 5.6, 3.8))
    return [shell(body), detail("M8.8 9.4C10 11.2 10 14 8.8 15.8"), shell(burst(18.4, 12.6, 3.3, 1.7, 6, r=L(S, 0, 0.5))),
            dot(15.4, 8.4, 0.7), dot(15.2, 17, 0.7), line(seg(7, 16.4, 6, 20.6)), line(seg(10, 16.4, 10, 20.6)), line(seg(12.8, 15.8, 14.2, 20))]


@icon("diving-beetle", CAT, "Side view of a smooth oval beetle underwater with a silver air bubble at its tail and paddle legs",
      tags=["dytiscus", "water beetle", "pond", "aquatic", "air bubble", "swimming", "insect"])
def _(S):
    body = union(ellipse(11.4, 11.4, 7.4, 3.8), circle(4.2, 11.6, 2.2))
    return [line("M2 3.6C4 2.4 6 2.4 8 3.6C10 4.8 12 4.8 14 3.6C16 2.4 18 2.4 20 3.6"), shell(body), detail("M12 7.8C14 9.6 14 13.2 12 15"),
            shell(circle(19.8, 13.8, 2.2)), line(poly([(15, 15), (17.2, 18.4)], r=S.r)), solid(rot(ellipse(17.8, 19.4, 1, 2.2), 30, 17.8, 19.4)),
            line(poly([(8.4, 15), (7.6, 18.4)], r=S.r))]


@icon("tortoise-beetle", CAT, "Top view of a round flat beetle with a wide clear shield rim around a small domed centre",
      tags=["cassidinae", "shield", "golden tortoise", "leaf beetle", "insect", "round", "armor"])
def _(S):
    outer = L(S, "M12 21.4C8 21.4 4 18.2 4 13C4 8.6 7.4 5.6 12 5.6C16.6 5.6 20 8.6 20 13C20 18.2 16 21.4 12 21.4Z".replace("12 21.4C8", "12 21.4C8"),
              circle(12, 13.4, 8))
    return [shell(union(outer, circle(12, 4.4, 1.9))), shell(ellipse(12, 13.4, 3.4, 4)), dot(12, 13, 1) if False else dot(12, 14, 0.9)]


@icon("violin-beetle", CAT, "Top view of a very flat beetle shaped like the body of a violin with a long narrow head",
      tags=["mormolyce", "fiddle beetle", "flat", "ground beetle", "insect", "violin", "tropical"])
def _(S):
    body = union(ellipse(12, 4.6, 1.5, 2.8), ellipse(12, 10.8, 3.6, 2.8), ellipse(12, 16.8, 4.8, 4.4))
    return [shell(body), detail(seg(12, 8.4, 12, 20))] + legs_pair(S, [(9.2, 10.4), (5.8, 11), (4, 13.4)], [(8, 15), (4.4, 16.6), (3.6, 19.4)], [(9, 19.6), (6.4, 21.8)])


@icon("colorado-potato-beetle", CAT, "Top view of a domed beetle with bold stripes running lengthwise down each wing cover",
      tags=["leptinotarsa", "crop pest", "potato", "striped beetle", "garden pest", "insect", "agriculture"])
def _(S):
    el = ellipse(12, 14.4, 6.4, 6.8)
    parts = [shell(union(circle(12, 5.6, 2.2), ellipse(12, 8.8, 3.6, 1.8))), shell(el), detail(seg(12, 8.4, 12, 21.2))]
    for x in (8, 16):
        parts.append(mark(clip(el, rect(x - 0.7, 8, 1.4, 14))))
    parts += legs_pair(S, [(6.2, 12), (3.8, 13.4)], [(6, 16), (3.8, 18)])
    return parts


@icon("cockchafer", CAT, "Side view of a chunky beetle with a pointed tail and fan-shaped leaf antennae spread open",
      tags=["may bug", "maybug", "melolontha", "chafer", "june bug", "insect", "scarab"])
def _(S):
    body = L(S, "M7.6 11.6C7.6 8 11 7.6 14 8C17.4 8.4 19.4 11 21.6 14.4C19 17.2 14 17.6 10.6 16.8C8.6 16.2 7.6 14 7.6 11.6Z",
            "M7.6 11.6C7.6 8 11 7.6 14 8C17.4 8.4 19 11 20.6 14C18.6 16.8 14 17.6 10.6 16.8C8.6 16.2 7.6 14 7.6 11.6Z")
    return [shell(union(body, circle(5.4, 12.6, 2.2))), detail("M12.4 8.4C14.2 10.6 14.4 14 13 16.8"),
            line(poly([(4.6, 10.6), (3.8, 8.4)], r=S.r)), line(seg(3.8, 8.4, 1.8, 6.6)), line(seg(3.8, 8.4, 3.4, 5.4)), line(seg(3.8, 8.4, 5.6, 5.8)),
            line(seg(9.4, 16.8, 8.2, 21)), line(seg(13, 17, 13, 21)), line(seg(17, 16.2, 18.6, 20.4))]


@icon("woodworm", CAT, "Plank end with scattered small round bore holes and a winding tunnel exposed along its lower edge",
      tags=["wood borer", "furniture beetle", "timber damage", "infestation", "pest control", "carpentry", "rot"])
def _(S):
    plank = rect(2.5, 4.5, 19, 15, L(S, 1, 2))
    return [shell(plank), mark(circle(7, 9, 1.2)), mark(circle(14.4, 8, 1.1)), mark(circle(18.4, 11, 1.2)), mark(circle(10.4, 12, 0.9)),
            detail("M5 16.4C7.6 14 9.6 18.4 12.2 16C14.4 14 16.4 17.4 19 15.4")]


# ============================================================================ flies, larvae and flying insects

@icon("mosquito", CAT, "Side view of a mosquito with long thin legs, narrow wings and a long needle proboscis pointing down",
      tags=["malaria", "bite", "dengue", "zika", "pest", "biting insect", "bug"])
def _(S):
    head = circle(6.2, 9, 1.6)
    thorax = ellipse(9.8, 9.2, 2.4, 2)
    abd = rot(ellipse(16, 10.6, 4.6, 1.6), 10, 16, 10.6)
    w = cut_wing(lens(S, 12, 5.4, 3.8, 1.1, -14), thorax, g=1.5)
    return [shell(w), shell(union(head, thorax)), shell(abd), sthick("M5.4 10.4L4 17.6", 1.2), sthick("M9 11L7 16L6 21.6", 1.2),
            sthick("M10.4 11.2L12 17L11.2 21.8", 1.2), sthick("M11.8 10.8L15.4 16L17.8 21.4", 1.2)]


@icon("mosquito-larva", CAT, "Comma-shaped larva hanging head-down from the water surface line by a short breathing tube",
      tags=["wriggler", "aquatic larva", "standing water", "pest control", "breeding", "insect", "pond"])
def _(S):
    abd = thick("M12.6 12.6C13.6 10.6 14.6 8.6 14.8 6.6", 2.6, S)
    body = union(circle(9.8, 18.2, 2.1), circle(11.6, 14.2, 2.8), abd)
    return [line("M2 4C4.5 2.8 6.5 2.8 9 4C11.5 5.2 13.5 5.2 16 4C18.5 2.8 20 2.8 22 4"), line(seg(14.8, 4.4, 14.8, 7)), shell(body),
            dot(8.8, 18.6, 0.7)]


@icon("housefly", CAT, "Top view of a fly with a chunky body, big round compound eyes and two clear wings angled back",
      tags=["fly", "musca", "pest", "household pest", "insect", "buzz", "bug"])
def _(S):
    thorax = ellipse(12, 11, 3.2, 3)
    abd = ellipse(12, 17.6, 2.8, 3.8)
    w = cut_wing(wing(7.6, 15, 5.2, 2.1, -64), thorax, abd, g=1.4)
    return [shell(w), shell(flip(w)), shell(union(thorax, abd)), shell(circle(12, 6.4, 1.8)), mark(circle(9.4, 5.6, 1.9)), mark(circle(14.6, 5.6, 1.9)),
            detail(seg(9, 14.4, 15, 14.4))] + legs_pair(S, [(9.6, 10.4), (6.4, 9.6), (4.4, 6.6)], [(9.2, 12), (5.2, 13), (3.4, 16)])


@icon("crane-fly", CAT, "Top view of a thin long-bodied fly with two narrow wings and six extremely long spindly legs",
      tags=["daddy long legs", "tipulidae", "mosquito hawk", "insect", "long legs", "fly", "garden"])
def _(S):
    body = union(circle(12, 4.6, 1.5), ellipse(12, 8.2, 1.8, 2))
    abd = ellipse(12, 15.6, 1.4, 5.4)
    w = cut_wing(lens(S, 6.6, 10.8, 5, 1.2, -20), body, g=1.2)
    return [shell(w), shell(flip(w)), shell(body), shell(abd), sthick("M10.8 8L7 4.4L3 10.4", 1.1), sthick("M13.2 8L17 4.4L21 10.4", 1.1),
            sthick("M10.6 9L5 9.4L3.4 16", 1.1), sthick("M13.4 9L19 9.4L20.6 16", 1.1), sthick("M10.8 10L7 15L5.6 21.6", 1.1), sthick("M13.2 10L17 15L18.4 21.6", 1.1)]


@icon("stalk-eyed-fly", CAT, "Front view of a small fly with its eyes on the ends of two long horizontal stalks",
      tags=["diopsidae", "stalk eyes", "eye span", "insect", "curious fly", "sexual selection", "fly"])
def _(S):
    wl = lens(S, 6.4, 15.6, 3.6, 1.6, 18)
    return [sthick("M3.6 9.6L20.4 9.6", 1.5), solid(circle(3.4, 9.6, 2)), solid(circle(20.6, 9.6, 2)), shell(circle(12, 9.8, 2.4)),
            shell(ellipse(12, 16, 3.6, 4.4)), shell(cut_wing(wl, ellipse(12, 16, 3.6, 4.4), g=1.2)), shell(flip(cut_wing(wl, ellipse(12, 16, 3.6, 4.4), g=1.2))),
            sthick("M9.6 19L8 21.8", 1.2), sthick("M14.4 19L16 21.8", 1.2)]


@icon("fly-face", CAT, "Front view of a fly head with two huge compound eyes, short antennae and a sponge mouthpart",
      tags=["compound eyes", "head", "fly", "insect portrait", "macro", "mouthparts", "bug"])
def _(S):
    el = ellipse(7.4, 11, 4.5, 5.6)
    parts = [shell(el), shell(flip(el))]
    for x, y in ((6, 9), (8.8, 9.8), (6.6, 12.6)):
        parts += [dot(x, y, 0.75), dot(24 - x, y, 0.75)]
    parts += [line(poly([(11.2, 5.8), (10, 2.8)], r=S.r)), line(poly([(12.8, 5.8), (14, 2.8)], r=S.r)), line(seg(12, 16.6, 12, 18)),
              shell(ellipse(12, 20, 2.8, 1.8))]
    return parts


@icon("maggot", CAT, "Side view of a smooth tapered legless larva with ring segment lines, pointed at the head end",
      tags=["fly larva", "larvae", "decay", "fishing bait", "forensic", "worm", "insect"])
def _(S):
    body = L(S, "M2.4 12C5 8.4 12 7.4 20 8.8C21.8 10 21.8 14 20 15.2C12 16.6 5 15.6 2.4 12Z",
             "M2.8 12C4.6 9 11.6 7.4 19.6 8.6C22 9.6 22 14.4 19.6 15.4C11.6 16.6 4.6 15 2.8 12Z")
    return [shell(body), detail("M7 9.8C8 11.2 8 12.8 7 14.2"), detail("M10.8 8.8C11.8 10.8 11.8 13.2 10.8 15.2"),
            detail("M14.6 8.6C15.6 10.8 15.6 13.2 14.6 15.4"), detail("M18.2 9C19 10.8 19 13.2 18.2 15")]


@icon("grub", CAT, "Side view of a plump C-shaped white larva with a small round head and short legs near the front",
      tags=["white grub", "beetle larva", "lawn pest", "soil", "larva", "scarab larva", "insect"])
def _(S):
    body = thick(arc(11, 12.6, 5.2, 75, 310), 6.4, S)
    return [shell(union(body, circle(16.4, 6.6, 2.8))), dot(17.4, 6, 0.8), detail(seg(3.6, 11, 6.4, 11.6)), detail(seg(4.4, 15.4, 7, 14.4)),
            detail(seg(7.6, 19, 9, 16.8)), sthick("M14.2 11.4L16 13.4", 1.3), sthick("M13.8 14L15.2 16.4", 1.3)]


@icon("dragonfly", CAT, "Top view of a dragonfly with a long straight segmented tail and four long wings held flat and open",
      tags=["odonata", "pond", "flying insect", "summer", "wings", "mosquito hawk", "insect"])
def _(S):
    thorax = ellipse(12, 8.4, 2, 2.2)
    fw = cut_wing(lens(S, 7.2, 5.8, 4.8, 1.4, -10), thorax, g=1.2)
    hw = cut_wing(lens(S, 7.2, 11.6, 4.8, 1.4, 10), thorax, g=1.2)
    tail = minus(rect(10.9, 10.4, 2.2, 11.2), rect(10, 13.2, 4, 0.9), rect(10, 16, 4, 0.9), rect(10, 18.8, 4, 0.9))
    return [shell(fw), shell(flip(fw)), shell(hw), shell(flip(hw)), shell(union(circle(12, 4.4, 2), thorax)), solid(tail)]


@icon("damselfly", CAT, "Side view of a slender damselfly resting on a stem with its wings folded together above its thin body",
      tags=["odonata", "pond", "slender", "stem", "wings folded", "insect", "blue damselfly"])
def _(S):
    w = cut_wing(wing(14.2, 8, 6.6, 1.15, 4), union(circle(5, 11.6, 1.8), ellipse(8.8, 11.8, 2.2, 1.8)), g=1.6)
    return [shell(w), shell(union(circle(5, 11.6, 1.8), ellipse(8.8, 11.8, 2.2, 1.8))), sthick("M10.6 12.4L21 13.4", 1.8),
            sthick("M7.8 13.4L7 16", 1.2), sthick("M9.4 13.6L10 16.4", 1.2), line(seg(2, 17.6, 22, 16.4))]


@icon("mayfly", CAT, "Side view of a delicate fly with upright wings and two or three very long thin tail filaments",
      tags=["ephemeroptera", "fishing fly", "aquatic insect", "one day", "short lived", "insect", "dun"])
def _(S):
    body = union(circle(5.2, 14, 1.7), ellipse(8.6, 14, 2.2, 1.8))
    w1 = cut_wing(rot(lens(S, 10, 7, 5.4, 2.6, 0), 90 + 14, 10, 7), body, g=1.5)
    w2 = cut_wing(rot(lens(S, 14.4, 11.2, 2.6, 1.7, 0), 90 + 30, 14.4, 11.2), body, g=1.5)
    return [shell(w1), shell(w2), shell(body), sthick("M10.6 15L15.4 16.4", 1.6), sthick("M15 16.4C17.6 15 19.6 13.6 21.6 11.4", 1.0),
            sthick("M15.2 16.6C18.2 17 20 17.8 21.8 18.8", 1.0), sthick("M15 16.8C16.8 19 18.4 20.6 20.2 21.8", 1.0),
            sthick("M7.4 15.6L6 19.6", 1.2), sthick("M9.2 15.8L9.6 20", 1.2)]


@icon("lacewing", CAT, "Top view of a slim insect with large clear net-veined wings folded like a roof and long antennae",
      tags=["chrysopidae", "green lacewing", "aphid lion", "garden helper", "net wings", "insect", "beneficial"])
def _(S):
    body = union(circle(12, 5.4, 1.5), ellipse(12, 8.8, 1.5, 1.8))
    abd = ellipse(12, 15.6, 1.8, 5.2)
    w = cut_wing(wing(8.8, 14.4, 3.6, 8.4, 9), body, abd, g=1.2)
    return [shell(w), shell(flip(w)), shell(body), shell(abd), detail(seg(9.4, 9.8, 8, 20)), detail(seg(14.6, 9.8, 16, 20))] + sym_lines(S, [(11.2, 4.4), (8.6, 1.8), (5.4, 3.4)])
