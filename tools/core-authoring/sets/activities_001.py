"""TypeIcon Core: activities and actions (batch 001): hand gestures, body language and poses.

Hands are regions: fingers are capsules (3.4 wide, the pitch used by the gestures set) unioned with a palm and
outlined as one shell, so Filled turns them solid and knocks out the finger separations. Line keeps wrist and
palm corners square, Rounded softens them.

Faces are a circle with two eyes (crisp bars in Line, soft ovals in Rounded). Whole-body poses are stick figures
in the style of the people and sports sets: a solid head (r 2.25) over 2 px limbs, faceted in Line and filleted
in Rounded.

Where a hand overlaps a face or body, the icon is drawn in layers (front first) and what lies behind is cut away
around the front silhouette with a gap in every style.
"""
from __future__ import annotations

import math

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path

from dsl import LINE, Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar  # noqa: F401

CAT = "activities"
FW = 3.4  # finger width


# --------------------------------------------------------------------------- region helpers

def cap(x0, y0, x1, y1, w=FW):
    """Finger or limb: a capsule along a segment."""
    return ST(seg(x0, y0, x1, y1), w, "round", "round")


def capd(d, w=FW):
    """Capsule along any open path (a curled finger)."""
    return ST(d, w, "round", "round")


def box(x, y, w, h, r=0.0):
    return P(rect(x, y, w, h, r))


def disc(cx, cy, r):
    return P(circle(cx, cy, r))


def outline(*regions, **attrs):
    return shell(path_to_d(U(*regions)), **attrs)


def wr(S):
    """Wrist / palm corner radius: square for Line, soft for Rounded."""
    return 0.5 if S.name == "line" else 2.5


def pick(S, a, b):
    return a if S.name == "line" else b


def mitten(x0, y0, x1, y1, w=5.0):
    """Flat hand seen edge-on: straight wrist at (x0, y0), rounded fingertips at (x1, y1)."""
    return U(ST(seg(x0, y0, x1, y1), w, "butt", "miter"), P(circle(x1, y1, w / 2)))


# --------------------------------------------------------------------------- transforms

def _xd(d, m):
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def xparts(parts, m):
    return [Part(p.kind, _xd(p.d, m), dict(p.attrs)) for p in parts]


def mirror_x(parts, cx=12.0):
    return xparts(parts, (-1, 0, 0, 1, 2 * cx, 0))


def scale_at(parts, k, tx, ty):
    """Scale by k about the origin, then shift."""
    return xparts(parts, (k, 0, 0, k, tx, ty))


# --------------------------------------------------------------------------- layering

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


def _paint(parts, S):
    regs = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        else:
            regs.append(ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4))))
    return U(*regs)


def _grow(region, g):
    if g <= 0:
        return region
    return U(region, ST(path_to_d(region), 2 * g, "round", "round"))


def _stroke_layers(S, layers, gap):
    out = list(layers[0])
    cover = _grow(_sil(layers[0], S), gap)
    for layer in layers[1:]:
        if not layer:
            continue
        vis = D(_paint(layer, S), cover)
        if abs(vis.area) > 0.01:
            out.append(solid(path_to_d(vis)))
        cover = U(cover, _grow(_sil(layer, S), gap))
    return out


def _filled_layers(layers, gap):
    result = filled_region(layers[0])
    cover = _grow(result, gap)
    for layer in layers[1:]:
        if not layer:
            continue
        f = filled_region(layer)
        result = U(result, D(f, cover))
        cover = U(cover, _grow(f, gap))
    return result


def fig(name, desc, tags, aliases=(), gap=1.25):
    """Register an icon drawn as layers: fn(S) -> [front layer, layer behind, ...]."""
    def deco(fn):
        icon(name, CAT, desc, tags=tags, aliases=aliases,
             filled=lambda: _filled_layers(fn(LINE), gap))(lambda S: _stroke_layers(S, fn(S), gap))
        return fn
    return deco


# --------------------------------------------------------------------------- shared shapes

