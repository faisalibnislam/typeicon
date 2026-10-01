"""TypeIcon Core: kids (batch kids_003).

Pool and playground equipment, party games, fairground rides, art and craft supplies, school day items and
baby care helpers, drawn from the objects themselves. Front or side views where possible; small parts sit
inside a clear silhouette so they survive at 16 px.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, LINE as LINE_S, P, ST, U, fmt, path_to_d, rotation, transform_path  # noqa: F401

CAT = "kids"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12.0, cy=12.0):
    """Rotate a closed outline clockwise on screen about (cx, cy)."""
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rot_pts(points, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in points]


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def cut_line(d, S, cutters, gap=1.5, w=2.0):
    """A stroke along d drawn as a solid mark with gaps around the cutter strokes (for things passing behind)."""
    reg = ST(d, w, S.cap, S.join)
    cut = U(*[ST(c, 2 + 2 * gap, "round", "round") for c in cutters])
    return Part("solid", path_to_d(D(reg, cut)))


def behind(back_d, fronts, gap=1.75):
    """Outline of the part of back_d not hidden by the front shapes, kept `gap` clear of their strokes."""
    cut = U(*[U(P(f), ST(f, 2 * (gap + 2), "round", "round")) for f in fronts])
    return path_to_d(D(P(back_d), cut))


def wave(x0, x1, y, amp, n):
    """Smooth wave line from x0 to x1 made of n half waves."""
    step = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        xa = x0 + i * step
        sgn = -1 if i % 2 == 0 else 1
        d += f"Q{fmt(xa + step / 2)} {fmt(y + sgn * amp * 2)} {fmt(xa + step)} {fmt(y)}"
    return d


def star(cx, cy, ro, ri, rnd=0.0):
    pts = []
    for i in range(10):
        ang = -90 + i * 36
        rad = ro if i % 2 == 0 else ri
        pts.append((cx + rad * math.cos(math.radians(ang)), cy + rad * math.sin(math.radians(ang))))
    return poly(pts, closed=True, r=rnd)


def pt_on(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def ring(cx, cy, ro, ri):
    return minus(circle(cx, cy, ro), circle(cx, cy, ri))


def band(cx, cy, ro, ri, a0, a1):
    """Annular sector from angle a0 to a1 (clockwise on screen, 0 = right)."""
    p0, p1 = pt_on(cx, cy, ro, a0), pt_on(cx, cy, ro, a1)
    q1, q0 = pt_on(cx, cy, ri, a1), pt_on(cx, cy, ri, a0)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return (f"M{fmt(p0[0])} {fmt(p0[1])}A{fmt(ro)} {fmt(ro)} 0 {large} 1 {fmt(p1[0])} {fmt(p1[1])}"
            f"L{fmt(q1[0])} {fmt(q1[1])}A{fmt(ri)} {fmt(ri)} 0 {large} 0 {fmt(q0[0])} {fmt(q0[1])}Z")


def head(x, y, r=2):
    return dot(x, y, r)


def limb(S, *pts):
    return line(poly(list(pts), r=S.r * 0.6))


# ============================================================================ pool and water play

@icon("kiddie-pool", CAT, "Inflatable paddling pool made of two stacked rings with water rippling above the rim",
      tags=["paddling pool", "kiddie pool", "wading pool", "inflatable pool", "summer", "backyard"])
def _(S):
    r = 2.75
    body = (f"M5 10H19A{r} {r} 0 0 1 19 15.5A{r} {r} 0 0 1 19 21H5A{r} {r} 0 0 1 5 15.5A{r} {r} 0 0 1 5 10Z")
    return [
        shell(body),
        detail(seg(5, 15.5, 19, 15.5)),
        line(wave(4.5, 19.5, 6, 0.75, 4)),
    ]


@icon("swim-ring", CAT, "Inflatable swim ring with stripes and a valve on top",
      tags=["swim ring", "rubber ring", "inflatable ring", "float", "pool toy", "swimming"])
def _(S):
    cx, cy, ro, ri = 12, 13, 8.5, 4
    parts = [shell(ring(cx, cy, ro, ri))]
    for a in (45, 135, 225, 315):
        a0, a1 = pt_on(cx, cy, ri, a), pt_on(cx, cy, ro, a)
        parts.append(detail(seg(a0[0], a0[1], a1[0], a1[1])))
    parts.append(shell(rect(10.5, 2, 3, 3, L(S, 0, 1))))
    return parts


@icon("pool-noodle", CAT, "Foam pool noodle bent into an arch with its hollow end facing out",
      tags=["pool noodle", "foam noodle", "float", "pool toy", "swimming", "water play"])
def _(S):
    endc = pt_on(11, 19, 7, 338)
    end = circle(endc[0], endc[1], 3.2)
    body = behind(band(11, 19, 9, 5, 180, 350), [end], gap=-0.5)
    return [
        shell(body),
        detail(arc(11, 19, 7, 200, 300)),
        shell(end),
        dot(endc[0], endc[1], 1.1),
    ]


@icon("splash-pad", CAT, "Ground level fountain jets spraying arcs of water upward from a flat pad",
      tags=["splash pad", "spray park", "water playground", "fountain jets", "summer", "sprinkler"])
def _(S):
    return [
        shell(rect(3, 19, 18, 2.5, rr(S, 1.25))),
        line(seg(12, 17, 12, 5)),
        line("M9.5 17C9.5 10 6 7.5 3.5 10.5"),
        line("M14.5 17C14.5 10 18 7.5 20.5 10.5"),
        dot(12, 2.5, 1.1), dot(3, 14, 1.1), dot(21, 14, 1.1),
    ]


@icon("water-table", CAT, "Play table on legs with a basin of water and a scoop resting below",
      tags=["water table", "sensory table", "water play", "sand and water table", "toddler", "outdoor play"])
def _(S):
    return [
        shell(poly([(2.5, 6), (21.5, 6), (19.5, 12.5), (4.5, 12.5)], closed=True, r=S.r)),
        detail(wave(7, 17, 9.25, 0.5, 4)),
        line(seg(6, 12.5, 4.5, 21.5)), line(seg(18, 12.5, 19.5, 21.5)),
        shell(rect(8.5, 16.5, 4.5, 4.5, rr(S, 1.25))),
        line(seg(13, 18.5, 15.5, 16)),
    ]


# ============================================================================ playground

@icon("playground-slide", CAT, "Playground slide with a ladder up one side and a curved chute down the other",
      tags=["slide", "playground slide", "park", "playground", "recess", "slippery slide"])
def _(S):
    parts = [
        line(seg(3.5, 21.5, 3.5, 4)), line(seg(8.5, 21.5, 8.5, 4)),
        line(poly([(8.5, 5), (10.5, 5), (13.5, 7)], r=S.r)),
        line("M13.5 7C16 10 17 14 18.5 17.5C19.3 19.3 20.5 20 22 20"),
        line(seg(15.5, 11, 15.5, 21.5)),
    ]
    for y in (9, 13, 17):
        parts.append(detail(seg(3.5, y, 8.5, y)))
    return parts


@icon("spiral-slide", CAT, "Tower with a slide coiling around it in a spiral down to the ground",
      tags=["spiral slide", "twisty slide", "helter skelter", "playground", "tube slide", "park"])
def _(S):
    curves = ["M3 5.5C7 10.5 15 11 21 8", "M3 11.5C7 16.5 15 17 21 14"]
    run = "M3 17.5C6 21 9 21.5 13 21.5H21.5"
    tower = union(rect(10, 5, 4, 16.5, 0), poly([(9, 5.5), (12, 1.5), (15, 5.5)], closed=True))
    cut = U(*[ST(c, 5, "round", "round") for c in curves + [run]])
    tower = path_to_d(D(P(tower), cut))
    return [shell(tower)] + [line(c) for c in curves] + [line(run)]


@icon("tire-swing", CAT, "Tire hanging flat from three ropes tied to a tree branch",
      tags=["tire swing", "tyre swing", "swing", "playground", "backyard", "tree swing"])
def _(S):
    tire = union(ellipse(12, 15.5, 8.5, 3.5), rect(3.5, 15.5, 17, 3), ellipse(12, 18.5, 8.5, 3.5))
    return [
        line(seg(2.5, 3, 21.5, 3)),
        line(seg(12, 3, 12, 6)),
        line(seg(12, 6, 4.5, 14.5)), line(seg(12, 6, 19.5, 14.5)), line(seg(12, 6, 12, 12)),
        shell(tire),
        detail(ellipse(12, 15.5, 4, 1.2)),
    ]


@icon("seesaw", CAT, "Seesaw plank balanced on a central pivot with a handle near each end",
      tags=["seesaw", "teeter totter", "teeter-totter", "playground", "balance", "park"])
def _(S):
    ang = -14
    plank = rot(rect(2, 11, 20, 2.5, rr(S, 1.25)), ang, 12, 12.25)
    (hl0, hl1), (hr0, hr1) = rot_pts([(5.5, 11), (5.5, 7.5)], ang, 12, 12.25), rot_pts([(18.5, 11), (18.5, 7.5)], ang, 12, 12.25)
    (tl0, tl1) = rot_pts([(4, 7.5), (7, 7.5)], ang, 12, 12.25)
    (tr0, tr1) = rot_pts([(17, 7.5), (20, 7.5)], ang, 12, 12.25)
    return [
        shell(plank),
        shell(poly([(12, 15), (16.5, 21.5), (7.5, 21.5)], closed=True, r=S.r)),
        line(seg(*hl0, *hl1)), line(seg(*tl0, *tl1)),
        line(seg(*hr0, *hr1)), line(seg(*tr0, *tr1)),
    ]


@icon("merry-go-round", CAT, "Round playground spinning platform with a centre post and hand rails, seen at an angle",
      tags=["merry go round", "roundabout", "spinner", "playground", "carousel", "park"])
def _(S):
    deck = union(ellipse(12, 15, 9.5, 3.5), rect(2.5, 15, 19, 2.5), ellipse(12, 17.5, 9.5, 3.5))
    return [
        shell(deck),
        detail("M2.5 15A9.5 3.5 0 0 0 21.5 15"),
        line(seg(12, 3, 12, 13.5)),
        line(poly([(5.5, 13), (5.5, 8.5), (12, 5.5)], r=S.r)),
        line(poly([(18.5, 13), (18.5, 8.5), (12, 5.5)], r=S.r)),
    ]


@icon("monkey-bars", CAT, "Overhead horizontal ladder held up by two upright frames",
      tags=["monkey bars", "overhead ladder", "horizontal ladder", "playground", "climbing", "park"])
def _(S):
    parts = [
        line(seg(3.5, 21.5, 3.5, 4)), line(seg(20.5, 21.5, 20.5, 4)),
        shell(rect(3.5, 4, 17, 5, 0)),
    ]
    for x in (7.75, 12, 16.25):
        parts.append(detail(seg(x, 4, x, 9)))
    return parts


@icon("jungle-gym", CAT, "Cube shaped climbing frame of bars with a platform floor inside",
      tags=["jungle gym", "climbing frame", "climber", "playground", "play structure", "park"])
def _(S):
    return [
        line(poly([(3, 21.5), (3, 9), (15, 9), (15, 21.5)], r=0)),
        line(poly([(3, 9), (9, 3), (21, 3), (21, 15.5)], r=S.r)),
        line(seg(15, 9, 21, 3)),
        line(seg(9, 9, 9, 21.5)),
        line(seg(3, 15, 15, 15)), line(seg(15, 15, 21, 9)),
        line(seg(18, 6, 18, 18.5)),
    ]


@icon("climbing-dome", CAT, "Dome shaped climbing frame of bars joined into triangles",
      tags=["climbing dome", "geodome", "dome climber", "playground", "climbing frame", "geodesic dome"])
def _(S):
    cx, by = 12, 20.5
    rx, ry = 9.5, 12
    parts = [line(f"M{fmt(cx - rx)} {by}A{rx} {ry} 0 0 1 {fmt(cx + rx)} {by}"), line(seg(1.5, 21.5, 22.5, 21.5))]
    return parts + [
        line("M4.5 13.5C9 11.8 15 11.8 19.5 13.5"),
        line(poly([(2.5, 21), (7, 12.4), (12, 21), (17, 12.4), (21.5, 21)], r=S.r * 0.5)),
        line(poly([(7, 12.4), (12, 8.5), (17, 12.4)], r=S.r * 0.5)),
        line(seg(12, 8.5, 12, 12.2)),
    ]


@icon("climbing-net", CAT, "Pyramid shaped rope net stretched from a central pole",
      tags=["climbing net", "rope pyramid", "spider net", "playground", "rope climber", "park"])
def _(S):
    return [
        line(seg(12, 2, 12, 21.5)),
        line(poly([(3, 21.5), (12, 3.5), (21, 21.5)], r=S.r * 0.5)),
        line(seg(3, 21.5, 21, 21.5)),
        line(seg(8, 11.5, 16, 11.5)), line(seg(5.5, 16.5, 18.5, 16.5)),
        line(seg(12, 3.5, 7.5, 21.5)), line(seg(12, 3.5, 16.5, 21.5)),
    ]


@icon("spring-rider", CAT, "Rocking animal seat mounted on a big coiled spring set in the ground",
      tags=["spring rider", "spring rocker", "rocking horse", "playground", "bouncer", "park"])
def _(S):
    body = union(rect(4, 7, 12, 4.5, rr(S, 2.25) if S.name == "rounded" else 1),
                 path_to_d(ST(seg(14.5, 8, 17.5, 4.5), 3.5, S.cap, S.join)),
                 ellipse(18.5, 4.5, 2.8, 2))
    return [
        shell(body),
        dot(18.5, 4.2, 0.9),
        line(poly([(12, 11.5), (8, 13), (16, 14.8), (8, 16.6), (16, 18.4), (12, 19.9)], r=S.r * 0.6)),
        line(seg(12, 19.9, 12, 21.5)),
        line(seg(5, 21.5, 19, 21.5)),
    ]


@icon("sandbox", CAT, "Wooden sandbox with a mound of sand and a small shovel stuck in it",
      tags=["sandbox", "sandpit", "sand pit", "playground", "digging", "backyard"])
def _(S):
    return [
        shell(rect(2.5, 13.5, 19, 8, rr(S, 2))),
        detail(seg(2.5, 17.5, 21.5, 17.5)),
        line("M3.5 13.5C5.5 8.5 10 8.5 12 13.5"),
        line(seg(16.5, 10.5, 20, 3)),
        shell(rot(poly([(14, 8), (18, 8), (18, 11), (16, 13), (14, 11)], closed=True, r=L(S, 0, 0.8)), 25, 16, 10.5)),
    ]


@icon("sand-bucket", CAT, "Beach pail with a handle and a small spade leaning against it",
      tags=["sand bucket", "beach pail", "pail and spade", "bucket and spade", "beach", "sandcastle"])
def _(S):
    return [
        shell(poly([(2.5, 9), (15.5, 9), (14, 21.5), (4, 21.5)], closed=True, r=S.r)),
        detail(seg(3.2, 12.5, 14.8, 12.5)),
        line("M3.5 9C3.5 2.5 14.5 2.5 14.5 9"),
        line(seg(19.5, 3, 19.5, 14)),
        shell(poly([(17.5, 14), (21.5, 14), (21.5, 19), (19.5, 21.5), (17.5, 19)], closed=True, r=L(S, 0, 0.8))),
    ]


@icon("sandcastle", CAT, "Sandcastle of bucket shaped towers with battlements and a flag on top",
      tags=["sandcastle", "sand castle", "beach", "summer", "building sand", "seaside"])
def _(S):
    merl = [(7, 6), (9, 6), (9, 8), (11, 8), (11, 6), (13, 6), (13, 8), (15, 8), (15, 6), (17, 6), (17.8, 15), (6.2, 15)]
    castle = union(poly(merl, closed=True, r=L(S, 0, 0.4)),
                   poly([(3, 11), (7.5, 11), (8, 17), (2.5, 17)], closed=True, r=L(S, 0, 0.4)),
                   poly([(16.5, 11), (21, 11), (21.5, 17), (16, 17)], closed=True, r=L(S, 0, 0.4)),
                   rect(1.5, 16, 21, 5.5, rr(S, 2)))
    return [
        shell(castle),
        detail("M10.5 21.5V19A1.5 1.5 0 0 1 13.5 19V21.5"),
        detail(seg(8, 11.5, 16, 11.5)),
        line(seg(12, 6, 12, 1.5)),
        solid(poly([(12, 1.5), (15.5, 2.75), (12, 4)], closed=True)),
    ]


@icon("sand-digger", CAT, "Ride-on digger seat on a post with a scoop arm reaching into the sand",
      tags=["sand digger", "sandbox digger", "ride on excavator", "playground digger", "sandpit", "digging toy"])
def _(S):
    return [
        shell(poly([(2.5, 5), (5, 5), (5, 9), (10, 9), (10, 11.5), (2.5, 11.5)], closed=True, r=L(S, 0, 0.8))),
        line(seg(6.5, 11.5, 6.5, 21.5)),
        line(seg(3, 21.5, 10, 21.5)),
        line(poly([(10, 10), (15, 5), (18.5, 10)], r=S.r)),
        shell(poly([(16, 11), (21, 11), (21, 13), (19, 16), (16, 16)], closed=True, r=L(S, 0, 0.8))),
        line("M13 21.5C15 18.5 20 18.5 22 21.5"),
    ]


@icon("kids-playhouse", CAT, "Small play house with a door and window and a slide coming off the side",
      tags=["playhouse", "wendy house", "play house", "cubby house", "backyard", "garden"])
def _(S):
    return [
        shell(poly([(2.5, 10.5), (8.75, 3.5), (15, 10.5), (15, 21.5), (2.5, 21.5)], closed=True, r=S.r)),
        detail(rect(5, 15, 3.5, 6.5, 0)),
        detail(rect(10, 13, 2.5, 2.5, 0)),
        line("M15 12C18 12 18.5 17 20 19.5C20.7 20.8 21.3 21.5 22 21.5"),
    ]


@icon("treehouse", CAT, "Small hut in the branches of a tree with a ladder leading up to it",
      tags=["treehouse", "tree house", "den", "fort", "backyard", "adventure"])
def _(S):
    return [
        shell(poly([(8.5, 8), (15, 2.5), (21.5, 8), (20.5, 8), (20.5, 13.5), (9.5, 13.5), (9.5, 8)], closed=True, r=S.r)),
        detail(rect(13.5, 9.5, 3, 4, 0)),
        shell(poly([(13, 13.5), (17, 13.5), (17.5, 19.5), (19.5, 21.5), (10.5, 21.5), (12.5, 19.5)], closed=True, r=L(S, 0, 0.6))),
        line(seg(3, 21.5, 6.5, 13.5)), line(seg(6.5, 21.5, 9.5, 14.5)),
        line(seg(4, 19, 7.5, 19)), line(seg(5.2, 16, 8.8, 16)),
    ]


@icon("rope-ladder", CAT, "Ladder of two ropes with wooden rungs hanging from a bar",
      tags=["rope ladder", "climbing ladder", "playground", "treehouse ladder", "climbing", "escape ladder"])
def _(S):
    parts = [line(seg(2.5, 2.5, 21.5, 2.5))]
    ys = [7, 12.5, 18]
    for x in (7.5, 16.5):
        prev = 2.5
        for y in ys:
            parts.append(line(seg(x, prev, x, y)))
            prev = y + 2
        parts.append(line(seg(x, prev, x, 22)))
    for y in ys:
        parts.append(shell(rect(5, y, 14, 2, rr(S, 1))))
    return parts


@icon("wobble-bridge", CAT, "Plank bridge sagging between two posts with chain hand rails",
      tags=["wobble bridge", "rope bridge", "suspension bridge", "playground", "swinging bridge", "chain bridge"])
def _(S):
    def yq(x, top, sag):
        t = (x - 3) / 18
        return top + sag * 4 * t * (1 - t)
    parts = [line(seg(3, 4, 3, 21.5)), line(seg(21, 4, 21, 21.5))]
    parts.append(line(f"M3 6Q12 {6 + 2 * 4} 21 6"))
    for x in (7.5, 12, 16.5):
        parts.append(line(seg(x, yq(x, 6, 4) + 1, x, yq(x, 14, 3) - 1.2)))
    for x in (5.6, 8.8, 12, 15.2, 18.4):
        y = yq(x, 14.5, 3)
        parts.append(mark(rect(x - 1.1, y, 2.2, 3.5, L(S, 0, 0.6))))
    return parts


@icon("crawl-tunnel", CAT, "Fabric play tunnel with hoop ribs, its open end facing out",
      tags=["play tunnel", "crawl tunnel", "pop up tunnel", "toddler", "agility tunnel", "soft play"])
def _(S):
    far = ellipse(19.5, 13, 2.5, 7) if S.name == "rounded" else rect(15, 6, 7, 14, 2)
    body = union(ellipse(5, 13, 3, 7), rect(5, 6, 14.5, 14), far)
    return [
        shell(body),
        detail(ellipse(5, 13, 1.25, 4.25)),
        detail("M10.5 6A2.5 7 0 0 1 10.5 20"),
        detail("M15 6A2.5 7 0 0 1 15 20"),
    ]


@icon("bouncy-castle", CAT, "Inflatable bouncy castle with rounded turrets, an arched opening and a soft floor",
      tags=["bouncy castle", "bounce house", "moonwalk", "inflatable castle", "party", "jumping castle"])
def _(S):
    body = union(rect(1.5, 15, 21, 6.5, rr(S, 3)),
                 rect(6, 8, 12, 8, 0),
                 rect(2.5, 5, 4.5, 11, 2.25), rect(17, 5, 4.5, 11, 2.25),
                 circle(9.5, 8, 1.75), circle(14.5, 8, 1.75))
    return [
        shell(body),
        detail("M9.5 15.5V13A2.5 2.5 0 0 1 14.5 13V15.5"),
        detail(seg(3, 17.75, 21, 17.75)),
    ]


@icon("trampoline", CAT, "Round trampoline on legs with a child doing a star jump above it",
      tags=["trampoline", "bouncing", "jump", "backyard", "gymnastics", "rebounder"])
def _(S):
    return [
        head(12, 3.8, 1.9),
        line(poly([(8, 6.5), (12, 8), (16, 6.5)], r=S.r * 0.5)),
        line(seg(12, 7, 12, 10)),
        line(poly([(9, 13), (12, 10), (15, 13)], r=S.r * 0.5)),
        shell(ellipse(12, 17, 9.5, 2)),
        line(seg(4.5, 18.5, 4.5, 21.5)), line(seg(19.5, 18.5, 19.5, 21.5)), line(seg(12, 19, 12, 21.5)),
    ]


@icon("teacup-ride", CAT, "Oversized fairground teacup with a spinning wheel in the middle and motion arcs",
      tags=["teacup ride", "spinning teacups", "fairground", "funfair", "amusement park", "carnival ride"])
def _(S):
    cup = "M5 11H19C19 16.5 16.5 20.5 12 20.5C7.5 20.5 5 16.5 5 11Z"
    return [
        shell(cup),
        line("M19 12.5A2.5 2.5 0 0 1 19 17.5H18"),
        line(seg(12, 8, 12, 11)),
        shell(ellipse(12, 5.5, 4, 1.75)),
        line(arc(12, 14, 10, 150, 205)),
        line(seg(9, 22, 15, 22)),
    ]


@icon("bumper-car", CAT, "Round bumper car with a rubber bumper ring and a pole reaching up to the ceiling grid",
      tags=["bumper car", "dodgem", "dodgems", "fairground", "funfair", "amusement park"])
def _(S):
    body = union(rect(2, 15, 20, 6.5, 3.25), rect(4, 9.5, 5, 6, 0), rect(4, 12.5, 15, 3, 0))
    return [
        shell(body),
        detail(seg(2, 18.25, 22, 18.25)),
        line(seg(6.5, 9.5, 6.5, 4)),
        line(seg(2.5, 4, 13.5, 4)),
        line(seg(14.5, 12.5, 16, 9.5)),
        line(seg(13.5, 9, 18.5, 9)),
    ]


@icon("carousel-horse", CAT, "Carousel horse mounted on a vertical pole with a saddle on its back",
      tags=["carousel horse", "merry go round horse", "carousel", "fairground", "funfair", "galloper"])
def _(S):
    w = 3
    body = union(rect(4.5, 10, 11, 5, 2.5),
                 path_to_d(ST(seg(14, 11.5, 17, 6.5), 3.5, "round", "round")),
                 rot(ellipse(19, 6.5, 2.8, 1.7), 30, 19, 6.5),
                 path_to_d(ST(poly([(14.5, 14), (17, 16), (15.5, 18.5)]), 2.2, "round", "round")),
                 path_to_d(ST(seg(6.5, 14, 5, 19.5), 2.2, "round", "round")),
                 path_to_d(ST("M5 11C3 11.5 2.5 13 2.5 15", 1.8, "round", "round")))
    return [
        shell(body),
        line(seg(10, 2, 10, 10)), line(seg(10, 15, 10, 22)),
        detail("M8 10.5C8 12.5 12 12.5 12 10.5"),
    ]


# ============================================================================ fairground and party games

@icon("claw-machine", CAT, "Arcade claw machine with a glass case, a claw hanging over the prizes and a joystick",
      tags=["claw machine", "crane game", "claw crane", "arcade", "prize machine", "grabber"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 2))),
        detail(rect(7, 5.5, 10, 11, L(S, 0, 1))),
        detail(seg(12, 5.5, 12, 8)),
        detail(poly([(9.5, 11.5), (9.5, 9.5), (12, 8), (14.5, 9.5), (14.5, 11.5)], r=S.r * 0.5)),
        dot(9.75, 14.25, 1.1), dot(14.25, 14.25, 1.1),
        detail(seg(8, 19, 11, 19)),
        dot(15.5, 19, 1.1),
    ]


@icon("ring-toss", CAT, "Upright peg with rings stacked on it and another ring flying toward it",
      tags=["ring toss", "hoopla", "quoits", "carnival game", "party game", "fair game"])
def _(S):
    return [
        line(seg(15, 6.5, 15, 12.5)),
        dot(15, 5.5, 1.5),
        line(ellipse(15, 14.25, 5.5, 1.3)),
        line(ellipse(15, 18.5, 5.5, 1.3)),
        line(seg(8, 21.75, 22, 21.75)),
        line(rot(ellipse(6, 7, 3.75, 1.3), -30, 6, 7)),
        line(seg(3, 13.5, 5, 12.5)),
        line(seg(2.5, 17, 6, 15.25)),
    ]


@icon("whack-a-mole", CAT, "Game board with a mole popping out of a hole and a mallet raised above it",
      tags=["whack a mole", "mole game", "arcade game", "carnival game", "mallet", "reaction game"])
def _(S):
    mallet = rot(rect(14, 2.5, 7.5, 4, rr(S, 1.5)), 25, 17.75, 4.5)
    return [
        shell(rect(2, 15.5, 20, 6, rr(S, 2))),
        shell("M5 15.5V13A4 4 0 0 1 13 13V15.5Z"),
        dot(7.6, 12.5, 0.9), dot(10.4, 12.5, 0.9),
        shell(mallet),
        line(seg(18.5, 8, 21, 12)),
    ]


@icon("pin-the-tail", CAT, "Donkey outline with its tail held apart on a pin, ready to be pinned on blindfolded",
      tags=["pin the tail on the donkey", "party game", "donkey", "blindfold game", "birthday game", "kids party"])
def _(S):
    body = union(rect(8, 9, 10, 6, rr(S, 3) if S.name == "rounded" else 2),
                 path_to_d(ST(seg(16, 10.5, 18.5, 6), 3.5, "round", "round")),
                 rot(ellipse(19.5, 6.5, 2.8, 1.8), 35, 19.5, 6.5),
                 path_to_d(ST(seg(17.5, 5, 16.5, 2), 1.8, "round", "round")),
                 path_to_d(ST(seg(10, 14, 9.5, 21), 2.2, "round", "round")),
                 path_to_d(ST(seg(16, 14, 16.5, 21), 2.2, "round", "round")))
    tuft = "M4.5 13C6 14.5 6 16.5 4.5 18.5C3 16.5 3 14.5 4.5 13Z"
    return [
        shell(body),
        dot(3.5, 3.5, 1.6),
        line("M3.5 5.5C3.5 8 4.5 9.5 4.5 12"),
        shell(tuft),
    ]


@icon("musical-chairs", CAT, "Two chairs set back to back with a music note playing above them",
      tags=["musical chairs", "party game", "birthday game", "music game", "chairs", "kids party"])
def _(S):
    parts = []
    for sx in (1, -1):
        X = (lambda x: x) if sx == 1 else (lambda x: 24 - x)
        parts += [
            line(poly([(X(9.5), 10.5), (X(9.5), 21.5)], r=0)),
            line(poly([(X(9.5), 15.5), (X(3.5), 15.5), (X(3.5), 21.5)], r=S.r)),
        ]
    parts += [
        shell(ellipse(10.5, 7, 2, 1.5)),
        line(poly([(12.5, 7), (12.5, 2), (15.5, 3.5)], r=S.r * 0.4)),
    ]
    return parts


@icon("apple-bobbing", CAT, "Tub of water with apples floating on the surface",
      tags=["apple bobbing", "bobbing for apples", "halloween game", "party game", "autumn", "fall festival"])
def _(S):
    def apple(cx, cy, r):
        return (f"M{fmt(cx)} {fmt(cy - r * 0.7)}C{fmt(cx + r * 0.6)} {fmt(cy - r * 1.15)} {fmt(cx + r * 1.1)} {fmt(cy - r * 0.8)} "
                f"{fmt(cx + r)} {fmt(cy)}C{fmt(cx + r * 0.95)} {fmt(cy + r * 0.9)} {fmt(cx + r * 0.4)} {fmt(cy + r)} {fmt(cx)} {fmt(cy + r * 0.85)}"
                f"C{fmt(cx - r * 0.4)} {fmt(cy + r)} {fmt(cx - r * 0.95)} {fmt(cy + r * 0.9)} {fmt(cx - r)} {fmt(cy)}"
                f"C{fmt(cx - r * 1.1)} {fmt(cy - r * 0.8)} {fmt(cx - r * 0.6)} {fmt(cy - r * 1.15)} {fmt(cx)} {fmt(cy - r * 0.7)}Z")
    a1, a2 = apple(8, 9.5, 3.4), apple(16.5, 10, 3.4)
    tub = behind(poly([(2.5, 12), (21.5, 12), (19.5, 21.5), (4.5, 21.5)], closed=True), [a1, a2], gap=0.25)
    return [
        shell(tub),
        detail(seg(4, 16, 20, 16)),
        shell(a1), shell(a2),
        line(seg(8, 6.5, 8.8, 3.5)), line(seg(16.5, 7, 17.3, 4)),
    ]


@icon("limbo", CAT, "Limbo bar on two posts with a person bending backwards to pass under it",
      tags=["limbo", "limbo dance", "limbo bar", "party game", "how low can you go", "beach party"])
def _(S):
    return [
        line(seg(3, 21.5, 3, 7)), line(seg(21, 21.5, 21, 7)),
        line(seg(3, 10.5, 21, 10.5)),
        head(6.5, 15.5, 1.9),
        limb(S, (9, 16.2), (13, 17.8), (16.5, 16), (16.5, 21.5)),
        limb(S, (13, 17.8), (13, 21.5)),
        limb(S, (10, 16.6), (8.5, 21)),
    ]


@icon("mini-golf", CAT, "Putting green with a little windmill obstacle, a golf ball and a flagged hole",
      tags=["mini golf", "crazy golf", "putt putt", "miniature golf", "windmill", "putting"])
def _(S):
    return [
        shell(poly([(4, 21.5), (5.5, 11.5), (9.5, 11.5), (11, 21.5)], closed=True, r=L(S, 0, 0.8))),
        detail("M6.5 21.5V19.5A1 1 0 0 1 8.5 19.5V21.5"),
        line(seg(4, 5, 11, 12)), line(seg(11, 5, 4, 12)),
        line(seg(2, 21.5, 22, 21.5)),
        dot(15, 19, 1.5),
        line(seg(20.5, 21.5, 20.5, 5)),
        solid(poly([(20.5, 5), (16, 7), (20.5, 9)], closed=True)),
    ]


@icon("ice-pop", CAT, "Frozen ice pop on a flat wooden stick with a bite taken out of the top",
      tags=["ice pop", "ice lolly", "ice block", "frozen treat", "summer", "freezer pop"])
def _(S):
    pop = minus(rect(6.5, 2.5, 11, 14, 5.5 if S.name == "rounded" else 3), circle(17.5, 3, 3))
    return [
        shell(pop),
        detail(seg(9.5, 7, 9.5, 12.5)),
        shell(rect(10.5, 16.5, 3, 5.5, L(S, 0, 1.5))),
    ]


@icon("face-paint", CAT, "Child's face with a painted star on the cheek and a paint brush beside it",
      tags=["face paint", "face painting", "party", "carnival", "fete", "kids party"])
def _(S):
    return [
        shell(circle(10.5, 12.5, 8.5)),
        dot(7.5, 10.5, 1.1), dot(12.5, 10.5, 1.1),
        detail("M7.5 15.5Q9.5 17.5 11.5 15.5"),
        mark(star(14.5, 15, 2.6, 1.2, L(S, 0, 0.3))),
        line(seg(22, 2, 18.5, 5.5)),
        shell(rot(rect(16, 5, 3, 4.5, L(S, 0, 1)), 45, 17.5, 7.25)),
    ]


def _cap(x1, y1, x2, y2, w=3.5):
    return path_to_d(ST(seg(x1, y1, x2, y2), w, "round", "round"))


@icon("balloon-animal", CAT, "Twisted balloon dog made of linked sausage shaped segments",
      tags=["balloon animal", "balloon dog", "balloon twisting", "party entertainer", "clown", "kids party"])
def _(S):
    segs = [
        (3, 7.5, 6.5, 7.5),     # snout
        (8.5, 4.5, 9, 2.5),     # ear
        (9, 10, 9, 13),         # neck
        (11, 14, 16.5, 14),     # body
        (9.5, 17, 8.5, 21),     # front leg
        (18.5, 17, 19.5, 21),   # back leg
        (18.5, 11.5, 20.5, 8),  # tail
    ]
    parts = []
    for x1, y1, x2, y2 in segs:
        if S.name == "line":
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            half = math.hypot(x2 - x1, y2 - y1) / 2 + 1.3
            ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
            parts.append(shell(rot(ellipse(cx, cy, half, 1.3), ang, cx, cy)))
        else:
            parts.append(shell(_cap(x1, y1, x2, y2, w=2.6)))
    parts.append(shell(circle(8.5, 7.5, 1.6)))
    return parts

@icon("pinata", CAT, "Animal shaped paper pinata with a fringe band, hanging from a string",
      tags=["pinata", "piñata", "party", "birthday", "fiesta", "candy"])
def _(S):
    rk = L(S, 0, 1)
    body = union(rect(3.5, 11, 12, 6, 0), rect(12, 6, 4, 6, 0), rect(12, 5, 8, 4, 0),
                 rect(4.5, 16, 3, 5.5, 0), rect(11.5, 16, 3, 5.5, 0), rect(12.5, 2.5, 2, 3, 0))
    body = path_to_d(transform_path(P(body), (1, 0, 0, 1, 0, 0)))
    return [
        shell(poly([(3.5, 11), (12, 11), (12, 5), (12.5, 5), (12.5, 2.5), (14.5, 2.5), (14.5, 5), (20, 5), (20, 9),
                    (16, 9), (16, 17), (14.5, 17), (14.5, 21.5), (11.5, 21.5), (11.5, 17), (7.5, 17), (7.5, 21.5),
                    (4.5, 21.5), (4.5, 17), (3.5, 17)], closed=True, r=rk * 0.6)),
        detail(seg(3.5, 14, 16, 14)),
        line(seg(18, 5, 18, 1.5)),
    ]


@icon("goodie-bag", CAT, "Small party bag tied with a ribbon with a lollipop peeking out of the top",
      tags=["goodie bag", "party bag", "loot bag", "favor bag", "favour bag", "treat bag"])
def _(S):
    bag = "M7 11.5H17L19.5 19Q20 21.5 17.5 21.5H6.5Q4 21.5 4.5 19Z"
    return [
        shell(bag),
        line(poly([(8, 11.5), (7, 8), (10, 9.5), (12, 7.5), (14, 9.5)], r=S.r * 0.3)),
        detail(seg(7.5, 14, 16.5, 14)),
        line(seg(14.5, 9.5, 16.5, 6.5)),
        shell(circle(18, 4.5, 2.5)),
    ]


@icon("party-horn", CAT, "Party blower with a mouthpiece and a paper tube unrolling into a curl",
      tags=["party horn", "party blower", "noisemaker", "blowout", "birthday", "new year"])
def _(S):
    c = (5, 15)
    return [
        shell(rot(rect(2.5, 13.25, 4.5, 3.5, L(S, 0, 1.25)), -32, *c)),
        shell(rot(poly([(7, 13.5), (15, 13.25), (15, 16.75), (7, 16.5)], closed=True, r=L(S, 0, 0.6)), -32, *c)),
        line("M14.2 9.9C16.5 6.5 21 6.5 21 10.5C21 13 18.5 14 17.2 12.6C16.3 11.6 17.1 10.3 18.4 10.6"),
    ]


@icon("kazoo", CAT, "Small tapered kazoo tube with a round buzzer cap on top and sound coming out",
      tags=["kazoo", "toy instrument", "humming", "party", "music toy", "buzzer"])
def _(S):
    return [
        shell(poly([(2.5, 11.5), (16.5, 13), (16.5, 17.5), (2.5, 19)], closed=True, r=S.r)),
        shell("M7 12V9.5A3 1.5 0 0 1 13 9.5V12.5Z"),
        line(arc(16.5, 15.25, 3.5, -45, 45)),
        line(arc(16.5, 15.25, 6.5, -35, 35)),
    ]


# ============================================================================ art, craft and school


@icon("slide-whistle", CAT, "Tube whistle with its sliding plunger rod pulled out of the end",
      tags=["slide whistle", "swanee whistle", "toy whistle", "sound effect", "music toy", "whistle"])
def _(S):
    return [
        shell(rect(2.5, 9.5, 12, 5, rr(S, 1.5))),
        detail(poly([(5.5, 9.5), (5.5, 12), (8, 12)], r=0)),
        line(seg(14.5, 12, 19.5, 12)),
        shell(rect(19.5, 9, 2.5, 6, L(S, 0, 1.25))),
    ]


@icon("kids-drawing", CAT, "Child's drawing of a house and a sun on a sheet held up by a magnet",
      tags=["kids drawing", "child art", "fridge art", "artwork", "picture", "magnet"])
def _(S):
    return [
        shell(rot(rect(3, 4.5, 18, 17, rr(S, 2)), -5)),
        shell(circle(12, 4, 2.25) if S.name == "rounded" else rect(9.75, 1.75, 4.5, 4.5, 0.5)),
        dot(7.5, 10, 1.75),
        detail(poly([(12, 18.5), (12, 14), (15, 11), (18, 14), (18, 18.5)], closed=True, r=L(S, 0, 0.5))),
        detail(seg(5, 18.8, 10, 18.4)),
    ]


@icon("pencil-case", CAT, "Zipped soft pencil case with a pencil sticking out of the half open zip",
      tags=["pencil case", "pencil pouch", "school supplies", "stationery", "back to school", "zip pouch"])
def _(S):
    pouch = rect(2.5, 11, 19, 10.5, rr(S, 3))
    pencil = rot(poly([(13, 14), (13, 5), (15, 1.5), (17, 5), (17, 14)], closed=True, r=L(S, 0, 0.5)), 20, 15, 12)
    return [
        shell(behind(pencil, [pouch], gap=0.25)),
        shell(pouch),
        detail(seg(5, 14.5, 10.5, 14.5)),
        detail(seg(8, 14.5, 8, 17.5)),
    ]


@icon("glue-stick", CAT, "Twist-up glue stick with the glue pushed up out of the tube and a label band",
      tags=["glue stick", "glue", "craft", "school supplies", "stationery", "paste"])
def _(S):
    top = ("M8.5 10V6.5Q12 3 15.5 5V10Z" if S.name == "rounded" else "M8.5 10V6.5L15.5 4V10Z")
    return [
        shell(rect(6.5, 10, 11, 9.5, rr(S, 1.5))),
        detail(wave(8.5, 15.5, 14.75, 0.6, 3)),
        shell(rect(7.5, 19.5, 9, 2.5, L(S, 0, 1))),
        shell(top),
    ]


@icon("colored-pencils", CAT, "Three coloured pencils standing in a cup with their tips at different heights",
      tags=["colored pencils", "coloured pencils", "pencil cup", "drawing", "art supplies", "crayons"])
def _(S):
    cup = poly([(4.5, 13), (19.5, 13), (18, 21.5), (6, 21.5)], closed=True, r=S.r)

    def pencil(cx, top, ang):
        pts = [(cx - 1.75, 14), (cx - 1.75, top + 3), (cx, top), (cx + 1.75, top + 3), (cx + 1.75, 14)]
        return rot(poly(pts, closed=True, r=L(S, 0, 0.4)), ang, cx, 16)
    pens = [pencil(12, 2.5, 0), pencil(7.5, 5.5, -18), pencil(16.5, 7, 18)]
    return [shell(behind(p, [cup], gap=0.25)) for p in pens] + [shell(cup)]


@icon("crayon-box", CAT, "Open box of crayons with their pointed tips standing up above the front",
      tags=["crayon box", "crayons", "coloring", "colouring", "art supplies", "drawing"])
def _(S):
    parts = [shell(poly([(3.5, 11), (9, 11), (12, 13.5), (15, 11), (20.5, 11), (20.5, 21.5), (3.5, 21.5)], closed=True, r=S.r)),
             detail(seg(3.5, 17.5, 20.5, 17.5))]
    for cx, top in ((7, 4.5), (12, 2.5), (17, 5)):
        bot = 9 if cx != 12 else 11.5
        parts.append(solid(poly([(cx - 1.6, bot), (cx - 1.6, top + 3), (cx - 0.6, top), (cx + 0.6, top), (cx + 1.6, top + 3), (cx + 1.6, bot)],
                                closed=True, r=L(S, 0, 0.4))))
    return parts


@icon("paint-pots", CAT, "Set of three round paint pots in a tray with a paintbrush lying above",
      tags=["paint pots", "poster paint", "paint set", "art class", "painting", "kids paint"])
def _(S):
    return [
        shell(rect(1.5, 12, 21, 9, rr(S, 4.5))),
        dot(6.5, 16.5, 2), dot(12, 16.5, 2), dot(17.5, 16.5, 2),
        line(seg(3, 9, 12, 5.5)),
        shell(rot(poly([(12, 5.5), (16, 3.5), (20, 5.5), (16, 7.5)], closed=True, r=L(S, 0, 0.8)), -21, 12, 5.5)),
    ]


@icon("coloring-book", CAT, "Open colouring book with a flower outline on one page and a crayon on the other",
      tags=["coloring book", "colouring book", "activity book", "crayon", "kids activity", "drawing"])
def _(S):
    pts = [(12, 6), (8, 4.5), (2.5, 4.5), (2.5, 18.5), (8, 18.5), (12, 20.5), (16, 18.5), (21.5, 18.5), (21.5, 4.5), (16, 4.5)]
    crayon = rot(poly([(6, 17), (6, 10.5), (7, 8.5), (8, 10.5), (8, 17)], closed=True, r=L(S, 0, 0.3)), 25, 7, 12.5)
    tulip = poly([(15, 7.5), (16, 9), (17, 7.5), (18, 9), (19, 7.5), (19, 10), (17, 12), (15, 10)], closed=True, r=L(S, 0, 0.3))
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(12, 6, 12, 20.5)),
        detail(tulip),
        detail(seg(17, 12, 17, 16)),
        mark(crayon),
    ]


@icon("sticker-chart", CAT, "Reward chart grid with star stickers filling some of the boxes",
      tags=["sticker chart", "reward chart", "star chart", "chore chart", "behaviour chart", "potty chart"])
def _(S):
    parts = [shell(rect(2.5, 2.5, 19, 19, S.R))]
    for v in (8.83, 15.17):
        parts.append(detail(seg(v, 2.5, v, 21.5)))
        parts.append(detail(seg(2.5, v, 21.5, v)))
    for cx, cy in ((5.67, 5.67), (12, 5.67), (5.67, 12), (18.33, 5.67)):
        parts.append(mark(star(cx, cy, 2.3, 1.0, L(S, 0, 0.3))))
    return parts


@icon("cubby", CAT, "Shelf unit of square cubbies with a small backpack stored in one of them",
      tags=["cubby", "cubbies", "cubby hole", "cloakroom", "classroom storage", "preschool"])
def _(S):
    bag = union(rect(5, 15, 4.5, 5, L(S, 0.5, 1.5)), path_to_d(ST("M6 15V14A1.25 1.25 0 0 1 8.5 14V15", 1.5, "round", "round")))
    return [
        shell(rect(2.5, 3, 19, 18.5, S.R)),
        detail(seg(12, 3, 12, 21.5)),
        detail(seg(2.5, 12.25, 21.5, 12.25)),
        mark(bag),
    ]


@icon("crossing-guard", CAT, "Crossing guard in a vest holding a round stop sign high on a pole",
      tags=["crossing guard", "lollipop lady", "lollipop man", "school crossing", "road safety", "stop sign"])
def _(S):
    return [
        head(7, 4.5, 2),
        shell(poly([(3.5, 8.5), (10.5, 8.5), (10, 15.5), (4, 15.5)], closed=True, r=L(S, 0, 1))),
        detail(seg(3.8, 12, 10.2, 12)),
        line(seg(5.5, 15.5, 5.5, 21.5)), line(seg(8.5, 15.5, 8.5, 21.5)),
        line(seg(10.3, 10.5, 16.5, 12.5)),
        line(seg(17, 9, 17, 21.5)),
        shell(circle(17, 5.5, 3.5)),
    ]


@icon("children-crossing", CAT, "Triangular warning sign with two children walking, one carrying a school bag",
      tags=["children crossing", "school zone", "school crossing", "road sign", "warning sign", "slow children"])
def _(S):
    def kid(x, top, h, bag=False):
        r = h * 0.14
        body = poly([(x - h * 0.13, top + 2 * r + 0.5), (x + h * 0.13, top + 2 * r + 0.5), (x + h * 0.2, top + h * 0.7), (x - h * 0.2, top + h * 0.7)], closed=True)
        legs = U(ST(seg(x - h * 0.1, top + h * 0.65, x - h * 0.18, top + h), 1.3, "butt", "miter"),
                 ST(seg(x + h * 0.1, top + h * 0.65, x + h * 0.18, top + h), 1.3, "butt", "miter"))
        shape = U(P(circle(x, top + r, r)), P(body), legs)
        if bag:
            shape = U(shape, P(rect(x - h * 0.2 - 1.8, top + 2 * r + 1, 1.6, 2.2, 0.4)))
        return Part("dot", path_to_d(shape))
    return [
        shell(poly([(12, 2), (22, 20.5), (2, 20.5)], closed=True, r=S.r)),
        kid(10, 8.5, 9.5, bag=True),
        kid(14.5, 10.5, 7.5),
    ]


@icon("nap-mat", CAT, "Folded out nap mat with a small pillow at one end and a sleepy Z above",
      tags=["nap mat", "rest mat", "sleeping mat", "nap time", "preschool", "daycare"])
def _(S):
    body = union(rect(2, 15, 20, 6.5, rr(S, 2)), rect(3.5, 11, 6.5, 5, rr(S, 2)))
    return [
        shell(body),
        detail(seg(3.5, 15, 10, 15)),
        detail(seg(12.5, 15, 12.5, 21.5)), detail(seg(17.25, 15, 17.25, 21.5)),
        line(poly([(14, 4), (19, 4), (14, 10), (19, 10)], r=S.r * 0.3)),
    ]


@icon("lunch-tray", CAT, "Cafeteria lunch tray divided into compartments of different sizes",
      tags=["lunch tray", "school lunch", "cafeteria", "canteen", "compartment tray", "meal tray"])
def _(S):
    return [
        shell(rect(2, 4.5, 20, 15, S.R)),
        detail(seg(2, 11.5, 22, 11.5)),
        detail(seg(8.5, 4.5, 8.5, 11.5)), detail(seg(15, 4.5, 15, 11.5)),
        detail(seg(13.5, 11.5, 13.5, 19.5)),
    ]


@icon("science-fair-board", CAT, "Trifold science fair display board standing open with a title and a bar chart",
      tags=["science fair", "trifold board", "display board", "school project", "presentation board", "poster board"])
def _(S):
    board = poly([(2, 6), (7.5, 3.5), (16.5, 3.5), (22, 6), (22, 18), (16.5, 20.5), (7.5, 20.5), (2, 18)], closed=True, r=L(S, 0, 0.8))
    return [
        shell(board),
        detail(seg(7.5, 3.5, 7.5, 20.5)), detail(seg(16.5, 3.5, 16.5, 20.5)),
        detail(seg(10, 7, 14, 7)),
        detail(seg(10, 17, 10, 13)), detail(seg(14, 17, 14, 10.5)),
    ]


@icon("googly-eyes", CAT, "Pair of round craft googly eyes with their loose pupils rolled to one side",
      tags=["googly eyes", "wiggle eyes", "craft eyes", "crafts", "silly", "arts and crafts"])
def _(S):
    parts = []
    for cx in (6.25, 17.75):
        parts.append(shell(circle(cx, 12, 3.75) if S.name == "line" else ellipse(cx, 12, 3.6, 4.1)))
        parts.append(dot(cx + 1.5, 13.3, 1.9))
    return parts


@icon("craft-stick", CAT, "Two flat wooden craft sticks with rounded ends crossed over each other",
      tags=["craft stick", "lolly stick", "tongue depressor", "crafts", "wooden stick"])
def _(S):
    rad = 2.25 if S.name == "rounded" else 1
    top = rot(rect(10, 1.5, 4.5, 21, rad), 30, 12.25, 12)
    under = rot(rect(10, 1.5, 4.5, 21, rad), -30, 12.25, 12)
    return [shell(behind(under, [top], gap=0.25)), shell(top)]


@icon("bead-pegboard", CAT, "Square pegboard with fuse beads set on the pegs in a heart pattern",
      tags=["bead pegboard", "fuse beads", "melty beads", "iron beads", "pixel art", "crafts"])
def _(S):
    parts = [shell(rect(2.5, 2.5, 19, 19, S.R))]
    rows = ["01010", "11111", "11111", "01110", "00100"]
    for j, row in enumerate(rows):
        for i, c in enumerate(row):
            if c == "1":
                parts.append(dot(6 + 3 * i, 6.5 + 3 * j, 1.1))
    return parts


@icon("base-ten-blocks", CAT, "Base ten maths blocks: a flat hundred square, a ten rod and a single unit cube",
      tags=["base ten blocks", "place value", "math manipulatives", "maths", "counting", "hundreds tens ones"])
def _(S):
    parts = [shell(rect(2, 10, 11, 11.5, rr(S, 1.5)))]
    for v in (5.67, 9.33):
        parts.append(detail(seg(v, 10, v, 21.5)))
    for h in (13.83, 17.67):
        parts.append(detail(seg(2, h, 13, h)))
    parts += [shell(rect(17, 10, 3, 11.5, L(S, 0, 1))), shell(rect(17, 3, 3, 3, L(S, 0, 1)))]
    return parts


@icon("geoboard", CAT, "Square geoboard with a grid of pegs and a rubber band stretched into a triangle",
      tags=["geoboard", "peg board", "rubber band", "geometry", "math manipulatives", "shapes"])
def _(S):
    parts = [shell(rect(2.5, 2.5, 19, 19, S.R))]
    for x in (7, 12, 17):
        for y in (7, 12, 17):
            parts.append(dot(x, y, 1.1))
    parts.append(detail(poly([(7, 17), (12, 7), (17, 17)], closed=True, r=S.r * 0.4)))
    return parts


@icon("paper-hat", CAT, "Folded newspaper hat with a pointed top and a turned up band",
      tags=["paper hat", "newspaper hat", "origami hat", "party hat", "crafts", "folded hat"])
def _(S):
    return [
        shell(poly([(3.5, 15), (12, 2.5), (20.5, 15)], closed=True, r=S.r)),
        shell(rect(2.5, 15, 19, 5.5, L(S, 0, 1.5))),
        detail(seg(10, 10, 14, 10)),
    ]


@icon("paper-crown", CAT, "Zigzag paper party crown with a band and little dots on its points",
      tags=["paper crown", "party crown", "birthday crown", "cracker crown", "paper hat", "crafts"])
def _(S):
    pts = [(3, 20.5), (3, 9), (7.5, 13.5), (12, 9), (16.5, 13.5), (21, 9), (21, 20.5)]
    parts = [shell(poly(pts, closed=True, r=S.r * 0.6)), detail(seg(3, 16.5, 21, 16.5))]
    for x in (3, 12, 21):
        parts.append(dot(x, 5.5, 1.5))
    return parts


@icon("paper-fortune-teller", CAT, "Folded paper fortune teller seen from above with four pointed pockets",
      tags=["paper fortune teller", "cootie catcher", "chatterbox", "origami", "playground game", "salt cellar"])
def _(S):
    outer = poly([(12, 2), (22, 12), (12, 22), (2, 12)], closed=True, r=S.r)
    return [
        shell(outer),
        detail(poly([(7, 7), (17, 7), (17, 17), (7, 17)], closed=True, r=0)),
        detail(seg(7, 7, 17, 17)), detail(seg(17, 7, 7, 17)),
    ]


@icon("bedtime-story", CAT, "Open storybook with a crescent moon and stars rising from its pages",
      tags=["bedtime story", "story time", "fairy tale", "reading", "goodnight", "picture book"])
def _(S):
    book = "M2.5 15.5Q7 13.5 12 16Q17 13.5 21.5 15.5V21Q17 19 12 21.5Q7 19 2.5 21Z"
    moon = minus(circle(9, 7.5, 4.5), circle(11.5, 5.5, 4))
    return [
        shell(book),
        detail(seg(12, 16, 12, 21.5)),
        shell(moon),
        mark(star(17.5, 6, 2.6, 1.15, L(S, 0, 0.3))),
    ]


@icon("kids-tablet", CAT, "Tablet in a chunky bumper case with a carry handle on top",
      tags=["kids tablet", "tablet case", "bumper case", "screen time", "learning tablet", "children's tablet"])
def _(S):
    body = union(rect(2, 7.5, 20, 14, S.R + 1), minus(rect(7, 2.5, 10, 7, L(S, 1, 3)), rect(9, 4.5, 6, 5, L(S, 0, 1))))
    return [
        shell(body),
        detail(rect(5.5, 11, 10.5, 7, L(S, 0, 1))),
        dot(19, 14.5, 1.1),
    ]


@icon("toilet-training-seat", CAT, "Padded child toilet seat ring with a handle on each side",
      tags=["potty seat", "toilet training seat", "toilet seat reducer", "potty training", "toddler", "bathroom"])
def _(S):
    ring = minus(ellipse(12, 13, 7, 8.5), ellipse(12, 13.5, 3.25, 4.5))
    return [
        shell(ring),
        line(poly([(5, 9.5), (2.5, 9.5), (2.5, 16), (5.2, 16)], r=S.r)),
        line(poly([(19, 9.5), (21.5, 9.5), (21.5, 16), (18.8, 16)], r=S.r)),
    ]


@icon("pacifier-clip", CAT, "Pacifier hanging from a short strap with a clip at the other end",
      tags=["pacifier clip", "dummy clip", "soother clip", "dummy chain", "baby", "pacifier"])
def _(S):
    return [
        shell(rect(2.5, 2, 4.5, 8, L(S, 0.5, 2))),
        detail(seg(4.75, 4.5, 4.75, 7.5)),
        line("M4.75 10C4.75 14.5 7 15 8.5 15"),
        line(circle(10.5, 15, 2)),
        shell(ellipse(15, 15, 1.75, 5) if S.name == "rounded" else rect(13.25, 10, 3.5, 10, 1)),
        shell(ellipse(19.5, 15, 2.5, 2) if S.name == "rounded" else "M16.75 13.5H19.5A1.5 1.5 0 0 1 19.5 16.5H16.75Z"),
    ]


@icon("bottle-drying-rack", CAT, "Drying rack tray with pegs holding two upside down baby bottles",
      tags=["bottle drying rack", "bottle rack", "drying rack", "baby bottles", "feeding", "sterilizing"])
def _(S):
    def bottle(x):
        return poly([(x, 3), (x + 5, 3), (x + 5, 11), (x + 3.5, 12.5), (x + 3.5, 14.5), (x + 1.5, 14.5), (x + 1.5, 12.5), (x, 11)], closed=True, r=L(S, 0, 0.6))
    return [
        shell(rect(2, 18.5, 20, 3.5, rr(S, 1.5))),
        shell(bottle(3)), shell(bottle(11)),
        line(seg(19.5, 8, 19.5, 18.5)),
        line(seg(5.5, 14.5, 5.5, 18.5)), line(seg(13.5, 14.5, 13.5, 18.5)),
    ]


@icon("formula-dispenser", CAT, "Stacked formula dispenser with three round compartments and a funnel spout on top",
      tags=["formula dispenser", "formula container", "milk powder", "baby formula", "feeding", "travel"])
def _(S):
    k = 2 if S.name == "rounded" else 0.75
    body = union(rect(4, 9, 16, 4.5, k), rect(4, 13, 16, 4.5, k), rect(4, 17, 16, 4.5, k),
                 poly([(8, 9.5), (10.5, 3), (13.5, 3), (16, 9.5)], closed=True, r=L(S, 0, 0.6)))
    return [
        shell(body),
        detail(seg(4, 13.25, 20, 13.25)), detail(seg(4, 17.25, 20, 17.25)),
    ]


@icon("baby-car-mirror", CAT, "Wide car seat mirror strapped to a headrest showing a small baby face",
      tags=["baby car mirror", "car seat mirror", "rear facing mirror", "back seat mirror", "baby", "car travel"])
def _(S):
    return [
        shell("M5 8.5V5A3 3 0 0 1 8 2H16A3 3 0 0 1 19 5V8.5Z" if S.name == "rounded" else rect(5, 2, 14, 6.5, 1)),
        line(seg(8.5, 8.5, 8.5, 10.5)), line(seg(15.5, 8.5, 15.5, 10.5)),
        shell(rect(2, 10.5, 20, 11, L(S, 2.5, 5.5))),
        detail(circle(12, 16, 3.25)),
        dot(10.75, 15.6, 0.9), dot(13.25, 15.6, 0.9),
    ]


# ============================================================================ chunk 6: the last few

@icon("pencil-sharpener", CAT, "Small wedge shaped pencil sharpener with a pencil pushed into its side and a shaving curling up above",
      tags=["pencil sharpener", "sharpener", "pencil shavings", "school supplies", "stationery", "back to school"])
def _(S):
    return [
        shell(poly([(1.5, 13), (8, 13), (11, 16.25), (8, 19.5), (1.5, 19.5)], closed=True, r=S.r)),
        detail(seg(4.75, 13, 4.75, 19.5)),
        shell(poly([(11, 10), (21.5, 13.5), (21.5, 21.5), (11, 21.5)], closed=True, r=S.r)),
        dot(17, 17.5, 1.25),
        line("M12 6.5C12 3.3 17.5 2.8 17.5 5.6C17.5 7.6 14.6 7.6 14.6 5.9"),
    ]


@icon("finger-paint", CAT, "Child's open hand with a blob of paint on the palm, ready to make a handprint",
      tags=["finger paint", "finger painting", "handprint", "hand print", "messy play", "art class", "paint"])
def _(S):
    hand = poly([(7, 22), (7, 18.5), (3, 14.5), (4.3, 12.3), (7, 14.3), (7, 8), (10.5, 8), (10.5, 4), (14, 4), (14, 4.5),
                 (17.5, 4.5), (17.5, 8.5), (21, 8.5), (21, 22)], closed=True, r=S.r)
    return [
        shell(hand),
        detail(seg(10.5, 8, 10.5, 13)),
        detail(seg(14, 4.5, 14, 13)),
        detail(seg(17.5, 8.5, 17.5, 13)),
        dot(14, 17.5, 2),
    ]


@icon("paper-lunch-bag", CAT, "Brown paper lunch bag with the top rolled down and a small heart drawn on the front",
      tags=["paper lunch bag", "brown bag", "packed lunch", "lunch sack", "school lunch", "paper bag", "picnic"])
def _(S):
    return [
        shell(poly([(6, 9), (4.5, 21.5), (19.5, 21.5), (18, 9)], closed=True, r=S.r)),
        shell(rect(3.5, 3, 17, 6.5, L(S, 1, 2.5))),
        detail("M12 19C8.6 16.5 9 13.6 10.6 13.6C11.5 13.6 12 14.2 12 14.8C12 14.2 12.5 13.6 13.4 13.6C15 13.6 15.4 16.5 12 19Z"),
    ]


def _chain_region(S, w):
    """Three paper links on a diagonal; each link threads through the next (over at one crossing, under at the other)."""
    r = L(S, 2, 4)
    size, step = 9.0, 5.5
    links = [rect(2 + i * step, 2 + i * step, size, size, r) for i in range(3)]
    regs = [ST(d, w, S.cap, S.join) for d in links]
    hw = 2 * 1.25 + w
    for i in range(2):
        ox = i * step
        # link i+1 passes over link i at the lower-left crossing ...
        regs[i] = D(regs[i], ST(seg(7.5 + ox, 9, 7.5 + ox, 13), hw, "round", "round"))
        # ... and under it at the upper-right crossing
        regs[i + 1] = D(regs[i + 1], ST(seg(11 + ox, 5.5 + ox, 11 + ox, 9.5 + ox), hw, "round", "round"))
    return U(*regs)


@icon("paper-chain", CAT, "Three linked loops of paper strip forming a short paper chain",
      tags=["paper chain", "paper links", "chain decoration", "party decoration", "kids craft", "garland", "christmas craft"],
      filled=lambda: _chain_region(LINE_S, 2.7))
def _(S):
    return [Part("solid", path_to_d(_chain_region(S, 2.0)))]
