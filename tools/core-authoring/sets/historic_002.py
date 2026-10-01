"""TypeIcon Core: historic objects (batch 002).

Ancient, medieval and early-modern artefacts, tools and dress, drawn from the objects themselves as simple
front or side views.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar  # noqa: F401

CAT = "historic"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def inter(a, b):
    return path_to_d(I(P(a), P(b)))


def grow(d, g):
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled body."""
    return Part("dot", d)


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


# ============================================================================ ancient Egypt

@icon("shabti", CAT, "Small mummy-shaped funerary figurine with a headdress, crossed arms and a line of text",
      tags=["ushabti", "egyptian", "figurine", "tomb", "mummy", "artifact"], aliases=["ushabti"])
def _(S):
    body = poly([(12, 2.5), (15, 3.2), (16.5, 6), (16.5, 11), (15.5, 21), (8.5, 21), (7.5, 11), (7.5, 6), (9, 3.2)],
                closed=True, r=L(S, 0, 1.5))
    return [
        shell(body),
        detail("M10 5.5V7.5A2 2 0 0 0 14 7.5V5.5"),
        detail(poly([(9.5, 12), (12, 13.5), (14.5, 12)], r=S.r)),
        detail(seg(10.5, 17.5, 13.5, 17.5)),
    ]


@icon("crook-and-flail", CAT, "A shepherd's crook crossed with a flail, the royal regalia of Egyptian pharaohs",
      tags=["pharaoh", "egyptian", "regalia", "kingship", "osiris", "scepter"], aliases=["heka-and-nekhakha"])
def _(S):
    return [
        line("M17.5 21.5L8 6A2.5 2.5 0 0 0 3 6V7.5"),
        line(seg(6.5, 21.5, 16, 4.5)),
        line(seg(16, 4.5, 16.5, 11.5)),
        line(seg(16, 4.5, 20, 9.5)),
        line(seg(16, 4.5, 21.5, 5.5)),
    ]


@icon("was-scepter", CAT, "Was scepter: a straight staff with a slanted animal-head top and a forked base",
      tags=["egyptian", "scepter", "staff", "power", "god", "regalia"])
def _(S):
    head = poly([(13.5, 8.5), (13.5, 5), (8, 2), (5.5, 3), (6, 5), (11, 6.5), (11, 8.5)], closed=True, r=S.r * 0.4)
    return [
        shell(head, stroke_miterlimit="2"),
        line(seg(12.25, 8.5, 12.25, 18.5)),
        line(poly([(9, 21.5), (9, 20), (12, 18), (15, 20), (15, 21.5)], r=S.r)),
    ]


@icon("hieroglyphs", CAT, "Stone panel carved with picture signs: an eye, a sun, a reed and wavy water",
      tags=["egyptian", "writing", "script", "ancient", "inscription", "glyphs"], aliases=["hieroglyphics"])
def _(S):
    eye = ("M7.5 7.5Q12 3.5 16.5 7.5Q12 11.5 7.5 7.5Z" if S.name == "line"
           else "M7.9 7.9Q7.5 7.5 7.9 7.1Q12 3.5 16.1 7.1Q16.5 7.5 16.1 7.9Q12 11.5 7.9 7.9Z")
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 3))),
        detail(eye),
        dot(12, 7.5, 1),
        dot(9, 13, 1.75),
        detail(poly([(14, 15), (14, 11), (16, 12.5)], r=S.r * 0.5)),
        detail(poly([(7.5, 18.5), (9.25, 17), (11, 18.5), (12.75, 17), (14.5, 18.5), (16.5, 17)], r=S.r * 0.5)),
    ]


@icon("egyptian-cat-statue", CAT, "Side view of a slim seated cat statue with tall ears and a collar",
      tags=["bastet", "egyptian", "cat", "statue", "sculpture", "goddess"])
