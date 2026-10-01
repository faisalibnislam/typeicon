"""TypeIcon Core: household (batch household_003): laundry care, shoe care, oral care and personal grooming.

Original drawings of everyday bathroom, laundry and grooming objects. Bodies are shells; labels, folds, doors and
texture marks are details so the Filled style knocks them out. Laundry care symbols are drawn as plain geometry
(tub, triangle, square, circle, iron) in the same 2 px language as the rest of the set.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import LINE, I, fmt, path_to_d, polar

CAT = "household"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def mark(d) -> Part:
    return Part("dot", d)


def tip(S, cx, cy, ang, size=2.2):
    """Open arrowhead (chevron) at (cx, cy) pointing along `ang` degrees (0 = right, 90 = down)."""
    a = math.radians(ang)
    pts = []
    for s in (150, -150):
        b = a + math.radians(s)
        pts.append((cx + size * math.cos(b), cy + size * math.sin(b)))
    return poly([pts[0], (cx, cy), pts[1]], r=S.r * 0.5)


def bar(p0, p1, w):
    """Closed rectangle of width w along the segment p0-p1."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    n = math.hypot(dx, dy)
    nx, ny = -dy / n * w / 2, dx / n * w / 2
    return [(p0[0] + nx, p0[1] + ny), (p1[0] + nx, p1[1] + ny), (p1[0] - nx, p1[1] - ny), (p0[0] - nx, p0[1] - ny)]


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


# ============================================================================ laundry machines and racks

@icon("clothes-wringer", CAT, "Old mangle with two stacked rollers, a support leg and a crank wheel",
      tags=["mangle", "wringer", "laundry", "roller", "squeeze", "vintage", "washday"])
def _(S):
    return [
        shell(rect(3, 3.5, 14, 10, rr(S, 3))),
        detail(seg(3, 8.5, 17, 8.5)),
        line(poly([(6, 13.5), (6, 21)])), line(poly([(14, 13.5), (14, 21)])),
        line(seg(4, 21, 16, 21)),
        shell(circle(19.5, 10, 2.5)),
        line(poly([(19.5, 12.5), (19.5, 17)])),
    ]


@icon("top-load-washer", CAT, "Top loading washing machine seen from the front with a control panel and the open tub",
      tags=["washing machine", "washer", "laundry", "top loader", "appliance", "tub", "wash"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 3))),
        detail(seg(4, 8, 20, 8)),
        dot(7.5, 5.2, 1), dot(11, 5.2, 1),
        detail(seg(15, 5.2, 17.5, 5.2)),
        detail(ellipse(12, 14.5, 5, 3)),
    ]


@icon("stacked-washer-dryer", CAT, "Tall unit with a dryer stacked on a washing machine, each with a round door",
      tags=["washer dryer", "laundry", "stacked laundry", "appliance", "laundry room", "tower", "wash"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 3))),
        detail(seg(5, 11.5, 19, 11.5)),
        detail(circle(12, 7, 2.2)),
        detail(circle(12, 16.7, 2.8)),
        dot(7.8, 4.3, 0.8), dot(16.2, 4.3, 0.8),
    ]


@icon("laundromat", CAT, "Row of three front loading machines side by side with a coin slot above each",
      tags=["laundrette", "launderette", "coin laundry", "self service laundry", "washing machines", "wash", "shop"])
def _(S):
    return [
        shell(rect(2, 4, 20, 17, rr(S, 3))),
        detail(seg(2, 8.5, 22, 8.5)),
        detail(circle(6, 15, 1.5)), detail(circle(12, 15, 1.5)), detail(circle(18, 15, 1.5)),
        dot(6, 6.2, 0.7), dot(12, 6.2, 0.7), dot(18, 6.2, 0.7),
    ]


@icon("clip-hanger", CAT, "Trouser hanger with a straight bar and two spring clips hanging from it",
      tags=["skirt hanger", "trouser hanger", "clothes hanger", "clip", "wardrobe", "closet", "laundry"])
def _(S):
    return [
        line(poly([(12, 8), (12, 6)])),
        line("M12 6A2.2 2.2 0 1 0 9.8 3.8"),
        line(poly([(3, 8), (21, 8)], r=0)),
        shell(rect(4.5, 8, 4, 12, rr(S, 1.5))),
        shell(rect(15.5, 8, 4, 12, rr(S, 1.5))),
        detail(seg(4.5, 16.5, 8.5, 16.5)), detail(seg(15.5, 16.5, 19.5, 16.5)),
    ]


@icon("pants-hanger", CAT, "Clothes hanger with a pair of pants folded over its bar",
      tags=["trousers", "hanger", "folded pants", "wardrobe", "closet", "clothes", "laundry"])
def _(S):
    return [
        line("M12 6V4.8"),
        line("M12 4.8A1.9 1.9 0 1 0 10.1 2.9"),
        line(poly([(3, 9.5), (12, 6), (21, 9.5)], r=S.r)),
        shell(poly([(6.5, 9.5), (17.5, 9.5), (17.5, 21.5), (13.2, 21.5), (12, 14), (10.8, 21.5), (6.5, 21.5)], closed=True, r=S.r * 0.4)),
        detail(seg(6.5, 9.5, 17.5, 9.5)),
    ]


@icon("folded-clothes", CAT, "Stack of neatly folded shirts with the collar of the top one visible",
      tags=["laundry", "folded shirts", "clothing stack", "wardrobe", "tidy", "linen", "clothes"])
def _(S):
    return [
        shell(rect(3, 10, 18, 11, rr(S, 2.5))),
        shell(rect(5, 3, 14, 7, rr(S, 2))),
        detail(poly([(10, 3), (12, 6), (14, 3)], r=S.r * 0.5)),
        detail(seg(3, 15.5, 21, 15.5)),
    ]


@icon("stain-remover", CAT, "Pen shaped stain remover stick with a pointed tip aimed at a small splotch",
      tags=["stain pen", "spot cleaner", "laundry", "stain", "cleaning", "spot remover", "stain stick"])
def _(S):
    a, b = (20, 3), (12.5, 10.5)
    n = 2.3 / math.sqrt(2)
    tipp = (9.3, 13.7)
    pts = [(a[0] + n, a[1] + n), (b[0] + n, b[1] + n), tipp, (b[0] - n, b[1] - n), (a[0] - n, a[1] - n)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.6)),
        detail(poly([(11.3, 7.2), (15.6, 11.5)])),
        shell(circle(6.5, 18, 3)),
        dot(3, 13.5, 0.9), dot(12, 20.3, 0.9),
    ]


