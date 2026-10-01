"""TypeIcon Core: world dishes (batch dishes_006).

South Asian, Balkan, French, Spanish, British, American and Latin American plates, pots, wraps and sandwiches,
drawn from the food itself. Side views sit on a shallow plate or in a round bowl; top views sit on a round
plate (r 9).
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



# =========================================================================== chunk 1


def pod(x1, y1, x2, y2, bend, w):
    """Closed lens-shaped pod from (x1, y1) to (x2, y2), curved by `bend`, w = half thickness."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    a, b = (bend + w) * 2, (bend - w) * 2
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx * a)} {fmt(my + ny * a)} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(mx + nx * b)} {fmt(my + ny * b)} {fmt(x1)} {fmt(y1)}Z")


@icon("dal-bati", CAT, "Round baked wheat balls beside a small bowl of lentils",
      tags=["baati", "rajasthani", "indian", "lentils", "dal", "ghee", "baked wheat balls"],
      aliases=["dal-baati"])
def _(S):
    bati = circle(7, 15, 4.9)
    back = circle(11, 6.8, 3.7)
    if S.name == "line":
        bowl_d = "M13 14.5H22C22 18.5 19.5 21 17.5 21C15.5 21 13 18.5 13 14.5Z"
    else:
        bowl_d = "M14 14.5H21A1 1 0 0 1 22 15.5C21.6 19 19.6 21 17.5 21C15.4 21 13.4 19 13 15.5A1 1 0 0 1 14 14.5Z"
    bowl_d = union(bowl_d, "M14.6 14.5C15.3 10.8 19.7 10.8 20.4 14.5Z")
    return [shell(behind(back, [bati], 1.25)), shell(bati), detail("M4.8 12.8Q8 13.2 9.2 16.6"),
            shell(bowl_d), detail(seg(13, 14.5, 22, 14.5)), dot(17.5, 17.8, 1.0)]


@icon("sambar", CAT, "A bowl of lentil and vegetable stew with a long seeded drumstick pod sticking out",
      tags=["south indian", "lentil stew", "idli", "drumstick", "moringa", "dal", "soup"])
def _(S):
    b = bowl(S, 14)
    p = capsule(10.5, 12.5, 19.5, 3.8, 4.6)
    return [shell(behind(p, [b], 1.25)), shell(b), dot(8.5, 17.6, 1.1), dot(14, 18.4, 1.1),
            dot(13.2, 9.2, 0.85), dot(16.6, 6.2, 0.85)]


@icon("shopska-salad", CAT, "A bowl of chopped tomato and cucumber hidden under a tall heap of grated white cheese",
      tags=["bulgarian", "balkan", "sirene", "feta", "grated cheese", "tomato cucumber salad", "salad"])
def _(S):
    heap = "M5.5 13C5.5 9 9.5 6.5 12 2.8C14.5 6.5 18.5 9 18.5 13Z"
    if S.name == "rounded":
        heap = "M5.5 13C5.5 9 9 7 10.6 3.8Q12 1.8 13.4 3.8C15 7 18.5 9 18.5 13Z"
    body = union(bowl(S, 13.5), heap)
    return [shell(body), detail(seg(3, 13.5, 21, 13.5)), dot(12, 9.2, 0.9), dot(8.2, 16.8, 1.1), dot(14.2, 17.6, 1.1)]


@icon("duck-confit", CAT, "A crisp duck leg with a knob bone end resting on a bed of sliced potatoes",
      tags=["french", "confit de canard", "duck leg", "roast duck", "potatoes", "poultry"])
def _(S):
    meat = oval(14.5, 7.8, 6.6, 4.8, -45)
    bone = capsule(10.5, 11.4, 6.3, 15.6, 2.0)
    leg = union(meat, bone, circle(5.4, 15.6, 1.5), circle(7.3, 17.4, 1.4))
    strip = "M2.5 21.5V20A3.2 3.2 0 0 1 8.9 20A3.2 3.2 0 0 1 15.1 20A3.2 3.2 0 0 1 21.5 20V21.5Z"
    return [shell(behind(strip, [leg], 1.25)), shell(leg), detail("M13 5.8Q16 6.8 17 9.8")]


@icon("chip-butty", CAT, "A soft white bread roll stuffed with thick chips poking out of the top",
      tags=["chip sandwich", "chip roll", "fries sandwich", "british", "carbs", "bun", "pub food"],
      aliases=["chip-sandwich"])
def _(S):
    bun = "M3.5 15C3.5 11.5 7.5 10.5 12 10.5C16.5 10.5 20.5 11.5 20.5 15V17C20.5 19.5 18.5 21 16 21H8C5.5 21 3.5 19.5 3.5 17Z"
    chips = [line(seg(7, 11, 5.4, 4.2)), line(seg(12, 11, 12.6, 2.8)), line(seg(17, 11, 18.8, 5.4))]
    return chips + [shell(bun), detail(seg(3.5, 15.6, 20.5, 15.6))]


@icon("pie-and-mash", CAT, "A pie and a scoop of mashed potato in a shallow dish of green parsley sauce",
      tags=["london", "cockney", "eel", "liquor", "mashed potato", "meat pie", "british"])
