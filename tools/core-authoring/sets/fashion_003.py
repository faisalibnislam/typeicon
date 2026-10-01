"""TypeIcon Core: fashion (batch fashion_003).

Footwear, bags, jewellery, gems, watches and eyewear. Shoes point right with the heel on the left, in the
same proportions as sets/clothing.py. Solid panels (saddle bands, hatching) use `dot`-kind parts, which are
solid in Line/Rounded and knocked out in Filled.
"""
import math

from dsl import D, I, P, Part, ST, U, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar  # noqa: F401

CAT = "fashion"


def _band(outline_d, pts):
    """Part of a closed outline inside a polygon, as a d-string (shaded panels)."""
    return path_to_d(I(P(outline_d), P(poly(pts, closed=True))))


def _aglet(x1, y1, x2, y2, w=2.6, n=3.2):
    """Small solid tip at the end (x2,y2) of a lace running from (x1,y1)."""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    px, py = -uy * w / 2, ux * w / 2
    bx, by = x2 - ux * n, y2 - uy * n
    return solid(poly([(bx + px, by + py), (x2 + px, y2 + py), (x2 - px, y2 - py), (bx - px, by - py)], closed=True))


def _lattice(outline_d, step=6.0, w=1.6, x0=-6, x1=30, y0=-6, y1=30):
    """Diagonal criss-cross strands clipped to a closed outline (weave, mesh), as a d-string."""
    ds = ""
    c = x0 - (y1 - y0)
    while c < x1:
        ds += f"M{fmt(c)} {fmt(y0)}L{fmt(c + (y1 - y0))} {fmt(y1)}"
        ds += f"M{fmt(c + (y1 - y0))} {fmt(y0)}L{fmt(c)} {fmt(y1)}"
        c += step
    return path_to_d(I(P(outline_d), ST(ds, w, "butt", "miter")))


def _ep(cx, cy, rx, ry, n=10, start=-90.0):
    """Points on an ellipse (for faceted Line versions of round shapes)."""
    return [(cx + rx * math.cos(math.radians(start + i * 360 / n)), cy + ry * math.sin(math.radians(start + i * 360 / n)))
            for i in range(n)]


def _ring(S, cx, cy, rx, ry=None, n=8):
    """Closed round outline: a faceted n-gon in Line, a smooth rounded shape in Rounded."""
    ry = rx if ry is None else ry
    if S.name == "line":
        return poly(_ep(cx, cy, rx, ry, n), closed=True)
    return ellipse(cx, cy, rx, ry)


def _bead(S, x, y, r):
    """Round bead: outlined hexagon in Line, outlined circle in Rounded, solid disc in Filled."""
    return shell(poly(_ep(x, y, r, r, 6), closed=True) if S.name == "line" else circle(x, y, r))


def _mirror_x(pts):
    return [(24 - x, y) for x, y in pts]


# ============================================================================ footwear

@icon("saddle-shoe", CAT, "Low lace-up shoe with a shaded saddle panel across the middle of the upper.",
      tags=["saddle oxford", "two tone shoe", "retro shoe", "school shoe", "footwear", "lace up"],
      aliases=["saddle-oxford"])
def _(S):
    d = poly([(3, 20), (3, 5.5), (7.5, 5.5), (13.5, 10), (19, 11), (21, 13.5), (21, 20)], closed=True, r=S.r)
    return [
        shell(d),
        detail(seg(3, 16.5, 21, 16.5)),
        Part("dot", _band(d, [(8.2, 2), (13, 2), (15.5, 16), (10.7, 16)])),
    ]


@icon("pointe-shoe", CAT, "Ballet pointe shoe standing on its flat toe, with two ribbons crossing above the ankle.",
      tags=["ballet shoe", "ballet", "dance", "ballerina", "toe shoe", "ribbon", "footwear"],
      aliases=["ballet-shoe"])
def _(S):
    return [
        shell(poly([(4.5, 3), (12, 3), (14, 9), (17, 15), (17.5, 21), (11, 21), (9.5, 16), (4.5, 10)], closed=True, r=S.r)),
        detail(seg(11, 16.5, 17.3, 16.5)),
        detail(seg(4.6, 4.5, 13, 8.5)),
        detail(seg(12.3, 4, 4.6, 9)),
    ]


@icon("platform-shoe", CAT, "High-heeled shoe on a very thick platform sole under the toe and a chunky heel.",
      tags=["platform heel", "chunky heel", "flatform", "high heel", "footwear", "disco"],
      aliases=["platform-heel"])
def _(S):
    return [
        shell(poly([(3.5, 3.5), (8, 3.5), (10, 7.5), (15, 8.5), (21, 10.5), (21, 18), (9, 18), (9, 21.5), (3.5, 21.5)],
                   closed=True, r=S.r)),
        detail(seg(3.5, 14, 21, 14)),
    ]


@icon("wedge-heel", CAT, "Shoe standing on a solid wedge that rises from the toe to a tall heel.",
      tags=["wedge", "wedge sandal", "espadrille", "summer shoe", "footwear", "heels"],
      aliases=["wedge-shoe"])
def _(S):
    return [
        shell(poly([(3.5, 4), (8, 4), (10, 8), (15, 9.5), (21, 12.5), (21, 21), (3.5, 21)], closed=True, r=S.r)),
        detail(seg(3.5, 13, 21, 17.5)),
    ]


@icon("gladiator-sandal", CAT, "Flat sandal with many horizontal straps that climb up the shin.",
      tags=["strappy sandal", "lace up sandal", "roman sandal", "summer", "footwear", "straps"],
      aliases=["roman-sandal"])
def _(S):
    return [
        shell(poly([(6, 2.5), (13.5, 2.5), (13.5, 12.5), (20, 15), (21, 16.5), (21, 21), (4, 21), (4, 16), (6, 12)],
                   closed=True, r=S.r)),
        detail(seg(6, 5.5, 13.5, 5.5)), detail(seg(6, 8.75, 13.5, 8.75)), detail(seg(6, 12, 13.5, 12)),
        detail(seg(4, 18, 21, 18)),
    ]


@icon("slide-sandal", CAT, "Open-back slide sandal with one wide band across the top of the foot.",
      tags=["slides", "pool slide", "slip on sandal", "summer", "footwear", "beach"],
      aliases=["slides"])
def _(S):
    rr = "A2 2 0 0 1 " if S.name == "rounded" else ""
    d = ("M3 17H11.5C11.5 12 14 9 17 9.5C19.5 10 20.5 13.5 21 17V19"
         + ("A2 2 0 0 1 19 21H5A2 2 0 0 1 3 19V17Z" if S.name == "rounded" else "V21H3Z"))
    return [shell(d), detail(seg(3, 17, 21, 17))]


@icon("high-top-sneaker", CAT, "Sneaker with a collar that rises above the ankle, laces and a round ankle patch.",
      tags=["high top", "hi top", "basketball shoe", "trainer", "footwear", "sport"],
      aliases=["high-top", "hi-top"])
def _(S):
    return [
        shell(poly([(3, 19.5), (3, 3.5), (11, 3.5), (11, 10), (17, 12.5), (21, 15), (21, 19.5)], closed=True, r=S.r)),
        detail(seg(3, 16, 21, 16)),
        detail(seg(11, 6.5, 8.2, 6.5)), detail(seg(11.4, 9.6, 8.6, 9.6)),
        dot(6.5, 12.6, 1.4),
    ]


@icon("bunny-slipper", CAT, "Fluffy house slipper with two long rabbit ears and eyes on the toe.",
      tags=["rabbit slipper", "animal slipper", "novelty slipper", "cozy", "house shoe", "footwear", "kids"],
      aliases=["rabbit-slipper"])
