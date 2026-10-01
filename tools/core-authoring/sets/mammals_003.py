"""TypeIcon Core: mammals (batch 003). Small insectivores, xenarthrans, marine mammals, marsupials, hoofed animals and horned heads.

Whole animals are drawn in side view facing left (head on the left); heads are drawn in front view unless stated.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "mammals"


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


def thick(d, w, S):
    """Outline of a stroke of width w along d (limbs, tails, necks inside a silhouette)."""
    return path_to_d(ST(d, w, S.cap, S.join))


def flip(d):
    """Mirror a d-string across the vertical centre line."""
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def grow(d, g):
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled body."""
    return Part("dot", d)


def _p(p):
    return f"{fmt(p[0])} {fmt(p[1])}"


def pt(c, r, deg):
    return (c[0] + r * math.cos(math.radians(deg)), c[1] + r * math.sin(math.radians(deg)))


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    x = u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0]
    y = u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]
    return x, y


def cub(c):
    """d-string of a cubic from four control points."""
    return "M" + _p(c[0]) + "C" + " ".join(_p(q) for q in c[1:])


def across(c, t, half):
    """Segment crossing the cubic c at parameter t, half-length half."""
    x, y = bez(*c, t)
    x2, y2 = bez(*c, min(1, t + 1e-3))
    x1, y1 = bez(*c, max(0, t - 1e-3))
    dx, dy = x2 - x1, y2 - y1
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln
    return seg(x + nx * half, y + ny * half, x - nx * half, y - ny * half)


def soft(S, pts, closed=True, k=1.0):
    return poly(pts, closed=closed, r=L(S, 0, k))


def _nose(S, x, y, w=2.8, h=1.6):
    """Small nose: crisp triangle (Line) or soft oval (Rounded)."""
    if S.name == "line":
        return mark(poly([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x, y + h / 2)], closed=True))
    return mark(ellipse(x, y, w / 2, h / 2 + 0.1))


def legs(xs, top, bottom=21):
    return [line(seg(x, top, x, bottom)) for x in xs]


def stride(x, top, bottom=21, spread=1.0):
    return [line(seg(x - 1, top, x - 1 - spread, bottom)), line(seg(x + 1, top, x + 1 + spread * 0.6, bottom))]


def taper(c, w0, w1, n=14):
    """Closed outline around cubic c whose width goes from w0 to w1 (tails, trunks, snouts)."""
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x, y = bez(*c, t)
        x2, y2 = bez(*c, min(1, t + 1e-3))
        x1, y1 = bez(*c, max(0, t - 1e-3))
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy)
        w = (w0 + (w1 - w0) * t) / 2
        left.append((x - dy / ln * w, y + dx / ln * w))
        right.append((x + dy / ln * w, y - dx / ln * w))
    return poly(left + right[::-1], closed=True, r=0)


def leafshape(S, cx, top, bottom, w):
    """Pointed oval ear from top to bottom: sharp (Line) or round (Rounded)."""
    if S.name == "rounded":
        return ellipse(cx, (top + bottom) / 2, w / 2, (bottom - top) / 2)
    my = (top + bottom) / 2
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + w * 0.66)} {fmt(top + (my - top) * 0.35)} {fmt(cx + w * 0.66)} {fmt(bottom - (bottom - my) * 0.35)} {fmt(cx)} {fmt(bottom)}"
            f"C{fmt(cx - w * 0.66)} {fmt(bottom - (bottom - my) * 0.35)} {fmt(cx - w * 0.66)} {fmt(top + (my - top) * 0.35)} {fmt(cx)} {fmt(top)}Z")


def fluff(S, cx, cy, r, n=14, depth=1.6):
    """Puffy outline: pointed tufts (Line) or scalloped bumps (Rounded)."""
    if S.name == "line":
        return poly([pt((cx, cy), r + (depth if i % 2 == 0 else -depth * 0.3), -90 + i * 360 / n) for i in range(n)], closed=True)
    return union(circle(cx, cy, r - 0.4), *[circle(*pt((cx, cy), r - 0.8, -90 + i * 360 / n), depth * 0.9) for i in range(n)])


# =========================================================================== small mammals


@icon("angora-rabbit", CAT, "Angora rabbit as a round puff of long fur with a small face and tufted ears",
      tags=["angora", "fluffy rabbit", "bunny", "wool", "pet", "fur"])
def _(S):
    ear = leafshape(S, 8.4, 2.4, 9.4, 3.4)
    ear2 = leafshape(S, 15.6, 2.4, 9.4, 3.4)
    body = fluff(S, 12, 14, 7.4, 12, 1.4)
    return [shell(union(body, rot(ear, -8, 8.4, 9.4), rot(ear2, 8, 15.6, 9.4))),
            dot(9.6, 13.4, 1), dot(14.4, 13.4, 1), _nose(S, 12, 16, 2, 1.2)]


@icon("mara", CAT, "Patagonian mara standing on long legs with a rabbit-like head and long ears",
      tags=["patagonian hare", "rodent", "argentina", "long legs", "wildlife"])
def _(S):
    body = union(ellipse(14, 11.4, 6, 3.6), circle(7, 8.4, 2.6), soft(S, [(6, 7.8), (2.4, 9.6), (2.6, 11.2), (6.6, 11.4)], k=0.8),
                 thick(seg(7.6, 9.6, 10, 11), 3.4, S))
    ear = soft(S, [(6.6, 6.2), (7.4, 3.2), (9.2, 6.4)], k=0.5)
    return [shell(union(body, ear)), dot(5.8, 8.2, 0.9), line(seg(11, 14.4, 10.6, 21)), line(seg(14, 14.8, 14, 21)),
            line(poly([(17.6, 13.8), (18.6, 17.6), (18, 21)], r=S.r)), line(seg(20.4, 10.4, 21.6, 9))]


@icon("star-nosed-mole", CAT, "Star-nosed mole face with a ring of fleshy tentacles around its nose and strong claws",
      tags=["mole", "star nose", "tentacles", "burrowing", "wetland", "north america"])
def _(S):
    n = 16
    c = (12, 9)
    if S.name == "line":
        star = poly([pt(c, 6.2 if i % 2 == 0 else 3.8, -90 + i * 360 / n) for i in range(n)], closed=True)
    else:
        star = union(circle(*c, 4.2), *[circle(*pt(c, 4.6, -90 + i * 45), 1.6) for i in range(8)])
    body = union(ellipse(12, 17, 7.4, 4.8), ellipse(12, 12, 4, 3.4))
    claw_l = [line(seg(3.4, 18.4, 2.6, 21)), line(seg(5.2, 19.4, 4.8, 21.6))]
    return [shell(union(body, star)), mark(circle(12, 9, 1.4)), dot(8.8, 12.8, 0.8), dot(15.2, 12.8, 0.8),
            *claw_l, *[line(seg(24 - x1, y1, 24 - x2, y2)) for (x1, y1, x2, y2) in ((3.4, 18.4, 2.6, 21), (5.2, 19.4, 4.8, 21.6))]]


@icon("shrew", CAT, "Shrew in side view with a tiny body, a long pointed snout and a thin tail",
      tags=["tiny mammal", "insectivore", "long snout", "whiskers", "small animal"])
def _(S):
    body = union(ellipse(14.4, 13.6, 6, 3.6), soft(S, [(9.4, 11.6), (3.6, 14.2), (9.6, 15.6)], k=0.6), circle(9.6, 12.4, 2.4))
    return [shell(body), dot(8.6, 12, 0.85), mark(circle(4.4, 14.1, 0.6)), line("M20 14.2C22 14.4 22.4 12.2 21.6 10.4"), line(seg(11.4, 16.6, 11.4, 19.6)), line(seg(17, 16.6, 17, 19.6))]


@icon("elephant-shrew", CAT, "Elephant shrew in side view with a long flexible snout, big eye and long thin legs",
      tags=["sengi", "trunk snout", "africa", "small mammal", "big eye", "long legs"])
def _(S):
    body = union(ellipse(14, 10.6, 5, 3.2), circle(8.6, 9.8, 2.6))
    snout = taper(((7, 10.8), (4.4, 12), (3, 13.6), (3.2, 16)), 2.2, 1)
    return [shell(union(body, snout)), dot(8.4, 9, 1.05), line(poly([(11, 13), (9, 17), (10.4, 21)], r=S.r)),
            line(poly([(16, 13.4), (19, 16), (17.4, 21)], r=S.r)), line("M18.8 9C20.4 8 21.4 6.6 21.6 4.6")]


@icon("colugo", CAT, "Colugo gliding with a wide kite-shaped skin membrane stretched from neck to tail",
      tags=["flying lemur", "gliding", "membrane", "southeast asia", "glide", "mammal"])
def _(S):
    mem = poly([(12, 7.2), (21.4, 7.2), (17.6, 11.8), (19, 17), (13.4, 16.6), (12, 20.6), (10.6, 16.6), (5, 17), (6.4, 11.8), (2.6, 7.2)],
               closed=True, r=L(S, 0, 1.2))
    head = union(circle(12, 5.4, 2.6), circle(9.8, 3.6, 1), circle(14.2, 3.6, 1))
    return [shell(union(mem, head)), dot(11, 5.4, 0.7), dot(13, 5.4, 0.7), detail(seg(12, 10.4, 12, 14.6))]


@icon("rock-hyrax", CAT, "Rock hyrax sitting on a rock with a compact round body, small ears and no tail",
      tags=["hyrax", "dassie", "rock rabbit", "africa", "small mammal", "rocky"])
