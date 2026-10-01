"""TypeIcon Core: education & science."""
import math

from dsl import D, P, ST, U, arc, circle, detail, dot, ellipse, fmt, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401


def _axis(origin, deg):
    """Map local (u along the axis, v across it) to grid coordinates."""
    ox, oy = origin
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return lambda u, v: (ox + u * c - v * s, oy + u * s + v * c)


def _lens(cx, cy, a, b, deg):
    """Pointed orbit (two circular arcs meeting in sharp tips), rotated by deg."""
    R = (a * a + b * b) / (2 * b)
    m = _axis((cx, cy), deg)
    p0, p1 = m(-a, 0), m(a, 0)
    return (f"M{fmt(p0[0])} {fmt(p0[1])}A{fmt(R)} {fmt(R)} 0 0 1 {fmt(p1[0])} {fmt(p1[1])}"
            f"A{fmt(R)} {fmt(R)} 0 0 1 {fmt(p0[0])} {fmt(p0[1])}Z")


def _oval(cx, cy, a, b, deg):
    """Ellipse rotated by deg."""
    m = _axis((cx, cy), deg)
    p0, p1 = m(-a, 0), m(a, 0)
    return (f"M{fmt(p0[0])} {fmt(p0[1])}A{fmt(a)} {fmt(b)} {fmt(deg)} 1 0 {fmt(p1[0])} {fmt(p1[1])}"
            f"A{fmt(a)} {fmt(b)} {fmt(deg)} 1 0 {fmt(p0[0])} {fmt(p0[1])}Z")


# --------------------------------------------------------------------------- school

@icon("graduation-cap", "education", "Graduation cap (mortarboard) with tassel", tags=["graduation", "mortarboard", "degree", "school", "university", "student"])
def _(S):
    return [shell(poly([(2.5, 9), (12, 4.5), (21.5, 9), (12, 13.5)], closed=True, r=S.r), stroke_miterlimit="2"),
            line("M6.5 11.5V16C6.5 17.8 9 19.5 12 19.5C15 19.5 17.5 17.8 17.5 16V11.5"),
            line(seg(21, 9.5, 21, 15.5))]


@icon("school-backpack", "education", "School backpack with front pocket", tags=["backpack", "rucksack", "bag", "school", "student"])
def _(S):
    t, b = (4.5, 2) if S.name == "line" else (5.5, 3)
    body = (f"M5 {10.5 + 0}A{t} {t} 0 0 1 {fmt(5 + t)} {fmt(10.5 - t)}H{fmt(19 - t)}A{t} {t} 0 0 1 19 10.5"
            f"V{fmt(21 - b)}A{b} {b} 0 0 1 {fmt(19 - b)} 21H{fmt(5 + b)}A{b} {b} 0 0 1 5 {fmt(21 - b)}Z")
    return [shell(body),
            line(poly([(9.5, 6), (9.5, 3), (14.5, 3), (14.5, 6)], r=S.r * 0.66)),
            detail(rect(8.5, 13, 7, 5, min(S.R, 1.5))), detail(seg(8.5, 15.5, 15.5, 15.5))]


@icon("pencil", "education", "Wooden pencil with eraser", tags=["pencil", "write", "draw", "school", "stationery"])
def _(S):
    m = _axis((3.5, 20.5), -45)
    body = [m(0, 0), m(5.5, -2.5), m(21, -2.5), m(21, 2.5), m(5.5, 2.5)]
    return [shell(poly(body, closed=True, r=S.r * 0.66)),
            detail(seg(*m(5.5, -2.5), *m(5.5, 2.5))), detail(seg(*m(17.5, -2.5), *m(17.5, 2.5)))]


@icon("pen", "education", "Ballpoint pen with a pocket clip", tags=["pen", "ballpoint", "write", "sign", "school", "stationery"])
def _(S):
    m = _axis((4, 20), -45)
    a, e = m(19.5, -2.25), m(19.5, 2.25)
    body = (poly([m(19.5, 2.25), m(3.5, 2.25), m(0, 0), m(3.5, -2.25), a], r=S.r * 0.4)
            + f"A2.25 2.25 0 0 1 {fmt(e[0])} {fmt(e[1])}Z")
    return [shell(body), detail(seg(*m(7, -2.25), *m(7, 2.25))),
            line(poly([m(18.5, -3.25), m(18.5, -5.25), m(12, -5.25)], r=S.r * 0.5))]


