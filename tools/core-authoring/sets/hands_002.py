"""TypeIcon Core: hands (batch 002): hands holding things, hand actions and a few hand signs.

Hands are regions: fingers are capsules (3.4 wide, the pitch of the gestures set) unioned with a palm and
outlined as one shell, so Filled turns them solid and knocks out the finger separations. Line keeps wrist and
palm corners square, Rounded softens them.

"Something in hand" icons share one palm-up hand held out from the left (the hand of hand-heart and
hand-coins); the object floats above the cupped fingers inside the box x 8-20, y 2-12.

Where a hand overlaps an object the icon is drawn in layers (front first) and what lies behind is cut away
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


def box(x, y, w, h, r=0.0):
    return P(rect(x, y, w, h, r))


def disc(cx, cy, r):
    return P(circle(cx, cy, r))


def region(d):
    return P(d)


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


def rot_pts(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rot_d(d, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return _xd(d, (c, s, -s, c, cx - cx * c + cy * s, cy - cx * s - cy * c))


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


def _grow(reg, g):
    if g <= 0:
        return reg
    return U(reg, ST(path_to_d(reg), 2 * g, "round", "round"))


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

def palm_up(S, dx=0.0, dy=0.0):
    """A hand held out palm up from the left, fingertips curling up on the right."""
    wrist = box(2.5 + dx, 15 + dy, 7, 6.5, wr(S))
    fingers = [cap(8 + dx, 19.2 + dy, 17.5 + dx, 19.2 + dy, 3.2), cap(17.5 + dx, 19.2 + dy, 19.8 + dx, 16.8 + dy, 3.2)]
    thumb = cap(8 + dx, 16.8 + dy, 10.4 + dx, 15.2 + dy, 2.8)
    return [outline(wrist, *fingers, thumb)]


def sparkle_d(cx, cy, r, k=0.28):
    """Four-pointed sparkle (outline centre line)."""
    q = r * k
    return (f"M{fmt(cx)} {fmt(cy - r)}Q{fmt(cx + q)} {fmt(cy - q)} {fmt(cx + r)} {fmt(cy)}"
            f"Q{fmt(cx + q)} {fmt(cy + q)} {fmt(cx)} {fmt(cy + r)}Q{fmt(cx - q)} {fmt(cy + q)} {fmt(cx - r)} {fmt(cy)}"
            f"Q{fmt(cx - q)} {fmt(cy - q)} {fmt(cx)} {fmt(cy - r)}Z")


def star_pts(cx, cy, ro, ri, n=5, start=-90.0):
    pts = []
    for i in range(2 * n):
        pts.append(polar(cx, cy, ro if i % 2 == 0 else ri, start + i * 180 / n))
    return pts


def drop_d(cx, cy, r, h):
    """Water drop: round bottom of radius r centred (cx, cy), point h above the centre."""
    a = math.degrees(math.asin(r / h))
    p0 = polar(cx, cy, r, -90 - (90 - a))
    p1 = polar(cx, cy, r, -90 + (90 - a))
    return (f"M{fmt(cx)} {fmt(cy - h)}L{fmt(p1[0])} {fmt(p1[1])}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(p0[0])} {fmt(p0[1])}Z")


def open_hand(S, dx=0.0):
    """Raised open palm facing the viewer, fingers together (the hand-stop hand)."""
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


def point_up(S):
    """Back of a hand with the index finger raised."""
    idx = cap(8.5, 13, 8.5, 4.6)
    fist = box(6.8, 11, 11.6, 10, wr(S))
    knuck = [cap(12, 12.6, 12, 12.6), cap(15.4, 12.8, 15.4, 12.8)]
    thumb = cap(7.2, 17.5, 4.2, 14)
    return [outline(idx, fist, *knuck, thumb), detail(seg(7.8, 17.2, 12, 17.2))]


# ============================================================================ things held on an open palm

def on_palm(name, desc, tags, aliases=()):
    """fn(S) -> parts of the object floating above the palm-up hand."""
    def deco(fn):
        icon(name, CAT, desc, tags=tags, aliases=aliases)(lambda S: palm_up(S) + fn(S))
        return fn
    return deco


@on_palm("shield-in-hand", "An open hand held palm up with a shield above it; protection or insurance.",
         tags=["protection", "insurance", "security", "safe", "guard", "cover"])
def _(S):
    d = pick(S, "M14.5 2.8L19 4.4V7.3C19 9.8 17.2 11.3 14.5 12.3C11.8 11.3 10 9.8 10 7.3V4.4Z",
             "M13.6 3.1Q14.5 2.7 15.4 3.1L18.1 4.1Q19 4.4 19 5.4V7.3C19 9.8 17.2 11.3 14.5 12.3C11.8 11.3 10 9.8 10 7.3V5.4Q10 4.4 10.9 4.1Z")
    return [shell(d)]


@on_palm("paw-in-hand", "An open hand held palm up with a paw print above it; pet care or adoption.",
         tags=["pet care", "adopt", "animal welfare", "rescue", "vet", "paw"])
def _(S):
    pad = ellipse(14.5, 9.9, 3, 2.1)
    return [shell(pad), dot(10.7, 6.6, 1.35), dot(13.1, 4.1, 1.35), dot(15.9, 4.1, 1.35), dot(18.3, 6.6, 1.35)]


@on_palm("gear-in-hand", "An open hand held palm up with a gear above it; service, support or settings.",
         tags=["service", "support", "maintenance", "settings", "solution", "operations"])
def _(S):
    cx, cy, ro, ri, n = 14.6, 7.3, 5, 3.5, 6
    pts = []
    for i in range(n):
        a0 = -90 + i * 360 / n
        for da, rr in ((-17, ri), (-10, ro), (10, ro), (17, ri)):
            pts.append(polar(cx, cy, rr, a0 + da))
    return [shell(poly(pts, closed=True, r=pick(S, 0, 0.4)), stroke_miterlimit="2"), detail(circle(cx, cy, 1.1))]


@on_palm("star-in-hand", "An open hand held palm up with a star above it; favourite, reward or top service.",
         tags=["favorite", "reward", "rating", "excellence", "loyalty", "premium"])
def _(S):
    return [shell(poly(star_pts(14.8, 7.4, 4.9, 2.2), closed=True, r=S.r * 0.35), stroke_miterlimit="2")]


@on_palm("time-in-hand", "An open hand held palm up with a clock above it; time management or saving time.",
         tags=["time management", "save time", "punctual", "clock", "deadline", "schedule"])
def _(S):
    return [shell(circle(14.6, 7.4, 4.5)), detail(poly([(14.6, 5), (14.6, 7.4), (16.4, 8.6)], r=S.r * 0.5))]


@on_palm("recycling-in-hand", "An open hand held palm up with three arrows chasing round a triangle; recycling.",
         tags=["recycle", "recycling", "sustainable", "eco", "reuse", "environment"])
def _(S):
    v = [(14.6, 2.6), (19.9, 11.6), (9.3, 11.6)]
    out = []
    for i in range(3):
        a, b = v[i], v[(i + 1) % 3]
        L = math.dist(a, b)
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        p0 = (a[0] + ux * 1.6, a[1] + uy * 1.6)
        tip = (a[0] + ux * (L - 1.4), a[1] + uy * (L - 1.4))
        base = (tip[0] - ux * 3.2, tip[1] - uy * 3.2)
        n = (-uy, ux)
        hw = 2.1
        head = poly([tip, (base[0] + n[0] * hw, base[1] + n[1] * hw), (base[0] - n[0] * hw, base[1] - n[1] * hw)], closed=True)
        out.append(line(seg(*p0, base[0] + ux * 0.5, base[1] + uy * 0.5)))
        out.append(solid(head))
    return out


@on_palm("puzzle-piece-in-hand", "An open hand held palm up with a jigsaw puzzle piece above it; a solution or fit.",
         tags=["puzzle", "solution", "fit", "strategy", "problem solving", "jigsaw"])
def _(S):
    x0, x1, y0, y1 = 9.6, 17.6, 6.4, 12.6
    k = 2.0  # knob radius
    xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
    n = 1.7  # half neck
    d = (f"M{x0} {y0}H{xm - n}A{k} {k} 0 1 1 {xm + n} {y0}H{x1}V{ym - n}A{k} {k} 0 1 1 {x1} {ym + n}V{y1}H{x0}"
         f"V{ym + 1.4}A1.4 1.4 0 0 0 {x0} {ym - 1.4}Z")
    if S.name != "line":
        d = (f"M{x0 + 1.2} {y0}H{xm - n}A{k} {k} 0 1 1 {xm + n} {y0}H{x1 - 1.2}Q{x1} {y0} {x1} {y0 + 1.2}V{ym - n}"
             f"A{k} {k} 0 1 1 {x1} {ym + n}V{y1 - 1.2}Q{x1} {y1} {x1 - 1.2} {y1}H{x0 + 1.2}Q{x0} {y1} {x0} {y1 - 1.2}"
             f"V{ym + 1.4}A1.4 1.4 0 0 0 {x0} {ym - 1.4}V{y0 + 1.2}Q{x0} {y0} {x0 + 1.2} {y0}Z")
    return [shell(d)]


@on_palm("diamond-in-hand", "An open hand held palm up with a cut gem above it; value, quality or premium.",
         tags=["gem", "value", "premium", "quality", "jewel", "wealth"])
def _(S):
    pts = [(10, 6), (12.2, 3.2), (16.8, 3.2), (19, 6), (14.5, 12.2)]
    return [shell(poly(pts, closed=True, r=S.r * 0.3), stroke_miterlimit="2"), detail(seg(10.5, 6, 18.5, 6))]


@on_palm("cloud-in-hand", "An open hand held palm up with a cloud above it; cloud service or hosting.",
         tags=["cloud", "hosting", "cloud service", "storage", "saas", "weather"])
def _(S):
    parts = [disc(12.2, 8.4, 2.3), disc(15.4, 6.3, 3.2), disc(18.4, 8.6, 2.1), box(12.2, 7.5, 6.2, 3.2)]
    return [outline(*parts)]


@on_palm("medical-care-hand", "An open hand held palm up with a medical cross above it; health care.",
         tags=["health care", "medical", "care", "first aid", "insurance", "clinic"])
def _(S):
    cx, cy, a, b = 14.6, 7.3, 1.7, 4.4
    pts = [(cx - a, cy - b), (cx + a, cy - b), (cx + a, cy - a), (cx + b, cy - a), (cx + b, cy + a), (cx + a, cy + a),
           (cx + a, cy + b), (cx - a, cy + b), (cx - a, cy + a), (cx - b, cy + a), (cx - b, cy - a), (cx - a, cy - a)]
    return [shell(poly(pts, closed=True, r=S.r * 0.5))]


@on_palm("location-in-hand", "An open hand held palm up with a map pin above it; a place or local service.",
         tags=["location", "place", "local", "map pin", "address", "destination"])
def _(S):
    cx, cy, r = 14.8, 6.6, 3.8
    pl, pr = polar(cx, cy, r, 140), polar(cx, cy, r, 40)
    d = (f"M{fmt(cx)} 12.6L{fmt(pl[0])} {fmt(pl[1])}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(pr[0])} {fmt(pr[1])}Z" if S.name == "line" else
         f"M{fmt(cx)} 12.6Q{fmt(cx - 0.8)} 11.6 {fmt(pl[0])} {fmt(pl[1])}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(pr[0])} {fmt(pr[1])}Q{fmt(cx + 0.8)} 11.6 {fmt(cx)} 12.6Z")
    return [shell(d, stroke_miterlimit="2"), dot(cx, cy, 1.5)]


@on_palm("chart-in-hand", "An open hand held palm up with three rising bars above it; growth or business results.",
         tags=["growth", "results", "sales", "chart", "business", "profit"])
def _(S):
    return [line(seg(13.5, 11.5, 13.5, 9)), line(seg(17, 11.5, 17, 6)), line(seg(20.5, 11.8, 20.5, 3))]


@on_palm("target-in-hand", "An open hand held palm up with a bullseye target above it; goals within reach.",
         tags=["goal", "target", "aim", "objective", "achievement", "focus"])
def _(S):
    return [shell(circle(14.7, 7.3, 4.6)), dot(14.7, 7.3, 1.5)]


@on_palm("book-in-hand", "An open hand held palm up with a closed book above it; reading, learning or a manual.",
         tags=["book", "reading", "learning", "education", "manual", "library"])
def _(S):
    return [shell(rect(11, 3, 7.8, 8.4, min(S.R, 1.5))), detail(seg(13.2, 3, 13.2, 11.4)), detail(seg(13.2, 9, 18.8, 9))]


@on_palm("presenting-gesture", "An open hand held out palm up beside a sparkle; here it is, introducing or presenting.",
         tags=["present", "introduce", "here it is", "reveal", "show", "ta-da"])
def _(S):
    return [shell(sparkle_d(14, 8, 4.4, 0.22)), shell(sparkle_d(19.6, 4.3, 1.9, 0.3))]


# ============================================================================ things held upright in a fist

def grip(S, top=13.0, rw=2.9, dx=0.0, n=2):
    """Hand seen from the side, arm from the left, fingers curled round an upright stick at x ~ 12.5 + dx.

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