def _(S):
    rock = poly([(2, 21), (3.6, 17.4), (9, 16.4), (14, 17.6), (19, 16), (22, 21)], closed=True, r=L(S, 0, 1.4))
    body = union(ellipse(13, 11.4, 6, 5), circle(7, 10, 2.8), soft(S, [(6, 10.2), (3, 11.8), (3.6, 13.4), (7, 13.4)], k=0.8),
                 soft(S, [(6.6, 7.6), (7.6, 5.4), (9.2, 7.8)], k=0.4))
    return [shell(rock), shell(minus(body, grow(rock, 0.1))), dot(6.4, 9.6, 0.9), mark(circle(3.6, 11.8, 0.8))]


@icon("sloth", CAT, "Sloth hanging from a branch by long curved claws with a smiling face",
      tags=["tree sloth", "slow", "hanging", "rainforest", "lazy", "branch"])
def _(S):
    body = union(ellipse(12, 12.4, 6.4, 3.6), circle(12, 14.8, 4.4))
    mask = ellipse(12, 15, 3, 2.2)
    return [line(seg(2, 3.5, 22, 3.5)), line("M8 10.6C6.4 8 6 6 7.4 3.5"), line("M16 10.6C17.6 8 18 6 16.6 3.5"),
            shell(body), detail(mask), dot(10.6, 14.4, 0.7), dot(13.4, 14.4, 0.7),
            line(L(S, "M10.6 16.2L12 16.8L13.4 16.2", "M10.6 16Q12 17.4 13.4 16")), line(seg(9, 18.6, 8, 21)), line(seg(15, 18.6, 16, 21))]


@icon("giant-anteater", CAT, "Giant anteater in side view with a very long snout, a shoulder stripe and a huge bushy tail",
      tags=["anteater", "long snout", "south america", "bushy tail", "insect eater"])
def _(S):
    body = union(ellipse(12, 11.4, 6, 3.6), circle(7.6, 9.8, 2.4), taper(((8.4, 10.4), (5.6, 12), (3.6, 14.2), (2.4, 16.4)), 3.4, 1.2))
    tail = taper(((16.4, 9.6), (19.4, 8.6), (20.6, 12.4), (20, 19.6)), 1.6, 4.4)
    return [shell(union(body, tail)), detail(seg(9.4, 8.8, 13, 13.6)), dot(6.8, 9.6, 0.8), mark(circle(2.6, 16.4, 0.6)),
            line(seg(10.4, 14.4, 10.4, 21)), line(seg(15, 14.6, 15.2, 21))]


@icon("armadillo", CAT, "Armadillo in side view with a banded armored shell, a pointed snout and a tapered tail",
      tags=["armored", "bands", "shell", "south america", "burrowing", "texas"])
def _(S):
    shellp = minus(ellipse(13.4, 14.6, 7.4, 6), rect(0, 14.6, 24, 10))
    head = union(circle(5.6, 12.6, 2.4), soft(S, [(5, 11.2), (1.8, 13.6), (2.2, 14.8), (6, 14.8)], k=0.7))
    body = union(shellp, rect(6.4, 14, 14.8, 2, 0), head)
    tail = taper(((20.4, 15), (22, 16.4), (22.2, 18.4), (21.2, 20)), 2.4, 0.8)
    return [shell(union(body, tail)), detail("M10 9.4C9.6 11 9.6 12.6 10 14"), detail("M13.4 8.8C13 10.6 13 12.4 13.4 14"), detail("M16.8 9.4C17 11 17 12.6 16.8 14"),
            dot(5.2, 12.2, 0.8), line(seg(9, 16.4, 8.6, 20)), line(seg(17, 16.4, 17.4, 20))]


@icon("pangolin", CAT, "Pangolin in side view covered in overlapping pointed scales with a long tapering tail",
      tags=["scaly anteater", "scales", "armored", "endangered", "africa", "asia"])
def _(S):
    body = union(ellipse(11.4, 12.4, 6.4, 4), circle(5.6, 11.4, 2.4), soft(S, [(5, 10), (2, 12.6), (2.4, 13.8), (6, 14)], k=0.6))
    tail = taper(((16.4, 12), (20, 12.4), (22, 15), (21, 19.6)), 4, 1)
    sc = [detail(f"M{x} {y}l1.6 1.6l1.6 -1.6") for (x, y) in ((8.6, 9.4), (12.6, 9.4), (10.6, 12.8))]
    return [shell(union(body, tail)), dot(4.8, 11, 0.75), *sc, line(seg(8.6, 16.4, 8.6, 20)), line(seg(14.4, 16.4, 14.4, 20))]


@icon("aardvark", CAT, "Aardvark in side view with an arched back, a long tube snout, tall ears and a thick tail",
      tags=["antbear", "africa", "termite eater", "long ears", "burrowing", "nocturnal"])
def _(S):
    body = union(rot(ellipse(13.4, 11.6, 6.8, 4.6), 8, 13.4, 11.6), circle(8.4, 10.4, 2.6), taper(((8.6, 11.2), (5.6, 13), (3.6, 15), (2.6, 17)), 3.6, 1.6))
    ear = leafshape(S, 9.6, 3, 9, 2.8)
    tail = taper(((18.8, 12.6), (20.6, 15), (21.6, 17.6), (21.6, 20.4)), 3.6, 1.4)
    return [shell(union(body, rot(ear, 14, 9.6, 9), tail)), dot(7.6, 10, 0.8), mark(circle(2.6, 17, 0.6)),
            line(seg(10.6, 15.4, 10.6, 21)), line(seg(16, 15.6, 16.4, 21))]


@icon("long-eared-bat", CAT, "Bat face with huge ears almost as long as its head and small folded wings",
      tags=["bat", "big ears", "nocturnal", "echolocation", "flying mammal", "plecotus"])
def _(S):
    ear_l = rot(leafshape(S, 7, 2.4, 13, 4.4), -12, 7, 13)
    ear_r = flip(ear_l)
    head = union(circle(12, 14.6, 4.4), ear_l, ear_r)
    wings = [soft(S, [(8.6, 18.6), (3.4, 17.8), (5, 21.6), (9.6, 20.4)], k=0.7), soft(S, [(15.4, 18.6), (20.6, 17.8), (19, 21.6), (14.4, 20.4)], k=0.7)]
    return [shell(union(head, *wings)), dot(10.2, 14, 0.85), dot(13.8, 14, 0.85), _nose(S, 12, 16.4, 1.8, 1),
            detail(L(S, "M6.4 5L7.4 11", "M6.4 5.4C6.4 7.4 6.8 9.4 7.4 11")), detail(flip(L(S, "M6.4 5L7.4 11", "M6.4 5.4C6.4 7.4 6.8 9.4 7.4 11")))]


@icon("horseshoe-bat", CAT, "Horseshoe bat hanging upside down with a horseshoe-shaped leaf nose and pointed ears",
      tags=["bat", "leaf nose", "hanging", "cave", "nocturnal", "roost"])
def _(S):
    wrap = union(ellipse(12, 9, 4.6, 6.4), circle(12, 15.6, 4))
    ear_l = soft(S, [(8.6, 15), (6, 19.6), (10.4, 18.6)], k=0.5)
    ear_r = soft(S, [(15.4, 15), (18, 19.6), (13.6, 18.6)], k=0.5)
    return [line(seg(3, 2.6, 21, 2.6)), shell(union(wrap, ear_l, ear_r)), detail("M8.4 10.4C8.8 13.6 15.2 13.6 15.6 10.4"),
            dot(10.4, 15.4, 0.75), dot(13.6, 15.4, 0.75), detail(L(S, "M10.4 17.8C11.2 18.8 12.8 18.8 13.6 17.8", "M10.4 17.6C11.2 19 12.8 19 13.6 17.6"))]


# =========================================================================== marine mammals


def cet(S, cx, cy, rx, ry, tx, flukes=True):
    """Cetacean silhouette facing left: round body, tail stalk and a two-lobed fluke ending near x = tx + 2.6."""
    stalk = taper(((cx + rx - 1.5, cy), (cx + rx + 1, cy - 0.3), (tx - 2, cy - 0.3), (tx, cy - 0.2)), ry * 1.3, 1.6)
    fl = poly([(tx - 0.6, cy - 0.2), (tx + 1.4, cy - 4.2), (tx + 2.6, cy - 3.2), (tx + 1.8, cy - 0.2), (tx + 2.6, cy + 2.8), (tx + 1.4, cy + 3.8)],
              closed=True, r=L(S, 0, 0.6))
    return union(ellipse(cx, cy, rx, ry), stalk, fl)


def flip_(S, x, y, dx=2.6, dy=3.6):
    return poly([(x, y), (x + dx * 0.2, y + dy), (x + dx, y + 0.6)], closed=True, r=L(S, 0, 0.8))


@icon("walrus", CAT, "Walrus face with a bristly muzzle pad and two long tusks pointing down",
      tags=["tusks", "arctic", "marine mammal", "whiskers", "pinniped", "sea animal"])
def _(S):
    head = union(ellipse(12, 10.4, 8, 6.4), circle(9.6, 13.4, 2.6), circle(14.4, 13.4, 2.6))
    tusk_l = taper(((9.2, 15), (8.6, 17.4), (8.4, 19.6), (8.6, 21.4)), 2.4, 1) if S.name == "line" else thick("M9.2 15C8.6 17.4 8.4 19.6 8.6 21", 2, S)
    return [shell(union(head, tusk_l, flip(tusk_l))), dot(8.8, 8.8, 0.9), dot(15.2, 8.8, 0.9), mark(ellipse(12, 11.4, 1.6, 1)),
            detail(seg(12, 13, 12, 15.6))]


@icon("orca", CAT, "Orca in side view with a tall dorsal fin, a pale eye patch and a pale belly",
      tags=["killer whale", "whale", "dorsal fin", "ocean", "marine mammal", "sea animal"])
