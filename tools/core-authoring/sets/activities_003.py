"""TypeIcon Core: activities (batch 003): chores, family care, errands, study and work, social moments,
safety signs and first aid.

People are the stick figures of `people.py` (a solid head of radius 2.25 over 2 px limbs, polylines filleted
with S.r). Objects they hold or use are shells, so Filled turns them solid while the limbs get heavier.
Where a limb must pass in front of an object the drawing is split into layers (front first): back layers
are cut away around the front silhouette with a gap, in every style, so the figure stays readable at 16 px.
"""
import math
import re

from dsl import LINE, D, P, ST, U, Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar  # noqa: F401

CAT = "activities"
HR = 2.25  # head radius


# --------------------------------------------------------------------------- helpers

def pick(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


def limb(S, *pts):
    return line(poly(list(pts), r=S.r))


def rpt(p, deg, c=(12.0, 12.0)):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca)


def rpts(pts, deg, c=(12.0, 12.0)):
    return [rpt(p, deg, c) for p in pts]


def rbox(S, cx, cy, w, h, deg, rr=None):
    """Rotated rectangle as a closed polygon (filleted in Rounded)."""
    pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]
    return poly(rpts(pts, deg, (cx, cy)), closed=True, r=S.r * 0.5 if rr is None else rr)


def u(*ds):
    """Union of closed shapes as one outline (d-string)."""
    return path_to_d(U(*[P(d) for d in ds]))


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def tshirt(S, cx, top, w=9.0, h=11.0, sl=3.0):
    """T-shirt outline: body w x h from `top`, short sleeves."""
    x0, x1 = cx - w / 2, cx + w / 2
    return poly([(x0 + 1.5, top), (x0 - sl + 0.5, top + 2.5), (x0 - sl + 2, top + 5.5), (x0, top + 4.5), (x0, top + h),
                 (x1, top + h), (x1, top + 4.5), (x1 + sl - 2, top + 5.5), (x1 + sl - 0.5, top + 2.5), (x1 - 1.5, top)],
                closed=True, r=S.r * 0.5)


def openbook(S, cx, cy, hw=2.5, h=4.0):
    """Open book seen from the front: two pages dipping to the spine."""
    return poly([(cx - hw, cy - h / 2), (cx, cy - h / 2 + 1), (cx + hw, cy - h / 2), (cx + hw, cy + h / 2),
                 (cx, cy + h / 2 + 1), (cx - hw, cy + h / 2)], closed=True, r=S.r * 0.3)


def profile(dx=0.0, dy=0.0, mouth=False, s=1.0):
    """Head and neck in profile facing right, scaled by s then moved by (dx, dy). The open-mouth version
    has a notch at the lips."""
    if mouth:
        d = "M4.5 21.5V17.5C3 16.3 2.5 14.3 2.5 12A6 6 0 0 1 14 9.5L15 12.5H13L14 15.5A1.5 1.5 0 0 1 12.5 16.5H10V21.5Z"
    else:
        d = "M4.5 21.5V17.5C3 16.3 2.5 14.3 2.5 12A6 6 0 0 1 14 9.5L15 12.5H13.5V15A1.5 1.5 0 0 1 12 16.5H10V21.5Z"
    if dx == 0 and dy == 0 and s == 1:
        return d
    X = lambda v: fmt(float(v) * s + dx)  # noqa: E731
    Y = lambda v: fmt(float(v) * s + dy)  # noqa: E731
    toks = re.findall(r"[A-Z]|-?\d+\.?\d*", d)
    out, i, cmd = [], 0, None
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            out.append(t)
            i += 1
        elif cmd in ("M", "L"):
            out.append(f"{X(toks[i])} {Y(toks[i + 1])}")
            i += 2
        elif cmd == "H":
            out.append(X(t))
            i += 1
        elif cmd == "V":
            out.append(Y(t))
            i += 1
        elif cmd == "C":
            out.append(" ".join(f"{X(toks[i + k])} {Y(toks[i + k + 1])}" for k in (0, 2, 4)))
            i += 6
        elif cmd == "A":
            out.append(f"{fmt(float(toks[i]) * s)} {fmt(float(toks[i + 1]) * s)} {toks[i + 2]} {toks[i + 3]} {toks[i + 4]} "
                       f"{X(toks[i + 5])} {Y(toks[i + 6])}")
            i += 7
    return "".join((" " + x) if k and not x[0].isalpha() and not out[k - 1].isalpha() else x for k, x in enumerate(out))


def burst(cx, cy, r1, r2, n=7, start=-90.0):
    return [polar(cx, cy, r1 if k % 2 == 0 else r2, start + k * 180 / n) for k in range(2 * n)]


def bust_d(S, cx, top, hw, bottom=21.5):
    """Open-bottom shoulders (square in Line, round in Rounded)."""
    r = pick(S, 1.5, min(3.0, hw - 0.5))
    return (f"M{fmt(cx - hw)} {fmt(bottom)}V{fmt(top + r)}A{r} {r} 0 0 1 {fmt(cx - hw + r)} {fmt(top)}"
            f"H{fmt(cx + hw - r)}A{r} {r} 0 0 1 {fmt(cx + hw)} {fmt(top + r)}V{fmt(bottom)}")


def bird(x, y, flip=False):
    """Small bird standing on the ground, facing left (right when flipped): body, head, beak and tail."""
    f = -1 if flip else 1
    body = ellipse(x + f * 1.5, y, 3, 2)
    head = circle(x - f * 1.5, y - 2, 1.75)
    beak = poly([(x - f * 3, y - 2.75), (x - f * 4.75, y - 1.75), (x - f * 3, y - 1.25)], closed=True)
    tail = poly([(x + f * 3.5, y - 1.5), (x + f * 6, y - 3.5), (x + f * 5, y + 0.5)], closed=True)
    return u(body, head, beak, tail)


def capsule(x0, y0, x1, y1, w=3.4):
    """Finger or limb region: a capsule along a segment (for building hand outlines)."""
    return ST(seg(x0, y0, x1, y1), w, "round", "round")


def outline(*regions, **attrs):
    return shell(path_to_d(U(*regions)), **attrs)


def flake(cx, cy, r=2.0):
    """Tiny snowflake: three crossing strokes."""
    return [line(seg(*polar(cx, cy, r, a), *polar(cx, cy, r, a + 180))) for a in (90, 30, 150)]


# --------------------------------------------------------------------------- layering (from people.py)

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


def _stroke_layers(S, layers, gap):
    out = list(layers[0])
    cover = _grow(_sil(layers[0], S), gap)
    for parts in layers[1:]:
        if not parts:
            continue
        vis = D(_paint(parts, S), cover)
        if abs(vis.area) > 0.01:
            out.append(solid(path_to_d(vis)))
        cover = U(cover, _grow(_sil(parts, S), gap))
    return out


def _filled_layers(layers, gap):
    result = filled_region(layers[0])
    cover = _grow(result, gap)
    for parts in layers[1:]:
        if not parts:
            continue
        f = filled_region(parts)
        result = U(result, D(f, cover))
        cover = U(cover, _grow(f, gap))
    return result


def figure(name, desc, tags, aliases=(), gap=1.25):
    """Register an icon drawn as layers: fn(S) -> [front layer, layer behind, ...]."""
    def deco(fn):
        icon(name, CAT, desc, tags=tags, aliases=aliases,
             filled=lambda: _filled_layers(fn(LINE), gap))(lambda S: _stroke_layers(S, fn(S), gap))
        return fn
    return deco


# ============================================================================ laundry and chores

@icon("ironing-clothes", CAT, "Person pressing clothes with an iron on an ironing board",
      tags=["ironing", "iron", "ironing board", "laundry", "press", "chores"])
def _(S):
    iron = poly([(10.5, 13), (21, 13), (19.5, 10), (10.5, 10)], closed=True, r=S.r * 0.4)
    return [
        dot(5, 4.5, HR),
        limb(S, (5, 8.5), (5, 15)),
        limb(S, (3, 21), (5, 15), (7, 21)),
        limb(S, (5, 9.5), (8.5, 7.5), (12.5, 7)),
        shell(iron),
        line(pick(S, poly([(12.5, 10), (12.5, 7), (17.5, 7), (17.5, 10)]), "M12.5 10V8.5A1.5 1.5 0 0 1 14 7H16A1.5 1.5 0 0 1 17.5 8.5V10")),
        line(seg(9, 16, 22, 16)),
        line(seg(12, 16, 18.5, 21.5)), line(seg(18.5, 16, 12, 21.5)),
    ]


@icon("folding-clothes", CAT, "T-shirt with a centre fold line and a curved arrow folding one side over",
      tags=["folding", "fold laundry", "clothes", "laundry", "tidy", "chores"])
def _(S):
    return [
        shell(tshirt(S, 12, 10, 9, 11, 3.5)),
        detail(seg(12, 12.5, 12, 21)),
        line(arc(12, 9.5, 6.5, 195, 330)),
        line(poly([(15.3, 4.6), (17.9, 6.2), (18.4, 3.2)], r=S.r * 0.4)),
    ]


