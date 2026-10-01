"""TypeIcon Core: learning (batch learning_003): subject books, maths manipulatives, reading corner
and classroom furniture, scripts and language learning, geometry, grading, and study programmes.

Subject books share one closed book (spine on the left); what sits on the cover names the subject.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path.parser import parse_path
from geometry import SCALE, D, I, P, ST, U, fmt, path_to_d, rotation

CAT = "learning"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def tf(d, m):
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def rot(d, deg, cx=12.0, cy=12.0):
    """Rotate a d-string clockwise on screen about (cx, cy)."""
    return tf(d, rotation(deg, cx, cy))


def mv(d, dx, dy):
    return tf(d, (1, 0, 0, 1, dx, dy))


def flip(d):
    return tf(d, (-1, 0, 0, 1, 24, 0))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def clip(d, box):
    return path_to_d(I(P(d), P(box)))


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def lens(x0, y0, x1, y1, bulge):
    """Pointed leaf between two points; bulge is the half-width at the middle (quadratic sides)."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln
    k = bulge * 2
    return (f"M{fmt(x0)} {fmt(y0)}Q{fmt(mx + nx * k)} {fmt(my + ny * k)} {fmt(x1)} {fmt(y1)}"
            f"Q{fmt(mx - nx * k)} {fmt(my - ny * k)} {fmt(x0)} {fmt(y0)}Z")


def ring(cx, cy, r, n, S):
    """Round-ish closed shape: a true circle in Rounded, a sharp n-gon in Line."""
    if S.name == "rounded":
        return circle(cx, cy, r)
    return poly(regular(cx, cy, r, n), closed=True)


def book(S, x=3.5, y=2.5, w=17, h=19, spine=3.5):
    """Closed book seen from the front: cover with a spine band on the left."""
    return [shell(rect(x, y, w, h, rr(S, 2.5))), detail(seg(x + spine, y, x + spine, y + h))]


def plus_d(cx, cy, h):
    return seg(cx - h, cy, cx + h, cy) + seg(cx, cy - h, cx, cy + h)


def times_d(cx, cy, h):
    return seg(cx - h, cy - h, cx + h, cy + h) + seg(cx - h, cy + h, cx + h, cy - h)


# ============================================================================ subject books

@icon("history-book", CAT, "Closed book with an hourglass on its cover",
      tags=["history", "textbook", "past", "hourglass", "timeline", "school subject", "heritage"])
def _(S):
    return [*book(S),
            detail(poly([(10.5, 7), (17.5, 7), (10.5, 17), (17.5, 17)], closed=True, r=S.r * 0.3))]


@icon("science-book", CAT, "Closed book with an atom on its cover",
      tags=["science", "textbook", "atom", "physics", "chemistry", "school subject", "lab"])
def _(S):
    return [*book(S),
            detail(rot(ellipse(14, 12, 6.3, 2.7), -55, 14, 12)),
            detail(rot(ellipse(14, 12, 6.3, 2.7), 55, 14, 12)),
            mark(circle(14, 12, 1.3))]


@icon("math-book", CAT, "Closed book with plus, minus, times and divide signs on its cover",
      tags=["maths", "mathematics", "textbook", "arithmetic", "numbers", "school subject", "algebra"])
def _(S):
    return [*book(S, spine=3),
            detail(plus_d(10.8, 8, 1.8)), detail(seg(14.5, 8, 18, 8)),
            detail(times_d(10.8, 15.5, 1.6)),
            detail(seg(14.5, 15.5, 18, 15.5)), dot(16.25, 13.3, 0.8), dot(16.25, 17.7, 0.8)]


@icon("medical-textbook", CAT, "Thick closed book with a medical cross on its cover",
      tags=["medicine", "anatomy", "textbook", "nursing", "doctor", "health", "school subject"])
def _(S):
    cross = union(rect(12.25, 6, 3.5, 9.5), rect(9.5, 8.75, 9, 4))
    return [*book(S), mark(cross), detail(seg(7, 18, 20.5, 18))]


@icon("fairy-tale-book", CAT, "Closed book with a small castle with pointed towers on its cover",
      tags=["fairytale", "storybook", "castle", "fantasy", "children's book", "story", "once upon a time"])
def _(S):
    castle = union(rect(9.5, 12, 3, 6), rect(15, 12, 3, 6), rect(11.5, 14, 4.5, 4),
                   poly([(9, 12), (11, 7), (13, 12)], closed=True), poly([(14.5, 12), (16.5, 7), (18.5, 12)], closed=True))
    return [*book(S), mark(castle)]


@icon("art-book", CAT, "Closed book with a paint palette on its cover",
      tags=["art", "painting", "palette", "artbook", "drawing", "design", "school subject"])
def _(S):
    pal = minus(ellipse(14, 12, 5.2, 4.6), circle(11.5, 10.6, 0.9), circle(14.3, 9.2, 0.9), circle(16.8, 10.8, 0.9),
                circle(15, 14.6, 1.2))
    return [*book(S), mark(pal)]


@icon("literature", CAT, "Open book with a feather quill standing in the fold",
      tags=["novel", "poetry", "writing", "author", "quill", "books", "english literature"])
def _(S):
    pages = poly([(12, 14), (21.5, 12), (21.5, 20.5), (12, 22), (2.5, 20.5), (2.5, 12)], closed=True, r=S.r * 0.5)
    return [shell(pages), detail(seg(12, 14, 12, 22)),
            shell(lens(12.5, 11.5, 19.5, 2.5, 2.4)), line(seg(12, 14, 15.2, 7.6))]


@icon("philosophy", CAT, "Seated figure resting its chin on one hand in a thinking pose",
      tags=["thinker", "thinking", "wisdom", "ethics", "logic", "contemplation", "reflect"])
def _(S):
    return [shell(circle(8, 6, 2.7)),
            line(poly([(12, 9.5), (16.5, 16)], r=S.r)),
            line(poly([(16.5, 16), (9.5, 16), (9.5, 21.5), (6.5, 21.5)], r=S.r)),
            line(seg(8.3, 10, 10, 15.5)),
            shell(rect(13, 19, 8.5, 2.5, 0.5 if S.name == "rounded" else 0))]


@icon("psychology", CAT, "Greek letter psi inside a head outline in profile",
      tags=["mind", "mental health", "psi", "therapy", "cognitive", "behaviour", "brain"])
def _(S):
    head = ("M8 21V17.5C5.3 15.8 3.5 13 3.5 9.5C3.5 5.5 7.2 2.5 11.5 2.5C16.3 2.5 19.5 5.6 19.5 9L21.5 12.5L19.5 13.5V16.5"
            "C19.5 17.5 18.5 18 17.5 18H14V21Z")
    return [shell(head), detail("M8.5 6.5V8.8A3.5 3.5 0 0 0 15.5 8.8V6.5"), detail(seg(12, 5.5, 12, 15))]


@icon("physical-education", CAT, "Coach whistle on a cord next to a ball",
      tags=["pe", "gym class", "sports", "whistle", "coach", "ball", "games lesson"])
def _(S):
    return [shell(circle(14.5, 9.5, 3.5)), shell(rect(17.5, 7.5, 4.5, 3, rr(S, 1.2))), dot(14.5, 9.5, 1.1),
            line(poly([(12, 7), (8.5, 3.5), (3, 3.5)], r=S.r)),
            shell(ring(9, 16, 5.5, 10, S)), mark(poly(regular(9, 16, 2.2, 5), closed=True)),
            *[detail(seg(*pt_on(9, 16, 2.2, a), *pt_on(9, 16, 5.5, a))) for a in (-90, -18, 54, 126, 198)]]


# ============================================================================ group work and maths

@icon("group-project", CAT, "Poster board with three hands reaching up to place notes on it",
      tags=["teamwork", "collaboration", "poster", "sticky notes", "group work", "brainstorm", "class project"])