@icon("eraser-school", "education", "Rubber eraser block", tags=["eraser", "rubber", "erase", "school", "stationery"])
def _(S):
    m = _axis((12, 11), -45)
    block = [m(-7, -3.5), m(7, -3.5), m(7, 3.5), m(-7, 3.5)]
    return [shell(poly(block, closed=True, r=S.r)), detail(seg(*m(-1.5, -3.5), *m(-1.5, 3.5))),
            line(seg(13, 20.5, 20.5, 20.5))]


@icon("crayon", "education", "Wax crayon with paper wrapper", tags=["crayon", "colour", "color", "draw", "kids", "art"])
def _(S):
    return [shell(poly([(10.5, 3.5), (13.5, 3.5), (15.5, 9), (15.5, 21), (8.5, 21), (8.5, 9)], closed=True, r=S.r * 0.66)),
            detail(seg(8.5, 9, 15.5, 9)), detail(seg(8.5, 17, 15.5, 17))]


@icon("chalkboard", "education", "Chalkboard on an easel", tags=["blackboard", "board", "class", "teach", "school"], aliases=["blackboard"])
def _(S):
    return [shell(rect(3, 3, 18, 13, min(S.R, 2.5))),
            detail(seg(6.5, 7.5, 13.5, 7.5)), detail(seg(6.5, 11.5, 10.5, 11.5)),
            line(seg(7.5, 16, 6, 21)), line(seg(16.5, 16, 18, 21))]


@icon("abacus", "education", "Abacus with beads on three rods", tags=["abacus", "counting", "beads", "math", "arithmetic"])
def _(S):
    beads = [(7, 7.5), (10.5, 7.5), (17, 7.5), (7, 12), (13.5, 12), (17, 12), (7, 16.5), (10.5, 16.5), (14, 16.5)]
    return [shell(rect(3, 3, 18, 18, min(S.R, 2.5))),
            detail(seg(3, 7.5, 21, 7.5)), detail(seg(3, 12, 21, 12)), detail(seg(3, 16.5, 21, 16.5)),
            *[dot(x, y, 1.6) for x, y in beads]]


@icon("desk-globe", "education", "Desk globe on a stand", tags=["globe", "world", "geography", "earth", "school"])
def _(S):
    return [shell(circle(12, 9.5, 5.5)),
            detail(seg(6.5, 9.5, 17.5, 9.5)), detail(ellipse(12, 9.5, 2, 5.5)),
            line(arc(12, 9.5, 9, 50, 220)),
            line(seg(12, 18.5, 12, 21)), line(seg(8, 21, 16, 21))]


# --------------------------------------------------------------------------- science

@icon("atom", "education", "Atom with three electron orbits", tags=["atom", "physics", "science", "nuclear", "electron"])
def _(S):
    orb = _lens if S.name == "line" else _oval
    return [line(orb(12, 12, 9.5, 3.75, d)) for d in (0, 60, 120)] + [dot(12, 12, 1.75)]


@icon("molecule", "education", "Ring molecule with a bonded atom", tags=["molecule", "chemistry", "benzene", "bond", "science"])
def _(S):
    ring = regular(10, 14, 6.5, 6)
    return [shell(poly(ring, closed=True, r=S.r)),
            line(seg(*ring[1], 16.9, 7.1)), shell(circle(18.5, 5.5, 2.25))]


@icon("beaker", "education", "Laboratory beaker with liquid level", tags=["beaker", "lab", "chemistry", "science", "experiment"])
def _(S):
    return [shell(poly([(4.5, 3.5), (19.5, 3.5), (18, 5), (18, 20.5), (6, 20.5), (6, 5)], closed=True, r=S.r)),
            detail(seg(6, 12.5, 18, 12.5)), detail(seg(6, 8.5, 9, 8.5)), detail(seg(6, 16.5, 9, 16.5))]


@icon("telescope", "education", "Telescope on a tripod", tags=["telescope", "astronomy", "space", "stars", "science"])
def _(S):
    m = _axis((13, 8.5), -30)
    tube = [m(-7, -2.5), m(7, -2.5), m(7, 2.5), m(-7, 2.5)]
    eye = [m(-10.5, -1.5), m(-8.5, -1.5), m(-8.5, 1.5), m(-10.5, 1.5)]
    return [shell(poly(tube, closed=True, r=S.r * 0.66)), shell(poly(eye, closed=True, r=S.r * 0.33)),
            line(seg(12, 13, 7.5, 21)), line(seg(12, 13, 16.5, 21))]


