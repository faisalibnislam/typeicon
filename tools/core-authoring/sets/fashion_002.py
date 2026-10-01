"""TypeIcon Core: fashion (batch fashion_002).

Cultural garments, headwear and footwear. Hats are drawn in side or front silhouette on a 3-21 frame;
dome and curve shapes get an explicit Line versus Rounded difference (sharp base corners versus rounded).
"""
import math

from dsl import D, I, P, Part, ST, U, arc, circle, detail, dot, ellipse, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar  # noqa: F401

CAT = "fashion"


# --------------------------------------------------------------------------- helpers

def _tee(top=3.5, hem=20.5, body=(7, 17)):
    bl, br = body
    return [(8.5, top), (3, top + 3), (4.5, top + 7.5), (bl, top + 6.5), (bl, hem),
            (br, hem), (br, top + 6.5), (19.5, top + 7.5), (21, top + 3), (15.5, top)]


def _ls(cuff=19.0, hem=21.0, neck=(9, 15), top=3.0, shoulder=5.0, body=(7, 17), outer=(3, 21)):
    (nl, nr), (bl, br), (ol, orr) = neck, body, outer
    return [(nl, top), (ol + 1.5, shoulder), (ol, cuff), (bl, cuff), (bl, hem),
            (br, hem), (br, cuff), (orr, cuff), (orr - 1.5, shoulder), (nr, top)]


def _seams(y0=10.0, y1=19.0, body=(7, 17)):
    return [detail(seg(body[0], y0, body[0], y1)), detail(seg(body[1], y0, body[1], y1))]


def _crew(top=3.5, l=8.5, r=15.5, depth=2.5):
    mid = top + depth
    return (f"M{fmt(l)} {fmt(top)}C{fmt(l + 0.7)} {fmt(top + 1.7)} {fmt(l + 1.9)} {fmt(mid)} 12 {fmt(mid)}"
            f"C{fmt(r - 1.9)} {fmt(mid)} {fmt(r - 0.7)} {fmt(top + 1.7)} {fmt(r)} {fmt(top)}")


def _dome(S, x0, x1, base, top, cx=12.0, k=0.56):
    """Dome (half ellipse-ish) with a flat base; Line keeps sharp base corners, Rounded rounds them."""
    hw0, hw1 = cx - x0, x1 - cx
    h = base - top
    if S.name == "rounded":
        return (f"M{fmt(x0 + 1.5)} {fmt(base)}A1.5 1.5 0 0 1 {fmt(x0)} {fmt(base - 1.5)}"
                f"C{fmt(x0)} {fmt(base - h * 1.0)} {fmt(cx - hw0 * k)} {fmt(top)} {fmt(cx)} {fmt(top)}"
                f"C{fmt(cx + hw1 * k)} {fmt(top)} {fmt(x1)} {fmt(base - h * 1.0)} {fmt(x1)} {fmt(base - 1.5)}"
                f"A1.5 1.5 0 0 1 {fmt(x1 - 1.5)} {fmt(base)}Z")
    return (f"M{fmt(x0)} {fmt(base)}C{fmt(x0)} {fmt(base - h * 1.0)} {fmt(cx - hw0 * k)} {fmt(top)} {fmt(cx)} {fmt(top)}"
            f"C{fmt(cx + hw1 * k)} {fmt(top)} {fmt(x1)} {fmt(base - h * 1.0)} {fmt(x1)} {fmt(base)}Z")


def _arc_pts(cx, cy, r, a0, a1, n=8, ry=None):
    ry = r if ry is None else ry
    out = []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        x, _ = polar(0, 0, r, a)
        _, y = polar(0, 0, ry, a)
        out.append((cx + x, cy + y))
    return out


# ============================================================================ garments

@icon("djellaba", CAT, "Long loose robe with wide sleeves and a pointed hood rising behind the neck.",
      tags=["jellabiya", "hooded robe", "north african", "moroccan", "gown", "modest wear"], aliases=["jellaba"])
def _(S):
    pts = [(12, 2.5), (15, 6), (19, 8), (21, 17), (17.5, 18), (16.5, 13), (16.5, 21), (7.5, 21), (7.5, 13), (6.5, 18), (3, 17), (5, 8), (9, 6)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(poly([(9.5, 6.5), (12, 10.5), (14.5, 6.5)], r=S.r)),
        detail(seg(12, 10.5, 12, 18)),
    ]


@icon("kurta", CAT, "Long-sleeved knee-length tunic with a small stand collar and a short button placket.",
      tags=["indian tunic", "long shirt", "south asian", "ethnic wear", "kurti", "menswear"], aliases=["kurti"])
def _(S):
    pts = [(9.5, 3), (4.5, 5), (3, 17), (6.5, 17.5), (7, 12), (6.5, 21), (17.5, 21), (17, 12), (17.5, 17.5), (21, 17), (19.5, 5), (14.5, 3)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(12, 5.5, 12, 11)),
        detail(poly([(9.5, 3), (12, 5.5), (14.5, 3)], r=S.r)),
        dot(12, 14, 1), dot(12, 17.5, 1),
    ]


@icon("sherwani", CAT, "Long buttoned coat with a stand collar and fitted sleeves, worn for weddings and formal events.",
      tags=["wedding coat", "groom", "achkan", "south asian", "formal", "menswear", "ethnic wear"], aliases=["achkan"])
def _(S):
    return [
        shell(poly(_ls(cuff=17.5, hem=21.5, neck=(10, 14), top=2.5, shoulder=4.5, body=(6.5, 17.5), outer=(3, 21)), closed=True, r=S.r)),
        detail(seg(6.5, 9, 6.5, 17.5)), detail(seg(17.5, 9, 17.5, 17.5)),
        detail(poly([(10, 2.5), (12, 5), (14, 2.5)], r=S.r)),
        dot(12, 8, 1), dot(12, 11.5, 1), dot(12, 15, 1), dot(12, 18.5, 1),
    ]


@icon("lehenga", CAT, "Short cropped blouse above a long flared skirt with a decorated hem band.",
      tags=["choli", "indian skirt", "bridal", "south asian", "ethnic wear", "wedding dress", "ghagra"], aliases=["ghagra"])
def _(S):
    return [
        shell(poly([(8.5, 2.5), (15.5, 2.5), (18.5, 5), (16.5, 8), (7.5, 8), (5.5, 5)], closed=True, r=S.r)),
        detail(_crew(top=2.5, l=10, r=14, depth=1.5)),
        shell(poly([(8.5, 12), (15.5, 12), (21, 21), (3, 21)], closed=True, r=S.r)),
        detail(seg(4.8, 17.5, 19.2, 17.5)),
    ]


@icon("salwar-kameez", CAT, "Short-sleeved tunic over loose trousers that gather at the ankles.",
      tags=["shalwar", "punjabi suit", "south asian", "ethnic wear", "trousers", "tunic", "pakistani"], aliases=["shalwar-kameez"])
