"""TypeIcon Core: plants (batch plants_002): garden flowers, bouquets, arrangements and houseplants.

Drawn from the plants themselves; flowers are mostly front or side views on a short stem, houseplants sit in a pot
on the baseline (y 21.5).
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, LINE, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "plants"


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


def rpts(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def region(d):
    """Area covered by a closed outline filled to its outer stroke edge."""
    return U(P(d), ST(d, 2))


def grow(p, g):
    return U(p, ST(path_to_d(p), 2 * g, "round", "round"))


def cut_strokes(S, ds, cutter, gap=2.0):
    """Stroke outlines of ds (in style S) with grow(cutter, gap) removed, for things seen behind another."""
    body = U(*[ST(d, 2, S.cap, S.join) for d in ds])
    return solid(path_to_d(D(body, grow(cutter, gap))))


def leaf_shape(x1, y1, x2, y2, bulge):
    """Pointed leaf from (x1, y1) to (x2, y2), each half bowing out by about bulge px."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    b = bulge * 2
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx * b)} {fmt(my + ny * b)} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(mx - nx * b)} {fmt(my - ny * b)} {fmt(x1)} {fmt(y1)}Z")


def blob(*circles):
    """Cloud-like crown: union of circles (cx, cy, r)."""
    return union(*[circle(x, y, r) for x, y, r in circles])


def star_pts(cx, cy, R, r, n, start=-90.0):
    return [polar(cx, cy, R if k % 2 == 0 else r, start + k * 180 / n) for k in range(2 * n)]


GROUND = 21.5


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def stem(x0, y0, x1, y1):
    return line(seg(x0, y0, x1, y1))


def bell_d(S, cx, top, w, h, k=0.6):
    """Hanging bell: narrow closed top flaring to a flat mouth."""
    return poly([(cx - w * k / 2, top), (cx + w * k / 2, top), (cx + w / 2, top + h), (cx - w / 2, top + h)],
                closed=True, r=S.r)


def chain(pts_r):
    """Scalloped column: union of circles (x, y, r)."""
    return union(*[circle(x, y, r) for x, y, r in pts_r])


def rot_ellipse(cx, cy, rx, ry, deg, px, py):
    return rot(ellipse(cx, cy, rx, ry), deg, px, py)


def layered2(back, front, gap=1.5):
    """Filled design: front(S) parts sit in front of back(S) parts (back cut around front)."""
    def f():
        from dsl import filled_region
        fr = filled_region(front(LINE))
        return U(D(filled_region(back(LINE)), grow(fr, gap)), fr)
    return f


# ============================================================================ chunk 1: garden flowers


def dbell(S, cx, top, w, h):
    """Hanging bell with a domed top and a flaring mouth."""
    l, r_, y = cx - w / 2, cx + w / 2, top + h
    return (f"M{fmt(l)} {fmt(y)}L{fmt(cx - w * 0.28)} {fmt(top + 1.6)}Q{fmt(cx)} {fmt(top - 0.6)} {fmt(cx + w * 0.28)} {fmt(top + 1.6)}"
            f"L{fmt(r_)} {fmt(y)}Z")


def flower_d(cx, cy, r, n=5, pr=None, start=-90.0):
    """Small blossom silhouette: n round petals around a centre."""
    pr = pr or r * 0.55
    return union(*[circle(*polar(cx, cy, r - pr, start + k * 360 / n), pr) for k in range(n)], circle(cx, cy, r - pr))


def pot_d(S, x0=7, x1=17, top=16, bottom=21.5, inset=1.5):
    return poly([(x0, top), (x1, top), (x1 - inset, bottom), (x0 + inset, bottom)], closed=True, r=L(S, 0, 1.2))


def frond(p0, p1, p2, p3, n=5, ln=2.4, side=1):
    """Open d-string: a curved rachis with short alternating leaflet ticks pointing forward."""
    parts = [f"M{fmt(p0[0])} {fmt(p0[1])}C{fmt(p1[0])} {fmt(p1[1])} {fmt(p2[0])} {fmt(p2[1])} {fmt(p3[0])} {fmt(p3[1])}"]
    for i in range(1, n + 1):
        t = i / (n + 1)
        x, y = bez(p0, p1, p2, p3, t)
        x2, y2 = bez(p0, p1, p2, p3, min(1, t + 0.02))
        dx, dy = x2 - x, y2 - y
        m = math.hypot(dx, dy) or 1
        dx, dy = dx / m, dy / m
        for sg in (1, -1):
            a = math.radians(40 * sg)
            ux, uy = dx * math.cos(a) - dy * math.sin(a), dx * math.sin(a) + dy * math.cos(a)
            parts.append(f"M{fmt(x)} {fmt(y)}L{fmt(x + ux * ln)} {fmt(y + uy * ln)}")
    return "".join(parts)


def rot_open(d, deg, cx, cy):
    """Rotate an open d-string made of absolute M/L/C commands (Path ops would drop or close it)."""
    import re
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    out, nums = [], []
    for tok in re.findall(r"[MLC]|-?\d*\.?\d+", d):
        if tok in "MLC":
            out.append(tok)
        else:
            nums.append(float(tok))
            if len(nums) == 2:
                x, y = nums
                out.append(f"{fmt(cx + (x - cx) * ca - (y - cy) * sa)} {fmt(cy + (x - cx) * sa + (y - cy) * ca)} ")
                nums = []
    return "".join(out)


@icon("crocus", CAT, "Crocus flower cup growing low between two thin grassy leaves",
      tags=["crocus", "spring flower", "bulb", "saffron", "garden", "early bloom"])
def _(S):
    cup = union(leaf_shape(12, 15, 12, 3.5, 2.4), leaf_shape(12, 15, 6, 6.5, 1.7), leaf_shape(12, 15, 18, 6.5, 1.7))
    return [shell(cup, stroke_miterlimit="8"), stem(12, 15, 12, GROUND),
            line("M12 21.5C11.5 19 8 16.5 3.5 16"), line("M12 21.5C12.5 19 16 16.5 20.5 16")]


@icon("hyacinth", CAT, "Hyacinth with a dense column of small florets between tall strap leaves",
      tags=["hyacinth", "spring flower", "bulb", "fragrant", "garden", "flower spike"])
def _(S):
    col = chain([(12, 4, 2.2), (9.4, 6.8, 2.3), (14.6, 6.8, 2.3), (9.4, 10.3, 2.3), (14.6, 10.3, 2.3), (12, 8.5, 2.5), (12, 12.3, 2.3)])
    return [shell(col), stem(12, 14, 12, GROUND),
            shell(leaf_shape(11, 21.5, 4.5, 13.5, 1.2)), shell(leaf_shape(13, 21.5, 19.5, 13.5, 1.2))]


@icon("lavender", CAT, "Three lavender stems topped with slender tiered flower spikes",
      tags=["lavender", "herb", "purple", "aromatherapy", "provence", "fragrant", "garden"])
def _(S):
    def spike(x, y, dx=0.0, n=4):
        return chain([(x + dx * i / (n - 1), y + 2.8 * i, 1.55 + 0.1 * i) for i in range(n)])
    return [shell(spike(12, 2.8)), shell(spike(6, 6.8, -0.8, 3)), shell(spike(18, 6.8, 0.8, 3)),
            line("M12 12.5L12 21.5"), line("M6 13.5C6 17 10 19 12 21.5"), line("M18 13.5C18 17 14 19 12 21.5")]