@icon("laundry-sorter", CAT, "Laundry cart with three fabric bags side by side on a metal frame and wheels",
      tags=["laundry hamper", "sorting cart", "laundry bags", "whites and colors", "laundry", "trolley", "clothes"])
def _(S):
    return [
        shell(rect(3, 4, 18, 10, rr(S, 2.5))),
        detail(seg(9, 4, 9, 14)), detail(seg(15, 4, 15, 14)),
        line(poly([(5, 14), (5, 19)])), line(poly([(19, 14), (19, 19)])),
        dot(5, 20.5, 1.4), dot(19, 20.5, 1.4),
    ]


@icon("dry-cleaning", CAT, "Garment on a hanger covered by a clear plastic bag with a paper ticket",
      tags=["dry cleaner", "garment bag", "cleaners", "suit", "plastic cover", "laundry service", "clothes"])
def _(S):
    return [
        line("M10 7V5.6"),
        line("M10 5.6A1.8 1.8 0 1 0 8.2 3.8"),
        shell(rect(3.5, 7, 13, 14.5, rr(S, 4))),
        detail(poly([(6.5, 13), (10, 11), (13.5, 13)], r=S.r * 0.6)),
        detail(poly([(7.3, 15.8), (10, 19), (12.7, 15.8)], r=S.r * 0.4)),
        mark(rect(19, 11, 2.6, 6, 0.6)),
    ]


@icon("fabric-shaver", CAT, "Handheld fabric shaver with a round mesh head on a slim body and a power button",
      tags=["lint remover", "pill remover", "bobble remover", "defuzzer", "sweater", "clothes care", "laundry"])
def _(S):
    return [
        shell(rect(8, 12.5, 8, 9, rr(S, 3))),
        shell(circle(12, 8, 5.5)),
        detail(circle(12, 8, 2)),
        dot(12, 17, 1),
    ]


@icon("care-label", CAT, "Garment care label hanging from a seam with lines of printed care text",
      tags=["clothing tag", "garment label", "wash instructions", "laundry tag", "textile label", "tag", "sewn in label"])
def _(S):
    return [
        line(seg(2, 4.5, 22, 4.5)),
        shell(rect(6, 4.5, 12, 17, rr(S, 1.5))),
        detail(seg(9.5, 9, 14.5, 9)),
        detail(seg(9.5, 13, 13, 13)),
        detail(seg(9.5, 17, 14.5, 17)),
    ]


