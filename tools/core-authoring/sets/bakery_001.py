"""TypeIcon Core: bakery (batch bakery_001).

Breads, rolls, flatbreads, pastries, tarts, pies and fried doughs drawn from the baked goods themselves.
Loaves are shown in side view on a flat base; flat and round items are shown from above or at a slight angle.
"""
import math
import re

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, rotation, transform_path  # noqa: F401

CAT = "bakery"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def xf(d, deg=0.0, cx=12.0, cy=12.0, dx=0.0, dy=0.0):
    """Rotate (clockwise on screen) about (cx, cy), then translate, an absolute d-string made of
    M/L/H/V/C/Q/Z and A commands (works for open paths too)."""
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    toks = re.findall(r"[MLCQAZHV]|-?\d*\.?\d+(?:e-?\d+)?", d)

    def tp(x, y):
        x, y = x - cx, y - cy
        return f"{fmt(cx + x * ca - y * sa + dx)} {fmt(cy + x * sa + y * ca + dy)}"

    out, i, cmd = [], 0, None
    cur = (0.0, 0.0)
    start = (0.0, 0.0)
    while i < len(toks):
        t = toks[i]
        if t in "MLCQAZHV":
            cmd = t
            if t == "Z":
                out.append("Z")
                cur = start
            elif t not in "HV":
                out.append(t)
            i += 1
            continue
        if cmd == "H":
            cur = (float(t), cur[1])
            out += ["L", tp(*cur)]
            i += 1
        elif cmd == "V":
            cur = (cur[0], float(t))
            out += ["L", tp(*cur)]
            i += 1
        elif cmd == "A":
            rx, ry, rot, la, sw, x, y = toks[i:i + 7]
            rot = fmt(float(rot) + (deg if rx != ry else 0))
            cur = (float(x), float(y))
            out.append(f"{rx} {ry} {rot} {la} {sw} " + tp(*cur))
            i += 7
        else:
            cur = (float(toks[i]), float(toks[i + 1]))
            if cmd == "M":
                start = cur
            out.append(tp(*cur))
            i += 2
    s = ""
    for t in out:
        s += t if (len(t) == 1 and t in "MLCQAZ") else (t if s and s[-1] in "MLCQAZ" else " " + t)
    return s


def rotd(d, deg, cx=12.0, cy=12.0, dx=0.0, dy=0.0):
    """Rotate a closed outline via pathops (any SVG commands)."""
    a, b, c, d_, e, f = rotation(deg, cx, cy)
    return path_to_d(transform_path(P(d), (a, b, c, d_, e + dx, f + dy)))


def scaled(d, s, dx=0.0, dy=0.0):
    """Scale a closed outline about the origin, then translate."""
    return path_to_d(transform_path(P(d), (s, 0, 0, s, dx, dy)))


