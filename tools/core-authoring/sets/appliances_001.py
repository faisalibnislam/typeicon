"""TypeIcon Core: appliances (batch appliances_001): kitchen, climate and household appliances.

Original drawings of generic appliances seen from the front (or the side where the profile identifies
them). Bodies are shells; doors, windows, handles and control strips are details so the Filled style
knocks them out. Knobs and indicator lights are small dots.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import LINE, I, fmt, path_to_d, polar

CAT = "appliances"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    """Container corner radius for the style, optionally capped for small shapes."""
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def mark(d) -> Part:
    """Small solid shape: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def layered(draw, gap=1.5):
    """Filled override where later shells sit in front of earlier ones, separated by a `gap` px counter.

    Otherwise follows the standard Filled rules (details and dots knock out, lines get heavier)."""
    def filled():
        from dsl import HEAVY, KNOCK
        parts = draw(LINE)
        body = None
        for p in parts:
            if p.kind != "shell":
                continue
            region = U(P(p.d), ST(p.d, 2.0, "butt", "miter"))
            body = region if body is None else U(D(body, U(P(p.d), ST(p.d, 2.0 + 2 * gap, "round", "round"))), region)
        extras = []
        for p in parts:
            if p.kind == "detail":
                region = ST(p.d, KNOCK, "butt", "miter")
                if body is not None and abs(I(region, body).area) >= 0.5 * abs(region.area):
                    body = D(body, region)
                else:
                    extras.append(ST(p.d, HEAVY, "butt", "miter"))
            elif p.kind == "dot":
                region = P(p.d)
                if body is not None and abs(I(region, body).area) >= 0.5 * abs(region.area):
                    body = D(body, region)
                else:
                    extras.append(region)
            elif p.kind == "line":
                extras.append(ST(p.d, HEAVY, "butt", "miter"))
            elif p.kind == "solid":
                extras.append(P(p.d))
        return U(*([body] if body is not None else []), *extras)
    return filled


def flame(cx, top, bottom, w):
    """Small teardrop flame with a pointed top and a round base."""
    my = bottom - w / 2
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + w * 0.35)} {fmt(top + (my - top) * 0.45)} {fmt(cx + w / 2)} {fmt(my - (my - top) * 0.25)} "
            f"{fmt(cx + w / 2)} {fmt(my)}A{fmt(w / 2)} {fmt(w / 2)} 0 0 1 {fmt(cx - w / 2)} {fmt(my)}"
            f"C{fmt(cx - w / 2)} {fmt(my - (my - top) * 0.25)} {fmt(cx - w * 0.35)} {fmt(top + (my - top) * 0.45)} {fmt(cx)} {fmt(top)}Z")


def fire(cx, top, bottom, w):
    """Flame with a round base, a tip leaning right and a small lick cut into its left side."""
    h = bottom - top
    X = lambda u: fmt(cx - w / 2 + u * w)
    Y = lambda v: fmt(top + v * h)
    return (f"M{X(0.55)} {Y(0)}C{X(0.62)} {Y(0.2)} {X(1)} {Y(0.38)} {X(1)} {Y(0.66)}"
            f"C{X(1)} {Y(0.88)} {X(0.78)} {Y(1)} {X(0.5)} {Y(1)}C{X(0.22)} {Y(1)} {X(0)} {Y(0.88)} {X(0)} {Y(0.66)}"
            f"C{X(0)} {Y(0.5)} {X(0.1)} {Y(0.38)} {X(0.25)} {Y(0.28)}C{X(0.28)} {Y(0.42)} {X(0.36)} {Y(0.5)} {X(0.46)} {Y(0.52)}"
            f"C{X(0.4)} {Y(0.34)} {X(0.44)} {Y(0.14)} {X(0.55)} {Y(0)}Z")


def spiral(cx, cy, r0, r1, turns, a0=-90.0, n=48):
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append(polar(cx, cy, r0 + (r1 - r0) * t, a0 + 360 * turns * t))
    return pts


def wave(x, y0, y1, amp=1.2):
    """Gentle vertical heat wave from y0 up to y1 (one S bend)."""
    h = y0 - y1
    return f"M{fmt(x)} {fmt(y0)}C{fmt(x - amp)} {fmt(y0 - h * 0.35)} {fmt(x + amp)} {fmt(y1 + h * 0.35)} {fmt(x)} {fmt(y1)}"


def hwave(y, x0, x1, amp=1.2):
    """Gentle horizontal wave from x0 to x1 (one S bend)."""
    w = x1 - x0
    return f"M{fmt(x0)} {fmt(y)}C{fmt(x0 + w * 0.35)} {fmt(y - amp)} {fmt(x1 - w * 0.35)} {fmt(y + amp)} {fmt(x1)} {fmt(y)}"


# ============================================================================ refrigeration

@icon("french-door-fridge", CAT, "French door fridge with two upper doors and a pull-out freezer drawer",
      tags=["refrigerator", "fridge", "french door", "freezer drawer", "kitchen", "appliance"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 3))),
        detail(seg(4, 15, 20, 15)),
        detail(seg(12, 2.5, 12, 15)),
        detail(seg(9.5, 5, 9.5, 12)), detail(seg(14.5, 5, 14.5, 12)),
        detail(seg(7, 18.5, 17, 18.5)),
    ]


@icon("side-by-side-fridge", CAT, "Side-by-side fridge freezer with two full-height doors and long handles",
      tags=["refrigerator", "fridge freezer", "american fridge", "double door", "kitchen", "appliance"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, rr(S, 3))),
        detail(seg(11, 2.5, 11, 21.5)),
        detail(seg(7.5, 7, 7.5, 16)), detail(seg(14.5, 7, 14.5, 16)),
    ]


@icon("mini-fridge", CAT, "Small cube fridge on short feet with a single door, a side handle and a freezer box",
      tags=["bar fridge", "compact fridge", "dorm fridge", "minibar", "cooler", "appliance"])
def _(S):
    return [
        shell(rect(5, 4, 14, 14, rr(S, 3))),
        detail(rect(10.5, 7, 5.5, 3, L(S, 0, 1))),
        detail(seg(8, 7.5, 8, 14.5)),
        line(seg(7.5, 18, 7.5, 21)), line(seg(16.5, 18, 16.5, 21)),
    ]


@icon("chest-freezer", CAT, "Chest freezer with a hinged lid and a snowflake on the front",
      tags=["deep freezer", "freezer", "chest", "frozen food", "cold storage", "appliance"])
def _(S):
    body = poly([(5, 4), (19, 4), (22, 8.5), (22, 20.5), (2, 20.5), (2, 8.5)], closed=True, r=S.r)
    c = (12, 16)
    flake = detail("".join(seg(*polar(*c, 2.75, a), *polar(*c, 2.75, a + 180)) for a in (90, 30, 150)))
    return [
        shell(body),
        detail(seg(2, 8.5, 22, 8.5)),
        detail(seg(2, 11.5, 22, 11.5)),
        flake,
    ]


@icon("ice-maker", CAT, "Countertop ice maker with a lift lid and ice cubes behind a front window",
      tags=["ice machine", "ice cubes", "countertop", "cold drinks", "bar", "appliance"])
def _(S):
    def cube(cx, cy, h=1.9):
        return mark(poly([(cx, cy - h), (cx + h, cy), (cx, cy + h), (cx - h, cy)], closed=True, r=L(S, 0, 0.5)))
    return [
        shell(rect(3.5, 2.5, 17, 19, rr(S, 3))),
        detail(seg(3.5, 7, 20.5, 7)),
        detail(rect(6.5, 10, 11, 8.5, rr(S, 1.5))),
        cube(9.6, 15.4), cube(14.4, 15.4), cube(12, 12.9),
    ]


