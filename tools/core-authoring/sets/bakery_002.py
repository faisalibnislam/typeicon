"""TypeIcon Core: bakery (batch 002): cakes, desserts, frozen treats and cookies.

Drawn from the objects themselves. Cakes and slabs use a simple oblique view (front face plus a top face
pushed up and to the right) so every block reads as a solid at 24 px; round things are seen from the side.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "bakery"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def behind(back_d, fronts, gap=1.0):
    """Outline of the part of back_d not hidden by the front shapes, kept `gap` px clear of their strokes
    (gap 0: the strokes just touch)."""
    cut = U(*[U(P(f), ST(f, 2 * (gap + 2), "round", "round")) for f in fronts])
    return path_to_d(D(P(back_d), cut))


def soften(d, r):
    """Round the convex corners of a closed outline with radius r (erode, then grow back)."""
    reg = P(d)
    eroded = D(reg, ST(d, 2 * r, "butt", "miter", 20))
    ed = path_to_d(eroded)
    return path_to_d(U(eroded, ST(ed, 2 * r, "round", "round")))


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled body."""
    return Part("dot", d)


def thick(d, w, cap="round", join="round"):
    """Closed outline of a stroke of width w along d."""
    return path_to_d(ST(d, w, cap, join))


def rot_pts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rot_d(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rot_line(d, deg, cx=12.0, cy=12.0):
    """Rotate an open path made of M/L/Q/C commands (absolute coordinates) without closing it."""
    import re
    toks = re.findall(r"[MLQC]|-?\d*\.?\d+", d)
    out, nums = [], []
    for t in toks:
        if t in "MLQC":
            out.append(t)
        else:
            nums.append(float(t))
            if len(nums) == 2:
                (x, y), = rot_pts([tuple(nums)], deg, cx, cy)
                out.append(f"{fmt(x)} {fmt(y)}")
                nums = []
    s = ""
    for t in out:
        s += t if t in "MLQC" else ((" " if s and s[-1] not in "MLQC" else "") + t)
    return s


def _p(p):
    return f"{fmt(p[0])} {fmt(p[1])}"


def bumpy(a, b, n, h, closed_start=True):
    """Path segment (no M) from a to b made of n bumps bulging h px to the left of the direction a->b."""
    dx, dy = (b[0] - a[0]) / n, (b[1] - a[1]) / n
    ln = math.hypot(dx, dy)
    nx, ny = dy / ln, -dx / ln  # left-hand normal on screen (y down)
    out = ""
    for i in range(n):
        s = (a[0] + dx * i, a[1] + dy * i)
        e = (a[0] + dx * (i + 1), a[1] + dy * (i + 1))
        c = ((s[0] + e[0]) / 2 + nx * 2 * h, (s[1] + e[1]) / 2 + ny * 2 * h)
        out += "Q" + _p(c) + " " + _p(e)
    return out


def wavy(x0, x1, y, n, h):
    """Open wavy line from (x0, y) to (x1, y) with n half-waves of height h (alternating up/down)."""
    w = (x1 - x0) / n
    out = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        sgn = -1 if i % 2 == 0 else 1
        out += f"Q{fmt(x0 + w * (i + 0.5))} {fmt(y + sgn * 2 * h)} {fmt(x0 + w * (i + 1))} {fmt(y)}"
    return out


def scallops(x0, x1, y, n, h):
    """Open line of n equal bumps hanging below y (a piped shell border)."""
    w = (x1 - x0) / n
    out = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        out += f"Q{fmt(x0 + w * (i + 0.5))} {fmt(y + 2 * h)} {fmt(x0 + w * (i + 1))} {fmt(y)}"
    return out


def spiral(cx, cy, r0, r1, pitch, start=0.0, step=15.0):
    """Archimedean spiral polyline from radius r0 to r1 (clockwise on screen)."""
    b = pitch / 360.0
    n = int((r1 - r0) / b / step) + 1
    pts = []
    for i in range(n + 1):
        t = min(i * step, (r1 - r0) / b)
        r = r0 + b * t
        a = math.radians(start + t)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return poly(pts)


def ell_pt(cx, cy, rx, ry, deg):
    a = math.radians(deg)
    return (cx + rx * math.cos(a), cy + ry * math.sin(a))


def box(x, y, w, h, dx, dy, r=0.0):
    """Oblique block: front face (x, y, w, h) and a top/side face pushed by (dx, -dy).
    Returns (outline_points, front_top_edge, front_side_edge, diagonal_edge)."""
    pts = [(x, y), (x + dx, y - dy), (x + w + dx, y - dy), (x + w + dx, y + h - dy), (x + w, y + h), (x, y + h)]
    return pts


def box_parts(S, x, y, w, h, dx, dy):
    pts = box(x, y, w, h, dx, dy)
    return (shell(poly(pts, closed=True, r=S.r)),
            detail(poly([(x, y), (x + w, y), (x + w, y + h)])),
            detail(seg(x + w, y, x + w + dx, y - dy)))


# =========================================================================== cakes

@icon("bubble-waffle", CAT, "A bubbly waffle cone folded around a scoop of ice cream",
      tags=["egg waffle", "hong kong waffle", "waffle cone", "street food", "ice cream", "dessert"])
def _(S):
    top_l, top_r, tipp = (3.5, 10), (20.5, 10), (12, 21.5)
    cone = "M" + _p(top_r) + bumpy(top_r, tipp, 4, 0.8) + bumpy(tipp, top_l, 4, 0.8) + "Z"
    if S.name == "line":
        scoop = "M3.5 10C3.5 5.8 7.3 3 12 3C16.7 3 20.5 5.8 20.5 10Z"
    else:
        scoop = "M5 10C3.6 10 3 8.9 3.6 7.7C4.9 4.8 8.2 3 12 3C15.8 3 19.1 4.8 20.4 7.7C21 8.9 20.4 10 19 10Z"
    return [shell(union(cone, scoop)), detail(seg(4, 10, 20, 10)),
            dot(8, 13, 1.1), dot(12, 13, 1.1), dot(16, 13, 1.1), dot(10.1, 16.2, 1.1), dot(13.9, 16.2, 1.1)]


@icon("hamantaschen", CAT, "A triangular cookie with its sides folded up around a round filling",
      tags=["purim", "triangle cookie", "filled cookie", "jewish", "pastry", "cookie"],
      aliases=["hamentashen"])
def _(S):
    c = (12, 13.2)
    tri = regular(c[0], c[1], 10, 3)
    parts = [shell(poly(tri, closed=True, r=L(S, 0.8, 2.6))), mark(circle(c[0], c[1], 2.7))]
    for deg in (-90, 30, 150):
        a, b = (c[0] + 4.8 * math.cos(math.radians(deg)), c[1] + 4.8 * math.sin(math.radians(deg))), \
               (c[0] + 7.6 * math.cos(math.radians(deg)), c[1] + 7.6 * math.sin(math.radians(deg)))
        parts.append(detail(seg(*a, *b)))
    return parts


@icon("cake-slice", CAT, "A wedge of layered cake with frosting and a cherry on top",
      tags=["slice of cake", "piece of cake", "dessert", "layer cake", "birthday", "sweet"])
def _(S):
    cherry = circle(15.5, 4.8, 2)
    cake = poly([(3, 12.5), (17, 6.5), (21, 9), (21, 20.5), (3, 20.5)], closed=True, r=S.r)
    return [shell(behind(cake, [cherry], 0)), shell(cherry),
            detail(seg(3, 12.5, 21, 9)), detail(seg(3, 16.7, 21, 14.6))]


@icon("sheet-cake", CAT, "A flat rectangular cake with a piped shell border along the top edge",
      tags=["slab cake", "tray bake", "party cake", "office cake", "celebration", "dessert"])
def _(S):
    x, y, w, h, dx, dy = 3, 12, 14, 7.5, 4, 5
    pts = box(x, y, w, h, dx, dy)
    return [shell(poly(pts, closed=True, r=S.r)),
            detail(scallops(x, x + w, y, 4, 1.1)), detail(seg(x + w, y, x + w, y + h)),
            detail(seg(x + w, y, x + w + dx, y - dy))]


@icon("wedding-cake", CAT, "A three-tier round cake with piped pearls on each tier",
      tags=["tiered cake", "wedding", "celebration", "marriage", "anniversary", "reception"])
def _(S):
    r = min(S.R, 1.5)
    body = union(rect(3, 15, 18, 6, r), rect(5.5, 9.5, 13, 6, r), rect(8, 4, 8, 6, r))
    return [shell(body), dot(7, 18, 1), dot(12, 18, 1), dot(17, 18, 1),
            dot(9.5, 12.25, 1), dot(14.5, 12.25, 1), dot(12, 7, 1)]


@icon("bundt-cake", CAT, "A ring cake with fluted sides and a hole in the middle",
      tags=["bundt", "ring cake", "fluted cake", "gugelhupf", "pound cake", "dessert"])
def _(S):
    top = "M5.5 8C5.5 6.3 8.4 5 12 5C15.6 5 18.5 6.3 18.5 8"
    if S.name == "line":
        base = "C19.6 10.5 20.5 14 20.8 20H3.2C3.5 14 4.4 10.5 5.5 8Z"
    else:
        base = "C19.6 10.5 20.5 14 20.8 18C20.9 19.6 17 20.5 12 20.5C7 20.5 3.1 19.6 3.2 18C3.5 14 4.4 10.5 5.5 8Z"
    return [shell(top + base), detail("M5.5 8C5.5 9.7 8.4 11 12 11C15.6 11 18.5 9.7 18.5 8"),
            mark(ellipse(12, 8, 2.2, 1)),
            detail("M8.2 10.6C7.3 13.5 7 16.5 7.1 19.8"), detail(seg(12, 11, 12, 20)),
            detail("M15.8 10.6C16.7 13.5 17 16.5 16.9 19.8")]


@icon("king-cake", CAT, "An oval ring cake with bands of sugar and a small crown on top",
      tags=["mardi gras", "carnival", "epiphany", "galette des rois", "rosca de reyes", "ring cake"])
def _(S):
    cx, cy, rx, ry, irx, iry = 12, 14.6, 9.4, 6.4, 4, 1.9
    crown = poly([(8.5, 9.5), (8.5, 4), (10.25, 6.2), (12, 3.2), (13.75, 6.2), (15.5, 4), (15.5, 9.5)],
                 closed=True, r=L(S, 0, 0.8))
    ring = minus(ellipse(cx, cy, rx, ry), ellipse(cx, cy, irx, iry))
    parts = [shell(behind(ring, [crown], 0.75)), shell(crown)]
    for deg in (45, 90, 135, 200, 340):
        a, b = ell_pt(cx, cy, irx, iry, deg), ell_pt(cx, cy, rx, ry, deg)
        parts.append(detail(seg(*a, *b)))
    return parts


@icon("pound-cake", CAT, "A long loaf cake in a tin shape with a cracked split along its domed top",
      tags=["loaf cake", "madeira cake", "butter cake", "tea cake", "bakery", "dessert"])
def _(S):
    tin = poly([(2.5, 12.5), (21.5, 12.5), (20.3, 19.5), (3.7, 19.5)], closed=True, r=S.r)
    dome = "M2.5 12.5C3 8.6 6.5 7 12 7C17.5 7 21 8.6 21.5 12.5Z"
    return [shell(union(tin, dome)), detail(seg(3, 12.5, 21, 12.5)),
            detail(poly([(6.5, 10.2), (8.7, 9), (10.8, 10.3), (13.2, 9), (15.3, 10.3), (17.5, 9.2)], r=S.r * 0.4))]


def _sector(cx, cy, r, a0, a1):
    """Closed pie region from angle a0 clockwise to a1 (degrees, screen)."""
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{fmt(cx)} {fmt(cy)}L{_p(p0)}A{fmt(r)} {fmt(r)} 0 {large} 1 {_p(p1)}Z"


@icon("upside-down-cake", CAT, "A round cake seen from above with pineapple rings and a cherry in each ring, one slice cut away",
      tags=["pineapple upside-down cake", "pineapple cake", "fruit cake", "retro dessert", "cherry", "baking"])
def _(S):
    c, d = 12, 4.8
    body = _sector(c, c, 9.2, 90, 30)
    if S.name == "rounded":
        body = soften(body, 1.2)
    parts = [shell(body)]
    for deg in (150, 240, 330):
        x, y = c + d * math.cos(math.radians(deg)), c + d * math.sin(math.radians(deg))
        parts += [detail(circle(x, y, 2.2)), dot(x, y, 0.85)]
    return parts


@icon("carrot-cake", CAT, "A slice of layered cake with frosting and a small piped carrot on top",
      tags=["carrot", "spice cake", "cream cheese frosting", "layer cake", "dessert", "easter"])
def _(S):
    carrot = poly([(5.5, 7.6), (14.6, 4.6), (15.4, 8.4)], closed=True, r=L(S, 0.3, 1.2))
    return [shell(rect(4, 11, 16, 9.5, min(S.R, 2))), detail(wavy(4, 20, 13.8, 4, 0.7)),
            detail(seg(4, 17.2, 20, 17.2)), shell(carrot),
            line(seg(17, 6.2, 19.5, 4.2)), line(seg(17.3, 8.4, 20, 8.9))]


@icon("cheesecake", CAT, "A wedge of cheesecake on a thin crumb base with fruit sauce dripping down",
      tags=["cheese cake", "new york cheesecake", "slice", "berry sauce", "dessert", "cake"])
def _(S):
    cake = poly([(3, 9.5), (8, 5), (21, 12.5), (21, 20.5), (3, 20.5)], closed=True, r=S.r)
    sauce = "M3 9.5L21 12.5"
    drip = "M3.5 12.3L7 12.9Q7.7 16.3 9.2 13.3L14 14.1Q14.7 16.8 16.1 14.4L20.5 15.2"
    return [shell(cake), detail(sauce), detail(drip), detail(seg(3, 18, 21, 18))]


@icon("swiss-roll", CAT, "A rolled sponge log with its cut end showing a spiral of cream",
      tags=["jelly roll", "roll cake", "roulade", "cake roll", "sponge", "dessert"])
def _(S):
    end = circle(8.5, 12, 6.5)
    body = ("M8.5 5.5H18.5C20 5.5 21 8.5 21 12C21 15.5 20 18.5 18.5 18.5H8.5Z" if S.name == "rounded"
            else "M8.5 5.5H19.5C20.5 7.5 21 9.5 21 12C21 14.5 20.5 16.5 19.5 18.5H8.5Z")
    return [shell(behind(body, [end], 0)), shell(end), detail(spiral(8.5, 12, 0.6, 5.6, 3.9, start=180))]


@icon("yule-log", CAT, "A log-shaped cake with bark lines, a cut branch stump and a holly sprig",
      tags=["buche de noel", "christmas log", "chocolate log", "christmas", "holiday", "cake"])
def _(S):
    endf = ellipse(18.2, 15.4, 2.8, 5)
    stump = "M5 11.5V8C5 7 6 6.2 7.25 6.2C8.5 6.2 9.5 7 9.5 8V11.5Z"
    log = rect(2.5, 10.4, 16, 10, min(S.R, 3))
    body = behind(union(log, stump), [endf], 0)
    lv1 = poly([(14, 7.6), (16.4, 5.4), (19.4, 5.2), (17.2, 7.6)], closed=True, r=L(S, 0, 0.8))
    lv2 = poly([(14, 7.6), (13.2, 4.6), (10.8, 3.2), (11.6, 6)], closed=True, r=L(S, 0, 0.8))
    return [shell(body), shell(endf), dot(18.2, 15.4, 1.2), shell(lv1), shell(lv2),
            detail("M4.5 14C6.5 13.2 8.5 14.8 11 14"), detail("M5.5 17.4C7.5 16.6 10 18.2 12.5 17.4")]


@icon("charlotte-cake", CAT, "A round cake ringed by upright sponge fingers, tied with a ribbon and topped with berries",
      tags=["charlotte", "charlotte russe", "ladyfinger cake", "berry cake", "dessert", "french"])
def _(S):
    body = "M4 20.5V10A2 2 0 0 1 8 10A2 2 0 0 1 12 10A2 2 0 0 1 16 10A2 2 0 0 1 20 10V20.5Z"
    if S.name == "line":
        body = poly([(4, 20.5), (4, 9), (6, 8), (8, 9), (10, 8), (12, 9), (14, 8), (16, 9), (18, 8), (20, 9), (20, 20.5)],
                    closed=True)
    return [shell(body), detail(seg(8, 10, 8, 20.5)), detail(seg(16, 10, 16, 20.5)),
            detail(seg(4, 15.75, 20, 15.75)),
            mark(poly([(12, 15.75), (9.3, 13.6), (9.3, 17.9)], closed=True, r=L(S, 0, 0.6))),
            mark(poly([(12, 15.75), (14.7, 13.6), (14.7, 17.9)], closed=True, r=L(S, 0, 0.6))),
            dot(8, 4.6, 1.4), dot(12, 3.8, 1.4), dot(16, 4.6, 1.4)]


@icon("tiramisu", CAT, "A square portion of layered sponge and cream with a cocoa-dusted top",
      tags=["italian dessert", "coffee dessert", "mascarpone", "ladyfingers", "cocoa", "layered dessert"])
def _(S):
    x, y, w, h, dx, dy = 3, 9.5, 13, 11, 5, 5.5
    return [*box_parts(S, x, y, w, h, dx, dy), detail(wavy(3, 16, 13.2, 3, 0.6)), detail(seg(3, 16.9, 16, 16.9)),
            dot(8.4, 6.75, 1), dot(12, 6.75, 1), dot(15.6, 6.75, 1)]


@icon("lamington", CAT, "A cube of sponge cake coated all over in flakes of coconut",
      tags=["coconut cake", "australian", "sponge cake", "chocolate coconut", "afternoon tea", "cake"])
def _(S):
    x, y, w, h, dx, dy = 3, 9, 12, 12, 6, 6
    flakes = [(6, 12.5, 30), (10.5, 11.8, -40), (12.2, 15.2, 70), (7.2, 16.4, -15), (10, 18.6, 45),
              (10.5, 5.8, 10), (15.2, 5.4, -50), (18, 11.4, 80), (17.8, 16.2, 20)]
    parts = list(box_parts(S, x, y, w, h, dx, dy))
    for fx, fy, a in flakes:
        ddx, ddy = 0.9 * math.cos(math.radians(a)), 0.9 * math.sin(math.radians(a))
        parts.append(detail(seg(fx - ddx, fy - ddy, fx + ddx, fy + ddy)))
    return parts


@icon("petit-four", CAT, "A tiny square iced cake with a piped flower on top",
      tags=["petit fours", "small cake", "iced cake", "afternoon tea", "fancy cake", "mignardise"])
def _(S):
    fl = union(*[circle(12 + 1.9 * math.cos(math.radians(a)), 7 + 1.9 * math.sin(math.radians(a)), 1.5)
                 for a in range(-90, 270, 72)])
    cake = rect(4.5, 11, 15, 9.5, min(S.R, 2.5))
    return [shell(behind(cake, [fl], 0)), shell(fl), dot(12, 7, 1),
            detail("M4.5 13.5H7Q8 17 9 13.5H14.5Q15.5 16.5 16.5 13.5H19.5")]


@icon("cake-pop", CAT, "A ball of cake on a stick with a coating and sprinkles",
      tags=["cakepop", "cake ball", "lollipop cake", "party treat", "sprinkles", "dessert"])
def _(S):
    return [shell(circle(12, 8.5, 6.2)), line(seg(12, 15.7, 12, 21.5)),
            detail("M5.9 9.6Q7.3 12.2 8.5 10.2Q10 13.4 11.8 10.4Q13.5 13.4 15.2 10.2Q16.6 12.2 18.1 9.6"),
            detail(seg(8.6, 6.4, 9.8, 5.2)), detail(seg(12.2, 4.8, 13.8, 5.2)), detail(seg(14.6, 7.6, 15.2, 6.2))]


@icon("brownie", CAT, "A square chunk of dense chocolate cake with a crackled top",
      tags=["chocolate brownie", "fudge brownie", "blondie", "square", "bake sale", "dessert"])
def _(S):
    x, y, w, h, dx, dy = 3, 14, 14, 6.5, 4.5, 8
    return [*box_parts(S, x, y, w, h, dx, dy),
            detail(poly([(6.5, 12.2), (9, 10.2), (11.2, 11.4), (13.6, 8.6)], r=S.r * 0.4)),
            detail(poly([(12.4, 12.4), (15.2, 11.6), (17.6, 9.2)], r=S.r * 0.4))]


def _battenberg_filled():
    x, y, w, h, dx, dy = 3, 10, 10, 10, 8, 6
    out = poly(box(x, y, w, h, dx, dy), closed=True)
    body = U(P(out), ST(out, 2, "butt", "miter", 4))
    edges = ST(poly([(x, y), (x + w, y), (x + w, y + h)]), 2, "butt", "miter", 4)
    diag = ST(seg(x + w, y, x + w + dx, y - dy), 2, "butt", "miter", 4)
    return D(body, edges, diag, P(rect(4, 11, 4, 4)), P(rect(8, 15, 4, 4)))


@icon("battenberg", CAT, "A long cake whose square end shows a two-by-two checkerboard of light and dark sponge",
      tags=["battenberg cake", "checkerboard cake", "marzipan", "british", "afternoon tea", "cake"],
      aliases=["battenburg"], filled=_battenberg_filled)
def _(S):
    x, y, w, h, dx, dy = 3, 10, 10, 10, 8, 6
    return [*box_parts(S, x, y, w, h, dx, dy), detail(seg(8, 10, 8, 20)), detail(seg(3, 15, 13, 15)),
            mark(rect(4, 11, 3, 3)), mark(rect(9, 16, 3, 3))]


@icon("baumkuchen", CAT, "A round tree cake with concentric rings, a hole in the middle and one slice cut away",
      tags=["tree cake", "spit cake", "layer cake", "german cake", "japanese", "ring cake"])
def _(S):
    c, R, h = 12, 9, 2.6
    a0, a1 = 0, 300

    def pp(r, a):
        return _p((c + r * math.cos(math.radians(a)), c + r * math.sin(math.radians(a))))
    body = (f"M{pp(R, a0)}A{R} {R} 0 1 1 {pp(R, a1)}L{pp(h, a1)}A{h} {h} 0 1 0 {pp(h, a0)}Z")
    if S.name == "rounded":
        body = soften(body, 1.2)
    return [shell(body), detail(f"M{pp(5.8, a0 + 8)}A5.8 5.8 0 1 1 {pp(5.8, a1 - 8)}")]


def _mooncake_edge(S, cx, cy, R, n):
    pts = [(cx + R * math.cos(math.radians(-90 + i * 360 / n)), cy + R * math.sin(math.radians(-90 + i * 360 / n)))
           for i in range(n)]
    br = R * math.sin(math.pi / n) * 1.15
    d = "M" + _p(pts[0])
    for i in range(n):
        d += f"A{fmt(br)} {fmt(br)} 0 0 1 {_p(pts[(i + 1) % n])}"
    return d + "Z"


@icon("mooncake", CAT, "A round pastry with a fluted edge and a flower pressed into its top",
      tags=["moon cake", "mid-autumn festival", "chinese pastry", "lotus paste", "festival", "pastry"],
      aliases=["moon-cake"])
def _(S):
    fl = union(*[circle(12 + 1.7 * math.cos(math.radians(a)), 12 + 1.7 * math.sin(math.radians(a)), 1.5)
                 for a in (45, 135, 225, 315)])
    if S.name == "rounded":
        edge = _mooncake_edge(S, 12, 12, 8.6, 12)
    else:
        pts = []
        for i in range(12):
            a0 = -90 + i * 30
            pts += [(12 + 8 * math.cos(math.radians(a0)), 12 + 8 * math.sin(math.radians(a0))),
                    (12 + 9.4 * math.cos(math.radians(a0 + 9)), 12 + 9.4 * math.sin(math.radians(a0 + 9))),
                    (12 + 9.4 * math.cos(math.radians(a0 + 21)), 12 + 9.4 * math.sin(math.radians(a0 + 21)))]
        edge = poly(pts, closed=True)
    return [shell(edge), detail(circle(12, 12, 6)), detail(fl)]


@icon("molten-lava-cake", CAT, "A small chocolate cake cut open with thick sauce flowing out onto the plate",
      tags=["lava cake", "chocolate fondant", "molten cake", "chocolate", "restaurant dessert", "pudding"])
def _(S):
    if S.name == "rounded":
        cake = "M5 16V11C5 7 8 4.5 12 4.5C16 4.5 19 7 19 11V16Z"
    else:
        cake = "M5 16V9.5L8 4.5H16L19 9.5V16Z"
    lava = ("M11.3 7.5H12.7L13.6 13.5C13.9 15.4 14.8 16.4 16.5 16.8C17.5 17 19.8 17.1 20.6 17.4C21.3 17.7 21.6 18.3 21.6 19"
            "C21.6 20 20.8 20.5 19.5 20.5H4.5C3.2 20.5 2.4 20 2.4 19C2.4 18.3 2.7 17.7 3.4 17.4C4.2 17.1 6.5 17 7.5 16.8"
            "C9.2 16.4 10.1 15.4 10.4 13.5Z")
    return [shell(behind(cake, [lava], 0.75)), mark(lava)]


@icon("strawberry-shortcake", CAT, "A slice of sponge with whipped cream layers and a whole strawberry on top",
      tags=["shortcake", "strawberry cake", "cream cake", "japanese shortcake", "sponge cake", "dessert"])
def _(S):
    berry = ("M12 2.8C14.8 3.8 16.6 6.2 16.3 8.4C16.1 9.8 14.2 10.4 12 10.4C9.8 10.4 7.9 9.8 7.7 8.4"
             "C7.4 6.2 9.2 3.8 12 2.8Z")
    cake = rect(3.5, 11.2, 17, 9.3, min(S.R, 2.5))
    return [shell(behind(cake, [berry], 0)), shell(berry), dot(12, 5.6, 0.8), dot(10.3, 8, 0.8), dot(13.7, 8, 0.8),
            detail(wavy(3.5, 20.5, 15.8, 4, 0.8))]


@icon("crepe-cake", CAT, "A round cake of many thin stacked crepes with a slice cut out to show the layers",
      tags=["mille crepe", "crepe layer cake", "pancake cake", "layered cake", "french", "dessert"])
def _(S):
    cyl = "M3 8C3 5.8 7 4 12 4C17 4 21 5.8 21 8V17C21 19.2 17 21 12 21C7 21 3 19.2 3 17Z"
    body = minus(cyl, "M12 17H24V24H12Z")
    parts = [shell(body if S.name == "line" else soften(body, 1)),
             detail("M3 8C3 10.2 7 12 12 12V8H21"), detail(seg(12, 12, 12, 17))]
    for y in (11, 14):
        parts.append(detail(f"M3 {y}C3 {y + 2.2} 7 {y + 4} 12 {y + 4}"))
        parts.append(detail(seg(12, y, 21, y)))
    return parts


@icon("whoopie-pie", CAT, "Two soft domed cakes sandwiching a thick layer of white filling",
      tags=["whoopie", "moon pie", "sandwich cake", "gob", "cream filling", "dessert"])
def _(S):
    fill = rect(2.8, 9.8, 18.4, 4.4, L(S, 1, 2.2))
    top = "M4.5 11.5C4.5 6.7 8 4 12 4C16 4 19.5 6.7 19.5 11.5Z"
    bot = "M4.5 12.5C4.5 17.3 8 20 12 20C16 20 19.5 17.3 19.5 12.5Z"
    return [shell(fill), shell(behind(top, [fill], 0.75)), shell(behind(bot, [fill], 0.75))]


@icon("mug-cake", CAT, "A coffee mug with a domed sponge cake rising above its rim",
      tags=["microwave cake", "cake in a mug", "mug", "quick dessert", "single serving", "baking"])
def _(S):
    dome = "M3 11.2C3 7 6.4 4.5 10.25 4.5C14.1 4.5 17.5 7 17.5 11.2Z"
    mug = rect(4, 10.5, 12.5, 10.5, min(S.R, 2.5))
    return [shell(dome), shell(behind(mug, [dome], 0.75)), dot(8, 8.2, 1.1), dot(12.3, 7.6, 1.1),
            line("M16.5 13.5H18C19.7 13.5 20.8 14.6 20.8 16.2C20.8 17.8 19.7 18.8 18 18.8H16.5" if S.name == "rounded"
                 else "M16.5 13.5H20.8V18.8H16.5")]


@icon("muffin", CAT, "A paper-lined muffin with a big rounded top spilling over its pleated case",
      tags=["blueberry muffin", "breakfast", "bakery", "cafe", "baked goods", "snack"])
def _(S):
    cap = ("M3.4 12.2C2.6 12.2 2.3 11.2 2.5 10.2C3.2 6.6 7 4 12 4C17 4 20.8 6.6 21.5 10.2"
           "C21.7 11.2 21.4 12.2 20.6 12.2Z")
    case = poly([(5.5, 12), (18.5, 12), (17, 21), (7, 21)], closed=True, r=S.r)
    return [shell(cap), shell(behind(case, [cap], 0)), detail(seg(10, 14.2, 10.4, 21)), detail(seg(14, 14.2, 13.6, 21)),
            dot(8, 9, 1.2), dot(12.5, 7.2, 1.2), dot(16.2, 9.6, 1.2)]


@icon("pavlova", CAT, "A round meringue nest with a crisp shell, a mound of cream and berries on top",
      tags=["meringue cake", "berries", "whipped cream", "australian", "new zealand", "dessert"])
def _(S):
    base = poly([(3, 14.2), (21, 14.2), (19.8, 20.5), (4.2, 20.5)], closed=True, r=S.r)
    cream = "M4.6 14.2C3.8 12.2 5.4 10.2 7.6 10.8C7.6 8 9.6 6.2 12 6.2C14.4 6.2 16.4 8 16.4 10.8C18.6 10.2 20.2 12.2 19.4 14.2Z"
    return [shell(union(base, cream)), detail(seg(3.5, 14.2, 20.5, 14.2)),
            dot(9.6, 10.6, 1.2), dot(13.2, 9, 1.2), dot(15.2, 12, 1.2),
            detail(seg(8, 16.6, 8, 20.5)), detail(seg(12, 16.6, 12, 20.5)), detail(seg(16, 16.6, 16, 20.5))]


@icon("meringue", CAT, "A single swirled meringue kiss with ridged sides and a curled tip",
      tags=["meringue kiss", "meringue cookie", "pavlova", "egg white", "piped", "sweet"])
def _(S):
    body = ("M12 2.8C13 5.6 15.6 7.6 17.8 10C20.4 12.9 20.6 16.9 18.6 19C17.6 20 16.5 20.5 15 20.5H9"
            "C7.5 20.5 6.4 20 5.4 19C3.4 16.9 3.6 12.9 6.2 10C8.4 7.6 11 5.6 12 2.8Z")
    if S.name == "line":
        body = ("M12 2.8C13 5.6 15.6 7.6 17.8 10C20.4 12.9 20.6 16.9 18.9 20.5H5.1"
                "C3.4 16.9 3.6 12.9 6.2 10C8.4 7.6 11 5.6 12 2.8Z")
    return [shell(body), line("M12 2.8C12.6 2 14 1.9 14.6 2.9"),
            detail("M5 15.5C8.5 17 14.5 16.4 18.9 13.3"), detail("M7.8 10.9C10 11.8 13.6 11.3 16 9")]


@icon("baked-alaska", CAT, "A dome of swirled meringue with toasted peaks on a flat cake base",
      tags=["bombe alaska", "meringue", "ice cream cake", "flambe", "retro dessert", "dessert"])
def _(S):
    cx, cy = 12, 16.5
    pts = []
    n = 10
    for i in range(n + 1):
        a = 180 + i * 180 / n
        r = 9.4 if i % 2 == 1 else 7.4
        if i in (0, n):
            r = 8.4
        pts.append((cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))))
    dome = poly(pts, closed=True, r=L(S, 0.2, 1.2))
    base = rect(3, 16.5, 18, 4, min(S.R, 1.5))
    return [shell(behind(dome, [base], 0)), shell(base), detail("M8 13.2C9.5 11.8 11.4 11.8 12.6 13C13.8 14.2 15.4 14 16.2 12.8")]


