"""TypeIcon Core: plants (batch plants_003): houseplants, carnivorous plants, cacti and succulents, grasses,
crop and herb plants, seeds, roots, wood and plant parts."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, LINE, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "plants"
G = 21.5


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def mirror(d):
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def leaf_shape(x1, y1, x2, y2, bulge):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    b = bulge * 2
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx * b)} {fmt(my + ny * b)} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(mx - nx * b)} {fmt(my - ny * b)} {fmt(x1)} {fmt(y1)}Z")


def arc_leaf(x1, y1, x2, y2, bend, w):
    """Curved pointed leaf from p1 to p2; bend shifts the centre line sideways, w is half width."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    cx, cy = mx + nx * bend, my + ny * bend
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(cx + nx * w * 2)} {fmt(cy + ny * w * 2)} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(cx - nx * w * 2)} {fmt(cy - ny * w * 2)} {fmt(x1)} {fmt(y1)}Z")


def heart(ax, ay, ang, length, width):
    """Heart-shaped leaf: notch at (ax, ay), tip `length` away in direction ang (0 = right, 90 = down)."""
    l, w = length, width
    d = (f"M{fmt(ax)} {fmt(ay)}C{fmt(ax - .15 * l)} {fmt(ay - .35 * w)} {fmt(ax - .05 * l)} {fmt(ay - .55 * w)} {fmt(ax + .22 * l)} {fmt(ay - .5 * w)}"
         f"C{fmt(ax + .55 * l)} {fmt(ay - .45 * w)} {fmt(ax + .85 * l)} {fmt(ay - .2 * w)} {fmt(ax + l)} {fmt(ay)}"
         f"C{fmt(ax + .85 * l)} {fmt(ay + .2 * w)} {fmt(ax + .55 * l)} {fmt(ay + .45 * w)} {fmt(ax + .22 * l)} {fmt(ay + .5 * w)}"
         f"C{fmt(ax - .05 * l)} {fmt(ay + .55 * w)} {fmt(ax - .15 * l)} {fmt(ay + .35 * w)} {fmt(ax)} {fmt(ay)}Z")
    return rot(d, ang, ax, ay)


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def taper(p0, p1, p2, p3, w0, n=16, power=0.9):
    """Closed outline of a tapering curved shape (chili, horn, root): width w0 at p0 falling to a point at p3."""
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x, y = bez(p0, p1, p2, p3, t)
        xa, ya = bez(p0, p1, p2, p3, min(1, t + 1e-3))
        xb, yb = bez(p0, p1, p2, p3, max(0, t - 1e-3))
        ln = math.hypot(xa - xb, ya - yb)
        nx, ny = -(ya - yb) / ln, (xa - xb) / ln
        w = w0 * (1 - t) ** power / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return left + right[::-1][1:]