def _(S):
    pts = [(16.5, 21), (15.5, 11), (17, 8.5), (17.5, 6.5), (16.5, 2.5), (14.5, 4.5), (12.5, 2.5), (12, 6.5),
           (11.5, 9.5), (8.5, 12), (7, 15.5), (7, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
        detail(seg(11, 10.5, 16, 10.5)),
        detail(seg(13, 15, 13, 21)),
    ]


@icon("scribe-palette", CAT, "Long scribe's palette with two round ink wells and a slot for reed brushes",
      tags=["scribe", "egyptian", "writing", "ink", "brush", "palette"])
def _(S):
    return [
        shell(rect(2, 8, 20, 8, rr(S, 2.5))),
        dot(5.75, 10.25, 1.4),
        dot(5.75, 13.75, 1.4),
        detail(seg(10, 12, 18.5, 12)),
        line(seg(15, 12, 21, 4)),
    ]


@icon("egyptian-broad-collar", CAT, "Front view of a wide semicircular beaded collar necklace",
      tags=["wesekh", "usekh", "egyptian", "necklace", "jewelry", "collar"], aliases=["wesekh"])
def _(S):
    cx, cy, ro, ri = 12, 6, 10, 4.5
    body = f"M{cx - ro} {cy}A{ro} {ro} 0 0 0 {cx + ro} {cy}H{cx + ri}A{ri} {ri} 0 0 1 {cx - ri} {cy}Z"
    parts = [shell(body)]
    for a in range(20, 170, 28):
        x, y = polar(cx, cy, 7.25, a)
        parts.append(dot(x, y, 1))
    return parts


@icon("egyptian-headrest", CAT, "Side view of an ancient headrest: a crescent neck rest on a column and base",
      tags=["egyptian", "headrest", "pillow", "furniture", "tomb", "sleep"])
def _(S):
    cres = "M3.5 4A8.4 8.4 0 0 0 20.5 4A11.5 11.5 0 0 1 3.5 4Z"
    return [
        shell(union(cres, rect(10, 9, 4, 9.5), rect(5, 18, 14, 3, rr(S, 1))), stroke_miterlimit="2"),
    ]


# ============================================================================ Greece and Rome

@icon("greek-krater", CAT, "Ancient Greek mixing vessel with a wide mouth, low handles and a foot",
      tags=["krater", "vase", "amphora", "pottery", "ancient greece", "urn"], aliases=["krater"])
def _(S):
    bowl = "M4 3.5H20L18 7.5C18 12.5 16 15.5 13.5 16.5H10.5C8 15.5 6 12.5 6 7.5Z"
    foot = poly([(10.5, 16), (13.5, 16), (13.5, 18.5), (16.5, 21), (7.5, 21), (10.5, 18.5)], closed=True)
    return [
        shell(union(bowl, foot)),
        detail(seg(6.2, 9.5, 17.8, 9.5)),
        line(poly([(6.3, 11), (3, 11), (3, 14), (8, 14)], r=S.r)),
        line(poly([(17.7, 11), (21, 11), (21, 14), (16, 14)], r=S.r)),
    ]


@icon("greek-kylix", CAT, "Side view of a shallow ancient Greek drinking cup on a slender stem with loop handles",
      tags=["kylix", "cup", "chalice", "pottery", "ancient greece", "wine"], aliases=["kylix"])
def _(S):
    bowl = "M5 7.5H19C19 11 16 13.5 12 13.5C8 13.5 5 11 5 7.5Z"
    stem = poly([(11, 13), (13, 13), (13, 17.5), (17, 21), (7, 21), (11, 17.5)], closed=True)
    return [
        shell(union(bowl, stem)),
        line(poly([(5.5, 10.5), (2.5, 10.5), (2.5, 7.5)], r=S.r)),
        line(poly([(18.5, 10.5), (21.5, 10.5), (21.5, 7.5)], r=S.r)),
    ]


@icon("greek-key-pattern", CAT, "Band of right-angled meander key pattern used as a classical border",
      tags=["meander", "greek key", "fret", "border", "pattern", "ornament"], aliases=["meander-pattern"])
def _(S):
    return [line(poly([(6, 9), (6, 15), (10, 15), (10, 5), (2, 5), (2, 19), (22, 19), (22, 5), (14, 5), (14, 15),
                       (18, 15), (18, 9)], r=S.r * 0.5))]


@icon("groma", CAT, "Roman surveying groma: a staff with a cross on top and plumb lines hanging from its arms",
      tags=["roman", "surveying", "survey", "instrument", "plumb line", "engineering"])
def _(S):
    return [
        line(seg(12, 5, 12, 21.5)),
        line(seg(3, 5, 21, 5)),
        line(seg(4, 5, 4, 12)), line(seg(20, 5, 20, 12)),
        line(seg(8, 5, 8, 9)), line(seg(16, 5, 16, 9)),
        mark(poly([(2.5, 12.5), (5.5, 12.5), (4, 15.5)], closed=True)),
        mark(poly([(18.5, 12.5), (21.5, 12.5), (20, 15.5)], closed=True)),
        dot(8, 10.5, 1.25), dot(16, 10.5, 1.25),
    ]


@icon("gold-death-mask", CAT, "Front view of a hammered gold funeral mask with closed eyes, moustache and beard",
      tags=["death mask", "funeral mask", "mycenae", "gold", "mask", "archaeology"], aliases=["funeral-mask"])
def _(S):
    face = "M12 2.5C7.5 2.5 5 5.5 5 10.5C5 16.5 8 21.5 12 21.5C16 21.5 19 16.5 19 10.5C19 5.5 16.5 2.5 12 2.5Z"
    return [
        shell(face),
        detail("M7.5 9Q9 10.5 10.5 9"), detail("M13.5 9Q15 10.5 16.5 9"),
        detail(poly([(8.5, 15), (12, 13.5), (15.5, 15)], r=S.r)),
        detail(seg(12, 17.5, 12, 19)),
    ]


# ============================================================================ Celtic, China, Japan, Korea

def _ell_arc(cx, cy, rx, ry, t0, t1):
    """Elliptical arc from parameter t0 to t1 (degrees, increasing = clockwise on screen), under 180 degrees."""
    p0 = (cx + rx * math.cos(math.radians(t0)), cy + ry * math.sin(math.radians(t0)))
    p1 = (cx + rx * math.cos(math.radians(t1)), cy + ry * math.sin(math.radians(t1)))
    return f"M{fmt(p0[0])} {fmt(p0[1])}A{fmt(rx)} {fmt(ry)} 0 0 1 {fmt(p1[0])} {fmt(p1[1])}"


@icon("celtic-knot", CAT, "Interlaced knot of two looped bands weaving over and under each other",
      tags=["celtic", "knotwork", "interlace", "irish", "scottish", "ornament"], aliases=["knotwork"])
def _(S):
    g = L(S, 14, 20)  # half-gap in degrees around the crossings where a band passes under
    th = math.degrees(math.acos(4.425 / 9.5))  # crossing parameter on the long axis
    tv = math.degrees(math.acos(4.425 / 5))
    parts = []
    for a, b in ((180 - th, 360 - th), (360 - th, 540 - th)):
        parts.append(line(_ell_arc(12, 12, 9.5, 5, a + g, b - g)))
    for a, b in ((tv, 180 + tv), (180 + tv, 360 + tv)):
        parts.append(line(_ell_arc(12, 12, 5, 9.5, a + g, b - g)))
    return parts


@icon("terracotta-warrior", CAT, "Front view of a standing clay soldier figure in armor with a side topknot",
      tags=["terracotta army", "qin", "chinese", "statue", "soldier", "archaeology"])
def _(S):
    head = union(circle(12, 5.5, 2.75), circle(14.5, 2.9, 1.3))
    torso = poly([(8, 9.5), (16, 9.5), (17, 17.5), (7, 17.5)], closed=True, r=L(S, 0, 1.5))
    legs = union(rect(8.5, 17, 3, 4.5, rr(S, 1)), rect(12.5, 17, 3, 4.5, rr(S, 1)))
    return [
        shell(head),
        shell(union(torso, legs)),
        detail(seg(10, 11.5, 9.6, 17.5)), detail(seg(14, 11.5, 14.4, 17.5)),
        detail(seg(12, 17.5, 12, 21.5)),
    ]


@icon("bronze-ding", CAT, "Ancient Chinese ritual cauldron with a round body, three legs and two upright handles",
      tags=["ding", "cauldron", "chinese", "bronze", "ritual vessel", "tripod"], aliases=["ding-vessel"])
def _(S):
    body = "M3.5 8H20.5C20.5 13.5 16.8 17 12 17C7.2 17 3.5 13.5 3.5 8Z"
    return [
        shell(body),
        line(poly([(6.5, 8), (6.5, 3.5), (9.5, 3.5), (9.5, 8)], r=S.r)),
        line(poly([(14.5, 8), (14.5, 3.5), (17.5, 3.5), (17.5, 8)], r=S.r)),
        detail(seg(5, 11.5, 19, 11.5)),
        line(seg(6.5, 15, 5.5, 21.5)), line(seg(12, 17, 12, 21.5)), line(seg(17.5, 15, 18.5, 21.5)),
    ]


@icon("bronze-mirror", CAT, "Back of an ancient round bronze mirror with a central knob, a ring and a beaded band",
      tags=["bronze mirror", "chinese", "han dynasty", "mirror", "artifact", "antique"])
def _(S):
    parts = [shell(circle(12, 12, 9)), detail(circle(12, 12, 4.25)), dot(12, 12, 1.5)]
    for i in range(8):
        x, y = polar(12, 12, 6.75, 22.5 + 45 * i)
        parts.append(dot(x, y, 0.85) if S.name == "rounded" else mark(rect(x - 0.8, y - 0.8, 1.6, 1.6)))
    return parts


@icon("spade-money", CAT, "Ancient Chinese bronze coin shaped like a small spade with a socket and two legs",
      tags=["spade money", "chinese", "coin", "bronze", "ancient currency", "money"])
def _(S):
    pts = [(10.5, 2.5), (13.5, 2.5), (13.5, 6), (18, 7.5), (18, 21.5), (13.5, 21.5), (13.5, 17.5), (10.5, 17.5),
           (10.5, 21.5), (6, 21.5), (6, 7.5), (10.5, 6)]
    return [shell(poly(pts, closed=True, r=S.r * 0.5)), detail(seg(12, 9.5, 12, 14))]


@icon("knife-money", CAT, "Ancient Chinese bronze coin shaped like a curved knife with a ring on the handle",
      tags=["knife money", "chinese", "coin", "bronze", "ancient currency", "money"])
def _(S):
    blade = poly([(9, 12.5), (13.5, 9), (17, 5.8), (21, 2.5), (19.8, 7), (16.5, 11), (12, 15)], closed=True, r=S.r * 0.4)
    return [
        shell(blade, stroke_miterlimit="2"),
        line(seg(10.5, 13.75, 7.3, 16.9)),
        shell(circle(5.5, 18.5, 2.25)),
    ]


@icon("haniwa", CAT, "Front view of a Japanese hollow clay cylinder figure with hole eyes and mouth and raised arms",
      tags=["haniwa", "japanese", "clay figure", "kofun", "terracotta", "tomb"])
def _(S):
    body = "M8.5 21.5V7.5A3.5 3.5 0 0 1 15.5 7.5V21.5Z" if S.name == "line" else \
        "M8.5 20V7.5A3.5 3.5 0 0 1 15.5 7.5V20A1.5 1.5 0 0 1 14 21.5H10A1.5 1.5 0 0 1 8.5 20Z"
    return [
        shell(body),
        mark(ellipse(10.5, 8, 0.9, 1.2)), mark(ellipse(13.5, 8, 0.9, 1.2)),
        mark(ellipse(12, 11.5, 1.2, 1)),
        line(poly([(8.5, 15), (5, 13), (5, 9.5)], r=S.r)),
        line(poly([(15.5, 15), (19, 16), (19, 18.5)], r=S.r)),
    ]


@icon("dogu", CAT, "Front view of a Japanese clay figurine with huge goggle eyes, a wide body and stubby limbs",
      tags=["dogu", "jomon", "japanese", "clay figure", "figurine", "archaeology"])
def _(S):
    head = ellipse(12, 6.5, 7.5, 4.5)
    body = poly([(8, 10.5), (16, 10.5), (20.5, 12.5), (19.5, 15.5), (16.5, 14.5), (17, 21.5), (13.5, 21.5), (12, 19.5),
                 (10.5, 21.5), (7, 21.5), (7.5, 14.5), (4.5, 15.5), (3.5, 12.5)], closed=True, r=S.r * 0.5)
    return [
        shell(union(head, body)),
        detail(ellipse(8.75, 6.5, 2, 1.6)), detail(ellipse(15.25, 6.5, 2, 1.6)),
    ]


@icon("inro", CAT, "Japanese inro: a small stacked lacquer case on a cord with a bead and a toggle",
      tags=["inro", "japanese", "case", "netsuke", "lacquer", "container"])
def _(S):
    return [
        shell(rect(6, 10, 12, 11.5, rr(S, 3))),
        detail(seg(6, 14, 18, 14)), detail(seg(6, 17.5, 18, 17.5)),
        line(poly([(9, 10), (12, 6.5), (15, 10)], r=S.r * 0.3)),
        shell(circle(12, 5, 1.6)),
        line(seg(12, 3.4, 12, 2)),
    ]


@icon("biwa", CAT, "Japanese biwa lute with a pear-shaped body, short neck and sharply bent-back pegbox",
      tags=["biwa", "lute", "japanese", "string instrument", "music", "traditional"])
def _(S):
    body = "M12 8C8.5 8 6 12.5 6 16C6 19.5 8.5 21.5 12 21.5C15.5 21.5 18 19.5 18 16C18 12.5 15.5 8 12 8Z"
    return [
        shell(union(body, rect(10.75, 5, 2.5, 4.5), poly([(10.75, 5.5), (15.5, 2), (16.8, 3.8), (13.25, 6.5)], closed=True)),
              stroke_miterlimit="2"),
        detail(seg(12, 10.5, 12, 18.5)),
        detail(seg(9.5, 18.5, 14.5, 18.5)),
    ]


@icon("turtle-ship", CAT, "Side view of a Korean armored warship with a spiked shell roof, oars and a dragon head",
      tags=["geobukseon", "korean", "warship", "ship", "joseon", "navy"], aliases=["geobukseon"])
def _(S):
    roof = "M4.5 15C4.5 11 7.8 9 12.5 9C17.2 9 20.5 11 20.5 15Z"
    hull = poly([(3, 15), (22, 15), (20, 18.5), (5, 18.5)], closed=True, r=S.r * 0.5)
    head = poly([(5.5, 12.5), (2, 11), (2, 13.5), (5, 15)], closed=True, r=S.r * 0.3)
    parts = [shell(union(roof, hull, head)), detail(seg(4, 15, 21.5, 15))]
    for x in (8, 12.5, 17):
        parts.append(mark(poly([(x - 1.2, 9.6), (x, 6.8), (x + 1.2, 9.6)], closed=True)))
    parts += [line(seg(8, 18.5, 6.5, 21.5)), line(seg(12.5, 18.5, 11, 21.5)), line(seg(17, 18.5, 15.5, 21.5))]
    return parts


@icon("korean-gat", CAT, "Side view of a Korean gat: a tall cylindrical horsehair hat with a wide flat brim and chin strings",
      tags=["gat", "korean", "hat", "joseon", "horsehair", "traditional"])
def _(S):
    crown = poly([(8.5, 11.5), (9, 3.5), (15, 3.5), (15.5, 11.5)], closed=True, r=L(S, 0, 1.2))
    return [
        shell(crown),
        shell(rect(2, 11.5, 20, 2.5, L(S, 0, 1.25))),
        line(poly([(8.5, 14.5), (10.5, 21), (13.5, 21), (15.5, 14.5)], r=S.r)),
    ]


@icon("howdah", CAT, "Side view of an elephant carrying a canopied seat with a domed roof",
      tags=["howdah", "elephant", "india", "canopy", "seat", "procession"])
def _(S):
    torso = "M2.5 16.5C2.5 12.5 5 10.5 9.5 10.5H14.5V18.5H2.5Z"
    legs = union(rect(3, 15, 3.5, 6.5, rr(S, 1)), rect(10.5, 15, 3.5, 6.5, rr(S, 1)))
    head = circle(17, 12, 4)
    trunk = path_to_d(ST("M19.5 13.5Q21.5 16.5 20.5 20.5", 2.5, "round", "round"))
    return [
        shell(union(torso, legs, head, trunk)),
        shell("M4 6.5A4.5 4.5 0 0 1 13 6.5Z"),
        line(seg(5, 6.5, 5, 10.5)), line(seg(12, 6.5, 12, 10.5)),
        detail("M15.5 10A3 3 0 0 1 15.5 15"),
    ]


@icon("indus-seal", CAT, "Square ancient stamp seal carved with a bull in profile and a row of script signs",
      tags=["indus valley", "harappa", "seal", "stamp", "ancient", "bull"], aliases=["harappan-seal"])
def _(S):
    bull = poly([(6.5, 12.5), (14, 12), (15.5, 10.5), (18, 13.5), (16.5, 14), (16.5, 18), (14.8, 18), (14.8, 15.5),
                 (9, 15.5), (9, 18), (7.3, 18), (7.3, 15)], closed=True)
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(seg(7, 6, 7, 8.5)), detail(poly([(10, 6), (10, 8.5), (12.5, 8.5), (12.5, 6)], r=S.r * 0.4)),
        detail(seg(15.5, 6, 17.5, 8.5)), detail(seg(17.5, 6, 15.5, 8.5)),
        mark(bull),
    ]