@icon("mont-blanc-dessert", CAT, "A small mound of piped chestnut cream strands on a round base",
      tags=["mont blanc", "chestnut", "chestnut cream", "french pastry", "japanese pastry", "dessert"])
def _(S):
    dome = "M4 17V14C4 8.5 7.5 5 12 5C16.5 5 20 8.5 20 14V17Z"
    base = rect(3, 17, 18, 3.5, min(S.R, 1.5))
    parts = [shell(behind(dome, [base], 0)), shell(base)]
    for x in (8, 12, 16):
        top = 8.2 if x != 12 else 7.2
        parts.append(detail(f"M{x} {top}Q{x - 1} {top + 2} {x} {top + 4}T{x} 17" if x != 12 else
                            f"M12 {top}Q11 {top + 2.3} 12 {top + 4.7}T12 17"))
    return parts


@icon("christmas-pudding", CAT, "A round dark pudding with white sauce over the top and a holly sprig",
      tags=["plum pudding", "figgy pudding", "christmas", "holiday dessert", "holly", "british"])
def _(S):
    lv1 = poly([(11.2, 6.2), (9.4, 3.4), (5.8, 3.2), (7.6, 6)], closed=True, r=L(S, 0, 0.8))
    lv2 = poly([(12.8, 6.2), (14.6, 3.4), (18.2, 3.2), (16.4, 6)], closed=True, r=L(S, 0, 0.8))
    dome = ("M3 20.5V17C3 11.5 7 7.8 12 7.8C17 7.8 21 11.5 21 17V20.5Z" if S.name == "line" else
            "M3 18.5V17C3 11.5 7 7.8 12 7.8C17 7.8 21 11.5 21 17V18.5C21 19.6 20.1 20.5 19 20.5H5C3.9 20.5 3 19.6 3 18.5Z")
    sauce = "M3.8 13.4Q5.8 13 6.2 15.2Q6.6 17.2 8 15.6Q9.3 13.8 11.2 14.2Q13.4 14.6 14 16.6Q14.6 18.2 15.8 16Q16.8 13.6 20.2 13.4"
    return [shell(behind(dome, [lv1, lv2], 0.75)), shell(lv1), shell(lv2), dot(12, 5.2, 1.4), detail(sauce),
            dot(9, 18, 1), dot(18, 18.2, 1)]