def eye(S, x, y, h=2.8):
    """Eye mark: crisp bar in Line, oval in Rounded; knocked out of a Filled face."""
    return Part("dot", rect(x - 1, y - h / 2, 2, h) if S.name == "line" else ellipse(x, y, 1.1, h / 2))


def face(S, cx=12.0, cy=12.0, r=8.0, ey=None, dx=3.0, eyes=True):
    ey = cy - 1.5 if ey is None else ey
    parts = [shell(circle(cx, cy, r))]
    if eyes:
        parts += [eye(S, cx - dx, ey), eye(S, cx + dx, ey)]
    return parts


def head(x, y, r=2.25):
    return dot(x, y, r)


def limb(S, pts):
    return line(poly(pts, r=S.r))


def heart_d(cx, cy, w):
    """Heart of width w centred on (cx, cy)."""
    k = w / 16.0
    return _xd("M12 20L4.4 12.6A4.6 4.6 0 0 1 11 6.3L12 7.3L13 6.3A4.6 4.6 0 0 1 19.6 12.6Z",
               (k, 0, 0, k, cx - 12 * k, cy - 13 * k))


def palm_up(S, dx=0.0, dy=0.0):
    """A hand held out palm up from the left, fingertips curling up on the right."""
    wrist = box(2.5 + dx, 15 + dy, 7, 6.5, wr(S))
    fingers = [cap(8 + dx, 19.2 + dy, 17.5 + dx, 19.2 + dy, 3.2), cap(17.5 + dx, 19.2 + dy, 19.8 + dx, 16.8 + dy, 3.2)]
    thumb = cap(8 + dx, 16.6 + dy, 11.3 + dx, 14.4 + dy, 2.8)
    return [outline(wrist, *fingers, thumb)]


def point_up(S):
    """Back of a hand with the index finger raised."""
    idx = cap(8.5, 13, 8.5, 4.6)
    fist = box(6.8, 11, 11.6, 10, wr(S))
    knuck = [cap(12, 12.6, 12, 12.6), cap(15.4, 12.8, 15.4, 12.8)]
    thumb = cap(7.2, 17.5, 4.2, 14)
    return [outline(idx, fist, *knuck, thumb), detail(seg(7.8, 17.2, 12, 17.2))]


def mirror_x_regions(pair):
    rows, body = pair
    m = lambda r: P(_xd(path_to_d(r), (-1, 0, 0, 1, 24, 0)))  # noqa: E731
    return [m(r) for r in rows], m(body)


def touch_hand(S, tx=3.5, k=0.8):
    return xparts(point_up(S), (k, 0, 0, k, tx, 21 - 21 * k))


# ============================================================================ hand signs

@icon("i-love-you-hand", CAT, "A raised hand with the thumb, index and little finger out and the middle two folded; I love you in sign.",
      tags=["i love you", "ily", "sign language", "love", "hand sign", "asl"])
def _(S):
    palm = box(6.5, 12, 13, 9, wr(S))
    index = cap(7.9, 13, 7.6, 4.8)
    pinky = cap(18.1, 13, 18.4, 6.5)
    knuck = [cap(11.3, 12.6, 11.3, 12.6), cap(14.7, 12.6, 14.7, 12.6)]
    thumb = cap(7.8, 17.8, 3.6, 14.6)
    return [outline(palm, index, pinky, *knuck, thumb), detail(seg(9.8, 15, 16.2, 15))]


@fig("shushing", "A face with an index finger held upright against the lips; be quiet.",
     tags=["shush", "quiet", "silence", "hush", "secret", "be quiet"], aliases=["shush"])
def _(S):
    hand = [outline(cap(12, 18, 12, 10.5, 3.2), box(8, 17.5, 8, 4.5, wr(S))), detail(seg(8, 19.5, 11, 19.5))]
    return [hand, face(S, 12, 10.5, 8.5, ey=8, dx=4) + [detail(seg(7.5, 13.5, 16.5, 13.5))]]


@fig("holding-hands", "Two people standing side by side holding hands.",
     tags=["holding hands", "together", "friends", "couple", "partners", "companionship"])
