"""TypeIcon Core: hands & gestures.

Hands are built as regions: fingers are capsules 3.4 wide (the pitch of the body `hand`), unioned with a
palm, and outlined as one shell. Finger separations are details, so Filled knocks them out. Line keeps the
wrist corners square, Rounded softens them.

Mirrored / rotated siblings (point-left, point-down, thumbs-down) are recorded as transform-derived designs.
"""
from __future__ import annotations

import math

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path

from dsl import REGISTRY, D, P, Part, ST, U, arc, circle, detail, dot, ellipse, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "gestures"
FW = 3.4  # finger width


# --------------------------------------------------------------------------- region helpers

def cap(x0, y0, x1, y1, w=FW):
    """Finger: a capsule along a segment."""
    return ST(seg(x0, y0, x1, y1), w, "round", "round")


def box(x, y, w, h, r=0.0):
    return P(rect(x, y, w, h, r))


def outline(*regions, **attrs):
    return shell(path_to_d(U(*regions)), **attrs)


def wr(S):
    """Wrist / palm corner radius: square for Line, soft for Rounded."""
    return 0.5 if S.name == "line" else 2.5


# --------------------------------------------------------------------------- layers (overlapping hands)

def _sil(parts, S):
    regs = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        elif p.kind == "shell":
            regs.append(U(P(p.d), ST(p.d, 2.0, S.cap, S.join)))
        else:
            regs.append(ST(p.d, 2.0, S.cap, S.join))
    return U(*regs)


def _paint(parts, S):
    return U(*[P(p.d) if p.kind in ("dot", "solid") else ST(p.d, 2.0, S.cap, S.join) for p in parts])


def _grow(r, g):
    return r if g <= 0 else U(r, ST(path_to_d(r), 2 * g, "round", "round"))


def _stack_stroke(S, layers, gap):
    out = list(layers[0])
    cover = _grow(_sil(layers[0], S), gap)
    for layer in layers[1:]:
        vis = D(_paint(layer, S), cover)
        if abs(vis.area) > 0.01:
            out.append(solid(path_to_d(vis)))
        cover = U(cover, _grow(_sil(layer, S), gap))
    return out


def _stack_filled(layers, gap):
    from dsl import filled_region
    res = filled_region(layers[0])
    cover = _grow(res, gap)
    for layer in layers[1:]:
        f = filled_region(layer)
        res = U(res, D(f, cover))
        cover = U(cover, _grow(f, gap))
    return res


def layered(name, desc, tags, aliases=(), gap=1.5):
    """fn(S) -> [front parts, parts behind, ...]; what is behind is cut away around what is in front."""
    from dsl import LINE

    def deco(fn):
        icon(name, CAT, desc, tags=tags, aliases=aliases,
             filled=lambda: _stack_filled(fn(LINE), gap))(lambda S: _stack_stroke(S, fn(S), gap))
        return fn
    return deco


# --------------------------------------------------------------------------- transforms (for derived siblings)

MIRROR_X = (-1, 0, 0, 1, 24, 0)
MIRROR_Y = (1, 0, 0, -1, 0, 24)


def _xd(d, m):
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def _xparts(parts, m):
    return [Part(p.kind, _xd(p.d, m), dict(p.attrs)) for p in parts]


def derived(name, base_fn, base_name, m, transform, description, tags, aliases=()):
    icon(name, CAT, description, tags=tags, aliases=aliases)(lambda S: _xparts(base_fn(S), m))
    REGISTRY[-1].derived_from = {"name": base_name, "transform": transform}


def _affine(deg=0.0, k=1.0, tx=0.0, ty=0.0):
    """Rotate by deg and scale by k about the centre, then shift."""
    a = math.radians(deg)
    c, sn = math.cos(a) * k, math.sin(a) * k
    return (c, sn, -sn, c, 12 - c * 12 + sn * 12 + tx, 12 - sn * 12 - c * 12 + ty)


def heart_d(cx, cy, w):
    """Heart of width w centred on (cx, cy) (outline centre line)."""
    k = w / 16.0
    return "".join(ch for ch in _xd("M12 20L4.4 12.6A4.6 4.6 0 0 1 11 6.3L12 7.3L13 6.3A4.6 4.6 0 0 1 19.6 12.6Z",
                                    (k, 0, 0, k, cx - 12 * k, cy - 13 * k)))


# ============================================================================ open hands