def _(S):
    return [
        shell(poly([(9,2.5),(15,2.5),(19.5,4.5),(20,8),(17,9),(17,12.5),(7,12.5),(7,9),(4,8),(4.5,4.5)], closed=True, r=S.r)),
        detail(_crew(top=2.5, l=9.5, r=14.5, depth=2)),
        shell(poly([(7.5, 16), (16.5, 16), (15.5, 21.5), (13, 21.5), (12, 18), (11, 21.5), (8.5, 21.5)], closed=True, r=S.r)),
    ]


@icon("dashiki", CAT, "Loose short-sleeved tunic with a wide V-shaped decorated panel around the neck.",
      tags=["west african", "embroidered shirt", "african print", "tunic", "ethnic wear", "kaftan shirt"], aliases=[])
def _(S):
    return [
        shell(poly(_tee(hem=21), closed=True, r=S.r)),
        detail(poly([(8.5, 3.5), (12, 11), (15.5, 3.5)], r=S.r)),
        dot(12, 14.5, 1),
        detail(seg(7, 18, 17, 18)),
    ]


@icon("huipil", CAT, "Boxy square-cut blouse with a round neck and bands of woven zigzag patterns.",
      tags=["mayan blouse", "mexican blouse", "embroidered", "traditional dress", "latin american", "tunic"], aliases=[])
def _(S):
    return [
        shell(poly([(9, 4), (3, 4), (3, 10), (6, 10), (6, 20), (18, 20), (18, 10), (21, 10), (21, 4), (15, 4)], closed=True, r=S.r)),
        detail("M9 4a3 3 0 0 0 6 0"),
        detail(poly([(6, 13.5), (9, 11), (12, 13.5), (15, 11), (18, 13.5)])),
        detail(seg(6, 17, 18, 17)),
    ]


@icon("toga", CAT, "Figure wrapped in a long cloth draped diagonally over one shoulder in folds.",
      tags=["roman", "ancient rome", "drape", "senator", "costume", "greek robe", "classical"], aliases=[])
def _(S):
    return [
        shell(circle(12, 5.5, 2.5)),
        shell(poly([(8, 10.5), (16, 10.5), (19, 21), (5, 21)], closed=True, r=S.r)),
        detail("M8.5 11.5C11 14 14 15.5 17 16"),
        detail(seg(11, 17, 10.5, 21)),
    ]


@icon("kente-cloth", CAT, "Rectangle of woven cloth made of vertical strips with offset bars in each strip.",
      tags=["west african", "ghana", "woven", "textile", "strip weave", "african fabric", "pattern"], aliases=[])
def _(S):
    return [
        shell(rect(3, 5, 18, 14, S.R)),
        detail(seg(9, 5, 9, 19)), detail(seg(15, 5, 15, 19)),
        detail(seg(3, 12, 9, 12)), detail(seg(15, 12, 21, 12)),
        detail(seg(9, 8.5, 15, 8.5)), detail(seg(9, 15.5, 15, 15.5)),
    ]


def _ruff_d(S):
    n, rb, ra = 8, 6.8, 2.85
    pts = [polar(12, 12, rb, -90 + i * 360 / n + 22.5) for i in range(n)]
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(1, n + 1):
        x, y = pts[i % n]
        d += f"A{fmt(ra)} {fmt(ra)} 0 0 1 {fmt(x)} {fmt(y)}"
    return d + "Z"


@icon("ruff-collar", CAT, "Top view of a stiff pleated round collar with a scalloped edge around a neck hole.",
      tags=["elizabethan", "renaissance", "pleated collar", "tudor", "clown collar", "costume", "historical"], aliases=[])
def _(S):
    return [
        shell(_ruff_d(S)),
        detail(circle(12, 12, 3)),
    ]


@icon("beaded-collar", CAT, "Wide flat necklace in a ring with an open neck gap at the top and a row of beads.",
      tags=["broad collar", "bead necklace", "ceremonial", "african jewelry", "maasai", "tribal", "beadwork"], aliases=[])
def _(S):
    a0, a1 = -62, 242
    ox0, oy0 = polar(12, 12.5, 9, a0)
    ox1, oy1 = polar(12, 12.5, 9, a1)
    ix0, iy0 = polar(12, 12.5, 4, a0)
    ix1, iy1 = polar(12, 12.5, 4, a1)
    d = (f"M{fmt(ox0)} {fmt(oy0)}A9 9 0 1 1 {fmt(ox1)} {fmt(oy1)}L{fmt(ix1)} {fmt(iy1)}"
         f"A4 4 0 1 0 {fmt(ix0)} {fmt(iy0)}Z")
    parts = [shell(d)]
    for ang in (-40, 0, 40, 80, 120, 160, 200):
        pass
    for ang in (-30, 10, 50, 90, 130, 170, 210):
        x, y = polar(12, 12.5, 6.5, ang)
        parts.append(dot(x, y, 0.95))
    return parts


@icon("keffiyeh", CAT, "Checked headscarf draped down from the crown, held by a double cord ring on top.",
      tags=["shemagh", "kufiya", "arab scarf", "desert scarf", "checkered", "headdress", "middle east"], aliases=["shemagh", "kufiya"])
def _(S):
    body = "M12 3.5C8 3.5 6.5 6.5 5.5 11L3 20H21L18.5 11C17.5 6.5 16 3.5 12 3.5Z"
    if S.name == "rounded":
        body = "M12 3.5C8 3.5 6.5 6.5 5.5 11L3.3 18.8A1.2 1.2 0 0 0 4.5 20H19.5A1.2 1.2 0 0 0 20.7 18.8L18.5 11C17.5 6.5 16 3.5 12 3.5Z"
    return [
        shell(body),
        detail(ellipse(12, 8, 6, 2)),
        detail(seg(12, 10, 12, 20)),
        detail(seg(4.2, 15, 19.8, 15)),
    ]


@icon("turban", CAT, "Head covering of cloth wound in layered diagonal folds.",
      tags=["sikh", "dastar", "pagri", "head wrap", "headwear", "religious", "cloth hat"], aliases=["dastar"])
def _(S):
    return [
        shell(_dome(S, 4, 20, 18, 4.5)),
        detail("M4.5 14C9 14 14 10.5 17.5 5.8"),
        detail("M7 18C11 16.5 17 13 19.8 9"),
    ]


@icon("fez", CAT, "Short flat-topped brimless cylinder hat that narrows upward, with a tassel hanging from the top.",
      tags=["tarboosh", "turkish hat", "moroccan hat", "tassel", "headwear", "tarbush"], aliases=["tarboosh"])
def _(S):
    return [
        shell(poly([(3, 19), (5.5, 8), (14.5, 8), (17, 19)], closed=True, r=S.r)),
        detail(seg(3.5, 16, 16.5, 16)),
        line("M10 8C15 4.5 19 7 19 12"),
        solid(rect(17.75, 12, 2.5, 5, 1.25 if S.name == "rounded" else 0)),
    ]


@icon("kufi", CAT, "Short rounded brimless cap with a band at the base and small dots of embroidery.",
      tags=["taqiyah", "prayer cap", "skullcap", "muslim cap", "kofia", "embroidered cap", "headwear"], aliases=["taqiyah"])
def _(S):
    return [
        shell(_dome(S, 4, 20, 18, 5.5)),
        detail(seg(4, 15, 20, 15)),
        dot(12, 9.3, 1), dot(8, 12, 1), dot(16, 12, 1),
    ]


