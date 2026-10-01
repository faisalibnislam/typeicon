"""TypeIcon Core: sea life (batch 002).

Cephalopods, crustaceans, molluscs, echinoderms, cnidarians, corals, sponges, plankton and shore plants.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "sea-life"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12, cy=12):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def thick(d, w, S):
    return path_to_d(ST(d, w, S.cap, S.join))


def flip(d):
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def mark(d):
    return Part("dot", d)


def _p(p):
    return f"{fmt(p[0])} {fmt(p[1])}"


def tip(a, p, b, r):
    if r <= 0:
        return "L" + _p(p)
    la = math.hypot(a[0] - p[0], a[1] - p[1])
    lb = math.hypot(b[0] - p[0], b[1] - p[1])
    t = min(r, la / 2, lb / 2)
    s = (p[0] + (a[0] - p[0]) * t / la, p[1] + (a[1] - p[1]) * t / la)
    e = (p[0] + (b[0] - p[0]) * t / lb, p[1] + (b[1] - p[1]) * t / lb)
    return "L" + _p(s) + "Q" + _p(p) + " " + _p(e)


def pt(c, r, deg):
    return (c[0] + r * math.cos(math.radians(deg)), c[1] + r * math.sin(math.radians(deg)))


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def tube(ctrl, width, n=28):
    """Closed outline around a cubic centreline; width(t) in px."""
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x, y = bez(*ctrl, t)
        x2, y2 = bez(*ctrl, min(1, t + 1e-3))
        x1, y1 = bez(*ctrl, max(0, t - 1e-3))
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy)
        nx, ny = -dy / ln, dx / ln
        w = width(t) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return left + right[::-1]


def pt_rot(x, y, deg, cx, cy):
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return (cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c)


def cpt(ctrl, t):
    return bez(*ctrl, t)


def claw(cx, cy, r, deg, S, notch=0.9):
    """Pincer: disc with a wedge cut out, wedge opening toward angle deg."""
    a = pt((cx, cy), r * 1.6, deg - 22)
    b = pt((cx, cy), r * 1.6, deg + 22)
    wedge = poly([(cx, cy), a, b], closed=True)
    return minus(circle(cx, cy, r), wedge)


def scallops(x_from, x_to, y, n, depth, S):
    """Bottom edge going from x_from to x_to, n scallops (path fragment, continues from current point)."""
    d = ""
    w = (x_to - x_from) / n
    for i in range(n):
        xa = x_from + i * w
        if S.name == "line":
            d += f"L{fmt(xa + w / 2)} {fmt(y - depth)}L{fmt(xa + w)} {fmt(y)}"
        else:
            d += f"Q{fmt(xa + w / 2)} {fmt(y + depth)} {fmt(xa + w)} {fmt(y)}"
    return d


def whorls(x, y0, ws, lean=0.0, apex=0.5, step=0.8, slant=2.2):
    """Stepped spiral shell silhouette, apex at (x, y0); whorls are (y_end, half_width[, peak]).
    Returns (closed polygon points, suture segments [((xl, y), (xr, y))])."""
    right, left, sut = [], [], []
    yp, wp = y0, apex
    for i, item in enumerate(ws):
        y1, w1 = item[0], item[1]
        pk = item[2] if len(item) > 2 else 0.82
        ws0 = wp * step if i else apex
        for (u, w) in ((0, ws0), (pk, w1), (1, w1 * 0.92)):
            y = yp + (y1 - yp) * u
            off = lean * (y - y0)
            right.append((x + off + w, y))
            left.append((x + off - w, y))
        if i < len(ws) - 1:
            off = lean * (y1 - y0)
            ww = w1 * 0.92
            sut.append(((x + off - ww, y1 + slant), (x + off + ww, y1 - slant)))
        yp, wp = y1, w1 * 0.92
    pts = [(x, y0)] + right + left[::-1]
    return pts, sut


def star_pts(c, n, R, rho, S, flat=5.0, start=-90.0):
    """Star outline with n arms; arm tips are flat in Line (no miter spike) and rounded by poly r in Rounded."""
    pts = []
    for i in range(n):
        a = start + i * 360 / n
        if S.name == "line":
            pts += [pt(c, R, a - flat), pt(c, R, a + flat)]
        else:
            pts.append(pt(c, R, a))
        pts.append(pt(c, rho, a + 180 / n))
    return pts


def scallop_circle(c, R, n, depth, S):
    """Circle outline with n scallops (Rounded) or n teeth (Line)."""
    if S.name == "line":
        pts = []
        for i in range(n):
            a = -90 + i * 360 / n
            pts.append(pt(c, R, a))
            pts.append(pt(c, R + depth, a + 180 / n))
        return poly(pts, closed=True)
    d = "M" + _p(pt(c, R, -90))
    for i in range(n):
        a1 = -90 + (i + 1) * 360 / n
        am = -90 + (i + 0.5) * 360 / n
        q = pt(c, R + depth * 2, am)
        e = pt(c, R, a1)
        d += "Q" + _p(q) + " " + _p(e)
    return d + "Z"


def wavy(x, y0, y1, amp, n, dirn=1):
    """Vertical wavy centreline from (x, y0) to (x, y1), n half waves."""
    d = f"M{fmt(x)} {fmt(y0)}"
    h = (y1 - y0) / n
    for i in range(n):
        ya = y0 + i * h
        sgn = dirn * (1 if i % 2 == 0 else -1)
        d += f"C{fmt(x + sgn * amp)} {fmt(ya + h * 0.3)} {fmt(x + sgn * amp)} {fmt(ya + h * 0.7)} {fmt(x)} {fmt(ya + h)}"
    return d


def water(x0, x1, y, a=1.2, waves=3):
    w = (x1 - x0) / waves
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(waves):
        xa = x0 + i * w
        d += (f"C{fmt(xa + w * 0.25)} {fmt(y - a)} {fmt(xa + w * 0.25)} {fmt(y - a)} {fmt(xa + w * 0.5)} {fmt(y)}"
              f"C{fmt(xa + w * 0.75)} {fmt(y + a)} {fmt(xa + w * 0.75)} {fmt(y + a)} {fmt(xa + w)} {fmt(y)}")
    return d


# --------------------------------------------------------------------------- cephalopods and crustaceans

@icon("blue-ringed-octopus", CAT, "Small octopus with ring shaped spots on its head and curling arms",
      tags=["venomous octopus", "octopus", "ringed", "ocean", "marine", "tide pool"])
def _(S):
    return [shell(ellipse(12, 9.5, 7, 6)), detail(circle(8.8, 7, 1.5)), detail(circle(15.2, 7, 1.5)),
            dot(9.5, 12, 1), dot(14.5, 12, 1),
            line("M7.5 14.5C7.5 17.5 5.5 19 3 18.5"), line("M10.7 15.5C10.7 18.5 9.5 20.5 7 21"),
            line("M16.5 14.5C16.5 17.5 18.5 19 21 18.5"), line("M13.3 15.5C13.3 18.5 14.5 20.5 17 21")]


@icon("vampire-squid", CAT, "Squid like animal with a webbed cloak spread over its arms and two fins on top",
      tags=["deep sea", "cephalopod", "cloak", "umbrella", "abyss", "marine"])
def _(S):
    fins = union(rot(ellipse(5, 8.5, 2.6, 1.6), -35, 5, 8.5), rot(ellipse(19, 8.5, 2.6, 1.6), 35, 19, 8.5))
    d = "M5.5 18.5C5.5 10.5 8 6.5 12 6.5C16 6.5 18.5 10.5 18.5 18.5" + scallops(18.5, 5.5, 18.5, 4, 1.6, S) + "Z"
    return [shell(union(fins, d)), dot(9.6, 11, 1.2), dot(14.4, 11, 1.2)]


@icon("squid-ink", CAT, "Squid jetting away from a billowing cloud of ink puffs",
      tags=["ink cloud", "cephalopod", "escape", "defence", "calamari", "ocean"])
def _(S):
    cloud = union(circle(5.5, 18, 3), circle(10, 19.2, 2.2), circle(4, 13, 2), circle(8.8, 14.5, 1.8))
    x, y = 15.5, 8.5
    mant = poly([(x, y - 6.5), (x + 4.5, y - 2.5), (x + 2.5, y - 2), (x + 2.5, y + 3), (x - 2.5, y + 3), (x - 2.5, y - 2), (x - 4.5, y - 2.5)],
                closed=True, r=L(S, 0, 1))
    return [shell(cloud), shell(rot(mant, 45, x, y)),
            line(rot(f"M{x - 1.2} {y + 3}V{y + 6.5}", 45, x, y)), line(rot(f"M{x + 1.2} {y + 3}V{y + 6.5}", 45, x, y)),
            dot(*pt_rot(x - 1, y - 0.5, 45, x, y), 0.9), dot(*pt_rot(x + 1, y - 0.5, 45, x, y), 0.9)]


@icon("octopus-tentacle", CAT, "Single curling arm in an S shape with round suckers along it",
      tags=["octopus arm", "suckers", "cephalopod", "tentacle", "ocean", "marine"])
def _(S):
    c = ((7, 21.5), (6.5, 12), (17.5, 14), (16, 3))
    t = poly(tube(c, lambda t: 6.5 - 4.8 * t), closed=True, r=0)
    ds = [dot(*cpt(c, tt), 1.1) for tt in (0.13, 0.34, 0.56)]
    return [shell(t), *ds]


@icon("lobster", CAT, "Top view of a lobster with two big claws, long feelers and a fan tail",
      tags=["crustacean", "seafood", "shellfish", "claws", "ocean", "boil"])
def _(S):
    car = ellipse(12, 10.5, 3, 4.8)
    tail = poly([(10, 14.5), (14, 14.5), (13.3, 19), (15.8, 21.8), (12, 20.4), (8.2, 21.8), (10.7, 19)], closed=True, r=L(S, 0, 0.8))
    return [shell(union(car, tail)), detail("M10.3 17H13.7"),
            shell(claw(4.8, 6.2, 3.1, -100, S)), shell(claw(19.2, 6.2, 3.1, -80, S)),
            line("M9.2 9.5L7 8.4"), line("M14.8 9.5L17 8.4"),
            line("M9.2 12.5L5.5 14"), line("M14.8 12.5L18.5 14"),
            line("M11 6L10 2"), line("M13 6L14 2")]


@icon("crayfish", CAT, "Side view of a freshwater lobster with slim claws held forward and a curled tail",
      tags=["crawfish", "crawdad", "freshwater", "crustacean", "claws", "bayou"])
def _(S):
    body = ellipse(11, 13.5, 5, 3.2)
    tail = poly(tube(((14.5, 13), (18, 12.5), (20.3, 14), (20.6, 17.2)), lambda t: 3.8 - 1.0 * t), closed=True)
    fan = poly([(18.6, 17), (22.4, 17), (21.8, 21.6), (20.5, 20.2), (19.2, 21.6)], closed=True, r=L(S, 0, 0.4))
    return [shell(union(body, tail, fan)), dot(8, 12.6, 1),
            line("M6.8 11.5L4.5 8"), shell(claw(4, 5.8, 2.7, -125, S)),
            line("M8 16.5V19.5"), line("M11 17V20"), line("M14 16.5V19.5")]


@icon("king-crab", CAT, "Top view of a crab with a spiny round shell, two claws and thick spiky legs",
      tags=["alaskan crab", "crustacean", "seafood", "spiny", "legs", "ocean"])
def _(S):
    c = (12, 13.5)
    pts = []
    for i in range(14):
        a = -90 + i * 360 / 14
        rr = 5.6 if i % 2 == 0 else 4.2
        pts.append((c[0] + 1.15 * rr * math.cos(math.radians(a)), c[1] + 0.95 * rr * math.sin(math.radians(a))))
    legs = []
    for sx in (1, -1):
        for (a, b, e) in (((7, 13), (3.5, 12.5), (2.5, 17)), ((8.5, 17), (6, 19), (5.5, 22))):
            pts2 = [(12 + sx * (12 - a[0]), a[1]), (12 + sx * (12 - b[0]), b[1]), (12 + sx * (12 - e[0]), e[1])]
            legs.append(line(poly(pts2, r=S.r)))
    return [shell(poly(pts, closed=True, r=L(S, 0, 0.5))), *legs,
            line("M8.5 9.5L6.5 7"), line("M15.5 9.5L17.5 7"),
            shell(claw(5.5, 5, 2.4, -100, S)), shell(claw(18.5, 5, 2.4, -80, S)), dot(10.5, 11, 0.9), dot(13.5, 11, 0.9)]


@icon("spider-crab", CAT, "Top view of a small crab body with tiny claws and extremely long thin jointed legs",
      tags=["japanese spider crab", "long legs", "crustacean", "deep sea", "arthropod", "ocean"])
def _(S):
    legs = []
    for sx in (1, -1):
        for (a, b, e) in (((9.5, 12), (3.5, 8.5), (2, 13.5)),
                          ((9.5, 13.5), (3.5, 15), (3, 21)), ((10.5, 15.2), (7.5, 19), (8, 22))):
            pts2 = [(12 + sx * (12 - a[0]), a[1]), (12 + sx * (12 - b[0]), b[1]), (12 + sx * (12 - e[0]), e[1])]
            legs.append(line(poly(pts2, r=S.r)))
    body = poly([(12, 7.5), (15.2, 12.5), (13.8, 16.5), (10.2, 16.5), (8.8, 12.5)], closed=True, r=L(S, 0, 1.2))
    return [shell(body), *legs, line("M10.5 9.5L8.5 5"), line("M13.5 9.5L15.5 5"),
            shell(circle(8.2, 4, 1.3)), shell(circle(15.8, 4, 1.3)), dot(10.8, 12.5, 0.9), dot(13.2, 12.5, 0.9)]


@icon("ghost-crab", CAT, "Front view of a square crab with tall eye stalks and one claw raised",
      tags=["sand crab", "beach crab", "crustacean", "eye stalks", "shore", "claw"])
def _(S):
    legs = [line("M17 15L20.5 14"), line("M17 17L21 19.5"), line("M7 17.5L3.5 19.5"), line("M7 15.5L4.5 15.5")]
    return [shell(rect(7, 12, 10, 7, S.R * 0.6)), line("M9.5 12V8"), line("M14.5 12V8"),
            shell(circle(9.5, 6.3, 1.7)), shell(circle(14.5, 6.3, 1.7)),
            *legs, line("M20 12L20.5 9.5"), shell(claw(20.5, 7.5, 2, -90, S))]


@icon("fiddler-crab", CAT, "Front view of a small crab with one giant raised claw and one tiny claw",
      tags=["claw", "mismatched claws", "crustacean", "mud flat", "beach", "ocean"])
def _(S):
    return [shell(ellipse(14, 16, 5.5, 3.2)), line("M10 14.5L7.5 11"), shell(claw(6, 7.5, 3.9, -80, S)),
            line("M19 14.8L20 13"), dot(20.4, 12, 1.1), line("M12.5 13V10.5"), line("M15.5 13V10.5"),
            dot(12.5, 9.8, 1), dot(15.5, 9.8, 1),
            line("M10 18L8 21"), line("M14 19.2V21.5"), line("M18 18L20 21")]


@icon("crab-claw", CAT, "Single crab pincer with an open jagged gripping tip",
      tags=["pincer", "nipper", "crustacean", "claw", "seafood", "grip"])
def _(S):
    r = L(S, 0, 0.5)
    a = tube(((6, 14), (7, 8), (12, 5), (20, 4.5)), lambda t: 6.5 - 5.2 * t)
    b = tube(((12, 16), (15, 14), (18, 12.5), (21, 12)), lambda t: 5.2 - 4.0 * t)
    return [shell(union(ellipse(8, 16, 5.5, 4.8), poly(a, closed=True), poly(b, closed=True))), detail("M12.5 8.5L14 10.5L15.8 8.2")]


@icon("krill", CAT, "Small curved shrimp like crustacean with a big eye and feathery legs",
      tags=["zooplankton", "crustacean", "whale food", "antarctic", "swarm", "ocean"])
def _(S):
    c = ((17, 9), (11, 9), (5, 10), (6.5, 18))
    t = poly(tube(c, lambda t: 5.6 - 3 * t), closed=True)
    head = circle(17, 9, 3.4)
    fan = poly([(4.8, 17.5), (8.6, 17.5), (9, 21.4), (6.7, 20), (4.4, 21.4)], closed=True, r=L(S, 0, 0.4))
    segs = []
    for tt in (0.35, 0.55):
        x, y = cpt(c, tt)
        x2, y2 = cpt(c, tt + 0.01)
        dx, dy = x2 - x, y2 - y
        ln = math.hypot(dx, dy)
        nx, ny = -dy / ln, dx / ln
        segs.append(detail(seg(x - nx * 2, y - ny * 2, x + nx * 2, y + ny * 2)))
    return [shell(union(head, t, fan)), dot(17.8, 8.2, 1.2), *segs, line("M19.8 6L22 4"), line("M20 8.5L22.2 8")]


@icon("barnacle", CAT, "Cluster of small cone shaped shells with slotted openings sitting on a rock",
      tags=["acorn barnacle", "crustacean", "shell cluster", "rock", "tide pool", "pier"])
def _(S):
    r = L(S, 0, 1)
    parts = []
    for (x0, x1, top) in ((2.5, 8.5, 11.5), (9.5, 15.5, 7), (16.5, 21.5, 12)):
        n = (x1 - x0) * 0.2
        parts.append(shell(poly([(x0, 18), (x0 + n, top), (x1 - n, top), (x1, 18)], closed=True, r=r)))
        parts.append(detail(seg((x0 + x1) / 2 - 0.8, top + 2.8, (x0 + x1) / 2 + 0.8, top + 2.8)))
    return [*parts, line("M2 21.5H22")]


@icon("pistol-shrimp", CAT, "Side view of a small shrimp with one oversized snapping claw and a burst mark at its tip",
      tags=["snapping shrimp", "alpheid", "claw", "crustacean", "sonic", "reef"])
def _(S):
    c = ((14.5, 10.5), (20, 11), (21, 17), (15.5, 19.5))
    body = poly(tube(c, lambda t: 5.2 - 2.4 * t), closed=True)
    fan = poly([(14, 18), (17, 17.8), (17.5, 22), (15.5, 20.8), (13.5, 22)], closed=True, r=L(S, 0, 0.4))
    return [shell(union(body, fan)), shell(claw(6.5, 15, 4.2, -115, S)), line("M10.4 13.6L12.2 12.6"), dot(15, 9.6, 0.9),
            line("M6.5 8V5.2"), line("M2.8 9.6L1.9 8.5"), line("M10.4 9.6L11.4 8.5")]


@icon("giant-isopod", CAT, "Top view of a large segmented oval crustacean with many small legs and two tail spines",
      tags=["deep sea", "pill bug", "woodlouse", "crustacean", "abyss", "segmented"])
def _(S):
    return [shell(ellipse(12, 11.5, 5.6, 8.3)), detail("M7 8.5Q12 10 17 8.5"), detail("M6.6 12.5Q12 14 17.4 12.5"),
            detail("M7.5 16.2Q12 17.4 16.5 16.2"), dot(10, 5.4, 0.9), dot(14, 5.4, 0.9),
            line("M6.4 9L3.5 8.2"), line("M6 12.2L3 12.6"), line("M6.7 15.5L4 17"),
            line("M17.6 9L20.5 8.2"), line("M18 12.2L21 12.6"), line("M17.3 15.5L20 17"),
            line("M10.5 19.4L10 22"), line("M13.5 19.4L14 22")]


@icon("lobster-trap", CAT, "Slatted dome cage trap with a rope leading up to a small float",
      tags=["lobster pot", "crab pot", "fishing", "cage", "buoy", "fisherman"])
def _(S):
    d = "M3 20.5V15.5C3 12 7 10.5 12 10.5C17 10.5 21 12 21 15.5V20.5Z"
    if S.name == "line":
        d = "M3 20.5V14L7 10.5H17L21 14V20.5Z"
    return [shell(d), detail("M9 11V20.5"), detail("M15 11V20.5"), detail("M3 16H21"),
            line("M12 6C10.5 7.5 13.5 8.8 12 10.5"), shell(circle(12, 4, 1.9))]


@icon("oyster", CAT, "Closed oyster shell with a rough craggy edge and layered ridges",
      tags=["bivalve", "shellfish", "seafood", "pearl", "raw bar", "mollusc"])
def _(S):
    pts = [(12, 2.8), (15.5, 4), (18.8, 6), (19.2, 9.5), (21.2, 13), (19, 17), (17, 19.4), (13.5, 21.2), (10, 20), (6.5, 21), (4.8, 17.5),
           (3, 14), (4.2, 9.5), (5.5, 6), (8.5, 4.2)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 1.6))), detail(arc(12, 17.5, 4.5, -160, -20)), detail(arc(12, 17.5, 9, -150, -30))]


@icon("mussel", CAT, "Side view of a long dark teardrop shaped shell with fine growth lines",
      tags=["blue mussel", "bivalve", "shellfish", "seafood", "mollusc", "moules"])
def _(S):
    d = "M4.5 20C3.5 12 9 4 16 4.5C21 5 21.5 12 17 16C13.5 19.5 8 21.5 4.5 20Z"
    if S.name == "line":
        d = "M3.5 20.5L6 8.5C9 4.5 13 3.5 16.5 4.5C21 6 21.5 12 17 16C13.5 19.5 8 21.5 3.5 20.5Z"
    return [shell(d), detail(arc(5, 20, 7.5, -80, -15)), detail(arc(5, 20, 12, -68, -28))]


@icon("cowrie", CAT, "Glossy egg shaped shell with a narrow toothed slit down the middle",
      tags=["cowry", "seashell", "money shell", "beach", "mollusc", "shell"])
def _(S):
    d = ellipse(12, 12, 9.5, 6.5) if S.name != "line" else "M2.5 12C6 4.5 18 4.5 21.5 12C18 19.5 6 19.5 2.5 12Z"
    return [shell(d), detail("M6.5 12H17.5"), detail("M9 10.2V13.8"), detail("M12 10V14"), detail("M15 10.2V13.8")]


@icon("abalone", CAT, "Ear shaped flat shell with a curved row of small breathing holes near one edge",
      tags=["paua", "ormer", "seashell", "mother of pearl", "mollusc", "sea ear"])
def _(S):
    pts = [(2.5, 13), (4.5, 8.2), (10, 4.8), (16.5, 5), (20.8, 8.8), (21.2, 14), (16.5, 18.8), (8.5, 19.2), (4, 17.5)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 3.5))), detail("M6.5 15.5C5.7 11.8 8.5 9.2 12 10"),
            dot(13, 8.2, 0.9), dot(16.2, 9.4, 0.9), dot(18, 12, 0.9), dot(17.6, 15, 0.9)]


@icon("limpet", CAT, "Low cone shaped shell stuck to a rock with ribs radiating from its peak",
      tags=["sea snail", "tide pool", "rock", "seashell", "mollusc", "conical shell"])
def _(S):
    cone = poly([(2.5, 18), (5, 12.5), (9.5, 7.5), (12, 6.5), (14.5, 7.5), (19, 12.5), (21.5, 18)], closed=True, r=L(S, 0, 2.5))
    return [shell(cone), detail("M12 10.5V18"), detail("M8.8 12.5L7.2 18"), detail("M15.2 12.5L16.8 18"), line("M2 21.5H22")]


@icon("razor-clam", CAT, "Long narrow straight shell with a foot poking out of one end",
      tags=["razor shell", "bivalve", "shellfish", "seafood", "mollusc", "beach"])
def _(S):
    shp = union(rect(8, 2.5, 8, 14.5, S.R * 0.6), "M10 16.5V18.5C8.6 19 8.6 22 12 22C15.4 22 15.4 19 14 18.5V16.5Z")
    return [shell(rot(shp, 20, 12, 12)), detail(rot("M12 5V14", 20, 12, 12))]


@icon("geoduck", CAT, "Large clam shell with a long thick siphon neck stretching up from it",
      tags=["gooey duck", "clam", "siphon", "bivalve", "pacific", "shellfish"])
def _(S):
    shp = ellipse(10.5, 17.8, 8.5, 4) if S.name != "line" else "M2 17.8C2 14.5 6.5 14 10.5 14C14.5 14 19 14.5 19 17.8C19 21 14.5 21.6 10.5 21.6C6.5 21.6 2 21 2 17.8Z"
    neck = poly(tube(((15, 16), (15, 11), (12, 8), (12.5, 3.5)), lambda t: 5.6 - 0.8 * t), closed=True)
    return [shell(union(shp, neck)), dot(12.6, 4.8, 1.1), detail("M5 18.5Q10.5 20.5 16 18.5")]


@icon("auger-shell", CAT, "Long thin sharply pointed spiral shell like a tall screw",
      tags=["terebra", "seashell", "turret shell", "spiral", "mollusc", "beach"])
def _(S):
    r = L(S, 0, 0.8)
    pts = [(12, 1.8), (16.5, 21), (7.5, 21)]
    ds = []
    for y in (8, 12.5, 17):
        half = 4.5 * (y - 1.8) / 19.2
        ds.append(detail(seg(12 - half, y + 1.2, 12 + half, y - 1.2)))
    return [shell(poly(pts, closed=True, r=r)), *ds]


@icon("cone-shell", CAT, "Cone shaped shell with a low spiral top and a patterned tapering body",
      tags=["cone snail", "seashell", "textile cone", "mollusc", "beach", "venomous snail"])
def _(S):
    r = L(S, 0, 1)
    top = ellipse(12, 6.2, 3.6, 1.8)
    body = "M4.5 9C4.5 7 7.5 6.5 12 6.5C16.5 6.5 19.5 7 19.5 9L14.5 21.5H9.5Z" if S.name != "line" else "M4.5 9L7 6.5H17L19.5 9L14.5 21.5H9.5Z"
    return [shell(union(top, body)), detail("M7.5 12.5H16.5"), detail("M9.3 16.8H14.7")]


@icon("sundial-shell", CAT, "Flat round spiral shell with beaded rings winding to a center",
      tags=["architectonica", "seashell", "spiral", "mollusc", "beach", "whorl"])
def _(S):
    pts = []
    for i in range(0, 61):
        th = i / 60 * 3.0 * math.pi
        rr = 0.6 + 5.4 * th / (3.0 * math.pi)
        pts.append((12 + rr * math.cos(th), 12 + rr * math.sin(th)))
    return [shell(circle(12, 12, 9)), detail(poly(pts, closed=False))]


@icon("tusk-shell", CAT, "Slim curved hollow tube shell tapering like a small elephant tusk",
      tags=["scaphopod", "dentalium", "seashell", "tooth shell", "mollusc", "beach"])
def _(S):
    c = ((5, 20.5), (4.5, 9), (12, 3), (20, 4))
    t = poly(tube(c, lambda t: 5.6 - 3.6 * t), closed=True, r=L(S, 0, 0.6))
    segs = []
    for tt in (0.4, 0.68):
        x, y = cpt(c, tt)
        x2, y2 = cpt(c, tt + 0.01)
        dx, dy = x2 - x, y2 - y
        ln = math.hypot(dx, dy)
        nx, ny = -dy / ln, dx / ln
        h = (5.6 - 3.6 * tt) / 2
        segs.append(detail(seg(x - nx * h, y - ny * h, x + nx * h, y + ny * h)))
    return [shell(t), *segs]


@icon("nudibranch", CAT, "Side view of a soft sea slug with two horn feelers on its head and a frilly gill tuft on its back",
      tags=["sea slug", "opisthobranch", "rhinophores", "gills", "tide pool", "colorful slug"])
def _(S):
    body = "M3 17C3 14 7 13 12 13C17 13 20 14.5 22.5 19.5C17 20.2 9 20.2 4.5 19.8C3.5 19.6 3 18.5 3 17Z"
    return [shell(body), line("M5.5 13.6L4.5 10"), line("M8.2 13.2L8.8 9.8"), dot(4.4, 9.2, 1.1), dot(8.9, 8.8, 1.1),
            line("M13 13C11.5 10.6 14 9.4 12.4 6.8"), line("M16.2 13.6C15 11.4 17.6 10.2 16.4 7.6")]


@icon("blue-dragon-sea-slug", CAT, "Top view of a small slug with a slim body and two pairs of fingered fronds spread out",
      tags=["glaucus atlanticus", "sea slug", "blue glaucus", "pelagic", "nudibranch", "ocean"])
def _(S):
    parts = [shell(ellipse(12, 12, 2.1, 8.8))]
    for y in (7, 16.5):
        for sx in (1, -1):
            x0 = 12 + sx * 1.8
            for dy in (-3, 0, 3):
                parts.append(line(f"M{fmt(x0)} {fmt(y)}L{fmt(12 + sx * 8.6)} {fmt(y + dy)}"))
    return parts


@icon("chiton", CAT, "Top view of an oval mollusc with overlapping plates across its back and a girdle rim",
      tags=["coat of mail shell", "polyplacophora", "armored mollusc", "intertidal", "rock", "plates"])
def _(S):
    return [shell(ellipse(12, 12, 9.5, 6)) if S.name != "line" else shell("M2.5 12C2.5 7 7 5.5 12 5.5C17 5.5 21.5 7 21.5 12C21.5 17 17 18.5 12 18.5C7 18.5 2.5 17 2.5 12Z"),
            detail("M8 6.4Q6.6 12 8 17.6"), detail("M12 5.8V18.2"), detail("M16 6.4Q17.4 12 16 17.6")]


@icon("sea-angel", CAT, "Tiny translucent swimming snail with two wing like flaps and a small head",
      tags=["clione", "sea butterfly", "pteropod", "planktonic", "arctic", "swimming snail"])
def _(S):
    r = L(S, 0, 0.8)
    wing = poly([(10.2, 11), (3, 5), (3.6, 13), (10.2, 15)], closed=True, r=r)
    return [shell(union(ellipse(12, 14.5, 2.6, 5.8), circle(12, 7.2, 2.3), wing, flip(wing))), dot(12, 7, 0.9)][:1] + [line("M11 5L10 2.5"), line("M13 5L14 2.5")]


@icon("starfish", CAT, "Five armed sea star with a small circle at the center and dotted texture on its arms",
      tags=["sea star", "echinoderm", "beach", "ocean", "tide pool", "marine"])
def _(S):
    c = (12, 12.8)
    pts = star_pts(c, 5, 9.6, 4.4, S, flat=6)
    ds = [dot(*pt(c, 6.6, -90 + k * 72), 0.8) for k in range(5)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 1.8))), dot(12, 12.8, 1.3), *ds]


@icon("sunflower-starfish", CAT, "Sea star with a wide central disc and many short arms radiating like petals",
      tags=["sea star", "sunflower star", "many arms", "echinoderm", "marine", "ocean"])
def _(S):
    pts = star_pts((12, 12), 16, 9.8, 7.0, S, flat=3.4)
    return [shell(poly(pts, closed=True, r=L(S, 0, 1.0))), detail(circle(12, 12, 3))]


@icon("crown-of-thorns-starfish", CAT, "Many armed sea star covered in long sharp spikes",
      tags=["acanthaster", "spiny sea star", "coral eater", "echinoderm", "reef", "predator"])
def _(S):
    n = 9
    pts = star_pts((12, 12), n, 10.2, 3.8, S, flat=3.4)
    ds = [detail(seg(*pt((12, 12), 2.2, -90 + k * 40), *pt((12, 12), 7, -90 + k * 40))) for k in range(n)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 0.8))), *ds]


@icon("brittle-starfish", CAT, "Small round disc with five very thin long snaking arms",
      tags=["brittle star", "serpent star", "ophiuroid", "echinoderm", "marine", "ocean floor"])
def _(S):
    parts = [shell(circle(12, 12, 3.2))]
    for k in range(5):
        parts.append(line(rot("M12 8.8C14.4 6.8 10 5.6 12 3.2", k * 72, 12, 12)))
    return parts


@icon("sea-urchin", CAT, "Round ball with long thin spines radiating out in every direction",
      tags=["urchin", "spiny", "echinoderm", "uni", "marine", "ocean"])
def _(S):
    c = (12, 12)
    sp = [poly([pt(c, 4, a - 11), pt(c, 10.6, a), pt(c, 4, a + 11)], closed=True, r=L(S, 0, 0.3)) for a in [-90 + k * 30 for k in range(12)]]
    return [shell(union(circle(12, 12, 5), *sp)), dot(12, 12, 1.2)]


@icon("pencil-urchin", CAT, "Round urchin with a few thick blunt pencil shaped spines pointing out",
      tags=["slate pencil urchin", "echinoderm", "spines", "reef", "marine", "aquarium"])
def _(S):
    parts = [circle(12, 12, 4.4)]
    for k in range(7):
        a = k * 360 / 7
        parts.append(rot(rect(9.9 + 0, 2, 4.2, 8, L(S, 0, 1.6)), a, 12, 12))
    return [shell(union(*parts)), dot(12, 12, 1.1)]


@icon("sand-dollar-shell", CAT, "Flat round disc with a five petal flower pattern of dots in the center",
      tags=["sand dollar", "sea biscuit", "echinoderm", "beach", "seashell", "test"])
def _(S):
    ds = [detail(rot("M12 10.6C10.8 9 10.8 7 12 5.2C13.2 7 13.2 9 12 10.6Z", k * 72, 12, 12)) for k in range(5)]
    return [shell(circle(12, 12, 9)), *ds, dot(12, 12, 1.1)]


@icon("sea-cucumber", CAT, "Long soft bumpy sausage shaped body with a ring of short tentacles at one end",
      tags=["holothurian", "echinoderm", "bêche de mer", "seafloor", "marine", "trepang"])
def _(S):
    body = rot(ellipse(13.5, 13, 8, 3.4) if S.name != "line" else "M5.5 13C5.5 10 9 9.6 13.5 9.6C18 9.6 21.5 10 21.5 13C21.5 16 18 16.4 13.5 16.4C9 16.4 5.5 16 5.5 13Z", -15, 13.5, 13)
    return [shell(body), dot(11, 13.8, 1), dot(14.2, 12.8, 1), dot(17.4, 11.8, 1),
            line("M6 15L2.6 12.5"), line("M6 15.4L2.4 15.8"), line("M6.4 16L3.6 19")]


@icon("sea-pig", CAT, "Plump deep sea cucumber walking on several tube legs with feelers on top",
      tags=["scotoplanes", "deep sea cucumber", "abyss", "echinoderm", "marine", "tube feet"])
def _(S):
    return [shell(rect(3.5, 7.5, 17, 9, S.R)), line("M7 16.5V20.5"), line("M11 16.5V21"), line("M15 16.5V21"), line("M18.5 16.5V20.5"),
            line("M7.5 7.5L6 3.5"), line("M10 7.5L10 3")]


@icon("sea-lily", CAT, "Feather star on a long stalk with feathery arms opening like a flower at the top",
      tags=["crinoid", "feather star", "echinoderm", "stalk", "deep sea", "marine"])
def _(S):
    return [line("M12 22.5V12.5"), line("M12 12.5C10 10 6.5 9 4.5 4.5"), line("M12 12.5C11 9.5 8.5 7 8 2.5"),
            line("M12 12.5V2"), line("M12 12.5C13 9.5 15.5 7 16 2.5"), line("M12 12.5C14 10 17.5 9 19.5 4.5"),
            line("M9 20H15")][:-1] + [dot(12, 12.5, 1.8)]


@icon("box-jellyfish", CAT, "Jellyfish with a square cube shaped bell and tentacles hanging from each corner",
      tags=["sea wasp", "cubozoa", "stinger", "venomous", "ocean", "marine"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 10.5, S.R)), detail("M9.5 2.5V13"), detail("M14.5 2.5V13"),
            line(wavy(6.5, 14.5, 22, 1.3, 3)), line(wavy(12, 14.5, 22, 1.3, 3, -1)), line(wavy(17.5, 14.5, 22, 1.3, 3))]


@icon("moon-jellyfish", CAT, "Round translucent bell seen from above with four horseshoe rings in the center and a fringe edge",
      tags=["aurelia", "saucer jelly", "common jellyfish", "ocean", "marine", "bloom"])
def _(S):
    ds = [detail(arc(12, 12, 4.2, a, a + 60)) for a in (15, 105, 195, 285)]
    return [shell(scallop_circle((12, 12), 8.6, 12, 0.9, S)), *ds]


@icon("lions-mane-jellyfish", CAT, "Wide bell jellyfish with a dense mass of long hair like tentacles hanging below",
      tags=["cyanea", "giant jellyfish", "arctic", "stinger", "ocean", "marine"])
def _(S):
    bell = poly([(2.5, 10), (4, 5.5), (9, 3), (15, 3), (20, 5.5), (21.5, 10)], closed=True, r=L(S, 0, 4))
    ds = [line(wavy(x, 10, 22, 1.2, 3, 1)) for x in (5.5, 8.7, 12, 15.3, 18.5)]
    return [shell(bell), *ds]


@icon("man-o-war", CAT, "Floating crested balloon float with a ruffled top edge and long tentacles hanging below",
      tags=["portuguese man o war", "siphonophore", "bluebottle", "stinger", "ocean", "beach hazard"])
def _(S):
    float_ = "M3 12C3 9.5 6 8.8 10 8.8H21.5C21.5 12 18 13.5 13 13.5H7C4.5 13.5 3 13 3 12Z"
    crest = poly([(9, 9), (11, 4.5), (13, 8), (15.2, 3.8), (17, 9)], closed=True, r=L(S, 0, 0.6))
    return [shell(union(float_, crest)), line(wavy(7, 13.5, 22, 1.3, 3)), line(wavy(12, 13.5, 22, 1.3, 3, -1)), line(wavy(17, 13.5, 22, 1.3, 3))]


@icon("by-the-wind-sailor", CAT, "Small oval raft float with a diagonal triangular sail on top and short fringe underneath",
      tags=["velella", "sea raft", "purple sail", "hydrozoan", "beach", "ocean"])
def _(S):
    raft = ellipse(12, 15, 9.5, 3) if S.name != "line" else "M2.5 15L5 12H19L21.5 15L19 18H5Z"
    sail = poly([(7, 12), (17.5, 3.5), (16, 12)], closed=True, r=L(S, 0, 0.8))
    return [shell(union(raft, sail)), line("M7 18.5V21.5"), line("M11 19V22"), line("M15 18.5V21.5")]


@icon("comb-jelly", CAT, "Oval transparent body with rows of comb stripes running from top to bottom",
      tags=["ctenophore", "sea gooseberry", "bioluminescent", "plankton", "ocean", "marine"])
def _(S):
    d = ellipse(12, 12, 6.2, 9.2) if S.name != "line" else "M12 2.8C15.5 5 18.2 8 18.2 12C18.2 16 15.5 19 12 21.2C8.5 19 5.8 16 5.8 12C5.8 8 8.5 5 12 2.8Z"
    return [shell(d), detail("M9 6.2Q7.8 12 9 17.8"), detail("M12 3.8V20.2"), detail("M15 6.2Q16.2 12 15 17.8")]


@icon("sea-anemone", CAT, "Short stalk topped with a crown of many wavy tentacles swaying upward",
      tags=["anemone", "cnidarian", "tentacles", "tide pool", "reef", "clownfish home"])
def _(S):
    ds = []
    for i, xt in enumerate((4, 8, 12, 16, 20)):
        x0 = 9.8 + i * 1.1
        ds.append(line(f"M{fmt(x0)} 14C{fmt(x0 + (xt - x0) * 0.2)} 10 {fmt(xt + (2 if i % 2 else -2))} 9 {fmt(xt)} 3.5"))
    return [shell(poly([(8, 22), (9.2, 14), (14.8, 14), (16, 22)], closed=True, r=L(S, 0, 1))), *ds]


@icon("brain-coral", CAT, "Rounded dome coral covered in winding maze like grooves",
      tags=["coral reef", "dome coral", "grooved coral", "maze", "ocean", "marine"])
def _(S):
    dome = poly([(2.5, 19.5), (3.5, 12.5), (8, 6.8), (12, 5.5), (16, 6.8), (20.5, 12.5), (21.5, 19.5)], closed=True, r=L(S, 0, 5))
    return [shell(dome), detail("M6.5 17C8 14 9.5 16 11 13C12.5 10.5 14 12.5 15.5 10"), detail("M12 17.2C13.5 15.5 15 17 16.5 15C17 14.2 17.4 13.6 18 13.5"),
            detail("M8 10.5C9 9 10.2 9.8 11 8.2")]


@icon("staghorn-coral", CAT, "Coral with several branching antler like arms forking upward from a base",
      tags=["acropora", "branching coral", "antler", "reef", "ocean", "marine"])
def _(S):
    r = S.r
    return [line("M12 22V16"), line(poly([(12, 16), (7, 10.5), (5.5, 3)], r=r)), line(poly([(7, 10.5), (9.8, 5.5)], r=r)),
            line(poly([(12, 16), (12.5, 3)], r=r)), line(poly([(12, 16), (17, 10.5), (18.5, 3)], r=r)),
            line(poly([(17, 10.5), (14.5, 7)], r=r))]


@icon("sea-fan", CAT, "Flat fan shaped coral with a fine net lattice of branches spreading from a short stem",
      tags=["gorgonian", "gorgonia", "soft coral", "lattice", "reef", "ocean"])
def _(S):
    fan = poly([(12, 19), (3, 8), (5.5, 4), (12, 3), (18.5, 4), (21, 8)], closed=True, r=L(S, 0, 2.5))
    return [shell(fan), detail("M12 19V4"), detail("M12 17L6 6.5"), detail("M12 17L18 6.5"), detail("M7.2 12.2Q12 10.2 16.8 12.2"), line("M12 19V22.5")]


@icon("sea-whip", CAT, "A few long thin flexible rod coral stems rising and bending from a rock base",
      tags=["gorgonian", "whip coral", "soft coral", "reef", "ocean", "marine"])
def _(S):
    return [shell(rect(4, 18.5, 16, 3.5, S.R)), line("M8 18.5C7 12.5 11 9.5 9 2.5"), line("M12.5 18.5C13.5 13.5 10.5 10.5 13.5 3"),
            line("M17 18.5C17.5 13.5 19.5 10 17.5 5")]


@icon("table-coral", CAT, "Flat wide plate shaped coral spreading horizontally on top of a short central stem",
      tags=["acropora", "plate coral", "reef", "shelter", "ocean", "marine"])
def _(S):
    plate = poly([(2.5, 11), (5, 8), (19, 8), (21.5, 11), (19, 13.5), (5, 13.5)], closed=True, r=L(S, 0, 2.6))
    stem = rect(10, 12, 4, 10, 0)
    return [shell(union(plate, stem)), line("M7.5 10.8H9"), line("M15 10.8H16.5")][:1] + [detail("M7 10.8H17")]


@icon("pillar-coral", CAT, "Several tall upright cylinder columns of coral rising from the seabed, fuzzy at their tops",
      tags=["dendrogyra", "column coral", "cathedral coral", "reef", "ocean", "marine"])
def _(S):
    def col(x0, x1, top):
        r = (x1 - x0) / 2
        return f"M{fmt(x0)} 20.5V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V20.5Z"
    return [shell(col(3.5, 10, 7.5)), shell(col(14, 20.5, 3)), dot(6.8, 13, 1), dot(6.8, 17, 1), dot(17.2, 8.5, 1), dot(17.2, 12.5, 1), dot(17.2, 16.5, 1),
            line("M2 22.5H22")]


@icon("mushroom-coral", CAT, "Round disc coral seen from above with fine ridges radiating from a central slit",
      tags=["fungia", "plate coral", "disc coral", "reef", "ocean", "marine"])
def _(S):
    ds = [detail("M8.8 12H15.2")]
    for a in (32, 66, 114, 148, 212, 246, 294, 328):
        ds.append(detail(seg(*pt((12, 12), 3.4, a), *pt((12, 12), 7.4, a))))
    return [shell(circle(12, 12, 9)), *ds]


@icon("bubble-coral", CAT, "Cluster of round grape like bubbles packed together on a coral base",
      tags=["plerogyra", "grape coral", "bubble", "reef", "ocean", "marine"])
def _(S):
    cs = [(6.5, 17.5), (12, 17.5), (17.5, 17.5), (9.2, 12), (14.8, 12), (12, 6.8)]
    body = union(*[circle(x, y, 3.2) for x, y in cs])
    return [shell(body), *[dot(x, y, 1) for x, y in cs]]


@icon("coral-polyp", CAT, "Close up of a tiny tube shaped polyp with a ring of short tentacles opening at its top",
      tags=["coral animal", "polyp", "cnidarian", "tentacles", "reef", "marine biology"])
def _(S):
    tube_ = poly([(9, 22), (9.5, 11.5), (14.5, 11.5), (15, 22)], closed=True, r=L(S, 0, 1))
    ds = [line(f"M{fmt(x0)} 11.5L{fmt(xt)} {fmt(yt)}") for x0, xt, yt in ((10, 5, 5.5), (11.2, 8.4, 3), (12.8, 15.6, 3), (14, 19, 5.5))]
    return [shell(tube_), *ds, line("M12 11.5V4.5")]


@icon("coral-nursery", CAT, "Small coral fragments hanging from a frame of horizontal lines like a rack underwater",
      tags=["coral restoration", "coral farm", "propagation", "reef", "conservation", "frame"])
def _(S):
    r = S.r
    ds = []
    for x in (7.5, 12, 16.5):
        ds.append(line(poly([(x, 4), (x, 9), (x - 2, 12.5)], r=r)))
        ds.append(line(poly([(x, 9), (x + 2, 12.5)], r=r)))
    return [line(poly([(2.5, 21), (2.5, 4), (21.5, 4), (21.5, 21)], r=r)), line("M2.5 17.5H21.5"), *ds][:1] + ds + [line("M2.5 17.5H21.5")]


@icon("coral-spawning", CAT, "Coral head releasing a stream of small round dots rising up into the water",
      tags=["coral reproduction", "eggs", "gametes", "full moon", "reef", "marine biology"])
def _(S):
    dome = poly([(4.5, 21.5), (5.5, 17), (9, 14), (12, 13.2), (15, 14), (18.5, 17), (19.5, 21.5)], closed=True, r=L(S, 0, 4))
    return [shell(dome), detail("M8.5 19C10 17.2 11.5 19 13 17.2"), dot(10, 9.5, 1.3), dot(14.5, 8.2, 1.3), dot(11, 4.8, 1.2), dot(17, 11.5, 1.1), dot(7, 6, 1.1), dot(16.5, 4, 1)]


@icon("sea-pen", CAT, "Tall feather quill shaped colony standing upright in the sand with leaf like side branches",
      tags=["pennatulacea", "sea feather", "soft coral", "colony", "sand", "ocean floor"])
def _(S):
    leaf = "M12 2.5C17.5 6 17.5 13 12 17C6.5 13 6.5 6 12 2.5Z" if S.name != "line" else "M12 2.5L17 8L15.5 14L12 17L8.5 14L7 8Z"
    return [shell(leaf), detail("M12 6V16"), detail("M12 9.5L9 7.5"), detail("M12 9.5L15 7.5"), detail("M12 13L9.4 11.2"), detail("M12 13L14.6 11.2"),
            line("M12 17V22")]


@icon("sea-sponge", CAT, "Tube shaped sponge with an open top rim and small pores dotted over its body",
      tags=["porifera", "tube sponge", "barrel sponge", "reef", "pores", "ocean"])
def _(S):
    body = poly([(6.5, 8.5), (5.2, 21), (18.8, 21), (17.5, 8.5)], closed=True, r=L(S, 0, 1.5))
    rim = ellipse(12, 8.5, 5.5, 2.4) if S.name != "line" else poly([(6.5, 8.5), (9, 6.1), (15, 6.1), (17.5, 8.5), (15, 10.9), (9, 10.9)], closed=True)
    return [shell(union(body, rim)), detail("M8.6 9.2Q12 11.6 15.4 9.2"), dot(8.8, 15, 1), dot(14.6, 14.2, 1), dot(11.6, 18.2, 1), dot(15.8, 18.4, 0.9)]


@icon("glass-sponge", CAT, "Tall vase shaped sponge made of a crisscross lattice grid with a fringe at its top",
      tags=["hexactinellid", "venus flower basket", "deep sea", "lattice", "sponge", "ocean"])
def _(S):
    vase = poly([(9.2, 21.5), (9.5, 16), (6.5, 11), (6, 7), (18, 7), (17.5, 11), (14.5, 16), (14.8, 21.5)], closed=True, r=L(S, 0, 2))
    return [shell(vase), detail("M6.5 9.5L15 16"), detail("M17.5 9.5L9 16"), line("M8.5 4.2V5"), line("M12 3V5"), line("M15.5 4.2V5")]


@icon("plankton", CAT, "A few tiny drifting shapes, a round cell, a crescent and a small crustacean",
      tags=["zooplankton", "phytoplankton", "microscopic", "drifting", "microscope", "ocean life"])
def _(S):
    return [shell(circle(7, 7.2, 3.4)), dot(7, 7.2, 1.0), line("M15.2 4.6C19.4 5 20.4 9.6 17.4 11.6"),
            shell(ellipse(13, 17.6, 5.2, 2.6)), line("M18 17.2L21.5 15"), dot(11, 17, 0.9)]


@icon("diatom", CAT, "Tiny round pillbox cell with a radial pattern of fine lines and dots, like a lens",
      tags=["algae", "phytoplankton", "silica", "frustule", "microscopic", "microscope"])
def _(S):
    outer = circle(12, 12, 9) if S.name != "line" else poly(regular(12, 12, 9.4, 12), closed=True)
    return [shell(outer), detail(circle(12, 12, 4.8)), dot(12, 12, 1.1)]


@icon("radiolarian", CAT, "Small sphere lattice with long thin spines radiating outward from its surface",
      tags=["protist", "zooplankton", "microscopic", "silica skeleton", "plankton", "microscope"])
def _(S):
    ds = []
    for k in range(8):
        a = -90 + k * 45
        ds.append(line(seg(*pt((12, 12), 5.8, a), *pt((12, 12), 9.4, a))))
        ds.append(dot(*pt((12, 12), 10, a), 1.0))
    return [shell(circle(12, 12, 4.4)), detail("M8.6 12H15.4"), detail("M12 8.6V15.4"), *ds][:3] + ds


@icon("seaweed", CAT, "Several wavy ribbon fronds growing up from a small rock and swaying to one side",
      tags=["kelp", "algae", "marine plant", "ocean", "seabed", "kombu"])
def _(S):
    return [shell(rect(3.5, 19.5, 17, 3, 1.5 if S.name != "line" else 0)), line(wavy(8, 19.5, 3, 1.8, 3)), line(wavy(12.5, 19.5, 5, 1.8, 3, -1)),
            line(wavy(17, 19.5, 3, 1.8, 3))]


@icon("sea-grass", CAT, "Cluster of long thin straight blades growing from a sandy seabed line",
      tags=["eelgrass", "seagrass meadow", "marine plant", "ocean", "seabed", "blades"])
def _(S):
    r = S.r
    return [line(poly([(5.5, 20), (4.5, 12), (6, 5)], r=r)), line(poly([(9.2, 20), (9, 9), (11, 3.5)], r=r)), line(poly([(13, 20), (13.8, 8), (13, 2.5)], r=r)),
            line(poly([(16.8, 20), (17.5, 11), (19.5, 6)], r=r)), line("M2.5 21.8H21.5")]


@icon("sea-lettuce", CAT, "Thin crinkled green leaf sheet with ruffled wavy edges",
      tags=["ulva", "green algae", "seaweed", "edible algae", "ocean", "marine plant"])
def _(S):
    return [shell(scallop_circle((12, 12), 8, 9, 1.1, S)), detail("M7 12.5C8.5 9.5 11 9.5 12.5 11C14 12.5 15.5 12.5 17 10"), detail("M8 16.5C10 15 12 15.5 14 16.5")]


@icon("sargassum", CAT, "Floating mat of branching seaweed with small round berry floats resting on a wavy surface line",
      tags=["gulfweed", "floating seaweed", "sea berries", "brown algae", "ocean", "drift"])
def _(S):
    return [line(water(2, 22, 19.5, 1.2, 3)), line("M3 16C7 15 8.5 11.5 12.5 11C15.5 10.6 17.5 8 20 6.5"), line("M9 14.5C9.5 12 8.5 10 6.5 8.5"),
            dot(6.2, 7.2, 1.4), dot(11, 8.2, 1.4), dot(16, 12.5, 1.4), dot(20, 4.6, 1.3)]


@icon("samphire", CAT, "Small succulent plant with jointed branching cylinder stems like tiny green fingers",
      tags=["sea asparagus", "glasswort", "salicornia", "salt marsh plant", "succulent", "edible"])
def _(S):
    r = S.r
    return [line("M12 22V5"), line(poly([(12, 17), (7.5, 13), (7.5, 8.5)], r=r)), line(poly([(12, 17), (16.5, 13), (16.5, 8.5)], r=r)),
            dot(12, 3.8, 1.1), dot(7.5, 7.2, 1.0), dot(16.5, 7.2, 1.0)]


@icon("algae-bloom", CAT, "Wavy water surface line with a thick layer of blotchy scum and dots floating on it",
      tags=["red tide", "eutrophication", "green water", "pond scum", "pollution", "cyanobacteria"])
def _(S):
    blob = union(circle(6.5, 12.5, 2.9), circle(11.5, 11, 3.5), circle(17, 12.5, 2.9))
    return [line(water(2, 22, 18, 1.2, 3)), shell(blob), dot(5, 6, 1.1), dot(11, 4.5, 1.1), dot(18, 6.5, 1.1)]


@icon("dune-grass", CAT, "Tufts of long thin grass blades bending in the wind on top of a rounded sand dune",
      tags=["marram grass", "beach grass", "sand dune", "coast", "shore", "windswept"])
def _(S):
    dune = "M2 21.5C4 16 9 13.5 13 14.5C17 15.5 20 18 22 21.5Z"
    return [shell(dune), line("M10 14C10 10 12 7 16 6"), line("M13 14.5C12.5 9.5 13.5 5.5 16.5 3"), line("M8 15C7 12 7 9.5 5 7.5")]


@icon("salt-marsh", CAT, "Reed tufts and grass growing in patches between winding tidal channels of water",
      tags=["tidal marsh", "wetland", "estuary", "reeds", "coast", "marshland"])
def _(S):
    return [line("M4 16.5L3 8"), line("M7 16.5V4.5"), line("M10 16.5L11 8"),
            line("M14.5 16.5L13.5 9"), line("M17.5 16.5V6"), line("M20.5 16.5L21 10"),
            line("M2 20.5C6 18.8 8 22.2 12 20.5C16 18.8 18 22.2 22 20.5")]


@icon("rocky-shore", CAT, "A row of rounded rocks and boulders at the edge of a wavy water line",
      tags=["tide pool", "boulders", "coast", "shoreline", "intertidal", "rocks"])
def _(S):
    r = L(S, 0, 2.5)
    rocks = [poly([(2.5, 17.5), (3.2, 13.5), (7, 11.8), (10, 14), (10.3, 17.5)], closed=True, r=r),
             poly([(11.5, 17.5), (11.8, 11), (15.5, 8.8), (19, 11), (19.4, 17.5)], closed=True, r=r)]
    return [shell(rocks[0]), shell(rocks[1]), line(water(2, 22, 20.5, 1.1, 3))]
