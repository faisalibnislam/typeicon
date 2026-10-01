"""TypeIcon Core: classroom (batch classroom_001): school subjects, classroom science, crafts, PE,
tests and grading, stationery extras, graduation and study habits.

Subject lessons share one small chalkboard on two legs; what is drawn on the board names the subject.
Test and grading icons share one portrait sheet of paper.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path.parser import parse_path
from geometry import SCALE, D, P, ST, U, fmt, path_to_d, rotation

CAT = "classroom"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def tf(d, m):
    """Apply an affine matrix (a, b, c, d, e, f) to a d-string, keeping open paths open."""
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def rot(d, deg, cx=12.0, cy=12.0):
    """Rotate a d-string clockwise on screen about (cx, cy)."""
    return tf(d, rotation(deg, cx, cy))


def mv(d, dx, dy):
    return tf(d, (1, 0, 0, 1, dx, dy))


def flip(d):
    """Mirror across the vertical centre line."""
    return tf(d, (-1, 0, 0, 1, 24, 0))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def grow(d, g):
    """Region d expanded by g px (used to cut clean gaps between overlapping parts)."""
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def turn(parts, deg, cx=12.0, cy=12.0):
    return [Part(p.kind, rot(p.d, deg, cx, cy), p.attrs) for p in parts]


def shift(parts, dx, dy):
    return [Part(p.kind, mv(p.d, dx, dy), p.attrs) for p in parts]


def fit(parts, cx=12.0, cy=12.0):
    """Translate parts so their drawn bounds are centred on (cx, cy), snapped to half pixels."""
    regions = []
    for p in parts:
        regions.append(P(p.d) if p.kind in ("shell", "dot", "solid") else ST(p.d, 2.0))
    x0, y0, x1, y1 = U(*regions).bounds
    dx = round((cx - (x0 + x1) / 2 / SCALE) * 2) / 2
    dy = round((cy - (y0 + y1) / 2 / SCALE) * 2) / 2
    if dx == 0 and dy == 0:
        return parts
    return [Part(p.kind, mv(p.d, dx, dy), p.attrs) for p in parts]


def lens(x0, y0, x1, y1, bulge):
    """Pointed leaf between two points; bulge is the half-width at the middle (quadratic sides)."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln
    k = bulge * 2
    return (f"M{fmt(x0)} {fmt(y0)}Q{fmt(mx + nx * k)} {fmt(my + ny * k)} {fmt(x1)} {fmt(y1)}"
            f"Q{fmt(mx - nx * k)} {fmt(my - ny * k)} {fmt(x0)} {fmt(y0)}Z")


def board(S):
    """Small chalkboard on two splayed legs. Writing area (stroke centres) x 5..19, y 6..15."""
    return [shell(rect(2, 3, 20, 15, rr(S, 2.5))), line(seg(6.5, 18, 5, 21.5)), line(seg(17.5, 18, 19, 21.5))]


def sheet(S, x=4, y=2.5, w=16, h=19):
    return shell(rect(x, y, w, h, rr(S, 2.5)))


def butterfly(cx, cy, s=1.0):
    """Small solid butterfly silhouette (four wings split by a thin body gap)."""
    def wing(x, y, rx, ry, deg):
        return rot(ellipse(cx + x * s, cy + y * s, rx * s, ry * s), deg, cx + x * s, cy + y * s)
    shape = union(wing(-2.3, -1.3, 2.6, 2.0, -30), wing(2.3, -1.3, 2.6, 2.0, 30),
                  wing(-1.7, 2.1, 1.9, 1.5, 30), wing(1.7, 2.1, 1.9, 1.5, -30))
    return minus(shape, rect(cx - 0.5 * s, cy - 5 * s, 1 * s, 10 * s))


def cycle_ring(S):
    """Two clockwise arcs with arrowheads around the centre (a life cycle)."""
    parts = []
    r = 8.5
    for a0, a1 in ((200, 330), (20, 150)):
        parts.append(line(arc(12, 12, r, a0, a1)))
        tip = pt_on(12, 12, r, a1)
        t = math.radians(a1 + 90)
        n = math.radians(a1)
        back = (tip[0] - 2.6 * math.cos(t), tip[1] - 2.6 * math.sin(t))
        b1 = (back[0] + 2.6 * math.cos(n), back[1] + 2.6 * math.sin(n))
        b2 = (back[0] - 2.6 * math.cos(n), back[1] - 2.6 * math.sin(n))
        parts.append(line(poly([b1, tip, b2], r=S.r * 0.4)))
    return parts


def sparkle(cx, cy, r):
    """Four-pointed sparkle (solid mark)."""
    pts = [pt_on(cx, cy, r if i % 2 == 0 else r * 0.38, -90 + i * 45) for i in range(8)]
    return poly(pts, closed=True)


def soft(S, d, k=0.6):
    """Region d with its corners rounded by k in Rounded (unchanged in Line)."""
    if S.name == "line":
        return d
    inner = D(P(d), ST(d, 2 * k, "round", "round"))
    return path_to_d(U(inner, ST(path_to_d(inner), 2 * k, "round", "round")))


def clip(d, box):
    """Intersection of two regions."""
    from geometry import I
    return path_to_d(I(P(d), P(box)))


def mortarboard(cx, cy, w, h):
    """Flat mortarboard top (rhombus) centred on (cx, cy)."""
    return [(cx - w / 2, cy), (cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2)]


# ============================================================================ school subjects

@icon("math-class", CAT, "Chalkboard on legs showing a plus and a times sign",
      tags=["maths lesson", "mathematics", "arithmetic", "school subject", "chalkboard", "numeracy"])
def _(S):
    return [*board(S),
            detail(seg(5.5, 10.5, 10.5, 10.5)), detail(seg(8, 8, 8, 13)),
            detail(seg(14, 8.5, 18, 12.5)), detail(seg(18, 8.5, 14, 12.5))]


@icon("music-class", CAT, "Chalkboard on legs showing a pair of beamed eighth notes",
      tags=["music lesson", "music education", "notes", "school subject", "choir", "chalkboard"])
def _(S):
    return [*board(S),
            detail(poly([(10, 13), (10, 7), (16, 6.5), (16, 12)], r=S.r * 0.4)),
            dot(8.4, 13.2, 1.8), dot(14.4, 12.2, 1.8)]


@icon("language-arts", CAT, "Capital letter A standing above an open book",
      tags=["english class", "literacy", "reading", "writing", "alphabet", "school subject"])