@icon("carnation", CAT, "Carnation with a frilled zigzag flower head above a narrow calyx on a stem",
      tags=["carnation", "dianthus", "flower", "pink", "corsage", "mothers day"])
def _(S):
    head = poly([(4, 8.5), (5, 4), (8, 6.5), (10, 3.5), (12, 6.5), (14, 3.5), (16, 6.5), (19, 4), (20, 8.5), (17, 12.5), (7, 12.5)],
                closed=True, r=S.r * 0.5)
    return [shell(head), detail(seg(9.5, 8.5, 10, 12.5)), detail(seg(14.5, 8.5, 14, 12.5)),
            shell(poly([(9, 13.5), (15, 13.5), (14, 17.5), (10, 17.5)], closed=True, r=S.r * 0.5)), stem(12, 17.5, 12, GROUND)]


@icon("peony", CAT, "Peony bloom made of many layered ruffled cupped petals on a stem with two leaves",
      tags=["peony", "paeonia", "flower", "wedding", "bloom", "garden", "spring"])
def _(S):
    body = blob((6.8, 9, 4.3), (17.2, 9, 4.3), (12, 6.3, 4.6), (12, 10.5, 6.6))
    return [shell(body), detail("M6.5 10C7.5 14 16.5 14 17.5 10"), detail("M9.5 7.3C11 9.6 13 9.6 14.5 7.3"),
            stem(12, 17, 12, GROUND), shell(leaf_shape(12, 20.5, 6.5, 17.3, 1.2)), shell(leaf_shape(12, 20.5, 17.5, 17.3, 1.2))]


@icon("chrysanthemum", CAT, "Chrysanthemum seen from the side as a dense domed ball of fine petals on a stem with leaves",
      tags=["chrysanthemum", "mum", "autumn flower", "flower", "garden", "asian flower"])
def _(S):
    dome = "M3.5 14A8.5 10 0 0 1 20.5 14Z"
    dets = [detail(seg(12, 14, *polar(12, 14, 7.5, a))) for a in (-155, -122, -90, -58, -25)]
    return [shell(dome), *dets, stem(12, 14, 12, GROUND), shell(leaf_shape(12, 20, 6, 17, 1.2)), shell(leaf_shape(12, 20, 18, 17, 1.2))]


@icon("pansy", CAT, "Pansy with five overlapping rounded petals and face-like markings at the centre",
      tags=["pansy", "viola", "flower", "garden", "spring", "bedding plant"])
def _(S):
    body = blob((8.3, 7.5, 4.4), (15.7, 7.5, 4.4), (6.5, 13, 3.8), (17.5, 13, 3.8), (12, 16.5, 4.5))
    return [shell(body), detail(seg(12, 12, 8.5, 14.5)), detail(seg(12, 12, 15.5, 14.5)), detail(seg(12, 12, 12, 15.5)), dot(12, 11, 1.25)]


@icon("morning-glory", CAT, "Morning glory flower seen from the front with a five-point star pattern and a twining vine",
      tags=["morning glory", "ipomoea", "vine", "climbing flower", "trumpet flower", "garden"])
def _(S):
    body = blob(*[(*polar(12, 10.5, 4.3, -90 + 72 * k), 3.4) for k in range(5)], (12, 10.5, 4.6))
    dets = [detail(seg(12, 10.5, *polar(12, 10.5, 4.6, -90 + 72 * k))) for k in range(5)]
    return [shell(body), *dets, dot(12, 10.5, 1.3), line("M12 18.5C12 21 14.5 21.5 18 21.5")]


@icon("calla-lily", CAT, "Calla lily with a smooth flared cup spathe and a straight spike rising from its middle, on a long stem",
      tags=["calla lily", "arum lily", "zantedeschia", "wedding flower", "white flower", "elegant"])
def _(S):
    cup = "M12 18C6 17 4.5 11 7 4C8 7 10 9 12 9C14 9 16 7 17 4C19.5 11 18 17 12 18Z"
    return [shell(cup, stroke_miterlimit="8"), line(seg(12, 9, 12, 2.5)), stem(12, 18, 12, GROUND)]


@icon("anthurium", CAT, "Anthurium with a glossy heart-shaped spathe and a curved finger-like spike rising from its middle",
      tags=["anthurium", "flamingo flower", "tropical", "heart flower", "houseplant", "spathe"])
def _(S):
    heart = "M12 19C5.5 15 3.5 11 6 8C8.5 5.5 11 7 12 9C13 7 15.5 5.5 18 8C20.5 11 18.5 15 12 19Z"
    return [shell(heart, stroke_miterlimit="8"), detail("M11.5 14.5C11.5 10 14 7 15 2.5"), stem(12, 19, 12, GROUND)]


@icon("bird-of-paradise", CAT, "Bird of paradise flower with a horizontal beak-like sheath and pointed petals fanning upward",
      tags=["bird of paradise", "strelitzia", "tropical flower", "exotic", "crane flower", "hawaii"])
def _(S):
    sheath = "M3 12.5C7 10.5 12 10.5 16 12.5C12 17 7 16.5 3 12.5Z"
    pet = union(leaf_shape(11, 11.5, 11, 2.5, 2), leaf_shape(13.5, 11.5, 17.5, 3.5, 1.8), leaf_shape(15, 12.5, 20.5, 7, 1.6), sheath)
    return [shell(pet, stroke_miterlimit="8"), stem(13.5, 15, 13.5, GROUND)]


def _protea_back(S):
    fan = union(*[leaf_shape(12, 17, *polar(12, 17, 10.5, a), 1.9) for a in (-165, -130, -90, -50, -15)])
    return [shell(fan, stroke_miterlimit="8")]


def _protea_front(S):
    return [shell(circle(12, 11.5, 4.3))]


def _protea_back(S):
    return [shell(union(*[leaf_shape(12, 17.5, *polar(12, 17.5, 11, a), 2) for a in (-158, -125, -55, -22)]), stroke_miterlimit="8")]


def _protea_front(S):
    return [dot(12, 10.5, 3.9)]


@icon("protea", CAT, "Protea flower head with a solid domed centre inside a bowl of pointed bracts, on a short stem",
      tags=["protea", "king protea", "south africa", "fynbos", "exotic flower", "bouquet"],
      filled=layered2(_protea_back, _protea_front))
def _(S):
    fan = union(*[leaf_shape(12, 17.5, *polar(12, 17.5, 11, a), 2) for a in (-158, -125, -55, -22)])
    body = U(*[ST(fan, 2, S.cap, S.join, 8)])
    return [solid(path_to_d(D(body, grow(P(circle(12, 10.5, 3.9)), 1.6)))), *_protea_front(S), stem(12, 17.5, 12, GROUND)]


@icon("passion-flower", CAT, "Passion flower with ten pointed petals, a ring of filaments and a centre of stigmas",
      tags=["passion flower", "passiflora", "tropical vine", "flower", "exotic", "bloom"])
def _(S):
    petals = union(*[leaf_shape(12, 12, *polar(12, 12, 10, -90 + 36 * k), 2.2) for k in range(10)])
    return [shell(petals, stroke_miterlimit="8"), detail(circle(12, 12, 4.8)), dot(12, 12, 1.6)]