@icon("souffle", CAT, "A straight-sided ramekin with a puffed top rising well above the rim",
      tags=["souffle", "cheese souffle", "chocolate souffle", "ramekin", "french", "baked dessert"])
def _(S):
    puff = ("M5.5 12.5V9C5.5 5.4 8.4 2.8 12 2.8C15.6 2.8 18.5 5.4 18.5 9V12.5Z" if S.name == "rounded" else
            "M5.5 12.5V7.5L8.5 3H15.5L18.5 7.5V12.5Z")
    dish = rect(3.5, 12.5, 17, 8, min(S.R, 2))
    return [shell(behind(puff, [dish], 0.75)), shell(dish), detail(seg(3.5, 15, 20.5, 15)),
            detail(seg(8, 17.5, 8, 20.5)), detail(seg(12, 17.5, 12, 20.5)), detail(seg(16, 17.5, 16, 20.5))]


@icon("trifle", CAT, "A footed glass bowl showing layers of sponge, fruit, custard and cream",
      tags=["trifle bowl", "layered dessert", "custard", "sponge", "british", "party dessert"])
def _(S):
    bowl = poly([(3, 6.5), (21, 6.5), (18.5, 16.5), (14, 16.5), (14, 18.5), (18, 18.5), (18, 21), (6, 21),
                 (6, 18.5), (10, 18.5), (10, 16.5), (5.5, 16.5)], closed=True, r=S.r * 0.6)
    cream = "M4.5 6.5C4.5 4.3 6.5 3 8.3 4.3C9.3 2.6 11 2.3 12 3.6C13 2.3 14.7 2.6 15.7 4.3C17.5 3 19.5 4.3 19.5 6.5Z"
    return [shell(union(bowl, cream)), detail(seg(3.5, 6.5, 20.5, 6.5)), detail(wavy(4.2, 19.8, 10, 4, 0.6)),
            detail(seg(5, 13.3, 19, 13.3))]


