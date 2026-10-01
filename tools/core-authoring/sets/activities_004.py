"""TypeIcon Core: activities (batch 004): everyday actions, gestures and small scenes.

Figures follow the people set: a head disc r 2.25 over 2 px limbs, polylines filleted with S.r so Line and
Rounded differ. Hands are regions (finger capsules unioned with a palm) outlined as one shell. Overlapping
parts are drawn in layers (front first): what lies behind is cut away around the front with a gap, in every
style, so scenes stay readable at 16 px.
"""
from __future__ import annotations

import math

from dsl import LINE, D, I, P, ST, U, Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "activities"
FW = 3.0  # finger width


# --------------------------------------------------------------------------- region helpers

def cap(x0, y0, x1, y1, w=FW):
    """Finger or limb capsule along a segment."""
    return ST(seg(x0, y0, x1, y1), w, "round", "round")


def box(x, y, w, h, r=0.0):
    return P(rect(x, y, w, h, r))


def outline(*regions, **attrs):
    return shell(path_to_d(U(*regions)), **attrs)


def wr(S):
    """Palm / wrist corner radius: square for Line, soft for Rounded."""
    return 0.5 if S.name == "line" else 2.0


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def pl(S, pts, closed=False, k=1.0):
    return poly(pts, closed=closed, r=S.r * k)


def head(x, y, r=2.25):
    return dot(x, y, r)


def ell_arc(cx, cy, rx, ry, a0, a1, n=24):
    """Elliptical arc as a smooth polyline-free path (SVG A), angles in degrees clockwise on screen."""
    p0 = (cx + rx * math.cos(math.radians(a0)), cy + ry * math.sin(math.radians(a0)))
    p1 = (cx + rx * math.cos(math.radians(a1)), cy + ry * math.sin(math.radians(a1)))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{fmt(p0[0])} {fmt(p0[1])}A{fmt(rx)} {fmt(ry)} 0 {large} 1 {fmt(p1[0])} {fmt(p1[1])}"


def flake(cx, cy, r=2.5):
    """Small snowflake: three crossing strokes."""
    return [line(seg(*polar(cx, cy, r, a), *polar(cx, cy, r, a + 180))) for a in (90, 30, -30)]


def drop_d(cx, cy, h=4.0, w=3.0):
    """Tear drop pointing up, centred at the round bottom (cx, cy)."""
    r = w / 2
    return (f"M{fmt(cx)} {fmt(cy - h)}L{fmt(cx + r * 0.9)} {fmt(cy - r * 0.4)}"
            f"A{fmt(r)} {fmt(r)} 0 1 1 {fmt(cx - r * 0.9)} {fmt(cy - r * 0.4)}Z")


def waves(S, y, x0=3.0, x1=21.0, amp=1.25, n=3):
    """Gentle wave line: n humps between x0 and x1 (quadratic curves)."""
    w = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        a = x0 + i * w
        d += f"Q{fmt(a + w / 4)} {fmt(y - amp * 2)} {fmt(a + w / 2)} {fmt(y)}T{fmt(a + w)} {fmt(y)}"
    return d


# --------------------------------------------------------------------------- layering

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


def scene(name, desc, tags, aliases=(), gap=1.5):
    """Register an icon drawn as layers: fn(S) -> [front parts, parts behind, ...]."""
    def deco(fn):
        icon(name, CAT, desc, tags=tags, aliases=aliases,
             filled=lambda: _filled_layers(fn(LINE), gap))(lambda S: _stroke_layers(S, fn(S), gap))
        return fn
    return deco


# ============================================================================ hands and gestures

@icon("reaching-out-hand", CAT, "An arm stretched forward with the hand open toward a dot just out of reach.",
      tags=["reach", "reach out", "grasp", "almost", "out of reach", "stretch"])
def _(S):
    sleeve = shell(rect(2, 11, 5, 6.5, min(S.R, 1)) if S.name == "line" else rect(2, 11, 5, 6.5, 1.5))
    palm = box(8.5, 11.5, 4.5, 5.5, wr(S) * 0.6)
    fingers = [cap(12, 12.5, 16, 11.5, 2.4), cap(12, 15, 16.5, 15, 2.4), cap(11.5, 16.5, 15.5, 18.5, 2.4)]
    thumb = cap(10, 12, 12, 8.5, 2.4)
    return [sleeve, outline(palm, thumb, *fingers), dot(20.5, 13.5, 1.5)]


@icon("letting-go", CAT, "An open hand with spread fingers and a small bird flying away from it.",
      tags=["let go", "release", "freedom", "set free", "bird", "open hand"])
def _(S):
    palm = box(5.5, 15.5, 7, 6.5, wr(S))
    w = 2.4
    fingers = [cap(6.5, 18, 3, 14.5, w), cap(7, 16.5, 4.5, 10, w), cap(9, 16.5, 9.5, 8.5, w), cap(11.5, 17, 14.5, 11, w)]
    bird = "M13 7A2.6 2.6 0 0 1 17.5 7A2.6 2.6 0 0 1 22 7"
    return [outline(palm, *fingers), line(bird)]


@icon("finger-frame", CAT, "Two hands forming a rectangle with thumbs and index fingers, framing a view.",
      tags=["frame", "framing", "director", "viewfinder", "composition", "photo"])
def _(S):
    r = wr(S)
    left = [box(2.5, 15.5, 6, 6, r), cap(5, 16, 5, 6.5), cap(8, 18.5, 14, 18.5)]
    right = [box(15.5, 2.5, 6, 6, r), cap(19, 8, 19, 17.5), cap(16, 5.5, 10, 5.5)]
    return [outline(*left), outline(*right)]


# ============================================================================ poses

@scene("hands-behind-head", "A person leaning back with both hands clasped behind the head and elbows out.",
       tags=["relax", "relaxed", "laid back", "chill", "break", "leisure"])
def _(S):
    body = shell(_bust(S, 12, 15.5, 6.5, 21.5))
    arms = [line(pl(S, [(6.5, 16), (3.5, 8.5), (9, 5.5)])), line(pl(S, [(17.5, 16), (20.5, 8.5), (15, 5.5)]))]
    return [[shell(circle(12, 9, 3.5))], [body], arms]


def _bust(S, cx=12.0, top=14.0, hw=7.0, bottom=21.0):
    """Open-bottom shoulders as in the people set. Line has squarer shoulders than Rounded."""
    r = hw - (1.0 if S.name != "line" else 2.0)
    r = min(r, bottom - top)
    x0, x1 = cx - hw, cx + hw
    return (f"M{fmt(x0)} {fmt(bottom)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + r)} {fmt(top)}"
            f"H{fmt(x1 - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(bottom)}")


@scene("chin-on-hand", "A head in profile with the chin resting on a fist propped on a bent arm.",
       tags=["thinking", "pondering", "bored", "daydream", "chin on hand", "listening"])
def _(S):
    fist = shell(rect(11.5, 13, 5.5, 4.5, min(S.R, 2)))
    return [[fist, line(seg(15, 17.5, 16, 21.5)), line(seg(2, 21.5, 22, 21.5))],
            [shell(circle(9.5, 8, 4.5))],
            [line(pl(S, [(4, 21.5), (4.5, 17), (9, 15)]))]]


@scene("sneezing-into-elbow", "A head in profile sneezing into a raised bent elbow, with droplets stopped by the sleeve.",
       tags=["sneeze", "cough", "etiquette", "hygiene", "cover your cough", "germs"])