@icon("magnolia", CAT, "Magnolia flower, a goblet of thick rounded petals rising from a bare woody twig",
      tags=["magnolia", "spring bloom", "tree flower", "goblet flower", "southern", "twig"])
def _(S):
    cup = union(ellipse(12, 10, 3.7, 7), rot_ellipse(12, 10, 3.7, 7, -38, 12, 16.5), rot_ellipse(12, 10, 3.7, 7, 38, 12, 16.5))
    return [shell(cup), detail("M9 9.5C9 12.5 10 15 12 16.5"), detail("M15 9.5C15 12.5 14 15 12 16.5"), stem(12, 17, 12, 20), line("M3.5 21.5C8 21 16 20.5 20.5 18")]


# ============================================================================ chunk 2: blooms and sprays


@icon("plumeria", CAT, "Plumeria flower of five teardrop petals twisted like a pinwheel around a small centre",
      tags=["plumeria", "frangipani", "tropical flower", "hawaii", "lei flower", "pinwheel", "bali"])
def _(S):
    petal = "M12 12C8.3 9.2 9.3 4.5 13 2.5C16.6 5 15.7 9.5 12 12Z"
    edge = "M12 12C8.3 9.2 9.3 4.5 13 2.5"
    shape = union(*[rot(petal, 72 * k, 12, 12) for k in range(5)])
    return [shell(shape, stroke_miterlimit="8"), *[detail(rot_open(edge, 72 * k, 12, 12)) for k in range(5)], dot(12, 12, 1.3)]


def _wcluster(cx, top):
    rows = [(top, 1.7, 1.9), (top + 3.6, 1.4, 1.8), (top + 7, 0.9, 1.7), (top + 10, 0, 1.6), (top + 12.8, 0, 1.25)]
    circs = []
    for y, off, r in rows:
        if off:
            circs += [(cx - off, y, r), (cx + off, y, r)]
        else:
            circs.append((cx, y, r))
    return chain(circs)


@icon("wisteria", CAT, "Wisteria vine with long hanging clusters of small pea flowers tapering to a point",
      tags=["wisteria", "climbing vine", "hanging flowers", "purple flowers", "pergola", "japan", "garden"])
def _(S):
    return [line("M2.5 4.5C8 2.5 16 2.5 21.5 4.5"), line(seg(7, 4, 7, 5.5)), shell(_wcluster(7, 7)), line(seg(17, 4, 17, 5.5)), shell(_wcluster(17, 7))]


@icon("hydrangea", CAT, "Hydrangea with a round ball of small florets above two broad leaves on a stem",
      tags=["hydrangea", "mophead", "flower ball", "blue flower", "garden", "shrub", "bloom"])
def _(S):
    ball = blob((12, 8.3, 4.6), *[(*polar(12, 8.3, 4.2, -90 + 60 * k), 3.3) for k in range(6)])
    return [shell(ball), dot(10, 6.8, 1.0), dot(14.3, 7.3, 1.0), dot(12, 10.6, 1.0), stem(12, 15.5, 12, GROUND),
            shell(leaf_shape(12, 20, 5, 16.5, 1.3)), shell(leaf_shape(12, 20, 19, 16.5, 1.3))]


@icon("edelweiss", CAT, "Edelweiss star of pointed woolly bracts around a small cluster of round flower heads",
      tags=["edelweiss", "alpine flower", "mountain flower", "leontopodium", "austria", "switzerland", "star flower"])
def _(S):
    rays = union(*[leaf_shape(12, 12, *polar(12, 12, 10, -90 + 45 * k), 1.6) for k in range(8)])
    return [shell(rays, stroke_miterlimit="8"), dot(12, 10.8, 1.2), dot(10.2, 13.4, 1.2), dot(13.8, 13.4, 1.2)]


@icon("thistle", CAT, "Thistle with a spiky tuft rising from a round bristly base on a short stem",
      tags=["thistle", "scotland", "prickly", "wildflower", "weed", "spiky flower", "scottish emblem"])
def _(S):
    base = poly([(6.5, 13), (9, 10), (15, 10), (17.5, 13), (15, 18), (9, 18)], closed=True, r=S.r * 0.8)
    return [*[line(seg(12, 10, *polar(12, 10, 8, a))) for a in (-160, -125, -90, -55, -20)], shell(base),
            detail(seg(8.7, 11, 14, 17)), detail(seg(15.3, 11, 10, 17)), stem(12, 18, 12, GROUND)]


@icon("water-lily", CAT, "Water lily with a fan of pointed petals floating open on a round pad above a water line",
      tags=["water lily", "nymphaea", "pond flower", "aquatic plant", "lotus like", "monet", "floating flower"])
def _(S):
    pet = union(leaf_shape(12, 17, 12, 3.5, 2.4), leaf_shape(12, 17, 5.5, 6.5, 2), leaf_shape(12, 17, 18.5, 6.5, 2),
                leaf_shape(12, 17, 2.8, 12.5, 1.6), leaf_shape(12, 17, 21.2, 12.5, 1.6), ellipse(12, 17.3, 9.5, 2.3))
    return [shell(pet, stroke_miterlimit="8"), line(seg(2.5, 21.5, 21.5, 21.5))]


@icon("poinsettia", CAT, "Poinsettia star of large pointed bracts in two layers around a cluster of small dots",
      tags=["poinsettia", "christmas flower", "red bracts", "holiday plant", "winter", "festive", "euphorbia"])
def _(S):
    outer = union(*[leaf_shape(12, 12, *polar(12, 12, 10.3, -90 + 60 * k), 2.6) for k in range(6)])
    inner = [detail(leaf_shape(*polar(12, 12, 2.8, -60 + 60 * k), *polar(12, 12, 7.2, -60 + 60 * k), 1.4)) for k in range(6)]
    return [shell(outer, stroke_miterlimit="8"), *inner, dot(12, 12, 1.4)]


@icon("heather", CAT, "Heather sprig with a woody stem and many small bell flowers along short side stems",
      tags=["heather", "calluna", "moorland", "scotland", "purple flowers", "sprig", "erica"])
def _(S):
    parts = [line("M5.5 21.5C8 16 10.5 10 13.5 3")]
    for (x0, y0), (x1, y1) in [((7.4, 17.8), (4, 15.8)), ((9.3, 13.6), (13.2, 15.8)), ((10.8, 10), (6.6, 8.3)),
                               ((12, 7.2), (16.5, 8.7)), ((13, 4.8), (9.8, 3.2))]:
        parts += [line(seg(x0, y0, x1, y1)), dot(x1, y1, 1.6)]
    return parts


@icon("fuchsia", CAT, "Fuchsia flower hanging from a stem with flared sepals, a bell skirt of petals and long dangling stamens",
      tags=["fuchsia", "ballerina flower", "hanging flower", "lady's eardrops", "garden", "basket plant"])
def _(S):
    skirt = poly([(10, 6), (14, 6), (18, 14), (6, 14)], closed=True, r=L(S, 0, 1.8))
    sep = union(leaf_shape(11, 7, 3.5, 4.5, 1.3), leaf_shape(13, 7, 20.5, 4.5, 1.3))
    return [line(seg(12, 2.5, 12, 6.5)), shell(union(skirt, sep), stroke_miterlimit="8"),
            line(seg(10, 14, 10, 19)), dot(10, 19.6, 1.2), line(seg(14, 14, 14, 20.5)), dot(14, 21, 1.0)]


