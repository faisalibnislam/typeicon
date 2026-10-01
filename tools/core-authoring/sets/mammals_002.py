"""TypeIcon Core: mammals (batch 002). Dog breeds, bears, mustelids, small carnivores and rodents.

Faces are drawn in front view; whole animals in side view facing left (head on the left), matching sets/mammals_001.py.
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



def _dog(S, hx=6, hy=8.4, ear="up", snout=3.6):
    """Side-view dog head facing left: skull, muzzle and ear."""
    head = [circle(hx, hy, 2.5), soft(S, [(hx - 0.6, hy - 1.8), (hx - snout, hy + 0.6), (hx - snout + 0.2, hy + 2), (hx + 0.2, hy + 2.3)], k=0.8)]
    if ear == "up":
        head.append(soft(S, [(hx - 0.8, hy - 1.8), (hx + 0.4, hy - 4.8), (hx + 2.2, hy - 1.2)], k=0.5))
    elif ear == "round":
        head.append(ellipse(hx + 0.8, hy - 3, 1.7, 2.3))
    return union(*head)


# --------------------------------------------------------------------------- local helpers (batch 002)

def eyes(y, dx=3, r=1.0, cx=12):
    return [dot(cx - dx, y, r), dot(cx + dx, y, r)]


def fluff(S, cx, cy, r, n=12, bump=2.0, start=-90.0, spike=1.6):
    """Fluffy round outline: scallops (Rounded) or a jagged star (Line)."""
    if S.name == "line":
        pts = []
        for i in range(2 * n):
            a = start + i * 180.0 / n
            pts.append(pt((cx, cy), r + (spike if i % 2 == 0 else 0), a))
        return poly(pts, closed=True)
    parts = [circle(cx, cy, r)]
    for i in range(n):
        c = pt((cx, cy), r, start + i * 360.0 / n)
        parts.append(circle(c[0], c[1], bump))
    return union(*parts)


# =========================================================================== dog breeds, faces

@icon("french-bulldog", CAT, "French bulldog face with large upright rounded bat ears and a flat nose", tags=["frenchie", "dog breed", "bat ears", "pet", "flat face"], aliases=["frenchie"])
def _(S):
    ear = soft(S, [(3.4, 11.4), (2.6, 5.4), (4.4, 2.8), (8.6, 4.6), (9.6, 10)], k=L(S, 0.6, 2.4))
    head = rect(4, 8.4, 16, 11.2, L(S, 3, 5.6))
    return [shell(union(head, ear, flip(ear))), *eyes(12.6, 4.2, 1.1), mark(ellipse(12, 15.4, 2.4, 1.3)), detail(L(S, "M12 16.6L12 17.8", "M12 16.6L12 17.6"))]


@icon("pug", CAT, "Pug face with a round wrinkled forehead, big eyes, folded ears and a dark muzzle", tags=["dog breed", "wrinkles", "pet", "flat face", "toy dog"])
def _(S):
    ear = soft(S, [(4.2, 10), (3, 4.6), (9, 7.6)], k=1.0)
    head = ellipse(12, 13.2, 8, 7.2) if S.name == "rounded" else poly([(6.6, 7), (17.4, 7), (20.2, 11), (20, 16), (16.4, 20.4), (7.6, 20.4), (4, 16), (3.8, 11)], closed=True)
    return [shell(union(head, ear, flip(ear))), detail("M9.4 9.8Q12 8.4 14.6 9.8"), *eyes(12.6, 4, 1.3),
            mark(rect(8.8, 14.8, 6.4, 4, L(S, 1, 2))), ]


@icon("chihuahua", CAT, "Chihuahua head with a small apple-shaped skull and huge ears angled outward", tags=["dog breed", "tiny dog", "toy dog", "big ears", "pet"])
def _(S):
    ear = soft(S, [(9, 11), (1.6, 8), (1.6, 2.6), (10, 7.4)], k=L(S, 0, 1.4))
    head = circle(12, 13.6, 6)
    return [shell(union(head, ear, flip(ear))), *eyes(13, 2.8, 1.3), mark(soft(S, [(10.6, 16.4), (13.4, 16.4), (12, 17.8)], k=0.5))]


@icon("afghan-hound", CAT, "Afghan hound head with a long narrow face framed by long silky hair curtains", tags=["hound", "dog breed", "long hair", "silky", "sighthound"])
def _(S):
    hair = soft(S, [(12, 2.6), (18, 4.6), (20.6, 10), (20.4, 21), (16.4, 21), (16, 16), (8, 16), (7.6, 21), (3.6, 21), (3.4, 10), (6, 4.6)], k=L(S, 0, 2))
    return [shell(hair), detail("M8.8 6.6Q8.4 12 9.4 15.4L12 19L14.6 15.4Q15.6 12 15.2 6.6"), *eyes(10.8, 2, 0.9), mark(ellipse(12, 16.2, 1.5, 1))]


@icon("basset-hound", CAT, "Basset hound in side view with a long low body, very long ears and droopy eyes", tags=["hound", "dog breed", "long ears", "low dog", "pet"])
def _(S):
    body = union(ellipse(13.6, 12.4, 7.6, 3), _dog(S, 5.6, 9.6, ear=None, snout=3.4), thick(seg(6.4, 10.8, 8.6, 12), 3.6, S))
    ear = ellipse(6.6, 13.4, 1.6, 3.4) if S.name == "rounded" else "M6.6 9.8C8.6 11 8.6 16 6.6 16.8C4.6 16 4.6 11 6.6 9.8Z"
    return [shell(minus(body, grow(ear, 2.4))), shell(ear), dot(4.8, 9.2, 0.75), *legs((9.6, 12, 17, 19.6), 14.6, 20.4), line("M21 11C21.8 10.4 22 9.4 21.8 8.4")]


@icon("bloodhound", CAT, "Bloodhound face with loose wrinkled skin, deep jowls and very long hanging ears", tags=["hound", "dog breed", "tracking dog", "scent", "wrinkles"])
def _(S):
    ear = soft(S, [(7.6, 6), (3.4, 8), (3.2, 15), (5, 20.4), (7.6, 17)], k=L(S, 0, 2))
    head = union(ellipse(12, 10, 4.8, 6.4), rect(7.6, 12, 8.8, 8, L(S, 1.5, 3.6)))
    return [shell(union(head, ear, flip(ear))), detail("M9.6 6.6Q12 5.4 14.4 6.6"), *eyes(9.6, 2.6, 0.95), mark(ellipse(12, 13.8, 2, 1.2)),
            detail(L(S, "M9.6 17L14.4 17", "M9.6 16.8Q12 18 14.4 16.8"))]


@icon("schnauzer", CAT, "Schnauzer face with bushy eyebrows, a long square beard and folded ears", tags=["dog breed", "beard", "mustache", "terrier", "pet"])
def _(S):
    ear = soft(S, [(6.6, 5.6), (4, 3.4), (4.4, 8.6)], k=0.8)
    head = rect(6.4, 4.8, 11.2, 9, L(S, 1.5, 3))
    beard = soft(S, [(6.6, 12), (17.4, 12), (18.6, 21), (5.4, 21)], k=L(S, 0, 1.4))
    brow = lambda s: soft(S, [(7, 8.4 + s), (10.8, 8.8 + s), (10.8, 10.2 + s), (7.4, 9.8 + s)], k=0.4)
    return [shell(union(head, beard, ear, flip(ear))), mark(brow(0)), mark(flip(brow(0))), *eyes(11.6, 2.6, 0.8), mark(ellipse(12, 14.2, 1.7, 1.1)),
            detail(L(S, "M12 15.4L12 18.4", "M12 15.4L12 18.2"))]


@icon("pomeranian", CAT, "Pomeranian as a round fluffy ball of fur with a small fox face and tiny pointed ears", tags=["dog breed", "fluffy", "toy dog", "spitz", "pet"])
def _(S):
    ear = soft(S, [(6.6, 7.4), (6.4, 2.4), (11, 5.4)], k=0.7)
    return [shell(union(fluff(S, 12, 13.2, 6.8, 10, 1.9, spike=1.4), ear, flip(ear))), *eyes(12.2, 3, 1.0), mark(ellipse(12, 14.6, 1.5, 1)),
            detail("M12 15.6Q12 17.2 10.4 17.4"), detail("M12 15.6Q12 17.2 13.6 17.4")]


@icon("chow-chow", CAT, "Chow chow face with a thick lion-like mane ruff, small rounded ears and a scowl", tags=["dog breed", "mane", "fluffy", "ruff", "pet"])
def _(S):
    ear = soft(S, [(5.4, 6.4), (5.6, 2.4), (9.6, 4.4)], k=0.9)
    return [shell(union(fluff(S, 12, 12.6, 7.6, 12, 2.2, spike=1.8), ear, flip(ear))), detail(ellipse(12, 12.4, 5, 4.6)),
            detail("M7.8 9.2L10.6 10.4"), detail("M16.2 9.2L13.4 10.4"), *eyes(11.6, 2.8, 0.8), mark(ellipse(12, 14.2, 1.7, 1))]


@icon("shar-pei", CAT, "Shar pei face with heavy deep folds over the head and a broad padded muzzle", tags=["dog breed", "wrinkles", "folds", "chinese dog", "pet"])
def _(S):
    ear = soft(S, [(5.6, 8.6), (3.8, 5.6), (8.2, 6.6)], k=0.8)
    head = rect(3.8, 5.6, 16.4, 14.6, L(S, 4, 7))
    return [shell(union(head, ear, flip(ear))), detail("M7 9.2Q12 6.8 17 9.2"), detail("M6.4 12Q12 9.8 17.6 12"), *eyes(13.6, 4.6, 0.85),
            mark(rect(8.4, 15.4, 7.2, 3, L(S, 1, 1.5))), ]


@icon("samoyed", CAT, "Samoyed face with thick white fluffy fur, upright ears and an upturned smiling mouth", tags=["dog breed", "spitz", "fluffy", "smile", "white dog"])
def _(S):
    ear = soft(S, [(6.4, 7), (6.6, 2.4), (10.8, 5)], k=0.8)
    head = union(ellipse(12, 13, 7.2, 6.6), circle(5.4, 14.6, 2), circle(18.6, 14.6, 2)) if S.name == "rounded" else \
        poly([(7, 7.6), (17, 7.6), (20.4, 12), (19.6, 14), (20.4, 16), (16.6, 19.8), (7.4, 19.8), (3.6, 16), (4.4, 14), (3.6, 12)], closed=True)
    return [shell(union(head, ear, flip(ear))), *eyes(11.8, 3.4, 1.0), mark(ellipse(12, 14, 1.6, 1.0)), detail("M8.6 15.6Q10.4 18.2 12 15.6Q13.6 18.2 15.4 15.6")]


@icon("boston-terrier", CAT, "Boston terrier face with upright pointed ears, big round eyes and a white blaze", tags=["dog breed", "tuxedo", "terrier", "pet", "big eyes"])
def _(S):
    ear = soft(S, [(6.2, 8), (4.4, 2.6), (9.4, 5.8)], k=L(S, 0, 0.8))
    head = rect(4.6, 5.6, 14.8, 14.2, L(S, 2.4, 5.2))
    return [shell(union(head, ear, flip(ear))), detail("M12 6.6L12 10.6"), *eyes(12, 4, 1.3), mark(ellipse(12, 14.8, 2, 1.2)), detail(L(S, "M12 16L12 17.2", "M12 16L12 17"))]


@icon("cocker-spaniel", CAT, "Cocker spaniel face with a curly topknot and long wavy ears hanging below the jaw", tags=["spaniel", "dog breed", "floppy ears", "gundog", "pet"])
def _(S):
    if S.name == "line":
        ear = poly([(7.4, 5.4), (3.6, 8), (3.4, 12.4), (2.6, 15), (4.4, 17), (3.8, 20.4), (6.6, 19.2), (8, 16), (7.6, 10)], closed=True)
    else:
        ear = "M7.4 5.4C4 5.4 2.8 8.6 3.4 12.4C3.8 15 2.6 17 4.4 19.4C6.2 21 7.8 18 8 15.6C8.2 12 8 8 7.4 5.4Z"
    head = union(ellipse(12, 10.4, 5.2, 5.8), circle(12, 4.4, 1.9) if S.name == "rounded" else soft(S, [(10, 5.4), (12, 2.2), (14, 5.4)], k=0))
    return [shell(union(head, ear, flip(ear))), *eyes(10.4, 2.6, 1.0), mark(ellipse(12, 14.2, 1.9, 1.2)), detail("M12 15.4L12 16.8"), detail("M9.6 16.8Q12 18 14.4 16.8")]


@icon("beagle", CAT, "Beagle face with long drooping rounded ears, a white blaze and a broad muzzle", tags=["hound", "dog breed", "floppy ears", "scent hound", "pet"])
def _(S):
    ear = soft(S, [(7.4, 5.4), (3.6, 6.8), (3.4, 14), (6, 16.6), (8, 12)], k=L(S, 0, 2.2))
    head = ellipse(12, 11, 5.4, 6.4) if S.name == "rounded" else poly([(9, 4.6), (15, 4.6), (17.4, 9), (16.8, 16), (13.4, 17.6), (10.6, 17.6), (7.2, 16), (6.6, 9)], closed=True)
    return [shell(union(head, ear, flip(ear))), detail("M12 6L12 9.6"), *eyes(10.6, 2.8, 1.0), detail(ellipse(12, 15, 3.2, 2.6)), mark(ellipse(12, 13.8, 1.6, 1.0))]


@icon("boxer-dog", CAT, "Boxer dog head with a square short muzzle, an undershot jaw and a wrinkled forehead", tags=["dog breed", "square muzzle", "underbite", "guard dog", "pet"])
def _(S):
    ear = soft(S, [(6.4, 7.6), (4, 3.4), (9, 5.6)], k=L(S, 0, 0.8))
    head = union(rect(5.6, 4.6, 12.8, 8.6, L(S, 1.5, 3.4)), rect(7.2, 10.6, 9.6, 9.6, L(S, 1.5, 3.4)))
    return [shell(union(head, ear, flip(ear))), detail("M10 6.8Q12 8 14 6.8"), *eyes(10.2, 3.4, 0.95), mark(rect(10.4, 12.4, 3.2, 1.6, 0.6)), detail(L(S, "M9.6 16.6L14.4 16.6", "M9.6 16.6Q12 17.6 14.4 16.6"))]


@icon("rottweiler", CAT, "Rottweiler head with a broad heavy skull, folded triangular ears and tan spots above the eyes", tags=["dog breed", "guard dog", "working dog", "strong", "pet"])
def _(S):
    ear = soft(S, [(6.6, 4.6), (2.8, 5.8), (4.4, 12), (7.4, 10)], k=L(S, 0, 1.2))
    head = union(rect(5.4, 3.6, 13.2, 9, L(S, 2, 4)), rect(7.4, 10, 9.2, 10.4, L(S, 1.5, 3.4)))
    return [shell(union(head, ear, flip(ear))), dot(8.8, 7, 0.8), dot(15.2, 7, 0.8), *eyes(9.8, 3, 0.9), mark(ellipse(12, 13.4, 2.4, 1.4)), detail(L(S, "M9.2 16.8L14.8 16.8", "M9.2 16.6Q12 17.8 14.8 16.6"))]


@icon("golden-retriever", CAT, "Golden retriever head with feathered wavy ears, a fluffy ruff and a friendly open mouth", tags=["retriever", "dog breed", "family dog", "friendly", "pet"])
def _(S):
    if S.name == "line":
        ear = poly([(7.2, 5), (3.4, 7), (3.2, 12), (4.6, 14.6), (3.6, 17), (6.6, 16), (8, 11)], closed=True)
        ruff = poly([(6, 15), (18, 15), (19.6, 18.6), (16.6, 17.8), (15, 21), (12, 18.8), (9, 21), (7.4, 17.8), (4.4, 18.6)], closed=True)
    else:
        ear = "M7.2 5C3.8 5 2.8 8.4 3.4 11.6C3.6 13.6 3 15 4.4 16.4C6 17.4 7.6 15 8 12C8.2 9 8 6.6 7.2 5Z"
        ruff = union(circle(8, 17.6, 2.6), circle(12, 18.4, 2.6), circle(16, 17.6, 2.6), ellipse(12, 15.4, 6, 2.6))
    head = ellipse(12, 10, 5.4, 5.8) if S.name == "rounded" else poly([(9, 4.2), (15, 4.2), (17.4, 8), (17.2, 14), (14, 16), (10, 16), (6.8, 14), (6.6, 8)], closed=True)
    return [shell(union(head, ear, flip(ear), ruff)), *eyes(9.6, 2.8, 1.0), mark(ellipse(12, 12.4, 2, 1.2)), detail("M9.4 14Q12 16.6 14.6 14"), mark(ellipse(12, 16.6, 1.3, 0.9))]


@icon("bichon-frise", CAT, "Bichon frise face as a round cloud-like puff of curly white hair with dark eyes and nose", tags=["dog breed", "curly", "fluffy", "toy dog", "pet"])
def _(S):
    if S.name == "line":
        puff = fluff(S, 12, 12, 7.6, 9, 2.4, spike=2.2)
    else:
        puff = union(circle(12, 12.4, 7), circle(12, 5.6, 2.6), circle(6.4, 8, 2.6), circle(17.6, 8, 2.6), circle(5.4, 14, 2.4), circle(18.6, 14, 2.4),
                     circle(8.4, 18.4, 2.4), circle(15.6, 18.4, 2.4))
    return [shell(puff), *eyes(11.6, 3, 1.1), mark(ellipse(12, 14.4, 1.8, 1.2))]


@icon("west-highland-terrier", CAT, "West Highland terrier head with a round chrysanthemum face of white fur and small pointed ears", tags=["westie", "dog breed", "terrier", "scottish", "white dog"], aliases=["westie"])
def _(S):
    ear = soft(S, [(7.4, 7.6), (7.6, 2.6), (11, 6)], k=L(S, 0, 0.7))
    if S.name == "line":
        face = poly([(12, 5.4), (16.4, 6.2), (19.4, 8.6), (21, 12.4), (19.4, 16), (17, 19), (12, 20.4), (7, 19), (4.6, 16), (3, 12.4), (4.6, 8.6), (7.6, 6.2)], closed=True)
    else:
        face = union(ellipse(12, 13, 7.6, 7), circle(5.6, 10, 2.2), circle(18.4, 10, 2.2), circle(5.8, 16.4, 2.2), circle(18.2, 16.4, 2.2), circle(12, 19.4, 2.4))
    return [shell(union(face, ear, flip(ear))), *eyes(11.8, 3.2, 1.0), mark(ellipse(12, 14.8, 2.2, 1.5))]


@icon("papillon", CAT, "Papillon face with large fringed upright ears spread like butterfly wings", tags=["dog breed", "butterfly", "toy dog", "big ears", "pet"])
def _(S):
    ear = rot(ellipse(6.6, 9, 5.4, 3.2) if S.name == "rounded" else "M1.2 9L6.6 5.8L12 9L6.6 12.2Z", 36, 6.6, 9)
    head = circle(12, 14, 5)
    return [shell(union(head, ear, flip(ear))), detail("M3.6 4.6L8 9"), detail("M20.4 4.6L16 9"),
            *eyes(13.2, 2.4, 1.0), mark(ellipse(12, 16.4, 1.4, 0.9))]


@icon("pekingese", CAT, "Pekingese face with a flat nose, a long flowing mane and heavily fringed drooping ears", tags=["dog breed", "lion dog", "flat face", "toy dog", "pet"])
def _(S):
    ear = soft(S, [(6.8, 5), (2.6, 7), (2.4, 14), (5, 16.6), (7.4, 11)], k=L(S, 0, 2))
    mane = soft(S, [(5.4, 13), (18.6, 13), (21.4, 21), (2.6, 21)], k=L(S, 0, 2))
    head = ellipse(12, 10.6, 6, 5.8) if S.name == "rounded" else poly([(8, 5), (16, 5), (18.4, 9), (18, 14), (14, 16.6), (10, 16.6), (6, 14), (5.6, 9)], closed=True)
    return [shell(union(head, ear, flip(ear), mane)), *eyes(9.8, 3, 1.15), mark(ellipse(12, 12.6, 2, 1.1)), detail("M9.6 15Q12 16.4 14.4 15"), detail(seg(12, 17.8, 12, 20))]


@icon("old-english-sheepdog", CAT, "Old English sheepdog face with shaggy hair completely covering the eyes and a round black nose", tags=["sheepdog", "dog breed", "shaggy", "herding dog", "pet"])
def _(S):
    return [shell(fluff(S, 12, 12.2, 7.6, 10, 2.4, spike=2.0)), detail(seg(7.8, 5.6, 7.8, 10.6)), detail(seg(12, 4.6, 12, 10.6)), detail(seg(16.2, 5.6, 16.2, 10.6)),
            mark(ellipse(12, 14, 2.4, 1.7)), detail(L(S, "M12 15.8L12 18", "M12 15.8L12 17.8"))]


@icon("brussels-griffon", CAT, "Brussels griffon face with a short nose, a bushy beard and mustache and a human-like expression", tags=["dog breed", "toy dog", "beard", "griffon", "pet"])
def _(S):
    ear = soft(S, [(6.6, 6.6), (4, 3.6), (4.2, 9.6)], k=L(S, 0, 0.8))
    head = circle(12, 10.6, 6.6)
    beard = soft(S, [(5.8, 12.6), (18.2, 12.6), (16, 20.6), (8, 20.6)], k=L(S, 0, 2))
    return [shell(union(head, beard, ear, flip(ear))), *eyes(9.6, 3, 1.3), mark(ellipse(12, 12.6, 1.7, 1.1)), detail("M8.2 15Q10 13.6 12 14.8Q14 13.6 15.8 15"), detail(seg(12, 16.8, 12, 18.4))]


@icon("cavalier-king-charles-spaniel", CAT, "Cavalier King Charles spaniel face with big round eyes and long silky feathered ears", tags=["spaniel", "dog breed", "toy dog", "big eyes", "pet"])
def _(S):
    if S.name == "line":
        ear = poly([(7.8, 4.6), (4, 6), (3, 11), (3.6, 14.4), (2.6, 16.6), (4.6, 19), (5.6, 16.6), (7.6, 18), (8.6, 12)], closed=True)
    else:
        ear = "M7.8 4.6C4.6 4.6 3 7.6 3.2 11C3.4 13.4 2.6 15.4 3.8 17.6C5.2 19.6 7 18.2 7.6 16.4C8.6 14 8.8 7.6 7.8 4.6Z"
    head = ellipse(12, 10.6, 5.4, 6.2) if S.name == "rounded" else poly([(9, 4.6), (15, 4.6), (17.4, 8.6), (17, 14), (13.6, 16.8), (10.4, 16.8), (7, 14), (6.6, 8.6)], closed=True)
    return [shell(union(head, ear, flip(ear))), detail("M12 5.6L12 9.4"), *eyes(10.2, 2.6, 1.3), mark(ellipse(12, 13.8, 1.9, 1.2)), detail("M9.8 15.8Q12 17.2 14.2 15.8")]


@icon("bernese-mountain-dog", CAT, "Bernese mountain dog face with a white blaze, rust brows, tricolor markings and folded ears", tags=["dog breed", "mountain dog", "tricolor", "swiss", "pet"])
def _(S):
    ear = soft(S, [(7, 4.6), (3.2, 5.4), (4.2, 11.6), (7.6, 10)], k=L(S, 0, 1.4))
    head = union(ellipse(12, 10.2, 6, 6.2), rect(8, 12.4, 8, 7.6, L(S, 1.5, 3.4))) if S.name == "rounded" else \
        union(poly([(8, 4.2), (16, 4.2), (18, 9), (16.6, 14), (7.4, 14), (6, 9)], closed=True), rect(8, 12.4, 8, 7.6, 1.5))
    return [shell(union(head, ear, flip(ear))), mark(ellipse(5.6, 8.2, 1.2, 2.2)), mark(ellipse(18.4, 8.2, 1.2, 2.2)), detail("M12 5.4L12 9"), dot(8.6, 7.6, 0.75), dot(15.4, 7.6, 0.75),
            *eyes(10, 3.2, 0.9), mark(ellipse(12, 13.6, 1.9, 1.1)), detail(L(S, "M9.6 17L14.4 17", "M9.6 16.8Q12 18 14.4 16.8"))]


@icon("komondor", CAT, "Komondor as a mop of long corded dreadlocks covering the whole body and face", tags=["dog breed", "dreadlocks", "corded coat", "mop", "hungarian"])
def _(S):
    if S.name == "line":
        body = poly([(12, 3), (17.4, 4.6), (20.6, 9.6), (20.6, 21), (18.2, 18.6), (16.4, 21), (14.2, 18.6), (12, 21), (9.8, 18.6), (7.6, 21), (5.8, 18.6), (3.4, 21), (3.4, 9.6), (6.6, 4.6)], closed=True)
    else:
        body = union(rect(3.4, 4, 17.2, 13, 7), circle(5.6, 17.2, 2.2), circle(9.4, 17.6, 2), circle(14.6, 17.6, 2), circle(18.4, 17.2, 2.2), circle(12, 17.8, 2.2))
    return [shell(body), detail(seg(6.8, 6.4, 6.8, 16)), detail(seg(9.6, 5.4, 9.6, 16)), detail(seg(14.4, 5.4, 14.4, 16)), detail(seg(17.2, 6.4, 17.2, 16)), mark(ellipse(12, 11.6, 1.3, 1.0))]


@icon("yorkshire-terrier", CAT, "Yorkshire terrier with long silky hair parted down the center and a small bow topknot on the head", tags=["yorkie", "dog breed", "toy dog", "bow", "long hair"], aliases=["yorkie"])
def _(S):
    hair = soft(S, [(12, 6), (17.6, 7.8), (19.6, 13), (20.6, 21), (3.4, 21), (4.4, 13), (6.4, 7.8)], k=L(S, 0, 2.2))
    bow = soft(S, [(12, 4.6), (8.2, 2.2), (8.2, 7)], k=L(S, 0, 0.5))
    return [shell(union(hair, bow, flip(bow))), detail(ellipse(12, 13.4, 4.6, 4.4)), *eyes(12.4, 2.2, 0.9), mark(ellipse(12, 14.8, 1.4, 0.9)), dot(12, 4.6, 0.9)]


# =========================================================================== dog breeds, profiles and whole dogs

def _prof(S, nx=2.4, ny=12.4, sx=8.6, sy=8.8, jaw=15.8, neck=9.6, k=1.0, top=7.2):
    """Dog head in profile facing left with a neck running off to the lower right."""
    pts = [(nx, ny - 1.2), (sx, sy), (sx + 1.6, top), (14.4, top + 0.2), (18.2, top + 2.6), (20.8, 14.4), (20.8, 21), (neck, 21), (neck, jaw + 0.8),
           (sx - 1.8, jaw), (nx + 0.6, jaw - 1.6), (nx - 0.1, ny + 0.6)]
    return poly(pts, closed=True, r=L(S, 0, k))


@icon("german-shepherd", CAT, "German shepherd head in profile with a tall pointed ear, a long muzzle and a dark saddle marking", tags=["alsatian", "dog breed", "police dog", "working dog", "pet"], aliases=["alsatian"])
def _(S):
    ear = soft(S, [(8.8, 8.8), (10, 2.4), (14.2, 7.6)], k=L(S, 0, 0.8))
    return [shell(union(_prof(S), ear)), mark(soft(S, [(14.6, 11), (19.4, 14.2), (19.4, 19), (14.6, 15)], k=L(S, 0, 0.8))), dot(8.4, 11, 0.9), mark(ellipse(3.6, 12.4, 1.2, 1))]


@icon("doberman", CAT, "Doberman head in profile with a tall cropped pointed ear, a long narrow muzzle and tan brow spots", tags=["dobermann", "dog breed", "guard dog", "sleek", "pet"], aliases=["dobermann"])
def _(S):
    ear = soft(S, [(9.4, 8.6), (9.8, 2.8), (13, 7.4)], k=L(S, 0, 0.6))
    head = _prof(S, nx=1.8, ny=12.8, sx=9, sy=9.2, jaw=15.6, neck=11.4, top=7.6)
    return [shell(union(head, ear)), dot(9.6, 8.2, 0.7), dot(8.6, 11.6, 0.9), mark(ellipse(2.8, 12.6, 1.1, 0.9)), detail(L(S, "M13 15L13 21", "M13 15.4L13 20.6"))]


@icon("bull-terrier", CAT, "Bull terrier head in profile with a long egg-shaped face and no stop between skull and nose", tags=["dog breed", "egg head", "terrier", "pet", "roman nose"])
def _(S):
    head = poly([(2.2, 14), (6.6, 8.4), (10.6, 6.6), (14.6, 7), (18.4, 9.6), (20.8, 14.4), (20.8, 21), (10.2, 21), (10.2, 16.4), (5, 16.6), (2.2, 15.6)], closed=True, r=L(S, 0, 1.8))
    ear = soft(S, [(10.6, 7.4), (11.2, 2.6), (14.6, 7.2)], k=L(S, 0, 0.7))
    return [shell(union(head, ear)), dot(8.2, 11.8, 0.85), mark(ellipse(3.2, 14, 1.2, 1.0))]


@icon("borzoi", CAT, "Borzoi head in profile with a very long narrow slightly curved muzzle and silky neck fur", tags=["russian wolfhound", "dog breed", "sighthound", "long nose", "pet"])
def _(S):
    head = poly([(1.4, 13.6), (5, 11), (8.6, 8.4), (11, 7.2), (15, 7.6), (18.4, 10), (21, 14), (21, 21), (11.6, 21), (11.4, 16.4), (8.6, 15.6), (2.4, 15.2)], closed=True, r=L(S, 0, 1.4))
    ear = soft(S, [(11, 8), (13.4, 5.4), (14, 9.6)], k=L(S, 0, 0.6))
    return [shell(union(head, ear)), dot(9, 11, 0.85), mark(ellipse(2.4, 13.8, 1, 0.8)), detail(L(S, "M15 12L18.6 17", "M15 12Q17.6 14 18.6 17")), detail(L(S, "M17.6 11.6L20 16", "M17.8 11.8Q19.6 13.4 20 16"))]


@icon("rough-collie", CAT, "Rough collie head in profile with a long narrow muzzle, a full neck ruff and a tipped ear", tags=["collie", "dog breed", "long hair", "herding dog", "pet"])
def _(S):
    if S.name == "line":
        ruff = poly([(10, 13), (16, 10.6), (21.2, 14), (21.2, 21), (17.4, 19.4), (15.4, 21), (12.6, 19), (10, 20.6), (9.2, 17)], closed=True)
    else:
        ruff = union(ellipse(15.4, 16, 6, 5.6), circle(10.6, 18.4, 2.2), circle(13.8, 20, 2.2))
    head = poly([(1.8, 13), (8.6, 8.8), (10.4, 7.2), (14.6, 7.4), (16.6, 9.6), (13, 12.8), (10, 16), (5.6, 15.8), (2.4, 14.6)], closed=True, r=L(S, 0, 1.2))
    ear = poly([(9.6, 8.4), (10.2, 3), (13.2, 3.2), (14.6, 7.8)], closed=True, r=L(S, 0, 0.8))
    return [shell(union(head, ear, ruff)), dot(8.2, 11, 0.85), mark(ellipse(2.8, 13, 1, 0.85))]


@icon("labrador-retriever", CAT, "Labrador head in profile with a broad skull, short smooth coat, a drop ear and a thick neck", tags=["lab", "retriever", "dog breed", "family dog", "pet"], aliases=["lab-dog"])
def _(S):
    head = poly([(2.6, 11.6), (8, 8.6), (10, 6.6), (15, 6.8), (19, 9.6), (21, 14.4), (21, 21), (9.8, 21), (9.6, 16.8), (5, 16.2), (2.6, 14.6)], closed=True, r=L(S, 0, 2))
    return [shell(head), detail("M11.4 9C14.8 8.6 16 12 15 15C13.2 15.6 11.2 13.6 11.4 9"), dot(8.2, 10.8, 0.9), mark(ellipse(3.8, 11.8, 1.3, 1.1)), detail(L(S, "M6 15L8.6 14.4", "M5.6 15Q7 15 8.6 14.4"))]


@icon("saluki", CAT, "Saluki head in profile with a long narrow muzzle and long silky feathered hanging ear", tags=["persian greyhound", "dog breed", "sighthound", "feathered ears", "pet"])
def _(S):
    head = poly([(1.6, 13.4), (5, 11), (9, 8.4), (11.4, 6.8), (15.4, 7.2), (19, 10), (21, 14.6), (21, 21), (12, 21), (11.8, 16), (8.6, 15.6), (2.6, 15)], closed=True, r=L(S, 0, 1.4))
    if S.name == "line":
        ear = poly([(10.8, 8), (15, 8.4), (16, 13), (15.4, 17), (14, 15.6), (12.6, 18.4), (11.6, 14)], closed=True)
    else:
        ear = "M10.8 8C13.6 7.6 15.6 9.4 15.8 12.6C16 15.4 14.6 18 13.4 18C12.2 17.6 11.6 15 11.2 12.4Z"
    return [shell(union(head, ear)), dot(8.4, 10.6, 0.85), mark(ellipse(2.6, 13.6, 1, 0.8)), detail("M13.4 10.4L13.4 14.8")]


@icon("pharaoh-hound", CAT, "Pharaoh hound head in profile with very large upright ears on a slender long head and neck", tags=["dog breed", "sighthound", "egyptian", "big ears", "pet"])
def _(S):
    head = _prof(S, nx=2, ny=12.8, sx=8.8, sy=9.4, jaw=15.8, neck=11.6, top=8)
    ear = soft(S, [(8.6, 9.2), (9.2, 1.6), (13.8, 3), (14, 8.4)], k=L(S, 0, 1.4))
    return [shell(union(head, ear)), detail(L(S, "M10.4 7.6L11.2 3.8", "M10.6 7.6L11.2 4")), dot(8.4, 11.6, 0.85), mark(ellipse(3, 12.8, 1.1, 0.9))]


@icon("corgi", CAT, "Corgi in side view with a long body on very short legs, large pointed ears and a fluffy rump", tags=["welsh corgi", "dog breed", "short legs", "pet", "herding dog"])
def _(S):
    body = union(ellipse(13.8, 13.4, 7, 3.6), circle(19.8, 13, 2.8) if S.name == "rounded" else soft(S, [(18, 10.6), (22, 12), (21.6, 15.6), (18, 16)], k=0),
                 _dog(S, 5.4, 10.2, ear=None, snout=3.4), thick(seg(6, 11.6, 8.8, 13), 3.8, S))
    ear = soft(S, [(4.6, 8.8), (5.4, 3), (8.6, 8.4)], k=L(S, 0, 0.6))
    return [shell(union(body, ear)), dot(4.8, 9.8, 0.8), *legs((9.4, 12.2, 16.4, 19), 15.6, 20.6)]


@icon("dalmatian", CAT, "Dalmatian standing in side view with a short smooth coat covered in round black spots", tags=["dog breed", "spotted", "firehouse dog", "spots", "pet"])
def _(S):
    ear = soft(S, [(6.8, 6.6), (9.4, 7.8), (8.6, 11.4), (6.8, 10.2)], k=L(S, 0, 0.8))
    body = union(ellipse(13.8, 11.6, 6.4, 3.4), _dog(S, 6, 8.4, ear=None), thick(seg(6.8, 9.8, 9.6, 11.6), 3.6, S))
    tail = taper(((19.6, 10.4), (21.4, 9.4), (21.8, 7), (20.8, 4.8)), 1.8, 2.2)
    return [shell(union(body, tail)), shell(ear), dot(5.6, 8, 0.75), *stride(9.8, 13.6), *stride(17, 13.6), *[dot(x, y, 0.8) for x, y in ((12, 10.4), (15, 12.4), (17, 10.2))]]


@icon("great-dane", CAT, "Great Dane standing tall in side view with a long square muzzle, deep chest and very long legs", tags=["dog breed", "giant dog", "tall", "pet", "mastiff"])
def _(S):
    body = union(ellipse(13.4, 10.4, 6.6, 3.8), _dog(S, 6, 6.2, ear=None, snout=4.2), thick(seg(6.8, 7.6, 9.6, 10), 3.8, S))
    ear = soft(S, [(6.6, 4.4), (9, 5.6), (8.4, 9), (6.6, 7.8)], k=L(S, 0, 0.8))
    return [shell(union(body, ear)), dot(5.4, 5.8, 0.8), *stride(10, 13, 21, 0.4), *stride(17, 13, 21, 0.4), line("M19.8 9C21.4 10.6 21.8 14 21.2 17.4")]


@icon("greyhound", CAT, "Greyhound in side view with a deep narrow chest, a thin tucked waist, long legs and a thin tail", tags=["dog breed", "racing dog", "sighthound", "fast", "slim"])
def _(S):
    body = union(ellipse(9.6, 10.4, 3.8, 3.8), ellipse(17.6, 10.2, 3.2, 2.8), thick(seg(10.6, 9.2, 17, 9.4), 3, S), _dog(S, 5.2, 6.4, ear=None, snout=3.6),
                 thick(seg(5.8, 7.6, 8, 9.4), 3, S))
    return [shell(body), dot(4.8, 6, 0.75), line(seg(7.8, 13.6, 6.8, 21)), line(seg(11, 14, 11.6, 21)), line(seg(16.4, 12.6, 15.4, 21)), line(seg(19.4, 12, 20.6, 21)),
            line("M20.4 9.2C21.6 11 21.8 13.6 21.4 15.6")]


@icon("saint-bernard", CAT, "Saint Bernard in side view, a massive dog with a small rescue barrel hanging under the collar", tags=["dog breed", "rescue dog", "alpine", "barrel", "big dog"])
def _(S):
    body = union(ellipse(14, 12.2, 7.2, 4.6), circle(6, 8.8, 3.2), soft(S, [(5, 7.8), (2.2, 9.8), (2.6, 12), (5.6, 12.4)], k=0.8),
                 thick(seg(9.8, 14.6, 9.8, 20.6), 3, S), thick(seg(17.8, 14.6, 17.8, 20.6), 3, S), thick(seg(6.4, 10, 9.6, 12), 4.4, S))
    ear = soft(S, [(6.6, 5.6), (9.4, 6.8), (9, 11), (6.6, 9.6)], k=L(S, 0, 0.8))
    return [shell(union(body, ear)), dot(4.6, 8.2, 0.8), detail(L(S, "M6.6 10.6L8.2 13", "M6.6 10.6L8 12.8")), shell(circle(5.6, 16, 1.8)), line("M7.4 13L6.6 14.4")]


@icon("shiba-inu", CAT, "Shiba inu in side view with a fox-like face, pointed ears and a tail curled over the back", tags=["dog breed", "japanese dog", "spitz", "curly tail", "japanese spitz"])
def _(S):
    body = union(ellipse(13.2, 13, 6, 3.4), _dog(S, 6, 9.4, ear="up", snout=3.4), thick(seg(6.8, 10.6, 9.4, 12.4), 3.6, S))
    tail = taper(((18.2, 11.2), (21.8, 11.6), (22.2, 6.4), (18.8, 7.4)), 2.2, 3.2)
    return [shell(union(body, tail)), dot(5.6, 9, 0.8), *legs((9.6, 12, 15.6, 18), 15, 20.6)]


@icon("jack-russell-terrier", CAT, "Jack Russell terrier standing in side view with small folded ears, a compact body and an upright tail", tags=["dog breed", "terrier", "parson russell", "energetic", "pet"])
def _(S):
    ear = soft(S, [(6.4, 5.8), (9.2, 6.6), (7.8, 10), (6.4, 9)], k=L(S, 0, 0.8))
    body = union(ellipse(13.4, 12.4, 6, 3.2), _dog(S, 6, 9, ear=None, snout=3.2), thick(seg(6.8, 10.2, 9.4, 11.8), 3.4, S))
    tail = taper(((19.2, 11.2), (20.6, 9.4), (21, 7), (20.6, 4.6)), 1.6, 2)
    return [shell(union(body, tail)), shell(ear), dot(5.4, 8.6, 0.75), *legs((9.6, 12.2, 15.6, 18), 14.4, 20.6), mark(soft(S, [(12, 10.4), (15, 10.2), (14.6, 12.6), (12.6, 12.8)], k=0.6))]


@icon("scottish-terrier", CAT, "Scottish terrier in side view with a boxy low body, a long beard, a pricked ear and an upright tail", tags=["scottie", "dog breed", "terrier", "black dog", "pet"], aliases=["scottie"])
def _(S):
    body = union(rect(7.6, 8.6, 11.8, 6.4, L(S, 2.5, 3.4)), rect(2.4, 6.4, 7.6, 5.8, L(S, 1.2, 2.4)), soft(S, [(2.6, 11), (2.4, 15.6), (6.4, 15.8), (7.6, 12)], k=L(S, 0, 0.8)))
    ear = soft(S, [(6.6, 6.8), (7.4, 2.6), (9.8, 6.8)], k=L(S, 0, 0.6))
    tail = taper(((19.2, 10), (20.6, 8.4), (21.2, 6.4), (21, 4)), 1.8, 2.2)
    return [shell(union(body, ear, tail)), dot(5.2, 8.6, 0.8), mark(ellipse(3.4, 10.2, 1, 0.8)), *legs((9.8, 12.6, 16, 18.4), 14.6, 20.6)]


@icon("bedlington-terrier", CAT, "Bedlington terrier in side view looking like a lamb, with a pear-shaped head, a topknot and an arched back", tags=["dog breed", "terrier", "lamb dog", "curly", "pet"])
def _(S):
    body = union(rot(ellipse(13.4, 10.8, 6.6, 3.2), -6, 13.4, 10.8), _dog(S, 5.8, 8.8, ear=None, snout=3.4), circle(6.6, 5.6, 2), thick(seg(6.6, 10, 9.4, 11.2), 3.6, S))
    ear = soft(S, [(7.4, 7.6), (9.6, 8.6), (8.6, 12.2), (7, 10.6)], k=L(S, 0, 0.8))
    return [shell(union(body, ear)), dot(5.2, 8.4, 0.75), *stride(9.8, 13, 21, 0.6), *stride(16.6, 12.6, 21, 0.6), line("M19.8 9.2C21 10.4 21.4 12.6 21 14.6")]


@icon("pointer-dog", CAT, "Pointer dog in the pointing pose with one front paw raised, body stretched forward and tail straight out", tags=["dog breed", "gundog", "hunting dog", "pointing", "bird dog"])
def _(S):
    body = union(ellipse(13, 10.6, 6.8, 3.2), _dog(S, 4.6, 8.6, ear=None, snout=3.4), thick(seg(5.6, 9.4, 8.6, 10.6), 3.4, S))
    ear = soft(S, [(5, 6.4), (7.4, 7.4), (6.4, 10.6), (4.8, 9)], k=L(S, 0, 0.8))
    return [shell(union(body, ear)), dot(4.2, 8.2, 0.75), line(poly([(8.6, 12), (7.6, 14.2), (10.6, 15.4)], r=S.r)), line(seg(10.6, 13, 10.6, 21)),
            line(seg(15.6, 13, 15.2, 21)), line(seg(18.2, 12.6, 19.4, 21)), line("M19.8 9.8L23 8.6")]


@icon("xoloitzcuintli", CAT, "Hairless Mexican dog in side view with large bat ears, a sleek bare body and a thin tail", tags=["xolo", "mexican hairless dog", "dog breed", "hairless", "aztec"], aliases=["xolo"])
def _(S):
    ear = soft(S, [(5, 6.8), (5.8, 2.6), (9.6, 6.8)], k=L(S, 0, 0.8))
    body = union(ellipse(13.4, 11.8, 6.2, 3), _dog(S, 6, 8.8, ear=None, snout=3.4), thick(seg(6.8, 10, 9.4, 11.4), 3.2, S))
    return [shell(union(body, ear)), dot(5.4, 8.4, 0.75), *stride(9.8, 13.4, 21, 0.6), *stride(16.6, 13.4, 21, 0.6), line("M19.4 11C21 12.4 21.6 15 21 18")]


@icon("irish-setter", CAT, "Irish setter in side view with a long feathered coat on the ears, chest, legs and tail", tags=["red setter", "dog breed", "gundog", "feathered", "pet"])
def _(S):
    if S.name == "line":
        chest = poly([(8, 13), (12, 15.4), (10.6, 16.4), (13.6, 18), (8.2, 16.8), (6.6, 15)], closed=True)
    else:
        chest = union(ellipse(9.6, 15, 2.4, 2.6), circle(11.6, 16.6, 1.4))
    body = union(ellipse(13.6, 11.2, 6.4, 3.2), _dog(S, 6, 8.2, ear=None, snout=3.8), thick(seg(6.8, 9.4, 9.6, 11), 3.4, S), chest)
    ear = soft(S, [(6.8, 6.4), (9.8, 7.6), (9.4, 13), (7, 11.6)], k=L(S, 0, 1))
    tail = taper(((19.4, 10.2), (21.6, 11.4), (21.6, 15.4), (20, 19)), 1.6, 3.6)
    return [shell(union(body, ear, tail)), dot(5.4, 7.8, 0.75), *stride(10.6, 14.4, 21, 0.4), *stride(17, 13.8, 21, 0.4)]


@icon("airedale-terrier", CAT, "Airedale terrier in side view with a long flat head, a wiry beard, folded ears and a square stance", tags=["dog breed", "terrier", "wiry", "beard", "pet"])
def _(S):
    body = union(rect(8.4, 8.6, 11, 6, L(S, 2, 3)), rect(2.4, 5.8, 8.2, 5, L(S, 1, 2.2)), soft(S, [(2.6, 9.8), (2.4, 14.4), (6.6, 14.6), (8, 10.8)], k=L(S, 0, 0.8)),
                 thick(seg(8, 8.6, 9, 12), 3.6, S))
    ear = soft(S, [(6.8, 4.8), (9.8, 6), (8.6, 9.2), (6.4, 7.8)], k=L(S, 0, 0.8))
    tail = taper(((19.2, 10), (20.6, 8.4), (21.2, 6.2), (21, 3.6)), 1.8, 2.2)
    return [shell(union(body, ear, tail)), dot(4.8, 8, 0.75), mark(ellipse(3.4, 9.2, 1, 0.8)), *legs((10, 12.4, 16.2, 18.6), 14.4, 21)]


@icon("border-collie", CAT, "Border collie in a low herding crouch with its head down, a white face blaze and a low tail", tags=["collie", "dog breed", "sheepdog", "herding dog", "crouch"])
def _(S):
    body = union(rot(ellipse(13.4, 12.4, 6.6, 3), 10, 13.4, 12.4), circle(5.4, 12.8, 2.6), soft(S, [(4.4, 11.4), (1.8, 14), (2.4, 15.6), (5.6, 15.4)], k=0.8),
                 thick(seg(6.4, 13, 9, 12.6), 3.4, S))
    ear = soft(S, [(5.6, 10.6), (6.4, 8), (8.4, 10.8)], k=L(S, 0, 0.6))
    tail = taper(((19.4, 13.6), (21, 15.2), (21.6, 17.4), (20.6, 19.6)), 1.8, 3.2)
    return [shell(union(body, ear, tail)), dot(4.8, 12.2, 0.75), mark(ellipse(2.8, 14.4, 0.9, 0.7)), *stride(10.2, 14.2, 21, 1.0), *stride(17, 15, 21, 0.6)]


@icon("chinese-crested", CAT, "Chinese crested dog with a hairless body, a long silky crest on the head, fringed ears and a plumed tail", tags=["dog breed", "hairless", "powderpuff", "crest", "pet"])
def _(S):
    body = union(ellipse(13.4, 12.4, 6, 3), _dog(S, 6, 9.6, ear=None, snout=3.2), thick(seg(6.8, 10.8, 9.4, 12), 3, S))
    ear = soft(S, [(4.8, 8), (5.6, 2.8), (8.6, 8)], k=L(S, 0, 0.6))
    crest = soft(S, [(6.6, 7.8), (8.6, 4.4), (12, 2.6), (11, 6), (9.6, 8.6)], k=L(S, 0, 1))
    plume = taper(((19.2, 11.2), (21, 13), (21.6, 15.4), (20.8, 18.6)), 1.2, 4)
    return [shell(union(body, ear, crest, plume)), dot(5.4, 9.2, 0.75), *legs((9.8, 12.2, 16, 18.2), 14.6, 19.2),
            *[shell(ellipse(x, 20.4, 1.3, 1.1)) for x in (9.8, 12.2, 16, 18.2)]]


# =========================================================================== bears and small carnivores

def cub(c):
    return "M" + _p(c[0]) + "C" + " ".join(_p(q) for q in c[1:])


def across(c, t, half):
    x, y = bez(*c, t)
    x2, y2 = bez(*c, min(1, t + 1e-3))
    x1, y1 = bez(*c, max(0, t - 1e-3))
    dx, dy = x2 - x1, y2 - y1
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln
    return seg(x + nx * half, y + ny * half, x - nx * half, y - ny * half)


@icon("polar-bear", CAT, "Polar bear walking in side view with a long neck, small head, small ears and a large rounded body", tags=["arctic", "bear", "ice", "north pole", "wildlife"])
def _(S):
    head = union(circle(5.4, 7.8, 2.4), soft(S, [(4.6, 6.6), (1.6, 9.2), (2, 10.6), (5.4, 10.6)], k=0.8), circle(7.4, 5.6, 1.1))
    body = union(ellipse(14.8, 12.6, 6.8, 4.2), head, thick(seg(6.4, 9, 10.2, 11.6), 3.4, S),
                 thick(seg(10.6, 15, 10.6, 20.6), 3.2, S), thick(seg(13, 15.6, 13, 20.6), 3.2, S), thick(seg(17.6, 15.6, 17.6, 20.6), 3.2, S), thick(seg(20, 14, 20, 20.6), 3.2, S))
    return [shell(body), dot(4.8, 7.4, 0.75), mark(ellipse(2.4, 9.4, 0.9, 0.7))]


@icon("sun-bear", CAT, "Sun bear standing upright with short sleek fur, small round ears and a U-shaped crescent patch on the chest", tags=["malayan bear", "bear", "honey bear", "rainforest", "wildlife"])
def _(S):
    head = union(circle(12, 6.6, 3.8), circle(8.4, 3.8, 1.5), circle(15.6, 3.8, 1.5))
    body = union(ellipse(12, 15.2, 5.6, 5.6), thick(seg(6.8, 13, 5.6, 17), 3, S), thick(seg(17.2, 13, 18.4, 17), 3, S))
    return [shell(union(head, body)), *eyes(6, 1.8, 0.8), mark(ellipse(12, 8, 1.5, 1)), detail("M8.6 13.6Q12 19.2 15.4 13.6")]


@icon("sloth-bear", CAT, "Sloth bear in side view with a shaggy mane, a long pale snout and long curved front claws", tags=["bear", "shaggy", "india", "claws", "wildlife"])
def _(S):
    head = union(circle(6.6, 9.6, 2.8), soft(S, [(5.6, 8.4), (1.6, 11.4), (2.2, 13), (6.2, 13.2)], k=0.8), circle(8.2, 7, 1.2))
    if S.name == "line":
        mane = poly([(8, 7.6), (9.4, 5.6), (11, 7.4), (12.6, 5.4), (14, 7.6), (16.4, 6.6), (18, 9), (20.6, 10.4), (20.4, 14.6), (9.6, 15)], closed=True)
    else:
        mane = union(ellipse(14, 11, 6.6, 4), circle(10.4, 7.6, 1.6), circle(13, 7.2, 1.6), circle(15.6, 7.6, 1.6))
    body = union(mane, head, thick(seg(8.6, 15, 8.6, 20), 3, S), thick(seg(17, 14.6, 17, 20), 3, S))
    return [shell(body), dot(5.8, 9.2, 0.75), mark(ellipse(2.8, 12, 0.9, 0.7)), line("M5.4 18C6.6 19.8 8.4 20.2 9.4 20"), line("M14.4 18C15.6 19.8 17 20.2 18 20")]


@icon("spectacled-bear", CAT, "Spectacled bear face with pale rings around the eyes like glasses on a dark round head", tags=["andean bear", "bear", "glasses", "south america", "wildlife"])
def _(S):
    head = union(circle(12, 12.4, 7.6), circle(6.6, 5.8, 2.4), circle(17.4, 5.8, 2.4))
    return [shell(head), detail(circle(9, 11, 2.5)), detail(circle(15, 11, 2.5)), detail(seg(11.4, 11, 12.6, 11)), dot(9, 11, 0.8), dot(15, 11, 0.8),
            mark(ellipse(12, 16, 2.2, 1.6))]


@icon("red-panda", CAT, "Red panda sitting on a branch with a white-marked face, pointed ears and a thick ringed tail", tags=["lesser panda", "red bear-cat", "himalaya", "bamboo", "wildlife"])
def _(S):
    ear = soft(S, [(6.4, 6.4), (6.6, 2.4), (10, 4.6)], k=L(S, 0, 0.6))
    head = union(circle(9, 8.4, 3.8), ear, flip2(ear, 18))
    body = ellipse(9, 15.6, 4.2, 4)
    c = ((12.8, 16.2), (19, 18), (22, 12), (18.4, 6.4))
    tail = taper(c, 3.6, 4.6)
    return [line(seg(2, 20.6, 22, 20.6)), shell(union(head, body)), shell(tail), dot(7.6, 8, 0.85), dot(10.8, 8, 0.85), mark(ellipse(9.2, 10.2, 1.2, 0.8)),
            *[detail(across(c, t, 2.0)) for t in (0.3, 0.52, 0.74)]]


def flip2(d, w):
    """Mirror a d-string across the vertical line x = w / 2."""
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, w, 0)))


@icon("weasel", CAT, "Weasel standing up on its hind legs with a long thin body, short legs, small round ears and a short tail", tags=["stoat", "ermine", "mustelid", "predator", "wildlife"])
def _(S):
    head = union(circle(12, 5.8, 2.8), circle(9.6, 4, 1.1), circle(14.4, 4, 1.1))
    body = ellipse(12, 13.2, 3, 6.4)
    return [shell(union(head, body)), dot(11, 5.6, 0.7), dot(13, 5.6, 0.7), line("M9.4 10.4L8 13"), line("M14.6 10.4L16 13"), line(seg(10.6, 19, 10, 21.2)), line(seg(13.4, 19, 14, 21.2)),
            line("M14.6 18.4C17 17.6 19 18 20.4 19.6")]


@icon("badger", CAT, "Badger face with bold black and white stripes running from the nose over the eyes to the ears", tags=["european badger", "stripes", "woodland", "sett", "wildlife"])
def _(S):
    head = union(ellipse(12, 12.6, 7.2, 7.6), circle(6, 5.8, 1.9), circle(18, 5.8, 1.9)) if S.name == "rounded" else \
        poly([(7.6, 5.6), (16.4, 5.6), (19.6, 10), (19, 16), (15, 20.4), (9, 20.4), (5, 16), (4.4, 10)], closed=True)
    band = minus(soft(S, [(6.6, 7), (10.6, 6), (10.4, 15.6), (8.8, 17.4), (6, 14)], k=L(S, 0, 0.8)), circle(8.4, 11.4, 0.9))
    return [shell(head), mark(band), mark(minus(flip(soft(S, [(6.6, 7), (10.6, 6), (10.4, 15.6), (8.8, 17.4), (6, 14)], k=L(S, 0, 0.8))), circle(15.6, 11.4, 0.9))),
            mark(ellipse(12, 17.6, 1.6, 1))]


@icon("honey-badger", CAT, "Honey badger in side view with a low stocky dark body and a pale grey mantle from head to tail", tags=["ratel", "badger", "africa", "fearless", "wildlife"])
def _(S):
    body = union(ellipse(13.4, 12.6, 7.6, 3.6), circle(5, 11, 2.6), soft(S, [(4.2, 9.8), (1.8, 12), (2.4, 13.6), (5, 13.6)], k=0.8), thick(seg(5.6, 11.6, 8.4, 12.4), 3.4, S),
                 circle(6.4, 8.8, 1.1))
    belly = D(P(ellipse(13.4, 12.6, 7.6, 3.6)), P(rect(4, 6, 20, 7.6)))
    return [shell(body), mark(path_to_d(belly)), dot(4.4, 10.6, 0.7), *legs((8.6, 11.6, 16.6, 19), 15, 20.6), line("M21 11.6L22 13")]


@icon("wolverine", CAT, "Wolverine in side view with a stocky bear-like body, a pale side stripe and a short bushy tail", tags=["glutton", "mustelid", "north", "tough", "wildlife"])
def _(S):
    body = union(ellipse(12.6, 11.6, 6.8, 4), circle(5.6, 9.6, 2.6), soft(S, [(4.8, 8.4), (2, 10.6), (2.4, 12.2), (5.4, 12.4)], k=0.8), circle(7.2, 7.2, 1.1),
                 thick(seg(6.4, 10.4, 9.4, 11.6), 3.4, S), taper(((18.4, 10.6), (20.6, 11.4), (21.6, 13.4), (21.2, 16)), 2.4, 3.6))
    return [shell(body), dot(4.8, 9, 0.75), mark(ellipse(2.8, 10.8, 0.8, 0.7)), detail("M8.8 13.4C11.4 10.6 15.4 10.4 18.4 12.6"), *legs((9, 11.8, 15.6, 18), 15, 20.6)]


@icon("skunk", CAT, "Skunk in side view with a white stripe down its back and a large bushy tail raised over its body", tags=["stink", "spray", "stripes", "north america", "wildlife"])
def _(S):
    tail = rot(ellipse(17, 8.6, 3.6, 6.6) if S.name == "rounded" else "M17 1.8L20.6 8.6L17 15.4L13.4 8.6Z", 18, 17, 8.6)
    body = union(ellipse(10, 15, 6, 3.6), circle(4.6, 13.4, 2.4), soft(S, [(3.8, 12.2), (1.6, 14), (2.2, 15.6), (4.6, 15.8)], k=0.6), thick(seg(5.2, 14, 7.6, 15), 3, S))
    return [shell(union(body, tail)), dot(4.2, 13, 0.7), detail("M7.2 12.8C9.4 11.8 12 11.8 14.2 12.8"), detail("M16 14C17.6 11 18 7.6 17 4.4"), *legs((7.6, 10.4, 13.4), 17.6, 20.8)]


@icon("ferret", CAT, "Ferret in a stretched side view with a long slinky body, a masked face and short legs", tags=["polecat", "pet", "mustelid", "slinky", "weasel"])
def _(S):
    c = ((7, 13), (10.6, 8.6), (14.4, 17.4), (19, 12.6))
    body = union(thick(cub(c), 4.4, S), circle(5, 12.4, 2.6), soft(S, [(4.2, 11.2), (2, 13.2), (2.6, 14.6), (5, 14.8)], k=0.6), circle(6.6, 9.8, 1.1))
    return [shell(body), dot(4.4, 11.8, 0.7), mark(ellipse(4.4, 11.8, 1.5, 1.2)) if False else dot(2.8, 13.2, 0.6), line(seg(8.6, 15.4, 8.6, 20)), line(seg(11.4, 15, 11.4, 20)),
            line(seg(15.6, 16, 15.6, 20)), line(seg(18.2, 14.6, 18.4, 20)), line("M20.6 11.8C21.6 11 22 10 21.8 9")]


@icon("mongoose", CAT, "Mongoose in side view with a slim long body, a pointed face, small ears and a long tapering tail", tags=["snake hunter", "snake fighter", "meerkat", "africa", "wildlife"])
def _(S):
    body = union(rot(ellipse(11.8, 12.6, 6, 2.8), -6, 11.8, 12.6), circle(5.2, 10.6, 2.4), soft(S, [(4.6, 9.4), (1.8, 11.4), (2.4, 12.8), (5.2, 13)], k=0.6),
                 circle(6.8, 8.4, 1.1), thick(seg(5.8, 11.4, 8.4, 12), 3, S))
    tail = taper(((17.4, 11.4), (20.4, 11.6), (21.6, 14), (20.6, 18.4)), 2.4, 0.8)
    return [shell(union(body, tail)), dot(4.6, 10.2, 0.7), *stride(8.8, 14.4, 20.6, 0.8), *stride(14.8, 14.4, 20.6, 0.8)]


@icon("meerkat", CAT, "Meerkat standing upright on its hind legs on sentry duty, with dark eye patches and paws held at the chest", tags=["suricate", "sentry", "africa", "desert", "wildlife"])
def _(S):
    head = union(ellipse(12, 6.2, 3, 3.4), soft(S, [(11, 6.6), (12, 10), (13, 6.6)], k=0.4) if False else ellipse(12, 8, 1.6, 1.6))
    body = ellipse(12, 14.4, 3.8, 5.6)
    return [shell(union(head, body)), mark(ellipse(10.6, 5.6, 1.1, 1.3)), mark(ellipse(13.4, 5.6, 1.1, 1.3)), mark(ellipse(12, 8.2, 0.9, 0.7)),
            line("M9.2 12.4L10.6 14.6"), line("M14.8 12.4L13.4 14.6"), line(seg(10.4, 19.4, 9.6, 21.4)), line(seg(13.6, 19.4, 14.4, 21.4)), line("M15.6 18.4C18 18.4 20 19 21 20.6")]


@icon("genet", CAT, "Genet in side view with a slender spotted body, a pointed face, large ears and a long ringed tail", tags=["spotted", "civet", "africa", "nocturnal", "wildlife"])
def _(S):
    c = ((14.6, 11.4), (18, 9.2), (21.4, 11), (21.4, 16))
    body = union(ellipse(10.4, 12.2, 5.6, 2.6), circle(4.6, 10, 2.3), soft(S, [(4, 8.8), (1.6, 10.8), (2.2, 12.2), (4.6, 12.4)], k=0.6),
                 soft(S, [(4.6, 8.2), (5.4, 4.6), (7.6, 8)], k=L(S, 0, 0.5)), thick(seg(5, 10.8, 7.6, 11.8), 2.8, S))
    return [shell(union(body, thick(cub(c), 2.8, S))), dot(4, 9.6, 0.7), dot(9.4, 11, 0.6), dot(12, 12.6, 0.6), *[detail(across(c, t, 1.4)) for t in (0.5, 0.74)],
            *legs((7.4, 13), 14, 19), *legs((15,), 13, 19)]


@icon("binturong", CAT, "Binturong on a branch with shaggy fur, tufted ears, long whiskers and a prehensile tail wrapped around", tags=["bearcat", "asia", "prehensile tail", "popcorn", "wildlife"])
def _(S):
    body = ellipse(12.4, 14, 5.6, 4.2)
    head = union(circle(6.4, 10.6, 3.2), soft(S, [(4.8, 8.4), (4.6, 4.4), (8.2, 7.6)], k=L(S, 0, 0.5)), soft(S, [(8, 8), (10, 4.8), (10.8, 9)], k=L(S, 0, 0.5)))
    c = ((17, 14.4), (21.8, 13.4), (21.8, 19.4), (17, 19.4))
    return [line(seg(2, 19.6, 22, 19.6)), shell(union(body, head)), line(cub(c)), dot(5.6, 10, 0.75), mark(ellipse(3.6, 11.8, 0.8, 0.7)), line(seg(3.2, 13.4, 1.4, 14.2)), line(seg(9.4, 17, 9.4, 19.6)), line(seg(14.2, 17.6, 14.2, 19.6))]


@icon("fossa", CAT, "Fossa in side view with a sleek cat-like body, rounded ears, a short muzzle and a very long tail", tags=["madagascar", "predator", "cat-like", "long tail", "wildlife"])
def _(S):
    body = union(ellipse(11, 11.4, 6.2, 3), circle(5, 9.8, 2.6), circle(6.6, 7.4, 1.1), thick(seg(5.8, 10.6, 8.2, 11.4), 3.2, S))
    tail = taper(((16.6, 10.4), (21.6, 8.4), (22, 14), (19.8, 20)), 2, 1.4)
    return [shell(union(body, tail)), dot(4.4, 9.4, 0.7), mark(ellipse(2.6, 11, 0.8, 0.7)), *stride(8.6, 13.4, 20.6, 0.6), *stride(14.4, 13.4, 20.6, 0.6)]


@icon("kinkajou", CAT, "Kinkajou hanging by a prehensile tail from a branch with a round face, big eyes and small ears", tags=["honey bear", "rainforest", "prehensile tail", "nocturnal", "wildlife"])
def _(S):
    head = union(circle(8.6, 12, 3.6), circle(5.8, 8.8, 1.3), circle(11.6, 8.6, 1.3))
    body = union(ellipse(12.6, 15.8, 3.4, 4.4), thick(seg(10, 13.8, 11.6, 16), 3, S))
    c = ((15, 17), (20.4, 17), (20.4, 8), (16.6, 3.4))
    return [line(seg(2, 3.2, 22, 3.2)), shell(union(head, body)), line(cub(c)), dot(7, 11.6, 1.05), dot(10.2, 11.6, 1.05), mark(ellipse(8.6, 14, 1, 0.7)),
            line(seg(12.2, 20, 11.6, 21)), line(seg(14.4, 19.8, 15, 21))]


@icon("coati", CAT, "Coati walking in side view with a long upturned pointed snout and a banded tail held straight up", tags=["coatimundi", "south america", "ringtail", "snout", "wildlife"])
def _(S):
    c = ((18.4, 12), (20.6, 9.6), (20.6, 6.4), (19.4, 3.6))
    body = union(ellipse(12.4, 13.4, 6, 3), circle(5.4, 11.4, 2.4), soft(S, [(4.8, 10.2), (1.6, 8.6), (1.6, 10.4), (4.6, 13.2)], k=0.5), circle(7, 9.2, 1.1),
                 thick(seg(6, 12, 8.6, 13), 3, S))
    return [shell(union(body, taper(c, 3.4, 3))), dot(5, 10.8, 0.7), *[detail(across(c, t, 1.9)) for t in (0.3, 0.55, 0.8)], *stride(9.4, 15.4, 20.6, 0.8), *stride(15, 15.4, 20.6, 0.8)]


# =========================================================================== rodents and rabbits

@icon("capybara", CAT, "Capybara sitting in side view with a large barrel body, a blunt square head, small ears and no tail", tags=["rodent", "south america", "water pig", "largest rodent", "wildlife"])
def _(S):
    body = union(ellipse(14, 13.4, 7.6, 4.8), rect(2.2, 8.4, 8.4, 6.4, L(S, 2, 3)), thick(seg(10, 16, 10, 20.4), 3.2, S), thick(seg(18, 16, 18, 20.4), 3.2, S), circle(9, 7.8, 1.2))
    return [shell(body), dot(5.6, 10.8, 0.8), mark(ellipse(3.6, 11.8, 0.9, 1.2)), detail(L(S, "M3.6 14.2L6.6 14.2", "M3.6 14L6.6 14"))]


@icon("porcupine", CAT, "Porcupine in side view with long sharp quills fanning up and back from its body", tags=["rodent", "quills", "spines", "prickly", "wildlife"])
def _(S):
    body = union(ellipse(12.4, 15.4, 6.6, 3.8), circle(5.2, 15.4, 2.4), soft(S, [(4.4, 14.4), (2, 16), (2.4, 17.6), (5, 17.8)], k=0.6), thick(seg(5.6, 16, 8, 16), 3, S))
    quills = []
    for a in range(-150, -20, 18):
        p0 = (12.6 + 6.4 * math.cos(math.radians(a)), 15.4 + 3.2 * math.sin(math.radians(a)))
        p1 = (12.6 + 10.4 * math.cos(math.radians(a)), 15.4 + 10.2 * math.sin(math.radians(a)))
        quills.append(line(seg(p0[0], p0[1], p1[0], p1[1])))
    return [shell(body), *quills, dot(4.6, 15, 0.75), *legs((8.4, 11.6, 15.6, 18.2), 18.4, 20.6)]


@icon("flying-squirrel", CAT, "Flying squirrel gliding seen from above with skin membranes stretched between its front and back legs and a flat tail", tags=["glider", "squirrel", "gliding", "rodent", "nocturnal"])
def _(S):
    wing = soft(S, [(2.4, 8.6), (9.6, 10), (9.6, 16), (3.6, 18.4)], k=L(S, 0, 1.2))
    body = union(ellipse(12, 12.4, 2.6, 4.4), circle(12, 6.6, 2.8), circle(9.8, 4.4, 1.1), circle(14.2, 4.4, 1.1), rect(10.4, 15.6, 3.2, 5.4, L(S, 0.8, 1.6)))
    return [shell(union(body, wing, flip(wing))), dot(11, 6.4, 0.7), dot(13, 6.4, 0.7)]


@icon("prairie-dog", CAT, "Prairie dog standing upright at the mouth of a burrow mound with small paws held together", tags=["rodent", "burrow", "sentry", "north america", "wildlife"])
def _(S):
    mound = "M2.4 21C3.6 17.4 7.6 16 12 16C16.4 16 20.4 17.4 21.6 21Z"
    anim = union(circle(12, 6.6, 3.6), circle(8.6, 4.2, 1.2), circle(15.4, 4.2, 1.2), ellipse(12, 12.4, 3.6, 4.8))
    return [shell(minus(anim, grow(mound, 1.8))), shell(mound), dot(10.8, 6.2, 0.75), dot(13.2, 6.2, 0.75), mark(ellipse(12, 8.2, 1, 0.7)), detail("M10.2 12L12 13.6L13.8 12")]


@icon("groundhog", CAT, "Groundhog peeking up out of a round burrow hole with a stout body and small ears", tags=["woodchuck", "marmot", "burrow", "groundhog day", "rodent"], aliases=["woodchuck"])
def _(S):
    hole = ellipse(12, 19, 8.6, 2.6)
    anim = union(ellipse(12, 9.6, 5.6, 5), circle(7.2, 5.4, 1.4), circle(16.8, 5.4, 1.4), ellipse(12, 15, 6, 4))
    return [shell(minus(anim, grow(hole, 2))), shell(hole), dot(9.6, 9, 0.85), dot(14.4, 9, 0.85), mark(ellipse(12, 11.6, 1.5, 1)), detail("M10.6 13.6L13.4 13.6") if False else detail(L(S, "M10.4 13.4L13.6 13.4", "M10.4 13.2Q12 14.2 13.6 13.2"))]


@icon("gopher", CAT, "Pocket gopher popping out of a dirt mound with big front teeth and bulging cheek pouches", tags=["rodent", "burrow", "mound", "cheek pouches", "garden pest"])
def _(S):
    mound = "M2.4 21C3.8 17 7.6 15.8 12 15.8C16.4 15.8 20.2 17 21.6 21Z"
    anim = union(ellipse(12, 10, 7.2, 5.4), circle(6.6, 5.6, 1.3), circle(17.4, 5.6, 1.3))
    return [shell(minus(anim, grow(mound, 1.6))), shell(mound), dot(9.4, 8.6, 0.8), dot(14.6, 8.6, 0.8), mark(ellipse(12, 10.6, 1.4, 0.9)),
            detail(rect(10.4, 12.4, 1.6, 2.2, 0.4)) if False else mark(rect(10.4, 12, 1.4, 2.2, 0.3)), mark(rect(12.2, 12, 1.4, 2.2, 0.3))]


@icon("chipmunk", CAT, "Chipmunk sitting with stripes down its back and face and cheeks stuffed full", tags=["rodent", "striped", "cheeks", "acorn", "woodland"])
def _(S):
    c = ((14.4, 16.4), (20.4, 17), (21.6, 9.6), (17, 5.4))
    head = union(circle(7.6, 8.4, 3.6), circle(6.2, 10.4, 2.2), circle(5.6, 5.2, 1.2), circle(9.6, 5, 1.2))
    body = union(ellipse(10.6, 15, 4.8, 5.2), head)
    return [shell(union(body, taper(c, 3.4, 4.4))), dot(6.4, 8, 0.75), mark(ellipse(4.4, 9.6, 0.8, 0.7)), detail("M8.6 4.8L9.6 7.2") if False else detail("M11.8 11C13.6 13 14.2 16 13.4 19.4"),
            detail("M10.4 11.8C11.6 14 11.8 16.4 11.2 19"), line(seg(8.4, 19.6, 8.4, 21)), line(seg(12.6, 20, 12.6, 21))]


@icon("naked-mole-rat", CAT, "Naked mole rat with wrinkled hairless skin, tiny eyes and two long buck teeth sticking out", tags=["hairless", "burrowing", "rodent", "wrinkled", "africa"])
def _(S):
    body = union(ellipse(13, 13.6, 8, 4.2), ellipse(6, 13.2, 4, 3.4))
    return [shell(body), mark(rect(1.2, 13, 2.6, 1.3, 0.4)), mark(rect(1.2, 14.8, 2.6, 1.3, 0.4)) if False else mark(rect(1.2, 15, 2.6, 1.2, 0.4)), dot(6, 11.6, 0.6),
            detail("M10.4 10.6Q11.6 13.6 10.4 16.4"), detail("M14 9.8Q15.2 13.6 14 17.4"), line(seg(9, 17.6, 9, 20)), line(seg(16.4, 17.6, 16.4, 20)), line("M21 13.4C21.6 14.4 21.8 15.4 21.6 16.6")]


@icon("jerboa", CAT, "Jerboa standing on very long kangaroo-like hind legs, with huge ears and a long tail ending in a tuft", tags=["desert rodent", "hopping", "big ears", "long legs", "africa"])
def _(S):
    ear1 = rot(ellipse(10.4, 4.4, 1.3, 3) if S.name == "rounded" else "M10.4 2.6L11.8 5L10.4 7.4L9 5Z", 16, 10.4, 4.4)
    ear2 = rot(ellipse(6.2, 4.4, 1.3, 3) if S.name == "rounded" else "M6.2 2.6L7.6 5L6.2 7.4L4.8 5Z", -16, 6.2, 4.4)
    body = union(circle(8.2, 9, 2.8), ellipse(11.2, 13.4, 3.2, 3.4), ear1, ear2)
    tuft = ellipse(21, 8.4, 1.3, 2.2)
    return [shell(union(body, tuft)), dot(7.4, 8.6, 0.7), line(poly([(12, 16), (14.4, 18.6), (12.2, 21)], r=S.r)), line(poly([(9.8, 16), (9.6, 18.6), (7.8, 21)], r=S.r)), line("M14 13C16.6 13 19 12 20.6 9.8")]


@icon("chinchilla", CAT, "Chinchilla sitting with large round ears, a round fluffy body and a bushy tail curled up behind", tags=["rodent", "fluffy", "pet", "soft fur", "andes"])
def _(S):
    c = ((15.8, 16), (21.4, 16), (21.6, 9), (17.2, 6.2))
    head = union(circle(7.6, 9, 3.4), ellipse(6.4, 4.6, 1.6, 2.6) if S.name == "rounded" else soft(S, [(5, 6), (6.4, 2.4), (8, 6)], k=0), ellipse(10.4, 4.8, 1.6, 2.6) if S.name == "rounded" else soft(S, [(9.2, 6), (10.6, 2.4), (12.2, 6)], k=0))
    body = union(circle(11.4, 15, 5.6), head)
    return [shell(union(body, taper(c, 3.6, 4.6))), dot(6.4, 8.6, 0.8), mark(ellipse(4.6, 10.2, 0.8, 0.7)), line(seg(9, 20.6, 9, 21.2)) if False else line(seg(9.4, 20, 8.4, 21)), line(seg(13.6, 20.4, 14.4, 21))]


@icon("pika", CAT, "Pika sitting as a small round ball with rounded ears and no visible tail", tags=["rock rabbit", "ochotona", "mountain", "small mammal", "alpine"])
def _(S):
    body = union(ellipse(12, 13.8, 7.4, 6.2), circle(7.4, 6.6, 2.6), circle(15.4, 6.6, 2.6))
    return [shell(body), *eyes(11.6, 3.6, 0.95), mark(ellipse(12, 14, 1.5, 1)), detail("M12 15L12 16.2") if False else detail(L(S, "M10.2 16.6Q12 17.8 13.8 16.6", "M10.2 16.6Q12 17.8 13.8 16.6"))]


@icon("lop-rabbit", CAT, "Lop-eared rabbit sitting with long ears hanging down both sides of its face", tags=["bunny", "pet", "floppy ears", "rabbit breed", "hare"])
def _(S):
    ear = soft(S, [(8.8, 4.4), (5, 5.6), (4, 11), (4.6, 15), (7.2, 13.8), (8.4, 9)], k=L(S, 0, 2))
    body = union(circle(12, 9, 4.4), ellipse(12, 17, 5, 4))
    return [shell(union(body, ear, flip(ear))), *eyes(8.6, 2.2, 0.85), mark(soft(S, [(11, 10.8), (13, 10.8), (12, 12)], k=0.4)), detail("M12 12L12 13.4") if False else detail(L(S, "M10.6 13Q12 13.8 13.4 13", "M10.6 13Q12 13.8 13.4 13"))]
