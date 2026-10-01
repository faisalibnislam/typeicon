"""TypeIcon Core: household (batch household_001): bathroom fixtures, washing, cleaning tools.

Original drawings of generic bathroom and cleaning objects from the front or side. Bodies are shells,
inner marks are details (knocked out in Filled), small fittings are dots.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
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


# ============================================================================ toilet

@icon("toilet-paper", CAT, "Toilet paper roll seen from the front with a hollow core and a loose sheet hanging down",
      tags=["toilet roll", "bathroom tissue", "loo roll", "restroom", "wc", "paper"])
def _(S):
    return [
        shell(circle(11, 10, 7)),
        detail(circle(11, 10, 2.25)),
        line(poly([(17.5, 12.8), (17.5, 21.5), (13.5, 21.5), (13.5, 16.5)], r=S.r)),
    ]


@icon("toilet-paper-holder", CAT, "Wall holder with a toilet roll on a bar and a short tail of paper hanging below",
      tags=["toilet roll holder", "tissue holder", "bathroom", "restroom", "wall mount", "bracket"])
def _(S):
    return [
        line(seg(3.5, 4, 3.5, 15)),
        line(seg(20.5, 4, 20.5, 15)),
        shell(rect(7, 5, 10, 10, rr(S, 2))),
        detail(seg(10, 10, 14, 10)),
        line("M12.5 15V21.5H17.5V15"),
    ]


@icon("toilet-paper-pack", CAT, "Plastic-wrapped pack of four toilet rolls in a square, two by two",
      tags=["toilet roll pack", "multipack", "bulk buy", "bathroom tissue", "supplies", "four pack"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 18, rr(S, 3))),
        detail(circle(8, 8.5, 2.25)), detail(circle(16, 8.5, 2.25)),
        detail(circle(8, 15.5, 2.25)), detail(circle(16, 15.5, 2.25)),
    ]


@icon("toilet-brush", CAT, "Toilet brush with a round bristle head standing in its cylindrical holder",
      tags=["toilet cleaning", "loo brush", "bathroom cleaning", "scrub", "bowl brush", "cleaner"])
def _(S):
    return [
        shell(ellipse(12, 6.5, 5, 4.5)),
        dot(10, 6.5, 1), dot(14, 6.5, 1), dot(12, 4.5, 1),
        line(seg(12, 11, 12, 15)),
        shell(rect(6.5, 14.5, 11, 7, rr(S, 2.5))),
    ]


@icon("plunger", CAT, "Plunger with a straight handle and a dome-shaped rubber cup at the bottom",
      tags=["unblock", "clogged drain", "blocked toilet", "plumbing", "sink", "drain cleaner"])
def _(S):
    cup = poly([(4.5, 21.5), (7, 15), (12, 12.5), (17, 15), (19.5, 21.5)], closed=True, r=S.r * 1.6)
    if S.name == "line":
        cup = "M4.5 21.5L7 15Q12 11 17 15L19.5 21.5Z"
    return [
        line(seg(12, 2.5, 12, 12)),
        shell(cup),
    ]


@icon("bidet", CAT, "Side view of a low floor-mounted bowl with a small tap on its back rim",
      tags=["bathroom fixture", "hygiene", "washing", "bowl", "toilet", "wash basin"])
def _(S):
    body = poly([(3, 9.5), (19.5, 9.5), (19.5, 12.5), (16, 16), (16, 21.5), (8, 21.5), (8, 16), (4.5, 13)], closed=True, r=S.r)
    return [
        shell(body),
        line(poly([(17, 9), (17, 5), (13.5, 5), (13.5, 6.5)], r=S.r)),
    ]


@icon("urinal", CAT, "Wall-mounted urinal, a tall rounded bowl open at the front with a flush pipe above",
      tags=["men's room", "restroom", "public toilet", "washroom", "bowl", "wall mounted"])
def _(S):
    bowl = poly([(6, 6.5), (18, 6.5), (18, 14), (15, 20), (9, 20), (6, 14)], closed=True, r=S.r + 1)
    return [
        line(seg(12, 2.5, 12, 6.5)),
        shell(bowl),
        detail(seg(9, 11, 15, 11)),
        dot(12, 16, 1.1),
    ]


@icon("squat-toilet", CAT, "Top view of a floor-level oval pan with two footrests on either side",
      tags=["squat pan", "asian toilet", "floor toilet", "eastern toilet", "public toilet", "hole"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, rr(S, 4))),
        detail(ellipse(12, 15, 3, 4)),
        sq(6, 5.5, 3.5, 5, L(S, 0, 1)),
        sq(14.5, 5.5, 3.5, 5, L(S, 0, 1)),
    ]


@icon("child-potty", CAT, "Small plastic potty chair seen from the side with a curved backrest and a round seat",
      tags=["potty training", "baby potty", "toddler toilet", "nappy", "diaper", "kids bathroom"])
def _(S):
    body = poly([(4, 3), (9, 3), (9, 9), (20, 9), (20, 16), (17, 21.5), (7, 21.5), (4, 16)], closed=True, r=S.r)
    return [
        shell(body),
        detail(seg(8, 14, 16, 14)),
    ]


@icon("toilet-seat", CAT, "Front view of an open toilet seat ring with the lid raised behind it",
      tags=["toilet lid", "toilet ring", "loo seat", "bathroom", "wc", "restroom"])
def _(S):
    lid = "M6.5 10V6Q6.5 2.5 12 2.5Q17.5 2.5 17.5 6V10" if S.name == "rounded" else "M6.5 10V5L9 2.5H15L17.5 5V10"
    return [
        line(lid),
        shell(ellipse(12, 16, 9, 5.5)),
        detail(ellipse(12, 16, 4, 2)),
    ]


@icon("dual-flush-button", CAT, "Rectangular wall plate holding two buttons, one small and one large, side by side",
      tags=["flush plate", "toilet flush", "water saving", "cistern button", "push plate", "eco flush"])
def _(S):
    return [
        shell(rect(2.5, 4, 19, 16, rr(S, 3))),
        dot(8, 12, 2),
        detail(rect(12.5, 8, 5.5, 8, L(S, 0, 1.5))),
    ]


@icon("pull-chain-toilet", CAT, "Toilet bowl below a high wall cistern with a hanging chain and a handle at its end",
      tags=["high level cistern", "old toilet", "victorian toilet", "chain flush", "vintage", "loo"])
def _(S):
    return [
        shell(rect(9, 2.5, 11, 5, rr(S, 2))),
        line("M9 5H4.5V12"),
        dot(4.5, 13.5, 1.3),
        line(seg(14.5, 7.5, 14.5, 13.5)),
        shell(poly([(8, 13.5), (20, 13.5), (19, 17.5), (16, 19.5), (16, 21.5), (11, 21.5), (11, 19.5)], closed=True, r=S.r)),
    ]


@icon("toilet-cistern", CAT, "Toilet tank viewed from the front with the lid lifted and a float valve inside",
      tags=["toilet tank", "water tank", "flush tank", "float valve", "ballcock", "plumbing"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 3.5, rr(S, 1.5))),
        shell(rect(4, 9.5, 16, 12, rr(S, 2.5))),
        detail(seg(8, 14, 13, 14)),
        dot(16, 15.5, 2),
    ]


@icon("bidet-sprayer", CAT, "Handheld bidet spray nozzle with a trigger, joined to a hose and a wall valve",
      tags=["bum gun", "shattaf", "hygiene shower", "handheld bidet", "toilet sprayer", "muslim shower"])
def _(S):
    nozzle = poly([(13, 2.5), (19, 2.5), (19, 7), (17.5, 9), (17.5, 14.5), (14.5, 14.5), (14.5, 9), (13, 7)], closed=True, r=S.r)
    return [
        shell(nozzle),
        line(seg(14.5, 11, 11.5, 11)),
        line("M16 14.5V18Q16 21 12.5 21H7"),
        shell(rect(2.5, 17, 4.5, 4.5, rr(S, 1.5))),
    ]


@icon("portable-toilet", CAT, "Tall portable toilet cabin with a roof vent, a door and a small handle",
      tags=["porta potty", "portaloo", "event toilet", "construction site", "festival", "outdoor toilet"])
def _(S):
    return [
        line(seg(9, 3, 15, 3)),
        shell(rect(5.5, 6, 13, 15.5, rr(S, 2))),
        detail("M9 21.5V10H15V21.5"),
        dot(13, 15.5, 1.1),
    ]


def wave(x, y0, y1, amp=1.2):
    """Gentle vertical wave from y0 up to y1 (one S bend)."""
    h = y0 - y1
    return f"M{fmt(x)} {fmt(y0)}C{fmt(x - amp)} {fmt(y0 - h * 0.35)} {fmt(x + amp)} {fmt(y1 + h * 0.35)} {fmt(x)} {fmt(y1)}"


@icon("chamber-pot", CAT, "Short round pot with a flared rim and a loop handle on one side",
      tags=["potty", "commode", "night pot", "bed pan", "old toilet", "enamel pot"])
def _(S):
    body = poly([(2.5, 7), (18.5, 7), (18.5, 10), (17.5, 10), (17.5, 15), (15, 19.5), (6, 19.5), (3.5, 15), (3.5, 10), (2.5, 10)], closed=True, r=S.r)
    return [
        shell(body),
        line("M17.5 12H19.5Q21.5 12 21.5 14.5Q21.5 17 17 17"),
    ]


@icon("handheld-shower", CAT, "Shower handset with a round spray face and a hose curving down from its handle",
      tags=["shower head", "hand shower", "spray", "bathroom", "hose", "rinse"])
def _(S):
    return [
        shell(circle(12, 7, 5)),
        dot(10, 6, 1), dot(14, 6, 1), dot(12, 8.5, 1),
        shell(rect(10.5, 11.5, 3, 6, rr(S, 1.5))),
        line("M12 17.5V19Q12 21.5 15 21.5H21.5"),
    ]


@icon("shower-curtain", CAT, "Shower curtain hanging in folds from a straight rod, drawn half open",
      tags=["bath curtain", "bathroom", "privacy screen", "shower", "rod", "rings"])
def _(S):
    curtain = "M4.5 6.5H17.5L16 19.5Q14 21.5 12 19.5T8 19.5T4.5 19.5Z"
    return [
        line(seg(2.5, 3.5, 21.5, 3.5)),
        shell(curtain),
        detail(seg(8, 10, 8, 16)),
        detail(seg(12, 10, 12, 16)),
    ]


@icon("shower-enclosure", CAT, "Glass shower cubicle seen from the front with a shower head and falling drops inside",
      tags=["shower cubicle", "shower cabin", "shower stall", "glass screen", "bathroom", "walk-in"])
def _(S):
    head = poly([(8.5, 10), (10.5, 6.5), (13.5, 6.5), (15.5, 10)], closed=True, r=L(S, 0, 0.6))
    return [
        shell(rect(3.5, 2.5, 17, 19, S.R)),
        detail(seg(12, 2.5, 12, 6.5)),
        mark(head),
        dot(9, 14, 0.9), dot(12, 16, 0.9), dot(15, 14, 0.9),
        dot(13.5, 18.5, 0.9),
    ]


@icon("shower-caddy", CAT, "Wire caddy hooked over a shower pipe holding two bottles on stacked baskets",
      tags=["bath organiser", "shampoo holder", "shower shelf", "bathroom storage", "hanging basket", "toiletries"])
def _(S):
    return [
        line(seg(3, 2.5, 3, 21.5)),
        line(seg(3, 6, 7.5, 6)),
        line(seg(3, 17, 7.5, 17)),
        shell(rect(7.5, 3.5, 14, 17, rr(S, 2))),
        detail(seg(7.5, 12.5, 21.5, 12.5)),
        sq(10.5, 6, 3, 4, L(S, 0, 1)),
        sq(15.5, 5, 3, 5, L(S, 0, 1)),
    ]


@icon("shower-drain", CAT, "Square floor grate with a slotted pattern and water drops falling onto it",
      tags=["floor grate", "wet room drain", "bathroom floor", "water outlet", "linear drain", "grate"])
def _(S):
    return [
        shell(rect(3.5, 10, 17, 11.5, rr(S, 2))),
        detail(seg(7, 14, 17, 14)),
        detail(seg(7, 17.5, 17, 17.5)),
        dot(8, 4.5, 1.4), dot(12, 6.5, 1.4), dot(16, 4.5, 1.4),
    ]


@icon("floor-drain", CAT, "Round floor drain cover with three rows of vertical slots",
      tags=["drain cover", "sewer grate", "round drain", "basement drain", "garage drain", "gully"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(seg(8, 8.5, 8, 15.5)),
        detail(seg(12, 7, 12, 17)),
        detail(seg(16, 8.5, 16, 15.5)),
    ]


@icon("drain-strainer", CAT, "Round mesh basket strainer seated in a drain hole, seen from above",
      tags=["sink strainer", "hair catcher", "drain filter", "plughole", "sink basket", "waste trap"])
def _(S):
    outer = poly(regular(12, 12, 9.6, 8, start=-67.5), closed=True) if S.name == "line" else circle(12, 12, 9)
    return [
        shell(outer),
        detail(circle(12, 12, 4.5)),
        dot(12, 12, 1.25),
    ]


@icon("shower-chair", CAT, "Short four-legged stool with a flat seat and grab arms on each side",
      tags=["bath seat", "shower stool", "accessible bathroom", "elderly care", "disability aid", "bathing"])
def _(S):
    return [
        line(poly([(4, 4.5), (8, 4.5), (8, 9.5)], r=S.r)),
        line(poly([(20, 4.5), (16, 4.5), (16, 9.5)], r=S.r)),
        shell(rect(3.5, 9.5, 17, 4, rr(S, 1.5))),
        line(seg(7, 13.5, 6, 21.5)),
        line(seg(17, 13.5, 18, 21.5)),
    ]


@icon("shower-mixer", CAT, "Round mixer valve with a lever and hot and cold marks on each side",
      tags=["shower valve", "thermostatic mixer", "temperature control", "tap", "hot cold", "bathroom"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(seg(12, 12, 12, 6)),
        dot(12, 12, 2.25),
        dot(6.5, 16, 1.1), dot(17.5, 16, 1.1),
    ]


@icon("bath-plug", CAT, "Round rubber sink plug with a small ring and chain attached to its top",
      tags=["sink plug", "drain stopper", "bath stopper", "plughole", "chain", "rubber plug"])
def _(S):
    plug = poly([(4, 11), (20, 11), (18, 14), (15.5, 20.5), (8.5, 20.5), (6, 14)], closed=True, r=S.r)
    return [
        shell(circle(11, 5.5, 2.5)),
        line("M13.5 5.5H18Q21 5.5 21 8.5"),
        shell(plug),
    ]


@icon("bath-mat", CAT, "Rectangular bath mat with a border pattern and a fringe of short tassels on both ends",
      tags=["bathroom rug", "floor mat", "bath rug", "towel mat", "shower mat", "fringe"])
def _(S):
    return [
        line(seg(2.5, 10, 5, 10)), line(seg(2.5, 14, 5, 14)),
        line(seg(19, 10, 21.5, 10)), line(seg(19, 14, 21.5, 14)),
        shell(rect(5, 6.5, 14, 11, rr(S, 3))),
        detail(seg(8.5, 12, 15.5, 12)),
    ]


@icon("clawfoot-tub", CAT, "Freestanding roll-top bathtub raised on four curved claw feet",
      tags=["freestanding bath", "roll top bath", "vintage bathtub", "slipper tub", "luxury bathroom", "soak"])
def _(S):
    body = poly([(3.5, 10.5), (20.5, 10.5), (19.5, 14), (16.5, 17.5), (7.5, 17.5), (4.5, 14)], closed=True, r=S.r)
    return [
        line(poly([(18, 6.5), (18, 3.5), (14.5, 3.5)], r=S.r)),
        line(seg(2.5, 7.5, 21.5, 7.5)),
        shell(body),
        line("M7.5 17.5V19Q7.5 20.5 5.5 20.5"),
        line("M16.5 17.5V19Q16.5 20.5 18.5 20.5"),
    ]


@icon("hot-tub", CAT, "Round wooden tub with a metal band and rising steam lines",
      tags=["spa", "jacuzzi", "whirlpool", "barrel tub", "soak", "outdoor bath", "relax"])
def _(S):
    tub = poly([(3, 10.5), (21, 10.5), (19.5, 21.5), (4.5, 21.5)], closed=True, r=S.r)
    return [
        line(wave(8, 8, 3)), line(wave(12, 8, 3)), line(wave(16, 8, 3)),
        shell(tub),
        detail(seg(3.5, 15, 20.5, 15)),
    ]


@icon("baby-bathtub", CAT, "Small oval baby bath with a rubber duck floating above its water",
      tags=["infant bath", "newborn", "baby wash", "nursery", "bath time", "duck"])
def _(S):
    tub = poly([(2.5, 11.5), (21.5, 11.5), (19, 19), (16.5, 21.5), (7.5, 21.5), (5, 19)], closed=True, r=S.r)
    return [
        shell(tub),
        solid(ellipse(10, 8, 3.25, 2.25)),
        dot(13.5, 5.5, 1.75),
    ]


# ============================================================================ bath and basin

@icon("bubble-bath", CAT, "Bathtub overflowing with a mound of round foam bubbles above the rim",
      tags=["foam bath", "bubbles", "relaxing bath", "spa", "soak", "bathtub"])
def _(S):
    tub = poly([(3, 14.5), (21, 14.5), (19.5, 19), (17, 21.5), (7, 21.5), (4.5, 19)], closed=True, r=S.r)
    return [
        shell(circle(8, 10.5, 3.25)),
        shell(circle(14.5, 9, 3.75)),
        dot(19.5, 11, 1.4), dot(11.5, 4.5, 1.3),
        shell(tub),
    ]


@icon("bath-thermometer", CAT, "Floating bath thermometer shaped like a small fish with a scale on its side",
      tags=["baby bath", "water temperature", "fish thermometer", "nursery", "safe bath", "bath toy"])
def _(S):
    return [
        shell(ellipse(10.5, 12, 7.5, 5.5)),
        line(poly([(17.8, 9.2), (21.5, 7), (21.5, 17), (17.8, 14.8)], r=S.r)),
        dot(6.5, 10.5, 1.1),
        detail(seg(10, 10.5, 10, 14)),
        detail(seg(14, 10.5, 14, 14)),
    ]


@icon("medicine-cabinet", CAT, "Wall-mounted bathroom cabinet with its mirrored door swung open to show a shelf of bottles",
      tags=["bathroom cabinet", "first aid cabinet", "mirror cabinet", "pharmacy", "storage", "bottles"])
def _(S):
    return [
        shell(rect(8.5, 3.5, 12.5, 17, rr(S, 2))),
        line(poly([(8.5, 3.5), (3, 5.5), (3, 18.5), (8.5, 20.5)], r=S.r)),
        detail(seg(8.5, 12.5, 21, 12.5)),
        sq(11.5, 6.5, 3, 4, L(S, 0, 1)), sq(16.5, 5.5, 2.5, 5, L(S, 0, 1)),
        sq(11.5, 15, 3.5, 3.5, L(S, 0, 1)),
    ]


@icon("vanity-unit", CAT, "Bathroom vanity: a basin with a tap set on a cabinet with two doors",
      tags=["bathroom cabinet", "sink cabinet", "washstand", "basin unit", "bathroom furniture", "tap"])
def _(S):
    return [
        line(poly([(12, 6.5), (12, 3), (15, 3)], r=S.r)),
        line(poly([(7, 10), (8, 6.5), (16, 6.5), (17, 10)], r=S.r)),
        shell(rect(3, 10, 18, 11.5, rr(S, 2.5))),
        detail(seg(3, 13.5, 21, 13.5)),
        detail(seg(12, 13.5, 12, 21.5)),
        dot(9.5, 17.5, 1), dot(14.5, 17.5, 1),
    ]


@icon("pedestal-sink", CAT, "Freestanding washbasin on a single column pedestal with a tap on the back",
      tags=["washbasin", "bathroom sink", "basin", "cloakroom", "column basin", "lavatory"])
def _(S):
    body = poly([(3, 7), (21, 7), (20, 10.5), (16, 13), (14.5, 13), (14.5, 18), (17, 21.5), (7, 21.5), (9.5, 18), (9.5, 13), (8, 13), (4, 10.5)], closed=True, r=S.r)
    return [
        line(poly([(12, 6.5), (12, 3), (15.5, 3)], r=S.r)),
        shell(body),
    ]


@icon("vessel-sink", CAT, "Round bowl basin sitting on top of a counter with a tall tap beside it",
      tags=["countertop basin", "bowl sink", "bathroom counter", "washbasin", "designer sink", "tap"])
def _(S):
    bowl = poly([(3.5, 8), (16.5, 8), (15.5, 11.5), (13, 14.5), (7, 14.5), (4.5, 11.5)], closed=True, r=S.r)
    return [
        line(poly([(20.5, 14.5), (20.5, 3.5), (14.5, 3.5), (14.5, 5.5)], r=S.r)),
        shell(bowl),
        shell(rect(2.5, 14.5, 19, 5.5, rr(S, 1.5))),
    ]


@icon("towel-stack", CAT, "Three folded towels stacked on top of each other with staggered ends",
      tags=["folded towels", "linen", "bath towels", "spa", "laundry", "hotel"])
def _(S):
    body = poly([(5, 4), (18, 4), (18, 8.5), (21, 8.5), (21, 14.5), (20, 14.5), (20, 20), (4, 20), (4, 14.5), (3, 14.5), (3, 8.5), (5, 8.5)], closed=True, r=S.r)
    return [
        shell(body),
        detail(seg(4, 8.5, 20, 8.5)),
        detail(seg(4, 14.5, 20, 14.5)),
    ]


@icon("heated-towel-rail", CAT, "Ladder-style radiator with several horizontal bars and a towel draped over the top rung",
      tags=["towel warmer", "bathroom radiator", "towel radiator", "heating", "drying", "rail"])
def _(S):
    return [
        line(seg(4.5, 2.5, 4.5, 21.5)),
        line(seg(19.5, 2.5, 19.5, 21.5)),
        line(seg(4.5, 5, 8.5, 5)), line(seg(15.5, 5, 19.5, 5)),
        line(seg(4.5, 10, 8.5, 10)), line(seg(15.5, 10, 19.5, 10)),
        line(seg(4.5, 15.5, 19.5, 15.5)),
        line(seg(4.5, 20.5, 19.5, 20.5)),
        shell(rect(8.5, 2.5, 7, 10.5, rr(S, 1.5))),
    ]


@icon("towel-ring", CAT, "Round towel ring on the wall with a hand towel pulled through it",
      tags=["towel holder", "hand towel", "bathroom", "wall ring", "kitchen towel", "hanger"])
def _(S):
    return [
        line(arc(12, 9, 6.5, 122.5, 417.5)),
        shell(rect(8.5, 7.5, 7, 13.5, L(S, 0, 2.5))),
    ]


@icon("robe-hook", CAT, "Wall hook plate with a bathrobe hanging from it by its loop",
      tags=["bathrobe", "dressing gown", "door hook", "bathroom", "spa robe", "hanger"])
def _(S):
    robe = poly([(9, 8.5), (15, 8.5), (19, 11), (19, 21.5), (5, 21.5), (5, 11)], closed=True, r=S.r)
    return [
        shell(rect(5, 2.5, 14, 3, rr(S, 1.5))),
        line(seg(12, 5.5, 12, 8.5)),
        shell(robe),
        detail(poly([(9.5, 9), (12, 14), (14.5, 9)])),
        detail(seg(5, 17.5, 19, 17.5)),
    ]


@icon("grab-bar", CAT, "Horizontal bathroom wall grab rail with mounting flanges at each end",
      tags=["safety rail", "handrail", "accessible bathroom", "support bar", "disability aid", "elderly care"])
def _(S):
    return [
        line(seg(3.5, 7, 3.5, 17)),
        line(seg(20.5, 7, 20.5, 17)),
        shell(rect(4.5, 10, 15, 4, rr(S, 2))),
    ]


@icon("soap-dish", CAT, "Shallow dish with ribs holding a bar of soap",
      tags=["soap holder", "soap tray", "bathroom", "sink accessory", "washing", "hygiene"])
def _(S):
    dish = poly([(2.5, 14.5), (21.5, 14.5), (19, 20), (5, 20)], closed=True, r=S.r)
    return [
        shell(rect(6.5, 7, 11, 7.5, rr(S, 3))),
        shell(dish),
        dot(9, 17.25, 0.9), dot(12, 17.25, 0.9), dot(15, 17.25, 0.9),
    ]


@icon("soap-bar", CAT, "Rounded bar of soap with a small cluster of bubbles on one corner",
      tags=["hand soap", "bar soap", "wash", "hygiene", "clean", "bathroom"])
def _(S):
    return [
        shell(circle(18, 6.5, 2.75)),
        dot(21.5, 11, 1.2), dot(12, 4.5, 1.3),
        shell(rect(2.5, 9, 15, 11.5, rr(S, 4.5))),
        detail(seg(6.5, 14.75, 13.5, 14.75)),
    ]


@icon("soap-dispenser", CAT, "Liquid soap pump bottle with a downward spout and bubbles beside it",
      tags=["liquid soap", "hand wash", "pump bottle", "sanitizer", "bathroom", "kitchen sink"])
def _(S):
    return [
        line(poly([(7.5, 5.5), (14.5, 5.5), (14.5, 8.5)], r=S.r)),
        line(seg(10.5, 5.5, 10.5, 11)),
        shell(rect(5.5, 11, 10, 10.5, rr(S, 3))),
        dot(19.5, 13, 1.4), dot(18.5, 17.5, 1.1),
    ]


@icon("foam-soap-dispenser", CAT, "Soap pump bottle with a wide nozzle releasing a round blob of foam",
      tags=["foaming soap", "hand wash", "foam pump", "bathroom", "sanitizer", "bubbles"])
def _(S):
    return [
        line(poly([(6, 6), (13.5, 6)], r=S.r)),
        line(seg(9.5, 6, 9.5, 11)),
        shell(rect(4.5, 11, 10, 10.5, rr(S, 3))),
        shell(circle(17.5, 9, 3.5)),
        dot(20.5, 15, 1.2),
    ]


@icon("toothbrush-holder", CAT, "Cup-shaped holder with two toothbrushes standing in it",
      tags=["toothbrush cup", "bathroom", "dental", "brushing teeth", "tumbler", "hygiene"])
def _(S):
    cup = poly([(5.5, 12), (18.5, 12), (17, 21.5), (7, 21.5)], closed=True, r=S.r)
    return [
        line(seg(9, 12, 9, 6.5)),
        sq(7.5, 2.5, 3, 5, L(S, 0, 1)),
        line(seg(15, 12, 15, 8.5)),
        sq(13.5, 3.5, 3, 5, L(S, 0, 1)),
        shell(cup),
    ]


@icon("rubber-duck", CAT, "Side view of a bath rubber duck with a flat base, round head and small beak",
      tags=["bath toy", "duckie", "baby bath", "squeaky toy", "yellow duck", "bath time"])
def _(S):
    return [
        shell(circle(10, 8.5, 4)),
        shell(poly([(6.5, 7.5), (2.5, 9.5), (6.5, 11.5)], closed=True, r=S.r * 0.5)),
        shell(ellipse(14, 16.5, 7.5, 4.5)),
        line(seg(20, 14, 22, 11)),
        dot(10.5, 7.5, 0.9),
        detail("M11.5 15.5Q14.5 19 18 15.5"),
    ]


# ============================================================================ bath extras, mirrors, signs

@icon("bath-bomb", CAT, "Round bath bomb ball fizzing with small bubbles and specks on its surface",
      tags=["fizzy bath", "bath fizzer", "bath ball", "spa gift", "bath treat", "fizz"])
def _(S):
    band = detail(seg(5.5, 11.5, 18.5, 11.5)) if S.name == "line" else detail("M5 10.5Q12 15.5 19 10.5")
    return [
        shell(circle(12, 14, 7.75)),
        band,
        dot(8.5, 16.5, 1.1), dot(13, 18, 1.1), dot(15.5, 15, 1.1),
        dot(7.5, 3.5, 1.2), dot(12, 2.75, 1.2), dot(16.5, 3.5, 1.2),
    ]


@icon("bath-salts", CAT, "Wide glass jar of bath salt crystals with a lid",
      tags=["epsom salt", "bath crystals", "spa jar", "bath soak", "mineral salts", "aromatherapy"])
def _(S):
    def crystal(cx, cy, h=1.7):
        return mark(poly([(cx, cy - h), (cx + h, cy), (cx, cy + h), (cx - h, cy)], closed=True))
    return [
        shell(rect(5, 3.5, 14, 4, rr(S, 2))),
        shell(rect(3.5, 9, 17, 12.5, rr(S, 4))),
        crystal(8.5, 15, 1.5), crystal(12.5, 13.5, 1.5), crystal(15.5, 17, 1.5), crystal(9.5, 18.5, 1.2),
    ]


@icon("bath-caddy", CAT, "Long tray bridging across the rim of a bathtub holding a candle and a book",
      tags=["bath tray", "bath shelf", "bath rack", "spa night", "relaxing bath", "bathtub tray"])
def _(S):
    return [
        shell(rect(2.5, 10.5, 19, 3, S.R)),
        line(seg(5, 13.5, 5, 21.5)),
        line(seg(19, 13.5, 19, 21.5)),
        shell(rect(4.5, 4.5, 8, 6, S.R)),
        detail(seg(8.5, 4.5, 8.5, 10.5)),
        shell(rect(15.5, 6.5, 4, 4, rr(S, 1.5))),
        dot(17.5, 3.6, 1.3),
    ]


def _blade(ang):
    pts = []
    for t in (0, 0.33, 0.66, 1):
        pass
    import math as m
    c, s_ = m.cos(m.radians(ang)), m.sin(m.radians(ang))

    def rot(x, y):
        dx, dy = x - 12, y - 12
        return fmt(12 + dx * c - dy * s_), fmt(12 + dx * s_ + dy * c)
    p0, p1, p2, p3 = rot(12, 12), rot(12, 8.5), rot(14, 6), rot(17, 6)
    return f"M{p0[0]} {p0[1]}C{p1[0]} {p1[1]} {p2[0]} {p2[1]} {p3[0]} {p3[1]}"


@icon("bathroom-extractor-fan", CAT, "Square wall vent grille with three fan blades in the middle",
      tags=["exhaust fan", "ventilation", "bathroom vent", "extractor", "air extraction", "humidity"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(_blade(0)), detail(_blade(120)), detail(_blade(240)),
    ]


@icon("hand-dryer", CAT, "Wall-mounted hand dryer with a downward nozzle blowing air lines",
      tags=["air dryer", "restroom", "washroom", "dry hands", "warm air", "public toilet"])
def _(S):
    body = poly([(3.5, 2.5), (20.5, 2.5), (20.5, 11), (15.5, 11), (14, 14), (10, 14), (8.5, 11), (3.5, 11)], closed=True, r=S.r)
    return [
        shell(body),
        dot(7.5, 6.75, 1.2),
        line(wave(9, 21.5, 16.5)), line(wave(12, 21.5, 16.5)), line(wave(15, 21.5, 16.5)),
    ]


@icon("paper-towel-dispenser", CAT, "Wall-mounted box dispenser with a single paper towel sheet sticking out the bottom",
      tags=["towel dispenser", "restroom", "washroom", "hand towels", "tissue dispenser", "hygiene"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 14, rr(S, 3))),
        detail(rect(7.5, 6, 9, 4.5, L(S, 0, 1.5))),
        line(poly([(9, 16.5), (9, 21.5), (15, 21.5), (15, 16.5)], r=S.r)),
    ]


@icon("pedal-bin", CAT, "Round pedal bin with a hinged lid lifted open and a foot pedal at the front",
      tags=["kitchen bin", "waste bin", "trash can", "garbage", "rubbish", "step bin"])
def _(S):
    return [
        line(poly([(19, 8), (5, 4.5)], r=S.r)),
        shell(poly([(5, 10), (19, 10), (17.5, 21.5), (6.5, 21.5)], closed=True, r=S.r)),
        line(seg(18, 19.5, 21.5, 19.5)),
        detail(seg(10, 14, 14, 14)),
    ]


@icon("hand-mirror", CAT, "Oval hand mirror with a long handle and a glint line on the glass",
      tags=["vanity mirror", "handheld mirror", "makeup", "grooming", "reflection", "beauty"])
def _(S):
    return [
        shell(ellipse(12, 8.5, 6.5, 7)),
        shell(rect(10.5, 15, 3, 6.5, L(S, 0, 1.5))),
        detail(arc(12, 8.5, 3.25, 200, 255)),
    ]


@icon("compact-mirror", CAT, "Open round compact with a mirror on the lid and a powder case below the hinge",
      tags=["makeup compact", "pocket mirror", "powder compact", "cosmetics", "purse mirror", "beauty"])
def _(S):
    return [
        shell(circle(12, 7.5, 5.75)),
        detail(arc(12, 7.5, 2.75, 200, 255)),
        shell(ellipse(12, 17, 9, 4.5)),
        detail(ellipse(12, 17, 4, 1.6)),
    ]


@icon("magnifying-mirror", CAT, "Round swivel mirror on a stand with a magnified eye visible in the glass",
      tags=["makeup mirror", "shaving mirror", "zoom mirror", "vanity", "tabletop mirror", "enlarging mirror"])
def _(S):
    eye = "M7 9Q12 4.5 17 9Q12 13.5 7 9Z" if S.name == "line" else "M7.5 9Q12 5 16.5 9Q12 13 7.5 9Z"
    return [
        shell(circle(12, 9, 7.75)),
        detail(eye),
        dot(12, 9, 1.4),
        line(seg(12, 17, 12, 20.5)),
        line(seg(7, 20.5, 17, 20.5)),
    ]


@icon("lighted-vanity-mirror", CAT, "Rectangular mirror framed by round light bulbs on all four sides",
      tags=["hollywood mirror", "makeup mirror", "bulb mirror", "dressing room", "theatre mirror", "vanity lights"])
def _(S):
    parts = [shell(rect(7.5, 7.5, 9, 9, rr(S, 2))), detail(seg(10.5, 13.5, 13.5, 10.5))]
    for v in (6, 12, 18):
        parts += [dot(v, 3, 1.3), dot(v, 21, 1.3), dot(3, v, 1.3), dot(21, v, 1.3)]
    return parts


@icon("wc-sign", CAT, "The letters WC in bold, the sign for a water closet or public toilet",
      tags=["toilet sign", "restroom sign", "lavatory", "water closet", "public toilet", "loo sign"])
def _(S):
    return [
        line(poly([(2.5, 7), (5, 17), (8, 10), (11, 17), (13.5, 7)], r=S.r)),
        line(poly([(21, 7), (16.5, 7), (16.5, 17), (21, 17)], r=S.r)),
    ]


@icon("restroom-sign", CAT, "Rectangular sign split down the middle with a man figure on one side and a woman on the other",
      tags=["toilets sign", "men and women", "public toilet", "washroom sign", "gents and ladies", "wc"])
def _(S):
    dress = poly([(16.75, 10), (19.5, 18), (14, 18)], closed=True, r=L(S, 0, 0.5))
    return [
        shell(rect(2.5, 3, 19, 18, S.R)),
        detail(seg(12, 3, 12, 21)),
        dot(7.25, 7.5, 1.6),
        sq(5.5, 10, 3.5, 8, L(S, 0, 1.5)),
        dot(16.75, 7.5, 1.6),
        mark(dress),
    ]


@icon("baby-changing-table", CAT, "Changing table sign: an adult figure standing beside a baby lying on a flat table",
      tags=["nappy changing", "diaper station", "parent room", "baby room", "family restroom", "changing station"])
def _(S):
    return [
        dot(5.5, 4.5, 1.9),
        sq(4, 8, 3.5, 13.5, L(S, 0, 1.75)),
        line(seg(7.5, 10.5, 10.5, 13)),
        dot(12.5, 10.5, 1.6),
        solid(ellipse(17.5, 11, 4, 1.6)),
        line(seg(10.5, 14.5, 21.5, 14.5)),
        line(seg(12, 14.5, 12, 21.5)),
        line(seg(20, 14.5, 20, 21.5)),
    ]


@icon("changing-pad", CAT, "Padded baby changing mat with a raised border around a contoured, sunken middle",
      tags=["changing mat", "nappy mat", "diaper pad", "nursery", "baby care", "wipe clean mat"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 19, 13, S.R + 2)),
        detail(rect(6.5, 9, 11, 6, L(S, 0, 2.5))),
    ]


@icon("sauna-bucket", CAT, "Wooden sauna bucket with metal bands and a long-handled ladle resting inside",
      tags=["sauna ladle", "steam", "water bucket", "spa", "wooden pail", "finnish sauna"])
def _(S):
    return [
        shell(poly([(4.5, 9.5), (17.5, 9.5), (16.5, 21.5), (5.5, 21.5)], closed=True, r=S.r)),
        detail(seg(4.75, 13, 17.25, 13)),
        detail(seg(5.2, 18, 16.8, 18)),
        line(seg(13, 10, 21, 3)),
    ]


# ============================================================================ cleaning tools

TILT = 45  # long tools are designed upright and turned clockwise so the handle points to the bottom-left


def rot(pts, deg=TILT, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s_ = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s_, cy + (x - cx) * s_ + (y - cy) * c) for x, y in pts]


def rp(pts, closed=True, r=0.0, deg=TILT):
    return poly(rot(pts, deg), closed=closed, r=r)


def rpath(cmds, deg=TILT) -> str:
    out = []

    def pt(p):
        q = rot([p], deg)[0]
        return f"{fmt(q[0])} {fmt(q[1])}"
    for c in cmds:
        op = c[0]
        if op in ("M", "L"):
            out.append(op + pt(c[1]))
        elif op == "A":
            out.append(f"A{fmt(c[1])} {fmt(c[1])} 0 {c[2]} {c[3]} " + pt(c[4]))
        elif op == "Z":
            out.append("Z")
    return "".join(out)


def rrect(x, y, w, h, rx=0.0, deg=TILT) -> str:
    rx = max(0.0, min(rx, w / 2, h / 2))
    if rx == 0:
        return rp([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], deg=deg)
    return rpath([("M", (x + rx, y)), ("L", (x + w - rx, y)), ("A", rx, 0, 1, (x + w, y + rx)),
                  ("L", (x + w, y + h - rx)), ("A", rx, 0, 1, (x + w - rx, y + h)), ("L", (x + rx, y + h)),
                  ("A", rx, 0, 1, (x, y + h - rx)), ("L", (x, y + rx)), ("A", rx, 0, 1, (x + rx, y)), ("Z",)], deg)


def rseg(x1, y1, x2, y2, deg=TILT) -> str:
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg)
    return seg(a, b, c, d)


def rdot(x, y, r=1.0, deg=TILT) -> Part:
    c = rot([(x, y)], deg)[0]
    return dot(c[0], c[1], r)


@icon("spray-bottle", CAT, "Cleaning spray bottle with a trigger nozzle and a fine mist coming out",
      tags=["cleaner", "disinfectant", "surface spray", "household cleaning", "trigger spray", "mist"])
def _(S):
    body = poly([(4.5, 21.5), (4.5, 14), (7.5, 11), (7.5, 7.5), (5.5, 7.5), (5.5, 3.5), (14, 3.5), (17.5, 5), (17.5, 7.5), (11.5, 7.5), (11.5, 11), (14.5, 14), (14.5, 21.5)], closed=True, r=S.r)
    return [
        shell(body),
        line(poly([(14, 8.5), (16.5, 10.5), (16.5, 13)], r=S.r)),
        dot(20.5, 4, 1.1), dot(21, 7.5, 1.1), dot(20, 11, 1.1),
    ]


@icon("dustpan-and-brush", CAT, "Dustpan with a short handle and a hand brush lying across it",
      tags=["sweeping", "hand brush", "dust pan", "cleaning up", "crumbs", "housekeeping"])
def _(S):
    A = -20
    return [
        shell(rp([(3.5, 6), (14, 6), (14, 10), (3.5, 10)], r=S.r * 0.5, deg=A)),
        line(rseg(14, 8, 21, 8, A)),
        line(rseg(5.5, 10, 5.5, 13, A)), line(rseg(8.5, 10, 8.5, 13, A)), line(rseg(11.5, 10, 11.5, 13, A)),
        shell(poly([(3, 21), (17, 21), (19.5, 15.5), (5.5, 15.5)], closed=True, r=S.r)),
        line(poly([(19.5, 15.5), (21.5, 11.5)])),
    ]


@icon("lobby-dustpan", CAT, "Upright dustpan on a long handle with a hinged pan at the bottom",
      tags=["long handle dustpan", "upright dustpan", "janitor", "sweeping", "office cleaning", "stand-up dustpan"])
def _(S):
    return [
        line(poly([(14.5, 3), (19, 3), (19, 14.5)], r=S.r)),
        shell(poly([(3, 21.5), (19, 21.5), (19, 14.5), (16, 14.5)], closed=True, r=S.r)),
        dot(15.5, 18.5, 1),
    ]


@icon("feather-duster", CAT, "Feather duster with a round fan of feathers on a thin handle",
      tags=["duster", "dusting", "cobweb", "housekeeping", "cleaning", "ostrich feathers"])
def _(S):
    parts = []
    for deg, ln in ((-90, 10.5), (-55, 9.5), (-125, 9.5), (-22, 7.5), (-158, 7.5)):
        c, s_ = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        x0, y0 = 12, 13.5
        x1, y1 = x0 + ln * c, y0 + ln * s_
        if S.name == "line":
            parts.append(line(seg(x0, y0, x1, y1)))
        else:
            mx, my = x0 + ln * 0.55 * c - 1.6 * s_, y0 + ln * 0.55 * s_ + 1.6 * c
            parts.append(line(f"M{fmt(x0)} {fmt(y0)}Q{fmt(mx)} {fmt(my)} {fmt(x1)} {fmt(y1)}"))
    parts.append(shell(rect(10.5, 13.5, 3, 8, L(S, 0, 1.5))))
    return parts


@icon("dusting-mitt", CAT, "Fuzzy chenille mitt with a thumb and a looped nubby texture",
      tags=["duster glove", "microfibre mitt", "dust glove", "cleaning glove", "housework", "chenille"])
def _(S):
    body = poly([(8, 21.5), (8, 7), (10, 3.5), (16, 3.5), (18.5, 7), (18.5, 21.5)], closed=True, r=S.r * 1.5)
    thumb = poly([(8, 17), (4, 14), (4.5, 10.5), (8, 12.5)], closed=False, r=S.r * 0.5)
    return [
        shell(body),
        line(thumb),
        detail(seg(8, 18.5, 18.5, 18.5)),
        dot(11.5, 8, 1), dot(15, 8, 1), dot(13.25, 11.5, 1), dot(11.5, 15, 1), dot(15, 15, 1),
    ]


@icon("microfiber-cloth", CAT, "Square cleaning cloth with a folded corner and a quilted texture",
      tags=["cleaning cloth", "microfibre", "polishing cloth", "duster", "rag", "wiping"])
def _(S):
    body = poly([(3.5, 4.5), (14.5, 4.5), (20.5, 10.5), (20.5, 19.5), (3.5, 19.5)], closed=True, r=S.r)
    return [
        shell(body),
        detail(poly([(14.5, 4.5), (14.5, 10.5), (20.5, 10.5)], r=S.r * 0.6)),
        dot(7.5, 9, 1), dot(7.5, 15, 1), dot(12, 15, 1), dot(16.5, 15, 1), dot(11, 9.5, 1),
    ]


@icon("cleaning-sponge", CAT, "Rectangular kitchen sponge with a darker scouring layer on top",
      tags=["kitchen sponge", "dish sponge", "scrubber", "washing up", "wipe", "cleaning"])
def _(S):
    return [
        shell(rect(3.5, 6.5, 17, 13, rr(S, 3))),
        detail(seg(3.5, 12, 20.5, 12)),
        dot(8, 16.5, 1.1), dot(13, 15.75, 1.1), dot(17, 17, 1.1),
    ]


@icon("scouring-pad", CAT, "Round steel wool pad with a jagged edge and tangled curly lines",
      tags=["steel wool", "scrubbing pad", "scourer", "pot scrubber", "dish cleaning", "abrasive"])
def _(S):
    pts = [polar(12, 12, 9.4 if i % 2 == 0 else 8.0, i * 22.5) for i in range(16)]
    sp = [polar(12, 12, 0.8 + 4.6 * i / 28, -90 + 720 * i / 28) for i in range(29)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.8)),
        detail(poly(sp)),
    ]


@icon("scrub-brush", CAT, "Hand scrub brush with a curved wooden back and a row of stiff bristles below",
      tags=["hand brush", "floor brush", "laundry brush", "scrubbing", "cleaning", "stiff bristles"])
def _(S):
    back = poly([(3, 12), (3, 8.5), (6, 5.5), (18, 5.5), (21, 8.5), (21, 12)], closed=True, r=S.r)
    return [
        shell(back),
        detail(seg(8, 8.75, 16, 8.75)),
        line(seg(6, 12, 6, 18.5)), line(seg(10, 12, 10, 18.5)), line(seg(14, 12, 14, 18.5)), line(seg(18, 12, 18, 18.5)),
    ]


@icon("dish-brush", CAT, "Long-handled dish brush with a round bristle head",
      tags=["washing up", "kitchen brush", "pot brush", "dishes", "scrubber", "cleaning"])
def _(S):
    return [
        line(rseg(8.5, 2.5, 8.5, 5.5)), line(rseg(12, 2, 12, 5.5)), line(rseg(15.5, 2.5, 15.5, 5.5)),
        shell(rrect(6.5, 6, 11, 4.5, rr(S, 2))),
        shell(rrect(10.5, 10.5, 3, 11, rr(S, 1.5))),
        rdot(12, 19.5, 0.75),
    ]


@icon("sponge-wand", CAT, "Dish wand with a clear handle filled with soap and a sponge head",
      tags=["soap dispensing brush", "dish wand", "washing up", "kitchen", "soap handle", "scrubber"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 7, rr(S, 3))),
        detail(seg(4.5, 6, 19.5, 6)),
        shell(rect(9, 10, 6, 11.5, rr(S, 2))),
        detail(seg(9, 14, 15, 14)),
        dot(11, 18, 0.9), dot(13.3, 19.5, 0.8),
    ]


@icon("bottle-brush", CAT, "Bottle cleaning brush with a twisted wire stem and a cylinder of bristles",
      tags=["baby bottle brush", "flask brush", "tube cleaner", "narrow brush", "washing up", "cleaning"])
def _(S):
    parts = [shell(rect(8.5, 2.5, 7, 10, rr(S, 1.5))), line(seg(12, 12.5, 12, 21.5))]
    for y in (4.5, 7.5, 10.5):
        parts.append(line(seg(5.5, y, 8.5, y)))
        parts.append(line(seg(15.5, y, 18.5, y)))
    return parts


@icon("grout-brush", CAT, "Narrow brush with a thin angled head for cleaning tile gaps, shown between two tiles",
      tags=["tile brush", "grout cleaner", "bathroom cleaning", "tile gap", "scrub", "mould removal"])
def _(S):
    return [
        shell(rect(9.5, 2.5, 5, 9.5, rr(S, 2))),
        dot(12, 6, 1.1),
        shell(poly([(9.5, 12), (14.5, 12), (13, 15.5), (11, 15.5)], closed=True)),
        line(seg(12, 15.5, 12, 19)),
        sq(2.5, 15, 6, 6.5, L(S, 0, 1.5)),
        sq(15.5, 15, 6, 6.5, L(S, 0, 1.5)),
    ]
@icon("wire-brush", CAT, "Wire brush with a flat handle and short stiff metal bristles",
      tags=["metal brush", "rust removal", "paint stripping", "scraping", "workshop", "steel brush"])
def _(S):
    return [
        shell(rect(9.5, 2.5, 5, 9.5, rr(S, 2))),
        dot(12, 6.5, 1.1),
        shell(rect(5.5, 12, 13, 4, rr(S, 1.5))),
        line(seg(7, 16, 7, 21.5)), line(seg(10.3, 16, 10.3, 21.5)), line(seg(13.7, 16, 13.7, 21.5)), line(seg(17, 16, 17, 21.5)),
    ]


@icon("grill-brush", CAT, "Barbecue grill brush with a long handle, wire bristles and a scraper blade at the tip",
      tags=["bbq brush", "barbecue cleaner", "grill cleaning", "grate scraper", "outdoor cooking", "wire bristles"])
def _(S):
    return [
        line(seg(6, 2.5, 6, 5)), line(seg(9, 2.5, 9, 5)), line(seg(12, 2.5, 12, 5)),
        shell(rect(4, 5, 10, 4.5, rr(S, 1.5))),
        shell(poly([(14.5, 5), (20, 2.5), (20, 9.5), (14.5, 9.5)], closed=True, r=S.r)),
        shell(rect(10.5, 9.5, 3, 12, rr(S, 1.5))),
        dot(12, 19.25, 0.8),
    ]


@icon("squeegee", CAT, "Window squeegee with a T-shaped rubber blade and a short handle",
      tags=["window cleaning", "glass wiper", "shower squeegee", "window washer", "rubber blade", "streak free"])
def _(S):
    return [
        shell(rect(10.5, 8, 3, 13.5, rr(S, 1.5))),
        shell(rect(2.5, 3, 19, 5.5, rr(S, 2))),
        sq(3.5, 10.5, 17, 2.5, L(S, 0, 1)),
    ]
