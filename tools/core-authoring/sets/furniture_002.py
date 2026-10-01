"""TypeIcon Core: furniture (batch furniture_002).

Original drawings of beds, baby furniture, storage, lighting, rugs, window dressing, mirrors, clocks and
home decor. Masses are shells, inner divisions are details, legs and frames are open strokes.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "furniture"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    """Container corner radius for the style, optionally capped for small shapes."""
    if cap is None:
        return S.R
    return min(S.R, cap) if S.name == "rounded" else min(S.R, cap) * 0.4


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def mark(d) -> Part:
    return Part("dot", d)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def flip(d):
    """Mirror a d-string across the vertical centre line."""
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


# ============================================================================ beds and baby

@icon("sleigh-bed", CAT, "Side view of a bed whose headboard and footboard curl outward like a sleigh.",
      tags=["sleigh bed", "bed", "bedroom", "scroll bed", "furniture", "classic"])
def _(S):
    return [
        shell(rect(6, 12, 13, 4.5, rr(S, 2))),
        line("M6 20.5V7A3 3 0 0 0 3 4"),
        line("M19 20.5V10.5A2.5 2.5 0 0 1 21.5 8"),
    ]


@icon("water-bed", CAT, "Side view of a bed frame whose mattress has wavy water lines inside.",
      tags=["waterbed", "bed", "mattress", "waves", "bedroom", "furniture"])
def _(S):
    return [
        shell(rect(3, 8, 18, 10, rr(S, 3))),
        detail("M6.5 13Q8.25 11 10 13T13.5 13T17 13"),
        line(seg(6, 18, 6, 21)), line(seg(18, 18, 18, 21)),
    ]


@icon("twin-beds", CAT, "Top view of two single beds side by side, each with a pillow and a folded cover.",
      tags=["twin beds", "single beds", "bedroom", "guest room", "hotel room", "kids room", "two beds"])
def _(S):
    def bed(x):
        return [
            shell(rect(x, 3.5, 7.5, 17, rr(S, 2))),
            detail(seg(x, 11, x + 7.5, 11)),
            sq(x + 2, 5.5, 3.5, 3, 1),
        ]
    return bed(3) + bed(13.5)


@icon("double-bed", CAT, "Front view of a wide bed with two pillows side by side against the headboard.",
      tags=["double bed", "king bed", "queen bed", "bedroom", "couple", "master bedroom", "pillows"])
def _(S):
    return [
        line(poly([(4, 20.5), (4, 3.5), (20, 3.5), (20, 20.5)], r=S.r)),
        shell(rect(6.5, 7, 5, 4, rr(S, 1.5))),
        shell(rect(12.5, 7, 5, 4, rr(S, 1.5))),
        shell(rect(4, 12.5, 16, 5, rr(S, 2))),
    ]


@icon("futon", CAT, "Thin mattress laid flat on the floor with a pillow and a folded quilt.",
      tags=["floor bed", "japanese bed", "mattress", "sleeping mat", "bedding", "guest bed"])
def _(S):
    return [
        shell(rect(2.5, 13, 19, 6, rr(S, 2))),
        detail(seg(14.5, 13, 14.5, 19)),
        line(poly([(5.5, 13), (5.5, 10), (8, 8), (11, 8), (11, 13)], r=S.r)),
    ]


@icon("charpai", CAT, "Traditional rope bed with a crisscross lattice stretched on a four-legged wooden frame.",
      tags=["charpoy", "rope bed", "woven bed", "cot", "string bed", "south asian", "traditional"])
def _(S):
    return [
        shell(rect(3, 7.5, 18, 9, rr(S, 2))),
        detail(seg(9, 7.5, 9, 16.5)), detail(seg(15, 7.5, 15, 16.5)), detail(seg(3, 12, 21, 12)),
        line(seg(5, 16.5, 5, 21)), line(seg(19, 16.5, 19, 21)),
    ]


@icon("bassinet", CAT, "Small oval baby basket with a hood at one end on a stand with legs.",
      tags=["baby bed", "newborn", "moses basket", "nursery", "infant", "sleeper"])
def _(S):
    return [
        shell("M3 11H21Q21 17.5 12 17.5Q3 17.5 3 11Z"),
        line("M3 11C3 6.5 6 4 10.5 4V11"),
        line(seg(6, 17, 4.5, 21)), line(seg(18, 17, 19.5, 21)),
    ]


@icon("cradle", CAT, "Wooden baby bed with slatted sides sitting on two curved rockers.",
      tags=["baby cradle", "rocking cot", "nursery", "infant", "newborn", "rocker"])
def _(S):
    return [
        shell(poly([(3.5, 5.5), (20.5, 5.5), (18.5, 16), (5.5, 16)], closed=True, r=S.r * 0.6)),
        detail(seg(9, 5.5, 9.5, 16)), detail(seg(15, 5.5, 14.5, 16)),
        line("M2.5 18.5Q12 24 21.5 18.5"),
    ]


@icon("playpen", CAT, "Square mesh-sided baby play enclosure with a ball inside.",
      tags=["play pen", "playard", "baby play area", "nursery", "toddler", "enclosure"])
def _(S):
    return [
        shell(rect(3, 5.5, 18, 14, rr(S, 3))),
        detail(seg(7.5, 5.5, 7.5, 19.5)), detail(seg(16.5, 5.5, 16.5, 19.5)),
        shell(circle(12, 12.5, 2.2)),
        line(seg(6, 19.5, 6, 21.5)), line(seg(18, 19.5, 18, 21.5)),
    ]


@icon("baby-mobile", CAT, "Hanging crib mobile with a bar and three small shapes dangling on strings.",
      tags=["crib mobile", "nursery", "hanging toy", "baby toy", "infant", "cot mobile"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 4.5)), line(seg(3, 4.5, 21, 4.5)),
        line(seg(5, 4.5, 5, 9.5)), line(seg(12, 4.5, 12, 11)), line(seg(19, 4.5, 19, 9.5)),
        shell(circle(5, 12, 2.5)),
        shell(poly([(12, 11), (14.5, 13.75), (12, 16.5), (9.5, 13.75)], closed=True, r=S.r * 0.4)),
        shell(circle(19, 12, 2.5)),
    ]


@icon("baby-gate", CAT, "Short gate of vertical bars with rails, fitted between two wall posts.",
      tags=["safety gate", "stair gate", "child safety", "toddler", "pet gate", "barrier"])
def _(S):
    return [
        line(seg(4, 3, 4, 21)), line(seg(20, 3, 20, 21)),
        line(seg(4, 7, 20, 7)), line(seg(4, 17, 20, 17)),
        line(seg(8, 7, 8, 17)), line(seg(12, 7, 12, 17)), line(seg(16, 7, 16, 17)),
    ]


# ============================================================================ storage

@icon("display-cabinet", CAT, "Tall cabinet with glass doors showing plates standing on shelves inside.",
      tags=["china cabinet", "curio cabinet", "glass cabinet", "hutch", "dining room", "showcase"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 17, rr(S, 3))),
        detail(seg(4.5, 9, 19.5, 9)), detail(seg(4.5, 14.5, 19.5, 14.5)),
        dot(9, 6, 1.4), dot(15, 6, 1.4), dot(12, 11.75, 1.4),
        line(seg(7, 19.5, 7, 21.5)), line(seg(17, 19.5, 17, 21.5)),
    ]


@icon("toy-box", CAT, "Open wooden chest with a propped lid and a ball poking out.",
      tags=["toy chest", "kids storage", "nursery", "playroom", "toy storage", "tidy up"])
def _(S):
    return [
        shell(rect(3.5, 13, 17, 8, rr(S, 2))),
        line(poly([(5, 13), (7, 4.5), (17, 4.5), (19, 13)], r=S.r)),
        line("M9 13A3 3 0 0 1 15 13"),
    ]


@icon("magazine-rack", CAT, "Small floor rack with a curved slat holding two standing magazines.",
      tags=["magazine holder", "newspaper rack", "reading corner", "living room", "bathroom", "storage"])
def _(S):
    return [
        line(poly([(6.5, 10), (6.5, 3), (11.5, 3), (11.5, 10)], r=S.r)),
        line(poly([(12.5, 10), (12.5, 3), (17.5, 3), (17.5, 10)], r=S.r)),
        shell(poly([(3.5, 10), (20.5, 10), (18.5, 19.5), (5.5, 19.5)], closed=True, r=S.r * 0.6)),
        detail(seg(5, 14.75, 19, 14.75)),
    ]


@icon("cube-storage", CAT, "Square shelving unit divided into a grid of cubbies, some with fabric bins.",
      tags=["cubby shelf", "cube shelf", "cubbies", "storage cubes", "kids storage", "organizer"])
def _(S):
    return [
        shell(rect(3.5, 3.5, 17, 17, rr(S, 3))),
        detail(seg(12, 3.5, 12, 20.5)), detail(seg(3.5, 12, 20.5, 12)),
        sq(6, 15, 4, 3.5, 0.5), sq(14, 6, 4, 3.5, 0.5),
    ]


@icon("ladder-shelf", CAT, "Leaning ladder-shaped shelf with three shelves narrowing toward the top.",
      tags=["ladder bookcase", "leaning shelf", "storage", "bookshelf", "living room", "display"])
def _(S):
    return [
        line(seg(4, 21.5, 7, 2.5)), line(seg(20, 21.5, 17, 2.5)),
        line(seg(6.3, 7, 17.7, 7)), line(seg(5.3, 13, 18.7, 13)), line(seg(4.4, 19, 19.6, 19)),
    ]


@icon("corner-shelf", CAT, "Top view of a quarter-round shelf fitted into a wall corner, holding a small plant.",
      tags=["corner shelves", "wall shelf", "quarter round shelf", "plant shelf", "display", "storage"])
def _(S):
    return [
        line(poly([(3, 21), (3, 3), (21, 3)], r=S.r)),
        shell("M6.5 6.5H19A12.5 12.5 0 0 1 6.5 19Z"),
        shell(circle(11, 11, 2.5)),
    ]


@icon("bookends", CAT, "Two L-shaped bookends holding an upright book and a leaning book between them.",
      tags=["book ends", "book holder", "book supports", "desk organizer", "library", "shelf"])
def _(S):
    return [
        line(poly([(3.5, 4.5), (3.5, 20.5), (6, 20.5)], r=S.r)),
        line(poly([(20.5, 4.5), (20.5, 20.5), (18, 20.5)], r=S.r)),
        shell(rect(7.5, 6, 4.5, 14.5, rr(S, 1))),
        shell(poly([(13.5, 20.5), (17, 20.5), (17.8, 9), (14.5, 8.2)], closed=True, r=S.r * 0.3)),
    ]


@icon("storage-basket", CAT, "Woven basket with striped weave and two side handles.",
      tags=["wicker basket", "woven basket", "laundry basket", "organizer", "hamper", "home storage"])
def _(S):
    return [
        shell(poly([(5.5, 8), (18.5, 8), (17, 21), (7, 21)], closed=True, r=S.r * 0.6)),
        detail(seg(5.9, 12.2, 18.1, 12.2)), detail(seg(6.4, 16.6, 17.6, 16.6)),
        line("M5.5 10Q1.5 12 5.8 16"), line("M18.5 10Q22.5 12 18.2 16"),
    ]


@icon("key-rack", CAT, "Small wall plaque with hooks holding two keys.",
      tags=["key holder", "key hooks", "entryway", "hallway", "wall hook", "house keys"])
def _(S):
    return [
        shell(rect(3, 3, 18, 5.5, rr(S, 2))),
        line(seg(7.5, 8.5, 7.5, 10.5)), shell(circle(7.5, 12.7, 2.2)), line(seg(7.5, 14.9, 7.5, 21)), line(seg(7.5, 19, 9.5, 19)),
        line(seg(16.5, 8.5, 16.5, 10.5)), shell(circle(16.5, 12.7, 2.2)), line(seg(16.5, 14.9, 16.5, 21)), line(seg(16.5, 19, 18.5, 19)),
    ]


@icon("valet-stand", CAT, "Standing suit valet with a jacket on a shaped hanger, a stem and a tripod foot.",
      tags=["suit stand", "clothes stand", "dressing stand", "jacket hanger", "bedroom", "wardrobe"])
def _(S):
    return [
        line(seg(12, 2, 12, 4.5)),
        shell(poly([(12, 4.5), (4.5, 8.5), (4.5, 14), (19.5, 14), (19.5, 8.5)], closed=True, r=S.r * 0.6)),
        detail(seg(12, 8, 12, 14)),
        line(seg(12, 14, 12, 18.5)),
        line(poly([(6, 21.5), (12, 18.5), (18, 21.5)], r=S.r)),
    ]


@icon("blanket-ladder", CAT, "Wooden ladder leaning on a wall with a wide folded blanket draped over its top rungs.",
      tags=["decorative ladder", "towel ladder", "throw blanket", "living room", "bathroom", "home decor"])
def _(S):
    return [
        line(seg(7, 2.5, 6.5, 5.5)), line(seg(17, 2.5, 17.5, 5.5)),
        shell(rect(3.5, 5.5, 17, 8.5, rr(S, 2))),
        detail(seg(3.5, 9.75, 20.5, 9.75)),
        line(seg(6.5, 14, 5.5, 21.5)), line(seg(17.5, 14, 18.5, 21.5)),
        line(seg(6, 18, 18, 18)),
    ]


@icon("folding-screen", CAT, "Three-panel folding room divider standing in a zigzag.",
      tags=["room divider", "privacy screen", "partition", "shoji screen", "dressing screen", "bedroom"])
def _(S):
    return [
        shell(poly([(3, 5), (9, 3), (15, 5), (21, 3), (21, 19), (15, 21), (9, 19), (3, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(9, 3, 9, 19)), detail(seg(15, 5, 15, 21)),
    ]


@icon("shoji-door", CAT, "Japanese sliding door with a fine wooden grid over paper panels.",
      tags=["shoji screen", "sliding door", "japanese door", "paper door", "fusuma", "grid door"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, rr(S, 2))),
        detail(seg(12, 2.5, 12, 21.5)),
        detail(seg(3.5, 9, 20.5, 9)), detail(seg(3.5, 15.5, 20.5, 15.5)),
    ]


@icon("wall-cabinet", CAT, "Wall-hung upper cabinet with two doors mounted above a counter.",
      tags=["kitchen cabinet", "upper cabinet", "wall unit", "cupboard", "kitchen", "storage"])
def _(S):
    return [
        shell(rect(3, 3, 18, 10.5, rr(S, 2))),
        detail(seg(12, 3, 12, 13.5)),
        sq(8.75, 7.5, 1.5, 3.5), sq(13.75, 7.5, 1.5, 3.5),
        shell(rect(2.5, 17.5, 19, 4, rr(S, 1.5))),
    ]


@icon("paper-lantern", CAT, "Round ribbed paper lantern hanging from a cord with small caps top and bottom.",
      tags=["chinese lantern", "japanese lantern", "chochin", "hanging lamp", "festival", "pendant light"])
def _(S):
    return [
        line(seg(12, 2, 12, 4.5)),
        solid(rect(9.25, 4.25, 5.5, 2.25, 0.6)),
        shell(ellipse(12, 12.5, 8.5, 6.5)),
        detail(ellipse(12, 12.5, 3.6, 6.2)),
        solid(rect(9.25, 18.5, 5.5, 2.25, 0.6)),
    ]


@icon("tripod-lamp", CAT, "Floor lamp with a drum shade on three splayed legs.",
      tags=["tripod floor lamp", "floor lamp", "standing lamp", "living room", "lighting", "scandinavian"])
def _(S):
    return [
        shell(poly([(7.5, 2.5), (16.5, 2.5), (19, 10), (5, 10)], closed=True, r=S.r * 0.5)),
        line(seg(9, 10, 5, 21.5)), line(seg(12, 10, 12, 21.5)), line(seg(15, 10, 19, 21.5)),
    ]


@icon("neon-sign", CAT, "Glowing tube light bent into a heart shape inside a thin wall frame.",
      tags=["neon light", "led sign", "glowing sign", "wall art", "bar sign", "heart sign", "light sign"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 18, rr(S, 4))),
        detail("M12 17C5 12.5 6.5 7 9.5 7C11 7 12 8 12 9C12 8 13 7 14.5 7C17.5 7 19 12.5 12 17Z"),
    ]


@icon("cage-light", CAT, "Hanging pendant bulb inside a domed wire cage guard.",
      tags=["pendant lamp", "industrial light", "wire cage lamp", "hanging light", "loft", "bulb guard"])
def _(S):
    return [
        line(seg(12, 2, 12, 5.5)),
        solid(rect(10, 5, 4, 2.5, 0.5)),
        shell("M4.5 21V15A7.5 7.5 0 0 1 19.5 15V21Z"),
        detail(seg(8.5, 9, 8.5, 21)), detail(seg(15.5, 9, 15.5, 21)),
        dot(12, 15.5, 1.5),
    ]


@icon("hurricane-lamp", CAT, "Kerosene lantern with a rounded glass chimney on a metal base and a wire handle.",
      tags=["oil lamp", "storm lantern", "kerosene lamp", "camping lamp", "rustic light", "glass lantern"])
def _(S):
    return [
        line("M6.5 12Q5.5 2.5 12 2.5Q18.5 2.5 17.5 12"),
        shell("M8.5 17.5C4 14.5 5.5 7 12 7C18.5 7 20 14.5 15.5 17.5Z"),
        mark("M12 10Q14.5 13.5 12 16Q9.5 13.5 12 10Z"),
        shell(rect(6.5, 17.5, 11, 4, rr(S, 1.5))),
    ]


# ============================================================================ lighting

@icon("candelabra", CAT, "Branched candle holder with three curved arms each holding a lit candle.",
      tags=["candle holder", "candlestick", "branched candlestick", "dinner table", "romantic", "gothic"])
def _(S):
    return [
        line("M4.5 10V11.5Q4.5 16 12 16Q19.5 16 19.5 11.5V10"),
        line(seg(12, 16, 12, 20)), line(seg(8, 21, 16, 21)),
        line(seg(4.5, 10, 4.5, 7)), line(seg(19.5, 10, 19.5, 7)), line(seg(12, 16, 12, 7)),
        dot(4.5, 4.3, 1.3), dot(19.5, 4.3, 1.3), dot(12, 4.3, 1.3),
    ]


@icon("tealight", CAT, "Small round tea light candle in a shallow metal cup with a flame.",
      tags=["tea light", "votive", "small candle", "candle", "ambience", "flame", "relax"])
def _(S):
    return [
        solid("M12 2.5Q16.5 7 12 11Q7.5 7 12 2.5Z"),
        shell(poly([(3.5, 13.5), (20.5, 13.5), (18.5, 21), (5.5, 21)], closed=True, r=S.r * 0.6)),
    ]


@icon("lampshade", CAT, "Empty drum lampshade with a tapered shape and a small ring fitting at the top.",
      tags=["lamp shade", "shade", "lamp cover", "light fitting", "bedside lamp", "home decor"])
def _(S):
    return [
        line(poly([(9.5, 5), (9.5, 2.5), (14.5, 2.5), (14.5, 5)], r=S.r * 0.5)),
        shell("M8 5H16L21 18Q12 21.5 3 18Z"),
        detail("M6.2 11.5Q12 13.5 17.8 11.5"),
    ]


@icon("sputnik-chandelier", CAT, "Ceiling light with a central ball and many straight arms radiating out, each with a bulb.",
      tags=["starburst chandelier", "atomic light", "mid century light", "ceiling lamp", "pendant", "modern"])
def _(S):
    out = [line(seg(12, 2, 12, 9.6)), shell(circle(12, 13, 2.4))]
    for a in (-45, 0, 45, 90, 135, 180, 225):
        x1, y1 = polar(12, 13, 4.3, a)
        x2, y2 = polar(12, 13, 7.3, a)
        bx, by = polar(12, 13, 8.9, a)
        out.append(line(seg(x1, y1, x2, y2)))
        out.append(dot(bx, by, 1.5))
    return out


@icon("mushroom-lamp", CAT, "Small table lamp shaped like a mushroom with a dome cap over a short stem.",
      tags=["toadstool lamp", "mushroom light", "table lamp", "night light", "cottagecore", "bedside"])
def _(S):
    return [
        shell("M3 13A9 9 0 0 1 21 13Z"),
        dot(8.5, 9.5, 1.3), dot(14, 7.5, 1.3), dot(16.5, 10.5, 1.0),
        line(seg(9.5, 13, 9.5, 19.5)), line(seg(14.5, 13, 14.5, 19.5)),
        line(seg(6.5, 20.5, 17.5, 20.5)),
    ]


@icon("plasma-ball", CAT, "Glass globe on a base with forked lightning lines reaching from the center to the glass.",
      tags=["plasma globe", "lightning ball", "tesla ball", "static electricity", "science toy", "energy"])
def _(S):
    def bolt(a):
        return detail(poly([(12, 9.5), polar(12, 9.5, 2.6, a - 25), polar(12, 9.5, 4, a + 20), polar(12, 9.5, 6, a)]))
    return [
        shell(circle(12, 9.5, 7.5)),
        bolt(-150), bolt(-30), bolt(90),
        shell(poly([(7, 21.5), (9, 17.5), (15, 17.5), (17, 21.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("garden-torch", CAT, "Bamboo garden torch on a tall pole with a flame burning in its top cup.",
      tags=["tiki torch", "outdoor torch", "patio", "backyard", "bamboo", "flame", "luau"])
def _(S):
    return [
        solid("M12 2Q16.5 6.5 12 9.5Q7.5 6.5 12 2Z"),
        shell(poly([(7.5, 10.5), (16.5, 10.5), (14.5, 14.5), (9.5, 14.5)], closed=True, r=S.r * 0.4)),
        line(seg(12, 14.5, 12, 21.5)),
        line(seg(10, 18, 14, 18)),
    ]


# ============================================================================ rugs and mats

@icon("round-rug", CAT, "Circular rug with an outer ring and a diamond pattern at the center.",
      tags=["circle rug", "area rug", "carpet", "floor covering", "living room", "bedroom"])
def _(S):
    return [
        shell(circle(12, 12, 9.5)),
        detail(poly(regular(12, 12, 5.8, 4), closed=True, r=S.r)),
    ]


@icon("sheepskin-rug", CAT, "Irregular fluffy hide-shaped rug with lumpy legs and wavy wool edges.",
      tags=["sheepskin", "fur rug", "hide rug", "faux fur", "fluffy rug", "cozy", "throw"])
def _(S):
    return [
        shell("M9.5 3.5Q12 2.5 14.5 3.5L15.5 6.5C17.5 5.8 19.5 6 20.5 8.2L19.2 11C20.3 13.3 20.5 16 19.5 18.5L16.5 20.2C15.5 21.5 13.5 21.5 12 20.5C10.5 21.5 8.5 21.5 7.5 20.2L4.5 18.5C3.5 16 3.7 13.3 4.8 11L3.5 8.2C4.5 6 6.5 5.8 8.5 6.5Z"),
        detail("M9.5 13Q12 10.5 14.5 13"),
    ]


@icon("shag-rug", CAT, "Rectangular rug with long shaggy pile strands drawn as wavy vertical lines and a zigzag fringe.",
      tags=["shaggy carpet", "fluffy rug", "deep pile", "high pile rug", "flokati", "living room"])
def _(S):
    return [
        shell(poly([(3, 4), (21, 4), (21, 16), (19, 20), (17, 16), (15, 20), (13, 16), (11, 20), (9, 16), (7, 20), (5, 16), (3, 20)],
                   closed=True, r=S.r * 0.3)),
        detail("M8 7Q9.5 9 8 11T8 14"),
        detail("M12 7Q13.5 9 12 11T12 14"),
        detail("M16 7Q17.5 9 16 11T16 14"),
    ]


@icon("braided-rug", CAT, "Oval rug made of a tight braid coiled in an S-shaped spiral.",
      tags=["oval rug", "rag rug", "country rug", "coiled rug", "farmhouse", "floor mat"])
def _(S):
    return [
        shell(ellipse(12, 12, 9.5, 7.5)),
        detail("M7.5 12C7.5 9 12 9 12 12C12 15 16.5 15 16.5 12"),
    ]


@icon("rolled-rug", CAT, "Carpet partly rolled up into a thick cylinder with the flat end lying in front.",
      tags=["rolled carpet", "rolled up rug", "moving", "storage", "carpet roll", "floor covering"])
def _(S):
    return [
        shell(circle(7.5, 8, 6)),
        detail(circle(7.5, 8, 2.1)),
        shell(rect(7.5, 14, 14, 5, rr(S, 1.5))),
    ]


@icon("prayer-rug", CAT, "Rectangular prayer mat with a pointed arch niche motif and a small lamp dot above.",
      tags=["prayer mat", "janamaz", "sejadah", "islamic", "mosque", "rug", "worship", "muslim"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, rr(S, 2))),
        detail(poly([(8.5, 18), (8.5, 12.5), (12, 8), (15.5, 12.5), (15.5, 18)], r=S.r * 0.6)),
        dot(12, 14, 1.3),
    ]


@icon("tatami-mat", CAT, "Rectangular Japanese straw floor mat with lengthwise weave lines.",
      tags=["tatami", "straw mat", "japanese floor", "igusa", "rush mat", "yoga mat", "zen"])
def _(S):
    return [
        shell(rect(2.5, 6, 19, 12, rr(S, 2))),
        detail(seg(2.5, 10, 21.5, 10)), detail(seg(2.5, 14, 21.5, 14)),
    ]


@icon("play-mat", CAT, "Kids play mat printed with a winding road, a small house and a tree.",
      tags=["baby play mat", "activity mat", "road mat", "nursery", "toddler", "playroom", "kids rug"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, rr(S, 4))),
        detail(poly([(5.5, 11.5), (5.5, 8), (8.25, 6), (11, 8), (11, 11.5)])),
        dot(17.5, 8, 2),
        detail("M5.5 17.5H10.5Q14.5 17.5 14.5 15Q14.5 13 17 13H19"),
    ]


# ============================================================================ window dressing

@icon("roller-blind", CAT, "Window covered by a smooth blind pulled down from a roller at the top with a pull cord.",
      tags=["window blind", "window shade", "roller shade", "blinds", "window covering", "privacy"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 4, rr(S, 2))),
        line(poly([(5, 6.5), (5, 14.5), (19, 14.5), (19, 6.5)], r=S.r)),
        line(seg(12, 14.5, 12, 18.5)), dot(12, 20, 1.5),
    ]


@icon("venetian-blind", CAT, "Window covered by many thin horizontal slats hanging from a head rail with a pull cord.",
      tags=["window blinds", "slatted blind", "horizontal blinds", "mini blinds", "window covering", "louvre"])
def _(S):
    return [
        shell(rect(3, 2.5, 15, 3, rr(S, 1.5))),
        line(seg(3.5, 8.5, 17.5, 8.5)), line(seg(3.5, 12.5, 17.5, 12.5)), line(seg(3.5, 16.5, 17.5, 16.5)),
        line(seg(3.5, 20.5, 17.5, 20.5)),
        line(seg(20.5, 4, 20.5, 19)), dot(20.5, 20.3, 1.3),
    ]


@icon("roman-blind", CAT, "Fabric window blind folded up in soft horizontal pleats near the top.",
      tags=["roman shade", "fabric blind", "pleated blind", "window covering", "window treatment", "folds"])
def _(S):
    return [
        shell("M3 3H21V13Q12 16.5 3 13Z"),
        detail("M3 7Q12 10 21 7"),
        line(seg(12, 16, 12, 19.5)), dot(12, 20.5, 1.2),
    ]


@icon("vertical-blinds", CAT, "Row of tall vertical slats hanging from a track across a window.",
      tags=["vertical blind", "patio blinds", "slat blinds", "window covering", "office blinds", "louvres"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 3, rr(S, 1.5))),
        line(seg(5, 8, 5, 20)), line(seg(9, 8, 9, 19)), line(seg(13, 8, 13, 20)), line(seg(17, 8, 17, 19)),
        line(seg(21, 8, 21, 20)),
    ]


@icon("window-shutters", CAT, "Two open louvered window shutters standing on either side of a window.",
      tags=["louvered shutters", "plantation shutters", "window shutter", "exterior shutters", "louvre", "house"])
def _(S):
    return [
        shell(rect(2.5, 3, 7, 18, rr(S, 2))),
        detail(seg(2.5, 7.5, 9.5, 7.5)), detail(seg(2.5, 12, 9.5, 12)), detail(seg(2.5, 16.5, 9.5, 16.5)),
        shell(rect(14.5, 3, 7, 18, rr(S, 2))),
        detail(seg(14.5, 7.5, 21.5, 7.5)), detail(seg(14.5, 12, 21.5, 12)), detail(seg(14.5, 16.5, 21.5, 16.5)),
    ]


@icon("cafe-curtain", CAT, "Short curtain covering only the lower half of a window, hung from a rod across the middle.",
      tags=["cafe curtains", "half curtain", "kitchen curtain", "short curtain", "window treatment", "valance"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 3))),
        detail(seg(3, 10, 21, 10)),
        detail("M8.5 10Q7 15.5 8.5 21"), detail("M15.5 10Q17 15.5 15.5 21"),
    ]


@icon("curtain-rod", CAT, "Horizontal rod with ball finials at each end and three rings holding folds of hanging fabric.",
      tags=["drapery rod", "curtain pole", "curtain rail", "finial", "curtain rings", "window hardware"])
def _(S):
    return [
        line(seg(5, 5.5, 19, 5.5)),
        dot(3.4, 5.5, 2.4), dot(20.6, 5.5, 2.4),
        dot(8, 9, 1.3), dot(12, 9, 1.3), dot(16, 9, 1.3),
        line("M8 11.5Q6.3 16.5 8 21"), line("M12 11.5Q10.3 16.5 12 21"), line("M16 11.5Q14.3 16.5 16 21"),
    ]


@icon("bead-curtain", CAT, "Doorway curtain made of many vertical strings of beads hanging from a rail.",
      tags=["beaded curtain", "door beads", "hippie curtain", "string curtain", "boho", "doorway curtain"])
def _(S):
    out = [shell(rect(3, 2.5, 18, 2.5, rr(S, 1)))]
    for x in (4.5, 8.5, 12.5, 16.5, 20.5):
        for i, y in enumerate((8, 12, 16, 20)):
            out.append(dot(x, y, 1.4))
    return out


@icon("noren", CAT, "Japanese split doorway curtain hanging from a rod in three fabric panels with slits.",
      tags=["noren curtain", "japanese curtain", "split curtain", "shop curtain", "restaurant entrance", "door curtain"])
def _(S):
    return [
        line(seg(2.5, 3.5, 21.5, 3.5)),
        line(seg(6, 3.5, 6, 6.5)), line(seg(12, 3.5, 12, 6.5)), line(seg(18, 3.5, 18, 6.5)),
        shell(rect(3.5, 6.5, 17, 14, rr(S, 2))),
        detail(seg(9, 20.5, 9, 12)), detail(seg(15, 20.5, 15, 12)),
    ]


@icon("blackout-curtain", CAT, "Closed dark curtains fully covering a window with a crescent moon beside them.",
      tags=["darkening curtain", "thermal curtain", "night curtain", "bedroom curtain", "sleep", "light blocking"])
def _(S):
    return [
        line(seg(2.5, 6, 14.5, 6)),
        shell(rect(3, 7.5, 11, 13.5, rr(S, 2))),
        detail(seg(8.5, 7.5, 8.5, 21)),
        solid(minus(circle(18.3, 9, 3.7), circle(19.7, 7.6, 3.2))),
    ]


# ============================================================================ mirrors

@icon("cheval-mirror", CAT, "Full-length oval mirror swiveling between two uprights on a floor stand.",
      tags=["standing mirror", "floor mirror", "dressing mirror", "full length mirror", "bedroom", "swivel mirror"])
def _(S):
    return [
        line(seg(3.5, 4, 3.5, 21.5)), line(seg(20.5, 4, 20.5, 21.5)),
        line(seg(2.5, 21.5, 21.5, 21.5)),
        line(seg(3.5, 11.5, 6, 11.5)), line(seg(18, 11.5, 20.5, 11.5)),
        shell(ellipse(12, 11.5, 6, 8)),
        detail("M9.5 11Q9.8 8.5 12 7.5"),
    ]


@icon("sunburst-mirror", CAT, "Round mirror with a glint, surrounded by radiating spikes like sun rays.",
      tags=["starburst mirror", "sun mirror", "wall mirror", "decorative mirror", "rays", "mid century"])
def _(S):
    out = [shell(circle(12, 12, 5.8)), detail(arc(12, 12, 2.6, 195, 265))]
    for i in range(12):
        a = i * 30
        r2 = 10.6 if i % 2 == 0 else 9.2
        x1, y1 = polar(12, 12, 8.3, a)
        x2, y2 = polar(12, 12, r2, a)
        out.append(line(seg(x1, y1, x2, y2)))
    return out


@icon("trifold-mirror", CAT, "Three-panel tabletop mirror with a tall center panel and two angled side wings.",
      tags=["triptych mirror", "vanity mirror", "three way mirror", "dressing table", "makeup mirror", "tabletop mirror"])
def _(S):
    return [
        shell(poly([(2.5, 5.5), (7, 3.5), (7, 15.5), (2.5, 17.5)], closed=True, r=S.r * 0.4)),
        shell(poly([(21.5, 5.5), (17, 3.5), (17, 15.5), (21.5, 17.5)], closed=True, r=S.r * 0.4)),
        shell(rect(8.5, 2.5, 7, 14, rr(S, 2))),
        line(seg(12, 16.5, 12, 20)), line(seg(7.5, 21, 16.5, 21)),
    ]


# ============================================================================ clocks

def hands(cx, cy, r, S):
    """Hour and minute hands as one polyline (knocked out in Filled)."""
    return detail(poly([(cx, cy - r * 0.55), (cx, cy), (cx + r * 0.42, cy + r * 0.2)], r=S.r * 0.5))


def gear_d(cx, cy, ro, ri, n):
    pts = []
    p = 360 / n
    for i in range(n):
        a0 = i * p
        for rad, da in ((ri, -0.5), (ro, -0.27), (ro, 0.27), (ri, 0.5)):
            pts.append(polar(cx, cy, rad, a0 + da * p))
    return poly(pts, closed=True)


@icon("clock-cuckoo", CAT, "Carved house-shaped wall clock with a round dial, a small bird door and two hanging weights.",
      tags=["cuckoo clock", "black forest clock", "chalet clock", "bird clock", "wall clock", "german", "swiss"])
def _(S):
    return [
        shell(poly([(3.5, 16), (3.5, 10), (12, 2.5), (20.5, 10), (20.5, 16)], closed=True, r=S.r * 0.5)),
        detail(circle(12, 11.6, 2.9)),
        line(seg(8, 16, 8, 18.5)), dot(8, 20.2, 1.6),
        line(seg(16, 16, 16, 18.5)), dot(16, 20.2, 1.6),
    ]


@icon("clock-grandfather", CAT, "Tall floor-standing longcase clock with an arched dial on top and a swinging pendulum below.",
      tags=["grandfather clock", "longcase clock", "floor clock", "pendulum clock", "tall clock", "antique"])
def _(S):
    return [
        shell("M6.5 10.5V6Q6.5 2.5 12 2.5Q17.5 2.5 17.5 6V10.5H15.5V19H17V21.5H7V19H8.5V10.5Z"),
        detail(circle(12, 6.6, 2.4)),
        detail(seg(12, 13, 12, 16.2)), dot(12, 17.3, 1.1),
    ]


@icon("clock-mantel", CAT, "Wide wooden clock with an arched top and a round dial with hands, sitting on a stepped base.",
      tags=["mantel clock", "mantle clock", "shelf clock", "fireplace clock", "desk clock", "antique"])
def _(S):
    return [
        shell("M2.5 21H21.5V18.5H20.5V10.5A8.5 8.5 0 0 0 3.5 10.5V18.5H2.5Z"),
        detail(circle(12, 11, 4.6)),
        hands(12, 11, 4.6, S),
    ]


@icon("clock-carriage", CAT, "Small rectangular brass carriage clock with a round dial and a carry handle on top.",
      tags=["carriage clock", "travel clock", "brass clock", "desk clock", "glass clock", "antique"])
def _(S):
    return [
        line("M8 8.5V5.5Q8 3 10.5 3H13.5Q16 3 16 5.5V8.5"),
        shell(rect(3.5, 8.5, 17, 12.5, rr(S, 2))),
        detail(circle(12, 14.75, 4.3)),
        hands(12, 14.75, 4.3, S),
    ]


@icon("clock-flip", CAT, "Retro flip clock with two split-flap number cards showing digits on a small base.",
      tags=["flip clock", "split flap clock", "retro clock", "digital clock", "desk clock", "vintage", "bedside"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 8.5, 13, rr(S, 2))),
        shell(rect(13, 3.5, 8.5, 13, rr(S, 2))),
        detail(poly([(5.6, 8), (7.8, 6.2), (7.8, 14)], r=S.r * 0.4)),
        detail(ellipse(17.25, 10, 1.4, 2.8)),
        line(seg(4, 20.5, 20, 20.5)),
    ]


@icon("clock-station", CAT, "Double-sided station clock hanging from a ceiling bar on a rod, with its second face behind.",
      tags=["station clock", "railway clock", "train station clock", "hanging clock", "platform clock", "double sided clock"])
def _(S):
    return [
        line(seg(5, 2.5, 19, 2.5)), line(seg(12.5, 2.5, 12.5, 7.5)),
        line(arc(14.5, 14.5, 6.5, -68, 68)),
        shell(circle(10.5, 14.5, 6.5)),
        hands(10.5, 14.5, 6.5, S),
    ]


@icon("clock-sunburst", CAT, "Wall clock with a small round face surrounded by long pointed rays.",
      tags=["sunburst clock", "starburst clock", "atomic clock", "mid century clock", "wall clock", "rays"])
def _(S):
    out = [shell(circle(12, 12, 4.6)), hands(12, 12, 4.6, S)]
    for i in range(12):
        a = i * 30
        r2 = 11 if i % 2 == 0 else 9.6
        bx, by = polar(12, 12, 7.4, a)
        c, s = math.cos(math.radians(a + 90)), math.sin(math.radians(a + 90))
        tx, ty = polar(12, 12, r2, a)
        out.append(solid(poly([(bx - c * 1.1, by - s * 1.1), (tx, ty), (bx + c * 1.1, by + s * 1.1)], closed=True)))
    return out


@icon("clock-anniversary", CAT, "Clock under a glass dome with a small disc pendulum below the dial.",
      tags=["anniversary clock", "400 day clock", "torsion clock", "dome clock", "glass dome clock", "mantel"])
def _(S):
    return [
        line("M6 18.5V9Q6 2.5 12 2.5Q18 2.5 18 9V18.5"),
        shell(rect(4, 18.5, 16, 3, rr(S, 1.5))),
        detail(circle(12, 8.2, 3.4)),
        dot(12, 8.2, 1.1),
        line(seg(12, 12.6, 12, 14.5)), dot(12, 16, 1.7),
    ]


@icon("clock-skeleton", CAT, "Clock with an open face showing a toothed gear at its center.",
      tags=["skeleton clock", "gear clock", "open clock", "mechanical clock", "steampunk", "cogs", "movement"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(gear_d(12, 12, 5.2, 3.9, 8)),
        dot(12, 12, 1.4),
    ]


# ============================================================================ vases and home decor

@icon("bud-vase", CAT, "Slender vase with a long neck holding a single stem with one tulip-like flower.",
      tags=["single stem vase", "flower vase", "slim vase", "flower", "table decor", "bloom", "tulip"])
def _(S):
    return [
        shell("M9.5 6.5V2.5L11 4L12 2L13 4L14.5 2.5V6.5Q14.5 8.5 12 8.5Q9.5 8.5 9.5 6.5Z"),
        line(seg(12, 8.5, 12, 12)),
        shell("M10.5 11.5H13.5V13Q18 15 18 18Q18 21 15.5 21H8.5Q6 21 6 18Q6 15 10.5 13Z"),
        line("M12 10Q16 10 16.5 7"),
    ]


@icon("amphora", CAT, "Tall ancient jar with two looped handles on the neck and a pointed base.",
      tags=["greek vase", "roman jar", "wine jar", "ancient pottery", "classical urn", "museum"])
def _(S):
    return [
        shell("M9.5 2.5H14.5V5.5Q18 8 18 12.5Q18 17 12 21.5Q6 17 6 12.5Q6 8 9.5 5.5Z"),
        line("M9.6 5Q3.5 4.5 3.8 9Q4 11 6.3 11"),
        line("M14.4 5Q20.5 4.5 20.2 9Q20 11 17.7 11"),
        detail("M6.6 14Q12 16 17.4 14"),
    ]


@icon("ginger-jar", CAT, "Round-shouldered lidded jar with a domed cap and a decorated band.",
      tags=["lidded jar", "porcelain jar", "temple jar", "chinoiserie", "ceramic jar", "canister"])
def _(S):
    return [
        line(poly([(7.5, 8), (8.5, 4.8), (15.5, 4.8), (16.5, 8)], r=S.r)),
        dot(12, 3, 1.2),
        shell(poly([(7.5, 8), (16.5, 8), (20.5, 12.5), (20.5, 16.5), (16.5, 21), (7.5, 21), (3.5, 16.5), (3.5, 12.5)], closed=True, r=L(S, 0, 3.5))),
        detail("M4 14.5Q12 17 20 14.5"),
    ]


@icon("music-box", CAT, "Open wooden music box with a tiny ballerina beside a floating music note.",
      tags=["jewellery box", "jewelry box", "ballerina box", "musical box", "gift", "nursery", "lullaby"])
def _(S):
    return [
        dot(8, 5.6, 1.5),
        solid("M8 8.6L5 12.6H11Z"),
        dot(16, 10.8, 1.6), line(seg(17.6, 10.8, 17.6, 4.5)), line("M17.6 4.5Q20.5 5 20.5 7.8"),
        shell(rect(3.5, 14.5, 17, 6.5, rr(S, 2))),
    ]


@icon("candle-snuffer", CAT, "Long-handled bell cone lowered over a short candle with a wisp of smoke.",
      tags=["candle extinguisher", "snuffer", "put out candle", "flame out", "church", "candle accessory"])
def _(S):
    return [
        line(seg(14, 7.5, 21, 2.5)),
        shell("M12 7Q15 9.5 17 13.5H7Q9 9.5 12 7Z"),
        shell(rect(9.5, 16, 5, 5, rr(S, 1.2))),
        line("M4 13Q2.8 10.5 4.8 8.5"),
    ]


@icon("wind-chime", CAT, "Round top ring with several hanging metal tubes of different lengths.",
      tags=["wind chimes", "garden chime", "porch chime", "bells", "tubular chime", "breeze", "zen"])
def _(S):
    return [
        line(seg(12, 2, 12, 3.8)),
        shell(rect(4, 3.8, 16, 2.6, rr(S, 1.3))),
        line(seg(6, 7, 6, 16)), line(seg(9.6, 7, 9.6, 20)),
        line(seg(14.4, 7, 14.4, 18)), line(seg(18, 7, 18, 14)),
    ]


@icon("dreamcatcher", CAT, "Hoop with a woven web inside and feathers hanging from strings below.",
      tags=["dream catcher", "native american", "boho", "bohemian", "sleep", "feathers", "wall hanging"])
def _(S):
    return [
        shell(circle(12, 9, 6.5)),
        detail(circle(12, 9, 2.6)),
        line(seg(8, 14.3, 7.3, 16.4)), line(seg(12, 15.5, 12, 17.4)), line(seg(16, 14.3, 16.7, 16.4)),
        solid(ellipse(7, 18.7, 1.4, 2.3)), solid(ellipse(12, 19.6, 1.4, 2.3)), solid(ellipse(17, 18.7, 1.4, 2.3)),
    ]


@icon("macrame-wall-hanging", CAT, "Knotted cord wall hanging draped from a wooden dowel with a diamond knot pattern and fringe.",
      tags=["macrame", "boho wall art", "woven hanging", "fiber art", "knotted rope", "wall decor", "bohemian"])
def _(S):
    return [
        line(seg(3, 3.5, 21, 3.5)),
        dot(3, 3.5, 1.6), dot(21, 3.5, 1.6),
        line(seg(6, 3.5, 6, 20.5)), line(seg(18, 3.5, 18, 20.5)),
        line(seg(12, 3.5, 12, 6.5)),
        shell(poly([(12, 6.5), (15, 11), (12, 15.5), (9, 11)], closed=True, r=S.r * 0.5)),
        line(seg(12, 15.5, 12, 21)),
    ]


@icon("wall-tapestry", CAT, "Large woven textile hanging from a rod with a diamond pattern and tassels along the bottom edge.",
      tags=["tapestry", "wall hanging", "fabric art", "woven wall art", "textile", "bohemian", "wall decor"])
def _(S):
    return [
        line(seg(3, 2.5, 21, 2.5)),
        dot(3, 2.5, 1.6), dot(21, 2.5, 1.6),
        shell(rect(5, 5.5, 14, 13, rr(S, 1.5))),
        detail(poly([(12, 8), (15.5, 12), (12, 16), (8.5, 12)], closed=True, r=S.r * 0.5)),
        line(seg(7.5, 18.5, 7.5, 21.5)), line(seg(12, 18.5, 12, 21.5)), line(seg(16.5, 18.5, 16.5, 21.5)),
    ]


@icon("wall-plate", CAT, "Decorative round plate with a floral center hung on a wall by a wire hanger.",
      tags=["decorative plate", "hanging plate", "plate wall", "china plate", "wall decor", "ceramic", "display plate"])
def _(S):
    return [
        line(poly([(8, 8.5), (12, 3), (16, 8.5)], r=S.r)),
        shell(circle(12, 14, 8)),
        detail(circle(12, 14, 4.6)),
        dot(12, 14, 1.3),
    ]


@icon("letter-board", CAT, "Felt letter board with rows of small letter tiles in a frame.",
      tags=["message board", "changeable letters", "felt board", "quote board", "menu board", "sign board"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, rr(S, 2))),
        sq(6, 6.5, 3, 4, 0.4), sq(10.5, 6.5, 3, 4, 0.4), sq(15, 6.5, 3, 4, 0.4),
        sq(8.25, 13, 3, 4, 0.4), sq(12.75, 13, 3, 4, 0.4),
    ]


@icon("cork-board", CAT, "Framed cork board with a pinned note and a photo held by push pins.",
      tags=["corkboard", "pin board", "notice board", "bulletin board", "memo board", "push pins", "office"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, rr(S, 2))),
        detail(rect(5.8, 8.5, 5, 6, rr(S, 0.8))),
        detail(rect(13.2, 7.5, 5, 8, rr(S, 0.8))),
        dot(8.3, 8.5, 1.2), dot(15.7, 7.5, 1.2),
    ]


@icon("triptych", CAT, "Three framed art panels hanging side by side, the middle one larger.",
      tags=["three panel art", "wall art", "gallery wall", "diptych", "canvas set", "art panels", "altarpiece"])
def _(S):
    return [
        shell(poly([(2.5, 7), (8, 7), (8, 4), (16, 4), (16, 7), (21.5, 7), (21.5, 17), (16, 17), (16, 20), (8, 20), (8, 17), (2.5, 17)],
                   closed=True, r=S.r * 0.5)),
        detail(seg(8, 7, 8, 17)), detail(seg(16, 7, 16, 17)),
        dot(12, 12, 2),
    ]