def _open_hand(S, dx=0.0):
    xs = [6.3, 9.7, 13.1, 16.5]
    tops = [7, 5, 5.5, 7.5]
    fingers = [cap(x + dx, t, x + dx, 13) for x, t in zip(xs, tops)]
    palm = box(4.6 + dx, 12, 13.6, 9, wr(S))
    thumb = cap(6 + dx, 17.5, 3.6 + dx, 13.5)
    parts = [outline(*fingers, palm, thumb)]
    for k in range(3):
        xm = (xs[k] + xs[k + 1]) / 2 + dx
        parts.append(detail(seg(xm, max(tops[k], tops[k + 1]) + 1.7, xm, 12.5)))
    return parts


@icon("hand-stop", CAT, "A raised flat palm with the fingers together; stop", tags=["stop", "halt", "palm", "wait", "block", "raised hand"])
def _(S):
    return _open_hand(S, 1.3)


@icon("hand-wave", CAT, "A tilted open hand with motion marks; waving hello", tags=["wave", "hello", "hi", "goodbye", "greeting", "bye"],
      aliases=["hello"])
def _(S):
    parts = _xparts(_open_hand(S, 0.5), _affine(-18, 0.9, -1, 1.5))
    return parts + [line("M16.5 3.5C18.3 3.9 19.7 5.1 20.4 6.8"), line("M16 6.5C16.9 6.8 17.6 7.4 17.9 8.2")]


# ============================================================================ pointing

def _point_up(S):
    """Back of a hand with the index finger raised."""
    idx = cap(8.5, 13, 8.5, 4.6)
    fist = box(6.8, 11, 11.6, 10, wr(S))
    knuck = [cap(12, 12.6, 12, 12.6), cap(15.4, 12.8, 15.4, 12.8)]
    thumb = cap(7.2, 17.5, 4.2, 14)
    return [outline(idx, fist, *knuck, thumb), detail(seg(7.8, 17.2, 12, 17.2))]


@icon("hand-point-up", CAT, "A hand pointing up with the index finger", tags=["point", "up", "finger", "index", "above", "direction"],
      aliases=["point-up"])
def _(S):
    return _point_up(S)


derived("hand-point-down", _point_up, "hand-point-up", (-1, 0, 0, -1, 24, 24), "rotate(180 12 12)",
        "A hand pointing down with the index finger", tags=["point", "down", "finger", "index", "below", "direction"],
        aliases=["point-down"])


def _point_right(S):
    """Back of a hand seen from the side, index finger pointing right."""
    idx = cap(10, 9.5, 19.3, 9.5, 3.2)
    curled = [cap(10, 12.9, 14, 12.9), cap(10, 16.3, 13.4, 16.3), cap(10, 19.4, 12.6, 19.4, 2.8)]
    back = box(7, 7.9, 5.5, 13, 1)
    thumb = cap(8.5, 8.2, 12.8, 6.2, 2.8)
    cuff = box(3, 8.5, 2.5, 12, 0.5 if S.name == "line" else 1.25)
    return [outline(idx, back, *curled, thumb), outline(cuff),
            detail(seg(11.5, 11.2, 14.5, 11.2)), detail(seg(11.5, 14.6, 14.5, 14.6)), detail(seg(11.5, 17.9, 13.5, 17.9))]


@icon("hand-point-right", CAT, "A hand pointing right with the index finger", tags=["point", "right", "finger", "index", "next", "direction"],
      aliases=["point-right"])
def _(S):
    return _point_right(S)


derived("hand-point-left", _point_right, "hand-point-right", MIRROR_X, "matrix(-1 0 0 1 24 0)",
        "A hand pointing left with the index finger", tags=["point", "left", "finger", "index", "back", "direction"],
        aliases=["point-left"])


# ============================================================================ thumbs

def _thumbs_up(S):
    thumb = cap(9, 11, 9, 4.7, 3.6)
    rows = [cap(9.5, y, 18, y, 3.2) for y in (12.4, 15.6)] + [cap(9.5, 18.8, 17, 18.8, 3.2)]
    fist = box(7, 10.8, 8, 9.6, 1.5)
    cuff = box(3, 10.8, 3.5, 9.6, 0.5 if S.name == "line" else 1.5)
    return [outline(thumb, fist, *rows), outline(cuff),
            detail(seg(12, 14, 17, 14)), detail(seg(12, 17.2, 16.5, 17.2)), detail(seg(10.9, 10.8, 13, 10.8))]