def _(S):
    book = poly([(12, 16), (21.5, 14.5), (21.5, 20), (12, 21.5), (2.5, 20), (2.5, 14.5)], closed=True, r=S.r * 0.5)
    return [line(poly([(6.5, 12), (12, 2.5), (17.5, 12)], r=S.r * 0.5), stroke_miterlimit="4"),
            line(seg(8.8, 8.5, 15.2, 8.5)),
            shell(book), detail(seg(12, 16, 12, 21.5))]


@icon("social-studies-class", CAT, "Globe resting on a closed textbook",
      tags=["geography", "history", "civics", "social science", "world", "school subject"])
def _(S):
    return [shell(circle(12, 7.5, 5)),
            detail(seg(7, 7.5, 17, 7.5)), detail(ellipse(12, 7.5, L(S, 2, 2.2), 5)),
            shell(rect(3, 15.5, 18, 5.5, rr(S, 2))), detail(seg(6.5, 18.25, 21, 18.25))]


@icon("home-economics-class", CAT, "Wooden spoon standing beside a spool of thread",
      tags=["home ec", "family and consumer science", "cooking class", "sewing class", "life skills"])
def _(S):
    return [shell(ellipse(6.5, 7, 3.5, 4.5)), line(seg(6.5, 11.5, 6.5, 21.5)),
            line(seg(12.5, 4, 21.5, 4)), line(seg(12.5, 21, 21.5, 21)),
            shell(rect(14, 4, 6, 17, L(S, 0, 1))),
            detail(seg(14, 9, 20, 11.5)), detail(seg(14, 13.5, 20, 16))]


@icon("shop-class", CAT, "Hand saw held above a wooden plank",
      tags=["woodshop", "woodworking", "technology class", "carpentry", "industrial arts", "diy"])
