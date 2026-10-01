"""TypeIcon Core: mammals (batch 001). Primates, wild and domestic cats, wild dogs and a few dog breeds.

Faces are drawn in front view; whole animals in side view facing left (head on the left), matching sets/animals.py.
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


# =========================================================================== apes and monkeys

@icon("gorilla", CAT, "Gorilla head and broad shoulders in front view", tags=["ape", "primate", "silverback", "jungle", "wildlife"])
def _(S):
    head = "M12 2.6C14.6 3.4 16.8 6 16.8 9.8C16.8 13.6 14.6 16.2 12 16.2C9.4 16.2 7.2 13.6 7.2 9.8C7.2 6 9.4 3.4 12 2.6Z"
    if S.name == "line":
        head = "M12 2.4L14.6 4.2C16 5.4 16.8 7.4 16.8 9.8C16.8 13.6 14.6 16.2 12 16.2C9.4 16.2 7.2 13.6 7.2 9.8C7.2 7.4 8 5.4 9.4 4.2Z"
    body = soft(S, [(2.5, 21), (3, 16.5), (5.5, 13.8), (18.5, 13.8), (21, 16.5), (21.5, 21)], k=2.5)
    return [shell(union(head, body)), detail("M8.2 9.4Q12 7.4 15.8 9.4"), dot(10.2, 11.2, 1), dot(13.8, 11.2, 1),
            mark(ellipse(12, 13.6, 1.9, 1)), detail(seg(7, 17.5, 7, 21)), detail(seg(17, 17.5, 17, 21))]


@icon("orangutan", CAT, "Orangutan face with wide flat cheek pads", tags=["ape", "primate", "borneo", "rainforest", "wildlife"])
def _(S):
    pads = rect(2.5, 4, 19, 11.5, L(S, 4, 5.75))
    body = soft(S, [(4, 21), (5, 14), (19, 14), (20, 21)], k=2)
    return [shell(union(pads, body)), detail(ellipse(12, 10.2, 3.6, 4.4)), dot(10.7, 8.9, 0.95), dot(13.3, 8.9, 0.95),
            detail(L(S, "M10.6 12.4L13.4 12.4", "M10.6 12.2Q12 13.2 13.4 12.2")), detail(seg(8, 17, 8.6, 21)), detail(seg(16, 17, 15.4, 21))]


@icon("gibbon", CAT, "Gibbon hanging from a branch by its long arms", tags=["ape", "primate", "swing", "hanging", "rainforest"])
def _(S):
    body = union(circle(12, 9.6, 2.4), ellipse(12, 15, 2.8, 3.8))
    return [line(seg(2, 3, 22, 3)), line(poly([(10.2, 12.4), (7.2, 8), (5, 3)], r=S.r)), line(poly([(13.8, 12.4), (16.8, 8), (19, 3)], r=S.r)),
            shell(body), line(poly([(10.6, 18), (9.4, 21), (7.6, 21)], r=S.r)), line(poly([(13.4, 18), (14.6, 21), (16.4, 21)], r=S.r))]


@icon("siamang", CAT, "Siamang head with a large inflated throat sac", tags=["gibbon", "ape", "primate", "throat pouch", "call"])
def _(S):
    head = union(ellipse(12, 8, 5.2, 5), circle(6.6, 8.4, 1.5), circle(17.4, 8.4, 1.5))
    sac = circle(12, 16.3, 5)
    return [shell(union(head, sac)), detail(arc(12, 8, 5.2, 25, 155) if S.name == "rounded" else "M7.3 10.2L9 12.6L15 12.6L16.7 10.2"),
            detail("M8.6 6.8Q12 5 15.4 6.8"), dot(10.2, 8.4, 0.95), dot(13.8, 8.4, 0.95), dot(11.2, 10.8, 0.7), dot(12.8, 10.8, 0.7)]


@icon("baboon", CAT, "Baboon walking on all fours with a long muzzle and arched tail", tags=["monkey", "primate", "savanna", "africa", "wildlife"])
def _(S):
    r = L(S, 0, 1)
    body = rot(ellipse(12.5, 11.8, 6, 3.2), -6, 12.5, 11.8)
    head = union(circle(6.2, 8.8, 2.8), soft(S, [(5, 7.4), (1.8, 9.6), (2.2, 11.4), (5.6, 11.4)], k=0.8))
    return [shell(union(body, head)), line("M18.3 10.6C18.6 6.4 21.4 6 21.8 10.4"), dot(6.3, 8.2, 0.9),
            line(seg(8.5, 13.5, 7.8, 21)), line(seg(11.5, 14.6, 11.5, 21)), line(seg(15, 14.8, 15.5, 21)), line(seg(17.6, 13.8, 18.5, 21))]


@icon("mandrill", CAT, "Mandrill face with a long ridged nose and a pointed beard", tags=["monkey", "primate", "colourful", "rainforest", "wildlife"])
def _(S):
    r = L(S, 0, 1.4)
    face = union(ellipse(12, 6.8, 7.4, 4.4), "M6.6 7.6C6.6 12 7.2 15.4 8.4 17.4L10.2 18.2" + tip((10.2, 18.2), (12, 21.8), (13.8, 18.2), r)
                 + "L13.8 18.2L15.6 17.4C16.8 15.4 17.4 12 17.4 7.6Z")
    return [shell(face), detail(seg(12, 8, 12, 14.6)), detail("M9.3 9.2C8.9 11.6 9.1 13.8 9.9 15.8"), detail(flip("M9.3 9.2C8.9 11.6 9.1 13.8 9.9 15.8")),
            mark(ellipse(12, 16.4, 2, 1.1)), dot(9.4, 6.4, 1), dot(14.6, 6.4, 1)]


@icon("ring-tailed-lemur", CAT, "Sitting lemur with a tall ringed tail", tags=["lemur", "madagascar", "primate", "striped tail", "wildlife"])
def _(S):
    r = L(S, 0, 0.8)
    head = union(circle(7.2, 8, 2.8), soft(S, [(5.4, 6.8), (2.6, 8.8), (2.8, 10.2), (5.8, 10.4)], k=0.6),
                 soft(S, [(6.6, 5.6), (7.2, 3.4), (8.8, 5.6)], k=0.5))
    body = union(ellipse(9, 15.2, 3.8, 5), rect(6, 19, 7, 2, L(S, 0, 1)))
    c = ((12, 19.4), (18.8, 19.2), (17.2, 10), (18.6, 3))
    tail = thick(cub(c), 3.2, S)
    return [shell(union(head, body)), shell(minus(tail, grow(body, 2.4))), dot(6.6, 7.6, 0.9),
            *[detail(across(c, t, 1.7)) for t in (0.42, 0.62, 0.82)]]


@icon("aye-aye", CAT, "Aye-aye with huge eyes, big ears and one long thin finger", tags=["lemur", "madagascar", "primate", "nocturnal", "finger"])
def _(S):
    ear_l = rot(ellipse(5.8, 6.2, 2.6, 4) if S.name == "rounded" else "M5.8 2.2C8.4 3.6 8.4 8.8 5.8 10.2C3.2 8.8 3.2 3.6 5.8 2.2Z", -35, 5.8, 6.2)
    ear_r = flip(ear_l)
    head = union(ellipse(12, 11, 5, 4.4), ear_l, ear_r)
    return [shell(head), detail(circle(9.9, 10.6, 1.4)), detail(circle(14.1, 10.6, 1.4)), dot(12, 13.4, 0.8),
            line(poly([(15, 21.5), (18.4, 17.6), (21.2, 11.5)], r=S.r))]


@icon("tarsier", CAT, "Tarsier clinging to a twig with enormous round eyes", tags=["primate", "nocturnal", "big eyes", "philippines", "wildlife"])
def _(S):
    head = union(circle(10, 8.6, 5.4), soft(S, [(5.6, 5.6), (5.4, 2.6), (7.8, 3.8)], k=0.6), soft(S, [(14.4, 5.6), (14.6, 2.6), (12.2, 3.8)], k=0.6))
    body = ellipse(11.4, 16.4, 3.2, 4)
    return [line(seg(19.5, 2, 19.5, 22)), shell(union(head, body)), dot(7.8, 8.6, 1.9), dot(12.2, 8.6, 1.9),
            line(poly([(13.6, 14), (17.8, 13.2), (18.5, 12)], r=S.r)), line(poly([(13.8, 19.2), (17.8, 19.6), (18.5, 21)], r=S.r))]


@icon("slow-loris", CAT, "Slow loris face with big eyes in dark rings and a pale nose stripe", tags=["loris", "primate", "nocturnal", "big eyes", "wildlife"])
def _(S):
    head = union(ellipse(12, 12.6, 8, 7.2), circle(5.6, 6.4, 1.6), circle(18.4, 6.4, 1.6))
    patch = "M8.8 16C6.8 16 5.8 14.4 5.8 12.6C5.8 10.2 7.4 7.4 9.6 5.8L10.8 6.4C10.6 8.6 11 10.6 11.2 12.8C11.4 14.6 10.6 16 8.8 16Z"
    if S.name == "rounded":
        patch = "M8.6 16C6.6 16 5.8 14.4 5.8 12.6C5.8 10.2 7.6 7.2 9.8 6C10.8 5.5 11 6.6 10.9 7.4C10.8 9.2 11.2 11 11.2 12.8C11.2 14.6 10.4 16 8.6 16Z"
    eye = circle(8.6, 12.6, 1.05)
    return [shell(head), mark(minus(patch, eye)), mark(minus(flip(patch), flip(eye))), _nose(S, 12, 17.2, 2, 1.2)]


@icon("galago", CAT, "Bushbaby perched on a branch with big ears, big eyes and a long tail", tags=["bushbaby", "bush baby", "primate", "nocturnal", "africa"])
def _(S):
    r = L(S, 0, 0.8)
    ear_l = rot(ellipse(6.6, 4.8, 1.6, 2.6) if S.name == "rounded" else "M6.6 2.2C8.4 3.2 8.4 6.4 6.6 7.4C4.8 6.4 4.8 3.2 6.6 2.2Z", -20, 6.6, 4.8)
    ear_r = rot(ellipse(11.4, 4.8, 1.6, 2.6) if S.name == "rounded" else "M11.4 2.2C13.2 3.2 13.2 6.4 11.4 7.4C9.6 6.4 9.6 3.2 11.4 2.2Z", 20, 11.4, 4.8)
    head = union(circle(9, 8.4, 3), ear_l, ear_r)
    body = ellipse(11, 13.8, 3.6, 3.4)
    c = ((13.8, 15), (17.5, 15.5), (19.5, 16.5), (20, 21.5))
    tail = union(thick(cub(c), 2, S), ellipse(20, 19.6, 1.9, 2.4))
    return [shell(union(head, body)), line(seg(2, 18.5, 16.5, 18.5)), shell(minus(tail, grow(seg(2, 18.5, 16.5, 18.5), 2.6), grow(body, 2.4))),
            dot(7.9, 8.6, 1.05), dot(10.4, 8.6, 1.05), line(seg(8.8, 16.2, 8.8, 17.5))]


@icon("sifaka", CAT, "Sifaka leaping sideways upright with its arms raised", tags=["lemur", "madagascar", "primate", "dancing", "leap"])
def _(S):
    body = union(circle(11, 5.2, 2.6), rot(ellipse(11.6, 11.6, 2.8, 4.4), 8, 11.6, 11.6))
    c = ((12.8, 15.5), (17, 18), (20.5, 15), (19.5, 10.5))
    return [shell(body), line(poly([(9.6, 9), (6.4, 6.2), (4.6, 2.6)], r=S.r)), line(poly([(13.2, 8.8), (16, 6.2), (16.8, 2.6)], r=S.r)),
            line(poly([(10.4, 15.4), (6.5, 17.2), (8.2, 21)], r=S.r)), line(poly([(12.4, 16), (11.6, 19), (13.8, 21)], r=S.r)),
            line(cub(c)), dot(10.2, 5, 0.85)]


@icon("proboscis-monkey", CAT, "Proboscis monkey head in profile with a long drooping nose", tags=["monkey", "primate", "long nose", "borneo", "wildlife"])
def _(S):
    nose = ("M10 7.6C6.8 7.4 4.6 10 4.6 13.4C4.6 15.6 5.8 17 7.4 16.8C9.2 16.6 10 15 9.8 13Z" if S.name == "rounded"
            else "M10 7.6C6.8 7.4 4.6 10 4.6 13.4L5.2 16.4L7.4 16.8C9.2 16.6 10 15 9.8 13Z")
    head = union(circle(14, 8.8, 5.4), ellipse(11.4, 15.2, 2.6, 2), nose,
                 soft(S, [(9, 21), (10.5, 16), (17, 13.4), (20.5, 16.5), (21, 21)], k=2.5))
    return [shell(head), detail("M9.8 12.6C10 14.8 9.4 16.2 7.8 16.8"), dot(12.4, 7.8, 1)]


@icon("howler-monkey", CAT, "Howler monkey face with a bearded jaw and an open calling mouth", tags=["monkey", "primate", "loud", "call", "rainforest"])
def _(S):
    r = L(S, 0, 1.2)
    head = union(circle(10.5, 8.8, 5.6), circle(4.8, 8.8, 1.6), circle(16.2, 8.8, 1.6),
                 "M5.6 10C5.4 14.5 7.4 18.8 10.5 21.5C13.6 18.8 15.6 14.5 15.4 10Z" if S.name == "rounded"
                 else poly([(5.6, 10), (6.2, 15.5), (10.5, 21.5), (14.8, 15.5), (15.4, 10)], closed=True))
    return [shell(head), detail(ellipse(10.5, 14.4, 1.8, 2.2)), dot(8.4, 8.4, 0.95), dot(12.6, 8.4, 0.95),
            line(arc(10.5, 13.6, 8.8, -40, 0) if S.name == "rounded" else poly([pt((10.5, 13.6), 8.8, -40), pt((10.5, 13.6), 8.8, -20), pt((10.5, 13.6), 8.8, 0)])),
            line(arc(10.5, 13.6, 11.5, -32, -4) if S.name == "rounded" else poly([pt((10.5, 13.6), 11.5, -32), pt((10.5, 13.6), 11.5, -18), pt((10.5, 13.6), 11.5, -4)]))]


@icon("spider-monkey", CAT, "Spider monkey hanging by its tail and one long arm", tags=["monkey", "primate", "prehensile tail", "rainforest", "swing"])
def _(S):
    body = union(circle(13, 8.6, 2.3), rot(ellipse(12.4, 13.2, 2.4, 3.6), -12, 12.4, 13.2))
    return [line(seg(2, 3.5, 22, 3.5)), shell(body), line(poly([(11, 10.8), (8.8, 7.5), (7, 3.5)], r=S.r)),
            line(poly([(10.6, 12.2), (7, 13.6), (3.5, 16.5)], r=S.r)), line("M14 15.6C19 16.5 19.8 10 19.2 3.5"),
            line(poly([(11.4, 16.4), (10, 19), (8.2, 21.5)], r=S.r)), line(poly([(13.6, 16.6), (14.6, 19), (16.2, 21.5)], r=S.r))]


def _mhead(S, cx=12, cy=12, r=6.8, ear=1.8):
    return union(circle(cx, cy, r), ellipse(cx - r - 0.2, cy + 0.5, ear, ear + 0.6), ellipse(cx + r + 0.2, cy + 0.5, ear, ear + 0.6))


def _mface(S, cx=12, ey=12.6, dx=2.6, mouth=True):
    parts = [dot(cx - dx, ey, 1), dot(cx + dx, ey, 1), dot(cx - 0.8, ey + 2.6, 0.7), dot(cx + 0.8, ey + 2.6, 0.7)]
    if mouth:
        parts.append(detail(L(S, f"M{cx - 2} {ey + 4.6}L{cx} {ey + 5.4}L{cx + 2} {ey + 4.6}", f"M{cx - 2} {ey + 4.4}Q{cx} {ey + 5.8} {cx + 2} {ey + 4.4}")))
    return parts


@icon("capuchin-monkey", CAT, "Capuchin monkey face with a dark cap of hair", tags=["monkey", "primate", "cap", "pet monkey", "rainforest"])
def _(S):
    cap = minus(circle(12, 12, 4.9), poly([(0, 24), (0, 8.2), (12, 10.4), (24, 8.2), (24, 24)], closed=True, r=L(S, 0, 1)))
    return [shell(_mhead(S, 12, 12, 7.2)), mark(cap), *_mface(S, 12, 12.8, 2.6)]


@icon("squirrel-monkey", CAT, "Squirrel monkey face with a dark muzzle and pale eye mask", tags=["monkey", "primate", "small monkey", "rainforest", "wildlife"])
def _(S):
    cap = minus(circle(12, 12, 4.9), poly([(0, 24), (0, 7), (12, 8.8), (24, 7), (24, 24)], closed=True))
    muzzle = ellipse(12, 16.2, 2.8, 2.2) if S.name == "rounded" else poly([(9.2, 14.6), (14.8, 14.6), (14, 17.6), (12, 18.4), (10, 17.6)], closed=True, r=0.3)
    return [shell(_mhead(S, 12, 12, 7.2)), mark(cap), mark(muzzle), detail(ellipse(9.2, 11.8, 1.7, 2)), detail(ellipse(14.8, 11.8, 1.7, 2)),
            dot(9.2, 11.8, 0.8), dot(14.8, 11.8, 0.8)]


@icon("marmoset", CAT, "Marmoset head with large white ear tufts fanning out", tags=["monkey", "primate", "tufts", "small monkey", "pet"])
def _(S):
    tufts = []
    for x0, sgn in ((6.4, -1), (17.6, 1)):
        for a in (-40, -5, 30):
            e = pt((x0, 10.5), 4.4, 180 + a if sgn < 0 else -a)
            tufts.append(line(seg(x0, 10.5, *e)))
    return [shell(circle(12, 12.5, 5.4)), *tufts, detail("M9.6 9.2Q12 7.6 14.4 9.2"), dot(10, 12.2, 1), dot(14, 12.2, 1), _nose(S, 12, 15, 1.8, 1.1)]


@icon("golden-lion-tamarin", CAT, "Golden lion tamarin face inside a full round mane", tags=["tamarin", "monkey", "primate", "mane", "brazil"])
def _(S):
    c = (12, 11.6)
    if S.name == "line":
        mane = poly([pt(c, 9.4 if i % 2 == 0 else 8, -90 + i * 360 / 16) for i in range(16)], closed=True)
    else:
        mane = union(circle(12, 11.6, 8), *[circle(*pt(c, 7.8, -90 + i * 45), 1.8) for i in range(8)])
    face = minus(ellipse(12, 12.4, 3.3, 4.3), circle(10.7, 11.4, 0.9), circle(13.3, 11.4, 0.9), ellipse(12, 14.6, 1, 0.7))
    return [shell(mane), mark(face)]


@icon("emperor-tamarin", CAT, "Emperor tamarin face with a long drooping white mustache", tags=["tamarin", "monkey", "primate", "mustache", "moustache"])
def _(S):
    c = ((11.4, 12.6), (7.6, 12.4), (4.6, 14.8), (4.4, 20.6))
    k = 12
    left = [bez(*c, i / k) for i in range(k + 1)]
    right = []
    for i in range(k + 1):
        t = i / k
        x, y = bez(*c, t)
        w = 2.6 * (1 - t) + 0.2
        right.append((x + w * 0.55, y + w * 0.85))
    must = poly(left + right[::-1], closed=True, r=L(S, 0, 0.4))
    head = _mhead(S, 12, 8.2, 5.4, 1.4)
    return [shell(head), shell(union(must, flip(must))), dot(10, 7.8, 1), dot(14, 7.8, 1), _nose(S, 12, 10.6, 1.8, 1)]


@icon("cotton-top-tamarin", CAT, "Cotton-top tamarin head with a tall swept-back crest", tags=["tamarin", "monkey", "primate", "crest", "colombia"])
def _(S):
    crest = soft(S, [(6.5, 11), (7.4, 6), (11, 3.4), (20.4, 3.4), (17, 5.8), (20.4, 7.4), (15.5, 9), (18.2, 11.2), (12.5, 11.5)], k=0.8)
    head = circle(9.2, 13.4, 4.4)
    body = soft(S, [(6, 21), (8, 18.4), (15, 17.2), (18.5, 21)], k=1.5)
    return [shell(minus(crest, grow(head, 2.4))), shell(union(head, body)), dot(7.6, 13, 1), mark(ellipse(5.9, 15, 0.8, 0.9))]


@icon("snow-monkey", CAT, "Snow monkey bathing in a steaming hot spring", tags=["japanese macaque", "macaque", "onsen", "hot spring", "japan"])
def _(S):
    head = minus(circle(9.5, 11.5, 5.5), rect(0, 16, 24, 8))
    return [shell(head), detail("M6.8 13.8C6.2 11 8 9.4 9.5 10.6C11 9.4 12.8 11 12.2 13.8"), dot(8.4, 12, 0.85), dot(10.6, 12, 0.85),
            line(L(S, "M2 18.5L4.5 17.5L7 18.5L9.5 17.5L12 18.5L14.5 17.5L17 18.5L19.5 17.5L22 18.5",
                   "M2 18.2C3.2 17.2 4.4 17.2 5.5 18.2C6.7 19.2 7.8 19.2 9 18.2C10.2 17.2 11.3 17.2 12.5 18.2C13.7 19.2 14.8 19.2 16 18.2C17.2 17.2 18.3 17.2 19.5 18.2C20.4 19 21.2 19 22 18.4")),
            line(seg(4, 21.5, 20, 21.5)),
            line("M17 12C16 10.5 18 9 17 7.5C16.4 6.6 16.6 5.6 17.2 4.8"), line("M20.5 12C19.5 10.5 21.5 9 20.5 7.5C19.9 6.6 20.1 5.6 20.7 4.8")]


@icon("celebes-crested-macaque", CAT, "Crested macaque face with a spiky crest and a long flat muzzle", tags=["macaque", "monkey", "primate", "sulawesi", "crest"])
def _(S):
    r = L(S, 0, 0.8)
    crest = soft(S, [(8, 8), (9.2, 3.6), (10.8, 5.6), (12, 3), (13.2, 5.6), (14.8, 3.6), (16, 8)], k=0.5)
    head = union(ellipse(12, 10.8, 6, 4.6), rect(8, 11, 8, 9.5, L(S, 2.5, 4)), crest)
    return [shell(head), detail("M7.6 11Q12 8 16.4 11"), dot(9.8, 12.2, 0.95), dot(14.2, 12.2, 0.95), dot(11, 17.2, 0.75), dot(13, 17.2, 0.75)]


@icon("gray-langur", CAT, "Seated gray langur with a long tail arching over its back", tags=["langur", "hanuman langur", "monkey", "primate", "india"])
def _(S):
    body = union(rot(ellipse(9.4, 14.2, 3.8, 5.2), 12, 9.4, 14.2), rect(5, 19, 8, 2, L(S, 0, 1)))
    head = union(circle(6.6, 7.4, 2.9), ellipse(4.4, 8.4, 1.4, 1.2))
    return [shell(minus(body, grow(head, 2.4))), shell(head), dot(6, 6.8, 0.9), line(cub(((12.4, 19), (22.5, 19.5), (23, 2.5), (13, 3))))]


@icon("night-monkey", CAT, "Night monkey face with two huge round eyes and pale brows", tags=["owl monkey", "douroucouli", "monkey", "primate", "nocturnal"])
def _(S):
    head = circle(12, 12, 8.4) if S.name == "rounded" else poly(regular(12, 12, 8.8, 12, -75), closed=True)
    return [shell(head), detail(circle(8.6, 11.6, 2.6)), detail(circle(15.4, 11.6, 2.6)), dot(8.6, 11.6, 1.1), dot(15.4, 11.6, 1.1),
            detail("M6.4 7.2Q8.6 6 10.8 7.2"), detail("M13.2 7.2Q15.4 6 17.6 7.2"), _nose(S, 12, 16, 2, 1.1)]


@icon("de-brazzas-monkey", CAT, "De Brazza monkey face with a dark brow band and a long white beard", tags=["de brazza", "monkey", "guenon", "primate", "beard"])
def _(S):
    r = L(S, 0, 1.5)
    beard = "M7.2 11.5L16.8 11.5L15" + " 17" + tip((15, 17), (12, 21.8), (9, 17), r) + "L9 17Z"
    head = union(_mhead(S, 12, 8.4, 5.6, 1.4), beard)
    band = minus(ellipse(12, 6.4, 4, 2.4), ellipse(12, 8.2, 4.4, 2.2))
    return [shell(head), mark(band), dot(10, 8.6, 0.95), dot(14, 8.6, 0.95), detail(ellipse(12, 12.4, 2.6, 1.8)), mark(ellipse(12, 11.4, 1, 0.6))]


# =========================================================================== wild cats


def _chead(S, hx, hy, hr=2.6, ear=2.2, muzzle=True):
    """Side-view cat head facing left, with one upright ear."""
    parts = [circle(hx, hy, hr), soft(S, [(hx - 0.6, hy - hr + 0.9), (hx + 0.3, hy - hr - ear + 0.5), (hx + 1.9, hy - hr + 1.3)], k=0.5)]
    if muzzle:
        parts.append(ellipse(hx - hr + 0.3, hy + 1, 1.4, 1.2))
    return union(*parts)


@icon("leopard", CAT, "Leopard walking in side view with a spotted coat and a long tail", tags=["big cat", "spots", "safari", "africa", "wildlife"])
def _(S):
    body = union(ellipse(13.8, 11.6, 6.8, 3.6), _chead(S, 5.4, 8.8), thick(seg(6.2, 9.6, 9, 11), 3.6, S))
    return [shell(body), dot(4.9, 8.4, 0.8), *stride(9.6, 13.8), *stride(17, 14.2),
            line("M20.5 10.6C22.6 12 22.9 16.2 21.8 19"),
            *[dot(x, y, 0.8) for x, y in ((11.2, 10.2), (14.4, 9.8), (17.6, 10.4), (12.8, 12.9), (16, 12.9))]]


@icon("cheetah", CAT, "Slim spotted cheetah running at full stride", tags=["big cat", "fast", "speed", "sprint", "safari"])
def _(S):
    body = union(rot(ellipse(12.6, 10.6, 6.4, 2.8), -4, 12.6, 10.6), _chead(S, 4.6, 8.2, 2.3, 1.8), thick(seg(5.4, 8.8, 8, 10), 3, S))
    return [shell(body), dot(4.1, 7.9, 0.75),
            line(poly([(8.4, 12.2), (5.4, 15), (2.4, 15.4)], r=S.r)), line(poly([(9.6, 12.6), (8, 16.4), (5.4, 18.4)], r=S.r)),
            line(poly([(15.8, 12.6), (19.4, 15.6), (21.6, 18.6)], r=S.r)), line(poly([(17.4, 11.8), (21.2, 12.6), (22, 15)], r=S.r)),
            line("M18.8 9C20.6 8 21.6 6.6 21.8 4.8"),
            *[dot(x, y, 0.7) for x, y in ((10.4, 10.6), (13, 10), (15.6, 10.4))]]


@icon("jaguar", CAT, "Jaguar head with a broad skull, short ears and rosettes", tags=["big cat", "rosettes", "amazon", "rainforest", "wildlife"])
def _(S):
    k = L(S, 0, 1.4)
    head = union(ellipse(12, 13.2, 8.8, 7.4), poly([(3.6, 9.4), (4.4, 4.2), (9, 6.8)], closed=True, r=k), poly([(20.4, 9.4), (19.6, 4.2), (15, 6.8)], closed=True, r=k))
    return [shell(head), detail(circle(12, 8.8, 1.3)), detail(circle(6.8, 15.6, 1.3)), detail(circle(17.2, 15.6, 1.3)),
            dot(9, 12, 1.1), dot(15, 12, 1.1), _nose(S, 12, 15.2, 2.6, 1.5), detail(L(S, "M10 17.8L12 18.8L14 17.8", "M10 17.6Q12 19.2 14 17.6"))]


@icon("snow-leopard", CAT, "Snow leopard lying down with a very thick tail curled forward", tags=["big cat", "mountain", "himalaya", "ounce", "wildlife"])
def _(S):
    body = union(ellipse(13, 15.8, 7, 3.4), _chead(S, 5.6, 11.8, 2.7), thick(seg(6.4, 12.6, 9, 14.4), 3.6, S),
                 rect(2.4, 17.8, 7, 2.4, L(S, 0.6, 1.2)))
    tail = thick("M19.6 14.4C22.6 12 22.2 6.6 18.4 5.4C15.6 4.6 13 6 12.4 8.4", 3.2, S)
    return [shell(body), shell(minus(tail, grow(body, 2.4))), dot(5.1, 11.4, 0.8),
            *[dot(x, y, 0.8) for x, y in ((11.6, 15.2), (14.8, 14.8), (17.6, 15.6), (13.2, 17.6))]]


@icon("cougar", CAT, "Cougar standing in side view with a plain coat and a long tail", tags=["puma", "mountain lion", "panther", "big cat", "wildlife"], aliases=["puma", "mountain-lion"])
def _(S):
    body = union(ellipse(13.6, 11.4, 6.6, 3.4), _chead(S, 5.4, 8.2, 2.4, 1.8), thick(seg(6.2, 9, 9, 10.8), 3.4, S))
    return [shell(body), dot(4.9, 7.8, 0.8), *stride(9.6, 13.6), *stride(16.8, 14),
            line("M20.2 10.4C22.4 11.6 22.8 15 22 17.6"), mark(circle(21.8, 18.6, 1.4))]


@icon("lynx", CAT, "Lynx head with tufted ears and a flared cheek ruff", tags=["bobcat", "wild cat", "ear tufts", "forest", "wildlife"])
def _(S):
    pts = [(9.4, 7.4), (6.4, 4.6), (5.4, 9.4), (3, 15.4), (6.4, 15.4), (5.6, 18.6), (9, 18), (12, 20.4), (15, 18), (18.4, 18.6),
           (17.6, 15.4), (21, 15.4), (18.6, 9.4), (17.6, 4.6), (14.6, 7.4)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 1))), line(seg(6.4, 4.6, 6, 2)), line(seg(17.6, 4.6, 18, 2)),
            dot(9.4, 11.6, 1.05), dot(14.6, 11.6, 1.05), _nose(S, 12, 14.4, 2.4, 1.3), detail(L(S, "M10.4 16.4L12 17.2L13.6 16.4", "M10.4 16.2Q12 17.6 13.6 16.2"))]


@icon("bobcat", CAT, "Bobcat standing with ear tufts, spots and a short bobbed tail", tags=["wild cat", "lynx", "short tail", "north america", "wildlife"])
def _(S):
    body = union(ellipse(13.6, 12, 6, 3.6), _chead(S, 6, 9, 2.8, 1.8), thick(seg(6.8, 9.8, 9.4, 11.4), 3.6, S))
    return [shell(body), line(seg(6.3, 5.4, 6.3, 3.4)), line(L(S, "M19.2 10.2L21.2 8.2", "M19.2 10.2Q20.6 9.6 21.2 8.2")), dot(5.5, 8.6, 0.8),
            *stride(10.2, 14.4), *stride(16.6, 14.6), *[dot(x, y, 0.75) for x, y in ((12.4, 10.8), (15.4, 10.4), (14, 13), (17, 12.6))]]


@icon("caracal", CAT, "Caracal head with very long pointed ears ending in tassels", tags=["desert lynx", "wild cat", "tassels", "africa", "wildlife"])
def _(S):
    r = L(S, 0, 1)
    head = union(ellipse(12, 15, 6.4, 5.8), soft(S, [(6.6, 12.2), (5.4, 5.4), (10.4, 10)], k=0.8), soft(S, [(17.4, 12.2), (18.6, 5.4), (13.6, 10)], k=0.8))
    return [shell(head), line(seg(5.4, 5.4, 4.8, 2.2)), line(seg(18.6, 5.4, 19.2, 2.2)), dot(9.6, 14.2, 1), dot(14.4, 14.2, 1),
            _nose(S, 12, 17, 2.2, 1.2)]


@icon("serval", CAT, "Serval standing on long thin legs with big oval ears", tags=["wild cat", "long legs", "africa", "savanna", "wildlife"])
def _(S):
    ear = "M6.6 2C7.8 2.6 8 5.2 7.4 6.6L5.4 6.6C5 4.8 5.4 2.6 6.6 2Z"
    if S.name == "rounded":
        ear = rot(ellipse(6.5, 4.4, 1.2, 2.5), 10, 6.5, 4.4)
    head = union(circle(5.6, 8.4, 2.5), ellipse(3.4, 9.4, 1.3, 1.1), ear)
    body = union(ellipse(13.8, 9.8, 5.8, 2.8), head, thick(seg(6.4, 9, 9, 9.8), 3.2, S))
    return [shell(body), dot(5.2, 8.2, 0.75), *stride(10.8, 11.6, 21, 0.8), *stride(16.8, 11.8, 21, 0.8), line("M19.4 8.8C21.2 9.6 21.8 11.6 21.4 13.8"),
            *[dot(x, y, 0.7) for x, y in ((12.4, 9.6), (15, 9.2), (17.4, 9.8))]]


@icon("ocelot", CAT, "Ocelot lying down with chain-like spots along its body", tags=["wild cat", "spots", "rainforest", "south america", "wildlife"])
def _(S):
    body = union(ellipse(13.4, 15.6, 7.2, 3.6), _chead(S, 5.4, 11.6, 2.7), thick(seg(6.2, 12.4, 9, 14.4), 3.6, S),
                 rect(2.4, 17.8, 7, 2.4, L(S, 0.6, 1.2)))
    k = 0.5 if S.name == "rounded" else 0.2
    chain = [rect(10.2, 14.4, 2.8, 1.4, 0.7 * k * 2), rect(14.2, 13.8, 2.8, 1.4, 0.7 * k * 2), rect(12.2, 16.6, 2.8, 1.4, 0.7 * k * 2), rect(16.2, 16.2, 2.8, 1.4, 0.7 * k * 2)]
    return [shell(body), dot(4.9, 11.2, 0.8), *[mark(c) for c in chain], line("M20.4 16.8C22 17.6 22.4 19.6 21.4 21.4")]


@icon("clouded-leopard", CAT, "Clouded leopard resting on a branch with a long thick tail", tags=["big cat", "tree", "asia", "rainforest", "wildlife"])
def _(S):
    body = union(ellipse(13, 11.4, 6.8, 3.2), _chead(S, 5, 10.2, 2.6))
    tail = thick("M19.4 11.8C21.4 13 21.4 16.4 20 20.6", 2.8, S)
    return [shell(union(body, tail)), line(seg(2, 15.6, 22, 15.6)), dot(4.5, 9.8, 0.8),
            line(seg(8.8, 14.4, 8.8, 20.4)), line(seg(15.6, 14.4, 15.6, 20.4)),
            mark(soft(S, [(9.6, 10.2), (12.4, 9.6), (13, 11.2), (11.6, 12.6), (9.4, 12)], k=0.6)),
            mark(soft(S, [(14.6, 9.8), (17.8, 9.8), (17.4, 12), (15, 12.4)], k=0.6))]


@icon("black-panther", CAT, "Sleek black panther prowling with its head held low", tags=["panther", "black leopard", "big cat", "jungle", "wildlife"])
def _(S):
    body = union(rot(ellipse(13.2, 9.8, 6.8, 3.2), 6, 13.2, 9.8), _chead(S, 4.6, 12.4, 2.5, 1.8), thick(seg(5.4, 11.6, 8.4, 10.4), 3.8, S))
    return [shell(body), mark(ellipse(4, 12, 0.8, 0.5) if S.name == "rounded" else poly([(3.2, 11.8), (4.8, 11.6), (4.4, 12.4)], closed=True)),
            line(poly([(8.6, 12.4), (8, 16.6), (6.4, 21)], r=S.r)), line(poly([(11.4, 13), (11.6, 17), (10.4, 21)], r=S.r)),
            *legs((15.6, 18.6), 13.4), line("M20 9.4C22.2 10.4 22.6 13.8 21.6 16.2")]


@icon("sand-cat", CAT, "Sand cat face with a wide flat head and very broad low ears", tags=["desert cat", "wild cat", "sahara", "small cat", "wildlife"])
def _(S):
    r = L(S, 0, 1.2)
    head = union(ellipse(12, 14.4, 8.8, 6), soft(S, [(3.8, 12), (2.2, 5.4), (9.6, 9.2)], k=1.4), soft(S, [(20.2, 12), (21.8, 5.4), (14.4, 9.2)], k=1.4))
    return [shell(head), detail(L(S, "M4.6 10.4L4 7.4L6.4 8.8", "M4.6 10.4Q4 8.6 4.2 7.6Q5.4 8 6.4 8.8")), detail(flip(L(S, "M4.6 10.4L4 7.4L6.4 8.8", "M4.6 10.4Q4 8.6 4.2 7.6Q5.4 8 6.4 8.8"))),
            dot(8.8, 13.4, 1.25), dot(15.2, 13.4, 1.25), _nose(S, 12, 16.2, 2.2, 1.2)]


@icon("pallas-cat", CAT, "Pallas cat face with a flat fluffy head and tiny low ears", tags=["manul", "wild cat", "fluffy", "grumpy", "mongolia"], aliases=["manul"])
def _(S):
    if S.name == "line":
        head = poly([(4, 10.4), (3.4, 7.6), (6.4, 7.4), (9, 6), (15, 6), (17.6, 7.4), (20.6, 7.6), (20, 10.4), (21.6, 13), (19.8, 14.4), (20.6, 17.4),
                     (17.4, 17.6), (16.4, 20), (12, 19.4), (7.6, 20), (6.6, 17.6), (3.4, 17.4), (4.2, 14.4), (2.4, 13)], closed=True)
    else:
        head = union(ellipse(12, 12.8, 8.6, 6.6), circle(4.6, 8.4, 1.5), circle(19.4, 8.4, 1.5), circle(3.8, 13.6, 1.6), circle(20.2, 13.6, 1.6),
                     circle(5.8, 17, 1.6), circle(18.2, 17, 1.6), circle(9, 18.8, 1.7), circle(15, 18.8, 1.7))
    return [shell(head), dot(8.8, 11.8, 1.3), dot(15.2, 11.8, 1.3), _nose(S, 12, 14.8, 2, 1.1),
            detail(L(S, "M10.2 16.8L12 17.6L13.8 16.8", "M10.2 16.6Q12 18 13.8 16.6"))]


@icon("jaguarundi", CAT, "Jaguarundi with a long low body, short legs and a small flat head", tags=["wild cat", "otter cat", "weasel cat", "americas", "wildlife"])
def _(S):
    body = union(ellipse(12.4, 13.6, 7.4, 2.9), ellipse(4.2, 12.6, 2.6, 2), soft(S, [(4.4, 10.8), (5.2, 9.4), (6.2, 11)], k=0.4),
                 thick(seg(5, 12.8, 7.6, 13.4), 3, S))
    return [shell(body), dot(3.8, 12.2, 0.75), *legs((7.8, 10.4, 14.6, 17.2), 15.8, 20), line("M19.6 13C21.4 13.6 22 15.6 21.6 18.6")]

# =========================================================================== domestic cats


@icon("saber-toothed-cat", CAT, "Prehistoric saber-toothed cat head in profile with two long fangs", tags=["sabertooth", "smilodon", "prehistoric", "ice age", "extinct"], aliases=["sabertooth"])
def _(S):
    ear = soft(S, [(13.4, 4.4), (15.4, 1.8), (17.2, 4.6)], k=0.6)
    head = union(circle(14.4, 9.4, 5.6), ellipse(7, 9.6, 4.6, 2.8), ear, soft(S, [(15, 13), (20, 11), (21.4, 21), (13.6, 21)], k=1.5))
    fang = "M4.6 11.4C5.4 14 5.8 16.8 5.8 20C7.2 17.4 7.6 14.4 7.6 11.6Z"
    if S.name == "rounded":
        fang = "M4.6 11.4C5.4 14 5.8 16.8 5.6 19.4C5.6 20.2 6.4 20.2 6.6 19.4C7.2 17 7.6 14.4 7.6 11.6Z"
    jaw = soft(S, [(8.6, 13), (12.6, 13.4), (11.6, 15.6), (9.2, 15)], k=0.6)
    return [shell(minus(head, grow(fang, 2.2))), shell(fang), shell(minus(jaw, grow(head, 1), grow(fang, 2.2))), dot(9.6, 7.8, 1), mark(ellipse(3.4, 8.2, 0.9, 0.7))]


@icon("sphynx-cat", CAT, "Hairless sphynx cat face with huge ears and a wrinkled forehead", tags=["hairless cat", "cat breed", "bald cat", "pet", "kitten"])
def _(S):
    r = L(S, 0, 1.6)
    d = ("M9.6 8.4Q12 7.8 14.4 8.4" + tip((14.4, 8.4), (20.2, 3.4), (18.2, 12.6), r) + "L18.2 12.6"
         "C18.6 17 15.6 20.6 12 20.6C8.4 20.6 5.4 17 5.8 12.6" + tip((5.8, 12.6), (3.8, 3.4), (9.6, 8.4), r) + "Z")
    eye = L(S, "M8 13.4L9.6 12.4L11 13.4L9.6 14.2Z", "M8 13.4Q9.6 11.8 11 13.4Q9.6 14.6 8 13.4Z")
    return [shell(d), detail(L(S, "M10 10.2L12 10.8L14 10.2", "M10 10.2Q12 11.2 14 10.2")), mark(eye), mark(flip(eye)), _nose(S, 12, 16.2, 1.8, 1)]


@icon("persian-cat", CAT, "Persian cat face with a flat nose, round head and a fluffy ruff", tags=["longhair", "cat breed", "fluffy cat", "pet", "flat face"])
def _(S):
    c = (12, 12.4)
    if S.name == "line":
        tufts = [poly([pt(c, 7, a - 14), pt(c, 9.4, a), pt(c, 7, a + 14)], closed=True) for a in (15, 50, 90, 130, 165)]
        ears = [poly([(4.8, 9.6), (5.6, 4.8), (9.4, 6)], closed=True), poly([(19.2, 9.6), (18.4, 4.8), (14.6, 6)], closed=True)]
    else:
        tufts = [circle(*pt(c, 7.4, a), 1.6) for a in (15, 50, 90, 130, 165)]
        ears = [circle(6.2, 6.8, 1.8), circle(17.8, 6.8, 1.8)]
    return [shell(union(circle(12, 12.4, 7.6), *tufts, *ears)), dot(9.2, 11.8, 1.3), dot(14.8, 11.8, 1.3), _nose(S, 12, 13.8, 1.6, 0.9),
            detail(L(S, "M10.4 16.6L12 15.8L13.6 16.6", "M10.4 16.6Q12 15.2 13.6 16.6"))]


@icon("maine-coon", CAT, "Maine coon cat head with tufted ears and a shaggy ruff", tags=["cat breed", "longhair", "big cat breed", "fluffy cat", "pet"])
def _(S):
    head = soft(S, [(9, 6.4), (6, 3.4), (5.2, 9), (6.2, 13.6), (9, 15), (15, 15), (17.8, 13.6), (18.8, 9), (18, 3.4), (15, 6.4)], k=1.4)
    if S.name == "line":
        ruff = poly([(4.8, 11), (2.6, 14.4), (4.6, 15), (3.6, 18.4), (6.6, 18.2), (7.4, 21.4), (10, 19.6), (12, 21.8), (14, 19.6), (16.6, 21.4),
                     (17.4, 18.2), (20.4, 18.4), (19.4, 15), (21.4, 14.4), (19.2, 11)], closed=True)
    else:
        ruff = union(ellipse(12, 16, 7.2, 4.6), *[circle(x, y, 1.6) for x, y in ((4.8, 14.6), (5.8, 18), (9, 20), (12, 20.6), (15, 20), (18.2, 18), (19.2, 14.6))])
    return [shell(minus(ruff, grow(head, 2.4))), shell(head), line(seg(6, 3.4, 5.6, 1.8)), line(seg(18, 3.4, 18.4, 1.8)),
            dot(9.6, 9.8, 1), dot(14.4, 9.8, 1), _nose(S, 12, 12.2, 1.8, 1)]


@icon("siamese-cat", CAT, "Siamese cat with a wedge-shaped head, dark mask and dark ears", tags=["cat breed", "colourpoint", "thai cat", "pet", "blue eyes"])
def _(S):
    r = L(S, 0, 1.4)
    d = ("M9.4 7.6Q12 7 14.6 7.6" + tip((14.6, 7.6), (19.8, 3), (19.2, 10.8), r) + "L19.2 10.8L14" + " 19.4"
         + tip((14, 19.4), (12, 20.8), (10, 19.4), r) + "L10 19.4L4.8 10.8" + tip((4.8, 10.8), (4.2, 3), (9.4, 7.6), r) + "Z")
    mask = soft(S, [(12, 10.6), (15.6, 12.2), (13.4, 17.6), (12, 18.4), (10.6, 17.6), (8.4, 12.2)], k=0.8)
    mask = minus(mask, ellipse(9.8, 12.8, 1, 0.7), ellipse(14.2, 12.8, 1, 0.7))
    ear = soft(S, [(6.2, 8.2), (6, 5.6), (8, 7.4)], k=0.3)
    return [shell(d), mark(mask), mark(ear), mark(flip(ear))]


@icon("scottish-fold", CAT, "Scottish fold cat face with small ears folded forward on a round head", tags=["cat breed", "folded ears", "owl cat", "pet", "round face"])
def _(S):
    ear = soft(S, [(5.6, 8.6), (7, 5), (10.2, 5.8), (8.2, 7.2)], k=1)
    return [shell(union(circle(12, 13.2, 7.6), ear, flip(ear))), dot(9, 12.8, 1.4), dot(15, 12.8, 1.4), _nose(S, 12, 15.6, 1.8, 1),
            detail(L(S, "M10.4 17.8L12 18.6L13.6 17.8", "M10.4 17.6Q12 19 13.6 17.6"))]


def _dhead(S, hx, hy, hr=3.2):
    """Side-view domestic cat head facing left with two ears."""
    e1 = soft(S, [(hx - 2.4, hy - hr + 1.4), (hx - 1.8, hy - hr - 1.8), (hx - 0.1, hy - hr + 0.4)], k=0.5)
    e2 = soft(S, [(hx + 0.4, hy - hr + 0.3), (hx + 1.6, hy - hr - 1.8), (hx + 2.5, hy - hr + 1.4)], k=0.5)
    return union(circle(hx, hy, hr), e1, e2)


@icon("munchkin-cat", CAT, "Munchkin cat standing on very short stubby legs", tags=["cat breed", "short legs", "sausage cat", "pet", "kitten"])
def _(S):
    body = union(ellipse(13.2, 14.4, 6.8, 3.4), _dhead(S, 6.2, 10.8), thick(seg(7, 12, 9.4, 13.4), 3.6, S))
    return [shell(body), dot(4.8, 10.6, 0.9), *legs((9.2, 11.8, 14.8, 17.4), 17, 20.6), line("M19.6 13C21.6 12 22 9 21.2 6")]


@icon("manx-cat", CAT, "Manx cat standing with a rounded rump and no tail", tags=["cat breed", "tailless cat", "isle of man", "pet", "stumpy"])
def _(S):
    body = union(ellipse(13.2, 11.8, 6.6, 3.8), circle(17.2, 11.4, 3.8), _dhead(S, 6, 8.8), thick(seg(6.8, 10, 9.4, 11.4), 3.6, S))
    return [shell(body), dot(4.6, 8.6, 0.9), *stride(9.6, 14.2), *stride(17, 14.6)]


@icon("devon-rex", CAT, "Devon rex cat face with oversized low-set ears and a small pointed chin", tags=["cat breed", "big ears", "pixie cat", "curly cat", "pet"])
def _(S):
    ear = rot(ellipse(5.6, 8.4, 2.9, 4.6) if S.name == "rounded" else "M5.6 3.8C8.6 5.4 8.6 11.4 5.6 13C2.6 11.4 2.6 5.4 5.6 3.8Z", -48, 5.6, 8.4)
    face = "M12 21C9.6 21 6.6 18 6.6 14.4C6.6 11 9 8.8 12 8.8C15 8.8 17.4 11 17.4 14.4C17.4 18 14.4 21 12 21Z"
    return [shell(union(face, ear, flip(ear))), dot(9.8, 13.8, 1.3), dot(14.2, 13.8, 1.3), _nose(S, 12, 17, 1.6, 0.9)]


@icon("british-shorthair", CAT, "British shorthair cat face with a very round head and chubby cheeks", tags=["cat breed", "british blue", "chubby cat", "round face", "pet"])
def _(S):
    ear = soft(S, [(4.4, 10.4), (5, 5), (9.6, 7.4)], k=1.6)
    head = union(ellipse(12, 12.4, 7.6, 6.2), ellipse(12, 15, 9, 5.4), ear, flip(ear))
    return [shell(head), dot(8.8, 12.4, 1.15), dot(15.2, 12.4, 1.15), _nose(S, 12, 15, 2, 1.1),
            detail(L(S, "M9.8 17.2L12 16.4L14.2 17.2", "M9.8 17.4C10.6 17.6 11.4 17.2 12 16.4C12.6 17.2 13.4 17.6 14.2 17.4"))]


@icon("bengal-cat", CAT, "Bengal cat sitting in side view with a spotted coat", tags=["cat breed", "spotted cat", "leopard cat", "pet", "rosettes"])
def _(S):
    body = union(ellipse(13.4, 15.4, 5, 5.6), rect(8.6, 18.8, 10, 2.2, L(S, 0.4, 1.1)))
    head = _dhead(S, 9.2, 7.8)
    return [shell(minus(body, grow(head, 2.4))), shell(head), dot(7.8, 7.6, 0.9), line("M18.4 20.2C20.8 20.6 21.8 19 21.4 16.6"),
            *[dot(x, y, 0.9) for x, y in ((13.6, 12.6), (16.2, 14.2), (11.6, 15.6), (14.4, 16.6))]]


@icon("american-curl", CAT, "American curl cat face with ears curling backward", tags=["cat breed", "curled ears", "pet", "kitten", "cute cat"])
def _(S):
    ear = "M6.2 9.4C5.8 6.6 5.2 4.6 3.2 3.6C5.6 2.4 8.8 3.6 10.6 6.8Z"
    if S.name == "rounded":
        ear = "M6.2 9.4C5.8 6.6 5.2 4.8 3.6 4C2.8 3.6 3 2.8 3.8 2.8C6.2 2.6 9 4 10.6 6.8Z"
    return [shell(union(circle(12, 13.4, 7.2), ear, flip(ear))), detail("M7.2 7.4C6.8 6.2 6.2 5.4 5.6 5"), detail(flip("M7.2 7.4C6.8 6.2 6.2 5.4 5.6 5")),
            dot(9.2, 12.8, 1.1), dot(14.8, 12.8, 1.1), _nose(S, 12, 15.4, 1.8, 1)]


@icon("black-cat", CAT, "Black cat with an arched back and an upright tail", tags=["halloween", "spooky", "superstition", "cat", "witch"])
def _(S):
    c = ((7.4, 21), (6.6, 6.4), (17.6, 6.4), (17.2, 21))
    k = 16
    left, right = [], []
    for i in range(k + 1):
        t = i / k
        x, y = bez(*c, t)
        x2, y2 = bez(*c, min(1, t + 1e-3))
        x1, y1 = bez(*c, max(0, t - 1e-3))
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy)
        w = (2 + 3.2 * math.sin(math.pi * t)) / 2
        left.append((x - dy / ln * w, y + dx / ln * w))
        right.append((x + dy / ln * w, y - dx / ln * w))
    arch = poly(left + right[::-1], closed=True)
    head = _dhead(S, 6, 10.4, 2.9)
    return [shell(union(arch, head)), dot(4.6, 10.2, 0.85), line("M18.6 13C21 11.4 21.6 8 20.4 5.4C20 4.6 19.2 4.4 18.8 5")]


@icon("sleeping-cat", CAT, "Cat curled up asleep with its tail wrapped around", tags=["sleep", "nap", "cozy", "curled up", "pet"])
def _(S):
    body = ellipse(13.8, 13, 7.8, 6.2)
    e1 = soft(S, [(3.4, 13.8), (2.8, 9.6), (6.2, 11.6)], k=0.6)
    e2 = soft(S, [(6.8, 11.8), (9.2, 9.4), (10, 13)], k=0.6)
    head = union(circle(7, 15.2, 3.4), e1, e2)
    return [shell(minus(body, grow(head, 2.4))), shell(head), detail(L(S, "M4.8 15.6L6.6 16.4", "M4.8 15.4Q5.6 16.4 6.8 16")),
            detail("M19.6 12.8C19.6 16.4 16.6 18.2 13 17.6")]


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


def _dog(S, hx=6, hy=8.4, ear="up", snout=3.6):
    """Side-view dog head facing left: skull, muzzle and ear."""
    head = [circle(hx, hy, 2.5), soft(S, [(hx - 0.6, hy - 1.8), (hx - snout, hy + 0.6), (hx - snout + 0.2, hy + 2), (hx + 0.2, hy + 2.3)], k=0.8)]
    if ear == "up":
        head.append(soft(S, [(hx - 0.8, hy - 1.8), (hx + 0.4, hy - 4.8), (hx + 2.2, hy - 1.2)], k=0.5))
    elif ear == "round":
        head.append(ellipse(hx + 0.8, hy - 3, 1.7, 2.3))
    return union(*head)


@icon("jackal", CAT, "Jackal standing with tall pointed ears and a bushy tail held low", tags=["wild dog", "canine", "golden jackal", "africa", "wildlife"])
def _(S):
    body = union(ellipse(13.6, 11.6, 6.2, 3), _dog(S, 6, 8.6), thick(seg(6.8, 9.6, 9.4, 11), 3.4, S))
    tail = taper(((19.4, 10.8), (21.2, 12), (21.6, 15), (21.4, 18.6)), 2, 2.8)
    return [shell(union(body, tail)), dot(5.6, 8.2, 0.8), *stride(9.6, 13.4), *stride(16.2, 13.6)]


@icon("dingo", CAT, "Dingo standing alert with upright ears and a tail curled up", tags=["wild dog", "canine", "australia", "outback", "wildlife"])
def _(S):
    body = union(ellipse(13.4, 12, 6.2, 3.2), _dog(S, 6, 8.8), thick(seg(6.8, 9.8, 9.4, 11.4), 3.6, S))
    tail = taper(((19.2, 10.6), (21.8, 9.6), (22, 6), (19.8, 4.4)), 2, 2.4)
    return [shell(union(body, tail)), dot(5.6, 8.4, 0.8), *legs((9.4, 12), 14), *legs((15.4, 18), 14.2)]


@icon("african-wild-dog", CAT, "African wild dog with huge round ears, a blotched coat and a pale-tipped tail", tags=["painted dog", "painted wolf", "wild dog", "africa", "wildlife"])
def _(S):
    head = union(circle(6, 10, 2.5), soft(S, [(5.4, 8.2), (2.6, 10.6), (2.8, 12), (6.2, 12.3)], k=0.8))
    ear = ellipse(7, 5.4, 2, 2.8) if S.name == "rounded" else "M7 2.4C9.4 2.4 9.6 7 8.2 8.2L5.8 8.2C4.4 7 4.6 2.4 7 2.4Z"
    body = union(ellipse(13.6, 12.4, 6.2, 3.2), head, ear, thick(seg(6.8, 11, 9.4, 11.8), 3.4, S))
    return [shell(body), dot(5.2, 9.8, 0.8), *stride(9.8, 14.4), *stride(16.6, 14.6), line("M19.4 11.2C21 11.8 21.6 13.6 21.4 15.4"), shell(ellipse(21.4, 17.6, 1.2, 1.6)),
            mark(soft(S, [(10.8, 10.4), (13.4, 10.2), (12.8, 12.6), (10.6, 12.8)], k=0.5)), mark(soft(S, [(15.2, 11.8), (17.8, 10.6), (17.6, 13.2), (15.6, 13.6)], k=0.5))]


@icon("fennec-fox", CAT, "Fennec fox face with enormous upright ears and a small pointed snout", tags=["fox", "desert fox", "sahara", "big ears", "wildlife"])
def _(S):
    r = L(S, 0, 1.6)
    ear = ("M9.4 12" + tip((9.4, 12), (3.4, 2.6), (11.2, 9.6), r) + "L11.2 9.6Z") if S.name == "line" else "M9.4 12C6 9.6 3.6 6 3.8 3.4C4 2.4 5 2.4 6 3C8.4 4.4 10.2 6.8 11.2 9.6Z"
    face = "M12 20.8C10.4 19.6 7 18 7 14.4C7 11.4 9.2 9.6 12 9.6C14.8 9.6 17 11.4 17 14.4C17 18 13.6 19.6 12 20.8Z"
    return [shell(union(face, ear, flip(ear))), detail(L(S, "M8.2 10.8L5.6 5.4", "M8.2 10.8C7.2 8.6 6.4 7 5.6 5.4")), detail(flip(L(S, "M8.2 10.8L5.6 5.4", "M8.2 10.8C7.2 8.6 6.4 7 5.6 5.4"))),
            dot(10, 14, 1), dot(14, 14, 1), mark(ellipse(12, 18.4, 1, 0.8))]


@icon("arctic-fox", CAT, "Arctic fox curled up with a big bushy tail over its nose", tags=["polar fox", "snow fox", "white fox", "fox", "winter"])
def _(S):
    body = ellipse(14.4, 11.4, 7, 5.4)
    ears = [soft(S, [(4.8, 9), (4.6, 5.6), (7.2, 7.2)], k=0.9), soft(S, [(8, 7), (9.8, 4.8), (10.6, 8.2)], k=0.9)]
    head = union(circle(7.8, 10.8, 3), soft(S, [(6.4, 8.6), (2.6, 12.6), (7, 13.6)], k=0.8), *ears)
    tail = ("M21.4 11.6C21.8 17.6 17.4 21 11.4 21C7 21 3 19.4 2.4 15C5.4 17 8.4 17.6 11.4 17.2C15.4 16.6 19 14.8 21.4 11.6Z" if S.name == "rounded"
            else "M21.4 11.6C21.8 17.6 17.4 21 11.4 21L2.4 15C5.4 17 8.4 17.6 11.4 17.2C15.4 16.6 19 14.8 21.4 11.6Z")
    return [shell(minus(body, grow(head, 2.4), grow(tail, 2.4))), shell(minus(head, grow(tail, 2.4))), shell(tail), dot(7, 10.4, 0.85)]


@icon("maned-wolf", CAT, "Maned wolf on very long legs with a fox face and a dark neck mane", tags=["wolf", "wild dog", "canine", "south america", "long legs"])
def _(S):
    body = union(ellipse(14.2, 9.4, 5.4, 2.6), _dog(S, 6.4, 8.2, snout=3.2), thick(seg(7, 9, 10, 9.4), 3.2, S))
    mane = soft(S, [(7.8, 5.8), (10.6, 7.2), (12.4, 7.2), (10.8, 8.2), (8.4, 8.2)], k=0.4)
    tail = taper(((19.2, 8.6), (20.8, 9.6), (21.2, 11.6), (20.8, 14)), 1.8, 2.4)
    return [shell(union(body, tail)), mark(mane), dot(5.9, 7.8, 0.75), *stride(10.6, 11, 21, 0.6), *stride(17, 11, 21, 0.6)]


@icon("bat-eared-fox", CAT, "Bat-eared fox face with very wide sideways ears and a dark eye mask", tags=["fox", "big ears", "africa", "savanna", "wildlife"])
def _(S):
    ear = rot(ellipse(5.6, 9, 4.2, 2.4) if S.name == "rounded" else "M1.4 9C3.4 6.6 7.8 6.6 9.8 9C7.8 11.4 3.4 11.4 1.4 9Z", -24, 5.6, 9)
    face = "M12 20.6C10.6 19.4 7.4 17 7.4 13.6C7.4 11 9.4 9.4 12 9.4C14.6 9.4 16.6 11 16.6 13.6C16.6 17 13.4 19.4 12 20.6Z"
    mask = minus(soft(S, [(8, 12.4), (12, 13.6), (16, 12.4), (14.6, 15.6), (12, 15), (9.4, 15.6)], k=0.6), circle(10.2, 13.8, 0.8), circle(13.8, 13.8, 0.8))
    return [shell(union(face, ear, flip(ear))), mark(mask), mark(ellipse(12, 18.6, 1, 0.8))]


@icon("raccoon-dog", CAT, "Raccoon dog face with a dark eye mask, fluffy cheeks and small round ears", tags=["tanuki", "raccoon dog", "canine", "japan", "wildlife"], aliases=["tanuki"])
def _(S):
    if S.name == "line":
        head = poly([(8, 6.6), (6.4, 4), (4.6, 5.6), (5, 9), (2.4, 12.8), (4.6, 13.6), (2.8, 16.6), (6.4, 17), (8.6, 19.6), (12, 20.6), (15.4, 19.6),
                     (17.6, 17), (21.2, 16.6), (19.4, 13.6), (21.6, 12.8), (19, 9), (19.4, 5.6), (17.6, 4), (16, 6.6)], closed=True)
    else:
        head = union(ellipse(12, 13, 7, 7.2), circle(5.8, 5.6, 1.8), circle(18.2, 5.6, 1.8), circle(4.6, 12.6, 1.8), circle(19.4, 12.6, 1.8),
                     circle(5.2, 16, 1.8), circle(18.8, 16, 1.8))
    patch = soft(S, [(7, 11.4), (10.8, 11.6), (10.4, 14.6), (8.6, 17), (6.6, 15.4)], k=0.8)
    patch = minus(patch, circle(9, 12.8, 0.8))
    return [shell(head), mark(patch), mark(flip(patch)), _nose(S, 12, 16.6, 2, 1.1)]


@icon("tibetan-fox", CAT, "Tibetan fox face with a square flat head, narrow eyes and small ears", tags=["tibetan sand fox", "fox", "square face", "plateau", "wildlife"])
def _(S):
    r = L(S, 0, 0.8)
    head = union(rect(3.6, 7.2, 16.8, 10.2, L(S, 1, 2.5)), soft(S, [(7, 7.6), (8.2, 4.2), (10.2, 7.6)], k=0.6), soft(S, [(17, 7.6), (15.8, 4.2), (13.8, 7.6)], k=0.6),
                 rect(9.4, 15, 5.2, 5.6, L(S, 1, 2.2)))
    return [shell(head), detail(seg(6.8, 11.6, 10, 11.6)), detail(seg(14, 11.6, 17.2, 11.6)), mark(ellipse(12, 17.6, 1.1, 0.8))]


@icon("bush-dog", CAT, "Bush dog with a stocky long body, very short legs and small round ears", tags=["wild dog", "canine", "south america", "short legs", "wildlife"])
def _(S):
    body = union(ellipse(13.2, 13, 7.6, 3.6), circle(5.4, 11.4, 2.8), soft(S, [(4.2, 10), (2.2, 12), (2.6, 13.6), (5.2, 14)], k=0.8), circle(6.4, 8.8, 1.4))
    return [shell(body), dot(4.8, 11, 0.8), *legs((7.6, 10.4, 15.6, 18.4), 15.8, 20), line("M20.6 12C21.8 11.2 22 10 21.8 9")]


@icon("hyena", CAT, "Spotted hyena with a sloping back, round ears and a spotted coat", tags=["spotted hyena", "laughing hyena", "scavenger", "africa", "wildlife"])
def _(S):
    body = union(rot(ellipse(13, 10.6, 6.4, 3.4), 14, 13, 10.6), _dog(S, 5.6, 8.4, ear="round", snout=3), thick(seg(6.4, 9, 9.4, 8.6), 3.8, S))
    return [shell(body), dot(5, 8.2, 0.8), *stride(9.2, 12, 21, 0.8), *stride(16.4, 14.2, 21, 0.8), line("M18.6 13C19.8 14 20.2 15.6 19.8 17"),
            *[dot(x, y, 0.8) for x, y in ((11.2, 9.4), (14.2, 10.4), (12.4, 11.8))]]


@icon("dachshund", CAT, "Dachshund with a very long low body, short legs and long floppy ears", tags=["sausage dog", "wiener dog", "doxie", "dog breed", "pet"], aliases=["sausage-dog"])
def _(S):
    body = union(ellipse(13, 13.2, 8, 3), _dog(S, 5.2, 10.4, ear=None, snout=3.2), thick(seg(5.8, 11.6, 7.4, 12.6), 3.4, S))
    ear = ellipse(6.4, 11.6, 1.5, 2.6) if S.name == "rounded" else "M6.4 8.8C8.2 9.8 8.2 13.4 6.4 14.4C4.6 13.4 4.6 9.8 6.4 8.8Z"
    return [shell(minus(body, grow(ear, 2.4))), shell(ear), dot(4.4, 9.8, 0.75), *legs((8.2, 11, 15.8, 18.6), 15.4, 20.4), line("M20.8 12.2C21.8 11.4 22 10 21.8 8.6")]


@icon("poodle", CAT, "Poodle in a show clip with pom-poms on its head, chest, hips, legs and tail", tags=["dog breed", "pom poms", "show dog", "groomed", "pet"])
def _(S):
    head = union(circle(6.2, 6.4, 2.2), circle(6.8, 4, 1.8), soft(S, [(5.4, 5.4), (2.2, 7.2), (2.4, 8.4), (6, 8.4)], k=0.6))
    chest = ellipse(8.6, 11.6, 3.4, 3.6)
    hip = circle(16.6, 11.2, 2.8)
    waist = thick(seg(10, 11.6, 15, 11.2), 2.4, S)
    return [shell(union(head, chest, hip, waist)), dot(5.6, 6.2, 0.75), line(seg(7.6, 14.8, 7.6, 18.4)), line(seg(10.4, 14.4, 10.4, 18.4)),
            line(seg(15.6, 13.6, 15.6, 18.4)), line(seg(18, 13, 18, 18.4)), line("M19 9.8L20.2 6.8"), shell(circle(20.6, 5, 1.7)),
            *[shell(ellipse(x, 19.6, 1.5, 1.4)) for x in (7.2, 10.8, 15.2, 18.4)]]


@icon("bulldog", CAT, "Bulldog face with heavy jowls, a pushed-in nose and an underbite", tags=["english bulldog", "british bulldog", "dog breed", "tough", "pet"])
def _(S):
    ear = soft(S, [(4.4, 8), (6.2, 4.8), (9.2, 6.8), (6, 8.6)], k=0.6)
    if S.name == "line":
        head = poly([(5, 6.4), (19, 6.4), (21, 11), (20.6, 17), (17.6, 19.8), (14, 20.6), (10, 20.6), (6.4, 19.8), (3.4, 17), (3, 11)], closed=True)
    else:
        head = union(rect(3, 6.4, 18, 11, 5), ellipse(12, 17, 7.6, 3.6))
    return [shell(union(head, ear, flip(ear))), detail("M9.6 9Q12 10.2 14.4 9"), dot(8, 11.4, 1), dot(16, 11.4, 1), mark(ellipse(12, 12.4, 1.8, 1.1)),
            detail("M7.6 15.6C9 14 10.6 13.8 12 14.8C13.4 13.8 15 14 16.4 15.6"), detail(L(S, "M9 18.2L15 18.2", "M9 18Q12 19 15 18"))]
