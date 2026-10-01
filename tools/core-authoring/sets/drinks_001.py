"""TypeIcon Core: drinks (batch drinks_001): coffee and tea makers, cups, pots and accessories.

Mostly front or side views. Cups with a handle keep the handle on the right. Combined silhouettes
(a cup with a dome or scoop on top) are merged into one shell and a detail line marks the rim.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path.parser import parse_path
from geometry import SCALE, D, P, ST, U, fmt, path_to_d, rotation

CAT = "drinks"


# --------------------------------------------------------------------------- local helpers

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
    return tf(d, (-1, 0, 0, 1, 24, 0))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def hole(d):
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


def glass(S, x0, x1, y0, y1, bx0=None, bx1=None, r=None):
    """Tapered tumbler silhouette from top x0..x1 at y0 to bottom bx0..bx1 at y1."""
    bx0 = x0 + 1.2 if bx0 is None else bx0
    bx1 = x1 - 1.2 if bx1 is None else bx1
    return poly([(x0, y0), (x1, y0), (bx1, y1), (bx0, y1)], closed=True, r=S.r if r is None else r)


# ============================================================================ coffee drinks

@icon("latte-art", CAT, "Top view of a round cup with a heart poured in the foam and a small handle",
      tags=["latte", "foam art", "barista", "coffee", "cappuccino", "heart", "cafe"])
def _(S):
    heart = "M10 15.6L6.6 12.2A2.1 2.1 0 0 1 10 9.6A2.1 2.1 0 0 1 13.4 12.2Z"
    handle = poly([(17.3, 9.5), (20.8, 9.5), (20.8, 14.5), (17.3, 14.5)], r=S.r)
    return [shell(circle(10, 12, 7.5)), line(handle), detail(heart)]


@icon("latte-macchiato", CAT, "Tall glass with a handle showing milk, an espresso band and a foam cap",
      tags=["macchiato", "layered coffee", "latte", "glass", "espresso", "milk", "cafe"])
def _(S):
    body = glass(S, 3.5, 15.5, 3, 21, 4.6, 14.4, r=S.r)
    handle = poly([(15.3, 6.5), (20, 6.5), (20, 14.5), (14.8, 14.5)], r=S.r)
    return [shell(body), line(handle), detail(seg(4.2, 8, 14.8, 8)), detail(seg(4.6, 13.5, 14.4, 13.5))]


@icon("affogato", CAT, "Glass cup holding a scoop of ice cream with espresso pouring over it",
      tags=["ice cream", "espresso", "dessert", "coffee", "scoop", "italian", "pour"])
def _(S):
    cup = poly([(5, 12), (19, 12), (17.2, 20.5), (6.8, 20.5)], closed=True, r=S.r)
    scoop = circle(11, 9.5, 4.5)
    sil = union(cup, scoop)
    return [shell(sil), detail(seg(5.5, 12, 18.5, 12)), line("M20 2.5C17.5 3 16.5 5 16.5 7")]


@icon("iced-coffee", CAT, "Tall glass of coffee with ice cubes on top and a straw",
      tags=["cold coffee", "ice", "straw", "summer", "iced latte", "cafe", "drink"])
def _(S):
    body = glass(S, 5, 18, 6, 21, 6.4, 16.6)
    return [shell(body), detail(seg(5.4, 11.5, 17.6, 11.5)), sq(7.5, 8, 3, 2.5), sq(11.5, 8, 3, 2.5),
            detail(seg(12.5, 16, 16, 2.5))]


@icon("cold-brew", CAT, "Glass jar with a filter bag of grounds hanging inside on a string",
      tags=["cold brew", "mason jar", "steep", "coffee", "infusion", "iced coffee", "filter bag"])
def _(S):
    jar = poly([(7, 3.5), (17, 3.5), (17, 6), (19.5, 8.5), (19.5, 20), (4.5, 20), (4.5, 8.5), (7, 6)], closed=True, r=S.r)
    return [shell(jar), detail(rect(9, 12, 6, 5.5, L(S, 0, 1.2))), detail(seg(12, 12, 12, 2.5))]


@icon("frappe", CAT, "Clear cup with a domed lid, a thick straw and a liquid line",
      tags=["blended coffee", "iced", "cold drink", "cup with lid", "cafe", "milkshake"])
def _(S):
    cup = poly([(5.5, 10), (18.5, 10), (17, 21), (7, 21)], closed=True, r=S.r)
    dome = "M5.5 10A6.5 5.5 0 0 1 18.5 10Z"
    return [shell(union(cup, dome)), detail(seg(6, 10, 18, 10)), detail(seg(13.5, 15, 16, 2.5)),
            detail(seg(7.4, 16, 16.6, 16))]


@icon("irish-coffee", CAT, "Stemmed glass mug with coffee and a thick band of cream on top",
      tags=["whiskey coffee", "cream", "cocktail", "hot drink", "stemmed glass", "pub", "coffee"])
def _(S):
    bowl = "M4 4H16V9A6 6 0 0 1 4 9Z"
    handle = poly([(16, 6.5), (19.5, 6.5), (19.5, 10.5), (15.6, 10.5)], r=S.r)
    return [shell(bowl), line(handle), line(seg(10, 15, 10, 20)), line(seg(6, 20.5, 14, 20.5)),
            detail(seg(4.5, 8.5, 15.5, 8.5))]


@icon("cezve", CAT, "Small long-handled coffee pot with a wide base, narrow neck and pouring lip",
      tags=["ibrik", "turkish coffee", "briki", "coffee pot", "copper pot", "arabic coffee", "stovetop"],
      aliases=["ibrik"])
def _(S):
    body = poly([(4.5, 3.5), (13, 4), (13, 9.5), (16.5, 19.5), (4.5, 19.5), (8, 9.5), (8, 6)], closed=True, r=S.r)
    return [shell(body), line(seg(13.3, 7.5, 21.5, 3.5))]


@icon("dalgona-coffee", CAT, "Glass of milk topped with a peak of whipped coffee and a spoon",
      tags=["whipped coffee", "frothed coffee", "korean coffee", "cream", "trend", "milk", "spoon"])
def _(S):
    cup = poly([(5, 10), (17, 10), (15.8, 21), (6.2, 21)], closed=True, r=S.r)
    peak = poly([(6, 10), (7, 7), (10, 6), (11, 3), (12.5, 6), (14.5, 7), (16, 10)], closed=True, r=S.r)
    return [shell(union(cup, peak)), detail(seg(5.5, 10, 16.5, 10)), detail(seg(15, 13, 19, 5)), hole(circle(19.8, 3.6, 1.5))]


@icon("coffee-filter", CAT, "Paper cone filter with pleated folds",
      tags=["paper filter", "pour over", "brewing", "fluted", "drip", "coffee maker", "pleats"])
def _(S):
    cone = poly([(3, 6), (21, 6), (15, 20), (9, 20)], closed=True, r=S.r)
    return [shell(cone), detail(seg(8.5, 7, 10.3, 19)), detail(seg(12, 7, 12, 19)), detail(seg(15.5, 7, 13.7, 19))]


@icon("coffee-bean", CAT, "Single coffee bean with an S-shaped crease",
      tags=["beans", "roast", "arabica", "robusta", "caffeine", "coffee", "seed"])
def _(S):
    if S.name == "line":
        outline = "M12 2.5C18.5 6 18.5 18 12 21.5C5.5 18 5.5 6 12 2.5Z"
    else:
        outline = "M12 2.5C17 2.5 18.5 8 18.5 12C18.5 16 17 21.5 12 21.5C7 21.5 5.5 16 5.5 12C5.5 8 7 2.5 12 2.5Z"
    crease = "M12 3C8.5 7.5 15.5 10.5 12 15C10.5 17 11.5 19.5 12 21"
    return [shell(rot(outline, 40)), detail(rot(crease, 40))]


@icon("coffee-grinder", CAT, "Manual box grinder with a crank on top and a drawer at the bottom",
      tags=["hand grinder", "mill", "crank", "grind beans", "wooden grinder", "coffee", "manual"])
def _(S):
    return [shell(rect(5, 9, 14, 12, rr(S, 2))), line(poly([(12, 9), (12, 4.5), (19, 4.5), (19, 7)])),
            detail(seg(5.5, 15.5, 18.5, 15.5)), hole(circle(12, 18.3, 1))]


@icon("burr-grinder", CAT, "Electric grinder with a bean hopper on top and a grounds cup in front",
      tags=["electric grinder", "bean hopper", "grind", "barista", "coffee", "kitchen", "appliance"])
def _(S):
    hopper = poly([(5, 3), (19, 3), (15.5, 10), (8.5, 10)], closed=True, r=S.r)
    body = rect(6, 10, 12, 11, rr(S, 2))
    return [shell(union(hopper, body)), detail(rect(9.5, 14.5, 5, 4.5, 0))]


@icon("espresso-machine", CAT, "Boxy espresso machine with a group head, portafilter and cup underneath",
      tags=["coffee machine", "barista", "cafe", "portafilter", "pressure", "brew", "espresso"])
def _(S):
    body = rect(3, 3, 18, 9, rr(S, 2.5))
    head = rect(9, 11, 6, 4.5, 0)
    cup = poly([(9, 18.5), (15, 18.5), (14.2, 21.5), (9.8, 21.5)], closed=True, r=S.r)
    return [shell(union(body, head)), shell(cup), hole(circle(7, 7.5, 1.3)), detail(seg(11.5, 7.5, 17.5, 7.5))]


@icon("moka-pot", CAT, "Faceted stovetop coffee pot with a pinched waist, pointed spout and side handle",
      tags=["stovetop espresso", "italian coffee", "coffee pot", "percolator", "octagonal", "brew", "camping"])
def _(S):
    body = poly([(4.5, 4), (17, 4), (15, 12), (18.5, 20.5), (5.5, 20.5), (9, 12), (7, 6.5)], closed=True, r=S.r)
    handle = poly([(16.3, 6.5), (20.5, 6.5), (20.5, 16), (17, 16)], r=S.r)
    return [shell(body), line(handle), detail(seg(9.3, 12, 14.7, 12))]


@icon("french-press", CAT, "Glass beaker in a frame with a plunger rod and knob rising from the lid",
      tags=["cafetiere", "press pot", "plunger", "coffee maker", "brew", "immersion", "kitchen"],
      aliases=["cafetiere"])
def _(S):
    body = rect(6, 10.5, 11, 10.5, rr(S, 2))
    lid = rect(4.5, 8, 14, 3, rr(S, 1))
    handle = poly([(16.8, 13), (20.5, 13), (20.5, 18.5), (16.8, 18.5)], r=S.r)
    return [shell(union(body, lid)), line(handle), detail(seg(11.5, 8, 11.5, 4.2)), solid(circle(11.5, 3.8, 2)),
            detail(seg(6.5, 16, 16.5, 16))]


@icon("pour-over-dripper", CAT, "Cone dripper sitting above a mug with a drop falling between them",
      tags=["pour over", "drip cone", "manual brew", "filter coffee", "drop", "mug"])
def _(S):
    cone = poly([(4, 2.5), (17, 2.5), (12.8, 9.5), (8.2, 9.5)], closed=True, r=S.r)
    mug = rect(5, 14.5, 11, 6.5, rr(S, 2))
    handle = poly([(15.8, 16), (19.5, 16), (19.5, 19.5), (15.8, 19.5)], r=S.r)
    return [shell(cone), shell(mug), line(handle), hole(circle(10.5, 12.3, 1.1))]


@icon("siphon-coffee-maker", CAT, "Two stacked glass globes joined by a tube on a stand with a flame underneath",
      tags=["vacuum pot", "syphon", "coffee maker", "brewing", "glass", "science", "barista"],
      aliases=["syphon"])
def _(S):
    flame = "M9 18.6C11 20.2 11.2 21.8 9 21.8C6.8 21.8 7 20.2 9 18.6Z"
    return [shell(circle(9, 5.5, 3.5)), shell(circle(9, 14, 4.5)), line(seg(9, 9, 9, 9.5)),
            line(seg(19, 3, 19, 21)), line(seg(13, 5, 19, 5)), line(seg(13.5, 14, 19, 14)), solid(flame)]


@icon("drip-coffee-maker", CAT, "Countertop coffee machine with a tall back, a brew head and a carafe on the base",
      tags=["coffee machine", "filter coffee", "brewer", "carafe", "kitchen appliance", "office", "morning"])
def _(S):
    frame = union(rect(13.5, 3, 7.5, 18, rr(S, 2)), rect(3, 3, 18, 5, rr(S, 2)), rect(3, 18.5, 18, 2.5, rr(S, 1)))
    carafe = poly([(5, 11.5), (11, 11.5), (11, 16.5), (5, 16.5)], closed=True, r=S.r)
    return [shell(frame), shell(carafe), hole(circle(8, 9.3, 0.8))]


@icon("coffee-carafe", CAT, "Round glass coffee pot with a collar, a handle and a level line",
      tags=["glass pot", "decanter", "coffee pot", "brew", "serve", "drip", "kitchen"])
def _(S):
    body = "M8.5 7H13.5C17 9 17.5 12 17.5 15C17.5 19 15 21 11 21C7 21 4.5 19 4.5 15C4.5 12 5 9 8.5 7Z"
    collar = rect(8, 3, 6, 4.5, rr(S, 1.5))
    handle = poly([(17.2, 10), (20.5, 10), (20.5, 16.5), (17.4, 16.5)], r=S.r)
    return [shell(union(body, collar)), line(handle), detail(seg(5, 13.5, 17, 13.5))]


@icon("percolator", CAT, "Tall tapered pot with a domed lid, a glass knob and a side handle",
      tags=["coffee pot", "camping", "stovetop", "campfire", "brew", "tapered pot", "outdoor"])
def _(S):
    body = poly([(6, 8), (16, 8), (17, 20.5), (5, 20.5)], closed=True, r=S.r)
    dome = "M6.5 8A4.5 3.2 0 0 1 15.5 8Z"
    handle = poly([(16.4, 11), (20.5, 11), (20.5, 17), (16.8, 17)], r=S.r)
    return [shell(union(body, dome)), line(handle), solid(circle(11, 3.8, 1.6)), detail(seg(6.3, 8.3, 15.7, 8.3)),
            detail(seg(5.5, 15, 16.5, 15))]


@icon("cold-drip-tower", CAT, "Tall stand with a water globe on top, a drip tube in the middle and a carafe at the bottom",
      tags=["cold brew tower", "kyoto", "slow drip", "coffee dripper", "coffee maker", "glass", "barista"])
def _(S):
    carafe = poly([(9, 14.5), (15, 14.5), (16.5, 21), (7.5, 21)], closed=True, r=S.r * 0.5)
    return [line(seg(3.5, 3, 3.5, 21)), line(seg(20.5, 3, 20.5, 21)), line(seg(3.5, 10, 20.5, 10)),
            shell(circle(12, 6, 3.2)), line(seg(12, 10, 12, 12.5)), shell(carafe)]


@icon("portafilter", CAT, "Round filter basket with a long straight handle and two spouts underneath",
      tags=["portafilter", "espresso", "group handle", "basket", "barista", "coffee", "tool"])
def _(S):
    basket = poly([(2.5, 6), (14.5, 6), (13.3, 12), (3.7, 12)], closed=True, r=S.r)
    grip = rect(14.5, 7.3, 7.5, 3.4, rr(S, 1.7))
    return [shell(basket), shell(grip), line(seg(6.3, 12.5, 6.3, 17.5)), line(seg(10.7, 12.5, 10.7, 17.5))]


@icon("coffee-tamper", CAT, "Flat round tamper with a rounded knob handle on top",
      tags=["tamp", "espresso", "barista", "press grounds", "puck", "coffee", "tool"])
def _(S):
    knob = rect(8, 4.5, 8, 11, rr(S, 3))
    base = rect(4, 15.5, 16, 4.5, rr(S, 1.5))
    return [shell(union(knob, base)), detail(seg(4.5, 15.5, 19.5, 15.5))]


@icon("milk-frother", CAT, "Handheld wand with a button on the grip and a small wire whisk at the tip",
      tags=["frother", "whisk", "foam", "latte", "milk", "barista", "battery"])
def _(S):
    coil = "M12 15C8 16.2 8 21 12 21C16 21 16 16.2 12 15Z"
    return [shell(rect(9.5, 2.5, 5, 11, rr(S, 2.5))), hole(circle(12, 6.5, 1.1)), line(seg(12, 13.5, 12, 15.5)),
            line(coil)]


@icon("frothing-pitcher", CAT, "Small steel jug with a pointed spout, a tapered body and a loop handle",
      tags=["milk jug", "steaming pitcher", "barista", "latte art", "pour", "stainless", "coffee"])
def _(S):
    body = poly([(3.5, 4.5), (16, 4.5), (14.8, 20.5), (7.8, 20.5), (7.3, 10)], closed=True, r=S.r)
    handle = poly([(15.7, 7.5), (20.3, 7.5), (19.6, 16.5), (14.8, 16.5)], r=S.r)
    return [shell(body), line(handle)]


@icon("coffee-capsule", CAT, "Small pod shaped like a truncated cone with a ridged rim and flat lid",
      tags=["pod", "single serve", "cartridge", "espresso", "coffee"])
def _(S):
    rim = rect(4, 4.5, 16, 3.5, rr(S, 1.2))
    cone = poly([(5.5, 7), (18.5, 7), (15.5, 20.5), (8.5, 20.5)], closed=True, r=S.r)
    return [shell(union(rim, cone)), detail(seg(4.5, 8.3, 19.5, 8.3)), detail(seg(8, 13.5, 16, 13.5))]


@icon("coffee-bag", CAT, "Stand-up pouch with a folded top, a valve and a bean on the front",
      tags=["coffee beans", "roasted", "pouch", "package", "retail", "one-way valve", "grocery"])
def _(S):
    bean = rot(ellipse(12, 15, 2.6, 3.8), 35, 12, 15)
    return [shell(rect(5, 3.5, 14, 17.5, rr(S, 4))), detail(seg(5.5, 8.5, 18.5, 8.5)), hole(circle(12, 6, 1)),
            hole(bean)]


@icon("coffee-sack", CAT, "Tied burlap sack with a coffee bean on the front",
      tags=["burlap", "bag", "green coffee", "beans", "harvest", "export", "farm"])
def _(S):
    if S.name == "line":
        sack = poly([(9, 3.5), (15, 3.5), (14.5, 7), (19, 12), (19, 21), (5, 21), (5, 12), (9.5, 7)], closed=True)
    else:
        sack = "M9 3.5H15L14.5 7C17.5 8.5 19 12 19 16C19 19.5 17 21 12 21C7 21 5 19.5 5 16C5 12 6.5 8.5 9.5 7Z"
    bean = rot(ellipse(12, 15, 2.3, 3.5), 35, 12, 15)
    return [shell(sack), detail(seg(9.3, 7.3, 14.7, 7.3)), hole(bean)]


@icon("coffee-cherries", CAT, "Short branch with a pointed leaf and a pair of round coffee cherries",
      tags=["coffee fruit", "coffee plant", "berries", "harvest", "farm", "branch", "arabica"])
def _(S):
    if S.name == "line":
        leaf = "M11.5 9C11.5 5 15 3 20.5 3.5C20.5 7.5 17 9.5 11.5 9Z"
    else:
        leaf = poly([(11.5, 9), (13, 5), (16.5, 3.6), (20.5, 3.6), (19.3, 7.6), (15.5, 9.2)], closed=True, r=S.r)
    return [shell(circle(6.5, 16.5, 3.7)), shell(circle(15.5, 16.5, 3.7)), line(seg(7.2, 12.9, 11.5, 9)),
            line(seg(14.8, 12.9, 11.5, 9)), line(seg(11.5, 9, 7, 4)), shell(leaf)]


@icon("gooseneck-kettle", CAT, "Kettle with a slender curved spout rising from the base and an arched handle",
      tags=["pour over kettle", "swan neck", "tea kettle", "barista", "precise pour", "water", "brew"])
def _(S):
    body = poly([(3, 11), (15, 11), (15, 20.5), (3, 20.5)], closed=True, r=S.r)
    return [shell(body), line("M5 11C5 3.5 13 3.5 13 11"), line("M15 18.5C18 18.5 19 15.5 17.5 12.5C16.7 11 17.5 9.5 20.5 9.5")]


@icon("coffee-scoop", CAT, "Round scoop with a straight handle holding a heap of beans",
      tags=["measure", "measuring scoop", "beans", "dose", "grounds", "spoon", "coffee"])
def _(S):
    bowl = "M3.5 12H14.5A5.5 5.5 0 0 1 3.5 12Z"
    heap = "M5 12A4 4.5 0 0 1 13 12Z"
    return [shell(union(bowl, heap)), detail(seg(4, 12, 14, 12)), line(seg(14.5, 11.5, 20.5, 6.5))]


@icon("coffee-roaster", CAT, "Drum roaster with a funnel hopper on top and a cooling bar in front",
      tags=["roasting", "roastery", "beans", "drum", "coffee machine", "artisan", "cafe"])
def _(S):
    hopper = poly([(7, 2.5), (17, 2.5), (14.5, 9), (9.5, 9)], closed=True, r=S.r)
    body = rect(4, 8.5, 16, 8.5, rr(S, 2))
    return [shell(union(hopper, body)), detail(circle(12, 13, 1.9)), line(seg(3.5, 20.5, 20.5, 20.5))]


@icon("coffee-urn", CAT, "Tall cylindrical urn on short legs with a tap and a sight tube",
      tags=["percolator urn", "catering", "dispenser", "large batch", "hot drink", "event", "tap"])
def _(S):
    return [shell(rect(6, 3.5, 12, 14, rr(S, 2.5))), detail(seg(6.5, 7.5, 17.5, 7.5)), detail(seg(13.5, 10, 13.5, 14.5)),
            line(poly([(6, 14.5), (3, 14.5), (3, 17)], r=S.r)), line(seg(8, 17.5, 7, 21)), line(seg(16, 17.5, 17, 21))]


@icon("coffee-to-go", CAT, "Tapered paper cup with a raised sip lid and a sleeve band around the middle",
      tags=["takeaway", "takeout", "to go cup", "disposable", "cafe", "hot drink", "sleeve"])
def _(S):
    cup = poly([(6, 8), (18, 8), (16.5, 21), (7.5, 21)], closed=True, r=S.r)
    lid = rect(5, 5, 14, 3, rr(S, 1.5))
    tip = rect(8.5, 3, 7, 2.5, rr(S, 1))
    return [shell(union(cup, lid, tip)), detail(seg(5.5, 8, 18.5, 8)), detail(seg(7, 13, 17, 13)), detail(seg(7.2, 17, 16.8, 17))]


@icon("cup-carrier", CAT, "Cardboard tray holding two takeaway cups side by side",
      tags=["drink tray", "cup holder", "takeaway", "coffee run", "delivery", "office", "two cups"])
def _(S):
    c1 = poly([(3.5, 3.5), (10.3, 3.5), (9.5, 14), (4.3, 14)], closed=True, r=S.r * 0.6)
    c2 = poly([(13.7, 3.5), (20.5, 3.5), (19.7, 14), (14.5, 14)], closed=True, r=S.r * 0.6)
    tray = rect(3, 13, 18, 8, rr(S, 2))
    return [shell(union(c1, c2, tray)), detail(seg(4.6, 6.5, 9.2, 6.5)), detail(seg(14.8, 6.5, 19.4, 6.5)),
            detail(seg(3.5, 14.5, 20.5, 14.5))]


@icon("pod-coffee-machine", CAT, "Compact pod machine with a hinged top, a mug recess and a button",
      tags=["capsule machine", "single serve", "coffee maker", "pod", "kitchen", "office"])
def _(S):
    body = union(rect(4, 3, 16, 5.5, rr(S, 2.5)), rect(5, 8, 14, 13, rr(S, 2)))
    return [shell(body), detail(seg(4.5, 8.5, 19.5, 8.5)), detail(rect(8.5, 12.5, 7, 5.5, 0)), hole(circle(8, 5.8, 1))]


@icon("vietnamese-coffee-filter", CAT, "Small metal drip filter with a lid sitting on a short glass with a dark layer at the bottom",
      tags=["phin", "drip filter", "vietnamese coffee", "slow drip", "condensed milk", "glass", "brew"],
      aliases=["phin"])
def _(S):
    knob = rect(9.5, 2.5, 5, 3, rr(S, 1))
    cup = poly([(6, 5), (18, 5), (17.5, 10.5), (6.5, 10.5)], closed=True, r=S.r * 0.6)
    flange = rect(4, 10, 16, 2.6, rr(S, 1))
    body = poly([(6.5, 12), (17.5, 12), (16.8, 21), (7.2, 21)], closed=True, r=S.r)
    return [shell(union(knob, cup, flange, body)), detail(seg(6.5, 7.5, 17.5, 7.5)), detail(seg(7.3, 17, 16.7, 17))]


@icon("dallah", CAT, "Arabic coffee pot with a curved beak spout, a pinched waist and a pointed lid",
      tags=["arabic coffee", "gulf coffee", "qahwa", "middle eastern", "hospitality", "brass pot", "pot"])
def _(S):
    body = poly([(9, 7.5), (15, 7.5), (14.3, 11.5), (17.5, 20.5), (6.5, 20.5), (9.7, 11.5)], closed=True, r=S.r)
    dome = "M9 7.5A3 2.5 0 0 1 15 7.5Z"
    finial = poly([(11, 5.2), (13, 5.2), (12, 2.5)], closed=True)
    handle = poly([(14.6, 9.5), (19.5, 9.5), (19.5, 17.5), (16.6, 17.5)], r=S.r)
    return [shell(union(body, dome)), line(handle), solid(finial),
            line("M7.5 17C4 14.5 3.5 9 3.8 5.3L6.8 6.3"), detail(seg(9.9, 11.5, 14.1, 11.5))]


@icon("drip-bag-coffee", CAT, "Paper filter bag hooked over the rim of a cup by two side tabs",
      tags=["hanging filter", "single serve", "instant pour over", "travel coffee", "office", "sachet", "brew"])
def _(S):
    cup = poly([(5, 13), (19, 13), (17.5, 21), (6.5, 21)], closed=True, r=S.r)
    bag = rect(8, 4, 8, 9.5, rr(S, 1.5))
    return [shell(union(cup, bag)), detail(seg(5.5, 13, 18.5, 13)),
            line(poly([(8, 7), (3.5, 7), (3.5, 11.5)], r=S.r)), line(poly([(16, 7), (20.5, 7), (20.5, 11.5)], r=S.r))]


@icon("cafe-au-lait-bowl", CAT, "Wide handleless bowl of coffee with a steam curl above it",
      tags=["cafe au lait", "french breakfast", "bowl coffee", "latte bowl", "hot drink", "steam", "morning"])
def _(S):
    if S.name == "line":
        bowl = poly([(3, 11.5), (21, 11.5), (17.5, 20), (6.5, 20)], closed=True)
    else:
        bowl = "M3 11.5H21C21 17 17.5 20 12 20C6.5 20 3 17 3 11.5Z"
    return [shell(bowl), line("M9 8C7.5 6.5 10.5 5.5 9 4"), line("M15 8C13.5 6.5 16.5 5.5 15 4")]


@icon("syrup-pump-bottle", CAT, "Tall bottle with a pump head and a curved nozzle on top",
      tags=["flavor syrup", "barista", "dispenser", "sweetener", "pump", "coffee shop", "caramel"])
def _(S):
    bottle = poly([(10, 7.5), (14, 7.5), (14, 9), (17, 11.5), (17, 21), (7, 21), (7, 11.5), (10, 9)], closed=True, r=S.r)
    return [shell(bottle), line(poly([(12, 7.5), (12, 3.5), (17.5, 3.5), (17.5, 5.5)], r=S.r)),
            detail(rect(9.5, 14, 5, 4, 0))]


@icon("coffee-cart", CAT, "Small wheeled cart with a canopy and a coffee machine on the counter",
      tags=["coffee stand", "kiosk", "street vendor", "mobile cafe", "barista cart", "stall", "food truck"])
def _(S):
    canopy = poly([(3, 8), (5, 3.5), (19, 3.5), (21, 8)], closed=True, r=S.r)
    counter = union(rect(9.5, 10, 5, 4, 0), rect(4, 13.5, 16, 5.5, rr(S, 1.5)))
    return [shell(canopy), shell(counter), line(seg(6, 8.5, 6, 13.5)), line(seg(18, 8.5, 18, 13.5)),
            solid(circle(8, 20, 1.9)), solid(circle(16, 20, 1.9))]


@icon("sugar-packet", CAT, "Small paper packet with a tear notch and a few grains spilling out",
      tags=["sweetener", "sugar sachet", "stick pack", "cafe table", "sachet", "grains", "condiment"])
def _(S):
    packet = poly([(5.5, 3.5), (18.5, 3.5), (18.5, 8), (16.3, 9.5), (18.5, 11), (18.5, 18), (5.5, 18)], closed=True, r=S.r)
    return [shell(packet), detail(seg(6, 6.8, 18, 6.8)), solid(circle(8, 21, 0.9)), solid(circle(12, 20.8, 0.9)),
            solid(circle(16, 21, 0.9))]


@icon("creamer-cup", CAT, "Tiny single-serve cup with a peel-back lid lifted at one corner",
      tags=["coffee creamer", "portion cup", "milk cup", "single serve", "cafe", "diner", "peel lid"])
def _(S):
    cup = poly([(5, 11), (19, 11), (17.5, 21), (6.5, 21)], closed=True, r=S.r)
    return [shell(cup), line(poly([(5, 8), (14, 8), (20.5, 3.5)], r=S.r))]


@icon("sugar-bowl", CAT, "Round lidded bowl with two small handles and a spoon poking out",
      tags=["sugar pot", "tea service", "lidded bowl", "dining table", "sweetener", "tableware", "spoon"])
def _(S):
    if S.name == "line":
        bowl = poly([(5, 12), (19, 12), (16.5, 20.5), (7.5, 20.5)], closed=True)
        dome = poly([(6.5, 12), (8.5, 8), (15.5, 8), (17.5, 12)], closed=True)
    else:
        bowl = "M5 12H19C19 17.5 16 20.5 12 20.5C8 20.5 5 17.5 5 12Z"
        dome = "M6.5 12A5.5 4.5 0 0 1 17.5 12Z"
    h = poly([(5.3, 13.2), (2.7, 13.2), (2.7, 16), (6.3, 16)], r=S.r)
    return [shell(union(bowl, dome)), detail(seg(5.5, 12, 18.5, 12)), line(h), line(flip(h)),
            line(seg(14.5, 8, 19, 3.5))]


@icon("cream-jug", CAT, "Small squat pitcher with a wide pouring lip and a loop handle",
      tags=["creamer", "milk jug", "tea service", "pitcher", "tableware", "gravy", "pour"])
def _(S):
    body = poly([(3.5, 5.5), (14, 5.5), (16, 13), (14.3, 21), (6, 21), (4.8, 13), (5.8, 10)], closed=True, r=S.r * 1.3)
    handle = poly([(15.5, 8.5), (20, 8.5), (20, 16), (15.3, 16)], r=S.r)
    return [shell(body), line(handle)]


@icon("tea-leaf", CAT, "Two pointed tea leaves and a bud on a short stem",
      tags=["tea plant", "camellia", "green tea", "herbal", "sprig", "leaves", "harvest"])
def _(S):
    if S.name == "line":
        leaf = "M11.5 15.5C6.5 15.5 4.2 12.5 4 8.5C8.5 8.5 11.5 11 11.5 15.5Z"
        bud = "M12 11.5C10 8.5 10.3 5 12 2.8C13.7 5 14 8.5 12 11.5Z"
    else:
        leaf = poly([(11.5, 15.5), (6, 14), (4.3, 8.7), (10, 10.2)], closed=True, r=S.r)
        bud = poly([(12, 11.5), (10, 7.5), (12, 2.8), (14, 7.5)], closed=True, r=S.r)
    return [shell(leaf), shell(flip(leaf)), shell(bud), line(seg(12, 15, 12, 21))]


@icon("tea-infuser", CAT, "Mesh ball infuser with a seam, a chain and a hook",
      tags=["tea ball", "loose leaf", "steeper", "mesh", "brewing", "tea", "strainer"])
def _(S):
    ball = circle(12, 14, 6.5) if S.name == "rounded" else poly(regular(12, 14, 7, 10), closed=True)
    return [shell(ball), detail(seg(5.6, 14, 18.4, 14)), hole(circle(9, 11.3, 0.8)), hole(circle(15, 11.3, 0.8)),
            hole(circle(9, 17, 0.8)), hole(circle(15, 17, 0.8)), line("M12 7.5V3.5H16.5V5.5")]


@icon("tea-strainer", CAT, "Small mesh bowl strainer with a long handle and a hook at the end",
      tags=["sieve", "loose tea", "filter", "mesh", "kitchen tool", "cup strainer", "pouring"])
def _(S):
    if S.name == "line":
        bowl = poly([(3, 9), (15, 9), (13, 15), (5, 15)], closed=True)
    else:
        bowl = "M3 9H15A6 6.5 0 0 1 3 9Z"
    return [shell(bowl), hole(circle(6.5, 11.5, 0.8)), hole(circle(11.5, 11.5, 0.8)), hole(circle(9, 13.3, 0.8)),
            line(poly([(15, 9), (21, 9), (21, 12)], r=S.r))]


@icon("matcha-bowl", CAT, "Wide low tea bowl on a small foot with a row of foam bubbles",
      tags=["chawan", "green tea", "japanese tea", "tea ceremony", "froth", "foam", "whisked"])
def _(S):
    if S.name == "line":
        bowl = poly([(3, 8.5), (21, 8.5), (17.5, 18), (6.5, 18)], closed=True)
    else:
        bowl = "M3 8.5H21C21 14.5 17 18 12 18C7 18 3 14.5 3 8.5Z"
    return [shell(bowl), hole(circle(8, 12, 1)), hole(circle(12, 12, 1)), hole(circle(16, 12, 1)), line(seg(9.5, 21, 14.5, 21))]


@icon("matcha-whisk", CAT, "Bamboo whisk with a round handle and a dome of fine curved tines",
      tags=["chasen", "bamboo", "green tea", "tea ceremony", "froth", "japanese", "whisking"],
      aliases=["chasen"])
def _(S):
    bulb = "M8 11C4.5 13.5 4.5 20 9 21.5H15C19.5 20 19.5 13.5 16 11Z"
    handle = rect(9, 2.5, 6, 9, rr(S, 3))
    return [shell(union(bulb, handle)), detail(seg(12, 12, 12, 21)), detail("M8.8 12.5C7.4 15.5 7.8 19 9 21"),
            detail("M15.2 12.5C16.6 15.5 16.2 19 15 21")]


@icon("bubble-tea", CAT, "Sealed plastic cup with a wide straw through the lid and round pearls at the bottom",
      tags=["boba", "tapioca", "pearl milk tea", "taiwanese", "cold drink", "straw", "tea"],
      aliases=["boba"])
def _(S):
    cup = poly([(5.5, 8), (18.5, 8), (17, 21), (7, 21)], closed=True, r=S.r)
    lid = rect(5, 6, 14, 2.5, rr(S, 1))
    return [shell(union(cup, lid)), detail(seg(5.5, 8.5, 18.5, 8.5)), detail(seg(12.5, 13, 16, 2.5)),
            hole(circle(9, 18, 1.3)), hole(circle(12.3, 18.8, 1.3)), hole(circle(15, 17.8, 1.3)), hole(circle(10.5, 15, 1.1)),
            hole(circle(14, 14.6, 1.1))]


@icon("iced-tea", CAT, "Tall glass with ice cubes, a lemon wheel on the rim and a long spoon",
      tags=["cold tea", "lemon tea", "summer drink", "ice", "citrus", "refreshment", "glass"])
def _(S):
    glass_ = glass(S, 4.5, 16.5, 5, 21, 5.8, 15.2)
    return [shell(union(glass_, circle(17, 5, 3.4))), detail(seg(5, 11, 16, 11)), sq(7, 8, 3, 2.3), sq(11, 8, 3, 2.3),
            detail(seg(8.5, 17, 6, 2.6))]


@icon("gaiwan", CAT, "Small lidded tea bowl on a saucer with the lid slightly tilted",
      tags=["chinese tea", "gongfu", "tea ceremony", "lidded bowl", "saucer", "porcelain", "brewing"])
def _(S):
    if S.name == "line":
        bowl = poly([(5, 11.5), (19, 11.5), (16.5, 17.5), (7.5, 17.5)], closed=True)
        lid = poly([(6.5, 10.5), (8.5, 6.5), (15.5, 6.5), (17.5, 10.5)], closed=True)
    else:
        bowl = "M5 11.5H19C19 15.5 16 17.5 12 17.5C8 17.5 5 15.5 5 11.5Z"
        lid = "M6.5 10.5A5.5 4.5 0 0 1 17.5 10.5Z"
    return [shell(bowl), shell(rot(lid, -12, 6.5, 10.5)), line(seg(3.5, 20.5, 20.5, 20.5))]


@icon("samovar", CAT, "Tall metal urn with side handles and a tap, a small teapot on top",
      tags=["russian tea", "tea urn", "hot water", "brass", "tea service", "persian", "urn"])
def _(S):
    body = poly([(7, 9), (17, 9), (18.5, 13.5), (17, 19), (7, 19), (5.5, 13.5)], closed=True, r=S.r)
    foot = rect(8, 18.5, 8, 2.7, rr(S, 1))
    pot = rect(9.5, 4.5, 5, 4, rr(S, 1.5))
    h = poly([(5.8, 12), (3, 12), (3, 15)], r=S.r)
    return [shell(union(body, foot)), shell(pot), line(h), line(flip(h)), hole(circle(12, 14, 1.2)),
            detail(seg(7.3, 10, 16.7, 10))]


@icon("tulip-tea-glass", CAT, "Small tulip-shaped glass with a curved waist standing on a saucer",
      tags=["turkish tea", "armudu", "cay", "tea glass", "saucer", "waisted glass", "hot drink"])
def _(S):
    glass_ = poly([(6.5, 3.5), (17.5, 3.5), (15.3, 9), (17, 14), (15.3, 17.5), (8.7, 17.5), (7, 14), (8.7, 9)], closed=True, r=S.r * 1.3)
    return [shell(glass_), detail(seg(7.4, 7, 16.6, 7)), line(seg(3.5, 20.5, 20.5, 20.5))]


@icon("tea-glass-holder", CAT, "Straight tea glass set in a metal holder with a curved handle",
      tags=["podstakannik", "chai glass", "tea holder", "metal holder", "russian tea", "handle", "hot drink"])
def _(S):
    glass_ = glass(S, 4.5, 15.5, 3.5, 20, 5.3, 14.7)
    holder = rect(3.8, 11, 12.4, 9.5, rr(S, 2))
    return [shell(union(glass_, holder)), detail(seg(4.3, 11.3, 15.7, 11.3)), detail(seg(5.5, 7, 14.5, 7)),
            hole(circle(7.5, 16, 0.9)), hole(circle(12.5, 16, 0.9)), line("M16 12.5C21 12.5 21 19 16 19")]


@icon("kulhad-cup", CAT, "Small unglazed clay cup without a handle, wider at the top, with steam rising",
      tags=["chai", "clay cup", "terracotta", "indian tea", "earthenware", "masala chai", "steam"])
def _(S):
    cup = poly([(5, 9), (19, 9), (17.3, 12.5), (15.3, 15), (16, 20.5), (8, 20.5), (8.7, 15), (6.7, 12.5)], closed=True, r=S.r)
    return [shell(cup), detail(seg(8.6, 15, 15.4, 15)), line("M9 6.5C7.5 5 10.5 4 9 2.5"), line("M15 6.5C13.5 5 16.5 4 15 2.5")]


@icon("kombucha", CAT, "Large glass jar with a floating culture disc and a cloth tied over the mouth",
      tags=["fermented tea", "scoby", "ferment", "probiotic", "jar", "brew", "home brewing"])
def _(S):
    cloth = poly([(6, 3.5), (18, 3.5), (20.5, 8), (3.5, 8), ], closed=True, r=S.r)
    jar = rect(4.5, 7.5, 15, 13.5, rr(S, 4))
    return [shell(union(cloth, jar)), detail(seg(4.6, 8, 19.4, 8)), detail(seg(7, 12.5, 17, 12.5)),
            hole(circle(8.5, 17, 1)), hole(circle(14, 17.8, 1)), hole(circle(11.5, 15.5, 0.9))]


@icon("mate-gourd", CAT, "Round gourd cup filled with herbs and a metal straw with a flattened tip",
      tags=["yerba mate", "bombilla", "calabash", "south american", "herbal tea", "straw", "infusion"])
def _(S):
    if S.name == "line":
        bowl = poly([(5, 10), (19, 10), (17.5, 17), (13.5, 21), (10.5, 21), (6.5, 17)], closed=True)
        heap = poly([(6.5, 10), (8.5, 7), (15.5, 7), (17.5, 10)], closed=True)
    else:
        bowl = "M5 10H19C19 15.5 16 20.5 12 20.5C8 20.5 5 15.5 5 10Z"
        heap = "M6.5 10A5.5 3.5 0 0 1 17.5 10Z"
    return [shell(union(bowl, heap)), detail(seg(5.5, 10, 18.5, 10)), detail(seg(11, 12, 17, 3.5)),
            solid(rot(ellipse(17.6, 3.2, 1.2, 2), 35, 17.6, 3.2))]


@icon("tea-cozy", CAT, "Knitted dome cover over a teapot with a pompom on top, spout and handle showing",
      tags=["tea cosy", "knitted", "teapot cover", "warmer", "wool", "cozy", "afternoon tea"],
      aliases=["tea-cosy"])
def _(S):
    if S.name == "line":
        dome = poly([(5, 20), (5, 12), (8, 7.5), (16, 7.5), (19, 12), (19, 20)], closed=True)
    else:
        dome = "M5 20C5 11 8 7.5 12 7.5C16 7.5 19 11 19 20Z"
    return [shell(dome), detail(seg(5.5, 16.5, 18.5, 16.5)), solid(circle(12, 4.6, 2)),
            line(poly([(5, 14.5), (3.3, 14.5), (3.3, 11)], r=S.r)), line(poly([(19, 11), (20.7, 11), (20.7, 15.5), (19, 15.5)], r=S.r))]


@icon("tea-tin", CAT, "Cylindrical tin with a fitted lid and a leaf on the label",
      tags=["tea caddy", "canister", "loose leaf storage", "tea", "pantry", "gift tin", "container"])
def _(S):
    body = rect(5, 7.5, 14, 13.5, rr(S, 4))
    lid = rect(4.5, 3.5, 15, 4.5, rr(S, 3))
    leaf = "M12 18.5C8 17.5 8 13 10 11C14 11.5 16 15 12 18.5Z"
    return [shell(union(body, lid)), detail(seg(5, 8, 19, 8)), hole(leaf)]


@icon("kyusu", CAT, "Round Japanese teapot with a short spout and a straight handle sticking out to the side",
      tags=["japanese teapot", "side handle", "sencha", "green tea", "yokode", "tea ceremony", "teapot"])
def _(S):
    body = circle(11, 14, 6.6) if S.name == "rounded" else poly(regular(11, 14, 7, 10, -90), closed=True)
    grip = rect(17.3, 12.3, 4.7, 3.2, rr(S, 1.6))
    return [shell(body), shell(grip), solid(circle(11, 6.4, 1.4)), line("M4.6 13C3 12.6 2.6 10.8 3 9")]


@icon("cast-iron-teapot", CAT, "Squat teapot with a bumpy dotted surface and an arched handle over the top",
      tags=["tetsubin", "iron kettle", "japanese teapot", "heavy", "tea", "studded", "arare"])
def _(S):
    if S.name == "line":
        body = poly([(4, 12), (6.5, 9), (17.5, 9), (20, 12), (18, 19.5), (6, 19.5)], closed=True)
    else:
        body = "M4 13C4 9.5 8 9 12 9C16 9 20 9.5 20 13C20 18 17 20.5 12 20.5C7 20.5 4 18 4 13Z"
    return [shell(body), line("M7.5 9.5C7.5 3 16.5 3 16.5 9.5"), line("M4.3 14.2C2.6 14 2.2 12 2.6 10"),
            hole(circle(8.5, 13.5, 0.9)), hole(circle(12, 12.6, 0.9)), hole(circle(15.5, 13.5, 0.9)),
            hole(circle(10.2, 16.8, 0.9)), hole(circle(13.8, 16.8, 0.9))]


@icon("moroccan-teapot", CAT, "Tall metal teapot with a domed pointed lid, a long curved spout and a side handle",
      tags=["moroccan tea", "mint tea", "silver teapot", "north african", "hospitality", "tall spout", "pot"])
def _(S):
    body = poly([(8, 10), (16, 10), (18, 20.5), (6, 20.5)], closed=True, r=S.r)
    lid = poly([(8.3, 10), (9.5, 6.5), (12, 4), (14.5, 6.5), (15.7, 10)], closed=True, r=S.r)
    handle = poly([(16.7, 11.5), (20.5, 11.5), (20.5, 18), (17.6, 18)], r=S.r)
    return [shell(union(body, lid)), line(handle), solid(circle(12, 2.6, 1.3)), detail(seg(7.2, 14.5, 16.8, 14.5)),
            line("M6.6 18C2.5 16 5.5 9 3 5.5")]


@icon("blooming-tea", CAT, "Round glass teapot with an open flower suspended in the water",
      tags=["flowering tea", "tea flower", "glass teapot", "display tea", "petals", "brew", "tea art"])
def _(S):
    body = circle(11, 14, 6.6) if S.name == "rounded" else poly(regular(11, 14, 7, 10, -90), closed=True)
    petal = "M11 18.6C8.6 16.3 8.6 13 11 10.6C13.4 13 13.4 16.3 11 18.6Z"
    handle = poly([(17.2, 10.5), (21, 10.5), (21, 17), (16.8, 17)], r=S.r)
    return [shell(union(body, rect(8.5, 6, 5, 2, 0))), line(handle), solid(circle(11, 4.4, 1.4)), line(seg(5, 13.5, 2.6, 10.3)),
            hole(petal), hole(rot(petal, 50, 11, 18.6)), hole(rot(petal, -50, 11, 18.6))]


@icon("mulled-wine", CAT, "Glass mug of dark wine with an orange slice on the rim and a star anise above",
      tags=["glogg", "gluhwein", "hot wine", "winter drink", "christmas market", "spices", "orange slice"])
def _(S):
    mug = poly([(3.5, 7), (16, 7), (14.8, 20.5), (4.7, 20.5)], closed=True, r=S.r)
    star = [pt_on(8, 3.3, 2.4 if i % 2 == 0 else 1.0, -90 + i * 45) for i in range(16 // 2)]
    star = [pt_on(8, 3.6, 2.4 if i % 2 == 0 else 1.0, -90 + i * 22.5) for i in range(16)]
    handle = poly([(15.6, 10), (20.5, 10), (20.5, 17), (15, 17)], r=S.r)
    return [shell(union(mug, circle(14.5, 6.6, 2.8))), line(handle), detail(seg(4.2, 11.5, 15.3, 11.5)),
            solid(poly(star, closed=True))]


@icon("thermos", CAT, "Tall vacuum flask with a cup lid on top and a band around the body",
      tags=["vacuum flask", "insulated bottle", "hot drink", "camping", "picnic", "lunch", "travel"])
def _(S):
    body = rect(7, 10, 10, 11, rr(S, 3))
    cup = rect(7, 3, 10, 7.5, rr(S, 2.5))
    return [shell(union(body, cup)), detail(seg(7.5, 10.3, 16.5, 10.3)), detail(seg(7.5, 17, 16.5, 17)),
            line(poly([(17, 5), (20.5, 5), (20.5, 8.5), (17, 8.5)], r=S.r))]


@icon("travel-mug", CAT, "Tall tapered insulated mug with a sip lid and a side handle",
      tags=["tumbler", "commuter mug", "insulated", "reusable cup", "coffee", "lid", "to go"])
def _(S):
    cup = poly([(5.5, 7.5), (16.5, 7.5), (15, 21), (7, 21)], closed=True, r=S.r)
    lid = rect(5, 4.5, 12, 3, rr(S, 1.5))
    tab = rect(8.5, 2.5, 5, 2, rr(S, 1))
    handle = poly([(16.2, 10.5), (20.5, 10.5), (20.5, 17), (15.6, 17)], r=S.r)
    return [shell(union(cup, lid, tab)), line(handle), detail(seg(5.6, 8, 16.4, 8)), detail(seg(6.2, 13, 15.8, 13))]


@icon("camping-mug", CAT, "Enamel mug with a rolled rim, straight sides and a couple of chipped spots",
      tags=["enamel mug", "tin cup", "outdoor", "campfire", "hiking", "picnic", "metal mug"])
def _(S):
    handle = poly([(16.5, 8.5), (20.5, 8.5), (20.5, 16.5), (16.5, 16.5)], r=S.r)
    return [shell(rect(4, 5, 12.5, 15, rr(S, 2))), line(handle), detail(seg(4.5, 8, 16, 8)),
            hole(circle(8, 14, 1)), hole(circle(12, 17, 0.9))]


@icon("paper-cup", CAT, "Plain tapered paper cup with a rolled rim and no lid",
      tags=["disposable cup", "water cup", "party cup", "cooler", "drink", "single use", "cup"])
def _(S):
    cup = poly([(5.5, 5.5), (18.5, 5.5), (16.5, 21), (7.5, 21)], closed=True, r=S.r)
    rim = rect(4.5, 3.5, 15, 2.5, rr(S, 1.2))
    return [shell(union(cup, rim)), detail(seg(5, 6, 19, 6))]


@icon("sippy-cup", CAT, "Child cup with two side handles and a spouted lid",
      tags=["toddler cup", "kids cup", "training cup", "spout cup", "baby", "childcare", "feeding"])
def _(S):
    body = rect(6, 9.5, 12, 11.5, rr(S, 3))
    lid = rect(5.5, 7, 13, 3, rr(S, 1.5))
    spout = poly([(9, 7.3), (10, 3.5), (14, 3.5), (15, 7.3)], closed=True, r=S.r * 0.7)
    h = poly([(6, 12.5), (3, 12.5), (3, 17), (6, 17)], r=S.r)
    return [shell(union(body, lid, spout)), detail(seg(6.3, 10, 17.7, 10)), line(h), line(flip(h))]


@icon("baby-bottle", CAT, "Feeding bottle with measuring lines, a screw collar and a rounded nipple",
      tags=["feeding bottle", "infant", "formula", "milk", "newborn", "nursing", "nipple"])
def _(S):
    body = rect(6.5, 9.5, 11, 11.5, rr(S, 3))
    collar = rect(6, 7, 12, 3, rr(S, 1.2))
    nipple = poly([(9.8, 7), (10, 4.3), (12, 2.6), (14, 4.3), (14.2, 7)], closed=True, r=S.r)
    return [shell(union(body, collar, nipple)), detail(seg(6.8, 10, 17.2, 10)), detail(seg(7, 14, 10.8, 14)),
            detail(seg(7, 17.5, 10.8, 17.5))]


@icon("milkshake", CAT, "Tall soda glass topped with whipped cream, a cherry and a straw",
      tags=["shake", "soda fountain", "diner", "whipped cream", "dessert drink", "cherry", "straw"])
def _(S):
    glass_ = poly([(6, 8.5), (18, 8.5), (15.3, 18.5), (8.7, 18.5)], closed=True, r=S.r)
    cream = "M6 8.5A6 5 0 0 1 18 8.5Z"
    return [shell(union(glass_, cream)), detail(seg(6.5, 8.5, 17.5, 8.5)), detail(seg(14, 14, 18, 2.5)),
            solid(circle(10.8, 3.2, 1.6)), line(seg(12, 18.5, 12, 21)), line(seg(8.5, 21, 15.5, 21))]


@icon("hot-chocolate", CAT, "Mug topped with a heap of marshmallows and two steam curls",
      tags=["cocoa", "marshmallow", "winter drink", "cozy", "warm drink", "mug", "steam"])
def _(S):
    mug = rect(4.5, 10.5, 12, 10.5, rr(S, 3))
    m1 = rect(5.5, 7.3, 4.6, 3.6, rr(S, 1.4))
    m2 = rect(10.6, 6.8, 4.6, 4.1, rr(S, 1.4))
    handle = poly([(16.3, 12.5), (20.5, 12.5), (20.5, 18), (16, 18)], r=S.r)
    return [shell(union(mug, m1, m2)), line(handle), detail(seg(5, 10.8, 16, 10.8)),
            line("M8.5 4.5C7 3.5 9.5 2.8 8 1.8"), line("M13.5 4.5C12 3.5 14.5 2.8 13 1.8")]


@icon("drink-vending-machine", CAT, "Tall vending machine with a window of bottles, a coin slot and a pickup flap",
      tags=["soda machine", "beverage dispenser", "vending", "bottles", "coin slot", "convenience", "kiosk"])
def _(S):
    return [shell(rect(4, 2.5, 16, 19, rr(S, 2.5))), detail(rect(6.5, 5, 7.5, 9.5, 0)),
            hole(circle(9, 8, 1)), hole(circle(11.6, 8, 1)), hole(circle(9, 11.4, 1)), hole(circle(11.6, 11.4, 1)),
            hole(rect(16, 6, 1.6, 3.2, 0)), detail(rect(6.5, 16.8, 7.5, 2.4, 0))]


@icon("citrus-juicer", CAT, "Ribbed dome reamer sitting in a shallow dish with a pouring lip",
      tags=["lemon squeezer", "reamer", "orange juice", "fresh juice", "kitchen tool", "squeeze", "citrus"])
def _(S):
    dish = poly([(2, 15), (22, 15), (18.5, 21), (5.5, 21)], closed=True, r=S.r)
    dome = "M6 15A6 7.5 0 0 1 18 15Z"
    return [shell(union(dish, dome)), detail(seg(2.6, 15, 21.4, 15)), detail(seg(12, 10, 12, 14)),
            detail(seg(8.6, 12, 8.6, 14)), detail(seg(15.4, 12, 15.4, 14))]


@icon("slushie", CAT, "Clear cup with a mound of crushed ice on top and a spoon straw",
      tags=["slush", "frozen drink", "shaved ice", "summer", "crushed ice", "cold drink"])
def _(S):
    cup = poly([(5.5, 10), (18.5, 10), (17, 21), (7, 21)], closed=True, r=S.r)
    mound = poly([(5, 10), (5.6, 7.3), (8.5, 6), (10.5, 4), (13.5, 5.3), (16.3, 6), (18.6, 7.6), (19, 10)], closed=True, r=S.r)
    return [shell(union(cup, mound)), detail(seg(5.6, 10, 18.4, 10)), detail(seg(13, 15, 16, 4)),
            solid(rot(ellipse(16.6, 3.4, 1.3, 2.2), 20, 16.6, 3.4)), hole(circle(9, 14.5, 0.9)), hole(circle(11.5, 18, 0.9)),
            hole(circle(9, 18.3, 0.8))]
