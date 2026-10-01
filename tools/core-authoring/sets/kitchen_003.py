"""TypeIcon Core: kitchen (batch kitchen_003): oven mode symbols, care labels, prep tools, serving and cooking scenes.

Oven mode symbols share the oven frame used by kitchen_004 (an 18 x 18 square) with the heating element or
fan drawn inside it. Hand tools are drawn upright or turned 45 degrees like kitchen_001 and kitchen_002.
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


def tr(parts, deg, cx, cy):
    """Rotate parts clockwise by deg about (cx, cy) without re-centring."""
    return [Part(p.kind, rot(p.d, deg, cx, cy), p.attrs) for p in parts]


def rpoly(S, pts, closed=True, k=1.0):
    return poly(pts, closed=closed, r=S.r * k)


def steam(x, y0, y1, a=1.5):
    """Wavy rising line from (x, y1) up to (x, y0)."""
    h = y1 - y0
    return f"M{fmt(x)} {fmt(y1)}Q{fmt(x - a)} {fmt(y1 - h / 4)} {fmt(x)} {fmt(y1 - h / 2)}T{fmt(x)} {fmt(y0)}"


def flame(cx, top, bottom, w):
    """Upright flame: pointed tip at top, round base; w is the half width."""
    h = bottom - top
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + w * 0.4)} {fmt(top + h * 0.3)} {fmt(cx + w)} {fmt(top + h * 0.45)} "
            f"{fmt(cx + w)} {fmt(top + h * 0.72)}A{fmt(w)} {fmt(h * 0.28)} 0 0 1 {fmt(cx - w)} {fmt(top + h * 0.72)}"
            f"C{fmt(cx - w)} {fmt(top + h * 0.45)} {fmt(cx - w * 0.4)} {fmt(top + h * 0.3)} {fmt(cx)} {fmt(top)}Z")


def drop(cx, top, bottom):
    """Water drop: pointed top, round bottom."""
    h = bottom - top
    r = h * 0.36
    cy = bottom - r
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + r * 0.3)} {fmt(top + h * 0.25)} {fmt(cx + r)} {fmt(cy - r * 0.5)} "
            f"{fmt(cx + r)} {fmt(cy)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx - r)} {fmt(cy)}"
            f"C{fmt(cx - r)} {fmt(cy - r * 0.5)} {fmt(cx - r * 0.3)} {fmt(top + h * 0.25)} {fmt(cx)} {fmt(top)}Z")


# ============================================================================ oven mode symbols

def _frame(S):
    return shell(rect(3, 3, 18, 18, rr(S, 4)))


def _fan(cx, cy, r):
    """Three solid curved fan blades meeting at the hub (knocked out of a Filled frame)."""
    k = r / 5.5
    blade = (f"M12 12C{fmt(12 - 2.6 * k)} {fmt(12 - 1.6 * k)} {fmt(12 - 2.2 * k)} {fmt(12 - 4.9 * k)} "
             f"{fmt(12 + 0.6 * k)} {fmt(12 - 5.5 * k)}C{fmt(12 + 2.4 * k)} {fmt(12 - 4.2 * k)} "
             f"{fmt(12 + 2.2 * k)} {fmt(12 - 1.8 * k)} 12 12Z")
    blade = mv(blade, cx - 12, cy - 12)
    return [hole(rot(blade, a, cx, cy)) for a in (0, 120, 240)]


def _dish(cy):
    """Small baking dish seen from the side, open at the top, top edge at cy."""
    return detail(f"M7 {fmt(cy)}L8 {fmt(cy + 3)}H16L17 {fmt(cy)}")


def _zigzag(y0, y1):
    return detail(poly([(6.5, y0), (9.25, y1), (12, y0), (14.75, y1), (17.5, y0)]))


@icon("oven-convection-fan", CAT, "Oven convection mode: a three-bladed fan inside the oven frame",
      tags=["fan oven", "fan assisted", "convection", "oven setting", "oven function", "appliance symbol"],
      aliases=["fan-oven"])
def _(S):
    return [_frame(S)] + _fan(12, 12, 6)


@icon("oven-top-heat", CAT, "Oven top heat mode: a heating bar along the top of the oven frame above a dish",
      tags=["top heat", "upper heat", "oven setting", "oven function", "browning", "appliance symbol"])
def _(S):
    return [_frame(S), detail(seg(7, 7, 17, 7)), _dish(12)]


@icon("oven-bottom-heat", CAT, "Oven bottom heat mode: a heating bar along the bottom of the oven frame below a dish",
      tags=["bottom heat", "lower heat", "oven setting", "oven function", "base heat", "appliance symbol"])
def _(S):
    return [_frame(S), detail(seg(7, 17, 17, 17)), _dish(9)]


@icon("oven-top-bottom-heat", CAT, "Oven conventional mode: heating bars along the top and bottom with a dish between",
      tags=["conventional oven", "top and bottom heat", "static oven", "oven setting", "oven function", "appliance symbol"],
      aliases=["oven-conventional-mode"])
def _(S):
    return [_frame(S), detail(seg(7, 6.75, 17, 6.75)), detail(seg(7, 17.25, 17, 17.25)), _dish(10.5)]


@icon("oven-grill-element", CAT, "Oven grill mode: a zigzag heating element along the top of the oven frame",
      tags=["grill", "broil", "broiler", "oven setting", "oven function", "appliance symbol"],
      aliases=["oven-broil-mode"])
def _(S):
    return [_frame(S), _zigzag(6.5, 9.5)]


@icon("oven-light", CAT, "Oven light: a light bulb inside the oven frame",
      tags=["oven lamp", "light", "bulb", "oven setting", "oven function", "appliance symbol"])
def _(S):
    bulb = ("M10 17H14V14.6C15.3 13.8 16 12.5 16 11A4 4 0 0 0 8 11C8 12.5 8.7 13.8 10 14.6Z" if S.name == "rounded"
            else "M10 17H14V14.6L15.4 13.2C15.8 12.6 16 11.8 16 11A4 4 0 0 0 8 11C8 11.8 8.2 12.6 8.6 13.2L10 14.6Z")
    return [_frame(S), detail(bulb), detail(seg(10, 14.6, 14, 14.6))]


@icon("oven-fan-grill", CAT, "Oven fan grill mode: a zigzag element along the top and a small fan below it",
      tags=["fan grill", "fan broil", "convection broil", "oven setting", "oven function", "appliance symbol"],
      aliases=["oven-convection-broil"])
def _(S):
    return [_frame(S), _zigzag(6, 8.5)] + _fan(12, 14.75, 3.5)


@icon("oven-ring-heat", CAT, "Oven fan forced mode: a fan in the centre surrounded by a round heating ring",
      tags=["true convection", "fan forced", "ring element", "hot air", "oven setting", "oven function"],
      aliases=["oven-true-convection"])
def _(S):
    return [_frame(S), detail(circle(12, 12, 5.75))] + _fan(12, 12, 3.4)


@icon("oven-fan-bottom-heat", CAT, "Oven fan with bottom heat mode: a small fan above a heating bar at the bottom",
      tags=["fan with bottom heat", "pizza setting", "convection bake", "oven setting", "oven function", "appliance symbol"])
def _(S):
    return [_frame(S), detail(seg(7, 17, 17, 17))] + _fan(12, 10, 3.6)


@icon("oven-defrost", CAT, "Oven defrost mode: a small fan beside a water drop inside the oven frame",
      tags=["defrost", "thaw", "defrosting", "oven setting", "oven function", "appliance symbol"])
def _(S):
    return [_frame(S), hole(drop(16, 8.5, 15.5))] + _fan(9.5, 12, 3.4)


@icon("oven-steam-mode", CAT, "Oven steam mode: three wavy steam lines rising inside the oven frame",
      tags=["steam oven", "steam cooking", "moisture", "oven setting", "oven function", "appliance symbol"])
def _(S):
    return [_frame(S), detail(steam(8, 7, 17)), detail(steam(12, 7, 17)), detail(steam(16, 7, 17))]


# ============================================================================ care labels and symbols

@icon("dish-towel", CAT, "Dish towel hanging from a loop with a striped band near the bottom",
      tags=["tea towel", "kitchen towel", "dish cloth", "drying", "linen", "cloth"], aliases=["tea-towel"])
def _(S):
    top = "M5 9V8A2 2 0 0 1 7 6H17A2 2 0 0 1 19 8V9" if S.name == "rounded" else "M5 9V6H19V9"
    cloth = top + "V20C16.5 22.5 14.5 18.5 12 20.5C9.5 22.5 7.5 18.5 5 20.5Z"
    return [line(circle(12, 3.5, 1.75)), shell(cloth), detail(seg(5, 12.5, 19, 12.5)), detail(seg(5, 16, 19, 16))]


@icon("keep-warm", CAT, "Keep warm: a covered plate with wavy heat lines rising above the dome",
      tags=["warming", "hold temperature", "warm setting", "food warmer", "hot food", "heat"],
      aliases=["keep-hot"])
def _(S):
    body = union("M4.5 19.5A7.5 7 0 0 1 19.5 19.5Z", rect(2.5, 19, 19, 2.5, L(S, 0, 1.25)))
    return [shell(body), detail(seg(4.5, 19, 19.5, 19)),
            line(steam(8, 3, 9.5)), line(steam(12, 2.5, 9.5)), line(steam(16, 3, 9.5))]


@icon("dishwasher-safe", CAT, "Dishwasher safe: a plate and a glass standing in a rack under falling water drops",
      tags=["dishwasher proof", "care label", "machine washable", "dishes", "cleaning", "kitchenware"],
      aliases=["dishwasher-proof"])
def _(S):
    rack = rpoly(S, [(2.5, 17.5), (2.5, 21), (21.5, 21), (21.5, 17.5)], closed=False, k=0.6)
    glass = rpoly(S, [(15, 10), (20.5, 10), (19.75, 18.5), (15.75, 18.5)], k=0.5)
    return [line(rack), shell(circle(8, 14, 4.25)), shell(glass),
            solid(drop(7, 2, 7)), solid(drop(12, 2, 7)), solid(drop(17, 2, 7))]


@icon("oven-safe", CAT, "Oven safe: a covered dish inside an oven outline with a small flame below",
      tags=["ovenproof", "oven proof", "care label", "heat resistant", "bakeware", "kitchenware"],
      aliases=["ovenproof"])
def _(S):
    dish = union(rect(7.5, 8.5, 9, 4, L(S, 0.5, 1.5)), rect(5.5, 8.5, 13, 1.5, L(S, 0, 0.75)))
    return [shell(rect(3, 2.5, 18, 14, rr(S, 3))), detail(dish), solid(flame(12, 17.5, 22, 2.2))]


@icon("freezer-safe", CAT, "Freezer safe: a snowflake above a small lidded food container",
      tags=["freezer proof", "care label", "frozen", "freeze", "cold storage", "food container"],
      aliases=["freezer-proof"])
def _(S):
    flake = "".join(seg(*pt_on(12, 6, 4, a), *pt_on(12, 6, 4, a + 180)) for a in (0, 60, 120))
    box = union(rect(3.5, 12.5, 17, 3, L(S, 0.5, 1.5)), rect(5, 14, 14, 7.5, rr(S, 2.5)))
    return [line(flake), shell(box), detail(seg(5, 15.5, 19, 15.5))]


@icon("food-safe-symbol", CAT, "Food safe symbol: a wine glass beside a fork",
      tags=["food grade", "food contact", "glass and fork", "food safe", "kitchenware", "label"],
      aliases=["food-grade"])
def _(S):
    bowl = "M2.5 3H10V6.5A3.75 3.75 0 0 1 2.5 6.5Z" if S.name == "rounded" else "M2.5 3H10V7L6.25 10.5L2.5 7Z"
    tines = "M14.5 3V8A3 3 0 0 0 20.5 8V3" if S.name == "rounded" else "M14.5 3V11H20.5V3"
    return fit([shell(bowl), line(seg(6.25, 10.5, 6.25, 20)), line(seg(3, 21, 9.5, 21)),
                line(tines), line(seg(17.5, 3, 17.5, 21))])


def smooth(pts, closed=False):
    """Catmull-Rom spline through pts as cubic Beziers (clean curves from few points)."""
    n = len(pts)
    out = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if closed or i > 0 else pts[i]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if closed or i + 2 < n else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        out += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return out + ("Z" if closed else "")


@icon("induction-compatible", CAT, "Induction compatible: a pot standing above a looped induction coil",
      tags=["induction ready", "induction hob", "cookware label", "magnetic base", "induction cooktop", "pan"],
      aliases=["induction-ready"])
def _(S):
    loops, x0, x1, yc = 3, 5.5, 18.5, 17.5
    a = (x1 - x0) / (loops * 2 * math.pi)
    b, c = 3.0, 3.25
    pts = []
    steps = loops * 8
    for i in range(steps + 1):
        t = i / steps * loops * 2 * math.pi + math.pi
        pts.append((x0 + a * (t - math.pi) + b * math.sin(t), yc - c * math.cos(t)))
    pot = rect(5, 2.5, 14, 6.5, rr(S, 2))
    return [shell(pot), line(seg(2.5, 5, 5, 5)), line(seg(19, 5, 21.5, 5)), line(seg(2.5, 11.5, 21.5, 11.5)),
            line(smooth(pts))]


@icon("colander", CAT, "Colander: a deep perforated bowl with side handles on the rim and a ring foot",
      tags=["strainer", "pasta strainer", "draining", "sieve", "rinsing", "kitchen tool"])
def _(S):
    bowl = "M4 8.5H20C20 15 16.5 19 12 19C7.5 19 4 15 4 8.5Z"
    rim = rect(1.5, 7, 21, 3, L(S, 0.5, 1.5))
    foot = rect(8.5, 17.5, 7, 4, L(S, 0.5, 1.5))
    return [shell(union(bowl, rim, foot)), detail(seg(4, 10, 20, 10)),
            dot(8.5, 13, 1.1), dot(12, 13, 1.1), dot(15.5, 13, 1.1), dot(10.25, 16, 1.1), dot(13.75, 16, 1.1)]


@icon("mesh-strainer", CAT, "Mesh strainer: a round fine mesh bowl with a crosshatch, a long handle and a rim hook",
      tags=["sieve", "fine mesh sieve", "sifter", "tea strainer", "straining", "kitchen tool"], aliases=["sieve"])
def _(S):
    cx, top, r = 9.5, 9, 7
    bowl = f"M{fmt(cx - r)} {fmt(top)}H{fmt(cx + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx - r)} {fmt(top)}Z"
    hook = rpoly(S, [(2.5, 9), (1, 9), (1, 7)], closed=False, k=0.5)
    return fit([shell(bowl), detail(seg(6.5, top, 6.5, 15)), detail(seg(12.5, top, 12.5, 15)),
                detail(seg(4, 12.5, 15, 12.5)), line(seg(cx + r, top, 22, 4.5)), line(hook)])


@icon("service-bell", CAT, "Service bell: a dome counter bell with a push button on top, sitting on a flat base",
      tags=["counter bell", "reception bell", "desk bell", "call bell", "ring for service", "concierge"],
      aliases=["counter-bell", "desk-bell"])
def _(S):
    body = union("M4.5 17A7.5 7.5 0 0 1 19.5 17Z", rect(2.5, 17, 19, 3.5, L(S, 0.5, 1.75)))
    return [shell(body), detail(seg(4.5, 17, 19.5, 17)), line(seg(12, 6, 12, 9.5)),
            shell(rect(9.5, 3.5, 5, 2.5, L(S, 0.5, 1.25))), line(seg(4.5, 5, 6.5, 7)), line(seg(19.5, 5, 17.5, 7))]


@icon("dough-whisk", CAT, "Dough whisk: a wooden handle with a pointed wire loop crossed by two wires",
      tags=["danish dough whisk", "dough hook", "bread whisk", "mixing", "baking", "kitchen tool"],
      aliases=["danish-dough-whisk"])
def _(S):
    loop = "M12 13C7.5 12 5.5 8.5 7 5C8.5 2 15.5 2 17 5C18.5 8.5 16.5 12 12 13Z" if S.name == "rounded" else \
        "M12 13L7.5 9.5L7 5L10 2.5H14L17 5L16.5 9.5Z"
    return tilt([line(loop), line("M8 5.5C10.5 6.5 13.5 9.5 16 10"), line("M16 5.5C13.5 6.5 10.5 9.5 8 10"),
                 shell(rect(10.25, 13, 3.5, 9, L(S, 0.5, 1.75)))])


@icon("cake-leveler", CAT, "Cake leveler: a U-shaped wire frame on two feet with a cutting wire slicing a cake",
      tags=["cake slicer", "cake leveller", "layer cutter", "torting", "cake decorating", "baking"],
      aliases=["cake-leveller"])
def _(S):
    frame = rpoly(S, [(3, 20.5), (3, 3), (21, 3), (21, 20.5)], closed=False)
    return [line(frame), line(seg(1.5, 21, 4.5, 21)), line(seg(19.5, 21, 22.5, 21)),
            shell(rect(7, 10, 10, 11, rr(S, 1.5))), line(seg(4, 14, 7, 14)), line(seg(17, 14, 20, 14)),
            detail(seg(7, 14, 17, 14))]


@icon("herb-scissors", CAT, "Herb scissors: a comb of parallel blades on a crossing pair of ring handles",
      tags=["multi blade scissors", "herb shears", "herb cutter", "chopping herbs", "chives", "kitchen tool"],
      aliases=["herb-shears"])
def _(S):
    head = rect(4.5, 2.5, 15, 7, L(S, 1, 3))
    return [shell(head), detail(seg(8.25, 2.5, 8.25, 9.5)), detail(seg(12, 2.5, 12, 9.5)), detail(seg(15.75, 2.5, 15.75, 9.5)),
            line(seg(7.75, 16, 13.5, 10)), line(seg(16.25, 16, 10.5, 10)),
            line(circle(6.5, 18.5, 2.5)), line(circle(17.5, 18.5, 2.5))]


@icon("rotary-grater", CAT, "Rotary grater: a drum grater with a crank on one side and a grip handle below",
      tags=["drum grater", "cheese grater", "rotary cheese grater", "parmesan", "grating", "kitchen tool"],
      aliases=["drum-grater"])
def _(S):
    drum = rect(3, 3.5, 13, 9, rr(S, 2.5))
    crank = rpoly(S, [(16, 8), (20, 8), (20, 12)], closed=False, k=0.6)
    return [shell(drum), dot(6.5, 8, 1), dot(9.5, 6.25, 1), dot(12.5, 8, 1), dot(9.5, 9.75, 1), line(crank),
            shell(rect(18, 12, 4, 3.5, L(S, 0.5, 1.5))),
            shell(rect(6.5, 12.5, 6, 9.5, rr(S, 2.5))), detail(seg(9.5, 15.5, 9.5, 19.5))]


@icon("campfire-pot", CAT, "Campfire pot: a cooking pot hanging from a tripod of poles over small flames",
      tags=["camp cooking", "tripod", "dutch oven", "cauldron", "outdoor cooking", "camping"],
      aliases=["tripod-pot"])
def _(S):
    pot = rpoly(S, [(9, 10.5), (15, 10.5), (15, 14.5), (13.5, 16.5), (10.5, 16.5), (9, 14.5)], k=1)
    return [line(seg(1.5, 21.5, 12.9, 1)), line(seg(22.5, 21.5, 11.1, 1)), line(seg(12, 3.5, 12, 10.5)), shell(pot),
            solid(flame(10, 18.5, 22, 1.5)), solid(flame(14, 18.5, 22, 1.5))]


@icon("vertical-rotisserie", CAT, "Vertical rotisserie: a tall cone of stacked meat on an upright spit beside a heating panel",
      tags=["doner", "shawarma", "gyro", "kebab spit", "al pastor", "rotisserie"],
      aliases=["doner-spit"])
def _(S):
    cone = "M3.5 5H15.5C15.5 10.5 14 15 12 18H7C5 15 3.5 10.5 3.5 5Z"
    return [line(seg(9.5, 1.5, 9.5, 5)), shell(cone), detail("M4.2 9.5Q9.5 11 14.8 9.5"), detail("M5.4 14Q9.5 15.5 13.6 14"),
            line(seg(9.5, 18, 9.5, 21)), line(seg(4, 21.5, 15, 21.5)), shell(rect(18, 3.5, 3.5, 17, L(S, 0.5, 1.75)))]


@icon("cereal-dispenser", CAT, "Cereal dispenser: a tall clear hopper of cereal with a tapered spout above a bowl",
      tags=["dry food dispenser", "cereal", "breakfast", "granola", "food storage", "canister"])
def _(S):
    hopper = rpoly(S, [(6, 2.5), (18, 2.5), (18, 11), (14, 15), (10, 15), (6, 11)], k=0.7)
    return [shell(hopper), dot(8.75, 6.25, 0.9), dot(12.25, 5, 0.9), dot(15.5, 7, 0.9), dot(10.25, 9.25, 0.9), dot(13.75, 10.25, 0.9),
            shell("M6 18.5H18C18 20.5 15.5 22 12 22C8.5 22 6 20.5 6 18.5Z")]


def _bowl(x0, x1, y, depth):
    cx, r = (x0 + x1) / 2, (x1 - x0) / 2
    return f"M{fmt(x0)} {fmt(y)}H{fmt(x1)}A{fmt(r)} {fmt(depth)} 0 0 1 {fmt(x0)} {fmt(y)}Z"


@icon("napkin-holder", CAT, "Napkin holder: a low open holder with a fan of paper napkins standing in it",
      tags=["serviette holder", "napkin stand", "paper napkins", "table", "dining", "tabletop"],
      aliases=["serviette-holder"])
def _(S):
    holder = rect(4, 13.5, 16, 8, rr(S, 2.5))
    sheet = rect(8.5, 3, 7, 12, L(S, 0, 1))
    left, right = rot(sheet, -18, 12, 15), rot(sheet, 18, 12, 15)
    return [shell(minus(left, sheet, holder)), shell(minus(right, sheet, holder)), shell(minus(sheet, holder)), shell(holder)]


@icon("rinsing-produce", CAT, "Rinsing produce: a tap with a water drop falling onto two vegetables in a colander",
      tags=["washing vegetables", "washing fruit", "rinse", "produce", "food prep", "clean eating"],
      aliases=["washing-vegetables"])
def _(S):
    tap = rpoly(S, [(3, 6), (3, 2.5), (12, 2.5), (12, 5)], closed=False, k=0.8)
    bowl = "M4 14.5H20C20 19 16.5 21.5 12 21.5C8 21.5 4 19 4 14.5Z"
    body = union(bowl, rect(2.5, 13.5, 19, 2.5, L(S, 0.5, 1.25)))
    return [line(tap), solid(drop(12, 6.5, 11)), shell(circle(7.5, 11.25, 2.25)), shell(circle(16.5, 11.25, 2.25)),
            shell(body), dot(9, 19, 1), dot(12, 19, 1), dot(15, 19, 1)]


@icon("washing-dishes", CAT, "Washing dishes: plates standing in a sink basin with soap bubbles above",
      tags=["dishwashing", "washing up", "sink", "dishes", "cleaning", "chores"], aliases=["washing-up"])
def _(S):
    basin = rect(2.5, 13, 19, 8.5, rr(S, 3))
    return [line(arc(8, 13, 4.5, 180, 360)), line(arc(12.5, 13, 4.5, 215, 360)), shell(basin),
            detail(seg(2.5, 15.5, 21.5, 15.5)), line(circle(18.5, 6.5, 2)), line(circle(15, 3, 1.25))]


@icon("chef-jacket", CAT, "Chef jacket: a double-breasted white jacket with a stand collar and two rows of buttons",
      tags=["chef coat", "chef whites", "chef uniform", "cook", "restaurant", "kitchen uniform"],
      aliases=["chef-coat"])
def _(S):
    body = rpoly(S, [(8, 4), (3.5, 6.5), (2, 16.5), (5.5, 16.5), (6.5, 11), (6.5, 21.5), (17.5, 21.5), (17.5, 11),
                     (18.5, 16.5), (22, 16.5), (20.5, 6.5), (16, 4)], k=0.6)
    return [shell(body), shell(rect(8, 2, 8, 3, L(S, 0.5, 1.5))), dot(10, 9.5, 1.1), dot(14, 9.5, 1.1),
            dot(10, 13.5, 1.1), dot(14, 13.5, 1.1), dot(10, 17.5, 1.1), dot(14, 17.5, 1.1)]


@icon("order-ticket-rail", CAT, "Order ticket rail: a kitchen rail with three paper order tickets hanging from it",
      tags=["ticket rail", "order rail", "check rail", "kitchen tickets", "restaurant orders", "order tickets"],
      aliases=["ticket-rail"])
def _(S):
    out = [shell(rect(2, 3, 20, 3.5, L(S, 0.5, 1.75)))]
    for x, h in ((3, 12), (10.25, 15), (17.5, 10)):
        y1 = 6.5 + h
        out.append(shell(rpoly(S, [(x, 6.5), (x + 3.5, 6.5), (x + 3.5, y1), (x + 1.75, y1 - 1.5), (x, y1)], k=0.3)))
    return out


@icon("recipe-box", CAT, "Recipe box: an open box of index cards with a raised divider tab",
      tags=["recipe cards", "recipe file", "card index", "index cards", "cookbook", "recipes"],
      aliases=["recipe-card-box"])
def _(S):
    box = rect(3, 12.5, 18, 9, rr(S, 2))
    card = union(rect(5.5, 6, 13, 8, L(S, 0, 1)), rect(6.5, 3, 5.5, 4, L(S, 0, 1)))
    return [shell(minus(card, box)), shell(box), detail(seg(8, 17, 16, 17))]


@icon("knife-sharpener", CAT, "Knife sharpener: a pull-through block with a V-shaped slot and a knife blade lowered into it",
      tags=["pull through sharpener", "knife sharpening", "sharpen knife", "honing", "blade", "knife care"],
      aliases=["pull-through-sharpener"])
def _(S):
    block = rpoly(S, [(3, 21.5), (3, 12), (8, 12), (12, 17.5), (16, 12), (21, 12), (21, 21.5)], k=0.7)
    blade = rpoly(S, [(9.75, 7.5), (14.25, 7.5), (12, 13.5)], k=0.4)
    return [shell(block), shell(rect(10.25, 2, 3.5, 5.5, L(S, 0.5, 1.5))), shell(blade)]


@icon("knife-roll", CAT, "Knife roll: an unrolled fabric wrap with knife handles in a row of pockets and a tie strap",
      tags=["knife bag", "knife wrap", "chef's roll", "knife case", "culinary school", "knife storage"],
      aliases=["knife-bag"])
def _(S):
    out = [shell(rect(2.5, 9.5, 16, 12, rr(S, 2))), detail(seg(2.5, 14, 18.5, 14))]
    for x in (5.5, 10.5, 15.5):
        out.append(shell(rect(x - 1.25, 3, 2.5, 8.5, L(S, 0.5, 1.25))))
        out.append(detail(seg(x + 2.5, 14, x + 2.5, 21.5)) if x < 15 else detail(seg(x + 2.5, 14, x + 2.5, 14)))
    out.append(line("M18.5 17.5H20.5A1.5 1.5 0 0 1 20.5 20.5H19" if S.name == "rounded" else "M18.5 17.5H22V20.5H19"))
    return out


@icon("rising-dough", CAT, "Rising dough: a bowl covered with a cloth pushed up into a dome by the dough underneath",
      tags=["proofing dough", "proving dough", "bread dough", "yeast", "baking", "bread making"],
      aliases=["proofing-dough"])
def _(S):
    cloth = "M2 15C2 8 6.5 4.5 12 4.5C17.5 4.5 22 8 22 15L19.5 13.5L17 15L14.5 13.5L12 15L9.5 13.5L7 15L4.5 13.5Z"
    bowl = "M4 16H20C19.5 19.5 16.5 21.5 12 21.5C7.5 21.5 4.5 19.5 4 16Z"
    return [shell(cloth, stroke_miterlimit="2"), shell(bowl), detail("M7 9.5Q9 7.5 12 7.5")]


@icon("meat-claws", CAT, "Meat claws: a pair of shredding claws, each with a grip handle and a row of long pointed tines",
      tags=["bear claws", "meat shredder", "pulled pork", "shredding claws", "barbecue", "bbq tool"],
      aliases=["bear-claws"])
def _(S):
    def claw(cx):
        out = [shell(rect(cx - 4, 3, 8, 5.5, rr(S, 2.5))), detail(seg(cx - 2, 5.75, cx + 2, 5.75))]
        for dx in (-3, 0, 3):
            tip = (cx + dx, 21) if S.name == "line" else (cx + dx, 20.5)
            out.append(line(seg(cx + dx, 8.5, *tip)))
        return out
    return tr(claw(6.5), -8, 6.5, 8) + tr(claw(17.5), 8, 17.5, 8)


@icon("chestnut-pan", CAT, "Chestnut pan: a shallow perforated pan with a long handle holding roasting chestnuts",
      tags=["chestnut roaster", "roasting chestnuts", "perforated pan", "open fire", "winter", "roasting"],
      aliases=["chestnut-roaster"])
def _(S):
    def nut(x):
        return f"M{fmt(x - 2.75)} 12.5C{fmt(x - 2.75)} 9.5 {fmt(x - 1.25)} 8 {fmt(x)} 6.5C{fmt(x + 1.25)} 8 {fmt(x + 2.75)} 9.5 {fmt(x + 2.75)} 12.5Z"
    pan = rpoly(S, [(2, 12.5), (16.5, 12.5), (15, 18), (3.5, 18)], k=0.8)
    return [shell(nut(6)), shell(nut(12.5)), shell(pan), line(seg(16, 14.5, 22, 11.5)),
            dot(6, 15.25, 0.9), dot(9.25, 15.25, 0.9), dot(12.5, 15.25, 0.9)]


@icon("soft-serve-machine", CAT, "Soft serve machine: a box machine with a lever above a swirled ice cream cone",
      tags=["ice cream machine", "frozen yogurt", "soft ice", "froyo", "dessert", "machine"],
      aliases=["ice-cream-machine"])
def _(S):
    swirl = union(rect(5.5, 13.5, 13, 3.5, L(S, 1, 1.75)), rect(8, 10, 8, 4, L(S, 1, 2)))
    cone = rpoly(S, [(7, 17), (17, 17), (12, 22.5)], k=0.5)
    return [shell(rect(3, 2, 18, 5, rr(S, 2))), dot(7, 4.5, 0.9), detail(seg(11, 4.5, 17, 4.5)),
            shell(union(swirl, cone)), detail(seg(8, 17, 16, 17))]


@icon("plate-stack", CAT, "Plate stack: three dinner plates stacked on top of each other, seen from the side",
      tags=["stack of plates", "dishes", "crockery", "dinnerware", "tableware", "clean plates"],
      aliases=["stacked-plates"])
def _(S):
    return [shell(rpoly(S, [(3.5, y), (20.5, y), (17, y + 4), (7, y + 4)], k=0.5)) for y in (3.5, 9.5, 15.5)]


@icon("grill-press", CAT, "Grill press: a flat iron weight with ridges underneath and a handle on top",
      tags=["bacon press", "burger weight", "steak weight", "cast iron", "griddle", "grilling"],
      aliases=["bacon-press"])
def _(S):
    return [shell(rect(5.5, 3.5, 13, 3.5, rr(S, 1.75))), line(seg(8, 7, 8, 10)), line(seg(16, 7, 16, 10)),
            shell(rect(2.5, 10, 19, 5.5, rr(S, 1.5)))] + [line(seg(x, 15.5, x, 18.5)) for x in (4.5, 9.5, 14.5, 19.5)] + \
        [line(seg(2.5, 21, 21.5, 21))]


def rpt(x, y, deg, cx, cy):
    """Rotate one point clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    return (cx + (x - cx) * math.cos(a) - (y - cy) * math.sin(a), cy + (x - cx) * math.sin(a) + (y - cy) * math.cos(a))


