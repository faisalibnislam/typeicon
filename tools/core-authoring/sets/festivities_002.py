"""TypeIcon Core: festivities (cultural celebration objects, gifts, party and wedding items), batch 2."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "festivities"


def L(S, a, b):
    return a if S.name == "line" else b


def flame(x, y, h=4.0, w=1.7):
    """Small solid flame with its base centre at (x, y)."""
    return solid(f"M{fmt(x)} {fmt(y - h)}C{fmt(x + w)} {fmt(y - h * 0.4)} {fmt(x + w)} {fmt(y)} {fmt(x)} {fmt(y)}"
                 f"C{fmt(x - w)} {fmt(y)} {fmt(x - w)} {fmt(y - h * 0.4)} {fmt(x)} {fmt(y - h)}Z")


def star(cx, cy, ro, ri, n=5, rot=-90.0):
    pts = []
    for i in range(n):
        pts.append(polar(cx, cy, ro, rot + 360 / n * i))
        pts.append(polar(cx, cy, ri, rot + 360 / n * i + 180 / n))
    return pts


def orect(cx, cy, w, h, ang):
    """Corners of a w x h rectangle centred at (cx, cy), turned clockwise by ang degrees."""
    a = math.radians(ang)
    c, s = math.cos(a), math.sin(a)
    out = []
    for dx, dy in [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]:
        out.append((cx + dx * c - dy * s, cy + dx * s + dy * c))
    return out


def mx(pts):
    return [(24 - x, y) for x, y in pts]


# ============================================================================ japan

@icon("hina-dolls", CAT, "Two seated festival dolls in wide robes on a platform, one with a tall hat and one with a crown",
      tags=["hina", "dolls", "girls day", "hinamatsuri", "japan", "emperor empress", "festival", "doll display"])
def _(S):
    return [
        shell(poly([(6.5, 12), (11, 19), (2, 19)], closed=True, r=S.r), stroke_miterlimit="2"),
        shell(circle(6.5, 9, 1.8)),
        shell(poly([(17.5, 12), (22, 19), (13, 19)], closed=True, r=S.r), stroke_miterlimit="2"),
        shell(circle(17.5, 9, 1.8)),
        line(poly([(15.6, 6.2), (15.6, 4), (17.5, 5.6), (19.4, 4), (19.4, 6.2)]), stroke_miterlimit="2"),
        shell(rect(5.2, 2.5, 2.6, 3.2, 0)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("tanabata-bamboo", CAT, "Upright bamboo stalk with a twig carrying hanging paper wish strips",
      tags=["tanabata", "bamboo", "wish", "star festival", "japan", "paper strips", "tanzaku", "july"])
def _(S):
    return [
        shell(rect(3.5, 2, 3.5, 20, min(S.R, 1))),
        detail(seg(3.5, 9, 7, 9)), detail(seg(3.5, 16, 7, 16)),
        line(seg(7, 4.5, 21.5, 4.5)),
        shell(rect(10.5, 4.5, 3.5, 8, min(S.R, 1))),
        shell(rect(16.5, 4.5, 3.5, 12, min(S.R, 1))),
    ]


@icon("floating-lantern", CAT, "Small box lantern with a glowing flame sitting on wavy water lines",
      tags=["lantern", "floating", "water", "obon", "memorial", "paper lantern", "festival", "river"])
def _(S):
    return [
        shell(rect(7, 2.5, 10, 11, min(S.R, 2))),
        detail(seg(7, 5.5, 17, 5.5)),
        flame(12, 12, 4.2, 1.6),
        line("M3 17.5Q5 15.5 7 17.5T11 17.5T15 17.5T19 17.5T21 17.5"),
        line("M3 21.5Q5 19.5 7 21.5T11 21.5T15 21.5T19 21.5T21 21.5"),
    ]


@icon("oni-mask", CAT, "Front view of a demon mask with two horns, angry brows, round eyes and fanged mouth",
      tags=["oni", "demon", "mask", "japan", "setsubun", "ogre", "horns", "festival"])
def _(S):
    return [
        shell(poly([(5.5, 8.5), (5.5, 2.5), (9.5, 6.5)], closed=True, r=S.r * 0.3)),
        shell(poly([(18.5, 8.5), (18.5, 2.5), (14.5, 6.5)], closed=True, r=S.r * 0.3)),
        shell(rect(4.5, 7, 15, 14.5, min(S.R, 5) + 2)),
        detail(poly([(7.5, 10.5), (10.5, 12)])),
        detail(poly([(16.5, 10.5), (13.5, 12)])),
        dot(9, 13.5, 1), dot(15, 13.5, 1),
        detail(seg(8, 18, 16, 18)),
    ]


@icon("samurai-helmet", CAT, "Front view of a warrior helmet with a flared neck guard and a crescent crest",
      tags=["samurai", "kabuto", "helmet", "japan", "warrior", "boys day", "childrens day", "armor"])
def _(S):
    return [
        line("M12 8Q9 7.5 8.5 2.5"),
        line("M12 8Q15 7.5 15.5 2.5"),
        shell("M6.5 14C6.5 10 9 8 12 8C15 8 17.5 10 17.5 14Z"),
        shell(poly([(6.5, 14), (3, 20.5), (21, 20.5), (17.5, 14)], closed=True, r=S.r * 0.5)),
        detail(poly([(8.5, 17), (15.5, 17)])),
    ]


@icon("hagoita", CAT, "Decorated wooden paddle with a short handle and a feathered shuttle beside it",
      tags=["hagoita", "paddle", "new year", "japan", "battledore", "shuttlecock", "hanetsuki", "game"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 10, 13.5, min(S.R, 2))),
        shell(rect(5.5, 16, 4, 5.5, 0)),
        detail(circle(7.5, 7, 1.5)),
        detail(poly([(4.8, 13), (7.5, 9.6), (10.2, 13)])),
        shell(circle(18.5, 19, 1.8)),
        line(seg(18.5, 17.2, 18.5, 12)),
        line(seg(18.5, 17.2, 16.2, 12.8)),
        line(seg(18.5, 17.2, 20.8, 12.8)),
    ]


@icon("portable-shrine", CAT, "Small shrine box with a curved roof and bird finial carried on two long poles",
      tags=["mikoshi", "shrine", "portable", "festival", "matsuri", "japan", "procession", "poles"])
def _(S):
    return [
        line(seg(12, 7.5, 12, 4.5)),
        shell(poly([(2.5, 11), (8.5, 7.5), (15.5, 7.5), (21.5, 11)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        shell(rect(6.5, 11, 11, 5, 0)),
        dot(12, 3.2, 1.4),
        line(seg(1.5, 19, 22.5, 19)),
        line(seg(1.5, 22, 22.5, 22)),
    ]


@icon("fox-mask", CAT, "Front view of a fox face mask with tall pointed ears, narrow eyes and cheek marks",
      tags=["kitsune", "fox", "mask", "inari", "japan", "festival", "noh", "spirit"])
def _(S):
    return [
        shell(poly([(4, 2.5), (9.5, 7), (14.5, 7), (20, 2.5), (20, 13), (12, 21.5), (4, 13)], closed=True, r=S.r)),
        detail(poly([(6.5, 11), (10.5, 13)])),
        detail(poly([(17.5, 11), (13.5, 13)])),
        dot(12, 17.5, 1.2),
    ]


@icon("temari-ball", CAT, "Round thread ball wrapped with two crossing curved bands",
      tags=["temari", "thread ball", "japan", "craft", "new year", "embroidery", "traditional toy", "ball"])
def _(S):
    ry = L(S, 3.2, 4.2)

    def band(deg):
        a = math.radians(deg)
        dx, dy = 8.6 * math.cos(a), 8.6 * math.sin(a)
        return (f"M{fmt(12 - dx)} {fmt(12 - dy)}A8.6 {ry} {deg} 1 0 {fmt(12 + dx)} {fmt(12 + dy)}"
                f"A8.6 {ry} {deg} 1 0 {fmt(12 - dx)} {fmt(12 - dy)}Z")
    return [
        shell(circle(12, 12, 9)),
        detail(band(45)),
        detail(band(-45)),
    ]


@icon("mochi-pounding", CAT, "Wooden tub holding a mound of rice dough with a heavy mallet raised above it",
      tags=["mochitsuki", "mochi", "mallet", "new year", "japan", "rice", "kine", "usu"])
def _(S):
    h = orect(17.5, 6, 3.6, 7.5, -30)
    return [
        shell(poly([(3.5, 13), (20.5, 13), (18.5, 21), (5.5, 21)], closed=True, r=S.r * 0.5)),
        line("M7 13C7 10.3 9 9.5 11 9.5C13 9.5 15 10.3 15 13"),
        shell(poly(h, closed=True, r=S.r * 0.5)),
        line(seg(16.3, 8.3, 10.5, 8.5) if False else seg(16.1, 7.8, 11.5, 9.7)),
    ]


@icon("shrine-bell", CAT, "Round bell hanging from a beam with a thick braided rope below it",
      tags=["suzu", "shrine", "bell", "rope", "japan", "prayer", "temple", "worship"])
def _(S):
    return [
        line(seg(3, 3.5, 21, 3.5)),
        line(seg(12, 3.5, 12, 5.5)),
        shell(circle(12, 10, 4.5)),
        detail(seg(7.5, 11, 16.5, 11)),
        shell(rect(10.5, 14.5, 3, 7, 0)),
        detail(seg(10.5, 17, 13.5, 17)),
        detail(seg(10.5, 19.5, 13.5, 19.5)),
    ]


@icon("fortune-slip", CAT, "Narrow paper fortune strip tied around a horizontal cord",
      tags=["omikuji", "fortune", "paper strip", "shrine", "japan", "luck", "tied", "prediction"])
def _(S):
    return [
        shell(rect(9, 3, 6, 18, 0)),
        line(seg(2.5, 8, 9, 8)),
        line(seg(15, 8, 21.5, 8)),
        detail(seg(9, 8, 15, 8)),
        detail(seg(12, 12, 12, 17)),
    ]


@icon("hahoe-mask", CAT, "Front view of a carved wooden mask with crescent eyes, a broad smile and a separate hinged chin",
      tags=["hahoe", "mask", "korea", "korean", "mask dance", "talchum", "traditional", "theatre"])
def _(S):
    return [
        shell("M5 6C5 3.5 8 2.5 12 2.5C16 2.5 19 3.5 19 6L19.5 10.5C19.5 14 17 16 12 16C7 16 4.5 14 4.5 10.5Z"),
        detail("M6.5 8.3Q8.5 6 10.5 8.3"),
        detail("M13.5 8.3Q15.5 6 17.5 8.3"),
        detail(seg(12, 9, 12, 11.5)),
        detail("M8.5 13Q12 14.6 15.5 13"),
        shell("M8 18.5Q12 23 16 18.5Z"),
    ]


@icon("songpyeon", CAT, "Three half-moon rice cakes stacked in a small pyramid on a pine needle bed",
      tags=["songpyeon", "rice cake", "chuseok", "korea", "korean", "harvest", "half moon", "dumpling"])
def _(S):
    return [
        shell("M8 9.5a4 4 0 0 1 8 0Z"),
        shell("M2.5 17a4.5 4.5 0 0 1 9 0Z"),
        shell("M12.5 17a4.5 4.5 0 0 1 9 0Z"),
        line(seg(2, 21, 22, 21)),
    ]


def _duck(S, m):
    def X(x):
        return 24 - x if m else x
    body = (f"M{fmt(X(1.5))} 10.5C{fmt(X(2))} 15.5 {fmt(X(4.5))} 18 {fmt(X(8))} 18C{fmt(X(10.5))} 18 {fmt(X(11))} 16.5 {fmt(X(11))} 14.5"
            f"C{fmt(X(11))} 12.6 {fmt(X(9.5))} 12.2 {fmt(X(7.5))} 12.4C{fmt(X(5))} 12.6 {fmt(X(3.2))} 12 {fmt(X(1.5))} 10.5Z")
    beak = [(X(8.8), 6.6), (X(11), 7.6), (X(8.8), 8.6)]
    return [
        shell(body),
        shell(circle(X(6.8), 8, 2.4)),
        solid(poly(beak, closed=True)),
        detail(seg(X(4.5), 15, X(8), 15)),
    ]


@icon("wedding-ducks", CAT, "Pair of carved ducks facing each other, each with a wing band",
      tags=["mandarin ducks", "wedding", "korea", "korean", "pair", "fidelity", "couple", "wooden ducks"])
def _(S):
    return _duck(S, False) + _duck(S, True)


def cut(d):
    """Small shape that is solid in Line/Rounded and knocked out of a Filled body."""
    return Part("dot", d)


def leaf(bx, by, tx, ty, w):
    """Pointed leaf from base (bx, by) to tip (tx, ty), bulging by w on both sides."""
    dx, dy = tx - bx, ty - by
    n = math.hypot(dx, dy)
    nx, ny = -dy / n * w, dx / n * w
    mx_, my_ = (bx + tx) / 2, (by + ty) / 2
    return (f"M{fmt(bx)} {fmt(by)}Q{fmt(mx_ + nx)} {fmt(my_ + ny)} {fmt(tx)} {fmt(ty)}"
            f"Q{fmt(mx_ - nx)} {fmt(my_ - ny)} {fmt(bx)} {fmt(by)}Z")


def bead_points(p0, p1, p2, n):
    """n points spread evenly by arc length along a quadratic curve."""
    pts = []
    for i in range(241):
        t = i / 240
        pts.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
    acc = [0.0]
    for a, b in zip(pts, pts[1:]):
        acc.append(acc[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    out = []
    for k in range(n):
        target = acc[-1] * k / (n - 1)
        j = next(i for i, v in enumerate(acc) if v >= target)
        out.append(pts[j])
    return out


# ============================================================================ southeast asia

@icon("krathong", CAT, "Round leaf float with petals, a candle with flame and incense sticks, resting on a water line",
      tags=["krathong", "loy krathong", "thailand", "lotus", "float", "candle", "water festival", "offering"])
def _(S):
    return [
        shell(rect(10.5, 9, 3, 5, 0)),
        flame(12, 8.5, 4, 1.5),
        line(seg(7.5, 14, 5.5, 8)),
        line(seg(16.5, 14, 18.5, 8)),
        shell(leaf(12, 16.5, 3.5, 11, 3), stroke_miterlimit="3"),
        shell(leaf(12, 16.5, 20.5, 11, 3), stroke_miterlimit="3"),
        line("M3 17.5Q12 19 21 17.5"),
        line("M3 22Q5 20.5 7 22T11 22T15 22T19 22T21 22"),
    ]


@icon("penjor", CAT, "Tall bamboo pole arching over at the top with a long woven ornament hanging from its tip",
      tags=["penjor", "bali", "galungan", "bamboo pole", "indonesia", "offering", "festival", "decoration"])
def _(S):
    return [
        line("M6 21C6 11 7.5 3.5 13 3.5C16 3.5 17.5 5 17.5 7"),
        shell(poly([(17.5, 7), (20, 11.5), (17.5, 18), (15, 11.5)], closed=True, r=S.r * 0.5), stroke_miterlimit="3"),
        line(seg(16.3, 18, 16.3, 21.5)), line(seg(18.7, 18, 18.7, 21.5)),
        line(seg(2.5, 22, 9.5, 22)),
    ]


@icon("jasmine-garland", CAT, "Hanging string of small flower buds ending in a rose bud and a short tassel",
      tags=["jasmine", "garland", "flower", "string", "india", "wedding", "indonesia", "gajra", "buds"])
def _(S):
    return [
        dot(12, 3.5, 1.5), dot(12, 7.5, 1.5), dot(12, 11.5, 1.5),
        shell(circle(12, 16, 3)),
        detail("M10.7 16.5Q12 14.2 13.3 16.5"),
        line(seg(12, 19.2, 12, 22.5)),
    ]


@icon("square-rice-cake", CAT, "Square leaf-wrapped rice cake tied with crossed strings into four quarters",
      tags=["banh chung", "rice cake", "tet", "vietnam", "vietnamese", "new year", "leaf wrapped", "square"])
def _(S):
    return [
        shell(rect(3.5, 3.5, 17, 17, S.R)),
        detail(seg(12, 3.5, 12, 20.5)),
        detail(seg(3.5, 12, 20.5, 12)),
        detail(poly([(3.5, 3.5), (8, 8)])), detail(poly([(20.5, 20.5), (16, 16)])),
    ]


@icon("barong-mask", CAT, "Front view of a guardian beast mask with a tall zigzag crown, bulging eyes and a toothy mouth",
      tags=["barong", "bali", "indonesia", "mask", "guardian", "lion", "dance", "festival"])
def _(S):
    return [
        shell(poly([(6, 8), (6.5, 2.5), (9.5, 5), (12, 2), (14.5, 5), (17.5, 2.5), (18, 8)], closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        shell(rect(3.5, 8, 17, 13.5, min(S.R, 4))),
        shell(circle(8.5, 12.5, 2.2)),
        shell(circle(15.5, 12.5, 2.2)),
        dot(8.5, 12.5, 0.8), dot(15.5, 12.5, 0.8),
        detail(poly([(7, 17), (8.8, 19.3), (10.6, 17), (12.4, 19.3), (14.2, 17), (16, 19.3), (17.4, 17)], r=0)),
    ]


# ============================================================================ latin america

@icon("papel-picado", CAT, "Line of cut-paper banners with notched lower edges and punched holes, hanging in a row",
      tags=["papel picado", "mexico", "mexican", "banner", "day of the dead", "fiesta", "cut paper", "bunting"])
def _(S):
    def banner(x):
        return [shell(poly([(x, 4.5), (x + 5.5, 4.5), (x + 5.5, 17), (x + 2.75, 14.5), (x, 17)], closed=True, r=S.r * 0.3)),
                dot(x + 2.75, 9, 1)]
    return [line(seg(1.5, 4.5, 22.5, 4.5))] + banner(2) + banner(9.25) + banner(16.5)


@icon("sugar-skull", CAT, "Decorated skull with flower-shaped eyes, a heart-shaped nose and a stitched smile",
      tags=["sugar skull", "calavera", "day of the dead", "dia de muertos", "mexico", "skull", "halloween", "altar"])
def _(S):
    def flower(cx, cy):
        return "".join(circle(cx + dx, cy + dy, 1.25) for dx, dy in [(0, -1.3), (1.3, 0), (0, 1.3), (-1.3, 0), (0, 0)])
    return [
        shell("M5 10C5 5.5 8 2.5 12 2.5C16 2.5 19 5.5 19 10C19 12.5 17.5 13.5 16.5 14.5L16.5 20C16.5 21 15.5 21.5 14.5 21.5H9.5C8.5 21.5 7.5 21 7.5 20V14.5C6.5 13.5 5 12.5 5 10Z"),
        cut(flower(8.6, 10)), cut(flower(15.4, 10)),
        cut("M12 16C10.4 15 10.4 13.6 11.2 13.6C11.7 13.6 12 14 12 14.2C12 14 12.3 13.6 12.8 13.6C13.6 13.6 13.6 15 12 16Z"),
        detail(seg(10, 18.3, 10, 21)), detail(seg(14, 18.3, 14, 21)),
    ]


@icon("ofrenda", CAT, "Stepped altar of three tiers with a photo frame at the top, candles and marigold flowers",
      tags=["ofrenda", "altar", "day of the dead", "dia de muertos", "mexico", "marigold", "candles", "remembrance"])
def _(S):
    return [
        shell(poly([(8, 2.5), (16, 2.5), (16, 8.5), (19, 8.5), (19, 14.5), (22, 14.5), (22, 21.5), (2, 21.5), (2, 14.5), (5, 14.5),
                    (5, 8.5), (8, 8.5)], closed=True, r=S.r * 0.4)),
        detail(circle(12, 5.6, 1.4)),
        dot(8.5, 11.5, 1), dot(15.5, 11.5, 1),
        dot(5.5, 18, 1), dot(12, 18, 1), dot(18.5, 18, 1),
    ]


@icon("luminaria", CAT, "Paper bag with a folded cuff, a candle flame rising from the top and a star cut in the front",
      tags=["luminaria", "farolito", "paper bag", "candle", "christmas eve", "new mexico", "lantern", "glow"])
def _(S):
    st = poly(star(12, 16.4, 2.9, 1.3, 5), closed=True)
    return [
        flame(12, 7, 4.5, 1.6),
        shell(poly([(5.5, 7.5), (18.5, 7.5), (19.5, 21.5), (4.5, 21.5)], closed=True, r=S.r * 0.5)),
        detail(seg(5.5, 11, 18.5, 11)),
        cut(st),
    ]


@icon("gods-eye", CAT, "Diamond of yarn woven in nested square bands around two crossed sticks",
      tags=["ojo de dios", "gods eye", "yarn", "craft", "mexico", "weaving", "diamond", "protection"])
def _(S):
    return [
        shell(poly([(12, 5), (19, 12), (12, 19), (5, 12)], closed=True, r=S.r * 0.3), stroke_miterlimit="3"),
        detail(poly([(12, 8.5), (15.5, 12), (12, 15.5), (8.5, 12)], closed=True)),
        line(seg(12, 1.5, 12, 5)), line(seg(12, 19, 12, 22.5)),
        line(seg(1.5, 12, 5, 12)), line(seg(19, 12, 22.5, 12)),
    ]


@icon("worry-dolls", CAT, "Three tiny stick dolls in a row with round heads and thread-wrapped bodies",
      tags=["worry dolls", "guatemala", "dolls", "tiny dolls", "trouble dolls", "handmade", "craft", "folk art"])
def _(S):
    out = []
    for cx in (5, 12, 19):
        out += [shell(circle(cx, 6, 1.9)), shell(rect(cx - 2, 9.5, 4, 11.5, L(S, 0.5, 2))), detail(seg(cx - 2, 13.5, cx + 2, 13.5)),
                detail(seg(cx - 2, 17, cx + 2, 17))]
    return out


@icon("carnival-headdress", CAT, "Tall fan of plumed feathers rising from a jeweled headband",
      tags=["carnival", "headdress", "feathers", "samba", "rio", "costume", "plumes", "parade"])
def _(S):
    feathers = []
    for ang, ln in [(-55, 12), (-28, 14), (0, 15), (28, 14), (55, 12)]:
        tx, ty = polar(12, 17, ln, ang - 90)
        feathers.append(shell(leaf(12, 17, tx, ty, 2.2), stroke_miterlimit="3"))
    return feathers + [
        shell(rect(5, 17, 14, 4.5, min(S.R, 2))),
        dot(9, 19.3, 0.8), dot(12, 19.3, 0.8), dot(15, 19.3, 0.8),
    ]


@icon("mardi-gras-beads", CAT, "Two looped strands of large round beads hanging in curves",
      tags=["mardi gras", "beads", "new orleans", "necklace", "carnival", "parade", "strands", "throws"])
def _(S):
    out = []
    r = L(S, 1.7, 2.0)
    for x0, depth, n in [(2.5, 20, 8), (6, 12, 5)]:
        out.append(line(f"M{fmt(x0)} 3Q12 {fmt(depth + 6)} {fmt(24 - x0)} 3"))
        for x, y in bead_points((x0, 3), (12, depth + 6), (24 - x0, 3), n):
            out.append(dot(x, y, r))
    return out


# ============================================================================ easter and spring

@icon("easter-egg-tree", CAT, "Bare branches in a vase with decorated eggs hanging from threads",
      tags=["easter", "egg tree", "eggs", "decorated eggs", "branches", "spring", "ostereierbaum", "vase"])
def _(S):
    return [
        shell(poly([(8.5, 16.5), (15.5, 16.5), (16.5, 21.5), (7.5, 21.5)], closed=True, r=S.r * 0.5)),
        line(seg(12, 16.5, 12, 3)),
        line(seg(12, 11, 5.5, 6)),
        line(seg(12, 8, 18.5, 3.5)),
        line(seg(5.5, 6, 5.5, 8.3)), line(seg(18.5, 3.5, 18.5, 5.8)),
        shell(ellipse(5.5, 11.2, 2, 2.9)), shell(ellipse(18.5, 8.7, 2, 2.9)),
    ]


@icon("palm-cross", CAT, "Small cross folded from a strip of palm leaf with crossing fold lines",
      tags=["palm sunday", "palm cross", "easter", "holy week", "folded palm", "christian", "cross", "palm leaf"])
def _(S):
    return [
        shell(poly([(9.5, 2.5), (14.5, 2.5), (14.5, 7.5), (20, 7.5), (20, 12.5), (14.5, 12.5), (14.5, 21.5), (9.5, 21.5),
                    (9.5, 12.5), (4, 12.5), (4, 7.5), (9.5, 7.5)], closed=True, r=S.r * 0.4)),
        detail(seg(9.5, 7.5, 14.5, 12.5)),
        detail(seg(14.5, 7.5, 9.5, 12.5)),
    ]


# ============================================================================ europe

@icon("beer-stein", CAT, "Tall tankard with a hinged domed lid, a thumb lever, a big handle and two relief bands",
      tags=["stein", "beer", "oktoberfest", "tankard", "german", "mug", "lid", "festival"])
def _(S):
    return [
        line("M15 6.5L17.5 4"),
        shell("M3.5 8C3.5 4.5 6 3.5 9.25 3.5C12.5 3.5 15 4.5 15 8Z"),
        shell(rect(3.5, 8, 11.5, 13.5, min(S.R, 2))),
        detail(seg(3.5, 12, 15, 12)),
        detail(seg(3.5, 17, 15, 17)),
        line(L(S, "M15 10.5H18.5V17.5H15", "M15 10.5H18a2.5 2.5 0 0 1 2.5 2.5V15.5a2.5 2.5 0 0 1 -2.5 2.5H15")),
    ]


@icon("candle-crown", CAT, "Leafy ring crown with three upright candles and flames standing on it",
      tags=["st lucia", "candle crown", "lucia", "sweden", "advent", "wreath", "candles", "saint lucy"])
def _(S):
    return [
        flame(6.5, 9.5, 3.8, 1.4), flame(12, 7, 3.8, 1.4), flame(17.5, 9.5, 3.8, 1.4),
        line(seg(6.5, 16, 6.5, 10.5)), line(seg(12, 16, 12, 8)), line(seg(17.5, 16, 17.5, 10.5)),
        shell(ellipse(12, 18, 9.5, 3.5)),
        detail(seg(7, 18, 7.01, 18)) if False else dot(12, 18, 1),
    ]


@icon("midsummer-pole", CAT, "Tall pole with a crossbar, leafy sprigs up its length and two leafy rings hanging from the bar",
      tags=["midsummer", "maypole", "pole", "sweden", "scandinavia", "wreath", "summer solstice", "festival"])
def _(S):
    return [
        line(seg(12, 2, 12, 22)),
        line(seg(4, 5, 20, 5)),
        line(seg(4, 5, 4, 6.5)), line(seg(20, 5, 20, 6.5)),
        shell(circle(4.6, 9, 2.4)), shell(circle(19.4, 9, 2.4)),
        shell(leaf(12, 15, 6.5, 12.5, 1.6), stroke_miterlimit="3"),
        shell(leaf(12, 20, 17.5, 17.5, 1.6), stroke_miterlimit="3"),
    ]


@icon("martenitsa", CAT, "Two small yarn dolls, one plain and one dark, hanging from a looped cord with short tassels",
      tags=["martenitsa", "bulgaria", "yarn dolls", "red and white", "spring", "march", "baba marta", "tassel"])
def _(S):
    return [
        line("M5.5 7C5.5 1.5 18.5 1.5 18.5 7"),
        shell(circle(5.5, 9, 2)),
        shell(poly([(5.5, 11.5), (9, 18), (2, 18)], closed=True, r=S.r), stroke_miterlimit="2"),
        shell(circle(18.5, 9, 2)),
        solid(poly([(18.5, 11.5), (22, 18), (15, 18)], closed=True, r=S.r * 0.5)),
        line(seg(4, 18, 4, 21.5)), line(seg(7, 18, 7, 21.5)),
        line(seg(17, 18, 17, 21.5)), line(seg(20, 18, 20, 21.5)),
    ]


@icon("paschal-lamb", CAT, "Side view of a fluffy lamb standing with a pole and a small flag",
      tags=["paschal lamb", "easter", "lamb", "agnus dei", "christian", "flag", "sheep", "spring"])
def _(S):
    return [
        line(seg(11, 9.5, 11, 2.5)),
        shell(poly([(11, 2.5), (19, 4.5), (11, 6.5)], closed=True, r=S.r * 0.3), stroke_miterlimit="3"),
        shell("M8 17.5a3.2 3.2 0 0 1 -1 -6.2a3.6 3.6 0 0 1 6.5 -2a3.6 3.6 0 0 1 6.3 2a3.2 3.2 0 0 1 -1 6.2Z"),
        shell(ellipse(4.3, 13.2, 2, 2.6)),
        line(seg(10, 17.5, 10, 21.5)), line(seg(17, 17.5, 17, 21.5)),
    ]


@icon("dala-horse", CAT, "Side view of a stylized carved wooden horse with a thick body, straight legs and a painted harness band",
      tags=["dala horse", "sweden", "swedish", "wooden horse", "folk art", "toy", "dalahast", "carved"])
def _(S):
    return [
        shell(poly([(2.5, 10), (7, 9), (14, 9.5), (15.5, 4.5), (19, 2.5), (21.5, 5.5), (21, 8), (18.5, 8.5), (18.5, 21.5),
                    (15, 21.5), (15, 15.5), (9, 15.5), (9, 21.5), (5.5, 21.5), (5.5, 14), (2.5, 14)], closed=True, r=S.r * 0.7)),
        detail(seg(12, 9.5, 12, 15.5)),
        dot(18.6, 5.3, 0.9),
    ]


@icon("leprechaun-hat", CAT, "Tall top hat with a wide band, a square buckle at the front and a wide brim",
      tags=["leprechaun", "st patricks day", "irish", "ireland", "top hat", "buckle", "hat", "march 17"])
def _(S):
    return [
        shell(poly([(7, 3), (17, 3), (18, 16), (6, 16)], closed=True, r=S.r * 0.6)),
        shell(rect(2.5, 16, 19, 4.5, min(S.R, 2.2))),
        detail(seg(6.4, 12.5, 17.6, 12.5)),
        detail(rect(10, 9.5, 4, 5, 0)),
    ]


@icon("triquetra", CAT, "Three interlaced pointed loops forming a triangular knot",
      tags=["triquetra", "celtic knot", "trinity knot", "celtic", "irish", "knot", "trinity", "pagan"])
def _(S):
    def loop(deg):
        a = math.radians(deg)
        cx, cy = 12 + 3.4 * math.cos(a), 12 + 3.4 * math.sin(a)
        dx, dy = 6.2 * math.cos(a), 6.2 * math.sin(a)
        x1, y1, x2, y2 = cx - dx, cy - dy, cx + dx, cy + dy
        if S.name == "line":
            return (f"M{fmt(x1)} {fmt(y1)}A7.2 7.2 0 0 1 {fmt(x2)} {fmt(y2)}A7.2 7.2 0 0 1 {fmt(x1)} {fmt(y1)}Z")
        return (f"M{fmt(x1)} {fmt(y1)}A6.2 3.6 {fmt(deg)} 1 0 {fmt(x2)} {fmt(y2)}A6.2 3.6 {fmt(deg)} 1 0 {fmt(x1)} {fmt(y1)}Z")
    return [line(loop(-90)), line(loop(30)), line(loop(150))]


@icon("triskele", CAT, "Three spiral arms joined at the centre and turning the same way",
      tags=["triskele", "triskelion", "celtic", "spiral", "three spirals", "irish", "pagan", "symbol"])
def _(S):
    parts = []
    for k in range(3):
        base = k * 120 - 90
        pts = []
        for i in range(17):
            t = i / 16
            r = 0.6 + t * 8.6
            ang = base + t * 250
            pts.append(polar(12, 12, r, ang))
        parts.append(line(poly(pts)))
        if S.name != "line":
            ex, ey = pts[-1]
            parts.append(dot(ex, ey, 1.4))
    return parts


@icon("bodhran", CAT, "Round hand frame drum seen at an angle with a double-ended beater beside it",
      tags=["bodhran", "irish drum", "frame drum", "celtic", "music", "ireland", "beater", "percussion"])
def _(S):
    return [
        shell(ellipse(9.5, 9, 7.5, 6)),
        line("M2 9V12.5a7.5 6 0 0 0 15 0V9"),
        detail(seg(9.5, 3, 9.5, 15)) if False else detail(ellipse(9.5, 9, 3, 2.2)),
        line(seg(13.5, 22, 21.5, 14)),
        dot(13.5, 22, 1.4) if False else dot(14.3, 21.2, 1.5), dot(21.2, 14.3, 1.5),
    ]


@icon("wassail-bowl", CAT, "Large footed bowl with two handles, a ladle resting in it and floating fruit slices",
      tags=["wassail", "punch bowl", "bowl", "christmas", "mulled", "ladle", "winter", "apple"])
def _(S):
    return [
        shell("M3.5 10H20.5C20.5 15 17 18 12 18C7 18 3.5 15 3.5 10Z"),
        shell(rect(9, 18, 6, 3, 0)),
        line("M3.2 11.5H1.8V14.5H4.8"), line("M20.8 11.5H22.2V14.5H19.2"),
        line(seg(12, 10, 19, 2.8)),
        shell(circle(19.5, 4, 2)),
        dot(8, 13, 1), dot(12.5, 14, 1),
    ]


@icon("ceremonial-torch", CAT, "Hand-held torch with a tapered grip, a wide cup and a tall flame",
      tags=["torch", "olympic", "flame", "ceremonial", "fire", "ceremony", "relay", "handheld"])
def _(S):
    return [
        flame(12, 7, 5.5, 2.6),
        shell(poly([(7, 7), (17, 7), (14.5, 12), (9.5, 12)], closed=True, r=S.r * 0.5)),
        shell(poly([(10, 12), (14, 12), (13, 22), (11, 22)], closed=True, r=0)),
    ]


# ============================================================================ african and middle eastern

@icon("kinara", CAT, "Wooden candleholder with seven candles and small flames in a row, the middle one the tallest",
      tags=["kinara", "kwanzaa", "candles", "candleholder", "seven", "african american", "menorah", "holiday"])
def _(S):
    out = []
    for i in range(7):
        x = 3 + i * 3
        top = 6.5 if i == 3 else 10
        out += [line(seg(x, 16, x, top)), dot(x, top - 2.4, 1)]
    return out + [shell(rect(2, 16, 20, 5, min(S.R, 2)))]


@icon("carved-mask", CAT, "Elongated oval wooden mask with slit eyes, a long straight nose and carved bands",
      tags=["african mask", "wooden mask", "carved", "tribal", "ceremonial", "ritual", "art", "sculpture"])
def _(S):
    return [
        shell("M12 2.5C16.5 2.5 18 8 17.5 13C17 18 14.5 21.5 12 21.5C9.5 21.5 7 18 6.5 13C6 8 7.5 2.5 12 2.5Z"),
        detail(seg(7.8, 8, 9.8, 8)), detail(seg(14.2, 8, 16.2, 8)),
        detail(seg(12, 9.5, 12, 15)),
        detail(seg(10.5, 18, 13.5, 18)),
    ]


@icon("ceremonial-stool", CAT, "Carved stool with a curved crescent seat on a central pillar and a flat base",
      tags=["stool", "ashanti", "ceremonial", "african", "carved", "chief", "seat", "throne"])
def _(S):
    return [
        shell("M2.5 6Q12 13.5 21.5 6V9Q12 16.5 2.5 9Z"),
        shell(rect(10, 12, 4, 6, 0)),
        shell(rect(5, 17.5, 14, 4, min(S.R, 1.5))),
    ]


def heart_d(cx, cy, s):
    """Heart outline centred at (cx, cy); s = 1 gives a width of about 9.6."""
    def P(x, y):
        return f"{fmt(cx + x * s)} {fmt(cy + y * s)}"
    return (f"M{P(0, 4.8)}C{P(-6, 0.5)} {P(-5, -3.6)} {P(-2.3, -3.6)}C{P(-1, -3.6)} {P(0, -2.6)} {P(0, -1.8)}"
            f"C{P(0, -2.6)} {P(1, -3.6)} {P(2.3, -3.6)}C{P(5, -3.6)} {P(6, 0.5)} {P(0, 4.8)}Z")


def heart_poly(cx, cy, s):
    pts = [(0, 4.6), (-4.8, -0.4), (-4.8, -2.2), (-3, -3.6), (-1.2, -3.6), (0, -2), (1.2, -3.6), (3, -3.6), (4.8, -2.2), (4.8, -0.4)]
    return poly([(cx + x * s, cy + y * s) for x, y in pts], closed=True)


# ============================================================================ gifts, love and party

@icon("love-padlock", CAT, "Heart-shaped padlock with a keyhole, its shackle closed around a railing bar",
      tags=["love lock", "padlock", "heart", "bridge", "romance", "couple", "valentine", "forever"])
def _(S):
    return [
        line(seg(2, 5.5, 22, 5.5)),
        line("M9 9V6.5a3 3 0 0 1 6 0V9"),
        shell(heart_d(12, 14.5, 1.45)),
        cut(circle(12, 13.6, 1.4)),
        detail(seg(12, 13.6, 12, 17)),
    ]


@icon("candy-hearts", CAT, "Three small heart-shaped candies overlapping, each with a short line of text",
      tags=["candy hearts", "conversation hearts", "valentine", "sweets", "love", "february", "candy", "messages"])
def _(S):
    out = []
    for cx, cy in [(7.5, 7.5), (16.5, 7.5), (12, 15.5)]:
        out += [shell(heart_d(cx, cy, 1.05)), detail(seg(cx - 1.4, cy, cx + 1.4, cy))]
    return out


@icon("heart-balloon", CAT, "Heart-shaped balloon with a small knot at the bottom and a curly string",
      tags=["heart balloon", "balloon", "valentine", "love", "helium", "romance", "foil", "anniversary"])
def _(S):
    return [
        shell(heart_d(12, 9, 1.85)),
        solid(poly([(12, 18), (10.6, 20), (13.4, 20)], closed=True)),
        line("M12 20C9.8 20.6 9.8 22 12 22C13.6 22 13.8 22.8 12.6 23"),
    ]


@icon("heart-garland", CAT, "String of small hearts hanging in a gentle swag from a line",
      tags=["heart garland", "bunting", "valentine", "decoration", "string", "love", "party", "banner"])
def _(S):
    out = [line("M2 3.5Q12 10 22 3.5")]
    for x, y in [(6.4, 9.2), (12, 11.6), (17.6, 9.2)]:
        if S.name == "line":
            out.append(solid(heart_poly(x, y, 0.62)))
        else:
            out.append(solid(heart_d(x, y, 0.62)))
    return out


# ============================================================================ egypt and persian

@icon("ankh", CAT, "Cross with a teardrop loop in place of the upper arm",
      tags=["ankh", "egypt", "egyptian", "life", "key of life", "cross", "symbol", "ancient"])
def _(S):
    if S.name == "line":
        loop = "M12 13C7.6 10.6 8 2.5 12 2.5C16 2.5 16.4 10.6 12 13Z"
    else:
        loop = "M8.2 7.8a3.8 5 0 1 1 7.6 0a3.8 5 0 1 1 -7.6 0Z"
    return [line(loop), line(seg(12, 12.5, 12, 22)), line(seg(6, 14.5, 18, 14.5))]


@icon("eye-of-horus", CAT, "Stylized eye with a brow above, a dark pupil and a curled mark and drop line below",
      tags=["eye of horus", "wadjet", "egypt", "egyptian", "protection", "eye", "ancient", "symbol"])
def _(S):
    return [
        line("M3.5 5.5Q10 2 17.5 4"),
        shell("M2 10.5C5 6.5 8.5 6 11.5 6C15 6 18.5 7 21.5 10.5C18.5 13.5 15 14.5 11.5 14.5C8.5 14.5 5 14 2 10.5Z"),
        dot(11.5, 10.3, 2.3),
        line("M9 14.5V19Q9 21 6.5 21"),
        line("M15 14.5Q19 15.5 19 18.5Q19 21.5 16 21.5Q14 21.5 14 19.5Q14 18 15.5 18"),
    ]


@icon("scarab-amulet", CAT, "Top view of a beetle-shaped amulet with a rounded shell split down the middle and outstretched wings",
      tags=["scarab", "beetle", "egypt", "egyptian", "amulet", "wings", "khepri", "ancient"])
def _(S):
    return [
        shell(ellipse(12, 14, 4.8, 6.5)),
        shell(circle(12, 5.6, 2.2)),
        detail(seg(12, 8, 12, 20.5)),
        shell(poly([(7.3, 11.5), (2.2, 6), (2.2, 13), (7.6, 16)], closed=True, r=S.r * 0.6)),
        shell(poly([(16.7, 11.5), (21.8, 6), (21.8, 13), (16.4, 16)], closed=True, r=S.r * 0.6)),
    ]


@icon("sabzeh", CAT, "Shallow dish of tall sprouting wheatgrass tied in a bunch with a ribbon bow",
      tags=["sabzeh", "nowruz", "persian", "iranian", "wheatgrass", "haft sin", "spring", "new year"])
def _(S):
    tops = [(4.5, 4.5), (8, 2.5), (12, 2), (16, 2.5), (19.5, 4.5)]
    out = [line(seg(12, 10.5, x, y)) for x, y in tops]
    out += [line(seg(11, 13, 9.8, 17)), line(seg(13, 13, 14.2, 17)),
            solid(poly([(12, 11.8), (8.2, 9.8), (8.2, 13.8)], closed=True)),
            solid(poly([(12, 11.8), (15.8, 9.8), (15.8, 13.8)], closed=True)),
            shell("M3.5 17H20.5C20.5 20 17 21.8 12 21.8C7 21.8 3.5 20 3.5 17Z")]
    return out


@icon("jebena-coffee-pot", CAT, "Round-bellied clay coffee pot with a long narrow neck, a side spout and a looping handle",
      tags=["jebena", "coffee pot", "ethiopian", "coffee ceremony", "clay pot", "eritrean", "traditional", "brew"])
def _(S):
    return [
        shell(circle(11.5, 16.3, 5.2)),
        shell(poly([(10, 11.4), (9.4, 3.5), (14.2, 3.5), (13.6, 11.4)], closed=True, r=S.r * 0.4)),
        line(seg(8.4, 2.8, 15.2, 2.8)),
        shell(poly([(15.3, 14), (19.8, 8.5), (21.8, 10.2), (16.6, 16)], closed=True, r=S.r * 0.3)),
        line("M9.5 5.5Q3.2 5 3.7 11.5Q4 14.5 6.6 15.6"),
    ]


@icon("tiki-torch", CAT, "Bamboo pole torch with a woven canister holding a flame, staked in the ground",
      tags=["tiki torch", "garden torch", "bamboo", "luau", "tropical", "flame", "patio", "hawaiian"])
def _(S):
    return [
        flame(12, 7, 5, 2.2),
        shell(poly([(7.5, 7), (16.5, 7), (15, 13), (9, 13)], closed=True, r=S.r * 0.4)),
        detail(seg(8, 10, 16, 10)),
        shell(rect(10.5, 13, 3, 8, 0)),
        detail(seg(10.5, 17, 13.5, 17)),
        line(seg(5, 22, 19, 22)),
    ]


@icon("spiderweb", CAT, "Corner spiderweb of radial threads joined by sagging arcs, with a small spider on a thread",
      tags=["spiderweb", "cobweb", "web", "halloween", "spooky", "spider", "corner", "october"])
def _(S):
    ends = [polar(2, 2, 16, a) for a in (0, 30, 60, 90)]
    parts = [line(seg(2, 2, x, y)) for x, y in ends]
    for k in (5.5, 11):
        pts = [polar(2, 2, k, a) for a in (0, 30, 60, 90)]
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            cx, cy = (x1 + x2) / 2 - 0.8, (y1 + y2) / 2 - 0.8
            parts.append(line(f"M{fmt(x1)} {fmt(y1)}Q{fmt(cx)} {fmt(cy)} {fmt(x2)} {fmt(y2)}"))
    parts += [line(seg(18, 2, 18, 15.5)), shell(circle(18, 18, 2.4)),
              line(seg(14.6, 16.5, 15.8, 17.3)), line(seg(21.4, 16.5, 20.2, 17.3))]
    return parts


@icon("coffin", CAT, "Top view of a six-sided elongated coffin, widest at the shoulders, with a cross on the lid",
      tags=["coffin", "casket", "halloween", "vampire", "funeral", "burial", "death", "spooky"])
def _(S):
    return [
        shell(poly([(9, 2), (15, 2), (19, 8), (15, 22), (9, 22), (5, 8)], closed=True, r=S.r * 0.6)),
        detail(seg(12, 6.5, 12, 16.5)),
        detail(seg(9.5, 9.5, 14.5, 9.5)),
    ]


@icon("egg-dyeing-cup", CAT, "Cup of dye with a wire dipper lifting a half-colored egg above it",
      tags=["egg dyeing", "easter", "dye", "eggs", "cup", "wire dipper", "coloring", "spring"])
def _(S):
    return [
        shell(poly([(4, 12), (18, 12), (17, 21.5), (5, 21.5)], closed=True, r=S.r * 0.5)),
        detail(seg(5.5, 16, 16.5, 16)),
        shell(ellipse(11, 6.6, 3.4, 4.4)),
        solid("M7.6 7.4a3.4 3.6 0 0 0 6.8 0Z"),
        line(seg(14.6, 5.5, 21, 2.5)),
    ]


@icon("empty-tomb", CAT, "Rock-cut tomb opening in a hillside with a large round stone rolled aside and a small cross above",
      tags=["empty tomb", "easter", "resurrection", "tomb", "stone", "christian", "sunday", "cave"])
def _(S):
    return [
        line(seg(12, 1.5, 12, 6)), line(seg(10, 3.4, 14, 3.4)),
        shell(L(S, "M2 21.5V15C2 11 6.5 8.5 12 8.5C17.5 8.5 22 11 22 15V21.5Z",
                "M2 19.5V15C2 11 6.5 8.5 12 8.5C17.5 8.5 22 11 22 15V19.5Q22 21.5 20 21.5H4Q2 21.5 2 19.5Z")),
        detail("M5.2 21.5V17.2a2.4 2.4 0 0 1 4.8 0V21.5"),
        detail(circle(16.6, 17.4, 3)),
    ]


class Turn:
    """Rotate path points clockwise by `deg` about (px, py), then shift by (dx, dy)."""

    def __init__(self, px, py, deg, dx=0.0, dy=0.0):
        a = math.radians(deg)
        self.c, self.s, self.px, self.py, self.dx, self.dy = math.cos(a), math.sin(a), px, py, dx, dy

    def pt(self, x, y):
        X, Y = x - self.px, y - self.py
        return (self.px + X * self.c - Y * self.s + self.dx, self.py + X * self.s + Y * self.c + self.dy)

    def p(self, x, y):
        a, b = self.pt(x, y)
        return f"{fmt(a)} {fmt(b)}"

    def pts(self, pts):
        return [self.pt(x, y) for x, y in pts]


# ============================================================================ gifts and party

@icon("number-candle", CAT, "Birthday candle shaped like a thick numeral one with a wick and a flame on top",
      tags=["number candle", "birthday", "candle", "cake", "numeral", "age", "party", "anniversary"])
def _(S):
    return [
        flame(14.5, 6, 4, 1.5),
        line(seg(14.5, 8.5, 14.5, 6)),
        shell(poly([(7, 13), (12, 8.5), (17.5, 8.5), (17.5, 21.5), (11.5, 21.5), (11.5, 14.5), (7, 14.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("party-blower", CAT, "Paper blowout noisemaker with a mouthpiece and a curled tube partly unrolled into a straight line",
      tags=["party blower", "party horn", "noisemaker", "blowout", "new year", "birthday", "celebration", "whistle"])
def _(S):
    return [
        shell(rect(2.5, 15, 11, 3.6, 0)),
        line("M13.5 16.8C19 16.8 21.5 12.5 19 9.5C16.5 6.8 12.5 9 14.5 11.5"),
        detail(seg(5.5, 15, 5.5, 18.6)),
    ]


@icon("bunting", CAT, "Gently sagging string with a row of triangular pennant flags hanging from it",
      tags=["bunting", "pennant", "flags", "banner", "party", "garland", "decoration", "triangle flags"])
def _(S):
    def y(x):
        return 4 + 2.2 * (1 - ((x - 12) / 10) ** 2)
    out = [line("M2 4Q12 8.4 22 4")]
    for cx in (6, 12, 18):
        out.append(shell(poly([(cx - 2.6, y(cx - 2.6)), (cx + 2.6, y(cx + 2.6)), (cx, y(cx) + 7.5)], closed=True, r=S.r * 0.4),
                         stroke_miterlimit="3"))
    return out


@icon("gift-bag", CAT, "Paper gift bag with a rope handle arching above and tissue paper points sticking out of the top",
      tags=["gift bag", "present", "shopping", "tissue paper", "birthday", "wrapped", "handle", "paper bag"])
def _(S):
    return [
        line("M7 10.5C7 1.5 17 1.5 17 10.5"),
        shell(poly([(9.5, 10), (10.8, 6.5), (12, 9.5), (13.2, 6.5), (14.5, 10)])),
        shell(rect(3.5, 10, 17, 11.5, min(S.R, 2))),
        detail(seg(3.5, 14, 20.5, 14)),
    ]


@icon("gift-tag", CAT, "Luggage-style tag with clipped top corners, a punched hole and a looping string",
      tags=["gift tag", "label", "present", "to and from", "christmas", "tag", "string", "wrapping"])
def _(S):
    return [
        line("M12 7.5C12 2.5 19.5 1.5 20.5 5C21 7.5 18.5 9 15 8.6"),
        shell(poly([(12, 5.5), (18, 10), (18, 21.5), (6, 21.5), (6, 10)], closed=True, r=S.r * 0.5)),
        cut(circle(12, 9.6, 1.3)),
        detail(seg(9.5, 14.5, 14.5, 14.5)),
        detail(seg(9.5, 18, 14.5, 18)),
    ]


@icon("wrapping-paper-roll", CAT, "Roll of patterned paper seen end-on with a sheet partly unrolled flat beneath it",
      tags=["wrapping paper", "gift wrap", "roll", "paper", "present", "christmas", "birthday", "wrapping"])
def _(S):
    return [
        shell(L(S, "M9 15H15C18.5 15 20.5 17 22 19.5V21.5H9Z", "M9 15H15C18.5 15 20.5 17 22 19.5V20Q22 21.5 20.5 21.5H9Z")),
        shell(circle(9, 9.5, 5.5)),
        detail(circle(9, 9.5, 1.6)),
        dot(13.5, 18.6, L(S, 0.9, 1.2)), dot(17, 19.3, L(S, 0.9, 1.2)),
    ]


@icon("gift-bow", CAT, "Large ribbon bow with two looping wings, a knot in the middle and two short trailing tails",
      tags=["bow", "ribbon", "gift bow", "present", "christmas", "wrapping", "tie", "decoration"])
def _(S):
    return [
        shell("M12 11C9.5 4.2 3.2 4 3.3 8C3.5 11.6 9 12 12 11Z"),
        shell("M12 11C14.5 4.2 20.8 4 20.7 8C20.5 11.6 15 12 12 11Z"),
        shell(poly([(10.8, 12.5), (6.5, 21), (9.8, 19), (12, 13)], closed=True, r=S.r * 0.3), stroke_miterlimit="3"),
        shell(poly([(13.2, 12.5), (17.5, 21), (14.2, 19), (12, 13)], closed=True, r=S.r * 0.3), stroke_miterlimit="3"),
        shell(circle(12, 11, 1.6)),
    ]


@icon("gift-stack", CAT, "Three wrapped presents stacked in a small pyramid, each tied with ribbon",
      tags=["gifts", "presents", "stack", "pile", "boxes", "christmas", "birthday", "wrapped"])
def _(S):
    r = L(S, 0.5, 2)
    return [
        shell(rect(2.5, 14.5, 9, 7.5, r)), shell(rect(12.5, 14.5, 9, 7.5, r)),
        shell(rect(7.5, 5.5, 9, 8.5, r)),
        detail(seg(7, 14.5, 7, 22)), detail(seg(17, 14.5, 17, 22)), detail(seg(12, 5.5, 12, 14)),
    ]


@icon("gift-basket", CAT, "Woven basket with a tall arched handle, wrapped items in it and a bow on the handle",
      tags=["gift basket", "hamper", "basket", "present", "easter", "picnic", "wicker", "bow"])
def _(S):
    return [
        line("M5.5 12C5.5 -0.5 18.5 -0.5 18.5 12"),
        solid(poly([(12, 3.6), (9.4, 2), (9.4, 5.2)], closed=True)), solid(poly([(12, 3.6), (14.6, 2), (14.6, 5.2)], closed=True)),
        shell(rect(7, 8, 4, 4, 0)), shell(rect(13, 7, 4, 5, 0)),
        shell(poly([(3.5, 12), (20.5, 12), (18.5, 21.5), (5.5, 21.5)], closed=True, r=S.r * 0.5)),
        detail(seg(4.6, 16.8, 19.4, 16.8)),
    ]


@icon("balloon-arch", CAT, "Arch of clustered round balloons curving from the ground on one side to the other",
      tags=["balloon arch", "balloons", "party", "garland", "wedding", "birthday", "entrance", "decoration"])
def _(S):
    out = []
    for a in (180, 225, 270, 315, 360):
        x, y = polar(12, 17.5, 8.4, a)
        out.append(shell(circle(x, y, L(S, 2.3, 2.5))))
    for a in (202, 248, 292, 338):
        x, y = polar(12, 17.5, 5.8, a)
        out.append(dot(x, y, 1.2))
    return out


@icon("helium-tank", CAT, "Upright gas cylinder with a valve on top and a balloon inflating at its nozzle",
      tags=["helium", "tank", "gas", "balloon", "cylinder", "party", "inflate", "air"])
def _(S):
    return [
        shell(rect(4.5, 10, 8, 12, min(S.R, 3.5))),
        shell(rect(6.5, 6, 4, 4, 0)),
        detail(seg(4.5, 15, 12.5, 15)),
        line(seg(10.5, 7.5, 14, 7.5)),
        shell(circle(18, 7, 3.6)),
    ]


@icon("clown-nose", CAT, "Round ball nose with a small highlight, held by thin elastic bands going round the head",
      tags=["clown nose", "red nose", "circus", "clown", "costume", "comic relief", "elastic", "joke"])
def _(S):
    return [
        shell(circle(12, 12.5, 6)),
        detail("M8.8 10.6Q9.6 9 11.4 8.8"),
        line("M6.2 11.5Q2 11 2 5"),
        line("M17.8 11.5Q22 11 22 5"),
    ]


@icon("toast-glasses", CAT, "Two stemmed flutes tilted together clinking at the rims with small burst lines",
      tags=["toast", "cheers", "clink", "champagne", "flutes", "celebration", "wedding", "new year"])
def _(S):
    def flute(sign):
        t = Turn(12, 21, sign * 12, dx=sign * -6.6)
        bowl = poly(t.pts([(9.3, 3.5), (14.7, 3.5), (13.3, 12), (12, 13.6), (10.7, 12)]), closed=True, r=S.r * 0.5)
        (x1, y1), (x2, y2) = t.pts([(12, 13), (12, 19.5)])
        (b1x, b1y), (b2x, b2y) = t.pts([(9.5, 20), (14.5, 20)])
        return [shell(bowl), line(seg(x1, y1, x2, y2)), line(seg(b1x, b1y, b2x, b2y))]
    return flute(1) + flute(-1) + [line(seg(12, 2.4, 12, 0.8)), line(seg(8.6, 3.2, 7.6, 1.8)), line(seg(15.4, 3.2, 16.4, 1.8))]


@icon("firework-rocket", CAT, "Upright rocket firework with a pointed nose cone, a long stick below and small spark marks at the tip",
      tags=["rocket", "firework", "bottle rocket", "fireworks", "fourth of july", "new year", "pyrotechnics", "launch"])
def _(S):
    return [
        shell(poly([(12, 3.5), (15.5, 8.5), (15.5, 15), (8.5, 15), (8.5, 8.5)], closed=True, r=S.r * 0.4), stroke_miterlimit="3"),
        line(seg(8.5, 15, 6.5, 18)), line(seg(15.5, 15, 17.5, 18)),
        line(seg(12, 15, 12, 22)),
        line(seg(12, 2, 12, 0.6)) if False else dot(12, 1.4, 0.8),
        line(seg(6.4, 4.6, 5, 3.2)), line(seg(17.6, 4.6, 19, 3.2)),
    ]


@icon("firework-fountain", CAT, "Cone-shaped ground firework spraying a fountain of sparks upward and outward",
      tags=["fountain", "firework", "sparks", "sparkler", "ground firework", "fireworks", "celebration", "spray"])
def _(S):
    out = [shell(poly([(8, 14.5), (16, 14.5), (18.5, 21.5), (5.5, 21.5)], closed=True, r=S.r * 0.4))]
    for a, ln in [(-90, 10), (-62, 9), (-118, 9), (-36, 7), (-144, 7)]:
        x1, y1 = polar(12, 13, 2.8, a)
        x2, y2 = polar(12, 13, ln, a)
        out += [line(seg(x1, y1, x2, y2)), dot(x2, y2, 1.1)]
    return out


@icon("pinwheel-firework", CAT, "Spinning wheel firework pinned to a post with curved spark trails around its rim",
      tags=["pinwheel", "catherine wheel", "firework", "spinning", "sparks", "fireworks", "celebration", "spinner"])
def _(S):
    out = [shell(circle(12, 9.5, 3.4)), dot(12, 9.5, 1), line(seg(12, 12.9, 12, 22))]
    for a in (-80, 40, 160):
        out.append(line(arc(12, 9.5, 7.4, a, a + 50)))
        x, y = polar(12, 9.5, 7.4, a + 50)
        out.append(dot(x, y, 1.1))
    return out


@icon("ring-pillow", CAT, "Small square cushion with tassels at the corners and a ring tied at the centre",
      tags=["ring pillow", "ring bearer", "wedding", "cushion", "rings", "ceremony", "tassels", "marriage"])
def _(S):
    return [
        shell("M5 6C9 7.5 15 7.5 19 6C17.6 10.5 17.6 13.5 19 18C15 16.5 9 16.5 5 18C6.4 13.5 6.4 10.5 5 6Z"),
        dot(3.4, 4.6, L(S, 1.4, 1.8)), dot(20.6, 4.6, L(S, 1.4, 1.8)), dot(3.4, 19.4, L(S, 1.4, 1.8)), dot(20.6, 19.4, L(S, 1.4, 1.8)),
        detail(circle(12, 12.6, L(S, 2.6, 2.9))),
    ]


@icon("wedding-bells", CAT, "Two bells hanging together, tied with a ribbon bow at the top",
      tags=["wedding bells", "bells", "marriage", "ceremony", "ribbon", "chime", "married", "church"])
def _(S):
    def bell(sign):
        t = Turn(12, 4, sign * 14, dx=sign * 1.2)
        body = (f"M{t.p(9, 7)}C{t.p(9, 3.4)} {t.p(15, 3.4)} {t.p(15, 7)}C{t.p(15, 11)} {t.p(17.2, 12)} {t.p(17.6, 15)}"
                f"L{t.p(6.4, 15)}C{t.p(6.8, 12)} {t.p(9, 11)} {t.p(9, 7)}Z")
        cx, cy = t.pt(12, 17.3)
        return [shell(body), dot(cx, cy, L(S, 1.2, 1.8))]
    return bell(-1) + bell(1) + [
        solid(poly([(12, 3.4), (8.6, 1.8), (8.6, 5)], closed=True)), solid(poly([(12, 3.4), (15.4, 1.8), (15.4, 5)], closed=True)),
    ]


@icon("just-married-car", CAT, "Side view of a wedding car with tin cans trailing behind it on strings",
      tags=["just married", "wedding car", "honeymoon", "tin cans", "car", "newlyweds", "getaway", "marriage"])
def _(S):
    return [
        shell(poly([(11.5, 10.5), (13.5, 6), (18, 6), (20, 10.5)], closed=True, r=S.r * 0.5)),
        shell(rect(8.5, 10.5, 14, 5.5, min(S.R, 2))),
        dot(12, 16.5, 2.2), dot(19, 16.5, 2.2),
        line(seg(8.5, 12.5, 5, 13.5)), line(seg(8.5, 14, 5.5, 18)),
        dot(3.6, 14, 1.5), dot(4.4, 19.2, 1.5),
    ]


@icon("quaich", CAT, "Shallow wide drinking bowl with a flat lug handle on each side",
      tags=["quaich", "scottish", "scotland", "cup", "friendship cup", "whisky", "bowl", "two handled"])
def _(S):
    return [
        shell("M5.5 9H18.5C18.5 14.5 16 18 12 18C8 18 5.5 14.5 5.5 9Z"),
        shell(rect(1.5, 8.5, 4, 3.4, 0)), shell(rect(18.5, 8.5, 4, 3.4, 0)),
        detail(seg(8, 12.5, 16, 12.5)),
        line(seg(8.5, 21, 15.5, 21)),
    ]
