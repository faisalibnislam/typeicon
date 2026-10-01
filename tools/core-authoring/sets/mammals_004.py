"""TypeIcon Core: mammals (batch 004). Sheep and goat heads, deer, ice age and prehistoric mammals, tracks and skulls.

Whole animals are drawn in side view facing left (head on the left), matching sets/mammals_001.py.
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
    """Segment crossing the cubic c at parameter t, half-length half (bands on tails)."""
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
    """A walking pair of legs under x: one reaching forward, one back."""
    return [line(seg(x - 1, top, x - 1 - spread, bottom)), line(seg(x + 1, top, x + 1 + spread * 0.6, bottom))]



def taper(c, w0, w1, n=12, S=None):
    """Closed outline around cubic c whose width goes from w0 to w1 (a bushy tail)."""
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x, y = bez(*c, t)
        x2, y2 = bez(*c, min(1, t + 1e-3))
        x1, y1 = bez(*c, max(0, t - 1e-3))
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy)
        w = (w0 + (w1 - w0) * math.sin(math.pi * t * 0.6) / math.sin(math.pi * 0.6)) / 2 if t < 1 else w1 / 2
        left.append((x - dy / ln * w, y + dx / ln * w))
        right.append((x + dy / ln * w, y - dx / ln * w))
    return poly(left + right[::-1], closed=True, r=0)





def mp(pts):
    """Mirror a point list across the vertical centre line."""
    return [(24 - x, y) for x, y in pts]


def wave(p0, p1, amp, turns, n=24, taper_to=1.0):
    """Points of a corkscrew-like wave running from p0 to p1 (amplitude shrinks towards p1)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln
    out = []
    for i in range(n + 1):
        t = i / n
        a = amp * (1 - (1 - taper_to) * t) * math.sin(2 * math.pi * turns * t)
        out.append((p0[0] + dx * t + nx * a, p0[1] + dy * t + ny * a))
    return out


# =========================================================================== sheep and goats

def _sheep_face(S):
    return soft(S, [(8.4, 9.4), (15.6, 9.4), (15.2, 16.4), (12, 20.4), (8.8, 16.4)], k=2)


@icon("jacob-sheep", CAT, "Jacob sheep head with four horns, two curving up and two curling down beside the face",
      tags=["sheep", "four horned sheep", "rare breed", "horns", "farm", "livestock"])
def _(S):
    up = "M9.8 9C9.4 5.4 7.4 3 4.2 3.2"
    curl = "M8.6 11C4.8 9.6 2.4 12.4 3.4 15.2C4 16.8 6 16.6 6 15"
    return [shell(_sheep_face(S)), line(up), line(flip(up)), line(curl), line(flip(curl)),
            dot(10.4, 13, 1), dot(13.6, 13, 1), _nose(S, 12, 18, 2.2, 1.3)]


@icon("racka-sheep", CAT, "Racka sheep head with long straight horns twisted like corkscrews spiraling upward in a V",
      tags=["sheep", "corkscrew horns", "hungarian", "twisted horns", "rare breed", "livestock"])
def _(S):
    w = wave((10, 8.4), (3.6, 1.6), 1.5, 2, taper_to=0.8)
    wr = [(24 - x, y) for x, y in w]
    return [shell(_sheep_face(S)), line(poly(w, r=S.r * 0.5)), line(poly(wr, r=S.r * 0.5)),
            dot(10.4, 13, 1), dot(13.6, 13, 1), _nose(S, 12, 18, 2.2, 1.3)]


@icon("nubian-goat", CAT, "Nubian goat head in profile with a convex Roman nose, a small beard and a long drooping ear",
      tags=["goat", "roman nose", "floppy ear", "dairy goat", "livestock", "farm"])