def _(S):
    parts = [shell(rect(3, 2.5, 18, 10, rr(S, 2))),
             mark(rect(5.5, 6, 3.5, 3.5)), mark(rect(10.25, 6, 3.5, 3.5)), mark(rect(15, 6, 3.5, 3.5))]
    for x0, x1 in ((4.5, 7), (12, 12), (19.5, 17)):
        parts.append(line(seg(x0, 22, x1, 18.5)))
        parts.append(dot(x1, 17, 1.9))
    return parts


@icon("circle-time", CAT, "Top view of a ring of small heads sitting around a round mat",
      tags=["story time", "carpet time", "kindergarten", "preschool", "sitting in a circle", "group", "early years"])
def _(S):
    parts = [shell(ring(12, 12, 3.3, 8, S))]
    for i in range(6):
        x, y = pt_on(12, 12, 8.6, -90 + i * 60)
        parts.append(shell(circle(x, y, 2.2)))
    return parts


@icon("algebra", CAT, "Letter x with a small 2 above it, a plus sign and letter y",
      tags=["equation", "variable", "x squared", "maths", "unknown", "formula", "polynomial"])
def _(S):
    return [line(seg(2.5, 11, 8.5, 19)), line(seg(8.5, 11, 2.5, 19)),
            line(poly([(9.8, 5.5), (11, 3.8), (13, 3.8), (14.2, 5.5), (9.8, 9), (14.2, 9)], r=S.r * 0.3)),
            line(plus_d(13.3, 15, 2.5)),
            line(seg(17, 11, 19.5, 16.5)), line(seg(22, 11, 17.2, 22))]


@icon("geometry-shapes", CAT, "Triangle, square and circle with a centre dot, the basic shapes of geometry",
      tags=["shapes", "geometry", "triangle", "circle", "square", "maths", "polygon"])
def _(S):
    return [shell(poly([(12, 2.5), (17.5, 10.5), (6.5, 10.5)], closed=True, r=S.r)),
            shell(rect(3, 13.5, 8, 8, rr(S, 2))),
            shell(ring(17, 17.5, 4.3, 10, S)), dot(17, 17.5, 1)]


@icon("trigonometry", CAT, "Right triangle with a marked angle arc under a sine wave",
      tags=["trig", "sine", "cosine", "angle", "triangle", "maths", "hypotenuse", "waves"])
def _(S):
    wave = "M3 6.5C5 1.5 7 1.5 9 6.5C11 11.5 13 11.5 15 6.5C17 1.5 19 1.5 21 6.5"
    return [line(wave),
            shell(poly([(3.5, 12.5), (3.5, 21.5), (17.5, 21.5)], closed=True, r=S.r * 0.4)),
            detail(arc(17.5, 21.5, 6.5, 180, 210))]


def erode(d, k):
    """Region d shrunk by k px (for Filled designs with clean gaps between pieces)."""
    return D(P(d), ST(d, 2 * k, "butt", "miter"))


def star_pts(cx, cy, ro, ri, n=5):
    return [pt_on(cx, cy, ro if i % 2 == 0 else ri, -90 + i * 180 / n) for i in range(2 * n)]


@icon("fraction-circles", CAT, "Circle cut into quarters with one quarter pulled out of the pie",
      tags=["fractions", "pie", "quarter", "manipulative", "maths", "parts of a whole", "wedge"])
def _(S):
    main = "M9.5 14.5V7.5A7 7 0 1 0 16.5 14.5Z"
    wedge = "M13.5 10.5V3.5A7 7 0 0 1 20.5 10.5Z"
    return [shell(main), detail(seg(9.5, 14.5, 2.5, 14.5)), detail(seg(9.5, 14.5, 9.5, 21.5)), shell(wedge)]


@icon("linking-cubes", CAT, "Row of four snapped-together cubes with small nubs on top",
      tags=["snap cubes", "counting cubes", "manipulative", "maths", "blocks", "early maths", "building"])
def _(S):
    parts = [shell(rect(2.5, 10.5, 19, 9, rr(S, 2))),
             detail(seg(7.25, 10.5, 7.25, 19.5)), detail(seg(12, 10.5, 12, 19.5)), detail(seg(16.75, 10.5, 16.75, 19.5))]
    for cx in (4.9, 9.6, 14.4, 19.1):
        parts.append(mark(rect(cx - 1.4, 7, 2.8, 3.5, L(S, 0, 0.8))))
    return parts


@icon("geometric-solids", CAT, "Cube, cone and sphere grouped together",
      tags=["3d shapes", "solids", "sphere", "cone", "cube", "geometry", "maths manipulative"])
def _(S):
    cube = regular(6.5, 17.5, 4.8, 6)
    return [shell(poly(cube, closed=True, r=S.r * 0.3)),
            detail(seg(6.5, 17.5, *cube[1])), detail(seg(6.5, 17.5, *cube[3])), detail(seg(6.5, 17.5, *cube[5])),
            shell(f"M12 2L7.5 10A4.5 1.8 0 0 0 16.5 10Z"),
            shell(circle(17.5, 17.5, 4.5)), detail("M13 17.5A4.5 1.6 0 0 0 22 17.5")]


@icon("times-table", CAT, "Grid with a times sign in the corner cell and marked headers along the top and left",
      tags=["multiplication", "multiplication table", "maths", "grid", "tables", "times", "homework"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 2.5))),
             detail(seg(10.5, 3, 10.5, 21)), detail(seg(15.75, 3, 15.75, 21)),
             detail(seg(3, 10.5, 21, 10.5)), detail(seg(3, 15.75, 21, 15.75)),
             line(times_d(6.75, 6.75, 1.5))]
    for c in (13.1, 18.4):
        parts.append(dot(c, 6.75, 1.2))
        parts.append(dot(6.75, c, 1.2))
    return parts


@icon("pythagorean-theorem", CAT, "Right triangle with a square drawn on each of its three sides",
      tags=["pythagoras", "hypotenuse", "right triangle", "geometry", "a squared plus b squared", "maths proof", "squares"],
      filled=lambda: U(*[erode(d, 1.0) for d in _pyth_shapes()]))
def _(S):
    return [shell(poly(pts, closed=True, r=S.r * 0.4)) for pts in _pyth_polys()]


def _pyth_polys():
    x0, y0, w = 8.75, 15.0, 6.25  # right angle at (x0, y0); both legs have length w
    A, B, C = (x0, y0 - w), (x0 + w, y0), (x0, y0)
    return [[C, A, B],
            [(x0 - w, y0 - w), (x0, y0 - w), (x0, y0), (x0 - w, y0)],
            [(x0, y0), (x0 + w, y0), (x0 + w, y0 + w), (x0, y0 + w)],
            [A, B, (B[0] + w, B[1] - w), (A[0] + w, A[1] - w)]]


def _pyth_shapes():
    return [poly(p, closed=True) for p in _pyth_polys()]


@icon("napier-bones", CAT, "Two number rods whose cells are each split by a diagonal line",
      tags=["napier's rods", "multiplication", "calculating rods", "abacus", "maths history", "numbers", "counting aid"])
def _(S):
    parts = []
    for x0 in (3, 13.5):
        parts += [shell(rect(x0, 2.5, 7.5, 19, rr(S, 2))), detail(seg(x0, 12, x0 + 7.5, 12))]
        for y0, y1 in ((2.5, 12), (12, 21.5)):
            parts.append(detail(seg(x0 + 7.5, y0 + 0.5, x0, y1 - 0.5)))
    return parts


def bear_face(cx, base, r):
    """Teddy head with two round ears; the silhouette is the union of the three circles."""
    cy = base - r
    e = r * 0.52
    return union(circle(cx, cy, r), circle(cx - r * 0.78, cy - r * 0.74, e), circle(cx + r * 0.78, cy - r * 0.74, e))


@icon("counting-bears", CAT, "Three teddy bear heads in a row, each smaller than the last",
      tags=["counters", "teddy bears", "manipulatives", "sorting", "early maths", "sizes", "preschool"])