def _(S):
    body = ("M3 19.5V15.5H9.5C9.5 12.5 12 11 15 11C18.5 11 21 13 21 16.5V19.5Z" if S.name == "line" else
            "M3 18A1.5 1.5 0 0 1 4.5 16.5H9.5C9.5 12.5 12 11 15 11C18.5 11 21 13 21 16.5V18A1.5 1.5 0 0 1 19.5 19.5H4.5A1.5 1.5 0 0 1 3 18Z")
    return [
        shell(body),
        line("M12 11C10.5 7 10.5 3.5 12.5 3.5C14.5 3.5 15 7 14.5 11"),
        line("M17 11C17.5 7 18 3.5 20 3.5C22 3.5 21 7 19.5 11"),
        dot(14, 15, 1.2), dot(18.4, 15, 1.2),
    ]


@icon("baby-bootie", CAT, "Small soft knitted baby shoe with a ribbed cuff and a bow on the toe.",
      tags=["baby shoe", "bootee", "infant", "newborn", "knitted", "nursery", "footwear"],
      aliases=["baby-bootee", "baby-shoe"])
def _(S):
    bow = poly([(16.6, 16.8), (14.2, 15.2), (14.2, 18.4)], closed=True) + poly([(16.6, 16.8), (19, 15.2), (19, 18.4)], closed=True)
    return [
        shell(poly([(4, 20), (4, 5), (11, 5), (11, 11), (17, 12.5), (21, 15), (21, 20)], closed=True, r=S.r)),
        detail(seg(4, 9.5, 11, 9.5)),
        solid(bow),
    ]


@icon("tap-shoe", CAT, "Low-heeled lace-up dance shoe with a metal plate under the toe and another on the heel.",
      tags=["tap dance", "dance shoe", "clogging", "jazz", "metal taps", "theatre", "footwear"],
      aliases=["tap-dance-shoe"])
def _(S):
    return [
        shell(poly([(3, 5.5), (8, 5.5), (12.5, 9.5), (18.5, 10.5), (21, 13), (21, 21), (3, 21)], closed=True, r=S.r)),
        detail(seg(3, 16.5, 21, 16.5)),
        detail(seg(17.3, 12.5, 17.3, 16.5)),
        detail(seg(3, 18.75, 8.5, 18.75)),
        detail(seg(9.6, 7.9, 8.3, 9.9)), detail(seg(12.6, 9.9, 11.5, 11.7)),
    ]


@icon("boot-spur", CAT, "Riding spur with a U-shaped heel band, a short shank and a spiked star wheel.",
      tags=["spur", "cowboy", "rowel", "horse riding", "western", "equestrian", "boot"],
      aliases=["spur"])
def _(S):
    spikes = [line(seg(*polar(17, 12.5, 2.9, a), *polar(17, 12.5, 5.6, a))) for a in range(0, 360, 60)]
    return [
        line(poly([(3.5, 3), (3.5, 12), (6, 17.5), (10.5, 18.5), (15, 15)], r=S.r * 2)),
        dot(17, 12.5, 2.2),
        *spikes,
    ]


@icon("shoelace", CAT, "Shoelace tied in a bow with two loops and two hanging ends with metal tips.",
      tags=["lace", "laces", "bow", "tie shoes", "knot", "string", "footwear"],
      aliases=["shoe-lace", "shoestring"])
def _(S):
    lp = [(11, 10.5), (8.5, 5.5), (5, 3.5), (2.8, 6), (3.5, 10), (7, 11.5)]
    return [
        shell(poly(lp, closed=True, r=S.r)), shell(poly(_mirror_x(lp), closed=True, r=S.r)),
        line("M11.5 11.5C10.5 14 9.5 16 8 18.5"), line("M12.5 11.5C13.5 14 14.5 16 16 18.5"),
        _aglet(9.2, 16.5, 8, 18.8), _aglet(14.8, 16.5, 16, 18.8),
        dot(12, 10.8, 1.9),
    ]


@icon("shoebox", CAT, "Open shoebox with its lid lifted above and the toe of a shoe peeking out.",
      tags=["shoe box", "shoe shopping", "footwear store", "packaging", "new shoes", "unboxing", "retail"],
      aliases=["shoe-box"])
def _(S):
    return [
        shell(rect(3.5, 13.5, 17, 8, min(S.R, 1.5))),
        shell(poly([(3, 7), (17, 3.5), (21, 6.5), (7, 10)], closed=True, r=S.r)),
        line(poly([(8, 13.5), (8, 12), (13, 12), (15, 13.5)], r=S.r)),
    ]


@icon("shoe-last", CAT, "Wooden foot form used by shoemakers, side view, with a socket hole on top of the ankle.",
      tags=["cobbler", "shoemaker", "shoe form", "shoe tree", "last", "bespoke", "cordwainer"],
      aliases=["cobbler-last"])
def _(S):
    return [
        shell(poly([(3.5, 12), (6.5, 4.5), (12, 4.5), (13, 10), (18.5, 11.5), (21, 15), (21, 19.5), (9, 19.5), (3.5, 17)],
                   closed=True, r=S.r)),
        dot(9, 8.5, 1.5),
    ]


@icon("shoe-rack", CAT, "Two-shelf shoe rack with a pair of shoes standing on each shelf.",
      tags=["shoe storage", "shoe shelf", "hallway", "entryway", "organizer", "closet", "footwear"],
      aliases=["shoe-shelf"])
def _(S):
    def shoe(x, y):
        return Part("dot", poly([(x, y + 4), (x, y), (x + 2.6, y), (x + 5, y + 2), (x + 7, y + 2.5), (x + 7, y + 4)], closed=True))
    return [
        line(seg(3.5, 3, 3.5, 21.5)), line(seg(20.5, 3, 20.5, 21.5)),
        line(seg(3.5, 3.5, 20.5, 3.5)),
        line(seg(3.5, 12.5, 20.5, 12.5)), line(seg(3.5, 21, 20.5, 21)),
        shoe(5.5, 7.8), shoe(13, 7.8), shoe(5.5, 16.3), shoe(13, 16.3),
    ]


@icon("boot-jack", CAT, "Flat wooden board with a U-shaped notch cut into one end, used to pull off boots.",
      tags=["boot puller", "boot remover", "cowboy boots", "riding boots", "entryway", "footwear tool", "notch"],
      aliases=["boot-puller"])
def _(S):
    if S.name == "line":
        d = "M3 6H21V9H18A3 3 0 0 0 18 15H21V18H3Z"
    else:
        d = "M5 6H19A2 2 0 0 1 21 8V9H18A3 3 0 0 0 18 15H21V16A2 2 0 0 1 19 18H5A2 2 0 0 1 3 16V8A2 2 0 0 1 5 6Z"
    return [shell(d), dot(8, 12, 1.4)]


@icon("stockings", CAT, "Long sheer stocking with a scalloped lace band at the top and a seam running down the back.",
      tags=["thigh highs", "hosiery", "nylons", "lace top", "pantyhose", "lingerie", "legwear"],
      aliases=["hosiery"])
def _(S):
    d = poly([(7.5, 3), (15.5, 3), (15.5, 14.5), (21, 17), (21, 21), (7.5, 21)], closed=True, r=S.r)
    return [
        shell(d),
        Part("dot", _band(d, [(5, 1), (18, 1), (18, 6), (15.5, 8.2), (13.5, 6), (11.5, 8.2), (9.5, 6), (7.5, 8.2), (5, 6)])),
        detail(seg(10.5, 11.5, 10.5, 21)),
    ]


@icon("knee-high-socks", CAT, "Tall sock reaching the knee with two solid stripes around the ribbed top.",
      tags=["knee socks", "tall socks", "school socks", "sports socks", "striped socks", "football socks", "hosiery"],
      aliases=["knee-socks"])
def _(S):
    d = poly([(6.5, 3), (16, 3), (16, 14), (21, 17), (21, 21), (6.5, 21)], closed=True, r=S.r)
    return [
        shell(d),
        Part("dot", _band(d, [(4, 6.2), (18, 6.2), (18, 8.2), (4, 8.2)])),
        Part("dot", _band(d, [(4, 10.2), (18, 10.2), (18, 12.2), (4, 12.2)])),
    ]


