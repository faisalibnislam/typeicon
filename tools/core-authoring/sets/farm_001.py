"""TypeIcon Core: garden and farm equipment, structures and water works (batch farm_001).

Original drawings from the objects themselves. Long tools stand upright; short hand tools are turned 45 degrees.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path

CAT = "farm"


def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def mark(d) -> Part:
    """Small solid shape: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def rot(pts, deg=45, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rsg(x1, y1, x2, y2, deg=45):
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg)
    return seg(a, b, c, d)


def rpl(pts, deg=45, closed=False, r=0.0):
    return poly(rot(pts, deg), closed=closed, r=r)


def rrect(x, y, w, h, rx=0.0, deg=45):
    """Rotated rounded rectangle."""
    rx = max(0.0, min(rx, w / 2, h / 2))
    pts = [(x + rx, y), (x + w - rx, y), (x + w, y + rx), (x + w, y + h - rx), (x + w - rx, y + h),
           (x + rx, y + h), (x, y + h - rx), (x, y + rx)]
    if rx == 0:
        return rpl([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], deg, closed=True)
    # build with arcs, rotating the endpoints (arcs are rotation invariant)
    q = rot(pts, deg)
    f = lambda p: f"{fmt(p[0])} {fmt(p[1])}"
    a = f"A{fmt(rx)} {fmt(rx)} 0 0 1 "
    return (f"M{f(q[0])}L{f(q[1])}{a}{f(q[2])}L{f(q[3])}{a}{f(q[4])}L{f(q[5])}{a}{f(q[6])}L{f(q[7])}{a}{f(q[0])}Z")


def orect(cx, cy, w, h, rx=0.0, deg=0.0):
    """Rounded rectangle centred on (cx, cy), turned clockwise by deg about its own centre."""
    x, y = cx - w / 2, cy - h / 2
    rx = max(0.0, min(rx, w / 2, h / 2))
    if rx == 0:
        return poly(rot([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], deg, cx, cy), closed=True)
    pts = [(x + rx, y), (x + w - rx, y), (x + w, y + rx), (x + w, y + h - rx), (x + w - rx, y + h),
           (x + rx, y + h), (x, y + h - rx), (x, y + rx)]
    q = rot(pts, deg, cx, cy)
    f = lambda p: f"{fmt(p[0])} {fmt(p[1])}"
    a = f"A{fmt(rx)} {fmt(rx)} 0 0 1 "
    return f"M{f(q[0])}L{f(q[1])}{a}{f(q[2])}L{f(q[3])}{a}{f(q[4])}L{f(q[5])}{a}{f(q[6])}L{f(q[7])}{a}{f(q[0])}Z"


def rotd(d, deg, cx=12.0, cy=12.0):
    """Rotate a path string clockwise by deg about (cx, cy)."""
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rdot(x, y, r=1.25, deg=45):
    (a, b), = rot([(x, y)], deg)
    return dot(a, b, r)


def bz(p0, p1, p2, p3, n=12):
    """Points along a cubic bezier."""
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return out


# ============================================================================ hand tools

@icon("digging-fork", CAT, "Upright garden digging fork with a D-shaped handle and four straight tines",
      tags=["spading fork", "garden fork", "dig", "soil", "gardening", "tool", "turn soil"], aliases=["spading-fork"])
def _(S):
    e = L(S, 21.5, 21)
    return [
        shell(rect(7.5, 2.5, 9, 5, rr(S, 2.5))),
        line(seg(12, 7.5, 12, 12.5)),
        line(seg(5, 12.5, 19, 12.5)),
        *[line(seg(x, 12.5, x, e)) for x in (5, 9.67, 14.33, 19)],
    ]


@icon("draw-hoe", CAT, "Garden hoe with a long handle and a flat blade set at a right angle",
      tags=["hoe", "weeding", "garden tool", "cultivate", "soil", "gardening", "weed"], aliases=["garden-hoe"])
def _(S):
    return [
        line(seg(8, 2.5, 8, 16)),
        shell(rect(8, 16, 12, 4.5, rr(S, 1.5))),
    ]


@icon("stirrup-hoe", CAT, "Long-handled stirrup hoe with an open rectangular loop blade",
      tags=["loop hoe", "scuffle hoe", "weeding", "garden tool", "oscillating hoe", "weed", "soil"], aliases=["loop-hoe"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 14)),
        line(rect(4, 14, 16, 6.5, L(S, 1, 3))),
    ]


@icon("hand-fork", CAT, "Small hand fork with three tines and a round grip, shown at a slant",
      tags=["trowel fork", "hand tool", "weeding", "garden", "soil", "gardening", "cultivate"], aliases=["garden-hand-fork"])
def _(S):
    return [
        shell(rrect(10, 14, 4, 7.5, rr(S, 2))),
        line(rsg(12, 9, 12, 14)),
        line(rsg(8.5, 9, 15.5, 9)),
        *[line(rsg(x, 9, x, L(S, 2.5, 3))) for x in (8.5, 12, 15.5)],
    ]


@icon("hand-cultivator", CAT, "Hand cultivator with three curved claw prongs on a short handle",
      tags=["claw", "hand tool", "weeder", "garden", "loosen soil", "gardening", "tiller"], aliases=["garden-claw"])
def _(S):
    curls = []
    for x in (7, 11.5, 16):
        curls.append(line(poly(rot(bz((x, 12), (x, 9), (x - 1, 6.5), (x - 4, 6.5)), 45), r=0)))
    return [
        shell(rrect(10, 15.5, 4, 6, rr(S, 2))),
        line(rsg(12, 12, 12, 15.5)),
        line(rpl([(7, 12), (16, 12)])),
        *curls,
    ]


@icon("pruning-shears", CAT, "Bypass pruning shears with a hooked blade, a pivot and two chunky handles",
      tags=["secateurs", "pruners", "garden", "prune", "cut branches", "hand pruner", "clippers"], aliases=["secateurs"])
def _(S):
    g = rr(S, 2)
    return [
        line(seg(9.5, 12.5, 9.5, 3)),
        line("M16.5 12.5C16.5 7.5 14 4.5 10.5 3"),
        shell(orect(9.5, 17.6, 4.6, 8.8, g, 5)),
        shell(orect(16.6, 17.6, 4.6, 8.8, g, -12)),
        dot(13, 10.5, 1.2),
    ]


@icon("loppers", CAT, "Long-handled loppers with crossed handles and a hooked cutting head",
      tags=["pruners", "branch cutter", "garden", "prune", "long handle", "trees", "shrubs"], aliases=["branch-loppers"])
def _(S):
    g = rr(S, 1.8)
    return [
        line(seg(14.5, 3.5, 8.4, 14.5)),
        line(seg(9.5, 3.5, 15.6, 14.5)),
        line("M14.5 3.5Q16.8 2.5 17.5 5"),
        shell(orect(6.56, 17.8, 3.6, 7.6, g, 29)),
        shell(orect(17.44, 17.8, 3.6, 7.6, g, -29)),
        dot(12, 8, 1.3),
    ]


@icon("pruning-saw", CAT, "Curved pruning saw with a toothed inner edge and a pistol grip",
      tags=["hand saw", "garden saw", "branch", "prune", "cut", "trees", "lopping"], aliases=["garden-saw"])
def _(S):
    outer = bz((15, 6), (8, 3.5), (3, 7), (2.5, 14.5), 12)
    # the tip is at the bottom left; the inner (toothed) edge runs back to the grip along the concave side
    inner = bz((2.5, 14.5), (5.5, 12), (11, 13), (15, 11), 12)
    teeth = []
    for i, (x, y) in enumerate(inner[1:-1]):
        if i % 2 == 0:
            teeth.append((x - 0.6, y + 1.9))
        else:
            teeth.append((x, y))
    blade = outer + teeth[::1] + [(15, 11)]
    return [
        shell(poly(blade, closed=True, r=0), stroke_miterlimit="2"),
        shell(rect(15, 4.5, 5, 13, rr(S, 2.5))),
        detail(seg(15, 6.5, 15, 15.5)),
    ]