@icon("kippah", CAT, "Small round skullcap sitting on the top of a head drawn as an open circle.",
      tags=["yarmulke", "skullcap", "jewish", "judaism", "religious", "head covering", "kipa"], aliases=["yarmulke"])
def _(S):
    return [
        shell(_dome(S, 5.5, 18.5, 10, 4.5)),
        line("M5.07 10A8 8 0 1 0 18.93 10"),
    ]


@icon("hijab", CAT, "Head and shoulders wrapped in a scarf that frames the face and covers the hair and neck.",
      tags=["headscarf", "muslim", "veil", "modest fashion", "head covering", "scarf", "islamic"], aliases=["headscarf"])
def _(S):
    body = "M12 3C7 3 5.5 7 5.5 11C5.5 14 4.5 16.5 3 21H21C19.5 16.5 18.5 14 18.5 11C18.5 7 17 3 12 3Z"
    return [
        shell(body),
        detail(ellipse(12, 10.5, 3.2, 4)),
        detail("M8.5 16C10.5 18 13.5 18 15.5 16"),
    ]


def _scallops(x_from, x_to, y, n):
    """Arcs bulging downward along a horizontal edge travelled right to left (x_from > x_to)."""
    w = (x_from - x_to) / n
    r = w / 2
    out = ""
    for i in range(1, n + 1):
        out += f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x_from - w * i)} {fmt(y)}"
    return out


# ============================================================================ ceremonial and regional headwear

@icon("tallit", CAT, "Prayer shawl rectangle with a stripe near each short end and fringes hanging from the corners.",
      tags=["prayer shawl", "jewish", "judaism", "tzitzit", "fringe", "religious", "synagogue"], aliases=["prayer-shawl"])
def _(S):
    return [
        shell(rect(3, 4, 18, 11, S.R if S.name == "rounded" else 0)),
        detail(seg(8, 4, 8, 15)), detail(seg(16, 4, 16, 15)),
        line(seg(4.5, 15, 4.5, 20.5)), line(seg(7.5, 15, 7.5, 20.5)),
        line(seg(16.5, 15, 16.5, 20.5)), line(seg(19.5, 15, 19.5, 20.5)),
    ]


@icon("head-wrap", CAT, "Cloth wound tightly around the head with the ends folded into a large fan that flares up from the top.",
      tags=["gele", "african headwrap", "headtie", "turban wrap", "scarf", "fabric", "hair wrap"], aliases=["gele", "headtie"])
def _(S):
    return [
        shell(_dome(S, 5.5, 18.5, 20, 11.5)),
        detail("M5.6 16.5C9 15.5 14 13.5 18.4 12.8"),
        shell("M12 11.5C9 9.5 4.5 8 4 4.3C7.5 2.8 11 4.8 12 7.8C13 4.8 16.5 2.8 20 4.3C19.5 8 15 9.5 12 11.5Z"),
    ]


@icon("durag", CAT, "Smooth skull-fitting cloth cap with a seam over the top and two long tails hanging at the back.",
      tags=["du-rag", "doo-rag", "wave cap", "head covering", "hair care", "skull cap", "streetwear"], aliases=["du-rag"])
def _(S):
    return [
        shell(_dome(S, 7, 20, 14.5, 4.5, cx=13.5)),
        detail("M9 8C12 6.6 16 7.3 19 11"),
        line("M8.5 15.5C6.5 17 5 19 4 21.5"),
        line("M10.5 15.5C10 17.5 10 19.5 10.5 21.5"),
    ]


@icon("sombrero", CAT, "Wide-brimmed hat with a tall pointed crown and a scalloped edge along the brim.",
      tags=["mexican hat", "mariachi", "fiesta", "straw hat", "wide brim", "cinco de mayo", "headwear"], aliases=[])
def _(S):
    d = ("M10.5 4.5L13.5 4.5L15 12.5C17.5 12.6 20 13.3 21.5 14.5V17" + _scallops(21.5, 2.5, 17, 6) +
         "V14.5C4 13.3 6.5 12.6 9 12.5Z")
    return [
        shell(d),
        detail(seg(9.6, 10, 14.4, 10)),
    ]


@icon("conical-hat", CAT, "Wide shallow cone of woven straw with a chin strap looping underneath.",
      tags=["asian conical hat", "rice hat", "coolie hat", "non la", "straw hat", "farmer", "paddy hat"], aliases=["rice-hat"])
def _(S):
    return [
        shell(poly([(12, 3.5), (21.5, 15), (2.5, 15)], closed=True, r=S.r)),
        detail("M7.3 12C10.5 13.3 13.5 13.3 16.7 12"),
        line("M6 15.5C6 21.5 18 21.5 18 15.5"),
    ]


@icon("chullo", CAT, "Knitted hat with hanging ear flaps and strings, a patterned band and a pompom on top.",
      tags=["peruvian hat", "andean hat", "ear flap hat", "knit hat", "alpaca", "winter hat", "pompom"], aliases=["ear-flap-hat"])
def _(S):
    body = ("M5 18V11.5C5 8 8 6.5 12 6.5C16 6.5 19 8 19 11.5V18H15.5V14H8.5V18Z")
    return [
        shell(body),
        solid(circle(12, 4.3, 2)),
        detail(seg(5, 11, 19, 11)),
        line(seg(6.75, 18, 6.75, 21.5)), line(seg(17.25, 18, 17.25, 21.5)),
    ]


@icon("tyrolean-hat", CAT, "Alpine felt hat with a pinched crown, a narrow brim and a long feather tucked into the band.",
      tags=["alpine hat", "bavarian hat", "german hat", "oktoberfest", "feather", "felt hat", "headwear"], aliases=["alpine-hat", "bavarian-hat"])
def _(S):
    pts = [(3, 15), (7, 14.5), (8.5, 6.5), (12, 9), (15.5, 6.5), (17, 14.5), (21, 15), (21, 17.5), (3, 17.5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(7.5, 12.3, 16.6, 12.3)),
        line("M16.5 12C19 9 19.6 5.5 18.6 3"),
    ]


@icon("kokoshnik", CAT, "Tall crescent-shaped headdress arching over the head, studded with a row of pearls.",
      tags=["russian headdress", "folk headdress", "crown", "traditional costume", "tiara", "pearls", "slavic"], aliases=[])
def _(S):
    body = "M3.5 19C3.5 11 6.5 6 12 3C17.5 6 20.5 11 20.5 19H16.5C16.5 13.5 15 10.5 12 9.5C9 10.5 7.5 13.5 7.5 19Z"
    parts = [shell(body)]
    for x, y in ((5.5, 16), (6.3, 11.8), (8.9, 8.2), (15.1, 8.2), (17.7, 11.8), (18.5, 16)):
        parts.append(dot(x, y, 0.95))
    return parts


@icon("mitre", CAT, "Tall pointed bishop's hat with a cross on the front and a decorated band at the base.",
      tags=["bishop hat", "miter", "church", "clergy", "catholic", "religious headwear", "pope"], aliases=["miter"])