def _(S):
    face = shell(circle(16.5, 9, 4))
    arm = line(pl(S, [(16, 21), (5, 13.5), (8.5, 4)]), stroke_width="2")
    return [[face], [arm, dot(9.8, 9.5, 1), dot(10.3, 12.5, 1)]]


@icon("twirling", CAT, "A person spinning on one foot with arms out and a curved arrow circling around the feet.",
      tags=["twirl", "spin", "pirouette", "dance", "turn around", "whirl"])
def _(S):
    rx, ry, cy = 8, 3, 17.5
    front = ell_arc(12, cy, rx, ry, 0, 180)
    tip = (4, 15)
    arrow = pl(S, [(2, 17.2), tip, (6, 17.2)], k=0.4)
    return [head(12, 3.5), line(pl(S, [(5, 5.5), (8, 7.5), (16, 7.5), (19, 5.5)])), line(seg(12, 7.5, 12, 17)),
            line(pl(S, [(12, 12.5), (16, 13.5), (14.5, 16)], k=0.5)), line(front + f"L{fmt(4)} {fmt(15.8)}"), line(arrow)]


@icon("ducking", CAT, "A person crouched low with the head down as a ball flies past above.",
      tags=["duck", "dodge", "crouch", "avoid", "take cover", "evade"])
def _(S):
    return [head(15.5, 14), line(pl(S, [(6, 15.5), (12, 11.5), (16.5, 9.5)])),
            line(pl(S, [(6, 15.5), (11.5, 17), (10.5, 21.5)])), line(seg(3, 21.5, 21, 21.5)),
            shell(circle(6, 5, 2.5)), line(seg(11, 3.5, 20, 3.5)), line(seg(11, 6.5, 16.5, 6.5))]


@icon("hugging-knees", CAT, "A seated person with knees drawn up to the chest and arms wrapped around them.",
      tags=["sitting", "hug knees", "curled up", "sad", "lonely", "waiting"])
def _(S):
    return [head(8.5, 5), line(pl(S, [(8, 9), (7, 19), (13.5, 10.5), (16.5, 19)])),
            line(pl(S, [(8, 10.5), (15.5, 14)])), line(seg(3, 21.5, 21, 21.5))]


@icon("lying-on-stomach", CAT, "A person lying face down with the head propped on the forearms and feet in the air.",
      tags=["lying down", "lounging", "reading on floor", "relaxing", "prone", "rest"])
def _(S):
    return [head(5, 9.5), line(pl(S, [(9, 13), (17, 15.5), (20, 10)])),
            line(pl(S, [(9, 13), (8.5, 17), (4, 16)])), line(seg(2, 20, 22, 20))]


@icon("person-kicking", CAT, "A person balanced on one leg with the other leg kicked high forward.",
      tags=["kick", "high kick", "martial arts", "dance", "exercise", "stretch"])
def _(S):
    return [head(8, 4.5), line(seg(8.5, 8.5, 9, 14)), line(pl(S, [(9, 14), (8, 21.5)])),
            line(pl(S, [(9, 14), (19.5, 5.5)])), line(pl(S, [(3.5, 13), (8.5, 9), (12.5, 11)]))]


@icon("leaping", CAT, "A person in mid-air with legs stretched in a wide split and arms raised.",
      tags=["leap", "jump", "split leap", "dance", "joy", "ballet"])
def _(S):
    return [head(12, 4.5), line(pl(S, [(6.5, 3), (9, 9), (15, 9), (17.5, 3)])), line(seg(12, 9, 12, 13)),
            line(pl(S, [(2.5, 16.5), (12, 13), (21.5, 16.5)])), line(seg(8.5, 21, 15.5, 21))]


# --------------------------------------------------------------------------- profile head (facing right)

def _xf(ox, oy, k, deg, c=(10.0, 12.0)):
    a = math.radians(deg)
    cs, sn = math.cos(a), math.sin(a)

    def f(p):
        x, y = p[0] - c[0], p[1] - c[1]
        x, y = x * cs - y * sn + c[0], x * sn + y * cs + c[1]
        return (ox + k * x, oy + k * y)
    return f


def _cmds_d(cmds, f, k):
    out = []
    for c in cmds:
        op = c[0]
        if op in ("M", "L"):
            q = f(c[1]); out.append(f"{op}{fmt(q[0])} {fmt(q[1])}")
        elif op == "A":
            q = f(c[4]); out.append(f"A{fmt(c[1] * k)} {fmt(c[1] * k)} 0 {c[2]} {c[3]} {fmt(q[0])} {fmt(q[1])}")
        elif op == "Q":
            a, b = f(c[1]), f(c[2]); out.append(f"Q{fmt(a[0])} {fmt(a[1])} {fmt(b[0])} {fmt(b[1])}")
        elif op == "C":
            a, b, e = f(c[1]), f(c[2]), f(c[3])
            out.append(f"C{fmt(a[0])} {fmt(a[1])} {fmt(b[0])} {fmt(b[1])} {fmt(e[0])} {fmt(e[1])}")
        elif op == "Z":
            out.append("Z")
    return "".join(out)


def profile(S, ox=0.0, oy=0.0, k=1.0, deg=0.0, mouth="closed"):
    """Head and neck in profile facing right (the body-set head), in a 4..20.5 x 3..21 box, scaled by k about
    the origin, rotated by deg about (10, 12) and shifted by (ox, oy). Line has a pointed nose and square neck;
    Rounded softens them. mouth="open" cuts a small notch under the nose."""
    f = _xf(ox, oy, k, deg)
    soft = S.name == "rounded"
    cmds = [("M", (8, 21)) if not soft else ("M", (8, 20)), ("L", (8, 17.2)), ("C", (5.6, 15.8), (4, 13.3), (4, 10.5)),
            ("C", (4, 6.4), (7.6, 3), (12, 3)), ("C", (16.1, 3), (19, 5.9), (19, 9.5))]
    if soft:
        cmds += [("L", (20.2, 12)), ("Q", (20.6, 12.9), (19.7, 13.1)), ("L", (19, 13.3))]
    else:
        cmds += [("L", (20.5, 12.8)), ("L", (19, 13.3))]
    if mouth == "open":
        cmds += [("L", (19, 13.6)), ("L", (16.5, 14.5)), ("L", (19, 15.4))]
    cmds += [("L", (19, 15.5)), ("C", (19, 16.6), (18.1, 17.5), (17, 17.5)), ("L", (14, 17.5))]
    if soft:
        cmds += [("L", (14, 20)), ("Q", (14, 21), (13, 21)), ("L", (9, 21)), ("Q", (8, 21), (8, 20))]
    else:
        cmds += [("L", (14, 21))]
    cmds += [("Z",)]
    return _cmds_d(cmds, f, k)


def pt_xf(p, ox=0.0, oy=0.0, k=1.0, deg=0.0):
    return _xf(ox, oy, k, deg)(p)


# ============================================================================ water and food

@icon("floating-in-water", CAT, "A person lying on their back on the water with arms and legs spread.",
      tags=["float", "floating", "swim", "relax", "pool", "lake"])
def _(S):
    return [head(4.5, 11), line(pl(S, [(7.5, 12.5), (15, 12.5), (21, 10.5)])), line(pl(S, [(9.5, 12.5), (13, 8)])),
            line(pl(S, [(15, 12.5), (20.5, 14)])), line(waves(S, 18.5, 2, 22, 1.0, 4))]


