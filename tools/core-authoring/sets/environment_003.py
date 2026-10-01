"""TypeIcon Core: environment (batch 003).

Recycling and waste, reuse and low-waste living, renewable energy at home, saving energy and water,
green buildings and cities, local food and nature protection.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, LINE, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "environment"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def strokes(d, w=1.0):
    return path_to_d(ST(d, w, "butt", "miter"))


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled body."""
    return Part("dot", d)


def grow(d, g):
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def cut_lines(S, ds, cutter, gap=2.0, w=2.0):
    """Stroke outlines of ds minus the grown cutter region: something seen behind another thing."""
    body = U(*[ST(d, w, S.cap, S.join) for d in ds])
    return solid(path_to_d(D(body, P(grow(cutter, gap)))))


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def flip(d):
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def P2(p):
    return f"{fmt(p[0])} {fmt(p[1])}"


def head_pts(tip, deg, size=3.2, spread=42):
    """Two wing points of an arrow head whose tip is at `tip` and points along `deg`."""
    return (polar(*tip, size, deg + 180 - spread), polar(*tip, size, deg + 180 + spread))


def arrow_head(S, tip, deg, size=3.2, spread=42):
    a, b = head_pts(tip, deg, size, spread)
    return line(poly([a, tip, b], r=S.r * 0.5))


def arc_arrow(S, cx, cy, r, a0, a1, size=3.2):
    """Clockwise arc with an arrow head at its end: list of parts."""
    end = polar(cx, cy, r, a1)
    return [line(arc(cx, cy, r, a0, a1)), arrow_head(S, end, a1 + 90, size)]


def loop_arrows(S, cx, cy, r, size=3.2, gap=34, start=-90 + 0):
    """Two chasing arrows around a circle (clockwise), each ~146 degrees long."""
    span = 180 - gap
    parts = []
    for k in range(2):
        a0 = start + gap / 2 + k * 180
        parts += arc_arrow(S, cx, cy, r, a0, a0 + span, size)
    return parts