@icon("spin-cycle", CAT, "Round washing drum with a swirl of curved arrows spinning inside it",
      tags=["spin dry", "washing machine", "rinse and spin", "laundry", "rotate", "drum", "centrifuge"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(arc(12, 12, 4.6, 200, 320)), detail(arc(12, 12, 4.6, 20, 140)),
        detail(tip(S, *polar(12, 12, 4.6, 320), 50, 2.0)),
        detail(tip(S, *polar(12, 12, 4.6, 140), 230, 2.0)),
    ]


@icon("shoe-polish", CAT, "Round shoe polish tin seen from above with a shoe outline on the lid",
      tags=["boot polish", "shoe shine", "shoe care", "cobbler", "wax tin", "cleaning", "leather"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(poly([(7.5, 8), (10.5, 8), (11, 11), (13, 12), (17, 13.5), (17, 16), (7.5, 16)], closed=True, r=S.r * 0.6)),
    ]


@icon("shoe-brush", CAT, "Shoe brush with a wooden back, a hand strap and a row of short bristles",
      tags=["shoe shine", "polishing brush", "boot brush", "shoe care", "cleaning", "cobbler", "bristles"])
def _(S):
    return [
        line("M7 7C7 3.5 17 3.5 17 7"),
        shell(rect(3, 7, 18, 6, rr(S, 2.5))),
        line(seg(6, 13, 6, 18)), line(seg(10, 13, 10, 18)), line(seg(14, 13, 14, 18)), line(seg(18, 13, 18, 18)),
    ]


@icon("shoe-horn", CAT, "Long curved shoe horn with a hanging hole at the handle end",
      tags=["shoehorn", "shoe helper", "footwear", "dressing aid", "hallway", "heel", "slip on"])
def _(S):
    top = "M13 2.5H18.5" if S.name == "line" else "M13 4.7Q13 2.5 15.2 2.5H16.3Q18.5 2.5 18.5 4.7"
    return [
        shell(top + "C18.5 11 16 16 10 19.3C8.3 20.3 5.5 21 4 20.2C3 19.4 3.4 17.8 5 16.8C10 13.8 13 10 13 4.7Z"
              if S.name != "line" else top + "C18.5 11 16 16 10 19.3C8.3 20.3 5.5 21 4 20.2C3 19.4 3.4 17.8 5 16.8C10 13.8 13 10 13 2.5Z"),
        dot(15.7, 5.6, 1.4),
    ]


@icon("shoe-tree", CAT, "Wooden shoe tree shaped like a shoe with a split between toe and heel blocks and a knob",
      tags=["shoe stretcher", "shoe form", "footwear care", "shoe keeper", "cedar", "boot tree", "shoe storage"])
def _(S):
    return [
        shell(poly([(3, 9), (10, 9), (11, 12), (14, 12.5), (20.5, 15), (21.5, 17), (21.5, 20.5), (3, 20.5)], closed=True, r=L(S, 0.8, 2.2))),
        detail(seg(10.5, 15, 10.5, 20.5)),
        line(seg(6.5, 9, 6.5, 6.3)),
        shell(circle(6.5, 4.6, 1.6)),
    ]


@icon("sewing-kit", CAT, "Small open tin holding thread spools, a needle and a thimble",
      tags=["sewing box", "travel sewing kit", "thread", "needle", "tailor", "mending", "haberdashery"])
def _(S):
    return [
        shell(rect(3, 12.5, 18, 9, rr(S, 3))),
        shell(rect(4.5, 4, 4.5, 8.5, rr(S, 1))),
        detail(seg(4.5, 8.2, 9, 8.2)),
        line(seg(12, 12.5, 12, 3)),
        shell(poly([(15, 12.5), (15.5, 7.5), (19.5, 7.5), (20, 12.5)], closed=True, r=L(S, 0.6, 1.6))),
    ]


@icon("thimble", CAT, "Dimpled metal thimble with a rounded top and a rim band",
      tags=["sewing", "finger protector", "needlework", "tailor", "quilting", "embroidery", "craft"])
def _(S):
    return [
        shell("M6 21.5L7.3 10.5C7.6 5.5 16.4 5.5 16.7 10.5L18 21.5Z") if S.name == "line" else
        shell("M6.3 21.5L7.4 11C7.7 5.8 16.3 5.8 16.6 11L17.7 21.5Z"),
        detail(seg(6.4, 18.2, 17.6, 18.2)),
        dot(9, 10.5, 0.85), dot(12, 10.5, 0.85), dot(15, 10.5, 0.85),
        dot(10.5, 14, 0.85), dot(13.5, 14, 0.85),
    ]


@icon("darning-egg", CAT, "Wooden darning egg on a short handle with darning stitches across it",
      tags=["sock darner", "mending", "sewing", "repair socks", "darn", "stitching", "craft"])
def _(S):
    return [
        shell(ellipse(12, 8, 7.5, 5.5)),
        detail(seg(7, 6.3, 17, 6.3)), detail(seg(7, 10.2, 17, 10.2)),
        shell(rect(10.3, 13.5, 3.4, 8, rr(S, 1.5))),
    ]


@icon("mothballs", CAT, "Three round mothballs in a cluster beside a small moth",
      tags=["moth repellent", "naphthalene", "closet", "pest control", "clothes storage", "moths", "camphor"])
def _(S):
    return [
        shell(circle(5, 18.5, 2.3)), shell(circle(11.4, 18.5, 2.3)), shell(circle(8.2, 12.8, 2.3)),
        shell(poly([(16.5, 8), (11.5, 3.5), (10.5, 10), (16.5, 12.8), (22.5, 10), (21.5, 3.5)], closed=True, r=L(S, 0, 1.2))),
        detail(seg(16.5, 4.5, 16.5, 12.3)),
    ]


def tub(S, top=4.5, bottom=18.5):
    """Laundry care washtub: a wide bowl with slightly sloping sides."""
    return shell(poly([(2.5, top), (21.5, top), (18.5, bottom), (5.5, bottom)], closed=True, r=L(S, 0.8, 2.2)))


@icon("care-machine-wash", CAT, "Laundry care symbol: a washtub with a wavy water line",
      tags=["washing symbol", "care symbol", "laundry label", "machine washable", "wash cycle", "garment care", "wash tub"])
def _(S):
    return [tub(S), detail("M6.5 12Q8.5 9.5 10.5 12T14.5 12T18.5 12")]


@icon("care-hand-wash", CAT, "Laundry care symbol: a washtub with a hand dipped into the water",
      tags=["hand washable", "washing symbol", "care symbol", "laundry label", "gentle wash", "garment care", "wash by hand"])
def _(S):
    return [
        tub(S, 10, 21),
        line(seg(9, 2.5, 9, 10)), line(seg(14.5, 2.5, 14.5, 10)),
        detail("M9 10.5V12.5Q9 15.5 11.75 15.5Q14.5 15.5 14.5 12.5V10.5"),
    ]


@icon("care-delicate-wash", CAT, "Laundry care symbol: a washtub with two horizontal lines underneath it",
      tags=["delicate cycle", "gentle wash", "care symbol", "laundry label", "washing symbol", "garment care", "wool wash"])
def _(S):
    return [tub(S, 2.5, 14.5), line(seg(3, 18.2, 21, 18.2)), line(seg(3, 21.5, 21, 21.5))]


@icon("care-wash-cold", CAT, "Laundry care symbol: a washtub with one dot inside for cold water",
      tags=["cold wash", "30 degrees", "care symbol", "laundry label", "washing temperature", "garment care", "cold water"])
def _(S):
    return [tub(S), dot(12, 11.5, 1.4)]


@icon("care-wash-warm", CAT, "Laundry care symbol: a washtub with two dots inside for warm water",
      tags=["warm wash", "40 degrees", "care symbol", "laundry label", "washing temperature", "garment care", "warm water"])
def _(S):
    return [tub(S), dot(9.5, 11.5, 1.4), dot(14.5, 11.5, 1.4)]


@icon("care-wash-hot", CAT, "Laundry care symbol: a washtub with three dots inside for hot water",
      tags=["hot wash", "60 degrees", "care symbol", "laundry label", "washing temperature", "garment care", "hot water"])
def _(S):
    return [tub(S), dot(7.5, 11.5, 1.4), dot(12, 11.5, 1.4), dot(16.5, 11.5, 1.4)]


@icon("care-bleach", CAT, "Laundry care symbol: an empty outline triangle meaning any bleach may be used",
      tags=["bleach allowed", "care symbol", "laundry label", "whitener", "chlorine bleach", "garment care", "triangle"])
def _(S):
    return [shell(poly([(12, 3.5), (21.5, 20.5), (2.5, 20.5)], closed=True, r=L(S, 0.6, 2.2)))]


@icon("care-non-chlorine-bleach", CAT, "Laundry care symbol: a triangle with two diagonal lines inside",
      tags=["oxygen bleach", "non chlorine bleach only", "care symbol", "laundry label", "color safe bleach", "garment care", "triangle"])
def _(S):
    return [
        shell(poly([(12, 3.5), (21.5, 20.5), (2.5, 20.5)], closed=True, r=L(S, 0.6, 2.2))),
        detail(seg(9, 18, 11.8, 13.5)), detail(seg(13, 18, 15.8, 13.5)),
    ]


@icon("care-tumble-dry", CAT, "Laundry care symbol: a square with a circle inside it",
      tags=["tumble dryer", "dryer safe", "care symbol", "laundry label", "machine dry", "garment care", "drying symbol"])
def _(S):
    return [shell(rect(3, 3, 18, 18, rr(S, 3))), detail(circle(12, 12, 5.2))]


@icon("care-tumble-dry-low", CAT, "Laundry care symbol: a square with a circle and one dot inside",
      tags=["low heat dryer", "tumble dry low", "care symbol", "laundry label", "gentle dry", "garment care", "drying symbol"])
def _(S):
    return [shell(rect(3, 3, 18, 18, rr(S, 3))), detail(circle(12, 12, 5.6)), dot(12, 12, 1.2)]


@icon("care-tumble-dry-high", CAT, "Laundry care symbol: a square with a circle and three dots inside",
      tags=["high heat dryer", "tumble dry high", "care symbol", "laundry label", "hot dry", "garment care", "drying symbol"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))), detail(circle(12, 12, 6)),
        dot(12, 9.5, 1), dot(9.7, 13.5, 1), dot(14.3, 13.5, 1),
    ]