@icon("wading-in-water", CAT, "A person standing knee deep in water with waves around the legs.",
      tags=["wading", "paddling", "shallow water", "beach", "river", "knee deep"])
def _(S):
    return [head(12, 4), line(pl(S, [(6.5, 13), (8.5, 8.5), (15.5, 8.5), (17.5, 13)])), line(seg(12, 8.5, 12, 13)),
            line(pl(S, [(9.5, 16), (12, 12.5), (14.5, 16)])),
            line(waves(S, 19.5, 2, 22, 1.0, 4))]


@scene("taking-a-bite", "A face in profile with the mouth open, biting into an apple.",
       tags=["bite", "eat", "eating", "apple", "snack", "hungry"])
def _(S):
    apple = "M18.5 11C20.5 10 22.3 11.5 22 14.5C21.7 18 20 20.5 18.5 20C17 20.5 15.3 18 15 14.5C14.7 11.5 16.5 10 18.5 11Z"
    return [[shell(apple), line(seg(18.5, 10.5, 19.2, 8))], [shell(profile(S, -2, 2, 0.85, 0, "open"))]]


@scene("licking-ice-cream", "A face in profile with the tongue touching a scoop of ice cream on a cone.",
       tags=["ice cream", "lick", "cone", "dessert", "summer", "treat"])
def _(S):
    cone = pl(S, [(16, 12.5), (21.5, 12.5), (18.75, 20.5)], closed=True, k=0.4)
    return [[shell(circle(18.75, 9.5, 2.75)), shell(cone, stroke_miterlimit="2")], [line(seg(14, 14, 15.8, 12.5))],
            [shell(profile(S, -2.5, 2, 0.85, 0, "open"))]]


def _glass(S, cx, top, deg):
    c = (cx, top + 8)

    def f(p):
        return pt_xf(p, 0, 0, 1, 0)
    a = math.radians(deg)

    def rot(p):
        x, y = p[0] - c[0], p[1] - c[1]
        return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))
    p = [rot(q) for q in [(cx - 3, top), (cx + 3, top), (cx + 3, top + 3), (cx, top + 6.5), (cx - 3, top + 3)]]
    bowl = (f"M{fmt(p[0][0])} {fmt(p[0][1])}L{fmt(p[1][0])} {fmt(p[1][1])}L{fmt(p[2][0])} {fmt(p[2][1])}"
            f"A3 3 0 0 1 {fmt(p[4][0])} {fmt(p[4][1])}Z")
    s0, s1 = rot((cx, top + 6)), rot((cx, top + 13))
    b0, b1 = rot((cx - 2.5, top + 13)), rot((cx + 2.5, top + 13))
    return [shell(bowl), line(seg(*s0, *s1)), line(seg(*b0, *b1))]


@icon("clinking-glasses", CAT, "Two wine glasses tilted toward each other, touching at the rims, with spark lines.",
      tags=["cheers", "toast", "celebrate", "drinks", "wine", "party"])
def _(S):
    return (_glass(S, 8.2, 7.5, 14) + _glass(S, 15.8, 7.5, -14) +
            [line(seg(12, 2, 12, 4.5)), line(seg(7.5, 3, 9, 5)), line(seg(16.5, 3, 15, 5))])


# ============================================================================ home routines

@scene("person-showering", "A person standing under a round shower head with water falling on them.",
       tags=["shower", "wash", "bathe", "bathroom", "hygiene", "morning routine"])
def _(S):
    dome = "M7.5 7A4.5 3.5 0 0 1 16.5 7Z"
    return [[shell(dome), line(pl(S, [(12, 3.5), (12, 2.5), (21, 2.5)])),
             line(seg(8.5, 9.5, 8, 11.5)), line(seg(12, 9.5, 12, 11.5)), line(seg(15.5, 9.5, 16, 11.5)),
             dot(12, 15, 2.25), shell(_bust(S, 12, 19, 5.5, 22))]]


@icon("looking-in-mirror", CAT, "A person standing in front of an oval mirror with their reflection inside.",
      tags=["mirror", "reflection", "self image", "getting ready", "dressing", "vanity"])
def _(S):
    return [head(5.5, 5), line(pl(S, [(2.5, 14), (3.5, 9.5), (7.5, 9.5), (9.5, 12)])), line(seg(5.5, 9.5, 5.5, 14.5)),
            line(pl(S, [(3.5, 21.5), (5.5, 14.5), (7.5, 21.5)])),
            shell(ellipse(16.5, 10, 4.5, 7.5)), dot(16.5, 8.5, 1.5), line("M14 14.5A2.5 2.5 0 0 1 19 14.5"),
            line(seg(16.5, 17.5, 16.5, 21.5)), line(seg(13.5, 21.5, 19.5, 21.5))]


@icon("going-to-bed", CAT, "A person lying in bed under a blanket with a crescent moon above.",
      tags=["bedtime", "go to bed", "sleep", "night", "rest", "goodnight"])
def _(S):
    blanket = pl(S, [(8.5, 16), (8.5, 12), (21, 12), (21, 16)], k=0.6)
    moon = "M19 2.5A3.5 3.5 0 1 0 22 7A2.8 2.8 0 0 1 19 2.5Z"
    return [line(seg(2.5, 8, 2.5, 21.5)), line(seg(2.5, 16, 21.5, 16)), line(seg(21, 16, 21, 21.5)),
            dot(6, 12.5, 2), shell(blanket), shell(moon)]


@icon("napping-in-hammock", CAT, "A person lying in a hammock slung between two posts, with a small z above.",
      tags=["nap", "siesta", "hammock", "relax", "lazy", "summer"])
def _(S):
    zz = pl(S, [(10.5, 3), (14, 3), (10.5, 7), (14, 7)], k=0.3)
    return [line(seg(2.5, 7, 2.5, 21.5)), line(seg(21.5, 7, 21.5, 21.5)),
            line("M2.5 10Q12 20 21.5 10"), dot(7, 10.5, 2), line(pl(S, [(10, 14), (16.5, 13), (18, 10.5)])), line(zz)]


# ============================================================================ together

@icon("coffee-chat", CAT, "Two people sitting at a small round table facing each other, each with a mug.",
      tags=["coffee", "chat", "meet up", "cafe", "catch up", "conversation"])
def _(S):
    parts = [line(seg(8.5, 12.5, 15.5, 12.5)), line(seg(12, 12.5, 12, 21.5)), line(seg(9.5, 21.5, 14.5, 21.5))]
    for sx in (1, -1):
        X = (lambda x: x) if sx == 1 else (lambda x: 24 - x)
        parts += [head(X(4), 5), line(pl(S, [(X(3.5), 8.5), (X(3.5), 15.5), (X(7), 15.5), (X(7), 21.5)])),
                  shell(rect(min(X(8.5), X(10.5)), 8.5, 2, 2.5, 0.5 if S.name == "rounded" else 0))]
    return parts


@scene("talking-on-phone", "A person holding a phone to their ear.",
       tags=["phone call", "talking", "calling", "on the phone", "chat", "call"])
def _(S):
    phone = shell(rect(12.5, 4, 3.5, 8, min(S.R, 1)))
    return [[shell(circle(9, 10, 3.5)), shell(_bust(S, 9, 16.5, 6.5, 22))], [phone],
            [line(pl(S, [(17.5, 21.5), (18.5, 16), (15, 12)]))]]