@icon("hanging-laundry", CAT, "T-shirt pinned with two pegs to a washing line",
      tags=["washing line", "clothesline", "laundry", "drying", "pegs", "hang out"])
def _(S):
    return [
        line("M2 4.5Q12 6.5 22 4.5"),
        shell(tshirt(S, 12, 7, 9, 13, 3.5)),
        sq(7.25, 3, 1.75, 6, 0.4), sq(15, 3, 1.75, 6, 0.4),
    ]


@figure("carrying-laundry", "Person carrying a full laundry basket on one hip",
        tags=["laundry basket", "carry", "washing", "laundry day", "clothes", "chores"])
def _(S):
    basket = poly([(10.5, 11.5), (21.5, 11.5), (20, 19), (12, 19)], closed=True, r=S.r * 0.5)
    return [
        [limb(S, (7, 9.5), (9.5, 13.5), (13, 14.5))],
        [shell(basket), detail(seg(11.5, 15, 20.5, 15)),
         line("M12.5 9.5A2 2 0 0 1 16 8.2A2.2 2.2 0 0 1 19.8 9.5")],
        [dot(7, 4.5, HR), limb(S, (7, 8.5), (7, 15)), limb(S, (4.5, 21), (7, 15), (9.5, 21))],
    ]


@icon("mowing-lawn", CAT, "Person pushing a lawn mower across the grass",
      tags=["lawn mower", "mowing", "grass", "garden", "yard work", "cut the grass"])
def _(S):
    body = poly([(13, 17.5), (14.5, 14), (21.5, 14), (21.5, 17.5)], closed=True, r=S.r * 0.5)
    return [
        dot(6, 4.5, HR),
        limb(S, (7, 8), (5.5, 14)),
        limb(S, (2.5, 21), (5.5, 14), (7.5, 21)),
        limb(S, (7, 9.5), (10.5, 10.5)),
        line(seg(10.5, 10.5, 15.5, 14)),
        shell(body),
        dot(15, 20.5, 1.5), dot(20, 20.5, 1.5),
    ]


@icon("raking-leaves", CAT, "Person pulling a rake towards a fallen leaf",
      tags=["raking", "rake", "leaves", "autumn", "fall", "yard work"])
def _(S):
    leaf = "M16 20.5C16 16.5 18.5 15 22 15C22 19 19.5 20.5 16 20.5Z"
    return [
        dot(5.5, 4.5, HR),
        limb(S, (5.5, 8.5), (5.5, 15)),
        limb(S, (3.5, 21), (5.5, 15), (7.5, 21)),
        limb(S, (5.5, 9.5), (8.5, 11)),
        line(seg(8, 9.5, 12, 17.5)),
        line(pick(S, poly([(9.5, 20.5), (9.5, 17.5), (14.5, 17.5), (14.5, 20.5)]),
                  poly([(9.5, 20.5), (9.5, 17.5), (14.5, 17.5), (14.5, 20.5)], r=1))),
        line(seg(12, 17.5, 12, 20.5)),
        shell(leaf), detail(seg(17.5, 19, 20.5, 16.5)),
    ]


@icon("shoveling-snow", CAT, "Person lifting a shovel heaped with snow under a falling snowflake",
      tags=["snow shovel", "shoveling", "snow", "winter", "driveway", "clear snow"], aliases=["shovelling-snow"])
def _(S):
    load = u(poly([(13.5, 15.5), (21.5, 15.5), (21.5, 18.5), (14.5, 18.5)], closed=True),
             "M15 15.5C15 12 21 12 21 15.5Z")
    return [
        dot(5.5, 5, HR),
        limb(S, (6, 9), (6.5, 15)),
        limb(S, (3.5, 21), (6.5, 15), (9.5, 21)),
        limb(S, (6, 10), (9.5, 12.5)),
        line(seg(7, 10.5, 13.5, 15.5)),
        shell(load), detail(seg(14.5, 15.5, 21.5, 15.5)),
        *flake(18, 5.5, 3),
    ]


@icon("pulling-weeds", CAT, "Kneeling person pulling a weed with its roots out of the ground",
      tags=["weeding", "weeds", "gardening", "pull weeds", "garden", "yard work"], aliases=["weeding"])
def _(S):
    leaf_l = "M16 11C13 11 11.5 9 11.5 6.5C14.5 6.5 16 8.5 16 11Z"
    leaf_r = "M16 9C16 6 17.5 4 20.5 4C20.5 7 19 9 16 9Z"
    return [
        dot(4.5, 5.5, HR),
        limb(S, (5, 9.5), (5.5, 15)),
        limb(S, (2, 20.5), (5.5, 20.5), (5.5, 15), (9.5, 15), (9.5, 20.5)),
        limb(S, (5.5, 10.5), (9, 13), (14.5, 13)),
        line(seg(16, 8, 16, 16)),
        shell(leaf_l), shell(leaf_r),
        line(poly([(13, 19.5), (16, 16), (19, 19.5)], r=S.r * 0.5)),
        line(seg(16, 16, 16, 21)),
    ]


@figure("washing-car", "Car seen from the side being scrubbed with a soapy sponge",
        tags=["car wash", "washing car", "clean car", "sponge", "valet", "soap"], aliases=["car-wash"])
def _(S):
    body = poly([(2.5, 19), (2.5, 15), (5, 14.5), (7.5, 11), (14.5, 11), (18, 14.5), (21.5, 15.5), (21.5, 19)],
                closed=True, r=S.r * 0.6)
    return [
        [shell(rbox(S, 12.5, 15.5, 5.5, 3.5, -15, min(S.r, 1)))],
        [shell(body), dot(7, 19.5, 2), dot(17, 19.5, 2)],
        [line(circle(15, 4.5, 2)), line(circle(20.5, 7, 1.25)), line(circle(9, 5.5, 1.25))],
    ]


@icon("hammering-nail", CAT, "Hammer swinging down onto a nail in a board with impact lines",
      tags=["hammering", "hammer", "nail", "diy", "carpentry", "repair"])
def _(S):
    c = (15, 6.5)
    head = rbox(S, 15, 6.5, 3.5, 8, -15)
    return [
        shell(head),
        line(seg(*rpt((13.25, 6.5), -15, c), 2.5, 9.5)),
        line(seg(16, 14, 16, 17.5)), line(seg(14, 14, 18, 14)),
        line(seg(10.5, 14.5, 12, 13.5)), line(seg(21.5, 14.5, 20, 13.5)),
        shell(rect(4, 17.5, 18, 3.5, min(S.R, 1))),
    ]


@icon("changing-lightbulb", CAT, "Person on a step stool reaching up to a ceiling light bulb",
      tags=["light bulb", "change bulb", "lamp", "diy", "home repair", "step stool"])
def _(S):
    return [
        line(seg(12, 2, 22, 2)),
        line(seg(17, 2, 17, 4)),
        shell(u(circle(17, 8.5, 2.75), rect(15.75, 4, 2.5, 3))),
        dot(8.5, 7, 2),
        limb(S, (8.5, 10), (8.5, 14)),
        limb(S, (6.5, 17), (8.5, 14), (10.5, 17)),
        limb(S, (8.5, 11), (13.5, 7.5)),
        line(seg(4.5, 18.5, 13, 18.5)),
        line(seg(6, 18.5, 5, 21.5)), line(seg(11.5, 18.5, 12.5, 21.5)),
    ]


@icon("assembling-furniture", CAT, "Kneeling person turning an L-shaped hex key in a flat-pack panel",
      tags=["flat pack", "assembly", "hex key", "allen key", "furniture", "diy"], aliases=["flat-pack"])
def _(S):
    return [
        dot(4.5, 5.5, HR),
        limb(S, (5, 9.5), (5.5, 15)),
        limb(S, (2, 20.5), (5.5, 20.5), (5.5, 15), (9.5, 15), (9.5, 20.5)),
        limb(S, (5.5, 10.5), (11, 10.5)),
        line(poly([(11, 10.5), (17, 10.5), (17, 15.5)], r=S.r)),
        line(arc(17, 8, 3.5, 200, 340)),
        line(poly([(19.2, 4.5), (20.3, 7), (22, 5)], r=S.r * 0.4)),
        shell(rect(12.5, 17, 9.5, 4, min(S.R, 1))),
    ]


@icon("feeding-pet", CAT, "Person bending to pour food from a scoop into a pet bowl",
      tags=["feed pet", "pet food", "dog bowl", "cat food", "kibble", "pet care"])
