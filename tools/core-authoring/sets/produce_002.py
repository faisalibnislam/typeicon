"""TypeIcon Core: produce (batch produce_002): seeds, pods, vegetables, roots and grains.

Drawn from the plant part itself: upright side views, cut faces shown front on.
Stalks are open strokes; seeds are small solid dots that the Filled style knocks out.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, rotation, transform_path  # noqa: F401

CAT = "produce"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def grow(d, g):
    """Region d expanded by g px (cuts clean gaps between overlapping parts)."""
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def cut(d, *fronts, g=2.4):
    """d with every front shape (grown by g) removed: d seen behind the fronts."""
    return minus(d, *[grow(f, g) for f in fronts])


def thick(d, w, cap="round"):
    """Closed outline of a stroke of width w along d."""
    return path_to_d(ST(d, w, cap, "round"))


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled body."""
    return Part("dot", d)


def _p(p):
    return f"{fmt(p[0])} {fmt(p[1])}"


def tip(a, p, b, r):
    """Corner at p (from a, towards b): sharp when r == 0, softened with a quadratic when r > 0."""
    if r <= 0:
        return "L" + _p(p)
    la = math.hypot(a[0] - p[0], a[1] - p[1])
    lb = math.hypot(b[0] - p[0], b[1] - p[1])
    t = min(r, la / 2, lb / 2)
    s = (p[0] + (a[0] - p[0]) * t / la, p[1] + (a[1] - p[1]) * t / la)
    e = (p[0] + (b[0] - p[0]) * t / lb, p[1] + (b[1] - p[1]) * t / lb)
    return "L" + _p(s) + "Q" + _p(p) + " " + _p(e)


def leaf(x1, y1, x2, y2, bulge):
    """Closed pointed leaf from (x1, y1) to (x2, y2); bulge = half width."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    b = bulge * 2
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx * b)} {fmt(my + ny * b)} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(mx - nx * b)} {fmt(my - ny * b)} {fmt(x1)} {fmt(y1)}Z")


def smooth(pts, closed=True, k=1 / 6):
    """Smooth curve through pts (Catmull-Rom as cubics)."""
    n = len(pts)
    d = "M" + _p(pts[0])
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if closed or i > 0 else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if closed or i + 2 < n else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) * k, p1[1] + (p2[1] - p0[1]) * k)
        c2 = (p2[0] - (p3[0] - p1[0]) * k, p2[1] - (p3[1] - p1[1]) * k)
        d += "C" + _p(c1) + " " + _p(c2) + " " + _p(p2)
    return d + ("Z" if closed else "")


def blob(cx, cy, rx, ry, radii, start=-90.0):
    """Smooth irregular oval: one radius factor per evenly spaced direction."""
    n = len(radii)
    pts = []
    for i, f in enumerate(radii):
        a = math.radians(start + i * 360 / n)
        pts.append((cx + rx * f * math.cos(a), cy + ry * f * math.sin(a)))
    return smooth(pts)


def spiky(cx, cy, rx, ry, n, h, S, skip=(), start=-90.0):
    """Oval outline with n triangular spikes of height h (sharp in Line, softened in Rounded)."""
    pts = []
    for i in range(2 * n):
        a = math.radians(start + i * 180 / n)
        if i % 2 == 1 and (i // 2) not in skip:
            k = 1 + h / ((rx + ry) / 2)
        else:
            k = 1
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    return poly(pts, closed=True, r=L(S, 0, 0.45))


def region(d):
    """Area covered by a closed outline filled to its outer stroke edge."""
    return U(P(d), ST(d, 2))


def layered(ds, gap=1.4):
    """Filled design for overlapping shapes listed back to front: each front shape is separated from those
    behind it by a knocked-out gap."""
    body = None
    for d in ds:
        r = region(d)
        body = r if body is None else U(D(body, U(r, ST(path_to_d(r), 2 * gap, "round", "round"))), r)
    return body


def beads(pts, r):
    """Silhouette of a cluster of touching beads (drupelets)."""
    return union(*[circle(x, y, r) for x, y in pts])


def stem(x1, y1, x2, y2, bend=0.0):
    """Short curved stalk from (x1, y1) to (x2, y2)."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    return line(f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx * bend)} {fmt(my + ny * bend)} {fmt(x2)} {fmt(y2)}")



def pt_(cx, cy, r, deg):
    return (cx + r * math.cos(math.radians(deg)), cy + r * math.sin(math.radians(deg)))


def drop(S, b, t, hw, k=0.7):
    """Teardrop from round base b to pointed tip t; hw is about the half width. Rounded softens the tip."""
    bx, by = b
    tx, ty = t
    ln = math.hypot(tx - bx, ty - by)
    ux, uy = (tx - bx) / ln, (ty - by) / ln
    nx, ny = -uy, ux
    k = 0 if S.name == "line" else k
    a = (tx - ux * k + nx * k * 0.55, ty - uy * k + ny * k * 0.55)
    c = (tx - ux * k - nx * k * 0.55, ty - uy * k - ny * k * 0.55)

    def P2(x, y, s):
        return (x + nx * s, y + ny * s)
    c1 = P2(tx - ux * ln * 0.35, ty - uy * ln * 0.35, hw * 1.0)
    c2 = P2(bx + ux * ln * 0.05, by + uy * ln * 0.05, hw * 1.35)
    d1 = P2(tx - ux * ln * 0.35, ty - uy * ln * 0.35, -hw * 1.0)
    d2 = P2(bx + ux * ln * 0.05, by + uy * ln * 0.05, -hw * 1.35)
    s = "M" + _p(a)
    s += ("Q" + _p(t) + " " + _p(c)) if k else ("L" + _p(t) + "L" + _p(c))
    s += "C" + _p(d1) + " " + _p(d2) + " " + _p(b) + "C" + _p(c2) + " " + _p(c1) + " " + _p(a) + "Z"
    return s


def ell(cx, cy, rx, ry, deg=0):
    return rot(ellipse(cx, cy, rx, ry), deg, cx, cy) if deg else ellipse(cx, cy, rx, ry)


def rotd(d, deg, cx=12.0, cy=12.0):
    """Rotate an open or closed path written with absolute M L Q C Z commands only."""
    import re
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    toks = re.findall(r"[MLQCZ]|-?\d*\.?\d+", d)
    out, i = [], 0
    while i < len(toks):
        t = toks[i]
        if t == "Z":
            out.append("Z")
            i += 1
            continue
        pairs = []
        i += 1
        while i < len(toks) and toks[i] not in "MLQCZ":
            x, y = float(toks[i]), float(toks[i + 1])
            pairs.append(_p((cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c)))
            i += 2
        out.append(t + " ".join(pairs))
    return "".join(out)


def pod(S, p1, p2, hw, bend=0.0):
    """Slender pod from p1 to p2, half width hw, bowed sideways by bend. Line ends pointed, Rounded ends blunt."""
    (x1, y1), (x2, y2) = p1, p2
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    cu = (mx + nx * (2 * hw + bend), my + ny * (2 * hw + bend))
    cl = (mx - nx * (2 * hw - bend), my - ny * (2 * hw - bend))
    if S.name == "line":
        return f"M{_p(p1)}Q{_p(cu)} {_p(p2)}Q{_p(cl)} {_p(p1)}Z"
    e = 0.5
    a1 = (x1 + nx * e, y1 + ny * e)
    a2 = (x1 - nx * e, y1 - ny * e)
    b1 = (x2 + nx * e, y2 + ny * e)
    b2 = (x2 - nx * e, y2 - ny * e)
    return f"M{_p(a1)}Q{_p(cu)} {_p(b1)}L{_p(b2)}Q{_p(cl)} {_p(a2)}Z"