def serrated(x1, y1, x2, y2, bulge, teeth=4, depth=1.0, r=0.0):
    """Pointed leaf from p1 to p2 with a saw-toothed edge (teeth per side, depth in px)."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln

    def side(sign, forward):
        cx, cy = mx + nx * bulge * 2 * sign, my + ny * bulge * 2 * sign
        pts = []
        m = teeth * 2
        order = range(1, m) if forward else range(m - 1, 0, -1)
        for i in order:
            t = i / m
            u = 1 - t
            x = u * u * x1 + 2 * u * t * cx + t * t * x2
            y = u * u * y1 + 2 * u * t * cy + t * t * y2
            tx, ty = 2 * u * (cx - x1) + 2 * t * (x2 - cx), 2 * u * (cy - y1) + 2 * t * (y2 - cy)
            tl = math.hypot(tx, ty)
            # outward normal for this side
            ox, oy = -ty / tl * sign, tx / tl * sign
            k = depth if i % 2 == 1 else 0.0
            pts.append((x + ox * k, y + oy * k))
        return pts
    pts = [(x1, y1)] + side(1, True) + [(x2, y2)] + side(-1, False)
    return poly(pts, closed=True, r=r)


def blob(*circles):
    return union(*[circle(x, y, r) for x, y, r in circles])


def flower_d(cx, cy, r, n=5, pr=None, start=-90.0):
    pr = pr or r * 0.55
    return union(*[circle(*polar(cx, cy, r - pr, start + k * 360 / n), pr) for k in range(n)], circle(cx, cy, r - pr))


def pot(S, top=16, bot=21.5, hw=5.5, bw=4):
    """Flower pot: flared trapezoid."""
    return shell(poly([(12 - hw, top), (12 + hw, top), (12 + bw, bot), (12 - bw, bot)], closed=True, r=S.r))


def ground(x0=2.5, x1=21.5, y=G):
    return line(seg(x0, y, x1, y))


# ============================================================================ chunk 1: houseplants and carnivores

@icon("hanging-plant", CAT, "Pot held in a rope hanger with leafy vines trailing below",
      tags=["hanging plant", "macrame", "trailing vine", "houseplant", "basket", "pothos"])
def _(S):
    return [shell(poly([(6.5, 8.5), (17.5, 8.5), (16, 13.5), (8, 13.5)], closed=True, r=S.r)),
            line(poly([(6.5, 8.5), (12, 3.5), (17.5, 8.5)], r=S.r)), line(seg(12, 3.5, 12, 2)),
            line("M9.5 13.5C8 16.5 11 18 9.5 21"), line("M15 13.5C16 15 14.5 16.5 15 18"),
            solid(leaf_shape(9.2, 16, 5, 15.5, 1.3)), solid(leaf_shape(9.8, 20.5, 13.5, 19.5, 1.3)),
            solid(leaf_shape(15, 17.5, 19.3, 17.5, 1.3))]

@icon("potted-palm", CAT, "Pot with a cluster of arching palm fronds",
      tags=["palm", "potted palm", "areca", "houseplant", "tropical", "fronds"])
def _(S):
    cx, cy = 12, 14
    return [pot(S, 17, 21.5, 5, 3.5), line(seg(12, 17, 12, 13.5)),
            shell(arc_leaf(cx, cy, 2.5, 13, -5, 1.4)), shell(arc_leaf(cx, cy, 21.5, 13, 5, 1.4)),
            shell(arc_leaf(cx, cy, 6.5, 3.5, -1.5, 1.2)), shell(arc_leaf(cx, cy, 17.5, 3.5, 1.5, 1.2))]

@icon("peace-lily", CAT, "Pot of glossy leaves with a hooded white flower on a tall stalk",
      tags=["peace lily", "spathiphyllum", "houseplant", "air purifier", "indoor", "flower"])
def _(S):
    return [pot(S, 17, 21.5, 5, 3.5),
            shell(leaf_shape(11.5, 17, 4.5, 10.5, 1.7)), shell(leaf_shape(12.5, 17, 19.5, 10.5, 1.7)),
            line(seg(12, 17, 12, 10)),
            shell(leaf_shape(12, 2.5, 12, 10, 2.3)), dot(12, 7, 0.9)]


@icon("philodendron", CAT, "Pot with large glossy heart-shaped leaves on long stalks",
      tags=["philodendron", "heart leaf", "houseplant", "tropical", "indoor", "foliage"])
def _(S):
    return [pot(S, 17, 21.5, 5, 3.5),
            line(poly([(12, 17), (9, 13.5)], r=0)), line(poly([(12, 17), (15.5, 11)], r=0)),
            shell(heart(9, 13.5, -115, 9.5, 7.5)), shell(heart(15.5, 11, -65, 8.5, 7))]

def _arrowhead(ax, ay, ang, length, width):
    l, w = length, width
    d = (f"M{fmt(ax)} {fmt(ay)}C{fmt(ax - .05 * l)} {fmt(ay - .15 * w)} {fmt(ax + .05 * l)} {fmt(ay - .9 * w)} {fmt(ax + .1 * l)} {fmt(ay - w)}"
         f"C{fmt(ax + .4 * l)} {fmt(ay - .6 * w)} {fmt(ax + .7 * l)} {fmt(ay - .25 * w)} {fmt(ax + l)} {fmt(ay)}"
         f"C{fmt(ax + .7 * l)} {fmt(ay + .25 * w)} {fmt(ax + .4 * l)} {fmt(ay + .6 * w)} {fmt(ax + .1 * l)} {fmt(ay + w)}"
         f"C{fmt(ax + .05 * l)} {fmt(ay + .9 * w)} {fmt(ax - .05 * l)} {fmt(ay + .15 * w)} {fmt(ax)} {fmt(ay)}Z")
    return rot(d, ang, ax, ay)


def _arrow(ax, ay, ang, length, width):
    l, w = length, width
    pts = [(ax, ay - l), (ax + w, ay + .25 * l), (ax, ay), (ax - w, ay + .25 * l)]
    return pts, ang, ax, ay


@icon("alocasia", CAT, "Pot with a tall stalk carrying a large arrowhead leaf with light veins",
      tags=["alocasia", "elephant ear", "arrowhead", "houseplant", "tropical", "veined leaf"])
def _(S):
    return [pot(S, 18, 21.5, 4.5, 3.2),
            line(seg(12, 18, 12, 15)), line(poly([(11, 18), (8.5, 16.5)], r=0)),
            shell(heart(12, 15, -88, 12.5, 8.6)),
            shell(heart(8.5, 16.5, -150, 6, 4.2)),
            detail(seg(12, 13.5, 12, 7))]

@icon("umbrella-plant", CAT, "Pot with a ring of oval leaflets fanning from one stalk like umbrella spokes",
      tags=["umbrella plant", "schefflera", "houseplant", "palmate", "indoor", "leaflets"])
def _(S):
    parts = [pot(S, 17, 21.5, 5, 3.5), line(seg(12, 17, 12, 11))]
    for a in (-170, -130, -90, -50, -10):
        x, y = polar(12, 11, 8.8, a)
        parts.append(shell(leaf_shape(12, 11, x, y, 1.6)))
    return parts


@icon("polka-dot-plant", CAT, "Pot with oval leaves covered in round spots",
      tags=["polka dot plant", "hypoestes", "freckle face", "spotted leaf", "houseplant", "indoor"])
def _(S):
    return [pot(S, 17.5, 21.5, 4.5, 3.2),
            shell(leaf_shape(11.5, 17.5, 4.5, 10, 2.8)), shell(leaf_shape(12.5, 17.5, 19.5, 10, 2.8)),
            shell(leaf_shape(12, 17.5, 12, 3.5, 2.8)),
            dot(12, 10, 1.0), dot(12, 14, 0.9), dot(8.3, 13.3, 0.9), dot(15.7, 13.3, 0.9)]


@icon("african-violet", CAT, "Low rosette of round leaves in a pot with a cluster of five-petal flowers",
      tags=["african violet", "saintpaulia", "houseplant", "windowsill", "flowering", "purple"])
def _(S):
    return [pot(S, 16.5, 21.5, 5, 3.5),
            shell(ellipse(6.5, 14, 3.8, 2.2)), shell(ellipse(17.5, 14, 3.8, 2.2)),
            shell(flower_d(12, 8.5, 5.2)), dot(12, 8.5, 1.1)]


@icon("bromeliad", CAT, "Rosette of stiff arching strap leaves with a spiky flower spike in the middle",
      tags=["bromeliad", "tropical", "rosette", "flower spike", "air plant", "pineapple family"])
def _(S):
    return [shell(arc_leaf(11, 20, 3, 9, -2.5, 1.3)), shell(arc_leaf(13, 20, 21, 9, 2.5, 1.3)),
            shell(leaf_shape(12, 20, 12, 2.5, 2.1))]

@icon("braided-money-tree", CAT, "Pot with a braided slim trunk and a round crown of hand-shaped leaves",
      tags=["money tree", "pachira", "braided trunk", "houseplant", "luck", "feng shui"])
def _(S):
    return [pot(S, 16.5, 21.5, 5, 3.5),
            line("M10.3 16.5C10.3 14.3 13.7 13.3 13.7 11"), line("M13.7 16.5C13.7 14.3 10.3 13.3 10.3 11"),
            shell(blob((8, 7.5, 3.5), (12, 5, 3.5), (16, 7.5, 3.5), (12, 8.3, 3.3))),
            detail(seg(12, 8.5, 12, 6)), detail(seg(12, 8.5, 9.3, 7)), detail(seg(12, 8.5, 14.7, 7))]


@icon("ponytail-palm", CAT, "Swollen bulbous trunk base topped by a fountain of long thin curly leaves",
      tags=["ponytail palm", "elephant foot", "beaucarnea", "houseplant", "bulb trunk", "succulent"])
def _(S):
    base = L(S, "M6.5 21.5C4 18 6 13.5 12 13.5C18 13.5 20 18 17.5 21.5Z",
             "M8 21.5Q6.3 21.5 5.6 20C4.2 17 6 13.5 12 13.5C18 13.5 19.8 17 18.4 20Q17.7 21.5 16 21.5Z")
    return [shell(base),
            line("M12 13.5C11 6 5 4 3.5 11"), line("M12 13.5C13 6 19 4 20.5 11"),
            line("M12 13.5C11.5 8 8.5 6.5 7.5 10.5"), line("M12 13.5C12.5 8 15.5 6.5 16.5 10.5"),
            line(seg(12, 13.5, 12, 4))]


@icon("staghorn-fern", CAT, "Wall-mounted board with a round shield leaf and forked antler-like fronds",
      tags=["staghorn fern", "platycerium", "epiphyte", "wall mount", "fern", "houseplant"])
def _(S):
    return [shell(rect(4, 2.5, 16, 19, L(S, 1.5, 3))),
            detail(circle(12, 17, 2.2)),
            detail(seg(12, 14.8, 12, 6)), detail(seg(12, 10, 9.3, 7)), detail(seg(12, 10, 14.7, 7)),
            detail(poly([(10, 16), (7, 12.5), (7, 7.5)], r=S.r)), detail(poly([(14, 16), (17, 12.5), (17, 7.5)], r=S.r))]


@icon("yucca", CAT, "Woody trunk topped by a spiky ball of stiff sword-shaped leaves",
      tags=["yucca", "spiky", "desert plant", "sword leaves", "houseplant", "agave family"])
def _(S):
    parts = [line("M12 21.5C12 18 13 16 12 10")]
    for a in (-175, -145, -115, -90, -65, -35, -5):
        x, y = polar(12, 9.5, 8.5, a)
        parts.append(line(seg(12, 9.5, x, y)))
    parts += [line(seg(9, 21.5, 15, 21.5))]
    return parts

def _teeth():
    out = []
    ux, uy = -8 / 15.26, -13 / 15.26
    nx, ny = 13 / 15.26, -8 / 15.26
    for t in (.3, .5, .7):
        ax, ay = 12 - 8 * t, 17.5 - 13 * t
        off = 2 * t * (1 - t) * 6.4 * 0.55
        ex, ey = ax + nx * off, ay + ny * off
        out.append(seg(ex, ey, ex + nx * 3.4, ey + ny * 3.4))
    return out


_JAW = [(11.5, 17.5), (10.4, 14.6), (7.8, 14.2), (9.3, 11.8), (6.7, 10.6), (8.3, 8.4), (5.4, 6.8), (5.6, 4.5)]


def _jaw(S):
    return poly(_JAW, closed=True, r=S.r * 0.4)


@icon("venus-flytrap", CAT, "Open leaf trap with two jaws lined with bristle teeth on a short stem",
      tags=["venus flytrap", "dionaea", "carnivorous plant", "insect trap", "teeth", "bog plant"])
def _(S):
    outer = "M11.5 17.5C5.5 17 3 10 5.6 4.5"
    return [shell(union(_jaw(S), "M11.5 17.5C4 17 2.5 9 5.6 4.5L7 9L9 14Z")),
            shell(mirror(union(_jaw(S), "M11.5 17.5C4 17 2.5 9 5.6 4.5L7 9L9 14Z"))),
            line(seg(12, 17.5, 12, 21.5))]

@icon("pitcher-plant", CAT, "Tall tube-shaped pitcher leaf with a rolled rim and a small lid over its opening",
      tags=["pitcher plant", "nepenthes", "carnivorous plant", "insect trap", "tube", "tropical"])
def _(S):
    return [line("M7 9.5C7 15 6.5 21.5 12 21.5C17.5 21.5 17 15 17 9.5"),
            shell(ellipse(12, 9.5, 5, 2)),
            shell(arc_leaf(9.5, 5, 18, 4.5, -1.2, 1.6)),
            detail(seg(12, 14, 12, 18))]


# ============================================================================ chunk 2: carnivores, cacti, succulents

@icon("sundew", CAT, "Round leaf covered with thin tentacles each tipped with a sticky dew drop",
      tags=["sundew", "drosera", "carnivorous plant", "sticky leaf", "dew", "bog plant"])
def _(S):
    parts = [shell(circle(12, 11.5, 3.5))]
    for a in (-90, -45, 0, 45, 135, 180, -135):
        x1, y1 = polar(12, 11.5, 3.5, a)
        x2, y2 = polar(12, 11.5, 6.6, a)
        x3, y3 = polar(12, 11.5, 8.2, a)
        parts += [line(seg(x1, y1, x2, y2)), dot(x3, y3, 1.3)]
    parts.append(line(seg(12, 15, 12, G)))
    return parts


@icon("cobra-lily", CAT, "Hooded tube leaf curving over like a cobra head with a forked tongue hanging below",
      tags=["cobra lily", "darlingtonia", "cobra plant", "carnivorous plant", "pitcher", "hood"])
def _(S):
    body = L(S, "M6.5 21.5C6.5 14 5.5 6 12 3.5C17 2 20.5 5.5 18.5 10L15.5 9.5C14.5 13 14.5 17 16 21.5Z",
             "M8 21.5Q6.5 21.5 6.5 20C6.3 13.5 5.8 6.2 12 3.5C17 2 20.5 5.5 18.5 10L15.5 9.5C14.5 13 14.5 17 15.5 20Q15.8 21.5 14 21.5Z")
    return [shell(body), line(poly([(19.5, 11.5), (19.5, 15.5)], r=0)), line(seg(19.5, 15.5, 17.5, 18)), line(seg(19.5, 15.5, 21.5, 18))]


@icon("christmas-cactus", CAT, "Pot with drooping chains of flat segmented stems ending in flowers",
      tags=["christmas cactus", "holiday cactus", "schlumbergera", "houseplant", "trailing", "winter bloom"])
def _(S):
    return [pot(S, 17, 21.5, 5, 3.5),
            line(poly([(10.5, 17), (8.5, 12), (5.5, 9.5), (4, 12.5)], r=S.r)),
            line(poly([(13.5, 17), (15.5, 12), (18.5, 9.5), (20, 12.5)], r=S.r)),
            line(seg(12, 17, 12, 11)),
            solid(flower_d(4, 14.6, 2.6)), solid(flower_d(20, 14.6, 2.6)), solid(flower_d(12, 9, 2.8))]

@icon("moon-cactus", CAT, "Small round ribbed cactus ball grafted on top of a column cactus in a pot",
      tags=["moon cactus", "gymnocalycium", "grafted cactus", "colourful cactus", "houseplant", "hibotan"])
def _(S):
    return [pot(S, 18, 21.5, 4.5, 3.2),
            shell(union(circle(12, 9, 5.2), rect(9, 12, 6, 6, 0))),
            solid(flower_d(12, 2.9, 2.1)),
            dot(9.8, 7.8, 0.9), dot(14.2, 7.8, 0.9), dot(12, 10.8, 0.9)]

@icon("barrel-cactus", CAT, "Squat round barrel-shaped cactus with vertical ribs and a few flowers on top",
      tags=["barrel cactus", "echinocactus", "golden barrel", "desert", "spines", "ribbed cactus"])
def _(S):
    body = L(S, "M3.5 21.5C2.5 15 6 9 12 9C18 9 21.5 15 20.5 21.5Z",
             "M5 21.5Q3.3 21.5 3.2 19.8C2.6 14.5 6.2 9 12 9C17.8 9 21.4 14.5 20.8 19.8Q20.7 21.5 19 21.5Z")
    return [shell(body), detail(seg(12, 10.5, 12, 21)),
            detail("M8.3 11C6.7 14 6.7 18 8 21"), detail("M15.7 11C17.3 14 17.3 18 16 21"),
            dot(9, 5.3, 1.4), dot(12, 4.3, 1.4), dot(15, 5.3, 1.4)]

@icon("star-cactus", CAT, "Top view of a round cactus divided into star-like ribs radiating from a centre dot",
      tags=["star cactus", "astrophytum", "sand dollar cactus", "top view", "ribs", "desert"])
def _(S):
    n = 5
    pts = []
    for k in range(n):
        pts.append(polar(12, 12, 9.5, -90 + k * 72))
        pts.append(polar(12, 12, 6.4, -90 + k * 72 + 36))
    parts = [shell(poly(pts, closed=True, r=L(S, 0, 1.8)), stroke_miterlimit="8")]
    for k in range(n):
        a = -90 + k * 72 + 36
        x1, y1 = polar(12, 12, 2.6, a)
        x2, y2 = polar(12, 12, 6.4, a)
        parts.append(detail(seg(x1, y1, x2, y2)))
    parts.append(dot(12, 12, 1.2))
    return parts


@icon("organ-pipe-cactus", CAT, "Cluster of tall straight ribbed cactus columns rising from one base",
      tags=["organ pipe cactus", "stenocereus", "saguaro", "columnar cactus", "desert", "sonoran"])
def _(S):
    rx = L(S, 1.5, 2.5)
    cols = [rot(rect(3.5, 7, 5, 14.5, rx), -9, 6, 21.5), rect(9.5, 2.5, 5, 19, rx), rot(rect(15.5, 9, 5, 12.5, rx), 9, 18, 21.5)]
    return [shell(union(*cols)), ground(2.5, 21.5)]

@icon("old-man-cactus", CAT, "Upright cactus column covered in long shaggy white hair lines",
      tags=["old man cactus", "cephalocereus", "hairy cactus", "desert", "shaggy", "columnar cactus"])
def _(S):
    return [shell(rect(9, 5.5, 6, 16, 3)),
            line("M7 7C5 10.5 7 14 5 18.5"), line("M17 7C19 10.5 17 14 19 18.5"),
            line("M8 12.5C6.5 14.5 7.5 17 6.5 19.5"), line("M16 12.5C17.5 14.5 16.5 17 17.5 19.5"),
            dot(12, 2.8, 1.3)]

@icon("echeveria", CAT, "Top view of a succulent rosette of plump pointed leaves in a tight spiral",
      tags=["echeveria", "succulent", "rosette", "top view", "hens and chicks", "stone rose"])
def _(S):
    petals = union(*[leaf_shape(12, 12, *polar(12, 12, 9.6, -90 + k * 60), 2.7) for k in range(6)])
    parts = [shell(petals, stroke_miterlimit="8")]
    for k in range(6):
        x1, y1 = polar(12, 12, 2.8, -90 + k * 60)
        x2, y2 = polar(12, 12, 6.3, -90 + k * 60)
        parts.append(detail(seg(x1, y1, x2, y2)))
    parts.append(dot(12, 12, 1.1))
    return parts


@icon("haworthia", CAT, "Small pot with a tight rosette of stiff pointed leaves marked with horizontal stripes",
      tags=["haworthia", "zebra plant", "succulent", "striped leaves", "houseplant", "rosette"])
def _(S):
    r = S.r * 0.6
    return [pot(S, 17, 21.5, 5.5, 4),
            shell(poly([(3, 17), (5, 8.5), (10.5, 17)], closed=True, r=r)),
            shell(poly([(13.5, 17), (19, 8.5), (21, 17)], closed=True, r=r)),
            shell(poly([(8, 17), (12, 3.5), (16, 17)], closed=True, r=r)),
            detail(seg(10.6, 12, 13.4, 12)), detail(seg(5.6, 14, 7.6, 14)), detail(seg(16.4, 14, 18.4, 14))]


@icon("agave", CAT, "Large spiky rosette of broad thick leaves with pointed tips growing from the ground",
      tags=["agave", "century plant", "tequila", "succulent", "desert", "spiky"])
def _(S):
    cx, cy = 12, 19
    def lf(r, a, b):
        x, y = polar(cx, cy, r, a)
        return shell(leaf_shape(cx, cy, x, y, b), stroke_miterlimit="8")
    return [lf(11.5, -152, 1.7), lf(11.5, -28, 1.7), lf(15, -122, 1.9), lf(15, -58, 1.9), lf(16.5, -90, 2.0), ground(4, 20)]

@icon("lithops", CAT, "Pair of split pebble-like succulents with flat tops sitting in gravel",
      tags=["lithops", "living stones", "pebble plant", "succulent", "desert", "mesemb"])
def _(S):
    return [shell(rect(2.5, 10.5, 9, 7.5, L(S, 3, 3.5))), shell(rect(13, 12.5, 8.5, 5.5, L(S, 2.5, 2.75))),
            detail(seg(7, 10.5, 7, 14.5)), detail(seg(17.25, 12.5, 17.25, 15)),
            dot(5, 21, 0.9), dot(9.5, 20.8, 0.9), dot(14, 21, 0.9), dot(19, 20.8, 0.9)]

@icon("welwitschia", CAT, "Desert plant with two long ribbon leaves sprawling and splitting along the ground from a low stump",
      tags=["welwitschia", "namib", "desert plant", "ribbon leaves", "living fossil", "strap leaves"])
def _(S):
    stump = L(S, "M8 16C8 11 9.5 9.5 12 9.5C14.5 9.5 16 11 16 16Z",
              "M9 16Q8 16 8 15C8 11 9.5 9.5 12 9.5C14.5 9.5 16 11 16 15Q16 16 15 16Z")
    return [shell(stump),
            shell(arc_leaf(9, 15, 2.5, 18.5, -2.2, 1.8)), shell(arc_leaf(15, 15, 21.5, 18.5, 2.2, 1.8)),
            shell(arc_leaf(10, 17, 3.5, 21, -1.5, 1.5)), shell(arc_leaf(14, 17, 20.5, 21, 1.5, 1.5))]

@icon("ocotillo", CAT, "Cluster of long thin whip-like stems fanning up from the ground with red flower tips",
      tags=["ocotillo", "coachwhip", "desert", "sonoran", "spiny stems", "flowering shrub"])
def _(S):
    parts = []
    for bx, cx, tx, ty in ((10.5, 6, 3.5, 5), (11.3, 9, 8, 3.5), (12, 12, 12, 3), (12.7, 15, 16, 3.5), (13.5, 18, 20.5, 5)):
        parts.append(line(f"M{bx} 21.5C{bx} 15 {cx} 12 {tx} {ty + 1.6}"))
        parts.append(dot(tx, ty, 1.5))
    return parts

@icon("grass-tree", CAT, "Short dark trunk topped by a round skirt of fine grassy leaves and one tall spear flower spike",
      tags=["grass tree", "xanthorrhoea", "blackboy", "australia", "spear flower", "bush"])
def _(S):
    return [shell(rect(10, 13.5, 4, 8, L(S, 0, 1.5))),
            line("M12 13C7.5 13 4.5 14 3.5 18"), line("M12 13C8.5 11 5 11.5 3 14"),
            line("M12 13C16.5 13 19.5 14 20.5 18"), line("M12 13C15.5 11 19 11.5 21 14"),
            line(seg(12, 13.5, 12, 6)), solid(leaf_shape(12, 9, 12, 2.5, 1.1))]


@icon("plant-cloche", CAT, "Glass bell dome with a knob on top covering a small plant",
      tags=["cloche", "glass dome", "terrarium", "bell jar", "plant cover", "greenhouse"])
def _(S):
    dome = L(S, "M4.5 18C4.5 10 8 6.5 12 6.5C16 6.5 19.5 10 19.5 18Z",
             "M6.5 18Q4.5 18 4.5 16C4.5 10 8 6.5 12 6.5C16 6.5 19.5 10 19.5 16Q19.5 18 17.5 18Z")
    return [shell(dome), dot(12, 4, 1.8), shell(rect(2.5, 18, 19, 3.5, L(S, 0, 1.75))),
            detail(seg(12, 18, 12, 13)), Part("dot", leaf_shape(12, 15, 7.5, 11.5, 1.4)), Part("dot", leaf_shape(12, 14, 16.5, 11, 1.4))]



# ============================================================================ chunk 3: grasses, crops, herbs

@icon("rice-plant", CAT, "Tuft of long thin leaves with a drooping panicle of small grains bending down from the top",
      tags=["rice", "paddy", "grain", "crop", "panicle", "cereal", "harvest"])
def _(S):
    return [line("M12 21.5C12 13 12 7 15.5 4.5C18.5 3 19.5 6 19 9"),
            line("M12 21.5C9.5 18 6.5 15 4 11"), line("M12 21.5C8.5 20 6 19 3.5 17"),
            line("M12 21.5C15.5 19.5 18 17.5 20.5 15.5"),
            solid(leaf_shape(19, 7.2, 19, 10.5, 1.1)), solid(leaf_shape(16.8, 6, 16.8, 9.3, 1.1)),
            solid(leaf_shape(20.5, 9.5, 20.5, 12.8, 1.1)), solid(leaf_shape(17.5, 11, 17.5, 14, 1.1))]


@icon("oat-plant", CAT, "Thin stem with small dangling spikelets hanging from delicate side branches",
      tags=["oat", "oats", "grain", "cereal", "spikelet", "crop", "porridge"])
def _(S):
    return [line(seg(12, 21.5, 12, 5)),
            line("M12 6.5Q9 5.5 7 8"), solid(leaf_shape(7, 7.6, 7, 12.6, 1.3)),
            line("M12 10Q15 9 17 11.5"), solid(leaf_shape(17, 11, 17, 16, 1.3)),
            line("M12 14.5Q9 13.5 7.3 16"), solid(leaf_shape(7.3, 15.3, 7.3, 20.3, 1.3)),
            solid(leaf_shape(12, 2.3, 12, 7, 1.3))]


@icon("pampas-grass", CAT, "Clump of long arching blades with tall feathery plumes rising above them",
      tags=["pampas grass", "cortaderia", "ornamental grass", "plume", "garden", "boho"])
def _(S):
    return [line("M12 21.5C11 16 6 14 2.8 15.5"), line("M12 21.5C13 16 18 14 21.2 15.5"),
            line("M11.5 21.5C10 18.5 7 18 4 20.5"), line("M12.5 21.5C14 18.5 17 18 20 20.5"),
            line(seg(12, 21.5, 12, 13)),
            shell(leaf_shape(12, 14, 9, 2.5, 1.7)), shell(leaf_shape(12, 14, 15.5, 3.5, 1.6))]


@icon("cattail", CAT, "Tall stem with a brown sausage-shaped spike near the top and long straight leaves",
      tags=["cattail", "bulrush", "typha", "marsh", "wetland", "reed"])
def _(S):
    return [line(seg(12, 21.5, 12, 12)), shell(rect(10, 4.5, 4, 8.5, L(S, 1.5, 2))), line(seg(12, 4.5, 12, 2.5)),
            line(seg(10.5, 21.5, 5, 9)), line(seg(13.5, 21.5, 19, 11.5))]


@icon("papyrus", CAT, "Tall stems each topped with a spray of thin radiating threads like an umbrella",
      tags=["papyrus", "cyperus", "sedge", "egypt", "nile", "umbrella plant", "aquatic"])
def _(S):
    parts = [line(seg(12, 21.5, 12, 11)), line(seg(5, 21.5, 5, 16.5)), line(seg(19, 21.5, 19, 15.5))]
    for a in (-180, -150, -120, -90, -60, -30, 0):
        parts.append(line(seg(12, 11, *polar(12, 11, 8, a))))
    for a in (-170, -130, -90, -50, -10):
        parts.append(line(seg(5, 16.5, *polar(5, 16.5, 3.4, a))))
        parts.append(line(seg(19, 15.5, *polar(19, 15.5, 3.4, a))))
    return parts

@icon("grass-tuft", CAT, "Small clump of pointed grass blades of different heights on a ground line",
      tags=["grass", "tuft", "lawn", "meadow", "blades", "weed", "turf"])
def _(S):
    parts = [ground(3, 21)]
    for bx, tx, ty in ((7, 4.5, 13), (9.5, 8, 7), (12, 12, 3.5), (14.5, 16.5, 8), (17, 19.5, 13.5)):
        parts.append(line(f"M{bx} 21.5C{bx} {(21.5 + ty) / 2 + 3} {tx} {ty + 4} {tx} {ty}"))
    return parts


@icon("tumbleweed", CAT, "Round ball of tangled dry twigs rolling with short motion lines behind it",
      tags=["tumbleweed", "desert", "wild west", "dry", "rolling", "barren"])
def _(S):
    rs = [6, 6.5, 5.7, 6.3, 5.9, 6.5, 5.8, 6.4, 6, 6.1]
    pts = [polar(16, 12, rs[k], -90 + k * 36) for k in range(10)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 3))),
            detail("M11 10.5Q16 15.5 21 10"), detail("M11.5 16Q16 8.5 20.5 15.5"),
            line(seg(2.5, 9, 7, 9)), line(seg(2.5, 12.5, 6, 12.5)), line(seg(2.5, 16, 7, 16))]

@icon("cotton-boll", CAT, "Open split pod with fluffy white cotton puffs and dry pointed bracts",
      tags=["cotton", "boll", "cotton plant", "fibre", "textile", "crop", "fluffy"])
def _(S):
    return [line(seg(12, 21.5, 12, 18)),
            shell(leaf_shape(12, 18.5, 3.5, 10.5, 1.7)), shell(leaf_shape(12, 18.5, 20.5, 10.5, 1.7)),
            shell(union(circle(8.5, 8.5, 3.6), circle(15.5, 8.5, 3.6), circle(12, 6.2, 3.6), circle(12, 11, 3.2)))]


@icon("coffee-plant", CAT, "Branch with glossy paired leaves and a cluster of round coffee cherries",
      tags=["coffee", "coffee plant", "coffee cherries", "coffee bean", "arabica", "plantation"])
def _(S):
    return [line(seg(2.5, 14.5, 21, 9.5)),
            shell(leaf_shape(6.5, 13.4, 4.5, 5.5, 1.6)), shell(leaf_shape(6.5, 13.4, 8.5, 20.5, 1.6)),
            shell(leaf_shape(11.5, 12, 10.5, 4, 1.6)), shell(leaf_shape(11.5, 12, 14, 19, 1.6)),
            dot(17.5, 13, 1.9), dot(20.3, 12.3, 1.7), dot(17.8, 16.6, 1.9)]


@icon("vanilla-pod", CAT, "Two long thin dark bean pods crossed below a small vanilla orchid flower",
      tags=["vanilla", "vanilla bean", "vanilla pod", "orchid", "spice", "baking"])
def _(S):
    return [shell(arc_leaf(3.5, 21, 20, 10, 1.6, 1.0)), shell(arc_leaf(4, 10, 20.5, 21, -1.6, 1.0)),
            shell(flower_d(12, 5.5, 3.6)), dot(12, 5.5, 1.0)]


@icon("peanut-plant", CAT, "Low leafy plant above a ground line with peanut pods hanging from pegs in the soil below",
      tags=["peanut", "groundnut", "peanut plant", "legume", "crop", "pegs"])
def _(S):
    def pod(x, y):
        return solid(union(circle(x, y - 1.7, 2.3), circle(x, y + 1.7, 2.3)))
    return [line(seg(12, 13, 12, 7)),
            shell(leaf_shape(12, 9.5, 6, 6.5, 1.5)), shell(leaf_shape(12, 9.5, 18, 6.5, 1.5)), shell(leaf_shape(12, 7, 12, 2.5, 1.3)),
            ground(2.5, 21.5, 13),
            line("M8.5 13L8 15.5"), pod(8, 18.3), line("M15.5 13L16 15"), pod(16, 17.8)]


def _ivy_leaf(S, cx, cy, ang):
    pts = []
    for k in range(10):
        r = 4.7 if k % 2 == 0 else 2.3
        pts.append(polar(cx, cy, r, ang + k * 36))
    return poly(pts, closed=True, r=S.r * 0.5)


def _ivy_leaf(x, y, phi, k=1.0):
    """Three-lobed leaf with its base at (x, y), tip pointing along phi (degrees, 0 = right, -90 = up)."""
    return union(leaf_shape(x, y, *polar(x, y, 7 * k, phi), 1.7 * k),
                 leaf_shape(x, y, *polar(x, y, 5 * k, phi - 55), 1.3 * k),
                 leaf_shape(x, y, *polar(x, y, 5 * k, phi + 55), 1.3 * k))


@icon("ivy", CAT, "Trailing vine with alternating leaves each shaped with pointed lobes",
      tags=["ivy", "vine", "climber", "hedera", "trailing", "creeper"])
def _(S):
    return [line("M12 21.5C12 18 11 16 12 13.5C13 11 12 9.5 12 7.5"),
            shell(_ivy_leaf(12, 20, -20), stroke_miterlimit="8"),
            shell(_ivy_leaf(12, 14.5, -160), stroke_miterlimit="8"),
            shell(_ivy_leaf(12, 10, -20), stroke_miterlimit="8"),
            shell(_ivy_leaf(12, 7.5, -90, 0.75), stroke_miterlimit="8")]

@icon("kelp", CAT, "Tall wavy underwater stalks with long ribbon blades and small round air bladders",
      tags=["kelp", "seaweed", "algae", "underwater", "ocean", "sea forest"])
def _(S):
    return [line("M8 21.5C4.5 17 11.5 14 8 9.5C5.5 6.5 8 4.5 9 2.5"),
            line("M16 21.5C19.5 18 12.5 15.5 16 11C18.5 8 16 5.5 15 3.5"),
            dot(11.3, 15, 1.4), dot(5, 11.5, 1.4), dot(13.2, 12.5, 1.4), dot(19, 13.5, 1.4), dot(11.5, 6.5, 1.3)]


@icon("moss", CAT, "Low rounded cushion of dense moss with tiny upright stalks on a rock",
      tags=["moss", "bryophyte", "rock", "damp", "woodland", "cushion"])
def _(S):
    mound = union("M3 21.5C3 17 6 15 12 15C18 15 21 17 21 21.5Z", blob((7.5, 14, 3.5), (12, 12.5, 4), (16.5, 14, 3.5)))
    return [shell(mound),
            line(seg(7.5, 9.5, 7, 7)), line(seg(12, 7.5, 12, 4.5)), line(seg(16.5, 9.5, 17, 7)),
            dot(8, 19, 0.9), dot(12.5, 18.5, 0.9), dot(16.5, 19.5, 0.9)]



# ============================================================================ chunk 4: moss, sap, herbs, seeds

@icon("spanish-moss", CAT, "Branch with long tangled strands of grey moss hanging down from it",
      tags=["spanish moss", "tillandsia", "air plant", "swamp", "louisiana", "hanging moss"])
def _(S):
    return [line(seg(2.5, 4, 21.5, 4)),
            line("M5.5 4C3.5 8 7.5 11 5.5 15C4.5 17.5 6 19 5.5 21"),
            line("M10 4C8 7 12 10 10 13C9 15 10.5 16 10 17.5"),
            line("M14.5 4C16.5 8 12.5 12 14.5 16C15.5 18.5 14 20 14.5 21.5"),
            line("M19 4C17.5 7 20.5 9 19 12")]


@icon("horsetail-plant", CAT, "Jointed upright stem with whorls of thin needle branches at each joint",
      tags=["horsetail", "equisetum", "scouring rush", "fern ally", "jointed stem", "primitive plant"])
def _(S):
    parts = [line(seg(12, 21.5, 12, 3))]
    for y in (16.5, 11, 5.5):
        w = 5 if y > 8 else 3.5
        parts += [line(seg(12, y, 12 - w, y - 3.2)), line(seg(12, y, 12 + w, y - 3.2))]
    return parts


@icon("rubber-tapping", CAT, "Tree trunk with a spiral cut groove draining latex into a small cup tied below",
      tags=["rubber tree", "latex", "tapping", "rubber plantation", "hevea", "natural rubber"])
def _(S):
    return [shell(rect(3.5, 2.5, 10, 19, L(S, 0, 2))),
            detail(poly([(3.5, 7.5), (13.5, 12)], r=0)),
            line(seg(13.5, 12, 18.5, 12)), solid(circle(18.5, 15, 1.2)),
            shell(poly([(15.5, 17.5), (21.5, 17.5), (20.5, 21.5), (16.5, 21.5)], closed=True, r=S.r * 0.6))]


@icon("tree-sap", CAT, "Tree trunk with a spout tapped into it and a drop falling into a hanging bucket",
      tags=["sap", "maple syrup", "tapping", "tree sap", "spile", "bucket", "sugaring"])
def _(S):
    return [shell(rect(2.5, 2.5, 9, 19, L(S, 0, 2))),
            line(seg(11.5, 8, 15.5, 8)), solid(circle(16, 11, 1.3)),
            shell(poly([(13.5, 15), (21, 15), (19.8, 21.5), (14.7, 21.5)], closed=True, r=S.r * 0.6)),
            line("M14.5 15C14.5 12.5 20 12.5 20 15")]


@icon("avocado-sprout", CAT, "Avocado pit held by toothpicks on the rim of a glass of water with roots below and a shoot above",
      tags=["avocado", "sprout", "pit", "propagation", "toothpick", "water glass", "kitchen garden"])
def _(S):
    return [shell(rect(6.5, 13.5, 11, 8, L(S, 1, 2.5))),
            shell(L(S, "M12 5C8.3 5.5 8.3 14 12 14.5C15.7 14 15.7 5.5 12 5Z", "M12 5C8.5 5 8.5 14.5 12 14.5C15.5 14.5 15.5 5 12 5Z")),
            line(seg(3.5, 12.3, 8.3, 12.3)), line(seg(15.7, 12.3, 20.5, 12.3)),
            line("M10.5 16.5C10 18 11 19 10.5 20"), line("M13.5 16.5C14 18 13 19 13.5 20"),
            line(seg(12, 5, 12, 3)), solid(leaf_shape(12, 3.2, 8, 1.8, 1.0)), solid(leaf_shape(12, 3.2, 16, 1.8, 1.0))]

@icon("sod-roll", CAT, "Rolled-up strip of grass turf with its blades on the outside and soil layer visible at the end",
      tags=["sod", "turf", "lawn", "grass roll", "landscaping", "garden", "new lawn"])
def _(S):
    parts = [shell(union(circle(9.5, 13.5, 7), rect(9.5, 6.5, 11, 14, 0))),
             detail("M9.5 13.5a1.2 1.2 0 0 1 1.2-1.2a2.4 2.4 0 0 1 2.4 2.4a3.6 3.6 0 0 1-3.6 3.6")]
    for x in (12.5, 15.5, 18.5):
        parts.append(line(seg(x, 6.5, x + 0.5, 3.5)))
    return parts

@icon("mint-sprig", CAT, "Sprig with pairs of oval leaves with deep veins, largest at the bottom",
      tags=["mint", "spearmint", "peppermint", "herb", "sprig", "mojito", "kitchen garden"])
def _(S):
    return [line(seg(12, 21.5, 12, 3.5)),
            shell(leaf_shape(12, 18.5, 4.5, 14.5, 2.4)), shell(leaf_shape(12, 18.5, 19.5, 14.5, 2.4)),
            shell(leaf_shape(12, 12, 6, 7.5, 2.0)), shell(leaf_shape(12, 12, 18, 7.5, 2.0)),
            shell(leaf_shape(12, 6.5, 12, 2.5, 1.3)),
            detail(seg(11, 17.6, 7.5, 15.6)), detail(seg(13, 17.6, 16.5, 15.6))]


@icon("sage-plant", CAT, "Stem with elongated oval leaves covered in a pebbly dotted texture",
      tags=["sage", "salvia", "herb", "culinary herb", "textured leaves", "kitchen garden"])
def _(S):
    return [line(seg(12, 21.5, 12, 4)),
            shell(leaf_shape(12, 20, 4.5, 12.5, 2.6)), shell(leaf_shape(12, 14.5, 19.5, 7.5, 2.6)),
            shell(leaf_shape(12, 9, 6.5, 3.5, 1.8)),
            dot(8.3, 15, 0.8), dot(6.8, 13.2, 0.8), dot(15.7, 9.5, 0.8), dot(17.2, 7.8, 0.8)]


@icon("ginseng-root", CAT, "Forked pale root with thin trailing root hairs and a small leafy stem on top",
      tags=["ginseng", "root", "herbal medicine", "panax", "tonic", "forked root"])
def _(S):
    body = poly([(9.5, 9), (14.5, 9), (14.8, 14), (17.5, 21.5), (14, 21), (12, 16), (10, 21), (6.5, 21.5), (9.2, 14)], closed=True, r=S.r * 0.8)
    return [shell(body), line(seg(12, 9, 12, 5)),
            shell(leaf_shape(12, 5.5, 7.5, 3, 1.1)), shell(leaf_shape(12, 5.5, 16.5, 3, 1.1)),
            line(seg(9, 12.5, 6, 12)), line(seg(15, 13, 18, 12.5))]

@icon("poison-ivy", CAT, "Three pointed glossy leaflets on one stalk, the middle one on a longer stem",
      tags=["poison ivy", "toxic plant", "rash", "leaves of three", "hiking", "allergy"])
def _(S):
    return [line(seg(12, 21.5, 12, 13)), line(seg(12, 13, 12, 10.5)),
            line(poly([(12, 16), (8.5, 14)], r=0)), line(poly([(12, 16), (15.5, 14)], r=0)),
            shell(leaf_shape(12, 10.5, 12, 2.5, 2.6)),
            shell(leaf_shape(8.5, 14, 2.5, 9.5, 2.3)), shell(leaf_shape(15.5, 14, 21.5, 9.5, 2.3)),
            detail(seg(12, 9, 12, 5))]


@icon("tulsi-plant", CAT, "Holy basil plant growing in a square pedestal planter with a raised base",
      tags=["tulsi", "holy basil", "ocimum", "hindu", "courtyard", "sacred plant", "india"])
def _(S):
    return [shell(rect(6, 12.5, 12, 9, L(S, 1, 2))), detail(seg(6, 15.5, 18, 15.5)),
            detail("M10 21.5V18.8C10 17.8 10.8 17.3 12 17.3C13.2 17.3 14 17.8 14 18.8V21.5"),
            line(seg(12, 12.5, 12, 5.5)),
            shell(leaf_shape(12, 10.5, 7, 8, 1.3)), shell(leaf_shape(12, 10.5, 17, 8, 1.3)),
            shell(leaf_shape(12, 6, 8.5, 2.8, 1.2)), shell(leaf_shape(12, 6, 15.5, 2.8, 1.2))]


def _almond(S, cx, cy, length, width, ang):
    if S.name == "line":
        d = leaf_shape(cx - length / 2, cy, cx + length / 2, cy, width / 2)
    else:
        d = ellipse(cx, cy, length / 2, width / 2)
    return rot(d, ang, cx, cy)


@icon("seed", CAT, "Single almond-shaped seed with a curved line along its seam",
      tags=["seed", "kernel", "grain", "sowing", "planting", "germination", "gardening"])
def _(S):
    return [shell(_almond(S, 12, 12, 17, 9, -45)),
            detail(rot("M6.5 12Q12 9.5 17.5 12", -45, 12, 12))]


@icon("germinating-seed", CAT, "Split seed coat with a small root curling down and a pale shoot rising with two first leaves",
      tags=["germination", "sprout", "seedling", "root", "shoot", "growth", "sprouting seed"])
def _(S):
    seed = poly([(6, 12.5), (7.5, 9.5), (12, 8.5), (16.5, 9.5), (18, 12.5), (15.5, 15.5), (8.5, 15.5)], closed=True, r=L(S, 1.4, 4))
    return [shell(seed), detail("M8.5 12.5Q12 10.5 15.5 12.5"),
            line("M11 15.5C11 18 13.5 19 13 21.5"),
            line(seg(12, 8.5, 12, 5)),
            shell(leaf_shape(12, 5.5, 6.5, 3, 1.2)), shell(leaf_shape(12, 5.5, 17.5, 3, 1.2))]

@icon("seed-anatomy", CAT, "Cut bean seed showing the outer coat, two halves of stored food and a tiny embryo plant inside",
      tags=["seed anatomy", "bean", "cotyledon", "embryo", "biology", "botany", "seed coat", "science class"])
def _(S):
    pts = [(3.5, 12), (5.5, 7), (12, 5.5), (18.5, 7), (20.5, 12), (18.5, 17), (12, 18.5), (5.5, 17)]
    return [shell(poly(pts, closed=True, r=L(S, 2, 6))),
            detail(seg(12, 7, 12, 10.5)), detail(seg(12, 14.5, 12, 17)),
            Part("dot", leaf_shape(12, 13, 8.5, 9.8, 1.0)), dot(14.8, 12.8, 1.0)]


# ============================================================================ chunk 5: seeds, leaves, roots, wood

@icon("maple-seed", CAT, "Pair of joined winged seeds spreading apart like a helicopter",
      tags=["maple seed", "samara", "helicopter seed", "whirligig", "winged seed", "tree seed", "spinning"])
def _(S):
    a = "M11.6 17L4.5 5.5C9 3.5 13 8 12.4 17Z"
    b = mirror(a)
    return [shell(union(a, b, circle(12, 18, 2.3)), stroke_miterlimit="8")]


@icon("milkweed-pod", CAT, "Open boat-shaped pod with fluffy silk-tailed seeds spilling out",
      tags=["milkweed", "seed pod", "silk", "fluff", "monarch", "asclepias", "seed dispersal"])
def _(S):
    boat = L(S, "M3 14C6 20 15 20.5 21 11C15 14.5 8 14.5 3 14Z",
             "M4.5 14.6Q3 14.3 3.6 15.6C6.6 20.4 15 20.2 20.5 12.4Q21 11.4 19.8 11.9C14.6 14.6 8.6 14.8 4.5 14.6Z")
    return [shell(boat),
            line("M8.5 13C8 9 6 7 5 4.5"), line("M12 13.5C12 9 12.5 6 12 2.5"), line("M16 12.5C16.5 9 18 7 19 4.5"),
            dot(8.5, 12.3, 1.3), dot(12, 12.6, 1.3), dot(16, 11.8, 1.3)]


@icon("poppy-seed-head", CAT, "Round capsule with a flat ribbed star-shaped crown on top of a stem",
      tags=["poppy", "seed head", "capsule", "poppy seed", "opium poppy", "dried flower", "baking"])
def _(S):
    body = L(S, "M7 8.5C4.5 14 7.5 19 12 19C16.5 19 19.5 14 17 8.5Z",
             "M7 8.5C4.5 14 7.5 19 12 19C16.5 19 19.5 14 17 8.5Z")
    return [shell(body), shell(ellipse(12, 7.5, 6.5, 2.3)),
            detail(seg(12, 11, 12, 17)), detail("M9 11.5C8.5 13.5 9 15 10 16.5"), detail("M15 11.5C15.5 13.5 15 15 14 16.5"),
            line(seg(12, 19, 12, 21.5))]


@icon("physalis", CAT, "Papery lantern-shaped husk with ribs and a round berry glowing inside",
      tags=["physalis", "chinese lantern", "cape gooseberry", "ground cherry", "husk", "autumn", "lantern plant"])
def _(S):
    return [line(seg(12, 1.5, 12, 4)), shell(leaf_shape(12, 4, 12, 21, 6.4), stroke_miterlimit="8"),
            detail("M12 6.5C8.3 9.5 8.3 15.5 12 18.5"), detail("M12 6.5C15.7 9.5 15.7 15.5 12 18.5"),
            dot(12, 12.5, 1.5)]

def _zig(cx, y0, y1, hw, n, inset=1.0):
    """Caterpillar-like outline with n bumps on each side (sharp notches)."""
    pts = []
    step = (y1 - y0) / n
    for i in range(n):
        pts.append((cx + hw, y0 + step * (i + .5)))
        pts.append((cx + hw - inset, y0 + step * (i + 1)))
    for i in range(n - 1, -1, -1):
        pts.append((cx - hw + inset, y0 + step * (i + 1)))
        pts.append((cx - hw, y0 + step * (i + .5)))
    return pts


def _catkin(S, cx, y0, y1, hw):
    if S.name == "line":
        return poly(_zig(cx, y0, y1, hw, 3, 0.9), closed=True, r=0)
    return blob(*[(cx, y0 + hw + k * (y1 - y0 - 2 * hw) / 3, hw) for k in range(4)])


@icon("catkin", CAT, "Dangling fuzzy caterpillar-like flower spikes hanging from a twig",
      tags=["catkin", "willow", "hazel", "birch", "pussy willow", "spring", "flower spike"])
def _(S):
    return [line(seg(2.5, 4, 21.5, 4)),
            line(seg(8, 4, 8, 6)), shell(_catkin(S, 8, 6, 20, 2.4)),
            line(seg(16, 4, 16, 6)), shell(_catkin(S, 16, 6, 16, 2.4))]


@icon("holly", CAT, "Two glossy spiky-edged holly leaves with a cluster of three round berries",
      tags=["holly", "christmas", "berries", "evergreen", "winter", "yuletide", "ilex"])
def _(S):
    r = L(S, 0, 0.4)
    return [shell(serrated(12, 14.5, 3.5, 6.5, 3.0, 3, 1.5, r), stroke_miterlimit="8"),
            shell(serrated(12, 14.5, 20.5, 6.5, 3.0, 3, 1.5, r), stroke_miterlimit="8"),
            dot(12, 15.5, 1.8), dot(9.3, 18.7, 1.8), dot(14.7, 18.7, 1.8)]


@icon("mistletoe", CAT, "Sprig of forked stems with paired smooth oval leaves and small round berries",
      tags=["mistletoe", "christmas", "kiss", "parasitic plant", "holiday", "berries", "winter"])
def _(S):
    return [line(poly([(12, 21.5), (12, 14.5), (6.5, 9.5)], r=S.r)), line(seg(12, 14.5, 17.5, 9.5)),
            shell(leaf_shape(6.5, 9.5, 2.8, 5.8, 1.5)), shell(leaf_shape(6.5, 9.5, 8.5, 3.4, 1.5)),
            shell(leaf_shape(17.5, 9.5, 21.2, 5.8, 1.5)), shell(leaf_shape(17.5, 9.5, 15.5, 3.4, 1.5)),
            dot(9.6, 16.5, 1.4), dot(14.4, 16.5, 1.4), dot(12, 12.3, 1.4)]


@icon("cedar-sprig", CAT, "Flat fan-shaped spray of branching scale-covered fronds",
      tags=["cedar", "thuja", "cypress", "conifer", "evergreen", "frond", "foliage"])
def _(S):
    cx, cy = 12, 20.5
    leaves = [(17, -90), (16, -115), (16, -65), (13.5, -140), (13.5, -40)]
    fan = union(*[leaf_shape(cx, cy, *polar(cx, cy, ln, a), 2.2) for ln, a in leaves])
    parts = [shell(fan, stroke_miterlimit="8")]
    for ln, a in leaves:
        parts.append(detail(seg(*polar(cx, cy, 4, a), *polar(cx, cy, ln * 0.72, a))))
    return parts


@icon("taproot", CAT, "Single thick tapering main root pointing down with a few thin side roots, stem and leaves above",
      tags=["taproot", "main root", "carrot", "dandelion", "root system", "botany", "underground"])
def _(S):
    root = poly(taper((12, 9.5), (12, 14), (12, 16.5), (12.4, 20.5), 6.6), closed=True, r=S.r * 0.5)
    return [ground(2.5, 21.5, 9.5), shell(root),
            line(seg(12, 9.5, 12, 5.5)), shell(leaf_shape(12, 6.3, 7, 3, 1.4)), shell(leaf_shape(12, 6.3, 17, 3, 1.4)),
            line(seg(9.3, 13, 5.5, 14.5)), line(seg(14.7, 15, 18.5, 16.5)), line(seg(10.6, 17.5, 8, 19.5))]

@icon("fibrous-roots", CAT, "Short stem with a dense tangle of many thin roots of similar size spreading downward",
      tags=["fibrous roots", "root system", "grass roots", "botany", "underground", "roots"])
def _(S):
    parts = [ground(2.5, 21.5, 8.5), line(seg(12, 8.5, 12, 4.5)),
             solid(leaf_shape(12, 5.5, 7.5, 2.8, 1.2)), solid(leaf_shape(12, 5.5, 16.5, 2.8, 1.2))]
    for tx, cx in ((4, 5), (8, 8), (12, 12), (16, 16), (20, 19)):
        parts.append(line(f"M12 8.5C{cx} 13 {tx} 15 {tx} 21"))
    parts += [line(seg(6.3, 14.8, 3.5, 15.8)), line(seg(17.7, 14.8, 20.5, 15.8))]
    return parts


@icon("root-ball", CAT, "Plant lifted out of a pot showing a pot-shaped mass of soil wrapped in circling roots",
      tags=["root ball", "rootbound", "repotting", "transplant", "potted plant", "roots", "gardening"])
def _(S):
    body = L(S, "M6.5 10.5H17.5Q18 16 15.5 19.5Q13.8 21.5 12 21.5Q10.2 21.5 8.5 19.5Q6 16 6.5 10.5Z",
             "M8.5 10.5H15.5Q17.5 10.5 17.6 12.5Q17.8 16.5 15.5 19.5Q13.8 21.5 12 21.5Q10.2 21.5 8.5 19.5Q6.2 16.5 6.4 12.5Q6.5 10.5 8.5 10.5Z")
    return [shell(body),
            detail("M7.2 14Q12 17 16.8 14"), detail("M9 17.6Q12 19.8 15 17.6"),
            line(seg(12, 10.5, 12, 6.5)),
            shell(leaf_shape(12, 7.5, 6.5, 3.2, 1.5)), shell(leaf_shape(12, 7.5, 17.5, 3.2, 1.5))]

@icon("rhizome", CAT, "Thick knobby horizontal underground stem with shoots rising up and roots growing down",
      tags=["rhizome", "ginger", "iris", "underground stem", "botany", "spreading", "root stock"])
def _(S):
    body = blob((5.5, 15, 3.2), (10, 13.8, 3.6), (14.8, 14.6, 3.4), (19, 13.2, 2.8))
    return [shell(body),
            line(seg(10, 10.5, 10, 5.5)), solid(leaf_shape(10, 6.5, 10, 2.5, 1.2)),
            line(seg(18.5, 10.8, 18.5, 6)), solid(leaf_shape(18.5, 7, 18.5, 3, 1.2)),
            line(seg(5.5, 18, 4.5, 21.5)), line(seg(12.5, 17.5, 12.5, 21.5)), line(seg(17, 17.5, 18.5, 21.5))]

@icon("flower-bulb", CAT, "Onion-shaped bulb with a pointed sprouting tip and a tuft of roots at its flat base",
      tags=["bulb", "flower bulb", "tulip bulb", "daffodil", "planting", "autumn planting", "garden"])
def _(S):
    bulb = L(S, "M12 2.5C13.5 6 19.5 9 19.5 14C19.5 17.5 16 19 12 19C8 19 4.5 17.5 4.5 14C4.5 9 10.5 6 12 2.5Z",
             "M12.2 3.4C13.6 6.4 19.5 9 19.5 14C19.5 17.5 16 19 12 19C8 19 4.5 17.5 4.5 14C4.5 9 10.4 6.4 11.8 3.4Q12 3 12.2 3.4Z")
    return [shell(bulb, stroke_miterlimit="8"), detail("M12 7.5C9.5 10 9 13 10 16"), detail("M12 7.5C14.5 10 15 13 14 16"),
            line(seg(9, 19, 8, 21.5)), line(seg(12, 19, 12, 21.5)), line(seg(15, 19, 16, 21.5))]


@icon("tree-bark", CAT, "Square patch of rough bark with deep vertical ridges and furrows",
      tags=["bark", "tree bark", "texture", "trunk", "wood", "rough", "furrows"])
def _(S):
    return [shell(rect(3, 3, 18, 18, L(S, 1.5, 4))),
            detail("M8 3.5C6.8 8 9.3 13 8 20.5"), detail("M12.5 3.5C11.2 9 14 14 12.5 20.5"), detail("M17 3.5C16 8 18 14 16.8 20.5")]


@icon("wood-log", CAT, "Horizontal log with bark along its side and growth rings on its cut end",
      tags=["log", "firewood", "timber", "lumber", "tree trunk", "growth rings", "wood"])
def _(S):
    return [shell(rect(2.5, 6.5, 14, 12, L(S, 1.5, 3))),
            shell(ellipse(16.5, 12.5, 4, 6)),
            detail(ellipse(16.5, 12.5, 1.3, 2.3)) if False else dot(16.5, 12.5, 1.1),
            detail("M5.5 10Q8 9 11 10"), detail("M5 15Q8.5 16.3 12 15")]


@icon("log-pile", CAT, "Stack of cut logs in a pyramid seen from the end, showing round ring faces",
      tags=["log pile", "woodpile", "firewood", "stacked logs", "timber", "lumber", "forestry"])
def _(S):
    def lg(x, y):
        return poly(regular(x, y, 3.4, 10), closed=True, r=0) if S.name == "line" else circle(x, y, 3.4)
    pos = [(6, 18), (12, 18), (18, 18), (9, 12.3), (15, 12.3), (12, 6.6)]
    return [shell(lg(x, y)) for x, y in pos] + [dot(x, y, 0.9) for x, y in pos]


@icon("thorn", CAT, "Stem with several sharp curved thorns pointing along it",
      tags=["thorn", "prickle", "spike", "rose stem", "sharp", "bramble", "thorny"])
def _(S):
    def th(x, y, sx, dy):
        return solid(poly(taper((x, y), (x + sx * 2, y - dy * .2), (x + sx * 4, y - dy * .6), (x + sx * 6, y - dy * 1.2), 3.4, power=0.9), closed=True))
    return [line("M12 2.5C10.5 8 13.5 14 12 21.5"),
            th(11.4, 8.2, -1, 2.2), th(12.6, 13.2, 1, 2.4), th(11.4, 18.6, -1, 2.2)]


@icon("tendril", CAT, "Thin stem ending in a tight coiled spiral tendril wrapping around a support",
      tags=["tendril", "climbing plant", "coil", "spiral", "vine", "pea plant", "grapevine"])
def _(S):
    return [line("M3.5 21C3.5 14.5 9 12.5 12.5 12.5C16.3 12.5 18 9.8 16.5 7.6C15 5.5 11.5 6.6 12 9C12.3 10.6 14.6 10.6 14.6 9"),
            line(seg(20.5, 2.5, 20.5, 21.5))]


@icon("stamen", CAT, "Thin filament stalk topped by a two-lobed anther head dusted with pollen dots",
      tags=["stamen", "anther", "pollen", "flower anatomy", "botany", "filament", "reproduction"])
def _(S):
    lobe = lambda cx: L(S, leaf_shape(cx, 11.5, cx, 3.5, 2.6), ellipse(cx, 7.5, 2.6, 4.2))
    return [line(seg(12, 21.5, 12, 11.5)), shell(union(lobe(9.6), lobe(14.4)), stroke_miterlimit="8"),
            dot(5, 6, 0.9), dot(19, 6, 0.9), dot(6, 10.5, 0.9), dot(18, 10.5, 0.9)]