def rot_parts(parts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return xparts(parts, (c, sn, -sn, c, cx - cx * c + cy * sn, cy - cx * sn - cy * c))


@fig("microphone-in-hand", "A hand gripping a handheld microphone upright; singing, speaking or an interview.",
     tags=["microphone", "mic", "karaoke", "singer", "speech", "interview"], gap=1.0)
def _(S):
    tilt, px, py = 22, 12.5, 16
    head = [shell(circle(12.5, 4.8, 3.2)), detail(seg(9.3, 4.8, 15.7, 4.8))]
    handle = [shell(poly([(10.8, 8.6), (14.2, 8.6), (13.5, 16), (11.5, 16)], closed=True, r=S.r * 0.3))]
    return [grip(S, 13.3), rot_parts(head + handle, tilt, px, py)]


@fig("balloon-in-hand", "A hand holding the string of a round balloon; party or celebration.",
     tags=["balloon", "party", "birthday", "celebration", "fun", "festival"], gap=1.0)
def _(S):
    ball = [shell(ellipse(16, 5.4, 3.6, 3.7)), solid(poly([(14.9, 10.3), (17.1, 10.3), (16, 8.9)], closed=True))]
    string = [line("M16 10.3C16 12.2 12.2 11.6 12.4 14.4")]
    return [grip(S, 13.6, 2.75), ball, string]


@fig("flower-in-hand", "A hand holding a single flower upright by its stem; a gift of flowers or thanks.",
     tags=["flower", "gift", "thank you", "romance", "apology", "bloom"], gap=1.0)
def _(S):
    tilt, px, py = 20, 12.5, 16
    cx, cy = 12.5, 5.2
    petals = [disc(*polar(cx, cy, 2.5, -90 + k * 72), 2.05) for k in range(5)]
    leaf = pick(S, poly([(12.5, 12.2), (9.6, 9.8)]), "M12.5 12.4Q11.6 10.4 9.4 9.8")
    return [grip(S, 13.3), rot_parts([outline(*petals), dot(cx, cy, 1.1)], tilt, px, py),
            rot_parts([line(seg(cx, 9.5, cx, 16)), line(leaf)], tilt, px, py)]


@fig("ticket-in-hand", "A hand holding up a ticket stub with notched ends and a tear line; admission or entry.",
     tags=["ticket", "admission", "entry", "event", "concert", "pass"], gap=1.0)
def _(S):
    t = D(box(5, 3.5, 15, 9, min(S.R, 1.5)), disc(5, 8, 1.8), disc(20, 8, 1.8))
    ticket = [outline(t)] + [detail(seg(15.8, y, 15.8, y + 1.2)) for y in (4.5, 7.4, 10.3)]
    return [grip(S, 13.3), rot_parts(ticket, -10, 12.5, 9)]


@fig("paying-by-card", "A hand holding out a bank card with a chip and a stripe; card payment.",
     tags=["card payment", "pay", "credit card", "debit card", "checkout", "contactless"], gap=1.0)
def _(S):
    card = [shell(rect(4.5, 2.5, 15.5, 10.5, min(S.R, 2))), detail(seg(4.5, 5.6, 20, 5.6)),
            detail(rect(7, 8.2, 3.2, 2.4, 0.4))]
    return [grip(S, 13.3), card]


@fig("cash-fan", "A hand holding several banknotes spread into a fan; cash, spending or payday.",
     tags=["cash", "money", "banknotes", "payday", "spend", "bills"], gap=1.0)
def _(S):
    def note(deg):
        return rot_parts([shell(rect(9.5, 3.2, 6, 11, min(S.R, 1.2)))], deg, 12.5, 15)
    front = rot_parts([shell(rect(9.5, 3.2, 6, 11, min(S.R, 1.2))), detail(circle(12.5, 7.6, 1.3))], 28, 12.5, 15)
    return [grip(S, 13.3), front, note(0), note(-28)]


@fig("paintbrush-in-hand", "A hand gripping a paintbrush with its pointed tip raised; painting or art.",
     tags=["paint", "painting", "brush", "art", "artist", "creative"], gap=1.0)
def _(S):
    tilt, px, py = 24, 12.5, 16
    head = solid("M12.5 0.8C15.4 3.6 15.6 6 15.2 7.7H9.8C9.4 6 9.6 3.6 12.5 0.8Z")
    brush = [head, shell(rect(10.8, 8.7, 3.4, 3, 0.3)), line(seg(12.5, 11.7, 12.5, 16))]
    return [grip(S, 13.3), rot_parts(brush, tilt, px, py)]


@fig("bandaged-finger", "An open hand with an adhesive bandage wrapped round one finger; a small cut or first aid.",
     tags=["bandage", "cut", "first aid", "plaster", "injury", "finger"], gap=1.0)
def _(S):
    band = rot_parts([shell(rect(2.6, 9.3, 7.8, 3.8, min(S.R, 1.4))), dot(6.5, 11.2, 0.7)], -22, 6.5, 11.2)
    return [band, xparts(open_hand(S), (1, 0, 0, 1, 1.6, 0))]


def small_open_hand(S, k=0.84, tx=0.6, ty=3.2):
    return scale_at(open_hand(S), k, tx, ty)


@icon("germy-hand", CAT, "An open hand speckled with germs and a germ floating beside it; dirty hands or infection.",
      tags=["germs", "dirty hands", "bacteria", "infection", "hygiene", "virus"])
def _(S):
    germ = [shell(circle(19.2, 5.8, 2.1))] + [dot(*polar(19.2, 5.8, 3.9, a), 0.95) for a in (-90, -10, 70, 150, 230)]
    specks = [dot(9.2, 16.2, 1.05), dot(13.8, 15.6, 1.05), dot(11.4, 19.2, 1.05)]
    return small_open_hand(S) + specks + germ


@icon("clean-hand", CAT, "An open hand with two sparkles beside it; clean hands and good hygiene.",
      tags=["clean", "hygiene", "washed hands", "sanitised", "fresh", "spotless"])
def _(S):
    return small_open_hand(S) + [shell(sparkle_d(18.8, 7.2, 3, 0.25), stroke_miterlimit="2"), shell(sparkle_d(19.4, 15, 1.9, 0.3), stroke_miterlimit="2")]


@icon("sweaty-palm", CAT, "An open palm with drops of sweat beside the fingers; nervous or hot.",
      tags=["sweat", "sweaty", "nervous", "anxiety", "hot", "clammy"])
def _(S):
    return small_open_hand(S) + [shell(drop_d(19.5, 6.8, 1.7, 3.6)), shell(drop_d(20, 13.3, 1.5, 3.2)),
                                 shell(drop_d(17.3, 19.2, 1.4, 3))]


def spread_hand(S):
    fingers = [cap(8.5, 16.5, 4.3, 12.2, 3.2), cap(10.2, 12.5, 8.9, 5.8, 3.2), cap(12.6, 12.5, 12.6, 4.9, 3.2),
               cap(15, 12.5, 16.1, 6, 3.2), cap(16.5, 14, 19.2, 9.6, 3)]
    palm = box(8.2, 11.5, 9.4, 8, pick(S, 0.5, 3))
    wrist = box(9.2, 18, 6.4, 3.8, pick(S, 0, 0.01))
    return [outline(*fingers, palm, wrist)]


@icon("cave-hand-stencil", CAT, "A spread hand outline ringed by sprayed dots, like a prehistoric cave stencil.",
      tags=["cave art", "stencil", "prehistoric", "rock art", "handprint", "ancient"])
def _(S):
    pts = [(1.8, 10.2), (5.4, 7.6), (5.8, 3.2), (9.8, 1.4), (15.6, 1.8), (19.8, 4.2), (22.2, 8.2), (21.9, 13.4),
           (19.6, 18.2), (18.4, 21.6), (6.6, 21.6), (5.2, 18.2), (1.8, 14.6)]
    return spread_hand(S) + [dot(x, y, 0.95) for x, y in pts]


def cupped_hands(S):
    """Two hands held out palm up from either side, fingertips meeting in the middle."""
    regs = []
    for m in (1, -1):
        x = (lambda v: v if m == 1 else 24 - v)
        regs += [box(min(x(2), x(6.5)), 15.2, 4.5, 6.3, wr(S)), cap(x(5.5), 19.3, x(9.2), 19.3, 3.2),
                 cap(x(9.2), 19.3, x(10.7), 17, 3.2), cap(x(5.8), 16.8, x(7.6), 15.2, 2.8)]
    return [outline(*regs), detail(seg(12, 16.5, 12, 21))]


@fig("bowl-in-hands", "Two cupped hands holding up an empty round bowl; an offering, alms or asking for help.",
     tags=["bowl", "alms", "offering", "charity", "hunger", "donation"], gap=1.0)
def _(S):
    bowl = [shell(pick(S, "M4.5 8H19.5A7.5 6.5 0 0 1 4.5 8Z", "M5.5 8H18.5Q19.5 8 19.5 9A7.5 5.5 0 0 1 4.5 9Q4.5 8 5.5 8Z"))]
    return [cupped_hands(S), bowl]


@fig("soil-in-hands", "Two cupped hands holding a mound of soil with a small sprout; earth, planting or sustainability.",
     tags=["soil", "earth", "planting", "gardening", "sustainability", "land"], gap=1.0)
def _(S):
    mound = [shell(pick(S, "M4.6 14.7L7.6 11.3H16.4L19.4 14.7Z", "M4.6 14.7Q6 11.3 12 11.3Q18 11.3 19.4 14.7Z"))]
    sprout = [line(seg(12, 10.4, 12, 5.2)), shell("M12.9 6.2Q13.6 2.8 17.2 2.9Q16.6 6.2 12.9 6.2Z"),
              shell("M11.1 7.9Q10.4 4.6 6.8 4.6Q7.4 7.9 11.1 7.9Z")]
    return [cupped_hands(S), mound, sprout]


@on_palm("mug-in-hand", "An open hand held palm up carrying a steaming mug; coffee, tea or a hot drink.",
         tags=["mug", "coffee", "tea", "hot drink", "break", "cup"])
def _(S):
    return [shell(rect(10.5, 5.5, 7, 6.5, min(S.R, 1.5))), line(pick(S, poly([(17.5, 7), (19.8, 7), (19.8, 10), (17.5, 10)]),
                                                                       arc(17.5, 8.5, 2, -90, 90))),
            line("M12.8 3.8Q11.8 2.9 12.8 2"), line("M15.6 3.8Q14.6 2.9 15.6 2")]


# ============================================================================ more shared shapes

def touch(S, tx, ty, k=0.8):
    """point_up scaled by k with the fingertip centre moved to (tx, ty)."""
    return scale_at(point_up(S), k, tx - 8.5 * k, ty - 4.6 * k)


def finger_at(S, tx, ty, k, deg):
    """point_up scaled by k, fingertip at (tx, ty), finger pointing along deg (0 right, 90 down, -90 up)."""
    return rot_parts(touch(S, tx, ty, k), deg + 90, tx, ty)


def touch_down(S, tx, ty, k=0.8):
    """point_up flipped upside down: hand above, fingertip at (tx, ty) pointing down."""
    return xparts(point_up(S), (k, 0, 0, -k, tx - 8.5 * k, ty + 4.6 * k))


def arrow_head(S, x, y, deg, s=2.6, kind=None):
    """Open chevron arrowhead with its tip at (x, y) pointing along deg."""
    a = polar(x, y, s, deg + 180 - 45)
    b = polar(x, y, s, deg + 180 + 45)
    return (kind or line)(poly([a, (x, y), b], r=S.r * 0.4))


def arc_arrow(S, cx, cy, r, a0, a1, s=2.4):
    """Arc clockwise from a0 to a1 with an arrowhead at a1."""
    tip = polar(cx, cy, r, a1)
    return [line(arc(cx, cy, r, a0, a1)), arrow_head(S, tip[0], tip[1], a1 + 90, s)]


def fist_side(S, x=3.0, y=7.0, w=7.5, h=10.5):
    """Side view of a fist: knuckle bumps to the right, thumb folded across the top."""
    rh = (h - 3.2) / 3
    rows = [cap(x + 2, y + 3.2 + rh * (k + 0.5), x + w - rh / 2, y + 3.2 + rh * (k + 0.5), rh) for k in range(3)]
    body = box(x, y, w - 1.5, h, 1.5 if S.name == "line" else 2.5)
    thumb = cap(x + 1.5, y + 1.6, x + w - 1.8, y + 1.6, 3.2)
    seps = [detail(seg(x + w - 3.2, y + 3.2 + rh * k, x + w, y + 3.2 + rh * k)) for k in (1, 2)]
    return [outline(body, thumb, *rows), detail(seg(x + 1.5, y + 3.2, x + w - 1, y + 3.2))] + seps


def point_right(S, tx, ty, fl=4.5, fw=6.5, fh=7.5):
    """Side view of a hand pointing right, index fingertip centre at (tx, ty)."""
    x1 = tx - fl
    fist = box(x1 - fw, ty - 1.6, fw, fh, wr(S))
    idx = cap(x1 - 1, ty, tx, ty, 3.2)
    knuck = cap(x1, ty + 3.4, x1, ty + 3.4, 3)
    return [outline(fist, idx, knuck), detail(seg(x1 - fw + 1.6, ty + 1.8, x1 - 0.2, ty + 1.8))]


def eye_d(S, cx, cy, w, h):
    """Almond eye for Line, oval eye for Rounded."""
    if S.name == "line":
        return (f"M{fmt(cx - w / 2)} {fmt(cy)}Q{fmt(cx)} {fmt(cy - h)} {fmt(cx + w / 2)} {fmt(cy)}"
                f"Q{fmt(cx)} {fmt(cy + h)} {fmt(cx - w / 2)} {fmt(cy)}Z")
    return ellipse(cx, cy, w / 2, h / 2)


# ============================================================================ batch 002, part 2

@icon("watching-you-gesture", CAT, "Two fingers spread in a V below a pair of wide open eyes; I am watching you.",
      tags=["watching you", "keep an eye on", "surveillance", "warning", "suspicious", "gesture"])
def _(S):
    palm = box(6.5, 14.5, 11.5, 6.5, wr(S))
    fingers = [cap(8.3, 15.5, 6.8, 12), cap(11.7, 15.5, 13.4, 12)]
    knuck = [cap(14.9, 15.2, 14.9, 15.2, 3.2), cap(16.6, 15.8, 16.6, 15.8, 2.8)]
    thumb = cap(7.2, 18.6, 12.3, 17.8, 3)
    eyes = []
    for cx in (6.8, 16.2):
        eyes += [shell(eye_d(S, cx, 4.6, 7, 3.4)), dot(cx, 4.6, 1.2)]
    return [outline(palm, *fingers, *knuck, thumb), detail(seg(7.8, 16.9, 12.4, 16.9))] + eyes


@fig("butterfly-on-finger", "A raised index finger with a butterfly perched on the fingertip, wings open.",
     tags=["butterfly", "nature", "gentle", "calm", "spring", "wildlife"], gap=1.0)
def _(S):
    left = [outline(disc(6.9, 5.4, 3.2), disc(8.4, 9.4, 2.2))]
    right = mirror_x(left)
    fly = left + right + [line(seg(12, 4, 12, 10.4))]
    return [fly, touch(S, 12, 12.6, 0.62)]


@fig("finger-prick-test", "A raised fingertip with a drop of blood on it and a lancet pen beside it; a finger prick blood test.",
     tags=["finger prick", "blood test", "glucose", "diabetes", "lancet", "blood sugar"], gap=1.0)
def _(S):
    idx = U(box(6, 8.5, 6.4, 7, 0), disc(9.2, 8.5, 3.2))
    fist = box(5, 14, 11, 7, wr(S))
    knuck = [cap(14.2, 15.4, 14.2, 15.4, 3.2), cap(16.2, 16, 16.2, 16, 2.8)]
    thumb = cap(6, 18.4, 3.6, 15.4, 3)
    hand = [outline(idx, fist, *knuck, thumb), Part("dot", drop_d(9.2, 10.6, 1.6, 3.2)), detail(seg(6.6, 18.2, 11.2, 18.2))]
    pen = rot_parts([shell(rect(14.8, 3, 3.4, 6.8, min(S.R, 1.7))), line(seg(16.5, 9.8, 16.5, 12.2))], 24, 16.5, 12.2)
    return [hand, pen]


@fig("hand-stamp-entry", "The back of a hand marked with a star stamp and a rubber stamp lifting away; event re-entry.",
     tags=["hand stamp", "re-entry", "admission", "club", "event entry", "wristband"], gap=1.0)
def _(S):
    hand = scale_at(open_hand(S), 0.74, -0.2, 6.3)[:1]
    star = Part("dot", poly(star_pts(8.4, 17.9, 2.6, 1.1), closed=True))
    stamp = [outline(disc(18.3, 3.6, 1.8), box(17.3, 4.6, 2, 3.2), box(14.3, 7.3, 8, 2.6, pick(S, 0.3, 1)))]
    return [hand + [star], stamp]


@fig("touching-water", "A fingertip touching still water with ripple rings spreading out from the contact point.",
     tags=["ripple", "water", "touch", "calm", "mindfulness", "surface"], gap=1.0)
def _(S):
    rings = [shell(ellipse(12, 15, 4.6, 1.9)), shell(ellipse(12, 15.6, 9.6, 4.6))]
    fing = [shell(pick(S, "M9.6 2V10.6A2.4 2.4 0 0 0 14.4 10.6V2Z", "M9.6 3Q9.6 2 10.6 2H13.4Q14.4 2 14.4 3V10.6A2.4 2.4 0 0 1 9.6 10.6Z"))]
    return [fing, rings[:1], rings[1:]]


@fig("chalking-hands", "Two hands clapping together with a puff of chalk dust rising between them.",
     tags=["chalk", "chalk dust", "climbing", "gymnastics", "weightlifting", "grip"], gap=1.0)
def _(S):
    right = [outline(mitten(16.8, 22, 13.3, 11.2), cap(16.6, 18.5, 19.4, 15.2, 2.8))]
    left = [outline(mitten(7.2, 22, 10.7, 11.2), cap(7.4, 18.5, 4.6, 15.2, 2.8))]
    dust = [dot(12, 6.2, 1.2), dot(8.4, 6.8, 1), dot(15.6, 6.8, 1), dot(10, 3, 1), dot(14, 3, 1), dot(5.2, 4, 0.9), dot(18.8, 4, 0.9)]
    return [right + dust, left]


@fig("sign-language-stop", "The edge of one flat hand chopping down onto the upturned palm of the other; the sign for stop.",
     tags=["sign language", "stop", "halt", "asl", "deaf", "signing"], gap=1.0)
def _(S):
    top = [outline(mitten(12.5, 1.5, 12.5, 11.6, 4.4))]
    low = [outline(U(ST(seg(2, 17.8, 18.5, 17.8), 5, "butt", "miter"), disc(18.5, 17.8, 2.5)), cap(7, 15.6, 10, 13.2, 2.8)),
           detail(seg(8, 18.6, 18, 18.6))]
    marks = [line(seg(6.5, 4, 6.5, 8.5)), line(seg(18.5, 4, 18.5, 8.5))]
    return [top + marks, low]


@fig("applying-bandage", "A fingertip pressing an adhesive bandage flat onto the skin; applying a plaster.",
     tags=["bandage", "plaster", "first aid", "wound care", "graze", "injury"], gap=1.0)
def _(S):
    strip = [shell(rect(2.5, 14.5, 19, 6.2, pick(S, 1, 3.1))), detail(seg(9, 14.5, 9, 20.7)), detail(seg(15, 14.5, 15, 20.7))]
    return [touch_down(S, 12, 13, 0.6), strip]


@icon("turning-watch-crown", CAT, "A smartwatch with a curved arrow turning the crown on its side.",
      tags=["watch crown", "digital crown", "smartwatch", "scroll", "wind", "dial"])
def _(S):
    body = [box(3.5, 6.5, 11.5, 11, min(S.R, 3)), box(5.5, 2, 7.5, 5), box(5.5, 17, 7.5, 5), box(14.5, 10.5, 2.4, 3, 0.5)]
    return [outline(*body), detail(rect(6.5, 9.5, 5.5, 5, pick(S, 0.5, 1)))] + arc_arrow(S, 16, 12, 5.2, -65, 65, 2.2)


@icon("rule-of-thumb", CAT, "A raised thumb from a fist with ruler tick marks alongside it; a rule of thumb.",
      tags=["rule of thumb", "estimate", "guideline", "approximation", "measure", "heuristic"])
def _(S):
    thumb = cap(8.5, 11.5, 8.5, 4, 3.6)
    rows = [cap(9, y, 17.5, y, 3.2) for y in (13, 16.2)] + [cap(9, 19.4, 16.5, 19.4, 3.2)]
    fist = box(6.5, 11.4, 8, 9.6, pick(S, 1, 1.5))
    cuff = box(2.5, 11.4, 3.5, 9.6, pick(S, 0.5, 1.5))
    ticks = [line(seg(13, y, 13 + L, y)) for y, L in ((2.6, 4.5), (5.4, 2.5), (8.2, 4.5))]
    return [outline(thumb, fist, *rows), outline(cuff), detail(seg(11.5, 14.6, 16.5, 14.6)),
            detail(seg(11.5, 17.8, 16, 17.8)), detail(seg(10.4, 11.4, 12.5, 11.4))] + ticks


@fig("hanging-on-ledge", "Four fingertips gripping the top edge of a ledge with the hand hanging below it.",
     tags=["hanging on", "cliffhanger", "ledge", "hold on", "struggle", "danger"], gap=1.0)
def _(S):
    xs = (7.3, 10.7, 14.1, 17.5)
    fingers = [cap(x, 4.4, x, 13) for x in xs]
    hand = [outline(*fingers, box(5.6, 11.5, 13.6, 6.5, wr(S)), box(8, 16, 8.8, 5.5, pick(S, 0, 0.01)))]
    ledge = [shell(rect(2, 8, 20, 3.6, min(S.R, 1))), ]
    return [ledge, hand]


@fig("poke-gesture", "An index finger jabbing into a round shape that dents in, with two impact marks.",
     tags=["poke", "nudge", "prod", "jab", "attention", "ping"], gap=1.0)
def _(S):
    hand = point_right(S, 13.2, 10.6)
    ball = D(disc(18.2, 10.6, 3.9), disc(13.4, 10.6, 2.6))
    marks = [line(seg(15.8, 4.6, 14.6, 2.6)), line(seg(15.8, 16.6, 14.6, 18.6))]
    return [hand, [outline(ball)] + marks]


# ============================================================================ batch 002, part 3

def pinch_hold(S):
    """Side view of a hand pinching something small between thumb and index; contact point (18, 12.8)."""
    back = box(2.5, 7.5, 7, 10.5, wr(S))
    idx = capd("M8 9.3Q13.2 8.2 16.2 11.4", 3.2)
    thumb = cap(8, 16.2, 15.6, 14.2, 3.4)
    return [outline(back, idx, thumb), detail(seg(8.8, 12.6, 11.5, 12.6))]


def pinch_at(S, x, y, k, deg):
    """pinch_hold scaled by k, contact point at (x, y), fingers pointing along deg."""
    return rot_parts(scale_at(pinch_hold(S), k, x - 18 * k, y - 12.8 * k), deg, x, y)


@fig("drawing-from-hat", "A hand reaching into a top hat and lifting out a folded slip of paper; a prize draw or raffle.",
     tags=["draw", "raffle", "lottery", "random pick", "prize draw", "lucky dip"], gap=1.0)
def _(S):
    hat = [shell(pick(S, "M6.5 11.5V18.5H17.5V11.5", "M6.5 11.5V17.5Q6.5 18.5 7.5 18.5H16.5Q17.5 18.5 17.5 17.5V11.5")),
           shell(ellipse(12, 11.5, 5.5, 2)), shell(rect(2.5, 18.5, 19, 3, pick(S, 0.3, 1.5)))]
    slip = rot_parts([shell(rect(14.6, 2.4, 4.6, 6.4, 0.4))], 12, 17, 6)
    arm = [outline(box(9.6, 1.6, 4.4, 8.6, 0))]
    return [arm, slip, hat]


@fig("pinning-a-note", "A thumb pressing a pushpin into a note card; pinning a reminder to a board.",
     tags=["pushpin", "pin", "note", "reminder", "noticeboard", "thumbtack"], gap=1.0)
def _(S):
    thumb = [shell(pick(S, "M9.6 2V7.2A2.4 2.4 0 0 0 14.4 7.2V2Z", "M9.6 3Q9.6 2 10.6 2H13.4Q14.4 2 14.4 3V7.2A2.4 2.4 0 0 1 9.6 7.2Z"))]
    pin = [shell(ellipse(12, 10.6, 3.2, 1.1)), line(seg(12, 11.7, 12, 14.4))]
    note = [shell(rect(3.5, 13, 17, 8.5, min(S.R, 1.5))), line(seg(7, 18.2, 17, 18.2))]
    return [thumb, pin, note]


@fig("entering-pin", "A fingertip pressing a key on a number pad below a field of four masked digits; entering a PIN.",
     tags=["pin code", "passcode", "keypad", "enter pin", "security", "card payment"], gap=1.0)
def _(S):
    field = [shell(rect(2.5, 2, 19, 5.5, min(S.R, 2)))] + [dot(x, 4.75, 1) for x in (6.6, 10.2, 13.8, 17.4)]
    keys = [dot(x, y, 1.3) for x in (5.5, 12, 18.5) for y in (11, 15, 19)]
    return [touch(S, 12, 15, 0.42), field + keys]


@icon("hand-turkey-drawing", CAT, "A traced outline of a spread hand turned into a turkey, the thumb its head with a beak.",
      tags=["hand turkey", "thanksgiving", "kids craft", "drawing", "art class", "turkey"])
def _(S):
    feathers = [cap(10.2, 12.5, 8.9, 5.8, 3.2), cap(12.6, 12.5, 12.6, 4.9, 3.2), cap(15, 12.5, 16.1, 6, 3.2), cap(16.5, 14, 19.2, 9.6, 3)]
    neck = cap(9, 15.5, 6, 10.5, 3.2)
    head = disc(5.6, 9.4, 2.4)
    body = box(8.2, 11.5, 9.4, 7.5, pick(S, 0.5, 3))
    beak = solid(poly([(3.4, 9.2), (1.8, 10.2), (3.6, 11)], closed=True))
    legs = [line(seg(11, 19.5, 10.5, 22)), line(seg(14.5, 19.5, 15, 22))]
    return [outline(*feathers, neck, head, body), dot(6.1, 8.8, 0.8), beak] + legs


@icon("flipping-hourglass", CAT, "An hourglass tipped over with a curved arrow turning it round; flipping the timer over.",
      tags=["flip hourglass", "turn over", "timer", "restart", "time", "reset"])
def _(S):
    g = [(8, 4), (16, 4), (16, 6.5), (12.8, 12), (16, 17.5), (16, 20), (8, 20), (8, 17.5), (11.2, 12), (8, 6.5)]
    glass = [shell(poly(g, closed=True, r=S.r * 0.5))]
    glass = rot_parts(scale_at(glass, 0.72, 3.36, 3.36), 28, 12, 12)
    return glass + arc_arrow(S, 12, 12, 10, -62, 62, 2.4)


@fig("hand-in-cookie-jar", "A hand reaching down into a jar, its lid set aside; caught in the cookie jar.",
     tags=["cookie jar", "caught", "temptation", "snack", "sneaky", "treat"], gap=1.0)
def _(S):
    jar = [shell(rect(3.5, 10, 12, 12, min(S.R, 3.5))), shell(rect(5, 7, 9, 3, pick(S, 0.3, 1))),
           dot(6.6, 18.4, 0.8), dot(10.2, 19.2, 0.8), dot(12.4, 16.2, 0.8)]
    lid = rot_parts([shell(rect(15.6, 4.5, 6, 2.4, pick(S, 0.3, 1))), dot(18.6, 3.2, 1)], 14, 18.6, 5.7)
    arm = [outline(box(6.4, 1.6, 6, 10.4, 0)), detail(seg(6.4, 4.6, 12.4, 4.6))]
    return [arm, jar, lid]


@icon("tossing-in-bin", CAT, "A crumpled paper ball flying along a dashed arc into an open waste bin.",
      tags=["throw away", "bin", "trash", "rubbish", "discard", "toss"])
def _(S):
    pts = [(1.8, 5.2), (4, 2.8), (6.6, 3.4), (8.6, 5.4), (8.2, 8.4), (5.8, 10.4), (3, 9.8), (1.4, 7.6)]
    ball = [solid(poly(pts, closed=True, r=0.4 if S.name == "rounded" else 0))]
    path = [dot(*polar(12, 14, 6.6, a), 1.05) for a in (-110, -80, -50)]
    bin_ = [shell(poly([(12.5, 14.4), (21.5, 14.4), (20.3, 22), (13.7, 22)], closed=True, r=S.r * 0.6)), line(seg(11, 12.4, 23, 12.4))]
    return ball + path + bin_


# ============================================================================ batch 002, part 4

@fig("sealing-envelope", "A fingertip pressing down the pointed flap of an envelope to seal it.",
     tags=["seal", "envelope", "letter", "mail", "close", "post"], gap=1.0)
def _(S):
    env = [shell(rect(2.5, 5, 19, 13.5, min(S.R, 2))), detail(poly([(2.5, 5), (12, 12.5), (21.5, 5)], r=S.r))]
    return [finger_at(S, 13.2, 13.4, 0.5, -95), env]


@icon("crossing-off-item", CAT, "A pencil drawing a line through one item on a short list; crossing a task off.",
      tags=["cross off", "done", "task", "to do list", "strike through", "complete"])
def _(S):
    rows = [dot(3.8, 4.5, 1.3), line(seg(7, 4.5, 14.5, 4.5)), line(poly([(2.4, 11.8), (3.8, 13.2), (6, 10.2)], r=S.r * 0.3)), line(seg(8.4, 11.6, 13.4, 11.6)),
            dot(3.8, 18.7, 1.3), line(seg(7, 18.7, 17, 18.7))]
    pencil = [shell(poly([(14.6, 11.6), (17.29, 11.17), (21.39, 7.07), (19.13, 4.81), (15.03, 8.91)], closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
              detail(seg(17.29, 11.17, 15.03, 8.91))]
    return rows + pencil


@fig("knock-on-wood", "A fist knocking its knuckles on a wooden plank with grain lines and two knock marks.",
     tags=["knock on wood", "touch wood", "luck", "superstition", "knock", "jinx"], gap=1.0)
def _(S):
    fist = [outline(box(6.4, 1.8, 11.2, 9.2, wr(S))), detail(seg(9.2, 11, 9.2, 6.6)), detail(seg(12, 11, 12, 6.6)), detail(seg(14.8, 11, 14.8, 6.6))]
    plank = [shell(rect(2.5, 15.5, 19, 6, min(S.R, 1.5))), detail("M5 18.5C8 17.3 10 19.7 13 18.5S17 17.3 19 18.5")]
    marks = [line(seg(4.4, 10.5, 2.6, 8.7)), line(seg(19.6, 10.5, 21.4, 8.7))]
    return [fist + marks, plank]


@fig("pushing-up-glasses", "An index finger pushing a pair of glasses up by the bridge; nerdy or adjusting glasses.",
     tags=["glasses", "nerd", "smart", "adjust glasses", "actually", "geek"], gap=1.0)
def _(S):
    glasses = [shell(circle(6.3, 7.5, 3.8)), shell(circle(17.7, 7.5, 3.8)), line(arc(12, 8.2, 2.1, 200, 340))]
    return [touch(S, 12, 10.2, 0.6), glasses]