def sp(x, y, r=0.9):
    return dot(x, y, r)



# =========================================================================== seeds and nuts

@icon("pine-nut", CAT, "Three slender pointed pine nut kernels standing together",
      tags=["pine kernel", "pignoli", "pesto", "nut", "seed", "produce"])
def _(S):
    k1 = drop(S, (7.6, 19.6), (5.4, 6.4), 2.4)
    k2 = drop(S, (16.4, 19.6), (18.6, 6.4), 2.4)
    k3 = drop(S, (12, 20.8), (12, 3.2), 2.4)
    return [shell(cut(k1, k3, g=2.3)), shell(cut(k2, k3, g=2.3)), shell(k3)]


@icon("mixed-nuts", CAT, "Bowl heaped with a walnut, an almond and a hazelnut",
      tags=["nuts", "trail mix", "snack", "assorted nuts", "bowl", "produce"])
def _(S):
    bowl = poly([(3, 14.6), (21, 14.6), (20, 18), (16.6, 21), (7.4, 21), (4, 18)], closed=True, r=L(S, 0, 2))
    walnut = circle(7.6, 9.4, 3.6)
    almond = drop(S, (16.6, 12.4), (17.2, 3.4), 2.5)
    hazel = circle(12.2, 5.4, 2.6)
    return [shell(cut(hazel, walnut, almond, g=2.0)), shell(walnut), detail("M7.6 6.6V12.4"), shell(almond), shell(bowl)]


@icon("sunflower-seed", CAT, "Teardrop shaped sunflower seed with bold lengthwise stripes",
      tags=["seed", "snack", "sunflower", "kernel", "bird seed", "produce"])
def _(S):
    body = drop(S, (12, 18.6), (12, 3.4), 4.6)
    return [shell(rot(body, 18)), detail(rotd("M9.8 8Q8.8 13.6 10.4 17", 18)),
            detail(rotd("M14.2 8Q15.2 13.6 13.6 17", 18)), detail(rotd("M12 9L12 17", 18))]


@icon("pumpkin-seeds", CAT, "Two flat oval pumpkin seeds with pointed tips",
      tags=["pepitas", "seed", "snack", "halloween", "roasted seeds", "produce"])
def _(S):
    a = drop(S, (7.8, 19.4), (10.2, 4.8), 3.6)
    b = drop(S, (16.6, 20), (15.6, 7), 3.4)
    return [shell(a), shell(b), detail("M8.4 16Q8.8 13 9.6 10"), detail("M16.4 17Q16.2 14.6 15.8 11.4")]


@icon("sesame-seeds", CAT, "Four small flat sesame seeds scattered apart",
      tags=["seed", "benne", "tahini", "bagel topping", "spice", "produce"])
def _(S):
    s1 = drop(S, (5.4, 10.2), (9, 3.6), 2.2)
    s2 = drop(S, (20, 8.4), (15, 4), 2.2)
    s3 = drop(S, (7.6, 21), (5.6, 14.4), 2.2)
    s4 = drop(S, (13.4, 12.6), (18.6, 20.4), 2.2)
    return [shell(s1), shell(s2), shell(s3), shell(s4)]


@icon("poppy-seed-pod", CAT, "Round poppy seed capsule with a flat ridged crown on a short stem",
      tags=["poppy", "capsule", "seed head", "opium poppy", "baking", "produce"])
def _(S):
    body = ellipse(12, 13.6, 7, 6.4)
    crown = poly([(7.2, 8), (8.8, 4.2), (15.2, 4.2), (16.8, 8)], closed=True, r=L(S, 0, 1.2))
    return [shell(union(body, crown)), line("M12 20V22.4"), detail("M9 11.4Q8.2 13.8 9 16.4M15 11.4Q15.8 13.8 15 16.4")]


@icon("lotus-seed-pod", CAT, "Flat topped lotus pod with seed holes across its face, on a stem",
      tags=["lotus", "seed head", "water lily", "dried flower", "asian", "produce"])
def _(S):
    top = ellipse(12, 8, 8.4, 3.6)
    cone = poly([(4, 8.4), (20, 8.4), (14, 18.2), (10, 18.2)], closed=True, r=L(S, 0, 1.2))
    return [shell(union(top, cone)), sp(8.6, 8, 0.85), sp(12, 9.4, 0.85), sp(15.4, 8, 0.85), sp(12, 6.6, 0.85),
            line("M12 18.4V22")]


@icon("grain-kernel", CAT, "Single cereal grain with a crease down its middle",
      tags=["wheat", "kernel", "cereal", "whole grain", "seed", "produce"])
def _(S):
    body = leaf(12, 3, 12, 21, 5.4) if S.name == "line" else ellipse(12, 12, 5.4, 9)
    return [shell(rot(body, 28)), detail(rotd("M12 6.4Q15.2 12 12 17.6", 28))]


@icon("nutcracker", CAT, "Hinged hand nutcracker with two handles gripping a round nut",
      tags=["nut", "walnut", "cracker", "kitchen", "holiday", "tool", "produce"])
def _(S):
    return [line(poly([(3.5, 18), (8, 10), (21, 6.6)], r=S.r)), line(poly([(3.5, 18), (8.4, 19), (21, 20.8)], r=S.r)),
            shell(circle(11.2, 14.8, 3))]


@icon("tomato-slice", CAT, "Round tomato slice cut by a cross of inner walls with a seed in each part",
      tags=["tomato", "slice", "sandwich", "burger", "salad", "vegetable", "produce"])
def _(S):
    seeds = [sp(x, y, 0.9) for x, y in ((8.7, 8.7), (15.3, 8.7), (8.7, 15.3), (15.3, 15.3))]
    return [shell(circle(12, 12, 9)), detail("M12 5.8V18.2M5.8 12H18.2"), *seeds]


@icon("cherry-tomatoes", CAT, "Truss of three small round tomatoes hanging from a vine",
      tags=["tomato", "vine tomatoes", "grape tomatoes", "truss", "vegetable", "produce"])
def _(S):
    return [line("M3 4.8Q12 2.4 21 6"), line("M7 4.3V10.4"), line("M12 4V14.8"), line("M17 5.4V9.6"),
            shell(circle(7, 13.4, 3)), shell(circle(17, 12.6, 3)), shell(circle(12, 18.6, 3))]


@icon("tomato-plant", CAT, "Staked tomato plant with leaves and two tomatoes hanging from the stem",
      tags=["tomato", "garden", "growing", "vine", "vegetable plant", "produce"])
def _(S):
    return [line("M3 3V22"), line("M10 22C10 17 11.4 13 10 6.4"), shell(leaf(10, 15.6, 6, 11.4, 1.2)),
            shell(leaf(10.2, 6.4, 14.6, 2.6, 1.2)), line("M10.6 9.4Q13 8.2 16.6 8.6"), shell(circle(17, 10.6, 3)),
            line("M10.4 17Q13.4 15.6 16.4 16.8"), shell(circle(16.8, 19, 3))]


@icon("cucumber-slice", CAT, "Round cucumber slice with a thin skin ring and three seed marks",
      tags=["cucumber", "slice", "salad", "spa", "eye mask", "vegetable", "produce"])
def _(S):
    seeds = [mark(drop(S, pt_(12, 12, 1.2, a), pt_(12, 12, 4.4, a), 0.9)) for a in (-90, 30, 150)]
    return [shell(circle(12, 12, 9)), detail(circle(12, 12, 5.8)), *seeds]


@icon("butternut-squash", CAT, "Bell shaped butternut squash with a long narrow neck, round bulb and short stem",
      tags=["squash", "winter squash", "gourd", "autumn", "vegetable", "produce"])