def _(S):
    return [shell(bear_face(7.2, 17, 3.8)), dot(7.2, 15.2, 0.8),
            shell(bear_face(14.3, 17, 2.7)), dot(14.3, 15.8, 0.6),
            shell(bear_face(19.2, 17, 1.9))]


@icon("venn-diagram", CAT, "Two overlapping circles with the overlap shaded",
      tags=["sets", "intersection", "overlap", "compare contrast", "logic", "maths", "diagram"])
def _(S):
    a, b = ring(8.5, 12, 6.5, 12, S), ring(15.5, 12, 6.5, 12, S)
    return [shell(a), shell(b), mark(clip(a, b))]


@icon("number-pyramid", CAT, "Stacked bricks in a pyramid with a number mark in each brick",
      tags=["addition pyramid", "number bonds", "maths puzzle", "bricks", "sums", "arithmetic", "steps"])
def _(S):
    outline = [(3, 21.5), (3, 15.5), (6, 15.5), (6, 9.5), (9, 9.5), (9, 3.5), (15, 3.5), (15, 9.5), (18, 9.5),
               (18, 15.5), (21, 15.5), (21, 21.5)]
    parts = [shell(poly(outline, closed=True, r=S.r * 0.5)),
             detail(seg(9, 9.5, 15, 9.5)), detail(seg(6, 15.5, 18, 15.5)),
             detail(seg(12, 9.5, 12, 15.5)), detail(seg(9, 15.5, 9, 21.5)), detail(seg(15, 15.5, 15, 21.5))]
    for x, y in ((12, 6.5), (9, 12.5), (15, 12.5), (6, 18.5), (12, 18.5), (18, 18.5)):
        parts.append(dot(x, y, 1))
    return parts


@icon("clock-worksheet", CAT, "Sheet with a clock face to read and an answer line under it",
      tags=["telling time", "clocks", "time worksheet", "homework", "analog clock", "maths", "primary school"])
def _(S):
    return [shell(rect(3.5, 2.5, 17, 19, rr(S, 2.5))),
            detail(circle(12, 10, 3.8)), detail(poly([(12, 7.3), (12, 10), (14.1, 10)])),
            detail(seg(7, 18, 17, 18))]


@icon("fact-family-triangle", CAT, "Triangle with a number circle at each corner and a plus sign in the middle",
      tags=["fact family", "number bond", "addition subtraction", "maths", "triangle", "related facts", "arithmetic"])
def _(S):
    pts = [(12, 5.5), (20, 19), (4, 19)]
    parts = []
    for i in range(3):
        a, b = pts[i], pts[(i + 1) % 3]
        ln = math.hypot(b[0] - a[0], b[1] - a[1])
        ux, uy = (b[0] - a[0]) / ln, (b[1] - a[1]) / ln
        parts.append(line(seg(a[0] + ux * 3.2, a[1] + uy * 3.2, b[0] - ux * 3.2, b[1] - uy * 3.2)))
    for x, y in pts:
        parts.append(shell(ring(x, y, 3, 8, S)))
        parts.append(dot(x, y, 0.9))
    parts.append(line(plus_d(12, 14, 1.8)))
    return parts


@icon("number-rods", CAT, "Staircase of rods of increasing length laid side by side",
      tags=["colour rods", "rods", "manipulatives", "maths", "counting", "bars", "early maths"])
def _(S):
    return [shell(rect(3, y, w, 3.3, L(S, 0, 1.6))) for y, w in ((2.75, 5), (8, 9), (13.25, 13), (18.5, 17))]


@icon("teacher-desk", CAT, "Wide desk with a drawer stack on one side, an apple and a pile of papers on top",
      tags=["teacher", "classroom", "desk", "apple", "papers", "office", "school"])
def _(S):
    return [shell(rect(2.5, 11, 19, 3, L(S, 0, 1.4))),
            shell(rect(4, 14, 7, 7.5, L(S, 0, 1.6))), detail(seg(4, 17.75, 11, 17.75)), dot(7.5, 15.9, 0.6), dot(7.5, 19.6, 0.6),
            line(seg(19.5, 14, 19.5, 21.5)),
            shell(circle(7.5, 7, 2.8)), line(seg(7.5, 4.3, 9, 2.5)),
            shell(rect(13.5, 7, 6, 2.5, L(S, 0, 1))), shell(rect(14.5, 4, 4.5, 2.2, L(S, 0, 1)))]


@icon("reward-stamp", CAT, "Rubber stamp standing beside its round impression showing a smiling face",
      tags=["sticker", "praise", "teacher stamp", "good job", "smiley", "marking", "reward"])
def _(S):
    return [shell(rect(4.5, 2.5, 5, 8, rr(S, 2))), shell(rect(2.5, 10.5, 9, 4, L(S, 0, 1.5))),
            line(seg(2.5, 18.5, 11.5, 18.5)),
            shell(ring(17, 16.5, 4.8, 12, S)), dot(15.2, 15.2, 0.9), dot(18.8, 15.2, 0.9),
            detail("M14.8 17.8A2.6 2.6 0 0 0 19.2 17.8")]


@icon("student-of-the-month", CAT, "Framed small portrait with a star above the frame",
      tags=["award", "star student", "recognition", "portrait", "achievement", "school", "honor"])
def _(S):
    return [mark(poly(star_pts(12, 6.2, 4.2, 1.9), closed=True)),
            shell(rect(4.5, 11.5, 15, 10, rr(S, 3.5))),
            dot(12, 15.3, 1.5), detail("M8.5 20.5V19.5A3.5 2.6 0 0 1 15.5 19.5V20.5")]


# ============================================================================ reading corner and library

@icon("classroom-library", CAT, "Picture books turned face out on a low cabinet with a small reading rug in front",
      tags=["reading corner", "book nook", "picture books", "bookshelf", "classroom", "early reading", "rug"])
def _(S):
    lean = rot(rect(10.2, 3.5, 4.4, 9, L(S, 0, 1)), 13, 12.4, 12.5)
    return [shell(rect(4, 5, 4.4, 7.5, L(S, 0, 1))), mark(rect(5.2, 6.8, 2, 2)),
            shell(lean), mark(rot(rect(11.4, 5.3, 2, 2), 13, 12.4, 12.5)),
            shell(rect(16, 5, 4.4, 7.5, L(S, 0, 1))), mark(rect(17.2, 6.8, 2, 2)),
            shell(rect(2.5, 12.5, 19, 6, rr(S, 2))), detail(seg(12, 12.5, 12, 18.5)),
            line(seg(4.5, 21.5, 19.5, 21.5))]


@icon("book-bin", CAT, "Plastic tub with a label on the front holding a row of upright books",
      tags=["book box", "book tub", "classroom library", "storage", "reading", "leveled books", "crate"])
def _(S):
    parts = []
    for x, top in ((4, 4), (9.7, 2.5), (15.4, 4.5)):
        parts.append(shell(rect(x, top, 4.6, 10 - top, L(S, 0, 1))))
        parts.append(detail(seg(x, top + 2.6, x + 4.6, top + 2.6)))
    parts += [shell(rect(2.5, 10, 19, 3, L(S, 0, 1.4))),
              shell(poly([(4, 13), (20, 13), (18.5, 21.5), (5.5, 21.5)], closed=True, r=S.r * 0.5)),
              detail(rect(9, 15.2, 6, 3, L(S, 0, 1)))]
    return parts


def phones(cx, S):
    """Headphones seen from the front: band over two ear cups."""
    return [line(f"M{fmt(cx - 3)} 9.5V8.5A3 3 0 0 1 {fmt(cx + 3)} 8.5V9.5"),
            mark(rect(cx - 4.6, 8.5, 3.2, 5.5, L(S, 0, 1.4))), mark(rect(cx + 1.4, 8.5, 3.2, 5.5, L(S, 0, 1.4)))]


@icon("listening-center", CAT, "Small audio player in the middle with several headphones plugged in around it",
      tags=["audio station", "listening station", "headphones", "audiobook", "reading center", "classroom", "music player"])