def _(S):
    return [[head(6.5, 4.5), head(17.5, 4.5),
             limb(S, [(3, 14.5), (5, 9.5), (8, 9.5), (12, 13.5), (16, 9.5), (19, 9.5), (21, 14.5)]),
             line(seg(6.5, 9.5, 6.5, 14.5)), line(seg(17.5, 9.5, 17.5, 14.5)),
             limb(S, [(4, 21), (6.5, 14.5), (9, 21)]), limb(S, [(15, 21), (17.5, 14.5), (20, 21)])]]


@icon("finger-snap", CAT, "A hand with the thumb and middle finger pressed together and sparks at the fingertips; a snap.",
      tags=["snap", "click fingers", "instantly", "just like that", "rhythm", "gesture"])
def _(S):
    fist = box(4, 13, 8.5, 8.5, wr(S))
    rows = [cap(8, y, 13.5, y, 3.0) for y in (15, 18.3)]
    thumb = cap(6.5, 13.5, 12.5, 8, 3.2)
    mid = cap(10, 14.5, 13, 8.3, 3.0)
    sparks = [line(seg(*polar(13.5, 7, 3.2, a), *polar(13.5, 7, 6, a))) for a in (-80, -30, 20)]
    return [outline(fist, *rows, thumb, mid), detail(seg(10.5, 16.65, 13.5, 16.65))] + sparks


@icon("offering-hand", CAT, "An open hand held out palm up with a small ball resting on it; offering or giving.",
      tags=["offer", "give", "present", "hand out", "share", "provide"])
def _(S):
    return palm_up(S) + [shell(circle(13, 9.5, 3.5))]


@fig("timeout-gesture", "Two flat hands forming a T; a call for a time out or a break.",
     tags=["time out", "timeout", "break", "pause", "stop", "referee"], aliases=["time-out"], gap=1.0)
def _(S):
    top = [outline(mitten(2.5, 6, 19.5, 6, 5.4)), detail(seg(4.5, 7.5, 11, 7.5))]
    stem = [outline(mitten(12, 21.5, 12, 11, 5.4))]
    return [top, stem]


# ============================================================================ body language (busts and standing figures)

def bust(S, cx=12.0, hy=7.0, hr=3.5, top=13.5, hw=7.0, bottom=21.0):
    """Head over open-bottom shoulders (the people set's user bust). Line has squarer shoulders."""
    r = min(hw - (1.0 if S.name != "line" else 2.0), bottom - top)
    x0, x1 = cx - hw, cx + hw
    d = (f"M{fmt(x0)} {fmt(bottom)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + r)} {fmt(top)}"
         f"H{fmt(x1 - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(bottom)}")
    return [shell(circle(cx, hy, hr)), shell(d)]


@fig("arms-crossed", "A person with both forearms folded across the chest; waiting or unimpressed.",
     tags=["arms crossed", "folded arms", "waiting", "impatient", "unimpressed", "defensive"], aliases=["folded-arms"])
def _(S):
    band = [shell(rect(3.5, 14.5, 17, 5, min(S.R, 2.5))), detail(seg(7, 17, 17, 17))]
    return [band, bust(S, hy=6.5, top=12.5)]


@fig("hands-on-hips", "A standing figure with both elbows out and the hands resting on the hips.",
     tags=["hands on hips", "akimbo", "confident", "impatient", "posture", "stance"], aliases=["akimbo"])
def _(S):
    return [[head(12, 4.5),
             limb(S, [(10, 14.5), (5.5, 12), (8.5, 9.5), (15.5, 9.5), (18.5, 12), (14, 14.5)]),
             line(seg(12, 9.5, 12, 14.5)),
             limb(S, [(8.5, 21), (12, 14.5), (15.5, 21)])]]


@fig("shrug", "A figure with raised shoulders and both forearms turned out, palms up; I don't know.",
     tags=["shrug", "dunno", "no idea", "whatever", "unsure", "who knows"], aliases=["dunno"])
