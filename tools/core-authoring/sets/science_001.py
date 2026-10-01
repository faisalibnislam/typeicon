"""TypeIcon Core: science (batch science_001).

Laboratory glassware and instruments, molecules and bonds, and simple chemistry phenomena. Drawn from the
objects and diagrams themselves; side or front views, kept to a few clear shapes.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "science"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap):
    """Container radius: small and square-ish in Line, fully softened (up to cap) in Rounded."""
    return min(S.R, cap) if S.name == "rounded" else min(S.R, cap) * 0.3


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def grow(d, g):
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def axis(origin, deg):
    """Local frame: x runs along `deg` (0 = right, positive = clockwise on screen)."""
    ox, oy = origin
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return lambda x, y: (ox + x * c - y * s, oy + x * s + y * c)


def drop_d(cx, top, w, h):
    """Small teardrop with its point up: tip at (cx, top), round bottom of width w, total height h."""
    ys = top + h - w / 2
    k = ys - top
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + w * 0.2)} {fmt(top + k * 0.4)} {fmt(cx + w / 2)} {fmt(ys - k * 0.3)} "
            f"{fmt(cx + w / 2)} {fmt(ys)}A{fmt(w / 2)} {fmt(w / 2)} 0 0 1 {fmt(cx - w / 2)} {fmt(ys)}"
            f"C{fmt(cx - w / 2)} {fmt(ys - k * 0.3)} {fmt(cx - w * 0.2)} {fmt(top + k * 0.4)} {fmt(cx)} {fmt(top)}Z")


def drop(cx, top, w=2.6, h=3.6):
    return solid(drop_d(cx, top, w, h))


def wave_d(x, y0, y1, amp=1.5):
    """Vertical wavy vapor stroke from (x, y0) to (x, y1)."""
    m = (y0 + y1) / 2
    return (f"M{fmt(x)} {fmt(y0)}C{fmt(x - amp * 1.6)} {fmt((y0 + m) / 2)} {fmt(x + amp * 1.6)} {fmt((y0 + m) / 2 + (m - y0) / 2)} "
            f"{fmt(x)} {fmt(m)}C{fmt(x - amp * 1.6)} {fmt((m + y1) / 2)} {fmt(x + amp * 1.6)} {fmt((m + y1) / 2 + (y1 - m) / 2)} {fmt(x)} {fmt(y1)}")


def flame_d(cx, by, h=8.0, w=6.0):
    """Flame silhouette: base centre (cx, by), tip above."""
    top = by - h
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + w * 0.15)} {fmt(top + h * 0.3)} {fmt(cx + w / 2)} {fmt(by - h * 0.45)} "
            f"{fmt(cx + w / 2)} {fmt(by - h * 0.2)}C{fmt(cx + w / 2)} {fmt(by + h * 0.02)} {fmt(cx + w * 0.25)} {fmt(by)} {fmt(cx)} {fmt(by)}"
            f"C{fmt(cx - w * 0.25)} {fmt(by)} {fmt(cx - w / 2)} {fmt(by + h * 0.02)} {fmt(cx - w / 2)} {fmt(by - h * 0.2)}"
            f"C{fmt(cx - w / 2)} {fmt(by - h * 0.45)} {fmt(cx - w * 0.15)} {fmt(top + h * 0.3)} {fmt(cx)} {fmt(top)}Z")


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def arc_arrow(cx, cy, r, a0, a1, head=2.4):
    """Clockwise arc with an open arrowhead at its end."""
    ex, ey = polar(cx, cy, r, a1)
    t = math.radians(a1 + 90)
    tx, ty = math.cos(t), math.sin(t)
    nx, ny = -ty, tx
    b = (ex - tx * head, ey - ty * head)
    return [line(arc(cx, cy, r, a0, a1)),
            line(poly([(b[0] + nx * head, b[1] + ny * head), (ex, ey), (b[0] - nx * head, b[1] - ny * head)]))]


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def tube(ctrl, width, n=16):
    """Closed outline around a cubic centreline; width(t) gives the width in px."""
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


def bubbles(pts, r=1.0):
    return [dot(x, y, r) for x, y in pts]


# ============================================================================ glassware

@icon("round-bottom-flask", CAT, "Round-bottom laboratory flask with a straight neck and liquid in the ball.",
      tags=["boiling flask", "flask", "chemistry", "glassware", "lab", "reaction vessel"])
def _(S):
    body = union(poly([(10, 3), (14, 3), (14, 9), (10, 9)], closed=True, r=S.r * 0.6), circle(12, 15, 6.5))
    return [shell(body), detail(seg(6, 16, 18, 16))]


@icon("volumetric-flask", CAT, "Pear-shaped volumetric flask with a long neck, a fill mark and a stopper.",
      tags=["measuring flask", "standard flask", "chemistry", "glassware", "lab", "dilution"])
def _(S):
    body = union(rect(8.5, 2.5, 7, 3, rr(S, 1.5)), rect(10, 5, 4, 7), circle(12, 16.5, 5.5))
    return [shell(body), detail(seg(8.5, 5.5, 15.5, 5.5)), detail(seg(10, 9, 14, 9))]


@icon("side-arm-flask", CAT, "Conical flask with a short hose barb on the side of the neck.",
      tags=["vacuum flask", "filter flask", "buchner flask", "suction", "chemistry", "glassware"])
def _(S):
    body = union(poly([(10, 3), (14, 3), (14, 9), (20, 20.5), (4, 20.5), (10, 9)], closed=True, r=S.r),
                 rect(3, 5, 8.5, 4, rr(S, 1.2)))
    return [shell(body), detail(seg(6.5, 16, 17.5, 16))]


@icon("graduated-cylinder", CAT, "Tall measuring cylinder with a pouring spout, a wide foot and tick marks.",
      tags=["measuring cylinder", "volume", "chemistry", "glassware", "lab", "measure liquid"])
def _(S):
    body = poly([(7.5, 3), (15, 3), (15, 18), (18.5, 20.5), (5.5, 20.5), (9, 18), (9, 4.5)], closed=True, r=S.r * 0.8)
    return [shell(body), detail(seg(15, 7, 12, 7)), detail(seg(15, 11, 12, 11)), detail(seg(9, 15.5, 15, 15.5))]


@icon("burette", CAT, "Long graduated tube with a stopcock near the bottom and a drop falling from the tip.",
      tags=["titration", "buret", "chemistry", "glassware", "lab", "dispense liquid"])
def _(S):
    body = union(rect(10, 2, 4, 12), rect(7.5, 13.5, 9, 3.5, rr(S, 1)))
    return [shell(body), detail(seg(10, 5, 12.5, 5)), detail(seg(10, 9, 12.5, 9)),
            line(seg(16.5, 15.25, 20.5, 15.25)), line(seg(12, 17, 12, 18.5)), drop(12, 19.6, 2.6, 2.6)]


@icon("separatory-funnel", CAT, "Pear-shaped glass funnel with a stopper on top, two liquid layers and a tap on the stem.",
      tags=["separating funnel", "extraction", "chemistry", "glassware", "lab", "liquid layers"])
def _(S):
    body = union(poly([(9.5, 2), (14.5, 2), (13.5, 4.5), (10.5, 4.5)], closed=True, r=S.r * 0.5), circle(12, 10, 6.5),
                 poly([(6.8, 12.5), (17.2, 12.5), (13, 18), (11, 18)], closed=True, r=S.r * 0.3))
    return [shell(body), detail(seg(5.6, 11, 18.4, 11)), line(seg(12, 17, 12, 21.5)), line(seg(8.5, 19.5, 15.5, 19.5))]


@icon("buchner-funnel", CAT, "Wide flat funnel with a perforated plate, set in a collar on a flask neck.",
      tags=["suction filter", "vacuum filtration", "chemistry", "glassware", "lab", "filter flask"])
def _(S):
    funnel = poly([(3.5, 3.5), (20.5, 3.5), (20.5, 9), (14, 11.5), (10, 11.5), (3.5, 9)], closed=True, r=S.r * 0.6)
    flask = union(rect(8.5, 11, 7, 3.5, rr(S, 1)),
                  poly([(10, 14), (14, 14), (14, 16.5), (19.5, 21.5), (4.5, 21.5), (10, 16.5)], closed=True, r=S.r * 0.5))
    return [shell(union(funnel, flask)), dot(7.5, 7, 1), dot(12, 7, 1), dot(16.5, 7, 1)]


@icon("thistle-funnel", CAT, "Long thin glass tube with a small bulb and a flared cup at the top, like a thistle head.",
      tags=["thistle tube", "funnel", "chemistry", "glassware", "lab", "add liquid"])
def _(S):
    body = union(poly([(5.5, 2.5), (18.5, 2.5), (14.5, 8), (9.5, 8)], closed=True, r=S.r * 0.5), circle(12, 11, 3.5))
    return [shell(body), line(seg(12, 14, 12, 21.5))]


@icon("filter-funnel", CAT, "Lab funnel holding a folded paper cone, with a drip falling from the stem.",
      tags=["filter paper", "filtering", "chemistry", "glassware", "lab", "strain"])
def _(S):
    return [shell(poly([(4, 3.5), (20, 3.5), (13, 12), (11, 12)], closed=True, r=S.r * 0.6)),
            detail("M8 5.5L12 10.5L16 5.5"), line(seg(12, 12, 12, 17)), drop(12, 18.6, 2.8, 3.6)]


@icon("watch-glass", CAT, "Shallow curved glass dish seen from the side with a drop falling toward it.",
      tags=["watch glass", "glass dish", "chemistry", "glassware", "lab", "sample dish", "evaporation"])
def _(S):
    return [shell("M3 10H21A11.5 11.5 0 0 1 3 10Z"), drop(12, 2.5, 3, 4)]


@icon("evaporating-dish", CAT, "Wide shallow bowl with a pouring lip and wisps of vapor rising from it.",
      tags=["evaporation dish", "porcelain dish", "chemistry", "glassware", "lab", "heating", "vapor"])
def _(S):
    bowl = "M4 11H21C21 16.5 17 20 12.5 20C8 20 4 16.5 4 11Z"
    return [shell(bowl), line(seg(4, 11, 2.8, 9.4)),
            line(wave_d(9.5, 2.5, 8, 1.1)), line(wave_d(15.5, 2.5, 8, 1.1))]


@icon("crucible-tongs", CAT, "Long scissor-like tongs gripping a small crucible cup at the tip.",
      tags=["tongs", "crucible", "chemistry", "lab", "heating", "hot", "grip"])
def _(S):
    m = axis((10, 13.5), -45)
    a = [m(-8, 3), m(7, -3.6)]
    b = [m(-8, -3), m(7, 3.6)]
    cup = poly([m(7.5, -3.8), m(11.5, -4.6), m(11.5, 4.6), m(7.5, 3.8)], closed=True, r=S.r * 0.6)
    return [line(poly(a)), line(poly(b)), shell(cup), dot(*m(-0.5, 0), 1.0)]


@icon("test-tube-holder", CAT, "Spring clothespin-style clamp gripping a test tube near its mouth, with a long handle.",
      tags=["test tube clamp", "tube holder", "chemistry", "lab", "heating", "clothespin"])
def _(S):
    tube = "M6 2H12V17.5A3 3 0 0 1 6 17.5Z"
    clamp = union(rect(3.5, 6, 10, 5.5, rr(S, 2)), rect(12, 7, 9, 3.5, rr(S, 1.5)))
    pieces = minus(tube, rect(3.5, 7, 10, 3.5))
    return [shell(pieces), shell(clamp), detail(seg(14.5, 8.75, 19.5, 8.75)), dot(9, 8.75, 1.0), detail(seg(6, 15.5, 12, 15.5))]


@icon("reagent-bottle", CAT, "Squat glass bottle with a mushroom stopper and a blank label.",
      tags=["chemical bottle", "stock bottle", "chemistry", "glassware", "lab", "jar", "stopper"])
def _(S):
    body = union("M7.5 6.5A4.5 4.5 0 0 1 16.5 6.5Z", rect(9.5, 6, 5, 4),
                 poly([(9, 8), (15, 8), (15, 10.5), (19, 12.5), (19, 21), (5, 21), (5, 12.5), (9, 10.5)], closed=True, r=S.r * 0.6))
    return [shell(body), detail(rect(9, 14, 6, 4.5, rr(S, 1)))]


@icon("dropper-bottle", CAT, "Small bottle with a rubber bulb dropper cap and a blank label.",
      tags=["dropper", "tincture bottle", "chemistry", "lab", "pipette bottle", "serum", "drops"])
def _(S):
    body = union(ellipse(12, 5.5, 2.5, 3.5), rect(9, 8.5, 6, 3, rr(S, 1)),
                 poly([(9, 11), (15, 11), (18, 13.5), (18, 21), (6, 21), (6, 13.5)], closed=True, r=S.r * 0.6))
    return [shell(body), detail(rect(9, 15, 6, 3.5, rr(S, 1)))]


@icon("desiccator", CAT, "Wide glass pot with a domed lid, a knob and a perforated plate across the middle.",
      tags=["drying jar", "vacuum desiccator", "chemistry", "glassware", "lab", "dry", "moisture"])
def _(S):
    body = union("M4 11C4 6.5 8 4.5 12 4.5C16 4.5 20 6.5 20 11Z", rect(10.5, 2, 3, 3, rr(S, 1)),
                 rect(3, 11, 18, 10.5, rr(S, 2)))
    return [shell(body), detail(seg(3, 11, 21, 11)), detail(seg(5.5, 16.5, 8.5, 16.5)),
            detail(seg(10.5, 16.5, 13.5, 16.5)), detail(seg(15.5, 16.5, 18.5, 16.5))]


@icon("glass-condenser", CAT, "Long diagonal tube inside a wider jacket with two small hose inlets on opposite sides.",
      tags=["liebig condenser", "reflux", "distillation", "chemistry", "glassware", "lab", "cooling"])
def _(S):
    m = axis((12, 12), -35)
    jacket = poly([m(-8, -4), m(8, -4), m(8, 4), m(-8, 4)], closed=True, r=S.r * 0.6)
    return [shell(jacket), line(poly([m(-11, 0), m(11, 0)])), line(poly([m(-5, 4), m(-5, 7)])),
            line(poly([m(5, -4), m(5, -7)]))]


@icon("distillation-setup", CAT, "Round flask over a flame, joined by an angled condenser to a collecting flask.",
      tags=["distillation", "still", "chemistry", "glassware", "lab", "purify", "apparatus"])
def _(S):
    m = axis((10.8, 5), 50)
    cond = poly([m(0, -2.2), m(10, -2.2), m(10, 2.2), m(0, 2.2)], closed=True, r=S.r * 0.5)
    flask = union(rect(5.5, 3, 3, 4, 0), circle(7, 11.5, 4.5))
    coll = poly([(16.5, 15.5), (19.5, 15.5), (22, 21.5), (14, 21.5)], closed=True, r=S.r * 0.4)
    return [shell(flask), line(seg(7, 3.5, 10.8, 3.5)), shell(cond), shell(coll), solid(flame_d(7, 22, 3.6, 3.6))]


@icon("retort-stand", CAT, "Heavy flat base with an upright rod and a clamp arm holding a small round flask.",
      tags=["ring stand", "lab stand", "clamp stand", "chemistry", "lab", "support", "apparatus"])
def _(S):
    flask = union(rect(14, 3.5, 4, 5, 0), circle(16, 12, 4))
    return [shell(rect(3, 18.5, 18, 2.5, rr(S, 1))), line(seg(6.5, 18.5, 6.5, 3)), line(seg(6.5, 6, 19.5, 6)),
            shell(flask)]


@icon("bunsen-burner", CAT, "Upright burner barrel on a round base with a side gas inlet and a pointed flame.",
      tags=["gas burner", "heating", "chemistry", "lab", "flame", "fire", "gas"])
def _(S):
    body = union(rect(9.5, 12, 5, 6, 0), poly([(5, 21.5), (7, 18), (17, 18), (19, 21.5)], closed=True, r=S.r * 0.4))
    return [shell(body), line(seg(14.5, 14.5, 20.5, 14.5)), shell(flame_d(12, 9.5, 6, 5))]


@icon("spirit-lamp", CAT, "Squat glass jar with a wick holder in the lid and a small teardrop flame.",
      tags=["alcohol lamp", "burner", "heating", "chemistry", "lab", "flame", "fuel"])
def _(S):
    body = union(rect(10.5, 9.5, 3, 3, 0),
                 poly([(9, 12), (15, 12), (19, 14), (19, 21), (5, 21), (5, 14)], closed=True, r=S.r * 0.6))
    return [shell(body), detail(seg(7, 17, 17, 17)), shell(flame_d(12, 8, 5, 4))]


@icon("tripod-gauze", CAT, "Three-legged metal stand with a square wire mesh on top and a flame below.",
      tags=["wire gauze", "tripod stand", "heating", "chemistry", "lab", "support", "flame"])
def _(S):
    plate = poly([(7, 3.5), (17, 3.5), (21, 8.5), (3, 8.5)], closed=True, r=S.r * 0.5)
    return [shell(plate), detail(seg(12, 3.5, 12, 8.5)), line(seg(6, 8.5, 3.5, 21.5)), line(seg(18, 8.5, 20.5, 21.5)),
            shell(flame_d(12, 21, 7, 5))]


# ============================================================================ small tools and consumables

@icon("stirring-rod", CAT, "Slim glass rod leaning in a beaker of liquid with a wavy surface.",
      tags=["glass rod", "stir", "mix", "chemistry", "lab", "beaker", "swirl"])
def _(S):
    beaker = poly([(5, 6), (5, 21), (19, 21), (19, 6)], closed=True, r=S.r)
    return [shell(beaker), detail("M5 12.5Q7.5 10.5 10 12.5T15 12.5T19 12.5"), line(seg(17.5, 1.5, 10.5, 17))]


@icon("lab-spatula", CAT, "Thin metal spatula with a curved spoon end and a flat blade at the other end.",
      tags=["spatula", "scoop", "scoopula", "chemistry", "lab", "powder", "sample"])
def _(S):
    m = axis((12, 12), -45)
    spoon = rot(ellipse(*m(7, 0), 4.6, 3), -45, *m(7, 0))
    blade = poly([m(-11.5, -2.2), m(-7.5, -2.2), m(-7.5, 2.2), m(-11.5, 2.2)], closed=True, r=S.r * 0.5)
    return [shell(spoon), shell(blade), line(poly([m(-7.5, 0), m(2.4, 0)]))]


@icon("rubber-stopper", CAT, "Tapered rubber plug seen from above the side, with one hole through the middle.",
      tags=["bung", "cork", "stopper", "chemistry", "lab", "flask", "seal"])
def _(S):
    if S.name == "line":
        body = union(ellipse(12, 7.5, 8, 3), poly([(4, 7.5), (20, 7.5), (17.2, 19), (6.8, 19)], closed=True))
    else:
        body = union(ellipse(12, 7.5, 8, 3), poly([(4, 7.5), (20, 7.5), (17.2, 18.5), (6.8, 18.5)], closed=True), ellipse(12, 18.5, 5.2, 2.2))
    return [shell(body), Part("dot", ellipse(12, 7.5, 2.4, 0.9))]


@icon("retort", CAT, "Round glass vessel with a long neck that bends down and tapers to a point.",
      tags=["glass retort", "distilling", "alchemy", "chemistry", "glassware", "lab", "alchemist"])
def _(S):
    ball = circle(8.5, 15, 5.5)
    neck = poly(tube(((10.5, 11), (14, 2), (21, 1), (21, 20.5)), lambda t: 4.2 - L(S, 3.4, 2.0) * t), closed=True)
    body = union(ball, neck)
    if S.name == "rounded":
        body = union(body, circle(21, 19.5, 1.6))
    return [shell(body), detail(seg(3.5, 16.5, 13.5, 16.5))]


@icon("vacuum-bell-jar", CAT, "Glass dome with a knob on a flat plate, a small bell hanging inside.",
      tags=["bell jar", "vacuum chamber", "physics", "sound in vacuum", "lab", "experiment", "glass dome"])
def _(S):
    dome = union("M4.5 18.5V12C4.5 7 8 5 12 5C16 5 19.5 7 19.5 12V18.5Z", rect(10.5, 2, 3, 3.5, rr(S, 1)),
                 rect(2.5, 18.5, 19, 3, rr(S, 1)))
    return [shell(dome), detail(seg(12, 5, 12, 9)), detail("M9 16C9 12 10.3 10 12 10C13.7 10 15 12 15 16Z")]


@icon("chromatography-column", CAT, "Vertical glass column with bands stacked inside and a tap at the bottom.",
      tags=["column chromatography", "separation", "chemistry", "glassware", "lab", "purification", "bands"])
def _(S):
    body = union(rect(7.5, 2, 9, 12.5, rr(S, 1.5)), poly([(7.5, 14), (16.5, 14), (13, 18), (11, 18)], closed=True, r=S.r * 0.3))
    return [shell(body), detail(seg(7.5, 6.5, 16.5, 6.5)), detail(seg(7.5, 10.5, 16.5, 10.5)),
            line(seg(12, 18, 12, 21.5)), line(seg(8.5, 20, 15.5, 20))]


@icon("paper-chromatography", CAT, "Strip of paper standing in a beaker of solvent with separated spots on it.",
      tags=["chromatogram", "separation", "chemistry", "lab", "ink", "pigment", "solvent"])
def _(S):
    return [line(poly([(4, 9), (4, 21), (20, 21), (20, 9)], r=S.r)), shell(rect(9.5, 2.5, 5, 14, rr(S, 1))),
            detail(seg(4, 15.5, 8, 15.5)), detail(seg(16, 15.5, 20, 15.5)), dot(12, 6.5, 1.0), dot(12, 10.5, 1.0)]


@icon("sample-vial", CAT, "Short cylindrical vial with a crimped cap and a septum dot on top.",
      tags=["vial", "glass vial", "sample bottle", "chemistry", "lab", "analysis", "autosampler"])
def _(S):
    body = union(rect(7, 3, 10, 4.5, rr(S, 1.5)), rect(8, 7, 8, 14.5, rr(S, 2)))
    return [shell(body), dot(12, 5.25, 1.0), detail(seg(8, 15, 16, 15))]


@icon("microcentrifuge-tube", CAT, "Small conical tube with a hinged snap cap swung open to the side.",
      tags=["eppendorf tube", "micro tube", "centrifuge tube", "chemistry", "biology", "lab", "sample"])
def _(S):
    m = axis((15.5, 8.8), -50)
    tube = union(rect(4.5, 8, 11, 2.5, rr(S, 1)), poly([(5.5, 10), (14.5, 10), (14.5, 14.5), (10, 21), (5.5, 14.5)], closed=True, r=S.r * 0.6))
    lid = poly([m(0.8, -2.3), m(5.5, -2.3), m(5.5, 2.3), m(0.8, 2.3)], closed=True, r=S.r * 0.6)
    return [shell(tube), shell(lid)]


@icon("cuvette", CAT, "Small square-sided transparent tube with a light beam passing through it.",
      tags=["spectroscopy", "sample cell", "chemistry", "lab", "light beam", "absorbance", "optical"])
def _(S):
    return [shell(rect(8, 4.5, 8, 16, rr(S, 2))), detail(seg(8, 9, 16, 9)),
            line(seg(2, 14, 6, 14)), line(seg(18, 14, 21, 14)), line(poly([(19.2, 12), (21.5, 14), (19.2, 16)]))]


@icon("volumetric-pipette", CAT, "Long thin glass pipette with a bulge in the middle and a mark on the upper stem.",
      tags=["transfer pipette", "bulb pipette", "chemistry", "glassware", "lab", "measure liquid", "titration"])
def _(S):
    bulb = ellipse(12, 12, 3.4, 5.5) if S.name == "rounded" else "M12 6.5C17 9.5 17 14.5 12 17.5C7 14.5 7 9.5 12 6.5Z"
    return [shell(bulb), line(seg(12, 2, 12, 6.5)), line(seg(12, 17.5, 12, 21.5)), line(seg(10, 4.5, 14, 4.5))]


# ============================================================================ instruments

@icon("magnetic-stirrer", CAT, "Flat plate with a dial under a beaker holding a stir bar and a swirl in the liquid.",
      tags=["stir plate", "hotplate stirrer", "chemistry", "lab", "mixing", "stir bar", "equipment"])
def _(S):
    return [shell(rect(6, 3.5, 12, 12, rr(S, 2))), shell(rect(3, 17, 18, 4, rr(S, 1.5))),
            detail("M7 8Q9.5 6 12 8T17 8"), Part("dot", rect(9, 12, 6, 1.6, 0.8)), dot(18, 19, 0.9)]


@icon("orbital-shaker", CAT, "Flat platform holding two conical flasks, with a circular arrow showing the shaking motion.",
      tags=["shaker", "lab shaker", "incubator shaker", "chemistry", "biology", "mixing", "equipment"])
def _(S):
    fl = lambda dx: poly([(6.5 + dx, 2.5), (9.5 + dx, 2.5), (9.5 + dx, 5), (12 + dx, 10.5), (4 + dx, 10.5), (6.5 + dx, 5)], closed=True, r=S.r * 0.5)
    return [shell(fl(0)), shell(fl(8)), shell(rect(2.5, 11, 19, 3, rr(S, 1))), *arc_arrow(12, 18.5, 2.9, 30, 320, 2.2)]


@icon("lab-water-bath", CAT, "Rectangular tank with two test tubes poking out of the lid and wavy heat lines inside.",
      tags=["water bath", "heated bath", "chemistry", "biology", "lab", "incubate", "heat"])
def _(S):
    tank = rect(3, 11, 18, 10.5, rr(S, 2))
    tubes = minus(union(rect(6, 3, 4, 9), rect(14, 3, 4, 9)), tank)
    return [shell(tubes), shell(tank), detail("M6 16Q8 14 10 16T14 16T18 16")]


@icon("fume-hood", CAT, "Tall cabinet with a sash window raised halfway and an exhaust duct on top.",
      tags=["fume cupboard", "ventilation", "chemistry", "lab", "safety", "extraction", "cabinet"])
def _(S):
    body = union(rect(9.5, 2, 5, 5, rr(S, 1)), rect(3.5, 6, 17, 15.5, rr(S, 2)))
    return [shell(body), detail(rect(6.5, 9.5, 11, 8, rr(S, 1))), detail(seg(6.5, 13.5, 17.5, 13.5))]


@icon("spectrophotometer", CAT, "Benchtop instrument with a sample lid, and a small display showing a graph peak.",
      tags=["spectrometer", "absorbance", "chemistry", "lab", "analysis", "instrument", "uv vis"])
def _(S):
    box = union(rect(3, 13, 18, 8.5, rr(S, 1.5)), rect(4.5, 9.5, 5.5, 4, rr(S, 1)))
    return [shell(box), shell(rect(12, 2.5, 8.5, 8, rr(S, 1.5))), detail("M14 8.5H15.5L16.25 5.5L17 8.5H18.5")]


@icon("rotary-evaporator", CAT, "Round flask dipping into a heated bath, joined by an arm to a coiled condenser and motor.",
      tags=["rotavap", "evaporator", "solvent removal", "chemistry", "lab", "condenser", "equipment"])
def _(S):
    bath = "M2.5 13H14C14 18 11 21.5 8.25 21.5C5.5 21.5 2.5 18 2.5 13Z"
    flask = minus(circle(8.25, 9.5, 4.5), bath)
    return [shell(bath), shell(flask), line(seg(11.5, 6.5, 16, 4)),
            shell(rect(14.5, 2.5, 6, 3.5, rr(S, 1))),
            line(poly([(17.5, 6), (17.5, 8.5), (20, 10), (15.5, 12), (20, 14), (15.5, 16), (20, 18), (17.5, 20)]))]


@icon("electron-microscope", CAT, "Tall column instrument made of stacked sections beside a monitor.",
      tags=["sem", "tem", "microscope", "science", "lab", "nanoscale", "imaging"])
def _(S):
    col = union(rect(6.5, 2.5, 4, 3, 0), rect(5, 5, 7, 5, 0), rect(6.5, 10, 4, 3, 0), rect(3.5, 13, 10, 7.5, rr(S, 1.5)))
    return [shell(col), shell(rect(15.5, 8, 6, 5.5, rr(S, 1.5))), line(seg(18.5, 13.5, 18.5, 17)), line(seg(15.5, 17.5, 21.5, 17.5))]


@icon("microtome", CAT, "Block machine with a hand wheel on the side and a blade slicing a thin curled ribbon.",
      tags=["tissue slicer", "sectioning", "histology", "biology", "lab", "specimen", "blade"])
def _(S):
    return [shell(rect(2.5, 13, 10, 8.5, rr(S, 1.5))), shell(rect(4.5, 8, 5, 5, rr(S, 1))),
            shell(circle(17.5, 15, 4.5)), dot(17.5, 15, 1.2), line(seg(11, 5, 13.5, 8.5)),
            line("M3.5 5C5 2.5 8 2.5 9 4.5")]


@icon("bioreactor", CAT, "Stainless tank with a domed top, a motor, a stirrer shaft inside and pipes leading in.",
      tags=["fermenter", "fermentor", "biotech", "culture vessel", "lab", "tank", "industrial"])
def _(S):
    tank = union("M5 9C5 6.5 8 5.5 12 5.5C16 5.5 19 6.5 19 9Z", rect(5, 8.5, 14, 12, rr(S, 2)), rect(9.5, 1.5, 5, 4, rr(S, 1)))
    return [shell(tank), detail(seg(12, 6, 12, 16)), detail(seg(9, 17, 15, 17)), line(seg(2, 11, 5, 11)), line(seg(19, 14.5, 22, 14.5))]


# ============================================================================ instruments, balances

@icon("chemistry-set", CAT, "Open case holding two test tubes of liquid, like a beginner chemistry kit.",
      tags=["chemistry kit", "science kit", "experiment kit", "test tubes", "lab", "stem", "educational toy"])
def _(S):
    body = union(rect(2.5, 13, 19, 8.5, rr(S, 2)), rect(4.5, 4, 5, 9.5, rr(S, 1.5)), rect(14.5, 6.5, 5, 7, rr(S, 1.5)))
    return [shell(body), detail(seg(4.5, 8.5, 9.5, 8.5)), detail(seg(14.5, 10, 19.5, 10)), detail(seg(6, 17.25, 18, 17.25))]


@icon("analytical-balance", CAT, "Precision scale with a glass draft shield around the weighing pan and a display at the front.",
      tags=["precision balance", "lab scale", "milligram", "weighing", "chemistry", "lab", "mass measurement"])
def _(S):
    body = union(rect(4, 2.5, 16, 14, rr(S, 2)), rect(2.5, 15.5, 19, 6, rr(S, 1.5)))
    return [shell(body), detail(seg(8, 12, 16, 12)), detail(seg(12, 8.5, 12, 12)), detail(seg(6, 19, 11, 19))]


@icon("beam-balance", CAT, "Two-pan balance on a central post with a beam tilted so the left pan hangs lower.",
      tags=["equal arm balance", "scales", "weighing", "mass", "physics", "lab", "compare weight"])
def _(S):
    return [line(seg(12, 5, 12, 20.5)), line(poly([(7.5, 21), (16.5, 21)])),
            line(seg(4.5, 8.5, 19.5, 4.5)),
            line(seg(5.5, 8.5, 5.5, 13)), line(seg(18.5, 4.5, 18.5, 9)),
            shell(poly([(2.5, 13), (8.5, 13), (7.5, 16.5), (3.5, 16.5)], closed=True, r=S.r * 0.5)),
            shell(poly([(15.5, 9), (21.5, 9), (20.5, 12.5), (16.5, 12.5)], closed=True, r=S.r * 0.5))]


@icon("triple-beam-balance", CAT, "Weighing pan on the left and three horizontal beams with sliding weights on the right.",
      tags=["lab balance", "school balance", "mass", "weighing", "physics", "chemistry", "sliding weights"])
def _(S):
    return [shell(rect(3, 17.5, 18, 4, rr(S, 1.5))), line(seg(12, 3.5, 12, 17.5)),
            shell("M3.5 9H10.5A3.5 3 0 0 1 3.5 9Z" if False else poly([(3, 9), (10, 9), (9, 12.5), (4, 12.5)], closed=True, r=S.r * 0.5)),
            line(seg(6.5, 12.5, 6.5, 17.5)),
            line(seg(12, 5, 21.5, 5)), line(seg(12, 9.5, 21.5, 9.5)), line(seg(12, 14, 21.5, 14)),
            dot(17.5, 5, 1.6), dot(19, 9.5, 1.6), dot(15.5, 14, 1.6)]


@icon("spring-scale", CAT, "Hanging tube scale with tick marks, a hook at the bottom and a weight pulling it down.",
      tags=["force meter", "newton meter", "dynamometer", "physics", "weighing", "lab", "measure force"])
def _(S):
    return [line(seg(12, 2.5, 12, 5)),
            shell(rect(7.5, 5, 9, 10.5, rr(S, 2))),
            detail(seg(10, 8.5, 14, 8.5)), detail(seg(10, 12, 14, 12)),
            line(seg(12, 15.5, 12, 18)),
            shell(poly([(9, 18), (15, 18), (16.5, 21.5), (7.5, 21.5)], closed=True, r=S.r * 0.5))]


@icon("calibration-weight", CAT, "Stubby metal test weight with a knob on top and a smaller one beside it.",
      tags=["test weight", "standard mass", "scale calibration", "weighing", "metrology", "lab", "kilogram"])
def _(S):
    big = union(rect(3, 12, 9.5, 9.5, rr(S, 2)), rect(5.5, 7.5, 4.5, 5, rr(S, 2)))
    small = union(rect(16.5, 16, 5, 5.5, rr(S, 1.5)), rect(18, 13.5, 2, 3, 0))
    return [shell(big), shell(small), detail(seg(5.5, 16.5, 10, 16.5))]


# ============================================================================ reactions and bonds

def shine(S, cx, cy, r):
    """Rounded only: a small highlight dot inside a ring."""
    return [dot(cx - r * 0.3, cy - r * 0.3, 0.9)] if S.name == "rounded" and r >= 4.5 else []


@icon("chemical-reaction", CAT, "Two small particles with an arrow pointing to one larger combined particle.",
      tags=["reaction", "reactants", "products", "synthesis", "chemistry", "combine", "equation"])
def _(S):
    prod = poly(regular(18.5, 12, 4.5, 6, -90), closed=True, r=S.r * 1.2) if S.name == "line" else circle(18.5, 12, 4.5)
    return [shell(circle(5, 7, 2.5)), shell(circle(5, 17, 2.5)),
            line(seg(9.5, 12, 13, 12)), line(poly([(11.2, 10), (13.2, 12), (11.2, 14)], r=S.r * 0.5)), shell(prod)]


@icon("reversible-reaction", CAT, "Two half-headed arrows stacked and pointing in opposite directions, the sign for an equilibrium.",
      tags=["equilibrium", "reversible", "back and forth", "chemistry", "reaction arrows", "harpoon arrows", "dynamic equilibrium"])
def _(S):
    return [line(seg(3, 9, 21, 9)), line(seg(21, 9, 16.5, 4.5)), line(seg(21, 15, 3, 15)), line(seg(3, 15, 7.5, 19.5))]


@icon("covalent-bond", CAT, "Two overlapping atoms sharing a pair of electrons in the lens where they meet.",
      tags=["shared electrons", "electron pair", "bond", "chemistry", "atoms", "molecule", "bonding"])
def _(S):
    r = L(S, 6.5, 6.8)
    return [shell(circle(8, 12, r)), shell(circle(16, 12, r)), dot(12, 9.8, 1.1), dot(12, 14.2, 1.1)] + \
           ([dot(8, 12, 0.9), dot(16, 12, 0.9)] if S.name == "rounded" else [])


@icon("ionic-bond", CAT, "A small positive ion touching a larger negative ion, each marked with its charge sign.",
      tags=["ions", "cation", "anion", "salt", "charge", "chemistry", "electrostatic"])
def _(S):
    return [shell(circle(7, 12, 4)), shell(circle(16.5, 12, 5.5)),
            line(seg(5.2, 12, 8.8, 12)), line(seg(7, 10.2, 7, 13.8)), line(seg(14, 12, 19, 12))]


@icon("hydrogen-bond", CAT, "Two water molecules with a dotted link between a hydrogen of one and the oxygen of the other.",
      tags=["water bonding", "intermolecular", "dipole", "chemistry", "molecules", "attraction", "cohesion"])
def _(S):
    h = L(S, 1.4, 1.8)
    return [shell(circle(6.5, 15, L(S, 3, 3.3))), dot(11.7, 12.9, h), dot(3.3, 10.4, h),
            shell(circle(18, 8, L(S, 3, 3.3))), dot(20.7, 13.2, h), dot(15, 13.4, h),
            dot(13.7, 11.2, 0.6), dot(14.3, 10.2, 0.6)]


@icon("crystal-lattice", CAT, "Cube of atoms joined by rods in a repeating three-dimensional grid.",
      tags=["unit cell", "crystal structure", "solid state", "chemistry", "materials", "atoms", "cubic lattice"])
def _(S):
    f = [(4.5, 9.5), (15, 9.5), (15, 20), (4.5, 20)]
    b = [(9.5, 4.5), (20, 4.5), (20, 15), (9.5, 15)]
    return [line(poly(f, closed=True, r=S.r)), line(poly(b, closed=True, r=S.r)),
            line(seg(4.5, 9.5, 9.5, 4.5)), line(seg(15, 9.5, 20, 4.5)), line(seg(15, 20, 20, 15)), line(seg(4.5, 20, 9.5, 15))] + \
           [Part("dot", rect(x - 1.7, y - 1.7, 3.4, 3.4)) if S.name == "line" else dot(x, y, 1.9) for x, y in f + b]


@icon("water-molecule", CAT, "One large oxygen ball with two small hydrogen balls attached at an angle, like a mouse head.",
      tags=["h2o", "water", "molecule", "chemistry", "oxygen", "hydrogen", "ball model"])
def _(S):
    return [shell(circle(12, 14, 5.5)), shell(circle(4.8, 6.5, 2.8)), shell(circle(19.2, 6.5, 2.8))] + shine(S, 12, 14, 5.5)


@icon("carbon-dioxide-molecule", CAT, "Three touching balls in a straight line, a carbon between two oxygens.",
      tags=["co2", "carbon dioxide", "molecule", "greenhouse gas", "chemistry", "linear molecule", "emissions"])
def _(S):
    a, b = L(S, 3.2, 3.7), L(S, 2.8, 3.2)
    return [shell(circle(5.2, 12, a)), shell(circle(12, 12, b)), shell(circle(18.8, 12, a))]


@icon("methane-molecule", CAT, "Central carbon ball with four small hydrogen balls on sticks spread in a tetrahedron.",
      tags=["ch4", "methane", "tetrahedral", "molecule", "chemistry", "natural gas", "hydrocarbon"])
def _(S):
    c = (12, 12)
    hs = [(12, 3.5), (4.6, 16.3), (19.4, 16.3), (12, 20)]
    out = [shell(circle(12, 12, 3))]
    for x, y in hs:
        d = math.hypot(x - c[0], y - c[1])
        ux, uy = (x - c[0]) / d, (y - c[1]) / d
        out.append(line(seg(c[0] + ux * 4, c[1] + uy * 4, x - ux * 2, y - uy * 2)))
        out.append(dot(x, y, 1.8))
    return out


# ============================================================================ nanostructures and biomolecules

def hex_pts(cx, cy, R):
    return [polar(cx, cy, R, -90 + 60 * k) for k in range(6)]


def hex_cluster(centers, R):
    """Outer boundary (ordered) and interior edges of a cluster of pointy-top hexagons."""
    key = lambda p: (round(p[0], 2), round(p[1], 2))
    edges = {}
    for c in centers:
        v = hex_pts(c[0], c[1], R)
        for i in range(6):
            a, b = v[i], v[(i + 1) % 6]
            k = frozenset((key(a), key(b)))
            edges.setdefault(k, []).append((a, b))
    outer = [e[0] for e in edges.values() if len(e) == 1]
    inner = [e[0] for e in edges.values() if len(e) == 2]
    nxt = {key(a): (a, b) for a, b in outer}
    a, b = outer[0]
    ring = [a]
    while key(b) != key(a):
        ring.append(b)
        b = nxt[key(b)][1]
    return ring, inner


@icon("buckyball", CAT, "Round cage of hexagons and pentagons like a soccer ball, built around a central pentagon.",
      tags=["fullerene", "c60", "carbon", "soccer ball molecule", "nanotechnology", "chemistry", "molecule"])
def _(S):
    pent = regular(12, 12, 3.4, 5, -90)
    out = [shell(circle(12, 12, 9)), detail(poly(pent, closed=True, r=S.r))]
    for p in pent:
        d = math.hypot(p[0] - 12, p[1] - 12)
        out.append(detail(seg(p[0], p[1], 12 + (p[0] - 12) / d * 9, 12 + (p[1] - 12) / d * 9)))
    return out


@icon("graphene-sheet", CAT, "Patch of a honeycomb sheet made of joined carbon hexagons.",
      tags=["graphene", "carbon sheet", "honeycomb lattice", "2d material", "nanotechnology", "chemistry", "materials science"])
def _(S):
    R = 4.5
    cs = [(8.1, 8.2), (15.9, 8.2), (12, 14.95)]
    ring, inner = hex_cluster(cs, R)
    return [shell(poly(ring, closed=True, r=S.r))] + [detail(seg(a[0], a[1], b[0], b[1])) for a, b in inner]


@icon("carbon-nanotube", CAT, "Slanted open tube whose wall is a mesh of hexagons.",
      tags=["nanotube", "cnt", "carbon", "nanotechnology", "cylinder", "materials science", "chemistry"])
def _(S):
    r = lambda d: rot(d, 40, 12, 12)
    body = union(rect(7.5, 4.5, 9, 15, 0), ellipse(12, 19.5, 4.5, L(S, 2, 2.6)))
    z1 = poly([(7.5, 10), (9.75, 11.5), (12, 10), (14.25, 11.5), (16.5, 10)])
    z2 = poly([(7.5, 16.5), (9.75, 15), (12, 16.5), (14.25, 15), (16.5, 16.5)])
    return [shell(r(body)), detail(r(ellipse(12, 4.5, 4.5, 2))), detail(r(z1), stroke_miterlimit="1.5"), detail(r(z2), stroke_miterlimit="1.5"),
            detail(r(seg(9.75, 11.5, 9.75, 15))), detail(r(seg(14.25, 11.5, 14.25, 15)))]


@icon("polymer-chain", CAT, "Zigzag chain of linked beads with a bracket over the repeating unit.",
      tags=["polymer", "macromolecule", "monomer", "repeat unit", "plastic", "chemistry", "chain molecule"])
def _(S):
    pts = [(3, 16), (7.5, 10), (12, 16), (16.5, 10), (21, 16)]
    return [line(poly(pts, r=S.r)), line(poly([(7.5, 6.5), (7.5, 3.5), (16.5, 3.5), (16.5, 6.5)], r=S.r))] + \
           [dot(x, y, 2) for x, y in pts]


@icon("protein-structure", CAT, "Coiled ribbon helix on the left flowing into a flat arrow-shaped sheet on the right.",
      tags=["alpha helix", "beta sheet", "protein folding", "biochemistry", "amino acids", "biology", "secondary structure"])
def _(S):
    n = 40
    pts = []
    for i in range(n + 1):
        t = i / n * 3.6 * math.pi
        pts.append((3.5 + 0.9 * t - 2.8 * math.sin(t), 12 - 4.5 * math.cos(t)))
    return [line(poly(pts)), shell(poly([(14.5, 9.5), (17.5, 9.5), (17.5, 6), (22, 12), (17.5, 18), (17.5, 14.5), (14.5, 14.5)],
                                          closed=True, r=S.r))]


@icon("lipid-bilayer", CAT, "Two rows of round heads with wavy tails pointing toward each other, like a cell membrane.",
      tags=["cell membrane", "phospholipid", "membrane", "biology", "cell", "biochemistry", "amphipathic"])
def _(S):
    out = []
    for x in (5.5, 12, 18.5):
        out += [dot(x, 4.5, L(S, 2.3, 2.8)), line(seg(x, 8, x, 10.8)),
                dot(x, 19.5, L(S, 2.3, 2.8)), line(seg(x, 16, x, 13.2))]
    return out


@icon("enzyme", CAT, "Round protein with a wedge-shaped notch and a small wedge-shaped molecule fitting toward it.",
      tags=["active site", "substrate", "lock and key", "catalyst", "biochemistry", "protein", "biology"])
def _(S):
    cx, cy, R = 9.5, 12, 8
    a, b = polar(cx, cy, R, -35), polar(cx, cy, R, 35)
    pac = f"M{fmt(cx)} {fmt(cy)}L{fmt(a[0])} {fmt(a[1])}A{R} {R} 0 1 0 {fmt(b[0])} {fmt(b[1])}Z"
    return [shell(pac, stroke_miterlimit="3"), shell(poly([(21.5, 8.8), (21.5, 15.2), (15, 12)], closed=True, r=S.r))]


def particle(S, x, y):
    return Part("dot", rect(x - 1, y - 1, 2, 2)) if S.name == "line" else dot(x, y, 1.05)


@icon("states-of-matter", CAT, "Three bands of dots: tightly packed, loosely spaced and widely scattered.",
      tags=["solid liquid gas", "particles", "phases of matter", "physics", "chemistry", "kinetic theory", "density"])
def _(S):
    solid_ = [(5 + 2.5 * k, 5.2) for k in range(7)] + [(6.25 + 2.5 * k, 7.4) for k in range(6)]
    liquid = [(5.5, 11.8), (9.2, 13.5), (13, 11.8), (16.8, 13.5), (20, 12)]
    gas = [(6, 18.2), (11, 19.6), (15.5, 17.8), (19.5, 19.4)]
    return [shell(rect(2.5, 2.5, 19, 19, rr(S, 3))), detail(seg(2.5, 9.5, 21.5, 9.5)), detail(seg(2.5, 15.5, 21.5, 15.5))] + \
           [particle(S, x, y) for x, y in solid_ + liquid + gas]


@icon("filtration", CAT, "Funnel holding a filter paper over a flask, with a drop falling from the stem.",
      tags=["filter", "separation", "filtering", "chemistry", "lab", "residue", "filtrate"])
def _(S):
    fun = poly([(3.5, 2.5), (20.5, 2.5), (13.5, 9), (13.5, 11), (10.5, 11), (10.5, 9)], closed=True, r=S.r * 0.6)
    fl = poly([(9.5, 16), (14.5, 16), (14.5, 17.5), (19.5, 21.5), (4.5, 21.5), (9.5, 17.5)], closed=True, r=S.r * 0.6)
    return [shell(fun), shell(fl), drop(12, 12.2, 2.0, 2.8)]


@icon("evaporation", CAT, "Water surface with three wavy vapor lines rising and ending in arrowheads.",
      tags=["vapor", "vaporization", "water cycle", "drying", "phase change", "physics", "chemistry"])
def _(S):
    out = [line("M2.5 18.5C5 16.5 7.5 20.5 10 18.5S15 16.5 17.5 18.5S20 19.5 21.5 18.5"),
           line("M2.5 21.5C5 19.5 7.5 23 10 21.5S15 19.5 17.5 21.5S20 22.5 21.5 21.5")] if False else \
          [line("M2.5 18C5 16 7.5 20 10 18S15 16 17.5 18S20 19 21.5 18")]
    for x in (6, 12, 18):
        out += [line(wave_d(x, 14, 6, 1.0)), line(poly([(x - 2.2, 6.5), (x, 4), (x + 2.2, 6.5)], r=S.r * 0.5))]
    return out


@icon("condensation", CAT, "Cold drinking glass beaded with water droplets, one of them running down.",
      tags=["water droplets", "dew", "cold glass", "humidity", "phase change", "physics", "chemistry"])
def _(S):
    glass = poly([(5.5, 3.5), (18.5, 3.5), (17, 21), (7, 21)], closed=True, r=S.r)
    return [shell(glass), drop(9.5, 6.5, 2.2, 3.2), drop(14.5, 8.5, 2.2, 3.2), drop(9.5, 13, 2.2, 3.2),
            line(seg(14.2, 13, 14.2, 15.5)), dot(14.2, 17.2, 1.2)]


@icon("electrolysis", CAT, "Beaker with two electrodes wired to a battery and bubbles rising from each.",
      tags=["electrodes", "electrolytic cell", "splitting water", "chemistry", "battery", "electrochemistry", "bubbles"])
def _(S):
    return [line(poly([(3.5, 12), (3.5, 20.5), (20.5, 20.5), (20.5, 12)], r=S.r)),
            line(seg(8, 7, 8, 17.5)), line(seg(16, 7, 16, 17.5)),
            line(poly([(8, 7), (8, 4), (10, 4)])), line(seg(10, 2, 10, 6)),
            line(seg(14, 3, 14, 5)), line(poly([(14, 4), (16, 4), (16, 7)])),
            dot(5.8, 16, 0.9), dot(12, 14, 0.9), dot(12.5, 17.5, 0.9), dot(18.2, 16, 0.9)]


@icon("voltaic-pile", CAT, "Stack of flat metal discs with a wire leaving the top disc on one side and the bottom disc on the other.",
      tags=["voltaic cell", "volta", "early battery", "stacked cells", "electrochemistry", "physics", "history of science"])
def _(S):
    return [shell(rect(6, 4.5, 12, 3, rr(S, 1))), shell(rect(6, 10.5, 12, 3, rr(S, 1))), shell(rect(6, 16.5, 12, 3, rr(S, 1))),
            line(poly([(18, 6), (21.5, 6)])), line(poly([(6, 18), (2.5, 18)]))]


@icon("lemon-battery", CAT, "Lemon with two wires pushed into it and a small light bulb above, the classic fruit battery experiment.",
      tags=["fruit battery", "citrus battery", "science experiment", "electricity", "school project", "lemon", "stem"])
def _(S):
    nub = poly([(17.5, 13.8), (21, 16.5), (17.5, 19.2)], closed=True, r=S.r * 1.5)
    lemon = union(ellipse(11, 16.5, 8.5, 5.2), nub)
    return [shell(circle(11, 5, 3)), line(poly([(9.8, 8), (9.8, 9.5), (6.5, 9.5), (6.5, 14)])),
            line(poly([(12.2, 8), (12.2, 9.5), (15.5, 9.5), (15.5, 14)])), shell(lemon)]


@icon("element-tile", CAT, "Square periodic table tile with a large letter symbol, a small number in the corner and a bar for the mass.",
      tags=["periodic table", "chemical element", "atomic number", "chemistry", "symbol", "elements", "tile"])
def _(S):
    return [shell(rect(3, 2.5, 18, 19, rr(S, 3))), detail(seg(6.3, 5.5, 6.3, 8.2)),
            detail(arc(12, 11.8, 3.6, 45, 315)), detail(seg(9, 18.2, 15, 18.2))]


# ============================================================================ phenomena and indicators

@icon("chirality", CAT, "Two mirror-image molecules with different attachments, facing each other across a dashed line.",
      tags=["handedness", "enantiomers", "mirror image", "stereochemistry", "optical isomers", "chemistry", "chiral"])
def _(S):
    out = [line(seg(12, 2.5, 12, 5.5)), line(seg(12, 9.5, 12, 13.5)), line(seg(12, 17.5, 12, 21.5))]
    subs = [((7.5, 4.5), 1.9), ((2.8, 16.5), 1.3), ((9.5, 19), 1.6)]
    for mirror in (False, True):
        f = (lambda x: 24 - x) if mirror else (lambda x: x)
        out.append(shell(circle(f(7), 11.5, 2.4)))
        for (x, y), r in subs:
            d = math.hypot(x - 7, y - 11.5)
            ux, uy = (x - 7) / d, (y - 11.5) / d
            out.append(line(seg(f(7 + ux * 3.4), 11.5 + uy * 3.4, f(x - ux * r * 0.8), y - uy * r * 0.8)))
            out.append(dot(f(x), y, r + L(S, 0, 0.25)))
    return out


@icon("fire-triangle", CAT, "Triangle with a flame in the middle, the model of heat, fuel and oxygen needed for a fire.",
      tags=["combustion", "fire safety", "heat fuel oxygen", "fire prevention", "chemistry", "flame", "burning"])
def _(S):
    return [shell(poly([(12, 2.5), (21.5, 20), (2.5, 20)], closed=True, r=S.r)),
            detail(flame_d(12, 17, 8, 5.4))]


@icon("flame-test", CAT, "Wire loop holding a sample in the flame above a burner barrel.",
      tags=["flame colour", "flame color", "metal ions", "qualitative analysis", "chemistry", "lab", "nichrome wire"])
def _(S):
    return [shell(rect(7.5, 19.5, 9, 2.5, rr(S, 1))), shell(flame_d(12, 18, 14, 9.5)),
            detail(poly([(21.5, 3.5), (14, 10.5)])), detail(circle(12.6, 11.8, 1.8))]


@icon("litmus-paper", CAT, "Thin paper test strip with a darker dipped end, beside a drop of liquid.",
      tags=["ph paper", "test strip", "acid base indicator", "indicator paper", "chemistry", "lab", "ph test"])
def _(S):
    return [shell(rect(4.5, 2.5, 6.5, 18, rr(S, 1.5))), detail(seg(4.5, 11, 11, 11)), solid(rect(5.7, 12.4, 4.1, 6.6)) if False else detail(seg(6.5, 14.5, 9, 14.5)),
            shell(drop_d(17.5, 6, 6.5, 10.5))]


@icon("ph-scale", CAT, "Horizontal colour bar with dividers and a pointer above the neutral middle.",
      tags=["acidity", "alkalinity", "acid base", "neutral", "ph", "chemistry", "indicator scale"])
def _(S):
    return [shell(rect(2.5, 11.5, 19, 8, rr(S, 2))), detail(seg(7.25, 11.5, 7.25, 19.5)), detail(seg(16.75, 11.5, 16.75, 19.5)),
            solid(poly([(8.5, 3), (15.5, 3), (12, 8.5)], closed=True, r=S.r * 0.5))]


@icon("ph-meter", CAT, "Handheld meter with a small display and buttons, its probe on a cord dipped in a beaker.",
      tags=["ph probe", "acidity meter", "digital ph", "electrode", "chemistry", "lab", "water testing"])
def _(S):
    return [shell(rect(2.5, 2.5, 8.5, 15, rr(S, 2))), detail(rect(4.5, 4.5, 4.5, 4)), dot(5, 13, 1), dot(8.5, 13, 1),
            line(poly([(11, 5), (17.5, 5), (17.5, 14.5)])), dot(17.5, 16.5, 1.6),
            line(poly([(13.5, 13), (13.5, 21), (21.5, 21), (21.5, 13)], r=S.r))]


@icon("precipitate", CAT, "Test tube of liquid with a layer of grains settled at the bottom and specks still falling.",
      tags=["sediment", "solid formation", "settling", "chemical test", "chemistry", "lab", "test tube"])
def _(S):
    tube = union(rect(7, 2.5, 10, 14, rr(S, 1)), circle(12, 16, 5))
    return [shell(tube), dot(10.3, 8.5, 0.9), dot(13.8, 11, 0.9), dot(11, 13.5, 0.9),
            dot(9.8, 17.8, 1), dot(13.5, 17.2, 1), dot(11.8, 19.2, 0.8)]


@icon("effervescence", CAT, "Beaker of fizzing liquid with bubbles rising inside and bursting above the rim.",
      tags=["fizzing", "bubbles", "gas release", "carbonation", "chemical reaction", "chemistry", "lab"])
def _(S):
    return [line(poly([(4.5, 9), (4.5, 20.5), (19.5, 20.5), (19.5, 9)], r=S.r)),
            line("M4.5 12.5C7 11 9.5 14 12 12.5S17 11 19.5 12.5"),
            dot(9, 17, 1.1), dot(14, 16, 1.2), dot(11.5, 19, 0.8), dot(16, 19, 0.8),
            dot(8, 5, 1.3), dot(12.5, 3.2, 1.3), dot(16, 6, 1.1), dot(11, 7.5, 0.9)]