# ============================================================================ tools, serving and cooking scenes

@icon("lemon-squeezer", CAT, "Lemon squeezer: a cup holding a lemon half with a pair of long hinged handles",
      tags=["citrus press", "lime squeezer", "juicer", "hand juicer", "squeezing", "kitchen tool"],
      aliases=["citrus-press"])
def _(S):
    cup = "M2.5 11H14.5A6 6 0 0 1 2.5 11Z"
    lemon = "M4.75 11C4.75 7.5 6.5 5.5 8.5 4.25C10.5 5.5 12.25 7.5 12.25 11Z"
    return [shell(lemon), shell(cup), line(seg(13.5, 14, 21.5, 17.5)), line(seg(14.5, 9, 21.5, 6.5))]


@icon("vegetable-dicer", CAT, "Vegetable dicer: a box with diced cubes inside and a lifted lid whose underside is a grid of blades",
      tags=["chopper", "onion chopper", "veggie chopper", "dicing", "food prep", "kitchen tool"],
      aliases=["onion-chopper"])
def _(S):
    lid = rect(4, 2.5, 16, 8, rr(S, 2))
    return [shell(lid), detail(seg(9.33, 2.5, 9.33, 10.5)), detail(seg(14.67, 2.5, 14.67, 10.5)), detail(seg(4, 6.5, 20, 6.5)),
            shell(rect(3, 13.5, 18, 8, rr(S, 2.5))), hole(rect(6.5, 16.5, 3, 3, L(S, 0, 0.75))),
            hole(rect(10.5, 16.5, 3, 3, L(S, 0, 0.75))), hole(rect(14.5, 16.5, 3, 3, L(S, 0, 0.75)))]


