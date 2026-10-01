"""TypeIcon Core: crafts (batch 003, puzzles, hobby models, studio tools, fibre crafts and collecting).

Visual language: sheets and boards are plain rectangles with the style radius, small printed or cut marks are
`mark` parts (solid in Line and Rounded, knocked out of a Filled shell), long tools lie on the 45 degree diagonal
with the handle to the bottom-left, and ground or table lines sit near y 21.
"""
from __future__ import annotations

import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "crafts"


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


def rseg(x1, y1, x2, y2, deg, cx=12.0, cy=12.0):
    (a, b), (c, d) = rpts([(x1, y1), (x2, y2)], deg, cx, cy)
    return seg(a, b, c, d)


def move(d, dx, dy):
    return path_to_d(transform_path(P(d), (1, 0, 0, 1, dx, dy)))


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled shell."""
    return Part("dot", d)


def pip(S, x, y, r=1.25):
    """Round dot in Rounded, square dot in Line."""
    if S.name == "line":
        return mark(rect(x - r * 0.9, y - r * 0.9, r * 1.8, r * 1.8))
    return dot(x, y, r)


def star_pts(cx, cy, r, inner=0.45, n=5, start=-90.0):
    out = []
    for i in range(n * 2):
        out.append(polar(cx, cy, r if i % 2 == 0 else r * inner, start + i * 180.0 / n))
    return out


def sparkle(cx, cy, r, k=0.3):
    """Four-point sparkle outline points."""
    return [(cx, cy - r), (cx + r * k, cy - r * k), (cx + r, cy), (cx + r * k, cy + r * k),
            (cx, cy + r), (cx - r * k, cy + r * k), (cx - r, cy), (cx - r * k, cy - r * k)]


def wave(x0, x1, y, n, amp=1.0):
    """Gentle wave line from x0 to x1 made of n half waves."""
    w = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        xa = x0 + i * w
        d += f"Q{fmt(xa + w / 2)} {fmt(y - amp * (2 if i % 2 == 0 else -2))} {fmt(xa + w)} {fmt(y)}"
    return d


def heart_d(cx, cy, w, h):
    """Heart outline centred on cx: top cusp at cy - h/2 + h*0.22, point at cy + h/2."""
    top = cy - h / 2
    bot = cy + h / 2
    cusp = top + h * 0.22
    x0, x1 = cx - w / 2, cx + w / 2
    return (f"M{fmt(cx)} {fmt(bot)}C{fmt(cx - w * 0.2)} {fmt(bot - h * 0.2)} {fmt(x0)} {fmt(cy + h * 0.05)} {fmt(x0)} {fmt(top + h * 0.3)}"
            f"C{fmt(x0)} {fmt(top - h * 0.05)} {fmt(cx - w * 0.05)} {fmt(top - h * 0.05)} {fmt(cx)} {fmt(cusp)}"
            f"C{fmt(cx + w * 0.05)} {fmt(top - h * 0.05)} {fmt(x1)} {fmt(top - h * 0.05)} {fmt(x1)} {fmt(top + h * 0.3)}"
            f"C{fmt(x1)} {fmt(cy + h * 0.05)} {fmt(cx + w * 0.2)} {fmt(bot - h * 0.2)} {fmt(cx)} {fmt(bot)}Z")


# ============================================================================ puzzles and paper crafts

@icon("crossword", CAT, "Square crossword grid with a few blacked-out squares",
      tags=["crossword puzzle", "puzzle", "word game", "newspaper puzzle", "grid", "clues"])
def _(S):
    c = 6
    out = [shell(rect(3, 3, 18, 18, S.R))]
    for i in (1, 2):
        out.append(detail(seg(3 + c * i, 3, 3 + c * i, 21)))
        out.append(detail(seg(3, 3 + c * i, 21, 3 + c * i)))
    for col, row in ((1, 0), (2, 1), (0, 2)):
        x, y = 3 + c * col, 3 + c * row
        out.append(mark(rect(x + 1, y + 1, c - 2, c - 2)))
    return out


@icon("connect-the-dots", CAT, "Star outline half joined by straight lines between a ring of dots",
      tags=["dot to dot", "join the dots", "activity book", "kids puzzle", "drawing game", "star"])
def _(S):
    pts = star_pts(12, 12.6, 9.2, inner=0.46)
    out = [line(poly(pts[:8], r=S.r), stroke_miterlimit="2")]
    for x, y in pts:
        out.append(dot(x, y, 2.1) if S.name == "rounded" else mark(rect(x - 1.8, y - 1.8, 3.6, 3.6)))
    return out


@icon("sand-art-bottle", CAT, "Corked bottle filled with wavy layers of coloured sand",
      tags=["sand art", "layered sand", "bottle craft", "souvenir", "kids craft", "colored sand"])
def _(S):
    body = poly([(10, 7.5), (10, 9.5), (6, 12.5), (6, 21), (18, 21), (18, 12.5), (14, 9.5), (14, 7.5)], closed=True, r=S.r)
    return [
        shell(body),
        mark(rect(10, 2, 4, 3.5, L(S, 0, 1))),
        detail(wave(6, 18, 14.5, 3, 0.7)),
        detail(wave(6, 18, 18, 3, 0.7)),
    ]


@icon("glitter", CAT, "Shaker tube of glitter with sparkles flying out of its cap",
      tags=["sparkle", "glitter shaker", "shimmer", "craft supply", "decoration", "shiny"])
def _(S):
    return [
        shell(rect(3.5, 8.5, 8, 12.5, min(S.R, 2))),
        detail(seg(3.5, 12, 11.5, 12)),
        shell(poly(sparkle(17, 7, 4.8), closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
        shell(poly(sparkle(17.5, 16.5, 2.8), closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        dot(9.5, 4.5, 1.1), dot(13, 12, 1.1), dot(5.5, 4.5, 1.1),
    ]


@icon("modeling-clay", CAT, "Open tub of modelling clay with a squashed lump beside it",
      tags=["modelling clay", "modelling dough", "kids craft", "sculpting", "dough"])
def _(S):
    tub = poly([(2.5, 11), (12.5, 11), (11.5, 21), (3.5, 21)], closed=True, r=S.r)
    dome = "M3.5 11.5C3.5 7 11.5 7 11.5 11.5Z"
    lump = "M14.5 21C14.5 16.5 16.5 14 18.3 14C20.2 14 22 16.5 22 21Z"
    return [
        shell(union(tub, dome)),
        detail(seg(2.5, 11, 12.5, 11)),
        detail(seg(3, 14, 12, 14)),
        shell(lump),
        detail(arc(18.3, 19.2, 1.4, 190, 350)),
    ]


@icon("craft-punch", CAT, "Square paper punch with a push lever on top and a punched star below",
      tags=["paper punch", "shape punch", "scrapbooking", "punch", "star punch", "card making"])
def _(S):
    return [
        shell(rect(6.5, 2.5, 11, 2.5, min(S.R, 1.25))),
        line(seg(12, 5, 12, 7)),
        shell(rect(5, 7, 14, 8, min(S.R, 3))),
        line(seg(2, 12, 5, 12)), line(seg(19, 12, 22, 12)),
        detail(seg(5, 12, 19, 12)),
        solid(poly(star_pts(12, 19.6, 2.7, inner=0.48), closed=True, r=S.r * 0.2)),
    ]


@icon("pop-up-card", CAT, "Opened greeting card with a paper house standing up from the fold",
      tags=["pop up card", "greeting card", "paper engineering", "card making", "3d card", "kirigami"])
def _(S):
    return [
        line(poly([(4, 14), (4, 3), (20, 3), (20, 14)], r=S.r)),
        line(poly([(7, 14), (4, 14), (2, 20.5), (22, 20.5), (20, 14), (17, 14)], r=S.r)),
        shell(poly([(9, 17), (9, 10.5), (12, 7.5), (15, 10.5), (15, 17)], closed=True, r=S.r * 0.6)),
    ]


@icon("heat-press", CAT, "Clamshell heat press with its top plate lifted open on a hinge above the base plate",
      tags=["heat press", "t-shirt press", "transfer press", "sublimation", "htv", "garment printing"])
def _(S):
    hx, hy = 4.5, 14.0
    plate = poly(rpts([(4.5, 10.5), (17.5, 10.5), (17.5, 14), (4.5, 14)], -26, hx, hy), closed=True, r=S.r * 0.6)
    hd = rpts([(17.5, 12.25), (20.5, 12.25)], -26, hx, hy)
    return [
        shell(rect(2.5, 16.5, 19, 4.5, min(S.R, 2))),
        dot(18.5, 18.75, 1),
        shell(plate),
        line(seg(hd[0][0], hd[0][1], hd[1][0], hd[1][1])),
        line("M11 14.5Q10 13.5 11 12.5"),
        line("M15 14.5Q14 13.5 15 12.5"),
    ]


@icon("vinyl-cutter", CAT, "Desktop cutting plotter with a front slot and a sheet feeding out below with a star cut from it",
      tags=["cutting plotter", "craft cutter", "vinyl", "plotter", "sign making", "decals", "cutting machine"])
def _(S):
    return [
        shell(rect(2, 3.5, 20, 9, S.R)),
        detail(seg(2, 8, 22, 8)),
        pip(S, 18.5, 5.8, 0.9),
        line(poly([(6, 12.5), (6, 21), (18, 21), (18, 12.5)], r=S.r)),
        mark(poly(star_pts(12, 16.8, 2.8, inner=0.5), closed=True, r=S.r * 0.15)),
    ]


@icon("3d-pen", CAT, "Chunky 3D printing pen drawing a raised squiggle of plastic",
      tags=["3d pen", "3d printing pen", "doodle pen", "filament", "hot plastic", "maker"])
def _(S):
    local = poly([(9, 2), (15, 2), (15, 12), (13.5, 15.5), (10.5, 15.5), (9, 12)], closed=True, r=S.r)
    pen = rot(local, 40, 12, 9)
    tip = rpts([(12, 16.5)], 40, 12, 9)[0]
    return [
        shell(pen),
        detail(rseg(12, 5, 12, 8.5, 40, 12, 9)),
        line(f"M{fmt(tip[0])} {fmt(tip[1] + 0.5)}C{fmt(tip[0] - 1)} 21 9 21.5 10 18.5S14 16 14.5 19S18 22 21.5 18.5"),
    ]


@icon("drawing-tablet", CAT, "Graphics tablet with a stylus pen lying across its drawing area",
      tags=["graphics tablet", "pen tablet", "stylus", "digital art", "illustration", "drawing pad"])
def _(S):
    pen = rot(poly([(10.5, 5), (13.5, 5), (13.5, 17), (12, 20), (10.5, 17)], closed=True, r=S.r * 0.5), 45)
    return [
        shell(rect(2, 4, 20, 16, S.R)),
        detail(pen),
        dot(5, 8, 1), dot(5, 11.5, 1),
    ]


@icon("model-kit", CAT, "Plastic model kit frame with small parts held by runners",
      tags=["sprue", "model kit", "plastic kit", "scale model", "runner", "hobby", "parts frame"])
def _(S):
    out = [
        shell(rect(3, 3.5, 18, 17, S.R)),
        detail(seg(12, 3.5, 12, 20.5)),
        detail(seg(3, 12, 21, 12)),
    ]
    out += [dot(7.25, 7.75, 1.9), detail(seg(9, 7.75, 12, 7.75))]
    out += [mark(rect(14.5, 5.5, 4, 3.5, L(S, 0, 1))), detail(seg(16.5, 9, 16.5, 12))]
    out += [mark(rect(5.5, 15.5, 4, 3, L(S, 0, 1))), detail(seg(7.5, 12, 7.5, 15.5))]
    out += [dot(16.75, 16.25, 1.9), detail(seg(12, 16.25, 15, 16.25))]
    return out


def sail(x, top, bot, wt=1.7, wb=2.4):
    return poly([(x - wt, top), (x + wt, top), (x + wb, bot), (x - wb, bot)], closed=True, r=0)


@icon("model-ship", CAT, "Model three-masted sailing ship with square sails on a display stand",
      tags=["ship model", "tall ship", "galleon", "scale model", "hobby", "sailing ship"])
def _(S):
    out = [shell(poly([(2.5, 14), (21.5, 14), (18.5, 18), (5.5, 18)], closed=True, r=S.r * 0.6))]
    for x, top in ((5.8, 5.5), (12, 2.5), (18.2, 5.5)):
        out.append(line(seg(x, top - 0.5, x, 14)))
        out.append(mark(sail(x, top + 1.2, 11.8)))
    out += [line(seg(9, 18, 9, 20.5)), line(seg(15, 18, 15, 20.5)), line(seg(6, 21, 18, 21))]
    return out


@icon("sudoku", CAT, "Square number-puzzle grid split into nine boxes, each with a few small digit marks",
      tags=["sudoku", "number puzzle", "logic puzzle", "grid puzzle", "brain teaser", "newspaper puzzle"])
def _(S):
    out = [shell(rect(3, 3, 18, 18, S.R))]
    for i in (1, 2):
        out.append(detail(seg(3 + 6 * i, 3, 3 + 6 * i, 21)))
        out.append(detail(seg(3, 3 + 6 * i, 21, 3 + 6 * i)))
    for col, row, dx in ((0, 0, 0.3), (2, 0, -0.3), (1, 1, 0), (0, 2, -0.3), (2, 2, 0.3)):
        x, y = 3 + 6 * col + 3 + dx, 3 + 6 * row + 3
        out.append(mark(rect(x - 0.9, y - 1.6, 1.8, 3.2, L(S, 0, 0.9))))
    return out


@icon("string-art", CAT, "Wooden board with a heart of thread looped around nails",
      tags=["string art", "nail and thread", "thread art", "heart", "diy decor", "wall art"])
def _(S):
    out = [shell(rect(2.5, 2.5, 19, 19, S.R))]
    out.append(detail(heart_d(12, 12.2, 10.5, 9.5)))
    for x, y in ((12, 17), (6.8, 10), (17.2, 10)):
        out.append(dot(x, y, 1.6) if S.name == "rounded" else mark(rect(x - 1.4, y - 1.4, 2.8, 2.8)))
    return out


@icon("paper-quilling", CAT, "Flower built from tight rolled paper coils around a centre coil",
      tags=["quilling", "paper coil", "paper rolling", "filigree", "paper craft", "card decoration"])
def _(S):
    out = [dot(12, 12, 2.2) if S.name == "rounded" else mark(rect(10, 10, 4, 4))]
    for dx, dy in ((0, -6.5), (0, 6.5), (-6.5, 0), (6.5, 0)):
        if S.name == "rounded":
            out.append(shell(circle(12 + dx, 12 + dy, 2.7)))
        else:
            out.append(shell(poly(regular(12 + dx, 12 + dy, 3.1, 4, 45), closed=True)))
    return out


def _snow_arms(r):
    arms = []
    for k in range(6):
        a = -90 + 60 * k
        arms.append(poly([polar(12, 12, 1.5, a), polar(12, 12, 6.4, a + 27), polar(12, 12, 9.6, a), polar(12, 12, 6.4, a - 27)],
                         closed=True, r=r))
    return arms


def _snow_filled():
    arms = _snow_arms(0)
    body = U(*[P(d) for d in arms], *[ST(d, 2.0, "butt", "miter", 2.0) for d in arms])
    cuts = []
    for k in range(6):
        a = -90 + 60 * k
        c = polar(12, 12, 5.6, a)
        cuts.append(P(poly([polar(*c, 2.4, a), polar(*c, 1.3, a + 90), polar(*c, 2.4, a + 180), polar(*c, 1.3, a - 90)], closed=True)))
    return D(body, *cuts)


@icon("paper-snowflake", CAT, "Six-armed snowflake cut from folded paper with small diamond cutouts",
      tags=["snowflake", "paper cut", "folded paper", "winter craft", "kirigami", "christmas decoration"], filled=_snow_filled)
def _(S):
    return [shell(union(*_snow_arms(S.r * 0.4)), stroke_miterlimit="2")]


@icon("stencil-brush", CAT, "Round stencil brush with a flat end dabbing paint through a star-shaped stencil sheet",
      tags=["stencil", "stippling brush", "dabber", "stenciling", "paint through stencil", "diy decor"])
def _(S):
    def br(pts):
        return [(x + 1.8, y - 4.6) for x, y in rpts(pts, 45, 12, 15)]
    body = [(11, 4.5), (13, 4.5), (13, 8), (14, 8), (14, 11.5), (15.5, 11.5), (15.5, 15), (8.5, 15), (8.5, 11.5), (10, 11.5), (10, 8), (11, 8)]
    d = br([(10, 11.5), (14, 11.5)])
    return [
        shell(rect(2.5, 12.5, 12.5, 9, min(S.R, 3))),
        mark(poly(star_pts(8.75, 17.2, 3.0, inner=0.5), closed=True, r=S.r * 0.15)),
        shell(poly(br(body), closed=True, r=S.r * 0.4)),
        detail(seg(*d[0], *d[1])),
    ]


@icon("rc-transmitter", CAT, "Handheld radio controller with two joysticks and a long antenna",
      tags=["rc controller", "remote control", "radio control", "transmitter", "drone controller", "hobby"])
def _(S):
    body = poly([(3, 11.5), (21, 11.5), (21, 18), (16, 21), (8, 21), (3, 18)], closed=True, r=S.r * 1.2)
    return [
        line(seg(17.5, 11.5, 17.5, 2.5)),
        shell(body),
        dot(8, 16, 1.6), dot(16, 16, 1.6),
        line(seg(12, 14, 12, 14.01)) if False else mark(rect(11, 13.5, 2, 2)),
    ]


@icon("model-rocket", CAT, "Slim model rocket with a pointed nose cone and fins, standing beside its launch rod",
      tags=["rocket kit", "model rocketry", "launch", "hobby rocket", "space", "launch rod"])
def _(S):
    d = ("M9.5 2C12.3 4.5 12.8 7.5 12.8 10.5L12.8 15L15.5 19.5L4 19.5L6.2 15L6.2 10.5C6.2 7.5 6.7 4.5 9.5 2Z")
    out = [shell(d, stroke_miterlimit="2"), detail(seg(9.5, 14, 9.5, 19.5)), dot(9.5, 9.5, 1.3),
           line(seg(19.5, 5, 19.5, 21)), line(seg(16.5, 21, 22.5, 21))]
    return out


@icon("diorama", CAT, "Shadow box scene with a small pine tree, a figure and a floor inside an open-fronted frame",
      tags=["scale scene", "miniature scene", "shadow box", "model scene", "hobby display", "tiny world"])
def _(S):
    return [
        shell(rect(3, 3.5, 18, 17, S.R)),
        mark(poly([(8.5, 6.5), (11.5, 12.5), (5.5, 12.5)], closed=True, r=S.r * 0.3)),
        detail(seg(8.5, 12.5, 8.5, 16)),
        dot(16, 10.5, 1.4),
        detail(seg(16, 12.5, 16, 16)),
        detail(seg(3, 16, 21, 16)),
    ]


@icon("hobby-knife", CAT, "Pen-style craft knife with a ridged grip and a small pointed blade",
      tags=["craft knife", "precision knife", "scalpel", "cutting", "modelling tool"])
def _(S):
    def T(d):
        return rot(d, 45)
    blade = poly([(10.5, 8.5), (10.5, 2.5), (13.5, 8.5)], closed=True, r=S.r * 0.3)
    return [
        shell(T(blade), stroke_miterlimit="2"),
        shell(T(poly([(10.5, 8.5), (13.5, 8.5), (14, 11), (10, 11)], closed=True, r=S.r * 0.3))),
        shell(T(rect(9.5, 11, 5, 10.5, min(S.R, 2)))),
        detail(rseg(9.5, 14.5, 14.5, 14.5, 45)),
        detail(rseg(9.5, 17.5, 14.5, 17.5, 45)),
    ]


@icon("model-paint-pot", CAT, "Small faceted hobby paint pot with a flip-up lid and a painted label",
      tags=["hobby paint", "miniature paint", "enamel pot", "acrylic paint", "paint bottle", "model paint"])
def _(S):
    body = poly([(5, 12.5), (8, 9.5), (16, 9.5), (19, 12.5), (19, 21), (5, 21)], closed=True, r=S.r)
    return [
        shell(body),
        shell(rect(8, 3.5, 8, 6, min(S.R, 2))),
        line(seg(16, 6.5, 19.5, 6.5)),
        mark(rect(9, 14, 6, 4, L(S, 0, 1))),
    ]


@icon("tabletop-miniature", CAT, "Small warrior figure with a sword standing on a round base, a fine brush reaching in to paint it",
      tags=["miniature", "wargaming", "tabletop gaming", "figurine", "painted mini", "hobby painting", "role playing"])
def _(S):
    out = [
        shell(rect(3, 17, 11, 4, 2)),
        dot(9.5, 6.3, 2.2),
        shell(poly([(7, 10.5), (12, 10.5), (13, 17), (6, 17)], closed=True, r=S.r * 0.6)),
        line(seg(3.5, 6, 3.5, 14)),
        line(seg(2.5, 8.5, 4.5, 8.5)),
        line(seg(21.5, 2.5, 18, 6)),
        dot(16.8, 7.6, 1.6),
    ]
    return out


@icon("balsa-glider", CAT, "Toy balsa glider seen from above with a straight wing and tail slotted onto a thin body",
      tags=["toy plane", "model plane", "free flight", "paper plane", "kids toy", "airplane", "hobby"])
def _(S):
    def T(pts):
        return rpts(pts, 40, 12, 12)
    return [
        line(seg(*T([(12, 2.5), (12, 21.5)])[0], *T([(12, 2.5), (12, 21.5)])[1])),
        shell(poly(T([(3, 7), (21, 7), (21, 11.5), (3, 11.5)]), closed=True, r=S.r * 0.5)),
        shell(poly(T([(8, 17), (16, 17), (16, 20.5), (8, 20.5)]), closed=True, r=S.r * 0.5)),
    ]


@icon("pottery-kiln", CAT, "Squat studio kiln with a front door, a round peephole and a top vent, with heat rising above",
      tags=["kiln", "ceramics kiln", "firing", "pottery", "oven", "studio", "ceramic"])
def _(S):
    return [
        shell(rect(3.5, 10.5, 17, 10.5, min(S.R, 3))),
        detail(rect(7, 13.5, 10, 5, 0)),
        line(seg(12, 10.5, 12, 8)),
        line("M8 7.5Q7 6 8 4.5T8 2.5"),
        line("M16 7.5Q15 6 16 4.5T16 2.5"),
        pip(S, 12, 16, 1.0),
    ]


@icon("paint-box", CAT, "Open artist paint box with its lid raised, a brush lying inside and a row of paint tubes",
      tags=["artist box", "watercolor box", "paint set", "art supplies", "painting kit", "oil paint box", "easel box"])
def _(S):
    return [
        shell(poly([(4, 8.5), (6.5, 3), (17.5, 3), (20, 8.5)], closed=True, r=S.r * 0.6)),
        shell(rect(2.5, 8.5, 19, 12.5, min(S.R, 3))),
        detail(seg(6, 12.5, 18, 12.5)),
        mark(rect(6, 15, 3, 4.5, L(S, 0, 1))),
        mark(rect(10.5, 15, 3, 4.5, L(S, 0, 1))),
        mark(rect(15, 15, 3, 4.5, L(S, 0, 1))),
    ]


# ============================================================================ drawing, painting and sculpture

@icon("portrait-sketch", CAT, "Sheet of paper with a loosely sketched face in pencil",
      tags=["face sketch", "portrait drawing", "pencil drawing", "life drawing", "figure study", "sketchbook"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, S.R)),
        detail(ellipse(12, 11.5, 4.6, 5.6)),
        pip(S, 10.2, 10.2, 0.85),
        pip(S, 13.8, 10.2, 0.85),
        detail(seg(10.5, 14, 13.5, 14)),
    ]


@icon("gesture-drawing", CAT, "Figure sketched with a few quick flowing curves in a dynamic pose",
      tags=["quick sketch", "life drawing", "figure drawing", "pose", "croquis", "movement", "sketching"])
def _(S):
    return [
        dot(15.5, 4.8, 2.1),
        line("M14.2 8C12.5 10.5 9.5 11.5 9.5 15"),
        line("M9.5 15C9 18 6.5 19.5 4.5 21"),
        line("M9.5 15C11.5 16.5 14.5 17 17.5 18"),
        line("M13 10C15.5 10 18 11.5 20.5 10.5"),
        line("M12 10.5C9.5 9 6.5 9.5 4 7.5"),
    ]


def _inside_rr(x, y, x0, y0, w, h, r, tol=0.02):
    cx = min(max(x, x0 + r), x0 + w - r)
    cy = min(max(y, y0 + r), y0 + h - r)
    return math.hypot(x - cx, y - cy) <= r + tol


def clip_seg(p0, p1, x0, y0, w, h, r):
    """Shrink a segment whose ends lie on the bounding box until both ends sit on the rounded rectangle outline."""
    def walk(a, b):
        for i in range(0, 400):
            t = i / 400
            x, y = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            if _inside_rr(x, y, x0, y0, w, h, r):
                return x, y
        return a
    return walk(p0, p1), walk(p1, p0)


@icon("cross-hatching", CAT, "Square shaded with two sets of crossing diagonal lines that grow denser toward one corner",
      tags=["hatching", "shading", "pen and ink", "drawing technique", "sketch shading", "crosshatch", "tone"])
def _(S):
    rr_ = min(S.R, 2.5)
    out = [shell(rect(3, 3, 18, 18, rr_))]
    lines = []
    for c in (14, 20, 26):
        p0 = (3, c - 3) if c <= 24 else (c - 21, 21)
        p1 = (c - 3, 3) if c <= 24 else (21, c - 21)
        lines.append((p0, p1))
    for d in (-12, -6):
        lines.append(((3, 3 - d), (21 + d, 21)))
    for p0, p1 in lines:
        a, b = clip_seg(p0, p1, 3, 3, 18, 18, rr_)
        out.append(detail(seg(a[0], a[1], b[0], b[1])))
    return out


@icon("stippling", CAT, "Round sphere shaded only with dots, dense on one side and sparse on the other",
      tags=["stipple", "dot shading", "pointillism", "dotwork", "pen shading", "ink dots", "illustration technique"])
def _(S):
    out = [shell(circle(12, 12, 9.2) if S.name == "rounded" else poly(regular(12, 12, 9.6, 8, 22.5), closed=True))]
    for x, y in ((15, 8.5), (18, 12), (12.5, 12.5), (15.5, 15.5), (9.5, 15.5), (12.5, 18.5), (8.5, 8), (12, 5.8), (5.8, 12.5)):
        out.append(pip(S, x, y, 1.0))
    return out


@icon("abstract-painting", CAT, "Framed canvas with overlapping circle, square and triangle shapes in a loose composition",
      tags=["modern art", "abstract art", "gallery", "canvas", "geometric art", "contemporary art", "artwork"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 18, S.R)),
        detail(circle(9.5, 10, 3.2)),
        mark(poly([(14, 6.5), (18, 12.5), (10.5, 15.5)], closed=True, r=S.r * 0.3)) if False else mark(poly([(15.5, 6.5), (18.5, 11.5), (12.5, 11.5)], closed=True, r=S.r * 0.3)),
        mark(rect(10.5, 14.5, 4.5, 3.5, L(S, 0, 1))),
    ]


@icon("portrait-painting", CAT, "Framed portrait painting hanging from a cord, showing a head and shoulders silhouette",
      tags=["portrait", "oil painting", "gallery frame", "hanging picture", "wall art", "artwork", "head and shoulders"])
def _(S):
    return [
        line(poly([(7.5, 6.5), (12, 2.5), (16.5, 6.5)], r=S.r * 0.5)),
        shell(rect(4, 6.5, 16, 15, S.R)),
        mark(circle(12, 11.3, 2.4)),
        mark("M7.6 20.5C7.6 15.8 16.4 15.8 16.4 20.5Z"),
    ]


@icon("brush-hanger", CAT, "Gallows-style brush stand with three calligraphy brushes hanging tip down from its arm",
      tags=["brush stand", "calligraphy brush", "brush rack", "ink brush", "brush holder", "chinese brush", "drying rack"])
def _(S):
    out = [line(poly([(3, 3.5), (20, 3.5), (20, 21)], r=S.r * 0.5)), line(seg(16.5, 21, 22, 21))]
    for x in (5.2, 10.5, 15.8):
        out.append(line(seg(x, 3.5, x, 10.5)))
        out.append(mark(poly([(x - 1.6, 10.5), (x + 1.6, 10.5), (x + 1.6, 15), (x, 20.5), (x - 1.6, 15)], closed=True, r=S.r * 0.3)))
    return out


@icon("abstract-sculpture", CAT, "Smooth looping ribbon sculpture twisting back on itself, standing on a square base",
      tags=["modern sculpture", "abstract art", "gallery", "statue", "art object", "ribbon sculpture", "plinth"])
def _(S):
    return [
        line("M12 13C7 10 7 3.5 12 3.5C17 3.5 17 10 12 13C8 15.5 8 17 12 17C16 17 16 15.5 12 13"),
        shell(rect(6.5, 19, 11, 2.5, L(S, 0, 1.25))),
    ]


@icon("painted-tile", CAT, "Square ceramic tile painted with a symmetrical four-petal flower and corner dots",
      tags=["ceramic tile", "hand painted tile", "azulejo", "talavera", "decorative tile", "mosaic", "flower motif"])
def _(S):
    out = [shell(rect(3, 3, 18, 18, S.R))]
    for a in (0, 90, 180, 270):
        c = polar(12, 12, 4.4, a)
        out.append(mark(poly([polar(*c, 3.0, a), polar(*c, 1.5, a + 90), polar(*c, 3.0, a + 180), polar(*c, 1.5, a - 90)], closed=True)))
    out.append(dot(12, 12, 1.4))
    return out


@icon("yarn-cone", CAT, "Tall cone of wound yarn on a flat base with the loose end trailing to the side",
      tags=["thread cone", "yarn", "weaving", "knitting supply", "bobbin", "textile", "wool"])
def _(S):
    return [
        shell(poly([(10, 3.5), (14, 3.5), (17, 18), (7, 18)], closed=True, r=S.r * 0.5)),
        shell(rect(5, 18, 14, 3, min(S.R, 1.5))),
        detail("M8.8 9Q12 11 15.2 9"),
        detail("M8.2 13.5Q12 15.5 15.8 13.5"),
        line("M14 5.5C18 4 19 8 18 11C17 14 21 14 21.5 11"),
    ]


@icon("latch-hook", CAT, "Rug latch hook with a hooked tip and a small hinged latch flap, on a grip handle",
      tags=["rug hooking", "rug making", "latch hook tool", "hook", "yarn craft", "needlecraft", "rug hook"])
def _(S):
    return [
        line("M12 14V7.5A2.75 2.75 0 0 1 17.5 7.5V9.5"),
        line(seg(12, 10.5, 17, 8.2)),
        shell(rect(9.5, 14, 5, 7.5, min(S.R, 2.5))),
        detail(seg(12, 16.5, 12, 19)),
    ]


@icon("cable-needle", CAT, "Short knitting needle bent into a shallow U with a loop of yarn resting in the dip",
      tags=["cable knitting", "knitting tool", "stitch holder", "knit", "needlework", "yarn craft", "aran"])
def _(S):
    return [
        line(poly([(2.5, 6.5), (7.5, 6.5), (10, 12), (14, 12), (16.5, 6.5), (21.5, 6.5)], r=S.r * 0.8)),
        line("M9.6 12.2Q9.6 19.5 12 19.5Q14.4 19.5 14.4 12.2"),
    ]


# ============================================================================ sewing, woodwork and metal

@icon("batik-wax-pen", CAT, "Batik wax pen: a small handle with a tiny copper cup and thin spout drawing a wax line on cloth",
      tags=["tjanting", "batik", "wax resist", "fabric art", "dye craft", "wax pen", "textile"])
def _(S):
    cup = poly([(9, 4.5), (15, 4.5), (14, 9.5), (10, 9.5)], closed=True, r=S.r * 0.4)
    return [
        shell(rot(cup, 45)),
        shell(rot(rect(10.5, 9.5, 3, 11.5, min(S.R, 1.5)), 45)),
        line(rseg(15, 6.5, 20, 9.5, 45)),
        line("M13 21Q15.5 17.5 18 20Q19.5 21.5 21.5 18.5"),
    ]


@icon("embroidery-scissors", CAT, "Small embroidery scissors with long slim pointed blades and tiny ring handles",
      tags=["stork scissors", "sewing scissors", "thread snips", "needlework", "cross stitch", "fine scissors", "sewing"])
def _(S):
    return [
        line(seg(8.4, 18, 16.2, 2.5)),
        line(seg(15.6, 18, 7.8, 2.5)),
        shell(circle(7.6, 19.4, 2.3) if S.name == "rounded" else poly(regular(7.6, 19.4, 2.7, 4, 45), closed=True)),
        shell(circle(16.4, 19.4, 2.3) if S.name == "rounded" else poly(regular(16.4, 19.4, 2.7, 4, 45), closed=True)),
        dot(12, 11.2, 1.0),
    ]


@icon("presser-foot", CAT, "Sewing machine presser foot seen from below with two flat toes, a needle slot and a mounting shank",
      tags=["sewing foot", "machine foot", "sewing machine part", "zipper foot", "quilting foot", "sewing", "notions"])
def _(S):
    return [
        line(seg(8.5, 3, 15.5, 3)),
        line(seg(12, 3, 12, 9)),
        shell(poly([(3.5, 9), (20.5, 9), (20.5, 21), (14.6, 21), (14.6, 13.5), (9.4, 13.5), (9.4, 21), (3.5, 21)], closed=True, r=S.r * 0.5)),
    ]


@icon("serger", CAT, "Compact overlock sewing machine with four thread cones standing in a row on top",
      tags=["overlocker", "overlock machine", "sewing machine", "serging", "thread cones", "garment sewing", "hemming"])
def _(S):
    out = [
        shell(poly([(2.5, 21), (2.5, 12.5), (17, 12.5), (17, 15), (21.5, 15), (21.5, 21)], closed=True, r=S.r * 0.8)),
        detail(seg(2.5, 17.5, 21.5, 17.5)),
    ]
    for x in (5, 9.6, 14.2, 18.8):
        out.append(mark(poly([(x - 0.7, 3.5), (x + 0.7, 3.5), (x + 1.4, 10), (x - 1.4, 10)], closed=True)))
    out.append(line(seg(3, 11, 21, 11)))
    return out


@icon("hook-knife", CAT, "Spoon-carving hook knife: a wooden handle with a blade curled into a tight hook",
      tags=["spoon knife", "carving knife", "woodcarving", "whittling", "bowl carving", "green woodwork", "spoon carving"])
def _(S):
    blade = path_to_d(ST("M12 12.5V9C12 5 8.6 3.2 5.8 4.8C4 6 4.5 9 7.4 9", 2.2, "round", "round"))
    return [
        solid(rot(blade, 45)),
        shell(rot(rect(9.5, 11.5, 5, 10, min(S.R, 2.5)), 45)),
        detail(rseg(12, 14.5, 12, 19, 45)),
    ]


@icon("miter-joint", CAT, "Two boards meeting at a right-angle corner with a diagonal 45 degree seam",
      tags=["mitre joint", "picture frame corner", "woodworking joint", "carpentry", "45 degree cut", "trim", "corner joint"])
def _(S):
    return [
        shell(poly([(3, 3), (21, 3), (21, 9.5), (9.5, 9.5), (9.5, 21), (3, 21)], closed=True, r=S.r * 0.6)),
        detail(seg(3, 3, 9.5, 9.5)),
    ]


@icon("tongue-and-groove", CAT, "Two boards set slightly apart, one with a protruding tongue and one with a matching slot",
      tags=["wood joint", "flooring", "carpentry", "joinery", "planks", "woodworking joint", "panelling"])
def _(S):
    return [
        shell(poly([(2.5, 6), (8.5, 6), (8.5, 10), (12.5, 10), (12.5, 14), (8.5, 14), (8.5, 18), (2.5, 18)], closed=True, r=S.r * 0.4)),
        shell(poly([(21.5, 6), (16, 6), (16, 9), (20, 9), (20, 15), (16, 15), (16, 18), (21.5, 18)], closed=True, r=S.r * 0.4)),
    ]


@icon("lampworking", CAT, "Small torch flame heating a round glass bead on a thin mandrel",
      tags=["lampwork", "glass beads", "bead making", "torch", "flameworking", "glass art", "jewelry making"])
def _(S):
    return [
        line(seg(2.5, 7, 8.4, 7)),
        line(seg(15.6, 7, 21.5, 7)),
        shell(circle(12, 7, 3.4)),
        shell("M12 12.5C9 15.5 8 18 12 20C16 18 15 15.5 12 12.5Z"),
        line(seg(9.5, 21.5, 14.5, 21.5)),
    ]


@icon("mosaic-nippers", CAT, "Tile nippers with crossed handles and two small round wheel blades biting a square tile",
      tags=["wheeled nippers", "tile cutter", "mosaic tools", "tile nipper", "glass tile", "tessera", "mosaic art"])
def _(S):
    return [
        line(seg(8, 21.5, 14.4, 9)),
        line(seg(16, 21.5, 9.6, 9)),
        shell(circle(14.4, 6.8, 2.6)),
        shell(circle(9.6, 6.8, 2.6)),
        mark(rect(10.8, 1.8, 2.4, 2.4)),
    ]


@icon("metal-stamping", CAT, "Small hammer striking a letter punch that marks a round metal disc blank",
      tags=["hand stamping", "metal blank", "letter punch", "jewelry making", "leather stamp", "hammer and punch", "engraving"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 9, 4.5, min(S.R, 1.5))),
        line(seg(12.5, 4.75, 21.5, 4.75)),
        shell(poly([(6.5, 7), (9.5, 7), (9.5, 14), (8, 15.5), (6.5, 14)], closed=True, r=S.r * 0.3)),
        shell(ellipse(8, 19, 6.5, 2.4)),
    ]


@icon("chainmaille", CAT, "Pattern of small linked metal rings, each ring threaded through its four neighbours",
      tags=["chain mail", "chainmail", "maille", "metal rings", "jump rings", "armor weaving", "jewelry weaving"])
def _(S):
    out = []
    for cx, cy in ((7.5, 7.5), (16.5, 7.5), (12, 12), (7.5, 16.5), (16.5, 16.5)):
        if S.name == "rounded":
            out.append(line(circle(cx, cy, 3.8)))
        else:
            out.append(line(poly(regular(cx, cy, 4.1, 8, 22.5), closed=True)))
    return out


@icon("papier-mache", CAT, "Round balloon wrapped in curved paper strips with a paste brush beside it",
      tags=["paper mache", "papier mache", "paper strips", "balloon craft", "paste", "sculpting with paper", "craft project"])
def _(S):
    return [
        shell(circle(9.5, 9.5, 6.5)),
        detail("M3.5 10Q9.5 13 15.5 10"),
        detail("M7 4.2Q11 9.5 7.5 15"),
        shell(poly([(8.3, 16.6), (10.7, 16.6), (9.5, 18.8)], closed=True, r=S.r * 0.2)) if False else solid(poly([(8.4, 16.3), (10.6, 16.3), (9.5, 18.7)], closed=True)),
        line(seg(21.5, 10, 17.8, 14.2)),
        dot(16.6, 15.6, 1.7),
    ]


@icon("die-cut-machine", CAT, "Hand-crank die cutting machine with a cutting plate sandwich feeding through its rollers",
      tags=["die cutter", "craft cutter", "scrapbooking", "card making", "embossing", "manual die cut", "paper crafts"])
def _(S):
    return [
        shell(rect(7, 5.5, 12, 12.5, min(S.R, 3))),
        detail(seg(7, 11.75, 19, 11.75)),
        shell(rect(2.5, 10.25, 6.5, 3, min(S.R, 1))),
        line(seg(19, 11.75, 22, 11.75)),
        line(seg(22, 8.5, 22, 15)),
        line(seg(8, 21, 18, 21)),
    ]


@icon("light-painting", CAT, "Camera on a small tripod facing a bright looping light trail drawn in the dark",
      tags=["long exposure", "light trails", "night photography", "light graffiti", "slow shutter", "photography technique", "tripod"])
def _(S):
    return [
        shell(rect(2.5, 6, 9, 6.5, min(S.R, 2))),
        shell(circle(7, 9.25, 1.7)) if False else dot(7, 9.25, 1.5),
        line(seg(5, 12.5, 3.5, 21)),
        line(seg(9, 12.5, 10.5, 21)),
        line(seg(7, 12.5, 7, 17)),
        line("M14 20C21 20 22 13 18 10.5C14.5 8.5 12.5 11.5 15.5 13C18.5 14.5 21 11 20.5 7.5"),
    ]


@icon("contact-sheet", CAT, "Photo proof sheet with a grid of small frames in rows",
      tags=["proof sheet", "photo proofs", "film contact print", "darkroom", "photo selection", "thumbnail sheet", "negatives"])
def _(S):
    out = [shell(rect(3, 2.5, 18, 19, S.R))]
    for r in range(3):
        for c in range(2):
            out.append(mark(rect(6.5 + c * 6, 5.8 + r * 5, 4.8, 3.4, L(S, 0, 0.8))))
    return out


# ============================================================================ studio supplies and collecting

@icon("palette-cup", CAT, "Pair of small paint cups joined side by side, with a curved clip underneath for hooking onto a palette",
      tags=["dipper", "paint cup", "oil painting", "solvent cup", "palette clip", "double dipper", "art supplies"])
def _(S):
    return [
        shell(poly([(2.5, 3.5), (11, 3.5), (10, 12.5), (3.5, 12.5)], closed=True, r=S.r * 0.5)),
        shell(poly([(13, 3.5), (21.5, 3.5), (20.5, 12.5), (14, 12.5)], closed=True, r=S.r * 0.5)),
        line("M12 12.5V17.5Q12 20.5 15.5 20.5H21V17"),
    ]


@icon("foam-brush", CAT, "Wedge-shaped foam brush with a slanted tip on a plain wooden stick handle",
      tags=["sponge brush", "foam paintbrush", "craft brush", "painting", "staining", "diy", "disposable brush"])
def _(S):
    head = poly([(8, 11), (8, 5.5), (16, 2.5), (16, 11)], closed=True, r=S.r * 0.5)
    return [
        shell(rot(head, 45), stroke_miterlimit="2"),
        line(rseg(12, 11, 12, 21.5, 45)),
        detail(rseg(10.5, 8, 13.5, 8, 45)),
    ]


@icon("film-drying-clip", CAT, "Film strip with sprocket holes hanging from a drying line by a clip, with a weighted clip at its foot",
      tags=["film drying", "negative strip", "darkroom", "film developing", "weight clip", "analog photography", "35mm film"])
def _(S):
    return [
        line(seg(2, 3, 22, 3)),
        shell(rect(9.5, 3.5, 5, 3, min(S.R, 1))),
        shell(rect(7.5, 6.5, 9, 12, min(S.R, 1))),
        mark(rect(9, 8, 1.4, 1.4)), mark(rect(9, 11.3, 1.4, 1.4)), mark(rect(9, 14.6, 1.4, 1.4)),
        mark(rect(13.6, 8, 1.4, 1.4)), mark(rect(13.6, 11.3, 1.4, 1.4)), mark(rect(13.6, 14.6, 1.4, 1.4)),
        shell(rect(9, 18.5, 6, 3, min(S.R, 1))),
    ]


@icon("photo-booth", CAT, "Tall photo booth with a curtain drawn partly across, a stool inside and a photo strip at the side slot",
      tags=["photobooth", "instant photos", "photo strip", "passport photo", "kiosk", "booth", "photo machine"])
def _(S):
    return [
        shell(rect(3, 2.5, 13, 19, min(S.R, 3))),
        detail(seg(3, 7.5, 16, 7.5)),
        mark(rect(10.4, 9, 4.2, 11.5, L(S, 0, 1))),
        line(seg(4.6, 15.5, 8, 15.5)),
        line(seg(6.3, 15.5, 6.3, 20)),
        shell(rect(18, 8, 3.5, 9.5, min(S.R, 1))),
        detail(seg(18, 12.75, 21.5, 12.75)),
    ]


@icon("coin-album", CAT, "Coin collector album page with rows of round holes, some holding coins",
      tags=["coin collecting", "numismatics", "coin folder", "coin holder", "collection", "coin page", "collector album"])
def _(S):
    out = [shell(rect(2.5, 2.5, 19, 19, S.R))]
    for i, (x, y) in enumerate(((8, 8), (16, 8), (8, 16), (16, 16))):
        if i in (0, 3):
            out.append(dot(x, y, 2.6) if S.name == "rounded" else mark(rect(x - 2.3, y - 2.3, 4.6, 4.6)))
        else:
            out.append(detail(circle(x, y, 2.2) if S.name == "rounded" else rect(x - 2.2, y - 2.2, 4.4, 4.4)))
    return out


@icon("card-binder-page", CAT, "Clear binder sheet with a three by three grid of pockets, each holding a small card",
      tags=["trading card binder", "card sleeves", "card collection", "tcg", "card pocket page", "nine pocket", "collector"])
def _(S):
    out = [shell(rect(2.5, 2.5, 19, 19, S.R))]
    for r in range(3):
        for c in range(3):
            out.append(mark(rect(6 + c * 4.5, 5.2 + r * 5.3, 3, 4, L(S, 0, 0.7))))
    return out


@icon("graded-card", CAT, "Trading card sealed in a rigid clear grading case with a label strip across the top",
      tags=["slabbed card", "card grading", "collectible", "trading card", "sports card", "sealed card"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, S.R)),
        mark(rect(7, 4.6, 10, 1.6)),
        detail(rect(8, 9, 8, 9.5, min(S.R, 1.5))),
    ]


@icon("decal-sheet", CAT, "Sheet of printed decals with a star, stripes and a number, one corner peeling away",
      tags=["stickers sheet", "waterslide decal", "model decals", "transfer sheet", "peel", "hobby decals", "sticker"])
def _(S):
    return [
        shell(poly([(3, 3), (21, 3), (21, 12.5), (12.5, 21), (3, 21)], closed=True, r=S.r * 0.6)),
        detail(poly([(21, 12.5), (13, 13), (12.5, 21)], r=0)),
        mark(poly(star_pts(8.5, 8.6, 3.2, inner=0.5), closed=True, r=S.r * 0.15)),
        mark(rect(13, 6, 5, 1.8)),
        mark(rect(13, 9.4, 3.2, 1.8)),
        mark(rect(6.4, 14.5, 1.8, 3.8)),
    ]


@icon("family-tree", CAT, "Tree with a trunk and branches ending in three small round portrait frames",
      tags=["genealogy", "ancestry", "lineage", "pedigree", "heritage", "relatives", "family history"])
def _(S):
    def fr(x, y):
        return shell(circle(x, y, 2.3)) if S.name == "rounded" else shell(rect(x - 2.1, y - 2.1, 4.2, 4.2))
    return [
        line("M12 21.5V15M12 15C12 12.5 8 13 6.2 11.6M12 15C12 12.5 16 13 17.8 11.6M12 15V7.4"),
        fr(5.8, 9.2), fr(18.2, 9.2), fr(12, 5),
    ]


@icon("magic-rings", CAT, "Three large solid metal rings linked together, as in the classic rings magic trick",
      tags=["linking rings", "magic trick", "magician", "chinese rings", "illusion", "conjuring", "close up magic"])
def _(S):
    out = []
    for cx, cy in ((8.3, 8.3), (15.7, 8.3), (12, 15)):
        out.append(line(circle(cx, cy, 5.2)) if S.name == "rounded" else line(poly(regular(cx, cy, 5.5, 8, 22.5), closed=True)))
    return out


@icon("rc-boat", CAT, "Radio-controlled speedboat with a pointed hull, a small cabin and a thin antenna",
      tags=["remote control boat", "model boat", "speedboat", "radio controlled", "hobby boat", "toy boat", "rc hobby"])
def _(S):
    return [
        shell(poly([(2.5, 12.5), (21.5, 12.5), (18.5, 18.5), (6.5, 18.5)], closed=True, r=S.r * 0.6)),
        shell(poly([(9.5, 12.5), (11.5, 8), (16, 8), (17, 12.5)], closed=True, r=S.r * 0.5)),
        line(seg(16, 8, 19.5, 2.5)),
        line(wave(2.5, 21.5, 21.3, 4, 0.6)),
    ]


@icon("sprue-cutter", CAT, "Spring-loaded side cutter with short flat jaws snipping a model part from its runner",
      tags=["sprue nippers", "model nippers", "hobby cutter", "side cutter", "plastic model tool", "snips"])
def _(S):
    return [
        line(seg(6, 21.5, 11, 13)),
        line(seg(16, 21.5, 11, 13)),
        line(seg(11, 13, 14.2, 7.5)),
        line(seg(11, 13, 7.8, 7.5)),
        line(seg(7.8, 7.5, 10.5, 3)),
        line(seg(14.2, 7.5, 11.5, 3)),
        mark(rect(17.3, 3.5, 4, 3.2)),
        line(seg(14, 5, 17.3, 5)),
    ]


@icon("pin-vise", CAT, "Slim hand drill with a ridged barrel, a tiny drill bit in its chuck and a swivel cap on top",
      tags=["hand drill", "pin chuck", "micro drill", "hobby drill", "modelling tool", "jewelry drilling", "precision drill"])
def _(S):
    return [
        shell(rot(rect(10, 2, 4, 2, min(S.R, 1)), 45)),
        shell(rot(rect(9.5, 4.5, 5, 11, min(S.R, 2)), 45)),
        detail(rseg(9.5, 8, 14.5, 8, 45)),
        detail(rseg(9.5, 11, 14.5, 11, 45)),
        shell(rot(poly([(10.5, 15.5), (13.5, 15.5), (12.8, 18), (11.2, 18)], closed=True), 45)),
        line(rseg(12, 18, 12, 22, 45)),
    ]


@icon("clay-extruder", CAT, "Clay extruder gun: a metal tube with a plunger and lever pushing a clay coil out through a die plate",
      tags=["clay gun", "pottery tool", "ceramics", "extruding", "coil maker", "die plate", "sculpting tool"])
def _(S):
    return [
        line(seg(8, 2.5, 16, 2.5)),
        line(seg(12, 2.5, 12, 8)),
        shell(rect(7.5, 6, 9, 8, min(S.R, 2))),
        shell(rect(6.5, 14, 11, 2, min(S.R, 1))),
        line("M12 16.5Q8.5 18 12 19.3Q15.5 20.7 12 22"),
    ]


@icon("slab-roller", CAT, "Clay slab roller: a roller with a side crank pressing a flat slab of clay on the table",
      tags=["clay roller", "slab rolling", "pottery", "ceramics", "rolling pin", "handbuilding", "clay studio"])
def _(S):
    return [
        shell(rect(3, 6, 14, 6, min(S.R, 3))),
        line(seg(17, 9, 21.5, 9)),
        line(seg(21.5, 5.5, 21.5, 12.5)),
        shell(rect(3, 14.5, 15, 3.5, min(S.R, 1.75))),
        line(seg(2.5, 21, 21.5, 21)),
    ]


@icon("pottery-trimming-tool", CAT, "Wooden-handled trimming tool with a looped metal ribbon blade bent at an angle",
      tags=["loop tool", "trimming tool", "ribbon tool", "turning tool", "pottery wheel tool", "ceramics", "carving clay"])
def _(S):
    return [
        line(rot("M12 10C8 9.5 8 2.5 12 2.5C16 2.5 16 9.5 12 10Z", 45)),
        line(rseg(12, 10, 12, 12.5, 45)),
        shell(rot(rect(10, 12.5, 4, 9, L(S, 0, 2)), 45)),
    ]


@icon("glaze-test-tiles", CAT, "Row of three small upright test tiles with hanging holes, each showing a different glaze drip",
      tags=["test tile", "glaze sample", "ceramic glaze", "pottery", "kiln test", "glaze chemistry", "ceramics studio"])
def _(S):
    out = []
    for x, y in ((5, 12.5), (12, 14.5), (19, 11)):
        out.append(shell(rect(x - 1.7, 3.5, 3.4, 17, L(S, 0, 1.7))))
        out.append(dot(x, 6.3, 0.75))
        out.append(detail(seg(x - 1.7, y, x + 1.7, y)))
    return out


@icon("felt-sheets", CAT, "Stack of three soft felt sheets fanned out, the top one with a star cut from it",
      tags=["craft felt", "felt fabric", "fabric sheets", "felting", "soft crafts", "kids crafts", "felt stack"])
def _(S):
    return [
        line(poly([(8, 3), (21.5, 3), (21.5, 15)], r=S.r * 0.6)),
        line(poly([(5.5, 6.5), (18.5, 6.5), (18.5, 18)], r=S.r * 0.6)),
        shell(rect(2.5, 9.5, 12.5, 12, min(S.R, 3))),
        mark(poly(star_pts(8.75, 15.8, 3.5, inner=0.5), closed=True, r=S.r * 0.15)),
    ]


@icon("quilting-hoop", CAT, "Large round quilting hoop on a floor stand holding stretched patchwork fabric",
      tags=["quilt hoop", "embroidery hoop", "patchwork", "quilting frame", "sewing", "fabric stretching", "hoop stand"])
def _(S):
    out = [shell(circle(12, 9.3, 6.4) if S.name == "rounded" else poly(regular(12, 9.3, 6.9, 8, 22.5), closed=True))]
    out += [detail(seg(12, 3, 12, 15.6)), detail(seg(5.6, 9.3, 18.4, 9.3))]
    out += [mark(rect(7.6, 5.2, 2.4, 2.4)), mark(rect(14, 11.4, 2.4, 2.4))]
    out += [line(seg(12, 16.7, 12, 21)), line(seg(7.5, 21.3, 16.5, 21.3))]
    return out


@icon("applique", CAT, "Fabric square with a heart sewn on top and small stitches around its edge",
      tags=["applique stitch", "sewn patch", "fabric heart", "patchwork", "hand sewing", "quilt block", "textile craft"])
def _(S):
    out = [shell(rect(3, 3, 18, 18, S.R)), mark(heart_d(12, 12.3, 9, 8))]
    for a in (-150, -30, 90, 180, 0):
        pass
    for x, y, w, h in ((5.4, 11.5, 1.8, 1.0), (16.8, 11.5, 1.8, 1.0)):
        out.append(mark(rect(x, y, w, h)))
    return out


@icon("blanket-stitch", CAT, "Fabric edge with evenly spaced L-shaped stitches running along it",
      tags=["hand embroidery stitch", "edge stitch", "sewing stitch", "felt sewing", "hem finish", "needlework", "embroidery"])
def _(S):
    out = [shell(rect(2.5, 2.5, 19, 11, min(S.R, 3)))]
    for x in (5, 9.5, 14, 18.5):
        d = f"M{fmt(x)} 9.5V19" + (f"H{fmt(x + 2.6)}" if x < 18 else "")
        out.append(line(d))
    return out