def _(S):
    bowl = poly([(12.5, 17), (21.5, 17), (20, 21), (14, 21)], closed=True, r=S.r * 0.5)
    scoop = poly([(11, 9), (16, 9), (15, 12), (12, 12)], closed=True, r=S.r * 0.4)
    return [
        dot(5, 4.5, HR),
        limb(S, (6.5, 8), (5.5, 14)),
        limb(S, (3, 21), (5.5, 14), (8, 21)),
        limb(S, (6.5, 9), (11, 9)),
        shell(rbox(S, 14, 10.5, 5, 3, 25)),
        dot(17, 14.5, 1.1), dot(15.5, 14.2, 1.1),
        shell(bowl),
    ]


@icon("playing-fetch", CAT, "Person throwing a ball for a running dog",
      tags=["fetch", "dog", "throw ball", "play with dog", "pet", "park"])
def _(S):
    return [
        dot(5, 7, HR),
        limb(S, (5.5, 11), (5.5, 16)),
        limb(S, (3, 21.5), (5.5, 16), (8, 21.5)),
        limb(S, (5.5, 12), (9, 9), (11, 5)),
        line(circle(16, 4, 1.75)),
        line(poly([(12.5, 13.5), (13.5, 15.5), (19, 15.5)], r=S.r * 0.5)),
        shell(poly([(18.5, 13.5), (19.5, 11.5), (22, 12.5), (21, 15.5), (19, 15.5)], closed=True, r=S.r * 0.3)),
        line(poly([(12, 21), (14, 17.5), (13.5, 15.5)], r=S.r * 0.5)),
        line(poly([(20.5, 21), (19.5, 17.5), (19, 15.5)], r=S.r * 0.5)),
    ]


@icon("changing-diaper", CAT, "Baby lying on its back in a diaper with its arms and legs up",
      tags=["diaper", "nappy", "baby changing", "changing table", "parenting", "infant care"], aliases=["changing-nappy"])
def _(S):
    body = rect(8.5, 9.5, 7, 7.5, min(S.R, 3))
    return [
        shell(circle(12, 5, 2.75)),
        shell(body), detail(pick(S, poly([(8.5, 13), (12, 14.5), (15.5, 13)]), "M8.5 13Q12 15.5 15.5 13")),
        line(poly([(8.5, 11), (5, 10), (3.5, 7)], r=S.r * 0.5)),
        line(poly([(15.5, 11), (19, 10), (20.5, 7)], r=S.r * 0.5)),
        line(poly([(9.5, 17), (6, 19.5), (7, 22)], r=S.r * 0.5)),
        line(poly([(14.5, 17), (18, 19.5), (17, 22)], r=S.r * 0.5)),
    ]


@icon("bathing-baby", CAT, "Baby sitting in a small tub while water is poured from a cup",
      tags=["baby bath", "bath time", "bathing", "infant", "wash baby", "parenting"], aliases=["baby-bath"])
def _(S):
    tub = poly([(2.5, 13.5), (21.5, 13.5), (19.5, 20.5), (4.5, 20.5)], closed=True, r=S.r * 0.6)
    cup = poly([(x + 18.5, y + 4.5) for x, y in rpts([(-2.25, -2.5), (2.25, -2.5), (1.5, 2.5), (-1.5, 2.5)], 130, (0, 0))],
               closed=True, r=S.r * 0.3)
    return [
        dot(9.5, 8.5, 2.75),
        limb(S, (4.5, 11.5), (5.5, 8)),
        shell(tub), detail(seg(2.5, 16, 21.5, 16)),
        shell(cup),
        dot(15, 8.5, 1), dot(14, 11.25, 1),
    ]


@figure("cradling-baby", "Person holding a swaddled baby across the chest in both arms",
        tags=["holding baby", "cradle", "newborn", "parent", "mother", "father"], aliases=["holding-baby"], gap=1.0)
def _(S):
    c = (13, 15)
    wrap = poly(rpts([(9.5, 12.5), (17.5, 12.5), (19.5, 15), (17.5, 17.5), (9.5, 17.5)], -20, c), closed=True, r=S.r)
    hx, hy = rpt((6.5, 15), -20, c)
    return [
        [shell(circle(hx, hy - 0.5, 2.5))],
        [shell(wrap)],
        [dot(12, 4.5, 3), shell("M4 21.5V13.5A3.5 3.5 0 0 1 7.5 10H16.5A3.5 3.5 0 0 1 20 13.5V21.5" if S.name != "line"
                              else "M4 21.5V12A2 2 0 0 1 6 10H18A2 2 0 0 1 20 12V21.5")],
    ]


@figure("tucking-in-child", "Adult leaning over a small bed and pulling the blanket up to a child",
        tags=["bedtime", "tuck in", "goodnight", "sleep", "child", "parenting"], aliases=["bedtime"])
def _(S):
    return [
        [dot(17, 4.5, HR), limb(S, (16.5, 8.5), (19, 14)), limb(S, (16.5, 21.5), (19, 14), (21.5, 21.5)),
         limb(S, (17, 9.5), (13, 12.5))],
        [shell(circle(5.5, 11.5, 2)),
         shell(rect(2.5, 14.5, 14, 3.5, min(S.R, 1.5))),
         line(seg(2.5, 18, 2.5, 21)), line(seg(15.5, 18, 15.5, 21))],
    ]


@figure("pushing-swing", "Adult pushing a child sitting on a swing hung from a bar",
        tags=["swing", "playground", "push swing", "park", "child", "play"])
def _(S):
    return [
        [dot(18, 8, 2), limb(S, (17.5, 11), (16.5, 15)), limb(S, (16.5, 15), (20, 15), (21, 19))],
        [line(seg(9, 2.5, 22, 2.5)), line(seg(17, 2.5, 13.5, 15.5)), line(seg(12.5, 15.5, 18, 15.5))],
        [dot(4.5, 5.5, HR), limb(S, (5, 9.5), (5.5, 15)), limb(S, (3, 21.5), (5.5, 15), (8.5, 21.5)),
         limb(S, (5.5, 10.5), (11, 12))],
    ]


@icon("grocery-shopping", CAT, "Person pushing a shopping cart with groceries sticking out",
      tags=["groceries", "supermarket", "shopping cart", "trolley", "food shop", "errands"])
def _(S):
    return [
        dot(4.5, 4.5, HR),
        limb(S, (5.5, 8.5), (4.5, 14.5)),
        limb(S, (2.5, 21), (4.5, 14.5), (7, 21)),
        limb(S, (5.5, 9.5), (9.5, 10)),
        line(poly([(9, 10), (11, 10), (12.5, 16.5), (20, 16.5), (21.5, 10.5), (11, 10.5)], r=S.r * 0.5)),
        shell(rect(13.5, 5, 3.5, 4, min(S.R, 1))),
        line(seg(18.5, 9, 20.5, 4)),
        dot(13.5, 20, 1.5), dot(19, 20, 1.5),
    ]


@figure("posting-letter", "Envelope going into the slot of a round-topped pillar postbox",
        tags=["post a letter", "postbox", "mail", "send letter", "post", "postal"], aliases=["mailing-letter"])
def _(S):
    box = "M6 21.5V9A6 6 0 0 1 18 9V21.5Z" if S.name == "line" else "M7.5 21.5A1.5 1.5 0 0 1 6 20V9A6 6 0 0 1 18 9V20A1.5 1.5 0 0 1 16.5 21.5Z"
    return [
        [shell(rect(8, 5.5, 8, 5.5, min(S.R, 1))), detail(poly([(8, 5.5), (12, 8.5), (16, 5.5)], r=S.r * 0.3))],
        [shell(box), detail(seg(9, 12, 15, 12)), detail(seg(6, 16, 18, 16))],
    ]


@icon("using-atm", CAT, "Person reaching towards the screen of a wall cash machine",
      tags=["atm", "cash machine", "withdraw cash", "cashpoint", "bank", "money"], aliases=["cash-withdrawal"])
def _(S):
    return [
        dot(5, 5, HR),
        limb(S, (5, 9), (5, 15.5)),
        limb(S, (2.5, 21.5), (5, 15.5), (7.5, 21.5)),
        limb(S, (5, 10), (9, 12.5), (11.5, 11.5)),
        shell(rect(13, 3, 8.5, 12.5, min(S.R, 2))),
        detail(rect(15, 5.5, 4.5, 4, 0.5)),
        detail(seg(15, 12.5, 19.5, 12.5)),
        line(seg(13, 19, 21.5, 19)),
    ]


@figure("receiving-parcel", "Person in a doorway taking a box from a delivery hand",
        tags=["parcel delivery", "package", "delivery", "doorstep", "courier", "receive"], aliases=["package-delivery"])
def _(S):
    return [
        [dot(7, 6.5, 2), limb(S, (7, 9.5), (7, 15)), limb(S, (5, 21), (7, 15), (9, 21)),
         limb(S, (7, 10.5), (13, 12.5)),
         shell(rect(13.5, 9.5, 6, 6, min(S.R, 1))), detail(seg(16.5, 9.5, 16.5, 12.5)),
         line(seg(20, 13, 22.5, 13))],
        [line(poly([(2.5, 21.5), (2.5, 2.5), (11.5, 2.5), (11.5, 21.5)], r=S.r))],
    ]


