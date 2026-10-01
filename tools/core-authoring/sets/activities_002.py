"""TypeIcon Core: activities and actions (batch 002).

Everyday actions drawn as stick figures in the style of people/person-walking: a solid head (r 2.25) over
2 px limbs, with any object as a closed shell. Polylines use the style fillet (S.r) so Line has sharp elbows
and Rounded soft ones. Where a figure overlaps an object, the object is drawn as a layer behind the figure and
cut away around it with a gap (same technique as sets/people.py).
"""
import math

from dsl import LINE, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from dsl import D, I, P, ST, U, filled_region
from geometry import fmt, path_to_d, polar, transform_path

CAT = "activities"


# --------------------------------------------------------------------------- layering (as in sets/people.py)

def _paint(parts, S):
    regs = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        else:
            regs.append(ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4))))
    return U(*regs)


def _sil(parts, S):
    regs = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        elif p.kind == "shell":
            regs.append(U(P(p.d), ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4)))))
        else:
            regs.append(ST(p.d, 2.0, S.cap, S.join))
    return U(*regs)


def _grow(region, g):
    if g <= 0:
        return region
    return U(region, ST(path_to_d(region), 2 * g, "round", "round"))


def _unpack(layer, gap, fgap):
    if isinstance(layer, tuple):
        return layer
    return layer, gap, fgap


def _stroke_layers(S, layers, gap, fgap):
    parts, halo, _ = _unpack(layers[0], gap, fgap)
    out = list(parts)
    cover = _grow(_sil(parts, S), halo)
    for layer in layers[1:]:
        parts, halo, _ = _unpack(layer, gap, fgap)
        if not parts:
            continue
        vis = D(_paint(parts, S), cover)
        if abs(vis.area) > 0.01:
            out.append(solid(path_to_d(vis)))
        cover = U(cover, _grow(_sil(parts, S), halo))
    return out


def _filled_layers(layers, gap, fgap):
    parts, _, fh = _unpack(layers[0], gap, fgap)
    result = filled_region(parts)
    cover = _grow(result, fh)
    for layer in layers[1:]:
        parts, _, fh = _unpack(layer, gap, fgap)
        if not parts:
            continue
        f = filled_region(parts)
        result = U(result, D(f, cover))
        cover = U(cover, _grow(f, fh))
    return result


def figure(name, desc, tags, aliases=(), gap=1.5, fgap=None):
    """Register an icon drawn as layers: fn(S) -> [front layer, layer behind, ...]."""
    fg = gap if fgap is None else fgap

    def deco(fn):
        icon(name, CAT, desc, tags=tags, aliases=aliases,
             filled=lambda: _filled_layers(fn(LINE), gap, fg))(lambda S: _stroke_layers(S, fn(S), gap, fg))
        return fn
    return deco


# --------------------------------------------------------------------------- helpers

