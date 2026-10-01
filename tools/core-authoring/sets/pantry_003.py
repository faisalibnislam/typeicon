"""TypeIcon Core: pantry (batch pantry_003).

Packaged, preserved and boxed pantry foods drawn from the containers and foods themselves.
Mostly front views; trays and packs are shown flat.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from geometry import fmt

CAT = "pantry"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def leaf(x1, y1, x2, y2, bulge):
    """Closed pointed leaf from (x1, y1) to (x2, y2); bulge = half width."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    b = bulge * 2
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx * b)} {fmt(my + ny * b)} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(mx - nx * b)} {fmt(my - ny * b)} {fmt(x1)} {fmt(y1)}Z")


def oval_dot(cx, cy, rx, ry) -> Part:
    return Part("dot", ellipse(cx, cy, rx, ry))


# --------------------------------------------------------------------------- chunk 1

@icon("meat-tray-pack", CAT, "A shallow foam tray holding a steak with a small price label",
      tags=["steak", "meat", "butcher", "supermarket", "packaged meat", "tray"])
def _(S):
    tray = poly([(2, 14), (22, 14), (20, 21), (4, 21)], closed=True, r=S.r)
    steak = "M6 14C4 9 8 5 13 6C18 7 20 11 18 14Z"
    return [shell(tray), shell(steak), dot(11, 10.5, 1.3), Part("dot", rect(14, 16.5, 3.5, 2.5, 0.5))]


@icon("cold-cuts-pack", CAT, "A flat deli pack with a peel-back corner and fanned round slices of ham",
      tags=["deli", "ham", "luncheon meat", "sliced meat", "lunch meat", "packaged"])
def _(S):
    cres = ["M9 11A4.2 4.2 0 0 0 9 19", "M13.5 11A4.2 4.2 0 0 0 13.5 19", "M18 11A4.2 4.2 0 0 0 18 19"]
    return [shell(rect(2, 4, 20, 16, S.R)), detail(poly([(16, 4), (16, 8), (22, 8)], r=S.r)),
            *[detail(c) for c in cres]]


@icon("butcher-paper-parcel", CAT, "A paper-wrapped parcel with twisted ends and a string bow on top",
      tags=["butcher paper", "wrapped meat", "deli paper", "string", "package", "wrapped"])
def _(S):
    body = rect(5, 8, 14, 12, L(S, 0, 2))
    lf = poly([(5, 11), (2, 9.5), (2, 18.5), (5, 17)], closed=True, r=S.r * 0.5)
    rt = poly([(19, 11), (22, 9.5), (22, 18.5), (19, 17)], closed=True, r=S.r * 0.5)
    bow = [leaf(12, 8, 7.5, 3.5, 1.2), leaf(12, 8, 16.5, 3.5, 1.2)]
    return [shell(body), shell(lf), shell(rt), detail(seg(12, 8, 12, 20)), line(bow[0]), line(bow[1])]


@icon("cheese-box", CAT, "A round wooden cheese box with its lid lifted above a dome of soft cheese",
      tags=["camembert", "brie", "soft cheese", "wooden box", "dairy", "round cheese"])
def _(S):
    box = poly([(2, 14), (22, 14), (20, 21), (4, 21)], closed=True, r=S.r * 0.6)
    lid = rect(4, 3, 16, 3, L(S, 0, 1.5))
    cheese = "M6.5 14A5.5 5.5 0 0 1 17.5 14Z"
    return [shell(box), shell(lid), shell(cheese), dot(11, 11.8, 0.9)]


@icon("smoked-salmon", CAT, "A wavy slice of smoked salmon with diagonal stripes and a sprig of dill",
      tags=["lox", "gravlax", "fish", "cured fish", "salmon slice", "brunch", "dill"])
def _(S):
    body = "M2.5 13Q7 10.5 12 13T21.5 13V19Q17 21.5 12 19T2.5 19Z"
    stripes = [detail(seg(x, 14.5 + dy, x - 2, 19 + dy)) for x, dy in ((8, 0), (13, 0.3), (18, 0))]
    dill = [line(seg(12, 9, 12, 3)), line(seg(12, 6.5, 9.5, 4)), line(seg(12, 6.5, 14.5, 4))]
    return [shell(body), *stripes, *dill]


# --------------------------------------------------------------------------- chunk 2

@icon("taco-shells", CAT, "Three empty hard taco shells standing upright in a tray",
      tags=["taco", "hard shell", "tortilla", "mexican", "tex-mex", "taco night", "empty shells"])