@icon("pulling-noodles", CAT, "Pulling noodles: two fists stretching long noodle strands that hang in loops between them",
      tags=["hand pulled noodles", "la mian", "noodle making", "stretching dough", "chinese noodles", "noodle chef"],
      aliases=["hand-pulled-noodles"])
def _(S):
    return [shell(rect(2, 2.5, 5, 6.5, L(S, 1, 2.25))), shell(rect(17, 2.5, 5, 6.5, L(S, 1, 2.25))),
            line("M7 4.5Q12 14 17 4.5"), line("M7 6.5Q12 19 17 6.5"), line("M7 8.5Q12 24 17 8.5")]


@icon("sizzling-platter", CAT, "Sizzling platter: a cast iron serving plate on a wooden board with steam rising from it",
      tags=["fajita plate", "hot plate", "cast iron", "sizzling", "steak plate", "restaurant"],
      aliases=["fajita-plate"])
def _(S):
    plate = "M2.5 12.5H21.5C21 15 19 16 17 16H7C5 16 3 15 2.5 12.5Z" if S.name == "rounded" else "M2.5 12.5H21.5L18.5 16H5.5Z"
    return [line(steam(7.5, 2.5, 9.5)), line(steam(12, 2.5, 9.5)), line(steam(16.5, 2.5, 9.5)),
            shell(plate), shell(rect(4, 18, 16, 3.5, L(S, 0.5, 1.75)))]