def _magnet(c):
    k = lambda v: fmt(v)  # noqa: E731
    if c == 0:
        return "M4 3.5H9V12A3 3 0 0 0 15 12V3.5H20V12A8 8 0 0 1 4 12Z"
    return (f"M4 {k(3.5 + c)}A{c} {c} 0 0 1 {k(4 + c)} 3.5H{k(9 - c)}A{c} {c} 0 0 1 9 {k(3.5 + c)}V12A3 3 0 0 0 15 12"
            f"V{k(3.5 + c)}A{c} {c} 0 0 1 {k(15 + c)} 3.5H{k(20 - c)}A{c} {c} 0 0 1 20 {k(3.5 + c)}V12A8 8 0 0 1 4 12Z")


@icon("magnet", "education", "Horseshoe magnet", tags=["magnet", "magnetic", "attract", "physics", "science"])
def _(S):
    return [shell(_magnet(S.r)), detail(seg(4, 8, 9, 8)), detail(seg(15, 8, 20, 8))]


@icon("protractor", "education", "Semicircular protractor", tags=["protractor", "angle", "measure", "geometry", "math"])
def _(S):
    return [shell(f"M3 16.5A9 9 0 0 1 21 16.5Z" if S.name == "line" else "M4.5 16.5H19.5A1.5 1.5 0 0 0 21 15A9 9 0 0 0 3 15A1.5 1.5 0 0 0 4.5 16.5Z"),
            detail(arc(12, 16.5, 3.5, 180, 360)),
            *[detail(seg(*pt_on(12, 16.5, 6.25, a), *pt_on(12, 16.5, 9, a))) for a in (-135, -90, -45)]]


@icon("math-compass", "education", "Drawing compass with a hinge and two legs", tags=["compass", "geometry", "drawing", "circle", "math"])
def _(S):
    return [line(seg(12, 2.5, 12, 4.5)), shell(circle(12, 7, 2.5)),
            line(seg(10.8, 9.2, 6, 20.5)), line(seg(13.2, 9.2, 18, 20.5)),
            line(arc(12, 7, 9, 58, 122))]


# --------------------------------------------------------------------------- books and papers

@icon("exercise-book", "education", "School exercise book with a label", tags=["notebook", "exercise", "copybook", "school", "homework"])
def _(S):
    return [shell(rect(5, 3, 14, 18, min(S.R, 2.5))), detail(seg(8.5, 3, 8.5, 21)),
            detail(seg(11.5, 8, 16, 8)), detail(seg(11.5, 11.5, 14.5, 11.5))]


@icon("school-bell", "education", "Hand bell with a wooden handle", tags=["bell", "school", "ring", "class", "break"])
def _(S):
    return [shell(rect(10, 2.5, 4, 5.5, min(S.R, 2))),
            shell("M12 8C8.8 8 7.5 11 7.5 14.5C7.5 16.3 6.5 17.3 4.5 17.8V18.5H19.5V17.8C17.5 17.3 16.5 16.3 16.5 14.5C16.5 11 15.2 8 12 8Z" if S.name == "rounded" else
                  "M12 8C8.8 8 7.5 11 7.5 14.5C7.5 16.3 6.5 17.3 4.5 18.5H19.5C17.5 17.3 16.5 16.3 16.5 14.5C16.5 11 15.2 8 12 8Z"),
            dot(12, 21, 1.5)]


@icon("formula", "education", "Written formula with a root and an equals sign", tags=["formula", "equation", "math", "algebra", "science"])
def _(S):
    return [shell(rect(3.5, 3, 17, 18, min(S.R, 2.5))),
            detail(poly([(6.5, 9.5), (8, 9), (9.5, 12), (11.5, 6), (17.5, 6)], r=S.r * 0.5)),
            detail(seg(8, 15, 16, 15)), detail(seg(8, 18, 16, 18))]