def _(S):
    teeth = []
    for i in range(5):
        x = 3.5 + i * 2.4
        teeth += [(x, 10), (x + 1.2, 11.3)]
    blade = [(3, 7), (15, 4.5), (15, 10.5)] + [(x, y) for x, y in reversed(teeth)] + [(3, 10)]
    return [shell(poly(blade, closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
            shell(rect(15, 3.5, 6.5, 8, rr(S, 2.5))), detail(seg(17.5, 6, 17.5, 9)),
            shell(rect(2.5, 15, 19, 5.5, rr(S, 1.5))), detail(seg(6, 17.75, 13, 17.75))]


@icon("computer-lab", CAT, "Two desktop monitors side by side on one long desk",
      tags=["ict suite", "computer room", "it class", "computing lesson", "workstations", "media lab"])
def _(S):
    return [shell(rect(2.5, 3.5, 8, 7, rr(S, 1.5))), shell(rect(13.5, 3.5, 8, 7, rr(S, 1.5))),
            line(seg(6.5, 10.5, 6.5, 13.5)), line(seg(17.5, 10.5, 17.5, 13.5)),
            line(seg(2, 14.5, 22, 14.5)), line(seg(4.5, 14.5, 4.5, 21)), line(seg(19.5, 14.5, 19.5, 21))]


@icon("chemistry-class", CAT, "Chalkboard on legs showing a benzene ring beside a conical flask",
      tags=["chemistry lesson", "science class", "lab class", "molecule", "school subject", "chalkboard"])
def _(S):
    hexa = poly(regular(8.75, 10.5, 2.9, 6, start=0), closed=True, r=S.r * 0.3)
    flask = poly([(15.25, 6.5), (17.25, 6.5), (17.25, 9), (19, 14), (13.5, 14), (15.25, 9)], closed=True, r=S.r * 0.3)
    return [*board(S), detail(hexa), detail(flask)]


@icon("physics-class", CAT, "Chalkboard on legs showing a ball on a ramp and a swinging pendulum",
      tags=["physics lesson", "mechanics", "forces", "motion", "science class", "chalkboard"])
def _(S):
    return [*board(S),
            detail(poly([(5.5, 14.5), (12, 14.5), (12, 9.5)], closed=True, r=S.r * 0.3)),
            dot(7.3, 10.2, 1.6),
            detail(seg(16, 4, 17, 10)), dot(17.2, 11.6, 1.9)]


@icon("biology-class", CAT, "Chalkboard on legs showing a leaf and a round cell with a nucleus",
      tags=["biology lesson", "life science", "cells", "plants", "science class", "chalkboard"])
def _(S):
    return [*board(S),
            detail(circle(8.5, 10.5, 3.3)), dot(8.5, 10.5, 1.1),
            detail(lens(14, 14, 18.5, 7, 1.6)), detail(seg(14, 14, 16.5, 10.3))]


# ============================================================================ STEM kits and classroom science

@icon("block-coding", CAT, "Three puzzle-notched code blocks stacked like a program",
      tags=["visual programming", "coding for kids", "drag and drop code", "blocks", "computing", "stem"])
def _(S):
    def block(x0, x1, yt, yb, top_dent, bottom_tab):
        k = S.r * 0.3
        pts = [(x0, yt)]
        if top_dent:
            pts += [(7, yt), (7.75, yt + 1.5), (10.25, yt + 1.5), (11, yt)]
        pts += [(x1, yt), (x1, yb)]
        if bottom_tab:
            pts += [(11, yb), (10.25, yb + 1.5), (7.75, yb + 1.5), (7, yb)]
        pts += [(x0, yb)]
        return shell(poly(pts, closed=True, r=k), stroke_miterlimit="2")
    return [block(3, 16, 2.5, 6.5, False, True), block(3, 21, 10, 14, True, True), block(3, 13, 17.5, 21.5, True, False)]


@icon("circuit-kit", CAT, "Snap circuit board with a battery, a switch and a bulb joined by wires",
      tags=["electronics kit", "snap circuits", "electric circuit", "stem kit", "bulb", "battery"])
def _(S):
    k = S.r * 0.5
    return [shell(rect(2.5, 3, 19, 18, rr(S, 2.5))),
            detail(poly([(9.75, 9), (7, 9), (7, 10.5)], r=k)),
            detail(poly([(7, 15), (7, 17), (10, 17)], r=k)),
            detail(seg(10, 17, 13.5, 15)),
            detail(poly([(14, 17), (17, 17), (17, 9), (14.25, 9)], r=k)),
            detail(circle(12, 9, 2.25)),
            mark(rect(5, 10.5, 4, 4.5, L(S, 0, 1)))]


@icon("butterfly-habitat", CAT, "Tall pop-up mesh habitat with a butterfly resting inside",
      tags=["butterfly kit", "insect habitat", "caterpillar enclosure", "life science", "mesh cage"])
def _(S):
    return [shell(rect(4, 2.5, 16, 19, rr(S, 3))),
            detail(seg(4, 5.5, 20, 5.5)), detail(seg(4, 18.5, 20, 18.5)),
            mark(butterfly(12, 12, 1.15))]


@icon("bean-in-a-jar", CAT, "Glass jar with a sprouting bean, its shoot rising out and roots growing down",
      tags=["germination", "seed experiment", "sprouting bean", "plant growth", "science experiment"])
def _(S):
    return [shell(rect(5, 9, 14, 12.5, rr(S, 3))),
            mark(ellipse(12, 15.3, 2.4, 1.7)),
            detail(seg(12, 13.5, 12, 9)), line(seg(12, 9, 12, 5.5)),
            shell(lens(12, 5.5, 7.5, 3, 1.3)), shell(lens(12, 5.5, 16.5, 3.5, 1.3)),
            detail(seg(11, 17, 10, 19)), detail(seg(13, 17, 14, 19))]


@icon("parts-of-a-plant", CAT, "Flowering plant with roots below the soil and label lines pointing at its parts",
      tags=["plant diagram", "plant anatomy", "botany", "labelled diagram", "life science", "flower parts"])
def _(S):
    return [shell(circle(7.5, 5, 2.5)),
            line(seg(7.5, 7.5, 7.5, 15)),
            shell(lens(7.5, 11.5, 11.8, 9.2, 1.2)),
            line(seg(2.5, 15, 12.5, 15)),
            line(poly([(7.5, 15), (7.5, 19.5)])), line(seg(5.5, 17, 4.5, 19.5)), line(seg(9.5, 17, 10.5, 19.5)),
            line(seg(12.5, 5, 21.5, 5)), line(seg(14.5, 10, 21.5, 10)), line(seg(14, 18.5, 21.5, 18.5))]


# ============================================================================ life cycles and experiments

@icon("butterfly-life-cycle", CAT, "Butterfly inside a ring of arrows showing its life cycle",
      tags=["metamorphosis", "life cycle", "caterpillar", "chrysalis", "science lesson", "insects"])
def _(S):
    return [*cycle_ring(S), mark(butterfly(12, 12, 1.2))]


@icon("plant-life-cycle", CAT, "Seedling inside a ring of arrows showing a plant's life cycle",
      tags=["life cycle", "germination", "seed to plant", "growth", "science lesson", "botany"])
def _(S):
    return [*cycle_ring(S), line(seg(12, 16, 12, 11)),
            shell(lens(12, 11.5, 8, 8.5, 1.3)), shell(lens(12, 11.5, 16, 8.5, 1.3))]


@icon("lung-model-balloon", CAT, "Bottle lung model: a Y-shaped straw holding two balloons above a rubber sheet",
      tags=["lung model", "breathing model", "diaphragm model", "bell jar", "respiration", "science experiment"])
def _(S):
    bottle = poly([(9, 3.5), (15, 3.5), (15, 5.5), (20, 8.5), (20, 18), (4, 18), (4, 8.5), (9, 5.5)], closed=True, r=S.r)
    return [shell(bottle),
            line(seg(12, 2, 12, 4.5)), detail(seg(12, 4.5, 12, 10)),
            detail(poly([(8.5, 13), (12, 10), (15.5, 13)], r=S.r * 0.5)),
            mark(circle(8.5, 14, 2.1)), mark(circle(15.5, 14, 2.1)),
            line("M4 18Q12 22.5 20 18")]


@icon("magnet-wand", CAT, "Magnet wand with a round tip lifting a chain of paperclips",
      tags=["magnetism", "magnet", "paperclips", "science experiment", "attraction", "stem"])
def _(S):
    wand = union(rect(2.5, 5, 10, 3, L(S, 0, 1.5)), circle(15.5, 6.5, 3.5))
    return [shell(wand),
            shell(rect(13.5, 11.5, 4, 5, rr(S, 2))), shell(rect(15, 17.5, 4, 4.5, rr(S, 2)))]


@icon("soda-geyser", CAT, "Soda bottle with a tall fountain of foam spraying from its mouth",
      tags=["mentos experiment", "diet cola geyser", "soda fountain", "chemical reaction", "science experiment"])
def _(S):
    foam = union(circle(8, 6.5, 3), circle(12, 5, 3), circle(16, 6.5, 3), rect(10.5, 6, 3, 4.5, 0))
    return [shell(foam),
            shell(poly([(10.5, 13), (13.5, 13), (13.5, 14.5), (15.5, 16.5), (15.5, 21.5), (8.5, 21.5), (8.5, 16.5), (10.5, 14.5)], closed=True, r=S.r * 0.6)),
            dot(5, 12, 1.25), dot(19, 12, 1.25)]


@icon("elephant-toothpaste", CAT, "Conical flask with a thick column of foam overflowing and running down its sides",
      tags=["foam experiment", "chemical reaction", "hydrogen peroxide", "catalyst", "science demo", "chemistry"])
def _(S):
    foam = union(circle(8, 6.5, 3), circle(12, 5, 3.2), circle(16, 6.5, 3),
                 rect(3.5, 6.5, 3, 7, 1.5), rect(17.5, 6.5, 3, 7, 1.5))
    flask = poly([(10, 11), (14, 11), (14, 13), (19.5, 21.5), (4.5, 21.5), (10, 13)], closed=True, r=S.r)
    return [shell(foam), shell(minus(flask, grow(foam, 3)))]


# ============================================================================ maths, literacy and crafts

@icon("two-color-counters", CAT, "Two overlapping round counters, one outlined and one solid",
      tags=["double sided counters", "math manipulatives", "counting chips", "integers", "counters"])
def _(S):
    b = circle(15.5, 15.5, 5.5)
    return [shell(minus(circle(8.5, 8.5, 5.5), grow(b, 3))), detail(arc(8.5, 8.5, 2.5, 185, 275)), mark(b)]


@icon("pictograph", CAT, "Picture chart: three labelled rows of repeated symbols of different lengths",
      tags=["pictogram", "picture graph", "tally chart", "data handling", "statistics", "chart"])
def _(S):
    parts = []
    for y, n in ((5, 3), (12, 1), (19, 2)):
        parts.append(line(seg(2.5, y, 6.5, y)))
        parts += [dot(10.5 + 5 * i, y, 1.9) for i in range(n)]
    return parts


@icon("story-dice", CAT, "Two picture dice, one showing a moon and the other a star",
      tags=["story cubes", "storytelling", "creative writing", "picture dice", "prompt", "literacy game"])
def _(S):
    a = rect(2.5, 9.5, 11.5, 11.5, rr(S, 2.5))
    b = rot(rect(12, 3.5, 9, 9, rr(S, 2.5)), 15, 16.5, 8)
    moon = minus(circle(8.25, 15.25, 3), circle(9.75, 13.75, 2.4))
    star = rot(poly([pt_on(16.5, 8, 2.6 if i % 2 == 0 else 1.1, -90 + i * 36) for i in range(10)], closed=True), 15, 16.5, 8)
    return [shell(a), shell(minus(b, grow(a, 3))), mark(moon), mark(star)]


@icon("big-book-easel", CAT, "Oversized open picture book standing on a low floor easel",
      tags=["big book", "shared reading", "story time", "read aloud", "book stand", "early years"])
def _(S):
    book = poly([(12, 5), (21.5, 3), (21.5, 14.5), (12, 16.5), (2.5, 14.5), (2.5, 3)], closed=True, r=S.r * 0.5)
    return [shell(book), detail(seg(12, 5, 12, 16.5)),
            line(seg(2, 18.5, 22, 18.5)), line(seg(6, 18.5, 4.5, 21.5)), line(seg(18, 18.5, 19.5, 21.5))]


@icon("safety-scissors", CAT, "Child's safety scissors with short blunt blades and chunky loop handles",
      tags=["kids scissors", "blunt scissors", "school scissors", "craft", "cutting", "preschool"])
def _(S):
    hl = rot(ellipse(7.5, 16.5, 4.5, 4), 25, 7.5, 16.5)
    hr = rot(ellipse(16.5, 16.5, 4.5, 4), -25, 16.5, 16.5)
    body = union(rect(9.5, 2.5, 5, 12, L(S, 2, 2.5)), hl, hr)
    return [shell(body), detail(seg(12, 5, 12, 12)),
            detail(ellipse(7.3, 17, 1.8, 1.5)), detail(ellipse(16.7, 17, 1.8, 1.5))]


@icon("loop-scissors", CAT, "Loop scissors: crossed blades whose handles are joined by one springy loop",
      tags=["easy grip scissors", "adaptive scissors", "self opening scissors", "special needs", "cutting", "craft"])
def _(S):
    def blade(tip, base, w):
        dx, dy = base[0] - tip[0], base[1] - tip[1]
        ln = math.hypot(dx, dy)
        nx, ny = -dy / ln * w, dx / ln * w
        return poly([tip, (base[0] + nx, base[1] + ny), (base[0] - nx, base[1] - ny)], closed=True)
    blades = union(blade((4.5, 2.5), (14, 13), 1.6), blade((19.5, 2.5), (10, 13), 1.6))
    return [shell(blades, stroke_miterlimit="2"), dot(12, 10.8, 0.9),
            line("M14 13C19 17 17 21.5 12 21.5C7 21.5 5 17 10 13")]


@icon("paste-pot", CAT, "Round pot of school paste with a flat wooden spreader poking out of the lid",
      tags=["paste", "glue pot", "school glue", "craft glue", "gluing", "arts and crafts"])
def _(S):
    pot = union(rect(3.5, 8.5, 17, 3.5, rr(S, 1.5)), rect(5, 11, 14, 10.5, rr(S, 3)))
    stick = rot(rect(12.5, 1, 3, 9.5, 1.5), 20, 14, 5.75)
    return [shell(pot), shell(minus(stick, grow(pot, 3))), detail(seg(5, 12, 19, 12))]


@icon("glitter-glue", CAT, "Squeeze tube with a pointed nozzle drawing a line of glitter glue",
      tags=["glitter", "sparkle glue", "craft glue", "decorating", "arts and crafts", "kids craft"])
def _(S):
    tube = [shell(poly([(9, 2.5), (17, 2.5), (16, 11.5), (10, 11.5)], closed=True, r=S.r * 0.5)),
            detail(seg(9.3, 5, 16.7, 5)),
            shell(poly([(10.5, 11.5), (15.5, 11.5), (13, 16)], closed=True, r=S.r * 0.4))]
    tube = turn(tube, 35, 13, 9)
    return [*tube, line("M2.5 21C4.5 18 6.5 18 8 20C9.5 22 11.5 22 13 19.5"),
            mark(sparkle(18, 17.5, 3)), mark(sparkle(20.5, 11.5, 1.8))]


@icon("macaroni-art", CAT, "Sheet of paper with elbow macaroni glued in the shape of a flower",
      tags=["pasta art", "noodle craft", "kids craft", "collage", "preschool art", "arts and crafts"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 2.5))), dot(12, 12, 1.4)]
    for i in range(5):
        a = -90 + i * 72
        c = pt_on(12, 12, 4.4, a)
        parts.append(detail(arc(c[0], c[1], 1.6, a - 90, a + 90)))
    return parts


