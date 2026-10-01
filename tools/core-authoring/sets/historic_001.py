"""TypeIcon Core: historic (batch historic_001).

Medieval and ancient armour, shields, weapons, monuments, heraldry and standards. Helmets in side view
face left. Heraldic shields share one heater outline; charges are solid in Line and Rounded and knocked out
of the solid shield in Filled.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, rotation, transform_path  # noqa: F401

CAT = "historic"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def inter(a, b):
    return path_to_d(I(P(a), P(b)))


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def flip(d):
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def inset(d, w):
    """Region d shrunk by w px."""
    return path_to_d(D(P(d), ST(d, 2 * w, "butt", "miter")))


def mark(d):
    """Small solid region: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def rotp(pts, deg, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rseg(x1, y1, x2, y2, deg, cx=12.0, cy=12.0):
    (a, b), (c, d) = rotp([(x1, y1), (x2, y2)], deg, cx, cy)
    return seg(a, b, c, d)


def rpoly(pts, S, k=1.0):
    return poly(pts, closed=True, r=S.r * k)


# ============================================================================ helmets

@icon("bascinet", CAT, "Side view of a medieval helmet with a pointed crown and a beaked visor",
      tags=["helmet", "hounskull", "pig face", "knight", "medieval", "armour"], aliases=["pig-faced-bascinet"])
def _(S):
    skull = ("M5 19.5V13C5 8.5 8 4.5 12.5 2.5C17 4.5 19.5 8.5 19.5 13V19.5Z" if S.name == "line" else
             "M6.5 19.5Q5 19.5 5 18V13C5 8.5 8 4.8 11.6 2.9Q12.5 2.5 13.4 2.9C17 4.8 19.5 8.5 19.5 13V18Q19.5 19.5 18 19.5Z")
    snout = ("M9 7C6 8.5 3.5 11 2 13.5C3.5 16 6 18 9 19.5Z" if S.name == "line" else
             "M9 7C6.2 8.4 4 10.4 2.6 12.6Q2.1 13.5 2.7 14.3C4.1 16.3 6.3 18 9 19.5Z")
    return [shell(union(skull, snout)), detail("M9 7C10.8 10 11.2 15 10.3 19.5"),
            detail(seg(3.8, 11.5, 9.5, 11.5)), dot(5.5, 14.8, 0.9), dot(8.2, 15.8, 0.9)]


@icon("sallet", CAT, "Side view of a rounded sallet helmet with a long neck tail and an eye slit",
      tags=["helmet", "medieval", "knight", "armour", "late gothic", "visor"])
def _(S):
    body = ("M4 14.5C3.5 8 7.5 4.5 12 4.5C16.5 4.5 19 7.5 19 11.5C19 14 19.5 15.8 21 17.5C16 18.5 10.5 17 4 14.5Z" if S.name == "line" else
            "M4 14C3.5 8 7.5 4.5 12 4.5C16.5 4.5 19 7.5 19 11.5C19 14 19.4 15.5 20.4 16.8Q20.8 17.5 20 17.6C15.5 18.3 10.2 16.8 4.6 14.8Q4 14.6 4 14Z")
    return [shell(body), detail(seg(3.8, 10.5, 10.5, 10.5))]


@icon("barbute", CAT, "Front view of a tall rounded barbute helmet with a T-shaped face opening",
      tags=["helmet", "barbuta", "italian helmet", "medieval", "knight", "armour"], aliases=["barbuta"])
def _(S):
    body = ("M5 20.5V10C5 5.5 8 3 12 3C16 3 19 5.5 19 10V20.5Z" if S.name == "line" else
            "M7 20.5Q5 20.5 5 18.5V10C5 5.5 8 3 12 3C16 3 19 5.5 19 10V18.5Q19 20.5 17 20.5Z")
    return [shell(body), detail(seg(7.5, 10.5, 16.5, 10.5)), detail(seg(12, 10.5, 12, 17.5))]


@icon("kettle-hat", CAT, "Side view of an open bowl helmet with a wide downturned brim",
      tags=["helmet", "chapel de fer", "war hat", "medieval", "infantry", "armour"], aliases=["chapel-de-fer"])
def _(S):
    body = ("M2 18C3 15 5 13.5 6.5 13.5C6.5 7.5 9 4 12 4C15 4 17.5 7.5 17.5 13.5C19 13.5 21 15 22 18"
            "C19 16.5 16 16 12 16C8 16 5 16.5 2 18Z")
    if S.name == "rounded":
        body = ("M2.6 17.4C3.6 15 5 13.5 6.5 13.5C6.5 7.5 9 4 12 4C15 4 17.5 7.5 17.5 13.5C19 13.5 20.4 15 21.4 17.4"
                "Q21.6 18.2 20.8 17.8C18.5 16.6 15.5 16 12 16C8.5 16 5.5 16.6 3.2 17.8Q2.4 18.2 2.6 17.4Z")
    return [shell(body), detail(seg(6.5, 13.5, 17.5, 13.5))]


@icon("morion-helmet", CAT, "Side view of a morion helmet with a tall comb and an upswept pointed brim",
      tags=["morion", "conquistador", "helmet", "renaissance", "comb", "armour"], aliases=["morion"])
def _(S):
    comb = "M8.5 10.5C8.5 6 10 2.5 12 2.5C14 2.5 15.5 6 15.5 10.5Z"
    dome = "M6.5 14C6.5 10 9 7.5 12 7.5C15 7.5 17.5 10 17.5 14Z"
    brim = ("M2 9C4 13 7 14.5 12 14.5C17 14.5 20 13 22 9C20.5 15 17 17.5 12 17.5C7 17.5 3.5 15 2 9Z" if S.name == "line" else
            "M2.3 9.6Q2.2 8.8 2.7 9.5C4.8 12.8 7.5 14.5 12 14.5C16.5 14.5 19.2 12.8 21.3 9.5Q21.8 8.8 21.7 9.6C20.5 15 17 17.5 12 17.5C7 17.5 3.5 15 2.3 9.6Z")
    return [shell(union(comb, dome, brim)), detail("M6.8 12C7.6 9.5 9.4 7.8 11 7.6"),
            detail("M13 7.6C14.6 7.8 16.4 9.5 17.2 12")]


@icon("corinthian-helmet", CAT, "Side view of an ancient Greek helmet with an almond eye hole and a tall crest",
      tags=["greek helmet", "hoplite", "spartan", "ancient greece", "crest", "bronze"], aliases=["greek-helmet"])
def _(S):
    body = ("M5 21V13.5C5 9.5 8 7.5 12 7.5C16 7.5 19 9.5 19 13V16.5C19 18 20 19.5 21.5 21Z" if S.name == "line" else
            "M6.5 21Q5 21 5 19.5V13.5C5 9.5 8 7.5 12 7.5C16 7.5 19 9.5 19 13V16.5C19 18 20 19.2 20.8 20.1Q21.4 21 20.3 21Z")
    crest = "M5.5 7.5C7 3.5 11 2 15 2.5C18.5 3 21 5.5 22 9.5C20 7.5 17 5.5 12 5.5C9 5.5 7 6.3 5.5 7.5Z"
    return [shell(body), shell(crest), detail("M6 12.8Q8 11.3 10.5 12.3Q8.5 14 6 12.8Z"), detail(seg(8.5, 15, 8.5, 21))]


@icon("roman-legionary-helmet", CAT, "Side view of a Roman legionary helmet with a brow ridge, cheek plate and neck guard",
      tags=["galea", "roman helmet", "legionary", "imperial gallic", "centurion", "ancient rome"], aliases=["galea"])
def _(S):
    body = ("M3 13H5C5 7.5 8 4.5 12.5 4.5C17 4.5 19.5 7.5 19.5 11.5L22 14.5V16H15.5V13Z" if S.name == "line" else
            "M3.8 13H5C5 7.5 8 4.5 12.5 4.5C17 4.5 19.5 7.5 19.5 11.5L21.6 14.1Q22 14.5 22 15V15Q22 16 21 16H16.5Q15.5 16 15.5 15V13Z")
    cheek = rpoly([(7, 15.5), (13, 15.5), (12.5, 21), (8.5, 21)], S, 0.6)
    return [shell(body), shell(cheek), dot(10, 17.8, 0.9)]


@icon("spangenhelm", CAT, "Front view of a conical spangenhelm built from riveted bands with a nose guard",
      tags=["helmet", "migration period", "early medieval", "frankish", "armour", "riveted"])
def _(S):
    dome = ("M4 13.5C4 8.5 7.5 5 12 2.5C16.5 5 20 8.5 20 13.5Z" if S.name == "line" else
            "M4 13.5C4 8.5 7.5 5 11.1 3Q12 2.5 12.9 3C16.5 5 20 8.5 20 13.5Z")
    band = rect(4, 13, 16, 3.5, min(S.R, 1.5))
    nasal = rpoly([(10.5, 16), (13.5, 16), (13, 20.5), (11, 20.5)], S, 0.5)
    return [shell(union(dome, band, nasal)), detail(seg(4, 13.25, 20, 13.25)),
            detail("M12 3.2C10.3 6 9.3 9.3 9 13.2"), detail("M12 3.2C13.7 6 14.7 9.3 15 13.2"),
            dot(6.8, 15.3, 0.8), dot(17.2, 15.3, 0.8)]


@icon("nasal-helm", CAT, "Front view of a plain pointed cone helmet with a nose bar",
      tags=["norman helmet", "nasal helmet", "conical helmet", "viking", "medieval", "armour"], aliases=["norman-helmet"])
def _(S):
    if S.name == "line":
        d = ("M4 16C4.5 10 7.5 5.5 12 2.5C16.5 5.5 19.5 10 20 16C17.5 14.3 15.5 13.8 13.5 14L13.2 21H10.8"
             "L10.5 14C8.5 13.8 6.5 14.3 4 16Z")
    else:
        d = ("M4.2 15C4.8 9.8 7.8 5.6 11.2 3Q12 2.5 12.8 3C16.2 5.6 19.2 9.8 19.8 15Q19.9 16 19 15.6"
             "C17 14.4 15.3 13.9 13.5 14L13.3 20Q13.2 21 12.2 21H11.8Q10.8 21 10.7 20L10.5 14C8.7 13.9 7 14.4 5 15.6Q4.1 16 4.2 15Z")
    return [shell(d)]


@icon("spectacle-helmet", CAT, "Front view of a Norse helmet with a spectacle guard around both eyes",
      tags=["viking helmet", "norse", "gjermundbu", "vendel", "spectacle guard", "armour"], aliases=["viking-helmet"])
def _(S):
    dome = "M4 13.5C4 7 7.5 3.5 12 3.5C16.5 3.5 20 7 20 13.5Z" if S.name == "line" else \
        "M5.5 13.5Q4 13.5 4 12C4.3 6.8 7.8 3.5 12 3.5C16.2 3.5 19.7 6.8 20 12Q20 13.5 18.5 13.5Z"
    return [shell(dome), shell(circle(8.25, 17, 2.75)), shell(circle(15.75, 17, 2.75)), line(seg(12, 13.5, 12, 21.5))]


@icon("frog-mouth-helm", CAT, "Side view of a jousting helm with a flat crown, jutting lower front and a sight gap",
      tags=["jousting helmet", "stechhelm", "tournament", "tilting helm", "medieval", "armour"], aliases=["stechhelm"])
def _(S):
    d = rpoly([(8.5, 3.5), (17, 3.5), (20.5, 7), (20.5, 21), (6.5, 21), (2.5, 11.5), (11, 10), (6.5, 8.5)], S, 0.6)
    return [shell(d), dot(16, 14, 1), dot(16, 17.5, 1)]


@icon("close-helmet", CAT, "Side view of a close helmet with a comb on top and a pointed visor with sight slits",
      tags=["armet", "knight helmet", "plate armour", "visor", "renaissance", "armour"])
def _(S):
    comb = "M8 7C9 2.5 15.5 2 18.5 6.5Z"
    skull = "M3.5 12L6.5 8C8 5.5 10 4.5 12.5 4.5C17 4.5 19.5 8 19.5 12.5V18.5L15.5 21H8L6 16.5Z"
    if S.name == "rounded":
        skull = ("M4.1 11.2L6.5 8C8 5.5 10 4.5 12.5 4.5C17 4.5 19.5 8 19.5 12.5V17.5Q19.5 18.5 18.6 19.1L16.4 20.5"
                 "Q15.6 21 14.6 21H9Q8 21 7.6 20.1L6.4 17.4Q6 16.5 5.3 15.8L4.2 14.7Q3.4 13.3 4.1 11.2Z")
    return [shell(union(comb, skull)), detail("M7 8.5C10.5 9.5 13 12.5 13 21"),
            detail(seg(5.3, 11, 10.2, 11)), detail(seg(6.3, 14, 11, 14))]


@icon("samurai-face-mask", CAT, "Front view of a samurai armour face mask with a stern mouth and a throat guard",
      tags=["menpo", "mempo", "samurai", "japanese armour", "face guard", "warrior"], aliases=["menpo"])
def _(S):
    mask = ("M3.5 5.5L9.5 7L10.5 3H13.5L14.5 7L20.5 5.5C20.5 11 16.5 15 12 15C7.5 15 3.5 11 3.5 5.5Z" if S.name == "line" else
            "M4.6 5.8L9 6.9Q9.6 7 9.8 6.4L10.2 4Q10.5 3 11.5 3H12.5Q13.5 3 13.8 4L14.2 6.4Q14.4 7 15 6.9L19.4 5.8Q20.5 5.5 20.5 6.6C20.3 11.5 16.4 15 12 15C7.6 15 3.7 11.5 3.5 6.6Q3.5 5.5 4.6 5.8Z")
    guard = rect(6, 18, 12, 3.5, min(S.R, 1.5))
    return [shell(mask), detail("M8 11.2L9.5 10.3H14.5L16 11.2"), shell(guard), detail(seg(10, 18, 10, 21.5)),
            detail(seg(14, 18, 14, 21.5))]


# ============================================================================ body armour

@icon("pauldron", CAT, "Side view of a curved shoulder guard of overlapping plates with a raised ridge",
      tags=["shoulder armour", "spaulder", "plate armour", "knight", "medieval", "armour"], aliases=["shoulder-guard"])
def _(S):
    cap = ("M3 13C3 7 7 3.5 12 3.5C17 3.5 21 7 21 13C18 11.5 15 11 12 11C9 11 6 11.5 3 13Z" if S.name == "line" else
           "M3.6 12.6C3.4 7 7.2 3.5 12 3.5C16.8 3.5 20.6 7 20.4 12.6Q20.3 13.3 19.6 13C17 11.6 14.5 11 12 11C9.5 11 7 11.6 4.4 13Q3.7 13.3 3.6 12.6Z")
    return [shell(cap), detail("M6.5 9C8 7 10 6 12 6"), line("M4.5 17C7 15.5 9.5 14.8 12 14.8C14.5 14.8 17 15.5 19.5 17"),
            line("M6.5 20.5C8.3 19.3 10.2 18.8 12 18.8C13.8 18.8 15.7 19.3 17.5 20.5")]


@icon("gorget", CAT, "Front view of a crescent-shaped metal throat plate with a rivet at each tip",
      tags=["throat armour", "neck guard", "collar", "plate armour", "officer", "armour"], aliases=["neck-guard"])
def _(S):
    d = ("M3 5.5C3 14 7 19.5 12 19.5C17 19.5 21 14 21 5.5H16.5C16.5 10.5 14.5 13.5 12 13.5C9.5 13.5 7.5 10.5 7.5 5.5Z"
         if S.name == "line" else
         "M4.5 5.5Q3 5.5 3 7C3.3 14.5 7.2 19.5 12 19.5C16.8 19.5 20.7 14.5 21 7Q21 5.5 19.5 5.5H18Q16.5 5.5 16.5 7"
         "C16.3 11 14.3 13.5 12 13.5C9.7 13.5 7.7 11 7.5 7Q7.5 5.5 6 5.5Z")
    return [shell(d), dot(5.3, 8.2, 1), dot(18.7, 8.2, 1)]


@icon("sabaton", CAT, "Side view of an armoured foot of overlapping plates ending in a pointed toe",
      tags=["armoured shoe", "solleret", "foot armour", "plate armour", "knight", "armour"], aliases=["solleret"])
def _(S):
    d = rpoly([(13.5, 6), (20, 6), (21, 19.5), (3.2, 19.5), (7, 16.5), (10.5, 13.5)], S, 0.8)
    return [shell(d), detail("M10.5 13.5Q13.5 16 13.5 19.5"), detail("M13.5 9.5Q17 13 17 19.5"), detail(seg(13.5, 9.5, 20.2, 9.5))]


@icon("mail-coif", CAT, "Front view of a chainmail hood over head and shoulders with an oval face opening",
      tags=["chainmail hood", "chain mail", "coif", "hauberk", "medieval", "armour"], aliases=["chainmail-hood"])
def _(S):
    d = ("M12 2.5C16.5 2.5 18.5 6 18.5 10.5V14C19 15.5 21 16.5 21.5 21H2.5C3 16.5 5 15.5 5.5 14V10.5C5.5 6 7.5 2.5 12 2.5Z"
         if S.name == "line" else
         "M12 2.5C16.5 2.5 18.5 6 18.5 10.5V14C19 15.5 21 16.5 21.4 19.9Q21.5 21 20.4 21H3.6Q2.5 21 2.6 19.9C3 16.5 5 15.5 5.5 14V10.5C5.5 6 7.5 2.5 12 2.5Z")
    return [shell(d), detail(ellipse(12, 10.5, 3, 4)), dot(6, 18.5, 0.9), dot(9, 18.5, 0.9), dot(12, 18.5, 0.9),
            dot(15, 18.5, 0.9), dot(18, 18.5, 0.9)]


def _vest(S):
    return rpoly([(7.5, 2.5), (4, 4.5), (4.5, 9), (4, 21.5), (20, 21.5), (19.5, 9), (20, 4.5), (16.5, 2.5),
                  (14.5, 5), (9.5, 5)], S, 0.8)


@icon("scale-armor", CAT, "Front view of sleeveless torso armour covered in rows of overlapping scales",
      tags=["scale armour", "lamellar", "cuirass", "ancient armour", "scales", "armour"], aliases=["scale-armour"])
def _(S):
    rows = []
    for y, xs in ((9, (6, 10, 14)), (13, (8, 12)), (17, (6, 10, 14))):
        for x in xs:
            rows.append(detail(f"M{fmt(x)} {y}A2 2 0 0 0 {fmt(x + 4)} {y}"))
    return [shell(_vest(S))] + rows


@icon("segmented-armor", CAT, "Front view of Roman torso armour of curved horizontal bands with shoulder plates",
      tags=["lorica segmentata", "roman armour", "legionary", "banded armour", "cuirass", "armour"],
      aliases=["lorica-segmentata", "segmented-armour"])
def _(S):
    return [shell(_vest(S)), detail("M4.3 11.5Q12 13 19.7 11.5"), detail("M4.3 15Q12 16.5 19.7 15"),
            detail("M4.2 18.5Q12 20 19.8 18.5"), detail("M4.3 8.3Q6.5 7 8.5 5.5"), detail("M19.7 8.3Q17.5 7 15.5 5.5")]


@icon("gambeson", CAT, "Front view of a quilted padded jacket with stitched channels and a high collar",
      tags=["aketon", "padded jacket", "arming doublet", "quilted armour", "medieval", "armour"], aliases=["aketon"])
def _(S):
    body = rpoly([(8.5, 4.5), (3, 7), (2, 17.5), (5, 17.5), (6, 11), (6, 21.5), (18, 21.5), (18, 11), (19, 17.5),
                  (22, 17.5), (21, 7), (15.5, 4.5)], S, 0.8)
    collar = rect(8.5, 2, 7, 3.5, min(S.R, 1))
    return [shell(body), shell(collar), detail(seg(9.5, 8, 9.5, 21.5)), detail(seg(14.5, 8, 14.5, 21.5))]


@icon("kite-shield", CAT, "Front view of a tall kite shield rounded at the top and tapering to a point",
      tags=["norman shield", "medieval shield", "knight", "heater", "defence", "armour"], aliases=["norman-shield"])
def _(S):
    if S.name == "line":
        d = "M4.5 4Q12 1.5 19.5 4V8.5C19.5 13 16 17.5 12 22C8 17.5 4.5 13 4.5 8.5Z"
    else:
        d = "M5.5 3.7Q12 1.5 18.5 3.7Q19.5 4 19.5 5V8.5C19.5 13 16 17.3 12.7 21.2Q12 22 11.3 21.2C8 17.3 4.5 13 4.5 8.5V5Q4.5 4 5.5 3.7Z"
    return [shell(d), detail(circle(12, 9.5, 2))]


@icon("buckler", CAT, "Front view of a small round fist shield with a domed boss and a riveted rim",
      tags=["round shield", "fist shield", "sword and buckler", "medieval", "fencing", "defence"])
def _(S):
    rivets = []
    for k in range(8):
        a = math.radians(k * 45 + 22.5)
        x, y = 12 + 6 * math.cos(a), 12 + 6 * math.sin(a)
        rivets.append(dot(x, y, 0.85) if S.name == "rounded" else mark(rect(x - 0.8, y - 0.8, 1.6, 1.6)))
    return [shell(circle(12, 12, 9)), detail(circle(12, 12, 2.5))] + rivets


@icon("roman-scutum", CAT, "Front view of a tall rectangular Roman shield with a round boss and wing lines",
      tags=["scutum", "roman shield", "legionary", "ancient rome", "testudo", "defence"], aliases=["scutum"])
def _(S):
    return [shell(rect(5, 2, 14, 20, S.R * 0.75)), detail(circle(12, 12, 2.3)), detail("M9 10L7.5 5.5"),
            detail("M15 10L16.5 5.5"), detail("M9 14L7.5 18.5"), detail("M15 14L16.5 18.5")]


@icon("pavise", CAT, "Front view of a tall standing pavise shield with a central ridge and a rounded top",
      tags=["pavise shield", "crossbowman", "siege shield", "mantlet", "medieval", "defence"], aliases=["pavis"])
def _(S):
    d = ("M3.5 21.5V6Q10 1 16.5 6V21.5Z" if S.name == "line" else "M5.5 21.5Q3.5 21.5 3.5 19.5V6.5Q10 1.2 16.5 6.5V19.5Q16.5 21.5 14.5 21.5Z")
    return [shell(d), detail(seg(10, 3.5, 10, 21.5)), line(seg(17.5, 12, 21, 21.5))]


@icon("hoplite-shield", CAT, "Front view of a large round Greek shield with a wide rim and a central emblem",
      tags=["aspis", "hoplon", "greek shield", "spartan", "hoplite", "defence"], aliases=["aspis"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(circle(12, 12, 6)),
            detail(poly([(9.2, 14.8), (12, 8.6), (14.8, 14.8)], r=S.r * 0.7))]


@icon("viking-round-shield", CAT, "Front view of a round wooden plank shield with a domed iron boss",
      tags=["viking shield", "norse shield", "round shield", "planks", "boss", "defence"], aliases=["norse-shield"])
def _(S):
    c = 12
    boss = dot(12, 12, 2.6) if S.name == "rounded" else mark(regular(12, 12, 2.9, 8, -22.5) and poly(regular(12, 12, 2.9, 8, -22.5), closed=True))
    return [shell(circle(12, 12, 9)), boss, detail(seg(7.5, 4.5, 7.5, 19.5)), detail(seg(16.5, 4.5, 16.5, 19.5)),
            detail(seg(c, 3, c, 7.8)), detail(seg(c, 16.2, c, 21))]


# ============================================================================ horses

@icon("horse-chanfron", CAT, "Side view of a horse head covered by an armoured face plate with a spike",
      tags=["chanfron", "chamfron", "barding", "horse armour", "warhorse", "knight"], aliases=["chamfron"])
def _(S):
    ear = "L15.5 2.5L17.5 6.5" if S.name == "line" else "L15.1 3.2Q15.5 2.5 15.9 3.2L17.5 6.5"
    head = ("M12.5 5.5" + ear + "C20 9.5 21 14.5 21 21.5H12C12 19 12 17.5 12.5 16.5C10.5 17.8 8.5 18.5 6.5 18.5"
            "C4.5 18.5 3.3 17.3 3.5 15.7C3.7 14.3 4.5 13.3 5.5 12.3Z")
    spike = poly([(8, 7.5), (5.5, 6.2), (7, 9.2)], closed=True)
    return [shell(head), detail("M6.2 13.3L9.2 16.5M12.2 6.5L15.5 10"), solid(spike), dot(13, 11, 1.2)]


@icon("caparisoned-horse", CAT, "Side view of a horse draped to the ankles in a long cloth with a shield on its flank",
      tags=["caparison", "barding", "tournament", "jousting", "warhorse", "knight"], aliases=["caparison"])
def _(S):
    body = rpoly([(2.5, 10), (5.5, 4.5), (6.5, 2.5), (8, 5), (11, 8.5), (19, 8.5), (21.5, 11), (21.5, 18.5),
                  (6.5, 18.5), (6.5, 12), (4.5, 11.5)], S, 0.8)
    legs = [line(seg(x, 18.5, x, 21.5)) for x in (8.5, 12, 15.5, 19.5)]
    crest = ("M13.5 11H17.5V13.5C17.5 15 16 16 15.5 16.3C15 16 13.5 15 13.5 13.5Z" if S.name == "line" else
             "M14 11H17Q17.5 11 17.5 11.5V13.5C17.5 15 16 16 15.5 16.3C15 16 13.5 15 13.5 13.5V11.5Q13.5 11 14 11Z")
    return [shell(body), detail(crest), dot(5.8, 7.3, 0.9)] + legs


# ============================================================================ weapons

@icon("halberd", CAT, "Tall pole arm with an axe blade, a back hook and a spear point",
      tags=["pole arm", "polearm", "pike", "swiss guard", "medieval weapon", "axe"], aliases=["polearm"])
def _(S):
    blade = ("M10.5 5.5C7 5.5 4.5 7 3.5 9.5C4.5 12 7 13.5 10.5 13.5Z" if S.name == "line" else
             "M10.5 5.5C7.2 5.5 5 6.8 3.9 8.8Q3.5 9.5 3.9 10.2C5 12.2 7.2 13.5 10.5 13.5Z")
    hook = rpoly([(13.5, 7.5), (19, 11), (13.5, 10.5)], S, 0.4)
    tip = rpoly([(12, 2.5), (13.8, 5.5), (10.2, 5.5)], S, 0.4)
    return [shell(blade), shell(hook), shell(tip), line(seg(12, 5.5, 12, 22))]


@icon("ballista", CAT, "Side view of a ballista: a giant crossbow on a wooden stand with a bolt",
      tags=["siege engine", "crossbow", "artillery", "roman", "scorpion", "siege weapon"], aliases=["scorpio"])
def _(S):
    return [line("M8 3.5Q4.5 11 8 18.5"), line(poly([(8, 3.5), (16, 10)], r=0)), line(poly([(8, 18.5), (16, 12)])),
            shell(rect(3, 10, 18, 2.5, min(S.R, 1))), line(seg(14, 12.5, 11, 21)), line(seg(14, 12.5, 17.5, 21))]


@icon("scabbard", CAT, "Sword in its scabbard with a metal throat and tip, hilt showing at the top",
      tags=["sheath", "sword", "sheathed sword", "knight", "medieval", "blade"], aliases=["sword-sheath"])
def _(S):
    body = rpoly([(10, 9), (14, 9), (14, 19.5), (12, 22), (10, 19.5)], S, 0.5)
    parts = [line(seg(8, 7, 16, 7)), line(seg(12, 2.5, 12, 5)), shell(body), detail(seg(10, 12, 14, 12)),
             detail(seg(10, 17.5, 14, 17.5))]
    return [Part(p.kind, rot(p.d, 45) if p.kind != "line" else _rline(p.d), p.attrs) for p in parts]


def _rline(d):
    """Rotate a two-point 'M x y L x y' segment by 45 degrees about the centre."""
    a, b = d[1:].split("L")
    x1, y1 = map(float, a.split())
    x2, y2 = map(float, b.split())
    return rseg(x1, y1, x2, y2, 45)


@icon("powder-horn", CAT, "Curved horn flask for gunpowder with a stopper, a capped end and a strap",
      tags=["gunpowder", "musket", "flintlock", "frontier", "flask", "horn"])
def _(S):
    horn = "M19.5 9C14 10 8.5 13 4.5 17L5.5 18.5C10 16.5 15 15.5 20 15.5Z"
    if S.name == "rounded":
        horn = "M18.5 9.2C13.5 10.3 8.5 13 5 16.6Q4.4 17.2 4.9 17.8L5.2 18.2Q5.6 18.7 6.3 18.4C10.5 16.6 15 15.6 19.2 15.5Q20 15.5 20 14.7L19.6 9.9Q19.5 9 18.5 9.2Z"
    return [shell(horn), detail(seg(17, 9.5, 17.3, 15.6)), line(seg(4.5, 18, 2.8, 19.5)),
            line("M7 14.5C8 8.5 12 5.5 17.5 9.3")]


# ============================================================================ buildings and monuments

@icon("castle-ruin", CAT, "Crumbling castle tower with a broken top, an arched window and fallen stones",
      tags=["ruin", "ruins", "castle", "abandoned", "medieval", "heritage"], aliases=["ruined-castle"])
def _(S):
    tower = rpoly([(4, 20.5), (4, 5), (6.5, 3), (8.5, 6), (11, 2.5), (13, 7), (15.5, 5.5), (15.5, 20.5)], S, 0.4)
    win = "M8 13V11.2A1.75 1.75 0 0 1 11.5 11.2V13"
    return [shell(tower), detail(win), mark(rect(18, 17.5, 3.5, 3, min(S.R, 0.8))), mark(rect(18.5, 13, 2.5, 2.5, min(S.R, 0.8))),
            line(seg(2, 21.5 - 0.5 + 0.5, 2, 21.5)) if False else line(seg(2.5, 21.5, 21.5, 21.5))]


@icon("broch", CAT, "Tall round drystone tower whose walls curve inward, with a small doorway",
      tags=["iron age tower", "scotland", "drystone", "round tower", "prehistoric", "fort"])
def _(S):
    d = ("M4.5 21.5C6.5 15.5 7 9 6 2.5H18C17 9 17.5 15.5 19.5 21.5Z" if S.name == "line" else
         "M6 21.5Q4.4 21.5 4.9 20.1C6.6 14.7 7 8.9 6.2 3.6Q6 2.5 7.1 2.5H16.9Q18 2.5 17.8 3.6C17 8.9 17.4 14.7 19.1 20.1Q19.6 21.5 18 21.5Z")
    door = "M10.5 21.5V18.5A1.5 1.5 0 0 1 13.5 18.5V21.5"
    return [shell(d), detail(door), detail(seg(7.8, 7, 11, 7)), detail(seg(13, 11, 16.2, 11)), detail(seg(8.2, 14.5, 11.2, 14.5))]


@icon("crannog", CAT, "Round thatched hut on a stilted timber platform above water with a walkway to shore",
      tags=["lake dwelling", "stilt hut", "iron age", "loch", "ireland", "scotland"], aliases=["lake-dwelling"])
def _(S):
    roof = rpoly([(3.5, 8.5), (9.5, 2.5), (15.5, 8.5)], S, 0.8)
    return [shell(roof), shell(rect(5.5, 8.5, 8, 4, 0)), line(seg(2.5, 14.5, 16.5, 14.5)),
            line(seg(5, 14.5, 5, 21.5)), line(seg(14, 14.5, 14, 21.5)), line(poly([(16.5, 14.5), (21.5, 17.5)])),
            line("M2.5 19Q4 17.8 5.5 19T8.5 19T11.5 19T14.5 19T17.5 19")]


@icon("bartizan", CAT, "Small round turret with a conical roof overhanging the corner of a stone wall on corbels",
      tags=["turret", "corner tower", "echauguette", "castle", "watch turret", "fortification"], aliases=["echauguette"])
def _(S):
    wall = rpoly([(2.5, 21.5), (2.5, 14.5), (21.5, 14.5), (21.5, 21.5)], S, 0.5)
    turret = rpoly([(8, 8), (16, 8), (16, 12), (14.5, 14.5), (9.5, 14.5), (8, 12)], S, 0.5)
    roof = rpoly([(7, 8), (12, 2), (17, 8)], S, 0.6)
    return [shell(union(wall, turret)), shell(roof), detail(seg(12, 9.8, 12, 12.2)), detail(seg(12, 16.5, 12, 21.5)),
            detail(seg(9.5, 14.5, 14.5, 14.5))]


@icon("great-wall", CAT, "Crenellated wall winding over rolling hills with a square watchtower on the ridge",
      tags=["ancient wall", "china", "fortification", "defensive wall", "rampart", "landmark"], aliases=["long-wall"])
def _(S):
    tower = rpoly([(9, 4), (10.5, 4), (10.5, 5.5), (12, 5.5), (12, 4), (13.5, 4), (13.5, 5.5), (15, 5.5), (15, 4),
                   (16.5, 4), (16.5, 11), (9, 11)], S, 0.3)
    left = rpoly([(2, 14.5), (9, 10), (9, 13.5), (2, 18)], S, 0.4)
    right = rpoly([(16.5, 10), (22, 13.5), (22, 17), (16.5, 13.5)], S, 0.4)
    return [shell(union(tower, left, right)), line("M2 21.5C6 19 9 18 12.5 19.5C15.5 21 18.5 20.5 22 19.5"),
            detail(seg(12.75, 11, 12.75, 8.5))]


@icon("beehive-hut", CAT, "Domed hut of stacked flat stones with a low doorway",
      tags=["clochan", "corbelled hut", "stone hut", "ireland", "monastic", "drystone"], aliases=["clochan"])
def _(S):
    d = "M3 20.5C3 12 6.5 3.5 12 3.5C17.5 3.5 21 12 21 20.5Z" if S.name == "line" else \
        "M4.5 20.5Q3 20.5 3 19C3.3 11.5 6.8 3.5 12 3.5C17.2 3.5 20.7 11.5 21 19Q21 20.5 19.5 20.5Z"
    return [shell(d), detail("M10 20.5V17.5A2 2 0 0 1 14 17.5V20.5"), detail("M6.3 9.5H17.7"), detail("M4.5 14H19.5"),
            detail(seg(3.6, 17.5, 7.5, 17.5)), detail(seg(16.5, 17.5, 20.4, 17.5))]


@icon("keyhole-tomb", CAT, "Top view of a keyhole-shaped burial mound ringed by a moat",
      tags=["kofun", "burial mound", "japan", "tumulus", "ancient tomb", "archaeology"], aliases=["kofun"])
def _(S):
    def key(g, rr):
        c = circle(12, 8.5, 4 + g)
        b = poly([(12 - 2.5 - g * 0.9, 10), (12 + 2.5 + g * 0.9, 10), (12 + 5.5 + g, 18.5 + g * 0.6), (12 - 5.5 - g, 18.5 + g * 0.6)], closed=True, r=rr)
        return union(c, b)
    return [shell(key(2.5, S.r)), detail(key(0, S.r * 0.6))]


@icon("trilithon", CAT, "Two tall standing stones topped by a flat lintel stone forming a gateway",
      tags=["stonehenge", "megalith", "standing stones", "neolithic", "prehistoric", "monument"], aliases=["megalith-gate"])
def _(S):
    left = rpoly([(4, 21), (4.5, 11), (5.5, 10), (9.5, 10), (10, 21)], S, 0.8)
    right = rpoly([(14, 21), (14.5, 10.5), (15.5, 10), (19, 10), (20, 21)], S, 0.8)
    lintel = rpoly([(3, 4), (21, 3.5), (21, 7), (3, 7.5)], S, 0.8)
    return [shell(left), shell(right), shell(lintel), line(seg(2, 21.5, 22, 21.5)) if False else line(seg(2, 21, 22, 21))]


@icon("roman-road", CAT, "Straight road of fitted paving stones running toward the horizon",
      tags=["via", "roman road", "paved road", "cobbles", "ancient rome", "causeway"], aliases=["via"])
def _(S):
    road = rpoly([(2.5, 21.5), (9.5, 2.5), (14.5, 2.5), (21.5, 21.5)], S, 0.5)
    return [shell(road), detail(seg(6.8, 9.5, 17.2, 9.5)), detail(seg(4.9, 15, 19.1, 15)),
            detail(seg(12, 2.5, 12, 9.5)), detail(seg(9.5, 9.5, 9, 15)), detail(seg(14.5, 9.5, 15, 15)),
            detail(seg(12, 15, 12, 21.5))]


@icon("roman-milestone", CAT, "Short Roman stone column on a square base carved with lines of text",
      tags=["milestone", "miliarium", "roman", "mile marker", "inscription", "ancient road"], aliases=["miliarium"])
def _(S):
    col = ("M7 4.5Q12 2.5 17 4.5V16.5H7Z" if S.name == "line" else "M7 5.5Q7 4.5 8 4.2Q12 2.8 16 4.2Q17 4.5 17 5.5V16.5H7Z")
    base = rect(4.5, 16.5, 15, 5, min(S.R, 1.5))
    return [shell(union(col, base)), detail(seg(9.5, 7.5, 14.5, 7.5)), detail(seg(9.5, 10.5, 14.5, 10.5)),
            detail(seg(10.5, 13.5, 13.5, 13.5)), detail(seg(4.5, 16.5, 19.5, 16.5))]


@icon("bull-capital-column", CAT, "Fluted column topped by a capital of two kneeling bulls facing away from each other",
      tags=["persepolis", "apadana", "persian column", "bull capital", "achaemenid", "ancient persia"], aliases=["persian-column"])
def _(S):
    capital = rpoly([(9, 4.5), (4.5, 4.5), (2.5, 7), (4.5, 8.5), (6, 8.5), (6, 10.5), (18, 10.5), (18, 8.5), (19.5, 8.5),
                     (21.5, 7), (19.5, 4.5), (15, 4.5), (15, 6), (9, 6)], S, 0.5)
    return [shell(capital), line("M5 4.5Q4.5 2.5 6.5 2"), line("M19 4.5Q19.5 2.5 17.5 2"),
            shell(rect(9, 12.5, 6, 7, 0)), shell(rect(7, 19.5, 10, 2, min(S.R, 1))), detail(seg(12, 12.5, 12, 19.5))]


@icon("ancient-lighthouse", CAT, "Tall tiered ancient lighthouse with a square base, an octagonal middle and a fire on top",
      tags=["pharos", "lighthouse of alexandria", "wonder of the world", "beacon", "ancient egypt", "tower"],
      aliases=["pharos"])
def _(S):
    base = rect(5.5, 14.5, 13, 7, min(S.R, 1))
    mid = poly([(8, 14.5), (8.5, 9), (15.5, 9), (16, 14.5)], closed=True)
    top = rect(9.5, 6.5, 5, 2.5, 0)
    flame = ("M12 1.8C13.2 3 13.5 4 12.8 5.2H11.2C10.5 4 10.8 3 12 1.8Z")
    return [shell(union(base, mid, top)), detail(seg(8, 14.5, 16, 14.5)), detail(seg(8.5, 9, 15.5, 9)),
            detail("M10.5 21.5V19.5A1.5 1.5 0 0 1 13.5 19.5V21.5"), solid(flame)]


@icon("dol-hareubang", CAT, "Carved stone guardian statue with a brimmed cap, round eyes, a big nose and hands on its belly",
      tags=["harubang", "jeju", "stone grandfather", "korea", "guardian statue", "basalt"], aliases=["harubang"])
def _(S):
    cap = ("M8.5 6.5C8.5 3.8 10 2.5 12 2.5C14 2.5 15.5 3.8 15.5 6.5H18.5V8H5.5V6.5Z" if S.name == "line" else
           "M8.5 6.5C8.5 3.8 10 2.5 12 2.5C14 2.5 15.5 3.8 15.5 6.5H17.8Q18.5 6.5 18.5 7.2Q18.5 8 17.8 8H6.2Q5.5 8 5.5 7.2Q5.5 6.5 6.2 6.5Z")
    body = ("M7 10H17C17.5 14 18 18 17.5 21.5H6.5C6 18 6.5 14 7 10Z" if S.name == "line" else
            "M8 10H16Q17 10 17.1 11C17.5 14.5 17.9 18 17.6 20.5Q17.5 21.5 16.5 21.5H7.5Q6.5 21.5 6.4 20.5C6.1 18 6.5 14.5 6.9 11Q7 10 8 10Z")
    return [shell(cap), shell(body), dot(9.6, 12.3, 1.1), dot(14.4, 12.3, 1.1), detail(seg(12, 12.5, 12, 15)),
            detail(seg(8.5, 17.3, 13, 17.3)), detail(seg(11, 19.5, 15.5, 19.5))]


@icon("chalk-hill-figure", CAT, "Rounded hill with a stylised horse outline cut into its slope",
      tags=["white horse", "hill figure", "geoglyph", "uffington", "chalk horse", "prehistoric"], aliases=["white-horse"])
def _(S):
    hill = "M2 21.5C3 12 7 6.5 12 6.5C17 6.5 21 12 22 21.5Z" if S.name == "line" else \
        "M3.5 21.5Q2 21.5 2.2 20C3.3 11.7 7.2 6.5 12 6.5C16.8 6.5 20.7 11.7 21.8 20Q22 21.5 20.5 21.5Z"
    horse = [detail("M5.5 15L8 13.5H15L17.5 11"), detail(seg(8.5, 13.5, 7, 18)), detail(seg(14, 13.5, 15.5, 18))]
    return [shell(hill)] + horse


# ============================================================================ heraldry

_HS_LINE = "M4 3H20V10.5C20 15.5 16.8 19.2 12 21.5C7.2 19.2 4 15.5 4 10.5Z"
_HS_ROUND = ("M6.5 3H17.5Q20 3 20 5.5V10.5C20 15.5 16.8 19.2 12.9 21.1Q12 21.5 11.1 21.1C7.2 19.2 4 15.5 4 10.5V5.5"
             "Q4 3 6.5 3Z")


def _hs(S):
    return _HS_LINE if S.name == "line" else _HS_ROUND


def _field(S):
    """Inside of the heater shield, reaching slightly under its stroke so charges join the outline."""
    return inset(_hs(S), 0.8)


def _charge(S, *regions):
    """Shield outline with a solid charge clipped to the field."""
    return [shell(_hs(S)), mark(inter(_field(S), union(*regions)))]


def _band(d, w):
    return path_to_d(ST(d, w, "butt", "miter", 8))


@icon("heraldic-bend", CAT, "Heater shield crossed by one broad diagonal band",
      tags=["bend", "coat of arms", "heraldry", "ordinary", "diagonal band", "escutcheon"])
def _(S):
    return _charge(S, _band(seg(0, -1, 24, 23), 4.5))


@icon("heraldic-chevron", CAT, "Heater shield with a broad inverted V band rising to a peak",
      tags=["chevron", "coat of arms", "heraldry", "ordinary", "rafter", "escutcheon"])
def _(S):
    return _charge(S, _band(poly([(1, 19), (12, 8), (23, 19)]), 4.5))


@icon("heraldic-saltire", CAT, "Heater shield with a broad diagonal X cross",
      tags=["saltire", "coat of arms", "heraldry", "st andrew's cross", "x cross", "ordinary"])
def _(S):
    return _charge(S, _band(seg(0, -1, 24, 23), 3.5), _band(seg(24, -1, 0, 23), 3.5))


@icon("heraldic-pale", CAT, "Heater shield with one broad vertical band down the center",
      tags=["pale", "coat of arms", "heraldry", "ordinary", "vertical band", "escutcheon"])
def _(S):
    return _charge(S, rect(9.5, 0, 5, 24))


@icon("heraldic-fess", CAT, "Heater shield with one broad horizontal band across the middle",
      tags=["fess", "fesse", "coat of arms", "heraldry", "ordinary", "horizontal band"])
def _(S):
    return _charge(S, rect(0, 8.5, 24, 4.5))


@icon("heraldic-per-pale", CAT, "Heater shield split down the middle with the left half filled",
      tags=["per pale", "party per pale", "coat of arms", "heraldry", "division", "half"])
def _(S):
    return _charge(S, rect(0, 0, 12, 24))


@icon("heraldic-chief", CAT, "Heater shield with its top third filled",
      tags=["chief", "coat of arms", "heraldry", "ordinary", "top band", "escutcheon"])
def _(S):
    return _charge(S, rect(0, 0, 24, 8.5))


@icon("heraldic-pall", CAT, "Heater shield with a Y-shaped band reaching the top corners and the base",
      tags=["pall", "pairle", "coat of arms", "heraldry", "y cross", "ordinary"], aliases=["pairle"])
def _(S):
    return _charge(S, _band(poly([(1, 0), (12, 11), (23, 0)]), 3.5), rect(10.25, 10, 3.5, 14))


@icon("heraldic-bordure", CAT, "Heater shield with a band running around the inside of its edge",
      tags=["bordure", "border", "coat of arms", "heraldry", "edge band", "escutcheon"])
def _(S):
    return [shell(_hs(S)), detail(path_to_d(P(inset(_hs(S), 4))))]


@icon("heraldic-chequy", CAT, "Heater shield filled with a checkerboard of small squares",
      tags=["chequy", "checky", "checkered", "coat of arms", "heraldry", "checkerboard"], aliases=["checky"])
def _(S):
    sq = [rect(4 + 4 * i, 3 + 4 * j, 4, 4) for i in range(4) for j in range(5) if (i + j) % 2 == 0]
    return _charge(S, *sq)


@icon("heraldic-gyronny", CAT, "Heater shield divided from its center into eight wedges, alternately filled",
      tags=["gyronny", "coat of arms", "heraldry", "pinwheel", "wedges", "division"])
def _(S):
    cx, cy = 12, 11
    wedges = []
    for k in range(0, 8, 2):
        a, b = -90 + 45 * k, -45 + 45 * k
        wedges.append(poly([(cx, cy), pt(cx, cy, 20, a), pt(cx, cy, 20, b)], closed=True))
    return _charge(S, *wedges)


def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


@icon("heraldic-inescutcheon", CAT, "Heater shield with a smaller solid shield in its center",
      tags=["inescutcheon", "escutcheon", "coat of arms", "heraldry", "shield in shield", "charge"])
def _(S):
    small = ("M8.5 7H15.5V10.5C15.5 13 14 14.8 12 15.8C10 14.8 8.5 13 8.5 10.5Z" if S.name == "line" else
             "M9.5 7H14.5Q15.5 7 15.5 8V10.5C15.5 13 14 14.8 12.5 15.6Q12 15.8 11.5 15.6C10 14.8 8.5 13 8.5 10.5V8Q8.5 7 9.5 7Z")
    return [shell(_hs(S)), mark(small)]


@icon("heraldic-ermine-spot", CAT, "Heraldic ermine mark of three dots above a tapering spike with flared tails",
      tags=["ermine", "ermine spot", "heraldry", "fur", "brittany", "tincture"])
def _(S):
    tail = rpoly([(12, 9), (14.5, 13.5), (18.5, 19.5), (14.3, 17.8), (12, 21), (9.7, 17.8), (5.5, 19.5), (9.5, 13.5)], S, 0.3)
    return [shell(tail), dot(12, 3.8, 1.6), dot(7.8, 6.5, 1.6), dot(16.2, 6.5, 1.6)]


# ============================================================================ crosses and ornaments

def soften(d, r):
    """Round convex corners by r."""
    region = P(d)
    er = D(region, ST(path_to_d(region), 2 * r, "butt", "round"))
    return path_to_d(U(er, ST(path_to_d(er), 2 * r, "butt", "round")))


def fillet_in(d, r):
    """Round concave corners by r."""
    region = P(d)
    di = U(region, ST(path_to_d(region), 2 * r, "butt", "round"))
    return path_to_d(D(di, ST(path_to_d(di), 2 * r, "butt", "round")))


@icon("cross-pattee", CAT, "Cross whose arms are narrow at the center and flare wide at their flat ends",
      tags=["cross formee", "templar cross", "iron cross", "heraldry", "order", "medal"], aliases=["cross-formee"])
def _(S):
    d = ("M10.5 10.5Q11 5.5 7.5 2.5H16.5Q13 5.5 13.5 10.5Q18.5 11 21.5 7.5V16.5Q18.5 13 13.5 13.5Q13 18.5 16.5 21.5H7.5"
         "Q11 18.5 10.5 13.5Q5.5 13 2.5 16.5V7.5Q5.5 11 10.5 10.5Z")
    return [shell(d if S.name == "line" else soften(d, 0.8))]


@icon("cross-potent", CAT, "Cross with a short crossbar capping the end of each arm",
      tags=["crutch cross", "jerusalem cross", "heraldry", "t cross", "potent", "christian"], aliases=["crutch-cross"])
def _(S):
    return [line(seg(12, 3, 12, 21)), line(seg(3, 12, 21, 12)), line(seg(7.5, 3, 16.5, 3)), line(seg(7.5, 21, 16.5, 21)),
            line(seg(3, 7.5, 3, 16.5)), line(seg(21, 7.5, 21, 16.5))]


@icon("cross-moline", CAT, "Cross whose four arms split at the ends into two outward curling tips",
      tags=["moline", "millrind", "heraldry", "anchor cross", "cross", "christian"])
def _(S):
    parts = [line(seg(12, 6.5, 12, 17.5)), line(seg(6.5, 12, 17.5, 12))]
    for a in (0, 90, 180, 270):
        for side in (-1, 1):
            q = rotp([(12, 6.5), (12, 4), (12 + 2 * side, 2.2), (12 + 4.5 * side, 4.4)], a)
            parts.append(line("M" + " ".join(f"{fmt(x)} {fmt(y)}" if i != 1 else f"C{fmt(x)} {fmt(y)}"
                                             for i, (x, y) in enumerate(q))))
    return parts


@icon("quatrefoil", CAT, "Four round lobes arranged in a cross forming a four-leaf outline",
      tags=["four lobes", "gothic tracery", "ornament", "heraldry", "four leaf", "window"])
def _(S):
    d = union(circle(16.5, 12, 4.5), circle(7.5, 12, 4.5), circle(12, 7.5, 4.5), circle(12, 16.5, 4.5))
    return [shell(d if S.name == "line" else fillet_in(d, 1.2)), dot(12, 12, 1.5)]


# ============================================================================ armour pieces (2)

@icon("armor-stand", CAT, "Empty suit of plate armour with a closed helmet standing on a small base",
      tags=["suit of armour", "knight", "plate armour", "museum", "castle", "display"],
      aliases=["suit-of-armor", "suit-of-armour"])
def _(S):
    helm = ("M9.5 8V5C9.5 3.2 10.5 2 12 2C13.5 2 14.5 3.2 14.5 5V8Z" if S.name == "line" else
            "M10.5 8Q9.5 8 9.5 7V5C9.5 3.2 10.5 2 12 2C13.5 2 14.5 3.2 14.5 5V7Q14.5 8 13.5 8Z")
    torso = rpoly([(7, 9.5), (17, 9.5), (16, 15), (8, 15)], S, 0.8)
    return [shell(helm), shell(torso), line(poly([(6, 10.5), (4.5, 16.5)])), line(poly([(18, 10.5), (19.5, 16.5)])),
            line(seg(10, 15, 10, 19.5)), line(seg(14, 15, 14, 19.5)), shell(rect(6.5, 19.5, 11, 2, min(S.R, 1)))]


@icon("jousting-lance", CAT, "Long tapering tournament lance with a cone-shaped hand guard near the grip",
      tags=["lance", "tournament", "joust", "tilting", "knight", "vamplate"], aliases=["tilting-lance"])
def _(S):
    shaft = rotp([(11, 13), (12, -1), (13, 13)], 45)
    cone = ("M11 12.5H13L16.5 18.5Q12 20 7.5 18.5Z" if S.name == "line" else
            "M11.5 12.5H12.5Q13 12.5 13.2 13L16 17.5Q16.5 18.5 15.4 18.8Q12 19.6 8.6 18.8Q7.5 18.5 8 17.5L10.8 13Q11 12.5 11.5 12.5Z")
    grip = rotp([(12, 19.5), (12, 24.5)], 45)
    return [shell(poly(shaft, closed=True, r=S.r * 0.3)), shell(rot(cone, 45)), line(seg(*grip[0], *grip[1]))]


# ============================================================================ dwellings (2)

@icon("iron-age-roundhouse", CAT, "Round hut with low walls, a tall conical thatched roof and a dark doorway",
      tags=["roundhouse", "iron age", "celtic", "thatched hut", "prehistoric", "village"])
def _(S):
    roof = ("M1.5 13.5L12 2.5L22.5 13.5Q12 17.5 1.5 13.5Z" if S.name == "line" else
            "M2.6 13.1L11.3 3.2Q12 2.5 12.7 3.2L21.4 13.1Q22 14 21 14.3Q12 17 3 14.3Q2 14 2.6 13.1Z")
    wall = "M4.5 14V19.5Q12 22.5 19.5 19.5V14Z"
    door = mark("M10 21V18.5Q10 17 12 17Q14 17 14 18.5V21.2Q12 21.5 10 21Z")
    return [shell(roof), shell(wall), door]


# ============================================================================ heraldic beasts and emblems

@icon("heraldic-lion-rampant", CAT, "Stylised lion rearing on one hind leg with forepaws raised and tail curled high",
      tags=["lion rampant", "coat of arms", "heraldry", "royal", "scotland", "emblem"], aliases=["lion-rampant"])
def _(S):
    body = rpoly([(9, 2.5), (11.5, 3.5), (12.5, 6.5), (13.5, 10), (16, 13.5), (16.5, 17), (18, 21.5), (14.5, 21.5),
                  (13.5, 18), (11.5, 16.5), (10, 18.5), (7.5, 19), (8.5, 16.5), (9.5, 14.5), (8, 11.5), (4.5, 11),
                  (3, 9.5), (7, 8.8), (6, 7.2), (3, 6.8), (4.2, 5), (3.5, 3.5), (6, 2.8)], S, 0.4)
    tail = "M16 14C19.5 13.5 20.5 10.5 19 8C18 6.3 19 4.3 21 4.5"
    return [shell(body), line(tail), dot(7.5, 4.8, 0.8)]


@icon("double-headed-eagle", CAT, "Stylised eagle with spread wings and tail and two heads facing away from each other",
      tags=["two headed eagle", "bicephalous eagle", "coat of arms", "heraldry", "byzantine", "emblem"],
      aliases=["two-headed-eagle"])
def _(S):
    wing = rpoly([(10.5, 10.5), (3.5, 5.5), (2, 7.5), (3.5, 9), (2.5, 11), (4.5, 12), (4, 14), (10.5, 14)], S, 0.4)
    neck = rpoly([(10.2, 9.5), (8, 5.5), (9.8, 5), (12, 8.5)], S, 0.4)
    head = circle(8.2, 4.2, 1.9)
    beak = rpoly([(7, 3), (4.2, 4.6), (7.2, 5.5)], S, 0.3)
    body = ellipse(12, 12.5, 2.7, 4.5)
    tail = rpoly([(10.5, 16), (13.5, 16), (15.5, 21.5), (8.5, 21.5)], S, 0.4)
    half = union(wing, neck, head, beak)
    return [shell(union(half, flip(half), body, tail))]


@icon("heraldic-stag", CAT, "Stylised standing stag with one foreleg raised and a large branching antler rack",
      tags=["stag", "hart", "deer", "coat of arms", "heraldry", "emblem"], aliases=["stag-trippant"])
def _(S):
    body = rpoly([(4, 9.5), (6.5, 8), (8.5, 12), (17.5, 12), (20, 13.5), (19, 17), (7.5, 17), (6, 13), (3.5, 11)], S, 0.6)
    legs = [line(seg(8.5, 17, 8.5, 21.5)), line(poly([(10.5, 17), (12, 19), (10.5, 20.5)], r=S.r * 0.5)),
            line(seg(16, 17, 16, 21.5)), line(seg(18.5, 17, 19, 21.5))]
    antlers = [line("M5.5 8C4.5 6 4.5 4 5.5 2"), line(seg(4.8, 5.2, 2.5, 4)),
               line("M6.8 8.3C8 6 10 4.5 13 4"), line(seg(9.2, 5.3, 9.2, 2.5)), line(seg(11.3, 4.3, 12.5, 2))]
    return [shell(body)] + legs + antlers


@icon("heraldic-rose", CAT, "Stylised five-petal rose with a round center and pointed barbs between the petals",
      tags=["tudor rose", "heraldic rose", "coat of arms", "heraldry", "england", "emblem"], aliases=["tudor-rose"])
def _(S):
    petals = union(circle(12, 12, 4.5), *[circle(*pt(12, 12, 4.8, -90 + 72 * k), 4.1) for k in range(5)])
    if S.name == "rounded":
        petals = fillet_in(petals, 1)
    barbs = []
    for k in range(5):
        a = -54 + 72 * k
        barbs.append(solid(poly([pt(12, 12, 7, a - 12), pt(12, 12, 10.3, a), pt(12, 12, 7, a + 12)], closed=True)))
    return [shell(petals), detail(circle(12, 12, 3))] + barbs


@icon("coronet", CAT, "Low jewelled crown band topped with pearls on spikes and leaf points",
      tags=["coronet", "noble crown", "peerage", "earl", "heraldry", "royal"])
def _(S):
    band = rect(3.5, 14, 17, 6.5, min(S.R, 1.5))
    leaves = [rpoly([(x - 2.2, 14.2), (x, 9.5), (x + 2.2, 14.2)], S, 0.4) for x in (5.5, 12, 18.5)]
    parts = [shell(union(band, *leaves))]
    for x in (8.75, 15.25):
        parts += [line(seg(x, 14, x, 8)), dot(x, 6, 1.7)]
    return parts + [dot(8.5, 17.25, 1), dot(12, 17.25, 1), dot(15.5, 17.25, 1)]


# ============================================================================ banners and standards

@icon("gonfalon", CAT, "Banner hanging from a crossbar on a pole with long pointed tails along its bottom edge",
      tags=["banner", "gonfanon", "processional banner", "guild banner", "medieval", "flag"], aliases=["gonfanon"])
def _(S):
    banner = rpoly([(6, 5.5), (18, 5.5), (18, 16), (16, 20.5), (14, 16), (12, 20.5), (10, 16), (8, 20.5), (6, 16)], S, 0.4)
    return [line(seg(12, 2, 12, 4.5)), line(seg(3.5, 4.5, 20.5, 4.5)), shell(banner)]


@icon("roman-eagle-standard", CAT, "Roman legion standard with an eagle on a crossbar above a plaque on a tall pole",
      tags=["aquila", "legion", "roman standard", "eagle", "ancient rome", "insignia"])
def _(S):
    wing = rpoly([(11, 7), (4, 2.5), (4.5, 5), (6, 5.5), (6.5, 7.5), (8.5, 8), (10, 9.5)], S, 0.4)
    eagle = union(wing, flip(wing), ellipse(12, 7.5, 2.2, 2.5), circle(12, 4.3, 1.6),
                  poly([(11, 3.5), (8.8, 4.8), (11, 5.2)], closed=True))
    return [shell(eagle), line(seg(7.5, 11, 16.5, 11)), line(seg(12, 11, 12, 22)),
            shell(rect(8, 14.5, 8, 4, min(S.R, 1)))]


@icon("roman-vexillum", CAT, "Pole with a spear tip and a crossbar from which a square fringed flag hangs",
      tags=["vexillum", "roman flag", "legion", "cavalry standard", "ancient rome", "banner"], aliases=["vexillum"])
def _(S):
    tip_ = rpoly([(12, 2.8), (13.6, 6), (10.4, 6)], S, 0.3)
    flag = rect(5.5, 7.5, 13, 8.5, min(S.R, 1))
    fringe = [dot(x, 18.5, 1.1) for x in (7, 9.5, 14.5, 17)]
    return [shell(tip_), line(seg(12, 6, 12, 22)), line(seg(4, 7.5, 20, 7.5)), shell(flag)] + fringe


@icon("draco-standard", CAT, "Pole topped with a dragon head whose open mouth leads into a windsock tail",
      tags=["draco", "dragon standard", "windsock", "roman cavalry", "sarmatian", "banner"], aliases=["dragon-standard"])
def _(S):
    head = rpoly([(2, 5), (5, 3), (8, 1.8), (8.5, 3.2), (10.5, 4), (11, 9.5), (7, 10), (4, 9.5), (6.5, 7.2), (3, 7)], S, 0.4)
    sock = "M10.5 4C14 3.5 15.5 6 18 5.5C19.8 5.1 20.8 4 22 4C21.3 7 19.8 9 17.5 9.5C15 10 13.5 9 11 9.5Z"
    return [shell(union(head, sock)), line(seg(8, 10, 8, 22)), detail(seg(11, 4.2, 11, 9.3)), dot(7, 5.3, 0.9)]


# ============================================================================ completions

@icon("vambrace", CAT, "Angled metal forearm guard tube with a flared elbow end, two straps and hinge rivets",
      tags=["forearm guard", "arm armour", "bracer", "plate armour", "knight", "armour"], aliases=["forearm-guard"])
def _(S):
    tube = rotp([(6.5, 3.5), (17.5, 3.5), (16, 8), (15.3, 20.5), (8.7, 20.5), (8, 8)], 40)
    return [shell(poly(tube, closed=True, r=S.r * 0.6)),
            detail(rseg(8, 8, 16, 8, 40)), detail(rseg(8.8, 13.2, 15.2, 13.2, 40)),
            detail(rseg(8.6, 17.2, 15.4, 17.2, 40))]


@icon("greave", CAT, "Front view of a metal shin guard curving around the calf with a rounded knee cap on top",
      tags=["shin guard", "leg armour", "plate armour", "knight", "medieval", "armour"], aliases=["shin-guard"])
def _(S):
    plate = ("M6.5 11.5C6.5 15 8 18 9 21.5H15C16 18 17.5 15 17.5 11.5Z" if S.name == "line" else
             "M6.5 11.5C6.5 15 8 17.8 8.7 20.6Q9 21.5 9.9 21.5H14.1Q15 21.5 15.3 20.6C16 17.8 17.5 15 17.5 11.5Z")
    cap = ("M7.5 8C7.5 4.8 9.3 2.5 12 2.5C14.7 2.5 16.5 4.8 16.5 8Z" if S.name == "line" else
           "M8.5 8Q7.5 8 7.5 7C7.5 4.8 9.3 2.5 12 2.5C14.7 2.5 16.5 4.8 16.5 7Q16.5 8 15.5 8Z")
    return [shell(cap), shell(plate), detail("M12 13.5C11.6 16 12.2 18 12 19.5")]


@icon("heraldic-crest", CAT, "Coat of arms with a shield topped by a helmet and flowing leafy mantling on both sides",
      tags=["coat of arms", "achievement", "heraldry", "crest", "armorial", "family crest"], aliases=["coat-of-arms"])
def _(S):
    shield = ("M6.5 12.5H17.5V16C17.5 18.8 15 20.5 12 22C9 20.5 6.5 18.8 6.5 16Z" if S.name == "line" else
              "M7.5 12.5H16.5Q17.5 12.5 17.5 13.5V16C17.5 18.8 15 20.3 12.6 21.7Q12 22 11.4 21.7C9 20.3 6.5 18.8 6.5 16V13.5Q6.5 12.5 7.5 12.5Z")
    helm = ("M9.5 9V5C9.5 3.5 10.5 2.5 12 2.5C13.5 2.5 14.5 3.5 14.5 5V9Z" if S.name == "line" else
            "M10.5 9Q9.5 9 9.5 8V5C9.5 3.5 10.5 2.5 12 2.5C13.5 2.5 14.5 3.5 14.5 5V8Q14.5 9 13.5 9Z")
    left = "M8 4.5C5 4.5 3 6.5 3 9.5C3 10.5 3.3 11.2 3.8 11.8"
    right = flip(left)
    return [shell(helm), line(left), line(right), shell(shield), detail(seg(9.5, 5.8, 14.5, 5.8))]


@icon("circlet", CAT, "Thin metal headband drawn as a tilted ring with a single gem at the front",
      tags=["diadem", "headband", "tiara", "princess", "elf", "royal"])
def _(S):
    ring = rot(ellipse(12, 11, 9.5, 5), -8)
    gx, gy = rotp([(12, 16)], -8)[0]
    if S.name == "line":
        gem = poly([(gx, gy - 3.4), (gx + 3, gy), (gx, gy + 3.4), (gx - 3, gy)], closed=True)
    else:
        gem = circle(gx, gy, 3)
    return [line(ring), shell(gem)]