@icon("yogurt-parfait", CAT, "A tall glass of layered yogurt, granola and fruit with a spoon sticking out",
      tags=["parfait", "yogurt", "granola", "breakfast", "layered", "healthy"])
def _(S):
    glass = poly([(6, 6.5), (18, 6.5), (16.5, 21), (7.5, 21)], closed=True, r=S.r)
    return [shell(glass), line(seg(14, 6.5, 18.5, 2)),
            detail(wavy(6.5, 17.5, 10, 4, 0.6)), dot(9.5, 13.2, 1), dot(12, 13.2, 1), dot(14.5, 13.2, 1),
            detail(seg(7.4, 16.5, 16.6, 16.5)), dot(9, 4.2, 1.3)]


@icon("panna-cotta", CAT, "A smooth dome of set cream on a plate with berry sauce pooling around it",
      tags=["pannacotta", "italian dessert", "cream pudding", "berry coulis", "set dessert", "dessert"])
def _(S):
    dome = ("M5 16.5V13C5 8.5 8 5 12 5C16 5 19 8.5 19 13V16.5Z" if S.name == "rounded" else
            "M5 16.5L5.5 10.5L8.5 5H15.5L18.5 10.5L19 16.5Z")
    pool = ("M2 18.4C2 16.4 4.5 15.2 7.5 15.5C10 15.8 14 15.8 16.5 15.5C19.5 15.2 22 16.4 22 18.4"
            "C22 20.1 18.5 21 12 21C5.5 21 2 20.1 2 18.4Z")
    return [shell(dome), shell(behind(pool, [dome], 0.75)), detail("M8 11.5C8 9.6 9 8.3 10.5 7.8")]


@icon("creme-brulee", CAT, "A shallow ramekin with a cracked caramel top and a spoon about to tap it",
      tags=["creme brulee", "burnt cream", "custard", "caramelized sugar", "french dessert", "ramekin"])
def _(S):
    dish = "M2.5 13A8.5 3.5 0 0 1 19.5 13V17.5A8.5 3.5 0 0 1 2.5 17.5Z"
    if S.name == "line":
        dish = "M2.5 13A8.5 3.5 0 0 1 19.5 13V21H2.5Z"
    bowl = rot_d(ellipse(17, 6, 2.2, 1.4), -40, 17, 6)
    return [shell(dish), detail("M2.5 13A8.5 3.5 0 0 0 19.5 13"),
            detail(poly([(6.5, 12.6), (9, 11.4), (11, 13), (13.6, 11.6)], r=S.r * 0.4)),
            shell(bowl), line(seg(18.8, 4.6, 21.5, 2.3))]


@icon("flan", CAT, "A round custard turned out on a plate with caramel running down its sides",
      tags=["creme caramel", "caramel custard", "leche flan", "pudding", "custard", "dessert"])
