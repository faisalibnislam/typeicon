"""TypeIcon Core: world dishes (batch dishes_005).

Southeast and South Asian, Middle Eastern, African and other world dishes, salads, bowls, soups and classic
plates, drawn from the food itself. Side views sit on a shallow plate or in a round bowl; top views sit on a
round plate (r 9).
"""
import math
import re

from dsl import Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, LINE, P, ST, U, fmt, path_to_d, rotation, transform_path  # noqa: F401

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

def holey(name, desc, tags, holes, aliases=()):
    """Like @icon, but the Filled design has real holes (d-strings) cut through it."""
    def deco(fn):
        def filled():
            base = filled_region(fn(LINE))
            for h in holes:
                base = D(base, P(h))
            return base
        icon(name, CAT, desc, tags=tags, aliases=aliases, filled=filled)(fn)
        return fn
    return deco


def steam(S, x, y0=7.5, h=4.5, amp=1.2):
    """A short wavy steam line from (x, y0) going up by h."""
    return line(f"M{fmt(x)} {fmt(y0)}Q{fmt(x + amp * 2)} {fmt(y0 - h / 4)} {fmt(x)} {fmt(y0 - h / 2)}"
                f"Q{fmt(x - amp * 2)} {fmt(y0 - h * 0.75)} {fmt(x)} {fmt(y0 - h)}")


def claw(cx, cy, r, mid, half=36):
    """Pincer: a disc with a wedge-shaped mouth centred on angle mid (degrees, 0 = right, clockwise)."""
    a0, a1 = pt_on(cx, cy, r, mid + half), pt_on(cx, cy, r, mid - half)
    return (f"M{fmt(cx)} {fmt(cy)}L{fmt(a0[0])} {fmt(a0[1])}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(a1[0])} {fmt(a1[1])}Z")


def curl(cx, cy, r, mid=-40, gap=70):
    """Open C-shaped arc (a curled shrimp) whose opening faces angle mid."""
    return arc(cx, cy, r, mid + gap / 2, mid - gap / 2 + 360)


def cube(x, y, s=4.0, rx=0.8, deg=0.0):
    d = rect(x, y, s, s, rx)
    return d if not deg else rotd(d, deg, x + s / 2, y + s / 2)


# =========================================================================== soups and breakfast


@icon("kaya-toast", CAT, "A slice of toast with a thick block of butter sitting on it",
      tags=["kaya", "coconut jam", "butter toast", "singapore", "breakfast", "toast sandwich", "malaysian"])
def _(S):
    return [shell(toast(S)), blob(7.5, 9, 9, 6, L(S, 0.5, 1.25))]


@icon("minestrone", CAT, "A bowl of soup heaped with beans and pasta tubes above the rim",
      tags=["vegetable soup", "italian soup", "pasta soup", "beans", "bowl", "hearty soup"])
def _(S):
    mound = bumps([(5, 11.5), (7.5, 6.8), (12, 4.5), (16.5, 6.8), (19, 11.5)], r=3.6) + "Z"
    return [shell(bowl(S, 12)), shell(mound), dot(8.8, 9, 1.2), dot(12, 6.6, 1.2), dot(15.2, 9, 1.2)]


@icon("egg-drop-soup", CAT, "A bowl of broth with thin egg ribbons drifting above it and a spoon",
      tags=["egg flower soup", "chinese soup", "broth", "ribbons", "spoon", "starter"])
def _(S):
    return [shell(bowl(S, 12)), line(wave_d(4.5, 13.5, 8.2, 1.1, 9)), line(wave_d(7.5, 13.5, 4.8, 0.9, 6)),
            line(poly([(16, 10), (20.5, 3.5)]))]


@icon("chicken-noodle-soup", CAT, "A mug of soup with noodles curling over the rim and carrot coins inside",
      tags=["chicken soup", "noodle soup", "mug", "comfort food", "cold remedy", "broth"])
def _(S):
    body = ("M4.5 10H15V17C15 19.5 13.5 21 11 21H8.5C6 21 4.5 19.5 4.5 17Z" if S.name == "line" else
            "M6 10H14A1 1 0 0 1 15 11V17C15 19.5 13.5 21 11 21H8.5C6 21 4.5 19.5 4.5 17V11.5A1.5 1.5 0 0 1 6 10Z")
    handle = "M15 12H17.5A2 2 0 0 1 19.5 14V15A2 2 0 0 1 17.5 17H15"
    return [shell(body), line(handle), line(wave_d(5.5, 13.5, 6.8, 1.2, 8)),
            dot(8.2, 14.2, 1.15), dot(11.6, 16.2, 1.15)]


def bowl2(S, top, x0, x1, d):
    """A round-bottomed bowl with a flat rim at y=top, from x0 to x1, depth d (side view)."""
    xm = (x0 + x1) / 2
    w = (x1 - x0) / 2
    b = top + d
    if S.name == "line":
        return (f"M{fmt(x0)} {fmt(top)}H{fmt(x1)}C{fmt(x1)} {fmt(top + d * 0.55)} {fmt(xm + w * 0.55)} {fmt(b)} {fmt(xm)} {fmt(b)}"
                f"C{fmt(xm - w * 0.55)} {fmt(b)} {fmt(x0)} {fmt(top + d * 0.55)} {fmt(x0)} {fmt(top)}Z")
    k = 1.5
    return (f"M{fmt(x0 + k)} {fmt(top)}H{fmt(x1 - k)}A{fmt(k)} {fmt(k)} 0 0 1 {fmt(x1 - 0.1)} {fmt(top + k)}"
            f"C{fmt(x1 - 0.6)} {fmt(top + d * 0.6)} {fmt(xm + w * 0.55)} {fmt(b)} {fmt(xm)} {fmt(b)}"
            f"C{fmt(xm - w * 0.55)} {fmt(b)} {fmt(x0 + 0.6)} {fmt(top + d * 0.6)} {fmt(x0 + 0.1)} {fmt(top + k)}"
            f"A{fmt(k)} {fmt(k)} 0 0 1 {fmt(x0 + k)} {fmt(top)}Z")


@icon("kimchi-stew", CAT, "An earthenware pot on a trivet with tofu cubes and bubbles rising from the stew",
      tags=["kimchi jjigae", "korean stew", "hot pot", "tofu", "earthenware", "spicy stew", "ttukbaegi"])
def _(S):
    return [shell(bowl2(S, 11, 4.5, 19.5, 8)), shell(cube(6.6, 6, 3.8, L(S, 0.3, 0.9))),
            shell(cube(12.6, 5.4, 3.8, L(S, 0.3, 0.9))), dot(18.2, 6.8, 1.1), dot(17.3, 3.6, 0.9), line(seg(7, 21.2, 17, 21.2))]