@icon("kitchen-counter", CAT, "Kitchen counter: a wall cabinet above a worktop with a tap, over a base cabinet",
      tags=["kitchen cabinets", "kitchen units", "countertop", "worktop", "kitchen design", "cupboards"],
      aliases=["kitchen-cabinets"])
def _(S):
    return [shell(rect(3, 2.5, 18, 6.5, rr(S, 2))), detail(seg(12, 2.5, 12, 9)), shell(rect(2, 12, 20, 2.5, L(S, 0.5, 1.25))),
            line(rpoly(S, [(15, 12), (15, 9.5), (18, 9.5)], closed=False, k=0.5)),
            shell(rect(3, 14.5, 18, 7, rr(S, 2))), detail(seg(12, 14.5, 12, 21.5)),
            dot(9.75, 18, 0.9), dot(14.25, 18, 0.9)]


@icon("cornbread-pan", CAT, "Cornbread pan: a cast iron tray with a row of corn-cob shaped wells",
      tags=["corn stick pan", "corn bread mold", "cast iron", "baking pan", "southern cooking", "bakeware"],
      aliases=["corn-stick-pan"])
def _(S):
    def cob(x):
        return f"M{fmt(x)} 6.5C{fmt(x + 2.5)} 8.5 {fmt(x + 2.5)} 14 {fmt(x + 1.75)} 16.5A1.75 1.75 0 0 1 {fmt(x - 1.75)} 16.5C{fmt(x - 2.5)} 14 {fmt(x - 2.5)} 8.5 {fmt(x)} 6.5Z"
    return [shell(rect(2.5, 3.5, 19, 17, rr(S, 3))), hole(cob(7.5)), hole(cob(12)), hole(cob(16.5))]