@icon("thumbs-up", CAT, "A thumbs-up hand; like or approve", tags=["like", "approve", "good", "yes", "agree", "upvote"],
      aliases=["thumb-up"])
def _(S):
    return _thumbs_up(S)


derived("thumbs-down", _thumbs_up, "thumbs-up", (-1, 0, 0, -1, 24, 24), "rotate(180 12 12)",
        "A thumbs-down hand; dislike or reject", tags=["dislike", "reject", "bad", "no", "disagree", "downvote"],
        aliases=["thumb-down"])


# ============================================================================ finger signs (front view, palm out)

def _sign(S, up, curled_x, thumb):
    """up: [(x, tip_y, lean)] raised fingers; curled_x: x centres of folded fingers; thumb: capsule ends."""
    regs = [box(5.5, 12, 13, 9, wr(S))]
    for x, t, lean in up:
        regs.append(cap(x, 13, x + lean, t))
    for x in curled_x:
        regs.append(cap(x, 12.8, x, 12.8))
    regs.append(cap(*thumb))
    return regs


@icon("hand-peace", CAT, "A hand making a V sign; peace or victory", tags=["peace", "victory", "v sign", "two", "fingers", "win"],
      aliases=["victory", "v-sign"])
def _(S):
    return [outline(*_sign(S, [(8.2, 4.8, -1.5), (11.6, 4.8, 1.5)], [15, 17.2], (6.5, 17, 12.5, 16))), detail(seg(7, 16.2, 12.5, 16.2))]


@icon("hand-rock", CAT, "A hand making the horns sign with the index and little fingers", tags=["rock", "metal", "horns", "concert", "music", "party"],
      aliases=["rock-on", "horns"])
def _(S):
    return [outline(*_sign(S, [(7.2, 4.8, -0.7), (16.8, 5.8, 0.7)], [10.4, 13.6], (6.5, 17, 12.5, 16))), detail(seg(7, 16.2, 12.5, 16.2))]


@icon("hand-call-me", CAT, "A hand with the thumb and little finger out; call me", tags=["call me", "shaka", "hang loose", "phone", "surf", "aloha"],
      aliases=["shaka", "hang-loose"])
def _(S):
    palm = box(7.5, 11, 10.5, 10, wr(S))
    knuck = [cap(x, 11.8, x, 11.8) for x in (9.2, 12.6)]
    pinky = cap(16.3, 13, 18.6, 5.8, 3.2)
    thumb = cap(8.5, 16.5, 4, 10.5)
    return [outline(palm, *knuck, pinky, thumb), detail(seg(10.9, 12.5, 10.9, 14)), detail(seg(14.3, 11, 14.3, 14))]


@icon("hand-ok", CAT, "A hand making the OK sign", tags=["ok", "okay", "perfect", "fine", "agree", "good"],
      aliases=["okay-hand"])
def _(S):
    ring = D(P(circle(7.6, 10, 4.5)), P(circle(7.6, 10, 2.1)))
    fingers = [cap(12.3, 13, 12.3, 5), cap(15.7, 13, 15.7, 5.5), cap(19.1, 13, 19.1, 7)]
    palm = box(8, 12, 12.8, 9, wr(S))
    return [outline(ring, palm, *fingers), detail(seg(14, 7.2, 14, 12.5)), detail(seg(17.4, 8.7, 17.4, 12.5))]


@layered("hand-crossed-fingers", "A hand with the index and middle fingers crossed; good luck",
         tags=["fingers crossed", "luck", "hope", "wish", "promise", "superstition"], aliases=["fingers-crossed", "good-luck"], gap=1.0)
def _(S):
    front = [outline(cap(9, 12.5, 14, 5.6))]
    back = [outline(box(6, 12, 12, 9, wr(S)), cap(13, 13, 8.8, 5), cap(16.2, 12.8, 16.2, 12.8, 3.2), cap(7, 17, 12.5, 16)),
            detail(seg(7.5, 16.2, 12.5, 16.2))]
    return [front, back]


# ============================================================================ two hands

def _mitten(x0, y0, x1, y1, w=5.6):
    """Flat hand seen edge-on: straight wrist, rounded fingertips."""
    return U(ST(seg(x0, y0, x1, y1), w, "butt", "miter"), P(circle(x1, y1, w / 2)))