def _(S):
    return [[head(12, 5.5),
             limb(S, [(3, 8.5), (6, 13), (8.5, 9.5), (15.5, 9.5), (18, 13), (21, 8.5)]),
             line(seg(12, 9.5, 12, 15)),
             limb(S, [(9, 21), (12, 15), (15, 21)])]]


@fig("salute", "A figure raising a flat hand to the brow in a salute.",
     tags=["salute", "respect", "military", "honor", "yes sir", "attention"], aliases=["saluting"])
def _(S):
    return [[head(10.5, 5),
             limb(S, [(4.5, 14.5), (7, 9.5), (14, 9.5), (18.5, 9), (14.2, 3.8)]),
             line(seg(10.5, 9.5, 10.5, 14.5)),
             limb(S, [(7.5, 21), (10.5, 14.5), (13.5, 21)])]]


@fig("bowing-person", "A standing figure bent forward at the waist in a polite bow.",
     tags=["bow", "bowing", "respect", "thank you", "apology", "greeting"])
def _(S):
    return [[head(6, 5),
             line(seg(15.5, 12.5, 9, 7)),
             line(seg(10.5, 8.3, 10.5, 14.5)),
             limb(S, [(15.5, 12.5), (15.5, 21)])]]


@fig("curtsy", "A figure in a flared skirt holding its edges out to the sides; a curtsy.",
     tags=["curtsy", "curtsey", "bow", "courtesy", "ballet", "polite greeting"], aliases=["curtsey"])
def _(S):
    skirt = poly([(10, 10.5), (14, 10.5), (18.5, 17), (5.5, 17)], closed=True, r=S.r * 0.6)
    return [[head(12, 4.5), shell(skirt),
             limb(S, [(4, 14.5), (9.5, 9)]), limb(S, [(20, 14.5), (14.5, 9)]),
             limb(S, [(10, 17), (10, 21.5)]), limb(S, [(14, 17), (16, 21.5)])]]


def fist_side(S, x=3.0, y=7.0, w=7.5, h=10.5):
    """Side view of a fist: knuckle rows to the right, thumb folded across the top."""
    rh = (h - 3.2) / 3
    rows = [cap(x + 2, y + 3.2 + rh * (k + 0.5), x + w - rh / 2, y + 3.2 + rh * (k + 0.5), rh) for k in range(3)]
    body = box(x, y, w - 1.5, h, 1.5 if S.name == "line" else 2.5)
    thumb = cap(x + 1.5, y + 1.6, x + w - 1.8, y + 1.6, 3.2)
    seps = [detail(seg(x + w - 3.2, y + 3.2 + rh * k, x + w, y + 3.2 + rh * k)) for k in (1, 2)]
    return [outline(body, thumb, *rows), detail(seg(x + 1.5, y + 3.2, x + w - 1, y + 3.2))] + seps


@fig("fist-palm-salute", "A closed fist pressed into an open flat palm; a traditional greeting of respect.",
     tags=["fist and palm", "baoquan", "kung fu salute", "respect", "greeting", "martial arts"], aliases=["baoquan"], gap=1.0)
def _(S):
    palm = [outline(mitten(15.5, 21.5, 15.5, 6, 6), cap(12.8, 16, 11, 12, 2.8))]
    return [palm, fist_side(S, 3, 8, 9.5, 11)]


# ============================================================================ faces and hands

@fig("nodding-yes", "A smiling face with motion arcs above and below; nodding yes.",
     tags=["nod", "yes", "agree", "approve", "okay", "consent"], aliases=["nod"])
def _(S):
    return [face(S, 12, 12, 6.5, ey=11, dx=2.6) + [detail(arc(12, 12.5, 3, 30, 150))],
            [line(arc(12, 12, 9.5, 245, 295)), line(arc(12, 12, 9.5, 65, 115))]]


@fig("shaking-head-no", "A face with motion arcs on both sides; shaking the head no.",
     tags=["shake head", "no", "disagree", "refuse", "decline", "nope"], aliases=["head-shake"])
def _(S):
    return [face(S, 12, 12, 6.5, ey=11, dx=2.6) + [detail(seg(10, 15, 14, 15))],
            [line(arc(12, 12, 9.5, 155, 205)), line(arc(12, 12, 9.5, -25, 25))]]


