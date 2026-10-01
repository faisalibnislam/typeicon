"""TypeIcon Core: world dishes (batch dishes_002).

British, American, Japanese and Korean dishes, sandwiches, fried snacks, platters and seafood, drawn from
the food itself. Side views sit on a shallow plate or in a round bowl; top views sit on a round plate (r 9).
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


def taper(x1, y1, w1, x2, y2, w2):
    """Quad (d-string) that narrows from width w1 at (x1, y1) to w2 at (x2, y2): a drumstick or bone."""
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    return poly([(x1 + nx * w1 / 2, y1 + ny * w1 / 2), (x2 + nx * w2 / 2, y2 + ny * w2 / 2),
                 (x2 - nx * w2 / 2, y2 - ny * w2 / 2), (x1 - nx * w1 / 2, y1 - ny * w1 / 2)], closed=True)


def chord(cx, cy, r, ang, off):
    """Segment of a chord of the circle (cx, cy, r), direction ang degrees, shifted off px to the side (for scoring lines)."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    fx, fy = cx - uy * off, cy + ux * off
    h = math.sqrt(max(r * r - off * off, 0))
    return seg(fx - ux * h, fy - uy * h, fx + ux * h, fy + uy * h)


# =========================================================================== British and stews


@icon("goulash", CAT, "A cauldron of stew hanging from a tripod over a small fire",
      tags=["stew", "cauldron", "campfire", "hungarian", "soup", "kettle"])
def _(S):
    pot = ("M6 7.5H18C18 12.5 15.5 15.5 12 15.5C8.5 15.5 6 12.5 6 7.5Z" if S.name == "line" else
           "M7 7.5H17A1 1 0 0 1 18 8.5C17.8 12.5 15.4 15.5 12 15.5C8.6 15.5 6.2 12.5 6 8.5A1 1 0 0 1 7 7.5Z")
    flame = "M12 16.8C13.8 18.6 14.2 19.8 14.2 20.4C14.2 21.4 13.3 21.9 12 21.9C10.7 21.9 9.8 21.4 9.8 20.4C9.8 19.8 10.2 18.6 12 16.8Z"
    return [shell(pot), line(poly([(9.9, 7.5), (12, 3.6), (14.1, 7.5)])),
            line(seg(6.8, 15.5, 4.5, 21.5)), line(seg(17.2, 15.5, 19.5, 21.5)), solid(flame)]