def _(S):
    return [
        shell("M5 19C5 12 8.5 7 12 3C15.5 7 19 12 19 19Z" if S.name == "line" else
              "M5.5 19C5 12 8.5 7 12 3C15.5 7 19 12 18.5 19Z"),
        detail(seg(12, 8, 12, 14)), detail(seg(9.5, 10.5, 14.5, 10.5)),
        detail("M5.2 17H18.8"),
    ]


@icon("mantilla", CAT, "Lace veil with a scalloped hem, pinned high by a tall comb and draped over the head and shoulders.",
      tags=["spanish veil", "lace veil", "peineta", "comb", "church veil", "bridal", "traditional"], aliases=["peineta"])
def _(S):
    d = ("M8.5 7C8.5 2 15.5 2 15.5 7C16.5 10 18.5 13 20.5 18" + _scallops(20.5, 3.5, 18, 5) +
         "C5.5 13 7.5 10 8.5 7Z")
    return [
        shell(d),
        dot(12, 10.5, 1), dot(9.5, 14.5, 1), dot(14.5, 14.5, 1),
    ]


@icon("geta", CAT, "Japanese wooden sandal on two tall wooden teeth with a thong strap over the top.",
      tags=["japanese sandal", "clog", "wooden sandal", "zori", "kimono", "footwear", "traditional"], aliases=[])
def _(S):
    pts = [(3, 11.5), (21, 11.5), (21, 15), (18, 15), (18, 20.5), (15, 20.5), (15, 15), (9, 15), (9, 20.5), (6, 20.5), (6, 15), (3, 15)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        line("M9 11.5C9 5.5 14 5.5 14 11.5"),
    ]


@icon("curled-toe-slipper", CAT, "Flat embroidered slipper whose pointed toe curls up and back.",
      tags=["aladdin shoe", "khussa", "genie shoe", "arabian slipper", "pointed toe", "footwear", "oriental"], aliases=["khussa"])
def _(S):
    d = "M3 18V12Q3 11 4 11H10C11 13 14 13.5 16 12L20.5 6.5C21.5 11 20.5 16 17 18Z"
    return [
        shell(d),
        dot(7, 15, 1), dot(11, 15.3, 1),
    ]


@icon("furoshiki", CAT, "Square cloth wrapped around a box and tied in a knot with two ears on top.",
      tags=["wrapping cloth", "japanese wrap", "gift wrap", "knot", "bento cloth", "eco wrapping", "fabric"], aliases=[])
def _(S):
    return [
        shell(rect(3.5, 11, 17, 9.5, min(S.R, 2))),
        detail(poly([(3.5, 11), (12, 16), (20.5, 11)])),
        shell("M12 11C9.5 11 6.5 9.5 6 6.5C9.5 5.5 12 7.5 12 11Z"),
        shell("M12 11C14.5 11 17.5 9.5 18 6.5C14.5 5.5 12 7.5 12 11Z"),
    ]


@icon("sporran", CAT, "Leather pouch with a flap and three tassels hanging below, hung from a looped chain.",
      tags=["scottish pouch", "kilt pouch", "highland dress", "scotland", "belt pouch", "purse", "tassels"], aliases=[])
def _(S):
    return [
        line("M7 8.5C7 2.5 17 2.5 17 8.5"),
        shell(poly([(5.5, 8.5), (18.5, 8.5), (19, 16), (5, 16)], closed=True, r=S.r)),
        detail(poly([(5.5, 12), (12, 14.5), (18.5, 12)])),
        line(seg(8, 16, 8, 20)), line(seg(12, 16, 12, 20.5)), line(seg(16, 16, 16, 20)),
    ]


# ============================================================================ everyday hats and caps

@icon("bowler-hat", CAT, "Hard round dome crown with a short curled-up brim and a ribbon band.",
      tags=["derby hat", "coke hat", "billycock", "gentleman", "melon hat", "formal hat", "english"], aliases=["derby-hat"])
def _(S):
    d = ("M7 13.5C7 8 9 4.5 12 4.5C15 4.5 17 8 17 13.5C18.5 13.5 20 13 21.5 14.5V16.5"
         "C18.5 18 14 18 12 18C10 18 5.5 18 2.5 16.5V14.5C4 13 5.5 13.5 7 13.5Z")
    return [
        shell(d),
        detail("M7.3 11.5H16.7"),
    ]


@icon("boater-hat", CAT, "Flat-topped straw hat with straight sides, a striped ribbon band and a stiff flat brim.",
      tags=["straw boater", "skimmer", "summer hat", "gondolier", "barbershop", "panama", "flat brim"], aliases=["skimmer-hat"])
def _(S):
    pts = [(7, 13.5), (7, 6), (17, 6), (17, 13.5), (21.5, 14.5), (21.5, 17.5), (2.5, 17.5), (2.5, 14.5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(7, 11.5, 17, 11.5)),
    ]


@icon("flat-cap", CAT, "Rounded flat cap sloping forward into a short stiff brim, side view.",
      tags=["ivy cap", "newsboy", "driver cap", "gatsby", "golf cap", "scally cap", "irish cap", "headwear"], aliases=["ivy-cap"])
def _(S):
    d = "M3 17C3 10 7 6.5 12 7C16 7.5 19.5 10 21.5 14.5L21.5 17Z" if S.name == "line" else "M3 16C3 10 7 6.5 12 7C16 7.5 19.5 10 21.5 14.5L21.5 16A1 1 0 0 1 20.5 17H4A1 1 0 0 1 3 16Z"
    return [
        shell(d),
        detail("M7 17C8 13 10 11 14 10.5"),
    ]


@icon("newsboy-cap", CAT, "Puffy cap made of eight panels meeting at a button on top, with a short brim.",
      tags=["baker boy", "eight panel", "paperboy", "cabbie cap", "apple cap", "headwear", "vintage"], aliases=["baker-boy-hat"])
def _(S):
    d = "M3 16C2.5 9 7 5.5 12 5.5C17 5.5 21.5 9 21 15L21.5 16.5V17H12H3Z" if S.name == "line" else "M3 16C2.5 9 7 5.5 12 5.5C17 5.5 21.5 9 21 15L21 15.5C21.7 16 21.5 17 20.5 17H4A1 1 0 0 1 3 16Z"
    return [
        shell(d),
        detail("M12 5.5C9.5 8.5 9 12 9.5 17"), detail("M12 5.5C14.5 8.5 15 12 14.5 17"),
        dot(12, 8.3, 1),
    ]


@icon("bucket-hat", CAT, "Soft hat with a rounded crown and a short brim sloping down all the way around.",
      tags=["fisherman hat", "sun hat", "festival hat", "reversible hat", "summer", "safari hat", "brimmed hat"], aliases=["fisherman-hat"])
def _(S):
    return [
        shell("M7.5 13.5C7.5 8 9 6 12 6C15 6 16.5 8 16.5 13.5L21 17.5H3Z" if S.name == "line" else
              "M7.5 13.5C7.5 8 9 6 12 6C15 6 16.5 8 16.5 13.5L20.3 16.8Q21.5 17.5 20 17.5H4Q2.5 17.5 3.7 16.8Z"),
        detail(seg(7.6, 11, 16.4, 11)),
    ]