def _(S):
    body = ("M6.5 7A5.5 2.2 0 0 1 17.5 7L20 16.5A8 2 0 0 1 4 16.5Z" if S.name == "rounded" else
            "M6.5 7A5.5 2.2 0 0 1 17.5 7L20 17.5H4Z")
    return [shell(body), detail("M6.5 7A5.5 2.2 0 0 0 17.5 7"),
            detail("M5.9 10.3Q7.3 14.5 8.5 11.2Q10.2 14.8 12 11.7Q13.8 14.8 15.5 11.2Q16.7 14.5 18.1 10.3"),
            line(seg(2.5, 20.5, 21.5, 20.5))]


@icon("gelatin-dessert", CAT, "A fluted jelly on a plate with short wobble lines on either side",
      tags=["jelly", "jelly mold", "gelatin", "wobbly", "molded dessert", "party dessert"])
def _(S):
    top = "M7 9.5Q7 5.8 9.5 6Q10.5 4.2 12 4.2Q13.5 4.2 14.5 6Q17 5.8 17 9.5"
    body = top + ("L18.5 17.5H5.5Z" if S.name == "line" else "L18.3 16C18.4 17 17.8 17.5 17 17.5H7C6.2 17.5 5.6 17 5.7 16Z")
    return [shell(body), detail(seg(10, 8.5, 9.5, 17.5)), detail(seg(14, 8.5, 14.5, 17.5)),
            line(seg(3, 20.5, 21, 20.5)), line("M3.5 8.5Q2 11.5 3.5 14.5"), line("M20.5 8.5Q22 11.5 20.5 14.5")]


@icon("mochi", CAT, "A soft round flattened rice cake dusted with flour and with a gentle sheen",
      tags=["daifuku", "rice cake", "japanese sweet", "wagashi", "glutinous rice", "dessert"])
def _(S):
    body = ("M3.5 18.5C2.5 11 7 6 12 6C17 6 21.5 11 20.5 18.5Z" if S.name == "line" else
            "M3 16C3 10.5 7 6 12 6C17 6 21 10.5 21 16C21 18.8 17 19.8 12 19.8C7 19.8 3 18.8 3 16Z")
    return [shell(body), detail("M6.8 12.6C7.2 10.8 8.4 9.6 10 9.2"), dot(13.5, 12, 0.9), dot(16.5, 14.5, 0.9),
            dot(10.5, 15.5, 0.9)]


@icon("taiyaki", CAT, "A fish-shaped filled cake with scales, a round eye and a fanned tail",
      tags=["fish cake", "fish waffle", "bungeoppang", "japanese street food", "red bean", "snack"])
def _(S):
    if S.name == "line":
        body = ("M2.5 12C2.5 8 6.5 5.5 11 5.5C14 5.5 16 6.8 17.2 8.8L21.5 5.5V18.5L17.2 15.2"
                "C16 17.2 14 18.5 11 18.5C6.5 18.5 2.5 16 2.5 12Z")
    else:
        body = ("M2.5 12C2.5 8 6.5 5.5 11 5.5C14 5.5 16 6.8 17.2 8.8L19.8 6.6C20.6 5.9 21.5 6.3 21.5 7.4V16.6"
                "C21.5 17.7 20.6 18.1 19.8 17.4L17.2 15.2C16 17.2 14 18.5 11 18.5C6.5 18.5 2.5 16 2.5 12Z")
    return [shell(body), dot(6.2, 10.5, 1.2), detail("M9 7.8Q10.8 12 9 16.2"),
            detail(poly([(12.5, 10), (14, 11.2), (15.5, 10)], r=S.r * 0.3)),
            detail(poly([(12.5, 13.5), (14, 14.7), (15.5, 13.5)], r=S.r * 0.3))]


@icon("dango", CAT, "Three round rice dumplings threaded on a thin skewer",
      tags=["hanami dango", "mitarashi dango", "rice dumpling", "skewer", "japanese sweet", "wagashi"])
def _(S):
    cs = [rot_pts([(12, y)], 45)[0] for y in (5.2, 11.4, 17.6)]
    balls = [circle(x, y, 3.1) for x, y in cs]
    a, b = rot_pts([(12, 20.7), (12, 24.2)], 45)
    parts = [shell(union(*balls) if S.name == "rounded" else union(*balls))]
    parts += [line(seg(*a, *b))]
    for i in range(2):
        m = rot_pts([(12, 8.3 + i * 6.2)], 45)[0]
        p1, p2 = rot_pts([(9.6, 8.3 + i * 6.2), (14.4, 8.3 + i * 6.2)], 45)
        parts.append(detail(seg(*p1, *p2)))
    if S.name == "line":
        t1, t2 = rot_pts([(12, 0.5), (12, 2.1)], 45)
    else:
        t1, t2 = rot_pts([(12, 1.3), (12, 2.1)], 45)
    parts.append(line(seg(*t1, *t2)))
    return parts


@icon("tanghulu", CAT, "A skewer of three glossy candied strawberries with a shine mark on each",
      tags=["candied fruit", "sugar coated strawberry", "bingtanghulu", "chinese street food", "skewer", "candy"])
def _(S):
    def berry(cy):
        d = (f"M12 {fmt(cy + 3.3)}C9.6 {fmt(cy + 2.2)} 8.4 {fmt(cy)} 8.6 {fmt(cy - 1.5)}"
             f"C8.8 {fmt(cy - 2.8)} 10.2 {fmt(cy - 3.1)} 12 {fmt(cy - 3.1)}C13.8 {fmt(cy - 3.1)} 15.2 {fmt(cy - 2.8)} 15.4 {fmt(cy - 1.5)}"
             f"C15.6 {fmt(cy)} 14.4 {fmt(cy + 2.2)} 12 {fmt(cy + 3.3)}Z")
        return rot_d(d, 45)
    ys = (4.6, 11.1, 17.6)
    parts = [shell(union(*[berry(y) for y in ys]))]
    for y in ys:
        parts.append(dot(*rot_pts([(13.6, y - 1.1)], 45)[0], 0.9))
    a, b = rot_pts([(12, 20.9), (12, 24)], 45)
    parts.append(line(seg(*a, *b)))
    return parts


@icon("gulab-jamun", CAT, "A small bowl of round dark sweets half sunk in syrup",
      tags=["gulab jamun", "indian sweet", "syrup", "mithai", "diwali", "dessert"])
def _(S):
    bowl = ("M2.5 12.5H21.5C21.5 17.5 17.5 21 12 21C6.5 21 2.5 17.5 2.5 12.5Z" if S.name == "rounded" else
            "M2.5 12.5H21.5L18.5 21H5.5Z")
    balls = union(circle(6.8, 11.5, 3.4), circle(12, 9.8, 3.6), circle(17.2, 11.5, 3.4))
    return [shell(bowl), shell(behind(balls, [bowl], 0.75)), dot(11.2, 8.8, 0.9), dot(6, 10.8, 0.8), dot(16.4, 10.8, 0.8),
            detail(wavy(5, 19, 16, 4, 0.5))]


# =========================================================================== fried and syrup sweets

@icon("jalebi", CAT, "A loose spiral coil of fried batter soaked in syrup",
      tags=["jilapi", "zulbia", "indian sweet", "fried sweet", "syrup", "spiral"])
def _(S):
    coil = spiral(12, 12, 0.8, 9, 4.3, start=180, step=10)
    return [line(coil)]


@icon("ladoo", CAT, "A small pyramid of three round sweet balls with a textured surface on a plate",
      tags=["laddu", "laddoo", "indian sweet", "mithai", "diwali", "festival sweet"])
def _(S):
    bl, br, tp = circle(8.2, 14.6, 3.6), circle(15.8, 14.6, 3.6), circle(12, 8, 3.6)
    parts = [shell(bl), shell(behind(br, [bl], 0.5)), shell(behind(tp, [bl, br], 0.5)),
             line(seg(3, 20.8, 21, 20.8) if S.name == "line" else "M3 20.8H21")]
    for cx, cy in ((8.2, 14.6), (15.8, 14.6), (12, 8)):
        parts += [dot(cx - 1.1, cy - 0.6, 0.75), dot(cx + 1.2, cy + 0.9, 0.75)]
    return parts


@icon("sesame-balls", CAT, "Two round fried balls covered all over in sesame seeds",
      tags=["jian dui", "sesame ball", "dim sum", "chinese pastry", "fried dessert", "red bean"])
def _(S):
    front, back = circle(9, 14.2, 6.3), circle(15.8, 8.6, 5.6)
    seeds = [(6.5, 11.5, 30), (10.5, 12, -30), (7, 16, -60), (11.5, 16.2, 40), (9.2, 19, 0),
             (4.7, 14.4, 80), (14.8, 5.4, 20), (18.5, 7.5, -50), (17.6, 11.4, 30)]
    parts = [shell(front), shell(behind(back, [front], 0.6))]
    for x, y, a in seeds:
        seed = ellipse(x, y, 1.1, 0.6) if S.name != "line" else poly([(x - 1.2, y), (x, y - 0.6), (x + 1.2, y), (x, y + 0.6)], closed=True)
        parts.append(mark(rot_d(seed, a, x, y)))
    return parts


# =========================================================================== frozen treats

@icon("soft-serve", CAT, "A cone topped with a tall twisted swirl of soft ice cream ending in a curled tip",
      tags=["soft ice cream", "whippy", "twist cone", "ice cream cone", "frozen yogurt", "summer"])
def _(S):
    swirl = ("M6 12.5C4.6 12.5 4.4 10.2 6 9.9C5.8 8.2 7 7.2 8.4 7.2C8.2 5.4 9.6 4.4 11.2 4.4"
             "C11 3.2 12.2 2.2 14 2.1C13.4 2.9 13.6 3.9 14.2 4.5C15.6 4.9 16.2 6 15.9 7.2"
             "C17.2 7.2 18.3 8.2 18 9.9C19.6 10.2 19.4 12.5 18 12.5Z")
    cone = poly([(6.5, 12.5), (17.5, 12.5), (12, 22)], closed=True, r=L(S, 0, 1.5))
    return [shell(swirl), shell(behind(cone, [swirl], 0)), detail(seg(6.6, 9.9, 17.4, 9.9)),
            detail(seg(8.8, 7.2, 15.2, 7.2)), detail(seg(9.5, 14.5, 13.4, 18.4))]


