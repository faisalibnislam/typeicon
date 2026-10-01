"""TypeIcon Core: learning (batch learning_001): classroom gear, books and libraries, knowledge, research
and academic writing, language and handwriting.

Shared pieces: one portrait sheet of paper for documents, one upright closed book for book variants and
one open book for knowledge icons. Text lines are 2 px strokes; tiny marks are solid dots.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path.parser import parse_path
from geometry import SCALE, D, P, ST, U, fmt, path_to_d, rotation

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


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def thin(d, w=1.3):
    """Thin solid curve (a filled region, not a stroke): solid in Line/Rounded, knocked out of a Filled shell."""
    return mark(path_to_d(ST(d, w, "round", "round")))


def lens(x0, y0, x1, y1, bulge):
    """Pointed leaf between two points; bulge is the half-width at the middle."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln
    k = bulge * 2
    return (f"M{fmt(x0)} {fmt(y0)}Q{fmt(mx + nx * k)} {fmt(my + ny * k)} {fmt(x1)} {fmt(y1)}"
            f"Q{fmt(mx - nx * k)} {fmt(my - ny * k)} {fmt(x0)} {fmt(y0)}Z")


def speech(S, x, y, w, h, tx):
    """Speech bubble outline (closed poly) with a tail under x = tx."""
    pts = [(x, y), (x + w, y), (x + w, y + h), (tx + 2.5, y + h), (tx, y + h + 3), (tx - 0.5, y + h), (x, y + h)]
    return poly(pts, closed=True, r=S.r)


def cut_stroke(S, d, cuts, w=2.0):
    """Stroked outline of d with circular gaps (list of (cx, cy, r)) cut out; solid in every style."""
    region = ST(d, w, S.cap, S.join, 3.0)
    for cx, cy, r in cuts:
        region = D(region, P(circle(cx, cy, r)))
    return solid(path_to_d(region))


def arrow_head(cx, cy, r, deg, size=2.6, spread=38):
    """Two-stroke chevron for a clockwise arc arrow ending at angle deg on circle (cx, cy, r)."""
    ex, ey = pt_on(cx, cy, r, deg)
    tx, ty = -math.sin(math.radians(deg)), math.cos(math.radians(deg))
    out = []
    for sgn in (-1, 1):
        a = math.radians(180 + sgn * spread)
        bx = ex + size * (tx * math.cos(a) - ty * math.sin(a))
        by = ey + size * (tx * math.sin(a) + ty * math.cos(a))
        out.append((bx, by))
    return poly([out[0], (ex, ey), out[1]])


def ax(origin, deg):
    """Map local (u along the axis, v across it) to grid coordinates; deg is the screen angle of +u."""
    ox, oy = origin
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return lambda u, v: (ox + u * c - v * s, oy + u * s + v * c)


def star_pts(cx, cy, ro, ri, n=5, start=-90.0):
    out = []
    for i in range(2 * n):
        r = ro if i % 2 == 0 else ri
        out.append(pt_on(cx, cy, r, start + i * 180 / n))
    return out


def scallop(cx, cy, rv, rb, n):
    """Closed scalloped circle: n outward bumps of radius rb between vertices on radius rv."""
    v = [pt_on(cx, cy, rv, -90 + i * 360 / n) for i in range(n)]
    d = f"M{fmt(v[0][0])} {fmt(v[0][1])}"
    for i in range(1, n + 1):
        p = v[i % n]
        d += f"A{fmt(rb)} {fmt(rb)} 0 0 1 {fmt(p[0])} {fmt(p[1])}"
    return d + "Z"


def sheet(S, x=4.5, y=2.5, w=15, h=19):
    return shell(rect(x, y, w, h, rr(S, 2.5)))


def text_lines(ys, x0=8, x1=16):
    return [detail(seg(x0, y, x1, y)) for y in ys]


def book_closed(S, x=4.5, y=2.5, w=15, h=19, spine=3.5):
    return [shell(rect(x, y, w, h, rr(S, 3.5))), detail(seg(x + spine, y, x + spine, y + h))]


def open_book(S, top=6, left=2.5, right=21.5, t=4.5, b=18.5, dip=2):
    """Open book with two facing pages. top = centre crease top y, dip = how far the crease sits below the page tops."""
    cx = (left + right) / 2
    pts = [(cx, top), (cx - 4, t), (left, t), (left, b), (cx - 4, b), (cx, b + dip), (cx + 4, b), (right, b), (right, t), (cx + 4, t)]
    return [shell(poly(pts, closed=True, r=S.r)), detail(seg(cx, top, cx, b + dip))]


# =========================================================================== classroom gear

@icon("classroom", CAT, "Chalkboard on the front wall above rows of small student desks",
      tags=["classroom", "school", "lesson", "class", "desks", "teaching", "room"])
def _(S):
    parts = [shell(rect(3, 3, 18, 6, rr(S, 3)))]
    for y in (12, 16, 20):
        for x0 in (3, 9.75, 16.5):
            parts.append(mark(rect(x0, y, 4.5, 2, L(S, 0, 0.8))))
    return parts


@icon("chalk-stick", CAT, "Short stick of chalk lying diagonally with a worn tip and a few dust dots",
      tags=["chalk", "blackboard", "write", "teacher", "classroom", "draw"])
def _(S):
    m = ax((3.5, 19.5), -45)
    body = [m(0, -2.5), m(12, -2.5), m(14.5, -0.5), m(13.5, 2.5), m(0, 2.5)]
    return [shell(poly(body, closed=True, r=S.r * 0.5), stroke_miterlimit="3"),
            detail(seg(*m(9, -2.5), *m(9, 2.5))),
            dot(17, 18.5, 1.25), dot(20.5, 15.5, 1.25), dot(14.5, 21, 1.25)]


@icon("chalkboard-eraser", CAT, "Felt chalkboard duster with a wooden back and a puff of chalk dust below",
      tags=["eraser", "duster", "chalkboard", "blackboard", "felt", "clean", "classroom"])
def _(S):
    return [shell(rect(3, 3, 18, 9, rr(S, 4))), detail(seg(3, 7, 21, 7)),
            dot(7, 16.5, 1.5), dot(12, 18.5, 1.75), dot(17, 16.5, 1.5), dot(9.5, 21, 1.1), dot(15, 21.3, 1.1)]


@icon("chalk-holder", CAT, "Slim metal clutch tube with a stick of chalk poking out of one end",
      tags=["chalk holder", "chalk", "clutch", "teacher", "blackboard", "classroom", "tube"])
def _(S):
    m = ax((3.5, 20.5), -45)
    tube = [m(0, -2.5), m(10, -2.5), m(12.5, -1.75), m(12.5, 1.75), m(10, 2.5), m(0, 2.5)]
    return [shell(poly(tube, closed=True, r=S.r * 0.5)),
            detail(seg(*m(7, -2.5), *m(7, 2.5))),
            line(seg(*m(12.5, 0), *m(19.5, 0)))]


@icon("school-locker", CAT, "Two tall metal lockers side by side with vent slots, a dial and a handle",
      tags=["locker", "school", "storage", "hallway", "combination", "student", "lock"])