@icon("pole-pruner", CAT, "Tall pole pruner with a hooked blade at the top and a pull cord",
      tags=["tree pruner", "long reach pruner", "branch cutter", "garden", "pole saw", "trees", "prune"], aliases=["tree-pruner"])
def _(S):
    return [
        line(seg(7, 21.5, 7, 7.5)),
        line("M7 7.5V6A3.5 3.5 0 0 1 10.5 2.5H16"),
        shell(poly([(9.5, 10), (16, 10), (16, 6.5)], closed=True, r=S.r * 0.5)),
        line(seg(16, 10, 16, 16.5)),
        dot(16, 19, 1.6),
    ]


@icon("grass-shears", CAT, "Hand grass shears with two long flat blades and handles angled upward",
      tags=["lawn shears", "edging shears", "grass clippers", "garden", "trim lawn", "cut grass", "hand shears"], aliases=["lawn-shears"])
def _(S):
    g = rr(S, 1.8)
    return [
        line(seg(9, 15.5, 21.5, 13.5)),
        line(seg(9, 15.5, 21.5, 19.5)),
        line(seg(9, 15.5, 6.5, 11)),
        line(seg(9, 15.5, 10.5, 11)),
        shell(orect(5.16, 7.77, 3.6, 7, g, -22.7)),
        shell(orect(11.6, 7.7, 3.6, 7, g, 18.4)),
    ]


@icon("half-moon-edger", CAT, "Lawn edger with a half-moon blade at the foot of a T-handled shaft",
      tags=["lawn edger", "edging", "spade", "border", "garden tool", "turf cutter", "lawn"], aliases=["lawn-edger"])
def _(S):
    r = 7
    blade = f"M5 13.5H19A7 7 0 0 1 5 13.5Z" if S.name == "line" else "M6.5 13.5H17.5A7 7 0 0 1 6.5 13.5Z"
    return [
        line(seg(8, 2.5, 16, 2.5)),
        line(seg(12, 2.5, 12, 13.5)),
        shell(blade),
    ]


@icon("bulb-planter", CAT, "Tapered hollow bulb planter with a crossbar handle and a cutaway slot",
      tags=["bulb digger", "plant bulbs", "garden tool", "corer", "spring bulbs", "tulips", "hole"], aliases=["bulb-digger"])
def _(S):
    return [
        line(seg(7, 2.5, 17, 2.5)),
        line(seg(12, 2.5, 12, 7)),
        shell(poly([(7, 7), (17, 7), (15, 21.5), (9, 21.5)], closed=True, r=S.r)),
        detail(seg(12, 11, 12, 18.5)),
    ]


@icon("dibber", CAT, "Pointed wooden dibber with a T-shaped handle and depth rings on the shaft",
      tags=["dibble", "seed planting", "garden tool", "hole maker", "seedlings", "sowing", "transplant"], aliases=["dibble"])
def _(S):
    return [
        shell(rrect(7.5, 2, 9, 3.5, rr(S, 1.75))),
        shell(rpl([(9.5, 5.5), (14.5, 5.5), (14.5, 15.5), (12, 21.5), (9.5, 15.5)], closed=True, r=S.r * 0.6)),
        detail(rsg(9.5, 9, 14.5, 9)),
        detail(rsg(9.5, 12.5, 14.5, 12.5)),
    ]


@icon("soil-sieve", CAT, "Round garden riddle with a square mesh and fine soil falling through",
      tags=["riddle", "soil sifter", "garden sieve", "compost", "sift", "mesh", "potting"], aliases=["garden-riddle"])
def _(S):
    return [
        shell(circle(12, 9.5, 7.5)),
        detail(seg(9.5, 3, 9.5, 16)),
        detail(seg(14.5, 3, 14.5, 16)),
        detail(seg(5, 7.5, 19, 7.5)),
        detail(seg(5, 12, 19, 12)),
        *([mark(rect(6.8, 18.8, 2.4, 2.4)), mark(rect(10.8, 19.8, 2.4, 2.4)), mark(rect(14.8, 18.8, 2.4, 2.4))] if S.name == 'line' else
          [dot(8, 20, 1.3), dot(12, 21, 1.3), dot(16, 20, 1.3)]),
    ]


@icon("dandelion-weeder", CAT, "Long-shafted weeder with a forked fishtail tip and a round handle",
      tags=["weeder", "weed puller", "lawn weeds", "garden tool", "root remover", "dandelion", "gardening"], aliases=["weed-puller"])