@icon("sun-hat", CAT, "Floppy hat with a very wide drooping brim, a ribbon band and a bow at the side.",
      tags=["beach hat", "floppy hat", "straw hat", "summer", "wide brim", "garden hat", "derby"], aliases=["floppy-hat"])
def _(S):
    d = "M7.5 12C7.5 7 9.5 5.5 12 5.5C14.5 5.5 16.5 7 16.5 12C19 12.5 21.5 14 21.5 16.5C18.5 15.5 15 15.5 12 15.5C9 15.5 5.5 15.5 2.5 16.5C2.5 14 5 12.5 7.5 12Z"
    return [
        shell(d),
        detail("M7.6 11.2H16.4"),
        solid("M15 11.3L20 8.5V14Z" if S.name == "line" else "M15 11.3L19.6 8.9Q20.3 8.6 20.3 9.4V13.6Q20.3 14.4 19.6 14Z"),
    ]


@icon("beret", CAT, "Soft flat round cap slanted to one side with a small stalk on the top.",
      tags=["french hat", "painter", "artist", "military beret", "wool cap", "parisian", "headwear"], aliases=[])
def _(S):
    d = "M3 15.5C3 9 9 6.5 14 7.5C19 8.5 21.5 11.5 21 15.5C21 17 19 17.5 15 17.5H8C4.5 17.5 3 17 3 15.5Z"
    return [
        shell(d),
        line(seg(14, 7.5, 15.5, 4)),
        detail("M3.6 14.5C8 15.5 15 15.5 20.5 14"),
    ]


@icon("cloche-hat", CAT, "Bell-shaped hat pulled low over the head with a small brim and a flower on the side.",
      tags=["1920s hat", "flapper", "vintage", "gatsby", "womens hat", "retro", "bell hat"], aliases=["flapper-hat"])
def _(S):
    d = "M5 17.5C4 10 7 4.5 12 4.5C17 4.5 20 10 19 15.5C20.5 16.5 21.5 17 21.5 18C18 19.5 6 19.5 2.5 18C2.5 17 3.5 16.5 5 17.5Z"
    if S.name == "line":
        d = "M5 17.5C4 10 7 4.5 12 4.5C17 4.5 20 10 19 15.5L21.5 17.5V18.5C18 19.8 6 19.8 2.5 18.5V17.5Z"
    return [
        shell(d),
        detail("M5.2 15.3C9 16.3 14 16.3 18.8 15"),
        dot(15.5, 10.8, 1.6), 
    ]


@icon("fascinator", CAT, "Small decorative disc with feathers and a short net veil, worn on a headband.",
      tags=["derby headpiece", "wedding guest", "ascot", "hair accessory", "headpiece", "feather", "millinery"], aliases=["headpiece"])
def _(S):
    return [
        line("M3 12C3 8 6 6.5 9 6.5"),
        shell(circle(9, 11, 3.2)),
        line("M11.5 8.5C13 4.5 16.5 3.5 20 3.5"),
        line("M12 10.5C14.5 7.5 18 7 21 8"),
        line("M12 12.5C16 12.5 18.5 14.5 19.5 18"),
    ]


@icon("sun-visor", CAT, "Headband with a wide curved peak that shades the eyes and no crown.",
      tags=["visor cap", "tennis visor", "golf visor", "sports", "eye shade", "headwear", "open top"], aliases=["visor-cap"])
def _(S):
    return [
        shell("M3 13C3 10 4.5 8 7 7.5L17 7.5C19.5 8 21 10 21 13Z" if S.name == "line" else
              "M3.5 12.5C4 10 5 8 7 7.5H17C19 8 20 10 20.5 12.5Z"),
        shell("M3 13H21C22 13 22 16 21 16.5C17 18.5 7 18.5 3 16.5C2 16 2 13 3 13Z"),
    ]


@icon("trapper-hat", CAT, "Fur hat with long ear flaps hanging at each side, a band across the crown and a strap under the chin.",
      tags=["ushanka", "russian hat", "winter hat", "aviator hat", "ear flap hat", "fur hat", "cold weather"], aliases=["ushanka"])
def _(S):
    if S.name == "line":
        body = "M4.5 18V11C4.5 7 8 5 12 5C16 5 19.5 7 19.5 11V18H15.5V14H8.5V18Z"
    else:
        body = "M4.5 16.5V11C4.5 7 8 5 12 5C16 5 19.5 7 19.5 11V16.5A2 2 0 0 1 15.5 16.5V14H8.5V16.5A2 2 0 0 1 4.5 16.5Z"
    return [
        shell(body),
        detail(seg(4.5, 10.5, 19.5, 10.5)),
        line("M6.5 18.5C6.5 22 17.5 22 17.5 18.5" if S.name == "line" else "M6.5 18.5C6.5 22 17.5 22 17.5 18.5"),
    ]


@icon("coonskin-cap", CAT, "Round fur cap with a striped animal tail hanging down from the back.",
      tags=["davy crockett", "frontier", "raccoon tail", "fur cap", "pioneer hat", "trapper", "tail"], aliases=[])
def _(S):
    return [
        shell(_dome(S, 7, 21, 15, 5, cx=14)),
        shell(poly([(2.5, 12), (8, 12), (7, 21.5), (3.8, 21.5)], closed=True, r=S.r)),
        detail(seg(2.5, 15.5, 8, 15.5)), detail(seg(2.5, 18.5, 8, 18.5)),
        dot(14.5, 10.5, 1),
    ]


@icon("balaclava", CAT, "Knitted head covering that hugs the head and neck and leaves only a slot open for the eyes.",
      tags=["ski mask", "face mask", "winter wear", "motorcycle", "cold weather", "head cover", "knit"], aliases=["ski-mask"])
def _(S):
    body = "M12 3C7.5 3 5.5 6.5 5.5 11C5.5 14 4.5 16 3.5 20C6 21 18 21 20.5 20C19.5 16 18.5 14 18.5 11C18.5 6.5 16.5 3 12 3Z"
    if S.name == "line":
        body = "M12 3C7.5 3 5.5 6.5 5.5 11C5.5 14 4.5 16 3 21H21C19.5 16 18.5 14 18.5 11C18.5 6.5 16.5 3 12 3Z"
    return [
        shell(body),
        detail(rect(8, 9, 8, 3.2, 1.6 if S.name == "rounded" else 0.4)),
    ]


@icon("sailor-hat", CAT, "Round white canvas hat with a brim turned up all around, side view.",
      tags=["dixie cup", "navy hat", "gob hat", "seaman", "nautical", "military", "sailor cap"], aliases=["dixie-cup-hat"])
def _(S):
    return [
        shell("M7 6H17L21 17C17 18.5 7 18.5 3 17Z" if S.name == "line" else
              "M8 6H16Q17 6 17.3 7L20.8 16.3Q21.2 17.3 20 17.7C16 19 8 19 4 17.7Q2.8 17.3 3.2 16.3L6.7 7Q7 6 8 6Z"),
        detail("M5 13C9 14.6 15 14.6 19 13"),
    ]