@icon("aztec-sun-stone", CAT, "Round carved stone calendar disc with a face in the centre and rings of carving",
      tags=["sun stone", "aztec", "calendar stone", "mexica", "mexico", "piedra del sol"], aliases=["aztec-calendar"])
def _(S):
    parts = [shell(circle(12, 12, 9)), detail(circle(12, 12, 4.75)), dot(10.6, 11.2, 0.9), dot(13.4, 11.2, 0.9),
             detail(seg(11, 13.6, 13, 13.6))]
    for i in range(8):
        x, y = polar(12, 12, 7, 22.5 + 45 * i)
        parts.append(mark(poly(regular(x, y, 1.3, 3, 22.5 + 45 * i + 180), closed=True)))
    return parts


# ============================================================================ Oceania, Arctic and ancient money

def _wobbly(cx, cy, radii):
    """Smooth closed blob through points at the given radii (evenly spaced angles)."""
    n = len(radii)
    pts = [polar(cx, cy, r, -90 + 360 * i / n) for i, r in enumerate(radii)]
    mids = [((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2) for i in range(n)]
    d = f"M{fmt(mids[-1][0])} {fmt(mids[-1][1])}"
    for i in range(n):
        d += f"Q{fmt(pts[i][0])} {fmt(pts[i][1])} {fmt(mids[i][0])} {fmt(mids[i][1])}"
    return d + "Z"


_COIN = [9.2, 9.0, 9.4, 9.1, 8.9, 9.3, 9.2, 8.9, 9.3, 9.0]


@icon("voyaging-canoe", CAT, "Side view of an ocean voyaging canoe with a curved crab-claw sail",
      tags=["waka", "polynesian", "canoe", "sail", "navigation", "pacific"])
def _(S):
    hull = "M2 15.5H22L20.5 19Q12 21.5 3.5 19Z"
    sail = "M11 13C7 10.5 4.5 7 4 2.5C7.5 6.5 10.5 8 13 7.5C15.5 7 18.5 5.5 21 3C19 8.5 15.5 11.5 11 13Z"
    return [
        shell(hull),
        shell(sail, stroke_miterlimit="2"),
        line(seg(11, 13, 11, 15.5)),
    ]


@icon("inukshuk", CAT, "Stone figure of stacked rocks with two legs, a long arm slab and a head stone",
      tags=["inuksuk", "inuit", "cairn", "stone figure", "arctic", "landmark"], aliases=["inuksuk"])
def _(S):
    k = rr(S, 1)
    body = union(rect(6, 15.5, 4.5, 6, k), rect(13.5, 15.5, 4.5, 6, k), rect(6.5, 11.5, 11, 4, k),
                 rect(2, 8, 20, 3.5, k), rect(9.5, 2.5, 5, 5.5, k))
    return [
        shell(body),
        detail(seg(6.5, 11.5, 17.5, 11.5)),
        detail(seg(9.5, 8, 14.5, 8)),
        detail(seg(10.5, 15.5, 13.5, 15.5)),
    ]


@icon("snow-goggles", CAT, "Front view of carved snow goggles with two narrow eye slits and a tie cord",
      tags=["snow goggles", "inuit", "arctic", "eyewear", "sun protection", "carved"])
def _(S):
    body = ("M4 9.5Q12 6.5 20 9.5V13Q16.5 15.5 13.5 13.5L12 12.5L10.5 13.5Q7.5 15.5 4 13Z" if S.name == "line" else
            "M4 11Q4 9.5 5.5 9Q12 7 18.5 9Q20 9.5 20 11V12.5Q16.5 15.5 13.5 13.5Q12 12.5 10.5 13.5Q7.5 15.5 4 12.5Z")
    return [
        shell(body),
        detail(seg(6.5, 11.25, 10, 11.25)), detail(seg(14, 11.25, 17.5, 11.25)),
        line("M4 11.5Q1.5 12 2 16"), line("M20 11.5Q22.5 12 22 16"),
    ]


@icon("ancient-coin", CAT, "Irregular hand-struck ancient coin showing a profile head",
      tags=["ancient coin", "roman coin", "greek coin", "numismatics", "denarius", "drachma"])
def _(S):
    head = poly([(9, 16.5), (9, 13.5), (7.2, 11.5), (7.3, 8.5), (9.5, 6.2), (12.5, 6), (15, 7.5), (15.5, 9.5), (16.8, 11.5),
                 (15.5, 12), (15.5, 14), (13.3, 14.3), (13.3, 16.5)], closed=True, r=L(S, 0, 1.2))
    return [shell(_wobbly(12, 12, _COIN)), mark(head)]


@icon("owl-coin", CAT, "Irregular thick ancient silver coin showing an owl with large round eyes",
      tags=["athenian owl", "tetradrachm", "greek coin", "ancient coin", "athena", "numismatics"], aliases=["tetradrachm"])
def _(S):
    k = L(S, 0, 0.8)
    owl = union(ellipse(12, 14, 3.8, 4), ellipse(12, 9.3, 4.2, 3.3),
                poly([(8.2, 8.5), (8.3, 5.2), (10.5, 7)], closed=True, r=k), poly([(15.8, 8.5), (15.7, 5.2), (13.5, 7)], closed=True, r=k))
    eyes = [circle(10.3, 9.4, 1.3), circle(13.7, 9.4, 1.3)] if S.name == "rounded" else \
        [rect(9.1, 8.2, 2.4, 2.4), rect(12.5, 8.2, 2.4, 2.4)]
    return [shell(_wobbly(12, 12, _COIN)), mark(minus(owl, *eyes))]


@icon("rai-stone", CAT, "Large round stone disc with a big hole through its centre standing on the ground",
      tags=["rai stone", "stone money", "yap", "micronesia", "currency", "ancient money"], aliases=["stone-money"])
def _(S):
    return [
        shell(minus(circle(12, 10.5, 8.5), circle(12, 10.5, 3))),
        line(seg(2, 20.5, 22, 20.5)),
    ]


# ============================================================================ writing and household

@icon("sealed-scroll", CAT, "Rolled parchment scroll tied with a ribbon and a hanging round wax seal",
      tags=["scroll", "parchment", "decree", "charter", "wax seal", "document"])
def _(S):
    seal = circle(12, 16.5, 3.25)
    cut = grow(seal, 2)
    return [
        shell(rect(2.5, 4, 19, 7.5, L(S, 2, 3.75))),
        detail(seg(5.5, 4, 5.5, 11.5)) if S.name == "line" else detail("M5.5 4.5Q6.5 7.75 5.5 11"),
        detail(seg(18.5, 4, 18.5, 11.5)) if S.name == "line" else detail("M18.5 4.5Q17.5 7.75 18.5 11"),
        line(seg(11, 11.5, 10.3, 12.9)), line(seg(13, 11.5, 13.7, 12.9)),
        line(seg(9.2, 19.9, 8.5, 21.5)), line(seg(14.8, 19.9, 15.5, 21.5)),
        shell(seal),
        dot(12, 16.5, 1),
    ]


def _tube(p0, p1, p2, p3, w0, w1, n=16):
    """Closed outline around a cubic centreline whose width changes linearly from w0 to w1."""
    def bz(t):
        u = 1 - t
        return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        a, b = bz(max(0, t - 0.01)), bz(min(1, t + 0.01))
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy)
        nx, ny = -dy / ln, dx / ln
        x, y = bz(t)
        w = (w0 + (w1 - w0) * t) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return left + right[::-1]