def _(S):
    body = smooth([(10.5, 5.6), (13.5, 5.6), (13.6, 10.6), (14.6, 12.4), (17.8, 14.2), (18.8, 17.4), (16.6, 20.8), (12, 21.8),
                   (7.4, 20.8), (5.2, 17.4), (6.2, 14.2), (9.4, 12.4), (10.4, 10.6)])
    return [shell(body), line("M12 5.6V2.6"), detail("M8.6 16.4Q8.8 18.6 10.4 20"), detail("M12 8.6V12.6")]


@icon("acorn-squash", CAT, "Round ribbed acorn squash with a pointed base and a thick stem",
      tags=["squash", "winter squash", "ribbed", "autumn", "vegetable", "produce"])
def _(S):
    body = smooth([(12, 6.8), (16.4, 7.6), (19.6, 11.4), (19.2, 16), (15.8, 19.8), (12, 21.8), (8.2, 19.8), (4.8, 16),
                   (4.4, 11.4), (7.6, 7.6)])
    stem = rect(10.4, 2.6, 3.2, 4.8, L(S, 0.3, 1.2))
    return [shell(union(body, stem)), detail("M8.6 9.6Q6.6 14.4 10 19.4"), detail("M15.4 9.6Q17.4 14.4 14 19.4"),
            detail("M12 10.6V18")]



# =========================================================================== squash, gourds and peppers

@icon("pattypan-squash", CAT, "Flying saucer shaped pattypan squash with a scalloped rim and a short stem",
      tags=["squash", "summer squash", "scallop squash", "saucer", "vegetable", "produce"])
def _(S):
    body = blob(12, 14, 9.2, 6.6, [1, 0.9, 1, 0.9, 1, 0.9, 1, 0.9, 1, 0.9, 1, 0.9, 1, 0.9, 1, 0.9])
    stem = rect(10.4, 3.2, 3.2, 5, L(S, 0.3, 1.2))
    return [shell(union(body, stem)), detail("M7.2 14Q12 17.4 16.8 14")]


@icon("bottle-gourd", CAT, "Bottle shaped gourd with a small round top, a narrow waist and a large round bottom",
      tags=["gourd", "calabash", "lauki", "dudhi", "vegetable", "produce"])
def _(S):
    body = union(circle(12, 5.6, 3.2), rect(10.6, 6, 2.8, 6, 0), circle(12, 15.8, 6.2))
    return [shell(body), detail("M8.6 15Q8.6 18 10.4 19.6")]


@icon("bitter-melon", CAT, "Long tapered bitter melon covered in rows of warty ridges",
      tags=["bitter gourd", "karela", "bitter squash", "vegetable", "asian", "produce"])
def _(S):
    b, t = (7.6, 7.4), (19.6, 20.6)
    ticks = []
    for f in (0.3, 0.5, 0.7):
        cx, cy = b[0] + (t[0] - b[0]) * f, b[1] + (t[1] - b[1]) * f
        ticks.append(detail(seg(cx - 1.0, cy + 1.0, cx + 1.0, cy - 1.0)))
    return [shell(drop(S, b, t, 3.8)), line("M7 6.8L4.4 3.6"), *ticks]


@icon("chayote", CAT, "Pear shaped chayote squash with puckered creases gathered at the wide bottom end",
      tags=["squash", "mirliton", "choko", "vegetable pear", "vegetable", "produce"])
def _(S):
    body = smooth([(12, 4.6), (15, 6.6), (17.2, 10.4), (19.2, 14.6), (17.8, 18.8), (14, 21.2), (10, 21.2), (6.2, 18.8),
                   (4.8, 14.6), (6.8, 10.4), (9, 6.6)])
    return [shell(body), line("M12 4.8L12.8 2.4"), detail("M10.4 21Q10.8 18.2 9.2 15.4"), detail("M13.6 21Q13.2 18.2 14.8 15.4")]


@icon("bell-pepper", CAT, "Blocky bell pepper with three rounded lobes at the bottom and a curved stem",
      tags=["pepper", "capsicum", "sweet pepper", "paprika", "vegetable", "produce"])
def _(S):
    body = smooth([(12, 7.6), (16.2, 6.4), (19.4, 8), (19.8, 12.6), (18.8, 17.6), (17.2, 20.8), (14.8, 19.4), (12, 21.2),
                   (9.2, 19.4), (6.8, 20.8), (5.2, 17.6), (4.2, 12.6), (4.6, 8), (7.8, 6.4)])
    return [shell(body), line("M12 7.6Q12 4.4 14.6 2.6"), detail("M9 10.6Q9.6 14.6 9.2 17.4"), detail("M15 10.6Q14.4 14.6 14.8 17.4")]


@icon("bell-pepper-half", CAT, "Bell pepper cut across showing three lobes, inner walls and seeds",
      tags=["pepper", "capsicum", "cut pepper", "cross section", "seeds", "vegetable", "produce"])
def _(S):
    d = L(S, 5.3, 5.0)
    r = L(S, 5, 5.3)
    cx, cy = 12, 13.2
    lobes = [pt_(cx, cy, d, a) for a in (-90, 30, 150)]
    body = union(*[circle(x, y, r) for x, y in lobes])
    walls = [detail(seg(*pt_(cx, cy, 1.4, a), *pt_(cx, cy, 6, a))) for a in (90, 210, 330)]
    seeds = [sp(*pt_(cx, cy, 3.2, a), 0.85) for a in (-90, 30, 150)]
    return [shell(body), *walls, *seeds]


@icon("chili-string", CAT, "Three dried chili peppers tied together at the stem and hanging from a loop",
      tags=["ristra", "dried chili", "chilli", "peppers", "hanging", "spice", "produce"])
def _(S):
    return [shell(circle(12, 3.6, 1.7)), line("M12 5.4V8.2"), line("M5.6 8.2H18.4"),
            shell(drop(S, (6, 10), (5.4, 21.4), 2.2)), shell(drop(S, (12, 9.6), (12.4, 22), 2.2)),
            shell(drop(S, (18, 10), (18.6, 21.4), 2.2))]


@icon("okra", CAT, "Tapered okra pod with a pointed tip and a cap stem, beside a small star shaped slice",
      tags=["lady finger", "bhindi", "gumbo", "pod", "vegetable", "produce"])
def _(S):
    star = poly(regular(18, 17.6, 3.7, 5, 90), closed=True, r=L(S, 0, 1.2))
    return [shell(drop(S, (14.8, 5.6), (4.8, 20.2), 3.6)), line("M15.6 4.8L17.6 2.6"), detail("M13 8.6L8.6 15.4"),
            shell(star), sp(18, 17.6, 0.9)]


@icon("green-bean", CAT, "Three long slender green bean pods with gentle curves and small stem ends",
      tags=["string bean", "snap bean", "french bean", "haricot", "vegetable", "produce"])
def _(S):
    return [shell(pod(S, (6, 6), (5.6, 20.6), 1.6, -1.4)), shell(pod(S, (12, 5), (12.6, 20.8), 1.6, 1.6)),
            shell(pod(S, (18, 6), (18.2, 20.6), 1.6, -1.2)),
            line("M6 6L6.6 3.6"), line("M12 5L11.6 2.8"), line("M18 6L18.8 3.8")]


@icon("pea-pod", CAT, "Open pea pod split along its seam showing a row of round peas inside",
      tags=["peas", "garden pea", "pod", "legume", "vegetable", "produce"])
def _(S):
    p1, p2 = (2.6, 16.6), (21.4, 7.4)
    dots = []
    for f in (0.28, 0.5, 0.72):
        x, y = p1[0] + (p2[0] - p1[0]) * f, p1[1] + (p2[1] - p1[1]) * f
        dots.append(sp(x + 0.4, y - 0.3, 2.0))
    return [shell(pod(S, p1, p2, 4.6, 2.2)), *dots]