def _(S):
    dish = poly([(2.5, 15.5), (21.5, 15.5), (19, 21.5), (5, 21.5)], closed=True, r=S.r)
    pie = "M3.8 15.5V10.6C3.8 8.8 5.2 8 6.6 8H10.4C11.8 8 13.2 8.8 13.2 10.6V15.5Z"
    mash = "M13.8 15.5C13.8 11.5 15 6.5 17.3 6.5C19.6 6.5 20.8 11.5 20.8 15.5Z"
    body = union(dish, pie, mash)
    return [shell(body), detail(wave_d(2.5, 21.5, 15.5, 0.55, 4.75)), detail(seg(6, 11, 11, 11)), detail("M15.8 10.6Q17.3 12 18.8 10.6")]


def rrect_pts(x, y, w, h, deg):
    return rot_pts([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], deg, x + w / 2, y + h / 2)


@icon("chicken-fried-steak", CAT, "A breaded flat steak smothered in thick peppered white gravy",
      tags=["country fried steak", "southern", "american", "gravy", "breaded cutlet", "diner", "comfort food"],
      aliases=["country-fried-steak"])
def _(S):
    body = oval(12, 12, 9.6, 7.4, -14)
    cloud = path_to_d(transform_path(P(scallop_ring(12, 12, 5.7, 7, 1.15, -80)), (1.2, 0, 0, 0.92, -2.4, 0.9)))
    return [shell(body), detail(rotd(cloud, -14)), dot(10.4, 10, 0.75), dot(13.8, 12.2, 0.75), dot(9.8, 13.4, 0.75)]


@icon("walking-taco", CAT, "A small open snack bag filled with taco toppings and a fork sticking out",
      tags=["taco in a bag", "chip bag taco", "chips bag", "mexican", "snack", "midwest", "street food"],
      aliases=["taco-in-a-bag"])
def _(S):
    bag = poly([(5.5, 10), (7.6, 8.4), (9.8, 10), (12, 8.4), (14.2, 10), (16.4, 8.4), (18.5, 10), (17, 21), (7, 21)], closed=True, r=S.r * 0.5)
    pile = "M6.8 9.4C6.4 6.4 9 5.4 10.4 6.6C11.8 4.8 14.6 5.2 15 7.2C16.6 7.4 17.4 8.6 17.2 9.4Z"
    return [shell(union(bag, pile)), detail(seg(6.4, 14.5, 17.6, 14.5)), *fork(S, 20.4, 3.4, 125, 8.6)]


@icon("hotdish", CAT, "A rectangular baking dish topped with neat rows of crisp potato cylinders",
      tags=["potato tot casserole", "potato tots", "casserole", "midwest", "minnesota", "baked dish", "potluck"],
      aliases=["tot-casserole"])
def _(S):
    top = poly([(7, 4.5), (21, 4.5), (19.5, 11), (5.5, 11)], closed=True, r=L(S, 0, 1))
    front = rect(4.5, 11, 15, 9, L(S, 0.5, 2))
    tots = [Part("dot", oval(x + (y - 7.5) * -0.22, y, 1.45, 1.05)) for x in (9.3, 13.2, 17.1) for y in (6.9, 9.3)]
    return [shell(union(top, front)), detail(seg(4.5, 11, 19.5, 11)), line(seg(1.5, 15, 4.5, 15)), line(seg(19.5, 15, 22.5, 15))] + tots


@icon("bean-pot", CAT, "A round lidded crock of baked beans in sauce, the lid tilted off to show beans at the rim",
      tags=["baked beans", "boston baked beans", "crock", "bean crock", "stew pot", "slow cooker", "new england"],
      aliases=["baked-beans-pot"])
def _(S):
    body = ("M4.5 12H19.5C19.5 17.5 16.5 21 12 21C7.5 21 4.5 17.5 4.5 12Z" if S.name == "line" else
            "M5.5 12H18.5A1 1 0 0 1 19.5 13C19.2 17.6 16.4 21 12 21C7.6 21 4.8 17.6 4.5 13A1 1 0 0 1 5.5 12Z")
    lid = xf("M5.5 11C5.5 7.2 8.4 5.6 12 5.6C15.6 5.6 18.5 7.2 18.5 11Z", 20, 18.5, 11.4)
    knob = xf(seg(12, 5.6, 12, 4), 20, 18.5, 11.4)
    return [shell(body), line(seg(2, 14.5, 4.6, 14.5)), line(seg(19.4, 14.5, 22, 14.5)), shell(lid), line(knob),
            Part("dot", oval(7.6, 10.2, 1.5, 1.0, -20)), Part("dot", oval(11.4, 9.6, 1.5, 1.0, 15))]


@icon("moqueca", CAT, "A round clay pot of fish stew with a fish tail and pepper ring showing, its wooden lid leaning against it",
      tags=["brazilian", "fish stew", "seafood stew", "clay pot", "coconut", "bahia", "capixaba"])