def behind(back_d, fronts, gap=1.75):
    """Outline (d) of the part of back_d not hidden by the front shapes, kept `gap` clear of their strokes.
    gap=None attaches the back shape to the front outline (their strokes merge)."""
    if gap is None:
        cut = U(*[P(f) for f in fronts])
    else:
        cut = U(*[U(P(f), ST(f, 2 * (gap + 2), "round", "round")) for f in fronts])
    return path_to_d(D(P(back_d), cut))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def pt_on(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def rot_pts(points, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in points]


def capsule(x1, y1, x2, y2, w, rc=None):
    """Bar of width w along (x1, y1)-(x2, y2) with end corners of radius rc (w / 2 = stadium)."""
    rc = w / 2 if rc is None else min(rc, w / 2)
    ln = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / ln, (y2 - y1) / ln
    nx, ny = -uy * w / 2, ux * w / 2
    d = rect(0, -w / 2, ln, w, rc)
    a = math.degrees(math.atan2(uy, ux))
    ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
    del nx, ny
    return path_to_d(transform_path(P(d), (ca, sa, -sa, ca, x1, y1)))


def blob(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def oval_dot(cx, cy, rx, ry) -> Part:
    return Part("dot", ellipse(cx, cy, rx, ry))


def mark(d) -> Part:
    return Part("dot", d)


def leaf(x1, y1, x2, y2, bulge):
    """Closed pointed leaf from (x1, y1) to (x2, y2); bulge = half width."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    b = bulge * 2
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx * b)} {fmt(my + ny * b)} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(mx - nx * b)} {fmt(my - ny * b)} {fmt(x1)} {fmt(y1)}Z")


def scallop_ring(cx, cy, R, n, bulge=1.1, start=-90.0):
    pts = [pt_on(cx, cy, R, start + i * 360 / n) for i in range(n)]
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    br = R * math.sin(math.pi / n) * bulge
    for i in range(n):
        x, y = pts[(i + 1) % n]
        d += f"A{fmt(br)} {fmt(br)} 0 0 1 {fmt(x)} {fmt(y)}"
    return d + "Z"


def bumps(pts, r=None, sweep=1):
    """Open path of arcs through pts (sweep 1 bulges left of travel, i.e. up when going right)."""
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        ch = math.hypot(x1 - x0, y1 - y0)
        rr = max(r or ch * 0.62, ch / 2 + 0.01)
        d += f"A{fmt(rr)} {fmt(rr)} 0 0 {sweep} {fmt(x1)} {fmt(y1)}"
    return d


def earc(cx, cy, rx, ry, a0, a1):
    """Elliptical arc clockwise on screen from angle a0 to a1 (degrees, 0 = right, 90 = down)."""
    x0, y0 = cx + rx * math.cos(math.radians(a0)), cy + ry * math.sin(math.radians(a0))
    x1, y1 = cx + rx * math.cos(math.radians(a1)), cy + ry * math.sin(math.radians(a1))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{fmt(x0)} {fmt(y0)}A{fmt(rx)} {fmt(ry)} 0 {large} 1 {fmt(x1)} {fmt(y1)}"


def ell_chord(cx, cy, rx, ry, c, kind, inset=0.0):
    """Chord of ellipse along x + y = c ('/') or x - y = c ('\\'), shortened by inset at both ends."""
    if kind == "/":
        v = (1 / math.sqrt(2), -1 / math.sqrt(2))
        p0 = ((c - cy + cx) / 2, (c + cy - cx) / 2)
    else:
        v = (1 / math.sqrt(2), 1 / math.sqrt(2))
        p0 = ((c + cx + cy) / 2, (cx + cy - c) / 2)
    ax, ay = (p0[0] - cx) / rx, (p0[1] - cy) / ry
    bx, by = v[0] / rx, v[1] / ry
    A = bx * bx + by * by
    B = 2 * (ax * bx + ay * by)
    C = ax * ax + ay * ay - 1
    disc = math.sqrt(B * B - 4 * A * C)
    t1, t2 = (-B - disc) / (2 * A) + inset, (-B + disc) / (2 * A) - inset
    return seg(p0[0] + t1 * v[0], p0[1] + t1 * v[1], p0[0] + t2 * v[0], p0[1] + t2 * v[1])


def loaf(x0, x1, top, bot, R, sh=None, k=0.45):
    """Side-view loaf: straight sides up to the shoulder sh, domed top at `top`, flat base with corner radius R."""
    sh = top + (bot - top) * 0.45 if sh is None else sh
    mid = (x0 + x1) / 2
    d = (f"M{fmt(x0)} {fmt(bot - R)}V{fmt(sh)}C{fmt(x0)} {fmt(top + (sh - top) * 0.1)} {fmt(x0 + (mid - x0) * k)} {fmt(top)} {fmt(mid)} {fmt(top)}"
         f"C{fmt(x1 - (x1 - mid) * k)} {fmt(top)} {fmt(x1)} {fmt(top + (sh - top) * 0.1)} {fmt(x1)} {fmt(sh)}V{fmt(bot - R)}")
    if R:
        d += f"A{fmt(R)} {fmt(R)} 0 0 1 {fmt(x1 - R)} {fmt(bot)}"
    d += f"H{fmt(x0 + R)}"
    if R:
        d += f"A{fmt(R)} {fmt(R)} 0 0 1 {fmt(x0)} {fmt(bot - R)}"
    return d + "Z"


def _p(p):
    return f"{fmt(p[0])} {fmt(p[1])}"


def tip(a, p, b, r):
    """Corner at p (coming from a, leaving towards b): sharp when r == 0, softened with a quadratic when r > 0."""
    if r <= 0:
        return "L" + _p(p)
    la = math.hypot(a[0] - p[0], a[1] - p[1])
    lb = math.hypot(b[0] - p[0], b[1] - p[1])
    t = min(r, la / 2, lb / 2)
    s = (p[0] + (a[0] - p[0]) * t / la, p[1] + (a[1] - p[1]) * t / la)
    e = (p[0] + (b[0] - p[0]) * t / lb, p[1] + (b[1] - p[1]) * t / lb)
    return "L" + _p(s) + "Q" + _p(p) + " " + _p(e)


SLICE = ("M4.5 {b}V11.5C3.2 10.9 2.5 9.7 2.5 8.2C2.5 5.1 5.5 3 9.5 3H14.5C18.5 3 21.5 5.1 21.5 8.2"
         "C21.5 9.7 20.8 10.9 19.5 11.5V{b}")


def bread_slice(S):
    """A slice of bread seen face on, crown at the top (body x 4.5 to 19.5, y 3 to 21)."""
    if S.name == "line":
        return SLICE.format(b=21) + "Z"
    return SLICE.format(b=19) + "A2 2 0 0 1 17.5 21H6.5A2 2 0 0 1 4.5 19Z"


def edge_behind(back_d, fronts, S, gap=1.0):
    """Visible part of back_d's outline stroke, kept `gap` clear of the front shapes' strokes (solid mark)."""
    cut = U(*[U(P(f), ST(f, 2 * (gap + 1), "round", "round")) for f in fronts])
    return solid(path_to_d(D(ST(back_d, 2, S.cap, S.join), cut)))


def spiral(cx, cy, r0, h, halves, ratio=1.0, start_right=True):
    """Spiral of half-ellipse arcs: radius grows by h every half turn; ratio squashes it vertically."""
    x = cx + r0 if start_right else cx - r0
    d = f"M{fmt(x)} {fmt(cy)}"
    centres = (cx, cx + h) if start_right else (cx, cx - h)
    for k in range(halves):
        c = centres[k % 2]
        r = abs(x - c)
        x = 2 * c - x
        d += f"A{fmt(r)} {fmt(r * ratio)} 0 0 1 {fmt(x)} {fmt(cy)}"
    return d


def hull2(c1, r1, c2, r2):
    """Closed outline around two circles (centres on a vertical line, c1 below c2) and their tangents."""
    dd = c1[1] - c2[1]
    sa = (r1 - r2) / dd
    ca = math.sqrt(1 - sa * sa)
    x = c1[0]
    return (f"M{fmt(x + r1 * ca)} {fmt(c1[1] - r1 * sa)}L{fmt(x + r2 * ca)} {fmt(c2[1] - r2 * sa)}"
            f"A{fmt(r2)} {fmt(r2)} 0 1 0 {fmt(x - r2 * ca)} {fmt(c2[1] - r2 * sa)}"
            f"L{fmt(x - r1 * ca)} {fmt(c1[1] - r1 * sa)}A{fmt(r1)} {fmt(r1)} 0 1 0 {fmt(x + r1 * ca)} {fmt(c1[1] - r1 * sa)}Z")


def tube(d, w):
    """Closed outline of a round-ended stroke of width w along d."""
    return path_to_d(ST(d, w, "round", "round"))


# =========================================================================== loaves and breads

@icon("baguette", CAT, "A long thin baguette lying diagonally with slanted score marks",
      tags=["french bread", "french stick", "loaf", "bakery", "bread"], aliases=["french-stick"])
def _(S):
    body = rotd(capsule(1.8, 12, 22.2, 12, 7, L(S, 2.2, 3.5)), -45)
    scores = [xf(seg(u - 1.5, 13.6, u + 1.5, 10.4), -45) for u in (6.2, 10.2, 14.2, 18.2)]
    return [shell(body), *(detail(s) for s in scores)]


def _bagel_outline():
    return "M3 9.5A9 5.5 0 0 1 21 9.5V14A9 5.5 0 0 1 3 14Z"


def _bagel_hole(S):
    if S.name == "line":
        return "M8.5 9.5Q12 5.6 15.5 9.5Q12 13.4 8.5 9.5Z"
    return ellipse(12, 9.5, 3.5, 1.9)


def _bagel_filled():
    o = _bagel_outline()
    body = U(P(o), ST(o, 2))
    return D(body, ST("M3 9.5A9 5.5 0 0 0 21 9.5", 2), P(ellipse(12, 9.5, 4.5, 2.9)))


@icon("bagel", CAT, "A thick bagel seen at a slight angle with its round hole",
      tags=["bread ring", "breakfast", "bakery", "deli", "brunch"], filled=_bagel_filled)
def _(S):
    return [shell(_bagel_outline()), detail("M3 9.5A9 5.5 0 0 0 21 9.5"), line(_bagel_hole(S))]


@icon("brioche", CAT, "A brioche with a fluted base and a round knob of dough on top",
      tags=["brioche a tete", "french bread", "sweet bread", "bakery", "breakfast"])
def _(S):
    head = circle(12, 6.6, 3.8)
    top = bumps([(2.5, 13.2), (7.25, 13.2), (12, 13.2), (16.75, 13.2), (21.5, 13.2)], r=2.9)
    base = top + ("L18.2 20.5H5.8Z" if S.name == "line" else "L18.6 19.3Q18.3 20.5 17 20.5H7Q5.7 20.5 5.4 19.3Z")
    base = behind(base, [head], 1.0)
    return [shell(head), shell(base), detail(seg(7.25, 13.4, 8.8, 20.5)), detail(seg(12, 13.4, 12, 20.5)),
            detail(seg(16.75, 13.4, 15.2, 20.5))]


def _challah(S):
    top = bumps([(2.5, 12.5), (7.3, 8), (12, 7), (16.7, 8), (21.5, 12.5)], r=3.2)
    bot = bumps([(21.5, 12.5), (16.7, 17), (12, 18), (7.3, 17), (2.5, 12.5)], r=3.2)
    return top + bot[bot.index("A"):] + "Z"


@icon("challah", CAT, "A plump braided loaf with its woven strands",
      tags=["braided bread", "plaited loaf", "shabbat", "jewish bread", "bakery"])
def _(S):
    ups = [seg(x - 1.5, 12.5, x + 0.8, 9) for x in (7.3, 12, 16.7)]
    downs = [seg(x - 0.8, 16, x + 1.5, 12.5) for x in (9.65, 14.35)]
    return [shell(_challah(S)), *(detail(u) for u in ups), *(detail(v) for v in downs)]


@icon("ciabatta", CAT, "A flat wide ciabatta loaf with flour streaks on top",
      tags=["italian bread", "slipper bread", "loaf", "bakery", "sandwich bread"])
def _(S):
    R = L(S, 1.5, 3.5)
    d = (f"M2.5 {fmt(18 - R)}V11.5C2.5 8.5 4.5 7.2 7.5 7.6C10 8 13.5 7 16.5 7.2C19.8 7.4 21.5 9 21.5 11.5V{fmt(18 - R)}"
         f"A{R} {R} 0 0 1 {fmt(21.5 - R)} 18H{fmt(2.5 + R)}A{R} {R} 0 0 1 2.5 {fmt(18 - R)}Z")
    return [shell(d), detail("M6 12.8Q7.8 11.5 9.8 11.6"), detail("M11 14.2Q13 13 15 13.2"), detail("M14.5 10.9Q16.3 9.9 18.2 10.1")]


@icon("focaccia", CAT, "A flat slab of focaccia seen from above, covered in dimples",
      tags=["italian bread", "flatbread", "dimpled bread", "bakery", "olive oil bread"])
def _(S):
    dims = [(7, 8.5), (12, 8.5), (17, 8.5), (9.5, 12), (14.5, 12), (7, 15.5), (12, 15.5), (17, 15.5)]
    return [shell(rect(3, 4.5, 18, 15, S.R)), *(dot(x, y, 1.05) for x, y in dims)]


@icon("cottage-loaf", CAT, "A cottage loaf: a small round bun sitting on a larger one, with a dimple on top",
      tags=["english loaf", "round loaf", "two tier bread", "bakery", "farmhouse bread"])
def _(S):
    top = ellipse(12, 8.2, 5.6, 4.6)
    bottom = loaf(2.5, 21.5, 10.3, 20.5, L(S, 1.5, 3.5), sh=15.5, k=0.3)
    return [shell(top), shell(behind(bottom, [top], 1.0)), dot(12, 7.4, 1.2)]


@icon("sliced-bread", CAT, "Three slices of bread stacked one behind the other",
      tags=["bread slices", "loaf", "sandwich bread", "toast", "bakery"])
def _(S):
    s = bread_slice(S)
    front = scaled(s, 0.68, 0.5, 6.7)
    mid = scaled(s, 0.68, 3.5, 4.2)
    back = scaled(s, 0.68, 6.5, 1.7)
    return [shell(front), edge_behind(mid, [front], S), edge_behind(back, [mid, front], S)]


def _rye_body(S):
    if S.name == "line":
        return "M2.5 12.5C5 8.3 8.3 6.5 12 6.5C15.7 6.5 19 8.3 21.5 12.5C19 16.7 15.7 18.5 12 18.5C8.3 18.5 5 16.7 2.5 12.5Z"
    return ellipse(12, 12.5, 9.5, 6.2)


@icon("rye-bread", CAT, "An oval rye loaf with a diamond pattern scored across the top",
      tags=["rye loaf", "dark bread", "pumpernickel", "sourdough", "bakery"])
def _(S):
    cuts = [ell_chord(12, 12.5, 8, 4.6, c, k, 0.3) for c, k in ((20.5, "/"), (28.5, "/"), (-4, "\\"), (4, "\\"))]
    return [shell(_rye_body(S)), *(detail(c) for c in cuts)]


def _epi_lobes(S):
    o, u, n = (3.2, 20.8), (1 / math.sqrt(2), -1 / math.sqrt(2)), (1 / math.sqrt(2), 1 / math.sqrt(2))

    def at(s, k):
        return (o[0] + u[0] * s + n[0] * k, o[1] + u[1] * s + n[1] * k)
    lobes = []
    for i, s in enumerate((3.5, 7.3, 11.1, 14.9)):
        side = 1 if i % 2 == 0 else -1
        a, b = at(s, 0), at(s + 4.2, side * 4.4)
        lobes.append(leaf(*a, *b, 2.1))
    lobes.append(leaf(*at(17.2, 0), *at(24.2, 0), 2.1))
    return lobes, (at(0, 0), at(17.2, 0))


@icon("epi-bread", CAT, "An epi baguette cut into alternating pointed lobes like an ear of wheat",
      tags=["pain d'epi", "wheat stalk bread", "baguette", "french bread", "bakery"])
def _(S):
    lobes, (a, b) = _epi_lobes(S)
    parts = [line(seg(*a, *b))]
    return parts + [shell(lb) for lb in lobes]


def _fougasse(S):
    r = L(S, 0, 2.2)
    a, p, b = (8, 6.2), (12, 2.5), (16, 6.2)
    return ("M3.5 15.5C3.5 11.5 5.5 8.5 8 6.2" + tip(a, p, b, r) + "L16 6.2"
            "C18.5 8.5 20.5 11.5 20.5 15.5C20.5 19.5 17 21.5 12 21.5C7 21.5 3.5 19.5 3.5 15.5Z")


@icon("fougasse", CAT, "A flat leaf-shaped fougasse with a centre slit and angled slits on each side",
      tags=["provencal bread", "leaf bread", "flatbread", "french bread", "bakery"])
def _(S):
    slits = [seg(12, 8.5, 12, 18.5), seg(9.6, 12.6, 7.4, 10.8), seg(14.4, 12.6, 16.6, 10.8),
             seg(9.6, 17.6, 6.6, 15.4), seg(14.4, 17.6, 17.4, 15.4)]
    return [shell(_fougasse(S)), *(detail(s) for s in slits)]


@icon("pita", CAT, "Half a round pita bread with its pocket opened along the cut edge",
      tags=["pitta", "pocket bread", "flatbread", "middle eastern bread", "bakery"], aliases=["pitta"])
def _(S):
    k = dict(deg=-18, cx=12, cy=12)
    r = L(S, 0, 1.6)
    body = "M3 10Q12 6.5 21 10A9 9 0 0 1 3 10Z"
    if S.name == "rounded":
        body = "M4.2 9.4Q12 6.5 19.8 9.4Q21.2 10 21 11.4A9 9 0 0 1 3 11.4Q2.8 10 4.2 9.4Z"
    pocket = "M5.5 10.6Q12 8.6 18.5 10.6Q12 14.2 5.5 10.6Z"
    return [shell(xf(body, **k)), mark(xf(pocket, **k))]


@icon("naan", CAT, "A teardrop-shaped naan flatbread with charred bubbles",
      tags=["nan", "indian bread", "flatbread", "tandoor", "curry"], aliases=["nan-bread"])
def _(S):
    r = L(S, 0, 2.6)
    d = ("M3 15.5C3 10.5 8 7 13.5 5.7" + tip((13.5, 5.7), (20.8, 3.4), (19.2, 10.2), r)
         + "L19.2 10.2C17.5 15.5 12.8 20.3 7.8 20.5C5 20.6 3 18.5 3 15.5Z")
    return [shell(d), dot(7.8, 15.4, 1.4), dot(12.2, 10.8, 1.1), dot(13, 15.6, 0.95)]


@icon("tortillas", CAT, "A stack of thin round tortillas with toasted spots on the top one",
      tags=["tortilla", "flatbread", "wraps", "mexican food", "corn tortilla"])
def _(S):
    top = ellipse(12, 8.5, 9, 4.2)
    layers = [earc(12, 12.2, 9, 4.2, 0, 180), earc(12, 15.9, 9, 4.2, 0, 180)]
    spots = [oval_dot(8.5, 8, 1.1, 0.8), oval_dot(13.5, 7, 1, 0.75), oval_dot(15.5, 9.8, 0.9, 0.7)]
    if S.name == "rounded":
        spots = [dot(8.5, 8, 1), dot(13.5, 7, 0.9), dot(15.5, 9.8, 0.85)]
    return [shell(top), *(line(l) for l in layers), *spots]


@icon("paratha", CAT, "A round flatbread seen from above with a spiral of flaky layers",
      tags=["parotta", "layered flatbread", "indian bread", "flatbread", "lachha paratha"], aliases=["parotta"])
def _(S):
    body = ellipse(12, 12, 9.5, 8.5) if S.name == "rounded" else poly(regular(12, 12, 9.7, 14, -90), closed=True)
    return [shell(body), detail(spiral(12, 12, 0.9, 1.9, 5, 0.9))]


@icon("bread-roll", CAT, "A small round dinner roll with a single slash across its dome",
      tags=["dinner roll", "bun", "bread", "bakery", "bap"], aliases=["dinner-roll"])
def _(S):
    r = L(S, 0, 1.5)
    body = ("M3.5 18C2.5 16.5 2.5 15 2.5 14C2.5 9.2 6.8 6 12 6C17.2 6 21.5 9.2 21.5 14C21.5 15 21.5 16.5 20.5 18"
            + tip((20.5, 18), (19.5, 19.5), (4.5, 19.5), r) + tip((19.5, 19.5), (4.5, 19.5), (3.5, 18), r) + "Z")
    return [shell(body), detail("M6.5 13.2Q10.5 8.6 17 10")]


def _kaiser_folds():
    out = []
    for i in range(5):
        a = -90 + i * 72
        p0 = pt_on(12, 12, 2.4, a)
        p1 = pt_on(12, 12, 7.6, a + 38)
        c = pt_on(12, 12, 6.2, a + 5)
        out.append(f"M{_p(p0)}Q{_p(c)} {_p(p1)}")
    return out


@icon("kaiser-roll", CAT, "A round kaiser roll seen from above with five curved folds like a pinwheel",
      tags=["kaiser bun", "vienna roll", "hard roll", "bread roll", "bakery"])
def _(S):
    body = circle(12, 12, 9.2) if S.name == "rounded" else poly(regular(12, 12, 9.6, 15, -90), closed=True)
    return [shell(body), *(detail(f) for f in _kaiser_folds())]


@icon("burger-bun", CAT, "An empty split burger bun: a sesame-topped dome floating above a flat base",
      tags=["hamburger bun", "bun", "sesame bun", "bread roll", "bakery"])
def _(S):
    R = L(S, 1, 2)
    top = (f"M3 {fmt(11.5 - R)}C3 6.5 7 3.5 12 3.5C17 3.5 21 6.5 21 {fmt(11.5 - R)}"
           f"A{R} {R} 0 0 1 {fmt(21 - R)} 11.5H{fmt(3 + R)}A{R} {R} 0 0 1 3 {fmt(11.5 - R)}Z")
    Rb = L(S, 0.5, 1.5)
    bottom = (f"M{fmt(3 + Rb)} 15H{fmt(21 - Rb)}A{Rb} {Rb} 0 0 1 21 {fmt(15 + Rb)}V16C21 18.8 18.5 20.5 15.5 20.5"
              f"H8.5C5.5 20.5 3 18.8 3 16V{fmt(15 + Rb)}A{Rb} {Rb} 0 0 1 {fmt(3 + Rb)} 15Z")
    return [shell(top), shell(bottom), oval_dot(8, 7.8, 1.1, 0.7), oval_dot(12, 6.4, 1.1, 0.7), oval_dot(16, 7.8, 1.1, 0.7)]


def _hotdog_bun(S):
    return rect(2.5, 7.5, 19, 11, L(S, 3, 5.5))


@icon("hot-dog-bun", CAT, "A long soft hot dog bun split open along its top",
      tags=["hotdog bun", "finger roll", "bread roll", "sausage roll bun", "bakery"])
def _(S):
    body = rotd(capsule(2.2, 12, 21.8, 12, 9.5, L(S, 3, 4.75)), -30)
    gap = xf("M5.5 11.2Q12 17 18.5 11.2Q12 8.6 5.5 11.2Z", -30)
    return [shell(body), mark(gap)]


def zig(x0, x1, y, amp, n):
    w = (x1 - x0) / n
    pts = [(x0, y)]
    for i in range(n):
        pts.append((x0 + w * (i + 0.5), y - amp))
        pts.append((x0 + w * (i + 1), y))
    return pts


@icon("english-muffin", CAT, "An english muffin split in half with rough, craggy inner faces",
      tags=["breakfast muffin", "muffin", "toasted muffin", "breakfast", "bakery"])
def _(S):
    R = L(S, 1, 2.5)
    top = (f"M3 10V{fmt(3.5 + R)}A{R} {R} 0 0 1 {fmt(3 + R)} 3.5H{fmt(21 - R)}A{R} {R} 0 0 1 21 {fmt(3.5 + R)}V10"
           "Q19.5 8.5 18 10T15 10Q13.8 8.2 12 10Q10.2 11.4 9 9.8T6 10Q4.5 11.5 3 10Z")
    bottom = ("M3 14.5Q4.5 13 6 14.5T9 14.7Q10.2 13.1 12 14.5Q13.8 16.3 15 14.5T18 14.5Q19.5 13 21 14.5"
              f"V{fmt(20.5 - R)}A{R} {R} 0 0 1 {fmt(21 - R)} 20.5H{fmt(3 + R)}A{R} {R} 0 0 1 3 {fmt(20.5 - R)}Z")
    return [shell(top), shell(bottom), dot(7.5, 17.5, 0.9), dot(12, 18, 0.9), dot(16.5, 17.5, 0.9)]


@icon("crumpet", CAT, "A thick round crumpet seen at an angle with small holes across its top",
      tags=["griddle cake", "british breakfast", "tea time", "pikelet", "bakery"])
def _(S):
    o = "M3 9.5A9 5.5 0 0 1 21 9.5V14A9 5.5 0 0 1 3 14Z"
    holes = [(7.2, 9.2), (11.2, 7.2), (15.4, 7.8), (12.4, 11.2), (16.8, 10.8)]
    return [shell(o), detail("M3 9.5A9 5.5 0 0 0 21 9.5"), *(dot(x, y, 0.95 if S.name == "line" else 1.05) for x, y in holes)]


@icon("buttermilk-biscuit", CAT, "A tall round biscuit in side view with stacked flaky layers",
      tags=["southern biscuit", "biscuit", "breakfast", "scone", "bakery"])
def _(S):
    R = L(S, 1.5, 3)
    body = loaf(4, 20, 4, 20.5, R, sh=7, k=0.3)
    return [shell(body), detail("M4 10.5Q8 9.5 12 10.5T20 10.5"), detail("M4 15.5Q8 14.5 12 15.5T20 15.5")]


@icon("cornbread", CAT, "A square piece of cornbread with crumb dots and a pat of butter on top",
      tags=["corn bread", "johnnycake", "southern food", "square", "bakery"])
def _(S):
    R = L(S, 1.5, 3)
    butter = rotd(rect(8.5, 3, 7, 5, L(S, 0.5, 1.5)), -8)
    body = behind(rect(3, 7, 18, 14, R), [butter], 0.8)
    crumbs = [(7.5, 12.5), (12, 13.5), (16.5, 12.5), (9.5, 17), (14.5, 17)]
    return [shell(butter), shell(body), *(dot(x, y, 1) for x, y in crumbs)]


@icon("breadsticks", CAT, "Thin crisp breadsticks standing in a tall glass",
      tags=["grissini", "bread sticks", "italian", "appetizer", "snack"], aliases=["grissini"])
def _(S):
    glass = rect(7, 12, 10, 9.5, L(S, 1, 2.5))
    sticks = [seg(10, 12, 5, 2.5), seg(12.5, 12, 12.5, 2.2), seg(15, 12, 19.5, 3.5)]
    return [shell(glass), *(line(s) for s in sticks), detail(seg(7, 15, 17, 15))]


@icon("toast-slice", CAT, "A single slice of toast with a pat of butter melting on it",
      tags=["toast", "buttered toast", "breakfast", "bread slice", "slice"])
def _(S):
    butter = ("M8.5 10H15.5V14.5H13.2V16.2A1.2 1.2 0 0 1 10.8 16.2V14.5H8.5Z" if S.name == "line" else
              "M9.8 10H14.2A1.3 1.3 0 0 1 15.5 11.3V13.2A1.3 1.3 0 0 1 14.2 14.5H13.2V16.2A1.2 1.2 0 0 1 10.8 16.2V14.5H9.8A1.3 1.3 0 0 1 8.5 13.2V11.3A1.3 1.3 0 0 1 9.8 10Z")
    return [shell(bread_slice(S)), detail(butter)]


@icon("french-toast", CAT, "Two slices of french toast with a pat of butter and syrup running down",
      tags=["eggy bread", "pain perdu", "brunch", "breakfast", "maple syrup"], aliases=["eggy-bread"])
def _(S):
    s = bread_slice(S)
    front = scaled(s, 0.78, 0.4, 5.2)
    back = scaled(s, 0.78, 4.4, 1.7)
    butter = rect(7, 9.8, 6, 3.4, L(S, 0.5, 1.2))
    syrup = "M3.9 15.5Q5.5 14.7 7 15.5V18A1.25 1.25 0 0 0 9.5 18V15.7Q11.5 15 13 15.7V16.6A1.25 1.25 0 0 0 15.5 16.6V15.5Q16 15.1 16.6 15.2"
    return [shell(front), edge_behind(back, [front], S), detail(butter), detail(syrup)]


@icon("concha", CAT, "A domed concha sweet bun with a shell pattern scored into its sugar topping",
      tags=["pan dulce", "mexican sweet bread", "sweet bun", "panaderia", "bakery"])
def _(S):
    R = L(S, 1.5, 3)
    body = (f"M2.5 {fmt(19.5 - R)}V15C2.5 9 7 5 12 5C17 5 21.5 9 21.5 15V{fmt(19.5 - R)}"
            f"A{R} {R} 0 0 1 {fmt(21.5 - R)} 19.5H{fmt(2.5 + R)}A{R} {R} 0 0 1 2.5 {fmt(19.5 - R)}Z")
    return [shell(body), detail("M2.5 14.2Q12 17.6 21.5 14.2"), detail("M12 15.6V7"),
            detail("M10 15.4Q7.2 11.5 6.2 8.6"), detail("M14 15.4Q16.8 11.5 17.8 8.6")]


@icon("pan-de-muerto", CAT, "A round domed pan de muerto with crossed bone-shaped strips and a ball on top",
      tags=["bread of the dead", "day of the dead", "dia de muertos", "mexican bread", "sweet bread"])
def _(S):
    R = L(S, 1.5, 3)
    ball = circle(12, 5.6, 2.6)
    body = (f"M2.5 {fmt(20 - R)}V16C2.5 11 6.5 8 12 8C17.5 8 21.5 11 21.5 16V{fmt(20 - R)}"
            f"A{R} {R} 0 0 1 {fmt(21.5 - R)} 20H{fmt(2.5 + R)}A{R} {R} 0 0 1 2.5 {fmt(20 - R)}Z")
    return [shell(ball), shell(behind(body, [ball], 0.8)), detail("M9.6 10.2Q6.2 13 5.6 19.5"), detail("M14.4 10.2Q17.8 13 18.4 19.5"),
            dot(7, 14.6, 1.6), dot(17, 14.6, 1.6), detail("M12 11V19.5"), dot(12, 15.2, 1.6)]


@icon("panettone", CAT, "A tall panettone with a domed top rising out of its paper band",
      tags=["christmas bread", "italian sweet bread", "fruit bread", "holiday", "bakery"])
def _(S):
    R = L(S, 1, 2.5)
    dome = "M3.5 11C3.5 6.2 7.5 3 12 3C16.5 3 20.5 6.2 20.5 11Z"
    band = f"M5.5 10H18.5V{fmt(21 - R)}A{R} {R} 0 0 1 {fmt(18.5 - R)} 21H{fmt(5.5 + R)}A{R} {R} 0 0 1 5.5 {fmt(21 - R)}Z"
    return [shell(union(dome, band)), detail(seg(4.5, 11, 19.5, 11)), dot(9, 7.2, 1), dot(14.5, 6.4, 1), dot(12.5, 8.8, 0.9)]


@icon("babka", CAT, "A babka loaf with its cut end showing a swirl of chocolate",
      tags=["chocolate babka", "swirl bread", "jewish bakery", "sweet loaf", "bakery"])
def _(S):
    R = L(S, 1.5, 3)
    face = loaf(2.5, 13.5, 6, 20.5, R, sh=9.5, k=0.4)
    body = loaf(6, 21.5, 3.5, 17.5, R, sh=7, k=0.4)
    return [shell(face), shell(behind(body, [face], 1.0)), detail(spiral(8, 14, 0.8, 1.6, 3, 1.0))]


@icon("banana-bread", CAT, "A loaf of banana bread with half a banana lying on top",
      tags=["banana loaf", "quick bread", "loaf cake", "baking", "bakery"])
def _(S):
    R = L(S, 1.5, 3)
    cake = f"M2.5 11H21.5V{fmt(20.5 - R)}A{R} {R} 0 0 1 {fmt(21.5 - R)} 20.5H{fmt(2.5 + R)}A{R} {R} 0 0 1 2.5 {fmt(20.5 - R)}Z"
    r = L(S, 0, 1)
    banana = ("M4.5 7.5" + tip((4.5, 7.5), (3.2, 5.5), (6.5, 6.5), r) + "L6.5 6.5C10 7.8 14 7.8 17.5 6.3"
              "C18.8 5.8 20 5.2 20.8 4.4C21 7 19 9.6 15 10.3C11 11 7 10 4.5 7.5Z")
    return [shell(banana), shell(behind(cake, [banana], 0.8)), dot(7.5, 16, 1), dot(12, 17, 1), dot(16.5, 16, 1)]


@icon("sourdough-starter", CAT, "A jar of bubbly sourdough starter with a loose lid",
      tags=["levain", "starter jar", "wild yeast", "fermentation", "sourdough"])
def _(S):
    R = L(S, 1.5, 3.5)
    jar = rect(4.5, 7, 15, 14.5, R)
    lid = rotd(rect(4, 2.6, 13, 2.8, L(S, 0.5, 1.4)), -8, 10.5, 4)
    dough = "M4.5 12.5Q6.4 10.8 8.3 12.5T12 12.5T15.7 12.5T19.5 12.5"
    return [shell(jar), shell(lid), detail(dough), dot(9, 16.5, 1.1), dot(14.5, 15.5, 1.1), dot(12.2, 18.6, 0.9)]


@icon("dough-ball", CAT, "A smooth ball of dough resting on a floured work surface",
      tags=["pizza dough", "bread dough", "kneading", "baking", "proofing"])
def _(S):
    body = "M3.5 14.8C3.5 10 7.3 7 12 7C16.7 7 20.5 10 20.5 14.8C20.5 17.6 17.2 18.5 12 18.5C6.8 18.5 3.5 17.6 3.5 14.8Z"
    return [shell(body), line(seg(2, 21.5, 22, 21.5) if S.name == "line" else seg(2.5, 21.5, 21.5, 21.5)),
            dot(4, 4.5, 1), dot(19.5, 4, 1), dot(15.5, 3, 0.9), dot(8, 3.2, 0.9)]


@icon("proofing-bowl", CAT, "A bowl covered with a checked cloth that bulges up from the rising dough",
      tags=["proving bowl", "rising dough", "bread proofing", "covered bowl", "baking"])
def _(S):
    top = 11.5
    bowl = (f"M2.5 {top}L21.5 {top}C21.5 {top + 5} 17.5 {top + 9.5} 12 {top + 9.5}C6.5 {top + 9.5} 2.5 {top + 5} 2.5 {top}Z")
    r = L(S, 0, 1.2)
    cloth = ("M4 11.2C4 7 7.5 4 12 4C16.5 4 20 7 20 11.2" + tip((20, 11.2), (20.8, 13.4), (18.4, 12.6), r)
             + "L18.4 12.6Q12 11.4 5.6 12.6" + tip((5.6, 12.6), (3.2, 13.4), (4, 11.2), r) + "Z")
    return [shell(cloth), shell(behind(bowl, [cloth], 0.8)), detail(seg(9.5, 4.8, 9.5, 11.8)), detail(seg(14.5, 4.8, 14.5, 11.8)),
            detail(seg(5, 8.2, 19, 8.2))]


@icon("flour-sack", CAT, "A tied cloth sack of flour with a wheat ear printed on the front",
      tags=["flour bag", "sack of flour", "baking", "wheat", "mill"])
def _(S):
    r = L(S, 0, 1.2)
    sack = ("M9 8.5C5 10 3.5 13.5 3.5 17C3.5 20 5 21 7.5 21H16.5C19 21 20.5 20 20.5 17C20.5 13.5 19 10 15 8.5Z")
    top = poly([(9, 7), (7.5, 2.8), (12, 4.2), (16.5, 2.8), (15, 7)], closed=True, r=r)
    return [shell(top), shell(behind(sack, [top], 0.6)), detail(seg(12, 19, 12, 12)),
            detail("M12 15.8L9.8 13.8"), detail("M12 15.8L14.2 13.8"), detail("M12 12.6L10.2 11"), detail("M12 12.6L13.8 11")]


def _cinnamon_outline():
    return "M12 21A9 9 0 1 1 21 12H18.2"


@icon("cinnamon-roll", CAT, "A thick cinnamon roll seen at an angle with its spiral of dough on top",
      tags=["cinnamon bun", "sticky bun", "sweet roll", "pastry", "bakery"], aliases=["cinnamon-bun"])
def _(S):
    o = "M3 10A9 7.2 0 0 1 21 10V13.8A9 7.2 0 0 1 3 13.8Z"
    sp = spiral(12, 10, 1.1, 2.1, 4, 0.8, start_right=False)
    return [shell(o), detail("M3 10A9 7.2 0 0 0 21 10"), detail(sp)]


@icon("pain-au-chocolat", CAT, "A rectangular flaky pastry with bars of chocolate peeking out of its end",
      tags=["chocolate croissant", "chocolatine", "french pastry", "viennoiserie", "breakfast"],
      aliases=["chocolatine"])
def _(S):
    R = L(S, 2, 4)
    body = rect(2.5, 5.5, 16, 13, R)
    chocs = [rect(16, 8, 6, 2.6, L(S, 0.3, 1.3)), rect(16, 13.4, 6, 2.6, L(S, 0.3, 1.3))]
    return [shell(body), detail("M6.5 6Q8.2 12 6.5 18"), detail("M11 6Q12.7 12 11 18"),
            *(solid(minus(c, rect(1.5, 4.5, 18, 15, R + 1))) for c in chocs)]


@icon("danish-pastry", CAT, "A square danish with its corners folded over and a round fruit filling",
      tags=["danish", "fruit danish", "breakfast pastry", "viennoiserie", "bakery"], aliases=["danish"])
def _(S):
    R = L(S, 1.5, 3)
    folds = [seg(3.5, 9, 9, 3.5), seg(15, 3.5, 20.5, 9), seg(3.5, 15, 9, 20.5), seg(15, 20.5, 20.5, 15)]
    return [shell(rect(3, 3, 18, 18, R)), shell(circle(12, 12, 3.6)), *(detail(f) for f in folds)]


@icon("eclair", CAT, "A long eclair with a smooth glaze covering its top",
      tags=["chocolate eclair", "choux pastry", "french pastry", "patisserie", "dessert"])
def _(S):
    body = rect(2.5, 7, 19, 10, L(S, 3.5, 5))
    glaze = ("M6.5 9.8H17.5A1.2 1.2 0 0 1 17.5 12.2H16.5V13.1A1.2 1.2 0 0 1 14.1 13.1V12.2H10V13.7"
             "A1.2 1.2 0 0 1 7.6 13.7V12.2H6.5A1.2 1.2 0 0 1 6.5 9.8Z")
    return [shell(body), mark(glaze)]


@icon("cream-puff", CAT, "A round choux cream puff split open with cream piped in the middle",
      tags=["profiterole", "choux bun", "choux pastry", "patisserie", "dessert"], aliases=["profiterole"])
def _(S):
    cap = "M5 10C5 6 8.2 3.5 12 3.5C15.8 3.5 19 6 19 10Z" if S.name == "line" else \
        "M6 10C5.4 10 5 9.6 5 9C5.4 5.6 8.4 3.5 12 3.5C15.6 3.5 18.6 5.6 19 9C19 9.6 18.6 10 18 10Z"
    base = "M3 14.5H21C21 18.5 17 21 12 21C7 21 3 18.5 3 14.5Z"
    cream = bumps([(3.5, 12.3), (7.75, 12.3), (12, 12.3), (16.25, 12.3), (20.5, 12.3)], r=2.3)
    return [shell(cap), line(cream), shell(base), dot(10, 6.6, 0.9), dot(14, 6.6, 0.9)]


@icon("croquembouche", CAT, "A tall cone of stacked cream puffs on a plate",
      tags=["choux tower", "wedding cake", "profiterole tower", "french dessert", "celebration"])
def _(S):
    balls = [(6.5, 16), (12, 16), (17.5, 16), (9.25, 10.8), (14.75, 10.8), (12, 5.6)]
    r = 2.6
    parts = []
    fronts = []
    for x, y in reversed(balls):
        c = circle(x, y, r) if S.name == "rounded" else poly(regular(x, y, r + 0.15, 8, -90 + 22.5), closed=True)
        parts.append(shell(behind(c, fronts, -0.6) if fronts else c))
        fronts.append(c)
    return parts + [line(seg(3, 21, 21, 21))]


@icon("macaron", CAT, "A macaron in side view: two domed shells with ruffled feet and a filling between",
      tags=["macaroon", "french cookie", "patisserie", "almond cookie", "dessert"])
def _(S):
    top = "M3.5 9.8C3.5 6.5 7.3 4.5 12 4.5C16.7 4.5 20.5 6.5 20.5 9.8Z"
    bottom = "M3.5 14.2H20.5C20.5 17.5 16.7 19.5 12 19.5C7.3 19.5 3.5 17.5 3.5 14.2Z"
    fill = rect(5, 11.2, 14, 1.6, 0.8 if S.name == "rounded" else 0)
    return [shell(top), shell(bottom), solid(fill)]


@icon("mille-feuille", CAT, "A slice of mille-feuille with layers of pastry and cream under an iced top",
      tags=["napoleon", "vanilla slice", "custard slice", "french pastry", "patisserie"], aliases=["napoleon"])
def _(S):
    R = L(S, 1, 2.5)
    return [shell(rect(3, 4.5, 18, 15, R)), detail(seg(3, 8.5, 21, 8.5)),
            detail("M3 12Q4.5 11 6 12T9 12T12 12T15 12T18 12T21 12"), detail(seg(3, 15.5, 21, 15.5)),
            detail("M7 4.8L9 8.2"), detail("M12 4.8L14 8.2")]


@icon("strudel", CAT, "A rolled strudel log with slits on top and a cut end showing its spiral",
      tags=["apple strudel", "apfelstrudel", "austrian pastry", "rolled pastry", "dessert"])
def _(S):
    face = circle(7.5, 12.5, 5.5)
    R = L(S, 2.5, 5)
    log = f"M7.5 7H{fmt(21.5 - R)}A{R} {R} 0 0 1 21.5 {fmt(7 + R)}V{fmt(18 - R)}A{R} {R} 0 0 1 {fmt(21.5 - R)} 18H7.5Z"
    slits = [seg(13.5, 13.5, 15.5, 10), seg(17.2, 13.5, 19.2, 10)]
    return [shell(face), shell(behind(log, [face], 0.8)), detail(spiral(7.5, 12.5, 0.9, 1.8, 3)), *(detail(s) for s in slits)]


@icon("churros", CAT, "A ridged churro dipped into a small cup of chocolate",
      tags=["churro", "fried dough", "spanish dessert", "mexican dessert", "chocolate"], aliases=["churro"])
def _(S):
    R = L(S, 1, 3)
    cup = f"M11 14H21V{fmt(21 - R)}A{R} {R} 0 0 1 {fmt(21 - R)} 21H{fmt(11 + R)}A{R} {R} 0 0 1 11 {fmt(21 - R)}Z"
    stick = capsule(4.6, 4.6, 17, 17, 6.4, L(S, 1.2, 3.2))
    stick = minus(stick, rect(10.9, 13.9, 10.2, 8))
    return [shell(cup), shell(behind(stick, [cup], 0.8)), detail(seg(6.4, 6.4, 10, 10)), detail(seg(11, 17, 21, 17))]


@icon("beignet", CAT, "A puffy square beignet heavily dusted with powdered sugar",
      tags=["fried dough", "new orleans", "doughnut", "powdered sugar", "cafe"])
def _(S):
    r = L(S, 0, 2.2)
    pts = [(4, 6.5), (18.5, 4), (20.5, 17), (6, 20)]
    d = "M" + _p(((pts[3][0] + pts[0][0]) / 2, (pts[3][1] + pts[0][1]) / 2))
    for i in range(4):
        a, p, b = pts[i - 1], pts[i], pts[(i + 1) % 4]
        d += tip(a, p, b, r) if r else "L" + _p(p)
    d = ("M4 6.5Q11 4 18.5 4Q21.5 10.5 20.5 17Q13 18.5 6 20Q2.5 13 4 6.5Z" if S.name == "line" else
         "M5.5 5.8Q11.2 4 17 4.1Q18.8 4.2 19.1 5.9Q21.2 11 20.2 15.8Q19.9 17.2 18.5 17.4Q12.8 18.6 7.4 19.8Q5.9 20.1 5.4 18.7Q2.9 12.8 4.1 7.3Q4.4 6.1 5.5 5.8Z")
    sugar = [(8, 9), (12.5, 8), (16.5, 9.2), (10, 12.5), (14.5, 13), (9, 16.2), (15.5, 16)]
    return [shell(d), *(dot(x, y, 0.95) for x, y in sugar)]


@icon("cannoli", CAT, "A crisp cannoli tube lying on its side with cream bulging from both open ends",
      tags=["cannolo", "sicilian pastry", "italian dessert", "ricotta", "pastry"])
def _(S):
    k = dict(deg=-30, cx=12, cy=12)
    R = L(S, 0, 2)
    tube = rect(6.5, 8.5, 11, 7, R)
    n = L(S, 5, 6)
    cl = xf(scallop_ring(5.4, 12, 3.2, n, 1.15, 180), **k)
    cr = xf(scallop_ring(18.6, 12, 3.2, n, 1.15, 0), **k)
    return [shell(cl), shell(cr), shell(behind(xf(tube, **k), [cl, cr], 0.7)), dot(*rot_pts([(12, 12)], -30)[0], 1)]


@icon("turnover", CAT, "A triangular turnover with crimped edges and a steam slit on top",
      tags=["apple turnover", "fruit pastry", "hand pie", "puff pastry", "bakery"])
def _(S):
    n = 5
    bottom = [(20 - 15.5 * i / n, 19.5) for i in range(n + 1)]
    left = [(4.5, 19.5 - 15.5 * i / n) for i in range(n + 1)]
    r = L(S, 1.9, 1.6)
    d = "M4.5 4L20 19.5" + bumps(bottom, r=r)[len("M20 19.5"):] + bumps(left, r=r)[len("M4.5 19.5"):] + "Z"
    if S.name == "rounded":
        d = xf(d)
    return [shell(d), detail(seg(8.3, 13.3, 11.2, 16.2))]


def _twist_outline(S):
    top = bumps([(2.5, 10), (6.3, 10), (10.1, 10), (13.9, 10), (17.7, 10), (21.5, 10)], r=2.2)
    bot = bumps([(21.5, 14), (17.7, 14), (13.9, 14), (10.1, 14), (6.3, 14), (2.5, 14)], r=2.2)
    if S.name == "line":
        return top + "L" + bot[1:] + "Z"
    return top + "A2 2 0 0 1 " + bot[1:] + "A2 2 0 0 1 2.5 10Z"


@icon("pastry-twist", CAT, "A long flaky pastry strip twisted into a tight spiral",
      tags=["cheese straw", "twist", "puff pastry", "pastry stick", "bakery"])
def _(S):
    k = dict(deg=-40, cx=12, cy=12)
    xs = (6.3, 10.1, 13.9, 17.7)
    twists = [seg(x, 10, x - 1, 14) if S.name == "line" else f"M{fmt(x)} 10Q{fmt(x - 1.2)} 12 {fmt(x)} 14" for x in xs]
    return [shell(xf(_twist_outline(S), **k)), *(detail(xf(t, **k)) for t in twists)]


@icon("cream-horn", CAT, "A cone of spiralled pastry lying on its side with whipped cream at the open end",
      tags=["cream roll", "lady lock", "puff pastry", "cream cone", "dessert"])
def _(S):
    k = dict(deg=-15, cx=12, cy=12)
    cone = poly([(2.5, 12), (14, 5.5), (14, 18.5)], closed=True, r=S.r)
    cream = bumps([(14, 5.2), (18.8, 6.8), (21.2, 12), (18.8, 17.2), (14, 18.8)], r=2.9) + "Z"
    bands = [seg(6.2, 9.2, 7.8, 15.8), seg(10, 7.2, 11.6, 17.4)]
    cr = xf(cream, **k)
    return [shell(cr), shell(behind(xf(cone, **k), [cr], 0.8)), *(detail(xf(b, **k)) for b in bands)]


@icon("sfogliatella", CAT, "A shell-shaped sfogliatella made of thin layers fanning out from a pointed end",
      tags=["lobster tail", "italian pastry", "neapolitan pastry", "ricotta", "layered pastry"])
def _(S):
    r = L(S, 0, 1.5)
    body = ("M4 20.5" if S.name == "line" else "M4.8 20.2") + "C3 15 3.5 8.5 7 5.2C10.5 2 16.5 2.5 19.5 6C22.2 9.2 21.5 14 18 16.8C14.5 19.5 9 20.5 4.8 20.2Z"
    if S.name == "line":
        body = "M4 20.5C3 15 3.5 8.5 7 5.2C10.5 2 16.5 2.5 19.5 6C22.2 9.2 21.5 14 18 16.8C14.5 19.5 9 20.5 4 20.5Z"
    layers = ["M5.5 18.5C6.5 12 10.5 8 15 7.2", "M6.5 19C9 14.5 13 11.8 17.5 11.2"]
    return [shell(body), *(detail(l) for l in layers)]


# =========================================================================== buns, tarts and pies

@icon("hot-cross-bun", CAT, "A round glossy bun with a piped cross of icing over its top",
      tags=["easter bun", "spiced bun", "good friday", "sweet bun", "bakery"])
def _(S):
    r = L(S, 0, 1.5)
    body = ("M3.5 18C2.5 16.5 2.5 15 2.5 14C2.5 9.2 6.8 6 12 6C17.2 6 21.5 9.2 21.5 14C21.5 15 21.5 16.5 20.5 18"
            + tip((20.5, 18), (19.5, 19.5), (4.5, 19.5), r) + tip((19.5, 19.5), (4.5, 19.5), (3.5, 18), r) + "Z")
    return [shell(body), detail("M12 6.5V19.5"), detail("M2.8 11.8Q12 15.8 21.2 11.8")]


@icon("scone", CAT, "A tall scone split in half with cream and a drip of jam between the halves",
      tags=["cream tea", "afternoon tea", "clotted cream", "jam", "bakery"])
def _(S):
    R = L(S, 1, 2.5)
    top = (f"M4 10V7C4 4.9 7.6 3.5 12 3.5C16.4 3.5 20 4.9 20 7V10Z" if S.name == "line" else
           "M5.2 10A1.2 1.2 0 0 1 4 8.8V7C4 4.9 7.6 3.5 12 3.5C16.4 3.5 20 4.9 20 7V8.8A1.2 1.2 0 0 1 18.8 10Z")
    bottom = f"M4 15H20V{fmt(21 - R)}A{R} {R} 0 0 1 {fmt(20 - R)} 21H{fmt(4 + R)}A{R} {R} 0 0 1 4 {fmt(21 - R)}Z"
    cream = bumps([(2.8, 12.6), (7.2, 12.6), (11.6, 12.6), (16, 12.6), (20.4, 12.6)], r=2.4)
    return [shell(top), shell(bottom), line(cream), mark("M13.8 15H16.2V17.2A1.2 1.2 0 0 1 13.8 17.2Z")]


def _flute_ring(S, cx, cy, R, n):
    if S.name == "line":
        return scallop_ring(cx, cy, R - 0.4, n, 1.25)
    return scallop_ring(cx, cy, R - 0.3, n - 2, 1.05)


@icon("egg-tart", CAT, "A round egg tart seen from above: a fluted pastry cup with glossy custard and caramel spots",
      tags=["custard tart", "pastel de nata", "portuguese tart", "dan tat", "dim sum"], aliases=["custard-tart"])
def _(S):
    return [shell(_flute_ring(S, 12, 12, 9, 14)), detail(circle(12, 12, 5.2)), dot(10.3, 10.6, 1.2), dot(13.8, 13.4, 0.9)]


@icon("fruit-tart", CAT, "A fluted tart case topped with a row of round fruit",
      tags=["fruit flan", "berry tart", "tartlet", "patisserie", "dessert"])
def _(S):
    base = poly([(2.5, 13), (21.5, 13), (19, 20.5), (5, 20.5)], closed=True, r=S.r)
    fruit = [circle(6.8, 10, 2.7), circle(12, 8.4, 3.1), circle(17.2, 10, 2.7)]
    mid = fruit[1]
    parts = [shell(mid), shell(behind(fruit[0], [mid], 0.6)), shell(behind(fruit[2], [mid], 0.6))]
    base = behind(base, fruit, 0.6)
    return parts + [shell(base), detail(seg(8.5, 15.5, 8.9, 20.5)), detail(seg(12, 15.5, 12, 20.5)), detail(seg(15.5, 15.5, 15.1, 20.5))]


def _wedge_out(a0, a1, R, cx=12, cy=12):
    p0, p1 = pt_on(cx, cy, R, a0), pt_on(cx, cy, R, a1)
    return f"M{fmt(cx)} {fmt(cy)}L{_p(p0)}A{fmt(R)} {fmt(R)} 0 0 1 {_p(p1)}Z"


@icon("quiche", CAT, "A round quiche in a fluted crust seen from above with one wedge cut out",
      tags=["quiche lorraine", "savory tart", "egg pie", "brunch", "bakery"])
def _(S):
    ring = minus(_flute_ring(S, 12, 12, 9, 14), _wedge_out(-80, -20, 14))
    inner = earc(12, 12, 5.2, 5.2, -12, 272)
    return [shell(ring), detail(inner)]


@icon("pie-slice", CAT, "A wedge of pie with a crimped crust edge and a lattice top",
      tags=["slice of pie", "apple pie", "cherry pie", "dessert", "bakery"], aliases=["slice-of-pie"])
def _(S):
    top = "M3 13L14.5 5.5" + bumps([(14.5, 5.5), (18.3, 6.4), (21, 10.5)], r=2.5)[len("M14.5 5.5"):]
    body = "M3 13L14.5 5.5" + bumps([(14.5, 5.5), (18.3, 6.4), (21, 10.5)], r=2.5)[len("M14.5 5.5"):] + "V15.5L3 18Z"
    if S.name == "rounded":
        body = ("M3.8 12.5L14.5 5.5" + bumps([(14.5, 5.5), (18.3, 6.4), (21, 10.5)], r=2.5)[len("M14.5 5.5"):]
                + "V14.3Q21 15.3 20 15.5L4.2 17.8Q3 18 3 16.8V13.8Q3 13 3.8 12.5Z")
    return [shell(body), detail(seg(3.6, 13.3, 21, 10.8)), detail(seg(9, 9.5, 12.8, 12.1)), detail(seg(14, 7.8, 17.2, 11.1)),
            detail(seg(12.8, 7.6, 18.6, 8.4))]


@icon("meringue-pie", CAT, "A wedge of pie topped with a tall layer of swirled meringue peaks",
      tags=["lemon meringue", "meringue", "lemon pie", "dessert", "bakery"], aliases=["lemon-meringue-pie"])
def _(S):
    top = "M3 14C4.5 11 6 10.5 7.2 7.2C8.2 9 9.8 8.6 11.5 4.2C12.6 7.4 14.8 6.5 16.8 5.5C17 8 19.5 8.5 21 11.5"
    if S.name == "rounded":
        top = "M3 14C4.5 11 5.8 10.2 6.8 7.8Q7.2 7 7.6 7.8C8.4 9.2 9.7 8.2 11.1 5Q11.5 4.2 11.9 5C13 7.4 14.6 6.8 16.2 5.9Q17 5.5 17 6.3C17.2 8.3 19.5 8.8 21 11.5"
    body = top + "V16L3 18.5Z" if S.name == "line" else top + "V15.2Q21 16 20.2 16.1L4 18.4Q3 18.5 3 17.5Z"
    return [shell(body), detail(seg(3.4, 14.2, 20.6, 11.9)), detail("M7.5 11.6Q9.5 10.2 10 8.2")]


@icon("mince-pie", CAT, "A small round mince pie seen from above with a star cut into its sugared lid",
      tags=["christmas pie", "mincemeat", "festive", "holiday baking", "bakery"])
def _(S):
    pts = []
    for i in range(10):
        pts.append(pt_on(12, 12.3, 5.2 if i % 2 == 0 else 2.4, -90 + i * 36))
    star = poly(pts, closed=True, r=L(S, 0, 0.6))
    return [shell(_flute_ring(S, 12, 12, 9, 16)), detail(star)]


@icon("cornish-pasty", CAT, "A D-shaped pasty standing on its flat side with a crimped ridge along its top",
      tags=["pasty", "hand pie", "empanada", "savory pastry", "bakery"], aliases=["pasty"])
def _(S):
    R = L(S, 1, 2.5)
    pts = [pt_on(12, 20, 9.4, 180 + i * 180 / 8) for i in range(9)]
    crest = bumps(pts, r=2.0)
    body = (f"M2.6 {fmt(20 - R)}" + "L" + crest[1:] + f"L21.4 {fmt(20 - R)}A{R} {R} 0 0 1 {fmt(21.4 - R)} 20H{fmt(2.6 + R)}"
            f"A{R} {R} 0 0 1 2.6 {fmt(20 - R)}Z")
    inner = earc(12, 20, 6, 6, 190, 350)
    return [shell(body), detail(inner)]


@icon("madeleine", CAT, "A small shell-shaped madeleine cake with ridges fanning out from its narrow end",
      tags=["french cake", "sponge cake", "tea cake", "shell cake", "patisserie"])
def _(S):
    r = L(S, 0, 1.4)
    body = ("M12 20.5" + tip((12, 20.5), (12, 20.5), (6, 18), 0)[len("L12 20.5"):]
            + "C6 18 3 14 3 10C3 5.6 7 3.2 12 3.2C17 3.2 21 5.6 21 10C21 14 18 18 12 20.5Z")
    if S.name == "rounded":
        body = "M12 20.3C11.2 20 6 18 3 10C3 5.6 7 3.2 12 3.2C17 3.2 21 5.6 21 10C18 18 12.8 20 12 20.3Z"
    ridges = [f"M{_p(pt_on(12, 20, 6.5, a))}L{_p(pt_on(12, 20, 13.8 if abs(a + 90) < 30 else 12.3, a))}" for a in (-132, -107, -73, -48)]
    return [shell(body), *(detail(x) for x in ridges)]


@icon("canele", CAT, "A small canele cake with deep vertical flutes and a caramelized crown",
      tags=["cannele", "bordeaux cake", "french pastry", "custard cake", "patisserie"], aliases=["cannele"])
def _(S):
    R = L(S, 1, 2.5)
    crown = bumps([(6, 7.5), (9, 7.5), (12, 7.5), (15, 7.5), (18, 7.5)], r=1.7)
    body = (crown + f"L19.5 {fmt(21 - R)}A{R} {R} 0 0 1 {fmt(19.5 - R)} 21H{fmt(4.5 + R)}A{R} {R} 0 0 1 4.5 {fmt(21 - R)}Z")
    return [shell(body), detail(seg(5.3, 11, 18.7, 11)), detail(seg(9.5, 11, 9.1, 21)), detail(seg(14.5, 11, 14.9, 21))]


@icon("paris-brest", CAT, "A ring of choux pastry split in half with a thick band of piped cream",
      tags=["choux ring", "praline cream", "french pastry", "patisserie", "dessert"])
def _(S):
    top = "M3 10.5A9 5 0 0 1 21 10.5Q12 13.5 3 10.5Z"
    if S.name == "rounded":
        top = "M3.6 11.2Q2.6 10.4 3.6 8.6C5.3 6.4 8.4 5.5 12 5.5C15.6 5.5 18.7 6.4 20.4 8.6Q21.4 10.4 20.4 11.2Q12 13.8 3.6 11.2Z"
    bottom = "M3 16Q12 19 21 16A9 4.5 0 0 1 3 16Z"
    cream = bumps([(2.6, 14), (7.1, 14), (11.6, 14), (16.1, 14), (20.6, 14)], r=2.6, sweep=0)
    return [shell(top), shell(bottom), line(cream), mark("M8.6 8.6Q12 6.8 15.4 8.6Q12 10.2 8.6 8.6Z")]


@icon("palmier", CAT, "A heart-shaped palmier made of two pastry scrolls curling in to meet in the middle",
      tags=["elephant ear", "pig's ear", "puff pastry", "french cookie", "patisserie"], aliases=["elephant-ear"])
def _(S):
    r = L(S, 0, 1.4)
    body = ("M12 20.5" + "C8 18 2.5 14.5 2.5 9.4C2.5 5.8 4.8 3.6 7.5 3.6C9.6 3.6 11.2 4.8 12 6.4"
            "C12.8 4.8 14.4 3.6 16.5 3.6C19.2 3.6 21.5 5.8 21.5 9.4C21.5 14.5 16 18 12 20.5Z")
    if S.name == "rounded":
        body = ("M12.9 19.9Q12 20.5 11.1 19.9C7.5 17.5 2.5 14 2.5 9.4C2.5 5.8 4.8 3.6 7.5 3.6C9.6 3.6 11.2 4.8 12 6.4"
                "C12.8 4.8 14.4 3.6 16.5 3.6C19.2 3.6 21.5 5.8 21.5 9.4C21.5 14 16.5 17.5 12.9 19.9Z")
    left = spiral(8, 9.6, 0.9, 1.8, 3, 1.0, start_right=True)
    return [shell(body), detail(left), detail(_mirror_x(left))]


def _mirror_x(d):
    """Mirror an M/A path about x = 12 (flips arc sweep)."""
    toks = re.findall(r"[MA]|-?\d*\.?\d+", d)
    out, i = "", 0
    while i < len(toks):
        t = toks[i]
        if t == "M":
            out += f"M{fmt(24 - float(toks[i + 1]))} {toks[i + 2]}"
            i += 3
        elif t == "A":
            rx, ry, rot, la, sw, x, y = toks[i + 1:i + 8]
            out += f"A{rx} {ry} {rot} {la} {1 - int(sw)} {fmt(24 - float(x))} {y}"
            i += 8
        else:
            i += 1
    return out


@icon("toaster-pastry", CAT, "A flat rectangular toaster pastry with an iced top and sprinkles",
      tags=["breakfast pastry", "frosted pastry", "toaster tart", "snack"], aliases=["toaster-tart"])
def _(S):
    sprinkles = [capsule(9, 10.4, 11, 8.6, 1.5), capsule(12.8, 9.2, 15.2, 9.9, 1.5), capsule(9.2, 14.6, 11.6, 15.4, 1.5),
                 capsule(13.4, 15.6, 15, 13.4, 1.5)]
    return [shell(rect(3.5, 2.5, 17, 19, S.R)), detail(rect(6.5, 5.5, 11, 13, L(S, 0.5, 2))), *(mark(s) for s in sprinkles)]


@icon("pie-bird", CAT, "A small ceramic bird with an open beak poking up through the crust of a pie",
      tags=["pie funnel", "pie vent", "baking tool", "pie crust", "kitchen"], aliases=["pie-funnel"])
def _(S):
    r = L(S, 0, 1.2)
    bird = ("M9.5 15V9.5C9.5 6.5 10.6 4 12.8 4C14 4 14.8 4.6 15.3 5.4"
            + tip((15.3, 5.4), (20, 4.4), (16.4, 7.4), r) + tip((20, 4.4), (16.4, 7.4), (20, 9.8), 0)
            + tip((16.4, 7.4), (20, 9.8), (15.5, 9.8), r) + "L15.5 9.8V15Z")
    pie = "M2.5 15.5Q12 11.5 21.5 15.5L19.5 20.5H4.5Z" if S.name == "line" else \
        "M3.4 14.9Q12 11.5 20.6 14.9Q21.8 15.4 21.3 16.6L20 19.6Q19.6 20.5 18.6 20.5H5.4Q4.4 20.5 4 19.6L2.7 16.6Q2.2 15.4 3.4 14.9Z"
    return [shell(bird), shell(behind(pie, [bird], 0.8)), dot(12.6, 7, 1), detail(seg(3.5, 17.2, 20.5, 17.2))]


@icon("stroopwafel", CAT, "A thin round stroopwafel with a waffle grid on top and a layer of caramel inside",
      tags=["syrup waffle", "caramel waffle", "dutch cookie", "waffle cookie", "coffee"], aliases=["syrup-waffle"])
def _(S):
    if S.name == "line":
        o = "M3 9L5.6 5.5L12 4L18.4 5.5L21 9V15L18.4 18.5L12 20L5.6 18.5L3 15Z"
        edge = "M3 9L5.6 12.5L12 14L18.4 12.5L21 9"
        mid = "M3 12L5.6 15.5L12 17L18.4 15.5L21 12"
    else:
        o = "M3 9A9 5 0 0 1 21 9V15A9 5 0 0 1 3 15Z"
        edge = "M3 9A9 5 0 0 0 21 9"
        mid = "M3 12A9 5 0 0 0 21 12"
    grid = [ell_chord(12, 9, 9, 5, c, k, 0.3) for c, k in ((18, "/"), (24, "/"), (-3, "\\"), (3, "\\"))]
    return [shell(o), detail(edge), detail(mid), *(detail(g) for g in grid)]