@icon("edamame", CAT, "Closed edamame pod with bean bumps and one bean popping out of the top end",
      tags=["soybean", "soy pod", "green soybean", "japanese", "bean", "vegetable", "produce"])
def _(S):
    p1, p2 = (3.6, 20.4), (15.4, 9)
    seams = []
    for f in (0.36, 0.64):
        x, y = p1[0] + (p2[0] - p1[0]) * f, p1[1] + (p2[1] - p1[1]) * f
        seams.append(detail(seg(x - 1.8, y - 1.8, x + 1.8, y + 1.8)))
    return [shell(pod(S, p1, p2, 4.2, 1.8)), *seams, shell(circle(19, 5.4, 2.4))]


@icon("cauliflower", CAT, "Rounded bumpy cauliflower head wrapped at the base by curling leaves",
      tags=["cauliflower", "brassica", "florets", "white vegetable", "keto", "produce"])
def _(S):
    cloud = union(circle(7.4, 11, 3.6), circle(12, 7.4, 4), circle(16.6, 11, 3.6), circle(12, 12, 4.4))
    cup = "M3.8 12.4Q4.4 19.6 12 21.6Q19.6 19.6 20.2 12.4Z"
    return [shell(union(cloud, cup)), detail("M12 14.6V19.4"), detail("M7.6 14.6Q8 17.4 10 19"), detail("M16.4 14.6Q16 17.4 14 19")]


@icon("romanesco", CAT, "Cone shaped romanesco head covered in tiers of small pointed cones",
      tags=["roman cauliflower", "fractal", "broccoflower", "spiral", "vegetable", "produce"])
def _(S):
    body = "M12 2.8C14 8 19 12 20.2 19.6Q12 22.6 3.8 19.6C5 12 10 8 12 2.8Z"
    tris = []
    for x, y in ((12, 9.6), (9.4, 14.4), (14.6, 14.4), (7, 19), (12, 19), (17, 19)):
        tris.append(mark(poly([(x - 1.5, y), (x, y - 3), (x + 1.5, y)], closed=True, r=L(S, 0, 0.4))))
    return [shell(body), *tris]


@icon("cabbage", CAT, "Round cabbage head wrapped in broad leaves with curved veins",
      tags=["cabbage", "brassica", "coleslaw", "leafy vegetable", "green cabbage", "produce"])
def _(S):
    head = circle(12, 12.6, 9) if S.name == "line" else blob(12, 12.6, 9, 9, [1, 0.95] * 6)
    return [shell(head), detail("M5.8 6.2C11 7.2 14.6 11.4 14.4 20.6"), detail("M3.6 13C6.4 13.4 8.6 15.6 9.2 20")]


@icon("cabbage-half", CAT, "Cabbage cut in half showing its core and tightly layered curved leaves",
      tags=["cabbage", "cross section", "cut cabbage", "core", "layers", "vegetable", "produce"])
def _(S):
    return [shell(circle(12, 12.6, 9)), detail("M12 21C7.4 18.6 6 12.6 10.6 6.8"), detail("M12 21C16.6 18.6 18 12.6 13.4 6.8"),
            detail("M12 21V13")]


# =========================================================================== leafy greens, stalks and alliums

@icon("napa-cabbage", CAT, "Tall oblong napa cabbage with ribbed stalks and a crinkled frilly top",
      tags=["chinese cabbage", "wombok", "kimchi", "leafy vegetable", "cabbage", "produce"])
def _(S):
    body = union(ellipse(12, 14.4, 6.4, 7.2), circle(8.2, 7.6, 2.8), circle(12, 6, 3), circle(15.8, 7.6, 2.8))
    return [shell(body), detail("M12 10.4V20"), detail("M8.6 11.4Q8 15 9 19"), detail("M15.4 11.4Q16 15 15 19")]


@icon("bok-choy", CAT, "Bundle of thick white bok choy stalks flaring into large rounded leaves",
      tags=["pak choi", "chinese cabbage", "asian greens", "stir fry", "leafy vegetable", "produce"])
def _(S):
    top = ellipse(12, 8.2, 8.4, 5.6)
    stalks = poly([(7.6, 11), (16.4, 11), (14.6, 21.6), (9.4, 21.6)], closed=True, r=L(S, 0, 1))
    return [shell(union(top, stalks)), detail("M12 4.6V10"), detail("M10.6 13V21M13.4 13V21")]


@icon("brussels-sprout", CAT, "Tall stalk studded with small round sprouts along its length",
      tags=["brussels sprouts", "sprouts", "brassica", "christmas dinner", "cabbage", "vegetable", "produce"])
def _(S):
    sprouts = [circle(7.4, 6.6, 3.4), circle(16.6, 11.2, 3.4), circle(7.4, 15.8, 3.4), circle(16.6, 20, 2.4)]
    return [line("M12 2.4V22"), *[shell(c) for c in sprouts]]


@icon("kale", CAT, "Long kale leaf with a thick center rib and a tightly curled frilly edge",
      tags=["leafy green", "superfood", "curly kale", "salad", "vegetable", "produce"])
def _(S):
    pts = []
    n = 7
    for i in range(n + 1):
        y = 3 + i * 17 / n
        w = 7.4 * math.sin(math.pi * (0.06 + 0.88 * i / n)) ** 0.6
        pts.append((12 + w + (0.9 if i % 2 else -0.4), y))
    for i in range(n, -1, -1):
        y = 3 + i * 17 / n
        w = 7.4 * math.sin(math.pi * (0.06 + 0.88 * i / n)) ** 0.6
        pts.append((12 - w - (0.9 if i % 2 else -0.4), y))
    return [shell(smooth(pts)), line("M12 20V22.4"), detail("M12 5.4V19.4"), detail("M12 10L8.6 8M12 10L15.4 8"),
            detail("M12 14.6L8.4 12.8M12 14.6L15.6 12.8")]


@icon("spinach", CAT, "Bunch of three smooth spade shaped spinach leaves on long stems",
      tags=["leafy green", "salad", "popeye", "baby spinach", "vegetable", "produce"])
def _(S):
    return [shell(leaf(10.4, 13.4, 4, 6.2, 3)), shell(leaf(13.6, 13.4, 20, 6.2, 3)), shell(leaf(12, 10.6, 12, 2.6, 3)),
            line("M10.4 13.4Q12 17 12 21.8"), line("M13.6 13.4Q12 17 12 21.8"), line("M12 10.6V21.8")]


@icon("swiss-chard", CAT, "Large crinkled chard leaf on a thick wide stem rib with branching veins",
      tags=["chard", "rainbow chard", "leafy green", "silverbeet", "vegetable", "produce"])
def _(S):
    leafd = blob(12, 9.8, 6.8, 7.6, [1, 0.92, 1, 0.92, 1, 0.92, 1, 0.92, 1, 0.92, 1, 0.92])
    stem = poly([(10.2, 15), (13.8, 15), (14.4, 22), (9.6, 22)], closed=True, r=L(S, 0, 0.6))
    return [shell(union(leafd, stem)), detail("M12 19V5"), detail("M12 13L8.6 10.4M12 13L15.4 10.4"),
            detail("M12 8.6L9.6 6.4M12 8.6L14.4 6.4")]


@icon("arugula", CAT, "Narrow arugula leaf with deep rounded lobes along both sides like a ladder",
      tags=["rocket", "rucola", "salad green", "peppery", "leafy green", "produce"])
def _(S):
    lobes = [ell(12, 4, 2, 2.6), ell(8, 8, 3.6, 2.2, -28), ell(16, 8, 3.6, 2.2, 28), ell(7.4, 13.2, 3.8, 2.3, -28),
             ell(16.6, 13.2, 3.8, 2.3, 28), ell(8.6, 18, 3, 2, -28), ell(15.4, 18, 3, 2, 28)]
    return [shell(union(rect(10.6, 4, 2.8, 15, L(S, 0, 1.2)), *lobes)), line("M12 18.6V22.2"), detail("M12 7V17")]


