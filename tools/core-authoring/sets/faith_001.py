"""TypeIcon Core: faith (batch 001).

Religious objects, places, vestments and scenes, drawn respectfully and in their conventional form.
Same language as sets/culture.py: closed silhouettes are shells, inner lines are details, small solid marks
(panels, gems, candles) are `mark`s that stay solid in Line/Rounded and are knocked out of Filled shells.
Figures follow the stick-figure style of sets/activities_002.py (solid head r 2.25 over 2 px limbs).
Where a part sits behind another, it is cut away around the front part with a gap (`cut`).
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "faith"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def grow(d, g):
    """Region d expanded by g px."""
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def cut(back, front, g=3.5):
    """Back region with the front region (grown by g) removed: leaves a clear gap between their outlines."""
    return minus(back, grow(front, g))


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def rotd(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def flip(d):
    """Mirror a d-string across the vertical centre line."""
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def small_cross(cx, top, bottom, bar_y, half):
    """Two strokes forming a small cross (use as a line part)."""
    return f"M{fmt(cx)} {fmt(top)}V{fmt(bottom)}M{fmt(cx - half)} {fmt(bar_y)}H{fmt(cx + half)}"


def head(x, y):
    return dot(x, y, 2.25)


def limb(S, *pts):
    return line(poly(pts, r=S.r))


def bell(cx, top, w, bottom):
    """Bell outline: domed crown, straight shoulders and a flared lip."""
    k = w * 0.33
    l, r = cx - w / 2, cx + w / 2
    return (f"M{fmt(l)} {fmt(bottom)}C{fmt(l + 0.9)} {fmt(bottom - 0.8)} {fmt(cx - k)} {fmt(bottom - 1.6)} {fmt(cx - k)} {fmt(top + k + 0.8)}"
            f"A{fmt(k)} {fmt(k)} 0 0 1 {fmt(cx + k)} {fmt(top + k + 0.8)}"
            f"C{fmt(cx + k)} {fmt(bottom - 1.6)} {fmt(r - 0.9)} {fmt(bottom - 0.8)} {fmt(r)} {fmt(bottom)}Z")


def flame(cx, top, bottom, w, S):
    """Teardrop flame; pointed tip in Line, softened tip in Rounded."""
    h = bottom - top
    t = L(S, 0.0, 0.6)
    return (f"M{fmt(cx)} {fmt(top + t)}C{fmt(cx + w * 0.2)} {fmt(top + h * 0.3)} {fmt(cx + w / 2)} {fmt(top + h * 0.45)} {fmt(cx + w / 2)} {fmt(top + h * 0.7)}"
            f"A{fmt(w / 2)} {fmt(h * 0.3)} 0 0 1 {fmt(cx - w / 2)} {fmt(top + h * 0.7)}"
            f"C{fmt(cx - w / 2)} {fmt(top + h * 0.45)} {fmt(cx - w * 0.2)} {fmt(top + h * 0.3)} {fmt(cx)} {fmt(top + t)}Z")


# ============================================================================ church objects

@icon("ciborium", CAT, "Lidded cup on a tall stem and flared foot with a small cross on its domed lid",
      tags=["pyx", "eucharist", "communion", "host", "church", "mass"])
def _(S):
    body = union("M6 10.5A6 4 0 0 1 18 10.5Z", "M6 10.5H18C18 13.6 15.4 15.5 12 15.5C8.6 15.5 6 13.6 6 10.5Z")
    return [
        line(small_cross(12, 2, 6.8, 3.75, 1.75)),
        shell(body),
        detail(seg(6, 10.5, 18, 10.5)),
        line(seg(12, 15.5, 12, 18.5)),
        shell(poly([(8.5, 21), (15.5, 21), (13.5, 18.5), (10.5, 18.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("prayer-kneeler", CAT, "Side view of a prie-dieu: a padded kneeling step and an upright with a slanted armrest",
      tags=["prie-dieu", "kneeler", "prayer desk", "prayer bench", "church", "kneel"], aliases=["prie-dieu"])
def _(S):
    return [
        shell(poly([(7, 9.5), (19.5, 5), (20.5, 7.5), (8, 12)], closed=True, r=S.r * 0.5)),
        line(seg(17, 8.8, 17, 15.5)),
        shell(rect(3, 15.5, 16.5, 5.5, min(S.R, 2.5))),
    ]


@icon("confessional-booth", CAT, "Wooden confessional with a curtained middle bay between two doors and a cross on its peak",
      tags=["confessional", "confession", "penance", "reconciliation", "church", "priest"], aliases=["confessional"])
def _(S):
    return [
        line(small_cross(12, 2, 6.8, 4, 2)),
        shell(poly([(3, 21), (3, 11), (12, 6.5), (21, 11), (21, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(8.5, 8.4, 8.5, 21)), detail(seg(15.5, 8.4, 15.5, 21)),
        detail("M9.5 12.5Q10.75 14.5 12 12.5Q13.25 14.5 14.5 12.5"),
        detail(seg(12, 15, 12, 21)),
        dot(6.25, 15.5, 1), dot(17.75, 15.5, 1),
    ]


@icon("scapular", CAT, "Two small cloth panels joined by two cord loops, one panel marked with a cross",
      tags=["brown scapular", "devotional", "sacramental", "catholic", "carmelite", "medal"])
def _(S):
    rr = min(S.R, 2)
    return [
        line("M4.5 13C4.5 1 19.5 1 19.5 13"),
        line("M8 13C8 6.5 16 6.5 16 13"),
        shell(rect(2.5, 13, 7.5, 8, rr)),
        shell(rect(14, 13, 7.5, 8, rr)),
        detail(small_cross(6.25, 15, 19, 16.5, 1.5)),
    ]


@icon("saint-medal", CAT, "Oval medal with a haloed robed figure, hanging from a small ring",
      tags=["religious medal", "patron saint", "miraculous medal", "pendant", "catholic", "devotional"],
      aliases=["religious-medal"])
def _(S):
    return [
        shell(circle(12, 4.5, 1.75)),
        shell(ellipse(12, 14.25, 6.5, 7.25)),
        detail(circle(12, 11.75, 2.25)),
        mark(poly([(12, 16), (14.5, 19.5), (9.5, 19.5)], closed=True, r=L(S, 0, 0.8))),
    ]


@icon("orthodox-icon", CAT, "Framed panel painting of a haloed figure, head and shoulders",
      tags=["icon painting", "orthodox", "byzantine", "saint", "holy image", "church"], aliases=["religious-icon"])
def _(S):
    return [
        shell(rect(4, 2, 16, 20, S.R)),
        detail(rect(7, 5, 10, 14, min(S.R, 1.5))),
        detail(circle(12, 9.75, 2.25)),
        mark("M8.6 18.2C8.6 15.9 10 14.6 12 14.6C14 14.6 15.4 15.9 15.4 18.2Z"),
    ]


@icon("iconostasis", CAT, "Church screen wall with a row of icon panels over two side doors and an arched central door",
      tags=["icon screen", "templon", "orthodox church", "royal doors", "sanctuary", "altar screen"])
def _(S):
    parts = [
        line(small_cross(12, 2, 6, 3.5, 1.5)),
        shell(rect(2, 6, 20, 15, min(S.R, 2))),
        detail("M9 21V16A3 3 0 0 1 15 16V21"),
        mark(rect(4.5, 15.5, 2, 5.5)), mark(rect(17.5, 15.5, 2, 5.5)),
    ]
    for cx in (5.5, 8.75, 12, 15.25, 18.5):
        parts.append(mark(rect(cx - 1.1, 8.25, 2.2, 2.75, L(S, 0, 0.5))))
    return parts


@icon("forehead-ashes", CAT, "Head in profile with a small ash cross on the forehead",
      tags=["ash wednesday", "ashes", "lent", "cross", "forehead", "christian"], aliases=["ash-wednesday"])
def _(S):
    r = L(S, 0, 1)
    d = ("M7.5 21V17.5C4.8 16 3.5 13 3.5 10.5C3.5 5.8 7.3 2.5 12 2.5C16.4 2.5 19.2 5.6 19.2 9.5"
         + poly([(19.2, 9.5), (20.6, 13), (19.2, 13.6), (19.2, 16)], r=r)[len("M19.2 9.5"):]
         + "C19.2 17 18.4 17.6 17.2 17.6H15.5V21Z")
    return [shell(d), detail(small_cross(14.75, 4.75, 9.75, 6.75, 2))]


@icon("hymnal", CAT, "Closed hymn book with a music note on the cover and a ribbon bookmark",
      tags=["hymn book", "songbook", "church music", "worship", "choir", "psalter"], aliases=["hymn-book"])
def _(S):
    book = union(rect(5, 2, 14, 17, min(S.R, 2.5)),
                 poly([(14.5, 17), (17.5, 17), (17.5, 22), (16, 20.6), (14.5, 22)], closed=True))
    return [
        shell(book, stroke_miterlimit="2"),
        detail(seg(8.5, 2, 8.5, 19)),
        dot(12.6, 14, 1.6),
        detail(seg(14.1, 14, 14.1, 7)),
        detail("M14.1 7C15.6 7.4 16.5 8.4 16.5 10"),
    ]


# ============================================================================ crosses

@icon("coptic-cross", CAT, "Equal-armed cross with flared arms ending in three rounded points around a central ring",
      tags=["coptic", "egyptian christian", "orthodox", "cross", "christian", "church"])
def _(S):
    rb = 7 / 6
    arm = (f"M10.6 12L8.5 4.4A{fmt(rb)} {fmt(rb)} 0 0 1 {fmt(8.5 + 2 * rb)} 4.4A{fmt(rb)} {fmt(rb)} 0 0 1 {fmt(8.5 + 4 * rb)} 4.4"
           f"A{fmt(rb)} {fmt(rb)} 0 0 1 15.5 4.4L13.4 12Z")
    body = union(*[rotd(arm, a) for a in (0, 90, 180, 270)], circle(12, 12, 3.6))
    return [shell(body, stroke_miterlimit="2"), detail(circle(12, 12, 1.4)) if S.name == "line" else dot(12, 12, 1.5)]


def _(S):
    rb = 7 / 6
    arm = (f"M10.5 6.8L8.5 3.8A{fmt(rb)} {fmt(rb)} 0 0 1 {fmt(8.5 + 2 * rb)} 3.8A{fmt(rb)} {fmt(rb)} 0 0 1 {fmt(8.5 + 4 * rb)} 3.8"
           f"A{fmt(rb)} {fmt(rb)} 0 0 1 15.5 3.8L13.5 6.8" + ("Z" if S.name == "line" else "Q12 6.3 10.5 6.8Z"))
    parts = [shell(circle(12, 12, 2.6))]
    for a in (0, 90, 180, 270):
        parts.append(shell(rotd(arm, a), stroke_miterlimit="2"))
    return parts


@icon("tau-cross", CAT, "T-shaped tau cross with a flat top bar flaring at its ends",
      tags=["tau", "franciscan", "saint anthony", "cross", "christian", "t cross"], aliases=["st-anthonys-cross"])
def _(S):
    pts = [(3, 3), (21, 3), (20, 8), (14, 7), (14, 21), (10, 21), (10, 7), (4, 8)]
    return [shell(poly(pts, closed=True, r=S.r * 0.5))]


@icon("patriarchal-cross", CAT, "Upright cross with two crossbars, the upper one shorter",
      tags=["double cross", "archiepiscopal cross", "cross of lorraine", "orthodox", "cross", "christian"],
      aliases=["double-cross"])
def _(S):
    pts = [(10, 2), (14, 2), (14, 4), (17, 4), (17, 7.5), (14, 7.5), (14, 11), (20, 11), (20, 15), (14, 15),
           (14, 22), (10, 22), (10, 15), (4, 15), (4, 11), (10, 11), (10, 7.5), (7, 7.5), (7, 4), (10, 4)]
    return [shell(poly(pts, closed=True, r=S.r * 0.4))]


@icon("khachkar", CAT, "Round-topped stone slab carved with a budding cross above a small rosette",
      tags=["cross stone", "armenian", "carved stone", "memorial", "cross", "christian"], aliases=["cross-stone"])
def _(S):
    r = S.r * 0.5
    return [
        shell("M5 21.5V8A7 6 0 0 1 19 8V21.5Z" if S.name == "line" else
              "M5 19.5V8A7 6 0 0 1 19 8V19.5A2 2 0 0 1 17 21.5H7A2 2 0 0 1 5 19.5Z"),
        detail(seg(12, 6, 12, 12)), detail(seg(9, 8.75, 15, 8.75)),
        detail(poly([(10.6, 4.6), (12, 6), (13.4, 4.6)], r=r)),
        detail(poly([(10.6, 13.4), (12, 12), (13.4, 13.4)], r=r)),
        detail(poly([(7.6, 7.35), (9, 8.75), (7.6, 10.15)], r=r)),
        detail(poly([(16.4, 7.35), (15, 8.75), (16.4, 10.15)], r=r)),
        detail(circle(12, 17.5, 1.5)),
    ]


@icon("reliquary", CAT, "House-shaped casket with a peaked roof topped by a cross, standing on short feet",
      tags=["relic", "shrine", "casket", "saint", "church treasure", "chasse"])
def _(S):
    body = union(poly([(3, 11), (12, 6.3), (21, 11)], closed=True), rect(4.5, 11, 15, 7))
    return [
        line(small_cross(12, 2, 6.5, 3.5, 1.5)),
        shell(body),
        detail(seg(4.5, 11, 19.5, 11)),
        detail("M10.5 18V15A1.5 1.5 0 0 1 13.5 15V18"),
        line(seg(6.5, 18, 6.5, 21)), line(seg(17.5, 18, 17.5, 21)),
    ]


@icon("sanctus-bells", CAT, "Cluster of small bells hanging from a crossbar on a short handle",
      tags=["altar bells", "mass bells", "sacring bell", "consecration", "church", "bell"], aliases=["altar-bells"])
def _(S):
    return [
        line(seg(12, 2, 12, 12)),
        line(seg(3.5, 7.5, 20.5, 7.5)),
        line(seg(5.5, 7.5, 5.5, 10)), line(seg(18.5, 7.5, 18.5, 10)),
        shell(bell(5.5, 10, 4.5, 15.5)), shell(bell(18.5, 10, 4.5, 15.5)), shell(bell(12, 12, 4.5, 18.5)),
        dot(5.5, 17.4, 1), dot(18.5, 17.4, 1), dot(12, 20.4, 1),
    ]


@icon("cross-necklace", CAT, "Chain necklace hanging in a V with a small cross pendant",
      tags=["crucifix necklace", "cross pendant", "jewelry", "jewellery", "christian", "chain"])
def _(S):
    cross = poly([(11, 14.5), (13, 14.5), (13, 16.25), (15, 16.25), (15, 18.25), (13, 18.25), (13, 21.5), (11, 21.5),
                  (11, 18.25), (9, 18.25), (9, 16.25), (11, 16.25)], closed=True, r=L(S, 0, 0.5))
    return [
        line("M4 2.5C4.5 8.5 8 12.5 12 13.5C16 12.5 19.5 8.5 20 2.5"),
        solid(cross),
    ]


@icon("calvary-crosses", CAT, "Three crosses on a rounded hill, the middle one taller",
      tags=["calvary", "golgotha", "crucifixion", "good friday", "easter", "three crosses"], aliases=["golgotha"])
def _(S):
    return [
        line(small_cross(12, 3, 15.2, 7, 3.5)),
        line(small_cross(5.5, 9, 17.4, 11.5, 2.5)),
        line(small_cross(18.5, 9, 17.4, 11.5, 2.5)),
        shell("M2 21C4.5 16.5 8 15.2 12 15.2C16 15.2 19.5 16.5 22 21Z"),
    ]


# ============================================================================ angels

_CH_WING = ("M9 14C6.5 12.2 4 12 1.8 12.6C1.9 14.2 2.7 15.2 3.8 15.6C3.7 16.9 4.6 17.8 5.8 17.9"
            "C6.1 19 7.1 19.7 8.3 19.5C8.7 20 9.3 20.1 9.8 19.9Z")


@icon("cherub", CAT, "Round child's face with curly hair and small wings behind the head",
      tags=["cherubim", "putto", "angel", "baby angel", "heaven", "wings"], aliases=["putto"])
def _(S):
    hd = union(circle(12, 12, 5), circle(9.4, 7.9, 1.7), circle(12, 7, 1.8), circle(14.6, 7.9, 1.7))
    body = union(hd, _CH_WING, flip(_CH_WING))
    return [
        shell(body),
        detail(arc(12, 12, 5, 105, 160)), detail(arc(12, 12, 5, 20, 75)),
        dot(10.1, 12, 0.9), dot(13.9, 12, 0.9),
        detail(arc(12, 13.4, 1.6, 35, 145)),
    ]


_AW = ("M10.5 10C8.6 7.1 5.6 5.2 2 5C2 7.5 2.6 9.3 3.6 10.4C3.2 11.8 3.8 13 5.2 13.4C5.2 14.8 6.2 15.8 7.6 15.8"
       "C8.3 16.8 9.5 17 10.5 16.5Z")


@icon("angel-wings", CAT, "Pair of feathered wings spread wide with a halo floating between them",
      tags=["angel", "wings", "halo", "heaven", "memorial", "guardian angel"])
def _(S):
    return [
        line(ellipse(12, 4.25, 3.5, 1.6)),
        shell(_AW), shell(flip(_AW)),
        detail("M9.3 12.2C7.6 10.4 5.8 9.2 4 8.6"), detail(flip("M9.3 12.2C7.6 10.4 5.8 9.2 4 8.6")),
    ]


# ============================================================================ worship objects

def _(S):
    parts = [
        dot(12, 3.5, 1.6), line(seg(12, 5, 12, 10)),
        shell(rect(6, 10, 12, 2.5, L(S, 0.3, 1.25))),
        shell(rect(2.5, 17, 19, 3, L(S, 0.3, 1.5))),
        line(seg(12, 12.5, 12, 17)),
    ]
    for x in (7.5, 10, 14, 16.5):
        parts.append(mark(rect(x - 0.9, 7, 1.8, 2.2, L(S, 0, 0.5))))
    for x in (4, 6.5, 9, 15, 17.5, 20):
        parts.append(mark(rect(x - 0.9, 14, 1.8, 2.2, L(S, 0, 0.5))))
    return parts


def _cruet(cx, side, S):
    body = (f"M{fmt(cx - 1.25)} 8.5H{fmt(cx + 1.25)}V10.5C{fmt(cx + 1.25)} 11.8 {fmt(cx + 2.75)} 12 {fmt(cx + 2.75)} 14.5"
            f"V16.5Q{fmt(cx + 2.75)} 18.25 {fmt(cx + 1.25)} 18.25H{fmt(cx - 1.25)}Q{fmt(cx - 2.75)} 18.25 {fmt(cx - 2.75)} 16.5"
            f"V14.5C{fmt(cx - 2.75)} 12 {fmt(cx - 1.25)} 11.8 {fmt(cx - 1.25)} 10.5Z")
    s = side
    handle = (f"M{fmt(cx + s * 1.25)} 10C{fmt(cx + s * 4.8)} 9.8 {fmt(cx + s * 5.2)} 13.2 {fmt(cx + s * 2.9)} 15")
    return [shell(body), line(handle), dot(cx, 6.3, 1.4)]


@icon("altar-cruets", CAT, "Two small jugs with stoppers and handles standing on a tray",
      tags=["cruets", "wine and water", "mass", "altar", "church", "jugs"], aliases=["cruets"])
def _(S):
    return [*_cruet(7.25, -1, S), *_cruet(16.75, 1, S), line(seg(3, 21, 21, 21))]


@icon("prosphora", CAT, "Round loaf seen from above, stamped with a square seal divided by a cross",
      tags=["communion bread", "holy bread", "orthodox", "eucharist", "seal", "bread"], aliases=["communion-bread"])
def _(S):
    k = L(S, 0.5, 1.5)
    return [
        shell(circle(12, 12, 9)),
        detail(circle(12, 12, 6.5)),
        detail(rect(8.6, 8.6, 6.8, 6.8, k)),
        detail(small_cross(12, 8.6, 15.4, 12, 3.4)),
    ]


@icon("semantron", CAT, "Long wooden plank held at its waist, struck by a small mallet",
      tags=["simandron", "talanton", "wooden gong", "monastery", "call to prayer", "orthodox"], aliases=["simandron"])
def _(S):
    plank = [(2, 13), (9.5, 13), (10.5, 14), (13.5, 14), (14.5, 13), (22, 13), (22, 18), (14.5, 18), (13.5, 17),
             (10.5, 17), (9.5, 18), (2, 18)]
    head = rpts([(14.5, 8), (19.5, 8), (19.5, 11), (14.5, 11)], -30, 17, 9.5)
    return [
        shell(poly(plank, closed=True, r=S.r * 0.4)),
        shell(poly(head, closed=True, r=S.r * 0.5)),
        line(seg(18.3, 8.1, 21.5, 2.5)),
        line(seg(4, 10.5, 3, 8)), line(seg(7.5, 10.5, 7.5, 7.5)), line(seg(11, 10.5, 12, 8)),
    ]


@icon("ihs-christogram", CAT, "The letters IHS under a small cross inside a ring of short rays",
      tags=["christogram", "holy name", "jesuit", "monogram", "jesus", "christian"], aliases=["ihs"])
def _(S):
    s_d = ("M19 10C18.6 9.3 17.9 9 17.2 9C16.2 9 15.5 9.7 15.5 10.5C15.5 12.4 19.1 11.8 19.1 13.9"
           "C19.1 14.9 18.3 15.6 17.3 15.6C16.5 15.6 15.8 15.3 15.3 14.6")
    parts = [
        line(seg(5.5, 9, 5.5, 15.6)),
        line(seg(8.5, 9, 8.5, 15.6)), line(seg(12.5, 9, 12.5, 15.6)), line(seg(8.5, 12.3, 12.5, 12.3)),
        line(s_d),
        line(small_cross(10.5, 3, 7.5, 4.75, 1.75)),
    ]
    for k in range(12):
        a = -90 + 30 * k
        if k in (0, 11, 1):
            continue
        parts.append(line(seg(*polar(12, 12.25, 8.75, a), *polar(12, 12.25, 10.75, a))))
    return parts


@icon("anchor-cross", CAT, "Mariner's cross: a cross whose foot ends in the curved flukes of an anchor",
      tags=["mariner's cross", "anchor", "hope", "christian", "early christian", "cross"], aliases=["mariners-cross"])
def _(S):
    cross = [(10.25, 2), (13.75, 2), (13.75, 6), (18.5, 6), (18.5, 9.5), (13.75, 9.5), (13.75, 20.2), (10.25, 20.2),
             (10.25, 9.5), (5.5, 9.5), (5.5, 6), (10.25, 6)]
    return [
        shell(poly(cross, closed=True, r=S.r * 0.4)),
        line("M4.5 14.5C5 18.5 7.8 21 10.25 21M13.75 21C16.2 21 19 18.5 19.5 14.5"),
        line(poly([(2.5, 16.5), (4.5, 14), (6.5, 16.5)], r=S.r * 0.5)),
        line(poly([(17.5, 16.5), (19.5, 14), (21.5, 16.5)], r=S.r * 0.5)),
    ]


_TRUMPET = "M-0.9 0C-0.9 -3 -1.6 -5 -3.6 -7.2L-1.8 -6.7L0 -8.2L1.8 -6.7L3.6 -7.2C1.6 -5 0.9 -3 0.9 0Z"


def _place(d, deg, x, y):
    a = math.radians(deg)
    return path_to_d(transform_path(P(d), (math.cos(a), math.sin(a), -math.sin(a), math.cos(a), x, y)))


@icon("easter-lily", CAT, "Two trumpet-shaped lily flowers on one stem with long narrow leaves",
      tags=["lily", "easter", "resurrection", "flower", "spring", "church"])
def _(S):
    leaf = "M12 20.5C9.2 20 6.8 18.2 4.8 15.2C8 16 10.5 17.4 12 19"
    return [
        shell(_place(_TRUMPET, -40, 10.3, 13), stroke_miterlimit="2"),
        shell(_place(_TRUMPET, 40, 13.7, 13), stroke_miterlimit="2"),
        line(poly([(12, 21.5), (12, 15.2), (10.3, 13)], r=S.r)),
        line(poly([(12, 15.2), (13.7, 13)], r=S.r)),
        shell(leaf + "Z"), shell(flip(leaf + "Z")),
    ]


@icon("sanctuary-lamp", CAT, "Hanging oil lamp: a flame in a cup held by a metal holder on chains",
      tags=["sanctuary light", "altar lamp", "tabernacle lamp", "eternal flame", "church", "oil lamp"],
      aliases=["sanctuary-light"])
def _(S):
    return [
        dot(12, 2.4, 1.3),
        line(seg(12, 2.4, 5, 12)), line(seg(12, 2.4, 19, 12)),
        shell(flame(12, 5, 10, 3.4, S)),
        shell("M4.5 12H19.5C19.5 16 16.3 18.5 12 18.5C7.7 18.5 4.5 16 4.5 12Z"),
        detail(seg(5.5, 14.5, 18.5, 14.5)),
        line(seg(12, 18.5, 12, 21.5)),
    ]


# ============================================================================ vestments and regalia

@icon("galero-hat", CAT, "Wide flat-brimmed hat with cords ending in rows of tassels on both sides",
      tags=["galero", "cardinal's hat", "ecclesiastical heraldry", "cardinal", "bishop", "hat"], aliases=["galero"])
def _(S):
    parts = [
        shell(union(rect(2.5, 6.25, 19, 2.75, L(S, 0.3, 1.375)), "M7.5 7C7.5 2.8 16.5 2.8 16.5 7Z")),
        line("M9.5 9C7.2 10 6 11.5 6 13.3"), line("M14.5 9C16.8 10 18 11.5 18 13.3"),
    ]
    for cx, sgn in ((6, 1), (18, -1)):
        for x, y in ((0, 14.6), (-1.75, 17.6), (1.75, 17.6), (-3.5, 20.6), (0, 20.6), (3.5, 20.6)):
            parts.append(dot(cx + sgn * x, y, 1.2))
    return parts


@icon("biretta", CAT, "Square clerical cap with curved fins on top and a pompom in the centre",
      tags=["clerical cap", "priest hat", "catholic", "clergy", "cleric", "hat"])
def _(S):
    return [
        line("M5.5 11C5.5 8 6.6 7 8.8 7"), line("M18.5 11C18.5 8 17.4 7 15.2 7"),
        line(seg(12, 7.5, 12, 11)),
        dot(12, 6, 1.9),
        shell(rect(5, 11, 14, 9, min(S.R, 2.5))),
        detail(seg(5, 13.5, 19, 13.5)),
    ]


def _(S):
    hat = rect(4.5, 3.5, 10, 11, min(S.R, 1.5))
    veil = "M12 3.5H16C17.5 9 19.5 15 21 21.5H15.5C15.5 18.5 15.2 16.5 14.5 14.5Z"
    return [
        shell(union(hat, veil), stroke_miterlimit="2"),
        detail(seg(14.5, 3.5, 14.5, 14.5)),
        detail(seg(4.5, 12, 14.5, 12)),
    ]


@icon("papal-tiara", CAT, "Beehive-shaped triple crown with a small cross on top and two hanging ribbons",
      tags=["triregnum", "triple crown", "pope", "papacy", "vatican", "crown"], aliases=["triregnum"])
def _(S):
    body = union("M6 19.5C6 11 8 5.5 12 5.5C16 5.5 18 11 18 19.5Z",
                 poly([(8, 19), (10, 19), (10, 22), (9, 21.1), (8, 22)], closed=True),
                 poly([(14, 19), (16, 19), (16, 22), (15, 21.1), (14, 22)], closed=True))
    return [
        line(small_cross(12, 1.8, 5.8, 3.4, 1.5)),
        shell(body, stroke_miterlimit="2"),
        detail("M8.1 10.2Q12 11.6 15.9 10.2"),
        detail("M6.9 14.3Q12 15.8 17.1 14.3"),
    ]


def _key(S):
    """One key, upright (bow at the bottom, bit at the top right), turned 45 degrees clockwise."""
    bow = rotd(circle(12, 20, 2.5), 45)
    shaft = rotd(seg(12, 17.5, 12, 2.5), 45)
    bit = rotd(poly([(12, 3), (15.5, 3), (15.5, 4.6), (14.2, 4.6), (14.2, 6), (12, 6)], closed=True, r=L(S, 0, 0.4)), 45)
    return bow, shaft, bit


@icon("crossed-keys", CAT, "Two keys crossed in an X with their bits at the top",
      tags=["keys of heaven", "saint peter", "papal keys", "holy see", "vatican", "keys"], aliases=["keys-of-heaven"])
def _(S):
    parts = []
    for deg, m in ((45, False), (-45, True)):
        def pts(ps):
            q = rpts([(24 - x, y) if m else (x, y) for x, y in ps], deg)
            return q
        (bx, by), = pts([(12, 19.6)])
        a, b = pts([(12, 17.1), (12, 2.4)])
        bit = poly(pts([(12, 2.6), (16.2, 2.6), (16.2, 4.6), (14.6, 4.6), (14.6, 6.8), (12, 6.8)]), closed=True, r=L(S, 0, 0.5))
        parts += [shell(circle(bx, by, 2.5)), line(seg(*a, *b)), mark(bit)]
    return parts


def _(S):
    (bx, by), = rpts([(12, 19.6)], 45)
    a, b = rpts([(12, 17.1), (12, 2.4)], 45)
    bit = poly(rpts([(12, 2.6), (16.2, 2.6), (16.2, 4.6), (14.6, 4.6), (14.6, 6.8), (12, 6.8)], 45), closed=True, r=L(S, 0, 0.5))
    key = [shell(circle(bx, by, 2.5)), line(seg(*a, *b)), mark(bit)]
    return key + [Part(p.kind, flip(p.d), p.attrs) for p in key]


def _(S):
    bow, shaft, bit = _key(S)
    return [
        line(bow), line(shaft), mark(bit),
        line(flip(bow)), line(flip(shaft)), mark(flip(bit)),
    ]


@icon("rose-cross", CAT, "Latin cross with a five-petal rose blooming where the bars meet",
      tags=["rosy cross", "rosicrucian", "rose", "cross", "mysticism", "esoteric"], aliases=["rosy-cross"])
def _(S):
    cx, cy = 12, 9.5
    cross = poly([(10, 2), (14, 2), (14, 7.5), (21, 7.5), (21, 11.5), (14, 11.5), (14, 22), (10, 22), (10, 11.5), (3, 11.5),
                  (3, 7.5), (10, 7.5)], closed=True, r=S.r * 0.4)
    body = union(cross, circle(cx, cy, 5.1))
    petals = union(*[circle(*polar(cx, cy, 1.55, -90 + 72 * k), 1.5) for k in range(5)])
    return [shell(body), detail(petals)]


def _(S):
    cx, cy = 12, 9.5
    petals = [circle(*polar(cx, cy, 1.5, -90 + 72 * k), 1.45) for k in range(5)]
    rose = union(*petals, circle(cx, cy, 1.5))
    g = 5.2
    return [
        shell(rose),
        dot(cx, cy, 0.8),
        line(seg(cx, 2, cx, cy - g)), line(seg(cx, cy + g, cx, 22)),
        line(seg(3, cy, cx - g, cy)), line(seg(cx + g, cy, 21, cy)),
    ]


@icon("grotto-shrine", CAT, "Rocky cave arch sheltering a small haloed statue with candles at its base",
      tags=["grotto", "lourdes", "marian shrine", "cave shrine", "pilgrimage", "statue"], aliases=["marian-grotto"])
def _(S):
    outer = poly([(2, 21.5), (2.2, 14.5), (3.4, 9.5), (5.5, 6), (8.5, 3.5), (12, 2.6), (15.5, 3.5), (18.5, 6),
                  (20.6, 9.5), (21.8, 14.5), (22, 21.5)], closed=True, r=S.r * 0.4)
    inner = "M5.5 23V12.5C5.5 7 18.5 7 18.5 12.5V23Z"
    return [
        shell(minus(outer, inner), stroke_miterlimit="2"),
        dot(12, 13.3, 1.4),
        line(arc(12, 13.3, 2.9, 205, 335)),
        mark(poly([(12, 15.4), (13.8, 21.5), (10.2, 21.5)], closed=True, r=L(S, 0, 0.6))),
        line(seg(8, 18.5, 8, 21.5)), dot(8, 16.3, 0.9),
        line(seg(16, 18.5, 16, 21.5)), dot(16, 16.3, 0.9),
    ]


@icon("easter-basket", CAT, "Woven basket with an arched handle holding three decorated eggs",
      tags=["easter", "egg hunt", "basket", "easter eggs", "spring", "holiday"])
def _(S):
    basket = poly([(3, 13.5), (21, 13.5), (19, 21), (5, 21)], closed=True, r=S.r)
    handle = poly([(3.5, 13.5), (3.5, 9)], r=0) + "C3.5 1 20.5 1 20.5 9V13.5"
    mid = ellipse(12, 9.6, 2.6, 3.4)
    sides = union(ellipse(7.3, 10.6, 2.4, 3.1), ellipse(16.7, 10.6, 2.4, 3.1))
    return [
        line(handle),
        shell(basket),
        detail(seg(4.2, 17.25, 19.8, 17.25)),
        shell(cut(mid, basket, 2.5)),
        detail(seg(9.7, 9.2, 14.3, 9.2)),
        shell(cut(cut(sides, mid, 2), basket, 2.5), stroke_miterlimit="2"),
    ]


def _(S):
    basket = poly([(3, 13.5), (21, 13.5), (19, 21), (5, 21)], closed=True, r=S.r)
    mid = ellipse(12, 8.8, 2.6, 3.4)
    sides = union(ellipse(7.6, 10.3, 2.4, 3), ellipse(16.4, 10.3, 2.4, 3))
    return [
        line(arc(12, 13.5, 9.5, 180, 360)),
        shell(basket),
        detail(seg(4.2, 17.25, 19.8, 17.25)),
        shell(cut(mid, basket, 2.8)),
        detail(seg(9.7, 8.4, 14.3, 8.4)),
        shell(cut(cut(sides, mid, 2.8), basket, 2.8), stroke_miterlimit="2"),
    ]


def _(S):
    tip = L(S, 0, 1.2)
    bag = union(ellipse(15, 9, 5.5, 2),
                f"M9.5 9C9.5 15 12 19.2 {fmt(15 - tip * 0.7)} {fmt(20.8 - tip * 0.2)}Q15 21 {fmt(15 + tip * 0.7)} {fmt(20.8 - tip * 0.2)}C18 19.2 20.5 15 20.5 9Z")
    return [
        line(seg(2, 9, 9.5, 9)),
        shell(bag),
        detail("M9.5 9A5.5 2 0 0 0 20.5 9"),
        shell(circle(15, 3.6, 2)),
    ]


# ============================================================================ places of worship

@icon("gothic-cathedral", CAT, "Cathedral front with two spired towers, a round rose window and a pointed doorway",
      tags=["cathedral", "gothic", "church", "notre dame", "minster", "architecture"], aliases=["cathedral"])
def _(S):
    pts = [(2.5, 21), (2.5, 8.5), (5, 2), (7.5, 8.5), (7.5, 10), (12, 6), (16.5, 10), (16.5, 8.5), (19, 2), (21.5, 8.5),
           (21.5, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        detail(seg(7.5, 10, 7.5, 21)), detail(seg(16.5, 10, 16.5, 21)),
        detail(circle(12, 12.3, 1.75)),
        detail("M10.25 21V19.2Q10.25 17.6 12 17Q13.75 17.6 13.75 19.2V21"),
        mark(rect(4.25, 12, 1.5, 3.5, L(S, 0, 0.75))), mark(rect(18.25, 12, 1.5, 3.5, L(S, 0, 0.75))),
    ]


@icon("basilica", CAT, "Columned church front with a triangular pediment and a large dome with a cross behind",
      tags=["basilica", "domed church", "saint peter's", "cathedral", "church", "architecture"])
def _(S):
    facade = union(poly([(2.5, 14.5), (12, 10.5), (21.5, 14.5)], closed=True), rect(3.5, 14.5, 17, 6.5))
    dome = "M5.5 11A6.5 6.5 0 0 1 18.5 11Z"
    return [
        line(small_cross(12, 1.6, 4.6, 2.9, 1.4)),
        shell(cut(dome, facade, 3), stroke_miterlimit="2"),
        shell(facade),
        detail(seg(3.5, 14.5, 20.5, 14.5)),
        *[detail(seg(x, 16.5, x, 21)) for x in (7, 10.5, 13.5, 17)],
    ]


@icon("monastery", CAT, "Walled monastery with a bell tower, a long roofed hall and an arched gateway",
      tags=["abbey", "convent", "priory", "monks", "cloister", "religious community"], aliases=["abbey"])
def _(S):
    wall = rect(2, 13, 20, 8, min(S.R, 1.5))
    tower = poly([(3.5, 13), (3.5, 6), (6, 2.5), (8.5, 6), (8.5, 13)], closed=True, r=S.r * 0.4)
    hall = poly([(11.5, 13), (11.5, 9), (13.5, 6.5), (21.5, 6.5), (21.5, 13)], closed=True, r=S.r * 0.4)
    return [
        shell(wall),
        detail("M10 21V18A2 2 0 0 1 14 18V21"),
        shell(cut(tower, wall, 3), stroke_miterlimit="2"),
        mark(rect(5.25, 6.8, 1.5, 2.2, L(S, 0, 0.75))),
        shell(cut(hall, wall, 3), stroke_miterlimit="2"),
    ]


@icon("catacomb", CAT, "Arched underground tunnel receding into the distance with burial niches in its walls",
      tags=["catacombs", "burial tunnel", "crypt", "underground", "tomb", "ossuary"], aliases=["catacombs"])
def _(S):
    niche_l = [poly([(4.5, 7.8), (7.2, 9), (7.2, 11), (4.5, 10.2)], closed=True, r=L(S, 0, 0.4)),
               poly([(4.5, 13.2), (7.2, 13.8), (7.2, 15.6), (4.5, 15.4)], closed=True, r=L(S, 0, 0.4))]
    return [
        line("M2.5 21.5V10C2.5 5 6.8 2.5 12 2.5C17.2 2.5 21.5 5 21.5 10V21.5"),
        mark("M9.8 16V12.5A2.2 2.2 0 0 1 14.2 12.5V16Z"),
        line(seg(2.5, 21.5, 9.2, 16.8)), line(seg(21.5, 21.5, 14.8, 16.8)),
        *[mark(d) for d in niche_l], *[mark(flip(d)) for d in niche_l],
    ]


@icon("western-wall", CAT, "Wall of large stone blocks with a plant growing from a joint and paper notes in the cracks",
      tags=["wailing wall", "kotel", "jerusalem", "prayer notes", "judaism", "stone wall"], aliases=["kotel", "wailing-wall"])
def _(S):
    parts = [
        shell(rect(2, 6, 20, 15, min(S.R, 1))),
        line("M17 6C17 4.3 18 3 20 2.6"), line("M17 6C16.6 4.6 15.4 3.8 13.8 3.8"),
    ]
    for y in (9.75, 13.5, 17.25):
        parts.append(detail(seg(2, y, 22, y)))
    for (y0, y1), xs in (((6, 9.75), (8.5, 15.5)), ((9.75, 13.5), (5.5, 12, 18.5)), ((13.5, 17.25), (8.5, 15.5)),
                         ((17.25, 21), (5.5, 12, 18.5))):
        for x in xs:
            parts.append(detail(seg(x, y0, x, y1)))
    parts += [mark(rect(11, 12.6, 2.2, 1.8, L(S, 0, 0.5))), mark(rect(14.5, 16.3, 2.2, 1.8, L(S, 0, 0.5)))]
    return parts


@icon("river-ghat", CAT, "Stone steps descending to rippling water with a small spired shrine at the top",
      tags=["ghat", "ganges", "varanasi", "bathing steps", "river steps", "pilgrimage"], aliases=["ghat"])
def _(S):
    steps = union(poly([(2, 17), (2, 9.5), (9, 9.5), (9, 12), (12, 12), (12, 14.5), (15, 14.5), (15, 17)], closed=True),
                  poly([(3, 9.5), (3, 6.5), (5.5, 2), (8, 6.5), (8, 9.5)], closed=True))
    return [
        shell(steps, stroke_miterlimit="2"),
        detail(seg(3, 9.5, 8, 9.5)),
        line("M2 20Q4.5 18.6 7 20T12 20T17 20T22 20"),
    ]


@icon("prayer-room", CAT, "Sign for a prayer room: a doorway with a kneeling figure holding folded hands",
      tags=["multifaith room", "chapel", "quiet room", "meditation room", "prayer", "wayfinding"],
      aliases=["multifaith-room"])
def _(S):
    return [
        line(poly([(4.5, 21), (4.5, 3.5), (19.5, 3.5), (19.5, 21)], r=S.r)),
        head(11, 7.8),
        limb(S, (11, 11.5), (10.5, 15.5), (13, 20), (7.5, 20)),
        limb(S, (11, 12), (13.8, 14.5), (14.8, 11.5)),
    ]


@icon("fire-temple", CAT, "Columned temple on a stepped base with a large flame rising above its roof",
      tags=["atash behram", "zoroastrian", "agiary", "sacred fire", "parsi", "temple"], aliases=["agiary"])
def _(S):
    top = union(flame(12, 2, 11, 7, S), rect(3, 9.5, 18, 3, L(S, 0.3, 1)))
    return [
        shell(top),
        detail("M12 5.8C13.5 7.2 13.6 8.4 12.9 9.5"),
        *[line(seg(x, 12.5, x, 17.5)) for x in (5.5, 9.8, 14.2, 18.5)],
        shell(poly([(3.5, 17.5), (20.5, 17.5), (20.5, 19.25), (22, 19.25), (22, 21.5), (2, 21.5), (2, 19.25), (3.5, 19.25)],
                   closed=True, r=S.r * 0.3)),
    ]


def _heart_leaf(cx, cy, s, deg=0.0):
    """Small heart-shaped leaf with a drawn-out tip pointing up (before rotation); (cx, cy) is its middle."""
    d = (f"M0 2.3C-1.2 3 -2.6 2.4 -2.6 0.8C-2.6 -0.8 -1 -1.8 0 -3.6C1 -1.8 2.6 -0.8 2.6 0.8C2.6 2.4 1.2 3 0 2.3Z")
    a = math.radians(deg)
    return path_to_d(transform_path(P(d), (s * math.cos(a), s * math.sin(a), -s * math.sin(a), s * math.cos(a), cx, cy)))


@icon("bodhi-tree", CAT, "Broad spreading tree with a thick trunk and heart-shaped leaves with long tips",
      tags=["bodhi", "peepal", "sacred fig", "buddha", "enlightenment", "tree"], aliases=["peepal-tree"])
def _(S):
    crown = union(circle(7, 9.5, 4.8), circle(12, 7, 5), circle(17, 9.5, 4.8), rect(4, 9.5, 16, 4.5, 2))
    trunk = poly([(10.5, 13), (13.5, 13), (13.5, 17.5), (16.5, 21), (7.5, 21), (10.5, 17.5)], closed=True)
    return [
        shell(union(crown, trunk), stroke_miterlimit="2"),
        mark(_heart_leaf(7.2, 9.8, 0.75, -25)), mark(_heart_leaf(12, 6.6, 0.75)), mark(_heart_leaf(16.8, 9.8, 0.75, 25)),
    ]


@icon("shinto-sacred-tree", CAT, "Old tree with a thick trunk girded by a straw rope hung with zigzag paper streamers",
      tags=["shinboku", "goshinboku", "shimenawa", "shide", "shinto", "sacred tree"], aliases=["shinboku"])
def _(S):
    crown = union(circle(7, 6.5, 4), circle(12, 5, 4), circle(17, 6.5, 4), rect(3, 6.5, 18, 2.5, 1.2))
    trunk = ("M9 8.5H15V16.5C15 19 16 20.5 18.5 21.5H5.5C8 20.5 9 19 9 16.5Z")
    rope = rect(4.5, 11.5, 15, 3.5, L(S, 1, 1.75))
    return [
        shell(union(crown, trunk, rope), stroke_miterlimit="2"),
        detail(seg(9, 11.5, 15, 11.5)), detail(seg(9, 15, 15, 15)),
        line(poly([(5.8, 15), (7.2, 16.5), (5.6, 18), (7, 19.5)], r=S.r * 0.4)),
        line(poly([(18.2, 15), (16.8, 16.5), (18.4, 18), (17, 19.5)], r=S.r * 0.4)),
    ]


def _(S):
    trunk = ("M5.5 21.5C8 20.5 8.8 19 8.8 16.5V8.5C8.8 6.5 7.5 4.5 5.5 2.5H8.5C10 4 11 5.5 12 7C13 5.5 14 4 15.5 2.5H18.5"
             "C16.5 4.5 15.2 6.5 15.2 8.5V16.5C15.2 19 16 20.5 18.5 21.5Z")
    rope = rect(4.5, 9.5, 15, 4, L(S, 1, 2))
    zz = "M5.5 14.5L7 16L5.3 17.5L6.8 19"
    return [
        shell(union(trunk, rope), stroke_miterlimit="2"),
        detail(seg(8.8, 9.5, 15.2, 9.5)), detail(seg(8.8, 13.5, 15.2, 13.5)),
        line(poly([(5.5, 14.5), (7, 16), (5.3, 17.5), (6.8, 19)], r=S.r * 0.4)),
        line(poly([(18.5, 14.5), (17, 16), (18.7, 17.5), (17.2, 19)], r=S.r * 0.4)),
    ]


# ============================================================================ scripture scenes

@icon("noahs-ark", CAT, "Wooden ark with a cabin on deck floating on a wave under a rainbow",
      tags=["noah", "ark", "flood", "bible story", "rainbow", "boat"], aliases=["noah-ark"])
def _(S):
    hull = poly([(2, 12.5), (22, 12.5), (19.5, 18), (4.5, 18)], closed=True, r=S.r * 0.5)
    cabin = poly([(7.5, 12.5), (7.5, 8.8), (12, 6), (16.5, 8.8), (16.5, 12.5)], closed=True, r=S.r * 0.5)
    return [
        line(arc(12, 12, 9.5, 212, 328)),
        shell(union(hull, cabin), stroke_miterlimit="2"),
        detail(seg(7.5, 12.5, 16.5, 12.5)),
        mark(rect(10.8, 8.8, 2.4, 2.2, L(S, 0, 0.5))),
        line("M2 21Q4.5 19.5 7 21T12 21T17 21T22 21"),
    ]


@icon("burning-bush", CAT, "Small rounded bush with flames rising from it",
      tags=["moses", "exodus", "bible story", "fire", "flame", "bush"])
def _(S):
    bush = union(circle(7, 17, 3.5), circle(12, 15.5, 4), circle(17, 17, 3.5), rect(3.5, 17, 17, 4.5, 1.5))
    flames = union(flame(12, 2, 12.5, 6, S), rotd(flame(6, 7, 13.5, 3.6, S), -20, 6, 13.5),
                   rotd(flame(18, 7, 13.5, 3.6, S), 20, 18, 13.5))
    return [
        shell(bush),
        detail("M9 21.5V19.2L7.5 17.8M9 19.2L10.5 17.8"), detail("M15 21.5V19.2L13.5 17.8M15 19.2L16.5 17.8"),
        shell(cut(flames, bush, 2.8), stroke_miterlimit="2"),
    ]


def _fish(cx, cy, dirn, S, k=0.85):
    """Fish of length about 7; dirn 1 = head to the right."""
    t = L(S, 0, 0.5)
    d = (f"M-4 0C-2.1 -2.4 1.2 -2.4 2.2 -0.6L{fmt(3.8 - t)} -2.1V2.1L2.2 0.6C1.2 2.4 -2.1 2.4 -4 0Z")
    return path_to_d(transform_path(P(d), (-dirn * k, 0, 0, k, cx, cy)))


@icon("loaves-and-fishes", CAT, "Basket holding two round loaves above two fish",
      tags=["feeding the five thousand", "miracle", "bread and fish", "bible story", "tabgha", "loaves"],
      aliases=["loaves-fishes"])
def _(S):
    basket = poly([(4, 10.5), (20, 10.5), (18.5, 14.5), (5.5, 14.5)], closed=True, r=S.r * 0.5)
    loaves = union("M5.5 10.5C5.5 5.2 11.2 5.2 11.2 10.5Z", "M12.8 10.5C12.8 5.2 18.5 5.2 18.5 10.5Z")
    return [
        shell(basket),
        shell(cut(loaves, basket, 2.5), stroke_miterlimit="2"),
        shell(_fish(5.6, 19.3, -1, S)), shell(_fish(18.4, 19.3, 1, S)),
        dot(3.9, 19.1, 0.75), dot(20.1, 19.1, 0.75),
    ]


@icon("tower-of-babel", CAT, "Tall tapering tower with a ramp spiralling up to an unfinished top",
      tags=["babel", "bible story", "genesis", "ziggurat", "tower", "languages"], aliases=["babel"])
def _(S):
    pts = [(3, 21.5), (21, 21.5), (16, 5), (14.8, 3.8), (13.4, 5), (12, 3.4), (10.4, 4.6), (9, 4), (8, 5)]
    lx = lambda y: 3 + (21.5 - y) * 5 / 16.5  # noqa: E731
    rx = lambda y: 21 - (21.5 - y) * 5 / 16.5  # noqa: E731
    parts = [shell(poly(pts, closed=True, r=S.r * 0.3), stroke_miterlimit="2")]
    for yl, yr in ((18.5, 14.8), (13.2, 9.6), (8.1, 5.9)):
        parts.append(detail(seg(lx(yl), yl, rx(yr), yr)))
    return parts


_CHERUB_L = "M7.8 9.8C8.4 7 9.8 5 11.4 3.5C11.8 6.5 11.2 8.8 9.6 11Z"


@icon("ark-of-the-covenant", CAT, "Chest on carrying poles with two winged figures facing each other on its lid",
      tags=["ark", "covenant", "tabernacle", "ten commandments", "bible", "cherubim"], aliases=["ark-covenant"])
def _(S):
    return [
        dot(6.6, 8.2, 1.4), dot(17.4, 8.2, 1.4),
        mark(poly([(5, 12), (5.8, 10.2), (8.4, 10.2), (9.6, 12)], closed=True, r=L(S, 0, 0.5))),
        mark(poly([(19, 12), (18.2, 10.2), (15.6, 10.2), (14.4, 12)], closed=True, r=L(S, 0, 0.5))),
        shell(_CHERUB_L), shell(flip(_CHERUB_L)),
        shell(rect(4, 12.5, 16, 6.5, min(S.R, 1.5))),
        detail(seg(4, 14.5, 20, 14.5)),
        line(seg(1.5, 16.75, 4, 16.75)), line(seg(20, 16.75, 22.5, 16.75)), detail(seg(4, 16.75, 20, 16.75)),
        line(seg(6, 19, 6, 21.5)), line(seg(18, 19, 18, 21.5)),
    ]


@icon("pearly-gates", CAT, "Arched double gate studded with pearls, standing on clouds with rays behind",
      tags=["heaven", "gates of heaven", "saint peter", "afterlife", "paradise", "gate"], aliases=["heaven-gate"])
def _(S):
    clouds = union(circle(5.5, 18.5, 3), circle(10, 17.2, 3.5), circle(14.5, 17.2, 3.5), circle(19, 18.5, 3),
                   rect(2.5, 18.5, 19, 3, 1.5))
    parts = [
        shell(clouds),
        line("M5.5 13.5V10A6.5 6.5 0 0 1 18.5 10V13.5"),
        line(seg(8.75, 5.6, 8.75, 12.5)), line(seg(12, 3.5, 12, 12.5)), line(seg(15.25, 5.6, 15.25, 12.5)),
        dot(8.75, 9.5, 1.3), dot(12, 9.5, 1.3), dot(15.25, 9.5, 1.3),
    ]
    for a in (-150, -30):
        parts.append(line(seg(*polar(12, 10, 8.6, a), *polar(12, 10, 10.6, a))))
    return parts


@icon("ladder-to-heaven", CAT, "Tall ladder rising from the ground into a cloud with rays of light",
      tags=["jacob's ladder", "stairway to heaven", "heaven", "ascension", "bible story", "ladder"],
      aliases=["jacobs-ladder"])
def _(S):
    cloud = union(circle(8.5, 6, 2.8), circle(12.5, 4.8, 3.3), circle(16, 6.5, 2.6), rect(6, 6, 12.5, 3, 1.5))
    lx = lambda y: 7.5 + (21.5 - y) * 2.5 / 10  # noqa: E731
    parts = [
        shell(cloud),
        line(seg(7.5, 21.5, 10, 11.5)), line(seg(16.5, 21.5, 14, 11.5)),
        line(seg(4.5, 9.8, 2.5, 12.5)), line(seg(19.5, 9.8, 21.5, 12.5)),
    ]
    for y in (19, 15.5, 12.5):
        parts.append(line(seg(lx(y), y, 24 - lx(y), y)))
    return parts


@icon("forbidden-fruit", CAT, "Apple with a leaf and a small snake coiled around its stem, head raised",
      tags=["garden of eden", "adam and eve", "temptation", "original sin", "serpent", "apple"],
      aliases=["apple-and-serpent"])
def _(S):
    apple = ("M12 9.5C10 8 5 8 4.5 13C4 18 7.5 21.5 10 21.5C11 21.5 11.5 21 12 21C12.5 21 13 21.5 14 21.5"
             "C16.5 21.5 20 18 19.5 13C19 8 14 8 12 9.5Z")
    return [
        shell(apple),
        line(seg(12, 9.5, 12.5, 5.5)),
        shell("M13.2 6.4C14.6 4.4 17 3.8 19.2 4.4C18.4 6.8 15.8 7.8 13.2 6.4Z" if S.name == "line" else
              "M13.2 6.4C14.6 4.4 17 3.8 18.6 4.2Q19.3 4.4 19 5C18 7 15.6 7.8 13.2 6.4Z"),
        line("M14 9C12.4 10.3 9.4 10 9.4 8.3C9.4 6.6 12.4 7 12.4 5.2C12.4 3.9 11 3.2 9.6 3.5"),
        dot(8.9, 3.7, 1.4),
        detail("M7.5 14.5C7.5 13 8.3 12 9.5 11.6"),
    ]


_WAVE_L = ("M2 21.5V6C2 3.8 3.6 2.5 5.4 2.5C7.6 2.5 9.2 4.2 9.2 6.2C9.2 7.8 8 8.9 6.6 8.6"
           "C7.4 12 7.6 16 7 21.5Z")


@icon("parting-sea", CAT, "Two towering walls of water curling on either side of a dry path",
      tags=["red sea", "exodus", "moses", "miracle", "bible story", "sea"], aliases=["red-sea"])
def _(S):
    return [
        shell(_WAVE_L), shell(flip(_WAVE_L)),
        detail("M4.2 8C4.2 6.2 5.2 5.3 6.4 5.6"), detail(flip("M4.2 8C4.2 6.2 5.2 5.3 6.4 5.6")),
        line(seg(9.8, 21.5, 11.2, 13)), line(seg(14.2, 21.5, 12.8, 13)),
    ]


# ============================================================================ jewish ritual objects

@icon("torah-crown", CAT, "Domed crown with a band, curved ribs meeting at a finial and small bells on its rim",
      tags=["keter torah", "torah crown", "synagogue", "judaica", "sefer torah", "crown"], aliases=["keter-torah"])
def _(S):
    body = union("M5.5 14.5C5.5 8.8 8 5.5 12 5C16 5.5 18.5 8.8 18.5 14.5Z", rect(4, 14, 16, 3.5, L(S, 0.5, 1.5)))
    parts = [
        dot(12, 3.3, 1.5),
        shell(body),
        detail(seg(5.5, 14, 18.5, 14)),
        detail("M9 14C9 10.5 10 7.8 12 5.6"), detail("M15 14C15 10.5 14 7.8 12 5.6"),
    ]
    for cx in (6.5, 12, 17.5):
        parts.append(mark(bell(cx, 18.2, 2.8, 21.5)))
    return parts


def _rimon(cx, S):
    knob = union(circle(cx, 8.5, 3), poly([(cx - 1.4, 6), (cx - 0.9, 3), (cx, 4.4), (cx + 0.9, 3), (cx + 1.4, 6)], closed=True))
    return [
        shell(knob, stroke_miterlimit="2"),
        line(seg(cx, 11.5, cx, 21.5)),
        line(seg(cx - 1.75, 17, cx + 1.75, 17)),
        dot(cx - 3.3, 13.4, 1), dot(cx + 3.3, 13.4, 1),
    ]


@icon("torah-finials", CAT, "Pair of Torah finials: stems topped by pomegranate-shaped knobs hung with little bells",
      tags=["rimonim", "torah finials", "synagogue", "judaica", "sefer torah", "pomegranate"], aliases=["rimonim"])
def _(S):
    return [*_rimon(7, S), *_rimon(17, S)]


@icon("chai-symbol", CAT, "The Hebrew word chai, meaning life, written with the letters chet and yud",
      tags=["chai", "life", "hebrew", "judaism", "jewish", "pendant"], aliases=["chai"])
def _(S):
    return [
        line(poly([(10.5, 20.5), (10.5, 4.5), (20, 4.5), (20, 20.5)], r=L(S, 0, 2.5))),
        line(poly([(4, 4.5), (7.5, 4.5), (7.5, 8.5), (5.2, 11)], r=S.r)),
    ]


@icon("hanukkah-gelt", CAT, "Small mesh bag tied at the top with round chocolate coins spilling out",
      tags=["gelt", "chanukah gelt", "chocolate coins", "hanukkah", "chanukah", "coins"], aliases=["chanukah-gelt"])
def _(S):
    bag = ("M4.5 20C2.5 20 2 17.5 3 14.5C3.8 12 5.5 10.5 6.5 9H9.5C10.5 10.5 12.2 12 13 14.5C14 17.5 13.5 20 11.5 20Z")
    top = poly([(5, 4.5), (11, 4.5), (9.6, 9), (6.4, 9)], closed=True)
    return [
        shell(union(bag, top), stroke_miterlimit="2"),
        detail(seg(6.4, 9, 9.6, 9)),
        detail(seg(4.2, 13.5, 10.4, 19.7)), detail(seg(11.8, 13.5, 5.6, 19.7)),
        shell(circle(17.5, 16.8, 4.3)),
        detail(circle(17.5, 16.8, 1.8)),
        shell(circle(18.5, 8.2, 2.5)),
    ]


@icon("memorial-candle", CAT, "Lit candle burning inside a glass tumbler",
      tags=["yahrzeit candle", "memorial light", "remembrance", "mourning", "jewish", "candle"], aliases=["yahrzeit-candle"])
def _(S):
    return [
        shell(poly([(5.5, 5), (18.5, 5), (17.2, 21), (6.8, 21)], closed=True, r=S.r)),
        detail(seg(6.25, 14, 17.75, 14)),
        mark(flame(12, 7.3, 12.3, 3, S)),
    ]


@icon("priestly-breastplate", CAT, "Square breastplate set with twelve gems in four rows of three, hung from two chains",
      tags=["hoshen", "breastplate of judgment", "high priest", "twelve tribes", "gemstones", "judaism"], aliases=["hoshen"])
def _(S):
    parts = [
        line(seg(6.5, 7.5, 4.8, 3.2)), line(seg(17.5, 7.5, 19.2, 3.2)), dot(4.4, 2.6, 1.4), dot(19.6, 2.6, 1.4),
        shell(rect(5, 7.5, 14, 14, L(S, 1.5, 3))),
    ]
    for y in (10, 12.9, 15.8, 18.7):
        for x in (8.5, 12, 15.5):
            parts.append(dot(x, y, 1.1))
    return parts


# ============================================================================ islamic practice

@icon("wudu-station", CAT, "Row of taps above a long washing trough with low stools in front",
      tags=["wudu", "ablution", "ablution area", "mosque", "washing", "islam"], aliases=["ablution-area"])
def _(S):
    parts = [
        line(seg(2, 4, 22, 4)),
        shell(rect(2, 12, 20, 4, L(S, 0.5, 2))),
    ]
    for x in (5.5, 12, 18.5):
        parts.append(line(poly([(x - 1, 4), (x - 1, 7), (x + 1, 7), (x + 1, 8.5)], r=S.r * 0.5)))
        parts.append(dot(x + 1, 10.3, 0.8))
        parts.append(line(seg(x - 1.75, 18.5, x + 1.75, 18.5)))
        parts.append(line(seg(x, 18.5, x, 21.5)))
    return parts


@icon("prostration-prayer", CAT, "Figure in prostration on a prayer mat, forehead and palms on the ground",
      tags=["sujood", "sajdah", "salah", "namaz", "prostrate", "muslim prayer"], aliases=["sujood"])
def _(S):
    return [
        line(seg(2, 21.5, 22, 21.5)),
        head(18.5, 16.6),
        limb(S, (3.5, 19), (8, 19), (8.5, 11), (15.5, 14)),
        limb(S, (15.5, 14), (14.5, 19)),
    ]


@icon("attar-bottle", CAT, "Small round cut-glass perfume bottle with a long thin stopper",
      tags=["attar", "ittar", "perfume oil", "fragrance", "oud", "perfume bottle"], aliases=["ittar-bottle"])
def _(S):
    t = L(S, 0, 0.5)
    stopper = f"M12 {fmt(2.6 + t)}C12.9 4.4 13.1 5.8 13 7H11C10.9 5.8 11.1 4.4 12 {fmt(2.6 + t)}Z"
    body = union(circle(12, 15.5, 5.5), rect(10.6, 8.8, 2.8, 2.5))
    return [
        shell(stopper, stroke_miterlimit="2"),
        shell(body),
        detail(poly([(12, 12.8), (14.7, 15.5), (12, 18.2), (9.3, 15.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("call-to-prayer", CAT, "Slender minaret with a balcony and a loudspeaker sending out sound waves",
      tags=["adhan", "azan", "minaret", "muezzin", "mosque", "prayer time"], aliases=["adhan", "azan"])
def _(S):
    body = union(poly([(8, 2), (10, 6.5), (6, 6.5)], closed=True), rect(6.5, 6.5, 3, 3), rect(4.8, 9.5, 6.4, 2),
                 rect(6.5, 11.5, 3, 10), poly([(9.5, 13.2), (13, 11.6), (13, 16.4), (9.5, 14.8)], closed=True))
    return [
        shell(body, stroke_miterlimit="2"),
        line(arc(13, 14, 3.2, -45, 45)), line(arc(13, 14, 6.5, -45, 45)),
    ]


@icon("moon-sighting", CAT, "Telescope on a tripod pointed up at a thin crescent moon",
      tags=["hilal", "moon sighting", "crescent moon", "ramadan", "eid", "islamic calendar"], aliases=["hilal-sighting"])
def _(S):
    tube = poly(rpts([(3.5, 10.8), (13.5, 10.8), (13.5, 14.2), (3.5, 14.2)], -33, 8.5, 12.5), closed=True, r=L(S, 0, 1))
    return [
        shell(minus(circle(18, 6, 4), circle(20, 4.6, 3.3)), stroke_miterlimit="2"),
        shell(tube),
        line(seg(8.5, 15, 4.5, 21.5)), line(seg(8.5, 15, 12.5, 21.5)), line(seg(8.5, 15, 8.5, 21.5)),
    ]


@icon("iftar-meal", CAT, "Bowl of dates beside a glass of water under a thin crescent moon",
      tags=["iftar", "ramadan", "breaking fast", "dates", "fasting", "suhoor"], aliases=["iftar"])
def _(S):
    return [
        shell(minus(circle(8, 5.5, 3.5), circle(9.8, 4.4, 3)), stroke_miterlimit="2"),
        mark(ellipse(5.2, 13.3, 1.3, 1.8)), mark(ellipse(8, 12.6, 1.3, 1.8)), mark(ellipse(10.8, 13.3, 1.3, 1.8)),
        shell("M2.5 15.5H13.5C13.5 18.5 11 21 8 21C5 21 2.5 18.5 2.5 15.5Z"),
        shell(poly([(15.5, 10), (21, 10), (20.3, 21), (16.2, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(15.75, 14, 20.75, 14)),
    ]


# ============================================================================ hindu practice

@icon("tilak-mark", CAT, "Face with a U-shaped tilak on the forehead and a dot below it",
      tags=["tilak", "tilaka", "namam", "bindi", "hindu", "forehead mark"], aliases=["tilaka"])
def _(S):
    return [
        shell(ellipse(12, 12.5, 7, 9)),
        detail(poly([(10, 4.6), (10, 9.8), (14, 9.8), (14, 4.6)], r=L(S, 0, 2))),
        dot(12, 12.4, 1),
        dot(8.8, 14.6, 1.1), dot(15.2, 14.6, 1.1),
        detail(arc(12, 16.2, 2.2, 40, 140)),
    ]


@icon("kamandalu", CAT, "Round water pot with a spout on one side and an arched handle over the top",
      tags=["kamandalu", "water pot", "ascetic", "sadhu", "hindu", "vessel"], aliases=["kamandal"])
def _(S):
    body = union(circle(11, 15.5, 5.5), rect(9, 8.5, 4, 3),
                 poly([(15.6, 12.6), (20.2, 8.6), (21.3, 9.6), (16.4, 15.8)], closed=True))
    return [
        shell(body, stroke_miterlimit="2"),
        line("M7.2 11.4C5.5 2.8 16.5 2.8 14.8 11.4"),
    ]


_SOLE = [(5.2, 21.5), (4, 16), (3.2, 9.5), (3.4, 5), (5, 2.5), (8, 2.5), (9.6, 5), (9.8, 9.5), (9, 16), (7.8, 21.5)]


@icon("paduka-sandals", CAT, "Pair of flat wooden sandals seen from above, each with a knob post at the toe",
      tags=["paduka", "wooden sandals", "toe knob sandal", "sadhu", "hindu", "footwear"], aliases=["paduka"])
def _(S):
    sole = poly(_SOLE, closed=True, r=L(S, 1.2, 2.5))
    sole_r = poly([(24 - x, y) for x, y in _SOLE], closed=True, r=L(S, 1.2, 2.5))
    return [shell(sole), dot(6.5, 6.5, 1.6), shell(sole_r), dot(17.5, 6.5, 1.6)]


@icon("floating-flower-bowl", CAT, "Shallow bowl of water with flower heads and a small candle floating on it",
      tags=["urli", "diwali", "floating candle", "flower bowl", "offering", "decoration"], aliases=["urli"])
def _(S):
    bowl = "M2 14H22C22 18 17.5 21 12 21C6.5 21 2 18 2 14Z"
    flowers = union(circle(3.8, 12.2, 1.4), circle(5.5, 11.3, 1.6), circle(7.2, 12.2, 1.4),
                    circle(16.8, 12.2, 1.4), circle(18.5, 11.3, 1.6), circle(20.2, 12.2, 1.4))
    candle = rect(10, 9, 4, 3.5, L(S, 0.4, 1))
    return [
        shell(bowl),
        shell(cut(flowers, bowl, 2.5)),
        shell(cut(candle, bowl, 2.5)),
        mark(flame(12, 2.5, 7.2, 2.6, S)),
    ]


@icon("vel-spear", CAT, "Tall staff topped by a broad leaf-shaped spear blade",
      tags=["vel", "murugan", "kartikeya", "spear", "lance", "hindu"], aliases=["vel"])
def _(S):
    t = L(S, 0, 0.6)
    blade = (f"M12 {fmt(2 + t)}C13.5 4.5 16.8 7.5 16.8 10.5C16.8 12.6 14.6 13.8 12 13.8C9.4 13.8 7.2 12.6 7.2 10.5"
             f"C7.2 7.5 10.5 4.5 12 {fmt(2 + t)}Z")
    return [
        shell(blade),
        detail(seg(12, 6, 12, 11)),
        shell(rect(10.5, 13.8, 3, 2.2, L(S, 0.3, 1))),
        line(seg(12, 16, 12, 22)),
    ]


@icon("vedic-birth-chart", CAT, "Square horoscope chart divided by both diagonals and an inner diamond into twelve houses",
      tags=["kundli", "janam kundali", "jyotish", "vedic astrology", "horoscope", "birth chart"], aliases=["kundli"])
def _(S):
    k = L(S, 0, 3)
    c = 3 + k * (1 - math.cos(math.radians(45))) if k else 3
    return [
        shell(rect(3, 3, 18, 18, k)),
        detail(seg(c, c, 24 - c, 24 - c)), detail(seg(24 - c, c, c, 24 - c)),
        detail(poly([(12, 3), (21, 12), (12, 21), (3, 12)], closed=True)),
    ]


@icon("shivling", CAT, "Rounded upright stone marked with three lines, set in a wide base with a spout",
      tags=["shiva lingam", "lingam", "shiva", "hindu", "temple", "shivalinga"], aliases=["shiva-lingam"])
def _(S):
    body = union("M8.5 14V7.5C8.5 4 10 2.5 12 2.5C14 2.5 15.5 4 15.5 7.5V14Z",
                 rect(2.5, 14, 15, 3.5, L(S, 0.5, 1.5)),
                 poly([(16.5, 14), (22, 15), (22, 17), (16.5, 17.5)], closed=True, r=S.r * 0.4),
                 rect(5.5, 17.5, 9, 4, min(S.R, 1)))
    return [
        shell(body, stroke_miterlimit="2"),
        detail(seg(8.5, 14, 15.5, 14)), detail(seg(5.5, 17.5, 14.5, 17.5)),
        detail(seg(9.5, 5.5, 14.5, 5.5)), detail(seg(9.5, 8.5, 14.5, 8.5)), detail(seg(9.5, 11.5, 14.5, 11.5)),
    ]