def _(S):
    body = union(cet(S, 10.4, 12.6, 8.4, 4.4, 19), poly([(8.8, 9), (11.4, 3), (13.6, 9)], closed=True, r=L(S, 0, 0.8)), flip_(S, 9.6, 15.8))
    return [shell(body), dot(4.8, 11.6, 0.75), detail("M6.6 9.6L9 10.6"), detail("M4 14.4C8 15.6 12 15.2 15.6 13.6")]

@icon("sperm-whale", CAT, "Sperm whale in side view with a huge square head and a narrow lower jaw",
      tags=["whale", "moby dick", "deep diver", "ocean", "marine mammal", "sea animal"])
def _(S):
    head = rect(2.4, 6.6, 10.6, 8.8, L(S, 1.4, 3.4))
    body = cet(S, 14, 12.2, 6, 3.8, 19.4)
    jaw = rect(3.4, 16.4, 7, 2.2, L(S, 0.2, 1))
    return [shell(union(head, body)), shell(jaw), dot(5.6, 9.6, 0.85)]

@icon("narwhal", CAT, "Narwhal swimming in side view with a long straight tusk projecting from its head",
      tags=["unicorn of the sea", "tusk", "arctic", "whale", "marine mammal", "sea animal"])
def _(S):
    body = union(cet(S, 11.4, 14.6, 7.6, 3.8, 19.6), flip_(S, 10, 17.6, 2.4, 2.6))
    return [shell(body), line(seg(5.6, 12.6, 2.4, 4.4)), dot(6.6, 13.4, 0.8), detail(seg(13.4, 15.4, 17, 15.4))]

@icon("beluga", CAT, "Beluga whale in side view with a bulging round forehead, no dorsal fin and a smiling mouth",
      tags=["white whale", "arctic", "melon", "smile", "marine mammal", "sea animal"])
def _(S):
    body = union(cet(S, 11, 13.6, 8.2, 4.4, 19.2), circle(6.6, 10.4, 3.6), flip_(S, 10.6, 16.8, 2.4, 2.6))
    return [shell(body), dot(5.6, 12.2, 0.8), detail(L(S, "M2.8 15L5.2 16L7.8 15.2", "M2.8 14.8Q5.4 17 8 15"))]

@icon("manatee", CAT, "Manatee floating in side view with a rounded body, a small flipper and a round paddle tail",
      tags=["sea cow", "dugong", "gentle giant", "florida", "marine mammal", "sea animal"])
def _(S):
    body = union(ellipse(11.4, 12, 8, 4.8), taper(((17, 12), (19, 12.4), (20, 12.6), (21, 12.6)), 4, 2), ellipse(20.4, 12.6, 2.4, 3.6))
    head = union(circle(5, 11.6, 2.6))
    flipper = rot(ellipse(8.4, 17, 1.6, 3), 28, 8.4, 17)
    return [shell(union(body, head, flipper)), dot(4.2, 10.6, 0.8), mark(ellipse(3.2, 13.2, 0.9, 0.6)), detail(seg(12, 9.6, 12.6, 13.4)) if False else detail("M11 8.6C12 11 12 13 11 15")]


@icon("sea-lion", CAT, "Sea lion sitting upright on its flippers with a ball balanced on its nose",
      tags=["seal", "circus", "ball", "trick", "marine mammal", "sea animal", "aquarium"])
def _(S):
    head = union(circle(11.6, 9.4, 3.4), ellipse(8, 10.4, 2.6, 1.6))
    body = taper(((12, 11.4), (13.4, 14), (13.6, 17), (13, 20.4)), 6, 7.4)
    flipper = poly([(12, 20.4), (16, 19.4), (20.6, 20.6), (16.6, 21.6)], closed=True, r=L(S, 0, 0.6))
    fl = poly([(10.6, 13.6), (7.4, 17.6), (9.6, 18.4), (12.4, 15.4)], closed=True, r=L(S, 0, 0.6))
    return [shell(union(head, body, flipper, fl)), dot(11.2, 8.6, 0.8), mark(circle(6.2, 9.9, 0.7)), shell(circle(7.4, 3.8, 2.2))]


@icon("hooded-seal", CAT, "Hooded seal head with a large inflated balloon bulging from one nostril",
      tags=["balloon nose", "bladder", "arctic", "seal", "marine mammal", "sea animal"])
def _(S):
    head = union(circle(13, 15.4, 5), ellipse(8.4, 16.8, 3.4, 2.4), taper(((13, 19), (13.4, 21), (13.4, 22), (13.4, 22.4)), 7, 7))
    balloon = circle(9.6, 7, 4.6)
    return [shell(union(head, balloon)), dot(12.4, 14, 0.85), mark(circle(5.4, 16.2, 0.8)), detail("M6.4 10.6C7.6 12.4 9.4 12.8 11 12.2")]


@icon("river-dolphin", CAT, "River dolphin in side view with a very long thin beak, a rounded forehead and a low hump",
      tags=["amazon dolphin", "boto", "freshwater", "beak", "marine mammal", "river"])
def _(S):
    beak = taper(((6.6, 12.8), (4, 14), (2.6, 15.8), (2.6, 18)), 2.4, 1)
    body = union(cet(S, 11.4, 12.6, 6.8, 3.8, 18.8), circle(7.8, 10.4, 3), beak, flip_(S, 10.4, 15.2, 2.4, 2.8),
                 poly([(14, 9.4), (15.6, 7.6), (17.4, 9.8)], closed=True, r=L(S, 0, 0.8)))
    return [shell(body), dot(6.8, 10.4, 0.8)]

@icon("whale-tail", CAT, "Whale tail fluke rising out of the water with a notch in the middle",
      tags=["fluke", "diving whale", "ocean", "whale watching", "marine mammal", "sea animal"])
def _(S):
    fluke = ("M10.4 19.4L10.6 14.6C9 13.6 4.4 12.8 2.4 5.6C5.6 7.4 9.6 7.8 12 10.4C14.4 7.8 18.4 7.4 21.6 5.6C19.6 12.8 15 13.6 13.4 14.6L13.6 19.4Z"
             if S.name == "line" else
             "M10.4 19.4L10.6 14.8C8.8 13.8 4.8 12.6 3 6.6C2.8 5.8 3.4 5.4 4 5.8C6.6 7.4 9.8 7.6 12 10.2C14.2 7.6 17.4 7.4 20 5.8C20.6 5.4 21.2 5.8 21 6.6C19.2 12.6 15.2 13.8 13.4 14.8L13.6 19.4Z")
    return [shell(fluke), line(seg(2, 19.4, 22, 19.4)), line(seg(6, 22, 18, 22))]


# =========================================================================== marsupials and monotremes


def efluff(S, cx, cy, rx, ry, n=16, d=1.5):
    """Ellipse outline with tufts (Line) or bumps (Rounded) for woolly or spiny coats."""
    pts = [(cx + (rx + (d if i % 2 == 0 else -d * 0.3)) * math.cos(2 * math.pi * i / n - math.pi / 2),
            cy + (ry + (d if i % 2 == 0 else -d * 0.3)) * math.sin(2 * math.pi * i / n - math.pi / 2)) for i in range(n)]
    if S.name == "line":
        return poly(pts, closed=True)
    return union(ellipse(cx, cy, rx, ry), *[circle(cx + rx * math.cos(2 * math.pi * i / n - math.pi / 2), cy + ry * math.sin(2 * math.pi * i / n - math.pi / 2), d * 0.95)
                                          for i in range(n)])


@icon("wombat", CAT, "Wombat in side view with a stout barrel body, short legs, a broad flat nose and small ears",
      tags=["marsupial", "burrowing", "australia", "stocky", "digger", "wildlife"])
def _(S):
    body = union(ellipse(13.4, 13, 7.6, 5), circle(5.6, 12.4, 3.2), soft(S, [(5, 10.6), (2.4, 12.4), (2.6, 14.6), (5.6, 15.4)], k=0.8),
                 soft(S, [(6, 9.6), (7.2, 7.2), (8.8, 9.8)], k=0.5))
    return [shell(body), dot(5.6, 11.6, 0.85), mark(ellipse(2.8, 12.8, 0.8, 0.6)), line(seg(8.4, 17, 8.4, 20.6)), line(seg(12, 17.6, 12, 20.6)),
            line(seg(16, 17.6, 16, 20.6)), line(seg(19.4, 16.4, 19.4, 20.6))]


@icon("tasmanian-devil", CAT, "Tasmanian devil with a stocky dark body, a pale chest band and an open toothy mouth",
      tags=["devil", "marsupial", "tasmania", "australia", "scavenger", "growl"])
def _(S):
    body = union(ellipse(14, 12.6, 6.4, 4.2), circle(6, 9.8, 3.4), soft(S, [(6, 8.2), (2.6, 8.8), (2.4, 12.8), (6.6, 12.8)], k=0.8),
                 circle(8.6, 6.6, 1.5))
    return [shell(body), dot(6.4, 8.8, 0.85), detail(seg(2.6, 11, 5.6, 11.4)), detail(seg(10, 11.6, 10.8, 16.6)),
            line(seg(10.4, 16.8, 10, 21)), line(seg(14, 16.8, 14, 21)), line(seg(18, 16, 18.6, 21)), line("M20.2 11.6C21.4 12 22 13.4 21.8 15")]


@icon("opossum", CAT, "Opossum hanging by its curled tail from a branch, with a pointed face and round ears",
      tags=["possum", "marsupial", "hanging", "tail", "north america", "playing dead"])