def _(S):
    return [shell(rect(7.5, 17.5, 9, 4.5, L(S, 0.5, 1.8))), dot(10.5, 19.75, 0.9), detail(seg(13, 19.75, 14.5, 19.75)),
            *phones(6.5, S), *phones(17.5, S),
            line(seg(9.5, 14, 9.5, 17.5)), line(seg(14.5, 14, 14.5, 17.5))]


def gear(cx, cy, ro, ri, n, S):
    pts = []
    for i in range(n):
        a = -90 + i * 360 / n
        w = 360 / n * 0.22
        pts += [pt_on(cx, cy, ri, a - w * 1.6), pt_on(cx, cy, ro, a - w), pt_on(cx, cy, ro, a + w), pt_on(cx, cy, ri, a + w * 1.6)]
    return poly(pts, closed=True, r=S.r * 0.25)


@icon("makerspace", CAT, "Workbench with a gear and a small robot arm standing on it",
      tags=["maker lab", "stem", "fab lab", "robotics", "tinkering", "workshop", "engineering class"])
def _(S):
    return [shell(rect(2.5, 15, 19, 3, L(S, 0, 1.4))),
            line(seg(5, 18, 5, 21.5)), line(seg(19, 18, 19, 21.5)),
            shell(gear(8, 9.5, 5, 3.6, 6, S)), dot(8, 9.5, 1.3),
            shell(rect(15, 12.5, 5, 2.5, L(S, 0, 1))),
            line(poly([(17.5, 12.5), (17.5, 7), (13.5, 4.5)], r=S.r * 0.5)),
            line(poly([(11.8, 3.6), (13.5, 4.5), (13, 6.5)]))]


@icon("library-self-checkout", CAT, "Kiosk with a screen on a stand and a book resting on a scanner pad",
      tags=["self service", "borrow books", "check out", "library kiosk", "scanner", "loan desk", "librarian"])
def _(S):
    return [shell(rect(2.5, 2.5, 11.5, 9.5, rr(S, 2))), detail(poly([(5.2, 7.2), (7.2, 9.2), (11.4, 5)])),
            line(seg(8.25, 12, 8.25, 19.5)), line(seg(4.5, 20.5, 12, 20.5)),
            shell(rect(14.5, 16, 7, 4.5, L(S, 0, 1.5))),
            mark(rect(14.8, 11.6, 6.4, 3.2))]


@icon("book-cradle", CAT, "Two angled foam wedges supporting an old book opened partway",
      tags=["book support", "conservation", "rare books", "archive", "special collections", "foam wedge", "reading rest"])
def _(S):
    bk = [(2.5, 4), (12, 7), (21.5, 4), (21.5, 10.5), (12, 16.2), (2.5, 10.5)]
    return [shell(poly(bk, closed=True, r=S.r * 0.4)), detail(seg(12, 7, 12, 16.2)),
            shell(poly([(2.5, 13.7), (11, 18.8), (11, 21.5), (2.5, 21.5)], closed=True, r=S.r * 0.4)),
            shell(poly([(21.5, 13.7), (13, 18.8), (13, 21.5), (21.5, 21.5)], closed=True, r=S.r * 0.4))]


@icon("archival-gloves", CAT, "White cotton glove reaching the corner of a book page",
      tags=["cotton gloves", "archive", "rare books", "conservation", "handling", "special collections", "museum"])
def _(S):
    palm = rect(3.5, 10, 9, 6.5, L(S, 0, 1.2))
    fingers = union(rect(3.5, 6, 2.25, 6, 1.1), rect(5.75, 4, 2.25, 8, 1.1),
                    rect(8, 4.5, 2.25, 7.5, 1.1), rect(10.25, 7, 2.25, 5, 1.1))
    thumb = path_to_d(ST(seg(12, 14.5, 16, 10.5), 2.6, "round", "round"))
    glove = union(palm, fingers, thumb)
    page = minus(rect(15, 3.5, 6.5, 18, L(S, 0, 1.2)), path_to_d(ST(glove, 4.5, "round", "round")))
    return [shell(page), shell(glove), shell(rect(3.5, 17.2, 9, 3.6, L(S, 0, 1.2))),
            detail(seg(5.75, 7.5, 5.75, 10.5)), detail(seg(8, 7.5, 8, 10.5)), detail(seg(10.25, 8.5, 10.25, 10.5))]


@icon("canadian-syllabics", CAT, "Three triangle syllabic characters pointing up, right and down, with a small dot",
      tags=["cree", "inuktitut", "indigenous writing", "abugida", "writing system", "script", "canada language"])
def _(S):
    return [shell(poly([(6.5, 3), (10.5, 10), (2.5, 10)], closed=True, r=S.r * 0.6)),
            shell(poly([(14.5, 3), (14.5, 11), (21.5, 7)], closed=True, r=S.r * 0.6)),
            shell(poly([(7, 14), (15, 14), (11, 21.5)], closed=True, r=S.r * 0.6)),
            dot(19, 17.5, 1.6)]


@icon("mongolian-script", CAT, "Vertical line of traditional Mongolian script with a central stem and hooks branching off it",
      tags=["traditional mongolian", "vertical writing", "uyghur script", "mongolia", "writing system", "calligraphy", "alphabet"])
def _(S):
    return [line(seg(12, 2.5, 12, 18.5)),
            line("M12 6.5C9.5 6.5 8 7.5 7.5 10"), line("M12 10.5C14.5 10.5 16 11.5 16.5 14"),
            line("M12 14.5C9.5 14.5 8.5 15.5 8 18"),
            line("M12 18.5C12 21 14.5 21.5 17 20")]


@icon("tifinagh-script", CAT, "Tifinagh letter yaz: a vertical stem with one curved arm opening up and one opening down",
      tags=["amazigh", "berber", "yaz", "north africa", "writing system", "alphabet", "tuareg"])
def _(S):
    return [line(seg(12, 3.5, 12, 20.5)),
            line("M7.5 3.5V6A4.5 4.5 0 0 0 16.5 6V3.5"),
            line("M7.5 20.5V18A4.5 4.5 0 0 1 16.5 18V20.5")]


@icon("shorthand-writing", CAT, "Steno pad with a few quick curved and hooked shorthand strokes",
      tags=["stenography", "steno pad", "speedwriting", "gregg", "note taking", "secretary", "dictation"])
def _(S):
    return [shell(rect(4, 2.5, 16, 19, rr(S, 2.5))), detail(seg(4, 6.5, 20, 6.5)),
            detail("M7.5 12C9 9 11.5 9 12.5 11.5C13.3 13 15 12.5 16.5 10"),
            detail("M7.5 18C9 15.5 11 15 12 17C13 19 15 18.5 16.5 16")]


def arrow_head(tip, deg, size=2.4):
    """Open chevron arrowhead whose tip points along direction deg (0 = right, 90 = down)."""
    a = math.radians(deg)
    back = (tip[0] - size * math.cos(a), tip[1] - size * math.sin(a))
    nx, ny = -math.sin(a), math.cos(a)
    return [(back[0] + nx * size * 0.8, back[1] + ny * size * 0.8), tip, (back[0] - nx * size * 0.8, back[1] - ny * size * 0.8)]


def arrow_tip(tip, deg, size=3.4, half=1.9, r=0.0):
    """Solid triangular arrowhead with its point at tip, pointing along deg."""
    a = math.radians(deg)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    bx, by = tip[0] - dx * size, tip[1] - dy * size
    return poly([tip, (bx + nx * half, by + ny * half), (bx - nx * half, by - ny * half)], closed=True, r=r)


@icon("stroke-order", CAT, "Chinese character ren with a start dot and arrowhead on each of its two strokes",
      tags=["chinese characters", "hanzi", "kanji", "handwriting", "calligraphy", "writing order", "how to write"])