@icon("wagging-finger", CAT, "A raised index finger with motion arcs on both sides; no, no, no.",
      tags=["wag finger", "no no", "tut tut", "warning", "scold", "not allowed"], aliases=["finger-wag"])
def _(S):
    hand = xparts(point_up(S), (1, 0, 0, 1, 3.5, 0))
    return hand + [line(arc(12, 10, 7.5, 200, 232)), line(arc(12, 10, 7.5, 308, 340))]


@fig("hand-over-mouth", "A wide-eyed face with one hand covering the mouth; shock or a slip of the tongue.",
     tags=["oops", "gasp", "shock", "surprised", "embarrassed", "speechless"])
def _(S):
    hand = [outline(mitten(21.5, 16.5, 7.5, 15.5, 5.6))]
    eyes = [detail(pick(S, rect(x - 1.4, 7.1, 2.8, 2.8), circle(x, 8.5, 1.4))) for x in (8.8, 15.2)]
    return [hand, [shell(circle(12, 11, 8.5))] + eyes]


@icon("counting-on-fingers", CAT, "A raised hand with three fingers up and a dot above each; counting.",
      tags=["count", "three", "number", "fingers", "tally", "math"])
def _(S):
    palm = box(5.5, 13, 13, 8.5, wr(S))
    ups = [cap(x, 14, x, 8) for x in (7.2, 10.6, 14)]
    pinky = cap(17.2, 13.8, 17.2, 13.8)
    thumb = cap(6.5, 18, 12.5, 17)
    return [outline(palm, *ups, pinky, thumb), detail(seg(7, 17.2, 12.5, 17.2)), dot(7.2, 3.5, 1.3), dot(10.6, 3.5, 1.3), dot(14, 3.5, 1.3)]


# ============================================================================ arm poses

@fig("arms-x-sign", "A person with both forearms crossed in front of the chest in a large X; no or stop.",
     tags=["x sign", "no", "stop", "wrong", "not allowed", "refuse"])
def _(S):
    return [[line(seg(4.5, 11, 18.5, 21.5)), line(seg(19.5, 11, 5.5, 21.5))], bust(S, hy=5.5, hr=3, top=12)]


@fig("open-arms", "A standing figure with both arms spread wide and slightly raised; welcome.",
     tags=["welcome", "hug", "open arms", "embrace", "greeting", "come here"])
def _(S):
    return [[head(12, 4.5),
             limb(S, [(2.5, 7), (8, 10), (16, 10), (21.5, 7)]),
             line(seg(12, 10, 12, 15)),
             limb(S, [(9, 21), (12, 15), (15, 21)])]]


@fig("surrender-pose", "A standing figure with both arms raised straight up; hands up or surrender.",
     tags=["hands up", "surrender", "give up", "don't shoot", "arrest", "raise hands"], aliases=["hands-up"])
def _(S):
    return [[head(12, 6),
             limb(S, [(6.5, 2.5), (8, 10.5), (16, 10.5), (17.5, 2.5)]),
             line(seg(12, 10.5, 12, 15.5)),
             limb(S, [(9, 21.5), (12, 15.5), (15, 21.5)])]]


@fig("blowing-kiss", "A face blowing a kiss with a small heart floating away.",
     tags=["blow kiss", "kiss", "love", "goodbye", "mwah", "affection"], aliases=["air-kiss"])
def _(S):
    return [[shell(heart_d(18, 6.5, 7), stroke_miterlimit="2")],
            face(S, 10, 13.5, 7.5, ey=12, dx=3) + [detail(circle(12.5, 16.5, 1.2))]]


# ============================================================================ hands with devices

@fig("holding-phone", "A hand gripping an upright smartphone with the thumb on the screen.",
     tags=["phone in hand", "smartphone", "mobile", "scrolling", "using phone", "handheld"], gap=1.0)