def _(S):
    tray = rect(2, 16, 20, 5, L(S, 0, 1.5))
    return [shell(tray), line("M8 16V10A4 4 0 0 1 16 10V16"), line("M2.5 16V11.5A4.5 4.5 0 0 1 7 7"),
            line("M21.5 16V11.5A4.5 4.5 0 0 0 17 7")]


@icon("wafer-cones", CAT, "An empty wafer cone with a rim band and a crisscross grid pattern",
      tags=["ice cream cone", "sugar cone", "waffle cone", "empty cone", "dessert", "cones"])
def _(S):
    cone = poly([(6, 4), (18, 4), (12, 21)], closed=True, r=S.r)
    return [shell(cone), detail(seg(7.5, 8, 16.5, 8)), detail(seg(9, 8, 13.5, 14)), detail(seg(15, 8, 10.5, 14))]


@icon("rotisserie-chicken-box", CAT, "A takeaway tray with a clear domed lid over a whole roast chicken",
      tags=["roast chicken", "takeaway", "deli", "hot food", "supermarket chicken", "dome lid"])
def _(S):
    base = rect(2, 17, 20, 4, L(S, 0, 1.5))
    dome = "M3 17A9 9 0 0 1 21 17Z"
    return [shell(base), shell(dome), shell(rect(10.5, 5, 3, 3, 1)), detail(ellipse(11, 13.5, 4.5, 2.5)), dot(16.5, 12.5, 1.25)]


@icon("yogurt-tube", CAT, "A flat squeezable yogurt tube with a crimped top and a strawberry on the front",
      tags=["yoghurt", "kids snack", "squeeze pouch", "dairy", "lunchbox", "frozen tube"])
def _(S):
    body = poly([(6, 3), (10.5, 3), (12, 5), (13.5, 3), (18, 3), (18, 6), (17, 7), (17, 21), (7, 21), (7, 7), (6, 6)],
                closed=True, r=S.r * 0.6)
    berry = "M9 12.5Q12 11 15 12.5Q14.5 16.5 12 19Q9.5 16.5 9 12.5Z"
    return [shell(body), detail(seg(6.5, 6.5, 17.5, 6.5)), detail(berry)]


@icon("preserved-lemons", CAT, "A wide jar packed with lemon wedges in brine and salt settled at the bottom",
      tags=["pickled lemon", "moroccan", "brine", "jar", "citrus", "fermented", "salt"])
def _(S):
    jar = rect(4, 7, 16, 14, L(S, 1, 3))
    lid = rect(5, 3, 14, 4, L(S, 0, 1.5))
    return [shell(jar), shell(lid), detail(ellipse(9.5, 11.5, 2.5, 1.75)), detail(ellipse(14.5, 14.5, 2.5, 1.75)),
            dot(8, 18, 0.9), dot(12, 18, 0.9), dot(16, 18, 0.9)]


@icon("pickled-ginger", CAT, "A small dish with thin curled slices of ginger fanned up like petals",
      tags=["gari", "sushi ginger", "ginger slices", "pink ginger", "japanese", "condiment"])
def _(S):
    dish = "M3 15H21C21 19 17 21 12 21C7 21 3 19 3 15Z"
    petals = [leaf(12, 15, 5.5, 6.5, 2.6), leaf(12, 15, 12, 4, 2.6), leaf(12, 15, 18.5, 6.5, 2.6)]
    return [shell(dish), *[shell(p) for p in petals]]


@icon("pickled-plum", CAT, "A round wrinkled plum sitting on a jagged leaf",
      tags=["umeboshi", "preserved plum", "salted plum", "japanese", "sour", "ume"])
def _(S):
    plum = circle(12, 9.5, 6.5)
    leafd = poly([(3, 17.5), (6.5, 19.5), (9.5, 17.5), (12, 19.5), (14.5, 17.5), (17.5, 19.5), (21, 17.5), (21, 21.5),
                  (3, 21.5)], closed=True, r=S.r * 0.4)
    return [shell(plum), shell(leafd), detail("M12 4Q8.5 9.5 12 15")]


@icon("pickle-press", CAT, "A square pickling container with a pressing plate pushed down by a screw knob",
      tags=["fermenting", "sauerkraut", "kimchi", "pickling crock", "weight", "preserving", "screw press"])
def _(S):
    box = rect(3, 10, 18, 11, L(S, 1, 3))
    return [shell(box), line(seg(8, 3, 16, 3)), line(seg(12, 3, 12, 10)), detail(seg(12, 10, 12, 15)),
            detail(seg(6, 15, 18, 15))]


# --------------------------------------------------------------------------- chunk 3

@icon("cookie-mix-jar", CAT, "A jar of layered flour, sugar and chips tied with a ribbon at the neck",
      tags=["cookie jar gift", "baking mix", "mason jar", "layers", "homemade gift", "dry ingredients"])