def _(S):
    return [
        shell(rect(8.5, 2.5, 7, 6, rr(S, 3))),
        line(seg(12, 8.5, 12, 13.5)),
        shell(poly([(10, 13.5), (14, 13.5), (15.5, 21.5), (12, 18.5), (8.5, 21.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("scythe", CAT, "Long curved scythe with a hand grip and a sweeping blade",
      tags=["harvest", "mow", "grass cutter", "reaper", "hay", "farm tool", "cut grain"], aliases=["grain-scythe"])
def _(S):
    return [
        line("M5 2.5C5 9 6 14 8.5 17.5"),
        line(seg(6, 9, 10, 9)),
        shell("M8.5 17C12 12.5 17.5 11.5 21 14.5C17.5 14.5 13 17 8.5 21Z"),
    ]


@icon("sickle", CAT, "Short-handled sickle with a crescent blade curving back toward the grip",
      tags=["harvest", "cut grass", "reaping", "hand tool", "grain", "crescent blade", "farm tool"], aliases=["reaping-hook"])
def _(S):
    lune = path_to_d(D(P(circle(12, 10, 8.5)), P(circle(14.2, 12.2, 7))))
    return [
        shell(lune, stroke_miterlimit="3"),
        shell(orect(6.5, 18, 3.8, 7.5, rr(S, 1.9), -45)),
    ]


@icon("billhook", CAT, "Billhook with a short handle and a broad blade hooked at the tip",
      tags=["hedge knife", "brush cutter", "hooked blade", "coppice", "farm tool", "clear brush", "hedging"], aliases=["brush-hook"])
def _(S):
    blade = rotd("M7.5 14V7C7.5 4 10 2.5 13.5 2.5C16 2.5 17.8 3.4 18.5 5C16.2 5.2 15 6.5 15 9.5L16 14Z", 18)
    return [
        shell(blade, stroke_miterlimit="3"),
        shell(orect(*rot([(11.7, 17.8)], 18)[0], 5.5, 7.5, rr(S, 2.5), 18)),
    ]


@icon("broadfork", CAT, "Wide broadfork with two tall handles and a row of long vertical tines",
      tags=["garden fork", "soil aeration", "no-dig", "loosen soil", "market garden", "tool", "spading"], aliases=["grelinette"])
def _(S):
    e = L(S, 21.5, 21)
    return [
        line(seg(4, 3, 4, 11.5)),
        line(seg(20, 3, 20, 11.5)),
        line(seg(4, 11.5, 20, 11.5)),
        *[line(seg(x, 11.5, x, e)) for x in (4, 8, 12, 16, 20)],
    ]


@icon("wheel-hoe", CAT, "Push wheel hoe with a front wheel, a hoe blade behind it and a long handle",
      tags=["wheel cultivator", "weeding", "garden tool", "push hoe", "market garden", "rows", "cultivate"], aliases=["push-hoe"])
def _(S):
    return [
        shell(circle(7, 15, 5)),
        dot(7, 15, 1.2),
        line(poly([(7, 15), (11.5, 11), (21, 3.5)])),
        line(seg(12.5, 10.3, 16, 18)),
        shell(rect(13, 18, 8, 3, rr(S, 1.5))),
    ]


@icon("soil-knife", CAT, "Straight garden soil knife with a notched blade, guard and grip handle",
      tags=["hori hori", "digging knife", "weeding knife", "trowel knife", "garden tool", "planting", "transplant"], aliases=["hori-hori"])
def _(S):
    return [
        shell(rpl([(12, 2), (15.5, 5.5), (15.5, 12.5), (8.5, 12.5), (8.5, 5.5)], closed=True, r=S.r * 0.5)),
        detail(rsg(8.5, 7, 11.5, 7)),
        detail(rsg(8.5, 9.75, 11.5, 9.75)),
        line(rsg(7, 13.5, 17, 13.5)),
        shell(rrect(9.5, 13.5, 5, 8, rr(S, 2))),
    ]


@icon("pruning-knife", CAT, "Folding pruning knife with a slim hooked blade and a wooden handle",
      tags=["budding knife", "grafting knife", "garden knife", "prune", "hooked blade", "orchard", "cut"], aliases=["garden-knife"])
def _(S):
    blade = rotd("M10 13.5V8C10 4.5 11.5 2.5 14.5 2.5C16.5 2.5 17 3.5 16.5 4.8C14.2 4.6 13.5 6.5 14 9.5L14 13.5Z", 28)
    return [
        shell(blade, stroke_miterlimit="3"),
        shell(orect(11.6, 17.8, 5, 8.5, rr(S, 2.5), 28)),
        dot(*rot([(12, 14.5)], 28)[0], 1.0),
    ]


@icon("garden-kneeler", CAT, "Kneeling pad on a low frame with two upright side rails for standing up",
      tags=["kneeling bench", "gardening seat", "knee pad", "garden stool", "weeding", "comfort", "flip bench"], aliases=["kneeling-bench"])
def _(S):
    return [
        line(poly([(5, 11.5), (5, 4.5), (19, 4.5), (19, 11.5)], r=S.r)),
        shell(rect(3, 11.5, 18, 4.5, rr(S, 2.2))),
        line(seg(6.5, 16, 5.5, 21.5)),
        line(seg(17.5, 16, 18.5, 21.5)),
    ]


@icon("garden-trug", CAT, "Shallow wooden trug basket made of curved slats with a high arched handle",
      tags=["trug basket", "harvest basket", "flower basket", "gathering", "garden", "wooden basket", "sussex trug"], aliases=["trug-basket"])
def _(S):
    return [
        line("M6 11.5A6 6 0 0 1 18 11.5" if False else "M5.5 11V9A6.5 6.5 0 0 1 18.5 9V11"),
        shell("M2.5 11H21.5C21.5 16.5 18 20.5 12 20.5C6 20.5 2.5 16.5 2.5 11Z"),
        detail("M3.6 14.7H20.4"),
        detail("M6.8 17.7H17.2"),
    ]


@icon("leaf-scoops", CAT, "Pair of wide hand scoops with finger slots, held together to lift leaves",
      tags=["leaf grabber", "leaf claws", "yard work", "rake", "pick up leaves", "garden cleanup", "hand scoops"], aliases=["leaf-grabbers"])
def _(S):
    return [
        shell(poly([(4, 3), (8, 3), (11, 21), (3, 21)], closed=True, r=S.r + 0.5)),
        shell(poly([(20, 3), (16, 3), (13, 21), (21, 21)], closed=True, r=S.r + 0.5)),
        detail(seg(5.6, 7.5, 6.6, 12.5)),
        detail(seg(18.4, 7.5, 17.4, 12.5)),
    ]


@icon("garden-twine", CAT, "Ball of garden twine wound in loops with a loose end trailing off",
      tags=["string", "cord", "jute", "tie plants", "yarn ball", "support", "garden supplies"], aliases=["twine-ball"])
def _(S):
    return [
        shell(circle(10.5, 10.5, 7.5)),
        detail("M3.8 8.5C8 11 13 10.5 17 7.5"),
        detail("M5 14.5C8.5 11.5 12 8.5 13.5 3.8"),
        line("M14.5 16.5C15 20.5 18 21.5 19.5 19C20.5 17.5 21.8 18.5 21.5 21"),
    ]


@icon("hose-reel", CAT, "Drum of coiled hose on a small frame with the hose end trailing out",
      tags=["garden hose", "hose holder", "hose winder", "watering", "coil", "water", "reel"], aliases=["hose-winder"])
def _(S):
    return [
        shell(circle(11, 9.5, 7.5)),
        detail("M11 9.5A1.5 1.5 0 0 1 14 9.5A3 3 0 0 1 8 9.5A4 4 0 0 1 16 9.5"),
        line("M17.5 14.5C19.5 17.5 18.5 20 21.5 20"),
        line(poly([(6, 21.5), (11, 17.5), (16, 21.5)])),
    ]


@icon("hose-nozzle", CAT, "Pistol-grip hose spray nozzle with a trigger and a fan of spray",
      tags=["spray gun", "garden hose", "watering", "spray nozzle", "trigger", "water jet", "sprayer"], aliases=["spray-nozzle"])
def _(S):
    return [
        shell(rect(3, 5.5, 12, 5, rr(S, 2))),
        shell(orect(6.6, 15.8, 5, 10.5, rr(S, 2.5), 12)),
        line(seg(10.5, 10.5, 11.8, 14.5)),
        line(seg(18.2, 5.5, 21.5, 3.5)),
        line(seg(18.2, 8, 22, 8)),
        line(seg(18.2, 10.5, 21.5, 12.5)),
    ]


@icon("backpack-sprayer", CAT, "Knapsack pressure sprayer with a tank, shoulder strap, pump lever and spray lance",
      tags=["pump sprayer", "knapsack sprayer", "pesticide", "garden spray", "crop spraying", "weed killer", "tank"], aliases=["knapsack-sprayer"])
def _(S):
    return [
        shell(rect(4, 5.5, 9, 14, rr(S, 3.5))),
        shell(rect(6.5, 2.5, 4, 3, rr(S, 1))),
        detail("M3.5 9C1.5 11.5 1.5 14 3.5 16.5") if False else detail(seg(4, 10, 13, 10)),
        line("M13 13C16.5 13 17 15 17 17"),
        line(seg(17, 17, 21.5, 21.5)),
        line(seg(13, 8, 19, 5)),
        dot(19.2, 4.9, 1.3),
    ]


@icon("leaf-blower", CAT, "Handheld leaf blower with a top handle and a long tube blowing air",
      tags=["yard work", "garden cleanup", "blow leaves", "blower", "autumn", "air", "power tool"], aliases=["garden-blower"])
def _(S):
    return [
        shell(rect(2.5, 9, 8.5, 9, rr(S, 3))),
        line(poly([(4.5, 9), (4.5, 5), (9, 5), (9, 9)], r=S.r)),
        shell(poly([(11, 10.5), (17.5, 11), (17.5, 15.5), (11, 16)], closed=True, r=S.r * 0.6)),
        line(seg(19.5, 10, 22, 10)),
        line(seg(19.5, 13.25, 22, 13.25)),
        line(seg(19.5, 16.5, 22, 16.5)),
    ]


def leaf(cx, top, bottom, w, S=None):
    """Vertical leaf from top to bottom, width w. Line: pointed tips; Rounded: softer tips."""
    my = (top + bottom) / 2
    k = w * (0.66 if S is None or S.name == "line" else 0.72)
    a = 0.35 if S is None or S.name == "line" else 0.2
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + k)} {fmt(top + (my - top) * a)} {fmt(cx + k)} {fmt(bottom - (bottom - my) * a)} {fmt(cx)} {fmt(bottom)}"
            f"C{fmt(cx - k)} {fmt(bottom - (bottom - my) * a)} {fmt(cx - k)} {fmt(top + (my - top) * a)} {fmt(cx)} {fmt(top)}Z")


def leaf_at(base, tip, w, S=None):
    """Leaf from base point to tip point."""
    bx, by = base
    tx, ty = tip
    ln = math.hypot(tx - bx, ty - by)
    deg = math.degrees(math.atan2(tx - bx, -(ty - by)))
    return rotd(leaf(bx, by - ln, by, w, S), deg, bx, by)


def wave(x0, x1, y, amp=1.3, step=4.0):
    """Wavy line from x0 to x1 (quadratic bezier chain)."""
    d = f"M{fmt(x0)} {fmt(y)}Q{fmt(x0 + step / 2)} {fmt(y - 2 * amp)} {fmt(x0 + step)} {fmt(y)}"
    x = x0 + step
    while x + step <= x1 + 1e-6:
        x += step
        d += f"T{fmt(x)} {fmt(y)}"
    return d


def star(cx, cy, ro, ri, n, start=-90.0):
    pts = []
    for i in range(2 * n):
        pts.append(polar(cx, cy, ro if i % 2 == 0 else ri, start + i * 180 / n))
    return pts


def clip_diag(x0, y0, x1, y1, c, kind):
    """Segment of the line x+y=c (kind '+') or x-y=c (kind '-') inside the box, or None."""
    pts = []
    for x in (x0, x1):
        y = (c - x) if kind == "+" else (x - c)
        if y0 - 1e-6 <= y <= y1 + 1e-6:
            pts.append((x, y))
    for y in (y0, y1):
        x = (c - y) if kind == "+" else (c + y)
        if x0 - 1e-6 <= x <= x1 + 1e-6:
            pts.append((x, y))
    pts = sorted(set((round(a, 3), round(b, 3)) for a, b in pts))
    if len(pts) < 2:
        return None
    return pts[0], pts[-1]


# ============================================================================ power tools and lawn care

@icon("string-trimmer", CAT, "String trimmer with a motor at the top, a long shaft, a side handle and a spinning cord head",
      tags=["weed eater", "weed whacker", "line trimmer", "strimmer", "lawn edging", "grass", "garden power tool"], aliases=["weed-eater"])
def _(S):
    return [
        shell(rrect(9, 2.5, 6, 5, rr(S, 2))),
        line(rsg(12, 7.5, 12, 18)),
        line(rsg(12, 12.5, 17, 12.5)),
        shell(rrect(8.5, 18, 7, 3, rr(S, 1.5))),
        line(rsg(8.5, 19.5, 5.5, 19.5)),
        line(rsg(15.5, 19.5, 18.5, 19.5)),
    ]


@icon("rototiller", CAT, "Rototiller with an engine above a spiky tine wheel and handlebars angled back",
      tags=["garden tiller", "cultivator", "soil tiller", "till", "dig", "plow", "garden power tool"], aliases=["garden-tiller"])
def _(S):
    return [
        shell(rect(4, 4.5, 11, 6, rr(S, 2))),
        shell(poly(star(9.5, 16.5, 6, 4, 9), closed=True, r=S.r * 0.4), stroke_miterlimit="3"),
        line(seg(15, 7, 21.5, 3)),
        line(seg(15, 9.5, 21.5, 9)),
    ]


@icon("lawn-aerator", CAT, "Push lawn aerator with a spiked roller, a long handle and small holes in the grass",
      tags=["spike aerator", "core aerator", "lawn care", "grass", "aerate", "turf", "roller"], aliases=["spike-aerator"])
def _(S):
    return [
        shell(poly(star(8.5, 14.5, 6.5, 4.6, 8, -90 + 22.5), closed=True, r=S.r * 0.3), stroke_miterlimit="3"),
        line(seg(8.5, 14.5, 20, 3)),
        dot(16.5, 19.5, 1.3),
        dot(20.5, 19.5, 1.3),
    ]


@icon("lawn-roller", CAT, "Wide smooth lawn roller drum with a U-shaped pull handle",
      tags=["garden roller", "grass", "lawn care", "flatten", "seed", "turf", "compact"], aliases=["garden-roller"])
def _(S):
    return [
        line(poly([(5.5, 14), (8.5, 4.5), (15.5, 4.5), (18.5, 14)], r=S.r)),
        shell(rect(2.5, 14, 19, 7, rr(S, 3.5))),
        detail(seg(7, 14.5, 7, 20.5)),
    ]


@icon("lawn-spreader", CAT, "Push lawn spreader with an open hopper on wheels and granules scattering below",
      tags=["seed spreader", "fertilizer spreader", "broadcast spreader", "lawn care", "grass seed", "granules", "feed"], aliases=["seed-spreader"])
def _(S):
    return [
        shell(poly([(3.5, 4.5), (15, 4.5), (13, 13), (5.5, 13)], closed=True, r=S.r)),
        shell(circle(16.5, 17, 3.5)),
        line(seg(14, 8, 21.5, 2.5)),
        dot(4.5, 17.5, 1.2), dot(8.5, 19.5, 1.2), dot(6, 21, 1.2), dot(10.5, 16.5, 1.2),
    ]


@icon("riding-mower", CAT, "Small ride-on lawn tractor with a seat, steering wheel and mower deck",
      tags=["lawn tractor", "ride on mower", "grass cutting", "lawn care", "garden tractor", "mowing", "yard"], aliases=["lawn-tractor"])
def _(S):
    return [
        shell(circle(16.5, 16.5, 4.5)),
        shell(rect(2.5, 9.5, 10, 5, rr(S, 2))),
        shell(circle(5.5, 19.5, 2.4)),
        line("M14 4V9"),
        line(seg(14, 9, 19, 9)),
        line(seg(9, 9.5, 9.6, 4.5)),
        line(seg(6.8, 4.5, 11.8, 4.5)),
    ]


@icon("wood-chipper", CAT, "Wheeled wood chipper with a wide intake funnel and a curved discharge chute",
      tags=["wood shredder", "tree service", "branch chipper", "mulch", "arborist", "garden power tool", "chip"], aliases=["wood-shredder"])
def _(S):
    return [
        shell(poly([(2.5, 4), (9, 4), (11, 11), (5, 11)], closed=True, r=S.r * 0.6)),
        shell(rect(8, 11, 13, 7, rr(S, 2))),
        line("M17.5 11V7.5C17.5 4.5 19.5 3.5 21.5 5"),
        shell(circle(13.5, 20, 2)),
    ]


# ============================================================================ beds, frames and structures

@icon("raised-bed", CAT, "Plank-sided raised planter bed with small plants sprouting in a row",
      tags=["garden bed", "planter box", "vegetable bed", "grow box", "raised garden", "soil", "allotment"], aliases=["planter-bed"])
def _(S):
    sprouts = []
    for x in (6.5, 12, 17.5):
        sprouts.append(line(f"M{fmt(x)} 11.5V8M{fmt(x)} 9.5C{fmt(x)} 7.5 {fmt(x - 1.3)} 6.3 {fmt(x - 2.4)} 6.3M{fmt(x)} 9.5C{fmt(x)} 7.5 {fmt(x + 1.3)} 6.3 {fmt(x + 2.4)} 6.3"))
    return [
        *sprouts,
        shell(rect(2.5, 11.5, 19, 9.5, rr(S, 1.5))),
        detail(seg(3, 16.25, 21, 16.25)),
    ]


@icon("cold-frame", CAT, "Low wooden frame box with a sloping glass lid propped open on a stick",
      tags=["cloche", "hotbed", "seed hardening", "mini greenhouse", "glass lid", "season extension", "garden frame"], aliases=["garden-cold-frame"])
def _(S):
    return [
        shell(poly([(3, 20.5), (3, 13), (21, 16.5), (21, 20.5)], closed=True, r=S.r)),
        shell(orect(9.6, 7.8, 15, 2.6, rr(S, 1.3), -30)),
        line(seg(15, 8.2, 15, 14.6)),
    ]


@icon("propagator", CAT, "Seed tray propagator with a clear domed lid, a top vent and seedlings inside",
      tags=["seed starter", "seed tray", "germination", "seedlings", "grow dome", "sowing", "nursery"], aliases=["seed-propagator"])
def _(S):
    return [
        shell(rect(10, 2.5, 4, 3, rr(S, 1))),
        shell("M4 15A8 10 0 0 1 20 15Z"),
        detail("M8.5 15V12M8.5 12C8.5 10.8 7.6 10.2 6.6 10.2M8.5 12C8.5 10.8 9.4 10.2 10.4 10.2") if False else
        detail("M9 15V11.5M9 11.5C9 10 7.6 9.3 6.3 9.3M9 11.5C9 10 10.4 9.3 11.7 9.3"),
        shell(rect(2.5, 15, 19, 6, rr(S, 1.5))),
    ]


@icon("potting-bench", CAT, "Potting bench with a back shelf holding a plant pot and a soil bag on the top",
      tags=["potting table", "garden workbench", "planting station", "greenhouse", "repotting", "shed", "work table"], aliases=["potting-table"])
def _(S):
    return [
        line(seg(3, 13.5, 21, 13.5)),
        line(seg(5, 13.5, 5, 21.5)),
        line(seg(19, 13.5, 19, 21.5)),
        line(seg(5, 18, 19, 18)),
        shell(poly([(5, 4), (10.5, 4), (9.5, 9), (6, 9)], closed=True, r=S.r * 0.4)),
        line(seg(3, 9, 12.5, 9)),
        shell(rect(14, 6.5, 6, 7, rr(S, 1.5))),
    ]


@icon("potting-soil", CAT, "Soft sack of potting compost with a folded top, a leaf mark and soil spilling at the base",
      tags=["compost bag", "potting mix", "soil bag", "growing medium", "garden supplies", "peat", "planting"], aliases=["potting-mix"])
def _(S):
    return [
        shell(poly([(6, 3.5), (18, 3.5), (19.5, 19), (4.5, 19)], closed=True, r=S.r)),
        detail(seg(6.3, 6.5, 17.7, 6.5)),
        detail("M12 16.5C8.5 14.5 9 11 14.5 10C15.5 14 15 15.5 12 16.5Z"),
        dot(2.8, 20.6, 1.2), dot(5.6, 21.7, 1.0), dot(21, 20.8, 1.2),
    ]


@icon("tomato-cage", CAT, "Conical wire cage of stacked rings held by legs, with a leafy sprout and a tomato inside",
      tags=["plant support", "tomato support", "garden cage", "trellis", "vegetable garden", "climbing", "stake"], aliases=["plant-cage"])
def _(S):
    def x_at(y, side):
        t = (y - 11) / 10.5
        return 12 + side * (4 + 4.5 * t)
    parts = [
        line(seg(x_at(11, -1), 11, x_at(21.5, -1), 21.5)),
        line(seg(x_at(11, 1), 11, x_at(21.5, 1), 21.5)),
    ]
    for y in (11, 16.2, 21.5):
        parts.append(line(seg(x_at(y, -1), y, x_at(y, 1), y)))
    parts.append(line(seg(12, 11, 12, 7)))
    parts.append(shell(leaf_at((12, 8.5), (6.5, 3.5), 3.4, S)))
    parts.append(shell(leaf_at((12, 8.5), (17.5, 3.5), 3.4, S)))
    parts.append(dot(12, 13.6, 1.3))
    return parts


@icon("bean-poles", CAT, "Teepee of three tall poles tied at the top with a bean vine winding up the poles",
      tags=["bean teepee", "pole beans", "climbing plants", "garden support", "wigwam", "vegetable garden", "runner beans"], aliases=["bean-teepee"])
def _(S):
    return [
        line(seg(12, 3, 4.5, 21.5)),
        line(seg(12, 3, 12, 21.5)),
        line(seg(12, 3, 19.5, 21.5)),
        line("M9 18.5C9 15.5 15 15.5 15 12.5C15 10 10.5 9.8 11 8"),
        dot(12, 3, 1.8),
    ]


@icon("garden-trellis", CAT, "Diagonal lattice trellis panel for climbing plants",
      tags=["lattice", "plant support", "climbing plants", "fence panel", "vine", "garden structure", "wooden trellis"], aliases=["lattice-trellis"])
def _(S):
    x0, y0, x1, y1 = 4, 3, 20, 21
    parts = [shell(rect(x0, y0, x1 - x0, y1 - y0, L(S, 0, 4)))]
    for c in (15, 25, 35):
        sg = clip_diag(x0, y0, x1, y1, c, "+")
        if sg:
            parts.append(detail(seg(*sg[0], *sg[1])))
    for c in (-10, 0, 10):
        sg = clip_diag(x0, y0, x1, y1, c, "-")
        if sg:
            parts.append(detail(seg(*sg[0], *sg[1])))
    return parts


@icon("garden-shed", CAT, "Small garden shed with a pitched roof, a plank door and a side window",
      tags=["tool shed", "outbuilding", "storage", "potting shed", "backyard", "wooden shed", "hut"], aliases=["tool-shed"])
def _(S):
    return [
        shell(poly([(4.5, 21), (4.5, 10), (19.5, 10), (19.5, 21)], closed=True, r=S.r * 0.5)),
        line(poly([(2.5, 10.5), (12, 3.5), (21.5, 10.5)], r=S.r)),
        detail("M6.5 21V13.5H11.5V21"),
        detail(seg(9, 13.5, 9, 21)),
        detail(rect(14, 13.5, 3.5, 3.5)),
    ]


@icon("compost-tumbler", CAT, "Barrel compost tumbler on an A-frame stand with a hatch and a turning handle",
      tags=["compost drum", "rotating composter", "compost barrel", "kitchen scraps", "recycling", "soil", "tumbling bin"], aliases=["compost-drum"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 15, 9, rr(S, 4.5))),
        detail(rect(7.5, 8.5, 5, 3, rr(S, 0.8))),
        line("M17.5 10H21.5V14.5"),
        line(seg(6.5, 14.5, 4, 21.5)),
        line(seg(13.5, 14.5, 16, 21.5)),
        line(seg(2.5, 21.5, 17.5, 21.5)),
    ]


@icon("rain-barrel", CAT, "Water butt barrel with a downpipe feeding the lid and a small tap near the base",
      tags=["water butt", "rainwater harvesting", "rain collection", "downspout", "garden water", "tap", "storage barrel"], aliases=[])
def _(S):
    return [
        line("M19.5 2.5V5H11V7.5"),
        shell("M5.5 7.5H16.5C17.5 11 17.5 17.5 16.5 21.5H5.5C4.5 17.5 4.5 11 5.5 7.5Z"),
        detail(seg(5, 11, 17, 11)),
        detail(seg(5, 17.5, 17, 17.5)),
        line("M17 19.5H20.5V22"),
    ]


@icon("drip-irrigation", CAT, "Thin drip tube with emitters letting drops fall onto small plants at the soil line",
      tags=["drip line", "micro irrigation", "watering", "emitter", "soaker", "garden watering", "water saving"], aliases=["drip-line"])
def _(S):
    parts = [line(seg(2.5, 3.5, 21.5, 3.5))]
    for x in (6, 12, 18):
        parts.append(line(seg(x, 3.5, x, 6)))
        parts.append(mark(poly([(x, 8.5), (x + 1.4, 11), (x, 13), (x - 1.4, 11)], closed=True)) if S.name == "line" else
                     mark(f"M{fmt(x)} 8.3C{fmt(x + 0.5)} 9.5 {fmt(x + 1.5)} 10.6 {fmt(x + 1.5)} 11.6A1.5 1.5 0 0 1 {fmt(x - 1.5)} 11.6C{fmt(x - 1.5)} 10.6 {fmt(x - 0.5)} 9.5 {fmt(x)} 8.3Z"))
        parts.append(line(f"M{fmt(x)} 21.5V17.5M{fmt(x)} 19.3L{fmt(x - 1.8)} 17.5M{fmt(x)} 19.3L{fmt(x + 1.8)} 17.5"))
    return parts


@icon("hedge-maze", CAT, "Square hedge maze seen from above with spiral walls leading to the centre",
      tags=["labyrinth", "garden maze", "puzzle", "topiary", "park", "estate garden", "maze game"], aliases=["garden-maze"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 2))),
        detail("M8.5 21V8.5H15.5V15.5H12"),
        dot(12, 12, 1.2),
    ]


