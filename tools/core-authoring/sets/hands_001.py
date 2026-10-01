"""TypeIcon Core: hands (batch 001): hand shapes, touch gestures and hands at work.

Hands are regions in the style of the gestures set: fingers are capsules (3.4 wide, or a little thinner for
small hands) unioned with a palm and outlined as one shell, so Filled turns them solid and knocks out the
finger separations. Line keeps wrist and palm corners square, Rounded softens them.

Shared hands: the raised index finger of hand-point-up (touch gestures), the raised palm of hand-stop, the
palm-up hand of hand-heart ("something in hand") and a side-view fist gripping an upright object.

Where a hand overlaps an object, the icon is drawn in layers (front first) and what lies behind is cut away
around the front silhouette with a gap in every style.
"""
from __future__ import annotations

import math

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path

from dsl import LINE, Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar  # noqa: F401

CAT = "hands"
FW = 3.4  # finger width


# --------------------------------------------------------------------------- region helpers

def cap(x0, y0, x1, y1, w=FW):
    """Finger or limb: a capsule along a segment."""
    return ST(seg(x0, y0, x1, y1), w, "round", "round")


def capd(d, w=FW):
    """Capsule along any open path (a curled finger)."""
    return ST(d, w, "round", "round")


def bar(x0, y0, x1, y1, w):
    """Straight band with square ends."""
    return ST(seg(x0, y0, x1, y1), w, "butt", "miter")


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


def arrow_head(S, x, y, deg, s=2.6, kind=None):
    """Open chevron arrowhead with its tip at (x, y) pointing along deg."""
    a = polar(x, y, s, deg + 180 - 45)
    b = polar(x, y, s, deg + 180 + 45)
    return (kind or line)(poly([a, (x, y), b], r=S.r * 0.4))


def arc_arrow(S, cx, cy, r, a0, a1, s=2.4):
    """Arc clockwise from a0 to a1 with an arrowhead at a1."""
    tip = polar(cx, cy, r, a1)
    return [line(arc(cx, cy, r, a0, a1)), arrow_head(S, tip[0], tip[1], a1 + 90, s)]


def dashes(x0, y0, x1, y1, n, frac=0.55, kind=None):
    """n short dashes along a segment."""
    out = []
    for k in range(n):
        t0 = k / n
        t1 = t0 + frac / n
        out.append((kind or line)(seg(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0, x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)))
    return out


def drop_d(cx, cy, r, h):
    """Water drop: round bottom of radius r centred (cx, cy), point h above the centre."""
    a = math.degrees(math.asin(r / h))
    p0 = polar(cx, cy, r, -90 - (90 - a))
    p1 = polar(cx, cy, r, -90 + (90 - a))
    return f"M{fmt(cx)} {fmt(cy - h)}L{fmt(p1[0])} {fmt(p1[1])}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(p0[0])} {fmt(p0[1])}Z"


# --------------------------------------------------------------------------- transforms

def _xd(d, m):
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def xparts(parts, m):
    return [Part(p.kind, _xd(p.d, m), dict(p.attrs)) for p in parts]


def mirror_x(parts, cx=12.0):
    return xparts(parts, (-1, 0, 0, 1, 2 * cx, 0))


def place(parts, k, tx, ty):
    """Scale by k about the origin, then shift."""
    return xparts(parts, (k, 0, 0, k, tx, ty))