@icon("lobster-bisque", CAT, "A bowl of smooth soup with a cream swirl and a lobster claw on the rim",
      tags=["bisque", "lobster soup", "seafood soup", "claw", "cream soup", "shellfish", "fine dining"])
def _(S):
    cx, cy, r = 16.3, 7.3, 4.2
    a0, a1 = pt_on(cx, cy, r, -12), pt_on(cx, cy, r, -78)
    claw = f"M{fmt(cx)} {fmt(cy)}L{fmt(a0[0])} {fmt(a0[1])}A{r} {r} 0 1 1 {fmt(a1[0])} {fmt(a1[1])}Z"
    swirl = poly(spiral_pts(8, 7.6, 0.4, 3.4, 1.4, start=200, n=28))
    return [shell(bowl(S, 12)), shell(claw), line(swirl)]


@icon("pumpkin-soup", CAT, "Soup served in a hollowed pumpkin with its stemmed lid leaning beside it",
      tags=["pumpkin", "squash soup", "autumn", "fall", "halloween", "harvest", "seasonal"])
def _(S):
    body = ("M6 10H18C21.6 11.6 22 15.6 20 18.6C18.3 21 15 21.5 12 21.5C9 21.5 5.7 21 4 18.6C2 15.6 2.4 11.6 6 10Z")
    lid = rotd("M13.5 9C13.5 5.3 18.5 5.3 18.5 9Z", 22, 13.5, 9)
    stem = xf("M16 5.6V3.2", 22, 13.5, 9)
    return [shell(body), detail("M9.3 11C7.6 13.5 7.6 18 9.6 21"), detail("M14.7 11C16.4 13.5 16.4 18 14.4 21"),
            shell(lid), line(stem)]


def drum(ang, dx, dy):
    """Upright drumstick (bulb on top) rotated clockwise by ang about the centre, then shifted."""
    def f(d):
        return xf(d, ang, 12, 12, dx=dx, dy=dy)
    k = [(p[0] + dx, p[1] + dy) for p in rot_pts([(10.2, 20.6), (13.8, 20.6)], ang, 12, 12)]
    meat = f("M6.6 11.4A7 7 0 1 1 17.4 11.4Q14.6 13.8 14 17.5L10 17.5Q9.4 13.8 6.6 11.4Z")
    return meat, f("M12 17.5V20.6"), k, f


@icon("tandoori-chicken", CAT, "A chicken drumstick with diagonal slash cuts and char spots beside an onion ring",
      tags=["tandoor", "grilled chicken", "indian", "drumstick", "chicken leg", "spiced chicken", "barbecue"])
def _(S):
    meat, bone, kn, f = drum(45, -1.5, -0.5)
    return [shell(meat), detail(f("M8 6.6H13.2")), detail(f("M10.8 10.6H16")), line(bone),
            dot(kn[0][0], kn[0][1], 1.6), dot(kn[1][0], kn[1][1], 1.6), shell(circle(18.7, 18.7, 2.7)), dot(18.7, 18.7, 0.8)]


@icon("palak-paneer", CAT, "A bowl of dark creamed greens dotted with square white cheese cubes",
      tags=["saag paneer", "spinach curry", "indian cheese", "vegetarian curry", "greens", "cottage cheese cubes"],
      aliases=["saag-paneer"])
def _(S):
    return [shell(bowl(S, 12)), shell(leaf(4.8, 10.6, 11.2, 4.4, 2.3)), detail(seg(6.2, 9.2, 9.6, 6)),
            shell(cube(13, 4.8, 5, L(S, 0.3, 1), 10))]


@holey("medu-vada", "A ring-shaped lentil fritter with a hole in the middle beside a small bowl of sambar",
       ["vada", "south indian", "lentil doughnut", "fritter", "sambar", "breakfast snack", "urad dal"],
       [circle(8.5, 8.5, 2.3)], aliases=["medu-wada"])
def _(S):
    return [shell(circle(8.5, 8.5, 5.8)), shell(circle(8.5, 8.5, 2.3)), shell(bowl2(S, 15.5, 12, 21.5, 5)),
            dot(17, 18, 1)]


@icon("bhel-puri", CAT, "A paper cone of puffed rice snack mix with a flat crisp stuck in the top",
      tags=["chaat", "puffed rice", "indian street food", "mumbai", "snack cone", "murmura", "puri"])
def _(S):
    cone = poly([(4.5, 11.5), (19.5, 11.5), (12, 21.5)], closed=True, r=L(S, 0, 1.2))
    heap = bumps([(5.2, 10.5), (7.6, 6.4), (12, 5.6), (16.4, 6.4), (18.8, 10.5)], r=3.4) + "Z"
    crisp = rotd(ellipse(17.6, 5.6, 3.6, 2.2), -45, 17.6, 5.6)
    return [shell(cone), shell(heap), dot(9.3, 8.7, 1), dot(13.2, 8.4, 1), shell(crisp), detail(seg(6.5, 11.5, 17.5, 11.5))]


@icon("jianbing", CAT, "A folded square crepe with egg and two crisp crackers sticking out of the open end",
      tags=["chinese crepe", "breakfast crepe", "street food", "egg pancake", "tianjin", "cracker", "scallion"])
def _(S):
    crepe = rect(3.5, 10.5, 17, 10.5, L(S, 1.5, 3))
    c1 = rotd(rect(5.8, 3.5, 5, 9, L(S, 0.3, 1)), -16, 8.3, 12)
    c2 = rotd(rect(13.2, 3.5, 5, 9, L(S, 0.3, 1)), 16, 15.7, 12)
    return [shell(crepe), shell(behind(c1, [crepe], None)), shell(behind(c2, [crepe], None)),
            detail(wave_d(6.5, 17.5, 15.2, 1, 5.5)), dot(12, 18.6, 0.9)]


# =========================================================================== China, Korea, Japan and Southeast Asia


@icon("tangyuan", CAT, "A bowl of round glutinous rice balls, one with a dark filling showing",
      tags=["glutinous rice balls", "sweet soup", "dumpling soup", "lantern festival", "chinese dessert", "rice ball", "yuanxiao"])
def _(S):
    return [shell(bowl(S, 12.5)), shell(circle(8, 9, 2.6)), shell(circle(14, 9, 2.6)), shell(circle(11, 4.6, 2.6)),
            dot(14, 9, 0.9)]