def _(S):
    head = ("M11 3.6C9.4 4.2 8.2 5.4 7.2 6.8C5.6 7.6 2.8 9.4 3 12.6C3.2 15.4 4.6 17 6.6 17.4C8.6 17.8 10.6 17 11.6 15.8"
            "L14.5 21L21 21L17.6 12C16.6 8 14.6 4.2 11 3.6Z")
    beard = soft(S, [(4.8, 16.8), (8.6, 17.6), (6.2, 21.6)], k=0.6)
    ear = "M12.4 6.4C16 6.4 17 11.4 16.2 15.2C15.6 17.6 14 18.4 12.8 17.4C11.4 16.2 10.8 10.4 12.4 6.4Z"
    return [shell(union(head, beard)), detail(ear), dot(8.2, 9.2, 1), mark(ellipse(4.2, 13, 0.75, 0.9))]


@icon("angora-goat", CAT, "Angora goat in side view covered in long curly ringlets of mohair with backward curved horns",
      tags=["goat", "mohair", "curly fleece", "wool", "fibre", "livestock"])
def _(S):
    k = L(S, 0.4, 1.2)
    cs = [(9.6, 10, 3), (13, 8.2, 3), (16.6, 9, 3), (19, 12, 2.6), (17, 15, 2.8), (12.6, 15.6, 3), (9, 14, 2.8), (12.8, 11.6, 3.2)]
    cloud = union(*[circle(x, y, r) for x, y, r in cs], rect(9.6, 14.6, 2.8, 6.2, k), rect(16.2, 14.6, 2.8, 6.2, k))
    head = union(circle(5.6, 8.8, 2.5), soft(S, [(4.6, 9), (2.6, 11.4), (5.4, 12.4), (7, 10.6)], k=0.8))
    return [shell(union(cloud, head)), line("M5.4 6.6C5 3.8 7.4 2.6 9.4 4"), dot(5.4, 8.4, 0.9)]


# =========================================================================== deer

@icon("moose", CAT, "Moose head with wide flat palm-shaped antlers, a long drooping nose and a dewlap bell",
      tags=["elk", "antlers", "palmate antlers", "canada", "wildlife", "north america"])
def _(S):
    k = L(S, 0, 1.6)
    face = soft(S, [(9.4, 8), (14.6, 8), (15, 13), (15.8, 17.4), (14, 19.6), (10, 19.6), (8.2, 17.4), (9, 13)], k=k)
    pal = [(9.2, 9.6), (3.4, 10.2), (2.6, 6.4), (4.6, 7.4), (5.2, 3.8), (7.2, 5.6), (8.6, 2.8), (10, 6.2)]
    pal_l = soft(S, pal, k=L(S, 0, 0.8))
    pal_r = soft(S, mp(pal), k=L(S, 0, 0.8))
    return [shell(union(face, pal_l, pal_r)), dot(10.6, 12, 0.95), dot(13.4, 12, 0.95),
            mark(circle(11, 17.4, 0.7)), mark(circle(13, 17.4, 0.7)), line(seg(12, 19.6, 12, 21)), dot(12, 21, 1.2)]


@icon("musk-deer", CAT, "Musk deer head in profile with no antlers and a long thin fang hanging from the upper jaw",
      tags=["deer", "fangs", "tusks", "musk", "himalaya", "wildlife", "hornless"])
def _(S):
    head = ("M3.4 13.6C3.4 12.6 4.2 11.8 5.6 11.2L10 7.8C12.6 7.2 14.6 8 15.6 10L17.8 21L11.6 21L11.4 16.8C9 17.4 5.8 17.4 4.6 16.2C3.8 15.6 3.4 14.8 3.4 13.6Z")
    ear = ellipse(15.6, 6.2, 2.1, 4.2)
    ear = path_to_d(transform_path(P(ear), rotation(28, 15.6, 6.2)))
    return [shell(union(head, ear)), line(seg(6.2, 16.4, 5.6, 20.8)), dot(9.6, 11.6, 1), mark(ellipse(4.3, 13, 0.8, 0.8))]


@icon("fallow-deer", CAT, "Fallow deer in side view with a spotted coat and broad flat palmate antlers",
      tags=["deer", "spotted deer", "antlers", "palmate antlers", "park", "wildlife"])