def _(S):
    body = union(ellipse(12.6, 13, 5.6, 3.4), circle(6.4, 14.6, 2.6), soft(S, [(6, 13.4), (2.6, 16.6), (2.6, 17.8), (6.4, 17)], k=0.7),
                 circle(8, 11.6, 1.4))
    return [line(seg(2, 3.4, 22, 3.4)), shell(body), dot(6.6, 14, 0.8), mark(circle(2.8, 17.4, 0.6)),
            line("M17.4 12C21 11 21.2 6 18.6 3.4C17.6 2.6 16.6 3.6 17.4 4.6"), line(seg(10.6, 16, 10.6, 19.6)), line(seg(14.6, 16, 14.6, 19.6))]


@icon("sugar-glider", CAT, "Sugar glider gliding with its skin membrane stretched between its legs, big eyes and a long tail",
      tags=["glider", "marsupial", "flying squirrel", "gliding", "australia", "pet"])
def _(S):
    mem = poly([(12, 8.4), (21.6, 8), (18.6, 15.8), (12, 14.6), (5.4, 15.8), (2.4, 8)], closed=True, r=L(S, 0, 1.4))
    head = union(circle(12, 5.4, 2.8), circle(9.4, 3.6, 1.3), circle(14.6, 3.6, 1.3))
    return [shell(union(mem, head)), dot(10.8, 5.2, 0.85), dot(13.2, 5.2, 0.85), line("M12 14.6C12 18 15.6 18 15.6 21.4")]


@icon("quokka", CAT, "Quokka sitting with a round face, small rounded ears and a big smile",
      tags=["happy animal", "smile", "rottnest island", "marsupial", "australia", "selfie"])
def _(S):
    head = union(circle(12, 10.4, 6.4), circle(6.8, 5.2, 1.8), circle(17.2, 5.2, 1.8))
    body = soft(S, [(6.4, 21), (6, 17.4), (9, 15.4), (15, 15.4), (18, 17.4), (17.6, 21)], k=2.4)
    return [shell(union(head, body)), dot(9.4, 9.4, 0.9), dot(14.6, 9.4, 0.9), _nose(S, 12, 11.4, 2.2, 1.4),
            detail(L(S, "M8.8 13.4L12 15.2L15.2 13.4", "M8.6 13.2Q12 16.6 15.4 13.2"))]


@icon("numbat", CAT, "Numbat in side view with pale stripes across its back, a pointed snout and a bushy tail held up",
      tags=["banded anteater", "marsupial", "termite eater", "australia", "stripes", "endangered"])
def _(S):
    body = union(ellipse(12.8, 12.6, 6.4, 3), circle(6, 11.2, 2.4), soft(S, [(5.6, 9.8), (2.4, 12), (2.6, 13), (6.4, 13.2)], k=0.6),
                 soft(S, [(6.4, 9.2), (7.2, 7), (8.8, 9.4)], k=0.4))
    tail = taper(((18.2, 11.4), (20.4, 9.4), (20.6, 6), (20.2, 3.2)), 2, 4.8)
    return [shell(union(body, tail)), dot(5.6, 10.6, 0.75), detail(seg(11, 9.6, 11, 15.6)), detail(seg(14, 9.6, 14, 15.6)), detail(seg(17, 10.2, 17, 15)),
            *stride(9.6, 15.2), *stride(16, 15.2)]


@icon("bilby", CAT, "Bilby in side view with long rabbit-like ears, a long pointed snout and a long tail",
      tags=["rabbit-eared bandicoot", "marsupial", "easter bilby", "australia", "desert", "burrow"])
def _(S):
    body = union(ellipse(13.4, 13, 5.4, 3.6), circle(7.6, 11.4, 2.6), soft(S, [(7, 10.2), (2.4, 13.2), (2.8, 14.2), (7.6, 14)], k=0.6))
    ear = leafshape(S, 9.6, 2.6, 9.6, 2.8)
    return [shell(union(body, rot(ear, 18, 9.6, 9.6))), dot(7, 10.8, 0.8), line("M18.6 12.4C21 13.4 22 16 21.6 19.6"), mark(circle(21.6, 19.6, 1.3)),
            line(poly([(11, 15.8), (11.6, 18.6), (9.6, 21)], r=S.r)), line(poly([(16, 16), (18, 18.6), (17, 21)], r=S.r))]


@icon("quoll", CAT, "Quoll in side view with a cat-sized body covered in white spots, a pointed snout and a long tail",
      tags=["spotted marsupial", "native cat", "australia", "spots", "carnivore", "wildlife"])
def _(S):
    body = union(ellipse(13.6, 11.4, 6.2, 3.2), circle(6, 9.6, 2.5), soft(S, [(5.6, 8.4), (2.4, 10.4), (2.6, 11.4), (6.4, 11.8)], k=0.6),
                 soft(S, [(6.6, 7.6), (7.4, 5.4), (9, 7.8)], k=0.4))
    return [shell(body), dot(5.6, 9.2, 0.75), *stride(9.8, 14), *stride(16.6, 14), line("M19.8 10.6C22 11.4 22.4 15 21.8 18.4"),
            *[mark(circle(x, y, 0.75)) for x, y in ((11, 10.2), (14, 9.8), (17, 10.6), (12.6, 12.6), (15.8, 12.8))]]


@icon("thylacine", CAT, "Thylacine, the extinct Tasmanian tiger, in side view with dark stripes across its back and a stiff tail",
      tags=["tasmanian tiger", "extinct", "marsupial", "stripes", "tasmania", "cryptid"])
def _(S):
    body = union(ellipse(12.6, 11.4, 6.4, 3.4), circle(6, 9.8, 2.6), soft(S, [(5.6, 8.6), (2.2, 10.2), (2.4, 11.8), (6.6, 12.2)], k=0.6),
                 soft(S, [(6.6, 7.8), (7.4, 5.6), (9, 8.2)], k=0.4), taper(((17.4, 11), (19.4, 11.2), (21, 11.4), (22, 11.6)), 2.6, 1.4))
    return [shell(body), dot(5.6, 9.4, 0.75), detail("M13 8.4L13.4 12.4"), detail("M15.4 8.8L15.6 12.8"), detail("M17.6 9.8L17.6 13"),
            *stride(9.4, 14.2), *stride(16, 14.2)]


@icon("tree-kangaroo", CAT, "Tree kangaroo sitting on a branch with a bear-like face, strong arms and a long hanging tail",
      tags=["marsupial", "rainforest", "new guinea", "climbing", "branch", "australia"])
def _(S):
    head = union(circle(9, 6.8, 3), circle(6.4, 4.4, 1.2), circle(11.6, 4.4, 1.2))
    body = ellipse(10.6, 13.6, 4.2, 4.4)
    return [line(seg(2, 19.6, 17, 19.6)), shell(union(head, body)), dot(8, 6.6, 0.75), dot(10.2, 6.6, 0.75), mark(circle(9, 8.2, 0.7)),
            line(poly([(8, 12), (5.4, 13.6), (5, 16)], r=S.r)), line("M14.4 15C18 15.4 20 17 20.6 20.6"), line(seg(13.4, 17.6, 14.6, 19.6))]


@icon("platypus", CAT, "Platypus seen from above with a flat duck-like bill, webbed feet and a flat beaver-like tail",
      tags=["monotreme", "duckbill", "egg-laying mammal", "australia", "river", "wildlife"])
def _(S):
    bill = rect(2.2, 10, 7.4, 4, L(S, 1, 2))
    body = ellipse(12.8, 12, 5.2, 4)
    tail = ellipse(20, 12, 2.8, 2)
    feet = [line(poly([(10.4, 8.4), (9, 5.6), (11, 3.4)], r=S.r)), line(poly([(10.4, 15.6), (9, 18.4), (11, 20.6)], r=S.r)),
            line(poly([(15.6, 8.4), (16.6, 5.6), (18.4, 4.2)], r=S.r)), line(poly([(15.6, 15.6), (16.6, 18.4), (18.4, 19.8)], r=S.r))]
    return [shell(union(bill, body, tail)), *feet, dot(9.6, 10.6, 0.7), dot(9.6, 13.4, 0.7)]


@icon("echidna", CAT, "Echidna in side view with a dome of sharp spines and a long thin beak-like snout",
      tags=["spiny anteater", "monotreme", "spikes", "australia", "egg-laying mammal", "wildlife"])
def _(S):
    dome = minus(ellipse(13.6, 16.4, 7.6, 7), rect(0, 16.4, 24, 10))
    snout = taper(((7, 14.6), (5, 14.8), (3.6, 15.4), (2.6, 16.6)), 2.8, 1.2)
    spikes = [line(seg(*pt((13.6, 16.4), 7.6, a), *pt((13.6, 16.4), 10, a))) for a in (-165, -135, -105, -75, -45, -15)] if S.name == "line" else \
        [line(seg(*pt((13.6, 16.4), 7.6, a), *pt((13.6, 16.4), 9.6, a))) for a in (-160, -130, -100, -70, -40)]
    return [shell(union(dome, snout, rect(6.4, 15.6, 14, 2, 0))), *spikes, dot(6, 14.4, 0.7), line(seg(9.6, 18.6, 9.6, 20.6)), line(seg(17.6, 18.6, 17.6, 20.6))]


# =========================================================================== hoofed animals and pigs


@icon("donkey", CAT, "Donkey face with very long upright ears, a pale muzzle and a short upright mane",
      tags=["ass", "burro", "farm animal", "long ears", "pack animal", "mule"])
def _(S):
    ear = rot(leafshape(S, 6.2, 1.6, 11, 3.2), -16, 6.2, 11)
    face = union(ellipse(12, 12.4, 4.4, 6.4), ellipse(12, 17.8, 3.2, 3))
    return [shell(union(face, ear, flip(ear))), detail(ellipse(12, 18, 2.2, 1.6) if S.name == "rounded" else "M9.6 16.4L14.4 16.4"),
            dot(9.8, 10.6, 0.85), dot(14.2, 10.6, 0.85), mark(circle(10.8, 18.6, 0.6)), mark(circle(13.2, 18.6, 0.6)), detail(seg(12, 6.4, 12, 8.2))]