def _(S):
    return [shell(rect(2.5, 2.5, 8.5, 19, rr(S, 2.5))), shell(rect(13, 2.5, 8.5, 19, rr(S, 2.5))),
            detail(seg(5, 6.5, 8.5, 6.5)), detail(seg(5, 9.5, 8.5, 9.5)),
            detail(seg(15.5, 6.5, 19, 6.5)), detail(seg(15.5, 9.5, 19, 9.5)),
            dot(6.75, 15, 1.4), detail(seg(17.25, 13.5, 17.25, 18))]


@icon("writing-slate", CAT, "Framed slate board with a scribble on it and a pencil tied on by a string",
      tags=["slate", "writing slate", "chalk", "old school", "tablet", "handwriting", "school"])
def _(S):
    return [shell(rect(3, 3, 12, 14, rr(S, 2.5))),
            detail("M6 13Q7.5 7.5 9.5 10.5T12 8"),
            solid(poly([(18.5, 10.5), (21.5, 10.5), (21.5, 18), (20, 21.5), (18.5, 18)], closed=True, r=S.r * 0.4)),
            line("M15 6.5Q20 6.5 20 10")]


@icon("school-satchel", CAT, "Leather satchel with a front flap, two buckled straps and a top carry handle",
      tags=["satchel", "school bag", "messenger bag", "bag", "student", "leather", "education"])
def _(S):
    return [shell(rect(3.5, 7.5, 17, 13.5, rr(S, 3))),
            line(poly([(8.5, 7.5), (8.5, 5), (9.5, 3.5), (14.5, 3.5), (15.5, 5), (15.5, 7.5)], r=S.r * 0.6)),
            detail("M3.5 12.5C8 16 16 16 20.5 12.5"),
            detail(seg(8, 8, 8, 14)), detail(seg(16, 8, 16, 14)),
            mark(rect(6.75, 17, 2.5, 2.5, 0.5)), mark(rect(14.75, 17, 2.5, 2.5, 0.5))]


@icon("set-square", CAT, "Right-angled triangular ruler with a triangular cutout and tick marks along its legs",
      tags=["set square", "triangle ruler", "geometry", "drafting", "math", "angle", "protractor"])
def _(S):
    return [shell(poly([(3, 21), (3, 3), (21, 21)], closed=True, r=S.r * 0.8), stroke_miterlimit="3"),
            mark(poly([(7, 17), (7, 12), (12, 17)], closed=True, r=S.r * 0.3)),
            detail(seg(3, 8, 5.5, 8)), detail(seg(3, 12.5, 5.5, 12.5)),
            detail(seg(15, 21, 15, 18.5)), detail(seg(18.5, 21, 18.5, 18.5))]


@icon("scientific-calculator", CAT, "Tall calculator with a wide display and dense rows of small keys",
      tags=["scientific calculator", "calculator", "math", "trig", "function keys", "science", "exam"])
def _(S):
    parts = [shell(rect(5, 2.5, 14, 19, rr(S, 2.5))), detail(rect(7.5, 5.5, 9, 2.5, 0))]
    for y in (11.5, 14.5, 17.5):
        for x in (8, 10.7, 13.3, 16):
            parts.append(dot(x, y, 0.85))
    return parts


@icon("graphing-calculator", CAT, "Tall calculator with a large screen showing a curve above a grid of keys",
      tags=["graphing calculator", "calculator", "math", "plot", "function", "algebra", "exam"])
def _(S):
    parts = [shell(rect(4, 2.5, 16, 19, rr(S, 2.5))),
             detail(rect(6.5, 4.75, 11, 7.5, 0)), thin("M8.5 11C10.5 11 10.5 7 12 7.6C13.5 8.2 13.5 7.6 15.5 6.8")]
    for x in (8.5, 12, 15.5):
        parts.append(dot(x, 15.5, 0.85))
        parts.append(dot(x, 18.5, 0.85))
    return parts


@icon("report-card", CAT, "Report card with a heavy header bar and rows of grade marks beside subject lines",
      tags=["report card", "grades", "marks", "school report", "transcript", "student", "results"])
def _(S):
    parts = [sheet(S), mark(rect(7, 5.5, 10, 2.5, L(S, 0, 1)))]
    for y in (11.5, 15, 18.5):
        parts += [dot(8.2, y, 1.2), detail(seg(11.5, y, 16, y))]
    return parts


@icon("gold-star-sticker", CAT, "Five-point star inside a scalloped round sticker",
      tags=["gold star", "sticker", "reward", "praise", "good job", "kids", "teacher"])
def _(S):
    return [shell(scallop(12, 12, 7.6, 2.6, 10)),
            mark(poly(star_pts(12, 12.4, 5.3, 2.3), closed=True, r=S.r * 0.3))]


@icon("class-timetable", CAT, "Weekly timetable with a row of day dots over blocks of lessons",
      tags=["timetable", "schedule", "class schedule", "lessons", "periods", "week", "school"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 2.5))), detail(seg(3, 8, 21, 8))]
    for x in (5.5, 8.75, 12, 15.25, 18.5):
        parts.append(dot(x, 5.5, 0.8))
    for x0, y0 in ((5, 10.25), (13, 10.25), (5, 15.25)):
        parts.append(mark(rect(x0, y0, 6, 3.5, L(S, 0, 1))))
    return parts


@icon("school-crest", CAT, "Shield holding an open book with a laurel curve under it",
      tags=["crest", "school badge", "coat of arms", "emblem", "house", "shield", "academy"])
def _(S):
    shield = poly([(5, 3), (19, 3), (19, 9.5)], r=0) + "C19 12.6 15.8 14.6 12 15.8C8.2 14.6 5 12.6 5 9.5Z"
    return [shell(shield),
            mark("M8 7.3Q10.4 6.6 11.6 8V12.3Q10 11.3 8 11.8Z"), mark("M16 7.3Q13.6 6.6 12.4 8V12.3Q14 11.3 16 11.8Z"),
            line("M6 18.5C8.5 21.5 15.5 21.5 18 18.5")]


@icon("student-id-card", CAT, "Identity card with a portrait, a mortarboard mark and text lines",
      tags=["student card", "id card", "campus card", "badge", "identity", "university", "pass"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, rr(S, 2.5))),
            dot(8, 10.2, 1.9), detail("M4.8 16.3A3.2 3.2 0 0 1 11.2 16.3"),
            mark(poly([(13.5, 9), (16.5, 7.5), (19.5, 9), (16.5, 10.5)], closed=True)),
            detail(seg(14, 13.5, 19, 13.5)), detail(seg(14, 16.5, 17.5, 16.5))]


# =========================================================================== classroom life

@icon("kindergarten", CAT, "Small house with a round window, a door and a stack of toy blocks inside",
      tags=["kindergarten", "preschool", "nursery", "early years", "playschool", "toddler", "blocks"])
def _(S):
    house = poly([(3, 21), (3, 10), (12, 3), (21, 10), (21, 21)], closed=True, r=S.r * 0.8)
    return [shell(house), dot(12, 10.5, 2.1),
            mark(rect(5.5, 16.5, 3.5, 3.5)), mark(rect(10, 16.5, 3.5, 3.5)), mark(rect(7.75, 12.5, 3.5, 3.5)),
            detail("M16 21V16.5H18.75V21")]


@icon("teachers-apple", CAT, "Apple with a stem and leaf resting on a small stack of two books",
      tags=["teacher's apple", "apple", "teacher gift", "school", "books", "education", "teaching"])