# ============================================================================ cooking: hoods, hobs, ovens

@icon("range-hood", CAT, "Chimney cooker hood: a narrow duct widening into a canopy with lights underneath",
      tags=["extractor hood", "cooker hood", "vent hood", "exhaust", "kitchen", "appliance"])
def _(S):
    hood = poly([(9.5, 2), (14.5, 2), (14.5, 8.5), (21, 14), (21, 19), (3, 19), (3, 14), (9.5, 8.5)], closed=True, r=S.r)
    return [
        shell(hood),
        detail(seg(3, 14, 21, 14)),
        dot(8, 16.5, 1), dot(16, 16.5, 1),
    ]


@icon("induction-hob", CAT, "Top view of a glass induction hob with four plain cooking rings and touch controls",
      tags=["induction cooktop", "hob", "cooktop", "electric hob", "stovetop", "kitchen"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        detail(circle(8, 8, 3)), detail(circle(16.5, 7.5, 2)),
        detail(circle(7.5, 15, 2)), detail(circle(15.5, 14.5, 2.5)),
        dot(12, 18.75, 0.9),
    ]


@icon("gas-hob", CAT, "Top view of a gas hob with burners under cross pan supports and a row of knobs",
      tags=["gas cooktop", "hob", "burners", "stovetop", "gas stove", "kitchen"])
def _(S):
    parts = [shell(rect(2, 2.5, 20, 18.5, rr(S, 3)))]
    for cx in (7.25, 16.75):
        cy = 9
        parts += [detail(circle(cx, cy, 3) + seg(cx - 3, cy, cx + 3, cy) + seg(cx, cy - 3, cx, cy + 3))]
    parts += [dot(x, 17, 1) for x in (6, 10, 14, 18)]
    return parts


@icon("range-cooker", CAT, "Wide range cooker with knobs over two side-by-side oven doors",
      tags=["range", "cooker", "stove", "freestanding oven", "double oven", "kitchen"])
def _(S):
    return [
        line(poly([(5, 5.5), (5, 3.5), (9, 3.5), (9, 5.5)], r=S.r * 0.5)),
        line(poly([(15, 5.5), (15, 3.5), (19, 3.5), (19, 5.5)], r=S.r * 0.5)),
        shell(rect(2, 5.5, 20, 15.5, rr(S, 2.5))),
        dot(5.5, 8.5, 1), dot(9.5, 8.5, 1), dot(14.5, 8.5, 1), dot(18.5, 8.5, 1),
        detail(seg(12, 11.5, 12, 21)),
        detail(rect(4.5, 13.5, 5, 4.5, rr(S, 1))), detail(rect(14.5, 13.5, 5, 4.5, rr(S, 1))),
    ]


@icon("wall-oven", CAT, "Built-in wall oven with a control panel, a handle bar and a door window",
      tags=["built-in oven", "oven", "single oven", "baking", "kitchen", "appliance"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 3))),
        detail(seg(3, 7, 21, 7)),
        sq(9.5, 4, 5, 1.5, L(S, 0, 0.75)),
        detail(seg(7, 10.5, 17, 10.5)),
        detail(rect(6.5, 13.5, 11, 5, rr(S, 1.5))),
    ]


@icon("double-oven", CAT, "Built-in double oven with two stacked doors, each with a large window",
      tags=["two ovens", "oven", "built-in oven", "baking", "kitchen", "appliance"])
def _(S):
    return [
        shell(rect(4, 2, 16, 20, rr(S, 3))),
        detail(seg(4, 12, 20, 12)),
        detail(seg(7, 5, 17, 5)), sq(7, 7.5, 10, 2.5, L(S, 0, 1)),
        detail(seg(7, 15, 17, 15)), sq(7, 17.5, 10, 2.5, L(S, 0, 1)),
    ]


# ============================================================================ waste

@icon("trash-compactor", CAT, "Trash compactor cabinet with a press plate pushed down by an arrow over a pull-out drawer",
      tags=["compactor", "rubbish", "garbage", "waste", "crusher", "kitchen"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 3))),
        detail(seg(12, 5, 12, 9.5)),
        detail(poly([(9.5, 7.5), (12, 10), (14.5, 7.5)], r=S.r * 0.4)),
        detail(seg(8, 11.5, 16, 11.5)),
        detail(seg(5, 14.5, 19, 14.5)),
        detail(seg(9.5, 18, 14.5, 18)),
    ]


@icon("garbage-disposal", CAT, "Waste disposal unit hanging under a sink drain with a side outlet pipe",
      tags=["waste disposer", "food waste", "sink", "disposal unit", "kitchen", "plumbing"])
def _(S):
    return [
        line(seg(3, 3, 21, 3) if S.name == "line" else seg(4, 3, 20, 3)),
        line(seg(12, 3, 12, 6)),
        shell(rect(7, 6, 10, 15.5, rr(S, 3))),
        line(poly([(17, 11), (20, 11), (20, 15)], r=S.r)),
        detail(seg(7, 9.5, 17, 9.5)),
        dot(12, 17.5, 1.25),
    ]


# ============================================================================ mixers and blenders

def _stand_mixer(S):
    if S.name == "line":
        frame = "M3.5 21.5H21V19H9.5V9H18.5C20 9 21 8 21 6.5C21 4.5 19.5 3 17 3H9C5.5 3 3.5 5 3.5 8.5Z"
    else:
        frame = ("M5 21.5H19.75A1.25 1.25 0 0 0 21 20.25A1.25 1.25 0 0 0 19.75 19H9.5V9H18.5C20 9 21 8 21 6.5"
                 "C21 4.5 19.5 3 17 3H9C5.5 3 3.5 5 3.5 8.5V20A1.5 1.5 0 0 0 5 21.5Z")
    bowl = "M11 12H20.5C20.5 15.5 18.5 18 15.75 18C13 18 11 15.5 11 12Z"
    return [
        shell(frame),
        shell(bowl),
        line(seg(15.75, 9, 15.75, 13)),
    ]


icon("stand-mixer", CAT, "Stand mixer in side view with its head arm over a bowl and the beater in it",
     tags=["kitchen mixer", "mixer", "baking", "dough", "whisk", "appliance"], filled=layered(_stand_mixer))(_stand_mixer)


@icon("hand-mixer", CAT, "Handheld electric mixer with a looped handle and two whisk beaters",
      tags=["electric whisk", "hand whisk", "beater", "mixer", "baking", "appliance"])
def _(S):
    def whisk(x):
        return line(f"M{fmt(x)} 13.5V15C{fmt(x - 2.6)} 16 {fmt(x - 2.4)} 21.5 {fmt(x)} 21.5"
                    f"C{fmt(x + 2.4)} 21.5 {fmt(x + 2.6)} 16 {fmt(x)} 15")
    body = ("M4.5 9H16C19 9 21 10.2 21 11.25C21 12.3 19 13.5 16 13.5H4.5C3.4 13.5 3 12.8 3 11.25C3 9.7 3.4 9 4.5 9Z"
            if S.name == "rounded" else "M3 9H16C19 9 21 10.2 21 11.25C21 12.3 19 13.5 16 13.5H3Z")
    return [
        line(poly([(5.5, 9), (5.5, 4), (15, 4), (15, 9)], r=S.r)),
        shell(body),
        whisk(9), whisk(15.5),
    ]


@icon("immersion-blender", CAT, "Stick blender with a rounded handle, a long wand and a bell-shaped blade guard",
      tags=["hand blender", "stick blender", "wand blender", "puree", "soup", "appliance"])