@icon("giving-directions", CAT, "A person pointing the way while a second person beside them holds an open map.",
      tags=["directions", "pointing", "which way", "tourist", "map", "help"])
def _(S):
    mp = pl(S, [(13, 9), (15.5, 10), (18, 9), (20.5, 10), (20.5, 15), (18, 14), (15.5, 15), (13, 14)], closed=True, k=0.3)
    return [head(5, 4.5), line(seg(5, 8.5, 5, 14.5)), line(pl(S, [(5, 9.5), (10.5, 8)])),
            line(pl(S, [(3, 21.5), (5, 14.5), (7, 21.5)])),
            head(17, 4), shell(mp), detail(seg(15.5, 10, 15.5, 15)), detail(seg(18, 9, 18, 14)),
            line(pl(S, [(15, 21.5), (16.8, 17)])), line(pl(S, [(19, 21.5), (17.2, 17)]))]


@scene("sharing-umbrella", "Two people standing close together under one open umbrella, with rain around.",
       tags=["umbrella", "rain", "together", "couple", "shelter", "share"])
def _(S):
    canopy = "M2.5 10A9.5 8 0 0 1 21.5 10Z"
    return [[shell(canopy), line(seg(12, 2, 12, 1))],
            [dot(8, 14.5, 2), shell(_bust(S, 8, 18.5, 4, 22)), dot(16, 14.5, 2), shell(_bust(S, 16, 18.5, 4, 22))]]


# ============================================================================ play and outings

def _pillow(S, cx, cy, w=6.0, h=4.0, deg=0.0):
    """Puffy pillow: a rectangle with slightly pinched sides and corner tips."""
    a = math.radians(deg)

    def r(p):
        x, y = p[0] - cx, p[1] - cy
        return (cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a))
    hw, hh = w / 2, h / 2
    pts = [(cx - hw, cy - hh), (cx, cy - hh + 0.6), (cx + hw, cy - hh), (cx + hw - 0.6, cy), (cx + hw, cy + hh),
           (cx, cy + hh - 0.6), (cx - hw, cy + hh), (cx - hw + 0.6, cy)]
    return pl(S, [r(p) for p in pts], closed=True, k=0.5)


@scene("pillow-fight", "Two people swinging pillows at each other with small feathers floating between them.",
       tags=["pillow fight", "sleepover", "play", "fun", "kids", "bedroom"])
def _(S):
    rr = 1.0 if S.name == "line" else 1.75
    pa = shell(_rot_d(rect(4.5, 2.5, 6.5, 4, rr), -25, (7.75, 4.5)))
    pb = shell(_rot_d(rect(13, 2.5, 6.5, 4, rr), 25, (16.25, 4.5)))
    parts = [pa, pb, dot(12, 10, 1), dot(11, 13.5, 1)]
    for mx in (False, True):
        X = (lambda x: 24 - x) if mx else (lambda x: x)
        parts += [head(X(4), 10.5), line(seg(X(4), 14, X(4), 17.5)),
                  line(pl(S, [(X(2.5), 21.5), (X(4), 17.5), (X(6), 21.5)])), line(pl(S, [(X(4), 14.5), (X(7), 12.5), (X(7.5), 8)]))]
    return [parts]


def _rot_d(d, deg, c):
    from dsl import transform_path
    a = math.radians(deg)
    cs, sn = math.cos(a), math.sin(a)
    return path_to_d(transform_path(P(d), (cs, sn, -sn, cs, c[0] - cs * c[0] + sn * c[1], c[1] - sn * c[0] - cs * c[1])))


@scene("filing-papers", "A folder being dropped into the top drawer of a filing cabinet.",
       tags=["filing", "file", "filing cabinet", "archive", "paperwork", "office"])
def _(S):
    cab = [shell(rect(5, 9, 14, 12.5, min(S.R, 2))), detail(seg(5, 15.25, 19, 15.25)),
           detail(seg(10.5, 12, 13.5, 12)), detail(seg(10.5, 18.25, 13.5, 18.25))]
    folder = pl(S, [(7.5, 9), (7.5, 3), (11, 3), (12, 4.5), (16.5, 4.5), (16.5, 9)], k=0.4)
    return [cab, [shell(folder + "Z")], [line(seg(20.5, 2.5, 20.5, 7)), line(pl(S, [(19, 5.5), (20.5, 7), (22, 5.5)], k=0.3))]]


@scene("study-group", "Three people seated around a table with an open book in front of them.",
       tags=["study group", "students", "homework", "revision", "classmates", "learning"])
def _(S):
    book = pl(S, [(6.5, 16), (12, 17.2), (17.5, 16), (17.5, 21.5), (12, 22), (6.5, 21.5)], closed=True, k=0.3)
    return [[shell(book), detail(seg(12, 17.2, 12, 22))],
            [line(seg(2, 14, 22, 14))],
            [dot(5, 5.5, 2), line("M1.5 12.5A3.5 3.5 0 0 1 8.5 12.5"), dot(19, 5.5, 2), line("M15.5 12.5A3.5 3.5 0 0 1 22.5 12.5"),
             dot(12, 4, 2), line("M8.5 11A3.5 3.5 0 0 1 15.5 11")]]


@scene("clocking-in", "A time card pushed into the slot of a wall-mounted time clock.",
       tags=["clock in", "punch in", "time card", "timesheet", "shift", "attendance"])
def _(S):
    return [[shell(rect(4.5, 6.5, 15, 15, min(S.R, 3))), detail(circle(12, 14, 3.75)),
             detail(pl(S, [(12, 12), (12, 14), (13.5, 15)], k=0.3))],
            [shell(rect(9, 2, 6, 7, min(S.R, 1))), detail(seg(10.5, 4, 13.5, 4))]]


@icon("window-shopping", CAT, "A person standing in front of a shop window looking at a dress on display.",
      tags=["window shopping", "browse", "shop window", "fashion", "retail", "boutique"])
def _(S):
    dress = pl(S, [(14.5, 8.5), (17, 8.5), (17.2, 11.5), (19, 17), (12.5, 17), (14.3, 11.5)], closed=True, k=0.3)
    return [shell(rect(10, 4, 11.5, 17.5, min(S.R, 2))), mark(dress), line(seg(15.75, 6, 15.75, 8)),
            head(5, 5.5), line(seg(5, 9, 5, 15)), line(pl(S, [(3, 21.5), (5, 15), (7, 21.5)])),
            line(pl(S, [(2.5, 13.5), (5, 9.5), (7.5, 12)]))]


@scene("donating-clothes", "A shirt going into the slot of a clothes donation bin marked with a heart.",
       tags=["donate", "clothes donation", "charity", "second hand", "give away", "recycle clothes"])
def _(S):
    heart = ("M12 19.5L9.6 17.1A1.5 1.5 0 0 1 12 15.2A1.5 1.5 0 0 1 14.4 17.1Z")
    shirt = pl(S, [(10, 2), (6.5, 4), (7.8, 6.5), (9, 6), (9, 11), (15, 11), (15, 6), (16.2, 6.5), (17.5, 4), (14, 2)], closed=True, k=0.4)
    return [[shell(rect(4.5, 10, 15, 11.5, min(S.R, 2))), detail(seg(8, 13, 16, 13)), mark(heart)],
            [shell(shirt), detail("M10 2A2 2 0 0 0 14 2")]]