def _(S):
    apple = mv("M12 7C10 5.3 5.5 6 5.5 10.3C5.5 13 7 15.5 9 15.5C10.2 15.5 11 15 12 15C13 15 13.8 15.5 15 15.5C17 15.5 18.5 13 18.5 10.3C18.5 6 14 5.3 12 7Z", 0, -1.5)
    return [shell(apple), line("M12 5.5C12 4 12.4 3.2 13.4 2.6"),
            mark(lens(13.4, 4.8, 17.4, 2.8, 1.0)),
            mark(rect(3.5, 16.5, 17, 2.5, L(S, 0, 1))), mark(rect(5.5, 20.25, 13, 1.75, L(S, 0, 0.8)))]


@icon("pocket-chart", CAT, "Wall chart with horizontal clear pockets each holding a word card",
      tags=["pocket chart", "word cards", "sentence strips", "classroom", "literacy", "teaching", "chart"])
def _(S):
    parts = [shell(rect(3, 2.5, 18, 19, rr(S, 2.5))), detail(seg(3, 9, 21, 9)), detail(seg(3, 15.25, 21, 15.25))]
    for y, x0, x1 in ((4.75, 6.5, 17.5), (11.1, 6.5, 14), (17.35, 6.5, 16)):
        parts.append(mark(rect(x0, y, x1 - x0, 2, L(S, 0, 1))))
    return parts


@icon("response-clicker", CAT, "Small handheld voting remote with a tiny screen and four answer keys",
      tags=["clicker", "student response", "voting remote", "quiz", "poll", "classroom", "audience response"])
def _(S):
    return [shell(rect(6.5, 2.5, 11, 19, rr(S, 4))), mark(rect(9, 5.5, 6, 2.75, L(S, 0, 1))),
            dot(9.75, 13, 1.3), dot(14.25, 13, 1.3), dot(9.75, 17.5, 1.3), dot(14.25, 17.5, 1.3)]


@icon("laptop-cart", CAT, "Wheeled charging cabinet holding laptops standing in vertical slots",
      tags=["laptop cart", "charging cart", "trolley", "classroom laptops", "chromebook", "storage", "school it"])
def _(S):
    parts = [shell(rect(3.5, 3, 17, 14, rr(S, 2.5)))]
    for x in (7, 11, 15):
        parts.append(mark(rect(x, 6, 2, 8, L(S, 0, 0.6))))
    parts += [line(seg(7, 17, 7, 19)), line(seg(17, 17, 17, 19)), dot(7, 20.3, 1.7), dot(17, 20.3, 1.7)]
    return parts


@icon("homework-folder", CAT, "Two-pocket folder with a small house symbol on the front pocket",
      tags=["homework", "folder", "school folder", "assignments", "pocket folder", "student", "take home"])
def _(S):
    body = poly([(4.5, 21), (4.5, 3), (10, 3), (12, 5.5), (19.5, 5.5), (19.5, 21)], closed=True, r=S.r * 0.8)
    house = poly([(8.5, 17.5), (8.5, 14), (12, 11.5), (15.5, 14), (15.5, 17.5)], closed=True)
    return [shell(body), detail(seg(4.5, 10, 19.5, 10)), mark(house)]


@icon("pencil-cap-eraser", CAT, "Pencil with a wedge-shaped eraser cap fitted over its end",
      tags=["pencil eraser", "eraser cap", "pencil top", "rubber", "stationery", "school supplies", "correct"])
def _(S):
    m = ax((3.5, 20.5), -45)
    body = [m(0, 0), m(3.5, -2.5), m(14.5, -2.5), m(18, 2.5), m(3.5, 2.5)]
    return [shell(poly(body, closed=True, r=S.r * 0.5), stroke_miterlimit="3"),
            detail(seg(*m(3.5, -2.5), *m(3.5, 2.5))), detail(seg(*m(10, -2.5), *m(10, 2.5)))]


@icon("chalkboard-compass", CAT, "Large drawing compass with a rubber foot on one leg and a chalk holder on the other",
      tags=["compass", "drawing compass", "geometry", "chalkboard", "circle", "teacher", "math"])
def _(S):
    m = ax((16.3, 13.6), math.degrees(math.atan2(10.4, 4.4)))
    holder = [m(0, -1.9), m(4.6, -1.9), m(4.6, 1.9), m(0, 1.9)]
    return [line(seg(12, 4.5, 6.3, 18.3)), line(seg(12, 4.5, 16.3, 13.6)),
            dot(12, 4, 1.8), dot(5.6, 19.9, 2.0),
            solid(poly(holder, closed=True, r=S.r * 0.3)), line(seg(*m(4.6, 0), *m(7, 0)))]


@icon("coding-robot", CAT, "Small wheeled robot beside a bent arrow of programmed moves",
      tags=["coding robot", "programmable robot", "stem", "kids coding", "bee-bot", "toy", "robotics"])
def _(S):
    return [shell(rect(3, 6, 9.5, 8, rr(S, 3))), line(seg(7.75, 6, 7.75, 3)), dot(7.75, 2.6, 1.2),
            dot(6.2, 9.7, 1.0), dot(9.6, 9.7, 1.0),
            dot(5.5, 17.6, 1.7), dot(10, 17.6, 1.7),
            line(poly([(15.5, 7), (19.5, 7), (19.5, 17)], r=S.r * 0.6)),
            line(poly([(17.5, 15), (19.5, 17.5), (21.5, 15)]))]


@icon("language-lab", CAT, "Headset with a boom microphone beside a speech bubble holding the letter A",
      tags=["language lab", "language learning", "pronunciation practice", "headset", "speaking", "listening", "esl"])
def _(S):
    return [shell(speech(S, 13, 2.5, 8, 7, 14.5)),
            thin("M15.1 8L17 4.3L18.9 8"), thin("M15.8 6.6H18.2"),
            line("M3.5 15V13.5A4.75 4.75 0 0 1 13 13.5V15"),
            solid(rect(2, 14, 3, 5, L(S, 0, 1.2))), solid(rect(11.5, 14, 3, 5, L(S, 0, 1.2))),
            line("M13 19Q13 21.5 9.5 21.5"), dot(8.3, 21.5, 1.2)]


@icon("dog-eared-page", CAT, "Page of text lines with its top corner folded down into a triangle",
      tags=["dog ear", "folded corner", "page marker", "bookmark", "reading", "page", "fold"])
def _(S):
    page = poly([(5, 3), (14.5, 3), (19, 7.5), (19, 21), (5, 21)], closed=True, r=S.r * 0.8)
    return [shell(page), mark(poly([(14.5, 4.5), (14.5, 7.5), (17.5, 7.5)], closed=True)),
            detail(seg(8, 11.5, 16, 11.5)), detail(seg(8, 15, 16, 15)), detail(seg(8, 18.25, 13, 18.25))]


def _shoulders(cx, cy, w=3.5):
    return f"M{fmt(cx - w)} {fmt(cy)}A{fmt(w)} {fmt(w)} 0 0 1 {fmt(cx + w)} {fmt(cy)}Z"


@icon("book-club", CAT, "Three small heads and shoulders gathered behind one open book",
      tags=["book club", "reading group", "discussion", "literature circle", "readers", "community", "library"])