@icon("leg-warmers", CAT, "Scrunched ribbed knit tube bunched into folds, worn around the lower leg.",
      tags=["legwarmers", "dance wear", "knitwear", "ballet", "80s fashion", "ribbed", "winter"],
      aliases=["legwarmers"])
def _(S):
    d = poly([(7, 3), (17, 3), (19, 6.5), (17, 10), (19, 13.5), (17, 17), (18.5, 21), (5.5, 21), (7, 17), (5, 13.5),
              (7, 10), (5, 6.5)], closed=True, r=S.r)
    return [
        shell(d),
        detail(seg(7, 6.8, 17, 6.8)), detail(seg(7, 13.6, 17, 13.6)),
    ]


@icon("crossbody-bag", CAT, "Small flap bag hanging low, with a long strap sweeping up diagonally to the shoulder.",
      tags=["sling bag", "shoulder bag", "purse", "handbag", "messenger", "strap", "accessory"],
      aliases=["sling-bag"])
def _(S):
    return [
        shell(rect(5, 13, 14, 8, min(S.R, 2.5))),
        detail(poly([(5, 14), (12, 18), (19, 14)], r=S.r)),
        line("M7.5 13C7.5 6.5 9.5 3 13 3C16.5 3 16.5 8 16.5 13"),
    ]


@icon("messenger-bag", CAT, "Wide satchel with a large curved front flap, two buckles and a long shoulder strap.",
      tags=["satchel", "courier bag", "laptop bag", "school bag", "shoulder strap", "work bag", "buckles"],
      aliases=["satchel"])
def _(S):
    return [
        shell(rect(3, 8.5, 18, 12.5, min(S.R, 3))),
        detail("M3 13.5C7 17.5 17 17.5 21 13.5"),
        dot(8, 16, 1.4), dot(16, 16, 1.4),
        line("M6.5 8.5C7 2.5 17 2.5 17.5 8.5"),
    ]


@icon("duffel-bag", CAT, "Barrel-shaped sports bag with a zipper along the top, end panels and two handles.",
      tags=["gym bag", "sports bag", "holdall", "weekend bag", "travel bag", "luggage", "carryall"],
      aliases=["gym-bag", "holdall"])
def _(S):
    return [
        shell(rect(2.5, 9.5, 19, 11, min(S.R + 1, 4.5))),
        detail(seg(2.5, 13.5, 21.5, 13.5)),
        detail(seg(6.5, 13.5, 6.5, 20.5)), detail(seg(17.5, 13.5, 17.5, 20.5)),
        line("M7.5 9.5C7.5 4 10 4 11.5 4"), line("M16.5 9.5C16.5 4 14 4 12.5 4"),
    ]


@icon("fanny-pack", CAT, "Small domed zip pouch on a waist strap with a buckle.",
      tags=["belt bag", "waist pack", "bum bag", "hip bag", "hiking", "festival", "travel"],
      aliases=["belt-bag", "bum-bag"])
def _(S):
    return [
        shell("M5 18.5V14C5 9.5 8 7.5 12 7.5C16 7.5 19 9.5 19 14V18.5Z"),
        detail(seg(5, 13.5, 19, 13.5)),
        dot(9, 16.3, 1.2),
        line(seg(2, 15.5, 5, 15.5)), line(seg(19, 15.5, 22, 15.5)),
        Part("dot", rect(19.6, 13.3, 2.4, 4.4, 0.4)),
    ]


@icon("drawstring-bag", CAT, "Soft round pouch gathered at the top by a cord that ends in two tassels.",
      tags=["pouch", "cinch bag", "gym sack", "gift bag", "sack", "string bag", "cord"],
      aliases=["cinch-bag"])
def _(S):
    return [
        shell("M9 6.5H15C15 9 20 11 20 16C20 20 17 21 12 21C7 21 4 20 4 16C4 11 9 9 9 6.5Z"),
        detail(seg(9, 9, 15, 9)),
        line("M15 9C16.5 7.5 18 6 19 3.5"), dot(19.3, 3.3, 1.3),
        line("M9 9C7.5 7.5 6 6 5 3.5"), dot(4.7, 3.3, 1.3),
    ]


@icon("bucket-bag", CAT, "Tall round bag with a cinched top and a single shoulder strap.",
      tags=["bucket purse", "shoulder bag", "handbag", "drawstring purse", "cylinder bag", "strap", "accessory"],
      aliases=["bucket-purse"])
def _(S):
    return [
        shell("M6 8.5H18L19.5 20.5H4.5Z" if S.name == "line" else "M6 8.5H18L19.5 19C19.5 20.5 16.5 21.5 12 21.5C7.5 21.5 4.5 20.5 4.5 19Z"),
        detail(seg(5.6, 12, 18.4, 12)),
        line("M7.5 8.5C7.5 2 16.5 2 16.5 8.5"),
    ]


@icon("doctor-bag", CAT, "Wide leather bag with a hinged frame on top, a centre clasp and one handle.",
      tags=["gladstone bag", "medical bag", "physician bag", "house call", "vintage bag", "leather", "clasp"],
      aliases=["gladstone-bag"])
def _(S):
    return [
        shell("M3 12L6.5 8.5H17.5L21 12V21H3Z" if S.name == "line" else
              "M3 12C3 9.5 6 8.5 12 8.5C18 8.5 21 9.5 21 12V19A2 2 0 0 1 19 21H5A2 2 0 0 1 3 19Z"),
        detail(seg(3, 12.5, 21, 12.5)),
        Part("dot", rect(10.4, 11.5, 3.2, 4.5, 0.5)),
        line("M8 8.5C8 3 16 3 16 8.5"),
    ]


@icon("money-clip", CAT, "Banknote held in a folded metal clip that wraps around its lower half.",
      tags=["bill clip", "cash clip", "wallet", "cash", "money holder", "men accessory", "banknotes"],
      aliases=["cash-clip"])
def _(S):
    return [
        shell(rect(8, 7, 13, 10, min(S.R, 2))),
        dot(16.5, 12, 1.7),
        line("M13 4H5.5Q3.5 4 3.5 6V18Q3.5 20 5.5 20H13"),
    ]


@icon("steamer-trunk", CAT, "Large travel trunk with a domed lid, vertical wooden slats and a front latch.",
      tags=["travel trunk", "vintage luggage", "chest", "suitcase", "old fashioned", "voyage", "baggage"],
      aliases=["travel-trunk"])
def _(S):
    return [
        shell("M3 21V10L6.5 4H17.5L21 10V21Z" if S.name == "line" else "M3 21V11C3 6.5 7 4 12 4C17 4 21 6.5 21 11V21Z"),
        detail(seg(3, 12.5, 21, 12.5)),
        detail(seg(8, 4.6, 8, 21)), detail(seg(16, 4.6, 16, 21)),
        Part("dot", rect(10.6, 11, 2.8, 4, 0.5)),
    ]


@icon("saddle-bag", CAT, "Half-moon bag with a curved flap and a buckle, hung from a strap.",
      tags=["half moon bag", "crescent bag", "shoulder bag", "horse riding", "buckle", "handbag", "strap"],
      aliases=["half-moon-bag"])
def _(S):
    return [
        shell("M3 10H21L19.5 16L15 21H9L4.5 16Z" if S.name == "line" else "M3 10H21C21 16.5 17 21 12 21C7 21 3 16.5 3 10Z"),
        detail("M3.4 13C7 17 17 17 20.6 13"),
        dot(12, 17.2, 1.3),
        line("M6.5 10C6.5 2.5 17.5 2.5 17.5 10"),
    ]


@icon("straw-bag", CAT, "Woven straw basket bag with a criss-cross weave and two short handles.",
      tags=["basket bag", "wicker", "beach bag", "summer bag", "woven", "raffia", "market bag"],
      aliases=["basket-bag"])