@icon("century-egg", CAT, "A halved preserved egg with a dark yolk and a frost pattern in the white",
      tags=["preserved egg", "thousand year egg", "pidan", "black egg", "chinese", "congee topping", "egg half"])
def _(S):
    egg = "M12 2.8C16 2.8 19.5 8 19.5 13.2C19.5 18 16.2 21.2 12 21.2C7.8 21.2 4.5 18 4.5 13.2C4.5 8 8 2.8 12 2.8Z"
    if S.name == "line":
        egg = "M12 2.8C15.4 3.6 19.5 8.6 19.5 13.2C19.5 18 16.2 21.2 12 21.2C7.8 21.2 4.5 18 4.5 13.2C4.5 8.6 8.6 3.6 12 2.8Z"
    star = [seg(*pt_on(12, 8.6, 2.9, a), *pt_on(12, 8.6, 2.9, a + 180)) for a in (90, 30, 150)]
    return [shell(egg)] + [detail(d) for d in star] + [dot(12, 15.6, 3)]


@icon("chawanmushi", CAT, "A small lidded cup of steamed egg custard with a spoon beside it",
      tags=["steamed egg", "japanese custard", "savory custard", "egg custard", "cup", "spoon", "dashi"])
def _(S):
    lid = "M4 11.5C4 7.6 7 6 9.5 6C12 6 15 7.6 15 11.5Z"
    spoon_head = ellipse(19.3, 16.5, 1.9, 2.6)
    return [shell(bowl2(S, 12.5, 3, 16, 7.5)), shell(lid), line(seg(9.5, 3.3, 9.5, 6)), shell(spoon_head),
            line(poly([(19.3, 14), (19.3, 7.5)]))]


@icon("jajangmyeon", CAT, "A bowl of noodles topped with a glossy black bean sauce and cucumber matchsticks",
      tags=["black bean noodles", "korean chinese", "jjajangmyeon", "noodles", "sauce", "cucumber", "takeout"],
      aliases=["jjajangmyeon"])
def _(S):
    sauce = "M4.8 11.5C4.8 7.2 7.5 5.8 10 5.8C12.5 5.8 15 7.2 15 11.5Z"
    return [shell(bowl(S, 12)), solid(sauce), line(seg(16.6, 10.5, 19.4, 5.6)), line(seg(18.4, 10.5, 21, 7)),
            line(seg(15.4, 6.6, 17.2, 3.6))]


@icon("banh-xeo", CAT, "A crisp folded half-moon crepe with a ruffled lettuce leaf behind it",
      tags=["vietnamese pancake", "sizzling crepe", "bean sprouts", "turmeric crepe", "lettuce", "savory pancake", "vietnam"])
def _(S):
    crepe = "M2.8 19.5A9 9 0 0 1 20.8 19.5Z"
    lettuce = scallop_ring(16.6, 8.2, 5.2, 9, 1.1)
    return [shell(crepe), shell(behind(lettuce, [crepe], 1.2)), dot(8.5, 16.4, 1), dot(12.5, 14.8, 1), dot(15.6, 17.2, 1),
            dot(17, 7.6, 1)]


# =========================================================================== Central Asia, Middle East, Africa

@icon("plov", CAT, "A wide cauldron heaped with rice and carrot strips with a whole garlic bulb on top",
      tags=["pilaf", "pilau", "uzbek rice", "kazan", "carrot rice", "lamb rice", "central asian", "palov"],
      aliases=["pilaf"])
def _(S):
    heap = "M4.5 11.5C4.5 7.6 8.5 6.4 12 6.4C15.5 6.4 19.5 7.6 19.5 11.5Z"
    bulb = circle(12, 5.6, 2.6)
    return [shell(bowl2(S, 12, 3, 21, 8.5)), shell(behind(heap, [bulb], 1.0)), shell(bulb), line(seg(12, 3, 12, 1.4)),
            detail(seg(6.8, 10.4, 8.6, 8.4)), detail(seg(15.4, 10.4, 17.2, 8.4))]


@icon("manakish", CAT, "A round flatbread covered in herb speckles with a wavy drizzle of oil across it",
      tags=["manakeesh", "za'atar flatbread", "zaatar", "lebanese", "levantine", "herb bread", "breakfast flatbread"],
      aliases=["manakeesh"])
def _(S):
    disc = (poly(star_ring(12, 12, 9.4, 8.6, 18), closed=True) if S.name == "line" else circle(12, 12, 9))
    return [shell(disc), detail(wave_d(6.5, 17.5, 12, 1.2, 6)), dot(8.4, 7.8, 0.9), dot(13.6, 7.4, 0.9), dot(16.4, 8.6, 0.9),
            dot(7.6, 16.4, 0.9), dot(12.4, 16.6, 0.9), dot(16.6, 15.6, 0.9)]


@icon("tahdig", CAT, "A round golden crust of crispy rice with one wedge lifted out to show the fluffy rice under it",
      tags=["persian rice", "crispy rice", "rice crust", "iranian", "golden rice", "saffron rice", "crust"])
def _(S):
    cx, cy, r = 10.4, 13.6, 7.6
    a0, a1 = pt_on(cx, cy, r, -28), pt_on(cx, cy, r, -72)
    cake = f"M{fmt(cx)} {fmt(cy)}L{fmt(a0[0])} {fmt(a0[1])}A{r} {r} 0 1 1 {fmt(a1[0])} {fmt(a1[1])}Z"
    b0, b1 = pt_on(cx, cy, r, -72), pt_on(cx, cy, r, -28)
    wedge = f"M{fmt(cx)} {fmt(cy)}L{fmt(b0[0])} {fmt(b0[1])}A{r} {r} 0 0 1 {fmt(b1[0])} {fmt(b1[1])}Z"
    wedge = xf(wedge, 0, dx=3.8, dy=-3.8)
    return [shell(cake), shell(wedge), dot(7.4, 12, 1), dot(11, 16.4, 1), dot(13.6, 12.6, 1)]


@icon("koshari", CAT, "A bowl of layered rice, lentils and pasta crowned with a pile of crispy fried onion strands",
      tags=["kushari", "egyptian", "lentils", "macaroni", "chickpeas", "crispy onions", "street food", "vegan bowl"],
      aliases=["kushari"])
def _(S):
    return [shell(bowl(S, 12.5)), detail(seg(6, 16.5, 18, 16.5)), line("M6.5 11C7 7.6 9.6 5 12 4.4"),
            line("M17.5 11C17 7.6 14.4 5 12 4.4"), line("M10.2 11C10.6 9.2 12 7.8 14 7.6")]


