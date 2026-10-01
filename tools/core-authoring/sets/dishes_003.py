"""TypeIcon Core: world dishes (batch dishes_003).

Southeast and South Asian, Middle Eastern, African and other world dishes, salads, bowls, soups and classic
plates, drawn from the food itself. Side views sit on a shallow plate or in a round bowl; top views sit on a
round plate (r 9).
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


def frill(x, y, ang, w=3.4, h=2.6):
    """Zigzag paper cap (open polyline) sitting at (x, y) and pointing away at angle ang (degrees)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    pts = [(x + nx * (-w / 2), y + ny * (-w / 2)), (x + ux * h + nx * (-w / 4), y + uy * h + ny * (-w / 4)),
           (x + nx * 0 + ux * (h * 0.5), y + uy * (h * 0.5)),
           (x + ux * h + nx * (w / 4), y + uy * h + ny * (w / 4)), (x + nx * (w / 2), y + ny * (w / 2))]
    return pts



def dome(x0, x1, base, h):
    """Closed dome sitting on the line y=base (cubic, peak height h)."""
    k = h * 4 / 3
    return f"M{fmt(x0)} {fmt(base)}C{fmt(x0)} {fmt(base - k)} {fmt(x1)} {fmt(base - k)} {fmt(x1)} {fmt(base)}Z"


def oval(cx, cy, rx, ry, deg=0.0) -> str:
    return rotd(ellipse(cx, cy, rx, ry), deg, cx, cy)


def ovdot(cx, cy, rx, ry, deg=0.0) -> Part:
    return Part("dot", oval(cx, cy, rx, ry, deg))


def on_plate(S, dome_d, **kw):
    """One outline: a heap (built on y=19) merged into a shallow plate."""
    return shell(union(dome_d, plate(S, **kw).d))