@icon("korean-bbq-grill", CAT, "Korean barbecue grill: a domed ribbed grill plate with a drain rim over a small gas flame",
      tags=["kbbq", "tabletop grill", "gogi gui", "samgyeopsal", "barbecue", "dome grill"],
      aliases=["kbbq-grill"])
def _(S):
    dome = union("M5 11.5A7 6.5 0 0 1 19 11.5Z", rect(2.5, 11, 19, 2.5, L(S, 0.5, 1.25)))
    return [shell(dome), detail(seg(9, 7, 9, 11.5)), detail(seg(12, 5.5, 12, 11.5)), detail(seg(15, 7, 15, 11.5)),
            solid(flame(8, 16.5, 21.5, 1.75)), solid(flame(12, 16, 21.5, 2)), solid(flame(16, 16.5, 21.5, 1.75))]


@icon("ladling-soup", CAT, "Ladling soup: a ladle tilted over a bowl with a stream of soup pouring from its lip",
      tags=["soup ladle", "serving soup", "pouring", "soup kitchen", "broth", "dinner"],
      aliases=["serving-soup"])
def _(S):
    cup = rot("M5.5 7H15.5A5 5 0 0 1 5.5 7Z", -38, 10.5, 7)
    rim_r = rpt(15.5, 7, -38, 10.5, 7)
    lip = rpt(5.5, 7, -38, 10.5, 7)
    bowl = "M3.5 15.5H20.5C20.5 19.5 16.5 21.5 12 21.5C7.5 21.5 3.5 19.5 3.5 15.5Z"
    return [shell(cup), line(seg(rim_r[0], rim_r[1], 21.5, 2.5)), line(seg(lip[0] + 0.6, lip[1] + 1.5, lip[0] + 0.6, 13.75)),
            shell(bowl)]