def _(S):
    guard = ("M7 21.5C7 17.8 9.2 16 12 16C14.8 16 17 17.8 17 21.5Z" if S.name == "line" else
             "M8.5 21.5A1.5 1.5 0 0 1 7 20C7.3 17.4 9.4 16 12 16C14.6 16 16.7 17.4 17 20A1.5 1.5 0 0 1 15.5 21.5Z")
    return [
        shell(rect(9, 2, 6, 9.5, rr(S, 3))),
        dot(12, 5.25, 1.1),
        line(seg(12, 11.5, 12, 16)),
        shell(guard),
    ]


# ============================================================================ processors and juicers

@icon("food-processor", CAT, "Food processor with a motor base, a wide bowl with a lid and a tall feed tube",
      tags=["processor", "chopper", "slicer", "blender", "food prep", "appliance"])
def _(S):
    body = poly([(6, 7.5), (12.5, 7.5), (12.5, 3), (16.5, 3), (16.5, 7.5), (18, 7.5), (17, 15.5), (20, 15.5),
                 (20, 21.5), (4, 21.5), (4, 15.5), (7, 15.5)], closed=True, r=S.r * 0.6)
    return [
        shell(body),
        detail(seg(7, 15.5, 17, 15.5)),
        detail(seg(6.5, 10.5, 17.5, 10.5)),
        dot(12, 18.5, 1.25),
    ]


@icon("juicer", CAT, "Centrifugal juicer with a domed top and feed chute, pouring juice into a jug",
      tags=["juice extractor", "juice", "fruit", "smoothie", "fresh juice", "appliance"])
def _(S):
    if S.name == "line":
        body = "M2.5 21V14.5C2.5 11.5 5 9.5 8.25 9.5C11.5 9.5 14 11.5 14 14.5V21Z"
    else:
        body = "M4 21A1.5 1.5 0 0 1 2.5 19.5V14.5C2.5 11.5 5 9.5 8.25 9.5C11.5 9.5 14 11.5 14 14.5V19.5A1.5 1.5 0 0 1 12.5 21Z"
    return [
        shell(rect(6.25, 3, 4, 6.5, rr(S, 1))),
        shell(body),
        detail(seg(2.5, 15, 14, 15)),
        line(poly([(14, 12.5), (18.5, 12.5), (18.5, 14)], r=S.r * 0.5)),
        shell(rect(16.5, 16, 4.5, 5.5, rr(S, 1))),
    ]


# ============================================================================ electric pots and cookers

@icon("slow-cooker", CAT, "Slow cooker with a domed lid and knob, two side handles and a dial on the base",
      tags=["stew pot", "stew", "casserole", "one pot", "appliance"])
def _(S):
    k = L(S, 0, 3)
    body = (f"M4 11C4 7.5 7.5 6 12 6C16.5 6 20 7.5 20 11V{fmt(20.5 - k)}"
            + (f"A{k} {k} 0 0 1 {fmt(20 - k)} 20.5" if k else "")
            + f"H{fmt(4 + k)}" + (f"A{k} {k} 0 0 1 4 {fmt(20.5 - k)}" if k else "") + "Z")
    return [
        shell(rect(10.5, 3, 3, 3, L(S, 0, 1))),
        shell(body),
        detail(seg(4, 11, 20, 11)),
        line(seg(2, 13, 4, 13)), line(seg(20, 13, 22, 13)),
        dot(12, 15.75, 1.25),
    ]


@icon("pressure-cooker", CAT, "Pressure cooker with a locking lid, a long side handle and a valve on top",
      tags=["pressure pot", "electric pot", "cooker", "steam", "stew", "kitchen"])
def _(S):
    body = poly([(2, 8), (18, 8), (18, 11), (16.5, 11), (16.5, 21), (3.5, 21), (3.5, 11), (2, 11)], closed=True, r=S.r * 0.6)
    return [
        shell(body),
        detail(seg(3.5, 11, 16.5, 11)),
        line(seg(18, 9.5, 22, 9.5)),
        line(seg(10, 4.5, 10, 8)),
        shell(rect(8, 2.5, 4, 2, L(S, 0, 1))),
    ]


@icon("multicooker", CAT, "Electric multicooker with a hinged lid, a steam vent on top and a digital display",
      tags=["multi cooker", "electric pressure cooker", "slow cooker", "programmable cooker", "one pot", "appliance"])
def _(S):
    k = L(S, 1.5, 3.5)
    body = (f"M3 9C3 6 6 4.5 12 4.5C18 4.5 21 6 21 9V{fmt(21 - k)}A{k} {k} 0 0 1 {fmt(21 - k)} 21"
            f"H{fmt(3 + k)}A{k} {k} 0 0 1 3 {fmt(21 - k)}Z")
    return [
        shell(body),
        sq(14, 2, 3, 2.5, L(S, 0, 1)),
        detail(seg(3, 9.5, 21, 9.5)),
        detail(rect(8.5, 13, 7, 4, L(S, 0, 1.5))),
    ]


@icon("rice-cooker", CAT, "Rice cooker with a domed lid, a steam vent and a lever switch on the front",
      tags=["rice steamer", "rice", "cooker", "steam", "asian cooking", "appliance"])
def _(S):
    k = L(S, 0, 2.5)
    body = (f"M3 12C3 8 6.5 5.5 12 5.5C17.5 5.5 21 8 21 12V{fmt(19 - k)}"
            + (f"A{k} {k} 0 0 1 {fmt(21 - k)} 19" if k else "")
            + f"H{fmt(3 + k)}" + (f"A{k} {k} 0 0 1 3 {fmt(19 - k)}" if k else "") + "Z")
    return [
        shell(body),
        dot(12, 8.75, 1.1),
        detail(seg(3, 12, 21, 12)),
        detail(seg(12, 14.5, 12, 16.5)),
        line(seg(6, 19, 6, 21)), line(seg(18, 19, 18, 21)),
    ]


# ============================================================================ fryers, presses and ovens

@icon("air-fryer", CAT, "Air fryer with a dial on top and a pull-out basket drawer with a handle",
      tags=["airfryer", "fryer", "oil free", "crispy", "basket", "appliance"])
def _(S):
    body = poly([(6.5, 2.5), (17.5, 2.5), (20, 21.5), (4, 21.5)], closed=True, r=L(S, 1, 4))
    return [
        shell(body),
        detail(circle(12, 7.25, 2.25)),
        detail(seg(5.1, 12.5, 18.9, 12.5)),
        detail(seg(9, 16.5, 15, 16.5)),
    ]


@icon("deep-fryer", CAT, "Deep fat fryer with a lid window, a basket handle out the side and a thermostat knob",
      tags=["deep fat fryer", "chip pan", "fryer", "frying", "fries", "appliance"])
def _(S):
    body = poly([(4.5, 4), (14.5, 4), (15.5, 8.5), (16.5, 8.5), (16.5, 21), (2.5, 21), (2.5, 8.5), (3.5, 8.5)],
                closed=True, r=S.r * 0.6)
    return [
        shell(body),
        detail(seg(3.5, 8.5, 15.5, 8.5)),
        sq(6.5, 5.5, 6, 1.5, L(S, 0, 0.75)),
        line(poly([(16.5, 12), (19.5, 12), (21.5, 9)], r=S.r * 0.5)),
        detail(seg(2.5, 12, 16.5, 12)),
        detail("M5.5 16.5C6.75 15.3 8 15.3 9.5 16.5S12.25 17.7 13.5 16.5"),
    ]


@icon("sandwich-maker", CAT, "Closed sandwich toaster with two triangle plates on the lid over its base",
      tags=["toastie maker", "sandwich toaster", "panini press", "toasted sandwich", "snack", "appliance"])