@icon("pasta-necklace", CAT, "Hanging string threaded with tube pasta beads",
      tags=["macaroni necklace", "pasta beads", "threading", "kids craft", "fine motor", "jewellery craft"])
def _(S):
    parts = [line("M4 2.5C4 15 8 20.5 12 20.5C16 20.5 20 15 20 2.5")]
    for x, y, a in ((5.3, 12, 72), (12, 20.5, 0), (18.7, 12, -72)):
        parts.append(shell(rot(rect(x - 2.4, y - 1.6, 4.8, 3.2, L(S, 0, 1.4)), a, x, y)))
    return parts


@icon("thumbprint-bugs", CAT, "Thumbprint bug: an oval print with drawn legs and antennae",
      tags=["fingerprint art", "thumbprint art", "kids craft", "ink pad", "insect craft", "preschool art"])
def _(S):
    parts = [shell(ellipse(12, 13.5, 5, 6.5)),
             detail(arc(12, 14, 2.6, 180, 360)), detail(arc(12, 14.2, 2.6, 0, 120)),
             line(seg(10.5, 7.5, 8.5, 3.5)), line(seg(13.5, 7.5, 15.5, 3.5))]
    for y in (11, 14.5, 18):
        parts += [line(seg(6.5, y, 3, y + 0.5)), line(seg(17.5, y, 21, y + 0.5))]
    return parts


@icon("paper-weaving-mat", CAT, "Square mat of paper strips woven over and under in a checked pattern",
      tags=["paper weaving", "woven mat", "kids craft", "over under", "pattern", "arts and crafts"])
