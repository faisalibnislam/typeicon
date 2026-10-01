"""TypeIcon Core: festivities (holiday, ritual and cultural celebration objects), batch 5."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "festivities"


def L(S, a, b):
    return a if S.name == "line" else b


def rotp(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def P(*pts):
    return " ".join(f"{fmt(x)} {fmt(y)}" for x, y in pts)


def star(cx, cy, ro, ri, n=5, rot=-90.0):
    pts = []
    for i in range(n):
        pts.append(polar(cx, cy, ro, rot + 360 / n * i))
        pts.append(polar(cx, cy, ri, rot + 360 / n * i + 180 / n))
    return pts


# ============================================================================ chunk 1

@icon("vajra-bell", CAT, "Ritual hand bell with a flared body and a prong handle on top",
      tags=["bell", "ritual", "buddhist", "ceremony", "prayer", "handle", "temple"])
def _(S):
    return [
        shell(poly([(10, 10), (14, 10), (19, 19), (5, 19)], closed=True, r=S.r)),
        line("M12 10V3"),
        line("M8.5 4Q9 8 12 8.5Q15 8 15.5 4"),
        dot(12, 21.5, 1.2),
    ]


@icon("kransekake", CAT, "Cone tower of stacked ring cakes with a small flag on top",
      tags=["cake", "tower", "norwegian", "wedding", "ring cake", "dessert", "celebration"])
def _(S):
    return [
        shell(poly([(12, 7), (19, 21), (5, 21)], closed=True, r=S.r)),
        detail(seg(9.6, 12, 14.4, 12)),
        detail(seg(7.8, 16, 16.2, 16)),
        line("M12 7V2.5"),
        solid(poly([(12, 2.5), (16.5, 4), (12, 5.5)], closed=True)),
    ]


@icon("wedding-coins", CAT, "Small box with a stack of coins rising out of it, used in wedding coin ceremonies",
      tags=["coins", "wedding", "box", "ceremony", "treasure", "arras", "gift"])
def _(S):
    return [
        shell(rect(4, 14.5, 16, 7, min(S.R, 3))),
        shell(rect(7, 2.5, 10, 3.6, 1.8)),
        shell(rect(7, 5.9, 10, 3.6, 1.8)),
        shell(rect(7, 9.3, 10, 3.6, 1.8)),
    ]


@icon("turnip-lantern", CAT, "Round turnip lantern with a leaf top, carved eyes and a jagged mouth",
      tags=["turnip", "lantern", "halloween", "carved", "jack o lantern", "autumn", "glow"])
def _(S):
    return [
        shell("M12 20C7.5 20 4 17 4 12.5C4 8.5 7.5 6.5 12 6.5C16.5 6.5 20 8.5 20 12.5C20 17 16.5 20 12 20Z"),
        line("M12 6.5V3.5"),
        line("M12 4.5Q9.5 2.5 7.5 3.5"),
        line("M12 20V22.5"),
        dot(8.8, 11.5, 1.3),
        dot(15.2, 11.5, 1.3),
        detail("M8.5 15.5L10.2 17L12 15.5L13.8 17L15.5 15.5"),
    ]


@icon("icicle-ornament", CAT, "Long slender twisted drop ornament hanging from a cap",
      tags=["icicle", "ornament", "christmas", "drop", "spiral", "tree", "decoration"])
def _(S):
    return [
        shell(rect(10, 1.5, 4, 3, min(S.R, 1))),
        shell(poly([(12, 5.5), (15.5, 10), (12, 20), (8.5, 10)], closed=True, r=S.r)),
        detail(seg(10, 10.5, 14, 13)),
    ]


@icon("mustache-prop", CAT, "Drooping paper mustache on a thin stick for party photos",
      tags=["mustache", "moustache", "photo booth", "prop", "party", "stick", "costume"])
def _(S):
    return [
        shell("M12 8.5C10 6.8 7.5 7 5.8 8.6C4.6 9.6 3.3 8.8 3.6 6.8C2 10 3.8 13 7.6 13C9.6 13 11.3 12.2 12 11.4C12.7 12.2 14.4 13 16.4 13C20.2 13 22 10 20.4 6.8C20.7 8.8 19.4 9.6 18.2 8.6C16.5 7 14 6.8 12 8.5Z"),
        line("M12 12V22"),
    ]


@icon("selfie-frame-prop", CAT, "Hollow picture frame on a handle held up in front of a face",
      tags=["selfie", "frame", "photo booth", "prop", "party", "picture", "handle"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 13, S.R)),
        detail(rect(8, 6, 8, 6, min(S.R, 1.5))),
        line("M12 15.5V22"),
    ]


@icon("santa-beard", CAT, "Fluffy full beard with a curled mustache and ear loops",
      tags=["beard", "santa", "christmas", "costume", "mustache", "fake beard", "white beard"])
def _(S):
    return [
        shell("M4.5 6C5 9 6.5 10.5 9 10.5H15C17.5 10.5 19 9 19.5 6C21 12 18 21.5 12 21.5C6 21.5 3 12 4.5 6Z"),
        line("M4.5 6C2 6 1.5 3 4 2.5"),
        line("M19.5 6C22 6 22.5 3 20 2.5"),
        detail("M8 13.5Q10 11.5 12 13.5Q14 11.5 16 13.5"),
        dot(12, 17.5, 1.3),
    ]


@icon("tree-skirt", CAT, "Round tree skirt with a centre hole and a slit to the edge",
      tags=["tree skirt", "christmas", "tree", "fabric", "base", "decoration", "holiday"])
def _(S):
    return [
        shell(ellipse(12, 13, 10, 7.5)),
        detail(ellipse(12, 12, 3, 2) if S.name == "line" else circle(12, 12, 2.5)),
        detail(seg(12, 14, 12, 20.5)),
    ]


@icon("santa-claus", CAT, "Jolly face with a fur-trimmed hat, pompom, mustache and big beard",
      tags=["santa", "santa claus", "father christmas", "christmas", "face", "beard", "hat"])
def _(S):
    return [
        shell("M6.5 8.5L8 5Q11 2.5 15 3.5L17.5 8.5Z"),
        solid(circle(18.5, 3.5, 1.8)),
        shell(rect(5, 7.5, 14, 3, min(S.R, 1.5))),
        shell("M6.5 11C6 17.5 8.5 22 12 22C15.5 22 18 17.5 17.5 11Z"),
        dot(9.5, 13, 1),
        dot(14.5, 13, 1),
        detail("M8.5 17Q10.3 15 12 17Q13.7 15 15.5 17"),
    ]


@icon("shillelagh", CAT, "Knobbly walking stick with a rounded knot head and a ribbon bow",
      tags=["shillelagh", "irish", "walking stick", "cudgel", "st patricks", "stick", "cane"])
def _(S):
    return [
        shell(circle(16.5, 7.5, 4.5)),
        line("M13.5 10.5L4.5 21"),
        solid(poly([(9, 16.5), (4.4, 15.6), (7.4, 11.9)], closed=True)),
        solid(poly([(9, 16.5), (13.6, 17.4), (10.6, 21.1)], closed=True)),
    ]


@icon("fleur-de-lis", CAT, "Stylised lily with a tall centre petal, two curling side petals and a band",
      tags=["fleur de lis", "lily", "heraldry", "french", "royal", "emblem", "scout"])
def _(S):
    left = "M10.5 13C9 9 4 8.5 3.5 12.5C3.2 15.5 7.5 16 10 14"
    right = "M13.5 13C15 9 20 8.5 20.5 12.5C20.8 15.5 16.5 16 14 14"
    return [
        shell("M12 2C15 5 15.5 10 12 14.5C8.5 10 9 5 12 2Z"),
        line(left),
        line(right),
        shell(rect(7.5, 16, 9, 2.5, min(S.R, 1))),
        line("M9.5 18.5L8 22"),
        line("M14.5 18.5L16 22"),
    ]


@icon("maltese-cross", CAT, "Cross of four arrowhead arms, each notched with a V at its outer end",
      tags=["maltese cross", "cross", "knights", "emblem", "order", "badge", "symbol"])
def _(S):
    pts = [(8.5, 2), (12, 5.5), (15.5, 2), (14, 10), (22, 8.5), (18.5, 12), (22, 15.5), (14, 14),
           (15.5, 22), (12, 18.5), (8.5, 22), (10, 14), (2, 15.5), (5.5, 12), (2, 8.5), (10, 10)]
    pts = [(12 + (x - 12) * 0.86, 12 + (y - 12) * 0.86) for x, y in pts]
    return [shell(poly(pts, closed=True, r=max(S.r, 0.8) * 0.7))]


# ============================================================================ chunk 2

def mirror_d(pts):
    return [(24 - x, y) for x, y in pts]


@icon("sankofa", CAT, "Heart shape made of two mirrored spirals curling inward at the top",
      tags=["sankofa", "adinkra", "heart", "spiral", "african", "symbol", "return"])
def _(S):
    left = "M12 20.5C7 17.5 3.5 13.5 4 9.5C4.5 6 9 5 10.5 8C11.3 9.8 10 11 8.8 10.5"
    right = "M12 20.5C17 17.5 20.5 13.5 20 9.5C19.5 6 15 5 13.5 8C12.7 9.8 14 11 15.2 10.5"
    return [line(left), line(right)]


@icon("tiki-mug", CAT, "Tall carved mug with a stylised face, a handle and a straw",
      tags=["tiki", "mug", "cocktail", "tropical", "polynesian", "drink", "luau"])
def _(S):
    return [
        shell(poly([(5, 8), (16, 8), (15, 21), (6, 21)], closed=True, r=S.r)),
        line("M16 11H18.5Q20.5 11 20.5 13V15.5Q20.5 17.5 18.5 17.5H15.5"),
        line("M10 8L13.5 2.5"),
        dot(8.6, 12, 1.2),
        dot(12.4, 12, 1.2),
        detail(rect(8.3, 15.3, 4.4, 3, 0.5)),
    ]


@icon("party-tent", CAT, "Open-sided marquee tent with a peaked roof, scalloped edge and a pennant",
      tags=["tent", "marquee", "party", "wedding", "event", "canopy", "outdoor"])
def _(S):
    scallop = "M3 11" + "a1.8 1.8 0 0 0 3.6 0" * 5
    return [
        shell(poly([(12, 5), (21, 11), (3, 11)], closed=True, r=max(S.r, 1.2))),
        line(scallop),
        line("M4.5 13.5V21.5"),
        line("M19.5 13.5V21.5"),
        line("M12 5V1.5"),
        solid(poly([(12, 1.5), (16, 2.8), (12, 4.1)], closed=True)),
    ]


@icon("champagne-saber", CAT, "Bottle neck being opened with a curved saber as the cork flies off",
      tags=["champagne", "saber", "sabrage", "bottle", "celebration", "sparkling wine", "toast"])
def _(S):
    return [
        shell("M7 21.5H15V15Q15 12.5 13 11.5V7.5H9V11.5Q7 12.5 7 15Z"),
        line("M2.5 10Q10 2.5 19 6"),
        solid(circle(19.5, 11.5, 1.5)),
    ]


@icon("holy-water-sprinkler", CAT, "Short rod with a round perforated ball head flicking drops of water",
      tags=["aspergillum", "holy water", "sprinkler", "blessing", "church", "ritual", "drops"])
def _(S):
    return [
        line("M4.5 20.5L12 13"),
        shell(circle(15.5, 9.5, 4.5)),
        dot(14.3, 8.5, 0.9),
        dot(17, 10.8, 0.9),
        dot(21, 17, 1.2),
        dot(18, 20.5, 1.2),
        dot(21.5, 13, 1),
    ]


@icon("torah-ark", CAT, "Tall cabinet with a pointed top, double doors and a curtain valance",
      tags=["torah ark", "ark", "synagogue", "cabinet", "jewish", "scroll", "worship"])
def _(S):
    return [
        shell(poly([(12, 2.5), (19, 7), (19, 21.5), (5, 21.5), (5, 7)], closed=True, r=S.r)),
        detail(seg(5, 11, 19, 11)),
        detail(seg(12, 11, 12, 21.5)),
        dot(10.2, 16.5, 0.9),
        dot(13.8, 16.5, 0.9),
    ]


@icon("wedding-carriage", CAT, "Side view of a coach with a rounded cabin, a front seat and two wheels",
      tags=["carriage", "wedding", "coach", "horse drawn", "cinderella", "transport", "bride"])
def _(S):
    return [
        shell(rect(3.5, 3.5, 12, 9.5, L(S, 3, 5))),
        line("M15.5 9.5H21V14.5H3"),
        shell(circle(7.5, 18.5, 3)),
        shell(circle(17, 18.5, 3)),
    ]


@icon("tsoureki", CAT, "Braided sweet bread loaf with a dyed egg at one end",
      tags=["tsoureki", "easter bread", "greek", "braid", "egg", "bread", "bakery"])
def _(S):
    return [
        shell(rect(2, 6.5, 20, 11.5, L(S, 3, 5.5))),
        shell(ellipse(8, 12.2, 2, 2.6)),
        detail(seg(12, 17.3, 14, 7.2)),
        detail(seg(16.5, 17.3, 18.5, 7.2)),
    ]


@icon("hishi-mochi", CAT, "Diamond-shaped rice cake made of three stacked colour layers",
      tags=["hishi mochi", "rice cake", "diamond", "hinamatsuri", "japanese", "dessert", "layers"])
def _(S):
    return [
        shell(poly([(12, 2.5), (21.5, 12), (12, 21.5), (2.5, 12)], closed=True, r=S.r)),
        detail(seg(6.6, 8, 17.4, 8)),
        detail(seg(6.6, 16, 17.4, 16)),
    ]


@icon("yakgwa", CAT, "Flower-shaped honey cookie with scalloped petal edges and a seed in the centre",
      tags=["yakgwa", "korean", "honey cookie", "flower", "dessert", "scalloped", "sweet"])
def _(S):
    n = 8
    pts = [polar(12, 12, 9, 360 / n * i - 90 + 360 / n / 2) for i in range(n)]
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(1, n + 1):
        x, y = pts[i % n]
        d += f"A3.7 3.7 0 0 1 {fmt(x)} {fmt(y)}"
    return [shell(d + "Z"), dot(12, 12, 1.6)]


@icon("cinnamon-star-cookie", CAT, "Five-pointed star cookie with a smooth glaze on top",
      tags=["cinnamon star", "zimtstern", "cookie", "christmas", "star", "biscuit", "german"])
def _(S):
    return [
        shell(poly(star(12, 12.8, 10.5, 5, 5), closed=True, r=S.r)),
        detail(circle(12, 13, 2.2)),
    ]


@icon("krumkake", CAT, "Rolled cone-shaped wafer cookie with a fine grid pattern",
      tags=["krumkake", "wafer", "cone", "cookie", "norwegian", "rolled", "dessert"])
def _(S):
    return [
        shell(poly([(3, 21), (14, 4), (20.5, 10.5)], closed=True, r=S.r * 0.7)),
        detail(seg(8, 13.3, 11, 16.4)),
        detail(seg(11, 8.8, 15, 12.8)),
        detail(seg(3.5, 20.5, 16.5, 7.5)),
    ]


@icon("struffoli", CAT, "Mound of small fried dough balls stacked in a pyramid on a plate",
      tags=["struffoli", "honey balls", "fried dough", "italian", "christmas", "pyramid", "dessert"])
def _(S):
    return [
        shell(circle(6.5, 16.5, 2.8)),
        shell(circle(12, 16.5, 2.8)),
        shell(circle(17.5, 16.5, 2.8)),
        shell(circle(9.2, 10.8, 2.8)),
        shell(circle(14.8, 10.8, 2.8)),
        shell(circle(12, 5.3, 2.8)),
        line("M3 21.5H21"),
    ]


@icon("pashka", CAT, "Truncated pyramid of pressed cheese dessert with a raised cross",
      tags=["pashka", "paskha", "easter", "cheese dessert", "russian", "cross", "pyramid"])
def _(S):
    return [
        shell(poly([(7, 4), (17, 4), (21, 20.5), (3, 20.5)], closed=True, r=S.r)),
        detail(seg(12, 8, 12, 16.5)),
        detail(seg(9, 11, 15, 11)),
    ]


# ============================================================================ chunk 3

def rpath(cmds, deg, cx=12.0, cy=12.0):
    """Path from commands ("M", p) ("L", p) ("C", p1, p2, p3) ("Z",) with every point rotated clockwise by deg."""
    out = []
    for c in cmds:
        if c[0] == "Z":
            out.append("Z")
        else:
            out.append(c[0] + P(*rotp(list(c[1:]), deg, cx, cy)))
    return "".join(out)


@icon("qatayef", CAT, "Small pancake folded into a half-moon, with crushed nuts along its open edge",
      tags=["qatayef", "katayef", "ramadan", "pancake", "arabic", "dessert", "stuffed"])
def _(S):
    return [
        shell("M3 15.5A9 8.5 0 0 1 21 15.5Z"),
        detail("M7.5 12.5Q12 8.5 16.5 12.5"),
        dot(6, 19.5, 1.1),
        dot(10, 20.5, 1.1),
        dot(14, 19.5, 1.1),
        dot(18, 20.5, 1.1),
    ]


@icon("kunafa", CAT, "Round tray of shredded pastry with a slice cut out to show the filling layer",
      tags=["kunafa", "knafeh", "kanafeh", "pastry", "cheese", "arabic", "dessert"])
def _(S):
    a = polar(12, 12, 9, -80)
    b = polar(12, 12, 9, -10)
    return [
        shell(circle(12, 12, 9)),
        detail(f"M{P(a)}L12 12L{P(b)}"),
        detail(arc(12, 12, 5.2, -72, -18)) if S.name == "line" else detail(arc(12, 12, 3.6, -72, -18)),
    ] + ([] if S.name == "line" else [detail(arc(12, 12, 7, -68, -22))])


@icon("church-altar", CAT, "Altar table with a draped cloth, a small cross in the middle and a candle on each side",
      tags=["altar", "church", "cross", "candles", "communion", "worship", "sanctuary"])
def _(S):
    return [
        shell(rect(3, 12, 18, 9.5, min(S.R, 1.5))),
        detail(seg(3, 16.5, 21, 16.5)),
        line("M12 2.5V9.5"),
        line("M10 4.8H14"),
        line("M5.5 8.5V12"),
        dot(5.5, 5.8, 1.1),
        line("M18.5 8.5V12"),
        dot(18.5, 5.8, 1.1),
    ]


@icon("tabernacle", CAT, "Small domed cabinet with a cross on top and a pair of front doors",
      tags=["tabernacle", "church", "cabinet", "sanctuary", "doors", "cross", "altar"])
def _(S):
    return [
        shell("M5 21.5V11C5 7.5 8 6 12 6C16 6 19 7.5 19 11V21.5Z"),
        line("M12 6V2"),
        line("M10.3 3.6H13.7"),
        detail(seg(12, 10, 12, 21.5)),
        dot(10, 15.5, 0.9),
        dot(14, 15.5, 0.9),
    ]


@icon("marigold-flower", CAT, "Ruffled round marigold flower head on a short stem with a leaf",
      tags=["marigold", "flower", "cempasuchil", "day of the dead", "blossom", "garden", "orange"])
def _(S):
    n = 8
    pts = [polar(12, 9, 6.8, 360 / n * i - 90 + 360 / n / 2) for i in range(n)]
    d = f"M{P(pts[0])}"
    for i in range(1, n + 1):
        d += f"A2.7 2.7 0 0 1 {P(pts[i % n])}"
    return [
        shell(d + "Z"),
        detail(circle(12, 9, 1.9)),
        line("M12 17.5V22"),
        line("M12 20.5Q16 19 18.5 20.5Q15.5 22.5 12 20.5"),
    ]


@icon("pussy-willow-branch", CAT, "Slender upright twig with soft oval buds spaced along it",
      tags=["pussy willow", "willow", "branch", "spring", "easter", "palm sunday", "catkin"])
def _(S):
    return [
        line("M12 22V3"),
        shell(ellipse(8.6, 17, 2, 2.8)),
        shell(ellipse(15.4, 13, 2, 2.8)),
        shell(ellipse(8.6, 9, 2, 2.8)),
        shell(ellipse(15.4, 5.2, 2, 2.6)),
    ]


@icon("shinto-offering-branch", CAT, "Leafy evergreen sprig with a zigzag folded paper streamer tied on",
      tags=["sakaki", "shinto", "offering", "shide", "branch", "japanese", "shrine"])
def _(S):
    return [
        line("M12 22V3.5"),
        shell("M12 9.5C8 9.5 5.5 7 5.5 4C9 4 12 6 12 9.5Z"),
        shell("M12 9.5C16 9.5 18.5 7 18.5 4C15 4 12 6 12 9.5Z"),
        shell("M12 16C8.5 16 6.5 14 6.5 11.5C9.5 11.5 12 13 12 16Z"),
        line("M12 14H17.5"),
        line("M17.5 14L15.5 16.3L19 18.3L16.5 21"),
    ]


@icon("noh-mask", CAT, "Smooth oval theatre mask with narrow eye slits, high painted brows and small lips",
      tags=["noh", "mask", "japanese theatre", "theater", "performance", "face", "traditional"])
def _(S):
    outline = L(S,
                "M12 2.5C17 2.5 19 6 19 11C19 15.5 15 19 12 21.5C9 19 5 15.5 5 11C5 6 7 2.5 12 2.5Z",
                "M12 2.5C17 2.5 19 6 19 11C19 17 15.5 21.5 12 21.5C8.5 21.5 5 17 5 11C5 6 7 2.5 12 2.5Z")
    return [
        shell(outline),
        detail("M8 7.8Q9.5 6.6 11 7.8"),
        detail("M13 7.8Q14.5 6.6 16 7.8"),
        detail("M8 11.3Q9.5 12.3 11 11.3"),
        detail("M13 11.3Q14.5 12.3 16 11.3"),
        detail("M10.2 16.5Q12 17.5 13.8 16.5"),
    ]


@icon("luchador-mask", CAT, "Full head wrestling mask with round eye holes, a mouth opening and a V brow mark",
      tags=["luchador", "lucha libre", "wrestling", "mask", "mexican", "wrestler", "hood"])
def _(S):
    return [
        shell("M12 2.5C17 2.5 19.5 6 19.5 11C19.5 17 16 21.5 12 21.5C8 21.5 4.5 17 4.5 11C4.5 6 7 2.5 12 2.5Z"),
        detail("M7.5 6L12 9L16.5 6"),
        dot(8.7, 11.5, 1.7),
        dot(15.3, 11.5, 1.7),
        detail(ellipse(12, 17, 2.4, 1.4)),
    ]


@icon("bouzouki", CAT, "Long-necked lute with a pear-shaped bowl, a round sound hole and a pegbox",
      tags=["bouzouki", "greek", "lute", "string instrument", "music", "folk", "strings"])
def _(S):
    body = rpath([("M", (12, 11)), ("C", (8, 11), (6.3, 14.5), (6.3, 17)), ("C", (6.3, 20.3), (9, 22), (12, 22)),
                  ("C", (15, 22), (17.7, 20.3), (17.7, 17)), ("C", (17.7, 14.5), (16, 11), (12, 11)), ("Z",)], 38, 12, 12)
    neck = rpath([("M", (12, 11)), ("L", (12, 4.5))], 38, 12, 12)
    peg = poly(rotp([(10.3, 1.2), (13.7, 1.2), (13.7, 4.5), (10.3, 4.5)], 38), closed=True, r=S.r * 0.4)
    hole = rotp([(12, 17)], 38)[0]
    return [shell(body), line(neck), shell(peg), dot(hole[0], hole[1], 1.5)]


@icon("qanun", CAT, "Flat trapezoid zither seen from above with parallel strings and a row of small levers",
      tags=["qanun", "kanun", "zither", "string instrument", "arabic", "music", "psaltery"])
def _(S):
    return [
        shell(poly([(2.5, 19.5), (21.5, 19.5), (21.5, 5.5), (9.5, 5.5)], closed=True, r=S.r * 0.8)),
        detail(seg(12.5, 5.5, 12.5, 19.5)),
        detail(seg(16, 5.5, 16, 19.5)),
        dot(19, 9, 0.9),
        dot(19, 12.3, 0.9),
        dot(19, 15.6, 0.9),
    ]


@icon("chasuble", CAT, "Front view of a wide sleeveless vestment with a Y-shaped band down the front",
      tags=["chasuble", "vestment", "priest", "mass", "church", "robe", "liturgical"])
def _(S):
    return [
        shell(L(S, "M9 3Q12 5.5 15 3L20 8.5Q21.5 15 19.5 21.5H4.5Q2.5 15 4 8.5Z", "M9 3Q12 5.5 15 3L20 8.5Q21.5 15 19.5 20Q12 23.5 4.5 20Q2.5 15 4 8.5Z")),
        detail("M9 4.5L12 12"),
        detail("M15 4.5L12 12"),
        detail("M12 12V21.5"),
    ]


@icon("balloon-pump", CAT, "Hand pump with a T-handle plunger inflating a balloon on its nozzle",
      tags=["balloon pump", "inflator", "party", "air pump", "inflate", "balloon", "decorations"])
def _(S):
    return [
        shell(rect(4.5, 10, 6, 11.5, min(S.R, 1.5))),
        line("M7.5 10V4.5"),
        line("M4 4H11"),
        line("M10.5 18H17V15.8"),
        shell(ellipse(17, 10.6, 3.8, 5)),
    ]


@icon("stacked-sake-cups", CAT, "Three shallow flat cups stacked in shrinking sizes on a small foot",
      tags=["sake", "cups", "ochoko", "sakazuki", "ceremony", "japanese", "stacked"])
def _(S):
    return [
        shell(poly([(3, 14.5), (21, 14.5), (19, 19), (5, 19)], closed=True, r=S.r)),
        shell(poly([(6, 9.8), (18, 9.8), (16.8, 13), (7.2, 13)], closed=True, r=S.r * 0.6)),
        shell(poly([(8.5, 5.2), (15.5, 5.2), (14.8, 8), (9.2, 8)], closed=True, r=S.r * 0.4)),
        line("M8 21.5H16"),
    ]


@icon("straw-mobile", CAT, "Hanging geometric mobile of straw tubes forming a double pyramid on a thread",
      tags=["himmeli", "straw mobile", "hanging", "ornament", "finnish", "christmas", "geometric"])
def _(S):
    return [
        line("M12 1.5V4"),
        shell(poly([(12, 4), (19.5, 12), (12, 20), (4.5, 12)], closed=True, r=S.r)),
        detail("M4.5 12L12 15L19.5 12"),
        detail(seg(12, 4, 12, 15)),
        line("M12 20V22.5"),
    ]


# ============================================================================ chunk 4

@icon("nian-gao", CAT, "Round flat sticky rice cake with a red date on top",
      tags=["nian gao", "new year cake", "sticky rice cake", "chinese new year", "lunar", "dessert", "date"])
def _(S):
    ry = L(S, 4.5, 5.5)
    return [
        shell(f"M3 9V15.5A9 {fmt(ry)} 0 0 0 21 15.5V9A9 {fmt(ry)} 0 0 0 3 9Z"),
        detail(ellipse(12, 9, 2.6, 1.2)),
    ]


@icon("crescent-garland", CAT, "String hung in a swag with a crescent moon and a star dangling from it",
      tags=["garland", "crescent", "moon", "star", "ramadan", "eid", "bunting"])
def _(S):
    return [
        line("M2.5 4Q12 9.5 21.5 4"),
        line("M8 6.3V10"),
        shell("M9.8 10.3A4.5 4.5 0 1 0 9.8 18.9A5.5 5.5 0 0 1 9.8 10.3Z"),
        line("M16.5 6.3V10"),
        shell(poly(star(16.5, 14.3, 4.3, 1.9), closed=True, r=S.r * 0.4)),
    ]


@icon("clip-on-tree-candle", CAT, "Small taper candle in a metal clip holder gripping a fir branch",
      tags=["candle", "tree candle", "clip", "christmas tree", "fir branch", "flame", "holder"])
def _(S):
    return [
        dot(12, 4.3, 1.5),
        shell(rect(9.5, 7, 5, 8, min(S.R, 1.5))),
        shell(poly([(7.5, 15.5), (16.5, 15.5), (14.5, 19), (9.5, 19)], closed=True, r=S.r * 0.6)),
        line("M2.5 21.5H21.5"),
    ]


@icon("tree-topper-finial", CAT, "Tall pointed glass spike ornament with a round bulb, sitting on a treetop",
      tags=["tree topper", "finial", "christmas tree", "spike", "ornament", "glass", "decoration"])
def _(S):
    return [
        shell(poly([(12, 1.5), (14, 10), (10, 10)], closed=True, r=S.r * 0.5)),
        shell(circle(12, 13.5, 3.5)),
        line("M6.5 22L12 18.5L17.5 22"),
    ]


@icon("bid-paddle", CAT, "Round auction paddle with a number on its face, raised on a short handle",
      tags=["bid paddle", "auction", "paddle", "bidder", "fundraiser", "gala", "number"])
def _(S):
    return [
        shell(circle(12, 8.5, 6.8)),
        detail("M10.3 7L12.5 5.5V11.5"),
        line("M12 15.5V22"),
    ]


@icon("santa-boot", CAT, "Side view of a tall boot with a furry cuff and a strap",
      tags=["santa", "boot", "christmas", "winter", "fur", "shoe", "footwear"])
def _(S):
    return [
        shell(poly([(7, 8), (14, 8), (14, 14), (20.5, 16.5), (20.5, 21.5), (7, 21.5)], closed=True, r=S.r)),
        shell(rect(5.5, 3, 10, 4.5, min(S.R, 2.2))),
        detail(seg(7, 12.5, 14, 12.5)),
    ]


@icon("thousand-year-candy", CAT, "Tall narrow paper bag with a bird mark and two long candy sticks poking out",
      tags=["chitose ame", "thousand year candy", "candy", "bag", "shichi go san", "japanese", "crane"])
def _(S):
    return [
        line("M10 8.5L8.5 2.5"),
        line("M14 8.5L15.5 2.5"),
        shell(poly([(6.5, 8.5), (17.5, 8.5), (16.5, 22), (7.5, 22)], closed=True, r=S.r * 0.6)),
        detail("M9 14.5L12 17.5L15 14.5"),
    ]


@icon("gudi-pole", CAT, "Tall pole topped with an upturned pot, a draped cloth and a leaf sprig",
      tags=["gudi padwa", "gudi", "pole", "pot", "marathi new year", "flag", "festival"])
def _(S):
    return [
        line("M12 22V6.5"),
        shell("M8 6.5C8 3 10 2 12 2C14 2 16 3 16 6.5Z"),
        shell(poly([(12, 9), (20, 9), (18, 12), (20, 15), (12, 15)], closed=True, r=S.r * 0.5)),
        line("M12 19Q8 17.5 6 19.5Q9 21 12 19"),
    ]


@icon("moon-sieve", CAT, "Round mesh sieve held up in front of a full moon",
      tags=["sieve", "moon", "mid autumn", "strainer", "mesh", "viewing", "night"])
def _(S):
    return [
        shell(circle(10, 14, 8.3)),
        detail(seg(7, 8.5, 7, 19.5)),
        detail(seg(13, 8.5, 13, 19.5)),
        detail(seg(4.5, 11, 15.5, 11)),
        detail(seg(4.5, 17, 15.5, 17)),
        shell(circle(19, 5, 2.8)),
    ]


@icon("yusheng", CAT, "Platter of shredded salad strands lifted high by a pair of chopsticks",
      tags=["yusheng", "lo hei", "prosperity toss", "salad", "chinese new year", "chopsticks", "raw fish"])
def _(S):
    return [
        shell(ellipse(12, 18.5, 9.5, 3)),
        line("M8 17C7 13 10 11 9 7"),
        line("M12 17C12 13 14 11 13 6"),
        line("M16 17C15 14 17 12 16 8"),
        line("M3 3L11 11"),
        line("M6 2L15.5 9"),
    ]


@icon("straw-rope-wreath", CAT, "Twisted straw rope wreath with zigzag paper strips and an orange at the knot",
      tags=["shimenawa", "straw rope", "wreath", "new year", "japanese", "shide", "kadomatsu"])
def _(S):
    return [
        shell(circle(12, 10.5, 8)),
        detail(circle(12, 10.5, 4)),
        shell(circle(12, 20.5, 1.7)),
        line("M4.5 17.5L3 19.5L5.5 21"),
        line("M19.5 17.5L21 19.5L18.5 21"),
    ]


@icon("lucky-rice-scoop", CAT, "Woven scoop with a short handle hung upright by a cord with tassels",
      tags=["rice scoop", "lucky scoop", "shamoji", "woven", "tassels", "good fortune", "hanging"])
def _(S):
    return [
        line("M12 5V1.5"),
        shell(rect(10, 5, 4, 4, min(S.R, 1.2))),
        shell(poly([(5, 9), (19, 9), (17.5, 19), (6.5, 19)], closed=True, r=S.r)),
        detail(seg(12, 9, 12, 19)),
        detail(seg(5.6, 14, 18.4, 14)),
        line("M9.5 19V22"),
        line("M14.5 19V22"),
    ]


@icon("maamoul-mold", CAT, "Carved wooden paddle mold with a short handle and a round floral cavity",
      tags=["maamoul", "mold", "cookie mold", "date cookie", "paddle", "arabic", "baking"])
def _(S):
    return [
        shell(rect(5, 2, 14, 13, S.R * 0.75)),
        detail(circle(12, 8.5, 3.8)),
        dot(12, 8.5, 1),
        line("M12 15V22"),
    ]


@icon("moon-face-lantern", CAT, "Round paper lantern printed with a smiling moon face, hanging from a string",
      tags=["lantern", "moon", "mid autumn", "paper lantern", "face", "smile", "festival"])
def _(S):
    return [
        line("M12 4.5V1.5"),
        shell(rect(9.5, 4.5, 5, 2.5, min(S.R, 1))),
        shell(ellipse(12, 13.5, 8.3, 6.8)),
        dot(9, 12, 1.1),
        dot(15, 12, 1.1),
        detail("M8.8 15Q12 17.8 15.2 15"),
        line("M12 20.3V22.5"),
    ]


@icon("giant-round-kite", CAT, "Large round kite with a wheel pattern and a fringe of tassels below",
      tags=["kite", "round kite", "festival", "wheel", "tassels", "flying", "sky"])
def _(S):
    pts = [(polar(12, 10, 7.5, a), polar(12, 10, 7.5, a + 180)) for a in (0, 60, 120)]
    return [shell(circle(12, 10, 7.5))] + [detail(seg(p[0][0], p[0][1], p[1][0], p[1][1])) for p in pts] + [
        line("M9 18L8 21.5"), line("M12 18.5V22.5"), line("M15 18L16 21.5")]


@icon("wedding-glass-stomp", CAT, "Wine glass on the ground with a shoe sole raised above it, ready to be stomped",
      tags=["glass breaking", "jewish wedding", "stomp", "shoe", "wine glass", "mazel tov", "ceremony"])
def _(S):
    return [
        shell("M3.5 5.5Q3.5 3 6 3H17Q20.5 3 20.5 6V7H3.5Z"),
        shell(rect(3.5, 7, 4.5, 3, min(S.R, 1))),
        shell("M8 13.5H16Q16 18.5 12 18.5Q8 18.5 8 13.5Z"),
        line("M12 18.5V21.5"),
        line("M8.5 21.5H15.5"),
    ]


@icon("yule-lantern-candle", CAT, "Tall glass-paned lantern with a candle inside and a greenery sprig on its handle",
      tags=["lantern", "yule", "candle", "winter solstice", "greenery", "glass", "light"])
def _(S):
    return [
        line("M9 5Q12 0.8 15 5"),
        shell(poly([(5.5, 7.5), (8, 5), (16, 5), (18.5, 7.5)], closed=True, r=S.r * 0.6)),
        shell(rect(6.5, 7.5, 11, 14, min(S.R, 2))),
        dot(12, 11.5, 1.3),
        detail(seg(12, 14.5, 12, 21)),
        line("M15 3.8Q18 2 20 3.5Q17 5.5 15 3.8"),
    ]
