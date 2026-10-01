"""TypeIcon Core: kids (batch kids_002).

Classic toys, puzzles, puppets, ride-ons, ball games and yard play, drawn from the objects themselves.
Side or front views; small parts sit inside clear silhouettes so they survive at 16 px.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, LINE as LINE_S, P, ST, U, fmt, path_to_d, rotation, transform_path  # noqa: F401

CAT = "kids"


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


def pt_on(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def wheel(x, y, r=2.6):
    return solid(circle(x, y, r))


def ring(cx, cy, ro, ri):
    return minus(circle(cx, cy, ro), circle(cx, cy, ri))


def band(cx, cy, ro, ri, a0, a1):
    p0, p1 = pt_on(cx, cy, ro, a0), pt_on(cx, cy, ro, a1)
    q1, q0 = pt_on(cx, cy, ri, a1), pt_on(cx, cy, ri, a0)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return (f"M{fmt(p0[0])} {fmt(p0[1])}A{fmt(ro)} {fmt(ro)} 0 {large} 1 {fmt(p1[0])} {fmt(p1[1])}"
            f"L{fmt(q1[0])} {fmt(q1[1])}A{fmt(ri)} {fmt(ri)} 0 {large} 0 {fmt(q0[0])} {fmt(q0[1])}Z")


def wave(x0, x1, y, amp, n):
    step = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        xa = x0 + i * step
        sgn = -1 if i % 2 == 0 else 1
        d += f"Q{fmt(xa + step / 2)} {fmt(y + sgn * amp * 2)} {fmt(xa + step)} {fmt(y)}"
    return d


def star(cx, cy, ro, ri, rnd=0.0):
    pts = []
    for i in range(10):
        ang = -90 + i * 36
        rad = ro if i % 2 == 0 else ri
        pts.append((cx + rad * math.cos(math.radians(ang)), cy + rad * math.sin(math.radians(ang))))
    return poly(pts, closed=True, r=rnd)


def fillet(d, r):
    """Round the concave corners of a closed region d by closing it with radius r."""
    big = rect(-6, -6, 36, 36)
    grown = union(d, path_to_d(ST(d, 2 * r, "round", "round")))
    comp = minus(big, grown)
    comp_grown = union(comp, path_to_d(ST(comp, 2 * r, "round", "round")))
    return minus(big, comp_grown)


def thick(d, w, S):
    return path_to_d(ST(d, w, S.cap, S.join))


# ============================================================================ chunk 1: classic toys

@icon("toy-piano", CAT, "Small upright toy piano with a row of keys and two short legs",
      tags=["toy piano", "mini piano", "keyboard toy", "music toy", "toddler", "instrument"])
def _(S):
    parts = [
        shell(rect(3, 3.5, 18, 12.5, rr(S, 2))),
        detail(seg(3, 9, 21, 9)),
    ]
    for x in (7.5, 12, 16.5):
        parts.append(detail(seg(x, 9, x, 16)))
    parts += [line(seg(6, 16, 6, 21)), line(seg(18, 16, 18, 21))]
    return parts


@icon("toy-phone", CAT, "Pull along toy telephone with a handset on top, a dial and two eyes",
      tags=["toy phone", "pull along phone", "telephone toy", "rotary phone", "toddler", "pretend play"])
def _(S):
    return [
        shell(rect(4, 9, 16, 9, rr(S, 2.5))),
        shell(poly([(5, 6.5), (5, 4.5), (19, 4.5), (19, 6.5)], r=S.r * 0.6)),
        detail(seg(8, 6.5, 8, 9)), detail(seg(16, 6.5, 16, 9)),
        mark(circle(8, 13.5, 1.1)), mark(circle(16, 13.5, 1.1)),
        detail(circle(12, 13.5, 2)),
        wheel(8, 20, 1.8), wheel(16, 20, 1.8),
    ]


@icon("pull-toy", CAT, "Wooden duck on a wheeled base with a pull string ending in a bead",
      tags=["pull toy", "pull along toy", "wooden duck", "toddler toy", "wheels", "string toy"])
def _(S):
    duck = union(ellipse(9, 12.5, 5.5, 3.5), circle(14, 8.5, 2.75))
    return [
        shell(duck),
        shell(poly([(16.5, 7.5), (19.5, 8.5), (16.5, 10)], closed=True, r=S.r * 0.4)),
        mark(circle(14, 8, 0.9)),
        line(seg(3, 17, 17, 17)),
        wheel(6, 19.5, 1.9), wheel(14, 19.5, 1.9),
        line("M17 17Q21 17 21 12.5"),
        dot(21, 10.5, 1.6),
    ]


@icon("wind-up-toy", CAT, "Small mouse figure on wheels with a large wind-up key on its back",
      tags=["wind-up toy", "windup toy", "clockwork toy", "tin toy", "mechanical toy", "key"])
def _(S):
    return [
        shell(poly([(3, 16.5), (6, 11), (11, 9.5), (18, 10.5), (20, 16.5)], closed=True, r=S.r + 1)),
        shell(circle(8.5, 7.5, 2.25)),
        mark(circle(6.5, 13.5, 0.9)),
        line(seg(15.5, 10.5, 15.5, 7.5)),
        solid(circle(13, 5, 2.25)), solid(circle(18, 5, 2.25)),
        line("M20 14.5Q22 14 22 11"),
        wheel(7.5, 19.5, 1.9), wheel(16, 19.5, 1.9),
    ]


@icon("clock-learning-toy", CAT, "Chunky teaching clock with big hands and number marks on a small stand",
      tags=["learning clock", "teaching clock", "toy clock", "telling time", "preschool", "educational"])
def _(S):
    return [
        shell(circle(12, 9.5, 7.5)),
        detail(seg(12, 9.5, 12, 5.5)), detail(seg(12, 9.5, 15, 12)),
        mark(circle(18.25, 9.5, 0.9)), mark(circle(12, 15.75, 0.9)), mark(circle(5.75, 9.5, 0.9)),
        line(seg(8.5, 16, 6.5, 21.5)), line(seg(15.5, 16, 17.5, 21.5)),
    ]


@icon("lacing-card", CAT, "Card with punched holes and a shoelace threaded through some of them",
      tags=["lacing card", "threading card", "shoelace toy", "fine motor", "preschool", "sewing card"])
def _(S):
    return [
        shell(rect(4, 3, 16, 18, rr(S, 2.5))),
        line(poly([(8, 7), (16, 12), (8, 17)], r=S.r * 0.6)),
        mark(circle(16, 7, 1.1)), mark(circle(16, 17, 1.1)), mark(circle(8, 12, 1.1)),
    ]


@icon("climbing-triangle", CAT, "Wooden A frame climbing triangle for toddlers with two rungs",
      tags=["climbing triangle", "pikler triangle", "a frame", "toddler climber", "indoor climbing", "play gym"])
def _(S):
    return [
        line(poly([(4, 21), (12, 3.5), (20, 21)], r=S.r * 0.6)),
        line(seg(8.1, 12.5, 15.9, 12.5)),
        line(seg(6, 17, 18, 17)),
    ]


@icon("spinning-top", CAT, "Spinning top balanced on its point with a knob and motion arcs",
      tags=["spinning top", "top", "dreidel", "whirl", "classic toy", "spin"])
def _(S):
    return [
        shell("M5.5 10.5A6.5 3.5 0 0 1 18.5 10.5L12 21Z"),
        detail(seg(7.3, 14, 16.7, 14)),
        line(seg(12, 7, 12, 3.5)),
        line(seg(9.5, 3.5, 14.5, 3.5)),
        line("M3.5 11Q2.5 13 3.5 15"),
        line("M20.5 11Q21.5 13 20.5 15"),
    ]


@icon("yo-yo", CAT, "Round yo-yo with a groove ring and axle, hanging from a string that ends in a finger loop",
      tags=["yo-yo", "yoyo", "string toy", "classic toy", "trick", "spinner"])
def _(S):
    loop = poly(regular(17.5, 5, 3, 4), closed=True) if S.name == "line" else circle(17.5, 5, 2.25)
    return [
        shell(circle(9, 15, 6)),
        detail(circle(9, 15, 2.8)),
        line(seg(13.2, 10.8, 15.8, 7.6)),
        shell(loop),
    ]


@icon("kite", CAT, "Diamond kite with a cross frame and a tail of small bows below",
      tags=["kite", "flying kite", "windy day", "outdoor toy", "spring", "sky"])
def _(S):
    return [
        shell(poly([(12, 2.5), (18, 8.5), (12, 15.5), (6, 8.5)], closed=True, r=S.r * 0.7)),
        detail(seg(12, 2.5, 12, 15.5)),
        detail(seg(6, 8.5, 18, 8.5)),
        line("M12 15.5Q8.5 17.5 12 19Q15 20.5 12.5 22"),
        dot(9.5, 18, 1.1), dot(14.5, 20, 1.1),
    ]


@icon("pinwheel", CAT, "Paper pinwheel with four curled vanes pinned to the top of a stick",
      tags=["pinwheel", "windmill toy", "paper windmill", "spinner", "breeze", "garden"])
def _(S):
    cx, cy, R = 12, 9, 6.5
    parts = []
    for k in range(4):
        pts = rot_pts([(cx, cy), (cx, cy - R), (cx + R, cy - R)], 90 * k, cx, cy)
        parts.append(shell(poly(pts, closed=True, r=S.r * 0.5)))
    parts.append(line(seg(12, 9, 12, 21.5)))
    return parts


@icon("toy-train", CAT, "Wooden toy engine with a chimney pulling one cart on round wheels",
      tags=["toy train", "wooden train", "train set", "locomotive", "engine", "railway toy"])
def _(S):
    return [
        shell(poly([(2, 17.5), (2, 12), (9, 12), (9, 7.5), (13.5, 7.5), (13.5, 17.5)], closed=True, r=S.r * 0.7)),
        shell(rect(3.5, 7.5, 3, 4.5, 0)),
        shell(rect(15.5, 11, 6.5, 6.5, rr(S, 1.5))),
        line(seg(13.5, 15, 15.5, 15)),
        wheel(5.5, 19, 1.9), wheel(10.5, 19, 1.9), wheel(19, 19, 1.9),
    ]


@icon("wooden-train-track", CAT, "Curved wooden track piece with two grooves and a round peg at one end",
      tags=["train track", "wooden track", "railway track", "curved track", "toy railway", "track piece"])
def _(S):
    cx, cy = 12, 35.5
    peg = rot(rect(19, 12.3, 3.4, 3.4, 0), 16, 20.7, 14) if S.name == "line" else circle(20.6, 14, 1.9)
    return [
        shell(band(cx, cy, 29, 17, -106, -74)),
        detail(arc(cx, cy, 21, -106, -74)),
        detail(arc(cx, cy, 25, -106, -74)),
        shell(peg),
        mark(circle(7, 13.9, 1.2)),
    ]


@icon("toy-car", CAT, "Chunky toy car with a rounded cabin and oversized wheels, side view",
      tags=["toy car", "model car", "small car", "miniature car", "vehicle toy", "diecast"])
def _(S):
    return [
        shell(poly([(2, 17), (2, 13), (6, 12), (9, 7), (15.5, 7), (18, 12), (22, 13), (22, 17)], closed=True, r=S.r)),
        detail(seg(12.5, 7, 12.5, 12)),
        wheel(7, 18, 2.9), wheel(17, 18, 2.9),
    ]


# ============================================================================ chunk 2: toys, games, puzzles

@icon("toy-truck", CAT, "Toy dump truck with a tipped bed and oversized wheels, side view",
      tags=["toy truck", "dump truck", "tipper", "tonka style", "sandbox toy", "vehicle toy"])
def _(S):
    bed = rot_pts([(2.5, 8.5), (13, 8.5), (13, 15), (2.5, 15)], 14, 13, 15)
    return [
        shell(poly(bed, closed=True, r=S.r * 0.6)),
        shell(poly([(14.5, 18), (14.5, 9.5), (18.5, 9.5), (21.5, 13.5), (21.5, 18)], closed=True, r=S.r)),
        mark(rect(16.25, 11, 2.25, 3, 0)),
        line(seg(3, 18, 14.5, 18)),
        wheel(6.5, 19, 2.8), wheel(17.5, 19, 2.8),
    ]


@icon("toy-airplane", CAT, "Small propeller plane seen from above with a round nose, straight wings and a tail",
      tags=["toy airplane", "toy plane", "propeller plane", "balsa glider", "aeroplane", "flying toy"])
def _(S):
    body = union(rect(10, 4.5, 4, 16.5, rr(S, 2)), rect(2.5, 9.5, 19, 4.5, rr(S, 1.5)), rect(6.5, 17, 11, 3.5, rr(S, 1.5)))
    return [
        shell(body),
        line(seg(8, 3, 16, 3)),
    ]


@icon("rc-car", CAT, "Buggy with big wheels next to a handheld remote control with an antenna",
      tags=["rc car", "remote control car", "radio controlled", "buggy", "toy car", "controller"])
def _(S):
    return [
        shell(poly([(2, 17), (2, 13), (5.5, 12.5), (8, 9), (11, 9), (12, 17)], closed=True, r=S.r * 0.8)),
        wheel(5, 18.5, 2.7), wheel(11, 18.5, 2.7),
        shell(rect(15.5, 11.5, 6, 10, rr(S, 2))),
        mark(circle(18.5, 15, 1.2)),
        line(seg(20, 11.5, 20, 5)),
        line("M16.5 6.5Q16.5 3.5 19 3"),
    ]


@icon("hobby-horse", CAT, "Horse head on a long stick with a small wheel at the bottom",
      tags=["hobby horse", "stick horse", "horse on a stick", "pretend riding", "cowboy", "toy horse"])
def _(S):
    return [
        shell(poly([(3, 9.5), (4.5, 6.5), (8, 4), (10.5, 2.5), (12, 4.5), (16, 5.5), (17.5, 10), (15.5, 14), (11.5, 14), (9.5, 11.5), (5, 12)],
                   closed=True, r=S.r)),
        mark(circle(9.5, 7.5, 0.9)),
        line(seg(14, 14, 14, 20)),
        wheel(14, 20, 1.9),
    ]


@icon("marbles", CAT, "Three glass balls with a swirl inside each, one larger shooter marble",
      tags=["marbles", "glass marbles", "shooter", "taw", "classic toy", "playground game"])
def _(S):
    def hi(cx, cy, r):
        if S.name == "line":
            return detail(arc(cx, cy, r, 200, 320))
        return mark(circle(cx - r * 0.5, cy - r * 0.5, 0.9))
    return [
        shell(circle(8, 8, 5)), hi(8, 8, 2.2),
        shell(circle(18.5, 6.5, 3.5)), hi(18.5, 6.5, 1.2),
        shell(circle(13, 17.5, 3.5)), hi(13, 17.5, 1.2),
    ]


@icon("jacks", CAT, "Two six pronged metal jacks beside a small bouncing ball",
      tags=["jacks", "knucklebones", "jackstones", "classic game", "ball and jacks", "playground game"])
def _(S):
    def jack(cx, cy, r):
        out = []
        for a in (90, 30, 150):
            (x1, y1), (x2, y2) = pt_on(cx, cy, r, a), pt_on(cx, cy, r, a + 180)
            out.append(line(seg(x1, y1, x2, y2)))
        for a in (90, 30, 150, 270, 330, 210):
            x, y = pt_on(cx, cy, r, a)
            out.append(dot(x, y, 1.4) if S.name == "rounded" else solid(poly(regular(x, y, 1.9, 4, start=a + 45), closed=True)))
        return out
    return jack(7.5, 8, 5) + jack(14, 17, 4.6) + [shell(circle(19.5, 6.5, 2.5))]


@icon("pick-up-sticks", CAT, "Pile of thin sticks scattered across each other in a loose heap",
      tags=["pick up sticks", "pick-up sticks", "spillikins", "mikado", "jackstraws", "stick game"])
def _(S):
    return [
        line(seg(2.5, 18, 19.5, 8)),
        line(seg(5, 4.5, 21.5, 15)),
        line(seg(3, 11, 15.5, 21.5)),
        line(seg(11, 3, 21.5, 7)),
        line(seg(8, 21.5, 21.5, 20.5)),
    ]


@icon("cup-and-ball", CAT, "Wooden handle with a cup on top and a ball on a string swinging beside it",
      tags=["cup and ball", "ball in a cup", "bilboquet", "kendama style", "skill toy", "wooden toy"])
def _(S):
    return [
        shell(union(poly([(3, 3.5), (13, 3.5), (11, 9), (5, 9)], closed=True, r=0),
                    poly([(6.5, 9), (9.5, 9), (10.5, 21), (5.5, 21)], closed=True, r=0))),
        line("M13 5Q20 4 19 12"),
        shell(circle(19, 15.5, 3)),
    ]


@icon("paddle-ball", CAT, "Flat wooden paddle with a ball attached by an elastic string",
      tags=["paddle ball", "bat and ball toy", "rubber band ball", "paddle toy", "bouncing ball", "skill toy"])
def _(S):
    return [
        shell(union(circle(9, 8.5, 6), rect(7.25, 13, 3.5, 8.5, rr(S, 1.5)))),
        line("M14.5 9Q20 9 19 16"),
        shell(circle(19, 18.5, 2.5)),
    ]


@icon("diabolo", CAT, "Hourglass shaped spool balanced on a string stretched between two hand sticks",
      tags=["diabolo", "juggling", "circus toy", "spool", "string trick", "hand sticks"])
def _(S):
    return [
        shell(poly([(4, 3), (10.5, 7), (13.5, 7), (20, 3), (20, 12.5), (13.5, 9), (10.5, 9), (4, 12.5)], closed=True, r=S.r * 0.7)),
        line(poly([(6, 15), (12, 10.5), (18, 15)], r=S.r * 0.6)),
        line(seg(6, 15, 2.5, 21.5)), line(seg(18, 15, 21.5, 21.5)),
    ]


@icon("conkers", CAT, "Chestnut threaded on a knotted string, swinging",
      tags=["conkers", "conker", "horse chestnut", "autumn game", "string game", "schoolyard"])
def _(S):
    return [
        line(seg(12, 10, 12, 5)),
        dot(12, 3.8, 1.6),
        shell(circle(12, 15.5, 5.5)),
        mark(ellipse(12, 13, 2.2, 1.1)),
        line("M3.5 12Q2.5 16 4.5 19.5"),
        line("M20.5 12Q21.5 16 19.5 19.5"),
    ]


@icon("puzzle-cube", CAT, "Cube with a grid on each visible face like a twisting puzzle",
      tags=["puzzle cube", "twisty cube", "speed cube", "cube puzzle", "brain teaser", "rubik style"])
def _(S):
    cx, cy, R = 12, 12, 9.5
    v = {a: pt_on(cx, cy, R, a) for a in (270, 330, 30, 90, 150, 210)}
    c = (cx, cy)

    def mid(a, b):
        return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)

    def face(p0, p1, p2, p3):
        # quad p0 p1 p2 p3 in order; two mid lines
        a, b, cc, d = mid(p0, p1), mid(p2, p3), mid(p1, p2), mid(p3, p0)
        return [detail(seg(*a, *b)), detail(seg(*cc, *d))]
    parts = [shell(poly(list(v.values()), closed=True, r=S.r * 0.6))]
    parts += [detail(seg(*c, *v[210])), detail(seg(*c, *v[330])), detail(seg(*c, *v[90]))]
    parts += face(v[270], v[330], c, v[210]) + face(c, v[330], v[30], v[90]) + face(v[210], c, v[90], v[150])
    return parts


@icon("sliding-puzzle", CAT, "Square frame of small tiles with one empty slot",
      tags=["sliding puzzle", "tile puzzle", "15 puzzle", "slide puzzle", "brain teaser", "number puzzle"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 2.5)))]
    for r in range(3):
        for c in range(3):
            if (r, c) == (2, 2):
                continue
            parts.append(mark(rect(5.2 + c * 5.2, 5.2 + r * 5.2, 3.6, 3.6, L(S, 0, 0.8))))
    return parts


# ============================================================================ chunk 3: puzzles, games, play objects

@icon("wire-puzzle", CAT, "Two bent wire loops tangled together, each passing over and under the other",
      tags=["wire puzzle", "ring puzzle", "tangled rings", "disentanglement puzzle", "brain teaser", "metal puzzle"])
def _(S):
    k = S.r * 1.3
    return [
        line(poly([(11.8, 14.5), (14.5, 14.5), (14.5, 3.5), (3.5, 3.5), (3.5, 14.5), (7.2, 14.5)], r=k)),
        line(poly([(16.8, 9.5), (20.5, 9.5), (20.5, 20.5), (9.5, 20.5), (9.5, 9.5), (12.2, 9.5)], r=k)),
    ]


@icon("tangram", CAT, "Square cut into seven geometric pieces: large, medium and small triangles, a square and a parallelogram",
      tags=["tangram", "seven pieces", "chinese puzzle", "shape puzzle", "dissection puzzle", "geometry"])
def _(S):
    def g(x, y):
        return 3 + x * 4.5, 3 + y * 4.5
    segs = [((4, 0), (0, 4)), ((0, 0), (2, 2)), ((2, 4), (4, 2)), ((1, 3), (2, 4)), ((2, 2), (3, 3)), ((3, 1), (4, 2))]
    return [shell(rect(3, 3, 18, 18, rr(S, 2)))] + [detail(seg(*g(*a), *g(*b))) for a, b in segs]


@icon("maze-puzzle", CAT, "Square maze with an entry gap at the top and a dot at the exit in the middle",
      tags=["maze", "labyrinth", "maze puzzle", "find the way", "path puzzle", "brain teaser"])
def _(S):
    return [
        line(poly([(9, 3), (3, 3), (3, 21), (21, 21), (21, 3), (15, 3)], r=S.r * 0.6)),
        line(poly([(8, 16), (8, 8), (16, 8), (16, 16)], r=S.r * 0.6)),
        dot(12, 13, 1.6),
    ]


@icon("spot-the-difference", CAT, "Two small side by side pictures with a circle marking the one detail that differs",
      tags=["spot the difference", "find the difference", "picture puzzle", "compare pictures", "observation game", "kids puzzle"])
def _(S):
    rc = L(S, 0.5, 2.5)
    return [
        shell(rect(1.5, 5, 9.5, 14, rc)),
        shell(rect(13, 5, 9.5, 14, rc)),
        mark(circle(6.25, 9.5, 1.4)),
        mark(rect(4, 14.5, 4.5, 1.5, 0)), mark(rect(15.5, 14.5, 4.5, 1.5, 0)),
        detail(circle(17.75, 9.5, 2)),
    ]


@icon("paint-by-number", CAT, "Canvas split into small areas marked with numbers beside a paint brush",
      tags=["paint by number", "paint by numbers", "colour by number", "numbered painting", "art kit", "craft"])
def _(S):
    return [
        shell(rect(2.5, 6, 11.5, 15, rr(S, 2))),
        detail(seg(2.5, 13, 14, 13)),
        detail(seg(8, 13, 8, 21)),
        mark(circle(8, 9.5, 1)), mark(circle(5.2, 17.2, 1)), mark(circle(10.8, 17.2, 1)),
        line(seg(21.5, 3, 17.5, 8.5)),
        shell(poly([(16.5, 8), (19, 10), (16.3, 14.5), (15, 12.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("tumble-tower", CAT, "Tower of stacked wooden blocks in crossed layers with one block pulled out to the side",
      tags=["tumble tower", "jenga style", "block tower", "stacking game", "wooden blocks", "party game"])
def _(S):
    rc = L(S, 0.5, 2.5)
    parts = [shell(rect(3, 3, 11, 18, rc))]
    for y in (7.5, 12, 16.5):
        parts.append(detail(seg(3, y, 14, y)))
    for y0 in (3, 12):
        parts.append(detail(seg(8.5, y0, 8.5, y0 + 4.5)))
    parts.append(shell(rect(17.5, 8, 4.5, 3.5, L(S, 0, 1.2))))
    parts.append(line(seg(14, 9.75, 17.5, 9.75)))
    return parts


@icon("memory-game", CAT, "Grid of cards with two turned face up showing matching shapes and two face down",
      tags=["memory game", "matching game", "concentration", "pairs", "card game", "match the pairs"])
def _(S):
    d = poly(regular(0, 0, 1.9, 4, start=-90), closed=True)
    rc = L(S, 0.5, 2.5)

    def sym(cx, cy):
        return mark(path_to_d(transform_path(P(d), (1, 0, 0, 1, cx, cy))))
    return [
        shell(rect(3, 3, 7.5, 7.5, rc)), sym(6.75, 6.75),
        solid(rect(13.5, 3, 7.5, 7.5, rc)),
        solid(rect(3, 13.5, 7.5, 7.5, rc)),
        shell(rect(13.5, 13.5, 7.5, 7.5, rc)), sym(17.25, 17.25),
    ]


@icon("magnetic-fishing-game", CAT, "Toy rod whose line ends in a magnet lifting a flat fish by its metal ring",
      tags=["magnetic fishing", "fishing game", "toy fishing rod", "magnet game", "fish toy", "pond game"])
def _(S):
    fish = union(ellipse(11.5, 18.5, 5.5, 3), poly([(15.5, 18.5), (21, 15.5), (21, 21.5)], closed=True, r=0))
    return [
        line(seg(22, 2.5, 12, 4.5)),
        line(seg(12, 4.5, 12, 6.5)),
        line("M9.5 11V9.5A2.5 2.5 0 0 1 14.5 9.5V11"),
        shell(circle(12, 13.2, 1.5)),
        shell(fish),
        mark(circle(8.5, 17.8, 0.8)),
    ]


@icon("snakes-and-ladders", CAT, "Square game board with a leaning ladder on one side and a wavy snake sliding down the other",
      tags=["snakes and ladders", "chutes and ladders", "board game", "ladder", "snake", "family game"])
def _(S):
    rc = L(S, 0.5, 2.5)
    return [
        shell(rect(3, 3, 18, 18, rc)),
        detail(seg(5.5, 21, 9, 3)), detail(seg(10.7, 21, 14.2, 3)),
        detail(seg(7.2, 17, 12.4, 17)), detail(seg(7.9, 12.5, 13.1, 12.5)), detail(seg(8.6, 8, 13.8, 8)),
        mark(circle(18, 5.5, 1.3)),
        detail("M18 6.5Q15.8 10 18 13.5T18 19"),
    ]


@icon("spring-toy", CAT, "Coil spring toy arched like a rainbow walking down a step",
      tags=["slinky style", "spring toy", "coil toy", "walking spring", "stairs toy", "rainbow spring"])
def _(S):
    cx, cy = 13, 16
    ang = 25
    parts = [shell(rot(band(cx, cy, 8, 4, 180, 360), ang, cx, cy))]
    for a in (225, 270, 315):
        p0, p1 = pt_on(cx, cy, 4, a), pt_on(cx, cy, 8, a)
        (x0, y0), (x1, y1) = rot_pts([p0, p1], ang, cx, cy)
        parts.append(detail(seg(x0, y0, x1, y1)))
    parts.append(line(poly([(2.5, 15.5), (7.5, 15.5), (7.5, 21.5), (22, 21.5)], r=S.r * 0.5)))
    return parts


@icon("kaleidoscope", CAT, "Tube with a small eye cap on one end and a star pattern bursting from the other",
      tags=["kaleidoscope", "pattern tube", "toy telescope", "colourful patterns", "optical toy", "mirror tube"])
def _(S):
    return [
        shell(rect(8.5, 8, 9.5, 8, rr(S, 2))),
        detail(seg(12.5, 8, 12.5, 16)),
        shell(rect(18, 10, 3.5, 4, 0)),
        solid(star(4.2, 12, 3.4, 1.4, S.r * 0.2)),
    ]


@icon("zoetrope", CAT, "Open drum with vertical slits around its side on a spindle base",
      tags=["zoetrope", "animation toy", "wheel of life", "spinning drum", "optical toy", "early animation"])
def _(S):
    drum = union(ellipse(12, 7, 8, 2.5), rect(4, 7, 16, 8, 0), ellipse(12, 15, 8, 2.5))
    parts = [shell(drum), detail(ellipse(12, 7, 5, 0.9))]
    for x in (7, 10.2, 13.8, 17):
        parts.append(detail(seg(x, 9.5, x, 14)))
    parts += [line(seg(12, 17.5, 12, 19.5)), shell(rect(6.5, 19.5, 11, 2, rr(S, 1)))]
    return parts


@icon("tin-can-phone", CAT, "Two tin cans joined by a taut string stretched between them",
      tags=["tin can phone", "string telephone", "can telephone", "cup phone", "walkie talkie toy", "science toy"])
def _(S):
    rc = L(S, 0.5, 2.5)
    return [
        shell(rect(2.5, 3, 6.5, 9, rc)), detail(seg(2.5, 6.25, 9, 6.25)),
        shell(rect(15, 12, 6.5, 9, rc)), detail(seg(15, 15.25, 21.5, 15.25)),
        line(seg(9, 8, 15, 16)),
    ]


@icon("magnetic-drawing-board", CAT, "Portrait drawing board with a screen, a slide bar for erasing and a pen hanging on a cord",
      tags=["magnetic drawing board", "magna doodle", "doodle board", "erasable board", "drawing toy", "sketch pad"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 15, 19, L(S, 1, 3))),
        detail(rect(5, 5, 10, 9.5, L(S, 0, 1))),
        detail(seg(5, 18, 9.5, 18)),
        mark(rect(10.5, 17, 3.5, 2.2, 0)),
        line(seg(21, 4, 21, 10.5)),
        line("M17.5 17.5Q21 17.5 21 11.5"),
    ]


# ============================================================================ chunk 4: fidgets, puppets, water toys

@icon("fidget-spinner", CAT, "Three lobed hand spinner with a round bearing in the hub and a round weight in each lobe",
      tags=["fidget spinner", "hand spinner", "spinner", "stress toy", "bearing", "fidget toy"])
def _(S):
    cx, cy, d = 12, 12, 6.3
    lobes = [pt_on(cx, cy, d, a) for a in (-90, 30, 150)]
    parts_d = [circle(cx, cy, 4.3)] + [circle(x, y, 3.7) for x, y in lobes]
    parts_d += [path_to_d(ST(seg(cx, cy, x, y), 4.6, "butt", "miter")) for x, y in lobes]
    body = union(*parts_d)
    if S.name == "rounded":
        body = fillet(body, 1.6)
    return [shell(body), mark(circle(cx, cy, 1.9))] + [mark(circle(x, y, 1.2)) for x, y in lobes]


@icon("pop-fidget", CAT, "Flat tray of round push bubbles in a grid, some popped in and some still raised",
      tags=["pop it", "push pop", "bubble fidget", "popping toy", "sensory toy", "fidget toy"])
def _(S):
    parts = [shell(rect(2.5, 2.5, 19, 19, L(S, 1, 4)))]
    pressed = {(0, 2), (1, 1), (2, 0)}
    for r in range(3):
        for c in range(3):
            x, y = 7.5 + c * 4.5, 7.5 + r * 4.5
            if (r, c) in pressed:
                parts.append(mark(ring(x, y, 1.7, 0.8)))
            else:
                parts.append(mark(circle(x, y, 1.6)))
    return parts


@icon("slime", CAT, "Open tub with gooey slime piled above the rim and dripping down its side",
      tags=["slime", "goo", "gooey", "ooze", "putty", "sensory toy"])
def _(S):
    tub = poly([(3.5, 11.5), (20.5, 11.5), (19, 21.5), (5, 21.5)], closed=True, r=S.r)
    mound = ellipse(12, 8.5, 7, 4.5)
    return [
        shell(union(tub, mound)),
        detail("M7.5 11.5V15Q7.5 17 9.5 17Q11.5 17 11.5 15V11.5"),
        detail("M15 11.5V17.5Q15 19.5 17 19.5"),
    ]


@icon("play-dough", CAT, "Round tub overflowing with a lumpy mound of dough and a small star shaped cutter beside it",
      tags=["play dough", "playdough", "modelling clay", "clay", "dough tub", "sculpting"])
def _(S):
    tub = rect(2.5, 12.5, 12.5, 9, L(S, 1, 3))
    lumps = union(circle(6, 9.5, 3.4), circle(10.5, 8, 4), circle(13, 11, 2.6))
    return [
        shell(union(tub, lumps)),
        detail(seg(3, 15.5, 14.5, 15.5)),
        shell(star(18.5, 11, 3.6, 1.7, S.r * 0.3)),
        line(seg(18.5, 14.8, 18.5, 21)),
    ]


@icon("hand-puppet", CAT, "Glove puppet with a round face, stubby arms and a skirt that covers the wrist",
      tags=["hand puppet", "glove puppet", "puppet", "storytelling", "puppet show", "toy"])
def _(S):
    body = union(circle(12, 7.5, 4.8),
                 poly([(8, 12.5), (16, 12.5), (19, 21.5), (5, 21.5)], closed=True, r=S.r),
                 path_to_d(ST(seg(8.5, 15, 3.8, 11), 3, "round", "round")),
                 path_to_d(ST(seg(15.5, 15, 20.2, 11), 3, "round", "round")))
    return [
        shell(body),
        mark(circle(10, 6.5, 0.9)), mark(circle(14, 6.5, 0.9)),
        detail("M10 9.2Q12 11 14 9.2"),
    ]


@icon("finger-puppet", CAT, "Small bear head puppet sitting on a raised finger",
      tags=["finger puppet", "finger toy", "puppet", "bear puppet", "storytelling", "toy"])
def _(S):
    head = union(circle(12, 8.5, 5), circle(7, 4.2, 2.3), circle(17, 4.2, 2.3))
    return [
        shell(union(head, rect(8.5, 12.5, 7, 9, rr(S, 2)))),
        detail(seg(8.5, 17, 15.5, 17)),
        mark(circle(10, 8, 0.9)), mark(circle(14, 8, 0.9)), mark(circle(12, 10.5, 1)),
    ]


@icon("sock-puppet", CAT, "Sock on a forearm with button eyes and a mouth opened by the hand inside",
      tags=["sock puppet", "puppet", "diy puppet", "craft", "storytelling", "kids craft"])
def _(S):
    return [
        shell(poly([(9, 21.5), (9, 11.5), (3, 11.5), (3, 5), (8, 3), (19, 3), (19, 21.5)], closed=True, r=S.r + 1)),
        mark(circle(10.5, 6.5, 1.2)), mark(circle(15.5, 6.5, 1.2)),
        detail(seg(3, 8.5, 10, 8.5)),
        detail(seg(9, 18, 19, 18)),
    ]


@icon("marionette", CAT, "Figure hanging from strings attached to a crossbar control",
      tags=["marionette", "string puppet", "puppet on strings", "puppeteer", "puppet show", "theatre"])
def _(S):
    return [
        line(seg(4, 3, 20, 3)),
        line(seg(12, 3, 12, 6.2)),
        line(seg(4.5, 3, 6.8, 13.3)), line(seg(19.5, 3, 17.2, 13.3)),
        shell(circle(12, 8.5, 2.3)),
        line(poly([(6.8, 14), (12, 11.3), (17.2, 14)], r=S.r * 0.6)),
        line(seg(12, 11.3, 12, 16)),
        line(poly([(8.5, 21.5), (12, 16), (15.5, 21.5)], r=S.r * 0.6)),
    ]


@icon("puppet-theater", CAT, "Small stage booth with an open window and a puppet peeking out of it",
      tags=["puppet theater", "puppet theatre", "puppet stage", "puppet booth", "puppet show", "punch and judy style"])
def _(S):
    booth = poly([(3, 4), (21, 4), (21, 21.5), (16.5, 21.5), (16.5, 9.5), (7.5, 9.5), (7.5, 21.5), (3, 21.5)], closed=True, r=S.r * 0.6)
    return [
        shell(booth),
        mark(circle(12, 14.3, 2.1)),
        mark("M8.7 21.5Q8.7 17.8 12 17.8Q15.3 17.8 15.3 21.5Z"),
    ]


@icon("play-kitchen", CAT, "Toy kitchen unit with two burner rings on top, an oven door and a tap",
      tags=["play kitchen", "toy kitchen", "pretend cooking", "toy oven", "role play", "kitchenette"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, L(S, 1, 3))),
        detail(seg(3, 10.5, 21, 10.5)),
        mark(ring(7.5, 6.8, 2.2, 1)), mark(ring(16.5, 6.8, 2.2, 1)),
        mark(rect(11, 5, 2, 3.2, 0)),
        detail(rect(6, 13.5, 12, 5.5, L(S, 0, 1))),
        mark(rect(8.5, 15, 7, 1.3, 0)),
    ]


@icon("water-balloon", CAT, "Round water filled balloon with a knot and drops splashing out of it",
      tags=["water balloon", "water bomb", "balloon fight", "summer game", "splash", "party"])
def _(S):
    body = union(ellipse(12, 10, 6.5, 7), poly([(12, 16.5), (10, 20), (14, 20)], closed=True, r=S.r * 0.6))
    return [
        shell(body),
        detail(arc(12, 10, 3.6, 200, 260)) if S.name == "line" else mark(circle(9.7, 7.5, 1)),
        dot(3.5, 5, 1.2), dot(20.5, 6, 1.2), dot(20, 16.5, 1.2), dot(4.5, 15, 1.2),
    ]


@icon("stomp-rocket", CAT, "Foot pad joined by a hose to a small foam rocket sitting on a launch tube",
      tags=["stomp rocket", "air rocket", "foam rocket", "launcher", "outdoor toy", "foot pump"])
def _(S):
    return [
        shell(poly([(15, 12), (15, 6.5), (17.5, 2.5), (20, 6.5), (20, 12)], closed=True, r=S.r * 0.6)),
        line(seg(15, 11, 13, 14)), line(seg(20, 11, 22, 14)),
        line(seg(17.5, 12, 17.5, 16)),
        line("M10.5 19.5Q17.5 19.5 17.5 16"),
        shell(rect(2, 16.5, 9, 5, L(S, 1, 2.5))),
    ]


# ============================================================================ chunk 5: balls, outdoor games, ride-ons

@icon("beach-ball", CAT, "Beach ball seen from the top with curved panels spiralling out from a round cap",
      tags=["beach ball", "inflatable ball", "pool ball", "summer", "seaside", "beach toy"])
def _(S):
    cx, cy = 12, 12
    cap = poly(regular(cx, cy, 2.9, 4, start=0), closed=True) if S.name == "line" else circle(cx, cy, 2.3)
    parts = [shell(circle(cx, cy, 9)), shell(cap)]
    for k in range(6):
        a = -90 + 60 * k
        sx, sy = pt_on(cx, cy, 3, a)
        ex, ey = pt_on(cx, cy, 9, a + 50)
        qx, qy = pt_on(cx, cy, 7, a - 5)
        parts.append(detail(f"M{fmt(sx)} {fmt(sy)}Q{fmt(qx)} {fmt(qy)} {fmt(ex)} {fmt(ey)}"))
    return parts


@icon("bouncy-ball", CAT, "Small ball with arcs showing its bounces and a ground line below",
      tags=["bouncy ball", "rubber ball", "super ball", "bounce", "playground", "toy ball"])
def _(S):
    return [
        shell(circle(17.5, 7.5, 3.8)),
        line("M2.5 20Q5.5 10 8.5 20"),
        line("M8.5 20Q11.5 12 14 13"),
        line(seg(2, 21.5, 22, 21.5)),
        mark(circle(16.5, 6.5, 0.8)),
    ]


@icon("pogo-stick", CAT, "Upright pogo stick with handlebars, foot pegs and a coiled spring near the bottom",
      tags=["pogo stick", "pogo", "bouncing toy", "jumping", "spring", "outdoor toy"])
def _(S):
    return [
        line(seg(4.5, 2.5, 19.5, 2.5)),
        line(seg(12, 2.5, 12, 10)),
        line(seg(5, 7.5, 19, 7.5)),
        line(poly([(12, 10), (7, 12.3), (17, 15.7), (7, 19), (12, 20.2)], r=S.r * 0.6)),
        line(seg(12, 20.2, 12, 22)),
    ]


@icon("space-hopper", CAT, "Big rubber hopper ball with two horn handles and a smiling face",
      tags=["space hopper", "hopper ball", "hippity hop", "bouncy ball", "ride on ball", "retro toy"])
def _(S):
    ears = [poly(regular(x, 6.8, 2.7, 4, start=0), closed=True) if S.name == "line" else circle(x, 6.8, 2.2) for x in (6.3, 17.7)]
    return [
        shell(union(circle(12, 14, 7.8), *ears)),
        mark(circle(9.3, 12.5, 1)), mark(circle(14.7, 12.5, 1)),
        detail(arc(12, 14, 3.8, 30, 150)),
    ]


@icon("flying-disc", CAT, "Tilted flying disc with a rim lip and speed lines behind it",
      tags=["flying disc", "frisbee style", "throwing disc", "disc golf", "ultimate", "beach game"])
def _(S):
    cx, cy = 14, 12.5
    disc = union(ellipse(cx, cy - 1, 8, 3.6), ellipse(cx, cy + 1.2, 8, 3.6))
    dish = ellipse(cx, cy - 1, 4.6, 1.5)
    return [
        shell(rot(disc, -16, cx, cy)),
        detail(rot(dish, -16, cx, cy)),
        line(seg(2.5, 14, 6, 13)), line(seg(2.5, 18, 8, 16.5)),
    ]


@icon("bubble-wand", CAT, "Bubble wand with a ring end and several bubbles floating away",
      tags=["bubble wand", "bubbles", "soap bubbles", "bubble blower", "party", "outdoor play"])
def _(S):
    return [
        shell(circle(8, 8, 3.8)),
        line(seg(8, 11.8, 8, 21.5)),
        shell(circle(17, 5.5, 2.2)),
        shell(circle(18.5, 13, 3)),
        shell(circle(13.5, 18.5, 1.9)),
    ]


@icon("sidewalk-chalk", CAT, "Thick stick of chalk drawing a wavy line with a few dust dots at its tip",
      tags=["sidewalk chalk", "chalk", "pavement chalk", "drawing", "hopscotch", "outdoor art"])
def _(S):
    pts = rot_pts([(9.5, 1.5), (14.5, 1.5), (14.5, 14), (9.5, 14)], 35, 12, 9)
    return [
        shell(poly(pts, closed=True, r=S.r * 0.5)),
        line("M2.5 21Q5.5 18 8.5 20.5T14.5 20"),
        dot(14.2, 16.2, 1), dot(17.3, 18.4, 1), dot(18.8, 14.8, 1),
    ]


@icon("hopscotch", CAT, "Hopscotch court of single and double squares chalked in a column",
      tags=["hopscotch", "hop scotch", "chalk game", "playground game", "jumping game", "squares"])
def _(S):
    rows = [(16.5, 21, False), (12, 16.5, True), (7.5, 12, False), (3, 7.5, True)]
    rects = []
    for y0, y1, dbl in rows:
        x0, x1 = (7, 17) if dbl else (9.5, 14.5)
        rects.append(rect(x0, y0, x1 - x0, y1 - y0, 0))
    parts = [shell(poly([(9.5, 21), (9.5, 16.5), (7, 16.5), (7, 12), (9.5, 12), (9.5, 7.5), (7, 7.5), (7, 3), (17, 3), (17, 7.5),
                         (14.5, 7.5), (14.5, 12), (17, 12), (17, 16.5), (14.5, 16.5), (14.5, 21)], closed=True, r=S.r * 0.4))]
    for y in (7.5, 12, 16.5):
        parts.append(detail(seg(7, y, 17, y)))
    parts.append(detail(seg(12, 3, 12, 7.5)))
    parts.append(detail(seg(12, 12, 12, 16.5)))
    return parts


@icon("tee-ball", CAT, "Ball resting on a batting tee with a small bat standing beside it",
      tags=["tee ball", "t-ball", "batting tee", "baseball for kids", "bat and ball", "little league"])
def _(S):
    return [
        shell(circle(8, 7.5, 3.6)),
        line(poly([(5.2, 12.8), (6.8, 14), (9.2, 14), (10.8, 12.8)], r=S.r * 0.5)),
        line(seg(8, 14, 8, 21.5)),
        line(seg(4, 21.5, 12, 21.5)),
        shell(poly([(17.2, 21.5), (19.2, 21.5), (19.4, 14), (21.2, 11.5), (21.2, 4.5), (15.4, 4.5), (15.4, 11.5), (17, 14)], closed=True, r=S.r * 0.4)),
    ]


@icon("four-square", CAT, "Court divided into four squares with a ball sitting in one of them",
      tags=["four square", "foursquare", "playground game", "bouncing ball game", "recess", "ball game"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, L(S, 0.5, 3))),
        detail(seg(12, 3, 12, 21)), detail(seg(3, 12, 21, 12)),
        mark(circle(7.5, 7.5, 2.2)),
    ]


@icon("tetherball", CAT, "Tall pole with a ball hanging from a rope at the top",
      tags=["tetherball", "tether ball", "swing ball", "playground game", "pole and ball", "recess"])
def _(S):
    return [
        line(seg(7, 3, 7, 21.5)),
        line(seg(4, 21.5, 10, 21.5)),
        line("M7 3Q16.5 3 16.5 9"),
        shell(circle(16.5, 12.8, 3.8)),
        detail(arc(16.5, 12.8, 1.5, 200, 330)) if False else mark(circle(15.5, 11.8, 0.8)),
    ]


@icon("sled", CAT, "Wooden sled with curled runners and a pull rope",
      tags=["sled", "sledge", "toboggan", "snow", "winter", "sledding"])
def _(S):
    return [
        shell(rect(6.5, 8.5, 15, 3.5, L(S, 0.5, 1.75))),
        line(seg(9.5, 12, 9.5, 17.5)), line(seg(18.5, 12, 18.5, 17.5)),
        line("M4 12C4 16 5.5 17.5 8 17.5H21.5"),
        line("M4 12Q3 7.5 7 4.5"),
        dot(7.8, 4, 1.2),
    ]


@icon("tricycle", CAT, "Child tricycle with one large front wheel with pedals and two small rear wheels",
      tags=["tricycle", "trike", "toddler bike", "three wheeler", "ride on", "kids bike"])
def _(S):
    return [
        shell(circle(6.5, 16, 5)),
        mark(circle(6.5, 16, 1.3)),
        line(poly([(6.5, 16), (8.5, 8), (11.5, 8)], r=S.r * 0.6)),
        line(seg(6.5, 5.5, 10.5, 5.5)), line(seg(8.5, 8, 8.5, 5.5)),
        line(poly([(11.5, 8), (17, 11)], r=0)),
        line(seg(14.5, 11, 20, 11)),
        line(seg(17, 11, 19, 17)),
        shell(circle(19, 18.5, 3)),
        shell(circle(21.2, 17.2, 0.01)) if False else mark(circle(19, 18.5, 1)),
    ]


@icon("balance-bike", CAT, "Small bike with no pedals, a low seat and handlebars",
      tags=["balance bike", "push bike", "run bike", "strider style", "toddler bike", "learning to ride"])
def _(S):
    return [
        shell(circle(5.5, 17, 4.2)),
        shell(circle(18.5, 17, 4.2)),
        line(seg(5.5, 17, 8.5, 8)),
        line(seg(6.5, 6.5, 11, 6.5)), line(seg(8.5, 8, 8.5, 6.5)),
        line(poly([(8.5, 9), (16, 11.5), (18.5, 17)], r=S.r * 0.6)),
        line(seg(14, 9.5, 18.5, 9.5)),
    ]


@icon("training-wheels", CAT, "Back view of a bike wheel with a small stabilizer wheel on an arm at each side",
      tags=["training wheels", "stabilisers", "stabilizers", "learning to ride", "kids bike", "bike wheel"])
def _(S):
    rc = L(S, 0.5, 1.5)
    return [
        line(seg(9, 2.5, 15, 2.5)),
        line(seg(12, 2.5, 12, 5)),
        shell(rect(10.5, 5, 3, 16, rc)),
        line(seg(12, 15, 4.5, 18)), line(seg(12, 15, 19.5, 18)),
        shell(rect(2.5, 15.5, 3, 6, rc)), shell(rect(18.5, 15.5, 3, 6, rc)),
    ]


@icon("pull-wagon", CAT, "Open wagon with slatted sides on wheels with a long pull handle reaching forward",
      tags=["pull wagon", "wagon", "red wagon", "kids wagon", "cart", "pull along"])
def _(S):
    parts = [shell(rect(8, 5.5, 14, 9.5, L(S, 0.5, 2.5)))]
    for x in (12.7, 15, 17.3):
        parts.append(detail(seg(x, 5.5, x, 15)))
    parts += [
        line(seg(8, 12.5, 3, 5.5)),
        line(seg(1.5, 5.5, 4.5, 3.5)),
        wheel(11.5, 18.5, 3), wheel(19, 18.5, 3),
    ]
    return parts