def _(S):
    hand = [outline(box(3.5, 13.5, 9, 8, wr(S)), cap(5.5, 15, 10.8, 10.5, 3.2),
                    *[cap(10, y, 17.5, y, 2.8) for y in (14.5, 17.4)])]
    phone = [shell(rect(8.5, 2.5, 10, 17, min(S.R, 2.5))), detail(seg(12, 5, 15, 5))]
    return [hand, phone]


# ============================================================================ touch gestures

def _tip(k=0.8, tx=3.5):
    return tx + 8.5 * k, 21 - 21 * k + 4.6 * k


@icon("double-tap-gesture", CAT, "A pointing finger with a tap ripple and the number 2; double tap.",
      tags=["double tap", "tap twice", "touch", "gesture", "touchscreen", "like"], aliases=["double-tap"])
def _(S):
    hx, ty = _tip()
    two = pick(S, "M15.5 4.5A2.5 2.5 0 0 1 20.5 4.5C20.5 6.5 15.5 8 15.5 10.5H21",
               "M15.5 4.5A2.5 2.5 0 0 1 20.5 4.5C20.5 6.5 15.5 8 15.5 10.5H21")
    return touch_hand(S) + [line(arc(hx, ty, 4, 205, 335)), line(two)]


@icon("long-press-gesture", CAT, "A pointing finger pressing down inside a partial progress ring; press and hold.",
      tags=["long press", "press and hold", "hold", "touch", "gesture", "force touch"], aliases=["press-and-hold"])
def _(S):
    hx, ty = _tip()
    return touch_hand(S) + [line(arc(hx, ty, 5.5, 160, 380))]


@icon("two-finger-scroll", CAT, "A hand with two fingers extended beside a double-headed vertical arrow; two finger scroll.",
      tags=["two finger scroll", "scroll", "trackpad", "touchpad", "swipe", "gesture"])
def _(S):
    fingers = [cap(6.5, 13, 6.5, 5), cap(9.9, 13, 9.9, 5)]
    fist = box(4.8, 11, 10.6, 10, wr(S))
    knuck = cap(13.3, 12.6, 13.3, 12.6)
    thumb = cap(5.2, 17.5, 2.9, 14.5, 3)
    return [outline(*fingers, fist, knuck, thumb), detail(seg(8.2, 7.5, 8.2, 12.5)), detail(seg(5.8, 17.2, 10, 17.2)),
            line(seg(19.5, 3.5, 19.5, 20.5)), line(poly([(17, 6), (19.5, 3.5), (22, 6)], r=S.r * 0.4)),
            line(poly([(17, 18), (19.5, 20.5), (22, 18)], r=S.r * 0.4))]


@icon("shake-phone-gesture", CAT, "An upright smartphone with motion arcs on both sides; shake the phone.",
      tags=["shake", "shake phone", "motion", "undo", "accelerometer", "gesture"])
def _(S):
    return [shell(rect(8, 3, 8, 18, min(S.R, 2))), detail(seg(11, 18, 13, 18)),
            line(arc(12, 12, 7, 150, 210)), line(arc(12, 12, 10, 155, 205)),
            line(arc(12, 12, 7, -30, 30)), line(arc(12, 12, 10, -25, 25))]


# ============================================================================ signing and signalling

@icon("fingerspelling", CAT, "A closed hand shaping a letter beside a capital A; spelling words in sign language.",
      tags=["fingerspelling", "sign language", "manual alphabet", "asl", "deaf", "letters"])
def _(S):
    knuck = [cap(x, 9.5, x, 9.5, 3.0) for x in (4.5, 7.5, 10.5)]
    fist = box(3, 9.5, 9, 9, wr(S))
    thumb = cap(4, 11, 4, 15, 3)
    wrist = box(4.5, 18, 6, 3.5, pick(S, 0.5, 1))
    return [outline(*knuck, fist, thumb, wrist), detail(seg(6.2, 12.5, 12, 12.5)),
            line(poly([(13.5, 20.5), (17.5, 4), (21.5, 20.5)], r=S.r * 0.4)), line(seg(15, 14.5, 20, 14.5))]