@icon("periodic-table", "education", "Periodic table of the elements", tags=["periodic", "elements", "chemistry", "table", "science"])
def _(S):
    return [shell(poly([(2.5, 3.5), (7, 3.5), (7, 7.5), (17, 7.5), (17, 3.5), (21.5, 3.5), (21.5, 14), (2.5, 14)], closed=True, r=S.r * 0.66)),
            detail(seg(7, 7.5, 7, 14)), detail(seg(12, 7.5, 12, 14)), detail(seg(17, 7.5, 17, 14)),
            shell(rect(6.5, 17.5, 11, 3, min(S.R, 1.5)))]


@icon("lab-coat", "education", "Laboratory coat", tags=["lab", "coat", "scientist", "doctor", "science"])
def _(S):
    outline = [(9, 3), (5, 4.5), (3, 18), (6, 18), (7, 11), (7, 21), (17, 21), (17, 11), (18, 18), (21, 18), (19, 4.5), (15, 3)]
    return [shell(poly(outline, closed=True, r=S.r * 0.66)),
            detail(poly([(9, 3), (12, 10.5), (15, 3)], r=S.r * 0.5)), detail(seg(12, 10.5, 12, 21)),
            detail(seg(14, 15, 17, 15))]


@icon("test-paper", "education", "Marked test paper with ticks and a cross", tags=["test", "exam", "paper", "marks", "assessment", "school"], aliases=["exam"])
def _(S):
    return [shell(rect(4, 2.5, 16, 19, min(S.R, 2.5))),
            detail(poly([(7, 7), (8.5, 8.5), (11, 6)], r=S.r * 0.3)), detail(seg(13, 7.25, 17, 7.25)),
            detail(poly([(7, 12), (8.5, 13.5), (11, 11)], r=S.r * 0.3)), detail(seg(13, 12.25, 17, 12.25)),
            detail(seg(7.5, 16, 10.5, 19)), detail(seg(10.5, 16, 7.5, 19)), detail(seg(13, 17.5, 17, 17.5))]


@icon("grade-a", "education", "Top grade A plus", tags=["grade", "a-plus", "score", "mark", "excellent", "school"])
def _(S):
    return [line(poly([(3, 20.5), (8.5, 4.5), (14, 20.5)], r=S.r), stroke_miterlimit="3"), line(seg(5.2, 15, 11.8, 15)),
            line(seg(18.5, 5, 18.5, 12)), line(seg(15, 8.5, 22, 8.5))]


@icon("certificate-education", "education", "Certificate with a seal and ribbons", tags=["certificate", "award", "achievement", "qualification", "school"])
def _(S):
    return [shell(rect(2.5, 4, 19, 16, min(S.R, 2.5))),
            detail(seg(5.5, 8, 12.5, 8)), detail(seg(5.5, 11.5, 10.5, 11.5)), detail(seg(5.5, 15, 10.5, 15)),
            detail(circle(16.5, 10.5, 2.5)), detail(poly([(15, 13), (14.5, 17)], r=0)), detail(poly([(18, 13), (18.5, 17)], r=0))]


@icon("diploma", "education", "Rolled diploma tied with a ribbon", tags=["diploma", "scroll", "degree", "graduation", "certificate"])
def _(S):
    return [shell("M5 7.5H19A2 3.5 0 0 1 19 14.5H5A2 3.5 0 0 1 5 7.5Z"),
            detail(ellipse(5, 11, 1.5 if S.name == "line" else 1.75, 3.5)), detail(seg(12, 7.5, 12, 14.5)),
            line(poly([(11, 14.5), (9, 20.5)], r=0)), line(poly([(13, 14.5), (15, 20.5)], r=0))]


@icon("lecture", "education", "Teacher presenting at a board", tags=["lecture", "teacher", "presentation", "class", "lesson", "school"])
def _(S):
    return [shell(rect(9.5, 3, 12, 9.5, min(S.R, 2))), detail(seg(12.5, 6.5, 18.5, 6.5)), detail(seg(12.5, 9.5, 16, 9.5)),
            shell(circle(5.5, 11, 2.5)),
            line("M2.5 21V18C2.5 16.3 3.8 15 5.5 15C7.2 15 8.5 16.3 8.5 18V21" if S.name == "rounded" else poly([(2.5, 21), (2.5, 17), (4.5, 15), (6.5, 15), (8.5, 17), (8.5, 21)]))]