@icon("ink-horn", CAT, "Curved horn-shaped ink pot with a quill standing in its open end",
      tags=["inkhorn", "ink pot", "quill", "scribe", "writing", "medieval"], aliases=["inkhorn"])
def _(S):
    horn = poly(_tube((13.5, 10.5), (13.5, 17), (9, 21.5), (3.5, 16.5), 7, 1.5), closed=True)
    vane = ("M17 7.5C16.8 4.5 18.5 2.2 21.5 1.5C22 4.5 20.2 6.8 17 7.5Z" if S.name == "rounded" else
            poly([(17, 7.5), (18, 3.5), (21.5, 1.5), (20.5, 5.5)], closed=True))
    return [
        shell(horn, stroke_miterlimit="2"),
        detail(seg(10, 13, 17, 13)),
        line(seg(14.5, 10.5, 17, 7.5)),
        shell(vane, stroke_miterlimit="2"),
    ]


@icon("rhyton", CAT, "Curved drinking horn whose narrow end is shaped like an animal's head and forelegs",
      tags=["rhyton", "drinking horn", "ancient greece", "persian", "vessel", "cup"])
def _(S):
    horn = poly(_tube((17.5, 3), (17.5, 10), (14, 14.5), (9, 15), 7, 3.5), closed=True)
    head = poly([(10, 13), (7.5, 12.5), (4.5, 13.2), (2.5, 14.8), (2.5, 16.5), (5, 17.2), (8, 17.5), (10, 17)],
                closed=True, r=L(S, 0, 1))
    ear = poly([(6.3, 13), (7.3, 9.8), (9, 13)], closed=True, r=S.r * 0.3)
    return [
        shell(union(horn, head, ear), stroke_miterlimit="2"),
        detail(seg(13.8, 6, 21.2, 6)),
        line(seg(5.5, 17.5, 5, 21.5)), line(seg(8.5, 17.8, 9, 21.5)),
    ]


@icon("ancient-seismoscope", CAT, "Round bronze urn ringed with dragon heads holding balls above waiting toads",
      tags=["seismoscope", "earthquake detector", "zhang heng", "chinese invention", "seismograph", "han dynasty"])
def _(S):
    urn = "M7.5 7H16.5C19 9 19.5 12 18.5 14.5C17.5 17 15.5 18.5 12 18.5C8.5 18.5 6.5 17 5.5 14.5C4.5 12 5 9 7.5 7Z"
    lid = "M8.5 7.5A3.5 3.5 0 0 1 15.5 7.5Z"
    dl = poly([(5.5, 9.5), (2, 9.5), (2, 11.5), (5, 12)], closed=True, r=S.r * 0.4)
    dr = poly([(18.5, 9.5), (22, 9.5), (22, 11.5), (19, 12)], closed=True, r=S.r * 0.4)
    return [
        shell(union(urn, lid, dl, dr)),
        dot(12, 2.8, 1.3),
        detail(seg(6, 11.5, 18, 11.5)),
        dot(3.75, 15, 1.1), dot(20.25, 15, 1.1),
        line(poly([(2, 18.5), (2, 21.5), (5.5, 21.5), (5.5, 18.5)], r=S.r)),
        line(poly([(18.5, 18.5), (18.5, 21.5), (22, 21.5), (22, 18.5)], r=S.r)),
    ]


@icon("writing-slope", CAT, "Portable wooden writing box opened into a slanted desk with an inkwell and a quill",
      tags=["writing slope", "writing box", "lap desk", "portable desk", "stationery", "antique"], aliases=["lap-desk"])
def _(S):
    box = poly([(2, 20.5), (22, 20.5), (22, 11), (17, 11), (2, 15.5)], closed=True, r=L(S, 0, 1.2))
    well = rect(17.5, 6.5, 4, 4.5, rr(S, 1.2))
    return [
        shell(union(box, well)),
        detail(seg(17.5, 11, 21.5, 11)),
        detail(seg(2, 17.5, 22, 17.5)),
        line(seg(18.5, 6.5, 13.5, 1.5)),
    ]