def blob(cx, cy, rx, ry, rot_deg=0.0):
    pts = []
    for i, k in enumerate((1.0, 0.86, 1.0, 0.92, 1.0, 0.85, 0.95)):
        a = math.radians(rot_deg + i * 360 / 7)
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    return pts


@icon("stepping-stones", CAT, "Curving trail of flat irregular stepping stones laid across the lawn",
      tags=["garden path", "stone path", "walkway", "pavers", "landscaping", "trail", "flagstones"], aliases=["garden-path-stones"])
def _(S):
    r = L(S, 0.8, 2.0)
    return [
        shell(poly(blob(6.5, 18, 4.4, 3.3, 10), closed=True, r=r)),
        shell(poly(blob(15, 14.5, 4.4, 3.4, 40), closed=True, r=r)),
        shell(poly(blob(9.5, 7, 4.4, 3.3, 20), closed=True, r=r)),
    ]


@icon("bug-hotel", CAT, "Wooden insect hotel with a pitched roof and compartments of stacked canes and logs",
      tags=["insect house", "insect hotel", "wildlife garden", "pollinators", "solitary bees", "habitat", "nature"], aliases=["insect-hotel"])
def _(S):
    parts = [
        shell(rect(4, 8, 16, 13, rr(S, 1.2))),
        line(poly([(2.5, 8.5), (12, 3), (21.5, 8.5)], r=S.r)),
        detail(seg(12, 8.5, 12, 20.5)),
        detail(seg(4.5, 14.5, 19.5, 14.5)),
    ]
    for x, y in ((8, 11.4), (16, 11.4), (8, 18), (16, 18)):
        parts.append(dot(x, y, 1.0))
    return parts


