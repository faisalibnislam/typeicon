"""TypeIcon Core: letters & numbers.

One letterform system, drawn once as 2 px stroke skeletons (never font text, not traced from a typeface):

* Design units: cap height 14 (v = 0 cap line … v = 14 baseline); each glyph has its own width.
  Standalone glyphs map 1:1 onto y 5–19; inside a square they shrink to 7–17, inside a circle to 8–16
  (wide glyphs are condensed so every glyph keeps a 2 px gap to its container).
* Bowls and curves are quarter-ellipse Béziers; round strokes overshoot the cap line and baseline by 0.3.
  Bars sit on the cap line (0), the middle (7) and the baseline (14) so they land on whole pixels.
* Line: butt terminals, sharp joins (miter limit 2, bevelled on acute apexes) and slightly squarer bowls.
  Stems that end on the cap line or baseline are lengthened by 1 px so their flat ends line up with the
  outer edge of the bars (the same height a round cap reaches).
* Rounded: the same skeleton with round terminals and joins, 1.5 px fillets on straight corners and true
  elliptical bowls.
* Filled: the Line skeleton at 2.5 px; in a square or circle the glyph is knocked out of the solid shape.
"""
import math

from dsl import D, P, ST, U, circle, detail, icon, line, rect, shell  # noqa: F401
from geometry import fmt

CAT = "letters"
OVER = 0.3  # overshoot of round strokes (design units)
KAPPA = {"line": 0.64, "rounded": 0.5523}  # Line bowls are squarer
EXT = {"line": 1.0, "rounded": 0.0}  # Line: stem ends lengthened to the bar edge (grid px)
FILLET = {"line": 0.0, "rounded": 1.5}  # Rounded: fillets on straight corners (grid px)
MITER = "2"


# ============================================================================ curve helpers (design units)

def _axis(cx, cy, rx, ry, th):
    a = math.radians(th)
    return (cx + rx * round(math.cos(a)), cy + ry * round(math.sin(a)))


def _quarter(cx, cy, rx, ry, q, k):
    """Cubic for the quarter ellipse from angle 90q to 90(q+1) (screen angles, 90 = down)."""
    t0, t1 = 90 * q, 90 * (q + 1)
    p0, p3 = _axis(cx, cy, rx, ry, t0), _axis(cx, cy, rx, ry, t1)
    a0, a1 = math.radians(t0), math.radians(t1)
    d0 = (-rx * round(math.sin(a0)), ry * round(math.cos(a0)))
    d1 = (-rx * round(math.sin(a1)), ry * round(math.cos(a1)))
    return [p0, (p0[0] + k * d0[0], p0[1] + k * d0[1]), (p3[0] - k * d1[0], p3[1] - k * d1[1]), p3]


def _lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _split(b, t):
    p01, p12, p23 = _lerp(b[0], b[1], t), _lerp(b[1], b[2], t), _lerp(b[2], b[3], t)
    p012, p123 = _lerp(p01, p12, t), _lerp(p12, p23, t)
    m = _lerp(p012, p123, t)
    return [b[0], p01, p012, m], [m, p123, p23, b[3]]


def _sub(b, t0, t1):
    if t1 < 1:
        b = _split(b, t1)[0]
        t0 = t0 / t1 if t1 > 0 else 0
    if t0 > 0:
        b = _split(b, t0)[1]
    return b


def _arc(cx, cy, rx, ry, ta, tb, k):
    lo, hi = min(ta, tb), max(ta, tb)
    out = []
    q = math.floor(lo / 90)
    while 90 * q < hi - 1e-9:
        s, e = max(lo, 90 * q), min(hi, 90 * (q + 1))
        if e - s > 1e-9:
            out.append(_sub(_quarter(cx, cy, rx, ry, q, k), (s - 90 * q) / 90, (e - 90 * q) / 90))
        q += 1
    if tb < ta:
        out = [list(reversed(b)) for b in reversed(out)]
    return out