@icon("aquamanile", CAT, "Water jug shaped like a standing lion with a spout at its mouth and a handle over its back",
      tags=["aquamanile", "lion jug", "ewer", "medieval", "bronze", "vessel"])
def _(S):
    head = union(circle(7, 8, 3.5), rect(1.5, 8.5, 3, 2.5, L(S, 0, 1)))
    body = rect(7, 9, 12.5, 6.5, rr(S, 3))
    legs = union(rect(7.5, 14, 3, 7.5, rr(S, 1)), rect(16, 14, 3, 7.5, rr(S, 1)))
    return [
        shell(union(head, body, legs)),
        line("M8.5 4.8C11 1.5 16 2 17 9"),
        line("M19.5 11Q22 10.5 21.5 7"),
    ]


@icon("steelyard-scale", CAT, "Hanging steelyard balance with a pan on the short end and a sliding weight on the long arm",
      tags=["steelyard", "balance", "weighing", "scale", "roman", "market"], aliases=["steelyard"])
def _(S):
    return [
        line(seg(2, 7, 22, 7)),
        line(seg(8, 7, 8, 4.5)), shell(circle(8, 2.9, 1.4)),
        line(seg(4, 7, 2.5, 14)), line(seg(4, 7, 6.5, 14)),
        shell("M1 14H8C7.5 16.5 5.8 17.5 4.5 17.5C3.2 17.5 1.5 16.5 1 14Z" if S.name == "line" else
              "M1.5 14H7.5A1 1 0 0 1 7.3 15C6.6 16.7 5.6 17.5 4.5 17.5C3.4 17.5 2.4 16.7 1.7 15A1 1 0 0 1 1.5 14Z"),
        line(seg(17, 7, 17, 11)),
        shell(poly([(15.5, 11), (18.5, 11), (20, 17), (14, 17)], closed=True, r=L(S, 0, 1.2))),
        dot(12, 9.5, 0.8), dot(20.5, 9.5, 0.8),
    ]


@icon("grindstone", CAT, "Round sharpening stone wheel with a crank handle above a water trough",
      tags=["grindstone", "whetstone", "sharpening", "grinding wheel", "blacksmith", "mill"], aliases=["sharpening-wheel"])
def _(S):
    return [
        shell(circle(10.5, 8.5, 6)),
        dot(10.5, 8.5, 1.4),
        line(poly([(16.5, 8.5), (20.5, 8.5), (20.5, 12.5), (22.5, 12.5)], r=S.r)),
        shell(rect(3, 17, 15, 4.5, rr(S, 1.5))),
    ]


@icon("pole-lathe", CAT, "Wooden bench lathe with a springy pole overhead and a cord running down to a foot treadle",
      tags=["pole lathe", "bodger", "woodturning", "green woodworking", "lathe", "treadle"])
def _(S):
    return [
        line("M2 4.5Q11 1 21.5 3"),
        shell(rect(2, 12, 20, 2.5, L(S, 0, 1.25))),
        line(seg(4, 14.5, 3, 21.5)), line(seg(20, 14.5, 21, 21.5)),
        shell(rect(5, 6.5, 2.5, 5.5, L(S, 0, 1))), shell(rect(16.5, 6.5, 2.5, 5.5, L(S, 0, 1))),
        line(seg(7.5, 9, 16.5, 9)),
        line(seg(12, 2.5, 12, 8)),
        line(seg(12, 14.5, 12, 18)),
        line(seg(7, 21.5, 16, 18)),
    ]


@icon("pump-drill", CAT, "Pump drill: an upright spindle with a heavy flywheel and a crossbar wound on cords",
      tags=["pump drill", "bow drill", "drilling", "ancient tool", "fire making", "spindle"])
def _(S):
    return [
        line(seg(12, 2, 12, 22)),
        shell(rect(4, 9, 16, 2.5, L(S, 0, 1.25))),
        line(seg(5, 9, 12, 3)), line(seg(19, 9, 12, 3)),
        shell(rect(5, 15, 14, 4, rr(S, 2))),
    ]


@icon("bloomery-furnace", CAT, "Squat clay furnace with glowing coals at an arched opening and bellows beside it",
      tags=["bloomery", "furnace", "iron smelting", "forge", "iron age", "smelter"])
def _(S):
    body = poly([(3, 21.5), (15, 21.5), (12.5, 7.5), (5.5, 7.5)], closed=True, r=L(S, 0, 1.5))
    bellows = poly([(15.5, 17.5), (19, 14), (22, 14), (22, 21), (19, 21)], closed=True, r=S.r * 0.5)
    return [
        shell(body),
        detail("M6.5 21.5V19A2.5 2.5 0 0 1 11.5 19V21.5"),
        shell(bellows),
        shell(_flame(9, 5.5, 3.5, 1.6), stroke_miterlimit="2"),
    ]


@icon("olive-mill", CAT, "Round stone basin with an upright millstone rolled around by a wooden beam",
      tags=["olive mill", "olive press", "millstone", "oil mill", "trapetum", "edge runner"])
def _(S):
    return [
        shell(poly([(2, 15), (22, 15), (20.5, 21.5), (3.5, 21.5)], closed=True, r=L(S, 0, 1.5))),
        shell(circle(8.5, 9.5, 5.5)),
        dot(8.5, 9.5, 1.2),
        line(seg(14, 9.5, 22, 9.5)),
        line(seg(17.5, 3, 17.5, 15)),
    ]


@icon("warming-pan", CAT, "Round lidded pan with a pierced lid on the end of a long handle, used to warm a bed",
      tags=["warming pan", "bed warmer", "brass", "antique", "bedroom", "heating"], aliases=["bed-warmer"])
def _(S):
    parts = [shell(circle(8, 16, 6)), line(seg(12.4, 11.9, 16, 8.5)),
             shell(poly([(15, 8.5), (20.5, 3), (21.5, 4), (16, 9.5)], closed=True, r=L(S, 0, 0.6)))]
    for a in range(0, 360, 60):
        x, y = polar(8, 16, 3, a)
        parts.append(dot(x, y, 0.8) if S.name == "rounded" else mark(rect(x - 0.75, y - 0.75, 1.5, 1.5)))
    parts.append(dot(8, 16, 0.8) if S.name == "rounded" else mark(rect(7.25, 15.25, 1.5, 1.5)))
    return parts


@icon("ewer-and-basin", CAT, "Tall jug with a handle and a pointed spout standing in a wide shallow basin",
      tags=["ewer", "basin", "wash jug", "pitcher and bowl", "washstand", "antique"], aliases=["jug-and-basin"])
def _(S):
    jug = "M10 3.5L6.5 2.5L9.5 6.5C7.5 8.5 7 12.5 9 16.5H15C17 12.5 16.5 8.5 14.5 6.5V3.5Z"
    basin = "M2 16H22C21 19.5 17 21.5 12 21.5C7 21.5 3 19.5 2 16Z"
    return [
        shell(union(jug, basin), stroke_miterlimit="2"),
        detail(seg(8.9, 16, 15.1, 16)),
        line("M14.8 6H16.5C18.5 6 19.5 7.5 19.5 9.5C19.5 11.5 18 12.5 16.3 13"),
    ]


@icon("flagon", CAT, "Tall lidded pewter flagon with a thumb lever, a curved handle and a pouring lip",
      tags=["flagon", "tankard", "pewter", "jug", "ale", "medieval"])
def _(S):
    body = poly([(7, 21.5), (8, 8), (15.5, 8), (16.5, 21.5)], closed=True, r=L(S, 0, 1.2))
    lid = "M7.5 7.5A4.25 3.5 0 0 1 16 7.5Z"
    return [
        shell(union(body, lid, poly([(8.3, 8), (5, 7), (8.1, 11)], closed=True))),
        detail(seg(7.8, 8, 15.7, 8)),
        line(seg(15.5, 5, 17.5, 2.5)),
        line("M16.2 10H18.5C19.6 10 20.5 10.9 20.5 12V14.5C20.5 16 19 17.5 16.9 18"),
        detail(seg(7.3, 18.5, 16.2, 18.5)),
    ]


@icon("winged-hourglass", CAT, "Hourglass with a pair of outstretched bird wings at its sides",
      tags=["winged hourglass", "time flies", "tempus fugit", "memento mori", "emblem", "hourglass"])