@icon("care-line-dry", CAT, "Laundry care symbol: a square with a line hanging down in a loop from the top edge",
      tags=["hang to dry", "clothesline", "care symbol", "laundry label", "air dry", "garment care", "drying symbol"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail("M7.5 3V8Q7.5 15 12 15Q16.5 15 16.5 8V3"),
    ]


@icon("care-drip-dry", CAT, "Laundry care symbol: a square with three vertical lines inside",
      tags=["drip drying", "dry dripping wet", "care symbol", "laundry label", "no wring", "garment care", "drying symbol"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(seg(7.5, 7, 7.5, 17)), detail(seg(12, 7, 12, 17)), detail(seg(16.5, 7, 16.5, 17)),
    ]


@icon("care-dry-flat", CAT, "Laundry care symbol: a square with one horizontal line across the middle",
      tags=["lay flat to dry", "flat drying", "care symbol", "laundry label", "sweater dry", "garment care", "drying symbol"])
def _(S):
    return [shell(rect(3, 3, 18, 18, rr(S, 3))), detail(seg(7, 12, 17, 12))]


@icon("care-dry-in-shade", CAT, "Laundry care symbol: a square with two short diagonal lines in its top left corner",
      tags=["dry in shade", "no direct sun", "care symbol", "laundry label", "shade drying", "garment care", "drying symbol"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(seg(5.5, 9.5, 9.5, 5.5)), detail(seg(7, 13, 13, 7)),
    ]


def iron_shell(S):
    return shell(poly([(3, 19.5), (21, 19.5), (21, 15), (15.5, 6.5), (3, 6.5)], closed=True, r=L(S, 0.8, 2.2)))


@icon("care-iron-low", CAT, "Laundry care symbol: an iron outline with one dot inside",
      tags=["iron low heat", "cool iron", "care symbol", "laundry label", "ironing", "garment care", "one dot"])
def _(S):
    return [iron_shell(S), dot(11, 14, 1.4)]


@icon("care-iron-medium", CAT, "Laundry care symbol: an iron outline with two dots inside",
      tags=["iron medium heat", "warm iron", "care symbol", "laundry label", "ironing", "garment care", "two dots"])
def _(S):
    return [iron_shell(S), dot(8.5, 14, 1.4), dot(13.5, 14, 1.4)]


@icon("care-iron-high", CAT, "Laundry care symbol: an iron outline with three dots inside",
      tags=["iron high heat", "hot iron", "care symbol", "laundry label", "ironing", "garment care", "three dots"])
def _(S):
    return [iron_shell(S), dot(7, 14, 1.4), dot(11.5, 14, 1.4), dot(16, 14, 1.4)]


@icon("care-steam-iron", CAT, "Laundry care symbol: an iron outline with short steam lines below its sole",
      tags=["steam ironing", "steam allowed", "care symbol", "laundry label", "ironing", "garment care", "steam"])
def _(S):
    return [
        shell(poly([(3, 14), (21, 14), (21, 10.5), (15.5, 3), (3, 3)], closed=True, r=L(S, 0.8, 2.2))),
        line(seg(7, 17.5, 7, 21.5)), line(seg(12, 17.5, 12, 21.5)), line(seg(17, 17.5, 17, 21.5)),
    ]


@icon("care-dry-clean", CAT, "Laundry care symbol: an empty outline circle for professional dry cleaning",
      tags=["dry clean", "professional cleaning", "care symbol", "laundry label", "cleaners", "garment care", "circle"])
def _(S):
    return [shell(circle(12, 12, L(S, 9, 8.4)))]


@icon("care-wet-clean", CAT, "Laundry care symbol: a circle with the letter W inside",
      tags=["professional wet cleaning", "wet clean", "care symbol", "laundry label", "cleaners", "garment care", "letter w"])
def _(S):
    return [
        shell(circle(12, 12, L(S, 9, 8.4))),
        detail(poly([(7.3, 8.5), (9.6, 15.5), (12, 10), (14.4, 15.5), (16.7, 8.5)], r=S.r * 0.4)),
    ]


@icon("care-wring", CAT, "Laundry care symbol: a twisted cloth shaped like a bow with a knot in the middle",
      tags=["wring", "twist", "can be wrung", "care symbol", "laundry label", "garment care", "twisted cloth"])
def _(S):
    k = L(S, 0.6, 1.6)
    return [
        shell(poly([(2.5, 6.5), (10, 10.5), (10, 13.5), (2.5, 17.5)], closed=True, r=k)),
        shell(poly([(21.5, 6.5), (14, 10.5), (14, 13.5), (21.5, 17.5)], closed=True, r=k)),
        shell(rect(9.5, 8.5, 5, 7, rr(S, 2.5))),
    ]


def stick(S, p0, p1, tj, h1, h2, pt_end=True):
    """Polygon of a tool along p0 to p1: a slim handle (half width h1) that widens to h2 from fraction tj."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    nx, ny = -uy, ux
    q = (p0[0] + dx * tj, p0[1] + dy * tj)
    return [(p0[0] + nx * h1, p0[1] + ny * h1), (q[0] + nx * h1, q[1] + ny * h1), (q[0] + nx * h2, q[1] + ny * h2),
            (p1[0] + nx * h2, p1[1] + ny * h2), (p1[0] - nx * h2, p1[1] - ny * h2), (q[0] - nx * h2, q[1] - ny * h2),
            (q[0] - nx * h1, q[1] - ny * h1), (p0[0] - nx * h1, p0[1] - ny * h1)], (ux, uy), (nx, ny)


@icon("toothbrush", CAT, "Toothbrush at an angle with a long handle and a tuft of bristles at the head",
      tags=["brush teeth", "dental care", "oral hygiene", "bristles", "bathroom", "dentist", "teeth cleaning"])
def _(S):
    p0, p1 = (11.4, 12.6), (19.6, 4.4)
    nrm = (math.sqrt(0.5), math.sqrt(0.5))
    parts = [
        line(seg(3.8, 20.2, 12, 12)),
        shell(poly(bar(p0, p1, 4.4), closed=True, r=L(S, 0.6, 1.4))),
    ]
    for t in (0.2, 0.5, 0.8):
        bx, by = p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t
        parts.append(line(seg(bx - nrm[0] * 2.2, by - nrm[1] * 2.2, bx - nrm[0] * 4.8, by - nrm[1] * 4.8)))
    return parts


@icon("electric-toothbrush", CAT, "Electric toothbrush with a thick handle, a power button and a small round head",
      tags=["powered toothbrush", "sonic toothbrush", "oral care", "dental hygiene", "rechargeable", "bathroom", "teeth cleaning"])
def _(S):
    return [
        shell(rect(8.5, 10, 6.5, 11.5, rr(S, 3))),
        dot(11.75, 14, 1.1),
        line(seg(11.75, 8, 11.75, 10)),
        shell(rect(9.5, 2.5, 4.5, 5.5, rr(S, 2))),
        line(seg(14, 4, 17.5, 4)), line(seg(14, 6.6, 17.5, 6.6)),
    ]


@icon("toothpaste", CAT, "Squeezed toothpaste tube lying on its side with a screw cap and a curl of paste",
      tags=["tube", "dental care", "oral hygiene", "teeth cleaning", "paste", "bathroom", "brushing"])
def _(S):
    return [
        shell(poly([(2.5, 7), (2.5, 17), (13.5, 15.5), (13.5, 8.5)], closed=True, r=L(S, 0.5, 1.6))),
        detail(seg(5.6, 7, 5.6, 17)),
        shell(rect(13.5, 9.6, 3.5, 4.8, rr(S, 1))),
        line("M17 12H19.3A2.4 2.4 0 1 0 19.3 7.2"),
    ]


@icon("dental-floss", CAT, "Floss dispenser box with a strand of floss pulled out from its side",
      tags=["flossing", "interdental cleaning", "oral hygiene", "teeth", "dental care", "string", "bathroom"])
def _(S):
    return [
        shell(rect(3, 7.5, 13.5, 13.5, rr(S, 4))),
        detail(circle(9.75, 14.25, 3)),
        line("M16.5 12H19Q21.5 12 21.5 9V3.5"),
    ]


@icon("floss-pick", CAT, "Plastic floss pick with a forked head holding a taut strand and a pointed handle",
      tags=["flosser", "dental pick", "interdental", "oral hygiene", "teeth cleaning", "dental care", "disposable"])
def _(S):
    return [
        shell(poly([(12, 21.5), (10, 14.5), (10.4, 11), (13.6, 11), (14, 14.5)], closed=True, r=L(S, 0.5, 1.3))),
        line("M10.6 11Q7.8 8 8.5 3.5"), line("M13.4 11Q16.2 8 15.5 3.5"),
        line(seg(8.4, 3.5, 15.6, 3.5)),
    ]


@icon("interdental-brush", CAT, "Tiny bottle brush with bristles around a thin wire on a short handle",
      tags=["proxy brush", "gap cleaning", "braces cleaning", "oral hygiene", "dental care", "teeth"])
def _(S):
    return [
        shell(rect(9, 12.5, 6, 9, rr(S, 2.5))),
        line(seg(12, 12.5, 12, 2.5)),
        line(seg(9, 4, 15, 4)), line(seg(9, 7, 15, 7)), line(seg(9.5, 10, 14.5, 10)),
    ]


@icon("mouthwash", CAT, "Rounded bottle with a large cup shaped cap and a wave on the label",
      tags=["mouth rinse", "oral care", "gargle", "dental hygiene", "fresh breath", "bathroom", "antiseptic"])
def _(S):
    return [
        shell(rect(8, 2.5, 8, 4.5, rr(S, 1.5))),
        shell(rect(6, 7.5, 12, 14, rr(S, 4))),
        detail("M8.5 15.2Q10.3 12.7 12 15.2T15.5 15.2"),
    ]


@icon("breath-spray", CAT, "Small slim spray bottle with a mint leaf on the label and a puff of spray",
      tags=["mouth spray", "fresh breath", "mint", "oral care", "pocket spray", "bad breath", "freshener"])
def _(S):
    return [
        shell(rect(8, 8.5, 9, 13, rr(S, 3))),
        shell(rect(10, 4.5, 5, 4, rr(S, 1))),
        line(seg(8.3, 5.5, 4.5, 4)), line(seg(8.3, 7.3, 4, 8)),
        mark("M10.6 18.2C10.6 14.6 12.4 13.2 14.4 13.2C14.4 16.8 12.6 18.2 10.6 18.2Z"),
    ]


@icon("tongue-scraper", CAT, "U shaped flexible tongue scraper with a small grip on each end",
      tags=["tongue cleaner", "oral hygiene", "fresh breath", "dental care", "bathroom", "metal scraper", "mouth care"])
def _(S):
    k = L(S, 0.5, 2.5)
    return [
        line("M6 8.5C6 20 18 20 18 8.5"),
        shell(rect(3, 3.5, 6, 5, k)),
        shell(rect(15, 3.5, 6, 5, k)),
    ]


@icon("water-flosser", CAT, "Water flosser with a reservoir base and a wand spraying a thin jet of water",
      tags=["oral irrigator", "dental jet", "gum care", "oral hygiene", "flossing", "bathroom"])
def _(S):
    return [
        shell(rect(2.5, 9, 10, 12.5, rr(S, 3))),
        detail(seg(2.5, 14.5, 12.5, 14.5)),
        line(seg(12.5, 18.5, 15.5, 18.5)),
        shell(rect(15.5, 13, 4.5, 8.5, rr(S, 2))),
        line(seg(17.75, 13, 17.75, 8)),
        dot(17.75, 5, 1), dot(14.6, 5.6, 0.9), dot(20.9, 5.6, 0.9),
    ]


@icon("dentures", CAT, "Set of false teeth with an upper and a lower row, slightly apart",
      tags=["false teeth", "dental plate", "denture", "prosthetic teeth", "dentist", "elderly care", "oral health"])
def _(S):
    return [
        shell(rect(3, 3, 18, 7.5, rr(S, 3))),
        detail(seg(7.5, 3, 7.5, 10.5)), detail(seg(12, 3, 12, 10.5)), detail(seg(16.5, 3, 16.5, 10.5)),
        shell(rect(3, 14, 18, 7, rr(S, 3))),
        detail(seg(7.5, 14, 7.5, 21)), detail(seg(12, 14, 12, 21)), detail(seg(16.5, 14, 16.5, 21)),
    ]


@icon("dental-retainer", CAT, "Horseshoe shaped orthodontic retainer with a thin wire arching around the front",
      tags=["orthodontic retainer", "teeth retainer", "clear retainer", "orthodontics", "dentist", "aligner", "braces"])
def _(S):
    if S.name == "line":
        plate = "M6 4C6 12.5 8.5 16.5 12 16.5C15.5 16.5 18 12.5 18 4H14.5C14.5 9.5 13.5 12 12 12C10.5 12 9.5 9.5 9.5 4Z"
    else:
        plate = ("M6 5.75Q6 4 7.75 4Q9.5 4 9.5 5.75C9.5 9.5 10.5 12 12 12C13.5 12 14.5 9.5 14.5 5.75Q14.5 4 16.25 4Q18 4 18 5.75"
                 "C18 12.5 15.5 16.5 12 16.5C8.5 16.5 6 12.5 6 5.75Z")
    return [
        shell(plate),
        line("M2.8 6C2.8 17 7 20.8 12 20.8C17 20.8 21.2 17 21.2 6"),
    ]


@icon("teeth-braces", CAT, "Row of three teeth with small square brackets joined by a wire",
      tags=["orthodontics", "dental braces", "brackets", "orthodontist", "teeth straightening", "dentist", "smile"])
def _(S):
    return [
        shell(rect(2.5, 5, 19, 14, rr(S, 4))),
        detail(seg(8.83, 5, 8.83, 19)), detail(seg(15.17, 5, 15.17, 19)),
        detail(seg(2.5, 12, 21.5, 12)),
        sq(4.2, 10.5, 3, 3, 0.4), sq(10.5, 10.5, 3, 3, 0.4), sq(16.8, 10.5, 3, 3, 0.4),
    ]


@icon("mouth-guard", CAT, "Horseshoe shaped sports mouth guard with a thick rim and a channel for the teeth",
      tags=["gum shield", "mouthpiece", "sports protection", "boxing", "night guard", "teeth protection", "dentist"])
def _(S):
    if S.name == "line":
        g = "M2.5 4C2.5 16 6.5 21 12 21C17.5 21 21.5 16 21.5 4H15.5C15.5 10 14.5 13 12 13C9.5 13 8.5 10 8.5 4Z"
    else:
        g = ("M2.5 7Q2.5 4 5.5 4Q8.5 4 8.5 7C8.5 10 9.5 13 12 13C14.5 13 15.5 10 15.5 7Q15.5 4 18.5 4Q21.5 4 21.5 7"
             "C21.5 16 17.5 21 12 21C6.5 21 2.5 16 2.5 7Z")
    return [
        shell(g),
        detail("M5.5 6C5.5 14 8 17.5 12 17.5C16 17.5 18.5 14 18.5 6"),
    ]


def pick(S, a, b, tipl=3.0):
    """A toothpick: a stroke from a to b ending in a solid pointed tip."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    tp = (b[0] + ux * tipl, b[1] + uy * tipl)
    nx, ny = -uy, ux
    tri = [(b[0] + nx, b[1] + ny), tp, (b[0] - nx, b[1] - ny)]
    return [line(seg(a[0], a[1], b[0], b[1])), solid(poly(tri, closed=True))]


@icon("toothpick", CAT, "Two thin pointed toothpicks crossed at an angle",
      tags=["tooth pick", "cocktail stick", "wooden pick", "dental pick", "snack pick", "dining", "restaurant"])
def _(S):
    return pick(S, (3.5, 20.5), (17, 7)) + pick(S, (9, 3.5), (15.5, 17.5))


@icon("miswak", CAT, "Natural chewing stick twig with a frayed bristly tip at one end",
      tags=["siwak", "chewing stick", "natural toothbrush", "twig", "oral hygiene", "arak", "teeth cleaning"])
def _(S):
    return [
        shell(poly(bar((3.6, 20.4), (13.4, 10.6), 4.0), closed=True, r=L(S, 0.4, 1.2))),
        line(seg(14.6, 9.4, 17, 4)), line(seg(15.2, 8.8, 20, 7.2)), line(seg(15.8, 8.2, 21, 12)),
    ]


@icon("brushing-teeth", CAT, "Smiling mouth with a toothbrush brushing across its teeth and a bubble nearby",
      tags=["brush teeth", "dental hygiene", "morning routine", "oral care", "teeth cleaning", "bubbles", "smile"])
def _(S):
    return [
        shell("M3 12H21C21 18 17 21.5 12 21.5C7 21.5 3 18 3 12Z"),
        detail(seg(8.5, 12, 8.5, 16)), detail(seg(15.5, 12, 15.5, 16)),
        line(seg(2.8, 5.5, 10, 5.5)),
        shell(rect(10, 3.3, 6.5, 4.4, rr(S, 1.5))),
        line(seg(12, 7.7, 12, 9.2)), line(seg(14.6, 7.7, 14.6, 9.2)),
        shell(circle(20, 4.5, 1.5)),
    ]


# ============================================================================ grooming and skin care

def hand_glyph(cx, cy, k=1.0):
    """Tiny solid hand (palm and three fingers) for product labels."""
    x0, y0 = cx - 3 * k, cy - 3.5 * k
    palm = rect(x0, y0 + 2.3 * k, 6 * k, 4.7 * k, 1.0 * k)
    hs = (3.0, 3.9, 3.0)
    return path_to_d(U(P(palm), *[P(rect(x0 + i * 2.3 * k, y0 + (3.9 - hs[i]) * k, 1.4 * k, hs[i] + 0.5 * k, 0.6 * k)) for i in range(3)]))


def drop_d(cx, top, w, h):
    """Small teardrop with its point up."""
    my = top + h - w / 2
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + w * 0.3)} {fmt(top + h * 0.3)} {fmt(cx + w / 2)} {fmt(my - h * 0.2)} {fmt(cx + w / 2)} {fmt(my)}"
            f"A{fmt(w / 2)} {fmt(w / 2)} 0 0 1 {fmt(cx - w / 2)} {fmt(my)}"
            f"C{fmt(cx - w / 2)} {fmt(my - h * 0.2)} {fmt(cx - w * 0.3)} {fmt(top + h * 0.3)} {fmt(cx)} {fmt(top)}Z")