def _(S):
    d = "M4 10H20L18.5 19C18.3 20.5 16 21 12 21C8 21 5.7 20.5 5.5 19Z" if S.name == "line" else \
        "M5 10H19C19.8 10 20.3 10.5 20.2 11.3L18.8 19.2C18.5 20.5 16 21 12 21C8 21 5.5 20.5 5.2 19.2L3.8 11.3C3.7 10.5 4.2 10 5 10Z"
    return [
        shell(d),
        Part("dot", _lattice(d, step=6.5, w=1.4)),
        line("M6.5 10V7A2 2 0 0 1 10.5 7V10"), line("M13.5 10V7A2 2 0 0 1 17.5 7V10"),
    ]


@icon("net-bag", CAT, "String shopping bag made of a diamond mesh with two loop handles.",
      tags=["string bag", "mesh bag", "avocado bag", "reusable bag", "shopping bag", "market", "eco"],
      aliases=["string-bag"])
def _(S):
    d = ("M5 9H19L20.5 16L17.5 21H6.5L3.5 16Z" if S.name == "line" else
         "M5 9H19C20 13 20.5 17 18 20C16.5 21.5 7.5 21.5 6 20C3.5 17 4 13 5 9Z")
    return [
        shell(d),
        Part("dot", _lattice(d, step=5.6, w=1.3)),
        line("M8 9C8 3 11 3 11 9"), line("M13 9C13 3 16 3 16 9"),
    ]


# ============================================================================ jewellery

@icon("hoop-earring", CAT, "Large round hoop earring hanging from a small stud.",
      tags=["hoops", "earring", "jewelry", "ear", "gold hoop", "piercing", "accessory"],
      aliases=["hoops"])
def _(S):
    return [
        dot(12, 3.6, 1.7),
        line(seg(12, 5, 12, 7.5)),
        line(_ring(S, 12, 14.5, 7, 7, 10)),
    ]


@icon("stud-earring", CAT, "Round gem stud earring with a straight post and a butterfly back.",
      tags=["stud", "earring", "jewelry", "gem", "diamond", "post", "butterfly back", "ear"],
      aliases=["studs"])
def _(S):
    return [
        shell(poly(_ep(7.5, 12, 5, 5, 6), closed=True, r=S.r)),
        dot(7.5, 12, 1.4),
        line(seg(12.5, 12, 17.5, 12)),
        solid(rect(17, 8.5, 3.8, 7, 1.4)),
    ]


@icon("chandelier-earring", CAT, "Dangling earring that widens into tiers of drops like a chandelier.",
      tags=["drop earring", "dangle", "earring", "jewelry", "statement", "evening", "ear"],
      aliases=["dangle-earring"])
def _(S):
    return [
        dot(12, 3, 1.5),
        shell(poly([(12, 6), (18, 13), (6, 13)], closed=True, r=S.r)),
        line(seg(6, 13, 6, 17)), line(seg(12, 13, 12, 18)), line(seg(18, 13, 18, 17)),
        dot(6, 19, 1.7), dot(12, 20, 1.7), dot(18, 19, 1.7),
    ]


@icon("ear-cuff", CAT, "Curved metal band hugging the upper rim of an ear outline.",
      tags=["ear wrap", "cartilage", "piercing", "earring", "jewelry", "ear", "no piercing"],
      aliases=["ear-wrap"])
def _(S):
    ear = ("M7.5 11C7.5 8 9.5 6 12.5 6C15.5 6 17.5 8 17.5 11C17.5 13.8 16 14.8 15 16.3C14 17.8 14 19.3 12.6 20.3"
           "C11.3 21.2 9 21 8 19.6")
    return [
        line(ear),
        shell("M5.5 11C5.5 6 8.5 2.8 12.5 2.8C16.5 2.8 19.5 6 19.5 11L16 11C16 8.5 14.6 6.5 12.5 6.5C10.4 6.5 9 8.5 9 11Z"
              if S.name == "rounded" else "M5.5 11L7 5L12.5 2.8L18 5L19.5 11L16 11L15 7.5L12.5 6.5L10 7.5L9 11Z"),
    ]


@icon("nose-ring", CAT, "Side view of a nose with a small ring through the nostril.",
      tags=["nose piercing", "nostril", "septum", "piercing", "body jewelry", "ring", "face"],
      aliases=["nose-piercing"])
def _(S):
    return [
        line("M11 3C11 8 9.5 11.5 6.5 15C5.5 16.5 6.5 18.5 8.5 18.5H13C15.5 18.5 16.3 15.6 14 14"),
        line(_ring(S, 15.8, 16.3, 3.6, 3.6, 8)),
    ]


def _oval(S, cx, cy, rx, ry):
    return poly(_ep(cx, cy, rx, ry, 12), closed=True, r=S.r * 2.2) if S.name == "line" else ellipse(cx, cy, rx, ry)


@icon("brooch", CAT, "Oval ornamental pin with a centre stone ringed by small beads and a pin tip below.",
      tags=["pin", "corsage", "jewelry", "lapel", "vintage", "gemstone", "accessory"],
      aliases=["corsage-pin"])
def _(S):
    return [
        shell(_oval(S, 12, 11.5, 9, 7)),
        dot(12, 11.5, 2.4),
        dot(12, 7.2, 1), dot(12, 15.8, 1), dot(6.8, 11.5, 1), dot(17.2, 11.5, 1),
        line(seg(10, 19.5, 14, 19.5)),
        line(seg(12, 18.5, 12, 21.5)),
    ]


@icon("cameo-brooch", CAT, "Oval brooch with the raised profile of a head inside a double frame.",
      tags=["cameo", "portrait pin", "victorian", "antique", "profile", "jewelry", "vintage"])
def _(S):
    return [
        shell(_oval(S, 12, 12, 8.5, 9.5)),
        detail(_oval(S, 12, 12, 5.2, 6.5)),
        Part("dot", circle(11.6, 9.6, 2.1)),
        Part("dot", poly([(13.4, 9.6), (15.2, 10.6), (13.4, 11.4)], closed=True)),
        Part("dot", poly([(8.8, 16.3), (9.6, 13), (13.6, 13), (14.4, 16.3)], closed=True)),
    ]


@icon("pearl-necklace", CAT, "Hanging strand of round pearls of equal size with a small clasp at the top.",
      tags=["pearls", "necklace", "jewelry", "strand", "wedding", "formal", "beads"],
      aliases=["pearls"])
def _(S):
    parts = [_bead(S, *polar(12, 12.5, 8.8, -50 + i * 35), 1.55) for i in range(9)]
    parts.append(line(poly([polar(12, 12.5, 8.8, -50), (12, 3.4)])))
    parts.append(line(poly([polar(12, 12.5, 8.8, 230), (12, 3.4)])))
    parts.append(dot(12, 3.2, 1.5))
    return parts


@icon("torc", CAT, "Rigid open neck ring of twisted metal with a round knob at each end.",
      tags=["torque", "neck ring", "celtic", "viking", "ancient jewelry", "collar", "bronze age"],
      aliases=["neck-torc"])
def _(S):
    a0, a1 = -62, 242
    if S.name == "line":
        pts = [polar(12, 13, 8.3, a0 + (a1 - a0) * i / 6) for i in range(7)]
        ring = line(poly(pts))
    else:
        ring = line(arc(12, 13, 8.3, a0, a1))
    return [
        ring,
        dot(*polar(12, 13, 8.3, a0), 2.3), dot(*polar(12, 13, 8.3, a1), 2.3),
    ]


@icon("beaded-bracelet", CAT, "Ring of round beads threaded side by side on an elastic band.",
      tags=["bead bracelet", "stretch bracelet", "jewelry", "wrist", "gemstone beads", "diy", "craft"],
      aliases=["bead-bracelet"])
def _(S):
    return [_bead(S, *polar(12, 12, 8.4, k * 360 / 7 - 90), 2.15) for k in range(7)]


@icon("friendship-bracelet", CAT, "Woven thread bracelet with a chevron pattern and loose knotted ends at both sides.",
      tags=["thread bracelet", "embroidery floss", "braided", "summer camp", "handmade", "craft", "woven"],
      aliases=["thread-bracelet"])