def _(S):
    glass = poly([(9.5, 4), (14.5, 4), (14.5, 7), (12.6, 12), (14.5, 17), (14.5, 20), (9.5, 20), (9.5, 17), (11.4, 12),
                  (9.5, 7)], closed=True, r=S.r * 0.4)
    wl = poly([(7.5, 11), (5, 6.5), (2, 5), (2, 9), (3, 11.5), (4.5, 13.5), (7.5, 14.5)], closed=True, r=S.r * 0.5)
    wr = poly([(16.5, 11), (19, 6.5), (22, 5), (22, 9), (21, 11.5), (19.5, 13.5), (16.5, 14.5)], closed=True, r=S.r * 0.5)
    return [
        shell(glass, stroke_miterlimit="2"),
        shell(wl), shell(wr),
        detail(seg(2.5, 9, 6.5, 11.5)), detail(seg(21.5, 9, 17.5, 11.5)),
        line(seg(8, 3, 16, 3)), line(seg(8, 21, 16, 21)),
    ]


def _flame(cx, base, h, w):
    """Teardrop flame with its base centred at (cx, base)."""
    return (f"M{fmt(cx)} {fmt(base - h)}C{fmt(cx + w * 0.3)} {fmt(base - h * 0.6)} {fmt(cx + w)} {fmt(base - h * 0.45)}"
            f" {fmt(cx + w)} {fmt(base - h * 0.2)}A{fmt(w)} {fmt(h * 0.2)} 0 0 1 {fmt(cx - w)} {fmt(base - h * 0.2)}"
            f"C{fmt(cx - w)} {fmt(base - h * 0.45)} {fmt(cx - w * 0.3)} {fmt(base - h * 0.6)} {fmt(cx)} {fmt(base - h)}Z")


@icon("cresset", CAT, "Iron cage basket full of flames on top of a tall pole",
      tags=["cresset", "fire basket", "torch", "beacon", "medieval", "light"])
def _(S):
    cage = poly([(6.5, 10), (17.5, 10), (15, 15), (9, 15)], closed=True, r=S.r * 0.5)
    flames = union("M12 2C14.5 4.5 15.5 6.5 15.5 9V10.5H8.5V9C8.5 6.5 9.5 4.5 12 2Z",
                   "M7.5 5.5C9 7 9.5 8.5 9.5 10.5H5.5C5.5 8.5 6 7 7.5 5.5Z", "M16.5 5.5C18 7 18.5 8.5 18.5 10.5H14.5C14.5 8.5 15 7 16.5 5.5Z")
    return [
        shell(union(cage, flames)),
        detail(seg(7, 10.25, 17, 10.25)),
        detail(seg(12, 10.5, 12, 15)),
        line(seg(12, 15, 12, 21.5)),
        line(seg(9, 21.5, 15, 21.5)),
    ]


@icon("brazier", CAT, "Wide iron bowl of burning coals with flames, standing on three legs",
      tags=["brazier", "fire bowl", "fire pit", "coals", "heater", "medieval"], aliases=["fire-bowl"])
def _(S):
    bowl = "M3 11.5H21C21 15 17 17 12 17C7 17 3 15 3 11.5Z"
    flames = union("M12 3C14.5 5.5 15.5 7 15.5 9.5V11.5H8.5V9.5C8.5 7 9.5 5.5 12 3Z",
                   "M7 7C8.5 8.5 9 9.5 9 11.5H5C5 9.5 5.5 8.5 7 7Z", "M17 7C18.5 8.5 19 9.5 19 11.5H15C15 9.5 15.5 8.5 17 7Z")
    return [
        shell(union(bowl, flames)),
        detail(seg(3.5, 11.5, 20.5, 11.5)),
        line(seg(7, 16, 5.5, 21.5)), line(seg(12, 17, 12, 21.5)), line(seg(17, 16, 18.5, 21.5)),
    ]


# ============================================================================ hearth, home and personal effects

@icon("andiron", CAT, "Side view of an iron fire dog: a log bar on short legs with an upright front post and knob",
      tags=["andiron", "firedog", "fireplace", "hearth", "log holder", "fire iron"], aliases=["firedog"])
def _(S):
    finial = poly([(6, 1.5), (8, 4), (6, 6.5), (4, 4)], closed=True, r=L(S, 0, 1))
    post = rect(4.75, 6.5, 2.5, 11, L(S, 0, 1))
    foot = ("M2 21.5V20C2 17.5 3.8 16.5 6 16.5C8.2 16.5 10 17.5 10 20V21.5H8.5C8.5 20 7.5 19 6 19C4.5 19 3.5 20 3.5 21.5Z")
    return [
        shell(union(finial, post, foot)),
        detail(seg(4.75, 11, 7.25, 11)),
        line(seg(7.25, 14, 21.5, 14)),
        line(seg(20, 14, 20, 21.5)),
    ]


@icon("potbelly-stove", CAT, "Round-bellied cast iron wood stove on short legs with a small door and a tall chimney pipe",
      tags=["potbelly stove", "wood stove", "cast iron", "heater", "stove", "cabin"], aliases=["pot-belly-stove"])
def _(S):
    body = union(rect(8, 7, 8, 3, L(S, 0, 1)), circle(12, 13.5, 6), rect(8.5, 17.5, 7, 2.5, L(S, 0, 1)))
    return [
        shell(union(body, rect(10.5, 1.5, 3, 6))),
        detail(rect(9.5, 12, 5, 3.5, rr(S, 1))),
        detail(seg(6.5, 10, 17.5, 10)),
        line(seg(9, 20, 8, 22)), line(seg(15, 20, 16, 22)),
    ]


@icon("tin-bath", CAT, "Oval metal tin bath with a rolled rim and a handle at each end, standing on the floor",
      tags=["tin bath", "tub", "washtub", "galvanized", "bathing", "old fashioned"])
def _(S):
    tub = poly([(4.5, 9), (19.5, 9), (18, 20), (6, 20)], closed=True, r=L(S, 0, 2))
    return [
        shell(union(tub, rect(3, 7.5, 18, 2.5, L(S, 0, 1.25)))),
        detail(seg(4.7, 14, 19.3, 14)),
        line(poly([(4.2, 12), (1.8, 12), (1.8, 15.5), (4, 15.5)], r=S.r)),
        line(poly([(19.8, 12), (22.2, 12), (22.2, 15.5), (20, 15.5)], r=S.r)),
    ]


@icon("snuff-box", CAT, "Small decorated box with its hinged lid slightly open",
      tags=["snuff box", "trinket box", "pill box", "keepsake", "antique", "tobacco"], aliases=["snuffbox"])
def _(S):
    lid = poly([(20.5, 11), (3.5, 7), (4.1, 4.6), (21.1, 8.6)], closed=True, r=L(S, 0, 0.8))
    return [
        shell(rect(3, 12.5, 18, 8, rr(S, 2))),
        shell(lid),
        detail(ellipse(12, 16.5, 3.5, 1.75) if S.name == "rounded" else
               poly([(8.5, 16.5), (12, 14.8), (15.5, 16.5), (12, 18.2)], closed=True)),
    ]


@icon("button-hook", CAT, "Long thin metal hook with a hooked tip and a rounded handle for fastening boot buttons",
      tags=["button hook", "buttonhook", "boot hook", "victorian", "dressing", "tool"], aliases=["buttonhook"])
def _(S):
    handle = path_to_d(ST(seg(4.5, 19.5, 8.5, 15.5), 5, S.cap, S.join))
    return [
        shell(handle),
        line("M10 14L19 5C20.2 3.8 19.8 2 18.3 2C17 2 16.5 3.3 17 4.3"),
    ]


@icon("carpet-bag", CAT, "Boxy soft travel bag of patterned carpet with a metal frame opening and a handle",
      tags=["carpet bag", "carpetbag", "travel bag", "luggage", "doctor bag", "victorian"], aliases=["carpetbag"])
def _(S):
    parts = [
        shell(poly([(3.5, 10), (20.5, 10), (21, 21), (3, 21)], closed=True, r=L(S, 0, 2))),
        shell(rect(3, 8, 18, 2.5, L(S, 0, 1.25))),
        line("M8 8V6.5A4 3.5 0 0 1 16 6.5V8"),
    ]
    for x, y in ((8, 14.5), (12, 14.5), (16, 14.5), (10, 18), (14, 18)):
        parts.append(dot(x, y, 1) if S.name == "rounded" else mark(poly([(x - 1.3, y), (x, y - 1.3), (x + 1.3, y), (x, y + 1.3)], closed=True)))
    return parts