@icon("watercress", CAT, "Sprig of small round leaflets in pairs along a thin stem",
      tags=["cress", "salad green", "peppery", "herb", "leafy green", "produce"])
def _(S):
    out = [line("M12 22V6"), shell(circle(12, 4.2, 2.4))]
    for y, dx in ((10.4, 5.4), (17, 5.8)):
        out += [line(seg(12, y, 12 - dx + 2, y)), line(seg(12, y, 12 + dx - 2, y)),
                shell(circle(12 - dx, y, 2.8)), shell(circle(12 + dx, y, 2.8))]
    return out


@icon("endive", CAT, "Tight torpedo shaped endive head of overlapping pointed leaves",
      tags=["chicory", "belgian endive", "witloof", "salad", "leafy vegetable", "produce"])
def _(S):
    return [shell(drop(S, (12, 19.6), (12, 2.6), 5.6)), detail("M12 4.6C8.8 8.6 8.6 14 11 19"),
            detail("M12 4.6C15.2 8.6 15.4 14 13 19"), line("M9.8 21.2H14.2")]


@icon("celery", CAT, "Bunch of ribbed celery stalks with a cluster of small leaves at the top",
      tags=["celery stalks", "stalk vegetable", "crudites", "soup base", "vegetable", "produce"])
def _(S):
    bunch = poly([(8, 21.8), (6.4, 11), (17.6, 11), (16, 21.8)], closed=True, r=L(S, 0, 1.4))
    return [shell(bunch), detail("M10.4 13.4V20.6M13.6 13.4V20.6"), shell(leaf(8.4, 10.6, 5, 4, 1.9)),
            shell(leaf(12, 10.6, 12, 2.8, 1.9)), shell(leaf(15.6, 10.6, 19, 4, 1.9))]


@icon("asparagus", CAT, "Bundle of straight asparagus spears with scaled pointed tips, tied with a band",
      tags=["spears", "green asparagus", "spring vegetable", "bundle", "vegetable", "produce"])
def _(S):
    def spear(x, top, deg=0):
        pts = [(x - 2, 21.6), (x - 2, top + 5), (x, top), (x + 2, top + 5), (x + 2, 21.6)]
        return poly(rpts(pts, deg, 12, 21.6), closed=True, r=L(S, 0, 1))
    mid = spear(12, 2.6)
    return [shell(cut(spear(7, 5.4, -9), mid, g=2.2)), shell(cut(spear(17, 5.4, 9), mid, g=2.2)), shell(mid),
            detail("M5 17H19")]


@icon("artichoke", CAT, "Globe artichoke made of layered pointed bracts on a short stem",
      tags=["globe artichoke", "bracts", "thistle", "mediterranean", "vegetable", "produce"])
def _(S):
    body = smooth([(12, 2.8), (15.6, 5.4), (18.6, 9.8), (18.4, 15), (15.4, 19), (12, 20), (8.6, 19), (5.6, 15), (5.4, 9.8),
                   (8.4, 5.4)])
    return [shell(body), line("M12 20V22.4"),
            detail(poly([(6.6, 10.6), (9.3, 13.4), (12, 10.6), (14.7, 13.4), (17.4, 10.6)], r=S.r)),
            detail(poly([(7.6, 15.4), (9.8, 17.6), (12, 15.4), (14.2, 17.6), (16.4, 15.4)], r=S.r))]


@icon("leek", CAT, "Long white leek stem with roots at the bottom and flat leaves fanning out at the top",
      tags=["alliums", "vegetable", "soup", "potato leek", "welsh emblem", "produce"])
def _(S):
    return [shell(rect(9.4, 9.4, 5.2, 10, L(S, 0.4, 2))), shell(leaf(10.6, 9.6, 4, 3, 1.9)),
            shell(leaf(13.4, 9.6, 20, 3, 1.9)), shell(leaf(12, 9.4, 12, 2.4, 1.7)),
            line("M10.6 19.4L9.4 22M12 19.4V22M13.4 19.4L14.6 22"), detail("M9.4 13.6H14.6")]


@icon("green-onion", CAT, "Three thin green onion stalks with small white bulbs and wispy roots",
      tags=["scallion", "spring onion", "shallot", "chive", "allium", "garnish", "produce"])
def _(S):
    bulbs = union(circle(6.8, 15.6, 2.4), circle(12, 16.4, 2.6), circle(17.2, 15.6, 2.4))
    return [shell(bulbs), line("M6.8 13.2L5.8 2.6"), line("M12 13.8V2.4"), line("M17.2 13.2L18.2 2.6"),
            line("M6.8 18.2L5.8 21.4M12 19L12 22M17.2 18.2L18.2 21.4")]


@icon("garlic-clove", CAT, "Single curved garlic clove with a pointed tip and a flat root end",
      tags=["garlic", "clove", "allium", "seasoning", "vampire", "kitchen", "produce"])
def _(S):
    body = ("M13 2.8C8.4 6 6.2 12 7.2 17.2Q7.6 20.6 10 20.6H16Q18.6 20.6 18.2 17C17.8 12 15.6 6 13 2.8Z" if S.name == "line" else
            "M13 3.6C8.6 6.6 6.2 12 7.2 17.2Q7.6 20.6 10.4 20.6H15.6Q18.6 20.6 18.2 17C17.8 12 15.6 6.6 13.6 3.6Q13 2.8 13 3.6Z")
    return [shell(body), detail("M11.4 8.6C9.8 12 9.8 15 10.6 17.4")]


# =========================================================================== alliums, roots and tubers

@icon("garlic-braid", CAT, "Braided plait of garlic bulbs hanging from a loop",
      tags=["garlic", "braid", "plait", "hanging garlic", "allium", "kitchen", "produce"])
def _(S):
    def bulb(cx, cy, r=3.2):
        return union(circle(cx, cy + 0.6, r), poly([(cx - 1.4, cy - 1.4), (cx, cy - r - 0.6), (cx + 1.4, cy - 1.4)], closed=True))
    center = bulb(12, 18.4)
    return [shell(circle(12, 3.2, 1.6)), line(poly([(12, 4.8), (10.6, 7.6), (13.4, 10.4), (10.8, 13.2), (12, 15)], r=S.r)),
            shell(cut(bulb(6.8, 13), center, g=2.2)), shell(cut(bulb(17.2, 13), center, g=2.2)), shell(center)]


@icon("garlic-scape", CAT, "Long garlic scape curling over at the top into a pointed flower bud",
      tags=["garlic", "scape", "stem", "curl", "spring", "allium", "produce"])
def _(S):
    return [line("M7 22C7 12 8 3.8 13.4 3.8C17.6 3.8 19 7 18.6 9"), shell(drop(S, (18.6, 9.4), (18.6, 18), 2.4)),
            detail("M18.6 12.4V15")]


@icon("onion-half", CAT, "Onion cut in half showing concentric ring layers and a small root tuft",
      tags=["onion", "cut onion", "rings", "layers", "allium", "cooking", "produce"])
def _(S):
    outline = [(12, 3), (15.6, 7), (18, 12.6), (16.8, 17.8), (12, 20.6), (7.2, 17.8), (6, 12.6), (8.4, 7)]

    def scaled(k):
        return smooth([(12 + (x - 12) * k, 12.8 + (y - 12.8) * k) for x, y in outline])
    return [shell(smooth(outline)), detail(scaled(0.58)), line("M10.6 20.6L10 22.4M13.4 20.6L14 22.4"), sp(12, 12.8, 0.9)]