def _(S):
    return [
        shell(rect(6.5, 6.5, 11, 11, min(S.R, 2))),
        detail(poly([(9, 9), (11.5, 12), (9, 15)], r=S.r * 0.6)),
        detail(poly([(13.5, 9), (16, 12), (13.5, 15)], r=S.r * 0.6)) if False else detail(poly([(12.5, 9), (15, 12), (12.5, 15)], r=S.r * 0.6)),
        line(poly([(6.5, 10), (2.8, 8.2)])), line(poly([(6.5, 14), (2.8, 15.8)])),
        line(poly([(17.5, 10), (21.2, 8.2)])), line(poly([(17.5, 14), (21.2, 15.8)])),
    ]


@icon("hand-chain", CAT, "Finger ring joined by a short chain to a bracelet band below it, as worn across the back of the hand.",
      tags=["hand jewelry", "slave bracelet", "bracelet ring chain", "boho", "bridal", "ring", "hand harness"],
      aliases=["hand-harness"])
def _(S):
    return [
        shell(circle(12, 5.5, 3) if S.name == "rounded" else poly(_ep(12, 5.5, 3.2, 3.2, 6), closed=True)),
        dot(12, 11.2, 1), dot(12, 14.2, 1),
        shell(ellipse(12, 19, 8.5, 2.6) if S.name == "rounded" else poly(_ep(12, 19, 8.5, 2.8, 8), closed=True)),
    ]


@icon("anklet", CAT, "Leg and foot from the side with a thin chain around the ankle and a charm hanging from it.",
      tags=["ankle bracelet", "ankle chain", "foot jewelry", "beach", "summer", "charm", "chain"],
      aliases=["ankle-bracelet"])
def _(S):
    leg = poly([(8, 2.5), (8, 14.5), (5.5, 18.5), (5.5, 21), (19, 21), (21, 19), (21, 17.5), (16, 15), (16, 2.5)],
               r=S.r * 1.3)
    return [
        line(leg),
        detail("M8 9.5Q12 13 16 9.5"),
        dot(12, 14.2, 1.3),
    ]


@icon("cufflinks", CAT, "Pair of square cufflinks, each with a gem in the face and a post ending in a short toggle bar.",
      tags=["cuff links", "shirt accessory", "formal wear", "groom gift", "tuxedo", "french cuff", "menswear"],
      aliases=["cuff-links"])
def _(S):
    out = []
    for y in (6.5, 17.5):
        out += [
            shell(rect(3, y - 3.5, 7, 7, min(S.R, 1.5))),
            dot(6.5, y, 1.1),
            line(seg(10, y, 17.5, y)),
            line(seg(17.5, y - 3, 17.5, y + 3)),
        ]
    return out


def _tie_filled():
    body = "M10.5 2.5H13.5L13 6.5L16 19.5L12 22L8 19.5L11 6.5Z"
    bar = P(rect(5.5, 10.6, 13, 2.8, 1.2))
    halo = P(rect(4.5, 9.6, 15, 4.8, 1.8))
    base = U(P(body), ST(body, 2))
    return U(D(base, halo), bar)


@icon("tie-clip", CAT, "Necktie with a horizontal metal bar clipped across it to hold it flat.",
      tags=["tie bar", "tie pin", "necktie", "menswear", "formal", "suit accessory", "clasp"],
      aliases=["tie-bar", "tie-pin"], filled=_tie_filled)
def _(S):
    return [
        shell(poly([(10.5, 2.5), (13.5, 2.5), (13, 6.5), (16, 19.5), (12, 22), (8, 19.5), (11, 6.5)], closed=True, r=S.r * 0.6)),
        shell(rect(5.5, 10.6, 13, 2.8, 1.2)),
    ]


@icon("lapel-pin", CAT, "Round enamel pin with an emblem in the middle and a butterfly clutch on its post.",
      tags=["enamel pin", "pin badge", "badge", "flair", "collectible", "butterfly clutch", "jacket pin"],
)
def _(S):
    return [
        shell(poly(_ep(9, 9, 5.8, 5.8, 8), closed=True, r=S.r * 2) if S.name == "line" else circle(9, 9, 5.8)),
        dot(9, 9, 1.7),
        line(seg(13, 13, 15.5, 15.5)),
        solid(poly([(14, 15), (17.8, 17.8), (15, 21)], closed=True)),
        solid(poly([(20.5, 14.2), (17.8, 17.8), (21.4, 19.2)], closed=True)),
    ]


@icon("button-badge", CAT, "Round pin-back badge with a shine mark on its face and the curled pin showing behind the lower edge.",
      tags=["pin button", "pinback", "campaign button", "flair", "badge", "merch", "round badge"],
      aliases=["pinback-button"])
def _(S):
    return [
        shell(poly(_ep(11.5, 11, 8.3, 8.3, 8), closed=True, r=S.r * 2) if S.name == "line" else circle(11.5, 11, 8.3)),
        detail(arc(11.5, 11, 4.3, 200, 265)),
        line("M14 20.6H19.2Q21.4 20.6 21.4 18.4"),
    ]


@icon("signet-ring", CAT, "Ring with a flat oval face bearing an engraved letter T.",
      tags=["family crest ring", "class ring", "pinky ring", "monogram", "seal ring", "initial", "jewelry"],
      aliases=["pinky-ring"])
def _(S):
    return [
        shell(poly(_ep(12, 6.8, 5.8, 4.5, 8), closed=True, r=S.r * 2) if S.name == "line" else ellipse(12, 6.8, 5.8, 4.5)),
        Part("dot", rect(9.7, 4.6, 4.6, 1.8)),
        Part("dot", rect(11.1, 6.2, 1.8, 3)),
        line(arc(12, 16, 5.8, -50, 230)) if S.name == "rounded" else line(poly([polar(12, 16, 5.8, -50 + i * 280 / 5) for i in range(6)])),
    ]


_HEART = "M12 18.5C6 14.5 5 11.5 5 10C5 8 6.5 7 8.3 7C10 7 11.3 8 12 9.3C12.7 8 14 7 15.7 7C17.5 7 19 8 19 10C19 11.5 18 14.5 12 18.5Z"


@icon("claddagh-ring", CAT, "Ring showing a heart topped with a crown, cradled in the band below.",
      tags=["irish ring", "friendship ring", "heart and crown", "love loyalty friendship", "celtic", "promise ring", "jewelry"],
      aliases=["irish-ring"])
def _(S):
    heart = ("M12 18C6.5 14.5 6 12 6 10.6C6 9 7.2 8 8.6 8C10 8 11.3 8.8 12 10C12.7 8.8 14 8 15.4 8C16.8 8 18 9 18 10.6C18 12 17.5 14.5 12 18Z")
    return [
        shell(heart if S.name == "rounded" else poly([(12, 18.5), (5.5, 11.5), (7, 8), (10, 8), (12, 10), (14, 8), (17, 8), (18.5, 11.5)],
                                                    closed=True)),
        detail(poly([(8.5, 5.5), (8.5, 2.8), (10.3, 4.4), (12, 2.4), (13.7, 4.4), (15.5, 2.8), (15.5, 5.5)], r=S.r * 0.3)),
        line(arc(12, 11, 10.3, 20, 160)),
    ]


@icon("dog-tags", CAT, "Two metal identity tags with punched text lines, hanging side by side on a chain.",
      tags=["military tags", "id tags", "army", "soldier", "necklace", "identification", "pet tag"],
      aliases=["military-tags"])
def _(S):
    return [
        line("M6 2.5L11.5 8.5L17 2.5"),
        shell(rect(6, 9, 9, 12, min(S.R, 3))),
        line("M17 11V9.5Q17 8.5 16 8.5"),
        detail(seg(8.5, 14.5, 12.5, 14.5)), detail(seg(8.5, 17.5, 12.5, 17.5)),
        line("M18 11V19.5Q18 21 16.5 21H15"),
    ]