def _(S):
    return [line(seg(11, 4, 5.8, 19.2)), dot(11, 4, 1.8), solid(arrow_tip((5, 21.5), 109, r=S.r * 0.5)),
            line(seg(10.5, 9.5, 18.5, 17.8)), dot(10.5, 9.5, 1.8), solid(arrow_tip((20.5, 20), 45, r=S.r * 0.5))]


@icon("character-practice-grid", CAT, "Square box with dotted centre guide lines and a written character inside",
      tags=["handwriting practice", "calligraphy grid", "mi zi ge", "tian zi ge", "chinese writing", "kanji practice", "copybook"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 2.5)))]
    for t in (6, 18):
        parts.append(dot(t, 12, 0.75))
        parts.append(dot(12, t, 0.75))
    parts += [detail(seg(12, 6, 7.5, 18)), detail(seg(11, 10.5, 17.5, 18))]
    return parts


@icon("language-proficiency", CAT, "Speech bubble holding four bars that rise in height",
      tags=["language level", "fluency", "cefr", "speaking skill", "a1 to c2", "language learning", "skill level"])
def _(S):
    bubble = poly([(2.5, 3), (21.5, 3), (21.5, 17), (10, 17), (5.5, 21.5), (6, 17), (2.5, 17)], closed=True, r=S.r * 1.2)
    return [shell(bubble)] + [detail(seg(x, 14, x, 14 - h)) for x, h in ((7, 2), (11, 4), (15, 6), (19, 8.5))]


@icon("conjugation-table", CAT, "Small two-column table with a verb stem at the top and ending lines below",
      tags=["verb forms", "grammar table", "verb endings", "tenses", "language class", "paradigm", "inflection"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 2.5))), detail(seg(3, 8.5, 21, 8.5)), detail(seg(3, 14.75, 21, 14.75)),
             detail(seg(12, 8.5, 12, 21)), mark(rect(8, 4.9, 8, 1.7))]
    for cx in (7.5, 16.5):
        for cy in (11.6, 17.9):
            parts.append(mark(rect(cx - 2, cy - 0.8, 4, 1.6)))
    return parts


# ============================================================================ early reading and number sense

@icon("sight-word-card", CAT, "Flash card with a short written word and a small eye in the corner",
      tags=["flash card", "high frequency words", "early reading", "literacy", "look and say", "phonics", "word recognition"])
def _(S):
    eye = "M14.5 7.5C15.8 5.6 18.2 5.6 19.5 7.5C18.2 9.4 15.8 9.4 14.5 7.5Z"
    return [shell(rect(2.5, 3.5, 19, 17, rr(S, 2.5))),
            detail(circle(7, 14.5, 2.2)), detail(seg(9.2, 12, 9.2, 17)),
            detail(seg(13, 12, 13, 17)), detail(seg(11.5, 13.2, 14.8, 13.2)),
            detail(eye), dot(17, 7.5, 0.75)]


@icon("bundled-sticks", CAT, "Bundle of ten sticks tied with a band next to three loose sticks",
      tags=["tens and ones", "place value", "counting sticks", "base ten", "lolly sticks", "maths manipulative", "bundle"])
def _(S):
    return [shell(rect(3.5, 3.5, 8.5, 17, L(S, 0.5, 2.5))), detail(seg(6.3, 3.5, 6.3, 20.5)), detail(seg(9.2, 3.5, 9.2, 20.5)),
            mark(rect(2, 10.5, 11.5, 3, L(S, 0, 1))),
            line(seg(16, 7, 16, 20)), line(seg(18.75, 9, 18.75, 21)), line(seg(21.5, 6, 21.5, 18))]


@icon("prime-sieve", CAT, "Number grid where most cells are crossed out and a few are circled",
      tags=["sieve of eratosthenes", "prime numbers", "factors", "number theory", "maths", "hundred chart", "composite"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 2.5))),
             detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)), detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15))]
    ring_ = lambda cx, cy: minus(circle(cx, cy, 2.1), circle(cx, cy, 0.8))
    for c, r_, prime in ((0, 0, 1), (1, 0, 1), (2, 0, 0), (0, 1, 1), (1, 1, 0), (2, 1, 1), (0, 2, 0), (1, 2, 0), (2, 2, 0)):
        cx, cy = 6 + 6 * c, 6 + 6 * r_
        parts.append(mark(ring_(cx, cy)) if prime else detail(times_d(cx, cy, 1.3)))
    return parts


def sector(cx, cy, r, a0, a1):
    """Solid pie slice from angle a0 to a1 (clockwise on screen)."""
    p0, p1 = pt_on(cx, cy, r, a0), pt_on(cx, cy, r, a1)
    big = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{fmt(cx)} {fmt(cy)}L{fmt(p0[0])} {fmt(p0[1])}A{fmt(r)} {fmt(r)} 0 {big} 1 {fmt(p1[0])} {fmt(p1[1])}Z"


@icon("transversal-angles", CAT, "Two parallel lines cut by a steep slanted line with matching angle arcs at both crossings",
      tags=["parallel lines", "corresponding angles", "geometry", "transversal", "maths", "angles", "alternate angles"])
def _(S):
    top, bot = 8, 17
    x = lambda y: 15.5 - (y - 2.5) / 19 * 7
    up = math.degrees(math.atan2(-19, 7))  # direction of the slanted line going up
    return [line(seg(2.5, top, 21.5, top)), line(seg(2.5, bot, 21.5, bot)), line(seg(15.5, 2.5, 8.5, 21.5)),
            mark(sector(x(top), top, 5.2, 180, up + 360)), mark(sector(x(bot), bot, 5.2, 180, up + 360))]


@icon("solid-cross-section", CAT, "Cylinder sliced by a tilted flat plane showing an oval cut face",
      tags=["cross section", "slice", "cylinder", "3d geometry", "plane", "solid shapes", "maths"])
def _(S):
    body = "M5.5 11V19A6.5 2.6 0 0 0 18.5 19V7Z" if S.name == "rounded" else "M5.5 11V19L8 21.5H16L18.5 19V7Z"
    cut = rot(ellipse(12, 9, 6.8, 2.8), -17, 12, 9)
    return [shell(union(body, cut)), detail(cut)]


def _cube_geometry():
    hx = regular(12, 12, 9.5, 6)
    t, ur, lr, b, ll, ul = hx
    c = (12, 12)
    return hx, [(t, ur, c, ul), (ur, lr, b, c), (ul, c, b, ll)]


def _cube_filled():
    hx, faces = _cube_geometry()
    mid = lambda p, q: ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    pieces = []
    for a, b, c, d in faces:
        m_ab, m_bc, m_cd, m_da = mid(a, b), mid(b, c), mid(c, d), mid(d, a)
        ctr = mid(m_ab, m_cd)
        for quad in ((a, m_ab, ctr, m_da), (m_ab, b, m_bc, ctr), (ctr, m_bc, c, m_cd), (m_da, ctr, m_cd, d)):
            pieces.append(erode(poly(list(quad), closed=True), 1.0))
    return U(*pieces)


@icon("unit-cubes-volume", CAT, "Large cube made of small unit cubes, two per edge, seen corner-on",
      tags=["volume", "cubic units", "building blocks", "3d", "maths manipulative", "cube stack", "measurement"],
      filled=_cube_filled)
def _(S):
    hx, faces = _cube_geometry()
    mid = lambda p, q: ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    t, ur, lr, b, ll, ul = hx
    c = (12, 12)
    parts = [shell(poly(hx, closed=True, r=S.r * 0.4)),
             detail(seg(*c, *t)), detail(seg(*c, *lr)), detail(seg(*c, *ll))]
    for a, bb, cc, d in faces:
        parts.append(detail(seg(*mid(a, bb), *mid(d, cc))))
        parts.append(detail(seg(*mid(bb, cc), *mid(a, d))))
    return parts