@icon("deodorant-stick", CAT, "Twist-up deodorant stick with its cap off, showing a slanted solid top",
      tags=["antiperspirant", "underarm", "personal care", "hygiene", "bathroom", "stick", "body odor"])
def _(S):
    return [
        shell(poly([(8.5, 12), (8.5, 8.5), (15.5, 4.5), (15.5, 12)], closed=True, r=L(S, 0.5, 1.8))),
        shell(rect(6, 12, 12, 9.5, rr(S, 2.5))),
        detail(seg(6, 17, 18, 17)),
    ]


@icon("roll-on-deodorant", CAT, "Small roll-on bottle with a ball on top of a shouldered body",
      tags=["antiperspirant", "underarm", "personal care", "hygiene", "bathroom", "ball applicator", "body odor"])
def _(S):
    return [
        shell(poly([(6.5, 21.5), (6.5, 14), (9, 10.5), (15, 10.5), (17.5, 14), (17.5, 21.5)], closed=True, r=L(S, 1, 3))),
        shell(circle(12, 6.5, 3)),
        detail(seg(6.5, 17, 17.5, 17)),
    ]


@icon("body-lotion", CAT, "Pump bottle of lotion with a drop of cream at the nozzle",
      tags=["moisturizer", "skin care", "cream", "pump dispenser", "bathroom", "hydrating", "cosmetics"])