@icon("jewelry-box", CAT, "Open jewelry box with the lid raised behind it, a mirror on the lid and a ring in the tray.",
      tags=["jewellery box", "trinket box", "vanity", "keepsake", "dresser", "ring tray", "gifts"],
      aliases=["jewellery-box", "trinket-box"])
def _(S):
    return [
        shell(poly([(4, 2.5), (20, 2.5), (18.5, 10), (5.5, 10)], closed=True, r=S.r * 0.8)),
        Part("dot", ellipse(12, 6.2, 3.4, 1.6)),
        shell(rect(3, 12, 18, 9, min(S.R, 2.5))),
        detail(seg(9.5, 12, 9.5, 21)),
        detail(poly(_ep(15.5, 16.5, 2.8, 2.8, 8), closed=True)) if S.name == "line" else detail(circle(15.5, 16.5, 2.8)),
    ]


@icon("ring-box", CAT, "Small open ring box with its lid raised and a ring with a gem standing in the slot.",
      tags=["engagement ring box", "proposal", "wedding ring", "velvet box", "propose", "marriage", "jewelry gift"],
      aliases=["proposal-box"])
def _(S):
    return [
        shell(rect(3, 15, 18, 6.5, min(S.R, 2.5))),
        line(poly([(5, 15), (6.3, 2.8), (17.7, 2.8), (19, 15)], r=S.r)),
        shell(poly(_ep(12, 11.3, 2.7, 2.7, 8), closed=True) if S.name == "line" else circle(12, 11.3, 2.7)),
        solid(poly([(12, 4.6), (14, 6.6), (12, 8.6), (10, 6.6)], closed=True)),
    ]


@icon("jewelers-loupe", CAT, "Small round magnifier in a double-rimmed metal housing with a short swing arm, used to inspect gems.",
      tags=["jeweller loupe", "magnifying lens", "gem inspection", "diamond grading", "watchmaker", "eyepiece", "inspect"],
      aliases=["jewellers-loupe", "gem-loupe"])
def _(S):
    return [
        shell(_ring(S, 9.5, 12, 7.2, 7.2, 8)),
        detail(_ring(S, 9.5, 12, 3.4, 3.4, 6)),
        shell(rect(16.5, 9.8, 5.2, 4.4, min(S.R, 1.5))),
    ]


# ============================================================================ gemstones

@icon("emerald-cut-gem", CAT, "Rectangular gemstone with clipped corners and stepped facets forming nested frames.",
      tags=["emerald cut", "step cut", "gemstone", "jewel", "diamond", "precious stone", "jewelry"])
def _(S):
    if S.name == "line":
        outer = poly([(7.5, 2.5), (16.5, 2.5), (20, 6), (20, 18), (16.5, 21.5), (7.5, 21.5), (4, 18), (4, 6)], closed=True)
        inner = poly([(10, 8), (14, 8), (15.5, 9.5), (15.5, 14.5), (14, 16), (10, 16), (8.5, 14.5), (8.5, 9.5)], closed=True)
    else:
        outer = rect(4, 2.5, 16, 19, 4.5)
        inner = rect(8.5, 8, 7, 8, 2)
    return [shell(outer), detail(inner)]


@icon("pear-cut-gem", CAT, "Teardrop-shaped gemstone with a pointed tip, a small table and facet lines.",
      tags=["pear cut", "teardrop gem", "gemstone", "jewel", "diamond", "precious stone", "jewelry"],
      aliases=["teardrop-gem"])
def _(S):
    d = ("M12 2.5C12 2.5 5 9.5 5 15A7 7 0 0 0 19 15C19 9.5 12 2.5 12 2.5Z" if S.name == "line" else
         "M11.1 4C11.6 3.3 12.4 3.3 12.9 4C15 6.5 19 10.5 19 15A7 7 0 0 1 5 15C5 10.5 9 6.5 11.1 4Z")
    return [
        shell(d),
        detail("M12 9.5C12 9.5 9 12.5 9 15A3 3 0 0 0 15 15C15 12.5 12 9.5 12 9.5Z" if S.name == "line" else
               "M11.4 10.4C11.7 10 12.3 10 12.6 10.4C13.8 11.8 15 13.3 15 15A3 3 0 0 1 9 15C9 13.3 10.2 11.8 11.4 10.4Z"),
        detail(seg(12, 3.5, 12, 9.5)),
        detail(seg(7.2, 19.4, 9.6, 17.3)), detail(seg(16.8, 19.4, 14.4, 17.3)),
    ]


@icon("marquise-cut-gem", CAT, "Elongated boat-shaped gemstone pointed at both ends, with a central table and facet lines.",
      tags=["marquise cut", "navette", "boat shape gem", "gemstone", "jewel", "diamond", "jewelry"],
      aliases=["navette-gem"])
def _(S):
    d = ("M12 2.5L18.5 12L12 21.5L5.5 12Z" if S.name == "line" else
         "M12 2.5C17 7 17.5 16 12 21.5C6.5 16 7 7 12 2.5Z")
    return [
        shell(d),
        detail("M12 8.5L14.3 12L12 15.5L9.7 12Z" if S.name == "line" else "M12 8.5C14.2 10 14.2 14 12 15.5C9.8 14 9.8 10 12 8.5Z"),
        detail(seg(12, 3.5, 12, 8.5)), detail(seg(12, 15.5, 12, 20.5)),
    ]


@icon("princess-cut-gem", CAT, "Square gemstone seen from above with facet lines running from each corner to a small square table.",
      tags=["princess cut", "square cut", "gemstone", "jewel", "diamond", "engagement stone", "jewelry"])
def _(S):
    return [
        shell(rect(3.5, 3.5, 17, 17, min(S.R, 2.5))),
        detail(rect(8.5, 8.5, 7, 7, min(S.R, 1))),
        detail(seg(3.5, 3.5, 8.5, 8.5)), detail(seg(20.5, 3.5, 15.5, 8.5)),
        detail(seg(3.5, 20.5, 8.5, 15.5)), detail(seg(20.5, 20.5, 15.5, 15.5)),
    ]


@icon("trillion-cut-gem", CAT, "Triangular gemstone with gently curved sides, an inner triangle and corner facet lines.",
      tags=["trillion cut", "triangle gem", "trilliant", "gemstone", "jewel", "diamond", "jewelry"],
      aliases=["trilliant-gem"])
def _(S):
    d = ("M12 3L21 20L3 20Z" if S.name == "line" else "M12 3Q17.5 9.5 20.6 19.4Q12 22 3.4 19.4Q6.5 9.5 12 3Z")
    return [
        shell(d),
        detail("M12 10L16 16.5H8Z" if S.name == "line" else "M12 10.2L15.6 16.3Q12 17.6 8.4 16.3Z"),
        detail(seg(12, 3.5, 12, 10)), detail(seg(20.5, 19.5, 16, 16.5)), detail(seg(3.5, 19.5, 8, 16.5)),
    ]


@icon("oval-cut-gem", CAT, "Oval gemstone seen from above with a ring of radiating facets around the central table.",
      tags=["oval cut", "oval gem", "gemstone", "jewel", "diamond", "precious stone", "jewelry"])
def _(S):
    rays = [detail(seg(12 + 3.4 * math.cos(math.radians(a)), 12 + 4.6 * math.sin(math.radians(a)),
                       12 + 8.3 * math.cos(math.radians(a)), 12 + 9.5 * math.sin(math.radians(a)))) for a in (30, 90, 150, 210, 270, 330)]
    return [
        shell(_ring(S, 12, 12, 9, 9, 8) if False else (poly(_ep(12, 12, 8.3, 9.5, 10), closed=True) if S.name == "line" else ellipse(12, 12, 8.3, 9.5))),
        detail(poly(_ep(12, 12, 3.4, 4.6, 6), closed=True) if S.name == "line" else ellipse(12, 12, 3.4, 4.6)),
        *rays,
    ]


# ============================================================================ watches