def _(S):
    body = union(ellipse(14.4, 13, 6.4, 3.4), circle(6.4, 9.6, 2.1), soft(S, [(5.4, 9.6), (3, 11.6), (5.6, 12.6), (7.4, 11)], k=0.8),
                 thick(seg(7.6, 10.4, 10.6, 12.4), 3.2, S))
    pal = soft(S, [(6.6, 7.6), (5.2, 4.4), (7.6, 5.6), (8.6, 2.6), (10.6, 5.2), (13.4, 3.6), (12.2, 8)], k=L(S, 0, 0.8))
    return [shell(union(body, pal)), dot(6, 9.2, 0.8), *stride(10.6, 14.6, 21), *stride(18, 15, 21),
            *[dot(x, y, 0.75) for x, y in ((12.6, 11.6), (15.4, 11), (18, 12), (14, 14))]]


# =========================================================================== tracks and marks

@icon("hoof-print", CAT, "Pair of cloven hoof prints side by side, two teardrop halves with a gap between them",
      tags=["track", "footprint", "cloven hoof", "deer track", "hoofprint", "animal tracks"])
def _(S):
    r = L(S, 0, 2.2)
    left = "M10.4 3.8C8 7.4 4.2 10.8 4.2 15.4C4.2 18.8 6.8 20.6 10.4 20.4L10.4 3.8Z"
    if S.name == "rounded":
        left = "M10.2 4.2C8 8 4.4 10.8 4.4 15.4C4.4 18.6 6.8 20.2 10.2 20C10.6 20 10.8 19.8 10.8 19.4L10.8 5C10.8 4.4 10.6 4.1 10.2 4.2Z"
    return [shell(left), shell(flip(left))]


@icon("bear-track", CAT, "Bear footprint with a wide kidney-shaped pad and five toe pads topped by claw marks",
      tags=["paw print", "bear paw", "footprint", "claws", "animal tracks", "hiking"])
def _(S):
    pad = soft(S, [(5, 16), (8.5, 14.6), (15.5, 14.6), (19, 16), (19.4, 19), (15, 21), (9, 21), (4.6, 19)], k=3)
    xs = (3.9, 7.95, 12, 16.05, 20.1)
    ys = (11.6, 9.8, 9.2, 9.8, 11.6)
    out = [shell(pad)]
    for x, y in zip(xs, ys):
        out.append(dot(x, y, 1.6))
        out.append(solid(poly([(x - 1.2, y - 1.6), (x + 1.2, y - 1.6), (x, y - 4.6)], closed=True)))
    return out


@icon("claw-marks", CAT, "Three parallel curved scratch marks slashed diagonally, as left by an animal claw",
      tags=["scratch", "scratches", "slash", "claw", "scar", "wild animal", "damage"])
def _(S):
    return [line("M8.6 3C10.2 8.4 9 15 5 21"), line("M13.6 3C15.2 8.4 14 15 10 21"), line("M18.6 3C20.2 8.4 19 15 15 21")]


# =========================================================================== ice age and prehistoric mammals

def leg(S, x, top, w=3.2, bottom=21):
    return rect(x, top, w, bottom - top, L(S, 0.5, 1.5))


def tube(ctrl, width, n=20):
    """Closed outline around a cubic centreline whose width varies with t (width(t) -> px)."""
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x, y = bez(*ctrl, t)
        x2, y2 = bez(*ctrl, min(1, t + 1e-3))
        x1, y1 = bez(*ctrl, max(0, t - 1e-3))
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy)
        w = width(t) / 2
        left.append((x - dy / ln * w, y + dx / ln * w))
        right.append((x + dy / ln * w, y - dx / ln * w))
    return poly(left + right[::-1], closed=True, r=0)