@layered("clap", "Two hands clapping", tags=["clap", "applause", "bravo", "congrats", "praise", "well done"],
         aliases=["applause"], gap=1.0)
def _(S):
    right = [outline(_mitten(17, 21, 13.4, 7.5), cap(16.8, 15.5, 19.5, 12, 2.8))]
    left = [outline(_mitten(7, 21, 10.6, 7.5), cap(7.2, 15.5, 4.5, 12, 2.8))]
    marks = [line(seg(4, 3, 6.3, 5.3)), line(seg(20, 3, 17.7, 5.3))]
    return [right + marks, left]


@icon("pray", CAT, "Two palms pressed together; pray, please or thank you", tags=["pray", "please", "thanks", "hope", "namaste", "gratitude"],
      aliases=["namaste", "please"])
def _(S):
    d = ("M12 3C10 4.5 9 7.5 8.8 11L6 16V21H18V16L15.2 11C15 7.5 14 4.5 12 3Z" if S.name == "line" else
         "M12 3C10 4.5 9 7.5 8.8 11L6.4 15.3Q6 16 6 17V19Q6 21 8 21H16Q18 21 18 19V17Q18 16 17.6 15.3L15.2 11C15 7.5 14 4.5 12 3Z")
    return [shell(d), detail(seg(12, 5, 12, 21)), detail(seg(6, 17, 9.5, 17)), detail(seg(14.5, 17, 18, 17))]


def _fist_side(S, x=3.0, y=7.0, w=7.5, h=10.5):
    """Side view of a fist: knuckle bumps to the right, thumb folded across the top."""
    rh = (h - 3.2) / 3
    rows = [cap(x + 2, y + 3.2 + rh * (k + 0.5), x + w - rh / 2, y + 3.2 + rh * (k + 0.5), rh) for k in range(3)]
    body = box(x, y, w - 1.5, h, 1.5 if S.name == "line" else 2.5)
    thumb = cap(x + 1.5, y + 1.6, x + w - 1.8, y + 1.6, 3.2)
    seps = [detail(seg(x + w - 3.2, y + 3.2 + rh * k, x + w, y + 3.2 + rh * k)) for k in (1, 2)]
    return [outline(body, thumb, *rows), detail(seg(x + 1.5, y + 3.2, x + w - 1, y + 3.2))] + seps


@icon("fist-bump", CAT, "Two fists bumping knuckles", tags=["fist bump", "bro", "team", "respect", "greeting", "power"],
      aliases=["knuckle-bump"])
def _(S):
    left = _fist_side(S)
    return left + _xparts(left, MIRROR_X) + [line(seg(12, 2.5, 12, 5)), line(seg(12, 19, 12, 21.5))]


@icon("hand-grab", CAT, "A hand gripping a bar", tags=["grab", "grip", "hold", "handle", "grasp", "carry"],
      aliases=["grip"])
def _(S):
    knuck = [cap(x, 9, x, 9) for x in (7, 10.4, 13.8, 17.2)]
    fist = box(5.3, 9, 13.6, 12, wr(S))
    return [outline(*knuck, fist), detail(seg(5.3, 13.5, 18.9, 13.5)), detail(seg(8.7, 9, 8.7, 11.5)), detail(seg(12.1, 9, 12.1, 11.5)),
            detail(seg(15.5, 9, 15.5, 11.5)), line(seg(2.5, 13.5, 4.3, 13.5)), line(seg(19.9, 13.5, 21.5, 13.5))]


@icon("hand-pinch", CAT, "A thumb and index finger pinching something small", tags=["pinch", "zoom", "gesture", "touch", "squeeze", "small"],
      aliases=["pinch"])
def _(S):
    back = box(3, 7, 7, 12, wr(S))
    idx = cap(7, 8.4, 17.3, 8.4, 3.2)
    thumb = cap(7, 16.6, 17.3, 16.6, 3.2)
    return [outline(back, idx, thumb), dot(18, 12.5, 1.25)]


# ============================================================================ touch gestures (index finger up, smaller)

def _touch_hand(S, tx=3.5, k=0.8):
    return _xparts(_point_up(S), (k, 0, 0, k, tx, 21 - 21 * k))


@icon("hand-swipe", CAT, "A finger swiping sideways", tags=["swipe", "slide", "scroll", "touch", "gesture", "drag"],
      aliases=["swipe"])