@icon("przewalskis-horse", CAT, "Przewalski's horse in side view with a stocky body, a short stiff upright mane and a pale muzzle",
      tags=["wild horse", "takhi", "mongolia", "steppe", "mane", "equine"])
def _(S):
    body = union(ellipse(14, 12.4, 6.4, 3.6), taper(((8.6, 11), (7, 9), (6.4, 7), (6, 5.4)), 4.4, 3.4), rot(ellipse(4.6, 7.6, 3.4, 1.9), 55, 4.6, 7.6),
                 *[poly([(6.6 + i * 1.3, 5 - i * 0.3), (7.4 + i * 1.3, 3 - i * 0.2), (8.4 + i * 1.3, 5.2 - i * 0.3)], closed=True, r=L(S, 0, 0.4)) for i in range(3)])
    return [shell(body), dot(5.4, 6.8, 0.75), line(seg(10, 15.4, 9.6, 21)), line(seg(12.6, 15.6, 12.6, 21)), line(seg(16.4, 15.6, 16.4, 21)), line(seg(19, 14.8, 19.6, 21)),
            line("M20.2 10.6C21.6 12 22 15 21.4 18")]


@icon("okapi", CAT, "Okapi in side view with a giraffe-like head, a plain body and bold horizontal stripes on its rump and legs",
      tags=["forest giraffe", "stripes", "congo", "africa", "rainforest", "wildlife"])
def _(S):
    body = union(rot(ellipse(14, 11.6, 6.4, 3.6), 6, 14, 11.6), taper(((8.8, 10.4), (7.4, 8), (6.6, 5.8), (6, 4.2)), 4, 2.6), rot(ellipse(4.8, 3.6, 2.4, 1.5), -15, 4.8, 3.6),
                 circle(6.4, 2.6, 0.9))
    return [shell(body), dot(4.6, 3.2, 0.6), detail(seg(17, 8.8, 17.6, 14.4)), detail(seg(19, 10, 19.4, 13.8)), line(seg(10, 15, 10, 21)), line(seg(12.6, 15.2, 12.6, 21)),
            line(seg(16.6, 15.2, 16.6, 21)), line(seg(19.2, 14.4, 19.2, 21)), detail(seg(15.4, 17, 17.8, 17)), detail(seg(15.4, 19.4, 17.8, 19.4))]


@icon("tapir", CAT, "Tapir in side view with a short flexible trunk-like snout and a pale saddle across its middle",
      tags=["malayan tapir", "trunk", "saddle", "rainforest", "south america", "asia"])
def _(S):
    body = ellipse(13.6, 12.4, 7, 4.4)
    head = union(circle(6, 10.4, 3), taper(((5, 10.8), (3.6, 12), (3, 13.6), (3.6, 15.6)), 3.4, 2.4), circle(7.4, 7.8, 1.2))
    saddle = minus(body, rect(0, 0, 12.4, 30), rect(17.4, 0, 10, 30))
    return [shell(union(body, head)), mark(saddle), dot(5.6, 9.6, 0.75), line(seg(9.4, 16.4, 9.4, 21)), line(seg(12.6, 16.6, 12.6, 21)),
            line(seg(16.4, 16.6, 16.4, 21)), line(seg(19, 15.6, 19, 21))]


@icon("warthog", CAT, "Warthog face with two large upward curving tusks, wart bumps on the cheeks and a bristly mane",
      tags=["pig", "tusks", "africa", "safari", "wild pig", "savanna"])
def _(S):
    mane = poly([(8, 8.6), (9.4, 4), (12, 7.2), (14.6, 4), (16, 8.6)], closed=True)
    face = union(ellipse(12, 12.6, 6, 5.2), ellipse(12, 16.4, 3.6, 2.8), rot(ellipse(5.6, 8.6, 1.8, 2.6), -25, 5.6, 8.6), rot(ellipse(18.4, 8.6, 1.8, 2.6), 25, 18.4, 8.6))
    tusk = "M8.6 17.4C4 18 2.4 14 4.4 10.2"
    return [shell(union(face, mane if S.name == "line" else minus(mane, rect(0, 0, 1, 1)))), line(tusk), line(flip(tusk)), dot(9.2, 11.6, 0.8), dot(14.8, 11.6, 0.8),
            mark(circle(10.6, 16.4, 0.7)), mark(circle(13.4, 16.4, 0.7)), detail(circle(7.8, 14.4, 0.6)) if False else dot(7.6, 14.6, 0.6), dot(16.4, 14.6, 0.6)]


@icon("wild-boar", CAT, "Wild boar in side view with a bristly ridge along the back, a long snout and short upturned tusks",
      tags=["hog", "pig", "tusks", "forest", "bristles", "hunting"])
def _(S):
    ridge = poly([(9.6, 8.6), (10.6, 5.4), (12, 7.6), (13.4, 5), (14.8, 7.6), (16.2, 5.4), (17.4, 8.6)], closed=True)
    body = union(ellipse(14, 12, 6.4, 4), circle(6.4, 11.4, 3), soft(S, [(6, 9.8), (2.4, 12.4), (2.8, 14.4), (6.6, 14.4)], k=0.8),
                 soft(S, [(6.6, 8.8), (7.8, 6.2), (9.2, 9.2)], k=0.4), ridge)
    return [shell(body), dot(5.6, 10.6, 0.75), line(seg(4.4, 14.4, 4.6, 12.8)), line(seg(9.8, 15.4, 9.8, 21)), line(seg(12.6, 15.8, 12.6, 21)),
            line(seg(16.4, 15.8, 16.4, 21)), line(seg(19, 14.6, 19.4, 21))]


@icon("babirusa", CAT, "Babirusa head in profile with upper tusks growing up through the snout and curling back toward the forehead",
      tags=["deer pig", "tusks", "sulawesi", "indonesia", "wild pig", "curved tusks"])
def _(S):
    head = union(circle(13, 13, 5.4), ellipse(7.4, 15, 3.6, 2.6), soft(S, [(15, 9), (17, 5.6), (18.4, 10.4)], k=0.5), rect(10, 16, 9, 5, 0))
    return [shell(head), dot(11.4, 11.6, 0.8), mark(circle(4.6, 14.6, 0.7)), line("M6.2 12.4C3.6 8 5.6 2.6 10.4 3.2C12.4 3.6 13 5 12.6 6.4")]

@icon("red-river-hog", CAT, "Red river hog face with long white ear tufts, a pale stripe down the face and a long snout",
      tags=["bush pig", "pig", "africa", "tufts", "rainforest", "wild pig"])
def _(S):
    tuft = rot(leafshape(S, 6.4, 1.8, 11, 3.2), -14, 6.4, 11)
    face = union(ellipse(12, 12.6, 5.2, 5.4), ellipse(12, 17.6, 3.2, 3))
    return [shell(union(face, tuft, flip(tuft))), detail(seg(12, 8, 12, 13.6)), dot(9.6, 12, 0.8), dot(14.4, 12, 0.8), mark(circle(10.8, 17.4, 0.75)), mark(circle(13.2, 17.4, 0.75))]


@icon("pot-bellied-pig", CAT, "Pot-bellied pig in side view with a swayed back, a sagging belly and a short snout",
      tags=["pig", "pet pig", "mini pig", "farm animal", "swayback", "piglet"])
def _(S):
    body = union(ellipse(9.6, 13.4, 4.4, 4), ellipse(16.8, 13.2, 4.6, 4.4), ellipse(13.2, 16, 6.6, 3.2), circle(5.4, 13.4, 2.8), ellipse(2.8, 14.8, 1.4, 1.6),
                 soft(S, [(5.4, 10.8), (5.8, 8.6), (8.4, 10.8)], k=0.4))
    return [shell(body), dot(5, 13, 0.75), line(seg(8.4, 18.6, 8.4, 21)), line(seg(17.6, 18.6, 17.6, 21)), line("M20.6 11C22 10.4 22.6 12.4 21.4 13")]


@icon("mangalica-pig", CAT, "Mangalica pig in side view covered in a thick curly woolly coat like a sheep",
      tags=["woolly pig", "curly hair", "hungarian", "pig", "farm animal", "heritage breed"])
def _(S):
    body = efluff(S, 14, 12, 6, 3.6, 18, 0.9)
    head = union(circle(6.2, 12, 2.6), ellipse(3.6, 13.4, 1.6, 1.6), soft(S, [(5.8, 9.6), (6.6, 7.6), (8.6, 10)], k=0.4))
    return [shell(union(body, head)), dot(5.6, 11.4, 0.75), line(seg(9.8, 16.6, 9.8, 20.6)), line(seg(18, 16.6, 18, 20.6))]


# =========================================================================== cattle and antelopes


def face(S, rx=4.2, ry=6, cy=13.4, muz=True):
    """Front-view hoofed face: long oval, eyes and a muzzle with nostrils."""
    parts = [ellipse(12, cy, rx, ry)]
    if muz:
        parts.append(ellipse(12, cy + ry - 1, rx - 0.6, 2.6))
    return union(*parts)


def eyes(y, dx=2.4, r=0.85):
    return [dot(12 - dx, y, r), dot(12 + dx, y, r)]


def nostrils(y, dx=1.1):
    return [mark(circle(12 - dx, y, 0.6)), mark(circle(12 + dx, y, 0.6))]


def ear_h(S, x, y, ang, w=2.2, h=1.3):
    return rot(ellipse(x, y, w, h), ang, x, y)


def sym(d):
    return union(d, flip(d))


