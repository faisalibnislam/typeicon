"""TypeIcon Core: world dishes (batch dishes_004).

Sausages, pies, pancakes, Latin American, Asian, Jewish, European and Indian dishes, soups, sandwiches and
appetizers, drawn from the food itself. Side views sit on a shallow plate or in a round bowl; top views sit
on a round plate (r 9).
"""
import math
import re

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, rotation, transform_path  # noqa: F401

CAT = "dishes"


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


def pt_on(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def rot_pts(points, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in points]


def bar(x1, y1, x2, y2, w, rc=0.0):
    """Rectangle of width w along the axis (x1, y1)-(x2, y2), corners filleted by rc (as poly)."""
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln * w / 2, (x2 - x1) / ln * w / 2
    return poly([(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)], closed=True, r=rc)


def capsule(x1, y1, x2, y2, w):
    """Stadium (round-ended bar) of width w along (x1, y1)-(x2, y2)."""
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln * w / 2, (x2 - x1) / ln * w / 2
    r = fmt(w / 2)
    return (f"M{fmt(x1 + nx)} {fmt(y1 + ny)}L{fmt(x2 + nx)} {fmt(y2 + ny)}A{r} {r} 0 0 0 {fmt(x2 - nx)} {fmt(y2 - ny)}"
            f"L{fmt(x1 - nx)} {fmt(y1 - ny)}A{r} {r} 0 0 0 {fmt(x1 + nx)} {fmt(y1 + ny)}Z")


def blob(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def oval_dot(cx, cy, rx, ry) -> Part:
    return Part("dot", ellipse(cx, cy, rx, ry))


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


def star_ring(cx, cy, r_out, r_in, n, start=-90.0):
    pts = []
    for i in range(2 * n):
        pts.append(pt_on(cx, cy, r_out if i % 2 == 0 else r_in, start + i * 180 / n))
    return pts


def bumps(pts, r=None):
    """Open path of upward arcs through pts (left to right)."""
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        ch = math.hypot(x1 - x0, y1 - y0)
        rr = max(r or ch * 0.62, ch / 2 + 0.01)
        d += f"A{fmt(rr)} {fmt(rr)} 0 0 1 {fmt(x1)} {fmt(y1)}"
    return d


def zigzag(x0, x1, y, amp, n):
    """Points of a zigzag from x0 to x1 around y, n teeth."""
    w = (x1 - x0) / n
    pts = [(x0, y)]
    for i in range(n):
        pts.append((x0 + w * (i + 0.5), y - amp))
        pts.append((x0 + w * (i + 1), y))
    return pts


def wave_pts(x0, x1, y, amp, period, step=0.75, phase=0.0):
    n = max(2, int(round((x1 - x0) / step)))
    return [(x0 + (x1 - x0) * i / n, y + amp * math.sin(2 * math.pi * ((x1 - x0) * i / n) / period + phase))
            for i in range(n + 1)]


def wave_d(x0, x1, y, amp, period):
    """Smooth sine wave from x0 to x1 made of quadratic half-waves."""
    half = period / 2
    n = max(1, int(round((x1 - x0) / half)))
    half = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        xa = x0 + half * i
        sgn = -1 if i % 2 == 0 else 1
        d += f"Q{fmt(xa + half / 2)} {fmt(y + sgn * amp * 2)} {fmt(xa + half)} {fmt(y)}"
    return d


def fork(S, tx, ty, ang, length):
    """A fork as open strokes: tine tips centred at (tx, ty), handle pointing at angle ang (degrees)."""
    rot = ang - 90

    def tp(pts):
        return [(tx + x * math.cos(math.radians(rot)) - y * math.sin(math.radians(rot)),
                 ty + x * math.sin(math.radians(rot)) + y * math.cos(math.radians(rot))) for x, y in pts]
    head = poly(tp([(-2.6, 0), (-2.6, 3.2), (2.6, 3.2), (2.6, 0)]), r=S.r * 0.6)
    return [line(head), line(poly(tp([(0, 0), (0, length)])))]


BOWL_TOP = 11.5


def bowl(S, top=BOWL_TOP):
    """A round-bottomed bowl with a flat rim at y=top (side view)."""
    if S.name == "line":
        return f"M3 {top}L21 {top}C21 {top + 5} 17 {top + 9} 12 {top + 9}C7 {top + 9} 3 {top + 5} 3 {top}Z"
    return (f"M4.5 {top}L19.5 {top}C20.3 {top} 21 {top + 0.7} 20.9 {top + 1.5}C20.3 {top + 5.8} 16.6 {top + 9} 12 {top + 9}"
            f"C7.4 {top + 9} 3.7 {top + 5.8} 3.1 {top + 1.5}C3 {top + 0.7} 3.7 {top} 4.5 {top}Z")


def plate(S, y=18.5, x0=2.5, x1=21.5, h=2.5):
    """A shallow plate seen from the side (rim at y)."""
    return shell(poly([(x0, y), (x1, y), (x1 - h, y + h), (x0 + h, y + h)], closed=True, r=L(S, 0, 1)))


def toast(S):
    """A slice of bread seen from above, crown at the top (body x 4.5 to 19.5)."""
    top = ("M4.5 {b}V11.5C3.2 10.9 2.5 9.7 2.5 8.2C2.5 5.1 5.5 3 9.5 3H14.5C18.5 3 21.5 5.1 21.5 8.2"
           "C21.5 9.7 20.8 10.9 19.5 11.5V{b}")
    if S.name == "line":
        return top.format(b=21) + "Z"
    return top.format(b=19) + "A2 2 0 0 1 17.5 21H6.5A2 2 0 0 1 4.5 19Z"


def thick(d, w, S=None):
    """Outline of a stroke of width w along the open path d (limbs, bones, sticks inside a silhouette)."""
    return path_to_d(ST(d, w, "round", "round"))


def spiral_pts(cx, cy, r0, r1, turns, start=-90.0, n=26):
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append(pt_on(cx, cy, r0 + (r1 - r0) * t, start + 360 * turns * t))
    return pts


def hcyl(S, x0, x1, y0, y1, rx=3.0):
    """Horizontal cylinder with a flat left end and an elliptical face on the right (face centre x1 - rx)."""
    cx = x1 - rx
    r = L(S, 0, 1.5)
    ry = (y1 - y0) / 2
    cy = (y0 + y1) / 2
    if r == 0:
        return f"M{fmt(x0)} {fmt(y0)}H{fmt(cx)}A{fmt(rx)} {fmt(ry)} 0 0 1 {fmt(cx)} {fmt(y1)}H{fmt(x0)}Z"
    return (f"M{fmt(x0 + r)} {fmt(y0)}H{fmt(cx)}A{fmt(rx)} {fmt(ry)} 0 0 1 {fmt(cx)} {fmt(y1)}H{fmt(x0 + r)}"
            f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0)} {fmt(y1 - r)}V{fmt(y0 + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x0 + r)} {fmt(y0)}Z")


def half_disc(S, cx, cy, r, deg=0.0, rc=1.0):
    """Half disc (flat side up) centred at (cx, cy) with radius r, tilted by deg; corners softened for Rounded."""
    if S.name == "line":
        d = f"M{fmt(cx - r)} {fmt(cy)}A{fmt(r)} {fmt(r)} 0 0 0 {fmt(cx + r)} {fmt(cy)}Z"
    else:
        a = math.asin(min(0.9, rc / r))
        ex, ey = cx + r * math.cos(a), cy + r * math.sin(a)
        d = (f"M{fmt(cx - r + rc)} {fmt(cy)}H{fmt(cx + r - rc)}Q{fmt(cx + r)} {fmt(cy)} {fmt(ex)} {fmt(ey)}"
             f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(2 * cx - ex)} {fmt(ey)}Q{fmt(cx - r)} {fmt(cy)} {fmt(cx - r + rc)} {fmt(cy)}Z")
    return xf(d, deg, cx, cy) if deg else d


def frill(x, y, ang, w=3.4, h=2.6):
    """Zigzag paper cap (open polyline) sitting at (x, y) and pointing away at angle ang (degrees)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    pts = [(x + nx * (-w / 2), y + ny * (-w / 2)), (x + ux * h + nx * (-w / 4), y + uy * h + ny * (-w / 4)),
           (x + nx * 0 + ux * (h * 0.5), y + uy * (h * 0.5)),
           (x + ux * h + nx * (w / 4), y + uy * h + ny * (w / 4)), (x + nx * (w / 2), y + ny * (w / 2))]
    return pts



def flipx(d, cx=12.0):
    """Mirror an outline left to right about x = cx."""
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 2 * cx, 0)))


def puffy_rect(x0, y0, x1, y1, nx, ny, h=1.0):
    """Rectangle whose edges are made of outward arcs (nx across, ny down), bulging by h (clockwise path)."""
    def arcs(ax, ay, bx, by, n):
        ln = math.hypot(bx - ax, by - ay) / n
        r = (ln * ln / 4 + h * h) / (2 * h)
        out = ""
        for i in range(1, n + 1):
            out += f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(ax + (bx - ax) * i / n)} {fmt(ay + (by - ay) * i / n)}"
        return out
    return (f"M{fmt(x0)} {fmt(y0)}" + arcs(x0, y0, x1, y0, nx) + arcs(x1, y0, x1, y1, ny)
            + arcs(x1, y1, x0, y1, nx) + arcs(x0, y1, x0, y0, ny) + "Z")


# =========================================================================== sausages, pies and breads


@icon("lahmacun", CAT, "A thin round flatbread with a minced topping and a lemon wedge beside it",
      tags=["turkish pizza", "flatbread", "minced meat", "lemon wedge", "middle eastern", "street food"])
def _(S):
    lemon = half_disc(S, 17.5, 17.5, 3.5, -35, 1.0)
    bread = circle(10.5, 10.5, 7.5)
    return [shell(lemon), shell(behind(bread, [lemon], 1.5)),
            dot(7.6, 8.4, 1.1), dot(12.2, 7.4, 1.1), dot(8.4, 13.2, 1.1), dot(12.6, 11.6, 1.1)]


@icon("sausage-links", CAT, "A string of three plump sausages pinched together at the links",
      tags=["sausage chain", "bratwurst", "link sausage", "butcher", "charcuterie", "meat"])
def _(S):
    chain = union(*[capsule(12 + t - 1.7, 12, 12 + t + 1.7, 12, 6.2) for t in (-8.6, 0, 8.6)])
    return [shell(xf(chain, -40))]


@icon("salami", CAT, "A cured salami log with a round slice in front showing speckled fat",
      tags=["cured meat", "deli", "charcuterie", "sausage", "cold cuts", "antipasto"])
def _(S):
    log = rect(3, 4.5, 13, 9, L(S, 2, 4))
    sl = circle(16.5, 15.5, 4.5)
    return [shell(sl), shell(behind(log, [sl], 1.5)), detail(seg(7.5, 4.5, 7.5, 13.5)),
            dot(15.2, 14.6, 1.0), dot(18.1, 15.6, 1.0), dot(16.2, 17.9, 1.0)]


@icon("haggis", CAT, "A round tied haggis on a plate beside a mound of mash",
      tags=["scottish", "burns night", "neeps and tatties", "offal", "sausage", "traditional"])
def _(S):
    mash = bumps([(14.5, 18.5), (15.6, 14.6), (19, 13.6), (21, 18.5)], r=2.8) + "Z"
    return [shell(circle(7.6, 13.4, 4.7)), line(poly([(5.4, 3.6), (7.6, 6.2), (9.8, 3.6)], r=S.r * 0.6)), shell(mash), plate(S),
            dot(6.4, 14.2, 0.95), dot(9.2, 12.6, 0.95)]


@icon("meat-pie", CAT, "A small round pie with a crimped edge and a squiggle of sauce on top",
      tags=["hand pie", "pastry", "savory pie", "steak pie", "pub food", "australian"])
def _(S):
    if S.name == "line":
        body = "M3 13C3 7.5 7.5 5.5 12 5.5C16.5 5.5 21 7.5 21 13L19.5 20H4.5Z"
    else:
        body = "M3 13C3 7.5 7.5 5.5 12 5.5C16.5 5.5 21 7.5 21 13L19.6 18.8Q19.4 20 18.2 20H5.8Q4.6 20 4.4 18.8Z"
    return [shell(body), detail(poly(zigzag(3.4, 20.6, 13, 1, 6), r=S.r * 0.5)), detail(wave_d(7.5, 16.5, 9, 0.8, 4.5))]


@icon("canned-sardines", CAT, "An open tin with a pull ring and two small fish lying head to tail",
      tags=["tinned fish", "sardine tin", "pantry", "preserved fish", "seafood", "can"])
def _(S):
    def fish(cy, face_left):
        d = union(ellipse(11.2, cy, 4.9, 1.85), poly([(14.6, cy), (18.3, cy - 2.1), (18.3, cy + 2.1)], closed=True))
        return Part("dot", d if not face_left else flipx(d))
    return [shell(rect(2.5, 8, 19, 13, L(S, 1, 2.5))), line(circle(17.5, 4.6, 2.1)), fish(12.4, False), fish(17, True)]


@icon("lobster-tail", CAT, "A cooked lobster tail with curved shell bands and a fanned tail",
      tags=["seafood", "surf and turf", "shellfish", "crustacean", "fine dining", "shell"])
def _(S):
    body = "M3.4 12C3.4 8.2 6 6.6 9 6.6L15 8.2V15.8L9 17.4C6 17.4 3.4 15.8 3.4 12Z"
    fan = poly([(14.6, 8.2), (19.6, 6), (20.2, 9.4), (17.8, 10.2), (21.2, 12), (17.8, 13.8), (20.2, 14.6), (19.6, 18), (14.6, 15.8)],
               closed=True, r=L(S, 0.6, 1.0))
    whole = union(body, fan)
    bands = ["M6.6 7.4Q8.4 12 6.6 16.6", "M10 7.2Q11.8 12 10 16.8", "M13.4 7.8Q14.8 12 13.4 16.2"]
    return [shell(rotd(whole, -24, 12, 12, 0, 0)), *[detail(rotd(b, -24)) if False else detail(xf(b, -24)) for b in bands]]


@icon("dutch-baby", CAT, "A skillet holding a puffed pancake with a tall ruffled crown and powdered sugar",
      tags=["german pancake", "puffed pancake", "skillet", "breakfast", "brunch", "sugar"])
def _(S):
    crown = poly([(4.5, 14), (4.5, 6), (7.3, 9.3), (10.3, 6), (13.2, 9.3), (16, 6), (16, 14)], closed=True, r=S.r * 0.6)
    pan = poly([(2.5, 14), (18, 14), (16.6, 20), (4, 20)], closed=True, r=L(S, 0, 1))
    return [shell(crown), shell(pan), line(seg(18, 16.4, 21.5, 16.4)), dot(7.6, 12, 0.9), dot(10.3, 10.6, 0.9), dot(13, 12, 0.9)]


@icon("muffuletta", CAT, "A round layered sandwich loaf with olive salad, cut into wedges",
      tags=["new orleans", "olive salad", "sandwich", "round loaf", "deli", "cold cuts"])
def _(S):
    top = "M3 9.5C3 5.5 7 3.5 12 3.5C17 3.5 21 5.5 21 9.5Z"
    return [shell(top), shell(rect(3, 15.5, 18, 5, L(S, 1.5, 2.5))), detail(seg(12, 3.5, 12, 9.5)),
            detail(seg(12, 15.5, 12, 20.5)), dot(6.5, 12.5, 1.1), dot(9.6, 12.6, 1.1), dot(14.4, 12.6, 1.1), dot(17.5, 12.5, 1.1)]


@icon("bamboo-rice", CAT, "A bamboo tube split open lengthwise with cooked rice piled inside and a leaf",
      tags=["sticky rice", "bamboo tube", "steamed rice", "southeast asian", "lam", "street food"])
def _(S):
    trough = rect(3, 12, 18, 7.5, L(S, 1.5, 3.5))
    heap = bumps([(5, 12), (7.5, 8.4), (11, 7), (14.5, 8.4), (16.5, 12)], r=2.8) + "Z"
    return [shell(trough), shell(heap), detail(seg(8, 12.5, 8, 18.5)), detail(seg(16, 12.5, 16, 18.5)),
            shell(leaf(19, 8, 21.4, 2.6, 1.6))]


@icon("pineapple-fried-rice", CAT, "A hollowed pineapple half with a leafy crown, filled with fried rice",
      tags=["thai", "pineapple bowl", "fried rice", "tropical", "fruit bowl", "stuffed pineapple"])
def _(S):
    b = bowl(S, 12)
    heap = bumps([(8.5, 12), (10.3, 8.6), (14, 7.4), (17.6, 8.8), (19.5, 12)], r=3.0) + "Z"
    crown = [shell(leaf(6, 11.6, 3.2, 3.4, 1.5)), shell(leaf(6, 11.6, 6.2, 2.6, 1.3))]
    return [shell(b), shell(heap), *crown, detail(poly([(12, 14.2), (14.6, 16.6), (12, 19), (9.4, 16.6)], closed=True, r=S.r * 0.5))]


@icon("stamped-flatbread", CAT, "An oval flatbread with a thick raised rim and a stamped dotted centre",
      tags=["dimpled bread", "docked bread", "flatbread", "pide", "ekmek", "baked bread"])
def _(S):
    def pp(x, y):
        a, b = rot_pts([(x, y)], -20)[0]
        if S.name == "line":
            return Part("dot", poly([(a, b - 1.3), (a + 1.3, b), (a, b + 1.3), (a - 1.3, b)], closed=True))
        return dot(a, b, 1.0)
    if S.name == "line":
        rim = poly([(12 + 5.6 * math.cos(math.radians(a)), 12 + 3.6 * math.sin(math.radians(a))) for a in range(0, 360, 30)],
                   closed=True)
        rim = rotd(rim, -20)
    else:
        rim = rotd(ellipse(12, 12, 5.6, 3.6), -20)
    return [shell(rotd(ellipse(12, 12, 9, 6.9), -20)), detail(rim), pp(9.6, 12), pp(12, 12), pp(14.4, 12)]


@icon("stuffed-mussels", CAT, "An open mussel with its lid lifted, showing a mound of spiced rice stuffing",
      tags=["midye dolma", "mussel", "seafood", "rice stuffing", "shellfish", "turkish"])
def _(S):
    lower = "M3.5 15.5C7 21.5 17 21.5 20.5 15.5Z"
    heap = bumps([(6, 15.5), (8, 13.2), (12, 12), (16, 13.2), (18, 15.5)], r=3.0) + "Z"
    return [shell(lower), shell(heap), shell(leaf(4, 11.2, 19.5, 4.2, 2.6))]


@icon("toad-in-the-hole", CAT, "A puffy batter pudding tray with two sausages lying in it",
      tags=["british", "sausage", "yorkshire pudding", "batter", "comfort food", "roast tin"])
def _(S):
    return [shell(puffy_rect(3.5, 4.5, 20.5, 19.5, 4, 3, 1.1)),
            Part("dot", capsule(7.6, 9.2, 16.4, 9.2, 3.6)), Part("dot", capsule(7.6, 14.8, 16.4, 14.8, 3.6))]


@icon("sausage-sizzle", CAT, "A grilled sausage laid on a slice of white bread with a squiggle of sauce",
      tags=["bunnings", "barbecue", "australian", "hot sausage", "onions", "fundraiser"])
def _(S):
    sau = capsule(5.8, 13, 18.2, 13, 5.6)
    return [shell(sau), shell(behind(toast(S), [sau], 1.5)), detail(wave_d(6.5, 17.5, 13, 0.55, 3.5))]


# =========================================================================== Latin American, Asian and Jewish dishes


def pip(S, x, y, r=1.0):
    """Small solid mark: a diamond in Line, a round dot in Rounded."""
    if S.name == "line":
        return Part("dot", poly([(x, y - r * 1.3), (x + r * 1.3, y), (x, y + r * 1.3), (x - r * 1.3, y)], closed=True))
    return dot(x, y, r)


@icon("fairy-bread", CAT, "Two triangles of buttered bread covered in tiny sprinkles",
      tags=["sprinkles", "hundreds and thousands", "party food", "kids party", "australian", "bread and butter"])
def _(S):
    a = poly([(3, 20), (9.5, 7), (16, 20)], closed=True, r=S.r)
    b = poly([(8.5, 17), (15, 4), (21.5, 17)], closed=True, r=S.r)
    return [shell(a), shell(behind(b, [a], 1.5)), pip(S, 9.5, 12.8), pip(S, 7.6, 16.8), pip(S, 11.6, 17), pip(S, 16.6, 12)]


@icon("pupusa", CAT, "A thick round griddled corn cake with a crack oozing cheese, and slaw beside it",
      tags=["salvadoran", "stuffed corn cake", "cheese", "curtido", "masa", "griddle"])
def _(S):
    cake = circle(10.5, 10.5, 7.5)
    slaw = bumps([(13.5, 21), (14.5, 18), (17.5, 16.6), (20.5, 18.6), (21, 21)], r=2.6) + "Z"
    return [shell(slaw), shell(behind(cake, [slaw], 1.5)), detail(poly([(3, 10.5), (5.4, 12.4), (7.4, 9.8)])),
            pip(S, 11.5, 8, 1.0), pip(S, 13.2, 12.2, 1.0)]


@icon("chilaquiles", CAT, "A bowl of tortilla chips in sauce topped with a fried egg",
      tags=["mexican breakfast", "tortilla chips", "salsa", "fried egg", "brunch", "verde"])
def _(S):
    chip = poly([(4, 11), (7, 4.2), (10.2, 11)], closed=True, r=S.r)
    return [shell(bowl(S, 12.5)), shell(chip), shell(circle(15, 7.2, 3.4)), dot(15, 7.2, 1.1)]


@icon("huevos-rancheros", CAT, "A plate with a tortilla, two fried eggs and a ring of chunky salsa",
      tags=["ranch eggs", "mexican breakfast", "fried eggs", "tortilla", "salsa", "brunch"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(circle(9.4, 10, 2.4)), dot(9.4, 10, 1.0), detail(circle(14.8, 14.2, 2.4)),
            dot(14.8, 14.2, 1.0), pip(S, 15.4, 7.4), pip(S, 8.4, 16.4), pip(S, 5.8, 12.6, 0.8), pip(S, 18.2, 10.6, 0.8)]


@icon("taquitos", CAT, "Three thin tightly rolled crispy tortillas side by side with a drizzle of sauce",
      tags=["flautas", "rolled tacos", "fried tortilla", "mexican", "appetizer", "crispy"])
def _(S):
    return [shell(capsule(6, y, 18, y, 4.2)) for y in (6.5, 12, 17.5)] + [line(wave_d(3, 21, 12, 0.0, 6)) if False else
            line(poly([(9, 3.5), (11, 7.5), (13, 11), (11, 14), (13, 17), (15, 20.5)]))]


@icon("sopes", CAT, "A small thick corn base with a pinched rim holding beans and toppings",
      tags=["masa", "mexican", "beans", "antojitos", "corn cake", "street food"])
def _(S):
    base = poly([(3, 14), (21, 14), (19.5, 20.5), (4.5, 20.5)], closed=True, r=L(S, 0, 1))
    heap = bumps([(6, 14), (8, 10), (12, 8.6), (16, 10), (18, 14)], r=3.2) + "Z"
    return [shell(base), shell(heap), detail(poly(zigzag(4.2, 19.8, 14, 0, 1)) if False else seg(4, 17.2, 20, 17.2)),
            dot(10, 11.4, 1.0), dot(14, 11.4, 1.0)]


@icon("causa", CAT, "A tower of layered mashed potato with filling between the layers and a garnish on top",
      tags=["peruvian", "potato terrine", "layered potato", "cold dish", "aji amarillo", "appetizer"])
def _(S):
    return [shell(rect(5.5, 9, 13, 11.5, L(S, 1.5, 3))), detail(seg(5.5, 13, 18.5, 13)), detail(wave_d(5.5, 18.5, 16.8, 0.6, 3.25)),
            shell(circle(12, 5.2, 1.8)) if False else dot(12, 5.6, 1.7)]


@icon("hotteok", CAT, "A pair of filled round pancakes, one cut open with seeds and syrup inside",
      tags=["korean pancake", "sweet pancake", "brown sugar", "street food", "winter snack", "syrup"])
def _(S):
    back = circle(14, 14, 6.6)
    front = circle(9.5, 9.5, 6.4)
    return [shell(front), shell(behind(back, [front], 1.5)), pip(S, 7.2, 8, 0.95), pip(S, 11, 7.6, 0.95), pip(S, 9.4, 11.6, 0.95)]


@icon("cold-noodles", CAT, "A metal bowl of chilled noodles with ice cubes floating on top",
      tags=["naengmyeon", "chilled noodles", "summer", "ice", "korean", "soba"])
def _(S):
    cube1 = xf(rect(6.2, 4.6, 4.6, 4.6, L(S, 0.5, 1.2)), 14, 8.5, 6.9)
    cube2 = xf(rect(13, 4, 4.6, 4.6, L(S, 0.5, 1.2)), -12, 15.3, 6.3)
    return [shell(bowl(S, 12.5)), shell(cube1), shell(cube2), detail(wave_d(6.5, 17.5, 16.5, 0.8, 4))]


@icon("eel-rice-box", CAT, "A lacquer box of rice topped with a glazed eel fillet with grill stripes",
      tags=["unadon", "unagi", "unaju", "japanese", "grilled eel", "bento"])
def _(S):
    return [shell(rect(2.5, 5, 19, 14, L(S, 1.5, 3.5))), shell(capsule(8.5, 12, 15.5, 12, 5.2)),
            detail(seg(10.4, 10.6, 11.6, 13.4)), detail(seg(13.2, 10.6, 14.4, 13.4))]


@icon("latkes", CAT, "A stack of three potato pancakes with a dollop of applesauce on top",
      tags=["potato pancakes", "hanukkah", "fried", "applesauce", "jewish", "rosti"])
def _(S):
    rows = [rect(3, y, 18, 4.3, L(S, 1.5, 2.1)) for y in (16.2, 11.9, 7.6)]
    dollop = "M8.5 7.6C8.5 3.6 15.5 3.6 15.5 7.6Z"
    return [*[shell(r_) for r_ in rows], shell(dollop)]


@icon("seder-plate", CAT, "A round plate with six evenly spaced hollows around the rim",
      tags=["passover", "pesach", "jewish holiday", "ritual plate", "charoset", "tableware"])
def _(S):
    ring = [pip(S, *pt_on(12, 12, 5.8, -90 + 60 * i), 1.6) for i in range(6)]
    return [shell(circle(12, 12, 9)), detail(circle(12, 12, 1.6)) if False else pip(S, 12, 12, 1.0), *ring]


@icon("matzo", CAT, "A square flat cracker with rows of perforated dots and toasted stripes",
      tags=["matzah", "passover", "unleavened bread", "jewish", "cracker", "flatbread"], aliases=["matzah"])
def _(S):
    pts = [pip(S, x, y, 0.9) for x in (7.2, 12, 16.8) for y in (7.2, 12, 16.8)]
    return [shell(rect(3, 3, 18, 18, L(S, 1.5, 4))), *pts]


@icon("osechi", CAT, "Two stacked lacquer boxes, the top one divided into compartments of food",
      tags=["jubako", "japanese new year", "bento", "tiered box", "celebration", "lacquerware"])
def _(S):
    return [shell(rect(3, 3.5, 18, 8, L(S, 1.5, 2.5))), detail(seg(9, 4, 9, 11)), detail(seg(15, 4, 15, 11)),
            shell(rect(3, 14.5, 18, 6, L(S, 1.5, 2.5)))]


@icon("amuse-bouche", CAT, "A porcelain spoon holding a single tiny bite",
      tags=["amuse-gueule", "tasting spoon", "fine dining", "appetizer", "canape", "chef"], aliases=["amuse-gueule"])
def _(S):
    bowl_ = ellipse(8.5, 15.2, 5.6, 3.4)
    bite = circle(8.5, 10, 2.6)
    return [shell(bowl_), shell(behind(bite, [bowl_], None)), line(seg(14.2, 15.2, 21, 15.2))]


@icon("carpaccio", CAT, "A round plate of thin overlapping slices fanned in a circle around a pile of leaves",
      tags=["raw beef", "thin sliced", "italian", "arugula", "appetizer", "parmesan"])
def _(S):
    ring = union(*[circle(*pt_on(12, 12, 4.9, -90 + 360 / 7 * i), 2.3) for i in range(7)])
    return [shell(circle(12, 12, 9.2)), detail(ring), pip(S, 12, 12, 1.3)]


@icon("cannelloni", CAT, "Two filled pasta tubes in a small baking dish with a stripe of sauce across them",
      tags=["stuffed pasta", "italian", "baked pasta", "ricotta", "tomato sauce", "tubes"])
def _(S):
    dish = rect(3, 13.5, 18, 7, L(S, 1.5, 3))
    a = capsule(6.5, 9.4, 11, 9.4, 4.4)
    b = behind(capsule(13, 9.4, 17.5, 9.4, 4.4), [a], 1.25)
    return [shell(dish), shell(a), shell(b), line(poly([(6, 7.2), (9, 11.6), (12, 7.2), (15, 11.6), (18, 7.2)], r=S.r * 0.6))]


# =========================================================================== soups, cutlets and plates


@icon("crab-cake", CAT, "A thick round golden crab patty with a crumb crust and speckled top",
      tags=["maryland", "seafood patty", "fried", "crab", "appetizer", "crumb crust"])
def _(S):
    ry = L(S, 4.0, 4.7)
    body = union(ellipse(12, 9.8, 8.6, ry), ellipse(12, 15.8, 8.6, ry), rect(3.4, 9.8, 17.2, 6))
    return [shell(body), detail(ellipse(12, 10, 5.2, 1.9)) if False else detail("M3.4 10.6A8.6 4.2 0 0 0 20.6 10.6"),
            pip(S, 9, 8.6, 0.9), pip(S, 13.4, 9.4, 0.9), pip(S, 16, 7.8, 0.8)]


@icon("balanced-plate", CAT, "A round plate divided into four sections, each holding a different food",
      tags=["portion plate", "nutrition", "healthy eating", "diet", "meal planning", "food groups"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(seg(12, 3, 12, 21)), detail(seg(3, 12, 21, 12)),
            pip(S, 7.6, 7.6, 1.5), Part("dot", rect(14.6, 5.9, 3.4, 3.4, L(S, 0, 0.8))),
            Part("dot", poly([(7.6, 14.4), (9.6, 17.6), (5.6, 17.6)], closed=True, r=L(S, 0, 0.4))),
            Part("dot", ellipse(16.4, 16.4, 1.7, 1.1))]


@icon("tom-yum", CAT, "A bowl of hot and sour soup with a lemongrass stalk, a mushroom and a chili",
      tags=["thai soup", "hot and sour", "lemongrass", "shrimp soup", "spicy", "southeast asian"])
def _(S):
    cap = "M5 12C5 7 10.5 7 10.5 12Z"
    return [shell(bowl(S, 12.5)), shell(cap), line(seg(14.5, 11.5, 19.5, 3.5)), line("M12 11.5C12 8.5 13 6.5 14.5 5.6")]


@icon("wonton-soup", CAT, "A bowl of clear broth with floating wontons trailing pinched wrapper tails",
      tags=["chinese soup", "dumpling soup", "broth", "wonton", "noodle shop", "dim sum"])
def _(S):
    w1 = poly([(4, 12), (8, 4.4), (12, 12)], closed=True, r=S.r)
    w2 = poly([(12, 12), (16.2, 5), (20, 12)], closed=True, r=S.r)
    return [shell(bowl(S, 12.5)), shell(w1), shell(w2)]


@icon("laksa", CAT, "A deep bowl of curry noodle soup with a halved egg and a square tofu puff",
      tags=["curry noodles", "malaysian", "singaporean", "coconut soup", "prawns", "noodle soup"])
def _(S):
    tofu = xf(rect(13.5, 5.6, 4.6, 4.6, L(S, 0.5, 1.2)), 15, 15.8, 7.9)
    return [shell(bowl(S, 12.5)), shell(circle(8.5, 8, 3.2)), dot(8.5, 8, 1.1), shell(tofu)]


@icon("udon", CAT, "A bowl of thick noodles with a battered prawn across the rim and a fish cake slice",
      tags=["japanese noodles", "tempura udon", "kake udon", "wheat noodles", "noodle soup", "prawn tempura"])
def _(S):
    return [shell(bowl(S, 13)), shell(capsule(10.5, 8.6, 18.6, 4.6, 3.6)), shell(circle(6.6, 8.4, 2.7)), dot(6.6, 8.4, 0.9)]


@icon("pozole", CAT, "A bowl of soup with puffy hominy kernels, a radish slice and a lime wedge on the rim",
      tags=["hominy", "mexican stew", "rojo", "verde", "radish", "lime"])
def _(S):
    lime = half_disc(S, 18, 11.6, 3.2, 180, 0.9)
    return [shell(bowl(S, 12.5)), shell(circle(7.8, 8, 2.5)), dot(12, 9.2, 1.3), dot(14.2, 7.4, 1.2), shell(lime) if False else shell(lime)]


@icon("tomato-soup", CAT, "A mug of smooth soup with a grilled cheese triangle dunked into it",
      tags=["grilled cheese", "soup and sandwich", "comfort food", "lunch", "mug", "dipping"])
def _(S):
    mug = "M4 8H16V16C16 19 14 20.5 12 20.5H8C6 20.5 4 19 4 16Z" if S.name == "line" else \
        "M4 9A1 1 0 0 1 5 8H15A1 1 0 0 1 16 9V16C16 19 14 20.5 12 20.5H8C6 20.5 4 19 4 16Z"
    tri = poly([(8.5, 10), (14, 1.8), (20.2, 7.2)], closed=True, r=S.r)
    return [shell(mug), line("M16 10H18.4A2.6 3.1 0 0 1 18.4 16.2H16"), shell(behind(tri, [mug], None))]


@icon("bouillabaisse", CAT, "A shallow bowl of fish stew with a fish chunk and a sauce-topped crouton",
      tags=["french", "fish stew", "provencal", "seafood soup", "rouille", "marseille"])
def _(S):
    fish = xf(rect(4.6, 6.4, 5.6, 4, L(S, 0.6, 1.4)), -15, 7.4, 8.4)
    return [shell(bowl(S, 12.5)), shell(fish), shell(circle(15.2, 8, 3.3)), dot(15.2, 8, 1.1)]


@icon("gumbo", CAT, "A round bowl of dark stew with okra slices, sausage coins and a scoop of rice",
      tags=["louisiana", "cajun", "creole", "okra", "stew", "new orleans"])
def _(S):
    def star(x, y):
        return Part("dot", poly(star_ring(x, y, 1.9, 0.95, 5), closed=True))
    st = [star(*pt_on(12, 12, 5.7, a)) for a in (-90, 30, 150)]
    co = [pip(S, *pt_on(12, 12, 5.7, a), 1.3) for a in (-30, 90, 210)]
    return [shell(circle(12, 12, 9)), detail(circle(12, 12, 2.2)) if S.name == "rounded" else detail(poly(regular(12, 12, 2.4, 6), closed=True)), *st, *co]


@icon("samgyetang", CAT, "A stone pot of broth holding a small whole chicken with jujube dates beside it",
      tags=["korean", "ginseng chicken soup", "chicken soup", "hot pot", "summer stamina", "jujube"])
def _(S):
    chick = rotd(ellipse(10.5, 8.2, 5.6, 3.3), -12, 10.5, 8.2)
    return [shell(bowl(S, 12.5)), shell(chick), dot(17, 9, 1.2), dot(19.2, 11, 0.0001) if False else dot(17.6, 6.6, 1.2)]


@icon("khao-soi", CAT, "A bowl of curry noodle soup topped with a tangled nest of crispy fried noodles",
      tags=["northern thai", "chiang mai", "curry noodles", "crispy noodles", "coconut curry", "noodle soup"])
def _(S):
    return [shell(bowl(S, 13)), line(poly([(5.6, 11), (8, 5), (10.4, 10), (12.6, 4), (15, 10), (18.4, 5.2)], r=S.r * 0.5)),
            line(poly([(7, 8), (11, 9), (14, 5.5), (18, 9.6)], r=S.r * 0.5))]


@icon("cassoulet", CAT, "An earthenware bowl of beans with sausage and a duck leg bone sticking up",
      tags=["french", "bean stew", "duck confit", "toulouse", "casserole", "winter"])
def _(S):
    heap = bumps([(5.5, 13), (7.5, 9.6), (11, 8.4), (14, 10), (15.5, 13)], r=3.0) + "Z"
    return [shell(bowl(S, 13)), shell(heap), dot(9.4, 11.2, 0.9), dot(12.4, 11.2, 0.9), line(seg(16.2, 12.6, 19.6, 5.6)),
            shell(circle(20, 4.6, 1.6)) if False else dot(20, 4.6, 1.8)]


@icon("fried-calamari", CAT, "A plate of battered squid rings piled together",
      tags=["squid rings", "fried squid", "seafood", "appetizer", "tapas", "rings"])
def _(S):
    return [line(circle(6.8, 13, 3)), line(circle(13.8, 13, 3)), line(circle(10.3, 6.4, 3)), plate(S),
            line(circle(17.4, 6.6, 0.01)) if False else dot(18, 8, 0.0001) if False else line(seg(18.4, 11.5, 19, 9))]


@icon("pulled-pork", CAT, "A bun heaped with shredded pork strands",
      tags=["barbecue", "bbq", "shredded meat", "sandwich", "slider", "smoked"])
def _(S):
    heap = bumps([(4.5, 15.5), (5.6, 10.5), (9.5, 7.2), (14.5, 7.2), (18.4, 10.5), (19.5, 15.5)], r=4.4) + "Z"
    return [shell(heap), shell(rect(3, 17, 18, 3.8, L(S, 1.5, 1.9))), detail(seg(8.5, 13, 10.5, 9.8)), detail(seg(12, 13.4, 13.8, 10)),
            detail(seg(15.5, 13.2, 17, 11))]


@icon("tonkatsu", CAT, "A breaded pork cutlet sliced into strips beside a tall mound of shredded cabbage",
      tags=["katsu", "japanese cutlet", "pork cutlet", "breaded", "cabbage", "fried"])
def _(S):
    strips = [shell(rect(x, 6.5, 3.4, 13.5, L(S, 1, 1.7))) for x in (3.2, 7.6, 12)]
    cab = "M16 20.5C16 12 21 12 21 20.5Z"
    return [*strips, shell(cab), detail("M17.4 19.4C17.6 16.6 18.6 15.6 19.6 15.2")]


# =========================================================================== sandwiches, appetizers and plates


@icon("fruit-sandwich", CAT, "A crustless white bread sandwich cut open showing whole strawberries set in cream",
      tags=["sando", "strawberry sandwich", "japanese", "cream", "dessert sandwich", "fruit sando"])
def _(S):
    berry = "M12 14.2C9 12.4 8.4 9.4 10.4 9.4C11.3 9.4 12 10 12 10C12 10 12.7 9.4 13.6 9.4C15.6 9.4 15 12.4 12 14.2Z"
    return [shell(rect(3, 3.5, 18, 4.5, L(S, 1.5, 2.2))), shell(rect(3, 16, 18, 4.5, L(S, 1.5, 2.2))),
            Part("dot", xf(berry, 0, 12, 12, dx=-4.2)), Part("dot", xf(berry, 0, 12, 12, dx=4.2))]


@icon("sloppy-joe", CAT, "A round bun with loose saucy mince spilling out over the edges of the bottom bun",
      tags=["loose meat", "ground beef", "diner", "american", "messy sandwich", "manwich"])
def _(S):
    top = "M5 9C5 5 8.5 3.5 12 3.5C15.5 3.5 19 5 19 9Z"
    mince = bumps([(3, 16.5), (3.6, 13.4), (7, 11.6), (12, 11), (17, 11.6), (20.4, 13.4), (21, 16.5)], r=4.2) + "Z"
    return [shell(top), shell(mince), shell(rect(4, 17.5, 16, 3.4, L(S, 1.5, 1.7))), pip(S, 8, 14.2, 0.9), pip(S, 12.4, 13.6, 0.9), pip(S, 16.4, 14.4, 0.9)]


@icon("french-dip", CAT, "A long roll sandwich with one end dipped into a small cup of broth",
      tags=["au jus", "roast beef sandwich", "dipping sauce", "hoagie", "deli", "broth"])
def _(S):
    cup = poly([(13, 14.5), (21, 14.5), (19.6, 20.5), (14.4, 20.5)], closed=True, r=S.r)
    roll = capsule(5.2, 6.6, 15.5, 13.8, 5.2)
    return [shell(cup), shell(behind(roll, [cup], None))]


@icon("jalapeno-poppers", CAT, "Three halved peppers stuffed with cheese, lined up side by side",
      tags=["stuffed peppers", "bar food", "appetizer", "cheese", "fried", "bacon wrapped"])
def _(S):
    out = []
    for x in (5.6, 12, 18.4):
        out += [shell(capsule(x, 10.6, x, 15.6, 5.2)), line(seg(x, 5.4, x + 0.9, 3.4)), oval_dot(x, 13, 1.0, 2.4)]
    return out


@icon("potato-skins", CAT, "Two hollowed potato halves shaped like boats, filled with melted cheese and bacon",
      tags=["loaded potato", "bar food", "appetizer", "cheese", "bacon", "baked potato"])
def _(S):
    a = ellipse(9.5, 8.4, 6.8, 3.9)
    b = behind(ellipse(14.5, 15.4, 6.8, 3.9), [a], 1.5)
    return [shell(a), shell(b), detail(ellipse(9.5, 8.4, 3.2, 1.2)) if False else pip(S, 8, 8.4, 1.0), pip(S, 11.2, 8.4, 1.0),
            pip(S, 13, 15.4, 1.0), pip(S, 16.2, 15.4, 1.0)]


@icon("biscuits-and-gravy", CAT, "A split round biscuit covered with a lumpy peppered gravy pour",
      tags=["sausage gravy", "southern breakfast", "american breakfast", "comfort food", "biscuit", "diner"])
def _(S):
    gravy = ("M4.5 13C4.5 8.5 8 7 12 7C16 7 19.5 8.5 19.5 13Q18.6 16 17.2 13Q16 15.6 14.4 13Q13.2 15.6 11.6 13"
             "Q10.2 15.6 8.6 13Q7.4 16 6 13Q5.3 14 4.5 13Z")
    return [shell(rect(3.5, 14.5, 17, 6, L(S, 1.5, 2.6))), shell(gravy), pip(S, 8.6, 10.6, 0.9), pip(S, 12.6, 9.6, 0.9), pip(S, 15.6, 11.4, 0.9)]


@icon("crab-rangoon", CAT, "A fried wonton with four corners pinched together into a star-shaped point",
      tags=["fried wonton", "cream cheese", "chinese takeout", "appetizer", "dumpling", "american chinese"])
def _(S):
    star = poly(star_ring(12, 12, 9.2, 4.6, 4, start=-45), closed=True, r=S.r * 0.7)
    return [shell(star), detail(seg(12, 12, 12, 12.01)) if False else pip(S, 12, 12, 1.3)]


@icon("siu-mai", CAT, "An open topped cylindrical dumpling with pleated wrapper sides and a dot of roe on top",
      tags=["shumai", "dim sum", "pork dumpling", "steamed", "cantonese", "yum cha"], aliases=["shumai"])
def _(S):
    body = union(ellipse(12, 8.4, 6.4, 2.6), rect(5.6, 8.4, 12.8, 9.6), ellipse(12, 18, 6.4, 2.6))
    return [shell(body), detail(seg(9, 11.6, 9, 19.4)), detail(seg(12, 11.6, 12, 20)), detail(seg(15, 11.6, 15, 19.4)), pip(S, 12, 8.4, 1.3)]


@icon("churrasco", CAT, "A long sword skewer standing upright with a curved slab of grilled meat and a knife slicing it",
      tags=["brazilian barbecue", "rodizio", "espeto", "grilled meat", "steakhouse", "skewer"])
def _(S):
    meat = "M7.5 5.6C14.5 4.6 18.6 8.6 18.6 12.6C18.6 16.6 14 19 7.5 19Z"
    blade = poly([(14.2, 9.4), (21, 3.6), (21, 7)], closed=True, r=S.r * 0.4)
    return [line(seg(7.5, 2.6, 7.5, 21.4)), shell(meat), shell(blade)]


@icon("asado", CAT, "A butterflied cut of meat spread on an iron cross frame over a fire",
      tags=["argentinian barbecue", "parrilla", "whole lamb", "grill", "open fire", "gaucho"])
def _(S):
    flame = poly([(6.5, 21.4), (8, 17.4), (10, 19.6), (12, 16.2), (14, 19.6), (16, 17.4), (17.5, 21.4)], closed=True)
    return [shell(ellipse(12, 9, 6.6, 5.2)), line(seg(12, 2.4, 12, 15.4)), line(seg(5.2, 7.4, 18.8, 7.4)), solid(flame)]


@icon("baked-brie", CAT, "A round cheese wheel with a scored crosshatch top and a wedge cut out that oozes",
      tags=["brie en croute", "warm cheese", "appetizer", "party food", "camembert", "cheese board"])
def _(S):
    wheel = path_to_d(D(P(circle(12, 12, 9)), P(poly([(12, 12), (22, 5), (22, 19)], closed=True))))
    return [shell(wheel), detail(seg(5.6, 8.4, 11, 14)), detail(seg(5.6, 14.4, 9, 6.6)) if False else detail(seg(9, 5.2, 14, 10.8))]


@icon("galician-octopus", CAT, "A round wooden plate of sliced octopus rounds dotted with paprika",
      tags=["pulpo a la gallega", "pulpo", "spanish tapas", "seafood", "paprika", "tentacle"], aliases=["pulpo-a-la-gallega"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(circle(8.6, 9.2, 2.4)), pip(S, 8.6, 9.2, 0.9), detail(circle(15.4, 9.2, 2.4)), pip(S, 15.4, 9.2, 0.9),
            detail(circle(12, 15.6, 2.4)), pip(S, 12, 15.6, 0.9)]


@icon("hallaca", CAT, "A rectangular banana leaf parcel folded flat and tied with string in a crossed pattern",
      tags=["venezuelan", "christmas tamale", "banana leaf", "wrapped", "string", "tamal"])
def _(S):
    return [shell(rect(3, 5.5, 18, 13, L(S, 1.5, 3))), detail(seg(5, 7, 19, 17)), detail(seg(5, 17, 19, 7))]


@icon("gambas-al-ajillo", CAT, "A small terracotta dish of prawns in bubbling oil with garlic slices",
      tags=["garlic prawns", "garlic shrimp", "spanish tapas", "cazuela", "seafood", "sizzling"])
def _(S):
    return [shell(bowl(S, 13)), line(arc(8.6, 9, 3.3, 140, 400)), oval_dot(15.6, 8.4, 1.7, 1.1), oval_dot(17.6, 10.6, 1.4, 1.0)]


@icon("nasi-goreng", CAT, "A mound of fried rice topped with a fried egg and prawn crackers leaning against it",
      tags=["indonesian fried rice", "kerupuk", "fried egg", "rice dish", "malaysian", "krupuk"])
def _(S):
    heap = bumps([(3.5, 18.5), (4.6, 13.4), (8, 10), (12, 9), (15, 11.6), (15.6, 18.5)], r=4.6) + "Z"
    crack = behind(circle(18, 12.4, 3.5), [heap], 1.3)
    return [shell(heap), shell(crack), plate(S), shell(circle(9.6, 6.2, 2.6)), dot(9.6, 6.2, 0.95)]


@icon("baba-ganoush", CAT, "A shallow bowl of smooth eggplant dip with a drizzle swirl and pomegranate seeds",
      tags=["baba ghanoush", "eggplant dip", "middle eastern", "mezze", "tahini", "smoky"], aliases=["baba-ghanoush"])
def _(S):
    return [shell(bowl(S, 12.5)), line("M5.5 9.6Q9 6.2 12 9.4T18.5 9"), dot(9, 4.4, 1.0), dot(13, 4.6, 1.0), dot(16.4, 5.4, 1.0)]


@icon("fattoush", CAT, "A bowl of chopped salad with crisp triangular pita chips sticking up out of it",
      tags=["lebanese salad", "pita salad", "sumac", "mezze", "levantine", "bread salad"])
def _(S):
    c1 = xf(poly([(6, 12), (8.5, 3.6), (12, 12)], closed=True, r=S.r), -15, 9, 10)
    c2 = xf(poly([(11, 12), (15.4, 4.2), (18.6, 12)], closed=True, r=S.r), 12, 14.5, 10)
    return [shell(bowl(S, 12.5)), shell(c1), shell(c2), pip(S, 12, 9.6, 0.9)]


@icon("spanakopita", CAT, "A flat triangle of phyllo pastry with flaky layered edges",
      tags=["greek", "spinach pie", "phyllo", "filo", "feta", "savory pastry"])
def _(S):
    tri = poly([(3, 20), (21, 20), (12, 3.6)], closed=True, r=S.r)
    return [shell(tri), detail(wave_d(6.4, 17.6, 15.6, 0.6, 3.7)), detail(wave_d(9, 15, 11.2, 0.5, 3))]


@icon("moussaka", CAT, "A square slice showing layered eggplant rounds under a thick smooth golden topping",
      tags=["greek", "eggplant casserole", "baked", "bechamel", "layered", "mediterranean"])
def _(S):
    return [shell(rect(3, 4, 18, 16, L(S, 1.5, 3))), detail(seg(3, 8.6, 21, 8.6)), detail(seg(3, 14, 21, 14)),
            oval_dot(7.6, 11.3, 2.2, 1.0), oval_dot(12, 11.3, 2.2, 1.0), oval_dot(16.4, 11.3, 2.2, 1.0),
            oval_dot(7.6, 16.8, 2.2, 1.0), oval_dot(12, 16.8, 2.2, 1.0), oval_dot(16.4, 16.8, 2.2, 1.0)]


@icon("rosti", CAT, "A round golden shredded potato cake seen from the side with a crisp shredded top",
      tags=["swiss potato", "hash brown", "shredded potato", "fried egg", "breakfast", "switzerland"], aliases=["roesti"])
def _(S):
    ry = L(S, 4.0, 4.6)
    body = union(ellipse(12, 10.4, 9, ry), ellipse(12, 15.2, 9, ry), rect(3, 10.4, 18, 4.8))
    return [shell(body), detail(seg(6.6, 10, 9, 7.8)), detail(seg(11, 12, 13.4, 9.4)), detail(seg(15.2, 12.6, 17.4, 10)),
            detail(seg(6.6, 18.4, 8.2, 15.4)), detail(seg(11.2, 19.6, 12.8, 16.4)), detail(seg(16, 18.4, 17.6, 15.4))]


@icon("langos", CAT, "A round puffy fried dough disk spread with sour cream and topped with grated cheese",
      tags=["hungarian", "fried dough", "sour cream", "cheese", "street food", "fair food"])
def _(S):
    dome = "M3 18C3 12 7.5 9.4 12 9.4C16.5 9.4 21 12 21 18Z"
    cream = "M8.5 10.4C8.5 6.6 15.5 6.6 15.5 10.4Z"
    return [shell(dome), shell(cream), detail(wave_d(5.6, 18.4, 15, 0.7, 3.2)), pip(S, 10, 12.8, 0.8), pip(S, 14.2, 13, 0.8)]


@icon("flammkuchen", CAT, "A thin rectangular flatbread on a wooden board with onion rings and bacon bits",
      tags=["tarte flambee", "alsatian", "german pizza", "flatbread", "onion", "bacon"])
def _(S):
    return [shell(rect(2.5, 4, 19, 16, L(S, 1.5, 3))), detail(rect(6, 7.6, 12, 8.8, L(S, 0, 1))), line(circle(9.6, 12, 1.7)),
            pip(S, 14.4, 10.4, 0.9), pip(S, 14.4, 13.8, 0.9)]


@icon("zapiekanka", CAT, "A long half baguette open faced with mushrooms, melted cheese and a sauce zigzag",
      tags=["polish", "open sandwich", "street food", "baguette", "mushrooms", "ketchup"])
def _(S):
    return [shell(capsule(6.4, 12, 17.6, 12, 7.6)), detail(poly([(5.6, 12.6), (8.6, 9.6), (11.6, 12.6), (14.6, 9.6), (17.6, 12.6)], r=S.r * 0.4)),
            pip(S, 9.4, 14.6, 0.85), pip(S, 14.6, 14.6, 0.85)]


@icon("cevapi", CAT, "A row of small skinless sausages beside a folded flatbread",
      tags=["cevapcici", "balkan", "grilled meat", "somun", "minced meat rolls", "bosnian"], aliases=["cevapcici"])
def _(S):
    return [*[shell(capsule(5.6, y, 11.4, y, 4.2)) for y in (6.4, 12, 17.6)], shell(half_disc(S, 17, 12, 4.2, -90, 1.0))]


@icon("knodel", CAT, "Two large round dumplings on a plate, one sliced showing a bread cube texture",
      tags=["knoedel", "german dumpling", "bread dumpling", "bavarian", "gravy", "semmelknodel"], aliases=["knoedel"])
def _(S):
    a = circle(8, 13.2, 4.6)
    b = behind(circle(16, 13.2, 4.6), [a], 1.4)
    return [shell(a), shell(b), plate(S), pip(S, 16.6, 12, 0.8), pip(S, 15.4, 14.6, 0.8)]


@icon("francesinha", CAT, "A square layered sandwich covered in sauce with a fried egg on top, in a shallow dish",
      tags=["portuguese", "porto", "sandwich", "beer sauce", "melted cheese", "fried egg"])
def _(S):
    return [shell(rect(4.5, 9.2, 15, 8.4, L(S, 1.5, 2.6))), detail(seg(4.5, 13.4, 19.5, 13.4)), shell(circle(12, 5.6, 2.6)), dot(12, 5.6, 0.9), plate(S)]


@icon("dhokla", CAT, "Two stacked spongy steamed cakes with mustard seed dots and a green chili on top",
      tags=["gujarati", "steamed cake", "chickpea", "indian snack", "farsan", "khaman"])
def _(S):
    return [shell(rect(3.5, 15, 17, 5.5, L(S, 1.5, 2.4))), shell(rect(5.5, 9, 13, 5.5, L(S, 1.5, 2.4))), line("M13.6 8.4C13.6 5.6 15.6 3.6 18.6 4"),
            pip(S, 8, 17.7, 0.8), pip(S, 12, 17.7, 0.8), pip(S, 16, 17.7, 0.8), pip(S, 9.6, 11.7, 0.8), pip(S, 14.4, 11.7, 0.8)]


@icon("pav-bhaji", CAT, "Two buttered bun halves beside a bowl of mashed vegetable curry",
      tags=["mumbai", "street food", "bhaji", "bread rolls", "butter", "indian"])
def _(S):
    cup = ("M11.6 14H21C21 18 18.6 20.6 16.3 20.6C14 20.6 11.6 18 11.6 14Z" if S.name == "line" else
           "M12.6 14H20A1 1 0 0 1 21 15C20.8 18.4 18.6 20.6 16.3 20.6C14 20.6 11.8 18.4 11.6 15A1 1 0 0 1 12.6 14Z")
    heap = bumps([(13.2, 14), (14.4, 10.8), (17, 10), (19.4, 14)], r=2.4) + "Z"
    return [shell(rect(2.8, 4, 6.6, 7, L(S, 1.5, 2.6))), shell(rect(2.8, 13, 6.6, 7, L(S, 1.5, 2.6))), shell(cup), shell(heap)]


@icon("chole-bhature", CAT, "A large puffed round fried bread beside a small bowl of chickpea curry",
      tags=["punjabi", "chana masala", "puri", "fried bread", "north indian", "chickpeas"])
def _(S):
    bread = circle(9.4, 9.4, 6.4)
    cup = ("M13.6 15H21C21 18.4 19 20.8 17.3 20.8C15.6 20.8 13.6 18.4 13.6 15Z" if S.name == "line" else
           "M14.4 15H20.2A1 1 0 0 1 21 16C20.8 18.6 19 20.8 17.3 20.8C15.6 20.8 13.8 18.6 13.6 16A1 1 0 0 1 14.4 15Z")
    return [shell(cup), shell(behind(bread, [cup], 1.4)), detail("M6 8.4Q9.4 5.4 12.8 8.4"), dot(16.6, 17, 0.9)]


@icon("appam", CAT, "A bowl-shaped pancake with thin lacy crisp edges and a soft thick centre",
      tags=["hoppers", "palappam", "kerala", "sri lankan", "rice pancake", "fermented"])
def _(S):
    return [shell(bowl(S, 13)), line(bumps([(3, 13), (5.7, 11), (8.4, 13), (11.1, 11), (13.8, 13), (16.5, 11), (19.2, 13), (21, 12)], r=1.9)),
            Part("dot", circle(12, 16.4, 2.2))]


@icon("puttu", CAT, "A tall cylinder of steamed rice flour with alternating horizontal coconut bands",
      tags=["kerala", "steamed rice cake", "coconut", "breakfast", "south indian", "kadala curry"])
def _(S):
    return [shell(rect(6.5, 7, 11, 14, L(S, 1.5, 3))), detail(seg(6.5, 11, 17.5, 11)), detail(seg(6.5, 15, 17.5, 15)),
            line("M9.6 5.2C8.6 3.8 10.6 3.2 9.6 2"), line("M14.4 5.2C13.4 3.8 15.4 3.2 14.4 2")]