def _heart(cx, top, w):
    h = w * 0.95
    return (f"M{fmt(cx)} {fmt(top + h)}C{fmt(cx - w * 0.95)} {fmt(top + h * 0.5)} {fmt(cx - w * 0.6)} {fmt(top - h * 0.1)} {fmt(cx)} {fmt(top + h * 0.3)}"
            f"C{fmt(cx + w * 0.6)} {fmt(top - h * 0.1)} {fmt(cx + w * 0.95)} {fmt(top + h * 0.5)} {fmt(cx)} {fmt(top + h)}Z")


@icon("bleeding-heart-flower", CAT, "Arching stem with a row of dangling heart-shaped flowers, each with a small drop at the bottom",
      tags=["bleeding heart", "dicentra", "heart flower", "spring garden", "romantic", "dangling flowers"])
def _(S):
    return [line("M3.5 21.5C3.5 10 7.5 3.5 13 3.5C16.5 3.5 19 4.5 20.5 7"), line(seg(8.8, 5, 8.8, 8)), shell(_heart(8.8, 7.6, 5.2)),
            dot(8.8, 16.8, 1.2), line(seg(17, 4.2, 17, 9.4)), shell(_heart(17, 9, 5.2)), dot(17, 18.2, 1.2)]


@icon("trillium", CAT, "Trillium with three broad petals above three large leaves, everything arranged in threes",
      tags=["trillium", "wakerobin", "woodland flower", "three petals", "wildflower", "spring ephemeral"])
def _(S):
    pet = union(*[leaf_shape(12, 7.5, *polar(12, 7.5, 5.6, -90 + 120 * k), 1.9) for k in range(3)])
    lv = union(leaf_shape(12, 14, 3.2, 17.5, 2.2), leaf_shape(12, 14, 20.8, 17.5, 2.2), leaf_shape(12, 14, 12, 21.3, 2.2))
    return [shell(pet, stroke_miterlimit="8"), shell(lv, stroke_miterlimit="8"), stem(12, 11, 12, 14)]


@icon("red-hot-poker", CAT, "Red hot poker with a torch-shaped spike of downward-pointing tubular flowers on a tall stem",
      tags=["red hot poker", "kniphofia", "torch lily", "poker plant", "spike flower", "garden"])
def _(S):
    torch = ellipse(12, 8.3, 3.9, 6.2)
    return [shell(torch), detail("M9.5 6.5L12 9L14.5 6.5"), detail("M9.5 10.8L12 13.3L14.5 10.8"), stem(12, 14.5, 12, GROUND),
            line("M12 21.5C12 19 8.5 17 4.5 17"), line("M12 21.5C12 19 15.5 17 19.5 17")]


@icon("cockscomb-flower", CAT, "Cockscomb flower with a wavy ruffled crest like a rooster comb on a thick stem",
      tags=["cockscomb", "celosia", "rooster comb", "ruffled flower", "red crest", "garden", "annual"])
def _(S):
    crest = union(blob((5.6, 9, 2.8), (8.6, 6.3, 3.0), (12, 5.3, 3.2), (15.4, 6.3, 3.0), (18.4, 9, 2.8)),
                  poly([(5.6, 9), (18.4, 9), (14, 15), (10, 15)], closed=True, r=0))
    return [shell(crest), detail("M8.5 11.5C9.5 8.5 11 8.5 12 10.5C13 8.5 14.5 8.5 15.5 11.5"), stem(12, 15, 12, GROUND),
            shell(leaf_shape(12, 20.5, 6.5, 17.8, 1.1)), shell(leaf_shape(12, 20.5, 17.5, 17.8, 1.1))]

# ============================================================================ chunk 3: more blooms


@icon("mimosa-flower", CAT, "Mimosa sprig with fluffy round pompom flowers and feathery leaves",
      tags=["mimosa", "acacia", "wattle", "yellow flowers", "pompom flower", "womens day", "fluffy"])
def _(S):
    return [line("M4.5 21.5C8 18 11 14 12.5 10.5"), line("M12.5 10.5C11.2 9.6 10.2 8.8 9.6 8.2"), line("M12.5 10.5C13 9.8 13.5 9 14 8.4"),
            line("M12.5 10.5C14 10.8 15.3 11.1 16.6 11.4"),
            shell(circle(7.5, 6.3, 2.7)), shell(circle(14.6, 5.4, 2.7)), shell(circle(19, 11.6, 2.5)),
            shell(leaf_shape(8.5, 16, 3.5, 13.8, 1.0)), shell(leaf_shape(10.5, 18.5, 17, 16.8, 1.0))]


@icon("rafflesia", CAT, "Giant flat rafflesia flower with five thick round warty petals around a large open centre",
      tags=["rafflesia", "corpse flower", "giant flower", "parasitic plant", "rainforest", "borneo", "sumatra"])
def _(S):
    petals = union(*[circle(*polar(12, 12, 6.4, -90 + 72 * k), 4.6) for k in range(5)], circle(12, 12, 6))
    warts = [dot(*polar(12, 12, 8.3, -90 + 72 * k), 1.0) for k in range(5)]
    return [shell(petals), detail(circle(12, 12, 3.6)), *warts]


@icon("titan-arum", CAT, "Titan arum with a very tall central spike rising from a frilled upturned bell-shaped spathe",
      tags=["titan arum", "corpse flower", "amorphophallus", "giant flower", "rare plant", "botanical garden", "stinky"])
def _(S):
    bowl = "M9.8 21.5C9.8 18 5 16 3.5 11.5L5.6 13.3L7.6 11L10 13.3L12 11L14 13.3L16.4 11L18.4 13.3L20.5 11.5C19 16 14.2 18 14.2 21.5Z"
    return [shell(bowl), line(seg(12, 14, 12, 2.5))]


@icon("coneflower", CAT, "Coneflower with drooping petals hanging down around a raised spiky cone centre",
      tags=["coneflower", "echinacea", "purple coneflower", "daisy", "prairie flower", "medicinal", "wildflower"])
def _(S):
    pet = union(leaf_shape(8.5, 10.5, 2.5, 14.5, 1.3), leaf_shape(9.5, 11, 5.5, 19.5, 1.4), leaf_shape(12, 11, 12, 20.5, 1.4),
                leaf_shape(14.5, 11, 18.5, 19.5, 1.4), leaf_shape(15.5, 10.5, 21.5, 14.5, 1.3))
    cone = poly([(8, 10.5), (9, 6), (12, 2.8), (15, 6), (16, 10.5)], closed=True, r=S.r * 0.6)
    return [shell(pet, stroke_miterlimit="8"), shell(cone), detail(seg(9.6, 8.6, 12.4, 5.6)), detail(seg(14.4, 8.6, 11.6, 5.6))]


@icon("dogwood-flower", CAT, "Dogwood flower of four broad rounded bracts with notched tips around a small cluster of dots",
      tags=["dogwood", "cornus", "spring blossom", "white flower", "four petals", "notched petals", "tree flower"])