def side_quad(S, bx=14, by=11.6, rx=6.4, ry=3.8, head=(5.4, 9.6), hr=2.6, leg_top=14.6, leg_xs=(9.8, 12.4, 16, 18.6)):
    """Hoofed body in side view: body ellipse, neck, head circle with muzzle. Returns the silhouette (legs are added as lines)."""
    hx, hy = head
    return union(ellipse(bx, by, rx, ry), circle(hx, hy, hr), soft(S, [(hx - 0.4, hy - hr + 0.6), (hx - hr - 2, hy + 1.2), (hx - hr - 1.8, hy + 2.6), (hx + 0.6, hy + hr)], k=0.8),
                 thick(seg(bx - rx + 1.4, by - 0.6, hx + 0.8, hy + 0.6), 3.6, S))


def qlegs(xs=(9.8, 12.4, 16, 18.6), top=14.6, bottom=21):
    return [line(seg(x, top, x + (0.3 if i % 2 else -0.3), bottom)) for i, x in enumerate(xs)]


@icon("bison", CAT, "American bison in side view with a massive shoulder hump, a shaggy head and beard and short curved horns",
      tags=["buffalo", "american bison", "prairie", "great plains", "hump", "wildlife"])
def _(S):
    body = union(ellipse(14.4, 12.4, 6.6, 4.4), circle(9.8, 9, 4.6), circle(5.6, 13, 3.4), soft(S, [(4, 15.4), (5, 19.4), (8.4, 15.6)], k=0.6))
    return [shell(body), line("M4.8 10.6C3.4 9.4 3.6 7.6 5.2 7"), dot(5.6, 12.4, 0.8), line(seg(11, 16.4, 11, 21)), line(seg(14.4, 16.8, 14.4, 21)),
            line(seg(18, 16, 18.4, 21)), line("M20.8 10C21.8 11 22 13 21.4 15")]


@icon("yak", CAT, "Yak in side view with long shaggy hair hanging to the ground, a shoulder hump and wide curved horns",
      tags=["tibet", "himalaya", "shaggy", "mountain cattle", "horns", "highland"])
def _(S):
    skirt = poly([(6.6, 11), (6.6, 18.4), (8.6, 17), (10.6, 19.2), (12.6, 17), (14.6, 19.2), (16.6, 17), (18.6, 19.2), (20, 17.2), (20, 11)], closed=True)
    body = union(ellipse(13.4, 10.4, 7, 4), skirt, circle(5.4, 10.6, 2.8), circle(10, 7.4, 2.6))
    return [shell(body), line("M4.6 8.4C2.6 7 2 4.6 3.4 3") if False else line("M5 8.4C2.4 7.2 1.8 4.6 3.2 3"), dot(4.8, 10, 0.75), line(seg(9, 19.6, 9, 21.4)), line(seg(17, 19.6, 17, 21.4))]


@icon("water-buffalo", CAT, "Water buffalo head with very wide crescent horns sweeping back and out from the top of the head",
      tags=["buffalo", "carabao", "asia", "rice farming", "crescent horns", "livestock"])
def _(S):
    horn = taper(((9.2, 9), (4, 4), (1.8, 7.6), (2.8, 12.4)), 3.2, 1)
    return [shell(union(face(S, 4, 6, 13.2), sym(horn), ear_h(S, 7, 11.6, -20), ear_h(S, 17, 11.6, 20))), *eyes(11.6, 2.1), *nostrils(18.6)]


@icon("african-buffalo", CAT, "Cape buffalo head with horns joined in a heavy boss across the forehead that curve down and then up",
      tags=["cape buffalo", "big five", "safari", "boss", "horns", "africa"])
def _(S):
    horn = taper(((9, 7.6), (2.4, 7.4), (1.6, 14.4), (3.8, 11.2)), 3.4, 1)
    boss = rect(7.6, 5.4, 8.8, 3.6, L(S, 1, 1.8))
    return [shell(union(face(S, 4, 5.6, 13.6), boss, sym(horn), ear_h(S, 6.8, 12.6, 25, 2, 1.1), ear_h(S, 17.2, 12.6, -25, 2, 1.1))), *eyes(12, 2.1), *nostrils(18.6)]


@icon("zebu", CAT, "Zebu cow in side view with a large hump over the shoulders, drooping ears and a loose dewlap",
      tags=["brahman", "humped cattle", "india", "cow", "hump", "dewlap"])
def _(S):
    body = union(ellipse(14.4, 12.4, 6.4, 3.8), circle(10.2, 8, 2.8), circle(5.6, 10.4, 2.6), soft(S, [(5.2, 9.4), (2.4, 11), (2.6, 12.8), (6, 12.8)], k=0.8),
                 soft(S, [(7.6, 12), (8.4, 17), (11.6, 14)], k=0.8), ear_h(S, 6.8, 13, 50, 1.6, 0.9))
    return [shell(body), dot(5.2, 9.8, 0.75), line(seg(5.6, 7.6, 6.4, 5.2)), line(seg(11.6, 16, 11.6, 21)), line(seg(14.6, 16.2, 14.6, 21)),
            line(seg(17.6, 16, 17.8, 21)), line("M20.8 10.4C21.8 12 21.6 15 21.2 17.6")]


@icon("highland-cow", CAT, "Highland cow face with a long shaggy fringe covering the eyes and long wide upcurved horns",
      tags=["scottish cow", "scotland", "shaggy", "fringe", "horns", "cattle"])
def _(S):
    horn = taper(((7.4, 8.4), (2, 9.6), (1.6, 4.4), (4, 2.4)), 3, 1)
    fringe = poly([(7, 6.4), (17, 6.4), (17.4, 14), (15.4, 12.2), (13.8, 14.2), (12, 12.2), (10.2, 14.2), (8.6, 12.2), (6.6, 14)], closed=True)
    return [shell(union(face(S, 4.2, 6.2, 13.6), fringe, sym(horn))), dot(9.8, 13.4, 0.75), dot(14.2, 13.4, 0.75), *nostrils(19)]


@icon("longhorn-cattle", CAT, "Longhorn steer head with extremely long horns stretching wide to both sides",
      tags=["texas longhorn", "steer", "cow", "horns", "cattle", "western"])
def _(S):
    horn = taper(((9, 8.6), (3.4, 6.4), (1.8, 9.6), (1.8, 5)), 2.6, 0.9)
    return [shell(union(face(S, 3.8, 6, 13.6), sym(horn), ear_h(S, 7.4, 10.4, 10, 2.2, 1.1), ear_h(S, 16.6, 10.4, -10, 2.2, 1.1))), *eyes(12, 2, 0.8), *nostrils(18.8)]


@icon("ankole-watusi", CAT, "Ankole-Watusi cattle head with enormous thick lyre-shaped horns rising up and out",
      tags=["watusi", "african cattle", "lyre horns", "big horns", "africa", "cow"])
def _(S):
    horn = taper(((9.4, 10), (2.2, 9), (2.6, 4), (5, 2)), 4.8, 1.4)
    return [shell(union(face(S, 3.4, 5.4, 14.2), sym(horn))), *eyes(13, 1.9, 0.8), *nostrils(19.2, 1)]


@icon("belted-galloway", CAT, "Belted Galloway cow in side view with a shaggy dark body and a wide white belt around the middle",
      tags=["belted cow", "oreo cow", "scottish cattle", "cow", "belt", "farm animal"])
def _(S):
    body = union(ellipse(14, 11.4, 7, 4.2), circle(5.8, 9.6, 2.8), soft(S, [(5.4, 8.4), (2.4, 10.2), (2.6, 12), (6.2, 12)], k=0.8), ear_h(S, 7.8, 7.4, -30, 1.6, 0.9))
    return [shell(body), dot(5.4, 9, 0.75), detail("M11.6 7.6L11.6 15"), detail("M16.6 7.8L16.6 15"), line(seg(9.4, 15.6, 9.4, 21)), line(seg(12.4, 16, 12.4, 21)),
            line(seg(16.2, 16, 16.2, 21)), line(seg(19.2, 15, 19.4, 21))]


@icon("musk-ox", CAT, "Musk ox with a long shaggy coat hanging to the ground and heavy horns curving down beside the face",
      tags=["arctic", "tundra", "shaggy", "horns", "greenland", "ox"])
def _(S):
    hair = poly([(6.6, 8), (17.4, 8), (20.6, 21), (17.6, 19), (15, 21), (12, 19), (9, 21), (6.4, 19), (3.4, 21)], closed=True)
    horn = taper(((9, 6.6), (3, 6), (2.6, 11.6), (4.8, 14.6)), 3.2, 1)
    return [shell(union(hair, sym(horn), face(S, 3.2, 4.6, 11.6, False))), *eyes(11, 1.8, 0.8), mark(ellipse(12, 15.2, 1.6, 1))]


@icon("takin", CAT, "Takin in side view with a bulky body, a large arched Roman nose and short horns curving back",
      tags=["goat antelope", "himalaya", "bhutan", "roman nose", "golden fleece", "wildlife"])
def _(S):
    body = union(ellipse(14.6, 11.6, 6.6, 4.4), rot(ellipse(5.8, 10.4, 3.8, 2.6), 28, 5.8, 10.4), circle(3.8, 11.8, 1.6), thick(seg(9, 10.4, 7, 9.4), 4.4, S))
    return [shell(body), dot(6.4, 9.2, 0.75), line("M7.8 7.6C9 5.4 10.8 5 11.8 5.6"), line(seg(10.2, 15.6, 10.2, 21)), line(seg(13.4, 16, 13.4, 21)),
            line(seg(17, 16, 17.2, 21)), line(seg(19.8, 15.2, 20, 21))]