def _(S):
    frame = rect(3, 3, 18, 18, rr(S, 3))
    parts = [shell(frame)]
    for r in range(4):
        for c in range(4):
            if (r + c) % 2 == 0:
                parts.append(mark(soft(S, clip(rect(4 + c * 4, 4 + r * 4, 4, 4), rect(3, 3, 18, 18, rr(S, 3))))))
    return parts


@icon("cardboard-tube-craft", CAT, "Cardboard tube animal with pointed ears and big googly eyes",
      tags=["toilet roll craft", "paper roll craft", "recycled craft", "kids craft", "owl craft", "arts and crafts"])
def _(S):
    body = union(rect(6, 7, 12, 14.5, rr(S, 2)), poly([(6, 8), (6.5, 2.5), (10.5, 7)], closed=True),
                 poly([(18, 8), (17.5, 2.5), (13.5, 7)], closed=True))
    return [shell(body, stroke_miterlimit="3"), dot(9.6, 11.5, 1.9), dot(14.4, 11.5, 1.9),
            detail("M6 18Q12 20 18 18")]


@icon("paper-bag-puppet", CAT, "Paper bag puppet with a face on the folded flap and a mouth under the fold",
      tags=["puppet", "paper bag craft", "puppet show", "storytelling", "kids craft", "drama"])
def _(S):
    top = [(5, 3.5)] + [(5 + i * 1.75, 2.5 if i % 2 else 4) for i in range(1, 8)] + [(19, 3.5)]
    bag = poly(top + [(19, 21.5), (5, 21.5)], closed=True, r=S.r * 0.3)
    return [shell(bag, stroke_miterlimit="2"),
            detail(seg(5, 12, 19, 12)),
            dot(9.5, 8, 1.3), dot(14.5, 8, 1.3),
            detail("M9 14.5Q12 17.5 15 14.5")]


@icon("egg-carton-caterpillar", CAT, "Caterpillar made from a row of joined egg carton cups with antennae",
      tags=["egg box craft", "recycled craft", "caterpillar craft", "kids craft", "bug craft", "arts and crafts"])
def _(S):
    body = union(circle(6, 14.5, 3.5), circle(12.5, 15, 3.2), circle(18.5, 15, 3.2), rect(2.5, 14.5, 19.5, 5, L(S, 0, 1.5)))
    return [shell(body), detail(seg(9.25, 14.5, 9.25, 19.5)), detail(seg(15.5, 14.5, 15.5, 19.5)),
            dot(5.2, 14.8, 1.1),
            line(seg(4.5, 10.5, 3.2, 6.5)), line(seg(7.5, 10.5, 8.8, 6.5)), dot(3, 4.8, 1.25), dot(9, 4.8, 1.25)]


# ============================================================================ PE and games


@icon("play-parachute", CAT, "Round play parachute with alternating panels and a ball in the middle",
      tags=["parachute game", "gym parachute", "pe equipment", "cooperative game", "rainbow parachute"])
def _(S):
    parts = [shell(circle(12, 12, 9)), dot(12, 12, 2)]
    for i in range(4):
        a0 = -90 + i * 90
        a1 = a0 + 45
        p0, p1 = pt_on(12, 12, 4, a0), pt_on(12, 12, 4, a1)
        q0, q1 = pt_on(12, 12, 8.2, a0), pt_on(12, 12, 8.2, a1)
        w = (f"M{fmt(p0[0])} {fmt(p0[1])}L{fmt(q0[0])} {fmt(q0[1])}A8.2 8.2 0 0 1 {fmt(q1[0])} {fmt(q1[1])}"
             f"L{fmt(p1[0])} {fmt(p1[1])}A4 4 0 0 0 {fmt(p0[0])} {fmt(p0[1])}Z")
        parts.append(mark(soft(S, w, 1.4)))
    return parts


@icon("house-points-tubes", CAT, "Clear tubes of house points filled with tokens to different heights",
      tags=["house points", "reward system", "class points", "token tubes", "school houses", "behaviour chart"])
def _(S):
    parts = []
    for x, lvl in ((4.75, 12), (12, 7), (19.25, 15)):
        tube = f"M{fmt(x - 1.75)} 3V19.75A1.75 1.75 0 0 0 {fmt(x + 1.75)} 19.75V3"
        parts.append(line(tube))
        parts.append(mark(f"M{fmt(x - 1.75)} {lvl}H{fmt(x + 1.75)}V19.75A1.75 1.75 0 0 1 {fmt(x - 1.75)} 19.75Z"))
    return parts


@icon("training-pinnie", CAT, "Sleeveless mesh training bib with a wide neck and dotted mesh texture",
      tags=["pinnie", "training bib", "scrimmage vest", "team bib", "pe kit", "sports vest"])
def _(S):
    vest = poly([(6.5, 2.5), (9.5, 2.5), (12, 7), (14.5, 2.5), (17.5, 2.5), (18, 8), (19.5, 10.5), (19.5, 21.5),
                 (4.5, 21.5), (4.5, 10.5), (6, 8)], closed=True, r=S.r * 0.6)
    parts = [shell(vest)]
    for y, xs in ((12.5, (9, 12, 15)), (15.5, (7.5, 10.5, 13.5, 16.5)), (18.5, (9, 12, 15))):
        parts += [dot(x, y, 1) for x in xs]
    return parts


@icon("kickball", CAT, "Shoe kicking a rubber playground ball with motion lines",
      tags=["kick ball", "playground ball", "pe game", "recess", "kicking", "school sports"])
def _(S):
    shoe = poly([(2.5, 21), (2.5, 14.5), (7, 14.5), (9.5, 16.5), (13, 16.5), (16, 18), (16, 21)], closed=True, r=S.r * 0.6)
    return [shell(shoe), line(seg(4.5, 14.5, 4.5, 10)),
            shell(circle(16.5, 7.5, 4.5)),
            line(seg(7.5, 9, 10.5, 7.5)), line(seg(7, 4.5, 10, 4.5))]


# ============================================================================ getting to school

@icon("school-bus-stop-arm", CAT, "Side of a school bus with its octagonal stop arm swung out",
      tags=["bus stop sign", "stop arm", "school bus safety", "stop paddle", "student pickup", "traffic law"])
def _(S):
    octa = poly(regular(18.25, 10, 3.9, 8, start=22.5), closed=True, r=S.r * 0.3)
    wheels = [circle(5, 18.5, 2), circle(10.5, 18.5, 2)]
    body = minus(rect(2, 3, 11, 14.5, rr(S, 2.5)), *[grow(w, 3) for w in wheels])
    return [shell(body), detail(rect(4.5, 5.5, 6, 4, L(S, 0, 1))),
            shell(wheels[0]), shell(wheels[1]),
            line(seg(13, 10, 14.5, 10)), shell(octa)]