@icon("bobotie", CAT, "A baking dish of spiced mince with a smooth custard top and bay leaves standing in it",
      tags=["south african", "baked mince", "custard", "bay leaf", "casserole", "cape malay", "baking dish"])
def _(S):
    return [shell(rect(2.5, 12.5, 19, 8, L(S, 1.5, 3))), detail(seg(6, 16.5, 18, 16.5)),
            shell(leaf(8.4, 11.6, 5.8, 3.4, 1.7)), shell(leaf(12.6, 11.4, 13.2, 2.8, 1.7)), shell(leaf(16.4, 11.6, 19, 4.2, 1.7))]


FISH = "M4.6 12C6.6 8.4 11.4 8.4 15 11L19.4 8V16L15 13C11.4 15.6 6.6 15.6 4.6 12Z"


@icon("thieboudienne", CAT, "A round platter of rice with a whole fish and vegetable chunks arranged on top",
      tags=["thieb", "ceebu jen", "senegalese", "fish and rice", "west african", "national dish", "platter"])
def _(S):
    plate_ring = circle(12, 12, 9.2)
    return [shell(plate_ring), shell(FISH if S.name == "line" else poly([(4.6, 12), (8, 9), (15, 11), (19.4, 8), (19.4, 16), (15, 13), (8, 15)], closed=True, r=1.2)),
            dot(8, 11.2, 0.9), dot(8.2, 5.8, 1.2), dot(15.8, 5.6, 1.2), dot(8.2, 18.2, 1.2), dot(15.8, 18.4, 1.2)]


@icon("porchetta", CAT, "A rolled pork roast cut open to show a spiral of herbs inside a ring of crackling skin",
      tags=["italian roast pork", "pork belly roll", "crackling", "roast", "rolled roast", "herbs", "sliced pork"])
def _(S):
    outer = (poly(star_ring(12, 12, 9.5, 8.4, 16), closed=True) if S.name == "line" else scallop_ring(12, 12, 8.6, 16, 1.15))
    return [shell(outer), detail(poly(spiral_pts(12, 12, 0.6, 4.8, 1.5, start=-90, n=30)))]


@icon("poffertjes", CAT, "A plate piled with tiny puffy pancakes topped with a pat of butter and powdered sugar",
      tags=["dutch pancakes", "mini pancakes", "netherlands", "powdered sugar", "butter", "fair food", "dessert"])
def _(S):
    balls = [circle(7.4, 15, 2.6), circle(12, 15, 2.6), circle(16.6, 15, 2.6), circle(9.7, 10.6, 2.6), circle(14.3, 10.6, 2.6)]
    return [shell(b) for b in balls] + [plate(S, y=18.8, h=2), shell(rect(9.6, 4.2, 4.8, 3.4, L(S, 0.3, 1))),
                                         dot(5, 10, 0.8), dot(19, 10, 0.8), dot(4.6, 6.4, 0.7), dot(19.4, 6.4, 0.7)]


@icon("seafood-boil", CAT, "A pile of shrimp, a corn cob piece and a small potato spread on a tray",
      tags=["crawfish boil", "shrimp boil", "low country boil", "cajun", "shellfish", "corn", "potato", "tray"])
def _(S):
    cx, cy, r = 12.4, 7, 3.8
    a0, a1 = pt_on(cx, cy, r, -15), pt_on(cx, cy, r, -80)
    claw = f"M{fmt(cx)} {fmt(cy)}L{fmt(a0[0])} {fmt(a0[1])}A{r} {r} 0 1 1 {fmt(a1[0])} {fmt(a1[1])}Z"
    return [plate(S, y=18.8, h=2), shell(capsule(5.8, 14.6, 9.6, 14.6, 5)), detail(seg(7.8, 13.1, 7.8, 16.1)),
            shell(circle(16.6, 14.8, 2.8)), shell(claw), line(seg(8.6, 7, 4.6, 5))]


# =========================================================================== sandwiches, Japanese and Korean plates


@icon("cheesesteak", CAT, "A long soft roll piled with chopped steak and melted cheese running down the side",
      tags=["philly cheesesteak", "philadelphia", "steak sandwich", "hoagie", "sub", "american", "melted cheese"])
def _(S):
    meat = bumps([(4.5, 12.5), (7.5, 8.6), (12, 7.4), (16.5, 8.6), (19.5, 12.5)], r=4.4) + "Z"
    return [shell(rect(2.5, 13.5, 19, 6, L(S, 2, 3))), shell(meat), detail(seg(15.6, 14.6, 15.6, 17.4)), detail(seg(11.2, 14.6, 11.2, 16.6))]


@icon("chia-pudding", CAT, "A lidded glass jar of chia pudding with a fruit layer on top and seeds dotted through it",
      tags=["chia seeds", "overnight pudding", "breakfast jar", "healthy dessert", "vegan", "fruit", "meal prep"])
def _(S):
    return [shell(rect(5, 8.5, 14, 12.5, L(S, 1.5, 3))), shell(rect(6.5, 3.2, 11, 3.6, L(S, 0.5, 1.5))),
            detail(seg(5.5, 12.5, 18.5, 12.5)), dot(8.8, 15.8, 0.85), dot(13, 15.4, 0.85), dot(15.6, 18, 0.85), dot(10.4, 18.6, 0.85)]


@icon("gimbap", CAT, "Three thick round slices of seaweed rice roll, each showing a colourful filling",
      tags=["kimbap", "korean rice roll", "seaweed roll", "picnic food", "sliced roll", "korean", "lunch box"],
      aliases=["kimbap"])
def _(S):
    parts = []
    for cx, cy in ((12, 6.8), (6.6, 16.6), (17.4, 16.6)):
        parts += [shell(circle(cx, cy, 4)), blob(cx - 1.3, cy - 1.3, 2.6, 2.6, 0) if S.name == "line" else dot(cx, cy, 1.5)]
    return parts


@icon("chirashi", CAT, "A square lacquer box of rice scattered with fish slices, egg strips and roe",
      tags=["chirashi sushi", "scattered sushi", "sashimi bowl", "bara sushi", "japanese", "rice box", "raw fish"],
      aliases=["chirashi-sushi"])
def _(S):
    a = rotd(ellipse(8.8, 8.6, 3.2, 1.8), -28, 8.8, 8.6)
    b = rotd(rect(12.6, 8.2, 5.6, 3.6, 1.2), 14, 15.4, 10)
    return [shell(rect(3, 3, 18, 18, L(S, 1.5, 4))), detail(a), detail(b), detail(seg(6.4, 15.8, 10.8, 15.8)),
            dot(14, 15.2, 0.9), dot(16.8, 16.4, 0.9), dot(14.6, 18, 0.9)]