@icon("boarding-bus", CAT, "A person stepping up into the open front door of a bus.",
      tags=["bus", "board", "get on", "public transport", "commute", "passenger"])
def _(S):
    return [shell(rect(8.5, 4.5, 14, 12, min(S.R, 2.5))), detail(seg(12, 4.5, 12, 16.5)), detail(seg(12, 9.5, 22.5, 9.5)),
            detail(seg(17, 4.5, 17, 9.5)), dot(15, 18.5, 1.75), dot(20, 18.5, 1.75),
            head(3.5, 7), line(seg(4, 10.5, 4.5, 15)), line(pl(S, [(4.5, 15), (7.5, 15.5), (7.5, 18)])),
            line(pl(S, [(4.5, 15), (3, 21.5)])), line(pl(S, [(4, 11.5), (6.5, 13)]))]


@scene("having-picnic", "Two people seated on a checked blanket with a picnic basket between them.",
       tags=["picnic", "park", "outdoors", "lunch", "summer", "blanket"])
def _(S):
    blanket = pl(S, [(4.5, 16), (19.5, 16), (22, 21.5), (2, 21.5)], closed=True, k=0.4)
    basket = [shell(rect(9, 10, 6, 5, min(S.R, 1.5))), line("M9.8 10A2.2 2.2 0 0 1 14.2 10")]
    return [[shell(blanket), detail(seg(12, 16, 12, 21.5)), detail(seg(3.5, 18.75, 20.5, 18.75))], basket,
            [dot(4, 5, 2), line(pl(S, [(4, 8.5), (4, 13.5), (8, 13.5)])), dot(20, 5, 2), line(pl(S, [(20, 8.5), (20, 13.5), (16, 13.5)]))]]


@icon("roasting-marshmallows", CAT, "A person holding a long stick with a marshmallow over a small campfire.",
      tags=["marshmallow", "campfire", "camping", "roast", "s'mores", "bonfire"])
def _(S):
    flame = "M18 11C16 13 15 14.5 15 16.5A3 3 0 0 0 21 16.5C21 14.5 20 13 18 11Z"
    return [head(4, 5.5), line(pl(S, [(4, 9), (4, 15.5), (8, 15.5), (8, 21.5)])), line(pl(S, [(4, 10.5), (7.5, 12)])),
            line(seg(7.5, 12, 15.5, 6.5)), shell(rect(15.5, 3.5, 3.5, 3, min(S.R, 1))),
            shell(flame), line(seg(13, 21.5, 22, 21.5))]


@icon("throwing-snowball", CAT, "A person with an arm drawn back holding a snowball, with snowflakes around.",
      tags=["snowball", "snowball fight", "winter", "snow", "throw", "play"])
def _(S):
    return [head(12, 5), line(seg(12, 9, 12, 15)), line(pl(S, [(9, 21.5), (12, 15), (15, 21.5)])),
            line(pl(S, [(12, 10), (8, 11), (6, 7)])), line(pl(S, [(12, 10), (16, 12.5)])),
            shell(circle(5, 4, 2)), *flake(19.5, 4.5, 2.5), *flake(4, 16.5, 2.25)]


@icon("jumping-in-puddles", CAT, "A person in boots jumping into a puddle with splash drops flying up.",
      tags=["puddle", "splash", "rain", "jump", "wellies", "kids play"])
def _(S):
    rb = 0.6 if S.name == "rounded" else 0
    return [head(12, 3.5), line(pl(S, [(6.5, 5.5), (8.5, 8), (15.5, 8), (17.5, 5.5)])), line(seg(12, 8, 12, 11.5)),
            line(pl(S, [(9, 15.5), (9.5, 13), (12, 11.5), (14.5, 13), (15, 15.5)])),
            mark(rect(7.5, 15.5, 3.5, 3, rb)), mark(rect(13, 15.5, 3.5, 3, rb)),
            line(seg(5, 21.5, 19, 21.5)),
            line(seg(3.5, 18, 4.5, 19.5)), line(seg(20.5, 18, 19.5, 19.5)), line(seg(3, 14, 4, 15.5)), line(seg(21, 14, 20, 15.5))]


@icon("catching-snowflakes", CAT, "A face tilted up with the tongue out and snowflakes falling toward it.",
      tags=["snowflakes", "snow", "winter", "tongue out", "playful", "first snow"])
def _(S):
    return [shell(profile(S, -1.5, 3, 0.85, -35, "open")), *flake(18.5, 4.5, 2.5), *flake(20, 12, 2)]


@scene("watching-sunset", "A person seen from behind, sitting and facing a half sun setting on the horizon.",
       tags=["sunset", "evening", "view", "relax", "calm", "dusk"])
def _(S):
    rays = [line(seg(*polar(15.5, 14, 6.5, a), *polar(15.5, 14, 8.3, a))) for a in (-160, -120, -90, -60, -20)]
    return [[dot(6.5, 12.5, 2.25), shell(_bust(S, 6.5, 17, 4.25, 22))],
            [shell("M11 14A4.5 4.5 0 0 1 20 14Z"), line(seg(2, 14, 22, 14))] + rays]


@scene("doing-jigsaw", "The last piece being placed into a nearly complete square jigsaw puzzle.",
       tags=["jigsaw", "puzzle", "hobby", "last piece", "complete", "pastime"])
def _(S):
    k = 0.5
    board = pl(S, [(3, 8), (10.5, 8), (10.5, 14), (17, 14), (17, 21.5), (3, 21.5)], closed=True, k=k)
    piece = path_to_d(U(P(pl(S, [(14, 2.5), (21, 2.5), (21, 9.5), (14, 9.5)], closed=True, k=k)), P(circle(13.8, 6, 1.6))))
    seams = [detail("M10.5 14V16A1.75 1.75 0 0 1 10.5 19.5V21.5"), detail("M3 14H5A1.75 1.75 0 0 0 8.5 14H10.5")]
    return [[shell(piece)], [shell(board)] + seams]


@scene("singing-in-shower", "A person under a shower head with water falling and music notes floating beside them.",
       tags=["singing", "shower", "music", "happy", "morning", "bathroom"])
def _(S):
    dome = "M3 7A4 3.5 0 0 1 11 7Z"
    notes = [dot(15.5, 11, 1.5), line(pl(S, [(16.8, 11), (16.8, 4.5), (19, 5.5)], k=0.3)),
             dot(19.5, 18, 1.5), line(seg(20.8, 18, 20.8, 12.5))]
    return [[shell(dome), line(pl(S, [(7, 3.5), (7, 2.5), (14, 2.5)])), line(seg(5, 9.5, 5, 11)), line(seg(9, 9.5, 9, 11)),
             dot(7, 15, 2.25), shell(_bust(S, 7, 19, 5, 22))] + notes]


# ============================================================================ speaking, signalling, caring

@icon("person-speaking", CAT, "A head in profile with the mouth open and three curved sound lines coming out.",
      tags=["speak", "talk", "voice", "say", "speech", "announce"])
def _(S):
    return [shell(profile(S, -2, 1.5, 0.85, 0, "open")), line(arc(14.5, 13.5, 3.5, -40, 40)), line(arc(14.5, 13.5, 6.5, -40, 40))]


@icon("waving-flag", CAT, "A standing person holding a small flag up high and waving it.",
      tags=["flag", "wave flag", "fan", "supporter", "cheer", "parade"])