@icon("lip-reading", CAT, "An eye above a pair of lips linked by a dotted sight line; reading lips.",
      tags=["lip reading", "lipreading", "speechreading", "deaf", "hard of hearing", "watch lips"], aliases=["speechreading"])
def _(S):
    eye_d = pick(S, "M3 7L7 3.8H17L21 7L17 10.2H7Z", "M3 7C5.5 4.3 8.5 3 12 3C15.5 3 18.5 4.3 21 7C18.5 9.7 15.5 11 12 11C8.5 11 5.5 9.7 3 7Z")
    lips = pick(S, "M4 18L8.5 15L12 16L15.5 15L20 18L15.5 21H8.5Z",
                "M4 18C6 16.5 7.5 15 9 15C10.2 15 11 15.6 12 15.6C13 15.6 13.8 15 15 15C16.5 15 18 16.5 20 18C18 20 15.5 21 12 21C8.5 21 6 20 4 18Z")
    return [shell(eye_d), dot(12, 7, 1.6), shell(lips), detail(seg(4, 18, 20, 18)), dot(12, 12.8, 0.9)]


def _flag(S, x, y, w=5.5):
    """Semaphore flag: a solid square split on the diagonal by a thin gap."""
    sq = box(x, y, w, w, pick(S, 0.3, 1.2))
    return solid(path_to_d(D(sq, ST(seg(x, y, x + w, y + w), 1.3, "butt", "miter"))))


@icon("flag-semaphore", CAT, "A standing figure holding two small square flags out at different angles; semaphore signalling.",
      tags=["semaphore", "flag signals", "signalling", "navy", "scouts", "communication"], aliases=["semaphore-flags"])
def _(S):
    return [head(12, 5.5),
            limb(S, [(7.3, 7.3), (9, 10), (15.5, 10), (16.8, 14.8)]),
            _flag(S, 2, 2, 5), _flag(S, 16.8, 14.8, 5),
            line(seg(12, 10, 12, 15)),
            limb(S, [(9, 21.5), (12, 15), (15, 21.5)])]


@icon("traffic-hand-signal", CAT, "A traffic officer in a peaked cap with one arm raised palm out and the other stretched to the side.",
      tags=["traffic police", "traffic control", "stop signal", "hand signal", "crossing", "officer"])
def _(S):
    capd_ = pick(S, "M9 4.5H15.5L16 3L12.5 1.8L8.5 3Z", "M9 4.5H15.5Q16.2 3.6 15.4 3.1L12.5 1.8L9.2 3Q8.4 3.6 9 4.5Z")
    return [shell(capd_), head(12, 7, 2),
            limb(S, [(2.5, 11), (8.5, 11), (15.5, 11), (18.5, 7.5), (18.5, 3)]),
            line(seg(17, 3, 20, 3)),
            line(seg(12, 11, 12, 16)),
            limb(S, [(9, 21.5), (12, 16), (15, 21.5)])]


@icon("cycling-hand-signal", CAT, "A cyclist on a bicycle with one arm stretched straight out to signal a turn.",
      tags=["bike signal", "turn signal", "cyclist", "hand signal", "road safety", "bicycle"], aliases=["bike-turn-signal"])
def _(S):
    return [line(circle(6, 17.5, 3.5)), line(circle(18, 17.5, 3.5)),
            head(14.5, 4.5),
            limb(S, [(13.5, 8.5), (10.5, 12.5), (12.5, 17.5)]),
            line(seg(13.5, 8.5, 3, 8.5)),
            line(seg(6, 17.5, 10.5, 12.5)),
            limb(S, [(13.5, 8.5), (16, 12.5), (18, 17.5)])]


@icon("smoke-signal", CAT, "A small campfire with three separate puffs of smoke rising above it; a smoke signal.",
      tags=["smoke signal", "campfire", "signal", "message", "wilderness", "communication"])