def _(S):
    k = L(S, 0, 0.8)
    return [
        shell(rect(2, 2.5, 20, 16, rr(S, 3))),
        mark(poly([(6, 6), (16, 6), (6, 13.5)], closed=True, r=k)),
        mark(poly([(18, 8), (18, 15.5), (8, 15.5)], closed=True, r=k)),
        line(seg(4, 21, 20, 21) if S.name == "line" else seg(4.5, 21, 19.5, 21)),
    ]


@icon("waffle-iron", CAT, "Waffle iron seen from above: a round gridded plate in a square body with a side handle",
      tags=["waffle maker", "waffles", "breakfast", "belgian waffle", "griddle", "appliance"])
def _(S):
    c = (10.5, 12)
    r = 5.5
    grid = ""
    for o in (-2, 2):
        h = math.sqrt(r * r - o * o) - 0.2
        grid += seg(c[0] + o, c[1] - h, c[0] + o, c[1] + h) + seg(c[0] - h, c[1] + o, c[0] + h, c[1] + o)
    return [
        shell(rect(2, 3.5, 17, 17, rr(S, 4))),
        detail(circle(*c, r)),
        detail(grid),
        line(seg(19, 12, 22, 12) if S.name == "line" else seg(19, 12, 21.5, 12)),
    ]


@icon("toaster-oven", CAT, "Toaster oven on short feet with a glass door showing a rack and two dials",
      tags=["mini oven", "countertop oven", "toaster", "grill", "bake", "appliance"])
def _(S):
    return [
        shell(rect(2, 5, 20, 13, rr(S, 2.5))),
        detail(rect(4.5, 7.5, 10.5, 8, rr(S, 1.5))),
        detail(seg(4.5, 11.5, 15, 11.5)),
        dot(18.5, 9, 1.25), dot(18.5, 13.5, 1.25),
        line(seg(5, 18, 5, 20)), line(seg(19, 18, 19, 20)),
    ]


@icon("bread-maker", CAT, "Bread maker with a loaf in the lid window and control buttons on the front",
      tags=["breadmaker", "bread machine", "baking", "loaf", "dough", "appliance"])
def _(S):
    loaf = ("M7.5 13V9.5C7.5 7.5 9.3 6.5 12 6.5C14.7 6.5 16.5 7.5 16.5 9.5V13Z" if S.name == "line" else
            "M8.5 13A1 1 0 0 1 7.5 12V9.5C7.5 7.5 9.3 6.5 12 6.5C14.7 6.5 16.5 7.5 16.5 9.5V12A1 1 0 0 1 15.5 13Z")
    return [
        shell(rect(3.5, 2.5, 17, 19, rr(S, 3))),
        detail(loaf),
        detail(seg(3.5, 16, 20.5, 16)),
        dot(8, 18.75, 1), dot(12, 18.75, 1), dot(16, 18.75, 1),
    ]


@icon("egg-cooker", CAT, "Egg cooker: three eggs standing in a tray under a clear dome lid",
      tags=["egg boiler", "boiled eggs", "egg steamer", "breakfast", "eggs", "appliance"])
def _(S):
    def egg(cx, top, bottom=16, rx=1.9):
        return solid(f"M{fmt(cx - rx)} {fmt(bottom)}V{fmt(top + rx * 1.3)}C{fmt(cx - rx)} {fmt(top + 0.4)} {fmt(cx - rx * 0.6)} {fmt(top)} {fmt(cx)} {fmt(top)}"
                     f"C{fmt(cx + rx * 0.6)} {fmt(top)} {fmt(cx + rx)} {fmt(top + 0.4)} {fmt(cx + rx)} {fmt(top + rx * 1.3)}V{fmt(bottom)}Z")
    dome = "M3 16A9 8.5 0 0 1 21 16"
    return [
        line(dome),
        egg(7.25, 12.25), egg(12, 10.5), egg(16.75, 12.25),
        shell(rect(2, 16, 20, 5, rr(S, 2.5))),
    ]


def _coffee_maker(S):
    frame = poly([(3, 2.5), (21, 2.5), (21, 7.5), (9, 7.5), (9, 19), (21, 19), (21, 21.5), (3, 21.5)], closed=True, r=S.r)
    return [
        shell(frame),
        shell(poly([(11.5, 11), (16.5, 11), (17.5, 18.5), (10.5, 18.5)], closed=True, r=S.r * 0.6)),
        line(poly([(17, 12.5), (19.5, 12.5), (19.5, 16.5)], r=S.r * 0.5)),
        detail(seg(11, 14.75, 17, 14.75)),
    ]


icon("coffee-maker", CAT, "Drip coffee maker with an overhanging filter head and a glass carafe on the hot plate",
     tags=["coffee machine", "drip coffee", "filter coffee", "carafe", "brew", "appliance"],
     filled=layered(_coffee_maker))(_coffee_maker)


# ============================================================================ griddles, plates and outdoor ovens

@icon("hot-plate", CAT, "Single electric hot plate with a coiled heating ring and a control knob",
      tags=["hotplate", "electric burner", "single burner", "portable hob", "coil", "appliance"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, rr(S, 3))),
        detail(circle(10, 12, 5)),
        dot(10, 12, 1.5),
        dot(18.5, 12, 1.25),
    ]


@icon("portable-gas-stove", CAT, "Portable camping gas stove with a flame over the pan support, a knob and a cartridge door",
      tags=["camping stove", "camp stove", "butane stove", "gas burner", "outdoor cooking", "appliance"])
def _(S):
    return [
        mark(fire(12, 2.5, 9, 4)),
        line(poly([(6.5, 13), (6.5, 10.5), (17.5, 10.5), (17.5, 13)], r=S.r * 0.5)),
        shell(rect(2, 13, 20, 8, rr(S, 2.5))),
        detail(rect(5, 15.5, 6, 3, L(S, 0, 1))),
        dot(17, 17, 1.25),
    ]


@icon("pizza-oven", CAT, "Dome pizza oven with an arched mouth, a fire inside and a chimney",
      tags=["wood fired oven", "brick oven", "pizza", "stone oven", "outdoor oven", "baking"])
def _(S):
    dome = ("M2.5 20.5V14C2.5 8.5 6.5 5 12 5C17.5 5 21.5 8.5 21.5 14V20.5Z" if S.name == "line" else
            "M4 20.5A1.5 1.5 0 0 1 2.5 19V14C2.5 8.5 6.5 5 12 5C17.5 5 21.5 8.5 21.5 14V19A1.5 1.5 0 0 1 20 20.5Z")
    return [
        line(seg(16, 2, 16, 5.5)),
        shell(dome),
        detail("M7.5 20.5V16.5A4.5 4.5 0 0 1 16.5 16.5V20.5"),
        mark(fire(12, 15.5, 20.5, 3)),
    ]


@icon("bbq-smoker", CAT, "Barrel smoker on a cart with a side firebox and a tall chimney",
      tags=["smoker", "offset smoker", "barbecue", "bbq", "grill", "slow smoking"], aliases=["offset-smoker"])
def _(S):
    return [
        line(seg(4.5, 7, 4.5, 2.5)),
        line(seg(3, 2.5, 6, 2.5) if S.name == "line" else seg(3.5, 2.5, 5.5, 2.5)),
        shell(rect(2.5, 7, 13, 8, 4)),
        detail(seg(2.5, 11, 15.5, 11)),
        shell(rect(17, 9, 4.5, 6, rr(S, 1.5))),
        line(seg(5, 15, 5, 21.5)), line(seg(13, 15, 13, 21.5)),
        line(seg(5, 18.5, 13, 18.5)),
    ]