@icon("area-grid", CAT, "Irregular shape drawn on a square grid with the covered cells shaded",
      tags=["area", "square units", "counting squares", "grid paper", "measurement", "maths", "shaded cells"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 2.5))),
             detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)), detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15))]
    for c, r_ in ((0, 0), (0, 1), (1, 1), (1, 2)):
        parts.append(mark(rect(4.2 + 6 * c, 4.2 + 6 * r_, 3.6, 3.6)))
    return parts


@icon("perimeter", CAT, "Rectangle with arrows running around its outer edges",
      tags=["distance around", "boundary", "measurement", "shape", "geometry", "maths", "loop"])
def _(S):
    parts = [shell(rect(7.5, 7.5, 9, 9, rr(S, 2)))]
    for a, b, deg in (((3.5, 3.5), (17.5, 3.5), 0), ((20.5, 3.5), (20.5, 17.5), 90),
                      ((20.5, 20.5), (6.5, 20.5), 180), ((3.5, 20.5), (3.5, 6.5), 270)):
        parts.append(line(seg(*a, *b)))
        parts.append(line(poly(arrow_head(b, deg, 2.3))))
    return parts


# ============================================================================ courses, goals and modes of learning

def cap_mark(cx, cy, w=8, h=4):
    """Small solid mortarboard (flat diamond top over a short skull band)."""
    top = poly([(cx - w / 2, cy), (cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2)], closed=True)
    band = poly([(cx - w * 0.3, cy + h * 0.45), (cx - w * 0.3, cy + h * 1.1), (cx, cy + h * 1.45), (cx + w * 0.3, cy + h * 1.1),
                 (cx + w * 0.3, cy + h * 0.45), (cx, cy + h * 0.75)], closed=True)
    return union(top, band)


@icon("mobile-learning", CAT, "Smartphone showing a mortarboard above a small play button",
      tags=["m-learning", "learning app", "online course", "phone", "education app", "e-learning", "study on the go"])
def _(S):
    return [shell(rect(5.5, 2.5, 13, 19, rr(S, 3))),
            mark(cap_mark(12, 7.5, 8, 4)),
            mark(poly([(10.3, 14), (10.3, 18.5), (14.3, 16.25)], closed=True))]


@icon("educational-game", CAT, "Game controller with a small mortarboard resting on top",
      tags=["learning game", "gamification", "game based learning", "edutainment", "controller", "serious game", "play and learn"])
def _(S):
    pad = ("M6.5 10H17.5C20 10 22 12.5 22 15.5C22 18.5 20.8 20 19 20C17.5 20 16.8 19 15.8 18H8.2C7.2 19 6.5 20 5 20"
           "C3.2 20 2 18.5 2 15.5C2 12.5 4 10 6.5 10Z")
    return [shell(pad), detail(seg(7.5, 13.2, 7.5, 16.8)), detail(seg(5.7, 15, 9.3, 15)),
            dot(16, 14.2, 0.9), dot(18.3, 16, 0.9),
            mark(poly([(6.5, 4.8), (12, 2), (17.5, 4.8), (12, 7.6)], closed=True)),
            line(seg(17, 5.2, 17, 8))]


@icon("course-catalog", CAT, "Grid of four cards each showing a small book and a title line",
      tags=["course list", "curriculum", "course browser", "class listing", "e-learning", "catalogue", "subjects"])
def _(S):
    parts = []
    for x in (2.5, 13.5):
        for y in (2.5, 13.5):
            parts.append(shell(rect(x, y, 8, 8, L(S, 0.5, 2))))
            parts.append(mark(rect(x + 2, y + 1.9, 4, 2.4)))
            parts.append(mark(rect(x + 2, y + 5.2, 4, 0.9)))
    return parts


@icon("learning-goal", CAT, "Target with a small open book at the bullseye and an arrow hitting it",
      tags=["objective", "learning target", "aim", "outcome", "success criteria", "bullseye", "study goal"])
def _(S):
    book = poly([(9, 11), (11, 12), (13, 11), (13, 14.5), (11, 15.5), (9, 14.5)], closed=True)
    return [shell(ring(11, 13, 8.5, 14, S)), detail(ring(11, 13, 4.8, 10, S)),
            mark(minus(poly([(8.3, 10.2), (11, 11.4), (13.7, 10.2), (13.7, 15.4), (11, 16.6), (8.3, 15.4)], closed=True), rect(10.7, 10, 0.6, 8))),
            line(poly([(21.5, 2.5), (18, 6)])), line(seg(21.5, 2.5, 21.5, 5.5)), line(seg(21.5, 2.5, 18.5, 2.5)),
            detail(seg(18, 6, 13.8, 10.2))]


@icon("flipped-classroom", CAT, "House and schoolhouse side by side with a pair of swap arrows between them",
      tags=["homework swap", "home learning", "blended", "teaching model", "school and home", "lecture at home", "reverse"])
def _(S):
    return [shell(poly([(2.5, 21), (2.5, 13.5), (5.5, 10), (8.5, 13.5), (8.5, 21)], closed=True, r=S.r * 0.5)),
            shell(poly([(15.5, 21), (15.5, 13.5), (18.5, 10), (21.5, 13.5), (21.5, 21)], closed=True, r=S.r * 0.5)),
            line(seg(18.5, 10, 18.5, 4.5)), mark(poly([(18.5, 4.5), (21.5, 5.8), (18.5, 7.2)], closed=True)),
            line(seg(10.5, 13.5, 13.5, 13.5)), line(poly(arrow_head((14.5, 13.5), 0, 1.8))),
            line(seg(10.5, 18.5, 13.5, 18.5)), line(poly(arrow_head((9.5, 18.5), 180, 1.8)))]


@icon("blended-learning", CAT, "Laptop and an open book overlapping each other",
      tags=["hybrid learning", "online and in person", "digital and print", "laptop", "textbook", "mixed mode", "e-learning"])
def _(S):
    bk = [(12, 12), (16.75, 13.5), (21.5, 12), (21.5, 20.5), (16.75, 22), (12, 20.5)]
    bk_d = poly(bk, closed=True)
    halo = path_to_d(ST(bk_d, 4.0, "round", "round"))
    cutter = union(bk_d, halo)
    screen = minus(rect(2.5, 3, 13, 9.5, L(S, 1, 2)), cutter)
    base = minus(rect(1.5, 15.3, 14, 2.5, L(S, 0.5, 1.2)), cutter)
    return [shell(screen), shell(base), shell(poly(bk, closed=True, r=S.r * 0.4)), detail(seg(16.75, 13.5, 16.75, 22))]


@icon("test-booklet", CAT, "Stapled test booklet with answer bubbles on its cover and a pencil lying across it",
      tags=["exam booklet", "blue book", "standardized test", "answer sheet", "bubble sheet", "assessment", "pencil"])
def _(S):
    pencil_up = union(rect(10.5, 4, 3, 9.5, L(S, 0, 0.6)), poly([(10.5, 13.5), (13.5, 13.5), (12, 18)], closed=True))
    pencil = mv(rot(pencil_up, 45, 12, 11), 4.5, 3.5)
    cover = minus(rect(3.5, 2.5, 13.5, 19, rr(S, 2.5)), path_to_d(ST(pencil, 4.0, "round", "round")))
    ring_ = lambda cx, cy: minus(circle(cx, cy, 1.9), circle(cx, cy, 0.7))
    return [shell(cover), shell(pencil),
            mark(rect(5.3, 5.3, 2.2, 1)), mark(rect(5.3, 16.7, 2.2, 1)),
            mark(ring_(10.5, 7.8)), mark(ring_(10.5, 12.8)), mark(circle(10.5, 17.8, 1.6)) if False else mark(ring_(10.5, 17.8))]


def grade_a(x, y):
    return [line(poly([(x, y + 6.5), (x + 3.4, y), (x + 6.8, y + 6.5)])), line(seg(x + 1.6, y + 4.4, x + 5.2, y + 4.4))]


@icon("grading-scale", CAT, "Vertical bar split into five bands with the letters A at the top and F at the bottom",
      tags=["letter grades", "a to f", "marks", "report card", "score bands", "grade boundaries", "assessment"])
