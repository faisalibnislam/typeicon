"""TypeIcon Core: learning (batch learning_004).

Study aids, graphic organisers, classroom layouts and language and maths teaching tools, drawn from the
objects themselves. Front or top views; small marks sit inside a clear silhouette so they survive at 16 px.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, rotation, transform_path  # noqa: F401

CAT = "learning"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rot_pts(points, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in points]


def scale_d(d, k, cx, cy):
    """Scale a closed outline by k about (cx, cy)."""
    return path_to_d(transform_path(P(d), (k, 0, 0, k, cx - k * cx, cy - k * cy)))


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def thin(d, S, w=1.4):
    """Solid region of a thin stroke along d (for small letters and text lines inside shapes)."""
    return mark(path_to_d(ST(d, w, S.cap, S.join)))


def pt_on(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def glyph_d(ch, x, y, w, h, S, sw=1.4):
    """Tiny capital letter (A, B, C, K, L, T, W) as a solid region d-string, top-left at (x, y)."""
    f = fmt
    if ch == "A":
        d = f"M{f(x)} {f(y + h)}L{f(x + w / 2)} {f(y)}L{f(x + w)} {f(y + h)}M{f(x + w * 0.22)} {f(y + h * 0.66)}H{f(x + w * 0.78)}"
    elif ch == "B":
        d = (f"M{f(x)} {f(y)}V{f(y + h)}M{f(x)} {f(y)}H{f(x + w * 0.6)}Q{f(x + w)} {f(y)} {f(x + w)} {f(y + h * 0.25)}"
             f"Q{f(x + w)} {f(y + h * 0.5)} {f(x + w * 0.6)} {f(y + h * 0.5)}H{f(x)}M{f(x + w * 0.6)} {f(y + h * 0.5)}"
             f"Q{f(x + w * 1.05)} {f(y + h * 0.5)} {f(x + w * 1.05)} {f(y + h * 0.75)}Q{f(x + w * 1.05)} {f(y + h)} {f(x + w * 0.6)} {f(y + h)}H{f(x)}")
    elif ch == "K":
        d = f"M{f(x)} {f(y)}V{f(y + h)}M{f(x + w)} {f(y)}L{f(x)} {f(y + h * 0.6)}M{f(x + w * 0.35)} {f(y + h * 0.45)}L{f(x + w)} {f(y + h)}"
    elif ch == "L":
        d = f"M{f(x)} {f(y)}V{f(y + h)}H{f(x + w)}"
    elif ch == "T":
        d = f"M{f(x)} {f(y)}H{f(x + w)}M{f(x + w / 2)} {f(y)}V{f(y + h)}"
    elif ch == "W":
        d = f"M{f(x)} {f(y)}L{f(x + w * 0.25)} {f(y + h)}L{f(x + w * 0.5)} {f(y + h * 0.35)}L{f(x + w * 0.75)} {f(y + h)}L{f(x + w)} {f(y)}"
    elif ch == "C":
        d = f"M{f(x + w)} {f(y + h * 0.15)}Q{f(x + w * 0.6)} {f(y)} {f(x + w * 0.35)} {f(y)}Q{f(x)} {f(y)} {f(x)} {f(y + h / 2)}Q{f(x)} {f(y + h)} {f(x + w * 0.35)} {f(y + h)}Q{f(x + w * 0.6)} {f(y + h)} {f(x + w)} {f(y + h * 0.85)}"
    else:
        raise ValueError(ch)
    return path_to_d(ST(d, sw, S.cap, S.join))


def glyph(ch, x, y, w, h, S, sw=1.4):
    """Tiny capital letter as a solid mark, top-left at (x, y)."""
    return mark(glyph_d(ch, x, y, w, h, S, sw))


# ============================================================================ study aids and charts

@icon("study-guide", CAT, "Booklet with a small signpost on its cover pointing two ways",
      tags=["study guide", "revision guide", "exam prep", "booklet", "signpost", "cheat sheet", "review sheet"])
def _(S):
    ar = L(S, 0, 0.5)
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 3))),
        mark(rect(11.2, 6.3, 1.6, 11.7)),
        mark(poly([(7.6, 6.6), (14.6, 6.6), (16.6, 8.5), (14.6, 10.4), (7.6, 10.4)], closed=True, r=ar)),
        mark(poly([(16.4, 11.6), (9.4, 11.6), (7.4, 13.5), (9.4, 15.4), (16.4, 15.4)], closed=True, r=ar)),
    ]


def bead(S, x, y, r):
    return circle(x, y, r) if S.name == "rounded" else poly([pt_on(x, y, r * 1.08, 22.5 + 45 * i) for i in range(8)], closed=True)


@icon("counting-bead-string", CAT, "String of ring beads above a row of solid beads, looped at one end and tailed at the other",
      tags=["counting beads", "bead string", "abacus", "maths manipulative", "counting", "early maths", "bead chain"])
def _(S):
    xs = [5.8, 9.8, 13.8, 17.8]
    y1, y2 = 6.5, 17.5
    parts = [
        line(seg(2, y1, 4, y1)), line(seg(2, y2, 4, y2)),
        line(f"M19.7 {fmt(y1)}C21.3 {fmt(y1)} 21.3 {fmt(y2)} 19.7 {fmt(y2)}"),
    ]
    for x in xs:
        parts.append(mark(minus(bead(S, x, y1, 1.95), bead(S, x, y1, 0.75))))
        parts.append(mark(bead(S, x, y2, 1.95)))
    return parts


@icon("number-balance", CAT, "Balance beam resting on a triangle stand with round weights hung from hooks on both arms",
      tags=["number balance", "maths balance", "weights", "equation", "addition", "early maths", "scales"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 3.6, L(S, 0.6, 1.8))),
        shell(poly([(12, 7.1), (15.6, 21), (8.4, 21)], closed=True, r=S.r * 0.6)),
        line(seg(4.2, 7.1, 4.2, 16)), line(seg(19.5, 7.1, 19.5, 11)),
        mark(bead(S, 4.2, 11, 1.9)), mark(bead(S, 4.2, 16.4, 1.9)), mark(bead(S, 19.5, 12.8, 2.6)),
    ]


# pentomino tiling of a 5 x 3 board: cells labelled by piece (N, V and L)
PENT = ["00111", "20001", "22221"]


@icon("pentominoes", CAT, "Rectangle tiled by three differently shaped five-square pieces",
      tags=["pentominoes", "tiling puzzle", "polyomino", "spatial reasoning", "math puzzle", "jigsaw", "tangram"])
def _(S):
    x0, y0, cw, ch = 2.5, 5.25, 3.8, 4.5
    parts = [shell(rect(x0, y0, 19, 13.5, rr(S, 3)))]
    cols, rows = 5, 3
    for r in range(rows):
        for c in range(cols - 1):
            if PENT[r][c] != PENT[r][c + 1]:
                x = x0 + cw * (c + 1)
                parts.append(detail(seg(x, y0 + ch * r, x, y0 + ch * (r + 1))))
    for r in range(rows - 1):
        for c in range(cols):
            if PENT[r][c] != PENT[r + 1][c]:
                y = y0 + ch * (r + 1)
                parts.append(detail(seg(x0 + cw * c, y, x0 + cw * (c + 1), y)))
    return parts


@icon("art-smock", CAT, "Long-sleeved smock with a few paint spots on the front",
      tags=["art smock", "paint apron", "painting", "messy play", "art class", "overall", "protective clothing"])
def _(S):
    body = poly([(9, 3), (15, 3), (19, 5), (22, 15.5), (19.6, 16.6), (17.6, 11.5), (19, 21), (5, 21), (6.4, 11.5),
                 (4.4, 16.6), (2, 15.5), (5, 5)], closed=True, r=S.r)
    return [
        shell(body),
        detail("M9 3C9.4 5.6 14.6 5.6 15 3"),
        mark(circle(9.8, 15.2, 1.5)), mark(circle(14.6, 17.4, 1.2)), mark(circle(13.6, 12.8, 1.0)),
    ]


@icon("prefect-badge", CAT, "Small shield pin badge with a bar across the top and a star",
      tags=["prefect badge", "school badge", "monitor badge", "pin", "shield", "student leader", "honour"])
def _(S):
    if S.name == "line":
        d = "M4 3H20V11.5C20 16.5 16.5 19.8 12 22C7.5 19.8 4 16.5 4 11.5Z"
    else:
        d = "M6.2 3H17.8Q20 3 20 5.2V11.5C20 16 16.8 19.5 12.9 21.6Q12 22 11.1 21.6C7.2 19.5 4 16 4 11.5V5.2Q4 3 6.2 3Z"
    pts = []
    for i in range(10):
        a = -90 + 36 * i
        rad = 3.4 if i % 2 == 0 else 1.6
        pts.append(pt_on(12, 14, rad, a))
    return [shell(d), detail(seg(4, 8, 20, 8)), mark(poly(pts, closed=True, r=L(S, 0, 0.4)))]


@icon("school-assembly", CAT, "Stage with a lectern on top and a row of pupils seen from behind in front of it",
      tags=["school assembly", "auditorium", "speech", "students", "hall", "presentation", "audience"])
def _(S):
    parts = [
        shell(rect(2.5, 2.5, 19, 9.5, rr(S, 3))),
        mark(poly([(9.8, 6), (14.2, 6), (14.8, 10), (9.2, 10)], closed=True, r=L(S, 0, 0.4))),
        mark(circle(12, 4.6, 0.75)),
    ]
    for x in (5, 9.7, 14.3, 19):
        parts.append(mark(circle(x, 15.4, 1.6)))
        parts.append(mark(f"M{fmt(x - 2.3)} 21.6V20Q{fmt(x - 2.3)} 17.7 {fmt(x)} 17.7Q{fmt(x + 2.3)} 17.7 {fmt(x + 2.3)} 20V21.6Z"))
    return parts


@icon("exit-ticket", CAT, "Ticket with a tear-off stub, a question line and a check mark",
      tags=["exit ticket", "exit slip", "formative assessment", "check for understanding", "end of lesson", "reflection", "quick quiz"])
def _(S):
    tk = minus(rect(2.5, 5, 19, 14, rr(S, 3)), circle(16.5, 5, 1.7), circle(16.5, 19, 1.7))
    return [
        shell(tk),
        detail(seg(6, 9.5, 12.5, 9.5)),
        detail(poly([(6, 14), (8.3, 16), (12.5, 12.3)], r=S.r)),
        detail(seg(16.5, 8.6, 16.5, 10.6)), detail(seg(16.5, 13.4, 16.5, 15.4)),
    ]


@icon("word-wall", CAT, "Board with two letter headings and word cards pinned under each",
      tags=["word wall", "vocabulary", "sight words", "literacy", "classroom display", "spelling", "alphabet"])
def _(S):
    parts = [shell(rect(2.5, 2.5, 19, 19, rr(S, 3)))]
    parts.append(glyph("A", 5.2, 5, 3.6, 4.4, S, 1.5))
    parts.append(glyph("B", 14.6, 5, 3.6, 4.4, S, 1.5))
    for x in (4.6, 13.6):
        parts.append(mark(rect(x, 11.6, 5.8, 2.6, L(S, 0.3, 0.8))))
        parts.append(mark(rect(x, 15.8, 5.8, 2.6, L(S, 0.3, 0.8))))
    return parts


@icon("kwl-chart", CAT, "Sheet divided into three columns headed K, W and L",
      tags=["kwl chart", "know want learn", "graphic organizer", "graphic organiser", "reading strategy", "brainstorm", "planning sheet"])
def _(S):
    parts = [
        shell(rect(2.5, 3, 19, 18, rr(S, 3))),
        detail(seg(2.5, 11.5, 21.5, 11.5)),
        detail(seg(8.75, 3, 8.75, 21)), detail(seg(15.25, 3, 15.25, 21)),
    ]
    for ch, x in (("K", 4.3), ("W", 10.2), ("L", 17.6)):
        parts.append(glyph(ch, x, 4.9, 2.9, 3.6, S, 1.3))
    return parts


@icon("t-chart", CAT, "Sheet divided by a large T into two columns with a heading bar on each",
      tags=["t chart", "compare and contrast", "pros and cons", "graphic organizer", "graphic organiser", "two columns", "note taking"])
def _(S):
    parts = [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(seg(3, 8.5, 21, 8.5)), detail(seg(12, 8.5, 12, 21)),
        mark(rect(5.2, 4.6, 5, 1.6, 0.4)), mark(rect(13.8, 4.6, 5, 1.6, 0.4)),
    ]
    for x in (5.4, 14.4):
        parts.append(mark(circle(x + 0.3, 12.6, 1.05)))
        parts.append(mark(circle(x + 0.3, 17, 1.05)))
    return parts


@icon("frayer-model", CAT, "Square split into four boxes by a cross with an oval label in the middle",
      tags=["frayer model", "vocabulary organizer", "definition chart", "graphic organizer", "four square", "word study", "concept map"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(seg(3, 12, 6.8, 12)), detail(seg(17.2, 12, 21, 12)),
        detail(seg(12, 3, 12, 8.6)), detail(seg(12, 15.4, 12, 21)),
        detail(ellipse(12, 12, 5, 3.2)),
    ]


@icon("paragraph-burger", CAT, "Burger with a bun, filling and bun each showing a line of text for paragraph parts",
      tags=["paragraph burger", "essay structure", "writing organizer", "topic sentence", "hamburger paragraph", "writing", "conclusion"])
def _(S):
    top = "M3 9.5A9 6.5 0 0 1 21 9.5Z"
    return [
        shell(top),
        thin(seg(8, 6.9, 16, 6.9), S, 1.5),
        shell(poly([(3, 12.5), (21, 12.5), (21, 15.5), (3, 15.5)], closed=True, r=S.r * 0.5)),
        shell(rect(3, 18, 18, 3.5, L(S, 0.6, 1.7))),
    ]


@icon("sentence-strip", CAT, "Long thin card with handwriting on a ruled baseline",
      tags=["sentence strip", "writing strip", "handwriting", "literacy", "ruled card", "sentence building", "word order"])
def _(S):
    scribble = "M5.6 12.4C6.4 9.2 7.6 9.2 8.2 12.4C8.8 9.2 10 9.2 10.6 12.4C11.2 9.2 12.4 9.2 13 12.4C13.6 9.2 14.8 9.2 15.4 12.4"
    return [
        shell(rect(2.5, 6.5, 19, 11, rr(S, 2.5))),
        detail(seg(5.5, 14.5, 18.5, 14.5)),
        thin(scribble, S, 1.3),
    ]


def kidney_d(S):
    if S.name == "line":
        return "M2.5 16.5C2.5 12 7 9.5 12 9.5C17 9.5 21.5 12 21.5 16.5L19.6 20C16.5 17.2 14 17.4 12 17.4C10 17.4 7.5 17.2 4.4 20Z"
    return ("M3 16C3 12.2 7 9.5 12 9.5C17 9.5 21 12.2 21 16C21 18.8 19 20 17.4 20C15.4 20 14 17.8 12 17.8"
            "C10 17.8 8.6 20 6.6 20C5 20 3 18.8 3 16Z")


@icon("kidney-table", CAT, "Kidney-shaped table from above tilted on the page with chairs along its curved side",
      tags=["kidney table", "small group table", "guided reading", "teacher table", "bean table", "classroom furniture", "top view"])
def _(S):
    ang = -24
    table = path_to_d(transform_path(P(rot(scale_d(kidney_d(S), 0.86, 12, 14), ang, 12, 12.5)), (1, 0, 0, 1, 0.3, 1.4)))
    parts = [shell(table)]
    for x, y in ((4.8, 8.4), (8.8, 4.8), (14, 3.8), (19.2, 6.4)):
        a = math.radians(ang)
        cx, cy = 12 + (x - 12) * math.cos(a) - (y - 12.5) * math.sin(a), 12.5 + (x - 12) * math.sin(a) + (y - 12.5) * math.cos(a)
        parts.append(mark(rect(cx - 1.6, cy + 0.0, 3.2, 3.2, L(S, 0.4, 1.4))))
    return parts


@icon("clip-chart", CAT, "Behaviour chart of stacked bands with a clothespin clipped onto the middle band",
      tags=["clip chart", "behavior chart", "behaviour chart", "clothespin", "classroom management", "peg chart", "rewards"])
def _(S):
    board = rect(4, 2.5, 16, 19, rr(S, 3))
    pin = poly([(10.3, 7), (13.7, 7), (13.7, 11), (13.1, 12.4), (13.7, 13.8), (13.7, 19), (10.3, 19), (10.3, 13.8),
                (10.9, 12.4), (10.3, 11)], closed=True, r=L(S, 0, 0.5))
    cut = ST(pin, 2 * 1.5, "round", "round")
    parts = [shell(board)]
    for y in (9, 15):
        ln = ST(seg(4, y, 20, y), 2.0, S.cap, S.join)
        parts.append(mark(path_to_d(D(ln, U(P(pin), cut)))))
    slit = seg(12, 14.2, 12, 19.5)
    parts.append(mark(minus(pin, path_to_d(ST(slit, 0.8, "butt", "miter")))))
    return parts


@icon("classroom-noise-meter", CAT, "Half-circle dial from quiet to loud with a needle and an open mouth below",
      tags=["noise meter", "volume meter", "sound level", "voice level", "quiet", "classroom management", "loud"])
def _(S):
    cx, cy = 12, 13.5
    d = f"M2.5 {cy}A9.5 9.5 0 0 1 21.5 {cy}Z"
    nx, ny = pt_on(cx, cy, 6.6, -58)
    parts = [shell(d), detail(seg(cx, cy, nx, ny)), dot(cx, cy, 1.9)]
    for a in (-165, -130, -95, -28):
        x, y = pt_on(cx, cy, 6.3, a)
        parts.append(mark(circle(x, y, 0.95)))
    parts.append(mark(ellipse(12, 18.9, 3.2, 2)))
    return parts


@icon("desk-cluster", CAT, "Four desks pushed together into a square seen from above with a chair at each",
      tags=["desk cluster", "table group", "group seating", "pod", "classroom layout", "collaboration", "top view"])
def _(S):
    parts = [
        shell(rect(5.5, 7, 13, 10, rr(S, 3))),
        detail(seg(12, 7, 12, 17)), detail(seg(5.5, 12, 18.5, 12)),
    ]
    for x in (8.75, 15.25):
        parts.append(mark(rect(x - 2, 2.2, 4, 2.2, L(S, 0.3, 1.1))))
        parts.append(mark(rect(x - 2, 19.6, 4, 2.2, L(S, 0.3, 1.1))))
    return parts


@icon("u-shaped-seating", CAT, "Three desks in a U shape around an open centre seen from above",
      tags=["u shaped seating", "horseshoe layout", "classroom layout", "seating plan", "discussion setup", "desk arrangement", "top view"])
def _(S):
    return [
        shell(rect(2.5, 3, 5.5, 11.5, rr(S, 2.5))),
        shell(rect(16, 3, 5.5, 11.5, rr(S, 2.5))),
        shell(rect(2.5, 17.5, 19, 4, rr(S, 2))),
    ]


@icon("campus-quad", CAT, "Square lawn crossed by diagonal paths with a building on each side",
      tags=["campus quad", "quadrangle", "courtyard", "university", "school grounds", "lawn", "campus map"])
def _(S):
    return [
        shell(rect(7, 7, 10, 10, rr(S, 2))),
        detail(seg(7, 7, 17, 17)), detail(seg(17, 7, 7, 17)),
        mark(rect(8.6, 1.8, 6.8, 2.6, L(S, 0.3, 1))), mark(rect(8.6, 19.6, 6.8, 2.6, L(S, 0.3, 1))),
        mark(rect(1.8, 8.6, 2.6, 6.8, L(S, 0.3, 1))), mark(rect(19.6, 8.6, 2.6, 6.8, L(S, 0.3, 1))),
    ]


@icon("study-carrel", CAT, "Desk between two tall side panels with a small shelf above and books on it",
      tags=["study carrel", "library desk", "quiet study", "cubicle", "privacy desk", "focus", "library"])
def _(S):
    return [
        line(seg(4, 2.5, 4, 21.5)), line(seg(20, 2.5, 20, 21.5)),
        line(seg(4, 8.5, 20, 8.5)),
        mark(rect(8.4, 3.6, 2.2, 3.6)), mark(rect(11.2, 4.4, 2.2, 2.8)), mark(rect(14, 3.6, 1.8, 3.6)),
        shell(rect(4, 14.5, 16, 3.6, L(S, 0.4, 1.4))),
    ]


@icon("vowel-chart", CAT, "Four-sided vowel quadrilateral with a slanted left edge and dots at its corners and centre",
      tags=["vowel chart", "vowel quadrilateral", "phonetics", "linguistics", "pronunciation", "speech sounds", "phonology"])
def _(S):
    q = poly([(3, 4), (21, 4), (21, 20), (12.5, 20)], closed=True, r=S.r)
    parts = [shell(q)]
    for x, y in ((7.3, 8), (16.6, 8), (16.6, 15.6), (13.2, 15.6)):
        parts.append(mark(bead(S, x, y, 1.35)))
    parts.append(mark(bead(S, 12, 11.8, 1.35)))
    return parts


@icon("rhyme-scheme", CAT, "Four lines of verse with the letters A, B, A, B at their ends",
      tags=["rhyme scheme", "poetry", "verse", "stanza", "end rhyme", "poem", "abab"])
def _(S):
    parts = []
    for i, ch in enumerate("ABAB"):
        y = 4.3 + 5.1 * i
        parts.append(line(seg(3, y + 1.8, 13, y + 1.8)))
        parts.append(glyph(ch, 16.4, y, 3.4, 3.6, S, 1.3))
    return parts


def leaf_d(S, cx, top, bottom, w):
    my = (top + bottom) / 2
    k = w * 0.7
    if S.name == "line":
        return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + k)} {fmt(top + (my - top) * 0.45)} {fmt(cx + k)} {fmt(bottom - (bottom - my) * 0.45)} {fmt(cx)} {fmt(bottom)}"
                f"C{fmt(cx - k)} {fmt(bottom - (bottom - my) * 0.45)} {fmt(cx - k)} {fmt(top + (my - top) * 0.45)} {fmt(cx)} {fmt(top)}Z")
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + k * 1.15)} {fmt(top + (my - top) * 0.55)} {fmt(cx + k * 1.1)} {fmt(bottom - 0.5)} {fmt(cx)} {fmt(bottom)}"
            f"C{fmt(cx - k * 1.1)} {fmt(bottom - 0.5)} {fmt(cx - k * 1.15)} {fmt(top + (my - top) * 0.55)} {fmt(cx)} {fmt(top)}Z")


@icon("haiku", CAT, "Three rows of dots in a five, seven, five pattern below a small leaf",
      tags=["haiku", "poetry", "five seven five", "syllables", "japanese poem", "nature poem", "poem"])
def _(S):
    parts = [shell(rot(leaf_d(S, 12, 1.8, 10.6, 4.6), 32, 12, 6.2)), line(rot(seg(12, 10.6, 12, 12.4), 32, 12, 6.2))]
    for y, n in ((14.6, 5), (18.1, 7), (21.6, 5)):
        x0 = 12 - 3 * (n - 1) / 2
        for i in range(n):
            x = x0 + 3 * i
            parts.append(mark(circle(x, y, 1.1) if S.name == "rounded" else rect(x - 1, y - 1, 2, 2)))
    return parts


@icon("algebra-tiles", CAT, "Large square tile, a long rectangular tile and small unit squares grouped together",
      tags=["algebra tiles", "x squared", "polynomial", "algebra", "maths manipulative", "factoring", "unit tiles"])
def _(S):
    parts = [
        shell(rect(2.5, 2.5, 11, 11, rr(S, 2.5))),
        shell(rect(16, 2.5, 5.5, 11, rr(S, 2.5))),
    ]
    for x in (2.45, 7.55, 12.65, 17.75):
        parts.append(mark(rect(x, 16.8, 3.8, 3.8, L(S, 0.3, 1.1))))
    return parts


# ============================================================================ language, history and thinking tools

def branch_to(cx, cy, tx, ty, r):
    """Segment from (cx, cy) towards (tx, ty), stopping r short of the target."""
    dx, dy = tx - cx, ty - cy
    ln = math.hypot(dx, dy)
    return seg(cx, cy, tx - dx / ln * r, ty - dy / ln * r)


@icon("language-family-tree", CAT, "Tree with three branches ending in round leaves, each holding a different letter",
      tags=["language family tree", "linguistics", "language origins", "etymology", "proto language", "descendants", "language map"])
def _(S):
    parts = [line(seg(12, 21.5, 12, 15.5))]
    leaves = ((4.8, 7.6, "A"), (12, 5.2, "B"), (19.2, 7.6, "C"))
    for x, y, ch in leaves:
        parts.append(line(branch_to(12, 15.5, x, y, 2.6)))
    for x, y, ch in leaves:
        disc = bead(S, x, y, 3.05)
        letter = glyph_d(ch, x - 1.25, y - 1.6, 2.5, 3.2, S, 1.05)
        parts.append(mark(minus(disc, letter)))
    return parts


@icon("primary-source", CAT, "Old document with a torn lower edge under a magnifying glass showing a seal",
      tags=["primary source", "historical document", "archive", "source analysis", "history", "manuscript", "evidence"])
def _(S):
    doc = poly([(3.5, 2.5), (14.5, 2.5), (14.5, 16.4), (13, 18.8), (11.6, 16.6), (10, 19), (8.4, 16.6), (6.8, 19), (5.4, 16.8), (3.5, 19)], closed=True, r=S.r * 0.3)
    lens = circle(16, 14.6, 4)
    return [
        shell(behind_doc(doc, lens)),
        detail(seg(6.3, 6.6, 11.7, 6.6)), detail(seg(6.3, 10.4, 9.4, 10.4)),
        shell(lens), mark(circle(16, 14.6, 1.25)),
        line(seg(19, 17.6, 21.6, 20.6)),
    ]


def behind_doc(back, front, gap=1.6):
    cut = U(P(front), ST(front, 2 * (gap + 1), "round", "round"))
    return path_to_d(D(P(back), cut))


@icon("word-builder", CAT, "Three alphabet blocks stacked in a pyramid, each showing a letter",
      tags=["word builder", "alphabet blocks", "letter blocks", "spelling", "phonics", "early literacy", "toy blocks"])
def _(S):
    parts = []
    for x, y, ch in ((8.5, 3, "A"), (3.5, 13.5, "B"), (14, 13.5, "C")):
        parts.append(shell(rect(x, y, 7, 7, L(S, 0.4, 1.8))))
        parts.append(glyph(ch, x + 1.9, y + 1.6, 3.2, 3.8, S, 1.2))
    return parts


@icon("dot-to-dot", CAT, "Star-shaped dots with the first few joined by a line and the rest still to connect",
      tags=["dot to dot", "connect the dots", "join the dots", "drawing puzzle", "activity sheet", "numbers", "kids activity"])
def _(S):
    pts = []
    for i in range(10):
        r = 9.3 if i % 2 == 0 else 4.4
        pts.append(pt_on(12, 12.8, r, -90 + 36 * i))
    parts = [line(poly(pts[:8], r=L(S, 0.7, 1.4)))]
    for x, y in pts:
        parts.append(mark(bead(S, x, y, 1.7)))
    return parts


@icon("matching-exercise", CAT, "Two columns of items joined across by crossing lines",
      tags=["matching exercise", "match up", "match the pairs", "worksheet", "join with lines", "quiz", "pairing"])
def _(S):
    ys = (5.5, 12, 18.5)
    parts = []
    for y in ys:
        parts.append(mark(rect(2.5, y - 2, 4, 4, L(S, 0.3, 1.2))))
        parts.append(mark(circle(19.5, y, 2.1) if S.name == "rounded" else bead(S, 19.5, y, 2.1)))
    for a, b in ((0, 1), (1, 0), (2, 2)):
        parts.append(line(seg(8.8, ys[a], 15.2, ys[b])))
    return parts


@icon("odd-one-out", CAT, "Three small circles above a square that has a ring drawn around it",
      tags=["odd one out", "spot the difference", "which one is different", "classification", "reasoning", "puzzle", "sorting"])
def _(S):
    parts = [shell(circle(12, 16, 4.8)), mark(rect(9.8, 13.8, 4.4, 4.4, L(S, 0, 1.4)))]
    for x in (5, 12, 19):
        parts.append(mark(bead(S, x, 5, 2.6)))
    return parts


@icon("pattern-sequence", CAT, "Grid of alternating circles and squares with the last cell left as an empty dashed box",
      tags=["pattern sequence", "what comes next", "repeating pattern", "patterns", "early maths", "missing shape", "algebra readiness"])
def _(S):
    xs, ys = (4.2, 11.6, 19), (7.2, 16.8)
    parts = []
    k = 0
    for y in ys:
        for x in xs:
            if k == 5:
                h, q = 2.6, L(S, 0.9, 0.4)
                parts += [line(seg(x - q, y - h, x + q, y - h)), line(seg(x - q, y + h, x + q, y + h)),
                          line(seg(x - h, y - q, x - h, y + q)), line(seg(x + h, y - q, x + h, y + q))]
            elif k % 2 == 0:
                parts.append(mark(bead(S, x, y, 2.7)))
            else:
                parts.append(mark(rect(x - 2.5, y - 2.5, 5, 5, L(S, 0.2, 1))))
            k += 1
    return parts


@icon("biography", CAT, "Closed book with a head and shoulders silhouette on its cover",
      tags=["biography", "life story", "memoir", "autobiography", "person profile", "history reading", "nonfiction"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 3))),
        detail(seg(7.5, 2.5, 7.5, 21.5)),
        mark(circle(13.8, 8.8, 2.3)),
        mark("M9.8 17V16.2Q9.8 12.8 13.8 12.8Q17.8 12.8 17.8 16.2V17Z"),
    ]


@icon("degree-levels", CAT, "Three rising steps with a mortarboard on the top step",
      tags=["degree levels", "academic levels", "qualifications", "education ladder", "bachelor master doctorate", "progression", "graduation"])
def _(S):
    steps = poly([(2.5, 21.5), (2.5, 17), (8.8, 17), (8.8, 13.5), (15.2, 13.5), (15.2, 10.5), (21.5, 10.5), (21.5, 21.5)], closed=True, r=S.r * 0.5)
    cx, top, w = 17.4, 2.2, 9
    h = w * 0.36
    board = poly([(cx - w / 2, top + h / 2), (cx, top), (cx + w / 2, top + h / 2), (cx, top + h)], closed=True, r=L(S, 0, 0.5))
    skull = poly([(cx - w * 0.25, top + h * 0.6), (cx + w * 0.25, top + h * 0.6), (cx + w * 0.25, top + h * 1.5), (cx - w * 0.25, top + h * 1.5)], closed=True)
    return [shell(steps), mark(union(board, skull))]


@icon("learning-styles", CAT, "Eye above an ear and an open hand, standing for seeing, hearing and doing",
      tags=["learning styles", "visual auditory kinesthetic", "vark", "multisensory", "eye ear hand", "teaching methods", "senses"])
def _(S):
    eye = "M2.8 7C6 2.6 18 2.6 21.2 7C18 11.4 6 11.4 2.8 7Z" if S.name == "line" else "M2.8 7C6.4 2.6 17.6 2.6 21.2 7C17.6 11.4 6.4 11.4 2.8 7Z"
    parts = [
        shell(eye), mark(circle(12, 7, 1.9)),
        line("M3.2 15.4a3.6 3.6 0 1 1 7.2 0c0 1.9-1.4 2.3-1.4 4.2c0 1.2-0.8 2-2 2c-1.2 0-2-0.8-2-2"),
        mark(circle(6.8, 15.2, 0.9)),
        mark(rect(14, 17.4, 7.6, 4.4, L(S, 0.6, 1.8))),
    ]
    for x, top in ((14.8, 13), (17.6, 12), (20.4, 13)):
        parts.append(mark(rect(x - 0.8, top, 1.6, 6, L(S, 0, 0.8))))
    parts.append(line(seg(14, 20, 12, 16.6)))
    return parts


@icon("leitner-box", CAT, "Open card box split into five slots with cards standing at different heights",
      tags=["leitner box", "flashcards", "spaced repetition", "card box", "revision system", "memorisation", "study cards"])
def _(S):
    parts = [shell(rect(2.5, 11, 19, 10.5, rr(S, 2.5)))]
    for x in (6.3, 10.1, 13.9, 17.7):
        parts.append(detail(seg(x, 11, x, 21.5)))
    heights = (3.5, 5.5, 7.5, 5, 2.5)
    xs = (4.5, 8.2, 12, 15.8, 19.5)
    for x, h in zip(xs, heights):
        parts.append(mark(rot(rect(x - 0.8, 11 - h, 1.6, h - 1.2, 0.2), 9, x, 10)))
    return parts


@icon("forgetting-curve", CAT, "Falling curve on axes that recovers after each review bump and flattens out",
      tags=["forgetting curve", "memory decay", "spaced repetition", "retention", "review schedule", "memory graph", "ebbinghaus"])
def _(S):
    curve = ("M5.6 3.6C6 10 7.6 13.4 10 15.2L10.3 10C11 12.2 12.6 14.4 15 15.2L15.3 12.6C16.6 14.4 18.6 15 21 15.2")
    return [
        line(poly([(3, 2.5), (3, 21), (21.5, 21)], r=S.r)),
        line(curve),
    ]


@icon("blooms-taxonomy", CAT, "Pyramid cut into stacked bands from the wide base to the tip",
      tags=["blooms taxonomy", "thinking skills", "learning levels", "remember understand apply", "pyramid", "cognitive levels", "lesson planning"])
def _(S):
    tri = poly([(12, 2.5), (21.5, 21.5), (2.5, 21.5)], closed=True, r=S.r * 0.6)
    parts = [shell(tri)]
    for y in (6.3, 9.4, 12.5, 15.6, 18.7):
        t = (y - 2.5) / 19
        parts.append(thin(seg(12 - 9.5 * t, y, 12 + 9.5 * t, y), S, 1.3))
    return parts