@icon("captain-hat", CAT, "Peaked cap with a wide flat top, a band with a badge and a stiff visor in front.",
      tags=["skipper hat", "yacht captain", "naval officer", "peaked cap", "pilot", "nautical", "uniform"], aliases=["skipper-hat"])
def _(S):
    return [
        shell("M2.5 6.5H21.5L18.5 14C19 18.5 5 18.5 5.5 14Z" if S.name == "line" else
              "M3.5 6.5H20.5Q21.8 6.5 21.4 7.8L18.8 14C19.2 18.8 4.8 18.8 5.2 14L2.6 7.8Q2.2 6.5 3.5 6.5Z"),
        detail("M5.7 12.2H18.3"),
        dot(12, 9.3, 1.1),
    ]


# ============================================================================ historical and costume hats

@icon("deerstalker", CAT, "Cap with a peak at the front and at the back and ear flaps tied up in a bow on top.",
      tags=["sherlock", "detective hat", "hunting cap", "tweed cap", "country hat", "ear flaps", "mystery"], aliases=["detective-hat"])
def _(S):
    body = "M2.5 15.5L7 14C6.5 9 9 6.5 12 6.5C15 6.5 17.5 9 17 14L21.5 15.5L21 17.5C17 16.3 7 16.3 3 17.5Z"
    bow = "M12 6.5C10.5 3 8 3.5 8.5 5.5C9 7 11 6.8 12 6.5C13 6.8 15 7 15.5 5.5C16 3.5 13.5 3 12 6.5Z"
    return [
        shell(body),
        shell(bow),
        detail("M7.3 11.5H16.7"),
    ]


@icon("pith-helmet", CAT, "Tall dome helmet with a brim that slopes down all round and a band at the base of the crown.",
      tags=["safari helmet", "colonial hat", "explorer", "topi", "sun helmet", "jungle hat", "expedition"], aliases=["safari-helmet"])
def _(S):
    return [
        shell("M6.8 13C5.5 7.5 8.5 4 12 4C15.5 4 18.5 7.5 17.2 13L21.5 16.5C18 18.3 6 18.3 2.5 16.5Z"),
        detail("M6.5 11.5C9 12.5 15 12.5 17.5 11.5"),
    ]


@icon("bearskin-hat", CAT, "Very tall rounded fur hat with a band at the base and a strap under the chin.",
      tags=["guard hat", "busby", "ceremonial hat", "royal guard", "soldier", "parade", "fur cap"], aliases=["busby"])
def _(S):
    return [
        shell("M7 18C6.5 14 5.5 8 6.2 5.5C7 3 17 3 17.8 5.5C18.5 8 17.5 14 17 18Z" if S.name == "line" else
              "M7.5 18C6.8 14 5.5 8 6.2 5.5C7 3 17 3 17.8 5.5C18.5 8 17.2 14 16.5 18Q16.4 18.5 16 18.5H8Q7.6 18.5 7.5 18Z"),
        detail("M6.6 14.5H17.4"),
        line("M7.2 18.5C7.2 22 16.8 22 16.8 18.5"),
    ]


@icon("tricorn-hat", CAT, "Hat with the brim folded up on three sides to form a triangle around a low crown.",
      tags=["colonial hat", "pirate hat", "revolutionary", "three cornered hat", "18th century", "costume", "captain"], aliases=["three-cornered-hat"])
def _(S):
    return [
        shell("M2.5 8.5H8C8 3.5 16 3.5 16 8.5H21.5L12 18.5Z" if S.name == "line" else
              "M3.5 8.5H8C8 3.5 16 3.5 16 8.5H20.5Q22 8.5 21 9.5L12.7 18Q12 18.7 11.3 18L3 9.5Q2 8.5 3.5 8.5Z"),
        detail("M8.4 7.4H15.6"),
    ]


@icon("bicorne-hat", CAT, "Wide crescent-shaped hat with a point at each end and a round cockade on the front.",
      tags=["napoleon hat", "admiral", "naval hat", "general", "officer", "military", "cockade"], aliases=["napoleon-hat"])
def _(S):
    return [
        shell("M2.5 13.5C4 7.5 8 5 12 5C16 5 20 7.5 21.5 13.5C18 11.3 15 10.8 12 10.8C9 10.8 6 11.3 2.5 13.5Z"),
        dot(12, 7.9, 1.4),
    ]


@icon("plumed-hat", CAT, "Wide-brimmed hat with a long curling feather sweeping across the top.",
      tags=["cavalier hat", "musketeer", "feather hat", "pirate", "swashbuckler", "ostrich plume", "costume"], aliases=["cavalier-hat"])
def _(S):
    d = ("M8 14.5C8 11.5 9.5 10 12 10C14.5 10 16 11.5 16 14.5C19.5 14.8 21.5 15.6 21.5 16.6"
         "C21.5 18.6 17 19 12 19C7 19 2.5 18.6 2.5 16.6C2.5 15.6 4.5 14.8 8 14.5Z")
    return [
        shell(d),
        shell("M8.3 12C3.5 9.5 6 3.5 12 3.3C17 3.2 20 5.5 20.8 9C17.5 6.8 12.5 6.5 8.3 12Z"),
    ]


@icon("hennin", CAT, "Tall pointed cone hat with a long thin veil streaming from the tip.",
      tags=["princess hat", "medieval", "fairy tale", "cone hat", "veil", "castle", "costume"], aliases=["princess-hat"])
def _(S):
    return [
        shell(poly([(6.5, 19), (11, 4), (15.5, 19)], closed=True, r=S.r)),
        detail(seg(7.3, 15.5, 14.7, 15.5)),
        line("M11 4C17 3.5 21 8 20.5 14"),
        line("M12.3 7C16 7.5 18.3 10.5 18 14.5"),
    ]


@icon("jester-hat", CAT, "Soft cap with three floppy points, each ending in a small bell.",
      tags=["court jester", "fool", "clown", "harlequin", "bells", "medieval", "costume"], aliases=["fool-hat"])
def _(S):
    return [
        line("M8.5 15C7 10 4.5 9 3.5 12.5"),
        line("M12 15C12 11 13.5 8 16.5 7"),
        line("M15.5 15C17 10.5 19.5 9.5 20.5 13"),
        shell(rect(6.5, 14.5, 11, 4.5, min(S.R, 2))),
        dot(3.5, 14.3, 1.6), dot(17.6, 6.9, 1.6), dot(20.5, 15, 1.6),
    ]


@icon("pillbox-hat", CAT, "Small round hat with straight sides and a flat top, no brim.",
      tags=["jackie hat", "retro hat", "1960s", "bellhop", "flat top hat", "round hat", "vintage"], aliases=[])
def _(S):
    return [
        shell(poly([(5.5, 18), (6.5, 7.5), (17.5, 7.5), (18.5, 18)], closed=True, r=S.r)),
        detail("M6.5 7.5C8 10.3 16 10.3 17.5 7.5"),
        detail(seg(6, 14.2, 18, 14.2)),
    ]


@icon("aviator-cap", CAT, "Leather flying helmet with rounded ear flaps and a pair of goggles strapped on the forehead.",
      tags=["pilot hat", "flying helmet", "goggles", "vintage aviation", "biker cap", "leather helmet", "aviator"], aliases=["pilot-cap"])