@icon("pocket-watch", CAT, "Round pocket watch with a crown and ring at the top and a chain curving away from it.",
      tags=["fob watch", "chain watch", "antique", "vintage", "timepiece", "clock", "gentleman"])
def _(S):
    return [
        shell(_ring(S, 12, 15.3, 6.5, 6.5, 8)),
        shell(circle(12, 4.6, 1.8) if S.name == "rounded" else poly(_ep(12, 4.6, 1.9, 1.9, 6), closed=True)),
        detail(poly([(12, 11.8), (12, 15.3), (14.6, 15.3)], r=S.r * 0.6)),
        line("M13.9 4.6C17.6 4.6 20.6 6.3 21 10.5"),
    ]


@icon("chronograph-watch", CAT, "Round wristwatch face with three small subdials, a crown and two pushers on the right side.",
      tags=["chrono watch", "stopwatch watch", "wristwatch", "timepiece", "luxury watch", "racing watch", "subdials"],
      aliases=["chrono-watch"])
def _(S):
    return [
        shell(_ring(S, 10.5, 12, 7.5, 7.5, 8)),
        dot(10.5, 7.9, 1.25), dot(6.9, 13.2, 1.25), dot(14.1, 13.2, 1.25),
        line(seg(10.5, 12, 12.8, 13.3)),
        solid(rect(17, 4.8, 3.6, 2.4, 0.6)), solid(rect(17, 16.8, 3.6, 2.4, 0.6)),
        solid(rect(18.4, 10.8, 3, 2.4, 0.6)),
    ]


@icon("watch-strap", CAT, "Curved leather watch strap with a row of holes and a buckle at one end.",
      tags=["watch band", "wristband", "leather strap", "buckle strap", "watch repair", "replacement band", "holes"],
      aliases=["watch-band"])
def _(S):
    cx, cy, ro, ri = 12, 19, 10, 4.7
    a0, a1 = 200, 350
    p0, p1 = polar(cx, cy, ro, a0), polar(cx, cy, ro, a1)
    q0, q1 = polar(cx, cy, ri, a0), polar(cx, cy, ri, a1)
    if S.name == "line":
        d = poly([polar(cx, cy, ro, a) for a in (a0, 230, 260, 290, 320, a1)] + [polar(cx, cy, ri, a) for a in (a1, 320, 290, 260, 230, a0)], closed=True)
    else:
        d = (f"M{fmt(p0[0])} {fmt(p0[1])}A{ro} {ro} 0 0 1 {fmt(p1[0])} {fmt(p1[1])}L{fmt(q1[0])} {fmt(q1[1])}"
             f"A{ri} {ri} 0 0 0 {fmt(q0[0])} {fmt(q0[1])}Z")
    b0, b1 = 184, 200
    buckle = poly([polar(cx, cy, ro + 0.5, b0), polar(cx, cy, ro + 0.5, b1), polar(cx, cy, ri - 0.5, b1), polar(cx, cy, ri - 0.5, b0)],
                  closed=True, r=S.r * 0.4)
    holes = [Part("dot", circle(*polar(cx, cy, (ro + ri) / 2, a), 1.05)) for a in (250, 272, 294, 316)]
    return [shell(d), shell(buckle), *holes]


# ============================================================================ eyewear

def _heart(cx, cy, w):
    """Heart outline centred at (cx, cy) with total width w (height about 0.92 w)."""
    k = w / 10.0
    x = lambda v: fmt(cx + (v - 5) * k)  # noqa: E731
    y = lambda v: fmt(cy + (v - 4.6) * k)  # noqa: E731
    return (f"M{x(5)} {y(9.2)}C{x(0.6)} {y(6.3)} {x(0)} {y(4.3)} {x(0)} {y(3)}C{x(0)} {y(1.3)} {x(1.3)} {y(0)} {x(2.8)} {y(0)}"
            f"C{x(3.8)} {y(0)} {x(4.6)} {y(0.6)} {x(5)} {y(1.4)}C{x(5.4)} {y(0.6)} {x(6.2)} {y(0)} {x(7.2)} {y(0)}"
            f"C{x(8.7)} {y(0)} {x(10)} {y(1.3)} {x(10)} {y(3)}C{x(10)} {y(4.3)} {x(9.4)} {y(6.3)} {x(5)} {y(9.2)}Z")


@icon("aviator-sunglasses", CAT, "Sunglasses with large teardrop lenses that taper toward the nose and a double bridge bar.",
      tags=["aviators", "pilot glasses", "teardrop sunglasses", "shades", "eyewear", "sun", "retro"],
      aliases=["aviators"])
def _(S):
    lens = [(2.8, 9.5), (10.6, 9.5), (10.4, 13), (8, 17.6), (4.8, 17.2), (3, 13)]
    return [
        shell(poly(lens, closed=True, r=S.r * 1.6)),
        shell(poly(_mirror_x(lens), closed=True, r=S.r * 1.6)),
        line(seg(10.6, 11.2, 13.4, 11.2)),
        line("M2.8 9.5C5 6.2 9 5.6 12 6.6C15 5.6 19 6.2 21.2 9.5"),
    ]


@icon("cat-eye-glasses", CAT, "Glasses whose frames sweep up into points at the outer top corners.",
      tags=["cat eye", "retro glasses", "vintage eyewear", "pin up", "fifties", "frames", "spectacles"],
      aliases=["cateye-glasses"])
def _(S):
    lens = [(2.2, 5.5), (10.6, 8), (10.6, 12.6), (8.3, 16.4), (4.6, 16.4), (2.6, 12)]
    return [
        shell(poly(lens, closed=True, r=S.r * 1.3)),
        shell(poly(_mirror_x(lens), closed=True, r=S.r * 1.3)),
        line(seg(10.6, 9.6, 13.4, 9.6)),
    ]


@icon("browline-glasses", CAT, "Glasses with a thick heavy top rim and thin wire rims under the lenses.",
      tags=["half rim", "semi rimless", "retro glasses", "eyewear", "frames", "spectacles"],
)
def _(S):
    lens = poly([(2.5, 8), (10.6, 8), (10.6, 14), (8.4, 17.3), (4.7, 17.3), (2.5, 14)], closed=True, r=S.r * 1.2)
    lens2 = poly(_mirror_x([(2.5, 8), (10.6, 8), (10.6, 14), (8.4, 17.3), (4.7, 17.3), (2.5, 14)]), closed=True, r=S.r * 1.2)
    return [
        shell(lens), shell(lens2),
        Part("dot", _band(lens, [(1, 6), (12, 6), (12, 11.2), (1, 11.2)])),
        Part("dot", _band(lens2, [(12, 6), (23, 6), (23, 11.2), (12, 11.2)])),
        line(seg(10.6, 9.5, 13.4, 9.5)),
    ]


@icon("wraparound-sunglasses", CAT, "Sporty sunglasses with one curved shield lens that wraps across the whole face.",
      tags=["sport sunglasses", "shield sunglasses", "cycling glasses", "visor", "shades", "eyewear", "running"],
      aliases=["shield-sunglasses"])
def _(S):
    d = ("M2 8C2 6.8 3.5 6.5 6 6.5H18C20.5 6.5 22 6.8 22 8V12C22 15.5 19.5 17.5 16 17.5C13.6 17.5 13 15 12 15C11 15 10.4 17.5 8 17.5C4.5 17.5 2 15.5 2 12Z"
         if S.name == "rounded" else
         "M2 7L6 6.5H18L22 7V12L19 17.5H14L12 15L10 17.5H5L2 12Z")
    return [shell(d), detail(seg(5.5, 10.2, 9, 10.2)) if False else detail(poly([(5.5, 11), (8, 9.5)]))]


@icon("heart-sunglasses", CAT, "Novelty sunglasses with heart-shaped lenses joined by a short bridge.",
      tags=["heart shaped glasses", "party glasses", "love", "valentine", "shades", "eyewear", "novelty"],
      aliases=["heart-shaped-glasses"])