def _(S):
    br = [(12, 11), (7.6, 6.5), (8.6, 2.6), (12, 4.6), (15.4, 2.6), (16.4, 6.5)]
    bracts = union(*[path_to_d(P(poly(rpts(br, 90 * k, 12, 12), closed=True, r=L(S, 0, 2)))) for k in range(4)], circle(12, 12, 2.6))
    return [shell(bracts), dot(12, 10.9, 0.95), dot(10.8, 12.9, 0.95), dot(13.2, 12.9, 0.95)]


@icon("forget-me-not", CAT, "Small cluster of three forget-me-not flowers, each with five round petals and a small centre",
      tags=["forget me not", "myosotis", "blue flowers", "remembrance", "small flowers", "spring", "memorial"])
def _(S):
    f = lambda cx, cy: flower_d(cx, cy, 4.7)
    return [shell(union(f(7.3, 7.5), f(16.7, 7.5), f(12, 14.8))), dot(7.3, 7.5, 1.1), dot(16.7, 7.5, 1.1), dot(12, 14.8, 1.1), stem(12, 19.5, 12, GROUND)]


@icon("jasmine", CAT, "Jasmine sprig with small five-petal pinwheel star flowers and slim closed buds",
      tags=["jasmine", "fragrant flower", "white flower", "tea", "sprig", "perfume", "jasminum"])
def _(S):
    def fl(cx, cy, r):
        return union(*[leaf_shape(cx, cy, *polar(cx, cy, r, -90 + 72 * k), 1.5) for k in range(5)])
    return [line("M4.5 21.5C8 19 11 16.5 13 14"), line("M8.5 18.3C7.3 15 7.5 12.3 8 10.5"),
            shell(fl(8, 6.8, 4.3), stroke_miterlimit="8"), dot(8, 6.8, 1.0), shell(fl(16.5, 11.3, 4.5), stroke_miterlimit="8"), dot(16.5, 11.3, 1.0),
            shell(leaf_shape(13.6, 5.3, 16, 1.8, 0.9)), shell(leaf_shape(11.5, 19.5, 18, 18.2, 0.9))]


def _trumpet(px, py, ang, ln, w, S):
    pts = [(0, -0.8), (ln, -w / 2), (ln, w / 2), (0, 0.8)]
    return poly(rpts([(px + x, py + y) for x, y in pts], ang, px, py), closed=True, r=S.r * 0.6)


@icon("amaryllis", CAT, "Amaryllis with a tall stem topped by three large trumpet flowers facing outward in different directions",
      tags=["amaryllis", "hippeastrum", "trumpet flower", "christmas flower", "bulb", "red flower", "winter bloom"])
def _(S):
    tr = [_trumpet(12, 11, a, 9, 5.4, S) for a in (-90, -150, -30)]
    return [*[shell(d) for d in tr], stem(12, 11, 12, GROUND)]


@icon("nasturtium", CAT, "Nasturtium with a round shield-shaped leaf with veins radiating from its centre, beside a spurred flower",
      tags=["nasturtium", "tropaeolum", "edible flower", "round leaf", "garden", "orange flower", "spurred flower"])
def _(S):
    veins = [detail(seg(7.5, 14.5, *polar(7.5, 14.5, 4.2, -90 + 72 * k))) for k in range(5)]
    return [shell(circle(7.5, 14.5, 5.5)), *veins, dot(7.5, 14.5, 1.2), line("M7.5 14.5C9 17.5 10.5 20 11.5 21.5"),
            shell(flower_d(16.5, 7.3, 4.8)), dot(16.5, 7.3, 1.0), line("M19.8 10.2C21.5 12.5 21 15 18.5 15.5"), line("M16.5 12C14 15.5 12.5 19 11.5 21.5")]


@icon("lilac", CAT, "Lilac cone-shaped cluster of tiny florets on a woody twig with a heart-shaped leaf",
      tags=["lilac", "syringa", "purple flowers", "fragrant", "spring shrub", "flower cluster", "panicle"])
def _(S):
    rows = [[(12, 4)], [(9.8, 7.2), (14.2, 7.2)], [(8.2, 10.4), (12, 10.4), (15.8, 10.4)], [(9.8, 13.6), (14.2, 13.6)]]
    cone = chain([(x, y, 2.1) for r_ in rows for x, y in r_] + [(12, 16.6, 1.9)])
    return [shell(cone), line(seg(12, 18, 12, GROUND)), line("M3.5 21.5L20.5 21.5"), shell(_heart(17.2, 16, 4.2))]


@icon("dahlia", CAT, "Dahlia seen from above with rows of pointed cupped petals in neat concentric tiers forming a geometric star",
      tags=["dahlia", "flower", "geometric flower", "tiered petals", "garden", "autumn bloom", "top view"])
def _(S):
    outer = union(*[leaf_shape(12, 12, *polar(12, 12, 10.3, -90 + 36 * k), 2.3) for k in range(10)])
    inner = [detail(leaf_shape(*polar(12, 12, 1.6, -72 + 72 * k), *polar(12, 12, 6.4, -72 + 72 * k), 1.5)) for k in range(5)]
    return [shell(outer, stroke_miterlimit="8"), *inner, dot(12, 12, 1.3)]


@icon("lupine", CAT, "Lupine with a tall tapering cone spike of small pea flowers above a hand-shaped leaf of narrow leaflets",
      tags=["lupine", "lupin", "flower spike", "bluebonnet", "cottage garden", "wildflower", "palmate leaf"])
def _(S):
    rows = [[(12, 3.9, 1.5)], [(10.3, 6.9, 1.8), (13.7, 6.9, 1.8)], [(9, 10.1, 2), (12, 10.1, 2), (15, 10.1, 2)]]
    cone = chain([c for r_ in rows for c in r_])
    return [shell(cone), line(seg(12, 12.5, 12, GROUND)), *[line(seg(12, 21.5, *polar(12, 21.5, 7.5, a))) for a in (-160, -125, -55, -20)]]


@icon("columbine", CAT, "Nodding columbine flower with five long hooked spurs curving up and back from its bell",
      tags=["columbine", "aquilegia", "spurred flower", "hooked spurs", "woodland", "nodding flower", "granny's bonnet"])
def _(S):
    return [line("M12 2.5L12 8"), shell(dbell(S, 12, 8, 8, 9)),
            line("M8.5 10C6 9.5 4.3 8 3.8 5.3"), line("M15.5 10C18 9.5 19.7 8 20.2 5.3")]


@icon("angels-trumpet", CAT, "Angel's trumpet with a large hanging trumpet flower whose pointed curled tips flare at the open mouth",
      tags=["angel's trumpet", "brugmansia", "datura", "hanging flower", "trumpet flower", "poisonous plant", "tropical"])
def _(S):
    tr = "M10.5 4.5C10.5 9.5 8 13 3.8 16.3C6 16.8 7.3 16.6 8.3 16.3L12 21.5L15.7 16.3C16.7 16.6 18 16.8 20.2 16.3C16 13 13.5 9.5 13.5 4.5Z"
    return [line("M14 2.5C12.5 2.8 12 3.5 12 4.8"), shell(tr, stroke_miterlimit="8")]


@icon("wildflowers", CAT, "Small mixed bunch of different wild blooms on thin stems of varying height growing from grass",
      tags=["wildflowers", "meadow", "field flowers", "flower meadow", "wild bouquet", "countryside", "nature"])