def _(S):
    flag = ("M14 2.5Q17.5 0.8 21.5 2.5V8.5Q17.5 6.8 14 8.5Z" if S.name == "rounded" else
            "M14 2.5L17.75 1.5L21.5 2.5V8.5L17.75 7.5L14 8.5Z")
    return [shell(flag), line(seg(14, 2.5, 14, 13)), head(7.5, 6.5), line(seg(7.5, 10, 7.5, 15.5)),
            line(pl(S, [(5.5, 21.5), (7.5, 15.5), (9.5, 21.5)])), line(pl(S, [(4, 14), (7.5, 11), (13, 10)]))]


@scene("applauding-audience", "A row of three people seen from behind with a pair of clapping hands above them.",
       tags=["audience", "applause", "clapping", "crowd", "ovation", "show"])
def _(S):
    hands = [shell(_rot_d(ellipse(10.3, 6, 1.6, 3.3), -20, (10.3, 6))), shell(_rot_d(ellipse(13.7, 6, 1.6, 3.3), 20, (13.7, 6)))]
    ticks = [line(seg(6.5, 4.5, 4.5, 3.5)), line(seg(6.5, 8, 4.5, 9)), line(seg(17.5, 4.5, 19.5, 3.5)), line(seg(17.5, 8, 19.5, 9))]
    people = []
    for x in (5, 12, 19):
        people += [dot(x, 15, 2), line(f"M{fmt(x - 3.25)} 21.5A3.25 3.25 0 0 1 {fmt(x + 3.25)} 21.5")]
    return [hands + ticks, people]


@icon("pushing-wheelchair", CAT, "A standing person pushing a seated person in a wheelchair from behind.",
      tags=["wheelchair", "carer", "assist", "mobility", "accessibility", "care"])
def _(S):
    return [head(4, 4.5), line(pl(S, [(4.5, 8), (5, 14.5)])), line(pl(S, [(2.5, 21.5), (5, 14.5), (7.5, 21.5)])),
            line(pl(S, [(4.5, 9), (8.5, 10.5)])),
            line(pl(S, [(8.5, 10.5), (10, 10.5), (11, 15.5), (17, 15.5)])), shell(circle(13, 18.5, 3)),
            head(15, 5, 2), line(pl(S, [(14.5, 8.5), (14, 12.5), (18.5, 12.5), (19.5, 18)]))]


@scene("caring-for-sick", "A person placing a cloth on the forehead of someone lying ill in bed.",
       tags=["caring", "carer", "sick", "nursing", "illness", "look after"])
def _(S):
    return [[mark(rect(3.5, 9, 5, 2, 0.6 if S.name == "rounded" else 0)), line(pl(S, [(9.5, 10), (13.5, 7.5), (17, 7.5)])),
             head(18.5, 3.5)],
            [dot(6, 13.75, 2), shell(pl(S, [(9.5, 17), (9.5, 12.5), (21, 12.5), (21, 17)], k=0.6)),
             line(seg(2.5, 9, 2.5, 21.5)), line(seg(2.5, 17, 21.5, 17)), line(seg(21, 17, 21, 21.5))]]


@icon("measuring-child-height", CAT, "A child standing against a wall height chart with a mark drawn above the head.",
      tags=["height chart", "growth", "measure", "child", "how tall", "growing up"])
def _(S):
    ticks = [line(seg(3, y, 5.5 if i % 2 else 6.5, y)) for i, y in enumerate((4, 8, 12, 16))]
    return [line(seg(3, 2, 3, 21.5)), *ticks, line(seg(9.5, 5.5, 20, 5.5)),
            head(14.5, 10, 2.25), line(seg(14.5, 13.5, 14.5, 17)), line(pl(S, [(12.5, 21.5), (14.5, 17), (16.5, 21.5)])),
            line(pl(S, [(11.5, 17), (12.5, 14), (16.5, 14), (17.5, 17)]))]


@icon("decluttering", CAT, "Items moved from a crowded shelf into a box, shown by a curved arrow.",
      tags=["declutter", "tidy up", "clear out", "organise", "minimalism", "donate"])
def _(S):
    box_ = [shell(rect(12.5, 14, 9, 7.5, min(S.R, 1.5))), line(pl(S, [(12.5, 14), (11, 11.5)])), line(pl(S, [(21.5, 14), (23, 11.5)]))]
    return box_ + [line(seg(2, 9.5, 11, 9.5)), shell(rect(3, 3, 2.5, 4.5, 0.5 if S.name == "rounded" else 0)),
                   shell(rect(7, 4.5, 3, 3, 0.5 if S.name == "rounded" else 0)),
                   line("M6 12.5Q7.5 18 11 18.5" if False else "M5.5 12.5A7 7 0 0 0 10 18.5"),
                   line(pl(S, [(8.2, 19.6), (10, 18.5), (8.9, 16.6)], k=0.3))]


@icon("hanging-picture", CAT, "A picture frame on the wall with a spirit level resting on top of it.",
      tags=["hang picture", "diy", "spirit level", "decorate", "straight", "home improvement"])
def _(S):
    return [shell(rect(4, 9, 16, 12, min(S.R, 2))), detail(pl(S, [(4, 18.5), (9, 13.5), (12.5, 17), (14.5, 15), (20, 20)], k=0.5)),
            shell(rect(3, 2.5, 18, 4, min(S.R, 2))), mark(rect(10.5, 3.5, 3, 2, 1 if S.name == "rounded" else 0))]


# ============================================================================ kitchen and home

@icon("flipping-pancake", CAT, "A frying pan tossed upward with a pancake flipping in the air above it.",
      tags=["pancake", "flip", "toss", "cooking", "breakfast", "pancake day"])
def _(S):
    pan = "M2.5 14.5H14.5L13.5 17.5A1.5 1.5 0 0 1 12 18.5H5A1.5 1.5 0 0 1 3.5 17.5Z"
    cake = _rot_d(ellipse(9, 6.5, 4.5, 1.75), -20, (9, 6.5))
    return [shell(pan, stroke_miterlimit="2"), line(pl(S, [(14.5, 15.5), (21.5, 13)])), shell(cake),
            line(arc(9, 9, 6.5, 190, 230)), line(arc(9, 9, 6.5, 310, 350))]


@scene("tasting-with-spoon", "A face in profile sipping from a spoon held out from a steaming pot.",
       tags=["taste", "tasting", "cooking", "chef", "spoon", "soup"])
def _(S):
    pot = [shell(pl(S, [(12, 15), (22, 15), (21, 21.5), (13, 21.5)], closed=True, k=0.5)), line(seg(11, 15, 23, 15))]
    spoon = [shell(ellipse(16, 11.5, 1.8, 1.2)), line(seg(17.5, 12, 21.5, 14))]
    steam = [line("M21 3.5Q20 5 21 6.5T21 9.5")]
    return [spoon, pot + steam, [shell(profile(S, -1.5, 0, 0.78, 0, "open"))]]


@icon("seasoning-food", CAT, "A salt shaker tilted over a plate with small grains falling.",
      tags=["salt", "season", "seasoning", "shaker", "cooking", "pepper"])