def _stick(S, top=17):
    return rect(10.5, top, 3, 22 - top, L(S, 0, 1.5))


@icon("popsicle", CAT, "A round-topped frozen ice block on a flat wooden stick with a bite taken from one corner",
      tags=["ice lolly", "ice pop", "lolly", "frozen treat", "summer", "icy pole"])
def _(S):
    body = f"M6 17V9C6 5.7 8.7 3 12 3C15.3 3 18 5.7 18 9V{17 - S.R}A{S.R} {S.R} 0 0 1 {18 - S.R} 17H{6 + S.R}A{S.R} {S.R} 0 0 1 6 {17 - S.R}Z"
    body = minus(body, circle(18.2, 5.2, 2.5), circle(19.3, 9, 2.1))
    return [shell(body), shell(behind(_stick(S), [body], 0))]


@icon("freezer-pop", CAT, "A long thin plastic tube of frozen juice with a crimped end and the other end snipped open",
      tags=["ice pop", "freeze pop", "tube pop", "ice block", "plastic sleeve", "frozen juice"])
def _(S):
    deg = 40
    tube = poly(rot_pts([(9.5, 5.5), (14.5, 3.6), (14.5, 18.5), (9.5, 18.5)], deg), closed=True, r=S.r * 0.5)
    seal = poly(rot_pts([(9, 18.5), (15, 18.5), (15, 21.5), (13.5, 22.5), (12, 21.5), (10.5, 22.5), (9, 21.5)], deg),
                closed=True, r=L(S, 0, 0.5))
    a, b = rot_pts([(9.5, 10), (14.5, 10)], deg)
    return [shell(union(tube, seal)), detail(seg(*rot_pts([(9, 18.5)], deg)[0], *rot_pts([(15, 18.5)], deg)[0])),
            detail(seg(*a, *b))]


@icon("ice-cream-bar", CAT, "A rectangular coated ice cream bar on a stick with a drip line of chocolate",
      tags=["choc ice", "eskimo bar", "coated ice cream", "ice cream on a stick", "frozen treat", "summer"])
def _(S):
    body = rect(6, 3, 12, 14, min(S.R, 2.5))
    return [shell(body), shell(behind(_stick(S), [body], 0)),
            detail("M6 9H8Q9 13 10 9H13.5Q14.5 12 15.5 9H18")]


@icon("ice-cream-sandwich", CAT, "A block of ice cream between two wafer layers with dotted holes",
      tags=["ice cream sandwich", "wafer", "frozen treat", "cookie sandwich", "summer", "dessert"])
def _(S):
    x, y, w, h, dx, dy = 3, 9.5, 14, 11, 4, 5
    return [*box_parts(S, x, y, w, h, dx, dy), detail(seg(3, 13.2, 17, 13.2)), detail(seg(3, 16.8, 17, 16.8)),
            detail(seg(17, 13.2, 21, 8.2)), detail(seg(17, 16.8, 21, 11.8)),
            dot(7.5, 7, 0.9), dot(11.5, 7, 0.9), dot(15.5, 7, 0.9)]


@icon("sundae", CAT, "A tulip glass holding scoops of ice cream topped with a cherry",
      tags=["ice cream sundae", "hot fudge sundae", "dessert glass", "cherry on top", "parlour", "dessert"])
def _(S):
    glass = ("M4 12.5H20C20 15.4 17.4 17.5 13.2 17.6V19H16.5V21H7.5V19H10.8V17.6C6.6 17.5 4 15.4 4 12.5Z")
    if S.name == "line":
        glass = "M4 12.5H20L17 17.5H13.2V19H16.5V21H7.5V19H10.8V17.5H7Z"
    scoops = union(circle(8.2, 10.4, 3.3), circle(15.8, 10.4, 3.3), circle(12, 8.2, 3.6))
    cherry = circle(15.6, 3.6, 1.7)
    return [shell(glass), shell(behind(scoops, [glass, cherry], 0.9)), shell(cherry), line("M14.3 2.6Q13.2 1.6 11.6 2")]


@icon("banana-split", CAT, "A long boat dish with a split banana along its length and three scoops of ice cream on top",
      tags=["banana boat", "ice cream sundae", "soda fountain", "diner dessert", "banana", "ice cream"])
def _(S):
    dish = ("M3.5 15H20.5L18 19H6Z" if S.name == "line" else
            "M3.5 15H20.5C20 17.4 18 19 15 19H9C6 19 4 17.4 3.5 15Z")
    foot = rect(8.5, 19, 7, 2.2, min(S.R, 1))
    banana = "M3 9.2C4.6 13.4 7.8 15 12 15C16.2 15 19.4 13.4 21 9.2C18.8 10.9 15.8 11.4 12 11.4C8.2 11.4 5.2 10.9 3 9.2Z"
    scoops = union(circle(7.6, 8.6, 2.9), circle(12, 7.4, 3.1), circle(16.4, 8.6, 2.9))
    return [shell(union(dish, foot)), shell(behind(banana, [dish], 0)),
            shell(behind(scoops, [banana], 0.6))]


@icon("ice-cream-cup", CAT, "A small paper cup with two scoops of ice cream and a flat wooden spoon",
      tags=["ice cream tub", "gelato cup", "paper cup", "scoop", "dessert cup", "frozen treat"])
def _(S):
    cup = poly([(4.5, 12), (19.5, 12), (17.5, 21), (6.5, 21)], closed=True, r=S.r)
    spoon = thick(seg(15.2, 9.5, 20, 3.5), 2.6, "round" if S.name == "rounded" else "butt")
    scoops = union(circle(8.8, 10, 3.6), circle(15.2, 10, 3.6))
    return [shell(cup), shell(spoon), shell(behind(scoops, [cup, spoon], 0.75)), detail(seg(5.2, 15, 18.8, 15))]


@icon("ice-cream-tub", CAT, "A round tub of ice cream with its lid lifted to show the ice cream inside",
      tags=["ice cream carton", "pint", "tub", "frozen dessert", "grocery", "freezer"])
def _(S):
    tub = poly([(4, 11), (20, 11), (18.5, 21), (5.5, 21)], closed=True, r=S.r)
    lid = rot_d(rect(3, 5.5, 18, 2.6, min(S.R, 1.3)), -14, 21, 8.5)
    cream = "M5.5 11C5.5 9 7 8.8 8.3 9.6C9.2 8.3 10.6 8.2 11.6 9.3"
    return [shell(tub), shell(lid), detail(seg(4.8, 15, 19.2, 15)), detail(cream)]


@icon("neapolitan-ice-cream", CAT, "A block of ice cream with three flavour stripes side by side",
      tags=["neapolitan", "three flavours", "chocolate vanilla strawberry", "brick ice cream", "block", "dessert"])
def _(S):
    x, y, w, h, dx, dy = 3, 9.5, 14.4, 11, 4, 5
    a, b = x + w / 3, x + 2 * w / 3
    return [*box_parts(S, x, y, w, h, dx, dy), detail(seg(a, y, a, y + h)), detail(seg(b, y, b, y + h)),
            detail(seg(a, y, a + dx, y - dy)), detail(seg(b, y, b + dx, y - dy)),
            mark(rect(4, 10.5, a - 5, h - 2))]


@icon("dropped-ice-cream", CAT, "An upside-down cone stuck in a splattered puddle of melted ice cream",
      tags=["dropped cone", "melted ice cream", "accident", "oops", "summer", "bad day"])
def _(S):
    cone = poly([(12, 3), (17, 14.5), (7, 14.5)], closed=True, r=L(S, 0, 1.2))
    splat = union(ellipse(12, 17.6, 9, 3), circle(5.5, 16, 2.4), circle(18.2, 15.6, 2.6), circle(9, 15.2, 2.2))
    return [shell(cone), shell(behind(splat, [cone], 0.75)), detail(seg(9.3, 9.6, 14, 12.8)),
            dot(3.6, 10.5, 1.2), dot(20.6, 10.2, 1.1)]


@icon("frozen-banana", CAT, "A banana on a stick dipped halfway in chocolate with chopped nuts on the coating",
      tags=["chocolate banana", "banana pop", "frozen treat", "fair food", "banana", "summer"])
def _(S):
    tip = ("C14.6 2.2 15.6 2.9 15.2 4C14.9 4.8 14.6 5.4 14.5 6" if S.name == "rounded" else "L15.4 3.6L14.5 6")
    body = "M8.8 16.5C8 11 9.2 5.8 13.4 2.6" + tip + "C13.4 9.8 14 13 15 16.5Z"
    stick = rect(10.4, 16, 2.8, 6, L(S, 0, 1.4))
    return [shell(body), shell(behind(stick, [body], 0)), detail(seg(8.4, 11.6, 14.2, 10.2)),
            dot(10.6, 8, 0.8), dot(12.4, 5.8, 0.7)]


@icon("snow-cone", CAT, "A paper cone holding a rounded mound of shaved ice with syrup streaks",
      tags=["snowball", "shaved ice", "slush", "syrup", "fair food", "summer"])
def _(S):
    ice = ("M5 11.5C4 11.5 3.8 10 4.5 9.3C4 6.8 5.6 5.2 7.4 5.1C8.2 3.4 10 2.6 12 2.6C14 2.6 15.8 3.4 16.6 5.1"
           "C18.4 5.2 20 6.8 19.5 9.3C20.2 10 20 11.5 19 11.5Z")
    cone = poly([(5.5, 11.5), (18.5, 11.5), (12, 22)], closed=True, r=L(S, 0, 1.5))
    return [shell(ice), shell(behind(cone, [ice], 0)), detail("M9 11.5Q8 9 9.2 5.5"), detail("M14.2 11.5Q15.4 8.6 14.3 5.4"),
            detail(seg(9, 13.5, 13.8, 18))]