def _(S):
    return [
        shell(rect(6, 12.5, 12, 9, rr(S, 3))),
        shell(rect(10.5, 9, 3, 3.5, 0.5)),
        line(poly([(9, 5.5), (17, 5.5), (17, 7.3)], r=S.r)),
        line(seg(12, 5.5, 12, 9)),
        mark(drop_d(17, 8.6, 2, 2.8)),
    ]


@icon("shower-gel", CAT, "Squeeze bottle standing upside down on its flip cap with a bubble on the label",
      tags=["body wash", "shampoo", "soap", "bathroom", "shower", "bubbles", "personal care"])
def _(S):
    return [
        shell(poly([(6, 3), (18, 3), (17, 16.5), (7, 16.5)], closed=True, r=L(S, 1.2, 3.2))),
        shell(rect(8.5, 16.5, 7, 5, rr(S, 1.5))),
        detail(circle(11.3, 8.5, 2.3)),
        dot(15, 12.2, 1),
    ]


@icon("hand-cream", CAT, "Flat squeeze tube standing on its flip cap with a small hand symbol on the label",
      tags=["hand lotion", "moisturizer", "skin care", "tube", "cosmetics", "personal care", "dry hands"])
def _(S):
    return [
        shell(poly([(8, 17), (6.5, 3.5), (17.5, 3.5), (16, 17)], closed=True, r=L(S, 0.6, 1.8))),
        detail(seg(6.7, 6.3, 17.3, 6.3)),
        shell(rect(8.3, 17, 7.4, 4.5, rr(S, 1.5))),
        mark(hand_glyph(12, 12.3, 0.9)),
    ]