def _(S):
    rb, rc = (0.3, 0.2) if S.name == "line" else (2.2, 1.2)
    body = _rot_d(rect(12.5, 5.5, 6, 8, rb), 140, (15.5, 8))
    capd = _rot_d(rect(13, 2, 5, 3.5, rc), 140, (15.5, 8))
    plate = "M2.5 17.5H21.5A9.5 3.5 0 0 1 2.5 17.5Z"
    return [shell(body), shell(capd), dot(9, 12, 0.9), dot(11.5, 14, 0.9), dot(7.5, 15, 0.9), shell(plate)]


@icon("lighting-candle", CAT, "A lit match held to the wick of a pillar candle.",
      tags=["candle", "light", "match", "flame", "relax", "light a candle"])
def _(S):
    return [shell(rect(4.5, 12.5, 8, 9, min(S.R, 1.5))), line(seg(8.5, 10, 8.5, 12.5)),
            shell(drop_d(10.5, 8, 5, 3.5), stroke_miterlimit="2"), line(seg(13.5, 9.5, 20.5, 17)), dot(13, 9, 1.5)]


@scene("opening-window", "A window with its sash swung open and breeze lines blowing in.",
       tags=["open window", "fresh air", "ventilate", "breeze", "airing", "window"])
def _(S):
    sash = pl(S, [(9.5, 3), (3, 5.5), (3, 18.5), (9.5, 21)], closed=True, k=0.5)
    return [[shell(sash), detail(seg(6.25, 4.3, 6.25, 19.7)), detail(seg(3, 12, 9.5, 12))],
            [shell(rect(9.5, 3, 12, 18, min(S.R, 2))), detail("M12.5 9Q14.25 7.5 16 9T19.5 9"), detail("M12.5 15Q14.25 13.5 16 15T19.5 15")]]

@scene("drawing-curtains", "A pair of curtains pulled apart on a rail to let the sun shine in.",
       tags=["open curtains", "morning", "wake up", "sunlight", "daylight", "window"])
def _(S):
    left = "M2.5 4H7Q5.5 12 6.5 20H2.5Z"
    right = "M21.5 4H17Q18.5 12 17.5 20H21.5Z"
    rays = [line(seg(*polar(12, 11.5, 3.6, a), *polar(12, 11.5, 5.2, a))) for a in (-90, -45, -135, 45, 135, 90)]
    return [[shell(left, stroke_miterlimit="2"), shell(right, stroke_miterlimit="2"), line(seg(2, 2, 22, 2)),
             dot(12, 11.5, 2)] + rays]


@scene("collecting-mail", "Envelopes being pulled out of a post-mounted mailbox with its door open.",
       tags=["mail", "post", "letters", "mailbox", "check mail", "delivery"])
def _(S):
    envelope = [shell(rect(2.5, 4, 7, 5, min(S.R, 1))), detail(pl(S, [(2.5, 4), (6, 6.8), (9.5, 4)], k=0.3))]
    box_ = [shell("M8.5 14V9A3.5 3.5 0 0 1 12 5.5H18A3.5 3.5 0 0 1 21.5 9V14Z"), line(seg(16, 14, 16, 21.5)),
            line(seg(8.5, 14.5, 5, 17.5))]
    return [envelope, box_]


@scene("drop-cover-hold", "A person crouched under a table holding one leg, with shaking lines around the table.",
       tags=["earthquake", "drop cover hold", "safety drill", "take cover", "emergency", "shelter"])
def _(S):
    table = [line(seg(2, 8.5, 22, 8.5)), line(seg(4, 8.5, 4, 21.5)), line(seg(20, 8.5, 20, 21.5))]
    shake = [line(seg(3, 3, 4.5, 5.5)), line(seg(6, 3, 7.5, 5.5)), line(seg(21, 3, 19.5, 5.5)), line(seg(18, 3, 16.5, 5.5))]
    fig = [head(9, 15.5, 2), line("M11 12.5Q15.5 12 16 17.5L12.5 21.5" if S.name == "rounded" else pl(S, [(11, 12.5), (15.5, 13), (16, 17.5), (12.5, 21.5)])),
           line(seg(12.5, 13.5, 18.5, 13.5))]
    return [fig, table + shake]


@icon("stop-drop-and-roll", CAT, "A person lying on the ground rolling sideways, with a curved arrow and small flames.",
      tags=["stop drop and roll", "fire safety", "clothes on fire", "emergency", "burn", "safety"])
def _(S):
    return [head(4.5, 15.5), line(seg(7.5, 16, 20.5, 16)), line(pl(S, [(11, 16), (13, 13)])), line(seg(2, 20, 22, 20)),
            line(arc(10, 13, 5.5, 200, 330)), line(pl(S, [(12.2, 7.4), (14.8, 10.2), (15.5, 6.5)], k=0.3)), shell(flame_d(19.5, 9.5, 1.0))]


def flame_d(cx, by, k=1.0):
    """Flame with a side lick; (cx, by) is the centre of its round base."""
    pts = [("M", (0, -7)), ("C", (2, -4.5), (3, -3), (3, -1)), ("A", 3, (-3, -1)), ("C", (-3, -2.5), (-2.2, -3.6), (-1.5, -4.3)),
           ("C", (-1.2, -3), (-0.8, -2.6), (-0.2, -2.6)), ("C", (-0.6, -4), (-0.6, -5.5), (0, -7))]
    out = []
    for c in pts:
        if c[0] == "M":
            out.append(f"M{fmt(cx + k * c[1][0])} {fmt(by + k * c[1][1])}")
        elif c[0] == "C":
            out.append("C" + " ".join(f"{fmt(cx + k * p[0])} {fmt(by + k * p[1])}" for p in c[1:]))
        else:
            out.append(f"A{fmt(3 * k)} {fmt(3 * k)} 0 0 1 {fmt(cx + k * c[2][0])} {fmt(by + k * c[2][1])}")
    return "".join(out) + "Z"


@icon("safe-lifting", CAT, "A person squatting with a straight back and bent knees, lifting a box close to the body.",
      tags=["lifting", "manual handling", "safe lifting", "back care", "workplace safety", "carry box"])
def _(S):
    return [head(7.5, 4.5), line(pl(S, [(8, 8), (8.5, 14.5), (13.5, 15.5), (12.5, 21.5)])), line(pl(S, [(8, 9), (12, 12)])),
            shell(rect(13, 8.5, 8, 7, min(S.R, 1.5))), line(seg(2, 21.5, 22, 21.5))]


@scene("fanning-oneself", "A face with a folding hand fan held beside it and a drop of sweat.",
       tags=["hot", "heat", "fan", "summer", "heatwave", "cool down"])
def _(S):
    c, R = (15.5, 18), 7
    p0, p1 = polar(*c, R, -115), polar(*c, R, -25)
    fan = f"M{fmt(c[0])} {fmt(c[1])}L{fmt(p0[0])} {fmt(p0[1])}A{R} {R} 0 0 1 {fmt(p1[0])} {fmt(p1[1])}Z"
    ribs = [detail(seg(*c, *polar(*c, R, a))) for a in (-85, -55)]
    face = [shell(circle(8.5, 13, 6)), dot(6.5, 12.5, 1), dot(10.5, 12.5, 1), detail("M6.5 16A2 2 0 0 0 10.5 16")]
    return [[shell(fan, stroke_miterlimit="2")] + ribs, face, [shell(drop_d(3.5, 5.5, 3.5, 2.6), stroke_miterlimit="2")]]


@icon("picking-up-litter", CAT, "A person bending to drop a can into a rubbish bag held open.",
      tags=["litter", "clean up", "pick up trash", "volunteer", "environment", "rubbish"])