@icon("walking-school-bus", CAT, "Adult leading two small children who hold a shared rope",
      tags=["walk to school", "walking bus", "pedestrian safety", "school run", "group walk", "crossing"])
def _(S):
    rope = "M8.5 15H21.5"
    kid1 = "M11 21.5V16.5A2 2 0 0 1 15 16.5V21.5Z"
    kid2 = "M17.5 21.5V16.5A2 2 0 0 1 21.5 16.5V21.5Z"
    return [shell(circle(5.5, 4.5, 2.25)), shell("M2.5 21.5V12A3 3 0 0 1 8.5 12V21.5Z"),
            shell(circle(13, 11.5, 1.75)), shell(minus(kid1, grow(rope, 2.5))),
            shell(circle(19.5, 11.5, 1.75)), shell(minus(kid2, grow(rope, 2.5))),
            line(rope)]


# ============================================================================ tests and grading


@icon("failing-grade", CAT, "Test paper marked with a large letter F",
      tags=["fail", "f grade", "failed test", "bad grade", "report card", "exam result"])
def _(S):
    return [sheet(S), detail(poly([(15.5, 7), (9.5, 7), (9.5, 17.5)], r=S.r * 0.5)), detail(seg(9.5, 12, 14, 12))]


@icon("open-book-exam", CAT, "Open book lying in front of a test paper",
      tags=["open book test", "take home exam", "reference allowed", "exam", "assessment", "study"])
def _(S):
    book = poly([(8.75, 15), (15, 13.5), (15, 20), (8.75, 21.5), (2.5, 20), (2.5, 13.5)], closed=True, r=S.r * 0.5)
    paper = rect(9.5, 2.5, 12, 15.5, rr(S, 2))
    return [shell(minus(paper, grow(book, 3))), detail(seg(12.5, 6.5, 18.5, 6.5)), detail(seg(12.5, 10, 18.5, 10)),
            shell(book), detail(seg(8.75, 15, 8.75, 21.5))]


@icon("pop-quiz", CAT, "Test paper with a question mark beside a lightning bolt",
      tags=["surprise quiz", "unannounced test", "quick quiz", "quiz", "test", "question"])
def _(S):
    bolt = poly([(20.5, 2.5), (15.5, 12.5), (18.5, 12.5), (16.5, 21.5), (22, 9.5), (19, 9.5), (21.5, 2.5)], closed=True, r=S.r * 0.3)
    return [shell(rect(2.5, 3.5, 11.5, 18, rr(S, 2.5))),
            detail("M6 9.5A2.25 2.25 0 1 1 9.4 11.4C8.5 12 8.25 12.6 8.25 13.75"), dot(8.25, 17, 1.2),
            shell(bolt, stroke_miterlimit="2")]


@icon("exam-retake", CAT, "Test paper with a circular arrow looping around its corner",
      tags=["resit", "retest", "retake exam", "second attempt", "try again", "make up test"])
def _(S):
    ring = circle(17, 17, 4.5)
    parts = [shell(minus(rect(3, 2.5, 14.5, 17.5, rr(S, 2.5)), grow(ring, 3))),
             detail(seg(6.5, 7, 13.5, 7)), detail(seg(6.5, 10.5, 11, 10.5)),
             line(arc(17, 17, 4.5, 250, 160))]
    tip = pt_on(17, 17, 4.5, 160)
    parts.append(line(poly([(tip[0] - 0.6, tip[1] - 3), tip, (tip[0] + 2.6, tip[1] - 1)], r=S.r * 0.4)))
    return parts


@icon("test-anxiety", CAT, "Worried face with sweat drops above a test paper",
      tags=["exam stress", "exam nerves", "stress", "anxiety", "worried student", "pressure"])
def _(S):
    drop = "M0 -2.2C0.9 -0.9 1.5 0 1.5 0.7A1.5 1.5 0 0 1 -1.5 0.7C-1.5 0 -0.9 -0.9 0 -2.2Z"
    return [shell(circle(10, 7.75, 5.25)), dot(8.2, 6.8, 0.9), dot(11.8, 6.8, 0.9),
            detail("M7.8 10.6Q8.9 9.6 10 10.6Q11.1 11.6 12.2 10.6"),
            mark(mv(drop, 18, 5)), mark(mv(drop, 20.5, 10)),
            shell(rect(3, 16, 18, 5, rr(S, 1.5))), detail(seg(6, 18.5, 18, 18.5))]


@icon("sealed-exam-papers", CAT, "Envelope closed with a round seal and a diagonal security stripe",
      tags=["exam papers", "confidential", "sealed envelope", "secure delivery", "exam board", "tamper evident"])
def _(S):
    env = rect(2, 5, 20, 14, rr(S, 2))
    return [shell(env), detail(poly([(2, 5.5), (12, 12.5), (22, 5.5)], r=S.r * 0.5)),
            dot(12, 12.5, 2.5),
            detail(seg(15.5, 19, 20, 15)), ]


@icon("grading-papers", CAT, "Stack of papers with a pen ticking the top sheet",
      tags=["marking", "grading", "teacher", "assessment", "correcting homework", "red pen"])
def _(S):
    tip, end = (13, 15), (20.3, 5.3)
    dx, dy = end[0] - tip[0], end[1] - tip[1]
    ln = math.hypot(dx, dy)
    ux, uy, nx, ny = dx / ln, dy / ln, -dy / ln, dx / ln
    def at(u, v):
        return (tip[0] + ux * u + nx * v, tip[1] + uy * u + ny * v)
    w = 1.9
    pen = poly([at(0, 0), at(3.5, w), at(ln, w), at(ln, -w), at(3.5, -w)], closed=True, r=S.r * 0.4)
    front = rect(2.5, 5.5, 13, 16, rr(S, 2.5))
    return [line(poly([(6, 2.5), (17.5, 2.5), (17.5, 4)], r=S.r * 0.5)),
            shell(minus(front, grow(pen, 3))),
            detail(poly([(5.5, 14.5), (7.5, 16.5), (10.5, 12.5)], r=S.r * 0.3)),
            shell(pen), detail(seg(*at(6.5, -w), *at(6.5, w)))]


@icon("tardy-slip", CAT, "Small late slip with a clock face and a signature line",
      tags=["late pass", "late note", "tardiness", "attendance", "office pass", "school office"])