@icon("popcorn-machine", CAT, "Popcorn cart with a roof, glass walls, a kettle hanging inside and popcorn at the bottom",
      tags=["popcorn maker", "popper", "cinema", "movie snack", "concession", "fairground"])
def _(S):
    body = poly([(6, 2.5), (18, 2.5), (21, 6.5), (20, 6.5), (20, 17), (4, 17), (4, 6.5), (3, 6.5)], closed=True, r=S.r * 0.6)
    corn = "M5 14.5A1.75 1.75 0 0 1 8.5 14.5A1.75 1.75 0 0 1 12 14.5A1.75 1.75 0 0 1 15.5 14.5A1.75 1.75 0 0 1 19 14.5"
    return [
        shell(body),
        detail(seg(4, 6.5, 20, 6.5)),
        detail("M9.5 8.5H14.5C14.5 10.2 13.4 11 12 11C10.6 11 9.5 10.2 9.5 8.5Z"),
        detail(corn),
        line(seg(6.5, 17, 6.5, 21)), line(seg(17.5, 17, 17.5, 21)),
    ]


@icon("food-dehydrator", CAT, "Round food dehydrator: a stack of four drying trays under a fan cap",
      tags=["dehydrator", "dryer", "dried fruit", "jerky", "drying trays", "appliance"])
def _(S):
    k = L(S, 0, 2.5)
    body = (f"M3 7H5C5 4.5 8 3 12 3C16 3 19 4.5 19 7H21V{fmt(21.5 - k)}"
            + (f"A{k} {k} 0 0 1 {fmt(21 - k)} 21.5" if k else "") + f"H{fmt(3 + k)}"
            + (f"A{k} {k} 0 0 1 3 {fmt(21.5 - k)}" if k else "") + "Z")
    return [
        shell(body),
        dot(12, 5.25, 0.9),
        detail(seg(5, 7, 19, 7)),
        detail(seg(3, 10.75, 21, 10.75)), detail(seg(3, 14.5, 21, 14.5)), detail(seg(3, 18.25, 21, 18.25)),
    ]


@icon("sous-vide-cooker", CAT, "Sous vide stick circulator standing in a pot of water with a display on its head",
      tags=["sous vide", "immersion circulator", "precision cooker", "water bath", "slow cooking", "appliance"])
def _(S):
    pot = ("M2.5 10V21H20.5V10" if S.name == "line" else "M2.5 10V19A2 2 0 0 0 4.5 21H18.5A2 2 0 0 0 20.5 19V10")
    stick = poly([(12, 2.5), (18, 2.5), (18, 7.5), (17, 7.5), (17, 18), (13, 18), (13, 7.5), (12, 7.5)], closed=True, r=S.r * 0.6)
    return [
        line(pot),
        shell(stick),
        detail(seg(13.5, 5, 16.5, 5)),
        line("M4.5 13C5.5 12 6.5 12 7.5 13S9.5 14 10.5 13"),
    ]


@icon("vacuum-sealer", CAT, "Long vacuum sealer machine with a sealed food bag hanging from its front slot",
      tags=["food sealer", "vacuum packer", "sous vide bag", "food storage", "seal", "appliance"])
def _(S):
    return [
        shell(rect(2, 3, 20, 7, rr(S, 2.5))),
        dot(16, 6.5, 1), dot(19, 6.5, 1),
        detail(seg(5, 6.5, 12, 6.5)),
        shell(rect(6, 12, 12, 9.5, rr(S, 2))),
        detail(seg(6, 14.5, 18, 14.5)),
        dot(12, 18, 1.5),
    ]


# ============================================================================ grinders, rollers and openers

@icon("meat-grinder", CAT, "Meat mincer in side view with a hopper tray, a barrel and minced strands coming out",
      tags=["mincer", "meat mincer", "grinder", "sausage", "mince", "butcher"])
def _(S):
    body = poly([(2.5, 3.5), (13, 3.5), (10.5, 8.5), (16, 8.5), (16, 15), (5, 15), (5, 8.5), (6, 8.5)],
                closed=True, r=S.r * 0.6)
    return [
        shell(body),
        line(seg(18, 7.5, 18, 16)),
        line("M20 10C21.5 11.5 21.5 13.5 20.5 15.5"),
        line(poly([(5, 12), (2.5, 12), (2.5, 17)], r=S.r * 0.5)),
        line(seg(10.5, 15, 10.5, 21)),
        line(seg(7, 21, 14, 21) if S.name == "line" else seg(7.5, 21, 13.5, 21)),
    ]


@icon("pasta-maker", CAT, "Pasta machine with a crank handle and strands of fresh pasta coming out underneath",
      tags=["pasta machine", "pasta roller", "fresh pasta", "dough", "noodles", "kitchen"])
def _(S):
    def strand(x):
        return line(f"M{fmt(x)} 14C{fmt(x - 1.2)} 16 {fmt(x + 1.2)} 18 {fmt(x)} 21.5")
    return [
        shell(rect(3, 3, 15, 11, rr(S, 2.5))),
        detail(seg(6, 8.5, 15, 8.5)),
        line(poly([(18, 8.5), (21.5, 8.5), (21.5, 4)], r=S.r * 0.5)),
        strand(6.5), strand(10.5), strand(14.5),
    ]


@icon("electric-can-opener", CAT, "Countertop electric can opener with a lever arm holding a can below",
      tags=["can opener", "tin opener", "canned food", "opener", "kitchen", "appliance"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 11.5, rr(S, 3))),
        detail(seg(8.5, 6, 15.5, 10)),
        dot(8.5, 10.25, 1),
        shell(rect(7.5, 15, 9, 6.5, rr(S, 1.5))),
        detail(seg(7.5, 17.5, 16.5, 17.5)),
    ]


# ============================================================================ weighing, steaming and fondue

def _kitchen_scale(S):
    return [
        shell("M3.5 6.5H20.5C20.5 10 17 12 12 12C7 12 3.5 10 3.5 6.5Z"),
        shell(rect(2.5, 14.5, 19, 7, rr(S, 2.5))),
        sq(8, 16.75, 8, 2.5, L(S, 0, 1)),
    ]


icon("kitchen-scale", CAT, "Digital kitchen scale with a display on the front and a mixing bowl on the platform",
     tags=["food scale", "weighing scale", "digital scale", "baking", "weigh", "grams"],
     filled=layered(_kitchen_scale))(_kitchen_scale)


@icon("food-steamer", CAT, "Electric food steamer: stacked baskets under a domed lid on a water base",
      tags=["steamer", "vegetable steamer", "steam cooking", "healthy cooking", "baskets", "appliance"])
def _(S):
    k = L(S, 0, 2)
    body = (f"M5 9C5 6 8 4.5 12 4.5C16 4.5 19 6 19 9V16H21V{fmt(21.5 - k)}"
            + (f"A{k} {k} 0 0 1 {fmt(21 - k)} 21.5" if k else "") + f"H{fmt(3 + k)}"
            + (f"A{k} {k} 0 0 1 3 {fmt(21.5 - k)}" if k else "") + "V16H5Z")
    return [
        sq(10.5, 2, 3, 2, L(S, 0, 1)),
        shell(body),
        detail(seg(5, 9, 19, 9)), detail(seg(5, 12.5, 19, 12.5)), detail(seg(5, 16, 19, 16)),
        dot(12, 18.75, 1),
    ]


@icon("fondue-pot", CAT, "Fondue pot on a stand over a small burner with two long forks in it",
      tags=["fondue", "cheese fondue", "chocolate fondue", "fondue set", "party", "swiss"])