def _(S):
    parts = []
    for cx, hy in ((5.5, 6.3), (12, 4.3), (18.5, 6.3)):
        parts += [dot(cx, hy, 1.8), mark(_shoulders(cx, hy + 6.5))]
    pts = [(12, 15.5), (8, 14), (2.5, 14), (2.5, 20.5), (8, 20.5), (12, 22), (16, 20.5), (21.5, 20.5), (21.5, 14), (16, 14)]
    parts += [shell(poly(pts, closed=True, r=S.r * 0.8)), detail(seg(12, 15.5, 12, 22))]
    return parts


@icon("book-series", CAT, "Three upright books side by side with one, two and three dots on their spines",
      tags=["book series", "trilogy", "volumes", "saga", "numbered books", "set", "collection"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 2.5))), detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21))]
    parts.append(dot(6, 9, 1.0))
    for y in (8, 11): parts.append(dot(12, y, 1.0))
    for y in (7, 10, 13): parts.append(dot(18, y, 1.0))
    return parts


@icon("chained-book", CAT, "Old thick book with a short chain running from its cover off to the edge",
      tags=["chained book", "chained library", "medieval", "rare book", "restricted", "antique", "manuscript"])
def _(S):
    return [shell(rect(2.5, 4, 10, 16, rr(S, 2))), detail(seg(6, 4, 6, 20)), detail(seg(8, 9, 10.5, 9)),
            line(circle(15.75, 12, 1.75)), line(circle(19.75, 12, 1.75))]


@icon("scroll-case", CAT, "Cylindrical tube with its cap beside it and a rolled document poking out of the top",
      tags=["scroll case", "document tube", "diploma tube", "map tube", "rolled paper", "scroll", "canister"])
def _(S):
    return [shell(rect(3.5, 10, 9, 11.5, rr(S, 2.5))), detail(seg(3.5, 13.5, 12.5, 13.5)),
            line(poly([(5.75, 10), (5.75, 4), (10.25, 4), (10.25, 10)], r=S.r * 0.6)),
            shell(rect(15.5, 15, 5.5, 6.5, rr(S, 2.5)))]


@icon("rosetta-stone", CAT, "Irregular stone slab split into three horizontal bands of different script marks",
      tags=["rosetta stone", "hieroglyphs", "ancient script", "decipher", "translation", "egypt", "artifact"])
def _(S):
    slab = poly([(4.5, 21), (5, 9), (8, 4.5), (11.5, 2.8), (16, 3.5), (19.5, 6.5), (19.5, 21)], closed=True, r=S.r * 0.8)
    parts = [shell(slab), detail(seg(5, 9.5, 19.5, 9.5)), detail(seg(4.5, 15, 19.5, 15))]
    for x in (9, 12.5, 16): parts.append(dot(x, 6.6, 0.9))
    for x in (8.5, 13.5): parts.append(mark(rect(x, 11.6, 3, 1.2)))
    for x in (8.5, 13.5): parts.append(mark(rect(x, 17.6, 3, 1.2)))
    return parts


@icon("oracle-bone", CAT, "Flat bone fragment with a jagged crack line and columns of carved characters",
      tags=["oracle bone", "ancient china", "divination", "carved script", "archaeology", "fragment", "shang"])
def _(S):
    frag = poly([(6, 4), (15.5, 2.8), (20.5, 8), (19, 16.5), (14, 21.5), (6.5, 19), (3.5, 11)], closed=True, r=S.r * 0.8)
    parts = [shell(frag), detail("M14 4.5L12 9.5L15.5 13.5L13 18.5")]
    for y in (7, 11.5, 16):
        parts.append(mark(rect(6.2, y - 1.5, 1.2, 3))); parts.append(mark(rect(5.4, y - 0.4, 2.8, 1.2)))
    parts.append(mark(rect(17.4, 8, 1.2, 3))); parts.append(mark(rect(16.6, 9.1, 2.8, 1.2)))
    return parts


@icon("book-barcode", CAT, "Closed book above a barcode with a short number line under it",
      tags=["book barcode", "isbn", "book scan", "library catalogue", "inventory", "bookstore", "price tag"])
def _(S):
    parts = [shell(rect(7, 2.5, 10, 10, rr(S, 4))), detail(seg(10.5, 2.5, 10.5, 12.5))]
    x = 3.25
    for w in (1, 1.5, 1, 1, 1.5, 1, 1.5, 1, 1):
        parts.append(mark(rect(x, 15, w, 4.5)))
        x += w + 1
    parts.append(mark(rect(3.25, 20.75, x - 1 - 3.25, 1.1)))
    return parts


@icon("book-swap", CAT, "Two closed books with a pair of opposing arrows between them",
      tags=["book swap", "book exchange", "book trade", "lending", "community library", "swap", "share books"])
def _(S):
    return [shell(rect(3, 4, 5, 16, L(S, 1, 2.5))), shell(rect(16, 4, 5, 16, L(S, 1, 2.5))),
            detail(seg(3, 8, 8, 8)), detail(seg(16, 8, 21, 8)),
            line(seg(10.5, 10, 13.5, 10)), line(poly([(12.5, 8), (14, 10), (12.5, 12)])),
            line(seg(10.5, 15, 13.5, 15)), line(poly([(11.5, 13), (10, 15), (11.5, 17)]))]


@icon("digital-library", CAT, "Monitor showing a search bar above a shelf of book spines",
      tags=["digital library", "online library", "ebooks", "e-library", "catalogue", "database", "reading app"])
def _(S):
    parts = [shell(rect(2.5, 3, 19, 14, rr(S, 2.5))), line(seg(12, 17, 12, 20)), line(seg(8, 20.5, 16, 20.5)),
             mark(rect(5.5, 5.5, 13, 2, L(S, 0, 1)))]
    for x, top in ((5.5, 10), (8.5, 9.5), (11.5, 10), (14.5, 9.5), (17.5, 10)):
        parts.append(mark(rect(x, top, 1.6, 14.5 - top)))
    return parts


@icon("reading-list", CAT, "Clipboard with three lines each led by a small book mark",
      tags=["reading list", "to read", "book list", "checklist", "syllabus", "wishlist", "library"])
def _(S):
    parts = [shell(rect(4.5, 4.5, 15, 17, rr(S, 2.5))), mark(rect(8.5, 2.5, 7, 3.5, L(S, 0, 1.2)))]
    for y in (10.5, 14.5, 18.5):
        parts += [mark(rect(7, y - 1.5, 3, 3, L(S, 0, 0.6))), detail(seg(12, y, 17, y))]
    return parts


@icon("book-review", CAT, "Open book with a speech bubble of text lines above it",
      tags=["book review", "book report", "critique", "reader feedback", "opinion", "rating", "literature"])
def _(S):
    pts = [(12, 15.5), (8, 14), (2.5, 14), (2.5, 20), (8, 20), (12, 21.5), (16, 20), (21.5, 20), (21.5, 14), (16, 14)]
    return [shell(speech(S, 4.5, 2.5, 15, 7.5, 10.5)),
            detail(seg(8, 5, 16, 5)), detail(seg(8, 8, 13.5, 8)),
            shell(poly(pts, closed=True, r=S.r * 0.8)), detail(seg(12, 15.5, 12, 21.5))]