@icon("bottle-carrier", CAT, "Bottle carrier: an open crate holding four bottles with a handle rising from the centre divider",
      tags=["bottle crate", "beer carrier", "six pack carrier", "drinks carrier", "bottle tote", "picnic"],
      aliases=["bottle-crate"])
def _(S):
    handle = "M10.5 14V5.5A1.5 1.5 0 0 1 13.5 5.5V14" if S.name == "rounded" else "M10.5 14V4H13.5V14"
    out = [line(handle), shell(rect(2.5, 13, 19, 8.5, rr(S, 2.5)))]
    for x in (3.5, 7, 17, 20.5):
        out += [line(seg(x, 6, x, 13)), dot(x, 5.5, 1.25)]
    return out


@icon("taco-holder", CAT, "Taco holder: a low stand with two tacos standing upright in it, frilly filling showing over the rim",
      tags=["taco stand", "taco rack", "taco night", "mexican food", "tortilla", "serving"],
      aliases=["taco-stand"])
def _(S):
    def taco(cx):
        x0 = cx - 4.5
        top = f"M{fmt(x0)} 10" + "".join(f"A1.5 1.75 0 0 1 {fmt(x0 + 3 * (i + 1))} 10" for i in range(3))
        return top + f"A4.5 5.5 0 0 1 {fmt(x0)} 10Z"
    return [shell(taco(6.75)), shell(taco(17.25)), shell(rect(2.5, 15.5, 19, 6, rr(S, 2))), detail(seg(6.5, 18.5, 17.5, 18.5))]


@icon("sticky-rice-steamer", CAT, "Sticky rice steamer: a woven cone basket sitting in the mouth of a pot with steam rising",
      tags=["huad", "bamboo steamer", "rice steamer", "thai cooking", "lao cooking", "steaming"],
      aliases=["rice-steamer-basket"])
def _(S):
    pot = union("M4.5 14.5H19.5V19.5A2 2 0 0 1 17.5 21.5H6.5A2 2 0 0 1 4.5 19.5Z", rect(2.5, 13.5, 19, 2, L(S, 0, 1)))
    basket = rpoly(S, [(8.5, 13.5), (15.5, 13.5), (19.5, 6.5), (4.5, 6.5)], k=0.5)
    return [line(steam(8, 1.5, 4.5, 1)), line(steam(12, 1.5, 4.5, 1)), line(steam(16, 1.5, 4.5, 1)),
            shell(minus(basket, pot)), detail(seg(8.5, 7.5, 12.5, 12.5)), detail(seg(15.5, 7.5, 11.5, 12.5)), shell(pot)]


@icon("chimney-starter", CAT, "Chimney starter: an upright charcoal cylinder with a side handle and flames rising from the top",
      tags=["charcoal starter", "charcoal chimney", "bbq", "barbecue", "grilling", "lighting coals"],
      aliases=["charcoal-chimney"])
def _(S):
    handle = rpoly(S, [(16, 13), (20.5, 13), (20.5, 18)], closed=False, k=0.6)
    return [solid(flame(9.5, 1.5, 9, 3.25)), solid(flame(14.25, 4, 9, 2.25)), shell(rect(5.5, 10, 11, 11.5, rr(S, 2))),
            detail(seg(5.5, 14, 16.5, 14)), dot(8.75, 18, 0.9), dot(13.25, 18, 0.9), line(handle)]


@icon("stove-lighter", CAT, "Stove lighter: a long thin wand with a trigger grip and a small flame at the tip",
      tags=["gas lighter", "long lighter", "candle lighter", "grill lighter", "igniter", "barbecue"],
      aliases=["candle-lighter"])
def _(S):
    trigger = rpoly(S, [(9.75, 20.5), (7.25, 20.5), (7.25, 23.5)], closed=False, k=0.6)
    return tilt([solid(flame(12, -2.5, 4.5, 1.9)), line(seg(12, 4.5, 12, 19)), shell(rect(9.75, 18.5, 4.5, 9, rr(S, 2))), line(trigger)])


@icon("cookbook-stand", CAT, "Cookbook stand: an open book with lines of text resting upright in a trough-shaped stand",
      tags=["recipe stand", "book holder", "recipe book holder", "reading stand", "recipes", "kitchen counter"],
      aliases=["recipe-stand"])
def _(S):
    book = rpoly(S, [(2.5, 3.5), (12, 5.5), (21.5, 3.5), (21.5, 15), (12, 17), (2.5, 15)], k=0.6)
    stand = rpoly(S, [(4, 18), (4, 21.5), (20, 21.5), (20, 18)], closed=False, k=0.6)
    return [shell(book), detail(seg(12, 5.5, 12, 17)), detail(seg(5.5, 8.5, 9.5, 9.25)), detail(seg(5.5, 11.5, 9.5, 12.25)),
            detail(seg(14.5, 9.25, 18.5, 8.5)), detail(seg(14.5, 12.25, 18.5, 11.5)), line(stand)]


@icon("squeezing-lemon", CAT, "Squeezing lemon: a fist pressing a lemon half with juice drops falling from it",
      tags=["juicing", "citrus juice", "lemon juice", "hand squeezing", "lemonade", "cooking"],
      aliases=["juicing-lemon"])
def _(S):
    lemon = "M3.5 15.5C4.5 12 8 10.75 12 10.75C16 10.75 19.5 12 20.5 15.5Z"
    return [shell(rect(5, 2, 14, 7.5, rr(S, 3))), detail(seg(8.5, 5.5, 8.5, 9.5)), detail(seg(12, 5.5, 12, 9.5)), detail(seg(15.5, 5.5, 15.5, 9.5)),
            shell(lemon), solid(drop(8.5, 16.5, 21.5)), solid(drop(15.5, 16.5, 21.5))]


@icon("utensil-rail", CAT, "Utensil rail: a wall rail with a ladle, a spatula and a whisk hanging from it",
      tags=["hanging utensils", "kitchen rail", "wall rail", "cooking tools", "utensil hooks", "kitchen storage"],
      aliases=["utensil-hanger"])