def leaf_d(x1, y1, x2, y2, w):
    """Leaf outline from base (x1, y1) to tip (x2, y2); w is the bulge."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    nx, ny = -dy / n, dx / n
    c1 = (mx + nx * w, my + ny * w)
    c2 = (mx - nx * w, my - ny * w)
    return f"M{P2((x1, y1))}Q{P2(c1)} {P2((x2, y2))}Q{P2(c2)} {P2((x1, y1))}Z"


def leaf(S, x1, y1, x2, y2, w=4.4, rib=True):
    """Leaf shell with a midrib detail (list of parts). Rounded gets a slightly fuller leaf."""
    w = w * L(S, 1.0, 1.12)
    d = leaf_d(x1, y1, x2, y2, w)
    parts = [shell(d)]
    if rib:
        t = 0.25
        a = (x1 + (x2 - x1) * 0.0, y1 + (y2 - y1) * 0.0)
        b = (x1 + (x2 - x1) * 0.62, y1 + (y2 - y1) * 0.62)
        parts.append(detail(seg(*a, *b)))
    return parts


def bottle_solid(cx, top, h=8.5, w=4.0, neck=1.6):
    """Bottle silhouette (for marks)."""
    nb = top + h * 0.38
    pts = [(cx - neck / 2, top), (cx + neck / 2, top), (cx + neck / 2, top + h * 0.22), (cx + w / 2, nb),
           (cx + w / 2, top + h), (cx - w / 2, top + h), (cx - w / 2, nb), (cx - neck / 2, top + h * 0.22)]
    return poly(pts, closed=True)


# digits drawn as thin solid strokes (1.5 px) for the recycling code triangles
_DIGITS = {
    1: [[(-1.3, -2.2), (0.4, -3.2), (0.4, 3.2)]],
    2: [[(-1.9, -1.6), (-1, -3), (1, -3), (1.9, -1.8), (1.9, -0.6), (-1.9, 3.1), (2, 3.1)]],
    3: [[(-1.9, -3), (1.9, -3), (-0.1, -0.4)], [(-0.1, -0.4), (1.2, 0.1), (1.9, 1.2), (1.9, 1.9), (1, 3), (-1, 3), (-1.9, 2.2)]],
    4: [[(1.1, 3.2), (1.1, -3.2), (-2, 1.3), (2.2, 1.3)]],
    5: [[(1.9, -3), (-1.5, -3), (-1.8, -0.4), (0.3, -0.7), (1.6, 0.3), (1.9, 1.6), (1.1, 2.9), (-0.6, 3.1), (-1.9, 2.4)]],
    6: [[(1.4, -3), (-0.6, -3), (-1.9, -1.5), (-1.9, 1.6), (-1, 3), (1, 3), (1.9, 1.8), (1, 0.3), (-0.6, 0.3), (-1.9, 1.3)]],
    7: [[(-1.9, -3), (1.9, -3), (-0.6, 3.2)]],
}


def digit(n, cx, cy, s=1.0, w=1.5):
    ds = []
    for stroke in _DIGITS[n]:
        pts = [(cx + x * s, cy + y * s) for x, y in stroke]
        ds.append(ST(poly(pts), w, "round", "round"))
    return solid(path_to_d(U(*ds)))


# ============================================================================ recycling codes

def _chasing_triangle(S):
    """Three bent arrows chasing round a triangle. Returns parts."""
    A, B, C = (12, 3.6), (21.4, 19.8), (2.6, 19.8)
    V = [A, B, C]
    parts = []

    def lerp(p, q, t):
        return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    for k in range(3):
        p, q, r = V[k], V[(k + 1) % 3], V[(k + 2) % 3]
        start = lerp(p, q, 0.5)
        end = lerp(q, r, 0.36)
        parts.append(line(poly([start, q, end], r=L(S, 0.8, 2.6))))
        dx, dy = r[0] - q[0], r[1] - q[1]
        parts.append(arrow_head(S, end, math.degrees(math.atan2(dy, dx)), 3.0, 40))
    return parts


def _code_icon(n):
    def draw(S):
        return [*_chasing_triangle(S), digit(n, 12, 14.6, 0.95)]
    return draw


for _n, _nm, _desc, _tags in [
    (1, "pet", "Chasing arrows triangle with the number 1 inside.",
     ["recycling code 1", "pet", "plastic", "bottle plastic", "resin code", "recycle"]),
    (2, "hdpe", "Chasing arrows triangle with the number 2 inside.",
     ["recycling code 2", "hdpe", "plastic", "milk jug", "resin code", "recycle"]),
    (3, "pvc", "Chasing arrows triangle with the number 3 inside.",
     ["recycling code 3", "pvc", "vinyl", "plastic", "resin code", "recycle"]),
    (4, "ldpe", "Chasing arrows triangle with the number 4 inside.",
     ["recycling code 4", "ldpe", "plastic film", "plastic bag", "resin code", "recycle"]),
    (5, "pp", "Chasing arrows triangle with the number 5 inside.",
     ["recycling code 5", "polypropylene", "plastic", "resin code", "recycle"]),
    (6, "ps", "Chasing arrows triangle with the number 6 inside.",
     ["recycling code 6", "polystyrene", "foam", "plastic", "resin code", "recycle"]),
    (7, "other", "Chasing arrows triangle with the number 7 inside.",
     ["recycling code 7", "other plastic", "mixed plastic", "resin code", "recycle"]),
]:
    icon(f"recycle-code-{_nm}", CAT, _desc, tags=_tags)(_code_icon(_n))


# ============================================================================ sorted recycling

def _bank(S, inner_marks, body_top=3.0):
    return shell(rect(5, body_top, 14, 21 - body_top, S.R))


@icon("glass-recycling", CAT, "Recycling bin with a round opening and a bottle on its front.",
      tags=["glass recycling", "bottle bank", "glass bin", "recycle glass", "bottle", "bin", "waste"])
def _(S):
    return [shell(rect(5, 3, 14, 18, S.R)), dot(12, 7.5, 1.9), mark(bottle_solid(12, 11.2, 8.3, 4.0, 1.7))]


@icon("paper-recycling", CAT, "Recycling bin with a slot opening and a folded newspaper on its front.",
      tags=["paper recycling", "paper bin", "newspaper", "recycle paper", "cardboard", "bin", "waste"])
def _(S):
    paper = minus(rect(8.25, 11, 7.5, 8.2, 0.6), strokes(seg(9.6, 14.3, 14.4, 14.3), 1.0),
                  strokes(seg(9.6, 16.5, 14.4, 16.5), 1.0))
    return [shell(rect(5, 3, 14, 18, S.R)), mark(rect(8, 6.4, 8, 1.8, 0.9)), mark(paper)]


@icon("metal-recycling", CAT, "Recycling bin with a round opening and a tin can on its front.",
      tags=["metal recycling", "can bin", "tin can", "aluminium can", "aluminum", "recycle metal", "bin", "waste"])
def _(S):
    can = minus(rect(9.1, 10.8, 5.8, 8.4, 0.8), strokes(seg(8.5, 12.7, 15.5, 12.7), 0.9),
                strokes(seg(8.5, 17.3, 15.5, 17.3), 0.9))
    return [shell(rect(5, 3, 14, 18, S.R)), dot(12, 7.5, 1.9), mark(can)]


@icon("plastic-recycling", CAT, "Wheeled recycling bin with a lid and a plastic bottle on its front.",
      tags=["plastic recycling", "plastic bin", "plastic bottle", "recycle plastic", "bottle", "bin", "waste"])
def _(S):
    pb = minus(bottle_solid(12, 10.2, 9.6, 5.0, 2.2), strokes(seg(8, 15.6, 16, 15.6), 0.9))
    return [shell(poly([(4.5, 7), (19.5, 7), (18.5, 21), (5.5, 21)], closed=True, r=S.r)),
            shell(rect(3, 3, 18, 4, L(S, 0.6, 1.8))),
            mark(pb)]


# ============================================================================ recycling loops

@icon("battery-recycling", CAT, "Battery inside a loop of two chasing arrows.",
      tags=["battery recycling", "recycle batteries", "battery disposal", "used battery", "chasing arrows", "waste"])
def _(S):
    return [*loop_arrows(S, 12, 12, 9, 3.0, 38, -90 + 10),
            shell(rect(9, 8.5, 6, 8.5, L(S, 0.6, 1.6))), line(seg(11, 6.6, 13, 6.6)), detail(seg(12, 11.2, 12, 14.4))]


@icon("e-waste-recycling", CAT, "Smartphone inside a loop of two chasing arrows.",
      tags=["e-waste", "electronic waste", "phone recycling", "recycle electronics", "chasing arrows", "gadget"])
def _(S):
    return [*loop_arrows(S, 12, 12, 9, 3.0, 38, -90 + 10),
            shell(rect(9, 7.5, 6, 9, L(S, 0.6, 1.6))), dot(12, 14.2, 0.9)]


@icon("textile-recycling", CAT, "T-shirt inside a loop of two chasing arrows.",
      tags=["textile recycling", "clothes recycling", "recycle clothes", "fabric waste", "t-shirt", "clothing", "chasing arrows"])
def _(S):
    tee = poly([(9.3, 7.4), (6.6, 8.9), (7.6, 11.8), (9.3, 11.1), (9.3, 16.4), (14.7, 16.4), (14.7, 11.1), (16.4, 11.8),
                (17.4, 8.9), (14.7, 7.4), (13.2, 8.6), (10.8, 8.6)], closed=True, r=S.r * 0.4)
    return [*loop_arrows(S, 12, 12, 9, 3.0, 38, -90 + 10), solid(tee)]


@icon("clothing-donation-bin", CAT, "Tall clothing collection container with a chute and a shirt mark on its front.",
      tags=["clothing bank", "donation bin", "clothes donation", "charity bin", "textile bank", "donate clothes", "container"])
def _(S):
    tee = poly([(9.5, 13), (7.5, 14), (8.3, 16.5), (9.5, 16), (9.5, 19.5), (14.5, 19.5), (14.5, 16), (15.7, 16.5), (16.5, 14), (14.5, 13)], closed=True)
    return [shell(poly([(4.5, 6.5), (12, 3), (19.5, 6.5), (19.5, 21), (4.5, 21)], closed=True, r=S.r)),
            detail(seg(4.5, 9.5, 19.5, 9.5)), mark(tee)]


@icon("reverse-vending-machine", CAT, "Bottle return machine with a bottle being pushed into its slot and a receipt slot below.",
      tags=["bottle return", "reverse vending", "deposit machine", "bottle recycling machine", "refund", "can return", "kiosk"])
def _(S):
    return [shell(rect(12.5, 2.5, 9, 19, S.R)), mark(rect(15, 10.5, 4.5, 3, 1.2)), mark(rect(15, 17, 4.5, 1.6, 0.8)),
            detail(seg(15, 6, 19.5, 6)),
            shell(rect(2.5, 9, 5, 6, L(S, 0.6, 2))), line(seg(7.5, 12, 9.4, 12))]


@icon("deposit-return", CAT, "Bottle with a coin and a circular arrow beside it.",
      tags=["bottle deposit", "deposit refund", "bottle refund", "container deposit", "return bottles", "coin", "refund"])
def _(S):
    bottle = poly([(6.5, 2.5), (9.5, 2.5), (9.5, 6), (11.5, 9), (11.5, 21), (3.5, 21), (3.5, 9), (6.5, 6)], closed=True, r=L(S, 0, 1.2))
    return [shell(bottle), shell(circle(17.5, 7, 3.6)), dot(17.5, 7, 1.0),
            *arc_arrow(S, 17.5, 16.5, 3.6, 150, 440, 2.8)]


def rot_pts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def leaf_solid(x1, y1, x2, y2, w, rib=0.9):
    d = leaf_d(x1, y1, x2, y2, w)
    if not rib:
        return d
    a = (x1 + (x2 - x1) * 0.12, y1 + (y2 - y1) * 0.12)
    b = (x1 + (x2 - x1) * 0.7, y1 + (y2 - y1) * 0.7)
    return minus(d, strokes(seg(*a, *b), rib))


# ============================================================================ compost and waste reduction

@icon("food-waste", CAT, "Apple core with a stem dropped into a small bin.",
      tags=["food waste", "food scraps", "kitchen waste", "apple core", "organic waste", "leftovers", "compost"])
def _(S):
    core = L(S, "M8.2 6.4A3.8 2.4 0 0 1 15.8 6.4Q13.4 8.8 15.8 11.2A3.8 2.4 0 0 1 8.2 11.2Q10.6 8.8 8.2 6.4Z",
             "M8.2 6.4A3.8 2.4 0 0 1 15.8 6.4Q13.6 8.8 15.8 11.2A3.8 2.4 0 0 1 8.2 11.2Q10.4 8.8 8.2 6.4Z")
    return [shell(core), line("M12 4V1.8"), shell(poly([(4, 16.2), (20, 16.2), (18.5, 21.8), (5.5, 21.8)], closed=True, r=S.r))]


@icon("zero-waste", CAT, "Glass jar with a lid and a zero on its front.",
      tags=["zero waste", "no waste", "waste free", "low waste", "mason jar", "jar", "sustainable living"])
def _(S):
    jar = poly([(8, 2.5), (16, 2.5), (16, 5.5), (19.5, 8), (19.5, 21), (4.5, 21), (4.5, 8), (8, 5.5)], closed=True, r=S.r)
    return [shell(jar), detail(seg(8, 5.5, 16, 5.5)), detail(ellipse(12, 14.4, 2.3, 3.4))]


@icon("reusable-bag", CAT, "Cloth tote bag with long handles and a leaf printed on it.",
      tags=["tote bag", "cloth bag", "reusable bag", "shopping bag", "eco bag", "canvas bag", "plastic free"])
def _(S):
    body = poly([(4.5, 9), (19.5, 9), (20.5, 21.5), (3.5, 21.5)], closed=True, r=S.r)
    return [line("M8.5 9C8.5 1.5 15.5 1.5 15.5 9"), shell(body),
            mark(leaf_solid(9.3, 19, 14.7, 12.6, 2.3))]


@icon("reusable-cup", CAT, "Takeaway cup with a sleeve band and a sip lid.",
      tags=["reusable cup", "coffee cup", "travel mug", "keep cup", "takeaway cup", "to go cup", "zero waste"])
def _(S):
    cup = poly([(9, 2.5), (15, 2.5), (15, 5), (19, 5), (19, 8), (17.8, 8), (16.5, 21.5), (7.5, 21.5), (6.2, 8), (5, 8), (5, 5), (9, 5)],
               closed=True, r=S.r)
    return [shell(cup), detail(seg(6.6, 12, 17.4, 12)), detail(seg(7, 17, 17, 17))]


@icon("bamboo-toothbrush", CAT, "Toothbrush with a row of bristles and a segmented bamboo handle.",
      tags=["bamboo toothbrush", "eco toothbrush", "plastic free", "wooden toothbrush", "dental care", "zero waste", "brush teeth"])
def _(S):
    deg = 45

    def R(pts):
        return rot_pts(pts, deg)
    hd = poly(R([(8.6, 6), (15.4, 6), (15.4, 12), (14.2, 13.2), (14.2, 22), (9.8, 22), (9.8, 13.2), (8.6, 12)]), closed=True, r=S.r)
    tufts = [solid(poly(R([(x, 2), (x + 1.4, 2), (x + 1.4, 4.2), (x, 4.2)]), closed=True)) for x in (8.75, 11.3, 13.85)]
    ns = [detail(seg(*R([(10.8, y)])[0], *R([(13.2, y)])[0])) for y in (16.4, 19.4)]
    return [shell(hd), *tufts, *ns]


@icon("beeswax-wrap", CAT, "Square cloth wrap with a folded corner, printed with honeycomb hexagons.",
      tags=["beeswax wrap", "food wrap", "reusable wrap", "cling film alternative", "plastic free", "cloth", "honeycomb"])
def _(S):
    sheet = poly([(3.5, 3), (20.5, 3), (20.5, 14.5), (14.5, 20.5), (3.5, 20.5)], closed=True, r=S.r)
    fold = poly([(20.5, 14.5), (14.5, 14.5), (14.5, 20.5)], closed=True, r=S.r * 0.5)
    hx = [mark(poly(regular(x, y, 1.75, 6, -90), closed=True)) for x, y in ((8.2, 7.6), (12.6, 7.6), (10.4, 11.4))]
    return [shell(sheet), detail(fold), *hx]


@icon("bulk-food-jars", CAT, "Two wide glass storage jars with lids, filled with grains.",
      tags=["bulk food", "refill store", "dry goods", "storage jars", "pantry", "zero waste shop", "grains"])
def _(S):
    def jar(x0):
        return poly([(x0 + 1, 3.5), (x0 + 8, 3.5), (x0 + 8, 6.5), (x0 + 9, 8), (x0 + 9, 21.5), (x0, 21.5), (x0, 8), (x0 + 1, 6.5)],
                    closed=True, r=S.r)
    return [shell(jar(2)), shell(jar(13)), detail(seg(3, 6.5, 10, 6.5)), detail(seg(14, 6.5, 21, 6.5)),
            detail(seg(3.6, 13, 9.4, 13)), detail(seg(14.6, 16, 20.4, 16))]


@icon("metal-straw", CAT, "Bent drinking straw standing beside a thin cleaning brush.",
      tags=["metal straw", "reusable straw", "steel straw", "plastic free", "straw brush", "zero waste", "drinking straw"])
def _(S):
    straw = path_to_d(ST(poly([(6.5, 21), (6.5, 9), (11, 4)]), 3.6, "butt", "miter"))
    return [shell(straw, stroke_miterlimit="4"), line(seg(17.5, 21, 17.5, 3.5)),
            line(seg(14.6, 5, 20.4, 5)), line(seg(14.6, 9, 20.4, 9)), line(seg(14.6, 13, 20.4, 13))]


@icon("upcycling", CAT, "Tin can reused as a plant pot with a sprout growing from it.",
      tags=["upcycling", "upcycle", "reuse", "tin can planter", "diy planter", "repurpose", "can pot"])
def _(S):
    return [shell(rect(5.5, 12, 13, 9.5, L(S, 0.6, 2))), detail(seg(5.5, 15, 18.5, 15)),
            line(seg(12, 12, 12, 7)),
            solid(leaf_solid(12, 8.2, 5.2, 4, 2.6, 0)), solid(leaf_solid(12, 8.2, 18.8, 4, 2.6, 0))]


@icon("secondhand", CAT, "Clothes hanger inside a circular arrow loop.",
      tags=["secondhand", "second hand", "thrift", "preloved", "pre-owned", "vintage clothes", "resale", "hanger"])
def _(S):
    hang = poly([(6.6, 16.4), (12, 11.6), (17.4, 16.4)], closed=True, r=S.r * 0.6)
    return [*loop_arrows(S, 12, 12, 9.3, 3.0, 38, -90 + 10), line(hang), line("M12 11.6V10.2A1.6 1.6 0 1 0 10.4 8.6")]


@icon("circular-economy", CAT, "Three curved arrows forming a closed circle around a leaf.",
      tags=["circular economy", "closed loop", "regenerative", "sustainable", "reuse cycle", "cradle to cradle", "loop"])
def _(S):
    parts = []
    for k in range(3):
        a0 = -90 + 18 + k * 120
        parts += arc_arrow(S, 12, 12, 9, a0, a0 + 84, 3.0)
    return [*parts, solid(leaf_solid(9.2, 15, 14.8, 8.8, 2.8))]


def bolt_pts(cx, cy, s=1.0):
    return [(cx + 0.9 * s, cy - 3.2 * s), (cx - 2.1 * s, cy + 0.7 * s), (cx - 0.25 * s, cy + 0.7 * s), (cx - 0.9 * s, cy + 3.2 * s),
            (cx + 2.1 * s, cy - 0.7 * s), (cx + 0.25 * s, cy - 0.7 * s)]


def sun_rays(cx, cy, r0, r1, angles):
    return [line(seg(*polar(cx, cy, r0, a), *polar(cx, cy, r1, a))) for a in angles]


# ============================================================================ repair, packaging and sorting

@icon("repair-cafe", CAT, "Coffee mug holding a wrench and a pin-topped needle, like tools in a pot.",
      tags=["repair cafe", "repair shop", "fix it", "mending", "community repair", "coffee", "diy repair"])
def _(S):
    tip = (6.2, 5.2)
    ang = math.degrees(math.atan2(-6, -3))
    head = (tip[0] + math.cos(math.radians(ang)) * 1.0, tip[1] + math.sin(math.radians(ang)) * 1.0)
    return [
        line(seg(9.6, 12, *tip)), line(arc(head[0], head[1], 2.3, ang + 42, ang - 42 + 360)),
        line(seg(15, 12, 18.6, 4.6)), dot(18.8, 3.8, 1.5),
        shell(rect(4.5, 12, 12, 9.5, L(S, 0.6, 2.4))),
        line("M16.5 14.6H18.4A2.4 2.4 0 0 1 18.4 19.4H16.5"),
    ]


@icon("biodegradable", CAT, "Leaf above a dotted arrow pointing down to the ground.",
      tags=["biodegradable", "decomposes", "compostable", "breaks down", "natural", "eco friendly", "leaf"])
def _(S):
    return [*leaf(S, 7, 10.8, 17.5, 2.6, 3.8), dot(12, 13.2, 0.9), dot(12, 15.4, 0.9),
            arrow_head(S, (12, 19.3), 90, 3.4, 45), line(seg(4.5, 21.6, 19.5, 21.6))]


@icon("compostable-packaging", CAT, "Takeaway box with a sprout growing from its top.",
      tags=["compostable packaging", "biodegradable box", "eco packaging", "takeaway box", "plant based", "sprout", "green"])
def _(S):
    box = poly([(3.5, 11), (20.5, 11), (18.5, 21.5), (5.5, 21.5)], closed=True, r=S.r)
    return [shell(box), detail(seg(4.3, 14.4, 19.7, 14.4)), line(seg(12, 11, 12, 6.5)),
            solid(leaf_solid(12, 8.4, 5, 3.8, 2.8, 0)), solid(leaf_solid(12, 8.4, 19, 3.8, 2.8, 0))]


@icon("eco-label", CAT, "Scalloped seal badge with a leaf in its center.",
      tags=["eco label", "green certified", "eco friendly badge", "sustainability seal", "environment approved", "leaf", "stamp"])
def _(S):
    n = 16
    pts = []
    for i in range(n * 2):
        pts.append(polar(12, 12, 10 if i % 2 == 0 else 8.6, -90 + i * 180 / n))
    return [shell(poly(pts, closed=True, r=L(S, 0, 0.7))), solid(leaf_solid(8.4, 15.6, 15.6, 8.4, 3.6))]


@icon("sustainable-packaging", CAT, "Cardboard box with a leaf printed on its side.",
      tags=["sustainable packaging", "eco packaging", "cardboard box", "green shipping", "recyclable packaging", "leaf", "carton"])
def _(S):
    box = poly([(3, 4.5), (21, 4.5), (21, 9), (19.5, 9), (19.5, 21.5), (4.5, 21.5), (4.5, 9), (3, 9)], closed=True, r=S.r)
    return [shell(box), mark(leaf_solid(8.6, 19.2, 15.4, 11.6, 3.4))]


@icon("street-litter-bin", CAT, "Post-mounted public bin with a wide lid and a slot opening.",
      tags=["litter bin", "street bin", "public bin", "trash can", "park bin", "rubbish bin", "city"])
def _(S):
    body = poly([(4, 3), (20, 3), (20, 6.2), (18.6, 6.2), (17.6, 14.2), (6.4, 14.2), (5.4, 6.2), (4, 6.2)], closed=True, r=S.r * 0.6)
    return [shell(body), mark(rect(8, 8.4, 8, 3, 1.3)), line(seg(12, 14.2, 12, 21.5)), line(seg(8, 21.5, 16, 21.5))]


def sprout(cx, base, h=5.0, lw=2.4):
    """Stem with a pair of small solid leaves (list of parts)."""
    y = base - h
    return [line(seg(cx, base, cx, y + 0.8)), solid(leaf_solid(cx, y + 2.0, cx - lw - 0.6, y - 0.4, 1.3, 0)),
            solid(leaf_solid(cx, y + 2.0, cx + lw + 0.6, y - 0.4, 1.3, 0))]


# ============================================================================ renewable energy at home

@icon("solar-farm", CAT, "Two rows of tilted solar panels on open ground with a sun in the corner.",
      tags=["solar farm", "solar park", "photovoltaic array", "solar power plant", "renewable energy", "panels", "sun"])
def _(S):
    r1 = poly([(10.5, 8.2), (21, 8.2), (22, 12.8), (9.5, 12.8)], closed=True, r=S.r * 0.5)
    r2 = poly([(4.5, 15.6), (20.5, 15.6), (22, 21), (2.5, 21)], closed=True, r=S.r * 0.5)
    return [shell(r1), shell(r2), solid(circle(5.6, 5.6, 1.9)), *sun_rays(5.6, 5.6, 3.6, 5.0, (0, 45, 90))]


@icon("solar-charger", CAT, "Folding solar panel connected by a cable to a smartphone.",
      tags=["solar charger", "portable solar", "phone charger", "solar power bank", "camping", "panel", "cable"])
def _(S):
    return [shell(rect(2.5, 6.5, 11.5, 9, L(S, 0.6, 2))), detail(seg(8.25, 6.5, 8.25, 15.5)), detail(seg(2.5, 11, 14, 11)),
            shell(rect(17.2, 3.5, 4.8, 9.5, L(S, 0.6, 1.8))),
            line("M14 13.6H15.4V19.2H19.6V13")]


@icon("solar-street-light", CAT, "Street lamp post with a lamp head and a small tilted solar panel on top.",
      tags=["solar street light", "solar lamp", "street lamp", "outdoor lighting", "lamp post", "off grid light", "panel"])
def _(S):
    return [line(seg(8, 21.5, 8, 7)), line(seg(8, 7, 15, 7)),
            shell(poly([(13, 7), (21, 7), (19.3, 10.6), (14.7, 10.6)], closed=True, r=S.r * 0.4)),
            shell(poly([(2.5, 4.8), (10, 2.6), (11, 5.6), (3.5, 7.8)], closed=True, r=S.r * 0.4)),
            line(seg(15, 14, 15, 16.6)), line(seg(19.4, 14, 19.4, 16.6))]


@icon("solar-roof", CAT, "House roof covered with a grid of solar panel lines.",
      tags=["solar roof", "rooftop solar", "roof panels", "solar tiles", "home solar", "photovoltaic", "house"])
def _(S):
    roof = poly([(12, 3), (22, 15.5), (2, 15.5)], closed=True, r=S.r)
    return [shell(roof), detail(seg(8, 10.5, 16, 10.5)), detail(seg(12, 6.4, 12, 15.5)),
            line(seg(4.5, 21.2, 19.5, 21.2))]


@icon("small-wind-turbine", CAT, "Short three-blade wind turbine on a pole beside a house.",
      tags=["small wind turbine", "home wind", "micro wind", "backyard turbine", "renewable", "windmill", "house"])
def _(S):
    hub = (6.5, 8.2)
    blades = [line(seg(*hub, *polar(*hub, 5.2, a))) for a in (-90, 30, 150)]
    house = poly([(18.3, 10.5), (22.5, 14.8), (22.5, 21.5), (14, 21.5), (14, 14.8)], closed=True, r=S.r)
    return [*blades, dot(*hub, 1.4), line(seg(6.5, 9.5, 6.5, 21.5)), shell(house)]


@icon("micro-hydro", CAT, "Pipe running down a slope into a turbine box marked with a bolt.",
      tags=["micro hydro", "small hydropower", "stream power", "penstock", "water turbine", "renewable energy", "hydroelectric"])
def _(S):
    return [line(seg(2.8, 4.5, 11, 14.3)), line(seg(2.5, 21.5, 11, 21.5)),
            shell(rect(11.5, 11, 10.5, 10, L(S, 0.6, 2))), mark(poly(bolt_pts(16.75, 16, 1.0), closed=True))]


@icon("biomass", CAT, "Pile of three log ends beside a small flame.",
      tags=["biomass", "wood fuel", "firewood", "wood pellets", "bioenergy", "renewable heat", "logs"])
def _(S):
    logs = [shell(circle(5, 18.4, 2.6)), shell(circle(12.4, 18.4, 2.6)), shell(circle(8.7, 12, 2.6))]
    flame = ("M18.4 2.5C20.6 5.2 22 7.4 22 9.8A3.6 3.6 0 0 1 14.8 9.8C14.8 8.2 15.6 7.3 16.4 6.3C16.8 7.3 17.3 7.8 17.6 7.9C17.2 6 17.6 4.3 18.4 2.5Z")
    return [*logs, shell(flame), dot(18.4, 10.2, 0.9)]


@icon("renewable-energy", CAT, "Large leaf with a lightning bolt in the middle.",
      tags=["renewable energy", "green energy", "clean energy", "eco power", "sustainable electricity", "leaf", "bolt"])
def _(S):
    return [shell(leaf_d(4.5, 19.5, 19.5, 4.5, 7.4 * L(S, 1.0, 1.1))), mark(poly(bolt_pts(12, 12, 1.25), closed=True))]


def _letter_h(cx, cy, h=5.4, w=3.4, t=1.4):
    return union(rect(cx - w / 2, cy - h / 2, t, h), rect(cx + w / 2 - t, cy - h / 2, t, h), rect(cx - w / 2, cy - t / 2, w, t))


@icon("green-hydrogen", CAT, "Leaf beside a gas cylinder marked with the letter H.",
      tags=["green hydrogen", "hydrogen fuel", "clean hydrogen", "electrolysis", "gas bottle", "renewable fuel", "h2"])
def _(S):
    tank = poly([(13.8, 9.5), (13.8, 8.4), (15.2, 7), (19.8, 7), (21.2, 8.4), (21.2, 21.5), (13.8, 21.5)], closed=True, r=S.r * 0.5)
    return [*leaf(S, 2.5, 20, 11.5, 6, 3.6), shell(tank), line(seg(17.5, 7, 17.5, 3.8)), line(seg(15.6, 3.8, 19.4, 3.8)),
            mark(_letter_h(17.5, 14.6))]


def _house_sm(cx, top, S):
    return poly([(cx, top), (cx + 3.4, top + 2.8), (cx + 3.4, top + 6.4), (cx - 3.4, top + 6.4), (cx - 3.4, top + 2.8)], closed=True, r=S.r * 0.4)


@icon("micro-grid", CAT, "Three small houses joined by lines in a triangle.",
      tags=["micro grid", "microgrid", "local grid", "community energy", "distributed power", "neighborhood power", "houses"])
def _(S):
    return [shell(_house_sm(12, 2.6, S)), shell(_house_sm(5.3, 14.8, S)), shell(_house_sm(18.7, 14.8, S)),
            line(seg(10.6, 10.6, 7.4, 14.2)), line(seg(13.4, 10.6, 16.6, 14.2)), line(seg(10.4, 20, 13.6, 20))]


@icon("smart-grid", CAT, "Power pylon with linked network dots around it.",
      tags=["smart grid", "intelligent grid", "connected power", "energy network", "pylon", "electricity network", "iot"])
def _(S):
    return [line(seg(9.2, 21.5, 12, 6)), line(seg(14.8, 21.5, 12, 6)), line(seg(10.4, 14, 13.6, 14)), line(seg(9.6, 18.4, 14.4, 18.4)),
            line(seg(7.8, 9.4, 16.2, 9.4)), dot(4, 4.6, 1.7), dot(20, 4.6, 1.7), dot(3.6, 14, 1.7), dot(20.4, 14, 1.7),
            line(seg(5.2, 5.8, 7.8, 9.4)), line(seg(18.8, 5.8, 16.2, 9.4))]


@icon("off-grid-cabin", CAT, "Small cabin beside a wind turbine, with a solar panel on the roof.",
      tags=["off grid cabin", "off the grid", "remote cabin", "tiny house", "self sufficient", "solar cabin", "wind power"])
def _(S):
    cabin = poly([(8.5, 8.5), (14.5, 13), (14.5, 21.5), (2.5, 21.5), (2.5, 13)], closed=True, r=S.r)
    hub = (19, 7)
    blades = [line(seg(*hub, *polar(*hub, 4.4, a))) for a in (-90, 30, 150)]
    return [shell(cabin), solid(poly([(4.6, 11.2), (6.6, 9.6), (7.9, 10.8), (5.9, 12.4)], closed=True)),
            *blades, dot(*hub, 1.3), line(seg(19, 8, 19, 21.5))]


@icon("energy-efficiency-label", CAT, "Four stepped horizontal bars that shorten from top to bottom.",
      tags=["energy label", "efficiency rating", "energy rating", "appliance label", "epc", "a rating", "energy class"])
def _(S):
    def bar(y, x1):
        return shell(poly([(2.5, y + 0.6), (x1, y + 0.6), (x1 + 2.4, y + 2.4), (x1, y + 4.2), (2.5, y + 4.2)], closed=True, r=S.r * 0.4))
    return [bar(2.2, 15), bar(7.6, 12), bar(13, 9), bar(18.4, 6)]


@icon("home-insulation", CAT, "House section with a zigzag insulation layer inside.",
      tags=["home insulation", "loft insulation", "wall insulation", "thermal", "energy saving", "weatherproofing", "house"])
def _(S):
    house = poly([(12, 2.8), (21.5, 10.8), (21.5, 21.5), (2.5, 21.5), (2.5, 10.8)], closed=True, r=S.r)
    zz = poly([(5.6, 18.6), (8.2, 14.4), (10.8, 18.6), (13.4, 14.4), (16, 18.6), (18.6, 14.4)], r=S.r * 0.4)
    return [shell(house), detail(zz)]


@icon("draft-excluder", CAT, "Door with a long stuffed tube lying along its bottom edge.",
      tags=["draft excluder", "draught excluder", "door snake", "door seal", "draught stopper", "winter", "insulation"])
def _(S):
    return [line(poly([(6, 14.6), (6, 2.5), (18, 2.5), (18, 14.6)], r=S.r * 0.6)),
            dot(15, 9, 1.0), shell(rect(2.5, 17, 19, 4.6, 2.3))]


@icon("energy-audit", CAT, "Clipboard with a lightning bolt and a line of text.",
      tags=["energy audit", "energy assessment", "home energy check", "efficiency survey", "inspection", "clipboard", "bolt"])
def _(S):
    return [shell(rect(4.5, 4.5, 15, 17, L(S, 1.0, 2.4))), shell(rect(9, 2.5, 6, 3.6, L(S, 0.5, 1.4))),
            mark(poly(bolt_pts(12, 12.4, 1.4), closed=True)), detail(seg(8.5, 18.2, 15.5, 18.2))]


@icon("energy-monitor", CAT, "Small display unit showing a bar graph and a bolt.",
      tags=["energy monitor", "power meter", "smart meter display", "usage display", "electricity monitor", "consumption", "bar graph"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 14, L(S, 1.0, 2.6))), mark(rect(6, 11.6, 2.2, 3.4, 0.3)), mark(rect(9.6, 8.4, 2.2, 6.6, 0.3)),
            mark(poly(bolt_pts(16.6, 10.4, 1.0), closed=True)), line(seg(12, 17.5, 12, 20.6)), line(seg(8, 20.6, 16, 20.6))]


@icon("standby-power", CAT, "Power button symbol beside a small crescent moon.",
      tags=["standby power", "phantom load", "vampire power", "sleep mode", "idle power", "switch off", "power button"])
def _(S):
    return [line(arc(8, 15, 5.4, -50, 230)), line(seg(8, 8.6, 8, 14.4)),
            shell("M22 9.6A4 4 0 1 1 17.6 3.2A3.2 3.2 0 0 0 22 9.6Z")]


@icon("low-flow-shower", CAT, "Shower head with only three thin lines of water.",
      tags=["low flow shower", "water saving shower", "eco shower head", "efficient shower", "save water", "shower", "conserve"])
def _(S):
    return [shell("M4.5 10.5A7.5 6.5 0 0 1 19.5 10.5Z"), line(seg(12, 4, 12, 2.4)),
            line(seg(7.5, 14.5, 7.5, 19)), line(seg(12, 14.5, 12, 21)), line(seg(16.5, 14.5, 16.5, 19))]


@icon("dual-flush-toilet", CAT, "Toilet tank lid with one large round button and one small round button.",
      tags=["dual flush", "toilet flush", "water saving toilet", "two button flush", "half flush", "full flush", "cistern"])
def _(S):
    return [shell(rect(2.5, 6, 19, 12, L(S, 1.0, 3))), mark(circle(8.6, 12, 3.3)), mark(circle(16.6, 12, 1.8))]


# ============================================================================ green buildings and cities

@icon("passive-house", CAT, "House outline with a large window and a sun shining toward it.",
      tags=["passive house", "passivhaus", "low energy home", "solar gain", "south window", "insulated home", "sun"])
def _(S):
    house = poly([(13.5, 6), (22, 12.5), (22, 21.5), (5.5, 21.5), (5.5, 12.5)], closed=True, r=S.r)
    return [shell(house), detail(poly([(9, 14.2), (16.5, 14.2), (16.5, 18.6), (9, 18.6)], closed=True)),
            solid(circle(4.4, 4.4, 2.0)), *sun_rays(4.4, 4.4, 4.2, 6.0, (0, 45, 90))]


@icon("green-building", CAT, "Stepped office tower with window dots and small leaves growing from its sides.",
      tags=["green building", "eco tower", "sustainable architecture", "vertical garden", "leed", "office", "living facade"])
def _(S):
    tower = poly([(9.5, 2.5), (15.5, 2.5), (15.5, 7), (17, 7), (17, 21.5), (7, 21.5), (7, 7), (9.5, 7)], closed=True, r=S.r * 0.6)
    return [shell(tower), dot(10.4, 11.2, 0.9), dot(13.6, 11.2, 0.9), dot(10.4, 14.8, 0.9), dot(13.6, 14.8, 0.9),
            dot(10.4, 18.4, 0.9), dot(13.6, 18.4, 0.9),
            solid(leaf_solid(7, 13.6, 2.2, 8.4, 2.0, 0)), solid(leaf_solid(17, 18, 21.8, 12.8, 2.0, 0))]


@icon("bike-commute", CAT, "Bicycle with a briefcase strapped above its rear wheel.",
      tags=["bike commute", "cycle to work", "bicycle commuting", "green commute", "cycling", "briefcase", "work"])
def _(S):
    return [shell(circle(6, 17.5, 3.6)), shell(circle(18, 17.5, 3.6)),
            line(poly([(6, 17.5), (10.4, 12.2), (16, 12.2), (18, 17.5)], r=S.r * 0.6)), line(seg(10.4, 12.2, 12.6, 17.5)),
            line(poly([(16, 12.2), (15.2, 8), (17.4, 8)], r=S.r * 0.4)),
            shell(rect(2.5, 4.8, 7.4, 5.2, L(S, 0.5, 1.6)))]


@icon("walking-commute", CAT, "Person walking beside a leaf.",
      tags=["walking commute", "walk to work", "pedestrian", "green commute", "active travel", "on foot", "leaf"])
def _(S):
    return [solid(circle(8.5, 4.6, 2.3)), line(poly([(8.5, 8.4), (8.3, 14)])), line(poly([(5.4, 12), (8.5, 9.6), (11.6, 12.2)], r=S.r * 0.6)),
            line(poly([(5.8, 21.5), (8.3, 14), (11.6, 21.5)], r=S.r * 0.6)),
            *leaf(S, 14.6, 21, 21, 6.2, 4.6)]


@icon("eco-house", CAT, "House outline with a leaf growing where the chimney would be.",
      tags=["eco house", "green home", "sustainable home", "eco friendly house", "energy efficient home", "leaf", "house"])
def _(S):
    house = poly([(12, 4.8), (21, 12.8), (19, 12.8), (19, 21.5), (5, 21.5), (5, 12.8), (3, 12.8)], closed=True, r=S.r)
    return [shell(house), detail(poly([(10, 21.5), (10, 16.5), (14, 16.5), (14, 21.5)])), solid(leaf_solid(16.6, 9, 21.6, 2.4, 2.4))]


@icon("green-city", CAT, "City buildings with a tree between them and a leaf above.",
      tags=["green city", "eco city", "urban greening", "sustainable city", "city trees", "skyline", "leaf"])
def _(S):
    return [shell(rect(2.5, 10, 6, 11.5, L(S, 0.5, 1.6))), shell(rect(15.5, 7, 6, 14.5, L(S, 0.5, 1.6))),
            solid(circle(12, 14.2, 2.7)), line(seg(12, 15, 12, 21.5)),
            solid(leaf_solid(8.8, 7.6, 15.2, 1.8, 3.2))]


@icon("urban-farm", CAT, "Apartment building with a row of young plants growing on its roof.",
      tags=["urban farm", "rooftop farm", "city farming", "urban agriculture", "rooftop garden", "sprouts", "building"])
def _(S):
    return [shell(rect(3, 13.5, 18, 8.2, L(S, 0.6, 2))), dot(8, 17.6, 0.9), dot(12, 17.6, 0.9), dot(16, 17.6, 0.9),
            *sprout(6.6, 12, 6, 1.3), *sprout(12, 12, 6, 1.3), *sprout(17.4, 12, 6, 1.3)]


@icon("community-garden", CAT, "Raised garden bed with young plants and a person standing beside it.",
      tags=["community garden", "shared garden", "neighborhood garden", "volunteers", "gardening together", "raised bed", "allotment"])
def _(S):
    return [solid(circle(5, 8, 2.1)), line(poly([(5, 10.8), (5, 16.2)])), line(seg(2.4, 12.4, 7.6, 12.4)),
            line(poly([(2.8, 21.5), (5, 16.2), (7.2, 21.5)], r=S.r * 0.5)),
            shell(rect(11, 14.5, 10.5, 7, L(S, 0.5, 1.6))), *sprout(14.5, 13.5, 6.2, 1.2), *sprout(18.2, 13.5, 6.2, 1.2)]

# ============================================================================ local food and nature

@icon("allotment", CAT, "Picket fence around a small plot with young plants and a garden shed.",
      tags=["allotment", "vegetable plot", "kitchen garden", "garden plot", "grow your own", "shed", "fence"])
def _(S):
    shed = poly([(14.5, 13), (17.8, 8.6), (21.2, 13), (21.2, 21.5), (14.5, 21.5)], closed=True, r=S.r * 0.6)
    return [line(seg(3.5, 14.5, 3.5, 21.5)), line(seg(7.5, 14.5, 7.5, 21.5)), line(seg(11, 14.5, 11, 21.5)),
            line(seg(3.5, 17.2, 11, 17.2)), *sprout(5.5, 13.2, 4.2, 1.1), *sprout(9.5, 13.2, 4.2, 1.1), shell(shed)]


@icon("plant-based-diet", CAT, "Round plate holding a leaf and a carrot.",
      tags=["plant based diet", "vegan", "vegetarian", "vegetable plate", "healthy eating", "meat free", "carrot"])
def _(S):
    carrot = poly([(14.6, 8.6), (18.4, 11.4), (11.6, 17.6)], closed=True, r=S.r * 0.5)
    return [shell(circle(12, 12, 9.4)), mark(leaf_solid(5.8, 16.4, 11.2, 7.4, 2.6)), mark(carrot), mark(circle(16.8, 8.2, 1.0))]


@icon("local-produce", CAT, "Basket with a map pin above it.",
      tags=["local produce", "locally grown", "farm to table", "farmers market", "buy local", "regional food", "map pin"])
def _(S):
    basket = poly([(3.5, 15), (20.5, 15), (18.5, 21.5), (5.5, 21.5)], closed=True, r=S.r)
    pin = "M12 13C12 13 8.2 9.6 8.2 6.2A3.8 3.8 0 0 1 15.8 6.2C15.8 9.6 12 13 12 13Z"
    return [shell(basket), detail(seg(4.6, 18.2, 19.4, 18.2)), shell(pin), dot(12, 6.3, 1.2)]


@icon("organic-label", CAT, "Round seal with a check mark whose end sprouts a leaf.",
      tags=["organic label", "organic certified", "organic food", "natural seal", "eco certified", "pesticide free", "check"])
def _(S):
    return [shell(circle(12, 12, 9.6)), detail(poly([(7, 12.6), (10.2, 15.8), (14.8, 10.6)], r=S.r * 0.6)),
            mark(leaf_solid(13.6, 11.6, 17.8, 6.6, 2.2, 0))]


@icon("endangered-species", CAT, "Rhinoceros head in profile with two horns, inside a circle.",
      tags=["endangered species", "red list", "threatened animal", "rhino", "extinction", "wildlife", "conservation"])
def _(S):
    head = union(poly([(4.8, 16.4), (5.4, 13.6), (9.4, 12.2), (13.6, 9.8), (18.8, 10.8), (19.2, 17), (14.8, 18.8), (8.4, 18.8)], closed=True, r=S.r * 1.2),
                 poly([(5.6, 13.6), (7, 6.4), (10.4, 11.8)], closed=True, r=S.r * 0.5),
                 poly([(10.4, 11.6), (11.4, 8.8), (13, 10.6)], closed=True, r=S.r * 0.4),
                 poly([(15.6, 10), (17.2, 6.8), (18.6, 10.6)], closed=True, r=S.r * 0.5))
    return [shell(circle(12, 12, 10.2)), mark(minus(head, circle(14.6, 13.6, 1.0)))]


@icon("wildlife-protection", CAT, "Shield with a deer head and antlers inside.",
      tags=["wildlife protection", "animal conservation", "nature protection", "deer", "habitat", "shield", "protected species"])
def _(S):
    shield = poly([(12, 2.5), (20, 5.5), (20, 12), (16.5, 19), (12, 21.5), (7.5, 19), (4, 12), (4, 5.5)], closed=True, r=S.r * 1.2)
    return [shell(shield), mark(poly([(12, 18), (9.6, 11.6), (14.4, 11.6)], closed=True, r=0.6)),
            detail(poly([(10.2, 11.4), (8.8, 7.6)])), detail(poly([(13.8, 11.4), (15.2, 7.6)])),
            detail(seg(9.4, 9.4, 7, 8.2)), detail(seg(14.6, 9.4, 17, 8.2))]


@icon("nature-reserve", CAT, "Direction signpost beside a tree and a flying bird.",
      tags=["nature reserve", "protected area", "national park", "wildlife reserve", "conservation area", "trail sign", "tree"])
def _(S):
    return [line(seg(5.5, 8.6, 5.5, 21.5)), shell(poly([(2.5, 3.6), (8.6, 3.6), (10.8, 6.2), (8.6, 8.8), (2.5, 8.8)], closed=True, r=S.r * 0.4)),
            shell(circle(16.5, 11, 4.6)), line(seg(16.5, 15.6, 16.5, 21.5)),
            line(poly([(13, 4.4), (15.5, 2.6), (18, 4.4)], r=S.r * 0.4))]


@icon("tree-nursery", CAT, "Bench holding a row of young potted saplings.",
      tags=["tree nursery", "plant nursery", "saplings", "seedlings", "reforestation", "potted plants", "garden centre"])
def _(S):
    pots = [solid(poly([(x - 2.2, 14.6), (x + 2.2, 14.6), (x + 1.6, 18.2), (x - 1.6, 18.2)], closed=True)) for x in (5.5, 12, 18.5)]
    return [*pots, *sprout(5.5, 14, 6.6, 1.3), *sprout(12, 14, 6.6, 1.3), *sprout(18.5, 14, 6.6, 1.3),
            line(seg(2.5, 19.6, 21.5, 19.6)), line(seg(4.5, 19.6, 4.5, 22)), line(seg(19.5, 19.6, 19.5, 22))]


@icon("seed-bank", CAT, "Round vault door with a seed in its center.",
      tags=["seed bank", "seed vault", "seed storage", "biodiversity", "gene bank", "heritage seeds", "safe"])
def _(S):
    seed = rot(ellipse(12, 12, 2.0, 3.4), 35, 12, 12)
    return [shell(rect(2.5, 2.5, 19, 19, L(S, 1.0, 4))), detail(circle(12, 12, 6.2)), mark(seed)]


@icon("bee-hotel", CAT, "Wooden insect house with a pitched roof and rows of round nesting holes.",
      tags=["bee hotel", "insect hotel", "bug house", "solitary bees", "pollinators", "nesting box", "garden wildlife"])
def _(S):
    box = poly([(12, 3), (21, 10), (21, 21.5), (3, 21.5), (3, 10)], closed=True, r=S.r * 0.6)
    return [shell(box)] + [dot(x, y, 1.05) for y in (13.4, 17.8) for x in (8, 12, 16)]


@icon("pollinator-garden", CAT, "Flower on a stem with a bee hovering beside it.",
      tags=["pollinator garden", "bee friendly", "wildflowers", "butterfly garden", "bee", "flower", "pollination"])
def _(S):
    cx, cy = 8.5, 10.5
    petals = union(*[circle(*polar(cx, cy, 3.9, -90 + 72 * k), 2.3) for k in range(5)], circle(cx, cy, 2.6))
    flower = minus(petals, circle(cx, cy, 1.25))
    bee = minus(ellipse(17.4, 15.6, 3.4, 2.4), strokes(seg(16.2, 12.5, 16.2, 18.5), 0.8), strokes(seg(18.6, 12.5, 18.6, 18.5), 0.8))
    return [solid(flower), line(seg(8.5, 15, 8.5, 21.5)), solid(leaf_solid(8.5, 19.5, 4, 16.6, 1.6, 0)),
            solid(bee), line(seg(16.4, 13.4, 15.4, 10.6)), line(seg(18.4, 13.4, 19.6, 10.6))]