@icon("horse-brass", CAT, "Round decorative brass medallion with a cut-out star hanging from a leather strap",
      tags=["horse brass", "harness", "medallion", "brass", "amulet", "shire horse"])
def _(S):
    star = poly(sum(([polar(12, 15.2, 3.4, -90 + 72 * i), polar(12, 15.2, 1.5, -54 + 72 * i)] for i in range(5)), []),
                closed=True)
    return [
        shell(union(rect(9.5, 2, 5, 8, L(S, 0, 1.5)), circle(12, 15, 6.5))),
        detail(seg(9.7, 8.3, 14.3, 8.3)),
        detail(star),
    ]


# ============================================================================ machines and inventions

@icon("difference-engine", CAT, "Mechanical calculator with columns of stacked number wheels in a frame and a side crank",
      tags=["difference engine", "babbage", "mechanical calculator", "computer history", "analytical engine", "gears"])
def _(S):
    parts = [shell(rect(3, 2.5, 15, 19, rr(S, 2)))]
    for x in (7, 10.5, 14):
        parts.append(detail(seg(x, 2.5, x, 21.5)))
    for x in (7, 10.5, 14):
        for y in (7, 12, 17):
            parts.append(mark(rect(x - 1.25, y - 1, 2.5, 2, L(S, 0, 0.6))))
    parts += [line(poly([(18, 11), (21, 11), (21, 14.5)], r=S.r))]
    return parts


@icon("spinning-jenny", CAT, "Wooden spinning machine with a large drive wheel and a row of upright spindles",
      tags=["spinning jenny", "industrial revolution", "textile", "spinning", "loom", "cotton mill"])
def _(S):
    parts = [
        shell(rect(2, 13, 12, 2.5, L(S, 0, 1.25))),
        line(seg(3.5, 15.5, 3.5, 21.5)), line(seg(12.5, 15.5, 12.5, 21.5)),
        shell(circle(18, 13, 4.25)), dot(18, 13, 1.1),
        line(seg(18, 17.25, 18, 21.5)),
    ]
    for x in (4, 8, 12):
        parts.append(line(seg(x, 4, x, 13)))
        parts.append(mark(ellipse(x, 8.5, 1.4, 2.3) if S.name == "rounded" else rect(x - 1.4, 6.3, 2.8, 4.4)))
    return parts


@icon("aeolipile", CAT, "Hero's steam engine: a hollow sphere with two bent nozzles mounted above a boiling cauldron",
      tags=["aeolipile", "hero engine", "steam turbine", "ancient invention", "steam", "physics"], aliases=["heron-engine"])
def _(S):
    return [
        shell(circle(12, 7.5, 4.5)),
        line(poly([(7.5, 7.5), (4.5, 7.5), (4.5, 4.5)], r=S.r)),
        line(poly([(16.5, 7.5), (19.5, 7.5), (19.5, 10.5)], r=S.r)),
        line(seg(9.5, 11.3, 9.5, 14.5)), line(seg(14.5, 11.3, 14.5, 14.5)),
        shell("M4 14.5H20C20 18.8 16.5 21.5 12 21.5C7.5 21.5 4 18.8 4 14.5Z"),
        detail(seg(4.5, 16.5, 19.5, 16.5)),
    ]


@icon("beam-engine", CAT, "Early steam beam engine: a tall engine house with a rocking beam sticking out of the top",
      tags=["beam engine", "cornish engine", "steam engine", "pumping engine", "industrial revolution", "mine"])
def _(S):
    house = union(rect(3, 9, 11, 12.5, L(S, 0, 1)), rect(3.5, 2, 3, 7))
    return [
        shell(house),
        detail("M7.5 21.5V16.5A2 2 0 0 1 11.5 16.5V21.5"),
        shell(rect(8, 5, 14, 2.5, L(S, 0, 1.25))),
        detail(seg(3, 12, 14, 12)),
        line(seg(20.5, 7.5, 20.5, 21.5)),
        line(seg(17, 21.5, 22.5, 21.5)),
    ]


@icon("clockwork-automaton", CAT, "Small mechanical figure seated at a desk writing, with a winding key in its back",
      tags=["automaton", "clockwork", "mechanical doll", "robot history", "wind up", "android"])
def _(S):
    return [
        shell(circle(9, 5.5, 2.75)),
        shell(poly([(6.5, 9.5), (11.5, 9.5), (12, 16.5), (6, 16.5)], closed=True, r=L(S, 0, 1.2))),
        line(poly([(11.5, 11), (15.5, 12.5)], r=S.r)),
        line(seg(15.5, 12.5, 18, 8.5)),
        shell(rect(13.5, 13.5, 8.5, 2.5, L(S, 0, 1.25))),
        line(seg(20.5, 16, 20.5, 21.5)),
        line(seg(7, 16.5, 7, 21.5)), line(seg(11.5, 16.5, 11.5, 21.5)),
        line(seg(6.5, 12.5, 4, 12.5)),
        shell(union(circle(2.8, 10.9, 1.3), circle(2.8, 14.1, 1.3)) if S.name == "rounded" else
              poly([(1.5, 9.5), (4, 11.5), (4, 13.5), (1.5, 15.5)], closed=True)),
    ]


@icon("barrel-organ", CAT, "Street barrel organ: a wooden box of pipes on a pole with a side crank handle",
      tags=["barrel organ", "hurdy gurdy", "street organ", "organ grinder", "music box", "busker"],
      aliases=["street-organ"])
def _(S):
    parts = [shell(rect(3, 4, 15, 11, rr(S, 2)))]
    for x, top in ((7, 7), (10.5, 8.5), (14, 10)):
        parts.append(detail(seg(x, top, x, 15)))
    parts += [
        line(poly([(18, 9.5), (21, 9.5), (21, 12.5)], r=S.r)),
        line(seg(10.5, 15, 10.5, 21.5)),
        line(seg(7, 21.5, 14, 21.5)),
    ]
    return parts


@icon("antique-microscope", CAT, "Brass microscope with a tall tube on a curved arm, a round mirror and a round base",
      tags=["antique microscope", "brass microscope", "victorian science", "optics", "laboratory", "microscope"])
def _(S):
    return [
        shell(rect(12, 1.5, 4, 9.5, L(S, 0, 1.25))),
        shell(rect(9, 12.5, 10, 2.5, L(S, 0, 1.25))),
        line("M8 19.5C4.5 15.5 5.5 8 12 5.5"),
        shell(circle(14, 17.5, 1.5)),
        shell("M3.5 21.5C3.5 20 7 19 12 19C17 19 20.5 20 20.5 21.5Z" if S.name == "rounded" else
              poly([(3.5, 21.5), (5, 19), (19, 19), (20.5, 21.5)], closed=True)),
    ]


@icon("crank-wall-telephone", CAT, "Wooden wall telephone with two bells, a side crank, a horn mouthpiece and an earpiece on a cord",
      tags=["crank telephone", "wall phone", "magneto phone", "antique phone", "telephone", "vintage"],
      aliases=["magneto-telephone"])
def _(S):
    bells = union("M7.5 6.5V5A2.25 2.25 0 0 1 12 5V6.5Z", "M13 6.5V5A2.25 2.25 0 0 1 17.5 5V6.5Z")
    return [
        shell(union(rect(6.5, 6, 12, 15.5, rr(S, 2)), bells)),
        detail(seg(6.5, 6.5, 18.5, 6.5)),
        detail(seg(12.5, 9.5, 12.5, 12.5)),
        detail(poly([(10, 16.5), (15, 16.5), (13.5, 12.5), (11.5, 12.5)], closed=True, r=S.r * 0.4)),
        line(poly([(18.5, 10), (21.5, 10), (21.5, 13)], r=S.r)),
        shell(rect(1.5, 8, 2.5, 6.5, L(S, 0, 1.25))),
        line("M2.75 14.5V18.5H6.5"),
    ]


@icon("horse-mill", CAT, "Horse walking round a millstone while pulling the long wooden beam that turns it",
      tags=["horse mill", "horse gin", "animal power", "millstone", "grinding", "farm"], aliases=["horse-gin"])