def _(S):
    return [stem(6.5, 12.5, 6.5, GROUND), shell(circle(6.5, 9.5, 2.9)), stem(12, 10, 12, GROUND), shell(flower_d(12, 6.3, 4.1)), dot(12, 6.3, 0.9),
            stem(17.5, 14, 17.5, GROUND), shell(leaf_shape(17.5, 14, 17.5, 8.8, 1.7)),
            line("M2.5 21.5C2.8 19 3.5 18 4.2 17"), line("M21.5 21.5C21.2 19 20.5 18 19.8 17"), line("M9.3 21.5C9.3 20 9.8 19 10.4 18.4")]


@icon("bottlebrush-flower", CAT, "Bottlebrush flower, a cylindrical spike of bristly stamens around a branch that ends in narrow leaves",
      tags=["bottlebrush", "callistemon", "australian flower", "red flower", "bristles", "brush flower", "native plant"])
def _(S):
    bristles = [line(seg(10, y, 5.8, y - 1.8)) for y in (9.5, 12.2, 14.9)] + [line(seg(14, y, 18.2, y - 1.8)) for y in (9.5, 12.2, 14.9)]
    return [line(seg(12, 21.5, 12, 16.5)), shell(rect(10, 7.5, 4, 9, L(S, 0.5, 2))), *bristles, line(seg(12, 7.5, 12, 4.5)),
            shell(leaf_shape(12, 5.5, 8, 2.6, 0.9)), shell(leaf_shape(12, 5.5, 16, 2.6, 0.9))]


# ============================================================================ chunk 4: arrangements and flower objects


@icon("flower-bud", CAT, "Closed teardrop flower bud cupped by pointed sepals at its base, on a short stem",
      tags=["bud", "flower bud", "budding", "unopened flower", "sepals", "spring growth", "blossom"])
def _(S):
    bud = union(leaf_shape(12, 15.5, 12, 2.8, 3.3), leaf_shape(12, 17, 5.5, 10.5, 1.5), leaf_shape(12, 17, 18.5, 10.5, 1.5))
    return [shell(bud, stroke_miterlimit="8"), stem(12, 17, 12, GROUND)]


@icon("wilted-flower", CAT, "Wilted flower with its head drooping down on a bent stem and its petals hanging limp",
      tags=["wilted", "wilting", "dying flower", "drooping flower", "dead flower", "withered", "neglect"])
def _(S):
    petals = union(*[leaf_shape(15.5, 9, *polar(15.5, 9, 10.5, a), 1.5) for a in (48, 69, 90, 111, 132)])
    return [line("M5 21.5C5 11 7.5 4.5 12 4.5C14.8 4.5 15.5 6.5 15.5 9"), shell(petals, stroke_miterlimit="8"),
            shell(leaf_shape(5.4, 17.5, 11, 15, 1.1))]


@icon("petal", CAT, "Single tilted rounded petal with a pointed base and a fine curved vein",
      tags=["petal", "flower petal", "rose petal", "blossom", "he loves me", "botany", "floral part"])
def _(S):
    p = "M5.5 20.5C3 13.5 5.5 6 12 3.8C17 2.3 21 4.5 20.5 9C20 14 15.5 18 10.5 19.6C8.5 20.3 6.8 20.7 5.5 20.5Z"
    return [shell(p, stroke_miterlimit="8"), detail("M8 17C9 13 11.5 9.8 15.5 8")]


@icon("falling-petals", CAT, "Several small petals drifting diagonally through the air",
      tags=["falling petals", "petals drifting", "petal shower", "blossom fall", "wind", "confetti petals", "spring breeze"])
def _(S):
    def pet(cx, cy, ang, ln=6.2, b=1.9):
        a = math.radians(ang)
        dx, dy = math.cos(a) * ln / 2, math.sin(a) * ln / 2
        return shell(leaf_shape(cx - dx, cy - dy, cx + dx, cy + dy, b), stroke_miterlimit="8")
    return [pet(6.5, 5.5, 50), pet(16.5, 6, 100), pet(10.5, 13, 20), pet(18.5, 15.3, 70), pet(6.5, 19, 120, 5.6, 1.7)]


@icon("bouquet", CAT, "Bunch of flowers with stems gathered in a cone of wrapping paper tied with a bow",
      tags=["bouquet", "bunch of flowers", "flowers", "florist", "gift", "valentine", "wedding"])
def _(S):
    cone = poly([(4.5, 12), (19.5, 12), (12, 21.5)], closed=True, r=S.r)
    heads = union(flower_d(7.8, 7.8, 4.2), flower_d(16.2, 7.8, 4.2), flower_d(12, 5.2, 3.6))
    return [shell(union(cone, heads)), detail(poly([(9.5, 13.8), (12, 15.6), (9.5, 17.4)], closed=True)),
            detail(poly([(14.5, 13.8), (12, 15.6), (14.5, 17.4)], closed=True))]


@icon("flower-basket", CAT, "Woven basket with an arched handle filled with round blooms",
      tags=["flower basket", "basket of flowers", "florist", "spring", "gift basket", "blooms", "garden"])
def _(S):
    box = poly([(4.5, 13), (19.5, 13), (17.5, 21), (6.5, 21)], closed=True, r=S.r * 0.6)
    blooms = union(circle(8, 10.8, 2.6), circle(12, 9.8, 2.8), circle(16, 10.8, 2.6))
    return [line("M5 13C5 0.5 19 0.5 19 13"), shell(union(box, blooms)), detail(seg(5.6, 17, 18.4, 17))]


@icon("lei", CAT, "Garland of flowers strung closely together in a long necklace that drapes in a U shape",
      tags=["lei", "flower garland", "hawaiian lei", "necklace of flowers", "aloha", "luau", "flower necklace"])
def _(S):
    pts = [(12 + 6.8 * math.cos(math.radians(a)), 6.2 + 11.3 * math.sin(math.radians(a))) for a in (180, 147, 118, 90, 62, 33, 0)]
    fl = [flower_d(x, y, 3.1) for x, y in pts]
    return [shell(union(*fl)), *[dot(x, y, 0.9) for x, y in pts[1:-1:2]]]


@icon("flower-crown", CAT, "Band of flowers and leaves woven into a ring, seen at a slight angle",
      tags=["flower crown", "floral crown", "festival", "coachella", "bridal", "wreath worn on head", "halo of flowers"])
def _(S):
    ring = ellipse(12, 12.5, 9, 5)
    flowers = [(12, 17.5, 3.4), (4.8, 14.8, 3.0), (19.2, 14.8, 3.0), (7.6, 8.6, 2.6), (16.4, 8.6, 2.6)]
    fu = union(*[flower_d(x, y, r) for x, y, r in flowers])
    cut = path_to_d(D(ST(ring, 2, S.cap, S.join), grow(P(fu), 1.5)))
    return [solid(cut), shell(fu), dot(12, 17.5, 1.0)]


@icon("ikebana", CAT, "Minimal Japanese flower arrangement of one tall branch, one flower and one leaf rising from a low flat dish",
      tags=["ikebana", "japanese flower arranging", "kado", "minimalist arrangement", "zen", "vase", "floral art"])
def _(S):
    dish = poly([(3.5, 17.5), (20.5, 17.5), (17.5, 21.5), (6.5, 21.5)], closed=True, r=S.r * 0.6)
    return [shell(dish), line("M14 17.5C14 11 15 6 18.5 2.5"), line("M14.6 9.5C16 8.6 17.6 8.8 19 9.8"),
            line("M9.5 17.5C9.5 15.5 9 14.5 8.5 13.5"), shell(flower_d(8.5, 10, 3.6)), shell(leaf_shape(11.6, 17.3, 6, 14.6, 1.1))]