@icon("face-cream", CAT, "Short wide cream jar with its lid lifted above it and a swirl of cream rising from the top",
      tags=["moisturizer", "skin care", "beauty", "cosmetics", "jar", "night cream", "facial"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 4.5, rr(S, 2))),
        line("M7 12.5C7 8.5 11 8.5 12 9.5C13 8.5 17 8.5 17 12.5"),
        shell(rect(3, 12.5, 18, 9, rr(S, 3))),
    ]


@icon("sunscreen", CAT, "Squeeze bottle with a flip cap and a sun symbol on its label",
      tags=["sun cream", "sunblock", "spf", "sun protection", "beach", "skin care", "summer"])
def _(S):
    parts = [
        shell(rect(9, 2.5, 6, 4.5, rr(S, 1.5))),
        shell(rect(6, 7, 12, 14.5, rr(S, 3))),
        dot(12, 14.3, 1.7),
    ]
    for k in range(8):
        x, y = polar(12, 14.3, 3.5, k * 45)
        parts.append(dot(x, y, 0.65))
    return parts


@icon("hand-sanitizer", CAT, "Small flip top bottle with a hand symbol on its label and a gel drop at the spout",
      tags=["hand gel", "sanitiser", "disinfectant", "hygiene", "germs", "antibacterial", "clean hands"])
def _(S):
    return [
        shell(rect(6.5, 10, 11, 11.5, rr(S, 3))),
        shell(rect(8.8, 6, 6.4, 4, rr(S, 1.2))),
        line(poly([(15.2, 7.6), (19.5, 7.6)], r=0)),
        mark(drop_d(19.5, 9.4, 2.2, 3)),
        mark(hand_glyph(12, 16, 0.7)),
    ]