@icon("yakisoba", CAT, "Stir-fried noodles on a flat griddle with two metal spatulas crossing over them",
      tags=["fried noodles", "teppanyaki", "japanese noodles", "griddle", "spatula", "stir fry", "festival food"])
def _(S):
    return [shell(rect(2.5, 16.5, 19, 4, L(S, 1.5, 2))), line(wave_d(4.5, 19.5, 13.2, 1.4, 5)),
            line(seg(6.4, 2.8, 13.4, 9.4)), line(seg(17.6, 2.8, 10.6, 9.4))]


@icon("karaage", CAT, "A paper cone of craggy fried chicken pieces with a lemon wedge on the side",
      tags=["japanese fried chicken", "fried chicken", "chicken bites", "izakaya", "lemon wedge", "snack cone", "nuggets"])
def _(S):
    cone = poly([(4.5, 11.5), (19.5, 11.5), (12, 21.5)], closed=True, r=L(S, 0, 1.2))
    lemon = "M14.6 10.6A3.1 3.1 0 0 1 20.8 10.6Z"
    return [shell(cone), shell(circle(7.6, 8.2, 2.5)), shell(circle(11.8, 6.2, 2.3)), shell(behind(lemon, [circle(11.8, 6.2, 2.3)], 1.0)),
            detail(seg(6.8, 11.5, 12, 19))]


@icon("sukiyaki", CAT, "A shallow iron pan of beef slices, tofu blocks and greens with a small bowl holding a raw egg",
      tags=["japanese hot pot", "beef hot pot", "nabe", "raw egg dip", "tofu", "iron pan", "winter dish"])
def _(S):
    return [shell(bowl2(S, 13, 2.5, 15.5, 6)), shell(cube(4.4, 7.6, 3.6, L(S, 0.3, 0.9))), shell(leaf(10, 11.6, 14.4, 6, 1.6)),
            shell(bowl2(S, 16.5, 16.5, 22, 4.5)), shell(ellipse(19.3, 13.2, 1.7, 2.1))]


@icon("shabu-shabu", CAT, "A pot of simmering broth with chopsticks swishing a thin wavy slice of meat through it",
      tags=["hot pot", "japanese hot pot", "thin sliced beef", "chopsticks", "simmering", "nabe", "swish"])
def _(S):
    return [shell(bowl2(S, 14, 3.5, 20.5, 7.5)), line(wave_d(5, 13, 10.2, 1.2, 4)), line(seg(21, 2.6, 13.6, 8.6)),
            line(seg(22, 5.2, 14.6, 10.8))]


@icon("japchae", CAT, "A heap of glossy glass noodles with thin vegetable strips and sesame seeds on a plate",
      tags=["korean glass noodles", "sweet potato noodles", "stir fried noodles", "dangmyeon", "korean side dish", "festival"])
def _(S):
    heap = "M4 17C4 9 8 5.5 12 5.5C16 5.5 20 9 20 17Z"
    return [shell(heap), detail(wave_d(7.5, 16.5, 10.6, 1.1, 4.5)), detail(wave_d(6.5, 17.5, 14, 1.1, 5.5)),
            plate(S, y=19, h=2), dot(12, 7.6, 0.8)]


# =========================================================================== stir fries, curries and snacks


@icon("kung-pao-chicken", CAT, "A bowl of diced chicken with whole peanuts and a dried chili on top",
      tags=["gong bao", "kung po", "sichuan", "peanuts", "dried chili", "stir fry", "chinese takeout"],
      aliases=["gong-bao-chicken"])
def _(S):
    return [shell(bowl(S, 12.5)), shell(cube(4.8, 6.4, 4.4, L(S, 0.3, 1), -8)), shell(rotd(ellipse(12.6, 8.6, 2.5, 1.7), -30, 12.6, 8.6)),
            shell(leaf(15.6, 10.6, 21, 4.6, 1.5)), dot(10.2, 5.2, 0.9)]


@icon("sweet-and-sour-pork", CAT, "A plate of battered pork balls, a pineapple wedge and a pepper square in glossy sauce",
      tags=["sweet and sour", "chinese takeout", "pineapple", "pork", "bell pepper", "cantonese", "sauce"])
def _(S):
    wedge = poly([(10.6, 11.6), (16.6, 11.6), (13.6, 5.4)], closed=True, r=L(S, 0, 1))
    return [plate(S, y=18.6, h=2.2), shell(circle(7, 14.4, 3)), shell(wedge), shell(cube(17.4, 11.6, 4, L(S, 0.3, 1), 10)),
            dot(12.2, 15.2, 0.9)]


@icon("turnip-cake", CAT, "A stack of three rectangular pan-fried slices of radish cake on a small plate",
      tags=["lo bak go", "radish cake", "daikon cake", "dim sum", "pan fried", "chinese new year", "cantonese"],
      aliases=["radish-cake"])
def _(S):
    return [shell(rect(4, 3.6, 15, 3.2, L(S, 0.5, 1.5))), shell(rect(6, 8.8, 15, 3.2, L(S, 0.5, 1.5))),
            shell(rect(4, 14, 15, 3.2, L(S, 0.5, 1.5))), plate(S, y=19.2, h=1.8)]


@icon("butter-chicken", CAT, "A round copper bowl of creamy orange curry with chicken pieces and a cream swirl on top",
      tags=["murgh makhani", "indian curry", "chicken curry", "creamy sauce", "tikka masala", "copper bowl", "north indian"])
def _(S):
    return [shell(bowl(S, 12)), shell(rotd(rect(5.4, 6.4, 5.6, 4, 1.4), -10, 8.2, 8.4)), shell(rotd(rect(12.4, 5.8, 5.6, 4.2, 1.4), 12, 15.2, 7.9)),
            detail(poly(spiral_pts(12, 16.2, 0.5, 3.4, 1.3, start=180, n=24)))]


# =========================================================================== breads, rolls and cold plates


@icon("kachori", CAT, "A round puffed pastry with a cracked top beside a small bowl of chutney",
      tags=["indian snack", "fried pastry", "lentil kachori", "chutney", "puffed pastry", "street food", "rajasthani"])
def _(S):
    crack = poly([(4.6, 9), (6.6, 6.6), (8.6, 9.4), (10.6, 6.8), (12.4, 9.2)], r=S.r * 0.6)
    return [shell(circle(8.6, 8.6, 6)), detail(crack), shell(bowl2(S, 15.5, 12, 21.5, 5)), dot(17, 18, 1)]