@icon("waiting-for-bus", CAT, "Person standing beside a bus stop pole with a sign on top",
      tags=["bus stop", "waiting", "public transport", "commute", "transit", "bus"], aliases=["bus-waiting"])
def _(S):
    return [
        dot(7, 5, HR),
        limb(S, (7, 9), (7, 15.5)),
        limb(S, (4.5, 21.5), (7, 15.5), (9.5, 21.5)),
        limb(S, (4.5, 14), (7, 10), (9.5, 14)),
        shell(rect(13.5, 2.5, 8, 7, min(S.R, 2))),
        detail(seg(15.5, 6, 19.5, 6)),
        line(seg(17.5, 9.5, 17.5, 21.5)),
        line(seg(15, 21.5, 20, 21.5)),
    ]


@icon("hailing-taxi", CAT, "Person at the kerb raising an arm to stop a taxi",
      tags=["hail a cab", "taxi", "cab", "ride", "stop taxi", "street"], aliases=["hail-cab"])
def _(S):
    car = poly([(10, 20), (10, 16.5), (12.5, 16), (14.5, 12.5), (19.5, 12.5), (21.5, 16), (21.5, 20)], closed=True, r=S.r * 0.5)
    return [
        dot(5, 6.5, HR),
        limb(S, (5, 10.5), (5, 16)),
        limb(S, (3, 21.5), (5, 16), (7.5, 21.5)),
        limb(S, (5, 11), (7.5, 7), (9.5, 2.5)),
        shell(car),
        shell(rect(16, 9.5, 3, 1.5, 0.3)),
        dot(13.5, 20.5, 1.25), dot(18.5, 20.5, 1.25),
    ]


@figure("standing-on-train", "Standing passenger holding an overhead strap beside a train window",
        tags=["commuter", "train", "subway", "metro", "standing", "public transport"], aliases=["commuter"])
def _(S):
    return [
        [dot(12.5, 8.5, HR), limb(S, (12.5, 12), (12.5, 17)), limb(S, (10, 21.5), (12.5, 17), (15, 21.5)),
         limb(S, (12.5, 12.5), (9.5, 9), (8, 7.5)), limb(S, (12.5, 12.5), (14.5, 16))],
        [line(seg(2, 2.5, 22, 2.5)), line(seg(7.5, 2.5, 7.5, 4.5)), line(circle(7.5, 6.5, 1.75)),
         shell(rect(16.5, 6, 5.5, 7.5, min(S.R, 1.5)))],
    ]


@figure("person-driving", "Front view of a person behind a steering wheel with both hands on it",
        tags=["driving", "driver", "steering wheel", "car", "drive", "motorist"], aliases=["driver"])
def _(S):
    return [
        [line(circle(12, 15.5, 5.75)), dot(12, 15.5, 1.5), line(seg(6.25, 15.5, 10.5, 15.5)), line(seg(13.5, 15.5, 17.75, 15.5))],
        [dot(12, 4.5, 2.5), limb(S, (6.5, 13), (7, 9.5), (17, 9.5), (17.5, 13)), line(seg(12, 9.5, 12, 12))],
    ]


@icon("pumping-fuel", CAT, "Fuel pump with its hose running to the filler of a car",
      tags=["refuel", "petrol", "gas station", "fuel pump", "fill up", "gasoline"], aliases=["refueling"])
def _(S):
    car = poly([(9.5, 21), (9.5, 16.5), (12, 16), (14, 12), (19.5, 12), (21.5, 16), (21.5, 21)], closed=True, r=S.r)
    return [
        shell(rect(2.5, 4, 6.5, 17.5, min(S.R, 3))),
        detail(rect(4.5, 6.5, 2.5, 3, 0.4)),
        line(pick(S, "M9 8.5H12.5V13", "M9 8.5H10.5A2 2 0 0 1 12.5 10.5V13")),
        shell(car),
    ]


@icon("walking-to-school", CAT, "Child walking with a large backpack",
      tags=["school", "pupil", "backpack", "school run", "student", "walk"], aliases=["school-run"])
def _(S):
    return [
        dot(14, 5, 2.5),
        shell(rbox(S, 8, 11.5, 4.5, 6.5, -10, min(S.r, 1.5))),
        limb(S, (13, 9), (12, 15)),
        limb(S, (9, 21), (12, 15), (14.5, 17.5), (15, 21)),
        limb(S, (13, 10.5), (16, 13), (18, 13)),
    ]


@icon("packing-suitcase", CAT, "Open suitcase with a T-shirt laid in one half",
      tags=["packing", "suitcase", "travel", "luggage", "holiday", "trip"], aliases=["packing-luggage"])
def _(S):
    return [
        shell(rect(2, 7, 20, 14, min(S.R, 2))),
        line(pick(S, poly([(9.5, 7), (9.5, 4), (14.5, 4), (14.5, 7)]), poly([(9.5, 7), (9.5, 4), (14.5, 4), (14.5, 7)], r=1))),
        detail(seg(12, 7, 12, 21)),
        detail(seg(2, 14, 12, 14)),
        detail(poly([(15, 10), (13.8, 12.2), (14.8, 13), (15, 18), (19, 18), (19.2, 13), (20.2, 12.2), (19, 10)], closed=True)),
    ]


@icon("writing-at-desk", CAT, "Person sitting at a desk and writing on a sheet of paper with a pen",
      tags=["writing", "desk", "pen", "paperwork", "letter", "study"], aliases=["desk-writing"])
def _(S):
    return [
        dot(6.5, 4.5, HR),
        limb(S, (7, 8.5), (5.5, 14.5), (10.5, 14.5), (10.5, 21)),
        limb(S, (7, 9.5), (10, 12), (13, 11)),
        line(seg(13, 11, 15.5, 6.5)),
        line(seg(12, 13.5, 22, 13.5) if S.name == "line" else seg(12.5, 13.5, 21.5, 13.5)),
        line(seg(20, 13.5, 20, 21.5)),
        solid(rect(15, 11.25, 6, 1.25)),
    ]


@icon("studying", CAT, "Person sitting at a desk reading an open book beside a stack of books",
      tags=["study", "revision", "books", "learning", "student", "homework"], aliases=["revising"])
def _(S):
    return [
        dot(6, 4.5, HR),
        limb(S, (6.5, 8.5), (5.5, 14.5), (10, 14.5), (10, 21)),
        limb(S, (6.5, 9.5), (9.5, 11.5)),
        shell(openbook(S, 13, 10.5)),
        shell(rect(17.5, 6.5, 4.5, 6.5, min(S.R, 1))), detail(seg(17.5, 9.75, 22, 9.75)),
        line(seg(9, 15, 22, 15) if S.name == "line" else seg(9.5, 15, 21.5, 15)),
        line(seg(19.5, 15, 19.5, 21.5)),
    ]


@icon("taking-exam", CAT, "Person at a single desk writing a test under a wall clock",
      tags=["exam", "test", "examination", "assessment", "exam hall", "school"], aliases=["sitting-exam"])
def _(S):
    return [
        dot(5.5, 6.5, HR),
        limb(S, (6, 10.5), (4.5, 16), (9, 16), (9, 21.5)),
        limb(S, (6, 11.5), (9, 13.5), (12, 13)),
        line(seg(12, 13, 13.5, 10)),
        solid(rect(13.5, 13.25, 5.5, 1.25)),
        line(seg(10.5, 15.5, 21.5, 15.5)),
        line(seg(19.5, 15.5, 19.5, 21.5)),
        shell(circle(18.5, 5.5, 3.25)),
        detail(poly([(18.5, 4), (18.5, 5.75), (19.75, 6.5)], r=S.r * 0.3)),
    ]


@icon("reading-newspaper", CAT, "Person peeking over the top of an open newspaper",
      tags=["newspaper", "news", "reading", "paper", "headlines", "press"], aliases=["reading-the-news"])
def _(S):
    return [
        dot(12, 4.5, 2.5),
        shell(rect(2.5, 9, 19, 12, min(S.R, 1.5))), detail(seg(12, 9, 12, 21)),
        detail(seg(5, 12, 9.5, 12)), detail(seg(5, 15, 9.5, 15)), detail(seg(5, 18, 9.5, 18)),
        detail(rect(14.5, 12, 4.5, 3.5, 0.4)), detail(seg(14.5, 18, 19, 18)),
    ]


@figure("reading-in-bed", "Person sitting up in bed against a pillow reading a book",
        tags=["bedtime reading", "bed", "book", "reading", "night", "relax"], aliases=["bedtime-reading"])
def _(S):
    blanket = poly([(6, 14), (12.5, 14), (16, 11.5), (19.5, 14), (21.5, 14), (21.5, 18), (6, 18)], closed=True, r=S.r * 0.5)
    return [
        [shell(openbook(S, 13, 9.5, 2.25))],
        [dot(7.5, 5.5, HR), limb(S, (7.5, 9), (7.5, 13)), limb(S, (7.5, 10), (10.5, 11.5))],
        [shell(blanket)],
        [line(seg(2.5, 7, 2.5, 21.5)), line(seg(2.5, 18, 21.5, 18)), line(seg(21.5, 18, 21.5, 21.5))],
    ]


