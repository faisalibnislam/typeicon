"""TypeIcon Core: activities (batch 005).

Everyday actions drawn as small scenes. Figures follow the people and sports athletes (head dot r 2.25,
2 px limbs). Hands follow the gestures set (finger capsules unioned into one outlined shell).
Overlapping objects are drawn in layers (front first): back layers are cut away around the front
silhouette with a gap in every style, so the scenes stay readable at 16 px.
"""
import math

from dsl import LINE, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from dsl import D, P, ST, U, filled_region
from geometry import fmt, path_to_d, polar

CAT = "activities"


# --------------------------------------------------------------------------- helpers

def pick(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def cap(x0, y0, x1, y1, w=3.4):
    """Finger or limb region: a capsule along a segment."""
    return ST(seg(x0, y0, x1, y1), w, "round", "round")


def box(x, y, w, h, r=0.0):
    return P(rect(x, y, w, h, r))


def mitten(x0, y0, x1, y1, w=4.6):
    """Flat hand seen edge-on: straight wrist at (x0, y0), rounded fingertips at (x1, y1)."""
    return U(ST(seg(x0, y0, x1, y1), w, "butt", "miter"), P(circle(x1, y1, w / 2)))


def outline(*regions, **attrs):
    return shell(path_to_d(U(*regions)), **attrs)


def tilted_ellipse(cx, cy, rx, ry, deg):
    """Ellipse whose ry axis points along deg (0 = right, 90 = down)."""
    a = math.radians(deg)
    ux, uy = math.cos(a), math.sin(a)
    p1 = (cx + ry * ux, cy + ry * uy)
    p2 = (cx - ry * ux, cy - ry * uy)
    rot = deg
    return (f"M{fmt(p1[0])} {fmt(p1[1])}A{fmt(ry)} {fmt(rx)} {fmt(rot)} 1 0 {fmt(p2[0])} {fmt(p2[1])}"
            f"A{fmt(ry)} {fmt(rx)} {fmt(rot)} 1 0 {fmt(p1[0])} {fmt(p1[1])}Z")


def arrow_head(tip, deg, S, size=2.5):
    """Open chevron arrowhead at tip, pointing along deg."""
    a = polar(tip[0], tip[1], size * 1.2, deg + 180 - 45)
    b = polar(tip[0], tip[1], size * 1.2, deg + 180 + 45)
    return line(poly([a, tip, b], r=S.r * 0.4))


def bust(S, cx=12.0, top=14.0, hw=7.0, bottom=21.0):
    """Open-bottom shoulders, as in the people set. Line has squarer shoulders than Rounded."""
    r = hw - (1.0 if S.name != "line" else 2.0)
    r = min(r, bottom - top)
    x0, x1 = cx - hw, cx + hw
    return (f"M{fmt(x0)} {fmt(bottom)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + r)} {fmt(top)}"
            f"H{fmt(x1 - r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(bottom)}")


# ---- layering: back parts are cut away around the front silhouette (all styles)

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


def scene(name, desc, tags, aliases=(), gap=1.5):
    """Register an icon drawn as layers: fn(S) -> [front layer, layer behind, ...]."""
    def deco(fn):
        icon(name, CAT, desc, tags=tags, aliases=aliases,
             filled=lambda: _filled_layers(fn(LINE), gap))(lambda S: _stroke_layers(S, fn(S), gap))
        return fn
    return deco




# ---- transforms

def _xd(d, m):
    """Apply an affine matrix (a, b, c, d, e, f) to a path string."""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.svgLib.path import parse_path
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def xparts(parts, m):
    return [Part(p.kind, _xd(p.d, m), dict(p.attrs)) for p in parts]


def place(k, deg, src, dst):
    """Matrix: scale by k and rotate by deg (clockwise on screen) about src, then move src to dst."""
    a = math.radians(deg)
    c, s = math.cos(a) * k, math.sin(a) * k
    return (c, s, -s, c, dst[0] - c * src[0] + s * src[1], dst[1] - s * src[0] - c * src[1])


def point_hand(S):
    """Back of a hand with the index finger raised (fingertip at 8.5, 2.9), as in the gestures set."""
    wr = pick(S, 0.5, 2.5)
    idx = cap(8.5, 13, 8.5, 4.6)
    fist = box(6.8, 11, 11.6, 10, wr)
    knuck = [cap(12, 12.6, 12, 12.6), cap(15.4, 12.8, 15.4, 12.8)]
    thumb = cap(7.2, 17.5, 4.2, 14)
    return [outline(idx, fist, *knuck, thumb), detail(seg(7.8, 17.2, 12, 17.2))]


def thumbs_up(S):
    """Thumbs-up fist with its cuff, as in the gestures set (x 3 to 19.6, y 2.9 to 20.6)."""
    thumb = cap(9, 11, 9, 4.7, 3.6)
    rows = [cap(9.5, y, 18, y, 3.2) for y in (12.4, 15.6)] + [cap(9.5, 18.8, 17, 18.8, 3.2)]
    fist = box(7, 10.8, 8, 9.6, 1.5)
    cuff = box(3, 10.8, 3.5, 9.6, pick(S, 0.5, 1.5))
    return [outline(thumb, fist, *rows), outline(cuff),
            detail(seg(12, 14, 17, 14)), detail(seg(12, 17.2, 16.5, 17.2)), detail(seg(10.9, 10.8, 13, 10.8))]


def open_hand(S):
    """Open palm, fingers up, as in the gestures set (x 2.8 to 18.2, y 3.3 to 21; middle fingertip at 9.7, 3.3)."""
    xs = [6.3, 9.7, 13.1, 16.5]
    tops = [7, 5, 5.5, 7.5]
    fingers = [cap(x, t, x, 13) for x, t in zip(xs, tops)]
    palm = box(4.6, 12, 13.6, 9, pick(S, 0.5, 2.5))
    thumb = cap(6, 17.5, 3.6, 13.5)
    parts = [outline(*fingers, palm, thumb)]
    for k in range(3):
        xm = (xs[k] + xs[k + 1]) / 2
        parts.append(detail(seg(xm, max(tops[k], tops[k + 1]) + 1.7, xm, 12.5)))
    return parts


def flat_hand(S, wrist, tip, w=5.0, thumb_at=5.0, thumb_len=4.0, side=1):
    """Flat hand seen edge-on (as in the gestures clap): a mitten with the thumb sticking out on one side."""
    ux, uy = tip[0] - wrist[0], tip[1] - wrist[1]
    n = math.hypot(ux, uy)
    ux, uy = ux / n, uy / n
    nx, ny = -uy * side, ux * side
    b = (wrist[0] + ux * thumb_at + nx * (w / 2 - 1.2), wrist[1] + uy * thumb_at + ny * (w / 2 - 1.2))
    t = (b[0] + (ux * 0.55 + nx * 0.85) * thumb_len, b[1] + (uy * 0.55 + ny * 0.85) * thumb_len)
    return outline(mitten(wrist[0], wrist[1], tip[0], tip[1], w), cap(b[0], b[1], t[0], t[1], 2.8))


# ============================================================================ chunk 1

@scene("tapping-shoulder", "A hand tapping the shoulder of a person seen from behind.",
       tags=["tap", "shoulder", "attention", "excuse me", "nudge", "touch"])
def _(S):
    hand = [flat_hand(S, (21, 3), (14.5, 11), 4.4, 4, 3, -1)]
    marks = [line(seg(16.5, 14, 18.5, 15)), line(seg(14.5, 16, 15.5, 18))]
    person = [shell(circle(7.5, 7.5, 3.5)), shell(bust(S, 7.5, 14, 5.5, 21))]
    return [hand + marks, person]


@scene("walking-bicycle", "A person walking beside a bicycle and holding its handlebar.",
       tags=["bike", "push", "walk", "cyclist", "dismount", "bicycle"])
def _(S):
    bike = [line(circle(5, 18.5, 3)), line(circle(19, 18.5, 3)),
            line(poly([(5, 18.5), (7.5, 12.5), (16.5, 12.5), (19, 18.5)], r=S.r)),
            line(poly([(16.5, 12.5), (16, 9.5), (18.5, 9.5)], r=S.r))]
    person = [dot(11.5, 3.5, 2.25),
              line(poly([(11.5, 7), (14, 10), (16, 9.5)], r=S.r)),
              line(seg(11.5, 7, 12, 14)),
              line(poly([(10, 21.5), (12, 14), (14, 21.5)], r=S.r))]
    return [person, bike]


@icon("reading-map", CAT, "A standing person holding an unfolded map up in front of them.",
      tags=["map", "navigate", "tourist", "lost", "directions", "explore", "travel"])
def _(S):
    m = [(3, 7.5), (8.5, 9), (15.5, 7.5), (21, 9), (21, 15), (15.5, 13.5), (8.5, 15), (3, 13.5)]
    return [dot(12, 3.5, 2.25),
            shell(poly(m, closed=True, r=S.r * 0.5)),
            detail(seg(8.5, 9, 8.5, 15)), detail(seg(15.5, 7.5, 15.5, 13.5)),
            line(seg(10.5, 17.5, 10, 21.5)), line(seg(13.5, 17.5, 14, 21.5))]


@icon("looking-in-fridge", CAT, "A person bending toward an open refrigerator to look inside.",
      tags=["fridge", "refrigerator", "snack", "hungry", "kitchen", "food", "midnight snack"])
def _(S):
    body = [(14, 3), (19, 3), (21.5, 5), (21.5, 19), (19, 21), (14, 21)]
    return [shell(poly(body, closed=True, r=S.r * 0.6)),
            detail(seg(19, 3, 19, 21)),
            detail(seg(14, 9, 19, 9)), detail(seg(14, 15, 19, 15)),
            dot(9.5, 5.5, 2.25),
            line(seg(5, 13.5, 8.5, 9.5)),
            line(poly([(8.5, 9.5), (11.5, 12.5)], r=S.r)),
            line(poly([(3.5, 21.5), (5, 13.5), (7, 21.5)], r=S.r))]


@scene("tidying-toys", "A person dropping a toy block into a toy box with a teddy bear inside.",
       tags=["tidy up", "toys", "clean up", "toy box", "kids room", "chores", "put away"])
def _(S):
    toybox = [shell(rect(10, 13.5, 11.5, 8, min(S.R, 2))), detail(seg(10, 16.5, 21.5, 16.5))]
    bear = [outline(P(circle(16.5, 10.5, 2.75)), P(circle(14.2, 8.2, 1.4)), P(circle(18.8, 8.2, 1.4)))]
    kid = [dot(4.5, 4.5, 2.25),
           line(seg(4.5, 7.5, 4.5, 14)),
           line(poly([(4.5, 9), (7, 9.5)], r=S.r)),
           line(poly([(2.5, 21.5), (4.5, 14), (7, 21.5)], r=S.r)),
           sq(7.5, 7.5, 3.5, 3.5, pick(S, 0, 0.8))]
    return [toybox, bear, kid]


@scene("blowing-up-balloon", "A face in profile with a puffed cheek blowing into a balloon.",
       tags=["balloon", "inflate", "blow", "party", "birthday", "celebration"])
def _(S):
    balloon = [shell(tilted_ellipse(15.5, 8, 5, 6, -40)), detail(arc(15.5, 8, 3, 200, 260)),
               outline(cap(11.8, 13.8, 11, 14.8, 2.6))]
    head = [outline(P(circle(5.5, 16, 4)), P(circle(8.3, 17.3, 2.4))), dot(6, 14.2, 1)]
    return [balloon, head]


@scene("recording-voice-message", "A person holding a phone near their mouth to record a voice message.",
       tags=["voice message", "voice note", "record", "phone", "audio message", "dictate", "speak"])
def _(S):
    phone = [shell(rect(15, 5, 6.5, 12, min(S.R, 2))), dot(18.25, 11, 1.6)]
    waves = [line(arc(10.5, 11, 2, -45, 45))]
    person = [shell(circle(7, 7.5, 3.5)), shell(bust(S, 7, 14, 5, 21))]
    return [phone + waves, person]


@scene("sign-language-thank-you", "Sign for thank you: a flat hand moving forward and down from the chin.",
       tags=["sign language", "thank you", "thanks", "asl", "deaf", "gratitude", "signing"])
def _(S):
    hand = [flat_hand(S, (17.5, 20.5), (10.5, 12), 5, 5, 3.2, 1)]
    arrow = [line(arc(15, 9.5, 5, -95, -10)), arrow_head(polar(15, 9.5, 5, -10), 80, S, 2.2)]
    head = [shell(circle(6, 6, 3.5))]
    return [hand + arrow, head]


@scene("sign-language-please", "Sign for please: a flat palm on the chest with a circling arrow.",
       tags=["sign language", "please", "asl", "deaf", "polite", "request", "signing"])
def _(S):
    hand = [flat_hand(S, (17.5, 16.5), (7, 16.5), 5, 4.5, 3.2, 1)]
    ring = [line(arc(18, 6, 3, -60, 210)), arrow_head(polar(18, 6, 3, -60), 30, S, 2)]
    person = [shell(circle(10, 5, 3)), shell(bust(S, 11, 11.5, 9, 21.5))]
    return [hand, ring, person]


@scene("sign-language-help", "Sign for help: a thumbs-up fist resting on a flat palm, lifted upward.",
       tags=["sign language", "help", "assist", "asl", "deaf", "support", "signing"])
def _(S):
    fist = xparts(thumbs_up(S), (0.72, 0, 0, 0.72, -0.5, 0.2))
    palm = [outline(mitten(16.5, 18.5, 3.5, 18.5, 4))]
    arrow = [line(seg(19.5, 21, 19.5, 4.5)), arrow_head((19.5, 4), -90, S)]
    return [fist + arrow, palm]


@icon("fist-pump", CAT, "A person pulling a clenched fist down in celebration.",
      tags=["yes", "victory", "celebrate", "win", "success", "cheer", "nailed it"])
def _(S):
    return [dot(9.5, 4.5, 2.25),
            line(poly([(4.5, 14.5), (6.5, 9.5), (12.5, 9.5), (14.5, 14), (16.5, 11)], r=S.r)),
            line(seg(9.5, 9.5, 9.5, 14.5)),
            line(poly([(6.5, 21.5), (9.5, 14.5), (12.5, 21.5)], r=S.r)),
            dot(17, 9.3, 2.1),
            line(seg(15, 5.5, 14.3, 4)), line(seg(18.5, 5.3, 19.3, 3.8)), line(seg(20.5, 8.3, 22, 7.8))]


@icon("stomping", CAT, "A person stamping one foot down hard with impact lines at the heel.",
      tags=["stomp", "stamp", "angry", "foot", "tantrum", "march", "frustrated"])
def _(S):
    return [dot(9, 4, 2.25),
            line(poly([(5.5, 13), (6.5, 9), (11.5, 9), (12.5, 13)], r=S.r)),
            line(seg(9, 9, 9, 14)),
            line(seg(9, 14, 7, 21.5)),
            line(poly([(9, 14), (13, 16.5), (13, 21), (17, 21)], r=S.r)),
            line(seg(18.5, 19, 20.5, 18)), line(seg(16.5, 17, 17.5, 15)), line(seg(19, 21.5, 21.5, 21.5))]


@icon("toddler-tantrum", CAT, "A small child lying on its back kicking and waving its fists.",
      tags=["tantrum", "toddler", "meltdown", "screaming", "angry child", "parenting", "terrible twos"])
def _(S):
    return [dot(4.5, 16.5, 2.5),
            line(seg(8, 17.5, 13.5, 17.5)),
            line(poly([(13.5, 17.5), (16, 12), (18.5, 11)], r=S.r)),
            line(poly([(13.5, 17.5), (19, 16), (21, 13)], r=S.r)),
            line(poly([(9.5, 17.5), (10.5, 13), (9, 10.5)], r=S.r)),
            dot(8.8, 9.8, 1.6),
            line(poly([(3, 9), (4.5, 6.5), (6, 9), (7.5, 6.5)], r=S.r * 0.3)),
            line(poly([(12.5, 6), (14, 3.5), (15.5, 6), (17, 3.5)], r=S.r * 0.3)),
            line(seg(2, 21.5, 22, 21.5))]


def _walker(S, k=0.72, dx=0.0, oy=2.0):
    """The walking figure of the people set, scaled about (12, oy)."""
    def t(p):
        return (12 + (p[0] - 12) * k + dx, oy + (p[1] - oy) * k)
    return [dot(*t((13.5, 4.5)), 2.25 * max(k, 0.9)),
            line(poly([t(p) for p in [(8.5, 13.5), (10.5, 10), (12.5, 9.5), (14.5, 12), (17, 13)]], r=S.r)),
            line(seg(*t((12.5, 9.5)), *t((11, 15)))),
            line(poly([t(p) for p in [(7.5, 21), (11, 15), (14, 17.5), (14.5, 21)]], r=S.r))]


@icon("pacing", CAT, "A walking person above a curved two-way arrow showing a back-and-forth path.",
      tags=["pace", "back and forth", "restless", "nervous", "waiting", "walk", "anxious"])
def _(S):
    return _walker(S) + [
        line("M5 17.5Q12 23 19 17.5"),
        arrow_head((4.5, 17), 215, S, 2.2), arrow_head((19.5, 17), -35, S, 2.2)]


@scene("biting-nails", "A worried face with fingertips held between the teeth.",
       tags=["nervous", "anxious", "worried", "nail biting", "stress", "suspense", "fear"])
def _(S):
    hand = [outline(cap(10.3, 15.5, 10.3, 21, 3.4), cap(13.7, 15.5, 13.7, 21, 3.4)), detail(seg(12, 17.5, 12, 21))]
    face = [shell(circle(12, 11, 8.5)), dot(9, 10, 1.2), dot(15, 10, 1.2),
            detail(seg(7, 6.8, 10, 5.8)), detail(seg(14, 5.8, 17, 6.8)),
            detail(seg(8.5, 14, 15.5, 14))]
    return [hand, face]


# ============================================================================ chunk 2

def car_side(S, dx=0.0):
    """Small car in side view facing right (x 9.5 to 21.5 before the shift): body and two wheels."""
    body = [(9.5, 17.5), (9.5, 12.5), (12, 12), (13.5, 7.5), (18.5, 7.5), (20.5, 12), (21.5, 12.5), (21.5, 17.5)]
    body = [(x + dx, y) for x, y in body]
    return ([shell(circle(12.5 + dx, 18.5, 2)), shell(circle(18.5 + dx, 18.5, 2))],
            [shell(poly(body, closed=True, r=S.r * 0.6))])


@scene("pushing-car", "A person leaning forward and pushing a small car from behind.",
       tags=["push", "car", "breakdown", "stalled", "out of fuel", "help", "flat battery"])
def _(S):
    wheels, body = car_side(S)
    person = [dot(6.5, 6.5, 2.25),
              line(poly([(3.5, 15), (6, 10), (8.5, 12.5)], r=S.r)),
              line(poly([(2, 21.5), (3.5, 15), (6.5, 18), (6.5, 21.5)], r=S.r))]
    return [person, wheels, body]


@icon("arm-in-arm", CAT, "Two people walking side by side with their elbows linked.",
      tags=["arm in arm", "linked arms", "together", "friends", "couple", "companions", "stroll"])
def _(S):
    return [dot(6, 4.5, 2.25), line(seg(6, 7.5, 6, 14)),
            line(poly([(6, 9), (11, 13), (14, 11)], r=S.r)),
            line(seg(6, 9, 3.5, 13)),
            line(poly([(3.5, 21.5), (6, 14), (8, 21.5)], r=S.r)),
            dot(18, 4.5, 2.25), line(seg(18, 7.5, 18, 14)),
            line(poly([(18, 9), (13, 13), (10, 11)], r=S.r)),
            line(seg(18, 9, 20.5, 13)),
            line(poly([(16, 21.5), (18, 14), (20.5, 21.5)], r=S.r))]


@icon("taping-box", CAT, "A tape roll sealing the top seam of a closed cardboard box.",
      tags=["packing tape", "seal", "box", "moving", "shipping", "parcel", "packing"])
def _(S):
    sil = [(2.5, 12), (6.5, 8), (19.5, 8), (19.5, 17), (15.5, 21), (2.5, 21)]
    return [shell(poly(sil, closed=True, r=S.r * 0.4)),
            detail(poly([(2.5, 12), (15.5, 12), (15.5, 21)])), detail(seg(15.5, 12, 19.5, 8)),
            detail(seg(4.5, 10, 11, 10)),
            shell(circle(16, 4.5, 2.5))]


@scene("handing-over-keys", "One hand passing a ring of keys into another open hand.",
       tags=["keys", "hand over", "handover", "new home", "rental", "car keys", "move in"])
def _(S):
    keys = [shell(circle(14.5, 7, 2.5)),
            line(poly([(11, 7), (4.5, 7), (4.5, 10)], r=S.r * 0.4)), line(seg(8, 7, 8, 9.5))]
    top = [outline(mitten(21.5, 3.5, 17.5, 6.5, 4))]
    bottom = [outline(box(2.5, 15.5, 7, 6.5, pick(S, 0.5, 2.5)), cap(8, 19.2, 17.5, 19.2, 3.2),
                      cap(17.5, 19.2, 19.8, 16.8, 3.2), cap(8, 16.6, 11.3, 14.6, 2.8))]
    return [top, keys, bottom]


@icon("opening-jar", CAT, "A jar with its lid twisting off and a curved arrow above it.",
      tags=["open", "jar", "lid", "twist", "unscrew", "kitchen", "container"])
def _(S):
    lid = xparts([shell(rect(5.5, 5.5, 9, 3, min(S.R, 1)))], place(1, -12, (10, 7), (10, 7)))
    return [shell(poly([(6, 11.5), (14, 11.5), (15.5, 13.5), (15.5, 21), (4.5, 21), (4.5, 13.5)], closed=True, r=S.r)),
            detail(seg(4.5, 16.5, 15.5, 16.5))] + lid + [
            line(arc(15, 8, 5, -120, 60)), arrow_head(polar(15, 8, 5, 60), 150, S, 2)]


@scene("climbing-tree", "A person sitting astride a branch and hugging the trunk of a leafy tree.",
       tags=["climb", "tree", "treetop", "outdoors", "kids", "adventure", "play"])
def _(S):
    tree = [outline(P(circle(16, 5.5, 3.5)), P(circle(19.5, 8, 2.5)), P(circle(12.5, 7.5, 2.5))),
            line(seg(16, 11, 16, 22)), line(seg(15, 17.5, 9, 15))]
    kid = [dot(8, 9, 2.25),
           line(poly([(9, 12), (13.5, 12.5)], r=S.r)),
           line(poly([(9, 12), (8, 15.5), (11, 19.5)], r=S.r))]
    return [kid, tree]


@scene("carrying-firewood", "A person carrying a stack of split logs in both arms.",
       tags=["firewood", "logs", "wood", "carry", "fireplace", "cabin", "winter"])
def _(S):
    front = [shell(circle(12.5, 13, 2.5)), shell(circle(18.5, 13, 2.5)), dot(12.5, 13, 1), dot(18.5, 13, 1)]
    top = [shell(circle(15.5, 8, 2.5)), dot(15.5, 8, 1)]
    person = [dot(7, 3.5, 2.25),
              line(seg(7, 6.5, 6.5, 14)),
              line(poly([(7, 8), (9, 13), (12.5, 16.5), (18.5, 16.5)], r=S.r)),
              line(poly([(3.5, 21.5), (6.5, 14), (9.5, 21.5)], r=S.r))]
    return [front, top, person]


@icon("giving-up-seat", CAT, "A person offering an empty seat to an older person with a cane.",
      tags=["offer seat", "courtesy", "priority seat", "elderly", "kindness", "public transport", "manners"])
def _(S):
    return [dot(4, 4.5, 2.25),
            line(seg(4, 7.5, 4, 14)), line(poly([(4, 9), (7, 11.5)], r=S.r)),
            line(poly([(2.5, 21.5), (4, 14), (5.5, 21.5)], r=S.r)),
            line(poly([(9, 11), (9, 16.5), (13.5, 16.5)], r=S.r)),
            line(seg(9, 16.5, 9, 21.5)), line(seg(13.5, 16.5, 13.5, 21.5)),
            dot(18, 5, 2.25),
            line("M19.5 8C20.5 10 20.5 12 19.5 14.5"),
            line(poly([(19.5, 9.5), (17.5, 12.5), (16.5, 12.5)], r=S.r)),
            line(seg(16.5, 13.5, 16.5, 21.5)),
            line(poly([(18, 21.5), (19.5, 14.5), (21, 21.5)], r=S.r))]


@icon("beating-rug", CAT, "A person swinging a carpet beater at a rug hanging over a line.",
      tags=["rug", "carpet", "beat", "dust", "spring cleaning", "chores", "clean"])
def _(S):
    return [line(seg(11.5, 4, 22, 4)),
            shell(rect(13.5, 4, 7, 14, min(S.R, 1.5))),
            detail(poly([(17, 8), (18.8, 11), (17, 14), (15.2, 11)], closed=True, r=S.r * 0.3)),
            line(seg(14.5, 20, 14.5, 22)), line(seg(17, 20, 17, 22)), line(seg(19.5, 20, 19.5, 22)),
            dot(4, 6, 2.25),
            line(seg(4, 9, 4, 15)),
            line(poly([(4, 10), (7.5, 8)], r=S.r)),
            line(seg(7.5, 8, 9.5, 5)),
            shell(circle(10.5, 3.5, 1.5)),
            line(poly([(2.5, 21.5), (4, 15), (6, 21.5)], r=S.r)),
            dot(10, 11.5, 1.1), dot(10.5, 15, 1.1)]


@icon("pumping-tire", CAT, "A floor pump with its hose connected to a bicycle wheel.",
      tags=["pump", "tire", "tyre", "inflate", "bike", "air", "flat tire"])
def _(S):
    return [line(seg(2.5, 3.5, 9.5, 3.5)), line(seg(6, 3.5, 6, 7)),
            shell(rect(4.5, 7, 3, 12, min(S.R, 1))),
            line(seg(2.5, 21, 9.5, 21)), line(seg(6, 19, 6, 21)),
            line("M7.5 17C10 17 11 13 14 13.5"),
            line(circle(16.5, 14.5, 5)), dot(16.5, 14.5, 1.5)]


@scene("scraping-windshield", "An ice scraper clearing a stripe across a frosted car windshield.",
       tags=["ice scraper", "frost", "windshield", "windscreen", "winter", "car", "defrost"])
def _(S):
    scraper = [shell(poly([(10.5, 9), (15.5, 9), (15, 12), (11, 12)], closed=True, r=S.r * 0.4)),
               line(seg(13, 12, 13, 21.5))]
    glass = [shell(poly([(5.5, 3.5), (18.5, 3.5), (21.5, 16), (2.5, 16)], closed=True, r=S.r)),
             dot(6.5, 7, 1), dot(5, 12.5, 1), dot(7.5, 13.5, 1), dot(17.5, 7, 1), dot(19, 12.5, 1)]
    return [scraper, glass]


@icon("sign-language-yes", CAT, "Sign for yes: an upright fist nodding forward at the wrist.",
      tags=["sign language", "yes", "agree", "asl", "deaf", "nod", "signing"])
def _(S):
    x, y, w, h = 6.0, 3.5, 9.0, 10.5
    rh = (h - 3.2) / 3
    rows = [cap(x + 2, y + 3.2 + rh * (k + 0.5), x + w - rh / 2, y + 3.2 + rh * (k + 0.5), rh) for k in range(3)]
    body = box(x, y, w - 1.5, h, pick(S, 1.5, 2.5))
    thumb = cap(x + 1.5, y + 1.6, x + w - 1.8, y + 1.6, 3.2)
    arm = box(7, 13, 5.5, 8.5, pick(S, 0.5, 1.5))
    fist = [outline(body, thumb, *rows, arm), detail(seg(x + 1.5, y + 3.2, x + w - 1, y + 3.2))]
    fist += [detail(seg(x + w - 3.2, y + 3.2 + rh * k, x + w, y + 3.2 + rh * k)) for k in (1, 2)]
    fist = xparts(fist, place(1, 20, (10.5, 15), (9.5, 15)))
    return fist + [line(arc(10.5, 15, 10.5, -70, -40)), line(arc(10.5, 15, 10.5, -25, 5))]


@icon("sign-language-no", CAT, "Sign for no: the index and middle fingers snapping shut against the thumb.",
      tags=["sign language", "no", "disagree", "asl", "deaf", "refuse", "signing"])
def _(S):
    hand = outline(box(6, 8, 5.5, 11.5, pick(S, 1, 2)), cap(9, 10.5, 15, 6.5, 4.4), cap(9, 17, 15, 17, 3))
    cuff = outline(box(2.5, 8.5, 2.5, 10.5, pick(S, 0.5, 1.25)))
    return [hand, cuff, line(arc(14.5, 12, 5.5, -40, 30)), arrow_head(polar(14.5, 12, 5.5, 30), 120, S, 2)]
