"""TypeIcon Core: world dishes (batch dishes_001).

Breakfast, Latin American, Spanish, Italian, French and Central European dishes, drawn from the food
itself. Side views sit on a shallow plate or in a round bowl; top views sit on a round plate (r 9).
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


AVOCADO = ("M12 3C9.3 3.6 8 5.8 7.4 8.8C7 10.8 4.5 12.6 4.5 15.8C4.5 19 7.5 21 12 21"
           "C16.5 21 19.5 19 19.5 15.8C19.5 12.6 17 10.8 16.6 8.8C16 5.8 14.7 3.6 12 3Z")
EGG = "M12 3C16 3 19 9.5 19 14C19 18.5 16 21 12 21C8 21 5 18.5 5 14C5 9.5 8 3 12 3Z"


# =========================================================================== eggs and breakfast

@icon("scrambled-eggs", CAT, "A heap of scrambled eggs on a plate with a chive on top",
      tags=["eggs", "breakfast", "brunch", "scramble", "plate"])
def _(S):
    mound = bumps([(4.5, 15.5), (6.8, 10.8), (11.2, 8.2), (15.6, 9.6), (19.5, 15.5)], r=3.2)
    mound += "Z" if S.name == "line" else "L18.5 15.5A1 1 0 0 1 17.5 16.5H6.5A1 1 0 0 1 5.5 15.5Z"
    return [shell(mound), plate(S), line(seg(14, 5.5, 17, 3))]


@icon("eggs-benedict", CAT, "A poached egg with sauce dripping over a muffin half",
      tags=["benedict", "poached egg", "hollandaise", "brunch", "breakfast"])
def _(S):
    dome = ("M4.5 13C4.5 8.5 7.8 5 12 5C16.2 5 19.5 8.5 19.5 13H18.5V14.5A1.25 1.25 0 0 1 16 14.5V13"
            "H10V15.5A1.25 1.25 0 0 1 7.5 15.5V13Z")
    muffin = rect(2.5, 17, 19, 4, L(S, 1.5, 2))
    return [shell(dome), shell(behind(muffin, [dome], 1.0))]


@icon("soft-boiled-egg", CAT, "A soft-boiled egg with its top cracked open in an egg cup",
      tags=["boiled egg", "egg cup", "breakfast", "runny", "dippy egg"])
def _(S):
    cup = ("M5.5 11H18.5C18.5 14.6 15.6 16.5 12 16.5C8.4 16.5 5.5 14.6 5.5 11Z" if S.name == "line" else
           "M6.5 11H17.5A1 1 0 0 1 18.5 12C18.2 14.9 15.4 16.5 12 16.5C8.6 16.5 5.8 14.9 5.5 12A1 1 0 0 1 6.5 11Z")
    top = poly([(7.2, 6.5), (9.4, 5), (12, 6.5), (14.6, 5), (16.8, 6.5)], r=L(S, 0, 0.6))
    egg = top + "C17.6 8 18 9.8 18 12L6 12C6 9.8 6.4 8 7.2 6.5Z"
    return [shell(cup), shell(behind(egg, [cup], None)), detail(seg(7, 11, 17, 11)),
            line(poly([(12, 16.5), (12, 20.5)])), line(seg(8, 20.5, 16, 20.5) if S.name == "line" else seg(8.5, 20.5, 15.5, 20.5))]


@icon("egg-in-a-hole", CAT, "A slice of toast with an egg fried in a hole cut in the middle",
      tags=["egg in a basket", "toad in the hole", "toast", "fried egg", "breakfast"])
def _(S):
    return [shell(toast(S)), detail(circle(12, 14, 3.5)), dot(12, 14, 1.5)]


DEV_A = rotd(ellipse(8.6, 14.6, 6.2, 4.3), -25, 8.6, 14.6)
DEV_B = rotd(ellipse(15.4, 9.4, 6.2, 4.3), -25, 15.4, 9.4)


@icon("deviled-eggs", CAT, "Two halved eggs seen from above, each filled with piped yolk",
      tags=["devilled eggs", "stuffed eggs", "party food", "appetizer", "egg halves"], aliases=["devilled-eggs"])
def _(S):
    fill = (lambda cx, cy: poly(star_ring(cx, cy, 2.9, 2.0, 6), closed=True) if S.name == "line"
            else scallop_ring(cx, cy, 2.4, 6, 1.2))
    return [shell(DEV_A), shell(behind(DEV_B, [DEV_A], 1.25)), detail(fill(8.6, 14.6)),
            detail(behind(fill(16.2, 8.8), [DEV_A], 1.25))]


def _spiral(cx, cy, r0, r1, turns, start=-90.0, n=22):
    pts = []
    for i in range(n + 1):
        t = i / n
        ang = start + 360 * turns * t
        pts.append(pt_on(cx, cy, r0 + (r1 - r0) * t, ang))
    return pts


@icon("tamagoyaki", CAT, "A block of rolled Japanese omelette with spiral layers on its cut end",
      tags=["japanese omelette", "rolled omelette", "egg roll", "sushi", "bento"])
def _(S):
    hull = poly([(2.5, 8.5), (9, 4), (21.5, 4), (21.5, 16), (15, 20.5), (2.5, 20.5)], closed=True, r=L(S, 0, 1))
    return [shell(hull), detail(poly([(2.5, 8.5), (15, 8.5), (15, 20.5)])), detail(seg(15, 8.5, 21.5, 4)),
            detail(poly(_spiral(8.75, 14.5, 0.4, 3.7, 1.3, start=180, n=26), r=0))]


@icon("tea-egg", CAT, "A peeled egg covered in a network of marbled cracks",
      tags=["marbled egg", "chinese tea egg", "soy egg", "snack", "boiled egg"])
def _(S):
    egg = EGG if S.name == "rounded" else "M12 3C15.6 4 19 9.5 19 14C19 18.5 16 21 12 21C8 21 5 18.5 5 14C5 9.5 8.4 4 12 3Z"
    return [shell(egg),
            detail(poly([(6.6, 10.5), (9.2, 12), (11.8, 9.8), (14.4, 11.8), (17.2, 10.2)], r=S.r * 0.5)),
            detail(poly([(5.6, 16), (8.4, 17.4), (10.6, 15.6), (13.6, 17.6), (18.2, 15.4)], r=S.r * 0.5)),
            detail(seg(10.6, 15.6, 9.2, 12)), detail(seg(14.4, 11.8, 13.6, 17.6))]


@icon("scotch-egg", CAT, "A breaded scotch egg cut in half showing the egg inside",
      tags=["picnic", "british", "sausage meat", "snack", "egg"])
def _(S):
    outer = (poly(star_ring(12, 12, 9.3, 8.3, 14), closed=True) if S.name == "line" else scallop_ring(12, 12, 8.5, 14, 1.15))
    white = scaled(EGG, 0.5, 6, 5.5)
    return [shell(outer), detail(white), dot(12, 13.3, 1.9)]


@icon("shakshuka", CAT, "A skillet of tomato sauce with two eggs and herbs",
      tags=["shakshouka", "eggs in sauce", "skillet", "brunch", "middle eastern"], aliases=["shakshouka"])
def _(S):
    handle = bar(17.3, 7.2, 21.3, 3.2, 3, L(S, 0, 1.2))
    pan = circle(11, 13, 8.5)
    return [shell(pan), shell(behind(handle, [pan], None)), detail(circle(8.1, 15.2, 2.6)), dot(8.1, 15.2, 1.05),
            detail(circle(13.9, 10.6, 2.6)), dot(13.9, 10.6, 1.05)]


@icon("breakfast-plate", CAT, "A plate with a fried egg and a strip of bacon",
      tags=["full breakfast", "fry up", "bacon and eggs", "brunch", "diner"])
def _(S):
    bacon = wave_d(12, 18.6, 15.2, 0.6, 3.3)
    return [shell(circle(12, 12, 9.5)), detail(circle(9.4, 10.2, 3.3)), dot(9.4, 10.2, 1.4),
            detail(xf(bacon, -45, 15.3, 15.2))]


@icon("oatmeal", CAT, "A bowl of porridge with berries and a spoon",
      tags=["porridge", "oats", "breakfast", "cereal", "hot cereal"], aliases=["porridge"])
def _(S):
    return [shell(bowl(S)), line("M4.5 10.5Q12 6.5 19.5 10.5"), dot(8.5, 5.9, 1.4), dot(12.3, 5.2, 1.4),
            line(seg(16, 8.2, 20, 3))]


@icon("cereal-bowl", CAT, "A bowl of ring-shaped cereal with a spoon",
      tags=["cereal", "breakfast", "cereal loops", "milk", "hoops"])
def _(S):
    return [shell(bowl(S)), line(circle(6.8, 7.2, 2)), line(circle(11.8, 6.4, 2)),
            line(seg(16, 9.5, 20, 3.5))]


def _jar(S):
    body = ("M8 8H16V8.5C18 9 19 10.3 19 12.5V19C19 20.2 18.2 21 17 21H7C5.8 21 5 20.2 5 19V12.5C5 10.3 6 9 8 8.5Z"
            if S.name == "line" else
            "M8 8H16V8.5C18 9 19 10.3 19 12.5V17.5C19 19.5 17.5 21 15.5 21H8.5C6.5 21 5 19.5 5 17.5V12.5C5 10.3 6 9 8 8.5Z")
    return body


@icon("granola", CAT, "A glass jar filled with chunky granola clusters",
      tags=["muesli", "oats", "breakfast", "cereal", "jar", "clusters"])
def _(S):
    chunks = [[(8, 12.5), (10.2, 11.8), (10.8, 13.8), (8.6, 14.8)], [(13.2, 12), (15.8, 12.6), (15.2, 14.8), (12.8, 14.4)],
              [(7.8, 17.2), (10, 16.6), (10.8, 18.6), (8.2, 19)], [(13, 17), (15.6, 16.8), (16.2, 18.8), (13.4, 19.2)]]
    return [shell(rect(7, 2.5, 10, 3.5, L(S, 1, 1.5))), shell(_jar(S)),
            *[Part("dot", poly(c, closed=True, r=L(S, 0, 0.4))) for c in chunks]]


@icon("avocado-toast", CAT, "A slice of toast topped with half an avocado",
      tags=["avo toast", "brunch", "breakfast", "avocado", "toast"])
def _(S):
    avo = scaled(AVOCADO, 0.5, 6, 5.2)
    return [shell(toast(S)), detail(avo), dot(12, 13.2, 1.4)]


@icon("hash-browns", CAT, "A flat potato patty with a crispy shredded surface",
      tags=["hash brown", "potato", "rosti", "breakfast", "fried"], aliases=["hash-brown"])
def _(S):
    ticks = [(8, 10), (12, 10), (16, 10), (10, 14), (14, 14)]
    return [shell(rect(3, 6, 18, 12, L(S, 4, 6))), *[detail(seg(x - 1.1, y + 1.1, x + 1.1, y - 1.1)) for x, y in ticks]]


@icon("congee", CAT, "A bowl of rice porridge with a fried dough stick resting in it",
      tags=["jook", "rice porridge", "youtiao", "chinese breakfast", "bowl"], aliases=["jook"])
def _(S):
    b = bowl(S)
    stick = capsule(6, 11.5, 20.5, 6, 3.6)
    return [shell(b), shell(behind(stick, [b], 1.0)), detail(behind(seg(6, 11.5, 20.5, 6), [b], 2.2)),
            line("M5.5 3C4.7 4.3 6.3 5.2 5.5 6.8"), line("M9.3 2.5C8.5 3.8 10.1 4.7 9.3 6.3")]


@icon("youtiao", CAT, "Two long fried dough sticks joined along their length",
      tags=["chinese doughnut", "fried dough", "cruller", "breakfast", "chinese"], aliases=["you-tiao"])
def _(S):
    a = capsule(3, 10, 21, 10, 4)
    b = capsule(3, 14, 21, 14, 4)
    return [shell(rotd(union(a, b), -40)), detail(xf(seg(5, 12, 19, 12), -40))]


@icon("beans-on-toast", CAT, "A slice of toast covered with baked beans",
      tags=["baked beans", "toast", "british breakfast", "comfort food", "beans"])
def _(S):
    beans = [(8.2, 8.6, -20), (12, 8.2, 15), (15.8, 8.6, -25), (10, 12.6, 20), (14, 12.6, -15),
             (8.2, 16.6, 25), (12, 16.8, -20), (15.8, 16.6, 15)]
    return [shell(toast(S)), *[Part("dot", rotd(ellipse(x, y, 1.5, 1.05), a, x, y)) for x, y, a in beans]]


@icon("empanada", CAT, "A half-moon pastry turnover with a crimped edge",
      tags=["turnover", "pasty", "pastry", "latin american", "hand pie"])
def _(S):
    cx, cy, R, n = 12, 15.5, 8.2, 7
    pts = [pt_on(cx, cy, R, 180 + i * 180 / n) for i in range(n + 1)]
    if S.name == "line":
        edge = poly([pts[0]] + [q for i in range(n) for q in (pt_on(cx, cy, R + 1.1, 180 + (i + 0.5) * 180 / n), pts[i + 1])])
    else:
        br = R * math.sin(math.radians(90 / n)) * 1.15
        edge = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}" + "".join(f"A{fmt(br)} {fmt(br)} 0 0 1 {fmt(x)} {fmt(y)}" for x, y in pts[1:])
    body = edge + f"Q{cx} {cy + 5} {fmt(pts[0][0])} {fmt(pts[0][1])}Z"
    inner = f"M{cx - 5} {cy}A5 5 0 0 1 {cx + 5} {cy}"
    return [shell(xf(body, -15, 12, 14)), detail(xf(inner, -15, 12, 14))]


@icon("burrito", CAT, "A rolled burrito half wrapped in foil",
      tags=["wrap", "mexican", "tortilla", "takeaway", "tex-mex"])
def _(S):
    body = ("M7 6A5 2.5 0 0 1 17 6V18.5A2.5 2.5 0 0 1 14.5 21H9.5A2.5 2.5 0 0 1 7 18.5Z" if S.name == "rounded" else
            "M7 6A5 2.5 0 0 1 17 6V19.5C17 20.3 16.3 21 15.5 21H8.5C7.7 21 7 20.3 7 19.5Z")
    foil = poly(zigzag(7, 17, 13.5, -1.2, 4), r=L(S, 0, 0.5))
    return [shell(xf(body, 35)), detail(xf("M7 6A5 2.5 0 0 0 17 6", 35)), detail(xf(foil, 35))]


@icon("quesadilla", CAT, "A wedge of grilled quesadilla with melted cheese oozing out",
      tags=["cheese", "tortilla", "mexican", "grilled", "snack"])
def _(S):
    ax, ay, R = 4, 19.5, 16
    p1, p2 = pt_on(ax, ay, R, -80), pt_on(ax, ay, R, -10)
    wedge = (poly([p2, (ax, ay), p1], r=S.r) + f"A{R} {R} 0 0 1 {fmt(p2[0])} {fmt(p2[1])}Z")
    drips = "M8 18.9V20.5A1.25 1.25 0 0 0 10.5 20.5V18.5ZM13.5 18V19.8A1.25 1.25 0 0 0 16 19.8V17.6Z"
    marks = [seg(*pt_on(ax, ay, d, -80 + 6), *pt_on(ax, ay, d, -10 - 6)) for d in (7.5, 12)]
    return [shell(union(wedge, drips)), *[detail(m) for m in marks]]


@icon("enchiladas", CAT, "Three rolled tortillas lined up in a baking dish",
      tags=["enchilada", "mexican", "baked", "casserole", "tortilla"], aliases=["enchilada"])
def _(S):
    dish = rect(3.5, 12.5, 17, 8, L(S, 1.5, 3))
    rolls = [circle(x, 10.5, 2.6) for x in (7, 12, 17)]
    out = [shell(dish), line(seg(1.5, 15, 3.5, 15)), line(seg(20.5, 15, 22.5, 15))]
    for r_ in rolls:
        out.append(shell(behind(r_, [dish], 1.0)))
    return out


@icon("nachos", CAT, "A pile of tortilla chips with a jalapeno ring",
      tags=["tortilla chips", "cheese", "mexican", "snack", "tex-mex"])
def _(S):
    front = poly([(6, 15.5), (12, 5.5), (18, 15.5)], closed=True, r=S.r)
    left = poly([(3, 15.5), (5, 5), (11, 12)], closed=True, r=S.r)
    right = poly([(13, 12), (19, 5), (21, 15.5)], closed=True, r=S.r)
    return [shell(front), shell(behind(left, [front], 1.25)), shell(behind(right, [front], 1.25)),
            detail(circle(12, 12.3, 1.8)), plate(S)]


@icon("fajitas", CAT, "A sizzling skillet of fajitas on a wooden board",
      tags=["sizzling", "skillet", "mexican", "tex-mex", "peppers"])
def _(S):
    pan = poly([(3, 11.5), (17, 11.5), (15.5, 16), (4.5, 16)], closed=True, r=S.r)
    return [shell(pan), line(seg(17, 13, 21.5, 13)), shell(rect(2.5, 18.5, 19, 2.5, L(S, 0.5, 1.25))),
            line("M6 3.5C5 5 7 6.5 6 8.5"), line("M10 3.5C9 5 11 6.5 10 8.5"), line("M14 3.5C13 5 15 6.5 14 8.5")]


@icon("tostada", CAT, "A flat crisp tortilla heaped with toppings",
      tags=["tortilla", "mexican", "crispy", "toppings", "tex-mex"])
def _(S):
    disk = ellipse(12, 17.3, 9.5, 3.2)
    heap = bumps([(5, 16), (6.5, 11.6), (10, 9.8), (14, 9.8), (17.5, 11.6), (19, 16)], r=2.6) + "Z"
    return [shell(heap), shell(behind(disk, [heap], None)), dot(12, 12.2, 1.4),
            detail(poly(zigzag(6.5, 17.5, 16, 1.2, 5), r=L(S, 0, 0.5)))]


@icon("elote", CAT, "A grilled corn cob on a stick with a creamy drizzle",
      tags=["street corn", "mexican corn", "corn on the cob", "grilled corn", "street food"])
def _(S):
    cob = rect(7.5, 2, 9, 15, 4.5 if S.name == "rounded" else 3)
    k = dict(deg=35, cx=12, cy=12, dx=1, dy=0)
    grid = [seg(12, 3.5, 12, 15.5), seg(7.5, 6.5, 16.5, 6.5), seg(7.5, 10, 16.5, 10), seg(7.5, 13.5, 16.5, 13.5)]
    return [shell(xf(cob, **k)), *[detail(xf(g, **k)) for g in grid], line(xf(seg(12, 17, 12, 22), **k))]


@icon("guacamole", CAT, "A bowl of chunky avocado dip with a tortilla chip",
      tags=["guac", "avocado dip", "mexican", "dip", "chips and dip"], aliases=["guac"])
def _(S):
    b = bowl(S, 12.5)
    mound = bumps([(4.5, 12.5), (6, 9.3), (9.5, 7.8), (13, 8.3)], r=2.4) + "L13 13H4.5Z"
    chip = poly([(12.5, 10.5), (15, 2.5), (20.5, 7.5)], closed=True, r=S.r)
    return [shell(b), shell(behind(mound, [b], None)), detail(seg(4, 12.5, 12.5, 12.5)),
            shell(behind(chip, [b], 1.0)), dot(8.8, 10.6, 1)]


@icon("ceviche", CAT, "A stemmed glass cup of cubed fish with a lime wedge on the rim",
      tags=["cebiche", "seafood", "peruvian", "raw fish", "lime"], aliases=["cebiche"])
def _(S):
    cup = ("M4 10H20C20 14 16.5 16.5 12 16.5C7.5 16.5 4 14 4 10Z" if S.name == "line" else
           "M5 10H19A1 1 0 0 1 20 11C19.6 14.4 16.2 16.5 12 16.5C7.8 16.5 4.4 14.4 4 11A1 1 0 0 1 5 10Z")
    lime = "M14.5 7.5A4 4 0 0 1 22 7.5Z"
    cubes = [blob(5.5, 5.5, 2.8, 2.8, L(S, 0, 0.7)), blob(9.8, 5.2, 2.8, 2.8, L(S, 0, 0.7)), blob(7.6, 1.8, 2.6, 2.6, L(S, 0, 0.7))]
    return [shell(cup), shell(xf(lime, 20, 18.25, 7.5, dy=-0.3)), line(seg(12, 16.5, 12, 20.5)),
            line(seg(8, 20.5, 16, 20.5)), *cubes]


COXINHA = "M12 2.5C13.5 6 18.5 9.5 18.5 14.5C18.5 18.5 15.5 21 12 21C8.5 21 5.5 18.5 5.5 14.5C5.5 9.5 10.5 6 12 2.5Z"


@icon("coxinha", CAT, "A teardrop-shaped breaded croquette with a bite taken out",
      tags=["brazilian", "croquette", "chicken", "snack", "fried"])
def _(S):
    body = path_to_d(D(P(COXINHA), P(circle(19.5, 11.5, 3.8))))
    return [shell(body), detail("M15.3 11.8C14 12.6 13.8 14.4 15.2 15.4"), dot(9, 14.5, 1), dot(11.5, 18, 1), dot(10.5, 10.5, 1)]


@icon("pao-de-queijo", CAT, "Three puffy cheese bread rolls in a small basket",
      tags=["cheese bread", "brazilian", "cheese puffs", "bread rolls", "snack"])
def _(S):
    basket = poly([(3, 13), (21, 13), (18.5, 20.5), (5.5, 20.5)], closed=True, r=S.r)
    a, b_, c = circle(7.8, 10, 3.6), circle(16.2, 10, 3.6), circle(12, 6.6, 3.6)
    return [shell(basket), detail(seg(4.2, 16.8, 19.8, 16.8)), shell(behind(a, [basket], 1)), shell(behind(b_, [basket], 1)),
            shell(behind(c, [a, b_, basket], 1))]


@icon("mofongo", CAT, "A dome of mashed plantain in a wooden mortar with a pestle",
      tags=["plantain", "puerto rican", "dominican", "mashed", "caribbean"])
def _(S):
    body = poly([(3.5, 12), (20.5, 12), (17, 17), (15.5, 17), (16.5, 20.5), (7.5, 20.5), (8.5, 17), (7, 17)],
                closed=True, r=S.r * 0.6)
    dome = "M5 13C5 8.5 8 5.5 12 5.5C16 5.5 19 8.5 19 13Z"
    pestle = capsule(15, 8, 20.5, 2.5, 3)
    return [shell(body), shell(behind(dome, [body], None)), detail(seg(4.5, 12, 19.5, 12)),
            shell(behind(pestle, [dome, body], 1.0)), dot(9.5, 9.3, 1), dot(12.8, 8.4, 1)]


def _slice_pts(cx, cy):
    return rotd(ellipse(cx, cy, 2.6, 4.8), 35, cx, cy)


@icon("fried-plantain", CAT, "Three oval slices of fried plantain in a row",
      tags=["platanos", "maduros", "plantains", "caribbean", "side dish"], aliases=["maduros"])
def _(S):
    a, b_, c = _slice_pts(6.5, 13), _slice_pts(12, 11.5), _slice_pts(17.5, 10)
    inner = lambda cx, cy: rotd(ellipse(cx, cy, 0.9, 2.4), 35, cx, cy)  # noqa: E731
    return [shell(c), shell(behind(b_, [c], 1.0)), shell(behind(a, [b_], 1.0)), detail(inner(17.5, 10))]


@icon("stuffed-pepper", CAT, "A bell pepper filled with rice with its top set to one side",
      tags=["stuffed peppers", "bell pepper", "baked", "rice", "mince"])
def _(S):
    body = ("M4.5 11.5H17.5C18.7 14 18.6 18 16.8 20C15.6 21.3 14 21 13 19.6C12.2 20.4 9.8 20.4 9 19.6"
            "C8 21 6.4 21.3 5.2 20C3.4 18 3.3 14 4.5 11.5Z")
    mound = bumps([(5.5, 12), (6.5, 9.2), (9.5, 7.8), (12.8, 8.3), (15.5, 10), (16.5, 12)], r=2) + "L16.5 13H5.5Z"
    lid = xf("M15.5 7C15.5 5.3 16.8 4.3 18.5 4.3C20.2 4.3 21.5 5.3 21.5 7Z", 25, 18.5, 6, dy=0.3)
    stem = xf("M18.5 4.3C18.5 3 18.9 2.2 20 1.8", 25, 18.5, 6, dy=0.3)
    return [shell(body), shell(behind(mound, [body], None)), detail(seg(5, 11.5, 17, 11.5)),
            shell(lid), line(stem)]


@icon("patatas-bravas", CAT, "A small dish of fried potato cubes with a cocktail stick",
      tags=["bravas", "tapas", "spanish", "potatoes", "fried potatoes"], aliases=["bravas"])
def _(S):
    dish = ("M3 14H21C21 18 17.2 20.5 12 20.5C6.8 20.5 3 18 3 14Z" if S.name == "line" else
            "M4 14H20A1 1 0 0 1 21 15C20.5 18.3 16.8 20.5 12 20.5C7.2 20.5 3.5 18.3 3 15A1 1 0 0 1 4 14Z")
    a = rotd(rect(4.5, 8.5, 5, 5, L(S, 0.3, 1.3)), -10, 7, 11)
    b_ = rotd(rect(14.5, 8.5, 5, 5, L(S, 0.3, 1.3)), 12, 17, 11)
    c = rotd(rect(9.5, 5, 5, 5, L(S, 0.3, 1.3)), 6, 12, 7.5)
    return [shell(dish), shell(behind(a, [dish], 1)), shell(behind(b_, [dish], 1)),
            shell(behind(c, [a, b_, dish], 1)), line(seg(13, 5.2, 16.5, 1.8))]


@icon("spaghetti", CAT, "A plate of spaghetti with a fork standing in it",
      tags=["pasta", "noodles", "italian", "dinner", "bolognese"])
def _(S):
    mound = "M4.5 15.5C4.5 11.5 7.8 9.5 12 9.5C16.2 9.5 19.5 11.5 19.5 15.5Z"
    return [shell(mound), plate(S), detail(wave_d(7, 17, 13.2, 0.55, 3.4)),
            *fork(S, 18.6, 3.4, 140, 7.5)]


# =========================================================================== pasta and Italian dishes

@icon("spaghetti-meatballs", CAT, "A plate of spaghetti topped with three meatballs",
      tags=["spaghetti and meatballs", "pasta", "italian", "dinner", "meatballs"], aliases=["spaghetti-and-meatballs"])
def _(S):
    mound = "M4.5 15.5C4.5 11.8 7.5 10 12 10C16.5 10 19.5 11.8 19.5 15.5Z"
    return [shell(mound), plate(S), detail(wave_d(6.5, 17.5, 13.3, 0.5, 3.6)),
            dot(7.8, 7.4, 2.2), dot(12.3, 6.2, 2.2), dot(16.6, 7.8, 2.2)]

@icon("lasagna", CAT, "A slice of lasagna showing layers of pasta, sauce and cheese",
      tags=["lasagne", "pasta bake", "italian", "baked pasta", "layers"], aliases=["lasagne"])
def _(S):
    hull = poly([(2.5, 9.5), (8, 5), (21.5, 5), (21.5, 15), (16, 20.5), (2.5, 20.5)], closed=True, r=L(S, 0, 2))
    return [shell(hull), detail(poly([(2.5, 9.5), (16, 9.5), (16, 20.5)])), detail(seg(16, 9.5, 21.5, 5)),
            detail(wave_d(2.5, 16, 13.2, 0.4, 3.4)), detail(wave_d(2.5, 16, 16.9, 0.4, 3.4))]

def _pinked_square(S, x0, y0, x1, y1, n):
    """Square with a crimped edge: zigzag teeth (Line) or scallops (Rounded), n per side."""
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    d = f"M{fmt(x0)} {fmt(y0)}"
    for i in range(4):
        a, b = corners[i], corners[(i + 1) % 4]
        for k in range(n):
            p = (a[0] + (b[0] - a[0]) * (k + 1) / n, a[1] + (b[1] - a[1]) * (k + 1) / n)
            m = (a[0] + (b[0] - a[0]) * (k + 0.5) / n, a[1] + (b[1] - a[1]) * (k + 0.5) / n)
            ox, oy = m[0] - cx, m[1] - cy
            ln = math.hypot(ox, oy)
            nx, ny = (b[1] - a[1]) / math.hypot(b[0] - a[0], b[1] - a[1]), -(b[0] - a[0]) / math.hypot(b[0] - a[0], b[1] - a[1])
            if S.name == "line":
                d += f"L{fmt(m[0] - nx * 1.0)} {fmt(m[1] - ny * 1.0)}L{fmt(p[0])} {fmt(p[1])}"
            else:
                seglen = math.hypot(b[0] - a[0], b[1] - a[1]) / n
                d += f"A{fmt(seglen * 0.55)} {fmt(seglen * 0.55)} 0 0 1 {fmt(p[0])} {fmt(p[1])}"
            _ = ln
    return d + "Z"


@icon("ravioli", CAT, "A square pasta pillow with a crimped edge and a filled centre",
      tags=["pasta", "stuffed pasta", "italian", "dumpling", "filled pasta"])
def _(S):
    return [shell(_pinked_square(S, 4, 4, 20, 20, 4)), detail(rect(7.5, 7.5, 9, 9, L(S, 1.5, 3.5)))]


@icon("penne", CAT, "Two short pasta tubes cut on the diagonal",
      tags=["pasta", "penne rigate", "tubes", "italian", "rigatoni"])
def _(S):
    out = []
    for off in (-4, 4):
        tube = [(-7.5, -2.4), (4, -2.4), (7.5, 2.4), (-4, 2.4)]
        pts = rot_pts([(12 + x, 12 + y + off) for x, y in tube], -40)
        out.append(shell(poly(pts, closed=True, r=L(S, 0, 0.8))))
        rid = rot_pts([(12 - 3, 12 + off), (12 + 3, 12 + off)], -40)
        out.append(detail(seg(*rid[0], *rid[1])))
    return out


@icon("farfalle", CAT, "Bow-tie shaped pasta pinched in the middle with crinkled edges",
      tags=["bow tie pasta", "butterfly pasta", "pasta", "italian", "bowtie"])
def _(S):
    def wing(sgn):
        xo = 12 + sgn * 9
        edge = zigzag(5, 19, 0, 1.1, 4)  # along y, teeth outward
        pts = [(xo + sgn * a, y) for y, a in edge]
        return [(12 + sgn * 2, 10.5)] + pts + [(12 + sgn * 2, 13.5)]
    left, right = wing(-1), wing(1)
    body = poly(left[:1] + left[1:-1] + left[-1:] + right[-1:] + list(reversed(right[1:-1])) + right[:1],
                closed=True, r=L(S, 0, 0.6))
    return [shell(body), detail(seg(7, 9.5, 7, 14.5)), detail(seg(17, 9.5, 17, 14.5))]


@icon("fusilli", CAT, "A short corkscrew spiral of pasta",
      tags=["pasta", "spiral pasta", "rotini", "twists", "italian"])
def _(S):
    left = [(9, 3.5)]
    right = []
    d = "M9.5 3.5"
    # silhouette: lobes alternate left and right down the twist
    lobes = [(3.5, "L"), (6.5, "R"), (9.5, "L"), (12.5, "R"), (15.5, "L"), (18.5, "R")]
    _ = (left, right, d, lobes)
    body = ("M10 3.5H14C16 3.5 16.5 5.5 15.5 6.5C17 7.5 17 9.5 15.5 10.5C17 11.5 17 13.5 15.5 14.5"
            "C17 15.5 17 17.5 15.5 18.5C16.5 19.5 16 20.5 14 20.5H10C8 20.5 7.5 18.5 8.5 17.5"
            "C7 16.5 7 14.5 8.5 13.5C7 12.5 7 10.5 8.5 9.5C7 8.5 7 6.5 8.5 5.5C7.5 4.5 8 3.5 10 3.5Z")
    twists = [seg(8.5, 5.5, 15.5, 10.5), seg(8.5, 9.5, 15.5, 14.5), seg(8.5, 13.5, 15.5, 18.5)]
    k = dict(deg=30)
    return [shell(xf(body, **k)), *[detail(xf(t, **k)) for t in twists]]


@icon("wagon-wheel-pasta", CAT, "A round pasta wheel with a hub, spokes and a rim",
      tags=["rotelle", "ruote", "wheel pasta", "pasta", "kids pasta"], aliases=["rotelle"])
def _(S):
    rim = circle(12, 12, 9) if S.name == "rounded" else poly(regular(12, 12, 9.4, 12, -90 + 15), closed=True)
    spokes = [detail(seg(*pt_on(12, 12, 2.3, a), *pt_on(12, 12, 6, a))) for a in range(-90, 270, 60)]
    return [shell(rim), detail(circle(12, 12, 6)), dot(12, 12, 1.6), *spokes]


@icon("mac-and-cheese", CAT, "A baking dish heaped with cheesy macaroni",
      tags=["macaroni cheese", "mac n cheese", "pasta bake", "comfort food", "cheese"], aliases=["macaroni-cheese"])
def _(S):
    dish = rect(3.5, 13, 17, 7.5, L(S, 1.5, 3))
    mound = bumps([(5, 13.5), (6.5, 9.5), (10, 7.3), (14, 7.3), (17.5, 9.5), (19, 13.5)], r=2.6) + "Z"
    return [shell(dish), shell(behind(mound, [dish], None)), detail(seg(4, 13, 20, 13)),
            line(seg(1.5, 15.5, 3.5, 15.5)), line(seg(20.5, 15.5, 22.5, 15.5)),
            detail(arc(8.2, 11.2, 1.5, 250, 110)), detail(arc(13.4, 10.4, 1.5, 150, 10))]

@icon("bruschetta", CAT, "A slice of toasted bread topped with diced tomato and a basil leaf",
      tags=["crostini", "italian", "appetizer", "tomato", "toast"])
def _(S):
    bread = rotd(ellipse(12, 12.5, 9.5, 6.2), -15)
    cubes = [blob(6.3, 11, 2.8, 2.8, L(S, 0, 0.7)), blob(10.1, 13.8, 2.8, 2.8, L(S, 0, 0.7)),
             blob(10.6, 8.6, 2.8, 2.8, L(S, 0, 0.7))]
    return [shell(bread), *cubes, detail(leaf(14.5, 14, 18, 9.5, 1.2))]


@icon("calzone", CAT, "A folded half-moon pizza with a rolled edge and steam vents",
      tags=["folded pizza", "pizza", "italian", "turnover", "stromboli"])
def _(S):
    cx, cy, R = 12, 16.5, 9.5
    body = (f"M{cx - R} {cy}A{R} {R} 0 0 1 {cx + R} {cy}Z" if S.name == "line" else
            f"M{cx - R + 1.5} {cy}A1.5 1.5 0 0 1 {cx - R} {cy - 1.5}A{R - 0.3} {R - 0.3} 0 0 1 {cx + R} {cy - 1.5}"
            f"A1.5 1.5 0 0 1 {cx + R - 1.5} {cy}Z")
    return [shell(body), detail(arc(cx, cy, 6.6, 195, 345)), detail(seg(9.5, 13.5, 10.5, 11.5)),
            detail(seg(13.5, 13.5, 14.5, 11.5)), line(seg(2, 20.5, 22, 20.5))]


@icon("deep-dish-pizza", CAT, "A tall slice of deep-dish pizza with a thick raised crust",
      tags=["chicago pizza", "pizza pie", "deep pan", "pizza slice", "stuffed crust"], aliases=["chicago-pizza"])
def _(S):
    body = poly([(2.5, 12.5), (17.5, 5), (21.5, 5), (21.5, 20.5), (2.5, 20.5)], closed=True, r=S.r)
    return [shell(body), detail(seg(17.5, 5, 17.5, 20.5)), detail(wave_d(5.5, 17.5, 15.3, 0.45, 3))]


@icon("caprese-salad", CAT, "Overlapping slices of tomato and mozzarella with a basil leaf",
      tags=["caprese", "tomato mozzarella", "insalata caprese", "italian", "salad"], aliases=["insalata-caprese"])
def _(S):
    ctr = [(17.2, 7.8), (13.2, 10.6), (9.2, 13.4)]
    discs = [circle(x, y, 4.4) for x, y in ctr]
    out = [shell(discs[2]), shell(behind(discs[1], [discs[2]], 1.0)), shell(behind(discs[0], [discs[1]], 1.0))]
    out += [dot(8, 12.5, 0.9), dot(10.6, 14.6, 0.9), dot(18.4, 6.3, 0.9)]
    out.append(shell(leaf(13.5, 19.5, 20, 15, 1.5)))
    return out


@icon("panini", CAT, "A pressed sandwich cut diagonally with grill marks",
      tags=["panino", "pressed sandwich", "toastie", "grilled sandwich", "italian"], aliases=["panino"])
def _(S):
    a = poly([(3, 3), (19, 3), (3, 19)], closed=True, r=L(S, 0, 1.5))
    b_ = poly([(21, 5), (21, 21), (5, 21)], closed=True, r=L(S, 0, 1.5))
    return [shell(a), shell(b_), detail(seg(6.3, 9.7, 9.7, 6.3)),
            detail(seg(14.3, 17.7, 17.7, 14.3))]


@icon("risotto", CAT, "A wide-rimmed bowl of creamy risotto seen from above",
      tags=["rice", "italian", "arborio", "creamy rice", "dinner"])
def _(S):
    grains = [(9, 9.5, 30), (13.2, 8.8, -30), (15, 12.6, 60), (11.2, 12.8, -10), (8.4, 14.6, 45), (12.6, 16, 20)]

    def grain(x, y, a):
        if S.name == "line":
            p0, p1 = rot_pts([(x - 1.5, y), (x + 1.5, y)], a, x, y)
            return Part("dot", leaf(*p0, *p1, 0.55))
        return Part("dot", rotd(ellipse(x, y, 1.3, 0.8), a, x, y))
    return [shell(circle(12, 12, 9.5)), detail(circle(12, 12, 6.6)), *[grain(*g) for g in grains]]


@icon("french-onion-soup", CAT, "A soup crock with a bubbling cheese crust spilling over the rim",
      tags=["onion soup", "soupe a l'oignon", "gratinee", "french", "soup"], aliases=["onion-soup"])
def _(S):
    crock = rect(4.5, 12, 15, 8.5, L(S, 1.5, 3))
    crust = (bumps([(3.5, 12), (5, 8.5), (8.8, 6.3), (12.8, 5.9), (16.6, 7.2), (19, 9.8), (20.5, 12)], r=2.6)
             + "H17V14.5A1.25 1.25 0 0 1 14.5 14.5V12H9V15A1.25 1.25 0 0 1 6.5 15V12Z")
    return [shell(crust), shell(behind(crock, [crust], 1.0)), line(seg(1.5, 15.5, 4.5, 15.5)), line(seg(19.5, 15.5, 22.5, 15.5))]


@icon("ratatouille", CAT, "A round dish of vegetable slices arranged in an overlapping spiral",
      tags=["confit byaldi", "tian", "vegetables", "french", "provencal"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(scallop_ring(12, 12, 5.6, 9, 1.05)), detail(circle(12, 12, 1.6))]


@icon("escargot", CAT, "A snail shell served on a plate",
      tags=["snails", "french", "garlic butter", "delicacy", "appetizer"], aliases=["escargots"])
def _(S):
    shell_d = circle(12, 10.5, 6.5)
    spiral = poly(_spiral(12.3, 10.6, 0.3, 4.1, 1.3, start=0, n=24))
    return [shell(shell_d), detail(spiral), plate(S)]


@icon("mussels-pot", CAT, "A pot of mussels with its lid tilted open",
      tags=["moules", "mussels", "moules frites", "seafood", "steamed mussels"], aliases=["moules"])
def _(S):
    pot = rect(3.5, 12, 15, 8.5, L(S, 1.5, 3))
    shells = [leaf(5.5, 12.5, 8, 5.5, 1.4), leaf(10, 12.5, 11.5, 5, 1.4)]
    lid = xf(rect(12, 7, 10, 2, L(S, 0.3, 1)), -30, 17, 8)
    knob = xf(rect(15.5, 4.8, 3, 2.2, L(S, 0.3, 1)), -30, 17, 8)
    return [shell(pot), line(seg(1.5, 15, 3.5, 15)), line(seg(18.5, 15, 20.5, 15)),
            *[shell(behind(sh, [pot], 1.0)) for sh in shells], shell(union(lid, knob))]


@icon("schnitzel", CAT, "A thin breaded cutlet with a slice of lemon on top",
      tags=["wiener schnitzel", "cutlet", "escalope", "breaded", "austrian"], aliases=["escalope"])
def _(S):
    edge = (poly(star_ring(12, 12, 9.4, 8.4, 13), closed=True) if S.name == "line" else scallop_ring(12, 12, 8.6, 13, 1.15))
    body = path_to_d(transform_path(P(edge), (1, 0, 0, 0.78, 0, 12 * 0.22)))
    return [shell(rotd(body, -15)), detail(circle(13.5, 11, 3.2)), detail(seg(13.5, 8.8, 13.5, 13.2)),
            detail(seg(11.3, 11, 15.7, 11))]


@icon("currywurst", CAT, "A tray of sliced sausage in curry sauce with a small fork",
      tags=["german", "sausage", "street food", "curry sauce", "berlin"])
def _(S):
    tray = rect(2.5, 7, 17, 13, L(S, 2, 3.5))
    slices = [detail(circle(x, y, 2.1)) for x, y in ((7.2, 11.5), (13.2, 11.3), (10.2, 15.8))]
    return [shell(tray), *slices, line(seg(16, 15.5, 21, 3))]


def _half_moon(S, cx, cy, R):
    n = 5
    pts = [pt_on(cx, cy, R, 180 + i * 180 / n) for i in range(n + 1)]
    if S.name == "line":
        d = poly([pts[0]] + [q for i in range(n) for q in (pt_on(cx, cy, R + 0.9, 180 + (i + 0.5) * 180 / n), pts[i + 1])])
    else:
        br = R * math.sin(math.radians(90 / n)) * 1.15
        d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}" + "".join(f"A{fmt(br)} {fmt(br)} 0 0 1 {fmt(x)} {fmt(y)}" for x, y in pts[1:])
    return d + "Z"


@icon("pierogi", CAT, "Three half-moon dumplings with crimped edges",
      tags=["pierogies", "perogies", "polish dumplings", "dumplings", "varenyky"], aliases=["perogies"])
def _(S):
    return [shell(_half_moon(S, 6.6, 20, 4)), shell(_half_moon(S, 17.4, 20, 4)), shell(_half_moon(S, 12, 11.5, 5.4))]


@icon("kielbasa", CAT, "A horseshoe-shaped smoked sausage tied with string at one end",
      tags=["polish sausage", "smoked sausage", "sausage", "ring sausage", "polish"], aliases=["polish-sausage"])
def _(S):
    cx, cy, rc = 12, 13, 6.3
    centre = arc(cx, cy, rc, 160, 20)
    body = path_to_d(ST(centre, 4.8, "round" if S.name == "rounded" else "butt", "round"))
    end = pt_on(cx, cy, rc, 20)
    tie = [line(seg(end[0] + 0.6, end[1] + 2.6, end[0] + 2, end[1] + 6.5)), line(seg(end[0] - 1.6, end[1] + 3.2, end[0] - 1.6, end[1] + 7))]
    return [shell(body), *tie]