def _(S):
    pot = ("M4.5 10H19.5V12C19.5 15.3 16.4 17 12 17C7.6 17 4.5 15.3 4.5 12Z" if S.name == "line" else
           "M6 10H18A1.5 1.5 0 0 1 19.5 11.5V12C19.5 15.3 16.4 17 12 17C7.6 17 4.5 15.3 4.5 12V11.5A1.5 1.5 0 0 1 6 10Z")
    return [
        line(seg(9, 10, 11.5, 3.5)), line(seg(13, 10, 18, 4)),
        dot(11.75, 3, 1.5), dot(18.4, 3.5, 1.5),
        shell(pot),
        line(seg(6.5, 15.5, 4.5, 21.5)), line(seg(17.5, 15.5, 19.5, 21.5)),
        mark(fire(12, 18, 21.5, 2.5)),
    ]


@icon("crepe-maker", CAT, "Crepe maker: a large round hot plate on a low base with a thin crepe spread on it",
      tags=["crepe", "crepe pan", "pancake maker", "galette", "french pancake", "appliance"])
def _(S):
    return [
        shell(rect(5, 15.5, 14, 5, L(S, 0.5, 2.5))),
        shell(ellipse(12, 11, 9.5, 4)),
        detail(ellipse(12, 11, 5.5, 1.5)),
        dot(12, 18, 1),
    ]


# ============================================================================ drinks and baby

def _bottle_warmer(S):
    k = L(S, 0, 0.75)
    bottle = poly([(8.5, 16.5), (8.5, 9.5), (7.5, 9.5), (7.5, 7), (16.5, 7), (16.5, 9.5), (15.5, 9.5), (15.5, 16.5)],
                  closed=True, r=k)
    teat = "M10.5 7C10.5 4.4 11.1 3 12 3C12.9 3 13.5 4.4 13.5 7"
    cup = poly([(4.5, 16.5), (19.5, 16.5), (18.5, 21.5), (5.5, 21.5)], closed=True, r=S.r * 0.6)
    return [
        line(teat),
        shell(bottle),
        shell(cup),
        dot(12, 19, 1),
    ]


icon("bottle-warmer", CAT, "Baby bottle warmer: a cup-shaped heater holding a bottle with a teat, with a dial on the front",
     tags=["baby bottle", "bottle heater", "baby milk", "formula", "infant", "nursery"],
     filled=layered(_bottle_warmer))(_bottle_warmer)


@icon("personal-blender", CAT, "Personal blender: an upside-down blending bottle locked onto a short motor base",
      tags=["single cup blender", "smoothie maker", "single serve blender", "protein shake", "blender", "appliance"])
def _(S):
    k = L(S, 1.5, 3.5)
    body = (f"M8 12.5V{fmt(2.5 + k)}A{k} {k} 0 0 1 {fmt(8 + k)} 2.5H{fmt(16 - k)}A{k} {k} 0 0 1 16 {fmt(2.5 + k)}"
            "V12.5H16.5V15.5L18.5 21.5H5.5L7.5 15.5V12.5Z")
    return [
        shell(body),
        detail(seg(8, 12.5, 16, 12.5)),
        detail(seg(7.5, 15.5, 16.5, 15.5)),
        dot(12, 18.5, 1),
    ]


@icon("hot-water-dispenser", CAT, "Electric thermo pot with a large push button on top and a spout at the front",
      tags=["thermo pot", "water boiler", "hot water pot", "air pot", "tea", "appliance"])
def _(S):
    return [
        shell(rect(8.5, 2.5, 5, 3, L(S, 0, 1.5))),
        shell(rect(4.5, 5.5, 13, 16, rr(S, 3))),
        detail(seg(4.5, 9, 17.5, 9)),
        line(poly([(17.5, 11), (20.5, 11), (20.5, 13.5)], r=S.r * 0.5)),
        detail(seg(8, 12.5, 8, 18)),
    ]


@icon("kitchen-timer", CAT, "Round twist kitchen timer with a pointer on top and the set time marked as a wedge",
      tags=["egg timer", "cooking timer", "wind up timer", "countdown", "minutes", "baking"])
def _(S):
    c = (12, 13)
    wedge = f"M12 13V8.5A4.5 4.5 0 0 1 {fmt(polar(*c, 4.5, 30)[0])} {fmt(polar(*c, 4.5, 30)[1])}Z"
    return [
        solid(poly([(9.5, 2), (14.5, 2), (12, 4.5)], closed=True, r=L(S, 0, 0.5))),
        shell(circle(*c, 8.5)),
        detail(wedge if S.name == "line" else poly([(12, 13), (12, 8.5), polar(*c, 4.5, -45), polar(*c, 4.5, 0), polar(*c, 4.5, 30)], closed=True, r=0.8)),
    ]


# ============================================================================ laundry and floor care

@icon("washer-dryer-stack", CAT, "Stacked washer and dryer: two machines one on top of the other, each with a round door",
      tags=["stacked washer dryer", "laundry", "washing machine", "tumble dryer", "utility room", "appliance"])
def _(S):
    return [
        shell(rect(5, 2, 14, 20, rr(S, 3))),
        detail(seg(5, 12, 19, 12)),
        dot(8, 4.75, 0.9), detail(circle(13, 7.25, 2.25)),
        dot(8, 14.75, 0.9), detail(circle(13, 17.25, 2.25)),
    ]


@icon("drying-rack", CAT, "Folding clothes airer with parallel rails on splayed legs and a towel hanging over the top",
      tags=["clothes airer", "clothes horse", "laundry rack", "drying clothes", "airer", "laundry"], aliases=["clothes-airer"])
def _(S):
    return [
        line(seg(2.5, 5, 9.5, 5)), line(seg(14.5, 5, 21.5, 5)),
        line(seg(2.5, 9, 7, 9)), line(seg(17, 9, 21.5, 9)),
        shell(rect(9.5, 5, 5, 10, L(S, 0, 1))),
        detail(seg(9.5, 12, 14.5, 12)),
        line(seg(4.5, 5, 3, 21.5)), line(seg(19.5, 5, 21, 21.5)),
    ]


@icon("floor-polisher", CAT, "Floor polisher with a round disc housing, a long handle and a grip bar",
      tags=["floor buffer", "floor scrubber", "polishing machine", "cleaning", "janitor", "floor care"])
def _(S):
    housing = ("M3 21V19.5C3 16.5 6.5 14.5 11 14.5C15.5 14.5 19 16.5 19 19.5V21Z" if S.name == "line" else
               "M4.5 21A1.5 1.5 0 0 1 3 19.5C3 16.5 6.5 14.5 11 14.5C15.5 14.5 19 16.5 19 19.5A1.5 1.5 0 0 1 17.5 21Z")
    return [
        line(seg(11, 14.5, 17, 4)),
        line(seg(14.5, 2.5, 20, 5.5) if S.name == "line" else seg(15, 2.8, 19.5, 5.3)),
        shell(housing),
    ]


# ============================================================================ cooling

@icon("portable-air-conditioner", CAT, "Portable air conditioner on castors with a top vent and an exhaust hose",
      tags=["portable ac", "mobile air conditioner", "cooling", "air con", "room cooler", "summer"])
def _(S):
    return [
        shell(rect(3, 2.5, 12, 17, rr(S, 3))),
        detail(seg(5.5, 6, 12.5, 6)), detail(seg(5.5, 9, 12.5, 9)),
        dot(9, 14.5, 1.25),
        line("M15 8C19 8 21 9.5 21 13V21"),
        dot(6, 21, 1.25), dot(12, 21, 1.25),
    ]