@icon("shaved-ice", CAT, "A bowl with a tall mountain of shaved ice topped with fruit and a syrup drizzle",
      tags=["bingsu", "kakigori", "halo halo", "ice kacang", "shaved ice dessert", "summer"])
def _(S):
    bowl = ("M2.5 13.5H21.5C21.5 17.5 17.5 20 12 20C6.5 20 2.5 17.5 2.5 13.5Z" if S.name == "rounded" else
            "M2.5 13.5H21.5L18 20H6Z")
    foot = rect(8, 19.5, 8, 2, L(S, 0, 1))
    mountain = "M4.5 13.5C4.8 10 7.5 5.2 12 5.2C16.5 5.2 19.2 10 19.5 13.5Z"
    fruit = circle(12, 3.5, 2)
    return [shell(union(bowl, foot)), shell(behind(mountain, [bowl, fruit], 0.75)), shell(fruit),
            detail("M7.2 10.4Q9.5 9 12 10.4Q14.5 11.8 16.8 10.4")]


@icon("kulfi", CAT, "A tall cone-shaped frozen dessert on a stick with chopped nuts",
      tags=["matka kulfi", "indian ice cream", "pistachio", "frozen dessert", "stick", "summer"])
def _(S):
    body = ("M7.5 17L10.2 4.2C10.6 2.6 13.4 2.6 13.8 4.2L16.5 17Z" if S.name == "rounded" else
            "M7.5 17L10.3 3H13.7L16.5 17Z")
    return [shell(body), shell(behind(_stick(S, 16.5), [body], 0)), dot(11, 9, 0.9), dot(13.4, 11.6, 0.9), dot(10.6, 13.8, 0.9),
            dot(12.6, 6.6, 0.8)]


@icon("gelato-pan", CAT, "A metal pan heaped with swirled gelato and a flat paddle stuck in it",
      tags=["gelato", "gelateria", "ice cream display", "italian ice cream", "paddle", "shop"])
def _(S):
    pan = poly([(2.5, 13), (21.5, 13), (20, 20.5), (4, 20.5)], closed=True, r=S.r)
    heap = ("M3.5 13C3.3 10.2 5.4 8.5 7.8 9.3C8.8 6.9 11.6 6.2 13.6 7.6C15.8 6.8 18.4 8 18.8 10.4"
            "C20.2 10.8 20.8 12 20.5 13Z")
    paddle = thick(seg(14.5, 10, 18.5, 3.5), 3.2, "butt" if S.name == "line" else "round")
    return [shell(pan), shell(behind(heap, [pan, paddle], 0.6)), shell(behind(paddle, [pan], 0.6)),
            line(seg(18.5, 3.5, 20, 1.3)), detail(seg(3, 15.8, 21, 15.8)), detail("M6.2 12.4Q8.2 10.6 10.6 11.8")]


@icon("ice-cream-cart", CAT, "A push cart with a freezer box, two wheels and a small striped umbrella",
      tags=["ice cream vendor", "street cart", "gelato cart", "vendor", "summer", "market"])
def _(S):
    box = rect(3, 9.5, 14, 8, min(S.R, 2))
    canopy = ("M3.5 6.5C3.5 3.8 6.8 2 10 2C13.2 2 16.5 3.8 16.5 6.5Z" if S.name == "rounded" else
              "M3.5 6.5L10 2L16.5 6.5Z")
    return [shell(box), shell(canopy), line(seg(10, 6.5, 10, 9.5)), detail(seg(10, 2.5, 10, 6.5)),
            shell(circle(6.5, 19.8, 1.9)), shell(circle(13.5, 19.8, 1.9)),
            line(poly([(17, 11.5), (19, 11.5), (21, 8.5)], r=S.r)), detail(seg(3, 12.5, 17, 12.5))]


@icon("ice-cream-scoop", CAT, "A scoop tool with a long handle and a round bowl holding a ball of ice cream",
      tags=["scoop", "disher", "ice cream server", "kitchen tool", "scooper", "gelato"])
def _(S):
    bowl = "M2.5 12.5H14.5A6 6 0 0 1 2.5 12.5Z"
    ball = circle(8.5, 9.5, 5)
    handle = thick(seg(14, 14, 21, 17.5), 3, "butt" if S.name == "line" else "round")
    return [shell(bowl), shell(behind(ball, [bowl], 0.6)), shell(behind(handle, [bowl], 0)),
            detail("M5.2 8.6Q8.5 6.4 11.8 8.6")]


@icon("ice-cream-maker", CAT, "A wooden bucket with a crank handle on top and a metal canister inside",
      tags=["ice cream churn", "hand crank", "churn", "homemade ice cream", "bucket", "kitchen"])
def _(S):
    bucket = poly([(4, 10), (20, 10), (18.5, 21), (5.5, 21)], closed=True, r=S.r)
    can = rect(8, 6.5, 8, 3.5, L(S, 0, 1))
    return [shell(bucket), shell(can), detail(seg(4.5, 13.5, 19.5, 13.5)), detail(seg(5, 17.5, 19, 17.5)),
            line(poly([(12, 6.5), (12, 3), (18.5, 3), (18.5, 5.5)], r=S.r))]


# =========================================================================== more sweets and cookies

def bump_circle(cx, cy, r, n, h, off=0.0):
    """Closed outline of a circle whose edge is made of n outward bumps of height about h."""
    def v(i):
        return polar(cx, cy, r, off + i * 360.0 / n)
    d = "M" + _p(v(0))
    for i in range(n):
        c = polar(cx, cy, r + 2 * h, off + (i + 0.5) * 360.0 / n)
        d += "Q" + _p(c) + " " + _p(v(i + 1))
    return d + "Z"


def heart_d(cx, cy, s, round_tip=False):
    """Heart outline about 19 wide and 16.5 tall at s = 1, centred on (cx, cy)."""
    def q(x, y):
        return f"{fmt(cx + (x - 12) * s)} {fmt(cy + (y - 12.5) * s)}"
    if round_tip:
        start = "M" + q(13.6, 20.2)
        first = "C" + q(13, 21) + " " + q(11, 21) + " " + q(10.4, 20.2) + "C" + q(6, 17.2) + " " + q(2.5, 13.5) + " " + q(2.5, 9.2)
        last = "C" + q(21.5, 13.5) + " " + q(18, 17.2) + " " + q(13.6, 20.2) + "Z"
    else:
        start = "M" + q(12, 21)
        first = "C" + q(6, 17.2) + " " + q(2.5, 13.5) + " " + q(2.5, 9.2)
        last = "C" + q(21.5, 13.5) + " " + q(18, 17.2) + " " + q(12, 21) + "Z"
    return (start + first +
            "C" + q(2.5, 6.2) + " " + q(4.6, 4.5) + " " + q(7, 4.5) +
            "C" + q(9.3, 4.5) + " " + q(11, 5.8) + " " + q(12, 7.5) +
            "C" + q(13, 5.8) + " " + q(14.7, 4.5) + " " + q(17, 4.5) +
            "C" + q(19.4, 4.5) + " " + q(21.5, 6.2) + " " + q(21.5, 9.2) + last)


@icon("dorayaki", CAT, "Two small round pancakes with a thick layer of sweet bean paste between them and a bite taken out",
      tags=["red bean pancake", "anko", "japanese sweet", "pancake sandwich", "wagashi", "bean paste"])
def _(S):
    top = "M2.5 10.2C2.5 6 6.5 4.2 12 4.2C17.5 4.2 21.5 6 21.5 10.2Z"
    bot = "M2.5 13.8C2.5 18 6.5 19.8 12 19.8C17.5 19.8 21.5 18 21.5 13.8Z"
    paste = rect(3.2, 9.8, 17.6, 4.4, L(S, 0, 2.2))
    body = union(top, paste, bot)
    body = minus(body, circle(21.8, 7.4, 3.3), circle(22, 13, 2))
    return [shell(body), detail(seg(2.8, 10.2, 15.5, 10.2)), detail(seg(2.8, 13.8, 15.5, 13.8)),
            dot(7, 12, 0.9), dot(11.5, 12, 0.9)]


@icon("chocolate-fountain", CAT, "A three-tier fountain with sheets of melted chocolate flowing down between the tiers",
      tags=["chocolate waterfall", "fondue", "melted chocolate", "buffet", "party", "dessert table"])
def _(S):
    r = L(S, 0.5, 1.3)
    basin = poly([(2, 16), (22, 16), (19.5, 21), (4.5, 21)], closed=True, r=S.r)
    parts = [shell(rect(8.5, 4.5, 7, 2.6, r)), shell(rect(5, 10.2, 14, 2.6, r)), shell(basin), dot(12, 2.4, 1)]
    for x in (10, 14):
        parts.append(line(seg(x, 7.1, x, 10.2)))
    for x in (7.5, 12, 16.5):
        parts.append(line(seg(x, 12.8, x, 16)))
    return parts


@icon("rolled-ice-cream", CAT, "A cup holding three upright tight rolls of ice cream with a swirl showing on each top",
      tags=["thai rolled ice cream", "stir-fried ice cream", "ice cream rolls", "street food", "frozen treat", "dessert"])
def _(S):
    cup = poly([(4, 14.5), (20, 14.5), (18, 21.5), (6, 21.5)], closed=True, r=S.r)
    tops = [(7, 7), (12, 4.6), (17, 7)]
    rolls = union(*[union(rect(cx - 2.5, ty, 5, 15 - ty, 0), ellipse(cx, ty, 2.5, 1.6)) for cx, ty in tops])
    parts = [shell(cup), shell(behind(rolls, [cup], 0))]
    for cx, ty in tops:
        parts.append(detail(f"M{fmt(cx - 2.5)} {fmt(ty)}A2.5 1.6 0 0 0 {fmt(cx + 2.5)} {fmt(ty)}"))
    parts += [detail(seg(9.5, 9.5, 9.5, 14.5)), detail(seg(14.5, 9.5, 14.5, 14.5))]
    return parts