@icon("flower-arch", CAT, "Rounded arch covered with flowers and leaves standing on two posts",
      tags=["flower arch", "floral arch", "wedding arch", "garden arch", "arbor", "ceremony", "trellis"])
def _(S):
    arcpts = [(12 + 7.6 * math.cos(math.radians(a)), 12 - 7.6 * math.sin(math.radians(a))) for a in range(0, 181, 20)]
    band = blob(*[(x, y, 2.4) for x, y in arcpts])
    return [shell(band), dot(12, 4.4, 0.9), dot(7, 6.4, 0.9), dot(17, 6.4, 0.9), line(seg(4.4, 12.5, 4.4, GROUND)), line(seg(19.6, 12.5, 19.6, GROUND))]


@icon("flower-bed", CAT, "Rectangular bed of soil edged with a border, holding a row of small flowers",
      tags=["flower bed", "garden bed", "flowerbed", "planting bed", "border", "gardening", "raised bed"])
def _(S):
    return [shell(rect(2.5, 15.5, 19, 5.5, L(S, 0.8, 2.7))), stem(6.5, 15.5, 6.5, 11.6), shell(flower_d(6.5, 9, 3)), stem(12, 15.5, 12, 10.2),
            shell(flower_d(12, 7.2, 3.3)), stem(17.5, 15.5, 17.5, 11.6), shell(flower_d(17.5, 9, 3)), dot(6.5, 9, 0.8), dot(12, 7.2, 0.9), dot(17.5, 9, 0.8)]


@icon("window-box", CAT, "Long rectangular planter on a window sill with flowers and trailing leaves",
      tags=["window box", "window planter", "sill planter", "balcony flowers", "flower box", "gardening", "trailing plants"])
def _(S):
    box = rect(3, 12.5, 18, 6.5, min(S.R, 2))
    heads = union(flower_d(7, 8, 3.4), flower_d(12, 6.5, 3.6), flower_d(17, 8, 3.4))
    return [shell(union(box, heads)), line(seg(2.5, 21.5, 21.5, 21.5)), line("M7 19C7 20.5 6 21 5 21"), line("M17 19C17 20.5 18 21 19 21")]




# ============================================================================ chunk 5: houseplants


@icon("snake-plant", CAT, "Potted snake plant with several tall stiff upright sword leaves marked with bands",
      tags=["snake plant", "sansevieria", "mother in law's tongue", "houseplant", "succulent", "air purifier", "potted plant"])
def _(S):
    lv = union(leaf_shape(10.5, 15.5, 6.5, 4.5, 1.9), leaf_shape(12, 15.5, 12, 2.5, 1.9), leaf_shape(13.5, 15.5, 17.5, 5.5, 1.9))
    return [shell(lv, stroke_miterlimit="8"), detail(seg(10.7, 8, 13.3, 8)), detail(seg(10.7, 11.5, 13.3, 11.5)), shell(pot_d(S))]


@icon("pothos", CAT, "Hanging pot with long trailing vines of heart-shaped leaves spilling over the rim",
      tags=["pothos", "devil's ivy", "epipremnum", "trailing plant", "hanging plant", "houseplant", "vine"])
def _(S):
    return [shell(poly([(7, 2.8), (17, 2.8), (15.5, 8.5), (8.5, 8.5)], closed=True, r=L(S, 0, 1.2))),
            line("M8.8 8.5C6 11 6 15 7.5 21.5"), shell(leaf_shape(6.6, 12.5, 2.6, 15, 1.4)), shell(leaf_shape(6.6, 17.5, 10.6, 20.3, 1.4)),
            line("M15.2 8.5C18 12 18 16 16.5 21.5"), shell(leaf_shape(17.6, 11.6, 21.6, 14.3, 1.4)), shell(leaf_shape(17.2, 16.8, 13.3, 19.6, 1.4))]


@icon("fiddle-leaf-fig", CAT, "Tall potted fiddle leaf fig with one stem and large violin-shaped leaves with wavy edges",
      tags=["fiddle leaf fig", "ficus lyrata", "houseplant", "indoor tree", "big leaves", "potted plant", "decor"])
def _(S):
    lv = [leaf_shape(12, 14, 4.5, 11.5, 2.4), leaf_shape(12, 10.5, 19.5, 8.5, 2.4), leaf_shape(12, 7, 5.5, 4.5, 2.2), leaf_shape(12, 4.5, 16.5, 3, 1.8)]
    return [line(seg(12, 16, 12, 3.5)), *[shell(d, stroke_miterlimit="8") for d in lv[:3]], shell(pot_d(S, 8, 16, 16.5, 21.5, 1.2))]


@icon("zz-plant", CAT, "Potted ZZ plant with an upright stem lined with pairs of glossy oval leaflets",
      tags=["zz plant", "zamioculcas", "zanzibar gem", "houseplant", "low light plant", "glossy leaves", "potted plant"])
def _(S):
    parts = [line("M12 16L12 3.5")]
    for y in (13.5, 9.5, 5.5):
        parts += [shell(leaf_shape(12, y, 6.6, y - 3.4, 1.3), stroke_miterlimit="8"), shell(leaf_shape(12, y, 17.4, y - 3.4, 1.3), stroke_miterlimit="8")]
    return parts + [shell(pot_d(S, 7.5, 16.5, 16.5, 21.5, 1.3))]


@icon("spider-plant", CAT, "Potted spider plant with arching striped grass-like leaves and a small plantlet dangling on a long runner",
      tags=["spider plant", "chlorophytum", "airplane plant", "houseplant", "hanging plant", "plantlet", "runner"])
def _(S):
    return [line("M12 15.5C11 8 6 5 3.5 12"), line("M12 15.5C13 8 18 5 20.5 10"), line("M12 15.5C12 10 9 7.5 7.5 10.5"), line("M12 15.5C12 10 14.5 8 16.5 10.5"),
            line("M20.5 10C21.3 13 21.3 15.5 20.3 17.5"), shell(leaf_shape(20.3, 17, 18.3, 21.2, 0.9)), shell(leaf_shape(20.3, 17, 22, 21, 0.8)),
            shell(pot_d(S, 7.5, 16.5, 16, 21.5, 1.3))]


@icon("aloe-vera", CAT, "Potted aloe vera with thick tapering fleshy spear leaves and small teeth along their edges",
      tags=["aloe vera", "aloe", "succulent", "medicinal plant", "sunburn", "skin care", "gel"])
def _(S):
    lv = union(leaf_shape(11, 15.5, 4, 8.5, 2.1), leaf_shape(12, 15.5, 12, 2.5, 2.3), leaf_shape(13, 15.5, 20, 8.5, 2.1))
    teeth = [detail(seg(10.4, 7, 11.3, 6.2)), detail(seg(13.6, 7, 12.7, 6.2))]
    return [shell(lv, stroke_miterlimit="8"), detail(seg(12, 13.5, 12, 6)), shell(pot_d(S))]


@icon("jade-plant", CAT, "Potted jade plant with a thick trunk and branches bearing pairs of plump round leaves",
      tags=["jade plant", "crassula", "money plant", "succulent", "lucky plant", "houseplant", "bonsai like"])