def _(S):
    return [shell(rect(2, 5, 20, 14, rr(S, 2))),
            detail(circle(8, 12, 4)), detail(poly([(8, 9.75), (8, 12), (9.75, 12)], r=S.r * 0.3)),
            detail("M14 12.5C15 9.5 15.5 14 16.5 11.5C17.2 9.8 17.8 12.8 19 11.5"), detail(seg(14, 15.5, 19.5, 15.5))]


# ============================================================================ pencils and small supplies


@icon("pencil-topper", CAT, "Pencil with a round cartoon animal head fitted on its end",
      tags=["pencil topper", "pencil charm", "novelty stationery", "kids stationery", "bear topper"])
def _(S):
    head = union(circle(12, 7.5, 4), circle(8.5, 4.2, 1.8), circle(15.5, 4.2, 1.8))
    body = poly([(10, 11), (14, 11), (14, 17.5), (12, 21.5), (10, 17.5)], closed=True, r=S.r * 0.4)
    return [shell(union(head, body)), dot(10.5, 7.2, 0.9), dot(13.5, 7.2, 0.9), detail(seg(10, 17.5, 14, 17.5))]


@icon("pencil-grip", CAT, "Pencil with a triangular rubber grip sleeve near the tip",
      tags=["pencil grip", "handwriting aid", "writing grip", "occupational therapy", "fine motor", "stationery"])
def _(S):
    grip = rect(7.75, 11, 8.5, 6, L(S, 1, 2.5))
    body = poly([(10, 2.5), (14, 2.5), (14, 18.5), (12, 22), (10, 18.5)], closed=True, r=S.r * 0.4)
    parts = [shell(minus(body, grow(grip, 3))), shell(grip), detail(seg(12, 12.5, 12, 15.5)), detail(seg(10, 5.5, 14, 5.5))]
    return fit(turn(parts, 45))


@icon("mini-whiteboard", CAT, "Small handheld whiteboard with a written sum and a marker clipped to its side",
      tags=["mini whiteboard", "show me board", "dry erase board", "answer board", "assessment", "marker"])
def _(S):
    return [shell(rect(2.5, 4.5, 14, 15, rr(S, 2.5))),
            detail(seg(5.5, 9.5, 9.5, 9.5)), detail(seg(7.5, 7.5, 7.5, 11.5)),
            detail(seg(11.5, 8.5, 13.5, 8.5)), detail(seg(11.5, 11, 13.5, 11)),
            detail("M5.5 15.5C7 13.5 8 17 9.5 15C10.5 13.8 11.5 16 13.5 15"),
            shell(rect(18.5, 6.5, 3.5, 13, L(S, 0.5, 1.75))), shell(poly([(18.5, 6.5), (20.25, 3), (22, 6.5)], closed=True, r=S.r * 0.3))]


# ============================================================================ graduation

@icon("diploma-tube", CAT, "Long diploma tube with end caps and a ribbon tied around the middle",
      tags=["certificate tube", "document tube", "diploma holder", "graduation", "scroll case", "commencement"])
def _(S):
    body = union(rect(4, 9.5, 16, 5, L(S, 0, 0.5)), rect(2, 8.5, 4, 7, rr(S, 1.5)), rect(18, 8.5, 4, 7, rr(S, 1.5)))
    parts = [shell(body), detail(seg(6, 8.5, 6, 15.5)), detail(seg(18, 8.5, 18, 15.5)), detail(seg(12, 9.5, 12, 14.5)),
             line(seg(12, 14.5, 10, 19)), line(seg(12, 14.5, 14, 19))]
    return fit(turn(parts, -35))


@icon("kindergarten-graduation", CAT, "Small child wearing an oversized tilted mortarboard cap",
      tags=["preschool graduation", "kindergarten", "moving up day", "pre k graduation", "little graduate", "nursery graduation"])
def _(S):
    cap = rot(poly(mortarboard(12, 7, 19, 6), closed=True, r=S.r * 0.5), -10, 12, 7)
    head = circle(12, 13.5, 4.5)
    return [shell(cap, stroke_miterlimit="2"), shell(minus(head, grow(cap, 3))), dot(10.3, 14, 0.9), dot(13.7, 14, 0.9),
            line("M5 21.5C5.5 19.5 7 18.7 8.5 18.5"), line("M19 21.5C18.5 19.5 17 18.7 15.5 18.5"),
            line(seg(20.2, 5.4, 20.2, 10))]


@icon("graduation-cake", CAT, "Round cake topped with a mortarboard cap and tassel",
      tags=["graduation party", "celebration cake", "commencement", "grad party", "congratulations", "dessert"])