@icon("kathi-roll", CAT, "A flatbread roll open at the top with onion rings and a green chili poking out",
      tags=["kati roll", "frankie", "wrap", "indian street food", "kolkata", "paratha roll", "paper wrap"],
      aliases=["kati-roll"])
def _(S):
    body = ("M7 8.5A5 2.4 0 0 1 17 8.5V19.5C17 20.3 16.3 21 15.5 21H8.5C7.7 21 7 20.3 7 19.5Z" if S.name == "line" else
            "M7 8.5A5 2.4 0 0 1 17 8.5V18.5A2.5 2.5 0 0 1 14.5 21H9.5A2.5 2.5 0 0 1 7 18.5Z")
    return [shell(body), detail(seg(7.4, 15, 16.6, 13)), shell(circle(10, 5.4, 2.4)), line("M14.4 8C14.2 5.4 15.6 3.4 18.6 2.8")]


@icon("vada-pav", CAT, "A soft bun holding a round potato fritter with dots of chutney",
      tags=["mumbai burger", "bombay", "potato fritter", "indian street food", "bun", "chutney", "snack"],
      aliases=["wada-pav"])
def _(S):
    top = "M3.5 9C3.5 5 7.5 3.4 12 3.4C16.5 3.4 20.5 5 20.5 9Z"
    return [shell(top), shell(circle(12, 12.6, 3.3)), shell(rect(3.5, 17, 17, 4, L(S, 1, 1.8))), dot(12, 12.6, 0.9)]


@holey("simit", "A twisted ring of bread coated all over in sesame seeds",
       ["turkish bagel", "sesame ring", "sesame bread", "istanbul", "street bread", "gevrek", "bagel"],
       [circle(12, 12, 3.6)], aliases=["gevrek"])
def _(S):
    outer = poly(star_ring(12, 12, 9.4, 8.6, 22), closed=True) if S.name == "line" else scallop_ring(12, 12, 8.7, 22, 1.2)
    return [shell(outer), shell(circle(12, 12, 3.6)), dot(12, 5.8, 0.75), dot(17.2, 8.6, 0.75), dot(17.6, 15.4, 0.75),
            dot(12, 18.4, 0.75), dot(6.6, 15.6, 0.75), dot(6.4, 8.6, 0.75)]


@icon("blini", CAT, "A stack of thin pancakes topped with a dollop of sour cream and a few beads of roe",
      tags=["russian pancakes", "caviar", "sour cream", "smetana", "crepes", "appetizer", "festive", "maslenitsa"])
def _(S):
    dollop = "M8.6 11.2C8.6 6.4 15.4 6.4 15.4 11.2Z"
    return [shell(dollop), shell(rect(4, 12.4, 16, 3.2, L(S, 0.5, 1.5))), shell(rect(3, 17.6, 18, 3.2, L(S, 0.5, 1.5))),
            dot(10.8, 9, 0.7), dot(13.4, 9.4, 0.7)]


@icon("cabbage-rolls", CAT, "A cabbage leaf rolled into a parcel, its leaf veins showing, above a line of tomato sauce",
      tags=["stuffed cabbage", "golabki", "holubtsi", "sarma", "dolma", "eastern european", "tomato sauce"],
      aliases=["stuffed-cabbage"])
def _(S):
    ticks = []
    for x in (8.6, 11.8, 15):
        ticks += [detail(seg(x, 10.5, x + 2.2, 8.4)), detail(seg(x, 10.5, x + 2.2, 12.6))]
    return [shell(capsule(6.6, 10.5, 17.4, 10.5, 8.6)), detail(seg(7.6, 10.5, 16.4, 10.5))] + ticks + [line(wave_d(3.5, 20.5, 19.6, 0.9, 5))]


@icon("bratwurst", CAT, "A grilled sausage with diagonal grill marks on a plate beside a dollop of mustard",
      tags=["german sausage", "grilled sausage", "brat", "wurst", "mustard", "barbecue", "oktoberfest"])
def _(S):
    body = rotd(capsule(6, 11, 17.5, 11, 6.6), -8, 12, 11)
    marks = [detail(xf(seg(x, 8.4, x + 2, 13.6), -8, 12, 11)) for x in (7.6, 11, 14.4)]
    return [shell(body)] + marks + [plate(S, y=18.2, h=2.4), dot(19.4, 15.8, 1.1)]


@icon("spaetzle", CAT, "A bowl of short irregular egg noodles topped with crispy fried onion",
      tags=["spatzle", "german noodles", "egg noodles", "swabian", "cheese noodles", "kasespatzle", "side dish"],
      aliases=["spatzle"])
def _(S):
    return [shell(bowl(S, 12.5)), line(poly([(5.6, 10.6), (7.4, 8.4), (9.2, 10.6), (11, 8.4), (12.8, 10.6)], r=S.r * 0.6)),
            line(poly([(9, 6.2), (10.8, 4.2), (12.6, 6.2), (14.4, 4.2)], r=S.r * 0.6)),
            line(poly([(14.6, 10.6), (16.4, 8.4), (18.2, 10.6)], r=S.r * 0.6)), dot(17.4, 4.6, 0.9)]


@icon("ploughmans-lunch", CAT, "A board with a round crusty loaf and a cheese wedge",
      tags=["ploughman's lunch", "pub lunch", "british", "cheese and bread", "pickle", "cold plate", "lunch board"],
      aliases=["ploughmans"])
def _(S):
    loaf = "M3.2 16.4C3.2 11.4 6.6 8 8.4 8C10.2 8 13.6 11.4 13.6 16.4Z"
    cheese = poly([(15.4, 16.4), (21, 16.4), (21, 10.6)], closed=True, r=L(S, 0, 1))
    return [shell(loaf), detail(seg(6.4, 12.4, 7.8, 14.6)), shell(cheese), dot(18.8, 14.4, 0.8),
            shell(rect(2.5, 18.2, 19, 3, L(S, 1, 1.5)))]


# =========================================================================== Europe, the Americas and Africa


@icon("aligot", CAT, "A wooden spoon lifting a very long stretchy strand of cheesy mashed potato out of a pot",
      tags=["cheese potato", "stretchy cheese", "french", "aubrac", "mashed potato", "cheese pull", "wooden spoon"])
def _(S):
    head = rotd(ellipse(10.4, 4.6, 2.6, 2), -20, 10.4, 4.6)
    return [shell(bowl2(S, 14.5, 3.5, 20.5, 6.5)), shell(head), line(seg(13, 3.4, 20.6, 1.8)),
            line("M10.6 6.8C9.2 8.6 12.2 10.2 10.8 12.8"), dot(15.6, 17.2, 0.9)]