@icon("fruit-cage", CAT, "Tall netted fruit cage frame over a berry bush",
      tags=["berry cage", "netting", "bird protection", "soft fruit", "allotment", "currants", "raspberries"], aliases=["berry-cage"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, L(S, 0.5, 4))),
        detail(seg(9, 3.5, 9, 8)),
        detail(seg(15, 3.5, 15, 8)),
        detail(seg(3.5, 8, 20.5, 8)),
        detail("M6 21C5 17.5 7 15.3 9.3 15.8C9.8 13 14.2 13 14.7 15.8C17 15.3 19 17.5 18 21"),
        dot(9.5, 19, 1.0), dot(14.3, 18.6, 1.0),
    ]


@icon("plant-nursery", CAT, "Tray of small potted seedlings under a simple shade canopy",
      tags=["seedlings", "saplings", "garden centre", "shade cloth", "young plants", "greenhouse", "grower"], aliases=["garden-nursery"])
def _(S):
    parts = [
        shell(poly([(2.5, 7.5), (5, 3), (19, 3), (21.5, 7.5)], closed=True, r=S.r * 0.6)),
        line(seg(5, 7.5, 5, 13)) if False else line(seg(4.5, 7.5, 4.5, 21.5)),
        line(seg(19.5, 7.5, 19.5, 21.5)),
        shell(rect(7.5, 17.5, 9, 4, rr(S, 1.2))),
    ]
    for x in (10, 14):
        parts.append(line(f"M{fmt(x)} 17.5V13.5M{fmt(x)} 15.3L{fmt(x - 1.7)} 13.5M{fmt(x)} 15.3L{fmt(x + 1.7)} 13.5"))
    return parts