def _(S):
    parts = [shell(rect(3.5, 2.5, 6.5, 19, rr(S, 2))),
             detail(seg(3.5, 6.3, 10, 6.3)), detail(seg(3.5, 10.1, 10, 10.1)), detail(seg(3.5, 13.9, 10, 13.9)),
             detail(seg(3.5, 17.7, 10, 17.7))]
    parts += grade_a(13.7, 2.7)
    parts += [line(poly([(14.2, 21.5), (14.2, 15), (20.7, 15)])), line(seg(14.2, 18.2, 19.2, 18.2))]
    return parts


def _bell_y(x):
    """Height of the bell curve at x (for the two cubic pieces used below)."""
    pieces = [((2.5, 17.5), (7.5, 17.5), (8, 3.5), (12, 3.5)), ((12, 3.5), (16, 3.5), (16.5, 17.5), (21.5, 17.5))]
    for p0, p1, p2, p3 in pieces:
        if p0[0] <= x <= p3[0]:
            lo, hi = 0.0, 1.0
            for _ in range(40):
                t = (lo + hi) / 2
                u = 1 - t
                bx = u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0]
                if bx < x:
                    lo = t
                else:
                    hi = t
            t = (lo + hi) / 2
            u = 1 - t
            return u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1]
    return 17.5


@icon("grading-curve", CAT, "Bell curve whose area is split into four bands with a mark under each band",
      tags=["bell curve", "grade distribution", "normal distribution", "curving grades", "marks spread", "letter grades", "statistics"])
def _(S):
    bell = "M2.5 17.5C7.5 17.5 8 3.5 12 3.5C16 3.5 16.5 17.5 21.5 17.5Z"
    parts = [shell(bell)]
    for x in (7.5, 12, 16.5):
        parts.append(detail(seg(x, 17.5, x, _bell_y(x) + 0.5)))
    for cx in (5, 9.75, 14.25, 19):
        parts.append(dot(cx, 20.6, 1))
    return parts


@icon("math-worksheet", CAT, "Sheet with a stacked sum, a rule line and an empty answer box",
      tags=["sums", "addition", "arithmetic practice", "maths homework", "worksheet", "primary maths", "practice page"])
def _(S):
    return [shell(rect(3.5, 2.5, 17, 19, rr(S, 2.5))),
            mark(rect(11, 5.6, 6, 1.8)), mark(rect(11, 9.2, 6, 1.8)),
            mark(rect(5.9, 9.5, 3.6, 1.2)), mark(rect(7.1, 8.3, 1.2, 3.6)),
            detail(seg(6.5, 13.3, 17.5, 13.3)), detail(rect(11, 15.4, 6, 3, 0))]


@icon("late-night-study", CAT, "Desk lamp shining on an open book with a crescent moon above",
      tags=["studying at night", "cramming", "exam season", "night owl", "homework", "reading lamp", "all nighter"])
def _(S):
    bk = [(11, 14.5), (16.25, 16), (21.5, 14.5), (21.5, 20.5), (16.25, 22), (11, 20.5)]
    moon = minus(circle(17.5, 6.5, 4), circle(19.7, 5, 3.4))
    return [shell(moon),
            shell(poly([(4, 3.5), (8, 3.5), (10.5, 9), (1.5, 9)], closed=True, r=S.r * 0.4)),
            line(seg(6, 9, 6, 21.5)), line(seg(2.5, 21.5, 9.5, 21.5)),
            shell(poly(bk, closed=True, r=S.r * 0.4)), detail(seg(16.25, 16, 16.25, 22))]


@icon("open-mind", CAT, "Head in profile with the top of the skull lifted off and a lightbulb rising out of it",
      tags=["open minded", "new ideas", "growth mindset", "creativity", "brainstorm", "thinking", "idea"])
def _(S):
    head = ("M3.6 8C3.3 12 5.3 15.8 8 17.5V21H14V18H17.5C18.5 18 19.5 17.5 19.5 16.5V13.5L21.5 12.5L19.5 9.5L19.4 8Z")
    return [shell(head), shell(circle(11.5, 3.9, 2.3)),
            line("M2.6 5.6C2.6 3.3 4 2 6 1.8"), line("M17.3 1.6C19.4 2 20.6 3.4 20.6 5.2")]


def toy_block(S, x, y, w, h, kind):
    parts = [shell(rect(x, y, w, h, L(S, 0, 1)))]
    cx, cy = x + w / 2, y + h / 2
    if kind == "A":
        parts.append(mark(poly([(cx - 1.3, cy + 1.3), (cx, cy - 1.4), (cx + 1.3, cy + 1.3)], closed=True)))
    elif kind == "B":
        parts += [mark(circle(cx, cy - 1, 0.75)), mark(circle(cx, cy + 1, 0.75))]
    else:
        parts.append(mark(minus(circle(cx, cy, 1.4), circle(cx + 0.9, cy, 0.9))))
    return parts


@icon("alphabet-train", CAT, "Small toy train whose car carries stacked letter blocks",
      tags=["abc train", "toy train", "alphabet blocks", "letters", "preschool", "early literacy", "learning to read"])
def _(S):
    parts = [shell(rect(2.5, 11.5, 7, 6.5, L(S, 0.5, 2))), mark(rect(4, 8, 2.5, 3.4)),
             line(seg(10.5, 17.5, 21.5, 17.5)), line(seg(9, 17, 10.5, 17)),
             *toy_block(S, 10.5, 11, 5, 5, "A"), *toy_block(S, 16.5, 11, 5, 5, "B"), *toy_block(S, 13.5, 5.3, 5, 5, "C")]
    for cx in (4.7, 7.8, 13, 19):
        parts.append(dot(cx, 20.3, 1.4))
    return parts


@icon("story-sequence-cards", CAT, "Three cards in a row marked with one, two and three dots, each with a tiny picture",
      tags=["sequencing", "first next last", "storytelling", "retelling", "story order", "picture cards", "literacy"])
def _(S):
    parts = []
    for i, x in enumerate((2.5, 9.5, 16.5)):
        parts.append(shell(rect(x, 4, 5, 16, L(S, 0, 1.6))))
        for k in range(i + 1):
            parts.append(dot(x + 2.5, 7.7 + 2.2 * k, 0.75))
    parts += [mark(circle(5, 16, 1.4)), mark(poly([(9.5 + 1.2, 17.4), (9.5 + 2.5, 14.6), (9.5 + 3.8, 17.4)], closed=True)),
              mark(rect(17.9, 14.7, 2.2, 2.2))]
    return parts


@icon("syntax-tree", CAT, "Upside-down tree diagram with S at the top branching into two phrase nodes with triangles below",
      tags=["sentence diagram", "parse tree", "linguistics", "grammar", "noun phrase", "verb phrase", "syntax"])
def _(S):
    s_ = "M14 4C14 2.6 10 2.6 10 4.6C10 6.6 14 5.8 14 8C14 9.8 10 9.8 10 8.4"
    return [line(s_), line(seg(12, 10.5, 6.5, 13.5)), line(seg(12, 10.5, 17.5, 13.5)),
            dot(6.5, 14, 1.4), dot(17.5, 14, 1.4),
            shell(poly([(6.5, 15.5), (3, 21.5), (10, 21.5)], closed=True, r=S.r * 0.4)),
            shell(poly([(17.5, 15.5), (14, 21.5), (21, 21.5)], closed=True, r=S.r * 0.4))]


@icon("internship", CAT, "Briefcase with a small mortarboard on its front",
      tags=["work experience", "trainee", "placement", "student job", "career start", "graduate", "entry level"])
def _(S):
    return [shell(rect(2.5, 8, 19, 13, rr(S, 2.5))), line(f"M8.5 8V6C8.5 4.6 9.3 4 10.5 4H13.5C14.7 4 15.5 4.6 15.5 6V8"),
            mark(cap_mark(12, 13.2, 9, 4.4))]