def _(S):
    return [shell(poly(mortarboard(12, 6.5, 15, 5.5), closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
            line(seg(19.5, 6.5, 19.5, 10)),
            shell(rect(3, 12.5, 18, 9, rr(S, 2.5))),
            detail("M3 15.5C5 17.5 7 17.5 9 15.5C11 17.5 13 17.5 15 15.5C17 17.5 19 17.5 21 15.5")]


@icon("graduation-balloons", CAT, "Two round balloons with a mortarboard-shaped balloon between them",
      tags=["graduation party", "balloons", "grad party", "celebration", "commencement", "decorations"])
def _(S):
    cap = union(poly(mortarboard(12, 5, 9, 4), closed=True), rect(9.75, 5, 4.5, 3.5, 1))
    return [shell(ellipse(5.5, 9, 3, 3.8)), shell(ellipse(18.5, 9, 3, 3.8)), shell(soft(S, cap, 0.5), stroke_miterlimit="2"),
            line("M5.5 12.8C5.5 15.5 7 17 7 21.5"), line("M18.5 12.8C18.5 15.5 17 17 17 21.5"), line(seg(12, 8.5, 12, 21.5))]


@icon("graduation-photo", CAT, "Framed portrait of a graduate wearing a mortarboard",
      tags=["grad photo", "graduation portrait", "yearbook photo", "picture frame", "commencement", "memories"])
def _(S):
    return [shell(rect(3, 2.5, 18, 19, rr(S, 2.5))),
            mark(soft(S, poly(mortarboard(12, 7.5, 11, 4), closed=True), 0.5)),
            mark(circle(12, 12.3, 2.7)),
            mark("M6.5 20.5A5.5 4.2 0 0 1 17.5 20.5Z")]


@icon("decorated-graduation-cap", CAT, "Mortarboard decorated with flowers on its top and a hanging tassel",
      tags=["cap decorating", "decorated mortarboard", "grad cap design", "graduation", "diy", "commencement"])
def _(S):
    parts = [shell(poly(mortarboard(12, 9, 20, 12), closed=True, r=S.r), stroke_miterlimit="2"),
             line("M7 13.5V17.5C7 19 9.2 20.5 12 20.5C14.8 20.5 17 19 17 17.5V13.5"),
             line(seg(21, 9.5, 21, 15.5))]
    for cx, cy in ((7.5, 9), (12, 6.6), (12, 11.4), (16.5, 9)):
        parts.append(mark(union(*[circle(*pt_on(cx, cy, 1.05, a), 0.95) for a in range(-90, 270, 72)])))
    return parts


@icon("graduation-teddy-bear", CAT, "Teddy bear wearing a mortarboard and holding a rolled diploma",
      tags=["grad bear", "graduation gift", "plush toy", "teddy", "commencement", "keepsake"])
def _(S):
    cap = poly(mortarboard(12, 4, 12, 3.6), closed=True)
    head = union(circle(12, 10, 4.2), circle(7.3, 6.9, 2.3), circle(16.7, 6.9, 2.3))
    body = ellipse(12, 18, 6, 3.8)
    return [shell(soft(S, cap, 0.4)), shell(minus(head, grow(cap, 3))),
            dot(10.3, 9.2, 0.85), dot(13.7, 9.2, 0.85), detail(ellipse(12, 12, 1.9, 1.3)),
            shell(minus(body, grow(head, 3))), detail(seg(8, 19.5, 16, 16.5))]


@icon("graduation-ceremony", CAT, "Three graduates in mortarboards seen from behind facing a banner",
      tags=["commencement", "convocation", "graduation day", "graduates", "ceremony", "class of"])
def _(S):
    parts = [shell(rect(3, 2.5, 18, 5, rr(S, 1.5))), detail(seg(7, 5, 17, 5))]
    for x in (4.5, 12, 19.5):
        parts += [shell(poly(mortarboard(x, 12.5, 5.5, 2.5), closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
                  shell(f"M{fmt(x - 2)} 21.5V17A2 2 0 0 1 {fmt(x + 2)} 17V21.5Z")]
    return parts


@icon("tassel-turning", CAT, "Mortarboard with a curved arrow showing the tassel moving from one side to the other",
      tags=["turn the tassel", "graduation tradition", "commencement", "graduated", "degree conferred"])
def _(S):
    parts = [shell(poly(mortarboard(12, 12.5, 18, 7), closed=True, r=S.r), stroke_miterlimit="2"),
             line("M7 15V18.5C7 19.9 9.2 21 12 21C14.8 21 17 19.9 17 18.5V15"),
             line(seg(20.5, 13, 20.5, 18)),
             line("M6 6.5Q12 1 18 6.5")]
    parts.append(line(poly([(15.2, 6.8), (18, 6.5), (17.9, 3.7)], r=S.r * 0.4)))
    return parts


# ============================================================================ study habits


@icon("memory-palace", CAT, "House outline with numbered spots in its rooms linked by a path",
      tags=["method of loci", "memory technique", "mind palace", "recall", "study skills", "memorization"])
def _(S):
    return [shell(poly([(3, 10.5), (12, 3), (21, 10.5), (21, 21.5), (3, 21.5)], closed=True, r=S.r)),
            detail(poly([(7.5, 17.5), (11, 12.5), (16.5, 17)], r=S.r * 0.5)),
            dot(7.5, 17.5, 1.7), dot(11, 12.5, 1.7), dot(16.5, 17, 1.7)]


@icon("cramming", CAT, "Student's head peeking out from behind a tall stack of books",
      tags=["last minute study", "exam prep", "studying", "revision", "all nighter", "books"])
def _(S):
    books = union(rect(4, 10, 15, 3.8, L(S, 0.5, 1.2)), rect(3, 13.8, 17, 3.9, L(S, 0.5, 1.2)), rect(4.5, 17.7, 16, 3.8, L(S, 0.5, 1.2)))
    return [shell(minus(circle(12, 8.5, 5), grow(books, 3))), dot(10.2, 6.3, 0.9), dot(13.8, 6.3, 0.9),
            shell(books), detail(seg(4, 13.8, 19, 13.8)), detail(seg(4.5, 17.7, 20, 17.7))]


@icon("summarizing", CAT, "Long page of text with an arrow pointing to a short page of three lines",
      tags=["summary", "summarise", "condense", "key points", "tl dr", "study skills"])
def _(S):
    parts = [shell(rect(2.5, 2.5, 8, 19, rr(S, 2))),
             *[detail(seg(5, y, 8, y)) for y in (6.5, 10, 13.5, 17)],
             line(seg(11.5, 12, 15, 12)), line(poly([(13.5, 10), (15.5, 12), (13.5, 14)], r=S.r * 0.4)),
             shell(rect(17, 6.5, 5, 11, rr(S, 1.5))), detail(seg(19.5, 9.5, 19.5, 14.5))]
    return parts


@icon("taking-notes", CAT, "Pen writing a line of notes on a lined notebook page",
      tags=["note taking", "notes", "writing", "lecture notes", "study", "notebook"])
def _(S):
    tip, end = (12, 17), (20.5, 6)
    dx, dy = end[0] - tip[0], end[1] - tip[1]
    ln = math.hypot(dx, dy)
    ux, uy, nx, ny = dx / ln, dy / ln, -dy / ln, dx / ln
    def at(u, v):
        return (tip[0] + ux * u + nx * v, tip[1] + uy * u + ny * v)
    w = 1.9
    pen = poly([at(0, 0), at(3.5, w), at(ln, w), at(ln, -w), at(3.5, -w)], closed=True, r=S.r * 0.4)
    page = rect(2.5, 2.5, 14, 19, rr(S, 2.5))
    return [shell(minus(page, grow(pen, 3))),
            detail(seg(5.5, 6.5, 13.5, 6.5)), detail(seg(5.5, 10, 13.5, 10)),
            detail("M5.5 16C6.5 14 7.5 17.5 8.5 15.5C9.2 14.3 9.8 16.5 10.8 16"),
            shell(pen)]


@icon("color-coded-notes", CAT, "Notebook page split into three sections, each marked with its own tab",
      tags=["colour coded notes", "organised notes", "highlighting", "sections", "study skills", "index tabs"])
def _(S):
    parts = [shell(rect(2.5, 2.5, 14.5, 19, rr(S, 2.5)))]
    for i, y in enumerate((6, 12, 18)):
        parts.append(detail(seg(5.5, y, 14, y)))
        tab = rect(17, y - 2, 4.5, 4, L(S, 0, 1.5))
        parts.append(shell(tab) if i == 1 else mark(soft(S, rect(17, y - 2, 4.5, 4))))
    return parts