@icon("online-course", "education", "Laptop playing a lesson video", tags=["online", "course", "e-learning", "webinar", "lesson", "video"], aliases=["e-learning"])
def _(S):
    return [shell(rect(4, 4, 16, 11.5, min(S.R, 2.5))), detail(poly([(10.5, 7), (14.5, 9.75), (10.5, 12.5)], closed=True, r=S.r * 0.4)),
            line(poly([(2, 19), (22, 19)], r=0) if S.name == "line" else "M2.5 18.5H21.5")]


@icon("bookmark-book", "education", "Book with a ribbon bookmark", tags=["book", "bookmark", "reading", "saved", "library"])
def _(S):
    return [shell(rect(5, 3, 14, 18, min(S.R, 2.5))), detail(seg(8.5, 3, 8.5, 21)),
            detail(poly([(12, 3), (12, 11), (14, 9.5), (16, 11), (16, 3)], r=S.r * 0.33))]


@icon("reading", "education", "Person reading an open book", tags=["reading", "reader", "book", "study", "student", "library"])
def _(S):
    return [shell(circle(12, 5.5, 3)),
            shell(poly([(2.5, 11.5), (12, 14), (21.5, 11.5), (21.5, 19.5), (12, 21.5), (2.5, 19.5)], closed=True, r=S.r * 0.66)),
            detail(seg(12, 14, 12, 21.5))]


@icon("glasses-reading", "education", "Pair of reading glasses", tags=["glasses", "spectacles", "reading", "eyewear", "vision"], aliases=["spectacles"])
def _(S):
    def lens(x0, x1):
        if S.name == "line":
            return f"M{x0} 11H{x1}V13A4 4 0 0 1 {x0} 13Z"
        return f"M{x0 + 1.5} 11H{x1 - 1.5}A1.5 1.5 0 0 1 {x1} 12.5V13A4 4 0 0 1 {x0} 13V12.5A1.5 1.5 0 0 1 {x0 + 1.5} 11Z"
    return [shell(lens(2.5, 10.5)), shell(lens(13.5, 21.5)),
            line("M10.5 12.5C11.5 11.5 12.5 11.5 13.5 12.5"),
            line(seg(3, 11, 4.5, 6.5)), line(seg(21, 11, 19.5, 6.5))]


@icon("dictionary", "education", "Dictionary with A on the cover", tags=["dictionary", "words", "language", "reference", "book"])
def _(S):
    return [shell(rect(4.5, 3, 15, 18, min(S.R, 2.5))), detail(seg(8, 3, 8, 21)),
            detail(poly([(10.5, 17), (13.75, 7), (17, 17)], r=S.r * 0.5), stroke_miterlimit="3"), detail(seg(11.8, 13.5, 15.7, 13.5))]


@icon("encyclopedia", "education", "Row of encyclopedia volumes", tags=["encyclopedia", "books", "volumes", "reference", "library"])
def _(S):
    return [shell(rect(3, 4, 5, 17, min(S.R, 1.5))), shell(rect(9.5, 4, 5, 17, min(S.R, 1.5))),
            shell(poly([(16, 5.2), (20.8, 3.9), (22, 20), (17.2, 21.3)], closed=True, r=S.r * 0.5)),
            detail(seg(3, 8, 8, 8)), detail(seg(9.5, 8, 14.5, 8)), detail(seg(3, 17, 8, 17)), detail(seg(9.5, 17, 14.5, 17))]


@icon("quiz", "education", "Multiple-choice quiz with one answer ticked", tags=["quiz", "test", "multiple-choice", "questions", "poll", "exam"])
def _(S):
    return [shell(circle(5, 5, 2)), line(poly([(2.5, 12), (4.5, 14), (8, 10)], r=S.r * 0.5)), shell(circle(5, 19, 2)),
            line(seg(11, 5, 21, 5)), line(seg(11, 12, 21, 12)), line(seg(11, 19, 21, 19))]


@icon("homework", "education", "Worksheet with a pencil", tags=["homework", "assignment", "study", "worksheet", "school"])
def _(S):
    return [shell(rect(3, 3, 11.5, 18, min(S.R, 2.5))),
            detail(seg(6, 7.5, 11.5, 7.5)), detail(seg(6, 11.5, 11.5, 11.5)), detail(seg(6, 15.5, 9.5, 15.5)),
            shell(poly([(16.5, 3), (21, 3), (21, 16), (18.75, 20.5), (16.5, 16)], closed=True, r=S.r * 0.5)),
            detail(seg(16.5, 6.5, 21, 6.5)), detail(seg(16.5, 16, 21, 16))]