@icon("staked-tree", CAT, "Young thin tree tied to a wooden stake with a loop tie",
      tags=["tree planting", "sapling", "support stake", "orchard", "tree care", "tie", "nursery tree"], aliases=["tree-stake"])
def _(S):
    return [
        shell(poly(blob(10, 7, 5, 4.6, 12), closed=True, r=L(S, 0.8, 2.6))),
        line(seg(10, 11.5, 10, 21.5)),
        shell(poly([(15.5, 21.5), (15.5, 9), (17, 6), (18.5, 9), (18.5, 21.5)], closed=True, r=S.r * 0.5)),
        line(seg(10, 15.5, 15.5, 15.5)),
    ]


@icon("tree-guard", CAT, "Spiral plastic guard wrapped around the base of a young tree trunk",
      tags=["tree protector", "rabbit guard", "trunk wrap", "sapling protection", "orchard", "spiral guard", "bark"], aliases=["spiral-tree-guard"])
def _(S):
    return [
        shell(poly(blob(12, 5.6, 4, 3.6, 25), closed=True, r=L(S, 0.8, 2.2))),
        shell(rect(8.5, 10.5, 7, 11, rr(S, 1.5))),
        detail(seg(8.5, 19.2, 15.5, 16.2)),
        detail(seg(8.5, 15.2, 15.5, 12.2)),
    ]


@icon("polytunnel", CAT, "Long polytunnel hoop house covered in plastic with ribs and a door",
      tags=["hoop house", "poly tunnel", "plastic greenhouse", "growing tunnel", "market garden", "season extension", "farm"], aliases=["hoop-house"])
def _(S):
    return [
        shell("M2.5 20.5V16C2.5 10 6 6.5 12 6.5C18 6.5 21.5 10 21.5 16V20.5Z"),
        detail(seg(7.5, 7, 7.5, 20.5)),
        detail(seg(16.5, 7, 16.5, 20.5)),
        detail(rect(10.2, 13.8, 3.6, 6.5, 0)),
    ]


@icon("vertical-farm", CAT, "Tall shelving rack with three tiers of plant trays under the grow lights",
      tags=["indoor farming", "hydroponic rack", "grow shelves", "urban farming", "controlled environment", "grow lights", "agritech"], aliases=["indoor-farm-rack"])
def _(S):
    parts = [
        line(seg(4, 3, 4, 21)),
        line(seg(20, 3, 20, 21)),
        line(seg(4, 3, 20, 3)),
        line(seg(4, 9, 20, 9)),
        line(seg(4, 15, 20, 15)),
        line(seg(4, 21, 20, 21)),
    ]
    for yb in (9, 15, 21):
        for x in (8.5, 12, 15.5):
            parts.append(dot(x, yb - 2.6, 1.15))
    return parts


@icon("aquaponics", CAT, "Plant grow bed above a fish tank with arrows showing the water cycling between them",
      tags=["hydroponics", "fish farming", "closed loop", "sustainable farming", "grow bed", "aquaculture", "water cycle"], aliases=["aquaponic-system"])
def _(S):
    return [
        line("M9 6V3M9 4.6L7.4 3M9 4.6L10.6 3"),
        line("M15 6V3M15 4.6L13.4 3M15 4.6L16.6 3"),
        shell(rect(3, 6, 18, 4.5, rr(S, 1.2))),
        line(seg(7.5, 14.3, 7.5, 11.6)),
        mark(poly([(6, 12.9), (7.5, 11), (9, 12.9)], closed=True)),
        line(seg(16.5, 11.6, 16.5, 14.3)),
        mark(poly([(15, 13), (16.5, 14.9), (18, 13)], closed=True)),
        shell(rect(3, 15, 18, 6.5, rr(S, 1.5))),
        mark(f"M8.2 18.25C9.4 16.9 12 16.9 13.2 18.25C12 19.6 9.4 19.6 8.2 18.25Z"),
        mark(poly([(12.8, 18.25), (15.2, 16.9), (15.2, 19.6)], closed=True)),
    ]


@icon("center-pivot-irrigation", CAT, "Long pipe span on wheeled towers spraying water over a field",
      tags=["pivot irrigation", "field irrigation", "crop circle", "sprinkler system", "agriculture", "watering crops", "farm"], aliases=["pivot-irrigator"])
def _(S):
    parts = [
        line(seg(2.5, 5.5, 21.5, 5.5)),
        line(seg(5, 5.5, 2.8, 18)),
        line(seg(5, 5.5, 7.2, 18)),
        line(seg(19, 5.5, 16.8, 18)),
        line(seg(19, 5.5, 21.2, 18)),
        dot(2.8, 20.3, 1.4), dot(7.2, 20.3, 1.4), dot(16.8, 20.3, 1.4), dot(21.2, 20.3, 1.4),
        line(seg(12, 5.5, 12, 8.5)),
    ]
    for x, y in ((9, 12), (12, 13), (15, 12), (10, 16), (14, 16)):
        parts.append(dot(x, y, 1.15))
    return parts


# ============================================================================ water works