@icon("fennel", CAT, "Round layered white fennel bulb with stalks rising to feathery fronds",
      tags=["bulb fennel", "anise", "herb", "licorice", "vegetable", "produce"])
def _(S):
    return [shell(ellipse(12, 16, 6.8, 5.4)), line("M9 10.8L7.6 5.6"), line("M12 10.6V4.4"), line("M15 10.8L16.4 5.6"),
            line("M7.6 5.6L5.6 3M7.6 5.6L9.6 3"), line("M12 4.4L10.4 2M12 4.4L13.6 2"), line("M16.4 5.6L14.4 3M16.4 5.6L18.4 3"),
            detail("M9 13.6Q8.4 16 10 19")]


@icon("kohlrabi", CAT, "Round kohlrabi bulb with leaf stalks sprouting from its sides and top",
      tags=["german turnip", "brassica", "stem vegetable", "bulb", "vegetable", "produce"])
def _(S):
    return [shell(circle(12, 15.4, 6.2)), line("M7.4 11.2L6 9"), shell(leaf(6, 9, 3, 4.2, 1.7)), line("M12 9.2V7.6"),
            shell(leaf(12, 7.6, 12, 2.6, 1.7)), line("M16.6 11.2L18 9"), shell(leaf(18, 9, 21, 4.2, 1.7)),
            detail("M8.6 14.4Q8.6 17.4 10.4 19")]


@icon("beet", CAT, "Round beet root with a long tapering tail and leaf stalks with leaves on top",
      tags=["beetroot", "red beet", "root vegetable", "borscht", "vegetable", "produce"])
def _(S):
    body = union(circle(12, 13.2, 6.4), poly([(8.4, 17.2), (12, 22), (15.6, 17.2)], closed=True, r=L(S, 0, 0.8)))
    return [shell(body), line("M11 7.4L8 4.4"), shell(leaf(8, 4.4, 4.4, 2.2, 1.7)),
            line("M13 7.4L16 4.4"), shell(leaf(16, 4.4, 19.6, 2.2, 1.7)), detail("M8.2 12.6Q8.2 15.6 10 17.4")]


@icon("radish", CAT, "Small round radish with a thin tail, a banded top and two leaves",
      tags=["red radish", "salad", "root vegetable", "spring", "vegetable", "produce"])
def _(S):
    return [shell(circle(12, 13.6, 6.4)), line("M12 20L12.6 22.2"), line("M11 7.6L8 5"), shell(leaf(8, 5, 3.6, 2.4, 1.8)),
            line("M13 7.6L16 5"), shell(leaf(16, 5, 20.4, 2.4, 1.8)), detail("M6.8 12Q12 14.2 17.2 12")]


@icon("daikon", CAT, "Long thick white daikon radish tapering at the bottom with leafy tops",
      tags=["mooli", "white radish", "japanese radish", "root vegetable", "vegetable", "produce"])
def _(S):
    parts = [shell(drop(S, (12, 8.2), (12, 22.4), 4.6)), shell(leaf(11, 6.8, 7.6, 2, 1.6)), shell(leaf(13, 6.8, 16.4, 2, 1.6)),
             detail("M9 11Q8.6 15 10.6 18.6")]
    return [Part(p.kind, rotd(p.d, 24), p.attrs) for p in parts]


@icon("turnip", CAT, "Flattened globe turnip with a color band across the top and a thin taproot",
      tags=["root vegetable", "swede", "rutabaga", "vegetable", "garden", "produce"])
def _(S):
    return [shell(ellipse(12, 12.6, 8.4, 6.8)), line("M12 19.4L12.6 22.2"), line("M10 5.8L9 3M14 5.8L15 3"),
            detail("M4.8 10.8Q12 13.2 19.2 10.8")]


@icon("carrot-slices", CAT, "Three overlapping round carrot coins, each with a small core ring",
      tags=["carrot", "coins", "sliced carrot", "chopped", "vegetable", "produce"])
def _(S):
    r = L(S, 4.8, 5.4)
    a, b, c = circle(7.2, 7.8, r), circle(16.8, 8.6, r), circle(11.8, 16.4, r)
    return [shell(cut(a, b, c, g=2.2)), shell(cut(b, c, g=2.2)), shell(c), detail(circle(11.8, 16.4, 1.8)), sp(7.2, 7.4, 0.9),
            sp(16.8, 8.2, 0.9)]


@icon("sweet-potato", CAT, "Long lumpy sweet potato tapered at both ends with root hairs and eye marks",
      tags=["yam", "tuber", "root vegetable", "kumara", "vegetable", "produce"])
def _(S):
    body = rotd(blob(12, 12, 9.4, 4.4, [1, 0.92, 1.04, 0.94, 0.9, 0.95, 1, 0.9, 1.04, 0.94]), -36)
    parts = [line(rotd("M21.4 12L23 12", -36))]
    return [shell(body), line(rotd("M2.4 12L0.8 12", -36).replace("0.8", "1.2")), detail(rotd("M9 11L10.6 11", -36)), detail(rotd("M14 13L15.6 13", -36))]


@icon("cassava", CAT, "Long tapered cassava root with bark ring lines, cut at the thick end to show white flesh",
      tags=["yuca", "manioc", "tapioca", "root vegetable", "tuber", "produce"])
def _(S):
    pts = rpts([(7.6, 5), (16.4, 5), (14.6, 14), (12.8, 21.6), (11.2, 21.6), (9.4, 14)], 28, 12, 12)
    cutface = rot(ellipse(12, 5, 4.4, 1.8), 28, 12, 12)
    rings = [detail(rotd(f"M{fmt(x - 2.4)} {fmt(y)}Q{fmt(x)} {fmt(y + 1.4)} {fmt(x + 2.4)} {fmt(y)}", 28)) for x, y in ((12, 11.4), (12, 16))]
    return [shell(poly(pts, closed=True, r=L(S, 0, 1.2))), detail(cutface), *rings]


@icon("taro", CAT, "Round hairy taro corm with ring lines and a short stub on top",
      tags=["eddoe", "dasheen", "root vegetable", "corm", "tuber", "produce"])
def _(S):
    body = spiky(12, 14, 7.4, 6.8, 14, 1.0, S, skip=())
    stub = rect(10.4, 3.2, 3.2, 4, L(S, 0, 1))
    return [shell(union(body, stub)), detail("M6.4 12.4Q12 15 17.6 12.4"), detail("M6.8 16.6Q12 19.2 17.2 16.6")]


@icon("ginger-root", CAT, "Knobbly branching ginger rhizome with finger like lumps and ring lines on the skin",
      tags=["ginger", "rhizome", "spice", "root", "tea", "cooking", "produce"])
def _(S):
    k = L(S, 0.95, 1.08)
    body = union(ell(12, 15.8, 8.2 * k, 4.4 * k, -8), ell(6.2, 10.4, 2.6 * k, 3.8 * k, -14), ell(11.8, 9.4, 2.6 * k, 4.2 * k, -4),
                 ell(17.4, 10.8, 2.6 * k, 3.8 * k, 16))
    return [shell(body), detail("M5 11L7.4 10.4"), detail("M10.6 9L13 9"), detail("M16.2 11L18.6 11.6"), detail("M10 15.4L10.4 18")]


@icon("lotus-root", CAT, "Cross section slice of lotus root showing a round outline with a ring of holes around a center hole",
      tags=["lotus", "renkon", "rhizome", "slice", "asian vegetable", "holes", "produce"])
def _(S):
    ring = [sp(*pt_(12, 12, 4.8, a), 1.6) for a in (-90, -30, 30, 90, 150, 210)]
    head = circle(12, 12, 9) if S.name == "line" else blob(12, 12, 9, 9, [1, 0.96] * 6)
    return [shell(head), sp(12, 12, 1.6), *ring]


