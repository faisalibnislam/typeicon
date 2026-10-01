"""TypeIcon Core: festivities (holiday, ritual and cultural celebration objects), batch 1."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from dsl import D, P
from geometry import fmt, path_to_d, polar

CAT = "festivities"


def L(S, a, b):
    return a if S.name == "line" else b


def flame(x, y, h=4.0, w=1.7):
    """Small solid flame with its base centre at (x, y)."""
    return solid(f"M{fmt(x)} {fmt(y - h)}C{fmt(x + w)} {fmt(y - h * 0.4)} {fmt(x + w)} {fmt(y)} {fmt(x)} {fmt(y)}"
                 f"C{fmt(x - w)} {fmt(y)} {fmt(x - w)} {fmt(y - h * 0.4)} {fmt(x)} {fmt(y - h)}Z")


def heart(S, cx=12.0, top=7.0, w=8.0, tip=20.5):
    """Heart made of two arcs and a tip (pointed in Line, rounded in Rounded)."""
    r = w * 0.6
    if S.name == "line":
        return (f"M{fmt(cx)} {fmt(tip)}L{fmt(cx - w)} {fmt(top + 5.5)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx)} {fmt(top)}"
                f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx + w)} {fmt(top + 5.5)}Z")
    return (f"M{fmt(cx - w)} {fmt(top + 5.5)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx)} {fmt(top)}"
            f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx + w)} {fmt(top + 5.5)}L{fmt(cx + 1.4)} {fmt(tip - 1.4)}"
            f"Q{fmt(cx)} {fmt(tip + 0.4)} {fmt(cx - 1.4)} {fmt(tip - 1.4)}Z")


def flame_k(x, y, h=4.0, w=1.7):
    """Flame knocked out of a shell it sits inside (solid outside any shell)."""
    return Part("dot", f"M{fmt(x)} {fmt(y - h)}C{fmt(x + w)} {fmt(y - h * 0.4)} {fmt(x + w)} {fmt(y)} {fmt(x)} {fmt(y)}"
                       f"C{fmt(x - w)} {fmt(y)} {fmt(x - w)} {fmt(y - h * 0.4)} {fmt(x)} {fmt(y - h)}Z")


def tilt(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def arch_doc(S, x0=5, x1=19, top=2.5, bot=21):
    r = (x1 - x0) / 2
    cx = (x0 + x1) / 2
    cy = top + r
    if S.name == "line":
        return f"M{fmt(x0)} {fmt(bot)}V{fmt(cy)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(cy)}V{fmt(bot)}Z"
    return (f"M{fmt(x0)} {fmt(cy)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(cy)}V{fmt(bot - 2)}A2 2 0 0 1 {fmt(x1 - 2)} {fmt(bot)}"
            f"H{fmt(x0 + 2)}A2 2 0 0 1 {fmt(x0)} {fmt(bot - 2)}Z")


def star(cx, cy, ro, ri, n=5, rot=-90.0):
    pts = []
    for i in range(n):
        pts.append(polar(cx, cy, ro, rot + 360 / n * i))
        pts.append(polar(cx, cy, ri, rot + 360 / n * i + 180 / n))
    return pts


# ============================================================================ christmas

@icon("christmas-stocking", CAT, "Hanging holiday stocking with a cuff at the top",
      tags=["christmas", "stocking", "xmas", "holiday", "sock", "gift", "santa"])
def _(S):
    return [
        shell(poly([(8, 8), (14, 8), (14, 12.5), (20, 14.5), (20, 20.5), (8, 20.5)], closed=True, r=S.r)),
        shell(rect(6.5, 4, 9, 4.5, min(S.R, 2))),
        detail(seg(8, 16, 12, 16)),
    ]


@icon("christmas-bauble", CAT, "Round tree ornament ball with a cap, hanging loop and a band",
      tags=["christmas", "ornament", "bauble", "decoration", "tree", "xmas", "ball"])
def _(S):
    return [
        line("M10.5 5V3.5a1.5 1.5 0 0 1 3 0V5"),
        shell(circle(12, 14.5, 7.5)),
        shell(rect(9, 5, 6, 3, min(S.R, 1))),
        detail(L(S, "M5.2 13.5Q12 17.5 18.8 13.5", "M5 14Q12 18 19 14")),
    ]


@icon("santa-hat", CAT, "Drooping cone hat with a fur brim and a pompom",
      tags=["santa", "christmas", "hat", "xmas", "cap", "winter", "holiday"])
def _(S):
    return [
        shell("M6 15.5C6.5 9 10 5 14.5 5C17.5 5 19 7 19 9.5L19 15.5Z" if S.name == "line" else
              "M6 15.5C6.5 9 10 5 14.5 5C17.5 5 19 7 19 9.5L19 15.5Z"),
        shell(rect(3.5, 15, 17, 5, min(S.R, 2.5))),
        shell(circle(19, 5, 2)),
    ]


@icon("nutcracker-soldier", CAT, "Standing toy soldier with a tall hat, jaw, belted jacket and legs",
      tags=["nutcracker", "christmas", "toy", "soldier", "ballet", "holiday", "figurine"])
def _(S):
    return [
        shell(poly([(9, 2.5), (15, 2.5), (15.5, 7), (8.5, 7)], closed=True, r=S.r * 0.5)),
        shell(rect(9, 7, 6, 5, min(S.R, 2))),
        line(seg(7, 13.5, 4.5, 17.5)),
        line(seg(17, 13.5, 19.5, 17.5)),
        shell(rect(7, 12, 10, 5.5, min(S.R, 2))),
        detail(seg(7, 15, 17, 15)),
        line(seg(9.5, 17.5, 9.5, 21)),
        line(seg(14.5, 17.5, 14.5, 21)),
        dot(11, 9.5, 0.9), dot(13, 9.5, 0.9),
    ]


@icon("star-of-bethlehem", CAT, "Tall four-pointed star with a long bottom ray and small rays between the points",
      tags=["christmas", "nativity", "star", "epiphany", "guiding star", "xmas", "holiday"])
def _(S):
    body = [(12, 2.8), (14, 10), (19, 12), (14, 14), (12, 21.2), (10, 14), (5, 12), (10, 10)]
    return [
        shell(poly(body, closed=True, r=S.r * 0.6), stroke_miterlimit="2.5"),
    ]


@icon("christmas-angel", CAT, "Angel in a bell-shaped gown with spread wings and a halo",
      tags=["angel", "christmas", "halo", "wings", "xmas", "holiday", "heavenly"])
def _(S):
    return [
        line(L(S, "M8 3.2a4 1.2 0 1 1 8 0a4 1.2 0 1 1 -8 0", "M8 3.2a4 1.2 0 1 1 8 0a4 1.2 0 1 1 -8 0")),
        shell(circle(12, 8, 2.5)),
        shell(poly([(12, 11), (16, 21), (8, 21)], closed=True, r=S.r)),
        line(poly([(10.3, 13), (5, 9.5), (3.5, 13.5), (9, 15.5)], r=S.r)),
        line(poly([(13.7, 13), (19, 9.5), (20.5, 13.5), (15, 15.5)], r=S.r)),
    ]


@icon("elf-hat", CAT, "Tall pointed hat with a zigzag brim and a bell on the curled tip",
      tags=["elf", "christmas", "hat", "bell", "pointed hat", "holiday", "costume"])
def _(S):
    return [
        shell(poly([(6, 17), (10, 6), (15, 4), (18, 17)], closed=True, r=S.r)),
        shell(poly([(4.5, 17), (7, 20.5), (9.5, 17), (12, 20.5), (14.5, 17), (17, 20.5), (19.5, 17)], closed=True, r=S.r * 0.4)),
        shell(circle(17, 6.5, 2)),
        line("M15 4Q17 3 17 4.5"),
    ]


@icon("christmas-sweater", CAT, "Crew-neck sweater with a zigzag band across the chest and a small tree",
      tags=["christmas", "sweater", "jumper", "ugly sweater", "knit", "holiday", "winter"])
def _(S):
    return [
        shell(poly([(9, 3.5), (3, 6), (2.5, 14), (6, 14.5), (6, 20.5), (18, 20.5), (18, 14.5), (21.5, 14), (21, 6), (15, 3.5)],
                   closed=True, r=S.r)),
        detail("M9 3.5a3 2.2 0 0 0 6 0"),
        detail(poly([(6, 13.5), (8, 11.5), (10, 13.5), (12, 11.5), (14, 13.5), (16, 11.5), (18, 13.5)])),
        detail(poly([(12, 15.5), (10.5, 18.5), (13.5, 18.5)], closed=True)),
    ]


@icon("eggnog", CAT, "Short mug filled with a foamy drink, a cinnamon stick and sprinkled dots",
      tags=["eggnog", "christmas", "drink", "holiday", "mug", "cinnamon", "beverage"])
def _(S):
    return [
        shell(rect(4, 9, 12, 11.5, min(S.R, 3))),
        line(L(S, "M16 11.5H18.5V16H16", "M16 11.5H18.5a1.5 1.5 0 0 1 1.5 1.5v1.5a1.5 1.5 0 0 1 -1.5 1.5H16")),
        line(seg(10, 6.5, 14.5, 2.5)),
        dot(8, 13, 0.9), dot(11.5, 15.5, 0.9), dot(12.5, 12.5, 0.9),
    ]


@icon("santa-sack", CAT, "Bulging drawstring sack tied at the neck with a wrapped present poking out",
      tags=["santa", "sack", "gifts", "christmas", "bag", "presents", "toy bag"])
def _(S):
    return [
        shell("M9.5 10.5C3 12 2.5 18 6 20.5H18C21.5 18 21 12 14.5 10.5Z"),
        line(poly([(9.5, 10.5), (7.5, 7.5)], r=0)),
        line(poly([(14.5, 10.5), (16.5, 7.5)], r=0)),
        shell(rect(10, 3, 4, 4, min(S.R, 1))),
        detail(seg(9.5, 14.5, 14.5, 14.5)),
    ]


@icon("fruitcake", CAT, "Slice of loaf cake dotted with fruit pieces and nuts",
      tags=["fruitcake", "christmas", "cake", "dessert", "holiday", "fruit", "baking"])
def _(S):
    return [
        shell(rect(3, 6.5, 18, 13, min(S.R, 3))),
        detail(L(S, "M3 10.5H21", "M3 10.5H21")),
        dot(7.5, 14.5, 1.1), dot(12, 13.5, 1.1), dot(16.5, 15, 1.1), dot(10, 17.5, 1.1), dot(14.5, 17.8, 0.9),
    ]


@icon("stollen", CAT, "Oblong folded loaf dusted with sugar dots and a round marzipan core at the cut end",
      tags=["stollen", "christmas", "bread", "german", "holiday", "baking", "cake"])
def _(S):
    return [
        shell(poly([(3, 18), (3.5, 12), (8, 8), (16, 8), (16, 18)], closed=True, r=S.r + 1)),
        shell("M16 8C21.5 8 21.5 18 16 18"),
        detail(circle(17.5, 13, 1.6) if S.name == "line" else circle(17.5, 13, 1.6)),
        dot(8, 13.5, 0.9), dot(11.5, 11.5, 0.9), dot(11.5, 15.5, 0.9),
    ]


@icon("tinsel-garland", CAT, "Looping tinsel strand draped in a swag between two hooks",
      tags=["tinsel", "garland", "christmas", "decoration", "strand", "festive", "party"])
def _(S):
    pts = []
    n = 36
    for i in range(n + 1):
        t = i / n
        ph = 2 * math.pi * 3 * t
        bx = 3.5 + 17 * t
        by = 6 + 8 * math.sin(math.pi * t)
        pts.append((bx + 2.6 * math.sin(ph), by - 2.6 * math.cos(ph) + 2.6))
    return [line(poly(pts, r=S.r * 0.3)), dot(3.5, 4.2, 1.3), dot(20.5, 4.2, 1.3)]


@icon("nativity-scene", CAT, "Stable roof over a manger crib of straw with a star above the peak",
      tags=["nativity", "christmas", "stable", "manger", "crib", "bethlehem", "holiday"])
def _(S):
    return [
        solid(poly(star(12, 4.5, 2.4, 1.0), closed=True)),
        line(poly([(3.5, 12), (12, 8), (20.5, 12)], r=S.r)),
        line(seg(5.5, 11.5, 5.5, 20.5)),
        line(seg(18.5, 11.5, 18.5, 20.5)),
        shell(poly([(8.5, 15), (15.5, 15), (16, 17.5), (14.5, 20.5), (9.5, 20.5), (8, 17.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("candle-arch", CAT, "Arched candle bridge with small candles and flames rising along the curve",
      tags=["candle arch", "schwibbogen", "christmas", "candles", "german", "winter", "lights"])
def _(S):
    parts = [line("M3 21H21"), line("M4.5 21V17a7.5 7.5 0 0 1 15 0V21")]
    for x in (4.5, 8.3, 12, 15.7, 19.5):
        y = 17 - math.sqrt(max(0, 56.25 - (x - 12) ** 2))
        if abs(x - 4.5) < 0.1 or abs(x - 19.5) < 0.1:
            y = 16
        parts.append(line(seg(x, y, x, y - 3.5)))
        parts.append(flame(x, y - 4.5, 2.2, 1.0))
    return parts


@icon("christmas-pyramid", CAT, "Tiered wooden carousel with a propeller on top and candles on the tiers",
      tags=["christmas pyramid", "weihnachtspyramide", "carousel", "candles", "german", "winter", "holiday"])
def _(S):
    return [
        shell(poly([(12, 5), (18.5, 2.5), (18.5, 7.5)], closed=True, r=S.r * 0.4)),
        shell(poly([(12, 5), (5.5, 2.5), (5.5, 7.5)], closed=True, r=S.r * 0.4)),
        line(seg(12, 5, 12, 12)),
        shell(rect(6.5, 11.5, 11, 3, min(S.R, 1.5))),
        line(seg(12, 14.5, 12, 18)),
        shell(rect(3, 17.5, 18, 4, min(S.R, 2))),
        line(seg(8, 11.5, 8, 9.5)), line(seg(16, 11.5, 16, 9.5)),
    ]


@icon("yule-goat", CAT, "Straw goat seen from the side with curved horns, a ribbon band and legs",
      tags=["yule goat", "julbock", "christmas", "straw", "scandinavian", "winter", "goat"])
def _(S):
    return [
        shell(poly([(4.5, 10), (14, 10), (16.5, 6.5), (21, 7), (21, 10.5), (17.5, 12), (17.5, 16), (4.5, 16)],
                   closed=True, r=S.r)),
        line("M16.5 6.5C15.5 3.5 17.5 2.5 19 3.5"),
        line(seg(7, 16, 7, 20.5)), line(seg(15, 16, 15, 20.5)),
        detail(seg(10.5, 10, 10.5, 16)),
    ]


@icon("straw-star-ornament", CAT, "Flat eight-pointed star woven from straw strips, bound at the centre",
      tags=["straw star", "christmas", "ornament", "himmeli", "scandinavian", "decoration", "star"])
def _(S):
    return [
        shell(poly(star(12, 12, 10, 4.2, n=8), closed=True, r=S.r * 0.5), stroke_miterlimit="2.5"),
        dot(12, 12, 1.4),
    ]


@icon("north-pole-sign", CAT, "Candy-striped pole with an arrow sign nailed near the top",
      tags=["north pole", "santa", "christmas", "candy cane", "sign", "arrow", "winter"])
def _(S):
    return [
        shell(rect(6, 4, 5, 17.5, min(S.R, 2))),
        detail(seg(6, 11, 11, 8.5)),
        detail(seg(6, 17, 11, 14.5)),
        shell(poly([(11, 3.5), (18.5, 3.5), (21.5, 6.5), (18.5, 9.5), (11, 9.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("gingerbread-heart-cookie", CAT, "Heart-shaped cookie with an iced inner border and a ribbon loop at the top",
      tags=["gingerbread", "heart", "cookie", "christmas", "biscuit", "ribbon", "baking"])
def _(S):
    return [
        shell(heart(S, 12, 8, 8.5, 21)),
        detail(heart(S, 12, 10.5, 4.2, 16.5)),
        line("M12 8C10.5 5.5 10.5 3 12 3C13.5 3 13.5 5.5 12 8"),
    ]


@icon("kiddush-cup", CAT, "Stemmed goblet with an engraved band on the bowl, standing on a small saucer",
      tags=["kiddush", "cup", "goblet", "shabbat", "jewish", "wine", "chalice"])
def _(S):
    return [
        shell(poly([(7, 3.5), (17, 3.5), (16.5, 9), (12, 13.5), (7.5, 9)], closed=True, r=S.r * 1.3)),
        detail(seg(7.5, 7, 16.5, 7)),
        line(seg(12, 13.5, 12, 18)),
        shell(rect(5, 18, 14, 3.5, min(S.R, 1.75))),
    ]


@icon("torah-scroll", CAT, "Open scroll wound on two rollers with knobbed handles and lines of text",
      tags=["torah", "scroll", "jewish", "synagogue", "parchment", "sefer", "reading"])
def _(S):
    return [
        line(seg(4.5, 5, 4.5, 19)), line(seg(19.5, 5, 19.5, 19)),
        dot(4.5, 3.6, 1.4), dot(4.5, 20.4, 1.4), dot(19.5, 3.6, 1.4), dot(19.5, 20.4, 1.4),
        shell(rect(7.5, 5, 9, 14, min(S.R, 2))),
        detail(seg(10, 9.5, 14, 9.5)),
        detail(seg(10, 14.5, 14, 14.5)),
    ]


@icon("mezuzah", CAT, "Slim tilted case mounted beside a door frame line, with a small emblem near the top",
      tags=["mezuzah", "jewish", "door", "blessing", "home", "judaism", "doorpost"])
def _(S):
    case = tilt([(9.5, 3.5), (14.5, 3.5), (14.5, 20.5), (9.5, 20.5)], 14)
    return [
        line(seg(20, 2.5, 20, 21.5)),
        shell(poly(case, closed=True, r=S.r * 0.6)),
        dot(*tilt([(12, 8)], 14)[0], 1.1),
    ]


@icon("havdalah-candle", CAT, "Braided candle with twisted strands and several wicks sharing one wide flame",
      tags=["havdalah", "candle", "braided", "shabbat", "jewish", "flame", "ceremony"])
def _(S):
    return [
        solid("M12 2.5C17 6 17 9 12 9C7 9 7 6 12 2.5Z"),
        line(seg(12, 9, 12, 10.5)),
        shell(rect(7.5, 10.5, 9, 11, min(S.R, 2.5))),
        detail(seg(7.5, 18, 16.5, 14)),
    ]


@icon("lulav-and-etrog", CAT, "Bundled palm frond with myrtle and willow sprigs beside an oval citron",
      tags=["lulav", "etrog", "sukkot", "citron", "palm", "jewish", "harvest"])
def _(S):
    return [
        shell(poly([(8, 2.5), (10.5, 13), (5.5, 13)], closed=True, r=S.r * 0.6)),
        line(seg(8, 13, 8, 21.5)),
        line(poly([(4, 15), (8, 18), (12, 15)], r=S.r * 0.5)),
        shell(ellipse(17.5, 16.5, 3.8, 4.6)),
        dot(17.5, 10.8, 1.0),
    ]


@icon("torah-pointer", CAT, "Slender reading rod with a knobbed end and a small hand pointing at the tip",
      tags=["yad", "torah pointer", "jewish", "reading", "pointer", "scroll", "synagogue"])
def _(S):
    return [
        line(seg(6, 18, 12.5, 11.5)),
        shell(circle(4.5, 19.5, 2)),
        shell(rect(11.5, 7, 5.5, 5.5, min(S.R, 2))),
        line(seg(17, 9, 21.5, 3.5)),
    ]


@icon("tzedakah-box", CAT, "Small box with a coin slot on top and a coin dropping in",
      tags=["tzedakah", "charity", "donation", "box", "coin", "jewish", "giving"])
def _(S):
    return [
        shell(circle(16, 5.5, 2.5)),
        shell(rect(3.5, 11.5, 17, 9.5, min(S.R, 3))),
        detail(seg(11.5, 14.5, 18.5, 14.5)),
        line(seg(6, 4.5, 6, 8)),
    ]


@icon("shabbat-candles", CAT, "Two candlesticks side by side each holding a lit taper",
      tags=["shabbat", "candles", "sabbath", "jewish", "candlestick", "friday night", "lit"])
def _(S):
    parts = []
    for x in (6.5, 17.5):
        parts += [
            flame(x, 7.5, 3.6, 1.5),
            line(seg(x, 8.5, x, 14)),
            shell(poly([(x - 3.5, 14), (x + 3.5, 14), (x + 1.5, 17.5), (x - 1.5, 17.5)], closed=True, r=S.r * 0.4)),
            line(seg(x, 17.5, x, 21)),
            line(seg(x - 3.2, 21, x + 3.2, 21)),
        ]
    return parts


@icon("chuppah", CAT, "Canopy cloth on four thin poles, the back poles shorter, with drapes at the corners",
      tags=["chuppah", "huppah", "wedding", "jewish", "canopy", "marriage", "ceremony"])
def _(S):
    return [
        shell("M3 4.5H21L19.5 8Q12 6 4.5 8Z"),
        line(seg(4.5, 8, 4.5, 21.5)),
        line(seg(19.5, 8, 19.5, 21.5)),
        line(seg(9.5, 7.3, 9.5, 16)),
        line(seg(14.5, 7.3, 14.5, 16)),
    ]


@icon("ketubah", CAT, "Upright document with an arched top, lines of text and two signature lines",
      tags=["ketubah", "marriage contract", "jewish", "wedding", "document", "certificate", "scroll"])
def _(S):
    return [
        shell(arch_doc(S)),
        detail(seg(8.5, 10, 15.5, 10)),
        detail(seg(8.5, 13.5, 15.5, 13.5)),
        detail(seg(8.5, 17.5, 11, 17.5)),
        detail(seg(13, 17.5, 15.5, 17.5)),
    ]


# ============================================================================ jewish (continued)

@icon("tefillin", CAT, "Small cube box with leather straps winding away from it in loops",
      tags=["tefillin", "phylacteries", "jewish", "prayer", "straps", "judaism", "morning prayer"])
def _(S):
    return [
        shell(rect(3.5, 3.5, 9, 9, min(S.R, 2))),
        detail(rect(6.5, 6.5, 3, 3, 0)),
        line("M12.5 8H17A3.5 3.5 0 0 1 17 15H8"),
        line("M8 12.5V21.5"),
    ]


@icon("tablets-of-the-law", CAT, "Two round-topped stone tablets side by side with short lines engraved on each",
      tags=["ten commandments", "tablets", "stone tablets", "sinai", "law", "moses", "shavuot"])
def _(S):
    return [
        shell(arch_doc(S, 3.5, 10.5, 3, 20.5)),
        shell(arch_doc(S, 13.5, 20.5, 3, 20.5)),
        detail(seg(5.8, 11, 8.2, 11)), detail(seg(5.8, 14.5, 8.2, 14.5)), detail(seg(5.8, 18, 8.2, 18)),
        detail(seg(15.8, 11, 18.2, 11)), detail(seg(15.8, 14.5, 18.2, 14.5)), detail(seg(15.8, 18, 18.2, 18)),
    ]


@icon("apple-and-honey", CAT, "Small honey pot with a dipper stick next to a round apple with a leaf",
      tags=["rosh hashanah", "apple", "honey", "jewish new year", "sweet", "honey pot", "dipper"])
def _(S):
    return [
        shell(rect(2.5, 12.5, 9, 8.5, min(S.R, 3))),
        shell(rect(3.5, 9.5, 7, 3, min(S.R, 1))),
        line(seg(7, 9.5, 7, 4.5)),
        dot(7, 3.6, 1.4),
        shell(circle(17, 15.5, 5)),
        line(seg(17, 10.5, 17, 8.5)),
        solid("M17.5 8.5C18 6 20 5.5 21.5 5.5C21.5 7.5 20 9 17.5 8.5Z"),
    ]


@icon("quran-stand", CAT, "Folding X-shaped wooden book rest holding an open book in the V at the top",
      tags=["quran", "rehal", "book stand", "islam", "reading", "prayer", "ramadan"])
def _(S):
    return [
        shell(poly([(3, 4.5), (12, 7.5), (21, 4.5), (21, 10), (12, 13), (3, 10)], closed=True, r=S.r * 0.6)),
        detail(seg(12, 7.5, 12, 13)),
        line(seg(7, 14.5, 17, 21.5)),
        line(seg(17, 14.5, 7, 21.5)),
    ]


@icon("mosque-lamp", CAT, "Hanging glass lamp with a flared neck and round body, suspended on three chains",
      tags=["mosque lamp", "ramadan", "hanging lamp", "islam", "islamic", "chain", "glass lamp"])
def _(S):
    return [
        dot(12, 2.8, 1.3),
        line(seg(12, 2.8, 6, 8.5)), line(seg(12, 2.8, 12, 8.5)), line(seg(12, 2.8, 18, 8.5)),
        shell("M5 8.5H19L16 12.5C21 15 19 19.5 12 19.5C5 19.5 3 15 8 12.5Z"),
        line(seg(10, 21.5, 14, 21.5)),
    ]


@icon("kaaba", CAT, "Cube draped in cloth seen from a corner with a decorated band around the upper part",
      tags=["kaaba", "mecca", "hajj", "umrah", "islam", "pilgrimage", "cube"])
def _(S):
    return [
        shell(poly([(12, 3), (21, 7), (21, 17.5), (12, 21.5), (3, 17.5), (3, 7)], closed=True, r=S.r * 2)),
        detail(poly([(3, 7), (12, 11), (21, 7)])),
        detail(seg(12, 11, 12, 21.5)),
        detail(poly([(3, 12), (12, 16), (21, 12)])),
    ]


@icon("bakhoor-burner", CAT, "Footed incense burner with a square cup on a flared base and wisps of smoke rising",
      tags=["bakhoor", "incense", "burner", "oud", "mabkhara", "fragrance", "arabic"])
def _(S):
    return [
        line("M10 6.5C8.5 5 11.5 4 10 2.5"),
        line("M14 6.5C12.5 5 15.5 4 14 2.5"),
        shell(rect(6, 9, 12, 4.5, min(S.R, 2))),
        shell(poly([(9.5, 13.5), (14.5, 13.5), (18, 21), (6, 21)], closed=True, r=S.r * 0.8)),
    ]


@icon("ketupat", CAT, "Diamond pouch of woven palm leaf strips in a checkered weave with two leaf tails on top",
      tags=["ketupat", "eid", "hari raya", "rice cake", "woven", "malay", "indonesian"])
def _(S):
    return [
        line(seg(12, 5.5, 9, 2.5)),
        line(seg(12, 5.5, 15, 2.5)),
        shell(poly([(12, 5.5), (20.5, 13.5), (12, 21.5), (3.5, 13.5)], closed=True, r=S.r * 0.6)),
        detail(seg(7.75, 9.5, 16.25, 17.5)),
        detail(seg(16.25, 9.5, 7.75, 17.5)),
    ]


@icon("rub-el-hizb", CAT, "Eight-pointed star made of two overlapping squares with a small circle at the centre",
      tags=["rub el hizb", "islamic star", "quran", "verse marker", "eight-pointed star", "islam", "octagram"])
def _(S):
    a = [(5.5, 5.5), (18.5, 5.5), (18.5, 18.5), (5.5, 18.5)]
    b = tilt(a, 45)
    return [
        shell(poly(a, closed=True, r=S.r * 0.7)),
        shell(poly(b, closed=True, r=S.r * 0.7)),
        dot(12, 12, 1.5),
    ]


@icon("crescent-lantern", CAT, "Hanging lantern topped with a small crescent moon and pierced panels on the body",
      tags=["ramadan", "fanous", "lantern", "crescent", "islamic", "eid", "moon"])
def _(S):
    cres = path_to_d(D(P(circle(12, 4.7, 2.7)), P(circle(12, 3.5, 2.3))))
    return [
        solid(cres),
        line(seg(12, 7.5, 12, 9)),
        shell(poly([(8, 9), (16, 9), (18, 12), (18, 19), (6, 19), (6, 12)], closed=True, r=S.r)),
        detail(seg(10, 9.5, 10, 18.5)), detail(seg(14, 9.5, 14, 18.5)),
        line(seg(10, 19, 10, 21.5)), line(seg(14, 19, 14, 21.5)),
    ]


@icon("diya", CAT, "Small clay oil lamp shaped like a shallow leaf-tipped bowl with a single flame",
      tags=["diya", "diwali", "oil lamp", "deepam", "clay lamp", "festival of lights", "flame"])
def _(S):
    return [
        flame(11, 10.5, 5.5, 2.4),
        shell("M3 12.5H17.5C19 12.5 20.5 11.5 21.5 9.5C21 15 17 19.5 11.5 19.5C6.5 19.5 3.5 16.5 3 12.5Z"),
    ]


@icon("kalash", CAT, "Round-bellied pot with a narrow neck topped with mango leaves and a coconut",
      tags=["kalash", "kalasha", "puja", "coconut", "mango leaves", "hindu", "auspicious"])
def _(S):
    return [
        shell("M9.5 11.5V12.5C4 14.5 4 20.5 12 20.5C20 20.5 20 14.5 14.5 12.5V11.5Z"),
        shell(poly([(9, 11.5), (4, 7), (10, 7.5)], closed=True, r=S.r * 0.5)),
        shell(poly([(15, 11.5), (20, 7), (14, 7.5)], closed=True, r=S.r * 0.5)),
        shell(circle(12, 6, 2.6)),
    ]


@icon("toran", CAT, "Horizontal door hanging with pointed leaf pendants dangling along the bottom edge",
      tags=["toran", "door hanging", "bandanwar", "diwali", "decoration", "hindu", "festive"])
def _(S):
    return [
        line(seg(2.5, 5, 21.5, 5)),
        shell(poly([(3, 7), (8, 7), (5.5, 16)], closed=True, r=S.r * 0.6)),
        shell(poly([(9.5, 7), (14.5, 7), (12, 19)], closed=True, r=S.r * 0.6)),
        shell(poly([(16, 7), (21, 7), (18.5, 16)], closed=True, r=S.r * 0.6)),
    ]


@icon("marigold-garland", CAT, "Hanging loop of round flower heads strung close together with a tassel at the bottom",
      tags=["marigold", "garland", "flower garland", "mala", "hindu", "festive", "wedding"])
def _(S):
    parts = []
    for deg in (22, 56, 90, 124, 158):
        x, y = polar(12, 3.5, 9.5, deg)
        parts.append(shell(circle(x, y, 1.75)))
    parts.append(line(seg(12, 15, 12, 19.5)))
    parts.append(dot(12, 20.8, 1.2) if S.name == "rounded" else Part("dot", rect(10.8, 19.8, 2.4, 2.2)))
    return parts


# ============================================================================ hindu and south asian

@icon("holi-color-powder", CAT, "Small bowl heaped with coloured powder with a burst of powder puffs above it",
      tags=["holi", "color powder", "gulal", "festival of colors", "hindu", "spring", "powder"])
def _(S):
    return [
        shell("M3.5 14.5H20.5C20 18.5 16.5 20.5 12 20.5C7.5 20.5 4 18.5 3.5 14.5Z"),
        line(L(S, "M6.5 14.5L9.5 11H14.5L17.5 14.5", "M6.5 14.5C7 11 9 10.5 12 10.5C15 10.5 17 11 17.5 14.5")),
        dot(6.5, 6.5, 1.4), dot(12, 4.2, 1.7), dot(17.5, 6.5, 1.4), dot(9.5, 8, 0.9), dot(15, 8.3, 0.9),
    ]


@icon("pichkari", CAT, "Long water squirter tube with a plunger handle at one end and a spray from the nozzle",
      tags=["pichkari", "holi", "water gun", "squirter", "spray", "hindu", "festival of colors"])
def _(S):
    return [
        line(seg(2.5, 12, 6, 12)),
        line(seg(2.5, 9, 2.5, 15)),
        shell(rect(6, 9.5, 10, 5, min(S.R, 2))),
        line(seg(16, 12, 18.5, 12)),
        dot(21, 9, 0.9), dot(21.4, 12, 0.9), dot(21, 15, 0.9),
    ]


@icon("rakhi", CAT, "Thread bracelet loop with a flower rosette on top",
      tags=["rakhi", "raksha bandhan", "bracelet", "thread", "sibling", "hindu", "festival"])
def _(S):
    return [
        line(circle(12, 14, 7.5)),
        shell(poly(star(12, 6.5, 5, 3.6, n=8), closed=True, r=S.r * 0.5), stroke_miterlimit="2.5"),
        dot(12, 6.5, 1.2),
    ]


@icon("puja-thali", CAT, "Round plate from above holding a small lamp flame and three small bowls",
      tags=["puja thali", "aarti thali", "worship plate", "hindu", "ritual", "diya", "offering"])
def _(S):
    def bowl(x, y):
        return detail(circle(x, y, 1.6)) if S.name == "rounded" else detail(rect(x - 1.4, y - 1.4, 2.8, 2.8))
    return [
        shell(circle(12, 12, 9.5)),
        bowl(12, 5.8), bowl(6.6, 15.4), bowl(17.4, 15.4),
        flame_k(12, 14, 4.6, 1.7),
    ]


@icon("star-lantern", CAT, "Five-pointed star-shaped paper lantern with two ribbon tails hanging below",
      tags=["star lantern", "paper lantern", "diwali", "akash kandil", "christmas", "parol", "decoration"])
def _(S):
    return [
        shell(poly(star(12, 9.5, 7.4, 3.6), closed=True, r=S.r * 0.6), stroke_miterlimit="2.2"),
        line("M10.5 15.5C9.5 18 11.5 19.5 10 21.8"),
        line("M13.5 15.5C14.5 18 12.5 19.5 14 21.8"),
    ]


def _stick(a, b, w):
    ax, ay = a
    bx, by = b
    d = math.dist(a, b)
    ux, uy = (bx - ax) / d, (by - ay) / d
    nx, ny = -uy * w / 2, ux * w / 2
    return [(ax + nx, ay + ny), (bx + nx, by + ny), (bx - nx, by - ny), (ax - nx, ay - ny)]


@icon("dandiya-sticks", CAT, "Pair of short decorated sticks crossed in an X with bands and small tassel ends",
      tags=["dandiya", "garba", "navratri", "sticks", "raas", "hindu", "dance"])
def _(S):
    return [
        shell(poly(_stick((5.5, 18.5), (18, 6), 3.6), closed=True, r=S.r * 0.4)),
        shell(poly(_stick((5.5, 5.5), (18, 18), 3.6), closed=True, r=S.r * 0.4)),
        dot(20.3, 3.7, 1.3), dot(3.7, 3.7, 1.3), dot(20.3, 20.3, 1.3), dot(3.7, 20.3, 1.3),
    ]


@icon("standing-oil-lamp", CAT, "Tall brass lamp on a round base with a slim stem and a top dish holding five flames",
      tags=["deepastambha", "samai", "oil lamp", "brass lamp", "hindu", "lamp", "diwali"])
def _(S):
    parts = [flame(x, 8, 3.4, 1.15) for x in (6, 9, 12, 15, 18)]
    parts += [
        shell(poly([(4.5, 9.5), (19.5, 9.5), (17, 12.5), (7, 12.5)], closed=True, r=S.r * 0.6)),
        line(seg(12, 12.5, 12, 18.5)),
        shell(poly([(7.5, 18.5), (16.5, 18.5), (18, 21.5), (6, 21.5)], closed=True, r=S.r * 0.6)),
    ]
    return parts


@icon("aarti-lamp", CAT, "Handheld tiered lamp with rows of small flames rising in a cone and a short handle",
      tags=["aarti", "arti", "lamp", "hindu", "ritual", "flame", "worship"])
def _(S):
    parts = [flame(12, 5.5, 3, 1.2), flame(9.5, 9.5, 3, 1.2), flame(14.5, 9.5, 3, 1.2),
             flame(7, 13.5, 3, 1.2), flame(12, 13.5, 3, 1.2), flame(17, 13.5, 3, 1.2)]
    parts += [
        shell(poly([(4, 14.5), (20, 14.5), (17.5, 17.5), (6.5, 17.5)], closed=True, r=S.r * 0.6)),
        line(seg(12, 17.5, 12, 21.5)),
    ]
    return parts


@icon("pongal-pot", CAT, "Clay pot on three stones with froth boiling over the rim and a sugarcane stalk beside it",
      tags=["pongal", "pot", "boiling over", "harvest", "sugarcane", "tamil", "thai pongal"])
def _(S):
    return [
        line("M5.5 10.5C4.5 7.5 7.5 7 8.5 8.5C9 6 12.5 6 13 8.5C14 7 16 7.5 14 10.5"),
        shell("M5 10.5C2.5 13 2.5 18.5 9.5 18.5C16.5 18.5 16.5 13 14 10.5Z"),
        dot(5.5, 20.6, 1.3), dot(9.5, 20.8, 1.3), dot(13.5, 20.6, 1.3),
        line(seg(19, 21.5, 21, 4.5)),
    ]


@icon("snake-boat", CAT, "Very long narrow boat with a tall upswept stern and a row of oars along the side",
      tags=["snake boat", "chundan vallam", "onam", "boat race", "kerala", "rowing", "vallam kali"])
def _(S):
    return [
        shell("M2 14H17C19 14 20.5 12 21.5 7.5C21.5 15 18.5 18 14 18H6C3.5 18 2.5 16.5 2 14Z"),
        dot(6, 10.5, 1.2), dot(10, 10.5, 1.2), dot(14, 10.5, 1.2),
        line(seg(7, 15, 4.5, 21.5)), line(seg(11, 15, 8.5, 21.5)), line(seg(15, 15, 12.5, 21.5)),
    ]


@icon("dahi-handi", CAT, "Clay pot hanging from a rope high above a human pyramid of stacked heads",
      tags=["dahi handi", "janmashtami", "krishna", "human pyramid", "govinda", "pot", "hindu"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 5)),
        shell("M7.5 6.5C4.5 9 5 12 12 12C19 12 19.5 9 16.5 6.5Z"),
        dot(8.5, 16.3, 1.6), dot(15.5, 16.3, 1.6),
        dot(5, 20.6, 1.6), dot(12, 20.6, 1.6), dot(19, 20.6, 1.6),
    ]


@icon("evil-eye-bead", CAT, "Round flat bead with concentric rings and a dark centre, like a watchful eye, on a short cord",
      tags=["evil eye", "nazar", "amulet", "bead", "protection", "charm", "talisman"])
def _(S):
    return [
        line("M10 7.5C8.8 4 10.2 2.5 12 2.5C13.8 2.5 15.2 4 14 7.5"),
        shell(circle(12, 14.5, 7.5)),
        detail(circle(12, 14.5, 4.2)),
        dot(12, 14.5, 1.7) if S.name == "rounded" else Part("dot", rect(10.4, 12.9, 3.2, 3.2)),
    ]


@icon("trishul", CAT, "Three-pronged trident with a small drum tied on the shaft and a long handle",
      tags=["trishula", "trident", "shiva", "hindu", "damaru", "mahashivratri", "spear"])
def _(S):
    return [
        line("M6.5 5.5V9A5.5 5.5 0 0 0 17.5 9V5.5"),
        line(seg(12, 5, 12, 21.5)),
        solid("M12 2L10.3 5.5H13.7Z"), solid("M6.5 2L4.8 5.5H8.2Z"), solid("M17.5 2L15.8 5.5H19.2Z"),
        shell(poly([(9, 13.5), (15, 13.5), (13, 16.5), (15, 19.5), (9, 19.5), (11, 16.5)], closed=True, r=S.r * 0.3)),
    ]


@icon("shehnai", CAT, "Slender reed pipe with finger holes along the body and a wide flared bell",
      tags=["shehnai", "oboe", "wedding", "indian", "wind instrument", "reed pipe", "music"])
def _(S):
    def pts(ps):
        return tilt(ps, 30)
    holes = tilt([(12, 8.5), (12, 11.5), (12, 14.5)], 30)
    return [
        line(poly(tilt([(12, 2.5), (12, 5.5)], 30))),
        shell(poly(pts([(9.8, 5.5), (14.2, 5.5), (14.2, 16), (9.8, 16)]), closed=True, r=S.r * 0.4)),
        shell(poly(pts([(9.8, 16), (14.2, 16), (17, 20.5), (7, 20.5)]), closed=True, r=S.r * 0.5)),
        *[dot(x, y, 0.75) for x, y in holes],
    ]


@icon("mandap", CAT, "Four pillars supporting a domed canopy with a finial, for a wedding ceremony",
      tags=["mandap", "wedding canopy", "hindu wedding", "pavilion", "ceremony", "indian", "pillars"])
def _(S):
    return [
        shell("M4 10A8 8 0 0 1 20 10Z"),
        dot(12, 1.9, 0.9),
        line(seg(5.5, 10, 5.5, 21)), line(seg(9.5, 10, 9.5, 21)), line(seg(14.5, 10, 14.5, 21)), line(seg(18.5, 10, 18.5, 21)),
        line(seg(3, 21.5, 21, 21.5)),
    ]


# ============================================================================ buddhist

@icon("prayer-wheel", CAT, "Handheld prayer wheel: a cylinder on a stick with a weight on a chain swinging around it",
      tags=["prayer wheel", "mani wheel", "tibetan", "buddhist", "spinning", "mantra", "meditation"])
def _(S):
    return [
        line(seg(9.5, 2.5, 9.5, 5)),
        shell(rect(5.5, 5, 8, 9, min(S.R, 2.5))),
        line(seg(9.5, 14, 9.5, 21.5)),
        line(seg(13.5, 9.5, 17.5, 9.5)),
        dot(19.5, 9.5, 1.7),
        line("M15 4.5Q19.5 2.5 21.5 5.5"),
    ]


@icon("prayer-flags", CAT, "String of small square flags hanging from a line strung diagonally across",
      tags=["prayer flags", "tibetan", "buddhist", "bunting", "lungta", "himalaya", "flags"])
def _(S):
    parts = [line(seg(2.5, 4.5, 21.5, 9.5))]
    for x0 in (3.5, 10, 16.5):
        y = 4.5 + (x0 + 1.8 - 2.5) * 5 / 19 + 1.5
        parts.append(shell(rect(x0, y, 3.6, 7, min(S.R, 1))))
    return parts


@icon("butter-lamp", CAT, "Short stemmed metal cup with a wide bowl holding a small upright flame",
      tags=["butter lamp", "tibetan", "buddhist", "offering", "lamp", "temple", "flame"])
def _(S):
    return [
        flame(12, 10, 5.5, 2.3),
        shell("M4.5 11.5H19.5C19.5 16 16.5 18 12 18C7.5 18 4.5 16 4.5 11.5Z"),
        line(seg(12, 18, 12, 20.5)),
        line(seg(8, 21.5, 16, 21.5)),
    ]


@icon("alms-bowl", CAT, "Round lidded bowl on a small ring stand, seen from the side",
      tags=["alms bowl", "begging bowl", "monk", "buddhist", "patra", "offering", "bowl"])
def _(S):
    return [
        line("M6 12.5A6 6 0 0 1 18 12.5"),
        dot(12, 4.3, 1.2),
        shell("M3.5 12.5H20.5C20 17 16.5 19 12 19C7.5 19 4 17 3.5 12.5Z"),
        shell(poly([(8.5, 19), (15.5, 19), (16.5, 21.5), (7.5, 21.5)], closed=True, r=S.r * 0.3)),
    ]


@icon("vajra", CAT, "Symmetric ritual object with a central grip and two identical flared ends of curved prongs",
      tags=["vajra", "dorje", "thunderbolt", "buddhist", "tibetan", "ritual", "tantric"])
def _(S):
    def end(flip):
        def y(v):
            return 24 - v if flip else v
        return [line(f"M10 {fmt(y(9.5))}C5 {fmt(y(9))} 5.5 {fmt(y(4.5))} 12 {fmt(y(2.5))}"),
                line(f"M14 {fmt(y(9.5))}C19 {fmt(y(9))} 18.5 {fmt(y(4.5))} 12 {fmt(y(2.5))}"),
                line(seg(12, y(9.5), 12, y(2.5)))]
    return end(False) + end(True) + [shell(rect(9.5, 9.5, 5, 5, min(S.R, 2.5)))]


@icon("lotus-lantern", CAT, "Paper lantern shaped like a lotus flower with layered pointed petals and a small flame glow",
      tags=["lotus lantern", "vesak", "buddha's birthday", "lotus", "paper lantern", "buddhist", "yeondeung"])
def _(S):
    return [
        shell("M12 3.5C16 7.5 16 13.5 12 18.5C8 13.5 8 7.5 12 3.5Z"),
        flame_k(12, 14.5, 5, 1.8),
        shell("M11 18.5C6 18 3 14.5 3 10C8 10 10.5 13 11 18.5Z"),
        shell("M13 18.5C18 18 21 14.5 21 10C16 10 13.5 13 13 18.5Z"),
        line(seg(8, 21.5, 16, 21.5)),
    ]


def _horn_pt(x, y):
    """Local horn coordinates (x along the tube, y across) to the canvas, tube running to the top right."""
    k = math.sqrt(0.5)
    return (3.5 + (x + y) * k, 20.5 + (-x + y) * k)


@icon("tibetan-long-horn", CAT, "Very long telescoping horn laid diagonally with banded sections and a wide flared end",
      tags=["dungchen", "tibetan horn", "long horn", "buddhist", "monastery", "trumpet", "ritual"])
def _(S):
    body = [_horn_pt(0, -1), _horn_pt(13, -1.6), _horn_pt(15, -1.6), _horn_pt(21, -4),
            _horn_pt(21, 4), _horn_pt(15, 1.6), _horn_pt(13, 1.6), _horn_pt(0, 1)]
    bands = [(_horn_pt(6.5, -1.2), _horn_pt(6.5, 1.2)), (_horn_pt(10, -1.4), _horn_pt(10, 1.4))]
    return [shell(poly(body, closed=True, r=S.r * 0.5), stroke_miterlimit="2.5")] + \
           [detail(seg(a[0], a[1], b[0], b[1])) for a, b in bands]


@icon("endless-knot", CAT, "Interlaced knot of continuous ribbon forming right-angled loops with no beginning or end",
      tags=["endless knot", "eternal knot", "srivatsa", "buddhist", "tibetan", "infinity", "auspicious"])
def _(S):
    r = S.r * 2
    return [
        line(poly([(18.2, 8), (21, 8), (21, 16), (10.2, 16)], r=r)),
        line(poly([(5.8, 16), (3, 16), (3, 8), (13.8, 8)], r=r)),
        line(poly([(8, 10.2), (8, 21), (16, 21), (16, 18.2)], r=r)),
        line(poly([(16, 13.8), (16, 3), (8, 3), (8, 5.8)], r=r)),
    ]


# ============================================================================ east asian

@icon("firecracker-string", CAT, "Vertical string of small cylinder firecrackers hanging in pairs from a cord with a lit fuse",
      tags=["firecrackers", "chinese new year", "bao zhu", "string", "fuse", "lunar new year", "fireworks"])
def _(S):
    parts = [line(seg(12, 2.5, 12, 18))]
    for y0 in (4.5, 11.5):
        parts += [shell(rect(4.5, y0, 4.5, 5.5, min(S.R, 1.5))), shell(rect(15, y0, 4.5, 5.5, min(S.R, 1.5))),
                  line(seg(9, y0 + 2.75, 12, y0 + 2.75)), line(seg(15, y0 + 2.75, 12, y0 + 2.75))]
    parts += [line(seg(12, 18, 12, 20.5)), dot(12, 21.3, 1.0)]
    return parts


@icon("chinese-knot", CAT, "Decorative cord knot tilted like a diamond with a loop on top and a tassel below",
      tags=["chinese knot", "zhongguo jie", "lucky knot", "tassel", "lunar new year", "cord", "decoration"])
def _(S):
    return [
        line("M12 7C9.5 4.5 9.5 2.5 12 2.5C14.5 2.5 14.5 4.5 12 7"),
        shell(poly([(12, 7), (19, 12.5), (12, 18), (5, 12.5)], closed=True, r=S.r * 0.6)),
        detail(poly([(12, 10.5), (15, 12.5), (12, 14.5), (9, 12.5)], closed=True)),
        solid("M12 18L14 21.8H10Z"),
    ]


@icon("spring-couplets", CAT, "Two tall vertical paper banners side by side with a short horizontal banner above them",
      tags=["couplets", "chunlian", "spring festival", "lunar new year", "banner", "red paper", "calligraphy"])
def _(S):
    return [
        shell(rect(3.5, 8.5, 5.5, 13, min(S.R, 1.5))),
        shell(rect(15, 8.5, 5.5, 13, min(S.R, 1.5))),
        shell(rect(6.5, 2.5, 11, 4, min(S.R, 1.5))),
        dot(6.25, 12.5, 0.8), dot(6.25, 16, 0.8), dot(17.75, 12.5, 0.8), dot(17.75, 16, 0.8),
        detail(seg(9.5, 4.5, 14.5, 4.5)),
    ]


@icon("rabbit-lantern", CAT, "Paper lantern shaped like a sitting rabbit with long ears, on small wheels",
      tags=["rabbit lantern", "mid-autumn", "moon festival", "bunny", "paper lantern", "wheels", "lunar"])
def _(S):
    return [
        line(seg(14.5, 7.5, 13.5, 2.5)), line(seg(18, 7.5, 19, 2.5)),
        shell(circle(16.2, 10.5, 3.3)),
        shell(ellipse(10.5, 15, 7, 4.7)),
        dot(7, 20.5, 1.5), dot(14, 20.5, 1.5),
    ]


@icon("bagua-mirror", CAT, "Octagonal frame with trigram strokes on each side around a small round mirror",
      tags=["bagua", "feng shui", "trigram", "octagon", "mirror", "chinese", "protection"])
def _(S):
    parts = [shell(poly(regular(12, 12, 10.2, 8, start=-112.5), closed=True, r=S.r * 0.5)), shell(circle(12, 12, 2.3))]
    for i in range(8):
        a = -90 + 45 * i
        cx, cy = polar(12, 12, 6.6, a)
        tx, ty = -math.sin(math.radians(a)), math.cos(math.radians(a))
        parts.append(detail(seg(cx - tx * 1.25, cy - ty * 1.25, cx + tx * 1.25, cy + ty * 1.25)))
    return parts


@icon("incense-censer", CAT, "Round tripod bronze bowl with two upright handles and incense sticks standing in it",
      tags=["censer", "incense burner", "joss sticks", "temple", "tripod", "bronze", "prayer"])
def _(S):
    return [
        line(seg(10, 10, 9, 3)), line(seg(12, 10, 12, 2.5)), line(seg(14, 10, 15, 3)),
        line(seg(4.5, 11, 4.5, 8)), line(seg(19.5, 11, 19.5, 8)),
        shell("M3.5 10.5H20.5C20 15.5 17 17.5 12 17.5C7 17.5 4 15.5 3.5 10.5Z"),
        line(seg(8, 17, 6.5, 21.5)), line(seg(16, 17, 17.5, 21.5)), line(seg(12, 17.5, 12, 21.5)),
    ]


@icon("koinobori", CAT, "Carp-shaped windsock flying horizontally from a pole, with a round eye and scale arcs",
      tags=["koinobori", "carp streamer", "children's day", "windsock", "japan", "kodomo no hi", "fish flag"])
def _(S):
    return [
        line(seg(3, 2.5, 3, 21.5)),
        shell("M5 7.5C9.5 6 14 7.5 17 11L21.5 7.5V16.5L17 13C14 16.5 9.5 18 5 16.5Z"),
        dot(8.5, 11, 1.1),
        detail("M12.5 9.5Q14 12 12.5 14.5"),
    ]


@icon("kagami-mochi", CAT, "Two stacked round rice cakes on a small stand, topped with a small orange and leaf",
      tags=["kagami mochi", "new year", "japan", "rice cake", "offering", "mochi", "shogatsu"])
def _(S):
    return [
        solid("M12.6 3.4C13 1.8 14.8 1.6 15.8 2.2C15.4 3.6 14 4.2 12.6 3.4Z"),
        shell(circle(12, 5, 2.1)),
        shell("M7 12.5C7 9 9 7.6 12 7.6C15 7.6 17 9 17 12.5Z"),
        shell("M4 18C4 14 7 12.8 12 12.8C17 12.8 20 14 20 18Z"),
        shell(poly([(6, 18.6), (18, 18.6), (17, 21.2), (7, 21.2)], closed=True, r=S.r)),
    ]


@icon("daruma-doll", CAT, "Round weighted doll with a face window, one eye filled in and one left blank",
      tags=["daruma", "wish doll", "japan", "luck", "goal", "new year", "eye"])
def _(S):
    return [
        shell("M12 3C5.5 3 3 10 3 14.5C3 19 7 21 12 21C17 21 21 19 21 14.5C21 10 18.5 3 12 3Z"),
        detail(rect(6.5, 7, 11, 7, S.R)),
        dot(9.5, 10.5, 1.2),
        detail(circle(14.5, 10.5, 1.3)),
        detail(seg(9, 17.5, 15, 17.5)),
    ]


@icon("omamori", CAT, "Small fabric charm pouch with a knotted cord loop at the top and a band of pattern",
      tags=["omamori", "amulet", "charm", "shrine", "japan", "protection", "lucky charm"])
def _(S):
    return [
        line("M9.5 7C8 3.5 10 2.5 12 4.5C14 2.5 16 3.5 14.5 7"),
        shell(rect(6.5, 7, 11, 14.5, min(S.R, 3))),
        detail(seg(6.5, 11.5, 17.5, 11.5)),
        detail(poly([(12, 14), (14, 16.5), (12, 19), (10, 16.5)], closed=True)),
    ]


@icon("ema-plaque", CAT, "Five-sided wooden plaque with a pointed top, a cord loop and writing lines",
      tags=["ema", "wish plaque", "shrine", "japan", "prayer", "wooden plaque", "shinto"])
def _(S):
    return [
        line("M12 8C10.5 5.5 10.5 2.5 12 2.5C13.5 2.5 13.5 5.5 12 8"),
        shell(poly([(3.5, 12), (12, 7), (20.5, 12), (20.5, 21), (3.5, 21)], closed=True, r=S.r)),
        detail(seg(8, 14.5, 16, 14.5)),
        detail(seg(8, 17.5, 14, 17.5)),
    ]


@icon("shimenawa", CAT, "Thick twisted straw rope hanging horizontally with zigzag paper streamers dangling from it",
      tags=["shimenawa", "shinto", "sacred rope", "shide", "japan", "shrine", "straw rope"])
def _(S):
    parts = [shell(rect(2.5, 4.5, 19, 5, min(S.R, 2.5))),
             detail(seg(7, 4.5, 9, 9.5)), detail(seg(12, 4.5, 14, 9.5)), detail(seg(17, 4.5, 19, 9.5))]
    for x in (6.5, 12, 17.5):
        parts.append(line(poly([(x, 9.5), (x + 1.7, 12.5), (x - 1.7, 15.5), (x + 1.7, 18.5), (x - 1.2, 21)], r=S.r * 0.3)))
    return parts