def _(S):
    def lf(x, y, a):
        return shell(rot(ellipse(x, y, 2.6, 1.9), a, x, y))
    return [line(seg(12, 16, 12, 10.5)), line("M12 12.5C10.5 10.5 9 10 7.2 9.4"), line("M12 12.5C13.5 10.5 15 10 16.8 9.4"), line("M12 10.5V6.4"),
            lf(5.4, 7.2, -50), lf(6.8, 12.2, 10), lf(18.6, 7.2, 50), lf(17.2, 12.2, -10), lf(10.4, 4.4, -25), lf(13.6, 4.4, 25),
            shell(pot_d(S, 7.5, 16.5, 16, 21.5, 1.3))]


@icon("string-of-pearls", CAT, "Pot with long strands of small round bead-like leaves trailing down",
      tags=["string of pearls", "senecio", "succulent", "hanging plant", "trailing plant", "beads", "houseplant"])
def _(S):
    beads = [dot(x, y, 1.3) for x, top in ((6.5, 12), (12, 12.5), (17.5, 12)) for y in [top + 3 * k for k in range(4)]]
    return [shell(poly([(5.5, 2.8), (18.5, 2.8), (16.5, 9), (7.5, 9)], closed=True, r=L(S, 0, 1.2))), *beads,
            line(seg(6.5, 9, 6.5, 12)), line(seg(12, 9, 12, 12.5)), line(seg(17.5, 9, 17.5, 12))]


@icon("air-plant", CAT, "Rootless tuft of curling spiky silvery leaves resting on its own, with no pot or soil",
      tags=["air plant", "tillandsia", "epiphyte", "no soil plant", "spiky", "terrarium plant", "bromeliad"])
def _(S):
    return [line("M12 19C12 12 12 8 12 3"), line("M12 19C10.2 13 7 9.5 3.5 9"), line("M12 19C13.8 13 17 9.5 20.5 9"), line("M12 19C8.8 16.5 5 16 2.8 17.5"),
            line("M12 19C15.2 16.5 19 16 21.2 17.5"), shell(circle(12, 19.5, 1.3)), line("M12 19C9.8 12.5 9.5 7.5 7 4.5"), line("M12 19C14.2 12.5 14.5 7.5 17 4.5")]


@icon("boston-fern", CAT, "Hanging pot overflowing with many arching feathery fern fronds",
      tags=["boston fern", "fern", "nephrolepis", "hanging plant", "houseplant", "fronds", "porch plant"])
def _(S):
    f1 = frond((9.5, 8.5), (4, 7), (3, 13), (5.5, 20.5), 4, 2.2)
    f2 = frond((14.5, 8.5), (20, 7), (21, 13), (18.5, 20.5), 4, 2.2)
    f3 = frond((12, 8.5), (12, 12), (12, 16), (12, 21), 3, 2.2)
    return [shell(poly([(6.5, 2.8), (17.5, 2.8), (15.5, 8.5), (8.5, 8.5)], closed=True, r=L(S, 0, 1.2))), line(f1), line(f2), line(f3)]


@icon("prayer-plant", CAT, "Potted prayer plant with broad oval leaves marked by a herringbone pattern of stripes along the midrib",
      tags=["prayer plant", "maranta", "calathea", "houseplant", "patterned leaves", "stripes", "herringbone"])
def _(S):
    l1 = rot(ellipse(8, 9, 4.2, 6.6), -22, 8, 14)
    l2 = rot(ellipse(16, 9, 4.2, 6.6), 22, 16, 14)
    def ribs(cx, sg):
        return [detail(rot_open(seg(cx, 5.5, cx, 12.5), sg * 22, cx, 14)),
                detail(rot_open(f"M{cx - 2} 7.6L{cx} 9.8L{cx + 2} 7.6", sg * 22, cx, 14))]
    return [shell(l1), shell(l2), *ribs(8, -1), *ribs(16, 1), shell(pot_d(S, 7.5, 16.5, 16, 21.5, 1.3))]


@icon("chinese-money-plant", CAT, "Potted Chinese money plant with thin stalks each ending in a round flat coin-shaped leaf",
      tags=["chinese money plant", "pilea", "pilea peperomioides", "coin plant", "ufo plant", "houseplant", "round leaves"])
def _(S):
    leaves = [(6.3, 8.3), (12, 4.8), (17.7, 8.3)]
    return [*[shell(circle(x, y, 3.4)) for x, y in leaves], *[dot(x, y, 0.9) for x, y in leaves],
            line("M12 16C11 13 8.8 11.5 7.7 11.5"), line("M12 16L12 8.2"), line("M12 16C13 13 15.2 11.5 16.3 11.5"), shell(pot_d(S, 7.5, 16.5, 16, 21.5, 1.3))]


@icon("lucky-bamboo", CAT, "Lucky bamboo stalks twisted into a spiral with small leaves at the top, standing in a glass of water",
      tags=["lucky bamboo", "dracaena sanderiana", "feng shui", "water plant", "spiral bamboo", "houseplant", "luck"])
def _(S):
    return [line("M9.5 14C7.5 11.5 11.5 9.5 9.5 7C8.4 5.6 9 4.6 9.2 3.8"), line(seg(14.5, 14, 14.5, 4.5)), line(seg(13.2, 8.6, 15.8, 8.6)),
            shell(leaf_shape(9.2, 5.6, 4, 3.6, 1.0)), shell(leaf_shape(14.5, 5.6, 20, 3.4, 1.0)),
            shell(rect(6, 13.5, 12, 8, L(S, 1, 3))), detail(seg(6.6, 16.8, 17.4, 16.8))]


@icon("terrarium", CAT, "Glass jar terrarium with small plants and pebbles inside and an open neck at the top",
      tags=["terrarium", "glass garden", "miniature garden", "moss jar", "plants in glass", "houseplant", "pebbles"])
def _(S):
    glass = "M9.5 2.8V6C5 7.5 3.8 11 3.8 14.3C3.8 18.8 7.5 21.3 12 21.3C16.5 21.3 20.2 18.8 20.2 14.3C20.2 11 19 7.5 14.5 6V2.8"
    return [line(glass), line(seg(12, 17, 12, 12.5)), shell(leaf_shape(12, 13.5, 8.5, 10.5, 1.1)), shell(leaf_shape(12, 13.5, 15.5, 10.5, 1.1)),
            dot(8, 18.3, 1.0), dot(11.2, 19.3, 1.0), dot(14.8, 18.8, 1.0)]


@icon("kokedama", CAT, "Kokedama plant growing from a round moss ball wrapped in string, hanging from a cord",
      tags=["kokedama", "moss ball", "string garden", "japanese plant art", "hanging plant", "bonsai style", "moss"])
def _(S):
    ball = poly(regular(12, 16.3, 5.7, 8, -90 + 22.5), closed=True, r=L(S, 0.3, 2.6))
    return [line(seg(12, 2.5, 12, 10.6)), shell(ball), detail("M7 14.6C9.7 17.4 14.3 17.4 17 14.6"), detail(seg(12, 17.6, 12, 21)),
            shell(leaf_shape(12, 10.6, 5.5, 6.2, 1.2)), shell(leaf_shape(12, 10.6, 18.5, 6.2, 1.2))]