def _unit(dx, dy):
    n = math.hypot(dx, dy) or 1.0
    return dx / n, dy / n


# ============================================================================ stroke builder

def _stroke(items, S, pen, closed=False, ext=(False, False)) -> str:
    """Turn a skeleton (M/L/A/C/T items in design units) into a grid d-string for style S."""
    segs = []
    cur = start = None
    for it in items:
        op = it[0]
        if op == "M":
            cur = start = (it[1], it[2])
        elif op == "L":
            p = (it[1], it[2])
            segs.append(["L", cur, p])
            cur = p
        elif op == "A":
            bs = _arc(*it[1:], KAPPA[S.name])
            if cur is None:
                cur = start = bs[0][0]
            elif math.dist(cur, bs[0][0]) > 1e-6:
                segs.append(["L", cur, bs[0][0]])
            for b in bs:
                segs.append(["C", *b])
            cur = bs[-1][3]
        elif op == "H":  # horizontal line to u, keeping the current height
            p = (it[1], cur[1])
            segs.append(["L", cur, p])
            cur = p
        elif op == "C":
            p = (it[5], it[6])
            segs.append(["C", cur, (it[1], it[2]), (it[3], it[4]), p])
            cur = p
        elif op == "T":  # cubic that continues the previous tangent: (T, len, c2x, c2y, x, y)
            prev = segs[-1]
            ux, uy = _unit(prev[-1][0] - prev[-2][0], prev[-1][1] - prev[-2][1])
            c1 = (cur[0] + ux * it[1], cur[1] + uy * it[1])
            p = (it[4], it[5])
            segs.append(["C", cur, c1, (it[2], it[3]), p])
            cur = p
    if closed and math.dist(cur, start) > 1e-6:
        segs.append(["L", cur, start])
    segs = [[s[0], *[pen(p) for p in s[1:]]] for s in segs]

    o = EXT[S.name]
    if o and not closed:
        for which, flag in ((0, ext[0]), (1, ext[1])):
            if not flag:
                continue
            s = segs[0] if which == 0 else segs[-1]
            a, b = (s[1], s[2]) if which == 0 else (s[-1], s[-2])
            ux, uy = _unit(a[0] - b[0], a[1] - b[1])
            ln = o / abs(uy) if abs(uy) >= abs(ux) else o / abs(ux)
            p = (a[0] + ux * min(ln, 1.5 * o), a[1] + uy * min(ln, 1.5 * o))
            if which == 0:
                s[1] = p
            else:
                s[-1] = p

    r = FILLET[S.name]
    arcs = {}
    n = len(segs)
    vertices = range(n) if closed else range(1, n)
    if r > 0:
        for i in vertices:
            a, b = segs[i - 1], segs[i]
            if a[0] != "L" or b[0] != "L":
                continue
            p = a[2]
            ux, uy = a[1][0] - p[0], a[1][1] - p[1]
            vx, vy = b[2][0] - p[0], b[2][1] - p[1]
            la, lb = math.hypot(ux, uy), math.hypot(vx, vy)
            if la < 1e-6 or lb < 1e-6:
                continue
            ux, uy, vx, vy = ux / la, uy / la, vx / lb, vy / lb
            th = math.acos(max(-1.0, min(1.0, ux * vx + uy * vy)))
            if th < math.radians(75) or abs(th - math.pi) < 1e-3:
                continue  # acute apexes keep a plain round join
            t = r / math.tan(th / 2)
            rr = r
            if t > min(la, lb) / 2:
                t = min(la, lb) / 2
                rr = t * math.tan(th / 2)
            t1 = (p[0] + ux * t, p[1] + uy * t)
            t2 = (p[0] + vx * t, p[1] + vy * t)
            sweep = 0 if ux * vy - uy * vx > 0 else 1
            a[2] = t1
            b[1] = t2
            arcs[i] = f"A{fmt(rr)} {fmt(rr)} 0 0 {sweep} {fmt(t2[0])} {fmt(t2[1])}"

    def pt(q):
        return f"{fmt(q[0])} {fmt(q[1])}"

    out = ["M" + pt(segs[0][1])]
    for i, s in enumerate(segs):
        if s[0] == "L":
            out.append("L" + pt(s[2]))
        else:
            out.append("C" + pt(s[2]) + " " + pt(s[3]) + " " + pt(s[4]))
        j = (i + 1) % n
        if j in arcs and (closed or j != 0):
            out.append(arcs[j])
    if closed:
        out.append("Z")
    return "".join(out)


