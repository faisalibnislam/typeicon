"""TypeIcon Core: birds (batch 001).

Raptors, waterfowl, seabirds, waders, ratites and exotic birds, drawn from the birds themselves.
Most birds face left in side view; flight views are symmetric from below or above.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "birds"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12, cy=12):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpts(pts, deg, cx=12, cy=12):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def thick(d, w, S):
    """Outline of a stroke of width w along d (necks, legs inside a silhouette)."""
    return path_to_d(ST(d, w, S.cap, S.join))


def flip(d):
    """Mirror a d-string across the vertical centre line."""
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def fpts(pts):
    return [(24 - x, y) for x, y in pts]


def grow(d, g):
    """Region d expanded by g px (cuts clean gaps between overlapping parts)."""
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
    """Closed polygon with sharp corners in Line and softened corners in Rounded (beaks, tails, crests)."""
    return poly(pts, closed=True, r=L(S, 0, r))


def legs(*xs, y0=16.5, y1=21):
    return [line(seg(x, y0, x, y1)) for x in xs]


def water(S, y=20.5, x0=2.5, x1=21.5):
    """Gentle wave line."""
    n = max(2, round((x1 - x0) / 4.75))
    w = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        xa = x0 + i * w
        d += f"C{fmt(xa + w * 0.3)} {fmt(y - 1.1)} {fmt(xa + w * 0.7)} {fmt(y - 1.1)} {fmt(xa + w)} {fmt(y)}"
    return line(d)


# ============================================================================ raptors

@icon("falcon", CAT, "Falcon diving head first with its wings folded back",
      tags=["peregrine", "bird of prey", "dive", "raptor", "speed", "hawk"])
def _(S):
    r = L(S, 0, 0.8)
    body = ("M6 9.6C9.5 8.6 14 8.6 17 9.3" + tip((17, 9.3), (22, 10.2), (17.5, 11.8), r)
            + "L17.5 11.8" + tip((17.5, 11.8), (19.8, 14.2), (15, 14.4), r)
            + "L15 14.4C12 15.4 8.5 15.5 6 14.6Z")
    head = union(circle(5.6, 12, 2.7), "M3.2 10.8C2.2 11.6 2 13 2.6 14.6" + tip((2.6, 13.8), (2.6, 14.6), (4, 13.5), L(S, 0, 0.5)) + "L4 13.5Z")
    ex, ey = rpts([(5.4, 11.4)], -45)[0]
    return [shell(rot(union(body, head), -45)), detail(rot("M8.6 12.3C11.5 12.2 14.5 11.6 17 10.8", -45)),
            line(rot(seg(12, 5.6, 18.5, 6.4), -45)), line(rot(seg(13, 18.3, 18.5, 17.6), -45)), dot(ex, ey, 0.95)]


@icon("kestrel", CAT, "Small falcon hovering with its wings raised in a V and its tail fanned",
      tags=["hover", "falcon", "bird of prey", "raptor", "windhover", "hawk"])
def _(S):
    wl = [(10.6, 9.6), (4, 3.2), (4.2, 7.2), (5.8, 9.8), (10.4, 13.2)]
    body = union(ellipse(12, 12, 2.4, 3.8), circle(12, 7.6, 2.2),
                 tri(S, wl, 1), tri(S, fpts(wl), 1),
                 "M10.9 14.5L13.1 14.5L16.2 19C14.5 20.6 9.5 20.6 7.8 19Z")
    return [shell(body), mark(tri(S, [(11.1, 8.2), (12.9, 8.2), (12, 10.2)], 0.3))]


@icon("osprey", CAT, "Osprey flying with a fish held lengthwise in its talons",
      tags=["fish hawk", "sea hawk", "bird of prey", "raptor", "fishing", "catch"])
def _(S):
    body = union(ellipse(11.5, 10.2, 5.8, 2.2), circle(5.6, 9.5, 2),
                 tri(S, [(3.9, 8.4), (2.2, 10.6), (4.4, 10.9)], 0.5),
                 tri(S, [(16, 9.2), (21.3, 10.5), (16.5, 11.8)], 0.8),
                 tri(S, [(9, 9.5), (11.5, 4.5), (20.5, 2.8), (15.5, 7.2), (14.5, 9.5)], 1))
    fish = union(ellipse(11.3, 18.2, 4.3, 1.7), tri(S, [(15, 18.2), (18.5, 16.2), (18.5, 20.2)], 0.6))
    return [shell(body), shell(fish), line(seg(9.5, 12.4, 9.5, 16.5)), line(seg(13, 12.4, 13, 16.5)), dot(5.6, 9.2, 0.8)]


@icon("vulture", CAT, "Hunched vulture perched with a bare head, neck ruff and hooked beak",
      tags=["buzzard", "scavenger", "carrion", "bird of prey", "desert", "raptor"])
def _(S):
    r = L(S, 0, 1)
    body = ("M8.5 9.5C10 5.8 16 5.2 18.8 9C20.5 11.5 20.5 14.5 20 17"
            + tip((20, 17), (21.8, 21), (16.5, 19), r) + "L16.5 19C13.5 19.5 10.5 18.5 9 16C8 14.2 7.8 11.5 8.5 9.5Z")
    ruff = union(circle(8.4, 10.2, 2.1), circle(10.2, 8.6, 1.9), circle(9.5, 12.4, 1.8))
    head = union(thick("M7 9.5C6 8.8 5.5 8 5.5 7", 1.8, S), circle(5.3, 6.4, 1.9))
    beak = "M3.8 5.4C2.3 5.8 1.8 7.3 2.4 8.8" + tip((2.4, 8.2), (2.4, 8.8), (3.8, 7.6), L(S, 0, 0.5)) + "L3.8 7.6Z"
    return [shell(union(body, ruff, head, beak)), detail("M12.5 9.5C14.5 11 15.5 13.5 15.5 16.5"), dot(5.5, 6, 0.75),
            line(seg(11.5, 18.8, 11.5, 21)), line(seg(14, 19, 14, 21))]


@icon("condor", CAT, "Condor soaring seen from below with broad wings and splayed wingtip feathers",
      tags=["andean condor", "vulture", "soar", "bird of prey", "raptor", "glide"])
def _(S):
    r = L(S, 0, 0.5)
    wl = [(11, 9.3), (6.8, 8.4), (3.2, 6.8), (5.6, 10), (2.8, 11), (5.6, 12.3), (3.4, 15.2), (6.8, 14.8), (11, 15.2)]
    body = union(ellipse(12, 12.3, 1.9, 3.6), circle(12, 7.6, 1.5), poly(wl, closed=True, r=r), poly(fpts(wl), closed=True, r=r),
                 tri(S, [(10.6, 15), (13.4, 15), (14.3, 18), (9.7, 18)], 0.8))
    return [shell(body)]


@icon("harpy-eagle", CAT, "Eagle head from the front with a split double crest and a hooked beak",
      tags=["eagle", "crest", "rainforest", "bird of prey", "raptor", "harpy"])
def _(S):
    r = L(S, 0, 0.9)
    head = ("M7.3 8.2" + tip((7.3, 8.2), (4.8, 3.8), (9.3, 6.5), r) + tip((4.8, 3.8), (9.3, 6.5), (9, 3.5), r)
            + tip((9.3, 6.5), (9, 3.5), (12, 6.2), r) + "L12 6.2" + tip((12, 6.2), (15, 3.5), (14.7, 6.5), r)
            + tip((15, 3.5), (14.7, 6.5), (19.2, 3.8), r) + tip((14.7, 6.5), (19.2, 3.8), (16.7, 8.2), r)
            + "L16.7 8.2C19.8 10 20 14 17.5 16.8C16 18.4 14 19.3 12 21C10 19.3 8 18.4 6.5 16.8C4 14 4.2 10 7.3 8.2Z")
    beak = "M10.5 10.5L13.5 10.5C14.2 13 14 16 12 18.3C11.8 17.2 11 16.6 10.2 16.6C10.8 14.5 10.3 12.5 10.5 10.5Z"
    return [shell(head), mark(beak), dot(8.4, 12, 1.1), dot(15.6, 12, 1.1),
            detail(seg(6.5, 10.2, 9.5, 11)), detail(seg(17.5, 10.2, 14.5, 11))]


@icon("secretary-bird", CAT, "Tall secretary bird striding on long legs with quills behind its head",
      tags=["savanna", "africa", "long legs", "snake eater", "raptor", "quills"])
def _(S):
    body = union(rot(ellipse(12.5, 9.5, 5, 2.6), 12, 12.5, 9.5), thick("M8.5 9C7.5 7.5 6.8 6.5 6.3 5.5", 2.4, S),
                 circle(6, 5.2, 1.8), tri(S, [(4.5, 4.4), (3, 6.3), (4.8, 6.4)], 0.5),
                 tri(S, [(16.5, 10), (20.8, 13.3), (16, 12.2)], 0.8))
    return [shell(body), dot(6.2, 5, 0.7), line(seg(7.3, 4, 10, 2.8)), line(seg(7.8, 5.6, 10.8, 5)),
            line(poly([(11, 11.8), (9.5, 16), (6.5, 20.8)], r=S.r)), line(poly([(13.5, 12), (15, 16.5), (17.5, 20.8)], r=S.r))]


@icon("kite-bird", CAT, "Kite gliding seen from below with slender bent wings and a forked tail",
      tags=["red kite", "glide", "forked tail", "bird of prey", "raptor", "hawk"])
def _(S):
    wl = [(11, 8.8), (6.5, 6.8), (3, 9.3), (7, 9.8), (11, 12.8)]
    body = union(ellipse(12, 10.5, 1.9, 4), circle(12, 6.3, 1.7), tri(S, wl, 1), tri(S, fpts(wl), 1),
                 tri(S, [(10.8, 13.5), (13.2, 13.5), (15.5, 20), (12, 17.6), (8.5, 20)], 0.8))
    return [shell(body)]


@icon("eagle-spread-wings", CAT, "Eagle from the front with both wings raised and spread, head in profile",
      tags=["eagle", "wings spread", "emblem", "freedom", "bird of prey", "heraldic"])
def _(S):
    r = L(S, 0, 0.6)
    wl = [(10.2, 9.5), (8, 5), (3.2, 3.2), (4.2, 6), (2.8, 6.8), (4.4, 9), (3.2, 10.2), (5.4, 12), (10.2, 14)]
    body = union(ellipse(12, 13, 2.6, 4), circle(12.3, 7.6, 2.2), tri(S, [(10.6, 6.5), (8.3, 8.2), (10.8, 9.2)], 0.4),
                 poly(wl, closed=True, r=r), poly(fpts(wl), closed=True, r=r),
                 tri(S, [(10.5, 16), (13.5, 16), (15.3, 20.8), (8.7, 20.8)], 1))
    return [shell(body), dot(12.6, 7.1, 0.75)]


# ============================================================================ owls

@icon("barn-owl", CAT, "Barn owl from the front with a heart-shaped facial disc",
      tags=["owl", "night", "nocturnal", "heart face", "farm", "bird"])
def _(S):
    face = ("M12 7.2C10.5 5 6.5 5.3 6.5 9.3C6.5 13.3 9.5 16.3 12 17.8" if S.name == "rounded"
            else "M12 7.2C10.5 5 6.5 5.3 6.5 9.3C6.5 13.3 9.5 16.3 12 18.1")
    disc = face + "C14.5 16.3 17.5 13.3 17.5 9.3C17.5 5.3 13.5 5 12 7.2Z"
    outer = "M12 2.8C17.6 2.8 20.5 6.3 20.5 11C20.5 15.5 18.5 19 15 21L9 21C5.5 19 3.5 15.5 3.5 11C3.5 6.3 6.4 2.8 12 2.8Z"
    return [shell(outer), detail(disc), dot(9.6, 10.3, 1.2), dot(14.4, 10.3, 1.2),
            mark(tri(S, [(11.2, 12.6), (12.8, 12.6), (12, 14.6)], 0.3))]


@icon("burrowing-owl", CAT, "Small owl on long legs standing at the mouth of its burrow",
      tags=["owl", "burrow", "prairie", "ground", "desert", "bird"])
def _(S):
    body = union(ellipse(8.5, 10, 4.6, 6), tri(S, [(4.2, 11), (3.5, 15.5), (6, 14.5)], 0.6))
    return [shell(body), dot(6.8, 8.3, 1.05), dot(10.2, 8.3, 1.05), mark(tri(S, [(7.8, 9.8), (9.2, 9.8), (8.5, 11.4)], 0.3)),
            line(seg(7, 16, 7, 20.5)), line(seg(10, 16, 10, 20.5)), line(seg(2.5, 20.5, 21.5, 20.5)),
            solid("M13.5 20.5C13.5 17 15.3 14.8 17.5 14.8C19.7 14.8 21.5 17 21.5 20.5Z")]


# ============================================================================ waterfowl

@icon("goose", CAT, "Goose standing with a long straight neck and a wedge bill",
      tags=["gander", "waterfowl", "farm", "honk", "canada goose", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = ("M8 12C9.5 10.5 12 10.2 15 10.5" + tip((15, 10.5), (20.5, 9.8), (19.5, 13), r)
            + "L19.5 13C19.3 16 16.5 17.8 13 17.8C9.5 17.8 6.8 16 6.8 14C6.8 13.2 7.2 12.6 8 12Z")
    neck = thick("M8.5 13L7.2 5", 2.8, S)
    head = circle(7, 5, 2.2)
    bill = tri(S, [(5.2, 3.8), (2.3, 5.6), (5.2, 6.8)], 0.5)
    return [shell(union(body, neck, head, bill)), mark(circle(5.3, 3.8, 0.9)), dot(7.4, 4.5, 0.75),
            detail("M11 13.5C13 15 15.8 15 17.8 13.4"), line(seg(11, 17.5, 11, 21)), line(seg(14, 17.5, 14, 21))]


@icon("mandarin-duck", CAT, "Mandarin duck floating with sail feathers on its back and a swept crest",
      tags=["duck", "waterfowl", "ornamental", "pond", "sail feathers", "bird"])
def _(S):
    body = "M3.5 12.5C5.5 14.5 8.5 15 12 14.8C16 14.6 20.5 14.2 20.8 16.5C21 19 17.5 20.5 12 20.5C7 20.5 3.8 18.5 3.5 12.5Z"
    head = union(circle(7, 9, 2.8), tri(S, [(6.5, 6.3), (13, 8), (8.8, 11)], 0.8))
    bill = tri(S, [(4.6, 9), (2.3, 10.8), (4.8, 11.4)], 0.5)
    sails = union(tri(S, [(12.5, 14.8), (14.5, 9.2), (16.5, 14.6)], 0.7), tri(S, [(16, 14.8), (18.8, 10), (19.8, 15)], 0.7))
    return [shell(union(body, head, bill)), shell(minus(sails, grow(union(body, head), 1.5))), dot(6.5, 8.6, 0.85)]


@icon("duck-with-ducklings", CAT, "Mother duck swimming with ducklings following in a line",
      tags=["ducklings", "family", "mother", "pond", "spring", "follow the leader"])
def _(S):
    r = L(S, 0, 0.8)
    body = "M2.5 10.5C4 12.3 6 12.8 8 12.6C10.5 12.4 12.5 12.6 12.5 14.4C12.5 16.4 10.3 17.5 7.5 17.5C4.5 17.5 2.6 15.5 2.5 10.5Z"
    mom = union(body, circle(8.5, 7.8, 2.3), tri(S, [(10.3, 7.2), (12.8, 8.2), (10.3, 9.4)], 0.5))

    def chick(x, y):
        return mark(union(ellipse(x, y, 1.9, 1.3), circle(x + 1.2, y - 1.6, 1.1),
                          poly([(x + 2.1, y - 1.9), (x + 3.2, y - 1.4), (x + 2.1, y - 1)], closed=True)))
    return [shell(mom), dot(8.9, 7.4, 0.7), chick(14.5, 16.1), chick(19.3, 16.1), water(S, 20.3)]


@icon("swan-couple", CAT, "Two swans facing each other with their necks forming a heart",
      tags=["swans", "love", "romance", "wedding", "valentine", "heart"])
def _(S):
    body = "M2.5 13.5C4 15.5 6.5 16 9.5 15.5L11.2 15.5C11.2 18.5 9 20 6.5 20C4 20 2.5 18 2.5 13.5Z"
    neck = "M10 15.5C6.5 13 3.8 10.5 4 7.5C4.2 4.5 7.8 4 9.8 6.5"
    head = union(circle(9.8, 6.8, 1.35), tri(S, [(10.6, 6), (12, 8.6), (10.2, 8)], 0.4))
    return [shell(body), line(neck), shell(head), shell(flip(body)), line(flip(neck)), shell(flip(head))]


@icon("loon", CAT, "Loon swimming low in the water with a dagger bill and a spotted back",
      tags=["common loon", "diver", "lake", "waterfowl", "canada", "bird"])
def _(S):
    body = "M6.5 13C9 11.4 12 11 15 11.3C17.5 11.6 19.5 12.8 20.8 15.5L6 15.5Z"
    neck = thick("M7.5 14L7 9.5", 3, S)
    head = circle(7, 8.6, 2.4)
    bill = tri(S, [(5, 7.8), (2.8, 9.4), (5.2, 9.8)], 0.5)
    return [shell(union(body, neck, head, bill)), dot(7.3, 8, 0.8), dot(12.5, 13.5, 0.8), dot(15, 13.4, 0.8), dot(17.5, 13.6, 0.8),
            water(S, 19)]


@icon("grebe", CAT, "Grebe floating with a small crest and a striped chick riding on its back",
      tags=["great crested grebe", "chick", "waterfowl", "lake", "parent", "bird"])
def _(S):
    body = "M3.5 12C5.5 14.5 8.5 15 12 14.8C16 14.6 20.5 14.2 20.8 16.5C21 19 17.5 20.5 12 20.5C7 20.5 3.8 18.5 3.5 12Z"
    head = union(circle(6.5, 8.5, 2.5), tri(S, [(6.3, 6.1), (9.8, 5), (8.8, 7.8)], 0.5))
    bill = tri(S, [(4.3, 8.3), (2.8, 9.8), (4.6, 10.3)], 0.4)
    chick = union(ellipse(16, 12.3, 2.5, 1.3), circle(13.8, 10.5, 1.3), poly([(12.7, 10.2), (11.5, 10.8), (12.7, 11.2)], closed=True))
    return [shell(union(body, head, bill)), dot(6.4, 8.3, 0.75), mark(chick)]


@icon("coot", CAT, "Round coot swimming with a pale shield running from its bill up the forehead",
      tags=["waterbird", "rail", "pond", "moorhen", "lake", "bird"])
def _(S):
    body = "M5 13C7.5 11 11 10.5 14.5 10.8C18.5 11.2 21 13.5 21 16C21 17.3 20 18 18.5 18L6 18C4.8 16.5 4.3 14.8 5 13Z"
    head = circle(7.5, 8.5, 3.3)
    shield = union(ellipse(6.1, 6.9, 0.9, 1.8), tri(S, [(5.2, 7.2), (2.4, 9.7), (5.7, 10.4)], 0.4))
    return [shell(union(body, head)), mark(shield), dot(8.4, 8, 0.8), water(S, 21)]


@icon("cormorant", CAT, "Cormorant standing on a post with its wings held open to dry",
      tags=["shag", "seabird", "drying wings", "fishing bird", "coast", "bird"])
def _(S):
    r = L(S, 0, 0.6)
    wl = [(10.5, 8.5), (5.5, 7), (2.5, 8), (3, 11.5), (4.3, 10.8), (5, 13), (6.5, 12), (7.8, 14), (10.5, 13.5)]
    body = union(ellipse(12, 11.5, 2.6, 4.5), thick("M12 8L12.5 5.5", 2.4, S), circle(12.8, 4.4, 1.9),
                 tri(S, [(11.3, 3.6), (8.5, 4.3), (9, 5.5), (11.3, 5.3)], 0.4),
                 poly(wl, closed=True, r=r), poly(fpts(wl), closed=True, r=r))
    return [shell(body), dot(13.3, 4, 0.7), shell(rect(10, 17.8, 4, 3.7, min(S.R, 1))), line(seg(10.8, 15.5, 10.8, 17.8)), line(seg(13.2, 15.5, 13.2, 17.8))]


@icon("anhinga", CAT, "Anhinga swimming with only its snake-like neck and dagger bill above the water",
      tags=["snakebird", "darter", "swamp", "water turkey", "wetland", "bird"])
def _(S):
    head = union(ellipse(12.6, 5.8, 2, 1.5), tri(S, [(11, 5), (3.5, 5.2), (11, 6.8)], 0.4))
    return [shell(head), dot(13, 5.4, 0.7), line("M14 6.8C16 8.5 16 10.5 14 12.5C12 14.5 12 16.5 13.5 18"),
            line("M9 18.5C10.5 17.8 11.8 17.6 13 18.2C14.5 19 15.8 19 17.5 18.3"), line("M4 21.3C9 19.8 15 19.8 20 21.3")]


@icon("pelican", CAT, "Pelican standing with a long bill and a large hanging throat pouch",
      tags=["seabird", "pouch", "fishing", "coast", "harbour", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    head = circle(8.8, 5.4, 2.4)
    bill = "M7 4.4L2.5 5.3C2.2 7.5 3.2 10.5 5.5 11C7.3 11.3 8.8 9.5 9.4 7.8Z"
    neck = thick("M9.8 7L10.5 11.5", 2.8, S)
    body = ("M10 11.5C12 10 15.5 10 17.5 11.5" + tip((17.5, 11.5), (21.3, 14.2), (18.3, 15.5), r)
            + "L18.3 15.5C17.5 17.5 15 18.3 12.5 18C10 17.7 8.5 15.5 9 13.5Z")
    return [shell(union(head, bill, neck, body)), dot(9.3, 4.8, 0.8), detail("M3.2 5.8L7.3 5.3"),
            detail("M12 13C13.5 14.8 15.5 15.3 17.5 14.8"), line(seg(12, 17.8, 12, 21)), line(seg(15, 17.8, 15, 21))]


@icon("gannet", CAT, "Gannet plunge diving straight down with its wings swept back above a splash",
      tags=["booby", "dive", "seabird", "plunge", "fishing", "splash"])
def _(S):
    r = L(S, 0, 0.6)
    body = ("M12 3.5C13.3 3.5 13.7 6 13.6 9C13.5 11 13.4 12.5 13 13.5" + tip((13, 13.5), (12, 16.5), (11, 13.5), r)
            + "L11 13.5C10.6 12.5 10.5 11 10.4 9C10.3 6 10.7 3.5 12 3.5Z")
    wl = [(11, 9.5), (5.5, 2.5), (7, 2.5), (11, 6.5)]
    return [shell(union(body, tri(S, wl, 0.6), tri(S, fpts(wl), 0.6))), dot(12, 11.3, 0.7),
            line(seg(12, 17.5, 12, 18.5)), line(seg(8.5, 17.8, 9.5, 18.8)), line(seg(15.5, 17.8, 14.5, 18.8)),
            line("M3 21C6 19.8 9 19.8 12 21C15 22.2 18 22.2 21 21")]


@icon("blue-footed-booby", CAT, "Booby standing with one big webbed foot raised in a courtship strut",
      tags=["booby", "seabird", "galapagos", "webbed feet", "courtship", "dance"])
def _(S):
    r = L(S, 0, 0.8)
    body = union(rot(ellipse(12.5, 10, 3.8, 5.2), -10, 12.5, 10), circle(10.5, 4.8, 2.3),
                 tri(S, [(8.5, 4), (3.5, 6.2), (8.8, 6.5)], 0.5), tri(S, [(15, 13.5), (18.5, 17.5), (15.5, 15.8)], 0.8))
    return [shell(body), dot(10.6, 4.4, 0.75), line(seg(13.5, 14.8, 13.5, 19.5)),
            mark(poly([(13.5, 18.5), (17.5, 21), (10.5, 21)], closed=True, r=L(S, 0, 0.5))),
            line(poly([(11, 14.8), (9, 16.5), (7, 15.3)], r=S.r)),
            mark(poly([(7.4, 15.1), (2.6, 13.2), (4.2, 17.4)], closed=True, r=L(S, 0, 0.5)))]


@icon("albatross", CAT, "Albatross gliding with very long narrow wings seen from above",
      tags=["seabird", "ocean", "glide", "wandering albatross", "southern ocean", "bird"])
def _(S):
    wl = [(11, 10.3), (7, 9.8), (2.8, 11.3), (7, 12), (11, 13.4)]
    body = union(ellipse(12, 12.5, 2, 4.2), circle(12, 7.8, 1.8), tri(S, [(11.3, 6.5), (12, 4.6), (12.7, 6.5)], 0.3),
                 tri(S, wl, 0.8), tri(S, fpts(wl), 0.8), "M10.8 15.5L13.2 15.5L13 18.2Q12 19.2 11 18.2Z")
    return [shell(body, stroke_miterlimit="2")]


@icon("seagull", CAT, "Gull standing with a stout bill, long folded wings and webbed feet",
      tags=["gull", "seabird", "beach", "coast", "harbour", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = ("M8.5 10.8C10.5 9.2 14 9.5 16 11" + tip((16, 11), (21.3, 15), (16.3, 14.8), r)
            + "L16.3 14.8C15 16.3 13 16.8 11 16.5C8.5 16 7 14 7.5 12Z")
    head = circle(8, 7.5, 2.8)
    bill = "M5.5 6.8L3 7.3C2.8 8.3 3 9.1 3.6 9.3L5.8 9.2Z"
    return [shell(union(body, head, bill), stroke_miterlimit="2.5"), dot(8.2, 6.8, 0.8), mark(circle(4, 8.8, 0.7)),
            detail("M10 12.5C12.5 12.5 15.5 13 18.3 14.5"),
            line(seg(10.5, 16.5, 10.5, 20)), line(seg(13.5, 16.5, 13.5, 20)),
            mark(poly([(10.5, 19.3), (7.8, 21.2), (11, 21.2)], closed=True)), mark(poly([(13.5, 19.3), (10.8, 21.2), (14, 21.2)], closed=True))]


@icon("tern", CAT, "Tern flying with slim pointed wings, a dark cap and a long forked tail",
      tags=["sea swallow", "seabird", "arctic tern", "coast", "flight", "bird"])
def _(S):
    body = union(ellipse(10, 13, 5, 1.9), circle(5.5, 12.3, 2),
                 tri(S, [(4, 13), (3, 16.3), (5.5, 14)], 0.3),
                 tri(S, [(14, 12), (21, 10.5), (16.8, 13.2), (21, 16.5), (14, 14.3)], 0.6),
                 tri(S, [(8, 12.5), (13, 3.2), (15, 4), (12.3, 12.3)], 0.8))
    cap = "M3.6 12C3.8 10.8 4.8 10.1 5.9 10.2C6.8 10.3 7.4 10.8 7.6 11.5Z"
    return [shell(body), mark(cap)]


@icon("puffin", CAT, "Puffin standing upright with a large triangular striped bill and a pale face",
      tags=["atlantic puffin", "seabird", "sea parrot", "cliff", "iceland", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = union(ellipse(13.5, 13.5, 5.5, 7), circle(12, 7.8, 4.3),
                 "M8.3 5C5.5 5.5 3.2 7.8 2.8 10.8" + tip((3.2, 10.8), (2.8, 11.3), (8.3, 11), r) + "L8.3 11Z")
    return [shell(body), detail(ellipse(12.5, 8, 2.4, 2.1)), dot(12.7, 7.5, 0.8), detail(seg(5.8, 6.8, 5.8, 10.8)),
            detail("M15 13.5C16.5 15.5 16.5 18 15.5 19.8"), line(seg(11.5, 20, 11.5, 21.5)), line(seg(15.5, 20, 15.5, 21.5))]


@icon("frigatebird", CAT, "Frigatebird perched with its throat pouch puffed into a round balloon",
      tags=["man o war bird", "seabird", "throat pouch", "courtship", "tropical", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = ("M9.5 7.8C12 6.5 15.5 7.5 17.5 10" + tip((17.5, 10), (21.5, 16.5), (16.5, 14), r)
            + "L16.5 14C15.5 15 14 15.3 12.5 15C11.5 13 10 10.5 9.5 7.8Z")
    head = union(circle(8.5, 6, 2), "M6.8 5.2L3 5.5C2.6 6.3 2.8 7.2 3.5 7.6L6.8 7.3Z")
    pouch = circle(8.5, 12.3, 3.8)
    return [shell(union(body, head)), shell(minus(pouch, grow(head, 0.3))), dot(8.6, 5.5, 0.7),
            line(seg(12.5, 15.2, 12.5, 19)), line(seg(3, 19.5, 21, 19.5))]


@icon("tropicbird", CAT, "Tropicbird flying with a pair of very long thin tail streamers",
      tags=["seabird", "tropical", "streamers", "long tail", "ocean", "bird"])
def _(S):
    body = union(ellipse(8.5, 10, 4.5, 2), circle(4.8, 9.3, 1.9),
                 tri(S, [(3.4, 8.8), (2.8, 11.5), (4.2, 10.5)], 0.2),
                 tri(S, [(6.5, 9.5), (9, 3), (10.8, 3.5), (10.5, 9.5)], 0.7))
    return [shell(body), dot(4.8, 9, 0.7), line("M12.5 10.3C15.5 11 18.5 12.5 21 15"), line("M12.3 11.3C15 12.8 17.5 15 19.5 18")]


@icon("skimmer-bird", CAT, "Skimmer flying low with its long lower bill slicing the water surface",
      tags=["black skimmer", "seabird", "skim", "coast", "fishing", "bird"])
def _(S):
    body = union(ellipse(13, 10.5, 5, 2), circle(7.5, 10, 2.1),
                 tri(S, [(17, 9.8), (21.3, 10.2), (17.5, 12)], 0.6),
                 tri(S, [(11, 9.5), (15, 3), (16.5, 3.5), (15, 9.5)], 0.6))
    bill = union(tri(S, [(6, 9.5), (4, 10.4), (6, 11)], 0.3), tri(S, [(6.3, 11), (3, 16.5), (7.5, 11.8)], 0.3))
    return [shell(union(body, bill), stroke_miterlimit="2.5"), dot(7.6, 9.6, 0.7), water(S, 18.3)]


@icon("sandpiper", CAT, "Small sandpiper running on thin legs along the edge of a wave",
      tags=["shorebird", "wader", "beach", "stint", "coast", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = union(rot(ellipse(12, 10.5, 4.5, 3), -8, 12, 10.5), circle(8, 7.5, 2.2),
                 tri(S, [(15.5, 9), (20, 9), (16, 12)], 0.6), tri(S, [(6, 7.2), (2.5, 8.5), (6.2, 8.2)], 0.2))
    return [shell(body), dot(8, 7, 0.7), line(poly([(11, 13), (9.5, 15.5), (7.5, 17.3)], r=S.r)),
            line(poly([(13, 13.2), (14, 15.5), (16, 17)], r=S.r)),
            line("M2.5 20.5C5 19.3 7 19.3 9.5 20.5C12 21.7 14 21.7 16.5 20.5C18 19.8 19.5 19.8 21.5 20.3")]


@icon("oystercatcher", CAT, "Stocky oystercatcher using its long blade bill to pry open a shell",
      tags=["shorebird", "wader", "shellfish", "mussel", "coast", "bird"])
def _(S):
    body = union(rot(ellipse(14, 9.5, 5.5, 3.6), -10, 14, 9.5), circle(8.5, 6.8, 2.6),
                 tri(S, [(18.5, 7.5), (21.3, 8.5), (19, 11)], 0.8))
    lower = "M3 19.5L9 19.5C9 21 7.6 21.5 6 21.5C4.4 21.5 3 21 3 19.5Z"
    upper = rot("M3 18.8L9 18.8C9 17.3 7.6 16.8 6 16.8C4.4 16.8 3 17.3 3 18.8Z", 30, 9, 19)
    return [shell(body), dot(8.8, 6.3, 0.8), line(seg(6.6, 8.3, 4.6, 14.3)), shell(lower), shell(upper),
            line(seg(12.8, 13, 12.8, 21)), line(seg(16, 12.5, 16, 21))]


@icon("avocet", CAT, "Slender avocet with a long thin bill curving sharply upward",
      tags=["pied avocet", "wader", "shorebird", "upturned bill", "wetland", "bird"])
def _(S):
    body = union(rot(ellipse(14, 10, 5.2, 2.6), -8, 14, 10), thick("M10 10.5C8.8 10 8.3 9 8.3 8", 2.2, S), circle(8, 7, 1.9),
                 tri(S, [(18.5, 8.5), (21.3, 9.2), (18.8, 11)], 0.6))
    return [shell(body), dot(8, 6.6, 0.7), line("M6.3 7.6C4.5 8 3.2 7.3 2.8 5"), detail("M11.5 9.5C13.5 10.8 16 10.8 18 9.5"),
            line(seg(13, 12.5, 12, 21)), line(seg(15.5, 12.3, 16.5, 21))]


@icon("stilt-bird", CAT, "Small stilt balanced on extremely long thin legs with a needle bill",
      tags=["black-winged stilt", "wader", "long legs", "shorebird", "wetland", "bird"])
def _(S):
    r = L(S, 0, 0.6)
    body = union(rot(ellipse(13.5, 5.8, 4.5, 2), -8, 13.5, 5.8), circle(8.8, 4.3, 1.8),
                 tri(S, [(17.3, 4.5), (20.8, 5), (17.5, 6.8)], 0.5))
    return [shell(body), dot(8.7, 3.9, 0.65), line(seg(7, 4.6, 3, 5.6)), line(seg(12.5, 7.8, 10.5, 21)), line(seg(14.8, 7.8, 16.8, 21))]


@icon("lapwing", CAT, "Plump lapwing with a thin wispy crest curling up from the back of its head",
      tags=["peewit", "plover", "crest", "farmland", "wader", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = union(ellipse(13, 12.5, 6.5, 4.5), circle(8, 9, 3),
                 tri(S, [(18.5, 10.5), (21.3, 12), (19, 14.5)], 0.8), tri(S, [(5.3, 8.5), (3, 9.8), (5.4, 10.6)], 0.3))
    return [shell(body), dot(7.6, 8.6, 0.8), line("M9.5 6.5C10.5 4.5 13 3 15.5 3.5C16.8 3.8 17 5 16 5.5"),
            detail("M10.5 14.5C13 16 16 16 18.3 14"), line(seg(11.5, 16.8, 11.5, 21)), line(seg(14.5, 16.8, 14.5, 21))]


@icon("heron", CAT, "Heron standing in shallow water with its neck drawn back in an S curve",
      tags=["grey heron", "great blue heron", "wader", "fishing", "pond", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = ("M11 9.5C13.5 7.5 17 7.5 19 9.5" + tip((19, 9.5), (21.3, 13.5), (17.5, 13), r)
            + "L17.5 13C15.5 14.8 12.5 14.8 11 13Z")
    neck = thick("M12 10.5C9 10.5 7.8 9 8.5 7C9.2 5.3 9 4.3 8.5 3.8", 2.4, S)
    head = circle(8, 3.8, 1.8)
    bill = tri(S, [(6.5, 3.2), (2.5, 4.3), (6.5, 4.8)], 0.3)
    return [shell(union(body, neck, head, bill)), dot(8.2, 3.5, 0.65), line(seg(13.5, 14, 13.5, 18.5)), line(seg(16, 14, 16, 18.5)),
            water(S, 20.3, 8, 21.5)]


@icon("egret", CAT, "Slender egret standing on one leg with long lacy plumes from its back",
      tags=["great egret", "white heron", "wader", "plumes", "wetland", "bird"])
def _(S):
    body = rot(ellipse(13.5, 10.5, 4.5, 2.4), -15, 13.5, 10.5)
    neck = thick("M10 10.5C8 9 8.5 7 9.5 6C10.5 5 10 3.8 9 3.8", 2, S)
    head = circle(8.8, 3.8, 1.6)
    bill = tri(S, [(7.5, 3.3), (3, 4.3), (7.4, 4.6)], 0.3)
    return [shell(union(body, neck, head, bill)), dot(9, 3.5, 0.6), line("M15 9C18 9.5 20 11.5 21 14.5"), line("M15.5 11.3C17.5 12.5 18.5 14 19 16"),
            line(seg(12.5, 12.8, 12.5, 21)), line(poly([(13.5, 13), (15.5, 15), (13.2, 16.5)], r=S.r))]


@icon("bittern", CAT, "Streaked bittern standing upright among reeds with its bill pointing to the sky",
      tags=["reeds", "marsh", "camouflage", "heron", "wetland", "bird"])
def _(S):
    body = ("M9 8.5C9 6.5 10 5.2 11.5 5L12 2.8L13.2 5.2C14.8 6 15.5 8 15.5 11C15.5 15.5 14.8 18.5 13.5 20.5L11 20.5C9.5 17.5 9 13 9 8.5Z")
    return [shell(body), dot(11.4, 7.3, 0.65), detail("M12.3 10C12.8 13 12.8 15.5 12.3 18"),
            line("M5 21C5 15 5.2 10 4.5 5"), line("M19 21C19 16 19.3 12 20.5 7.5"), line("M5 13C6.3 11 7 9.5 7 8")]


@icon("stork", CAT, "Stork standing on long legs with a straight neck, heavy bill and dark wing edges",
      tags=["white stork", "wader", "nest", "migration", "long legs", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = ("M10.5 9.5C12.5 7.8 16 7.8 18.5 9.3" + tip((18.5, 9.3), (21.3, 12.5), (17.5, 12.3), r)
            + "L17.5 12.3C15.5 14 12.5 14 10.5 12.5Z")
    neck = thick("M11.5 10.5L8.2 5.3", 2.6, S)
    head = circle(7.8, 4.8, 1.9)
    bill = tri(S, [(6.4, 4), (2.8, 8.5), (7, 6.3)], 0.3)
    return [shell(union(body, neck, head, bill)), dot(8, 4.4, 0.65), mark(tri(S, [(16.5, 9.8), (19.8, 10.8), (18.5, 11.8), (16, 11.6)], 0.4)),
            line(seg(13.3, 13.3, 13.3, 21)), line(seg(15.8, 13.3, 15.8, 21))]


@icon("stork-with-baby", CAT, "Stork flying with a swaddled baby hanging from its bill",
      tags=["baby delivery", "birth", "newborn", "baby shower", "pregnancy", "announcement"])
def _(S):
    body = union(ellipse(16, 5.5, 4.3, 1.9), thick("M12 5.5L8 6", 2, S), circle(7.3, 6, 1.6),
                 tri(S, [(19.8, 4.7), (21.5, 5.5), (20, 6.5)], 0.4), tri(S, [(14, 5), (17, 2.3), (18.8, 2.8), (17.3, 5)], 0.6))
    bill = tri(S, [(6, 5.5), (4.2, 7), (6, 6.9)], 0.2)
    wrap = ellipse(13.5, 17.5, 6, 3)
    head = circle(5, 17, 2.4)
    return [shell(union(body, bill), stroke_miterlimit="2.5"), line(poly([(5, 8), (11.5, 14.5)], r=S.r)),
            shell(minus(wrap, grow(head, 2))), shell(head), detail("M12 15.3C13.5 17 14 18.5 13.5 20.2")]


@icon("crane-bird", CAT, "Crane standing tall with a crown patch, long neck and bushy drooping tail",
      tags=["common crane", "sandhill crane", "whooping crane", "wader", "migration", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = ("M10.5 10C12.5 8.3 16 8.5 18 10.5C19.5 12 21 14 21 16" + tip((21, 16), (19.5, 15), (18, 16.5), r)
            + tip((19.5, 15), (18, 16.5), (16.5, 14.2), r) + "L16.5 14.2C14 14.5 12 14 10.5 13Z")
    neck = thick("M11.5 11C10.5 8 9.5 6 9 4.5", 2.4, S)
    head = circle(8.8, 4.2, 1.9)
    bill = tri(S, [(7.3, 3.6), (3, 5), (7.4, 5.1)], 0.3)
    return [shell(union(body, neck, head, bill)), mark(ellipse(9, 2.9, 1.2, 0.7)), dot(8.8, 4.4, 0.6),
            line(seg(13, 14, 13, 21)), line(seg(15.5, 14.3, 15.5, 21))]


@icon("crowned-crane", CAT, "Crowned crane head and neck topped with a stiff spray of bristle feathers",
      tags=["grey crowned crane", "africa", "crown", "crest", "uganda", "bird"])
def _(S):
    neck = thick("M12.5 21C12.5 17 12 14.5 11 12", 3.2, S)
    head = circle(11, 10.5, 3)
    bill = tri(S, [(8.5, 9.8), (4.5, 12), (8.6, 11.8)], 0.3)
    spray = []
    for a in (-160, -125, -90, -55):
        x1, y1 = 11.5 + 6 * math.cos(math.radians(a)), 7.5 + 5 * math.sin(math.radians(a))
        spray.append(line(seg(11.5, 7.5, x1, y1)))
        spray.append(dot(x1, y1, 1.1))
    return [shell(union(neck, head, bill)), detail(ellipse(12.3, 10.8, 1.2, 1.3)), dot(10.3, 9.8, 0.6), *spray]


@icon("marabou-stork", CAT, "Hunched marabou stork with a bald head, huge bill and hanging throat sac",
      tags=["stork", "scavenger", "africa", "throat sac", "undertaker bird", "bird"])
def _(S):
    r = L(S, 0, 1)
    body = ("M11 8.5C12 5 17.5 4.8 19.8 8.5C21 10.8 21 13.5 20.5 15.5" + tip((20.5, 15.5), (21.3, 18), (17.5, 16.5), r)
            + "L17.5 16.5C14.5 17.5 12 16.5 11.3 14C10.8 12.3 10.7 10.3 11 8.5Z")
    head = circle(8.5, 5, 1.9)
    bill = tri(S, [(7, 4.2), (3.2, 10.5), (8.3, 6.8)], 0.4)
    sac = ellipse(9, 11.8, 1.5, 2.2)
    return [shell(union(body, head, bill)), shell(sac), dot(8.8, 4.6, 0.6),
            detail("M14.5 8.2C16.3 9.8 17 12.5 16.8 15.5"), line(seg(13.5, 16.8, 13.5, 21)), line(seg(16.5, 16.8, 16.5, 21))]


@icon("ibis", CAT, "Ibis standing with a long bill that curves smoothly downward",
      tags=["sacred ibis", "scarlet ibis", "wader", "curved bill", "wetland", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = ("M9.5 9.5C11.5 7.8 15 7.8 17.5 9.3" + tip((17.5, 9.3), (21.3, 12.8), (16.5, 12.8), r)
            + "L16.5 12.8C14.5 14.3 11.5 14.2 9.8 12.8C8.8 12 8.8 10.5 9.5 9.5Z")
    neck = thick("M10 10.5C8.5 9 8 7 8.5 5.5", 2.4, S)
    head = circle(8.5, 5.2, 2)
    return [shell(union(body, neck, head)), dot(8.8, 4.7, 0.65), line("M6.8 5.5C4.5 5.8 3.2 7.5 3 10.5"),
            line(seg(12, 13.8, 12, 21)), line(seg(14.8, 13.8, 14.8, 21))]


@icon("spoonbill", CAT, "Wading bird with a long flat bill ending in a wide rounded spoon tip",
      tags=["roseate spoonbill", "wader", "spoon", "wetland", "flat bill", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = ("M10.5 9.5C12.5 7.8 16 7.8 18.5 9.3" + tip((18.5, 9.3), (21.3, 12.8), (17.3, 12.8), r)
            + "L17.3 12.8C15.3 14.3 12.3 14.2 10.8 12.8Z")
    neck = thick("M11.5 10.5C10 9 9.5 7.5 9.8 6", 2.4, S)
    head = circle(9.8, 5.3, 1.9)
    spoon = ellipse(4, 6.2, 1.8, 1.6) if S.name == "rounded" else poly([(4, 4.4), (5.8, 5.4), (5.4, 7.6), (3.2, 8), (2.4, 6)], closed=True)
    return [shell(union(body, neck, head, spoon)), dot(10, 4.9, 0.6), line(seg(8, 5.5, 5.5, 6)),
            line(seg(13, 13.8, 13, 21)), line(seg(15.8, 13.8, 15.8, 21))]


@icon("shoebill", CAT, "Tall shoebill with a massive clog-shaped bill ending in a small hook",
      tags=["whale-headed stork", "shoe-billed stork", "africa", "swamp", "big bill", "bird"])
def _(S):
    r = L(S, 0, 1)
    head = circle(12.5, 6.5, 3.8)
    bill = ("M10 4.3L4 5C2.8 5.3 2.5 6.8 3.2 7.5" + tip((3.2, 7.5), (3.6, 8.8), (4.5, 7.8), L(S, 0, 0.4))
            + "L4.5 7.8C5.8 9 8 10 10.5 9.5Z")
    body = ("M11 9.5C13 9.5 17 10.5 18.5 13.5C19.5 15.5 19.5 17.5 19 19.5" + tip((19, 19.5), (20.8, 21.3), (16.5, 20.8), r)
            + "L16.5 20.8L13 20.8C11 18.5 10 15 10.5 12Z")
    return [shell(union(head, bill, body)), dot(13.5, 5.8, 0.85), detail("M4.6 6.8C6.5 7.2 8.5 7 10.3 6.6"),
            detail("M13.5 12.5C15.5 14 16.5 16.3 16.5 18.5")]


@icon("hamerkop", CAT, "Hamerkop whose crest and bill together make a hammer-shaped head",
      tags=["hammerkop", "hammerhead stork", "africa", "wader", "crest", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    head = union(circle(9, 6, 2.3), tri(S, [(10.5, 4.3), (16, 5.2), (10.8, 7.8)], 0.8), tri(S, [(7.5, 5), (3, 6.3), (7.5, 7.5)], 0.4))
    neck = thick("M9.5 7.5L10.5 11", 2.4, S)
    body = ("M9.5 11.5C11.5 10 15 10 17 11.5" + tip((17, 11.5), (20.8, 15), (16.5, 15), r)
            + "L16.5 15C14.5 16.5 11.5 16.3 10 15C9 14 8.8 12.5 9.5 11.5Z")
    return [shell(union(head, neck, body), stroke_miterlimit="2.5"), dot(8.8, 5.6, 0.7), line(seg(11.8, 16, 11.8, 21)), line(seg(14.5, 16, 14.5, 21))]


@icon("jacana", CAT, "Jacana walking on a floating lily pad on very long spread toes",
      tags=["lily trotter", "jesus bird", "wader", "lily pad", "pond", "bird"])
def _(S):
    r = L(S, 0, 0.7)
    body = union(rot(ellipse(13, 6.5, 4.3, 2.4), -10, 13, 6.5), circle(8.5, 4.3, 1.9),
                 tri(S, [(6.8, 3.8), (4, 4.8), (6.9, 5.4)], 0.3), tri(S, [(17, 5.2), (19.8, 6), (17.3, 7.8)], 0.5))
    pad = minus(ellipse(12, 19.5, 9, 2.2), tri(S, [(12, 19.5), (15, 16.5), (17, 17)], 0))
    return [shell(body), dot(8.5, 3.9, 0.65), line(poly([(12, 8.8), (11, 12.5), (10, 15.5)], r=S.r)), line(seg(14.5, 8.8, 15.5, 15.5)),
            line(seg(4.5, 15.5, 20, 15.5)), shell(pad)]


@icon("kingfisher", CAT, "Stocky kingfisher perched on a stick over water with a long dagger bill",
      tags=["halcyon", "fishing", "river", "perched", "blue bird", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    head = circle(10.5, 7, 3.6)
    bill = tri(S, [(7.5, 5.8), (2.8, 8.2), (7.5, 9.2)], 0.3)
    body = ("M8.5 9.5C8.5 12.5 10.5 15 13 15.5" + tip((13, 15.5), (17.5, 17.5), (15.5, 13.5), r)
            + "L15.5 13.5C15.5 10 14.5 7.5 12.5 7Z")
    return [shell(union(head, bill, body), stroke_miterlimit="2.5"), dot(10.3, 6.3, 0.9), detail("M11.5 11C12.3 12.5 13.5 13.3 14.5 13.5"),
            line(seg(5, 16.5, 20, 16.5)), water(S, 20.5)]


@icon("penguin-with-chick", CAT, "Adult penguin standing with a small fluffy chick in front of it",
      tags=["penguin family", "emperor penguin", "chick", "parent", "antarctic", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    adult = union(ellipse(9.5, 11, 5.5, 8.5), tri(S, [(4.5, 9), (2.5, 15), (5, 14)], 0.6))
    chick = union(circle(17, 16.3, 3.8), circle(16.8, 11.5, 2.5))
    return [shell(minus(adult, grow(chick, 1.5))), detail("M11.5 5.5C13 8 13.5 11 13 14"), dot(8, 6, 1), mark(tri(S, [(5.5, 7), (3.2, 8), (5.5, 8.6)], 0.3)),
            shell(chick), dot(16, 11.2, 0.8), mark(tri(S, [(14.6, 11.6), (13, 12.6), (14.8, 12.8)], 0.2)),
            mark(ellipse(8, 20.3, 2, 0.9))]


@icon("rockhopper-penguin", CAT, "Rockhopper penguin in side view with spiky tufts above its eyes",
      tags=["penguin", "crested penguin", "tufts", "antarctic", "subantarctic", "bird"])
def _(S):
    r = L(S, 0, 0.6)
    body = union(ellipse(12.5, 13, 5, 7.5), circle(11, 7, 3.5), tri(S, [(8, 6.3), (4, 8), (8.3, 8.3)], 0.4))
    return [shell(body), dot(10.5, 6.5, 0.85), line(poly([(12.3, 5.7), (16, 3.5)], r=0)), line(poly([(12.8, 7), (17.5, 6.8)], r=0)),
            line(poly([(12, 4.6), (14.2, 2.2)], r=0)),
            detail("M14.5 10.5C16.5 13 16.5 16 15 18.5"), mark(ellipse(11, 20.8, 2.3, 0.9))]


@icon("ostrich", CAT, "Ostrich standing with a small head on a long bare neck and long legs",
      tags=["ratite", "flightless", "africa", "savanna", "fast runner", "bird"])
def _(S):
    r = L(S, 0, 1)
    body = ("M9 10C10.5 7.8 14.5 7.5 17.5 8.5" + tip((17.5, 8.5), (21.3, 7.5), (19.8, 11.5), r)
            + "L19.8 11.5C19.5 13.5 17 14.5 14 14.5C11 14.5 8.8 13 9 10Z")
    head = union(ellipse(6.5, 3.3, 1.8, 1.4), tri(S, [(5, 2.8), (3, 3.8), (5, 4.2)], 0.3))
    return [shell(union(body, head)), dot(6.8, 3, 0.55), line("M7.3 4.5C7.5 7 8.5 9.5 10.5 10.5"),
            line(poly([(12.5, 14), (11.5, 17.5), (12, 21), (10, 21)], r=S.r)), line(poly([(15.5, 14), (16.5, 17.5), (15.5, 21), (17.5, 21)], r=S.r))]


@icon("ostrich-head-in-sand", CAT, "Ostrich with its neck bent down and its head buried in a mound of sand",
      tags=["denial", "avoidance", "ignore", "hiding", "head in sand", "ostrich"])
def _(S):
    r = L(S, 0, 1)
    body = ("M10 7.5C11.5 5 15 4.5 18 5.5" + tip((18, 5.5), (21.3, 4.5), (20, 8.5), r)
            + "L20 8.5C19.8 10.5 17.5 11.8 14.5 11.8C11.5 11.8 9.8 10 10 7.5Z")
    mound = "M2.5 21C3 17.5 5 16 7.5 16C10 16 12 17.5 12.5 21Z"
    return [shell(body), line("M10.5 8.5C8.5 8.5 7 10.5 7.3 14.5"), shell(mound),
            line(poly([(13, 11.5), (12.8, 15), (14.5, 21)], r=S.r)), line(poly([(16.5, 11.5), (17.8, 15.5), (17.5, 21), (19.5, 21)], r=S.r))]


@icon("emu", CAT, "Emu standing with a shaggy drooping body, long neck and strong legs",
      tags=["ratite", "flightless", "australia", "outback", "big bird", "bird"])
def _(S):
    r = L(S, 0, 0.6)
    body = ("M8.5 10.5C9.5 7.5 13.5 6.5 17 7.5C19.5 8.3 21 10.5 21 13" + tip((21, 13), (20.5, 15.5), (19, 14.2), r)
            + tip((20.5, 15.5), (19, 14.2), (17.8, 16.2), r) + tip((19, 14.2), (17.8, 16.2), (16.3, 14.5), r)
            + tip((17.8, 16.2), (16.3, 14.5), (14.8, 16.3), r) + tip((16.3, 14.5), (14.8, 16.3), (13.3, 14.5), r)
            + tip((14.8, 16.3), (13.3, 14.5), (11.5, 15.8), r) + tip((13.3, 14.5), (11.5, 15.8), (10.5, 13.5), r)
            + "L10.5 13.5C9 13 8.2 12 8.5 10.5Z")
    neck = thick("M10 10C8.5 8 8 6 7.8 4.5", 2.4, S)
    head = union(circle(7.5, 3.8, 1.7), tri(S, [(6.2, 3.3), (4, 4.3), (6.2, 4.6)], 0.3))
    return [shell(union(body, neck, head)), dot(7.6, 3.4, 0.55), line(seg(13, 15.5, 12, 21)), line(seg(16, 15.8, 17, 21))]


@icon("cassowary", CAT, "Cassowary head and neck with a tall helmet casque and hanging wattles",
      tags=["ratite", "casque", "rainforest", "australia", "new guinea", "bird"])
def _(S):
    casque = "M10.5 7C10.5 4.5 12 2.6 14.5 2.8C15.8 3 16.3 4.5 15.5 7Z"
    head = union(ellipse(13, 8.5, 3.3, 2.5), tri(S, [(10, 7.5), (5, 10.3), (10.3, 10.3)], 0.4))
    neck = "M12.2 10L15.8 10C16.3 14 16.8 18 17.3 21.5L13.7 21.5C13.3 18 12.8 14 12.2 10Z"
    wattles = union(ellipse(10.5, 14, 1.2, 2), ellipse(8, 13.2, 1.1, 1.8))
    return [shell(union(casque, head, neck)), shell(wattles), dot(13, 8, 0.8)]


@icon("kiwi-bird", CAT, "Round kiwi bird with no visible wings and a very long thin bill",
      tags=["kiwi", "new zealand", "flightless", "nocturnal", "ratite", "bird"])
def _(S):
    body = union(ellipse(14, 11.5, 6.8, 5.5), circle(8.5, 9.5, 2.5))
    return [shell(body), dot(8.5, 8.8, 0.7), line("M6.5 10.5C5 13 4 16 3.2 19.5"),
            line(poly([(12, 16.5), (11.5, 20.5), (9.8, 20.5)], r=S.r)), line(poly([(16, 16.5), (16.5, 20.5), (14.8, 20.5)], r=S.r))]


@icon("dodo", CAT, "Plump dodo with a large hooked bill, tiny wings and a curly tail tuft",
      tags=["extinct", "mauritius", "flightless", "dodo bird", "extinction", "bird"])
def _(S):
    body = union(ellipse(13.5, 13, 6.5, 5.8), circle(8.5, 6.5, 2.8))
    bill = "M6.5 5C4.5 5 3 6 3 8C3 9 3.3 9.8 4 10.5L4.5 9.3L7 9.3C8 8.5 8 7 7.5 6Z"
    neck = thick("M8.5 8L9 11", 3.5, S)
    return [shell(union(body, bill, neck)), dot(9, 5.8, 0.8), detail("M12 11.5C13.5 13 15 13.3 16.5 12.5"),
            line("M19.5 9.5C20.5 8 21.5 8 21.5 9.3"), line("M20 11C21 10.5 21.5 11.5 21 12.3"),
            line(seg(12, 18.5, 12, 21)), line(seg(15.5, 18.5, 15.5, 21))]


@icon("cockatoo", CAT, "Cockatoo perched with a tall fanned crest raised and a curved beak",
      tags=["parrot", "crest", "australia", "pet bird", "sulphur-crested", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    head = circle(10, 9, 3.3)
    beak = "M7.2 7.8C5.3 8 4.5 9.5 5 11.5L6.5 10.8L7.8 12Z"
    crest = union(tri(S, [(9, 6.3), (7.5, 2.3), (10.8, 6)], 0.5), tri(S, [(10.3, 6), (12, 2.2), (12.3, 6.8)], 0.5),
                  tri(S, [(12, 6.8), (15.5, 3.8), (13.1, 8.3)], 0.5))
    body = ("M8 11.5C7.5 15 9.5 17.5 12.5 18.3" + tip((12.5, 18.3), (17, 21.5), (15.5, 16.5), r)
            + "L15.5 16.5C16.2 12.5 14.5 9 11.5 8.5Z")
    return [shell(union(head, beak, crest, body)), dot(10.5, 8.8, 0.85), detail("M7.5 8.6C8.1 9.6 8.1 10.6 7.4 11.5"),
            line(seg(6, 19, 15.5, 19))]


@icon("lovebirds", CAT, "Two small parrots on a branch facing each other with a heart between them",
      tags=["love", "couple", "romance", "valentine", "parrots", "affection"])
def _(S):
    r = L(S, 0, 0.8)
    half = union(circle(6.5, 10, 2.8), ellipse(6, 14.5, 3, 4), tri(S, [(9, 9.3), (10.3, 10.8), (8.8, 11.8)], 0.3),
                 tri(S, [(4.3, 16.5), (2.8, 19.8), (6, 18)], 0.6))
    heart = "M12 8.5C11.2 7 9.8 7.2 9.8 8.5C9.8 9.5 11 10.5 12 11.3C13 10.5 14.2 9.5 14.2 8.5C14.2 7.2 12.8 7 12 8.5Z"
    return [shell(half), shell(flip(half)), dot(7.3, 9.6, 0.7), dot(16.7, 9.6, 0.7), mark(heart), line(seg(2.5, 19.3, 21.5, 19.3))]


@icon("toucan", CAT, "Toucan perched with an enormous banana-shaped bill almost as long as its body",
      tags=["tropical", "rainforest", "big beak", "exotic", "jungle", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    head = circle(14, 7.5, 3)
    bill = "M11.5 5.5C8 4.5 4.5 5 2.8 7.5C4.5 9.3 8 10.2 11.8 9.5Z"
    body = ("M11.5 9C11 13 12.3 16 14 17.5" + tip((14, 17.5), (15.5, 21.3), (16.8, 17.3), r)
            + "L16.8 17.3C18 14 17.8 10 16.5 8Z")
    return [shell(union(head, bill, body)), dot(14.3, 7, 0.85), detail("M3.8 7.6C6.5 7.9 9 7.6 11.3 7.3"),
            detail("M13.2 11C13.2 13 13.8 14.5 14.7 15.5"), line(seg(10, 18, 20, 18))]


@icon("hornbill", CAT, "Hornbill head and neck with a big curved bill topped by a horn-like casque",
      tags=["great hornbill", "casque", "tropical", "rainforest", "asia", "bird"])
def _(S):
    head = circle(15, 8.5, 3.5)
    bill = "M12.5 7.5C9 7.3 5.5 9.5 3 13.5C6.5 12.5 9.5 12 12.5 11.5Z"
    casque = "M12.5 7.5C11 5.5 8 5.5 6 7.5C5.5 8 5.8 8.8 6.5 8.6C8.5 8 10.5 7.8 12.5 8Z"
    neck = "M13.5 10.5L18.5 10.5C18.8 14.5 19.2 18 19.5 21.5L15.5 21.5C15.2 18 14.5 14 13.5 10.5Z"
    return [shell(union(head, bill, casque, neck)), dot(15.5, 8, 0.85), detail("M5.8 11.7C8 10.5 10.3 10 12.3 9.8")]


@icon("hummingbird", CAT, "Hummingbird hovering beside a flower with its long needle bill in the bloom",
      tags=["hummer", "nectar", "hover", "flower", "garden", "bird"])
def _(S):
    body = union(rot(ellipse(16, 11.5, 3.5, 2), 30, 16, 11.5), circle(13.5, 8.8, 1.9),
                 tri(S, [(18.3, 13), (21.3, 17.5), (19.3, 15)], 0.5))
    wing = tri(S, [(15.5, 10), (18.8, 3), (20.8, 3.7), (17.5, 11)], 0.8)
    c = (5.5, 9.5)
    petals = union(*[circle(c[0] + 2.3 * math.cos(math.radians(a)), c[1] + 2.3 * math.sin(math.radians(a)), 1.7) for a in range(-90, 270, 72)])
    return [shell(union(body, wing)), dot(13.4, 8.4, 0.65), line(seg(11.7, 9.1, 8.3, 9.6)), shell(petals), dot(5.5, 9.5, 0.9),
            line("M5.5 13.3C5.5 16 5.8 18.5 6.3 21")]


@icon("woodpecker", CAT, "Woodpecker clinging to a tree trunk with its tail braced, tapping with its bill",
      tags=["peck", "tree", "drumming", "forest", "knock", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = union(rot(ellipse(9.5, 12, 2.8, 5), -15, 9.5, 12), circle(11, 6.5, 2.5),
                 tri(S, [(11.8, 16), (13.3, 21), (9.5, 17)], 0.5))
    bill = tri(S, [(13, 5.5), (15.5, 6.3), (13.1, 7.5)], 0.3)
    crest = mark(tri(S, [(9, 4.8), (9.5, 3.5), (11.5, 4.1)], 0.3))
    return [shell(union(body, bill)), crest, dot(11.5, 6.2, 0.75), shell(rect(17, 2.5, 4.5, 19, min(S.R, 1.5))),
            line(seg(13, 3.6, 14.5, 2.4)), line(seg(13.5, 9.3, 15, 10.3)), detail("M7.8 10.5C8.2 12.5 9 14 10.2 15")]


@icon("hoopoe", CAT, "Hoopoe with a tall fan-shaped crest and a long thin downcurved bill",
      tags=["crest", "fan crest", "eurasian hoopoe", "israel", "garden", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = ("M8.5 12C10 10 14 9.8 16.5 11" + tip((16.5, 11), (21.3, 14.5), (16.5, 15), r)
            + "L16.5 15C14.5 17 11 17 9.5 15.5C8.5 14.5 8.2 13 8.5 12Z")
    head = circle(8.5, 9.5, 2.3)
    c = (9.5, 9.5)
    fan = []
    for a in (-165, -135, -105, -75, -45):
        x, y = c[0] + 6.8 * math.cos(math.radians(a)), c[1] + 6.8 * math.sin(math.radians(a))
        fan.append(line(seg(c[0] + 2.5 * math.cos(math.radians(a)), c[1] + 2.5 * math.sin(math.radians(a)), x, y)))
        fan.append(dot(x, y, 1.1))
    return [shell(union(body, head)), dot(8, 9.3, 0.7), line("M6.5 10.3C4.8 11 3.8 12.5 3.3 14.5"), *fan,
            detail("M11 13.5C12.5 14.5 14.5 14.5 16.5 13.3"), line(seg(11.5, 16.8, 11.5, 21)), line(seg(14, 16.8, 14, 21))]


@icon("kookaburra", CAT, "Stocky kookaburra perched on a branch with a big head and its bill open wide",
      tags=["laughing kookaburra", "australia", "kingfisher", "laugh", "bush", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    head = circle(11, 7.5, 4)
    upper = tri(S, [(8, 5.5), (2.8, 5.5), (7.5, 8)], 0.3)
    lower = tri(S, [(7.5, 9), (3.5, 11), (8.8, 10.8)], 0.3)
    body = ("M8.5 10.5C8.5 14 10.5 16.5 13 17" + tip((13, 17), (17, 20.5), (16, 15.5), r)
            + "L16 15.5C16.5 11.5 15.5 8.5 13 7.5Z")
    return [shell(union(head, upper, lower, body)), dot(11.5, 6.5, 0.9), detail("M10.5 5.8L15 7"),
            line(seg(6, 18.3, 18, 18.3)), line("M2.8 13.5L4.3 14.5"), line("M4.5 15.5L5.3 17")]


@icon("bee-eater", CAT, "Slender bee-eater perched on a twig holding a bee in its curved bill",
      tags=["european bee-eater", "insect eater", "colourful", "perched", "tail streamers", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = union(rot(ellipse(11.5, 9.5, 2.6, 4.3), 30, 11.5, 9.5), circle(8.5, 5.5, 2.3),
                 tri(S, [(13, 12), (15, 13.5), (13, 14.5)], 0.4))
    bee = ellipse(3.8, 9, 1.8, 1.3)
    return [shell(body), dot(8.3, 5, 0.7), line("M6.5 6C5.5 6.5 5 7 4.8 7.8"), mark(bee), line(seg(14.5, 14, 20.5, 20.5)),
            line(seg(6.5, 13.8, 16, 13.8))]


@icon("motmot", CAT, "Motmot perched with a long tail ending in bare shafts and racket-shaped tips",
      tags=["blue-crowned motmot", "racket tail", "tropical", "rainforest", "pendulum tail", "bird"])
def _(S):
    body = union(rot(ellipse(9, 7.5, 3, 4.3), 20, 9, 7.5), circle(6.3, 4.5, 2.3),
                 tri(S, [(4.3, 4), (2.8, 5.5), (4.5, 5.8)], 0.3))
    racket = rot(ellipse(17.5, 18, 1.6, 2.6) if S.name == "rounded" else poly([(17.5, 15.2), (19.1, 18), (17.5, 20.8), (15.9, 18)], closed=True), -35, 17.5, 18)
    return [shell(body), dot(6.4, 4, 0.7), line(seg(11.2, 11.8, 16, 16.3)),
            shell(racket), line(seg(3, 12.3, 13.5, 12.3))]


@icon("quetzal", CAT, "Quetzal perched with a rounded crest and very long flowing tail streamers",
      tags=["resplendent quetzal", "guatemala", "tropical", "cloud forest", "long tail", "bird"])
def _(S):
    body = union(rot(ellipse(8.5, 8.5, 3.2, 4.3), 15, 8.5, 8.5), circle(6.8, 5, 2.5),
                 tri(S, [(4.5, 4.8), (3, 6), (4.7, 6.4)], 0.3),
                 "M4.8 3.8C5.2 1.8 8.5 1.5 9.5 3.5Z")
    return [shell(body), dot(6.6, 4.7, 0.7), line("M10 12.5C12 16 15.5 18.5 21 19.5"), line("M9 13C10.5 17 14 20.5 18.5 21.5"),
            line(seg(3, 13.3, 12.5, 13.3))]


@icon("roadrunner", CAT, "Roadrunner running fast with a shaggy crest, a level tail and speed lines",
      tags=["greater roadrunner", "desert", "cuckoo", "fast", "southwest", "bird"])
def _(S):
    body = union(rot(ellipse(10, 10.5, 4.3, 2.2), -12, 10, 10.5), thick("M7.5 10L6 7.5", 2.4, S), circle(6, 7, 2),
                 tri(S, [(4.3, 6.4), (2.8, 7.6), (4.5, 7.9)], 0.3),
                 tri(S, [(7, 5.3), (10.5, 3.5), (9.5, 5), (11, 5.3), (7.8, 7)], 0.4),
                 tri(S, [(13, 9.3), (21.3, 7.3), (21.3, 9.3), (13.5, 11.8)], 0.6))
    return [shell(body, stroke_miterlimit="2.5"), dot(5.8, 6.7, 0.65), line(poly([(9, 12.8), (7, 16), (4.5, 16.5)], r=S.r)),
            line(poly([(11, 12.8), (12.5, 16.5), (11, 20)], r=S.r)), line(seg(15, 14.5, 20.5, 14.5)), line(seg(16.5, 18, 20.5, 18))]


@icon("cuckoo-bird", CAT, "Slim cuckoo perched with a long barred tail and a slightly curved bill",
      tags=["cuckoo", "common cuckoo", "spring", "cuckoo clock", "perched", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = union(rot(ellipse(9.5, 8.5, 4.8, 2.6), 30, 9.5, 8.5),
                 circle(5.5, 5.5, 2.2), tri(S, [(3.6, 5), (2.8, 6.8), (3.8, 6.4)], 0.2))
    tail = tri(S, [(12, 10), (20.5, 16), (19, 18.3), (11, 12.5)], 0.8)
    return [shell(union(body, tail)), dot(5.5, 5.1, 0.7), detail(seg(15.2, 13, 13.8, 15)), detail(seg(18, 15, 16.8, 17)),
            line(seg(3, 14, 12, 14))]


@icon("swift-bird", CAT, "Swift flying seen from below with long scythe-shaped wings and a notched tail",
      tags=["common swift", "flight", "fast", "summer", "aerial", "bird"])
def _(S):
    r = L(S, 0, 0.6)
    wl = "M11 10.5C8 9.5 5.5 10 2.8 13.5C6 12 8.5 12 11 13.3Z"
    body = union(ellipse(12, 11.8, 1.9, 3.2), circle(12, 8.5, 1.6), wl, flip(wl),
                 tri(S, [(10.8, 14), (13.2, 14), (14, 17.5), (12, 16.2), (10, 17.5)], 0.4))
    return [shell(body, stroke_miterlimit="2.5")]


@icon("umbrellabird", CAT, "Umbrellabird perched with an umbrella crest over its head and a long hanging wattle",
      tags=["amazonian umbrellabird", "cotinga", "crest", "rainforest", "wattle", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    crest = "M3 7.5C3 4.2 6 2.5 9 2.5C12 2.5 14 4.2 14 6.5L14 7.5Z"
    head = circle(9, 9, 2.5)
    body = ("M9 10.5C12 9.5 16 10.5 17.5 13.5" + tip((17.5, 13.5), (20.8, 19.5), (15.5, 17), r)
            + "L15.5 17C13 17.5 10.5 16.5 9.5 14.5Z")
    return [shell(union(crest, head, body)), dot(8, 9.3, 0.7), mark(tri(S, [(6.5, 9.8), (4.8, 10.5), (6.7, 11)], 0.2)),
            line("M8.3 12.5C7.8 15 7.8 17.5 8.3 20.5"), line(seg(11.5, 19.8, 20.8, 19.8))]


@icon("pheasant", CAT, "Pheasant walking with a very long pointed striped tail and a ring around its neck",
      tags=["ring-necked pheasant", "game bird", "countryside", "hunting", "long tail", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = union(rot(ellipse(9.5, 12.5, 4.5, 3), -10, 9.5, 12.5), thick("M6.5 11L5.8 7", 2.6, S), circle(5.8, 6.3, 2),
                 tri(S, [(4, 5.8), (2.8, 7.2), (4.2, 7.2)], 0.2),
                 tri(S, [(12.5, 10), (21.3, 5), (14, 13)], 0.6))
    return [shell(union(body), stroke_miterlimit="2.5"), dot(5.7, 5.9, 0.6), detail(seg(4.8, 9, 7.4, 9)),
            detail(seg(15.2, 8.8, 16, 10)), detail(seg(17.8, 7.3, 18.5, 8.3)),
            line(poly([(8.5, 15.3), (8, 18.5), (6.5, 21)], r=S.r)), line(poly([(11, 15.2), (12, 18), (11.5, 21)], r=S.r))]


@icon("quail", CAT, "Plump round quail with a single curled plume bobbing forward from its head",
      tags=["california quail", "game bird", "plume", "covey", "partridge", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = union(ellipse(13, 14, 7, 5.3), circle(8, 9.5, 3), tri(S, [(5.3, 9), (3.3, 10.3), (5.5, 11)], 0.3),
                 tri(S, [(19, 12), (21.3, 11.5), (20, 14.5)], 0.6))
    plume = rot(ellipse(5.5, 4.5, 1.4, 2), -30, 5.5, 4.5) if S.name == "rounded" else rot(poly([(5.5, 2.3), (6.9, 4.5), (5.5, 6.5), (4.1, 4.5)], closed=True), -30, 5.5, 4.5)
    return [shell(body), mark(plume), line("M8.5 6.5C8.3 5.5 7.8 5 7 5"), dot(7.6, 9.2, 0.75),
            detail("M11 15C13 16.5 16 16.5 18 14.5"), line(seg(11, 19, 11, 21.3)), line(seg(15, 19, 15, 21.3))]


@icon("turkey-bird", CAT, "Turkey from the front with its tail fanned into a half circle and a dangling wattle",
      tags=["thanksgiving", "gobble", "tom turkey", "farm", "autumn", "bird"])
def _(S):
    c = (12, 13)
    if S.name == "line":
        pts = []
        for i in range(13):
            a = 180 + i * 15
            pts.append(pt_on(c[0], c[1], 9.2 if i % 2 == 0 else 8, a))
        fan = poly(pts + [(20, 16), (4, 16)], closed=True)
    else:
        fan = union(minus(circle(12, 13, 8), rect(0, 13, 24, 11)), *[circle(*pt_on(12, 13, 7.8, 180 + i * 30), 1.5) for i in range(7)],
                    rect(4, 12.5, 16, 3.5))
    body = union(ellipse(12, 15.5, 3.8, 5), circle(12, 8.8, 2.1))
    return [shell(minus(fan, grow(body, 2))), shell(body), dot(11.3, 8.3, 0.6), dot(12.7, 8.3, 0.6),
            mark(union(tri(S, [(11.2, 9.5), (12.8, 9.5), (12, 10.7)], 0.2), ellipse(12.8, 11.8, 0.7, 1.2))),
            detail(arc(12, 13, 5.6, 200, 235)), detail(arc(12, 13, 5.6, 305, 340))]


@icon("guinea-fowl", CAT, "Guinea fowl with a round spotted body, small bare head and a bony helmet",
      tags=["guineafowl", "helmeted guinea fowl", "farm", "africa", "poultry", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = union(ellipse(13.5, 13.5, 7.5, 5.5), thick("M8 11L6.5 8", 2.4, S), circle(6.2, 7.2, 1.9),
                 tri(S, [(4.5, 6.8), (2.8, 8), (4.7, 8.3)], 0.3), tri(S, [(5.8, 5.6), (6.8, 3), (7.6, 5.6)], 0.4))
    spots = [dot(x, y, 0.85) for x, y in ((10.5, 12), (13.5, 11), (16.5, 12), (12, 15), (15, 14.8), (18, 15))]
    return [shell(body), dot(6.4, 6.9, 0.6), mark(ellipse(5.5, 9.5, 0.7, 1)), *spots, line(seg(11.5, 18.8, 11.5, 21.3)), line(seg(15.5, 18.8, 15.5, 21.3))]


@icon("silkie-chicken", CAT, "Fluffy silkie chicken with puffy feathers, a pompom crest and feathered feet",
      tags=["silkie", "fluffy chicken", "bantam", "pet chicken", "poultry", "bird"])
def _(S):
    k = L(S, 0, 0.3)
    body = union(ellipse(13, 12.5, 6.5, 5), circle(8.5, 9, 3 + k), circle(12, 7.8, 2.8 + k), circle(16.5, 8.5, 2.8 + k),
                 circle(19.5, 11.5, 2.3 + k), circle(18.5, 15.5, 2.5 + k), circle(9, 15, 2.8 + k))
    head = union(circle(6.5, 7.5, 2.2), circle(6.3, 4.5, 2 + k))
    beak = tri(S, [(4.5, 7.3), (2.8, 8.3), (4.6, 8.8)], 0.2)
    return [shell(union(body, head, beak)), dot(5.8, 7.4, 0.65), detail(arc(6.4, 7.6, 2.3, 280, 20)),
            shell(ellipse(11, 19.3, 1.8, 1.7)), shell(ellipse(15.5, 19.3, 1.8, 1.7))]


@icon("sage-grouse", CAT, "Displaying sage grouse with puffed chest air sacs and a spiky fanned tail",
      tags=["greater sage-grouse", "lek", "courtship", "prairie", "game bird", "bird"])
def _(S):
    c = (14, 12.5)
    spikes = []
    for i in range(9):
        a = 205 + i * 16.5
        spikes.append(pt_on(c[0], c[1], 7.8 if i % 2 == 0 else 5.5, a))
    fan = poly(spikes + [(19, 13)], closed=True, r=L(S, 0, 0.4))
    body = union(ellipse(11, 14.5, 6, 4.8), circle(5.8, 8.5, 1.9), tri(S, [(4.3, 8), (2.8, 9), (4.4, 9.4)], 0.2),
                 thick("M7 12L6 9", 2.6, S))
    return [shell(minus(fan, grow(body, 2)), stroke_miterlimit="2.5"), shell(body), dot(5.7, 8.2, 0.55),
            detail(ellipse(8.5, 14.8, 2.2, 2.2)),
            line(seg(10, 19.3, 10, 21.3)), line(seg(13.5, 19.3, 13.5, 21.3))]


@icon("brooding-hen", CAT, "Hen sitting low on a straw nest with egg tips peeking out from under her",
      tags=["nesting", "sitting hen", "eggs", "incubate", "farm", "poultry"])
def _(S):
    r = L(S, 0, 0.8)
    hen = union("M5 14C5 10 8 8 12 8.3C16 8.5 19 10.5 20 14Z", circle(7.5, 7, 2.6),
                tri(S, [(5.3, 6.3), (2.8, 7.3), (5.3, 8.2)], 0.3), tri(S, [(17.5, 10), (21, 6.5), (20.5, 12)], 0.8))
    nest = "M3 16L21 16C20.5 19.5 17.5 21.3 12 21.3C6.5 21.3 3.5 19.5 3 16Z"
    return [shell(hen), mark(union(circle(6.7, 4.2, 1.1), circle(8.5, 4.2, 1.1))), dot(7.8, 6.6, 0.7),
            detail("M10.5 11.5C12.5 12.5 15 12.5 17 11.5"), shell(nest), detail(seg(6.5, 18.8, 10, 18.3)), detail(seg(13.5, 18.3, 17.5, 18.8)),
            mark(ellipse(9.5, 14.8, 1.3, 0.9)), mark(ellipse(14, 14.8, 1.3, 0.9))]