@icon("birria-tacos", CAT, "Two folded crisp tacos beside a small cup of broth for dipping",
      tags=["quesabirria", "mexican", "consome", "dipping broth", "stewed beef", "crispy taco", "jalisco"])
def _(S):
    ta = "M1.8 19.4A5 5 0 0 1 11.8 19.4Z"
    tb = "M6.2 15.4A5.2 5.2 0 0 1 16.6 15.4Z"
    cup = ("M17.6 12.6H22V17.4C22 18.6 21 19.6 19.8 19.6C18.6 19.6 17.6 18.6 17.6 17.4Z" if S.name == "line" else
           "M18.6 12.6H21A1 1 0 0 1 22 13.6V17.4C22 18.6 21 19.6 19.8 19.6C18.6 19.6 17.6 18.6 17.6 17.4V13.6A1 1 0 0 1 18.6 12.6Z")
    return [shell(ta), shell(behind(tb, [ta], 1.2)), shell(cup), dot(19.8, 15.4, 0.8)]


@icon("esquites", CAT, "A cup of loose corn kernels topped with a creamy drizzle and a spoon",
      tags=["elote in a cup", "mexican street corn", "corn cup", "mayo", "cotija", "street food", "corn kernels"])
def _(S):
    cup = poly([(5, 8.5), (17, 8.5), (15.4, 21), (6.6, 21)], closed=True, r=L(S, 0, 1.4))
    return [shell(cup), detail(wave_d(7, 15, 11.6, 0.9, 4)), dot(8.6, 15, 0.9), dot(11, 17.6, 0.9), dot(13.2, 14.6, 0.9),
            line(seg(14, 7, 21, 2.6))]


@icon("choripan", CAT, "A split crusty roll holding a flat grilled sausage with herb sauce spooned on top",
      tags=["argentine sausage", "chorizo sandwich", "chimichurri", "street food", "barbecue", "asado", "sausage roll"])
def _(S):
    return [shell(capsule(6, 16.6, 18, 16.6, 6)), shell(rect(3, 9.4, 18, 4.6, L(S, 1.5, 2.3))),
            detail(seg(7.4, 10.4, 9.2, 13)), detail(seg(11.4, 10.4, 13.2, 13)), detail(seg(15.4, 10.4, 17.2, 13)),
            dot(8, 5.6, 0.9), dot(12.2, 4.6, 0.9), dot(16.2, 5.8, 0.9)]


@icon("tequenos", CAT, "A stick of dough wrapped in a spiral around cheese with one end bitten and a cheese strand stretching out",
      tags=["venezuelan", "cheese sticks", "tequenos", "fried cheese", "dough wrapped", "party snack", "finger food"])
def _(S):
    cap = capsule(6.2, 12, 15.6, 12, 6.2)
    body = path_to_d(D(P(cap), P(circle(19.2, 12, 2.6))))
    f = lambda d: xf(d, -36, 12, 12)
    stripes = [detail(f(seg(x, 9.6, x + 1.8, 14.4))) for x in (7.6, 11.2)]
    return [shell(rotd(body, -36, 12, 12))] + stripes + [line(f("M17.2 12C19.6 12 19.6 14.6 21.6 15"))]


@icon("jerk-chicken", CAT, "A chicken leg with charred grill stripes beside a small lantern-shaped hot pepper",
      tags=["jamaican", "jerk", "caribbean", "scotch bonnet", "grilled chicken", "spicy chicken", "bbq"])
def _(S):
    meat, bone, kn, f = drum(-45, 0.5, 1.5)
    pepper = xf("M5.6 13.6C3.6 13.6 3.2 16.6 4.4 18.4C5.2 19.8 7 19.8 7.8 18.4C9 16.6 7.6 13.6 5.6 13.6Z", 0, dx=12.6, dy=-9.8)
    return [shell(meat), detail(f("M7.6 6.2H13.4")), detail(f("M6.8 9.8H14.2")), line(bone),
            dot(kn[0][0], kn[0][1], 1.6), dot(kn[1][0], kn[1][1], 1.6), shell(pepper), line(seg(18.2, 3.8, 18.2, 2.2))]


@icon("shrimp-and-grits", CAT, "A bowl of creamy grits topped with a curled shrimp and a sprinkle of scallion",
      tags=["southern", "low country", "charleston", "cornmeal", "shrimp", "breakfast bowl", "comfort food"])
def _(S):
    shrimp = path_to_d(ST(arc(11.4, 7.6, 3.5, 160, 400), 2.8, "round", "round"))
    return [shell(bowl(S, 12.5)), shell(shrimp), dot(18.2, 8.4, 0.9), dot(18.6, 5.2, 0.9), dot(5.4, 6, 0.9)]


@icon("jambalaya", CAT, "A cast iron pot with a bail handle, heaped with rice, sausage coins and pepper pieces",
      tags=["cajun", "creole", "louisiana", "rice dish", "sausage", "shrimp", "one pot", "new orleans"])
def _(S):
    heap = "M5.4 11.5C5.4 8.4 8.4 7.4 12 7.4C15.6 7.4 18.6 8.4 18.6 11.5Z"
    return [shell(bowl2(S, 12, 3, 21, 8.5)), line("M3.6 12C3.6 2.6 20.4 2.6 20.4 12"), shell(heap), dot(9.4, 9.7, 0.85),
            dot(12.8, 9.4, 0.85), dot(15.6, 9.8, 0.85)]


@icon("po-boy", CAT, "A long crusty roll overflowing with fried shrimp, shredded lettuce and tomato slices",
      tags=["poboy", "new orleans", "shrimp sandwich", "submarine", "louisiana", "fried seafood", "sandwich"],
      aliases=["poboy"])
def _(S):
    return [shell(capsule(6, 18, 18, 18, 5)), line(poly(zigzag(4.5, 19.5, 13.8, 1.4, 5), r=S.r * 0.6)),
            shell(circle(8.2, 8, 2.6)), line(curl(15, 8.4, 2.6, -40, 90))]


@icon("blt", CAT, "A toasted sandwich seen from the side with wavy bacon, lettuce and tomato between the slices",
      tags=["bacon lettuce tomato", "club sandwich", "bacon sandwich", "deli", "lunch", "toast", "diner"])
def _(S):
    top = "M3.5 7.6V6.4C3.5 4.4 6.6 3.4 12 3.4C17.4 3.4 20.5 4.4 20.5 6.4V7.6Z"
    return [shell(top), line(wave_d(3.6, 20.4, 10.8, 1.2, 4.8)), line(poly(zigzag(3.6, 20.4, 14.6, 1.2, 6), r=S.r * 0.5)),
            shell(rect(3.5, 18, 17, 3.2, L(S, 1, 1.6)))]


