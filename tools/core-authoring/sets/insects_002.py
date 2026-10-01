"""TypeIcon Core: insects and small creatures (batch 002)."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "insects"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def flip(d):
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def lp(S, pts):
    """Open polyline stroke (legs, antennae)."""
    return line(poly(pts, r=S.r))


def mir(pts):
    return [(24 - x, y) for x, y in pts]


def sym(S, *legs):
    out = []
    for pts in legs:
        out.append(lp(S, pts))
        out.append(lp(S, mir(pts)))
    return out


def eo(cx, cy, rx, ry, deg):
    return rot(ellipse(cx, cy, rx, ry), deg, cx, cy)


def leaf(cx, top, bottom, w):
    """Vertical pointed oval from top to bottom, width w."""
    my = (top + bottom) / 2
    k = w * 0.66
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + k)} {fmt(top + (my - top) * 0.35)} {fmt(cx + k)} {fmt(bottom - (bottom - my) * 0.35)} {fmt(cx)} {fmt(bottom)}"
            f"C{fmt(cx - k)} {fmt(bottom - (bottom - my) * 0.35)} {fmt(cx - k)} {fmt(top + (my - top) * 0.35)} {fmt(cx)} {fmt(top)}Z")


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def path_pts(ctrls, n=10):
    """Points along a chain of cubic segments (each ctrl is p0, p1, p2, p3)."""
    pts = []
    for k, c in enumerate(ctrls):
        for i in range(n + 1):
            if k and i == 0:
                continue
            pts.append(bez(*c, i / n))
    return pts


def _norm(pts, i):
    a, b = pts[max(0, i - 1)], pts[min(len(pts) - 1, i + 1)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(dx, dy) or 1
    return -dy / ln, dx / ln


def tube_poly(pts, width):
    """Closed outline around a centre line; width is a function of t in 0..1 (diameter in px)."""
    left, right = [], []
    for i, (x, y) in enumerate(pts):
        nx, ny = _norm(pts, i)
        w = width(i / (len(pts) - 1)) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return left + right[::-1]


def ticks_across(pts, ts, half):
    """Short strokes across a tube at the given parameters (ring marks)."""
    out = []
    for t in ts:
        i = round(t * (len(pts) - 1))
        x, y = pts[i]
        nx, ny = _norm(pts, i)
        out.append(detail(seg(x - nx * half, y - ny * half, x + nx * half, y + ny * half)))
    return out


def mark(d):
    """Small solid mark (spot, hourglass). Solid in stroke styles, knocked out of a Filled body."""
    return Part("dot", d)


def rp(pts, deg, cx=12, cy=12):
    """Rotate a list of points about (cx, cy)."""
    c, sn = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [(cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c) for x, y in pts]


def bug(S, body, legs=(), ants=()):
    """Shell body plus symmetrical legs and antennae."""
    return [shell(body), *sym(S, *legs), *sym(S, *ants)]


# --------------------------------------------------------------------------- orthoptera and mantises

@icon("caddisfly-case", CAT, "Larva case made of tiny pebbles with the head and legs poking out one end",
      tags=["caddisfly", "larva", "pebbles", "stream", "aquatic insect", "case"])
def _(S):
    case = union(circle(5.3, 13.5, 3.2), circle(9.3, 10.5, 3.2), circle(9.8, 15.5, 3), circle(13.3, 12.6, 3.2))
    head = circle(18, 12.6, 2.4)
    return [shell(union(case, head)), dot(9.5, 10.6, 0.8), dot(9.9, 15.7, 0.8), dot(17.8, 12, 0.7),
            lp(S, [(17, 15), (15.8, 19.5)]), lp(S, [(19.8, 15), (21, 19.5)])]


@icon("grasshopper", CAT, "Grasshopper in side view with a big bent jumping leg",
      tags=["locust", "hopper", "insect", "jump", "meadow", "bug"])
def _(S):
    body = union(circle(5.5, 11, 2.7), eo(12, 11.8, 7.5, 3, 3),
                 poly([(17, 9.8), (20.8, 13), (17, 14)], closed=True, r=S.r))
    return [shell(body), lp(S, [(5, 8.6), (3, 4)]),
            lp(S, [(13.5, 13.5), (18.5, 6), (21.5, 19.5)]),
            lp(S, [(8.5, 14), (7, 19.5)]), lp(S, [(11, 14.6), (10.5, 20)]), dot(5.4, 10.4, 0.8)]


@icon("cricket-insect", CAT, "Round-bodied cricket with long antennae, hind legs and tail spikes",
      tags=["chirp", "insect", "field cricket", "bug", "night", "antennae"])
def _(S):
    body = union(circle(5.5, 13, 2.6), eo(12.5, 13.8, 6.5, 4.3, 0))
    return [shell(body), line("M5 10.6C3.5 6 7.5 3 13.5 3.5"),
            lp(S, [(9, 17.5), (8, 21)]), lp(S, [(12.5, 18.3), (12.5, 21)]), lp(S, [(16, 17.3), (19.5, 21)]),
            lp(S, [(18.5, 12.5), (22, 10.5)]), lp(S, [(18.5, 14.8), (22, 15.5)]), dot(5.3, 12.6, 0.8)]


@icon("mole-cricket", CAT, "Velvety cricket with broad shovel-like front legs for digging",
      tags=["digging insect", "burrowing", "cricket", "garden pest", "soil", "bug"])
def _(S):
    r = S.r
    body = union(ellipse(12, 9, 3.4, 4), ellipse(12, 16.5, 3.2, 4.8))
    c1 = poly([(8.6, 9), (5.5, 10.5), (3, 7), (4.5, 3.5), (7, 5.5), (8.6, 6.5)], closed=True, r=r)
    c2 = poly([(15.4, 9), (18.5, 10.5), (21, 7), (19.5, 3.5), (17, 5.5), (15.4, 6.5)], closed=True, r=r)
    return [shell(union(body, c1, c2)), detail(seg(12, 13.5, 12, 20)), *sym(S, [(9, 16.5), (5.5, 18), (4.5, 21)], [(9.5, 19.3), (8, 22)])]


@icon("praying-mantis", CAT, "Mantis standing upright with folded spiked front legs held up",
      tags=["mantis", "insect", "predator", "garden", "bug", "green"])
def _(S):
    head = poly([(2.5, 3), (8.5, 3), (5.5, 7.5)], closed=True, r=L(S, 0, 0.6))
    abd = eo(16.5, 14.5, 5.5, 2.2, 28)
    return [shell(head), shell(abd), line(poly([(6.5, 8), (13, 12)], r=0)),
            lp(S, [(7.5, 8.5), (11.5, 7), (11.5, 3)]),
            lp(S, [(13, 13), (12, 18), (10.5, 21.5)]), lp(S, [(16, 15), (16.5, 19), (15.5, 21.5)])]


@icon("orchid-mantis", CAT, "Mantis with wide petal-shaped lobes on its legs so it looks like a flower",
      tags=["flower mantis", "insect", "camouflage", "petal", "mimic", "bug"])
def _(S):
    head = poly([(2.5, 3), (8.5, 3), (5.5, 7.5)], closed=True, r=L(S, 0, 0.6))
    petals = union(eo(14, 9, 2, 4, 50), eo(12.5, 18, 2.2, 4.4, -25), eo(18, 16, 2.2, 4.4, 40), eo(19.5, 10, 1.8, 3.6, 75))
    return [shell(head), shell(petals), line(poly([(6.5, 8), (12, 11)], r=0)),
            lp(S, [(7.5, 8.5), (10.5, 7), (10.5, 3.5)])]


@icon("stick-insect", CAT, "Twig-thin insect with long jointed legs and thin antennae",
      tags=["walking stick", "phasmid", "camouflage", "twig", "insect", "bug"])
def _(S):
    def T(pts):
        return rp(pts, -32)
    legs = [[(9, 12), (6.5, 7), (3, 6)], [(9, 12), (6.5, 17), (3, 18)], [(13, 12), (12.5, 6), (9, 3.5)],
            [(13, 12), (12.5, 18), (9, 20.5)], [(18, 11.5), (22, 8)], [(18, 12.5), (22, 16)]]
    return [line(poly(T([(5, 12), (19, 12)]))), dot(*T([(20, 12)])[0], 1.4), *[lp(S, T(p)) for p in legs]]


@icon("leaf-insect", CAT, "Flat leaf-shaped insect with a midrib vein, small head and leafy legs",
      tags=["walking leaf", "phylliidae", "camouflage", "insect", "mimic", "bug"])
def _(S):
    body = union(leaf(12, 7, 22, 9), circle(12, 4.6, 1.9))
    return [shell(body), detail(seg(12, 9, 12, 19.5)), detail(seg(12, 13, 8.8, 10.5)), detail(seg(12, 13, 15.2, 10.5)),
            detail(seg(12, 17, 8.8, 14.5)), detail(seg(12, 17, 15.2, 14.5)),
            *sym(S, [(8, 10), (4, 9)], [(7.6, 15), (4, 16.5)])]


@icon("cicada", CAT, "Cicada from above with wide-set eyes and clear veined wings held like a tent",
      tags=["cicadas", "insect", "summer", "buzz", "wings", "bug"])
def _(S):
    head = rect(6.5, 2.5, 11, 4.5, L(S, 1.5, 2.2))
    body = eo(12, 11.5, 2.8, 6, 0)
    w1 = eo(7.4, 14.5, 2.8, 7, 18)
    w2 = eo(16.6, 14.5, 2.8, 7, -18)
    return [shell(union(head, body, w1, w2)), detail(seg(12, 9, 12, 16)), detail(poly([(7, 11), (6.5, 19)], r=0)),
            detail(poly([(17, 11), (17.5, 19)], r=0))]


@icon("cicada-shell", CAT, "Empty split cicada skin clinging to a twig with a crack down its back",
      tags=["exuvia", "molt", "cicada", "shed skin", "insect", "twig"])
def _(S):
    body = union(eo(13.5, 10.5, 7.5, 4.6, -6), circle(5.3, 11.5, 2.4))
    return [shell(body), detail("M9.5 8.3Q13.5 6.6 18 8.6"), line(seg(2, 21, 22, 18)),
            lp(S, [(9, 14.5), (6.5, 19.5)]), lp(S, [(13, 14.8), (11.5, 19)]), lp(S, [(17, 14.3), (17, 18.3)]), dot(5, 11, 0.7)]


@icon("stink-bug", CAT, "Shield-shaped bug from above with a triangular plate on its back",
      tags=["shield bug", "insect", "pest", "smelly", "garden", "bug"])
def _(S):
    shield = poly([(12, 6), (19, 8.5), (18.5, 16), (12, 21), (5.5, 16), (5, 8.5)], closed=True, r=L(S, 0, 2))
    return [shell(union(shield, circle(12, 4.6, 2))), detail(poly([(12, 10), (15.8, 16), (8.2, 16)], closed=True, r=0)),
            *sym(S, [(11, 3), (9, 1.5)]), *sym(S, [(5.4, 10.5), (2.5, 11.5)], [(5.6, 15), (2.5, 17)])]


@icon("aphid", CAT, "Tiny pear-shaped bug in side view with long legs, antennae and two tail tubes",
      tags=["plant louse", "greenfly", "insect", "garden pest", "blackfly", "bug"])
def _(S):
    body = union(circle(5.5, 11.5, 2.6), eo(13, 13, 6.8, 4.8, 0))
    return [shell(body), lp(S, [(4.5, 9.3), (2.5, 5.5)]), lp(S, [(6.5, 9.3), (8.5, 5.5)]),
            lp(S, [(18, 9.5), (19, 5.5)]), lp(S, [(20.5, 11), (22, 8)]),
            lp(S, [(8, 17), (6.5, 21)]), lp(S, [(12, 17.8), (12, 21)]), lp(S, [(17, 17.2), (18.5, 21)]), dot(5, 11, 0.7)]


@icon("bedbug", CAT, "Flat round oval bug from above with a banded abdomen and short legs",
      tags=["bed bug", "insect", "hotel", "infestation", "pest", "bite"])
def _(S):
    body = union(ellipse(12, 13.5, 6, 7), circle(12, 5.2, 2))
    return [shell(body), detail(seg(6.3, 13, 17.7, 13)), detail(seg(7.3, 17, 16.7, 17)),
            *sym(S, [(6.3, 9.5), (3, 8.5)], [(6, 13), (2.5, 14)], [(7, 18), (4, 20.5)])]

# --------------------------------------------------------------------------- bugs and lice

@icon("water-strider", CAT, "Thin bug skating on water on long splayed legs",
      tags=["pond skater", "water bug", "insect", "surface tension", "pond", "bug"])
def _(S):
    return [line(seg(12, 5, 12, 13)), dot(12, 4.2, 1.6),
            *sym(S, [(12, 6.5), (7.5, 4), (4, 6.5)], [(12, 9), (6, 9.5), (3, 13.5)], [(12, 12), (8, 14), (6, 17)]),
            line("M2 20.5q2.5-2 5 0t5 0t5 0t5 0")]


@icon("spotted-lanternfly", CAT, "Planthopper from above with folded spotted wings and a banded tip",
      tags=["lanternfly", "planthopper", "invasive", "insect", "pest", "spots"])
def _(S):
    wings = leaf(12, 7, 22, 10.5)
    return [shell(union(wings, circle(12, 4.6, 2))), dot(9.6, 10.6, 1), dot(14.4, 10.6, 1), dot(9.6, 14.4, 1), dot(14.4, 14.4, 1),
            dot(12, 18, 1), *sym(S, [(11, 3), (9, 1.5)])]


@icon("thorn-bug", CAT, "Small bug with a tall pointed thorn-shaped hump, clinging to a twig",
      tags=["treehopper", "thorn treehopper", "insect", "camouflage", "spike", "bug"])
def _(S):
    thorn = poly([(7.5, 13.5), (9, 8), (13, 5.5), (18.5, 4), (15.5, 9), (15, 14)], closed=True, r=L(S, 0, 0.8))
    body = union(eo(11.5, 14.8, 7, 3.4, 0), circle(4.6, 15.2, 2.1), thorn)
    return [shell(body), line(seg(2, 21.5, 22, 19.5)), lp(S, [(8.5, 17.8), (8, 20.8)]), lp(S, [(12, 18), (12, 20.6)]),
            lp(S, [(15.5, 17.6), (16.5, 20.2)]), lp(S, [(4, 13.2), (2.5, 10)]), dot(4.2, 14.8, 0.6)]


@icon("cockroach", CAT, "Flat oval cockroach with a shield head plate, long antennae and spiny legs",
      tags=["roach", "insect", "pest", "kitchen", "infestation", "bug"])
def _(S):
    body = union(eo(12, 15, 5, 6.5, 0), ellipse(12, 8, 3.4, 2.5))
    return [shell(body), detail(seg(12, 12, 12, 20.5)),
            line("M11 6C10 3 7.5 2.5 4.5 3.5"), line("M13 6C14 3 16.5 2.5 19.5 3.5"),
            *sym(S, [(7.4, 11), (3.5, 9.5), (2.5, 6.5)], [(7, 14.5), (2.5, 15)], [(7.6, 18.5), (4, 21)])]


@icon("earwig", CAT, "Long flat insect from above with a pair of curved pincers on its tail",
      tags=["pincers", "forceps", "insect", "garden", "bug", "creepy crawly"])
def _(S):
    body = union(eo(12, 11, 3, 6.8, 0), circle(12, 4.3, 2))
    return [shell(body), detail(seg(9.5, 11, 14.5, 11)),
            line("M10.6 17.5C7 18 6.5 21.5 9.8 22"), line("M13.4 17.5C17 18 17.5 21.5 14.2 22"),
            *sym(S, [(11, 2.5), (9.5, 1)]), *sym(S, [(9, 8), (5.5, 7)], [(9, 12), (5.5, 13)], [(9.5, 15.5), (6.5, 17.5)])]


@icon("silverfish", CAT, "Tapered carrot-shaped wingless insect with long antennae and three tail bristles",
      tags=["firebrat", "bristletail", "insect", "pest", "books", "bug"])
def _(S):
    body = poly([(9, 5), (15, 5), (13.8, 12), (12.6, 18), (11.4, 18), (10.2, 12)], closed=True, r=L(S, 0, 1))
    return [shell(body), detail(seg(9.8, 9, 14.2, 9)), detail(seg(10.3, 13, 13.7, 13)),
            lp(S, [(12, 18), (12, 22.5)]), lp(S, [(11.6, 18), (9, 22)]), lp(S, [(12.4, 18), (15, 22)]),
            *sym(S, [(10.3, 4.5), (8.5, 1.5)]), *sym(S, [(9.6, 8), (6, 7)], [(10, 12), (6, 12.5)], [(10.8, 15.5), (8, 18)])]


@icon("flea", CAT, "Flea in mid-jump with a big bent hind leg",
      tags=["jumping insect", "parasite", "pet", "bite", "insect", "bug"])
def _(S):
    body = union(eo(12.5, 11.5, 6.2, 3.9, -35), circle(18.2, 6.6, 2.2))
    return [shell(body), lp(S, [(8.5, 16), (3, 13), (2.5, 20.5)]), lp(S, [(12.5, 16.5), (14.5, 21)]), lp(S, [(16.5, 14), (20.5, 16.5)]),
            lp(S, [(19.5, 5), (21.5, 2.5)]), dot(18.6, 6.4, 0.6)]


@icon("head-louse", CAT, "Flat louse from above with a small head, segmented oval body and hooked claws",
      tags=["lice", "nits", "parasite", "scalp", "hair", "insect"])
def _(S):
    body = union(ellipse(12, 10, 3.4, 2.6), ellipse(12, 16.8, 4.8, 4.2), circle(12, 5.3, 2))
    return [shell(body), detail(seg(8.2, 16, 15.8, 16)), detail(seg(9, 19.2, 15, 19.2)),
            *sym(S, [(9.1, 9.3), (5, 8), (3, 10.5)], [(8.8, 10.8), (4, 12.5), (3, 15.5)], [(9.6, 12.2), (5.5, 15.5), (5, 19)])]


@icon("antlion", CAT, "Cone-shaped sand pit with an antlion larva's sickle jaws poking up at the bottom",
      tags=["doodlebug", "sand trap", "larva", "pit", "insect", "predator"])
def _(S):
    return [line(seg(2, 5.5, 22, 5.5)), line(poly([(4, 5.5), (12, 18.5), (20, 5.5)], r=S.r)),
            line("M11 19C8.5 16 10 13.5 12.2 13"), line("M13 19C15.5 16 14 13.5 11.8 13"), dot(2.5, 9, 0.8), dot(21.5, 9.5, 0.8)]


# --------------------------------------------------------------------------- arachnids

SPIDER_LEGS = ([(10, 10), (6.5, 7), (5.8, 3)], [(9.5, 11.5), (5, 10.3), (3, 7.3)],
               [(9.5, 13), (5, 14.2), (3, 17.2)], [(10, 14.5), (6.5, 17.5), (5.8, 21)])


def star_poly(cx, cy, rx, ry, n, tip, notch):
    """Closed outline with n spikes around an ellipse (tip/notch are radius scales)."""
    pts = []
    for i in range(2 * n):
        a = math.radians(-90 + i * 180 / n)
        k = tip if i % 2 == 0 else notch
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    return pts


@icon("scorpion", CAT, "Scorpion in side view with big pincers and a tail curling up to a stinger",
      tags=["arachnid", "sting", "desert", "venom", "pincers", "tail"])
def _(S):
    claw = eo(3.4, 9, 2.4, 3.8, -12)
    return [shell(union(eo(11, 16.2, 5.2, 2.8, 0), claw, eo(5.2, 13.3, 1.2, 2.2, 30))),
            detail(seg(3, 5.5, 3.6, 9)), line("M15.5 15.8C21.5 15.5 22 8.5 17.5 5.5"), line("M17.5 5.5L14.6 6.3"),
            lp(S, [(8.5, 18.6), (7.5, 21.5)]), lp(S, [(11.5, 18.9), (11.5, 21.5)]), lp(S, [(14.5, 18.4), (16, 21.5)])]


@icon("tarantula", CAT, "Large hairy spider from above with thick furry legs and a bristly round abdomen",
      tags=["spider", "hairy", "arachnid", "bird eater", "creepy", "halloween"])
def _(S):
    abd = poly(star_poly(12, 15, 5.4, 5.4, 8, 1.0, 0.8), closed=True, r=L(S, 0, 0.6))
    return [shell(union(abd, circle(12, 8, 3.2))), *sym(S, *SPIDER_LEGS)]


@icon("black-widow", CAT, "Spider with a glossy round abdomen marked with a red hourglass and thin legs",
      tags=["widow", "venomous", "arachnid", "hourglass", "spider", "danger"])
def _(S):
    hour = poly([(9.6, 11.8), (14.4, 11.8), (12, 15.3), (14.4, 18.8), (9.6, 18.8), (12, 15.3)], closed=True, r=0)
    return [shell(union(circle(12, 15.2, 5.6), circle(12, 7.6, 2.4))), mark(hour), *sym(S, *SPIDER_LEGS)]


@icon("jumping-spider", CAT, "Fuzzy spider face seen from the front with two huge eyes and small eyes beside them",
      tags=["salticid", "spider", "eyes", "arachnid", "face", "cute"])
def _(S):
    return [shell(ellipse(12, 12.5, 7, 6.5)), dot(8.8, 13, 2.5), dot(15.2, 13, 2.5), dot(10.3, 8.6, 0.9), dot(13.7, 8.6, 0.9),
            dot(7.2, 9.5, 0.9), dot(16.8, 9.5, 0.9),
            lp(S, [(10.3, 18.7), (9.8, 22)]), lp(S, [(13.7, 18.7), (14.2, 22)]),
            *sym(S, [(5.8, 9.5), (3, 5), (1.5, 2.5)], [(5, 14.5), (2.5, 19), (1.8, 21.5)])]


@icon("harvestman", CAT, "Tiny round body held up on eight extremely long thin bent legs, daddy longlegs",
      tags=["daddy longlegs", "opiliones", "arachnid", "long legs", "spider-like", "creepy"])
def _(S):
    return [dot(12, 12, 2.4), *sym(S, [(10.5, 11), (6, 4.5), (2.5, 8.5)], [(10, 11.5), (4.5, 9), (2.5, 14)],
                                   [(10, 12.5), (4.5, 15.5), (3.5, 21)], [(10.8, 13.4), (7, 18), (7.5, 22)])]


@icon("wolf-spider", CAT, "Spider from above carrying many tiny spiderlings on its back",
      tags=["spiderlings", "mother spider", "arachnid", "baby spiders", "brood", "spider"])
def _(S):
    return [shell(union(circle(12, 15, 5.8), circle(12, 7.6, 2.4))), dot(10, 12.6, 1), dot(14, 12.6, 1), dot(12, 15.2, 1),
            dot(9.2, 17.6, 1), dot(14.8, 17.6, 1), *sym(S, *SPIDER_LEGS)]


@icon("crab-spider", CAT, "Flat crab-like spider from above with long front legs held sideways and open",
      tags=["flower spider", "ambush", "arachnid", "sideways", "spider", "camouflage"])
def _(S):
    return [shell(union(ellipse(12, 13, 4.6, 5.4), circle(12, 6.8, 2.3))),
            *sym(S, [(8, 9), (4.5, 5), (1.8, 4.5)], [(7.6, 11.5), (3, 10), (1.5, 6.5)],
                 [(7.6, 14.5), (3.5, 16), (2.5, 20)], [(9, 17), (6.5, 20), (6.5, 22.5)])]


@icon("peacock-spider", CAT, "Tiny spider from the front raising a patterned fan above its body with two legs up",
      tags=["peacock jumping spider", "display", "courtship", "arachnid", "colorful", "dance"])
def _(S):
    fan = "M5 12A7 7 0 0 1 19 12Z"
    return [shell(fan), detail(seg(12, 12, 12, 5.5)), detail(seg(12, 12, 7.4, 7.4)), detail(seg(12, 12, 16.6, 7.4)),
            shell(circle(12, 17, 3)), *sym(S, [(9.4, 16, ), (5, 14), (3, 10)], [(9.2, 18.5), (5, 20)]),
            dot(10.9, 16.6, 0.7), dot(13.1, 16.6, 0.7)]


@icon("trapdoor-spider", CAT, "Soil cross section with a silk-lined burrow and a hinged round lid lifted open by a spider",
      tags=["burrow", "spider", "hinged lid", "underground", "arachnid", "ambush"])
def _(S):
    lid = poly([(16.5, 4), (20.5, 1.5), (22, 3), (17.5, 5.5)], closed=True, r=L(S, 0, 0.5))
    return [line("M2 5.5H8"), line("M8 5.5V17a4 4 0 0 0 8 0V5.5"), line("M16 5.5H18"), shell(lid),
            dot(12, 14, 2.3), dot(4.3, 12, 0.8), dot(19.7, 13, 0.8), dot(5, 19, 0.8), dot(19.2, 19.5, 0.8)]


@icon("spiny-orb-weaver", CAT, "Spider from above with a hard flat abdomen edged with six sharp spikes",
      tags=["crab spider", "spiny spider", "arachnid", "spikes", "garden", "spider"])
def _(S):
    abd = poly([(12 + 4.8 * k * math.cos(math.radians(a)), 15.5 + 4.2 * k * math.sin(math.radians(a)))
                for a, k in [(0, 1.45), (30, 0.85), (60, 1.45), (90, 0.85), (120, 1.45), (150, 0.85), (180, 1.45), (210, 0.85),
                             (240, 1.45), (270, 0.85), (300, 1.45), (330, 0.85)]], closed=True, r=L(S, 0, 0.5))
    return [shell(union(abd, circle(12, 7.3, 2.1))), dot(12, 15.5, 1.1),
            *sym(S, [(10.4, 6.8), (6.5, 4.2), (3, 4.8)], [(10.2, 8), (5, 8.5), (2.5, 11)])]


@icon("net-casting-spider", CAT, "Long-legged spider holding a small square silk net stretched between its front legs",
      tags=["ogre-faced spider", "net", "silk", "arachnid", "hunting", "spider"])
def _(S):
    net = rect(6.5, 11.5, 11, 9, L(S, 0.5, 1.5))
    return [shell(circle(12, 5.6, 2.6)), shell(net),
            detail(seg(8, 13, 16, 19)), detail(seg(16, 13, 8, 19)),
            lp(S, [(10.8, 7.8), (7.5, 11.5)]), lp(S, [(13.2, 7.8), (16.5, 11.5)]),
            *sym(S, [(10, 5), (6, 3), (3, 5.5)], [(9.5, 6.5), (4.5, 8.5), (2.5, 12.5)])]


@icon("bolas-spider", CAT, "Spider hanging from a line and swinging a single silk thread with a sticky ball at its end",
      tags=["bola spider", "sticky ball", "silk", "hunting", "arachnid", "spider"])
def _(S):
    return [line(seg(8, 1, 8, 4.3)), shell(union(circle(8, 6.3, 2.1), circle(8, 11.5, 3.4))),
            *[lp(S, p) for p in ([(6.3, 6), (3, 4)], [(5, 11), (2.5, 14)], [(6, 13.8), (4.5, 17.5)], [(11, 12.5), (13, 15)])],
            line("M9.8 6.8C15 4.5 20.5 8.5 19 14"), shell(circle(19, 17.2, 2.6))]


@icon("diving-bell-spider", CAT, "Spider underwater inside a round air bubble anchored to plant stems by silk",
      tags=["water spider", "underwater", "air bubble", "arachnid", "pond", "spider"])
def _(S):
    return [shell(circle(12, 10, 7)), dot(12, 9.6, 2), lp(S, [(10, 10.6), (8.5, 12.4)]), lp(S, [(14, 10.6), (15.5, 12.4)]),
            line("M9.5 17C8 19 10 20.5 8 22.5"), line("M14.5 17C16 19 14 20.5 16 22.5"), dot(3.5, 4.5, 0.9), dot(21, 4, 0.9)]

@icon("whip-spider", CAT, "Flat spider-like creature with spiny grasping arms and two extremely long whip legs",
      tags=["tailless whip scorpion", "amblypygid", "arachnid", "cave", "whip legs", "creepy"])
def _(S):
    return [shell(union(ellipse(12, 14.5, 4, 4.5), ellipse(12, 9.6, 3, 2.4))),
            line("M10.4 8.4C6 6.6 2.8 8 2.3 3"), line("M13.6 8.4C18 6.6 21.2 8 21.7 3"),
            lp(S, [(10.2, 10.8), (6.5, 11.5), (6, 8.5)]), lp(S, [(13.8, 10.8), (17.5, 11.5), (18, 8.5)]),
            *sym(S, [(8.2, 14), (4.2, 15), (3, 18.5)], [(9, 17.5), (6, 20), (6.5, 22.5)])]


@icon("whip-scorpion", CAT, "Scorpion-like creature with thick pincers and a long thin whip tail instead of a stinger",
      tags=["vinegaroon", "uropygid", "arachnid", "whip tail", "pincers", "creepy"])
def _(S):
    claw1, claw2 = eo(5.3, 4.8, 1.9, 3.3, -25), eo(18.7, 4.8, 1.9, 3.3, 25)
    return [shell(union(ellipse(12, 12.3, 3.8, 5.2), claw1, claw2)), line("M12 17.5C12 20 14 21 13.4 23"),
            lp(S, [(9.3, 9.5), (6.5, 8)]), lp(S, [(14.7, 9.5), (17.5, 8)]),
            *sym(S, [(8.4, 11.8), (4.5, 13.5), (4, 16.5)], [(8.6, 14.5), (5, 18), (5, 21)])]


@icon("pseudoscorpion", CAT, "Small oval arachnid with two long pincer arms and no tail",
      tags=["book scorpion", "arachnid", "pincers", "tiny", "tailless", "creepy"])
def _(S):
    return [shell(ellipse(12, 15.5, 3.8, 5.3)), lp(S, [(10.4, 12), (5, 9.5), (4, 5)]), lp(S, [(13.6, 12), (19, 9.5), (20, 5)]),
            shell(eo(4.3, 3.6, 1.5, 2.6, -12)), shell(eo(19.7, 3.6, 1.5, 2.6, 12)),
            *sym(S, [(8.4, 15), (4.5, 16), (3.5, 19)], [(9, 18.3), (6.5, 21), (7, 23)])]


@icon("camel-spider", CAT, "Hairy arachnid in side view with huge forward pointing jaws and long feelers",
      tags=["sun spider", "solifugae", "wind scorpion", "arachnid", "jaws", "desert"])
def _(S):
    r = L(S, 0, 0.5)
    jaw1 = poly([(6.5, 10), (1.6, 10.5), (6.5, 12.3)], closed=True, r=r)
    jaw2 = poly([(6.5, 13), (1.6, 14.6), (6.5, 14.8)], closed=True, r=r)
    body = union(circle(8, 12.5, 3.2), eo(15, 12.5, 6.2, 3.8, 0))
    return [shell(union(body, jaw1, jaw2)), lp(S, [(12, 8.8), (11.5, 6)]), lp(S, [(16, 8.9), (16.5, 6)]),
            lp(S, [(10, 16), (7.5, 19), (6, 22)]), lp(S, [(14, 16.2), (13.5, 22)]), lp(S, [(18, 15.8), (20.5, 18.5), (21.5, 22)])]


@icon("tick-arachnid", CAT, "Round flat tick from above with a small head, shield plate and eight short legs",
      tags=["tick", "parasite", "lyme", "bite", "arachnid", "blood sucker"])
def _(S):
    return [shell(union(circle(12, 13.5, 6), ellipse(12, 5.5, 2.2, 1.8))), detail("M8.4 11Q12 8.8 15.6 11"),
            *sym(S, [(6.7, 10.5), (3.3, 8.5)], [(6.1, 13.5), (2.3, 13.5)], [(6.4, 16.5), (3, 18.5)], [(8.6, 18.6), (6, 22)])]


@icon("mite", CAT, "Tiny round mite from above with eight short legs, like a dust mite",
      tags=["dust mite", "spider mite", "arachnid", "allergy", "microscopic", "bug"])
def _(S):
    return [shell(union(circle(12, 12.5, 5.2), circle(12, 5.6, 1.8))), dot(10.2, 12, 0.9), dot(13.8, 12, 0.9), dot(12, 15.5, 0.9),
            *sym(S, [(7.4, 9), (3.5, 6.5)], [(7, 11.8), (2.3, 11)], [(7, 14.4), (2.4, 16)], [(8.6, 17), (5.4, 21)])]


@icon("cobweb", CAT, "Triangular web in a corner with radiating threads joined by sagging arcs and a dangling strand",
      tags=["spider web", "spiderweb", "halloween", "cobwebs", "dusty", "abandoned"])
def _(S):
    o = (2.5, 2.5)
    def pa(r, deg):
        return pt_on(o[0], o[1], r, deg)
    rad = [line(seg(*o, *pa(19, a))) for a in (0, 30, 60, 90)]
    arcs = []
    for r in (7, 13):
        for a1, a2 in ((0, 30), (30, 60), (60, 90)):
            c = pt_on(o[0], o[1], r * 0.82, (a1 + a2) / 2)
            p1, p2 = pa(r, a1), pa(r, a2)
            arcs.append(line(f"M{fmt(p1[0])} {fmt(p1[1])}Q{fmt(c[0])} {fmt(c[1])} {fmt(p2[0])} {fmt(p2[1])}"))
    return [*rad, *arcs]


@icon("hanging-spider", CAT, "Spider dangling upside down at the end of a single vertical silk thread",
      tags=["dangling spider", "silk", "halloween", "drop", "arachnid", "spider"])
def _(S):
    return [line(seg(12, 1, 12, 7.5)), shell(union(circle(12, 11, 3.4), circle(12, 16.5, 2.1))),
            *sym(S, [(10.4, 15.6), (6, 11.5), (4, 7.5)], [(10, 16.8), (4.5, 15.5), (2.5, 11.5)],
                 [(10, 17.8), (4.5, 19.5), (3.5, 22.5)], [(10.6, 18.4), (8, 22.5)])]


@icon("spider-egg-sac", CAT, "Round fluffy silk egg ball held under a spider",
      tags=["egg case", "eggs", "spiderlings", "silk ball", "arachnid", "nest"])
def _(S):
    ball = union(circle(12, 15.5, 3.8), *[circle(12 + 4.2 * math.cos(math.radians(a)), 15.5 + 4.2 * math.sin(math.radians(a)), 1.9) for a in range(0, 360, 45)])
    return [shell(ball), shell(circle(12, 5.6, 2.6)), lp(S, [(12, 8.2), (12, 9.8)]),
            *sym(S, [(10.2, 4.6), (6.5, 2.5), (3.5, 3.5)], [(9.8, 6.4), (5.5, 7.5), (3, 10.5)])]


# --------------------------------------------------------------------------- many-legged and crustaceans

@icon("centipede", CAT, "Long flat segmented centipede with one pair of legs on each segment and long antennae",
      tags=["many legs", "myriapod", "creepy crawly", "bug", "venomous", "hundred legs"])
def _(S):
    legs = []
    for x in (4.5, 8.5, 12.5, 16.5):
        legs += [lp(S, [(x, 10), (x - 1.5, 5.5)]), lp(S, [(x, 14), (x - 1.5, 18.5)])]
    return [shell(rect(2.5, 10, 17, 4, L(S, 1, 2))), *legs, lp(S, [(19.5, 11), (22, 8)]), lp(S, [(19.5, 13), (22, 16)])]


@icon("millipede", CAT, "Tube-shaped millipede curled into a loose spiral with many tiny legs along its edge",
      tags=["thousand legs", "myriapod", "curled", "spiral", "creepy crawly", "bug"])
def _(S):
    cx, cy = 12, 12.5
    pts = []
    n = 60
    for i in range(n + 1):
        t = i / n
        a = math.radians(200 + t * 470)
        r = 2.4 + 6.2 * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    body = path_to_d(ST(poly(pts), 3, "round", "round"))
    ticks = []
    for i in range(10, n + 1, 4):
        t = i / n
        a = math.radians(200 + t * 470)
        r = 2.4 + 6.2 * t
        ticks.append(lp(S, [(cx + (r + 1.8) * math.cos(a), cy + (r + 1.8) * math.sin(a)), (cx + (r + 3.4) * math.cos(a), cy + (r + 3.4) * math.sin(a))]))
    e = pts[-1]
    return [shell(union(body, circle(e[0], e[1], 2.3))), *ticks]


@icon("pill-bug", CAT, "Pill bug rolled into a tight ball showing overlapping armor bands",
      tags=["roly poly", "woodlouse", "armadillidium", "curled", "armor", "bug"])
def _(S):
    ball = poly(regular(12, 12, 9, 12, -75), closed=True, r=L(S, 0, 2.2))
    return [shell(ball), detail("M5 8.4Q12 12.2 19 8.4"), detail("M3.6 12.6Q12 16.6 20.4 12.6"), detail("M5.4 16.6Q12 19.4 18.6 16.6")]


@icon("woodlouse", CAT, "Flat oval woodlouse from above with overlapping plates, short antennae and two tail spikes",
      tags=["sowbug", "slater", "crustacean", "garden", "damp", "bug"])
def _(S):
    return [shell(ellipse(12, 12.2, 5.6, 7.3)), detail("M6.6 9Q12 11 17.4 9"), detail("M6.4 13Q12 15 17.6 13"),
            lp(S, [(10.8, 19), (9.6, 22.5)]), lp(S, [(13.2, 19), (14.4, 22.5)]),
            *sym(S, [(10.6, 5.6), (9, 2.5)]), *sym(S, [(6.6, 9), (3.8, 8)], [(6.3, 12.5), (3.2, 12.8)], [(6.8, 16), (4, 17.5)])]


@icon("daphnia", CAT, "Translucent water flea in side view with a round shell, one eye and branched swimming antennae",
      tags=["water flea", "plankton", "crustacean", "pond", "microscopic", "aquatic"])
def _(S):
    return [shell(union(circle(12.5, 13.5, 6.3), ellipse(6, 11.2, 2.8, 2.4))), dot(5.3, 10.8, 0.8),
            lp(S, [(7.4, 9), (8.5, 4.5)]), lp(S, [(8.5, 4.5), (5.5, 2.5)]), lp(S, [(8.5, 4.5), (11.5, 2.8)]),
            dot(12.5, 12.8, 1.1), dot(14.6, 15.8, 1), lp(S, [(18, 16.5), (21.5, 20.5)])]


@icon("copepod", CAT, "Tiny teardrop-shaped crustacean from above with a single eye and two long antennae held sideways",
      tags=["plankton", "crustacean", "cyclops", "zooplankton", "microscopic", "aquatic"])
def _(S):
    body = "M12 3.5C16.5 3.5 17 10 14.2 14L12.2 20H11.8L9.8 14C7 10 7.5 3.5 12 3.5Z"
    return [shell(body), dot(12, 8, 1.3), lp(S, [(8.4, 7), (2.2, 8.2)]), lp(S, [(15.6, 7), (21.8, 8.2)]),
            lp(S, [(12, 20), (9.5, 23)]), lp(S, [(12, 20), (14.5, 23)])]


@icon("hermit-crab", CAT, "Crab with claws and legs poking out of a spiral snail shell it carries",
      tags=["crab", "shell", "beach", "crustacean", "seashell", "snail shell"])
def _(S):
    sp = [pt_on(14.5, 9.5, 0.9 + 3.2 * t / 50, 90 + t * 6.6) for t in range(51)]
    return [shell(circle(14.5, 9.5, 6.3)), detail(poly(sp)),
            shell(ellipse(9.5, 17.8, 5, 3)), lp(S, [(5.4, 16.8), (2.6, 14)]), shell(circle(2.4, 11.4, 1.7)),
            lp(S, [(7.5, 15), (7, 12.5)]), dot(7, 11.9, 0.8),
            lp(S, [(10.5, 20.5), (9.5, 22.5)]), lp(S, [(14.5, 20), (15.5, 22.5)]), lp(S, [(17.5, 18.5), (20, 21.5)])]


@icon("horseshoe-crab", CAT, "Horseshoe-shaped domed shell from above with a hinged back plate and a long straight spike tail",
      tags=["living fossil", "marine", "arthropod", "beach", "blue blood", "tail spike"])
def _(S):
    carap = "M2.5 13C2 6.5 7 2.8 12 2.8C17 2.8 22 6.5 21.5 13C21 15.2 18 15 16 14L8 14C6 15 3 15.2 2.5 13Z"
    abd = poly([(8, 13), (16, 13), (15, 19), (9, 19)], closed=True, r=L(S, 0, 1))
    return [shell(union(carap, abd)), detail("M8.2 5.8Q7 9 8.2 11.5"), detail("M15.8 5.8Q17 9 15.8 11.5"),
            lp(S, [(9, 16), (6.5, 18)]), lp(S, [(15, 16), (17.5, 18)]), line(seg(12, 19, 12, 23))]


@icon("trilobite", CAT, "Fossil trilobite from above with a half-moon head shield and a ribbed segmented body",
      tags=["fossil", "prehistoric", "paleozoic", "arthropod", "extinct", "palaeontology"], aliases=["trilobite-fossil"])
def _(S):
    body = "M12 2.5C17.5 2.5 19.5 7 19.5 12C19.5 17 15.8 20.4 12 22C8.2 20.4 4.5 17 4.5 12C4.5 7 6.5 2.5 12 2.5Z"
    return [shell(body), detail("M5 9.2Q12 6.2 19 9.2"), detail(seg(6, 13, 18, 13)), detail(seg(7, 16.4, 17, 16.4))]

# --------------------------------------------------------------------------- worms, snails and other small creatures

@icon("earthworm", CAT, "Long smooth ringed worm in an S curve with a thicker saddle band near the front",
      tags=["worm", "annelid", "garden", "soil", "compost", "fishing bait"])
def _(S):
    pts = path_pts([((2.8, 17.5), (5, 22.5), (9.5, 21.5), (12, 16.5)), ((12, 16.5), (14.5, 11), (17, 8.5), (21, 6.5))], 14)
    body = poly(tube_poly(pts, lambda t: 3.2), closed=True, r=L(S, 0, 0.6))
    return [shell(union(body, circle(*pts[0], 1.5))), *ticks_across(pts, (0.22, 0.36, 0.5), 1.6)]


@icon("earthworm-burrow", CAT, "Soil cross section with grass on top and a worm moving through a winding tunnel",
      tags=["worm", "soil", "underground", "garden", "tunnel", "compost"])
def _(S):
    pts = path_pts([((12, 9), (12, 12.5), (6.5, 12), (7, 15.5)), ((7, 15.5), (7.5, 19.5), (15, 18), (18.5, 19.5))], 12)
    body = poly(tube_poly(pts, lambda t: 2.6), closed=True, r=L(S, 0, 0.6))
    return [line("M2 8H9"), line("M15 8H22"), lp(S, [(4.5, 5.5), (5, 3)]), lp(S, [(18, 5.5), (18.5, 3)]), lp(S, [(20.5, 5.5), (21, 4)]),
            shell(union(body, circle(*pts[-1], 1.3))), dot(18.5, 13, 0.8), dot(3.5, 20, 0.8)]


@icon("leech", CAT, "Flat segmented worm arched in a loop with round suckers at both ends",
      tags=["bloodsucker", "annelid", "parasite", "swamp", "medicinal leech", "worm"])
def _(S):
    pts = path_pts([((4.5, 17.5), (3, 3.5), (19, 2.5), (20, 17.5))], 24)
    body = poly(tube_poly(pts, lambda t: 2.4 + 1.4 * math.sin(math.pi * t) + 0.8 * t), closed=True, r=L(S, 0, 0.6))
    return [shell(union(body, rect(2.2, 16.5, 4.8, 4.2, L(S, 0.5, 2.1)))), shell(rect(17.4, 16.4, 5, 4.8, L(S, 0.5, 2.4))), *ticks_across(pts, (0.3, 0.42, 0.56, 0.68), 1.6)]


@icon("tapeworm", CAT, "Long ribbon made of many small flat segments in a wave with a tiny round head",
      tags=["parasite", "flatworm", "intestinal", "cestode", "ribbon", "worm"])
def _(S):
    pts = path_pts([((5, 4), (5, 10), (19, 8), (19, 13)), ((19, 13), (19, 18), (8, 16), (9, 21.5))], 14)
    body = poly(tube_poly(pts, lambda t: 1.6 + 3.6 * t), closed=True, r=L(S, 0, 0.5))
    return [shell(union(body, circle(5, 3.6, 1.6))), *ticks_across(pts, (0.4, 0.55, 0.7, 0.85), 2.2)]


@icon("planarian", CAT, "Flat worm from above with an arrow-shaped head and two cross-eyed eyespots",
      tags=["flatworm", "regeneration", "pond", "turbellaria", "worm", "biology"])
def _(S):
    body = poly([(12, 21.5), (16.3, 15), (16.4, 10.5), (20.3, 8.2), (12, 3.8), (3.7, 8.2), (7.6, 10.5), (7.7, 15)], closed=True, r=L(S, 0, 1.2))
    return [shell(body), dot(10.7, 8, 1), dot(13.3, 8, 1)]


@icon("bristle-worm", CAT, "Segmented sea worm from above with small paddle legs and bristle tufts along both sides",
      tags=["polychaete", "marine worm", "annelid", "sea", "seabed", "worm"])
def _(S):
    legs = []
    for y in (6.5, 11.5, 16.5):
        legs += sym(S, [(9.7, y), (6, y - 1.8)], [(9.7, y), (6, y + 1.8)])
    return [shell(rect(9.5, 3, 5, 18, L(S, 2, 2.5))), *legs, *sym(S, [(11, 3), (9.5, 1)])]


@icon("tube-worm", CAT, "Two tall tubes rising from the seabed, each topped with a feathery plume",
      tags=["feather duster", "sea worm", "marine", "seabed", "tubeworm", "fanworm"])
def _(S):
    def plume(x, y):
        return [line(f"M{x} {y}C{x - 1} {y - 2} {x - 3} {y - 3.5} {x - 3.5} {y - 6}"), line(f"M{x} {y}V{y - 6.5}"),
                line(f"M{x} {y}C{x + 1} {y - 2} {x + 3} {y - 3.5} {x + 3.5} {y - 6}")]
    return [shell(rect(5, 11, 4, 10, L(S, 1, 2))), shell(rect(14.5, 8.5, 4, 12.5, L(S, 1, 2))), *plume(7, 10), *plume(16.5, 7.5),
            line(seg(2, 21.5, 22, 21.5))]


@icon("christmas-tree-worm", CAT, "Two spiral cone-shaped plumes rising from a coral mound like tiny fir trees",
      tags=["sea worm", "coral reef", "marine", "spirobranchus", "plume", "reef"])
def _(S):
    r = L(S, 0, 0.8)
    t1 = poly([(7.5, 4.2), (11.5, 13.5), (3.5, 13.5)], closed=True, r=r)
    t2 = poly([(16.5, 3.6), (20.5, 13.5), (12.5, 13.5)], closed=True, r=r)
    mound = union(circle(6, 18, 3.8), circle(12, 18.5, 4), circle(18, 18, 3.8), rect(3, 17, 18, 4.5, 1))
    return [shell(union(t1, t2, mound)), detail("M5.8 9.5L9.2 8.5"), detail("M14.8 8.5L18.4 9.5")]


@icon("velvet-worm", CAT, "Soft plump worm in side view with many stubby legs and two antennae",
      tags=["onychophora", "peripatus", "living fossil", "rainforest", "worm", "caterpillar-like"])
def _(S):
    return [shell(rect(3, 9, 18, 7.5, L(S, 3, 3.75))), dot(5.5, 12, 0.9),
            lp(S, [(4.5, 9), (3, 5)]), lp(S, [(7.5, 8.8), (7.5, 4.8)]),
            *[lp(S, [(x, 16.5), (x, 20.5)]) for x in (7, 11, 15, 19)]]


@icon("glowworm", CAT, "Silk threads hanging from a cave ceiling, each dotted with glowing beads of light",
      tags=["glow worm", "bioluminescent", "cave", "waitomo", "fungus gnat", "lights"])
def _(S):
    return [line("M2 4.5C5 6.5 8 3 12 4.8S19 3.2 22 4.8"),
            line(seg(6, 6, 6, 12)), dot(6, 14.2, 1.5), dot(6, 9.5, 0.9),
            line(seg(10.5, 6, 10.5, 17)), dot(10.5, 19.2, 1.5), dot(10.5, 11, 0.9), dot(10.5, 14.2, 0.9),
            line(seg(15, 6, 15, 10)), dot(15, 12.2, 1.5),
            line(seg(19, 6, 19, 14)), dot(19, 16.2, 1.5), dot(19, 10.5, 0.9)]


@icon("bookworm", CAT, "Small worm wearing round glasses peeking out of an open book",
      tags=["reader", "reading", "library", "student", "book lover", "worm"])
def _(S):
    book = "M2 21V12.5C5.5 10.8 9 11 12 13C15 11 18.5 10.8 22 12.5V21C18.5 19.5 15 19.7 12 21.5C9 19.7 5.5 19.5 2 21Z"
    return [shell(union(book, circle(12, 7, 4.8))), dot(9.7, 6.6, 1.5), dot(14.3, 6.6, 1.5), detail(seg(11.2, 6.6, 12.8, 6.6)),
            detail(seg(12, 14.5, 12, 20.5))]


@icon("worm-in-apple", CAT, "Apple with a small worm poking its head out of a round hole in the side",
      tags=["wormy apple", "fruit", "rotten", "pest", "orchard", "worm"])
def _(S):
    apple = "M10 7.5C12 4.8 17.5 5.5 17.5 12.3C17.5 17.8 14 21.5 10 20C6 21.5 2.5 17.8 2.5 12.3C2.5 5.5 8 4.8 10 7.5Z"
    return [shell(apple), line("M10 7.5C10 5.5 10.5 4 12 3"), dot(13.2, 13.2, 2.2), line("M14 12C17.5 10 20 11 20.8 7.5"), dot(20.8, 6.5, 1.5)]


@icon("worm-on-hook", CAT, "Fishing hook with a wriggling worm threaded onto it",
      tags=["bait", "fishing", "angler", "fish hook", "lure", "worm"])
def _(S):
    return [shell(circle(12.5, 3.6, 1.5)), line("M12.5 5.1V17A4.2 4.2 0 0 1 4.1 17V15"), line(poly([(4.1, 15), (2.4, 12.6)], r=0)),
            line("M3.5 9C6.5 4.5 9.5 13 13 9S18 5.5 21 8"), dot(21, 8, 1.4)]


@icon("worm-bin", CAT, "Plastic composting bin with air holes and two worms peeking out of the top",
      tags=["compost", "vermicompost", "worm farm", "recycling", "garden", "kitchen scraps"])
def _(S):
    return [shell(poly([(5, 11.5), (19, 11.5), (17.6, 21.5), (6.4, 21.5)], closed=True, r=L(S, 0, 1.2))),
            shell(rect(3, 9, 18, 2.8, L(S, 0.5, 1.4))),
            dot(9, 16.5, 0.9), dot(12, 16.5, 0.9), dot(15, 16.5, 0.9),
            line("M8.5 9V6C8.5 3.5 11 3.5 11 5.5"), line("M15 9V7"), dot(15, 5.4, 1.4)]


@icon("heartworm", CAT, "Heart shape with a thin wavy worm curled inside it",
      tags=["parasite", "dog", "pet health", "veterinary", "heart disease", "worm"])
def _(S):
    heart = ("M12 20.5C5 15.5 2.5 12 2.5 8.5C2.5 5.5 4.7 3.5 7.3 3.5C9.3 3.5 11 4.6 12 6.5C13 4.6 14.7 3.5 16.7 3.5C19.3 3.5 21.5 5.5 21.5 8.5C21.5 12 19 15.5 12 20.5Z")
    return [shell(heart), detail("M7.2 11C9 8.2 10.8 13.6 12.8 11S16 9.4 17 12.4")]


@icon("slug", CAT, "Slug in side view with a smooth body, a saddle on its back, two raised eye stalks and a slime line",
      tags=["gastropod", "garden pest", "slime", "mollusc", "slimy", "snail without shell"])
def _(S):
    body = "M2.5 17.5C2.5 14 6 12 10.5 12C15 12 19.5 13 21.5 17.5H2.5Z"
    return [shell(union(body, ellipse(13.5, 12.4, 4.8, 2.4))), lp(S, [(3.8, 13), (2.8, 7.8)]), lp(S, [(7.6, 12.3), (8.6, 7.8)]),
            dot(2.7, 7, 1.3), dot(8.8, 7, 1.3), line("M2.5 20.8q2-1.5 4 0t4 0t4 0t4 0t3.5 0")]


@icon("snail-shell", CAT, "Empty spiral snail shell with its round opening facing out",
      tags=["seashell", "gastropod", "spiral", "mollusc", "beach", "empty shell"])
def _(S):
    sp = [pt_on(10.5, 10.5, 0.8 + 4.6 * t / 60, 90 + t * 6.2) for t in range(61)]
    return [shell(union(circle(10.5, 10.5, 8), eo(16.2, 16, 4.6, 3.6, -40))), detail(poly(sp)), mark(eo(16.6, 16.2, 2.4, 1.5, -40))]


@icon("pond-snail", CAT, "Snail in side view with a tall pointed spiral shell and a flat foot",
      tags=["freshwater snail", "aquarium", "pond", "mollusc", "gastropod", "spire"])
def _(S):
    spire = "M9.5 18L14.4 2.8C16.6 4.8 17.5 6.8 17 8.6C19.6 10 20.4 13 19.2 15.4C20.2 16.6 19.8 18 18.5 18Z"
    foot = rect(2.5, 17, 19, 4, L(S, 1.5, 2))
    return [shell(union(spire, foot)), detail("M11 14.3Q15 13.2 18.4 14.8"), detail("M12.6 9.2Q15 8.4 16.8 9.4"),
            lp(S, [(3, 17), (1.8, 13)]), lp(S, [(5.8, 17), (6.2, 13.4)])]


@icon("ramshorn-snail", CAT, "Snail in side view with a flat coiled disc shell like a ram horn",
      tags=["aquarium snail", "planorbidae", "pond", "mollusc", "coil", "gastropod"])
def _(S):
    sp = [pt_on(13.5, 10, 0.6 + 5.6 * t / 90, 90 + t * 7.4) for t in range(91)]
    foot = poly([(2.5, 20.5), (3.4, 15.5), (7, 15.5), (9, 19), (13, 19), (20.5, 20.5)], closed=True, r=L(S, 0, 1.6))
    return [shell(union(circle(13.5, 10, 7.8), foot)), detail(poly(sp)), lp(S, [(4, 15.5), (2.8, 11.5)]), lp(S, [(6.5, 15.5), (7.3, 11.5)])]


@icon("tardigrade", CAT, "Chubby barrel-shaped water bear in side view with a round mouth and eight stubby legs",
      tags=["water bear", "moss piglet", "microscopic", "extremophile", "biology", "animal"])
def _(S):
    body = union(ellipse(13, 11, 8, 5.8), circle(4.6, 11, 2.4))
    return [shell(body), dot(3.6, 11, 1), detail("M10.6 6.2Q11.8 11 10.6 15.8"), detail("M15.6 6.2Q16.8 11 15.6 15.8"),
            *[lp(S, [(x, 16), (x - 0.6, 20.5)]) for x in (7.5, 11.3, 15.2, 19)]]


@icon("hydra-polyp", CAT, "Tall thin tube-shaped animal fixed to a surface with a crown of long thin tentacles on top",
      tags=["hydra", "polyp", "cnidarian", "freshwater", "tentacles", "regeneration"])
def _(S):
    return [line(seg(7, 21.5, 17, 21.5)), shell(rect(10, 9.5, 4, 12, L(S, 1.5, 2))),
            line("M12 8.5V2.8"), line("M10.8 9C9 7.5 8 5 8 2.8"), line("M13.2 9C15 7.5 16 5 16 2.8"),
            line("M10.2 9.8C7.5 9.2 5 7 3.8 4.5"), line("M13.8 9.8C16.5 9.2 19 7 20.2 4.5")]


@icon("compound-eye", CAT, "Dome made of a grid of small hexagons, like a close-up of an insect eye",
      tags=["insect eye", "hexagons", "ommatidia", "vision", "honeycomb", "biology"])
def _(S):
    a = 3.0
    edges = set()

    def hexcell(q, r):
        cx = 12 + a * math.sqrt(3) * (q + r / 2)
        cy = 12 + a * 1.5 * r
        vs = [(cx + a * math.cos(math.radians(-90 + 60 * k)), cy + a * math.sin(math.radians(-90 + 60 * k))) for k in range(6)]
        for k in range(6):
            p1, p2 = vs[k], vs[(k + 1) % 6]
            edges.add(tuple(sorted(((round(p1[0], 2), round(p1[1], 2)), (round(p2[0], 2), round(p2[1], 2))))))

    for q in range(-2, 3):
        for r in range(-2, 3):
            if abs(q + r) > 2:
                continue
            hexcell(q, r)
    parts = [shell(poly(regular(12, 12, 9.8, 10, -90), closed=True, r=L(S, 0, 3)))]
    for (x1, y1), (x2, y2) in sorted(edges):
        if math.hypot(x1 - 12, y1 - 12) <= 8.0 and math.hypot(x2 - 12, y2 - 12) <= 8.0:
            parts.append(detail(seg(x1, y1, x2, y2)))
    return parts


@icon("insect-wing", CAT, "Single clear insect wing with a network of branching veins",
      tags=["wing", "veins", "fly", "membrane", "entomology", "dragonfly wing"])
def _(S):
    w = "M3.5 20.5C3.8 12 9 4.5 20.5 3.5C21.2 9.5 17.5 17.2 8.5 19.8C6.5 20.6 4.8 21 3.5 20.5Z"
    return [shell(w), detail("M6.4 17C8.2 11.8 12.6 8.4 18 7"), detail("M9.4 18C12.4 15.2 16 13.2 19 11.6"), detail(seg(12, 11.2, 13.8, 15.2))]


@icon("insect-anatomy", CAT, "Insect from above split into head, thorax and abdomen with six legs",
      tags=["entomology", "body parts", "thorax", "abdomen", "biology", "diagram"])
def _(S):
    body = union(circle(12, 4.8, 2.4), ellipse(12, 11, 3.4, 3.2), ellipse(12, 18, 3.4, 4.4))
    return [shell(body), detail(seg(9, 7.7, 15, 7.7)), detail(seg(9, 14.4, 15, 14.4)),
            *sym(S, [(8.8, 9.2), (4.5, 7.5), (3, 3.5)], [(8.6, 11), (3.5, 11.5)], [(8.8, 12.8), (4.5, 16), (3.5, 21)]),
            *sym(S, [(11, 3), (9.5, 1.5)])]


@icon("insect-eggs", CAT, "Leaf with a neat cluster of small round eggs laid on it",
      tags=["eggs", "leaf", "butterfly eggs", "larvae", "lifecycle", "laying"])
def _(S):
    eggs = [(10.2, 8.4), (13.8, 8.4), (8.4, 11.8), (12, 11.8), (15.6, 11.8), (10.2, 15.2), (13.8, 15.2)]
    return [
        shell(rot(leaf(12, 2.5, 19.5, 13), 25, 12, 12)), *[dot(*rp([(x, y)], 25)[0], 1.1) for x, y in eggs],
        line(poly(rp([(12, 19.5), (12, 22.5)], 25), r=0))]


@icon("bug-bite", CAT, "Patch of skin with a raised round bump and small radiating itch lines",
      tags=["insect bite", "itch", "mosquito bite", "rash", "skin", "sting"])
def _(S):
    parts = [shell(rect(2.5, 3, 19, 18, L(S, 5, 8))), detail(circle(12, 12, 2.6)), mark(circle(12, 12, 0.8))]
    for k in range(8):
        a = k * 45 + 22.5
        p1, p2 = pt_on(12, 12, 5.8, a), pt_on(12, 12, 7.4, a)
        parts.append(detail(seg(*p1, *p2)))
    return parts