def _(S):
    flame = pick(S, "M12 13.5L14.5 17A2.5 2.5 0 0 1 9.5 17Z", "M12 13.5C13 15 14.5 15.8 14.5 17.3A2.5 2.5 0 0 1 9.5 17.3C9.5 15.8 11 15 12 13.5Z")
    puffs = [shell(ellipse(9.5, 10, 2.5, 1.6)), shell(ellipse(14, 6, 2.5, 1.6)), shell(ellipse(9.5, 2.9, 2, 0.9))]
    return [shell(flame), line(seg(5, 21.5, 19, 19)), line(seg(5, 19, 19, 21.5))] + puffs


# ============================================================================ whole-body poses (side and front views)

@icon("person-sitting", CAT, "Side view of a person sitting on a stool with the knees bent at a right angle.",
      tags=["sit", "sitting", "seated", "seat", "rest", "posture"], aliases=["sitting"])
def _(S):
    return [head(9.5, 4.5),
            limb(S, [(9.5, 9), (9, 14), (16, 14), (16, 21.5)]),
            line(seg(4, 17, 11.5, 17)), line(seg(5.5, 17, 5.5, 21.5)), line(seg(10, 17, 10, 21.5))]


@icon("person-kneeling", CAT, "Side view of a person kneeling on both knees with the upper body upright.",
      tags=["kneel", "kneeling", "on knees", "pray", "propose", "posture"], aliases=["kneeling"])
def _(S):
    return [head(13, 4.5),
            limb(S, [(13, 9), (12.5, 14.5), (14, 20), (6, 20)]),
            limb(S, [(13, 9.5), (16, 14)])]


@icon("person-lying", CAT, "A person lying on their back on the ground with one knee raised.",
      tags=["lie down", "lying", "rest", "relax", "recline", "floor"], aliases=["lying-down"])
def _(S):
    return [head(4.5, 14),
            limb(S, [(7.5, 16.5), (14, 16.5), (17.5, 12), (21, 16.5)]),
            line(seg(2.5, 20.5, 21.5, 20.5))]


@icon("person-squatting", CAT, "Side view of a person in a deep squat with the arms held forward for balance.",
      tags=["squat", "squatting", "crouch", "exercise", "leg day", "posture"], aliases=["squat"])
def _(S):
    return [head(11, 4.5),
            limb(S, [(10.5, 9), (8.5, 15.5), (15, 13.5), (14, 21)]),
            limb(S, [(10.5, 9.5), (19.5, 10)])]


@icon("person-jumping", CAT, "Front view of a person in mid-air with arms and legs spread above the ground.",
      tags=["jump", "jumping", "star jump", "jumping jack", "joy", "celebrate"], aliases=["jumping"])
def _(S):
    return [head(12, 4.5),
            limb(S, [(5, 3.5), (8.5, 9.5), (15.5, 9.5), (19, 3.5)]),
            line(seg(12, 9.5, 12, 14)),
            limb(S, [(6, 18.5), (12, 14), (18, 18.5)]),
            line(seg(8, 21.5, 16, 21.5))]


@icon("hopping", CAT, "A person hopping on one leg with the other leg bent up behind and motion marks below.",
      tags=["hop", "hopping", "one leg", "bounce", "hopscotch", "balance"], aliases=["hop"])
def _(S):
    return [head(11, 4),
            limb(S, [(11, 8.5), (11, 14)]),
            limb(S, [(7, 12), (11, 9), (15, 12)]),
            line(seg(11, 14, 11, 18.5)),
            limb(S, [(11, 14), (15.5, 16.5), (18, 12.5)]),
            line(seg(8.5, 21.5, 13.5, 21.5))]


@icon("marching", CAT, "Side view of a person marching with one knee raised high and the opposite arm swung forward.",
      tags=["march", "marching", "parade", "military", "step", "protest"], aliases=["march"])
def _(S):
    return [head(11.5, 4.5),
            limb(S, [(11.5, 9), (11.5, 14.5)]),
            limb(S, [(11.5, 14.5), (16, 14.5), (16, 19.5)]),
            limb(S, [(11.5, 14.5), (10.5, 21.5)]),
            limb(S, [(11.5, 9.5), (15, 11.5), (17.5, 8.5)]),
            limb(S, [(11.5, 9.5), (8, 13)])]


