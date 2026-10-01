"""TypeIcon Core: birds (batch 002).

Songbirds and crows, bird behaviour, nests and eggs, bird anatomy, and the things people build for birds
(houses, feeders, baths, falconry gear). Birds face left in side view unless the scene needs otherwise.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import LINE, D, I, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "birds"


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


def rotd(d, deg, cx=12, cy=12):
    """Rotate any d-string (open or closed) without turning open strokes into regions."""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.svgLib.path import parse_path
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, rotation(deg, cx, cy)))
    return pen.getCommands()


def rpts(pts, deg, cx=12, cy=12):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def thick(d, w, S):
    """Outline of a stroke of width w along d (necks, tails, legs inside a silhouette)."""
    return path_to_d(ST(d, w, S.cap, S.join))


def flip(d):
    """Mirror a d-string across the vertical centre line."""
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def fpts(pts):
    return [(24 - x, y) for x, y in pts]


def grow(d, g):
    """Region d expanded by g px (cuts clean gaps between overlapping parts)."""
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


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


def tri(S, pts, r=0.8):
    """Closed polygon with sharp corners in Line and softened corners in Rounded (beaks, tails, crests)."""
    return poly(pts, closed=True, r=L(S, 0, r))


def ground(y=21, x0=2.5, x1=21.5):
    return line(seg(x0, y, x1, y))


def mini_bird(x, y, s=1.0, S=None):
    """Small flying-bird mark (two raised wings) centred at x, y: a sharp V in Line, soft gull curves in Rounded."""
    w, h = 2.8 * s, 1.3 * s
    return line(f"M{fmt(x - w)} {fmt(y + h * 0.1)}Q{fmt(x - w * 0.5)} {fmt(y - h * 1.6)} {fmt(x)} {fmt(y + h * 0.5)}"
                f"Q{fmt(x + w * 0.5)} {fmt(y - h * 1.6)} {fmt(x + w)} {fmt(y + h * 0.1)}")


def perch_bird(S, hx, hy, hr=2.3, body=(0, 0, 3, 4.2, 30), bill=None, tail=None):
    """Perched songbird parts: head circle, body ellipse (dx, dy, rx, ry, tilt from head), bill and tail polygons."""
    dx, dy, rx, ry, tilt = body
    cx, cy = hx + dx, hy + dy
    parts = [circle(hx, hy, hr), rot(ellipse(cx, cy, rx, ry), -tilt, cx, cy)]
    if bill:
        parts.append(tri(S, bill, 0.3))
    if tail:
        parts.append(tri(S, tail, 0.7))
    return union(*parts)


def xf(d, x, y, s=1.0, mirror=False):
    """Scale a local d-string by s (mirrored left-right when asked) and move its origin to x, y."""
    return path_to_d(transform_path(P(d), (-s if mirror else s, 0, 0, s, x, y)))


def xpt(px, py, x, y, s=1.0, mirror=False):
    return (x + (-px if mirror else px) * s, y + py * s)


def songbird(S, x, y, s=1.0, mirror=False, open_bill=False):
    """Small perched songbird facing left (right when mirrored); origin at the body centre. Returns (d, eye)."""
    parts = [circle(-3.2, -3, 2.3), rot(ellipse(0.3, 0.4, 4, 2.9), 20, 0.3, 0.4),
             tri(S, [(2.6, 1), (6.8, 4), (3.2, 3.4)], 0.6)]
    if open_bill:
        parts += [tri(S, [(-5.1, -4), (-7.6, -4.4), (-5.3, -3)], 0.2), tri(S, [(-5.2, -2.3), (-7.2, -1), (-4.8, -1.5)], 0.2)]
    else:
        parts.append(tri(S, [(-5.2, -3.7), (-7.3, -2.6), (-5, -1.8)], 0.3))
    return xf(union(*parts), x, y, s, mirror), xpt(-3.3, -3.4, x, y, s, mirror)


def flyer(S, x, y, s=1.0, mirror=False):
    """Bird in flight in side view with both wings raised, facing left; origin at the body centre. Returns (d, eye)."""
    r = L(S, 0, 0.8)
    d = union(rot(ellipse(0.5, 3, 5, 2.4), -8, 0.5, 3), circle(-5.2, 1.2, 2.2),
              tri(S, [(-6.9, 0.4), (-9.4, 1.6), (-6.9, 2.6)], 0.3),
              tri(S, [(4.5, 2.2), (9.4, 0.6), (8.6, 4), (4.8, 4.6)], 0.6),
              poly([(-2.4, 2.2), (-4.8, -9), (1.8, -2), (1.5, 1.5)], closed=True, r=r),
              poly([(0.5, 0.8), (7.8, -8.8), (6.6, -2.2), (3.8, 1.5)], closed=True, r=r))
    return xf(d, x, y, s, mirror), xpt(-5.1, 0.7, x, y, s, mirror)


def leaf(cx, cy, length, width, deg, S):
    """Pointed leaf (lens) centred at cx, cy, rotated deg; tips softened in Rounded."""
    h, w = length / 2, width / 2
    k = L(S, 0, 0.35)
    d = (f"M{fmt(-h)} {fmt(k)}Q{fmt(-h * 0.2)} {fmt(-w * 1.9)} {fmt(h)} {fmt(-k)}"
         f"L{fmt(h)} {fmt(k)}Q{fmt(h * 0.2)} {fmt(w * 1.9)} {fmt(-h)} {fmt(-k)}Z") if k else (
         f"M{fmt(-h)} 0Q{fmt(-h * 0.2)} {fmt(-w * 1.9)} {fmt(h)} 0Q{fmt(h * 0.2)} {fmt(w * 1.9)} {fmt(-h)} 0Z")
    return rot(xf(d, cx, cy), deg, cx, cy)


EGG = "M0 -5.5C2.9 -5.5 4.4 -1.2 4.4 1.6C4.4 4.2 2.5 5.8 0 5.8C-2.5 5.8 -4.4 4.2 -4.4 1.6C-4.4 -1.2 -2.9 -5.5 0 -5.5Z"


def egg(x, y, s=1.0, deg=0.0):
    """Egg outline, pointed end up, centred at x, y (height about 11.3 * s)."""
    d = xf(EGG, x, y, s)
    return rot(d, deg, x, y) if deg else d


def zig(S, x0, x1, y, n=4, a=1.1):
    """Jagged crack line points from x0 to x1 around height y."""
    pts = []
    for i in range(n * 2 + 1):
        pts.append((x0 + (x1 - x0) * i / (n * 2), y + (a if i % 2 else -a) * (1 if i % 4 < 2 else 0.8)))
    return pts


def nest_bowl(S, x0=2.5, x1=21.5, top=12.5, bottom=21.3):
    """Side view of a woven nest bowl; returns the shell d."""
    cx = (x0 + x1) / 2
    k = L(S, 0.6, 1.2)
    return (f"M{fmt(x0 + k)} {fmt(top)}L{fmt(x1 - k)} {fmt(top)}Q{fmt(x1)} {fmt(top)} {fmt(x1 - 0.1)} {fmt(top + 1)}"
            f"C{fmt(x1 - 0.8)} {fmt(bottom - 2)} {fmt(cx + (x1 - x0) * 0.25)} {fmt(bottom)} {fmt(cx)} {fmt(bottom)}"
            f"C{fmt(cx - (x1 - x0) * 0.25)} {fmt(bottom)} {fmt(x0 + 0.8)} {fmt(bottom - 2)} {fmt(x0 + 0.1)} {fmt(top + 1)}"
            f"Q{fmt(x0)} {fmt(top)} {fmt(x0 + k)} {fmt(top)}Z")


def weave(x0, x1, y0, y1):
    """Curved twig lines inside a nest bowl, following its shape (x0..x1 at the first line, y0 and y1 their heights)."""
    cx, w = (x0 + x1) / 2, (x1 - x0) / 2
    return [detail(f"M{fmt(x0)} {fmt(y0)}C{fmt(cx - w * 0.5)} {fmt(y0 + 1.4)} {fmt(cx + w * 0.5)} {fmt(y0 + 1.4)} {fmt(x1)} {fmt(y0)}"),
            detail(f"M{fmt(x0 + 2.5)} {fmt(y1)}C{fmt(cx - w * 0.3)} {fmt(y1 + 1)} {fmt(cx + w * 0.3)} {fmt(y1 + 1)} {fmt(x1 - 2.5)} {fmt(y1)}")]


def sparkle(S, x, y, r):
    k = r * 0.28
    pts = [(x, y - r), (x + k, y - k), (x + r, y), (x + k, y + k), (x, y + r), (x - k, y + k), (x - r, y), (x - k, y - k)]
    return mark(poly(pts, closed=True, r=L(S, 0, 0.2)))


def zee(S, x, y, w):
    return line(poly([(x, y), (x + w, y), (x, y + w), (x + w, y + w)], r=L(S, 0, min(0.6, w / 4))))


def note_pair(S, x1, y1, x2, y2, top1, top2):
    """Two beamed music notes: heads at (x1, y1) and (x2, y2), stems rising to top1 and top2."""
    h1 = rot(ellipse(x1, y1, 1.6, 1.2), -20, x1, y1)
    h2 = rot(ellipse(x2, y2, 1.6, 1.2), -20, x2, y2)
    sx1, sx2 = x1 + 1.1, x2 + 1.1
    beam = poly([(sx1 - 0.4, top1 - 0.9), (sx2 + 0.4, top2 - 0.9), (sx2 + 0.4, top2 + 1.1), (sx1 - 0.4, top1 + 1.1)], closed=True)
    return [mark(h1), mark(h2), line(seg(sx1, y1 - 0.4, sx1, top1)), line(seg(sx2, y2 - 0.4, sx2, top2)), solid(beam)]


# ============================================================================ songbirds, pigeons and crows

@icon("carrier-pigeon", CAT, "Pigeon standing in side view with a small message tube strapped to its leg",
      tags=["homing pigeon", "messenger", "pigeon post", "message", "delivery", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = ("M8.8 9.6C11 8.6 14.5 8.8 16.5 10.2" + tip((16.5, 10.2), (21.4, 12.8), (17, 14.3), r)
            + "L17 14.3C15.5 16.3 12.5 16.8 10.5 16.1C7.8 15.2 6.6 12.3 8.8 9.6Z")
    head = circle(7.2, 6.8, 2.5)
    neck = thick("M7.6 8L8.8 11", 3.4, S)
    bill = tri(S, [(4.9, 6.2), (2.6, 7.3), (4.9, 8.1)], 0.3)
    return [shell(union(body, head, neck, bill)), dot(7.3, 6.3, 0.8), detail("M10.8 12.2C12.8 13.6 15.2 13.8 17.6 12.9"),
            line(seg(10.8, 16.2, 10.8, 21)), line(seg(13.8, 16.3, 13.8, 17.3)), line(seg(13.8, 20.3, 13.8, 21)),
            shell(rect(12.8, 17.3, 6.5, 3, min(S.R, 1.5)))]


@icon("crowned-pigeon", CAT, "Large pigeon in side view with a lacy fan-shaped crest on its head",
      tags=["victoria crowned pigeon", "crest", "new guinea", "fan crest", "pigeon", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = ("M8.8 13.2C11 11.8 15 11.8 17.2 13.2" + tip((17.2, 13.2), (21.4, 15.5), (17.6, 17), r)
            + "L17.6 17C16 18.6 12.5 18.9 10.5 18.2C8 17.3 7 15.2 8.8 13.2Z")
    head = circle(7.5, 11.5, 2.3)
    bill = tri(S, [(5.4, 11), (3, 12), (5.4, 12.6)], 0.3)
    c = (8, 10)
    angs = (-150, -118, -86, -54, -22)
    rays = [line(seg(*pt_on(c[0], c[1], 2.4, a), *pt_on(c[0], c[1], 5.4, a))) for a in angs]
    tips = [dot(*pt_on(c[0], c[1], 6.4, a), 1.15) for a in angs]
    return [shell(union(body, head, bill)), dot(7.4, 11.1, 0.75), *rays, *tips,
            detail("M11 15C13 16.2 15.5 16.2 17.8 15.3"), line(seg(11.5, 18.4, 11.5, 21.3)), line(seg(14.5, 18.5, 14.5, 21.3))]


@icon("swallow", CAT, "Swallow in flight seen from above with swept-back pointed wings and a long forked tail",
      tags=["barn swallow", "martin", "spring", "summer", "migration", "bird"])
def _(S):
    r = L(S, 0, 0.6)
    wl = ("M10.8 7.6C8 7.6 6 8.5 4.5 9.8" + tip((4.5, 9.8), (2.4, 15.2), (5.5, 12.6), r)
          + "L5.5 12.6C7.2 11.4 9 11 10.8 11.2Z")
    tail = [(10.9, 12), (13.1, 12), (13.4, 14.2), (16.4, 21.4), (12, 15.8), (7.6, 21.4), (10.6, 14.2)]
    head = "M10.3 6.2C10.3 3.6 13.7 3.6 13.7 6.2L13.8 9L10.2 9Z"
    body = union(ellipse(12, 9.3, 1.9, 3.6), head, wl, flip(wl), poly(tail, closed=True, r=L(S, 0, 0.4)))
    return [shell(body, stroke_miterlimit="2.5")]


@icon("cardinal-bird", CAT, "Cardinal perched on a twig with a tall pointed crest, a dark face mask and a thick cone bill",
      tags=["northern cardinal", "redbird", "songbird", "winter", "backyard", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    head = circle(8.5, 8.6, 3)
    crest = tri(S, [(6.6, 6.6), (9.8, 3), (11.4, 7.4)], 0.6)
    bill = tri(S, [(6, 7.5), (3, 9.3), (6.2, 11.1)], 0.5)
    body = ("M6.8 10.5C6 14.5 8 17 11.3 17.6" + tip((11.3, 17.6), (15.5, 21.2), (15.3, 16.3), r)
            + "L15.3 16.3C16.5 12.5 14.5 9 11 8.5Z")
    mask = poly([(5.2, 7.2), (8, 7.4), (8.3, 9.5), (7.2, 11.6), (5.4, 11)], closed=True, r=L(S, 0, 0.5))
    return [shell(union(head, crest, bill, body)), mark(mask), detail("M10 12C10.2 14 11.3 15.3 13 16"),
            line(seg(4.5, 18.5, 20.5, 18.5))]


@icon("blue-jay", CAT, "Jay perched in side view with a swept-back crest, a dark necklace and a long barred tail",
      tags=["jay", "crested jay", "songbird", "corvid", "backyard", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    head = circle(7.5, 7.5, 2.6)
    crest = tri(S, [(6.3, 5.3), (12.6, 3), (9.8, 6.8)], 0.6)
    bill = tri(S, [(5.2, 6.9), (2.6, 8), (5.2, 8.9)], 0.3)
    body = rot(ellipse(10.3, 11.3, 3.3, 4.5), -35, 10.3, 11.3)
    tail = poly([(11.5, 13.5), (19.8, 19.6), (18.3, 21.4), (10.3, 15.8)], closed=True, r=r)
    return [shell(union(head, crest, bill, body, tail)), dot(7.5, 7, 0.75), detail("M5.5 9.7C6.6 11 8.3 11.4 10 10.8"),
            detail(seg(14.6, 17.6, 15.9, 16)), detail(seg(16.9, 19.4, 18.1, 17.8)), line(seg(3, 16.3, 11.5, 16.3))]


@icon("crow", CAT, "Crow standing in side view with a thick straight bill, a sleek body and a wedge tail",
      tags=["raven", "rook", "corvid", "blackbird", "halloween", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = ("M7.8 9.8C10.5 9 14.5 9.8 16.5 11.3" + tip((16.5, 11.3), (21.4, 14.6), (19.8, 16.3), r)
            + tip((21.4, 14.6), (19.8, 16.3), (15.5, 15), r)
            + "L15.5 15C13.5 16.5 10.5 16.5 8.8 15.3C7 14 6.5 11.5 7.8 9.8Z")
    head = circle(7, 7.4, 2.6)
    bill = tri(S, [(5, 6.2), (2.6, 7.9), (5.3, 9.3)], 0.4)
    return [shell(union(body, head, bill)), dot(7.4, 6.8, 0.8), detail("M10.3 11.9C12.3 13.2 14.8 13.6 17.3 13.3"),
            line(poly([(10.5, 16), (10.5, 21), (8.5, 21)], r=S.r)), line(poly([(13.5, 16), (13.5, 21), (11.8, 21)], r=S.r))]


@icon("magpie", CAT, "Magpie perched in side view with a pied body and a very long graduated tail",
      tags=["eurasian magpie", "corvid", "black and white", "pied", "thief", "bird"])
def _(S):
    head = circle(5.8, 5.8, 2.3)
    bill = tri(S, [(3.8, 5.3), (2.6, 6.3), (3.9, 6.9)], 0.3)
    body = rot(ellipse(8.8, 9.5, 2.9, 4.3), -35, 8.8, 9.5)
    tail = thick("M10 11.5L20.3 20.3", 2.8, S)
    return [shell(union(head, bill, body, tail)), dot(5.9, 5.3, 0.7), detail("M7.7 7.3C9.6 7.8 10.8 9.2 11 11"),
            line(seg(2.5, 14.8, 12.5, 14.8))]


@icon("oxpecker", CAT, "Small bird perched on the back of a buffalo, pecking at its hide",
      tags=["tickbird", "symbiosis", "savanna", "buffalo", "africa", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    rhino = union(ellipse(15.2, 14.6, 6.3, 3.9),
                  poly([(10.5, 11.6), (6, 12.8), (3, 16.4), (4, 18), (9, 17.4), (11.5, 16.5)], closed=True, r=r),
                  tri(S, [(3.2, 15.4), (3, 10.6), (6, 13.8)], 0.5), tri(S, [(9.8, 12), (9.4, 9.6), (11.4, 11.4)], 0.4))
    bird = union(rot(ellipse(16, 6.8, 2.5, 1.4), -20, 16, 6.8), circle(13.4, 7.4, 1.3),
                 tri(S, [(12.6, 8), (11.9, 9.6), (13.4, 8.7)], 0.2), tri(S, [(18.1, 5.6), (20.8, 4.4), (18.5, 7)], 0.3))
    return [shell(rhino), dot(7, 14.4, 0.7), line(seg(11, 17.5, 11, 21.3)), line(seg(18.8, 17.5, 18.8, 21.3)),
            shell(bird), line(seg(15.8, 8.2, 15.8, 10.2))]


@icon("nuthatch", CAT, "Small stubby bird climbing head first down a tree trunk with a straight chisel bill",
      tags=["nuthatch", "upside down", "tree trunk", "climbing", "woodland", "bird"])
def _(S):
    body = rot(ellipse(11.2, 9.6, 3, 4.8), 25, 11.2, 9.6)
    head = circle(9.2, 14.8, 2.6)
    bill = tri(S, [(7, 14), (3.2, 13.2), (7, 15.6)], 0.3)
    tail = tri(S, [(11.8, 5.5), (14.3, 3.2), (14, 6.6)], 0.4)
    return [shell(union(body, head, bill, tail)), line(seg(18, 2.5, 18, 21.5)), line(seg(21.5, 2.5, 21.5, 21.5)),
            dot(8.6, 14.3, 0.75), line(poly([(13.9, 9.5), (16, 9.5)], r=0)), line(seg(13.4, 12.5, 16, 12.5))]


@icon("bowerbird", CAT, "Small bird beside its bower, an arch of upright twigs, with round trinkets on the ground",
      tags=["satin bowerbird", "courtship", "bower", "australia", "collector", "bird"])
def _(S):
    bird = union(rot(ellipse(6.3, 12.8, 3.3, 2.2), 20, 6.3, 12.8), circle(8.3, 9.8, 1.9),
                 tri(S, [(9.9, 9.2), (11.6, 10), (10, 10.8)], 0.3), tri(S, [(3.6, 13.3), (2.2, 16.8), (5, 14.5)], 0.5))
    return [shell(bird), dot(8.6, 9.4, 0.6), line(seg(6.3, 15, 6.3, 17)),
            line("M12.8 17C12.8 12 14.2 8 17 5.5"), line("M21.2 17C21.2 12 19.8 8 17 5.5"),
            line(seg(15.8, 17, 15.8, 11.5)), line(seg(18.2, 17, 18.2, 11.5)),
            ground(17), dot(3.5, 20.2, 1.1), dot(7.5, 20.2, 1.1), dot(11.5, 20.2, 1.1)]


@icon("crossbill", CAT, "Finch head in side view with the curved tips of its upper and lower bill crossing each other",
      tags=["red crossbill", "finch", "pine cone", "conifer", "crossed bill", "bird"])
def _(S):
    body = union(circle(10.6, 8, 3.4), rot(ellipse(14.6, 12.4, 5, 3.9), 25, 14.6, 12.4),
                 tri(S, [(17.5, 13.8), (21, 18.6), (16.5, 17.4)], 0.8))
    return [shell(body), dot(10.3, 7.3, 0.9), detail("M12.3 13C14 15 16.5 15.8 18.5 15.2"),
            line("M7.6 6.2C5 6.5 3.2 8.6 3 11.8"), line("M7.6 9.8C5 9.5 3.2 7.4 3 4.2"),
            line(seg(13.5, 16.3, 13.5, 19)), line(seg(3, 20, 21, 20))]


@icon("lyrebird", CAT, "Lyrebird in side view with its tail raised and curved into the outline of a lyre",
      tags=["superb lyrebird", "mimic", "australia", "lyre tail", "display", "bird"])
def _(S):
    body = union(ellipse(8.5, 16.3, 3.8, 2.6), circle(4.8, 13.8, 1.9), tri(S, [(3.3, 13.4), (2.5, 14.6), (3.4, 14.8)], 0.2))
    return [shell(body), dot(4.8, 13.4, 0.6), line(seg(7.5, 18.8, 7.5, 21.3)), line(seg(9.8, 18.6, 9.8, 21.3)),
            line("M11.5 15C9.6 11.5 9.8 8 11.5 5.5C12.2 4.4 11.8 3.3 10.5 3.4"),
            line("M12.5 15.8C16.5 14 20.5 10.5 20.8 5.8C20.9 4.3 20 3.3 18.6 3.6"),
            line("M12.8 14.2L14.3 5.8"), line("M13.8 14.8L17.8 6.5")]


@icon("paradise-bird", CAT, "Bird of paradise perched with long lacy flank plumes cascading behind and two thin tail wires",
      tags=["bird of paradise", "new guinea", "plumes", "display", "exotic", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    body = union(rot(ellipse(7.8, 8.4, 2.6, 3.6), -25, 7.8, 8.4), circle(5.6, 4.9, 2.1),
                 tri(S, [(3.8, 4.4), (2.2, 5.5), (3.9, 5.9)], 0.2))
    plumes = ("M9.3 9.6C13.5 8.4 18.5 9.5 21.2 13.5C20 13.5 19.3 13.8 18.8 14.5C17.5 12.9 15.9 12.7 14.8 13.3"
              "C13.5 12.2 11.5 12 10 12.4Z")
    return [shell(body), dot(5.7, 4.4, 0.6), shell(plumes, stroke_miterlimit="2.5"), detail("M12.5 10.3C14.8 10.3 17 11 18.7 12.4"),
            line("M8.8 11.8C9.5 15 9 18 7.5 19.8C6.5 21 5 20.5 5.2 19.2"), line("M10.3 12.5C12.2 15.5 13 18.3 12.5 20.2C12.2 21.3 10.8 21.2 10.8 20"),
            line(seg(2.5, 12.3, 7, 12.3))]


@icon("murmuration", CAT, "Swirling ribbon of many tiny birds flying together in a flowing cloud",
      tags=["starlings", "flock", "swarm", "swirl", "starling murmuration", "birds"])
def _(S):
    pts = [(4.5, 18.5), (6.5, 15), (8.8, 17.8), (8.8, 12.8), (11, 15.5), (11.3, 10.8), (13.5, 13.3), (13.5, 8.8),
           (15.8, 11.3), (15.8, 6.8), (18, 9), (18.2, 4.8), (20.2, 7), (3.2, 15.3), (6.8, 11)]
    return [*[dot(x, y, 1.05) for x, y in pts], mini_bird(19, 14, 0.9, S), mini_bird(5, 7, 0.9, S), mini_bird(14.5, 19.5, 0.9, S)]


@icon("archaeopteryx", CAT, "Feathered prehistoric bird in side view with clawed wings, a toothed jaw and a long feathered tail",
      tags=["dinosaur bird", "fossil", "prehistoric", "jurassic", "paleontology", "bird"])
def _(S):
    r = L(S, 0, 0.6)
    body = union(rot(ellipse(9.8, 11.8, 3.6, 2.4), 25, 9.8, 11.8), circle(5.5, 7.6, 2),
                 poly([(4, 6.6), (2.4, 7.8), (4, 9.2)], closed=True, r=r), thick("M6.5 9.2L7.8 10.8", 2.2, S))
    wing = poly([(9.6, 10.4), (11.8, 4.2), (17.4, 3.2), (13.2, 11.4)], closed=True, r=r)
    tail = ("M12.8 13.2C16.5 13 20.4 15.5 21.4 20.6" + tip((20.4, 15.5), (21.4, 20.6), (16.5, 18.5), r)
            + "L16.5 18.5C14.5 17.5 13 16.2 12.2 15Z")
    return [shell(union(body, wing, tail)), dot(5.8, 7, 0.6), detail("M13.5 14.3C16.5 15 19 17 20.5 19.6"),
            line(seg(11.6, 4.8, 9.6, 3.6)), line(poly([(9.2, 14.2), (8.4, 17.5), (9.4, 21)], r=S.r)), line(seg(9.4, 21, 7.2, 21))]


@icon("phoenix", CAT, "Phoenix rising with wings spread upward over a burst of flames",
      tags=["firebird", "rebirth", "myth", "legend", "flames", "renewal"])
def _(S):
    r = L(S, 0, 0.6)
    wl = [(10.8, 8.6), (6.5, 6.6), (2.6, 2.6), (3.2, 6), (2.4, 7), (4, 9.3), (3.4, 10.4), (6.5, 11.4), (10.8, 12)]
    head = union(circle(12, 4.8, 1.7), tri(S, [(10.7, 4.1), (9, 5.3), (10.8, 5.7)], 0.2), tri(S, [(12.6, 3.4), (14.8, 1.8), (13.6, 4.2)], 0.3))
    bird = union(ellipse(12, 9.6, 2.1, 3.6), head, poly(wl, closed=True, r=r), poly(fpts(wl), closed=True, r=r))

    def tongue(x, y0, y1, w, lean=0.0):
        k = L(S, 0, 0.7)
        return (f"M{fmt(x + lean)} {fmt(y0)}C{fmt(x + lean * 0.3 + w * 0.2 + k)} {fmt(y0 + 2)} {fmt(x + w)} {fmt(y1 - 3)} {fmt(x + w)} {fmt(y1 - 1.6)}"
                f"C{fmt(x + w)} {fmt(y1)} {fmt(x - w)} {fmt(y1)} {fmt(x - w)} {fmt(y1 - 1.6)}"
                f"C{fmt(x - w)} {fmt(y1 - 3)} {fmt(x + lean * 0.3 - w * 0.2 - k)} {fmt(y0 + 2)} {fmt(x + lean)} {fmt(y0)}Z")
    flames = union(tongue(12, 14.6, 21.5, 2.6), tongue(7.6, 16.6, 21.3, 2, -1.2), tongue(16.4, 16.6, 21.3, 2, 1.2))
    return [shell(bird, stroke_miterlimit="2.5"), dot(12.3, 4.5, 0.5), shell(minus(flames, grow(bird, 1.5)))]


# ============================================================================ bird behaviour

@icon("bird-flying", CAT, "Small bird in flight in side view with both wings raised above its body",
      tags=["flying bird", "flight", "freedom", "wings", "soar", "bird"])
def _(S):
    d, e = flyer(S, 12, 12)
    return [shell(d, stroke_miterlimit="2.5"), dot(*e, 0.7)]


@icon("bird-on-branch", CAT, "Small bird perched on a leafy twig that crosses the icon diagonally",
      tags=["perched bird", "branch", "twig", "songbird", "spring", "garden"])
def _(S):
    d, e = songbird(S, 12.5, 9.5, 1.05)
    return [shell(d), dot(*e, 0.75), line(seg(2.5, 20.5, 21.5, 13.5)), line(seg(11.8, 12.9, 11.8, 16.6)),
            shell(leaf(5.4, 16.4, 5, 2.2, -60, S)), shell(leaf(19.3, 18.2, 5, 2.2, 45, S))]


@icon("bird-on-wire", CAT, "Three small birds perched in a row on a sagging power line between two poles",
      tags=["birds on a wire", "power line", "perched", "telephone wire", "countryside", "birds"])
def _(S):
    def sit(x, y):
        return mark(union(rot(ellipse(x + 0.6, y - 2.1, 1.9, 1.5), 15, x + 0.6, y - 2.1), circle(x - 1.1, y - 3.6, 1.2),
                          tri(S, [(x - 2.2, y - 4), (x - 3.2, y - 3.5), (x - 2.2, y - 3.1)], 0.1),
                          tri(S, [(x + 2, y - 2), (x + 3.2, y - 0.3), (x + 1.8, y - 0.6)], 0.2)))
    return [line(seg(2.5, 5, 2.5, 21.5)), line(seg(21.5, 5, 21.5, 21.5)),
            line("M2.5 8C8.5 12.8 15.5 12.8 21.5 8"), sit(7, 10.5), sit(12.4, 11.6), sit(17.8, 10.4)]


@icon("bird-flock", CAT, "Group of five simple birds of different sizes flying together",
      tags=["flock", "birds flying", "migration", "sky", "group", "birds"])
def _(S):
    return [mini_bird(7, 6, 1.3, S), mini_bird(16.5, 4.8, 1, S), mini_bird(12.5, 11.5, 1.35, S),
            mini_bird(18.5, 13, 0.95, S), mini_bird(6.5, 17, 1.05, S)]


@icon("bird-migration", CAT, "Birds flying in a V formation with a curved arrow showing their direction",
      tags=["migration", "v formation", "flock", "autumn", "journey", "birds"])
def _(S):
    birds = [mini_bird(x, y, 0.8, S) for x, y in ((18.5, 8.5), (14, 5.5), (9.5, 3.5), (14, 11.5), (9.5, 13.5))]
    head = poly([(17.2, 16.2), (20.8, 16.6), (19.8, 20)], r=S.r)
    return [*birds, line("M3 19.5C8 21.5 14.5 20.5 20.4 16.9"), line(head)]


@icon("bird-singing", CAT, "Songbird perched with its beak open and two music notes rising from it",
      tags=["birdsong", "singing", "tweet", "chirp", "song", "music"])
def _(S):
    d, e = songbird(S, 15.5, 15, 1.15, open_bill=True)
    return [shell(d), dot(*e, 0.75), line(seg(10, 20.5, 21, 20.5)), *note_pair(S, 3.6, 12.2, 8.4, 10, 4.6, 2.8)]


@icon("bird-landing", CAT, "Bird coming in to land with wings raised, tail fanned and feet reaching for a perch",
      tags=["landing", "touchdown", "perch", "flight", "arrive", "bird"])
def _(S):
    d, e = flyer(S, 12.5, 10.5, 1.0)
    d, e = rot(d, 25, 12.5, 10.5), rpts([e], 25, 12.5, 10.5)[0]
    return [shell(d, stroke_miterlimit="2.5"), dot(*e, 0.7),
            line(poly([(10.5, 15), (8, 17.5), (6.5, 20)], r=S.r)), line(poly([(12.5, 15.5), (11, 18), (10.5, 20)], r=S.r)),
            line(seg(3, 21, 14, 21))]


@icon("bird-sleeping", CAT, "Round bird perched with its head sunk into its feathers, eyes closed and a small zzz above",
      tags=["sleeping bird", "roost", "night", "rest", "sleep", "zzz"])
def _(S):
    body = union(circle(12, 14.3, 5.5), circle(8.6, 10.6, 3), tri(S, [(6.1, 11.3), (3.4, 12.4), (6.2, 13.2)], 0.3),
                 tri(S, [(16.5, 15.5), (20.8, 19.2), (16.2, 18.8)], 0.6))
    return [shell(body, stroke_miterlimit="2.5"), detail(arc(8.4, 9.6, 1.3, 20, 160)), detail("M10.5 15C12 17 14.5 17.5 16.5 16"),
            line(seg(10.8, 19.8, 10.8, 21.3)), line(seg(13.4, 19.8, 13.4, 21.3)), line(seg(6.5, 21.3, 17.5, 21.3)),
            zee(S, 13.8, 3, 3.4), zee(S, 18.4, 7, 2.4)]


@icon("bird-pecking", CAT, "Small bird with its head down pecking at seeds scattered on the ground",
      tags=["pecking", "foraging", "seeds", "feeding", "ground", "bird"])
def _(S):
    body = union(rot(ellipse(13.8, 12, 5, 3.1), -25, 13.8, 12), circle(7.5, 15, 2.2),
                 tri(S, [(6.2, 16.4), (4.8, 19), (7.6, 17.2)], 0.3), tri(S, [(17.6, 8.8), (21.4, 5.8), (19.2, 10.8)], 0.6))
    return [shell(body), dot(7.9, 14.4, 0.7), detail("M11 12.8C13 13 15 12 16.8 10.4"),
            line(seg(12.5, 15.4, 12.5, 21)), line(seg(15.2, 14.6, 15.2, 21)), line(seg(10.5, 21, 21.5, 21)),
            dot(3, 20.8, 1), dot(6.3, 21, 1)]


@icon("bird-feeding-chicks", CAT, "Parent bird on the rim of a nest dropping a worm into the open beaks of its chicks",
      tags=["feeding chicks", "parent bird", "nestlings", "baby birds", "nest", "spring"])
def _(S):
    d, e = songbird(S, 15.8, 8.6, 1.0)
    nest = "M2.5 15.5L17 15.5C16.5 19.2 13.5 21.3 9.75 21.3C6 21.3 3 19.2 2.5 15.5Z"
    beaks = [mark(tri(S, [(x - 0.5, 15.2), (x - 2, 11.2), (x - 0.2, 12.6), (x + 0.2, 12.6), (x + 2, 11.2), (x + 0.5, 15.2)], 0.2))
             for x in (6, 11.5)]
    return [shell(d), dot(*e, 0.7), line(seg(16, 11.8, 16, 14.5)), shell(nest), detail(seg(5.5, 18.3, 14, 18.3)),
            *beaks, line("M8.8 7.5C9.8 8.3 8 9 8.9 10")]


@icon("nest-building", CAT, "Bird flying with a twig held crosswise in its bill toward a half-built nest",
      tags=["nest building", "twig", "spring", "home", "build", "bird"])
def _(S):
    d, e = flyer(S, 8.6, 8.2, 0.68, mirror=True)
    nest = "M8.5 16.5L21.5 16.5C21 19.6 18.5 21.3 15 21.3C11.5 21.3 9 19.6 8.5 16.5Z"
    return [shell(d, stroke_miterlimit="2.5"), dot(*e, 0.6), line(seg(14.2, 5.2, 15.8, 11.4)),
            shell(nest), detail("M11 17.8L17.5 20.2"), detail("M13.5 20.2L19.5 17.8"), line(seg(10, 15.5, 7.5, 13)), line(seg(20, 15.5, 21.5, 13.2))]


@icon("early-bird", CAT, "Small bird on the ground pulling a worm from the soil with a rising sun behind",
      tags=["early bird", "morning", "sunrise", "worm", "early riser", "productivity"])
def _(S):
    d, e = songbird(S, 8.2, 11.6, 0.88, mirror=True)
    worm = "M14.3 10C15.3 11.4 13.1 12.3 13.6 14C14 15.2 13.1 16 13.4 17"
    sun = minus(circle(19, 17, 3.3), rect(0, 17, 24, 8))
    return [shell(d), dot(*e, 0.65), line(seg(7.8, 14.4, 7.8, 17)), line(worm), line("M13.4 17C13.4 18.5 14.7 19 14.4 20.5"),
            shell(sun), line(seg(19, 10.8, 19, 12.2)), line(seg(15.6, 12.9, 16.4, 13.7)), line(seg(22.4, 12.9, 21.6, 13.7)),
            ground(17, 2.5, 21.5)]


@icon("bird-in-hand", CAT, "Open hand held out flat with a small bird perched on the fingertips",
      tags=["bird in the hand", "trust", "gentle", "care", "tame bird", "proverb"])
def _(S):
    r = L(S, 0, 1.2)
    palm = ("M2.5 21.5L2.5 17" + tip((2.5, 17), (2.5, 14.3), (5.5, 14.3), r) + "L19.8 14.3C21.4 14.3 21.4 17.6 19.8 17.6L10.5 17.6"
            "C8.5 17.6 7.5 19 7.5 21.5Z")
    thumb = "M5.2 14.8C5.8 12.8 7.2 11.4 8.8 11.2C9.9 11.1 10.4 12 9.8 13L9 14.8Z"
    d, e = songbird(S, 16.3, 8.2, 0.95)
    return [shell(union(palm, thumb)), shell(d), dot(*e, 0.7), line(seg(15.8, 11.3, 15.8, 14.3))]


@icon("bird-release", CAT, "Two cupped hands opening upward with a small bird flying out of them",
      tags=["release", "let go", "freedom", "set free", "hope", "bird"])
def _(S):
    r = L(S, 0, 0.8)
    hand = "M2.6 12.5C2.4 17.5 5.5 21.4 10.8 21.4L10.8 17.8C8.2 17.6 6.5 15.5 6.3 12.5C5.8 11.5 3.1 11.5 2.6 12.5Z"
    wl = [(11.2, 7.2), (4.2, 2.6), (5.2, 6.2), (11.2, 10.4)]
    bird = union(ellipse(12, 8.2, 1.7, 3), circle(12, 4.4, 1.5), poly(wl, closed=True, r=r), poly(fpts(wl), closed=True, r=r),
                 tri(S, [(11, 10.5), (13, 10.5), (13.8, 13.3), (10.2, 13.3)], 0.4))
    return [shell(hand), shell(flip(hand)), shell(bird, stroke_miterlimit="2.5"), detail(seg(4.8, 16.4, 8, 18.3)), detail(seg(19.2, 16.4, 16, 18.3))]


@icon("bird-cage-open", CAT, "Domed bird cage with its door swung open and a small bird flying out",
      tags=["open cage", "freedom", "escape", "release", "liberty", "bird"])
def _(S):
    cage = union("M3.5 18V11.5C3.5 7.8 6.2 5.8 9.5 5.8C12.8 5.8 15.5 7.8 15.5 11.5V18Z", rect(2.5, 17.8, 14, 3.4, L(S, 1, 1.7)))
    door = poly([(15.5, 11), (19.5, 12.6), (19.5, 20.2), (15.5, 18.6)], closed=True, r=L(S, 0, 0.6))
    return [shell(cage), detail(seg(6.5, 7.2, 6.5, 17.8)), detail(seg(12.5, 7.2, 12.5, 17.8)), detail(seg(9.5, 6, 9.5, 11.5)),
            line(door), line(seg(9.5, 5.8, 9.5, 3.5)), mini_bird(18.5, 5.5, 1.05, S)]


@icon("owl-graduate", CAT, "Owl seen from the front wearing a square mortarboard cap with a tassel",
      tags=["graduation", "wise owl", "school", "education", "mortarboard", "learning"])
def _(S):
    body = "M6.5 12C6.5 9.3 8.8 8 12 8C15.2 8 17.5 9.3 17.5 12L17.5 16C17.5 19.3 15 21.5 12 21.5C9 21.5 6.5 19.3 6.5 16Z"
    board = poly([(2.6, 5.2), (12, 2.2), (21.4, 5.2), (12, 8.2)], closed=True, r=L(S, 0, 0.8))
    return [shell(union(body, board), stroke_miterlimit="2"), detail(circle(9.6, 13, 1.9)), detail(circle(14.4, 13, 1.9)),
            mark(tri(S, [(11.2, 15.6), (12.8, 15.6), (12, 17.3)], 0.3)), line(seg(20.2, 6, 20.2, 10.5)), dot(20.2, 11.2, 1.1)]


@icon("fledgling", CAT, "Fluffy young bird standing on the rim of a nest with short wings stretched out, about to fly",
      tags=["fledgling", "young bird", "first flight", "leaving the nest", "growing up", "chick"])
def _(S):
    r = L(S, 0, 0.8)
    body = union(circle(12, 10.3, 4.6), tri(S, [(10.8, 5.9), (11.3, 3.2), (12.4, 5.8)], 0.3), tri(S, [(12, 5.9), (13.6, 3.6), (13.4, 6.2)], 0.3))
    wl = [(7.8, 10.5), (3, 7.8), (4.2, 11.6), (7.6, 13)]
    wings = union(poly(wl, closed=True, r=r), poly(fpts(wl), closed=True, r=r))
    nest = nest_bowl(S, 4, 20, 17, 21.5)
    return [shell(union(body, wings)), dot(10.4, 9.4, 0.8), dot(13.6, 9.4, 0.8),
            mark(tri(S, [(11, 11), (13, 11), (12, 12.6)], 0.2)), line(seg(10.5, 14.8, 10.5, 17)), line(seg(13.5, 14.8, 13.5, 17)),
            shell(nest), detail(seg(8, 19, 16, 19))]


@icon("bird-tracks", CAT, "Trail of three-toed bird footprints walking diagonally across the ground",
      tags=["bird footprints", "tracks", "prints", "trail", "tracking", "nature"])
def _(S):
    def foot(x, y, deg):
        a, b, c, d, e = rpts([(x, y), (x, y - 4.6), (x - 3.6, y - 2.8), (x + 3.6, y - 2.8), (x, y + 1.5)], deg, x, y)
        return [line(poly([c, a, d], r=S.r)), line(seg(*b, *e))]
    return [*foot(7, 19.3, -8), *foot(17, 13.8, 8), *foot(7, 8.3, -8)]


@icon("bird-nest", CAT, "Empty round woven nest bowl made of crossing twigs, seen from the side",
      tags=["nest", "twigs", "home", "woven", "spring", "bird"])
def _(S):
    return [shell(nest_bowl(S, 2.5, 21.5, 9.5, 19.5)), *weave(5.5, 18.5, 12.3, 15.6), line(seg(4.5, 9.5, 2.5, 6.8)),
            line(seg(19.5, 9.5, 21.5, 6.8)), line(seg(10, 9.5, 8.8, 7.5))]


def _nest_eggs():
    return [f"M3.4 12.5A2.8 5 0 0 1 9 12.5", f"M15 12.5A2.8 5 0 0 1 20.6 12.5", f"M9 12.5A3 6.2 0 0 1 15 12.5"]


def _nest_eggs_filled():
    fill = lambda d: U(P(d), ST(d, 2))  # noqa: E731
    nest = nest_bowl(LINE, 2.5, 21.5, 13.5, 21.3)
    e1, e2, mid = _nest_eggs()
    body = U(fill(e1 + "Z"), fill(e2 + "Z"))
    body = U(D(body, ST(mid + "Z", 5)), fill(mid + "Z"))
    body = U(D(body, ST(nest, 5)), fill(nest))
    for p in weave(5.5, 18.5, 16.2, 18.9):
        body = D(body, ST(p.d, 2))
    return body



@icon("nest-with-eggs", CAT, "Woven nest bowl seen from the side with three oval eggs sitting inside",
      tags=["nest", "eggs", "clutch", "spring", "easter", "bird"],
      filled=lambda: _nest_eggs_filled())
def _(S):
    return [shell(nest_bowl(S, 2.5, 21.5, 13.5, 21.3)), *[line(d) for d in _nest_eggs()], *weave(5.5, 18.5, 16.2, 18.9)]



@icon("nest-with-chicks", CAT, "Woven nest with three small chicks inside, their beaks wide open pointing upward",
      tags=["nestlings", "baby birds", "chicks", "hungry", "feed me", "nest"])
def _(S):
    nest = nest_bowl(S, 2.5, 21.5, 14, 21.3)
    parts = [shell(nest), *weave(5.5, 18.5, 16.8, 19.4)]
    for x in (6.5, 12, 17.5):
        head = circle(x, 11.8, 2.5)
        parts.append(shell(minus(head, grow(nest, 1.5))))
        parts.append(dot(x, 11.5, 0.7))
        parts.append(mark(tri(S, [(x - 1.1, 9.8), (x - 2.4, 5.8), (x - 0.1, 9.3)], 0.2)))
        parts.append(mark(tri(S, [(x + 1.1, 9.8), (x + 2.4, 5.8), (x + 0.1, 9.3)], 0.2)))
    return parts


@icon("weaver-nest", CAT, "Hanging woven nest shaped like a gourd with a downward entrance tube, dangling from a thin branch",
      tags=["weaver bird", "hanging nest", "woven", "gourd", "africa", "nest"])
def _(S):
    body = union(circle(10, 10.8, 4.8), thick("M11.5 12.5C14 14.5 15.2 17.5 15.2 21.3", 3.6, S), thick("M10 6.2L10 5", 2.2, S))
    return [line(poly([(2.5, 4.6), (10, 4), (21.5, 2.6)], r=S.r)), shell(body),
            detail("M6.5 9.5C8.5 11 11 11.5 13.5 10.5"), mark(ellipse(15.2, 21, 1, 0.5))]


@icon("mud-nest", CAT, "Cup-shaped mud nest built from little pellets, stuck under the edge of a roof eave with a swallow peeking out",
      tags=["swallow nest", "martin nest", "mud", "eave", "pellets", "nest"])
def _(S):
    bump = (lambda x, y: circle(x, y, 1.9)) if S.name == "rounded" else (lambda x, y: poly(regular(x, y, 2, 6, 0), closed=True))
    cup = union("M4.5 5L19.5 5C19.5 11.5 16.5 16 12 16C7.5 16 4.5 11.5 4.5 5Z",
                *[bump(*pt_on(12, 5.5, 8.6, a)) for a in (20, 52, 90, 128, 160)])
    return [shell(union(rect(2.5, 2.5, 19, 3.5, min(S.R, 1.5)), cup)),
            dot(8.4, 10.2, 0.85), dot(15.6, 10.2, 0.85), dot(12, 11.4, 0.85), dot(10, 14, 0.85), dot(14, 14, 0.85), dot(12, 8.2, 0.85)]


@icon("stork-nest", CAT, "Large flat nest of sticks on top of a chimney with a stork standing on it",
      tags=["stork", "chimney nest", "rooftop", "europe", "spring", "nest"])
def _(S):
    r = L(S, 0, 0.8)
    stork = union(rot(ellipse(14, 7.8, 4, 2.2), 12, 14, 7.8), thick("M11 7.2C10 6 9.8 4.8 9.6 3.8", 1.8, S), circle(9.6, 3.4, 1.4),
                  tri(S, [(8.4, 2.9), (3.6, 5), (8.6, 4.2)], 0.2), tri(S, [(17.5, 7.5), (20.6, 9.3), (17.3, 9.7)], 0.5))
    nest = poly([(3.5, 12.5), (20.5, 12.5), (19, 15.3), (5, 15.3)], closed=True, r=r)
    return [shell(stork), line(seg(13, 10, 13, 12.5)), line(seg(15.3, 10, 15.3, 12.5)), shell(nest),
            line(seg(4.4, 12.5, 3, 11)), line(seg(19.6, 12.5, 21, 11)), shell(rect(8, 15.3, 8, 6.2, min(S.R, 1))),
            detail(seg(8, 18.3, 16, 18.3))]


@icon("nest-hole", CAT, "Tree trunk with a round hole and a small bird head peeking out of it",
      tags=["tree hole", "cavity nest", "hollow", "woodpecker hole", "owl hole", "nest"])
def _(S):
    trunk = "M5 2.5L19 2.5L19 16.5C19 18.8 20 20.5 21.5 21.5L2.5 21.5C4 20.5 5 18.8 5 16.5Z"
    head = union(circle(12.8, 12.4, 1.9), tri(S, [(11.1, 11.8), (8.8, 12.6), (11.1, 13.4)], 0.3))
    hole = minus(ellipse(12, 10.6, 4, 4.9), grow(head, 1.5))
    return [shell(trunk, stroke_miterlimit="2.5"), mark(hole), shell(head), dot(13, 11.9, 0.65),
            line(seg(19, 7, 21.5, 5)), detail(seg(9, 18.2, 9, 20)), detail(seg(15, 18.2, 15, 20))]


@icon("ground-nest", CAT, "Speckled eggs lying in a shallow scrape on the ground ringed with small pebbles",
      tags=["scrape nest", "plover", "tern", "beach nest", "shorebird", "eggs"])
def _(S):
    peb = (lambda x, y: dot(x, y, 1.1)) if S.name == "rounded" else (lambda x, y: mark(poly(regular(x, y, 1.3, 4, 0), closed=True)))
    parts = [shell(egg(*pt_on(12, 12, 4.8, a), 0.42, a - 90)) for a in (-90, 30, 150)]
    parts += [peb(*pt_on(12, 12, 9.7, a)) for a in range(-60, 300, 40)]
    return parts


@icon("egg-cracked", CAT, "Empty eggshell broken into two jagged-edged halves side by side",
      tags=["broken eggshell", "eggshell", "cracked", "hatched", "empty shell", "egg"])
def _(S):
    cut = poly([(-6, 0), *[(x - 12, y - 12) for x, y in zig(S, 6.9, 17.1, 12, 3, 1.0)], (6, 0), (6, 9), (-6, 9)], closed=True)
    whole = egg(0, 0, 1.0)
    low = path_to_d(I(P(whole), P(cut)))
    top = minus(whole, cut)
    return [shell(xf(low, 7, 13.5)), shell(rot(xf(top, 17, 11), 25, 17, 11))]


@icon("chick-hatching", CAT, "Fluffy chick poking its head and wings out of a cracked egg with a piece of shell on its head",
      tags=["hatching", "chick", "newborn", "easter", "birth", "egg"])
def _(S):
    r = L(S, 0, 0.6)
    rim = zig(S, 5.5, 18.5, 14.2, 3, 1.0)
    base = poly([(5.5, 13.4), *rim[1:-1], (18.5, 13.4), (18.3, 17), (16, 21.3), (8, 21.3), (5.7, 17)], closed=True, r=r)
    head = union(circle(12, 10.2, 3.8), tri(S, [(8.8, 11.8), (5.6, 10.4), (8.5, 13.6)], 0.4),
                 tri(S, [(15.2, 11.8), (18.4, 10.4), (15.5, 13.6)], 0.4))
    cap = rot(poly([(8.6, 6.4), (9.2, 3.8), (11.8, 2.6), (14.4, 3.4), (15.4, 5.8), (14, 5), (12.6, 6.6), (11.2, 5), (10, 6.6)],
                   closed=True, r=r), 12, 12, 4.6)
    return [shell(union(base, head, cap)), detail(poly(rim, r=L(S, 0, 0.3))),
            detail(poly(rpts([(8.6, 6.4), (10, 6.6), (11.2, 5), (12.6, 6.6), (14, 5), (15.4, 5.8)], 12, 12, 4.6), r=L(S, 0, 0.3))),
            dot(10.7, 9.8, 0.75), dot(13.3, 9.8, 0.75), mark(tri(S, [(11.2, 11.2), (12.8, 11.2), (12, 12.6)], 0.2))]


@icon("egg-candling", CAT, "Egg held over a small lamp with light shining through it to show the embryo and air cell",
      tags=["candling", "incubation", "fertile egg", "embryo", "hatchery", "poultry"])
def _(S):
    rays = [line(seg(*pt_on(12, 10, 7.6, a), *pt_on(12, 10, 9.4, a))) for a in (-150, -118, -62, -30)]
    return [shell(egg(12, 10.8, 0.9)), detail("M8.6 8.2C10.5 9 13.5 9 15.4 8.2"), dot(12.6, 12.3, 1.4),
            shell(poly([(8.5, 17.5), (15.5, 17.5), (16.5, 21.5), (7.5, 21.5)], closed=True, r=L(S, 0, 0.8))), *rays]


@icon("egg-incubator", CAT, "Box incubator with a clear dome lid over a row of eggs and a small dial on the front",
      tags=["incubator", "hatching eggs", "hatchery", "poultry", "brooder", "farm"])
def _(S):
    return [line("M3.5 13C3.5 7.5 7.5 4.5 12 4.5C16.5 4.5 20.5 7.5 20.5 13"), shell(rect(2.5, 13, 19, 8.5, min(S.R, 2))),
            *[shell(egg(x, 10.4, 0.42)) for x in (7.5, 12, 16.5)], detail(circle(16.5, 17.2, 1.5)), detail(seg(6, 17.2, 11, 17.2))]


@icon("ostrich-egg", CAT, "Very large ostrich egg beside a small chicken egg to show the difference in size",
      tags=["ostrich egg", "big egg", "size comparison", "largest egg", "ratite", "egg"])
def _(S):
    big = egg(9, 12.4, 1.55)
    return [shell(big), detail("M5.2 12.5C5.2 9.5 6.3 7 8 5.8"), shell(egg(19, 17.6, 0.57)), line(seg(2.5, 21.5, 21.5, 21.5))]


@icon("golden-egg", CAT, "Single shining golden egg with a highlight and sparkles around it",
      tags=["golden egg", "treasure", "prize", "wealth", "fairy tale", "egg"])
def _(S):
    return [shell(egg(11, 13.3, 1.28)), detail("M7.8 13.8C7.8 11 8.8 8.5 10.5 7.4"),
            sparkle(S, 18.8, 5, 2.8), sparkle(S, 20, 11.5, 1.8), sparkle(S, 4, 5.5, 1.8)]


@icon("owl-pellet", CAT, "Oval owl pellet with small bones poking out of its furry surface",
      tags=["pellet", "owl", "regurgitated", "bones", "dissection", "science"])
def _(S):
    pellet = rot(ellipse(12, 12.5, 9.5, 6.8), -12, 12, 12.5)
    knob = (lambda x, y: dot(x, y, 1.3)) if S.name == "rounded" else (lambda x, y: mark(poly(regular(x, y, 1.5, 4, 45), closed=True)))
    return [shell(pellet), detail(seg(7, 13.6, 12.5, 10.6)), knob(6.2, 14.4), knob(6.6, 12.6), knob(13.3, 10.6), knob(12.6, 9),
            detail(circle(15.6, 14.4, 1.6)), detail("M6.5 17.5C8 18.3 9.5 18.5 11 18.4")]


@icon("bird-wing", CAT, "Single bird wing spread out with rows of long flight feathers ending in rounded tips",
      tags=["wing", "feathers", "flight", "angel wing", "plumage", "bird"])
def _(S):
    rows = [(5.5, 22), (10, 18.6), (14.5, 15.2), (19, 11.8)]
    parts = [rect(6, y - 2.25, x1 - 6, 4.5, L(S, 0.8, 2.25)) for y, x1 in rows]
    parts.append("M10 3.25C5.5 3.25 2.5 8 2.5 12.5C2.5 17 4.5 21.25 7 21.25L10 21.25Z")
    out = [shell(union(*parts)), *[detail(seg(9, y + 2.25, x1 - 3.2, y + 2.25)) for y, x1 in rows[:3]]]
    return [Part(p.kind, rotd(p.d, -15), p.attrs) for p in out]


@icon("talon", CAT, "Bird of prey foot with a scaly leg and three toes ending in long hooked claws",
      tags=["claw", "raptor foot", "eagle claw", "bird of prey", "grip", "sharp"])
def _(S):
    leg = rect(13, 2.5, 4.2, 10, min(S.R, 1.2))
    return [shell(leg), detail(seg(13, 5.6, 17.2, 5.6)), detail(seg(13, 8.8, 17.2, 8.8)),
            line(poly([(13.6, 12.5), (6.5, 15.4)], r=0) + "C4.8 16.1 4.1 17.8 4.6 20"),
            line(poly([(14.6, 12.5), (10.6, 17.6)], r=0) + "C9.8 18.7 9.8 20.2 10.6 21.5"),
            line(poly([(16.6, 12.5), (19.4, 15.6)], r=0) + "C20.5 16.8 20.6 18.6 19.6 20")]


@icon("webbed-foot", CAT, "Duck foot seen from above with three forward toes joined by webbing",
      tags=["duck foot", "webbed", "waterfowl", "swim", "paddle", "footprint"])
def _(S):
    r = L(S, 0, 0.9)
    lt, mt, rt = (3.2, 7.5), (12, 2.6), (20.8, 7.5)
    foot = ("M12 18.2L10.6 16.8" + tip((10.6, 16.8), lt, (8, 10), r)
            + f"Q7.5 9.4 11.3 4" + tip((11.3, 4), mt, (12.7, 4), r)
            + "L12.7 4Q16.5 9.4 16 10" + tip((16, 10), rt, (13.4, 16.8), r) + "L13.4 16.8Z")
    return [shell(foot, stroke_miterlimit="3"), detail(seg(12, 15.5, 12, 6.5)), line(seg(12, 18.5, 12, 22))]


@icon("bird-skull", CAT, "Bird skull in side view with a large round eye socket and a long pointed beak",
      tags=["skull", "bone", "skeleton", "anatomy", "halloween", "bird"])
def _(S):
    r = L(S, 0, 0.6)
    skull = union(circle(15.6, 10.5, 5.8), poly([(11, 7.2), (2.5, 13.6), (12.2, 15.2)], closed=True, r=r))
    return [shell(skull, stroke_miterlimit="3"), detail(circle(15.6, 10, 2.4)), dot(8, 12.4, 0.8),
            line(poly([(4.2, 16.8), (12, 18.6), (17.5, 17.8)], r=S.r))]


@icon("wishbone", CAT, "Forked V-shaped wishbone with the two arms joined at a rounded point",
      tags=["wishbone", "furcula", "make a wish", "luck", "thanksgiving", "bone"])
def _(S):
    v = thick("M6.2 5C7 11 9.5 16.3 11.2 18.8Q12 20 12.8 18.8C14.5 16.3 17 11 17.8 5", 3, S)
    return [shell(union(v, circle(6, 4.6, 2), circle(18, 4.6, 2)))]


@icon("peacock-feather", CAT, "Long peacock feather with a large eye spot near the tip and fine barbs along its shaft",
      tags=["peacock", "feather", "plume", "eye spot", "decoration", "boho"])
def _(S):
    vane = "M12 -1.6C15.6 -1.6 16.8 1.6 16.5 4.8C16 9.2 13.8 12.6 12 17C10.2 12.6 8 9.2 7.5 4.8C7.2 1.6 8.4 -1.6 12 -1.6Z"
    notches = [poly([(6, 8.2), (11, 11.4), (6, 11)], closed=True), poly([(18, 10.2), (13, 13.4), (18, 13)], closed=True)]
    parts = [shell(minus(vane, *notches), stroke_miterlimit="2"), detail(ellipse(12, 4, 2.5, 3)), dot(12, 4.2, 0.9),
             line(seg(12, 16.5, 12, 25.6))]
    return [Part(p.kind, rotd(p.d, 45), p.attrs) for p in parts]


@icon("birdhouse", CAT, "Small wooden birdhouse with a pitched roof, a round entrance hole and a perch peg below it",
      tags=["bird house", "nest box", "garden", "backyard", "shelter", "home"])
def _(S):
    body = union(rect(5.5, 10, 13, 11.5, min(S.R, 1.5)), poly([(2.5, 11.5), (12, 3), (21.5, 11.5)], closed=True, r=L(S, 0, 1)))
    return [shell(body), detail(seg(5.5, 11.5, 18.5, 11.5)), detail(circle(12, 14.9, 1.8)), dot(12, 19.2, 1)]


@icon("martin-house", CAT, "Multi-story birdhouse on a pole with rows of round entrance holes",
      tags=["purple martin", "bird house", "colony house", "apartment", "pole", "nest box"])
def _(S):
    body = union(rect(4, 8, 16, 9.5, min(S.R, 1.5)), poly([(2.5, 8.8), (12, 2.5), (21.5, 8.8)], closed=True, r=L(S, 0, 1)))
    return [shell(body, stroke_miterlimit="2"), detail(seg(4, 8.8, 20, 8.8)), *[dot(x, y, 1.1) for x in (8, 12, 16) for y in (11.6, 15)],
            line(seg(12, 17.5, 12, 21.5)), line(seg(8.5, 21.5, 15.5, 21.5))]


@icon("dovecote", CAT, "Round pigeon tower with a conical roof and small arched openings with ledges",
      tags=["pigeon house", "dove house", "columbarium", "pigeon loft", "tower", "farm"])
def _(S):
    body = union(rect(5, 9.5, 14, 12, min(S.R, 1.2)), poly([(3.5, 10.3), (12, 3.2), (20.5, 10.3)], closed=True, r=L(S, 0, 1)))

    def arch(x, y):
        return mark(f"M{fmt(x - 1.2)} {fmt(y + 1.3)}V{fmt(y)}A1.2 1.2 0 0 1 {fmt(x + 1.2)} {fmt(y)}V{fmt(y + 1.3)}Z")
    return [shell(body, stroke_miterlimit="2.5"), detail(seg(5, 10.3, 19, 10.3)), line(seg(12, 3.2, 12, 1.2)),
            *[arch(x, y) for x in (8.4, 12, 15.6) for y in (13.2, 17.4)]]


@icon("aviary", CAT, "Walk-in mesh bird enclosure with a curved roof, a door and a bird perched inside",
      tags=["aviary", "bird enclosure", "zoo", "flight cage", "birdhouse", "pets"])
def _(S):
    shape = "M2.5 21.5V10C2.5 6.2 6.5 3.5 12 3.5C17.5 3.5 21.5 6.2 21.5 10V21.5Z"
    b, e = songbird(S, 8, 14.2, 0.62)
    return [shell(shape), detail("M2.5 10C5.5 8 18.5 8 21.5 10"), detail(rect(14.5, 13, 4, 8.5, L(S, 0, 1))),
            mark(b), detail(seg(4.5, 17.2, 11.5, 17.2))]


@icon("chicken-coop", CAT, "Small wooden hen house on legs with a pitched roof, a little door and a ramp to the ground",
      tags=["hen house", "coop", "chickens", "poultry", "farm", "backyard"])
def _(S):
    body = union(rect(4.5, 9, 11, 7.5, min(S.R, 1.2)), poly([(2.5, 10), (10, 3), (17.5, 10)], closed=True, r=L(S, 0, 1)))
    return [shell(body), detail(seg(4.5, 10, 15.5, 10)), detail(rect(10.5, 12.3, 2.6, 4.2, 0)),
            line(seg(6.5, 16.5, 6.5, 21.5)), line(seg(12, 16.5, 12, 21.5)), line(seg(15.5, 15.8, 21.5, 21.3)),
            line(seg(17.4, 19.4, 18.4, 18.4))]


@icon("bird-feeder", CAT, "Hanging tube bird feeder full of seed, with a roof cap, feeding ports with perches and a base tray",
      tags=["bird feeder", "seed feeder", "tube feeder", "garden", "backyard", "winter"])
def _(S):
    cap = poly([(6.5, 7.2), (9, 4.2), (15, 4.2), (17.5, 7.2)], closed=True, r=L(S, 0, 0.8))
    tube = rect(8.5, 7.2, 7, 11.8, 0)
    return [line(seg(12, 1.8, 12, 4.2)), shell(union(cap, tube, rect(6.5, 18.5, 11, 3, min(S.R, 1.5)))),
            dot(10.5, 10.4, 0.8), dot(13.5, 11.6, 0.8), dot(11, 14.4, 0.8), dot(13.5, 15.8, 0.8),
            line(seg(8.5, 12.6, 4.5, 12.6)), line(seg(15.5, 15, 19.5, 15))]


@icon("hummingbird-feeder", CAT, "Hanging bulb of nectar over a round base dotted with small flower-shaped feeding ports",
      tags=["nectar feeder", "hummingbird", "sugar water", "garden", "backyard", "feeder"])
def _(S):
    bulb = union(circle(12, 9, 5), rect(10.3, 12, 3.4, 4, 0))
    base = rect(2.5, 15.5, 19, 5, L(S, 1.5, 2.5))
    return [line(seg(12, 1.8, 12, 4)), shell(union(bulb, base)), detail("M7.2 9.5C10 10.3 14 10.3 16.8 9.5"),
            sparkle(S, 6.5, 18, 1.8), sparkle(S, 12, 18, 1.8), sparkle(S, 17.5, 18, 1.8)]


@icon("bird-table", CAT, "Flat bird feeding platform on a post with a small pitched roof over it and seeds on the tray",
      tags=["bird table", "feeding station", "garden", "backyard", "seed tray", "wildlife"])
def _(S):
    roof = poly([(3, 8.5), (12, 4), (21, 8.5)], closed=True, r=L(S, 0, 0.8))
    return [shell(roof), line(seg(6.5, 8.5, 6.5, 14.5)), line(seg(17.5, 8.5, 17.5, 14.5)),
            shell(rect(3, 14.5, 18, 2.8, L(S, 0, 1.2))), line(seg(12, 17.3, 12, 21.5)),
            line(seg(8.5, 21.5, 15.5, 21.5)), dot(9.6, 12.4, 0.8), dot(12, 12, 0.8), dot(14.4, 12.4, 0.8)]


@icon("suet-feeder", CAT, "Square wire cage holding a block of seed cake, hanging from a chain",
      tags=["suet", "suet cage", "fat ball", "seed cake", "garden", "winter feeding"])
def _(S):
    cage = rect(4.5, 9, 15, 12, min(S.R, 2))
    return [shell(ellipse(12, 4.8, 1.4, 2.2)), line(seg(12, 7, 12, 9)), shell(cage),
            detail(seg(4.5, 9, 19.5, 21)), detail(seg(19.5, 9, 4.5, 21))]

@icon("bird-bath", CAT, "Shallow round basin on a pedestal stand with a small water ripple on top",
      tags=["bird bath", "garden", "water basin", "pedestal", "backyard", "drinking"])
def _(S):
    basin = "M2.5 10H21.5C21.5 14.2 17.5 16 12 16C6.5 16 2.5 14.2 2.5 10Z"
    stand = union(rect(10.4, 15.5, 3.2, 4, 0), rect(6.5, 19.5, 11, 2.5, L(S, 0, 1.2)))
    return [shell(union(basin, stand)), detail("M6.5 11.2Q9.2 9.6 12 11.2T17.5 11.2"),
            dot(8.5, 5.6, 0.9), dot(12, 3.8, 0.9), dot(15.5, 5.6, 0.9)]


@icon("birdseed", CAT, "Open sack with a small bird outline on it, beside a pile of loose seeds",
      tags=["birdseed", "bird seed", "seed sack", "feed", "millet", "bird food"])
def _(S):
    body = poly([(4.8, 8.5), (3.4, 20), (4.6, 21.5), (12.4, 21.5), (13.6, 20), (12.2, 8.5)], closed=True, r=L(S, 0, 1))
    cuff = rect(3.6, 4.5, 10.8, 4.2, L(S, 0, 1.5))
    return [shell(union(body, cuff)), detail(seg(3.6, 8.7, 14.4, 8.7)), detail(mini_bird(9, 16, 1.0).d),
            dot(16.3, 20.3, 1.1), dot(19.6, 20.3, 1.1), dot(17.9, 17.4, 1.1), dot(19.6, 14.6, 1.1)]

@icon("bird-swing", CAT, "Pet bird perched on a hanging swing: a bar on two strings from a ring at the top",
      tags=["bird swing", "pet bird", "perch", "parakeet", "cage toy", "budgie"])
def _(S):
    b, e = songbird(S, 12, 14.6, 0.6)
    return [shell(circle(12, 3.6, 1.6)), line(poly([(5.5, 18), (5.5, 10), (12, 5.2), (18.5, 10), (18.5, 18)], r=L(S, 0, 1.5))),
            shell(b), dot(e[0], e[1], 0.4), line(seg(3.5, 18, 20.5, 18))]

@icon("parrot-perch", CAT, "Bird stand with a horizontal perch bar on a pole and round base, a bird on one side and a feeding cup on the other",
      tags=["parrot stand", "perch", "pet bird", "play stand", "feeding cup", "cage"])
def _(S):
    cup = "M14.6 12.5H21C21 16.3 19 17.6 17.8 17.6C16.6 17.6 14.6 16.3 14.6 12.5Z"
    b, e = songbird(S, 7.6, 7.4, 0.72, True)
    return [shell(b), dot(e[0], e[1], 0.6), line(seg(3, 11.5, 21, 11.5)), line(seg(12, 11.5, 12, 19.5)), line(seg(17.8, 11.5, 17.8, 12.5)),
            shell(cup), shell(rect(6, 19.5, 12, 2.5, L(S, 0, 1.2)))]

@icon("bird-hide", CAT, "Small wooden hut with a long horizontal viewing slit and binoculars poking out",
      tags=["bird hide", "birdwatching", "blind", "observation hut", "nature reserve", "binoculars"])
def _(S):
    hut = union(rect(3.5, 8.5, 17, 13, 0), poly([(2, 9), (4.5, 4), (19.5, 4), (22, 9)], closed=True, r=L(S, 0, 0.8)))
    return [shell(hut), detail(seg(4.6, 14.6, 6.8, 14.6)), detail(seg(17.2, 14.6, 19.4, 14.6)),
            shell(union(circle(9.4, 14.6, 2.9), circle(14.6, 14.6, 2.9))), mark(circle(9.4, 14.6, 1)), mark(circle(14.6, 14.6, 1))]

@icon("bird-ring", CAT, "Bird's thin leg and three-toed foot with a small metal identification band around the leg",
      tags=["bird ring", "leg band", "banding", "ringing", "ornithology", "tag", "identification"])
def _(S):
    band = rect(5.5, 6.5, 5.5, 11, min(S.R, 2))
    return [line(seg(2, 12, 5.5, 12)), shell(band), line(seg(11, 12, 16, 12)),
            line(poly([(21.5, 7), (16, 12), (21.5, 17)], r=L(S, 0, 0.8))), line(seg(16, 12, 21.5, 12)),
            mark(circle(8.25, 9.8, 0.75)), mark(circle(8.25, 14.2, 0.75))]


@icon("bird-call", CAT, "Small wooden bird call whistle with a mouthpiece, a turned peg and curved sound lines",
      tags=["bird call", "whistle", "lure", "birdsong", "birdwatching", "hunting", "sound"])
def _(S):
    body = union(rect(5, 9.5, 10, 6.5, min(S.R, 2.5)), rect(2.5, 11, 3, 3.5, 0))
    return [shell(body), detail(seg(10.5, 9.5, 10.5, 16)), line(arc(15.5, 12.8, 3.6, -55, 55)),
            line(arc(15.5, 12.8, 7, -50, 50)), line(seg(8, 4.5, 8, 9.5)), shell(circle(8, 3.6, 1.3))]


@icon("duck-decoy", CAT, "Carved wooden duck decoy floating on the water with a weight cord hanging below it",
      tags=["decoy", "duck hunting", "waterfowl", "carved duck", "hunting", "lure", "floating"])
def _(S):
    body = union(ellipse(13, 10.6, 7.6, 3.9), circle(6.6, 6.4, 2.7), poly([(4.9, 8), (8, 8), (9.6, 12), (5.8, 10.6)], closed=True),
                 tri(S, [(4.6, 5.6), (2.8, 7), (4.6, 8.6)], 0.4), tri(S, [(19, 8.6), (21.2, 7.4), (20.4, 12)], 0.5))
    wave = "M2.5 15.4Q4.9 13.6 7.3 15.4T12.1 15.4T16.9 15.4T21.5 15.4"
    return [shell(body), dot(6.6, 5.9, 0.75), line(wave), line(seg(12, 15.4, 12, 18.5)),
            shell(poly([(9.8, 18.5), (14.2, 18.5), (15.4, 21.6), (8.6, 21.6)], closed=True, r=L(S, 0, 0.6)))]


def raptor(S, x, y, s=1.0, mirror=False):
    """Perched falcon facing left with a hooked bill and long tail; origin at the body centre. Returns (d, eye)."""
    parts = [circle(-3, -3.4, 2.4), rot(ellipse(0.4, 0.3, 4.2, 3.1), 28, 0.4, 0.3),
             tri(S, [(2.6, 1.6), (7.6, 7.6), (4.4, 6.4)], 0.6),
             tri(S, [(-5, -4.6), (-7.6, -3.6), (-6.8, -1.2), (-5.2, -2.2)], 0.3)]
    return xf(union(*parts), x, y, s, mirror), xpt(-3.4, -3.8, x, y, s, mirror)


@icon("falconry-glove", CAT, "Thick leather gauntlet held up with a falcon perched on the fist and jesses hanging",
      tags=["falconry", "gauntlet", "falconer", "glove", "bird of prey", "hawking", "leather"])
def _(S):
    fist = union(rect(2.5, 13.5, 6.5, 8, 0), rect(8, 14.2, 13.5, 7.3, L(S, 2, 3.4)))
    b, e = raptor(S, 13, 7.6, 0.9)
    return [shell(fist), detail(seg(9, 13.5, 9, 21.5)), shell(b), dot(e[0], e[1], 0.65),
            line(seg(12, 11.2, 12, 14.2)), detail("M15.4 14.2C15.4 16.4 16.6 17 16.6 19.4")]

@icon("falcon-hood", CAT, "Small leather falconry hood with a plume on top, a pointed beak opening and two trailing straps",
      tags=["falconry", "hood", "hawk hood", "leather", "bird of prey", "topknot", "straps"])
def _(S):
    hood = "M2.5 16L5.3 12.2C6.6 8.6 9.2 7 12.6 7C17.2 7 20.2 10.4 20.2 15V17.5H4.2Z"
    return [shell(hood, stroke_miterlimit="3"), detail(seg(9, 13.2, 14.5, 13.2)),
            line(seg(12.6, 7, 10.2, 3.4)), line(seg(12.6, 7, 12.6, 2.8)), line(seg(12.6, 7, 15, 3.4)),
            line(seg(16.2, 17.5, 16.2, 21.6)), line(seg(19.6, 17.5, 19.6, 21.6))]


@icon("bird-spikes", CAT, "Row of thin anti-bird spikes fanning up from a mounting strip on a ledge",
      tags=["anti-bird spikes", "pigeon deterrent", "bird control", "ledge", "pest control", "prevent roosting"])
def _(S):
    xs = (4.5, 8.25, 12, 15.75, 19.5)
    return [shell(rect(2.5, 17, 19, 4, L(S, 0, 1.5))),
            *[line(seg(x, 17, 12 + (x - 12) * 1.45, 4.5)) for x in xs]]


@icon("bird-strike", CAT, "Airplane nose with a small bird colliding with it and an impact burst at the point of contact",
      tags=["bird strike", "aviation", "collision", "airplane", "airport", "safety", "crash"])
def _(S):
    nose = "M22 13.5H16.6C13.4 13.5 11.2 15.4 9.8 17.4C11.2 19.4 13.4 21.2 16.6 21.2H22Z"
    b, e = flyer(S, 8, 8.2, 0.5)
    return [shell(nose), detail(seg(16.4, 16.2, 20, 16.2)), shell(b), dot(e[0], e[1], 0.5), sparkle(S, 11.2, 12.6, 2.3)]

@icon("bird-flu", CAT, "Bird head and neck in side view beside a round virus particle covered in short spikes",
      tags=["avian influenza", "bird flu", "h5n1", "virus", "poultry disease", "outbreak", "health"])
def _(S):
    neck = "M4.6 10.5C4.6 15 5 18.5 5.8 21.5H12.8C11.8 18.5 11.4 14 11.4 10.5Z"
    body = union(circle(8, 8.2, 3.6), neck, tri(S, [(5, 6.8), (1.8, 8.6), (5, 10.4)], 0.4))
    vx, vy = 18, 15.6
    spikes = [line(seg(*pt_on(vx, vy, 3.3, a), *pt_on(vx, vy, 5, a))) for a in range(0, 360, 45) if a != 180]
    return [shell(body), dot(7, 7.4, 0.8), shell(circle(vx, vy, 3.3)), *spikes]


@icon("bird-tracker", CAT, "Bird in flight carrying a small tracking tag with an antenna and radio signal waves",
      tags=["bird tracking", "gps tag", "telemetry", "migration study", "ornithology", "satellite tag", "wildlife monitoring"])
def _(S):
    b, e = flyer(S, 9, 15, 0.72)
    return [shell(b), dot(e[0], e[1], 0.5), line(seg(13.2, 16.6, 16.4, 12.8)), line(arc(16.4, 12.8, 2.6, -80, 0)),
            line(arc(16.4, 12.8, 5.2, -80, 0))]


@icon("origami-crane", CAT, "Folded paper crane in side view with flat angular wings, a pointed neck and a faceted body",
      tags=["origami", "paper crane", "paper folding", "peace", "japan", "senbazuru", "craft"])
def _(S):
    r = L(S, 0, 0.6)
    body = poly([(3, 6), (5.6, 5), (9.3, 12.6), (13.5, 14.6), (21.5, 10.4), (16.5, 19.2), (9.5, 18.4), (7.3, 14.6)], closed=True, r=r)
    wing = poly([(9.6, 12.6), (17.4, 3.4), (16.4, 14.4)], closed=True, r=r)
    return [shell(union(body, wing), stroke_miterlimit="3"), detail(seg(16.4, 14.4, 12.6, 18.8))]


@icon("communal-nest", CAT, "Huge thatched nest mass hanging from a branch with many small round entrance holes underneath",
      tags=["sociable weaver", "colony nest", "thatched nest", "apartment nest", "birds", "tree", "haystack"])
def _(S):
    mass = "M2.8 9C2.8 6.6 7 5.8 12 5.8C17 5.8 21.2 6.6 21.2 9C21.2 14 18 17.2 12 17.2C6 17.2 2.8 14 2.8 9Z"
    return [line(seg(2.5, 4, 21.5, 4)), shell(mass), mark(circle(7.3, 12.6, 1.2)), mark(circle(12, 14, 1.2)), mark(circle(16.7, 12.6, 1.2)),
            detail("M6.8 8.2L8.4 10"), detail("M11 8.6L12.6 10.4"), detail("M15.6 8.2L17.2 10"),
            mini_bird(6.5, 20.6, 0.85), mini_bird(17.5, 20.6, 0.85)]
