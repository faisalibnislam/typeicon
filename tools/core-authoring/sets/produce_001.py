"""TypeIcon Core: produce (batch produce_001): fruits, berries and nuts.

Drawn from the fruit itself: upright side views with the stem at the top, halves shown face on.
Stems and stalks are open strokes; seeds and pits are small solid dots that the Filled style knocks out.
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


# =========================================================================== orchard and stone fruit

@icon("quince", CAT, "Lumpy pear shaped quince with a woody stem and a leaf",
      tags=["fruit", "pome", "orchard", "membrillo", "autumn", "produce"])
def _(S):
    body = smooth([(12, 7), (14.6, 8), (15.9, 10.4), (18.6, 12.2), (19.8, 15.4), (18.8, 18.8), (15.8, 20.8),
                   (12.4, 20.2), (8.6, 20.9), (5.4, 18.9), (4.2, 15.4), (5.4, 12.2), (8.1, 10.4), (9.4, 8)])
    return [shell(body), line("M12 7L11.4 3.2"), shell(leaf(12.6, 5, 18.2, 3.4, 1.2)),
            detail("M15.2 12.4Q17 14 16.6 16.8")]


@icon("plum", CAT, "Oval plum with a crease down one side and a short bare stem",
      tags=["fruit", "stone fruit", "damson", "prune", "orchard", "produce"])
def _(S):
    body = "M12 6.8C10.2 5.4 5 6.6 5 13.2C5 18.4 8.2 21.5 12 21.5C15.8 21.5 19 18.4 19 13.2C19 6.6 13.8 5.4 12 6.8Z"
    return [shell(rot(body, 12, 12, 14)), detail(rot("M12 6.8C14.8 9.6 15.4 15.2 13.6 19.6", 12, 12, 14)),
            line(rot("M12 6.8C12 5 12.4 3.8 13.3 2.8", 12, 12, 14))]


@icon("prune", CAT, "Dried plum with a wrinkled skin and a tiny stem stub",
      tags=["dried plum", "dried fruit", "fiber", "snack", "wrinkled", "produce"])
def _(S):
    body = blob(12, 13.5, 8.6, 6.8, [1, 0.94, 1.02, 0.95, 1.0, 0.93, 1.02, 0.96, 1.0, 0.94, 1.03, 0.95])
    return [shell(body), line(seg(12, 6.7, 12.6, 4)),
            detail("M6.6 12C8.4 10.8 9.8 13 11.8 11.9C13.6 10.9 15.2 12.6 17.4 11.6"),
            detail("M6.8 15.6C8.8 14.6 10.2 16.8 12.2 15.7C14 14.7 15.6 16.4 17.2 15.6")]


@icon("date-fruit", CAT, "Two elongated dates with wrinkle lines and small caps",
      tags=["date", "dates", "medjool", "dried fruit", "ramadan", "produce"])
def _(S):
    out = []
    for cx, cy, a in ((7.4, 13.6, -10), (16.6, 11.6, 10)):
        top = cy - 7
        (x1, y1), (x2, y2) = rpts([(cx, top + 0.2), (cx, top - 1.8)], a, cx, cy)
        out += [shell(rot(ellipse(cx, cy, 3, 7), a, cx, cy)), line(seg(x1, y1, x2, y2)),
                detail(rot(f"M{fmt(cx - 0.6)} {fmt(cy - 3.6)}Q{fmt(cx + 0.9)} {fmt(cy)} {fmt(cx - 0.4)} {fmt(cy + 3.8)}", a, cx, cy))]
    return out


@icon("olive-fruit", CAT, "Two olives hanging from a sprig with narrow leaves",
      tags=["olive", "olives", "olive branch", "mediterranean", "olive oil", "produce"])
def _(S):
    twig = "M3 7.2C8 5.6 14 5.4 21 6.6"
    o1 = rot(ellipse(8, 15.6, 3, 4), -12, 8, 15.6)
    o2 = rot(ellipse(16.2, 16.6, 3, 4), 12, 16.2, 16.6)
    return [line(twig), shell(leaf(6, 6.4, 3, 2.5, 0.8)), shell(leaf(12.5, 5.7, 16.5, 2.2, 0.9)),
            shell(leaf(18, 6.2, 21.5, 9.6, 0.8)),
            line("M8.4 6.1L8.7 11.7"), line("M15.2 6L15.6 12.7"),
            shell(o1), shell(o2), dot(7.8, 16.3, 1.1)]


FIG = "M12 5C10 7.6 4.5 10.4 4.5 15.5C4.5 19.2 7.8 21.5 12 21.5C16.2 21.5 19.5 19.2 19.5 15.5C19.5 10.4 14 7.6 12 5Z"
FIG_R = ("M12.8 5.8C15 8.2 19.5 10.8 19.5 15.5C19.5 19.2 16.2 21.5 12 21.5C7.8 21.5 4.5 19.2 4.5 15.5"
         "C4.5 10.8 9 8.2 11.2 5.8Q12 4.9 12.8 5.8Z")


@icon("fig", CAT, "Teardrop shaped fig with a curved stem",
      tags=["fruit", "figs", "mediterranean", "dried fruit", "produce", "orchard"])
def _(S):
    return [shell(L(S, FIG, FIG_R)), line("M12 5.2C12 3.8 12.8 2.8 14.2 2.4"), detail("M9.4 11.2C8.3 13.8 8.5 16.8 10 19")]


@icon("fig-half", CAT, "Fig cut lengthwise showing its rind and seeds",
      tags=["fig", "cut fruit", "seeds", "fruit", "halved", "produce"])
def _(S):
    outer = ("M12 4C10 6.8 3.5 9.8 3.5 15.3C3.5 19.3 7.3 21.8 12 21.8C16.7 21.8 20.5 19.3 20.5 15.3"
             "C20.5 9.8 14 6.8 12 4Z")
    outer_r = ("M12.9 4.9C15.3 7.5 20.5 10.3 20.5 15.3C20.5 19.3 16.7 21.8 12 21.8C7.3 21.8 3.5 19.3 3.5 15.3"
               "C3.5 10.3 8.7 7.5 11.1 4.9Q12 3.9 12.9 4.9Z")
    inner = "M12 8.8C10.5 10.5 6.8 12.3 6.8 15.5C6.8 17.6 9 18.6 12 18.6C15 18.6 17.2 17.6 17.2 15.5C17.2 12.3 13.5 10.5 12 8.8Z"
    return [shell(L(S, outer, outer_r)), detail(inner), line("M12 4.2V2.2"),
            dot(12, 12.4, 0.85), dot(9.8, 14.5, 0.85), dot(14.2, 14.5, 0.85), dot(10.8, 16.6, 0.85), dot(13.2, 16.6, 0.85)]


@icon("pomegranate", CAT, "Round pomegranate with a pointed crown, cut open to show its seeds",
      tags=["fruit", "grenadine", "seeds", "arils", "superfood", "produce"])
def _(S):
    crown = poly([(8.9, 9), (8.3, 3.6), (10.3, 5.4), (12, 3), (13.7, 5.4), (15.7, 3.6), (15.1, 9)], closed=True, r=L(S, 0, 0.6))
    body = union(circle(12, 14, 7.5), crown)
    seeds = [dot(12, 14.8, 0.85)] + [dot(x, y, 0.85) for x, y in regular(12, 14.8, 2.5, 6, -90)]
    return [shell(body), detail(circle(12, 14.8, 4.9)), *seeds]


@icon("persimmon", CAT, "Flattened squarish persimmon with a large four leaf calyx and a short stem",
      tags=["fruit", "kaki", "sharon fruit", "autumn", "orchard", "produce"])
def _(S):
    body = blob(12, 14.4, 8.6, 6.8, [1, 1.08, 1, 1.08, 1, 1.08, 1, 1.08])
    calyx = poly([(6.6, 10.6), (10, 10.8), (8.6, 13.6), (12, 12), (15.4, 13.6), (14, 10.8), (17.4, 10.6), (12, 9.4)],
                  closed=True, r=L(S, 0, 0.6))
    return [shell(body), detail(calyx), line(poly([(12, 10.4), (12, 5.8), (13, 4.6)], r=S.r))]


@icon("lychee", CAT, "Lychee with a bumpy skin peeled back to show the smooth fruit",
      tags=["litchi", "fruit", "tropical", "asian fruit", "peeled", "produce"])
def _(S):
    cx, cy, R = 12, 13, 8
    pts = []
    for i in range(15):
        a = math.radians(55 + i * 195 / 14)
        rr = R if i % 2 == 0 else R + 0.9
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    sil = poly(pts, r=L(S, 0, 0.5)) + f"A{R} {R} 0 0 1 {_p(pts[0])}Z"
    peel = poly([pts[-1], (10.6, 9.6), (12.9, 11.3), (12.3, 14.4), (14.7, 16.2), pts[0]], r=L(S, 0, 0.8))
    return [shell(sil), detail(peel), detail(arc(cx, cy, 5.2, 285, 335))]


@icon("rambutan", CAT, "Round rambutan covered in soft curly hairs, with a short stem",
      tags=["fruit", "hairy fruit", "tropical", "asian fruit", "lychee", "produce"])
def _(S):
    cx, cy, r = 12, 13.4, 5.2
    out = [shell(circle(cx, cy, r)), line(poly([(12, 8.2), (12, 3), (13.4, 2.2)], r=S.r))]
    for i in range(9):
        a = -90 + 36 + i * 32
        p1 = (cx + (r + 1.6) * math.cos(math.radians(a)), cy + (r + 1.6) * math.sin(math.radians(a)))
        p2 = (cx + (r + 3.4) * math.cos(math.radians(a + 22)), cy + (r + 3.4) * math.sin(math.radians(a + 22)))
        q = (cx + (r + 3.6) * math.cos(math.radians(a - 2)), cy + (r + 3.6) * math.sin(math.radians(a - 2)))
        out.append(line("M" + _p(p1) + "Q" + _p(q) + " " + _p(p2)))
    return out


LONGAN = [(6, 12, 2.9), (18, 12, 2.9), (12, 18.6, 2.9)]


@icon("longan", CAT, "Small round longans hanging from a branching twig",
      tags=["dragon eye", "fruit", "tropical", "asian fruit", "cluster", "produce"])
def _(S):
    fruits = [(6.4, 11.4, 2.9), (17.4, 13.4, 2.9), (10.4, 18.6, 2.9)]
    return [line("M14 2.5C13.4 4.6 12.6 6 11.6 7.2"), line("M11.6 7.2C9.6 7.2 7.4 7.4 6.6 8.5"),
            line("M12.6 6.2C14.8 7.2 16.8 8.6 17.3 10.5"), line("M11.6 7.2C11.4 10 10.8 13 10.5 15.7"),
            *(shell(circle(*c)) for c in fruits)]


@icon("mangosteen", CAT, "Round mangosteen with a flat crown of rounded sepals and a stubby stem",
      tags=["fruit", "tropical", "queen of fruits", "purple fruit", "asian fruit", "produce"])
def _(S):
    cap = union(ellipse(7.6, 8.6, 2.6, 1.8), ellipse(16.4, 8.6, 2.6, 1.8), ellipse(10.4, 9.2, 2.6, 2), ellipse(13.6, 9.2, 2.6, 2))
    ball = circle(12, 14, 7.6)
    return [shell(cut(ball, cap, g=0.001)), shell(cap), detail(cap), shell(rect(10.8, 3, 2.4, 4.6, L(S, 0.3, 1.2)))]


@icon("durian", CAT, "Oval durian covered in sharp spikes with a thick short stem",
      tags=["fruit", "spiky fruit", "tropical", "smelly fruit", "king of fruits", "produce"])
def _(S):
    body = spiky(12, 14, 6.3, 6.6, 16, 1.6, S, skip=(0, 15))
    return [shell(body), shell(rect(10.8, 2.6, 2.4, 5.2, L(S, 0.3, 1.2)))]


@icon("jackfruit", CAT, "Large oblong jackfruit with a bumpy skin and a thick stem",
      tags=["fruit", "tropical", "jack", "vegan meat", "asian fruit", "produce"])
def _(S):
    body = rot(ellipse(12, 13.4, 6.4, 8.6), 32, 12, 13.4)
    st = rot(rect(10.8, 1.6, 2.4, 3.8, L(S, 0.3, 1.2)), 32, 12, 13.4)
    dots = [rpts([p], 32, 12, 13.4)[0] for p in [(9.4, 10), (12.4, 8.6), (14.6, 10.4), (9.8, 13.4), (12.6, 12.2),
                                                   (15, 13.8), (10.2, 16.8), (13, 15.8), (12, 19.2), (14.6, 17.6)]]
    return [shell(body), shell(st), *(dot(x, y, 0.85) for x, y in dots)]


# =========================================================================== tropical fruit


def _flame(cx, cy, rx, ry, a, S, w=16, h=3.4, lean=24):
    """Pointed scale tip poking out of an ellipse at angle a, leaning towards the top."""
    toward = -1 if (a % 360) < 90 or (a % 360) > 270 else 1
    b1, b2 = math.radians(a - w / 2), math.radians(a + w / 2)
    ta = math.radians(a + toward * lean)
    k = 1 + h / ((rx + ry) / 2)
    return poly([(cx + rx * 0.8 * math.cos(b1), cy + ry * 0.8 * math.sin(b1)),
                 (cx + rx * k * math.cos(ta), cy + ry * k * math.sin(ta)),
                 (cx + rx * 0.8 * math.cos(b2), cy + ry * 0.8 * math.sin(b2))], closed=True, r=L(S, 0, 0.5))


@icon("passion-fruit", CAT, "Passion fruit cut in half showing its rind and seedy pulp",
      tags=["maracuja", "granadilla", "fruit", "tropical", "halved", "produce"])
def _(S):
    cx, cy = 12, 13
    seeds = [dot(cx, cy, 0.9)] + [dot(x, y, 0.9) for x, y in regular(cx, cy, 2.9, 7, -90)]
    return [shell(circle(cx, cy, 8.4)), detail(circle(cx, cy, 5.6)), *seeds, line(poly([(12, 4.6), (12, 2.8), (13.4, 1.9)], r=S.r))]


@icon("guava", CAT, "Guava cut in half with pale flesh around a seedy centre",
      tags=["guayaba", "fruit", "tropical", "halved", "pink guava", "produce"])
def _(S):
    body = smooth([(12, 4.4), (16.4, 5.8), (19.6, 10.4), (19.4, 16), (16, 20.2), (12, 21.4), (8, 20.2), (4.6, 16),
                   (4.4, 10.4), (7.6, 5.8)])
    inner = blob(12, 13.4, 4.6, 4.8, [1, 0.82, 1, 0.82, 1, 0.82, 1, 0.82, 1, 0.82])
    seeds = [dot(x, y, 0.8) for x, y in ((12, 11.6), (10.2, 13.8), (13.8, 13.8), (12, 15.6))]
    return [shell(body), detail(inner), *seeds, line(poly([(12, 4.6), (12, 2.4), (13.2, 1.8)], r=S.r))]


PAPAYA = ("M12 2.8C9.6 2.8 8.7 4.8 8.2 7.4C7.4 11 6.2 13.4 6.2 16C6.2 19.6 8.8 21.6 12 21.6"
          "C15.2 21.6 17.8 19.6 17.8 16C17.8 13.4 16.6 11 15.8 7.4C15.3 4.8 14.4 2.8 12 2.8Z")
PAPAYA_CAV = "M12 9.2C10.6 9.2 10 11.4 9.8 13.4C9.5 16.4 10.4 18.6 12 18.6C13.6 18.6 14.5 16.4 14.2 13.4C14 11.4 13.4 9.2 12 9.2Z"


@icon("papaya", CAT, "Papaya cut lengthwise showing the hollow full of seeds",
      tags=["pawpaw", "fruit", "tropical", "halved", "seeds", "produce"])
def _(S):
    body = PAPAYA if S.name == "line" else PAPAYA.replace("M12 2.8C9.6 2.8", "M12 2.8C9.2 2.8")
    seeds = union(*[circle(x, y, 1.25) for x, y in ((12, 9.6), (11, 11.4), (13, 11.4), (10.8, 13.6), (13.2, 13.6),
                                                     (11, 15.8), (13, 15.8), (12, 17.6))])
    return [shell(rot(body, 38, 12, 12.2)), mark(rot(seeds, 38, 12, 12.2))]


@icon("star-fruit", CAT, "Star shaped slice of star fruit with a small star of seeds",
      tags=["carambola", "starfruit", "fruit", "tropical", "slice", "produce"])
def _(S):
    outer = [pt_(12, 12.6, 9.6 if i % 2 == 0 else 6, -90 + i * 36) for i in range(10)]
    inner = [pt_(12, 12.6, 2.9 if i % 2 == 0 else 1.2, -90 + i * 36) for i in range(10)]
    return [shell(poly(outer, closed=True, r=L(S, 2, 3.4))), detail(poly(inner, closed=True, r=L(S, 0, 0.3)))]


def pt_(cx, cy, r, deg):
    return (cx + r * math.cos(math.radians(deg)), cy + r * math.sin(math.radians(deg)))


@icon("custard-apple", CAT, "Heart shaped custard apple covered in rounded scales",
      tags=["cherimoya", "sugar apple", "sweetsop", "annona", "fruit", "produce"])
def _(S):
    body = smooth([(12, 6.6), (15.4, 5.6), (18.8, 7.6), (19.8, 11.4), (18.2, 16), (14.8, 19.8), (12, 21.2),
                   (9.2, 19.8), (5.8, 16), (4.2, 11.4), (5.2, 7.6), (8.6, 5.6)])
    scales = []
    for x, y in ((8.4, 10.4), (12, 10.4), (15.6, 10.4), (10.2, 14), (13.8, 14), (12, 17.6)):
        scales.append(detail(f"M{fmt(x - 1.7)} {fmt(y)}A1.7 1.7 0 0 0 {fmt(x + 1.7)} {fmt(y)}"))
    return [shell(body), *scales, line("M12 6.4L12.6 3")]


@icon("soursop", CAT, "Oblong curved soursop with rows of soft hooked spines",
      tags=["guanabana", "graviola", "fruit", "tropical", "annona", "produce"])
def _(S):
    body = rot(smooth([(12, 3.6), (15.4, 4.8), (17.2, 8.6), (17, 13.4), (15.2, 18), (12, 21), (8.6, 19.8),
                       (7, 15.6), (7.2, 10.6), (8.6, 6.2)]), 18, 12, 12.4)
    hooks = []
    for x, y in ((10, 8.8), (14, 8.4), (10, 12.8), (14, 12.6), (10.4, 16.8), (13.8, 16.6)):
        hooks.append(detail(rot(f"M{fmt(x - 0.8)} {fmt(y + 0.9)}Q{fmt(x - 0.6)} {fmt(y - 0.6)} {fmt(x + 0.9)} {fmt(y - 0.8)}", 18, 12, 12.4)))
    return [shell(body), *hooks, line(rot("M12 3.8V1.8", 18, 12, 12.4))]


@icon("tamarind", CAT, "Curved lumpy tamarind pod with a stalk and a cracked end",
      tags=["pod", "tamarindo", "sour", "legume", "tropical", "produce"])
def _(S):
    centres = [(5.4, 15.6, 2.8), (9.4, 17.8, 3.1), (13.8, 17, 3), (17.8, 13.8, 3.1)]
    pod = union(*(circle(*c) for c in centres), thick("M5.4 15.6Q9.4 18.6 13.8 17T17.8 13.8", 3.8))
    crack = poly([(19.2, 9.4), (18.6, 11.6), (20.2, 12.6), (19.4, 14.6), (21.6, 15.4), (23, 11)], closed=True)
    return [shell(minus(pod, crack)), line("M3.2 13.6Q2.6 11.8 3.4 10.2")]


@icon("salak", CAT, "Teardrop shaped snake fruit with a scaly skin",
      tags=["snake fruit", "zalacca", "fruit", "tropical", "indonesia", "produce"])
def _(S):
    body = ("M12 2.8C14 5.6 19.4 9.8 19.4 14.4C19.4 18.4 16.2 20.8 12 20.8C7.8 20.8 4.6 18.4 4.6 14.4C4.6 9.8 10 5.6 12 2.8Z"
            if S.name == "line" else
            "M12.8 3.8C15 6.4 19.4 10.2 19.4 14.4C19.4 18.4 16.2 20.8 12 20.8C7.8 20.8 4.6 18.4 4.6 14.4"
            "C4.6 10.2 9 6.4 11.2 3.8Q12 2.8 12.8 3.8Z")
    scales = []
    for x, y in ((12, 9.2), (8.8, 13.4), (15.2, 13.4), (12, 17.4)):
        scales.append(detail(poly([(x - 2, y - 0.8), (x, y + 0.8), (x + 2, y - 0.8)], r=L(S, 0, 0.5))))
    return [shell(body), *scales, line("M12 20.8V22.4")]


@icon("prickly-pear", CAT, "Prickly pear fruit sitting on the rim of a flat cactus pad",
      tags=["cactus fruit", "tuna", "nopal", "opuntia", "desert", "produce"])
def _(S):
    fruit = rot(ellipse(15.8, 6.8, 3, 3.9), 22, 15.8, 6.8)
    pad = rot(ellipse(10.4, 15.2, 6.8, 5.8), -22, 10.4, 15.2)
    top = rot(poly([(14.2, 4.4), (15.8, 5.4), (17.4, 4.4)], r=S.r), 22, 15.8, 6.8)
    return [shell(cut(pad, fruit, g=L(S, 2.2, 2.6))), shell(fruit), detail(top),
            dot(8, 13.4, 0.9), dot(12.2, 12.8, 0.9), dot(9.4, 17.4, 0.9), dot(13.6, 16.8, 0.9)]


def _chord(cx, cy, r, c, kind, inset=0.6):
    """Chord of a circle along x + y = c ('/') or x - y = c ('\\'), shortened at both ends."""
    if kind == "/":
        v = (1 / math.sqrt(2), -1 / math.sqrt(2))
        p0 = ((c - cy + cx) / 2, (c + cy - cx) / 2)
    else:
        v = (1 / math.sqrt(2), 1 / math.sqrt(2))
        p0 = ((c + cx + cy) / 2, (cx + cy - c) / 2)
    dx, dy = p0[0] - cx, p0[1] - cy
    h = math.sqrt(max(0.0, r * r - (dx * dx + dy * dy)))
    return seg(p0[0] - (h - inset) * v[0], p0[1] - (h - inset) * v[1], p0[0] + (h - inset) * v[0], p0[1] + (h - inset) * v[1])


@icon("cantaloupe", CAT, "Round cantaloupe melon with a netted skin and a stem scar",
      tags=["muskmelon", "rockmelon", "melon", "fruit", "summer", "produce"])
def _(S):
    cx, cy, r = 12, 13, 8.4
    net = [detail(_chord(cx, cy, r, cx + cy + d, "/")) for d in (-5.4, 0, 5.4)]
    net += [detail(_chord(cx, cy, r, cx - cy + d, "\\")) for d in (-5.4, 0, 5.4)]
    return [shell(circle(cx, cy, r)), *net, line(poly([(12, 4.6), (12, 2.6), (13.4, 2)], r=S.r))]


@icon("wax-apple", CAT, "Bell shaped wax apple with a flared scalloped base and a glossy highlight",
      tags=["rose apple", "java apple", "jambu", "chomphu", "fruit", "produce"])
def _(S):
    bottom = ""
    xs = [19.8, 15.9, 12, 8.1, 4.2]
    for x in xs[1:]:
        bottom += f"A2 2 0 0 1 {fmt(x)} 18.6"
    d = ("M12 4.6C14.2 4.6 15 6.2 15.3 8.2C15.8 11.8 19.2 13.6 19.8 18.6" + bottom +
         "C4.8 13.6 8.2 11.8 8.7 8.2C9 6.2 9.8 4.6 12 4.6Z")
    return [shell(d), line(poly([(12, 4.8), (12, 2.8), (13.2, 2)], r=S.r)), detail("M10.2 9.6Q9.6 12.4 7.8 14.4")]


# =========================================================================== unusual fruit and citrus


@icon("rose-hip", CAT, "Oval rose hip with dried spiky sepals at the tip and a thin stem",
      tags=["rosehip", "rose haw", "berry", "wild rose", "herbal tea", "produce"])
def _(S):
    return [shell(ellipse(12, 12.8, 4.8, 6)), line("M12 18.8C12 19.9 12.4 20.9 13.2 21.8"),
            line("M12 6.8C10.6 5.6 9 5.4 7.4 5.8"), line("M12 6.8C11.4 5 11.6 3.4 12.6 2.2"), line("M12 6.8C13.6 5.8 15.2 5.8 16.6 6.8")]


@icon("tomatillo", CAT, "Tomatillo sitting in its papery husk peeled back into petals",
      tags=["husk tomato", "tomate verde", "salsa verde", "mexican", "vegetable", "produce"])
def _(S):
    fruit = circle(12, 10.4, 5)
    petals = union(leaf(12, 12, 3.2, 17.4, 2.2), leaf(12, 12, 7.4, 21.4, 2.2), leaf(12, 12, 16.6, 21.4, 2.2),
                   leaf(12, 12, 20.8, 17.4, 2.2))
    return [shell(cut(petals, fruit, g=2.2)), shell(fruit), line(poly([(12, 5.4), (12, 2.8), (13.4, 2)], r=S.r))]


@icon("pomelo", CAT, "Large pear shaped pomelo with a pointed top, a thick peel and a leaf",
      tags=["pummelo", "shaddock", "citrus", "chinese grapefruit", "fruit", "produce"])
def _(S):
    body = ("M12 4.8C10.4 5.4 9.2 6.6 8.4 8.4C6.4 9.4 3.4 11.6 3.4 15.4C3.4 19.2 7.2 21.6 12 21.6"
            "C16.8 21.6 20.6 19.2 20.6 15.4C20.6 11.6 17.6 9.4 15.6 8.4C14.8 6.6 13.6 5.4 12 4.8Z")
    return [shell(body), detail("M17.8 14.2C18.2 16.8 16.8 18.6 14.2 19.2"), shell(leaf(12.4, 4.6, 18.6, 2.6, 1.3)),
            line(seg(12, 5, 11.4, 2.4))]


@icon("kumquat", CAT, "Two small oval kumquats on a twig with a pair of pointed leaves",
      tags=["cumquat", "citrus", "chinese new year", "fruit", "small orange", "produce"])
def _(S):
    f1 = rot(ellipse(7.8, 16.4, 3.4, 4.3), 10, 7.8, 16.4)
    f2 = rot(ellipse(16.4, 16.6, 3.4, 4.3), -10, 16.4, 16.6)
    return [line("M12 2.4V8.6"), line("M12 8.6C10 9.2 8.8 10.4 8.4 12.1"), line("M12 8.6C14 9.2 15.4 10.4 15.8 12.3"),
            shell(leaf(11.4, 6.2, 3.2, 3.8, 1.6)), shell(leaf(12.6, 6.2, 20.8, 3.8, 1.6)), shell(f1), shell(f2)]


@icon("grapefruit-half", CAT, "Grapefruit half seen from above with its segments and a spoon beside it",
      tags=["grapefruit", "breakfast", "citrus", "diet", "halved", "produce"])
def _(S):
    cx, cy, r = 8.6, 13.4, 6.6
    spokes = []
    for k in range(6):
        a = math.radians(-90 + k * 60)
        spokes.append(detail(seg(cx + 1.2 * math.cos(a), cy + 1.2 * math.sin(a), cx + 3.8 * math.cos(a), cy + 3.8 * math.sin(a))))
    return [shell(circle(cx, cy, r)), *spokes, shell(ellipse(19.9, 6.6, 1.9, 3)), line(seg(19.9, 9.6, 19.9, 21.4))]


RASP = [(7.4, 9.2), (10.2, 8.4), (13.8, 8.4), (16.6, 9.2), (7.6, 12.6), (10.6, 12), (13.4, 12), (16.4, 12.6),
        (9, 16), (12, 15.6), (15, 16), (10.4, 19.2), (13.6, 19.2)]


@icon("raspberry", CAT, "Raspberry made of small bead drupelets with a hollow top",
      tags=["berry", "rasp", "fruit", "summer fruit", "red berry", "produce"])
def _(S):
    body = beads(RASP, 2.3)
    return [shell(body), detail(ellipse(12, 8.8, 3, 1.3) if S.name == "line" else rect(9, 7.5, 6, 2.6, 1.3)),
            *(dot(x, y, 0.75) for x, y in ((9.2, 12.8), (12, 12.4), (14.8, 12.8), (10.6, 16.4), (13.4, 16.4), (12, 19.4)))]


BLACK = [(9.8, 10.2), (14.2, 10.2), (7.6, 13.6), (12, 13.6), (16.4, 13.6), (9.8, 17), (14.2, 17), (12, 20)]


@icon("blackberry", CAT, "Oval blackberry of shiny drupelets with a leafy calyx and a stem",
      tags=["bramble", "berry", "dewberry", "fruit", "blackberries", "produce"])
def _(S):
    calyx = poly([(8.6, 7.6), (8.8, 4.8), (10.6, 6), (12, 4), (13.4, 6), (15.2, 4.8), (15.4, 7.6)], closed=True, r=L(S, 0, 0.5))
    body = beads(BLACK, 2.3)
    return [shell(cut(body, calyx, g=2.2)), shell(calyx), line(seg(12, 4.2, 12, 1.8)),
            *(dot(x, y, 0.75) for x, y in ((7.6, 13.6), (12, 13.6), (16.4, 13.6), (12, 20)))]


@icon("mulberry", CAT, "Long narrow mulberry of tiny bead clusters on a thin stem",
      tags=["berry", "mulberries", "fruit", "morus", "silkworm tree", "produce"])
def _(S):
    pts = [(10.8, 9.4), (13.2, 10.6), (10.8, 11.8), (13.2, 13), (10.8, 14.2), (13.2, 15.4), (10.8, 16.6), (12.4, 18.4)]
    body = rot(beads(pts, 2), 28, 12, 14)
    st = rot("M12 7.8C12 5.4 13 3.6 15 2.4", 28, 12, 14)
    return [shell(body), line(st), *(dot(x, y, 0.7) for x, y in rpts([(12, 11.2), (12, 13.6), (12, 16)], 28, 12, 14))]


@icon("gooseberry", CAT, "Round gooseberry with vein stripes, a stem on top and a tuft below",
      tags=["berry", "goose berry", "fruit", "green berry", "ribes", "produce"])
def _(S):
    return [shell(circle(12, 12.4, 7)), detail(seg(12, 5.8, 12, 19)), detail("M8.8 6.6C6.8 9.8 6.8 15 8.8 18.2"),
            detail("M15.2 6.6C17.2 9.8 17.2 15 15.2 18.2"), line(seg(12, 5.4, 12.6, 2.4)),
            line("M10.6 21.8L12 19.6L13.4 21.8" if S.name == "line" else "M10.6 21.8Q12 19.6 13.4 21.8")]


@icon("currants", CAT, "String of small round currants hanging from a drooping stem with a leaf",
      tags=["redcurrant", "blackcurrant", "berries", "ribes", "fruit", "produce"])
def _(S):
    berries = [(8.4, 9.4, 2.4), (11.6, 12.8, 2.4), (13.2, 17.2, 2.4), (17.6, 15.8, 2.2), (9.8, 17.6, 2.2)]
    out = [line("M3.4 3.4C5.4 4.6 7 6.2 8.1 7")]
    for i, (x, y, r) in enumerate(berries):
        front = [circle(*b) for b in berries[i + 1:]]
        out.append(shell(cut(circle(x, y, r), *front, g=0.001) if front else circle(x, y, r)))
    return out + [shell(leaf(4.4, 4.6, 5.4, 10.8, 1.4))]


@icon("elderberry", CAT, "Hanging umbrella shaped cluster of tiny elderberries on thin stalks",
      tags=["elder", "sambucus", "berries", "elderflower", "syrup", "produce"])
def _(S):
    hub = (12, 8)
    tips = [pt_(hub[0], hub[1], 11, a) for a in (140, 115, 90, 65, 40)]
    out = [line(poly([(12, 8), (12, 3.6), (13.4, 2)], r=S.r))]
    for x, y in tips:
        out.append(line(seg(hub[0], hub[1], x + (hub[0] - x) * 0.19, y + (hub[1] - y) * 0.19)))
        out.append(shell(circle(x, y, 1.7)))
    return out


# =========================================================================== berries on the branch, groups


@icon("sea-buckthorn", CAT, "Branch densely packed with small oval sea buckthorn berries and narrow leaves",
      tags=["buckthorn", "seaberry", "sandthorn", "berries", "superfood", "produce"])
def _(S):
    out = [line("M3.6 21.4L15.6 7.4")]
    for t, side in ((0.12, 1), (0.28, -1), (0.42, 1), (0.58, -1), (0.72, 1)):
        x, y = 3.6 + 12 * t, 21.4 - 14 * t
        nx, ny = 0.76 * side, 0.65 * side
        out.append(dot(x + nx * 2.4, y + ny * 2.4, 1.5))
    out += [shell(leaf(15.6, 7.4, 20.8, 2.4, 0.9)), shell(leaf(15, 8.2, 21.4, 9, 0.8)), shell(leaf(14.4, 8.4, 12.6, 2.4, 0.8))]
    return out


@icon("banana-flower", CAT, "Teardrop shaped banana flower bud of overlapping bracts on a curved stalk",
      tags=["banana blossom", "banana heart", "plantain flower", "vegetable", "vegan fish", "produce"])
def _(S):
    bud = "M13 7.2C9.8 7.2 7.8 10 7.8 13.4C7.8 17 10.4 20.2 13 21.8C15.6 20.2 18.2 17 18.2 13.4C18.2 10 16.2 7.2 13 7.2Z"
    return [shell(bud if S.name == "line" else bud.replace("C10.4 20.2 13 21.8", "C10.4 20.2 12.2 21.4")),
            line("M13 7.2C12.6 4.6 10.4 2.8 6.6 2.6C5 2.5 3.8 3 3 3.8"),
            detail(poly([(8.2, 12), (13, 14.8), (17.8, 12)], r=L(S, 0, 1.2))), detail(poly([(9.4, 16.4), (13, 18.8), (16.6, 16.4)], r=L(S, 0, 1.2)))]


@icon("mixed-berries", CAT, "A strawberry, a raspberry and two blueberries grouped together",
      tags=["berries", "berry mix", "summer fruit", "smoothie", "fruit", "produce"])
def _(S):
    straw = "M7.4 20.8C4.8 19.4 2.8 15.8 2.8 13C2.8 11.4 3.8 10.6 5.4 10.6H9.4C11 10.6 12 11.4 12 13C12 15.8 10 19.4 7.4 20.8Z"
    crown = poly([(4.6, 10.6), (5.2, 7.8), (7.4, 9.2), (9.6, 7.8), (10.2, 10.6)], closed=True, r=L(S, 0, 0.5))
    rasp = beads([(15.6, 4.6), (18.8, 4.6), (14.2, 7.4), (17.2, 7.4), (20.2, 7.4), (15.6, 10.2), (18.8, 10.2)], 1.7)
    b1, b2 = circle(15.8, 18.6, 2.6), circle(20, 16.4, 2.1)
    return [shell(cut(straw, crown, g=0.001)), shell(crown), dot(5.8, 14, 0.8), dot(8.4, 16.6, 0.8),
            shell(rasp), shell(b1), shell(cut(b2, b1, g=0.001))]


def lemon(cx, cy, s, deg):
    d = ("M-6.5 0L-5.3 -1.2C-4.4 -3.4 -2.4 -4.2 0 -4.2C2.4 -4.2 4.4 -3.4 5.3 -1.2L6.5 0L5.3 1.2"
         "C4.4 3.4 2.4 4.2 0 4.2C-2.4 4.2 -4.4 3.4 -5.3 1.2Z")
    p = transform_path(P(d), (s, 0, 0, s, cx, cy))
    return rot(path_to_d(p), deg, cx, cy)


@icon("citrus-fruits", CAT, "A whole orange, a lemon and a lime slice grouped together",
      tags=["citrus", "oranges and lemons", "vitamin c", "fruit", "zest", "produce"])
def _(S):
    orange = circle(9.2, 8.8, 6)
    lem = lemon(15.4, 14.8, 0.95, -40)
    lime = circle(6.6, 17.2, 4.2)
    spokes = [detail(seg(6.6 + 0.9 * math.cos(a), 17.2 + 0.9 * math.sin(a), 6.6 + 2.6 * math.cos(a), 17.2 + 2.6 * math.sin(a)))
              for a in (math.radians(-90 + k * 60) for k in range(6))]
    return [shell(cut(orange, lem, lime)), shell(lem), shell(cut(lime, lem, g=0.001)), *spokes]


@icon("fruit-and-vegetables", CAT, "An apple and a carrot crossed together",
      tags=["fruit and veg", "greengrocer", "healthy eating", "5 a day", "grocery", "produce"])
def _(S):
    apple = ("M8.4 10.2C7.4 9.6 6.4 9.4 5.4 9.4C3.4 9.4 2.2 11 2.2 13.4C2.2 16.6 4.2 19.8 6.4 19.8"
             "C7.4 19.8 7.6 19.4 8.4 19.4C9.2 19.4 9.4 19.8 10.4 19.8C12.6 19.8 14.6 16.6 14.6 13.4"
             "C14.6 11 13.4 9.4 11.4 9.4C10.4 9.4 9.4 9.6 8.4 10.2Z")
    cx, cy, a = 15, 12.6, 28
    carrot = rot(poly([(12.4, 5.2), (17.6, 5.2), (15, 21.8)], closed=True, r=L(S, 0.4, 1.6)), a, cx, cy)
    tops = [line(rot(seg(x1, 5, x2, 1.8), a, cx, cy)) for x1, x2 in ((14, 12.6), (16, 17.4))]
    ridges = [detail(rot(seg(13.9, y, 15.8, y), a, cx, cy)) for y in (10, 14.4)]
    return [shell(cut(apple, carrot)), line("M8.4 10.2C8.4 8.6 8 7.4 7.2 6.6"), shell(carrot), *tops, *ridges]


# =========================================================================== cut fruit

@icon("apple-core", CAT, "Eaten apple core with a narrow bitten middle, a stem and seeds",
      tags=["core", "leftover", "compost", "food waste", "apple", "produce"])
def _(S):
    top = "M12 5.6C14.6 4.8 17.8 5.2 18 7.8C18.1 9 17.2 9.6 16.2 9.8"
    bite_r = "C15.2 10.4 14.6 12 14.6 13.4C14.6 14.8 15.2 16.2 16.2 16.8"
    bot = ("C17.4 17.2 18.2 17.8 18 19.2C17.6 21 14.6 21.4 12 21C9.4 21.4 6.4 21 6 19.2C5.8 17.8 6.6 17.2 7.8 16.8")
    bite_l = "C8.8 16.2 9.4 14.8 9.4 13.4C9.4 12 8.8 10.4 7.8 9.8"
    rest = "C6.8 9.6 5.9 9 6 7.8C6.2 5.2 9.4 4.8 12 5.6Z"
    if S.name == "rounded":  # softer bite edges
        top = "M12 5.6C14.6 4.8 17.8 5.2 18 7.8C18.1 9.4 16.6 9.6 15.8 10.2"
        bite_r = "C14.8 11 14.6 12.2 14.6 13.4C14.6 14.6 14.8 15.8 15.8 16.4"
        bot = "C16.8 17 18.2 17.6 18 19.2C17.6 21 14.6 21.4 12 21C9.4 21.4 6.4 21 6 19.2C5.8 17.6 7.2 17 8.2 16.4"
        bite_l = "C9.2 15.8 9.4 14.6 9.4 13.4C9.4 12.2 9.2 11 8.2 10.2"
        rest = "C7.4 9.6 5.9 9.4 6 7.8C6.2 5.2 9.4 4.8 12 5.6Z"
    return [shell(top + bite_r + bot + bite_l + rest), line(seg(12, 5.4, 12.6, 2.4)), dot(12, 12, 0.85), dot(12, 14.8, 0.85)]


APPLE_OUT = ("M12 8.6C10.8 7.6 9.4 7.2 8 7.2C5 7.2 3.4 9.8 3.4 13.2C3.4 17.4 6.4 21 9.4 21C10.6 21 11 20.6 12 20.6"
             "C13 20.6 13.4 21 14.6 21C17.6 21 20.6 17.4 20.6 13.2C20.6 9.8 19 7.2 16 7.2C14.6 7.2 13.2 7.6 12 8.6Z")


@icon("apple-half", CAT, "Apple cut across the middle showing a star of seed chambers",
      tags=["apple", "cut apple", "cross section", "seeds", "star", "produce"])
def _(S):
    star = [pt_(12, 14.2, 3.6 if i % 2 == 0 else 1.6, -90 + i * 36) for i in range(10)]
    return [shell(APPLE_OUT), detail(poly(star, closed=True, r=L(S, 0, 0.4))), line("M12 8.6C12 6.6 12.4 5 13.4 3.6")]


@icon("pear-half", CAT, "Pear cut lengthwise showing the core and seeds",
      tags=["pear", "cut pear", "halved", "core", "seeds", "produce"])
def _(S):
    body = ("M12 4.6C9.8 4.6 8.8 6.4 8.5 8.6C8.2 10.8 4.8 12.4 4.8 16C4.8 19.4 8 21.4 12 21.4C16 21.4 19.2 19.4 19.2 16"
            "C19.2 12.4 15.8 10.8 15.5 8.6C15.2 6.4 14.2 4.6 12 4.6Z")
    core = "M12 9.4C11 11 9.6 12.8 9.6 15.2C9.6 17 10.6 18 12 18C13.4 18 14.4 17 14.4 15.2C14.4 12.8 13 11 12 9.4Z"
    return [shell(body), detail(core), line(seg(12, 4.8, 12.6, 1.8)), dot(12, 13.8, 0.8), dot(12, 16.2, 0.8)]


@icon("peach-half", CAT, "Peach cut in half showing its wrinkled stone",
      tags=["peach", "stone fruit", "pit", "halved", "nectarine", "produce"])
def _(S):
    body = "M12 6.6C10 5.2 4 5.8 4 12.8C4 17.8 7.6 21 12 21C16.4 21 20 17.8 20 12.8C20 5.8 14 5.2 12 6.6Z"
    stone = ("M12 9.4C10.2 9.4 8.8 11.2 8.8 13.8C8.8 16.2 10.2 17.8 12 17.8C13.8 17.8 15.2 16.2 15.2 13.8"
             "C15.2 11.2 13.8 9.4 12 9.4Z")
    return [shell(body), detail(stone), detail(poly([(12, 11.4), (11, 12.8), (12.8, 13.8), (11.2, 15.2), (12, 16.2)], r=L(S, 0, 0.5)))]


@icon("strawberry-half", CAT, "Strawberry cut lengthwise with a pale core and a leafy cap",
      tags=["strawberry", "cut strawberry", "halved", "berry", "dessert", "produce"])
def _(S):
    body = "M12 21.6C8.4 20.4 5 16 5 12C5 9.8 6.6 8.6 8.6 8.8L12 9.2L15.4 8.8C17.4 8.6 19 9.8 19 12C19 16 15.6 20.4 12 21.6Z"
    cap = poly([(6.6, 9.6), (6.4, 5.4), (9.6, 7), (12, 3), (14.4, 7), (17.6, 5.4), (17.4, 9.6)], closed=True, r=L(S, 0, 0.6))
    core = "M12 11.6C10.6 11.6 9.4 12.8 9.4 14.4C9.4 16.2 10.8 17.8 12 18.8C13.2 17.8 14.6 16.2 14.6 14.4C14.6 12.8 13.4 11.6 12 11.6Z"
    return [shell(cut(body, cap, g=0.001)), shell(cap), detail(core)]


def _banana(stem=(4.4, 18.6)):
    """Upward curving banana with its stem end at the bottom left (before rotation)."""
    return ("M4.2 17.2C9.6 17.4 15.8 14.2 18.8 5.8C19.1 5 20.4 4.9 20.6 5.8C21.6 12.4 16.4 20 6.2 20.6"
            "C5 20.6 4.4 20.2 4.2 19.4Z")


def _bunch():
    b = path_to_d(transform_path(P(_banana()), (0.88, 0, 0, 0.88, 4.4 * 0.12 + 0.8, 18.8 * 0.12 + 0.2)))
    back, mid, front = (rot(b, a, 5.2, 19) for a in (-23, -6, 11))
    stem = rect(2.6, 17.2, 3.6, 4.2, 0.4)
    return back, mid, front, stem


@icon("banana-bunch", CAT, "Three curved bananas joined at one shared stem",
      tags=["bananas", "bunch", "hand of bananas", "fruit", "potassium", "produce"],
      filled=lambda: layered(_bunch()))
def _(S):
    back, mid, front, stem = _bunch()
    if S.name == "rounded":
        stem = rect(2.6, 17.2, 3.6, 4.2, 1.4)
    return [shell(cut(back, mid, front, stem, g=0.001)), shell(cut(mid, front, stem, g=0.001)), shell(cut(front, stem, g=0.001)),
            shell(stem)]


@icon("banana-peeled", CAT, "Banana with its peel split into flaps hanging down and the fruit showing on top",
      tags=["peeled banana", "banana", "snack", "fruit", "open", "produce"])
def _(S):
    flesh = "M9.8 12.4C9.8 8.6 10.6 5.4 12.6 3.2C13.6 2.4 14.8 3 14.6 4.2C14.2 6.8 14.2 9.6 14.2 12.4Z"
    peel = union("M9.2 11V19.6C9.2 20.6 10 21.2 11 21.2H12.8C13.8 21.2 14.6 20.6 14.6 19.6V11Z",
                 leaf(9.8, 11, 3.6, 16.6, 1.6), leaf(14, 11, 20.2, 14.8, 1.6))
    return [shell(cut(flesh, peel, g=0.001)), shell(peel), detail("M11.9 14.4V19")]


@icon("overripe-banana", CAT, "Single curved banana covered in dark ripe spots",
      tags=["ripe banana", "brown banana", "spotty", "banana bread", "food waste", "produce"])
def _(S):
    d = ("M5.6 8.6C6.8 13.2 9.8 15.2 14 15.2C16.6 15.2 18.6 14.4 20.2 12.8C21 12 21.8 12.6 21.4 13.6"
         "C20 17.8 16.6 20.2 12.4 20.2C7.4 20.2 3.8 16.4 3.2 9.6C3.1 8.4 5.2 7.6 5.6 8.6Z")
    return [shell(d), line(poly([(4.4, 8.4), (3.4, 5.4), (4.8, 4.8)], r=S.r)),
            dot(7.6, 15, 0.9), dot(11.4, 17.6, 0.9), dot(15.6, 17.8, 0.9), dot(18.8, 16, 0.8)]


# =========================================================================== nuts and stones

@icon("fruit-pit", CAT, "Oval fruit stone with a furrowed surface and a seam along one side",
      tags=["pit", "stone", "peach pit", "seed", "kernel", "produce"])
def _(S):
    d = ("M12 3.4C9 5.6 6.2 9 6.2 13.4C6.2 17.8 8.8 20.8 12 20.8C15.2 20.8 17.8 17.8 17.8 13.4C17.8 9 15 5.6 12 3.4Z"
         if S.name == "line" else
         "M12.9 4.2C15.6 6.6 17.8 9.6 17.8 13.4C17.8 17.8 15.2 20.8 12 20.8C8.8 20.8 6.2 17.8 6.2 13.4C6.2 9.6 8.4 6.6 11.1 4.2Q12 3.4 12.9 4.2Z")
    return [shell(d), detail("M12.4 5.2C14.6 8.4 15 13.2 13.6 19.2"), detail("M9 9.6Q10.4 10.8 9.6 12.6"),
            detail("M8.8 14.6Q10.4 15.6 9.8 17.6")]


@icon("wormy-apple", CAT, "Apple with a worm poking its head out of a hole in its side",
      tags=["worm", "rotten apple", "bug", "pest", "organic", "produce"])
def _(S):
    worm = thick("M13.6 14.6C16.4 14.8 18.8 12.8 19.4 9.8", 4.4)
    body = cut(APPLE_OUT.replace("C17.6 21 20.6 17.4 20.6 13.2", "C17.6 21 20.6 17.4 20.6 13.2"), worm, g=2.3)
    return [shell(body), shell(worm), line("M12 8.6C12 6.6 12.4 5 13.4 3.6"), dot(19.2, 9.4, 0.8)]


@icon("walnut", CAT, "Round walnut shell with a centre seam and wrinkled halves",
      tags=["nut", "walnuts", "shell", "brain food", "baking", "produce"])
def _(S):
    body = smooth([(12, 3.2), (16.4, 5.2), (19, 9.6), (19, 14.6), (16.4, 19.2), (12, 21), (7.6, 19.2), (5, 14.6),
                   (5, 9.6), (7.6, 5.2)])
    tipd = poly([(11, 4.2), (12, 2.4), (13, 4.2)], r=L(S, 0, 0.5))
    return [shell(body), detail(seg(12, 4.4, 12, 19.8)), line(tipd),
            detail("M9 7.6Q7.4 9.6 9 11.6Q10.4 13.4 8.8 15.6Q8 16.8 8.8 18"),
            detail("M15 7.6Q16.6 9.6 15 11.6Q13.6 13.4 15.2 15.6Q16 16.8 15.2 18")]


ALMOND = "M12 3C9.6 6 7.4 10 7.4 14C7.4 18.2 9.4 21 12 21C14.6 21 16.6 18.2 16.6 14C16.6 10 14.4 6 12 3Z"
ALMOND_R = "M12.8 3.9C15 6.8 16.6 10.4 16.6 14C16.6 18.2 14.6 21 12 21C9.4 21 7.4 18.2 7.4 14C7.4 10.4 9 6.8 11.2 3.9Q12 3 12.8 3.9Z"


@icon("almond", CAT, "Flat teardrop shaped almond with a pointed tip and long grooves",
      tags=["nut", "almonds", "marzipan", "almond milk", "snack", "produce"])
def _(S):
    return [shell(rot(L(S, ALMOND, ALMOND_R), 32, 12, 12)), detail(rot("M10.6 9.4Q9.6 13.4 10.4 17.6", 32, 12, 12)),
            detail(rot("M13.4 9.4Q14.4 13.4 13.6 17.6", 32, 12, 12))]


@icon("cashew", CAT, "Curved kidney shaped cashew nut with a faint centre line",
      tags=["nut", "cashews", "cashew nut", "snack", "vegan", "produce"])
def _(S):
    body = thick(arc(12, 10.2, 5.4, 25, 205), 6.4)
    if S.name == "line":
        body = thick(arc(12, 10.2, 5.4, 25, 205), 6.4)
    return [shell(body), detail(arc(12, 10.2, 5.4, L(S, 70, 66), L(S, 160, 164)))]


def _pist(S=None):
    rounded = S is not None and S.name == "rounded"
    bowl = ("M4.4 12.8H19.6Q20.8 12.8 20.8 14C20.4 18.2 16.6 20.8 12 20.8C7.4 20.8 3.6 18.2 3.2 14Q3.2 12.8 4.4 12.8Z"
            if rounded else "M3.2 12.8H20.8C20.8 17.8 16.8 20.8 12 20.8C7.2 20.8 3.2 17.8 3.2 12.8Z")
    nut = ellipse(12.6, 11.8, 5.2, 3.2)
    lid = ("M4.4 11.2H19.6Q20.8 11.2 20.6 10C20 7.4 16.4 5.8 12 5.8C7.6 5.8 4 7.4 3.4 10Q3.2 11.2 4.4 11.2Z"
           if rounded else "M3.2 11.2H20.8C20.8 8 16.8 5.8 12 5.8C7.2 5.8 3.2 8 3.2 11.2Z")
    return rot(lid, -24, 3.4, 12), nut, bowl


@icon("pistachio", CAT, "Pistachio shell split open with the nut showing between the halves",
      tags=["nut", "pistachios", "green nut", "snack", "shell", "produce"],
      filled=lambda: layered(_pist()))
def _(S):
    lid, nut, bowl = _pist(S)
    return [shell(cut(lid, nut, bowl, g=0.001)), shell(cut(nut, bowl, g=0.001)), shell(bowl)]


@icon("hazelnut", CAT, "Round hazelnut with a pointed tip sitting in a ragged leafy husk",
      tags=["nut", "filbert", "cobnut", "praline", "baking", "produce"])
def _(S):
    nut = "M12 2.8C13.6 4.6 18.4 7.4 18.4 12.6C18.4 16.4 15.6 19.4 12 19.4C8.4 19.4 5.6 16.4 5.6 12.6C5.6 7.4 10.4 4.6 12 2.8Z"
    husk = poly([(3.4, 10.6), (6.4, 13.6), (7.4, 10), (9.6, 13.8), (12, 11.6), (14.4, 13.8), (16.6, 10), (17.6, 13.6), (20.6, 10.6)],
                r=L(S, 0, 0.6)) + "C21 16.4 17.2 21.4 12 21.4C6.8 21.4 3 16.4 3.4 10.6Z"
    return [shell(cut(nut, husk, g=2.2)), shell(husk), detail("M12 15.4V19")]


@icon("chestnut", CAT, "Chestnut with a rounded top narrowing to a tassel point and a flat pale base",
      tags=["nut", "chestnuts", "roasted chestnuts", "marron", "autumn", "produce"])
def _(S):
    d = ("M12 4.2C15.4 6.6 19.8 10.4 19.8 15.2C19.8 17.8 18.6 19.8 16.4 20.6H7.6C5.4 19.8 4.2 17.8 4.2 15.2C4.2 10.4 8.6 6.6 12 4.2Z"
         if S.name == "line" else
         "M12 4.2C15.4 6.6 19.8 10.4 19.8 15.2C19.8 18 18.4 20.6 15.4 20.6H8.6C5.6 20.6 4.2 18 4.2 15.2C4.2 10.4 8.6 6.6 12 4.2Z")
    return [shell(d), line(poly([(12, 4.4), (12, 2.6), (13.2, 1.8)], r=S.r)), detail("M5.6 17.2C9.6 16.2 14.4 16.2 18.4 17.2")]


@icon("chestnut-burr", CAT, "Spiky chestnut burr split open with two glossy chestnuts inside",
      tags=["burr", "chestnut", "husk", "conker", "autumn", "produce"])
def _(S):
    pts = [(3.6, 12.6)]
    for i in range(1, 12):
        a = math.radians(i * 180 / 12)
        rr = 8.4 if i % 2 == 1 else 6.4
        pts.append((12 - rr * math.cos(a), 12.6 + rr * math.sin(a)))
    pts.append((20.4, 12.6))
    cup = poly(pts + [(17, 14.6), (12, 13), (7, 14.6)], closed=True, r=L(S, 0, 0.5))
    n1 = rot("M9 3.6C11.4 5.6 12.6 8 12.6 10.6C12.6 12.6 11 13.8 9 13.8C7 13.8 5.4 12.6 5.4 10.6C5.4 8 6.6 5.6 9 3.6Z", -14, 9, 9)
    n2 = rot("M15 3.6C17.4 5.6 18.6 8 18.6 10.6C18.6 12.6 17 13.8 15 13.8C13 13.8 11.4 12.6 11.4 10.6C11.4 8 12.6 5.6 15 3.6Z", 14, 15, 9)
    return [shell(cut(cup, n1, n2, g=2.2)), shell(cut(n1, n2, g=0.001)), shell(n2), detail(n2)]


@icon("pecan", CAT, "Elongated pecan pointed at both ends with dark stripe markings",
      tags=["nut", "pecans", "pecan pie", "baking", "snack", "produce"])
def _(S):
    d = ("M3.2 12C5 8.2 8.4 6.6 12 6.6C15.6 6.6 19 8.2 20.8 12C19 15.8 15.6 17.4 12 17.4C8.4 17.4 5 15.8 3.2 12Z"
         if S.name == "line" else
         "M4.2 11C6.2 8 9 6.6 12 6.6C15 6.6 17.8 8 19.8 11Q20.4 12 19.8 13C17.8 16 15 17.4 12 17.4C9 17.4 6.2 16 4.2 13Q3.6 12 4.2 11Z")
    return [shell(rot(d, -32)), detail(rot("M7 10.4C9.4 9.6 11.2 10.8 13.4 10.2", -32)),
            detail(rot("M10.8 14C13 13.4 14.6 14.4 17 13.6", -32))]


@icon("brazil-nut", CAT, "Triangular wedge shaped brazil nut with curved sides and a rough shell",
      tags=["nut", "brazil nuts", "selenium", "paranut", "snack", "produce"])
def _(S):
    r = L(S, 0, 1.4)
    a, b, c = (4.6, 19.6), (20.4, 15.4), (8.4, 3.4)
    d = ("M" + _p((6.2, 20)) + "C10.4 20.8 16.4 18.6 19 16.2" + tip((19, 16.2), b, (18.4, 13.8), r) + "L18.4 13.8"
         "C15.4 10.6 11.8 7.6 9.4 4.8" + tip((9.4, 4.8), c, (7.8, 5), r) + "L7.8 5C5.6 9 4.6 14.2 4.8 18.2"
         + tip((4.8, 18.2), a, (6.2, 20), r) + "Z")
    return [shell(d), detail("M8 8.6C8.4 11.6 9.6 14.6 12 17.6"), detail("M10.6 8C12.2 10.8 14.4 13.2 17 15")]