def gear(cx, cy, r, n=6, hole=1.0, tooth=1.5, tw=1.7):
    """Solid gear silhouette (body disc plus n square teeth, minus a centre hole) as one d-string."""
    parts = [circle(cx, cy, r)]
    for i in range(n):
        parts.append(rot(rect(cx - tw / 2, cy - r - tooth + 0.3, tw, tooth), i * 360 / n, cx, cy))
    return minus(union(*parts), circle(cx, cy, hole))


HEAD_LINE = "M8 21V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.5 12.8L19 13.3V15.5C19 16.6 18.1 17.5 17 17.5H14V21Z"
HEAD_ROUND = ("M8 20V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.2 12Q20.6 12.9 19.7 13.1L19 13.3V15.5"
              "C19 16.6 18.1 17.5 17 17.5H14V20C14 20.6 13.6 21 13 21H9C8.4 21 8 20.6 8 20Z")


def head(S):
    return HEAD_LINE if S.name == "line" else HEAD_ROUND


@icon("sheet-magnifier", CAT, "Flat rectangular magnifying sheet lying over text lines, with its text drawn larger",
      tags=["sheet magnifier", "page magnifier", "reading aid", "fresnel lens", "large print", "low vision", "read"])
def _(S):
    return [line(seg(3, 4.5, 21, 4.5)), line(seg(3, 8, 15, 8)),
            shell(rect(3, 11.5, 18, 9.5, rr(S, 3))),
            mark(rect(5.5, 13.75, 13, 2.25)), mark(rect(5.5, 17.5, 8, 2))]


@icon("interlibrary-loan", CAT, "Two small library buildings with a book carried between them by an arrow",
      tags=["interlibrary loan", "library loan", "borrow", "lending", "library network", "book transfer", "ill"])
def _(S):
    def bld(x):
        return shell(poly([(x, 21), (x, 15), (x + 3.75, 12), (x + 7.5, 15), (x + 7.5, 21)], closed=True, r=S.r * 0.6))
    return [bld(3), bld(13.5), line("M6.75 9.5C7.5 3.5 16.5 3.5 17.25 9.5"),
            line(poly([(15.5, 7.5), (17.25, 9.75), (19.25, 8)])),
            mark(rect(10.25, 6.5, 3.5, 4.5))]


@icon("book-repair", CAT, "Closed book with a strip of tape across its split spine",
      tags=["book repair", "mend", "bookbinding", "conservation", "tape", "fix", "library care"])
def _(S):
    return [*book_closed(S), mark(rot(rect(3, 10.25, 11, 4.25), -14, 8.5, 12.4))]


@icon("abc-book", CAT, "Closed book with the letters A B C stacked on its cover",
      tags=["abc book", "alphabet book", "primer", "early reader", "letters", "kids", "learn to read"])
def _(S):
    parts = book_closed(S, spine=3.5)
    parts += [thin("M11.2 9L13 5L14.8 9"), thin("M11.9 7.6H14.1"),
              thin("M11.2 10.4H13.4C14.3 10.4 14.6 10.9 14.6 11.4C14.6 12 14.2 12.4 13.4 12.4H11.2M13.4 12.4C14.4 12.4 14.8 12.9 14.8 13.5C14.8 14.1 14.4 14.6 13.4 14.6H11.2M11.2 10.4V14.6"),
              thin("M14.8 16.6C14.4 16.2 13.8 16 13.3 16C12 16 11.2 16.9 11.2 18.1C11.2 19.3 12 20.2 13.3 20.2C13.8 20.2 14.4 20 14.8 19.6")]
    return parts


@icon("bilingual-dictionary", CAT, "Thick closed book with two different letters on the cover separated by a slash",
      tags=["bilingual dictionary", "translation dictionary", "two languages", "translate", "language", "vocabulary", "esl"])
def _(S):
    return [*book_closed(S, x=3.5, w=17, spine=3.5),
            thin("M10.2 10.5L12 6L13.8 10.5"), thin("M10.9 9.1H13.1"),
            thin("M12.2 16.5L15.2 11.5"),
            thin("M18 12.5H15.2L17 15.2L15.2 18.2H18")]


@icon("book-of-knowledge", CAT, "Open book with rays of light fanning out above its pages",
      tags=["book of knowledge", "wisdom", "enlightenment", "revelation", "learning", "insight", "scripture"])
def _(S):
    parts = open_book(S, top=13.5, t=12, b=19, dip=2)
    for deg in (-90, -54, -126, -18, -162):
        a = pt_on(12, 11, 3.6, deg)
        b = pt_on(12, 11, 6.8, deg)
        parts.append(line(seg(a[0], a[1], b[0], b[1])))
    return parts


@icon("lamp-of-knowledge", CAT, "Classic oil lamp with a curved spout and flame resting on a closed book",
      tags=["lamp of knowledge", "oil lamp", "enlightenment", "wisdom", "study", "light", "learning"])
def _(S):
    bowl = "M6 9.5H15.5C16 12 14.5 14.5 11.5 14.5H10C7.5 14.5 6 12.5 6 9.5Z"
    return [shell(bowl), line("M6 9.5C4.2 9 3.3 8 3 6.3"),
            mark("M3 1.8Q5.3 4 3 6.4Q0.7 4 3 1.8Z"),
            line("M15.5 10.5C19 10 20 12 18.5 13.6L15 13.4"),
            shell(rect(3, 16.5, 18, 5, rr(S, 2.5))), detail(seg(7, 16.5, 7, 21.5))]


@icon("book-tree", CAT, "Small round-topped tree growing out of the crease of an open book",
      tags=["book tree", "growth", "knowledge grows", "nature reading", "education", "ecology", "learning"])
def _(S):
    parts = open_book(S, top=15, t=13.5, b=19.5, dip=2)
    parts += [shell(circle(12, 6.5, 4.25)), line(seg(12, 10.75, 12, 15))]
    return parts


@icon("head-with-gears", CAT, "Head in profile with two meshing gears inside the skull",
      tags=["head with gears", "thinking", "mindset", "cognitive", "process", "intelligence", "mental model"])
def _(S):
    return [shell(head(S)), mark(gear(9.5, 9.2, 3.0, 6, 0.9, 1.2, 1.6)), mark(gear(14.2, 12.6, 2.1, 6, 0.7, 1.0, 1.4))]


@icon("head-with-book", CAT, "Head in profile with a small open book inside the skull",
      tags=["head with book", "knowledge", "learning", "study", "mind", "memory", "education"])
def _(S):
    return [shell(head(S)),
            mark("M6.2 8.3Q9 7 11.2 8.8V14.2Q9 12.8 6.2 14Z"), mark("M16.2 8.3Q13.4 7 11.2 8.8V14.2Q13.4 12.8 16.2 14Z")]


def _small_head(S, mirrored):
    d = head(S)
    m = (0.5, 0, 0, 0.5, 0, 1.5)
    if mirrored:
        m = (-0.5, 0, 0, 0.5, 24, 1.5)
    return tf(d, m)


@icon("knowledge-sharing", CAT, "Two heads in profile facing each other with an open book between them",
      tags=["knowledge sharing", "teaching", "mentoring", "conversation", "exchange of ideas", "peer learning", "discussion"])
