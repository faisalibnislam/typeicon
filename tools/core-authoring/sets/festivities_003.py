"""TypeIcon Core: festivities (ritual, religious, wedding and cultural celebration objects), batch 3."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import P, fmt, path_to_d, polar, rotation, transform_path

CAT = "festivities"


def L(S, a, b):
    return a if S.name == "line" else b


def flame(x, y, h=4.0, w=1.7):
    """Small solid flame with its base centre at (x, y)."""
    return solid(f"M{fmt(x)} {fmt(y - h)}C{fmt(x + w)} {fmt(y - h * 0.4)} {fmt(x + w)} {fmt(y)} {fmt(x)} {fmt(y)}"
                 f"C{fmt(x - w)} {fmt(y)} {fmt(x - w)} {fmt(y - h * 0.4)} {fmt(x)} {fmt(y - h)}Z")


def ring(S, cx, cy, rx, ry=None, n=10):
    """Circle or ellipse for Rounded; a faceted polygon for Line so the two styles differ."""
    ry = rx if ry is None else ry
    if S.name != "line":
        return circle(cx, cy, rx) if ry == rx else ellipse(cx, cy, rx, ry)
    return poly([(cx + rx * math.cos(math.radians(i * 360 / n - 90)), cy + ry * math.sin(math.radians(i * 360 / n - 90))) for i in range(n)], closed=True)


def star(cx, cy, ro, ri, n=5, rot=-90.0):
    pts = []
    for i in range(n):
        pts.append(polar(cx, cy, ro, rot + 360 / n * i))
        pts.append(polar(cx, cy, ri, rot + 360 / n * i + 180 / n))
    return pts


# ============================================================================ chunk 1: ceremony and church

@icon("handfasting-knot", CAT, "Two cords tied in a loose double loop with two cord ends hanging down",
      tags=["handfasting", "wedding", "knot", "cord", "ceremony", "infinity", "tying the knot"])
def _(S):
    return [
        line(poly([(12, 8), (7, 4.5), (3.5, 8), (7, 11.5), (12, 8), (17, 4.5), (20.5, 8), (17, 11.5), (12, 8)], r=S.r)),
        line(seg(12, 8, 9, 19.5)),
        line(seg(12, 8, 15, 19.5)),
        dot(9, 20, 1.3), dot(15, 20, 1.3),
    ]


@icon("unity-candle", CAT, "Two slim taper candles flanking one thick pillar candle, all lit",
      tags=["unity candle", "wedding", "candles", "ceremony", "marriage", "flame", "union"])
def _(S):
    return [
        shell(rect(8.5, 9.5, 7, 11.5, min(S.R, 2))),
        flame(12, 7, 4, 1.7),
        line(seg(4, 10, 4, 21)),
        line(seg(20, 10, 20, 21)),
        flame(4, 8, 3.2, 1.3), flame(20, 8, 3.2, 1.3),
    ]


@icon("rice-toss", CAT, "Cupped hand below a burst of small rice grains flying upward",
      tags=["rice", "wedding", "toss", "throwing", "grains", "confetti", "send off"])
def _(S):
    pts = []
    for ang, r in [(-165, 7), (-135, 9), (-105, 6.5), (-75, 9.5), (-45, 7), (-15, 8)]:
        x, y = polar(12, 14, r, ang)
        tx, ty = polar(0, 0, 1.0, ang + 70)
        pts.append(line(seg(x - tx, y - ty, x + tx, y + ty)))
    return [
        shell("M3.5 16C4.5 21 8 21.5 12 21.5C16 21.5 19.5 21 20.5 16Z"),
    ] + pts


@icon("chalice", CAT, "Stemmed communion cup with a round wafer floating above it",
      tags=["chalice", "communion", "eucharist", "cup", "goblet", "church", "wafer", "mass"])
def _(S):
    return [
        shell("M6 9H18C18 13 15.5 14.5 12 14.5C8.5 14.5 6 13 6 9Z"),
        line(seg(12, 14.5, 12, 19.5)),
        line(seg(8, 21, 16, 21)),
        dot(12, 4.5, 2.3),
    ]


@icon("church-bell", CAT, "Large bell hanging from a beam next to a pull wheel with a rope",
      tags=["church bell", "bell tower", "steeple", "ring", "chime", "wedding", "worship"])
def _(S):
    return [
        line(seg(3, 3.5, 15, 3.5)),
        line(seg(9, 3.5, 9, 6)),
        shell(poly([(6, 6.5), (12, 6.5), (13, 12), (16, 17), (2, 17), (5, 12)], closed=True, r=S.r)),
        dot(9, 20.3, 1.6),
        shell(circle(18.5, 7.5, 3.5)),
        line(seg(18.5, 11, 18.5, 20)),
    ]


@icon("thurible", CAT, "Incense burner with a small domed lid and round bowl swinging from a ring on two chains",
      tags=["thurible", "censer", "incense", "church", "ritual", "chains", "orthodox"])
def _(S):
    return [
        line(circle(12, 3.8, 1.5)),
        line(seg(11, 5, 5.5, 14)),
        line(seg(13, 5, 18.5, 14)),
        shell(poly([(8, 12), (9, 9.3), (12, 8.3), (15, 9.3), (16, 12)], closed=True, r=S.r)),
        shell("M5.5 14.5H18.5C18.5 18.8 15.5 21 12 21C8.5 21 5.5 18.8 5.5 14.5Z"),
    ]


@icon("bible", CAT, "Closed thick book with a cross on the cover and a ribbon hanging from the bottom",
      tags=["bible", "holy book", "scripture", "church", "gospel", "christian", "testament"])
def _(S):
    return [
        shell(rect(4, 3, 15, 16, min(S.R, 2))),
        detail(seg(7.5, 3, 7.5, 19)),
        detail(seg(13.5, 6.5, 13.5, 14)),
        detail(seg(11, 9, 16, 9)),
        line(seg(15, 19, 15, 22)),
    ]


@icon("pulpit", CAT, "Raised speaking desk with a slanted book rest on a column with stepped base",
      tags=["pulpit", "lectern", "sermon", "preacher", "church", "podium", "speaker"])
def _(S):
    return [
        shell(poly([(4, 4), (20, 4), (17, 12), (7, 12)], closed=True, r=S.r)),
        detail(seg(8.5, 8, 15.5, 8)),
        line(seg(12, 12, 12, 17)),
        shell(poly([(4, 21), (4, 19), (7, 19), (7, 17), (17, 17), (17, 19), (20, 19), (20, 21)], closed=True, r=S.r)),
    ]


@icon("crozier", CAT, "Tall shepherd's staff ending in a curled spiral hook with a band on the shaft",
      tags=["crozier", "bishop", "staff", "crook", "shepherd", "pastoral", "church"])
def _(S):
    return [
        line("M11 21.5V11C11 5.5 13.5 3 16 3C19 3 20 6 18.5 7.5C17.5 8.5 15.5 8 15.5 6.5"),
        line(seg(8.5, 16, 13.5, 16)),
    ]


@icon("ichthys", CAT, "Fish outline made of two arcs that meet at the nose and cross at the tail",
      tags=["ichthys", "jesus fish", "christian", "symbol", "fish", "faith", "church"])
def _(S):
    return [
        line("M3 17Q12 2 21.5 12Q12 22 3 7"),
    ]


@icon("orthodox-cross", CAT, "Cross with a short top bar, a long main bar and a slanted lower footrest bar",
      tags=["orthodox cross", "russian cross", "christian", "church", "three bar cross", "faith", "byzantine"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 21.5)),
        line(seg(9.5, 5.5, 14.5, 5.5)),
        line(seg(6, 10, 18, 10)),
        line(seg(9, 18.5, 15, 15.5)),
    ]


@icon("celtic-cross", CAT, "Latin cross with a ring circling the crossing of its arms",
      tags=["celtic cross", "irish cross", "ring cross", "christian", "church", "heritage", "gravestone"])
def _(S):
    return [
        line(seg(12, 2, 12, 21.5)),
        line(seg(3.5, 9, 20.5, 9)),
        line(circle(12, 9, 4.2)),
    ]


@icon("votive-candles", CAT, "Two rows of small lit candle cups on a stand",
      tags=["votive", "candles", "tealight", "prayer", "church", "memorial", "vigil"])
def _(S):
    cups = []
    for x in (8.5, 15.5):
        cups.append(shell(rect(x - 2, 8, 4, 3.5, 1)))
        cups.append(flame(x, 6.5, 3, 1.2))
    for x in (5, 12, 19):
        cups.append(shell(rect(x - 2, 16.5, 4, 3.5, 1)))
        cups.append(flame(x, 15, 3, 1.2))
    return cups + [line(seg(2, 22, 22, 22))]


@icon("baptismal-font", CAT, "Wide stone basin on a thick pedestal with water ripples inside",
      tags=["baptism", "font", "baptismal", "christening", "church", "water", "basin"])
def _(S):
    return [
        shell("M4 6H20C20 10.5 16.5 13.5 12 13.5C7.5 13.5 4 10.5 4 6Z"),
        detail("M8 9Q10 8 12 9T16 9"),
        shell(poly([(9.5, 14.5), (14.5, 14.5), (15.5, 19), (8.5, 19)], closed=True, r=S.r * 0.5)),
        line(seg(5.5, 21, 18.5, 21)),
    ]


@icon("paschal-candle", CAT, "Tall thick candle marked with a cross, lit, standing on a base",
      tags=["paschal candle", "easter", "candle", "vigil", "church", "cross", "flame"])
def _(S):
    return [
        shell(rect(8, 8, 8, 11.5, min(S.R, 2))),
        detail(seg(12, 10.5, 12, 16)),
        detail(seg(10, 12, 14, 12)),
        flame(12, 6, 4.5, 2),
        line(seg(5.5, 21, 18.5, 21)),
    ]


# ============================================================================ chunk 2: symbols and stalls

@icon("chi-rho", CAT, "Monogram of a letter P on a long stem crossed low down by a large X",
      tags=["chi rho", "monogram", "christogram", "early christian", "church", "symbol", "labarum"])
def _(S):
    return [
        line("M12 3H15A3 3 0 0 1 15 9H12"),
        line(seg(12, 3, 12, 21.5)),
        line(seg(6.5, 10.5, 17.5, 20.5)),
        line(seg(17.5, 10.5, 6.5, 20.5)),
    ]


@icon("alpha-omega", CAT, "The Greek letters alpha and omega side by side",
      tags=["alpha", "omega", "greek letters", "beginning and end", "christian", "symbol", "first and last"])
def _(S):
    return [
        line("M10.5 17C8 13 5.5 9 3.5 10.5C1.5 12.5 3.5 17.5 6.5 16C8.5 15 10 12 11 8"),
        line("M13.5 8.5C13.5 14 14 16.5 16 16.5C17.5 16.5 18 14 18 11.5C18 14 18.5 16.5 20 16.5C22 16.5 22.5 14 22.5 8.5"),
    ]


@icon("crown-of-thorns", CAT, "Round ring of twisted branches with sharp solid thorns pointing outward",
      tags=["crown of thorns", "thorns", "passion", "good friday", "christian", "easter", "lent"])
def _(S):
    th = []
    for i in range(7):
        a = i * 360 / 7 + 10
        p0 = polar(12, 12, 6.3, a - 11)
        p1 = polar(12, 12, 6.3, a + 11)
        p2 = polar(12, 12, 10.6, a + 28)
        th.append(solid(poly([p0, p2, p1], closed=True)))
    return [line(ring(S, 12, 12, 6.3, None, 12))] + th


@icon("sacred-heart-emblem", CAT, "Heart topped with a small cross and short flame marks either side",
      tags=["sacred heart", "heart", "cross", "devotion", "catholic", "christian", "flame"])
def _(S):
    return [
        shell("M12 21C6 17 3.5 13.5 3.5 11A4.25 4.25 0 0 1 12 9.5A4.25 4.25 0 0 1 20.5 11C20.5 13.5 18 17 12 21Z"),
        line(seg(12, 2, 12, 7)),
        line(seg(9.5, 4, 14.5, 4)),
    ]


@icon("jerusalem-cross", CAT, "Large cross whose arms end in crossbars, with a dot in each quadrant",
      tags=["jerusalem cross", "crusader cross", "five-fold cross", "christian", "pilgrimage", "holy land", "heraldry"])
def _(S):
    return [
        line(seg(12, 4, 12, 20)),
        line(seg(4, 12, 20, 12)),
        line(seg(9.5, 4, 14.5, 4)),
        line(seg(9.5, 20, 14.5, 20)),
        line(seg(4, 9.5, 4, 14.5)),
        line(seg(20, 9.5, 20, 14.5)),
        dot(7.5, 7.5, 1.4), dot(16.5, 7.5, 1.4), dot(7.5, 16.5, 1.4), dot(16.5, 16.5, 1.4),
    ]


@icon("halo", CAT, "Flat floating ring with short rays radiating above it",
      tags=["halo", "angel", "saint", "holy", "glory", "nimbus", "heavenly"])
def _(S):
    return [
        line(ellipse(12, 15, 8.5, 3.3)),
        line(seg(12, 2.5, 12, 7.5)),
        line(seg(5, 5, 7, 8.5)),
        line(seg(19, 5, 17, 8.5)),
    ]


@icon("holy-water-stoup", CAT, "Wall niche with a small cross above a wide basin holding holy water",
      tags=["holy water", "stoup", "font", "church", "catholic", "blessing", "basin"])
def _(S):
    return [
        line(poly([(6, 15), (6, 8), (12, 2.5), (18, 8), (18, 15)], r=S.r * 1.5)),
        line(seg(12, 5.5, 12, 11)),
        line(seg(9.5, 7.8, 14.5, 7.8)),
        shell("M3 15.5H21C21 19.5 17 21.5 12 21.5C7 21.5 3 19.5 3 15.5Z"),
    ]


@icon("kara-bracelet", CAT, "Plain thick steel bangle seen at a slight angle",
      tags=["kara", "bracelet", "bangle", "sikh", "steel", "ring", "wristband"],
      filled=lambda: __import__("dsl").D(__import__("dsl").P(ellipse(12, 12.5, 10.5, 8.5)), __import__("dsl").P(ellipse(12, 11.5, 4.5, 2.5))))
def _(S):
    return [
        line(ring(S, 12, 12.5, 9.5, 7.5, 12)),
        line(ring(S, 12, 11.5, 5.5, 3.5, 12)),
    ]


@icon("nine-pointed-star-emblem", CAT, "Star with nine evenly spaced points around a small centre dot",
      tags=["nine pointed star", "star", "baha'i", "emblem", "enneagram", "nonagram", "faith symbol"])
def _(S):
    return [
        shell(poly(star(12, 12, 9, 5.2, 9), closed=True, r=S.r * 0.4), stroke_miterlimit="3"),
        dot(12, 12, 1.4),
    ]


@icon("faravahar", CAT, "Winged ring symbol with feathered wings spread wide and a forked tail below",
      tags=["faravahar", "farvahar", "zoroastrian", "persian", "winged symbol", "iran", "emblem"])
def _(S):
    return [
        line(circle(12, 9, 2.6)),
        line(seg(9, 8, 3, 5.5)),
        line(seg(9, 10.5, 2.5, 10.5)),
        line(seg(9.5, 13, 4, 15.5)),
        line(seg(15, 8, 21, 5.5)),
        line(seg(15, 10.5, 21.5, 10.5)),
        line(seg(14.5, 13, 20, 15.5)),
        line(seg(12, 12, 12, 16.5)),
        line(seg(12, 16.5, 9, 21.5)),
        line(seg(12, 16.5, 15, 21.5)),
    ]


@icon("flower-of-life", CAT, "Six overlapping circles forming a rosette inside a bounding circle",
      tags=["flower of life", "sacred geometry", "rosette", "overlapping circles", "mandala", "spiritual", "pattern"])
def _(S):
    petals = []
    for i in range(6):
        x, y = polar(12, 12, 4.2, i * 60)
        petals.append(line(ring(S, x, y, 4.2, None, 8)))
    return [line(ring(S, 12, 12, 9.5, None, 12))] + petals


def _unalome_pts():
    cx, cy = 12.0, 17.0
    pts = []
    n = 36
    for i in range(n + 1):
        th = math.radians(630.0 * i / n)
        r = 0.9 + 4.6 * i / n
        pts.append((cx + r * math.cos(th), cy + r * math.sin(th)))
    pts += [(14.5, 9.5), (9.5, 7.5), (12, 5.5)]
    return pts


@icon("unalome", CAT, "Line that coils into a spiral at the bottom, zigzags in the middle and ends in a dot",
      tags=["unalome", "path to enlightenment", "buddhist", "spiral", "tattoo", "spiritual", "journey"])
def _(S):
    return [
        line(poly(_unalome_pts())),
        line(seg(12, 5.5, 12, 4.5)),
        dot(12, 2.6, 1.3),
    ]


@icon("triple-moon", CAT, "Full moon circle flanked by a crescent on each side with horns pointing outward",
      tags=["triple moon", "goddess", "wicca", "pagan", "lunar", "moon phases", "crescent"])
def _(S):
    return [
        shell(circle(12, 12, 4)),
        line("M3.5 5Q6.8 12 3.5 19"),
        line("M20.5 5Q17.2 12 20.5 19"),
    ]


@icon("fair-booth", CAT, "Small market stall with a striped awning, scalloped edge and a counter",
      tags=["fair", "booth", "stall", "carnival", "market", "kiosk", "awning", "stand"])
def _(S):
    return [
        shell("M5 3.5H19L22 9.5A2.5 2.5 0 0 1 17 9.5A2.5 2.5 0 0 1 12 9.5A2.5 2.5 0 0 1 7 9.5A2.5 2.5 0 0 1 2 9.5Z"),
        detail(seg(8.5, 3.5, 7.5, 9)),
        detail(seg(12, 3.5, 12, 9)),
        detail(seg(15.5, 3.5, 16.5, 9)),
        line(seg(5, 12.5, 5, 16)),
        line(seg(19, 12.5, 19, 16)),
        shell(rect(3, 16, 18, 5, min(S.R, 1.5))),
    ]


# ============================================================================ chunk 3: ceremony, pageantry and charms

@icon("ribbon-cutting", CAT, "Open scissors with a ribbon stretched across the blade tips",
      tags=["ribbon cutting", "scissors", "grand opening", "inauguration", "launch", "ceremony", "opening day"])
def _(S):
    return [
        line(seg(4, 6, 19, 15)),
        line(seg(4, 18, 19, 9)),
        line(circle(20.3, 16.3, 2.2)),
        line(circle(20.3, 7.7, 2.2)),
        line(seg(1.8, 12, 6.5, 12)),
    ]


@icon("key-to-the-city", CAT, "Large ceremonial key with a round bow, a collar band and two teeth",
      tags=["key to the city", "ceremonial key", "honor", "award", "welcome", "civic", "big key"])
def _(S):
    return [
        line(ring(S, 12, 6.2, 4.2, None, 10)),
        dot(12, 6.2, 1.2),
        line(seg(12, 10.5, 12, 21.5)),
        line(seg(9.5, 12.5, 14.5, 12.5)),
        line(seg(12, 17, 16.5, 17)),
        line(seg(12, 20.3, 15.5, 20.3)),
    ]


@icon("ceremonial-mace", CAT, "Short staff with a crowned round head and decorative bands along the shaft",
      tags=["mace", "ceremonial mace", "parliament", "staff of office", "authority", "royal", "regalia"])
def _(S):
    return [
        line(poly([(8.5, 5.5), (8.5, 3.5), (10.3, 4.8), (12, 3.5), (13.7, 4.8), (15.5, 3.5), (15.5, 5.5)])),
        shell(circle(12, 11, 3.8)),
        line(seg(12, 14.8, 12, 21.5)),
        line(seg(9.5, 16.5, 14.5, 16.5)),
        line(seg(10, 19.5, 14, 19.5)),
    ]


@icon("remembrance-poppy", CAT, "Four-petal poppy with a dark centre, a stem and one leaf",
      tags=["poppy", "remembrance", "memorial day", "armistice", "veteran", "commemoration", "flower"])
def _(S):
    return [
        shell(circle(8.8, 7.3, 3.7)), shell(circle(15.2, 7.3, 3.7)),
        shell(circle(9, 12.7, 3.5)), shell(circle(15, 12.7, 3.5)),
        dot(12, 10, 2),
        line(seg(12, 16.5, 12, 21.5)),
        line(seg(12, 20, 17, 17.5)),
    ]


@icon("candlelight-vigil", CAT, "Lit slim candle standing in a paper cup drip guard with glow marks either side of the flame",
      tags=["vigil", "candlelight", "candle", "memorial", "remembrance", "mourning", "paper cup"])
def _(S):
    return [
        flame(12, 7, 4.5, 1.9),
        line(seg(12, 7, 12, 15)),
        shell(poly([(6, 15), (18, 15), (15.5, 21.5), (8.5, 21.5)], closed=True, r=S.r * 0.5)),
        line(seg(5.5, 3.5, 7.5, 5.5)),
        line(seg(18.5, 3.5, 16.5, 5.5)),
    ]


@icon("wreath-on-stand", CAT, "Thick round wreath resting on a three-legged stand",
      tags=["wreath", "funeral", "memorial", "flowers", "stand", "easel", "condolence"])
def _(S):
    return [
        line(ring(S, 12, 8.5, 7, None, 14)),
        line(ring(S, 12, 8.5, 3.2, None, 10)),
        line(seg(12, 16.5, 6.5, 21.5)),
        line(seg(12, 16.5, 17.5, 21.5)),
        line(seg(12, 16.5, 12, 21.5)),
    ]


@icon("pilgrim-hat", CAT, "Tall flat-crowned hat with a wide brim and a square buckle on the band",
      tags=["pilgrim hat", "thanksgiving", "buckle", "colonial", "costume", "hat", "autumn"])
def _(S):
    return [
        shell(poly([(7.5, 3), (16.5, 3), (17.8, 14), (22, 15.5), (22, 18.5), (2, 18.5), (2, 15.5), (6.2, 14)], closed=True, r=S.r * 0.6)),
        detail(rect(9.5, 7.5, 5, 5)),
        detail(seg(7, 10, 9.5, 10)),
        detail(seg(14.5, 10, 17, 10)),
    ]


@icon("ball-drop", CAT, "Round ball at the top of a tall mast with light rays around it",
      tags=["ball drop", "new year's eve", "countdown", "times square", "midnight", "celebration", "mast"])
def _(S):
    rays = []
    for a in (-90, -45, -135, 0, 180, 40, 140):
        x0, y0 = polar(12, 10, 6, a)
        x1, y1 = polar(12, 10, 8, a)
        rays.append(line(seg(x0, y0, x1, y1)))
    return [
        shell(circle(12, 10, 3.5)),
        line(seg(12, 13.5, 12, 21.5)),
    ] + rays


@icon("gamelan-metallophone", CAT, "Row of tapering metal bars over a carved trough frame with a mallet beside it",
      tags=["gamelan", "metallophone", "xylophone", "indonesian", "bronze", "instrument", "mallet", "javanese"])
def _(S):
    return [
        line(seg(5, 4.5, 5, 14)),
        line(seg(9.5, 6.5, 9.5, 14)),
        line(seg(14, 8.5, 14, 14)),
        line(seg(18.5, 10.5, 18.5, 14)),
        shell(poly([(2.5, 14.5), (21.5, 14.5), (19, 20.5), (5, 20.5)], closed=True, r=S.r)),
        dot(21.3, 3.3, 1.6),
        line(seg(21.3, 3.3, 17.5, 7.5)),
    ]


@icon("kite-reel", CAT, "Round spool wound with string, with handles on both ends of its axle and string trailing up",
      tags=["kite", "reel", "spool", "string", "kite flying", "festival", "spindle"])
def _(S):
    return [
        shell(circle(12, 14, 6.5)),
        detail(circle(12, 14, 3.2)),
        dot(12, 14, 1.2),
        line(seg(2.5, 14, 5.5, 14)),
        line(seg(2.5, 11.5, 2.5, 16.5)),
        line(seg(18.5, 14, 21.5, 14)),
        line(seg(21.5, 11.5, 21.5, 16.5)),
        line("M13 7.5C13 4.5 17 5 18.5 2.5"),
    ]


@icon("pierced-lamp-pot", CAT, "Round clay pot punched with small holes, with light rays rising from its neck",
      tags=["pierced pot", "lamp", "clay pot", "diya", "lantern", "candle holder", "glowing", "luminary"])
def _(S):
    return [
        shell("M8.5 8.5H15.5C15.5 10 19 11.5 19 16C19 19.5 16 21.5 12 21.5C8 21.5 5 19.5 5 16C5 11.5 8.5 10 8.5 8.5Z"),
        dot(9, 15, 1), dot(12, 13, 1), dot(15, 15, 1), dot(10.5, 18, 1), dot(13.5, 18, 1),
        line(seg(12, 2, 12, 5)),
        line(seg(6.5, 3.5, 8.5, 5.5)),
        line(seg(17.5, 3.5, 15.5, 5.5)),
    ]


@icon("palanquin", CAT, "Small curtained carriage with a wide upturned roof, carried on a long pole",
      tags=["palanquin", "litter", "sedan chair", "carriage", "procession", "bride", "royal"])
def _(S):
    return [
        shell(poly([(4, 10), (12, 4.5), (20, 10)], closed=True, r=S.r), stroke_miterlimit="2"),
        shell(rect(5.5, 11, 13, 6, min(S.R, 1.5))),
        detail(seg(12, 11, 12, 17)),
        line(seg(2, 20.5, 22, 20.5)),
        line(seg(8, 17, 8, 20.5)),
        line(seg(16, 17, 16, 20.5)),
    ]


def _elephant_body():
    from dsl import P, U
    from geometry import path_to_d
    return path_to_d(U(P(rect(9, 6.5, 12, 9.5, 4)), P(circle(6.5, 9.5, 4))))


@icon("decorated-elephant", CAT, "Side view of an elephant wearing a bordered blanket on its back and a plate on its forehead",
      tags=["decorated elephant", "festival elephant", "parade", "procession", "indian", "pageant", "caparison"])
def _(S):
    return [
        shell(_elephant_body()),
        detail(rect(11.5, 8.5, 7, 4, 1)),
        dot(6.5, 7, 1),
        line("M3.8 12.5Q2 16 3.8 20"),
        line(seg(11.5, 15, 11.5, 21.5)),
        line(seg(18.5, 15, 18.5, 21.5)),
    ]


@icon("lucky-coin-charm", CAT, "Round coin with a square hole, tied with a knotted cord and a tassel below",
      tags=["lucky coin", "charm", "coin", "tassel", "fortune", "new year", "feng shui", "good luck"])
def _(S):
    return [
        shell(circle(12, 8.5, 6.5)),
        detail(rect(9.5, 6, 5, 5)),
        dot(12, 18, 1.6),
        line(seg(12, 18.5, 10, 22)),
        line(seg(12, 18.5, 12, 22)),
        line(seg(12, 18.5, 14, 22)),
    ]


@icon("lucky-gold-ingot", CAT, "Boat-shaped gold ingot with upturned ends and a rounded dome rising in the middle",
      tags=["gold ingot", "yuanbao", "sycee", "lucky", "fortune", "wealth", "new year", "prosperity"])
def _(S):
    return [
        shell("M2.5 8C4.5 10.5 7.5 11 9 11C9 6 10 4.5 12 4.5C14 4.5 15 6 15 11C16.5 11 19.5 10.5 21.5 8C21.5 14 19 18 16 18H8C5 18 2.5 14 2.5 8Z"),
        detail(seg(7.5, 14.5, 16.5, 14.5)),
    ]


# ============================================================================ chunk 4: celebrations, sweets and keepsakes

def rot_d(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def tilt_rect(cx, cy, w, h, deg):
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    pts = [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]
    return [(cx + x * c - y * sn, cy + x * sn + y * c) for x, y in pts]


@icon("megillah-case", CAT, "Upright scroll case with a crown on top and a parchment slid out sideways",
      tags=["megillah", "scroll", "purim", "esther", "jewish", "case", "parchment"])
def _(S):
    return [
        shell(rect(3, 8.5, 6, 12.5, min(S.R, 1.5))),
        line(poly([(3, 6.5), (3, 3.5), (6, 5.3), (9, 3.5), (9, 6.5)])),
        shell(rect(9, 10.5, 12, 9.5, 1)),
        detail(seg(18.5, 10.5, 18.5, 20)),
        detail(seg(11.5, 13.8, 15.4, 13.8)),
        detail(seg(11.5, 16.8, 15.4, 16.8)),
    ]


@icon("christingle", CAT, "Orange with a lit candle on top, a ribbon band round its middle and sticks poking out",
      tags=["christingle", "orange", "advent", "candle", "christmas", "church", "ribbon"])
def _(S):
    return [
        shell(circle(12, 14.5, 6.5)),
        detail(seg(5.5, 15, 18.5, 15)),
        line(seg(12, 8, 12, 4.5)),
        flame(12, 4.5, 3, 1.2),
        line(seg(8, 10, 5, 6.5)),
        line(seg(16, 10, 19, 6.5)),
    ]


@icon("monstrance", CAT, "Sunburst of rays around a small round window on a stem and base",
      tags=["monstrance", "host", "eucharist", "adoration", "catholic", "church", "sunburst"])
def _(S):
    rays = []
    for a in (-90, -45, -135, 0, 180, 45, 135):
        x0, y0 = polar(12, 9, 5, a)
        x1, y1 = polar(12, 9, 7.2, a)
        rays.append(line(seg(x0, y0, x1, y1)))
    return [
        line(circle(12, 9, 2.4)),
        line(seg(12, 12, 12, 18)),
        line(seg(9.5, 15, 14.5, 15)),
        line(seg(7, 21, 17, 21)),
    ] + rays


@icon("temple-chariot", CAT, "Tall stepped tower on a platform with two spoked wheels and a rope trailing forward",
      tags=["temple chariot", "rath", "procession", "festival", "car festival", "juggernaut", "wheels"])
def _(S):
    return [
        line(seg(12, 1.8, 12, 4.5)),
        shell(rect(10, 4.5, 4, 3.5, 1)),
        shell(rect(8, 8.5, 8, 3.5, 1)),
        shell(rect(6, 12.5, 12, 3, 1)),
        shell(rect(4, 16, 16, 2.2, 1)),
        line(circle(8, 20.3, 1.7)), line(circle(16, 20.3, 1.7)),
        line("M4 17C2 18 2 20 2.5 21.5"),
    ]


@icon("pair-of-golden-fish", CAT, "Two fish standing on their tails and leaning towards each other",
      tags=["golden fish", "pair of fish", "auspicious", "buddhist", "fish", "lucky", "matsya"])
def _(S):
    return [
        shell(rot_d(ellipse(7.8, 10, 3.2, 7), 12, 7.8, 10)),
        shell(rot_d(ellipse(16.2, 10, 3.2, 7), -12, 16.2, 10)),
        line(seg(7.3, 17.5, 4.8, 21.5)),
        line(seg(7.3, 17.5, 9, 21.5)),
        line(seg(16.7, 17.5, 19.2, 21.5)),
        line(seg(16.7, 17.5, 15, 21.5)),
        dot(9.3, 5.6, 0.9), dot(14.7, 5.6, 0.9),
    ]


@icon("water-offering-bowls", CAT, "Row of small bowls filled with water sitting on a shelf line",
      tags=["water offering", "offering bowls", "buddhist", "altar", "shrine", "bowls", "seven bowls"])
def _(S):
    bowls = []
    for x in (2, 9.5, 17):
        bowls.append(solid(f"M{fmt(x)} 10.5H{fmt(x + 5)}C{fmt(x + 5)} 13.5 {fmt(x + 3.5)} 15.5 {fmt(x + 2.5)} 15.5C{fmt(x + 1.5)} 15.5 {fmt(x)} 13.5 {fmt(x)} 10.5Z"))
        bowls.append(dot(x + 2.5, 6.8, 1.0))
    return bowls + [line(seg(2, 19, 22, 19))]


@icon("save-the-date", CAT, "Calendar page with binding rings and a solid heart marking one date",
      tags=["save the date", "calendar", "wedding", "heart", "invitation", "date", "engagement"])
def _(S):
    return [
        shell(rect(3, 5, 18, 16, min(S.R, 3))),
        line(seg(8, 2.5, 8, 6.5)),
        line(seg(16, 2.5, 16, 6.5)),
        detail(seg(3, 10, 21, 10)),
        Part("dot", "M12 19.2C9 17 8 15.6 8 14.3A2.1 2.1 0 0 1 12 13.6A2.1 2.1 0 0 1 16 14.3C16 15.6 15 17 12 19.2Z"),
    ]


@icon("petal-confetti-cone", CAT, "Paper cone with small flower petals spilling from its open top",
      tags=["petal", "confetti", "cone", "wedding", "flower petals", "toss", "send off"])
def _(S):
    return [
        shell(poly([(6, 11), (18, 11), (12, 21.5)], closed=True, r=S.r)),
        dot(8.5, 6.3, 1.3), dot(12.3, 4.3, 1.3), dot(16, 6.3, 1.3), dot(10.5, 8.6, 1.1), dot(14.3, 8.6, 1.1),
        dot(20.3, 13.5, 1.1), dot(21, 18, 1.1),
    ]


@icon("flower-girl-basket", CAT, "Half-round basket with an arched handle and petals inside",
      tags=["flower girl", "basket", "petals", "wedding", "bridal party", "flowers", "handle"])
def _(S):
    return [
        shell("M4 12H20C20 17.5 16.8 21 12 21C7.2 21 4 17.5 4 12Z"),
        detail(seg(4, 16, 20, 16)),
        line("M6 12C6 2 18 2 18 12"),
        dot(9, 9.8, 1.1), dot(12, 8.2, 1.1), dot(15, 9.8, 1.1),
    ]


@icon("favor-box", CAT, "Pillow-shaped gift box with curved sides, a ribbon band and a bow",
      tags=["favor box", "party favor", "wedding favor", "pillow box", "gift", "ribbon", "bow"])
def _(S):
    tri = lambda pts: Part("dot", poly(pts, closed=True, r=0.6))
    return [
        shell("M4 5.5H20Q18 12 20 18.5H4Q6 12 4 5.5Z"),
        detail(seg(4.6, 12, 19.4, 12)),
        tri([(12, 12), (7.5, 9), (7.5, 15)]),
        tri([(12, 12), (16.5, 9), (16.5, 15)]),
    ]


@icon("wedding-lasso", CAT, "Corded loop twisted into a tall figure eight with a small cross inside the lower loop",
      tags=["wedding lasso", "lazo", "wedding cord", "rosary loop", "ceremony", "figure eight", "cross"])
def _(S):
    return [
        line("M12 11.5C8 9 7.5 2.5 12 2.5C16.5 2.5 16 9 12 11.5C8 14 7.5 21.5 12 21.5C16.5 21.5 16 14 12 11.5Z"),
        line(seg(12, 15, 12, 19.5)),
        line(seg(10.3, 16.5, 13.7, 16.5)),
    ]


@icon("unity-sand", CAT, "Two tilted vials pouring sand into one tall jar that shows layered bands",
      tags=["unity sand", "sand ceremony", "wedding", "jar", "vials", "layers", "ceremony"])
def _(S):
    return [
        shell(poly(tilt_rect(5, 5.5, 3.6, 7, -45), closed=True, r=S.r * 0.4)),
        shell(poly(tilt_rect(19, 5.5, 3.6, 7, 45), closed=True, r=S.r * 0.4)),
        shell(rect(7, 10.5, 10, 10.5, min(S.R, 2))),
        detail(seg(7, 14.5, 17, 14.5)),
        detail(seg(7, 17.8, 17, 17.8)),
    ]


@icon("number-balloon", CAT, "Foil balloon shaped like the numeral one with a curly string at its base",
      tags=["number balloon", "foil balloon", "birthday", "anniversary", "numeral", "milestone", "party"])
def _(S):
    return [
        shell(poly([(9, 3.5), (14.5, 3.5), (14.5, 17.5), (9.5, 17.5), (9.5, 9.5), (5, 11.5)], closed=True, r=S.r * 0.6)),
        line("M12 17.5Q10 19.5 12.5 20.5Q14 21.3 13 22"),
    ]


@icon("star-balloon", CAT, "Five-pointed foil star balloon with a curly ribbon below",
      tags=["star balloon", "foil balloon", "party", "birthday", "celebration", "ribbon", "helium"])
def _(S):
    return [
        shell(poly(star(12, 10.5, 7.6, 3.9), closed=True, r=S.r * 0.5), stroke_miterlimit="2.5"),
        line("M12 15.5C10 17.5 14 18.5 12 21"),
    ]


@icon("sun-cross", CAT, "Circle with an equal-armed cross inside whose arms touch the circle at four points",
      tags=["sun cross", "solar cross", "wheel cross", "ancient symbol", "heritage", "pagan", "circle cross"])
def _(S):
    return [
        line(ring(S, 12, 12, 9, None, 16)),
        line(seg(12, 3, 12, 21)),
        line(seg(3, 12, 21, 12)),
    ]


@icon("school-cone", CAT, "Tall cone of gifts with a ruffled fabric top gathered at a ribbon line",
      tags=["school cone", "schultute", "first day of school", "gift cone", "sweets", "back to school", "ruffle"])
def _(S):
    return [
        shell(poly([(6, 10), (18, 10), (12, 21.5)], closed=True, r=S.r)),
        line(poly([(6, 10), (7.5, 4.5), (10, 7.5), (12, 4), (14, 7.5), (16.5, 4.5), (18, 10)], r=S.r * 0.5)),
    ]


# ============================================================================ chunk 5: ornaments, sweets and offerings

@icon("pickle-ornament", CAT, "Bumpy pickle-shaped tree ornament hanging from a small cap and hook",
      tags=["pickle ornament", "christmas pickle", "tree ornament", "german tradition", "hook", "decoration", "christmas"])
def _(S):
    return [
        shell(rot_d(ring(S, 12, 13.5, 4.3, 8, 14), 14, 12, 13.5)),
        shell(rect(10.3, 3.8, 4, 3, min(S.R, 1))),
        line("M12.3 3.8V3C12.3 1.8 14.3 1.8 14.3 3"),
        dot(11, 11.5, 0.9), dot(13.6, 14.5, 0.9), dot(11.3, 17.5, 0.9), dot(14, 10, 0.8),
    ]


@icon("graduation-stole", CAT, "Long narrow stole draped as an upside-down V with a stripe band and fringe on each end",
      tags=["graduation stole", "sash", "honor cords", "graduation", "regalia", "commencement", "fringe"])
def _(S):
    return [
        shell(poly([(8.5, 3.5), (15.5, 3.5), (20, 19), (15.5, 19), (12, 9), (8.5, 19), (4, 19)], closed=True, r=S.r * 0.4)),
        detail(seg(5.6, 15.5, 8, 15.5)),
        detail(seg(16, 15.5, 18.4, 15.5)),
        line(seg(5.3, 19, 5.3, 22)), line(seg(7.6, 19, 7.6, 22)),
        line(seg(16.4, 19, 16.4, 22)), line(seg(18.7, 19, 18.7, 22)),
    ]


def _koru_pts():
    cx, cy = 12.0, 10.0
    pts = []
    n = 40
    for i in range(n + 1):
        th = math.radians(180 + 540.0 * i / n)
        r = 1.0 + 6.5 * i / n
        pts.append((cx + r * math.cos(th), cy + r * math.sin(th)))
    # tail: leave the outer end (right side) heading down, curve to bottom centre-left
    p0, p1, p2, p3 = pts[-1], (pts[-1][0], 16.0), (17.5, 19.0), (12.5, 21.5)
    for k in range(1, 9):
        t = k / 8
        u = 1 - t
        pts.append((u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]))
    return pts


@icon("koru", CAT, "Unfurling fern frond with a tight coil at the end of a curved stem",
      tags=["koru", "fern", "spiral", "maori", "new zealand", "new beginnings", "unfurling", "frond"])
def _(S):
    return [line(poly(_koru_pts()))]


@icon("royal-orb", CAT, "Round orb with a band around its middle and another over the top, crowned with a small cross",
      tags=["royal orb", "globus cruciger", "regalia", "coronation", "sovereign", "monarch", "crown jewels"])
def _(S):
    return [
        shell(circle(12, 14, 7)),
        detail("M5 13.5Q12 17.5 19 13.5"),
        detail(ellipse(12, 14, 3.2, 7)),
        line(seg(12, 2.5, 12, 7.5)),
        line(seg(10, 4.3, 14, 4.3)),
    ]


@icon("spooky-tree", CAT, "Bare twisted tree with crooked grasping branches and a knothole face on its trunk",
      tags=["spooky tree", "haunted tree", "halloween", "bare tree", "creepy", "scary", "branches"])
def _(S):
    return [
        shell("M8.5 21.5C9.5 18 9 14.5 10 11H14C15 14.5 14.5 18 15.5 21.5Z"),
        line(poly([(10.3, 12), (6, 8.5), (3.5, 9.5)])),
        line(poly([(6, 8.5), (5, 4.5)])),
        line(poly([(13.7, 12), (18, 8), (20.5, 9)])),
        line(poly([(18, 8), (19, 4)])),
        line(poly([(12, 11.5), (12, 6), (10, 3)])),
        dot(10.9, 15.5, 0.8), dot(13.1, 15.5, 0.8),
    ]


@icon("wish-tree", CAT, "Tree with a round leafy canopy hung with small paper tags and ribbons",
      tags=["wish tree", "tree", "tags", "wishes", "ribbons", "prayers", "tanabata", "hopes"])
def _(S):
    return [
        shell(ring(S, 12, 9.5, 7.5, None, 14)),
        line(seg(12, 16, 12, 22)),
        Part("dot", rect(8.3, 6, 1.8, 3.6, 0.4)),
        Part("dot", rect(13.8, 5.5, 1.8, 3.6, 0.4)),
        Part("dot", rect(11.1, 10.2, 1.8, 3.6, 0.4)),
        Part("dot", rect(7.4, 11, 1.8, 3.2, 0.4)),
        Part("dot", rect(15, 10.6, 1.8, 3.2, 0.4)),
    ]


@icon("sparkler", CAT, "Thin wire sparkler stick with a burst of sparks radiating from its lit tip",
      tags=["sparkler", "fireworks", "new year", "celebration", "sparks", "independence day", "diwali"])
def _(S):
    rays = []
    for i, a in enumerate((-90, -50, -10, 30, -130, -170, 170)):
        r1 = 6.8 if i % 2 == 0 else 5.2
        x0, y0 = polar(14, 10, 3, a)
        x1, y1 = polar(14, 10, r1, a)
        rays.append(line(seg(x0, y0, x1, y1)))
    return [
        line(seg(2.5, 21.5, 12.3, 11.7)),
        dot(14, 10, 1.5),
    ] + rays


@icon("mithai-box", CAT, "Open box of round sweets and diamond-shaped sweets arranged in neat rows",
      tags=["mithai", "sweets box", "indian sweets", "diwali", "gift box", "barfi", "festival"])
def _(S):
    dia = lambda x, y: Part("dot", poly([(x, y - 2), (x + 2, y), (x, y + 2), (x - 2, y)], closed=True))
    return [
        shell(rect(3, 6, 18, 15, min(S.R, 3))),
        dot(8, 11, 1.7), dia(12, 11), dot(16, 11, 1.7),
        dia(8, 16.3), dot(12, 16.3, 1.7), dia(16, 16.3),
    ]


@icon("moon-viewing-dumplings", CAT, "Pyramid of round white dumplings on a stand under a large arc of the full moon",
      tags=["tsukimi", "moon viewing", "dango", "mid-autumn", "dumplings", "harvest moon", "full moon"])
def _(S):
    return [
        line(arc(12, 12, 9.5, 165, 375)),
        dot(8, 16, 1.9), dot(12.2, 16, 1.9), dot(16.4, 16, 1.9),
        dot(10.1, 12, 1.9), dot(14.3, 12, 1.9),
        dot(12.2, 8, 1.9),
        line(seg(6, 20, 18.5, 20)),
    ]


@icon("may-basket", CAT, "Paper cone basket with a tall looped handle and blossoms poking out of the top",
      tags=["may basket", "may day", "spring", "flowers", "cone", "handle", "door basket"])
def _(S):
    return [
        shell(poly([(6, 11), (18, 11), (12, 21.5)], closed=True, r=S.r)),
        line("M7 11C7 -0.5 17 -0.5 17 11"),
        dot(9.8, 8, 1.4), dot(14.2, 8, 1.4), dot(12, 5.5, 1.4),
    ]


def _coil_pts():
    cx, cy = 12.0, 12.5
    pts = []
    n = 60
    for i in range(n + 1):
        th = math.radians(270 + 720.0 * i / n)
        r = 1.5 + 6.5 * i / n
        pts.append((cx + r * math.cos(th), cy + r * math.sin(th)))
    return pts


@icon("incense-coil", CAT, "Flat spiral incense coil hanging from a short hook",
      tags=["incense coil", "spiral incense", "temple", "joss", "smoke", "hanging", "worship"])
def _(S):
    return [
        line(poly(_coil_pts())),
        line(seg(12, 4, 12, 2.3)),
    ]


@icon("ancestral-tablet", CAT, "Upright rounded-top memorial tablet with an inscribed line on a stepped base",
      tags=["ancestral tablet", "spirit tablet", "memorial", "ancestors", "altar", "shrine", "qingming"])
def _(S):
    return [
        shell("M8.5 9A3.5 3.5 0 0 1 15.5 9V16.5H19V20.5H5V16.5H8.5Z"),
        detail(seg(12, 8, 12, 13.5)),
        line(seg(12, 2.5, 12, 4.5)),
    ]


@icon("prayer-counter-ring", CAT, "Finger ring with a small counter display and a press button on top",
      tags=["prayer counter", "tasbih ring", "digital counter", "smart ring", "dhikr", "tally", "meditation"])
def _(S):
    return [
        shell(rect(7.5, 2.5, 9, 6.5, min(S.R, 2))),
        detail(seg(10, 5.8, 14, 5.8)),
        line(seg(19.5, 5.8, 19.5, 5.8)),
        dot(19.5, 5.8, 1.3),
        line(ring(S, 12, 15.3, 5.5, None, 14)),
    ]


@icon("maamoul", CAT, "Domed round shortbread cookie with two curved ridge lines across it and a dusting of dots",
      tags=["maamoul", "date cookie", "eid", "easter", "shortbread", "middle eastern", "pastry"])
def _(S):
    return [
        shell("M3.5 19C3.5 11 7.5 7.5 12 7.5C16.5 7.5 20.5 11 20.5 19Z"),
        detail("M7.5 15Q12 11.5 16.5 15"),
        dot(5.5, 4.3, 0.9), dot(9.5, 3, 0.9), dot(14.5, 3, 0.9), dot(18.5, 4.3, 0.9),
    ]


@icon("modak", CAT, "Teardrop-shaped dumpling with pleated folds gathered to a pointed top",
      tags=["modak", "ganesh chaturthi", "dumpling", "indian sweet", "steamed", "pleated", "festival"])
def _(S):
    return [
        shell("M12 3C13 6.5 20 9.5 20 15C20 19 16.5 21.5 12 21.5C7.5 21.5 4 19 4 15C4 9.5 11 6.5 12 3Z", stroke_miterlimit="2"),
        detail(seg(12, 9, 12, 18.5)),
        detail(seg(11.4, 9, 8, 17.5)),
        detail(seg(12.6, 9, 16, 17.5)),
    ]


@icon("laddoo", CAT, "Three round sweet balls stacked in a small pyramid on a plate",
      tags=["laddoo", "laddu", "indian sweet", "diwali", "round sweet", "prasad", "festival"])
def _(S):
    return [
        shell(circle(7.3, 15.3, 3.6)),
        shell(circle(16.7, 15.3, 3.6)),
        shell(circle(12, 8.3, 3.6)),
        line(seg(2.5, 20.5, 21.5, 20.5)),
    ]


@icon("kulich", CAT, "Tall cylindrical sweet bread with a domed icing cap dripping down its sides and sprinkles",
      tags=["kulich", "easter bread", "russian", "orthodox", "icing", "paska", "sweet bread"])
def _(S):
    return [
        shell("M6 21.5V9C6 5.5 8.5 3.5 12 3.5C15.5 3.5 18 5.5 18 9V21.5Z"),
        detail("M6 12.5A2 2 0 0 0 10 12.5A2 2 0 0 0 14 12.5A2 2 0 0 0 18 12.5"),
        line(seg(9.2, 8.2, 10.4, 6.8)),
        line(seg(13.4, 8.6, 14.6, 7.2)),
    ]


@icon("colomba-cake", CAT, "Cake shaped like a dove seen from above with its wings spread wide, topped with sugar dots",
      tags=["colomba", "easter cake", "dove", "italian", "pastry", "peace", "almond"])
def _(S):
    return [
        shell(poly([(12, 2.5), (13.8, 4.8), (13.4, 8.3), (21, 7), (20, 12), (13.6, 13.8), (14.6, 20), (12, 18.2), (9.4, 20), (10.4, 13.8), (4, 12), (3, 7), (10.6, 8.3), (10.2, 4.8)],
                   closed=True, r=S.r * 0.7)),
        dot(7.2, 10, 0.9), dot(16.8, 10, 0.9),
    ]


@icon("simnel-cake", CAT, "Round layered cake topped with a ring of small marzipan balls around its edge",
      tags=["simnel cake", "easter cake", "marzipan", "fruit cake", "british", "lent", "eleven balls"])
def _(S):
    balls = []
    for i in range(11):
        a = -90 + i * 360 / 11
        bx, by = 12 + 6.6 * math.cos(math.radians(a)), 10 + 2.0 * math.sin(math.radians(a))
        balls.append(dot(bx, by, 0.95) if S.name != "line" else Part("dot", rect(bx - 0.9, by - 0.9, 1.8, 1.8)))
    return [
        shell("M3.5 10A8.5 3.6 0 0 1 20.5 10V18A8.5 3.6 0 0 1 3.5 18Z"),
        detail("M3.5 10A8.5 3.6 0 0 0 20.5 10"),
    ] + balls