@icon("job-interview", CAT, "Two people sitting across a small table, one reading a CV",
      tags=["interview", "job", "hiring", "recruitment", "candidate", "hr"], aliases=["interview"])
def _(S):
    return [
        dot(4, 5, 2),
        limb(S, (4, 8), (4, 14.5), (7.5, 14.5), (7.5, 21)),
        dot(20, 5, 2),
        limb(S, (20, 8), (20, 14.5), (16.5, 14.5), (16.5, 21)),
        limb(S, (20, 9.5), (17.5, 11.5)),
        shell(rect(11.5, 6.5, 4, 5, 0.5)),
        line(seg(10, 14, 14.5, 14) if S.name == "line" else seg(10.5, 14, 14, 14)),
        line(seg(12.25, 14, 12.25, 21.5)),
    ]


@icon("team-meeting", CAT, "Top view of a meeting table with five people around it",
      tags=["team meeting", "meeting", "huddle", "staff meeting", "round table", "colleagues"])
def _(S):
    return [
        shell(rect(5, 8.5, 12, 7, min(S.R, 3.5))),
        dot(8, 4.5, 2.25), dot(14, 4.5, 2.25), dot(8, 19.5, 2.25), dot(14, 19.5, 2.25), dot(20.5, 12, 2.25),
    ]


@figure("brainstorming", "Three people side by side under one glowing light bulb",
        tags=["brainstorm", "ideas", "creative thinking", "workshop", "idea", "team"], aliases=["ideation"])
def _(S):
    def bust(cx, hy, hw=3.5, top=None, bottom=21.5):
        top = hy + 4 if top is None else top
        r = pick(S, 1.5, 2.5)
        return [dot(cx, hy, 2),
                line(f"M{fmt(cx - hw)} {fmt(bottom)}V{fmt(top + r)}A{r} {r} 0 0 1 {fmt(cx - hw + r)} {fmt(top)}"
                     f"H{fmt(cx + hw - r)}A{r} {r} 0 0 1 {fmt(cx + hw)} {fmt(top + r)}V{fmt(bottom)}")]
    return [
        [shell(circle(12, 5.5, 3.25)), line(seg(10.75, 10.5, 13.25, 10.5)),
         line(seg(5.5, 3.5, 7, 4.5)), line(seg(18.5, 3.5, 17, 4.5))],
        bust(12, 14, 3.5),
        bust(5, 12.5, 3) + bust(19, 12.5, 3),
    ]


@figure("multitasking", "Person with four arms holding a phone, a pen, a mug and a sheet of paper",
        tags=["multitask", "busy", "juggling tasks", "productivity", "overload", "work"], aliases=["juggling-tasks"])
def _(S):
    return [
        [shell(rect(2, 2.5, 3.5, 5.5, 0.6)),
         line(seg(19, 2.5, 21.5, 7)),
         shell(poly([(2, 13.5), (5.5, 13.5), (5.5, 18), (2, 18)], closed=True, r=S.r * 0.3)),
         shell(rect(18.5, 14, 3.5, 4, min(S.R, 1))), line(seg(22, 15.5, 22.5, 15.5))],
        [dot(12, 4.5, HR), limb(S, (12, 8.5), (12, 15)), limb(S, (9, 21.5), (12, 15), (15, 21.5)),
         limb(S, (12, 9.5), (7.5, 8.5), (5.5, 6)), limb(S, (12, 9.5), (16.5, 8.5), (19, 5.5)),
         limb(S, (12, 11), (8, 13), (6, 15)), limb(S, (12, 11), (16, 13), (18, 15))],
    ]


@icon("working-late", CAT, "Person at a laptop on a desk with a crescent moon above",
      tags=["overtime", "late night", "night shift", "work late", "deadline", "burning the midnight oil"], aliases=["overtime"])
def _(S):
    return [
        dot(5.5, 7, HR),
        limb(S, (6, 11), (5, 16), (9.5, 16), (9.5, 21.5)),
        limb(S, (6, 12), (9, 14), (12, 13.5)),
        line(pick(S, poly([(12.5, 14.5), (17, 14.5), (18.5, 9.5)]), poly([(12.5, 14.5), (17, 14.5), (18.5, 9.5)], r=0.8))),
        line(seg(10.5, 16, 22, 16) if S.name == "line" else seg(11, 16, 21.5, 16)),
        line(seg(19.5, 16, 19.5, 21.5)),
        shell("M14.5 2.5A3 3 0 1 0 18.5 6.5A2.5 2.5 0 0 1 14.5 2.5Z"),
    ]


@icon("active-listening", CAT, "Two people facing each other: one speaks in a speech bubble, the other listens",
      tags=["listening", "listen", "conversation", "empathy", "attention", "communication"], aliases=["listening"])
def _(S):
    def bust(cx, hy, hw=4):
        r = pick(S, 1.5, 3)
        top = hy + 4.5
        return [dot(cx, hy, 2.5),
                line(f"M{fmt(cx - hw)} 21.5V{fmt(top + r)}A{r} {r} 0 0 1 {fmt(cx - hw + r)} {fmt(top)}"
                     f"H{fmt(cx + hw - r)}A{r} {r} 0 0 1 {fmt(cx + hw)} {fmt(top + r)}V21.5")]
    bubble = poly([(2.5, 2.5), (11, 2.5), (11, 8), (6.5, 8), (4.5, 10), (4.5, 8), (2.5, 8)], closed=True, r=S.r * 0.4)
    return [
        shell(bubble),
        *bust(6.5, 13.5), *bust(17.5, 13.5),
        line(arc(17.5, 13.5, 5, 200, 250)), line(arc(17.5, 13.5, 8, 205, 245)),
    ]


@icon("storytelling", CAT, "Seated adult reading an open book aloud to two small children",
      tags=["story time", "storytelling", "reading aloud", "bedtime story", "children", "library"], aliases=["story-time"])
def _(S):
    return [
        dot(17.5, 4.5, HR),
        limb(S, (17.5, 8.5), (18.5, 14.5), (14, 14.5), (14, 21)),
        limb(S, (17.5, 9.5), (15, 11.5)),
        shell(openbook(S, 11.5, 9.5)),
        dot(4, 14, 1.75), line(pick(S, "M1.5 21.5V19A1.5 1.5 0 0 1 3 17.5H5A1.5 1.5 0 0 1 6.5 19V21.5",
                                  "M1.5 21.5V20A2.5 2.5 0 0 1 6.5 20V21.5")),
        dot(9.5, 14, 1.75), line(pick(S, "M7 21.5V19A1.5 1.5 0 0 1 8.5 17.5H10.5A1.5 1.5 0 0 1 12 19V21.5",
                                    "M7 21.5V20A2.5 2.5 0 0 1 12 20V21.5")),
    ]


@icon("whispering", CAT, "Person cupping a hand beside the mouth and whispering to another",
      tags=["whisper", "secret", "gossip", "quiet", "confide", "tell a secret"], aliases=["secret"])
def _(S):
    def bust(cx, hy, hw=4):
        r = pick(S, 1.5, 3)
        top = hy + 4.5
        return [dot(cx, hy, 2.5),
                line(f"M{fmt(cx - hw)} 21.5V{fmt(top + r)}A{r} {r} 0 0 1 {fmt(cx - hw + r)} {fmt(top)}"
                     f"H{fmt(cx + hw - r)}A{r} {r} 0 0 1 {fmt(cx + hw)} {fmt(top + r)}V21.5")]
    return [
        *bust(6, 11), *bust(18.5, 11),
        limb(S, (9, 15.5), (11, 12), (10.5, 8.5)),
        dot(13.5, 7.5, 0.9), dot(15.5, 6.5, 0.9),
        line(arc(6, 11, 5, 280, 330)),
    ]


@icon("shouting-through-hands", CAT, "Head in profile with hands cupped around the mouth and loud sound lines",
      tags=["shout", "yell", "call out", "loud", "holler", "cupped hands"], aliases=["yelling"])
def _(S):
    head = ("M4.5 21.5V17.5C3 16.3 2.5 14.3 2.5 12A6 6 0 0 1 14 9.5L15 12.5H13.5V15A1.5 1.5 0 0 1 12 16.5H10V21.5Z")
    return [
        shell(head),
        shell(poly([(14.5, 12), (18, 9.5), (18, 17), (14.5, 14.5)], closed=True, r=S.r * 0.4)),
        line(seg(20, 8.5, 21.5, 7)), line(seg(20.5, 13.25, 22, 13.25)), line(seg(20, 18, 21.5, 19.5)),
    ]