@icon("gazelle", CAT, "Gazelle in side view with a slender body, a dark side stripe and ringed lyre-shaped horns",
      tags=["thomson's gazelle", "antelope", "savanna", "africa", "speed", "horns"])
def _(S):
    body = union(ellipse(14, 11.6, 6, 3), taper(((9.4, 10.6), (7.6, 8.4), (6.6, 6.4), (6.4, 5)), 3.2, 2.2), rot(ellipse(5.6, 4.8, 2.4, 1.5), 25, 5.6, 4.8))
    return [shell(body), dot(5.2, 4.2, 0.6), line("M6.2 3.4C5 1.8 5.4 1 6.4 1.6") if False else line("M7 3.6C6 2.4 6.4 1.8 7.4 1.6"), detail(seg(9.6, 12.6, 18.6, 12.6)),
            line(seg(10.4, 14.4, 10, 21)), line(seg(12.6, 14.4, 13, 21)), line(seg(16.4, 14.4, 16, 21)), line(seg(18.6, 13.6, 19.2, 21)), line(seg(20, 10.2, 21.6, 9))]


@icon("impala", CAT, "Impala head with long elegant lyre-shaped ringed horns spreading up and outward",
      tags=["antelope", "savanna", "africa", "lyre horns", "safari", "horns"])
def _(S):
    horn = "M9.8 9.4C5 8.4 5.2 4.4 8.6 4.2C11 4 9.4 1.6 6.4 1.4"
    return [shell(union(face(S, 3.2, 5.8, 14.2), ear_h(S, 6.6, 11.4, -25, 2.4, 1.2), ear_h(S, 17.4, 11.4, 25, 2.4, 1.2))), line(horn), line(flip(horn)), *eyes(12.4, 1.9, 0.8), *nostrils(19.2, 1)]


@icon("springbok", CAT, "Springbok mid-leap pronking with all four legs stiff and its back arched, with short curved horns",
      tags=["antelope", "pronking", "jump", "south africa", "leap", "horns"])
def _(S):
    body = union(rot(ellipse(13.4, 9.6, 6.2, 3.2), -6, 13.4, 9.6), rot(ellipse(5.8, 11, 2.8, 1.7), 40, 5.8, 11), thick(seg(8.6, 9.4, 6.6, 10.6), 3.2, S))
    return [shell(body), dot(5.4, 10.4, 0.6), line("M6.8 9C6.8 7 7.6 5.6 8.8 5"), line(seg(10, 12.4, 9.4, 19)), line(seg(12.6, 12.6, 12.6, 19.4)), line(seg(16, 12.4, 16.4, 19)),
            line(seg(18.4, 11.4, 19.4, 18.4))]


@icon("oryx", CAT, "Oryx in side view with very long straight spear-like horns and a dark and pale face mask",
      tags=["gemsbok", "antelope", "desert", "long horns", "africa", "arabia"])
def _(S):
    body = union(ellipse(14, 12.4, 6, 3.4), taper(((9.4, 11), (7.6, 9.4), (6.6, 8), (6.2, 7)), 3.4, 2.4), rot(ellipse(5, 8.4, 3, 1.7), 35, 5, 8.4))
    return [shell(body), dot(5.6, 7.6, 0.6), line(seg(6.6, 6.6, 14, 1.8)), line(seg(7.6, 7, 15, 3.4)) if False else line(seg(7.8, 6.6, 15.2, 3)), detail(seg(3.4, 8.6, 5.4, 6.4)),
            line(seg(10.4, 15, 10.4, 21)), line(seg(12.6, 15.2, 12.8, 21)), line(seg(16.4, 15.2, 16.2, 21)), line(seg(18.6, 14.4, 19, 21)), line("M20 10.6C21.4 12 21.8 15.6 21 18.4")]


@icon("kudu", CAT, "Greater kudu head with long open spiral corkscrew horns and large rounded ears",
      tags=["antelope", "spiral horns", "corkscrew", "africa", "safari", "greater kudu"])
def _(S):
    horn = "M10 9.4C6 8.8 5 6.8 8 6.2C10.6 5.6 9.4 3.8 6 3.4C5 3.2 4.6 2.8 4.8 2.4"
    return [shell(union(face(S, 3.2, 5.6, 14), ear_h(S, 5.6, 11.6, -30, 3, 1.8), ear_h(S, 18.4, 11.6, 30, 3, 1.8))), line(horn), line(flip(horn)), *eyes(12.6, 1.8, 0.8), *nostrils(18.6, 1)]


@icon("eland", CAT, "Eland in side view with a large heavy body, a hanging dewlap and straight tightly twisted horns",
      tags=["antelope", "largest antelope", "africa", "savanna", "dewlap", "horns"])
def _(S):
    body = union(ellipse(14.4, 11.8, 6.8, 4.2), circle(9.6, 8.6, 2.4), rot(ellipse(5, 9.4, 3, 1.8), 30, 5, 9.4), thick(seg(9.4, 10, 6.4, 9.2), 4, S),
                 soft(S, [(8.4, 11.6), (9, 17), (12, 14)], k=0.8))
    return [shell(body), dot(5.4, 8.6, 0.6), line(seg(6.4, 7.6, 9, 2.6)), line(seg(7.4, 8, 10.4, 3.4)), line(seg(11, 16, 11, 21)), line(seg(14.6, 16.2, 14.6, 21)),
            line(seg(18, 16, 18.2, 21)), line("M21 10.6C22 12.4 21.6 15 21 17")]


@icon("sable-antelope", CAT, "Sable antelope head in profile with long scimitar horns curving strongly backward and pale face stripes",
      tags=["antelope", "scimitar horns", "africa", "safari", "sable", "horns"])
def _(S):
    head = union(circle(9.6, 12.4, 3.4), ellipse(5.4, 14.6, 3.2, 2), soft(S, [(10, 9.4), (11.4, 6.8), (12.8, 10.4)], k=0.5), taper(((11, 14), (13, 17), (15, 18.4), (16.6, 20)), 5, 6))
    mane = [line(seg(14.4 + i * 1.4, 12 + i * 0.8, 16.8 + i * 1.4, 10.6 + i * 0.8)) for i in range(0)]
    return [shell(head), line("M9.4 9C10 3.4 16 2.4 21.4 7.6"), dot(8.8, 11.6, 0.75), detail(seg(3.6, 13.6, 7.2, 15.6)), mark(circle(3.2, 14.8, 0.6))]


@icon("blackbuck", CAT, "Blackbuck head with two long corkscrew spiral horns forming a V and pale rings around the eyes",
      tags=["antelope", "india", "spiral horns", "v shape", "corkscrew", "wildlife"])
def _(S):
    horn = "M10 8.8C7.4 7.6 9.6 6 7 4.8C4.8 3.8 6.6 2.4 4.4 1.4"
    return [shell(union(face(S, 3.4, 6, 14.4), ear_h(S, 6.6, 11.6, -30, 2.2, 1.2), ear_h(S, 17.4, 11.6, 30, 2.2, 1.2))), line(horn), line(flip(horn)),
            detail(circle(9.6, 13, 1.5)), detail(circle(14.4, 13, 1.5)), dot(9.6, 13, 0.7), dot(14.4, 13, 0.7), *nostrils(19.8, 1)]


@icon("wildebeest", CAT, "Wildebeest in side view with a sloping back, a shaggy beard, a mane and cow-like curved horns",
      tags=["gnu", "migration", "serengeti", "africa", "antelope", "beard"])
def _(S):
    mane = poly([(6.6, 6.4), (8, 3.6), (9.2, 5.8), (10.6, 4), (11.6, 6.6), (11.6, 9.4), (7, 9.4)], closed=True)
    body = union(rot(ellipse(14.6, 12.2, 6.6, 3.6), 10, 14.6, 12.2), rot(ellipse(5.2, 9.6, 3, 2.4), 25, 5.2, 9.6), thick(seg(9.4, 10.2, 7, 8), 4.4, S), mane)
    return [shell(body), dot(5.6, 8.8, 0.7), line("M5.8 7.4C3.6 7 2.8 4.8 4 3.4"), detail(seg(4.6, 12, 5, 14.6)), line(seg(10.6, 14.6, 10.4, 21)), line(seg(13.2, 15, 13.2, 21)),
            line(seg(17, 15.6, 17, 21)), line(seg(19.6, 15.4, 20, 21)), line("M21 12C21.8 14 21.8 16.6 21.2 18.6")]


@icon("hartebeest", CAT, "Hartebeest head with a very long narrow face and horns rising from a pedicle in a bracket shape",
      tags=["antelope", "long face", "africa", "savanna", "bracket horns", "wildlife"])
def _(S):
    horn = taper(((10.6, 6.4), (10.6, 2.2), (6.2, 1.8), (4.8, 4.6)), 2.6, 1)
    return [shell(union(face(S, 3, 7, 14, True), sym(horn), ear_h(S, 6.8, 9.6, -30, 2, 1), ear_h(S, 17.2, 9.6, 30, 2, 1))), *eyes(10, 1.8, 0.75), *nostrils(19.6, 0.9)]


@icon("gerenuk", CAT, "Gerenuk standing upright on its hind legs with a very long thin neck reaching up to a branch",
      tags=["giraffe antelope", "long neck", "browsing", "east africa", "antelope", "standing"])
def _(S):
    body = union(rot(ellipse(14.4, 13.2, 5.2, 2.8), -48, 14.4, 13.2), taper(((12.4, 10.4), (10.4, 8), (9.6, 5.8), (9, 4.4)), 2.8, 1.8), ellipse(7.8, 4, 2.4, 1.4))
    return [shell(body), dot(7.2, 3.6, 0.55), line(seg(14.2, 15.6, 13.4, 21)), line(seg(17, 14.8, 17.6, 21)), line(seg(2.2, 6.6, 6, 4.2)), line(seg(3.4, 5.8, 3.2, 3.6)),
            line("M19.4 10C21 10.6 21.6 12.4 21 14")]