def _(S):
    jar = rect(4, 8, 16, 13, L(S, 1, 3))
    lid = rect(6, 3, 12, 3, L(S, 0, 1.5))
    return [shell(jar), shell(lid), detail(seg(4, 12.5, 20, 12.5)), detail(seg(4, 16.5, 20, 16.5)),
            dot(8, 19, 0.9), dot(12, 19, 0.9), dot(16, 19, 0.9), dot(10, 14.5, 0.7), dot(14, 14.5, 0.7)]


@icon("twist-open-lid", CAT, "A jar lid seen at an angle with a curved arrow showing it twists off",
      tags=["jar opening", "unscrew", "screw cap", "twist off", "open jar", "counterclockwise", "lid"])
def _(S):
    lid = ellipse(12, 15.5, 8, 3.25)
    band = "M4 15.5V18Q4 21 12 21T20 18V15.5"
    arrow = "M19 10.5C19 3 5 3 5 10"
    head = poly([(2.5, 8), (5, 10.5), (7.5, 8)], r=S.r * 0.5)
    return [shell(lid), line(band), line(arrow), line(head)]


@icon("lemon-juice-bottle", CAT, "A lemon-shaped squeeze bottle with a small screw cap at one tip",
      tags=["lemon juice", "citrus", "squeeze bottle", "juice", "cooking", "condiment"])
def _(S):
    from dsl import P, U  # noqa: F401
    from geometry import path_to_d, rotation, transform_path
    body = "M2 12C5 9 8 6 11 6S17 9 20 12C17 15 14 18 11 18S5 15 2 12Z"
    parts = [shell(body), shell(rect(19.5, 10.5, 3, 3, L(S, 0, 1))), detail("M8 11Q9.5 9.5 11.5 9.5")]
    a, b, c, d, e, f = rotation(-35, 12, 12)
    for p in parts:
        p.d = path_to_d(transform_path(P(p.d), (a, b, c, d, e, f)))
    return parts


@icon("maraschino-cherries", CAT, "An open jar of cherries in syrup with their long stems sticking out",
      tags=["cocktail cherries", "candied cherry", "syrup", "garnish", "sundae topping", "preserved"])
def _(S):
    jar = poly([(7, 9), (17, 9), (20, 12), (20, 21), (4, 21), (4, 12)], closed=True, r=S.r)
    return [shell(jar), detail(circle(9.5, 16, 2.25)), detail(circle(14.5, 16, 2.25)),
            line("M9.5 13.75C9.5 9 10.5 6 12.5 3.5"), line("M14.5 13.75C14.5 9 15.5 6 17.5 3.5")]


@icon("sticky-rice-basket", CAT, "A small lidded woven basket with a narrow waist and a carrying loop",
      tags=["steamer", "thai", "bamboo", "glutinous rice", "woven", "kratip", "lidded basket"])
def _(S):
    lid = "M6 10Q6 5 12 5Q18 5 18 10Z"
    body = poly([(7, 10), (17, 10), (14.5, 15), (16.5, 21), (7.5, 21), (9.5, 15)], closed=True, r=S.r * 0.6)
    return [shell(lid), shell(body), line("M9.5 5C9.5 1.5 14.5 1.5 14.5 5"), detail(seg(9.5, 18, 14.5, 18))]


@icon("coffee-brick", CAT, "A vacuum-packed brick of ground coffee with a round one-way valve",
      tags=["ground coffee", "coffee pack", "vacuum pack", "beans", "roast", "grocery", "espresso"])
def _(S):
    outline = poly([(3, 9), (6, 4), (21, 4), (21, 16), (18, 21), (3, 21)], closed=True, r=S.r * 0.6)
    return [shell(outline), detail(seg(3, 9, 18, 9)), detail(seg(18, 9, 18, 21)), detail(seg(18, 9, 21, 4)),
            detail(circle(10.5, 15, 2.5))]


@icon("moldy-bread", CAT, "A bread slice with fuzzy round mold spots across its face",
      tags=["mouldy", "spoiled", "stale", "expired", "rotten", "food waste", "mold"])
def _(S):
    k = L(S, 0, 2)
    body = (f"M5 10C2 10 2 4 7 4H17C22 4 22 10 19 10V{fmt(21 - k)}"
            + (f"Q19 21 {fmt(19 - k)} 21H{fmt(5 + k)}Q5 21 5 {fmt(21 - k)}Z" if k else "V21H5Z"))
    return [shell(body), dot(9.5, 11.5, 1.6), dot(14.5, 14, 2), dot(9.5, 17, 1.3), detail(circle(14.5, 9.5, 1.2))]