@figure("arguing-people", "Two people facing each other with clashing speech bubbles full of exclamation marks",
        tags=["argument", "quarrel", "dispute", "conflict", "disagreement", "row"], aliases=["quarrel"])
def _(S):
    rb = poly([(12.5, 2), (21.5, 2), (21.5, 9.5), (20, 9.5), (20, 12), (17, 9.5), (12.5, 9.5)], closed=True, r=S.r * 0.4)
    lb = poly([(2.5, 3), (11.5, 3), (11.5, 10.5), (7, 10.5), (4, 13), (4, 10.5), (2.5, 10.5)], closed=True, r=S.r * 0.4)
    return [
        [shell(rb), detail(seg(17, 4, 17, 6)), Part("dot", circle(17, 7.75, 0.75))],
        [shell(lb), detail(seg(7, 5, 7, 7)), Part("dot", circle(7, 8.75, 0.75))],
        [dot(8, 17, 2), line(bust_d(S, 8, 20.25, 3, 22)), dot(16, 17, 2), line(bust_d(S, 16, 20.25, 3, 22))],
    ]


@icon("texting-while-walking", CAT, "Person walking with eyes on a phone towards a warning sign",
      tags=["texting", "distracted walking", "phone", "pedestrian safety", "smartphone", "look up"], aliases=["distracted-walking"])
def _(S):
    return [
        dot(9.5, 5, HR),
        limb(S, (8, 8.5), (7, 14)),
        limb(S, (3, 21), (7, 14), (9.5, 17), (9.5, 21)),
        limb(S, (8, 9.5), (9, 13), (11.5, 13)),
        shell(rbox(S, 13, 11.5, 2.5, 4.5, 30, 0.5)),
        shell(poly([(18, 12), (22, 20.5), (14, 20.5)], closed=True, r=S.r * 0.5)),
        detail(seg(18, 15, 18, 17)), dot(18, 18.9, 0.8),
    ]


@figure("taking-selfie", "Person holding a phone out at arm's length to photograph their own face",
        tags=["selfie", "self portrait", "phone camera", "front camera", "photo", "smile"], aliases=["selfie"])
def _(S):
    return [
        [shell(rbox(S, 18.5, 6, 4.5, 7.5, 15, min(S.r, 1)))],
        [dot(8, 9, 3), line(bust_d(S, 8, 15.5, 5.5)), limb(S, (12, 16.5), (15.5, 12), (17.5, 10))],
    ]


@icon("person-singing", CAT, "Head in profile with the mouth open and music notes flowing out",
      tags=["singing", "singer", "vocals", "karaoke", "song", "choir"], aliases=["singer-profile"])
def _(S):
    return [
        shell(profile(0, 0, True)),
        dot(16.5, 17.5, 1.75), dot(20.25, 15.5, 1.75),
        line(seg(17.75, 17.5, 17.75, 8.5)), line(seg(21.5, 15.5, 21.5, 6.5)),
        line(seg(17.75, 9, 21.5, 7) if S.name == "line" else seg(17.75, 8.5, 21.5, 6.5)),
    ]


@figure("watching-tv", "Person on a sofa seen from behind, facing a television",
        tags=["watching tv", "television", "couch", "relax", "binge watch", "movie night"], aliases=["couch-potato"])
def _(S):
    sofa = pick(S, "M2 21.5V15.5H5V17.5H19V15.5H22V21.5Z",
                "M3 21.5A1 1 0 0 1 2 20.5V17A1.5 1.5 0 0 1 5 17V17.5H19V17A1.5 1.5 0 0 1 22 17V20.5A1 1 0 0 1 21 21.5Z")
    return [
        [dot(12, 14.5, 2.5)],
        [shell(sofa)],
        [shell(rect(4, 2.5, 16, 8.5, min(S.R, 2)))],
    ]


@figure("using-vr-headset", "Head in profile wearing a boxy virtual reality headset with a strap",
        tags=["vr", "virtual reality", "headset", "metaverse", "gaming", "immersive"], aliases=["virtual-reality"])
def _(S):
    return [
        [shell(rect(10.5, 6.5, 8, 6.5, min(S.R, 2.5)))],
        [shell(profile(0, 0)), detail(seg(2.5, 10.5, 9.5, 10.5))],
    ]


@icon("person-dancing", CAT, "Person dancing with one arm raised, a hand on the hip and a leg kicked out",
      tags=["dance", "dancing", "party", "disco", "celebrate", "fun"], aliases=["dancer"])
def _(S):
    return [
        dot(10.5, 4.5, HR),
        limb(S, (10.5, 8.5), (11.5, 14.5)),
        limb(S, (10.5, 9.5), (14, 7.5), (16.5, 3)),
        limb(S, (10.5, 9.5), (7, 11.5), (9.5, 14)),
        limb(S, (11.5, 14.5), (9.5, 21.5)),
        limb(S, (11.5, 14.5), (16, 16.5), (19.5, 14.5)),
    ]


@icon("smelling-flower", CAT, "Face in profile with the nose close to a flower on its stem",
      tags=["smell", "flower", "scent", "fragrance", "spring", "nature"], aliases=["sniffing-flower"])
def _(S):
    petals = u(*[circle(*polar(18.5, 8.5, 2, a), 1.6) for a in range(0, 360, 72)])
    return [
        shell(profile(-0.5, 0)),
        shell(petals), dot(18.5, 8.5, 1),
        line("M18.5 12.5V21.5"),
        shell("M18.5 18C18.5 15.8 20 14.5 22 14.5C22 16.7 20.5 18 18.5 18Z"),
    ]


@icon("feeding-birds", CAT, "Person scattering seeds from an open hand to a bird on the ground",
      tags=["feed birds", "bird seed", "pigeons", "park", "wildlife", "nature"], aliases=["bird-feeding"])
def _(S):
    body = u(ellipse(18, 17.5, 3.5, 2.5), circle(15, 14.5, 1.9),
             poly([(13.5, 13.8), (11.8, 14.8), (13.5, 15.4)], closed=True),
             poly([(20.5, 16), (22.5, 14), (21.5, 18)], closed=True))
    return [
        dot(4.5, 4.5, HR),
        limb(S, (5, 8.5), (5, 14.5)),
        limb(S, (3, 21.5), (5, 14.5), (7.5, 21.5)),
        limb(S, (5, 9.5), (8.5, 11), (11, 9.5)),
        dot(13.5, 9.5, 0.9), dot(11.5, 13.5, 0.9), dot(14.5, 11.5, 0.9),
        shell(body, stroke_miterlimit="2"),
        line(seg(17.5, 20, 17.5, 22)),
    ]


@icon("picking-fruit", CAT, "Person reaching up to pick an apple from a leafy branch",
      tags=["fruit picking", "harvest", "orchard", "apple", "pick", "farm"], aliases=["apple-picking"])
def _(S):
    apple = "M16 8.5C14 7.3 11.5 8.5 11.5 11.3C11.5 14 13.6 16 16 15.4C18.4 16 20.5 14 20.5 11.3C20.5 8.5 18 7.3 16 8.5Z"
    return [
        line(pick(S, "M2 3H22", "M2 3.5Q12 2 22 3.5")),
        line(seg(16, 3, 16, 7)),
        shell("M18 3.5C18 6 19.8 7.5 22 7.5C22 5 20.3 3.5 18 3.5Z"),
        shell(apple),
        dot(5, 8, HR),
        limb(S, (5, 11.5), (5, 16.5)),
        limb(S, (3, 21.5), (5, 16.5), (7, 21.5)),
        limb(S, (5, 12.5), (8, 9.5), (10.5, 9.5)),
    ]


@icon("skipping-stones", CAT, "Person throwing a flat stone that skips across the water in small hops",
      tags=["skipping stones", "stone skimming", "lake", "shore", "throw", "water"], aliases=["skimming-stones"])
def _(S):
    return [
        dot(4.5, 5, HR),
        limb(S, (5, 9), (5.5, 15)),
        limb(S, (3, 21.5), (5.5, 15), (8.5, 21.5)),
        limb(S, (5, 10), (8.5, 12), (11, 11)),
        solid(ellipse(14.5, 10, 2, 1)),
        line(arc(15.5, 18, 2.5, 200, 340)), line(arc(20, 18, 1.75, 200, 340)),
        line(seg(11, 20.5, 22, 20.5) if S.name == "line" else seg(11.5, 20.5, 21.5, 20.5)),
    ]


@figure("chopping-firewood", "Axe driven into the top of a log standing on a chopping block",
        tags=["chopping wood", "firewood", "axe", "log", "splitting logs", "lumberjack"], aliases=["splitting-logs"])