def lune(x1, y1, x2, y2, b1, b2):
    """Crescent between two points; both edges bulge to the same side (b1 outer, b2 inner, half widths)."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx * b1 * 2)} {fmt(my + ny * b1 * 2)} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(mx + nx * b2 * 2)} {fmt(my + ny * b2 * 2)} {fmt(x1)} {fmt(y1)}Z")


def bowl34(S, cy=9.5, rx=8.5, ry=3.2, bottom=20.5):
    """A round bowl seen from slightly above: returns (body shell, front rim arc detail)."""
    x0, x1 = 12 - rx, 12 + rx
    if S.name == "line":
        body = (f"M{fmt(x0)} {cy}A{rx} {ry} 0 0 1 {fmt(x1)} {cy}C{fmt(x1)} {cy + 7} 16.5 {bottom} 12 {bottom}"
                f"C7.5 {bottom} {fmt(x0)} {cy + 7} {fmt(x0)} {cy}Z")
    else:
        body = (f"M{fmt(x0)} {cy}A{rx} {ry} 0 0 1 {fmt(x1)} {cy}C{fmt(x1)} {cy + 6} {fmt(x1 - 1.5)} {bottom - 1.5} {fmt(x1 - 4)} {bottom}"
                f"H{fmt(x0 + 4)}C{fmt(x0 + 1.5)} {bottom - 1.5} {fmt(x0)} {cy + 6} {fmt(x0)} {cy}Z")
    return shell(body), detail(f"M{fmt(x0)} {cy}A{rx} {ry} 0 0 0 {fmt(x1)} {cy}")


def sqr(cx, cy, s, deg=0.0, rc=0.0) -> Part:
    """A small solid square (cube) centred at (cx, cy), turned by deg."""
    return Part("dot", rotd(rect(cx - s / 2, cy - s / 2, s, s, rc), deg, cx, cy))


def tri_dot(pts, r=0.0) -> Part:
    return Part("dot", poly(pts, closed=True, r=r))


def chord(cx, cy, r, deg, off):
    """Segment of the chord of a circle (radius r) running at angle deg, offset from the centre by off."""
    a = math.radians(deg)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    h = math.sqrt(max(r * r - off * off, 0))
    px, py = cx + nx * off, cy + ny * off
    return seg(px - ux * h, py - uy * h, px + ux * h, py + uy * h)


def chestnut(cx, cy, r=0.0):
    return poly([(cx, cy - 3.6), (cx + 3.4, cy + 0.6), (cx + 2.6, cy + 3.4), (cx - 2.6, cy + 3.4), (cx - 3.4, cy + 0.6)], closed=True, r=r)


def crumb(S, cx, cy, r):
    """A craggy (Line) or smooth (Rounded) round fritter outline."""
    if S.name == "line":
        return poly(star_ring(cx, cy, r + 0.45, r - 0.45, 8), closed=True)
    return circle(cx, cy, r)


# =========================================================================== Southeast and South Asia


@icon("summer-roll", CAT, "A translucent rice paper roll with shrimp and greens showing through",
      tags=["spring roll", "rice paper roll", "vietnamese", "goi cuon", "fresh roll", "shrimp"],
      aliases=["fresh-spring-roll"])
def _(S):
    body = hcyl(S, 3.5, 20.5, 7, 17, 3.2)
    face = ellipse(17.3, 12, 3.2, 5)
    shrimp = "M7 10.2C10.5 8.5 12.5 10.2 13 13"
    leaf = poly(zigzag(5.6, 11, 14.6, 1.3, 2), r=L(S, 0, 0.5))
    return [shell(xf(body, -28)), detail(xf(shrimp, -28)), detail(xf(face, -28))]


@icon("zongzi", CAT, "A pyramid-shaped bamboo leaf parcel tied with string",
      tags=["rice dumpling", "sticky rice parcel", "dragon boat", "bamboo leaf", "chinese"])
def _(S):
    hull = poly([(12, 3), (3.5, 17.5), (11, 21), (20.5, 16.5)], closed=True, r=L(S, 0, 1.2))
    return [shell(hull), detail(seg(12, 3.5, 11, 20.5)), detail("M7.7 10.3Q12 13.6 16.6 10.3")]


@icon("scallion-pancake", CAT, "A thick round flaky flatbread with green onion flecks on top",
      tags=["green onion pancake", "cong you bing", "flatbread", "chinese", "street food"],
      aliases=["green-onion-pancake"])
def _(S):
    body = "M2.5 9.5A9.5 6 0 0 1 21.5 9.5V14.5A9.5 6 0 0 1 2.5 14.5Z"
    return [shell(body), detail("M2.5 9.5A9.5 6 0 0 0 21.5 9.5"), detail(seg(6.5, 8.5, 9, 7)), detail(seg(11, 10.5, 14, 8.5)),
            detail(seg(15, 6.6, 17.5, 8.2))]


@icon("claypot-rice", CAT, "A clay pot with a domed lid and a side handle, steam rising from the rice inside",
      tags=["clay pot", "claypot", "hong kong", "chinese sausage", "rice", "donabe"],
      aliases=["clay-pot-rice"])
def _(S):
    body = ("M3.5 12H18.5C18.5 17.5 16 21 11 21C6 21 3.5 17.5 3.5 12Z" if S.name == "line" else
            "M5 12H17A1.5 1.5 0 0 1 18.5 13.5C18.1 18 15.4 21 11 21C6.6 21 3.9 18 3.5 13.5A1.5 1.5 0 0 1 5 12Z")
    lid = "M5 12.2C5 8.2 7.6 6.2 11 6.2C14.4 6.2 17 8.2 17 12.2Z"
    return [shell(union(body, lid)), detail(seg(5, 12, 17, 12)), line(seg(18.5, 15.5, 22, 15.5)), line(seg(11, 6.2, 11, 3.5))]


@icon("chicken-rice", CAT, "A plate with a dome of rice and stacked slices of poached chicken",
      tags=["hainanese chicken rice", "poached chicken", "rice plate", "singapore", "hawker"],
      aliases=["hainanese-chicken-rice"])
def _(S):
    sl = lambda y: Part("dot", capsule(14.6, y, 18.2, y, 2.6) if S.name == "rounded" else rect(13.2, y - 1.3, 6.2, 2.6, 0.3))
    return [shell(circle(12, 12, 9.5)), detail(circle(8.2, 12, 3.7)), sl(8.4), sl(12), sl(15.6)]


@icon("fried-rice", CAT, "A mound of fried rice with diced vegetables and a spoon stuck in",
      tags=["egg fried rice", "rice", "stir fry", "takeaway", "chinese", "spoon"])
def _(S):
    return [on_plate(S, dome(4.5, 18.5, 19, 9.5)), line(seg(13, 11.5, 18, 7)),
            shell(oval(19.4, 5.8, 2.1, 3.2, 45)), blob(8, 14, 2, 2, L(S, 0, 0.5)), blob(12.5, 12.5, 2, 2, L(S, 0, 0.5)),
            blob(14, 15.5, 2, 2, L(S, 0, 0.5))]


@icon("instant-noodle-cup", CAT, "A paper cup of instant noodles with the lid peeled back",
      tags=["cup ramen", "ramen cup", "instant ramen", "noodle cup", "quick meal", "convenience"])
def _(S):
    cup = poly([(5.5, 10), (18.5, 10), (16.5, 21), (7.5, 21)], closed=True, r=L(S, 0, 1))
    return [shell(cup), detail(seg(6.3, 15, 17.7, 15)), line(wave_d(6.5, 17.5, 6.6, 1.2, 4.5)),
            line(poly([(5.5, 10), (3.5, 6.5), (6, 3.5)], r=L(S, 0, 1)))]


@icon("pad-thai", CAT, "A plate of stir-fried flat noodles with a lime wedge",
      tags=["thai noodles", "stir fried noodles", "rice noodles", "thailand", "lime", "peanuts"])
def _(S):
    lime = xf("M-3.1 0A3.1 3.1 0 0 1 3.1 0Z".replace("M-3.1 0", "M14.8 0").replace("A3.1 3.1 0 0 1 3.1 0Z", "A3.1 3.1 0 0 1 21 0Z"), 135, 17.9, 0, dx=0, dy=17.9)
    return [shell(circle(10.5, 10.5, 7.9)), detail(wave_d(5.2, 15.8, 8, 0.8, 5.3)), detail(wave_d(5.2, 15.8, 12.6, 0.8, 5.3)), shell(lime)]


@icon("nasi-lemak", CAT, "A banana leaf with a dome of coconut rice, a fried egg and cucumber",
      tags=["malaysian", "coconut rice", "banana leaf", "egg", "breakfast", "sambal"])
def _(S):
    leafd = "M2 19C6 16.5 18 16.5 22 19C18 21.6 6 21.6 2 19Z" if S.name == "rounded" else "M2 19L6 17L18 17L22 19L18 21.5L6 21.5Z"
    return [shell(union(dome(3.5, 12.5, 18.5, 9), leafd)), shell(oval(17.6, 13.6, 4, 3)), dot(17.6, 13.6, 1.0)]


@icon("mango-sticky-rice", CAT, "A plate with a mound of sticky rice beside a mango with a leaf",
      tags=["thai dessert", "mango", "sticky rice", "coconut", "sweet", "thailand"])
def _(S):
    mango = oval(16.8, 13, 4, 5.4, -22)
    return [on_plate(S, dome(2.5, 10, 19, 7)), shell(union(mango, rect(14, 16, 6, 3.5))), shell(leaf(17, 7.8, 20.5, 4.3, 1.5))]


@icon("tumpeng", CAT, "A tall cone of rice on a round tray with small side dishes",
      tags=["nasi tumpeng", "rice cone", "indonesian", "festive rice", "ceremony", "javanese"])
def _(S):
    cone = poly([(12, 3.2), (6.5, 16), (17.5, 16)], closed=True, r=L(S, 0, 1.8))
    return [shell(union(cone, plate(S, 18, 2.5, 21.5, 2.5).d)), dot(4.2, 15.6, 1.3), dot(19.8, 15.6, 1.3)]


@icon("prawn-crackers", CAT, "A pile of puffed curly prawn crackers with wavy edges",
      tags=["shrimp chips", "krupuk", "kerupuk", "keropok", "puffed chips", "snack"],
      aliases=["shrimp-chips"])
def _(S):
    a = scallop_ring(8.6, 9, 5.8, 9, 1.15, -80)
    b = scallop_ring(15, 14.6, 6.8, 10, 1.15, -60)
    return [shell(behind(a, [b], 1.25)), shell(b), detail(arc(15, 14.6, 2.6, 200, 330))]


@icon("banana-leaf-meal", CAT, "A banana leaf platter with a mound of rice and small portions of curry and vegetables",
      tags=["south indian meal", "thali", "sadya", "rice", "curry", "vegetarian"],
      aliases=["sadya"])
def _(S):
    leafd = poly([(2, 12), (5, 6.5), (19, 6.5), (22, 12), (19, 17.5), (5, 17.5)], closed=True, r=L(S, 0, 2))
    return [shell(leafd), detail(circle(9, 12, 3)), dot(15.5, 9.5, 1.2), dot(15.5, 14.5, 1.2), dot(19, 12, 1.1)]


@icon("samosa", CAT, "A triangular samosa pastry with a crimped seam",
      tags=["indian snack", "fried pastry", "pakistani", "chutney", "street food", "appetizer"])
def _(S):
    hull = poly([(11, 3), (2.5, 16.5), (10, 21), (21.5, 15.5)], closed=True, r=L(S, 0, 1.4))
    return [shell(hull), detail(poly([(11, 4), (12.3, 8), (9.7, 12), (12.3, 16), (10, 19.5)], r=L(S, 0, 0.5)))]


@icon("biryani", CAT, "A round pot with side handles heaped with spiced rice grains and a herb sprig",
      tags=["rice pot", "handi", "spiced rice", "indian", "hyderabadi", "dum"])
def _(S):
    pot = ("M4.5 13.5H19.5C19.5 18 16.5 21.5 12 21.5C7.5 21.5 4.5 18 4.5 13.5Z" if S.name == "line" else
           "M6 13.5H18A1.5 1.5 0 0 1 19.5 15C19.2 18.8 16 21.5 12 21.5C8 21.5 4.8 18.8 4.5 15A1.5 1.5 0 0 1 6 13.5Z")
    return [shell(pot), shell(dome(6, 18, 13.5, 8)), line(seg(2, 16, 4.6, 16)), line(seg(19.4, 16, 22, 16)),
            ovdot(9.2, 10.4, 1.3, 0.7, -30), ovdot(12.4, 8.2, 1.3, 0.7, 40), ovdot(14.8, 11, 1.3, 0.7, -20), ovdot(11.6, 11.6, 1.3, 0.7, 25)]




# =========================================================================== South Asia, Middle East and Africa


@icon("dosa", CAT, "A long golden rolled crepe lying diagonally beside a small bowl of chutney",
      tags=["south indian", "crepe", "rice crepe", "masala dosa", "chutney", "sambar"],
      aliases=["dosai"])
def _(S):
    body = hcyl(S, 2.5, 20, 6, 14, 2.6)
    face = "M17.4 6A2.6 4 0 0 0 17.4 14"
    return [shell(xf(body, -28, 11, 10, dx=-0.5, dy=-1)), detail(xf(face, -28, 11, 10, dx=-0.5, dy=-1)),
            dot(7.2, 12.4, 0.9), dot(11, 10.6, 0.9),
            shell("M13.5 17.3H22C22 19.8 20.2 21 17.8 21C15.4 21 13.5 19.8 13.5 17.3Z")]


@icon("idli", CAT, "Three round steamed rice cakes stacked on a plate",
      tags=["south indian", "rice cake", "steamed", "sambar", "breakfast", "vegetarian"],
      aliases=["idly"])
def _(S):
    top = oval(11.8, 7.6, 4.3, 3)
    return [shell(top), shell(behind(oval(7.2, 13, 4.3, 3), [top], 1.0)), shell(behind(oval(16.6, 12, 4.3, 3), [top], 1.0)), plate(S)]


@icon("chapati", CAT, "A quarter-folded round flatbread with scattered brown cooked spots",
      tags=["roti", "phulka", "indian flatbread", "tortilla", "wheat", "bread"],
      aliases=["roti"])
def _(S):
    if S.name == "line":
        q = "M4 20V3.5H5C13.5 3.5 20.5 10.5 20.5 19V20Z"
    else:
        q = "M4 17.5V9.5C4 6.5 6 4 9 4C15.8 4 20 8.2 20 15C20 18 18 20 15 20H6.5C5 20 4 19 4 17.5Z"
    return [shell(q), dot(9.5, 13.2, 1.1), dot(13.6, 14.8, 1.1), dot(14.3, 9.2, 1.1)]


@icon("pani-puri", CAT, "A round crisp puri shell cracked open at the top and filled with spiced water",
      tags=["golgappa", "puchka", "chaat", "indian street food", "snack", "crisp shells"],
      aliases=["golgappa", "puchka"])
def _(S):
    cut = poly([(1, 0), (23, 0), (23, 9), (19, 9), (17.5, 6.8), (15, 9), (12.5, 6.8), (10, 9), (7.5, 6.8), (5, 9), (1, 9)], closed=True)
    ball = path_to_d(D(P(circle(12, 13, 8.2)), P(cut)))
    return [shell(ball), detail(wave_d(6, 18, 12.3, 0.9, 6))]


@icon("pakora", CAT, "A small woven basket heaped with craggy fried vegetable fritters",
      tags=["bhaji", "onion bhaji", "fritters", "fried snack", "indian", "tea time"],
      aliases=["bhaji"])
def _(S):
    basket = poly([(4, 13.5), (20, 13.5), (18, 21), (6, 21)], closed=True, r=L(S, 0, 1))
    heap = bumps([(5.5, 14), (6, 9.5), (9.5, 6.5), (14, 6.5), (17.5, 9.5), (18.5, 14)], r=2.9) + "Z"
    return [shell(basket), shell(behind(heap, [basket], None)), detail(seg(7.5, 17.3, 16.5, 17.3)), detail(arc(12, 10.5, 2.2, 200, 340))]


@icon("papadum", CAT, "A large thin round lentil wafer with blistered bubbles across its surface",
      tags=["papad", "poppadom", "pappadam", "lentil crisp", "indian", "crispy"],
      aliases=["poppadom", "papad"])
def _(S):
    rim = poly(star_ring(12, 12, 9.4, 8.6, 20), closed=True) if S.name == "line" else circle(12, 12, 9)
    return [shell(rim), detail(circle(9, 10, 1.9)), detail(circle(15.2, 13.5, 2.2)), dot(10.5, 16, 0.9), dot(14.5, 7.5, 0.9)]


@icon("curry", CAT, "A two-handled bowl of curry seen from above the rim, with meat chunks in thick sauce",
      tags=["curry sauce", "stew", "gravy", "indian", "karahi", "meat curry"])
def _(S):
    b = ("M3.5 9.5A8.5 3.2 0 0 1 20.5 9.5C20.5 16.5 16.5 20.5 12 20.5C7.5 20.5 3.5 16.5 3.5 9.5Z")
    return [shell(b), detail("M3.5 9.5A8.5 3.2 0 0 0 20.5 9.5"), line(seg(1.8, 11.5, 3.6, 11.5)), line(seg(20.4, 11.5, 22.2, 11.5)),
            blob(8.2, 8.2, 2.2, 2.2, L(S, 0, 0.6)), blob(13.4, 7.7, 2.2, 2.2, L(S, 0, 0.6))]


@icon("falafel", CAT, "Three fried chickpea balls, one halved to show its green centre",
      tags=["chickpea fritter", "middle eastern", "vegan", "pita", "street food", "fried balls"])
def _(S):
    c = crumb(S, 12, 8, 4.8)
    a = crumb(S, 7.3, 15.8, 4.2)
    b = crumb(S, 16.7, 15.8, 4.2)
    return [shell(c), shell(behind(a, [c], 1.0)), shell(behind(b, [c], 1.0)), detail(circle(12, 8, 1.3)),
            dot(6, 16.6, 0.8), dot(8.6, 15, 0.8), dot(16, 17, 0.8), dot(18, 14.8, 0.8)]


@icon("hummus", CAT, "A bowl of chickpea dip with a swirled groove and whole chickpeas on top",
      tags=["chickpea dip", "tahini", "middle eastern", "mezze", "dip", "vegan"])
def _(S):
    b, r = bowl34(S)
    return [b, r, detail("M6.5 8.4Q9.3 6.4 12 8.4T17.5 8.4"), dot(8.3, 10.6, 0.9), dot(15.6, 10.6, 0.9)]


@icon("doner-kebab", CAT, "A pita pocket stuffed with shaved meat and salad shreds, wrapped in paper at the base",
      tags=["shawarma", "kebab", "pita", "turkish", "street food", "sandwich"])
def _(S):
    pita = ("M3.5 11.5H20.5C20.5 18 16.5 21 12 21C7.5 21 3.5 18 3.5 11.5Z" if S.name == "line" else
            "M5 11.5H19A1.5 1.5 0 0 1 20.5 13C20.1 18.4 16.3 21 12 21C7.7 21 3.9 18.4 3.5 13A1.5 1.5 0 0 1 5 11.5Z")
    fill = bumps([(5.5, 11.5), (6.3, 8.3), (9.5, 6.3), (13.5, 6.3), (16.8, 8), (18.5, 11.5)], r=2.8) + "Z"
    return [shell(pita), shell(fill), detail(poly([(3.8, 15.6), (9, 14), (14.5, 16.4), (20.2, 14.8)], r=L(S, 0, 0.5)))]


@icon("kibbeh", CAT, "A football-shaped fried croquette with pointed ends and a ridged crust",
      tags=["kubbeh", "kibbe", "lebanese", "bulgur", "croquette", "meat snack"],
      aliases=["kubbeh"])
def _(S):
    body = "M2.5 12Q12 3 21.5 12Q12 21 2.5 12Z" if S.name == "line" else "M3.3 12C3.3 7.5 7.5 5.5 12 5.5C16.5 5.5 20.7 7.5 20.7 12C20.7 16.5 16.5 18.5 12 18.5C7.5 18.5 3.3 16.5 3.3 12Z"
    return [shell(xf(body, -25)), detail(xf(seg(8, 10.5, 9.5, 14), -25)), detail(xf(seg(12, 9, 12, 15), -25)),
            detail(xf(seg(16, 10.5, 14.5, 14), -25))]


@icon("dolma", CAT, "Three small rolled grape leaf parcels stacked in a pyramid",
      tags=["sarma", "stuffed grape leaves", "vine leaves", "mezze", "turkish", "greek"])
def _(S):
    a = rect(2.5, 13.5, 9.5, 7.5, L(S, 3, 3.75))
    b = rect(12, 13.5, 9.5, 7.5, L(S, 3, 3.75))
    c = rect(7.25, 5.5, 9.5, 7.5, L(S, 3, 3.75))
    vein = lambda x, y: seg(x + 2.5, y + 5.5, x + 7, y + 2)
    return [shell(a), shell(b), shell(behind(c, [a, b], 1.0)), detail(vein(2.5, 13.5)), detail(vein(12, 13.5)), detail(vein(7.25, 5.5))]




@icon("couscous", CAT, "A bowl heaped with fine grain and topped with vegetable chunks",
      tags=["semolina", "north african", "moroccan", "grain", "tagine side", "vegetables"])
def _(S):
    heap = dome(4.5, 19.5, 12.5, 6.5)
    return [shell(bowl(S, 12.5)), shell(behind(heap, [bowl(S, 12.5)], None)), blob(8, 8.6, 2.6, 2.6, L(S, 0, 0.8)),
            blob(13.2, 7.6, 2.6, 2.6, L(S, 0, 0.8)), dot(11.3, 10.6, 0.7), dot(16.2, 10.6, 0.7), dot(6.8, 11.2, 0.7)]


@icon("injera", CAT, "A large round spongy flatbread topped with small mounds of stew in a circle",
      tags=["ethiopian", "eritrean", "flatbread", "teff", "sourdough", "wot"],
      aliases=["enjera"])
def _(S):
    ring = [dot(*pt_on(12, 12, 6.3, -90 + i * 60), 1.4) for i in range(6)]
    rim = poly(star_ring(12, 12, 9.8, 9, 24), closed=True) if S.name == "line" else circle(12, 12, 9.5)
    return [shell(rim), detail(circle(12, 12, 2.3)), *ring]


@icon("fufu", CAT, "A smooth round dough ball beside a bowl of soup",
      tags=["west african", "swallow", "cassava", "plantain", "soup", "dough ball"],
      aliases=["foufou"])
def _(S):
    b = ("M14 12H22C22 17.6 19.6 21 18 21C16.4 21 14 17.6 14 12Z" if S.name == "line" else
         "M15.3 12H20.7A1.3 1.3 0 0 1 22 13.3C21.6 18 19.6 21 18 21C16.4 21 14.4 18 14 13.3A1.3 1.3 0 0 1 15.3 12Z")
    return [shell(circle(7, 14.8, 5)), shell(b), line("M18 9.4C17.2 8.2 18.8 7.4 18 6.2")]


@icon("bunny-chow", CAT, "A hollowed quarter loaf of bread heaped with curry",
      tags=["south african", "durban", "bread bowl", "curry", "street food", "loaf"])
def _(S):
    bread = rect(3.5, 12.5, 17, 8.5, L(S, 2, 4))
    return [shell(bread), shell(behind(dome(5.5, 18.5, 12.5, 6.5), [bread], None)), dot(9.3, 9.6, 1), dot(13.5, 8.6, 1), dot(15.2, 11, 0.9)]


@icon("beef-jerky", CAT, "Three flat strips of dried meat with torn, uneven edges",
      tags=["dried meat", "biltong", "cured beef", "snack", "jerk", "protein"],
      aliases=["biltong"])
def _(S):
    r = L(S, 0, 0.7)

    def strip(y0, jag, x0=2.5):
        return poly([(x0, y0), (17.5 + jag, y0), (19.4 + jag, y0 + 1.3), (17.6 + jag, y0 + 2.6), (19.6 + jag, y0 + 4), (x0, y0 + 4)], closed=True, r=r)
    return [shell(strip(3.2, 0.5)), shell(strip(10, 0.8, 3.5)), shell(strip(16.8, 0, 2.5))]


# =========================================================================== salads and bowls


@icon("jollof-rice", CAT, "A plate with a mound of tomato rice and fried plantain slices",
      tags=["west african", "nigerian", "ghanaian", "party rice", "tomato rice", "plantain"])
def _(S):
    return [on_plate(S, dome(3, 14, 19, 8.5)), sqr(6.6, 14.2, 1.8, 20), sqr(9.6, 12.5, 1.8, -15), sqr(9.2, 16, 1.8, 10),
            shell(oval(17.6, 15.6, 3.3, 2.2, -20)), shell(behind(oval(18.4, 11.4, 3, 2), [oval(17.6, 15.6, 3.3, 2.2, -20)], 1.0))]


@icon("caesar-salad", CAT, "A bowl of torn romaine leaves with square croutons on top",
      tags=["romaine", "croutons", "parmesan", "lettuce", "starter", "green salad"])
def _(S):
    heap = bumps([(4.5, 12.5), (5.3, 8.6), (8.6, 6), (12, 7), (15.6, 5.5), (18.8, 8.4), (19.5, 12.5)], r=2.7) + "Z"
    return [shell(bowl(S, 12.5)), shell(behind(heap, [bowl(S, 12.5)], None)), sqr(9.5, 10, 2.2, 15), sqr(14.6, 9.4, 2.2, -12)]


@icon("greek-salad", CAT, "A bowl from above with tomato wedges, cucumber slices, olives and a slab of feta",
      tags=["horiatiki", "feta", "olives", "tomato", "cucumber", "mediterranean"],
      aliases=["horiatiki"])
def _(S):
    return [shell(circle(12, 12, 9.5)), sqr(8.6, 8.6, 4, 15, L(S, 0, 0.6)), tri_dot([(13.6, 6.6), (18.6, 8.2), (15.2, 12.4)], L(S, 0, 0.8)),
            Part("dot", circle(8.4, 15.8, 2.3)), dot(14.8, 16.2, 1.3), dot(18, 13.4, 1.0)]


@icon("coleslaw", CAT, "A small paper cup heaped with shredded cabbage and a fork standing in it",
      tags=["cabbage salad", "slaw", "side dish", "bbq", "takeaway", "shredded cabbage"],
      aliases=["slaw"])
def _(S):
    cup = poly([(5.5, 12), (18.5, 12), (16.5, 21), (7.5, 21)], closed=True, r=L(S, 0, 1))
    heap = bumps([(6, 12), (6.6, 8.6), (9.5, 6.6), (13.5, 6.6), (16.5, 8.6), (18, 12)], r=2.9) + "Z"
    return [shell(cup), shell(behind(heap, [cup], None)), detail(wave_d(8.2, 15.8, 9.6, 0.7, 3.8)), line(seg(14.5, 8, 20.5, 2.5))]


@icon("fruit-salad", CAT, "A bowl filled with mixed cut fruit pieces: a cube, a grape and a strawberry half",
      tags=["mixed fruit", "fruit bowl", "dessert", "healthy", "melon", "grapes"])
def _(S):
    b = bowl(S, 12.5)
    return [shell(b), shell(rotd(rect(4.6, 6.2, 4.6, 4.6, L(S, 0, 1)), 18, 6.9, 8.5)), shell(circle(13, 8.6, 2.5)),
            shell(poly([(16, 6), (21, 6), (18.5, 10.6)], closed=True, r=L(S, 0, 1)))]


@icon("cobb-salad", CAT, "A rectangular dish from above with salad toppings laid in neat parallel rows",
      tags=["chopped salad", "american", "bacon", "egg", "avocado", "rows"])
def _(S):
    return [shell(rect(2.5, 5, 19, 14, L(S, 2, 4))), detail(seg(8.8, 6, 8.8, 18)), detail(seg(15.2, 6, 15.2, 18)),
            dot(5.7, 9.5, 1), dot(5.7, 14.5, 1), sqr(12, 9.4, 2.2), sqr(12, 14.6, 2.2), dot(18.4, 9.5, 1), dot(18.4, 14.5, 1)]


@icon("poke-bowl", CAT, "A bowl from above with cubed raw fish, fanned avocado and sesame seeds over rice",
      tags=["hawaiian", "sushi bowl", "raw fish", "tuna", "avocado", "sesame"],
      aliases=["poke"])
def _(S):
    return [shell(circle(12, 12, 9.5)), sqr(7.8, 8.2, 3.6, 12, L(S, 0, 1.2)), sqr(12, 6.6, 3.6, -10, L(S, 0, 1.2)),
            Part("dot", lune(14.5, 10.5, 18.6, 17.2, 2.4, 0.2)), Part("dot", lune(11.6, 11.8, 14.6, 18, 2.2, 0.2)),
            dot(6.4, 13.8, 0.8), dot(8, 17, 0.8), dot(10.5, 14.8, 0.8)]


@icon("taco-salad", CAT, "A fluted crisp tortilla bowl filled with lettuce, tomato cubes and a dollop of sour cream",
      tags=["tortilla bowl", "mexican", "tex-mex", "lettuce", "sour cream", "fried shell"])
def _(S):
    zz = zigzag(3.5, 20.5, 12, -1.4, 6)
    body = poly(zz) + "C20.5 17 17 21 12 21C7 21 3.5 17 3.5 12Z"
    heap = bumps([(5.5, 11), (6, 7.6), (9, 5.6), (13, 5.6), (16.6, 7.6), (18.5, 11)], r=2.9) + "Z"
    return [shell(body), shell(behind(heap, [body], None)), sqr(10, 8.6, 2, 20), sqr(14.6, 8.2, 2, -15), dot(12, 3.6, 1.3)]


@icon("salad-jar", CAT, "A tall jar with clearly stacked horizontal salad layers and leafy greens on top",
      tags=["mason jar", "meal prep", "layered salad", "lunch", "healthy", "takeaway"],
      aliases=["mason-jar-salad"])
def _(S):
    jar = ("M6.5 8H17.5V9.5C18.8 10 19.5 11 19.5 12.5V19C19.5 20.2 18.7 21 17.5 21H6.5C5.3 21 4.5 20.2 4.5 19V12.5C4.5 11 5.2 10 6.5 9.5Z"
           if S.name == "line" else
           "M7 8H17V9.3C18.8 9.8 19.5 11 19.5 12.5V17.5C19.5 19.5 18 21 16 21H8C6 21 4.5 19.5 4.5 17.5V12.5C4.5 11 5.2 9.8 7 9.3Z")
    leaves = bumps([(6.5, 8), (6.8, 5.6), (9.4, 3.6), (12.6, 4.6), (15.4, 3.4), (17.2, 5.6), (17.5, 8)], r=2.6) + "Z"
    return [shell(union(jar, leaves)), detail(seg(5.5, 13, 18.5, 13)), detail(seg(5.5, 17, 18.5, 17))]


@icon("wedge-salad", CAT, "A wedge of iceberg lettuce drizzled with dressing and sprinkled with bacon bits",
      tags=["iceberg", "blue cheese", "steakhouse", "lettuce wedge", "dressing", "bacon bits"])
def _(S):
    tri = poly([(12, 21), (3.5, 9), (20.5, 9)], closed=True, r=L(S, 0, 1.4))
    cap = bumps([(3.5, 9), (5.3, 5.6), (9.4, 4), (14.6, 4), (18.7, 5.6), (20.5, 9)], r=3.6) + "Z"
    return [shell(union(tri, cap)), detail(poly([(6.5, 10), (9.2, 12.6), (12, 10), (14.8, 12.6), (17.5, 10)], r=L(S, 0, 0.6))),
            dot(9.6, 7, 0.8), dot(14, 6.6, 0.8), dot(12, 15.4, 0.8)]


@icon("potato-salad", CAT, "A bowl from above with potato cubes in dressing, an egg slice and herb specks",
      tags=["picnic", "bbq side", "mayonnaise", "egg", "german", "american"])
def _(S):
    return [shell(circle(12, 12, 9.5)), sqr(8.2, 8.4, 3.4, 15, L(S, 0, 0.8)), sqr(13.6, 7.2, 3.4, -12, L(S, 0, 0.8)),
            sqr(7.6, 14.6, 3.4, -8, L(S, 0, 0.8)), sqr(12.3, 12.6, 3, 25, L(S, 0, 0.7)),
            detail(circle(16.2, 15.6, 2.6)), dot(16.2, 15.6, 0.9), dot(17.8, 9.6, 0.7)]


@icon("seaweed-salad", CAT, "A small bowl piled with thin wavy seaweed strands and sesame seeds",
      tags=["wakame", "japanese", "sushi side", "sea vegetable", "sesame", "goma wakame"],
      aliases=["wakame-salad"])
def _(S):
    return [shell(bowl(S, 13)), line(wave_d(5.5, 18.5, 10.4, 1.1, 4.3)), line(wave_d(6.5, 17.5, 7, 1.1, 3.6)), dot(8.8, 4.2, 0.8),
            dot(14.6, 4.6, 0.8), dot(17.4, 7.6, 0.8)]


@icon("papaya-salad", CAT, "A clay mortar with a wooden pestle holding shredded papaya, a tomato and a chili",
      tags=["som tam", "thai salad", "green papaya", "mortar and pestle", "spicy", "thailand"],
      aliases=["som-tam"])
def _(S):
    mortar = ("M4 12.5H20C20 17.8 16.6 20.5 12 20.5C7.4 20.5 4 17.8 4 12.5Z" if S.name == "line" else
              "M5.5 12.5H18.5A1.5 1.5 0 0 1 20 14C19.6 18.2 16.4 20.5 12 20.5C7.6 20.5 4.4 18.2 4 14A1.5 1.5 0 0 1 5.5 12.5Z")
    return [shell(mortar), shell(bar(10, 12.5, 19.5, 2.5, 3, L(S, 0, 1.2))),
            line(wave_d(5.5, 11, 9.6, 0.9, 3.4)), dot(6.4, 6.6, 1.4)]


@icon("tabbouleh", CAT, "A shallow bowl of finely chopped herbs with tomato cubes and a lemon wedge",
      tags=["tabouli", "parsley salad", "bulgur", "lebanese", "mezze", "herbs"],
      aliases=["tabouli"])
def _(S):
    specks = [(7.2, 7), (10.4, 6.2), (13.6, 7.6), (9, 9.8), (15.6, 10.6), (6.4, 12.2), (11.6, 12.2), (8.6, 15.4), (13, 15.6)]
    return [shell(circle(12, 12, 9.5)), *[dot(x, y, 0.75) for x, y in specks], sqr(16, 15, 3, 18, L(S, 0, 0.6))]


@icon("grain-bowl", CAT, "A bowl from above divided into sections of grains, greens, chickpeas and an egg half",
      tags=["buddha bowl", "power bowl", "healthy", "quinoa", "vegetarian", "meal prep"],
      aliases=["buddha-bowl"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(seg(12, 3, 12, 21)), detail(seg(12, 12, 21, 12)), dot(7.2, 8, 1), dot(8.6, 12.4, 1),
            dot(6.6, 15.6, 1), dot(9.4, 17, 1), detail(circle(16.5, 7.4, 2)),
            detail(poly([(14.2, 14.6), (18.8, 14.6), (16.5, 19)], closed=True, r=L(S, 0, 1.4)))]


@icon("bread-bowl-soup", CAT, "A round crusty loaf hollowed out and filled with creamy soup, steam above",
      tags=["sourdough bowl", "chowder", "clam chowder", "soup", "bread", "lunch"])
def _(S):
    loaf = ("M3.5 21V15C3.5 10.5 7 8 12 8C17 8 20.5 10.5 20.5 15V21Z" if S.name == "line" else
            "M3.5 19V15C3.5 10.5 7 8 12 8C17 8 20.5 10.5 20.5 15V19C20.5 20.2 19.7 21 18.5 21H5.5C4.3 21 3.5 20.2 3.5 19Z")
    return [shell(loaf), detail(oval(12, 12.6, 5.4, 2.2)), line("M9.5 5.6C8.7 4.6 10.3 3.6 9.5 2.6"), line("M14.5 5.6C13.7 4.6 15.3 3.6 14.5 2.6")]


@icon("matzo-ball-soup", CAT, "A bowl of clear broth with one large round dumpling, carrot rounds and a dill sprig",
      tags=["jewish", "chicken soup", "matzah ball", "kneidlach", "broth", "passover"],
      aliases=["matzah-ball-soup"])
def _(S):
    b = bowl(S, 13)
    ball = circle(11.5, 9.5, 4.4)
    return [shell(behind(ball, [b], None)), shell(b), dot(6.6, 16, 1), dot(17.4, 17, 1), line(seg(17, 11, 20.5, 4.5)), line(seg(18.8, 7.8, 21, 8))]


@icon("borscht", CAT, "A bowl of beet soup with a swirl of sour cream in the middle and a sprig of dill",
      tags=["beet soup", "beetroot", "russian", "ukrainian", "sour cream", "eastern european"],
      aliases=["borsch"])
def _(S):
    b, r = bowl34(S)
    return [b, r, detail(oval(12, 8.8, 3.2, 1.1)), dot(12, 8.8, 0.9), line(seg(18.6, 7, 21.2, 2.6)), line(seg(19.8, 4.6, 22, 5))]


@icon("gazpacho", CAT, "A short glass of chilled tomato soup with a cucumber stick and a crouton on the rim",
      tags=["cold soup", "spanish", "chilled", "tomato soup", "summer", "andalusian"])
def _(S):
    glass = poly([(5.5, 8), (18.5, 8), (16.5, 21), (7.5, 21)], closed=True, r=L(S, 0, 1.2))
    return [shell(glass), detail(wave_d(6.4, 17.6, 12.6, 0.9, 5.6)), line(seg(14, 12, 19.5, 2.8)),
            shell(rotd(rect(3, 4.4, 4.4, 3.4, L(S, 0, 0.8)), -15, 5.2, 6.1))]


@icon("chili-con-carne", CAT, "A bowl of chili with kidney beans, a sour cream dollop and a tortilla chip stuck in",
      tags=["chilli", "texas chili", "bean stew", "beef and beans", "tex-mex", "spicy"],
      aliases=["chilli-con-carne"])
def _(S):
    b, r = bowl34(S)
    chip = poly([(14, 8.4), (16.4, 2.6), (20.8, 7.4)], closed=True, r=L(S, 0, 1))
    return [shell(behind(chip, [bowl34(S)[0].d], 1.0)), b, r, ovdot(7.6, 9.6, 1.6, 1, 20), ovdot(10.6, 8.2, 1.6, 1, -25),
            dot(13.6, 10.8, 1.2)]


@icon("dal", CAT, "A small bowl of lentil soup with a spiral of tempered oil and a curry leaf",
      tags=["dhal", "lentils", "indian", "soup", "tadka", "vegetarian"],
      aliases=["dhal"])
def _(S):
    b, r = bowl34(S)
    return [b, r, detail(poly(spiral_pts(12, 8.6, 0.5, 2.5, 1.3, start=180, n=16))), dot(7.6, 9, 0.8), dot(16.4, 9, 0.8),
            shell(leaf(15.6, 6.2, 20.6, 1.8, 1.3))]


# =========================================================================== East Asia, Gulf and Levant


@icon("loco-moco", CAT, "A mound of rice topped with a beef patty and a fried egg, gravy over the top",
      tags=["hawaiian", "rice bowl", "hamburger patty", "fried egg", "gravy", "comfort food"])
def _(S):
    patty = rect(6, 10, 12, 4, L(S, 1.5, 2))
    return [on_plate(S, dome(3.5, 20.5, 19, 8)), shell(patty), shell(oval(12, 6.8, 4.2, 2.6)), dot(12, 6.8, 1)]


@icon("char-siu", CAT, "A strip of glazed barbecue pork with a dark glazed edge, sliced at one end",
      tags=["cantonese", "bbq pork", "chinese roast pork", "honey glazed", "siu mei", "cha siu"],
      aliases=["cha-siu"])
def _(S):
    slab = rect(2.5, 5.5, 14, 8, L(S, 2, 4))
    return [shell(xf(slab, -15, 9.5, 9.5)), detail(xf(seg(5.5, 8.8, 13.5, 8.8), -15, 9.5, 9.5)),
            shell(oval(17, 16.4, 3.8, 2.4, -15)), shell(behind(oval(9.6, 18.6, 3.8, 2.4, -15), [oval(17, 16.4, 3.8, 2.4, -15)], 1.0))]


@icon("mapo-tofu", CAT, "A shallow bowl of soft tofu cubes in chili sauce with peppercorns and scallion rings",
      tags=["sichuan", "szechuan", "spicy tofu", "chinese", "chili oil", "bean curd"])
def _(S):
    b, r = bowl34(S)
    return [b, r, sqr(7.6, 8.6, 2.8, 15, L(S, 0, 0.6)), sqr(12, 7.6, 2.8, -15, L(S, 0, 0.6)), sqr(16.4, 8.8, 2.8, 10, L(S, 0, 0.6)),
            dot(9.8, 10.8, 0.6), dot(14.4, 11, 0.6), dot(11.8, 9.8, 0.5)]
@icon("sushi-boat", CAT, "A wooden boat-shaped platter carrying sushi pieces along its deck",
      tags=["sushi platter", "sushi bar", "japanese", "sashimi", "party platter", "nigiri"],
      aliases=["sushi-platter"])
def _(S):
    hull = poly([(2.5, 13), (5.5, 15.5), (18.5, 15.5), (21.5, 13), (18.5, 20.5), (5.5, 20.5)], closed=True, r=L(S, 0, 1.4))
    return [shell(hull), blob(5.2, 9.2, 4.2, 4, L(S, 0, 1)), blob(9.9, 9.2, 4.2, 4, L(S, 0, 1)), blob(14.6, 9.2, 4.2, 4, L(S, 0, 1))]


@icon("natto", CAT, "A small bowl of fermented soybeans with chopsticks lifting a few beans",
      tags=["japanese", "fermented soybeans", "breakfast", "sticky", "chopsticks", "soy"])
def _(S):
    return [shell(bowl(S, 13.5)), ovdot(7.8, 11.4, 1.6, 1.1, 20), ovdot(11.4, 10.8, 1.6, 1.1, -20), ovdot(15.2, 11.6, 1.6, 1.1, 15),
            line(seg(10, 9.4, 19, 2)), line(seg(13, 9.4, 21.5, 3.2))]


@icon("kabsa", CAT, "A wide platter of spiced rice topped with a whole roast chicken and scattered nuts",
      tags=["saudi", "gulf", "arabian rice", "mandi", "machboos", "roast chicken"])
def _(S):
    return [on_plate(S, dome(3.5, 20.5, 19, 6.5)), shell(oval(12, 10.2, 5.8, 3.6, -8)), ovdot(5.8, 15.4, 0.9, 0.6, 30),
            ovdot(18.2, 15.4, 0.9, 0.6, -30), ovdot(8.4, 16.4, 0.9, 0.6, 10)]


@icon("maqluba", CAT, "A tall dome of layered rice and vegetables turned out onto a tray",
      tags=["upside down", "palestinian", "jordanian", "layered rice", "eggplant", "levant"],
      aliases=["makloubeh"])
def _(S):
    return [on_plate(S, dome(4.5, 19.5, 19, 13)), detail(seg(5, 12.6, 19, 12.6)), detail(seg(4.6, 16.2, 19.4, 16.2))]


@icon("grilled-halloumi", CAT, "Two thick slabs of cheese with dark diagonal grill marks",
      tags=["cypriot", "grilling cheese", "bbq", "squeaky cheese", "vegetarian", "mediterranean"])
def _(S):
    return [shell(rect(2.5, 3.5, 14.5, 7.3, L(S, 1.5, 3))), shell(rect(7, 13.2, 14.5, 7.3, L(S, 1.5, 3))),
            detail(seg(6.5, 9, 9.3, 5.3)), detail(seg(10.7, 9, 13.5, 5.3)),
            detail(seg(11, 18.7, 13.8, 15)), detail(seg(15.2, 18.7, 18, 15))]


@icon("caviar", CAT, "A small round tin of tiny roe beads",
      tags=["fish roe", "sturgeon", "luxury", "delicacy", "beluga", "appetizer"])
def _(S):
    d = L(S, 4.6, 6)
    tin = f"M3 11A9 3.6 0 0 1 21 11V{fmt(11 + d)}A9 3.6 0 0 1 3 {fmt(11 + d)}Z"
    return [shell(tin), detail("M3 11A9 3.6 0 0 0 21 11"), dot(8, 9.6, 0.85), dot(11, 8.6, 0.85), dot(14, 9.8, 0.85), dot(17, 9.2, 0.85),
            dot(12, 11.2, 0.6)]


@icon("chicken-kiev", CAT, "A breaded chicken cutlet on a bone, cut open with herb butter spilling out",
      tags=["ukrainian", "russian", "garlic butter", "breaded chicken", "fried", "stuffed chicken"])
def _(S):
    body = oval(9.6, 13.8, 7, 5.3, -38)
    return [shell(body), detail("M8.4 9.8L10.2 14"), Part("dot", oval(9.6, 17, 2.6, 1, -38)),
            line(seg(14.4, 10.2, 18.6, 6)), dot(19.6, 4.8, 1.2), dot(20.2, 7.4, 1.2)]


@icon("garlic-bread", CAT, "A sliced baguette with herb and garlic butter on top",
      tags=["baguette", "garlic butter", "italian side", "toasted", "bread", "parsley"])
def _(S):
    loaf = rect(3.5, 7.5, 17, 9, 2.2) if S.name == "line" else capsule(7, 12, 17, 12, 8.4)
    cuts = [xf(seg(x, 7.5, x, 16.5), -20) for x in (8.5, 12, 15.5)]
    return [shell(xf(loaf, -20)), *[detail(c) for c in cuts], dot(10.2, 9.8, 0.8), dot(13.8, 8.6, 0.8)]


@icon("steak-tartare", CAT, "A round mound of chopped raw beef with an egg yolk in half a shell on top",
      tags=["raw beef", "french", "bistro", "tartar", "egg yolk", "starter"],
      aliases=["beef-tartare"])
def _(S):
    shell_d = "M8.6 7.4H15.4C15.4 10.6 13.8 12 12 12C10.2 12 8.6 10.6 8.6 7.4Z"
    return [on_plate(S, dome(4, 20, 19, 8.5)), shell(shell_d), dot(12, 6.2, 1.7)]


# =========================================================================== classic plates


@icon("terrine", CAT, "A rectangular slice of terrine showing a cracked mosaic of layered pieces",
      tags=["pate", "french", "charcuterie", "pressed meat", "deli", "cold cut"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, L(S, 2, 4))), detail(poly([(2.5, 10), (8, 8.6), (12, 12), (17, 9), (21.5, 11)], r=L(S, 0, 0.5))),
            detail(seg(12, 12, 10, 19.5)), detail(seg(17, 9, 17.6, 4.5)), detail(seg(14.6, 15.6, 21.5, 15.2))]


@icon("potato-gratin", CAT, "A baking dish of overlapping thin potato slices in rows with a browned bubbly top",
      tags=["dauphinoise", "scalloped potatoes", "french", "baked", "cheese", "side dish"],
      aliases=["gratin-dauphinois"])
def _(S):
    return [shell(rect(3.5, 5, 17, 14, L(S, 2, 4))), line(seg(1.5, 12, 3.6, 12)), line(seg(20.4, 12, 22.5, 12)),
            detail(wave_d(6.4, 17.6, 9.4, 1, 3.7)), detail(wave_d(6.4, 17.6, 14.6, 1, 3.7)), dot(9, 12, 0.8), dot(15, 12, 0.8)]


@icon("meatballs", CAT, "A small bowl of round meatballs in sauce with a toothpick in one",
      tags=["albondigas", "kottbullar", "polpette", "swedish", "sauce", "party food"],
      aliases=["polpette"])
def _(S):
    b = bowl(S, 13)
    top = circle(12, 7.6, 3.3)
    left = behind(circle(6.8, 10.6, 3.3), [top], 1.0)
    right = behind(circle(17.2, 10.6, 3.3), [top], 1.0)
    return [shell(top), shell(behind(left, [b], None)), shell(behind(right, [b], None)), shell(b), line(seg(12, 5.4, 18.4, 0.8))]
@icon("chicken-and-waffles", CAT, "A square waffle with a fried chicken drumstick on top",
      tags=["southern", "soul food", "brunch", "syrup", "fried chicken", "american"])
def _(S):
    return [shell(rect(3.5, 12.5, 17, 8.5, L(S, 1.5, 3))), detail(seg(9.2, 12.5, 9.2, 21)), detail(seg(14.8, 12.5, 14.8, 21)),
            detail(seg(3.5, 16.8, 20.5, 16.8)), shell(oval(9.6, 7.6, 4.8, 3.1, -28)), line(seg(13.4, 5.8, 18.6, 3.2)), dot(19.4, 2.9, 1.3)]


@icon("casserole", CAT, "An oval baking dish seen from above with a browned crusty top and bubbling edges",
      tags=["baked dish", "hotdish", "bake", "pie dish", "comfort food", "potluck"])
def _(S):
    return [shell(oval(12, 12, 8.4, 6.6)), line(seg(1.8, 12, 3.6, 12)), line(seg(20.4, 12, 22.2, 12)),
            detail(oval(12, 12, 5, 3.2)), dot(9.6, 11.6, 0.7), dot(14, 12.6, 0.7), dot(12.4, 10.6, 0.6)]


@icon("al-pastor", CAT, "A vertical meat spit stacked in layers and crowned with a pineapple",
      tags=["trompo", "tacos al pastor", "mexican", "shawarma", "spit", "pineapple"],
      aliases=["trompo"])
def _(S):
    spit = poly([(7, 9), (17, 9), (15.4, 19), (8.6, 19)], closed=True, r=L(S, 0, 1.2))
    return [shell(spit), detail(seg(7.6, 12.4, 16.4, 12.4)), detail(seg(8.2, 15.8, 15.8, 15.8)), line(seg(12, 19, 12, 22.2)),
            shell(oval(12, 6.3, 3.4, 2.4)), line(poly([(10, 4.1), (10.6, 2.6), (12, 3.6), (13.4, 2.6), (14, 4.1)], r=0))]


@icon("pastilla", CAT, "A round flaky pie dusted with sugar and decorated with a crisscross lattice",
      tags=["bastilla", "moroccan", "pigeon pie", "phyllo", "cinnamon", "savory pie"],
      aliases=["bastilla"])
def _(S):
    cs = [chord(12, 12, 8.4, 45, o) for o in (-3, 3)] + [chord(12, 12, 8.4, -45, o) for o in (-3, 3)]
    rim = poly(star_ring(12, 12, 9.5, 8.7, 16), closed=True) if S.name == "line" else circle(12, 12, 9.2)
    return [shell(rim), *[detail(c) for c in cs]]


@icon("roasted-chestnuts", CAT, "A paper cone full of hot roasted chestnuts with steam rising",
      tags=["street food", "winter", "christmas", "marron", "nuts", "market"])
def _(S):
    cone = poly([(5, 13), (19, 13), (12, 22), ], closed=True, r=L(S, 0, 1.4))
    nuts = [chestnut(8.4, 9.6, 1.6), chestnut(12.6, 8.4, 1.6), chestnut(16.6, 9.8, 1.6)]
    return [shell(cone), *[shell(behind(n, [cone], 1.0)) for n in nuts], line("M9 4.2C8.2 3.2 9.8 2.4 9 1.4"), line("M14 4C13.2 3 14.8 2.2 14 1.2")]


@icon("squid-skewer", CAT, "A grilled squid on a stick with crosshatch scoring on the body and tentacles hanging below",
      tags=["grilled squid", "calamari", "street food", "bbq", "seafood", "korean"])
def _(S):
    hood = poly([(12, 2.5), (17, 8), (15.6, 13.2), (8.4, 13.2), (7, 8)], closed=True, r=L(S, 0, 1.2))
    return [shell(hood), detail(seg(9.2, 8.4, 13.8, 12.4)), detail(seg(14.8, 8.4, 10.2, 12.4)),
            line(poly([(9.4, 13.4), (8.6, 17), (6.8, 19.6)], r=L(S, 0, 1))), line(poly([(14.6, 13.4), (15.4, 17), (17.2, 19.6)], r=L(S, 0, 1))),
            line(seg(12, 13.4, 12, 22.5))]


@icon("orecchiette", CAT, "Three small ear-shaped pasta cups, each with a thumbprint dent",
      tags=["italian", "puglia", "little ears", "pasta", "apulian", "dried pasta"])
def _(S):
    def ear(cx, cy, deg):
        return [shell(oval(cx, cy, 4.3, 3.4, deg)), detail(xf(arc(cx, cy + 0.2, 1.2, 190, 350), 0))]
    return [*ear(6.6, 16, -15), *ear(17.4, 16, 15), *ear(12, 7.2, 0)]