def skirt(S, x0, x1, y0, y1, n=3):
    """Zigzag fringe of long hair hanging from a belly between two legs."""
    step = (x1 - x0) / (n * 2)
    pts = [(x0, y0)]
    for i in range(n * 2):
        pts.append((x0 + step * (i + 0.5), y1 if i % 2 == 0 else y1 - 2.2))
    pts.append((x1, y0))
    return poly(pts, closed=True, r=L(S, 0, 0.5))


@icon("woolly-mammoth", CAT, "Woolly mammoth in side view with a high domed head, a sloping back, shaggy hair and long curved tusks",
      tags=["mammoth", "ice age", "tusks", "extinct", "prehistoric", "proboscidean", "woolly"])
def _(S):
    back = poly([(9, 3.8), (14, 5.6), (19.6, 10.4), (21.2, 16.2), (11, 16.2)], closed=True, r=L(S, 0, 3))
    body = union(circle(8.6, 8.4, 5), back, leg(S, 9.6, 14, 3.2), leg(S, 18, 14, 3.2), thick("M5.4 11.4C5 13.4 5.4 15.4 5.8 16.4", 2.8, S))
    return [shell(body), line("M8.6 13.8C9.2 19.4 5.2 21 2.8 16.6"), dot(6.4, 8, 1)]


@icon("woolly-rhinoceros", CAT, "Woolly rhinoceros in side view with a shaggy coat and a very long curved front horn",
      tags=["rhino", "ice age", "horn", "extinct", "prehistoric", "woolly"])
def _(S):
    k = L(S, 0, 1.4)
    body = rect(9, 7.6, 12.6, 9.4, L(S, 3.5, 4.5))
    head = poly([(3.8, 15), (4.2, 12.4), (9, 9), (11, 9.6), (11, 16), (5, 16.6)], closed=True, r=k)
    horn = tube(((4.4, 12.4), (2.4, 10.6), (2.6, 6.4), (5.2, 3)), lambda t: 3.2 - 2.4 * t)
    hump = circle(12, 8.2, 2.8)
    ear = poly([(9.8, 8.6), (10.4, 5.8), (12.2, 8.2)], closed=True, r=L(S, 0, 0.8))
    return [shell(union(body, head, horn, hump, ear, leg(S, 10, 14, 3.2), leg(S, 18.4, 14, 3.2), skirt(S, 13.6, 18.2, 15.6, 19.6, 1))),
            dot(7.6, 12.2, 0.95)]


@icon("glyptodon", CAT, "Glyptodon in side view with a large domed patterned shell like a giant armadillo and a spiked tail",
      tags=["armadillo", "ice age", "armored", "shell", "extinct", "prehistoric"])
def _(S):
    dome = "M4.4 17C4.4 9.6 8.4 5.8 12.2 5.8C16.2 5.8 19 9.8 19 17Z"
    lower = union(ellipse(3.6, 15.6, 2.2, 2), leg(S, 6.4, 16, 2.8), leg(S, 14.4, 16, 2.8))
    dots = [dot(x, y, 1.1) for x, y in ((9.6, 9.6), (14, 9.6), (7.6, 12.8), (11.8, 12.8), (16, 12.8))]
    return [shell(union(dome, lower)), *dots, dot(10, 15.4, 0.001) if False else dot(13.6, 15.2, 0.9), dot(8.6, 15.2, 0.9),
            line("M19 15.4C20.8 15.8 21.6 17.2 21.4 18.8"), mark(circle(21.4, 19.8, 1.5)), dot(3.6, 15.4, 0.8)]


def fan(cx, cy, r_out, r_in, a0, a1, n):
    """Serrated fan (a palmate antler): n tines between angles a0 and a1, valleys between them."""
    pts = [(cx, cy)]
    for i in range(n):
        a = a0 + (a1 - a0) * i / (n - 1)
        pts.append(pt((cx, cy), r_out, a))
        if i < n - 1:
            pts.append(pt((cx, cy), r_in, a + (a1 - a0) / (n - 1) / 2))
    return pts