# =========================================================================== stalks, plants and sprouts

@icon("rhubarb", CAT, "Several long rhubarb stalks with a large wavy crinkled leaf on top",
      tags=["pie plant", "stalks", "red stalks", "garden", "crumble", "vegetable", "produce"])
def _(S):
    leafd = blob(12, 7.2, 9.4, 4.4, [1, 0.9, 1, 0.9, 1, 0.9, 1, 0.9, 1, 0.9])
    return [shell(leafd), line("M12 22V11.6"), line("M12 22L7.4 11.4"), line("M12 22L16.6 11.4"),
            detail("M12 10V4.4"), detail("M12 8.6L8 6.4M12 8.6L16 6.4")]


@icon("sugarcane", CAT, "Two tall segmented sugarcane stalks with joint rings and narrow leaves at the top",
      tags=["cane", "sugar cane", "stalk", "sweetener", "tropical", "plant", "produce"])
def _(S):
    return [shell(rect(5.4, 9, 4.2, 13, L(S, 0, 1.4))), shell(rect(14.4, 7.4, 4.2, 14.6, L(S, 0, 1.4))),
            detail("M5.4 14.6H9.6M5.4 19H9.6"), detail("M14.4 13H18.6M14.4 17.4H18.6"),
            shell(leaf(7.4, 9, 3.4, 3, 1.1)), shell(leaf(7.6, 9, 11.4, 2.6, 1.1)), shell(leaf(16.4, 7.4, 21, 3.4, 1.1)),
            shell(leaf(16.4, 7.4, 13.4, 2.2, 1.1))]


@icon("wasabi-root", CAT, "Thick knobbly wasabi stem with ring scars and two heart shaped leaves on long stalks",
      tags=["wasabi", "horseradish", "sushi", "japanese", "rhizome", "spice", "produce"])
def _(S):
    def heart(cx, cy):
        return union(circle(cx - 1.7, cy - 0.6, 2.3), circle(cx + 1.7, cy - 0.6, 2.3),
                     poly([(cx - 3.8, cy + 0.2), (cx, cy + 4.4), (cx + 3.8, cy + 0.2)], closed=True))
    stem = union(rect(3, 15.2, 18, 5.8, L(S, 1.4, 2.9)), circle(6.6, 15.2, 1.9), circle(15.4, 15.2, 2.1))
    return [shell(stem), detail("M8 15.8V20.4M12.4 15.8V20.4M16.6 15.8V20.4"), line("M9.6 14.6L7 9.4"), line("M14.4 14.6L17 9.4"),
            shell(heart(6, 5.6)), shell(heart(18, 5.6))]


@icon("bean-sprout", CAT, "Curved thin white bean sprout with a small bean head and a thread like root tail",
      tags=["mung bean", "sprouts", "stir fry", "asian vegetable", "germinated", "produce"])
def _(S):
    return [shell(ell(16.6, 5.2, 3.6, 2.7, -24)), line("M14.8 7.8C7.4 9.4 7.6 14.6 11.4 17.4C13.2 18.8 12.4 20.6 11 22.2"),
            detail("M14.6 3.8L18.4 6.4")]


@icon("potato-plant", CAT, "Leafy potato plant above the ground line with round potatoes hanging on roots below",
      tags=["potato", "garden", "growing", "tubers", "harvest", "farm", "produce"])
def _(S):
    return [line("M12 11.4V7"), shell(leaf(12, 8.6, 6.4, 4.8, 1.7)), shell(leaf(12, 8.6, 17.6, 4.8, 1.7)),
            shell(leaf(12, 7, 12, 2, 1.6)), line("M2 11.4H22"), line("M12 11.4V15"), line("M12 15L8 17"), line("M12 15L16 16.4"),
            shell(ell(6.2, 18.6, 3.4, 2.5, -20)), shell(ell(17, 18.4, 3.4, 2.5, 20)), shell(ell(12, 20.2, 2.6, 1.9))]


@icon("sprouting-potato", CAT, "Potato with a few short curled sprouts growing out of its eyes",
      tags=["potato", "chitting", "sprouts", "eyes", "seed potato", "tuber", "produce"])
def _(S):
    body = blob(12, 15, 8.4, 6, [1, 0.94, 1.04, 0.95, 1, 0.94, 1.04, 0.95, 1, 0.94])
    return [shell(body), line("M8.6 10C7.4 7.4 8.6 4.6 10.8 4.8C12.2 5 12.2 6.6 11 6.8"),
            line("M13.4 9.6C13.4 7.4 14.8 5.4 16.8 5.8C18 6.2 17.8 7.6 16.8 7.6"),
            line("M17.4 12.2C19 11.4 20.8 11.8 21 13.4"), sp(8.4, 15.4, 0.9), sp(14.4, 17.4, 0.9), sp(16, 14.2, 0.9)]


@icon("squash-blossom", CAT, "Trumpet shaped squash flower with pointed petals attached to a small squash",
      tags=["zucchini flower", "courgette flower", "edible flower", "blossom", "vegetable", "produce"])
def _(S):
    flower = poly([(5, 3), (8.6, 7.4), (12, 2.8), (15.4, 7.4), (19, 3), (15.6, 11.4), (13.4, 13.6), (10.6, 13.6), (8.4, 11.4)],
                  closed=True, r=L(S, 0, 0.8))
    squash = ell(12, 18.4, 3.2, 4)
    return [shell(union(flower, squash)), detail("M12 6.8V12"), line("M12 22.4V23")] if False else \
        [shell(union(flower, squash)), detail("M12 7V12.4")]


def kidney(S, cx, cy, deg=0, k=0.82):
    """Kidney bean: a capsule with a round bite out of its inner edge."""
    w, h = 11.2 * k, 6.8 * k
    body = minus(rect(cx - w / 2, cy - h / 2, w, h, L(S, 2.4, h / 2)), circle(cx, cy - h / 2 - 1.2, 2.2))
    return rot(body, deg, cx, cy)


@icon("kidney-bean", CAT, "Three kidney shaped beans each with a small curved notch on the inner edge",
      tags=["red beans", "beans", "legume", "chili beans", "pulse", "produce"])
def _(S):
    return [shell(kidney(S, 7.4, 6.2, -16)), shell(kidney(S, 16.6, 11, 24)), shell(kidney(S, 8.6, 18, 4))]


@icon("black-eyed-pea", CAT, "Oval bean with a dark eye spot and ring on its inner curve",
      tags=["cowpea", "bean", "legume", "southern food", "pea", "pulse", "produce"])
def _(S):
    body = ellipse(12, 12, 8.4, 5.8) if S.name == "line" else rect(3.6, 6.2, 16.8, 11.6, 5.8)
    return [shell(rot(body, -24)), detail(rot(circle(11.6, 9.6, 2.5), -24)), sp(11.6, 9.6, 0.8)]


@icon("chickpea", CAT, "Round lumpy chickpea with a small pointed beak on one side",
      tags=["garbanzo", "chick pea", "legume", "hummus", "pulse", "produce"])
def _(S):
    body = blob(12, 13.4, 7.2, 7, [1, 0.96, 1.02, 0.95, 1, 0.97, 1.03, 0.96, 1, 0.95])
    beak = poly([(13.6, 7.4), (17.2, 3.2), (17.8, 9.4)], closed=True, r=L(S, 0, 0.6))
    return [shell(union(body, beak)), detail("M7.8 14Q9.4 17.6 13 18.2")]


@icon("lentils", CAT, "Small heap of flat round lentils piled in three rows",
      tags=["lentil", "dal", "pulse", "legume", "red lentils", "produce"])