def swab_head(S, a, b, w=4.6, L_=4.2):
    """Cotton head: a short fat bar starting at the stick end `b` and running out along the stick direction."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    return shell(poly(bar((b[0] - ux * 0.5, b[1] - uy * 0.5), (b[0] + ux * L_, b[1] + uy * L_), w), closed=True, r=L(S, 0.8, 2.2)))


@icon("cotton-swab", CAT, "Two cotton swabs crossed, each a thin stick with fluffy tips at both ends",
      tags=["ear bud", "cotton bud", "ear cleaning", "makeup", "first aid", "hygiene"])
def _(S):
    a1, b1 = (7, 17), (17, 7)
    a2, b2 = (8.5, 7), (15.5, 17)
    return [
        line(seg(a1[0], a1[1], b1[0], b1[1])), swab_head(S, a1, b1), swab_head(S, b1, a1),
        line(seg(a2[0], a2[1], b2[0], b2[1])), swab_head(S, a2, b2), swab_head(S, b2, a2),
    ]


@icon("cotton-pad", CAT, "Round flat cotton pad with a quilted dotted pattern",
      tags=["makeup remover pad", "cotton round", "toner pad", "skin care", "beauty", "cosmetics", "facial"])
def _(S):
    return [
        shell(circle(12, 12, L(S, 9, 8.4))),
        dot(12, 12, 1), dot(8, 12, 0.9), dot(16, 12, 0.9), dot(12, 8, 0.9), dot(12, 16, 0.9),
        dot(9.2, 9.2, 0.8), dot(14.8, 9.2, 0.8), dot(9.2, 14.8, 0.8), dot(14.8, 14.8, 0.8),
    ]


def scallop(cx, cy, r, n, a0=-90.0, bulge=0.56):
    """Fluffy ball outline: n outward bumps around a circle."""
    pts = [polar(cx, cy, r, a0 + i * 360.0 / n) for i in range(n)]
    chord = 2 * r * math.sin(math.pi / n)
    rad = chord * bulge
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(1, n + 1):
        q = pts[i % n]
        d += f"A{fmt(rad)} {fmt(rad)} 0 0 1 {fmt(q[0])} {fmt(q[1])}"
    return d + "Z"


@icon("cotton-balls", CAT, "Three fluffy cotton balls with soft scalloped outlines",
      tags=["cotton wool", "cotton", "first aid", "makeup remover", "skin care", "soft", "fluffy"])
def _(S):
    n = L(S, 7, 6)
    return [
        shell(scallop(12, 7, 3.9, n, bulge=0.6)),
        shell(scallop(6.4, 16.8, 3.9, n, -60, bulge=0.6)),
        shell(scallop(17.6, 16.8, 3.9, n, -120, bulge=0.6)),
    ]


@icon("tweezers", CAT, "Slanted tip tweezers seen from the side, two arms joined at the top",
      tags=["tweezer", "eyebrow", "plucking", "beauty", "grooming", "splinter", "precision"])
def _(S):
    k = L(S, 0.6, 2.0)
    return [
        line(poly([(12, 2.5), (9.3, 12), (11, 21.5)], r=k)),
        line(poly([(12, 2.5), (14.7, 12), (13, 21.5)], r=k)),
        line(seg(9.6, 8.5, 14.4, 8.5)),
    ]


@icon("nail-clippers", CAT, "Nail clipper with a curved lever arm on top of its jaws",
      tags=["nail cutter", "manicure", "pedicure", "grooming", "trimming nails", "fingernails", "toenails"])
def _(S):
    return [
        shell(rect(3, 12.5, 18, 5.5, rr(S, 2.5))),
        line("M3.5 9C9 6 16 6 20.5 10"),
        dot(19.5, 9.2, 1.3),
        detail(seg(7, 12.5, 7, 18)),
    ]


@icon("nail-file", CAT, "Long narrow emery board with rounded ends and a gritty texture",
      tags=["emery board", "manicure", "filing nails", "grooming", "nail care", "beauty", "abrasive"])
def _(S):
    parts = [shell(poly(bar((4.2, 19.8), (19.8, 4.2), 5.4), closed=True, r=L(S, 1.2, 2.7)))]
    for t in (0.3, 0.5, 0.7):
        parts.append(dot(4.2 + 15.6 * t, 19.8 - 15.6 * t, 0.85))
    return parts


@icon("nail-scissors", CAT, "Small scissors with short curved blades and round finger loops",
      tags=["manicure scissors", "cuticle scissors", "grooming", "nail care", "beauty", "trimming", "curved blades"])
def _(S):
    return [
        shell(circle(7, 18, 3)), shell(circle(17, 18, 3)),
        line("M8.3 15.2C10 10.5 12.8 6.2 16 3"), line("M15.7 15.2C14 10.5 11.2 6.2 8 3"),
        dot(12, 9.6, 1.1),
    ]


@icon("cuticle-nipper", CAT, "Small plier-like cuticle nipper with a spring between its handles",
      tags=["cuticle cutter", "manicure", "nail care", "grooming", "beauty", "hangnail", "pedicure"])
def _(S):
    return [
        shell(poly([(12, 2.5), (15.5, 6.5), (13.8, 10.5), (10.2, 10.5), (8.5, 6.5)], closed=True, r=L(S, 0.8, 2))),
        line(seg(10.5, 10.5, 6.8, 21)), line(seg(13.5, 10.5, 17.2, 21)),
        line(poly([(9.4, 17.4), (12, 14), (14.6, 17.4)], r=S.r)),
    ]


@icon("cuticle-pusher", CAT, "Slim double ended tool with a flat spoon tip at one end and a pointed tip at the other",
      tags=["manicure", "nail care", "cuticle", "grooming", "beauty", "orange stick", "nail tool"])
def _(S):
    A, B = (3.2, 20.8), (20.8, 3.2)
    dx, dy = B[0] - A[0], B[1] - A[1]
    n = math.hypot(dx, dy)
    u = (dx / n, dy / n)
    nr = (-u[1], u[0])
    def at(t, h):
        return (A[0] + dx * t + nr[0] * h, A[1] + dy * t + nr[1] * h)
    pts = [A, at(0.22, 1.2), at(0.72, 1.2), at(0.82, 2.3), at(1.0, 1.5), at(1.0, -1.5), at(0.82, -2.3), at(0.72, -1.2), at(0.22, -1.2)]
    return [shell(poly(pts, closed=True, r=L(S, 0.5, 1.2)))]


@icon("nail-buffer", CAT, "Slanted foam buffer block with three bands of different texture",
      tags=["nail polisher", "shine block", "manicure", "nail care", "beauty", "grooming", "buffing"])
def _(S):
    return [
        shell(poly([(6.5, 6), (21.5, 6), (17.5, 18), (2.5, 18)], closed=True, r=L(S, 0.8, 2.4))),
        detail(seg(11.5, 6, 7.5, 18)), detail(seg(16.5, 6, 12.5, 18)),
        dot(6.6, 12, 0.9), dot(11.6, 12, 0.9), dot(16.3, 12, 0.9),
    ]


@icon("foot-file", CAT, "Paddle shaped foot file with a rough grating surface and a handle",
      tags=["callus remover", "pedicure", "foot care", "heel scrubber", "grater", "spa", "dry skin"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 11.5, rr(S, 5))),
        dot(9.2, 6.3, 0.9), dot(14.8, 6.3, 0.9), dot(12, 8.5, 0.9), dot(9.2, 10.7, 0.9), dot(14.8, 10.7, 0.9),
        shell(rect(10, 14, 4, 7.5, rr(S, 1.8))),
    ]


@icon("pumice-stone", CAT, "Oval porous pumice stone with scattered small holes",
      tags=["pumice", "callus stone", "foot care", "pedicure", "exfoliate", "rough stone", "spa"])
def _(S):
    return [
        shell(poly([(4, 12), (6.5, 6.5), (13, 4.5), (19, 7), (20.5, 13), (16, 19), (9, 19.5)], closed=True, r=L(S, 2, 5))),
        dot(9, 9.5, 1), dot(14.5, 8.8, 0.9), dot(12, 13, 1.1), dot(16.5, 14, 0.8), dot(8.3, 14.6, 0.8),
    ]
