"""TypeIcon Core: crops, field systems, soil, irrigation and farm gear (batch crops_001).

Original drawings from the objects themselves, simplified to read at 24 px.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path

CAT = "crops"


def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def mark(d) -> Part:
    """Small solid shape: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def rotd(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def orect(cx, cy, w, h, rx=0.0, deg=0.0):
    return rotd(rect(cx - w / 2, cy - h / 2, w, h, rx), deg, cx, cy)


def leaf(x1, y1, x2, y2, w):
    """Lens shaped leaf from (x1,y1) to (x2,y2); w is the bulge of each side."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy) or 1
    nx, ny = -dy / n * w * 2, dx / n * w * 2
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx)} {fmt(my + ny)} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(mx - nx)} {fmt(my - ny)} {fmt(x1)} {fmt(y1)}Z")


def star(cx, cy, ro, ri, n, start=-90.0, r=0.0):
    pts = []
    for i in range(n * 2):
        pts.append(polar(cx, cy, ro if i % 2 == 0 else ri, start + i * 180 / n))
    return poly(pts, closed=True, r=r)


def ground(y=21.5, x1=2, x2=22):
    return line(seg(x1, y, x2, y))



def arrow_arc(cx, cy, r, a1, a2, hs=2.6, S=None):
    """Clockwise arc from a1 to a2 degrees with a chevron arrowhead at the end."""
    tip = polar(cx, cy, r, a2)
    th = math.radians(a2)
    tx, ty = -math.sin(th), math.cos(th)
    pts = []
    for sgn in (1, -1):
        ang = math.radians(sgn * 40)
        bx, by = -tx, -ty
        vx = bx * math.cos(ang) - by * math.sin(ang)
        vy = bx * math.sin(ang) + by * math.cos(ang)
        pts.append((tip[0] + vx * hs, tip[1] + vy * hs))
    return [line(arc(cx, cy, r, a1, a2)), line(poly([pts[0], tip, pts[1]], r=(S.r * 0.4 if S else 0)))]

# ============================================================================ crop plants

@icon("sugar-beet", CAT, "Tapered root crop with ridges, topped by a tuft of broad upright leaves",
      tags=["beet", "sugar crop", "root vegetable", "beetroot", "sugar", "farm", "harvest"])
def _(S):
    root = "M6.5 11H17.5C17.5 16 14.5 20 12 21.5C9.5 20 6.5 16 6.5 11Z"
    leaves = union(leaf(12, 11, 6.5, 3.5, 2.2), leaf(12, 11, 12, 2, 2.2), leaf(12, 11, 17.5, 3.5, 2.2))
    return [shell(union(root, leaves)), detail(seg(9, 14.5, 15, 14.5))]


@icon("black-pepper-vine", CAT, "Vine twining up a pole with a heart shaped leaf and a hanging spike of peppercorns",
      tags=["peppercorn", "pepper vine", "spice", "piper nigrum", "climber", "plantation", "farm"])
def _(S):
    return [
        line(seg(5, 2.5, 5, 22)),
        line("M5 20C10 18 10 15 5 13C10 11 10 8 5 6"),
        shell(leaf(10.2, 9.5, 18.5, 5, 2.8)),
        dot(15, 14, 1.3), dot(18.5, 14, 1.3), dot(16.8, 17.5, 1.3), dot(15, 20.7, 1.3), dot(18.6, 20.7, 1.3),
    ]


@icon("castor-plant", CAT, "Large star shaped lobed leaf beside an upright cluster of round seed capsules",
      tags=["castor bean", "ricinus", "castor oil", "oilseed", "palmate leaf", "seed pods", "farm"])
def _(S):
    return [
        shell(star(8.5, 10, 6.3, 3.3, 5, -90, S.r)),
        line(seg(8.5, 12, 8.5, 21)),
        line(seg(18.5, 3, 18.5, 21)),
        dot(16.6, 7, 1.6), dot(20.4, 10.5, 1.6), dot(16.6, 14, 1.6), dot(20.4, 17.5, 1.6),
    ]


@icon("safflower", CAT, "Thistle like flower head with a bract cup and a tuft of thread like florets on a stem",
      tags=["carthamus", "oilseed", "thistle", "dye plant", "flower head", "farm", "bloom"])
def _(S):
    cup = "M7 12C7 17 9.5 19 12 19C14.5 19 17 17 17 12Z"
    return [
        shell(cup),
        line("M8.5 12L4 6.5"), line("M12 12V3"), line("M15.5 12L20 6.5"),
        line(seg(12, 19, 12, 22)),
        shell(leaf(12, 21.5, 19, 17.5, 1.6)),
    ]


@icon("sesame-plant", CAT, "Upright stem with narrow leaves and ribbed seed capsules, the top capsule split open",
      tags=["sesame", "til", "oilseed", "seed pod", "capsule", "benne", "farm"])
def _(S):
    return [
        line(seg(12, 8, 12, 22)),
        line(poly([(8.5, 2.5), (12, 8), (15.5, 2.5)], r=S.r * 0.7)),
        shell(rect(14.5, 10, 4, 5, 2)),
        shell(rect(5.5, 12, 4, 5, 2)),
        shell(rect(14.5, 17, 4, 4, 2)),
    ]


@icon("date-palm", CAT, "Palm with a tall trunk, arching fronds and a cluster of dates hanging below the crown",
      tags=["palm tree", "dates", "oasis", "phoenix", "orchard", "desert crop", "fruit tree"])
def _(S):
    return [
        line(seg(12, 13.5, 12, 22)),
        line("M12 8C9 3 5 3 2.5 6.5"), line("M12 8C15 3 19 3 21.5 6.5"),
        line("M12 8C8.5 7.5 5.5 9.5 4 13"), line("M12 8C15.5 7.5 18.5 9.5 20 13"),
        line(seg(12, 8, 12, 2.5)),
        dot(9.2, 12, 1.4), dot(14.8, 12, 1.4),
    ]


@icon("cork-oak", CAT, "Gnarled oak tree with a stripped smooth lower trunk and a rough band where the cork bark stops",
      tags=["cork tree", "quercus suber", "bark", "wine cork", "tree", "forestry", "harvest"])
def _(S):
    canopy = union(circle(7.5, 8.5, 4.5), circle(16.5, 8.5, 4.5), circle(12, 5.5, 4.5))
    trunk = rect(9, 10, 6, 12, L(S, 0, 1))
    return [
        shell(union(canopy, trunk)),
        detail(seg(9, 16.5, 15, 16.5)),
    ]


@icon("cacao-tree", CAT, "Tree trunk with ribbed oval pods growing straight from it and a leafy canopy above",
      tags=["cocoa", "cacao pod", "chocolate", "theobroma", "plantation", "tropical", "tree"])
def _(S):
    canopy = union(circle(7.5, 6.5, 3.8), circle(16.5, 6.5, 3.8), circle(12, 5, 3.8))
    return [
        shell(canopy),
        line(seg(12, 9, 12, 22)),
        shell(ellipse(8, 16, 2, 3.6)),
        shell(ellipse(16, 14.5, 2, 3.6)),
    ]


@icon("moringa", CAT, "Branch of small round leaflets with long thin drumstick pods hanging straight down",
      tags=["drumstick tree", "moringa oleifera", "superfood", "pods", "leaves", "tropical", "plant"])
def _(S):
    return [
        line(seg(2.5, 5, 21.5, 5)),
        dot(5, 8, 1.3), dot(9, 8, 1.3), dot(15, 8, 1.3), dot(19, 8, 1.3),
        solid(leaf(7, 8, 7, 21, 1.2)), solid(leaf(12, 7, 12, 22, 1.2)), solid(leaf(17, 8, 17, 19, 1.2)),
    ]


@icon("finger-millet", CAT, "Stalk topped by a hand shaped head of curved grain spikes spreading like fingers",
      tags=["ragi", "eleusine", "millet", "cereal", "grain", "small grain", "harvest"])
def _(S):
    return [
        line(seg(12, 12, 12, 22)),
        line("M12 12C8 10 5.5 7.5 4.5 3"), line("M12 12C10.5 9.5 8.5 6 8.5 2.5"),
        line("M12 12C13.5 9.5 15.5 6 15.5 2.5"), line("M12 12C16 10 18.5 7.5 19.5 3"),
        shell(leaf(12, 21, 18.5, 16, 1.5)),
    ]


@icon("alfalfa", CAT, "Branching stem with oval leaves in threes, topped by a compact cluster of tiny pea flowers",
      tags=["lucerne", "forage", "hay", "legume", "pasture", "fodder", "clover family"])
def _(S):
    return [
        shell(ellipse(12, 6, 3, 4)),
        line(seg(12, 10, 12, 22)),
        shell(leaf(12, 15, 4.5, 13, 2)), shell(leaf(12, 15, 19.5, 13, 2)),
        shell(leaf(12, 21, 6, 20, 1.6)), shell(leaf(12, 21, 18, 20, 1.6)),
    ]


@icon("yam", CAT, "Large elongated rough skinned tuber, slightly bent, with one cut end showing pale flesh",
      tags=["tuber", "root vegetable", "sweet potato", "cassava", "tropical crop", "staple", "harvest"])
def _(S):
    body = "M3.5 17C3 13 7 10.5 11 11C15 11.5 17 8 19.5 6.5C21.5 7 21.5 10 19 13C16 18 11 21.5 6.5 20.5C5 20 3.7 18.8 3.5 17Z"
    return [
        shell(body),
        detail("M17 8.5C18.5 9.5 19 11 18.5 12"),
        dot(8, 16.5, 0.9), dot(12, 16, 0.9),
    ]


@icon("wheat-field", CAT, "Rows of upright wheat ears standing across a field above a low ground line",
      tags=["wheat", "grain field", "cereal", "harvest", "farmland", "crops", "ears"])
def _(S):
    return [
        ground(21.5),
        line(seg(5, 13, 5, 21)), line(seg(12, 11, 12, 21)), line(seg(19, 13, 19, 21)),
        shell(leaf(5, 5, 5, 13, 1.4)), shell(leaf(12, 3, 12, 11, 1.4)), shell(leaf(19, 5, 19, 13, 1.4)),
    ]


@icon("sunflower-field", CAT, "Row of tall sunflowers with round seed heads facing forward above a horizon line",
      tags=["sunflowers", "oilseed", "farmland", "bloom", "summer", "crops", "meadow"])
def _(S):
    return [
        ground(21.5),
        line(seg(12, 11, 12, 21)), line(seg(4.5, 14, 4.5, 21)), line(seg(19.5, 14, 19.5, 21)),
        shell(star(12, 7, 5.2, 4, 12, -90, S.r * 0.4)), dot(12, 7, 1.6),
        shell(circle(4.5, 11.5, 2.4)), shell(circle(19.5, 11.5, 2.4)),
    ]


@icon("lavender-field", CAT, "Rows of rounded flowering bushes running in perspective toward a horizon line",
      tags=["lavender", "purple flowers", "provence", "perfume crop", "essential oil", "rows", "farmland"])
def _(S):
    return [
        line(seg(2, 9, 22, 9)),
        dot(11, 12, 1), dot(12, 12, 1), dot(13.3, 12, 1),
        dot(9, 15.5, 1.4), dot(12, 15.5, 1.4), dot(15, 15.5, 1.4),
        dot(5.5, 20, 1.9), dot(12, 20, 1.9), dot(18.5, 20, 1.9),
    ]

# ============================================================================ fields and farming systems

@icon("hop-yard", CAT, "Tall poles joined by an overhead wire, with a leafy bine climbing a string and hop cones hanging",
      tags=["hops", "hop garden", "trellis", "brewing", "beer crop", "bine", "farm"])
def _(S):
    return [
        line(seg(3.5, 3, 3.5, 21.5)), line(seg(20.5, 3, 20.5, 21.5)),
        line(seg(3.5, 4, 20.5, 4)),
        line("M12 4C14 8 10 11 12 14C14 17 10 19 12 21.5"),
        solid(ellipse(8, 9, 1.4, 2)), solid(ellipse(16, 13, 1.4, 2)), solid(ellipse(8, 17.5, 1.4, 2)),
    ]


@icon("cranberry-bog", CAT, "Flooded field with a wavy water line and rows of round berries floating together",
      tags=["cranberries", "wet harvest", "marsh", "flooded bog", "berry harvest", "fruit farm", "water"])
def _(S):
    return [
        line("M2 6.5C4.5 4.5 6.5 8.5 9 6.5S13.5 4.5 16 6.5S20 8.5 22 6.5"),
        dot(5, 12, 1.6), dot(10, 12, 1.6), dot(15, 12, 1.6), dot(20, 12, 1.6),
        dot(7.5, 17, 1.6), dot(12.5, 17, 1.6), dot(17.5, 17, 1.6),
    ]


@icon("cotton-field", CAT, "Two cotton plants, each topped by a fluffy white boll, standing on the ground",
      tags=["cotton", "boll", "textile crop", "fibre", "fiber", "farmland", "harvest"])
def _(S):
    def boll(x, y):
        return union(circle(x - 1.5, y + 1.2, 2.1), circle(x + 1.5, y + 1.2, 2.1), circle(x, y - 0.8, 2.1))
    return [
        ground(21.5),
        line(seg(6.5, 15, 6.5, 21)), line(seg(17.5, 15, 17.5, 21)),
        shell(boll(6.5, 9)), shell(boll(17.5, 9)),
        line(poly([(3.5, 13), (6.5, 15.5), (9.5, 13)], r=S.r * 0.5)), line(poly([(14.5, 13), (17.5, 15.5), (20.5, 13)], r=S.r * 0.5)),
    ]


@icon("christmas-tree-farm", CAT, "Two tiered fir trees of different heights standing on level ground",
      tags=["tree farm", "fir", "conifer", "evergreen", "plantation", "holiday trees", "nursery"])
def _(S):
    def tree(cx, top, hw, base=17.5):
        t = top + (base - top) * 0.42
        return poly([(cx, top), (cx + hw * 0.6, t), (cx + hw * 0.3, t), (cx + hw, base), (cx - hw, base),
                     (cx - hw * 0.3, t), (cx - hw * 0.6, t)], closed=True, r=S.r * 0.6)
    return [
        shell(tree(7.5, 3.5, 5)), shell(tree(18.5, 9.5, 3.2)),
        line(seg(7.5, 17.5, 7.5, 20)), line(seg(18.5, 17.5, 18.5, 20)),
        ground(21.5),
    ]


@icon("corn-maze", CAT, "Top down square of corn plants with winding maze paths and an entrance gap on one side",
      tags=["maze", "farm attraction", "autumn", "fall", "corn", "labyrinth", "agritourism"])
def _(S):
    return [
        line(poly([(9, 21), (3, 21), (3, 3), (21, 3), (21, 21), (15, 21)], r=S.r)),
        line(poly([(8, 16), (8, 8), (16, 8), (16, 16), (12, 16), (12, 12)], r=S.r)),
    ]


@icon("three-sisters-planting", CAT, "Corn stalk with a bean vine twining up it and a broad squash leaf spreading at its base",
      tags=["three sisters", "companion planting", "corn beans squash", "polyculture", "indigenous farming", "milpa", "garden"])
def _(S):
    return [
        ground(21.5),
        line(seg(7, 6, 7, 21)),
        line(poly([(4, 4.5), (7, 2.5), (10, 4.5)], r=S.r * 0.5)),
        line("M7 16C13 15 13 12 7 11C13 9 13 7 7 6.5"),
        line("M7 17C5 15.5 3.5 14.5 2.5 13"),
        shell(ellipse(16.5, 18.2, 4.8, 2.3)),
    ]


@icon("intercropping", CAT, "Field with alternating rows of tall grain stalks and short bushy plants side by side",
      tags=["mixed cropping", "alternate rows", "crop mix", "polyculture", "companion crops", "strip", "farm"])
def _(S):
    bush = union(circle(10.5, 16.5, 2.2), circle(13.5, 16.5, 2.2), circle(12, 14.5, 2.2))
    return [
        ground(21.5),
        line(seg(4.5, 10, 4.5, 21)), shell(leaf(4.5, 3, 4.5, 11, 1.4)),
        line(seg(19.5, 10, 19.5, 21)), shell(leaf(19.5, 3, 19.5, 11, 1.4)),
        shell(bush),
    ]


@icon("agroforestry", CAT, "Rows of trees with strips of low crop sprouts growing in the alley between them",
      tags=["alley cropping", "silvopasture", "trees and crops", "sustainable farming", "permaculture", "forest farming", "agriculture"])
def _(S):
    return [
        ground(21.5),
        line(seg(5, 11, 5, 21)), shell(circle(5, 7.5, 3.4)),
        line(seg(19, 11, 19, 21)), shell(circle(19, 7.5, 3.4)),
        line(poly([(10, 14), (12, 17), (14, 14)], r=S.r * 0.5)), line(seg(12, 17, 12, 21)),
    ]


@icon("shelterbelt", CAT, "Line of tall trees along the edge of a field with wind lines curving up and over the treetops",
      tags=["windbreak", "hedgerow", "tree line", "wind protection", "erosion control", "farm trees", "shelter"])
def _(S):
    return [
        ground(21.5),
        line(seg(15, 11, 15, 21)), shell(circle(15, 7.5, 3.2)),
        line(seg(20.5, 14, 20.5, 21)), shell(circle(20.5, 10.5, 2.4)),
        line("M2 17C5 17 6 11 9 8"), line("M2 12C4 12 5.5 8 8 5"),
    ]


@icon("riparian-buffer", CAT, "Strip of trees between striped crop rows and a wavy stream along the field edge",
      tags=["buffer strip", "stream bank", "waterway", "tree strip", "water quality", "stream", "conservation"])
def _(S):
    return [
        line(seg(3.5, 3, 3.5, 21)), line(seg(7, 3, 7, 21)),
        shell(circle(13, 6.5, 2)), shell(circle(13, 12, 2)), shell(circle(13, 17.5, 2)),
        line("M20.5 3C18 7 23 10 20.5 13C18.5 16 22 19 20.5 21"),
    ]


@icon("contour-farming", CAT, "Hillside with curved crop rows following the slope in parallel bands around the hill",
      tags=["contour plowing", "terrace", "slope farming", "erosion control", "hill", "soil conservation", "sustainable"])
def _(S):
    return [
        shell(L(S, "M2 21C5 14 10 7.5 14 7.5C18 7.5 20 15 22 21Z", "M3 20.5C6 14 10 8.5 14 8.5C17.5 8.5 19.5 15 21 20.5Z")),
        detail(L(S, "M6.5 21C8 16 11.5 12.5 14 12.5C16.5 12.5 17.5 17 18.5 21", "M7.5 20.5C9 16 11.5 13.5 14 13.5C16 13.5 17 17 17.8 20.5")),
    ]


@icon("slash-and-burn", CAT, "Cleared patch with a tree stump and flames beside a standing tree, marking a field cleared by fire",
      tags=["swidden", "land clearing", "deforestation", "shifting cultivation", "burning", "fire", "forest"])
def _(S):
    flame = "M7 18.5C3.5 18.5 3 14 6 11C6 13 7.5 13.5 7.5 13.5C7.5 10.5 8.5 8.5 9.5 7.5C12 11 11.5 18.5 7 18.5Z"
    return [
        ground(21.5),
        shell(flame),
        shell(rect(12.5, 17, 3, 4)),
        line(seg(20, 11, 20, 21)), shell(circle(20, 7.5, 3)),
    ]


@icon("seed-furrow", CAT, "Soil cross section with a V shaped furrow holding a seed and loose soil mounded on both sides",
      tags=["sowing", "planting row", "drill", "seed bed", "furrow", "soil", "seeding"])
def _(S):
    return [
        shell(poly([(2, 9), (8, 9), (12, 15), (16, 9), (22, 9), (22, 21), (2, 21)], closed=True, r=S.r)),
        dot(12, 11.8, 1.3),
    ]


@icon("seedling-emergence", CAT, "Tiny shoots breaking up through a cracked soil line, each with two small seed leaves",
      tags=["sprout", "germination", "emerging", "seedlings", "early growth", "shoots", "sowing"])
def _(S):
    return [
        line(seg(2, 18, 8.5, 18)), line(seg(15.5, 18, 22, 18)),
        line(seg(12, 19, 12, 11)),
        shell(leaf(12, 11, 6, 7, 1.8)), shell(leaf(12, 11, 18, 7, 1.8)),
        dot(5, 21.3, 0.9), dot(19, 21.3, 0.9),
    ]


@icon("transplanting-seedling", CAT, "Small seedling with a soil plug held over a hole dug in the ground",
      tags=["transplant", "planting out", "seedling", "plug", "garden", "nursery", "hardening off"])
def _(S):
    return [
        line(seg(12, 11, 12, 6)),
        shell(leaf(12, 7.5, 6.5, 3.5, 1.6)), shell(leaf(12, 7.5, 17.5, 3.5, 1.6)),
        shell(poly([(8.5, 11), (15.5, 11), (14, 16), (10, 16)], closed=True, r=S.r * 0.6)),
        line(poly([(2, 19), (8, 19), (9, 21.5), (15, 21.5), (16, 19), (22, 19)], r=S.r * 0.4)),
    ]

# ============================================================================ sowing, field conditions and soil

@icon("planting-depth", CAT, "Soil block with a seed buried below the surface and a small ruler beside it marking depth",
      tags=["sowing depth", "seed depth", "measure", "ruler", "soil", "seeding", "agronomy"])
def _(S):
    return [
        shell(rect(2.5, 8, 12, 13.5, L(S, 0.5, 2))),
        dot(8.5, 14.5, 1.5),
        line(seg(19, 5, 19, 21.5)),
        line(seg(19, 8, 22, 8)), line(seg(19, 12, 21.5, 12)), line(seg(19, 16, 22, 16)), line(seg(19, 20, 21.5, 20)),
    ]


@icon("stubble-field", CAT, "Field of short cut stalks standing in a row above the ground after harvest",
      tags=["post harvest", "cut stalks", "straw", "reaped", "fallow", "wheat stubble", "farmland"])
def _(S):
    def stalk(x, top):
        return line(poly([(x, 21.5), (x, top + 1.5), (x + 1.5, top)], r=0))
    return [
        ground(21.5),
        stalk(4.5, 13), stalk(8.5, 16), stalk(12.5, 12), stalk(16.5, 15), stalk(20.5, 13.5),
        line(poly([(5, 8), (9, 6.5)])), line(poly([(14, 8), (18.5, 6)])),
    ]


@icon("crop-lodging", CAT, "Grain stalks with several bent over and flattened sideways by wind lines blowing across them",
      tags=["lodged crop", "flattened", "storm damage", "wind damage", "bent stalks", "rain damage", "cereal"])
def _(S):
    return [
        ground(21.5),
        line(seg(4.5, 21, 4.5, 9)), shell(leaf(4.5, 3, 4.5, 10, 1.4)),
        line("M10 21C10 15 13 12 17 12"), shell(leaf(17, 12, 22, 12, 1.3)),
        line("M14.5 21C14.5 19 16 17.5 19 17.5"),
        line("M9 4C12 3 15 3 18 4"), line("M12 8C15 7 17 7 20 8"),
    ]


@icon("waterlogged-field", CAT, "Rows of young crop plants standing in pooled water with ripple lines across the surface",
      tags=["flooded field", "wet soil", "drainage problem", "standing water", "saturated", "flood damage", "crops"])
def _(S):
    def sprout(x):
        return [line(seg(x, 17, x, 10)), line(poly([(x - 2.4, 6.5), (x, 10), (x + 2.4, 6.5)], r=S.r * 0.5))]
    return [
        *sprout(5), *sprout(12), *sprout(19),
        line("M2 16.5C4.5 14.5 6.5 18.5 9 16.5S13.5 14.5 16 16.5S20 18.5 22 16.5"),
        line("M2 21C4.5 19 6.5 23 9 21S13.5 19 16 21S20 23 22 21"),
    ]


@icon("corn-detasseling", CAT, "Corn stalk with leaves and an ear, its feathery tassel lifted clear above it by an upward arrow",
      tags=["detassel", "corn tassel", "seed corn", "pollination control", "hybrid corn", "farm labor", "maize"])
def _(S):
    return [
        line(seg(12, 11, 12, 21.5)),
        shell(leaf(12, 20, 5, 16, 1.5)), shell(leaf(12, 17, 19, 12.5, 1.5)),
        line(seg(12, 8, 12, 2.5)), line(seg(10.5, 8, 7.5, 3.5)), line(seg(13.5, 8, 16.5, 3.5)),
        line(seg(21, 9, 21, 3)), line(poly([(19, 5), (21, 3), (23, 5)], r=S.r * 0.4)),
    ]


@icon("air-layering", CAT, "Branch with a ball of moss wrapped in plastic and tied at both ends, small roots showing inside",
      tags=["marcotting", "propagation", "grafting", "plant cutting", "moss wrap", "roots", "gardening"])
def _(S):
    return [
        line(seg(2, 12, 6, 12)), line(seg(18, 12, 22, 12)),
        shell(ellipse(12, 12, 6, 5.2)),
        line(seg(6, 8.5, 6, 15.5)), line(seg(18, 8.5, 18, 15.5)),
        detail("M12 9.5V14.5"), detail("M12 12L9.5 14.5"), detail("M12 12L14.5 14.5"),
        shell(leaf(3, 12, 3.5, 5.5, 1.5)), shell(leaf(21, 12, 20.5, 18.5, 1.5)),
    ]


@icon("fruit-bagging", CAT, "Branch with fruits each enclosed in a small paper bag tied closed at the stem",
      tags=["fruit protection", "orchard", "paper bag", "pest control", "apple", "mango", "grape"])
def _(S):
    def bag(x):
        return [line(seg(x, 4, x, 8.5)),
                shell(poly([(x - 3.5, 11), (x - 1.5, 8.5), (x + 1.5, 8.5), (x + 3.5, 11), (x + 3.5, 20), (x - 3.5, 20)],
                           closed=True, r=S.r * 0.6)),
                dot(x, 15, 1.5)]
    return [line(seg(2, 4, 22, 4)), *bag(6.5), *bag(17.5)]


@icon("low-tunnel", CAT, "Low arched row cover of fabric over wire hoops sheltering a young plant, resting on the ground",
      tags=["row cover", "hoop tunnel", "frost protection", "season extension", "cloche", "polytunnel", "garden"])
def _(S):
    return [
        shell("M3 20C3 5 21 5 21 20Z"),
        detail(seg(12, 18, 12, 15)),
        detail(poly([(9.5, 12.5), (12, 15), (14.5, 12.5)], r=S.r * 0.5)),
        ground(21.5, 1.5, 22.5),
    ]


@icon("shade-net-house", CAT, "Rectangular frame structure with a mesh net roof and sides and young plants standing inside",
      tags=["shade house", "net house", "screenhouse", "nursery", "horticulture", "greenhouse", "mesh"])
def _(S):
    return [
        shell(rect(3, 5, 18, 16.5, L(S, 0, 2))),
        detail(seg(9, 5, 9, 10)), detail(seg(15, 5, 15, 10)), detail(seg(3, 10, 21, 10)),
        detail(seg(8, 20, 8, 16)), detail(poly([(5.5, 13.5), (8, 16), (10.5, 13.5)], r=S.r * 0.5)),
        detail(seg(16, 20, 16, 16)), detail(poly([(13.5, 13.5), (16, 16), (18.5, 13.5)], r=S.r * 0.5)),
    ]


@icon("germination-test", CAT, "Round dish holding seeds, some sending out small roots and shoots",
      tags=["seed test", "petri dish", "seed viability", "sprouting", "lab", "seed quality", "germination rate"])
def _(S):
    return [
        shell(circle(12, 12, L(S, 9.5, 9))),
        dot(8, 9, 1.4), dot(15.5, 8.5, 1.4), dot(11, 15.5, 1.4),
        line("M8 9C6.5 10.5 6.2 12 7 13.5"), line("M15.5 8.5C17 10 17.2 11.5 16.5 13"),
    ]


@icon("soil-probe", CAT, "T handled steel tube pushed into the ground, with a side slot showing a core of soil inside",
      tags=["soil sampler", "core sampler", "auger", "soil test", "soil sampling", "agronomy", "tube"])
def _(S):
    return [
        line(seg(6, 3.5, 18, 3.5)),
        shell(poly([(9.5, 5.5), (14.5, 5.5), (14.5, 18), (12, 21.5), (9.5, 18)], closed=True, r=S.r * 0.6)),
        detail(seg(12, 10.5, 12, 16)),
        line(seg(2, 14, 7, 14)), line(seg(17, 14, 22, 14)),
    ]


@icon("penetrometer", CAT, "T handled rod with a round dial gauge near the top and a pointed cone tip pushed into soil",
      tags=["soil resistance", "compaction tester", "dial gauge", "soil test", "cone penetrometer", "measure", "agronomy"])
def _(S):
    return [
        line(seg(8, 2.5, 16, 2.5)), line(seg(12, 2.5, 12, 5)),
        shell(circle(12, 9, 3.6)),
        detail(seg(12, 9, 13.8, 7.2)),
        line(seg(12, 12.6, 12, 17)),
        shell(poly([(9.5, 17), (14.5, 17), (12, 21.5)], closed=True, r=S.r * 0.4)),
        line(seg(2, 17.5, 7, 17.5)), line(seg(17, 17.5, 22, 17.5)),
    ]


@icon("soil-compaction", CAT, "Tractor tire pressing on the soil with tightly packed dense layer lines beneath it",
      tags=["compacted soil", "heavy machinery", "tire", "soil structure", "hard pan", "tractor", "soil health"])
def _(S):
    return [
        shell(circle(12, 7.5, 5)),
        dot(12, 7.5, 1.6),
        line(seg(2, 14, 22, 14)),
        line(seg(4, 17, 20, 17)), line(seg(6.5, 19.7, 17.5, 19.7)),
    ]


@icon("fertilizer-granules", CAT, "Small heap of round fertilizer pellets with a few loose pellets rolled away beside it",
      tags=["fertiliser", "pellets", "prills", "plant food", "nutrients", "granular", "farm input"])
def _(S):
    k = L(S, 0, 0.4)
    heap = union(circle(5.5, 18, 2.7 + k), circle(10, 18, 2.7 + k), circle(14.5, 18, 2.7 + k),
                 circle(7.7, 14, 2.7 + k), circle(12.2, 14, 2.7 + k), circle(10, 10, 2.7 + k), circle(10, 15.2, 2.2))
    return [shell(heap), dot(20.6, 20.2, 1.2), dot(20.6, 16.4, 1.2)]

# ============================================================================ inputs, mulch and soil life

@icon("liquid-fertilizer", CAT, "Jug with a handle and cap, a leaf on its label and a single drop falling beside the spout",
      tags=["liquid feed", "plant food", "nutrient solution", "foliar spray", "jug", "garden", "farm input"])
def _(S):
    return [
        shell(rect(3, 9.5, 11, 12, L(S, 1, 3))),
        shell(rect(6, 4.5, 5, 4, 0.5)),
        line("M14 12.5C17.5 12.5 17.5 18.5 14 18.5"),
        detail(leaf(6.5, 18, 10.5, 13, 1.3)),
        solid("M19.5 3.5C19.5 3.5 17.5 6.3 17.5 8A2 2 0 0 0 21.5 8C21.5 6.3 19.5 3.5 19.5 3.5Z"),
    ]


@icon("plastic-mulch", CAT, "Raised bed covered with a smooth plastic sheet, plants poking up through holes in the top",
      tags=["mulch film", "black plastic", "raised bed", "weed barrier", "drip tape", "vegetable farm", "ground cover"])
def _(S):
    def sprout(x):
        return [line(seg(x, 12.5, x, 8.5)), line(poly([(x - 2.4, 6), (x, 8.5), (x + 2.4, 6)], r=S.r * 0.5))]
    return [
        shell(poly([(2, 21), (5, 12.5), (19, 12.5), (22, 21)], closed=True, r=S.r)),
        dot(8, 15.8, 1.3), dot(16, 15.8, 1.3),
        *sprout(8), *sprout(16),
    ]


@icon("straw-mulch", CAT, "Young plant whose base is surrounded by a thick layer of short straw strands on top of the soil",
      tags=["hay mulch", "organic mulch", "weed control", "moisture retention", "garden bed", "ground cover", "straw"])
def _(S):
    return [
        line(seg(12, 15, 12, 8)),
        shell(leaf(12, 10, 5.5, 5, 1.8)), shell(leaf(12, 10, 18.5, 5, 1.8)),
        shell(L(S, "M2 21.5C4 16.5 9 15.5 12 15.5C15 15.5 20 16.5 22 21.5Z", "M2.5 21C4.5 17 9 16 12 16C15 16 19.5 17 21.5 21Z")),
        detail(seg(5.5, 19.5, 9, 18)), detail(seg(11, 19.5, 14.5, 18)), detail(seg(15.5, 19.5, 18.5, 18.5)),
    ]


@icon("cover-crop", CAT, "Low leafy carpet of plants growing over the soil with short roots reaching down below",
      tags=["green manure", "living mulch", "soil cover", "erosion control", "clover", "winter rye", "regenerative"])
def _(S):
    carpet = union(circle(5.5, 9.5, 2.8), circle(10.2, 8.5, 2.8), circle(14.8, 8.5, 2.8), circle(18.5, 9.5, 2.8),
                   rect(3.4, 9, 17.2, 3.5, 0))
    return [
        shell(carpet),
        line("M7 14.5C7 17 5.5 18.5 4.5 21"), line(seg(12, 14.5, 12, 21)), line("M17 14.5C17 17 18.5 18.5 19.5 21"),
    ]


@icon("root-nodules", CAT, "Legume root system below a soil line with small round nodules clustered along the roots",
      tags=["nitrogen fixing", "legume roots", "rhizobia", "bean roots", "soil bacteria", "nitrogen fixation", "biology"])
def _(S):
    return [
        line(seg(2, 8.5, 9, 8.5)), line(seg(15, 8.5, 22, 8.5)),
        line(seg(12, 3, 12, 19)),
        line("M12 11.5C9 12.5 7 16 6 20.5"), line("M12 11.5C15 12.5 17 16 18 20.5"),
        dot(6.3, 13.2, 1.4), dot(17.7, 13.2, 1.4), dot(9.8, 18, 1.4), dot(14.2, 18, 1.4),
    ]


@icon("nitrogen-cycle", CAT, "Three curved arrows chasing each other in a ring around the letter N",
      tags=["n cycle", "nitrogen", "fixation", "soil nutrients", "ecology", "recycling", "fertilizer"])
def _(S):
    out = []
    for a in (-80, 40, 160):
        out += arrow_arc(12, 12, 9, a, a + 80, 2.6, S)
    out.append(line(poly([(9.5, 15.5), (9.5, 8.5), (14.5, 15.5), (14.5, 8.5)], r=S.r * 0.4)))
    return out


@icon("peat-pot", CAT, "Tapered pot with a rough fibrous wall holding a small seedling with two leaves",
      tags=["biodegradable pot", "seed starting", "coir pot", "nursery", "seedling", "garden", "transplant"])
def _(S):
    return [
        line(seg(12, 12, 12, 7.5)),
        shell(leaf(12, 8.5, 5.5, 4.5, 1.7)), shell(leaf(12, 8.5, 18.5, 4.5, 1.7)),
        shell(poly([(4.5, 12), (19.5, 12), (17, 21.5), (7, 21.5)], closed=True, r=S.r * 0.6)),
        detail(seg(9, 15, 10, 18.5)), detail(seg(14, 15, 15, 18.5)),
    ]


@icon("seed-ball", CAT, "Round clay ball dotted with seeds and two small sprouts emerging from its top",
      tags=["seed bomb", "guerrilla gardening", "clay ball", "rewilding", "native seeds", "nature", "sprout"])
def _(S):
    return [
        line(seg(9.5, 9.5, 9.5, 5.5)), shell(leaf(9.5, 6.5, 5, 3.5, 1.3)),
        line(seg(15, 9.5, 15, 4.5)), shell(leaf(15, 6, 19.5, 3, 1.3)),
        shell(circle(12, 16, L(S, 6.2, 5.8))),
        dot(9.5, 15, 1.2), dot(14.5, 14.5, 1.2), dot(12, 19, 1.2),
    ]


@icon("biochar", CAT, "Small pile of black porous charcoal chunks mixed into soil with a sprout growing beside it",
      tags=["charcoal", "soil amendment", "carbon", "pyrolysis", "terra preta", "soil carbon", "sequestration"])
def _(S):
    a = poly([(2.5, 21), (3.5, 15.5), (8.5, 14), (12, 17), (11.5, 21)], closed=True, r=S.r)
    b = poly([(6, 14.5), (7.5, 9.5), (12.5, 9), (14, 13.5), (11.5, 16)], closed=True, r=S.r)
    return [
        shell(union(a, b)),
        dot(7, 18, 1), dot(10, 12.5, 1),
        line(seg(19, 21.5, 19, 14)), line(poly([(16.5, 11.5), (19, 14), (21.5, 11.5)], r=S.r * 0.5)),
    ]


@icon("hugelkultur-bed", CAT, "Cross section of a long mound with buried logs at its core and young plants growing on top",
      tags=["raised bed", "mound garden", "buried wood", "permaculture", "wood core bed", "sustainable garden", "composting"])
def _(S):
    def sprout(x):
        return [line(seg(x, 9, x, 5.5)), line(poly([(x - 2.3, 3), (x, 5.5), (x + 2.3, 3)], r=S.r * 0.5))]
    return [
        shell(L(S, "M2 21C3.5 13 8 9 12 9C16 9 20.5 13 22 21Z", "M2.5 21C4 13.5 8 9.5 12 9.5C16 9.5 20 13.5 21.5 21Z")),
        detail(circle(8.5, 17, 1.8)), detail(circle(15.5, 17, 1.8)), detail(circle(12, 13.6, 1.5)),
        *sprout(8), *sprout(16),
    ]


@icon("tile-drainage", CAT, "Field cross section with young crops on top and a perforated pipe buried below, drops seeping in",
      tags=["field drain", "subsurface drainage", "drain pipe", "perforated pipe", "water management", "soil water", "farm drainage"])
def _(S):
    def sprout(x):
        return [line(seg(x, 9, x, 5.5)), line(poly([(x - 2.3, 3), (x, 5.5), (x + 2.3, 3)], r=S.r * 0.5))]
    return [
        line(seg(2, 9.5, 22, 9.5)),
        *sprout(6), *sprout(18),
        shell(rect(2.5, 16, 19, 5.5, L(S, 1, 2.75))),
        dot(7, 18.7, 0.9), dot(12, 18.7, 0.9), dot(17, 18.7, 0.9),
        solid("M8 11.5C8 11.5 6.8 13.3 6.8 14.2A1.2 1.2 0 0 0 9.2 14.2C9.2 13.3 8 11.5 8 11.5Z"),
        solid("M16 11.5C16 11.5 14.8 13.3 14.8 14.2A1.2 1.2 0 0 0 17.2 14.2C17.2 13.3 16 11.5 16 11.5Z"),
    ]


@icon("anhydrous-ammonia-tank", CAT, "Horizontal capsule shaped pressure tank on a wheeled trailer frame with a valve cluster on top",
      tags=["nh3", "nurse tank", "fertilizer tank", "pressure vessel", "farm trailer", "ammonia", "nitrogen fertilizer"])
def _(S):
    return [
        shell(rect(3, 6.5, 18, 8, 4)),
        line(seg(12, 3, 12, 6.5)), line(seg(9, 3, 15, 3)),
        line(seg(2, 17.5, 22, 17.5)),
        dot(7, 20, 2), dot(17, 20, 2),
    ]

# ============================================================================ research, pests and irrigation

@icon("fertilizer-runoff", CAT, "Sloped field with an arrow washing down the slope into a stream dotted with floating algae blobs",
      tags=["nutrient pollution", "eutrophication", "agricultural runoff", "algae bloom", "water pollution", "erosion", "stream"])
def _(S):
    return [
        line(poly([(2, 4.5), (8, 4.5), (15, 10.5), (22, 10.5)], r=S.r)),
        line(seg(7, 9, 12, 14)), line(poly([(8.5, 14), (12, 14), (12, 10.5)], r=S.r * 0.4)),
        dot(14, 16.4, 1.2), dot(18, 16.4, 1.2), dot(10, 16.4, 1.2),
        line("M2 20C4.5 18.5 6.5 21.5 9 20S13.5 18.5 16 20S20 21.5 22 20"),
    ]


@icon("plant-breeding", CAT, "Two parent sprouts with a cross between them and an arrow down to a sturdier offspring plant",
      tags=["crossbreeding", "hybrid", "genetics", "cultivar", "seed development", "selection", "agronomy"])
def _(S):
    return [
        line(seg(4.5, 9, 4.5, 5)), line(poly([(2.3, 3.5), (4.5, 5.5), (6.7, 3.5)], r=S.r * 0.4)),
        line(seg(19.5, 9, 19.5, 5)), line(poly([(17.3, 3.5), (19.5, 5.5), (21.7, 3.5)], r=S.r * 0.4)),
        line(seg(10.2, 4.2, 13.8, 7.8)), line(seg(13.8, 4.2, 10.2, 7.8)),
        line(poly([(9.8, 10.5), (12, 12.7), (14.2, 10.5)], r=S.r * 0.4)),
        line(seg(12, 22, 12, 17)),
        shell(leaf(12, 19.5, 6, 15.5, 1.5)), shell(leaf(12, 19.5, 18, 15.5, 1.5)),
    ]


@icon("field-trial-plots", CAT, "Top down grid of four small rectangular plots, each with a different row pattern",
      tags=["research plots", "experiment", "test plots", "agronomy trial", "crop research", "variety trial", "randomized"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 8, 8, L(S, 0, 2))), shell(rect(13.5, 2.5, 8, 8, L(S, 0, 2))),
        shell(rect(2.5, 13.5, 8, 8, L(S, 0, 2))), shell(rect(13.5, 13.5, 8, 8, L(S, 0, 2))),
        detail(seg(6.5, 4.5, 6.5, 8.5)), detail(seg(15.5, 6.5, 19.5, 6.5)),
        detail(seg(4.7, 19.3, 8.3, 15.7)), dot(17.5, 17.5, 1.2),
    ]


@icon("growth-chamber", CAT, "Tall cabinet with shelves of small plants, each shelf lit from above, behind a glass front",
      tags=["plant growth cabinet", "grow room", "phytotron", "climate chamber", "research lab", "indoor farming", "grow light"])
def _(S):
    def sprout(x, y):
        return [detail(seg(x, y, x, y - 2)), detail(poly([(x - 1.8, y - 3.8), (x, y - 2), (x + 1.8, y - 3.8)], r=0))]
    return [
        shell(rect(3.5, 2.5, 17, 19, L(S, 1, 3))),
        detail(seg(3.5, 9.5, 20.5, 9.5)), detail(seg(3.5, 15.8, 20.5, 15.8)),
        *sprout(8.5, 8), *sprout(15.5, 8), *sprout(8.5, 14.3), *sprout(15.5, 14.3),
        dot(12, 19, 1.2),
    ]


@icon("agronomist", CAT, "Person in a cap standing beside a tall crop plant and holding a clipboard",
      tags=["crop scientist", "farm advisor", "field expert", "crop consultant", "agriculture specialist", "farmer", "researcher"])
def _(S):
    return [
        shell(circle(8, 6.5, 2.9)),
        line(seg(8.5, 3.8, 13, 3.8)),
        shell(L(S, "M3 21.5V15C3 12.5 5 11 8 11S13 12.5 13 15V21.5Z", "M3 21.5V15.5C3 12.5 5 11 8 11S13 12.5 13 15.5V21.5Z")),
        detail(rect(7.2, 14.5, 4, 5.5, 0)),
        line(seg(19, 8, 19, 21.5)), shell(leaf(19, 2.5, 19, 9, 1.3)),
        shell(leaf(19, 15, 22, 11.5, 1.1)),
    ]


@icon("pheromone-trap", CAT, "Triangular tent shaped delta trap with a lure inside, hanging by a wire from a branch",
      tags=["insect trap", "delta trap", "moth trap", "pest monitoring", "lure", "orchard", "integrated pest management"])
def _(S):
    return [
        line(seg(2, 3, 22, 3)),
        line(seg(12, 3, 12, 7.5)),
        shell(poly([(12, 7.5), (21, 20), (3, 20)], closed=True, r=S.r)),
        dot(12, 16, 1.5),
    ]


@icon("locust-swarm", CAT, "Two winged locusts flying low in a swarm above a row of crop stalks",
      tags=["grasshopper", "plague", "insect swarm", "crop pest", "infestation", "desert locust", "crop damage"])
def _(S):
    def loc(x, y):
        return [solid(ellipse(x, y, 3.2, 1.4)), solid(circle(x + 3.6, y - 0.3, 1.3)),
                shell(leaf(x - 1.5, y - 0.8, x + 2, y - 5, 1.3)),
                line(seg(x - 0.5, y + 1, x - 2, y + 3))]
    return [
        *loc(8, 8), *loc(15.5, 13.5),
        ground(21.5),
        line(seg(5, 17, 5, 21)), line(seg(12, 18.5, 12, 21)), line(seg(19, 17, 19, 21)),
    ]


@icon("bird-scare-cannon", CAT, "Flared gas cannon barrel on a small stand with a gas cylinder beside it and a burst at the muzzle",
      tags=["propane cannon", "bird deterrent", "crop protection", "noise scarer", "vineyard", "scarecrow", "pest control"])
def _(S):
    return [
        shell(poly([(4.5, 14.5), (7, 17.5), (15, 11), (12, 6.5)], closed=True, r=S.r * 0.7)),
        line(seg(8, 17, 6, 21.5)), line(seg(10, 15, 13, 21.5)),
        shell(rect(15.5, 14.5, 4.5, 7, L(S, 1, 2.2))),
        line(seg(17, 3, 19, 6)), line(seg(20.5, 8, 22, 9)),
    ]


@icon("scare-eye-balloon", CAT, "Round balloon printed with large concentric eye rings, hanging from a pole above the crops",
      tags=["bird scarer", "scare eyes", "predator eye", "pest deterrent", "orchard", "crop protection", "vineyard"])
def _(S):
    return [
        line(seg(6, 2.5, 18, 2.5)), line(seg(12, 2.5, 12, 5)),
        shell(union(circle(12, 12, 7), poly([(10.3, 19.2), (13.7, 19.2), (12, 17.5)], closed=True, r=S.r * 0.4))),
        detail(circle(12, 12, 3.8)), dot(12, 12, 1.4),
    ]


@icon("flame-weeder", CAT, "Long wand with a burner nozzle aiming a flame at a weed, a hose leading back to a gas cylinder",
      tags=["thermal weeding", "weed burner", "propane torch", "organic weed control", "garden tool", "weeds", "fire"])
def _(S):
    return [
        shell(rect(2.5, 14, 5, 7.5, L(S, 1, 2.5))),
        line("M5 14C5 9 6 6.5 9 5"),
        line(seg(9, 5, 14.5, 11)),
        solid("M16.5 13C18.5 13.5 19 16 17.5 17.5C17.5 16.5 16.5 16.2 16.5 16.2C16.5 17 16 17.6 15.5 17.8C14.3 16.5 15 14 16.5 13Z"),
        line(seg(20, 21.5, 20, 19)), line(poly([(18.3, 17.5), (20, 19), (21.7, 17.5)], r=S.r * 0.4)),
        ground(21.5, 14, 22),
    ]


@icon("flood-irrigation", CAT, "Top down field of square basins separated by low earth ridges, with water fed by a side channel",
      tags=["border irrigation", "basin irrigation", "surface irrigation", "paddy", "water supply", "rice field", "canal"])
def _(S):
    return [
        line("M2.5 3C4.5 6 .5 9 2.5 12C4.5 15 .5 18 2.5 21"),
        shell(rect(6.5, 3, 15.5, 18, L(S, 0, 2))),
        detail(seg(14.25, 3, 14.25, 21)), detail(seg(6.5, 12, 22, 12)),
        dot(10.4, 7.5, 1), dot(18, 7.5, 1), dot(10.4, 16.5, 1), dot(18, 16.5, 1),
    ]


@icon("wheel-line-irrigation", CAT, "Long pipe running through the hubs of large spoked wheels with a sprinkler spraying between them",
      tags=["sprinkler line", "side roll", "hand move", "irrigation system", "spray", "farm water", "sprinklers"])
def _(S):
    return [
        shell(circle(6.5, 16, 4)), shell(circle(17.5, 16, 4)),
        detail(seg(6.5, 13, 6.5, 19)), detail(seg(3.5, 16, 9.5, 16)),
        detail(seg(17.5, 13, 17.5, 19)), detail(seg(14.5, 16, 20.5, 16)),
        line(seg(2, 16, 22, 16)),
        line(seg(12, 16, 12, 10)),
        line(seg(12, 10, 8, 6)), line(seg(12, 10, 16, 6)), line(seg(12, 10, 12, 4.5)),
    ]


@icon("traveling-irrigator", CAT, "Hose reel on a wheeled cart with a hose running out to a tall sprinkler gun on a small sled",
      tags=["hose reel", "big gun", "rain gun", "reel irrigator", "sprinkler gun", "field irrigation", "farm water"])
def _(S):
    return [
        shell(circle(7, 10, 5)),
        detail(circle(7, 10, 1.5)),
        line(seg(2, 18, 13, 18)), dot(4.5, 20.5, 1.5), dot(10.5, 20.5, 1.5),
        line("M12 13C14 18 16 20 19 20.5"),
        line(seg(16, 21.8, 22, 21.8)),
        line(seg(19, 20, 19, 13)), line(seg(19, 13, 22, 9.5)),
        line(seg(15.5, 7, 17.5, 9)), line(seg(21.5, 5, 21.5, 7)),
    ]


@icon("siphon-tube-irrigation", CAT, "Curved tube arching over a ditch bank, carrying water from the ditch down into a crop furrow",
      tags=["siphon", "furrow irrigation", "ditch", "gated pipe", "canal", "water diversion", "surface irrigation"])
def _(S):
    return [
        line(poly([(2, 11), (5, 11), (7, 18), (11, 18), (13, 11), (22, 11)], r=S.r)),
        line("M9 17C9 3 18 3 18 8.5"),
        solid("M18 12C18 12 16.8 13.8 16.8 14.7A1.2 1.2 0 0 0 19.2 14.7C19.2 13.8 18 12 18 12Z"),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("tube-well", CAT, "Vertical pipe rising from the ground beside a small pump house, water arcing from its outlet",
      tags=["borehole", "groundwater", "water pump", "well", "irrigation source", "bore well", "pumping"])
def _(S):
    return [
        line(seg(2, 17.5, 22, 17.5)),
        shell(poly([(3, 17.5), (3, 12), (6.5, 8.5), (10, 12), (10, 17.5)], closed=True, r=S.r * 0.6)),
        line("M14.5 17.5V6.5H18.5"),
        solid("M20.5 9C20.5 9 19.3 10.8 19.3 11.7A1.2 1.2 0 0 0 21.7 11.7C21.7 10.8 20.5 9 20.5 9Z"),
        solid("M20.5 14.2C20.5 14.2 19.6 15.5 19.6 16.1A0.9 0.9 0 0 0 21.4 16.1C21.4 15.5 20.5 14.2 20.5 14.2Z"),
        line(seg(2, 21.5, 22, 21.5)) if False else dot(6.5, 21, 0.01) if False else line(seg(4, 21, 20, 21)),
    ]


@icon("farm-pond", CAT, "Dug pond with sloped banks, a water line inside and an inlet pipe pouring in from one side",
      tags=["reservoir", "water storage", "irrigation pond", "dugout", "dam", "water harvesting", "catchment"])
def _(S):
    return [
        line(poly([(2, 10), (5, 10), (8.5, 19), (15.5, 19), (19, 10), (22, 10)], r=S.r)),
        line("M7 14.5C9 13 10.5 16 12 14.5S15 13 17 14.5"),
        line(seg(2, 5.5, 8, 5.5)),
        solid("M9.5 6.2C9.5 6.2 8.3 8 8.3 8.9A1.2 1.2 0 0 0 10.7 8.9C10.7 8 9.5 6.2 9.5 6.2Z"),
    ]


@icon("irrigation-pump", CAT, "Engine driven pump on a skid with a round pump housing, a discharge pipe and a suction hose",
      tags=["water pump", "centrifugal pump", "diesel pump", "farm pump", "suction hose", "pumping water", "irrigation equipment"])
def _(S):
    return [
        shell(rect(2.5, 9, 8, 8, L(S, 1, 2))),
        shell(circle(15, 13, 4)),
        line("M15 8V4.5H22"),
        line(poly([(2, 20), (14, 20)])), line("M19 14C21 14 21.5 17 21 21.5"),
    ]


@icon("fertigation-tank", CAT, "Tank feeding nutrients into a drip line that runs along a row of young plants",
      tags=["drip fertilizer", "nutrient tank", "fertilizer injector", "drip line", "irrigation fertilizer", "greenhouse feed", "dosing"])
def _(S):
    def sprout(x):
        return [line(seg(x, 17, x, 13)), line(poly([(x - 2.2, 10.5), (x, 13), (x + 2.2, 10.5)], r=S.r * 0.5))]
    return [
        shell(rect(2.5, 3, 8, 10, L(S, 1, 3))),
        detail(seg(2.5, 7.5, 10.5, 7.5)),
        line("M6.5 13V18H21.5"),
        *sprout(14.5), *sprout(19.5),
        dot(14.5, 21, 1), dot(19.5, 21, 1),
    ]


@icon("olla-irrigation", CAT, "Unglazed clay pot buried to its neck in soil with a lid, moisture seeping out to the soil around it",
      tags=["clay pot", "buried pot", "ancient irrigation", "terracotta", "water saving", "garden watering", "porous pot"])
def _(S):
    return [
        line(seg(2, 8, 8.5, 8)), line(seg(15.5, 8, 22, 8)),
        shell(union(circle(12, 15, 6), rect(9.5, 7, 5, 4))),
        shell(rect(9, 3, 6, 2.5, 1)),
        dot(3.5, 14, 1), dot(20.5, 14, 1), dot(4.5, 19, 1), dot(19.5, 19, 1),
    ]


@icon("silage-clamp", CAT, "Long low mound of silage covered by a plastic sheet held down by rings of old tires",
      tags=["silage pit", "bunker silo", "forage storage", "fodder", "hay", "feed storage", "dairy farm"])
def _(S):
    return [
        shell(L(S, "M2 20.5C4 13 8 10 12 10S20 13 22 20.5Z", "M2.5 20C4.5 13.5 8 10.5 12 10.5S19.5 13.5 21.5 20Z")),
        detail(circle(12, 13.5, 1.4)), detail(circle(7.8, 17, 1.4)), detail(circle(16.2, 17, 1.4)),
    ]


@icon("crop-health-map", CAT, "Field outline divided into irregular zones with different amounts of marking and a small scale bar below",
      tags=["ndvi", "precision agriculture", "zone map", "satellite imagery", "yield map", "remote sensing", "field scouting"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 14, L(S, 0, 2))),
        detail("M9.5 2.5C9.5 7 12.5 9 12.5 16.5"), detail("M12.5 9.5H21.5"),
        dot(5.8, 6, 1), dot(5.8, 9.8, 1), dot(5.8, 13.5, 1), dot(17, 6, 1),
        line(seg(3.5, 20.5, 11, 20.5)), line(seg(3.5, 19, 3.5, 22)), line(seg(11, 19, 11, 22)),
    ]