def _s(*items, z=False, e=(0, 0)):
    return (items, z, (bool(e[0]), bool(e[1])))


# ============================================================================ glyph skeletons (design units)

def _A():
    top = -0.6
    xl = 6 * (14 - 9) / (14 - top)
    return 12, [_s(("M", 0, 14), ("L", 6, top), ("L", 12, 14), e=(1, 1)), _s(("M", xl, 9), ("L", 12 - xl, 9))]


def _B():
    return 10, [_s(("M", 0, 6.5), ("L", 0, 0), ("L", 5.25, 0), ("A", 5.25, 3.25, 3.75, 3.25, -90, 90), z=True),
                _s(("M", 0, 6.5), ("L", 5.75, 6.5), ("A", 5.75, 10.25, 4.25, 3.75, -90, 90), ("L", 0, 14), z=True)]


def _C():
    return 11, [_s(("A", 5.5, 7, 5.5, 7 + OVER, -44, -316))]


def _D():
    return 11, [_s(("M", 0, 0), ("L", 4.5, 0), ("A", 4.5, 7, 6.5, 7, -90, 90), ("L", 0, 14), z=True)]


def _E():
    return 9, [_s(("M", 9, 0), ("L", 0, 0), ("L", 0, 14), ("L", 9, 14)), _s(("M", 0, 7), ("L", 8, 7))]


def _F():
    return 9, [_s(("M", 9, 0), ("L", 0, 0), ("L", 0, 14), e=(0, 1)), _s(("M", 0, 7), ("L", 8, 7))]


def _G():
    end = -360 + math.degrees(math.asin(1 / (7 + OVER)))  # the bowl ends one unit below the middle
    return 12, [_s(("A", 6, 7, 6, 7 + OVER, -44, end), ("H", 6.5))]


def _H():
    return 10, [_s(("M", 0, 0), ("L", 0, 14), e=(1, 1)), _s(("M", 10, 0), ("L", 10, 14), e=(1, 1)), _s(("M", 0, 7), ("L", 10, 7))]


def _I():
    return 6, [_s(("M", 3, 0), ("L", 3, 14)), _s(("M", 0, 0), ("L", 6, 0)), _s(("M", 0, 14), ("L", 6, 14))]


def _J():
    return 8, [_s(("M", 8, 0), ("L", 8, 9.5), ("A", 4, 9.5, 4, 4.5 + OVER, 0, 165), e=(1, 0))]


def _K():
    ax = 3.5
    return 10, [_s(("M", 0, 0), ("L", 0, 14), e=(1, 1)), _s(("M", 10, 0), ("L", 0, 9), e=(1, 0)),
                _s(("M", ax, 9 * (10 - ax) / 10), ("L", 10, 14), e=(0, 1))]


def _L():
    return 8, [_s(("M", 0, 0), ("L", 0, 14), ("L", 8, 14), e=(1, 0))]


def _M():
    return 13, [_s(("M", 0, 14), ("L", 0, -0.4), ("L", 6.5, 10), ("L", 13, -0.4), ("L", 13, 14), e=(1, 1))]


def _N():
    return 10, [_s(("M", 0, 14), ("L", 0, -0.4), ("L", 10, 14.4), ("L", 10, 0), e=(1, 1))]


def _O():
    return 13, [_s(("A", 6.5, 7, 6.5, 7 + OVER, -90, 270), z=True)]


