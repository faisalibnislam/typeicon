"""TypeIcon Core: bakery (batch bakery_004): condiments, bakeware, baking tools, bakery shop items and
a few sweets and dairy items.

Containers are drawn in side view; pans and trays are drawn from the side or slightly above when the top
is what identifies them. Long hand tools are drawn upright and turned 45 degrees clockwise so the handle
points to the bottom-left and the working end to the top-right, matching the tools and kitchen sets.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path.parser import parse_path
from geometry import SCALE, D, P, ST, U, fmt, path_to_d, rotation

CAT = "bakery"
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
    """Turn an upright tool (handle down) so the handle points to the bottom-left, then centre it."""
    return fit([Part(p.kind, rot(p.d, deg), p.attrs) for p in parts])


def rbox(S, x, y, w, h, cap=None):
    return rect(x, y, w, h, rr(S, cap))


# ============================================================================ sauces and condiments

@icon("mayonnaise", CAT, "Wide squat jar with a swirled dollop of mayonnaise rising from the top",
      tags=["mayo", "condiment", "dressing", "sandwich spread", "jar", "sauce"], aliases=["mayo"])
def _(S):
    dollop = ("M7 12C6.5 9.5 8.5 8.5 10 8.5C10 6 11.5 4.5 14 3.5C13.5 5 14 6.5 15 7C16.5 7.3 17.5 9.5 17 12Z")
    jar = rbox(S, 4, 11.5, 16, 9.5, 3)
    return [shell(union(dollop, jar)), detail(seg(4, 11.5, 20, 11.5)), detail(seg(9, 16.5, 15, 16.5))]


@icon("hot-sauce", CAT, "Slim hot sauce bottle with a long narrow neck, a small cap and a chili pepper label",
      tags=["chili sauce", "hot pepper sauce", "spicy", "condiment", "bottle", "chilli sauce"])
def _(S):
    body = poly([(10.5, 5.5), (13.5, 5.5), (13.5, 9), (16.5, 12), (16.5, 21), (7.5, 21), (7.5, 12), (10.5, 9)],
                closed=True, r=S.r)
    chili = "M9.8 18.3C12.8 18.3 14.3 16.5 14.3 14.3"
    return [shell(body), solid(rect(10, 2, 4, 3, L(S, 0, 0.8))), detail(chili)]


@icon("soy-sauce", CAT, "Small soy sauce dispenser with a spout beside a shallow dipping dish",
      tags=["soya sauce", "shoyu", "tamari", "condiment", "sushi", "dispenser"], aliases=["soya-sauce"])
def _(S):
    body = union(rbox(S, 3, 10, 9, 11, 3), rect(5, 6.5, 5, 4))
    dish = poly([(13.5, 16.5), (21.5, 16.5), (20, 20.5), (15, 20.5)], closed=True, r=L(S, 0, 1))
    return [shell(body), detail(seg(3, 10, 12, 10)), line(seg(10, 7.5, 12.5, 5)), shell(dish)]


@icon("soy-fish", CAT, "Small fish-shaped soy sauce squeeze container with a screw cap in its mouth",
      tags=["soy sauce fish", "sauce container", "sushi", "takeaway", "condiment", "squeeze bottle"])
def _(S):
    body = "M7.5 12C9.5 8 15 8 17.5 11L21.5 8V16L17.5 13C15 16 9.5 16 7.5 12Z"
    cap = rect(2.5, 10, 4, 4, L(S, 0, 1))
    return [shell(body, stroke_miterlimit="2"), shell(cap), dot(11, 11.2, 1), detail(seg(14.2, 10, 14.2, 14))]


@icon("gravy-boat", CAT, "Low oval gravy boat with a long pouring lip and a loop handle on a saucer",
      tags=["sauce boat", "gravy", "jug", "roast dinner", "sauce", "tableware"], aliases=["sauce-boat"])
def _(S):
    boat = "M5 10.5H15.5L21.5 7C20.8 11 19 14 16.5 15.5C15 16.3 13.5 16.5 11.5 16.5C8 16.5 5.5 14.5 5 10.5Z"
    handle = "M5.3 12.2C2 11.4 1.6 15.4 6.4 14.8"
    return [shell(boat, stroke_miterlimit="2"), line(handle), line(seg(3, 20, 21, 20))]


@icon("oil-cruet", CAT, "Round glass oil cruet with a stopper and a thin angled pouring spout",
      tags=["oil bottle", "olive oil", "vinegar", "cruet", "dispenser", "salad dressing"])
def _(S):
    body = "M10.5 8H13.5V11.5C16.5 12.5 18.5 14.5 18.5 17C18.5 19.5 16 21 12 21C8 21 5.5 19.5 5.5 17C5.5 14.5 7.5 12.5 10.5 11.5Z"
    drop = "M12 13.5C13 15 14 16 14 17C14 18.1 13.1 18.8 12 18.8C10.9 18.8 10 18.1 10 17C10 16 11 15 12 13.5Z"
    return [shell(body), solid(rect(10, 5, 4, 3, L(S, 0, 0.8))), line(seg(13, 5.5, 17, 2.5)), detail(drop)]


@icon("dipping-sauce", CAT, "Small round ramekin of sauce with a chip dipped into it",
      tags=["dip", "salsa", "chips and dip", "guacamole", "sauce", "snack"], aliases=["dip"])
def _(S):
    bowl = "M3 13.5H21C21 18 17.5 21 12 21C6.5 21 3 18 3 13.5Z"
    chip = poly([(5, 4), (18.5, 2.5), (11.5, 11.5)], closed=True, r=L(S, 0, 1))
    return [shell(bowl), shell(chip, stroke_miterlimit="2"), detail(seg(9, 7.5, 14.2, 7.2))]


@icon("sauce-cup", CAT, "Small plastic portion cup of sauce with a snap-on lid",
      tags=["portion cup", "souffle cup", "dressing cup", "takeaway", "sauce", "condiment"])
def _(S):
    lid = rbox(S, 3.5, 7, 17, 3.5, 1.5)
    cup = poly([(5.5, 10.5), (18.5, 10.5), (16.5, 20), (7.5, 20)], closed=True)
    wave = "M8 14.5C9.5 13 10.5 13 12 14.5C13.5 16 14.5 16 16 14.5"
    return [shell(union(lid, cup)), detail(seg(3.5, 10.5, 20.5, 10.5)), detail(wave)]


@icon("sauce-packet", CAT, "Small sauce sachet with zigzag sealed ends and a tear notch",
      tags=["sachet", "condiment packet", "ketchup packet", "takeaway", "sauce", "single serve"])
def _(S):
    y0, y1, n = 6, 18, 4
    step = (y1 - y0) / n
    right = []
    for i in range(n):
        right += [(21, y0 + i * step), (19.8, y0 + (i + 0.5) * step)]
    right.append((21, y1))
    left = [(24 - x, y) for x, y in reversed(right)]
    pts = [(3, y0), (15.5, y0), (16.5, 7.5), (17.5, y0)] + right + [(3, y1)] + left[1:-1]
    return [shell(poly(pts, closed=True), stroke_miterlimit="2"),
            detail("M12 8.5C13.2 10.3 14.5 11.5 14.5 13C14.5 14.5 13.4 15.5 12 15.5C10.6 15.5 9.5 14.5 9.5 13C9.5 11.5 10.8 10.3 12 8.5Z")]


@icon("condiment-pump", CAT, "Countertop condiment dispenser jar with a push-down pump head and a curved spout",
      tags=["pump dispenser", "sauce pump", "syrup pump", "condiment", "dispenser", "fast food"])
def _(S):
    jar = rbox(S, 5, 12, 12, 9, 3)
    head = rbox(S, 7, 4, 8, 3, 1.2)
    spout = poly([(15, 5.5), (19.5, 5.5), (19.5, 8.5)], r=L(S, 0, 1.5))
    return fit([shell(jar), shell(rbox(S, 6.5, 10, 9, 2, 0.8)), line(seg(11, 7, 11, 10)), shell(head), line(spout),
                detail(seg(8, 16.5, 14, 16.5))])


@icon("honey-bear-bottle", CAT, "Squeeze bottle shaped like a sitting bear with a pointed cap on its head",
      tags=["honey bottle", "honey bear", "squeeze bottle", "honey", "sweetener", "condiment"])
def _(S):
    head = circle(12, 10, 3.8)
    ears = [circle(8.4, 7.2, 1.8), circle(15.6, 7.2, 1.8)]
    body = "M12 12.5C16.5 12.5 18.5 15.5 18.5 18C18.5 20 17 21 15 21H9C7 21 5.5 20 5.5 18C5.5 15.5 7.5 12.5 12 12.5Z"
    cap = poly([(10.6, 6.4), (13.4, 6.4), (12, 2)], closed=True, r=L(S, 0, 0.5))
    return [shell(union(head, *ears, body)), solid(cap), detail("M8.6 13.6C10.5 14.6 13.5 14.6 15.4 13.6")]


@icon("syrup-dispenser", CAT, "Glass syrup jar with a handle and a hinged metal lid with a thumb lever",
      tags=["syrup jug", "maple syrup", "pancake syrup", "dispenser", "pourer", "diner"])
def _(S):
    body = rbox(S, 5, 10, 11, 11, 3)
    lid = poly([(5, 10), (16, 10), (14.5, 6.5), (6.5, 6.5)], closed=True, r=L(S, 0, 0.8))
    handle = poly([(16, 12), (19.5, 12), (19.5, 18), (16, 18)], r=S.r)
    return fit([shell(union(body, lid)), detail(seg(5, 10, 16, 10)), line(seg(14, 7, 17, 3)),
                line(seg(6.5, 7.5, 3.5, 6)), line(handle), detail(seg(8, 13.5, 8, 17.5))])


@icon("sugar-dispenser", CAT, "Glass sugar dispenser with a domed metal lid and a slanted pouring spout",
      tags=["sugar shaker", "sugar pourer", "sugar jar", "cafe", "diner", "sweetener"], aliases=["sugar-pourer"])
def _(S):
    jar = rbox(S, 5.5, 10.5, 13, 10.5, 2.5)
    lid = "M5.5 10.5C5.5 8 8.5 7 12 7C15.5 7 18.5 8 18.5 10.5Z"
    spout = rot(rect(10.5, 2, 3, 6.5, L(S, 0, 0.6)), -35, 12, 8)
    return [shell(union(jar, lid, spout)), detail(seg(5.5, 10.5, 18.5, 10.5)),
            detail(seg(5.5, 15, 18.5, 15))]


# ============================================================================ baking tools

@icon("rolling-pin", CAT, "Rolling pin with two handles lying on a flat sheet of dough",
      tags=["rolling dough", "pastry", "baking", "roll out", "dough", "baker"])
def _(S):
    barrel = rbox(S, 6, 5, 12, 6, 3)
    dough = "M3 17C3 14.5 6 14.5 9 14.5H15.5C19 14.5 21 15 21 17C21 19 19 19.5 15.5 19.5H9C6 19.5 3 19.5 3 17Z"
    return [shell(barrel), line(seg(2.5, 8, 6, 8)), line(seg(18, 8, 21.5, 8)), shell(dough)]


@icon("piping-bag", CAT, "Piping bag with a star nozzle squeezing out a swirl of icing",
      tags=["pastry bag", "icing bag", "frosting", "cake decorating", "decorate", "baking"], aliases=["pastry-bag"])
def _(S):
    bag = "M7 5C7 3.2 17 3.2 17 5L13.5 13H10.5Z"
    nozzle = poly([(10.5, 13), (13.5, 13), (12.8, 15.5), (11.2, 15.5)], closed=True)
    parts = [shell(union(bag, nozzle), stroke_miterlimit="2"), detail(seg(10.5, 13, 13.5, 13)),
             detail(seg(7, 6.5, 17, 6.5))]
    parts = [Part(p.kind, mv(rot(p.d, 30, 12, 15.5), -0.7, -0.5), p.attrs) for p in parts]
    swirl = "M3 21.5C2.5 19.3 4 18.5 5.5 18.5C5.5 17 6.8 16 8 16C9.2 16 10.5 17 10.5 18.5C12 18.5 13.5 19.3 13 21.5Z"
    return [shell(swirl)] + parts


@icon("piping-tip", CAT, "Metal piping nozzle: a small cone with a serrated star-shaped opening",
      tags=["piping nozzle", "icing tip", "star tip", "decorating tip", "frosting", "cake decorating"],
      aliases=["piping-nozzle"])
def _(S):
    crown = [(14, 8), (14.5, 4), (13, 5.8), (12, 3.2), (11, 5.8), (9.5, 4), (10, 8)]
    cone = poly([(19, 18.5)] + crown + [(5, 18.5)], r=L(S, 0, 0.6)) + "C5 22 19 22 19 18.5Z"
    return [shell(cone, stroke_miterlimit="2"), detail("M6 15.5C6 18.5 18 18.5 18 15.5")]


def _gingerbread():
    head = circle(12, 5.5, 3.2)
    body = ("M9.5 8.5H14.5L19.5 10.5C20.8 11 20.5 13 19 12.8L15.5 12.3L16.5 16.5L18 20C18.4 21.2 17 22 16 21"
            "L12 17L8 21C7 22 5.6 21.2 6 20L7.5 16.5L8.5 12.3L5 12.8C3.5 13 3.2 11 4.5 10.5Z")
    return union(head, body)


@icon("cookie-cutter", CAT, "Metal cookie cutter shaped like a gingerbread figure, drawn as an empty outline",
      tags=["cutter", "gingerbread cutter", "cookie mold", "biscuit cutter", "baking", "christmas baking"],
      aliases=["biscuit-cutter"])
def _(S):
    return [line(_gingerbread())]


def _pan(S, x0, x1, top, depth, ry):
    """Round pan in perspective: top ellipse and side walls; Line gets a flatter bottom with corners."""
    rx = (x1 - x0) / 2
    brx = L(S, rx * 1.35, rx)
    bry = L(S, ry * 0.9, ry)
    return (f"M{fmt(x0)} {fmt(top)}A{fmt(rx)} {fmt(ry)} 0 0 1 {fmt(x1)} {fmt(top)}V{fmt(top + depth)}"
            f"A{fmt(brx)} {fmt(bry)} 0 0 1 {fmt(x0)} {fmt(top + depth)}Z")


def _rim(x0, x1, top, ry):
    return f"M{fmt(x0)} {fmt(top)}A{fmt((x1 - x0) / 2)} {fmt(ry)} 0 0 0 {fmt(x1)} {fmt(top)}"


@icon("doughnut-cutter", CAT, "Round doughnut cutter with a small inner ring for the hole and a handle arching over it",
      tags=["donut cutter", "ring cutter", "biscuit cutter", "doughnut making", "baking", "cutter"],
      aliases=["donut-cutter"])
def _(S):
    return [shell(_pan(S, 3, 21, 13, 3.5, 4.5)), detail(_rim(3, 21, 13, 4.5)), detail(ellipse(12, 13, 3, 1.3)),
            line("M5.5 11C5.5 2.5 18.5 2.5 18.5 11")]


@icon("muffin-tin", CAT, "Muffin tin from above: a rectangular pan with six round cups",
      tags=["muffin pan", "cupcake tray", "bun tin", "bakeware", "baking tray", "cupcakes"],
      aliases=["muffin-pan"])
def _(S):
    out = [shell(rbox(S, 2, 4, 20, 16, 3))]
    for x in (6.5, 12, 17.5):
        for y in (9, 15):
            out.append(dot(x, y, 2.2))
    return out


@icon("loaf-pan", CAT, "Deep rectangular loaf pan with slightly flared sides and a rim",
      tags=["loaf tin", "bread pan", "bread tin", "pound cake pan", "bakeware", "baking"], aliases=["loaf-tin"])
def _(S):
    body = poly([(2.5, 6), (21.5, 6), (21.5, 9), (19, 19.5), (5, 19.5), (2.5, 9)], closed=True, r=L(S, 0, 1.2))
    return [shell(body, stroke_miterlimit="2"), detail(seg(2.5, 9, 21.5, 9))]


@icon("bundt-pan", CAT, "Round bundt pan with fluted tapering sides and a central tube",
      tags=["bundt tin", "ring pan", "tube pan", "fluted pan", "bakeware", "gugelhupf"], aliases=["bundt-tin"])
def _(S):
    top, ry = 8, 4
    body = (f"M2.5 {top}A9.5 {ry} 0 0 1 21.5 {top}L18.5 18.5C17 20 7 20 5.5 18.5Z")
    return [shell(body, stroke_miterlimit="2"), detail(_rim(2.5, 21.5, top, ry)), detail(ellipse(12, 8, 2.8, 1.5)),
            detail("M7 13.5Q7.5 16 8 19"), detail(seg(12, 14, 12, 19.5)), detail("M17 13.5Q16.5 16 16 19")]


@icon("springform-pan", CAT, "Round springform pan with straight sides and a clamp latch on its side",
      tags=["springform tin", "cheesecake pan", "cake tin", "removable base", "bakeware", "baking"],
      aliases=["springform-tin"])
def _(S):
    latch = rbox(S, 18.5, 11, 4, 3.5, 1)
    return [shell(union(_pan(S, 2.5, 20.5, 8.5, 8, 3), latch)), detail(_rim(2.5, 20.5, 8.5, 3)),
            detail(seg(18.5, 11, 18.5, 14.5))]


@icon("cake-pan", CAT, "Round shallow cake pan with straight sides seen at an angle",
      tags=["cake tin", "round pan", "sandwich tin", "layer cake pan", "bakeware", "baking"], aliases=["cake-tin"])
def _(S):
    return [shell(_pan(S, 2.5, 21.5, 10, 4, 4.5)), detail(_rim(2.5, 21.5, 10, 4.5))]


def _scallop(cx, cy, R, n, a):
    d = ""
    for i in range(n):
        t0, t1 = -90 + i * 360 / n, -90 + (i + 1) * 360 / n
        p0, p1 = pt_on(cx, cy, R, t0), pt_on(cx, cy, R, t1)
        if i == 0:
            d += f"M{fmt(p0[0])} {fmt(p0[1])}"
        d += f"A{fmt(a)} {fmt(a)} 0 0 1 {fmt(p1[0])} {fmt(p1[1])}"
    return d + "Z"


@icon("tart-pan", CAT, "Shallow round tart pan from above with a fluted rim",
      tags=["tart tin", "flan tin", "quiche pan", "fluted pan", "bakeware", "pastry"], aliases=["tart-tin"])
def _(S):
    return [shell(_scallop(12, 12, 8.8, 22, 2.2)), detail(circle(12, 12, 5))]


@icon("pie-dish", CAT, "Empty shallow round pie dish with a wide rim and sloped sides",
      tags=["pie plate", "pie tin", "pie pan", "quiche dish", "bakeware", "baking"], aliases=["pie-plate"])
def _(S):
    sides = poly([(3, 11), (21, 11), (17.5, 18), (6.5, 18)], closed=True, r=L(S, 0, 2))
    return [shell(union(ellipse(12, 10, 10, 4.5), sides)), detail(ellipse(12, 10, 6.5, 2))]


@icon("baking-sheet", CAT, "Rimmed baking sheet seen at an angle holding rows of round cookies",
      tags=["sheet pan", "baking tray", "cookie sheet", "oven tray", "bakeware", "cookies"],
      aliases=["sheet-pan", "baking-tray"])
def _(S):
    tray = poly([(6, 5.5), (22, 5.5), (18, 18.5), (2, 18.5)], closed=True, r=L(S, 0, 1.5))
    out = [shell(tray)]
    for row, y in enumerate((9.2, 14.8)):
        shift = (18.5 - y) * (4 / 13)
        for x in (6.2, 11, 15.8):
            out.append(dot(x + shift - 0.8, y, 1.7))
    return out


@icon("cooling-rack", CAT, "Wire cooling rack seen at an angle, standing on short feet",
      tags=["wire rack", "cooling grid", "cake rack", "baking rack", "bakeware", "cookies"], aliases=["wire-rack"])
def _(S):
    frame = poly([(6, 4.5), (22, 4.5), (18.5, 15), (2.5, 15)], closed=True, r=L(S, 0, 1))
    out = [line(frame)]
    for t in (0.28, 0.5, 0.72):
        xa, xb = 6 + 16 * t, 2.5 + 16 * t
        out.append(line(seg(xa, 4.5, xb, 15)))
    out += [line(seg(3.5, 15, 3.5, 19.5)), line(seg(17.5, 15, 17.5, 19.5)), line(seg(20.8, 8, 20.8, 12.5))]
    return out


@icon("flour-sifter", CAT, "Cup flour sifter with a side crank handle and flour falling from its mesh bottom",
      tags=["sifter", "flour", "sieve", "sift", "baking", "powdered sugar"], aliases=["sifter"])
def _(S):
    cup = poly([(6, 3), (18, 3), (17, 14), (7, 14)], closed=True, r=S.r)
    handle = poly([(17.8, 5.5), (21, 5.5), (21, 11.5), (17.3, 11.5)], r=S.r)
    crank = poly([(6.2, 7), (3, 7), (3, 9.5)], r=L(S, 0, 1))
    out = [shell(cup), line(handle), line(crank), detail(seg(7, 10.5, 17, 10.5))]
    for x, y in ((9, 17.5), (12, 17.5), (15, 17.5), (10.5, 20.5), (13.5, 20.5)):
        out.append(dot(x, y, 1))
    return out


@icon("pastry-brush", CAT, "Pastry brush with a wooden handle, a metal band and flat bristles",
      tags=["basting brush", "egg wash", "glaze", "baking brush", "pastry", "baking"], aliases=["basting-brush"])
def _(S):
    bristles = poly([(8.5, 1.5), (15.5, 1.5), (15, 8.5), (9, 8.5)], closed=True, r=L(S, 0, 1))
    return tilt([shell(bristles), detail(seg(12, 1.5, 12, 5.5)), shell(rbox(S, 9, 8.5, 6, 3, 0.8)),
                 shell(rbox(S, 10.5, 11.5, 3, 11, 1.5))])


@icon("pastry-wheel", CAT, "Pastry wheel: a small fluted cutting wheel on the end of a handle",
      tags=["pastry cutter", "fluted cutter", "jagger", "ravioli cutter", "crimper", "baking"],
      aliases=["pastry-jagger"])
def _(S):
    return tilt([shell(_scallop(12, 6.5, 5, 8, 1.8)), dot(12, 6.5, 1.3), line(seg(12, 12.5, 12, 13)),
                 shell(rbox(S, 10.5, 13, 3, 9, 1.5))])


@icon("proofing-basket", CAT, "Round coiled proofing basket with ringed sides and a dome of dough rising above the rim",
      tags=["banneton", "brotform", "proving basket", "sourdough", "bread proofing", "baking"],
      aliases=["banneton"])
def _(S):
    bowl = "M2.5 10.5H21.5C21.5 16.5 17.5 20.5 12 20.5C6.5 20.5 2.5 16.5 2.5 10.5Z"
    dough = "M5 10.5C5 6 8.5 4 12 4C15.5 4 19 6 19 10.5Z"
    return [shell(union(bowl, dough)), detail(seg(2.5, 10.5, 21.5, 10.5)), detail(seg(9.5, 8.5, 14.5, 6)),
            detail("M3 14C8 15.3 16 15.3 21 14"), detail("M4.8 17.5C9 18.6 15 18.6 19.2 17.5")]


@icon("bread-lame", CAT, "Bread lame: a slim handle holding a curved razor blade for scoring dough",
      tags=["lame", "scoring blade", "dough scoring", "sourdough", "razor", "baking"], aliases=["scoring-blade"])
def _(S):
    blade = "M12 11C8.5 9 8 5 10.5 1.5C10.5 5 12 7.5 15 9.5Z"
    return tilt([shell(blade, stroke_miterlimit="2"), shell(rbox(S, 10.5, 11, 3, 11, 1.5))])


@icon("offset-spatula", CAT, "Offset spatula: a long thin rounded blade with a bent neck stepping down to a handle",
      tags=["icing spatula", "palette knife", "frosting knife", "cake decorating", "frosting", "baking"])
def _(S):
    blade = poly([(10, 12), (10, 5), (11.5, 1), (14.5, 1), (16, 5), (16, 12)], closed=True, r=L(S, 0, 1.5))
    neck = poly([(13, 12), (13, 14), (8.5, 16.5)], r=S.r)
    return tilt([shell(blade), line(neck), shell(rbox(S, 7, 16.5, 3, 6.5, 1.5))])


@icon("cake-turntable", CAT, "Cake turntable: a flat round rotating top on a short base with a curved arrow",
      tags=["cake stand", "turntable", "decorating stand", "revolving stand", "rotate", "cake decorating"],
      aliases=["decorating-turntable"])
def _(S):
    top = _pan(S, 2.5, 21.5, 11.5, 1.5, 2.5)
    base = poly([(9.5, 15.5), (14.5, 15.5), (16.5, 20.5), (7.5, 20.5)], closed=True, r=L(S, 0, 1))
    arrow = "M5 6.5C8 4 16 4 19 6.5"
    head = poly([(15.5, 6), (19.5, 7), (19.5, 3)], r=L(S, 0, 0.8)) if False else poly([(15.8, 7.2), (19.3, 7), (19.2, 3.6)], r=L(S, 0, 0.8))
    return [shell(top), shell(base), line(arrow), line(head)]


@icon("cake-stand", CAT, "Cake stand: a round plate on a single pedestal foot holding a cake",
      tags=["cake plate", "pedestal stand", "dessert stand", "cake display", "bakery", "party"])
def _(S):
    cake = rbox(S, 5.5, 4, 13, 8.5, 2)
    foot = "M8 20.5C8 18 10 17.5 12 17.5C14 17.5 16 18 16 20.5Z"
    return [shell(cake), detail(seg(5.5, 8, 18.5, 8)), line(seg(2.5, 13.5, 21.5, 13.5)), line(seg(12, 14, 12, 17.5)),
            shell(foot)]


@icon("tiered-stand", CAT, "Three-tier serving stand: round plates on a central rod with a loop handle",
      tags=["cake tier", "afternoon tea", "cupcake stand", "high tea", "serving stand", "dessert stand"],
      aliases=["tiered-cake-stand"])
def _(S):
    loop = circle(12, 3.5, 1.6) if S.name == "rounded" else rect(10.4, 1.9, 3.2, 3.2)
    return [line(loop), line(seg(12, 5.1, 12, 18)), shell(ellipse(12, 9, 5, 1.8)), shell(ellipse(12, 14.5, 7.5, 1.8)),
            shell(ellipse(12, 20, 10, 1.8))]


@icon("cake-carrier", CAT, "Round cake carrier with a domed lid and a folding carry handle over the top",
      tags=["cake keeper", "cake dome", "cake container", "carry cake", "dessert carrier", "bakery"],
      aliases=["cake-keeper"])
def _(S):
    dome = "M6.5 16C6.5 11.5 9 9.5 12 9.5C15 9.5 17.5 11.5 17.5 16Z"
    base = rbox(S, 2.5, 16, 19, 4.5, 1.5)
    return [shell(union(dome, base)), detail(seg(2.5, 16, 21.5, 16)),
            line("M3.5 16V12C3.5 3.8 20.5 3.8 20.5 12V16")]


@icon("cupcake-liner", CAT, "Empty pleated paper cupcake liner with flared ridged sides",
      tags=["cupcake case", "muffin case", "baking cup", "paper cup", "cupcake wrapper", "baking"],
      aliases=["cupcake-case"])
def _(S):
    body = f"M3.5 7.5A8.5 2.5 0 0 1 20.5 7.5L17 20H7Z"
    out = [shell(body, stroke_miterlimit="2"), detail(_rim(3.5, 20.5, 7.5, 2.5))]
    for xt, xb in ((7.2, 9.4), (12, 12), (16.8, 14.6)):
        out.append(detail(seg(xt, 12.5, xb, 20)))
    return out


@icon("doily", CAT, "Round lace paper doily with a scalloped edge and a ring of cut-out holes",
      tags=["lace mat", "paper doily", "cake doily", "tea party", "placemat", "decoration"])
def _(S):
    out = [shell(_scallop(12, 12, 8.8, 14, 2.4)), detail(circle(12, 12, 2.5))]
    for k in range(8):
        p = pt_on(12, 12, 6, k * 45 + 22.5)
        out.append(dot(p[0], p[1], 1.1))
    return out


def capsule(x1, y1, x2, y2, w):
    """Closed stadium shape of width w from (x1, y1) to (x2, y2)."""
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    length = math.hypot(x2 - x1, y2 - y1)
    d = rect(x1, y1 - w / 2, length, w, w / 2)
    return rot(d, ang, x1, y1)


# ============================================================================ boxes, bags and baskets

@icon("pastry-box", CAT, "Cardboard cake box with a window on the front and a string bow on top",
      tags=["cake box", "bakery box", "pastry takeaway", "gift box", "patisserie", "bakery"], aliases=["cake-box"])
def _(S):
    left = poly([(12, 8.5), (7.5, 5), (7.5, 8.5)], closed=True, r=L(S, 0, 0.8))
    loops = [shell(poly([(12, 8.5), (7.5, 4.5), (6.5, 8.5)], closed=True, r=L(S, 0, 1))),
             shell(poly([(12, 8.5), (16.5, 4.5), (17.5, 8.5)], closed=True, r=L(S, 0, 1)))]
    return [shell(rbox(S, 3, 9.5, 18, 11.5, 2))] + loops + [detail(rect(7, 13, 10, 5, L(S, 0, 1.2)))]


@icon("donut-box", CAT, "Open doughnut box with its lid flipped up behind a row of ring doughnuts",
      tags=["doughnut box", "dozen donuts", "bakery box", "donut shop", "takeaway", "pastries"],
      aliases=["doughnut-box"])
def _(S):
    lid = poly([(2.5, 10), (21.5, 10), (19.5, 3), (4.5, 3)], closed=True, r=L(S, 0, 1))
    out = [shell(lid), shell(rbox(S, 2, 10, 20, 10.5, 2))]
    for x in (6.2, 12, 17.8):
        out.append(detail(circle(x, 15.25, 1.9)))
    return out


@icon("bakery-bag", CAT, "Paper bakery bag with a folded rim and two baguettes sticking out of the top",
      tags=["bread bag", "baguette", "paper bag", "bakery", "groceries", "french bread"], aliases=["bread-bag"])
def _(S):
    bag = poly([(5, 10.5), (19, 10.5), (18, 21), (6, 21)], closed=True)
    b1 = capsule(9.5, 11, 6.5, 2.5, 3.5)
    b2 = capsule(14, 11, 17.5, 3.5, 3.5)
    body = union(bag, b1, b2)
    return [shell(body), detail(seg(5, 10.5, 19, 10.5)), detail(seg(5.3, 13.5, 18.7, 13.5)),
            detail(seg(7, 6.5, 8.6, 5.9)), detail(seg(15.3, 7.2, 16.9, 6.8))]


@icon("bread-box", CAT, "Bread box with its roll-top lid slid up to show a loaf inside",
      tags=["bread bin", "breadbox", "roll top", "kitchen storage", "bread", "counter"], aliases=["bread-bin"])
def _(S):
    body = "M2.5 21V11C2.5 6.5 6 4 10.5 4H14C18 4 21.5 6.5 21.5 11V21Z"
    return [shell(body), detail(seg(4.3, 10.5, 19.7, 10.5)), detail("M7 18C7 14.5 9 13.5 12 13.5C15 13.5 17 14.5 17 18Z")]


@icon("bread-basket", CAT, "Woven bread basket with a cloth lining holding a few rolls",
      tags=["roll basket", "breadbasket", "dinner rolls", "restaurant", "bread", "basket"])
def _(S):
    basket = poly([(3, 12.5), (21, 12.5), (19, 20.5), (5, 20.5)], closed=True, r=L(S, 0, 1.5))
    rolls = [circle(7.5, 11.5, 3), circle(16.5, 11.5, 3), circle(12, 9, 3.5)]
    return [shell(union(basket, *rolls)), detail(seg(3, 12.5, 21, 12.5)),
            detail(seg(8.5, 15.5, 9, 18)), detail(seg(12, 15.5, 12, 18)), detail(seg(15.5, 15.5, 15, 18))]


@icon("pastry-display", CAT, "Glass-fronted bakery display case with two shelves of cakes",
      tags=["display case", "bakery counter", "patisserie", "cake display", "glass case", "shop counter"],
      aliases=["display-case"])
def _(S):
    case = rect(2.5, 3, 19, 18, L(S, 1, 3.5))
    out = [shell(case), detail(seg(2.5, 16.5, 21.5, 16.5)), detail(seg(2.5, 10, 21.5, 10))]
    for y in (10, 16.5):
        out += [hole(f"M5.5 {y - 1}V{y - 2.5}C5.5 {y - 4.5} 9.5 {y - 4.5} 9.5 {y - 2.5}V{y - 1}Z"),
                hole(rect(14, y - 4, 4.5, 3, L(S, 0, 0.6)))]
    return out


@icon("bakery-shop", CAT, "Bakery shopfront with a scalloped awning, a display window with a loaf and a door",
      tags=["bakery", "baker", "boulangerie", "patisserie", "shop", "storefront"], aliases=["boulangerie"])
def _(S):
    n, x0, x1, y = 4, 2.5, 21.5, 8
    w = (x1 - x0) / n
    awn = f"M{x0} {y}V4.5C{x0} 3.5 3.5 3 4.5 3H19.5C20.5 3 {x1} 3.5 {x1} 4.5V{y}" if S.name == "rounded" else f"M{x0} {y}V3H{x1}V{y}"
    for i in range(n):
        awn += f"A{fmt(w / 2)} {fmt(w / 2)} 0 0 1 {fmt(x1 - (i + 1) * w)} {y}"
    awn += "Z"
    wall = poly([(4, 10.5), (4, 21), (20, 21), (20, 10.5)], r=S.r)
    loaf = "M7.5 17.5C7.5 15.5 9 15 10 15C11 15 12.5 15.5 12.5 17.5Z"
    return [shell(awn), line(wall), line(rect(5.5, 12.5, 8.5, 6.5, L(S, 0, 1))), solid(loaf),
            line(poly([(16, 21), (16, 12.5), (18.5, 12.5)], r=L(S, 0, 1)))]


# ============================================================================ sweets and dairy

@icon("cupcake-tower", CAT, "Two-tier stand holding cupcakes arranged in a pyramid",
      tags=["cupcake stand", "cupcake display", "party", "wedding", "dessert table", "cupcakes"],
      aliases=["cupcake-stand"])
def _(S):
    def cake(cx, by):
        cup = poly([(cx - 2.2, by), (cx + 2.2, by), (cx + 2.9, by - 3), (cx - 2.9, by - 3)], closed=True)
        top = f"M{fmt(cx - 2.9)} {fmt(by - 3)}A2.9 2.6 0 0 1 {fmt(cx + 2.9)} {fmt(by - 3)}Z"
        return [shell(union(cup, top)), detail(seg(cx - 2.9, by - 3, cx + 2.9, by - 3))]
    out = cake(12, 10) + cake(8, 19) + cake(16, 19)
    out += [line(seg(6, 11, 18, 11)), line(seg(12, 11, 12, 13.2)), line(seg(2.5, 20, 21.5, 20))]
    return out


@icon("candy-bag", CAT, "Striped paper sweet bag open at the top with round sweets and a lollipop peeking out",
      tags=["sweet bag", "sweets", "candy", "pick and mix", "treat bag", "party favor"], aliases=["sweet-bag"])
def _(S):
    bag = poly([(5, 11), (19, 11), (18, 21), (6, 21)], closed=True)
    sweets = [circle(8.5, 10, 2.3), circle(12.5, 10.5, 2)]
    out = [shell(union(bag, *sweets)), detail(seg(5, 11, 19, 11)), detail(seg(9.5, 14, 9.5, 21)),
           detail(seg(14.5, 14, 14.5, 21)), shell(circle(16.5, 5, 2.8)), line(seg(16.5, 7.8, 16.5, 11))]
    return out


@icon("mint-tin", CAT, "Small flat tin of mints with its hinged lid open, showing oval mints inside",
      tags=["mints", "breath mints", "peppermint", "tin", "sweets", "pocket tin"], aliases=["mints"])
def _(S):
    out = [shell(rbox(S, 3, 3.5, 18, 6.5, 3)), shell(rbox(S, 3, 12, 18, 8.5, 3))]
    for x in (7.5, 12, 16.5):
        out.append(hole(ellipse(x, 16.25, 2.1, 1.5)))
    return out


@icon("milk-splash", CAT, "Crown-shaped splash of milk rising from a flat pool with droplets flying up",
      tags=["splash", "milk", "liquid", "drop", "dairy", "pour"])
def _(S):
    crown = ("M4 18C5 16 5.5 14.5 5.5 12.5C7 13.5 7.5 14.5 8 15.5C8.5 13 8.5 11.5 8.5 9.5C10 11 10.8 12.5 11.2 14"
             "C11.5 12 12 10 12 8C12 10 12.5 12 12.8 14C13.2 12.5 14 11 15.5 9.5C15.5 11.5 15.5 13 16 15.5"
             "C16.5 14.5 17 13.5 18.5 12.5C18.5 14.5 19 16 20 18Z")
    pool = ellipse(12, 18.5, 9.5, 2.5)
    return [shell(union(crown, pool), stroke_miterlimit="2"), dot(8.5, 6.2, 1.2), dot(12, 4.3, 1.2), dot(15.5, 6.2, 1.2)]


@icon("milk-powder", CAT, "Tin of milk powder with a heap of powder above the rim and a scoop handle sticking out",
      tags=["powdered milk", "formula", "baby formula", "dry milk", "tin", "dairy"], aliases=["powdered-milk"])
def _(S):
    tin = rbox(S, 4, 11, 16, 10, 2.5)
    heap = "M4.5 11C6 7 9 6 12 6C15 6 18 7 19.5 11Z"
    return [shell(union(tin, heap)), detail(seg(4, 11, 20, 11)), detail(seg(8, 16, 16, 16)),
            line(seg(14, 7.5, 19.5, 3))]


@icon("condensed-milk", CAT, "Tilted can of condensed milk pouring a thick ribbon of milk",
      tags=["sweetened condensed milk", "evaporated milk", "can", "tin", "dairy", "baking"])
def _(S):
    can = rot(rbox(S, 3, 6, 9, 10, 1.5), 30, 7.5, 11)
    return [shell(can), detail(rot(seg(3, 8.5, 12, 8.5), 30, 7.5, 11)), line("M13 7C16.5 6.5 18.5 9 18.5 13V21")]


# ============================================================================ more baking tools

def thick(d, w):
    """Closed outline of a round-capped stroke of width w along d (for chunky bent parts)."""
    return path_to_d(ST(d, w, "round", "round"))


@icon("bench-scraper", CAT, "Bench scraper: a flat rectangular metal blade with a rolled handle along its top edge",
      tags=["dough scraper", "bench knife", "pastry scraper", "dough cutter", "baking", "dough"],
      aliases=["bench-knife"])
def _(S):
    handle = rbox(S, 3, 3.5, 18, 5, 2.5)
    blade = poly([(4.5, 8), (19.5, 8), (19.5, 20.5), (4.5, 20.5)], closed=True, r=L(S, 0, 1.5))
    return [shell(union(handle, blade)), detail(seg(3, 8.5, 21, 8.5)), detail(seg(8, 20.5, 8, 17.5)),
            detail(seg(12, 20.5, 12, 16)), detail(seg(16, 20.5, 16, 17.5))]


@icon("dough-hook", CAT, "Mixer dough hook: a collar on top and a thick curved hook below for kneading",
      tags=["kneading hook", "mixer attachment", "stand mixer", "kneading", "bread dough", "baking"])
def _(S):
    hook = path_to_d(ST("M12 8V12C12 14 7 15 7 18C7 20.3 9 21 11.5 21C15.5 21 18 18.5 18 14", 3.5,
                        L(S, "butt", "round"), "round"))
    return [shell(rect(8.5, 2, 7, 5, L(S, 0, 1.5))), shell(hook)]


@icon("bread-machine", CAT, "Bread machine: a countertop appliance with a lid window showing a loaf and a small control panel",
      tags=["bread maker", "breadmaker", "bread baker", "kitchen appliance", "home baking", "loaf"],
      )
def _(S):
    body = "M2.5 21V9.5C2.5 6.5 5 4 8 4H16C19 4 21.5 6.5 21.5 9.5V21Z" if S.name == "rounded" else \
        "M2.5 21V7L5.5 4H18.5L21.5 7V21Z"
    loaf = "M8 13.5V12.5C8 10 16 10 16 12.5V13.5Z"
    return [shell(body), detail(rect(5.5, 7, 13, 6.5, L(S, 0, 1))), hole(loaf), detail(seg(6, 17.5, 11, 17.5)),
            hole(circle(15, 17.5, 1.1)), hole(circle(18, 17.5, 1.1))]


@icon("toast-rack", CAT, "Toast rack: a wire arch on a base holding an upright slice of toast",
      tags=["toast holder", "breakfast", "toast", "tableware", "hotel breakfast", "bread"])
def _(S):
    toast = "M8 18V11C6.5 10.3 6.3 7.5 9 7.5H15C17.7 7.5 17.5 10.3 16 11V18Z"
    return [shell(toast, stroke_miterlimit="2"), line("M4 21V10C4 5.5 7.5 3.5 12 3.5C16.5 3.5 20 5.5 20 10V21"),
            line(seg(2, 21, 22, 21)), detail(seg(10.5, 13.5, 13.5, 13.5))]


# ============================================================================ sweets and pastries

@icon("choux-swan", CAT, "Choux pastry swan: a cream-filled puff with a pastry wing and a tall curved neck with a beak",
      tags=["cream puff swan", "swan pastry", "choux", "french pastry", "dessert", "patisserie"],
      aliases=["swan-puff"])
def _(S):
    base = "M3.5 14H20.5C20.5 18 17 20.5 12 20.5C7 20.5 3.5 18 3.5 14Z"
    cream = "M3.5 14C3.5 11.5 6.5 11 7.8 12.3C8.5 10.8 10.5 10.8 11.3 12Z"
    wing = "M11 14C11 9 14.5 5.5 20.5 4.5C20.5 9.5 19 13 16.5 14Z"
    neck = "M6.5 12.5C6.5 10.5 9 9.5 9 7C9 4 7.5 2.5 5.5 3.5"
    return [shell(union(base, cream, wing), stroke_miterlimit="2"), detail(seg(3.5, 14, 20.5, 14)),
            line(neck), line(seg(5.5, 3.5, 3.2, 5))]


@icon("twin-popsicle", CAT, "Twin ice pop: a rectangular ice lolly split down the middle with two wooden sticks",
      tags=["double ice pop", "twin ice lolly", "split popsicle", "ice pop", "frozen treat", "summer"],
      aliases=["twin-ice-pop"])
def _(S):
    body = minus(rbox(S, 4.5, 2.5, 15, 14, 4), poly([(10.5, 1), (13.5, 1), (12, 5)], closed=True))
    return [shell(body, stroke_miterlimit="2"), detail(seg(12, 6, 12, 16.5)),
            line(seg(8, 16.5, 8, 21.5)), line(seg(16, 16.5, 16, 21.5))]


@icon("rocket-popsicle", CAT, "Rocket ice pop: three stacked tiers narrowing to a pointed tip on a wooden stick",
      tags=["rocket ice lolly", "firecracker popsicle", "ice pop", "frozen treat", "summer", "ice lolly"],
      aliases=["rocket-ice-pop"])
def _(S):
    t1 = rbox(S, 6, 13, 12, 4.5, 1.5)
    t2 = rbox(S, 7.5, 8.5, 9, 5, 1)
    tip = poly([(9, 9), (15, 9), (12, 2.5)], closed=True, r=L(S, 0, 1))
    return [shell(union(t1, t2, tip), stroke_miterlimit="2"), detail(seg(7.5, 13, 16.5, 13)),
            detail(seg(9, 8.8, 15, 8.8)), line(seg(12, 17.5, 12, 22))]


# ============================================================================ breads, cheeses and cakes

@icon("cookie-press", CAT, "Cookie press: an upright tube with a plunger handle on top and a flower-shaped cookie below its nozzle plate",
      tags=["cookie gun", "spritz press", "biscuit press", "spritz cookies", "baking", "cookie maker"],
      aliases=["cookie-gun"])
def _(S):
    tube = rbox(S, 7, 5, 10, 7, 1.5)
    plate = rbox(S, 6, 12, 12, 2.5, 1)
    return [line(seg(7, 2.5, 17, 2.5)), line(seg(12, 2.5, 12, 5)), shell(tube), shell(plate),
            shell(_scallop(12, 18.3, 3.3, 6, 1.6)), dot(12, 18.3, 1)]


@icon("pyramid-cheese", CAT, "Pyramid goat cheese: a squat four-sided cheese with a flat top and an ash-dusted rind",
      tags=["goat cheese", "chevre", "ash rind cheese", "french cheese", "cheese board", "dairy"],
      aliases=["goat-cheese-pyramid"])
def _(S):
    outline = poly([(7.5, 6), (16.5, 6), (21.5, 19.5), (2.5, 19.5)], closed=True, r=L(S, 0, 1.2))
    return [shell(outline, stroke_miterlimit="2"), detail(seg(9.5, 6, 7.5, 19.5)), detail(seg(14.5, 6, 16.5, 19.5)),
            hole(circle(12, 11, 1.1)), hole(circle(11, 15.5, 1.1)), hole(circle(19, 16.5, 0.9)),
            hole(circle(5, 16.5, 0.9))]


@icon("melon-pan", CAT, "Melon pan: a round domed sweet bun with a crisp top scored in a crosshatch grid",
      tags=["melon bread", "japanese bun", "sweet bun", "cookie crust bun", "bakery", "pastry"],
      aliases=["melon-bread"])
def _(S):
    dome = "M2.5 17C2.5 9.5 7 5.5 12 5.5C17 5.5 21.5 9.5 21.5 17C21.5 18.7 20.5 19.5 19 19.5H5C3.5 19.5 2.5 18.7 2.5 17Z"
    return [shell(dome), detail(seg(5.5, 11, 13, 19.5)), detail(seg(9, 7, 18.5, 17.5)),
            detail(seg(18.5, 11, 11, 19.5)), detail(seg(15, 7, 5.5, 17.5))]


@icon("princess-cake", CAT, "Princess cake: a smooth dome-shaped cake with a marzipan cover and a single rose on top",
      tags=["prinsesstarta", "dome cake", "marzipan cake", "swedish cake", "layer cake", "dessert"],
      aliases=["prinsesstarta"])
def _(S):
    dome = "M3.5 19C3.5 13 7 9.5 12 9.5C17 9.5 20.5 13 20.5 19Z"
    rose = _scallop(12, 6, 3, 5, 1.5)
    leaf = "M13.5 8C14.5 6.3 17 5.8 18.5 6.5C17.8 8.3 15.5 9 13.5 8Z"
    return [shell(union(dome, rose, leaf)), detail(circle(12, 6, 0.9)), line(seg(2, 21.5, 22, 21.5))]


@icon("tomato-paste-tube", CAT, "Tube of tomato paste with a screw cap and its flat end rolled up",
      tags=["tomato puree", "paste tube", "concentrate", "tomato paste", "pantry", "cooking"],
      aliases=["tomato-puree-tube"])
def _(S):
    roll = rbox(S, 4.5, 2.5, 15, 5.5, 2.75)
    body = poly([(6, 8), (18, 8), (15.5, 16), (8.5, 16)], closed=True)
    neck = poly([(8.5, 16), (15.5, 16), (14, 18), (10, 18)], closed=True)
    cap = rect(9.5, 18, 5, 3.5, L(S, 0, 1))
    return [shell(union(roll, body, neck, cap), stroke_miterlimit="2"), detail(seg(6, 8, 18, 8)),
            detail(seg(9.5, 18, 14.5, 18)), hole(circle(12, 12, 1.8))]


# ============================================================================ cake scenes

def _axis(t, deg, s, w):
    """Point s along an axis from t at angle deg (screen degrees), offset w to its right."""
    a = math.radians(deg)
    return (t[0] + s * math.cos(a) - w * math.sin(a), t[1] + s * math.sin(a) + w * math.cos(a))


@icon("cake-decorating", CAT, "Cake decorating: a piping bag held over a round cake, piping icing onto its top edge",
      tags=["decorating cake", "icing", "frosting", "piping", "cake design", "baking class"],
      aliases=["decorate-cake"])
def _(S):
    tip, a = (12, 11.5), -45
    bag = poly([_axis(tip, a, 0, -0.9), _axis(tip, a, 0, 0.9), _axis(tip, a, 2.5, 1.5), _axis(tip, a, 8.5, 3.2),
                _axis(tip, a, 8.5, -3.2), _axis(tip, a, 2.5, -1.5)], closed=True, r=L(S, 0, 0.8))
    band = seg(*_axis(tip, a, 2.5, -1.5), *_axis(tip, a, 2.5, 1.5))
    cake = rbox(S, 2.5, 13.5, 16, 8, 3)
    return [shell(cake), detail("M2.5 17C4.5 17 4.5 18.5 6.5 18.5C8.5 18.5 8.5 17 10.5 17C12.5 17 12.5 18.5 14.5 18.5"
                                "C16.5 18.5 16.5 17 18.5 17"), shell(bag, stroke_miterlimit="2"), detail(band)]


@icon("cake-cutting", CAT, "Cake cutting: a round two-tier cake with a knife blade pushed into it from above",
      tags=["cutting the cake", "wedding cake", "cake knife", "celebration", "slice cake", "party"],
      aliases=["cut-cake"])
def _(S):
    cake = union(rbox(S, 2.5, 16.5, 17, 5, 2.5), rbox(S, 4.5, 12, 13, 5, 2))
    e, a = (12.5, 13), -62
    blade = poly([_axis(e, a, -6, -2), _axis(e, a, -6, 2), _axis(e, a, 6.5, 2), _axis(e, a, 6.5, -2)], closed=True)
    blade = minus(blade, path_to_d(U(P(cake), ST(cake, 3.0))))
    handle = poly([_axis(e, a, 6.5, -1.4), _axis(e, a, 6.5, 1.4), _axis(e, a, 11, 1.4), _axis(e, a, 11, -1.4)],
                  closed=True, r=L(S, 0, 1.3))
    return [shell(cake), detail(seg(4.5, 16.5, 17.5, 16.5)), shell(union(blade, handle), stroke_miterlimit="2"),
            detail(seg(*_axis(e, a, 6.5, -2), *_axis(e, a, 6.5, 2)))]


# ============================================================================ late additions

@icon("pastry-blender", CAT, "Pastry blender: a cross handle on top with curved U-shaped wires hanging below for cutting in butter",
      tags=["dough blender", "pastry cutter", "butter cutter", "pie crust", "biscuit dough", "baking tool"],
      aliases=["dough-blender"])
def _(S):
    outer = "M6.5 7V13.5A5.5 5.5 0 0 0 17.5 13.5V7"
    inner = "M10.5 7V15.5A1.5 1.5 0 0 0 13.5 15.5V7"
    return [shell(rect(4, 2.5, 16, 4.5, L(S, 0.5, 2.25))), line(outer), line(inner)]


@icon("monkey-bread", CAT, "Monkey bread: a ring-shaped loaf made of many small round dough balls baked together, seen from above",
      tags=["pull-apart bread", "bubble bread", "dough balls", "cinnamon bread", "bundt bread", "sweet bread"],
      aliases=["pull-apart-bread"])
def _(S):
    n = 8
    R, r = L(S, 7.5, 7.0), L(S, 3.0, 3.4)
    balls = union(*[circle(*pt_on(12, 12, R, -90 + i * 45), r) for i in range(n)])
    out = [shell(balls)]
    for i in range(n):
        a = -90 + 22.5 + i * 45
        out.append(detail(seg(*pt_on(12, 12, 5.7, a), *pt_on(12, 12, L(S, 8.2, 7.4), a))))
    return out


def _smooth_closed(pts):
    """Closed smooth curve (cubic Catmull-Rom) through the points."""
    n = len(pts)
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d + "Z"


@icon("bread-wreath", CAT, "Braided bread wreath: a round ring of plaited bread dough with a twisted braid running all the way around",
      tags=["braided bread", "bread ring", "challah wreath", "plait", "holiday bread", "christmas bread"],
      aliases=["braided-bread-ring"])
def _(S):
    n, per, mean, amp = 5, 8, 6.9, 2.4
    out = []
    for sign in (1, -1):
        pts = [pt_on(12, 12, mean + sign * amp * math.sin(2 * math.pi * k / per), -90 + k * 360 / (n * per))
               for k in range(n * per)]
        if S.name == "line":
            out.append(line(poly(pts, closed=True), stroke_miterlimit="1.5"))
        else:
            out.append(line(_smooth_closed(pts)))
    return out


@icon("provolone", CAT, "Provolone: a pear-shaped cheese hanging from a rope loop tied around its narrow neck and bound around its body",
      tags=["hanging cheese", "italian cheese", "cheese rope", "deli cheese", "cured cheese", "dairy"],
      aliases=["caciocavallo"])
def _(S):
    body = ("M10 7.5C10 6.5 10.8 6 12 6C13.2 6 14 6.5 14 7.5C14 9.5 17.5 11 18 15.5C18.3 19 15.5 21.5 12 21.5"
            "C8.5 21.5 5.7 19 6 15.5C6.5 11 10 9.5 10 7.5Z")
    return [shell(body), line("M10.5 6.5C8.5 3.5 10 1.8 12 1.8C14 1.8 15.5 3.5 13.5 6.5"),
            detail(seg(10, 9.5, 14, 9.5)), detail("M6.2 14.5C9 16.5 15 16.5 17.8 14.5")]