def _(S):
    if S.name == "line":
        body = "M5 17V10.5C5 6.5 8 4.5 12 4.5C16 4.5 19 6.5 19 10.5V17H15.5V14.5H8.5V17Z"
    else:
        body = "M5 16.5V10.5C5 6.5 8 4.5 12 4.5C16 4.5 19 6.5 19 10.5V16.5A1.8 1.8 0 0 1 15.4 16.5V14.5H8.6V16.5A1.8 1.8 0 0 1 5 16.5Z"
    return [
        shell(body),
        detail(circle(9.3, 9.3, 1.8)), detail(circle(14.7, 9.3, 1.8)),
        detail(seg(5, 9.3, 7.5, 9.3)), detail(seg(16.5, 9.3, 19, 9.3)),
    ]


@icon("rain-hat", CAT, "Waterproof hat with a crown and a brim that slopes far lower at the back than the front.",
      tags=["sou'wester", "fisherman", "rain gear", "yellow hat", "sailor", "storm", "waterproof"], aliases=["southwester"])
def _(S):
    d = ("M21 15.5C19.5 15.5 14 15.5 10.5 15.5L3 21.5C5.5 16 6.5 10 8.5 7C10 5 13 4.5 15.5 5.5C18 6.5 18.5 10 18.5 12.5"
         "C19.5 12.8 20.6 13.6 21 15.5Z")
    return [
        shell(d),
        detail("M8.2 10.5H18.4"),
    ]


@icon("bonnet", CAT, "Soft rounded hat framing the face, with ribbons tied in a bow under the chin.",
      tags=["baby bonnet", "easter bonnet", "victorian", "prairie", "bow", "ribbon hat", "old fashioned"], aliases=[])
def _(S):
    body = "M4 17C3.5 9 7 4.5 12 4.5C17 4.5 20.5 9 20 17H16.5C17 12.5 15.5 9.5 12 9.5C8.5 9.5 7 12.5 7.5 17Z"
    bow = "M12 19.3C10.3 17.3 8 18 8 19.5C8 21 10.3 21 12 19.3C13.7 21 16 21 16 19.5C16 18 13.7 17.3 12 19.3Z"
    return [
        shell(body),
        shell(bow),
    ]


@icon("nightcap", CAT, "Long floppy cone-shaped sleeping cap drooping to one side with a pompom at the tip.",
      tags=["sleep cap", "bedtime", "scrooge", "pajamas", "sleepwear", "bedroom", "santa hat"], aliases=["sleeping-cap"])
def _(S):
    return [
        shell("M4 18C4 9.5 8.5 4.5 14 4.8C17.5 5 19.5 8 19.8 12C17 9.5 14.5 10 13.5 12.5C12.8 14.5 13 16.5 14 18Z"),
        detail("M4.2 15.5H13.6"),
        solid(circle(19.5, 14.6, 2.2)),
    ]


@icon("propeller-beanie", CAT, "Round paneled beanie cap with a small two-bladed propeller spinning on top.",
      tags=["propeller hat", "silly hat", "nerd", "kids", "toy", "cartoon", "novelty hat"], aliases=["propeller-hat"])
def _(S):
    return [
        shell(_dome(S, 4, 20, 19, 9.5)),
        detail("M12 9.5C9.3 12.5 9.2 16 9.5 19"), detail("M12 9.5C14.7 12.5 14.8 16 14.5 19"),
        shell("M12 5.5C10 3.3 6.5 3.5 5 5C6.5 6.6 10 6.8 12 5.5Z"),
        shell("M12 5.5C14 3.3 17.5 3.5 19 5C17.5 6.6 14 6.8 12 5.5Z"),
        line(seg(12, 5.5, 12, 9.5)),
    ]


@icon("swim-cap", CAT, "Smooth rubber cap that fits snugly over the head, with a seam across it, above water waves.",
      tags=["swimming cap", "bathing cap", "pool", "swimmer", "swimwear", "triathlon", "water sport"], aliases=["bathing-cap"])
def _(S):
    return [
        shell(_dome(S, 5, 19, 15.5, 3.5)),
        detail("M5.2 11C9 12 15 12 18.8 11"),
        line("M3 20q2.25-2.2 4.5 0t4.5 0t4.5 0t4.5 0"),
    ]


# ============================================================================ head accessories

@icon("bridal-veil", CAT, "Sheer wedding veil falling from a small comb at the top of the head into a long gentle drape.",
      tags=["wedding veil", "bride", "tulle", "chapel veil", "marriage", "bridal accessory", "headpiece"], aliases=["wedding-veil"])
def _(S):
    d = "M9.5 6C9.5 2.5 14.5 2.5 14.5 6C16 10 19 14 20 20C17.5 21.5 15.5 18.5 12 20C8.5 21.5 6.5 18.5 4 20C5 14 8 10 9.5 6Z"
    return [
        shell(d),
        detail("M11 9.5C10 12.5 9.5 15 9.2 17"),
        detail("M13 9.5C14 12.5 14.5 15 14.8 17"),
    ]


@icon("cat-ear-headband", CAT, "Curved headband with two pointed triangular cat ears on top.",
      tags=["cat ears", "kitty ears", "cosplay", "anime", "party headband", "costume", "hair accessory"], aliases=["cat-ears"])
def _(S):
    return [
        line("M3.5 20C3.5 12 7.5 9.5 12 9.5C16.5 9.5 20.5 12 20.5 20"),
        shell(poly([(5.6, 11.2), (6.4, 3.5), (11.6, 8.6)], closed=True, r=S.r)),
        shell(poly([(18.4, 11.2), (17.6, 3.5), (12.4, 8.6)], closed=True, r=S.r)),
    ]


@icon("bandana", CAT, "Square scarf folded into a triangle with a paisley teardrop and dots printed on it.",
      tags=["kerchief", "neckerchief", "paisley", "head scarf", "cowboy", "biker", "hair tie"], aliases=[])
def _(S):
    return [
        shell(poly([(3, 6.5), (21, 6.5), (12, 20)], closed=True, r=S.r)),
        detail("M12 9.5C9.8 10.8 9.8 13.8 12 15.3C14.2 13.8 14.2 10.8 12 9.5Z"),
        dot(7.6, 8.8, 0.9), dot(16.4, 8.8, 0.9),
    ]


@icon("earmuffs", CAT, "Two soft ear pads joined by a curved headband that arches over the head.",
      tags=["ear warmers", "ear covers", "winter", "cold weather", "hearing protection", "fluffy", "headband"], aliases=["ear-warmers"])
def _(S):
    rr = 3 if S.name == "rounded" else 2
    return [
        line("M5.5 10.5C5.5 2.5 18.5 2.5 18.5 10.5"),
        shell(rect(2.5, 10, 6, 9.5, rr)),
        shell(rect(15.5, 10, 6, 9.5, rr)),
    ]


@icon("hatbox", CAT, "Round storage box with a wide lid, a ribbon band and a cord handle on top.",
      tags=["hat box", "round box", "luggage", "vintage travel", "millinery", "gift box", "storage"], aliases=["hat-box"])