def _P():
    return 10, [_s(("M", 0, 14), ("L", 0, 0), ("L", 5.5, 0), ("A", 5.5, 3.75, 4.5, 3.75, -90, 90), ("L", 0, 7.5), e=(1, 0))]


def _Q():
    return 13, [_s(("A", 6.5, 7, 6.5, 7 + OVER, -90, 270), z=True), _s(("M", 8, 9.5), ("L", 13, 15))]


def _R():
    w, st = _P()
    return w, st + [_s(("M", 5, 7.5), ("L", 10, 14), e=(0, 1))]


def _S():
    ux, uy, urx, ury = 5, 3.65, 4.6, 3.65 + OVER
    lx, ly, lrx, lry = 5, 10.35, 5, 3.65 + OVER
    return 10, [_s(("A", ux, uy, urx, ury, -28, -180),
                   ("C", ux - urx, uy + 3.4, lx + lrx, ly - 3.4, lx + lrx, ly),
                   ("A", lx, ly, lrx, lry, 0, 152))]


def _T():
    return 12, [_s(("M", 0, 0), ("L", 12, 0)), _s(("M", 6, 0), ("L", 6, 14), e=(0, 1))]


def _U():
    return 10, [_s(("M", 0, 0), ("L", 0, 9), ("A", 5, 9, 5, 5 + OVER, 180, 0), ("L", 10, 0), e=(1, 1))]


def _V():
    return 12, [_s(("M", 0, 0), ("L", 6, 14.6), ("L", 12, 0), e=(1, 1))]


def _W():
    return 16, [_s(("M", 0, 0), ("L", 3.9, 14.6), ("L", 8, 2.5), ("L", 12.1, 14.6), ("L", 16, 0), e=(1, 1))]


def _X():
    return 11, [_s(("M", 0, 0), ("L", 11, 14), e=(1, 1)), _s(("M", 11, 0), ("L", 0, 14), e=(1, 1))]


def _Y():
    return 12, [_s(("M", 0, 0), ("L", 6, 7.5), ("L", 12, 0), e=(1, 1)), _s(("M", 6, 7.5), ("L", 6, 14), e=(0, 1))]


def _Z():
    return 10, [_s(("M", 0, 0), ("L", 10, 0), ("L", 0, 14), ("L", 10, 14))]


def _0():
    return 9.5, [_s(("A", 4.75, 7, 4.75, 7 + OVER, -90, 270), z=True)]


def _1():
    return 8, [_s(("M", 0.5, 3.5), ("L", 4.5, -0.3), ("L", 4.5, 14)), _s(("M", 0.5, 14), ("L", 8.5, 14))]


def _2():
    return 9.5, [_s(("A", 4.75, 4.4, 4.5, 4.4 + OVER, -160, 30), ("T", 2.6, 1.2, 11, 0, 14), ("L", 9.5, 14))]


def _3():
    return 9.5, [_s(("A", 4.5, 3.3, 4.2, 3.3 + OVER, -155, 90), ("L", 3, 6.6)),
                 _s(("M", 3, 6.6), ("L", 4.7, 6.6), ("A", 4.7, 10.45, 4.8, 3.85 + OVER, -90, 155))]


def _4():
    return 10, [_s(("M", 7, 14), ("L", 7, -0.4), ("L", 0, 10), ("L", 10, 10), e=(1, 0))]


def _5():
    return 9.5, [_s(("M", 9, 0), ("L", 1, 0), ("A", 4.6, 9.8, 4.9, 4.5, -148, 150))]


def _6():
    return 9.5, [_s(("A", 5.5, 8, 5.5, 8 + OVER, -55, -180), ("L", 0, 9.55)),
                 _s(("A", 4.75, 9.55, 4.75, 4.45 + OVER, -90, 270), z=True)]


def _7():
    return 9.5, [_s(("M", 0, 0), ("L", 9.5, 0), ("L", 3, 14), e=(0, 1))]


