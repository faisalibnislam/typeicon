"""TypeIcon Core: plants (batch plants_001): trees, leaves, branches and flowers.

Drawn from the plants themselves. Trees stand on the baseline (y 21.5) with the crown in the top half;
single leaves point up-right on a short stalk so they sit comfortably in the live area.
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


# ============================================================================ trees


def layered(back, front, gap=1.5):
    """Filled design for a drawing where front(S) parts sit in front of back(S) parts: the back is cut around the front."""
    def f():
        from dsl import filled_region
        fr = filled_region(front(LINE))
        return U(D(filled_region(back(LINE)), grow(fr, gap)), fr)
    return f


def flower_d(cx, cy, r, n=5, pr=None, start=-90.0):
    """Small blossom silhouette: n round petals around a centre."""
    pr = pr or r * 0.55
    return union(*[circle(*polar(cx, cy, r - pr, start + k * 360 / n), pr) for k in range(n)], circle(cx, cy, r - pr))


def ground(x0=2.5, x1=21.5, y=GROUND):
    return line(seg(x0, y, x1, y))


# ---------------------------------------------------------------- birch
_BIRCH_CROWN = blob((7.5, 8.5, 4.5), (12, 7, 4.5), (16.5, 8.5, 4.5))


def _birch_trunk(S):
    return rect(9.5, 9, 5, 12.5, L(S, 0, 1.5))


def _birch_front(S):
    return [shell(_birch_trunk(S)), Part("dot", rect(10.5, 12, 2.25, 1.5)), Part("dot", rect(11.25, 15.5, 2.25, 1.5)),
            Part("dot", rect(10.5, 19, 2.25, 1.25))]


@icon("birch-tree", CAT, "Birch tree with a pale banded trunk in front of a small oval crown",
      tags=["birch", "tree", "silver birch", "woodland", "forest", "bark"],
      filled=layered(lambda S: [shell(_BIRCH_CROWN)], _birch_front))
def _(S):
    return [cut_strokes(S, [_BIRCH_CROWN], region(_birch_trunk(S))), *_birch_front(S)]


def _poplar(S, x, top, w, bottom):
    return [shell(rect(x - w / 2, top, w, bottom - top, L(S, 2, w / 2))), line(seg(x, bottom, x, GROUND))]


@icon("lombardy-poplar", CAT, "Tall thin columnar poplar trees standing in a row",
      tags=["poplar", "tree", "columnar", "windbreak", "avenue", "row"])
def _(S):
    return [*_poplar(S, 8, 2.5, 6.5, 18), detail(seg(8, 9, 8, 18)), *_poplar(S, 17, 7.5, 5, 18)]


@icon("cypress-tree", CAT, "Tall narrow cypress tree shaped like a flame",
      tags=["cypress", "tree", "evergreen", "mediterranean", "italy", "conifer"])
def _(S):
    tip = L(S, "M12 2.5", "M11.4 3.2Q12 2.5 12.6 3.2")
    d = (tip + "C15 6.5 16.5 11 16 15C15.6 17.6 14 19 12 19C10 19 8.4 17.6 8 15C7.5 11 9 6.5 "
         + L(S, "12 2.5Z", "11.4 3.2Z"))
    return [shell(d, stroke_miterlimit="8"), detail("M12 9.5C11 11.5 11 14 12 16"), line(seg(12, 19, 12, GROUND))]


@icon("baobab-tree", CAT, "Baobab tree with a swollen bottle-shaped trunk and short bare branches",
      tags=["baobab", "tree", "africa", "savanna", "madagascar", "bottle tree"])
def _(S):
    trunk = L(S, "M7 21.5C5 16.5 6.5 12.5 9.5 9.5H14.5C17.5 12.5 19 16.5 17 21.5Z",
              "M8 21.5C6.3 21.5 5.2 16.5 9.2 10.2Q9.6 9.5 10.4 9.5H13.6Q14.4 9.5 14.8 10.2C18.8 16.5 17.7 21.5 16 21.5Z")
    return [shell(trunk),
            line(poly([(10.5, 9.5), (7.5, 6), (4, 6)], r=S.r)), line(seg(7.5, 6, 7.5, 3)),
            line(seg(12, 9.5, 12, 3.5)),
            line(poly([(13.5, 9.5), (16.5, 6), (20, 6)], r=S.r)), line(seg(16.5, 6, 16.5, 3))]


@icon("acacia-tree", CAT, "Savanna acacia with a flat table-top crown on a forked trunk",
      tags=["acacia", "tree", "savanna", "safari", "africa", "umbrella thorn"])
def _(S):
    crown = L(S, "M2.5 9.5C2.5 7 4.5 5 8 5H16C19.5 5 21.5 7 21.5 9.5Z",
              "M4 9.5C3 9.5 2.5 8.8 2.7 8C3.3 6.2 5.3 5 8 5H16C18.7 5 20.7 6.2 21.3 8C21.5 8.8 21 9.5 20 9.5Z")
    return [shell(crown), line(poly([(7.5, 10.5), (12, 15.5), (16.5, 10.5)], r=S.r)), line(seg(12, 15.5, 12, GROUND))]


def _tuft(cx, cy, r=3.3, skip=None):
    return [line(seg(cx, cy, *polar(cx, cy, r, a))) for a in (-90, -30, 30, 150, -150) if a != skip]


@icon("joshua-tree", CAT, "Joshua tree with crooked arms ending in spiky leaf tufts",
      tags=["joshua tree", "yucca", "desert", "mojave", "california", "tree"])
def _(S):
    return [line(poly([(12, GROUND), (12, 14), (7.5, 11), (6.5, 7)], r=S.r)),
            line(poly([(12, 15), (16.5, 11.5), (17.5, 6)], r=S.r)),
            *_tuft(6.5, 7), *_tuft(17.5, 6)]


@icon("cedar-tree", CAT, "Cedar tree with flat layered tiers of foliage on a straight trunk",
      tags=["cedar", "lebanon", "tree", "conifer", "evergreen", "tiered"])
def _(S):
    k = L(S, 1.5, 1.75)
    return [shell(rect(7.5, 2.5, 9, 3.5, k)), shell(rect(4.5, 8.5, 15, 3.5, k)), shell(rect(2.5, 14.5, 19, 3.5, k)),
            line(seg(12, 6, 12, 8.5)), line(seg(12, 12, 12, 14.5)), line(seg(12, 18, 12, GROUND))]


@icon("dragon-blood-tree", CAT, "Dragon blood tree with a dense umbrella crown on a fan of branches",
      tags=["dragon tree", "socotra", "tree", "umbrella", "dracaena", "yemen"])
def _(S):
    cap = L(S, "M2.5 9.5C3.5 5.5 7 3.5 12 3.5C17 3.5 20.5 5.5 21.5 9.5Z",
            "M4 9.5C3 9.5 2.4 8.9 2.7 8.1C4 5.2 7.4 3.5 12 3.5C16.6 3.5 20 5.2 21.3 8.1C21.6 8.9 21 9.5 20 9.5Z")
    return [shell(cap),
            line(seg(6, 10.5, 12, 16)), line(seg(12, 10.5, 12, GROUND)), line(seg(18, 10.5, 12, 16)),
            line(seg(9, 10.5, 10.4, 13)), line(seg(15, 10.5, 13.6, 13))]


@icon("mangrove-tree", CAT, "Mangrove tree standing on arched stilt roots above water",
      tags=["mangrove", "tree", "swamp", "coast", "wetland", "stilt roots"])
def _(S):
    return [shell(blob((8.5, 7.5, 3.5), (12, 5.5, 3.5), (15.5, 7.5, 3.5))), line(seg(12, 11, 12, 14)),
            line("M12 14C8.5 14 6.5 15.5 5.5 18.5"), line("M12 14C15.5 14 17.5 15.5 18.5 18.5"),
            line(seg(12, 14, 12, 18.5)),
            line("M2.5 21.5Q4.75 19.5 7 21.5T12 21.5T17 21.5T21.5 21.5")]


@icon("bonsai-tree", CAT, "Bonsai with a twisting trunk and flat foliage pads in a shallow tray",
      tags=["bonsai", "miniature tree", "japan", "zen", "potted tree", "hobby"])
def _(S):
    return [shell(poly([(3.5, 17.5), (20.5, 17.5), (19, 21.5), (5, 21.5)], closed=True, r=S.r)),
            line("M11 17.5C11 14.5 8.5 13.5 9 11C9.5 9 13 9.5 14 7.5"),
            shell(rect(11, 2.5, 10, 4, 2)), shell(rect(3, 6.5, 6.5, 3.5, L(S, 1.5, 1.75)))]


@icon("olive-tree", CAT, "Olive tree with a gnarled twisted trunk and a loose leafy crown",
      tags=["olive", "tree", "mediterranean", "grove", "greece", "orchard"])
def _(S):
    crown = blob((7.5, 8, 4), (12.5, 6, 4), (16.5, 9, 3.5))
    return [shell(crown), detail(leaf_shape(8, 9.5, 11, 6.5, 0.7)), detail(leaf_shape(13.5, 9, 16, 6.5, 0.7)),
            line("M8.5 21.5C8.5 17.5 14.5 17.5 13.5 13.5"), line("M15.5 21.5C15.5 17.5 9.5 17.5 10.5 13.5")]


@icon("elm-tree", CAT, "Vase-shaped elm tree with branches fanning up into a wide rounded crown",
      tags=["elm", "tree", "street tree", "park", "deciduous", "shade"])
def _(S):
    crown = "M3 8.5C3 5 6.5 2.5 12 2.5C17.5 2.5 21 5 21 8.5C21 10.5 19.5 11.5 17.5 11.5H6.5C4.5 11.5 3 10.5 3 8.5Z"
    return [shell(crown), line("M12 21.5V17C12 15.5 9 14.5 8 12.5"), line("M12 17C12 15.5 15 14.5 16 12.5")]


# ---------------------------------------------------------------- chunk 2

@icon("travelers-palm", CAT, "Traveler's palm with long paddle leaves spread in a flat fan",
      tags=["travelers palm", "ravenala", "madagascar", "tropical", "fan", "palm"])
def _(S):
    cx, cy = 12, 14
    parts = []
    for a in (-162, -126, -90, -54, -18):
        x1, y1 = polar(cx, cy, 3.5, a)
        x2, y2 = polar(cx, cy, 10, a)
        parts.append(shell(leaf_shape(x1, y1, x2, y2, 1.25)))
    return parts + [line(seg(12, 13, 12, GROUND))]


_CHERRY_CROWN = blob((7.5, 9, 4.5), (12, 6.5, 4.5), (16.5, 9, 4.5))


@icon("cherry-blossom-tree", CAT, "Cherry tree with a blossom-covered crown and petals drifting down",
      tags=["cherry blossom", "sakura", "tree", "spring", "japan", "hanami"])
def _(S):
    return [shell(_CHERRY_CROWN), Part("dot", flower_d(12, 8.5, 3)),
            line(seg(12, 13.5, 12, GROUND)), line(seg(12, 17, 9, 14.8)),
            shell(leaf_shape(17, 16, 19.5, 17.5, 0.8)), shell(leaf_shape(4, 16.5, 6.5, 18.5, 0.8))]


@icon("kapok-tree", CAT, "Kapok tree with a flat crown and wide plank buttress roots at the base",
      tags=["kapok", "ceiba", "rainforest", "tree", "buttress roots", "amazon"])
def _(S):
    crown = L(S, "M2.5 8C3 5 6.5 2.5 12 2.5C17.5 2.5 21 5 21.5 8Z",
              "M4 8C3 8 2.4 7.4 2.7 6.6C3.8 4.2 7.2 2.5 12 2.5C16.8 2.5 20.2 4.2 21.3 6.6C21.6 7.4 21 8 20 8Z")
    trunk = "M10.5 7.5V14C10.5 17.5 8 19.5 3.5 21.5H20.5C16 19.5 13.5 17.5 13.5 14V7.5Z"
    return [shell(union(crown, trunk)), detail(seg(12, 17, 12, GROUND))]


@icon("bare-tree", CAT, "Leafless winter tree with forking bare branches",
      tags=["bare tree", "winter", "leafless", "branches", "dormant", "tree"])
def _(S):
    return [line(seg(12, GROUND, 12, 11)),
            line("M12 14C10 12.5 7 11.5 5.5 8"), line("M12 14C14 12.5 17 11.5 18.5 8"),
            line("M12 11C11 8.5 9.5 6.5 9 3"), line("M12 11C13 8.5 14.5 6.5 15 3"),
            line(seg(6.3, 9.6, 3, 9)), line(seg(17.7, 9.6, 21, 9)), line(seg(9.6, 6.2, 6.5, 4)), line(seg(14.4, 6.2, 17.5, 4))]


@icon("dead-tree", CAT, "Dead tree with a cracked leaning trunk and broken branch stubs",
      tags=["dead tree", "withered", "drought", "spooky", "halloween", "snag"])
def _(S):
    trunk = poly([(7.5, GROUND), (14.5, GROUND), (15, 9), (13.5, 7), (12.5, 9.5), (10.5, 5.5), (9.5, 9.5)], closed=True, r=S.r * 0.5)
    return [shell(trunk, stroke_miterlimit="6"), detail(poly([(12, 12.5), (13, 15), (11.5, 18)], r=S.r * 0.5)),
            line(poly([(9.5, 13.5), (5.5, 10), (5, 7.5)], r=S.r)), line(poly([(15, 12), (19, 9)], r=S.r))]


@icon("autumn-tree", CAT, "Round tree losing its leaves in autumn with a small pile of leaves",
      tags=["autumn", "fall", "tree", "falling leaves", "season", "october"])
def _(S):
    return [shell(ellipse(9.5, 8.5, 7, 6)), line(seg(9.5, 14.5, 9.5, GROUND)),
            shell(leaf_shape(17.5, 13, 20.5, 10, 0.9)), shell(leaf_shape(15.5, 17.5, 19, 16.5, 0.9)),
            shell(L(S, "M13.5 21.5C14 19.5 16 18.5 17.5 18.5C19 18.5 21 19.5 21.5 21.5Z",
                    "M14.5 21.5C13.7 21.5 13.8 19.6 16 18.9C17 18.6 18 18.6 19 18.9C21.2 19.6 21.3 21.5 20.5 21.5Z"))]


def _snowy_tier(cx, top, bottom, half, n):
    """Pine tier: apex at top, scalloped snowy lower edge."""
    d = f"M{fmt(cx)} {fmt(top)}L{fmt(cx + half)} {fmt(bottom)}"
    w = 2 * half / n
    for k in range(n):
        x = cx + half - (k + 1) * w
        d += f"A{fmt(w / 2)} {fmt(w / 2)} 0 0 1 {fmt(x)} {fmt(bottom)}"
    return d + "Z"


@icon("snowy-pine", CAT, "Pine tree with snow resting on each tier of branches",
      tags=["snowy pine", "winter", "christmas tree", "snow", "evergreen", "fir"])
def _(S):
    tiers = union(_snowy_tier(12, 2.5, 8.5, 4.5, 3), _snowy_tier(12, 5.5, 13, 6.5, 4), _snowy_tier(12, 9.5, 18, 8.5, 5))
    return [shell(tiers), line(seg(12, 19.5, 12, GROUND))]


@icon("tree-stump", CAT, "Cut tree stump with growth rings on top and spreading roots",
      tags=["stump", "tree stump", "logging", "wood", "felled", "rings"])
def _(S):
    body = "M5 8V16C5 18.5 4.5 20 3 21.5H21C19.5 20 19 18.5 19 16V8"
    return [shell(ellipse(12, 8, 7, 3.5)), line(body), detail(ellipse(12, 8, 3.5, 1.1)),
            line(seg(9, 18.5, 8.5, GROUND)), line(seg(15, 18.5, 15.5, GROUND))]


@icon("tree-hollow", CAT, "Thick tree trunk with a dark hollow and a branch stub",
      tags=["tree hollow", "tree hole", "cavity", "owl", "squirrel", "trunk"])
def _(S):
    trunk = poly([(6.5, 2.5), (16.5, 2.5), (16.5, 17.5), (19.5, GROUND), (3.5, GROUND), (6.5, 17.5)], closed=True, r=S.r)
    return [shell(trunk), Part("dot", ellipse(11.5, 11, 2.5, 3.5)), line(poly([(16.5, 8), (20.5, 4.5)], r=0))]


@icon("tree-roots", CAT, "Small tree above the ground line with a large root system below",
      tags=["roots", "root system", "tree", "underground", "growth", "foundation"])
def _(S):
    return [shell(blob((8.5, 7.5, 3), (12, 6, 3.5), (15.5, 7.5, 3))), line(seg(12, 10.5, 12, GROUND)), line(seg(2.5, 13, 21.5, 13)),
            line(poly([(12, 15), (7, 17.5), (3.5, 21)], r=S.r)), line(poly([(12, 15), (17, 17.5), (20.5, 21)], r=S.r)),
            line(seg(8.5, 17, 8, 21.5)), line(seg(15.5, 17, 16, 21.5))]


@icon("tree-of-life", CAT, "Circle framing a tree whose crown and roots both reach the rim",
      tags=["tree of life", "symbol", "spiritual", "family tree", "growth", "celtic"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(blob((8.8, 8.5, 3), (12, 6.5, 3.5), (15.2, 8.5, 3))),
            detail(seg(12, 9, 12, 21.5)), detail(poly([(12, 15.5), (9, 17.5), (7.3, 20.2)], r=S.r)),
            detail(poly([(12, 15.5), (15, 17.5), (16.7, 20.2)], r=S.r))]


@icon("deforestation", CAT, "Row of cut tree stumps next to a single standing tree",
      tags=["deforestation", "logging", "clear cut", "environment", "climate", "forest loss"])
def _(S):
    return [shell(ellipse(6, 8.5, 3.5, 5)), line(seg(6, 13.5, 6, GROUND)),
            shell(poly([(11.5, GROUND), (11.5, 17), (15.5, 15.5), (15.5, GROUND)], closed=True, r=S.r * 0.5)),
            shell(poly([(18, GROUND), (18, 16.5), (21.5, 15), (21.5, GROUND)], closed=True, r=S.r * 0.5)),
            ground(2.5, 21.5)]


@icon("bush", CAT, "Low rounded shrub sitting on the ground",
      tags=["bush", "shrub", "garden", "hedge", "landscaping", "greenery"])
def _(S):
    b = union(blob((7, 14, 4.5), (12, 11, 5.5), (17, 14, 4.5)), rect(3.5, 14, 17, 5.5, L(S, 0, 2)))
    return [shell(b), detail(leaf_shape(7, 16.5, 10.5, 13.5, 0.8)), detail(leaf_shape(13.5, 13, 17, 16, 0.8))]


# ---------------------------------------------------------------- chunk 3: shrubs and leaves

@icon("hedge", CAT, "Long clipped hedge with a flat leafy top and straight sides",
      tags=["hedge", "hedgerow", "shrub", "garden", "border", "privacy"])
def _(S):
    top = "M2.5 20.5V9" + "".join(f"A1.9 1.9 0 0 1 {fmt(2.5 + 3.8 * (k + 1))} 9" for k in range(5)) + "V20.5Z"
    top = top if S.name == "line" else path_to_d(U(P(top), P(rect(2.5, 9, 19, 11.5, 2))))
    return [shell(top), detail(leaf_shape(6, 16.5, 9.5, 13, 0.8)), detail(leaf_shape(14.5, 13, 18, 16.5, 0.8))]


@icon("topiary", CAT, "Shrub clipped into a ball on a bare stem in a square pot",
      tags=["topiary", "clipped shrub", "boxwood", "garden", "potted plant", "decor"])
def _(S):
    return [shell(circle(12, 7.5, 5)), detail(arc(10, 7.5, 1.75, 180, 270)), line(seg(12, 12.5, 12, 15.5)),
            shell(poly([(7, 15.5), (17, 15.5), (16, GROUND), (8, GROUND)], closed=True, r=S.r))]


@icon("kadomatsu", CAT, "Three angle-cut bamboo stalks bound together at the base with pine sprigs",
      tags=["kadomatsu", "japanese new year", "bamboo", "shogatsu", "decoration", "japan"])
def _(S):
    pts = [(6.5, 15), (6.5, 8.5), (9.5, 5.5), (9.5, 4.5), (14.5, 2.5), (14.5, 7), (17.5, 5), (17.5, 15), (19, 15),
           (17.5, GROUND), (6.5, GROUND), (5, 15)]
    return [shell(poly(pts, closed=True, r=S.r * 0.4)),
            detail(seg(9.5, 5.5, 9.5, 15)), detail(seg(14.5, 7, 14.5, 15)), detail(seg(5.5, 17.5, 18.5, 17.5)),
            line(seg(4.5, 12.5, 2.5, 10.5)), line(seg(19.5, 12.5, 21.5, 10.5)), line(seg(4, 14.5, 2.5, 14)), line(seg(20, 14.5, 21.5, 14))]


def _oak():
    return blob((12, 4.5, 2.2), (8.3, 7.5, 2.2), (15.7, 7.5, 2.2), (7.5, 11.5, 2.5), (16.5, 11.5, 2.5),
                (8.5, 15.5, 2.2), (15.5, 15.5, 2.2), (12, 11.5, 4))


@icon("ginkgo-leaf", CAT, "Fan-shaped ginkgo leaf with a notch in its top edge",
      tags=["ginkgo", "maidenhair tree", "leaf", "fan leaf", "autumn", "herbal"])
def _(S):
    cx, cy, R = 12, 16, 11
    a, b = polar(cx, cy, R, -145), polar(cx, cy, R, -35)
    na, nb = polar(cx, cy, R, -93.5), polar(cx, cy, R, -86.5)
    if S.name == "line":
        d = (f"M{fmt(cx)} {fmt(cy)}L{fmt(a[0])} {fmt(a[1])}A{R} {R} 0 0 1 {fmt(na[0])} {fmt(na[1])}"
             f"L12 8.5L{fmt(nb[0])} {fmt(nb[1])}A{R} {R} 0 0 1 {fmt(b[0])} {fmt(b[1])}Z")
    else:
        d = (f"M{fmt(cx)} {fmt(cy)}L{fmt(a[0])} {fmt(a[1])}A{R} {R} 0 0 1 {fmt(na[0])} {fmt(na[1])}"
             f"Q12 5.5 12 8.5Q12 5.5 {fmt(nb[0])} {fmt(nb[1])}A{R} {R} 0 0 1 {fmt(b[0])} {fmt(b[1])}Z")
    return [shell(d, stroke_miterlimit="8"),
            detail(seg(*polar(cx, cy, 3.5, -118), *polar(cx, cy, 8, -118))),
            detail(seg(*polar(cx, cy, 3.5, -62), *polar(cx, cy, 8, -62))),
            line(seg(12, 16, 12, GROUND))]


def _fern_pts():
    ys = [(5.5, 2.5), (8.5, 4), (11.5, 5.5), (14.5, 6.5), (17.5, 6.5)]
    right = [(12, 2.5)]
    for y, w in ys:
        right += [(12 + w, y - 1.2), (12 + w * 0.3, y + 0.6)]
    right[-1] = (12.9, 19)
    left = [(24 - x, y) for x, y in reversed(right[1:])]
    return right + left


@icon("fern-frond", CAT, "Arching fern frond with pairs of small leaflets tapering to the tip",
      tags=["fern", "frond", "leaf", "forest", "woodland", "greenery"])
def _(S):
    p0, p1, p2, p3 = (7, 21.5), (7, 13), (11, 5.5), (19, 3)
    out = [line(f"M{fmt(p0[0])} {fmt(p0[1])}C{fmt(p1[0])} {fmt(p1[1])} {fmt(p2[0])} {fmt(p2[1])} {fmt(p3[0])} {fmt(p3[1])}")]
    for t, ln in ((0.3, 4.5), (0.52, 4), (0.74, 3.2)):
        x, y = bez(p0, p1, p2, p3, t)
        x2, y2 = bez(p0, p1, p2, p3, t + 0.01)
        a = math.degrees(math.atan2(y2 - y, x2 - x))
        for side in (-1, 1):
            b = a + side * 55
            out.append(shell(leaf_shape(x, y, *polar(x, y, ln, b), 0.75)))
    return out


@icon("monstera-leaf", CAT, "Heart-shaped monstera leaf with deep splits between its veins",
      tags=["monstera", "swiss cheese plant", "houseplant", "tropical", "leaf", "jungle"])
def _(S):
    tip = L(S, "M12 2.5", "M11.3 2.9Q12 2.5 12.7 2.9")
    d = (tip + "C17.5 5 20.5 8.5 20.5 13C20.5 17 17.5 19.5 14 19.5" +
         ("L12 17L10 19.5" if S.name == "line" else "Q13 19.5 12.4 18.3L12 17.5L11.6 18.3Q11 19.5 10 19.5") +
         "C6.5 19.5 3.5 17 3.5 13C3.5 8.5 6.5 5 " + L(S, "12 2.5Z", "11.3 2.9Z"))
    slits = [detail(seg(3.5, 11.5, 8.5, 13)), detail(seg(4.5, 16.5, 9, 16)), detail(seg(5.5, 6.8, 9.5, 9.5)),
             detail(seg(20.5, 11.5, 15.5, 13)), detail(seg(19.5, 16.5, 15, 16)), detail(seg(18.5, 6.8, 14.5, 9.5))]
    return [shell(d, stroke_miterlimit="6"), *slits, detail(seg(12, 6, 12, 17)), line(seg(12, 17.5, 12, GROUND))]


@icon("lily-pad", CAT, "Round lily pad with a notch floating on rippling water",
      tags=["lily pad", "water lily", "pond", "frog", "lake", "aquatic plant"])
def _(S):
    pad = ellipse(12, 10.5, 9.5, 5.5)
    cut = poly([(12, 10.5), (15.5, 18), (21, 15)], closed=True)
    d = minus(pad, cut)
    if S.name == "rounded":
        d = path_to_d(U(D(P(pad), grow(P(cut), 0.6)), I(P(pad), P(circle(12, 10.5, 1.2)))))
    return [shell(d), line("M3 19.5Q5.25 17.5 7.5 19.5T12 19.5T16.5 19.5T21 19.5")]


@icon("bodhi-leaf", CAT, "Heart-shaped sacred fig leaf with a long drip tip",
      tags=["bodhi", "peepal", "sacred fig", "buddhism", "leaf", "enlightenment"])
def _(S):
    tip = L(S, "M12 3", "M11.6 3.5Q12 3 12.4 3.5")
    d = (tip + "C12.6 6.5 13.5 7.5 15.5 9C18.5 11 19.5 13.5 19 15.5C18.5 18 15.5 19.5 12 18.5"
         "C8.5 19.5 5.5 18 5 15.5C4.5 13.5 5.5 11 8.5 9C10.5 7.5 11.4 6.5 " + L(S, "12 3Z", "11.6 3.5Z"))
    return [shell(d), detail(seg(12, 9, 12, 18.5)),
            detail(poly([(8.5, 13), (12, 15.5), (15.5, 13)], r=S.r * 0.6)), line(seg(12, 18.5, 12, GROUND))]


def _obovate(cx, cy, a, r0, r1, w):
    ln = r1 - r0
    loc = [("M", (0, 0)), ("C", (ln * 0.45, w * 0.55), (ln * 0.85, w), (ln, 0)), ("C", (ln * 0.85, -w), (ln * 0.45, -w * 0.55), (0, 0))]
    x0, y0 = polar(cx, cy, r0, a)
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))

    def T(p):
        u, v = p
        return f"{fmt(x0 + u * ca - v * sa)} {fmt(y0 + u * sa + v * ca)}"
    out = ""
    for c in loc:
        out += c[0] + " ".join(T(p) for p in c[1:])
    return out + "Z"


@icon("horse-chestnut-leaf", CAT, "Palmate horse chestnut leaf with leaflets spreading from one point",
      tags=["horse chestnut", "conker", "buckeye", "leaf", "palmate", "autumn"])
def _(S):
    cx, cy = 12, 13.5
    specs = [(-90, 11, 2.2), (-45, 10, 2.1), (-135, 10, 2.1), (-5, 8, 1.8), (-175, 8, 1.8)]
    return [shell(_obovate(cx, cy, a, 1, r1, w)) for a, r1, w in specs] + [line(seg(12, 14.5, 12, GROUND))]


@icon("sassafras-leaf", CAT, "Mitten-shaped sassafras leaf with one thumb lobe",
      tags=["sassafras", "mitten leaf", "leaf", "autumn", "forest", "tree"])
def _(S):
    body = "M13.5 18.5C9.5 16 9.5 12.5 10.5 9C11.3 5.5 13 3 15.5 3C18 3 19.5 5.5 19.5 9C19.5 13 17.5 16 13.5 18.5Z"
    thumb = rot(ellipse(8, 9.5, 2.5, 4.5), -30, 8, 9.5)
    return [shell(union(body, thumb)), detail("M13.5 18.5C14 14 14.5 10 15.5 6.5"), line(seg(13.5, 18.5, 13.5, GROUND))]


# ---------------------------------------------------------------- chunk 4: leaves, branches, twigs

def _toothed(pts, amp=0.7, every=2.2):
    """Polyline through pts with small saw teeth pointing outward (to the left of travel)."""
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        ln = math.hypot(x1 - x0, y1 - y0)
        n = max(1, round(ln / every))
        nx, ny = (y1 - y0) / ln, -(x1 - x0) / ln
        for k in range(n):
            t0 = k / n
            tm = (k + 0.7) / n
            out.append((x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0))
            out.append((x0 + (x1 - x0) * tm + nx * amp, y0 + (y1 - y0) * tm + ny * amp))
    out.append(pts[-1])
    return out


@icon("linden-leaf", CAT, "Lopsided heart-shaped linden leaf with a toothed edge and a short tip",
      tags=["linden", "lime tree", "basswood", "leaf", "heart leaf", "tilia"])
def _(S):
    d = L(S, "M12 3C16.5 5.5 20 9 20 13C20 16.5 17 18.5 13.5 17.5L12 16.5C9.5 19 5 18.5 4.5 15C4 11 7.5 6.5 12 3Z",
          "M11.5 3.4Q12 3 12.5 3.3C16.5 5.5 20 9 20 13C20 16.5 17 18.5 13.5 17.5Q12.8 17.3 12.3 16.8Q12 16.5 11.7 16.8"
          "C9.5 19 5 18.5 4.5 15C4 11 7.5 6.5 11.5 3.4Z")
    return [shell(d), detail(seg(12, 7, 12, 16.5)), detail(seg(12, 11, 15.5, 9)), detail(seg(12, 13, 8, 11.5)),
            line(seg(12, 16.5, 12.5, GROUND))]


@icon("chestnut-leaf", CAT, "Long narrow chestnut leaf with a saw-toothed edge and straight side veins",
      tags=["chestnut", "sweet chestnut", "leaf", "autumn", "serrated", "forest"])
def _(S):
    right = [(12, 2.5), (15.2, 7), (15.8, 11.5), (14.5, 16), (12, 19)]
    left = [(24 - x, y) for x, y in reversed(right)]
    pts = _toothed(right, 0.9, 2.3)[:-1] + _toothed(left, 0.9, 2.3)[:-1]
    pts = rpts(pts, 35, 12, 12)
    mid = rpts([(12, 6), (12, 19), (12, 21.5)], 35, 12, 12)
    veins = []
    for y in (9.5, 13.5):
        for sx in (1, -1):
            a, b = rpts([(12, y + 1.5), (12 + sx * 2.8, y - 0.5)], 35, 12, 12)
            veins.append(detail(seg(*a, *b)))
    return [shell(poly(pts, closed=True, r=S.r * 0.2), stroke_miterlimit="6"), detail(seg(*mid[0], *mid[1])), *veins,
            line(seg(*mid[1], *mid[2]))]


@icon("ash-leaf", CAT, "Compound ash leaf with paired oval leaflets and one at the tip",
      tags=["ash", "ash tree", "compound leaf", "pinnate", "leaflets", "fraxinus"])
def _(S):
    out = [line(seg(12, GROUND, 12, 8))]
    for y in (17, 11.5):
        out += [shell(leaf_shape(12, y, 5, y - 3, 1.3)), shell(leaf_shape(12, y, 19, y - 3, 1.3))]
    out.append(shell(leaf_shape(12, 8, 12, 2.5, 1.4)))
    return out


@icon("pine-branch", CAT, "Evergreen pine bough with short needles bristling along both sides",
      tags=["pine branch", "fir branch", "bough", "evergreen", "christmas", "winter"])
def _(S):
    ax, ay, bx, by = 3.5, 20.5, 19.5, 4.5
    out = [line(seg(ax, ay, bx, by))]
    ang = math.degrees(math.atan2(by - ay, bx - ax))
    for t, ln in ((0.3, 4.5), (0.48, 4.5), (0.66, 4), (0.84, 3.2)):
        x, y = ax + (bx - ax) * t, ay + (by - ay) * t
        out += [line(seg(x, y, *polar(x, y, ln, ang - 60))), line(seg(x, y, *polar(x, y, ln, ang + 60)))]
    return out


@icon("olive-branch", CAT, "Curved olive twig with narrow leaves and two hanging olives",
      tags=["olive branch", "peace", "olive", "mediterranean", "harvest", "twig"])
def _(S):
    p0, p1, p2, p3 = (3.5, 21), (7, 14), (12, 8), (20.5, 3.5)
    out = [line(f"M{fmt(p0[0])} {fmt(p0[1])}C{fmt(p1[0])} {fmt(p1[1])} {fmt(p2[0])} {fmt(p2[1])} {fmt(p3[0])} {fmt(p3[1])}")]
    for t, ln, side in ((0.3, 6, -1), (0.55, 6, -1), (0.8, 5, -1), (0.42, 5.5, 1)):
        x, y = bez(p0, p1, p2, p3, t)
        x2, y2 = bez(p0, p1, p2, p3, t + 0.01)
        a = math.degrees(math.atan2(y2 - y, x2 - x))
        out.append(shell(leaf_shape(x, y, *polar(x, y, ln, a + side * 45), 1)))
    out += [Part("dot", ellipse(16.5, 13.5, 1.9, 2.4)), line(seg(15.2, 7.1, 16.3, 11))]
    return out


@icon("laurel-wreath", CAT, "Open wreath of two laurel branches with leaves meeting at the bottom",
      tags=["laurel", "wreath", "victory", "award", "winner", "honor"])
def _(S):
    cx, cy, R = 12, 12, 7.5
    out = [line(arc(cx, cy, R, 95, 230)), line(arc(cx, cy, R, -50, 85))]
    for sgn, angs in ((-1, (118, 158, 198)), (1, (62, 22, -18))):
        for a in angs:
            x, y = polar(cx, cy, R, a)
            tang = a + 90 if sgn < 0 else a - 90
            out.append(shell(leaf_shape(x, y, *polar(x, y, 3.8, tang + 45 * sgn), 0.9)))
    tl, tr = polar(cx, cy, R, 230), polar(cx, cy, R, -50)
    out += [shell(leaf_shape(*tl, *polar(*tl, 3.8, 230 + 90 + 10), 0.9)), shell(leaf_shape(*tr, *polar(*tr, 3.8, -50 - 90 - 10), 0.9))]
    return out


@icon("leafy-twig", CAT, "Short woody twig with three alternating leaves and a bud at the tip",
      tags=["twig", "sprig", "leaves", "spring", "branch", "nature"])
def _(S):
    out = [line(seg(4.5, 20.5, 16.5, 6.5))]
    for t, side in ((0.28, 1), (0.55, -1), (0.8, 1)):
        x, y = 4.5 + 12 * t, 20.5 - 14 * t
        a = -49.4 + side * 55
        out.append(shell(leaf_shape(x, y, *polar(x, y, 6, a), 1.4)))
    out.append(shell(ellipse(18, 4.8, 1.6, 1.6) if S.name == "rounded" else leaf_shape(16.5, 6.5, 19.5, 3, 1)))
    return out


@icon("tree-branch", CAT, "Branch splitting into two limbs, each with a few leaves",
      tags=["branch", "bough", "limb", "tree", "leaves", "wood"])
def _(S):
    out = [shell(poly([(2.5, 15.5), (10.5, 13), (11, 15.5), (2.5, 19)], closed=True, r=S.r * 0.5)),
           line(poly([(10.5, 13.5), (15, 9.5), (18, 4)], r=S.r)), line(poly([(11, 14.5), (16.5, 15), (21.5, 13)], r=S.r))]
    out += [shell(leaf_shape(15, 9.5, 20.5, 8.5, 1.1)), shell(leaf_shape(15.5, 10, 11.5, 5.5, 1.1)),
            shell(leaf_shape(16.5, 15, 19, 20, 1.1))]
    return out


@icon("twig", CAT, "Bare forked twig with small pointed buds along it and at the tips",
      tags=["twig", "stick", "branch", "bud", "winter", "wood"])
def _(S):
    out = [line(seg(6, 21.5, 12, 11)), line(seg(12, 11, 11, 5.5)), line(seg(12, 11, 16.5, 7))]
    out += [shell(leaf_shape(11, 5.5, 10.6, 2.5, 0.8)), shell(leaf_shape(16.5, 7, 18.9, 5, 0.8)),
            shell(leaf_shape(9, 16, 5.5, 14.5, 0.8)), shell(leaf_shape(11, 12.8, 14.5, 13.5, 0.8))]
    return out


@icon("leaf-skeleton", CAT, "Leaf outline filled with a fine network of branching veins",
      tags=["leaf skeleton", "veins", "venation", "botany", "biology", "leaf"])
def _(S):
    d = "M12 2.5C16.5 6 18.5 9.5 18 13.5C17.5 17 15 19 12 19C9 19 6.5 17 6 13.5C5.5 9.5 7.5 6 12 2.5Z"
    return [line(d), line(seg(12, 5, 12, GROUND)),
            line(poly([(8, 9.5), (12, 12.5), (16, 9.5)], r=S.r * 0.6)), line(poly([(7.5, 14), (12, 17), (16.5, 14)], r=S.r * 0.6)),
            line(seg(9.5, 11.2, 9.5, 8.5)), line(seg(14.5, 11.2, 14.5, 8.5)), line(seg(9.3, 15.3, 9.3, 18)), line(seg(14.7, 15.3, 14.7, 18))]


_PILE_C = leaf_shape(7.5, 14.5, 15.5, 8, 1.8)
_PILE_A = leaf_shape(2.5, 20, 11, 15, 1.6)
_PILE_B = leaf_shape(10.5, 16, 21.5, 20, 1.6)


def _pile_filled():
    a, b, c = region(_PILE_A), region(_PILE_B), region(_PILE_C)
    b2 = D(b, grow(c, 1.5))
    a2 = D(a, grow(U(b, c), 1.5))
    return U(a2, b2, c)


@icon("leaf-pile", CAT, "Small heap of overlapping fallen leaves on the ground",
      tags=["leaf pile", "fallen leaves", "autumn", "fall", "raking", "yard"], filled=_pile_filled)
def _(S):
    return [cut_strokes(S, [_PILE_A], U(region(_PILE_B), region(_PILE_C))), cut_strokes(S, [_PILE_B], region(_PILE_C)),
            shell(_PILE_C), detail(seg(9.5, 13, 13.5, 9.5))]


@icon("falling-leaves", CAT, "Two leaves drifting down with curved motion lines",
      tags=["falling leaves", "autumn", "fall", "wind", "season", "leaves"])
def _(S):
    return [shell(leaf_shape(3.5, 11, 11, 5, 1.6)), shell(leaf_shape(12, 20.5, 19.5, 14.5, 1.6)),
            line("M13.5 3C16 2.5 18 3.5 18.5 6.5"), line("M4.5 16C7 15 9 15.5 10 18")]


@icon("leaf-dewdrop", CAT, "Leaf with a round water drop resting near its tip",
      tags=["dew", "dewdrop", "water drop", "leaf", "morning", "fresh"])
def _(S):
    leaf = "M20.5 3.5C21 11 18 18 10.5 19C6.5 19.5 4.5 17 5 13C5.5 7 12 3.5 20.5 3.5Z"
    drop = L(S, "M14.5 6.5L16.8 9.8A2.8 2.8 0 1 1 12.2 9.8Z", "M14.1 7.1Q14.5 6.5 14.9 7.1L16.8 9.8A2.8 2.8 0 1 1 12.2 9.8Z")
    return [shell(leaf), detail(drop), detail(seg(7.5, 16.5, 11.5, 13.5)),
            line(seg(6.5, 17.5, 3, 21))]


@icon("frosted-leaf", CAT, "Leaf with a small snowflake of frost on its surface",
      tags=["frost", "frosted", "winter", "leaf", "cold", "freeze"])
def _(S):
    leaf = "M20.5 3.5C21 11 18 18 10.5 19C6.5 19.5 4.5 17 5 13C5.5 7 12 3.5 20.5 3.5Z"
    cx, cy, r = 13.2, 11, 3.6
    flake = [detail(seg(*polar(cx, cy, r, a), *polar(cx, cy, r, a + 180))) for a in (-90, -30, 30)]
    return [shell(leaf), *flake, line(seg(6.5, 17.5, 3, 21))]


@icon("leaf-spot", CAT, "Leaf marked with several round ringed disease spots",
      tags=["leaf spot", "plant disease", "fungus", "blight", "garden pest", "leaf"])
def _(S):
    d = "M12 2.5C16.5 6 18.5 9.5 18 13.5C17.5 17 15 19 12 19C9 19 6.5 17 6 13.5C5.5 9.5 7.5 6 12 2.5Z"
    tip = L(S, "M12 2.5", "M11.2 3.1Q12 2.5 12.8 3.1")
    d = tip + d[len("M12 2.5"):-len("12 2.5Z")] + L(S, "12 2.5Z", "11.2 3.1Z")
    return [shell(d, stroke_miterlimit="8"), detail(circle(12, 8.5, 1.75)), detail(circle(9.5, 14, 1.75)), detail(circle(14.8, 13.5, 1.5)),
            line(seg(12, 19, 12, GROUND))]


# ---------------------------------------------------------------- chunk 5: leaves and flowers

_VAR_LEAF = "M12 2.5C16.5 6 18.5 9.5 18 13.5C17.5 17 15 19 12 19C9 19 6.5 17 6 13.5C5.5 9.5 7.5 6 12 2.5Z"
_VAR_WAVE = "M12 5.5Q10.5 7.5 12 9.5T12 13.5T12 17.5V19"


@icon("variegated-leaf", CAT, "Leaf split along a wavy midline into a solid half and a pale half",
      tags=["variegated", "leaf", "houseplant", "two tone", "pattern", "foliage"])
def _(S):
    tip = L(S, "M12 2.5", "M11.2 3.1Q12 2.5 12.8 3.1")
    d = tip + _VAR_LEAF[len("M12 2.5"):-len("12 2.5Z")] + L(S, "12 2.5Z", "11.2 3.1Z")
    left = I(P(d), P("M12 2Q12 4 12 5.5Q10.5 7.5 12 9.5T12 13.5T12 17.5V20H2V2Z"))
    return [shell(d, stroke_miterlimit="8"), solid(path_to_d(left)), detail(_VAR_WAVE), line(seg(12, 19, 12, GROUND))]


@icon("leaf-bud", CAT, "Pointed closed bud with overlapping scales at the tip of a twig",
      tags=["bud", "leaf bud", "spring", "twig", "growth", "dormant"])
def _(S):
    bud = leaf_shape(11.5, 13.5, 18.5, 3, 2.6)
    return [shell(bud), detail("M12.5 12C12.5 9.5 14 7.5 16.5 6"), line(poly([(11.5, 13.5), (8.5, 17.5), (6.5, GROUND)], r=S.r)),
            shell(leaf_shape(8.5, 17.5, 4.5, 15.5, 0.8))]


@icon("lily", CAT, "Open lily flower with six pointed petals and long stamens",
      tags=["lily", "flower", "stargazer", "bloom", "wedding", "easter lily"])
def _(S):
    cx, cy = 12, 12
    petals = union(*[leaf_shape(cx, cy, *polar(cx, cy, 9.5, -90 + 60 * k + 30), 2.1) for k in range(6)], circle(cx, cy, 2.5))
    stamens = [detail(seg(*polar(cx, cy, 1, a), *polar(cx, cy, 5, a))) for a in (-120, -90, -60)]
    tips = [Part("dot", circle(*polar(cx, cy, 5.8, a), 1.1)) for a in (-120, -90, -60)]
    return [shell(petals, stroke_miterlimit="8"), *stamens, *tips]


@icon("orchid", CAT, "Orchid flower with broad side petals, narrow sepals and a frilled lip",
      tags=["orchid", "flower", "exotic", "houseplant", "phalaenopsis", "bloom"])
def _(S):
    cx, cy = 12, 10
    top = leaf_shape(cx, cy, 12, 2.5, 1.8)
    sl, sr = leaf_shape(cx, cy, 5, 17, 1.6), leaf_shape(cx, cy, 19, 17, 1.6)
    pl = rot(ellipse(7, 8.5, 4, 3), -20, 7, 8.5)
    pr = rot(ellipse(17, 8.5, 4, 3), 20, 17, 8.5)
    body = union(top, sl, sr, pl, pr, circle(cx, cy, 2.5))
    lip = "M9 13.5C9 12 10.5 11.5 12 11.5C13.5 11.5 15 12 15 13.5L14.5 16.5L13.2 15.5L12 17L10.8 15.5L9.5 16.5Z"
    return [shell(union(body, lip), stroke_miterlimit="6"), Part("dot", circle(cx, 9.5, 1.3)),
            line("M12 17C12 19 11.5 20.5 10.5 21.5")]


def _sakura_petals(cx, cy, S):
    ps = []
    for k in range(5):
        a = -90 + 72 * k
        c = circle(*polar(cx, cy, 5, a), 3.6)
        notch = poly([polar(cx, cy, 6.5, a), polar(cx, cy, 10, a - 12), polar(cx, cy, 10, a + 12)], closed=True)
        ps.append(minus(c, notch))
    return union(*ps, circle(cx, cy, 3))


@icon("cherry-blossom", CAT, "Cherry blossom with five notched petals and a dotted centre",
      tags=["cherry blossom", "sakura", "spring", "japan", "flower", "hanami"])
def _(S):
    cx, cy = 12, 12.5
    return [shell(_sakura_petals(cx, cy, S)), detail(circle(cx, cy, 1.8)),
            *[dot(*polar(cx, cy, 4.2, -90 + 72 * k + 36), 0.9) for k in range(5)]]


@icon("blossom-branch", CAT, "Thin crooked branch with small blossoms and buds",
      tags=["blossom", "branch", "spring", "cherry", "plum blossom", "flowering"])
def _(S):
    return [line(poly([(3, 21), (9, 15.5), (11.5, 16), (16.5, 9.5), (21, 7.5)], r=S.r)), line(seg(16.5, 9.5, 16, 4)),
            shell(flower_d(8.5, 10, 3.3)), shell(flower_d(18, 14.5, 3)), dot(16, 3.2, 1.5), dot(4, 16.5, 1.4)]


@icon("dandelion", CAT, "Round fluffy dandelion seed head on a thin stem with seeds blowing away",
      tags=["dandelion", "wish", "seed head", "clock", "weed", "summer"])
def _(S):
    cx, cy = 11, 8.5
    spokes = [line(seg(*polar(cx, cy, 1.8, a), *polar(cx, cy, 5.5, a))) for a in range(-180, 150, 36) if a not in (72, 108)]
    return [dot(cx, cy, 1.8), *spokes, line(seg(cx, cy + 1.5, 11, GROUND)),
            line(seg(18, 6, 20, 4)), dot(17.6, 6.4, 0.9), line(seg(19, 12, 21.5, 11)), dot(18.5, 12.2, 0.9)]


@icon("dandelion-seed", CAT, "Single dandelion seed with a thin stalk and an umbrella of fine hairs",
      tags=["dandelion seed", "seed", "wind", "float", "pappus", "wish"])
def _(S):
    cx, cy = 12, 10
    angs = (-162, -126, -90, -54, -18)
    return [*[line(seg(*polar(cx, cy, 2.2, a), *polar(cx, cy, 8, a))) for a in angs],
            *[dot(*polar(cx, cy, 8, a), 1.1) for a in angs],
            line(seg(cx, cy, cx, 17)), shell(leaf_shape(12, 17, 12, GROUND, 0.9))]


@icon("poppy", CAT, "Poppy flower with four broad petals around a dark centre on a curved stem",
      tags=["poppy", "flower", "remembrance", "red flower", "field", "bloom"])
def _(S):
    cx, cy = 12, 9.5
    petals = union(*[circle(*polar(cx, cy, 3.4, 45 + 90 * k), 4.1) for k in range(4)])
    return [shell(petals), Part("dot", circle(cx, cy, 2.6)), line("M12 16.5C12 18.5 12.5 20 13.5 21.5"),
            line("M12.4 19C14.5 18.5 16 17 16.5 15.5")]


@icon("iris-flower", CAT, "Iris flower with upright petals and petals falling outward on a tall stem",
      tags=["iris", "flower", "fleur", "bearded iris", "spring", "garden"])
def _(S):
    up = union(leaf_shape(12, 10, 12, 2.5, 2), leaf_shape(11, 10, 7.5, 4.5, 1.2), leaf_shape(13, 10, 16.5, 4.5, 1.2))
    fl = "M11 9.5C8 8.5 4.5 9.5 3.5 12.5C5.5 12 7.5 13 8 15C9.5 13.5 11 12 11 9.5Z"
    fr = "M13 9.5C16 8.5 19.5 9.5 20.5 12.5C18.5 12 16.5 13 16 15C14.5 13.5 13 12 13 9.5Z"
    return [shell(union(up, fl, fr)), line(seg(12, 11.5, 12, GROUND)), shell(leaf_shape(12, 21, 16.5, 15.5, 0.9))]


@icon("daffodil", CAT, "Daffodil with six broad pointed petals around a frilled central trumpet",
      tags=["daffodil", "narcissus", "spring", "flower", "easter", "wales"])
def _(S):
    cx, cy = 12, 10.5
    petals = union(*[leaf_shape(cx, cy, *polar(cx, cy, 8, -90 + 60 * k), 2.6) for k in range(6)])
    cup = poly([polar(cx, cy, 3.8 if k % 2 == 0 else 3.1, -90 + 30 * k) for k in range(12)], closed=True, r=S.r * 0.3)
    return [shell(petals, stroke_miterlimit="8"), detail(cup), dot(cx, cy, 1.2), line(seg(12, 18.5, 12, GROUND))]


def _bell2(cx, top, S):
    """Hanging bell whose mouth ends in three turned-back petal tips; top centre at (cx, top)."""
    y1, y2 = top + 4, top + 5.8
    tips = [(cx + 3, y2), (cx + 1.5, y1 + 0.6), (cx, y2), (cx - 1.5, y1 + 0.6), (cx - 3, y2)]
    return (f"M{fmt(cx - 2)} {fmt(top + 2)}C{fmt(cx - 2)} {fmt(top - 0.5)} {fmt(cx + 2)} {fmt(top - 0.5)} {fmt(cx + 2)} {fmt(top + 2)}"
            f"L{fmt(cx + 2)} {fmt(y1)}" + "".join(f"L{fmt(x)} {fmt(y)}" for x, y in tips) + f"L{fmt(cx - 2)} {fmt(y1)}Z")


@icon("bluebell", CAT, "Arching stem with bell flowers hanging along one side",
      tags=["bluebell", "hyacinthoides", "wildflower", "woodland", "spring", "bell flower"])
def _(S):
    return [line("M4.5 21.5C4.5 12 7 5 13 3.8C15.5 3.3 17.5 3.8 19 5"),
            line(seg(9.6, 5.5, 10.5, 8)), shell(_bell2(10.5, 8.5, S)), line(seg(16.5, 3.8, 16.5, 6.5)), shell(_bell2(16.5, 7, S))]


@icon("snowdrop", CAT, "Drooping snowdrop flower hanging from a bent stem beside a narrow leaf",
      tags=["snowdrop", "galanthus", "winter flower", "spring", "white flower", "bulb"])
def _(S):
    cx, top = 15.5, 7.5
    petals = union(leaf_shape(cx, top, cx, top + 8.5, 1.6), leaf_shape(cx, top, cx - 3.5, top + 7, 1.3), leaf_shape(cx, top, cx + 3.5, top + 7, 1.3))
    return [line("M10 21.5V8C10 5.5 11.5 3.5 13.5 3.5C15 3.5 15.5 4.5 15.5 5.5"), dot(cx, 6.6, 1.3), shell(petals),
            shell(leaf_shape(8.5, GROUND, 4, 10, 1.2))]