@icon("irrigation-canal", CAT, "Straight concrete irrigation channel running between two rows of crops in perspective",
      tags=["irrigation ditch", "water channel", "farm canal", "flood irrigation", "crop rows", "waterway", "agriculture"], aliases=["irrigation-ditch"])
def _(S):
    parts = [
        shell(poly([(8, 21.5), (16, 21.5), (13.3, 5), (10.7, 5)], closed=True, r=S.r * 0.5)),
        detail(wave(9.6, 14.4, 16.5, 1.0, 2.4)),
        detail(wave(10.5, 13.5, 11, 0.8, 1.5)) if False else detail(seg(10.4, 10.5, 13.6, 10.5)),
    ]
    for t, rad in ((0.92, 1.4), (0.52, 1.2), (0.16, 1.0)):
        y = 5 + 16.5 * t
        parts.append(dot(9.3 - 5.6 * t - 0.4, y, rad))
        parts.append(dot(14.7 + 5.6 * t + 0.4, y, rad))
    return parts


@icon("sluice-gate", CAT, "Metal sluice gate with a screw wheel on top, raised above a channel of flowing water",
      tags=["water gate", "floodgate", "canal gate", "irrigation", "weir", "water control", "dam"], aliases=["floodgate"])
def _(S):
    return [
        line(poly([(4.5, 21.5), (4.5, 6.5), (19.5, 6.5), (19.5, 21.5)], r=S.r * 0.5)),
        line(seg(12, 2.5, 12, 10)),
        line(seg(8.5, 2.5, 15.5, 2.5)),
        shell(rect(7.5, 10, 9, 4.5, rr(S, 1.2))),
        line(wave(6.5, 17.5, 19.5, 1.3, 3.667)),
    ]


@icon("hand-water-pump", CAT, "Cast-iron farm hand pump with a curved lever handle and a spout pouring water",
      tags=["well pump", "water pump", "old fashioned pump", "farmstead", "drawing water", "rural", "pitcher pump"], aliases=["well-pump"])
def _(S):
    return [
        line("M11 6.5C7.5 6.5 5 5 3 2.5"),
        shell(rect(7.5, 6.5, 6, 3, rr(S, 1.2))),
        shell(rect(8.5, 9.5, 4, 9, rr(S, 0.8))),
        shell(rect(5.5, 18.5, 10, 3, rr(S, 1.2))),
        line("M12.5 12.5H17.5"),
        dot(17.5, 16, 1.1), dot(17.5, 19, 1.1), dot(17.5, 21.6, 0.9),
    ]


@icon("windpump", CAT, "Farm wind pump with a many-bladed fan wheel and tail vane on a tall lattice tower",
      tags=["wind pump", "water pumping", "windmill pump", "farm windmill", "tower", "bore water", "ranch"], aliases=["farm-windpump"])
def _(S):
    parts = [
        shell(circle(10.5, 7.5, 5.8)),
        line(seg(16.3, 7.5, 18.5, 7.5)),
        shell(poly([(18.5, 5.5), (22, 5.5), (22, 9.5), (18.5, 9.5)], closed=True, r=S.r * 0.7)),
        line(seg(10.5, 13.3, 6.5, 21.5)),
        line(seg(10.5, 13.3, 14.5, 21.5)),
        line(seg(8.2, 18, 12.8, 18)),
        dot(10.5, 7.5, 1.2),
    ]
    for a in (0, 60, 120, 180, 240, 300):
        x, y = polar(10.5, 7.5, 4.3, a + 15)
        parts.append(detail(seg(*polar(10.5, 7.5, 2.4, a + 15), x, y)))
    return parts


@icon("shaduf", CAT, "Ancient shaduf: a pivoting pole on a post with a counterweight at one end and a bucket at the other over water",
      tags=["well sweep", "water lift", "ancient irrigation", "egypt", "lever", "bucket", "drawing water"], aliases=["well-sweep"])
def _(S):
    return [
        line(seg(12, 7.2, 12, 21.5)),
        line(seg(4.5, 5, 20, 9.4)),
        shell(circle(19.5, 12.5, 2.6)),
        line(seg(4.5, 5, 4.5, 12)),
        shell(poly([(2.5, 12), (6.5, 12), (6, 16), (3, 16)], closed=True, r=S.r * 0.4)),
        line(wave(2.5, 9.5, 20, 1.2, 3.5)),
    ]


@icon("water-wheel", CAT, "Large spoked water wheel with paddles turning in a stream",
      tags=["paddle wheel", "mill wheel", "river power", "hydropower", "noria", "stream", "rural"], aliases=["paddle-wheel"])
def _(S):
    parts = [shell(circle(12, 10.5, 5.4)), dot(12, 10.5, 1.2)]
    for a in range(0, 360, 45):
        cx, cy = polar(12, 10.5, 7.6, a)
        parts.append(mark(orect(cx, cy, 2.6, 2.8, 0, a + 90)))
    for a in (0, 90):
        parts.append(detail(seg(*polar(12, 10.5, 2.4, a), *polar(12, 10.5, 5.4, a))))
        parts.append(detail(seg(*polar(12, 10.5, 2.4, a + 180), *polar(12, 10.5, 5.4, a + 180))))
    parts.append(line(wave(2.5, 21.5, 21, 1.1, 4.75)))
    return parts


@icon("watermill", CAT, "Mill house with a large paddle wheel on its side and water flowing beneath",
      tags=["water mill", "grist mill", "flour mill", "mill wheel", "heritage", "river", "rural building"], aliases=["grist-mill"])
def _(S):
    parts = [
        shell(poly([(2.5, 20.5), (2.5, 10), (7.5, 5), (12.5, 10), (12.5, 20.5)], closed=True, r=S.r * 0.5)),
        detail("M5.5 20.5V15.5H9.5V20.5"),
        shell(circle(17.5, 12.5, 4.6)),
        dot(17.5, 12.5, 1.1),
        detail(seg(17.5, 8.8, 17.5, 16.2)),
        detail(seg(13.8, 12.5, 21.2, 12.5)),
        line(wave(13, 21.5, 21.3, 1.0, 4.25)),
    ]
    return parts


@icon("rain-gauge", CAT, "Clear rain gauge tube with a funnel top, measurement marks and water filled partway",
      tags=["precipitation", "weather station", "rainfall measure", "meteorology", "farm weather", "garden", "measuring"], aliases=["rainfall-gauge"])
def _(S):
    return [
        shell(poly([(4.5, 2.5), (19.5, 2.5), (14.5, 8), (9.5, 8)], closed=True, r=S.r * 0.5)),
        shell(rect(9, 8, 6, 13.5, rr(S, 2))),
        detail(seg(9, 11, 11.5, 11)),
        detail(seg(9, 13.75, 11, 13.75)),
        mark(rect(10.2, 16.5, 3.6, 4, 0)),
    ]


@icon("soil-moisture-sensor", CAT, "Two-pronged soil moisture probe pushed into the ground with a small display and a water drop",
      tags=["soil sensor", "moisture probe", "smart farming", "irrigation control", "agritech", "garden sensor", "iot"], aliases=["moisture-probe"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 7.5, rr(S, 2))),
        detail(rect(9, 5, 6, 2.5, 0)) if False else detail(seg(9, 6.25, 15, 6.25)),
        line(seg(8.5, 10, 8.5, 21.5)),
        line(seg(15.5, 10, 15.5, 21.5)),
        line(seg(2.5, 14.5, 5.5, 14.5)),
        line(seg(18.5, 14.5, 21.5, 14.5)),
        mark(poly([(12, 13.6), (13.4, 16.2), (12, 18.2), (10.6, 16.2)], closed=True)) if S.name == "line" else
        mark("M12 13.4C12.6 14.5 13.6 15.4 13.6 16.6A1.6 1.6 0 0 1 10.4 16.6C10.4 15.4 11.4 14.5 12 13.4Z"),
    ]


@icon("rice-paddy", CAT, "Flooded rice paddy with young rice shoots standing in rippled water",
      tags=["rice field", "paddy field", "rice farming", "wet rice", "asia agriculture", "terrace", "crops"], aliases=["rice-field"])
