"""TypeIcon Core: animals."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "animals"


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
    """Outline of a stroke of width w along d (for limbs, trunks, necks inside a silhouette)."""
    return path_to_d(ST(d, w, S.cap, S.join))


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    x = u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0]
    y = u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]
    return x, y


def tube(ctrl, width, n=48):
    """Closed outline around a cubic centreline whose width varies with t (width(t) -> px)."""
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x, y = bez(*ctrl, t)
        x2, y2 = bez(*ctrl, min(1, t + 1e-3))
        x1, y1 = bez(*ctrl, max(0, t - 1e-3))
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy)
        nx, ny = -dy / ln, dx / ln
        w = width(t) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return left + right[::-1]


def flip(d):
    """Mirror a d-string across the vertical centre line."""
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def grow(d, g):
    """Region d expanded by g px (used to cut clean gaps between overlapping parts)."""
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def mark(d):
    """Small solid mark (nose, patch). Solid in stroke styles, knocked out of a Filled body."""
    return Part("dot", d)


def _p(p):
    return f"{fmt(p[0])} {fmt(p[1])}"


def tip(a, p, b, r):
    """Corner at p (coming from a, leaving towards b): sharp when r == 0, softened with a quadratic when r > 0."""
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


def leaf(cx, top, bottom, w):
    """Vertical leaf / pointed oval from top to bottom, width w."""
    my = (top + bottom) / 2
    k = w * 0.66
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + k)} {fmt(top + (my - top) * 0.35)} {fmt(cx + k)} {fmt(bottom - (bottom - my) * 0.35)} {fmt(cx)} {fmt(bottom)}"
            f"C{fmt(cx - k)} {fmt(bottom - (bottom - my) * 0.35)} {fmt(cx - k)} {fmt(top + (my - top) * 0.35)} {fmt(cx)} {fmt(top)}Z")


# --------------------------------------------------------------------------- pets and farm

@icon("cat", CAT, "Cat face with pointed ears", tags=["kitten", "pet", "feline", "animal", "meow"])
def _(S):
    r = L(S, 0, 1.8)
    d = ("M10 7.2Q12 6.6 14 7.2" + tip((14, 7.2), (19, 4), (19.8, 10), r) + "L19.8 10"
         "C20.8 15.5 17 20 12 20C7 20 3.2 15.5 4.2 10" + tip((4.2, 10), (5, 4), (10, 7.2), r) + "Z")
    return [shell(d), dot(9, 12.5), dot(15, 12.5), mark(poly([(10.6, 15), (13.4, 15), (12, 16.6)], closed=True, r=L(S, 0, 0.5)))]


@icon("dog", CAT, "Dog face with floppy ears", tags=["puppy", "pet", "canine", "animal", "hound"])
def _(S):
    r = L(S, 0, 1.5)
    d = ("M8 4.8C10 3.8 14 3.8 16 4.8C18.5 4 20.8 5.5 20.6 8.5"
         + tip((20.6, 8.5), (20.2, 14), (17.5, 12.5), r) + tip((20.2, 14), (17.5, 12.5), (17.5, 16), r)
         + "L17.5 16C17.5 19 15 20.5 12 20.5C9 20.5 6.5 19 6.5 16"
         + tip((6.5, 16), (6.5, 12.5), (3.8, 14), r) + tip((6.5, 12.5), (3.8, 14), (3.4, 8.5), r)
         + "L3.4 8.5C3.2 5.5 5.5 4 8 4.8Z")
    return [shell(d), detail("M16.2 6.2C17.2 8 17.5 10 17.5 12.5"), detail("M7.8 6.2C6.8 8 6.5 10 6.5 12.5"),
            dot(10, 10.5), dot(14, 10.5), mark(ellipse(12, 14.8, 2, 1.4))]


@icon("bird", CAT, "Small songbird in side view", tags=["songbird", "sparrow", "tweet", "animal", "wildlife"])
def _(S):
    r = L(S, 0, 1.2)
    d = ("M15 4.5C17 4.5 18.5 5.8 18.8 7.4" + tip((18.8, 7.4), (21.5, 8.6), (18.7, 9.9), r)
         + "L18.7 9.9C18.5 14.5 15.5 18 11 18.3" + tip((11, 18.3), (3.5, 19.5), (7.8, 14.3), r)
         + "L7.8 14.3C10 12.5 11 10.5 11.3 8.5C11.6 6 13 4.5 15 4.5Z")
    return [shell(d), detail("M9.5 15.5C12.5 15.5 14.8 13.5 15.2 10.8"), dot(15.3, 7.6, 1.1)]


@icon("fish", CAT, "Fish in side view", tags=["seafood", "aquarium", "sea", "animal", "fishing"])
def _(S):
    r = L(S, 0, 1.2)
    d = ("M3 12C5.5 7.5 8.5 6 11.5 6C14 6 16 7.8 17 9.8" + tip((17, 9.8), (21, 6.5), (19.3, 12), r)
         + tip((21, 6.5), (19.3, 12), (21, 17.5), r) + tip((19.3, 12), (21, 17.5), (17, 14.2), r)
         + "L17 14.2C16 16.2 14 18 11.5 18C8.5 18 5.5 16.5 3 12Z")
    return [shell(d), detail("M11 8.8C10 10.8 10 13.2 11 15.2"), dot(7.2, 11)]


@icon("horse", CAT, "Horse head in profile", tags=["pony", "stallion", "equestrian", "animal", "farm"])
def _(S):
    return [shell(_horse(S)), dot(12.2, 9.8), dot(6, 14.8, 1)]


@icon("cow", CAT, "Cow head with horns", tags=["cattle", "bull", "dairy", "farm", "animal", "moo"])
def _(S):
    r = L(S, 0, 1.5)
    head = rect(7, 6, 10, 9, L(S, 2, 3))
    muzzle = rect(5.5, 12.5, 13, 8.5, L(S, 3, 4))
    ear_l = poly([(7.5, 8), (3, 7.2), (3.5, 10), (7.5, 11)], closed=True, r=r)
    ear_r = poly([(16.5, 8), (21, 7.2), (20.5, 10), (16.5, 11)], closed=True, r=r)
    return [shell(union(head, muzzle, ear_l, ear_r)),
            line("M8.5 6.2C7 5.8 6 4.5 5.8 3"), line("M15.5 6.2C17 5.8 18 4.5 18.2 3"),
            dot(9.5, 10), dot(14.5, 10), dot(9.5, 17), dot(14.5, 17)]


@icon("pig", CAT, "Pig face with snout", tags=["piggy", "hog", "farm", "animal", "oink", "pork"])
def _(S):
    r = L(S, 0, 1.2)
    ear_l = poly([(5, 10), (4.2, 3.5), (10, 6.2)], closed=True, r=r)
    ear_r = poly([(19, 10), (19.8, 3.5), (14, 6.2)], closed=True, r=r)
    return [shell(union(circle(12, 13, 8), ear_l, ear_r)), detail(ellipse(12, 15.5, 4, 2.8)),
            dot(10.6, 15.5, 0.9), dot(13.4, 15.5, 0.9), dot(9, 10.5), dot(15, 10.5)]


@icon("sheep", CAT, "Woolly sheep in side view", tags=["lamb", "wool", "farm", "animal", "ewe"])
def _(S):
    k = L(S, 0, 0.3)
    wool = union(ellipse(13.5, 11.5, 6, 4.5), circle(9, 9, 3 + k), circle(13, 7.3, 3 + k), circle(17, 8.3, 3 + k),
                 circle(19, 12, 2.8 + k), circle(16.5, 15, 3 + k), circle(11.5, 15.3, 3 + k), circle(8, 13.3, 3 + k))
    head = rot(ellipse(5.3, 12.3, 2.2, 3), 30, 5.3, 12.3)
    body = minus(wool, rot(ellipse(5.3, 12.3, 4.6, 5.4), 30, 5.3, 12.3))
    return [shell(body), mark(head), line(seg(10.5, 17.5, 10.5, 21)), line(seg(16, 17.5, 16, 21))]


@icon("goat", CAT, "Goat head with horns and beard", tags=["billy", "kid", "farm", "animal", "livestock"])
def _(S):
    r = L(S, 0, 1.2)
    face = poly([(7.8, 7), (16.2, 7), (14.8, 17), (12, 21.5), (9.2, 17)], closed=True, r=L(S, 0, 2))
    ear_l = poly([(8.6, 10.5), (3.3, 12.5), (4.3, 14.3), (9, 13)], closed=True, r=r)
    ear_r = poly([(15.4, 10.5), (20.7, 12.5), (19.7, 14.3), (15, 13)], closed=True, r=r)
    return [shell(union(face, ear_l, ear_r)), line("M9.8 7C9.6 4.5 8.3 3.2 6.3 3"), line("M14.2 7C14.4 4.5 15.7 3.2 17.7 3"),
            dot(10.4, 10.8, 1.1), dot(13.6, 10.8, 1.1)]


@icon("chicken", CAT, "Hen in side view", tags=["hen", "poultry", "farm", "animal", "egg", "bird"])
def _(S):
    r = L(S, 0, 1)
    body = circle(11, 12.5, 6)
    head = circle(15.5, 7, 3)
    beak = poly([(18, 6), (21, 7.6), (18, 9)], closed=True, r=r)
    tail = poly([(7.5, 9.5), (4, 5.2), (5.2, 11.5)], closed=True, r=r)
    return [shell(union(body, head, beak, tail)), mark(union(circle(14.3, 3.6, 1.3), circle(16.4, 3.4, 1.3))),
            dot(16, 6.8, 1.1),
            line(seg(10, 18.4, 10, 21)), line(seg(13, 18.2, 13, 21))]


@icon("duck", CAT, "Duck floating in side view", tags=["duckling", "waterfowl", "pond", "animal", "bird", "quack"])
def _(S):
    r = L(S, 0, 1)
    body = "M3 9.5C5.5 12 8 12.5 12 12.2C16 12 19.8 12.5 19.8 15C19.8 18 16.5 19.8 12 19.8C7 19.8 3.5 17.5 3 9.5Z"
    head = circle(15, 7, 3.5)
    beak = poly([(17.5, 6.8), (21.5, 7.8), (21, 9.6), (17.5, 9.8)], closed=True, r=r)
    return [shell(union(body, head, beak)), detail("M8 15C10 17 13.5 17 15.5 15"), dot(15.2, 6.2, 1.1)]


@icon("rabbit", CAT, "Rabbit head with long ears", tags=["bunny", "hare", "easter", "pet", "animal"], aliases=["bunny"])
def _(S):
    if S.name == "line":
        ear_l, ear_r = leaf(8.5, 2.8, 12, 3), leaf(15.5, 2.8, 12, 3)
    else:
        ear_l, ear_r = ellipse(8.5, 7.3, 2.3, 4.6), ellipse(15.5, 7.3, 2.3, 4.6)
    ear_l, ear_r = rot(ear_l, -12, 8.5, 10), rot(ear_r, 12, 15.5, 10)
    return [shell(union(ellipse(12, 15.5, 6.5, 5.5), ear_l, ear_r)), dot(9.5, 15), dot(14.5, 15),
            mark(ellipse(12, 17.5, 1.2, 0.9))]


@icon("mouse-animal", CAT, "Mouse in side view with a long tail", tags=["mouse", "rodent", "rat", "animal", "pet"])
def _(S):
    r = L(S, 0, 1.2)
    d = ("M10 18.5" + tip((10, 18.5), (3, 16.5), (8, 11), r)
         + "L8 11C9.5 10 11.5 9.5 13 9.5C17 9.5 19.5 13 19.5 16.5C19.5 17.8 18.8 18.5 17.5 18.5Z")
    return [shell(union(d, circle(10.5, 8.5, 3))), detail(arc(10.5, 8.5, 3, 25, 150)), line("M19.2 17C21.5 16.6 21.8 13.5 20.3 12"), dot(7.2, 14)]


@icon("hamster", CAT, "Chubby hamster with full cheeks", tags=["rodent", "pet", "gerbil", "animal", "cute"])
def _(S):
    return [shell(union(ellipse(12, 10.5, 6, 5.5), ellipse(12, 15, 8.5, 6), circle(6.8, 6.2, 2.2), circle(17.2, 6.2, 2.2))),
            dot(9.3, 10.8), dot(14.7, 10.8), mark(ellipse(12, 13, 1.2, 0.9)),
            detail(L(S, "M10 15.6L12 16.4L14 15.6", "M10 15.5C11 16.4 13 16.4 14 15.5")),
            dot(9.5, 19, 1), dot(14.5, 19, 1)]


def _(S):
    return [shell(union(ellipse(12, 13.5, 8.5, 7.5), circle(6.3, 6.5, 2.3), circle(17.7, 6.5, 2.3))),
            dot(9, 10.5), dot(15, 10.5), mark(ellipse(12, 12.6, 1.2, 0.9)),
            detail(L(S, "M8.5 17.5L10.5 16", "M8.5 17.5C9 16.5 9.7 16 10.5 16")), detail(L(S, "M15.5 17.5L13.5 16", "M15.5 17.5C15 16.5 14.3 16 13.5 16")),
            mark(ellipse(12, 17.8, 1.3, 1.7))]


# --------------------------------------------------------------------------- wild mammals and birds

def _nose(S, x, y, w=2.8, h=1.6):
    """Small nose: crisp triangle (Line) or soft oval (Rounded)."""
    if S.name == "line":
        return mark(poly([(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x, y + h / 2)], closed=True))
    return mark(ellipse(x, y, w / 2, h / 2 + 0.1))


@icon("bear", CAT, "Bear head with round ears", tags=["grizzly", "teddy", "wildlife", "animal", "forest"])
def _(S):
    return [shell(union(circle(12, 13, 8), circle(5.5, 6, 2.8), circle(18.5, 6, 2.8))),
            detail(ellipse(12, 16, 3.4, 2.6)), _nose(S, 12, 15.2, 2.6, 1.4), dot(9, 10.5), dot(15, 10.5)]


@icon("panda", CAT, "Panda head with dark eye patches", tags=["bamboo", "bear", "china", "wildlife", "animal"])
def _(S):
    pl = minus(rot(ellipse(8.8, 12.3, 1.9, 2.7), 35, 8.8, 12.3), circle(9.2, 11.8, 0.8))
    pr = minus(rot(ellipse(15.2, 12.3, 1.9, 2.7), -35, 15.2, 12.3), circle(14.8, 11.8, 0.8))
    return [shell(circle(12, 13, 8)), mark(circle(5.8, 6.2, 2.8)), mark(circle(18.2, 6.2, 2.8)),
            mark(pl), mark(pr), _nose(S, 12, 16.3, 2.4, 1.4)]


@icon("lion", CAT, "Lion head with a mane", tags=["king", "mane", "big cat", "wildlife", "animal", "safari"])
def _(S):
    c = (12, 12)
    if S.name == "line":
        mane = poly([pt(c, 9.6 if i % 2 == 0 else 7.9, -90 + i * 20) for i in range(18)], closed=True)
    else:
        mane = union(circle(12, 12, 8), *[circle(*pt(c, 7.8, -90 + i * 40), 1.8) for i in range(9)])
    face = union(circle(12, 12.6, 4.8), circle(*pt(c, 5.4, -130), 1.6), circle(*pt(c, 5.4, -50), 1.6))
    return [shell(minus(mane, face)), dot(10.2, 12, 1.05), dot(13.8, 12, 1.05), _nose(S, 12, 14.4, 2.4, 1.3)]


def _(S):
    c = (12, 12)
    if S.name == "line":
        pts = []
        for i in range(22):
            pts.append(pt(c, 9.4 if i % 2 == 0 else 7.9, -90 + i * 360 / 22))
        mane = poly(pts, closed=True)
    else:
        mane = union(circle(12, 12, 7.9), *[circle(*pt(c, 7.9, -90 + i * 360 / 11), 1.6) for i in range(11)])
    return [shell(minus(mane, circle(12, 12.3, 4.8))), dot(10.2, 11.5, 1.05), dot(13.8, 11.5, 1.05), _nose(S, 12, 14, 2.4, 1.3)]


@icon("tiger", CAT, "Tiger face with stripes", tags=["big cat", "stripes", "wildlife", "animal", "jungle"])
def _(S):
    return [shell(union(ellipse(12, 13, 8.5, 7.5), circle(6, 6.3, 2.6), circle(18, 6.3, 2.6))),
            detail(seg(12, 5.5, 12, 8.5)), detail(seg(9, 6.3, 9.7, 8.3)), detail(seg(15, 6.3, 14.3, 8.3)),
            detail(seg(3.6, 12, 6.2, 13)), detail(seg(20.4, 12, 17.8, 13)), detail(seg(4, 15.6, 6.4, 15.2)), detail(seg(20, 15.6, 17.6, 15.2)),
            dot(9, 11.3), dot(15, 11.3), _nose(S, 12, 15, 2.8, 1.6)]


@icon("elephant", CAT, "Elephant in side view with its trunk", tags=["trunk", "safari", "wildlife", "animal", "memory"])
def _(S):
    body = rect(8, 6.5, 13.5, 11, L(S, 3.5, 5))
    legs = [rect(8.5, 14, 3.5, 7, L(S, 0.5, 1.5)), rect(17.5, 14, 3.5, 7, L(S, 0.5, 1.5))]
    head = circle(7.5, 9.5, 4.5)
    trunk = thick("M5.5 12C4 14.5 3.8 17.5 4.5 20", 3, S)
    return [shell(union(body, *legs, head, trunk)), detail("M9.8 5.6C12.5 6.5 13.3 10 12.6 12.3C12.1 13.8 10.8 14.5 9.5 14.2"), dot(6.2, 8.8, 1.1)]


@icon("giraffe", CAT, "Giraffe with a long neck", tags=["safari", "tall", "wildlife", "animal", "africa"])
def _(S):
    head = rot(ellipse(5.8, 5.5, 3, 1.9), -25, 5.8, 5.5)
    neck = thick("M7.5 6L11.5 12.5", 3.2, S)
    body = rect(9.5, 11, 11, 5.5, L(S, 2, 2.75))
    return [shell(union(head, neck, body)), line(seg(6.8, 4, 7.4, 2)),
            line(seg(11, 16.5, 11, 21)), line(seg(19, 16.5, 19, 21)),
            line(seg(20.5, 12, 21.5, 15)), dot(12.5, 13.8, 1.1), dot(15.2, 13.7, 1.1), dot(17.9, 13.8, 1.1), dot(4.6, 5.8, 0.9)]


def _horse(S):
    r = L(S, 0, 1.2)
    return ("M13 6.5" + tip((13, 6.5), (15.5, 2.8), (16.8, 6.3), r)
            + "L16.8 6.3C19.3 9 20.5 14 20.5 21L10.5 21C10.5 18.5 11 16.8 12 15.2"
            "C10.5 16.8 8.8 17.8 6.8 17.8C5 17.8 3.8 16.8 3.8 15.3C3.8 14 4.3 13.2 5.2 12.3Z")


@icon("zebra", CAT, "Zebra head in profile with stripes", tags=["stripes", "safari", "wildlife", "animal", "africa"])
def _(S):
    mane = poly([(15.5, 4.8), (18.5, 4.5), (17.8, 6.8), (20.5, 7.5), (19.3, 9.3), (21.2, 11), (19.5, 12), (17, 8)], closed=True, r=L(S, 0, 0.8))
    return [shell(union(_horse(S), mane)), detail("M20.5 14L15.5 15.5"), detail("M20.5 18L13 19"), detail("M16.5 11L13.5 12.8"),
            detail("M9 8.8L11 11.2"), dot(12.2, 9.8), dot(6, 14.8, 1)]


@icon("monkey", CAT, "Monkey face", tags=["ape", "chimp", "primate", "jungle", "animal"])
def _(S):
    return [shell(union(ellipse(12, 12, 7, 8), ellipse(5, 12, 2, 2.5), ellipse(19, 12, 2, 2.5))),
            detail("M5.4 14.5C5 9.5 9.5 7.5 12 10C14.5 7.5 19 9.5 18.6 14.5"),
            dot(9.5, 12), dot(14.5, 12), dot(11, 14.6, 0.8), dot(13, 14.6, 0.8),
            detail(L(S, "M9.5 16.8L12 17.8L14.5 16.8", "M9.5 16.6C11 17.8 13 17.8 14.5 16.6"))]


@icon("fox", CAT, "Fox face with large pointed ears", tags=["vixen", "cunning", "wildlife", "animal", "forest"])
def _(S):
    r = L(S, 0, 1.8)
    d = ("M9.2 7.6Q12 6.8 14.8 7.6" + tip((14.8, 7.6), (20.2, 3.2), (20.5, 11.5), r) + "L20.5 11.5"
         "C19.5 15 15 18.5 12 20.5C9 18.5 4.5 15 3.5 11.5" + tip((3.5, 11.5), (3.8, 3.2), (9.2, 7.6), r) + "Z")
    return [shell(d), detail("M3.9 12.4C7 12.2 9.8 13.6 12 16C14.2 13.6 17 12.2 20.1 12.4"), dot(8.8, 10), dot(15.2, 10),
            mark(ellipse(12, 18.3, 1.2, 0.9))]


@icon("wolf", CAT, "Wolf face with upright ears and a furry ruff", tags=["wild dog", "howl", "wildlife", "animal", "forest", "pack"])
def _(S):
    pts = [(5.5, 3), (9.5, 7.2), (14.5, 7.2), (18.5, 3), (19.5, 9.5), (21, 13.5), (18.8, 13.8), (19.8, 16.5), (16.2, 16.8),
           (14.2, 20.5), (9.8, 20.5), (7.8, 16.8), (4.2, 16.5), (5.2, 13.8), (3, 13.5), (4.5, 9.5)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 1))), dot(9.3, 11.3), dot(14.7, 11.3),
            detail(seg(12, 11, 12, 15)), _nose(S, 12, 17.6, 3.2, 1.8)]


def _(S):
    pts = [(3.5, 4.2), (8.8, 6.6), (11.3, 6.3), (14.5, 3), (15.5, 8.3), (18.5, 11), (20.5, 15), (20.5, 21), (11, 21),
           (12.3, 18.7), (9.6, 17.8), (10.8, 15.8), (8.3, 14.5), (9.3, 12.5), (7.2, 9.5), (4.2, 5.8)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 0.9))), dot(11.3, 8.8, 1.1)]


@icon("deer", CAT, "Deer head with antlers", tags=["stag", "reindeer", "antlers", "forest", "wildlife", "animal"])
def _(S):
    r = L(S, 0, 1.2)
    face = "M8.5 7.5L15.5 7.5C16.8 10.5 16.2 14.5 14 18.7C13.3 20.2 10.7 20.2 10 18.7C7.8 14.5 7.2 10.5 8.5 7.5Z"
    ear_l = poly([(9, 8.5), (3.5, 8.3), (4.8, 10.8), (8.8, 11.2)], closed=True, r=r)
    ear_r = poly([(15, 8.5), (20.5, 8.3), (19.2, 10.8), (15.2, 11.2)], closed=True, r=r)
    return [shell(union(face, ear_l, ear_r)),
            line(poly([(10, 7.5), (8, 5), (4.5, 3.5)], r=S.r)), line(seg(8, 5, 8, 2.3)),
            line(poly([(14, 7.5), (16, 5), (19.5, 3.5)], r=S.r)), line(seg(16, 5, 16, 2.3)),
            dot(10.4, 12), dot(13.6, 12), mark(ellipse(12, 18.1, 1.4, 1))]


@icon("owl", CAT, "Owl with ear tufts and big eyes", tags=["night", "wise", "bird", "nocturnal", "animal"])
def _(S):
    r = L(S, 0, 1.8)
    d = ("M9 6.6Q12 5.9 15 6.6" + tip((15, 6.6), (19, 3.5), (19.8, 8.5), r)
         + "L19.8 8.5C20.2 10 20.2 11 20.2 12.5C20.2 17.5 16.5 21 12 21C7.5 21 3.8 17.5 3.8 12.5C3.8 11 3.8 10 4.2 8.5"
         + tip((4.2, 8.5), (5, 3.5), (9, 6.6), r) + "Z")
    return [shell(d), detail("M6.5 9.8C8.5 8.3 10.8 8.5 12 10.3C13.2 8.5 15.5 8.3 17.5 9.8"),
            dot(9.2, 12.3, 1.6), dot(14.8, 12.3, 1.6), mark(poly([(10.9, 14), (13.1, 14), (12, 16)], closed=True, r=L(S, 0, 0.4))),
            detail(L(S, "M9.5 18.5L12 19.5L14.5 18.5", "M9.5 18.4C11 19.4 13 19.4 14.5 18.4"))]


@icon("eagle", CAT, "Eagle head in profile with hooked beak", tags=["bird of prey", "hawk", "falcon", "bird", "animal", "freedom"])
def _(S):
    r = L(S, 0, 0.9)
    d = ("M8.5 6C12 4.2 17 4.3 19 7.5C20.5 10 20.8 15 21 20.8"
         + tip((21, 20.8), (18.5, 19), (16.5, 21), r) + tip((18.5, 19), (16.5, 21), (14.5, 19), r)
         + tip((16.5, 21), (14.5, 19), (12.5, 21), r) + "L12.5 21"
         "C12 18 11.5 15.5 10.5 13.5L7.5 12.6C6.5 12.4 5.5 12.7 4.8 13.6C3.2 12 3 9.5 4.5 8C5.5 7 7 6.3 8.5 6Z")
    return [shell(d), detail("M11 10.8L7.5 10.2"), dot(11.3, 8.3, 1.1)]


@icon("penguin", CAT, "Standing penguin", tags=["antarctic", "bird", "ice", "cold", "animal"])
def _(S):
    r = L(S, 0, 1)
    fl = poly([(7, 9), (3, 15.5), (6.5, 14.5)], closed=True, r=r)
    fr = poly([(17, 9), (21, 15.5), (17.5, 14.5)], closed=True, r=r)
    return [shell(union(ellipse(12, 11.5, 6.3, 8.5), fl, fr)), detail(ellipse(12, 14.3, 3.2, 4.8)),
            dot(10, 7.5, 1.1), dot(14, 7.5, 1.1), mark(poly([(11, 9), (13, 9), (12, 10.8)], closed=True, r=L(S, 0, 0.4))),
            mark(ellipse(9.3, 20.6, 2, 1)), mark(ellipse(14.7, 20.6, 2, 1))]


@icon("parrot", CAT, "Parrot perched in side view", tags=["macaw", "bird", "tropical", "pet", "animal"])
def _(S):
    r = L(S, 0, 1)
    head = circle(10.5, 7.5, 4)
    beak = "M7.5 4.8C5 4.8 3.6 7.2 4.3 10.6L6.2 9.6L7.8 10.8Z"
    body = ("M7.8 10C7 14 9.5 17.5 13 18.3" + tip((13, 18.3), (19, 21.5), (16.8, 16.5), r)
            + "L16.8 16.5C17.5 12.5 15.5 8.5 12 7.5Z")
    return [shell(union(head, beak, body)), detail("M7.8 5.6C8.6 7 8.6 8.8 7.6 10.2"), detail("M11 12C11.5 14.5 13 16 15.5 16.3"),
            dot(11, 7.2, 1.1)]


# --------------------------------------------------------------------------- birds, bugs, reptiles, sea life

@icon("dove", CAT, "Dove in flight", tags=["peace", "pigeon", "bird", "hope", "animal"], aliases=["pigeon"])
def _(S):
    r = L(S, 0, 1)
    body = ("M5.5 9.6C6.2 7.8 8.2 7.4 9.6 8.8C11.6 10.6 14.5 11.5 17 12" + tip((17, 12), (21, 11), (20, 15), r)
            + tip((21, 11), (20, 15), (14, 16), r) + "L14 16C12.5 16.3 11 16.2 9.5 15.6C7.5 14.8 6.2 13.3 5.7 11.6"
            + tip((5.7, 11.6), (3, 10.8), (5.5, 9.6), r) + "Z")
    wing = L(S, "M9 9.8C10.5 6.3 14 3.6 19.8 3C18.6 6.2 17.6 9.4 15.6 11.8Z",
             "M9 9.8C10.5 6.3 14 3.6 18.8 3.1C19.6 3 20 3.5 19.6 4.3C18.5 7 17.4 9.7 15.6 11.8Z")
    return [shell(union(body, wing)), detail("M10 10.5C12 11.5 14 12 15.8 12"), dot(7.6, 9.9, 0.9)]



_BF_UP = "M12 9.5C10 6 7 3.8 3.5 3.8{}L3.6 8C4 10.8 6.5 12.3 12 12.5Z"
_BF_LO = "M12 13.8C8 13.5 4.8 15 4.8 17.8C4.8 20.2 7.2 21.2 9.5 20.2C11 19.5 12 17.8 12 15.5Z"


def _bf_filled():
    up = _BF_UP.format(tip((7, 3.8), (3.2, 3.8), (3.6, 8), 0))
    wings = U(*[U(P(d), ST(d, 2)) for d in (up, flip(up), _BF_LO, flip(_BF_LO))])
    wings = D(wings, ST(seg(12, 2, 12, 22), 4.2), ST(seg(2, 13.1, 22, 13.1), 1.2))
    body = ST(seg(12, 8, 12, 19.5), 2.2, "round", "round")
    ants = U(ST(seg(11.3, 8.5, 9.3, 4.5), 2.5, "round", "round"), ST(seg(12.7, 8.5, 14.7, 4.5), 2.5, "round", "round"))
    return U(wings, body, ants)


@icon("butterfly", CAT, "Butterfly with open wings", tags=["insect", "moth", "spring", "nature", "animal"], filled=_bf_filled)
def _(S):
    up = _BF_UP.format(tip((7, 3.8), (3.2, 3.8), (3.6, 8), L(S, 0, 1.8)))
    return [shell(up), shell(flip(up)), shell(_BF_LO), shell(flip(_BF_LO)), line(seg(12, 8, 12, 19.5)),
            line(poly([(11.3, 8.5), (9.3, 4.5)], r=S.r)), line(poly([(12.7, 8.5), (14.7, 4.5)], r=S.r))]


def _(S):
    r = L(S, 0, 1.8)
    up = "M12 9.5C10 6 7 3.8 3.5 3.8" + tip((7, 3.8), (3.2, 3.8), (3.6, 8), r) + "L3.6 8C4 10.8 6.5 12.3 12 12.5Z"
    lo = "M12 13.8C8 13.5 4.8 15 4.8 17.8C4.8 20.2 7.2 21.2 9.5 20.2C11 19.5 12 17.8 12 15.5Z"
    return [shell(up), shell(flip(up)), shell(lo), shell(flip(lo)), line(seg(12, 8, 12, 19.5)),
            line(poly([(11.3, 8.5), (9.3, 4.5)], r=S.r)), line(poly([(12.7, 8.5), (14.7, 4.5)], r=S.r))]


@icon("bee", CAT, "Striped bee with wings", tags=["honey", "insect", "bumblebee", "buzz", "animal"])
def _(S):
    r = L(S, 0, 1)
    body = union(ellipse(13.3, 14.5, 6.3, 4.8), circle(5.4, 13.8, 2.6),
                 poly([(19, 12.5), (21.8, 14.5), (19, 16.5)], closed=True, r=r))
    wings = union(rot(ellipse(10.8, 7.3, 2.2, 3.6), -25, 10.8, 7.3), rot(ellipse(15.8, 7.3, 2.2, 3.6), 25, 15.8, 7.3))
    return [shell(union(body, wings)), detail(seg(11.5, 10, 11.5, 19.3)), detail(seg(15.3, 10.2, 15.3, 19)),
            dot(4.8, 13.4, 0.9), line(poly([(4.8, 11.3), (4, 8.5)], r=S.r))]


@icon("ant", CAT, "Ant seen from above", tags=["insect", "bug", "colony", "worker", "animal"])
def _(S):
    body = union(ellipse(12, 5.8, 2.3, 2), ellipse(12, 10.6, 1.9, 2.4), ellipse(12, 16.8, 3, 4))
    legs = []
    for pts in ([(10.6, 9.6), (7.5, 8), (5.5, 5.5)], [(10.4, 11), (6.5, 11.5), (4.2, 13.5)], [(10.8, 12.5), (7.8, 15.5), (7, 19.5)]):
        legs.append(line(poly(pts, r=S.r)))
        legs.append(line(poly([(24 - x, y) for x, y in pts], r=S.r)))
    return [shell(body), *legs, line(poly([(11, 4.2), (9.5, 2.8), (7.5, 2.8)], r=S.r)), line(poly([(13, 4.2), (14.5, 2.8), (16.5, 2.8)], r=S.r))]


@icon("spider", CAT, "Spider with eight legs", tags=["arachnid", "web", "halloween", "bug", "animal"])
def _(S):
    legs = []
    for pts in ([(10, 10), (6.5, 7), (5.8, 3)], [(9.5, 11.5), (5, 10.3), (3, 7.3)], [(9.5, 13), (5, 14.2), (3, 17.2)], [(10, 14.5), (6.5, 17.5), (5.8, 21)]):
        legs.append(line(poly(pts, r=S.r)))
        legs.append(line(poly([(24 - x, y) for x, y in pts], r=S.r)))
    return [shell(union(circle(12, 14.5, 3.8), circle(12, 8.8, 2.5))), *legs]


@icon("ladybug", CAT, "Ladybug with spots", tags=["ladybird", "beetle", "insect", "luck", "animal"])
def _(S):
    return [shell(union(circle(12, 13.5, 7.5), ellipse(12, 6.3, 3.6, 2.8))), detail(arc(12, 13.5, 7.5, 235, 305)),
            detail(seg(12, 6.3 + 2.4, 12, 21)), dot(8.6, 12.5, 1.4), dot(15.4, 12.5, 1.4), dot(9, 17.2, 1.4), dot(15, 17.2, 1.4),
            line(poly([(10.3, 4.2), (8.8, 2.6)], r=S.r)), line(poly([(13.7, 4.2), (15.2, 2.6)], r=S.r))]


@icon("snail", CAT, "Snail with a spiral shell", tags=["slow", "slug", "garden", "mollusc", "animal"])
def _(S):
    foot = poly([(3, 20.5), (4.3, 13), (7.5, 13), (8.5, 17.5), (19.5, 17.5), (21.5, 20.5)], closed=True, r=L(S, 0, 1.8))
    sp = [pt((14, 11), 1 + 3.3 * t / 60, 90 + t * 6) for t in range(61)]
    return [shell(union(circle(14, 11, 6.3), foot)), detail(poly(sp)),
            line(seg(5, 13, 4, 9.5)), line(seg(7, 13, 8, 9.5)), dot(3.9, 8.8, 1.1), dot(8.1, 8.8, 1.1)]


@icon("turtle", CAT, "Turtle in side view", tags=["tortoise", "slow", "shell", "reptile", "animal"])
def _(S):
    shell_top = "M3 14C3 9 6.5 6 11 6C15.5 6 18.5 9 18.5 14Z"
    head = ellipse(19, 12.5, 2.6, 2.1)
    band = rect(3, 13, 16.5, 3, L(S, 0.8, 1.5))
    legs = [rect(5, 14, 3, 5.5, L(S, 0.5, 1.5)), rect(13.5, 14, 3, 5.5, L(S, 0.5, 1.5))]
    return [shell(union(shell_top, head, band, *legs)), detail(seg(3.5, 13.5, 18.5, 13.5)),
            detail(poly([(7.5, 13.5), (9, 9.5), (13, 9.5), (14.5, 13.5)], r=S.r)), dot(19.6, 12, 0.9)]


@icon("frog", CAT, "Frog face with bulging eyes", tags=["toad", "amphibian", "pond", "ribbit", "animal"])
def _(S):
    return [shell(union(ellipse(12, 14, 9, 6.3), circle(7.3, 7.8, 3.3), circle(16.7, 7.8, 3.3))),
            dot(7.3, 7.8, 1.3), dot(16.7, 7.8, 1.3),
            detail(L(S, "M7 14.5L9.5 16.5L14.5 16.5L17 14.5", "M7 14.5C9 17 15 17 17 14.5")), dot(10.5, 12.3, 0.8), dot(13.5, 12.3, 0.8)]


@icon("snake", CAT, "Snake coiled in an S shape", tags=["serpent", "reptile", "viper", "python", "animal"])
def _(S):
    c = "M4 19.2H14C16.4 19.2 17.4 17.8 17.4 16.2C17.4 14.6 16.4 13.3 14 13.3H10C7.6 13.3 6.6 11.8 6.6 10.3C6.6 8.8 7.6 7.3 10 7.3H16"
    tail = poly([(4.5, 17.7), (2.5, 19.2), (4.5, 20.7)], closed=True, r=L(S, 0, 0.5))
    return [shell(union(thick(c, 3, S), ellipse(17.6, 7.3, 3.4, 2.7), tail)), dot(18.6, 6.6, 1)]


@icon("lizard", CAT, "Lizard seen from above", tags=["gecko", "reptile", "iguana", "animal", "desert"])
def _(S):
    body = union(thick("M16.2 6.8C14.5 8.8 12.5 11 10.5 13.3", 3.6, S), rot(ellipse(17.8, 5, 2.3, 3), 40, 17.8, 5))
    tail = "M10.5 13.3C8.2 16 7.3 18.3 8.8 19.8C10.2 21.2 12.8 20.7 14.2 19.2"
    return [shell(body), line(tail),
            line(poly([(14.5, 8.6), (11.8, 7), (11.5, 4.5)], r=S.r)), line(poly([(15.6, 9.6), (17.4, 12), (19.8, 12)], r=S.r)),
            line(poly([(11.2, 12), (8.2, 10.8), (6.5, 8.5)], r=S.r)), line(poly([(12.3, 13.4), (13.5, 16), (16, 16.3)], r=S.r))]


@icon("crocodile", CAT, "Crocodile in side view", tags=["alligator", "reptile", "swamp", "animal", "gator"], aliases=["alligator"])
def _(S):
    pts = [(2.5, 13), (3.5, 12), (4.5, 12.4), (8, 11.8), (8.5, 10), (10.3, 10), (10.8, 11.5), (12, 11.5), (12.8, 9.8), (13.8, 11.5), (14.8, 9.8),
           (15.8, 11.5), (16.8, 10.2), (17.8, 12), (21, 14.6), (17.5, 15.8), (16.5, 16), (16.8, 18.8), (14.3, 18.8), (14.3, 16.3),
           (11, 16.3), (10.7, 18.8), (8.2, 18.8), (8.3, 16), (2.5, 16)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 0.8))), detail(L(S, 'M4.5 14.3L7.5 14.3L9 13.3', 'M4.5 14.3L7.5 14.3L9 13.3')), dot(9.4, 11.8, 0.9)]


def _(S):
    snout = poly([(2.5, 13.3), (3.3, 12.3), (9.5, 11.8), (9.5, 15.8), (2.5, 15.8)], closed=True, r=L(S, 0, 1))
    body = ellipse(13, 13.8, 4.8, 2.6)
    tail = poly([(16, 11.5), (21.8, 15), (16.5, 16.3)], closed=True, r=L(S, 0, 0.8))
    legs = [thick(poly([(10.5, 15), (9.5, 18.8)]), 2.2, S), thick(poly([(15, 15), (14.5, 18.8)]), 2.2, S)]
    if S.name == "line":
        ridge = poly([(11, 11.8), (12, 10), (13, 11.5), (14, 10), (15, 11.5), (16, 10.3), (17, 12)], closed=True)
    else:
        ridge = union(circle(12, 11.2, 1), circle(14, 11.1, 1), circle(16, 11.5, 1))
    return [shell(union(snout, body, tail, *legs, circle(8.7, 11.5, 1.8), ridge)), dot(8.8, 11.4, 0.85)]


def _(S):
    head = poly([(2.5, 12.8), (3.2, 11.5), (9, 11), (9, 16), (2.5, 16)], closed=True, r=L(S, 0, 1.2))
    body = ellipse(12.5, 13.5, 5, 2.8)
    tail = poly([(16, 11), (21.5, 14), (16.5, 16.2)], closed=True, r=L(S, 0, 0.8))
    legs = [rect(8.5, 15, 2.4, 3.8, L(S, 0.5, 1.2)), rect(14.3, 15, 2.4, 3.8, L(S, 0.5, 1.2))]
    if S.name == "line":
        ridge = poly([(10, 11), (11, 9.2), (12, 10.8), (13, 9.2), (14, 10.8), (15, 9.4), (16.3, 11.2)], closed=True)
    else:
        ridge = union(circle(11, 10.4, 1.1), circle(13, 10.2, 1.1), circle(15, 10.5, 1.1))
    return [shell(union(head, body, tail, *legs, circle(8, 10.8, 1.8), ridge)), detail(seg(3.2, 14, 8, 14)), dot(8, 10.8, 0.85)]


def _(S):
    r = L(S, 0, 1)
    head = poly([(2.5, 12.5), (8, 11.5), (8, 15.5), (2.5, 15.5)], closed=True, r=L(S, 0, 1.3))
    body = ellipse(13, 13.5, 6, 3)
    tail = poly([(17, 11), (21.5, 16.5), (17.5, 16)], closed=True, r=r)
    legs = [rect(9, 14.5, 2.5, 4.5, L(S, 0.5, 1.2)), rect(15, 14.5, 2.5, 4.5, L(S, 0.5, 1.2))]
    bump = circle(8.2, 11.3, 2)
    if S.name == "line":
        ridge = poly([(10.5, 10.8), (11.5, 8.8), (12.5, 10.6), (13.5, 8.6), (14.5, 10.6), (15.5, 8.8), (16.5, 10.8)], closed=True)
    else:
        ridge = union(circle(11.5, 10.3, 1.2), circle(13.8, 10.1, 1.2), circle(16, 10.5, 1.2))
    return [shell(union(head, body, tail, *legs, bump, ridge)), detail(seg(3, 14, 7.5, 14)), dot(8.4, 11, 0.9)]


@icon("dinosaur", CAT, "Long-necked dinosaur", tags=["dino", "brontosaurus", "jurassic", "prehistoric", "fossil", "animal"])
def _(S):
    r = L(S, 0, 1)
    body = ellipse(13.5, 13.5, 5.5, 4)
    neck = thick("M10 11.5C8 9.5 6.5 7 6 4.5", 3, S)
    head = ellipse(5, 4.5, 2.5, 1.7)
    tail = poly([(17.5, 11), (21.5, 18), (16, 16.5)], closed=True, r=r)
    legs = [rect(9.3, 15, 2.8, 5.5, L(S, 0.5, 1.4)), rect(15.3, 15, 2.8, 5.5, L(S, 0.5, 1.4))]
    return [shell(union(body, neck, head, tail, *legs)), dot(4.4, 4.2, 0.85)]


@icon("whale", CAT, "Whale with a water spout", tags=["ocean", "sea", "marine", "mammal", "animal"])
def _(S):
    r = L(S, 0, 1)
    body = "M3 13C3 9.5 6.5 8 10 8C13.5 8 15.5 10 17 12C18 11 18.5 9.5 18.5 8L20 8C20 11.5 19.5 16 15 17.5C12 18.5 7 18.5 5 17C3.8 16 3 14.5 3 13Z"
    fluke = poly([(18.8, 9), (15.8, 5.8), (19.2, 6.2), (21.5, 4.2), (21, 8), (19.8, 9)], closed=True, r=r)
    return [shell(union(body, fluke)), detail("M3.8 14.6C6 15.6 9 15.6 11 14.6"), dot(7.2, 12.3, 1),
            line("M8 6.2C8 4.6 7 3.5 5.6 3.3"), line("M8 6.2C8 4.6 9 3.5 10.4 3.3")]


@icon("dolphin", CAT, "Dolphin leaping", tags=["porpoise", "ocean", "sea", "marine", "animal"])
def _(S):
    ctrl = ((3, 15), (4.5, 6), (13.5, 3), (18, 14.5))

    def w(t):
        if t < 0.07:
            return 1.8 + t * 5
        if t < 0.3:
            return 2.2 + (t - 0.07) / 0.23 * 3.6
        if t < 0.45:
            return 5.8
        return 5.8 - (t - 0.45) / 0.55 * 4.3
    body = poly(tube(ctrl, w), closed=True, r=L(S, 0, 0.6))
    e = bez(*ctrl, 1)
    tx, ty = 4.5, 11.5
    ln = math.hypot(tx, ty)
    tx, ty = tx / ln, ty / ln
    px, py = ty, -tx
    fl = [(e[0] + px * 0.8, e[1] + py * 0.8), (e[0] + tx * 2.4 + px * 3, e[1] + ty * 2.4 + py * 3), (e[0] + tx * 1.3, e[1] + ty * 1.3),
          (e[0] + tx * 2.4 - px * 3, e[1] + ty * 2.4 - py * 3), (e[0] - px * 0.8, e[1] - py * 0.8)]
    fluke = poly(fl, closed=True, r=L(S, 0, 0.8))
    fin = poly([(9.5, 5), (11.8, 2.3), (14, 5.6)], closed=True, r=L(S, 0, 0.8))
    return [shell(union(body, fluke, fin)), dot(6, 9.8, 0.9)]


def _(S):
    ctrl = ((3, 14.5), (4.5, 5.5), (15, 2.5), (19, 15.5))

    def w(t):
        if t < 0.07:
            return 1.4 + t * 8
        if t < 0.3:
            return 2 + (t - 0.07) / 0.23 * 2.8
        if t < 0.5:
            return 4.8
        return 4.8 - (t - 0.5) / 0.5 * 3.6
    body = poly(tube(ctrl, w), closed=True)
    e = bez(*ctrl, 1)
    fluke = poly([(e[0] - 0.8, e[1] - 1.2), (e[0] - 3.2, e[1] + 3.5), (e[0] + 0.3, e[1] + 1.8), (e[0] + 3.2, e[1] + 2.8), (e[0] + 1, e[1] - 1.2)], closed=True, r=L(S, 0, 1))
    fin = poly([(10, 5.3), (11.5, 1.8), (15, 5.5)], closed=True, r=L(S, 0, 1))
    return [shell(union(body, fluke, fin)), dot(6.3, 9.8, 0.9)]


def _(S):
    r = L(S, 0, 1)
    d = ("M3 12.5" + tip((3, 12.5), (6.3, 10.8), (8, 8), 0) + "C8.5 7.5 11 6 13.5 5.8" + tip((13.5, 5.8), (15.5, 3), (16.3, 6.3), r)
         + "L16.3 6.3C18.5 7.8 19.5 11 19 14.5" + tip((19, 14.5), (21.3, 17.8), (17.3, 17.6), r) + tip((21.3, 17.8), (17.3, 17.6), (16, 20.5), r)
         + tip((17.3, 17.6), (16, 20.5), (16.8, 15.5), r) + "L16.8 15.5C16.5 12 14 10.3 10.5 10.3C8.5 10.3 7 11.3 6 12.3" + tip((6, 12.3), (3, 12.5), (6.3, 10.8), r) + "Z")
    return [shell(d), dot(8.4, 9.3, 0.9)]


@icon("shark", CAT, "Shark with a dorsal fin", tags=["jaws", "ocean", "sea", "predator", "fish", "animal"])
def _(S):
    r = L(S, 0, 1)
    d = ("M2.5 13C5 10.5 9 9.8 11 9.8" + tip((11, 9.8), (13.5, 5.2), (15, 10), r) + "L15 10C17 10.3 18.5 11 19.3 11.6"
         + tip((19.3, 11.6), (21.5, 7.8), (20.5, 13.2), r) + tip((21.5, 7.8), (20.5, 13.2), (21.5, 17.2), r)
         + tip((20.5, 13.2), (21.5, 17.2), (19, 14.8), r) + "L19 14.8C16 16.4 12.5 16.8 9.5 16.5"
         + tip((9.5, 16.5), (9.3, 19), (7, 16), r) + "L7 16C5 15.4 3.5 14.3 2.5 13Z")
    return [shell(d), dot(6.3, 12.4, 1), detail("M3.8 14.2C5.5 15.2 7 15.3 8.5 14.8")]


@icon("octopus", CAT, "Octopus with curling tentacles", tags=["sea", "ocean", "tentacles", "marine", "animal"])
def _(S):
    return [shell(ellipse(12, 9, 6.5, 6)), dot(9.5, 9.8), dot(14.5, 9.8),
            line("M7.5 13.3C7 16.3 5.5 18.5 3 19"), line("M10.5 14.8C10.5 17.8 9.5 20 7.5 21"),
            line("M16.5 13.3C17 16.3 18.5 18.5 21 19"), line("M13.5 14.8C13.5 17.8 14.5 20 16.5 21")]


@icon("crab", CAT, "Crab with raised claws", tags=["crustacean", "seafood", "beach", "sea", "animal"])
def _(S):
    def claw(cx, cy, sx):
        n = poly([(cx, cy), (cx - 1.4 * sx, cy - 4.5), (cx + 3.2 * sx, cy - 3.2)], closed=True)
        return minus(circle(cx, cy, 2.7), n)
    legs = []
    for pts in ([(6.8, 14.5), (3.5, 13.5)], [(7, 16.8), (3.8, 18.5)], [(8.8, 18.3), (7, 21)]):
        legs.append(line(poly(pts, r=S.r)))
        legs.append(line(poly([(24 - x, y) for x, y in pts], r=S.r)))
    return [shell(ellipse(12, 15, 6, 4)), shell(claw(5.5, 7, 1)), shell(claw(18.5, 7, -1)),
            line(poly([(8.3, 11.8), (6.3, 9.5)], r=S.r)), line(poly([(15.7, 11.8), (17.7, 9.5)], r=S.r)),
            *legs, dot(10.3, 14, 1.1), dot(13.7, 14, 1.1)]


@icon("jellyfish", CAT, "Jellyfish with trailing tentacles", tags=["sea", "ocean", "sting", "marine", "animal"])
def _(S):
    if S.name == "line":
        edge = "L18 12.5L16 11.5L14 12.5L12 11.5L10 12.5L8 11.5L6 12.5L4 11.5Z"
    else:
        edge = "Q19 13 18 12Q17 11 16 12Q15 13 14 12Q13 11 12 12Q11 13 10 12Q9 11 8 12Q7 13 6 12Q5 11 4 11.5Z"
    dome = "M4 11.5C4 6.5 7.5 3.5 12 3.5C16.5 3.5 20 6.5 20 11.5" + edge
    return [shell(dome), line("M8 14.5C7 16.5 9 18 8 20.5"), line("M12 14.5C11 16.5 13 18 12 20.5"), line("M16 14.5C15 16.5 17 18 16 20.5")]


@icon("squid", CAT, "Squid with fins and tentacles", tags=["calamari", "sea", "ocean", "marine", "animal"])
def _(S):
    pts = [(12, 2.5), (17, 7.5), (15, 8.2), (15, 14.5), (9, 14.5), (9, 8.2), (7, 7.5)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 1.3))), dot(10.8, 12.2, 1), dot(13.2, 12.2, 1),
            line("M10 14.5C9.5 17 10.5 18.5 9.8 21"), line("M14 14.5C14.5 17 13.5 18.5 14.2 21"),
            line("M9.3 14.3C7 15.5 6 17.5 5.8 20"), line("M14.7 14.3C17 15.5 18 17.5 18.2 20")]


@icon("bat", CAT, "Bat with spread wings", tags=["vampire", "halloween", "night", "flying", "animal"])
def _(S):
    r = L(S, 0, 0.8)
    half = ("M12 8.2L13 8.2" + tip((13, 8.2), (13.8, 5.5), (14.6, 8.6), r) + "L14.6 8.6C16.5 8.2 19 7 21.5 5.2"
            "C21.9 8 21.4 10.6 20.2 12.6Q18.5 10.8 16.7 12.5Q15.2 12.9 13.8 15.5Q12.8 16.2 12 17.8Z")
    return [shell(union(half, flip(half))), dot(10.9, 10.4, 0.9), dot(13.1, 10.4, 0.9)]


@icon("squirrel", CAT, "Squirrel with a bushy tail", tags=["chipmunk", "rodent", "forest", "nuts", "animal"])
def _(S):
    r = L(S, 0, 1)
    body = union(ellipse(8.5, 15.8, 4.2, 4.8), circle(7, 9, 3), poly([(7, 6.4), (7.8, 4.2), (9.4, 6.9)], closed=True, r=r))
    tail = poly(tube(((10.5, 19.8), (22, 20), (11.5, 9), (19.5, 3.2)), lambda t: 3.2 + 3 * math.sin(math.pi * t)), closed=True, r=L(S, 0, 0.6))
    return [shell(union(body, tail)), detail("M11.3 12.3C12.8 14 13.1 16.8 11.8 19.2"), dot(6, 8.7, 1)]


def _(S):
    r = L(S, 0, 1)
    body = union(ellipse(8.8, 15.8, 4, 4.8), circle(7.5, 8.8, 3), poly([(6.3, 6.8), (7.6, 3.4), (9.8, 6.8)], closed=True, r=r))
    tail = poly(tube(((11, 20), (19.5, 20), (21, 9), (15.5, 3.8)), lambda t: 3.5 + 3.3 * math.sin(math.pi * t)), closed=True)
    return [shell(union(body, tail)), detail("M11.3 12.2C12.8 13.8 13.3 16.5 12.2 19.3"), dot(6.4, 8.6, 1)]


def _(S):
    r = L(S, 0, 1)
    body = union(ellipse(8.8, 15.5, 4, 5), circle(7.5, 8.6, 3.1), poly([(6.3, 6.5), (7.6, 3.2), (9.8, 6.6)], closed=True, r=r))
    tail = poly(tube(((11.5, 20.3), (22.5, 20.5), (23, 3.5), (14, 3.2)), lambda t: 3 + 4 * math.sin(math.pi * min(1, t * 1.05))), closed=True, r=L(S, 0, 0.8))
    return [shell(body), shell(minus(tail, grow(body, 2.4))), dot(6.4, 8.4, 1)]


def _(S):
    r = L(S, 0, 1)
    body = union(ellipse(9.5, 15.3, 4.3, 5.2), circle(7.5, 8.8, 3.1),
                 poly([(6.5, 6.5), (7.8, 3.5), (9.8, 6.8)], closed=True, r=r),
                 poly([(5, 8), (2.5, 10), (5.5, 11)], closed=True, r=r))
    tail = poly(tube(((12.5, 19.8), (21.5, 19.5), (22, 6), (15, 4)), lambda t: 3.2 + 2.6 * math.sin(math.pi * min(1, t * 1.1))), closed=True, r=L(S, 0, 0.8))
    return [shell(body), shell(minus(tail, grow(body, 2.6))), dot(6.8, 8.6, 1)]


@icon("hedgehog", CAT, "Hedgehog with spiky back", tags=["spiky", "quills", "garden", "wildlife", "animal"])
def _(S):
    c = (13.5, 18.5)
    spikes = []
    n = 13
    for i in range(n + 1):
        a = 190 + i * (170 / n)
        spikes.append(pt(c, (8 if i % 2 == 0 else 6.2), a))
    pts = spikes + [(21, 18.5), (7, 18.5), (2.5, 16)]
    shape = poly(pts, closed=True, r=L(S, 0, 0.5))
    return [shell(shape), detail("M7.8 11.5C9.2 13.5 9.2 16.2 8.3 18.2"), dot(5.8, 14.5, 1), mark(circle(2.9, 15.8, 1.1)),
            line(seg(10.5, 18.8, 10.5, 21)), line(seg(17.5, 18.8, 17.5, 21))]


@icon("koala", CAT, "Koala face with big fluffy ears", tags=["australia", "bear", "eucalyptus", "marsupial", "animal"])
def _(S):
    nose = rect(10.3, 12.2, 3.4, 5, 1.4) if S.name == "line" else ellipse(12, 14.7, 1.8, 2.6)
    return [shell(union(ellipse(12, 13.5, 7, 6.5), circle(5.8, 8.3, 3.3), circle(18.2, 8.3, 3.3))),
            detail("M5.2 10.8C4.4 9.8 4.4 8.2 5.4 7.2"), detail(flip("M5.2 10.8C4.4 9.8 4.4 8.2 5.4 7.2")),
            mark(nose), dot(8.5, 12.5), dot(15.5, 12.5)]


@icon("kangaroo", CAT, "Kangaroo standing on its hind legs", tags=["australia", "marsupial", "jump", "hop", "animal"])
def _(S):
    pts = [(13.4, 2.5), (14.8, 5), (16.2, 4.9), (20.3, 6.7), (20, 7.7), (16.8, 8.3), (15.8, 9.6), (16.6, 11), (18.8, 13.2), (18, 14),
           (16.3, 12.8), (16.4, 15.3), (17.6, 17.5), (20.8, 19.6), (20.8, 21), (11.5, 21), (10.4, 19.4), (2.8, 21), (9.2, 16),
           (10, 12), (11.8, 8.2), (13, 6.6), (12.6, 4.8)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 0.8))), dot(16.3, 6.3, 0.9)]


def _(S):
    r = L(S, 0, 1)
    head = rot(ellipse(15.8, 5.8, 3.4, 2.1), 15, 15.8, 5.8)
    ear = poly([(12.6, 5.2), (12.2, 2.8), (14.5, 4.2)], closed=True, r=r)
    neck = thick(seg(14.3, 7, 13.6, 9.5), 2.8, S)
    torso = rot(ellipse(12.8, 12.6, 3.2, 4.8), 18, 12.8, 12.6)
    thigh = ellipse(12.3, 16.5, 3.6, 3)
    foot = poly([(10.3, 18.8), (19.8, 19.8), (19.8, 21.2), (10.3, 21.2)], closed=True, r=r)
    tail = poly(tube(((10, 16), (7, 18), (5, 19.8), (2.8, 20.8)), lambda t: 3 - 2 * t), closed=True, r=r)
    arm = thick(poly([(15, 10.5), (17.3, 12), (17.2, 13.6)]), 1.8, S)
    return [shell(union(head, ear, neck, torso, thigh, foot, tail, arm)), dot(16, 5.2, 0.9)]


def _(S):
    r = L(S, 0, 1)
    head = rot(ellipse(16.3, 6.3, 3, 2), 12, 16.3, 6.3)
    ear = poly([(13.8, 5.8), (13.5, 2.3), (15.8, 4.8)], closed=True, r=r)
    torso = rot(ellipse(13.3, 12.5, 3.3, 5), 25, 13.3, 12.5)
    thigh = ellipse(12.3, 16.3, 3.5, 3)
    foot = poly([(10, 18.5), (19.8, 19.6), (19.8, 21), (10, 21)], closed=True, r=r)
    tail = poly(tube(((10, 15.5), (7, 17.5), (5, 19.5), (2.6, 20.8)), lambda t: 3 - 2 * t), closed=True, r=r)
    arm = thick(poly([(15.3, 11), (17.8, 13.3)]), 1.8, S)
    return [shell(union(head, ear, torso, thigh, foot, tail, arm)), dot(16.8, 5.8, 0.9)]


def _(S):
    pts = [(13.8, 2.3), (15.3, 4.8), (18, 5.3), (20.8, 7.2), (17.8, 8.8), (16.6, 10.6), (18.6, 13), (17.8, 13.8), (16.2, 12.8),
           (16, 16.3), (20.5, 19.5), (20.5, 21), (11.8, 21), (10.8, 18.6), (2.8, 21), (9.3, 15), (10.5, 11), (12.8, 6.8), (12.8, 4)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 1))), dot(16.5, 6.8, 0.9)]


def _(S):
    pts = [(14.3, 2.5), (15.5, 5), (18, 5.8), (20.3, 7.6), (17.5, 9), (16.5, 10.5), (18.8, 12.8), (16.3, 13.5), (16.2, 16.3),
           (20.5, 19.5), (20.5, 21), (11.8, 21), (10.8, 18.6), (2.8, 21), (9.3, 15), (10.5, 11), (13, 6.5), (13.2, 4)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 1))), dot(16.5, 7.2, 0.9)]


@icon("camel", CAT, "Camel with two humps", tags=["desert", "dromedary", "caravan", "sahara", "animal"])
def _(S):
    body = union(ellipse(14, 13, 6.3, 3.2), circle(11.8, 10.5, 2.8), circle(16.8, 10.5, 2.8))
    neck = thick("M9 13C7.5 12.5 6.5 10.5 6 7", 2.8, S)
    head = rot(ellipse(4.8, 6.3, 2.4, 1.6), -10, 4.8, 6.3)
    return [shell(union(body, neck, head)), line(seg(10, 15.5, 10, 21)), line(seg(13, 15.8, 13, 21)),
            line(seg(15.5, 15.8, 15.5, 21)), line(seg(18.5, 15.5, 18.5, 21)), dot(4.8, 5.8, 0.85)]


@icon("llama", CAT, "Llama with long neck and upright ears", tags=["alpaca", "andes", "wool", "farm", "animal"], aliases=["alpaca"])
def _(S):
    r = L(S, 0, 1)
    head = rot(ellipse(6.3, 7, 2.9, 2), -5, 6.3, 7)
    ears = [poly([(6, 5.5), (6.2, 3), (7.6, 5.3)], closed=True, r=r), poly([(8, 5.5), (8.8, 3), (9.8, 5.8)], closed=True, r=r)]
    neck = rect(6.5, 6, 3.8, 9, L(S, 0.5, 1.5))
    body = rect(6.5, 11.5, 13.5, 5.5, L(S, 2, 2.75))
    tail = circle(19.8, 12.3, 1.5)
    return [shell(union(head, *ears, neck, body, tail)), line(seg(8.5, 17, 8.5, 21)), line(seg(11.5, 17, 11.5, 21)),
            line(seg(15.5, 17, 15.5, 21)), line(seg(18.5, 17, 18.5, 21)), dot(6, 6.6, 0.85)]


# --------------------------------------------------------------------------- pet things

@icon("paw", CAT, "Animal paw print", tags=["pet", "footprint", "dog", "cat", "track", "animal"], aliases=["paw-print"])
def _(S):
    if S.name == "line":
        pad = poly([(12, 11.8), (17.8, 17.5), (15, 20.6), (12, 19.8), (9, 20.6), (6.2, 17.5)], closed=True, r=1.8)
    else:
        pad = ("M12 12C9 12 6.5 15.5 6.5 17.5C6.5 19.5 8 20.5 9.5 20.5C10.5 20.5 11 20 12 20C13 20 13.5 20.5 14.5 20.5"
               "C16 20.5 17.5 19.5 17.5 17.5C17.5 15.5 15 12 12 12Z")
    toes = [rot(ellipse(4.8, 11, 1.8, 2.3), -25, 4.8, 11), rot(ellipse(9.2, 6.2, 1.9, 2.5), -10, 9.2, 6.2),
            rot(ellipse(14.8, 6.2, 1.9, 2.5), 10, 14.8, 6.2), rot(ellipse(19.2, 11, 1.8, 2.3), 25, 19.2, 11)]
    return [shell(pad), *[shell(t) for t in toes]]


@icon("dog-bone", CAT, "Dog bone treat", tags=["bone", "treat", "chew", "pet", "dog"])
def _(S):
    k = L(S, 2.2, 2.5)
    b = union(rect(6, 10.2, 12, 3.6), circle(5.8, 9.6, k), circle(5.8, 14.4, k), circle(18.2, 9.6, k), circle(18.2, 14.4, k))
    return [shell(rot(b, -45, 12, 12))]


@icon("bird-cage", CAT, "Domed bird cage", tags=["birdcage", "cage", "pet", "parrot", "canary"])
def _(S):
    cage = union("M5 18V11C5 7 8 5.5 12 5.5C16 5.5 19 7 19 11V18Z", rect(3.5, 17.5, 17, 3.5, L(S, 1, 1.75)))
    return [shell(cage), detail(seg(9, 7, 9, 17.5)), detail(seg(12, 6, 12, 17.5)), detail(seg(15, 7, 15, 17.5)),
            detail(seg(4, 17.5, 20, 17.5)), line(circle(12, 3.8, 1.5) if S.name == "rounded" else rect(10.5, 2.3, 3, 2.7))]


@icon("fish-bowl", CAT, "Round fish bowl with a fish", tags=["aquarium", "goldfish", "pet", "tank", "fish"])
def _(S):
    bowl = union(minus(circle(12, 13, 8.2), rect(0, 0, 24, 6.2)), rect(7, 4, 10, 2.5, L(S, 0.5, 1.25)))
    fish = union(ellipse(11, 15, 3, 2), poly([(13.3, 15), (16, 13), (16, 17)], closed=True, r=L(S, 0, 0.5)))
    return [shell(bowl), detail(seg(4.3, 10, 19.7, 10)), mark(fish)]


@icon("pet-bowl", CAT, "Pet food bowl with food", tags=["dog bowl", "food", "feeding", "pet", "cat"])
def _(S):
    bowl = union(rect(3.5, 11, 17, 3, L(S, 1, 1.5)), poly([(5, 13.5), (19, 13.5), (20.5, 20.5), (3.5, 20.5)], closed=True, r=S.r))
    food = "M6 11C6.5 8 9 6.5 12 6.5C15 6.5 17.5 8 18 11Z"
    bone = union(rect(9.5, 16.3, 5, 1.4), circle(9.3, 16.2, 0.9), circle(9.3, 17.8, 0.9), circle(14.7, 16.2, 0.9), circle(14.7, 17.8, 0.9))
    return [shell(union(bowl, food)), detail(seg(4, 11, 20, 11)), mark(bone)]


# --------------------------------------------------------------------------- more wildlife and legends

@icon("rhino", CAT, "Rhinoceros with horns in side view", tags=["rhinoceros", "horn", "safari", "wildlife", "animal"], aliases=["rhinoceros"])
def _(S):
    r = L(S, 0, 1)
    body = rect(8.5, 7.5, 13, 9.5, L(S, 3.5, 4.5))
    head = poly([(3, 14.5), (3.5, 11.3), (8.5, 8.5), (10.5, 9), (10.5, 15.5), (5, 16.3)], closed=True, r=L(S, 0, 1.5))
    horns = [poly([(3.4, 12), (3, 6.8), (6.4, 10.3)], closed=True, r=r), poly([(7, 9.4), (7.6, 7.2), (8.8, 8.7)], closed=True, r=r)]
    ear = poly([(9.2, 8.5), (9.8, 5.3), (11.5, 8)], closed=True, r=r)
    legs = [rect(9.5, 14, 3, 7, L(S, 0.5, 1.5)), rect(17.5, 14, 3, 7, L(S, 0.5, 1.5))]
    return [shell(union(body, head, *horns, ear, *legs)), dot(7.8, 11.8, 0.95)]


@icon("hippo", CAT, "Hippopotamus face with a wide muzzle", tags=["hippopotamus", "river", "safari", "wildlife", "animal"], aliases=["hippopotamus"])
def _(S):
    return [shell(union(ellipse(12, 8.8, 5.8, 4.8), circle(7.2, 4.8, 1.7), circle(16.8, 4.8, 1.7), ellipse(12, 15.3, 8.5, 5.3))),
            dot(9.6, 8.3), dot(14.4, 8.3), dot(8.2, 13.8, 1.1), dot(15.8, 13.8, 1.1),
            detail(L(S, "M8 17.5L12 18.5L16 17.5", "M8 17.3C10.5 18.8 13.5 18.8 16 17.3"))]


@icon("flamingo", CAT, "Flamingo standing on one leg", tags=["bird", "pink", "tropical", "wading", "animal"])
def _(S):
    r = L(S, 0, 1)
    body = rot(ellipse(15, 10, 5, 3), -12, 15, 10)
    tail = poly([(19, 7.5), (21.8, 7.5), (19.5, 10.5)], closed=True, r=r)
    beak = poly([(10.3, 5), (9.8, 8.8), (8.6, 5.8)], closed=True, r=r)
    return [shell(union(body, tail)), line("M11 11C8 10.5 6.2 8.5 6.2 6C6.2 4 7.6 3 9 3C10.3 3 11 4 11 5"),
            mark(union(circle(9.8, 4.8, 1.5), beak)), line(seg(14.5, 13, 14.5, 21)), line(poly([(15.8, 12.5), (18.5, 15.5), (15.5, 16.5)], r=S.r))]


@icon("swan", CAT, "Swan gliding with a curved neck", tags=["bird", "lake", "grace", "elegant", "animal"])
def _(S):
    r = L(S, 0, 0.8)
    body = "M6 15C6 18 8.5 19.8 13 19.8C17.5 19.8 20.5 17.5 21.3 11.5C19 13.5 16.5 14 13.5 13.5C10.5 13 8 13.3 6 15Z"
    neck = thick("M8.3 5C10 6.5 9.8 9 8.3 11C7 12.8 7 14 8 15.5", 2.6, S)
    head = circle(7.4, 4.8, 2)
    beak = poly([(6, 3.9), (3, 6), (6.3, 6.2)], closed=True, r=r)
    return [shell(union(body, neck, head, beak)), detail("M11 16.5C14 17.5 17 16.5 19 14.2"), dot(7.8, 4.5, 0.8)]


@icon("peacock", CAT, "Peacock with its tail fanned out", tags=["peafowl", "bird", "feathers", "proud", "animal"])
def _(S):
    body = union(ellipse(12, 15.8, 2.6, 4), circle(12, 9.8, 1.9))
    fan = minus(circle(12, 13, 9) if S.name == "rounded" else poly(regular(12, 13, 9.2, 18), closed=True), rect(0, 17, 24, 8))
    fan = minus(fan, grow(body, 2.3))
    return [shell(fan), shell(body), *[dot(*pt((12, 13), 6.3, a), 1.3) for a in (195, 232, 270, 308, 345)],
            line(seg(12, 7.6, 12, 5.2)), line(seg(11, 19.5, 11, 21.5)), line(seg(13, 19.5, 13, 21.5))]


@icon("rooster", CAT, "Rooster with comb and tall tail feathers", tags=["cock", "cockerel", "farm", "morning", "bird", "animal"])
def _(S):
    r = L(S, 0, 1)
    body = rot(ellipse(11.5, 13.5, 5.5, 4.3), -15, 11.5, 13.5)
    neck = thick("M15 7L14.5 12", 3.4, S)
    head = circle(15.3, 6.6, 2.7)
    beak = poly([(17.5, 5.6), (20.3, 6.8), (17.6, 8)], closed=True, r=r)
    tail = poly(tube(((8, 11.5), (6.5, 3.5), (1, 4.5), (3.3, 14)), lambda t: 4.2 - 3 * t), closed=True, r=L(S, 0, 0.6))
    return [shell(union(body, neck, head, beak, tail)), mark(union(circle(13.7, 3.6, 1.2), circle(15.4, 3, 1.25), circle(17, 3.9, 1.1))),
            mark(ellipse(17.2, 9.4, 0.9, 1.4)), dot(15.8, 6.3, 1), detail("M7.8 13.5C6.6 11.5 6.2 9.5 6.5 7.5"),
            line(seg(10.5, 17.8, 10.5, 21)), line(seg(13.5, 17.5, 13.5, 21))]


@icon("unicorn", CAT, "Unicorn head with a horn", tags=["magic", "fantasy", "myth", "horse", "rainbow"])
def _(S):
    horn = poly([(10.8, 7.8), (8.6, 2.6), (13.2, 6.3)], closed=True, r=L(S, 0, 0.8))
    if S.name == "line":
        mane = poly([(15.5, 4.8), (18.5, 4.5), (17.8, 6.8), (20.5, 7.5), (19.3, 9.3), (21.2, 11), (19.5, 12), (17, 8)], closed=True)
    else:
        mane = union(circle(17.3, 5.5, 1.5), circle(19.2, 7.8, 1.5), circle(20.2, 10.5, 1.4), poly([(16, 5), (18.5, 5), (20.5, 11.5), (19.5, 12), (17, 8)], closed=True))
    return [shell(union(_horse(S), horn, mane)), dot(12.2, 9.8), dot(6, 14.8, 1)]


@icon("dragon", CAT, "Winged dragon", tags=["fantasy", "myth", "fire", "legend", "wyvern"])
def _(S):
    r = L(S, 0, 0.8)
    body = union(ellipse(11.5, 14.5, 4.5, 3), thick("M8.8 13C7 11.5 6 9.5 6 7", 2.6, S),
                 poly([(2.5, 7.8), (4, 5.3), (7.2, 4.8), (8.2, 6.6), (6.5, 8.3), (3, 8.8)], closed=True, r=r),
                 poly([(6.6, 5.2), (8.8, 2.5), (8.2, 5.6)], closed=True, r=r),
                 thick("M15.5 15.5C18.5 16.2 19.5 17.5 19.2 19.5", 2, S), poly([(17.3, 19.2), (21.5, 21.2), (20.8, 17.3)], closed=True, r=r),
                 rect(9, 16, 2.2, 5, L(S, 0.5, 1.1)), rect(12.6, 16, 2.2, 5, L(S, 0.5, 1.1)))
    wing = poly([(10.5, 11.5), (13.5, 3.2), (21.5, 3.5), (20, 6.5), (18, 6.3), (17.2, 8.8), (15, 8.6), (14.2, 11.5)], closed=True, r=r)
    return [shell(body), shell(minus(wing, grow(body, 2.2))), dot(5.5, 6.5, 0.8)]


@icon("seal", CAT, "Seal resting in side view", tags=["sea lion", "marine", "arctic", "ocean", "animal"])
def _(S):
    r = L(S, 0, 0.8)
    body = poly(tube(((7, 7.5), (6, 15), (11, 18.8), (18.5, 18.5)), lambda t: 5 + 1.5 * math.sin(math.pi * t) - 2.8 * t), closed=True, r=0)  # no fillet: the tube has hundreds of tiny segments and fillets on them break round-join stroking in fonts
    head = union(circle(7, 6.8, 3.2), ellipse(4, 7.8, 2, 1.5))
    tailf = poly([(18, 17.3), (21.6, 15.2), (20.5, 18.5), (21.6, 21), (18, 19.7)], closed=True, r=r)
    flip_ = poly([(9, 17), (12.5, 21), (8, 20.5)], closed=True, r=r)
    return [shell(union(body, head, tailf, flip_)), dot(7.5, 6, 0.95), mark(circle(2.9, 7.3, 0.9))]


@icon("otter", CAT, "Otter face with whiskers", tags=["river", "sea otter", "swim", "wildlife", "animal"])
def _(S):
    return [shell(union(ellipse(12, 12.8, 8.3, 7.3), circle(4.8, 8.6, 1.9), circle(19.2, 8.6, 1.9))),
            _nose(S, 12, 13.6, 3, 1.7), detail(L(S, "M10 17L12 16L14 17", "M10 17C11 17.6 11.6 17.2 12 16.2C12.4 17.2 13 17.6 14 17")),
            detail(seg(8.8, 14.6, 5.4, 13.8)), detail(seg(8.8, 16.6, 5.8, 17.8)), detail(seg(15.2, 14.6, 18.6, 13.8)), detail(seg(15.2, 16.6, 18.2, 17.8)),
            dot(8.8, 10.8), dot(15.2, 10.8)]


def _(S):
    return [shell(union(ellipse(12, 13, 8, 7), circle(5, 8.5, 1.9), circle(19, 8.5, 1.9))),
            detail(union(circle(10.1, 16, 2.1), circle(13.9, 16, 2.1))),
            _nose(S, 12, 13.2, 2.6, 1.5), dot(8.6, 11), dot(15.4, 11)]


@icon("beaver", CAT, "Beaver face with buck teeth", tags=["rodent", "dam", "river", "wildlife", "animal"])
def _(S):
    return [shell(union(ellipse(12, 12, 7.5, 7), circle(5.8, 6, 1.9), circle(18.2, 6, 1.9), rect(9.8, 17, 4.4, 4.3, L(S, 0.5, 1.2)))),
            detail(seg(12, 18.8, 12, 21.3)), dot(9, 10.5), dot(15, 10.5), _nose(S, 12, 14, 3.2, 1.8)]


@icon("raccoon", CAT, "Raccoon face with a bandit mask", tags=["bandit", "trash panda", "wildlife", "animal", "forest"])
def _(S):
    r = L(S, 0, 1.5)
    d = ("M9 6.8Q12 6.1 15 6.8" + tip((15, 6.8), (18.8, 3.2), (20, 8.5), r) + tip((18.8, 3.2), (20, 8.5), (21.3, 14), r)
         + tip((20, 8.5), (21.3, 14), (18.5, 14.8), r) + "L18.5 14.8C17.5 18 15 20.5 12 20.5C9 20.5 6.5 18 5.5 14.8"
         + tip((5.5, 14.8), (2.7, 14), (4, 8.5), r) + tip((2.7, 14), (4, 8.5), (5.2, 3.2), r) + tip((4, 8.5), (5.2, 3.2), (9, 6.8), r) + "Z")
    mask = "M5.5 10.5C7.5 9.3 10 9.6 12 11C14 9.6 16.5 9.3 18.5 10.5C18.5 12.5 17.5 13.8 15.5 13.8C14 13.8 12.8 13.2 12 12.5C11.2 13.2 10 13.8 8.5 13.8C6.5 13.8 5.5 12.5 5.5 10.5Z"
    return [shell(d), mark(minus(mask, circle(8.8, 11.6, 0.95), circle(15.2, 11.6, 0.95))), _nose(S, 12, 16.5, 2.8, 1.6)]
