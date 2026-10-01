"""TypeIcon Core: reptiles (snakes, lizards, turtles), batch 001."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "reptiles"


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


def thick(d, w, S):
    """Outline of a stroke of width w along d (snake bodies, limbs, necks)."""
    return path_to_d(ST(d, w, S.cap, S.join))


def mark(d):
    return Part("dot", d)


def pt_(cx, cy, r, deg):
    return (cx + r * math.cos(math.radians(deg)), cy + r * math.sin(math.radians(deg)))


def hd(cx, cy, rx, ry, deg):
    """Rotated ellipse used as a head."""
    return rot(ellipse(cx, cy, rx, ry), deg, cx, cy)


def tongue(x, y, deg, n=3.0, sp=1.1):
    """Forked tongue starting at (x, y) pointing along deg."""
    a = math.radians(deg)
    ex, ey = x + n * math.cos(a), y + n * math.sin(a)
    px, py = -math.sin(a), math.cos(a)
    t1 = (ex + n * 0.55 * math.cos(a) + sp * px, ey + n * 0.55 * math.sin(a) + sp * py)
    t2 = (ex + n * 0.55 * math.cos(a) - sp * px, ey + n * 0.55 * math.sin(a) - sp * py)
    return (f"M{fmt(x)} {fmt(y)}L{fmt(ex)} {fmt(ey)}M{fmt(ex)} {fmt(ey)}L{fmt(t1[0])} {fmt(t1[1])}"
            f"M{fmt(ex)} {fmt(ey)}L{fmt(t2[0])} {fmt(t2[1])}")


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def tube(ctrl, width, n=40):
    """Closed outline around a cubic centreline with width(t) in px."""
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
    return poly(left + right[::-1], closed=True)


def spikes(cx, cy, rx, ry, angles, ln=2.5, w=1.4):
    """Triangular spikes standing on an ellipse at the given angles (deg, 0 = right, 90 = down)."""
    out = []
    for a in angles:
        r = math.radians(a)
        tx, ty = -math.sin(r), math.cos(r)
        bx, by = cx + rx * math.cos(r), cy + ry * math.sin(r)
        nx, ny = math.cos(r) * ry, math.sin(r) * rx
        nn = math.hypot(nx, ny)
        nx, ny = nx / nn, ny / nn
        out.append(poly([(bx - tx * w - nx * 0.6, by - ty * w - ny * 0.6), (bx + nx * ln, by + ny * ln), (bx + tx * w - nx * 0.6, by + ty * w - ny * 0.6)], closed=True))
    return out


def interp(pts):
    def f(t):
        for (t0, w0), (t1, w1) in zip(pts, pts[1:]):
            if t <= t1:
                return w0 + (w1 - w0) * (t - t0) / (t1 - t0)
        return pts[-1][1]
    return f


def back_spikes(ctrl, ts, ln=2.4, w=1.2, side=-1):
    """Triangles standing on a centreline (offset 'half' not needed: they overlap the body) on the up side."""
    out = []
    for t in ts:
        x, y = bez(*ctrl, t)
        x2, y2 = bez(*ctrl, min(1, t + 1e-3))
        x1, y1 = bez(*ctrl, max(0, t - 1e-3))
        dx, dy = x2 - x1, y2 - y1
        n = math.hypot(dx, dy)
        dx, dy = dx / n, dy / n
        nx, ny = dy * side, -dx * side
        out.append(poly([(x - dx * w, y - dy * w), (x + nx * ln - dx * 0.3, y + ny * ln - dy * 0.3), (x + dx * w, y + dy * w)], closed=True))
    return out


def grow(d, g):
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def drop(x, y, s=1.0, r=0.0):
    """Teardrop pointing up, tip at (x, y - 1.6 s)."""
    return poly([(x, y - 1.8 * s), (x + 1.2 * s, y + 0.2 * s), (x, y + 1.3 * s), (x - 1.2 * s, y + 0.2 * s)], closed=True, r=r)


# --------------------------------------------------------------------------- snakes: species

@icon("cobra", CAT, "Cobra rearing up with its hood spread", tags=["snake", "serpent", "hood", "venomous", "reptile"])
def _(S):
    hood = "M9.4 6.6C4.5 8 3.5 13 8.5 15.2L15.5 15.2C20.5 13 19.5 8 14.6 6.6Z"
    head = ellipse(12, 5.4, 2.6, 2.9)
    body = thick("M12 14V17C12 19.5 14 20 16.5 20C19 20 20 21 18 21.2H6", 3, S)
    return [shell(union(hood, head, body)), detail("M12 9.5V13.5"), mark(circle(11, 5, 0.8)), mark(circle(13, 5, 0.8))]


@icon("spitting-cobra", CAT, "Cobra with hood spread spraying venom droplets", tags=["snake", "venom", "spit", "spray", "hood", "reptile"])
def _(S):
    hood = "M7.4 6.6C2.5 8 1.8 13 6.5 15.2L12.5 15.2C16.5 13 16.5 8 12.6 6.6Z"
    head = hd(10, 5.4, 3.2, 2.4, 15)
    body = thick("M9.5 14V17C9.5 19.5 11.5 20 14 20C16.5 20 17.5 21 15.5 21.2H4", 3, S)
    drops = [mark(circle(15.5, 4.2, 0.9)), mark(circle(18.5, 3, 0.9)), mark(circle(19, 6.5, 0.9)), mark(circle(21.3, 4.6, 0.8))]
    return [shell(union(hood, head, body)), detail("M9.5 9.5V13.5"), mark(circle(10.6, 4.7, 0.8))] + drops


@icon("rattlesnake", CAT, "Coiled rattlesnake with raised head and rattle", tags=["snake", "rattle", "venomous", "coiled", "desert", "reptile"])
def _(S):
    coil = union(rect(3, 16, 15, 5, 2.5), rect(5, 12, 11, 5, 2.5))
    neck = thick("M7 12.5V9C7 6.5 8.5 5.5 10 5.5", 3, S)
    head = hd(11, 5.3, 3.3, 2.2, -5)
    rattle = [circle(19.5, 15, 1.6), circle(19.5, 11.5, 1.6), circle(19.5, 8, 1.5)]
    return [shell(union(coil, neck, head)), detail(seg(5, 16.5, 16, 16.5)) if False else detail("M6 16.5H15"),
            mark(circle(11.6, 4.8, 0.8)), shell(union(*rattle[::-1], thick("M17 18.5H19.5V8", 2.6, S)))]


@icon("ball-python", CAT, "Python curled into a ball with its head on top", tags=["snake", "python", "coiled", "curled", "pet", "reptile"])
def _(S):
    ball = circle(12, 14, 7.5)
    head = hd(15.5, 6.2, 3.4, 2.3, 10)
    return [shell(union(ball, head)), detail(arc(12, 14, 3.6, 150, 440)), mark(circle(16.4, 5.7, 0.8))]


@icon("sea-snake", CAT, "Sea snake swimming with a paddle tail above waves", tags=["snake", "sea", "ocean", "swim", "water", "reptile"])
def _(S):
    body = thick("M5 11C7 6 10 6 12 10C14 14 17 14 18.5 10.5", 2.8, S)
    paddle = rot(ellipse(4, 11.5, 2.2, 3.2), -30, 4, 11.5)
    head = hd(20, 9.5, 2.6, 2, -30)
    return [shell(union(body, paddle, head)), mark(circle(20.6, 9, 0.7)), line("M3 17C5 15.5 7 18.5 9 17S13 15.5 15 17S19 18.5 21 17"),
            line("M3 21H21") if False else line("M4 21C6 20 8 22 10 21")]


@icon("coral-snake", CAT, "Slender banded snake in an S shape", tags=["snake", "banded", "venomous", "stripes", "bands", "reptile"])
def _(S):
    body = thick("M5 20C5 16 13 17 13 12.5C13 8.5 7 9 9 6", 4.4, S)
    head = hd(9.8, 4.4, 3.4, 2.6, -20)
    return [shell(union(body, head)), mark(circle(10.6, 3.9, 0.8)),
            detail("M3.8 17.2L7.6 17.7"), detail("M11.5 14.6L15.6 14.2"), detail("M7.2 8.4L11 9.4")]


@icon("black-mamba", CAT, "Tall slender snake rearing up with its mouth open wide", tags=["snake", "mamba", "venomous", "open mouth", "african", "reptile"])
def _(S):
    body = thick("M12 21C5 21 4 15 9 13C12.5 11.5 10.5 9.5 10.5 8", 2.8, S)
    head = poly([(8, 8.5), (8.5, 4.5), (12, 3), (20, 4.8), (13.2, 6.2), (20.5, 9.2), (15, 10.2), (11, 10)], closed=True, r=L(S, 0, 0.9))
    return [shell(union(body, head)), mark(circle(11.6, 5.4, 0.9))]


# --------------------------------------------------------------------------- snakes: shapes and behaviours

@icon("horned-viper", CAT, "Viper head in profile with two small horns above the eye", tags=["snake", "viper", "horns", "desert", "venomous", "reptile"])
def _(S):
    body = thick("M3.5 20.5H11C15 20.5 15.5 16 11.5 14.5", 3.2, S)
    head = poly([(5.5, 13.5), (7.5, 8.5), (13.5, 8), (21, 11.5), (15, 14.5), (9, 15)], closed=True, r=L(S, 0, 1.2))
    h1 = poly([(8.4, 9.5), (9, 4), (12, 8.5)], closed=True, r=L(S, 0, 0.6))
    h2 = poly([(12, 8.5), (14.6, 4.6), (15.6, 9.6)], closed=True, r=L(S, 0, 0.6))
    return [shell(union(body, head, h1, h2)), mark(circle(13.6, 11.2, 0.9))]


@icon("hognose-snake", CAT, "Snake head with an upturned snout above a short coil", tags=["snake", "hognose", "upturned", "snout", "harmless", "reptile"])
def _(S):
    body = thick("M3.5 20H14C18 20 19 16 15.5 14.5C13 13.5 9.5 13.5 8.5 12", 3.2, S)
    head = poly([(6, 9), (9, 6.5), (13.5, 6.5), (17, 4.2), (19.5, 2.5), (20.5, 4.5), (18.2, 8.8), (13.5, 11.5), (8, 12.5)], closed=True, r=L(S, 0, 1))
    return [shell(union(body, head)), mark(circle(12.2, 8.4, 0.9))]


@icon("vine-snake", CAT, "Very thin snake with a pointed head stretched along a vine", tags=["snake", "vine", "slender", "green", "thin", "reptile"])
def _(S):
    leaf1 = poly([(6, 18.5), (3, 14.5), (7.5, 14.5)], closed=True, r=L(S, 0, 0.8))
    head = poly([(15.5, 6.8), (19, 3.6), (22, 3), (21.2, 5.4), (18, 7.8)], closed=True, r=L(S, 0, 0.8))
    return [line("M4 20.5C6 12 12 17 14 11C15 8 15.5 7.5 17 6.5"), shell(head), mark(circle(19.4, 4.6, 0.6)),
            line("M10 17.5C11.5 19 14 20 17 19.6")]


@icon("garter-snake", CAT, "Striped snake stretched in an S shape", tags=["snake", "striped", "garden", "harmless", "stripes", "reptile"])
def _(S):
    c = "M3.5 18.5C10 18.5 9 12.5 12 12C15 11.5 14.5 6 20 5.5"
    body = thick(c, 5.4, S)
    head = hd(19.8, 5.4, 3, 2.6, -5)
    return [shell(union(body, head)), detail(c), mark(circle(20.2, 4.8, 0.8))]


@icon("sidewinder", CAT, "Sidewinder snake lifting its looped body with hooked tracks beside it", tags=["snake", "desert", "sand", "viper", "tracks", "reptile"])
def _(S):
    body = thick("M9 8.5C12.5 7.5 15 9 15 12C15 15.5 12 18.5 16.5 19.5", 3, S)
    head = hd(7.2, 7.8, 3.3, 2.3, 20)
    return [shell(union(body, head)), mark(circle(6.6, 7.2, 0.8)),
            line("M3.5 21.5L6.5 17.5"), line("M3.5 15.5L6.2 11.8") if False else line("M2.5 15L5 11.5"),
            line("M19.5 17.5L22 13.5")]


@icon("flying-snake", CAT, "Snake gliding in a flat S shape between two tree trunks", tags=["snake", "glide", "gliding", "jungle", "tree", "reptile"])
def _(S):
    body = thick("M6 18C8.5 10 12 17.5 14.5 11C15.5 8.5 16 8 16.5 8", 3, S)
    head = hd(18, 7.6, 2.8, 2.3, -10)
    return [line("M2.5 3V21"), line("M21.5 3V21"), shell(union(body, head)), mark(circle(18.4, 7, 0.7))]


@icon("two-headed-snake", CAT, "Snake body splitting into two heads with forked tongues", tags=["snake", "two heads", "mutation", "double", "rare", "reptile"])
def _(S):
    body = thick("M3.5 20H11C15.5 20 16 14.5 12 13.5C12 12.5 12 12 12 11.5", 3, S)
    neck1 = thick("M12 13C11 10 8.5 9.5 8.2 7", 2.6, S)
    neck2 = thick("M12 13C13 10 15.5 9.5 15.8 7", 2.6, S)
    h1 = hd(8, 5.6, 2.5, 3, 0)
    h2 = hd(16, 5.6, 2.5, 3, 0)
    return [shell(union(body, neck1, neck2, h1, h2)), mark(circle(7.2, 5.3, 0.7)), mark(circle(8.8, 5.3, 0.7)), mark(circle(15.2, 5.3, 0.7)), mark(circle(16.8, 5.3, 0.7)),
            line("M8 8.6V10") if False else line("M5.8 1.6L7 3")] if False else [shell(union(body, neck1, neck2, h1, h2)), mark(circle(7.3, 5.3, 0.7)), mark(circle(8.9, 5.3, 0.7)), mark(circle(15.1, 5.3, 0.7)), mark(circle(16.7, 5.3, 0.7))]


@icon("snake-head", CAT, "Front view of a snake head with a forked tongue", tags=["snake", "face", "serpent", "tongue", "reptile"])
def _(S):
    head = poly([(12, 2.5), (19.5, 9), (15.5, 17), (8.5, 17), (4.5, 9)], closed=True, r=L(S, 0, 3))
    return [shell(head), dot(9, 9, 1.1), dot(15, 9, 1.1), dot(10.8, 13.2, 0.7), dot(13.2, 13.2, 0.7), line("M12 17.5V20.5M12 20.5L10.5 22.5M12 20.5L13.5 22.5")]


@icon("snake-coiled", CAT, "Snake coiled in a stacked spiral with its head on top", tags=["snake", "coil", "coiled", "rope", "spiral", "reptile"])
def _(S):
    rr = L(S, 1.2, 2.25)
    stack = union(rect(3, 16.5, 18, 4.5, rr), rect(5, 12, 14, 5, rr), rect(7, 8, 10, 5, rr))
    head = hd(14.5, 5.5, 3.4, 2.4, 10)
    return [shell(union(stack, head)), detail("M5 16.7H19"), detail("M7 12.3H17"), mark(circle(15.4, 5, 0.8))]


@icon("snake-striking", CAT, "Snake lunging forward with open jaws and bared fangs", tags=["snake", "strike", "attack", "bite", "fangs", "danger"])
def _(S):
    body = thick("M3.5 19.5C9 19.5 8.5 12.5 12.5 12.5", 3, S)
    head = poly([(10, 13), (10.5, 7), (14, 4.5), (21.5, 5.5), (14.5, 10.2), (21, 15.5), (14.5, 16), (11.5, 15)], closed=True, r=L(S, 0, 0.9))
    fangs = [solid(poly([(16.2, 6.6), (18.4, 6.2), (17.6, 10.6)], closed=True)), solid(poly([(17, 14.6), (19, 14.8), (18.2, 11.4)], closed=True))]
    return [shell(union(body, head)), mark(circle(13, 8, 0.9))] + fangs


@icon("water-snake", CAT, "Snake head and neck gliding across a wavy water line", tags=["snake", "water", "swim", "swimming", "river", "reptile"])
def _(S):
    neck = thick("M5.5 17C5.5 11 11 14 12.5 9", 2.8, S)
    head = hd(14.5, 7.6, 3.2, 2.3, -15)
    return [shell(union(neck, head)), mark(circle(15.2, 6.9, 0.8)), line("M2 18C4 16.5 6 19.5 8 18S12 16.5 14 18S18 19.5 20 18"),
            line("M5 21.5C7 20.5 9 22.5 11 21.5S15 20.5 17 21.5")]


@icon("snake-hatchling", CAT, "Cracked egg with a small snake head poking out of the top", tags=["snake", "egg", "hatch", "baby", "newborn", "reptile"])
def _(S):
    shell_d = "M5.5 12.5L8.5 15.5L11.2 12.5L13.8 15.5L16.5 12.5L18.5 15C19.2 19.5 16.5 21.5 12 21.5C7.5 21.5 4.8 19.5 5.5 12.5Z"
    head = ellipse(12, 8.5, 3.4, 4.6)
    return [shell(union(shell_d, head)), mark(circle(10.6, 7.4, 0.8)), mark(circle(13.4, 7.4, 0.8))]

@icon("snake-fangs", CAT, "Open snake mouth showing two long fangs with venom drops", tags=["snake", "fangs", "venom", "bite", "poison", "mouth"])
def _(S):
    jaw = rect(3, 3.5, 18, 5, L(S, 1.5, 2.5))
    return [shell(jaw), line("M7.5 8.5C7.5 12 8.5 14.5 10 16.5"), line("M16.5 8.5C16.5 12 15.5 14.5 14 16.5"),
            solid(drop(10.2, 19.6, 0.9)), solid(drop(13.8, 19.6, 0.9))]

@icon("forked-tongue", CAT, "Snake snout with a long forked tongue", tags=["snake", "tongue", "forked", "flick", "smell", "reptile"])
def _(S):
    snout = rect(2.5, 7.5, 7, 9, L(S, 2, 3.5))
    return [shell(snout), dot(5.6, 10.2, 0.8), line("M9.5 12H14.5C16.5 12 17.5 10 20.5 8"), line("M14.5 12C16.5 12 17.5 14 20.5 16")]


@icon("snake-rattle", CAT, "Stack of interlocking rattlesnake rattle segments with motion lines", tags=["rattle", "rattlesnake", "tail", "warning", "shake", "snake"])
def _(S):
    rr = L(S, 1.2, 2)
    segs = union(rect(6.5, 16, 11, 5, rr), rect(7.5, 11.5, 9, 5, rr), rect(8.5, 7, 7, 5, rr), rect(9.5, 3, 5, 4.5, rr))
    return [shell(segs), detail("M7.5 16.2H16.5"), detail("M8.5 11.7H15.5"), detail("M9.5 7.2H14.5"),
            line("M4 5L3 8") if False else line("M5.5 5.5L3.5 7.5"), line("M18.5 5.5L20.5 7.5")]


@icon("snake-skull", CAT, "Side view of a snake skull with a row of curved teeth", tags=["snake", "skull", "bones", "fossil", "skeleton", "reptile"])
def _(S):
    skull = poly([(3, 13), (5.5, 8.5), (12, 6.5), (18, 7.5), (21, 11), (20, 14), (12, 13.5)], closed=True, r=L(S, 0, 1.5))
    teeth = [solid(poly([(x, 13.2), (x + 1.8, 13.2), (x + 0.2, 16.2)], closed=True)) for x in (6.5, 10, 13.5)]
    return [shell(skull), mark(circle(15.2, 10, 1.3)), line("M4.5 18.5H15C16.5 18.5 18 17.5 19 15.5")] + teeth


@icon("antivenom", CAT, "Medicine vial with a stopper and a small snake on its label", tags=["antivenom", "antidote", "vial", "medicine", "snake", "treatment"])
def _(S):
    vial = union(rect(9, 5.5, 6, 4, 0.8), rect(6, 9, 12, 12.5, L(S, 2, 3)))
    cap = rect(8, 2.2, 8, 3.3, L(S, 0.6, 1.3))
    return [shell(vial), shell(cap), detail("M9 18.5C10.5 18.5 10.5 15.5 12 15.5C13.5 15.5 13.5 12.5 15 12.5") if False else detail("M8.5 18C10 18 10 15 12 15C14 15 14 12.5 15.5 12.5")]


@icon("snake-in-grass", CAT, "Tall grass blades with a snake head peeking between them", tags=["snake", "grass", "hidden", "lurking", "garden", "danger"])
def _(S):
    left = poly([(2, 21.5), (3.2, 12), (5.4, 18), (7.2, 9.5), (9.2, 21.5)], closed=True, r=L(S, 0, 0.5))
    right = poly([(14.8, 21.5), (16.8, 10), (18.6, 17.5), (20.4, 12), (22, 21.5)], closed=True, r=L(S, 0, 0.5))
    neck = thick("M12 21.5V13", 2.8, S)
    head = hd(12.8, 11, 3.2, 2.4, -8)
    return [shell(union(left, right, neck, head)), mark(circle(13.8, 10.4, 0.8))]


@icon("snake-tracks", CAT, "Smooth wavy snake trail across flat ground", tags=["snake", "tracks", "trail", "sand", "path", "slither"])
def _(S):
    return [line("M2.5 11C5.5 4.5 8.5 4.5 11 11C13.5 17.5 16.5 17.5 21.5 10"), line("M3 21.5H21"), dot(5, 17, 0.9), dot(17.5, 5, 0.9), dot(21, 15, 0.9)]

@icon("snake-warning-sign", CAT, "Warning triangle with a coiled snake inside", tags=["snake", "warning", "danger", "caution", "hazard", "sign"])
def _(S):
    tri = poly([(12, 3), (21.8, 20), (2.2, 20)], closed=True, r=L(S, 0.8, 2.5))
    return [shell(tri), detail("M9.2 17.8H14.4C15.8 17.8 15.8 15 14.4 15H10.8C9.8 15 9.8 12.6 10.8 12.6"), dot(12.3, 12, 0.9)]


@icon("snake-hook", CAT, "Long handle ending in a J hook with a small snake hanging from it", tags=["snake", "hook", "handler", "tool", "catch", "pole"])
def _(S):
    snake = thick("M18 7.5C15.5 11.5 21 13 19 17.5", 2.4, S)
    head = hd(19, 19.2, 1.9, 2.4, 0)
    return [line("M7 21.5V9C7 5 10 3 13 3C16 3 18 5 18 7.5"), shell(union(snake, head)), mark(circle(19.7, 19.3, 0.55))]


@icon("snake-tongs", CAT, "Long reacher tongs with a pistol grip and two padded jaws", tags=["tongs", "snake", "grabber", "handler", "reacher", "tool"])
def _(S):
    shaft = rot(rect(11, 5, 2, 12, 0), 45, 12, 12)
    jaw1 = rot(poly([(11, 6), (8, 1.8), (10.2, 1.2), (12, 5)], closed=True, r=L(S, 0, 0.5)), 45, 12, 12)
    jaw2 = rot(poly([(13, 6), (16, 1.8), (13.8, 1.2), (12, 5)], closed=True, r=L(S, 0, 0.5)), 45, 12, 12)
    grip = rot(poly([(9.5, 15.5), (14.5, 15.5), (15, 21.5), (10.5, 21.5)], closed=True, r=L(S, 0, 1.2)), 45, 12, 12)
    return [shell(union(shaft, jaw1, jaw2, grip))]


@icon("snake-oil", CAT, "Old-fashioned corked bottle with a label and a small snake around its neck", tags=["snake oil", "bottle", "tonic", "remedy", "fraud", "cork"])
def _(S):
    bottle = union(rect(10, 5.5, 4, 5, 0.6), rect(6.5, 10, 11, 11.5, L(S, 2, 3)))
    cork = rect(10.4, 2.2, 3.2, 3.3, L(S, 0.5, 1.2))
    band = thick("M7.5 8.2C10 9.8 13.5 6.6 17 8.4", 2.2, S)
    return [shell(union(bottle, band)), shell(cork), detail(rect(8.7, 13.5, 6.6, 5, 1)), dot(12, 16, 0.9)]


@icon("rod-of-asclepius", CAT, "Vertical staff with a single snake winding around it", tags=["asclepius", "medicine", "healthcare", "staff", "snake", "doctor"])
def _(S):
    staff = rect(11, 2, 2, 20, L(S, 0, 1))
    body = thick("M12 20.5C6 20 6 16 12 15.5C18 15 18 11 12 10.5C8.5 10.2 8.3 8 9.6 6.7", 2.4, S)
    head = hd(10.5, 5, 2.4, 2, -30)
    return [shell(union(staff, body, head)), mark(circle(10.6, 4.7, 0.55))]


# --------------------------------------------------------------------------- chameleons and geckos

def _cham(S, dx=0.0, tail_curl=True):
    """Chameleon in side view on a branch, facing right. Returns (body d, extra parts)."""
    body = ellipse(11 + dx, 11.5, 6.2, 4.6)
    head = poly([(14.5 + dx, 8.2), (16 + dx, 3.6), (19.5 + dx, 5.8), (21.5 + dx, 10.5), (19.8 + dx, 13), (14.5 + dx, 14.2)], closed=True, r=L(S, 0, 1.2))
    tail = thick(f"M{5.4 + dx} 11.5C{2.5 + dx} 11.5 {2.2 + dx} 16.5 {5 + dx} 16.3C{6.8 + dx} 16.2 {6.6 + dx} 13.8 {5.2 + dx} 14", 2.2, S)
    legs = thick(f"M{9 + dx} 15V18.5M{14 + dx} 15V18.5", 2.4, S)
    return union(body, head, tail, legs) if tail_curl else union(body, head, legs)


@icon("chameleon", CAT, "Chameleon on a branch with a crested head and a curled tail", tags=["lizard", "reptile", "camouflage", "branch", "color", "tropical"])
def _(S):
    return [shell(_cham(S)), line("M2 20H22"), mark(circle(17.6, 8.6, 1.1)) if False else dot(17.6, 8.8, 1.1)]


@icon("three-horned-chameleon", CAT, "Chameleon head in profile with three long horns on its snout and brow", tags=["chameleon", "horns", "jackson", "lizard", "reptile", "head"])
def _(S):
    head = poly([(2.5, 10), (7, 5.5), (13, 5.5), (15.5, 11), (13.5, 15.5), (7, 16.5), (3, 14)], closed=True, r=L(S, 0, 2))
    horns = [poly([(12.5, 7), (21.5, 4), (14.5, 9.5)], closed=True, r=L(S, 0, 0.5)),
             poly([(14.5, 9.5), (22, 8.2), (15.3, 12)], closed=True, r=L(S, 0, 0.5)),
             poly([(15.2, 12), (21.5, 12.5), (14.4, 14.6)], closed=True, r=L(S, 0, 0.5))]
    return [shell(union(head, *horns)), detail(circle(8.6, 10.2, 2.2)), dot(8.8, 10.2, 0.9), line("M2 20H14")]


@icon("chameleon-tongue", CAT, "Chameleon on a branch shooting its long club-tipped tongue", tags=["chameleon", "tongue", "hunting", "catch", "lizard", "reptile"])
def _(S):
    return [shell(_cham(S, -3, False)), line("M2 20H17"), dot(14.6, 8.8, 1.1), line("M18.2 10.2H19.5"), shell(circle(21, 10.2, 1.3))]


@icon("leopard-gecko", CAT, "Spotted gecko in side view with a thick tapering tail", tags=["gecko", "lizard", "spots", "pet", "reptile", "desert"])
def _(S):
    ctrl = ((2.5, 15), (8, 17), (13, 8), (18.5, 11.5))
    body = tube(ctrl, lambda t: 0.4 + 6.5 * math.sin(min(1, t * 1.15) * math.pi * 0.62) ** 0.8 if t < 0.85 else 4.6)
    head = hd(19, 11.5, 3.4, 2.6, 0)
    legs = thick("M7.5 15.8L6.8 19.5M14.8 12.5L15.6 17", 2.4, S)
    return [shell(union(body, head, legs)), dot(19.8, 10.8, 0.8), dot(8, 14.3, 0.8), dot(12, 12.3, 0.8), dot(5.8, 15.6, 0.7), dot(15, 10.6, 0.7)]


@icon("crested-gecko", CAT, "Gecko in profile with a row of fringed crest spikes along its back", tags=["gecko", "crest", "lizard", "pet", "reptile", "eyelash"])
def _(S):
    body = thick("M3 17C8 18 10 15 13 14.5C15 14.2 17 14 18 13", 4.6, S)
    head = hd(18.5, 12.5, 4.2, 3, -10)
    crest = [poly([(x, y + 1.4), (x - 0.3, y - 1.6), (x + 1.6, y + 1.2)], closed=True) for x, y in [(15.8, 8.8), (12.8, 11.6), (9.8, 13.4), (6.8, 15)]]
    legs = thick("M9 17L8 20.5M15.5 15.5L16.5 19.5", 2.2, S)
    return [shell(union(body, head, legs, *crest)), dot(19.2, 11.5, 0.9)]


@icon("leaf-tailed-gecko", CAT, "Gecko clinging to a branch with a flat tail shaped like a leaf", tags=["gecko", "leaf", "camouflage", "madagascar", "lizard", "reptile"])
def _(S):
    leaf = poly([(2.5, 20.5), (3, 11.5), (10, 8), (8.5, 15.5)], closed=True, r=L(S, 0, 0.8)) if False else "M2.5 20.5C2.5 12 6 8 12 8C11 14 8 19 2.5 20.5Z"
    body = thick("M10 12.5C13 13.5 15 13 17 12", 4.2, S)
    head = hd(18.8, 11.5, 3.2, 2.6, -10)
    legs = thick("M13 14L12.5 19M16.5 13.5L17.5 18", 2.2, S)
    return [shell(union(leaf, body, head, legs)), detail("M4.5 18.2C6.5 15 8.5 12.5 10 11"), dot(19.6, 10.8, 0.8), line("M2 21.5H22")]


@icon("gecko-foot", CAT, "Splayed lizard foot with five toes ending in round sticky pads", tags=["gecko", "foot", "toe pads", "sticky", "grip", "climbing"])
def _(S):
    palm = ellipse(12, 17, 4.6, 3.8)
    toes = []
    pads = []
    for a, ln in [(-160, 9), (-125, 11), (-90, 11.5), (-55, 11), (-20, 9)]:
        r = math.radians(a)
        x0, y0 = 12 + 3.5 * math.cos(r), 17 + 2.8 * math.sin(r)
        x1, y1 = 12 + ln * math.cos(r), 17 + ln * math.sin(r)
        toes.append(thick(seg(x0, y0, x1, y1), 2, S))
        pads.append(circle(x1, y1, 1.9))
    return [shell(union(palm, *toes, *pads))]


# --------------------------------------------------------------------------- lizards

def _liz(S, by=11.0, rx=5.5, ry=3.2, head_w=3.6, tail_w=3.4, tail_to=(2.4, 15.5), legs=True, head=None):
    """Lizard in side view facing right: returns (shell d, leg line parts)."""
    body = ellipse(13.5, by, rx - 0.5, ry)
    hdp = head or poly([(15.5, by - 2.6), (21.5, by - 1.2), (21.8, by + 0.6), (16, by + 2.8)], closed=True, r=L(S, 0, 1))
    tail = tube(((9, by), (5.5, by + 0.2), (3.8, by + 2), tail_to), interp([(0, tail_w), (1, 0.4)]))
    parts = [union(body, hdp, tail)]
    lg = []
    if legs:
        lg = [line(f"M16.2 {by + ry - 0.5}L17.8 {by + ry + 3}H20.2"), line(f"M11.5 {by + ry - 0.5}L10 {by + ry + 3}H7.8")]
    return parts[0], lg


@icon("bearded-dragon", CAT, "Stout lizard in side view with a spiky beard under its jaw and spines along its back", tags=["lizard", "dragon", "beard", "pet", "reptile", "australian"])
def _(S):
    d, lg = _liz(S, 10.5, 5.8, 3.6, tail_to=(2.6, 15.5))
    beard = [poly([(16.3, 12), (17.2, 15.3), (18.6, 12.6)], closed=True), poly([(18.6, 12.6), (19.9, 15.3), (21, 11.8)], closed=True)]
    spines = [poly([(x, 7.8), (x + 0.9, 5.2), (x + 2, 7.6)], closed=True) for x in (8.5, 11.5, 14.5)]
    return [shell(union(d, *beard, *spines))] + lg + [dot(19.2, 9.6, 0.8)]


@icon("komodo-dragon", CAT, "Large heavy monitor lizard walking low with a forked tongue out", tags=["lizard", "monitor", "dragon", "komodo", "reptile", "giant"])
def _(S):
    head = poly([(16, 8.2), (20.5, 8.6), (21, 11.2), (16, 13.2)], closed=True, r=L(S, 0, 1))
    d, lg = _liz(S, 11.5, 6.4, 3.4, tail_w=3.8, tail_to=(2.5, 17), head=head)
    return [shell(d)] + lg + [dot(19, 9.8, 0.8), line("M21 10.4H22.3M22.3 10.4L23 9.4M22.3 10.4L23 11.4")]


@icon("thorny-devil", CAT, "Spiky desert lizard in side view covered in cone-shaped thorns", tags=["lizard", "thorny", "spikes", "desert", "australia", "reptile"])
def _(S):
    d, lg = _liz(S, 12, 5.6, 3.4, tail_to=(2.6, 18))
    th = spikes(12.5, 12, 5.6, 3.4, [205, 240, 275, 310], 3.2, 1.4) + [poly([(17, 8), (19, 4.5), (20.2, 8.6)], closed=True)]
    return [shell(union(d, *th))] + lg + [dot(19.3, 10.8, 0.8)]


@icon("basilisk-lizard", CAT, "Lizard running upright on its hind legs across the water with a crest on its head and back", tags=["lizard", "basilisk", "water", "running", "jesus lizard", "reptile"])
def _(S):
    body = rot(ellipse(12.5, 11, 5, 2.8), -25, 12.5, 11)
    head = poly([(15.5, 8.6), (20.5, 6.6), (21, 8.2), (16.8, 10.8)], closed=True, r=L(S, 0, 1))
    tail = tube(((8.5, 12.8), (5.5, 14), (4, 12), (2.5, 14.5)), interp([(0, 3), (1, 0.4)]))
    crest = poly([(10, 8.2), (12, 5.8), (14, 6.2), (16.5, 2.8), (17.5, 7.4)], closed=True, r=L(S, 0, 0.5))
    return [shell(union(body, head, tail, crest)), line("M11 13.5L13 17L16.5 17"), line("M9.5 13.8L8.5 17.5L5.5 17.5"), dot(18.8, 7.6, 0.7), line("M2.5 21H21.5")]


@icon("gila-monster", CAT, "Chunky lizard with a fat tail and a banded, beaded body pattern", tags=["gila", "lizard", "venomous", "desert", "beaded", "reptile"])
def _(S):
    body = ellipse(13, 11, 5.8, 3.6)
    head = poly([(16, 8), (21.6, 9.4), (21.8, 11.6), (16.5, 14)], closed=True, r=L(S, 0, 1.2))
    tail = tube(((8, 11), (5, 11.5), (3.5, 12.5), (2.6, 15)), interp([(0, 5.2), (0.8, 3.4), (1, 1.6)]))
    return [shell(union(body, head, tail)), detail("M10.5 8.2L10.5 13.8"), detail("M14.5 7.6L14.5 14.4"), detail("M5.2 9.6L5.2 13.6") if False else dot(4.8, 11.4, 0.7),
            line("M15.5 14L17.3 17.5H20"), line("M10 14L8.3 17.5H5.5"), dot(19.2, 9.6, 0.8)]


@icon("flying-lizard", CAT, "Lizard seen from above gliding with a wide wing membrane on each side", tags=["lizard", "draco", "glide", "gliding", "wings", "reptile"])
def _(S):
    wl = "M10.2 8C6 6.2 3 7.5 2.5 11.5C2.5 14.5 4.5 16 6.5 16.8L10.2 15.5Z"
    wr = flip(wl)
    body = tube(((12, 4), (12, 9), (12, 15), (12, 21.5)), interp([(0, 3.2), (0.25, 3.2), (0.5, 3.4), (1, 0.5)]))
    return [shell(union(wl, wr, body)), detail("M10 9.5L5 11"), detail("M10 13L6.5 14.5"), detail("M14 9.5L19 11"), detail("M14 13L17.5 14.5"), dot(11, 5.4, 0.6), dot(13, 5.4, 0.6)]


@icon("tuatara", CAT, "Sturdy reptile in side view with tall spines down its neck and back and a large eye", tags=["tuatara", "spines", "reptile", "new zealand", "crest", "lizard"])
def _(S):
    d, lg = _liz(S, 11.5, 5.8, 3.3, tail_to=(2.6, 17))
    spines = [poly([(x, 8.6), (x + 1.1, 4.6), (x + 2.3, 8.4)], closed=True) for x in (7.5, 10.2, 12.9, 15.6)]
    return [shell(union(d, *spines))] + lg + [dot(19, 10.4, 1.1)]


# --------------------------------------------------------------------------- turtles

def _dome(x0, x1, base, top):
    mid = (x0 + x1) / 2
    k = (x1 - x0) * 0.28
    return f"M{fmt(x0)} {fmt(base)}C{fmt(x0)} {fmt(top + 2)} {fmt(mid - k)} {fmt(top)} {fmt(mid)} {fmt(top)}C{fmt(mid + k)} {fmt(top)} {fmt(x1)} {fmt(top + 2)} {fmt(x1)} {fmt(base)}Z"


@icon("sea-turtle", CAT, "Top view of a sea turtle with long paddle flippers and a plated teardrop shell", tags=["turtle", "ocean", "swimming", "marine", "flippers", "reptile"])
def _(S):
    r = L(S, 0, 0.6)
    fl = poly([(8.2, 9.5), (2.5, 5.5), (3.2, 9), (7.6, 12.8)], closed=True, r=r)
    rl = poly([(9, 17.5), (5.2, 20.5), (8, 20.8), (10.6, 19.4)], closed=True, r=r)
    body = ellipse(12, 13.2, 5, 6.5)
    head = ellipse(12, 5.2, 2, 2.4)
    return [shell(union(body, head, fl, flip(fl), rl, flip(rl))), detail(poly(regular(12, 13, 2.4, 6), closed=True, r=L(S, 0, 0.6)))]


@icon("leatherback-turtle", CAT, "Top view of a large sea turtle with a tapered ridged shell and long flippers", tags=["turtle", "leatherback", "sea", "ridges", "marine", "reptile"])
def _(S):
    r = L(S, 0, 0.6)
    fl = poly([(8.4, 10), (2.6, 7.6), (3.4, 10.4), (7.8, 12.8)], closed=True, r=r)
    rl = poly([(9.4, 18), (6.4, 20.6), (8.6, 21), (10.6, 19.6)], closed=True, r=r)
    body = "M12 6.5C17 6.5 18.5 11 16.5 15L12 21.4L7.5 15C5.5 11 7 6.5 12 6.5Z"
    head = ellipse(12, 4.7, 1.9, 2.2)
    rid = "M10 10.5C10 12.5 10.6 14.2 11.3 15.8"
    return [shell(union(body, head, fl, flip(fl), rl, flip(rl))), detail(rid), detail(flip(rid))]

@icon("snapping-turtle", CAT, "Side view of a snapping turtle with a hooked beak, ridged shell and sawtooth tail", tags=["turtle", "snapper", "beak", "bite", "swamp", "reptile"])
def _(S):
    dome = "M5 15C5 9.5 8.5 7.5 12 7.5C15.5 7.5 18 9.5 18 15Z"
    tail = poly([(5.5, 13.5), (2.8, 13.8), (4, 15), (3, 16.5), (5.2, 15.8)], closed=True)
    head = poly([(16.5, 9), (20.5, 8.5), (22, 11.5), (20.4, 11.2), (21.2, 13.6), (17.5, 13)], closed=True, r=L(S, 0, 0.6))
    legs = [rect(6.5, 14, 3, 5.5, L(S, 0.5, 1.4)), rect(13.5, 14, 3, 5.5, L(S, 0.5, 1.4))]
    return [shell(union(dome, tail, head, *legs)), detail("M10 8V13.5"), detail("M14.3 9V13.5"), dot(19.2, 10.2, 0.7)]


@icon("softshell-turtle", CAT, "Top view of a flat round turtle with a smooth shell, long neck and pointed snout", tags=["turtle", "softshell", "flat", "pancake", "river", "reptile"])
def _(S):
    r = L(S, 0, 0.6)
    body = ellipse(12, 15, 7.3, 5.8)
    neck = thick("M12 10V6", 2.4, S)
    head = ellipse(12, 5.2, 2, 2.6)
    legs = [rot(ellipse(3.8, 12.5, 2.2, 1.3), 25, 3.8, 12.5), rot(ellipse(20.2, 12.5, 2.2, 1.3), -25, 20.2, 12.5),
            rot(ellipse(4.5, 19, 2.2, 1.3), -25, 4.5, 19), rot(ellipse(19.5, 19, 2.2, 1.3), 25, 19.5, 19)]
    return [shell(union(body, neck, head, *legs))]


@icon("star-tortoise", CAT, "Side view of a high domed tortoise with a star pattern on its shell", tags=["tortoise", "star", "dome", "shell", "land", "reptile"])
def _(S):
    dome = _dome(2.8, 18.2, 17, 4.8)
    head = ellipse(20, 14.5, 2.1, 1.9)
    legs = [rect(4.5, 16, 3.6, 4.5, L(S, 0.5, 1.5)), rect(12.5, 16, 3.6, 4.5, L(S, 0.5, 1.5))]
    return [shell(union(dome, head, *legs)), detail("M10.5 8.5V12.5M10.5 12.5L7.2 14.5M10.5 12.5L13.8 14.5"), dot(20.4, 14, 0.7)]


@icon("snake-necked-turtle", CAT, "Side view of a turtle with a very long S-curved neck", tags=["turtle", "long neck", "snake-necked", "freshwater", "australia", "reptile"])
def _(S):
    dome = "M2.8 18C2.8 12.5 6 10.5 10 10.5C14 10.5 16.5 13 16.5 18Z"
    neck = thick("M15.5 14.5C20.5 14.5 21 9.5 18 8C17 7.5 16 7 14.5 7.4", 2.4, S)
    head = hd(13.5, 7.5, 2.1, 1.5, 10)
    legs = [rect(4.5, 17, 3, 3.8, L(S, 0.5, 1.4)), rect(11, 17, 3, 3.8, L(S, 0.5, 1.4))]
    return [shell(union(dome, neck, head, *legs)), detail("M9.5 11V16.5"), dot(12.6, 7.2, 0.6)]


@icon("turtle-shell", CAT, "Top view of an empty turtle shell with a ring of hexagonal plates", tags=["turtle", "shell", "carapace", "scutes", "armor", "reptile"])
def _(S):
    off = [(0, -9.6), (7.5, -6), (7.5, 5), (0, 9.6), (-7.5, 5), (-7.5, -6)]
    outer = poly([(12 + x, 12 + y) for x, y in off], closed=True, r=L(S, 0, 3))
    inner = poly([(12 + x * 0.48, 12 + y * 0.48) for x, y in off], closed=True, r=L(S, 0, 1.2))
    sp = [detail(seg(12 + x * 0.48, 12 + y * 0.48, 12 + x * 0.92, 12 + y * 0.92)) for x, y in off]
    return [shell(outer), detail(inner)] + sp


@icon("turtle-hiding", CAT, "Domed turtle shell with head and legs pulled inside and only dark openings showing", tags=["turtle", "hiding", "shy", "retreat", "withdrawn", "shell"])
def _(S):
    dome = _dome(2.5, 21.5, 18, 4.5)
    arch_l = "M4.5 18V16.5C4.5 15 5.5 14 7 14C8.5 14 9.5 15 9.5 16.5V18Z"
    arch_r = "M14.5 18V16.5C14.5 15 15.5 14 17 14C18.5 14 19.5 15 19.5 16.5V18Z"
    return [shell(dome), mark(arch_l), mark(arch_r), detail("M12 6.5V11"), detail("M5.5 11H18.5"), line("M2 21H22")]


@icon("turtle-on-back", CAT, "Upside-down turtle lying on its domed shell with legs and head waving in the air", tags=["turtle", "upside down", "flipped", "stuck", "helpless", "reptile"])
def _(S):
    bowl = "M2.8 14H17.5C17.5 19.5 14 21.5 10 21.5C6 21.5 2.8 19.5 2.8 14Z"
    neck = thick("M16.5 14.5L19 11", 2.4, S)
    head = circle(19.4, 8.6, 2.4)
    return [shell(union(bowl, thick("M5.2 14L3.4 8.5", 2.2, S), thick("M10.5 14L10.5 8.5", 2.2, S), neck, head)), mark(circle(20.2, 8, 0.7)), detail("M6 17.5H14")]

@icon("turtles-on-log", CAT, "Three turtles of decreasing size sitting in a row on a floating log", tags=["turtles", "log", "pond", "basking", "group", "sunbathing"])
def _(S):
    t1 = union(_dome(2.2, 8.8, 14, 7.5), ellipse(10, 11.8, 1.3, 1.2))
    t2 = union(_dome(12.2, 16.6, 14, 9.5), ellipse(17.6, 12.2, 1, 0.9))
    t3 = _dome(18.8, 21.8, 14, 11.3)
    log = rect(2, 14, 20, 4.5, L(S, 1.5, 2.25))
    return [shell(union(t1, t2, t3, log)), line("M2 21.5H8M12 21.5H22")]


@icon("turtle-hatchling", CAT, "Baby turtle with flippers climbing out of a cracked round egg on the sand", tags=["turtle", "hatchling", "baby", "egg", "hatch", "sand"])
def _(S):
    egg = "M4.5 14L7.8 17L11 14L14 17L16.8 14L19.5 16.2C19.8 19.5 17 20.5 12 20.5C7 20.5 4.2 19.5 4.5 14Z"
    dome = "M7 14C7 9 9.5 7.5 12 7.5C14.5 7.5 17 9 17 14Z"
    head = ellipse(19, 10.5, 2, 1.8)
    fl = poly([(8, 12), (3.6, 9.5), (4.6, 13)], closed=True, r=L(S, 0, 0.5))
    return [shell(union(egg, dome, head, fl)), mark(circle(19.6, 10, 0.6))]

# --------------------------------------------------------------------------- snakes: scenes and things

@icon("snake-constricting", CAT, "Snake wrapped in tight coils around an upright pole with its head at the top", tags=["snake", "constrictor", "coil", "pole", "squeeze", "python"])
def _(S):
    pole = rect(10, 2.5, 4, 19, L(S, 0.5, 1.5))
    bands = union(thick("M5.5 19.5L18.5 16.5", 3, S), thick("M5.5 14.5L18.5 11.5", 3, S), thick("M5.5 9.5L16 7", 3, S))
    head = hd(18.5, 5.5, 2.8, 2.2, -20)
    return [shell(minus(pole, grow(bands, 1.1))), shell(union(bands, head)), mark(circle(19, 5, 0.7))]

@icon("snake-venom", CAT, "Single curved snake fang with a venom drop falling from its tip into a pool", tags=["snake", "fang", "venom", "poison", "toxin", "drop"])
def _(S):
    fang = "M7.5 3.5H16.5C16.5 8 14.8 12 12 15C9.2 12 7.5 8 7.5 3.5Z"
    return [shell(fang), detail("M12 6.5V11"), solid(drop(12, 18.6, 0.8)), line("M6 21H18")]


@icon("snake-charmer-basket", CAT, "Round woven basket with a cobra rising from it with its hood spread", tags=["snake", "charmer", "basket", "cobra", "flute", "performance"])
def _(S):
    hood = "M8.4 7C5.2 8 5.2 11.5 9 12.2H15C18.8 11.5 18.8 8 15.6 7Z"
    neck = thick("M12 12V15", 3, S)
    head = ellipse(12, 4.8, 2.1, 2.4)
    basket = poly([(4, 15), (20, 15), (18.5, 21.5), (5.5, 21.5)], closed=True, r=L(S, 0, 1.5))
    return [shell(union(hood, head)), shell(basket), detail("M5 18.3H19"), mark(circle(11.2, 4.4, 0.6)), mark(circle(12.8, 4.4, 0.6))]


@icon("snake-skin-shed", CAT, "Empty wavy tube of shed snake skin lying in an S shape with a scale texture", tags=["snake", "skin", "shed", "molt", "slough", "scales"])
def _(S):
    ctrl = ((4.5, 17.5), (7, 6), (16, 18), (19.5, 7))
    body = tube(ctrl, interp([(0, 1.6), (0.2, 4.4), (0.9, 4.4), (1, 5)]))
    ticks = []
    for t in (0.28, 0.45, 0.62, 0.79):
        x, y = bez(*ctrl, t)
        ticks.append(dot(x, y, 0.7))
    return [shell(body)] + ticks


@icon("tree-python", CAT, "Snake draped over a horizontal branch in loops with its head hanging down at the end", tags=["snake", "python", "branch", "tree", "arboreal", "loops"])
def _(S):
    sn = "M3.5 5.5C6 5.5 6.5 16.5 9.5 16.5C12.5 16.5 12.5 5.5 15.5 5.5C18 5.5 18.5 12.5 19.5 15"
    body = thick(sn, 2.6, S)
    head = hd(19.8, 17.2, 1.9, 2.8, 0)
    snake = union(body, head)
    branch = minus(thick("M2.5 11H21.5", 3.2, S), grow(snake, 1.0))
    return [shell(snake), shell(branch), mark(circle(20.6, 17, 0.6))]

# --------------------------------------------------------------------------- lizards: more species and scenes

@icon("chameleon-eye", CAT, "Front view of a turret-shaped chameleon eye with scale rings and a tiny round pupil", tags=["chameleon", "eye", "turret", "vision", "lizard", "reptile"])
def _(S):
    outer = poly(regular(12, 12, 9.6, 10), closed=True, r=L(S, 0, 2.4))
    return [shell(outer), detail(circle(12, 12, 5.2)), dot(12, 12, 1.9)]


@icon("frilled-lizard", CAT, "Front view of a lizard head with a huge frill spread around its neck and its mouth open", tags=["lizard", "frill", "frilled", "umbrella", "australia", "reptile"])
def _(S):
    frill = poly([pt_(12, 12, 9.8 if i % 2 == 0 else 8.2, -90 + i * 22.5) for i in range(16)], closed=True, r=L(S, 0, 1.8))
    head = ellipse(12, 12.6, 3.8, 4.9)
    return [shell(frill), detail(head), dot(10.4, 10.6, 0.8), dot(13.6, 10.6, 0.8), mark(ellipse(12, 15, 1.4, 1.2))]

@icon("horned-lizard", CAT, "Top view of a flat round-bodied lizard with a crown of sharp horns on its head and a short tail", tags=["lizard", "horned", "horny toad", "desert", "spikes", "reptile"])
def _(S):
    body = ellipse(12, 14, 6, 5.4)
    head = ellipse(12, 7.6, 2.4, 2.4)
    horns = [poly([(10, 8.6), (5.2, 5.4), (10.2, 6.6)], closed=True, r=L(S, 0, 0.4)), poly([(9.6, 10), (3.6, 9.2), (9.6, 8.4)], closed=True, r=L(S, 0, 0.4))]
    tail = tube(((12, 18), (12, 19.5), (12, 20.5), (12, 21.8)), interp([(0, 2.4), (1, 0.6)]))
    return [shell(union(body, head, *horns, *[flip(h) for h in horns], tail)),
            line("M7 12.4L3.5 11M17 12.4L20.5 11M7.4 17L4 19.4M16.6 17L20 19.4"), dot(12, 13.4, 0.8), dot(9.8, 15.6, 0.7), dot(14.2, 15.6, 0.7)]


@icon("lizard-hatchling", CAT, "Cracked oval egg with a small lizard head and front foot emerging from the top", tags=["lizard", "hatchling", "egg", "hatch", "baby", "reptile"])
def _(S):
    egg = "M4.5 13.5L7.8 16.5L11 13.5L14 16.5L16.8 13.5L19.5 16C20 19.5 17 21 12 21C7 21 4 19.5 4.5 13.5Z"
    head = poly([(8, 13.8), (8.8, 8.6), (12, 6), (20, 8.8), (20.8, 10.8), (14, 12.4), (12.8, 14)], closed=True, r=L(S, 0, 1.4))
    foot = thick("M7 13.5L4.5 10.5", 2, S)
    return [shell(union(egg, head, foot)), mark(circle(14, 8.6, 0.8))]

@icon("lizard-tracks", CAT, "Two rows of small five-toed footprints with a thin wavy tail-drag line between them", tags=["lizard", "tracks", "footprints", "trail", "prints", "reptile"])
def _(S):
    def pr(x, y):
        return union(ellipse(x, y + 1.1, 1.3, 1.1), circle(x - 1.9, y - 0.6, 0.8), circle(x, y - 1.3, 0.8), circle(x + 1.9, y - 0.6, 0.8))
    prints = [pr(5.5, 5.5), pr(5.5, 13.5), pr(5.5, 20), pr(18.5, 9), pr(18.5, 17)]
    return [solid(d) for d in prints] + [line("M12 3C10 7 14 10 12 14C10 18 14 20 12 22")] if False else [solid(d) for d in prints] + [line("M12 3C10 7 14 10 12 14C10 17 13 19 12 21")]


@icon("spiny-tailed-lizard", CAT, "Side view of a round-headed lizard with a short thick club tail ringed with rows of sharp spikes", tags=["lizard", "spiny", "tail", "mastigure", "spikes", "reptile"])
def _(S):
    body = ellipse(14.5, 11.5, 5, 3.2)
    head = poly([(17, 8.8), (21.8, 10.4), (21.8, 12.4), (17.5, 14)], closed=True, r=L(S, 0, 1.2))
    tail = ellipse(7.5, 12.5, 3.6, 2.6)
    sp = spikes(7.5, 12.5, 3.6, 2.6, [205, 240, 275, 310, 40, 140], 2.2, 1.2)
    return [shell(union(body, head, tail, *sp)), detail("M6.5 10.4V14.6"), dot(19.6, 10.6, 0.7), line("M16.5 14.4L17.6 18H20M11.5 14.4L10.6 18H8") if False else line("M16.5 14.4L17.6 18M11.5 14.4L10.6 18")]
