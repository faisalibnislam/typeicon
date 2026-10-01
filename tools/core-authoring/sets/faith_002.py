"""TypeIcon Core: faith (batch 002).

Sacred objects, practices and symbols from many traditions, drawn respectfully from the objects themselves.
Figures follow the people icons (head dot r 2.25, 2 px limbs). The category takes no variant badges.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, polar, rotation, transform_path

CAT = "faith"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def flip(d):
    """Mirror a d-string across the vertical centre line."""
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpt(pts, deg, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    c, s_ = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s_, cy + (x - cx) * s_ + (y - cy) * c) for x, y in pts]


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def fpts(pts):
    """Mirror points across x = 12."""
    return [(24 - x, y) for x, y in pts]


# ============================================================================ Hindu, Buddhist and Himalayan

@icon("mangalsutra", CAT, "Mangalsutra: a necklace of small black beads with two gold disc pendants",
      tags=["mangalsutra", "necklace", "wedding", "marriage", "hindu", "bride", "jewellery"])
def _(S):
    parts = []
    # beads along a deep U from the upper corners to the pendant hanger
    pts = []
    for k in range(11):
        a = math.radians(-180 + 180 * (k / 10))
        pts.append((12 + 8.5 * math.cos(a), 3.5 - 9 * math.sin(a)))
    for i, (x, y) in enumerate(pts):
        if i in (4, 5, 6):
            continue
        parts.append(dot(x, y, 1.15))
    parts += [
        line(poly([pts[4], (8.5, 15.6)], r=S.r)),
        line(poly([pts[6], (15.5, 15.6)], r=S.r)),
        shell(circle(8.5, 18.2, 2.3)),
        shell(circle(15.5, 18.2, 2.3)),
    ]
    return parts


@icon("buddha-statue", CAT, "Seated Buddha statue in meditation on a low base",
      tags=["buddha", "buddhism", "statue", "meditation", "lotus position", "temple", "enlightenment"])
def _(S):
    head = union(circle(12, 6.2, 2.4), circle(12, 3.3, 1.1))
    body = poly([(9.3, 10.6), (14.7, 10.6), (15.8, 14.2), (20, 15.8), (20, 18), (4, 18), (4, 15.8), (8.2, 14.2)],
                closed=True, r=S.r)
    return [
        shell(head),
        shell(body),
        detail("M9.5 15.6Q12 17 14.5 15.6"),
        line(seg(5.5, 21, 18.5, 21)),
    ]


@icon("reclining-buddha", CAT, "Reclining Buddha lying on its side with the head resting on one hand",
      tags=["buddha", "reclining", "parinirvana", "statue", "buddhism", "temple"])
def _(S):
    head = union(circle(6, 9, 2.4), circle(3.8, 7.6, 1.1))
    body = L(S, "M8.8 13C11.5 11.8 14.5 11.6 16.8 12.9C18.6 13.9 20.2 14.9 21.2 16.4V18.2H8.8Z",
             "M10.3 12.4C12.7 11.7 15 11.8 16.8 12.9C18.6 13.9 20 14.8 20.8 15.8Q21.5 16.7 21 17.5Q20.6 18.2 19.6 18.2H10.3Q8.8 18.2 8.8 16.7V14.4Q8.8 12.9 10.3 12.4Z")
    return [
        mark(head),
        shell(body),
        line(poly([(6.6, 12.8), (4.2, 18.2)], r=S.r)),
        line(seg(2.5, 21, 21.5, 21)),
    ]


@icon("laughing-buddha-statue", CAT, "Laughing Buddha statue with a round belly and both arms raised",
      tags=["laughing buddha", "budai", "hotei", "happiness", "luck", "statue", "prosperity"],
      aliases=["budai"])
def _(S):
    return [
        shell(circle(12, 7, 2.5)),
        shell(ellipse(12, 15.8, 6, 5.2)),
        line(poly([(8, 11.8), (4.5, 8.5), (5.5, 3.5)], r=S.r)),
        line(poly([(16, 11.8), (19.5, 8.5), (18.5, 3.5)], r=S.r)),
        dot(12, 16.5, 1.1),
    ]


@icon("phurba", CAT, "Phurba: a ritual peg with a carved head, knotted grip and three-sided blade",
      tags=["phurba", "kila", "ritual dagger", "tibetan", "vajrayana", "buddhism", "peg"], aliases=["kila"])
def _(S):
    return [
        shell(circle(12, 3.6, 1.6)),
        shell(rect(10, 7, 4, 4.5, min(S.R, 1.5))),
        line(seg(7.5, 13, 16.5, 13)),
        shell(poly([(9, 15), (15, 15), (12, 21.2)], closed=True, r=S.r * 0.5), stroke_miterlimit="6"),
    ]


@icon("gau-amulet-box", CAT, "Gau: a small amulet box with an arched window and a loop for a cord",
      tags=["gau", "ghau", "amulet", "prayer box", "tibetan", "charm", "reliquary", "pendant"], aliases=["ghau"])
def _(S):
    return [
        line(circle(12, 3.8, 1.6)),
        shell(poly([(5, 21), (5, 11.5), (12, 6.5), (19, 11.5), (19, 21)], closed=True, r=S.r)),
        detail(L(S, "M9.5 18V14.5A2.5 2.5 0 0 1 14.5 14.5V18Z",
                 "M10.5 18A1 1 0 0 1 9.5 17V14.5A2.5 2.5 0 0 1 14.5 14.5V17A1 1 0 0 1 13.5 18Z")),
    ]


@icon("butsudan", CAT, "Butsudan: a household shrine cabinet with open doors and a small seated figure",
      tags=["butsudan", "household altar", "shrine", "buddhist", "japanese", "cabinet", "ancestors"])
def _(S):
    return [
        shell(rect(7.5, 3, 9, 18, min(S.R, 2))),
        line(poly([(5.5, 4.5), (2.5, 6), (2.5, 18), (5.5, 19.5)], r=S.r)),
        line(poly([(18.5, 4.5), (21.5, 6), (21.5, 18), (18.5, 19.5)], r=S.r)),
        dot(12, 7.3, 1.3),
        mark("M9.8 12.7A2.2 2.2 0 0 1 14.2 12.7Z"),
        detail(seg(7.5, 15, 16.5, 15)),
    ]


@icon("five-ring-pagoda", CAT, "Five-ring pagoda: a stone stupa of cube, sphere, roof, bowl and jewel",
      tags=["gorinto", "gorintou", "stupa", "grave marker", "japanese", "buddhist", "five elements"],
      aliases=["gorinto"])
def _(S):
    roof = poly([(4.5, 11.2), (19.5, 11.2), (12, 7.8)], closed=True, r=S.r * 0.4)
    body = union(rect(7, 16.5, 10, 5, L(S, 0, 1)), circle(12, 13.6, 3.3), roof,
                 "M9.3 7.9A2.7 2.7 0 0 0 14.7 7.9Z",
                 "M12 2.3C13.3 3.6 13.9 4.6 13.9 5.4A1.9 1.9 0 0 1 10.1 5.4C10.1 4.6 10.7 3.6 12 2.3Z")
    return [
        shell(body),
        detail(seg(9.3, 11.2, 14.7, 11.2)),
        detail(seg(9.2, 16.5, 14.8, 16.5)),
    ]


def _sole(S):
    top = "M7 7.4C9.4 7.4 10.6 9.2 10.6 11.7C10.6 14.6 9.8 16.4 9.8 18.6"
    end = "A2.8 2.8 0 0 1 4.2 18.6" if S.name == "rounded" else "L9 21.2H5L4.2 18.6"
    return top + end + "C4.2 16.4 3.4 14.6 3.4 11.7C3.4 9.2 4.6 7.4 7 7.4Z"


@icon("sacred-footprints", CAT, "Sacred footprints: a pair of soles, each marked with a small wheel",
      tags=["buddhapada", "footprints of the buddha", "feet", "soles", "pilgrimage", "wheel", "relic"],
      aliases=["buddhapada"])
def _(S):
    left = [shell(_sole(S)), detail(circle(7, 12.6, 1.9)), dot(7, 12.6, 0.7),
            dot(9.4, 4.6, 1.25), dot(6.5, 4, 1), dot(4.2, 5, 0.95)]
    right = [Part(p.kind, flip(p.d), p.attrs) for p in left]
    return left + right


@icon("tibetan-scripture-bundle", CAT, "Tibetan scripture bundle: loose pages between two boards, tied with a strap",
      tags=["pecha", "tibetan book", "scripture", "sutra", "texts", "buddhist", "manuscript"], aliases=["pecha"])
def _(S):
    return [
        shell(rect(2, 7, 20, 10, min(S.R, 2))),
        detail(seg(2, 10, 9.5, 10)), detail(seg(14.5, 10, 22, 10)),
        detail(seg(2, 14, 9.5, 14)), detail(seg(14.5, 14, 22, 14)),
        mark(rect(10.5, 5, 3, 14, L(S, 0, 1))),
    ]


@icon("wisdom-eyes", CAT, "Wisdom eyes: two half-closed eyes under heavy brows with a curled nose between them",
      tags=["buddha eyes", "stupa eyes", "all-seeing", "nepal", "buddhism", "wisdom", "compassion"],
      aliases=["buddha-eyes"])
def _(S):
    eye = L(S, "M3 12.5Q6.5 10.5 10 12.5Q6.5 15.5 3 12.5Z", "M3.4 12.3Q6.5 10.5 9.6 12.3Q10 12.6 9.6 12.9Q6.5 15.5 3.4 12.9Q3 12.6 3.4 12.3Z")
    return [
        line("M2.5 8.5Q6.5 5 10.5 8"),
        line(flip("M2.5 8.5Q6.5 5 10.5 8")),
        shell(eye), shell(flip(eye)),
        line("M10.6 12.2C10.3 10.3 13.7 10.3 13.4 12.2C13.2 13.6 12 13.9 12 15.8"),
        dot(12, 19, 1.2),
    ]


@icon("treasure-vase", CAT, "Treasure vase: a plump vase with a flaming jewel rising from its mouth",
      tags=["bumpa", "treasure vase", "auspicious symbol", "ashtamangala", "wealth", "buddhism", "vase"])
def _(S):
    body = union(ellipse(12, 16, 6.2, 5.2), rect(10.5, 10, 3, 3), rect(8.6, 9, 6.8, 2, L(S, 0, 1)),
                 "M12 2C14 3.8 14.8 5.1 14.8 6.2A2.8 2.8 0 0 1 9.2 6.2C9.2 5.1 10 3.8 12 2Z")
    return [shell(body), detail("M7 16Q12 18.3 17 16")]


@icon("ceremonial-parasol", CAT, "Ceremonial parasol: a domed umbrella with a scalloped fringe and jewel finial",
      tags=["chhatra", "parasol", "royal umbrella", "auspicious symbol", "ashtamangala", "canopy", "honour"],
      aliases=["chhatra"])
def _(S):
    dome = ("M3.5 11.5A8.5 7 0 0 1 20.5 11.5" + "".join(
        f"A2.125 2.125 0 0 1 {fmt(20.5 - 4.25 * (k + 1))} 11.5" for k in range(4)) + "Z")
    fin = (poly([(12, 1.8), (13.3, 3.3), (12, 4.8), (10.7, 3.3)], closed=True) if S.name == "line"
           else circle(12, 3.3, 1.4))
    return [shell(dome), mark(fin), line(seg(12, 14.5, 12, 21.5))]


@icon("purification-basin", CAT, "Purification basin: a stone basin fed by a bamboo spout with a ladle across it",
      tags=["chozubachi", "temizuya", "water basin", "purification", "shinto", "shrine", "ablution"],
      aliases=["chozubachi"])
def _(S):
    return [
        shell(poly([(2, 3.5), (11, 3.5), (9.8, 6.5), (2, 6.5)], closed=True, r=S.r * 0.5)),
        line(seg(2.5, 11, 15, 11)),
        shell(rect(15, 7.5, 5, 4.5, min(S.R, 1.5))),
        shell(rect(2.5, 14, 19, 7.5, min(S.R, 2))),
    ]


@icon("gohei-wand", CAT, "Gohei: a wooden wand with two zigzag strips of folded paper",
      tags=["gohei", "shide", "shinto", "purification", "wand", "ritual", "shrine"], aliases=["gohei"])
def _(S):
    zig = [(10.5, 4), (6.5, 4), (9.5, 8), (5, 8), (8, 12), (3.5, 12), (6.5, 16.5)]
    return [
        line(seg(12, 2.5, 12, 21.5)),
        line(poly(zig, r=S.r * 0.5)),
        line(poly(fpts(zig), r=S.r * 0.5)),
    ]


@icon("jizo-statue", CAT, "Jizo statue: a small round-headed stone monk with a cloth bib, holding a staff",
      tags=["jizo", "ojizo-san", "bodhisattva", "guardian", "roadside statue", "japanese", "children"],
      aliases=["ojizo"])
def _(S):
    robe = poly([(7.8, 11), (14.2, 11), (16, 21.5), (6, 21.5)], closed=True, r=S.r)
    return [
        shell(circle(11, 6, 3.2)),
        shell(robe),
        detail(L(S, "M8.6 11L11 15.5L13.4 11", "M8.6 11Q11 17 13.4 11")),
        line(seg(19.5, 6.5, 19.5, 21.5)),
        line(circle(19.5, 3.8, 1.6)),
    ]


@icon("kagura-bells", CAT, "Kagura bells: a short handle topped by three tiers of small bells, with ribbons",
      tags=["kagura suzu", "suzu", "shinto", "shrine dance", "bells", "miko", "ritual"], aliases=["kagura-suzu"])
def _(S):
    bells = [(12, 3.4), (9.2, 7), (14.8, 7), (6.4, 10.6), (12, 10.6), (17.6, 10.6)]
    parts = [dot(x, y, 1.45) for x, y in bells]
    parts += [
        line(seg(5, 13.4, 19, 13.4)),
        shell(rect(10.5, 15.4, 3, 6.2, min(S.R, 1.5))),
        line("M8.5 15.8C8.5 17.6 6.2 18.2 6.2 20.5"),
        line("M15.5 15.8C15.5 17.6 17.8 18.2 17.8 20.5"),
    ]
    return parts


def _magatama():
    head = circle(12, 7.5, 4.5)
    half = "M12 3A9 9 0 0 0 12 21Z"
    return minus(union(head, minus(circle(12, 12, 9), "M12 2H22V22H12Z")), circle(12, 16.5, 4.5))


@icon("magatama-bead", CAT, "Magatama: a comma-shaped curved jewel with a hole through its round head",
      tags=["magatama", "curved jewel", "japanese", "shinto", "amulet", "bead", "jade"], aliases=["magatama"])
def _(S):
    body = rot(_magatama(), 20)
    hx, hy = polar(12, 12, 4.5, -90 + 20)
    return [shell(body, stroke_miterlimit=L(S, "10", "4")), detail(circle(hx, hy, 1.4))]


@icon("i-ching-coins", CAT, "Three round coins with square holes arranged in a triangle, used for I Ching casting",
      tags=["i ching", "yijing", "divination", "coins", "chinese", "taoism", "fortune", "cash coins"])
def _(S):
    parts = []
    for cx, cy in ((12, 6.2), (6.5, 16.8), (17.5, 16.8)):
        parts += [shell(circle(cx, cy, 4.2)), detail(rect(cx - 1.4, cy - 1.4, 2.8, 2.8, L(S, 0, 0.7)))]
    return parts


@icon("village-guardian-post", CAT, "Village guardian posts: two tall carved wooden posts with grinning faces and hats",
      tags=["jangseung", "totem", "guardian", "korean", "village", "folk religion", "carved post"],
      aliases=["jangseung"])
def _(S):
    parts = []
    for x in (3, 13.5):
        cx = x + 3.75
        parts += [
            shell(rect(x + 0.9, 2.5, 5.7, 3.3, min(S.R, 1.2))),
            line(seg(x - 0.5, 7.5, x + 8, 7.5)),
            shell(rect(x, 9.5, 7.5, 12, min(S.R, 2.5))),
            dot(cx - 1.7, 12.6, 1.05), dot(cx + 1.7, 12.6, 1.05),
            detail(L(S, f"M{fmt(cx - 2)} 16L{fmt(cx)} 18.3L{fmt(cx + 2)} 16Z",
                     f"M{fmt(cx - 2)} 16Q{fmt(cx)} 19.2 {fmt(cx + 2)} 16Z")),
        ]
    return parts


@icon("five-elements-cycle", CAT, "Five elements cycle: five circles in a ring joined by arrows, with a star of lines inside",
      tags=["wu xing", "five phases", "five elements", "chinese philosophy", "taoism", "cycle", "feng shui"],
      aliases=["wu-xing"])
def _(S):
    R = 8.3
    c = (12, 12.3)
    pts = [polar(c[0], c[1], R, -90 + 72 * k) for k in range(5)]
    parts = [dot(x, y, 1.9) for x, y in pts]
    for k in range(5):
        a0, a1 = -90 + 72 * k + 22, -90 + 72 * (k + 1) - 24
        parts.append(line(arc(c[0], c[1], R, a0, a1)))
        tip = polar(c[0], c[1], R, a1)
        t = math.radians(a1 + 90)
        back = (tip[0] - 1.7 * math.cos(t), tip[1] - 1.7 * math.sin(t))
        n = (math.cos(math.radians(a1)), math.sin(math.radians(a1)))
        parts.append(line(poly([(back[0] + 1.5 * n[0], back[1] + 1.5 * n[1]), tip,
                                (back[0] - 1.5 * n[0], back[1] - 1.5 * n[1])], r=S.r * 0.3)))
    v = regular(c[0], c[1], 3.6, 5)
    parts.append(shell(poly([v[0], v[2], v[4], v[1], v[3]], closed=True, r=S.r * 0.3), stroke_miterlimit="1"))
    return parts


@icon("kirpan", CAT, "Kirpan: a short curved ceremonial dagger in its sheath",
      tags=["kirpan", "sikh", "sikhism", "five ks", "dagger", "khalsa", "article of faith"])
def _(S):
    sheath = L(S, "M10.4 11H13.6V15.5C13.6 18.2 12.5 20.2 10.2 21.8C10.8 19.8 10.4 17.4 10.4 15.5Z",
               "M11.4 11H12.6Q13.6 11 13.6 12V15.5C13.6 18.2 12.6 20.1 10.8 21.4Q10.2 21.8 10.4 21C10.7 19.2 10.4 17.3 10.4 15.5V12Q10.4 11 11.4 11Z")
    parts = [shell(rect(10.8, 2.6, 2.4, 5, L(S, 0, 1.2))), shell(sheath)]
    parts = [Part(p.kind, rot(p.d, 30), p.attrs) for p in parts]
    return parts + [line(poly(rpt([(8.2, 9.3), (15.8, 9.3)], 30)))]


# ============================================================================ Egyptian, pagan and esoteric

@icon("djed-pillar", CAT, "Djed pillar: an upright column with four stacked bars across its top on a flared base",
      tags=["djed", "ancient egypt", "osiris", "stability", "hieroglyph", "pillar", "egyptian"], aliases=["djed"])
def _(S):
    parts = [shell(rect(9.5, 2.5, 5, 15.5, min(S.R, 1.5))),
             shell(poly([(9, 18), (15, 18), (17, 21.5), (7, 21.5)], closed=True, r=S.r * 0.5))]
    for y in (5, 8.2, 11.4, 14.6):
        parts += [line(seg(5, y, 9.5, y)), line(seg(14.5, y, 19, y)), detail(seg(9.5, y, 14.5, y))]
    return parts


@icon("canopic-jar", CAT, "Canopic jar: a tall rounded jar with a lid carved as a jackal head",
      tags=["canopic jar", "ancient egypt", "mummy", "jackal", "anubis", "burial", "egyptian", "museum"])
def _(S):
    head = poly([(8.2, 10), (8.2, 6.6), (8.8, 2.8), (10.8, 5.2), (13.2, 5.2), (15.2, 2.8), (15.8, 6.6), (15.8, 10)],
                closed=True, r=S.r * 0.6)
    jar = L(S, "M7.5 12H16.5L17.5 15.5C17.5 18.5 16 20.5 14.5 21.5H9.5C8 20.5 6.5 18.5 6.5 15.5Z",
            "M8.5 12H15.5Q16.4 12 16.7 12.9L17.5 15.5C17.5 18.5 16 20.5 14.5 21.5H9.5C8 20.5 6.5 18.5 6.5 15.5L7.3 12.9Q7.6 12 8.5 12Z")
    return [shell(head), dot(10.5, 7.8, 0.9), dot(13.5, 7.8, 0.9), shell(jar)]


@icon("sarcophagus", CAT, "Sarcophagus: an upright human-shaped coffin with a face, headdress and crossed arms",
      tags=["sarcophagus", "coffin", "mummy case", "ancient egypt", "pharaoh", "tomb", "museum", "egyptian"])
def _(S):
    pts = [(12, 2), (15.5, 3), (18.5, 11), (15.8, 21.5), (8.2, 21.5), (5.5, 11), (8.5, 3)]
    outline = poly(pts, closed=True, r=S.r)
    return [
        shell(outline),
        detail(L(S, "M10 6.2V8.4Q10 10.4 12 10.4Q14 10.4 14 8.4V6.2Z",
                 "M10.8 6.2H13.2Q14 6.2 14 7V8.4Q14 10.4 12 10.4Q10 10.4 10 8.4V7Q10 6.2 10.8 6.2Z")),
        detail(poly([(8, 13.8), (12, 16.2), (16, 13.8)], r=S.r * 0.6)),
        detail(seg(10, 18.6, 14, 18.6)),
    ]


@icon("winged-sun-disk", CAT, "Winged sun disk: a round sun at the centre with long outspread wings",
      tags=["winged sun", "behdet", "horus", "ancient egypt", "sun", "wings", "egyptian", "protection"])
def _(S):
    wing = poly([(7.4, 9.4), (1.8, 7.4), (2.4, 10.6), (4.8, 13.8), (7.4, 13.6)], closed=True, r=S.r * 0.6)
    feather = seg(3.8, 10.8, 7.4, 11.6)
    return [shell(circle(12, 11.5, 3)), shell(wing), shell(flip(wing)),
            detail(feather), detail(seg(24 - 3.8, 10.8, 24 - 7.4, 11.6))]


@icon("pentacle", CAT, "Pentacle: a five-pointed star drawn as one line inside a circle, one point up",
      tags=["pentacle", "wicca", "pagan", "witchcraft", "star in circle", "occult", "five elements"])
def _(S):
    v = regular(12, 12, 8.9, 5)
    star = poly([v[0], v[2], v[4], v[1], v[3]], closed=True)
    star = poly([v[0], v[2], v[4], v[1], v[3]], closed=True, r=S.r * 0.6)
    return [shell(circle(12, 12, 9.4)), detail(star, stroke_miterlimit="1")]


@icon("awen", CAT, "Awen: three rays fanning downward beneath three dots, inside a circle",
      tags=["awen", "druid", "druidry", "celtic", "pagan", "inspiration", "three rays"])
def _(S):
    return [
        shell(circle(12, 12, 9.2)),
        dot(8.6, 7.4, 1.2), dot(12, 6.2, 1.2), dot(15.4, 7.4, 1.2),
        detail(seg(9.5, 10, 6.8, 16.8)), detail(seg(12, 9.4, 12, 18.2)), detail(seg(14.5, 10, 17.2, 16.8)),
    ]


@icon("spiral-goddess", CAT, "Spiral goddess: a simple female figure with arms curved above the head and a spiral on the belly",
      tags=["goddess", "spiral goddess", "pagan", "wicca", "divine feminine", "fertility", "earth mother"])
def _(S):
    body = "M12 9.5C9.2 9.5 7.2 12 7.2 15C7.2 17.6 8.4 19.8 9.8 21.5H14.2C15.6 19.8 16.8 17.6 16.8 15C16.8 12 14.8 9.5 12 9.5Z"
    return [
        dot(12, 6, 2.1),
        line("M9.4 10.6C5.6 9.8 3.8 6.6 5 2.8"),
        line(flip("M9.4 10.6C5.6 9.8 3.8 6.6 5 2.8")),
        shell(body),
        detail(arc(12, 15.2, 2.2, -60, 230)),
        dot(12, 15.2, 0.8),
    ]


def _lens(c1, c2, r):
    """Overlap of two equal discs of radius r."""
    return path_to_d(D(P(circle(*c1, r)), D(P(circle(*c1, r)), P(circle(*c2, r)))))


@icon("vesica-piscis", CAT, "Vesica piscis: two equal overlapping circles with the almond-shaped overlap marked",
      tags=["vesica piscis", "mandorla", "sacred geometry", "ichthys", "overlap", "christian symbol", "geometry"],
      aliases=["mandorla"])
def _(S):
    r = 6.6
    a, b = (8.7, 12), (15.3, 12)
    if S.name == "rounded":
        almond = _lens(a, b, r - 2.8)
        almond = path_to_d(U(P(almond), ST(almond, 1.6, "round", "round")))
    else:
        almond = _lens(a, b, r - 2.1)
    return [line(circle(*a, r)), line(circle(*b, r)), mark(almond)]


@icon("flaming-chalice", CAT, "Flaming chalice: a stemmed cup with a large flame, framed by two overlapping rings",
      tags=["flaming chalice", "chalice", "flame", "unitarian", "universalist", "liberal religion", "church"])
def _(S):
    bowl = L(S, "M8.5 12.5H15.5C15.5 14.6 14 16 12 16C10 16 8.5 14.6 8.5 12.5Z",
             "M9.3 12.5H14.7Q15.5 12.5 15.4 13.3C15.1 14.9 13.8 16 12 16C10.2 16 8.9 14.9 8.6 13.3Q8.5 12.5 9.3 12.5Z")
    flame = "M12 4C14 6 15 7.6 15 9.2A3 3 0 0 1 9 9.2C9 8 9.6 7.2 10.3 6.6C10.5 7.6 11 8.2 11.5 8.3C11.3 6.8 11.4 5.4 12 4Z"
    return [
        line(arc(8.2, 12, 6.2, 70, 290)), line(arc(15.8, 12, 6.2, 250, 470)),
        shell(flame), shell(bowl),
        line(seg(12, 16.5, 12, 19)),
        line(seg(9.5, 19.5, 14.5, 19.5)),
    ]


@icon("astral-projection", CAT, "Astral projection: a figure lying on a bed with a dashed copy of it floating above",
      tags=["astral projection", "out of body", "astral travel", "soul", "lucid dream", "spirit", "mysticism"],
      aliases=["out-of-body"])
def _(S):
    return [
        dot(5.5, 14.6, 2.1), line(seg(9, 15, 20.5, 15)),
        line(poly([(2.5, 13), (2.5, 21.5)], r=S.r)), line(seg(2.5, 18.5, 21.5, 18.5)), line(seg(21.5, 18.5, 21.5, 21.5)),
        shell(circle(6, 6.5, 2.1)),
        line(seg(10, 7, 12.5, 7)), line(seg(15, 7, 17.5, 7)), line(seg(20, 7, 21.5, 7)),
    ]


@icon("third-eye", CAT, "Third eye: a face with an extra open eye in the forehead, surrounded by small rays",
      tags=["third eye", "ajna", "intuition", "insight", "chakra", "spiritual awakening", "mind's eye"],
      aliases=["ajna"])
def _(S):
    eye = L(S, "M8.8 10.5Q12 7.6 15.2 10.5Q12 13.4 8.8 10.5Z", "M9.3 10.1Q12 7.9 14.7 10.1Q15.2 10.5 14.7 10.9Q12 13.1 9.3 10.9Q8.8 10.5 9.3 10.1Z")
    return [
        shell(ellipse(12, 14, 6.8, 7.6)),
        detail(eye), dot(12, 10.5, 0.9),
        dot(9.4, 15.4, 1.05), dot(14.6, 15.4, 1.05),
        line(seg(12, 1.8, 12, 3.8)), line(seg(6.6, 3.2, 7.8, 4.8)), line(seg(17.4, 3.2, 16.2, 4.8)),
    ]


@icon("aura-person", CAT, "Aura: a standing figure surrounded by two glowing outlines that follow its shape",
      tags=["aura", "energy field", "glow", "spiritual", "chakra", "energy healing", "presence"])
def _(S):
    return [
        dot(12, 10.2, 1.9),
        line(L(S, "M9.2 21.5V16.8A2.8 2.8 0 0 1 14.8 16.8V21.5", "M9.2 21.5V16.8A2.8 2.8 0 0 1 14.8 16.8V21.5")),
        line("M6.2 21.5V11.2A5.8 5.8 0 0 1 17.8 11.2V21.5"),
        line("M3 21.5V11.5A9 9 0 0 1 21 11.5V21.5"),
    ]


@icon("tea-leaf-reading", CAT, "Tea leaf reading: a teacup on a saucer seen from above with leaves scattered inside",
      tags=["tasseography", "tea leaves", "fortune telling", "divination", "teacup", "reading", "psychic"],
      aliases=["tasseography"])
def _(S):
    leaf = "M-1.3 0Q0 -1.1 1.3 0Q0 1.1 -1.3 0Z"

    def lf(x, y, a):
        return path_to_d(transform_path(P(leaf), (math.cos(math.radians(a)), math.sin(math.radians(a)),
                                                    -math.sin(math.radians(a)), math.cos(math.radians(a)), x, y)))
    return [
        line(circle(12, 12, 9.5)),
        shell(circle(11, 12, 5.4)),
        line(seg(17.4, 12, 19.5, 12)),
        mark(lf(9.6, 10.4, 30)), mark(lf(12.8, 11.2, -40)), mark(lf(10.4, 13.9, 80)),
    ]


@icon("incense-cone", CAT, "Incense cone: a small cone of incense on a round dish with a curl of smoke",
      tags=["incense", "incense cone", "aroma", "fragrance", "meditation", "smoke", "ritual", "relax"])
def _(S):
    return [
        shell(poly([(8.8, 16.5), (15.2, 16.5), (12, 9.8)], closed=True, r=S.r * 0.6)),
        shell(L(S, "M3.5 18.5H20.5Q19.5 21.5 12 21.5Q4.5 21.5 3.5 18.5Z",
                "M4.5 18.5H19.5Q20.6 18.5 20.1 19.5Q18.7 21.5 12 21.5Q5.3 21.5 3.9 19.5Q3.4 18.5 4.5 18.5Z")),
        line("M12 7.6C10.6 6.4 13.2 5 11.8 3.6C11 2.8 11.8 2 12.8 2"),
    ]


@icon("worry-stone", CAT, "Worry stone: a smooth oval stone with a thumb resting in the dip in its middle",
      tags=["worry stone", "thumb stone", "palm stone", "anxiety", "calm", "fidget", "stress relief"])
def _(S):
    th0, th1 = (19.6, 3.6), (13.6, 11.6)
    thumb = path_to_d(U(ST(seg(*th0, *th1), 5.4, "butt", "round"), P(circle(*th1, 2.7))))
    ux, uy = (th1[0] - th0[0]), (th1[1] - th0[1])
    ln = math.hypot(ux, uy)
    ux, uy = ux / ln, uy / ln
    px, py = -uy, ux  # across the thumb
    c = (th1[0] - ux * 0.6, th1[1] - uy * 0.6)
    w = 1.2
    nail = (f"M{fmt(c[0] - ux * 2.4 + px * w)} {fmt(c[1] - uy * 2.4 + py * w)}"
            f"L{fmt(c[0] + px * w)} {fmt(c[1] + py * w)}"
            f"A{w} {w} 0 0 0 {fmt(c[0] - px * w)} {fmt(c[1] - py * w)}"
            f"L{fmt(c[0] - ux * 2.4 - px * w)} {fmt(c[1] - uy * 2.4 - py * w)}")
    stone = ellipse(11, 15.2, 8.8, 6)
    stone = path_to_d(D(P(stone), U(P(thumb), ST(thumb, 4, "round", "round"))))
    return [shell(stone), shell(thumb), detail(nail), detail("M5.4 16.4Q8 18.8 11.8 17.8")]


def _feather(x, y, a):
    d = "M0 0Q1.5 2.6 0 5.8Q-1.5 2.6 0 0Z"
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    return path_to_d(transform_path(P(d), (ca, sa, -sa, ca, x, y)))


@icon("medicine-wheel", CAT, "Medicine wheel: a circle divided into four quarters by a cross, with two feathers hanging below",
      tags=["medicine wheel", "sacred hoop", "four directions", "indigenous", "native american", "first nations", "healing"],
      aliases=["sacred-hoop"])
def _(S):
    return [
        shell(circle(12, 9, 6.6)),
        detail(seg(12, 2.4, 12, 15.6)), detail(seg(5.4, 9, 18.6, 9)),
        line(seg(8.6, 15, 7.8, 16.4)), line(seg(15.4, 15, 16.2, 16.4)),
        mark(_feather(7.4, 16.2, 12)), mark(_feather(16.6, 16.2, -12)),
    ]


@icon("talking-stick", CAT, "Talking stick: a carved stick with a wrapped grip, a band of beads and feathers tied near the top",
      tags=["talking stick", "speaking staff", "council", "indigenous", "circle", "turn taking", "community"])
def _(S):
    grip = rot(rect(10.5, 14, 3, 7.5, min(S.R, 1.5)), 45)
    bands = [rpt([(10.5, y), (13.5, y)], 45) for y in (16.5, 19)]
    stick = rpt([(12, 2.5), (12, 14)], 45)
    tie = rpt([(12, 5.5)], 45)[0]
    parts = [line(seg(*stick[0], *stick[1])), shell(grip)]
    parts += [detail(seg(*b[0], *b[1])) for b in bands]
    parts += [
        line(poly([tie, (tie[0], tie[1] + 2.2)], r=0)),
        dot(tie[0], tie[1] + 3.4, 1.3),
        mark(_feather(tie[0] - 1.1, tie[1] + 4.8, 14)), mark(_feather(tie[0] + 1.1, tie[1] + 4.8, -14)),
    ]
    return parts


@icon("worship-raised-hands", CAT, "Worship: a figure with both arms raised high overhead and palms open",
      tags=["worship", "praise", "raised hands", "hands up", "adoration", "church", "gospel"])
def _(S):
    return [
        dot(12, 9, 2.2),
        line(poly([(5.5, 5.4), (7.8, 12.2), (16.2, 12.2), (18.5, 5.4)], r=S.r)),
        line(seg(12, 12.2, 12, 16)),
        line(poly([(8.8, 21.5), (12, 16), (15.2, 21.5)], r=S.r)),
        dot(4.6, 2.6, 1.6), dot(19.4, 2.6, 1.6),
    ]


@icon("blessing-hand", CAT, "Blessing hand: a raised right hand with the index and middle fingers extended upward",
      tags=["blessing", "benediction", "sign of blessing", "priest", "christian", "icon", "hand"],
      aliases=["benediction"])
def _(S):
    tip = L(S, 1.2, 1.5)
    hand = union(rect(8.2, 3, 3, 10, tip), rect(11.4, 2.2, 3, 10, tip),
                 L(S, "M7 11H16.5V17.5C16.5 20 15 21.5 12.5 21.5H11C8.5 21.5 7 20 7 17.5Z",
                   "M8 11H15.5Q16.5 11 16.5 12V17.5C16.5 20 15 21.5 12.5 21.5H11C8.5 21.5 7 20 7 17.5V12Q7 11 8 11Z"),
                 "M7.5 15C5.8 14.2 4.8 12.6 4.6 10.8C4.5 9.7 5.6 9.2 6.3 10.1L7.6 12Z")
    return [
        shell(hand),
        detail(seg(11.3, 5, 11.3, 11)),
        detail("M14.4 12.2Q17 12.6 14.6 15.4"),
    ]


@icon("baptism-immersion", CAT, "Baptism by immersion: a person lowered backward into water, supported by another's arm",
      tags=["baptism", "immersion", "baptize", "baptise", "christening", "river baptism", "church", "sacrament"])
def _(S):
    wave = "M2 17.5Q4.5 15.5 7 17.5T12 17.5T17 17.5T22 17.5"
    wave_r = wave
    return [
        dot(7, 4.5, 2.2),
        line(seg(7, 8, 7, 15)),
        line(poly([(7, 9.5), (11, 12.5), (13.5, 13)], r=S.r)),
        dot(18.2, 9.4, 2.2),
        line(seg(16, 11.6, 11.5, 15)),
        line(wave if S.name == "line" else wave_r),
        line(L(S, "M5 21.2H10M14 21.2H19", "M5 21.2H10M14 21.2H19")),
    ]


@icon("anointing-oil-flask", CAT, "Anointing oil: a small horn-shaped flask tipped over with a drop of oil falling",
      tags=["anointing oil", "horn of oil", "chrism", "anoint", "oil", "blessing", "sacrament", "church"],
      aliases=["horn-of-oil"])
def _(S):
    horn = "M5.2 3.2C10 3.6 13.6 7.4 15.9 11.5L13.9 13.2C11.6 10.8 8.6 10 5.2 10.6A2.2 3.7 0 0 1 5.2 3.2Z"
    stopper = rot(rect(14.2, 11.5, 3.4, 2.2, L(S, 0, 0.8)), 45, 15.9, 12.6)
    drop = L(S, "M18.5 15.5L20.3 18.9A2 2 0 1 1 16.7 18.9Z", "M18.5 15.5C19.3 17 20.5 18 20.5 19.2A2 2 0 0 1 16.5 19.2C16.5 18 17.7 17 18.5 15.5Z")
    return [shell(horn), detail("M5.2 3.2A2.2 3.7 0 0 1 5.2 10.6"), shell(stopper), shell(drop)]


# ============================================================================ practices

@icon("walking-meditation", CAT, "Walking meditation: a figure stepping slowly, upright, with hands clasped in front and head lowered",
      tags=["walking meditation", "kinhin", "mindful walking", "mindfulness", "zen", "contemplation", "slow walk"],
      aliases=["kinhin"])
def _(S):
    return [
        dot(13.2, 4.6, 2.25),
        line(seg(11.5, 8.5, 11.5, 14.5)),
        line(poly([(11.5, 9.5), (13.4, 13), (15, 11.8)], r=S.r)),
        line(poly([(8.8, 21.5), (11.5, 14.5), (13.2, 18), (14.5, 21.5)], r=S.r)),
        line(seg(3, 21.5, 6, 21.5)), line(seg(17.5, 21.5, 21, 21.5)),
    ]


@icon("prayer-circle", CAT, "Prayer circle: people seen from above standing in a ring holding hands around a small flame",
      tags=["prayer circle", "prayer group", "vigil", "fellowship", "community", "holding hands", "worship"])
def _(S):
    R = 8
    parts = []
    n = 6
    for k in range(n):
        a = -90 + 360 / n * k
        parts.append(dot(*polar(12, 12, R, a), 2))
        parts.append(line(arc(12, 12, R, a + 21, a + 60 - 21)))
    flame = ("M12.4 7.6C14 9.2 14.8 10.8 14.8 12.4A2.8 2.8 0 0 1 9.2 12.4C9.2 11.4 9.6 10.6 10.2 10"
             "C10.4 10.8 10.8 11.2 11.3 11.3C11.2 10 11.6 8.8 12.4 7.6Z")
    parts.append(shell(flame))
    return parts


@icon("saying-grace", CAT, "Saying grace: two folded hands raised above a plate set between a fork and a knife",
      tags=["grace", "saying grace", "mealtime prayer", "blessing", "thanksgiving", "meal", "gratitude"])
def _(S):
    hands = L(S, "M12 1.8C10.8 2.6 10.3 4.2 10.2 6L8.6 8.6V10.4H15.4V8.6L13.8 6C13.7 4.2 13.2 2.6 12 1.8Z",
              "M12 1.8C10.8 2.6 10.3 4.2 10.2 6L8.9 8.1Q8.6 8.6 8.6 9.2V9.6Q8.6 10.4 9.4 10.4H14.6Q15.4 10.4 15.4 9.6V9.2Q15.4 8.6 15.1 8.1L13.8 6C13.7 4.2 13.2 2.6 12 1.8Z")
    return [
        shell(hands), detail(seg(12, 3.6, 12, 10.4)),
        shell(circle(12, 17, 4.6)),
        detail(circle(12, 17, 1.9)),
        line(seg(3.5, 16, 3.5, 21.5)), line(poly([(2.2, 11.5), (2.2, 14.8), (4.8, 14.8), (4.8, 11.5)], r=S.r * 0.4)),
        line(seg(20.5, 11.5, 20.5, 21.5)),
    ]


@icon("laying-on-of-hands", CAT, "Laying on of hands: a standing figure resting a hand on the bowed head of a kneeling figure",
      tags=["laying on of hands", "blessing", "ordination", "confirmation", "prayer", "healing", "church"])
def _(S):
    return [
        dot(6, 4.4, 2.25),
        line(seg(6, 8, 6, 14.5)),
        line(poly([(6, 9), (9.5, 9.5), (13.4, 10.2)], r=S.r)),
        line(poly([(3.4, 21.5), (6, 14.5), (8.6, 21.5)], r=S.r)),
        dot(14.6, 12.8, 2.1),
        line(poly([(16.6, 14.8), (18.8, 17.2), (15.6, 21.5), (21.2, 21.5)], r=S.r)),
    ]


@icon("fire-walking", CAT, "Fire walking: a barefoot figure walking across a bed of glowing coals with small flames",
      tags=["fire walking", "firewalk", "hot coals", "courage", "ritual", "trust", "festival"], aliases=["firewalk"])
def _(S):
    coals = "M2.5 20.8" + "".join(f"A1.9 1.9 0 0 1 {fmt(2.5 + 3.8 * (k + 1))} 20.8" for k in range(5))
    small = "M0 0C1.1 1 1.6 1.9 1.6 2.8A1.6 1.6 0 0 1 -1.6 2.8C-1.6 1.9 -1.1 1 0 0Z"

    def fl(x, y):
        return path_to_d(transform_path(P(small), (1, 0, 0, 1, x, y)))
    return [
        dot(12.8, 3.6, 2.2),
        line(poly([(8.2, 11.6), (10, 8.4), (12, 7.8), (13.8, 10.4), (16.2, 11.4)], r=S.r)),
        line(seg(12, 7.8, 10.8, 12.8)),
        line(poly([(7.4, 17.8), (10.8, 12.8), (13.6, 15), (14.4, 17.8)], r=S.r)),
        line(coals),
        mark(fl(4.2, 13.8)), mark(fl(19.4, 13.2)),
    ]


@icon("illuminated-manuscript", CAT, "Illuminated manuscript: an open book with a large decorated initial and a vine in the margin",
      tags=["illuminated manuscript", "book of hours", "medieval", "scripture", "calligraphy", "initial", "bible"])
def _(S):
    left = poly([(2.5, 4.5), (11.2, 6), (11.2, 20), (2.5, 18.5)], closed=True, r=S.r * 0.6)
    right = poly([(21.5, 4.5), (12.8, 6), (12.8, 20), (21.5, 18.5)], closed=True, r=S.r * 0.6)
    ini = minus(rect(4.4, 8, 5, 5, L(S, 0, 1)), "M5.9 11.6L6.9 9.4L7.9 11.6Z" if S.name == "line" else circle(6.9, 10.5, 0.9))
    return [
        shell(left), shell(right),
        mark(ini),
        detail(seg(4.6, 15.4, 9.2, 16)),
        detail(seg(14.8, 9.4, 19.4, 8.6)), detail(seg(14.8, 12.4, 19.4, 11.6)), detail(seg(14.8, 15.4, 17.4, 15)),
    ]


@icon("cremation-urn", CAT, "Cremation urn: a tall lidded urn on a narrow foot with a small dove on its front",
      tags=["urn", "cremation", "ashes", "funeral", "memorial", "remembrance", "burial", "dove"],
      aliases=["funeral-urn"])
def _(S):
    body = L(S, "M9 8H15C17.8 10 18.2 13.4 17.4 16C16.8 17.8 15.6 18.6 14.6 19H9.4C8.4 18.6 7.2 17.8 6.6 16C5.8 13.4 6.2 10 9 8Z",
             "M9.8 8H14.2Q15 8 15.6 8.5C17.8 10.6 18.1 13.6 17.4 16C16.8 17.8 15.6 18.6 14.6 19H9.4C8.4 18.6 7.2 17.8 6.6 16C5.9 13.6 6.2 10.6 8.4 8.5Q9 8 9.8 8Z")
    dove = "M9.4 13.2C10.2 12.5 11.3 12.5 11.9 13.2L14.6 11.4L13.9 14.2C13.5 15.3 12.4 15.9 11 15.7L9.4 16.2L10.2 14.8C9.8 14.4 9.5 13.8 9.4 13.2Z"
    return [
        dot(12, 3, 1.3),
        shell(rect(8.4, 5, 7.2, 1.6, L(S, 0, 0.8))),
        shell(body),
        mark(dove),
        shell(poly([(9.8, 19.8), (14.2, 19.8), (15.4, 21.5), (8.6, 21.5)], closed=True, r=S.r * 0.3)),
    ]