@icon("window-air-conditioner", CAT, "Window air conditioner unit sitting in a window frame with louvres and knobs",
      tags=["window ac", "window unit", "air con", "cooling", "room air conditioner", "summer"])
def _(S):
    return [
        line(poly([(2.5, 21.5), (2.5, 2.5), (21.5, 2.5), (21.5, 21.5)], r=S.r)),
        line(seg(2.5, 8, 21.5, 8)),
        shell(rect(5.5, 11, 13, 9, rr(S, 2))),
        detail(seg(8, 14, 13, 14)), detail(seg(8, 17, 13, 17)),
        dot(16, 14, 0.9), dot(16, 17, 0.9),
    ]


@icon("heat-pump", CAT, "Outdoor heat pump unit with a round fan grille, pipes out the side and warmth rising",
      tags=["air source heat pump", "outdoor unit", "hvac", "heating", "renewable heating", "compressor"])
def _(S):
    return [
        shell(rect(2.5, 8, 15, 13, rr(S, 2.5))),
        detail(circle(10, 14.5, 3.75)),
        dot(10, 14.5, 1.25),
        line(seg(17.5, 12, 21.5, 12)), line(seg(17.5, 16.5, 21.5, 16.5)),
        line(wave(6, 6, 2, 1.4)), line(wave(10, 6, 2, 1.4)), line(wave(14, 6, 2, 1.4)),
    ]


@icon("evaporative-cooler", CAT, "Evaporative air cooler with a front grille, a water tank window and water drops",
      tags=["swamp cooler", "air cooler", "water cooler fan", "desert cooler", "cooling", "humidifier"])
def _(S):
    return [
        shell(rect(3, 2.5, 13, 19, rr(S, 3))),
        detail(seg(5.5, 6, 13.5, 6)), detail(seg(5.5, 9, 13.5, 9)), detail(seg(5.5, 12, 13.5, 12)),
        detail(rect(6, 15, 7, 3.5, L(S, 0, 1))),
        mark(flame(19.5, 5.5, 11, 3)), mark(flame(19.5, 13, 18.5, 3)),
    ]


@icon("tower-fan", CAT, "Tall slim tower fan with a long vertical grille slot and a round base",
      tags=["column fan", "pillar fan", "oscillating fan", "cooling", "air circulator", "summer"])
def _(S):
    return [
        shell(rect(7.5, 2, 9, 16, rr(S, 3))),
        detail(rect(10.5, 5, 3, 10, L(S, 0, 1.5))),
        shell(rect(5.5, 19.5, 13, 2, 1 if S.name == "rounded" else 0)),
    ]


@icon("pedestal-fan", CAT, "Pedestal fan: a round bladed fan head on a tall pole with a round base",
      tags=["stand fan", "floor fan", "oscillating fan", "cooling", "electric fan", "summer"], aliases=["stand-fan"])
def _(S):
    c = (12, 8)
    spokes = "".join(seg(*c, *polar(*c, 4, a)) for a in (-90, 30, 150))
    return [
        shell(circle(*c, 6)),
        detail(spokes),
        line(seg(12, 14, 12, 20)),
        line(seg(7, 21, 17, 21) if S.name == "line" else seg(7.5, 21, 16.5, 21)),
    ]


def _spokes(cx, cy, r, start=-90):
    return "".join(seg(cx, cy, *polar(cx, cy, r, start + k * 120)) for k in range(3))


@icon("desk-fan", CAT, "Desk fan: a large round bladed head on a short neck and a flat base",
      tags=["table fan", "electric fan", "small fan", "cooling", "office fan", "summer"], aliases=["table-fan"])
def _(S):
    return [
        shell(circle(12, 9, 6.5)),
        detail(_spokes(12, 9, 4.5, -60)),
        line(seg(12, 15.5, 12, 18.5)),
        shell(rect(5.5, 18.5, 13, 2.5, L(S, 0, 1.25))),
    ]


@icon("box-fan", CAT, "Box fan: a square frame around a round bladed grille with a carry slot on top",
      tags=["square fan", "window fan", "floor fan", "cooling", "electric fan", "summer"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 3))),
        detail(seg(9.5, 5.5, 14.5, 5.5)),
        detail(circle(12, 13.5, 5)),
        detail(_spokes(12, 13.5, 3)),
    ]


@icon("bladeless-fan", CAT, "Bladeless fan: a tall open oval loop standing on a cylindrical base",
      tags=["bladeless", "loop fan", "ring fan", "cooling", "quiet fan", "modern fan"])
def _(S):
    return [
        line(ellipse(12, 8.5, 5.5, 6.5)),
        shell(rect(8.5, 15.5, 7, 6, L(S, 0.5, 2.5))),
        dot(12, 18.5, 1),
    ]


@icon("exhaust-fan", CAT, "Square wall extractor fan with a round opening and four propeller blades",
      tags=["extractor fan", "ventilation fan", "bathroom fan", "kitchen extractor", "vent", "airflow"], aliases=["extractor-fan"])
def _(S):
    c = (12, 12)
    blades = []
    for a in (45, 135, 225, 315):
        pts = [polar(*c, 1.2, a - 50), polar(*c, 5, a - 28), polar(*c, 5, a + 12), polar(*c, 1.2, a + 30)]
        blades.append(mark(poly(pts, closed=True, r=L(S, 0, 0.6))))
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        detail(circle(*c, 6.5)),
        *blades,
    ]


def _handheld_fan(S):
    return [
        shell(circle(12, 8.5, 6)),
        detail(_spokes(12, 8.5, 4)),
        shell(rect(10.25, 15, 3.5, 7, L(S, 0.5, 1.75))),
    ]


icon("handheld-fan", CAT, "Small battery handheld fan: a round bladed head on top of a vertical handle",
     tags=["mini fan", "portable fan", "personal fan", "usb fan", "cooling", "summer"],
     filled=layered(_handheld_fan, 1))(_handheld_fan)


# ============================================================================ heating

@icon("fan-heater", CAT, "Fan heater: a compact box with a round fan grille blowing out warm air",
      tags=["blow heater", "space heater", "electric heater", "warm air", "heating", "winter"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 13, 14, rr(S, 3))),
        detail(circle(9, 12.5, 3.75)),
        detail(_spokes(9, 12.5, 2.5)),
        line(hwave(8, 17.5, 21.5, 1.3)), line(hwave(12.5, 17.5, 21.5, 1.3)), line(hwave(17, 17.5, 21.5, 1.3)),
    ]


@icon("oil-filled-radiator", CAT, "Oil-filled radiator with rounded fins, castor feet and a control box on the end",
      tags=["oil heater", "column heater", "portable radiator", "electric radiator", "heating", "winter"])
def _(S):
    n, x0, w, top, bot = 4, 2.5, 3.5, 5.5, 15.5
    rr_ = w / 2
    d = f"M{fmt(x0)} {fmt(top)}"
    for k in range(n):
        d += f"A{fmt(rr_)} {fmt(rr_)} 0 0 1 {fmt(x0 + (k + 1) * w)} {fmt(top)}"
    d += f"V{fmt(bot)}"
    for k in range(n, 0, -1):
        d += f"A{fmt(rr_)} {fmt(rr_)} 0 0 1 {fmt(x0 + (k - 1) * w)} {fmt(bot)}"
    d += "Z"
    fins = "".join(seg(x0 + k * w, top, x0 + k * w, bot) for k in range(1, n))
    return [
        shell(d),
        detail(fins),
        shell(rect(18, 7.5, 3.5, 6, L(S, 0, 1.5))),
        dot(5.5, 20, 1.25), dot(13, 20, 1.25),
    ]