@icon("sandwich-cookie", CAT, "Two round dark cookies with an embossed top and a layer of white cream between them",
      tags=["cream cookie", "cookies and cream", "creme biscuit", "sandwich biscuit", "chocolate cookie", "twist cookie"])
def _(S):
    cx, cy, rx = 12, 8.4, 9.5
    ry = L(S, 4.2, 4.8)
    body = union(ellipse(cx, cy, rx, ry), rect(cx - rx, cy, 2 * rx, 8.2, 0), ellipse(cx, cy + 8.2, rx, ry))
    parts = [shell(body), detail(f"M{fmt(cx - rx)} {fmt(cy + 3.6)}A{rx} {fmt(ry)} 0 0 0 {fmt(cx + rx)} {fmt(cy + 3.6)}")]
    for a in range(0, 360, 60):
        x, y = cx + 5.2 * math.cos(math.radians(a)), cy + 1.9 * math.sin(math.radians(a))
        parts.append(dot(x, y, 0.85))
    return parts


@icon("fortune-cookie", CAT, "A folded crescent cookie with a small paper slip poking out of the fold",
      tags=["chinese restaurant", "luck", "prediction", "paper slip", "takeout", "good fortune"])
def _(S):
    body = ("M2.5 9C3 16 7.5 20.2 12.5 20.2C17.5 20.2 21 17.4 21.5 12.4C19 15.4 15 15.4 12 13.4"
            "C9 11.4 7 8.8 6.6 4.6C4.6 5.4 3 6.8 2.5 9Z")
    slip = rot_d(rect(11.2, 3.2, 4.6, 9.2, L(S, 0, 1)), 28, 13.5, 8)
    return [shell(behind(slip, [body], 0)), shell(body)]


@icon("gingerbread-man", CAT, "A cookie shaped like a simple person with a round head, icing eyes, a smile and buttons",
      tags=["gingerbread", "christmas cookie", "holiday cookie", "cookie cutter", "ginger snap", "person cookie"])
def _(S):
    cap = L(S, "butt", "round")
    arms = thick(poly([(4, 10.8), (12, 10), (20, 10.8)]), 3.6, cap, "round")
    torso = thick(seg(12, 10, 12, 15), 6.4, "butt", "round")
    legs = thick(poly([(7, 21), (12, 15), (17, 21)]), 3.8, cap, "round")
    head = circle(12, 5.4, 3.6)
    body = union(head, arms, torso, legs)
    return [shell(body), dot(10.6, 4.7, 0.8), dot(13.4, 4.7, 0.8), dot(12, 12.2, 0.9), dot(12, 15.2, 0.9)]


@icon("gingerbread-house", CAT, "A small cookie house with an icing-trimmed pitched roof, candy dots and a door",
      tags=["christmas house", "holiday baking", "candy house", "winter treat", "icing", "hansel and gretel"])
def _(S):
    roof = poly([(2.5, 11.5), (12, 3), (21.5, 11.5)], closed=False)
    walls = poly([(4.5, 11.5), (4.5, 20.5), (19.5, 20.5), (19.5, 11.5)])
    body = poly([(2.5, 11.5), (12, 3), (21.5, 11.5), (19.5, 11.5), (19.5, 20.5), (4.5, 20.5), (4.5, 11.5)],
                closed=True, r=S.r)
    door = poly([(10, 20.5), (10, 15.5), (14, 15.5), (14, 20.5)], r=L(S, 0, 0.8))
    return [shell(body), detail(scallops(4.5, 19.5, 11.5, 3, 1.1)), detail(door),
            dot(12, 7.6, 0.9), dot(7.2, 16.4, 1), dot(16.8, 16.4, 1)]


@icon("lebkuchen", CAT, "A large heart-shaped gingerbread cookie with an iced inner border and a ribbon loop at the top",
      tags=["gingerbread heart", "german cookie", "christmas market", "honey cake", "love cookie", "ribbon"])
def _(S):
    big = heart_d(12, 14, 0.92, round_tip=(S.name == "rounded"))
    small = heart_d(12, 14.4, 0.5)
    return [shell(big), detail(small), line(circle(12, 3.6, 1.8))]


@icon("biscotti", CAT, "Two long oblong slices of twice-baked biscuit with nuts showing in the cut face",
      tags=["cantucci", "italian cookie", "twice baked", "almond biscuit", "coffee dunk", "crunchy cookie"])
def _(S):
    parts = []
    for cy, sh in ((7.6, 0.0), (16.4, 1.6)):
        h = 5.4
        pts = [(5 + sh, cy - h / 2), (21 + sh - 1.6, cy - h / 2), (19 + sh - 1.6, cy + h / 2), (3 + sh, cy + h / 2)]
        pts = [(x - 1.2, y) for x, y in pts]
        parts.append(shell(poly(pts, closed=True, r=S.r)))
        for k in (0, 1, 2):
            parts.append(dot(7.4 + sh + k * 4.6 - 1.2, cy, 0.9))
    return parts


@icon("shortbread", CAT, "A rectangular finger of shortbread with rows of pricked fork holes",
      tags=["scottish biscuit", "butter cookie", "tea biscuit", "finger biscuit", "pricked", "buttery"])
def _(S):
    body = rot_d(rect(7.5, 3, 9, 18, L(S, 0.8, 3)), 35)
    parts = [shell(body)]
    for row in range(4):
        for col in range(2):
            x, y = 9.9 + col * 4.2, 6.3 + row * 3.8
            (px, py), = rot_pts([(x, y)], 35)
            parts.append(dot(px, py, 0.95))
    return parts


@icon("thumbprint-cookie", CAT, "A thick round cookie with a rough edge seen at an angle, with a dip in the middle filled with jam",
      tags=["jam cookie", "jam drop", "linzer", "butter cookie", "holiday cookie", "fruit filled"])
def _(S):
    cx, cy, rx, ry, th = 12, 9.2, 9.5, 5.2, 5
    n, h = 10, L(S, 0.8, 0.5)
    top = "M" + _p((cx + rx, cy))
    for i in range(n):
        a0, a1 = 360.0 * i / n, 360.0 * (i + 1) / n
        c = ell_pt(cx, cy, rx + 2 * h, ry + 2 * h, (a0 + a1) / 2)
        top += "Q" + _p(c) + " " + _p(ell_pt(cx, cy, rx, ry, a1))
    top += "Z"
    body = union(top, rect(cx - rx, cy, 2 * rx, th, 0), ellipse(cx, cy + th, rx, ry))
    return [shell(body), detail(ellipse(cx, cy, 5, 2.4)), mark(ellipse(cx, cy + 0.1, 2.3, 1.05))]


@icon("coconut-macaroon", CAT, "A lumpy mound of shredded coconut with its base dipped in chocolate",
      tags=["macaroon", "coconut cookie", "coconut haystack", "passover", "chocolate dipped", "confection"])
def _(S):
    mound = union(circle(7.2, 12.2, 4.4), circle(12, 9, 5.6), circle(17, 12, 4.6), circle(9.6, 6.4, 3.2),
                  rect(2.8, 13.5, 18.4, 7, min(S.R, 2)))
    below = "M2 17.4Q5.5 15.6 8 17.4T14 17.4T20 17.4T23 17.4V22H2Z"
    dip = path_to_d(I(P(mound), P(below)))
    return [shell(mound), mark(dip), detail(seg(9.3, 11.5, 10.8, 10.6)), detail(seg(14, 12.5, 15.6, 13.4))]


def _clip_line(x0, y0, x1, y1, px, py, dx, dy):
    """Clip the infinite line through (px, py) with direction (dx, dy) to the rectangle; return M..L path or ''."""
    t0, t1 = -1e9, 1e9
    for p_, q_ in ((-dx, px - x0), (dx, x1 - px), (-dy, py - y0), (dy, y1 - py)):
        if abs(p_) < 1e-9:
            if q_ < 0:
                return ""
            continue
        t = q_ / p_
        if p_ < 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
    if t1 - t0 < 2.5:
        return ""
    return seg(px + dx * t0, py + dy * t0, px + dx * t1, py + dy * t1)


def _wafer_lattice(x, y, w, h, inset=0.0, step=6.0, shift=0.0):
    cx, cy = x + w / 2, y + h / 2
    out = []
    for k in (-1, 0, 1):
        for sgn in (1, -1):
            d = _clip_line(x + inset, y + inset, x + w - inset, y + h - inset, cx + shift + k * step, cy, 1, sgn)
            if d:
                out.append(d)
    return out


def _wafer_filled():
    x, y, w, h, dx, dy = 2.5, 8.5, 15, 12, 4, 4.5
    out = poly(box(x, y, w, h, dx, dy), closed=True)
    body = U(P(out), ST(out, 2, "butt", "miter", 4))
    edges = ST(poly([(x, y), (x + w, y), (x + w, y + h)]), 2, "butt", "miter", 4)
    diag = ST(seg(x + w, y, x + w + dx, y - dy), 2, "butt", "miter", 4)
    lat = [ST(d, 2, "butt", "miter", 4) for d in _wafer_lattice(x, y, w, h, inset=2.6, step=5.2)]
    return D(body, edges, diag, *lat)


@icon("wafer", CAT, "A thin rectangular wafer biscuit with a diamond waffle grid on top and layered sides",
      tags=["waffle biscuit", "wafer cookie", "layered wafer", "crisp", "snack bar", "sheet"],
      filled=_wafer_filled)
def _(S):
    x, y, w, h, dx, dy = 2.5, 8.5, 15, 12, 4, 4.5
    parts = list(box_parts(S, x, y, w, h, dx, dy))
    for d in _wafer_lattice(x, y, w, h, shift=1.5):
        parts.append(detail(d))
    return parts
