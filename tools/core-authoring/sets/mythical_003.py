"""TypeIcon Core: mythical (batch 3) - fairy tales, witchcraft, alchemy and magical places and objects."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "mythical"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12, cy=12):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def flip(d):
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def pg(pts, S, r=None):
    """Closed polygon, filleted in Rounded."""
    return poly(pts, closed=True, r=S.r if r is None else r)


def mark(d):
    return Part("dot", d)


def sparkle(cx, cy, r, w=None):
    """Four-point sparkle as a small solid star."""
    w = r * 0.28 if w is None else w
    return poly([(cx, cy - r), (cx + w, cy - w), (cx + r, cy), (cx + w, cy + w), (cx, cy + r),
                 (cx - w, cy + w), (cx - r, cy), (cx - w, cy - w)], closed=True)


# --------------------------------------------------------------------------- witchcraft

@icon("witch-hat", CAT, "Wide-brimmed pointed hat with a bent tip and a hatband",
      tags=["witch", "hat", "halloween", "wizard", "costume", "magic", "brim"])
def _(S):
    cone = pg([(7.5, 17), (10, 8.5), (12.5, 4), (17, 3), (15, 7.5), (16.5, 17)], S)
    brim = ellipse(12, 18, 10, L(S, 3, 3.2))
    return [shell(union(cone, brim)), detail(seg(8.6, 13.2, 15.6, 13.2))]


@icon("flying-witch", CAT, "A witch in a pointed hat riding a broomstick past a crescent moon",
      tags=["witch", "broom", "broomstick", "halloween", "flying", "magic", "moon"])
def _(S):
    moon = minus(circle(5.5, 6, 3.8), circle(7.5, 4.8, 3.3))
    stick = seg(8, 19, 22, 16.5)
    bristles = pg([(2.5, 16.5), (8.5, 19), (2.5, 21.5)], S, r=S.r * 0.4)
    body = pg([(12, 17), (13, 11), (18.5, 11), (19, 16)], S, r=S.r * 0.6)
    hat = pg([(11.5, 9), (15.5, 2.5), (19.5, 9)], S, r=S.r * 0.6)
    brim = ellipse(15.5, 9.5, 6, 1)
    return [shell(moon), line(stick), shell(bristles), shell(union(body, hat, brim))]


@icon("wizard-staff", CAT, "Tall wooden staff with curled branches at the top holding a round orb",
      tags=["wizard", "staff", "magic", "orb", "sorcerer", "fantasy", "mage"])
def _(S):
    def t(x, y, deg=35):
        a = math.radians(deg)
        x -= 12
        y -= 12
        return (fmt(12 + x * math.cos(a) - y * math.sin(a)) + " " + fmt(12 + x * math.sin(a) + y * math.cos(a)))

    def tp(x, y, deg=35):
        a = math.radians(deg)
        x -= 12
        y -= 12
        return (12 + x * math.cos(a) - y * math.sin(a), 12 + x * math.sin(a) + y * math.cos(a))
    shaft = f"M{t(12, 22.5)}L{t(12, 11.5)}"
    prongs = f"M{t(6.5, 3.5)}Q{t(6.5, 11.5)} {t(12, 11.5)}Q{t(17.5, 11.5)} {t(17.5, 3.5)}"
    ox, oy = tp(12, 6.5)
    sx, sy = tp(12, 0.3)
    return [line(shaft), line(prongs), shell(circle(ox, oy, 2.4)), mark(sparkle(sx, sy, 1.7, 0.4))]


@icon("mandrake", CAT, "Root plant pulled from the soil with leaves on top and a screaming human-shaped root",
      tags=["mandrake", "root", "plant", "herb", "screaming", "witchcraft", "magic", "potion"])
def _(S):
    body = union(ellipse(12, 13, 4.6, L(S, 5, 5.2)),
                 pg([(8.6, 16), (8, 22), (10.6, 22), (12, 18.5), (13.4, 22), (16, 22), (15.4, 16)], S, r=S.r * 0.5))
    c = pg([(12, 8), (10.3, 5), (12, 2), (13.7, 5)], S, r=S.r * 0.5)
    l1 = pg([(10.5, 8), (5.5, 7), (5, 4), (9.5, 5)], S, r=S.r * 0.5)
    l2 = pg([(13.5, 8), (18.5, 7), (19, 4), (14.5, 5)], S, r=S.r * 0.5)
    return [shell(union(body, c, l1, l2)), dot(10.3, 12, 0.9), dot(13.7, 12, 0.9), dot(12, 15.2, 1.2)]


@icon("magic-circle", CAT, "Ritual circle with an inscribed triangle and rune dots",
      tags=["ritual", "summoning", "circle", "occult", "witchcraft", "sigil", "spell", "pentacle"])
def _(S):
    tri = poly(regular(12, 12, 7.6, 3), closed=True, r=S.r)
    ds = [dot(12 + 6.3 * math.cos(math.radians(a)), 12 + 6.3 * math.sin(math.radians(a)), 1.0) for a in (90, 210, 330)]
    return [shell(circle(12, 12, 9)), detail(tri)] + ds


@icon("alchemy-symbol", CAT, "Squared circle emblem: a circle in a triangle in a square in a circle",
      tags=["alchemy", "philosopher's stone", "squared circle", "emblem", "hermetic", "occult", "symbol"])
def _(S):
    a = 9.5 / math.sqrt(2)
    sq = pg([(12 - a, 12 - a), (12 + a, 12 - a), (12 + a, 12 + a), (12 - a, 12 + a)], S, r=S.r * 0.5)
    tri = pg([(12 - a, 12 + a), (12 + a, 12 + a), (12, 12 - a)], S, r=S.r * 0.5)
    return [shell(circle(12, 12, 9.5)), detail(sq), detail(tri), detail(circle(12, 14.8, 1.8))]


@icon("alembic", CAT, "Glass still with a round flask, domed head and a spout running to a small receiving flask",
      tags=["alchemy", "distillation", "still", "chemistry", "lab", "retort", "flask", "potion"])
def _(S):
    still = union(circle(8, 16, 4.6), rect(6.5, 8.5, 3, 6), circle(8, 7.5, 3.2))
    spout = "M10.6 6L18 9.5V14"
    recv = pg([(16, 14.5), (20, 14.5), (20.5, 21), (15.5, 21)], S, r=S.r * 0.6)
    return [shell(still), line(spout), shell(recv), detail(seg(4.3, 16.5, 11.7, 16.5))]


@icon("crystal-skull", CAT, "Front view of a faceted crystal skull with angular facets and hollow eyes",
      tags=["skull", "crystal", "artifact", "relic", "mystic", "quartz", "facets", "legend"])
def _(S):
    sk = pg([(12, 2), (17.5, 3.6), (20, 8.5), (18.5, 13), (16.5, 15), (16.5, 20), (7.5, 20), (7.5, 15), (5.5, 13), (4, 8.5), (6.5, 3.6)], S, r=S.r * 0.6)
    eyes = [mark(poly([(7.5, 9), (11, 9), (9.5, 12.2)], closed=True)), mark(poly([(13, 9), (16.5, 9), (14.5, 12.2)], closed=True))]
    return [shell(sk)] + eyes + [detail(poly([(12, 13), (11, 15), (13, 15)], closed=True)), detail(seg(10.2, 17.5, 10.2, 20)),
                                  detail(seg(13.8, 17.5, 13.8, 20)), detail(seg(12, 2, 12, 5.5))]


@icon("crystal-pendulum", CAT, "Pointed six-sided crystal hanging from a chain and swinging with arc marks",
      tags=["pendulum", "crystal", "dowsing", "divination", "quartz", "spiritual", "chain", "swing"])
def _(S):
    cr = pg([(12, 9), (15.5, 11.5), (15.5, 16.5), (12, 22), (8.5, 16.5), (8.5, 11.5)], S, r=S.r * 0.6)
    return [line("M12 2V9"), shell(cr), detail(seg(8.5, 11.5, 15.5, 16.5)), line(arc(12, 2, 18, 58, 74)), line(arc(12, 2, 18, 106, 122))]


@icon("dowsing-rod", CAT, "Forked stick held by two hands with its tip pointing down at water",
      tags=["dowsing", "divining rod", "water witching", "water", "groundwater", "forked stick", "divination"])
def _(S):
    y = "M5 5L12 12V16M19 5L12 12"
    waves = "M4 18.8q2 -2 4 0t4 0t4 0t4 0"
    return [line(y), dot(5, 4.5, 1.9), dot(19, 4.5, 1.9), line(waves), line("M8 22q2 -2 4 0t4 0")]


@icon("palm-reading", CAT, "Open palm facing forward with heart, head and life lines across it",
      tags=["palmistry", "palm", "fortune", "fortune teller", "hand", "psychic", "divination", "lines"])
def _(S):
    fingers = [rect(6.3, 4.5, 2.8, 9, 1.4), rect(9.3, 2.5, 2.8, 11, 1.4), rect(12.3, 3, 2.8, 10.5, 1.4), rect(15.3, 5.5, 2.8, 8, 1.4)]
    palm = rect(6.3, 9, 11.8, 12, L(S, 2, 4))
    thumb = rot(rect(2.5, 11.5, 2.8, 7, 1.4), -35, 4, 15)
    return [shell(union(palm, *fingers, thumb)), detail("M9 13q3 -1.5 6 .5"), detail("M9.5 16.5q3 -1 5.5 .5")]


# --------------------------------------------------------------------------- fairy tales

@icon("magic-mirror", CAT, "Oval framed wall mirror with a small finial and sparkles in the glass",
      tags=["mirror", "magic", "fairy tale", "enchanted", "looking glass", "sparkle", "fantasy"])
def _(S):
    fin = mark(poly([(12, 0.8), (13.4, 2.6), (12, 4.4), (10.6, 2.6)], closed=True)) if S.name == "line" else dot(12, 2.6, 1.3)
    return [shell(ellipse(12, 13, 7.6, L(S, 8.6, 8.4))), detail(ellipse(12, 13, 4.4, 5.4)), fin,
            mark(sparkle(11, 11.5, 1.8, 0.5)), mark(sparkle(13.4, 15.5, 1.1, 0.3))]


@icon("wishing-well", CAT, "Round stone well with a small peaked roof, posts and a hanging bucket",
      tags=["well", "wish", "water", "fairy tale", "stone", "bucket", "garden"])
def _(S):
    wall = rect(4, 14.5, 16, 7, L(S, 1, 3))
    roof = pg([(4.5, 8), (12, 2.5), (19.5, 8)], S)
    return [shell(wall), shell(roof), line("M7.5 8V14.5M16.5 8V14.5"), line("M12 8V10.5"), shell(rect(10.4, 10.5, 3.2, 2.6, 0.6))]


@icon("fairy-house", CAT, "Mushroom cap roof over a small round-doored house in the stalk",
      tags=["fairy", "mushroom", "house", "toadstool", "cottage", "gnome", "fantasy", "home"])
def _(S):
    cap = "M3 12A9 8.5 0 0 1 21 12Z"
    stalk = rect(7.5, 12, 9, 9.5, L(S, 1, 3))
    return [shell(cap), shell(stalk), detail("M10.5 21.5V17.5a1.5 1.5 0 0 1 3 0V21.5"), dot(8, 8.4, 1.1), dot(14.3, 6.3, 1.1), dot(17, 9.6, 0.9)]


@icon("magic-portal", CAT, "Upright oval doorway with a swirl inside and sparkles around its rim",
      tags=["portal", "gateway", "swirl", "vortex", "fantasy", "dimension", "teleport", "magic door"])
def _(S):
    return [shell(ellipse(12, 12, 7.6, 9.6)), detail("M10.5 12a1.5 1.5 0 0 1 3 0a3 3 0 0 1 -6 0a4.5 4.5 0 0 1 9 0"),
            mark(sparkle(2.8, 3.6, 1.8, 0.5)), mark(sparkle(21.2, 20.4, 1.8, 0.5))]


@icon("enchanted-rose", CAT, "Single rose with a falling petal under a glass bell jar on a base",
      tags=["rose", "enchanted", "bell jar", "fairy tale", "flower", "glass dome", "beauty", "cloche"])
def _(S):
    dome = "M5.5 19V11a6.5 6.5 0 0 1 13 0V19"
    base = rect(3.5, 18.5, 17, 3.5, L(S, 1, 1.7))
    return [line(dome), shell(base), shell(circle(12, 9.6, 2.8)), line("M12 12.4V18"), line("M12 16Q9.2 15.6 8.6 13.4"), dot(15.6, 15.6, 0.9), dot(12, 2.4, 1.0)]


@icon("glass-slipper", CAT, "Side view of a delicate high-heeled shoe with a facet line and a sparkle",
      tags=["slipper", "shoe", "cinderella", "glass", "high heel", "fairy tale", "ball", "crystal"])
def _(S):
    shoe = pg([(4, 6), (8.4, 6.6), (11, 11), (16, 14), (21, 17.5), (21, 20), (16, 20), (11.5, 17.2), (9.2, 16.6), (8.4, 22), (6.2, 22), (5.2, 15)], S, r=S.r * 0.7)
    return [shell(shoe), detail(seg(10.8, 12.4, 12.6, 16)), mark(sparkle(16.5, 6.5, 2.6, 0.65))]


@icon("magic-beanstalk", CAT, "Twisting bean vine with large leaves climbing up into a cloud",
      tags=["beanstalk", "jack", "giant", "vine", "fairy tale", "cloud", "beans", "plant"])
def _(S):
    cloud = union(circle(8, 6, 2.4), circle(12.6, 5, 3.3), circle(16.6, 6.4, 2.4), rect(8, 6, 8.6, 2.8))
    stem = "M11.5 22C8 19.5 15 17 11.5 13.5C9.5 11.7 13.5 10.8 12 9.6"
    lf1 = pg([(9.4, 18.5), (6.5, 14.4), (3, 17.4), (6, 20.6)], S, r=S.r * 0.6)
    lf2 = pg([(13.6, 15.4), (16.5, 11.4), (20.5, 14.4), (17.5, 17.6)], S, r=S.r * 0.6)
    return [shell(cloud), line(stem), shell(lf1), shell(lf2)]


@icon("poison-apple", CAT, "Apple with a bite taken out and a small skull face on its skin",
      tags=["apple", "poison", "fairy tale", "snow white", "bite", "skull", "witch", "cursed"])
def _(S):
    ap = minus(union(circle(9, 14.2, 6, ), circle(15, 14.2, 6), rect(9, 8.6, 6, 3)), circle(20.6, 9.2, 2.6), circle(21.2, 13.4, 2.3))
    leaf = pg([(13.4, 5.2), (15, 2.6), (18.4, 3), (16.6, 6)], S, r=S.r * 0.5)
    return [shell(ap), line("M12 9V5"), shell(leaf), dot(9.5, 14, 1.3), dot(14, 14, 1.3), detail(seg(10, 18, 13.6, 18))]


@icon("pumpkin-carriage", CAT, "Pumpkin-shaped coach with a window, curved ribs and two spoked wheels",
      tags=["pumpkin", "carriage", "coach", "cinderella", "fairy tale", "wheel", "magic", "halloween"])
def _(S):
    return [shell(ellipse(12, 11, 8.8, 6.4)), detail("M9.3 5Q7 11 9.3 17M14.7 5Q17 11 14.7 17"), detail(rect(10.6, 8.3, 2.8, 3.2, 0.8)),
            line("M12 4.7V2"), shell(circle(6.8, 19, 3)), shell(circle(17.2, 19, 3))]


@icon("frog-prince", CAT, "Sitting frog with bulging eyes wearing a small crown",
      tags=["frog", "prince", "crown", "fairy tale", "kiss", "royal", "toad", "enchanted"])
def _(S):
    body = union(ellipse(12, 15.5, 8, 5.5), circle(7.8, 10.8, 2.4), circle(16.2, 10.8, 2.4), ellipse(5.6, 19.6, 3, 2), ellipse(18.4, 19.6, 3, 2))
    crown = pg([(8.8, 7.2), (8.8, 2.8), (10.6, 4.6), (12, 2.3), (13.4, 4.6), (15.2, 2.8), (15.2, 7.2)], S, r=S.r * 0.5)
    return [shell(body), shell(crown), dot(7.8, 10.8, 0.8), dot(16.2, 10.8, 0.8), detail("M8 15.5q4 2.6 8 0")]


@icon("princess-and-the-pea", CAT, "Tall stack of mattresses on a bed with a single small pea underneath",
      tags=["princess", "pea", "mattress", "fairy tale", "bed", "royal", "sensitive", "stack"])
def _(S):
    return [shell(rect(6, 4, 12, 4, L(S, 1, 2))), shell(rect(6, 8, 12, 4, L(S, 1, 2))), shell(rect(6, 12, 12, 4, L(S, 1, 2))),
            dot(12, 18.6, 1.3), line("M3 5V21.5H21V5"), dot(3, 3, 1.3), dot(21, 3, 1.3)]


@icon("golden-goose", CAT, "Goose standing over a shiny egg with sparkles",
      tags=["goose", "golden egg", "fairy tale", "fable", "gold", "egg", "riches", "bird"])
def _(S):
    body = pg([(6.5, 12), (9.5, 8.6), (15, 8.6), (20.5, 5.6), (19.6, 11.6), (15.5, 14.4), (9.5, 14.4)], S, r=S.r * 0.8)
    beak = pg([(6, 3.2), (4, 4), (6, 4.9)], S, r=S.r * 0.3)
    return [shell(union(body, circle(7.8, 3.9, 1.9), beak)), line("M9.6 9.6Q5.8 8.8 7 5"), line("M9 14.4V17.2M16.4 14.4V17.2"),
            shell(ellipse(12.7, 19.6, 1.6, 2)), mark(sparkle(4.4, 17.6, 2, 0.5)), mark(sparkle(20.8, 18.4, 1.6, 0.4))]


@icon("man-in-the-moon", CAT, "Crescent moon with a sleepy face in profile on its inner curve",
      tags=["moon", "man in the moon", "crescent", "night", "face", "nursery rhyme", "sleep", "lunar"])
def _(S):
    moon = minus(circle(11, 12, 9.5), circle(16.5, 11.5, 8))
    nose = pg([(8.7, 10.2), (11.4, 12), (8.7, 13.6)], S, r=S.r * 0.5)
    return [shell(union(moon, nose)), detail("M5.2 10.2q1.2 1.2 2.6 0"), mark(sparkle(19.4, 5, 2, 0.5))]


@icon("wizard-tower", CAT, "Tall slim stone tower with a pointed conical roof, a high window and a star above",
      tags=["wizard", "tower", "magic", "sorcerer", "castle", "fantasy", "spire", "mage"])
def _(S):
    body = rect(8.5, 10, 7, 12, L(S, 0, 1))
    roof = pg([(6, 10.5), (11, 2.6), (16, 10.5)], S, r=S.r * 0.6)
    return [shell(union(body, roof)), detail(rect(10.9, 13.2, 2.2, 3.4, 1.1)), detail(seg(8.5, 19.5, 12, 19.5)), mark(sparkle(19, 4.6, 2.2, 0.55))]


@icon("floating-island", CAT, "Chunk of earth hovering in the air with a tree on top and dangling roots and rocks below",
      tags=["island", "floating", "sky", "fantasy", "tree", "earth", "hovering", "world"])
def _(S):
    isl = "M3 12.5H21Q20 16 15.6 17.4Q13.8 18.4 13.4 20.6H11.8Q11.4 18.6 8.6 17.6Q4 16.4 3 12.5Z"
    return [shell(isl), shell(circle(12, 6.3, 3.5)), line("M12 9.8V12.5"), dot(3.6, 19.6, 1.0), dot(20.6, 19, 1.1)]


@icon("atlantis", CAT, "Domed city of towers on the sea floor with bubbles rising and waves above",
      tags=["atlantis", "underwater city", "sunken city", "dome", "lost city", "sea", "legend", "ocean"])
def _(S):
    dome = "M3.5 19.5a8.5 8.5 0 0 1 17 0Z"
    return [shell(dome), detail(seg(9, 19.5, 9, 15.5)), detail(seg(12, 19.5, 12, 13.5)), detail(seg(15, 19.5, 15, 15.5)), line("M2 21.5H22"),
            line("M3 3.4q2 -1.5 4 0t4 0t4 0t4 0"), dot(6, 8, 0.9), dot(9.5, 6, 0.9), dot(18, 7.6, 0.9)]


@icon("poison-bottle", CAT, "Small corked bottle marked with a skull and crossbones",
      tags=["poison", "bottle", "toxic", "skull", "crossbones", "potion", "danger", "vial"])
def _(S):
    body = union(rect(4.5, 9.5, 15, 12.5, L(S, 2, 4)), rect(9.5, 5.5, 5, 5))
    return [shell(body), shell(rect(9.6, 2, 4.8, 3.5, L(S, 0.5, 1))), dot(10.2, 13, 1.1), dot(13.8, 13, 1.1),
            detail(seg(8, 16.4, 16, 20.6)), detail(seg(16, 16.4, 8, 20.6))]


@icon("treasure-hoard", CAT, "Heap of gold coins with a goblet and a gem poking out of it",
      tags=["treasure", "hoard", "gold", "coins", "dragon", "goblet", "gems", "riches", "loot"])
def _(S):
    mound = "M2.5 21.5Q4.5 12.5 12 11.5Q19.5 12.5 21.5 21.5Z"
    cup = "M9.3 2.6H14.7Q14.7 7.2 12 7.2Q9.3 7.2 9.3 2.6Z"
    return [shell(mound), shell(cup), line("M12 7.2V11"), detail(circle(8, 17.8, 1.4)), detail(circle(13.2, 16.6, 1.4)), detail(circle(17, 19, 1.3)),
            shell(pg([(17.2, 9.4), (19.4, 7), (21.6, 9.4), (19.4, 12.4)], S, r=S.r * 0.4))]


@icon("invisibility-cloak", CAT, "Hooded cloak standing upright with an empty dark opening and a dashed hem",
      tags=["invisibility", "cloak", "hood", "invisible", "magic", "hidden", "wizard", "cape"])
def _(S):
    cloak = "M12 2.5C8.4 2.5 7.4 6 7.4 8.4L4.6 18.8H19.4L16.6 8.4C16.6 6 15.6 2.5 12 2.5Z"
    return [shell(cloak), mark(ellipse(12, 8.6, 2.3, 3)), line("M4.6 21.8h3M10.5 21.8h3M16.4 21.8h3")]


@icon("spell-cast", CAT, "Open hand with spread fingers casting a spark above the palm",
      tags=["spell", "cast", "magic", "hand", "sparkle", "wizard", "sorcery", "enchant"])
def _(S):
    return [shell(rect(7, 14, 10, 8, L(S, 2, 4))), line("M9 14L6.6 9M12 14V8M15 14L17.4 9M7.4 17L3.6 14.4"),
            mark(sparkle(12, 3.4, 2.3, 0.6)), dot(4.5, 4.5, 1.1), dot(19.5, 4.5, 1.1)]


@icon("ouroboros", CAT, "Snake forming a circle while biting its own tail",
      tags=["ouroboros", "snake", "serpent", "infinity", "cycle", "eternity", "alchemy", "circle"])
def _(S):
    cx, cy, r = 12, 12, 8
    a0, a1 = -36, 286
    hx, hy = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    ang = math.degrees(math.atan2(-math.cos(math.radians(a0)), math.sin(math.radians(a0))))
    ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    head = rot(ellipse(hx, hy, 4.6, L(S, 2.8, 3)), ang, hx, hy)
    return [line(arc(cx, cy, r, a0, a1)), shell(head), dot(hx + ux * 1.6 + uy * 1.1, hy + uy * 1.6 - ux * 1.1, 0.8)]


@icon("horseshoe", CAT, "U-shaped horseshoe with the open end up and nail holes along both arms",
      tags=["horseshoe", "lucky", "luck", "charm", "farrier", "horse", "good fortune", "talisman"])
def _(S):
    shoe = "M4 3H9.5V12.5A2.5 3 0 0 0 14.5 12.5V3H20V12.5A8 9.5 0 0 1 4 12.5Z"
    holes = [dot(6.75, 6.5, 0.8), dot(6.75, 11, 0.8), dot(17.25, 6.5, 0.8), dot(17.25, 11, 0.8), dot(8.3, 16.4, 0.8), dot(15.7, 16.4, 0.8)]
    return [shell(shoe)] + holes