def _(S):
    bag = "M15 12.5H21L22 20A1.5 1.5 0 0 1 20.5 21.5H15.5A1.5 1.5 0 0 1 14 20Z"
    return [head(12.5, 5.5), line(pl(S, [(10, 7.5), (5, 11.5)])), line(pl(S, [(5, 11.5), (4, 21.5)])), line(pl(S, [(5, 11.5), (8, 21.5)])),
            line(pl(S, [(9.5, 8.5), (10.5, 13)])), shell(rect(9.5, 14.5, 2.5, 3.5, 0.5 if S.name == "rounded" else 0)),
            line(pl(S, [(9.5, 8), (15.5, 10.5)])), shell(bag)]


@icon("turning-off-tap", CAT, "A tap with a curved arrow turning its handle closed and one last drop falling.",
      tags=["turn off tap", "save water", "faucet", "water saving", "close tap", "conserve"])
def _(S):
    spout = pl(S, [(2, 10), (14, 10), (16.5, 12.5), (16.5, 15)], k=1.0)
    return [line(spout), line(seg(9, 10, 9, 7)), line(seg(6, 6.5, 12, 6.5)),
            line(arc(9, 6.5, 5.5, 200, 320)), line(pl(S, [(13, 1.8), (13.2, 3.3), (11.8, 4.2)], k=0.2)),
            shell(drop_d(16.5, 20.5, 3.5, 2.6), stroke_miterlimit="2")]


@icon("carrying-water-buckets", CAT, "A person with a pole across the shoulders and a bucket hanging from each end.",
      tags=["carry water", "buckets", "yoke", "water collection", "chores", "village"])
def _(S):
    parts = [head(12, 4.5), line(seg(2, 8.5, 22, 8.5)), line(seg(12, 11, 12, 15.5)), line(pl(S, [(9.5, 21.5), (12, 15.5), (14.5, 21.5)]))]
    for mx in (False, True):
        X = (lambda x: 24 - x) if mx else (lambda x: x)
        parts += [line(seg(X(4.5), 8.5, X(4.5), 12)), shell(pl(S, [(X(2), 12), (X(7), 12), (X(6.5), 18.5), (X(2.5), 18.5)], closed=True, k=0.4))]
    return parts


def _runner(S, dx, dy, k, reach=False):
    t = lambda p: (dx + p[0] * k, dy + p[1] * k)
    arm = [(6.5, 11.5), (9.5, 9), (13.5, 9), (16, 12), (19, 12.5)] if not reach else [(6.5, 11.5), (9.5, 9), (13.5, 9), (20, 8)]
    return [head(*t((15.5, 4.5)), 2.25 * k), line(pl(S, [t(p) for p in arm])), line(seg(*t((13.5, 9)), *t((11, 14.5)))),
            line(pl(S, [t(p) for p in [(4.5, 17.5), (8, 18.5), (11, 14.5), (14.5, 17), (13, 21)]]))]


@icon("playing-tag", CAT, "One running person reaching out to touch the back of another runner ahead.",
      tags=["tag", "tig", "chase", "playground", "kids game", "you're it"])
def _(S):
    return _runner(S, -1.3, 3, 0.74, reach=True) + _runner(S, 8.3, 3, 0.74)


@icon("tug-of-war", CAT, "Two people leaning back in opposite directions pulling a rope with a marker at its centre.",
      tags=["tug of war", "pull", "rope", "contest", "teamwork", "field day"])
def _(S):
    parts = [line(seg(2, 12, 22, 12)), solid(pl(S, [(10.5, 13), (13.5, 13), (12, 16)], closed=True))]
    for mx in (False, True):
        X = (lambda x: 24 - x) if mx else (lambda x: x)
        parts += [head(X(3), 5.5), line(pl(S, [(X(4), 8.5), (X(7), 16), (X(9.5), 21.5)])), line(seg(X(7), 16, X(5), 21.5)),
                  line(pl(S, [(X(4.5), 10), (X(7.5), 12)]))]
    return parts


@scene("blowing-dandelion", "A face in profile blowing at a round dandelion seed head with seeds drifting away.",
       tags=["dandelion", "make a wish", "wish", "spring", "blow", "seeds"])
def _(S):
    fluff = [line(seg(*polar(18, 9, 3.2, a), *polar(18, 9, 4.6, a))) for a in (-135, -90, -45, 0, 45, 135, 180)]
    return [[dot(18, 9, 2), line(seg(18, 12, 18, 21.5))] + fluff + [dot(21.5, 3, 0.9), dot(14.5, 2.5, 0.9)],
            [shell(profile(S, -1.5, 4.5, 0.72, 0, "open"))]]


@icon("flipping-coin", CAT, "A hand with the thumb just flicked up and a coin spinning in the air above it.",
      tags=["coin toss", "flip a coin", "heads or tails", "decide", "chance", "luck"])
def _(S):
    rows = [cap(8, y, 12.5, y, 2.6) for y in (15.3, 17.9, 20.5)]
    fist = outline(box(4, 13.5, 7, 9, wr(S)), *rows, cap(8, 13.5, 14.5, 10.5, 2.6))
    coin = _rot_d(ellipse(15, 5, 3.5, 1.8), -20, (15, 5))
    return [fist, detail(seg(10.5, 16.6, 13.8, 16.6)), detail(seg(10.5, 19.2, 13.8, 19.2)),
            shell(coin), line(arc(15, 5, 6, 150, 200)), line(arc(15, 5, 6, 330, 20))]


@icon("breaking-bread", CAT, "A round loaf torn into two halves with a few crumbs between them.",
      tags=["break bread", "share", "sharing food", "meal together", "bread", "hospitality"])
def _(S):
    loaf = P(ellipse(12, 13, 9.5, 6.5))
    zz = [(12, 4), (13, 7.5), (11.2, 10.5), (12.8, 13.5), (11.2, 16.5), (12.5, 22)]
    lp = P(poly([(0, 0)] + zz + [(0, 24)], closed=True))
    from dsl import transform_path
    tl = path_to_d(transform_path(I(loaf, lp), (1, 0, 0, 1, -1.5, 0)))
    tr = path_to_d(transform_path(D(loaf, lp), (1, 0, 0, 1, 1.5, 0)))
    return [shell(tl, stroke_miterlimit="2"), shell(tr, stroke_miterlimit="2"), detail(seg(4.5, 11, 7.5, 9)), detail(seg(16.5, 9, 19.5, 11)),
            dot(12, 4, 0.9)]


@icon("standing-up-from-chair", CAT, "A person rising from a chair with knees half straight and hands pushing on the armrest.",
      tags=["stand up", "get up", "rise", "sit to stand", "mobility", "chair"])
def _(S):
    chair = [line(seg(3, 5, 3, 21.5)), line(seg(3, 14.5, 10, 14.5)), line(seg(10, 14.5, 10, 21.5)), line(seg(3, 10.5, 8.5, 10.5))]
    fig = [head(14, 4.5), line(pl(S, [(13, 8), (11.5, 13), (15.5, 15.5), (15, 21.5)])), line(pl(S, [(12.8, 9), (9, 10.5)]))]
    up = [line(seg(20, 12, 20, 3.5)), line(pl(S, [(18, 5.5), (20, 3.5), (22, 5.5)], k=0.3))]
    return chair + fig + up