def _(S):
    parts = []
    for x in (5.5, 12, 18.5):
        parts.append(line(f"M{fmt(x)} 15V6"))
        parts.append(line(f"M{fmt(x - 2.4)} 8.4L{fmt(x)} 11.2L{fmt(x + 2.4)} 8.4"))
    parts.append(line(wave(2.5, 21.5, 18, 1.3, 4.75)))
    return parts




# ============================================================================ farm buildings and stores

@icon("silo", CAT, "Tall cylindrical tower silo with a domed top, stave bands and a small lean-to beside it",
      tags=["grain silo", "farm tower", "feed storage", "barn silo", "silage", "agriculture", "storage tower"], aliases=["tower-silo"])
def _(S):
    return [
        shell("M4.5 21.5V9A5 5 0 0 1 14.5 9V21.5Z" if S.name == "rounded" else "M4.5 21.5V9L9.5 4L14.5 9V21.5Z"),
        detail(seg(4.5, 12.5, 14.5, 12.5)),
        detail(seg(4.5, 17, 14.5, 17)),
        shell(poly([(14.5, 21.5), (14.5, 14.5), (18, 11.5), (21.5, 14.5), (21.5, 21.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("grain-bin", CAT, "Squat round corrugated grain bin with a shallow conical roof and a vent cap",
      tags=["grain storage", "corn bin", "farm bin", "crop storage", "harvest", "metal bin", "agriculture"], aliases=["grain-store"])
def _(S):
    return [
        shell(rect(2.5, 6, 3, 2.5, 0)) if False else shell(rect(10.5, 3, 3, 2.5, rr(S, 0.8))),
        shell(poly([(3.5, 11), (12, 5.2), (20.5, 11)], closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
        shell(rect(3.5, 11, 17, 10.5, rr(S, 1.2))),
        detail(seg(8, 11.5, 8, 21)),
        detail(seg(12, 11.5, 12, 21)),
        detail(seg(16, 11.5, 16, 21)),
    ]


@icon("grain-elevator", CAT, "Tall boxy grain elevator with a taller headhouse, a conveyor spout and a rail line at its base",
      tags=["grain storage", "prairie", "rail", "commodity", "harvest", "co-op", "agricultural building"], aliases=["country-elevator"])
def _(S):
    return [
        shell(rect(7, 2.5, 6, 5.5, rr(S, 1))),
        shell(rect(3.5, 8, 13, 10.5, rr(S, 1))),
        detail(seg(8, 8.5, 8, 18)),
        detail(seg(12, 8.5, 12, 18)),
        line(seg(13, 5, 21, 8.5)),
        line(seg(2.5, 21.5, 21.5, 21.5)),
    ]


@icon("feed-bin", CAT, "Hopper bin on legs with a cone-shaped bottom and a short auger pipe",
      tags=["feed hopper", "livestock feed", "grain hopper", "animal feed", "farm storage", "auger", "silo"], aliases=["feed-hopper"])
def _(S):
    return [
        shell(poly([(5.5, 3), (18.5, 3), (18.5, 10.5), (12, 17), (5.5, 10.5)], closed=True, r=S.r * 0.6)),
        detail(seg(5.5, 7, 18.5, 7)),
        line(seg(6, 12, 4.5, 21.5)),
        line(seg(18, 12, 19.5, 21.5)),
        line(seg(12, 17, 12, 20)),
        line(seg(12, 20, 16.5, 20)),
    ]


@icon("farmhouse", CAT, "Two-storey farmhouse with a gabled roof, chimney and a covered porch across the front",
      tags=["farm home", "homestead", "rural house", "country house", "ranch house", "porch", "agriculture"], aliases=["homestead-house"])
def _(S):
    return [
        shell(rect(5, 8.5, 14, 12.5, rr(S, 1))),
        line(poly([(3, 8.5), (12, 2.5), (21, 8.5)], r=S.r)),
        line(seg(17, 3.5, 17, 6.3)),
        detail(rect(10.5, 10.5, 3, 2.8, 0)),
        line(seg(3, 15.5, 21, 15.5)),
        detail("M6.5 21V17.5H9.5V21"),
        detail(rect(14, 17.5, 3, 2.3, 0)),
    ]


@icon("farmstead", CAT, "Farm scene with a barn, a tall silo and a small house side by side",
      tags=["homestead", "farm buildings", "rural", "ranch", "barn and silo", "agriculture", "countryside"], aliases=["farm-buildings"])
def _(S):
    return [
        shell(poly([(2.5, 21.5), (2.5, 13), (6, 9.5), (9.5, 13), (9.5, 21.5)], closed=True, r=S.r * 0.5)),
        detail("M4.5 21.5V16H7.5V21.5"),
        shell("M9.5 21.5V7.5A2.5 2.5 0 0 1 14.5 7.5V21.5Z"),
        detail(seg(9.5, 12, 14.5, 12)),
        shell(poly([(14.5, 21.5), (14.5, 15), (18, 11.5), (21.5, 15), (21.5, 21.5)], closed=True, r=S.r * 0.5)),
        detail(rect(16.5, 16.5, 2, 2, 0)),
    ]


@icon("corn-crib", CAT, "Narrow slatted corn crib on stilts with a peaked roof and cobs showing through the gaps",
      tags=["corn storage", "maize store", "rat proof", "grain store", "rural", "harvest", "raised store"], aliases=["maize-crib"])
def _(S):
    return [
        line(poly([(4, 9), (12, 3), (20, 9)], r=S.r)),
        shell(poly([(6, 9), (18, 9), (17, 16.5), (7, 16.5)], closed=True, r=S.r * 0.5)),
        detail(seg(9.8, 9.5, 9.3, 16)),
        detail(seg(14.2, 9.5, 14.7, 16)),
        dot(12, 11.4, 1.0), dot(12, 14.4, 1.0),
        line(seg(8, 16.5, 8, 21.5)),
        line(seg(16, 16.5, 16, 21.5)),
    ]


@icon("granary", CAT, "Small wooden grain store raised on mushroom-shaped staddle stones under a steep roof",
      tags=["grain store", "staddle stones", "raised barn", "rural building", "heritage", "storage", "harvest"], aliases=["staddle-granary"])
def _(S):
    return [
        line(poly([(3, 9), (12, 2.5), (21, 9)], r=S.r)),
        shell(rect(5, 9, 14, 7, rr(S, 1))),
        detail("M10.5 16V11.5H13.5V16"),
        line("M4 19H9.5M6.75 19V21.5"),
        line("M14.5 19H20M17.25 19V21.5"),
    ]


@icon("root-cellar", CAT, "Grassy earth mound with a wooden arched door set into its front",
      tags=["cold storage", "earth cellar", "food storage", "homestead", "vegetable storage", "underground", "preserving"], aliases=["earth-cellar"])
def _(S):
    return [
        line("M9 8.5L8 5.5M12 8V4.5M15 8.5L16 5.5"),
        shell("M2.5 21.5C2.5 14 6.5 9 12 9C17.5 9 21.5 14 21.5 21.5Z"),
        detail("M9.3 21.5V16.5A2.7 2.7 0 0 1 14.7 16.5V21.5"),
        detail(seg(12, 14, 12, 21)),
    ]


@icon("smokehouse", CAT, "Small narrow wooden smokehouse with a vented roof cupola and smoke curling from the top",
      tags=["smoking meat", "curing", "food preservation", "smoker", "bbq shed", "cured ham", "rural outbuilding"], aliases=["smoke-shed"])
def _(S):
    return [
        line("M12 5C10 3.8 13.6 3 12 1.8") if False else line("M12 5.2C10 4 13.8 3.2 12 2.2"),
        shell(rect(10, 5.5, 4, 2.6, rr(S, 0.8))),
        line(poly([(4.5, 12.5), (12, 7.5), (19.5, 12.5)], r=S.r)),
        shell(rect(6, 12.5, 12, 9, rr(S, 1))),
        detail("M9.5 21.5V16H14.5V21.5"),
    ]