def _(S):
    ladle = "M3.5 12H7.5A2 4.5 0 0 1 3.5 12Z"
    return [line(seg(2, 3, 22, 3)), line(seg(5.5, 3, 5.5, 12)), shell(ladle),
            line(seg(12, 3, 12, 10)), shell(rect(10, 10, 4, 10, rr(S, 1.5))),
            line(seg(18.5, 3, 18.5, 8)), shell(ellipse(18.5, 14.5, 2.5, 6.5)), detail(seg(18.5, 8, 18.5, 21))]


@icon("mesh-food-cover", CAT, "Mesh food cover: a collapsible mesh dome with ribs and a small knob over a plate",
      tags=["food tent", "fly cover", "picnic cover", "mesh dome", "food net", "outdoor dining"],
      aliases=["food-tent"])
def _(S):
    dome = union("M3.5 18A8.5 10 0 0 1 20.5 18Z", rect(2, 17.5, 20, 3, L(S, 0.5, 1.5)))
    return [dot(12, 3.75, 1.75), shell(dome), detail(seg(9, 9, 9, 17.5)), detail(seg(15, 9, 15, 17.5)), detail(seg(5.5, 13, 18.5, 13))]


def scallop(cx, cy, r, a0, a1, n, depth):
    """Points along an arc from a0 to a1 (degrees, clockwise on screen) with alternating radius r and r - depth."""
    pts = []
    for i in range(n + 1):
        a = a0 + (a1 - a0) * i / n
        pts.append(pt_on(cx, cy, r if i % 2 == 0 else r - depth, a))
    return pts


@icon("fish-scaler", CAT, "Fish scaler: a short handle with a toothed head, scales flying off to the side",
      tags=["scale remover", "fish descaler", "scaling fish", "fishmonger", "cleaning fish", "seafood prep"],
      aliases=["fish-descaler"])
def _(S):
    head = [shell(rect(6.5, 3.5, 11, 8.5, rr(S, 2.5))), hole(circle(9.5, 6.5, 0.8)), hole(circle(12, 6.5, 0.8)), hole(circle(14.5, 6.5, 0.8)),
            hole(circle(9.5, 9, 0.8)), hole(circle(12, 9, 0.8)), hole(circle(14.5, 9, 0.8)),
            line(seg(12, 12, 12, 13.5)), shell(rect(9.75, 13.5, 4.5, 9, rr(S, 2)))]
    return tr(head, 45, 12, 12) + [dot(5.5, 6, 1.1), dot(9, 3.25, 1.1), dot(4, 10.5, 1.1)]


@icon("spaghetti-measure", CAT, "Spaghetti measure: a flat disc with a handle and round holes that grow larger along a diagonal",
      tags=["pasta measure", "pasta portion", "pasta gauge", "portion control", "spaghetti portion", "cooking tool"],
      aliases=["pasta-measure"])
def _(S):
    body = union(circle(12, 9.5, 8.5), rect(9.75, 16, 4.5, 6, L(S, 0.5, 1.75)))
    return [shell(body), hole(circle(7, 6, 0.75)), hole(circle(9.5, 7.75, 1.05)), hole(circle(12.5, 9.75, 1.4)), hole(circle(16, 12.25, 1.8))]


@icon("ice-sphere-mold", CAT, "Ice sphere mold: a round two-part mold with a seam around its middle and a small fill hole on top",
      tags=["ice ball mold", "round ice", "whiskey ice", "cocktail ice", "ice maker", "bar tool"],
      aliases=["ice-ball-mold"])
def _(S):
    return [shell(union(circle(12, 12, 9), rect(2.5, 10.5, 19, 3, L(S, 0.5, 1.5)))), detail(seg(3.5, 12, 20.5, 12)), hole(circle(12, 6.25, 1.25))]


@icon("citrus-zester", CAT, "Citrus zester: a long flat grater blade with tiny holes on a short handle, zest curls beside it",
      tags=["lemon zester", "zesting", "lime zest", "grater", "peel", "kitchen tool"],
      aliases=["lemon-zester"])
def _(S):
    head = [shell(rect(8.5, -1, 7, 14, rr(S, 2.5))), hole(circle(10.5, 2.5, 0.75)), hole(circle(13.5, 2.5, 0.75)),
            hole(circle(10.5, 5.75, 0.75)), hole(circle(13.5, 5.75, 0.75)), hole(circle(10.5, 9, 0.75)), hole(circle(13.5, 9, 0.75)),
            line(seg(12, 13, 12, 14.5)), shell(rect(9.75, 14.5, 4.5, 8.5, rr(S, 2)))]
    return tr(head, 45, 12, 12) + [line("M4 5C6.5 3.5 8 5.5 6.5 6.5C5.5 7 4.5 6 5.25 5.25"), line("M3 12C5 10.5 6.5 12.5 5 13.5")]


@icon("pineapple-corer", CAT, "Pineapple corer: a tall tube with a spiral blade and a bar handle on top, cutting a pineapple ring",
      tags=["pineapple slicer", "fruit corer", "apple corer", "pineapple ring", "fruit prep", "kitchen tool"],
      aliases=["pineapple-slicer"])
def _(S):
    tube = rect(9, 5, 6, 13.5, rr(S, 2))
    return [shell(rect(4.5, 1.75, 15, 3, L(S, 0.5, 1.5))), shell(tube), detail(seg(9, 9, 15, 11)), detail(seg(9, 13, 15, 15)),
            shell(ellipse(12, 18.5, 9.5, 3))]


@icon("molinillo", CAT, "Molinillo: a carved wooden whisk stick with a bulbous head and loose rings around it",
      tags=["mexican chocolate whisk", "hot chocolate whisk", "wooden whisk", "frother", "chocolate", "kitchen tool"],
      aliases=["chocolate-whisk"])
def _(S):
    head = "M12 9C16.5 9 17 13 15.5 16C14.5 18.5 13.5 20 12 22C10.5 20 9.5 18.5 8.5 16C7 13 7.5 9 12 9Z" if S.name == "rounded" else \
        "M12 9L15.75 11.5L15.5 16L12 22L8.5 16L8.25 11.5Z"
    return tilt([line(seg(12, 0, 12, 9)), shell(head), line(seg(6.75, 12.5, 17.25, 12.5)), line(seg(7.5, 16.5, 16.5, 16.5))])


@icon("mooncake-mold", CAT, "Mooncake mold: a plunger press with a top handle pressing a patterned round cake",
      tags=["mooncake press", "moon cake mould", "pastry stamp", "mid autumn festival", "baking", "dessert mold"],
      aliases=["mooncake-press"])
def _(S):
    return [shell(rect(7.5, 2, 9, 3, L(S, 0.5, 1.5))), line(seg(12, 5, 12, 8.5)), shell(rect(5.5, 8.5, 13, 7, rr(S, 2))),
            shell(ellipse(12, 19, 8.5, 2.5)), hole(circle(9.5, 19, 0.7)), hole(circle(12, 19, 0.7)), hole(circle(14.5, 19, 0.7))]


@icon("spit-roast", CAT, "Spit roast: a joint of meat on a horizontal spit between two posts over flames, with a crank at one end",
      tags=["rotisserie", "open fire roast", "hog roast", "campfire cooking", "barbecue", "roasting"],
      aliases=["hog-roast"])
