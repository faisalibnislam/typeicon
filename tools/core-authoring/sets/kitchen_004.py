"""TypeIcon Core: kitchen (batch kitchen_004): serving ware, specialist tools, cooking actions and appliance modes.

Dishes and pots are drawn in side view unless the top is what identifies them. Long hand utensils are
drawn upright and turned 45 degrees clockwise so the handle points to the bottom-left, matching the
tools set and kitchen_001.
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


def arrow_head(tip, heading, size):
    """Chevron points (wing, tip, wing) for an arrow pointing along heading (degrees, 0 = right, 90 = down)."""
    a = pt_on(tip[0], tip[1], size, heading + 180 - 45)
    b = pt_on(tip[0], tip[1], size, heading + 180 + 45)
    return [a, tip, b]


def steam(S, xs, y0, y1):
    """Short wavy rising lines (heat, steam, sizzle)."""
    h = y0 - y1
    out = []
    for x in xs:
        out.append(line(f"M{fmt(x)} {fmt(y0)}C{fmt(x - 1.5)} {fmt(y0 - h * 0.35)} {fmt(x + 1.5)} {fmt(y0 - h * 0.65)} {fmt(x)} {fmt(y1)}"))
    return out


# ============================================================================ serving ware

@icon("crepe-spreader", CAT, "T-shaped crepe spreader resting on a thin crepe",
      tags=["crepe rake", "batter spreader", "crepe", "pancake", "galette", "kitchen tool"])
def _(S):
    tool = poly([(10.75, 2.5), (13.25, 2.5), (13.25, 10), (20.5, 10), (20.5, 12.5), (3.5, 12.5), (3.5, 10), (10.75, 10)],
                closed=True, r=S.r * 0.6)
    crepe = ellipse(12, 18.5, 9.5, 3) if S.name == "rounded" else poly([(2.5, 18.5), (5.5, 15.5), (18.5, 15.5), (21.5, 18.5), (18.5, 21.5), (5.5, 21.5)], closed=True)
    return [shell(tool), shell(crepe)]


@icon("cheese-curler", CAT, "Cheese curler: a cheese wheel on a board with a spindle, a crank arm and a curled rosette",
      tags=["girolle", "cheese scraper", "tete de moine", "cheese rosette", "cheese tool"], aliases=["girolle"])
def _(S):
    body = union(rect(5, 12, 14, 6.5, rr(S, 1)), rect(2.5, 18.5, 19, 3, rr(S, 1.5)))
    ros = poly(regular(7.5, 8, 2.3, 8), closed=True, r=L(S, 0, 0.8))
    return [shell(body), shell(ros), line(seg(12, 12, 12, 4.5)),
            line(poly([(12, 5), (19, 5), (19, 9)], r=S.r)), dot(12, 4, 1.5)]


@icon("oyster-plate", CAT, "Round oyster plate from above with six shell-shaped wells around a centre cup",
      tags=["oyster dish", "seafood plate", "shellfish", "raw bar", "serving plate"])
def _(S):
    out = [shell(circle(12, 12, 9.5)), dot(12, 12, 1.5)]
    for k in range(6):
        a = -90 + k * 60
        c = pt_on(12, 12, 6.6, a)
        tip = pt_on(12, 12, 3.3, a)
        r, off = 1.9, math.degrees(math.acos(1.9 / 3.3))
        pa, pb = pt_on(c[0], c[1], r, a + 180 + off), pt_on(c[0], c[1], r, a + 180 - off)
        if S.name == "rounded":
            t1, t2 = pt_on(tip[0], tip[1], 0.6, a + 90), pt_on(tip[0], tip[1], 0.6, a - 90)
            d = (f"M{fmt(t2[0])} {fmt(t2[1])}L{fmt(pb[0])} {fmt(pb[1])}A{r} {r} 0 1 0 {fmt(pa[0])} {fmt(pa[1])}"
                 f"L{fmt(t1[0])} {fmt(t1[1])}A0.6 0.6 0 0 0 {fmt(t2[0])} {fmt(t2[1])}Z")
        else:
            d = f"M{fmt(tip[0])} {fmt(tip[1])}L{fmt(pb[0])} {fmt(pb[1])}A{r} {r} 0 1 0 {fmt(pa[0])} {fmt(pa[1])}Z"
        out.append(hole(d))
    return out


@icon("chip-and-dip-bowl", CAT, "Wide serving bowl from above with a small dip bowl in the centre and chips around it",
      tags=["chip and dip", "snack bowl", "dip bowl", "party platter", "nachos", "serving bowl"])
def _(S):
    out = [shell(circle(12, 12, 9.5)), detail(circle(12, 12, 3))]
    for k in range(5):
        a = -90 + k * 72
        c = pt_on(12, 12, 6.7, a)
        tri = [pt_on(c[0], c[1], 2.1, a + 180 + j * 120) for j in range(3)]
        out.append(hole(poly(tri, closed=True, r=L(S, 0, 0.5))))
    return out


@icon("sushi-board", CAT, "Low wooden sushi board on two feet with two sushi rolls on top",
      tags=["geta", "sushi plate", "serving board", "japanese", "sushi"], aliases=["sushi-geta"])
def _(S):
    board = union(rect(2.5, 14.5, 19, 3, L(S, 0.5, 1.5)), rect(5, 16, 3, 5, L(S, 0, 1)), rect(16, 16, 3, 5, L(S, 0, 1)))
    out = [shell(board)]
    for x in (7.5, 16.5):
        out += [shell(circle(x, 8.5, 3)), dot(x, 8.5, 1.1)]
    return out


@icon("chopstick-rest", CAT, "Small chopstick rest with a pair of chopsticks lying across it",
      tags=["chopstick holder", "hashioki", "chopsticks", "table setting", "japanese dining"], aliases=["hashioki"])
def _(S):
    rest = rect(12, 14.5, 9, 5, rr(S, 2.5))
    return [shell(rest), detail(seg(14.5, 17, 18.5, 17)),
            line(seg(2.5, 20.5, 21.5, 7)), line(seg(2.5, 16.5, 19.5, 4))]


@icon("stone-bowl", CAT, "Heavy stone bowl on a wooden base with sizzle lines above",
      tags=["dolsot", "hot stone bowl", "bibimbap", "korean", "sizzling bowl"], aliases=["dolsot"])
def _(S):
    bowl = f"M3.5 10.5H20.5V{fmt(11 + L(S, 0, 0))}A8.5 6.5 0 0 1 3.5 11Z"
    return [shell(bowl), detail(seg(5.5, 13, 18.5, 13)), shell(rect(5, 19, 14, 2.5, rr(S, 1.25)))] + steam(S, (8, 12, 16), 7.5, 2.5)


@icon("gratin-dish", CAT, "Shallow oval gratin dish with a small ear handle at each end",
      tags=["au gratin", "oval baking dish", "gratin", "oven dish", "bakeware"])
def _(S):
    body = f"M4 11A8 3.5 0 0 1 20 11C19.5 15 17.5 17 15 17H9C6.5 17 4.5 15 4 11Z"
    ear = rect(1.8, 10, 3.2, 2.5, L(S, 0, 1.25))
    return [shell(union(body, ear, flip(ear))), detail("M5.5 12C8 14 16 14 18.5 12")]


@icon("terrine-mold", CAT, "Long narrow terrine mold with a flat lid and a small knob",
      tags=["terrine", "pate mold", "loaf mold", "terrine dish", "bakeware"], aliases=["pate-mold"])
def _(S):
    body = union(rect(2, 10, 20, 2.5, rr(S, 1.25)), rect(3.5, 12, 17, 6.5, L(S, 1, 2)), rect(10, 7, 4, 3.5, L(S, 0, 1.5)))
    return [shell(body), detail(seg(3.5, 12.5, 20.5, 12.5))]


@icon("gravy-separator", CAT, "Fat separator jug with a spout that rises from the bottom beside the body",
      tags=["fat separator", "gravy jug", "fat strainer", "sauce", "roast dinner"], aliases=["fat-separator"])
def _(S):
    return [shell(rect(7.5, 4.5, 9, 16.5, rr(S, 2))),
            line(poly([(16.5, 8), (20, 8), (20, 16), (16.5, 16)], r=S.r)),
            line(poly([(7.5, 18), (4, 18), (4, 7), (2.5, 4.5)], r=S.r)),
            detail(seg(10, 9, 14, 9))]


@icon("pie-iron", CAT, "Pie iron: a hinged square cooking head on two long handles over a flame",
      tags=["jaffle iron", "campfire sandwich", "toastie iron", "camping", "sandwich maker"], aliases=["jaffle-iron"])
def _(S):
    flame = "M7 14.5C10 17 10.5 18.5 10.5 19.5A3.5 3.5 0 0 1 3.5 19.5C3.5 18 4.5 16.5 7 14.5Z"
    if S.name == "line":
        flame = "M7 14.5L10.5 19.5L7 22L3.5 19.5Z"
    return [shell(rect(2.5, 5, 9, 6.5, rr(S, 2))), detail(seg(2.5, 8.25, 11.5, 8.25)),
            line(seg(11.5, 6, 21.5, 6)), line(seg(11.5, 10.5, 21.5, 10.5)), shell(flame)]


@icon("roasting-stick", CAT, "Long two-pronged roasting stick with a marshmallow on the tips",
      tags=["marshmallow stick", "campfire fork", "toasting fork", "s'mores", "camping"], aliases=["marshmallow-stick"])
def _(S):
    return tilt([shell(rect(7.5, 0.5, 9, 5, L(S, 0.8, 2.5))),
                 line(poly([(9, 5.5), (9, 8), (12, 12), (15, 8), (15, 5.5)], r=S.r * 0.6)),
                 line(seg(12, 12, 12, 17.5)), shell(rect(10.75, 17.5, 2.5, 6, L(S, 0, 1.25)))])


# ============================================================================ serving and trays


@icon("lid-rack", CAT, "Rack holding two pot lids standing on edge",
      tags=["lid holder", "lid organizer", "pan lid rack", "kitchen storage", "cabinet organizer"],
      aliases=["lid-organizer"])
def _(S):
    back = minus(circle(15.5, 9.5, 6), circle(9.5, 12, 8.5))
    return [shell(back), shell(circle(9.5, 12, 6.5)), dot(9.5, 12, 1.4), dot(17.5, 8, 1.2),
            line(poly([(2.5, 17), (2.5, 21), (21.5, 21), (21.5, 14)], r=S.r))]


@icon("spaghetti-jar", CAT, "Tall glass storage jar packed with long strands of dry spaghetti standing up out of it",
      tags=["pasta jar", "storage jar", "canister", "pantry", "spaghetti", "pasta storage"])
def _(S):
    return [shell(rect(6, 9, 12, 12.5, rr(S))), detail(seg(6, 12, 18, 12)),
            line(seg(9, 9, 8, 2.5)), line(seg(12, 9, 12, 2)), line(seg(15, 9, 16, 2.5))]


@icon("placemat", CAT, "Rectangular placemat from above set with a plate, a fork and a knife",
      tags=["place mat", "table mat", "table setting", "place setting", "dining"], aliases=["table-mat"])
def _(S):
    return [shell(rect(2, 5, 20, 14, L(S, 1, 3))), detail(circle(12, 12, 3.5)),
            detail(seg(5.5, 8.5, 5.5, 15.5)), detail(seg(18.5, 8.5, 18.5, 15.5))]


@icon("airline-meal-tray", CAT, "Airline meal tray with a covered dish, a cup and wrapped cutlery",
      tags=["in-flight meal", "plane food", "meal tray", "airplane meal", "catering", "travel"],
      aliases=["inflight-meal"])
def _(S):
    return [shell(rect(2, 4, 20, 16, rr(S, 3))), detail(rect(5, 7.5, 7.5, 5, L(S, 0, 1.5))),
            detail(circle(17.25, 10, 1.75)), detail(seg(5.5, 16.5, 18.5, 16.5))]


@icon("sushi-conveyor", CAT, "Sushi conveyor belt with rollers carrying two plates of sushi",
      tags=["kaiten sushi", "conveyor belt sushi", "sushi train", "revolving sushi", "japanese restaurant"],
      aliases=["sushi-train"])
def _(S):
    out = [shell(rect(2, 16.5, 20, 5, 2.5 if S.name == "rounded" else 1)),
           dot(5, 19, 1), dot(12, 19, 1), dot(19, 19, 1)]
    for x in (7, 17):
        out.append(shell(union(rect(x - 4, 12, 8, 1.5, L(S, 0, 0.75)), rect(x - 2.5, 7.5, 5, 4.5, L(S, 0.5, 2)))))
    return out


@icon("poaching-egg", CAT, "Pot of water from above with a swirling whirlpool and an egg in the middle",
      tags=["poached egg", "whirlpool", "poach", "breakfast", "egg", "cooking method"])
def _(S):
    spiral = "M17.5 12A5.5 5.5 0 0 1 6.5 12A4.5 4.5 0 0 1 15.5 12"
    if S.name == "line":
        spiral = "M17.5 12A5.5 5.5 0 0 1 6.5 12A4.5 4.5 0 0 1 14.5 9.5"
    return [shell(circle(12, 12, 8.5)), line(seg(2, 12, 3.5, 12)), line(seg(20.5, 12, 22, 12)),
            detail(spiral), dot(11.3, 12, 1.7)]


@icon("frosting-cake", CAT, "Offset spatula smoothing frosting on the side of a round layer cake",
      tags=["icing a cake", "cake decorating", "offset spatula", "frosting", "layer cake", "baking"],
      aliases=["icing-cake"])
def _(S):
    return [shell(rect(2.5, 9, 11.5, 12, rr(S, 2))), detail(seg(2.5, 13, 14, 13)), detail(seg(2.5, 17, 14, 17)),
            shell(rect(16.5, 9.5, 2.5, 11, L(S, 0, 1.25))),
            line(poly([(17.75, 9.5), (17.75, 7.5), (20, 5.5)], r=S.r)), shell(rect(19.5, 1.5, 2.5, 4.5, L(S, 0, 1.25)))]


@icon("piping-frosting", CAT, "Piping bag squeezing a swirl of frosting onto a cupcake",
      tags=["piping bag", "icing", "cupcake", "cake decorating", "frosting", "baking"])
def _(S):
    cake = union("M5 16C4 13 6.5 11 9 11.5C10 9.5 14 9.5 15 11.5C17.5 11 20 13 19 16Z",
                 poly([(6, 15.5), (18, 15.5), (16.5, 21.5), (7.5, 21.5)], closed=True, r=S.r * 0.5))
    bag = poly([(12, 7.5), (17, 1.5), (21.5, 5)], closed=True, r=S.r)
    return [shell(cake), detail(seg(5.5, 16, 18.5, 16)), detail(seg(10.5, 18.5, 10.5, 20)), detail(seg(13.5, 18.5, 13.5, 20)),
            shell(bag, stroke_miterlimit="2")]


@icon("slicing-bread", CAT, "Bread knife cutting into a loaf with a slice fallen away",
      tags=["bread knife", "slicing", "cutting bread", "loaf", "baking", "sandwich"])
def _(S):
    loaf = "M9.5 21.5V14.5C9.5 12 11.5 11 15.5 11C19.5 11 21.5 12 21.5 14.5V21.5Z"
    knife = union(rect(12.25, 1.5, 3, 4.5, L(S, 0, 1.5)), rect(12.5, 5.5, 2.5, 9, L(S, 0, 0.5)))
    slice_ = rot(rect(3, 12.5, 4, 9, L(S, 0.5, 1.8)), -12, 5, 17)
    return [shell(loaf), shell(knife), shell(slice_)]


@icon("draining-pasta", CAT, "Pot tipped over a colander, pouring out pasta",
      tags=["drain pasta", "colander", "strainer", "cooking pasta", "boiling", "noodles"])
def _(S):
    pot = rot(rect(2.5, 3, 10, 7, rr(S, 2)), 30, 7.5, 6.5)
    return [shell(pot), shell("M5.5 15H20.5A7.5 6 0 0 1 5.5 15Z"), dot(10, 17.5, 1), dot(13, 18.5, 1), dot(16, 17.5, 1),
            line(seg(20.5, 15, 22, 13.5)),
            line("M13 10.5C12 11.5 14 12 13 13"), line("M16 9.5C15 10.5 17 11 16 12.5")]


@icon("tossing-salad", CAT, "Salad servers lifting leaves above a bowl, with motion marks",
      tags=["salad", "toss", "salad servers", "mixing", "healthy eating", "greens"])
def _(S):
    bowl = "M3 13.5H21A9 7 0 0 1 3 13.5Z"
    leaf = "M8 10.5C8 7 10 5.5 13 5.5C13 9 11 10.5 8 10.5Z"
    leaf2 = "M13.5 3.5C16 2 18.5 3 19.5 5.5C17 7 14.5 6 13.5 3.5Z"
    return [shell(bowl), shell(leaf), shell(leaf2),
            line(seg(4, 11.5, 6, 3.5)), line(seg(20, 11.5, 19, 8.5)),
            line(arc(12, 8, 10, 195, 215)), line(arc(12, 8, 10, -35, -15))]


@icon("filleting-fish", CAT, "Long thin filleting knife lying below a whole fish",
      tags=["fillet knife", "filleting", "fish prep", "fishmonger", "seafood", "butchery"])
def _(S):
    fish = "M2.5 9C5 4.5 11.5 4 15.5 8.5L20.5 5V13L15.5 9.5C11.5 14 5 13.5 2.5 9Z"
    blade = poly([(2.5, 18), (15, 16.75), (15, 19.25), (4, 19.25)], closed=True, r=L(S, 0, 0.6))
    return [shell(fish, stroke_miterlimit="2"), dot(6.5, 8, 1.1), detail(seg(9, 9, 13, 9)),
            shell(union(blade, rect(15, 16, 7, 4, L(S, 0, 2))))]


@icon("marinating", CAT, "Bowl of meat pieces submerged in marinade with a basting brush resting on the rim",
      tags=["marinade", "marinate", "soak", "meat prep", "bbq", "brine"], aliases=["marinade"])
def _(S):
    bowl = "M2.5 12H18.5A8 8 0 0 1 2.5 12Z"
    brush = rot(rect(12.5, 7.5, 4, 3.5, L(S, 0, 1.2)), -40, 14.5, 9.25)
    return [shell(bowl), detail("M5 14.5C7 13.5 8.5 15.5 10.5 14.5S14 13.5 16 14.5"),
            hole(rect(6.5, 16.5, 3, 2.5, L(S, 0, 1))), hole(rect(11.5, 16.5, 3, 2.5, L(S, 0, 1))),
            shell(brush), line(seg(16.5, 7.5, 21.5, 3))]


# ============================================================================ oven modes

def _frame(S):
    return shell(rect(3, 3, 18, 18, rr(S, 4)))


@icon("oven-rotisserie-mode", CAT, "Oven rotisserie mode: a spit across the frame with a rotation arrow above it",
      tags=["rotisserie", "spit roast", "oven setting", "oven function", "appliance symbol"])
def _(S):
    return [_frame(S), detail(seg(6, 15.5, 18, 15.5)), dot(12, 15.5, 1.75), detail(arc(12, 12.5, 4.5, 190, 335)),
            detail(poly(arrow_head(pt_on(12, 12.5, 4.5, 335), 335 + 90, 2.8), r=S.r * 0.4))]


@icon("oven-pizza-mode", CAT, "Oven pizza mode: a pizza slice above a bottom heating bar",
      tags=["pizza setting", "oven setting", "oven function", "bottom heat", "appliance symbol"])
def _(S):
    return [_frame(S), detail(poly([(7, 7.5), (17, 7.5), (12, 14.5)], closed=True, r=S.r * 0.5)),
            detail(seg(7, 17.5, 17, 17.5))]


@icon("oven-proof-mode", CAT, "Oven proof mode: a small rising loaf with an upward arrow",
      tags=["proofing", "dough rise", "oven setting", "oven function", "bread", "appliance symbol"],
      aliases=["oven-proving-mode"])
def _(S):
    loaf = "M7 17.5V15C7 12.5 9 11.5 12 11.5C15 11.5 17 12.5 17 15V17.5Z"
    return [_frame(S), detail(loaf), detail(seg(12, 9, 12, 5.5)), detail(poly([(10, 7.5), (12, 5.5), (14, 7.5)], r=S.r * 0.4))]


def _sparkle(cx, cy, r):
    pts = []
    for k in range(8):
        pts.append(pt_on(cx, cy, r if k % 2 == 0 else r * 0.32, -90 + k * 45))
    return poly(pts, closed=True)


@icon("oven-self-clean", CAT, "Oven self-clean mode: sparkles inside the oven frame",
      tags=["pyrolytic", "self cleaning", "oven setting", "oven function", "clean", "appliance symbol"],
      aliases=["oven-pyrolytic-clean"])
def _(S):
    big = _sparkle(10, 13, 4.5)
    return [_frame(S), hole(big), hole(_sparkle(15.5, 7.5, 2.5)), hole(_sparkle(16, 16.5, 2))]


# ============================================================================ specialist tools and containers

@icon("jar-lifter", CAT, "Jar lifter tongs gripping the neck of a jar",
      tags=["canning tongs", "jar tongs", "canning", "preserving", "jar grabber", "kitchen tool"])
def _(S):
    jar = union(rect(9, 11, 6, 4, L(S, 0.5, 1)), rect(5, 14.5, 14, 7, rr(S, 3)))
    arm = poly([(7, 1.5), (12, 5), (17, 8.5), (17, 12)], r=S.r)
    return [shell(jar), line(arm), line(flip(arm)), detail(seg(8, 18, 16, 18))]


@icon("batter-dispenser", CAT, "Batter dispenser funnel with a handle releasing a drop of batter onto a pancake",
      tags=["pancake batter", "funnel dispenser", "cupcake batter", "baking", "pancakes"])
def _(S):
    body = poly([(4, 3), (16, 3), (16, 9), (11.5, 13.5), (8.5, 13.5), (4, 9)], closed=True, r=S.r * 0.6)
    return fit([shell(body), line(poly([(16, 4.5), (20, 4.5), (20, 11)], r=S.r)), detail(seg(6.5, 6, 13.5, 6)),
                dot(10, 16.5, 1.2), shell(rect(3, 19, 14, 3, 1.5 if S.name == "rounded" else 0.5))])


@icon("birds-beak-knife", CAT, "Short paring knife with a blade that curves down like a bird's beak",
      tags=["tourne knife", "peeling knife", "paring knife", "curved knife", "garnish", "kitchen knife"],
      aliases=["tourne-knife"])
def _(S):
    blade = "M10 13C9.5 8.5 11.5 4 17 2C14.5 5 14 9 14 13Z"
    return tilt([shell(blade, stroke_miterlimit="2"), shell(rect(10, 15, 4, 7.5, L(S, 0.5, 2))),
                 dot(12, 18.75, 0.9)])


@icon("sashimi-knife", CAT, "Very long slim sashimi knife with a straight spine, a pointed tip and a plain wooden handle",
      tags=["yanagiba", "sushi knife", "slicing knife", "japanese knife", "sashimi", "kitchen knife"],
      aliases=["yanagiba"])
def _(S):
    blade = poly([(10.5, 14.5), (10.5, 1), (13.5, 5.5), (13.5, 14.5)], closed=True, r=L(S, 0, 0.4))
    return tilt([shell(blade, stroke_miterlimit="2"), shell(rect(10.5, 17.5, 3, 6, L(S, 0, 1.5)))])


@icon("deli-container", CAT, "Round plastic deli tub with a snap-on lid and food visible through the side",
      tags=["deli tub", "takeout container", "soup container", "leftovers", "food storage", "quart container"])
def _(S):
    tub = union(rect(3.5, 3.5, 17, 4.5, L(S, 0.5, 1.5)), poly([(5, 7.5), (19, 7.5), (18, 21), (6, 21)], closed=True, r=S.r * 0.6))
    return [shell(tub), detail(seg(3.5, 8, 20.5, 8)), detail("M6.5 13C8.5 12 10 14 12 13S15.5 12 17.5 13")]


@icon("clamshell-container", CAT, "Hinged clamshell takeout box with its lid partly open",
      tags=["takeout box", "to-go box", "styrofoam box", "food container", "takeaway", "leftovers"],
      aliases=["takeout-box"])
def _(S):
    base = poly([(3, 13), (21, 13), (19, 20.5), (5, 20.5)], closed=True, r=S.r * 0.5)
    lid = rot(poly([(3, 11), (21, 11), (19, 6), (5, 6)], closed=True, r=S.r * 0.5), -25, 3, 11)
    return fit([shell(base), shell(lid)])


@icon("bakery-rack", CAT, "Tall wheeled bakery rack holding stacked sliding trays",
      tags=["sheet pan rack", "speed rack", "bun rack", "baking trays", "commercial kitchen", "bakery"],
      aliases=["speed-rack"])
def _(S):
    return [shell(rect(5, 2, 14, 16, L(S, 0.5, 2.5))), detail(seg(5, 6, 19, 6)), detail(seg(5, 10, 19, 10)),
            detail(seg(5, 14, 19, 14)), dot(7, 20.75, 1.5), dot(17, 20.75, 1.5)]


@icon("souffle-dish", CAT, "Deep fluted souffle dish with a puffed souffle rising above the rim",
      tags=["souffle", "ramekin", "baked dessert", "french cooking", "bakeware"])
def _(S):
    dish = union(rect(3.5, 11, 17, 10.5, rr(S, 2)), f"M5.5 12V9C5.5 {L(S, 2.5, 2)} 18.5 {L(S, 2.5, 2)} 18.5 9V12Z")
    return [shell(dish), detail(seg(3.5, 11, 20.5, 11)),
            detail(seg(7.5, 14, 7.5, 18.5)), detail(seg(12, 14, 12, 18.5)), detail(seg(16.5, 14, 16.5, 18.5))]


def _teeth(p0, p1, n, depth, square):
    """Points along p0 -> p1 with n notches cut inward (to the right of travel)."""
    (x0, y0), (x1, y1) = p0, p1
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux
    pts = []
    step = ln / (2 * n + 1)
    for k in range(1, 2 * n + 1):
        t = k * step
        bx, by = x0 + ux * t, y0 + uy * t
        inward = (k % 2 == 1)
        if square:
            if inward:
                pts += [(bx, by), (bx + nx * depth, by + ny * depth)]
            else:
                pts += [(bx + nx * depth, by + ny * depth), (bx, by)]
        else:
            if inward:
                pts.append((bx, by))
                pts.append((bx + ux * step / 2 + nx * depth, by + uy * step / 2 + ny * depth))
    return pts


@icon("cake-comb", CAT, "Triangular cake comb with a different toothed pattern on two of its edges",
      tags=["cake scraper", "icing comb", "decorating comb", "frosting texture", "cake decorating", "baking"],
      aliases=["icing-comb"])
def _(S):
    a, b, c = (12, 2), (22, 20.5), (2, 20.5)
    pts = [a] + _teeth(a, b, 3, 2.5, False) + [b] + _teeth(b, c, 2, 3, True) + [c]
    return [shell(poly(pts, closed=True, r=S.r * 0.4), stroke_miterlimit="2")]


@icon("lattice-roller", CAT, "Lattice pastry roller above a dough sheet cut with staggered slits",
      tags=["lattice cutter", "pastry cutter", "pie crust", "dough cutter", "lattice pie", "baking"],
      aliases=["lattice-cutter"])
def _(S):
    return [shell(rect(2.5, 2.5, 13, 6.5, rr(S, 2))), detail(seg(6.5, 2.5, 6.5, 9)), detail(seg(11.5, 2.5, 11.5, 9)),
            line(poly([(15.5, 5.75), (19.5, 5.75), (21.5, 10)], r=S.r)),
            shell(rect(2.5, 12.5, 19, 9, rr(S, 2))), detail(seg(5.5, 15.5, 10, 15.5)), detail(seg(13.5, 15.5, 18.5, 15.5)),
            detail(seg(9.5, 18.5, 14.5, 18.5))]


@icon("brioche-mold", CAT, "Deep round brioche mold with steeply flared fluted sides",
      tags=["brioche tin", "fluted mold", "brioche pan", "bakeware", "french baking"], aliases=["brioche-tin"])
def _(S):
    top = 6.5
    d = f"M2.5 {top}"
    xs = [2.5 + i * 19 / 4 for i in range(5)]
    for x in xs[1:]:
        d += f"A2.375 2.375 0 0 1 {fmt(x)} {top}"
    d += f"L16 20H8Z"
    return [shell(d), detail(seg(7.25, 9.5, 9.5, 17)), detail(seg(12, 9.5, 12, 17)), detail(seg(16.75, 9.5, 14.5, 17))]


@icon("flat-beater", CAT, "Stand mixer flat beater: an open triangular paddle on a short shaft",
      tags=["paddle attachment", "mixer paddle", "stand mixer", "beater", "mixing", "baking"],
      aliases=["paddle-attachment"])
def _(S):
    paddle = "M9 8H15L20 17C20.5 20 18.5 21.5 16 21.5H8C5.5 21.5 3.5 20 4 17Z"
    if S.name == "line":
        paddle = "M9 8H15L20.5 19.5V21.5H3.5V19.5Z"
    return [shell(rect(10.5, 2, 3, 6, L(S, 0, 1.5))), shell(paddle), detail(seg(12, 8, 12, 21.5))]


@icon("heated-display-case", CAT, "Glass-fronted heated display counter with food inside and heat rising above",
      tags=["hot food display", "food warmer", "heated cabinet", "deli counter", "hot case", "takeaway"],
      aliases=["food-warmer-case"])
def _(S):
    case = poly([(2.5, 21.5), (2.5, 14), (6.5, 10), (21.5, 10), (21.5, 21.5)], closed=True, r=S.r * 0.6)
    return [shell(case), detail(seg(2.5, 17.5, 21.5, 17.5)),
            hole("M8 15.5A2.25 2.25 0 0 1 12.5 15.5Z"), hole("M14.5 15.5A2.25 2.25 0 0 1 19 15.5Z")] + steam(S, (9, 14, 19), 7.5, 2.5)


@icon("trifle-bowl", CAT, "Footed glass trifle bowl showing layered stripes of dessert",
      tags=["trifle", "layered dessert", "glass bowl", "parfait", "pudding", "dessert"])
def _(S):
    bowl = union(rect(4, 2.5, 16, 12, L(S, 2, 4)), rect(10.5, 14, 3, 4.5), rect(6.5, 18, 11, 3.5, L(S, 0.5, 1.75)))
    return [shell(bowl), detail("M4 6.5C6.5 5.5 9 7.5 12 6.5S17.5 5.5 20 6.5"), detail(seg(4, 10.5, 20, 10.5))]


# ============================================================================ pots, stands and service

def _flame(S, cx, top, w, bottom):
    """Small flame: rounded teardrop for Rounded, faceted for Line."""
    h = bottom - top
    if S.name == "line":
        return poly([(cx, top), (cx + w / 2, top + h * 0.62), (cx, bottom), (cx - w / 2, top + h * 0.62)], closed=True)
    r = w / 2
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + r * 0.9)} {fmt(top + h * 0.3)} {fmt(cx + r)} {fmt(bottom - r * 1.2)} {fmt(cx + r)} {fmt(bottom - r)}"
            f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx - r)} {fmt(bottom - r)}C{fmt(cx - r)} {fmt(bottom - r * 1.2)} {fmt(cx - r * 0.9)} {fmt(top + h * 0.3)} {fmt(cx)} {fmt(top)}Z")


@icon("mustard-pot", CAT, "Small lidded mustard pot with a tiny spoon handle poking out of the lid",
      tags=["mustard", "condiment pot", "mustard jar", "table condiment", "relish"])
def _(S):
    pot = union(rect(4.5, 8.5, 15, 3.5, L(S, 0.5, 1.75)), rect(6, 11, 12, 10.5, rr(S, 3)), circle(10, 7.5, 1.75))
    return [shell(pot), detail(seg(6, 12, 18, 12)), line(seg(15.5, 8.5, 19, 2.5)), dot(19.25, 2.5, 1.5)]


@icon("three-legged-pot", CAT, "Round-bellied cast iron pot on three short legs with a lid and a bail handle",
      tags=["potjie", "cast iron pot", "campfire pot", "dutch oven", "cauldron", "outdoor cooking"],
      aliases=["potjie"])
def _(S):
    body = union("M3.5 11H20.5C20.5 16.5 17 19 12 19C7 19 3.5 16.5 3.5 11Z", rect(6, 8.5, 12, 3, L(S, 0.5, 1.5)))
    bail = "M3.5 11.5C3.5 1.5 20.5 1.5 20.5 11.5"
    return [shell(body), detail(seg(3.5, 11, 20.5, 11)), line(bail),
            line(seg(7, 17.5, 6, 21.5)), line(seg(17, 17.5, 18, 21.5)), line(seg(12, 19, 12, 21.5))]


@icon("plating", CAT, "Plating tweezers placing a garnish on a stacked portion of food on a plate",
      tags=["food plating", "presentation", "fine dining", "plating tweezers", "garnish", "chef"],
      aliases=["food-plating"])
def _(S):
    plate = "M2 17.5H22C21 20 19 21 16 21H8C5 21 3 20 2 17.5Z"
    return [shell(plate), shell(rect(5, 11, 10, 6.5, rr(S, 2))), detail(seg(5, 14.25, 15, 14.25)),
            line(poly([(21.5, 2), (13.5, 7.5), (21.5, 5)], r=S.r * 0.4)), dot(12.25, 8.25, 1.5)]


@icon("ham-stand", CAT, "Ham stand: a board with a clamp holding a whole cured ham leg at an angle",
      tags=["jamonero", "ham holder", "cured ham", "jamon", "prosciutto", "carving stand"], aliases=["jamonero"])
def _(S):
    ham = "M7 7.5C10 7.5 13 10.5 20 11V13C13 13.5 10 16.5 7 16.5A4.5 4.5 0 0 1 7 7.5Z"
    ham = mv(rot(ham, -32, 12, 12), -1.5, 0.5)
    return [shell(rect(2, 18.5, 20, 3, L(S, 0.5, 1.5))), shell(ham), line(seg(19.5, 18.5, 19.5, 4.5)),
            shell(rect(17.5, 2, 4, 3.5, L(S, 0, 1.25)))]


@icon("gnocchi-board", CAT, "Small ridged gnocchi board with a handle and a ridged gnocchi beside it",
      tags=["gnocchi paddle", "ridged board", "pasta tool", "gnocchi", "italian cooking"], aliases=["gnocchi-paddle"])
def _(S):
    return [shell(union(rect(2.5, 2.5, 13, 12.5, rr(S, 2)), rect(7.5, 14, 3, 8, L(S, 0, 1.5)))),
            detail(seg(2.5, 6, 15.5, 6)), detail(seg(2.5, 9, 15.5, 9)), detail(seg(2.5, 12, 15.5, 12)),
            shell(ellipse(18.5, 18.5, 3.5, 3) if S.name == "rounded" else rect(15, 15.5, 7, 6, 1.5)), detail(seg(18.5, 16.5, 18.5, 20.5))]


@icon("basting-mop", CAT, "Basting mop: a short handle ending in a small mop head of cotton strands",
      tags=["bbq mop", "sauce mop", "barbecue", "basting", "grilling", "smoker"], aliases=["bbq-mop"])
def _(S):
    top = 1.5
    d = "M7 11.5V4"
    for x in (9.5, 12, 14.5, 17):
        d += f"A1.25 1.25 0 0 1 {fmt(x)} 4" if S.name == "rounded" else f"L{fmt(x - 1.25)} {top + 1}L{fmt(x)} 4"
    d += "V11.5Z"
    return tilt([shell(d), detail(seg(9.5, 6, 9.5, 11.5)), detail(seg(14.5, 6, 14.5, 11.5)),
                 shell(rect(9.5, 11.5, 5, 2.5, L(S, 0, 1.25))), line(seg(12, 14, 12, 23))])


@icon("billy-can", CAT, "Billy can: a metal can hanging by its wire bail from a stick over a small fire",
      tags=["billy", "camp kettle", "campfire", "bushcraft", "camping", "outdoor cooking"])
def _(S):
    return [line(seg(2, 2.5, 22, 2.5)), shell(rect(6, 8.5, 12, 7, L(S, 0.5, 2))), detail(seg(6, 11, 18, 11)),
            line("M6 10C6 3.5 18 3.5 18 10"), shell(_flame(S, 12, 17.5, 6, 22.5))]


@icon("jam-pan", CAT, "Wide jam pan with flared sides, a pouring lip and a bail handle over the top",
      tags=["preserving pan", "maslin pan", "jam making", "preserves", "marmalade", "canning"],
      aliases=["preserving-pan"])
def _(S):
    pan = poly([(1.5, 9.5), (3.5, 11), (21.5, 11), (18, 20.5), (6, 20.5)], closed=True, r=S.r * 0.5)
    return [shell(pan, stroke_miterlimit="2"), line("M4 11C5 1.5 20 1.5 21 11"),
            detail("M5 14.5C7.5 13.5 9.5 15.5 12 14.5S16.5 13.5 19 14.5")]


@icon("garlic-keeper", CAT, "Terracotta garlic keeper with a lid and air holes beside a garlic bulb",
      tags=["garlic pot", "garlic storage", "terracotta", "garlic", "pantry"], aliases=["garlic-pot"])
def _(S):
    pot = union("M2 11H12.5V18C12.5 20 11.5 21.5 9.5 21.5H5C3 21.5 2 20 2 18Z", "M2.5 10C2.5 5.5 12 5.5 12 10Z",
                circle(7.25, 5, 1.5))
    bulb = "M19 12C19 13.5 22.5 15 22.5 18C22.5 20.5 21 21.5 19 21.5C17 21.5 15.5 20.5 15.5 18C15.5 15 19 13.5 19 12Z"
    return [shell(pot), detail(seg(2, 10.5, 12.5, 10.5)), dot(4.75, 16, 1), dot(7.25, 16, 1), dot(9.75, 16, 1),
            shell(bulb), detail("M19 16.5C18 18 18 20 19 21.5")]


@icon("order-spike", CAT, "Order spike: an upright metal spike on a base with paper tickets pierced on it",
      tags=["ticket spike", "spindle", "order ticket", "kitchen ticket", "receipt spike", "restaurant"],
      aliases=["ticket-spike"])
def _(S):
    ticket = rot(rect(4, 7.5, 16, 7, L(S, 0.5, 1.5)), -10, 12, 11)
    return [shell(ticket), shell(poly([(11, 8), (12, 1.5), (13, 8)], closed=True), stroke_miterlimit="2"),
            detail(seg(12, 8, 12, 14.5)), detail(seg(6.5, 10.5, 9.5, 10)), detail(seg(14.5, 12.5, 17.5, 12)),
            line(seg(12, 14.5, 12, 18.5)), shell(rect(5, 18.5, 14, 3, L(S, 0.5, 1.5)))]


@icon("restaurant-pager", CAT, "Round restaurant pager with a ring of small lights around its edge",
      tags=["guest pager", "buzzer", "coaster pager", "table ready", "waitlist", "food court"],
      aliases=["guest-pager"])
def _(S):
    out = [shell(circle(12, 12, 9.5)), detail(circle(12, 12, 2.5) if S.name == "rounded" else rect(9.5, 9.5, 5, 5))]
    for k in range(8):
        x, y = pt_on(12, 12, 6.25, -90 + k * 45)
        out.append(dot(x, y, 1))
    return out


@icon("hotel-pan", CAT, "Rectangular steel hotel pan with a wide flat rim lip",
      tags=["steam table pan", "gastronorm", "chafing pan", "catering pan", "buffet", "commercial kitchen"],
      aliases=["steam-table-pan", "gastronorm-pan"])
def _(S):
    pan = union(rect(2, 7, 20, 3.5, L(S, 0.5, 1.75)), poly([(4.5, 10), (19.5, 10), (18.5, 19), (5.5, 19)], closed=True, r=S.r * 0.6))
    return [shell(pan), detail(seg(4.5, 10.5, 19.5, 10.5)), detail(seg(7.5, 14.5, 16.5, 14.5))]


@icon("salad-bar", CAT, "Salad bar counter with food bins under a sloped glass sneeze guard",
      tags=["buffet", "sneeze guard", "self service", "salad", "food bar", "cafeteria"], aliases=["sneeze-guard"])
def _(S):
    out = [shell(rect(2, 14, 20, 7.5, rr(S, 2))), detail(seg(2, 17, 22, 17)),
           line(poly([(20, 14), (20, 3), (6, 8.5)], r=S.r))]
    for x in (6, 11, 16):
        mound = f"M{fmt(x - 2)} 14A2 2 0 0 1 {fmt(x + 2)} 14Z" if S.name == "rounded" else rect(x - 2, 11.75, 4, 2.25)
        out.append(hole(mound))
    return out


@icon("pot-filler-faucet", CAT, "Wall-mounted folding pot filler faucet reaching over a pot",
      tags=["pot filler", "wall faucet", "stove faucet", "tap", "kitchen plumbing", "faucet"],
      aliases=["pot-filler"])
def _(S):
    return [shell(rect(2, 2.5, 3, 6, L(S, 0, 1.5))), line(poly([(5, 5.5), (10, 5.5)])), dot(10.75, 5.5, 1.75),
            line(poly([(11.5, 5.5), (16, 5.5), (16, 8.5)], r=S.r)), dot(16, 11, 1),
            shell(rect(10, 13.5, 12, 8, rr(S, 2))), line(seg(7, 15.5, 10, 15.5))]


@icon("fry-scoop", CAT, "Wide flat fry scoop with a handle holding a fanned pile of fries",
      tags=["french fry scoop", "chip scoop", "fries", "fast food", "fry station", "bagging scoop"],
      aliases=["chip-scoop"])
def _(S):
    scoop = poly([(2.5, 15), (3.5, 20.5), (16.5, 20.5), (16.5, 11)], closed=True, r=S.r * 0.5)
    return [shell(scoop), line(poly([(16.5, 15), (21.5, 15), (21.5, 19.5)], r=S.r)),
            line(seg(6, 13.5, 3, 7)), line(seg(9.5, 12, 9.5, 3.5)), line(seg(13, 10.5, 15.5, 5.5))]


@icon("kitchen-twine", CAT, "Roll of kitchen twine with a centre hole, wound strands and a loose end trailing off",
      tags=["butcher's twine", "cooking string", "trussing", "string", "roast tying", "twine"],
      aliases=["butchers-twine"])
def _(S):
    body = "M3 6.5A6 2.5 0 0 1 15 6.5V17.5A6 2.5 0 0 1 3 17.5Z"
    return [shell(body), detail("M3 6.5A6 2.5 0 0 0 15 6.5"), dot(9, 6.5, 1),
            detail(seg(3, 11.5, 9, 18)), detail(seg(9, 10.5, 15, 16.5)),
            line("M15 11.5H17.5C21.5 11.5 21.5 16.5 19 17.5C17 18.5 18.5 21.5 21.5 21.5")]


@icon("baking-mat", CAT, "Silicone baking mat with printed circle guides and one end rolled up",
      tags=["silicone mat", "baking sheet liner", "macaron mat", "non-stick mat", "baking"],
      aliases=["silicone-baking-mat"])
def _(S):
    mat = union(rect(2, 5, 16, 14, L(S, 0.5, 2)), rect(16.5, 3.5, 5.5, 17, 2.75))
    return [shell(mat), detail(seg(16.5, 5, 16.5, 19)), dot(6.5, 9, 1.5), dot(12, 9, 1.5), dot(6.5, 15, 1.5), dot(12, 15, 1.5)]


@icon("tofu-press", CAT, "Tofu press: a frame with a spring pushing a plate down onto a block of tofu",
      tags=["tofu", "press", "vegan", "draining tofu", "bean curd", "kitchen gadget"])
def _(S):
    spring = poly([(12, 3), (8.5, 5), (15.5, 7.5), (12, 9.5)], r=S.r * 0.3)
    return [line(poly([(4, 19.5), (4, 3), (20, 3), (20, 19.5)], r=S.r)), line(spring), line(seg(6.5, 10.5, 17.5, 10.5)),
            shell(rect(7, 12.5, 10, 4.5, L(S, 0.5, 1.5))), shell(rect(2, 19.5, 20, 2.5, L(S, 0, 1.25)))]


@icon("wok-spatula", CAT, "Shovel-shaped wok spatula with a raised back lip on a long handle",
      tags=["wok chuan", "wok shovel", "stir fry spatula", "turner", "chinese cooking", "wok tool"],
      aliases=["wok-chuan"])
def _(S):
    blade = "M5 3.5C9 2 15 2 19 3.5L17 11C15 12.5 9 12.5 7 11Z"
    return tilt([shell(blade), detail("M7.5 8.75C10 10 14 10 16.5 8.75"), line(seg(12, 12.5, 12, 16.5)),
                 shell(rect(10.5, 16.5, 3, 7, L(S, 0, 1.5)))])


@icon("boiling-over", CAT, "Pot boiling over with foam spilling across the rim and down the side",
      tags=["boil over", "overflow", "spill", "pot", "boiling", "stovetop"])
def _(S):
    foam = union(circle(7, 7.5, 2.75), circle(12, 6.5, 3.25), circle(17, 7.5, 2.75), rect(4.25, 7, 15.5, 3.5),
                 rect(16, 8, 4, 9.5, 2))
    pot = rect(3.5, 9, 17, 12.5, rr(S, 3))
    pot = path_to_d(D(P(pot), U(P(foam), ST(foam, 8.0))))
    return [shell(foam), shell(pot)]


@icon("burnt-food", CAT, "Frying pan with a charred black lump and curls of smoke rising",
      tags=["burnt", "burned food", "overcooked", "charred", "smoke", "cooking fail"], aliases=["burned-food"])
def _(S):
    pan = "M2 15H15V16.5C15 19 13.5 20.5 11 20.5H6C3.5 20.5 2 19 2 16.5Z"
    return [shell(pan), shell(rect(15, 15.25, 7, 2.5, L(S, 0, 1.25))), solid("M4.5 14.5C4.5 10.5 12.5 10.5 12.5 14.5Z")] + steam(S, (6, 11), 8, 2)


@icon("quern", CAT, "Hand quern: two stacked round grinding stones with an upright handle",
      tags=["hand mill", "grindstone", "millstone", "grain mill", "grinding", "flour"], aliases=["hand-quern"])
def _(S):
    top = "M5 8A7 2.5 0 0 1 19 8V11.5A7 2.5 0 0 1 5 11.5Z"
    bottom = "M2.5 16A9.5 3 0 0 1 21.5 16V19A9.5 3 0 0 1 2.5 19Z"
    bottom = path_to_d(D(P(bottom), U(P(top), ST(top, 4.0))))
    return [shell(top), detail("M5 8A7 2.5 0 0 0 19 8"), shell(bottom), line(seg(16.5, 8.5, 16.5, 2))]


@icon("apple-peeler-machine", CAT, "Crank apple peeler clamped to a table with an apple on the spike and a curling peel",
      tags=["apple peeler", "apple corer", "crank peeler", "peeling machine", "apples", "kitchen gadget"],
      aliases=["apple-parer"])
def _(S):
    apple = "M17.5 7C19.5 5.5 22 6.5 22 9.5C22 12.5 20 14.5 17.5 14.5C15 14.5 13 12.5 13 9.5C13 6.5 15.5 5.5 17.5 7Z"
    return [line(poly([(2, 3.5), (4, 3.5), (4, 9.5), (13, 9.5)], r=S.r)), line(seg(8, 9.5, 8, 16.5)),
            shell(rect(4.5, 16.5, 7, 4.5, L(S, 0.5, 1.5))), line(seg(2, 18.75, 4.5, 18.75)),
            shell(apple), line(seg(17.5, 7, 18.5, 4)), line("M17 14.5C15 16.5 19 18 17.5 20C17 21 18 22 20 21.5")]


@icon("gummy-mold", CAT, "Silicone gummy mold tray with a row of bear-shaped cavities",
      tags=["gummy bear mold", "candy mold", "silicone mold", "gummies", "candy making", "jelly sweets"],
      aliases=["gummy-bear-mold"])
def _(S):
    out = [shell(rect(1.5, 5, 21, 14, rr(S, 3)))]
    for x in (6, 12, 18):
        bear = union(circle(x, 9.5, 1.75), circle(x - 1.4, 8.1, 0.9), circle(x + 1.4, 8.1, 0.9), ellipse(x, 14, 2.3, 2.8))
        out.append(hole(bear))
    return out


@icon("ginger-grater", CAT, "Round ceramic ginger grater from above covered with small spikes",
      tags=["oroshigane", "ceramic grater", "ginger", "wasabi grater", "japanese cooking", "grater"],
      aliases=["ceramic-grater"])
def _(S):
    out = [shell(circle(11, 12, 8.5) if S.name == "rounded" else circle(11, 12, 8.5)), shell(rect(19.5, 10.5, 2.5, 3, L(S, 0, 1.25)))]
    pts = [(11, 12)] + [pt_on(11, 12, 4, a) for a in range(-90, 270, 60)]
    for x, y in pts:
        out.append(dot(x, y, 1))
    return out


@icon("plastic-wrap", CAT, "Long box of plastic wrap with a serrated edge and a curling sheet of film pulled out",
      tags=["cling film", "cling wrap", "food wrap", "saran wrap", "film", "food storage"], aliases=["cling-film"])
def _(S):
    film = "M5 13C4 7 7 3 12 3H21.5C18.5 4.5 17.5 8 18.5 13Z"
    box = union(film, rect(2, 12.5, 20, 7, rr(S, 2)))
    teeth = poly([(2, 13), (4, 15), (6, 13), (8, 15), (10, 13), (12, 15), (14, 13), (16, 15), (18, 13), (20, 15), (22, 13)])
    return [shell(box), detail(teeth), detail(seg(9, 6.5, 8.5, 9.5))]


@icon("hob-bridge-zone", CAT, "Hob bridge zone: two cooking circles joined into one long oval zone",
      tags=["flex zone", "bridge element", "induction zone", "cooktop", "hob symbol", "griddle zone"],
      aliases=["flex-zone"])
def _(S):
    return [shell(rect(5.5, 2, 13, 20, L(S, 4, 6.5))), detail(circle(12, 7.75, 2.5)), detail(circle(12, 16.25, 2.5))]


@icon("pullman-pan", CAT, "Straight-sided Pullman loaf pan with its flat sliding lid partly pulled back",
      tags=["pain de mie pan", "sandwich loaf pan", "lidded loaf tin", "bread pan", "bakeware"],
      aliases=["pain-de-mie-pan"])
def _(S):
    return [shell(rect(2.5, 10, 15, 11.5, rr(S, 2))), shell(rect(7, 5.5, 15, 2.5, L(S, 0, 1.25))),
            line(seg(20, 8, 20, 10.5)), detail(seg(2.5, 13, 17.5, 13))]


@icon("angel-food-pan", CAT, "Tall straight-sided angel food tube pan with a centre tube rising above the rim",
      tags=["tube pan", "chiffon cake pan", "angel cake", "cake tin", "bakeware"], aliases=["tube-pan"])
def _(S):
    body = "M3 9A9 3 0 0 1 21 9V19A9 3 0 0 1 3 19Z"
    return [shell(body), detail("M3 9A9 3 0 0 0 21 9"), shell(rect(10.5, 2.5, 3, 7, L(S, 0, 1.5)))]


@icon("cheese-wire-slicer", CAT, "Cheese board with a hinged arm pressing a thin wire down through a block of cheese",
      tags=["cheese slicer", "wire cutter", "cheese board", "cheese cutter", "deli"], aliases=["cheese-wire"])
def _(S):
    return [shell(rect(2, 18, 20, 3.5, L(S, 0.5, 1.75))), shell(rect(3.5, 10.5, 9.5, 7.5, L(S, 0.5, 1.5))),
            dot(6.5, 14.5, 1), line(poly([(19.5, 18), (19.5, 15.5), (9.5, 5)], r=S.r)), dot(8.75, 4.25, 1.75),
            detail(seg(10, 10.5, 10, 18))]


@icon("spurtle", CAT, "Spurtle: a slim wooden stirring rod topped with a carved thistle-shaped knob",
      tags=["porridge stick", "scottish", "stirring rod", "oatmeal", "wooden spoon", "stirrer"],
      aliases=["porridge-stick"])
def _(S):
    knob = poly([(8.5, 11.5), (6.5, 6.5), (9.5, 7.5), (12, 1.5), (14.5, 7.5), (17.5, 6.5), (15.5, 11.5)], closed=True, r=S.r * 0.6)
    return tilt([shell(knob), shell(rect(10.75, 11, 2.5, 12, L(S, 0, 1.25)))])


@icon("food-ring", CAT, "Food ring standing on a plate with layered food stacked inside and a garnish on top",
      tags=["chef ring", "plating ring", "mousse ring", "stacked", "fine dining", "presentation", "cooking ring"],
      aliases=["chef-ring"])
def _(S):
    plate = "M2 17.5H22C21 20 19 21 16 21H8C5 21 3 20 2 17.5Z"
    return [shell(plate), shell(rect(6, 7, 12, 10.5, rr(S, 1.5))), detail(seg(6, 12.25, 18, 12.25)),
            dot(12, 3.75, 1.5)]