def _(S):
    pts = [(3, 8), (21, 8), (21, 12), (19.5, 12), (19.5, 20), (4.5, 20), (4.5, 12), (3, 12)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(4.5, 16, 19.5, 16)),
        line("M9 8C9 3.5 15 3.5 15 8"),
    ]


# ============================================================================ boots and shoes

@icon("cowboy-boot", CAT, "Tall western boot with a pointed toe, an angled heel and a V of decorative stitching on the shaft.",
      tags=["western boot", "rodeo", "ranch", "texan", "country", "leather boot", "footwear"], aliases=["western-boot"])
def _(S):
    pts = [(6, 3), (13.5, 3), (13.5, 12.5), (18.5, 14), (21.5, 17.5), (21.5, 19), (10.5, 19), (9.8, 21.5), (6, 21.5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(poly([(6, 7.3), (9.75, 11), (13.5, 7.3)])),
    ]


@icon("combat-boot", CAT, "High lace-up boot with a zigzag of laces, a padded collar and a thick lugged sole.",
      tags=["military boot", "army boot", "work boot", "punk", "lace up", "tactical", "footwear"], aliases=["army-boot"])
def _(S):
    pts = [(6, 3), (13.5, 3), (13.5, 11), (18.5, 12.5), (21.5, 14.5), (21.5, 21), (5.5, 21), (5.5, 10)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(5.5, 17, 21.5, 17)),
        detail(poly([(8.5, 6.5), (11.5, 8.5), (8.5, 10.5), (11.5, 12.5)])),
    ]


@icon("rain-boot", CAT, "Tall smooth rubber boot with a band at the top edge and a flat thick sole.",
      tags=["wellington", "gumboot", "wellies", "galoshes", "rubber boot", "puddle", "wet weather"], aliases=["wellington-boot", "wellies"])
def _(S):
    pts = [(6, 3), (13.5, 3), (13.5, 14), (19, 15), (21.5, 17), (21.5, 21), (6, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(6, 6.5, 13.5, 6.5)),
        detail(seg(6, 17.5, 21.5, 17.5)),
    ]


@icon("snow-boot", CAT, "Chunky insulated boot with a furry cuff at the top and a thick treaded sole.",
      tags=["winter boot", "fur boot", "snow", "insulated", "apres ski", "cold weather", "footwear"], aliases=["winter-boot"])
def _(S):
    pts = [(5.5, 4), (14.5, 4), (14.5, 13), (18, 14.5), (21.5, 17.5), (21.5, 21), (5.5, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(poly([(5.5, 8.5), (7, 10), (8.5, 8.5), (10, 10), (11.5, 8.5), (13, 10), (14.5, 8.5)])),
        detail(seg(5.5, 17.5, 21.5, 17.5)),
    ]


@icon("knee-high-boot", CAT, "Slim boot rising to the knee with a medium heel and a zip up the side.",
      tags=["tall boot", "riding boot", "fashion boot", "heeled boot", "zip boot", "womenswear", "footwear"], aliases=["tall-boot"])
def _(S):
    pts = [(8, 2.5), (14, 2.5), (14, 14.5), (18.5, 15.5), (21.5, 18.5), (21.5, 20), (11.5, 20), (11, 21.5), (8, 21.5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(11, 5, 11, 13)),
    ]


@icon("espadrille", CAT, "Canvas slip-on shoe on a thick braided rope sole marked with short rope ticks.",
      tags=["rope sole", "summer shoe", "canvas shoe", "alpargata", "beach shoe", "flat shoe", "footwear"], aliases=["alpargata"])
def _(S):
    pts = [(3.5, 9), (9, 9), (10.5, 11.5), (15, 12.5), (19.5, 14.5), (21.5, 16), (21.5, 20.5), (3.5, 20.5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(3.5, 16.3, 21.5, 16.3)),
        detail(seg(8, 16.3, 8, 20.5)), detail(seg(12.5, 16.3, 12.5, 20.5)), detail(seg(17, 16.3, 17, 20.5)),
    ]


@icon("clog", CAT, "Carved wooden shoe with a rounded bulbous toe and a deep opening for the foot, side view.",
      tags=["wooden shoe", "sabot", "dutch clog", "holland", "garden clog", "netherlands", "footwear"], aliases=["wooden-shoe", "sabot"])
def _(S):
    d = "M3 12.5C3 10.5 5.5 9.5 8 10C9.5 11.8 11.5 12.3 14 12.3C18.5 12.3 21.5 14.3 21.5 17.5C21.5 19 20.5 19.5 19 19.5H4.5C3.6 19.5 3 19 3 18Z"
    return [
        shell(d),
        detail("M8.2 10C8.2 12.3 10.2 13.7 12.7 13.7"),
        detail(seg(3, 16.5, 21.3, 16.5)),
    ]


def _flat_shoe(S, top=12.8, toe=21.5, base=18.5):
    """Low shoe silhouette facing right: heel cup at the left, opening, vamp and rounded toe."""
    if S.name == "line":
        return (f"M3 {base}V11.8C5 12 7 14.3 9.5 14.3C12 14.3 13.5 {top} 16 {top}C19.5 {top} {toe} 15 {toe} {base - 0.5}V{base}Z")
    return (f"M4.5 {base}Q3 {base} 3 {base - 1.5}V11.8C5 12 7 14.3 9.5 14.3C12 14.3 13.5 {top} 16 {top}"
            f"C19.5 {top} {toe} 15 {toe} {base - 1.5}Q{toe} {base} {toe - 1.5} {base}Z")


@icon("ballet-flat", CAT, "Low-cut flat shoe with a rounded toe and a small bow on the front.",
      tags=["flats", "ballerina shoe", "slip on", "womens shoe", "bow shoe", "pump", "footwear"], aliases=["ballerina-flat"])
def _(S):
    return [
        shell(_flat_shoe(S)),
        shell("M16.3 12.3C14.5 9.5 13 10.8 14.5 12.4C15.3 13 16 12.7 16.3 12.3C16.7 12.7 17.3 13 18.1 12.4C19.6 10.8 18 9.5 16.3 12.3Z"),
    ]


@icon("mary-jane-shoe", CAT, "Round-toed flat shoe with a single strap across the instep fastened by a button.",
      tags=["strap shoe", "school shoe", "girls shoe", "buckle strap", "patent leather", "flats", "footwear"], aliases=["mary-jane"])
def _(S):
    return [
        shell(_flat_shoe(S, top=12.3)),
        detail(seg(9.5, 14.3, 9.5, 18.5)),
        dot(9.5, 11.6, 1.1),
    ]


@icon("buckle-shoe", CAT, "Low-heeled shoe with a large square metal buckle on the front of the vamp.",
      tags=["pilgrim shoe", "colonial shoe", "dress shoe", "square buckle", "historical", "formal shoe", "footwear"], aliases=["pilgrim-shoe"])
def _(S):
    pts = [(3, 20.5), (3, 11.5), (9.5, 14), (12, 13.5), (17, 13.3), (21.5, 16), (21.5, 18.3), (8, 18.3), (8, 20.5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(rect(12, 13.9, 4.6, 4.4, 0.4)),
    ]
