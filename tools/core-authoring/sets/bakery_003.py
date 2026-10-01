"""TypeIcon Core: bakery, sweets and dairy (batch bakery_003).

Cookies and crackers, sweets and chocolates, honey and syrup, milk, butter, cheese and eggs, drawn from
the objects themselves. Most things are seen from the front or the side; flat round things from above.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, rotation, transform_path  # noqa: F401

CAT = "bakery"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rotd(d, deg, cx=12.0, cy=12.0, dx=0.0, dy=0.0):
    """Rotate a closed outline (clockwise on screen) about (cx, cy), then translate."""
    a, b, c, d_, e, f = rotation(deg, cx, cy)
    return path_to_d(transform_path(P(d), (a, b, c, d_, e + dx, f + dy)))


def rot_pts(points, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in points]


def rseg(x1, y1, x2, y2, deg, cx=12.0, cy=12.0):
    (a, b), (c, d) = rot_pts([(x1, y1), (x2, y2)], deg, cx, cy)
    return seg(a, b, c, d)


def behind(back_d, fronts, gap=1.75):
    """Outline of the part of back_d not hidden by the front shapes, kept `gap` clear of their strokes.
    gap=None attaches the back shape to the front outline (their strokes merge)."""
    if gap is None:
        cut = U(*[P(f) for f in fronts])
    else:
        cut = U(*[U(P(f), ST(f, 2 * (gap + 2), "round", "round")) for f in fronts])
    return path_to_d(D(P(back_d), cut))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def band(d, w, S=None, cap="round"):
    """Closed outline of an open centre line thickened to width w."""
    return path_to_d(ST(d, w, cap, "round"))


def capsule(x1, y1, x2, y2, w):
    """Stadium (round-ended bar) of width w along (x1, y1)-(x2, y2)."""
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln * w / 2, (x2 - x1) / ln * w / 2
    r = fmt(w / 2)
    return (f"M{fmt(x1 + nx)} {fmt(y1 + ny)}L{fmt(x2 + nx)} {fmt(y2 + ny)}A{r} {r} 0 0 0 {fmt(x2 - nx)} {fmt(y2 - ny)}"
            f"L{fmt(x1 - nx)} {fmt(y1 - ny)}A{r} {r} 0 0 0 {fmt(x1 + nx)} {fmt(y1 + ny)}Z")


def bar(x1, y1, x2, y2, w, rc=0.0):
    """Rectangle of width w along the axis (x1, y1)-(x2, y2), corners filleted by rc."""
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln * w / 2, (x2 - x1) / ln * w / 2
    return poly([(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)], closed=True, r=rc)


def pt_on(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def scallop_ring(cx, cy, R, n, bulge=1.1, start=-90.0):
    pts = [pt_on(cx, cy, R, start + i * 360 / n) for i in range(n)]
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    br = R * math.sin(math.pi / n) * bulge
    for i in range(n):
        x, y = pts[(i + 1) % n]
        d += f"A{fmt(br)} {fmt(br)} 0 0 1 {fmt(x)} {fmt(y)}"
    return d + "Z"


def heart(cx, cy, w, pointed=True):
    """Heart of width w centred on (cx, cy)."""
    s = w / 16.0
    if pointed:
        d = ("M8 14.5L2.2 8.6C0.4 6.8 0.4 3.9 2.2 2.2C3.9 0.5 6.6 0.6 8 2.6"
             "C9.4 0.6 12.1 0.5 13.8 2.2C15.6 3.9 15.6 6.8 13.8 8.6Z")
    else:
        d = ("M8 14.5C7.5 14.5 7.1 14.2 6.7 13.8L2.2 8.6C0.4 6.8 0.4 3.9 2.2 2.2C3.9 0.5 6.6 0.6 8 2.6"
             "C9.4 0.6 12.1 0.5 13.8 2.2C15.6 3.9 15.6 6.8 13.8 8.6L9.3 13.8C8.9 14.2 8.5 14.5 8 14.5Z")
    return path_to_d(transform_path(P(d), (s, 0, 0, s, cx - 8 * s, cy - 7.5 * s)))


def chips(pts, r=1.0):
    return [dot(x, y, r) for x, y in pts]


# =========================================================================== cookies and crackers

@icon("wafer-roll", CAT, "Two rolled wafer tubes lying side by side with a spiral line along each",
      tags=["wafer", "rolled wafer", "wafer stick", "biscuit", "cookie", "snack"])
def _(S):
    w = 5.5
    a = capsule(5.75, 7.25, 15.25, 7.25, w) if S.name == "rounded" else rect(3, 4.5, 15, w, 1)
    b = capsule(8.75, 16.75, 18.25, 16.75, w) if S.name == "rounded" else rect(6, 14, 15, w, 1)
    parts = [shell(a), shell(b)]
    for x in (7.5, 11.5, 15.5):
        parts.append(detail(seg(x - 1.4, 10, x + 1.4, 4.5)))
    for x in (10.5, 14.5, 18.5):
        parts.append(detail(seg(x - 1.4, 19.5, x + 1.4, 14)))
    return parts


@icon("linzer-cookie", CAT, "A round scalloped cookie with a heart-shaped window showing jam",
      tags=["linzer", "jam cookie", "sandwich cookie", "valentine cookie", "biscuit", "christmas cookie"])
def _(S):
    return [shell(scallop_ring(12, 12, 8.2, 10, 1.15)), detail(heart(12, 12.4, 8.5, S.name == "line"))]


@icon("pinwheel-cookie", CAT, "A round cookie with a two-tone spiral swirl",
      tags=["pinwheel", "swirl cookie", "spiral cookie", "icebox cookie", "biscuit", "cookie"])
def _(S):
    sp = ("M12 12A1.75 1.75 0 0 1 15.5 12A3.5 3.5 0 0 1 8.5 12A5.25 5.25 0 0 1 19 12"
          "A7 7 0 0 1 5 12")
    body = circle(12, 12, 9) if S.name == "rounded" else regular_poly(12, 12, 9.2, 12)
    return [shell(body), detail(sp)]


def regular_poly(cx, cy, r, n):
    return poly(regular(cx, cy, r, n), closed=True)


@icon("cracker", CAT, "A square crisp cracker with a crimped edge and rows of docking holes",
      tags=["saltine", "biscuit", "cracker biscuit", "snack", "crispbread", "soda cracker"])
def _(S):
    n = 4
    step = 18 / n
    d = "M3 3"
    for side in range(4):
        for k in range(n):
            if side == 0:
                x, y, cx_, cy_ = 3 + step * (k + 1), 3, 3 + step * (k + 0.5), 3
            elif side == 1:
                x, y = 21, 3 + step * (k + 1)
            elif side == 2:
                x, y = 21 - step * (k + 1), 21
            else:
                x, y = 3, 21 - step * (k + 1)
            if S.name == "rounded":
                d += f"A{fmt(step * 0.62)} {fmt(step * 0.62)} 0 0 1 {fmt(x)} {fmt(y)}"
            else:
                # small triangular teeth
                px, py = {0: (x - step / 2, y - 1.2), 1: (x + 1.2, y - step / 2),
                          2: (x + step / 2, y + 1.2), 3: (x - 1.2, y + step / 2)}[side]
                d += f"L{fmt(px)} {fmt(py)}L{fmt(x)} {fmt(y)}"
    d += "Z"
    holes = [dot(x, y, 1.1) for x in (8, 12, 16) for y in (8, 12, 16)]
    return [shell(d), *holes]


@icon("rice-cracker", CAT, "A round puffed rice cracker wrapped with a band of seaweed",
      tags=["senbei", "rice cake", "seaweed cracker", "japanese snack", "nori", "cracker"])
def _(S):
    disc = circle(12, 12, 8.5) if S.name == "rounded" else ellipse(12, 12, 8.8, 8.3)
    h = 8.1
    nori = path_to_d(I(P(rect(10.5, 2, 3, 20)), P(circle(12, 12, 8.5))))
    return [shell(disc), detail(seg(9.5, 12 - h, 9.5, 12 + h)), detail(seg(14.5, 12 - h, 14.5, 12 + h)), solid(nori),
            dot(6, 10, 0.8), dot(6.3, 14.3, 0.8), dot(18, 10, 0.8), dot(17.7, 14.3, 0.8)]


LADY = ("M6.75 9.25C10 10.1 14 10.1 17.25 9.25A2.75 2.75 0 0 1 17.25 14.75"
        "C14 13.9 10 13.9 6.75 14.75A2.75 2.75 0 0 1 6.75 9.25Z")


@icon("ladyfinger", CAT, "Two long flat sponge biscuits dusted with sugar dots",
      tags=["savoiardi", "sponge finger", "biscuit", "tiramisu", "boudoir biscuit", "cookie"])
def _(S):
    a = rotd(LADY, -45, 12, 12, -3.2, -3.2)
    b = rotd(LADY, -45, 12, 12, 3.4, 3.4)
    if S.name == "line":
        a = rotd(LADY.replace("A2.75 2.75 0 0 1", "A2.75 3 0 0 1"), -45, 12, 12, -3.2, -3.2)
    dots_a = [rot_pts([(x, 12)], -45)[0] for x in (9, 12, 15)]
    dots_b = [rot_pts([(x, 12)], -45)[0] for x in (9, 12, 15)]
    return [shell(a), shell(b),
            *[dot(x - 3.2, y - 3.2, 0.9) for x, y in dots_a], *[dot(x + 3.4, y + 3.4, 0.9) for x, y in dots_b]]


@icon("pizzelle", CAT, "A thin round wafer cookie pressed with a snowflake pattern",
      tags=["pizzelle", "wafer cookie", "italian cookie", "waffle cookie", "christmas cookie", "biscuit"])
def _(S):
    parts = [shell(scallop_ring(12, 12, 8.4, 16, 1.2) if S.name == "rounded" else
                   poly(regular(12, 12, 9, 16), closed=True))]
    for ang in (-90, -30, 30):
        (x1, y1), (x2, y2) = pt_on(12, 12, 5, ang), pt_on(12, 12, 5, ang + 180)
        parts.append(detail(seg(x1, y1, x2, y2)))
    return parts


@icon("granola-bar", CAT, "A chunky oat bar with its wrapper still around one end",
      tags=["cereal bar", "oat bar", "flapjack", "snack bar", "muesli bar", "energy bar"])
def _(S):
    right = [(20.8, 6.5), (19.8, 9.25), (20.8, 12), (19.8, 14.75), (20.8, 17.5)]
    torn = [(13, 17.5), (11.8, 15.3), (13, 13.1), (11.8, 10.9), (13, 8.7), (11.8, 6.5)]
    wrap = poly(right + torn, closed=True, r=L(S, 0, 0.6))
    barr = rect(3, 8.5, 12, 7, L(S, 1, 2))
    return [shell(wrap), shell(behind(barr, [wrap], 0)), detail(seg(17.5, 6.5, 17.5, 17.5)),
            dot(5.8, 11, 1), dot(8.8, 13.2, 1), dot(9, 10.6, 0.8), dot(5.8, 13.8, 0.8)]


@icon("milk-and-cookies", CAT, "A glass of milk with a chocolate chip cookie in front",
      tags=["milk", "cookie", "snack", "bedtime snack", "santa treat", "biscuits and milk"])
def _(S):
    glass = poly([(3.5, 3), (14.5, 3), (13.2, 21), (4.8, 21)], closed=True, r=S.r)
    cookie = circle(16.5, 16.5, 4.8)
    return [shell(behind(glass, [cookie], 1.25)), detail(seg(4, 7.5, 12, 7.5)), shell(cookie),
            dot(15, 15, 0.9), dot(18.3, 16.2, 0.9), dot(16, 18.6, 0.9)]


@icon("cookie-jar", CAT, "A round glass jar with a knobbed lid and a cookie inside",
      tags=["biscuit jar", "biscuit barrel", "cookie", "jar", "kitchen", "treat jar"])
def _(S):
    body = rect(4, 9, 16, 12.5, L(S, 3, 5))
    lid = rect(5.5, 5, 13, 2.5, L(S, 0.5, 1.25))
    knob = rect(10, 2, 4, 2.5, L(S, 0.5, 1.25))
    return [shell(body), shell(lid), shell(knob), detail(circle(12, 15.25, 3.75)),
            dot(10.7, 14, 0.85), dot(13.4, 14.6, 0.85), dot(11.8, 16.8, 0.85)]


@icon("cookie-tin", CAT, "A round cookie tin with its lid propped open and cookies inside",
      tags=["biscuit tin", "butter cookies", "tin", "gift tin", "cookies", "sewing tin"])
def _(S):
    body = rect(3, 13, 18, 8, L(S, 1.5, 3))
    lid = rotd(rect(5, 3, 16, 3.5, L(S, 1, 1.75)), 18, 13, 5)
    cookies = "M5 13A2.3 2.3 0 0 1 9.6 13A2.3 2.3 0 0 1 14.2 13A2.3 2.3 0 0 1 18.8 13Z"
    return [shell(body), shell(behind(cookies, [body], None)), shell(behind(lid, [body, cookies], 1.25)),
            detail(seg(3, 16, 21, 16))]


@icon("candy-cane", CAT, "A hooked striped candy cane",
      tags=["peppermint stick", "christmas", "candy", "sweet", "stripes", "holiday"])
def _(S):
    cen = "M16 20.5V9.75A4.5 4.5 0 0 0 7 9.75V11.5"
    outline = path_to_d(ST(cen, 4.5, L(S, "butt", "round"), "round"))
    parts = [shell(outline)]
    for y in (13, 16.5):
        parts.append(detail(seg(13.75, y + 1.4, 18.25, y - 1.4)))
    (x1, y1), (x2, y2) = pt_on(11.5, 9.75, 2.25, -60), pt_on(11.5, 9.75, 6.75, -60)
    parts.append(detail(seg(x1, y1, x2, y2)))
    (x1, y1), (x2, y2) = pt_on(11.5, 9.75, 2.25, -150), pt_on(11.5, 9.75, 6.75, -150)
    parts.append(detail(seg(x1, y1, x2, y2)))
    return parts


def gummy_bear(S):
    head = circle(12, 7.5, 4.2)
    ears = [circle(8.4, 4.3, 1.9), circle(15.6, 4.3, 1.9)]
    body = ellipse(12, 15, 5.3, 5.2)
    arms = [capsule(6.2, 12.5, 8.5, 14.2, 3), capsule(17.8, 12.5, 15.5, 14.2, 3)]
    if S.name == "rounded":
        feet = [ellipse(8.5, 19.6, 2.5, 1.9), ellipse(15.5, 19.6, 2.5, 1.9)]
    else:
        feet = [rect(6, 17.7, 5, 3.8, 1), rect(13, 17.7, 5, 3.8, 1)]
    return union(head, *ears, body, *arms, *feet)


@icon("gummy-bear", CAT, "A chubby bear-shaped gummy sweet with round ears and short limbs",
      tags=["gummy", "gummies", "jelly bear", "candy", "sweets", "gummi bear"], aliases=["gummi-bear"])
def _(S):
    return [shell(gummy_bear(S)), dot(10.4, 7.3, 0.9), dot(13.6, 7.3, 0.9)]


def _bez(p0, p1, p2, p3, t):
    u = 1 - t
    x = u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0]
    y = u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]
    dx = 3 * u * u * (p1[0] - p0[0]) + 6 * u * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0])
    dy = 3 * u * u * (p1[1] - p0[1]) + 6 * u * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1])
    ln = math.hypot(dx, dy)
    return (x, y), (-dy / ln, dx / ln)


WORM_A = ((5.5, 17), (5.5, 10.5), (10.5, 9), (12, 12.5))
WORM_B = ((12, 12.5), (13.5, 16), (18.5, 14.5), (18.5, 7))


@icon("gummy-worm", CAT, "A wiggly S-shaped gummy worm with bands of colour",
      tags=["gummy", "sour worm", "jelly worm", "candy", "sweets", "gummi worm"], aliases=["gummi-worm"])
def _(S):
    cen = "M{} {}C{} {} {} {} {} {}C{} {} {} {} {} {}".format(*[fmt(v) for p in WORM_A for v in p],
                                                          *[fmt(v) for p in WORM_B[1:] for v in p])
    outline = path_to_d(ST(cen, 5, "round", "round"))
    parts = [shell(outline)]
    for bz, ts in ((WORM_A, (0.3, 0.75)), (WORM_B, (0.25, 0.7))):
        for t in ts:
            (x, y), (nx, ny) = _bez(*bz, t)
            parts.append(detail(seg(x - nx * 2.5, y - ny * 2.5, x + nx * 2.5, y + ny * 2.5)))
    if S.name == "line":
        parts.append(dot(17.4, 6.4, 0.8))
    else:
        parts.append(dot(17.6, 6.8, 0.9))
    return parts


BEAN = ("M-1.4 -2.5C-0.5 -2.5 0.3 -1.7 1.6 -2.5C3.4 -3.1 4.8 -1.8 4.8 0C4.8 2.1 3 3 0 3"
        "C-3 3 -4.8 2.1 -4.8 0C-4.8 -1.7 -3.3 -2.5 -1.4 -2.5Z")


def _bean(deg, dx, dy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return path_to_d(transform_path(P(BEAN), (c, s, -s, c, dx, dy)))


@icon("jelly-bean", CAT, "Three bean-shaped jelly sweets with glossy highlights",
      tags=["jellybeans", "candy", "sweets", "easter candy", "beans", "jelly sweets"])
def _(S):
    beans = [_bean(-25, 8, 7), _bean(20, 16.3, 10.5), _bean(-5, 9.5, 17.8)]
    parts = [shell(b) for b in beans]
    hl = [(-25, 8, 7), (20, 16.3, 10.5), (-5, 9.5, 17.8)]
    for deg, dx, dy in hl:
        a = math.radians(deg)
        c, s = math.cos(a), math.sin(a)
        x0, y0 = L(S, (-2.8, 0.2), (-2.6, 0.4))
        x1, y1 = -1.2, 1.2
        parts.append(detail(seg(dx + x0 * c - y0 * s, dy + x0 * s + y0 * c, dx + x1 * c - y1 * s, dy + x1 * s + y1 * c)))
    return parts


def soften(d, r=1.0):
    """Round the convex corners of a closed outline by r (morphological opening)."""
    inner = D(P(d), ST(d, 2 * r, "round", "round"))
    return path_to_d(U(inner, ST(path_to_d(inner), 2 * r, "round", "round")))


def wedge(cx, cy, r, a0, a1, bend):
    """Curved pinwheel blade from the centre to the rim between angles a0 and a1."""
    (x0, y0), (x1, y1) = pt_on(cx, cy, r, a0), pt_on(cx, cy, r, a1)
    return (f"M{fmt(cx)} {fmt(cy)}A{fmt(bend)} {fmt(bend)} 0 0 1 {fmt(x0)} {fmt(y0)}"
            f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(y1)}A{fmt(bend)} {fmt(bend)} 0 0 0 {fmt(cx)} {fmt(cy)}Z")


# =========================================================================== sweets

def cloud(circles):
    return union(*[circle(*c) for c in circles])


@icon("cotton-candy", CAT, "A fluffy cloud of spun sugar on a paper cone",
      tags=["candy floss", "fairy floss", "fair food", "carnival", "sweet", "spun sugar"], aliases=["candy-floss"])
def _(S):
    fluff = cloud([(7.8, 8.8, 3.6), (12, 6.6, 3.6), (16.2, 8.8, 3.6), (12, 10, 3.6)])
    cone = poly([(8, 11.5), (16, 11.5), (12, 20.5)], closed=True, r=L(S, 0, 1))
    return [shell(fluff), shell(behind(cone, [fluff], 0.6)), detail(arc(12, 8.4, 2.6, 200, 290))]


@icon("cotton-candy-machine", CAT, "A cart with a wide spinning bowl and a cloud of candy floss rising from it",
      tags=["candy floss machine", "fairground", "carnival", "concession stand", "spun sugar", "fair"])
def _(S):
    bowl = "M3 10.5H21C21 13.6 17 15 12 15C7 15 3 13.6 3 10.5Z"
    fluff = cloud([(8.8, 7.5, 2.6), (12, 5.2, 3), (15.2, 7.5, 2.6), (12, 8.5, 2.5)])
    cart = rect(5.5, 17.5, 13, 4, L(S, 1, 2))
    return [shell(bowl), shell(behind(fluff, [bowl], 0.75)), shell(cart), line(seg(12, 15, 12, 17.5))]


APPLE = ("M12 9C10.9 8.3 9.7 8 8.3 8C5.3 8 3.5 10.2 3.5 13.3C3.5 17.3 6.2 21 9 21"
         "C10.3 21 10.8 20.4 12 20.4C13.2 20.4 13.7 21 15 21C17.8 21 20.5 17.3 20.5 13.3"
         "C20.5 10.2 18.7 8 15.7 8C14.3 8 13.1 8.3 12 9Z")


@icon("candy-apple", CAT, "A round apple coated in shiny candy on a stick with a drip pool at its base",
      tags=["toffee apple", "caramel apple", "fair food", "halloween", "sweet", "carnival"], aliases=["toffee-apple"])
def _(S):
    ap = path_to_d(transform_path(P(APPLE), (0.82, 0, 0, 0.82, 12 * 0.18, 14 * 0.18 - 0.3)))
    pool = ellipse(12, 19.8, 8.5, 1.6) if S.name == "rounded" else rect(3.5, 18.3, 17, 3, 1)
    return [shell(ap), shell(behind(pool, [ap], None)), line(seg(12, 9.8, 12, 2.5)),
            detail(arc(12, 14.2, 4.2, 195, 250))]


def _corn_x(y):
    return 12 + (y - 2.5) * 8.5 / 16


@icon("candy-corn", CAT, "A kernel-shaped sweet with three horizontal colour bands",
      tags=["halloween candy", "autumn", "fall", "candy", "sweet", "trick or treat"])
def _(S):
    pts = [(12, 2.5), (20.5, 18.5), (19, 21), (5, 21), (3.5, 18.5)]
    body = poly(pts, closed=True, r=L(S, 0.6, 2.2))
    return [shell(body), detail(seg(24 - _corn_x(9.5), 9.5, _corn_x(9.5), 9.5)),
            detail(seg(24 - _corn_x(15), 15, _corn_x(15), 15))]


def marshmallow_d(S, cx, cy, rx, ry, h):
    """Soft cylinder seen from slightly above: returns (outline, rim arc)."""
    top, bot = cy - h / 2, cy + h / 2
    k = 0.6
    out = (f"M{fmt(cx - rx)} {fmt(top)}C{fmt(cx - rx - k)} {fmt(top + h / 3)} {fmt(cx - rx - k)} {fmt(bot - h / 3)} "
           f"{fmt(cx - rx)} {fmt(bot)}A{fmt(rx)} {fmt(ry)} 0 0 0 {fmt(cx + rx)} {fmt(bot)}"
           f"C{fmt(cx + rx + k)} {fmt(bot - h / 3)} {fmt(cx + rx + k)} {fmt(top + h / 3)} {fmt(cx + rx)} {fmt(top)}"
           f"A{fmt(rx)} {fmt(ry)} 0 0 0 {fmt(cx - rx)} {fmt(top)}Z")
    rim = f"M{fmt(cx - rx)} {fmt(top)}A{fmt(rx)} {fmt(ry)} 0 0 0 {fmt(cx + rx)} {fmt(top)}"
    return out, rim


@icon("marshmallow", CAT, "Two soft cylindrical marshmallows, one standing and one lying on its side",
      tags=["mallow", "campfire", "sweet", "candy", "hot chocolate topping", "smores"])
def _(S):
    face = ellipse(16.5, 15.5, 3.5, 5)
    lying = union(rect(5, 10.5, 11.5, 10, L(S, 2, 4)), face)
    stand, rim = marshmallow_d(S, 9.5, 7, 5, 1.8, 6.5)
    return [shell(behind(stand, [lying], 1.25)), detail(rim), shell(lying), detail(face)]


@icon("roasted-marshmallow", CAT, "A toasted marshmallow on the end of a skewer above a small flame",
      tags=["campfire", "toasted marshmallow", "camping", "smores", "roasting stick", "bonfire"])
def _(S):
    ang = -50
    body = rect(12.5, 3.5, 7.5, 6.5, L(S, 1.5, 2.8))
    m = rotd(body, ang, 16.25, 6.75)
    cap = path_to_d(I(P(m), P(rotd(rect(17.5, 2, 5, 10), ang, 16.25, 6.75))))
    stick = seg(3, 21, 13.8, 9.2)
    flame = ("M17.5 21.5C15.2 21.5 13.5 20 13.5 17.8C13.5 15.8 15 14.8 15.8 12.5"
             "C17.2 13.4 18 14.6 18 16.2C18.7 15.6 19.2 14.8 19.4 13.8"
             "C20.8 15 21.5 16.4 21.5 17.8C21.5 20 19.8 21.5 17.5 21.5Z")
    if S.name == "line":
        flame = ("M17.5 21.5C15.2 21.5 13.5 20 13.5 17.8C13.5 15.8 15 14.8 15.8 12.5"
                 "L18 16.2L19.4 13.8C20.8 15 21.5 16.4 21.5 17.8C21.5 20 19.8 21.5 17.5 21.5Z")
    return [shell(m), Part("dot", cap), line(stick), shell(flame)]


@icon("smore", CAT, "A graham cracker sandwich with chocolate and gooey marshmallow in the middle",
      tags=["smores", "campfire", "graham cracker", "marshmallow", "chocolate", "camping dessert"], aliases=["smores"])
def _(S):
    R = L(S, 1, 2)
    top = rect(3, 3.5, 18, 5.5, R)
    bot = rect(3, 15, 18, 5.5, R)
    goo = ("M4 9H20C21.5 10 21.5 11.5 20.3 12C21.5 12.8 21.3 14.4 20 15H4C2.7 14.4 2.5 12.8 3.7 12"
           "C2.5 11.5 2.5 10 4 9Z")
    body = union(top, bot, goo)
    return [shell(body), detail(seg(3.5, 9, 20.5, 9)), detail(seg(3.5, 15, 20.5, 15)),
            dot(7.5, 6.25, 0.9), dot(12, 6.25, 0.9), dot(16.5, 6.25, 0.9),
            dot(7.5, 17.75, 0.9), dot(12, 17.75, 0.9), dot(16.5, 17.75, 0.9)]


@icon("licorice", CAT, "A twisted rope-like licorice stick with spiral grooves",
      tags=["liquorice", "twist", "candy", "sweet", "red vines", "licorice stick"], aliases=["liquorice"])
def _(S):
    x0, x1, hw, n = 4.5, 19.5, 2.8, 5
    step = (x1 - x0) / n
    top = [(x0 + step * i, 12 - hw) for i in range(n + 1)]
    bot = [(x0 + step * i + step / 2, 12 + hw) for i in range(n)]
    br = step * 0.62
    d = f"M{fmt(x0)} {fmt(12 - hw)}"
    for x, y in top[1:]:
        d += f"A{fmt(br)} {fmt(br)} 0 0 1 {fmt(x)} {fmt(y)}"
    d += f"L{fmt(x1)} {fmt(12 + hw)}" if S.name == "line" else f"A{fmt(hw)} {fmt(hw)} 0 0 1 {fmt(x1)} {fmt(12 + hw)}"
    for x, y in reversed(bot):
        d += f"A{fmt(br)} {fmt(br)} 0 0 1 {fmt(x)} {fmt(y)}"
    d += f"L{fmt(x0)} {fmt(12 + hw)}"
    d += "Z" if S.name == "line" else f"A{fmt(hw)} {fmt(hw)} 0 0 1 {fmt(x0)} {fmt(12 - hw)}Z"
    parts = [shell(rotd(d, -45))]
    for i in range(1, n):
        parts.append(detail(rseg(x0 + step * i, 12 - hw, x0 + step * i - step / 2, 12 + hw, -45)))
    return parts


@icon("gumball-machine", CAT, "A glass globe full of gumballs on a stand with a coin slot",
      tags=["gumball", "candy machine", "vending machine", "bubblegum", "sweets", "dispenser"])
def _(S):
    globe = circle(12, 9.5, 6.8)
    base = poly([(7.5, 15.5), (16.5, 15.5), (18, 21.5), (6, 21.5)], closed=True, r=S.r)
    cap = rect(10, 1.5, 4, 2.5, L(S, 0.5, 1))
    return [shell(behind(globe, [base], None)), shell(base), shell(cap),
            dot(9.5, 8, 1.1), dot(13.5, 7, 1.1), dot(11.5, 11.5, 1.1), dot(15, 11, 1.1),
            detail(seg(10.5, 18.5, 13.5, 18.5))]


@icon("chewing-gum", CAT, "A flat stick of chewing gum pulled halfway out of its wrapper",
      tags=["gum", "gum stick", "bubblegum", "mint", "fresh breath", "wrapper"])
def _(S):
    k = 30
    sleeve = rotd(rect(7, 10, 10, 12, L(S, 1, 2)), k)
    stick = rotd(rect(8.5, 1.5, 7, 12, L(S, 0.8, 1.6)), k)
    return [shell(behind(stick, [sleeve], 0)), shell(sleeve), detail(rseg(7, 13.5, 17, 13.5, k)),
            detail(rseg(7, 18.5, 17, 18.5, k))]


@icon("bubble-gum", CAT, "A big shiny bubble blown from a piece of chewing gum",
      tags=["bubblegum", "gum bubble", "chewing gum", "blow bubble", "candy", "pink"])
def _(S):
    bubble = circle(13, 10, 8)
    piece = rotd(rect(3, 16, 8, 5, L(S, 1, 2.5)), -15, 7, 18.5)
    return [shell(behind(bubble, [piece], 0.9)), shell(piece), detail(arc(13, 10, 5, 200, 250))]


@icon("peppermint-candy", CAT, "A round peppermint sweet with a pinwheel of curved stripes",
      tags=["peppermint", "mint", "starlight mint", "christmas candy", "sweet", "breath mint"])
def _(S):
    parts = [shell(circle(12, 12, 8.8))]
    for k in range(4):
        w = wedge(12, 12, 6.6, -90 + k * 90, -90 + k * 90 + 45, 4.2)
        parts.append(Part("dot", w if S.name == "line" else soften(w, 0.7)))
    return parts


@icon("chocolate-truffle", CAT, "A round cocoa-dusted chocolate ball in a fluted paper cup",
      tags=["truffle", "praline", "bonbon", "chocolate", "confectionery", "sweet"])
def _(S):
    cup = poly([(4.5, 13.5), (19.5, 13.5), (17.5, 21), (6.5, 21)], closed=True, r=S.r)
    ball = circle(12, 9.5, 6.5)
    return [shell(behind(ball, [cup], None)), shell(cup),
            detail(seg(9.5, 13.5, 10, 21)), detail(seg(14.5, 13.5, 14, 21)),
            dot(10, 7.5, 0.8), dot(13.8, 6.8, 0.8), dot(12.5, 10.3, 0.8)]


# =========================================================================== chocolates and confectionery

@icon("chocolate-box", CAT, "An open box of chocolates with round and square pieces in a grid",
      tags=["box of chocolates", "assorted chocolates", "pralines", "gift", "valentine", "confectionery"])
def _(S):
    box = rect(2.5, 9, 19, 12, L(S, 1.5, 3))
    lid = rect(3.5, 3, 17, 10, L(S, 1.5, 3))
    parts = [shell(behind(lid, [box], 0.75)), shell(box)]
    for i, x in enumerate((7, 12, 17)):
        for j, y in enumerate((12.5, 17.5)):
            if (i + j) % 2 == 0:
                parts.append(dot(x, y, 1.75))
            else:
                parts.append(Part("dot", rect(x - 1.6, y - 1.6, 3.2, 3.2, L(S, 0.3, 0.8))))
    return parts


@icon("heart-chocolate", CAT, "A heart-shaped chocolate in crinkled foil with a small gift tag",
      tags=["valentine chocolate", "heart candy", "love", "gift", "foil chocolate", "valentines day"])
def _(S):
    h = heart(10.5, 13.5, 15.5, S.name == "line")
    tag = rotd(rect(16, 2.5, 5.5, 4, L(S, 0.6, 1.2)), 25, 18.75, 4.5)
    return [shell(h), line("M13.2 8.3C14 6.8 15 5.8 16.2 5"), shell(tag),
            detail("M6 11.5C6 10.2 6.8 9.4 8 9.4")]


@icon("chocolate-mold", CAT, "A tray of heart-shaped chocolate moulds with one cavity filled",
      tags=["chocolate mould", "candy mold", "silicone mold", "praline mold", "chocolatier", "baking"],
      aliases=["chocolate-mould"])
def _(S):
    parts = [shell(rect(2.5, 3, 19, 18, L(S, 2, 4)))]
    for k, (x, y) in enumerate(((7.5, 8.2), (16.5, 8.2), (7.5, 16), (16.5, 16))):
        hd = heart(x, y, 5.6, S.name == "line")
        parts.append(Part("dot", heart(x, y, 7.6, S.name == "line")) if k == 3 else detail(hd))
    return parts


@icon("gumdrop", CAT, "A dome-shaped jelly sweet with a flat base coated in sugar",
      tags=["gum drop", "jelly sweet", "sugar coated", "candy", "sweet", "christmas candy"])
def _(S):
    body = ("M3.5 20C3.5 11 7 4.5 12 4.5C17 4.5 20.5 11 20.5 20Z" if S.name == "line" else
            "M5.5 20.5C4.4 20.5 3.5 19.6 3.5 18.5C3.5 10.5 7 4.5 12 4.5C17 4.5 20.5 10.5 20.5 18.5"
            "C20.5 19.6 19.6 20.5 18.5 20.5Z")
    return [shell(body), dot(10, 8.5, 0.9), dot(14.5, 10, 0.9), dot(8.2, 13, 0.9), dot(12, 14.5, 0.9),
            dot(16, 15.5, 0.9), dot(7.5, 17, 0.9)]


@icon("candy-jar", CAT, "A glass sweet jar with a domed lid full of round sweets",
      tags=["sweet jar", "bonbon jar", "apothecary jar", "candy", "sweets", "confectionery"])
def _(S):
    body = rect(4.5, 9.5, 15, 12, L(S, 2, 4))
    lid = "M5 7.5C5 5 8 3.8 12 3.8C16 3.8 19 5 19 7.5Z" if S.name == "rounded" else "M5 7.5L7 4.5H17L19 7.5Z"
    return [shell(body), shell(lid), line(seg(12, 3.8, 12, 1.8)),
            dot(8.3, 17.6, 1.5), dot(12, 18, 1.5), dot(15.7, 17.6, 1.5), dot(10.2, 14, 1.5), dot(14, 13.7, 1.5)]


@icon("chocolate-coin", CAT, "A round chocolate coin embossed with a star and with a bite taken out of its edge",
      tags=["gelt", "chocolate money", "foil coin", "hanukkah", "treasure", "candy coin"])
def _(S):
    cx, cy, r = 12, 12, 9
    bites = [circle(*pt_on(cx, cy, 10, a), 2.6) for a in (-72, -45, -18)]
    coin = path_to_d(D(P(circle(cx, cy, r)), *[P(b) for b in bites]))
    if S.name == "rounded":
        coin = soften(coin, 0.7)
    star = [pt_on(11.5, 12.8, 4.6 if k % 2 == 0 else 2.0, -90 + 36 * k) for k in range(10)]
    return [shell(coin), Part("dot", poly(star, closed=True, r=L(S, 0, 0.4)))]


def bunny_body(S):
    body = ellipse(10.5, 15.5, 6.8, 5.8)
    head = circle(14.5, 9, 3.8)
    ears = [capsule(13.2, 6.5, 11.8, 3, 2.8), capsule(15.8, 6.5, 16.8, 3, 2.8)]
    tail = circle(4.3, 17.5, 1.8)
    base = rect(4, 18.5, 14, 3, L(S, 0.5, 1.5))
    return union(body, head, *ears, tail, base)


@icon("chocolate-bunny", CAT, "A hollow chocolate rabbit sitting upright with long ears and a bow",
      tags=["easter bunny", "chocolate rabbit", "easter", "candy", "spring", "treat"])
def _(S):
    bow = "M11 11.2L13.3 13.8L14.3 11.3L16.6 13.2"
    return [shell(bunny_body(S)), dot(15.6, 8.6, 0.8), detail(bow if S.name == "line" else "M11.2 11.4C12 12.4 12.6 13 13.3 13.5C13.9 12.8 14.3 12 14.5 11.4")]


STRAW = "M12 21C7.5 19.5 4 14.5 4 11C4 9.2 5.2 8.5 7 8.5H17C18.8 8.5 20 9.2 20 11C20 14.5 16.5 19.5 12 21Z"


@icon("chocolate-strawberry", CAT, "A strawberry dipped halfway in chocolate with its leafy top showing",
      tags=["chocolate covered strawberry", "dipped strawberry", "valentine", "dessert", "fondue", "fruit"])
def _(S):
    crown = poly([(7, 8.5), (8.5, 5), (10.5, 6.2), (12, 3), (13.5, 6.2), (15.5, 5), (17, 8.5)], closed=True, r=L(S, 0, 0.6))
    dip = "M3 13.8Q7.5 12.2 12 13.8T21 13.8V22H3Z"
    inner = D(P(STRAW), ST(STRAW, 4, "round", "round"))
    choc = path_to_d(I(inner, P(dip)))
    return [shell(STRAW), shell(crown), detail(seg(7, 8.5, 17, 8.5)), Part("dot", choc),
            dot(9.5, 11, 0.85), dot(14.5, 11, 0.85)]


@icon("sugared-almonds", CAT, "A small tulle pouch tied with a ribbon bow holding sugar-coated almonds",
      tags=["dragees", "jordan almonds", "wedding favor", "bonbonniere", "favour bag", "confetti"],
      aliases=["jordan-almonds"])
def _(S):
    sack = "M8.5 10.5C4 12.5 3.5 21 12 21C20.5 21 20 12.5 15.5 10.5Z"
    frill = poly([(7.5, 3), (16.5, 3), (13.5, 8), (10.5, 8)], closed=True, r=L(S, 0, 0.8))
    tie = poly([(7, 9.5), (12, 9), (17, 9.5)]) if S.name == "line" else "M7 9.8C9 9 15 9 17 9.8"
    parts = [shell(sack), shell(frill), line(tie)]
    for cx, cy, deg in ((8.4, 17.6, -15), (12.2, 18.2, 10), (15.8, 17, -30), (10.4, 14.4, 25), (14.1, 13.9, -10)):
        a = math.radians(deg)
        parts.append(Part("dot", path_to_d(transform_path(P(ellipse(0, 0, 1.7, 1.15)),
                                                          (math.cos(a), math.sin(a), -math.sin(a), math.cos(a), cx, cy)))))
    return parts


@icon("sprinkles", CAT, "A scatter of short rod-shaped sprinkles at different angles",
      tags=["hundreds and thousands", "jimmies", "nonpareils", "cake decoration", "toppings", "baking"])
def _(S):
    rods = [(5, 6, 30), (11.5, 4.5, -40), (18, 6, 70), (7.5, 12, -70), (13.5, 11.5, 15), (19, 13, -35),
            (5, 18.5, 50), (11.5, 18.5, -10), (17.5, 19.5, 40)]
    parts = []
    for x, y, deg in rods:
        dx, dy = 1.6 * math.cos(math.radians(deg)), 1.6 * math.sin(math.radians(deg))
        parts.append(line(seg(x - dx, y - dy, x + dx, y + dy)))
    return parts


@icon("peanut-brittle", CAT, "An irregular shard of hard caramel with whole peanuts set in it",
      tags=["brittle", "nut brittle", "praline", "toffee", "candy", "chikki"])
def _(S):
    pts = [(3, 9), (9, 4.5), (14, 6.5), (21, 4), (19.5, 12), (21, 19), (13, 20.5), (7, 18.5), (3.5, 15)]
    parts = [shell(poly(pts, closed=True, r=S.r))]
    for cx, cy, deg in ((8.5, 9.5, -20), (14.5, 10.5, 30), (8.5, 14.5, 15), (14.5, 16, -25)):
        a = math.radians(deg)
        parts.append(Part("dot", path_to_d(transform_path(P(ellipse(0, 0, 2.1, 1.4)),
                                                          (math.cos(a), math.sin(a), -math.sin(a), math.cos(a), cx, cy)))))
    return parts


def maple_leaf(cx, cy, s):
    pts = [(0, -3), (0.8, -1.6), (2, -2.2), (1.7, -0.5), (3, 0), (1.9, 0.8), (2.1, 2), (0.4, 1.6), (0, 3),
           (-0.4, 1.6), (-2.1, 2), (-1.9, 0.8), (-3, 0), (-1.7, -0.5), (-2, -2.2), (-0.8, -1.6)]
    return poly([(cx + x * s, cy + y * s) for x, y in pts], closed=True)


@icon("maple-syrup", CAT, "A glass jug of maple syrup with a small finger loop and a maple leaf label",
      tags=["maple", "syrup", "pancake syrup", "canada", "breakfast", "sweetener"])
def _(S):
    body = poly([(9.5, 6), (6, 9.5), (5, 13), (5, 21), (19, 21), (19, 13), (18, 9.5), (14.5, 6)], closed=True, r=S.r)
    neck = rect(9.5, 2.5, 5, 3.5, L(S, 0.5, 1))
    return [shell(body), shell(neck), line(arc(17.8, 6.8, 2.2, 150, 390)),
            Part("dot", maple_leaf(12, 15, 1.35 if S.name == "line" else 1.3))]


@icon("honey-dipper", CAT, "A wooden honey dipper with a grooved head dripping a thick drop",
      tags=["honey stick", "honey spoon", "honey wand", "drizzle", "bee", "sweet"])
def _(S):
    k = 35
    head = rotd(rect(3.5, 9, 7.5, 8.5, L(S, 1.5, 3.5)), k, 7.25, 13.25)
    grooves = [rseg(3.5, y, 11, y, k, 7.25, 13.25) for y in (11.3, 13.25, 15.2)]
    handle = rseg(7.25, 9, 7.25, 1, k, 7.25, 13.25)
    drop = "M5.5 16.5C4.8 17.8 4 19 4 20A1.5 1.5 0 0 0 7 20C7 19 6.2 17.8 5.5 16.5Z"
    return [shell(head), *[detail(g) for g in grooves], line(handle)] + [shell(drop)]


# =========================================================================== milk and butter

def crown(x0, x1, y, h, n=3):
    """Splash crown sitting on y between x0 and x1 with n prongs."""
    pts = [(x0, y)]
    w = (x1 - x0) / (2 * n)
    for i in range(n):
        tall = h if i == n // 2 else h * 0.7
        pts.append((x0 + w * (2 * i + 1), y - tall))
        pts.append((x0 + w * (2 * i + 2), y - h * 0.3) if i < n - 1 else (x1, y))
    return pts


@icon("milk-glass", CAT, "A glass of milk with a small splash rising from the top",
      tags=["glass of milk", "milk", "dairy", "drink", "calcium", "breakfast"])
def _(S):
    glass = poly([(5, 3.5), (19, 3.5), (17.5, 20.5), (6.5, 20.5)], closed=True, r=S.r)
    inner = D(P(glass), ST(glass, 4, "round", "round"))
    level = "M0 8.5H9.5C10.3 8.5 10.6 7.8 11 7C11.4 7.8 11.7 8.5 12.5 8.5H24V24H0Z"
    milk = D(I(inner, P(level)), ST("M8.5 12.5L9 17", 4, "round", "round"))
    return [shell(glass), Part("dot", path_to_d(milk)), dot(15.5, 6.3, 0.8)]


@icon("milk-pail", CAT, "A metal milking pail with a wire handle and a drop of milk on its side",
      tags=["milk bucket", "milking", "dairy farm", "pail", "farm", "fresh milk"])
def _(S):
    pail = poly([(5, 9), (19, 9), (17.5, 21), (6.5, 21)], closed=True, r=S.r)
    return [shell(pail), detail(seg(5.4, 12, 18.6, 12)), line("M4.5 9.5C4.5 2.5 19.5 2.5 19.5 9.5"),
            detail("M12 13.8C13.4 15.5 14.1 16.6 14.1 17.4A2.1 2.1 0 0 1 9.9 17.4C9.9 16.6 10.6 15.5 12 13.8Z")]


@icon("dairy-products", CAT, "A milk bottle, a yogurt cup and a wedge of cheese standing together",
      tags=["dairy", "milk", "cheese", "yogurt", "grocery", "lactose"])
def _(S):
    bottle = poly([(4.5, 2.5), (9.5, 2.5), (9.5, 6), (11, 9), (11, 21), (3, 21), (3, 9), (4.5, 6)], closed=True, r=S.r)
    wedge = poly([(9.5, 21), (9.5, 15.5), (21.5, 11.5), (21.5, 21)], closed=True, r=S.r)
    cup = poly([(13, 4), (20.5, 4), (19.8, 10), (13.7, 10)], closed=True, r=S.r)
    return [shell(behind(bottle, [wedge], 1)), detail(seg(3.5, 9, 10.5, 9)), shell(cup),
            detail(seg(13, 6.2, 20.5, 6.2)), shell(wedge), dot(13.5, 17.5, 1.1), dot(17.8, 15.8, 1.1)]


@icon("butter", CAT, "A block of butter with its paper wrapper folded back from one end",
      tags=["butter block", "stick of butter", "margarine", "dairy", "baking", "spread"])
def _(S):
    out = poly([(2.5, 10), (6, 6.5), (21.5, 6.5), (21.5, 14.5), (18, 18), (2.5, 18)], closed=True, r=S.r)
    edges = poly([(2.5, 10), (18, 10), (21.5, 6.5)], r=0)
    edge2 = seg(18, 10, 18, 18)
    return [shell(out), detail(edges), detail(edge2), detail(poly([(7, 10), (8, 12), (7, 14), (8, 16), (7, 18)], r=L(S, 0, 0.5))),
            detail(seg(10.5, 6.5, 7, 10))]


@icon("butter-dish", CAT, "A covered butter dish with its domed lid lifted to show the butter",
      tags=["butter tray", "butter keeper", "tableware", "dairy", "kitchen", "breakfast"])
def _(S):
    plate = rect(2.5, 18.5, 19, 3, L(S, 1, 1.5))
    block = rect(6.5, 12.5, 11, 6, L(S, 0.5, 1.5))
    lid = rotd("M4 9.5C4 6 7.5 4.5 12 4.5C16.5 4.5 20 6 20 9.5Z" if S.name == "rounded" else
               "M4 9.5V7L6.5 4.5H17.5L20 7V9.5Z", -6, 12, 7, 0, 0)
    knob = rotd(rect(10.5, 2.5, 3, 2, 0.5), -6, 12, 7, 0, 0)
    return [shell(plate), shell(behind(block, [plate], None)), shell(lid), shell(knob)]


@icon("butter-churn", CAT, "A tall wooden butter churn with metal bands and a plunger handle",
      tags=["churn", "dasher churn", "farmhouse", "dairy", "old fashioned", "homestead"])
def _(S):
    body = poly([(6.5, 8), (17.5, 8), (19, 21), (5, 21)], closed=True, r=S.r)
    lid = rect(5.5, 6, 13, 2, L(S, 0.5, 1))
    return [shell(body), shell(lid), detail(seg(6.1, 11.5, 17.9, 11.5)), detail(seg(5.4, 17.5, 18.6, 17.5)),
            line(seg(12, 6, 12, 2)), line(seg(9, 2, 15, 2))]


@icon("yogurt", CAT, "A short cup of yogurt with its foil lid peeled back and a spoon",
      tags=["yoghurt", "yogurt cup", "dairy", "snack", "probiotic", "breakfast"], aliases=["yoghurt"])
def _(S):
    cup = poly([(4.5, 10), (19.5, 10), (18, 21), (6, 21)], closed=True, r=S.r)
    flap = poly([(5, 9.5), (3.5, 4), (10, 3), (11.5, 9.5)], closed=True, r=L(S, 0, 0.8))
    spoon = seg(14, 9.5, 19.5, 2.5)
    return [shell(behind(flap, [cup], 0.5)), shell(cup), line(spoon),
            detail(seg(4.9, 13, 19.1, 13))]


@icon("whipped-cream", CAT, "An aerosol can of whipped cream with a swirl of cream on the nozzle",
      tags=["squirty cream", "cream", "dessert topping", "aerosol", "dairy", "chantilly"])
def _(S):
    can = union(rect(7, 12, 10, 9.5, L(S, 1, 2)),
                poly([(7.5, 12.5), (16.5, 12.5), (14, 9.5), (10, 9.5)], closed=True, r=L(S, 0, 0.6)))
    if S.name == "rounded":
        cream = union(capsule(8.25, 6.5, 15.75, 6.5, 2.5), capsule(9.75, 4.5, 14.25, 4.5, 2.5),
                      "M10.5 4L12.2 1.8C13 2.3 13.5 3 13.5 4Z")
    else:
        cream = union(rect(7, 5.25, 10, 2.5, 0.5), rect(8.5, 3.25, 7, 2.5, 0.5), poly([(10.5, 3.5), (12.5, 1.5), (13.5, 3.5)], closed=True))
    return [shell(can), detail(seg(7, 12.5, 17, 12.5)), detail(seg(7, 16.5, 17, 16.5)), shell(cream),
            line(seg(12, 9.5, 12, 7.75))]


# =========================================================================== cheese

def _ellpt(cx, cy, rx, ry, deg):
    a = math.radians(deg)
    return cx + rx * math.cos(a), cy + ry * math.sin(a)


@icon("cheese-wheel", CAT, "A whole round cheese drum with a wedge cut out of the front",
      tags=["cheese round", "wheel of cheese", "gouda", "parmesan", "dairy", "cheesemonger"])
def _(S):
    cx, cy, rx, ry, h = 12, 8, 9, 3.5, 8
    p1, p2 = _ellpt(cx, cy, rx, ry, 10), _ellpt(cx, cy, rx, ry, 80)
    p1b, p2b = (p1[0], p1[1] + h), (p2[0], p2[1] + h)
    out = (f"M3 {fmt(cy)}A{rx} {ry} 0 0 1 {fmt(p1[0])} {fmt(p1[1])}L{fmt(p1b[0])} {fmt(p1b[1])}"
           f"L{fmt(cx)} {fmt(cy + h)}L{fmt(p2b[0])} {fmt(p2b[1])}A{rx} {ry} 0 0 1 3 {fmt(cy + h)}Z")
    return [shell(out if S.name == "line" else soften(out, 0.8)),
            detail(f"M3 {fmt(cy)}A{rx} {ry} 0 0 0 {fmt(p2[0])} {fmt(p2[1])}L{fmt(cx)} {fmt(cy)}L{fmt(p1[0])} {fmt(p1[1])}"),
            detail(seg(cx, cy, cx, cy + h)), detail(seg(p2[0], p2[1], p2b[0], p2b[1])),
            dot(16.3, 12.8, 0.9), dot(8, 14.5, 1)]


@icon("cheese-block", CAT, "A rectangular block of hard cheese with a thin slice falling from the end",
      tags=["cheddar", "block of cheese", "cheese slice", "dairy", "deli", "hard cheese"])
def _(S):
    out = poly([(2.5, 10), (6.5, 6), (16, 6), (16, 15), (12, 19), (2.5, 19)], closed=True, r=S.r)
    sl = rotd(poly([(12, 10), (16, 6), (16, 15), (12, 19)], closed=True, r=S.r), 14, 14, 12.5, 5.2, 0.4)
    return [shell(out), detail(poly([(2.5, 10), (12, 10), (16, 6)], r=0)), detail(seg(12, 10, 12, 19)),
            shell(sl), dot(6, 14, 1.3), dot(9.6, 16.4, 0.8)]


@icon("brie", CAT, "A wedge of soft cheese with a thin rind and its creamy centre bulging out",
      tags=["camembert", "soft cheese", "french cheese", "rind", "cheese board", "dairy"])
def _(S):
    # a flat wedge in three-quarter view: the cut top face, the front face and the curved rind at the back,
    # with the soft centre bulging out of the front face
    out = ("M2.5 15.5L14 7Q19.5 6 21.5 10V14L13 16.6"
           "C13 19.2 12.2 20.5 11 20.5C9.8 20.5 9.4 19.3 9.4 17.7L2.5 19.5Z")
    top = seg(2.5, 15.5, 21.5, 10)
    rind = "M11.3 9Q16.5 8.2 18 10.9"
    if S.name == "rounded":
        out = soften(out, 0.9)
    return [shell(out), detail(top), detail(rind)]


@icon("camembert", CAT, "A round wooden cheese box with its lid tilted open over a soft cheese",
      tags=["cheese box", "soft cheese", "french cheese", "brie", "baked camembert", "dairy"])
def _(S):
    box = "M3 14V17.5A9 3 0 0 0 21 17.5V14A9 3 0 0 0 3 14Z"
    rim = "M3 14A9 3 0 0 0 21 14"
    lid = rotd("M3 6.5V8.5A9 3 0 0 0 21 8.5V6.5A9 3 0 0 0 3 6.5Z", -14, 12, 7.5, 0, -0.8)
    return [shell(box), detail(rim), shell(behind(lid, [box], 0.9)), detail("M8 14.2A4.5 1.4 0 0 1 16 14.2")]


@icon("mozzarella", CAT, "A smooth ball of fresh mozzarella sitting in a bowl of liquid",
      tags=["fresh mozzarella", "bocconcini", "italian cheese", "caprese", "dairy", "soft cheese"])
def _(S):
    bowl = "M2.5 13H21.5C21.5 18 17.5 21 12 21C6.5 21 2.5 18 2.5 13Z"
    ball = circle(12, 9, 6)
    return [shell(behind(ball, [bowl], None)), shell(bowl),
            detail(f"M3.3 16Q5.5 14.8 7.7 16T12 16T16.3 16T20.7 16"), detail(arc(12, 9, 3.4, 200, 260))]


@icon("burrata", CAT, "A round pouch of cheese tied in a knot on top and torn open to show a creamy centre",
      tags=["burrata", "stracciatella", "italian cheese", "fresh cheese", "mozzarella", "dairy"])
def _(S):
    ball = circle(12, 13.5, 7.5)
    knot = ("M12 6.5L9 3.2C10 2.7 11 3 12 4C13 3 14 2.7 15 3.2Z" if S.name == "rounded" else
            "M12 6.5L9 3L12 4.2L15 3Z")
    tear = poly([(7.5, 14.5), (10, 13), (12.5, 14.5), (14.5, 13), (16.5, 14.5), (15, 18), (9, 18)], closed=True,
                r=L(S, 0, 0.8))
    return [shell(union(ball, knot)), Part("dot", tear)]


@icon("string-cheese", CAT, "A stick of cheese with thin strings peeling away from the top",
      tags=["cheese stick", "mozzarella stick", "snack cheese", "lunchbox", "dairy", "peel"])
def _(S):
    stick = rect(8.5, 10, 7, 11.5, L(S, 1.5, 3.5))
    return [shell(stick), line("M10.3 10C9.8 7 7.5 5.6 4.5 5"), line("M13.7 10C14.2 7.5 15.8 5 18.5 3.5"),
            line("M12 10C12 7.5 11.2 5 11.8 2.5")]


@icon("cheese-slice", CAT, "A square slice of cheese with a few holes and one corner curling up",
      tags=["slice of cheese", "sandwich cheese", "processed cheese", "swiss cheese", "dairy", "burger"])
def _(S):
    out = poly([(3, 3), (14, 3), (21, 10), (21, 21), (3, 21)], closed=True, r=L(S, 0, 1.5))
    if S.name == "rounded":
        out = soften(out, 1.5)
        curl = "M14 3.4L20.6 10C17 10.2 14.2 8 14 3.4Z"
    else:
        curl = "M14 3L21 10H16Q14 10 14 8Z"
    return [shell(out), shell(curl), dot(8, 8.5, 1.6), dot(8.5, 15.5, 1.2), dot(15, 15.5, 1.8)]


@icon("blue-cheese", CAT, "A wedge of cheese with branching blue veins running across its cut face",
      tags=["gorgonzola", "roquefort", "stilton", "veined cheese", "mould cheese", "dairy"])
def _(S):
    out = poly([(2.5, 11), (21.5, 3.5), (21.5, 20.5), (2.5, 20.5)], closed=True, r=S.r)
    return [shell(out), detail(seg(2.5, 11, 21.5, 11) if S.name == "line" else "M2.5 11H21.5"),
            detail(poly([(5.5, 17.5), (9, 14.5), (12.5, 16.5), (16.5, 14), (19, 17)], r=L(S, 0, 1))),
            detail(poly([(14.5, 8.6), (18.5, 7.5)], r=0))]


@icon("cheese-board", CAT, "A wooden serving board with a handle holding a cheese wedge and a bunch of grapes",
      tags=["charcuterie", "cheese platter", "grazing board", "party", "wine and cheese", "serving board"])
def _(S):
    board = union(rect(2.5, 16.5, 17, 4, L(S, 0.5, 1.5)), rect(18, 17.25, 3.5, 2.5, L(S, 0.5, 1.25)))
    wedge = poly([(3.5, 16.5), (11.5, 16.5), (11.5, 8)], closed=True, r=L(S, 0, 1))
    grapes = union(circle(14.6, 14.6, 1.9), circle(18, 14.6, 1.9), circle(16.3, 11.6, 1.9))
    return [shell(board), shell(behind(wedge, [board], None)), shell(behind(grapes, [board], None)),
            dot(9, 14, 1.1)]


@icon("cheese-knife", CAT, "A short cheese knife with holes along the blade and a forked tip",
      tags=["cheese knife", "fork tip", "cheese cutter", "cutlery", "cheese board", "utensil"])
def _(S):
    blade = [(9.5, 14), (9.5, 4.5), (10.5, 2.5), (12, 4.8), (13.5, 2.5), (14.5, 4.5), (14.5, 14)]
    handle = rect(10, 14.5, 4, 7.5, L(S, 1, 2))
    blade = rotd(poly(blade, closed=True, r=L(S, 0, 0.6)), 40)
    handle = rotd(handle, 40)
    h1, h2 = rot_pts([(12, 8), (12, 11.5)], 40)
    return [shell(blade), shell(handle), dot(*h1, 1.2), dot(*h2, 1.2)]


@icon("cheese-plane", CAT, "A cheese plane: a flat spade-shaped slicer with a slot blade and a short handle",
      tags=["cheese slicer", "cheese shaver", "slicer", "kitchen tool", "scandinavian", "utensil"])
def _(S):
    head = poly([(6.5, 3), (17.5, 3), (16.5, 9.5), (13.5, 12.5), (10.5, 12.5), (7.5, 9.5)], closed=True, r=S.r)
    handle = rect(10.5, 12.5, 3, 8, L(S, 0.5, 1.5))
    return [shell(rotd(head, 40)), shell(rotd(handle, 40)), detail(rseg(9.3, 6.7, 14.7, 6.7, 40))]


# =========================================================================== eggs

EGG_D = "M12 3C16 3 19 9.5 19 14C19 18.5 16 21 12 21C8 21 5 18.5 5 14C5 9.5 8 3 12 3Z"


def egg_at(cx, cy, s=1.0, deg=0.0):
    """The egg outline scaled by s around its centre (12, 12), rotated and moved to (cx, cy)."""
    a = math.radians(deg)
    c, n = math.cos(a) * s, math.sin(a) * s
    return path_to_d(transform_path(P(EGG_D), (c, n, -n, c, cx - 12 * c + 12 * n, cy - 12 * n - 12 * c)))


def fried_white(S):
    pts = [(12, 3), (16.5, 4), (20.5, 7.5), (20.5, 12.5), (18.5, 16), (19.5, 19.5), (15, 21), (10, 19.5),
           (6, 20.5), (3, 17), (4, 12.5), (3, 8), (7, 4.5)]
    return spline(pts, 0.5 if S.name == "rounded" else 0.32)


def spline(pts, t=0.5):
    """Closed smooth curve through pts (Catmull-Rom as cubic Beziers)."""
    n = len(pts)
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d + "Z"


@icon("fried-egg", CAT, "A fried egg from above with a wavy white and a round yolk",
      tags=["sunny side up", "egg", "breakfast", "brunch", "frying", "yolk"])
def _(S):
    return [shell(fried_white(S)), detail(circle(11.5, 12, 3.8)),
            detail(arc(11.5, 12, 1.6, 180, 270)) if S.name == "rounded" else dot(10.3, 10.8, 0.9)]


@icon("boiled-egg", CAT, "A hard-boiled egg cut in half lengthwise showing its round yolk",
      tags=["hard boiled egg", "egg half", "halved egg", "egg", "breakfast", "protein"])
def _(S):
    yolk = circle(12, 14, 3.8)
    return [shell(EGG_D), Part("dot", yolk) if S.name == "rounded" else detail(yolk)]


@icon("cracked-egg", CAT, "An egg broken into two jagged shell halves with the yolk dropping out between them",
      tags=["crack an egg", "broken egg", "baking", "cooking", "yolk", "recipe"])
def _(S):
    teeth = [(-4.5, 0), (-3, -1.6), (-1.5, 0), (0, -1.6), (1.5, 0), (3, -1.6), (4.5, 0)]
    half = poly(teeth, r=L(S, 0, 0.4)) + "A4.5 5 0 0 1 -4.5 0Z"

    def place(cx, cy, deg):
        a = math.radians(deg)
        c, n = math.cos(a), math.sin(a)
        return path_to_d(transform_path(P(half), (c, n, -n, c, cx, cy)))
    return [shell(place(6.5, 6, 145)), shell(place(17.5, 6, -145)), shell(circle(12, 17.5, 3.8))]


@icon("quail-egg", CAT, "A small egg covered in dark irregular speckles",
      tags=["speckled egg", "quail", "tiny egg", "egg", "delicacy", "spotted egg"])
def _(S):
    sp = [(9.5, 8.5, 1.2), (14, 7.5, 0.9), (8, 13.5, 1.4), (12.5, 12, 1.2), (15.8, 14.5, 1.3), (10.5, 17.5, 1.1),
          (14.5, 18.5, 0.9)]
    if S.name == "rounded":
        marks = [dot(x, y, r) for x, y, r in sp]
    else:
        marks = [Part("dot", poly(regular(x, y, r * 1.2, 5, -90 + 20 * i), closed=True)) for i, (x, y, r) in enumerate(sp)]
    return [shell(EGG_D), *marks]


@icon("egg-carton", CAT, "An open egg carton tray with a row of eggs sitting in its domed cups",
      tags=["egg box", "dozen eggs", "eggs", "grocery", "carton", "farm fresh"])
def _(S):
    tray = ("M2.5 14H21.5V16.5A3.17 3.17 0 0 1 15.17 16.5A3.17 3.17 0 0 1 8.83 16.5A3.17 3.17 0 0 1 2.5 16.5Z")
    if S.name == "line":
        tray = poly([(2.5, 14), (21.5, 14), (21.5, 16.5), (19.5, 19.5), (17, 19.5), (15.17, 16.5), (13.5, 19.5),
                     (10.5, 19.5), (8.83, 16.5), (7, 19.5), (4.5, 19.5), (2.5, 16.5)], closed=True)
    mid = ellipse(12, 10.5, 3.2, 4)
    left, right = ellipse(5.5, 11, 3.1, 3.8), ellipse(18.5, 11, 3.1, 3.8)
    lid = poly([(2.5, 7.5), (4, 3), (20, 3), (21.5, 7.5)], closed=True, r=L(S, 0, 1))
    eggs = [behind(mid, [tray], 1.0), behind(left, [tray, mid], 1.0), behind(right, [tray, mid], 1.0)]
    return [shell(tray)] + [shell(e) for e in eggs]


@icon("egg-basket", CAT, "A wire basket with a tall handle holding a heap of eggs",
      tags=["basket of eggs", "egg collecting", "farm", "eggs", "easter", "hen house"])
def _(S):
    basket = poly([(3, 12.5), (21, 12.5), (18.5, 21), (5.5, 21)], closed=True, r=S.r)
    eggs = union(ellipse(8.6, 10.5, 2.4, 3), ellipse(12, 9.5, 2.5, 3.2), ellipse(15.4, 10.5, 2.4, 3))
    return [shell(behind(eggs, [basket], None)), shell(basket), line("M3.5 12.5C3.5 0.5 20.5 0.5 20.5 12.5"),
            detail(seg(4.3, 16.5, 19.7, 16.5)), detail(seg(9.5, 12.5, 10, 21)), detail(seg(14.5, 12.5, 14, 21))]


@icon("egg-cup", CAT, "A footed egg cup holding a whole upright egg",
      tags=["egg holder", "soft boiled egg", "breakfast", "egg", "tableware", "dippy egg"])
def _(S):
    cup = union("M5.5 12.5H18.5A6.5 5 0 0 1 5.5 12.5Z",
                poly([(10.5, 16.5), (13.5, 16.5), (14, 19), (16.5, 21.5), (7.5, 21.5), (10, 19)], closed=True, r=S.r * 0.5))
    egg = egg_at(12, 8.2, 0.62)
    return [shell(behind(egg, [cup], None)), shell(cup)]


# =========================================================================== spreads and more sweets

@icon("peanut-butter", CAT, "A wide jar of peanut butter with a peanut on the label and a spreading knife",
      tags=["pb", "nut butter", "spread", "sandwich", "peanut", "jar"])
def _(S):
    jar = rect(2.5, 8.5, 13, 13, L(S, 1.5, 3))
    lid = rect(3.5, 4, 11, 3.5, L(S, 0.5, 1.2))
    nut = union(ellipse(7.3, 12.7, 2.2, 2.4), ellipse(10.7, 17.3, 2.2, 2.4), capsule(7.3, 12.7, 10.7, 17.3, 3))
    knife = union(rect(18.5, 3, 3, 10.5, L(S, 0.5, 1.5)), rect(18.8, 14, 2.4, 7.5, L(S, 0.5, 1.2)))
    return [shell(jar), shell(lid), Part("dot", nut), shell(knife), detail(seg(18.5, 13.8, 21.5, 13.8))]


def hex_pts(cx, cy, r):
    return regular(cx, cy, r, 6, -90)


@icon("honeycomb", CAT, "A cluster of hexagonal wax cells with honey dripping from one of them",
      tags=["honey comb", "beeswax", "bee", "honey", "hive", "hexagon"])
def _(S):
    r = 4.6
    w = r * math.sqrt(3)
    cs = [(12 - w / 2, 6.9), (12 + w / 2, 6.9), (12, 6.9 + 1.5 * r)]
    cells = [poly(hex_pts(x, y, r), closed=True, r=L(S, 0, 0.8)) for x, y in cs]
    out = union(*cells)
    x, y = cs[2]
    drip = f"M{fmt(x - 1.4)} {fmt(y + r - 0.8)}V19.8A1.4 1.4 0 0 0 {fmt(x + 1.4)} 19.8V{fmt(y + r - 0.8)}Z"
    inner = [detail(seg(12, 6.9 - r / 2 + 0.2, 12, 6.9 + r / 2)),
             detail(poly([(12 - w, 6.9 + r / 2), (12 - w / 2, 6.9 + r), (12, 6.9 + r / 2), (12 + w / 2, 6.9 + r), (12 + w, 6.9 + r / 2)], r=0))]
    return [shell(union(out, drip)), *inner, Part("dot", poly(hex_pts(x, y, r - 2.2), closed=True))]


# =========================================================================== last sweets, cheese and eggs

@icon("rock-candy", CAT, "A cluster of pointed sugar crystals growing on a wooden stick",
      tags=["sugar crystals", "crystal candy", "rock sugar", "swizzle stick", "sweet", "candy"])
def _(S):
    col = [(9.5, 15.5), (9.5, 7.5), (12, 3.5), (14.5, 7.5), (14.5, 15.5)]
    mid = poly(col, closed=True, r=S.r)
    left = rotd(poly([(6.5, 15.5), (6.5, 8.5), (9, 4.5), (11.5, 8.5), (11.5, 15.5)], closed=True, r=S.r), -28, 9, 15.5)
    right = rotd(poly([(12.5, 15.5), (12.5, 8.5), (15, 4.5), (17.5, 8.5), (17.5, 15.5)], closed=True, r=S.r), 28, 15, 15.5)
    return [shell(union(mid, left, right)), line(seg(12, 15.5, 12, 21.5))]


@icon("fudge", CAT, "Three square pieces of fudge stacked in a small pyramid",
      tags=["chocolate fudge", "toffee", "dessert", "candy", "confection", "sweet squares"])
def _(S):
    out = poly([(7.5, 3.5), (16.5, 3.5), (16.5, 11.5), (21.5, 11.5), (21.5, 21.5), (2.5, 21.5), (2.5, 11.5), (7.5, 11.5)],
               closed=True, r=S.r)
    return [shell(out), detail(seg(7.5, 11.5, 16.5, 11.5)), detail(seg(12, 11.5, 12, 21.5))]


@icon("sugar-cube", CAT, "Two sugar cubes in three-quarter view, one behind the other, with a few loose grains",
      tags=["sugar lump", "sugar", "sweetener", "tea", "coffee", "cubes"])
def _(S):
    r = 5.3

    def cube(cx, cy):
        hexa = poly(regular(cx, cy, r, 6, -90), closed=True, r=S.r)
        (lx, ly), (rx, ry) = pt_on(cx, cy, r, 210), pt_on(cx, cy, r, -30)
        return hexa, [detail(poly([(lx, ly), (cx, cy), (rx, ry)], r=0)), detail(seg(cx, cy, cx, cy + r))]
    a, da = cube(8.6, 15.5)
    b, db = cube(14.8, 9.2)
    return [shell(a), *da, shell(behind(b, [a], None)), *db, dot(18, 19, 0.9), dot(21, 16, 0.8)]


@icon("candy-wrapper", CAT, "An empty crinkled candy wrapper with twisted fan ends and a creased flat middle",
      tags=["wrapper", "sweet wrapper", "litter", "toffee wrapper", "bonbon", "foil"])
def _(S):
    mid = rect(7.5, 7, 9, 10, L(S, 0, 1))
    left = poly([(7.5, 8.5), (2.5, 5.5), (4.2, 12), (2.5, 18.5), (7.5, 15.5)], closed=True, r=S.r)
    right = poly([(16.5, 8.5), (21.5, 5.5), (19.8, 12), (21.5, 18.5), (16.5, 15.5)], closed=True, r=S.r)
    return [shell(union(mid, left, right)), detail(poly([(10, 9.5), (13.5, 12), (10.5, 14.5)], r=0))]


@icon("goat-cheese", CAT, "A short log of soft goat cheese with one round slice cut from the end",
      tags=["chevre", "cheese log", "fresh cheese", "soft cheese", "dairy", "deli"])
def _(S):
    rx = L(S, 1.7, 2.3)
    x0, x1, t, b = 4.5, 11.5, 6.5, 17.5
    body = (f"M{fmt(x0)} {t}H{fmt(x1)}A{fmt(rx)} 5.5 0 0 1 {fmt(x1)} {b}H{fmt(x0)}A{fmt(rx)} 5.5 0 0 1 {fmt(x0)} {t}Z")
    face = f"M{fmt(x1)} {t}A{fmt(rx)} 5.5 0 0 0 {fmt(x1)} {b}"
    sl = ellipse(19.3, 12, L(S, 1.8, 2.2), 5.5)
    return [shell(body), detail(face), shell(sl)]


@icon("cheese-cubes", CAT, "Three small cheese cubes each speared on a cocktail pick",
      tags=["cheese bites", "cocktail sticks", "toothpicks", "appetizer", "party food", "cubed cheese"])
def _(S):
    rc = L(S, 0.5, 1.2)
    out = []
    for cx, top, tilt in ((5.25, 14.5, -14), (12, 8, 0), (18.75, 14.5, 14)):
        cube = rect(cx - 2.75, top, 5.5, 5.5, rc)
        x0, y0 = rot_pts([(cx, top)], tilt, cx, top + 2.75)[0]
        x1, y1 = rot_pts([(cx, top - 4.2)], tilt, cx, top + 2.75)[0]
        out += [shell(cube), line(seg(x0, y0, x1, y1)), dot(x1, y1 - 0.6, 1.2)]
    return out


@icon("cheese-pull", CAT, "A wedge of melted cheese lifted up with long stretchy strands hanging below",
      tags=["melted cheese", "stretchy cheese", "pizza", "gooey", "fondue", "mozzarella sticks"])
def _(S):
    wedge = poly([(2.5, 11), (21.5, 3), (21.5, 11.5)], closed=True, r=S.r)
    out = [shell(wedge), dot(16.5, 8.4, 0.9)]
    for x, y, ln in ((8, 11.4, 19.5), (13.5, 11.4, 20), (18.5, 11.6, 18.5)):
        out.append(line(f"M{fmt(x)} {fmt(y + 0.3)}C{fmt(x + 2) } {fmt(y + 3)} {fmt(x - 2)} {fmt(y + 5)} {fmt(x)} {fmt(ln)}"))
        out.append(dot(x, ln + 0.4, 1.1))
    return out


@icon("omelet", CAT, "A folded half-moon omelet on a round plate with a sprinkle of herbs",
      tags=["omelette", "folded eggs", "breakfast", "egg dish", "brunch", "plate"])
def _(S):
    om = "M5.5 14.5A6.5 7.5 0 0 1 18.5 14.5Q12 17.8 5.5 14.5Z"
    if S.name == "rounded":
        om = soften(om, 1.3)
    return [line(circle(12, 12, 9.5)), shell(om), dot(9.5, 11.6, 0.8), dot(13, 10.6, 0.8), dot(15, 13, 0.8), dot(11.3, 13.3, 0.7)]