def _8():
    return 9.5, [_s(("A", 4.75, 3.35, 4.1, 3.35 + OVER, -90, 270), z=True),
                 _s(("A", 4.75, 10.65, 4.75, 3.35 + OVER, -90, 270), z=True)]


def _9():
    # Not a turned 6: the tail drops straight from the bowl before curling into the baseline.
    return 9.5, [_s(("A", 4.75, 4.5, 4.75, 4.5 + OVER, -90, 270), z=True),
                 _s(("M", 9.5, 4.5), ("L", 9.5, 10), ("A", 5.25, 10, 4.25, 4 + OVER, 0, 145))]


GLYPHS = {c: globals()[f"_{c.upper()}"] for c in "abcdefghijklmnopqrstuvwxyz0123456789"}


def glyph(ch, S, box):
    """Stroke d-strings for glyph ch in style S. box = 'plain' | 'square' | 'circle'."""
    w, strokes = GLYPHS[ch]()
    if box == "plain":
        sy, sx, top, maxw = 1.0, 1.0, 5.0, 18.0
    elif box == "square":
        sy, top, maxw = 10 / 14, 7.0, 10.0
        sx = min(sy, maxw / w)
    else:
        sy, top, maxw = 8 / 14, 8.0, 6.0
        sx = min(sy, maxw / w)
    x0 = 12 - sx * w / 2
    if box == "plain":
        x0 = math.floor(x0 + 0.5)  # stems on whole pixels

    def pen(p):
        return (x0 + sx * p[0], top + sy * p[1])

    return [_stroke(items, S, pen, closed=z, ext=e) for items, z, e in strokes]


# ============================================================================ icon definitions


def _knockout(base_d, ch, box):
    from geometry import LINE
    g = U(*[ST(d, 2.0, "butt", "miter", 2.0) for d in glyph(ch, LINE, box)])
    return D(U(P(base_d), ST(base_d, 2.0)), g)


NUMBER_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def _plain(ch):
    kind = "number" if ch.isdigit() else "letter"
    name = f"{kind}-{ch}"
    if ch.isdigit():
        desc = f"Digit {ch} ({NUMBER_WORDS[int(ch)]})"
        tags = [ch, NUMBER_WORDS[int(ch)], "number", "digit", "numeral", "count"]
    else:
        desc = f"Capital letter {ch.upper()}"
        tags = [ch, "letter", "alphabet", "capital", "character", "initial"]

    @icon(name, CAT, desc, tags=tags)
    def _(S, ch=ch):
        return [line(d, stroke_miterlimit=MITER) for d in glyph(ch, S, "plain")]


def _square(ch):
    base = lambda S: rect(3, 3, 18, 18, S.R)  # noqa: E731
    from geometry import LINE

    @icon(f"square-letter-{ch}", CAT, f"Capital letter {ch.upper()} in a square",
          tags=[ch, "letter", "square", "alphabet", "initial", "label"],
          filled=lambda ch=ch: _knockout(rect(3, 3, 18, 18, LINE.R), ch, "square"))
    def _(S, ch=ch):
        return [shell(base(S)), *[detail(d, stroke_miterlimit=MITER) for d in glyph(ch, S, "square")]]


def _circle(ch):
    word = NUMBER_WORDS[int(ch)]

    @icon(f"circle-number-{ch}", CAT, f"Digit {ch} ({word}) in a circle",
          tags=[ch, word, "number", "circle", "digit", "step"],
          filled=lambda ch=ch: _knockout(circle(12, 12, 9), ch, "circle"))
    def _(S, ch=ch):
        return [shell(circle(12, 12, 9)), *[detail(d, stroke_miterlimit=MITER) for d in glyph(ch, S, "circle")]]


for _c in "abcdefghijklmnopqrstuvwxyz":
    _plain(_c)
for _c in "0123456789":
    _plain(_c)
for _c in "abcdefghijklmnopqrstuvwxyz":
    _square(_c)
for _c in "0123456789":
    _circle(_c)