def _(S):
    pts = [(12, 16), (8.5, 14.5), (3.5, 14.5), (3.5, 20.5), (8.5, 20.5), (12, 22), (15.5, 20.5), (20.5, 20.5), (20.5, 14.5), (15.5, 14.5)]
    return [shell(_small_head(S, False)), shell(_small_head(S, True)),
            shell(poly(pts, closed=True, r=S.r * 0.8)), detail(seg(12, 16, 12, 22))]


@icon("mind-map", CAT, "Central rounded box with branching lines out to five small bubbles",
      tags=["mind map", "brainstorm", "concept map", "ideas", "diagram", "planning", "topics"])
def _(S):
    parts = [shell(rect(7, 9, 10, 6, rr(S, 3)))]
    for (x0, y0), (x1, y1) in (((8.5, 9), (5.5, 6.3)), ((15.5, 9), (18.5, 6.3)), ((8.5, 15), (5.5, 17.7)),
                               ((15.5, 15), (18.5, 17.7)), ((12, 15), (12, 18.3))):
        parts.append(line(seg(x0, y0, x1, y1)))
    for x, y in ((4.5, 5), (19.5, 5), (4.5, 19), (19.5, 19), (12, 20.3)):
        parts.append(dot(x, y, 1.7))
    return parts


@icon("learning-curve", CAT, "S-shaped curve climbing across axes to a small mortarboard at its top end",
      tags=["learning curve", "progress", "skill growth", "improvement", "training", "mastery", "graph"])
def _(S):
    return [line(poly([(3.5, 3), (3.5, 20.5), (21, 20.5)])),
            line("M6.5 18C11 18 10 11 13.5 11C15.5 11 15.5 9.5 17 8.6"),
            mark(poly([(15, 5), (18.5, 3.2), (22, 5), (18.5, 6.8)], closed=True))]


def _bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


@icon("learning-path", CAT, "Winding dashed path with milestone dots leading to a flag at the end",
      tags=["learning path", "roadmap", "curriculum", "journey", "milestones", "course", "progress"])
def _(S):
    p0, p1, p2, p3 = (5, 19.5), (13, 20.5), (6, 11.5), (16.5, 10.5)
    parts = [dot(*p0, 1.7)]
    for a, b in ((0.22, 0.4), (0.52, 0.68), (0.78, 0.92)):
        pts = [_bez(p0, p1, p2, p3, a + (b - a) * k / 4) for k in range(5)]
        parts.append(line(poly(pts)))
    parts += [line(seg(19, 3, 19, 11)), solid(poly([(19, 3), (22, 4.8), (19, 6.6)], closed=True))]
    return parts


@icon("lifelong-learning", CAT, "Open book with an infinity loop hovering above it",
      tags=["lifelong learning", "continuous learning", "infinite", "education", "growth", "self study", "never stop"])
def _(S):
    inf = ("M12 7.5C10 5 7.5 4 5.8 4.8C3.8 5.8 3.8 9.2 5.8 10.2C7.5 11 10 10 12 7.5"
           "C14 5 16.5 4 18.2 4.8C20.2 5.8 20.2 9.2 18.2 10.2C16.5 11 14 10 12 7.5Z")
    return [line(inf), *open_book(S, top=15, t=13.5, b=19, dip=2)]


@icon("academic-seal", CAT, "Round seal with a notched rim and an open book under a flame at its centre",
      tags=["academic seal", "university seal", "emblem", "accreditation", "official stamp", "college", "certified"])
def _(S):
    return [shell(scallop(12, 12, 8.1, 1.9, 14)),
            mark("M12 5Q14.7 8 12 11Q9.3 8 12 5Z"),
            mark("M7 12.6Q9.6 11.6 11.5 13V18Q9.6 16.8 7 17.6Z"), mark("M17 12.6Q14.4 11.6 12.5 13V18Q14.4 16.8 17 17.6Z")]


@icon("quill-and-scroll", CAT, "Feather quill resting on a rolled scroll of parchment",
      tags=["quill and scroll", "calligraphy", "writing", "parchment", "manuscript", "literature", "author"])
def _(S):
    return [shell(rect(2.5, 14.5, 15.5, 6.5, rr(S, 3.25))), detail(seg(6.5, 14.5, 6.5, 21)), detail(seg(14, 14.5, 14, 21)),
            shell(lens(10, 12.5, 21, 3, 2.6)), detail(seg(11, 11.5, 18, 5.2)),
            line(seg(8.5, 14, 10.3, 12.2))]


@icon("writing-prompt", CAT, "Glowing light bulb above a blank page with a pencil at its side",
      tags=["writing prompt", "story idea", "creative writing", "inspiration", "blank page", "journal prompt", "brainstorm"])
def _(S):
    m = ax((15.5, 21), -45)
    pencil = [m(0, 0), m(2.4, -1.8), m(7.5, -1.8), m(7.5, 1.8), m(2.4, 1.8)]
    bulb = union(circle(9, 5, 3.4), poly([(7, 7), (11, 7), (10.4, 9.6), (7.6, 9.6)], closed=True), rect(7.6, 9.8, 2.8, 1))
    return [solid(bulb), line(seg(2.5, 5, 3.8, 5)), line(seg(14.2, 5, 15.5, 5)),
            shell(rect(3.5, 13, 11, 8.5, rr(S, 2.5))),
            solid(poly(pencil, closed=True, r=S.r * 0.3))]


@icon("academic-journal", CAT, "Thin bound journal with a volume box on the cover and a spine band",
      tags=["academic journal", "periodical", "scholarly journal", "research paper", "publication", "volume", "issue"])
def _(S):
    return [shell(rect(5, 2.5, 14, 19, rr(S, 3.5))), detail(seg(8.5, 2.5, 8.5, 21.5)),
            mark(rect(11, 5.5, 5.5, 3.5)), detail(seg(11, 13, 16.5, 13)), detail(seg(11, 16.5, 14.5, 16.5))]


def _quote_mark(cx, cy):
    return union(circle(cx, cy, 1.9), poly([(cx - 1.9, cy), (cx + 1.9, cy), (cx - 1.1, cy + 4.2)], closed=True))


@icon("citation", CAT, "Quotation marks above lines of text, the last line ending in a small superscript one",
      tags=["citation", "cite", "quote", "reference", "source", "referencing", "attribution"])
def _(S):
    return [mark(_quote_mark(4.8, 6.3)), mark(_quote_mark(10, 6.3)),
            detail(seg(14, 6, 21, 6)), detail(seg(3, 14, 21, 14)), detail(seg(3, 18.5, 14, 18.5)),
            thin("M16.6 14.2L17.8 13.3V18.3", 1.2)]


@icon("footnote", CAT, "Page with a text line ending in a superscript one and a matching short line under a rule at the bottom",
      tags=["footnote", "endnote", "annotation", "note reference", "academic writing", "superscript", "reference"])
def _(S):
    return [sheet(S), detail(seg(8, 7.5, 13, 7.5)), thin("M14.6 6.6L15.7 5.8V9.4", 1.2),
            detail(seg(8, 11, 16, 11)),
            mark(rect(8, 14.25, 5, 1)), thin("M8.4 17.2L9.3 16.6V19.6", 1.1), detail(seg(11.5, 18.3, 16, 18.3))]


@icon("bibliography", CAT, "Page of reference entries, each with a hanging indent on its second line",
      tags=["bibliography", "references", "works cited", "sources", "reading list", "academic", "citations"])