@icon("apprenticeship", CAT, "Two figures of different size behind a workbench, with a hammer on the bench between them",
      tags=["mentor", "trade training", "on the job learning", "craft", "master and apprentice", "vocational", "guided practice"])
def _(S):
    return [shell(circle(8, 6.2, 2.7)), line("M3 16C3 11.5 4.8 9.6 8 9.6C11.2 9.6 13 11.5 13 16"),
            shell(circle(17.2, 9.5, 2.1)), line("M13.6 16C13.6 13.4 14.9 12 17.2 12C19.5 12 20.8 13.4 20.8 16"),
            shell(rect(2.5, 16, 19, 5.5, L(S, 1, 3))),
            mark(rect(9.3, 12, 5.4, 2.2, L(S, 0, 0.8))), mark(rect(11.4, 13.5, 1.2, 2.6))]


@icon("student-loan", CAT, "Mortarboard resting on top of a stack of coins",
      tags=["education debt", "tuition", "borrowing", "college cost", "financial aid", "graduate", "repayment"])
def _(S):
    return [shell(rect(6, 13, 12, 8.5, rr(S, 2))), detail(seg(6, 15.8, 18, 15.8)), detail(seg(6, 18.6, 18, 18.6)),
            shell(poly([(2.5, 7), (12, 3), (21.5, 7), (12, 11.5)], closed=True, r=S.r * 0.3)),
            line(seg(21, 7.2, 21, 11))]


@icon("college-fund", CAT, "Piggy bank wearing a mortarboard, with a coin dropping towards the slot on its back",
      tags=["college savings", "tuition savings", "education fund", "saving for school", "529", "piggy bank", "student savings"])
def _(S):
    body = union(ellipse(11, 15.5, 8, 5.3), ellipse(19.6, 16.3, 2, 2.4), rect(6, 18.5, 2.8, 3, L(S, 0, 1)),
                 rect(13.4, 18.5, 2.8, 3, L(S, 0, 1)))
    return [shell(body), detail(seg(8, 11.6, 12, 11.6)), dot(16.2, 14.6, 0.85),
            shell(circle(9.8, 5.3, 2.4)),
            mark(poly([(13.5, 8), (17, 5.8), (20.5, 8), (17, 10.2)], closed=True)),
            line(seg(20.2, 8.2, 20.2, 11))]


# ============================================================================ challenges and skills

@icon("craft-stick-bridge", CAT, "Small truss bridge made of crisscrossed sticks spanning two blocks",
      tags=["lolly stick bridge", "engineering challenge", "stem", "truss", "structures", "building project", "design and build"])
def _(S):
    return [shell(rect(2.5, 5.5, 19, 8.5, L(S, 0, 1.5))),
            detail(poly([(2.5, 14), (7.25, 5.5), (12, 14), (16.75, 5.5), (21.5, 14)])),
            shell(rect(2.5, 14.5, 5, 7, L(S, 0, 1.2))), shell(rect(16.5, 14.5, 5, 7, L(S, 0, 1.2)))]


@icon("marshmallow-challenge", CAT, "Tall tower of thin sticks joined at round nodes with a marshmallow on top",
      tags=["spaghetti tower", "team challenge", "stem", "design thinking", "building", "prototype", "tower"])
def _(S):
    nodes = [(5, 21), (12, 21), (19, 21), (8.5, 14), (15.5, 14), (12, 7.5)]
    edges = [(0, 1), (1, 2), (0, 3), (1, 3), (1, 4), (2, 4), (3, 4), (3, 5), (4, 5)]
    parts = [line(seg(*nodes[a], *nodes[b])) for a, b in edges]
    parts += [dot(x, y, 1.5) for x, y in nodes]
    parts.append(shell(ring(12, 3.6, 2.4, 8, S)))
    return parts


def turn_parts(parts, deg, cx=12.0, cy=12.0):
    return [Part(p.kind, rot(p.d, deg, cx, cy), p.attrs) for p in parts]


@icon("word-ladder", CAT, "Leaning ladder with a row of letter blocks above each rung, one block changing at each step",
      tags=["word puzzle", "change one letter", "spelling game", "vocabulary", "lewis carroll", "word chain", "phonics"])
def _(S):
    parts = [line(seg(4.5, 2, 4.5, 22)), line(seg(19.5, 2, 19.5, 22))]
    for k, yr in enumerate((9, 14.5, 20)):
        parts.append(line(seg(4.5, yr, 19.5, yr)))
        yc = yr - 3.2
        for j, xc in enumerate((8.6, 12, 15.4)):
            changed = j >= 3 - k
            parts.append(mark(circle(xc, yc, 1.25)) if changed else mark(rect(xc - 1.2, yc - 1.3, 2.4, 2.6)))
    return turn_parts(parts, 9)


@icon("brain-training", CAT, "Brain lifting a small dumbbell above its head",
      tags=["mental exercise", "cognitive training", "memory games", "mind fitness", "brain gym", "mental workout", "puzzle practice"])
def _(S):
    brain = ("M8.5 21C5.5 21 4 19 4 16.5C2.8 15.8 2.5 14.5 2.8 13.3C3 12 4 11 5.2 10.8C5.2 9 6.8 8 8.5 8.2C9.3 7.4 10.8 7.3 12 8"
             "C13.2 7.3 14.7 7.4 15.5 8.2C17.2 8 18.8 9 18.8 10.8C20 11 21 12 21.2 13.3C21.5 14.5 21.2 15.8 20 16.5C20 19 18.5 21 15.5 21Z")
    return [shell(brain), detail(seg(12, 8, 12, 20)),
            line(seg(8, 4.5, 16, 4.5)), line(seg(5.6, 9.6, 5.8, 7)), line(seg(18.4, 9.6, 18.2, 7)),
            mark(rect(4.2, 2, 3.2, 5, L(S, 0, 1))), mark(rect(16.6, 2, 3.2, 5, L(S, 0, 1)))]


@icon("speed-reading", CAT, "Open book with fast motion lines streaking in from the left",
      tags=["fast reading", "skimming", "reading speed", "scanning text", "quick read", "reading fluency", "words per minute"])
def _(S):
    bk = [(14.75, 7.5), (21.5, 6), (21.5, 18), (14.75, 19.5), (8, 18), (8, 6)]
    return [shell(poly(bk, closed=True, r=S.r * 0.4)), detail(seg(14.75, 7.5, 14.75, 19.5)),
            line(seg(2.5, 8.5, 5.5, 8.5)), line(seg(2.5, 12, 6, 12)), line(seg(2.5, 15.5, 5.5, 15.5))]


@icon("multiplication-wheel", CAT, "Circle with a times sign in the middle and a ring of dots for the multiples around it",
      tags=["times table wheel", "multiples", "multiplication practice", "skip counting", "maths", "number wheel", "times tables"])
def _(S):
    parts = [shell(ring(12, 12, 9.5, 16, S)), detail(times_d(12, 12, 2.1))]
    for i in range(8):
        x, y = pt_on(12, 12, 6.3, -90 + i * 45)
        parts.append(dot(x, y, 1.1))
    return parts


@icon("world-languages", CAT, "Globe with two small speech bubbles above it holding different letters",
      tags=["multilingual", "foreign languages", "translation", "international", "language exchange", "speak the world", "global communication"])
def _(S):
    def bubble(x, y, tail_x):
        return poly([(x, y), (x + 7, y), (x + 7, y + 5), (tail_x + 1.5, y + 5), (tail_x, y + 7.5), (tail_x - 0.5, y + 5), (x, y + 5)],
                    closed=True, r=S.r * 0.4)
    return [shell(circle(12, 16.3, 5.3)), detail(ellipse(12, 16.3, 2.4, 5.3)),
            shell(bubble(2.5, 2, 6)), shell(bubble(14.5, 2, 17)),
            mark(poly([(4.7, 5.4), (6, 3.4), (7.3, 5.4)], closed=True)), mark(minus(circle(18, 4.5, 1.4), circle(18, 4.5, 0.5)))]