@icon("irish-elk", CAT, "Irish elk in side view with gigantic wide flat antlers spanning wider than its body",
      tags=["giant deer", "megaloceros", "antlers", "ice age", "extinct", "prehistoric"])
def _(S):
    body = union(ellipse(14.6, 15.8, 6.2, 3), circle(6.6, 12.6, 1.9), soft(S, [(5.6, 12.6), (3.6, 14.2), (5.8, 15), (7.4, 13.6)], k=0.7),
                 thick(seg(8, 13.2, 10.6, 15), 2.8, S))
    pal = poly(fan(8.6, 11.8, 10.4, 8.4, 232, 338, 5), closed=True, r=L(S, 0, 0.5))
    return [shell(union(body, pal)), dot(6.2, 12, 0.8), *stride(11, 16.4, 21), *stride(17.8, 16.8, 21)]


@icon("deinotherium", CAT, "Deinotherium in side view, an elephant-like animal with tusks curving down and back from the lower jaw",
      tags=["elephant", "tusks", "hooked tusks", "miocene", "extinct", "prehistoric"])
def _(S):
    body = union(rect(8.2, 5.8, 13.4, 11.4, L(S, 3.5, 5)), circle(7.6, 9, 4.4), leg(S, 9, 14, 3.4), leg(S, 17.6, 14, 3.4),
                 thick("M5.6 11.8C5 13.6 5.2 15.6 5.8 16.8", 3, S))
    tusk = "M4.4 13.8C2.4 16.6 3.4 20 7.2 19.6"
    return [shell(body), line(tusk), dot(6, 8.4, 1.1), detail("M9.8 7.2C11.6 8 11.8 10.4 11 11.6")]


@icon("platybelodon", CAT, "Platybelodon head with a long flat shovel-like lower jaw tipped with wide flat tusks",
      tags=["shovel tusker", "elephant", "tusks", "miocene", "extinct", "prehistoric"])
def _(S):
    k = L(S, 0.4, 1.4)
    head = union(circle(16, 8.2, 4.8), rect(15, 9.2, 6.8, 11.8, k), thick("M12.6 9.4C11 10.2 10 11.4 9.6 12.6", 2.8, S))
    shovel = union(rect(2.4, 15.2, 11.8, 3.6, L(S, 0.6, 1.8)), rect(2.4, 13.4, 3.8, 7.2, L(S, 0.6, 1.8)))
    return [shell(head), shell(shovel), dot(15, 7.6, 1.1), detail("M17 5.8C19.4 6.4 19.8 9 18.8 10.8")]


@icon("paraceratherium", CAT, "Paraceratherium in side view, a giant hornless rhino relative with a long neck and long legs",
      tags=["indricotherium", "baluchitherium", "giant rhino", "hornless", "extinct", "prehistoric"])
def _(S):
    body = union(rect(10, 9.8, 11.4, 6, L(S, 2.4, 3)), leg(S, 10.4, 14, 3.2), leg(S, 18, 14, 3.2),
                 thick("M11.6 11.2L7 6.4", 3.8, S),
                 soft(S, [(2.4, 7.4), (3.4, 4), (7.6, 3.6), (9.4, 6), (8.2, 8.6), (4, 8.8)], k=1))
    return [shell(body), line("M21.4 11C22 13 22 15.4 21.2 17"), dot(6, 5.8, 0.9), mark(ellipse(3, 7.4, 0.7, 0.7))]


@icon("macrauchenia", CAT, "Macrauchenia in side view with a camel-like long neck and body and a short trunk on its snout",
      tags=["litoptern", "long neck", "south america", "ice age", "extinct", "prehistoric"])
def _(S):
    body = union(ellipse(15.4, 12.4, 5.6, 3.4), thick("M11.6 11.6C8.6 10.8 7.4 8 6.6 5", 2.4, S),
                 ellipse(5.2, 4.6, 2.2, 1.7), thick("M3.4 5.2C2.6 6.2 2.6 7.6 3.4 8.4", 1.8, S))
    return [shell(body), *stride(12.2, 14.4, 21, 0.6), *stride(18.6, 14.6, 21, 0.6), line("M20.8 11.6C21.8 13 21.8 15 21.2 16.4"),
            dot(5.6, 4.2, 0.8)]