def _(S):
    if S.name == "line":
        hp = lambda cx: poly([(cx, 18), (cx - 4.5, 12.5), (cx - 4.5, 9), (cx - 2.6, 7), (cx - 0.9, 7), (cx, 8.6),
                              (cx + 0.9, 7), (cx + 2.6, 7), (cx + 4.5, 9), (cx + 4.5, 12.5)], closed=True)
        l, r_ = hp(7), hp(17)
    else:
        l, r_ = _heart(7.2, 12.3, 9.6), _heart(16.8, 12.3, 9.6)
    return [shell(l), shell(r_), line(seg(11.8, 9.4, 12.2, 9.4)) if False else line(seg(11.5, 9.6, 12.5, 9.6))]


@icon("3d-glasses", CAT, "Cardboard 3D movie glasses with one shaded lens and one clear lens.",
      tags=["anaglyph glasses", "cinema glasses", "movie glasses", "paper glasses", "3d movie", "red blue", "eyewear"],
      aliases=["anaglyph-glasses"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 19, 11, min(S.R, 2.5))),
        Part("dot", rect(4.8, 8.8, 5.6, 6.4, min(S.R, 1))),
        detail(rect(13.6, 8.8, 5.6, 6.4, min(S.R, 1))),
    ]


@icon("monocle", CAT, "Single round eyeglass lens with a thin cord hanging from its rim.",
      tags=["single lens", "eyeglass", "gentleman", "victorian", "magnifier", "eyewear", "cord"],
      aliases=["single-eyeglass"])
def _(S):
    return [
        shell(_ring(S, 10, 9.5, 6.7, 6.7, 8)),
        detail(arc(10, 9.5, 3.3, 200, 265)),
        line("M15.6 6.2C20.5 6.6 21.3 12.5 19 17.5"),
        dot(19, 19.6, 1.4),
    ]


@icon("lorgnette", CAT, "Pair of round lenses on a bridge, held up by a long handle at one side.",
      tags=["opera glasses", "hand held glasses", "face a main", "theatre", "victorian", "eyewear", "handle"],
)
def _(S):
    return [
        shell(_ring(S, 6.3, 7.3, 4.3, 4.3, 8)), shell(_ring(S, 16.2, 7.3, 4.3, 4.3, 8)),
        line(seg(10.6, 7.3, 11.9, 7.3)),
        line(seg(19.2, 10.4, 21, 19.5)),
        dot(21.1, 20.4, 1.4),
    ]


@icon("glasses-chain", CAT, "Pair of glasses with a beaded chain hanging in a loop from both arms.",
      tags=["eyeglass chain", "glasses cord", "spectacle holder", "reading glasses", "lanyard", "beads", "eyewear"],
      aliases=["eyeglass-chain"])
def _(S):
    chain = [(Part('dot', poly(_ep(12 + 9.4 * t, 6.4 + 14.4 * (1 - t * t) ** 0.6, 1.25, 1.25, 4), closed=True)) if S.name == 'line' else dot(12 + 9.4 * t, 6.4 + 14.4 * (1 - t * t) ** 0.6, 1.05)) for t in [(-1 + 2 * i / 10) for i in range(11)]]
    return [
        shell(rect(3.8, 3, 7.4, 5.4, 0.8 if S.name == 'line' else 2.6)), shell(rect(12.8, 3, 7.4, 5.4, 0.8 if S.name == 'line' else 2.6)),
        line(seg(11.2, 4.8, 12.8, 4.8)),
        *chain,
    ]


@icon("ski-goggles", CAT, "Wide snow goggles with one large curved lens and a thick elastic strap.",
      tags=["snow goggles", "snowboard goggles", "winter sports", "skiing", "mountain", "eyewear", "strap"],
)
def _(S):
    return [
        shell(rect(4.5, 6.5, 15, 11, min(S.R + 1, 4))),
        detail(rect(7.5, 9.5, 9, 5, min(S.R, 1.5))) if False else detail(poly([(8, 13.5), (10.5, 10.5)])),
        solid(rect(1.5, 9.5, 3, 5, 0.8)), solid(rect(19.5, 9.5, 3, 5, 0.8)),
    ]


@icon("swim-goggles", CAT, "Two small oval goggle cups joined by a nose bridge, with strap stubs at the sides.",
      tags=["swimming goggles", "pool", "swim gear", "diving", "triathlon", "eyewear", "water sports"],
      aliases=["swimming-goggles"])
def _(S):
    return [
        shell(_ring(S, 7.5, 12.5, 4.7, 4, 8)), shell(_ring(S, 16.5, 12.5, 4.7, 4, 8)),
        line(seg(12.2, 12, 11.8, 12)) if False else line(seg(11.5, 11.5, 12.5, 11.5)),
        line(seg(2.8, 11, 1.8, 7.5)), line(seg(21.2, 11, 22.2, 7.5)),
    ]


@icon("eye-patch", CAT, "Oval patch over one eye held by a strap that runs diagonally across the head.",
      tags=["pirate patch", "eyepatch", "lazy eye", "amblyopia", "pirate", "costume", "medical"],
      aliases=["eyepatch", "pirate-patch"])
def _(S):
    return [
        shell(poly(_ep(11.5, 13, 5.8, 4.6, 10), closed=True, r=S.r * 2.2) if S.name == "line" else ellipse(11.5, 13, 5.8, 4.6)),
        line(seg(2.5, 4, 6.8, 9.4)),
        line(seg(16.2, 16.6, 21.5, 22)) if False else line(seg(16.4, 15.8, 21.5, 20.5)),
    ]


@icon("glasses-case", CAT, "Hard clamshell glasses case opened slightly so the lenses of a pair of glasses show inside.",
      tags=["spectacle case", "eyeglass case", "sunglasses case", "clamshell", "storage", "eyewear", "protective case"],
      aliases=["spectacle-case"])
def _(S):
    return [
        shell(rect(3, 11, 18, 10.5, min(S.R, 3))),
        line(poly([(3.5, 11), (5.5, 3.5), (18.5, 3.5), (20.5, 11)], r=S.r)),
        shell(_ring(S, 8, 16.2, 2.5, 2.5, 8)), shell(_ring(S, 16, 16.2, 2.5, 2.5, 8)),
        line(seg(10.5, 15.5, 13.5, 15.5)) if False else line(seg(10.4, 16.2, 13.6, 16.2)),
    ]


@icon("masquerade-mask", CAT, "Ornate eye mask with pointed upper corners, two eye holes and a stick handle at the side.",
      tags=["venetian mask", "carnival", "mardi gras", "costume party", "ball mask", "eye mask", "theatre"],
      aliases=["venetian-mask"])
def _(S):
    outline = poly([(2.5, 6.5), (8, 9), (12, 8), (16, 9), (21.5, 6.5), (21, 11.5), (17.5, 15.5), (14.5, 14.5), (12, 12.8),
                    (9.5, 14.5), (6.5, 15.5), (3, 11.5)], closed=True, r=S.r)
    return [
        shell(outline),
        detail(poly(_ep(7.3, 11.4, 2.3, 1.5, 6), closed=True)),
        detail(poly(_ep(16.7, 11.4, 2.3, 1.5, 6), closed=True)),
        line(seg(19, 15, 21, 21.5)),
    ]


@icon("belt-buckle", CAT, "Large oval western belt buckle with a star in the middle.",
      tags=["western buckle", "cowboy", "rodeo", "belt", "star", "leather belt", "accessory"],
      aliases=["western-buckle"])
def _(S):
    star = []
    for i in range(10):
        r_ = 5.2 if i % 2 == 0 else 2.2
        star.append(polar(12, 12.2, r_, -90 + i * 36))
    return [
        shell(poly(_ep(12, 12, 9.6, 7.6, 10), closed=True, r=S.r) if S.name == "line" else ellipse(12, 12, 9.6, 7.6)),
        Part("dot", poly(star, closed=True, r=S.r * 0.3)),
    ]