def rotate_about(parts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return xparts(parts, (c, s, -s, c, cx - c * cx + s * cy, cy - s * cx - c * cy))


def rot_pts(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rot(parts, deg, cx=12.0, cy=13.0):
    return rotate_about(parts, deg, cx, cy)


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


def fig(name, desc, tags, aliases=(), gap=1.0):
    """Register an icon drawn as layers: fn(S) -> [front layer, layer behind, ...]."""
    def deco(fn):
        icon(name, CAT, desc, tags=tags, aliases=aliases,
             filled=lambda: _filled_layers(fn(LINE), gap))(lambda S: _stroke_layers(S, fn(S), gap))
        return fn
    return deco


# --------------------------------------------------------------------------- shared hands

def point_up(S):
    """Back of a hand with the index finger raised; fingertip centre at (8.5, 4.6)."""
    idx = cap(8.5, 13, 8.5, 4.6)
    fist = box(6.8, 11, 11.6, 10, wr(S))
    knuck = [cap(12, 12.6, 12, 12.6), cap(15.4, 12.8, 15.4, 12.8)]
    thumb = cap(7.2, 17.5, 4.2, 14)
    return [outline(idx, fist, *knuck, thumb), detail(seg(7.8, 17.2, 12, 17.2))]


def touch(S, tx, ty, k=0.8):
    """point_up scaled by k with the fingertip centre moved to (tx, ty)."""
    return place(point_up(S), k, tx - 8.5 * k, ty - 4.6 * k)


def open_hand(S, dx=0.0, dy=0.0, tops=(7, 5, 5.5, 7.5), bottom=21):
    """Raised open palm facing the viewer, fingers together (the hand-stop hand)."""
    xs = [6.3, 9.7, 13.1, 16.5]
    fingers = [cap(x + dx, t + dy, x + dx, 13 + dy) for x, t in zip(xs, tops)]
    palm = box(4.6 + dx, 12 + dy, 13.6, bottom - 12, wr(S))
    thumb = cap(6 + dx, 17.5 + dy, 3.6 + dx, 13.5 + dy)
    parts = [outline(*fingers, palm, thumb)]
    for k in range(3):
        xm = (xs[k] + xs[k + 1]) / 2 + dx
        parts.append(detail(seg(xm, max(tops[k], tops[k + 1]) + dy + 1.7, xm, 12.5 + dy)))
    return parts


def palm_up(S, dx=0.0, dy=0.0):
    """A hand held out palm up from the left, fingertips curling up on the right (the hand-heart hand)."""
    wrist = box(2.5 + dx, 15 + dy, 7, 6.5, wr(S))
    fingers = [cap(8 + dx, 19.2 + dy, 17.5 + dx, 19.2 + dy, 3.2), cap(17.5 + dx, 19.2 + dy, 19.8 + dx, 16.8 + dy, 3.2)]
    thumb = cap(8 + dx, 16.8 + dy, 10.4 + dx, 15.2 + dy, 2.8)
    return [outline(wrist, *fingers, thumb)]


def grip(S, top=13.0, rw=2.9, dx=0.0, n=2):
    """Hand seen from the side, arm from the left, fingers curled round an upright object at x ~ 12.5 + dx.

    The thumb wraps over the top; n finger rows end in knuckles on the right.
    """
    t = top
    th = 2.7
    ys = [t + th + rw * (k + 0.5) + 0.2 for k in range(n)]
    bottom = ys[-1] + rw / 2
    ends = (17.4, 16.8, 16.2)
    rows = [cap(9 + dx, y, ends[k] + dx, y, rw) for k, y in enumerate(ys)]
    thumb = cap(8 + dx, t + th / 2, 14.6 + dx, t + th / 2, th)
    fist = box(6.5 + dx, t, 7, bottom - t, pick(S, 1, 2))
    cuff = box(2.5 + dx, t + 0.6, 3, bottom - t - 1.2, pick(S, 0.5, 1.5))
    seps = [detail(seg(11.5 + dx, (ys[k] + ys[k + 1]) / 2, 18 + dx, (ys[k] + ys[k + 1]) / 2)) for k in range(n - 1)]
    return [outline(fist, thumb, *rows), outline(cuff), detail(seg(9 + dx, t + th + 0.1, 15.2 + dx, t + th + 0.1))] + seps


def fist_side(S, x=3.0, y=7.0, w=7.5, h=10.5):
    """Side view of a fist: knuckle bumps to the right, thumb folded across the top."""
    rh = (h - 3.2) / 3
    rows = [cap(x + 2, y + 3.2 + rh * (k + 0.5), x + w - rh / 2, y + 3.2 + rh * (k + 0.5), rh) for k in range(3)]
    body = box(x, y, w - 1.5, h, pick(S, 1.5, 2.5))
    thumb = cap(x + 1.5, y + 1.6, x + w - 1.8, y + 1.6, 3.2)
    seps = [detail(seg(x + w - 3.2, y + 3.2 + rh * k, x + w, y + 3.2 + rh * k)) for k in (1, 2)]
    return [outline(body, thumb, *rows), detail(seg(x + 1.5, y + 3.2, x + w - 1, y + 3.2))] + seps


def fist_rows(S, x, y, w, h, n=2):
    """A fist seen from the front wrapped round an object: a block with n finger lines across it."""
    parts = [outline(box(x, y, w, h, wr(S)))]
    for k in range(1, n + 1):
        yy = y + h * k / (n + 1)
        parts.append(detail(seg(x, yy, x + w, yy)))
    return parts


def heart_d(cx, cy, w):
    """Heart of width w centred on (cx, cy)."""
    k = w / 16.0
    return _xd("M12 20L4.4 12.6A4.6 4.6 0 0 1 11 6.3L12 7.3L13 6.3A4.6 4.6 0 0 1 19.6 12.6Z",
               (k, 0, 0, k, cx - 12 * k, cy - 13 * k))


# ============================================================================ hand shapes

@icon("hand-pinky-up", CAT, "A closed fist with only the little finger raised straight up.",
      tags=["pinky", "little finger", "pinkie", "fist", "hand sign", "raised finger"])
def _(S):
    fist = box(5.4, 11, 12.6, 10, wr(S))
    knuck = [cap(x, 12.6, x, 12.6) for x in (7.1, 10.5)]
    ring = cap(13.9, 12.8, 13.9, 12.8, 3.2)
    pinky = cap(16.6, 13, 16.6, 6.6, 2.8)
    thumb = cap(6.6, 17.5, 3.6, 14)
    return [outline(fist, *knuck, ring, pinky, thumb), detail(seg(7.2, 17.2, 11.6, 17.2))]


@icon("c-shape-hand", CAT, "A hand seen from the side with thumb and fingers curved into an open letter C.",
      tags=["c hand", "letter c", "sign language", "cup", "curve", "grip"])
def _(S):
    cx, cy, r = 14, 12, 5.8
    fingers = capd(arc(cx, cy, r, 180, 325), 4.4)
    thumb = capd(arc(cx, cy, r, 35, 115), 3.2)
    wrist = bar(2, cy + 0.6, cx - r + 1, cy + 0.6, 5.6)
    return [outline(fingers, thumb, wrist), detail(seg(4.5, cy - 2.2, 4.5, cy + 3.4))]


@icon("hands-forming-roof", CAT, "Two flat hands meeting at the fingertips in a peaked roof over a small person.",
      tags=["shelter", "protection", "home", "insurance", "safe", "care"])
def _(S):
    left = mitten(3.8, 15, 11.1, 5.4, 4.2)
    right = mitten(20.2, 15, 12.9, 5.4, 4.2)
    body = pick(S, "M7.5 21.5V19.5Q7.5 17 10 17H14Q16.5 17 16.5 19.5V21.5", "M7.5 21.5V20A3 3 0 0 1 10.5 17H13.5A3 3 0 0 1 16.5 20V21.5")
    return [outline(left), outline(right), dot(12, 13, 2.2), line(body)]


@icon("hand-binoculars", CAT, "Two hands curled into tubes side by side and held up like binoculars.",
      tags=["hand binoculars", "looking", "search", "spy", "peek", "watching"])
def _(S):
    regs = []
    for m in (lambda x: x, lambda x: 24 - x):
        regs += [D(disc(m(7.2), 8.2, 4.6), disc(m(7.2), 8.2, 2)), box(min(m(3), m(12)), 10.5, 9, 11, wr(S))]
    return [outline(*regs), detail(seg(12, 11.5, 12, 21.5)), detail(seg(3, 14.6, 10.5, 14.6)), detail(seg(13.5, 14.6, 21, 14.6)),
            detail(seg(3, 17.9, 10.5, 17.9)), detail(seg(13.5, 17.9, 21, 17.9))]


@icon("talking-hand-gesture", CAT, "A hand shaped like a talking mouth, fingers above and thumb below, with speech lines.",
      tags=["talk", "chatter", "blah blah", "yapping", "gossip", "talking too much"])
def _(S):
    fingers = mitten(3, 9.5, 13.5, 8.2, 5.2)
    thumb = cap(5, 15.2, 12.5, 15.8, 3.0)
    wrist = box(2, 7, 4.5, 11, wr(S) * 0.6)
    lines = [line(seg(*polar(15, 12, 3, a), *polar(15, 12, 6.5, a))) for a in (-35, 0, 35)]
    return [outline(fingers, thumb, wrist), detail(seg(4.5, 10.3, 12, 10.3))] + lines


@icon("palm-note", CAT, "An open palm facing the viewer with scribbled notes written across it.",
      tags=["note on hand", "reminder", "memo", "cheat sheet", "palm", "handwriting"])
def _(S):
    xs = [6.3, 9.7, 13.1, 16.5]
    tops = [5, 3, 3.5, 5.5]
    dx = 1.3
    fingers = [cap(x + dx, t, x + dx, 10) for x, t in zip(xs, tops)]
    palm = box(4.6 + dx, 9, 13.6, 12.5, wr(S))
    thumb = cap(6 + dx, 16, 3.6 + dx, 12)
    parts = [outline(*fingers, palm, thumb)]
    for k in range(3):
        xm = (xs[k] + xs[k + 1]) / 2 + dx
        parts.append(detail(seg(xm, max(tops[k], tops[k + 1]) + 1.7, xm, 9.5)))
    parts.append(detail("M8.5 13.5Q9.6 12.2 10.7 13.5T12.9 13.5T15.1 13.5T17.3 13.5"))
    parts.append(detail("M8.5 17.5Q9.6 16.2 10.7 17.5T12.9 17.5T15.1 17.5"))
    return parts


@icon("wrap-it-up-gesture", CAT, "A raised index finger circling in the air, shown by a circular arrow around the fingertip.",
      tags=["wrap it up", "hurry", "finish", "time", "speed up", "round up"])
def _(S):
    hand = touch(S, 12, 9.5, 0.78)
    return hand + arc_arrow(S, 12, 8, 5.5, 125, 395)


@icon("hand-span", CAT, "An open hand with the fingers spread wide under a double-headed arrow measuring from thumb to little finger.",
      tags=["hand span", "span", "measure", "spread fingers", "stretch", "reach"])
def _(S):
    cx, cy = 12, 17
    regs = [box(7.5, 14, 9, 7.5, wr(S))]
    for a, ln, w in ((-168, 8.3, 3.0), (-116, 9.5, 2.8), (-93, 10, 2.8), (-70, 9.6, 2.8), (-45, 8.4, 2.6)):
        regs.append(cap(*polar(cx, cy, 3, a), *polar(cx, cy, ln, a), w))
    return [outline(*regs), line(seg(3.5, 3.5, 20.5, 3.5)), arrow_head(S, 3, 3.5, 180, 2.4), arrow_head(S, 21, 3.5, 0, 2.4)]


@icon("triple-tap-gesture", CAT, "A pointing finger with a tap ripple beside the number 3, for a triple tap.",
      tags=["triple tap", "tap three times", "touch", "gesture", "touchscreen", "zoom"])
def _(S):
    hand = touch(S, 8.5, 10, 0.72)
    three = pick(S, "M14.8 3H20L17.4 6.6C19.1 6.6 20.4 7.6 20.4 9.2C20.4 10.8 19.2 11.8 17.6 11.8C16.6 11.8 15.8 11.4 15.2 10.6",
                 "M15.6 3H18.9Q20.6 3 19.6 4.2L17.4 6.6C19.1 6.6 20.4 7.6 20.4 9.2C20.4 10.8 19.2 11.8 17.6 11.8C16.6 11.8 15.8 11.4 15.2 10.6")
    return hand + [line(arc(8.5, 10, 3.6, 200, 340)), line(arc(8.5, 10, 6.8, 210, 330)), line(three)]


@icon("two-finger-tap-gesture", CAT, "A hand with two fingers raised together tapping, with tap ripples above the fingertips.",
      tags=["two finger tap", "two finger click", "right click", "trackpad", "touch", "gesture"])
def _(S):
    fingers = [cap(10, 13, 10, 8), cap(13.4, 13, 13.4, 8)]
    fist = box(8.3, 11, 10.6, 10, wr(S))
    knuck = cap(16.8, 12.6, 16.8, 12.6)
    thumb = cap(8.7, 17.5, 6.4, 14.5, 3)
    return [outline(*fingers, fist, knuck, thumb), detail(seg(11.7, 9.5, 11.7, 12.5)), detail(seg(9.3, 17.2, 13.5, 17.2)),
            line(arc(11.7, 8, 4.2, 205, 335)), line(arc(11.7, 8, 7, 215, 325))]


@icon("three-finger-swipe-gesture", CAT, "A hand with three fingers raised under a long arrow pointing to the side.",
      tags=["three finger swipe", "swipe", "trackpad", "switch apps", "touch", "gesture"])
def _(S):
    xs = (7.3, 11, 14.7)
    fingers = [cap(x, 13, x, t, 3.2) for x, t in zip(xs, (8.2, 7.4, 8.2))]
    fist = box(5.6, 12, 13.4, 9.5, wr(S))
    knuck = cap(17.4, 13.8, 17.4, 13.8, 3.2)
    thumb = cap(6.2, 18, 3.4, 14.6, 3.0)
    return [outline(*fingers, fist, knuck, thumb), detail(seg(9.15, 10.4, 9.15, 13)), detail(seg(12.85, 10.4, 12.85, 13)),
            detail(seg(6.8, 18, 11, 18)), line(seg(3, 3.5, 20.5, 3.5)), arrow_head(S, 21, 3.5, 0, 2.6)]


@icon("flick-gesture", CAT, "A fingertip with a quick curved flick stroke leaving it and speed lines trailing.",
      tags=["flick", "fling", "swipe fast", "touch", "gesture", "throw"])
def _(S):
    return touch(S, 6.5, 10.5, 0.7) + [line("M8 5.5Q12 2.5 19 3.5"), arrow_head(S, 19.6, 3.6, 8, 2.6),
                                        line("M12.5 9.5Q15.5 8 19 8.5"), line("M15 14Q17 13.2 20 13.5")]


@fig("edge-swipe-gesture", "A phone with a fingertip at its side edge and an arrow pointing inward from the bezel.",
     tags=["edge swipe", "back gesture", "swipe", "touchscreen", "phone", "gesture"])
def _(S):
    hand = touch(S, 13, 11, 0.64)
    phone = [shell(rect(2.5, 2.5, 10.5, 19, min(S.R, 2.5)))]
    arrow = [detail(seg(10.5, 7.5, 6.2, 7.5)), arrow_head(S, 5.8, 7.5, 180, 2.4, detail)]
    return [hand, phone + arrow]


def corner_box(S, x, y, w, h, t=2.2):
    """Four corner brackets marking a square drop target."""
    r = S.r * 0.5
    return [line(poly([(x, y + t), (x, y), (x + t, y)], r=r)), line(poly([(x + w - t, y), (x + w, y), (x + w, y + t)], r=r)),
            line(poly([(x + w, y + h - t), (x + w, y + h), (x + w - t, y + h)], r=r)),
            line(poly([(x + t, y + h), (x, y + h), (x, y + h - t)], r=r))]


@fig("drag-and-drop-gesture", "A fingertip dragging a small tile toward a dashed drop target.",
     tags=["drag and drop", "drag", "drop", "move", "touch", "gesture"])
def _(S):
    tile = [shell(rect(3, 2.5, 7, 7, min(S.R, 2)))]
    hand = touch(S, 7.5, 8.5, 0.7)
    target = corner_box(S, 15, 2.5, 6.5, 6.5) + [line(seg(11.5, 6, 12.6, 6))]
    return [hand, tile, target]


@icon("force-press-gesture", CAT, "A fingertip pressing hard on a surface inside layered pressure rings, with a downward arrow.",
      tags=["force press", "deep press", "pressure touch", "hard press", "pressure", "gesture"])
def _(S):
    tx, ty = 10, 11
    rings = [line(arc(tx, ty, 4.2, 150, 390)), line(arc(tx, ty, 7.2, 160, 380))]
    return touch(S, tx, ty, 0.68) + rings + [line(seg(20, 2.5, 20, 8)), arrow_head(S, 20, 8.5, 90, 2.4)]


@fig("draw-gesture", "A fingertip at the end of a looping freehand line drawn from a dot.",
     tags=["draw", "finger drawing", "sketch", "doodle", "touchscreen", "gesture"])
def _(S):
    tx, ty = 16, 12.5
    path = "M3.5 17.5C3.5 11 6 5.5 9.5 5.5C12.5 5.5 12.5 10 10 10C7.5 10 8.5 6 12 7C14 7.6 16 9.5 16 12.5"
    return [touch(S, tx, ty, 0.6), [line(path), dot(3.5, 19.5, 1.6)]]


@icon("pattern-unlock", CAT, "A three by three grid of dots with a connected line drawn through several of them.",
      tags=["pattern lock", "unlock", "swipe pattern", "screen lock", "password", "security"])
def _(S):
    g = (4.5, 12, 19.5)
    path = [(g[0], g[1]), (g[1], g[0]), (g[2], g[1]), (g[1], g[2])]
    visited = set(path)
    parts = [line(poly(path, r=S.r))]
    for x in g:
        for y in g:
            if (x, y) not in visited:
                parts.append(dot(x, y, 1.3))
    parts.append(dot(g[1], g[2], 2.2))
    return parts


@icon("tilt-phone-gesture", CAT, "A phone tilted at an angle with a curved double-headed arrow beside its top corner.",
      tags=["tilt", "tilt phone", "motion", "gyroscope", "rotate device", "gesture"])
def _(S):
    cx, cy = 10.5, 13.5
    phone = rotate_about([shell(rect(cx - 3.5, cy - 6.5, 7, 13, min(S.R, 2))), detail(seg(cx - 1, cy + 3.8, cx + 1, cy + 3.8))], -20, cx, cy)
    r = 10.5
    a0, a1 = -72, -8
    return phone + [line(arc(cx, cy, r, a0, a1)), arrow_head(S, *polar(cx, cy, r, a0), a0 - 90, 2.4),
                    arrow_head(S, *polar(cx, cy, r, a1), a1 + 90, 2.4)]


@fig("raise-to-wake", "A wrist wearing a smartwatch lifted along a curved arrow, with its face lit up.",
     tags=["raise to wake", "wrist raise", "smartwatch", "wake screen", "lift", "gesture"])
def _(S):
    strap = [line(poly([(14.5, 9), (14.5, 3), (19.5, 3), (19.5, 9)])), line(poly([(14.5, 17), (14.5, 22), (19.5, 22), (19.5, 17)]))]
    face = [shell(rect(12, 8.5, 10, 9, min(S.R, 2.5))), line(poly([(17, 10.8), (17, 13), (19.2, 13)], r=S.r * 0.4))]
    return [face + strap + arc_arrow(S, 21, 12.5, 13.5, 150, 212, 2.4)]


@icon("multi-touch-gesture", CAT, "Five fingertip touch points spread in the arc of a hand on a trackpad.",
      tags=["multi-touch", "multitouch", "five finger", "trackpad", "touchscreen", "gesture"])
def _(S):
    pad = shell(rect(2.5, 3.5, 19, 17, S.R))
    pts = [(6.3, 14.5), (8.3, 9.2), (12, 7.6), (15.7, 9.2), (17.7, 14.5)]
    return [pad] + [dot(x, y, 1.8) for x, y in pts]


@fig("back-tap-gesture", "The back of a phone with a camera bump and a finger tapping the back panel.",
     tags=["back tap", "tap back", "phone", "shortcut", "accessibility", "gesture"])
def _(S):
    finger = [outline(cap(15.5, 20.6, 15.5, 13.4, 3.6)), line(seg(11.2, 10.4, 10.2, 9.2)), line(seg(19.8, 10.4, 20.8, 9.2)), line(seg(15.5, 9.4, 15.5, 7.8))]
    phone = [shell(rect(3.5, 2.5, 13, 18.5, min(S.R, 2.5))), shell(rect(6, 5, 4.5, 4.5, min(S.R, 1.2))), dot(8.25, 7.25, 0.8)]
    return [finger, phone]





@fig("hand-on-mouse", "A hand seen from above resting on a computer mouse with the index finger on the left button.",
     tags=["mouse", "computer mouse", "click", "desk", "computer", "office"])
def _(S):
    hand = [outline(cap(10.3, 13, 10.3, 7, 3.2), cap(13.7, 13, 13.7, 7.8, 3.2), box(8.7, 12, 6.6, 9.5, wr(S))),
            detail(seg(12, 9.6, 12, 12.5))]
    mouse = [shell(rect(3.5, 2.5, 17, 19, 7.5 if S.name == "rounded" else 5)), line(seg(12, 2.5, 12, 4))]
    return [hand, mouse]


@icon("data-glove", CAT, "A glove with sensor dots across the knuckles and a cable leading from the cuff.",
      tags=["data glove", "vr glove", "haptic", "motion capture", "sensor", "wearable"])
def _(S):
    xs = [7.3, 10.7, 14.1, 17.5]
    tops = [6, 4, 4.5, 6.5]
    fingers = [cap(x, t, x, 12) for x, t in zip(xs, tops)]
    palm = box(5.6, 11, 13.6, 7.5, wr(S))
    thumb = cap(7, 15.5, 4.6, 11.5)
    parts = [outline(*fingers, palm, thumb), shell(rect(7, 18.5, 10.8, 3, min(S.R, 1)))]
    for k in range(3):
        xm = (xs[k] + xs[k + 1]) / 2
        parts.append(detail(seg(xm, max(tops[k], tops[k + 1]) + 1.7, xm, 11.5)))
    parts += [dot(x, 14, 0.9) for x in (8.7, 12.4, 16.1)]
    parts.append(line("M17.8 20H20Q21.5 20 21.5 18.5V16"))
    return parts


@fig("palm-push", "A flat palm pressing against the side of a square block, with motion lines beyond it.",
     tags=["push", "shove", "force", "move", "press", "effort"])
def _(S):
    hand = place(open_hand(S), 0.64, 0.6, 3.2)
    block = [shell(rect(13.6, 5, 5.4, 14, min(S.R, 2))), line(seg(21.4, 8, 22.6, 8)), line(seg(21.4, 12, 22.6, 12)), line(seg(21.4, 16, 22.6, 16))]
    return [hand, block]


@icon("tearing-paper", CAT, "A sheet of paper being pulled apart into two halves along a jagged tear.",
      tags=["tear", "rip", "torn", "cancel", "break up", "destroy"])
def _(S):
    left = rotate_about([shell(poly([(4, 4), (11, 4), (9.5, 7.5), (11.5, 10.5), (9.5, 14), (11, 17), (10, 20), (4, 20)], closed=True, r=S.r * 0.3))], -8, 7, 20)
    right = rotate_about([shell(poly([(13, 4), (20, 4), (20, 20), (14, 20), (15, 17), (13.5, 14), (15.5, 10.5), (13.5, 7.5)], closed=True, r=S.r * 0.3))], 8, 17, 20)
    return left + right


@fig("crumpling-paper", "A hand squeezing a crumpled ball of paper with angular creases showing above the fingers.",
     tags=["crumple", "scrunch", "paper ball", "discard", "rejected idea", "waste paper"])
def _(S):
    ball = [shell(poly([(6.5, 10), (8, 5), (12, 2.8), (15.5, 4), (19.5, 3.2), (21, 8.5), (19, 13), (14, 15.5), (9, 14.5)], closed=True, r=S.r * 0.3),
                  stroke_miterlimit="2"),
            detail(poly([(12, 2.8), (13, 8), (19.5, 3.2)])), detail(seg(13, 8, 11, 13))]
    return [fist_side(S, 2.5, 11, 8, 10.5), ball]


@fig("peeling-sticker", "A finger lifting the curled corner of a square sticker off a surface.",
     tags=["peel", "sticker", "label", "decal", "remove", "peel off"])
def _(S):
    finger = [outline(cap(21, 21, 16.4, 16.4, 3.2))]
    flap = [shell(poly([(17, 11), (11, 17), (11, 11)], closed=True, r=S.r * 0.3), stroke_miterlimit="2")]
    sticker = [shell(poly([(3, 3), (17, 3), (17, 11), (11, 17), (3, 17)], closed=True, r=S.r * 0.5))]
    return [finger, flap, sticker]


@fig("stress-ball-squeeze", "A hand clenched around a round ball that bulges out above and beside the fingers.",
     tags=["stress ball", "squeeze", "stress relief", "anxiety", "grip", "exercise"])
def _(S):
    ball = [shell(circle(13.5, 9.5, 6.8))]
    return [fist_side(S, 3.5, 11, 8, 10.5), ball]


@fig("house-in-hand", "An open palm held up with a small house resting on it.",
     tags=["house in hand", "home", "real estate", "mortgage", "housing", "property"])
def _(S):
    house = [shell(poly([(7.5, 9.5), (12.5, 4.5), (17.5, 9.5), (17.5, 17.5), (7.5, 17.5)], closed=True, r=S.r * 0.6)),
             detail(seg(12.5, 17.5, 12.5, 13.5))]
    return [palm_up(S), house]


@fig("idea-in-hand", "An open palm held up with a lightbulb standing on it and short rays around the bulb.",
     tags=["idea", "lightbulb", "inspiration", "innovation", "insight", "brainstorm"])
def _(S):
    bulb = [shell("M10.6 14.3A4.25 4.25 0 1 1 14.4 14.3V17.5H10.6Z")]
    rays = [line(seg(*polar(12.5, 10.5, 6.9, a), *polar(12.5, 10.5, 8.6, a))) for a in (-150, -90, -30)]
    return [palm_up(S, 0, 1), bulb + rays]


@fig("checking-for-rain", "An open palm held out face up with raindrops falling onto it from above.",
     tags=["rain", "raining", "drops", "weather", "drizzle", "check weather"])
def _(S):
    drops = [shell(drop_d(x, y, 1.9, 4.4)) for x, y in ((7.5, 7), (16.5, 7), (12, 11.5))]
    return [palm_up(S, 0, 1.5), drops]


@fig("carrying-briefcase", "A hand gripping the top handle of a briefcase hanging below it.",
     tags=["briefcase", "carry", "commute", "work", "business", "office"])
def _(S):
    fist = [outline(box(8, 2.5, 8, 5.5, wr(S))), detail(seg(10.7, 4.6, 10.7, 8)), detail(seg(13.3, 4.6, 13.3, 8))]
    handle = [line(pick(S, "M9.5 11.5V9H14.5V11.5", "M9.5 11.5V10.5Q9.5 9 11 9H13Q14.5 9 14.5 10.5V11.5"))]
    case = [shell(rect(3, 11.5, 18, 9.5, min(S.R, 2.5))), detail(seg(3, 15.8, 21, 15.8)), dot(12, 15.8, 0.9)]
    return [fist, handle + case]


@fig("hand-holding-flashlight", "A hand gripping a flashlight with a widening beam of light from its head.",
     tags=["flashlight", "torch", "light beam", "search", "dark", "inspect"])
def _(S):
    torch = [shell(poly([(9.6, 19.5), (9.6, 10), (8.2, 6), (15.8, 6), (14.4, 10), (14.4, 19.5)], closed=True, r=S.r * 0.4))]
    fist = [outline(box(7.3, 13, 9.4, 7.5, wr(S))), detail(seg(7.3, 15.5, 16.7, 15.5)), detail(seg(7.3, 18, 16.7, 18))]
    beams = [line(seg(9, 3.6, 7.6, 1.8)), line(seg(12, 3.4, 12, 1)), line(seg(15, 3.6, 16.4, 1.8))]
    return [rot(fist, 38), rot(torch + beams, 38)]


@fig("pointing-remote", "A hand holding a remote control pointed forward with two signal arcs from its tip.",
     tags=["remote control", "tv remote", "clicker", "point", "infrared", "television"])
def _(S):
    remote = [shell(rect(9, 7.5, 6, 13, min(S.R, 2))), dot(12, 10.4, 0.9), dot(12, 13.4, 0.9)]
    fist = [outline(box(7.3, 16, 9.4, 6, wr(S))), detail(seg(7.3, 18.3, 16.7, 18.3))]
    arcs = [line(arc(12, 6, 3.4, -130, -50)), line(arc(12, 6, 6.0, -130, -50))]
    return [rot(fist, 35), rot(remote + arcs, 35)]


@fig("reading-with-finger", "An index finger resting under one line of text on a page with more lines above and below.",
     tags=["reading", "follow text", "literacy", "line by line", "study", "point at text"])
def _(S):
    page = [shell(rect(3, 2.5, 13, 18.5, min(S.R, 2))), detail(seg(6, 7, 13, 7)), detail(seg(6, 11, 13, 11)), detail(seg(6, 15, 13, 15))]
    hand = rotate_about(touch(S, 12.5, 13.4, 0.6), -90, 12.5, 13.4)
    return [hand, page]


@fig("turning-page", "A hand lifting the corner of the right page of an open book as it curls over.",
     tags=["turn page", "page", "book", "reading", "flip", "next page"])
def _(S):
    thumb = [outline(cap(21.4, 21, 18, 17.6, 2.8))]
    flap = [shell(poly([(21.5, 12.5), (16.5, 19), (14.7, 14.3)], closed=True, r=S.r * 0.3), stroke_miterlimit="2")]
    book = [shell(poly([(12, 6), (7, 4.5), (2.5, 5.5), (2.5, 19.5), (7, 18.5), (12, 20)], closed=False)),
            shell(poly([(12, 6), (17, 4.5), (21.5, 5.5), (21.5, 12.5), (16.5, 19), (12, 20)], closed=False)),
            line(seg(12, 6, 12, 20))]
    return [thumb, flap, book]


@fig("baby-grasping-finger", "A tiny baby hand wrapped around the tip of a larger adult index finger.",
     tags=["baby", "newborn", "parent", "bond", "infant hand", "family"])
def _(S):
    baby = [outline(box(14, 11, 6, 9.5, wr(S) * 0.8), cap(14.5, 12.2, 6.5, 12.2, 2.4), cap(14.5, 15.2, 6.5, 15.2, 2.4), cap(14.5, 18.2, 7, 18.2, 2.4)),
            detail(seg(9.5, 13.7, 14, 13.7)), detail(seg(9.5, 16.7, 14, 16.7))]
    adult = [outline(mitten(9.5, 23, 9.5, 5.5, 4.4))]
    return [baby, adult]


@fig("comforting-hand", "One hand resting gently on top of another hand with a small heart above them.",
     tags=["comfort", "support", "sympathy", "reassure", "care", "empathy"])
def _(S):
    lower = palm_up(S, 0, 1.4)
    upper = mirror_x(palm_up(S, 0, -3.5))
    heart = [shell(heart_d(12, 6.6, 7.5), stroke_miterlimit="2")]
    return [upper, lower, heart]


@fig("launching-paper-plane", "A hand releasing a paper plane forward with a dotted flight trail behind the plane.",
     tags=["paper plane", "launch", "throw", "release", "send off", "fly"])
def _(S):
    plane = [shell(poly([(21.5, 2.5), (9.5, 7.5), (13.5, 10.2), (16, 14.5)], closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
             detail(seg(21.5, 2.5, 13.5, 10.2))]
    trail = [dot(10.4, 14.4, 0.9), dot(7.6, 17, 0.9)]
    return [fist_side(S, 2.5, 13.5, 7.5, 9), plane + trail] if False else [fist_side(S, 2.5, 14, 7, 8.5), plane + trail]


@fig("cutting-with-scissors", "Open scissors cutting along a dashed line into a sheet of paper.",
     tags=["scissors", "cut", "cutting paper", "craft", "trim", "snip"])
def _(S):
    blades = [line(seg(6.3, 17.2, 15.5, 9.6)), line(seg(6.3, 8.8, 15.5, 16.4))]
    loops = [shell(circle(4.4, 7.2, 2.5)), shell(circle(4.4, 18.8, 2.5))]
    paper = [shell(rect(11, 4.5, 10.5, 15.5, min(S.R, 1.5))), line(seg(17, 13, 21.5, 13))]
    return [blades + loops, paper]


@fig("erasing-pencil-mark", "A hand rubbing an eraser over a smudged line with small crumbs scattered beside it.",
     tags=["eraser", "erase", "rubber", "correct", "rub out", "mistake"])
def _(S):
    eraser = rot([shell(rect(9, 2.5, 7, 11, min(S.R, 1.8))), detail(seg(9, 6, 16, 6))], 38, 12, 9)
    thumb = [outline(cap(21.5, 5, 17, 5.5, 2.8))]
    smudge = [line("M2.5 20Q4.5 17 6.5 20T10.5 20T14.5 20")]
    crumbs = [dot(17.5, 18.5, 0.9), dot(20.5, 20.5, 0.9), dot(20.5, 15.5, 0.9)]
    return [thumb, eraser + smudge + crumbs]


@icon("shielding-flame", CAT, "A cupped hand curved around one side of a candle flame to block the wind.",
      tags=["protect", "flame", "candle", "wind", "shelter", "fragile"])
def _(S):
    flame = [shell(drop_d(14, 9, 2.6, 6.2)), shell(rect(11.5, 13.5, 5, 7.5, min(S.R, 1.5)))]
    hand = [outline(capd(arc(15, 11.5, 7.5, 130, 230), 3.4))]
    wind = [line("M2.5 8.5Q3.8 7 5.1 8.5"), line("M2.5 12.5Q3.8 11 5.1 12.5")]
    return hand + flame + wind


@icon("breaking-chains", CAT, "A chain snapped at its middle link with the two halves pulled apart.",
      tags=["break chains", "freedom", "liberty", "escape", "free", "broken chain"])
def _(S):
    left = [shell(rect(2.5, 8.5, 7, 5.5, 2.75)), line(poly([(9.5, 11.2), (11.5, 11.2), (10.6, 13.6)], r=S.r * 0.3))]
    return left + mirror_x(left) + [line(seg(12, 3.5, 12, 6)), line(seg(8.4, 5, 9.6, 6.8)), line(seg(15.6, 5, 14.4, 6.8))]


@fig("flicking-lighter", "A hand holding a pocket lighter with the thumb on the wheel and a small flame on top.",
     tags=["lighter", "flint", "light", "flame", "smoker", "ignite"])
def _(S):
    lighter = [shell(rect(10, 8.5, 8, 13.5, min(S.R, 2))), detail(seg(10, 12, 18, 12)), shell(drop_d(14, 6, 1.8, 3.8))]
    return [fist_side(S, 3.5, 12.5, 8.5, 9.5), lighter]


@fig("threading-needle", "A thumb and finger holding the end of a thread pointed at the eye of an upright sewing needle.",
     tags=["thread needle", "sewing", "needle eye", "stitch", "tailor", "craft"])
def _(S):
    needle = [outline(mitten(17, 22, 17, 4.5, 4.2)), detail(seg(17, 5.8, 17, 9.4))]
    thread = [line("M4.5 17C6 11 10 7.5 13.5 7.6")]
    fingers = [outline(cap(3.6, 20.6, 6.4, 16.6, 2.8), cap(7.2, 21, 7.8, 17.6, 2.6))]
    return [fingers, needle + thread]


@fig("petting-dog", "A hand resting flat on top of a dog's head with two small curved stroke marks above the hand.",
     tags=["pet dog", "stroke dog", "pat", "dog", "puppy", "animal care"])
def _(S):
    hand = [outline(cap(4.6, 8.6, 17.4, 8.6, 5.0), cap(18.6, 11.4, 18.6, 11.4, 3.0)), detail(seg(13.6, 6.8, 13.6, 8.4))]
    marks = [line("M7 4.6Q8.6 2.8 10.2 4.6"), line("M13 4.6Q14.6 2.8 16.2 4.6")]
    dog = [shell(circle(12, 15.6, 5.6)), outline(cap(5.8, 13.6, 4.4, 18.4, 3.2)), outline(cap(18.2, 13.6, 19.6, 18.4, 3.2)),
           dot(10, 15, 0.9), dot(14, 15, 0.9), dot(12, 17.6, 1.2)]
    return [hand + marks, dog]