def _(S):
    return [sheet(S, x=3.5, w=17),
            detail(seg(6.5, 7, 17.5, 7)), detail(seg(9, 10.25, 17.5, 10.25)),
            detail(seg(6.5, 14, 17.5, 14)), detail(seg(9, 17.25, 14.5, 17.25))]


@icon("glossary", CAT, "Page with short bold terms, each followed by a longer definition line",
      tags=["glossary", "terms", "definitions", "vocabulary list", "word list", "lexicon", "key terms"])
def _(S):
    return [sheet(S, x=3.5, w=17),
            mark(rect(6.5, 5, 5, 2.2)), detail(seg(6.5, 10.25, 17.5, 10.25)),
            mark(rect(6.5, 13, 4, 2.2)), detail(seg(6.5, 18.25, 17.5, 18.25)),
            detail(seg(6.5, 18.25, 6.5, 18.25)) if False else detail(seg(6.5, 14.1, 6.5, 14.1)) if False else mark(rect(12.5, 13, 2.5, 2.2))]


@icon("questionnaire-form", CAT, "Sheet with questions, each over a row of answer dots",
      tags=["questionnaire", "survey", "quiz form", "multiple choice", "poll", "feedback form", "answers"])
def _(S):
    parts = [sheet(S)]
    for y, yd in ((6.25, 9.75), (13.25, 16.75)):
        parts += [dot(7.6, y, 1.0), detail(seg(10.5, y, 16, y))]
        for x in (8.5, 12, 15.5):
            parts.append(dot(x, yd, 1.15))
    return parts


@icon("cursive-writing", CAT, "Flowing looped cursive stroke running along a ruled baseline",
      tags=["cursive", "handwriting", "script", "penmanship", "calligraphy", "joined writing", "longhand"])
def _(S):
    return [line("M3 16C6 16 6.5 6 8.5 6C10.5 6 8.5 16 11.5 16C14 16 14 11 15.5 11C17 11 15 16 18 16C19.5 16 20.5 14.5 21 12.5"),
            mark(rect(2.5, 19.5, 19, 1)), mark(rect(2.5, 10.5, 19, 0.8))]


@icon("letter-tracing", CAT, "Dotted outline of a capital A with an arrow marking where the stroke starts",
      tags=["letter tracing", "handwriting practice", "alphabet", "preschool writing", "dotted letter", "trace", "kids"])
def _(S):
    parts = []

    def dots(p, q, n):
        for k in range(n + 1):
            t = k / n
            parts.append(dot(p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t, 1.0))
    dots((3.5, 21), (12, 7.5), 5)
    dots((12, 7.5), (20.5, 21), 5)
    dots((8.6, 16.2), (15.4, 16.2), 2)
    parts.append(line(poly([(9.2, 2.5), (12, 5), (14.8, 2.5)])))
    return parts


@icon("pronunciation", CAT, "Face profile with lips and curved sound waves coming out of the mouth",
      tags=["pronunciation", "speaking", "speech", "phonetics", "say it aloud", "accent", "language learning"])
def _(S):
    face = "M8.5 2.5V8Q8.5 9 7.5 10.5L5.8 12.8Q5.6 13.4 6.3 13.6L8.8 13.9Q9.6 14.6 9 15.2Q9.8 15.9 9 16.6Q9.7 17.4 9 18.2Q9.3 19.5 10 21"
    return [line(face), line(arc(12.5, 15.4, 4.5, -45, 45)), line(arc(12.5, 15.4, 8, -45, 45))]


@icon("sentence-diagram", CAT, "Horizontal base line with a vertical divider and slanted modifier lines hanging below",
      tags=["sentence diagram", "grammar", "parsing", "syntax", "reed kellogg", "english class", "sentence structure"])
def _(S):
    return [line(seg(2.5, 10.5, 21.5, 10.5)), line(seg(12, 6.5, 12, 14)),
            line(poly([(7.5, 10.5), (5, 18), (10, 18)], r=S.r * 0.3)),
            line(poly([(17.5, 10.5), (15, 18), (20, 18)], r=S.r * 0.3))]


@icon("spelling-bee", CAT, "Round striped bee beside a square letter tile marked with an A",
      tags=["spelling bee", "spelling contest", "word game", "bee", "letters", "competition", "vocabulary"])
def _(S):
    return [shell(ellipse(7.5, 14.5, 5.2, 3.8)), detail(seg(6, 10.8, 6, 18.2)), detail(seg(9.2, 10.8, 9.2, 18.2)),
            shell(ellipse(6, 7.5, 1.6, 2.6)), shell(ellipse(10.2, 7.3, 1.6, 2.6)),
            line(seg(12.7, 14.5, 14, 14.5)) if False else dot(2.4, 14.5, 0.7),
            shell(rect(14.5, 11, 7.5, 9.5, rr(S, 2.5))),
            thin("M16.6 18L18.25 13.4L19.9 18", 1.2), thin("M17.2 16.5H19.3", 1.2)]


@icon("latin-script", CAT, "Capital A and lowercase a side by side",
      tags=["latin script", "roman alphabet", "letter a", "uppercase lowercase", "alphabet", "typography", "case"])
def _(S):
    return [line(poly([(2.5, 19.5), (7.25, 5), (12, 19.5)], r=S.r * 0.4)), line(seg(4.4, 14.5, 10.1, 14.5)),
            line(circle(16.4, 15.6, 3.2)), line(seg(19.6, 11.8, 19.6, 19.5))]


def _piece(cx, cy, s=1.0):
    """Jigsaw piece silhouette: a square with a knob on top and on the right."""
    h = 2.3 * s
    return union(rect(cx - h, cy - h, 2 * h, 2 * h), circle(cx, cy - h - 0.6 * s, 0.95 * s), circle(cx + h + 0.6 * s, cy, 0.95 * s))


@icon("brain-teaser", CAT, "Brain outline with one jigsaw puzzle piece lifted out of it",
      tags=["brain teaser", "puzzle", "riddle", "mental challenge", "logic", "thinking game", "cognitive"])
def _(S):
    m = (0.82, 0, 0, 0.82, 0.6, 3.6)
    brain = tf("M6.5 17C4.3 16.6 3 14.8 3 12.8C3 11.3 3.6 10.2 4.5 9.5C4.3 6.6 6.4 4.5 9 4.5C10.2 3.6 11.5 3.2 13 3.3C15.3 3.4 17 4.6 17.8 6.3"
               "C19.9 7 21 8.8 21 10.8C21 13.3 19.2 15.2 16.8 15.4C16.3 16.8 15 17.7 13.5 17.7L13.5 21H11V17.2Z", m)
    return [shell(brain), detail(tf("M7.5 9.3C8.3 8.2 9.8 8 11 8.7", m)), detail(tf("M8 13C9.3 13.8 11 13.6 12 12.5", m)),
            mark(_piece(18.6, 5.6, 1.15))]


@icon("stem-education", CAT, "Two by two grid holding a flask, a gear, a laptop and a ruler",
      tags=["stem", "steam education", "science technology engineering maths", "lab", "coding class", "robotics club", "curriculum"])