@icon("infrared-heater", CAT, "Infrared panel heater: a flat plain panel with heat waves radiating from its face",
      tags=["ir heater", "panel heater", "radiant heater", "wall heater", "heating", "infrared"])
def _(S):
    return [
        shell(rect(2.5, 3, 7, 18, rr(S, 2))),
        line(hwave(7, 13, 21.5, 1.4)), line(hwave(12, 13, 21.5, 1.4)), line(hwave(17, 13, 21.5, 1.4)),
    ]


@icon("patio-heater", CAT, "Patio heater: a tall pole with a wide round reflector hood on top and a gas bottle base",
      tags=["outdoor heater", "garden heater", "mushroom heater", "terrace heater", "gas heater", "heating"])
def _(S):
    return [
        shell(poly([(2.5, 7), (21.5, 7), (14, 3), (10, 3)], closed=True, r=S.r)),
        line(seg(12, 7, 12, 15.5)),
        line(wave(6.5, 13.5, 9.5, 1)), line(wave(17.5, 13.5, 9.5, 1)),
        shell(rect(8.5, 15.5, 7, 6, rr(S, 2))),
    ]


@icon("wood-stove", CAT, "Wood-burning stove on short legs with flames behind a glass door and a flue pipe",
      tags=["wood burner", "log burner", "woodstove", "fireplace", "heating", "cabin"], aliases=["log-burner"])
def _(S):
    body = poly([(3.5, 8), (12, 8), (12, 2), (16, 2), (16, 8), (19.5, 8), (19.5, 19), (3.5, 19)], closed=True, r=S.r * 0.6)
    return [
        shell(body),
        detail(rect(6.5, 10.75, 10, 5.5, rr(S, 1.5))),
        mark(fire(11.5, 11.5, 15.5, 2.75)),
        line(seg(5.5, 19, 5.5, 21.5)), line(seg(17.5, 19, 17.5, 21.5)),
    ]


@icon("storage-heater", CAT, "Night storage heater: a low wide box with an outlet grille along the top and two dials",
      tags=["night storage heater", "electric storage heater", "off peak heater", "heating", "radiator", "winter"])
def _(S):
    return [
        shell(rect(2, 6.5, 20, 13, rr(S, 2.5))),
        detail("".join(seg(x, 9, x, 11.5) for x in (5, 8, 11, 14, 17))),
        detail(seg(2, 14, 22, 14)),
        dot(15, 16.75, 1), dot(18.5, 16.75, 1),
        line(seg(4.5, 19.5, 4.5, 21.5)), line(seg(19.5, 19.5, 19.5, 21.5)),
    ]


@icon("kerosene-heater", CAT, "Round kerosene heater with a caged flame window and a carry handle",
      tags=["paraffin heater", "oil heater", "portable heater", "camping heater", "heating", "winter"], aliases=["paraffin-heater"])
def _(S):
    return [
        line("M8.5 7A3.5 3.5 0 0 1 15.5 7"),
        shell(rect(4.5, 7, 15, 14.5, rr(S, 3))),
        detail(seg(8.25, 9.5, 8.25, 15)), detail(seg(15.75, 9.5, 15.75, 15)),
        mark(fire(12, 9.5, 15, 3.25)),
        detail(seg(4.5, 17.5, 19.5, 17.5)),
    ]


@icon("underfloor-heating", CAT, "Underfloor heating: a looped heating pipe under the floor line with warmth rising",
      tags=["floor heating", "radiant floor", "heated floor", "hydronic heating", "heating", "home"])
def _(S):
    return [
        line(wave(7, 9.5, 3, 1.3)), line(wave(12, 9.5, 3, 1.3)), line(wave(17, 9.5, 3, 1.3)),
        line(seg(2, 12.5, 22, 12.5) if S.name == "line" else seg(2.5, 12.5, 21.5, 12.5)),
        line("M2.5 16H18.75A2.25 2.25 0 0 1 18.75 20.5H2.5"),
    ]


@icon("electric-blanket", CAT, "Electric blanket with a zigzag heating wire and a controller on its cord",
      tags=["heated blanket", "electric underblanket", "bed warmer", "warm bed", "heating", "winter"])
def _(S):
    return [
        shell(rect(2.5, 3, 13.5, 18, rr(S, 2.5))),
        detail(seg(2.5, 6.5, 16, 6.5)),
        detail(poly([(5.5, 18), (5.5, 9.5), (9.25, 9.5), (9.25, 18), (13, 18), (13, 9.5)], r=S.r)),
        line("M16 12H17.5C18.6 12 19.5 12.9 19.5 14V15"),
        shell(rect(17.5, 15, 4, 6.5, L(S, 0.5, 1.5))),
    ]


@icon("furnace", CAT, "Home furnace: a tall cabinet with a duct rising from the top and a flame in the lower panel",
      tags=["gas furnace", "forced air", "hvac", "central heating", "heating system", "basement"])
def _(S):
    body = poly([(4.5, 7), (8.5, 7), (8.5, 2), (15.5, 2), (15.5, 7), (19.5, 7), (19.5, 21.5), (4.5, 21.5)],
                closed=True, r=S.r * 0.6)
    return [
        shell(body),
        detail(seg(8, 9.75, 16, 9.75)),
        detail(seg(4.5, 12.5, 19.5, 12.5)),
        mark(fire(12, 14.5, 19.5, 3.5)),
    ]


@icon("boiler", CAT, "Wall-mounted boiler with a display, a dial and a flame on the front and pipes below",
      tags=["combi boiler", "gas boiler", "central heating", "hot water", "heating", "plumbing"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 14.5, rr(S, 3))),
        sq(7, 5.5, 10, 2.5, L(S, 0, 1)),
        mark(fire(12, 9.5, 14.5, 3.5)),
        line(seg(8, 17, 8, 21.5)), line(seg(12, 17, 12, 21.5)), line(seg(16, 17, 16, 21.5)),
    ]


# ============================================================================ ventilation and ducts

@icon("air-vent", CAT, "Air vent register: a rectangle of parallel louvres with a screw at each end",
      tags=["vent", "air register", "grille", "ventilation", "hvac", "duct cover"], aliases=["vent-grille"])
def _(S):
    return [
        shell(rect(2, 5.5, 20, 13, rr(S, 2.5))),
        detail(seg(6.5, 9, 17.5, 9)), detail(seg(6.5, 12, 17.5, 12)), detail(seg(6.5, 15, 17.5, 15)),
        dot(4.25, 12, 0.9), dot(19.75, 12, 0.9),
    ]


@icon("air-filter", CAT, "Pleated HVAC air filter panel with zigzag pleats inside its frame",
      tags=["furnace filter", "hvac filter", "pleated filter", "air purification", "dust filter", "hepa"])
def _(S):
    pts = [(2.5 + 19 * k / 6, 3 if k % 2 == 0 else 21) for k in range(7)]
    return [
        shell(rect(2.5, 3, 19, 18, rr(S, 2.5))),
        detail(poly(pts, r=S.r * 0.5)),
    ]


@icon("hvac-duct", CAT, "Rectangular air duct with a right-angle elbow bend and joint seams",
      tags=["ductwork", "air duct", "ventilation duct", "hvac", "elbow", "sheet metal"], aliases=["ductwork"])
def _(S):
    body = poly([(2, 13), (13, 13), (13, 2), (21, 2), (21, 21), (2, 21)], closed=True, r=S.r * 0.6)
    return [
        shell(body),
        detail(seg(8, 13, 8, 21)),
        detail(seg(13, 8, 21, 8)),
        detail(seg(13, 13, 21, 21)),
    ]