@icon("dik-dik", CAT, "Dik-dik head with a small pointed face, huge round eyes, a short mobile snout and a crest tuft between short horns",
      tags=["tiny antelope", "big eyes", "africa", "small deer", "crest", "wildlife"])
def _(S):
    crest = poly([(9.6, 8.4), (10.6, 4), (12, 6.4), (13.4, 3.4), (14.4, 8.4)], closed=True)
    face_ = union(ellipse(12, 13.4, 4.4, 5), poly([(8.6, 15), (12, 21.6), (15.4, 15)], closed=True, r=L(S, 0, 1.6)))
    return [shell(union(face_, crest, ear_h(S, 6, 10.4, -30, 2.6, 1.4), ear_h(S, 18, 10.4, 30, 2.6, 1.4))), dot(9.6, 12.6, 1.4), dot(14.4, 12.6, 1.4), _nose(S, 12, 18.4, 1.8, 1),
            line(seg(8.6, 8.2, 7.6, 4.6)), line(seg(15.4, 8.2, 16.4, 4.6))]


@icon("klipspringer", CAT, "Klipspringer standing on the tips of its hooves on a small rock peak with short spike horns",
      tags=["antelope", "rock jumper", "cliff", "africa", "tiptoe", "small antelope"])
def _(S):
    rock = poly([(3.4, 21), (9.4, 15.6), (12, 17.8), (15, 14.6), (21, 21)], closed=True, r=L(S, 0, 1))
    body = union(ellipse(13.6, 8.8, 4.6, 2.6), thick(seg(10.4, 8, 8, 6.4), 3, S), circle(7, 5.8, 1.9), soft(S, [(6.2, 5.6), (3.8, 7), (4.4, 8), (6.8, 7.4)], k=0.6))
    return [shell(rock), shell(body), dot(6.6, 5.2, 0.6), line(seg(7.6, 4.2, 8.4, 1.8)), line(seg(11.4, 11, 11.6, 14.4)), line(seg(13, 11.2, 13.2, 14.6)),
            line(seg(15.4, 11, 15.4, 13.8)), line(seg(17, 10.4, 17.4, 14.6)) if False else line(seg(17, 10.6, 17, 13.4))]


@icon("saiga-antelope", CAT, "Saiga antelope head with a large bulbous drooping nose and short ringed horns",
      tags=["steppe", "kazakhstan", "big nose", "antelope", "endangered", "central asia"])
def _(S):
    nose = union(ellipse(12, 17, 4.6, 3.6))
    head = union(ellipse(12, 11.4, 4.2, 6), nose, ear_h(S, 6.4, 8.6, -25, 2, 1), ear_h(S, 17.6, 8.6, 25, 2, 1))
    return [shell(head), *eyes(9.8, 2, 0.8), mark(ellipse(10.2, 17.6, 0.9, 1.3)), mark(ellipse(13.8, 17.6, 0.9, 1.3)), line(seg(9.4, 5.6, 8.6, 2)), line(seg(14.6, 5.6, 15.4, 2)),
            detail(seg(8.4, 3.6, 10, 4)) if False else detail(seg(12, 13.6, 12, 15.2))]


@icon("pronghorn", CAT, "Pronghorn in side view with forked black horns, pale bands on the throat and a white rump patch",
      tags=["antelope", "north america", "prairie", "fast", "forked horns", "wildlife"])
def _(S):
    body = union(ellipse(14, 11.6, 6.4, 3.2), taper(((9, 10.4), (7.6, 8.4), (6.8, 6.6), (6.4, 5.4)), 3.4, 2.4), rot(ellipse(5.4, 5.2, 2.6, 1.6), 25, 5.4, 5.2))
    return [shell(body), dot(5, 4.6, 0.6), line("M6.6 3.6L7.4 1.4L9.2 1.2"), line(seg(7, 2.6, 5.6, 1.6)), detail(seg(7.4, 8.6, 9.6, 9.4)), mark(ellipse(19.4, 10.8, 1.4, 1.9)),
            line(seg(10.4, 14.4, 10, 21)), line(seg(12.6, 14.4, 13, 21)), line(seg(16.4, 14.4, 16, 21)), line(seg(18.6, 13.8, 19.2, 21))]


@icon("bongo", CAT, "Bongo antelope in side view with thin white vertical stripes on its body and spiralling horns",
      tags=["forest antelope", "stripes", "africa", "rainforest", "horns", "rare"])
def _(S):
    body = union(ellipse(14, 11.6, 6.8, 3.6), thick(seg(9, 10.4, 6.6, 8), 4, S), rot(ellipse(5.2, 6.8, 2.8, 1.7), 25, 5.2, 6.8), leafshape(S, 7.8, 3.6, 7.4, 1.8))
    return [shell(body), dot(4.8, 6.2, 0.6), line("M6.2 5.4C7.4 2.8 10.6 1.6 13 2.6"), detail(seg(10.4, 9.6, 10.4, 13.6)), detail(seg(13, 9.2, 13, 14)), detail(seg(15.6, 9.6, 15.6, 13.6)),
            detail(seg(18.2, 10.4, 18.2, 12.8)), line(seg(10.4, 15, 10.4, 21)), line(seg(13, 15.2, 13, 21)), line(seg(17, 15.2, 17, 21)), line(seg(19.6, 14.4, 19.8, 21))]


@icon("chamois", CAT, "Chamois head with short upright black horns that hook sharply backward at the tips",
      tags=["alps", "mountain goat antelope", "hooked horns", "europe", "mountain", "wildlife"])
def _(S):
    horn = "M10 8.4L9.6 3.4C9.6 1.8 7.4 1.6 6.4 3"
    return [shell(union(face(S, 3.4, 5.8, 14.2), ear_h(S, 6.6, 10.6, -25, 2.2, 1.2), ear_h(S, 17.4, 10.6, 25, 2.2, 1.2))), line(horn), line(flip(horn)), *eyes(12.4, 1.9, 0.8),
            detail(seg(7.4, 12.6, 10, 15.6)), detail(seg(16.6, 12.6, 14, 15.6)), *nostrils(19.4, 1)]


@icon("mountain-goat", CAT, "Mountain goat in side view on a ledge with a shaggy white coat, a beard and short black dagger horns",
      tags=["rocky mountain goat", "cliff", "climbing", "beard", "horns", "mountain"])
def _(S):
    body = union(efluff(S, 13.6, 11, 6.4, 3.8, 16, 1), circle(5.6, 8.4, 2.6), soft(S, [(5.2, 7.4), (2.6, 9.4), (3, 10.6), (6.4, 10.6)], k=0.7), soft(S, [(4, 11), (4.6, 14.4), (6.6, 11.4)], k=0.5))
    return [shell(body), dot(5.4, 8, 0.6), line(seg(6.6, 6.2, 8.2, 2.6)), line(seg(10.4, 15.8, 10.4, 19.8)), line(seg(17, 15.8, 17, 19.8)), line(seg(2.6, 21.4, 21.4, 21.4))]


@icon("markhor", CAT, "Markhor head with tall corkscrew horns twisting upward and a long flowing beard",
      tags=["wild goat", "corkscrew horns", "pakistan", "mountain", "beard", "screw horn"])
def _(S):
    horn = "M10 6.6C7.4 5.6 9 4 6.4 3C4.4 2.2 6.6 1 4.6 0.6" if False else "M10.4 6.6C7.4 5.8 9 4.2 6.6 3.4C5 2.8 6.6 1.8 5.4 1.4"
    beard = taper(((12, 14), (11.4, 17), (12.6, 19.6), (12, 22.4)), 3.4, 0.9)
    return [shell(union(face(S, 3.2, 5.2, 10.6, False), beard, ear_h(S, 6.4, 8.8, -25, 2.2, 1.1), ear_h(S, 17.6, 8.8, 25, 2.2, 1.1))), line(horn), line(flip(horn)), *eyes(9.6, 1.8, 0.8),
            mark(ellipse(12, 13.2, 1.2, 0.8))]


@icon("bighorn-sheep", CAT, "Bighorn sheep head in profile with a massive horn curling around in a full circle beside the face",
      tags=["ram", "rocky mountains", "curled horn", "north america", "wild sheep", "mountain"])
def _(S):
    head = union(circle(10.4, 15, 4), ellipse(5.6, 16.8, 3.2, 2.2), rect(8.6, 17, 8, 4.6, 0))
    horn = thick(arc(13.4, 11.4, 4.6, 185, 440), 3, S)
    return [shell(union(head, horn)), dot(9, 13.6, 0.75), mark(circle(3.8, 16.6, 0.6))]


@icon("barbary-sheep", CAT, "Barbary sheep in side view with long fringe hair hanging from the throat and front legs and backward curved horns",
      tags=["aoudad", "north africa", "wild sheep", "fringe", "horns", "desert"])
def _(S):
    body = union(ellipse(14.4, 11.6, 6.4, 3.8), circle(6.4, 8.8, 2.6), soft(S, [(6, 7.6), (2.8, 9.6), (3.2, 10.8), (6.8, 10.8)], k=0.7),
                 thick(seg(9.6, 10.2, 7, 9.4), 4, S), soft(S, [(7, 11.4), (5.6, 17.6), (8.4, 15.4), (9.6, 18), (11, 13)], k=0.4))
    return [shell(body), dot(6, 8.2, 0.6), line("M7.2 6.6C9.4 4.4 12 4.6 12.6 6.6"), line(seg(12.4, 15.4, 12.4, 21)), line(seg(16.4, 15.4, 16.4, 21)), line(seg(19.6, 14.6, 19.8, 21))]