def _(S):
    c, a = (9, 8.5), math.radians(35)
    U_, V_ = (math.sin(a), math.cos(a)), (math.cos(a), -math.sin(a))

    def at(p, q):
        return (c[0] + p * U_[0] + q * V_[0], c[1] + p * U_[1] + q * V_[1])
    head = poly([at(p, q) for p, q in [(-1.5, -1.5), (2, -1.5), (5.5, -3), (5.5, 2.25), (2, 1.5), (-1.5, 1.5)]],
                closed=True, r=S.r * 0.3)
    return [
        [shell(head)],
        [line(seg(*at(0, 1.5), *at(0, 10.5)))],
        [shell(rect(5.5, 11, 11, 6.5, min(S.R, 1.5)))],
        [shell(rect(2.5, 18.5, 19, 3, min(S.R, 1)))],
    ]


@icon("drawing-water-from-well", CAT, "Roofed well with a crank handle and a bucket raised on its rope",
      tags=["water well", "well", "bucket", "draw water", "village", "rural"], aliases=["water-well"])
def _(S):
    return [
        shell(poly([(4, 7.5), (12, 2.5), (20, 7.5)], closed=True, r=S.r * 0.5)),
        line(seg(6.5, 7.5, 6.5, 15.5)), line(seg(17.5, 7.5, 17.5, 15.5)),
        line(seg(6.5, 10, 20.5, 10)), line(poly([(20.5, 10), (20.5, 13), (22, 13)], r=S.r * 0.5)),
        line(seg(12, 10, 12, 11.5)),
        shell(poly([(10, 11.5), (14, 11.5), (13.5, 14.5), (10.5, 14.5)], closed=True, r=S.r * 0.3)),
        shell(rect(4, 16, 16, 5.5, min(S.R, 1.5))), detail(seg(12, 16, 12, 21.5)),
    ]


@figure("pounding-grain", "Person raising a tall pestle over a large standing mortar",
        tags=["mortar and pestle", "pounding", "grain", "millet", "grinding", "traditional"], aliases=["pestle-and-mortar"])
def _(S):
    mortar = poly([(11.5, 13), (21.5, 13), (18.5, 17), (19.5, 21.5), (13.5, 21.5), (14.5, 17)], closed=True, r=S.r * 0.5)
    return [
        [line(seg(16.5, 2.5, 16.5, 10.5))],
        [dot(5.5, 5, HR), limb(S, (6, 9), (6.5, 15)), limb(S, (4, 21.5), (6.5, 15), (9, 21.5)),
         limb(S, (6, 10), (10, 8), (14.5, 6.5))],
        [shell(mortar)],
    ]


@icon("unboxing", CAT, "Open cardboard box with its flaps folded out and sparkles rising",
      tags=["unboxing", "open box", "new purchase", "delivery", "package", "surprise"], aliases=["open-parcel"])
