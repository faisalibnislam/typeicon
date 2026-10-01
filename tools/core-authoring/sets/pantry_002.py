"""TypeIcon Core: pantry (batch pantry_002): baking staples, dried pasta shapes, takeaway packaging, food storage and food labels.

Objects are drawn in side or front view, kept to a few strong shapes so they read at 24 px.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path.parser import parse_path
from geometry import D, P, U, fmt, path_to_d, rotation

CAT = "pantry"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def tf(d, m):
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def rot(d, deg, cx=12.0, cy=12.0):
    """Rotate a d-string clockwise on screen about (cx, cy)."""
    return tf(d, rotation(deg, cx, cy))


def mv(d, dx, dy):
    return tf(d, (1, 0, 0, 1, dx, dy))


def flip(d):
    """Mirror across the vertical centre line."""
    return tf(d, (-1, 0, 0, 1, 24, 0))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def hole(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


# ============================================================================ baking staples

@icon("gelatin-sheets", CAT, "Two thin overlapping sheets of gelatin with diagonal ridges pressed into the front one",
      tags=["gelatine", "leaf gelatin", "baking", "setting agent", "dessert"])
def _(S):
    return [shell(rect(3.5, 8.5, 13, 12, rr(S, 2))), line("M7.5 8.5V4.5H20.5V16.5H16.5"),
            detail(seg(7, 13, 10, 10.5)), detail(seg(7, 17.5, 13, 12.5))]


@icon("powdered-sugar", CAT, "Dredger shaker with a perforated dome top dusting fine sugar downward",
      tags=["icing sugar", "confectioners sugar", "dusting", "shaker", "baking", "sprinkle"])
def _(S):
    c = L(S, 0, 2)
    body = f"M7 {fmt(13.5 - c)}V8A5 5 0 0 1 17 8V{fmt(13.5 - c)}" + (f"Q17 13.5 {fmt(17 - c)} 13.5H{fmt(7 + c)}Q7 13.5 7 {fmt(13.5 - c)}Z" if c else "H7Z")
    return [shell(body), detail(seg(7, 10, 17, 10)), hole(circle(10.5, 6.2, 0.9)), hole(circle(13.5, 6.2, 0.9)),
            dot(8.5, 17.5, 1.25), dot(15.5, 17.5, 1.25), dot(12, 19.5, 1.25), dot(12, 16, 1.0)]


@icon("chocolate-chips", CAT, "Small heap of chocolate chips with flat bottoms and pointed tops",
      tags=["chocolate drops", "choc chips", "baking", "cookie", "dessert", "morsels"])
def _(S):
    def chip(cx, b, w=3.6, h=8.0):
        if S.name == "line":
            return (f"M{fmt(cx - w)} {fmt(b)}C{fmt(cx - w)} {fmt(b - 3.5)} {fmt(cx - 1)} {fmt(b - h + 2.5)} {fmt(cx)} {fmt(b - h)}"
                    f"C{fmt(cx + 1)} {fmt(b - h + 2.5)} {fmt(cx + w)} {fmt(b - 3.5)} {fmt(cx + w)} {fmt(b)}Z")
        return (f"M{fmt(cx - w)} {fmt(b)}C{fmt(cx - w)} {fmt(b - 3.5)} {fmt(cx - 1.8)} {fmt(b - h + 2)} {fmt(cx)} {fmt(b - h + 0.3)}"
                f"C{fmt(cx + 1.8)} {fmt(b - h + 2)} {fmt(cx + w)} {fmt(b - 3.5)} {fmt(cx + w)} {fmt(b)}Z")
    return [shell(chip(12, 10.5)), shell(chip(6.5, 20.5)), shell(chip(17.5, 20.5))]


@icon("puff-pastry", CAT, "Sheet of puff pastry unrolling from a roll with a flat layered sheet",
      tags=["pastry dough", "croissant dough", "laminated dough", "baking", "pie crust", "roll"])
def _(S):
    k = math.sqrt(36 - 6.25)
    sheet = poly([(8 + k, 14.5), (21.5, 14.5), (21.5, 18), (8, 18)], r=S.r)
    return [shell(circle(8, 12, 6)), line(sheet), detail("M8 12m0-2a2 2 0 1 1-2 2")]


@icon("fondant", CAT, "Cake tier draped in a smooth sheet of fondant with a scalloped edge",
      tags=["sugar paste", "icing", "cake decorating", "rolled fondant", "baking", "frosting"])
def _(S):
    arcs = "".join(f"A2.125 2.125 0 0 0 {fmt(20.5 - 4.25 * i)} 12" for i in range(1, 5))
    drape = "M3.5 9C3.5 6 7.5 4.5 12 4.5C16.5 4.5 20.5 6 20.5 9V12" + arcs + "Z"
    return [shell(drape), line("M5.75 14V20.5H18.25V14")]


@icon("parchment-paper", CAT, "Dispenser box of baking parchment with a sheet pulled out over the serrated edge",
      tags=["baking paper", "greaseproof paper", "baking sheet liner", "kitchen", "roll"])
def _(S):
    return [shell(rect(3.5, 14.5, 17, 6, rr(S, 2))), line("M6.5 14.5V3.5H17.5V14.5"),
            detail(poly([(7, 18.5), (9.5, 16.5), (12, 18.5), (14.5, 16.5), (17, 18.5)], r=S.r))]


@icon("jaggery", CAT, "Domed block of unrefined jaggery sugar with a broken chunk beside it",
      tags=["gur", "panela", "unrefined sugar", "cane sugar", "sweetener", "indian sweet"])
def _(S):
    dome = "M2.5 19C2.5 12.5 5.5 8.5 9 8.5C12.5 8.5 15.5 12.5 15.5 19Z"
    chunk = poly([(18, 19), (18, 15), (21.5, 14), (21.5, 19)], closed=True, r=S.r)
    return [shell(dome), shell(chunk), detail(poly([(10, 12), (8.5, 14.5), (10, 16)], r=S.r))]


@icon("sugar-loaf", CAT, "Tall cone of hard sugar with its tip twisted in paper",
      tags=["sugarloaf", "sugar cone", "cone sugar", "preserved sugar", "old fashioned", "sweetener"])
def _(S):
    return [shell(poly([(4, 20.5), (12, 8), (20, 20.5)], closed=True, r=S.r)),
            detail(seg(7.5, 14.5, 16.5, 14.5)), line("M12 8L9.5 3.5"), line("M12 8L14.5 3.5")]


@icon("sweetener-dispenser", CAT, "Pocket click dispenser with a top button dropping small sweetener tablets",
      tags=["sugar substitute", "tablets", "diet", "saccharin", "stevia", "coffee", "sweetener"])
def _(S):
    return [shell(rect(3.5, 9, 10, 11.5, rr(S, 3))), shell(rect(6, 4.5, 5, 4.5, rr(S, 1.5))),
            detail(seg(6.5, 14, 10.5, 14)), line(seg(13.5, 12, 17, 12)),
            dot(19, 14.5, 1.5), dot(19, 19, 1.5)]


@icon("dough-tube", CAT, "Spiral-wound cardboard tube burst open with dough puffing out of the top",
      tags=["canned dough", "pop tube", "biscuit dough", "refrigerated dough", "baking", "crescent rolls"])
def _(S):
    body = union(rect(6, 12, 12, 9, rr(S, 2)), circle(9.5, 9, 3.5), circle(14.5, 8.5, 4), circle(12, 7, 3.5))
    return [shell(body), detail(seg(6, 18, 11, 14)), detail(seg(13, 20, 18, 16))]


@icon("cookie-dough-log", CAT, "Log of cookie dough with a round cut face and two round slices cut off below",
      tags=["icebox cookies", "slice and bake", "refrigerator cookies", "baking", "dough roll"])
def _(S):
    return [shell(union(rect(3, 3.5, 14.5, 9.5, rr(S, 2)), ellipse(17.5, 8.25, 3, 4.75))), detail(ellipse(17.5, 8.25, 0.1, 0.1)) if False else detail(seg(17.5, 5.5, 17.5, 11)),
            shell(circle(8, 18.5, 3.25)), shell(circle(16, 18.5, 3.25))]


@icon("turmeric", CAT, "Knobby turmeric root with a cut end beside a small heap of yellow powder",
      tags=["haldi", "curcuma", "spice", "ground spice", "root", "golden milk", "curry"])
def _(S):
    root = union(rot(rect(2.5, 6.5, 13, 5.5, L(S, 2, 2.75)), 40, 9, 9), rot(rect(4, 11, 4, 5, L(S, 1.5, 2)), 40, 9, 9))
    heap = "M11.5 20.5C11.5 16.5 14.5 14.5 16.75 14.5C19 14.5 22 16.5 22 20.5Z"
    return [shell(root), shell(heap), dot(16.75, 18, 0.9)]


@icon("halva", CAT, "Marbled slab of halva with a wedge cut off and set beside it",
      tags=["halwa", "halvah", "sesame sweet", "tahini", "dessert", "confection"])
def _(S):
    wedge = poly([(18.5, 20), (18.5, 12.5), (21.5, 20)], closed=True, r=S.r)
    return [shell(rect(2.5, 5, 13, 14.5, rr(S, 2.5))), shell(wedge),
            detail("M5.5 10C7 8 9 8 10 10C11 12 13 12 13 10"), detail("M5.5 15.5C7 13.5 9 13.5 10 15.5C11 17 12.5 16.5 13 15.5")]


@icon("katsuobushi", CAT, "Hard dried bonito block with curled shavings coiling off the top",
      tags=["bonito flakes", "dried bonito", "dashi", "japanese", "fish flakes", "shavings"])
def _(S):
    def spiral(cx, cy, r0, r1, turns, a0, n=14):
        pts = []
        for i in range(n + 1):
            t = i / n
            pts.append(pt_on(cx, cy, r0 + (r1 - r0) * t, a0 + 360 * turns * t))
        return poly(pts, r=0)
    return [shell(rect(2.5, 13, 13, 7.5, rr(S, 2.5))), detail(seg(6, 16.75, 12, 16.75)),
            line(spiral(16.5, 8, 0.9, 4.6, 1.3, 200, 18)), line("M17 19C18.5 17 20.5 17 21.5 15")]


@icon("dried-fish", CAT, "Flat dried fish with a forked tail, hanging from a hook",
      tags=["salted fish", "stockfish", "bacalao", "cured fish", "smoked fish", "preserved"])
def _(S):
    body = "M12 8C16.5 10 16.5 15 12 18.5C7.5 15 7.5 10 12 8Z"
    return [shell(body), line(poly([(8.5, 21.5), (12, 18.5), (15.5, 21.5)], r=S.r)), line("M12 8V4.5A1.75 1.75 0 1 0 10.25 2.75"),
            dot(12, 11.5, 1.0)]

# ============================================================================ asian staples, tea and spices

def wavy(x0, x1, y, n, amp, first_up=True):
    """Smooth wave segment (no leading M) from x0 to x1 at height y, n half-waves; returns path text starting with Q."""
    step = (x1 - x0) / n
    out = []
    sign = -1 if first_up else 1
    for i in range(n):
        xc = x0 + step * (i + 0.5)
        xe = x0 + step * (i + 1)
        out.append(f"Q{fmt(xc)} {fmt(y + sign * amp * 2)} {fmt(xe)} {fmt(y)}")
        sign = -sign
    return "".join(out)


def star(cx, cy, ro, ri, n=5):
    pts = []
    for i in range(n * 2):
        a = -90 + i * 180 / n
        r = ro if i % 2 == 0 else ri
        pts.append(pt_on(cx, cy, r, a))
    return pts


@icon("dumpling-wrappers", CAT, "Stack of thin dumpling wrappers with a folded half-moon pleated along its curved edge",
      tags=["gyoza wrappers", "wonton wrappers", "dough rounds", "pot sticker", "asian cooking", "dumpling skin"])
def _(S):
    pts = [pt_on(12, 12, 8, 180 + 36 * i) for i in range(6)]
    edge = "".join(f"A4.4 4.4 0 0 1 {fmt(x)} {fmt(y)}" for x, y in pts[1:])
    half = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}{edge}Z"
    return [shell(half), line("M4 15.5A8 2.5 0 0 0 20 15.5"), line("M4 19.5A8 2.5 0 0 0 20 19.5")]


@icon("rice-paper", CAT, "Round translucent rice paper sheet with a woven crosshatch texture",
      tags=["spring roll wrapper", "banh trang", "summer roll", "vietnamese", "wrapper", "asian cooking"])
def _(S):
    edge = poly(regular(12, 12, 9, 12, start=-75), closed=True, r=0) if S.name == "line" else circle(12, 12, 9)
    return [shell(edge), detail(seg(3.5, 9, 20.5, 9)), detail(seg(3.5, 15, 20.5, 15)),
            detail(seg(9, 3.5, 9, 20.5)), detail(seg(15, 3.5, 15, 20.5))]


@icon("noodle-nest", CAT, "Round nest of dried wavy egg noodles coiled into a loose ball",
      tags=["egg noodles", "dried noodles", "ramen", "pasta nest", "tagliatelle", "coil"])
def _(S):
    w1 = poly([(6, 10), (8.5, 8.5), (11, 10), (13.5, 8.5), (16, 10), (18, 9)], r=S.r)
    w2 = poly([(6, 15), (8.5, 13.5), (11, 15), (13.5, 13.5), (16, 15), (18, 14)], r=S.r)
    return [shell(ellipse(12, 12, 9.5, 7.5)), detail(w1), detail(w2)]


@icon("noodle-bundle", CAT, "Straight bundle of long dried noodles tied with a paper band around the middle",
      tags=["somen", "soba", "vermicelli", "dried noodles", "spaghetti bundle", "ramen", "pasta"])
def _(S):
    out = [shell(rect(4.5, 9.5, 15, 5.5, rr(S, 2)))]
    for x in (6.5, 10.25, 14, 17.5):
        out += [line(seg(x, 2.5, x, 9.5)), line(seg(x, 15, x, 21.5))]
    return out


@icon("puffed-rice-cake", CAT, "Thick round puffed rice cake seen from the side with a lipped top face",
      tags=["rice cracker", "rice cake", "puffed grain", "healthy snack", "popped rice", "diet"])
def _(S):
    ry = L(S, 3.6, 4.6)
    body = union(ellipse(12, 9.5, 9, ry), rect(3, 9.5, 18, 6.5, 0), ellipse(12, 16, 9, ry))
    return [shell(body), detail(f"M3 9.5A9 {ry} 0 0 0 21 9.5"), hole(rect(7.5, 13.2, 3, 1.4)), hole(rect(13.5, 14.2, 3, 1.4))]


@icon("tea-brick", CAT, "Pressed brick of tea leaves with an embossed inner border and a chipped corner",
      tags=["pu-erh", "compressed tea", "brick tea", "tea cake", "chinese tea", "tea leaves"])
def _(S):
    brick = poly([(3, 5.5), (14, 5.5), (16, 8.5), (18.5, 7.5), (21, 10.5), (21, 18.5), (3, 18.5)], closed=True, r=S.r)
    return [shell(brick), detail(rect(6.5, 9, 11, 6.5, rr(S, 1.5)))]


@icon("tea-chest", CAT, "Wooden tea crate with slatted sides, loose tea leaves heaped above the lid",
      tags=["tea crate", "tea box", "bulk tea", "plantation", "tea trade", "wooden crate"])
def _(S):
    return [shell(rect(3, 10.5, 18, 10, L(S, 0.5, 3))), detail(seg(3.5, 14.5, 20.5, 14.5)),
            detail(seg(9, 15, 9, 20)), detail(seg(15, 15, 15, 20)),
            dot(12, 4, 1.25), dot(9.2, 6.6, 1.25), dot(14.8, 6.6, 1.25)]


@icon("spice-sacks", CAT, "Row of three bins each heaped with a rounded mound of ground spice",
      tags=["spice market", "bazaar", "bulk spices", "powder", "souk", "ground spices", "sacks"])
def _(S):
    out = [shell(rect(2.5, 14, 19, 6.5, rr(S, 4)))]
    for cx in (6.25, 12, 17.75):
        out.append(line(f"M{fmt(cx - 2.75)} 14C{fmt(cx - 2.75)} 11 {fmt(cx - 1.25)} 7.5 {fmt(cx)} 7.5C{fmt(cx + 1.25)} 7.5 {fmt(cx + 2.75)} 11 {fmt(cx + 2.75)} 14"))
    return out


# ============================================================================ pasta shapes

@icon("rigatoni", CAT, "Two short wide ridged pasta tubes with square-cut ends",
      tags=["pasta", "tube pasta", "penne", "italian", "macaroni", "pasta shapes", "ridged"])
def _(S):
    def tube(x, y):
        return [shell(union(rect(x, y, 11, 6.5, rr(S, 2)), ellipse(x + 11, y + 3.25, 2.25, 3.25))),
                detail(seg(x + 3, y + 3.25, x + 9, y + 3.25))]
    return tube(3, 4.5) + tube(6, 13.5)


@icon("radiatori", CAT, "Short chunky pasta with a ruffled top and bottom and rows of fins like a little radiator",
      tags=["pasta", "radiator pasta", "fins", "ruffled pasta", "italian", "pasta shapes"])
def _(S):
    body = f"M3 8{wavy(3, 21, 8, 6, 0.9)}V17{wavy(21, 3, 17, 6, 0.9)}Z"
    return [shell(body), detail(seg(8, 11, 8, 14)), detail(seg(12, 11, 12, 14)), detail(seg(16, 11, 16, 14))]


@icon("campanelle", CAT, "Bell-shaped pasta with a rolled cone centre and a ruffled flared edge",
      tags=["pasta", "gigli", "bell pasta", "flower pasta", "italian", "pasta shapes", "cornetti"])
def _(S):
    arcs = "".join(f"A2.125 2.125 0 0 1 {fmt(20.5 - 4.25 * i)} 15.5" for i in range(1, 5))
    bell = "M10 4H14C14 9 18 11 20.5 15.5" + arcs.replace(" 0 0 1 ", " 0 0 1 ") + "C6 11 10 9 10 4Z"
    return [shell(bell), detail("M12 4C11 8 13.5 11 12 15")]


@icon("cavatappi", CAT, "Hollow ridged pasta tube twisted into a corkscrew spiral",
      tags=["pasta", "corkscrew pasta", "macaroni", "spiral pasta", "italian", "pasta shapes", "twist"])
def _(S):
    out = []
    for y in (4.5, 9, 13.5, 18):
        out.append(line(rot(f"M4 {fmt(y)}A8 3.2 0 0 0 20 {fmt(y)}", 14)))
    return out


@icon("lasagna-sheet", CAT, "Flat pasta sheet with ruffled wavy long edges, a second sheet peeking out behind",
      tags=["pasta", "lasagne", "noodle sheets", "italian", "baked pasta", "pasta sheets"])
def _(S):
    front = f"M3 11.5{wavy(3, 21, 11.5, 4, 1)}V20{wavy(21, 3, 20, 4, 1)}Z"
    back = f"M6 6.5{wavy(6, 21.5, 6.5, 4, 1)}"
    return [shell(front), line(back)]


@icon("alphabet-pasta", CAT, "Spoon holding small pasta letters in a scatter",
      tags=["letter pasta", "soup pasta", "abc", "kids food", "soup", "pastina", "spoon"])
def _(S):
    bowl = rot(ellipse(9.5, 9.5, 5.8, 7.2), -45, 9.5, 9.5)
    handle = rot(rect(8.5, 16.5, 2.2, 6.5, L(S, 0, 1.1)), -45, 9.5, 9.5)
    return [shell(bowl), shell(handle),
            hole(rect(6.8, 7, 4, 1.5)), hole(rect(8.05, 7, 1.5, 4.5)), hole(rect(10.6, 10.6, 1.5, 4)),
            hole(rect(10.6, 13.1, 3.8, 1.5))]


@icon("stelline", CAT, "Scatter of tiny star-shaped soup pasta with small holes through the centres",
      tags=["star pasta", "pastina", "soup pasta", "baby food", "italian", "little stars"])
def _(S):
    k = S.r * 0.35
    return [shell(poly(star(7, 7.5, 5, 2.5), closed=True, r=k)), shell(poly(star(17, 10, 4.8, 2.4), closed=True, r=k)),
            shell(poly(star(8.5, 17.5, 4.6, 2.3), closed=True, r=k)), dot(18, 18.5, 1.25)]


def lens(cx, cy, rx, ry, deg, S):
    """Plump grain: pointed lens in Line, smooth ellipse in Rounded, turned by deg."""
    if S.name == "line":
        d = (f"M{fmt(cx - rx)} {fmt(cy)}Q{fmt(cx)} {fmt(cy - ry * 2)} {fmt(cx + rx)} {fmt(cy)}"
             f"Q{fmt(cx)} {fmt(cy + ry * 2)} {fmt(cx - rx)} {fmt(cy)}Z")
    else:
        d = ellipse(cx, cy, rx, ry)
    return rot(d, deg, cx, cy)


@icon("orzo", CAT, "Small pile of plump rice-shaped orzo pasta grains",
      tags=["pasta", "risoni", "rice shaped pasta", "italian", "soup pasta", "greek", "pasta shapes"])
def _(S):
    return [shell(lens(7, 7, 4.2, 2.1, -25, S)), shell(lens(17, 8, 4.2, 2.1, 30, S)),
            shell(lens(7.5, 17, 4.2, 2.1, 25, S)), shell(lens(17, 17.5, 4.2, 2.1, -20, S)),
            shell(lens(12, 12.5, 3.6, 1.8, 90, S))]


@icon("gemelli", CAT, "Two strands of pasta twisted around each other like a double helix",
      tags=["pasta", "twins pasta", "twisted pasta", "braid", "italian", "pasta shapes", "spiral"])
def _(S):
    a = "M3 17.5C8 17.5 8 6.5 12 6.5C16 6.5 16 17.5 21 17.5"
    b = "M3 6.5C8 6.5 8 17.5 12 17.5C16 17.5 16 6.5 21 6.5"
    return [line(a), line(b)]


@icon("ditalini", CAT, "Several very short small pasta tubes seen at an angle showing their round holes",
      tags=["pasta", "thimbles", "soup pasta", "short tubes", "italian", "macaroni", "pasta shapes"])
def _(S):
    def tube(x, y):
        return [shell(union(rect(x, y, 6, 5.5, rr(S, 1.5)), ellipse(x + 6, y + 2.75, 2, 2.75))),
                hole(ellipse(x + 6, y + 2.75, 0.7, 1.2))]
    return tube(2.5, 3) + tube(13, 9) + tube(3.5, 15.5)


@icon("anelli", CAT, "Scatter of small thin rings of pasta with a few overlapping",
      tags=["pasta", "rings", "anellini", "soup pasta", "italian", "hoops", "pasta shapes"])
def _(S):
    def ring(cx, cy, r):
        return poly(regular(cx, cy, r, 10, start=-90), closed=True, r=0) if S.name == "line" else circle(cx, cy, r)
    return [shell(ring(7, 7.5, 3.6)), shell(ring(12.5, 9.5, 3.6)), shell(ring(6.5, 17, 3.4)), shell(ring(16.5, 17, 3.4))]


@icon("mafaldine", CAT, "Long flat ribbon of pasta with both edges ruffled into tight waves",
      tags=["pasta", "reginette", "ribbon pasta", "ruffled", "italian", "pasta shapes", "noodle"])
def _(S):
    body = f"M3.5 9{wavy(3.5, 20.5, 9, 8, 0.9)}V15{wavy(20.5, 3.5, 15, 8, 0.9)}Z"
    return [shell(rot(body, -25, 12, 12))]


@icon("creste-di-gallo", CAT, "Curved tube of pasta with a ruffled crest along its outer curve like a rooster comb",
      tags=["pasta", "cockscomb", "rooster comb", "crested pasta", "italian", "pasta shapes", "tube"])
def _(S):
    cx, cy, ro, ri = 12, 18, 10.5, 5.5
    outer = [pt_on(cx, cy, ro, 190 + i * 20) for i in range(9)]
    if S.name == "line":
        outer = [pt_on(cx, cy, ro - 1.3 + (1.3 if i % 2 else 0), 190 + i * 10) for i in range(17)]
        edge = "".join(f"L{fmt(x)} {fmt(y)}" for x, y in outer[1:])
    else:
        edge = "".join(f"A2.6 2.6 0 0 1 {fmt(x)} {fmt(y)}" for x, y in outer[1:])
    e0, e1 = outer[0], outer[-1]
    i0, i1 = pt_on(cx, cy, ri, 190), pt_on(cx, cy, ri, 350)
    d = (f"M{fmt(e0[0])} {fmt(e0[1])}{edge}L{fmt(i1[0])} {fmt(i1[1])}A{ri} {ri} 0 0 0 {fmt(i0[0])} {fmt(i0[1])}Z")
    return [shell(d)]


# ============================================================================ takeaway and food packaging

@icon("foil-container", CAT, "Rectangular foil takeaway tray with sloped sides and a card lid lifted at one edge",
      tags=["aluminium tray", "aluminum tray", "takeaway", "takeout", "foil pan", "food packaging", "leftovers"])
def _(S):
    tray = poly([(3, 12), (21, 12), (18.5, 20.5), (5.5, 20.5)], closed=True, r=S.r)
    return [shell(tray), line("M3 12L19 5"), detail(seg(9, 15, 9, 18)), detail(seg(15, 15, 15, 18))]


@icon("soup-to-go-cup", CAT, "Round paper soup cup with a vented domed lid and a wisp of steam",
      tags=["takeaway soup", "hot food", "paper cup", "takeout", "steam", "food packaging", "coffee cup"])
def _(S):
    cup = union("M4.5 10C4.5 7 8 6 12 6C16 6 19.5 7 19.5 10Z",
                poly([(5.5, 9), (18.5, 9), (17, 21), (7, 21)], closed=True, r=S.r))
    return [shell(cup), detail(seg(5, 10.5, 19, 10.5)), line("M12 4C10.5 3 13.5 2.5 12 1.5", ), hole(circle(12, 7.6, 0.6))]


@icon("salad-container", CAT, "Clear round salad bowl with a domed lid and leaves visible inside",
      tags=["salad bowl", "lunch", "takeaway", "healthy", "meal prep", "food packaging", "greens"])
def _(S):
    if S.name == "line":
        bowl = "M3 12H21C21 16 19.5 20.5 16 20.5H8C4.5 20.5 3 16 3 12Z"
    else:
        bowl = "M3 12H21C21 17 17 20.5 12 20.5C7 20.5 3 17 3 12Z"
    return [shell(bowl), line("M5 12C5 6.5 8 4.5 12 4.5C16 4.5 19 6.5 19 12"),
            detail("M8.5 12C8.5 9 10.5 8 12.5 8.5C12.5 10.8 11 12 8.5 12")]


@icon("sushi-pack", CAT, "Rectangular plastic tray with a clear lid over a row of sushi pieces",
      tags=["sushi tray", "takeaway", "japanese", "maki", "supermarket sushi", "food packaging", "bento"])
def _(S):
    return [shell(rect(2.5, 13, 19, 7.5, rr(S, 3))), line("M4 13V5H20V13"),
            solid(rect(5, 7.5, 4, 3.5, 1)), solid(rect(10, 7.5, 4, 3.5, 1)), solid(rect(15, 7.5, 4, 3.5, 1))]


@icon("paper-food-boat", CAT, "Open shallow paper tray with folded corners holding a heap of fries",
      tags=["fries tray", "chips", "street food", "takeaway", "snack tray", "food packaging", "french fries"])
def _(S):
    tray = poly([(3, 12), (21, 12), (18.5, 20.5), (5.5, 20.5)], closed=True, r=S.r)
    out = [shell(tray), detail(seg(5.5, 15.5, 18.5, 15.5))]
    for x, top in ((7.5, 5.5), (11, 3), (14.5, 4.5), (18, 6)):
        out.append(line(seg(x, top, x, 12)))
    return out


@icon("paper-cone", CAT, "Rolled paper cone with an open top and small round snacks heaped above",
      tags=["cone cup", "street food", "chips cone", "nuts", "popcorn", "takeaway", "food packaging"])
def _(S):
    return [shell(poly([(4.5, 9), (19.5, 9), (12, 21)], closed=True, r=S.r)), detail(seg(9, 10.5, 13.5, 17.5)),
            dot(7.8, 5.6, 1.7), dot(12, 4.4, 1.7), dot(16.2, 5.6, 1.7)]


@icon("disposable-cutlery-pack", CAT, "Sealed clear sleeve holding a plastic fork, knife and folded napkin side by side",
      tags=["takeaway cutlery", "plastic cutlery", "utensil kit", "napkin", "takeout", "food packaging", "fork knife"])
def _(S):
    return [shell(rect(2.5, 3, 19, 18, rr(S, 3))),
            detail("M5.5 7V9.5A1.5 1.5 0 0 0 8.5 9.5V7"), detail(seg(7, 11, 7, 17.5)),
            hole(rect(11, 6.5, 3, 6, 1.4)), hole(rect(11.8, 12, 1.4, 6)),
            hole(rect(16.2, 9, 3.4, 8.5, 0.8))]


@icon("pizza-slice-box", CAT, "Triangular cardboard pizza slice box with its lid hinged open over a single slice",
      tags=["pizza box", "slice", "takeaway", "takeout", "food packaging", "cardboard", "pizzeria"])
def _(S):
    return [shell(poly([(3, 12), (21, 12), (12, 21.5)], closed=True, r=S.r)), line("M3 12L5.5 3.5H18.5L21 12"),
            detail(seg(8, 14.5, 16, 14.5)), dot(12, 17, 1.0)]


@icon("pizza-saver", CAT, "Tiny three-legged plastic stand seen from the side like a little table",
      tags=["pizza stand", "box support", "pizza box", "takeaway", "food packaging", "tripod", "spacer"])
def _(S):
    return [shell(rect(3.5, 7, 17, 4.5, rr(S, 2))), line(seg(7, 11.5, 7, 19)), line(seg(12, 11.5, 12, 19)),
            line(seg(17, 11.5, 17, 19))]


# ============================================================================ lunch carriers and food keepers

def flute(cx, cy, rx, ry, n, dip, S):
    """Closed polygon of a fluted or scalloped round edge (alternating radii)."""
    pts = []
    for i in range(n * 2):
        a = math.radians(i * 180 / n)
        k = 1.0 if i % 2 == 0 else 1 - dip
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    return poly(pts, closed=True, r=S.r)


@icon("paper-plate", CAT, "Round disposable paper plate with a fluted rim seen at an angle",
      tags=["disposable plate", "party", "picnic", "takeaway", "food packaging", "barbecue", "tableware"])
def _(S):
    return [shell(flute(12, 12, 9.6, 7.4, 12, 0.1, S)), detail(ellipse(12, 12, 5.2, 3.1))]


@icon("burger-wrapper", CAT, "Burger with its top bun showing, half wrapped in a folded sheet of paper",
      tags=["hamburger", "fast food", "takeaway", "sandwich wrap", "food packaging", "cheeseburger", "paper wrap"])
def _(S):
    bun = "M5.5 12C5.5 6.5 8 4 12 4C16 4 18.5 6.5 18.5 12Z"
    wrap = poly([(3.5, 11.5), (20.5, 11.5), (19, 20.5), (5, 20.5)], closed=True, r=S.r)
    return [shell(union(bun, wrap)), detail(seg(3.5, 11.5, 20.5, 11.5)),
            detail(poly([(8, 15.5), (12, 18), (16, 15.5)], r=S.r)),
            hole(circle(9.5, 7.8, 0.8)), hole(circle(12.5, 6.6, 0.8)), hole(circle(15, 8.3, 0.8))]


@icon("lunch-pail", CAT, "Metal lunch box with a domed lid, a front latch and a wire handle on top",
      tags=["lunch box", "lunchbox", "tin lunch box", "packed lunch", "school lunch", "work lunch", "workman"])
def _(S):
    body = union("M3 11.5C3 6.5 7 5.5 12 5.5C17 5.5 21 6.5 21 11.5Z", rect(3, 11, 18, 9.5, rr(S, 2.5)))
    return [shell(body), detail(seg(3, 11.25, 21, 11.25)), hole(rect(10.5, 9.5, 3, 4.5, 0.8)),
            line("M7.5 5.8C7.5 2.3 16.5 2.3 16.5 5.8")]


@icon("lunch-bag", CAT, "Soft insulated lunch bag with a zip along the top and a carry handle",
      tags=["cooler bag", "insulated bag", "packed lunch", "school lunch", "work lunch", "thermal bag", "tote"])
def _(S):
    return [shell(rect(3.5, 9, 17, 12, rr(S, 4))), detail("M3.5 12.5C8.5 14.2 15.5 14.2 20.5 12.5"),
            line("M8.5 9C8.5 3.5 15.5 3.5 15.5 9")]


@icon("insulated-food-jar", CAT, "Short wide vacuum food jar with a screw lid and a folding spoon clipped to the side",
      tags=["thermos", "food flask", "soup flask", "lunch", "thermal jar", "vacuum flask", "hot lunch"])
def _(S):
    return [shell(rect(3.5, 8.5, 13, 12.5, rr(S, 3))), shell(rect(3, 4.5, 14, 4, rr(S, 1.5))),
            detail(seg(6, 13, 14, 13)), line(seg(20, 11.5, 20, 19)), solid(ellipse(20, 8.6, 1.6, 2.4))]


@icon("banana-case", CAT, "Hard curved banana-shaped case with a stem and a small clasp",
      tags=["banana guard", "fruit protector", "lunch", "travel", "snack case", "fruit case", "banana holder"])
def _(S):
    tip = "L22.2 18.9L20.5 17.2" if S.name == "line" else "C22.3 20.4 22.3 17.6 20.5 17.2"
    d = ("M5 3.5C3 3.5 3 5.5 3.2 7C4 15 9.5 21 20.5 20.5" + tip
         + "C14 16 10.2 12.5 9 5C8.8 3.8 7 3.5 5 3.5Z")
    return [shell(d), hole(circle(9.5, 12.3, 1.1))]


@icon("travel-cutlery-set", CAT, "Flat zipped case open to show a fork, a spoon and a pair of chopsticks in slots",
      tags=["portable cutlery", "camping cutlery", "reusable utensils", "chopsticks", "lunch", "zero waste", "utensil roll"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 17, rr(S, 3))),
            hole(rect(5, 6.5, 1.4, 4.2)), hole(rect(7.6, 6.5, 1.4, 4.2)), hole(rect(5, 10, 4, 1.4)), hole(rect(6.3, 11, 1.4, 6.5)),
            hole(ellipse(12.5, 8.6, 1.5, 2.3)), hole(rect(11.8, 10.5, 1.4, 7)),
            hole(rect(16.2, 6.5, 1.3, 11)), hole(rect(18.6, 6.5, 1.3, 11))]


@icon("silica-gel-packet", CAT, "Small sachet with a crimped top edge and tiny round beads inside",
      tags=["desiccant", "moisture absorber", "do not eat", "dry packet", "food safety", "packaging", "sachet"])
def _(S):
    return [shell(rect(4, 3.5, 16, 17, rr(S, 2.5))), detail(seg(4, 6.75, 20, 6.75)),
            dot(8.5, 10.5, 1.2), dot(15.5, 10.5, 1.2), dot(12, 13.5, 1.2), dot(8.5, 16.5, 1.2), dot(15.5, 16.5, 1.2)]


@icon("cake-dome", CAT, "Round glass dome with a knob handle covering a cake on a flat plate",
      tags=["cake stand", "cake cover", "cake keeper", "glass cloche", "bakery", "pastry display", "dessert"])
def _(S):
    return [shell(rect(2.5, 17.5, 19, 3.5, L(S, 0, 1.75))), line("M4.5 17.5C4.5 9 8 6 12 6C16 6 19.5 9 19.5 17.5"),
            dot(12, 3.8, 1.4), detail(rect(8.5, 12, 7, 5.5, 0.5))]


@icon("cheese-dome", CAT, "Low glass bell cover with a knob handle over a wedge of cheese on a board",
      tags=["cheese cover", "cheese keeper", "cheese board", "cloche", "deli", "dairy", "fromage"])
def _(S):
    return [shell(rect(2.5, 15.5, 19, 4.5, L(S, 0, 2.25))), line("M3.5 15.5C3.5 9.5 7.5 8 12 8C16.5 8 20.5 9.5 20.5 15.5"),
            dot(12, 5.8, 1.4), solid(poly([(8, 14.5), (16, 14.5), (16, 11)], closed=True, r=0.5))]


@icon("pantry-bin", CAT, "Clear rectangular storage bin with a cutout handle at the front holding small packets",
      tags=["storage bin", "pantry organizer", "organiser", "food storage", "clear bin", "kitchen organisation", "container"])
def _(S):
    bin_ = poly([(3, 9.5), (21, 9.5), (19.5, 20.5), (4.5, 20.5)], closed=True, r=S.r)
    return [shell(bin_), detail(rect(8.5, 12, 7, 3.2, rr(S, 1.6))), line("M6.5 9.5V4.5H10.5V9.5"), line("M13 9.5V3.5H17.5V9.5")]


@icon("rice-dispenser", CAT, "Upright grain bin with a push button on the front releasing rice into a small cup",
      tags=["cereal dispenser", "grain dispenser", "rice bin", "dry food storage", "pantry", "kitchen", "rice"])
def _(S):
    bin_ = poly([(4, 2.5), (16, 2.5), (16, 10.5), (11.5, 14), (8.5, 14), (4, 10.5)], closed=True, r=S.r)
    return [shell(bin_), hole(circle(10, 7, 1.8)), dot(9, 16.2, 0.8), dot(11.2, 17.2, 0.8),
            line(poly([(5.5, 18.5), (6.5, 21.5), (13.5, 21.5), (14.5, 18.5)], r=S.r))]


@icon("herb-keeper", CAT, "Tall clear container with a lid holding a bunch of fresh herbs standing in a little water",
      tags=["herb saver", "fresh herbs", "cilantro keeper", "parsley", "produce keeper", "fridge storage", "greens"])
def _(S):
    return [shell(rect(6.5, 7, 11, 14, rr(S, 3))), shell(rect(5.5, 3.5, 13, 3.5, rr(S, 1.5))),
            detail("M6.5 18C8.5 16.8 10 19.2 12 18C14 16.8 15.5 19.2 17.5 18"),
            detail(seg(9.8, 16, 9.8, 11)), detail(seg(14.2, 16, 14.2, 11)), hole(circle(9.8, 10.4, 1.3)), hole(circle(14.2, 10.4, 1.3))]


@icon("avocado-keeper", CAT, "Avocado-shaped storage container holding half an avocado with the pit in place",
      tags=["avocado saver", "guacamole", "produce keeper", "fridge storage", "fruit saver", "avocado holder"])
def _(S):
    if S.name == "line":
        top = "M12 2.5C13.5 4.5 14.6 7 16.5 9.3"
    else:
        top = "M12 3C14.5 3 15 6.5 16.5 9.3"
    d = (top + "C18.5 12 19 14 19 15.5C19 19 16 21 12 21C8 21 5 19 5 15.5C5 14 5.5 12 7.5 9.3"
         + ("C9.4 7 10.5 4.5 12 2.5Z" if S.name == "line" else "C9 6.5 9.5 3 12 3Z"))
    return [shell(d), detail(seg(8, 9.3, 16, 9.3)), detail(circle(12, 15, 2.6))]


@icon("bowl-cover", CAT, "Bowl under a stretchy fabric cover gathered with elastic around the rim",
      tags=["food cover", "reusable cover", "zero waste", "leftovers", "kitchen", "stretch lid", "bowl lid"])
def _(S):
    dome = ("M2.5 12.5L5 8L12 6.5L19 8L21.5 12.5Z" if S.name == "line"
            else "M2.5 12.5C2.5 8 7 6.5 12 6.5C17 6.5 21.5 8 21.5 12.5Z")
    bowl = "M5.5 12H18.5C18.5 17.5 16 21 12 21C8 21 5.5 17.5 5.5 12Z"
    return [shell(union(dome, bowl)), detail(f"M2.5 12.5{wavy(2.5, 21.5, 12.5, 6, 0.8)}")]


@icon("jar-opener", CAT, "Jar with a textured rubber grip band wrapped around its lid",
      tags=["jar grip", "lid opener", "rubber grip", "kitchen gadget", "stuck lid", "twist", "open jar"])
def _(S):
    return [shell(rect(6, 11.5, 12, 10, rr(S, 3))), shell(rect(4.5, 3.5, 15, 8, rr(S, 2.5))),
            detail(seg(8, 6.5, 8, 8.5)), detail(seg(12, 6.5, 12, 8.5)), detail(seg(16, 6.5, 16, 8.5)),
            detail(seg(9, 16, 15, 16))]


@icon("bag-sealer", CAT, "Small handheld heat sealer clamp pressed along the open top of a snack bag",
      tags=["chip clip", "bag clip", "heat sealer", "snack bag", "reseal", "kitchen gadget", "freshness"])
def _(S):
    bag = poly([(6, 12), (18, 12), (19.5, 20.5), (4.5, 20.5)], closed=True, r=S.r)
    return [shell(bag), shell(rect(3, 3.5, 18, 5.5, rr(S, 2.75))),
            hole(circle(17, 6.25, 1.1)), detail(seg(6.5, 6.25, 13, 6.25)),
            detail(poly([(8, 16), (10, 18), (12, 16), (14, 18), (16, 16)], r=S.r))]


# ============================================================================ cold food, labels and food safety

def snowflake(cx, cy, r):
    return [line(seg(*pt_on(cx, cy, r, a), *pt_on(cx, cy, r, a + 180))) for a in (90, 30, 150)]


@icon("community-fridge", CAT, "Upright fridge with its door swung open showing shelves and a heart on the door",
      tags=["free fridge", "food sharing", "food bank", "surplus food", "charity", "neighbourhood", "share food"])
def _(S):
    shape = union(rect(10, 2.5, 11.5, 19, L(S, 0.5, 3.5)), poly([(10, 3.5), (3.5, 5.5), (3.5, 19.5), (10, 21)], closed=True, r=0))
    return [shell(shape), detail(seg(10, 3.5, 10, 21)), detail(seg(10, 9.5, 21.5, 9.5)), detail(seg(10, 15.5, 21.5, 15.5)),
            hole("M6.8 14.6L5.1 12.9A1.1 1.1 0 0 1 6.8 11.3A1.1 1.1 0 0 1 8.5 12.9Z")]


@icon("cold-chain", CAT, "Refrigerated delivery truck with a snowflake on its box and a small thermometer above the cab",
      tags=["refrigerated transport", "reefer truck", "frozen delivery", "temperature controlled", "logistics", "cold storage"])
def _(S):
    cab = poly([(15, 10.5), (18.5, 10.5), (21.5, 13.5), (21.5, 18), (15, 18)], closed=True, r=S.r)
    flake = []
    for a in (90, 30, 150):
        flake.append(detail(seg(*pt_on(8.5, 12.75, 3.3, a), *pt_on(8.5, 12.75, 3.3, a + 180))))
    return [shell(rect(2, 7.5, 13, 10.5, rr(S, 2))), shell(cab), shell(circle(6.5, 19.5, 2)), shell(circle(17.5, 19.5, 2))] + flake + \
        [hole(circle(*pt_on(8.5, 12.75, 3.6, a), 0.9)) for a in (30, 90, 150, 210, 270, 330)] + \
        [line(seg(19.5, 2.5, 19.5, 5.5)), dot(19.5, 7, 1.5)]


@icon("non-vegetarian-mark", CAT, "Square outline with a solid upward-pointing triangle centred inside, the non-vegetarian food mark",
      tags=["non veg", "non-veg", "meat", "food label", "dietary mark", "india", "packaging symbol"])
def _(S):
    return [shell(rect(3.5, 3.5, 17, 17, rr(S, 3))), hole(poly([(12, 7.5), (16.5, 15.8), (7.5, 15.8)], closed=True, r=S.r * 0.5))]


@icon("halal-label", CAT, "Round seal with a crescent at the top and a flowing script-like line across the centre",
      tags=["halal food", "muslim", "islamic", "dietary", "food certification", "permissible", "food label"])
def _(S):
    crescent = "M14.3 4.8A3.4 3.4 0 1 0 14.3 11.2A2.7 2.7 0 1 1 14.3 4.8Z"
    return [shell(flute(12, 12, 9.8, 9.8, 12, 0.08, S)), hole(crescent),
            detail("M7 16C8.3 13.7 9.8 17.3 11.8 15.3C13.3 13.9 14.3 16.3 17 14.5")]


@icon("kosher-label", CAT, "Round seal with a bold letter K in the centre",
      tags=["kosher food", "jewish", "dietary", "food certification", "parve", "pareve", "food label"])
def _(S):
    return [shell(flute(12, 12, 9.8, 9.8, 12, 0.08, S)), detail(seg(9.5, 7.3, 9.5, 16.7)),
            detail(poly([(14.8, 7.3), (9.8, 12), (14.8, 16.7)], r=S.r))]


@icon("nutrition-facts", CAT, "Tall label panel with a bold top bar and rows of lines of different lengths below",
      tags=["nutrition label", "food label", "calories", "ingredients panel", "packaging", "diet", "serving size"])
def _(S):
    return [shell(rect(5, 2.5, 14, 19, rr(S, 2.5))), hole(rect(7.5, 5, 9, 2.4, 0.6)),
            detail(seg(7.5, 11, 16.5, 11)), detail(seg(7.5, 14.5, 16.5, 14.5)), detail(seg(7.5, 18, 13, 18))]


@icon("ingredients-list", CAT, "Pack label with a heading bar and a bulleted list of short lines",
      tags=["ingredients", "food label", "allergens", "contains", "packaging", "recipe list", "bullet list"])
def _(S):
    return [shell(rect(3.5, 3.5, 17, 17, rr(S, 3))), hole(rect(6.5, 6, 8, 2, 0.6)),
            dot(7, 12, 1.0), detail(seg(10, 12, 17, 12)), dot(7, 16.5, 1.0), detail(seg(10, 16.5, 15, 16.5))]


@icon("traffic-light-label", CAT, "Front-of-pack nutrition label with a row of rounded pills for fat, sugar and salt levels",
      tags=["nutrition label", "front of pack", "colour coded", "fat sugar salt", "food label", "healthy choice", "uk label"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 17, rr(S, 3))), hole(rect(4.8, 7, 3.6, 10, 1.8)), hole(rect(10.2, 7, 3.6, 10, 1.8)),
            hole(rect(15.6, 7, 3.6, 10, 1.8))]


@icon("warning-octagon-label", CAT, "Solid octagon stamp with short bars of text inside, the front-of-pack high-in warning",
      tags=["high in sugar", "high in sodium", "warning label", "front of pack", "food label", "stop sign", "health warning"])
def _(S):
    return [shell(poly(regular(12, 12, 10.6, 8, start=-67.5), closed=True, r=S.r)),
            hole(rect(7.5, 7.6, 9, 1.8, 0.8)), hole(rect(7.5, 11.1, 9, 1.8, 0.8)), hole(rect(7.5, 14.6, 5.5, 1.8, 0.8))]


@icon("sulfites", CAT, "Small wine bottle beside a molecule of three linked atoms, the sulfites allergen mark",
      tags=["sulphites", "contains sulfites", "allergen", "wine", "preservative", "so2", "food label"])
def _(S):
    bottle = poly([(6.5, 3), (9.5, 3), (9.5, 9), (11.5, 12), (11.5, 21), (4.5, 21), (4.5, 12), (6.5, 9)], closed=True, r=S.r)
    return [shell(bottle), detail(seg(4.5, 16.5, 11.5, 16.5)),
            line(seg(17, 6.5, 19.8, 12.3)), line(seg(19.8, 12.3, 16.3, 17.5)),
            dot(17, 6.5, 1.9), dot(19.8, 12.3, 1.9), dot(16.3, 17.5, 1.9)]


@icon("freezer-star-rating", CAT, "Snowflake next to a column of three small stars, the frozen food storage rating",
      tags=["frozen food", "freezer rating", "three star", "storage time", "deep freeze", "food label", "frozen"])
def _(S):
    out = snowflake(8, 12, 6.3)
    for y in (5.5, 12, 18.5):
        out.append(solid(poly(star(18.5, y, 3.1, 1.4), closed=True, r=0)))
    return out


@icon("food-irradiation-symbol", CAT, "Circle broken into dashes across the top, holding two leaves above a dot, the food irradiation mark",
      tags=["radura", "irradiated food", "food preservation", "food label", "radiation", "sterilised", "packaging symbol"])
def _(S):
    out = [line(arc(12, 12, 9.5, 12, 168))]
    for c in (186, 222, 258, 294, 330):
        out.append(line(arc(12, 12, 9.5, c + 0, c + 24)))
    out += [line(seg(12, 15.5, 12, 11)), dot(12, 17.6, 1.4),
            solid("M12 12.5C8.6 12.5 7.4 9.8 7.8 7.4C10.6 7.4 12 9.2 12 12.5Z"),
            solid("M12 12.5C15.4 12.5 16.6 9.8 16.2 7.4C13.4 7.4 12 9.2 12 12.5Z")]
    return out


@icon("food-safety", CAT, "Shield with a fork and a knife standing side by side inside it",
      tags=["food hygiene", "safe food", "haccp", "kitchen safety", "restaurant", "protection", "food standards"])
def _(S):
    shield = poly([(12, 2.5), (20, 5.5), (20, 12), (16, 18.5), (12, 21.5), (8, 18.5), (4, 12), (4, 5.5)], closed=True, r=S.r * 2)
    return [shell(shield), detail("M8.2 7V10A1.6 1.6 0 0 0 11.4 10V7"), detail(seg(9.8, 11.5, 9.8, 16.5)),
            detail("M15 7C16.6 7 17 9.5 17 12H15V16.5")]


@icon("food-miles", CAT, "Apple with a dotted travel route leading round to a map pin",
      tags=["food transport", "local food", "supply chain", "carbon footprint", "farm to table", "distance", "sustainable"])
def _(S):
    apple = ("M8 10.5C6 9 3 10.5 3 14.5C3 18.5 5.5 21 8 21C10.5 21 13 18.5 13 14.5C13 10.5 10 9 8 10.5Z")
    pin = "M17.5 12.5C17.5 12.5 13.6 9 13.6 6.2A3.9 3.9 0 0 1 21.4 6.2C21.4 9 17.5 12.5 17.5 12.5Z"
    return [shell(apple), shell(pin), hole(circle(17.5, 6.2, 1.3)), line("M8 10.5C8 8.5 9 7.3 10.5 7"),
            dot(15, 19.7, 0.95), dot(18, 20, 0.95), dot(20.7, 17.8, 0.95), dot(20.9, 14.8, 0.95)]


@icon("packaged-food", CAT, "Group of a can, a tall box and a jar standing together",
      tags=["groceries", "pantry goods", "canned goods", "supermarket", "processed food", "shelf stable", "packaging"])
def _(S):
    body = union(rect(2.5, 11, 8, 9.5, L(S, 0, 2.5)), rect(8, 3.5, 8, 17, L(S, 0, 2)), rect(14, 8, 7.5, 12.5, L(S, 0.5, 3)))
    return [shell(body), detail(poly([(8, 11), (10.5, 11), (10.5, 20.5)])), detail(poly([(14, 20.5), (14, 8), (16, 8)]))]


@icon("gmo-food", CAT, "Tomato with a small double helix strand drawn beside it",
      tags=["genetically modified", "gm crop", "gmo", "bioengineered", "dna", "food technology", "biotech"])
def _(S):
    tomato = "M9 10C7 8.5 3.5 10 3.5 14.5C3.5 18.5 6 21 9 21C12 21 14.5 18.5 14.5 14.5C14.5 10 11 8.5 9 10Z"
    return [shell(tomato), line("M9 10L6 7.8"), line("M9 10L12 7.8"), line("M9 10V6.5"),
            line("M16 3.5C22 8 15 14 21 19.5"), line("M21 3.5C15 8 22 14 16 19.5")]


@icon("insect-protein", CAT, "Cricket with long antennae standing beside a small heap of protein powder",
      tags=["cricket flour", "edible insects", "entomophagy", "alternative protein", "sustainable food", "bug", "grasshopper"])
def _(S):
    body = union(ellipse(11.5, 9.8, 6.5, 3.3), circle(5.2, 8.8, 2.6))
    return [shell(body), line("M4.5 6.4C4 4.6 3 3.6 2.5 2.8"), line("M6.3 6.5C7 4.8 8.3 3.8 9.5 3.2"),
            line("M8 12.5L6.8 17.5"), line("M11.5 12.8L11 17.5"), line("M15.5 11.5L19 8.5L21 13.5"),
            shell("M12.5 21C13 18.5 15 17 17.2 17C19.5 17 21.5 18.5 22 21Z")]


@icon("meat-alternative", CAT, "Round burger patty with a leaf laid across its top",
      tags=["plant based", "vegan burger", "veggie patty", "meat free", "vegetarian", "meatless", "plant protein"])
def _(S):
    patty = rect(3, 10, 18, 10, rr(S, 5))
    leaf = "M5.5 11.5C7 4.5 14 3 20 5.5C18.5 11.5 11 13 5.5 11.5Z"
    return [shell(union(patty, leaf)), detail("M7.5 10C11 8.3 14.8 7.3 18 7"),
            hole(circle(8, 16, 0.9)), hole(circle(12.5, 17.3, 0.9)), hole(circle(16.5, 15.8, 0.9))]
