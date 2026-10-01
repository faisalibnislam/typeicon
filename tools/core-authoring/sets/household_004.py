"""TypeIcon Core: household (batch household_004): bath and body care, personal grooming, shaving and hair tools.

Original drawings of generic personal-care objects. Bodies are shells, inner marks are details
(knocked out in Filled), small fittings are dots.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import LINE, I, fmt, path_to_d, polar

CAT = "household"


def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def mark(d) -> Part:
    return Part("dot", d)


def scallops(cx, cy, R, n, rad, start=-90.0):
    """Closed scalloped outline: n bumps of radius rad around a circle of radius R."""
    pts = [polar(cx, cy, R, start + i * 360 / n) for i in range(n)]
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(1, n + 1):
        p = pts[i % n]
        d += f"A{fmt(rad)} {fmt(rad)} 0 0 1 {fmt(p[0])} {fmt(p[1])}"
    return d + "Z"


def tilted_ellipse(cx, cy, rx, ry, deg):
    """Ellipse whose long axis is turned clockwise by deg."""
    a = math.radians(deg)
    dx, dy = rx * math.cos(a), rx * math.sin(a)
    return (f"M{fmt(cx - dx)} {fmt(cy - dy)}A{fmt(rx)} {fmt(ry)} {fmt(deg)} 1 1 {fmt(cx + dx)} {fmt(cy + dy)}"
            f"A{fmt(rx)} {fmt(ry)} {fmt(deg)} 1 1 {fmt(cx - dx)} {fmt(cy - dy)}Z")


def rot(pts, deg, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c) for x, y in pts]


def rp(pts, deg, closed=True, r=0.0):
    return poly(rot(pts, deg), closed=closed, r=r)


def rseg(x1, y1, x2, y2, deg):
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg)
    return seg(a, b, c, d)


def union_d(*ds):
    """Outline of the union of closed shapes (for overlapping pebbles and the like)."""
    return path_to_d(U(*[P(d) for d in ds]))


# ============================================================================ bath and body

@icon("back-scrubber", CAT, "Long curved handle ending in an oval bristle brush head",
      tags=["back brush", "bath brush", "long handle brush", "shower", "bathing", "body scrub"])
def _(S):
    return [
        shell(tilted_ellipse(15.5, 8.5, 7, 4.25, 45)),
        dot(12.75, 11.25, 1), dot(15.5, 8.5, 1), dot(18.25, 5.75, 1),
        line("M3.5 20.5C3.75 16 6 12.5 9.5 11.25"),
    ]


@icon("body-brush", CAT, "Dry body brush seen from the side with a strap handle on top and rows of bristles below",
      tags=["dry brushing", "skin brush", "massage brush", "exfoliation", "bath brush", "spa"])
def _(S):
    return [
        line("M6.5 9C6.5 3 17.5 3 17.5 9"),
        shell(rect(3, 9, 18, 4.5, rr(S, 2))),
        line(seg(6, 14, 6, 20.5)), line(seg(10, 14, 10, 20.5)), line(seg(14, 14, 14, 20.5)), line(seg(18, 14, 18, 20.5)),
    ]


@icon("loofah", CAT, "Cylindrical natural loofah with a mesh texture and a hanging loop",
      tags=["luffa", "bath sponge", "exfoliating", "scrubber", "shower", "natural sponge"])
def _(S):
    return [
        line(poly([(15, 9.5), (15, 4.5), (19, 4.5), (19, 9.5)], r=S.r)),
        shell(rect(3, 9.5, 18, 11.5, rr(S, 5))),
        detail(seg(8.5, 12.5, 7, 18)),
        detail(seg(13.5, 12.5, 12, 18)),
        detail(seg(18, 12.5, 16.5, 18)),
    ]


@icon("bath-pouf", CAT, "Round ruffled mesh bath pouf with a string loop on top",
      tags=["shower puff", "mesh sponge", "body puff", "bath flower", "scrubber", "bathing"])
def _(S):
    loop = poly([(10.25, 7.5), (10.25, 3.5), (13.75, 3.5), (13.75, 7.5)], r=0.5) if S.name == "line" else ellipse(12, 5, 1.75, 2.4)
    inner = poly(regular(12, 14, 2.4, 4), closed=True) if S.name == "line" else circle(12, 14, 2)
    return [
        shell(scallops(12, 14.5, 5, 7, 2.5)),
        detail(inner),
        line(loop),
    ]


@icon("bath-sponge", CAT, "Irregular round natural sea sponge full of holes of different sizes",
      tags=["sea sponge", "natural sponge", "bathing", "washing", "porous", "body wash"])
def _(S):
    return [
        shell("M6 8C6 4.5 10 3 13 4C17 3 20 6 19.5 10C21.5 13 20 18 16.5 19.5C13.5 21.5 8 20.5 6 17.5C3 15 3.5 10 6 8Z"),
        *([sq(9, 7.5, 2.4, 2.4), sq(14.75, 7.25, 1.8, 1.8), sq(11.5, 12, 3, 3), sq(7.75, 13.75, 1.8, 1.8), sq(15.75, 14.25, 2, 2)]
          if S.name == "line" else
          [dot(10, 8.5, 1.25), dot(15.5, 8, 1), dot(12.5, 13, 1.5), dot(8.5, 14.5, 1), dot(16.5, 15, 1.1)]),
    ]


@icon("exfoliating-mitt", CAT, "Bath mitt with a thumb and a ribbed scrubbing surface",
      tags=["bath glove", "scrub mitt", "kessa", "exfoliation", "body scrub", "shower glove"])
def _(S):
    body = poly([(7.5, 21.5), (7.5, 17), (3.5, 13), (5.5, 10.5), (7.5, 12.5), (7.5, 8), (9.5, 4.5), (16.5, 4.5),
                 (18.5, 8), (18.5, 21.5)], closed=True, r=S.r * 1.3)
    return [
        shell(body),
        detail(seg(11, 10.5, 15, 10.5)),
        detail(seg(11, 14.5, 15, 14.5)),
        detail(seg(11, 18.5, 15, 18.5)),
    ]


@icon("washcloth", CAT, "Square face cloth folded in quarters with a small hanging loop",
      tags=["flannel", "face cloth", "wash rag", "facecloth", "bath linen", "towel"])
def _(S):
    return [
        line(poly([(16, 7.5), (16, 4), (19.5, 4), (19.5, 7.5)], r=S.r * 0.5)),
        shell(rect(3.5, 7.5, 17, 13.5, rr(S, 2))),
        detail(poly([(3.5, 14.5), (11, 14.5), (11, 21)])),
    ]


@icon("bathrobe", CAT, "Wrap bathrobe with a V neckline, wide sleeves and a belt at the waist",
      tags=["dressing gown", "robe", "spa robe", "hotel robe", "housecoat", "loungewear"])
def _(S):
    body = poly([(9, 3.5), (15, 3.5), (20, 6), (21.5, 14.5), (17.5, 14.5), (17.5, 21.5), (6.5, 21.5), (6.5, 14.5),
                 (2.5, 14.5), (4, 6)], closed=True, r=S.r)
    return [
        shell(body),
        detail(poly([(9.5, 4), (12, 11.5), (14.5, 4)])),
        detail(seg(6.5, 17, 17.5, 17)),
        detail(seg(17.5, 14.5, 17.5, 10)),
        detail(seg(6.5, 14.5, 6.5, 10)),
    ]


@icon("shower-cap", CAT, "Elastic shower cap with a domed top and a gathered frilly edge",
      tags=["bath cap", "hair cover", "hair protection", "bathing", "waterproof", "hotel amenity"])
def _(S):
    d = "M3.5 15.5C3.5 8 7 4.5 12 4.5C17 4.5 20.5 8 20.5 15.5"
    n = 4
    w = 17 / n
    for i in range(n):
        x = 20.5 - w * (i + 1)
        d += f"A{fmt(w / 2)} {fmt(w / 2)} 0 0 1 {fmt(x)} 15.5"
    return [
        shell(d + "Z"),
        detail("M5 11.5Q12 9 19 11.5"),
    ]


@icon("hair-towel-wrap", CAT, "Head with a towel wrapped around the hair and twisted on top like a turban",
      tags=["hair turban", "towel turban", "after shower", "hair drying", "spa", "head towel"])
def _(S):
    return [
        shell("M4.5 12.5C4.5 8.5 7 6.5 10.5 5.75C10 3.5 12 2.5 13.5 3.25C15 4 14.5 5.5 14 5.75C17.5 6.5 19.5 9 19.5 12.5Z"),
        detail("M7.5 11.5Q9 8.5 14 7.5"),
        line("M6.5 12.5V15A5.5 5.5 0 0 0 17.5 15V12.5"),
        dot(9.5, 16.25, 1), dot(14.5, 16.25, 1),
    ]


@icon("hooded-baby-towel", CAT, "Square baby towel with a round hood showing two small ears",
      tags=["baby towel", "hooded towel", "bath time", "newborn", "infant bath", "bear towel"])
def _(S):
    body = "M3.5 21.5V10.5H7.5V8A4.5 4.5 0 0 1 16.5 8V10.5H20.5V21.5Z"
    return [
        shell(body),
        detail("M7.5 10.5Q12 15.5 16.5 10.5"),
        dot(7.5, 4.75, 1.5), dot(16.5, 4.75, 1.5),
    ]


@icon("sanitary-pad", CAT, "Menstrual pad seen from above with wings on both sides and a centre stripe",
      tags=["period pad", "sanitary towel", "menstrual pad", "feminine hygiene", "period", "panty liner"])
def _(S):
    body = poly([(9, 2.5), (15, 2.5), (17, 4.5), (17, 9), (20.5, 10), (20.5, 14), (17, 15), (17, 19.5), (15, 21.5),
                 (9, 21.5), (7, 19.5), (7, 15), (3.5, 14), (3.5, 10), (7, 9), (7, 4.5)], closed=True, r=S.r)
    return [
        shell(body),
        detail(seg(12, 6.5, 12, 17.5)),
    ]


@icon("tampon", CAT, "Cylindrical tampon with a rounded tip and a withdrawal string at the other end",
      tags=["period", "menstrual", "feminine hygiene", "sanitary", "applicator", "string"])
def _(S):
    top = "M8.5 8A3.5 3.5 0 0 1 15.5 8" if S.name == "rounded" else "M8.5 8L10.5 3.5H13.5L15.5 8"
    return [
        shell(top + "V16H8.5Z"),
        detail(seg(8.5, 12, 15.5, 12)),
        line("M12 16V18Q12 21.5 15 21.5"),
    ]


@icon("menstrual-cup", CAT, "Bell-shaped menstrual cup with a short stem and a ring at the bottom",
      tags=["period cup", "reusable period", "feminine hygiene", "silicone cup", "eco", "sustainable period"])
def _(S):
    if S.name == "rounded":
        cup = "M7 4H17A2 2 0 0 1 19 6C19 11.5 16 15.5 12 15.5C8 15.5 5 11.5 5 6A2 2 0 0 1 7 4Z"
    else:
        cup = "M5 4H19C19 11.5 16 15.5 12 15.5C8 15.5 5 11.5 5 4Z"
    return [
        shell(cup),
        detail(seg(5.5, 8.5, 18.5, 8.5)),
        line(seg(12, 15.5, 12, 19)),
        dot(12, 20.5, 1.4),
    ]


@icon("diaper", CAT, "Front of a disposable diaper with leg openings and fastening tabs at the waist",
      tags=["nappy", "baby", "infant", "changing", "toddler", "disposable"])
def _(S):
    body = "M3.5 5H20.5V10C20.5 14.5 16 15.5 15.5 21H8.5C8 15.5 3.5 14.5 3.5 10Z"
    if S.name == "rounded":
        body = "M5.5 5H18.5A2 2 0 0 1 20.5 7V10C20.5 14.5 16 15.5 15.5 21H8.5C8 15.5 3.5 14.5 3.5 10V7A2 2 0 0 1 5.5 5Z"
    return [
        shell(body),
        detail(seg(3.5, 9, 7, 9)),
        detail(seg(17, 9, 20.5, 9)),
    ]


@icon("baby-wipes", CAT, "Soft pack of wipes with a raised lid slot and a small baby face on the front",
      tags=["wet wipes", "wet tissues", "nappy change", "baby care", "cleaning wipes", "tissue pack"])
def _(S):
    body = poly([(3.5, 21.5), (3.5, 10), (7, 10), (7, 4.5), (17, 4.5), (17, 10), (20.5, 10), (20.5, 21.5)], closed=True, r=S.r)
    return [
        shell(body),
        detail(seg(10, 7.5, 14, 7.5)),
        dot(9.5, 15, 1), dot(14.5, 15, 1),
        detail("M9.5 17.75Q12 19.75 14.5 17.75"),
    ]


@icon("baby-powder", CAT, "Talc shaker bottle with a holed cap and a few specks of powder puffing out",
      tags=["talc", "talcum powder", "body powder", "nappy rash", "baby care", "shaker"])
def _(S):
    body = poly([(4.5, 21.5), (4.5, 11), (7, 9), (7, 4.5), (13, 4.5), (13, 9), (15.5, 11), (15.5, 21.5)], closed=True, r=S.r)
    return [
        shell(body),
        dot(9, 6.75, 0.8), dot(11, 6.75, 0.8),
        detail(seg(8, 14, 12, 14)),
        detail(seg(8, 17.5, 12, 17.5)),
        dot(18, 4.5, 1.1), dot(20.5, 7, 1.1), dot(18, 8.5, 1.1),
    ]


@icon("contact-lens", CAT, "Thin curved contact lens dome with a drop of solution beneath it",
      tags=["contacts", "eye care", "vision", "optical", "soft lens", "saline"])
def _(S):
    return [
        shell("M3 10C3 3 21 3 21 10A9 3 0 0 1 3 10Z"),
        detail("M7.5 10A4.5 1.5 0 0 0 16.5 10"),
        shell("M12 14.5C10 17 9.5 18.25 9.5 19.25A2.5 2.5 0 0 0 14.5 19.25C14.5 18.25 14 17 12 14.5Z"),
    ]


@icon("contact-lens-case", CAT, "Top view of a contact lens case with two round screw caps",
      tags=["lens case", "contacts", "eye care", "storage", "travel case", "optician"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 19, 13, L(S, 2, 6))),
        detail(circle(8, 12, 2.4)),
        detail(circle(16, 12, 2.4)),
    ]


@icon("earplugs", CAT, "Pair of foam earplugs, each with a rounded head and a short stem",
      tags=["ear plugs", "noise cancelling", "sleep aid", "hearing protection", "quiet", "foam plugs"])
def _(S):
    def plug(cx):
        return poly([(cx - 3.5, 13), (cx - 3.5, 7.5), (cx - 2, 4.5), (cx + 2, 4.5), (cx + 3.5, 7.5), (cx + 3.5, 13), (cx + 1.5, 13),
                     (cx + 1.5, 21), (cx - 1.5, 21), (cx - 1.5, 13)], closed=True, r=S.r * 1.6)
    return [shell(plug(6.75)), shell(plug(17.25))]


@icon("ear-cleaning", CAT, "Ear outline with a cotton swab pointing at the ear opening",
      tags=["cotton swab", "cotton bud", "earwax", "hygiene", "ear care"])
def _(S):
    return [
        line("M12 13V8.5A5 5 0 0 1 22 8.5C22 13 18.5 13.5 18.5 17.5A3.5 3.5 0 0 1 12 19"),
        line("M15.5 9.5A2 2 0 0 1 18.5 9.5C18.5 11.5 16.5 11.5 16.5 13.5"),
        line(seg(2.5, 21.5, 7, 17)),
        shell(tilted_ellipse(9, 15, 3, 1.75, -45)),
    ]


@icon("neti-pot", CAT, "Small teapot-like nasal rinse pot with a handle and a long narrow spout",
      tags=["nasal rinse", "sinus rinse", "nose wash", "saline", "allergy", "congestion"])
def _(S):
    body = poly([(7.5, 10), (16.5, 10), (17.5, 17.5), (15.5, 21), (8.5, 21), (6.5, 17.5)], closed=True, r=S.r * 1.6)
    return [
        shell(body),
        line("M16.75 12.5H19.5A2.5 2.5 0 0 1 19.5 18H17.25"),
        line("M7 15L3 8"),
        line(seg(9.5, 6.5, 14.5, 6.5)),
        line(seg(12, 6.5, 12, 10)),
    ]


@icon("hot-water-bottle", CAT, "Rubber hot water bottle with wavy ribs and a screw stopper at the neck",
      tags=["heat pack", "bed warmer", "cramp relief", "warm", "winter", "pain relief"])
def _(S):
    body = poly([(10, 7.5), (14, 7.5), (14, 9.5), (20, 13.5), (20, 19), (17.5, 21.5), (6.5, 21.5), (4, 19), (4, 13.5), (10, 9.5)],
                closed=True, r=S.r * 1.5)
    return [
        shell(body),
        line("M10 7.5V3H14V7.5"),
        detail("M6 14.5Q9 12.5 12 14.5T18 14.5"),
        detail("M6 18.5Q9 16.5 12 18.5T18 18.5"),
    ]


@icon("foot-spa", CAT, "Basin of bubbling water with massage rollers along its floor",
      tags=["foot bath", "foot massager", "pedicure", "relax", "spa tub", "foot soak"])
def _(S):
    body = poly([(3, 10.5), (21, 10.5), (19, 19), (18.4, 21), (5.6, 21), (5, 19)], closed=True, r=S.r)
    return [
        shell(body),
        dot(8.5, 16.5, 1.3), dot(12, 16.5, 1.3), dot(15.5, 16.5, 1.3),
        line(circle(8, 6.5, 1.5)), line(circle(13, 4.5, 1.75)), line(circle(17, 7, 1.25)),
    ]


@icon("massage-gun", CAT, "Percussive massage gun shaped like a T with a round head on a short arm",
      tags=["percussion massager", "muscle recovery", "deep tissue", "sports recovery", "physio", "vibration"])
def _(S):
    body = poly([(10, 4.5), (21, 4.5), (21, 11), (18, 11), (18, 21.5), (12, 21.5), (12, 11), (10, 11)], closed=True, r=S.r)
    return [
        shell(body),
        line(seg(10, 7.75, 8, 7.75)),
        solid(circle(5.5, 7.75, 3)),
        dot(16, 7.75, 1),
    ]


@icon("face-roller", CAT, "Facial roller with a large stone roller on one end and a small one on the other",
      tags=["jade roller", "facial massage", "skincare", "beauty", "lymphatic", "rose quartz"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 6, rr(S, 3))),
        line(seg(12, 8.5, 12, 15.5)),
        shell(rect(8.5, 15.5, 7, 6, rr(S, 3))),
    ]


@icon("gua-sha", CAT, "Flat heart-shaped gua sha stone with a notched top edge and a curved scraping edge",
      tags=["facial stone", "scraping tool", "skincare", "jade", "facial massage", "beauty"])
def _(S):
    notch = "C9.5 6.75 10.5 9 12 9C13.5 9 14.5 6.75 17.5 6" if S.name == "rounded" else "L12 9.5L17.5 6"
    return [
        shell("M3 9C3 6.5 4.5 5.5 6.5 6" + notch + "C19.5 5.5 21 6.5 21 9C21 15.5 16.5 20.5 12 20.5C7.5 20.5 3 15.5 3 9Z"),
    ]


@icon("derma-roller", CAT, "Small handheld roller with a spiked cylinder head",
      tags=["microneedling", "skincare", "needle roller", "beauty", "facial", "collagen"])
def _(S):
    return [
        shell(rect(3.5, 3.5, 17, 8, rr(S, 3))),
        dot(7, 7.5, 1), dot(10.5, 7.5, 1), dot(14, 7.5, 1), dot(17.5, 7.5, 1),
        line(seg(12, 11.5, 12, 14)),
        shell(rect(9.5, 14, 5, 7.5, rr(S, 2.5))),
    ]


@icon("hand-washing", CAT, "Tap running over a pair of hands rubbing together with soap bubbles",
      tags=["wash hands", "hygiene", "soap", "handwash", "sanitise", "clean hands"])
def _(S):
    return [
        line("M20 3.5H11.5A2.5 2.5 0 0 0 9 6V8"),
        line(seg(9, 10, 9, 11.5)),
        shell("M3.5 13.5H20.5C20.5 18 17 21.5 12 21.5C7 21.5 3.5 18 3.5 13.5Z"),
        detail(seg(12, 13.5, 12, 19)),
        line(circle(16.5, 8, 1.75)),
    ]


@icon("face-washing", CAT, "Face with closed eyes above a pair of cupped hands throwing up water",
      tags=["wash face", "splash water", "cleansing", "morning routine", "skincare", "facial wash"])
def _(S):
    return [
        shell(circle(12, 8, 5.5)),
        dot(9.75, 7.5, 1), dot(14.25, 7.5, 1),
        line("M3.5 15.5C3.5 19.5 7 21.5 12 21.5C17 21.5 20.5 19.5 20.5 15.5"),
        dot(4, 10, 1.1), dot(20, 10, 1.1),
    ]


# ============================================================================ spa and relaxation

@icon("toiletry-bag", CAT, "Zip-up toiletry bag hanging from a hook with pockets on its front",
      tags=["wash bag", "travel bag", "cosmetic bag", "hanging organiser", "packing"])
def _(S):
    return [
        line("M12 8V4.5A2.25 2.25 0 1 0 7.5 4.5"),
        shell(rect(4, 8, 16, 13.5, rr(S, 3))),
        detail(seg(4, 13, 20, 13)),
        detail(seg(12, 13, 12, 21.5)),
    ]


@icon("travel-bottles", CAT, "Three small travel size bottles of different heights inside a clear zip pouch",
      tags=["toiletries", "liquids bag", "carry-on", "tsa", "mini bottles", "packing"])
def _(S):
    def bottle(x, top, w=3.5):
        nx = x + w / 2
        return Part("dot", poly([(nx - 0.9, top), (nx + 0.9, top), (nx + 0.9, top + 1.5), (x + w, top + 2.5), (x + w, 18.5), (x, 18.5),
                                 (x, top + 2.5), (nx - 0.9, top + 1.5)], closed=True))
    return [
        shell(rect(2.5, 5.5, 19, 16, rr(S, 2.5))),
        detail(seg(2.5, 8.5, 21.5, 8.5)),
        bottle(5, 10.5), bottle(10.25, 11.5, 3.5), bottle(15.5, 12.5),
    ]


@icon("condom", CAT, "Square foil condom wrapper with serrated side edges and a round ring shape in the middle",
      tags=["contraceptive", "protection", "safe sex", "sexual health", "wrapper", "birth control"])
def _(S):
    pts = [(4.75, 3.5), (19.25, 3.5), (21, 6.5), (19.25, 9.5), (21, 12.5), (19.25, 15.5), (21, 18.5), (19.25, 21.5),
           (4.75, 21.5), (3, 18.5), (4.75, 15.5), (3, 12.5), (4.75, 9.5), (3, 6.5)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.5)),
        detail(circle(12, 12.5, 3.75)),
    ]


@icon("sleep-mask", CAT, "Eye mask with two curved closed-eye lines on its front",
      tags=["eye mask", "blindfold", "sleeping", "travel", "nap", "bedtime"])
def _(S):
    return [
        shell("M3 10C3 7 6 6 9 6.5C10.5 6.8 11 7.75 12 7.75C13 7.75 13.5 6.8 15 6.5C18 6 21 7 21 10C21 14.5 17.5 17 14.5 17C13 17 12.75 15.5 12 15.5C11.25 15.5 11 17 9.5 17C6.5 17 3 14.5 3 10Z"),
        detail("M6 11Q8 13.5 10 11"),
        detail("M14 11Q16 13.5 18 11"),
    ]


@icon("massage-stones", CAT, "Stack of three smooth flat stones balanced on each other",
      tags=["hot stones", "spa stones", "cairn", "zen", "balance", "stone therapy"])
def _(S):
    k = L(S, 0.5, 0)
    e1, e2, e3 = ellipse(12, 17.5, 8.5, 3.75 - k), ellipse(12, 12, 6.25, 3.25 - k), ellipse(12, 7, 4, 2.75 - k)
    return [
        shell(union_d(e1, e2, e3)),
        detail("M5.75 12A6.25 3.25 0 0 0 18.25 12"),
        detail("M8 7A4 2.75 0 0 0 16 7"),
    ]


@icon("essential-oil", CAT, "Small bottle with a dropper cap and a leaf on the label",
      tags=["aromatherapy", "oil dropper", "fragrance oil", "herbal", "natural remedy", "serum"])
def _(S):
    body = poly([(6.5, 21.5), (6.5, 11), (9, 9), (9, 7), (10.5, 7), (10.5, 3), (13.5, 3), (13.5, 7), (15, 7), (15, 9), (17.5, 11), (17.5, 21.5)],
                closed=True, r=S.r)
    return [
        shell(body),
        mark("M9.5 19C9.5 14.5 12 13.75 14.5 13.5C14.5 17 13 19 9.5 19Z"),
    ]


@icon("massage-table", CAT, "Folding massage table with a padded top, crossed legs and a headrest at one end",
      tags=["spa bed", "treatment table", "massage bed", "therapy", "physio", "portable table"])
def _(S):
    top = poly([(2.5, 9.5), (16, 9.5), (16, 6.5), (21.5, 6.5), (21.5, 12), (2.5, 12)], closed=True, r=S.r)
    return [
        shell(top),
        line(seg(6, 12, 18, 21.5)),
        line(seg(18, 12, 6, 21.5)),
    ]


@icon("aroma-oil-burner", CAT, "Ceramic oil burner with a bowl on top, a tea light in the base and scent curling upward",
      tags=["oil diffuser", "aromatherapy", "tea light", "fragrance", "scented oil", "wax melt"])
def _(S):
    return [
        line("M9 2.5C7.5 4 10.5 5 9 6.5"),
        line("M15 2.5C13.5 4 16.5 5 15 6.5"),
        shell("M5.5 9H18.5C18.5 12.5 15.5 14.25 12 14.25C8.5 14.25 5.5 12.5 5.5 9Z"),
        line(seg(12, 14.25, 12, 16.5)),
        shell(poly([(8.5, 16.5), (15.5, 16.5), (18, 21.5), (6, 21.5)], closed=True, r=S.r)),
        mark("M12 18C10.75 19.25 10.75 20.25 12 20.5C13.25 20.25 13.25 19.25 12 18Z"),
    ]


@icon("hot-towel", CAT, "Rolled towel showing its spiral end, with steam rising from it",
      tags=["steaming towel", "spa towel", "barber", "warm towel", "facial towel", "rolled towel"])
def _(S):
    return [
        line("M10 2.5C8.5 4 11.5 5 10 6.5"),
        line("M16 2.5C14.5 4 17.5 5 16 6.5"),
        shell(union_d(rect(7, 10, 14, 11, L(S, 2, 4)), ellipse(7, 15.5, 3.5, 5.5))),
        detail(circle(7, 15.5, 1.5)),
        detail(seg(15, 10, 15, 21)),
    ]


@icon("cucumber-eye-mask", CAT, "Face with a cucumber slice over each eye and a band across the forehead",
      tags=["spa face", "eye cooling", "facial", "puffy eyes", "relaxation", "beauty treatment"])
def _(S):
    return [
        shell(ellipse(12, 12.5, 8.5, 9)),
        detail("M6 7Q12 4 18 7"),
        dot(8.5, 11.5, 2.3), dot(15.5, 11.5, 2.3),
        detail("M9.5 17Q12 18.5 14.5 17"),
    ]


@icon("tanning-bed", CAT, "Sun lounger style tanning bed with a pillow end and a sun with rays above it",
      tags=["sunbed", "solarium", "tanning booth", "uv bed", "beauty salon", "tan"])
def _(S):
    rays = []
    for a in range(0, 360, 45):
        p1, p2 = pt_on(16.5, 7.5, 4.25, a), pt_on(16.5, 7.5, 5.75, a)
        rays.append(line(seg(p1[0], p1[1], p2[0], p2[1])))
    return [
        shell(circle(16.5, 7.5, 2)),
        *rays,
        shell(poly([(2.5, 11.5), (8, 11.5), (8, 14.5), (21.5, 14.5), (21.5, 18.5), (2.5, 18.5)], closed=True, r=S.r)),
        line(seg(5, 18.5, 5, 21.5)),
        line(seg(19, 18.5, 19, 21.5)),
    ]


@icon("facial-steamer", CAT, "Tabletop facial steamer with a round base, a bent arm and a nozzle releasing steam",
      tags=["face steamer", "skincare", "pore cleansing", "spa", "humidifier", "beauty device"])
def _(S):
    return [
        shell(rect(3.5, 12.5, 10, 9, rr(S, 4))),
        line("M8.5 12.5V6.5H15.5"),
        shell(poly([(15.5, 4.5), (19.5, 3.5), (19.5, 9.5), (15.5, 8.5)], closed=True, r=S.r * 0.5)),
        line("M16 13C14.5 14.25 17.5 15.5 16 17"),
        line("M20 12C18.5 13.25 21.5 14.5 20 16"),
    ]


@icon("pore-strip", CAT, "Butterfly-shaped nose strip with a narrow bridge and two flared wings",
      tags=["nose strip", "blackhead remover", "skincare", "facial", "cleansing", "beauty"])
def _(S):
    return [
        shell("M3 9C3 7 4.5 6.75 6.5 7.75L9.5 9.5H14.5L17.5 7.75C19.5 6.75 21 7 21 9V15C21 17 19.5 17.25 17.5 16.25L14.5 14.5H9.5L6.5 16.25C4.5 17.25 3 17 3 15Z"),
        detail(seg(6.25, 10.5, 6.25, 13.5)),
        detail(seg(17.75, 10.5, 17.75, 13.5)),
    ]


@icon("eye-patches", CAT, "Pair of crescent-shaped under-eye gel patches",
      tags=["under eye masks", "eye gel pads", "dark circles", "skincare", "beauty", "puffiness"])
def _(S):
    return [
        shell("M3 7.5C3.5 17.5 9.5 17.5 10 7.5C8.5 12 4.5 12 3 7.5Z"),
        shell("M14 7.5C14.5 17.5 20.5 17.5 21 7.5C19.5 12 15.5 12 14 7.5Z"),
    ]


@icon("cartridge-razor", CAT, "Disposable razor with a wide blade cartridge head angled from a long handle",
      tags=["razor", "disposable razor", "shaving", "multi-blade", "hair removal", "grooming"])
def _(S):
    T = 38
    head = rp([(6, 4), (18, 4), (18, 8.5), (13.5, 8.5), (13.5, 20.5), (10.5, 20.5), (10.5, 8.5), (6, 8.5)], T, r=S.r)
    return [
        shell(head),
        detail(rseg(8.5, 6.25, 15.5, 6.25, T)),
    ]


@icon("straight-razor", CAT, "Open straight razor with its blade swung out in line with the handle",
      tags=["cut-throat razor", "barber razor", "shaving", "barbershop", "blade", "grooming"])
def _(S):
    T = 40
    blade = rp([(10, 2.5), (14.5, 4.5), (14.5, 13), (10, 13)], T, r=S.r * 0.4)
    handle = rp([(10, 15.5), (14.5, 15.5), (14.5, 21.5), (10, 21.5)], T, r=S.r)
    c = rot([(12.25, 18)], T)[0]
    return [shell(blade, stroke_miterlimit="2"), shell(handle), dot(c[0], c[1], 1)]


@icon("razor-blade", CAT, "Double-edge razor blade, a thin rectangle with notched ends and a slot through its middle",
      tags=["safety razor blade", "shaving blade", "replacement blade", "sharp", "grooming", "steel"])
def _(S):
    blade = poly([(2.5, 6.5), (21.5, 6.5), (21.5, 10), (19.5, 10), (19.5, 14), (21.5, 14), (21.5, 17.5), (2.5, 17.5), (2.5, 14),
                  (4.5, 14), (4.5, 10), (2.5, 10)], closed=True, r=S.r * 0.6)
    return [
        shell(blade),
        detail(seg(8, 12, 16, 12)),
    ]


@icon("electric-shaver", CAT, "Electric foil shaver with a wide head, foil lines and a power button on the body",
      tags=["foil shaver", "electric razor", "shaving", "grooming", "men's care", "trimmer"])
def _(S):
    body = poly([(5.5, 2.5), (18.5, 2.5), (18.5, 8), (16.5, 8), (16.5, 21.5), (7.5, 21.5), (7.5, 8), (5.5, 8)], closed=True, r=S.r)
    return [
        shell(body),
        detail(seg(8.5, 5.25, 15.5, 5.25)),
        dot(12, 13, 1.25),
    ]


@icon("rotary-shaver", CAT, "Electric shaver with three round rotating heads arranged in a triangle",
      tags=["rotary razor", "electric razor", "shaving", "grooming", "triple head", "trimmer"])
def _(S):
    return [
        shell(union_d(circle(7.5, 6.75, 4.25), circle(16.5, 6.75, 4.25), circle(12, 12.25, 4.25))),
        detail(circle(7.5, 6.75, 1.25)), detail(circle(16.5, 6.75, 1.25)), detail(circle(12, 12.25, 1.25)),
        shell(rect(8.5, 18, 7, 3.5, rr(S, 1.75))),
    ]


@icon("shaving-brush", CAT, "Shaving brush with a fat dome of bristles on a bulbous handle",
      tags=["lather brush", "badger brush", "wet shave", "barber", "shaving", "grooming"])
def _(S):
    return [
        shell("M5.5 11.5C5.5 3.5 18.5 3.5 18.5 11.5H15V13.5C16.75 15 16.75 17.5 15.75 19.5L15.25 21.5H8.75L8.25 19.5C7.25 17.5 7.25 15 9 13.5V11.5Z"),
        detail(seg(9.5, 7.5, 9.5, 9.5)),
        detail(seg(14.5, 7.5, 14.5, 9.5)),
    ]


@icon("shaving-cream", CAT, "Tall aerosol can of shaving cream with a swirl of foam on its nozzle",
      tags=["shaving foam", "shaving gel", "lather", "aerosol", "grooming", "wet shave"])
def _(S):
    can = poly([(7.5, 21.5), (7.5, 12), (9.5, 10), (10.5, 10), (10.5, 8.5), (13.5, 8.5), (13.5, 10), (14.5, 10), (16.5, 12), (16.5, 21.5)],
               closed=True, r=S.r)
    return [
        shell(can),
        shell("M7.5 7.25C4.5 7.25 4.5 3.5 8 3.5C8.5 1.75 12 1.75 12.75 3.25C16 2.75 18 6.75 15.75 7.25Z"),
        detail(seg(7.5, 15, 16.5, 15)),
    ]


@icon("shaving-bowl", CAT, "Shallow bowl heaped with shaving foam and a brush resting in it",
      tags=["lather bowl", "shaving soap", "wet shave", "barber", "grooming", "foam"])
def _(S):
    return [
        shell("M3 14.5H21C21 18.75 17 21 12 21C7 21 3 18.75 3 14.5Z"),
        line("M5.5 14.5C3.75 10.5 7.5 8.5 9.5 10.25C10.5 7.5 14.5 7.5 15.25 10C17.75 9.25 19.75 12.25 18.5 14.5"),
        line(seg(21.5, 2.75, 17.25, 7)),
        shell(tilted_ellipse(15.25, 9, 2.75, 1.75, -45)),
    ]


@icon("beard-trimmer", CAT, "Slim beard trimmer with a toothed comb guard on its head",
      tags=["beard shaper", "facial hair", "grooming", "stubble", "electric trimmer", "men's care"])
def _(S):
    T = 35
    body = rp([(9, 21.5), (9, 10.5), (7.5, 10.5), (7.5, 6), (16.5, 6), (16.5, 10.5), (15, 10.5), (15, 21.5)], T, r=S.r)
    teeth = [line(rseg(x, 6, x, 2.75, T)) for x in (8.75, 12, 15.25)]
    c = rot([(12, 15)], T)[0]
    return [shell(body), *teeth, dot(c[0], c[1], 1.1)]


@icon("hair-clippers", CAT, "Hair clippers with a serrated blade, a tapered body and a cord from the base",
      tags=["clippers", "barber", "haircut", "buzz cut", "electric clippers", "trimmer"])
def _(S):
    pts = [(4.5, 7.5)]
    for i in range(5):
        pts += [(4.5 + 3 * i + 1.5, 3.5), (4.5 + 3 * i + 3, 7.5)]
    pts += [(19.5, 10.5), (16, 10.5), (16, 18.5), (8, 18.5), (8, 10.5), (4.5, 10.5)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        dot(12, 14.5, 1.25),
        line("M12 18.5V20A1.5 1.5 0 0 0 13.5 21.5H20"),
    ]


@icon("nose-hair-trimmer", CAT, "Pen-shaped trimmer with a narrow slotted cylinder at the tip",
      tags=["ear trimmer", "grooming", "facial hair", "personal care", "electric trimmer", "men's care"])
def _(S):
    T = 35
    body = rp([(10, 2.5), (14, 2.5), (14, 8.5), (16, 10), (16, 21.5), (8, 21.5), (8, 10), (10, 8.5)], T, r=S.r)
    slot = rp([(11.25, 4.25), (12.75, 4.25), (12.75, 7.25), (11.25, 7.25)], T)
    c = rot([(12, 14.5)], T)[0]
    return [shell(body), Part("dot", slot), dot(c[0], c[1], 1.25)]


@icon("beard-oil", CAT, "Dropper bottle with a curled mustache on its label",
      tags=["beard care", "grooming", "conditioner", "facial hair", "men's care", "dropper"])
def _(S):
    body = poly([(6, 21.5), (6, 11), (8.5, 9), (8.5, 7), (10.5, 7), (10.5, 3), (13.5, 3), (13.5, 7), (15.5, 7), (15.5, 9), (18, 11), (18, 21.5)],
                closed=True, r=S.r)
    return [
        shell(body),
        mark("M12 15.5C11 14 9 13.75 8 14.75C8.75 16.25 10 17.5 12 16.5C14 17.5 15.25 16.25 16 14.75C15 13.75 13 14 12 15.5Z"),
    ]


@icon("mustache-wax", CAT, "Small round tin of mustache wax with a curled mustache on its lid",
      tags=["moustache wax", "beard balm", "pomade", "grooming", "styling", "men's care"])
def _(S):
    return [
        shell(union_d(ellipse(12, 10, 9, 4.75), rect(3, 10, 18, 9, L(S, 2, 4)))),
        detail("M3 10A9 4.75 0 0 0 21 10"),
        mark("M12 9.25C11 7.75 8.75 7.75 7.75 9.25C8.75 10.5 10.75 10.75 12 10C13.25 10.75 15.25 10.5 16.25 9.25C15.25 7.75 13 7.75 12 9.25Z"),
    ]


@icon("aftershave", CAT, "Square splash bottle with a wide stopper cap and a wave on the front",
      tags=["cologne", "after shave lotion", "fragrance", "grooming", "men's care", "balm"])
def _(S):
    body = poly([(5.5, 21.5), (5.5, 11), (8, 9), (8, 3.5), (16, 3.5), (16, 9), (18.5, 11), (18.5, 21.5)], closed=True, r=S.r)
    return [
        shell(body),
        detail(seg(8, 6.75, 16, 6.75)),
        detail("M8 16.5Q10 14 12 16.5T16 16.5"),
    ]


# ============================================================================ barber shop

@icon("barber-pole", CAT, "Cylindrical barber pole with diagonal stripes and round caps at top and bottom",
      tags=["barbershop", "hairdresser sign", "salon", "spiral stripes", "haircut", "barber shop"])
def _(S):
    body = poly([(7, 2.5), (17, 2.5), (17, 6), (16, 6), (16, 18), (17, 18), (17, 21.5), (7, 21.5), (7, 18), (8, 18), (8, 6), (7, 6)],
                closed=True, r=S.r)
    return [
        shell(body),
        detail(seg(8, 7.5, 16, 11.5)),
        detail(seg(8, 12.5, 16, 16.5)),
    ]


@icon("barber-chair", CAT, "Side view of a barber chair with a high back, an armrest, a footrest and a hydraulic base",
      tags=["salon chair", "haircut", "hairdresser", "barbershop", "styling chair", "hydraulic chair"])
def _(S):
    seat = poly([(3.5, 3.5), (8.5, 3.5), (8.5, 11.5), (16.5, 11.5), (16.5, 16), (3.5, 16)], closed=True, r=S.r)
    return [
        shell(seat),
        line("M11 11.5V8.5H15"),
        line(seg(16.5, 14, 20.5, 18.5)),
        line(seg(10, 16, 10, 19)),
        shell(poly([(5, 21.5), (7, 19), (13, 19), (15, 21.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("thinning-shears", CAT, "Scissors with one plain blade and one blade with comb-like teeth along its edge",
      tags=["texturizing shears", "hair scissors", "hairdresser", "barber", "haircut", "salon tool"])
def _(S):
    ticks = []
    for t in (0.08, 0.2, 0.32):
        x, y = 15.5 - 7 * t, 2.5 + 14 * t
        ticks.append(line(seg(x, y, x + 1.8, y + 0.9)))
    return [
        line(seg(8.5, 2.5, 15.5, 16.5)),
        line(seg(15.5, 2.5, 8.5, 16.5)),
        *ticks,
        dot(12, 9.5, 1.1),
        line(circle(16.75, 19, 2.25)),
        line(circle(7.25, 19, 2.25)),
    ]


@icon("hair-cutting-cape", CAT, "Salon cape with sloping shoulders, a neck band and fastening snap, flaring to a wide hem",
      tags=["salon cape", "barber cape", "haircut", "hairdresser", "styling gown", "apron"])
def _(S):
    return [
        shell("M10 3.5H14L19 7C20 12 21 16 21.5 20.5Q12 23 2.5 20.5C3 16 4 12 5 7Z"),
        detail(seg(10, 7, 14, 7)),
        dot(12, 10.5, 1),
        detail(seg(7.5, 19, 8.5, 13)),
        detail(seg(16.5, 19, 15.5, 13)),
    ]


@icon("hair-dryer", CAT, "Side view of a hair dryer with a round barrel, a pistol handle and air flow lines",
      tags=["blow dryer", "blow dry", "hairdryer", "salon", "styling", "hot air"])
def _(S):
    body = poly([(2.5, 5.5), (12, 5.5), (16, 3.5), (16, 12.5), (12, 11), (11.5, 11), (11, 21.5), (6.5, 21.5), (6, 11), (2.5, 11)],
                closed=True, r=S.r)
    return [
        shell(body),
        detail(seg(5, 8.25, 9, 8.25)),
        line(seg(18.5, 5.5, 21.5, 5.5)),
        line(seg(18.5, 8.25, 21.5, 8.25)),
        line(seg(18.5, 11, 21.5, 11)),
    ]


@icon("hair-diffuser", CAT, "Hair dryer with a wide dish-shaped diffuser on the end studded with round-tipped prongs",
      tags=["curl diffuser", "blow dryer attachment", "curly hair", "styling", "salon", "dryer nozzle"])
def _(S):
    body = poly([(2.5, 7), (8.5, 7), (12, 4), (12, 14), (8.5, 11), (8, 11), (7.5, 21.5), (4, 21.5), (3.5, 11), (2.5, 11)],
                closed=True, r=S.r)
    return [
        shell(body),
        line(seg(14.5, 5, 18.5, 5)), dot(20.25, 5, 1.25),
        line(seg(14.5, 9, 18.5, 9)), dot(20.25, 9, 1.25),
        line(seg(14.5, 13, 18.5, 13)), dot(20.25, 13, 1.25),
    ]


@icon("curling-iron", CAT, "Curling iron with a long cylindrical barrel, a clamp arm alongside it and a grip handle",
      tags=["curler", "hair curling", "tongs", "salon", "styling", "heated styling tool"])
def _(S):
    body = poly([(4.5, 2.5), (11.5, 2.5), (11.5, 14), (10.5, 14), (10.5, 21.5), (5.5, 21.5), (5.5, 14), (4.5, 14)], closed=True, r=S.r * 1.5)
    return [
        shell(body),
        line(poly([(11, 17.5), (16, 17.5), (16, 5.5), (19.5, 5.5)], r=S.r)),
        detail(seg(8, 5.5, 8, 11)),
    ]


@icon("hair-straightener", CAT, "Hair straightener with two long flat plates hinged at the handle, slightly open",
      tags=["flat iron", "hair iron", "straightening", "salon", "styling", "heated plates"])
def _(S):
    a = rp([(9, 2.5), (12, 2.5), (12, 16), (9, 16)], -6, r=S.r * 0.5)
    b = rp([(12, 2.5), (15, 2.5), (15, 16), (12, 16)], 6, r=S.r * 0.5)
    # rotate about the hinge instead of the canvas centre
    def about(pts, deg):
        return rot(pts, deg, 12.0, 18.0)
    a = poly(about([(9, 2.5), (12, 2.5), (12, 16), (9, 16)], -6), closed=True, r=S.r * 0.5)
    b = poly(about([(12, 2.5), (15, 2.5), (15, 16), (12, 16)], 6), closed=True, r=S.r * 0.5)
    handle = poly([(9.5, 16), (14.5, 16), (14, 21.5), (10, 21.5)], closed=True, r=S.r * 0.5)
    return [shell(union_d(a, b, handle)), dot(12, 19, 0.9)]


@icon("hot-air-brush", CAT, "Round bristle brush head on a thick barrel handle with air vents",
      tags=["volumising brush", "blow dry brush", "styling", "salon", "hair dryer brush", "round dryer"])
def _(S):
    ticks = []
    for y in (4.5, 8, 11.5):
        ticks.append(line(seg(5, y, 8.5, y)))
        ticks.append(line(seg(15.5, y, 19, y)))
    return [
        shell(rect(9.5, 2.5, 5, 12, rr(S, 2.5))),
        *ticks,
        shell(poly([(8.5, 15.5), (15.5, 15.5), (15.5, 21.5), (8.5, 21.5)], closed=True, r=S.r)),
        detail(seg(10.5, 18.5, 13.5, 18.5)),
    ]


@icon("round-brush", CAT, "Round barrel hair brush with bristles sticking out on both sides and a long handle",
      tags=["barrel brush", "blow dry", "hairbrush", "styling", "salon", "curl brush"])
def _(S):
    T = 40
    ticks = []
    for y in (4.75, 8.25, 11.75):
        ticks.append(line(rseg(5.25, y, 8.5, y, T)))
        ticks.append(line(rseg(15.5, y, 18.75, y, T)))
    return [
        shell(rp([(8.5, 2.75), (15.5, 2.75), (15.5, 13.5), (8.5, 13.5)], T, r=S.r * 1.5)),
        *ticks,
        shell(rp([(10.5, 13.5), (13.5, 13.5), (13.5, 21.5), (10.5, 21.5)], T, r=S.r)),
    ]


@icon("detangling-brush", CAT, "Oval hair brush seen from above with rows of long and short flexible bristles and no handle",
      tags=["wet brush", "knot remover", "hairbrush", "paddle brush", "styling", "hair care"])
def _(S):
    rows = [(8.5, (8.75, 12, 15.25)), (12, (7.125, 10.375, 13.625, 16.875)), (15.5, (8.75, 12, 15.25))]
    marks = []
    for ri, (y, xs) in enumerate(rows):
        for xi, x in enumerate(xs):
            marks.append(dot(x, y, 1.25 if (xi + ri) % 2 == 0 else 0.85))
    return [
        shell(rect(2.5, 4.5, 19, 15, L(S, 3, 7.5))),
        *marks,
    ]


@icon("rat-tail-comb", CAT, "Fine-tooth comb with a long thin pointed tail in place of a handle",
      tags=["tail comb", "parting comb", "hair sectioning", "salon", "styling", "hairdresser"])
def _(S):
    T = -20
    spine = poly(rot([(2.5, 8), (21.5, 8.75), (14.5, 12), (2.5, 12)], T), closed=True, r=S.r * 0.6)
    teeth = [line(rseg(x, 12, x, 18.5, T)) for x in (4, 7.6, 11.2)]
    return [shell(spine, stroke_miterlimit="3"), *teeth]


@icon("wide-tooth-comb", CAT, "Comb with a rounded spine and a few thick, widely spaced teeth",
      tags=["detangling comb", "curly hair", "hair care", "styling", "grooming", "large comb"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 5.5, rr(S, 2.75))),
        line(seg(5.25, 8.5, 5.25, 21.5)),
        line(seg(9.75, 8.5, 9.75, 21.5)),
        line(seg(14.25, 8.5, 14.25, 21.5)),
        line(seg(18.75, 8.5, 18.75, 21.5)),
    ]


@icon("afro-pick", CAT, "Hair pick with four long straight tines and a raised fist handle",
      tags=["hair pick", "afro comb", "natural hair", "lift", "styling"])
def _(S):
    body = poly([(8.5, 2.5), (15.5, 2.5), (15.5, 8), (20.5, 8), (20.5, 12), (3.5, 12), (3.5, 8), (8.5, 8)], closed=True, r=S.r)
    return [
        shell(body),
        detail(seg(10, 5.25, 14, 5.25)),
        line(seg(5.25, 12, 5.25, 21.5)),
        line(seg(9.75, 12, 9.75, 21.5)),
        line(seg(14.25, 12, 14.25, 21.5)),
        line(seg(18.75, 12, 18.75, 21.5)),
    ]


@icon("hair-claw-clip", CAT, "Hair claw clip seen from the front: a curved jaw with downward teeth and a hinge spring on top",
      tags=["claw clip", "hair clip", "jaw clip", "updo", "hair accessory", "clamp"])
def _(S):
    d = "M3.5 13.5C3.5 5 20.5 5 20.5 13.5"
    w = 17 / 4
    for i in range(4):
        x0 = 20.5 - w * i
        d += f"L{fmt(x0 - w / 2)} 18L{fmt(x0 - w)} 13.5"
    return [
        shell(d + "Z"),
        dot(12, 9.25, 1.3),
    ]


@icon("bobby-pin", CAT, "Bobby pin with one straight arm and one wavy arm joined at a rounded end",
      tags=["hair pin", "hair grip", "hair accessory", "updo", "clip"])
def _(S):
    T = 40
    def P_(x, y):
        q = rot([(x, y)], T)[0]
        return f"{fmt(q[0])} {fmt(q[1])}"
    d = f"M{P_(9.75, 21.5)}L{P_(9.75, 7)}A2.25 2.25 0 0 1 {P_(14.25, 7)}"
    y = 7
    for i in range(4):
        y2 = y + 14.5 / 4
        d += f"A1.8 1.8 0 0 {i % 2} {P_(14.25, y2)}"
        y = y2
    return [line(d)]


@icon("scrunchie", CAT, "Ruffled fabric hair tie gathered in folds around an elastic ring",
      tags=["hair tie", "hair band", "fabric elastic", "ponytail", "hair accessory", "ruffle"])
def _(S):
    folds = []
    for i in range(10):
        a = -90 + i * 36 + 18
        p1, p2 = pt_on(12, 12, 4.5, a), pt_on(12, 12, 6.5, a)
        folds.append(detail(seg(p1[0], p1[1], p2[0], p2[1])))
    return [
        shell(scallops(12, 12, 7, 10, 2.3, start=-90)),
        detail(circle(12, 12, 3.25)) if S.name == "rounded" else detail(poly(regular(12, 12, 3.6, 8), closed=True)),
    ]


@icon("hair-tie", CAT, "Plain elastic hair band loop closed with a small metal joint",
      tags=["elastic band", "ponytail holder", "hair band", "hair accessory", "rubber band", "bobble"])
def _(S):
    return [
        line(circle(12, 12, 7.75)),
        shell(rect(17.25, 9.5, 4.5, 5, L(S, 0, 1.5))),
    ]


@icon("headband", CAT, "Hard curved hair headband seen from the front as a wide arc",
      tags=["hair band", "alice band", "hair hoop", "hair accessory", "styling", "arc"])
def _(S):
    return [
        shell("M2.5 16C2.5 6 21.5 6 21.5 16H18.5C18.5 10.5 5.5 10.5 5.5 16Z"),
    ]


@icon("hair-roller", CAT, "Mesh hair roller with a pattern of holes over its surface and a long pin clip across its base",
      tags=["curler", "hair curlers", "curls", "setting", "hair styling"])
def _(S):
    marks = []
    for i, y in enumerate((6.5, 9.5, 12.5, 15.5)):
        for x in ((9, 12, 15) if i % 2 == 0 else (10.5, 13.5)):
            marks.append(dot(x, y, 0.85))
    return [
        shell(rect(6, 3.5, 12, 14.5, rr(S, 4))),
        *marks,
        line(seg(3.5, 20.5, 20.5, 20.5)),
    ]