@icon("slider-burgers", CAT, "Two mini burgers side by side, each pinned with a flag toothpick",
      tags=["sliders", "mini burgers", "party food", "appetizer", "toothpick", "small burgers", "snack tray"],
      aliases=["sliders", "mini-burgers"])
def _(S):
    parts = []
    for cx in (6.2, 16.8):
        parts += [shell(f"M{fmt(cx - 4)} 12C{fmt(cx - 4)} 8.6 {fmt(cx - 2)} 7.8 {fmt(cx)} 7.8C{fmt(cx + 2)} 7.8 {fmt(cx + 4)} 8.6 {fmt(cx + 4)} 12Z"),
                  line(poly(zigzag(cx - 4, cx + 4, 14.8, 0.9, 2), r=S.r * 0.4)), shell(rect(cx - 4, 17.4, 8, 3.4, L(S, 0.8, 1.7))),
                  line(seg(cx - 0.4, 3.2, cx - 0.4, 7.8)), solid(poly([(cx - 0.4, 2.6), (cx + 2.8, 3.8), (cx - 0.4, 5)], closed=True))]
    return parts


@icon("stuffing", CAT, "A bowl of toasted bread cubes with herb specks and bits of celery",
      tags=["dressing", "thanksgiving", "bread stuffing", "holiday side", "sage", "roast dinner", "christmas dinner"])
def _(S):
    return [shell(bowl(S, 12.5)), shell(cube(5.8, 7.4, 3.8, L(S, 0.3, 0.9), -10)), shell(cube(11.6, 7, 3.8, L(S, 0.3, 0.9), 10)),
            shell(cube(8.6, 2.6, 3.4, L(S, 0.3, 0.9), 14)), dot(17.6, 8.6, 0.9), dot(16.8, 5.6, 0.8)]


@icon("mandazi", CAT, "Puffy triangular pieces of fried dough piled on a plate",
      tags=["mahamri", "east african doughnut", "fried dough", "swahili", "kenya", "tanzania", "coconut bread"])
def _(S):
    def tri(x0, y0, w, h, deg):
        a, b, c = (x0, y0), (x0 + w, y0), (x0 + w / 2, y0 - h)
        d = (f"M{fmt(a[0])} {fmt(a[1])}Q{fmt(x0 + w / 2)} {fmt(y0 + 1.4)} {fmt(b[0])} {fmt(b[1])}"
             f"Q{fmt(b[0] - 0.3)} {fmt(y0 - h / 2)} {fmt(c[0])} {fmt(c[1])}Q{fmt(x0 + 0.3)} {fmt(y0 - h / 2)} {fmt(a[0])} {fmt(a[1])}Z")
        return rotd(d, deg, x0 + w / 2, y0 - h / 3)
    return [shell(tri(2.6, 17.4, 8, 6.4, -12)), shell(tri(12.4, 17.4, 8, 6.4, 14)), shell(tri(8, 10.6, 8, 6.4, -4)), plate(S, y=19.4, h=2)]


@icon("katsudon", CAT, "A deep rice bowl topped with sliced breaded cutlet under a layer of soft egg",
      tags=["pork cutlet bowl", "tonkatsu", "donburi", "japanese rice bowl", "egg", "breaded pork", "comfort food"])
def _(S):
    return [shell(bowl(S, 12.5)), shell(rotd(rect(4.8, 5.2, 3.8, 6, L(S, 0.3, 1)), -8, 6.7, 8.2)), shell(rect(10.2, 4.6, 3.8, 6.6, L(S, 0.3, 1))),
            shell(rotd(rect(15.6, 5.2, 3.8, 6, L(S, 0.3, 1)), 8, 17.5, 8.2)), detail(wave_d(6.5, 17.5, 15.6, 1, 5))]


@icon("gyudon", CAT, "A bowl of rice topped with thin simmered beef slices and onion with a small heap of pickled ginger",
      tags=["beef bowl", "donburi", "japanese fast food", "sliced beef", "onion", "red ginger", "rice bowl"])
def _(S):
    beef = "M4.4 11.5C4.4 7.2 7.8 5.8 12 5.8C16.2 5.8 19.6 7.2 19.6 11.5Z"
    return [shell(bowl(S, 12.5)), shell(beef), detail(wave_d(6.6, 12.6, 9.4, 0.8, 4)), dot(15.6, 9.6, 0.9), dot(17.2, 8.2, 0.9)]


@icon("kushikatsu", CAT, "Three breaded skewers standing in a shared tray of dipping sauce",
      tags=["kushiage", "fried skewers", "osaka", "japanese", "deep fried", "dipping sauce", "izakaya"])
def _(S):
    parts = [shell(rect(2.5, 14.4, 19, 6.4, L(S, 1.5, 2.6))), detail(wave_d(5.5, 18.5, 17.6, 0.8, 6.5))]
    for cx in (6.6, 12, 17.4):
        parts += [shell(rect(cx - 2.2, 2.8, 4.4, 7, L(S, 0.6, 1.6))), line(seg(cx, 9.8, cx, 15.4))]
    return parts


@icon("sisig", CAT, "A round sizzling iron plate of chopped meat with a raw egg in the centre and a halved chili",
      tags=["filipino", "philippines", "sizzling plate", "pork sisig", "chopped meat", "egg", "calamansi", "pulutan"])
def _(S):
    plate_d = circle(10, 12, 8.2)
    handle = bar(17.6, 12, 22, 12, 3.4, L(S, 0, 1))
    return [shell(plate_d), shell(behind(handle, [plate_d], None)), detail(circle(10, 12, 3.4)), dot(10, 12, 1.3),
            dot(5.6, 7.8, 0.8), dot(8.6, 5.6, 0.8), dot(14.2, 7, 0.8), dot(15, 12.4, 0.8), dot(13.4, 16.6, 0.8),
            dot(6.4, 15.6, 0.8)]


@icon("chili-crab", CAT, "A shallow bowl of crab in thick red sauce with two raised claws above the rim",
      tags=["singapore", "seafood", "crab in sauce", "spicy crab", "mantou", "fried bun", "shellfish dish"])
def _(S):
    return [shell(bowl(S, 12.5)), shell(claw(6.2, 7.6, 3.6, -80, 34)), shell(claw(17.8, 7.6, 3.6, -100, 34)),
            shell("M8.4 11.4A3.6 3.2 0 0 1 15.6 11.4Z"), detail(wave_d(7, 17, 16.6, 1, 5))]