def _(S):
    return [line(seg(2.5, 9, 21, 9)), line(rpoly(S, [(21, 9), (21.5, 5), (19, 5)], closed=False, k=0.5)),
            shell(ellipse(12, 9, 6, 4)), line(seg(4.5, 9, 4.5, 20)), line(seg(19.5, 9, 19.5, 20)),
            solid(flame(9.5, 14.5, 21.5, 2)), solid(flame(14.5, 14.5, 21.5, 2))]


@icon("noodle-basket", CAT, "Noodle basket: a deep cylindrical wire basket with a long straight handle",
      tags=["noodle strainer", "pasta basket", "boiling basket", "fry basket", "ramen", "kitchen tool"],
      aliases=["noodle-strainer"])
def _(S):
    body = "M5.5 4.5V12.5A6.5 2.25 0 0 0 18.5 12.5V4.5A6.5 2.25 0 0 0 5.5 4.5Z"
    return tilt([shell(body), detail("M5.5 4.5A6.5 2.25 0 0 0 18.5 4.5"), detail(seg(9.5, 7, 9.5, 14.5)), detail(seg(14.5, 7, 14.5, 14.5)),
                 line(seg(12, 15, 12, 25))])


@icon("salt-block", CAT, "Salt block: a rectangular salt slab with crystal facets and a thin slice of meat cooking on top",
      tags=["himalayan salt block", "salt slab", "salt plate", "searing", "grilling stone", "cooking block"],
      aliases=["salt-slab"])
def _(S):
    def gem(x, y):
        return poly([(x, y - 1.5), (x + 1.25, y), (x, y + 1.5), (x - 1.25, y)], closed=True)
    return [line(steam(9, 1.5, 5)), line(steam(15, 1.5, 5)), shell(rect(5.5, 6.5, 13, 3.5, rr(S, 1.75))),
            shell(rect(3, 12, 18, 9.5, rr(S, 2))), hole(gem(7.5, 16.75)), hole(gem(12, 15.5)), hole(gem(16.5, 17))]


@icon("grilling-plank", CAT, "Grilling plank: a rectangular wooden plank with grain lines and a fish fillet lying on it",
      tags=["cedar plank", "plank salmon", "smoking plank", "wood plank", "fish fillet", "barbecue"],
      aliases=["cedar-plank"])
def _(S):
    fillet = "M3.5 12.5C6 7 14 5.5 20.5 10.5C17 13 7 13.5 3.5 12.5Z"
    return [shell(fillet), detail(seg(9, 8.5, 10.5, 11.75)), detail(seg(13.5, 8, 14.5, 11.75)),
            shell(rect(2.5, 14, 19, 7.5, rr(S, 2))), detail(seg(5.5, 17.75, 10, 17.75)), detail(seg(13, 17.75, 18.5, 17.75))]


@icon("metate", CAT, "Metate: a sloped grinding stone on short legs with a cylindrical hand stone resting across it",
      tags=["grinding stone", "mortar stone", "mano y metate", "corn grinding", "mexican kitchen", "stone mill"],
      aliases=["grinding-stone"])
def _(S):
    slab = rot(rect(2.5, 10.5, 19, 4, L(S, 0.5, 1.5)), 12, 12, 12)
    mano = rot(rect(7, 5.5, 10, 4, L(S, 1, 2)), 12, 12, 12)
    return [shell(mano), shell(slab), line(seg(5.25, 13.5, 5.25, 21)), line(seg(18.5, 16.25, 18.5, 21))]


@icon("roti-rolling-board", CAT, "Roti rolling board: a round raised board on short feet with a tapered rolling pin lying across it",
      tags=["chapati board", "chakla belan", "dough rolling board", "indian kitchen", "flatbread", "rolling pin"],
      aliases=["chakla-belan"])
def _(S):
    pin = rpoly(S, [(5.5, 14), (8.5, 12.25), (15.5, 12.25), (18.5, 14), (15.5, 15.75), (8.5, 15.75)], k=1.2)
    return [shell(ellipse(12, 14, 9.5, 5.5)), detail(pin), line(seg(6.5, 18.5, 6.5, 21.5)), line(seg(17.5, 18.5, 17.5, 21.5))]


@icon("rice-ball-mold", CAT, "Rice ball mold: a triangular mould with a press lid on top and a stem handle",
      tags=["onigiri mold", "onigiri maker", "triangle rice mold", "japanese cooking", "bento", "rice press"],
      aliases=["onigiri-mold"])
def _(S):
    tri = rpoly(S, [(12, 7.5), (20.5, 21.5), (3.5, 21.5)], k=1)
    inner = rpoly(S, [(12, 12.5), (16.75, 19), (7.25, 19)], k=0.5)
    return [shell(rect(8, 2, 8, 2.5, L(S, 0.5, 1.25))), line(seg(12, 4.5, 12, 7.5)), shell(tri), detail(inner)]


@icon("sushi-rice-tub", CAT, "Sushi rice tub: a wide shallow wooden tub with two metal bands and a flat paddle resting on the rim",
      tags=["hangiri", "sushi oke", "rice mixing tub", "sushi rice", "wooden tub", "japanese cooking"],
      aliases=["hangiri"])
def _(S):
    tub = rpoly(S, [(2.5, 11.5), (21.5, 11.5), (19.5, 21), (4.5, 21)], k=0.6)
    return [shell(ellipse(6.5, 7.5, 3.75, 2.25)), line(seg(10, 7.5, 21.5, 7.5)), shell(tub), detail(seg(3.5, 15.25, 20.5, 15.25)), detail(seg(4, 18.5, 20, 18.5))]


@icon("bamboo-wok-brush", CAT, "Bamboo wok brush: a bundle of thin bamboo strips tied with a band and fanning out at the bottom",
      tags=["wok cleaning brush", "bamboo brush", "cleaning brush", "dish brush", "chinese kitchen", "scrubbing"],
      aliases=["wok-brush"])
def _(S):
    out = [line(seg(11 + 0.5 * i, 2, 5.5 + 3.25 * i, 21.5)) for i in range(5)]
    return out + [shell(rect(9, 6.5, 6, 3.5, L(S, 0.5, 1.75)))]


@icon("coconut-scraper", CAT, "Coconut scraper: a low stool with a serrated round blade sticking out from one end",
      tags=["coconut grater", "coconut shredder", "coconut scraping", "kitchen stool", "caribbean kitchen", "south asian kitchen"],
      aliases=["coconut-grater"])
def _(S):
    n = 20
    teeth = [pt_on(16.5, 9, 4.5 if i % 2 == 0 else 3.4, i * 360 / n) for i in range(n)]
    return [shell(poly(teeth, closed=True, r=S.r * 0.3)), shell(rect(2.5, 12, 12, 3.5, L(S, 0.5, 1.5))), line(seg(5, 15.5, 3.5, 21.5)),
            line(seg(12, 15.5, 13.5, 21.5))]


@icon("spaetzle-maker", CAT, "Spaetzle maker: a flat perforated plate with a handle and a box hopper that slides along it",
      tags=["spatzle press", "noodle maker", "german noodles", "dough dumplings", "pasta tool", "kitchen tool"],
      aliases=["spatzle-maker"])
def _(S):
    hopper = rpoly(S, [(3.5, 2.5), (13.5, 2.5), (12, 14), (5, 14)], k=0.5)
    return [shell(hopper), shell(rect(2.5, 14, 15, 5.5, rr(S, 2))), hole(circle(6.25, 16.75, 0.9)), hole(circle(10, 16.75, 0.9)),
            hole(circle(13.75, 16.75, 0.9)), shell(rect(17.5, 15, 4, 3.5, rr(S, 1.5)))]