def _(S):
    def disc(x, y):
        return leaf(x - 3.8, y, x + 3.8, y, 2.2) if S.name == "line" else ellipse(x, y, 3.8, 2.3)
    spots = [(12, 9.8), (8.6, 14), (15.4, 14), (6, 18.6), (12, 18.6), (18, 18.6)]
    out = []
    for i, (x, y) in enumerate(spots):
        later = [disc(*p) for p in spots[i + 1:]]
        d = disc(x, y)
        out.append(shell(cut(d, *later, g=2.0) if later else d))
    return out


@icon("mixed-beans", CAT, "Pile of three kinds of beans: a kidney bean, a round bean and an oval bean with an eye",
      tags=["beans", "bean mix", "legumes", "pulses", "three bean salad", "produce"])
def _(S):
    ov = rot(ellipse(16.6, 17.4, 4.4, 3.2), -16, 16.6, 17.4)
    return [shell(circle(12, 7, 3.6)), shell(kidney(S, 7.4, 17.6, -8, 0.78)), shell(ov), sp(16.4, 17.2, 0.8)]


@icon("cocoa-pod", CAT, "Football shaped cocoa pod with deep lengthwise ridges and a short stem",
      tags=["cacao", "chocolate", "pod", "tropical", "bean pod", "produce"])
def _(S):
    body = leaf(12, 4, 12, 20.6, 6.2) if S.name == "line" else ellipse(12, 12.3, 6.2, 8.4)
    return [shell(rot(body, 34)), line(rotd("M12 4.2L12 1.8", 34)), detail(rotd("M12 6C8.8 9.4 8.8 15.2 12 18.8", 34)),
            detail(rotd("M12 6C15.2 9.4 15.2 15.2 12 18.8", 34)), detail(rotd("M12 6L12 18.8", 34))]


@icon("vanilla-bean", CAT, "Long thin curved vanilla pod lying next to a small open orchid flower",
      tags=["vanilla", "pod", "orchid", "spice", "baking", "flavouring", "produce"])
def _(S):
    petals = union(*[circle(*pt_(17.4, 16.4, 2.8, a), 2.1) for a in (-90, -18, 54, 126, 198)])
    return [shell(pod(S, (4.4, 20.4), (12.6, 4.4), 1.9, 2.6)), shell(petals), detail(circle(17.4, 16.4, 0.9))]


@icon("carob-pod", CAT, "Long flat curved carob pod with wavy edges and a row of seed bumps",
      tags=["locust bean", "chocolate substitute", "pod", "mediterranean", "legume", "produce"])
def _(S):
    P0, P1, P2 = (3.6, 19.8), (5.6, 5.4), (20.6, 5)
    amp = L(S, 0.5, 0.25)
    up, dn = [], []
    n = 10
    for i in range(n + 1):
        t = i / n
        x = (1 - t) ** 2 * P0[0] + 2 * (1 - t) * t * P1[0] + t * t * P2[0]
        y = (1 - t) ** 2 * P0[1] + 2 * (1 - t) * t * P1[1] + t * t * P2[1]
        dx = 2 * (1 - t) * (P1[0] - P0[0]) + 2 * t * (P2[0] - P1[0])
        dy = 2 * (1 - t) * (P1[1] - P0[1]) + 2 * t * (P2[1] - P1[1])
        ln = math.hypot(dx, dy)
        nx, ny = -dy / ln, dx / ln
        w = 3.5 * math.sin(math.pi * (0.08 + 0.84 * t)) ** 0.5
        wob = amp * math.sin(t * math.pi * 6)
        up.append((x + nx * (w + wob), y + ny * (w + wob)))
        dn.append((x - nx * (w - wob), y - ny * (w - wob)))
    body = smooth(up + dn[::-1])
    seeds = []
    for t in (0.3, 0.5, 0.7):
        x = (1 - t) ** 2 * P0[0] + 2 * (1 - t) * t * P1[0] + t * t * P2[0]
        y = (1 - t) ** 2 * P0[1] + 2 * (1 - t) * t * P1[1] + t * t * P2[1]
        seeds.append(sp(x, y, 0.9))
    return [shell(body), *seeds]


@icon("rice-stalk", CAT, "Rice stalk with a drooping panicle of small oval grains hanging at the top",
      tags=["rice", "paddy", "grain", "harvest", "farm", "cereal", "produce"])
def _(S):
    grains = []
    for x, y, a in ((12.4, 5.6, 8), (15.4, 5.2, 4), (18, 7, -4), (19.6, 10.2, -12), (13.6, 8.8, 14)):
        grains.append(solid(rotd(drop(S, (x, y), (x + 0.9, y + 4), 1.0), a, x, y)))
    return [line("M7.6 22C7.6 15 9 7 14.4 4.4C17.8 3.2 20 5.8 20 9"), *grains, shell(leaf(8.4, 17.2, 3.2, 10.2, 1.3))]


@icon("rice-grains", CAT, "Small heap of long oval grains of rice",
      tags=["rice", "grains", "cereal", "staple", "white rice", "uncooked", "produce"])
def _(S):
    grains = [((3.2, 19.4), (10.4, 16.2)), ((13.4, 20.4), (20.6, 17.4)), ((7.8, 14), (15.4, 10.2)),
              ((5, 8.6), (11.6, 5.4)), ((13.6, 5.6), (20.6, 8.6))]
    out = []
    for i, (a, b) in enumerate(grains):
        out.append(shell(pod(S, a, b, 1.7, 0.4)))
    return out


@icon("barley", CAT, "Ear of barley with plump kernels and very long straight bristle awns pointing upward",
      tags=["grain", "cereal", "malt", "awns", "wheat", "brewing", "produce"])
def _(S):
    out = [line("M12 22V9.6")]
    for y, off in ((19.6, 0), (15.6, 0), (11.6, 0)):
        out.append(shell(pod(S, (12, y), (8.8, y - 4), 1.7, 0.2)))
        out.append(shell(pod(S, (12, y), (15.2, y - 4), 1.7, -0.2)))
    out += [line("M8.8 15.6L5.4 7.6"), line("M15.2 15.6L18.6 7.6"), line("M8.8 7.6L7.4 2.4"), line("M15.2 7.6L16.6 2.4"),
            line("M12 7.6V2")]
    return out


@icon("bamboo-shoot", CAT, "Cone shaped bamboo shoot wrapped in layered pointed sheaths with a cut base",
      tags=["bamboo", "shoot", "asian vegetable", "stir fry", "spring", "takenoko", "produce"])
def _(S):
    body = ("M14 2.6C14 8 18.8 13 18.6 19.4Q11.6 22.2 4.6 19.4C5.4 13 12.2 8 14 2.6Z" if S.name == "line" else
            "M14 3.6C14 8.6 18.8 13 18.6 19.4Q11.6 22.2 4.6 19.4C5.4 13.4 12 8.6 13.4 3.8Q13.8 2.8 14 3.6Z")
    return [shell(body), detail("M8 12.4Q12 9.2 16.2 12.6"), detail("M6.6 17.2Q11.4 13.4 17.6 17")]


@icon("fiddlehead", CAT, "Tightly coiled young fern frond curling into a spiral on top of a short stalk",
      tags=["fern", "fiddlehead fern", "ostrich fern", "spring", "foraging", "spiral", "produce"])
def _(S):
    N = 18
    pts = []
    for i in range(N + 1):
        th = math.pi / 2 + 2 * math.pi * 1.5 * (i / N - 1)
        r = 1.4 + 6.6 * i / N
        pts.append((12 + r * math.cos(th), 10.4 + r * math.sin(th)))
    return [line(smooth(pts, closed=False)), line("M12 18.4V22"), sp(*pts[0], 0.9 if S.name == "line" else 1.1)]