def _(S):
    flask = poly([(5.6, 3.6), (8.4, 3.6), (8.4, 6.8), (10.4, 10), (3.6, 10), (5.6, 6.8)], closed=True)
    ruler = minus(rect(13.6, 14.2, 7, 4.2), rect(15, 14.2, 1, 1.6), rect(17.3, 14.2, 1, 1.6), rect(19.6, 14.2, 0.9, 1.6))
    return [shell(rect(3, 3, 18, 18, rr(S, 3))), detail(seg(12, 3, 12, 21)), detail(seg(3, 12, 21, 12)),
            mark(flask), mark(gear(17, 7.2, 2.3, 6, 0.8, 1.0, 1.4)),
            mark(rect(4.8, 14.2, 5.4, 3.3)), mark(rect(4, 18.4, 7, 0.9)), mark(ruler)]


@icon("peer-review", CAT, "Document with two overlapping magnifying glasses over its text",
      tags=["peer review", "referee", "manuscript review", "scholarly review", "critique", "evaluation", "research"])
def _(S):
    return [cut_stroke(S, rect(3, 3, 13, 17, rr(S, 2.5)), [(12, 14.5, 4.6), (17.5, 11.8, 4.6)]),
            detail(seg(6, 7, 12.5, 7)), detail(seg(6, 10.5, 9.5, 10.5)),
            line(circle(12, 14.5, 3.3)), line(seg(14.3, 16.8, 16.5, 19)),
            line(circle(17.5, 11.8, 3.3)), line(seg(19.8, 14.1, 21.5, 15.8))]


@icon("scientific-method", CAT, "Four arrows chasing each other in a circle around a small flask",
      tags=["scientific method", "experiment cycle", "hypothesis", "research process", "inquiry", "lab", "science"])
def _(S):
    parts = []
    for a0, a1 in ((-78, -28), (12, 62), (102, 152), (192, 242)):
        parts.append(line(arc(12, 12, 8.6, a0, a1)))
        parts.append(line(arrow_head(12, 12, 8.6, a1)))
    parts.append(mark(poly([(10.6, 8), (13.4, 8), (13.4, 11.6), (15.8, 16), (8.2, 16), (10.6, 11.6)], closed=True)))
    return parts


@icon("thesis", CAT, "Thick bound document with a spine band and a mortarboard emblem on the cover",
      tags=["thesis", "dissertation", "graduate research", "bound report", "phd", "masters", "capstone"])
def _(S):
    return [*book_closed(S, x=4, w=16, spine=3.5),
            mark(poly([(10.5, 8.5), (14.5, 6.5), (18.5, 8.5), (14.5, 10.5)], closed=True)),
            thin("M11.8 11.4V14Q14.5 15.8 17.2 14V11.4", 1.3), detail(seg(10.5, 18, 18.5, 18))]


@icon("thesis-defense", CAT, "Presenter at a podium facing three seated panel members behind a long table",
      tags=["thesis defense", "viva", "oral exam", "panel", "dissertation defence", "presentation", "committee"])
def _(S):
    parts = [dot(x, 4.3, 1.7) for x in (6, 12, 18)]
    parts += [mark(rect(3, 7.5, 18, 3, L(S, 0, 1.2))), dot(12, 14, 1.8),
              shell(poly([(8, 16.5), (16, 16.5), (15, 21.5), (9, 21.5)], closed=True, r=S.r * 0.5))]
    return parts


@icon("case-study", CAT, "Folder with a magnifying glass over a small bar chart",
      tags=["case study", "research folder", "analysis", "example", "business school", "investigation", "report"])
def _(S):
    body = poly([(4, 21), (4, 3), (9.5, 3), (11.5, 5.5), (20, 5.5), (20, 21)], closed=True, r=S.r * 0.8)
    return [shell(body), mark(rect(6.3, 10, 2, 3.5)), mark(rect(9.3, 8, 2, 5.5)),
            line(circle(14.5, 15.3, 3)), line(seg(16.7, 17.5, 19, 19.8))]


@icon("literature-review", CAT, "Stack of papers with a magnifying glass lying on top",
      tags=["literature review", "survey of sources", "research", "papers", "state of the art", "scholarship", "reading"])
def _(S):
    return [line(poly([(6, 6), (6, 3), (19, 3), (19, 15)], r=S.r * 0.4)),
            cut_stroke(S, rect(3, 6, 13, 15, rr(S, 2.5)), [(15, 14.5, 5.2)]),
            detail(seg(6, 10, 9.5, 10)), detail(seg(6, 13.5, 8, 13.5)),
            line(circle(15, 14.5, 3.4)), line(seg(17.5, 17, 21, 20.5))]


@icon("margin-notes", CAT, "Page of text lines with small handwritten scribbles in the side margin",
      tags=["margin notes", "marginalia", "annotations", "handwritten notes", "study notes", "comments", "reading notes"])
def _(S):
    return [sheet(S, x=3.5, w=17), detail(seg(6.5, 7, 12, 7)), detail(seg(6.5, 10.5, 12, 10.5)),
            detail(seg(6.5, 14, 12, 14)), detail(seg(6.5, 17.5, 10, 17.5)),
            thin("M14 9.6C14.8 8.2 15.6 11 16.4 9.6C17.2 8.2 18 10.6 18.6 9.6", 1.2),
            thin("M14 13.2C14.8 11.8 15.6 14.6 16.4 13.2", 1.2)]


@icon("plagiarism", CAT, "Two identical documents side by side joined by a copy arrow",
      tags=["plagiarism", "copied text", "duplicate", "similarity check", "copy", "academic integrity", "matching"])
def _(S):
    return [shell(rect(2.5, 4, 6.5, 16, rr(S, 2.5))), shell(rect(15, 4, 6.5, 16, rr(S, 2.5))),
            detail(seg(4.75, 8.5, 6.75, 8.5)), detail(seg(4.75, 12, 6.75, 12)), detail(seg(4.75, 15.5, 6.75, 15.5)),
            detail(seg(17.25, 8.5, 19.25, 8.5)), detail(seg(17.25, 12, 19.25, 12)), detail(seg(17.25, 15.5, 19.25, 15.5)),
            line(seg(10.5, 12, 13.5, 12)), line(poly([(12.3, 10), (14, 12), (12.3, 14)]))]


@icon("book-index", CAT, "Page with letters A B C down the left and short lines with page numbers beside them",
      tags=["index", "book index", "alphabetical", "lookup", "back of book", "page numbers", "reference"])
def _(S):
    parts = [sheet(S, x=3.5, w=17),
             thin("M6.2 9.4L7.6 5.8L9 9.4", 1.2), thin("M6.8 8.2H8.4", 1.2),
             thin("M6.4 10.8H8C8.7 10.8 9 11.2 9 11.6C9 12 8.7 12.4 8 12.4H6.4M8 12.4C8.8 12.4 9.2 12.8 9.2 13.3C9.2 13.8 8.8 14.2 8 14.2H6.4M6.4 10.8V14.2", 1.1),
             thin("M9 16.7C8.7 16.4 8.3 16.3 7.9 16.3C6.9 16.3 6.3 17 6.3 18C6.3 19 6.9 19.7 7.9 19.7C8.3 19.7 8.7 19.6 9 19.3", 1.2)]
    for y in (7.6, 12.5, 18):
        parts += [detail(seg(11.5, y, 14.5, y)), dot(17.2, y, 0.8)]
    return parts