def _(S):
    body = ("M3 11.5H16C16 17 13 20.8 9.5 20.8C6 20.8 3 17 3 11.5Z" if S.name == "line" else
            "M4 11.5H15A1 1 0 0 1 16 12.5C15.6 17.2 13 20.8 9.5 20.8C6 20.8 3.4 17.2 3 12.5A1 1 0 0 1 4 11.5Z")
    mound = "M4.4 11.5C4.4 8.8 6.4 7.8 9.5 7.8C12.6 7.8 14.6 8.8 14.6 11.5Z"
    tail = poly([(5.8, 8.6), (4.8, 4), (7.4, 5.6), (9.6, 4.2), (9, 8.6)], closed=True, r=L(S, 0, 0.6))
    lid = oval(19, 12.5, 2.7, 6.6, 12)
    pot = union(body, mound, tail)
    return [shell(behind(lid, [pot], 1.0)), shell(pot), detail(seg(3, 11.5, 16, 11.5)), detail(circle(12.4, 9.8, 1.3))]


@icon("acaraje", CAT, "A golden bean fritter split open like a clam, stuffed with shrimp and a spicy paste",
      tags=["brazilian", "bahia", "black-eyed pea fritter", "street food", "shrimp", "vatapa", "deep fried"],
      aliases=["acaraje-fritter"])
def _(S):
    if S.name == "line":
        top = "M3 12H21C21 7.5 17 4.5 12 4.5C7 4.5 3 7.5 3 12Z"
        bot = "M3 13.8H21C21 18.3 17 21 12 21C7 21 3 18.3 3 13.8Z"
    else:
        top = "M4 12H20A1 1 0 0 0 21 11C20.6 7.2 17 4.5 12 4.5C7 4.5 3.4 7.2 3 11A1 1 0 0 0 4 12Z"
        bot = "M4 13.8H20A1 1 0 0 1 21 14.8C20.6 18.6 17 21 12 21C7 21 3.4 18.6 3 14.8A1 1 0 0 1 4 13.8Z"
    lid = rotd(top, -14, 3, 12)
    fill = "M12.6 13.8Q13.4 10.8 15.4 12Q16.8 9.6 19 11.6Q20.4 12.6 20.4 13.8"
    return [shell(lid), shell(bot), line(fill), dot(9.6, 16.6, 1.0)]


@icon("tlayuda", CAT, "A very large thin crisp tortilla folded in half with beans and cheese showing along the open edge",
      tags=["oaxacan", "mexican", "giant tortilla", "memela", "beans", "quesillo", "street food"])
def _(S):
    fold = "M2.5 14A9.5 9.5 0 0 1 21.5 14Z" if S.name == "line" else "M3.5 14A9 9 0 0 1 20.5 14Z"
    cheese = "M4.5 14.6Q6.2 18.4 8.2 14.6Q10 18.4 12 14.6Q14 18.4 15.8 14.6Q17.6 18.4 19.5 14.6"
    return [shell(fold), line(cheese), dot(9, 10.6, 1.0), dot(14, 9.6, 1.0), dot(16.6, 12.4, 1.0)]


@icon("huaraches", CAT, "A long flat sandal-sole shaped corn base topped with beans and crumbled cheese",
      tags=["huarache", "mexican", "masa", "oval tortilla", "beans", "cotija", "street food"],
      aliases=["huarache"])
def _(S):
    sole = ("M2.4 12.6C2.4 9.8 4.4 8.4 7.4 8.4C10 8.4 11.6 8.8 13.6 8.4C15.6 8 17.4 6.6 19.6 7.2C21.4 7.7 22 9.6 22 12"
            "C22 14.6 21.2 16.6 19.2 17C17.2 17.4 15.4 16 13.6 15.8C11.6 15.6 10 15.8 7.4 15.8C4.4 15.8 2.4 15.2 2.4 12.6Z")
    return [shell(rotd(sole, -22)), detail(xf("M5.8 12Q8.8 9.8 11.8 12Q14.8 14.2 17.8 11.8", -22)),
            dot(*rot_pts([(8.6, 14.5)], -22)[0], 0.85), dot(*rot_pts([(14.6, 9.6)], -22)[0], 0.85)]


@icon("gatsby-sandwich", CAT, "A very long bread roll stuffed with chips, cut into sections",
      tags=["south african", "cape town", "chip roll", "sub", "fries sandwich", "footlong", "street food"])
def _(S):
    t = -14
    roll = capsule(4.5, 15, 19.5, 15, 8.4) if S.name == "rounded" else rect(2.5, 10.8, 19, 8.4, 3.6)
    if S.name == "rounded":
        roll = rect(2.5, 10.8, 19, 8.4, 4.2)
    chips = [line(xf(seg(6, 11.3, 4.4, 4.6), t)), line(xf(seg(10.2, 11.3, 10.6, 3.6), t)), line(xf(seg(14.4, 11.3, 13.6, 5), t)),
             line(xf(seg(18.2, 11.3, 19.8, 5.8), t))]
    return chips + [shell(rotd(roll, t)), detail(xf(seg(9, 10.8, 9, 19.2), t)), detail(xf(seg(15, 10.8, 15, 19.2), t))]
