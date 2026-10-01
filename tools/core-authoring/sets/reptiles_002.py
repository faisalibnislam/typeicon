"""TypeIcon Core: reptiles and amphibians (batch 002).

Turtle and crocodile scenes, frog life stages and poses, salamanders and newts, and reptile keeping gear.
Side views face right unless noted; top views are symmetric with the head up.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "reptiles"


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


def thick(d, w, S):
    return path_to_d(ST(d, w, S.cap, S.join))


def flip(d):
    """Mirror a d-string across the vertical centre line."""
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def grow(d, g):
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled body."""
    return Part("dot", d)


def _p(p):
    return f"{fmt(p[0])} {fmt(p[1])}"


def teeth(p0, p1, n, h, w, side=1):
    """Row of n triangles along the edge p0 to p1, pointing to one side (side = +1 or -1)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy * side, ux * side
    out = []
    for i in range(n):
        t = (i + 0.5) / n
        cx, cy = p0[0] + dx * t, p0[1] + dy * t
        a = (cx - ux * w / 2, cy - uy * w / 2)
        b = (cx + ux * w / 2, cy + uy * w / 2)
        c = (cx + nx * h, cy + ny * h)
        out.append(poly([a, b, c], closed=True))
    return union(*out)


def turtle_mini(cx, by, k=1.0):
    """Small solid turtle silhouette facing right, standing on y = by."""
    dome = (f"M{fmt(cx - 5 * k)} {fmt(by)}C{fmt(cx - 5 * k)} {fmt(by - 3.6 * k)} {fmt(cx - 2.6 * k)} {fmt(by - 5 * k)} {fmt(cx)} {fmt(by - 5 * k)}"
            f"C{fmt(cx + 2.6 * k)} {fmt(by - 5 * k)} {fmt(cx + 5 * k)} {fmt(by - 3.6 * k)} {fmt(cx + 5 * k)} {fmt(by)}Z")
    head = circle(cx + 6.2 * k, by - 2.2 * k, 1.6 * k)
    legs = [rect(cx - 3.8 * k, by - 0.5 * k, 2.2 * k, 1.5 * k), rect(cx + 1.8 * k, by - 0.5 * k, 2.2 * k, 1.5 * k)]
    return union(dome, head, *legs)


def wave(x0, x1, y, amp=1.0, step=4.0):
    """Wavy water line from x0 to x1 made of quadratic arches."""
    d = f"M{fmt(x0)} {fmt(y)}"
    x = x0
    up = True
    while x < x1 - 0.01:
        nx = min(x + step, x1)
        d += f"Q{fmt((x + nx) / 2)} {fmt(y - amp * 2 if up else y + amp * 2)} {fmt(nx)} {fmt(y)}"
        up = not up
        x = nx
    return d


# ============================================================================ turtles

@icon("turtle-nest", CAT, "Shallow hollow in the sand holding a pile of round turtle eggs",
      tags=["turtle eggs", "nesting", "hatchery", "beach", "conservation", "sea turtle"])
def _(S):
    ground = "M2 16.5H5C9 21.5 15 21.5 19 16.5H22"
    eggs = [rot(ellipse(8.6, 13.4, 2.3, 3), -18, 8.6, 13.4), rot(ellipse(15.4, 13.4, 2.3, 3), 18, 15.4, 13.4), ellipse(12, 7.6, 2.3, 3)]
    return [line(ground)] + [solid(e) for e in eggs]


@icon("turtle-tank", CAT, "Glass tank with water, a basking ramp and a small turtle resting on the ramp",
      tags=["turtle aquarium", "pet turtle", "basking", "habitat", "terrapin", "enclosure"])
def _(S):
    tank = rect(2.5, 3.5, 19, 17, L(S, 1, 3))
    ramp = poly([(2.5, 14.5), (11, 14.5), (15, 20.5)], r=S.r)
    return [shell(tank), detail(ramp), detail(wave(15.6, 21.5, 17, 0.7, 3)), mark(turtle_mini(6.2, 13.2, 0.7))]


@icon("turtle-tracks", CAT, "Two rows of flipper marks with a drag line running between them",
      tags=["sea turtle", "beach", "nesting trail", "footprints", "crawl", "marks"])
def _(S):
    return [line(seg(12, 3, 12, 21)),
            line(seg(4.5, 4.5, 8, 8)), line(seg(4.5, 13, 8, 16.5)),
            line(seg(19.5, 8.5, 16, 12)), line(seg(19.5, 17, 16, 20.5))]


@icon("turtle-crossing-sign", CAT, "Diamond road sign on a post showing a turtle",
      tags=["road sign", "wildlife crossing", "warning", "traffic", "turtles ahead", "drive carefully"])
def _(S):
    d = poly([(12, 1.8), (20.2, 10), (12, 18.2), (3.8, 10)], closed=True, r=S.r)
    return [shell(d), line(seg(12, 18.2, 12, 22)), mark(turtle_mini(11.6, 11.8, 0.9))]


@icon("tortoise-and-hare", CAT, "Small domed tortoise walking towards a finish flag while a hare sleeps above it with a Z of sleep",
      tags=["fable", "slow and steady", "race", "patience", "story", "aesop", "persistence"])
def _(S):
    hare = union(ellipse(8.8, 9, 5.8, 2.5), ellipse(15.4, 9, 2.4, 2.1), rot(ellipse(11.8, 5.8, 3.8, 0.9), 14, 11.8, 5.8),
                 rot(ellipse(8, 7.4, 1.2, 1.6), 0, 8, 7.4))
    tort = turtle_mini(9.6, 20.6, 1.1)
    return [solid(hare), solid(tort), line(seg(20.6, 10.4, 20.6, 21)), solid(rect(16.6, 10.8, 4, 3.4)),
            line(poly([(18, 3.4), (20.4, 3.4), (18, 6), (20.4, 6)], r=S.r))]


@icon("crocodile-lurking", CAT, "Water line with only a crocodile's two eye bumps and nostril bump showing above it",
      tags=["ambush", "hidden", "swamp", "danger", "river", "stalking", "crocodile eyes"])
def _(S):
    top = 13.8
    bumps = [solid(clip(circle(7, top, 3), rect(0, 0, 24, top))), solid(clip(circle(13.5, top, 3), rect(0, 0, 24, top))),
             solid(clip(circle(20, top, 2), rect(0, 0, 24, top)))]
    return [line(wave(2, 22, top + 0.5, 0.6, 5)), line(wave(5, 19, 19.5, 0.6, 5))] + bumps


def croc_mini(cx, by, k=1.0):
    """Small solid crocodile silhouette facing right; by is the baseline under its feet."""
    pts = [(-6, -0.2), (-3, -2.4), (1, -3), (6.4, -2.4), (6.4, -0.8), (2.6, -0.6), (2.2, 1), (0.6, 1), (0.4, -0.2),
           (-2, -0.2), (-2.3, 1), (-3.9, 1), (-4, 0.1)]
    return poly([(cx + x * k, by - 1 * k + y * k) for x, y in pts], closed=True)


def jaw_pair(S, upper_pts, lower_pts, up_edge, lo_edge, n_up, n_lo, th=2.3, tw=2.6, skip_up=(), skip_lo=()):
    """Open crocodile jaws: two outlined jaws with solid teeth along the mouth edges."""
    r = L(S, 0, 0.8)
    out = [shell(poly(upper_pts, closed=True, r=r)), shell(poly(lower_pts, closed=True, r=r))]
    out.append(solid(teeth(up_edge[0], up_edge[1], n_up, th, tw, side=-1)))
    out.append(solid(teeth(lo_edge[0], lo_edge[1], n_lo, th, tw, side=1)))
    return out


@icon("crocodile-jaws", CAT, "Side view of a crocodile head with its jaws gaping wide and rows of pointed teeth",
      tags=["alligator", "bite", "open mouth", "predator", "snap", "teeth", "danger"])
def _(S):
    upper = [(3, 12), (3, 7.5), (6.5, 5.5), (12, 4.6), (21.5, 3.4), (21.5, 6.6), (4.5, 12)]
    lower = [(3, 13), (4.5, 13), (21.5, 18.6), (21.5, 21.6), (6.5, 17.5), (3, 16.5)]
    parts = jaw_pair(S, upper, lower, ((20.5, 7.2), (7, 11.4)), ((20.5, 18), (7.5, 13.8)), 4, 4, th=2.2, tw=2.6)
    return parts + [mark(circle(8.6, 8.4, 0.8))]


@icon("crocodile-hatchling", CAT, "Cracked egg with a baby crocodile head and snout poking out of the top",
      tags=["baby crocodile", "hatching", "newborn", "egg", "reptile", "croc", "young"])
def _(S):
    zig = [(2, 14), (5, 11), (8, 14), (11, 11), (14, 14), (17, 11), (20, 14), (22, 11)]
    mask = poly(zig + [(22, 24), (2, 24)], closed=True, r=S.r)
    egg = clip(ellipse(12, 16.2, 8.6, 6.3), mask)
    head = poly([(6, 14), (6.5, 7.5), (9.5, 4.2), (15, 3.4), (21.5, 6), (21.5, 9.4), (15.5, 9.4), (14.5, 14)], closed=True, r=L(S, 0, 1))
    return [shell(egg), shell(minus(head, egg)), mark(circle(10.8, 7.2, 0.8)), detail(poly(zig[1:7], r=S.r))]


# ============================================================================ frog helpers

def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def tube(ctrl, width, n=40):
    """Closed outline around a cubic centreline whose width varies with t."""
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


def sc(d, k, ox, oy):
    """Scale d about the origin by k, then move by (ox, oy)."""
    return path_to_d(transform_path(P(d), (k, 0, 0, k, ox, oy)))


def limb(pts, w, S=None):
    """Rounded leg or arm stroke (always round, so limbs stay soft inside the silhouette)."""
    return path_to_d(ST(poly(pts), w, "round", "round"))


def frog_top(S, hind=((8.6, 15.4), (4.4, 15), (5.2, 20), (9, 20.8)), front=((8.2, 10.6), (5, 11.8), (4.2, 9.6)), w=2.4):
    """Top view of a sitting frog, head up: body, bulging eyes and four folded legs (as one outline)."""
    body = union(ellipse(12, 12.8, 4.2, 5.3), ellipse(12, 8.4, 4.6, 3.2), circle(9, 5.9, 1.8), circle(15, 5.9, 1.8))
    legs = []
    for pts in (hind, front):
        legs.append(limb(list(pts), w, S))
        legs.append(limb([(24 - x, y) for x, y in pts], w, S))
    return union(body, *legs)


def frog_front(S, k=1.0, ox=0.0, oy=0.0):
    """Sitting frog seen from the front: wide body, two bulging eyes, feet. Returns (outline d, detail parts)."""
    body = union(ellipse(12, 13.6, 8.4, 5.6), circle(7.6, 8.2, 3), circle(16.4, 8.2, 3), ellipse(6, 19.4, 3.2, 1.7), ellipse(18, 19.4, 3.2, 1.7))
    d = sc(body, k, ox, oy)
    parts = [mark(circle(7.6 * k + ox, 8.4 * k + oy, 1.15 * k + 0.1)), mark(circle(16.4 * k + ox, 8.4 * k + oy, 1.15 * k + 0.1)),
             detail(sc("M6.2 13.4C9 16.4 15 16.4 17.8 13.4", k, ox, oy))]
    return d, parts


# ============================================================================ tadpoles and spawn

@icon("tadpole", CAT, "Tadpole with a round head, a small eye and a long wavy tapering tail",
      tags=["baby frog", "pollywog", "amphibian larva", "pond", "metamorphosis", "swim"])
def _(S):
    tail = tube(((11, 11.5), (14.5, 7), (17.5, 17), (22, 11.5)), lambda t: 4.4 * (1 - t) + 0.4)
    head = ellipse(8, 11.5, 5.4, 4.6)
    return [shell(union(head, poly(tail, closed=True))), mark(circle(6.4, 10, 0.9))]


@icon("frog-spawn", CAT, "Cluster of round jelly-like frog eggs, each with a dark dot at its center",
      tags=["frogspawn", "eggs", "pond", "amphibian eggs", "tadpole eggs", "spring", "nature"])
def _(S):
    cs = [(7.2, 8), (14.8, 7.6), (4.4, 14.8), (11.4, 14.4), (18.8, 14.2)]
    out = []
    prev = []
    for (x, y) in cs:
        c = circle(x, y, 3.2)
        out.append(shell(minus(c, *prev) if prev else c))
        out.append(mark(circle(x, y, 1.0)))
        prev.append(c)
    return out + [line(wave(2.5, 21.5, 20.8, 0.6, 4.5))]


# ============================================================================ frog species and poses

@icon("poison-dart-frog", CAT, "Small frog seen from above with bold irregular patches across its back and round toe tips",
      tags=["poison frog", "rainforest", "toxic", "bright colors", "amphibian", "dendrobatid", "venomous"])
def _(S):
    pads = [circle(x, y, 1.6) for x, y in ((4.2, 9.2), (19.8, 9.2), (7.4, 21), (16.6, 21))]
    fr = frog_top(S, hind=((9, 15), (4.8, 16.4), (7.2, 20.6)), front=((8.6, 10.6), (5, 11), (4.2, 9.2)), w=2.2)
    patches = [mark(ellipse(10.6, 12, 1.6, 1.2)), mark(ellipse(13.8, 14, 1.2, 1.7)), mark(circle(10.6, 15.8, 1))]
    return [shell(union(fr, *pads))] + patches


@icon("frog-croaking", CAT, "Frog seen from the front with a round vocal sac swelling under its chin and sound arcs on both sides",
      tags=["ribbit", "frog call", "mating call", "noise", "pond at night", "vocal sac", "amphibian"])
def _(S):
    body = union(ellipse(12, 10.4, 6.8, 4.6), circle(8, 5.6, 2.7), circle(16, 5.6, 2.7))
    sac = minus(circle(12, 16.6, 4.7), body)
    return [shell(body), shell(sac), mark(circle(8, 5.8, 1.1)), mark(circle(16, 5.8, 1.1)),
            line(arc(12, 10.4, 9.8, -26, 26)), line(arc(12, 10.4, 9.8, 154, 206))]


@icon("frog-leaping", CAT, "Side view of a frog mid-jump with its back legs fully stretched behind and front legs reaching ahead",
      tags=["jump", "hop", "spring", "bounce", "leap frog", "amphibian", "pond"])
def _(S):
    body = union(rot(ellipse(12.5, 11.4, 5.6, 3.2), -22, 12.5, 11.4), circle(17.6, 8.6, 2.9), circle(18.4, 6.4, 1.6))
    legs = union(limb([(10.4, 12), (6.2, 15.6), (2.6, 19.4)], 2.2, S), limb([(15, 13), (18.6, 16), (21.4, 16.6)], 2.2, S),
                 limb([(2.6, 19.4), (4.6, 21.4)], 2.2, S))
    return [shell(union(body, legs)), mark(circle(18.6, 6.2, 0.7))]


@icon("frog-swimming", CAT, "Top view of a frog swimming with its back legs kicked wide and ripples beside it",
      tags=["breaststroke", "pond", "water", "swim", "paddle", "amphibian", "ripples"])
def _(S):
    fr = frog_top(S, hind=((9.4, 15.4), (5.6, 18.6), (3.4, 21.4)), front=((8.4, 10.4), (5.4, 8.8), (3.6, 9.8)), w=2.2)
    return [shell(fr), mark(circle(9, 5.9, 0.7)), mark(circle(15, 5.9, 0.7))]


@icon("frog-on-lily-pad", CAT, "Frog sitting on a round lily pad with a notch cut in it, floating on the water line",
      tags=["pond", "water lily", "sitting frog", "nature", "amphibian", "calm", "marsh"])
def _(S):
    d, parts = frog_front(S, 0.66, 6.1, 3.2)
    pad = minus(minus(ellipse(12, 16.6, 9.6, 2.7), "M12.6 16.6L22 14L22 19.4Z"), d)
    return [shell(d), shell(pad)] + parts + [line(wave(2, 22, 21.4, 0.5, 4))]


@icon("frog-catching-fly", CAT, "Frog shooting a long curved tongue at a small winged fly",
      tags=["tongue", "hunting", "feeding", "insect", "catch", "amphibian", "pond"])
def _(S):
    d, parts = frog_front(S, 0.8, 1.2, 5)
    fly = union(circle(19.6, 4.4, 1.2), ellipse(18, 3, 1.6, 0.8), ellipse(21.4, 3, 1.6, 0.8))
    return [shell(d)] + parts + [line("M12 14.6C12.4 11 16 11 19.4 6.2"), solid(fly)]




# ============================================================================ reptile keeping and anatomy

@icon("reptile-egg", CAT, "Single elongated oval leathery egg with a slight dent on one side",
      tags=["leathery egg", "clutch", "hatch", "lizard egg", "snake egg", "nest", "oviparous"])
def _(S):
    if S.name == "line":
        egg = ("M12 2.8C14.4 2.8 18.5 6.8 18.5 11.2C17.2 12.6 17.2 14.6 18.6 16.2C18 19 15.4 21.2 12 21.2"
               "C8.6 21.2 5.5 18.4 5.5 13.2C5.5 8 10 3.6 12 2.8Z")
    else:
        egg = ("M12 2.8C15.4 2.8 18.5 7 18.5 11.2C17.2 12.6 17.2 14.6 18.6 16.2C18 19 15.4 21.2 12 21.2"
               "C8.6 21.2 5.5 18.4 5.5 13.2C5.5 7.6 8.6 2.8 12 2.8Z")
    return [shell(egg), detail("M9 11c1.2 1 1.2 3.2 0 4.4")]


def almond(S, cy=13, h=7.5):
    if S.name == "line":
        return f"M2 {cy}C6 {cy - h} 18 {cy - h} 22 {cy}C18 {cy + h} 6 {cy + h} 2 {cy}Z"
    return f"M2.5 {cy}C6.5 {cy - h} 17.5 {cy - h} 21.5 {cy}C17.5 {cy + h} 6.5 {cy + h} 2.5 {cy}Z"


@icon("reptile-eye", CAT, "Almond-shaped eye with a narrow vertical slit pupil under a scalloped scaly brow ridge",
      tags=["snake eye", "lizard eye", "slit pupil", "cat eye", "vision", "predator", "dragon"])
def _(S):
    brow = "M4 5a2 2 0 0 1 4 0a2 2 0 0 1 4 0a2 2 0 0 1 4 0a2 2 0 0 1 4 0"
    brow = "M3.5 6.2a2.1 2.1 0 0 1 4.2 0a2.1 2.1 0 0 1 4.2 0a2.1 2.1 0 0 1 4.2 0a2.1 2.1 0 0 1 4.2 0"
    return [shell(almond(S, 14, 6.6)), mark(ellipse(12, 14, 1.4, 3.7)), line(brow)]


@icon("reptile-scales", CAT, "Square swatch covered in rows of overlapping rounded scales",
      tags=["scale pattern", "snake skin", "lizard skin", "texture", "armor", "fish scale", "pattern"])
def _(S):
    sq = rect(3, 3, 18, 18, L(S, 1, 3))
    rows = []
    for ri, y in enumerate((6.5, 12.5, 18.5)):
        if ri % 2 == 0:
            for x in (6, 12, 18):
                rows.append(arc(x, y, 3, 0, 180))
        else:
            rows.append(arc(3, y, 3, 0, 90))
            rows.append(arc(9, y, 3, 0, 180))
            rows.append(arc(15, y, 3, 0, 180))
            rows.append(arc(21, y, 3, 90, 180))
    return [shell(sq), detail("".join(rows))]


@icon("heat-mat", CAT, "Flat rectangular heating pad with a looping heating element inside and a cord leaving one corner",
      tags=["under tank heater", "terrarium heat", "warmth", "pet heating", "reptile enclosure", "thermostat", "pad"])
def _(S):
    pad = rect(2.5, 5.5, 15, 12, L(S, 1, 3))
    coil = "M6.5 9.5H12a2.25 2.25 0 0 1 0 4.5H6.5"
    cord = "M17.5 15.5H19.5a2 2 0 0 1 2 2V21"
    return [shell(pad), detail(coil), line(cord)]


@icon("reptile-hide", CAT, "Half hollow log shaped like an arch resting on the ground with a dark opening at the front",
      tags=["hideout", "shelter", "terrarium", "cave", "snake hide", "lizard shelter", "enclosure"])
def _(S):
    log = "M2.5 19.5V14a9.5 9.5 0 0 1 19 0v5.5Z"
    return [shell(log), mark("M8.2 19.5V16.4a3.8 3.8 0 0 1 7.6 0V19.5Z"),
            detail("M5.2 13.5C5.8 11 7 9.6 9 8.6")]


@icon("basking-rock", CAT, "Flat-topped rock slab with wavy heat lines rising from its top",
      tags=["basking spot", "heat lamp", "warm rock", "sun", "turtle haul out", "terrarium", "stone"])
def _(S):
    rock = poly([(2.5, 19.5), (3.2, 15.2), (6.2, 12.6), (17.5, 12.6), (20.6, 15), (21.5, 19.5)], closed=True, r=L(S, 0, 2))
    heat = ["M8 9.2q-1.6-1.4 0-2.8t0-2.8", "M12 9.2q-1.6-1.4 0-2.8t0-2.8", "M16 9.2q-1.6-1.4 0-2.8t0-2.8"]
    return [shell(rock), detail(poly([(14.5, 15), (12.6, 17), (14.2, 18.6)], r=0))] + [line(h) for h in heat]


def rp(x, y, deg=-30, cx=12, cy=12):
    a = math.radians(deg)
    dx, dy = x - cx, y - cy
    return (cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a))


@icon("feeding-tongs", CAT, "Long tweezer-style feeding tongs pinching a small cricket at the tip",
      tags=["tweezers", "pet feeding", "insect", "cricket", "reptile care", "forceps", "live food"])
def _(S):
    cr = path_to_d(transform_path(P(ellipse(18.2, 6.6, 3.4, 2.1)), rotation(-45, 18.2, 6.6)))
    return [line(poly([(3, 21), (14.2, 9.6)])), line(poly([(3, 21), (17, 13.4)])), solid(cr),
            line(seg(20.2, 4.4, 21.6, 2.4)), line(seg(21, 6, 22, 5.2))]


@icon("webbed-frog-foot", CAT, "Single frog foot with long thin toes joined by webbing between them",
      tags=["frog feet", "swimming", "amphibian", "webbing", "toes", "paddle", "pond"])
def _(S):
    tips = [(3.8, 9.8), (7.9, 5.2), (12, 3.9), (16.1, 5.2), (20.2, 9.8)]
    seq = tips[::-1]
    path = f"M10.2 22H13.8L14.6 17.6L{fmt(seq[0][0])} {fmt(seq[0][1])}"
    for i in range(1, 5):
        mx, my = (seq[i - 1][0] + seq[i][0]) / 2, (seq[i - 1][1] + seq[i][1]) / 2
        path += f"Q{fmt(mx + (12 - mx) * 0.1)} {fmt(my + (16.5 - my) * 0.45)} {fmt(seq[i][0])} {fmt(seq[i][1])}"
    path += "L9.4 17.6Z"
    toes = "".join(f"M12 17.2L{fmt(x + (12 - x) * 0.1)} {fmt(y + (17.2 - y) * 0.1 + 0.6)}" for x, y in tips)
    return [shell(path), detail(toes)]


def tri_sign(S, apex=2.6, base=20.4, hw=10):
    return poly([(12, apex), (12 + hw, base), (12 - hw, base)], closed=True, r=L(S, 0, 2.2))


@icon("crocodile-warning-sign", CAT, "Rounded warning triangle showing a crocodile above a wavy water line",
      tags=["crocodile ahead", "danger sign", "beware", "wildlife hazard", "swimming ban", "alligator warning", "caution"])
def _(S):
    return [shell(tri_sign(S)), mark(croc_mini(12.3, 16.3, 0.78)), line(wave(8, 16, 18.4, 0.5, 4))]


def toad_mini(cx, by, k=1.0):
    """Small solid toad in side view facing right, standing on y = by."""
    body = (f"M{fmt(cx - 5.5 * k)} {fmt(by)}C{fmt(cx - 5.8 * k)} {fmt(by - 3.4 * k)} {fmt(cx - 3.6 * k)} {fmt(by - 4.8 * k)} {fmt(cx - 1 * k)} {fmt(by - 4.8 * k)}"
            f"C{fmt(cx + 1.8 * k)} {fmt(by - 4.8 * k)} {fmt(cx + 3.4 * k)} {fmt(by - 4.2 * k)} {fmt(cx + 4.8 * k)} {fmt(by - 3 * k)}"
            f"L{fmt(cx + 6 * k)} {fmt(by - 2.2 * k)}L{fmt(cx + 5.8 * k)} {fmt(by)}Z")
    return union(body, circle(cx + 3.6 * k, by - 5 * k, 1.2 * k))


@icon("toad-crossing-sign", CAT, "Triangular road sign on a post showing a squat toad",
      tags=["toad migration", "road sign", "amphibian crossing", "wildlife warning", "drive carefully", "spring", "traffic"])
def _(S):
    d = poly([(12, 1.8), (21, 15.6), (3, 15.6)], closed=True, r=L(S, 0, 2))
    return [shell(d), line(seg(12, 15.6, 12, 22)), mark(toad_mini(11.6, 13.6, 0.95))]


@icon("toad-house", CAT, "Small upturned clay pot with an arched doorway cut into its rim, standing on the ground",
      tags=["garden toad", "flower pot", "shelter", "wildlife garden", "amphibian home", "terracotta", "frog house"])
def _(S):
    body = union(poly([(8, 4), (16, 4), (18, 13.5), (6, 13.5)], closed=True, r=L(S, 0, 1.2)), rect(4, 13, 16, 7, L(S, 0.5, 2)))
    return [shell(body), mark("M9.2 20V17.4a2.8 2.8 0 0 1 5.6 0V20Z"), line("M2 20.5H4"), line("M20 20.5H22")]


@icon("reptile-incubator", CAT, "Egg incubator box with a window showing a row of eggs and a thermometer dial on the front",
      tags=["hatching box", "egg hatching", "temperature control", "breeder", "clutch", "thermometer", "humidity"])
def _(S):
    box = rect(2.5, 3.5, 19, 17, L(S, 1, 3))
    win = rect(5.5, 6, 13, 6, L(S, 0, 1.5))
    eggs = [mark(ellipse(x, 9, 1.3, 1.7)) for x in (8.8, 12, 15.2)]
    return [shell(box), detail(win)] + eggs + [detail(circle(8.5, 16.8, 2)), mark(circle(8.5, 16.8, 0.5)), detail("M13 15.8H18.5"), detail("M13 18.2H17")]


@icon("reptile-egg-candling", CAT, "Small flashlight shining up through an egg, showing a curled embryo inside",
      tags=["egg check", "embryo", "fertile egg", "flashlight", "incubation", "breeding", "light test"])
def _(S):
    egg = ellipse(12, 8, 4.8, 6.2)
    torch = poly([(7.4, 15.6), (16.6, 15.6), (14.6, 18.4), (9.4, 18.4)], closed=True, r=S.r)
    return [shell(egg), detail(arc(12, 8.2, 1.9, -40, 250)), shell(torch), shell(rect(9.8, 18.4, 4.4, 3.6, L(S, 0.5, 1.5)))]


@icon("reptile-terrarium", CAT, "Glass tank with a lizard resting on a branch inside and a heat lamp dome on top",
      tags=["vivarium", "lizard tank", "pet reptile", "habitat", "heat lamp", "enclosure", "gecko"])
def _(S):
    tank = rect(2.5, 9, 19, 12, L(S, 1, 3))
    lamp = "M8.5 8A3.5 3.5 0 0 1 15.5 8Z"
    lizard = union(thick("M7.5 15.6Q11.5 16 15 14", 2.8, S), circle(16.6, 13.6, 1.9), thick("M7.5 15.6Q4.6 15 4.6 12.4", 1.4, S))
    return [shell(tank), shell(lamp), line("M5 17.8H19"), mark(lizard)]


# ============================================================================ more crocodilians

@icon("gharial", CAT, "Side view of a crocodilian with an extremely long thin snout ending in a round bulb at the tip",
      tags=["gharial", "gavial", "fish eating crocodile", "river", "long snout", "india", "crocodilian"])
def _(S):
    body = poly([(1.8, 14.6), (5, 12.2), (9, 11.4), (13.4, 11.4), (14.8, 12.8), (13.2, 14.2), (10.8, 14.4), (10.6, 16.6), (8.4, 16.6),
                 (8, 14.8), (5.4, 14.8), (5, 16.6), (2.8, 16.6)], closed=True, r=L(S, 0, 0.6))
    return [solid(body), line("M13.6 12.2L19.8 9.8"), solid(circle(20.6, 8.8, 1.9)), line(wave(2.5, 21.5, 20, 0.6, 4.75))]


@icon("crocodile-skull", CAT, "Top view of a long flat crocodile skull with two eye sockets and teeth along the snout",
      tags=["crocodile bones", "alligator skull", "fossil", "predator", "teeth", "anatomy", "skeleton"])
def _(S):
    out = poly([(8.6, 2.5), (15.4, 2.5), (17.4, 10), (20.2, 12.6), (20.4, 18.4), (15.6, 21.6), (8.4, 21.6), (3.6, 18.4), (3.8, 12.6), (6.6, 10)],
               closed=True, r=S.r)
    tl = teeth((9.4, 4.6), (8.4, 10), 2, 1.8, 2.8, side=-1)
    tr = teeth((14.6, 4.6), (15.6, 10), 2, 1.8, 2.8, side=1)
    return [shell(out), mark(tl), mark(tr), mark(circle(8.2, 16, 1.7)), mark(circle(15.8, 16, 1.7))]


@icon("crocodile-plover", CAT, "Crocodile head with its jaws open and a small bird standing inside the mouth beside the teeth",
      tags=["egyptian plover", "symbiosis", "cleaning", "mutualism", "bird", "bold bird", "teeth cleaning"])
def _(S):
    upper = [(3, 9), (3, 5.5), (6.5, 3.8), (12, 3), (21.5, 2.4), (21.5, 5.2), (4.5, 9)]
    lower = [(3, 14.4), (4.5, 14.4), (21.5, 19.4), (21.5, 22), (6.5, 19.2), (3, 17.6)]
    parts = jaw_pair(S, upper, lower, ((20.5, 5.8), (7, 8.9)), ((20.5, 18.8), (7.5, 14.9)), 2, 2, th=1.8, tw=2.6)
    bird = union(ellipse(14.4, 12, 3, 2), circle(17.6, 10, 1.6), thick("M18.8 10.2L21 10.8", 0.9, S),
                 thick("M13.2 13.4L13.2 15.6", 1.1, S), thick("M15.6 13.4L15.6 15.6", 1.1, S))
    return parts + [mark(circle(8.2, 6.2, 0.8)), solid(bird)]


# ============================================================================ frogs, toads and newts

def tadpole_mini(cx, cy, k=1.0):
    return union(circle(cx, cy, 1.5 * k), thick(f"M{fmt(cx + 1 * k)} {fmt(cy)}Q{fmt(cx + 2.4 * k)} {fmt(cy + 1.4 * k)} {fmt(cx + 3.6 * k)} {fmt(cy - 0.4 * k)}", 0.9 * k, LINE_S))


class _LS:
    cap = "round"
    join = "round"
    name = "rounded"
    r = 1.5
    R = 4


LINE_S = _LS()


@icon("froglet", CAT, "Young frog with a round head and body, two small back legs sprouting and a shortened tail",
      tags=["metamorphosis", "baby frog", "tadpole stage", "growing legs", "amphibian", "pond", "development"])
def _(S):
    body = union(ellipse(9.4, 10.6, 6.2, 4.8),
                 limb([(12.6, 13.6), (14.8, 17.4), (18, 18.4)], 2.2, S), limb([(8.6, 14), (9, 18.6), (12, 19.8)], 2.2, S))
    return [shell(body), line("M15.2 10.4Q18.6 9.6 21 12.8"), mark(circle(6.2, 9.2, 0.9))]


@icon("frog-life-cycle", CAT, "Circle of four arrows running around a tadpole to show the stages of a frog's life",
      tags=["metamorphosis", "amphibian", "biology", "science class", "stages", "growth", "pond cycle"])
def _(S):
    R = 9
    out = []
    for a in (-45, 45, 135, 225):
        s0, e0 = a - 26, a + 26
        out.append(line(arc(12, 12, R, s0, e0)))
        px, py = pt_on(12, 12, R, e0)
        tx, ty = -math.sin(math.radians(e0)), math.cos(math.radians(e0))
        nx, ny = math.cos(math.radians(e0)), math.sin(math.radians(e0))
        out.append(line(poly([(px - 2.4 * tx + 2 * nx, py - 2.4 * ty + 2 * ny), (px, py),
                              (px - 2.4 * tx - 2 * nx, py - 2.4 * ty - 2 * ny)])))
    tad = union(circle(10.4, 11.6, 2.6), thick("M12.4 12Q14.4 14.6 16.4 11.4", 1.5, LINE_S))
    return out + [solid(tad)]


@icon("tree-frog", CAT, "Frog clinging upright to a stem, seen from the front, with big round sticky pads on every toe",
      tags=["climbing frog", "sticky toes", "toe pads", "rainforest", "green frog", "amphibian", "clinging"])
def _(S):
    body = union(ellipse(12, 14.4, 3.8, 5.2), ellipse(12, 9.4, 4.6, 2.6), circle(9, 7.8, 2), circle(15, 7.8, 2),
                 limb([(9.4, 11.6), (5.6, 11.6)], 1.8, S), limb([(14.6, 11.6), (18.4, 11.6)], 1.8, S),
                 limb([(9.4, 17), (6.4, 18), (5.4, 20.4)], 1.8, S), limb([(14.6, 17), (17.6, 18), (18.6, 20.4)], 1.8, S),
                 circle(4.4, 11.6, 1.9), circle(19.6, 11.6, 1.9), circle(4.8, 20.6, 1.9), circle(19.2, 20.6, 1.9))
    return [shell(body), mark(circle(9, 8, 0.8)), mark(circle(15, 8, 0.8)), line(seg(12, 2, 12, 5))]


@icon("horned-frog", CAT, "Very round wide frog seen from the front with a huge mouth and a small pointed horn above each eye",
      tags=["pacman frog", "argentine horned frog", "wide mouth", "round frog", "amphibian", "pet frog", "predator"])
def _(S):
    body = union(ellipse(12, 13.8, 10, 6.6), circle(6.6, 8.4, 2.6), circle(17.4, 8.4, 2.6),
                 poly([(4.2, 7.6), (4.6, 4.2), (7.4, 6.2)], closed=True), poly([(19.8, 7.6), (19.4, 4.2), (16.6, 6.2)], closed=True),
                 ellipse(4.8, 19.6, 2.6, 1.4), ellipse(19.2, 19.6, 2.6, 1.4))
    return [shell(body), mark(circle(6.6, 8.7, 0.9)), mark(circle(17.4, 8.7, 0.9)), detail("M4 13.4C8.6 17.6 15.4 17.6 20 13.4")]


@icon("glass-frog", CAT, "Top view of a flat frog outline with the heart and gut drawn visible inside the belly",
      tags=["transparent frog", "see through", "anatomy", "rainforest", "amphibian", "heart", "translucent"])
def _(S):
    fr = frog_top(S, hind=((9, 15.6), (5, 15.4), (5.4, 20), (8.6, 20.8)), front=((8.4, 10.6), (5.4, 11.6), (4.4, 9.6)), w=2.2)
    return [shell(fr), mark(circle(12, 9.6, 1.3)), mark(ellipse(12, 15, 1.7, 2.4))]


def fan(ax, ay, deg, length=5.6, spread=36):
    """Webbed foot fan: apex (ax, ay), opening towards angle deg, three toe tips joined by scalloped webbing."""
    tips = [pt_on(ax, ay, length, deg + o) for o in (-spread, 0, spread)]
    d = f"M{fmt(ax)} {fmt(ay)}L{fmt(tips[0][0])} {fmt(tips[0][1])}"
    for i in (1, 2):
        mx, my = (tips[i - 1][0] + tips[i][0]) / 2, (tips[i - 1][1] + tips[i][1]) / 2
        cx, cy = mx + (ax - mx) * 0.38, my + (ay - my) * 0.38
        d += f"Q{fmt(cx)} {fmt(cy)} {fmt(tips[i][0])} {fmt(tips[i][1])}"
    return d + "Z"


@icon("flying-frog", CAT, "Frog gliding with arms and legs spread wide and webbing stretched between them like a small parachute",
      tags=["gliding frog", "parachute frog", "wallace's frog", "rainforest", "glide", "amphibian", "webbed feet"])
def _(S):
    web = poly([(10, 9.6), (3, 7.2), (4, 20.6), (12, 17.2), (20, 20.6), (21, 7.2), (14, 9.6)], closed=True, r=L(S, 0, 1.2))
    web = ("M10 9.6L3 7.4Q8.6 12.8 4 20.6Q12 15.8 20 20.6Q15.4 12.8 21 7.4L14 9.6Z")
    head = union(ellipse(12, 7, 3.4, 3.2), circle(9.8, 4.8, 1.5), circle(14.2, 4.8, 1.5))
    return [shell(union(web, head)), mark(circle(9.8, 4.9, 0.7)), mark(circle(14.2, 4.9, 0.7)), detail("M12 10.4V15")]


@icon("frog-legs-dish", CAT, "Plate holding a pair of cooked frog legs crossed over each other beside a lemon wedge",
      tags=["cuisine", "french food", "delicacy", "restaurant", "cooked frog", "fried legs", "menu"])
def _(S):
    plate = circle(9.8, 10, 7.4)
    legA = union(rot(ellipse(7.2, 7.6, 2.8, 1.9), 45, 7.2, 7.6), limb([(8.8, 9.2), (12.8, 13.4)], 1.4, S),
                 fan(12.4, 13, 45, 3.4, 42))
    legB = path_to_d(transform_path(P(legA), (-1, 0, 0, 1, 19.6, 0)))
    wedge = poly([(14.2, 21), (21.4, 21), (17.8, 16.6)], closed=True, r=S.r)
    return [shell(plate), mark(union(legA, legB)), shell(wedge)]


@icon("frog-skeleton", CAT, "Top view of a frog skeleton with a wide flat skull, short spine and long folded hind leg bones",
      tags=["bones", "anatomy", "biology class", "dissection", "amphibian skeleton", "osteology", "science"])
def _(S):
    skull = ellipse(12, 5.4, 4.8, 2.9)
    return [shell(skull), mark(circle(9.6, 5, 0.8)), mark(circle(14.4, 5, 0.8)), line(seg(12, 8.6, 12, 15.4)),
            line(seg(10, 15.4, 14, 15.4)),
            line(poly([(12, 10.4), (8, 11.6), (6.4, 9.4)])), line(poly([(12, 10.4), (16, 11.6), (17.6, 9.4)])),
            line(poly([(10.4, 15.4), (5.6, 13.4), (4.6, 19.4), (8.6, 21)])), line(poly([(13.6, 15.4), (18.4, 13.4), (19.4, 19.4), (15.4, 21)]))]


@icon("three-legged-toad", CAT, "Squat toad sitting on a pile of coins with a coin held in its mouth, showing only three legs",
      tags=["money toad", "lucky toad", "fortune", "wealth", "feng shui", "good luck charm", "coins"])
def _(S):
    body = union(ellipse(12, 10.8, 7.8, 5.4), circle(7, 5.8, 2.3), circle(17, 5.8, 2.3),
                 rect(5.6, 13.6, 3.2, 4.8, 1.2), rect(15.2, 13.6, 3.2, 4.8, 1.2), ellipse(21, 16.2, 1.5, 2.6))
    coins = [shell(rect(3.5, 19.4, 17, 2.6, L(S, 1, 1.3)))]
    return [shell(body), mark(circle(7, 6, 0.9)), mark(circle(17, 6, 0.9)), detail("M6 11.4Q12 14.2 18 11.4"), mark(circle(12, 13.8, 1.6))] + coins


@icon("axolotl", CAT, "Top view of an axolotl with a wide smiling head, three feathery gill fronds on each side and a finned tail",
      tags=["mexican salamander", "walking fish", "gills", "pet", "amphibian", "cute", "aquarium"])
def _(S):
    tail = tube(((12, 9), (12, 13), (13, 17.5), (12, 22)), lambda t: 5.4 * (1 - t) + L(S, 0.4, 1.2))
    body = union(ellipse(12, 6.6, 4.8, 3.8), poly(tail, closed=True),
                 limb([(10, 11), (7.4, 12.2), (6.6, 14)], 1.8, S), limb([(14, 11), (16.6, 12.2), (17.4, 14)], 1.8, S),
                 limb([(10.4, 16.6), (7.8, 17.6), (7.4, 19.4)], 1.8, S), limb([(13.6, 16.6), (16.2, 17.6), (16.6, 19.4)], 1.8, S))
    gills = []
    for sgn in (1, -1):
        for (y0, y1) in ((5, 2.8), (6.6, 6.4), (8.2, 10)):
            x0, x1 = (7.6, 2.6) if sgn == 1 else (16.4, 21.4)
            gills.append(line(seg(x0, y0, x1, y1)))
    return [shell(body), mark(circle(10, 5.6, 0.8)), mark(circle(14, 5.6, 0.8)), detail("M9.8 8Q12 9.4 14.2 8")] + gills


@icon("salamander", CAT, "Top view of a smooth-skinned salamander with a rounded snout, splayed legs, a long tail and round spots along its back",
      tags=["amphibian", "newt", "spotted salamander", "forest", "moist skin", "lizard like", "pond"])
def _(S):
    tail = tube(((12, 8), (12, 13), (10.4, 17.5), (15.5, 22)), lambda t: 4.2 * (1 - t) + L(S, 0.3, 1.4))
    body = union(ellipse(12, 5.2, 2.8, 3), poly(tail, closed=True),
                 limb([(10.8, 9), (6.6, 8.6), (4.6, 11.4)], 1.8, S), limb([(13.2, 9), (17.4, 8.6), (19.4, 11.4)], 1.8, S),
                 limb([(10.8, 13.4), (6.6, 14.4), (5, 17.6)], 1.8, S), limb([(13.2, 13.4), (17.4, 14.4), (19, 17.6)], 1.8, S))
    return [shell(body), mark(circle(12, 8.8, 0.9)), mark(circle(12, 12.4, 0.9)), mark(circle(11.2, 15.8, 0.8))]


@icon("crested-newt", CAT, "Side view of a newt with a tall jagged crest running along its back",
      tags=["great crested newt", "triton", "amphibian", "pond", "wildlife survey", "protected species", "water newt"])
def _(S):
    body = union(poly(tube(((21, 13.4), (15, 12.6), (8, 14.6), (2.6, 12.4)), lambda t: 4.2 * (1 - t) + 1.2), closed=True),
                 limb([(17, 14.6), (17.6, 18.6)], 2.2, S), limb([(9, 15), (8.2, 18.8)], 2.2, S))
    crest = poly([(5, 12), (7, 6.4), (9, 11), (11, 6.4), (13, 10.6), (15, 7.4), (16.6, 11.6)], closed=True)
    return [shell(body), solid(crest), mark(circle(19.2, 12.4, 0.8))]


@icon("salamander-in-flames", CAT, "Small salamander curled in the middle of a tall flame with three rising tongues",
      tags=["fire salamander", "legend", "mythical", "fire element", "alchemy", "heat", "flame lizard"])
def _(S):
    flame = ("M12 21.5C6.4 21.5 3 17.8 3 13.6C3 10.8 4.4 8.6 6 6.4C6.8 8.6 7.8 9.4 8.8 9.6C8.6 6 10.2 3.8 12 2.4C13.4 5 14.6 6.2 15.6 8C16.4 7.2 17 6.4 17.4 5.4C19.6 8 21 10.6 21 13.8C21 18 17.8 21.5 12 21.5Z")
    sal = union(thick("M15 11.6Q9 10.6 8.6 15.4Q9 19 15.2 17.6", 2.0, S), circle(15.4, 11.4, 1.7), limb([(9.4, 12.2), (7.6, 11)], 1.2, S),
                limb([(9.2, 17.8), (7.6, 19)], 1.2, S))
    return [shell(flame), mark(sal)]
