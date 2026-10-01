"""TypeIcon Core: kitchen (batch kitchen_001): cookware, bakeware and kitchen utensils.

Pans and pots are drawn in side view (or from above when the top is what identifies them). Long hand
utensils are drawn upright and turned 45 degrees clockwise so the handle points to the bottom-left and
the working end to the top-right, matching the tools set.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path.parser import parse_path
from geometry import SCALE, D, P, ST, U, fmt, path_to_d, rotation

CAT = "kitchen"
TILT = 45


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def tf(d, m):
    """Apply an affine matrix (a, b, c, d, e, f) to a d-string, keeping open paths open."""
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def rot(d, deg=TILT, cx=12.0, cy=12.0):
    """Rotate a d-string clockwise on screen about (cx, cy)."""
    return tf(d, rotation(deg, cx, cy))


def mv(d, dx, dy):
    return tf(d, (1, 0, 0, 1, dx, dy))


def flip(d):
    """Mirror across the vertical centre line."""
    return tf(d, (-1, 0, 0, 1, 24, 0))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def hole(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def fit(parts, cx=12.0, cy=12.0):
    """Translate parts so their drawn bounds are centred on (cx, cy), snapped to half pixels."""
    regions = []
    for p in parts:
        regions.append(P(p.d) if p.kind in ("shell", "dot", "solid") else ST(p.d, 2.0))
    x0, y0, x1, y1 = U(*regions).bounds
    dx = round((cx - (x0 + x1) / 2 / SCALE) * 2) / 2
    dy = round((cy - (y0 + y1) / 2 / SCALE) * 2) / 2
    if dx == 0 and dy == 0:
        return parts
    return [Part(p.kind, mv(p.d, dx, dy), p.attrs) for p in parts]


def tilt(parts, deg=TILT):
    """Turn an upright utensil (handle down) so the handle points to the bottom-left, then centre it."""
    return fit([Part(p.kind, rot(p.d, deg), p.attrs) for p in parts])


def ell_y(cx, cy, rx, ry, x, lower=True):
    """y of the ellipse (cx, cy, rx, ry) at x (lower or upper half)."""
    t = max(0.0, 1 - ((x - cx) / rx) ** 2)
    return cy + (ry if lower else -ry) * math.sqrt(t)


# ============================================================================ pans and pots

@icon("wok", CAT, "Round-bottomed wok with a long handle and a small loop handle",
      tags=["stir fry", "pan", "asian cooking", "cookware", "frying"])
def _(S):
    bowl = "M3.5 10.5H15.5A6 6 0 0 1 3.5 10.5Z"
    grip = rot(rect(15.5, 9.25, 6.8, 2.5, L(S, 0.4, 1.25)), -22, 15.5, 10.5)
    y = 13.5
    x = 9.5 - 6 * math.sqrt(1 - (3 / 6) ** 2)
    return [shell(bowl), shell(grip), line(f"M3.5 10.5C1.6 10.5 1.6 {fmt(y)} {fmt(x)} {fmt(y)}")]


@icon("karahi", CAT, "Deep round karahi pan with a loop handle on each side",
      tags=["kadai", "kadhai", "indian cooking", "curry pan", "cookware"], aliases=["kadai"])
def _(S):
    cx, cy, rx, ry = 12, 9, 8, 7.5
    bowl = f"M4 9H20A{rx} {ry} 0 0 1 4 9Z"
    y = 12.5
    x = cx - rx * math.sqrt(1 - ((y - cy) / ry) ** 2)
    ear = poly([(4.2, 9), (2, 9), (2, y), (x, y)], r=L(S, 0, 1.4))
    return [shell(bowl), line(ear), line(flip(ear))]


@icon("grill-pan", CAT, "Square grill pan with raised ridges and a long handle",
      tags=["griddle", "ridged pan", "grill marks", "stovetop grill", "cookware"])
def _(S):
    return [shell(rect(2.5, 5.5, 14, 14, rr(S, 3))), shell(rect(16.5, 11, 5.5, 3, rr(S, 1.5))),
            detail(seg(6.25, 9, 6.25, 16)), detail(seg(9.5, 9, 9.5, 16)), detail(seg(12.75, 9, 12.75, 16))]


@icon("griddle-plate", CAT, "Flat rectangular griddle plate with a rim and handles at both ends",
      tags=["griddle", "hot plate", "flat top", "plancha", "cookware"])
def _(S):
    h = poly([(4.5, 9.5), (2.2, 9.5), (2.2, 14.5), (4.5, 14.5)], r=L(S, 0, 1))
    return [shell(rect(4.5, 5.5, 15, 13, rr(S, 3))), line(h), line(flip(h)),
            detail(rect(8, 9, 8, 6, rr(S, 1.5)))]


@icon("crepe-pan", CAT, "Flat crepe pan seen from above with a thin crepe inside",
      tags=["crepe", "pancake pan", "flat pan", "galette", "cookware"])
def _(S):
    cx, cy, r = 9, 14, 7
    grip = rot(rect(cx + r, cy - 1.1, 7.5, 2.2, L(S, 0.3, 1.1)), -42, cx, cy)
    return [shell(circle(cx, cy, r)), shell(grip), detail(circle(cx, cy, 3.5))]


@icon("paella-pan", CAT, "Wide paella pan from above with two loop handles, rice and a lemon wedge",
      tags=["paella", "paellera", "spanish rice", "shallow pan", "cookware"])
def _(S):
    cx, cy, r = 12, 12, 7.5
    y0, y1 = 10.2, 13.8
    x0 = cx - math.sqrt(r * r - (cy - y0) ** 2)
    ear = poly([(x0, y0), (2, y0), (2, y1), (x0, y1)], r=L(S, 0, 1.4))
    return [shell(circle(cx, cy, r)), line(ear), line(flip(ear)),
            detail("M11.52 8.52A2.8 2.8 0 0 1 15.48 12.48Z"),
            dot(7.9, 10.4, 1.1), dot(9, 14.9, 1.1), dot(12.8, 16.3, 1.1), dot(15.8, 15, 1.1), dot(11.2, 12.4, 1.1)]


@icon("double-boiler", CAT, "Bowl nested on top of a pot of simmering water",
      tags=["bain marie", "water bath", "melting chocolate", "steam", "cookware"], aliases=["bain-marie"])
def _(S):
    cx, cy, rx, ry = 12, 7.5, 9, 7
    bowl = f"M3 7.5H21A{rx} {ry} 0 0 1 3 7.5Z"
    yt = ell_y(cx, cy, rx, ry, 5.5)
    c = L(S, 0, 2)
    pot = (f"M5.5 {fmt(yt)}V{fmt(20.5 - c)}" + (f"Q5.5 20.5 {fmt(5.5 + c)} 20.5" if c else "")
           + f"H{fmt(18.5 - c)}" + (f"Q18.5 20.5 18.5 {fmt(20.5 - c)}" if c else "") + f"V{fmt(yt)}")
    return [shell(bowl), line(pot), line(seg(2.5, 16, 5.5, 16)), line(seg(18.5, 16, 21.5, 16))]


@icon("bamboo-steamer", CAT, "Round bamboo steamer with two stacked tiers and a lid",
      tags=["dim sum", "dumpling steamer", "steaming basket", "asian cooking", "bamboo"])
def _(S):
    c = L(S, 1.5, 3)
    body = (f"M3.5 9C3.5 6 7.5 4.5 12 4.5C16.5 4.5 20.5 6 20.5 9V{fmt(20.5 - c)}"
            f"Q20.5 20.5 {fmt(20.5 - c)} 20.5H{fmt(3.5 + c)}Q3.5 20.5 3.5 {fmt(20.5 - c)}Z")
    out = [shell(body), detail("M3.5 9C6.5 10.5 17.5 10.5 20.5 9"), detail("M3.5 14.5C6.5 16 17.5 16 20.5 14.5")]
    for y0 in (12.3, 17.8):
        out += [detail(seg(8, y0, 8, y0 + 1.2)), detail(seg(12, y0 + 0.2, 12, y0 + 1.4)), detail(seg(16, y0, 16, y0 + 1.2))]
    return out


@icon("tagine", CAT, "Tagine: a shallow dish under a tall conical lid with a knob",
      tags=["tajine", "moroccan", "clay pot", "slow cooking", "stew"], aliases=["tajine"])
def _(S):
    c = L(S, 0.6, 2.5)
    body = (f"M2.5 16H5C8 15 10.5 10.5 11 6.5H13C13.5 10.5 16 15 19 16H21.5"
            f"C21 18.5 {fmt(19 + c * 0.2)} 20 {fmt(16.5)} 20H7.5C{fmt(5 - c * 0.2)} 20 3 18.5 2.5 16Z")
    return [shell(body, stroke_miterlimit="2"), detail(seg(5, 16, 19, 16)), dot(12, 4.3, 1.5)]


@icon("clay-pot", CAT, "Round earthenware pot with a short neck, small lid and ear handles",
      tags=["earthenware", "terracotta", "donabe", "stew pot", "cookware"])
def _(S):
    k = L(S, 0, 1)
    body = ("M8.5 8.5C4.5 9.5 3.5 12 3.5 14.5C3.5 18.5 7 20.5 12 20.5C17 20.5 20.5 18.5 20.5 14.5"
            f"C20.5 12 19.5 9.5 15.5 8.5C{fmt(16 - k)} 5.5 14.5 4.5 12 4.5C9.5 4.5 {fmt(8 + k)} 5.5 8.5 8.5Z")
    ear = "M5.2 10.2C2.6 9.4 1.9 12.6 3.7 13.4"
    return [shell(body), detail(seg(8.5, 8.5, 15.5, 8.5)), dot(12, 2.9, 1.3), line(ear), line(flip(ear))]


@icon("casserole-dish", CAT, "Deep casserole dish with a domed lid, knob and side handles",
      tags=["dutch oven", "cocotte", "oven dish", "stew", "bakeware", "cookware"], aliases=["cocotte"])
def _(S):
    c = L(S, 1.5, 3)
    body = (f"M4.5 12H5.5C5.5 8.5 8.5 7 12 7C15.5 7 18.5 8.5 18.5 12H19.5V{fmt(19.5 - c)}"
            f"Q19.5 19.5 {fmt(19.5 - c)} 19.5H{fmt(4.5 + c)}Q4.5 19.5 4.5 {fmt(19.5 - c)}Z")
    return [shell(body), detail(seg(5.5, 12, 18.5, 12)), dot(12, 5.2, 1.4),
            line(seg(2, 14.5, 4.5, 14.5)), line(seg(19.5, 14.5, 22, 14.5))]


@icon("braiser", CAT, "Wide shallow braiser with a low domed lid and two loop handles",
      tags=["braising pan", "shallow casserole", "saute", "slow cooking", "cookware"])
def _(S):
    c = L(S, 1.5, 2.5)
    body = (f"M4.5 14H5C6 11 9 10 12 10C15 10 18 11 19 14H19.5V{fmt(19 - c)}"
            f"Q19.5 19 {fmt(19.5 - c)} 19H{fmt(4.5 + c)}Q4.5 19 4.5 {fmt(19 - c)}Z")
    ear = "M4.5 14.5C1.8 14.5 1.8 18 4.5 18"
    return [shell(body), detail(seg(5, 14, 19, 14)), shell(rect(9.5, 6.5, 5, 2, rr(S, 1))),
            line(ear), line(flip(ear))]


@icon("baking-dish", CAT, "Rectangular baking dish with sloped sides and rim handles",
      tags=["casserole dish", "lasagna dish", "oven dish", "bakeware", "roasting dish"])
def _(S):
    return [shell(poly([(4, 11), (20, 11), (18.5, 17), (5.5, 17)], closed=True, r=S.r)),
            shell(rect(2, 9, 20, 2, L(S, 0, 1))), detail(seg(7, 14, 17, 14))]


@icon("roasting-pan", CAT, "Roasting pan with side handles holding a roast",
      tags=["roaster", "roast", "turkey pan", "oven tray", "bakeware"], aliases=["roaster"])
def _(S):
    body = poly([(3.5, 13), (20.5, 13), (19, 19.5), (5, 19.5)], closed=True, r=S.r)
    roast = f"M6 11C6 8 8.5 6.5 12 6.5C15.5 6.5 18 8 18 11Z"
    ear = poly([(3.5, 13), (2, 13), (2, 15.5), (4.2, 15.5)], r=L(S, 0, 1))
    return [shell(body), shell(roast, stroke_miterlimit="2"), line(seg(15.8, 7.4, 18, 5)), dot(18.8, 4.2, 1.5),
            line(ear), line(flip(ear))]


@icon("milk-pan", CAT, "Small deep saucepan with a pouring spout and a long handle",
      tags=["saucepan", "milk", "sauce pan", "pouring lip", "cookware"])
def _(S):
    c = L(S, 1.5, 3)
    body = (f"M16 9V{fmt(19.5 - c)}Q16 19.5 {fmt(16 - c)} 19.5H{fmt(5 + c)}Q5 19.5 5 {fmt(19.5 - c)}"
            "V11L2.8 8L7 9Z")
    grip = rot(rect(16, 8, 6.5, 2.5, rr(S, 1.25)), -15, 16, 9.25)
    return [shell(body, stroke_miterlimit="3"), shell(grip)]


@icon("takoyaki-pan", CAT, "Takoyaki pan from above with a grid of round wells and a short handle",
      tags=["takoyaki", "aebleskiver pan", "round wells", "japanese snack", "cookware"], aliases=["aebleskiver-pan"])
def _(S):
    out = [shell(rect(2.5, 4, 16, 16, rr(S, 3))), shell(rect(18.5, 10.5, 3.5, 3, L(S, 0.4, 1.5)))]
    for x in (6.5, 10.5, 14.5):
        for y in (8, 12, 16):
            out.append(dot(x, y, 1.4))
    return out


@icon("pasta-pot", CAT, "Tall pot with a perforated strainer insert lifted above the rim",
      tags=["stock pot", "pasta cooker", "strainer insert", "boiling", "cookware"])
def _(S):
    ins = poly([(6.5, 11), (6.5, 5.5), (17.5, 5.5), (17.5, 11)], r=S.r)
    return [shell(rect(4, 11, 16, 9.5, rr(S, 3))), line(ins), line(seg(4, 5.5, 6.5, 5.5)), line(seg(17.5, 5.5, 20, 5.5)),
            dot(9.5, 8.3, 1), dot(12, 8.3, 1), dot(14.5, 8.3, 1),
            line(seg(2, 14, 4, 14)), line(seg(20, 14, 22, 14))]


@icon("egg-poacher", CAT, "Egg poacher pan from above with four cups, each holding a yolk, and a handle",
      tags=["poached eggs", "egg cups", "breakfast", "poaching pan", "cookware"])
def _(S):
    out = [shell(rect(2, 4, 16.5, 16.5, rr(S, 4))), shell(rect(18.5, 10.8, 3.5, 2.9, L(S, 0.4, 1.4)))]
    for x in (6.65, 13.85):
        for y in (8.65, 15.85):
            out += [detail(circle(x, y, 2.25)), dot(x, y, 0.9)]
    return out


@icon("fish-poacher", CAT, "Long oval fish poacher from above with a fish inside and end handles",
      tags=["fish kettle", "poaching", "salmon", "whole fish", "cookware"], aliases=["fish-kettle"])
def _(S):
    ear = poly([(4, 10.5), (2, 10.5), (2, 13.5), (4, 13.5)], r=L(S, 0, 1))
    fish = "M7.5 12C9.5 9.6 12.6 9.6 14.6 12C12.6 14.4 9.5 14.4 7.5 12Z"
    return [shell(rect(4, 6.5, 16, 11, L(S, 3.5, 5.5))), line(ear), line(flip(ear)),
            detail(fish), detail(poly([(14.6, 12), (16.8, 10.2), (16.8, 13.8)], closed=True, r=L(S, 0, 0.5)))]


@icon("tawa", CAT, "Flat round tawa griddle seen at an angle with a short handle",
      tags=["tava", "roti pan", "chapati", "flat griddle", "indian cooking", "cookware"], aliases=["tava"])
def _(S):
    grip = rot(rect(18, 12.3, 4.5, 2.4, L(S, 0.4, 1.2)), -18, 18, 13.5)
    return [shell(ellipse(10.5, 13.5, 8, 4.5)), detail(ellipse(10.5, 13.2, 4.5, 2)), shell(grip)]


@icon("couscoussier", CAT, "Two-tier couscoussier: a perforated steamer on a round-bellied pot",
      tags=["couscous", "steamer pot", "moroccan", "two tier pot", "cookware"])
def _(S):
    k = L(S, 0, 0.8)
    body = poly([(6.5, 12.5), (4, 5), (20, 5), (17.5, 12.5)], r=k)
    body += "C20.5 13 21 15.5 21 17C21 19.5 18.5 21 15.5 21H8.5C5.5 21 3 19.5 3 17C3 15.5 3.5 13 6.5 12.5Z"
    return [shell(body, stroke_miterlimit="2"), detail(seg(6.5, 12.5, 17.5, 12.5)),
            dot(9, 8.5, 1), dot(12, 8.5, 1), dot(15, 8.5, 1), line(seg(2, 5, 4, 5)), line(seg(20, 5, 22, 5))]


@icon("pot-lid", CAT, "Round pot lid with a centre knob, seen at a slight angle",
      tags=["lid", "cover", "saucepan lid", "pan lid", "cookware"])
def _(S):
    body = "M2.5 15.5C2.5 9.5 21.5 9.5 21.5 15.5C21.5 18 2.5 18 2.5 15.5Z"
    return [shell(body), shell(rect(9.5, 7, 5, 3, L(S, 0.5, 1.5))), detail("M5.5 14C8.5 15.3 15.5 15.3 18.5 14")]


@icon("divided-hot-pot", CAT, "Round hot pot from above split into two broths by a curved divider",
      tags=["hot pot", "shabu shabu", "twin broth", "yuanyang pot", "fondue", "cookware"], aliases=["yuanyang-pot"])
def _(S):
    cx, cy, r = 12, 12, 7.5
    ear = poly([(4.6, 10.5), (2, 10.5), (2, 13.5), (4.6, 13.5)], closed=True, r=L(S, 0, 0.8))
    return [shell(circle(cx, cy, r)), shell(ear), shell(flip(ear)),
            detail("M12 5.5C9 8.5 15 15.5 12 18.5")]


@icon("fish-grill-basket", CAT, "Hinged fish-shaped wire grill basket with a long handle",
      tags=["fish basket", "grilling basket", "barbecue", "bbq", "grill", "fish"])
def _(S):
    body = "M2.5 12C4 7.5 8.5 6.5 11.5 10L14 8V16L11.5 14C8.5 17.5 4 16.5 2.5 12Z"
    return [shell(body, stroke_miterlimit="2"), shell(rect(14, 11, 8, 2, L(S, 0, 1))),
            detail(seg(5.8, 9, 5.8, 15)), detail(seg(9, 9, 9, 15)), detail(seg(3.8, 12, 11.2, 12))]


@icon("egg-ring", CAT, "Round egg ring with a folding handle and an egg inside",
      tags=["egg mold", "fried egg", "breakfast", "muffin ring", "cooking ring"])
def _(S):
    cx, cy, r = 10, 14, 6.5
    a = math.radians(-45)
    x0, y0 = cx + r * math.cos(a), cy + r * math.sin(a)
    end = circle(19.6, 4.4, 1.6) if S.name == "rounded" else rect(18, 2.8, 3.2, 3.2)
    return [shell(circle(cx, cy, r)), line(seg(x0, y0, 18.4, 5.6)), shell(end),
            detail(circle(9.3, 14.6, 2.4))]


@icon("idli-stand", CAT, "Idli stand: stacked plates with round dimples on a centre rod",
      tags=["idli maker", "idli plates", "south indian", "steamer", "cookware"], aliases=["idli-maker"])
def _(S):
    out = [shell(circle(12, 3.5, 1.5)), line(seg(12, 5, 12, 19))]
    for y in (8, 13.5, 19):
        out.append(line(f"M2.5 {y}H4.5A2.75 1.8 0 0 0 10 {y}H14A2.75 1.8 0 0 0 19.5 {y}H21.5"))
    return out


@icon("ramekin", CAT, "Small round ramekin dish with ribbed sides",
      tags=["souffle dish", "creme brulee", "custard cup", "baking cup", "bakeware"])
def _(S):
    c = L(S, 1.5, 3.5)
    body = (f"M4 10A8 2.5 0 0 1 20 10V{fmt(19 - c)}C20 {fmt(19 - c * 0.3)} 17 19.5 12 19.5"
            f"C7 19.5 4 {fmt(19 - c * 0.3)} 4 {fmt(19 - c)}Z")
    return [shell(body), detail("M4 10A8 2.5 0 0 0 20 10"),
            detail(seg(8, 14.5, 8, 17)), detail(seg(12, 14.8, 12, 17.3)), detail(seg(16, 14.5, 16, 17))]


@icon("pizza-peel", CAT, "Pizza peel: a wide flat paddle on a long handle",
      tags=["pizza paddle", "baker's peel", "pizza oven", "bread peel", "baking"], aliases=["pizza-paddle"])
def _(S):
    c = L(S, 1.5, 3)
    blade = (f"M7 12V{fmt(3 + c)}Q7 3 {fmt(7 + c)} 3H{fmt(17 - c)}Q17 3 17 {fmt(3 + c)}V12"
             "L13.2 14.5V21H10.8V14.5Z")
    return tilt([shell(blade, stroke_miterlimit="2")])


@icon("pizza-cutter", CAT, "Pizza cutter: a round blade wheel on a handle with a finger guard",
      tags=["pizza wheel", "rolling cutter", "slicer", "pizza", "kitchen tool"], aliases=["pizza-wheel"])
def _(S):
    return tilt([shell(circle(12, 7.5, 5.5)), line(seg(12, 7.5, 12, 15)), dot(12, 7.5, 1.2),
                 line(seg(8.5, 15, 15.5, 15)), shell(rect(10.5, 15, 3, 7, L(S, 0.5, 1.5)))])


@icon("oven-mitt", CAT, "Quilted oven mitt with a thumb, a cuff and a hanging loop",
      tags=["oven glove", "pot glove", "heat protection", "baking", "kitchen mitten"], aliases=["oven-glove"])
def _(S):
    body = ("M7.5 21V15.3C5.2 15.3 3.6 12.8 4.4 10.8C5.1 9 7 9.2 8 10.6"
            "C8 6 9.7 3 13 3C16.5 3 18 5.8 18 9.5V21Z")
    loop = "M18 18C21.2 18 21.2 21.5 18 21.5" if S.name == "rounded" else "M18 18H20.5V21.5H18"
    return [shell(body), detail(seg(7.5, 17.5, 18, 17.5)), detail(seg(10.5, 9, 15.5, 14)), detail(seg(15.5, 9, 10.5, 14)),
            line(loop)]


@icon("pot-holder", CAT, "Square quilted pot holder with a hanging loop at one corner",
      tags=["potholder", "hot pad", "trivet", "heat protection", "kitchen textile"], aliases=["potholder"])
def _(S):
    return [shell(rect(5, 5, 15.5, 15.5, rr(S))), shell(circle(4.2, 4.2, 1.9)),
            detail(poly([(12.75, 8), (17.5, 12.75), (12.75, 17.5), (8, 12.75)], closed=True, r=L(S, 0, 0.8)))]


@icon("measuring-cup", CAT, "Measuring jug with graduation marks, a spout and a handle",
      tags=["measuring jug", "liquid measure", "baking", "graduated cup", "volume"], aliases=["measuring-jug"])
def _(S):
    body = poly([(3, 5), (15.5, 5), (14.5, 20.5), (5.5, 20.5), (4.8, 8)], closed=True, r=S.r)
    handle = poly([(15.3, 8.5), (19.5, 8.5), (19.5, 16), (14.8, 16)], r=S.r)
    return [shell(body, stroke_miterlimit="2"), line(handle), detail(seg(5.4, 10.5, 9, 10.5)), detail(seg(5.6, 14, 9, 14)),
            detail(seg(5.8, 17.5, 9, 17.5))]


@icon("measuring-spoons", CAT, "Set of three measuring spoons of different sizes joined on a ring",
      tags=["spoon set", "teaspoon", "tablespoon", "baking", "measure"])
def _(S):
    rc = (5, 19)
    ring = circle(rc[0], rc[1], 1.8) if S.name == "rounded" else rect(rc[0] - 1.7, rc[1] - 1.7, 3.4, 3.4)
    out = [line(ring)]
    for a, rx, ry in ((-80, 3.3, 2.5), (-45, 2.8, 2.1), (-10, 2.4, 1.8)):
        u = (math.cos(math.radians(a)), math.sin(math.radians(a)))
        c = (rc[0] + 13 * u[0], rc[1] + 13 * u[1])
        s0 = (rc[0] + 1.8 * u[0], rc[1] + 1.8 * u[1])
        s1 = (c[0] - rx * u[0], c[1] - rx * u[1])
        out += [shell(rot(ellipse(c[0], c[1], rx, ry), a, c[0], c[1])), line(seg(s0[0], s0[1], s1[0], s1[1]))]
    return out


@icon("mixing-bowl", CAT, "Wide mixing bowl with a thick rim and a small pouring lip",
      tags=["bowl", "baking bowl", "batter", "mixing", "prep bowl"])
def _(S):
    k = L(S, 0, 1)
    body = (f"M3 7.5H21.5V10.5H20C19 16.5 16 19.5 12 19.5C8 19.5 5 16.5 4 10.5H3.5L2 7.5Z")
    return [shell(body, stroke_miterlimit="2"), detail(seg(4, 10.5, 20, 10.5))]


@icon("egg-separator", CAT, "Egg separator cup holding a yolk while the white drips through",
      tags=["egg white", "yolk", "baking", "separating eggs", "kitchen tool"])
def _(S):
    bowl = "M3 10H16C15.5 13.8 13 15.5 9.5 15.5C6 15.5 3.5 13.8 3 10Z"
    drop = "M9.5 17.5C10.6 18.8 11 19.6 11 20.3C11 21.1 10.3 21.6 9.5 21.6C8.7 21.6 8 21.1 8 20.3C8 19.6 8.4 18.8 9.5 17.5Z"
    return [shell(bowl), shell(rect(16, 9, 6, 2, L(S, 0, 1))), hole(circle(9.5, 8.6, 2.8)), shell(drop)]


@icon("whisk", CAT, "Balloon whisk with wire loops on a straight handle",
      tags=["whip", "beater", "baking", "mixing", "egg whisk", "whisking"])
def _(S):
    loop = "M12 14C6.8 10.5 7.2 2.5 12 2.5C16.8 2.5 17.2 10.5 12 14Z"
    return tilt([line(loop), line(seg(12, 2.5, 12, 14)), shell(rect(10.5, 14, 3, 8, L(S, 0.5, 1.5)))])


@icon("egg-beater", CAT, "Rotary egg beater with a crank wheel and two beaters",
      tags=["hand mixer", "rotary whisk", "hand beater", "whipping", "baking"], aliases=["rotary-beater"])
def _(S):
    return [shell(rect(9.5, 2, 5, 5, L(S, 0.5, 2))), line(seg(12, 7, 12, 12.5)), line(seg(12, 10, 15, 10)),
            shell(circle(18.2, 10, 3.2)), dot(18.2, 10, 1.1),
            line(ellipse(9.8, 16.8, 1.7, 4.2)), line(ellipse(14.2, 16.8, 1.7, 4.2))]


@icon("dough-docker", CAT, "Dough docker: a spiked roller on a frame with a handle",
      tags=["pastry docker", "pie crust", "pizza dough", "roller", "baking tool"], aliases=["pastry-docker"])
def _(S):
    top = [(6, 4.5)]
    bot = [(18, 9.5)]
    for i in range(6):
        x = 6 + i * 2
        top += [(x + 1, 3), (x + 2, 4.5)]
        bot += [(18 - i * 2 - 1, 11), (18 - i * 2 - 2, 9.5)]
    roller = poly(top + bot, closed=True, r=0)
    return [shell(roller, stroke_miterlimit="2"), line(poly([(6, 7), (3.5, 7), (3.5, 13), (20.5, 13), (20.5, 7), (18, 7)], r=S.r)),
            line(seg(12, 13, 12, 15)), shell(rect(10.5, 15, 3, 7, L(S, 0.5, 1.5)))]


@icon("food-cloche", CAT, "Serving cloche: a dome cover with a knob resting on a plate",
      tags=["cloche", "dome cover", "room service", "serving", "restaurant", "dish cover"], aliases=["cloche"])
def _(S):
    knob = circle(12, 6.3, 1.6) if S.name == "rounded" else rect(10.5, 4.8, 3, 3)
    return [shell("M4.5 17A7.5 7.5 0 0 1 19.5 17Z"), shell(knob), line(seg(2, 20, 22, 20)),
            detail("M7.6 14A4.6 4.6 0 0 1 10 11")]


@icon("aluminum-foil", CAT, "Box of aluminium foil with a crinkled sheet pulled out below",
      tags=["aluminium foil", "tin foil", "kitchen foil", "wrap", "baking"], aliases=["aluminium-foil", "tin-foil"])
def _(S):
    k = L(S, 0, 1.2)
    body = poly([(2.5, 5), (21.5, 5), (21.5, 11.5), (20, 11.5), (20, 18.5), (17, 20.5), (14, 18.5), (11, 20.5),
                 (8, 18.5), (4, 20), (4, 11.5), (2.5, 11.5)], closed=True, r=k)
    return [shell(body, stroke_miterlimit="2"), detail(seg(4, 11.5, 20, 11.5)), detail(circle(6.5, 8.25, 1.3))]


@icon("popsicle-mold", CAT, "Ice pop mold tray holding three pops with sticks",
      tags=["ice pop mold", "ice lolly", "popsicle", "frozen treat", "freezer"], aliases=["ice-pop-mold"])
def _(S):
    out = [shell(rect(2.5, 10, 19, 10.5, rr(S, 3)))]
    for x in (7, 12, 17):
        out += [detail(f"M{fmt(x - 1.5)} 12.5V16.5A1.5 1.5 0 0 0 {fmt(x + 1.5)} 16.5V12.5"), line(seg(x, 10, x, 3.5))]
    return out


@icon("spatula", CAT, "Kitchen turner with a slotted flat blade on a long handle",
      tags=["turner", "flipper", "fish slice", "pancake turner", "frying", "burger flip"], aliases=["turner"])
def _(S):
    return tilt([shell(rect(7, 2, 10, 10, rr(S, 2))), detail(seg(10.3, 4.8, 10.3, 9.2)), detail(seg(13.7, 4.8, 13.7, 9.2)),
                 line(seg(12, 12, 12, 14.5)), shell(rect(10.5, 14.5, 3, 7.5, L(S, 0.5, 1.5)))])


@icon("slotted-spoon", CAT, "Long-handled spoon with slot holes in the bowl",
      tags=["draining spoon", "strainer spoon", "serving spoon", "cooking spoon", "utensil"])
def _(S):
    bowl = ellipse(12, 7.5, 5, 5.8) if S.name == "rounded" else \
        "M12 1.7C15.3 1.7 17 4.5 17 7.5C17 10.8 14.8 13.3 12 13.3C9.2 13.3 7 10.8 7 7.5C7 4.5 8.7 1.7 12 1.7Z"
    return tilt([shell(bowl), detail(seg(10.25, 5, 10.25, 10)), detail(seg(13.75, 5, 13.75, 10)),
                 line(seg(12, 13.3, 12, 22))])


@icon("ladle", CAT, "Ladle with a deep round bowl and a long handle ending in a hook",
      tags=["soup ladle", "serving spoon", "dipper", "soup", "stew", "utensil"])
def _(S):
    return [shell("M2.5 13.5H13A5.25 5.25 0 0 1 2.5 13.5Z"),
            line("M12.5 13.5L18.3 4.8C19.2 3.5 21.2 4.1 21 5.8")]


@icon("kitchen-tongs", CAT, "Kitchen tongs: two arms joined by a spring loop with scalloped gripping ends",
      tags=["tongs", "serving tongs", "grill tongs", "bbq", "salad tongs", "utensil"], aliases=["tongs"])
def _(S):
    arms = "M8.2 17L10.3 4.5A1.8 1.8 0 0 1 13.7 4.5L15.8 17"
    pad = poly([(8.2, 17), (6.8, 22), (10.4, 20.2)], closed=True, r=L(S, 0, 0.8))
    return tilt([line(arms), shell(pad, stroke_miterlimit="2"), shell(flip(pad), stroke_miterlimit="2")])


@icon("spider-strainer", CAT, "Spider strainer: a flat round wire web on a long handle",
      tags=["spider skimmer", "skimmer", "wire strainer", "frying", "noodles", "utensil"], aliases=["spider-skimmer"])
def _(S):
    cx, cy, r = 12, 7.8, 6
    hexa = poly([(cx + 3 * math.cos(math.radians(a)), cy + 3 * math.sin(math.radians(a))) for a in range(-90, 270, 60)],
                closed=True, r=L(S, 0, 0.6))
    out = [shell(circle(cx, cy, r)), detail(hexa)]
    for a in (-90, -30, 30, 90, 150, 210):
        p0 = (cx + 3 * math.cos(math.radians(a)), cy + 3 * math.sin(math.radians(a)))
        p1 = (cx + 5 * math.cos(math.radians(a)), cy + 5 * math.sin(math.radians(a)))
        out.append(detail(seg(*p0, *p1)))
    out.append(line(seg(12, 13.8, 12, 22)))
    return tilt(out)


@icon("silicone-spatula", CAT, "Silicone spatula with a flat blade, one corner rounded, on a long handle",
      tags=["rubber spatula", "scraper", "baking", "bowl scraper", "batter", "utensil"], aliases=["rubber-spatula"])
def _(S):
    k = L(S, 0, 0.8)
    blade = f"M7.5 {fmt(3 + k)}Q7.5 3 {fmt(7.5 + k)} 3H13A3.5 3.5 0 0 1 16.5 6.5V11L13 13.5H11L7.5 11Z"
    return tilt([shell(blade, stroke_miterlimit="2"), shell(rect(10.75, 13.5, 2.5, 8.5, L(S, 0.4, 1.25)))])


@icon("wooden-spoon", CAT, "Wooden spoon with an oval bowl and a long straight handle",
      tags=["cooking spoon", "stirring spoon", "wood spoon", "baking", "utensil"])
def _(S):
    bowl = ellipse(12, 6.8, 3.8, 5.3) if S.name == "rounded" else \
        "M12 1.5C14.6 1.5 15.8 4 15.8 6.8C15.8 9.8 14.2 12.1 12 12.1C9.8 12.1 8.2 9.8 8.2 6.8C8.2 4 9.4 1.5 12 1.5Z"
    return tilt([shell(bowl), shell(rect(10.75, 12, 2.5, 10, L(S, 0.4, 1.25)))])


@icon("pasta-server", CAT, "Pasta server: a spoon with teeth around the bowl and a hole in the middle",
      tags=["spaghetti server", "pasta fork", "pasta spoon", "noodles", "utensil"], aliases=["spaghetti-server"])
def _(S):
    cx, cy = 12, 7.5
    pts = []
    for i in range(0, 13):
        a = math.radians(-180 + i * 15)
        rr_ = 6.4 if i % 2 else 4.8
        pts.append((cx + rr_ * math.cos(a), cy + rr_ * math.sin(a)))
    bowl = poly(pts, r=0) + f"A4.8 4.8 0 0 1 {fmt(cx - 4.8)} {fmt(cy)}Z"
    return tilt([shell(bowl, stroke_miterlimit="2"), detail(circle(cx, cy + 0.5, 1.5)), line(seg(12, 12.3, 12, 22))])


@icon("potato-masher", CAT, "Potato masher with a wavy wire head and a straight handle",
      tags=["masher", "mashed potatoes", "puree", "utensil", "mashing"])
def _(S):
    wave = "M4 17.5A2 2 0 0 0 8 17.5A2 2 0 0 1 12 17.5A2 2 0 0 0 16 17.5A2 2 0 0 1 20 17.5"
    frame = poly([(4, 17.5), (4, 12.5), (20, 12.5), (20, 17.5)], r=S.r)
    return [shell(rect(10, 2, 4, 7.5, L(S, 0.5, 2))), line(seg(12, 9.5, 12, 12.5)), line(frame), line(wave)]


@icon("garlic-press", CAT, "Garlic press with two hinged handles and a perforated chamber",
      tags=["garlic crusher", "mincer", "garlic", "press", "kitchen tool"], aliases=["garlic-crusher"])
def _(S):
    upper = rot(rect(3, 7, 19, 2.5, L(S, 0.4, 1.25)), -12, 3, 8.25)
    lower = rot(rect(9.5, 12.5, 12.5, 2.5, L(S, 0.4, 1.25)), 14, 9.5, 13.75)
    return [shell(rect(2.5, 10.5, 7, 5, L(S, 0.5, 1.5))), shell(upper), shell(lower),
            dot(4.5, 18.3, 1), dot(7.5, 18.3, 1), dot(6, 20.8, 1)]


@icon("rasp-grater", CAT, "Long narrow rasp grater with fine teeth and a handle",
      tags=["zester", "rasp", "fine grater", "citrus zest", "cheese grater", "kitchen tool"], aliases=["zester"])
def _(S):
    out = [shell(rect(9, 1.5, 6, 13, L(S, 0.5, 1.5))), shell(rect(9.5, 14.5, 5, 7.5, L(S, 1, 2.5)))]
    for y in (4.5, 8, 11.5):
        out.append(detail(seg(11, y, 13, y - 1)))
    return tilt(out)


@icon("box-grater", CAT, "Four-sided box grater with a top handle and rows of holes",
      tags=["cheese grater", "grater", "shredder", "grating", "kitchen tool"], aliases=["cheese-grater"])
def _(S):
    out = [shell(poly([(7, 7), (17, 7), (19.5, 21), (4.5, 21)], closed=True, r=S.r)),
           line(poly([(9.5, 7), (9.5, 3), (14.5, 3), (14.5, 7)], r=S.r))]
    for y, dx in ((11, 0), (14.5, 0.3), (18, 0.6)):
        out += [dot(9 - dx, y, 1), dot(12, y, 1), dot(15 + dx, y, 1)]
    return out


@icon("vegetable-peeler", CAT, "Y-shaped vegetable peeler with a slotted blade across the arms",
      tags=["peeler", "potato peeler", "y peeler", "peeling", "kitchen tool"], aliases=["peeler"])
def _(S):
    return [shell(rect(5, 2, 14, 5, L(S, 0.5, 2))), detail(seg(8, 4.5, 16, 4.5)),
            line(poly([(6.5, 7), (12, 12.5), (17.5, 7)], r=S.r)), line(seg(12, 12.5, 12, 14)),
            shell(rect(10.5, 14, 3, 8, L(S, 0.5, 1.5)))]


@icon("apple-slicer", CAT, "Apple slicer: a ring with blades radiating from a centre corer and two handles",
      tags=["apple corer", "apple cutter", "wedger", "fruit slicer", "kitchen tool"], aliases=["apple-corer"])
def _(S):
    out = [shell(circle(12, 12, 6.5)), shell(rect(2, 10.5, 4.5, 3, L(S, 0.4, 1.5))),
           shell(rect(17.5, 10.5, 4.5, 3, L(S, 0.4, 1.5))), detail(circle(12, 12, 1.7))]
    for a in range(-90, 270, 60):
        p0 = pt_on(12, 12, 1.7, a)
        p1 = pt_on(12, 12, 5.5, a)
        out.append(detail(seg(p0[0], p0[1], p1[0], p1[1])))
    return out


@icon("salad-spinner", CAT, "Salad spinner bowl with a lid, a pump knob and leaves inside",
      tags=["lettuce spinner", "salad dryer", "greens", "washing salad", "kitchen tool"])
def _(S):
    c = L(S, 1.5, 3)
    body = (f"M3 8H21V10.5H20.5L19 {fmt(20.5 - c)}Q18.8 20.5 {fmt(19 - c)} 20.5H{fmt(5 + c)}Q5.2 20.5 5 {fmt(20.5 - c)}"
            "L3.5 10.5H3Z")
    return [shell(body), detail(seg(3.5, 10.5, 20.5, 10.5)), line(seg(12, 5, 12, 8)),
            shell(rect(9.5, 2.5, 5, 2.5, L(S, 0.4, 1.25))),
            detail("M8 17.8C8 15 10.5 13.5 13.5 14C13.2 16.8 11 18.2 8 17.8Z")]


@icon("winged-corkscrew", CAT, "Winged corkscrew with both levers raised and a top knob",
      tags=["corkscrew", "wine opener", "bottle opener", "wine", "cork"], aliases=["wing-corkscrew"])
def _(S):
    knob = circle(12, 3.3, 1.6) if S.name == "rounded" else rect(10.5, 1.8, 3, 3)
    worm = "M12 16.5C14 17 14 18.2 12 18.6C10 19 10 20.2 12 20.6"
    return [shell(knob), shell(rect(10, 5.5, 4, 11, L(S, 0.5, 2))),
            line(seg(10, 9.5, 5.6, 5.3)), line(seg(14, 9.5, 18.4, 5.3)), dot(4.8, 4.5, 1.7), dot(19.2, 4.5, 1.7),
            line(worm), line(seg(12, 20.6, 12, 22))]


@icon("kitchen-shears", CAT, "Kitchen shears with straight blades, a serrated edge and thick loop handles",
      tags=["kitchen scissors", "poultry shears", "shears", "cutting", "herb scissors"], aliases=["kitchen-scissors"])
def _(S):
    left = poly([(12.8, 12.5), (8.2, 2.5), (10, 2.2), (13.4, 10.8)], closed=True, r=0)
    right = poly([(11.2, 12.5), (15.8, 2.5), (14.9, 3.8), (15.6, 4.3), (14.6, 5.6), (15.2, 6.1), (12.9, 10.3)],
                 closed=True, r=0)
    return tilt([shell(left, stroke_miterlimit="2"), shell(right, stroke_miterlimit="2"), dot(12, 11.3, 0.9),
                 line(ellipse(8.8, 18, 3, 3.5)), line(circle(15.6, 18.2, 2.3)),
                 line(seg(11.6, 13, 10.4, 14.8)), line(seg(12.4, 13, 13.8, 16.1))])


@icon("baster", CAT, "Turkey baster: a long tube with a squeeze bulb at one end",
      tags=["turkey baster", "bulb baster", "basting", "roast", "kitchen tool"], aliases=["turkey-baster"])
def _(S):
    return tilt([shell(ellipse(12, 5.2, 3.3, 3.8) if S.name == "rounded" else
                       "M12 1.4C14.3 1.4 15.3 3.2 15.3 5.2C15.3 7.3 14 9 12 9C10 9 8.7 7.3 8.7 5.2C8.7 3.2 9.7 1.4 12 1.4Z"),
                 shell(rect(9.5, 9, 5, 2, L(S, 0, 1))),
                 shell(poly([(10.2, 11), (13.8, 11), (12.8, 22), (11.2, 22)], closed=True, r=L(S, 0, 0.6)))])


@icon("kitchen-funnel", CAT, "Kitchen funnel with a wide cone, a narrow spout and a side ring tab",
      tags=["funnel", "pouring", "canning funnel", "liquids", "kitchen tool"])
def _(S):
    body = poly([(2.5, 5), (18.5, 5), (12.5, 13), (12.5, 21), (8.5, 21), (8.5, 13)], closed=True, r=S.r)
    ring = circle(20.2, 7.5, 1.7) if S.name == "rounded" else rect(18.5, 5.8, 3.4, 3.4)
    return [shell(body, stroke_miterlimit="3"), line(ring), detail(seg(5.2, 8, 15.8, 8))]


@icon("meat-tenderizer", CAT, "Meat tenderizer mallet with a spiked face on its head",
      tags=["meat mallet", "meat hammer", "tenderiser", "pounder", "kitchen tool"], aliases=["meat-mallet"])
def _(S):
    teeth = [(4, 3)]
    for i in range(3):
        y = 3 + i * 2.2
        teeth += [(2.5, y + 1.1), (4, y + 2.2)]
    head = poly(teeth + [(4, 9.6), (20, 9.6), (20, 3)], closed=True, r=0)
    return tilt([shell(head, stroke_miterlimit="2"), shell(rect(10.5, 9.6, 3, 12.4, L(S, 0.5, 1.5)))])


@icon("meat-thermometer", CAT, "Meat thermometer: a round dial on a long pointed probe",
      tags=["cooking thermometer", "probe thermometer", "roast", "temperature", "bbq", "grill"], aliases=["probe-thermometer"])
def _(S):
    probe = poly([(10.9, 14), (13.1, 14), (12, 22.5)], closed=True, r=L(S, 0, 0.5))
    return [shell(circle(12, 8, 6)), detail(seg(12, 8, 14.6, 5.4)), dot(12, 8, 1.3), shell(probe, stroke_miterlimit="6")]


@icon("molcajete", CAT, "Stone mortar on three short legs with a stubby pestle",
      tags=["mortar and pestle", "mortar", "pestle", "grinding", "guacamole", "salsa"])
def _(S):
    bowl = "M3 9.5H21C21 14.5 17 17.5 12 17.5C7 17.5 3 14.5 3 9.5Z"
    pestle = rot(rect(14, 2, 4, 7.5, L(S, 1, 2)), 25, 16, 9.5)
    return [shell(bowl), shell(pestle), dot(8, 12.3, 1), dot(12, 14.3, 1), dot(16, 12.3, 1),
            line(seg(7, 16.2, 6, 20.5)), line(seg(12, 17.5, 12, 21)), line(seg(17, 16.2, 18, 20.5))]