def pick(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


def head(x, y, r=2.25):
    return dot(x, y, r)


def limb(S, *pts):
    return line(poly(list(pts), r=S.r))


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def arrow_arc(S, cx, cy, r, a0, a1, size=2.5):
    """Clockwise arc from a0 to a1 with an open arrowhead at a1."""
    tip = polar(cx, cy, r, a1)
    tang = math.radians(a1 + 90)  # clockwise travel direction
    back = (tip[0] - size * math.cos(tang), tip[1] - size * math.sin(tang))
    nx, ny = math.cos(math.radians(a1)), math.sin(math.radians(a1))
    w1 = (back[0] + nx * size * 0.8, back[1] + ny * size * 0.8)
    w2 = (back[0] - nx * size * 0.8, back[1] - ny * size * 0.8)
    return [line(arc(cx, cy, r, a0, a1)), line(poly([w1, tip, w2], r=S.r * 0.4))]


def xf(d, ox=0.0, oy=0.0, deg=0.0, k=1.0, c=(12.0, 12.0)):
    """Scale a closed shape by k about c, rotate it clockwise by deg about c, then shift it by (ox, oy)."""
    a = math.radians(deg)
    ca, sa = math.cos(a) * k, math.sin(a) * k
    m = (ca, sa, -sa, ca, c[0] - ca * c[0] + sa * c[1] + ox, c[1] - sa * c[0] - ca * c[1] + oy)
    return path_to_d(transform_path(P(d), m))


def xp(p, ox=0.0, oy=0.0, deg=0.0, k=1.0, c=(12.0, 12.0)):
    a = math.radians(deg)
    x, y = (p[0] - c[0]) * k, (p[1] - c[1]) * k
    return (c[0] + x * math.cos(a) - y * math.sin(a) + ox, c[1] + x * math.sin(a) + y * math.cos(a) + oy)


def side_head(S, mouth=False, neck=20.5):
    """Closed head and neck in profile facing right (box 3..18 x 2.5..neck). Line: pointed nose and chin."""
    nose = "L18 12.5L16 13" if S.name == "line" else "L17.6 11.8Q18.3 13 17 13L16 13"
    lips = "L16 13.6L13.5 14.4L16 15.2" if mouth else ""
    chin = "L16 17H13" if S.name == "line" else "L16 15.8Q16 17 14.8 17H13"
    return f"M6.5 {fmt(neck)}V16.5C4.2 15 3 12.6 3 10A6.5 6.5 0 0 1 16 9.2{nose}{lips}{chin}V{fmt(neck)}Z"


def small_head(S, mouth=False, oy=0.0, k=0.85):
    """Profile head scaled about its back (x 3) so objects fit in front of the face; the neck reaches y 21.5."""
    neck = 12 + (21.5 - oy - 12) / k
    return xf(side_head(S, mouth, neck), 0, oy, 0, k, (3, 12))


def tilted_head(S, deg, ox=0.0, oy=0.0, k=0.85, mouth=False):
    """Profile head tipped back by deg (negative = face turned up), neck cut flat at y 21.5."""
    d = xf(side_head(S, mouth, 30), ox, oy, deg, k, (10, 12))
    return path_to_d(I(P(d), P(rect(-2, -2, 28, 23.5))))


def bust(S, cx=12.0, hy=8.0, hr=4.5, top=15.5, hw=7.5, bottom=21.5):
    """Head over rounded shoulders (front or back view)."""
    r = min(hw - (1.0 if S.name != "line" else 2.5), bottom - top)
    x0, x1 = cx - hw, cx + hw
    sh = (f"M{fmt(x0)} {fmt(bottom)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + r)} {fmt(top)}"
          f"H{fmt(x1 - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(bottom)}Z")
    return [shell(circle(cx, hy, hr)), shell(sh)]


def line_in(a, b):
    return seg(a[0], a[1], b[0], b[1])


def _shoulders(S, cx=12.0, top=15.5, hw=8.5, bottom=21.5):
    r = min(hw - (1.0 if S.name != "line" else 2.5), bottom - top)
    x0, x1 = cx - hw, cx + hw
    return (f"M{fmt(x0)} {fmt(bottom)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + r)} {fmt(top)}"
            f"H{fmt(x1 - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(bottom)}")


# ============================================================================ body movement

@figure("leaning-on-wall", "A person leaning a shoulder against a wall",
        tags=["lean", "leaning", "wall", "relax", "waiting", "casual"])
def _(S):
    return [[head(15, 4.75),
             limb(S, (18.5, 9.5), (14, 15)),
             limb(S, (8.5, 21), (14, 15), (13, 21)),
             line(seg(20.5, 2, 20.5, 22))]]


@figure("reaching-high-shelf", "A person reaching up to a box on a high shelf",
        tags=["reach", "shelf", "tiptoe", "stretch", "high", "storage"])
def _(S):
    return [[head(6.25, 6.5),
             limb(S, (13, 3.5), (8.5, 10.5), (5.5, 13.5)),
             limb(S, (8.5, 10.5), (8.5, 15.5)),
             limb(S, (6.5, 21), (8.5, 15.5), (10.5, 21)),
             line(seg(12, 8.5, 21.5, 8.5)),
             shell(rect(15, 2.5, 5.5, 5, min(S.R, 1.5)))]]


@figure("person-pointing", "A person in profile pointing forward with an outstretched arm",
        tags=["point", "pointing", "direct", "show", "that way", "indicate"])
def _(S):
    return [[head(8, 4.5),
             limb(S, (8, 9.5), (20, 9.5)),
             limb(S, (8, 9.5), (8, 15)),
             limb(S, (5, 21), (8, 15), (11, 21))]]


@figure("person-throwing", "A person with one arm drawn back overhead about to throw a ball",
        tags=["throw", "pitch", "toss", "ball", "sport", "launch"])
def _(S):
    return [[head(12.5, 5),
             shell(circle(4.5, 4.5, 1.75)),
             limb(S, (6, 7.5), (8, 11), (12, 10), (17, 11), (19.5, 8.5)),
             limb(S, (12, 10), (11, 15)),
             limb(S, (6.5, 21), (11, 15), (15, 17.5), (16, 21))]]


@figure("person-catching", "A person with both hands raised catching a ball",
        tags=["catch", "ball", "receive", "hands up", "sport", "game"])
def _(S):
    return [[shell(circle(12, 4.5, 1.75)),
             head(12, 10.5),
             limb(S, (8, 4.5), (7.5, 14.5), (16.5, 14.5), (16, 4.5)),
             limb(S, (12, 14.5), (12, 17.5)),
             limb(S, (9, 21.5), (12, 17.5), (15, 21.5))]]


@figure("falling-person", "A person tipped backwards in mid air with arms flailing",
        tags=["fall", "falling", "accident", "drop", "tumble", "hazard"])
def _(S):
    return [[head(5.5, 15.5),
             limb(S, (9.5, 13.5), (16, 12)),
             limb(S, (4, 9), (9.5, 13.5), (8, 20)),
             limb(S, (21, 16.5), (16, 12), (20, 7)),
             line(seg(9, 3, 9, 7)), line(seg(13, 2, 13, 6))]]


@figure("slipping-person", "A person slipping on a puddle, one foot sliding forward",
        tags=["slip", "slippery", "wet floor", "puddle", "accident", "caution"])
def _(S):
    return [[head(8, 4.5),
             limb(S, (4, 9.5), (9.5, 9.5), (14, 6.5)),
             limb(S, (9.5, 9.5), (11, 14.5)),
             limb(S, (8, 19), (11, 14.5), (18.5, 17)),
             shell(ellipse(15.5, 20.75, 6, 1)),
             dot(17, 13, 1), dot(20.5, 14, 1)]]


@figure("backflip", "An upside-down person in mid air under an arcing arrow",
        tags=["backflip", "flip", "acrobatics", "gymnastics", "stunt", "parkour"])
def _(S):
    return [[head(12, 18.5),
             limb(S, (12, 14), (12, 10)),
             limb(S, (8, 17), (12, 14), (16, 17)),
             limb(S, (9, 7), (12, 10), (15, 7)),
             *arrow_arc(S, 12, 12, 9.5, 215, 325)]]


@figure("person-pushing", "A person leaning forward pushing a large box",
        tags=["push", "pushing", "shove", "effort", "move", "force"])
def _(S):
    return [[head(9, 6),
             limb(S, (14, 9), (11, 9.5), (8, 13.5)),
             limb(S, (14, 13), (11, 12.5)),
             limb(S, (3, 20.5), (8, 13.5), (9.5, 17.5), (9, 21)),
             shell(rect(15, 7, 6.5, 14, min(S.R, 2)))]]


@figure("person-pulling", "A person leaning back pulling a crate on a rope",
        tags=["pull", "pulling", "tug", "rope", "drag", "haul"])
def _(S):
    return [[head(4.5, 5.5),
             limb(S, (7.5, 9.5), (13, 11)),
             limb(S, (7.5, 9.5), (10, 15)),
             limb(S, (8.5, 21), (10, 15), (14, 20.5)),
             line(seg(13, 11, 17.5, 15)),
             shell(rect(16.5, 15, 5, 6, min(S.R, 1.5)))]]


@figure("climbing-stairs", "A person stepping up a flight of stairs",
        tags=["stairs", "steps", "climb", "upstairs", "walk up", "staircase"])
def _(S):
    return [[head(9, 3.5),
             limb(S, (5.5, 11), (8.5, 8), (11.5, 10.5)),
             limb(S, (8.5, 8), (8, 12)),
             limb(S, (5, 20), (8, 12), (12, 12.5), (12, 16)),
             line(poly([(2, 21), (8.5, 21), (8.5, 17), (15, 17), (15, 13), (21.5, 13)], r=S.r * 0.3))]]


@figure("climbing-ladder", "A person climbing an upright ladder",
        tags=["ladder", "climb", "rungs", "up", "maintenance", "reach"])
def _(S):
    return [[head(8, 5.5),
             limb(S, (14, 4), (9.5, 9.5), (14, 12)),
             limb(S, (9.5, 9.5), (9, 14)),
             limb(S, (8, 21.5), (9, 14), (14, 16.5))],
            [line(seg(14, 2, 14, 22)), line(seg(20, 2, 20, 22)),
             line(seg(14, 6.5, 20, 6.5)), line(seg(14, 11.5, 20, 11.5)), line(seg(14, 16.5, 20, 16.5))]]


@figure("riding-escalator", "A person standing on an escalator holding the handrail",
        tags=["escalator", "moving stairs", "mall", "station", "up", "ride"])
def _(S):
    return [[head(9, 5),
             limb(S, (9, 9.5), (9, 14)),
             limb(S, (9, 9.5), (13, 10)),
             limb(S, (7.5, 17.5), (9, 14), (10.5, 17.5))],
            [line(poly([(2, 21.5), (6, 21.5), (6, 18.5), (12, 18.5), (21.5, 11.5)], r=S.r * 0.5)),
             line(poly([(2.5, 16), (4, 14), (21, 3.5)], r=S.r))]]


@figure("taking-elevator", "A person inside an open elevator beside the call buttons",
        tags=["elevator", "lift", "floor", "building", "up and down", "ride"])
def _(S):
    tri_u = poly([(18.5, 8), (20.5, 10.5), (16.5, 10.5)], closed=True)
    tri_d = poly([(16.5, 13.5), (20.5, 13.5), (18.5, 16)], closed=True)
    return [[shell(rect(2.5, 2.5, 12, 19, min(S.R, 2))),
             dot(8.5, 6.75, 2),
             detail(seg(8.5, 10.5, 8.5, 21.5)),
             detail(poly([(5.5, 15), (8.5, 10.5), (11.5, 15)], r=S.r)),
             solid(tri_u), solid(tri_d)]]


@figure("tripping-over", "A person pitching forward after catching a foot on a box",
        tags=["trip", "tripping", "stumble", "obstacle", "hazard", "fall"])
def _(S):
    return [[head(18.5, 6),
             limb(S, (15, 9.5), (10, 14)),
             limb(S, (21, 13), (15, 9.5), (12, 6.5)),
             limb(S, (7, 15.5), (10, 14), (14, 17.5), (16.5, 21)),
             shell(rect(3, 16.5, 5, 4.5, min(S.R, 1.5)))]]


@figure("person-crouching", "A person crouched low on bent knees with arms held forward",
        tags=["crouch", "squat", "kneel", "low", "duck", "hide"])
def _(S):
    return [[head(12.5, 5),
             limb(S, (19.5, 10.5), (11.5, 9.5), (7.5, 14.5)),
             limb(S, (7.5, 14.5), (14.5, 15), (12.5, 20)),
             line(seg(2, 21.5, 22, 21.5))]]


@figure("person-waving-arms", "A person waving both arms high to get attention",
        tags=["wave", "signal", "attention", "help", "hello", "cheer"])
def _(S):
    return [[head(12, 8.5),
             limb(S, (5.5, 5), (8.5, 12.5), (15.5, 12.5), (18.5, 5)),
             limb(S, (12, 12.5), (12, 16.5)),
             limb(S, (9, 21.5), (12, 16.5), (15, 21.5)),
             line(arc(5.5, 5, 3.5, 185, 250)), line(arc(18.5, 5, 3.5, 290, 355))]]


@figure("walking-with-umbrella", "A person walking in the rain under an open umbrella",
        tags=["umbrella", "rain", "walk", "wet weather", "shelter", "rainy day"])
def _(S):
    return [[shell("M2.5 8A7.5 5.5 0 0 1 17.5 8Z"),
             line(seg(10, 8, 10, 12.5)),
             head(7, 11.5, 2),
             limb(S, (7.5, 14.5), (10, 12.5)),
             limb(S, (7.5, 14.5), (7, 17.5)),
             limb(S, (4.5, 21.5), (7, 17.5), (10, 21.5)),
             line(seg(20.5, 9, 19.5, 12)), line(seg(21, 15, 20, 18)), line(seg(16.5, 13, 15.5, 16))]]


@figure("walking-hand-in-hand", "Two people side by side holding hands",
        tags=["hand in hand", "holding hands", "couple", "friends", "together", "walk"])
def _(S):
    return [[head(6.5, 4.5), head(17.5, 4.5),
             limb(S, (3.5, 14), (6.5, 9.5), (12, 13), (17.5, 9.5), (20.5, 14)),
             limb(S, (6.5, 9.5), (6.5, 15)), limb(S, (17.5, 9.5), (17.5, 15)),
             limb(S, (4, 21), (6.5, 15), (9, 21)), limb(S, (15, 21), (17.5, 15), (20, 21))]]


@figure("running-late", "A person running with a briefcase and a clock above",
        tags=["late", "hurry", "rush", "deadline", "commute", "running"])
def _(S):
    return [[head(16.5, 7.5),
             shell(circle(6, 5.5, 3.5)), detail(poly([(6, 3.5), (6, 5.5), (7.5, 5.5)], r=S.r * 0.4)),
             limb(S, (14.5, 11.5), (18, 14), (20.5, 12)),
             limb(S, (14.5, 11.5), (12, 16)),
             limb(S, (14.5, 11.5), (10.5, 12.5), (8, 14)),
             shell(rect(3.5, 14.5, 6, 4.5, min(S.R, 1.5))),
             limb(S, (8.5, 21.5), (12, 16), (16, 18.5), (15.5, 21.5))]]


@figure("carrying-on-head", "A person balancing a jar on the head with one hand",
        tags=["carry", "balance", "jar", "water pot", "load", "head carry"])
def _(S):
    jar = ("M10 7.5H14C16 7.5 16.5 5.5 15.5 4.5L14 3.5V2H10V3.5L8.5 4.5C7.5 5.5 8 7.5 10 7.5Z" if S.name == "line"
           else "M10.5 7.5H13.5C16.5 7.5 17 4.5 14 3.5V2.5A0.5 0.5 0 0 0 13.5 2H10.5A0.5 0.5 0 0 0 10 2.5V3.5C7 4.5 7.5 7.5 10.5 7.5Z")
    return [[shell(jar),
             head(12, 10),
             limb(S, (17.5, 5.5), (17, 14), (7, 14), (5.5, 18.5)),
             limb(S, (12, 14), (12, 17.5)),
             limb(S, (9.5, 21.5), (12, 17.5), (14.5, 21.5))]]


@figure("carrying-box", "A person walking with a large box held against the chest",
        tags=["carry", "box", "moving", "delivery", "parcel", "lift"])
def _(S):
    return [[shell(rect(11.5, 7.5, 9.5, 8.5, min(S.R, 1.5))), detail(seg(11.5, 11, 21, 11)),
             head(7, 4.5),
             limb(S, (7, 9), (11.5, 12.5)),
             limb(S, (7, 9), (7, 15)),
             limb(S, (4, 21), (7, 15), (10.5, 21))]]


@figure("carrying-shopping-bags", "A person holding a shopping bag in each hand",
        tags=["shopping", "bags", "shopper", "purchases", "mall", "carry"])
def _(S):
    def bag(x):
        return [shell(rect(x, 15.5, 5.5, 6, min(S.R, 1.5))), line(f"M{fmt(x + 1.25)} 15.5V14.25A1.5 1.5 0 0 1 {fmt(x + 4.25)} 14.25V15.5")]
    return [[head(12, 4.5),
             limb(S, (5.25, 12.75), (7.5, 9.5), (16.5, 9.5), (18.75, 12.75)),
             limb(S, (12, 9.5), (12, 15)),
             limb(S, (10.5, 21.5), (12, 15), (13.5, 21.5))] + bag(2.5) + bag(16)]


@figure("waking-from-sleep", "A person sitting up in bed stretching with the sun rising",
        tags=["wake up", "morning", "rise", "bed", "good morning", "alarm"])
def _(S):
    rays = [line(seg(*polar(18.5, 5.5, 3.5, a), *polar(18.5, 5.5, 4.25, a))) for a in (180, 225, 270, 315, 0)]
    return [[head(8, 7.5, 2),
             limb(S, (4, 3.5), (4, 11), (12, 11), (12, 3.5)),
             limb(S, (8, 11), (8, 16)),
             shell(rect(10.5, 13.5, 11, 3.5, min(S.R, 1.5))),
             line(poly([(2, 12), (2, 21.5)], r=0)), line(poly([(2, 18), (21.5, 18), (21.5, 21)], r=S.r)),
             solid(circle(18.5, 5.5, 2))] + rays]


def _cloud(pts):
    return path_to_d(U(*[P(circle(x, y, r)) for x, y, r in pts]))


@figure("dreaming", "A person asleep in bed with a thought bubble holding a star",
        tags=["dream", "sleep", "night", "imagine", "bed", "rest"])
def _(S):
    star = poly([polar(15.5, 6, 2.2 if k % 2 == 0 else 1, -90 + k * 36) for k in range(10)], closed=True)
    return [[shell(_cloud([(12.5, 6.5, 3), (15.5, 5, 3.5), (18.5, 6.5, 3)])), Part("dot", star),
             dot(8.5, 11, 1),
             head(4.5, 16.5),
             shell(rect(8, 14.5, 13.5, 4, min(S.R, 1.5))),
             line(poly([(2, 20.5), (22, 20.5)], r=0))]]


@figure("dozing-at-desk", "A person asleep with the head on folded arms at a desk",
        tags=["doze", "nap", "tired", "asleep at work", "sleepy", "desk"])
def _(S):
    return [[head(13.5, 9),
             limb(S, (10, 12.5), (17.5, 12.5)),
             limb(S, (10, 12.5), (5, 16.5)),
             limb(S, (5, 16.5), (10, 17), (10, 21.5)),
             line(poly([(8, 15), (21.5, 15)], r=0)), line(seg(19.5, 15, 19.5, 21.5)),
             line(poly([(15, 2.5), (19, 2.5), (15, 6.5), (19, 6.5)], r=0))]]


def _tooth(x):
    """Molar outline, 7.5 wide, crown at y 9 and two roots down to y 21."""
    return (f"M{fmt(x)} 11.5C{fmt(x)} 8.5 {fmt(x + 2.5)} 8.5 {fmt(x + 3.75)} 9.5C{fmt(x + 5)} 8.5 {fmt(x + 7.5)} 8.5 {fmt(x + 7.5)} 11.5"
            f"V15L{fmt(x + 6.5)} 21H{fmt(x + 5)}L{fmt(x + 3.75)} 17L{fmt(x + 2.5)} 21H{fmt(x + 1)}L{fmt(x)} 15Z")


@figure("flossing-teeth", "Dental floss pulled down between two teeth",
        tags=["floss", "dental floss", "teeth", "oral care", "hygiene", "dentist"], gap=1.0)
def _(S):
    return [[limb(S, (5, 2.5), (12, 16.5), (19, 2.5))],
            [shell(_tooth(2.5), stroke_miterlimit="2"), shell(_tooth(14), stroke_miterlimit="2")]]


@figure("gargling", "A head tipped back with bubbles rising from the open mouth",
        tags=["gargle", "mouthwash", "throat", "rinse", "sore throat", "oral care"])
def _(S):
    return [[shell(tilted_head(S, -35, -1.5, 1.5, 0.85, True)),
             dot(16.5, 6, 1.25), dot(19.5, 3.5, 1.5), dot(20.5, 8, 1)]]


@figure("shaving", "A face with shaving foam on the jaw and a razor at the cheek",
        tags=["shave", "razor", "shaving foam", "beard", "grooming", "barber"])
def _(S):
    foam = path_to_d(U(P(circle(6, 15, 2.5)), P(circle(9.5, 17.5, 2.5)), P(circle(13.5, 17, 2.5)), P(rect(6, 14, 7.5, 3.5))))
    return [[shell(rect(16, 7.5, 5.5, 3, min(S.R, 1))), line(seg(18.75, 10.5, 18.75, 21.5))],
            [shell(foam)],
            [shell(circle(10.5, 11, 8)), dot(8, 8.5, 1.1), dot(13, 8.5, 1.1)]]


@figure("combing-hair", "A person drawing a comb through the hair",
        tags=["comb", "hair", "grooming", "brush hair", "hairstyle", "tidy"])
def _(S):
    teeth = [line(seg(x, 7.5, x, 10.5)) for x in (12.5, 16, 19.5)]
    return [[shell(rect(10.5, 3, 11, 4.5, min(S.R, 1.5)))] + teeth,
            bust(S, 8.5, 9.5, 4.5, 16, 6.5)]


@figure("blow-drying-hair", "A hair dryer blowing warm air toward a person's head",
        tags=["hair dryer", "blow dry", "hairdryer", "salon", "styling", "grooming"])
def _(S):
    dryer = path_to_d(U(P(circle(18, 6.5, 3.5)), P(rect(10, 4.5, 8, 4, min(S.R, 1))), P(rect(15.5, 9, 3, 5.5, min(S.R, 1)))))
    return [[shell(dryer), line(seg(3.5, 4, 7.5, 4)), line(seg(3.5, 7.5, 7.5, 7.5))],
            bust(S, 6.5, 13.5, 3.5, 18.5, 5)]


@figure("applying-makeup", "A face with a makeup brush touching the cheek",
        tags=["makeup", "make-up", "blush", "cosmetics", "beauty", "brush"])
def _(S):
    c = (14, 14)
    bristle = pick(S, "M14 14.5L12 12L12.5 9H15.5L16 12Z",
                   "M14 14.5C12.5 14.5 11.8 13 12 11.5L12.5 9H15.5L16 11.5C16.2 13 15.5 14.5 14 14.5Z")
    return [[shell(xf(bristle, 1, -1.5, 40, 1, c)),
             line(poly([xp((14, 7.5), 1, -1.5, 40, 1, c), xp((14, 1.5), 1, -1.5, 40, 1, c)])),
             ],
            [shell(circle(9, 11.5, 7.5)), dot(6.5, 9.5, 1.1), dot(11.5, 9.5, 1.1), detail(seg(7.5, 15, 10.5, 15))]]


@figure("shampooing-hair", "A head in profile covered in foam bubbles",
        tags=["shampoo", "wash hair", "lather", "shower", "hair care", "bath"])
def _(S):
    return [[shell(circle(7, 5, 2.75)), shell(circle(13, 3.5, 2)), shell(circle(18.5, 4.5, 2.5))],
            [shell(side_head(S)), dot(12.5, 9.5, 1)]]


@figure("tying-ponytail", "The back of a head with a hair tie around a ponytail",
        tags=["ponytail", "hair tie", "hairstyle", "tie hair", "scrunchie", "hair"])
def _(S):
    tail = "M16 7C19.5 8 21 12 20 17C19.5 14 18 11.5 15.5 10.5Z"
    return [[shell(tail), shell(rect(13.5, 5.5, 3.5, 5.5, min(S.R, 1.5)))],
            bust(S, 10, 9, 5.5, 17, 7.5)]


@figure("braiding-hair", "The back of a head with a single braid hanging down",
        tags=["braid", "plait", "hairstyle", "hair", "pigtail", "weave"])
def _(S):
    links = [shell(ellipse(12, y, 2.25, 1.6)) for y in (13.5, 16.5, 19.5)]
    return [links,
            bust(S, 12, 7.5, 5.5, 15.5, 8.5, 21.5)[:1] + [line(_shoulders(S))]]


@figure("putting-in-eye-drops", "A head tipped back with a dropper above the eye and a falling drop",
        tags=["eye drops", "dropper", "dry eyes", "eye care", "medicine", "allergy"])
def _(S):
    drop = "M16 9.5C16.8 10.6 17.2 11.3 17.2 11.9A1.2 1.2 0 0 1 14.8 11.9C14.8 11.3 15.2 10.6 16 9.5Z"
    return [[shell(rect(14.5, 2.5, 3, 3, 0.75)), shell(poly([(14.75, 5.5), (17.25, 5.5), (16.5, 7.5), (15.5, 7.5)], closed=True)),
             solid(drop)],
            [shell(tilted_head(S, -40, -1.5, 3, 0.85)), dot(*xp(xp((12.5, 9), 0, 0, 0, 1), -1.5, 3, -40, 0.85, (10, 12)), 1.1)]]


@figure("inserting-contact-lens", "A fingertip holding a contact lens up to an open eye",
        tags=["contact lens", "contacts", "eye", "vision", "optician", "lens"])
def _(S):
    eye = "M2.5 10C5 5.5 8 4 12 4C16 4 19 5.5 21.5 10C19 14.5 16 16 12 16C8 16 5 14.5 2.5 10Z" if S.name == "line" else \
        "M3 10.5C3 10.5 6.5 4 12 4C17.5 4 21 10.5 21 10.5C21 10.5 17.5 16 12 16C6.5 16 3 10.5 3 10.5Z"
    return [[line(arc(12, 14.5, 3.5, 200, 340)), shell("M9.5 22V16A2.5 2.5 0 0 1 14.5 16V22")],
            [shell(eye), dot(12, 10, 2.5)]]


@figure("getting-dressed", "A person pulling a T-shirt down over the head",
        tags=["get dressed", "dress", "put on shirt", "clothes", "morning", "wear"])
def _(S):
    shirt = poly([(8, 10.5), (4.5, 4.5), (8, 3), (10, 8), (14, 8), (16, 3), (19.5, 4.5), (16, 10.5), (16, 17.5), (8, 17.5)], closed=True, r=S.r * 0.5)
    return [[shell(shirt), dot(12, 5, 2)],
            [limb(S, (9.5, 21.5), (10, 17)), limb(S, (14.5, 21.5), (14, 17))]]


@figure("tying-shoelaces", "A sneaker with its laces being tied in a bow",
        tags=["shoelaces", "tie laces", "shoe", "bow", "sneaker", "knot"])
def _(S):
    shoe = poly([(2.5, 20.5), (2.5, 13.5), (8.5, 13.5), (12, 16), (19, 17), (21.5, 18.5), (21.5, 20.5)], closed=True, r=S.r * 0.6)
    loop_l = xf("M10.5 8.5C7.5 6 4.5 6.5 4.5 8.5C4.5 10.5 7.5 11 10.5 8.5Z", 0, 0, 25, 1, (10.5, 8.5))
    loop_r = xf("M10.5 8.5C13.5 6 16.5 6.5 16.5 8.5C16.5 10.5 13.5 11 10.5 8.5Z", 0, 0, -25, 1, (10.5, 8.5))
    return [[shell(loop_l), shell(loop_r), limb(S, (10.5, 8.5), (8, 12.5)), limb(S, (10.5, 8.5), (13.5, 12.5))],
            [shell(shoe, stroke_miterlimit="2"), detail(seg(2.5, 17.5, 21.5, 17.5))]]


@figure("hanging-up-coat", "A person hanging a coat on a wall hook",
        tags=["hang coat", "coat hook", "hallway", "arrive home", "cloakroom", "jacket"])
def _(S):
    coat = poly([(15.5, 6.5), (12, 8), (11, 21), (20, 21), (19, 8)], closed=True, r=S.r * 0.5)
    return [[head(4.5, 6.5, 2),
             limb(S, (14, 3.5), (7, 10), (4.5, 10), (3.5, 15)),
             line(seg(15.5, 2, 15.5, 6.5))],
            [shell(coat), detail(poly([(13.5, 8), (15.5, 12), (17.5, 8)], r=S.r * 0.3)), detail(seg(15.5, 12, 15.5, 21))]]


@figure("making-bed", "A person leaning over a bed pulling the blanket straight",
        tags=["make bed", "bedding", "tidy", "housework", "chores", "bedroom"])
def _(S):
    return [[head(18.5, 4.5),
             limb(S, (16.5, 8.5), (12, 11.5)),
             limb(S, (16.5, 8.5), (19.5, 13.5), (19.5, 21.5)),
             limb(S, (19.5, 13.5), (22, 21.5))],
            [shell(rect(7.5, 12, 10, 4, min(S.R, 1.5))), shell(rect(3, 11.5, 3, 4.5, min(S.R, 1.25))),
             line(poly([(2, 9), (2, 21.5)], r=0)), line(poly([(2, 18), (17, 18)], r=0)), line(seg(15.5, 18, 15.5, 21.5))]]


@figure("taking-medicine", "A face in profile raising a pill to the lips beside a glass of water",
        tags=["medicine", "pill", "tablet", "medication", "dose", "take pill"])
def _(S):
    pill = xf(rect(15, 12, 5, 2.5, 1.25), 0, 0, -30, 1, (17.5, 13.25))
    return [[shell(pill), shell(pick(S, "M16.5 16H21.5L21 22H17Z", "M17 16H21A0.5 0.5 0 0 1 21.5 16.5L21 21.5A0.5 0.5 0 0 1 20.5 22H17.5A0.5 0.5 0 0 1 17 21.5L16.5 16.5A0.5 0.5 0 0 1 17 16Z"))],
            [shell(small_head(S, True, -1)), dot(*xp((12.5, 9), 0, -1, 0, 0.85, (3, 12)), 1)]]


@figure("drinking-water", "A face in profile tipping a tall glass of water to the lips",
        tags=["drink", "water", "hydrate", "thirsty", "glass", "sip"])
def _(S):
    glass = xf(pick(S, "M15 7H21L20 20H16Z", "M15.5 7H20.5A0.5 0.5 0 0 1 21 7.5L20 19.5A0.5 0.5 0 0 1 19.5 20H16.5A0.5 0.5 0 0 1 16 19.5L15 7.5A0.5 0.5 0 0 1 15.5 7Z"),
               -1, -0.5, 55, 1, (15, 13))
    return [[shell(glass), detail(line_in(xp((15.8, 10.5), -1, -0.5, 55, 1, (15, 13)), xp((20.2, 10.5), -1, -0.5, 55, 1, (15, 13))))],
            [shell(small_head(S, True, 0)), dot(*xp((12.5, 9), 0, 0, 0, 0.85, (3, 12)), 1)]]


@figure("drinking-coffee", "A face in profile sipping from a steaming mug",
        tags=["coffee", "tea", "mug", "hot drink", "break", "morning"])
def _(S):
    return [[shell(rect(14, 12, 6, 7.5, min(S.R, 1.5))), line(pick(S, "M20 13.5H22V17.5H20", "M20 13.5A2 2 0 0 1 20 17.5")),
             line("M15.5 9.5C14.8 8.5 16.2 7.5 15.5 6"), line("M18.5 9.5C17.8 8.5 19.2 7.5 18.5 6")],
            [shell(small_head(S, True, -1)), dot(*xp((12.5, 9), 0, -1, 0, 0.85, (3, 12)), 1)]]


@figure("person-eating", "A person at a table holding a fork and knife over a plate",
        tags=["eat", "meal", "dinner", "lunch", "restaurant", "dining"])
def _(S):
    return [[shell(ellipse(12, 16.5, 5, 1.25)), line(seg(2, 20, 22, 20)),
             line(seg(4, 9, 4, 16)), line(pick(S, "M2.5 9V11.5A1.5 1.5 0 0 0 5.5 11.5V9", "M2.5 9V11A1.5 1.5 0 0 0 5.5 11V9")),
             shell(pick(S, "M20 16V8L21.5 9.5V12L20.5 12.5", "M20 16V9A1 1 0 0 1 21.5 9.5V12L20.5 12.5"))],
            bust(S, 12, 6, 3.5, 12, 5.5, 15)]


@figure("eating-with-chopsticks", "A face in profile lifting a bite from a bowl with chopsticks",
        tags=["chopsticks", "eat", "asian food", "rice", "bowl", "meal"])
def _(S):
    return [[line(seg(21.5, 7, 14, 13)), line(seg(21.5, 10.5, 14.5, 14.5)), dot(15, 12.5, 1.5),
             shell("M13 17H22A4.5 4 0 0 1 13 17Z")],
            [shell(small_head(S, True, -1)), dot(*xp((12.5, 9), 0, -1, 0, 0.85, (3, 12)), 1)]]


@figure("slurping-noodles", "A face slurping noodles up from a bowl",
        tags=["noodles", "ramen", "slurp", "eat", "soup", "pasta"])
def _(S):
    return [[shell(pick(S, "M3 15H21A9 6.5 0 0 1 3 15Z", "M3.5 15H20.5A0.5 0.5 0 0 1 21 15.5A9 6 0 0 1 3 15.5A0.5 0.5 0 0 1 3.5 15Z")),
             line("M10 10.5C9 12 10.5 13 9.5 15"), line("M12 10.5C11 12 12.5 13 11.5 15"), line("M14 10.5C13 12 14.5 13 13.5 15")],
            [shell(circle(12, 7, 5.5)), dot(9.75, 6, 1), dot(14.25, 6, 1)]]


@figure("drinking-through-straw", "A face in profile sipping from a straw in a tall glass",
        tags=["straw", "sip", "drink", "juice", "smoothie", "soda"])
def _(S):
    return [[shell(pick(S, "M15.5 12H21.5L20.5 21.5H16.5Z", "M16 12H21A0.5 0.5 0 0 1 21.5 12.5L20.5 21A0.5 0.5 0 0 1 20 21.5H17A0.5 0.5 0 0 1 16.5 21L15.5 12.5A0.5 0.5 0 0 1 16 12Z")),
             line(poly([(14, 11.5), (17, 9), (19, 16)], r=S.r * 0.3)), detail(seg(16, 15, 21, 15))],
            [shell(small_head(S, False, -2)), dot(*xp((12.5, 9), 0, -2, 0, 0.85, (3, 12)), 1)]]


@figure("blowing-on-food", "A face in profile blowing on a hot spoonful to cool it",
        tags=["blow", "cool down", "hot food", "soup", "spoon", "too hot"])
def _(S):
    return [[shell(ellipse(18.5, 17, 3, 1.75)), line(seg(15.5, 17, 11, 21)),
             line(seg(13.5, 12, 16, 12)), line(seg(14, 9.5, 16.5, 10.5)),
             line("M18 13.5C17 12 19 11 18 9.5"), line("M20.5 13.5C19.5 12 21.5 11 20.5 9.5")],
            [shell(small_head(S, True, -3, 0.8)), dot(*xp((12.5, 9), 0, -3, 0, 0.8, (3, 12)), 1)]]


@figure("family-meal", "A family seated together behind a dinner table",
        tags=["family dinner", "meal", "eat together", "dining", "family", "dinner table"])
def _(S):
    return [[line(seg(2, 16.5, 22, 16.5)), line(seg(4.5, 16.5, 4.5, 21.5)), line(seg(19.5, 16.5, 19.5, 21.5)),
             shell(pick(S, "M9 14.5H15A3 2 0 0 1 9 14.5Z", "M9.5 14.5H14.5A0.5 0.5 0 0 1 15 15A3 1.8 0 0 1 9 15A0.5 0.5 0 0 1 9.5 14.5Z"))],
            bust(S, 5.5, 5.5, 2.5, 10, 3.5, 14.5) + bust(S, 18.5, 5.5, 2.5, 10, 3.5, 14.5) + [head(12, 8, 1.75)]]


@figure("leaving-home", "A person with a bag walking out of an open front door",
        tags=["leave home", "go out", "exit", "departure", "goodbye", "commute"])
def _(S):
    return [[head(15.5, 4.5, 2.25),
             limb(S, (15, 9), (14, 14.5)),
             limb(S, (11.5, 12.5), (15, 9), (18, 12)),
             limb(S, (11, 21.5), (14, 14.5), (17.5, 17), (17.5, 21.5)),
             shell(rect(17.5, 12.5, 4, 3.5, min(S.R, 1)))],
            [line(poly([(2.5, 21.5), (2.5, 2.5), (10, 2.5), (10, 21.5)], r=S.r * 0.4)),
             shell(poly([(2.5, 2.5), (6.5, 5), (6.5, 19.5), (2.5, 21.5)], closed=True, r=S.r * 0.3))]]


@figure("pressing-doorbell", "A finger pressing a doorbell button beside a door frame",
        tags=["doorbell", "ring bell", "press button", "visitor", "ding dong", "arrive"])
def _(S):
    finger = pick(S, "M22 10.5H15.5A1.5 1.5 0 0 0 15.5 13.5H22", "M22 10.5H15.5A1.5 1.5 0 0 0 15.5 13.5H22")
    return [[line(finger), line(seg(21, 13.5, 21, 16.5)),
             shell(rect(7, 5.5, 6, 13, min(S.R, 2))), dot(10, 12, 1.5),
             line(poly([(2.5, 2), (2.5, 22)], r=0)),
             line(arc(10, 12, 7, 290, 320) if False else seg(15.5, 6, 17, 4.5)), line(seg(15.5, 18, 17, 19.5))]]


@figure("turning-key", "A key turned in a lock with a curved arrow",
        tags=["turn key", "unlock", "lock", "key", "open door", "security"])
def _(S):
    key = [shell(circle(8, 8, 4)), dot(8, 8, 1.3) if S.name == "rounded" else sq(6.8, 6.8, 2.4, 2.4),
           line(seg(10.8, 10.8, 20, 20)), line(poly([(16.5, 16.5), (14, 19)], r=0)), line(poly([(19, 19), (17, 21)], r=0))]
    return [key + arrow_arc(S, 8, 8, 6.5, 100, 350, 2.2)]


@figure("opening-door", "A person pulling a door open by its handle",
        tags=["open door", "enter", "door", "doorway", "entrance", "pull"])
def _(S):
    return [[head(18, 5),
             limb(S, (18, 9.5), (18, 15)),
             limb(S, (13, 12.5), (18, 9.5), (20.5, 13.5)),
             limb(S, (15.5, 21.5), (18, 15), (20.5, 21.5))],
            [line(poly([(2.5, 21.5), (2.5, 2.5), (9, 2.5), (9, 21.5)], r=S.r * 0.4)),
             shell(poly([(9, 2.5), (13.5, 5), (13.5, 19), (9, 21.5)], closed=True, r=S.r * 0.3))]]


@figure("holding-door-open", "A person holding a door open for a smaller person walking through",
        tags=["hold door", "courtesy", "polite", "welcome", "after you", "kindness"])
def _(S):
    return [[head(18.5, 4.5),
             limb(S, (18.5, 9), (18.5, 15)),
             limb(S, (14, 9), (18.5, 9), (20.5, 13)),
             limb(S, (16.5, 21.5), (18.5, 15), (20.5, 21.5)),
             head(7, 10.5, 1.75),
             limb(S, (7, 14), (7, 17.5)), limb(S, (4.5, 16.5), (7, 14), (9.5, 16.5)), limb(S, (5, 21.5), (7, 17.5), (9, 21.5))],
            [line(poly([(2.5, 21.5), (2.5, 2.5), (11, 2.5), (11, 21.5)], r=S.r * 0.4)),
             shell(poly([(11, 2.5), (14, 4.5), (14, 19.5), (11, 21.5)], closed=True, r=S.r * 0.3))]]


@figure("flipping-switch", "A finger flipping up the toggle on a wall light switch",
        tags=["light switch", "turn on", "switch on", "lights", "toggle", "power"])
def _(S):
    finger = xf(rect(12, 11, 3.5, 13, pick(S, 1, 1.75)), 0, 0, -40, 1, (13.75, 12.5))
    return [[shell(finger)],
            [shell(rect(2.5, 2.5, 11, 17, min(S.R, 2))), detail(rect(6.5, 6, 3, 7, min(S.R, 1)))]]


@figure("pulling-lever", "A hand gripping a lever and pulling it down",
        tags=["lever", "pull", "switch", "control", "handle", "activate"])
def _(S):
    return [[shell(pick(S, "M4 21.5V17A5 5 0 0 1 14 17V21.5Z", "M4 21.5V17A5 5 0 0 1 14 17V21.5Z")),
             line(seg(9, 17, 17.5, 7.5)), shell(circle(18.5, 6.5, 2.5))] + arrow_arc(S, 9, 17, 12, 285, 330, 2.2)]


@figure("feet-on-footstool", "A person reclining in a chair with feet up on a footstool",
        tags=["feet up", "footstool", "relax", "rest", "lounge", "ottoman"])
def _(S):
    return [[head(5.5, 5),
             limb(S, (6.5, 9.5), (9.5, 14.5), (15.5, 14), (20.5, 13)),
             limb(S, (6.5, 9.5), (11, 11)),
             shell(rect(16, 16, 6, 3, min(S.R, 1))), line(seg(17.5, 19, 17.5, 21.5)), line(seg(20.5, 19, 20.5, 21.5))],
            [line(poly([(2.5, 6), (3.5, 17.5), (12.5, 17.5), (12.5, 21.5)], r=S.r)), line(seg(4, 17.5, 4, 21.5))]]


@figure("vacuuming", "A person pushing an upright vacuum cleaner across the floor",
        tags=["vacuum", "hoover", "vacuum cleaner", "housework", "cleaning", "carpet"])
def _(S):
    return [[head(6.5, 4.5),
             limb(S, (6.5, 9), (6, 14.5)),
             limb(S, (4, 12.5), (6.5, 9), (11, 10)),
             limb(S, (3.5, 21.5), (6, 14.5), (8.5, 21.5)),
             line(seg(11, 8.5, 14.5, 14.5)),
             shell(rect(13, 13, 4.5, 5.5, min(S.R, 1.5))),
             shell(rect(12.5, 19, 9, 2.5, min(S.R, 1.25))),
             dot(19.5, 15.5, 1), dot(21, 12.5, 1)]]


@figure("mopping-floor", "A person mopping a wet floor",
        tags=["mop", "mopping", "wet floor", "cleaning", "housework", "janitor"])
def _(S):
    return [[head(6.5, 4.5),
             limb(S, (6.5, 9), (6, 14.5)),
             limb(S, (4, 12.5), (6.5, 9), (10.5, 11)),
             limb(S, (3.5, 21.5), (6, 14.5), (8.5, 21.5)),
             line(seg(9.5, 7.5, 14.5, 17)),
             limb(S, (11, 21.5), (14.5, 17), (18, 21.5)), line(seg(14.5, 17, 14.5, 21.5)),
             dot(20.5, 14.5, 1), dot(21.5, 18, 1)]]


@figure("sweeping-floor", "A person sweeping dust into a pile with a long broom",
        tags=["sweep", "broom", "dust", "cleaning", "housework", "tidy up"])
def _(S):
    bristles = pick(S, "M12 18H16L17.5 21.5H10.5Z", "M12.5 18H15.5L17.5 21.5H10.5Z")
    return [[head(5.5, 4.5),
             limb(S, (5.5, 9), (5, 14.5)),
             limb(S, (3, 12.5), (5.5, 9), (9.5, 11)),
             limb(S, (2.5, 21.5), (5, 14.5), (7.5, 21.5)),
             line(seg(8.5, 7.5, 14, 18)), shell(bristles),
             solid("M17.5 22A2.5 2.5 0 0 1 22.5 22Z"),
             dot(20.5, 16.5, 0.9)]]


@figure("dusting", "A person dusting a shelf with a feather duster",
        tags=["dusting", "feather duster", "clean", "housework", "shelf", "spring cleaning"])
def _(S):
    duster = path_to_d(U(P(ellipse(15.5, 5.5, 2.25, 3.5)), P(ellipse(17.5, 4.5, 2.25, 3)), P(ellipse(13.5, 4.5, 2.25, 3))))
    return [[head(7, 9.5),
             limb(S, (7, 14), (7, 18)),
             limb(S, (4.5, 17.5), (7, 14), (11, 12.5)),
             limb(S, (4.5, 22), (7, 18), (9.5, 22)),
             line(seg(11, 12.5, 15, 9)),
             line(seg(12, 13.5, 22, 13.5)), dot(19, 17, 1), dot(21.5, 19.5, 1)],
            [shell(xf(duster, 0, 0, 30, 1, (15.5, 6)))]]


@figure("taking-out-trash", "A person carrying a tied rubbish bag to a wheeled bin",
        tags=["take out trash", "rubbish", "garbage", "bin day", "waste", "chores"])
def _(S):
    bag = pick(S, "M6 14L4.5 16.5V21.5H11.5V16.5L10 14Z", "M6.5 14L4.5 17V20.5A1 1 0 0 0 5.5 21.5H10.5A1 1 0 0 0 11.5 20.5V17L9.5 14Z")
    return [[head(9.5, 3.5, 2),
             limb(S, (9.5, 7.5), (9.5, 12)),
             limb(S, (8, 12), (9.5, 7.5), (12, 10)),
             shell(bag), line(seg(8, 14, 8, 11.5)),
             shell(rect(14, 9, 7.5, 10.5, min(S.R, 1))), line(seg(13, 7, 22, 7)), shell(circle(16, 20.5, 1.5))],
            [limb(S, (6.5, 13.5), (9.5, 12), (12.5, 16.5), (12.5, 21.5))]]


@figure("sorting-recycling", "A bottle dropping into one of two bins, one marked for recycling",
        tags=["recycling", "sort waste", "recycle", "bins", "separate", "eco"])
def _(S):
    return [[shell(pick(S, "M5.5 8V5L6.5 3.5V2H8.5V3.5L9.5 5V8Z", "M6 8A0.5 0.5 0 0 1 5.5 7.5V5L6.5 3.5V2H8.5V3.5L9.5 5V7.5A0.5 0.5 0 0 1 9 8Z")),
             shell(rect(2.5, 12, 9, 9.5, min(S.R, 1.5))), line(seg(2, 10.5, 12, 10.5) if False else seg(2, 10.5, 12, 10.5)),
             detail(arc(7, 16.5, 2.5, 200, 110)),
             shell(rect(13.5, 12, 8, 9.5, min(S.R, 1.5))), line(seg(13, 10.5, 22, 10.5))]]


@figure("drying-dishes", "A tea towel wiping a round plate dry",
        tags=["dry dishes", "tea towel", "dish towel", "washing up", "kitchen", "chores"])
def _(S):
    towel = poly([(13, 11), (21, 9), (22, 20.5), (15, 21.5)], closed=True, r=S.r * 0.6)
    return [[shell(towel), detail(seg(14.5, 14, 21.5, 12.5))],
            [shell(circle(10.5, 12.5, 8)), detail(circle(10.5, 12.5, 4))]]