@icon("basilosaurus", CAT, "Basilosaurus, an early whale, in side view with a very long serpent-like body and toothy jaws",
      tags=["ancient whale", "archaeocete", "zeuglodon", "eocene", "extinct", "prehistoric", "sea monster"])
def _(S):
    head = poly([(2.4, 9.6), (9.2, 5.8), (10.6, 11.8), (3.6, 11.4)], closed=True, r=L(S, 0, 1))
    teeth = [line(seg(4.6, 11.4, 4.6, 13.2)), line(seg(7.6, 11.8, 7.6, 13.6))]
    return [shell(head), *teeth, dot(8.2, 8, 0.75),
            line("M10.6 10.6C12 14.4 14 14.4 15.6 10.6C17 7.6 18.8 7.6 20.6 11"), line(seg(20.6, 11, 22.2, 8.4)), line(seg(20.6, 11, 22.4, 13.6)),
            line(seg(12, 13.4, 11, 16.6))]


@icon("entelodont", CAT, "Entelodont in side view, a hog-like animal with a huge long head, bony jaw knobs and long legs",
      tags=["hell pig", "terminator pig", "giant pig", "hog", "extinct", "prehistoric"])
def _(S):
    k = L(S, 0, 1.4)
    head = poly([(2.4, 11.4), (3.2, 8), (9.4, 7.6), (11.2, 10.6), (10.2, 14.4), (3.6, 14.6)], closed=True, r=k)
    body = union(rect(9.8, 8.2, 11.6, 6.4, L(S, 2.4, 3.4)), head, circle(9, 13.6, 1.3), circle(6, 15.2, 1.2),
                 poly([(9.6, 8), (10.4, 5.4), (12, 8)], closed=True, r=L(S, 0, 0.6)))
    return [shell(body), dot(7.6, 10.2, 0.9), *stride(12.4, 14, 21, 0.5), *stride(18.8, 14, 21, 0.5),
            line("M21.4 9.6C22.4 11 22.2 12.4 21.6 13")]


@icon("sivatherium", CAT, "Sivatherium head in profile, a stocky giraffe relative with broad palmate ossicones like moose antlers",
      tags=["giraffe", "ossicones", "palmate horns", "extinct", "prehistoric", "ice age"])
def _(S):
    head = soft(S, [(2.6, 14.6), (3.6, 12), (9.6, 10), (14.2, 10.4), (15, 14.8), (12.2, 18.2), (5, 17)], k=1.2)
    neck = soft(S, [(11.2, 16.4), (14.4, 10.6), (21, 21), (12, 21)], k=1)
    pal = soft(S, [(9.6, 10.6), (7.4, 7), (9.8, 7.4), (10.6, 3.8), (12.8, 6.6), (15.4, 4.2), (15.8, 7.8), (18.6, 7.4), (15.2, 10.8)], k=L(S, 0, 0.7))
    return [shell(union(head, neck, pal)), dot(8.2, 13, 0.95), mark(ellipse(3.6, 14, 0.75, 0.8))]


@icon("cattle-skull", CAT, "Front view cattle skull with a long face, empty eye sockets and wide curved horns",
      tags=["bull skull", "cow skull", "desert", "western", "bones", "southwest", "horns"])
def _(S):
    k = L(S, 0, 2)
    skull = soft(S, [(8, 6.6), (16, 6.6), (15.6, 11.4), (14.8, 20), (9.2, 20), (8.4, 11.4)], k=k)
    horn = "M8.4 8C4.4 8.6 2.6 6.4 3 2.8"
    return [shell(skull), line(horn), line(flip(horn)), dot(10, 11.4, 1.5), dot(14, 11.4, 1.5),
            mark(circle(11, 17.4, 0.7)), mark(circle(13, 17.4, 0.7))]