@icon("borek", CAT, "A round coiled spiral pastry seen from above",
      tags=["pastry", "spiral", "filo", "turkish", "savory pie", "coil", "burek"], aliases=["burek"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(poly(spiral_pts(12, 12, 0.6, 5.0, 1.6, start=200, n=30)))]


@icon("chimney-cake", CAT, "A hollow spiral pastry cylinder with a helix groove",
      tags=["kurtoskalacs", "trdelnik", "spit cake", "sweet", "street food", "spiral"], aliases=["kurtoskalacs"])
def _(S):
    body = "M7 5.5V19A5 2.2 0 0 0 17 19V5.5A5 2.2 0 0 0 7 5.5Z"
    if S.name == "rounded":
        body = "M7 6V19A5 2.2 0 0 0 17 19V6A5 2.2 0 0 0 7 6Z"
    return [shell(body), detail("M7 6A5 2.2 0 0 0 17 6"), detail("M7 11.5Q12 15 17 12"), detail("M7 16.5Q12 20.5 17 17")]


@icon("fish-and-chips", CAT, "A battered fish fillet in front of chips standing in a paper tray",
      tags=["british", "takeaway", "fried fish", "chippy", "fries", "batter"])
def _(S):
    tray = poly([(9.5, 11.5), (22, 11.5), (20, 21.5), (11.5, 21.5)], closed=True, r=S.r)
    fish = union(ellipse(9, 16, 6.6, 4.2), poly([(4.5, 16), (1.8, 12.4), (1.8, 19.6)], closed=True, r=S.r))
    chips = [line(seg(13.5, 11.5, 13.5, 4)), line(seg(17.5, 11.5, 17.5, 4)), line(seg(21, 11.5, 21, 5.5))]
    return [shell(behind(tray, [fish], 1.25)), shell(fish)] + chips + [dot(11.5, 15, 0.9)]


@icon("shepherds-pie", CAT, "A baking dish with a peaked, ridged top of browned mashed potato",
      tags=["cottage pie", "mash", "minced meat", "baked dish", "british", "comfort food"], aliases=["cottage-pie"])
def _(S):
    dish = poly([(3.5, 13), (20.5, 13), (19, 21), (5, 21)], closed=True, r=S.r)
    peaks = poly([(6, 13.5), (6, 9), (8, 5), (10.5, 8.5), (12, 4.5), (13.5, 8.5), (16, 5), (18, 9), (18, 13.5)], closed=True, r=S.r)
    handles = [line(seg(1.5, 15, 3.5, 15)), line(seg(20.5, 15, 22.5, 15))]
    return [shell(union(dish, peaks)), detail(seg(3.5, 13, 20.5, 13))]


@icon("sausage-roll", CAT, "A flaky pastry log cut at one end to show the round meat centre, with slashes on top",
      tags=["pastry", "sausage meat", "bakery", "british", "snack", "puff pastry"])
def _(S):
    return [shell(hcyl(S, 2.5, 21.5, 7.5, 16.5, 3.4)), detail(arc_half(18.1, 12, 3.4, 4.5)), dot(18.1, 12, 1.2),
            detail(seg(6, 13, 9, 10)), detail(seg(10.5, 13, 13.5, 10))]


def arc_half(cx, cy, rx, ry):
    """Left half of an ellipse face (top to bottom), for the cut end of a cylinder."""
    return f"M{fmt(cx)} {fmt(cy - ry)}A{fmt(rx)} {fmt(ry)} 0 0 0 {fmt(cx)} {fmt(cy + ry)}"


@icon("yorkshire-pudding", CAT, "A puffed crisp pudding cup with risen jagged edges and a hollow centre",
      tags=["british", "roast dinner", "batter pudding", "popover", "sunday roast", "baked"])
def _(S):
    r = S.r
    top = [(3, 11.5), (4.4, 4.5), (8, 8.3), (12, 5.2), (16, 8.3), (19.6, 4.5), (21, 11.5)]
    d = poly(top, r=r) + "C21 16 19 20.5 16 20.5H8C5 20.5 3 16 3 11.5Z"
    return [shell(d)]


@icon("bangers-and-mash", CAT, "A mound of mashed potato with two sausages leaning against it",
      tags=["sausages", "mash", "british", "gravy", "comfort food", "pub food"])
def _(S):
    mound = "M4 15C4 8 7.5 4 12 4C16.5 4 20 8 20 15Z"
    sa = capsule(3.5, 20, 12, 15, 3.4)
    sb = capsule(20.5, 20, 12, 15, 3.4)
    return [shell(behind(mound, [sa, sb], 1.25)), shell(sa), shell(behind(sb, [sa], 1.25))]


@icon("pork-pie", CAT, "A tall round raised pie with a crimped top edge and a lid band",
      tags=["british", "picnic", "hand raised pie", "pastry", "meat pie", "crust"])
def _(S):
    top = [(4, 8)]
    n = 4
    for i in range(n):
        x = 4 + 16 * i / n
        top += [(x + 16 / n / 2, 5.4), (x + 16 / n, 8)]
    body = poly(top + [(18.5, 20.5), (5.5, 20.5)], closed=True, r=S.r * 0.5)
    return [shell(body), detail(seg(4.8, 12, 19.2, 12))]


@icon("beef-wellington", CAT, "A lattice-topped pastry log with one round slice cut off, showing its pink centre",
      tags=["pastry wrapped beef", "fillet", "british", "festive", "roast", "puff pastry"])
def _(S):
    log = rect(2.5, 3.5, 19, 8, 1.5 if S.name == "line" else 3.5)
    return [shell(log), detail(seg(7, 9, 9.5, 6)), detail(seg(11, 9, 13.5, 6)), detail(seg(15, 9, 17.5, 6)),
            shell(circle(12, 17, 4.5)), dot(12, 17, 1.6)]


@icon("roast-beef", CAT, "A roast joint of beef tied with twine, sitting on a plate",
      tags=["sunday roast", "joint", "carvery", "meat", "rib of beef", "dinner"])
def _(S):
    joint = "M2.5 11.5C2.5 8 5 6.5 8 6.5H16C19 6.5 21.5 8 21.5 11.5C21.5 15 19 16.5 16 16.5H8C5 16.5 2.5 15 2.5 11.5Z"
    return [shell(joint), detail(seg(8.5, 6.5, 7, 16.5)), detail(seg(13, 6.5, 11.5, 16.5)), detail(seg(17.5, 6.5, 16, 16.5)),
            plate(S, 18.5, 2.5, 21.5, 2.5)]


@icon("glazed-ham", CAT, "A whole ham on the bone with a diamond-scored surface",
      tags=["christmas ham", "gammon", "holiday", "cloves", "pork", "easter"])
def _(S):
    body = circle(10.5, 10.5, 8.2)
    bone = thick("M15.5 15.5L19.3 19.3", 3.0)
    ends = [circle(20.4, 18.6, 1.7), circle(18.6, 20.6, 1.7)] if S.name == "line" else [circle(19.9, 19.9, 2.4)]
    return [shell(union(body, bone, *ends)),
            detail(chord(10.5, 10.5, 7.4, 45, -3.4)), detail(chord(10.5, 10.5, 7.4, 45, 3.4)),
            detail(chord(10.5, 10.5, 7.4, -45, -3.4)), detail(chord(10.5, 10.5, 7.4, -45, 3.4))]


@icon("roast-chicken", CAT, "A whole roast chicken on a platter with its drumsticks raised",
      tags=["roast bird", "rotisserie", "sunday roast", "trussed", "poultry", "dinner"])
def _(S):
    body = ellipse(12, 13.2, 7.4, 4.8)
    leg1 = taper(8.3, 12, 5.4, 4.8, 6.4, 2.6)
    leg2 = taper(15.7, 12, 5.4, 19.2, 6.4, 2.6)
    return [shell(union(body, leg1, leg2, circle(4.4, 5.6, 2.0), circle(19.6, 5.6, 2.0))), plate(S, 18.5, 2.5, 21.5, 2.5)]


@icon("roast-turkey", CAT, "A plump roast turkey on a platter with paper frills on the leg bones",
      tags=["thanksgiving", "christmas", "holiday", "feast", "roast bird", "poultry"])
def _(S):
    body = ellipse(12, 13, 8.4, 5.2)
    leg1 = taper(7.6, 12, 5, 6.2, 7.6, 1.8)
    leg2 = taper(16.4, 12, 5, 17.8, 7.6, 1.8)
    return [shell(union(body, leg1, leg2)), line(poly([(4.4, 6.6), (5, 4.2), (5.9, 6), (6.9, 4.2), (7.7, 6.6)])),
            line(poly([(16.3, 6.6), (17.1, 4.2), (18, 6), (19, 4.2), (19.6, 6.6)])), plate(S, 18.5, 2.5, 21.5, 2.5)]


@icon("roast-duck", CAT, "A glossy whole roast duck hanging from a hook by its neck",
      tags=["peking duck", "hanging duck", "chinese roast", "cantonese", "poultry", "hook"])
def _(S):
    body = "M12 8.5C16 9 18.5 12 18.5 15C18.5 18 15.8 19.5 12 19.5C8.2 19.5 5.5 18 5.5 15C5.5 12 8 9 12 8.5Z"
    return [shell(body), line("M12 9V4.5A2.3 2.3 0 1 0 9.7 7"), line(seg(9.3, 19.5, 8.3, 22)), line(seg(14.7, 19.5, 15.7, 22)),
            detail("M8.6 13.5Q9.4 16.5 12.5 17")]


@icon("roast-pig", CAT, "A whole roast pig lying on a platter with crackled skin",
      tags=["suckling pig", "hog roast", "spit roast", "luau", "crackling", "feast"])
def _(S):
    body = rect(6, 6.5, 15, 9.5, 4.5 if S.name == "rounded" else 3)
    snout = rect(1.8, 9.2, 5.6, 5, 1.8 if S.name == "rounded" else 0.5)
    ear = poly([(8.2, 6.8), (9.4, 2.8), (12.8, 6.8)], closed=True)
    return [shell(union(body, snout, ear)), dot(8.5, 10.4, 1.0), dot(3.6, 11.8, 0.8), dot(14, 10.5, 1.0), dot(18, 10.8, 1.0),
            line(seg(9.5, 16, 9.5, 18.5)), line(seg(18, 16, 18, 18.5)), plate(S, 18.5, 2.5, 21.5, 2.5)]


@icon("crown-roast", CAT, "A ring of lamb ribs with the bones curving inwards and round frilled caps on the tips",
      tags=["rack of lamb", "pork crown", "christmas dinner", "roast", "ribs", "festive"])
def _(S):
    band = "M3 14.5Q12 17.5 21 14.5V19.5Q12 22.5 3 19.5Z"
    bones = [line(seg(5.2, 14.5, 6.6, 7)), line(seg(9.6, 15.3, 10.4, 6.5)), line(seg(14.4, 15.3, 13.6, 6.5)), line(seg(18.8, 14.5, 17.4, 7))]
    caps = [solid(circle(x, 5.2, 1.7)) for x in (6.8, 10.5, 13.5, 17.2)]
    return [shell(band)] + bones + caps


@icon("lamb-chop", CAT, "A single lamb chop with a long clean rib bone and a round eye of meat",
      tags=["cutlet", "rib chop", "lollipop chop", "grill", "meat", "bone"])
def _(S):
    if S.name == "line":
        meat = poly([(9, 10.5), (13, 8), (18.5, 10), (21, 14.5), (18.5, 19.5), (13, 20), (8.5, 15.5)], closed=True)
        ends = [circle(3.6, 5.8, 1.6), circle(5.8, 3.6, 1.6)]
    else:
        meat = "M9 10.5C12 7.8 17.5 9 19.6 13C21.2 17 17.5 20.6 13 19.8C9.4 19.1 7 14.5 9 10.5Z"
        ends = [circle(4.6, 4.8, 2.3)]
    bone = taper(10, 10.8, 3.4, 5.4, 6.2, 2.4)
    return [shell(union(meat, bone, *ends)), dot(14.3, 14.6, 1.8)]


@icon("bbq-ribs", CAT, "A rack of barbecued ribs with the bone ends sticking out of the glazed meat",
      tags=["spare ribs", "barbecue", "bbq", "baby back", "smokehouse", "grill"])
def _(S):
    slab = rect(8, 5.5, 13.5, 13, 3 if S.name == "rounded" else 1.5)
    bones = [line(seg(2.6, y, 8, y)) for y in (8.5, 12, 15.5)]
    return [shell(slab), detail(seg(8, 10.2, 21.5, 10.2)), detail(seg(8, 13.8, 21.5, 13.8))] + bones


@icon("brisket", CAT, "A slab of smoked beef with a dark bark edge, sliced across at one end",
      tags=["smoked beef", "bbq", "texas", "barbecue", "pitmaster", "meat"])
def _(S):
    slab = rect(2.5, 6.5, 19, 11, 3 if S.name == "rounded" else 1.5)
    return [shell(slab), detail(seg(2.5, 9.5, 21.5, 9.5)), detail(seg(14.5, 9.5, 14.5, 17.5)),
            detail(seg(18.3, 9.5, 18.3, 17.5))]


@icon("meatloaf", CAT, "A loaf of meat with a glaze stripe on top and one slice cut off",
      tags=["loaf", "ground beef", "comfort food", "dinner", "american", "glaze"])
def _(S):
    loaf = "M2.5 18.5V11C2.5 8 4.5 6.5 8 6.5C11.5 6.5 13.5 8 13.5 11V18.5Z" if S.name == "line" else (
        "M2.5 17.5V11C2.5 8 4.5 6.5 8 6.5C11.5 6.5 13.5 8 13.5 11V17.5A1.5 1.5 0 0 1 12 19H4A1.5 1.5 0 0 1 2.5 17.5Z")
    return [shell(loaf), detail("M5 11.5Q8 13.5 11 11.5"), shell(rect(17, 9, 4.5, 10, 1 if S.name == "line" else 2)),
            ] if False else [shell(loaf), detail(seg(2.5, 11.5, 13.5, 11.5)), shell(rect(17.2, 8.5, 4.3, 10.5, 1 if S.name == "line" else 2))]


@icon("pot-roast", CAT, "A dutch oven holding a meat joint surrounded by carrot chunks",
      tags=["casserole", "dutch oven", "stew", "braise", "sunday dinner", "carrots"])
def _(S):
    pot = ("M4.5 12.5H19.5V17C19.5 19.5 18 20.5 16 20.5H8C6 20.5 4.5 19.5 4.5 17Z" if S.name == "line" else
           "M5.5 12.5H18.5A1 1 0 0 1 19.5 13.5V17C19.5 19.5 18 20.5 16 20.5H8C6 20.5 4.5 19.5 4.5 17V13.5A1 1 0 0 1 5.5 12.5Z")
    joint = "M7 12.5C7 8.5 9.5 7 12 7C14.5 7 17 8.5 17 12.5Z"
    return [shell(pot), shell(behind(joint, [pot], None)), line(seg(1.8, 15, 4.5, 15)), line(seg(19.5, 15, 22.2, 15)),
            line(seg(4.8, 10, 4.8, 12.5)) if False else solid(capsule(3.6, 9.2, 5.8, 11.6, 2.6)), solid(capsule(20.4, 9.2, 18.2, 11.6, 2.6))]


@icon("chicken-pot-pie", CAT, "A round pie dish topped with a domed pastry lid with steam vent slits",
      tags=["pie", "pastry lid", "ramekin", "comfort food", "savory pie", "american"])
def _(S):
    dish = poly([(3, 14), (21, 14), (19, 21), (5, 21)], closed=True, r=S.r)
    dome = "M3.5 14.5C3.5 8.5 7.5 5 12 5C16.5 5 20.5 8.5 20.5 14.5Z"
    return [shell(union(dish, dome)), detail(seg(3, 14.3, 21, 14.3)), detail(seg(10, 8, 9.2, 11)), detail(seg(14, 8, 14.8, 11))]


@icon("baked-potato", CAT, "A baked potato with a split top, topped with a pat of butter",
      tags=["jacket potato", "spud", "butter", "side dish", "steakhouse", "loaded potato"])
def _(S):
    skin = rotd(ellipse(12, 14.5, 9.8, 6.2), -8, 12, 14.5)
    return [shell(union(skin, rect(9.8, 4.8, 4.6, 4, 0.8 if S.name == "line" else 1.6))), detail("M6.5 12.6Q12 15 17.5 12")]


@icon("mashed-potatoes", CAT, "A mound of mashed potatoes on a plate with a gravy well on top running down the side",
      tags=["mash", "pureed potato", "side dish", "gravy", "thanksgiving", "comfort food"])
def _(S):
    mound = "M4.5 18.5C4.5 13 7 9.5 8.8 8.8H15.2C17 9.5 19.5 13 19.5 18.5Z"
    return [shell(union(mound, ellipse(12, 8.8, 4.2, 2.2))), detail("M7.8 8.8A4.2 2.2 0 0 0 16.2 8.8"), line(seg(12, 11.4, 12, 14.4)),
            plate(S, 18.5, 2.5, 21.5, 2.5)]


@icon("deli-sandwich", CAT, "A tall sandwich on rye with stacked meat layers and a pickle on a toothpick",
      tags=["deli", "pastrami", "reuben", "new york", "lunch", "sub"])
def _(S):
    top = "M3.5 9.5C3.5 6.8 6.5 5.5 12 5.5C17.5 5.5 20.5 6.8 20.5 9.5Z"
    bottom = rect(3.5, 17, 17, 3.8, 1 if S.name == "line" else 1.9)
    return [shell(top), line(wave_d(3.5, 20.5, 12.2, 1.0, 5.8)), line(wave_d(3.5, 20.5, 15.0, 1.0, 5.8)), shell(bottom),
            line(seg(12, 5.5, 12, 2.5)), solid(circle(12, 2.6, 1.3))]


@icon("sub-sandwich", CAT, "A long split roll filled with lettuce, tomato and meat, seen from the side",
      tags=["hoagie", "submarine", "hero", "grinder", "footlong", "deli roll"], aliases=["hoagie"])
def _(S):
    top = "M2 11C2 7.8 4.5 6 8 6H16C19.5 6 22 7.8 22 11Z"
    bottom = "M2 15.5H22C22 18.5 20 20 17 20H7C4 20 2 18.5 2 15.5Z"
    return [shell(top), shell(bottom), line(wave_d(2.8, 21.2, 13.2, 0.9, 4.8))]


@icon("club-sandwich", CAT, "A triangular three-layer sandwich held together by a toothpick with a frilled top",
      tags=["triple decker", "toothpick", "layers", "lunch", "diner", "sandwich half"])
def _(S):
    tri = poly([(2.5, 21), (21.5, 21), (12, 7)], closed=True, r=S.r * 0.6)
    return [shell(tri), detail(seg(6.2, 15.5, 17.8, 15.5)), detail(seg(4.6, 18.3, 19.4, 18.3)),
            line(seg(12, 7, 12, 3.5)), solid(poly([(9.8, 3.6), (12, 1.8), (14.2, 3.6)], closed=True))] if False else [
        shell(tri), detail(seg(6.4, 14.5, 17.6, 14.5)), detail(seg(4.6, 17.8, 19.4, 17.8)), line(seg(12, 7.5, 12, 4)),
        solid(circle(12, 3, 1.4))]


@icon("grilled-cheese", CAT, "Two toasted bread slices pulled apart with strings of melted cheese between them",
      tags=["toastie", "melted cheese", "cheese pull", "toasted sandwich", "diner", "lunch"])
def _(S):
    r = 1.5 if S.name == "line" else 2.6
    return [shell(rect(3, 3.5, 18, 5, r)), shell(rect(3, 15.5, 18, 5, r)),
            line("M8 8.5Q10 12 8 15.5"), line("M12.5 8.5Q14.5 12 12.5 15.5"), line("M17 8.5Q18.5 12 17 15.5")]


@icon("lobster-roll", CAT, "A split-top bun overflowing with chunky lobster meat",
      tags=["seafood", "new england", "maine", "sandwich", "shellfish", "summer"])
def _(S):
    bun = rect(2.5, 12, 19, 8, 3.5 if S.name == "rounded" else 2)
    chunks = union(circle(7.5, 9.6, 3.2), circle(12.2, 8, 3.6), circle(16.8, 9.8, 3.1))
    return [shell(union(bun, chunks)), detail(seg(2.5, 12.6, 21.5, 12.6))]


@icon("open-sandwich", CAT, "A single slice of dark bread topped with overlapping egg slices and a herb sprig",
      tags=["smorrebrod", "tartine", "open faced", "toast", "scandinavian", "canape"], aliases=["smorrebrod"])
def _(S):
    bread = rect(2.5, 15.5, 19, 5, 1 if S.name == "line" else 2.4)
    e1 = circle(8.5, 11, 3.6)
    e2 = circle(15.5, 11, 3.6)
    return [shell(bread), shell(behind(e1, [e2], 1.0)), shell(e2), dot(8.5, 11, 1.0), dot(15.5, 11, 1.0),
            solid(leaf(12, 7.5, 13.8, 3.2, 1.3))]


@icon("banh-mi", CAT, "A crusty baguette split open with herb sprigs and pickled vegetables sticking out",
      tags=["vietnamese", "baguette", "sandwich", "pickled carrot", "cilantro", "street food"], aliases=["banh-mi-sandwich"])
def _(S):
    body = rect(2, 12, 20, 8, 4)
    return [shell(body), detail(seg(7, 18, 9.5, 14.5)), detail(seg(12, 18, 14.5, 14.5)), detail(seg(17, 18, 18.5, 15.5)),
            solid(leaf(7, 12.5, 5.6, 5.5, 1.4)), solid(leaf(12, 12.5, 12.4, 4.2, 1.5)), solid(leaf(17, 12.5, 19.4, 5.8, 1.4))]


@icon("katsu-sando", CAT, "A crustless white bread sandwich cut in half showing a thick breaded cutlet layer",
      tags=["cutlet sandwich", "japanese", "pork cutlet", "tonkatsu", "konbini", "sando"], aliases=["katsu-sandwich"])
def _(S):
    r = 1.2 if S.name == "line" else 2.6
    back = rect(7.5, 4, 14, 11, r)
    front = rect(2.5, 9.5, 14, 11, r)
    return [shell(behind(back, [front], 1.25)), shell(front), detail(seg(2.5, 13.6, 16.5, 13.6)), detail(seg(2.5, 17.2, 16.5, 17.2)),
            dot(6, 15.4, 0.8), dot(9.5, 15.4, 0.8), dot(13, 15.4, 0.8)] if False else [
        shell(behind(back, [front], 1.25)), shell(front), detail(seg(2.5, 13.5, 16.5, 13.5)), detail(seg(2.5, 17, 16.5, 17))]


@icon("gua-bao", CAT, "A folded steamed bun holding a slab of pork belly and a herb leaf",
      tags=["bao", "taiwanese", "pork belly", "steamed bun", "lotus leaf bun", "taiwanese burger"], aliases=["pork-belly-bun"])
def _(S):
    bun = ("M2.5 11.5C2.5 10.5 3 10 4 10H20C21 10 21.5 10.5 21.5 11.5C21.5 16.5 17.5 20.5 12 20.5C6.5 20.5 2.5 16.5 2.5 11.5Z" if S.name == "line" else
           "M3.5 10H20.5A1.5 1.5 0 0 1 21.5 11.5C21.5 16.5 17.5 20.5 12 20.5C6.5 20.5 2.5 16.5 2.5 11.5A1.5 1.5 0 0 1 3.5 10Z")
    slab = rect(5, 5.5, 12.5, 5.5, 1.2 if S.name == "line" else 2.4)
    return [shell(bun), shell(slab), solid(leaf(17, 6.5, 21, 2.8, 1.3))]


@icon("fish-sticks", CAT, "Three rectangular breaded fish fingers on a round plate",
      tags=["fish fingers", "breaded fish", "kids meal", "frozen food", "fried fish", "dinner"], aliases=["fish-fingers"])
def _(S):
    fingers = []
    for off in (-4.3, 0, 4.3):
        fingers.append(detail(rotd(rect(6.2, 12 + off - 1.5, 11.6, 3, 0.6 if S.name == "line" else 1.4), 0, 12, 12)))
    return [shell(circle(12, 12, 9.5))] + fingers


@icon("chicken-nuggets", CAT, "An open box of breaded chicken nuggets with a small dip cup beside it",
      tags=["chicken bites", "fried chicken", "fast food", "kids meal", "dipping sauce", "takeaway"])
def _(S):
    box = poly([(2.5, 12), (15.5, 12), (14, 21.5), (4, 21.5)], closed=True, r=S.r)
    nug = union(circle(6.2, 8.4, 2.9), circle(10.6, 7.2, 3.1), circle(13.4, 10.4, 2.6))
    cup = poly([(17.2, 15), (22, 15), (21.2, 21.5), (18, 21.5)], closed=True, r=S.r * 0.6)
    return [shell(box), shell(behind(nug, [box], 1.0)), shell(cup)]


@icon("fried-chicken-bucket", CAT, "A tapered striped paper bucket piled with fried chicken pieces over the rim",
      tags=["takeaway", "family meal", "drumsticks", "fast food", "crispy", "party bucket"])
def _(S):
    bucket = poly([(4.5, 11.5), (19.5, 11.5), (17.5, 21.5), (6.5, 21.5)], closed=True, r=S.r * 0.6)
    pile = union(circle(8, 9.5, 3.4), circle(13.2, 8, 3.8), circle(17.6, 10, 3.2), taper(9, 8.5, 3.2, 5.6, 4.2, 2), circle(5.2, 3.8, 1.7))
    return [shell(union(bucket, pile)), detail(seg(9.8, 12, 9, 21.5)), detail(seg(14.2, 12, 15, 21.5))]


@icon("chicken-wing", CAT, "A single bent chicken wing with a glaze drip",
      tags=["buffalo wing", "hot wing", "wingette", "bar food", "fried chicken", "sauce"])
def _(S):
    d1 = taper(9.5, 15, 6, 5.5, 6.5, 2.8)
    d2 = taper(9.5, 15, 6, 19.5, 8.5, 3.4)
    wing = union(d1, d2, circle(9.5, 15, 3), circle(4.6, 5.4, 1.9), circle(6.4, 4, 1.4) if S.name == "line" else circle(4.6, 5.4, 1.9))
    drip = "M17 15.6C18.4 17.4 18.8 18.2 18.8 18.9C18.8 19.8 18 20.3 17 20.3C16 20.3 15.2 19.8 15.2 18.9C15.2 18.2 15.6 17.4 17 15.6Z"
    return [shell(wing), solid(drip)]


@icon("onion-rings", CAT, "Two thick battered onion rings leaning against each other",
      tags=["fried onion", "bar snack", "side dish", "battered", "fast food", "appetizer"])
def _(S):
    front = circle(9.5, 13.6, 6.6)
    back = circle(16.5, 9.6, 5.4)
    return [shell(behind(back, [front], 1.25)), shell(front), detail(circle(9.5, 13.6, 3.3)),
            detail(behind(circle(16.5, 9.6, 2.5), [front], 1.0))]


@icon("potato-tots", CAT, "A paper tray holding small crispy cylinder-shaped potato bites",
      tags=["hash brown bites", "side dish", "fried potato", "diner", "snack"])
def _(S):
    tray = poly([(3, 13.5), (21, 13.5), (19, 21.5), (5, 21.5)], closed=True, r=S.r * 0.6)
    tots = [shell(behind(capsule(x, y0, x, y1, 3), [tray], 1.0)) for x, y0, y1 in ((6.6, 8, 10.5), (12, 6.5, 10), (17.4, 8, 10.5))]
    return [shell(tray)] + tots


@icon("poutine", CAT, "A bowl of fries covered with gravy and white cheese curds",
      tags=["canadian", "quebec", "fries and gravy", "cheese curds", "comfort food", "late night"])
def _(S):
    return [shell(bowl(S, 13)), line(seg(7, 13, 5.5, 5)), line(seg(12, 13, 12, 3.5)), line(seg(17, 13, 18.5, 5)),
            detail("M6 16.2Q9 18.2 12 16.2Q15 14.2 18 16.2")]


@icon("corn-dog", CAT, "A sausage coated in thick batter on a wooden stick with a zigzag of mustard",
      tags=["corndog", "fair food", "state fair", "hot dog on a stick", "battered sausage", "snack"])
def _(S):
    body = capsule(12, 5.5, 12, 15.5, 8)
    return [shell(body), detail(poly([(9.5, 8.8), (11, 10.8), (12.5, 8.8), (14, 10.8), (15.2, 9.2)])),
            line(seg(12, 16, 12, 22))]


@icon("frozen-dinner", CAT, "A divided tray seen from above with three compartments of food under film",
      tags=["tv dinner", "microwave meal", "ready meal", "convenience food", "tray meal", "frozen food"])
def _(S):
    tray = rect(2.5, 4, 19, 16, 1.5 if S.name == "line" else 3.5)
    return [shell(tray), detail(seg(10.5, 4, 10.5, 20)), detail(seg(10.5, 12, 21.5, 12)), dot(6.5, 12, 1.3),
            dot(16, 8, 1.1), dot(16, 16, 1.1)]


@icon("pigs-in-a-blanket", CAT, "Three small sausages each wrapped in a spiral strip of pastry",
      tags=["cocktail sausages", "party food", "appetizer", "sausage rolls", "finger food", "wrapped sausage"])
def _(S):
    out = []
    for y in (5.8, 12, 18.2):
        out.append(shell(capsule(5.2, y, 18.8, y, 4.4) if S.name == "rounded" else rect(3, y - 2.2, 18, 4.4, 0.8)))
        for x in (8.5, 12, 15.5):
            out.append(detail(seg(x - 1.4, y + 2.2, x + 1.4, y - 2.2)))
    return out


@icon("chips-and-dip", CAT, "A triangular tortilla chip dipping into a small round bowl of dip",
      tags=["nachos", "salsa", "guacamole", "party snack", "appetizer", "crisps"])
def _(S):
    bowlp = "M2.5 13.5H16.5C16.5 18.5 13.5 21.5 9.5 21.5C5.5 21.5 2.5 18.5 2.5 13.5Z"
    chip = rotd(poly([(7, 5), (17.5, 5), (12.2, 15)], closed=True, r=S.r), -22, 12, 10)
    return [shell(behind(chip, [bowlp], 1.0)), shell(bowlp)]


@icon("charcuterie-board", CAT, "A round serving board with a handle holding a cheese wedge, grapes and a cracker",
      tags=["cheese board", "grazing board", "antipasto", "appetizer", "party platter", "meat and cheese"])
def _(S):
    board = union(circle(10.5, 12, 8.6), rect(17, 10.6, 5, 2.8, 1.2))
    wedge = poly([(5.6, 9.2), (11, 7.6), (11, 11.6)], closed=True, r=0.0)
    cracker = rotd(rect(6, 14, 3.6, 3.6, 0.6), 20, 7.8, 15.8)
    return [shell(board), detail(wedge), detail(cracker), dot(14.2, 9.4, 1.2), dot(15.8, 12.4, 1.2), dot(13.2, 13.4, 1.2)]


@icon("canapes", CAT, "A serving tray holding a row of small bite-sized toasts with round toppings",
      tags=["hors d'oeuvres", "party food", "finger food", "appetizer", "reception", "bites"])
def _(S):
    bases = [solid(rect(x - 2.6, 11.5, 5.2, 3, 0.8 if S.name == "line" else 1.5)) for x in (5.6, 12, 18.4)]
    tops = [solid(circle(x, 8.6, 1.7)) for x in (5.6, 12, 18.4)]
    return [plate(S, 16.5, 2.5, 21.5, 3)] + bases + tops


@icon("crudites", CAT, "A cup of upright raw vegetable sticks beside a small bowl of dip",
      tags=["veggie sticks", "vegetable platter", "celery", "carrot sticks", "party snack", "dip"])
def _(S):
    cup = poly([(3.5, 11.5), (13.5, 11.5), (12, 21.5), (5, 21.5)], closed=True, r=S.r * 0.6)
    sticks = [line(seg(5.6, 11.5, 4, 3.5)), line(seg(8.6, 11.5, 8.6, 2.8)), line(seg(11.6, 11.5, 13.2, 4))]
    dip = "M15.5 15.5H22C22 19.5 20 21.5 18.75 21.5C17.5 21.5 15.5 19.5 15.5 15.5Z"
    return [shell(cup), shell(dip)] + sticks


@icon("seafood-tower", CAT, "A two-tier platter stand loaded with oysters and prawns on each dish",
      tags=["shellfish tower", "raw bar", "plateau de fruits de mer", "oysters", "prawns", "luxury"])
def _(S):
    top = "M6.5 9.5H17.5C17.5 12 15 13 12 13C9 13 6.5 12 6.5 9.5Z"
    bot = "M2.5 16H21.5C21.5 19 17.5 20 12 20C6.5 20 2.5 19 2.5 16Z"
    return [shell(top), shell(bot), line(seg(12, 13, 12, 16)), solid(circle(9.3, 7.4, 1.5)), solid(circle(14.7, 7.4, 1.5)),
            solid(circle(12, 5.6, 1.5)), solid(circle(5.5, 14, 1.5)), solid(circle(9.5, 13.6, 1.3)), solid(circle(14.5, 13.6, 1.3)),
            solid(circle(18.5, 14, 1.5))]


@icon("oyster-platter", CAT, "A round plate of crushed ice with two open oyster half shells and a lemon wedge",
      tags=["raw bar", "shellfish", "half shell", "seafood", "ice", "appetizer"])
def _(S):
    if S.name == "line":
        o1, o2 = leaf(5.3, 5.8, 11.5, 11.6, 3.4), leaf(18.7, 18.2, 12.5, 12.4, 3.4)
    else:
        o1, o2 = rotd(ellipse(8.4, 8.6, 4.6, 3.3), 45, 8.4, 8.6), rotd(ellipse(15.6, 15.4, 4.6, 3.3), 45, 15.6, 15.4)
    return [shell(circle(12, 12, 9.5)), detail(o1), detail(o2), detail("M15.6 6.6A3.4 3.4 0 0 1 18.4 9.6Z")]


@icon("shrimp-cocktail", CAT, "A stemmed glass of cocktail sauce with a prawn draped over the rim",
      tags=["prawn cocktail", "shrimp", "appetizer", "seafood", "sauce", "starter"])
def _(S):
    glass = "M4.5 9.5H19.5C19.5 13.5 16 15.5 12 15.5C8 15.5 4.5 13.5 4.5 9.5Z"
    prawn = union(thick("M9 9.5C9 3.5 17.5 2.5 19.5 8.5", 3.2), poly([(19.5, 8.5), (16.8, 12), (22, 11.6)], closed=True))
    return [shell(glass), line(seg(12, 15.5, 12, 20.5)), line(seg(8, 20.5, 16, 20.5)), solid(prawn)]


@icon("grilled-fish", CAT, "A whole fish seen from the side with diagonal grill marks across its body",
      tags=["bbq fish", "charred", "seafood", "sea bass", "mackerel", "dinner"])
def _(S):
    body = "M2.5 11.5C6 5.5 14 5.5 17 11.5C14 17.5 6 17.5 2.5 11.5Z" if S.name == "line" else "M2.8 11.5C6 5.8 13.8 5.8 16.8 11.5C13.8 17.2 6 17.2 2.8 11.5Z"
    tail = poly([(16, 11.5), (21.5, 6.5), (21.5, 16.5)], closed=True, r=S.r * 0.5)
    return [shell(union(body, tail)), detail(seg(7, 8.2, 9.5, 14.8)), detail(seg(11, 8.2, 13.5, 14.8)), dot(5.6, 10.5, 0.8) if False else dot(5.4, 10.6, 0.9)]


@icon("sashimi", CAT, "Three slices of raw fish leaning against each other in a row on a long plate",
      tags=["raw fish", "japanese", "salmon", "tuna", "sushi bar", "slices"])
def _(S):
    r = 1 if S.name == "line" else 2.2
    sl = [rotd(rect(x - 2.2, 4.5, 4.4, 10.5, r), 14, x, 10) for x in (6.5, 12, 17.5)]
    return [shell(sl[0]), shell(behind(sl[1], [sl[0]], 1.0)) if False else shell(sl[1]), shell(sl[2]), plate(S, 17.5, 2.5, 21.5, 3)] if False else [
        shell(sl[0]), shell(behind(sl[1], [sl[2]], 0.0) if False else sl[1]), shell(sl[2]), plate(S, 17.5, 2.5, 21.5, 3)]


@icon("maki-roll", CAT, "A round slice of sushi roll with a seaweed ring, white rice and fillings in the middle",
      tags=["sushi roll", "california roll", "japanese", "nori", "rice roll", "sushi"])
def _(S):
    fills = [(12, 9.6), (9.9, 13.2), (14.1, 13.2)]
    if S.name == "line":
        bits = [Part("dot", rect(x - 1.15, y - 1.15, 2.3, 2.3)) for x, y in fills]
    else:
        bits = [dot(x, y, 1.25) for x, y in fills]
    return [shell(circle(12, 12, 9.2)), detail(circle(12, 12, 6.2))] + bits


@icon("temaki", CAT, "A cone-shaped seaweed hand roll with rice and fillings sticking out of the open top",
      tags=["hand roll", "sushi cone", "nori", "japanese", "rice", "sushi"])
def _(S):
    cone = poly([(4.5, 9.5), (12, 21.5), (19.5, 9.5)], closed=True, r=S.r * 0.8)
    return [shell(union(cone, ellipse(12, 9.5, 7.5, 2.4))), detail("M4.8 9.5A7.2 2.2 0 0 0 19.2 9.5"),
            solid(leaf(9, 8.5, 7.4, 3, 1.3)), solid(leaf(12.5, 8.4, 13, 2.4, 1.3)), solid(leaf(16, 8.6, 18.4, 4, 1.2))]


@icon("gunkan", CAT, "A warship-style sushi with a tall seaweed band around rice, topped with round fish roe",
      tags=["gunkan maki", "ikura", "roe", "salmon roe", "sushi", "battleship sushi"], aliases=["gunkan-maki"])
def _(S):
    band = rect(5, 9.5, 14, 10.5, 2.2 if S.name == "rounded" else 1.2)
    roe = [solid(circle(x, y, 1.75)) for x, y in ((8.4, 6.6), (12, 5.6), (15.6, 6.6))]
    return [shell(band)] + roe


@icon("inarizushi", CAT, "A plump pouch of fried tofu skin stuffed with rice and open slightly at the top",
      tags=["inari", "tofu pouch", "sushi", "japanese", "aburaage", "rice pouch"], aliases=["inari-sushi", "inari"])
def _(S):
    r = 1.2 if S.name == "line" else 3.6
    body = poly([(3, 19.5), (3, 10.5), (8.5, 10.5), (12, 12.5), (15.5, 10.5), (21, 10.5), (21, 19.5)], closed=True, r=r)
    rice = union(circle(9.6, 8.4, 2.4), circle(14.4, 8.4, 2.4), circle(12, 6.2, 2.4))
    return [shell(body), solid(rice)]


@icon("onigiri", CAT, "A triangular rice ball with rounded corners and a seaweed band at the base",
      tags=["rice ball", "japanese", "nori", "lunch", "konbini", "snack"])
def _(S):
    tri = poly([(12, 3.5), (21, 19.5), (3, 19.5)], closed=True, r=S.r + 1.4)
    return [shell(tri), detail("M9.3 19.5V14.6H14.7V19.5")]


@icon("musubi", CAT, "A block of rice topped with a slice of meat and wrapped with a band of seaweed",
      tags=["hawaiian snack", "hawaiian", "rice block", "nori", "snack", "lunch"])
def _(S):
    r = 1.2 if S.name == "line" else 2.2
    return [shell(rect(4, 11.5, 16, 8.5, r)), shell(rect(2.5, 4.5, 19, 5.5, r)), Part("dot", rect(9.5, 4.5, 5, 15.5))]


@icon("tempura", CAT, "A battered prawn with a bumpy crispy coating and a tail fan at one end",
      tags=["fried shrimp", "ebi", "japanese", "battered", "deep fried", "prawn"])
def _(S):
    cap = capsule(6.5, 16, 15, 10, 8)
    a = math.radians(-35)
    ux, uy = math.cos(a), math.sin(a)
    lumps = []
    for t in (0.0, 0.5, 1.0):
        cx, cy = 6.5 + (15 - 6.5) * t, 16 + (10 - 16) * t
        for sgn in (-1, 1):
            lumps.append(circle(cx - uy * sgn * 4, cy + ux * sgn * 4, 1.5))
    tail = poly([(15.5, 10.2), (17.6, 4), (19.4, 7.4), (22, 6.2), (20, 12.4)], closed=True, r=S.r * 0.4)
    return [shell(union(cap, tail, *lumps))]


@icon("takoyaki", CAT, "A boat-shaped paper tray of round batter balls with a sauce zigzag and a toothpick",
      tags=["octopus balls", "japanese", "street food", "osaka", "festival", "snack"])
def _(S):
    tray = "M2.5 14.5H21.5C21 18.5 19 20.5 16.5 20.5H7.5C5 20.5 3 18.5 2.5 14.5Z"
    balls = union(circle(7, 11, 3.6), circle(12.5, 10.5, 3.9), circle(17.6, 11.4, 3.4))
    return [shell(tray), shell(behind(balls, [tray], 1.0)), detail(poly([(6, 9), (8.5, 11.5), (11, 8.5), (13.5, 11.5), (16, 9), (18, 11)])) if False else
            line(poly([(6.5, 9.4), (9, 11.4), (11.5, 8.6), (14, 11.4), (16.5, 9.4)])), line(seg(17.5, 7.5, 21.5, 3)), ]


@icon("okonomiyaki", CAT, "A thick round savory pancake with zigzag lines of sauce and mayonnaise across the top",
      tags=["japanese pancake", "osaka", "savory pancake", "sauce", "mayonnaise", "teppanyaki"])
def _(S):
    body = "M2.5 9.5V16A9.5 3.6 0 0 0 21.5 16V9.5A9.5 3.6 0 0 0 2.5 9.5Z"
    return [shell(body), detail("M2.5 9.5A9.5 3.6 0 0 0 21.5 9.5"), detail(poly([(6.5, 8.4), (8.6, 6.6), (10.6, 8.6), (12.6, 6.6), (14.6, 8.6), (16.6, 6.8), (17.6, 7.6)]))]


@icon("zaru-soba", CAT, "A square bamboo tray of cold buckwheat noodles with a cup of dipping sauce beside it",
      tags=["cold noodles", "japanese", "buckwheat", "mori soba", "dipping sauce", "summer"])
def _(S):
    r = 1 if S.name == "line" else 2.2
    return [shell(rect(2.5, 3.5, 12.5, 17, r)), detail(wave_d(5.5, 12, 8, 0.9, 3.5)), detail(wave_d(5.5, 12, 12, 0.9, 3.5)),
            detail(wave_d(5.5, 12, 16, 0.9, 3.5)), shell(circle(19, 14, 3.1)), Part("dot", circle(19, 14, 0.9))]


@icon("curry-rice", CAT, "A top view of an oval plate with white rice on one side and chunky curry on the other",
      tags=["japanese curry", "katsu curry", "kare raisu", "curry", "rice", "comfort food"])
def _(S):
    plate_ = ellipse(12, 12, 10, 8) if S.name == "line" else rect(2, 4, 20, 16, 8)
    return [shell(plate_), detail("M11 4.6Q8.6 8.6 11 12Q13.4 15.4 11 19.4"), dot(16.6, 9, 1.4), dot(17, 14.4, 1.4),
            dot(6.4, 9.4, 0.8), dot(7.6, 13.4, 0.8), dot(7, 16.4, 0.8)]


@icon("miso-soup", CAT, "A lacquer soup bowl with its lid lifted aside and tofu cubes floating in the broth",
      tags=["japanese", "soup", "tofu", "seaweed", "breakfast", "bowl"])
def _(S):
    bowlp = bowl(S, 12.5)
    lid = rotd("M3.5 11H20.5C20.5 7 16.5 6 12 6C7.5 6 3.5 7 3.5 11Z", -16, 4, 11, 0, -0.5)
    return [shell(bowlp), shell(behind(lid, [bowlp], 1.0) if False else lid), solid(rect(14, 9.6, 2.4, 2.4, 0.3)), solid(rect(17.6, 10.4, 2, 2, 0.3))]


@icon("narutomaki", CAT, "A round slice of fish cake with a wavy scalloped edge and a spiral swirl in the middle",
      tags=["fish cake", "kamaboko", "ramen topping", "japanese", "swirl", "swirl fish cake"])
def _(S):
    edge = poly(star_ring(12, 12, 9.6, 8.4, 14), closed=True) if S.name == "line" else scallop_ring(12, 12, 8.7, 14, 1.15)
    return [shell(edge), detail(poly(spiral_pts(12, 12, 0.6, 4.3, 1.15, start=200, n=24)))]


@icon("oden", CAT, "A skewer holding a triangle, a ball and a cylinder of simmered fish cake and vegetables",
      tags=["japanese", "hot pot", "winter", "konbini", "simmered", "skewer"])
def _(S):
    return [line(seg(12, 1.5, 12, 22.5)), shell(poly([(12, 2.8), (17.4, 9.2), (6.6, 9.2)], closed=True, r=S.r * 0.4)),
            shell(circle(12, 13.6, 3.3)), shell(rect(8.6, 18, 6.8, 4, 0.8 if S.name == "line" else 1.8))] if False else [
        shell(poly([(12, 2.8), (17.4, 9), (6.6, 9)], closed=True, r=S.r * 0.4)), shell(circle(12, 13.4, 2.9)),
        shell(rect(8.8, 18.2, 6.4, 3.6, 0.8 if S.name == "line" else 1.6)), line(seg(12, 1.2, 12, 2.8)), line(seg(12, 22.4, 12, 22.4))]


@icon("omurice", CAT, "An oval omelette dome over rice on a plate with a zigzag of ketchup on top",
      tags=["omelette rice", "japanese", "yoshoku", "ketchup", "egg", "comfort food"])
def _(S):
    return [shell(ellipse(12, 12.4, 9.6, 5.8)), detail(poly([(6.4, 12), (8.4, 9.2), (10.4, 12.4), (12.4, 9.2), (14.4, 12.4), (16.4, 9.2), (18.2, 12)])),
            plate(S, 18.5, 2.5, 21.5, 2.5)]


@icon("bibimbap", CAT, "A stone bowl seen from above with toppings in separate sections around an egg yolk",
      tags=["korean", "mixed rice", "dolsot", "egg", "vegetables", "rice bowl"])
def _(S):
    arcs = [detail(arc(12, 12, 6.3, -90 + 72 * k + 10, -90 + 72 * k + 62)) for k in range(5)]
    return [shell(circle(12, 12, 9.4))] + arcs + [dot(12, 12, 2.1)]


@icon("kimchi", CAT, "A glass jar packed with fermented cabbage leaves and chili flakes",
      tags=["korean", "fermented", "napa cabbage", "pickled", "side dish", "banchan"])
def _(S):
    jar = rect(4.5, 7, 15, 14, 1.5 if S.name == "line" else 3.6)
    return [shell(jar), shell(rect(6.5, 3, 11, 3, 0.5 if S.name == "line" else 1.4)), detail(wave_d(6.5, 17.5, 11.5, 1.0, 5.5)),
            detail(wave_d(6.5, 17.5, 15.5, 1.0, 5.5)), dot(9, 18, 0.9), dot(15, 18.4, 0.9)]


@icon("tteokbokki", CAT, "A shallow pan of cylinder rice cakes in a thick red sauce with sesame seeds",
      tags=["korean", "rice cakes", "street food", "spicy", "gochujang", "snack"])
def _(S):
    def cake(off):
        a = math.radians(-30)
        ux, uy = math.cos(a), math.sin(a)
        cx, cy = 11 - uy * off, 12 + ux * off
        return detail(capsule(cx - ux * 1.8, cy - uy * 1.8, cx + ux * 1.8, cy + uy * 1.8, 2.6))
    return [shell(circle(11, 12, 8.8)), line(seg(19.8, 12, 22.4, 12)), cake(-5.2), cake(0), cake(5.2)]


@icon("banchan", CAT, "Four small round side dishes with different contents arranged together",
      tags=["korean", "side dishes", "small plates", "sharing", "kimchi", "meal"])
def _(S):
    return [shell(circle(6.5, 6.5, 3.6)), shell(circle(17.5, 6.5, 3.6)), shell(circle(6.5, 17.5, 3.6)), shell(circle(17.5, 17.5, 3.6)),
            dot(6.5, 6.5, 1.0), dot(16.5, 6.5, 0.8), dot(18.5, 6.5, 0.8), detail(seg(5.3, 17.5, 7.7, 17.5)),
            Part("dot", poly([(17.5, 16.2), (18.8, 18.4), (16.2, 18.4)], closed=True))]


@icon("spring-roll", CAT, "Two crisp cylindrical rolls with blistered skin, one cut at the end to show the filling",
      tags=["egg roll", "fried roll", "chinese", "vietnamese", "appetizer", "dim sum"])
def _(S):
    roll = rect(3, 4, 15, 7, 3.5) if S.name == "line" else capsule(6.5, 7.5, 17.5, 7.5, 7)
    return [shell(roll), dot(7.5, 7.5, 0.8), dot(12, 7.5, 0.8), shell(hcyl(S, 3, 21, 13.8, 20.8, 3.4)),
            detail(arc_half(17.6, 17.3, 3.4, 3.5)), dot(17.6, 17.3, 1.1)]


@icon("combo-meal", CAT, "A burger, a carton of fries and a drink cup with a straw grouped together",
      tags=["value meal", "fast food", "burger and fries", "takeaway", "kids meal", "drive thru"])
def _(S):
    r = 0.8 if S.name == "line" else 1.4
    cup = poly([(16.5, 9), (22, 9), (21, 20.5), (17.5, 20.5)], closed=True, r=S.r * 0.4)
    fries = poly([(9.5, 13.5), (15, 13.5), (14.2, 20.5), (10.3, 20.5)], closed=True, r=S.r * 0.4)
    return [shell(cup), line(seg(16, 9, 22.5, 9)), line(poly([(19.4, 9), (19.8, 4), (22, 3.2)])), shell(fries),
            line(seg(10.6, 13.5, 10, 8)), line(seg(12.3, 13.5, 12.3, 7)), line(seg(14, 13.5, 14.6, 8)),
            solid("M2 14C2 11 4 9.6 5.8 9.6C7.6 9.6 9.4 11 9.4 14Z"), solid(rect(2, 15, 7.4, 1.6, 0.6)), solid(rect(2, 17.6, 7.4, 2.8, 1.2))]