def _(S):
    y = 6.5
    return _touch_hand(S) + [line(seg(2.5, y, 7, y)), line(poly([(5.3, y - 2.8), (2.5, y), (5.3, y + 2.8)], r=S.r * 0.4)),
                             line(seg(14, y, 21, y)), line(poly([(18.2, y - 2.8), (21, y), (18.2, y + 2.8)], r=S.r * 0.4))]


@icon("hand-tap", CAT, "A finger tapping with ripples", tags=["tap", "touch", "press", "gesture", "select", "touchscreen"],
      aliases=["finger-tap"])
def _(S):
    k = 0.74
    hx, ty = 4 + 8.5 * k, 21 - 21 * k + 4.6 * k
    return _touch_hand(S, 4, k) + [line(arc(hx, ty, 3.9, 215, 325)), line(arc(hx, ty, 6.4, 220, 320))]


@icon("hand-click", CAT, "A pointing finger with click marks", tags=["click", "press", "cursor", "select", "tap", "button"])
def _(S):
    hx = 3.5 + 8.5 * 0.8
    ty = 21 - 21 * 0.8 + 4.6 * 0.8
    ticks = []
    for a in (-160, -90, -20):
        p0, p1 = polar(hx, ty, 4.5, a), polar(hx, ty, 7, a)
        ticks.append(line(seg(*p0, *p1)))
    return _touch_hand(S) + ticks


# ============================================================================ hands holding things

def _palm_up(S):
    """A hand held out palm up from the left, fingertips curling up on the right."""
    wrist = box(2.5, 15, 7, 6.5, wr(S))
    fingers = [cap(8, 19.2, 17.5, 19.2, 3.2), cap(17.5, 19.2, 19.8, 16.8, 3.2)]
    thumb = cap(8, 16.6, 11.3, 14.4, 2.8)
    return [outline(wrist, *fingers, thumb)]


@icon("hand-heart", CAT, "An open hand holding up a heart; care or charity", tags=["care", "charity", "love", "kindness", "donate", "support"],
      aliases=["care", "charity"])
def _(S):
    return _palm_up(S) + [shell(heart_d(12.5, 8.3, 11.5), stroke_miterlimit="2")]


@layered("hand-coins", "An open hand holding coins; pay or earn", tags=["coins", "money", "pay", "payment", "earn", "salary"],
         aliases=["pay"], gap=1.0)
def _(S):
    return [_palm_up(S) + [shell(rect(8, 3, 8, 9.5, min(S.R, 2))), detail(seg(8, 6.2, 16, 6.2)), detail(seg(8, 9.3, 16, 9.3))]]


@layered("hand-write", "A hand writing with a pen", tags=["write", "sign", "signature", "pen", "handwriting", "note"],
         aliases=["handwriting"], gap=1.0)
def _(S):
    pen = poly([(3.5, 20.5), (4.5, 17), (13, 8.5), (15.5, 11), (7, 19.5)], closed=True, r=S.r * 0.3)
    return [_fist_side(S, 12.5, 4, 8, 10), [shell(pen, stroke_miterlimit="2")]]


# ============================================================================ deal

@layered("hand-shake-deal", "Two hands clasped under burst marks; a deal is sealed", tags=["deal", "agreement", "contract", "partnership", "handshake", "success"],
         aliases=["deal"], gap=1.0)
def _(S):
    k = 0.5 if S.name == "line" else 1.5
    dy = 2.5
    thumb = [outline(cap(18, 9.8 + dy, 11, 7 + dy, 3))]
    left = U(box(2.5, 9.5 + dy, 7, 7, k), box(7, 8.5 + dy, 10.5, 9, 3))
    front = [outline(left), detail(seg(5.5, 9.5 + dy, 5.5, 16.5 + dy)),
             detail(seg(10.3, 17.5 + dy, 11.1, 14.3 + dy)), detail(seg(13.1, 17.5 + dy, 13.9, 14.3 + dy)), detail(seg(15.8, 17.5 + dy, 16.3, 15 + dy))]
    back = [outline(box(14, 10 + dy, 7.5, 7, k)), detail(seg(18.5, 10 + dy, 18.5, 17 + dy))]
    burst = [line(seg(6, 3, 7.5, 5.5)), line(seg(3.5, 7, 6, 8)), line(seg(20.5, 3.5, 19, 6))]
    return [thumb + burst, front, back]