@icon("quagga", CAT, "Quagga, the extinct zebra, in side view with stripes only on the head, neck and shoulders and a plain rear body",
      tags=["zebra", "horse", "extinct", "south africa", "stripes", "half striped"])
def _(S):
    body = union(ellipse(14.6, 13.4, 6.4, 3.4), thick("M9.8 11.6L7.2 7", 4, S), rot(ellipse(5, 8.2, 3.4, 1.8), 40, 5, 8.2),
                 poly([(7.8, 6), (8.8, 4), (10.2, 6.6)], closed=True, r=L(S, 0, 0.5)))
    st = [detail("M7.6 8.4L9.6 10.4"), detail("M10.6 11.2L11.6 15")]
    return [shell(body), *st, dot(4.6, 7.8, 0.75), *stride(11, 15.2, 21, 0.6), *stride(18.4, 15.4, 21, 0.6),
            line("M20.8 11.6C22 13.2 22 15.8 21.2 18.2")]


@icon("arsinoitherium", CAT, "Arsinoitherium head in profile, a prehistoric rhino-like animal with two huge conical horns side by side on the nose",
      tags=["rhino", "horns", "egypt", "eocene", "extinct", "prehistoric"])
def _(S):
    r = L(S, 0, 1.2)
    head = soft(S, [(2.4, 19), (2.8, 15.6), (10, 14.4), (16, 15.4), (17.4, 20.8), (8.6, 20.8)], k=1.4)
    neck = soft(S, [(12, 15.6), (17, 14.6), (21.6, 21), (12.4, 21)], k=1)
    h1 = poly([(3.8, 15.8), (5.6, 3.8), (9, 14.6)], closed=True, r=r)
    h2 = poly([(9.4, 14.8), (12, 5.4), (14.8, 15)], closed=True, r=r)
    return [shell(union(head, neck, h1, h2)), detail("M4 15H9"), detail("M9.6 15H14.6"), dot(7, 18, 0.9)]


@icon("uintatherium", CAT, "Uintatherium in side view with three pairs of knobby bony horns on the skull and long saber upper fangs",
      tags=["dinoceras", "horned mammal", "fangs", "eocene", "extinct", "prehistoric"])
def _(S):
    r = L(S, 0, 0.8)
    head = poly([(2.6, 14.4), (3.6, 11.6), (9, 9.8), (11.6, 10.4), (11.6, 16), (4.4, 16.4)], closed=True, r=L(S, 0, 1.4))
    knobs = [poly([(3.6, 11.8), (4.4, 8.4), (6, 10.6)], closed=True, r=r), poly([(6.2, 10.6), (7.4, 6.4), (9, 9.8)], closed=True, r=r),
             poly([(9.2, 10), (10.8, 7.2), (12, 10.6)], closed=True, r=r)]
    body = union(rect(9.6, 8.6, 12, 8.6, L(S, 3, 4)), head, *knobs, leg(S, 10.4, 14, 3.2), leg(S, 18.2, 14, 3.2))
    return [shell(body), line("M4.6 16.4L4.2 20.6"), dot(8.2, 12.6, 0.9)]


@icon("gomphotherium", CAT, "Gomphotherium in side view, an early elephant relative with two tusks on the upper jaw and two on the long lower jaw",
      tags=["elephant", "tusks", "four tusks", "miocene", "extinct", "prehistoric", "proboscidean"])
def _(S):
    body = union(rect(9, 6, 12.6, 11, L(S, 3.5, 5)), circle(8.4, 9, 4.4), leg(S, 10, 14, 3.4), leg(S, 17.8, 14, 3.4),
                 thick("M5.4 10.6C3.8 10.6 2.8 9.2 3.2 7.4", 2.6, S))
    upper = "M6.8 13C4.4 13.6 3.4 15.4 3.6 17.8"
    lower = "M8.6 15.4L3.8 19.8"
    return [shell(body), line(upper), line(lower), dot(7, 8.4, 1.1)]