def _(S):
    horse = poly([(2.5, 11.5), (2, 10), (4.2, 6.5), (4.8, 4.8), (6, 6.3), (8.5, 10), (13, 10), (14, 11.5), (14, 14.5),
                  (13.8, 21.5), (12, 21.5), (12, 15.5), (8, 15.5), (7.2, 21.5), (5.5, 21.5), (5.8, 14), (5.5, 11.5),
                  (4, 12)], closed=True, r=S.r * 0.4)
    return [
        shell(horse, stroke_miterlimit="2"),
        shell(rect(16, 16, 6, 5.5, rr(S, 1.5))),
        line(seg(19, 16, 19, 7)),
        line(seg(19, 8, 8.5, 8)),
    ]


# ============================================================================ tournaments and dress

@icon("tournament-pavilion", CAT, "Round striped medieval tent with a peaked roof, a scalloped valance and a pennant",
      tags=["pavilion", "medieval tent", "tournament", "joust", "fair", "camp"])
def _(S):
    rr_ = 1.8
    roof = f"M3 10L12 5L21 10"
    x = 21.0
    for _i in range(5):
        roof += f"A{rr_} {rr_} 0 0 1 {fmt(x - 2 * rr_)} 10"
        x -= 2 * rr_
    roof += "Z"
    return [
        shell(roof, stroke_miterlimit="2"),
        shell(rect(5, 15, 14, 6.5, L(S, 0, 1.5))),
        detail(seg(9.7, 15, 9.7, 21.5)), detail(seg(14.3, 15, 14.3, 21.5)),
        line(seg(12, 5, 12, 1.5)),
        mark(poly([(12, 1), (16.5, 2.3), (12, 3.6)], closed=True)),
    ]


@icon("quintain", CAT, "Jousting practice target: a post with a pivoting arm carrying a shield and a hanging sandbag",
      tags=["quintain", "jousting", "tilting", "medieval", "tournament", "target"])
def _(S):
    shield = ("M2 6.5H9V10C9 12.5 7.3 14.3 5.5 15C3.7 14.3 2 12.5 2 10Z" if S.name == "line" else
              "M2 7.5A1 1 0 0 1 3 6.5H8A1 1 0 0 1 9 7.5V10C9 12.5 7.3 14.3 5.5 15C3.7 14.3 2 12.5 2 10Z")
    bag = "M19.5 11.5C17.8 11.5 17 13.3 17 15.5C17 17.8 18 19 19.5 19C21 19 22 17.8 22 15.5C22 13.3 21.2 11.5 19.5 11.5Z"
    return [
        line(seg(12, 6, 12, 21.5)),
        line(seg(8.5, 21.5, 15.5, 21.5)),
        line(seg(9, 7.4, 20.5, 4.4)),
        shell(shield),
        detail(seg(5.5, 6.5, 5.5, 15)),
        line(seg(19.5, 4.7, 19.5, 11.5)),
        shell(bag),
    ]


@icon("herald-tabard", CAT, "Front view of a herald's short tunic with wide flap sleeves, divided into quarters",
      tags=["tabard", "herald", "heraldry", "tunic", "coat of arms", "medieval"])
def _(S):
    body = poly([(8.5, 3), (15.5, 3), (21.5, 4.5), (21.5, 11), (17.5, 11), (17.5, 21.5), (6.5, 21.5), (6.5, 11), (2.5, 11),
                 (2.5, 4.5)], closed=True, r=L(S, 0, 1.2))
    return [
        shell(body),
        detail("M9.5 3.2A2.5 2.5 0 0 0 14.5 3.2"),
        detail(seg(12, 5.7, 12, 21.5)),
        detail(seg(6.5, 13, 17.5, 13)),
        detail(seg(17.5, 4.5, 17.5, 11)), detail(seg(6.5, 4.5, 6.5, 11)),
    ]


@icon("wimple", CAT, "Front view of a head wrapped in a cloth wimple covering the hair, neck and chin, under a veil",
      tags=["wimple", "veil", "nun", "medieval dress", "headdress", "habit"])
def _(S):
    cloth = "M12 2C7 2 4.5 5.5 4.5 10V16L2.5 21.5H21.5L19.5 16V10C19.5 5.5 17 2 12 2Z"
    face = ellipse(12, 11, 3.5, 4.5) if S.name == "rounded" else \
        "M12 6.5C14.5 6.5 15.5 8.5 15.5 11C15.5 13.5 14 15.5 12 15.5C10 15.5 8.5 13.5 8.5 11C8.5 8.5 9.5 6.5 12 6.5Z"
    return [
        shell(minus(cloth, face)),
        detail("M5.5 17.5Q12 20.5 18.5 17.5"),
        dot(10.5, 10.5, 0.9), dot(13.5, 10.5, 0.9),
    ]


@icon("phrygian-cap", CAT, "Side view of a soft conical cap with its tip flopped forward",
      tags=["phrygian cap", "liberty cap", "bonnet rouge", "freedom", "revolution", "cap"], aliases=["liberty-cap"])
def _(S):
    top = "C5 15 6 13.5 7.5 12L3 13.5C3 7 7.5 3 12.5 3C16.5 3 19 6 19 11"
    cap = ("M5 21.5V17" + top + "V21.5Z" if S.name == "line" else
           "M6.5 21.5A1.5 1.5 0 0 1 5 20V17" + top + "V20A1.5 1.5 0 0 1 17.5 21.5Z")
    return [
        shell(cap, stroke_miterlimit="2"),
        detail("M7.5 12C8.5 9 11 7 14.5 7"),
        detail(seg(5, 17.5, 19, 17.5)),
    ]


# ============================================================================ late additions

@icon("anubis-jackal", CAT, "Side view of a seated jackal statue with tall pointed ears and a long snout",
      tags=["anubis", "egyptian", "jackal", "statue", "guardian", "tomb", "god"])
def _(S):
    pts = [(4, 21.5), (4, 17), (6, 13), (9, 10.5), (9, 6.5), (8.6, 1.8), (11.8, 4.3), (13.5, 4.3), (21, 8), (21, 10),
           (13.5, 10.5), (13.5, 12), (15.5, 13), (15.5, 21.5)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        detail(seg(9, 12, 13.5, 12)),
        detail(seg(11, 16, 11, 21.5)),
    ]


@icon("rushlight-holder", CAT, "Iron stand with a pincer clip holding a slanted rush with a flame at its tip and a weighted arm",
      tags=["rush light", "candle", "lighting", "iron", "medieval", "colonial", "illumination"])
def _(S):
    flame = "M18.5 2C20 3.5 20.5 4.5 20.5 5.3A2 2 0 0 1 16.5 5.3C16.5 4.5 17 3.5 18.5 2Z"
    return [
        shell(rect(7, 19, 10, 2.5, rr(S, 1.25))),
        line(seg(12, 19, 12, 12)),
        line(seg(4.5, 12, 15, 12)),
        shell(circle(3.5, 12, 2.25)),
        line(poly([(14, 9.5), (15, 12), (17.5, 10.5)], r=S.r)),
        line(seg(15, 11.5, 18, 7.5)),
        shell(flame),
    ]


@icon("powdered-wig", CAT, "Front view of a white powdered wig with rows of rolled curls beside the face",
      tags=["wig", "periwig", "judge", "georgian", "18th century", "barrister", "formal"], aliases=["periwig"])
def _(S):
    dome = "M4 12C4 6 7.5 2.5 12 2.5C16.5 2.5 20 6 20 12Z"
    face = ellipse(12, 15, 3.4, 4.6) if S.name == "rounded" else \
        "M12 10.4C14.6 10.4 15.4 12.5 15.4 15C15.4 17.5 14 19.6 12 19.6C10 19.6 8.6 17.5 8.6 15C8.6 12.5 9.4 10.4 12 10.4Z"

    def curl(cx, cy):
        return circle(cx, cy, 2.25) if S.name == "rounded" else rect(cx - 2, cy - 2, 4, 4, 0.5)

    return [
        shell(dome),
        shell(curl(5.5, 14.75)), shell(curl(5.5, 19.75)),
        shell(curl(18.5, 14.75)), shell(curl(18.5, 19.75)),
        detail(face),
    ]