def _(S):
    return [
        shell(rect(6, 12.5, 12, 9, min(S.R, 1.5))),
        shell(poly([(6, 12.5), (3, 9.5), (7.5, 9.5), (10, 12.5)], closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        shell(poly([(18, 12.5), (21, 9.5), (16.5, 9.5), (14, 12.5)], closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        line(seg(12, 2, 12, 7.5)), line(seg(7.5, 3.5, 9, 6)), line(seg(16.5, 3.5, 15, 6)),
    ]


@figure("unwrapping-gift", "Gift box with its lid lifted and the ribbon pulled loose",
        tags=["unwrap", "open present", "gift", "present", "birthday", "surprise"], aliases=["opening-present"])
def _(S):
    lid = rbox(S, 11.5, 7.5, 18, 3.5, -12, min(S.r, 1))
    return [
        [shell(lid), detail(seg(*rpt((11.5, 5.75), -12, (11.5, 7.5)), *rpt((11.5, 9.25), -12, (11.5, 7.5))))],
        [shell(rect(4.5, 12.5, 15, 9, min(S.R, 2))), detail(seg(12, 12.5, 12, 21.5))],
    ]


@icon("giving-gift", CAT, "Person holding out a wrapped gift box with a bow",
      tags=["give a gift", "present", "gift giving", "birthday", "thank you", "generosity"], aliases=["giving-present"])
def _(S):
    return [
        dot(5, 5, HR),
        limb(S, (5, 9), (5.5, 15)),
        limb(S, (3, 21.5), (5.5, 15), (8, 21.5)),
        limb(S, (5, 10), (8.5, 13.5), (12, 13.5)),
        shell(rect(12.5, 10, 9, 7.5, min(S.R, 1.5))), detail(seg(17, 10, 17, 17.5)),
        line(pick(S, poly([(17, 9), (14.5, 6.5), (14.5, 9)]), "M17 9C15.5 6 13.5 6.5 14.5 9")),
        line(pick(S, poly([(17, 9), (19.5, 6.5), (19.5, 9)]), "M17 9C18.5 6 20.5 6.5 19.5 9")),
    ]


@icon("blowing-out-candles", CAT, "Face in profile blowing at a small birthday cake with lit candles",
      tags=["birthday", "blow out candles", "make a wish", "cake", "party", "celebration"], aliases=["make-a-wish"])
def _(S):
    return [
        shell(profile(-0.5, 4.5, False, 0.75)),
        line(seg(12.5, 12, 14.5, 12)), line(seg(12, 15, 13.5, 15)),
        shell(rect(15.5, 15.5, 6.5, 6, min(S.R, 1.5))),
        line(seg(17, 11.5, 17, 15.5)), line(seg(20.5, 11.5, 20.5, 15.5)),
        solid("M17.3 9.8C18.8 9.2 19 7.8 18.2 6.5C17.8 7.7 16.4 8.1 16.4 9.2C16.4 9.6 16.8 10 17.3 9.8Z"),
        solid("M20.8 9.8C22.3 9.2 22.5 7.8 21.7 6.5C21.3 7.7 19.9 8.1 19.9 9.2C19.9 9.6 20.3 10 20.8 9.8Z"),
    ]


@icon("cheering-person", CAT, "Person jumping for joy with both fists raised in a V",
      tags=["cheer", "celebrate", "victory", "yay", "success", "excited"], aliases=["celebrating-person"])
def _(S):
    return [
        dot(12, 8, HR),
        limb(S, (6.5, 4.5), (9.5, 11.5), (14.5, 11.5), (17.5, 4.5)),
        dot(6, 3.5, 1.5), dot(18, 3.5, 1.5),
        limb(S, (12, 11.5), (12, 15.5)),
        limb(S, (8, 21), (9, 18), (12, 15.5), (15, 18), (16, 21)),
    ]


@figure("marriage-proposal", "Person kneeling on one knee holding up a diamond ring to a standing partner",
        tags=["proposal", "engagement", "will you marry me", "ring", "romance", "wedding"], aliases=["proposal"])
def _(S):
    return [
        [line(circle(12, 10, 2)), solid(poly([(10.5, 6.5), (12, 5), (13.5, 6.5), (12, 8)], closed=True))],
        [dot(4.5, 7.5, HR), limb(S, (5, 11), (5.5, 16.5)),
         limb(S, (2, 21.5), (5.5, 21.5), (5.5, 16.5), (9.5, 16.5), (9.5, 21.5)),
         limb(S, (5, 12), (8, 13.5), (10.5, 12.5)),
         dot(19, 4.5, HR), limb(S, (19, 8.5), (19, 15)), limb(S, (17, 21.5), (19, 15), (21, 21.5)),
         limb(S, (16.5, 12.5), (19, 9.5), (21.5, 12.5))],
    ]


@figure("graduation-cap-toss", "Graduation caps tossed up into the air with motion lines",
        tags=["graduation", "cap toss", "graduate", "class of", "commencement", "celebration"], aliases=["hat-toss"], gap=0.75)
def _(S):
    def cap(cx, cy, deg, w=6.0, h=3.0, sk=3.0):
        c = (cx, cy)
        board = rpts([(cx - w, cy), (cx, cy - h), (cx + w, cy), (cx, cy + h)], deg, c)
        pts = rpts([(cx - sk, cy), (cx - sk, cy + 4.5), (cx + sk, cy + 4.5), (cx + sk, cy)], deg, c)
        return [shell(poly(board, closed=True, r=S.r * 0.5), stroke_miterlimit="2")], [line(poly(pts, r=S.r * 0.5))]
    b1, s1 = cap(8.5, 5.5, -15)
    b2, s2 = cap(15.5, 14, 15, 5.5, 2.75, 2.75)
    return [b2, s2, b1, s1, [line(seg(3, 17, 5.5, 14.5)), line(seg(6, 21, 8.5, 18.5))]]


@icon("mind-your-head", CAT, "Person walking under a low beam and bumping their head, with a star at the impact",
      tags=["mind your head", "low ceiling", "low clearance", "caution", "head injury", "duck"], aliases=["low-ceiling"])
def _(S):
    return [
        shell(rect(2, 2.5, 20, 3.5, min(S.R, 1))),
        dot(9.5, 9, HR),
        limb(S, (9, 12.5), (8.5, 17)),
        limb(S, (5, 21.5), (8.5, 17), (11.5, 19), (12, 21.5)),
        limb(S, (5.5, 16), (6.5, 13.5), (9, 12.5), (11, 14.5), (13.5, 15)),
        solid(poly(burst(15.5, 9, 2.75, 1.1, 4, -90), closed=True)),
    ]


@icon("watch-your-step", CAT, "Person stepping down off a raised edge marked with a warning stripe",
      tags=["watch your step", "mind the step", "trip hazard", "caution", "step down", "safety sign"], aliases=["mind-the-step"])
def _(S):
    return [
        dot(8, 4.5, HR),
        limb(S, (8.5, 8), (9.5, 13)),
        limb(S, (6.5, 14), (9.5, 13), (13, 16.5), (14.5, 20.5)),
        limb(S, (6, 11.5), (8.5, 8.5), (11.5, 10.5)),
        line(pick(S, poly([(2, 15.5), (10.5, 15.5), (10.5, 21.5), (22, 21.5)]),
                  poly([(2, 15.5), (10.5, 15.5), (10.5, 21.5), (22, 21.5)], r=1.5))),
        shell(poly([(18, 3), (21.5, 10), (14.5, 10)], closed=True, r=S.r * 0.4)),
        dot(18, 8.25, 0.7), detail(seg(18, 5.5, 18, 6.5)),
    ]


@icon("mind-the-gap", CAT, "Person stepping across the gap between a platform edge and a train floor",
      tags=["mind the gap", "platform gap", "train", "subway", "underground", "safety sign"], aliases=["platform-gap"])
def _(S):
    return [
        dot(12, 4, HR),
        limb(S, (11.5, 7.5), (11, 12)),
        limb(S, (4.5, 17), (8, 14.5), (11, 12), (14.5, 13.5), (17.5, 17)),
        limb(S, (8, 11), (11.5, 8.5), (15, 10.5)),
        shell(rect(2, 19, 8, 3, min(S.R, 1))),
        shell(rect(14, 19, 8, 3, min(S.R, 1))),
        line(seg(20.5, 2.5, 20.5, 14.5) if S.name == "line" else seg(20.5, 3, 20.5, 14)),
    ]


@icon("social-distancing", CAT, "Two people standing apart with a double-headed arrow between them",
      tags=["social distancing", "keep your distance", "stand apart", "spacing", "two metres", "six feet"],
      aliases=["keep-distance"])
def _(S):
    def fig(x):
        return [dot(x, 5, HR), limb(S, (x - 2.5, 14), (x - 2, 9.5), (x + 2, 9.5), (x + 2.5, 14)), line(seg(x, 9.5, x, 14.5)),
                limb(S, (x - 2, 21.5), (x, 14.5), (x + 2, 21.5))]
    return [
        *fig(4.5), *fig(19.5),
        line(seg(9, 12, 15, 12)),
        line(poly([(10.5, 10), (8.5, 12), (10.5, 14)], r=S.r * 0.4)),
        line(poly([(13.5, 10), (15.5, 12), (13.5, 14)], r=S.r * 0.4)),
    ]


@figure("assembly-point", "Small group of people with arrows pointing in towards them from each corner",
        tags=["assembly point", "muster point", "emergency meeting point", "fire drill", "evacuation", "gather"],
        aliases=["muster-point"], gap=1.0)
def _(S):
    arrows = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            tip = (12 + sx * 6.5, 12 + sy * 6.5)
            tail = (12 + sx * 9.75, 12 + sy * 9.75)
            arrows.append(line(seg(*tail, *tip)))
            arrows.append(line(poly([(tip[0], tip[1] + sy * 3), tip, (tip[0] + sx * 3, tip[1])], r=S.r * 0.4)))
    return [
        arrows,
        [dot(12, 11, 1.75), line(bust_d(S, 12, 14, 2.75, 16.5))],
        [dot(8.25, 9, 1.5), line(bust_d(S, 8.25, 11.75, 2.25, 14.5)), dot(15.75, 9, 1.5), line(bust_d(S, 15.75, 11.75, 2.25, 14.5))],
    ]


@icon("person-smoking", CAT, "Head in profile holding a cigarette at the lips with a curl of smoke",
      tags=["smoking", "cigarette", "smoker", "smoking area", "tobacco", "smoke"], aliases=["smoker"])
def _(S):
    return [
        shell(profile(0, 0)),
        shell(rect(14.5, 13, 5.5, 2, 0.3)), solid(rect(20.5, 13, 1.5, 2, 0.3)),
        line("M20.5 10.5C19 9.5 19 8 20.5 7C22 6 22 4.5 20.5 3.5"),
    ]


@icon("recovery-position", CAT, "Person lying on their side with the top knee bent and a hand under the cheek",
      tags=["recovery position", "first aid", "unconscious", "lateral position", "emergency", "safe position"])
def _(S):
    return [
        dot(4.5, 13.5, HR),
        limb(S, (7.5, 16), (14, 16)),
        limb(S, (14, 16), (21.5, 16.5)),
        limb(S, (14, 16), (16.5, 12), (19, 12)),
        limb(S, (8.5, 16), (9.5, 11.5), (5.5, 10)),
        line(seg(2, 19.5, 22, 19.5) if S.name == "line" else seg(2.5, 19.5, 21.5, 19.5)),
    ]


@icon("performing-cpr", CAT, "Kneeling rescuer pressing with straight arms on the chest of a person lying down",
      tags=["cpr", "chest compressions", "resuscitation", "first aid", "cardiac arrest", "life saving"], aliases=["cpr"])
def _(S):
    return [
        dot(4, 18, HR),
        line(seg(7, 20, 22, 20) if S.name == "line" else seg(7, 20, 21.5, 20)),
        dot(11, 3.5, HR),
        limb(S, (12, 7), (16, 12.5)),
        limb(S, (16, 12.5), (19.5, 16), (21.5, 17)),
        limb(S, (12, 7.5), (9.5, 17.5)),
    ]


@figure("heimlich-maneuver", "Person standing behind another with arms around the waist giving abdominal thrusts",
        tags=["heimlich", "choking", "abdominal thrusts", "first aid", "airway", "emergency"],
        aliases=["heimlich-manoeuvre", "abdominal-thrusts"])
def _(S):
    return [
        [limb(S, (8.5, 9.5), (11, 12.5), (16, 12.5)), dot(16.5, 12.5, 1.5)],
        [dot(15.5, 4.5, HR), limb(S, (15, 8.5), (14.5, 15)), limb(S, (13, 21.5), (14.5, 15), (17, 21.5)),
         limb(S, (15, 9.5), (17.5, 9), (17, 7))],
        [dot(8.5, 5, HR), limb(S, (8.5, 9), (8.5, 15)), limb(S, (6, 21.5), (8.5, 15), (11, 21.5))],
    ]


@icon("hands-showing-size", CAT, "Two flat hands held apart facing each other with a double-headed arrow between them",
      tags=["size", "this big", "measure", "how big", "length", "gesture"], aliases=["this-big"])
def _(S):
    wr_ = pick(S, 0.5, 1.75)
    lh = [capsule(4.5, 4, 4.5, 14), P(rect(2.8, 12, 3.4, 9.5, wr_)), capsule(5, 13.5, 7.5, 10.5, 2.8)]
    rh = [capsule(19.5, 4, 19.5, 14), P(rect(17.8, 12, 3.4, 9.5, wr_)), capsule(19, 13.5, 16.5, 10.5, 2.8)]
    return [
        outline(*lh), outline(*rh),
        line(seg(9, 6, 15, 6)),
        line(poly([(10.5, 4), (8.5, 6), (10.5, 8)], r=S.r * 0.4)),
        line(poly([(13.5, 4), (15.5, 6), (13.5, 8)], r=S.r * 0.4)),
    ]


@icon("calm-down-gesture", CAT, "Two hands held palm down side by side with arrows pressing downwards",
      tags=["calm down", "settle down", "relax", "take it easy", "lower", "gesture"], aliases=["settle-down"])
def _(S):
    def hand(x0, thumb_right):
        fingers = P(rect(x0, 2.5, 6.5, 8, pick(S, 1.5, 3)))
        palm = P(rect(x0, 7, 6.5, 6, pick(S, 0.5, 2)))
        tx = x0 + 6.5 if thumb_right else x0
        k = 1 if thumb_right else -1
        thumb = capsule(tx - k * 0.75, 12, tx + k * 1, 9.5, 2.6)
        return outline(fingers, palm, thumb)
    return [
        hand(2, True), hand(15.5, False),
        detail(seg(4.25, 2.5, 4.25, 6.5)), detail(seg(6.25, 2.5, 6.25, 6.5)),
        detail(seg(17.75, 2.5, 17.75, 6.5)), detail(seg(19.75, 2.5, 19.75, 6.5)),
        line(seg(5.25, 16, 5.25, 21)), line(poly([(2.75, 18.5), (5.25, 21), (7.75, 18.5)], r=S.r * 0.4)),
        line(seg(18.75, 16, 18.75, 21)), line(poly([(16.25, 18.5), (18.75, 21), (21.25, 18.5)], r=S.r * 0.4)),
    ]
