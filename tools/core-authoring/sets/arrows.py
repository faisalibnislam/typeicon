"""TypeIcon Core: arrows & navigation.

Visual language follows the v0.1 `arrow-right`: 2 px shaft, open chevron head (`poly(..., r=S.r)`) with a
6 px spread, shaft stopping 0.5 px short of the tip. Filled draws a solid triangular head (back 4/3·h,
spread 1.25·h, tip +0.5 px) on a 3 px shaft, exactly like the v0.1 Filled arrow-right.

Directional siblings are drawn once in a base orientation and rotated / mirrored in code with an explicit
matrix per registered name.
"""
from __future__ import annotations

import math

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path

from dsl import (  # noqa: F401
    D, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    rect, regular, rotation, seg, shell, solid,
)

CAT = "arrows"
FILL = Style("filled", "butt", "miter", R=2.0, r=0.0)  # pseudo-style: parts for the Filled design
HD = 4 * math.sqrt(2)  # diagonal head: axis-aligned arms 8 px long


def isF(S) -> bool:
    return S.name == "filled"


def A(name, description, tags, aliases=()):
    """Register an arrows icon whose Filled design is built from `fn(FILL)`."""
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=lambda: filled_region(fn(FILL)))(fn)
    return deco


# --------------------------------------------------------------------------- transforms

MIRROR_X = (-1, 0, 0, 1, 24, 0)
MIRROR_Y = (1, 0, 0, -1, 0, 24)


def xd(d: str, m) -> str:
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def xparts(parts, m):
    return [Part(p.kind, xd(p.d, m), dict(p.attrs)) for p in parts]


def rot(fn, deg):
    m = rotation(deg)
    return lambda S: xparts(fn(S), m)


def mir(fn, m=MIRROR_X):
    return lambda S: xparts(fn(S), m)


# --------------------------------------------------------------------------- arrow helpers

def _u(deg):
    a = math.radians(deg)
    return math.cos(a), math.sin(a)


def _add(p, v, k=1.0):
    return (p[0] + v[0] * k, p[1] + v[1] * k)


def head_pts(tip, deg, h=6.0, sp=None):
    sp = h if sp is None else sp
    ux, uy = _u(deg)
    nx, ny = -uy, ux
    back = _add(tip, (ux, uy), -h)
    return [_add(back, (nx, ny), sp), tip, _add(back, (nx, ny), -sp)]


def heads(S, shaft_d, tips, h=6.0, sp=None, kind=line, w=3.0, solid_head=True):
    """Shaft d-string (already stopping 0.5 px short of each tip) plus open chevron heads.

    tips: [(tip_point, direction_deg), ...].  In the Filled pseudo-style (and kind=line) the heads become solid
    triangles on a `w` px shaft; details (heads inside a shell) are left to the knock-out rule.
    """
    sp = h if sp is None else sp
    if isF(S) and kind is line and solid_head:
        region = ST(shaft_d, w) if shaft_d else None
        tris = []
        for tip, deg in tips:
            ux, uy = _u(deg)
            nx, ny = -uy, ux
            tp = _add(tip, (ux, uy), 0.5)
            base = _add(tp, (ux, uy), -4 / 3 * h)
            tri = [_add(base, (nx, ny), 1.25 * sp), tp, _add(base, (nx, ny), -1.25 * sp)]
            tris.append(P(poly(tri, closed=True)))
            if region is not None:
                k = w / 2 + 0.6
                clip = [_add(base, (nx, ny), k), _add(tp, (nx, ny), k), _add(tp, (nx, ny), -k), _add(base, (nx, ny), -k)]
                region = D(region, P(poly(clip, closed=True)))
        body = U(*(([region] if region is not None else []) + tris))
        return [solid(path_to_d(body))]
    parts = [kind(shaft_d)] if shaft_d else []
    for tip, deg in tips:
        parts.append(kind(poly(head_pts(tip, deg, h, sp), r=S.r)))
    return parts


def sarrow(S, pts, h=6.0, sp=None, r=0.0, both=False, kind=line, w=3.0, solid_head=True):
    """Polyline arrow from pts[0] (tail) to pts[-1] (tip); `both` puts a head on the tail too."""
    pts = [tuple(map(float, p)) for p in pts]
    tip, prev = pts[-1], pts[-2]
    deg = math.degrees(math.atan2(tip[1] - prev[1], tip[0] - prev[0]))
    shaft = pts[:-1] + [_add(tip, _u(deg), -0.5)]
    tips = [(tip, deg)]
    if both:
        t0, n0 = pts[0], pts[1]
        deg0 = math.degrees(math.atan2(t0[1] - n0[1], t0[0] - n0[0]))
        shaft[0] = _add(t0, _u(deg0), -0.5)
        tips.append((t0, deg0))
    return heads(S, poly(shaft, r=r), tips, h, sp, kind, w, solid_head)


# =========================================================================== diagonal arrows

def _up_right(S):
    return sarrow(S, [(6, 18), (18, 6)], h=HD)


A("arrow-up-right", "Arrow pointing diagonally up and to the right.",
  ["northeast", "diagonal", "outbound", "up", "right", "trend"])(_up_right)
A("arrow-up-left", "Arrow pointing diagonally up and to the left.",
  ["northwest", "diagonal", "up", "left", "back"])(rot(_up_right, 270))
A("arrow-down-right", "Arrow pointing diagonally down and to the right.",
  ["southeast", "diagonal", "down", "right"])(rot(_up_right, 90))
A("arrow-down-left", "Arrow pointing diagonally down and to the left.",
  ["southwest", "diagonal", "down", "left", "inbound"])(rot(_up_right, 180))


# =========================================================================== double-headed

def _left_right(S):
    return sarrow(S, [(3.5, 12), (20.5, 12)], h=5, both=True)


A("arrows-left-right", "Double-headed horizontal arrow; move or resize sideways.",
  ["horizontal", "both ways", "resize", "width", "bidirectional", "east west"])(_left_right)
A("arrows-up-down", "Double-headed vertical arrow; move or resize up and down.",
  ["vertical", "both ways", "resize", "height", "bidirectional", "north south"])(rot(_left_right, 90))


# =========================================================================== big (block) arrows

def _big_right(S):
    pts = [(3.5, 9), (12, 9), (12, 4), (20, 12), (12, 20), (12, 15), (3.5, 15)]
    return [shell(poly(pts, closed=True, r=S.r))]


A("arrow-big-right", "Bold block arrow pointing right.", ["next", "forward", "right", "block", "bold", "east"])(_big_right)
A("arrow-big-down", "Bold block arrow pointing down.", ["down", "block", "bold", "south", "descend"])(rot(_big_right, 90))
A("arrow-big-left", "Bold block arrow pointing left.", ["back", "previous", "left", "block", "bold", "west"])(rot(_big_right, 180))
A("arrow-big-up", "Bold block arrow pointing up.", ["up", "block", "bold", "north", "ascend"])(rot(_big_right, 270))


# =========================================================================== arrow to a bar

def _bar_right(S):
    return sarrow(S, [(3, 12), (15.5, 12)]) + [line(seg(20, 4, 20, 20))]


A("arrow-bar-right", "Arrow pointing right against a bar; move to end.",
  ["end", "last", "right", "limit", "align right"])(_bar_right)
A("arrow-bar-down", "Arrow pointing down against a bar; move to bottom.",
  ["bottom", "end", "down", "limit", "align bottom"])(rot(_bar_right, 90))
A("arrow-bar-left", "Arrow pointing left against a bar; move to start.",
  ["start", "first", "left", "limit", "align left"])(rot(_bar_right, 180))
A("arrow-bar-up", "Arrow pointing up against a bar; move to top.",
  ["top", "start", "up", "limit", "align top"])(rot(_bar_right, 270))


# =========================================================================== arrows in containers

def _in_circle_right(S):
    return [shell(circle(12, 12, 9))] + sarrow(S, [(7.5, 12), (16, 12)], h=3.75, kind=detail)


A("arrow-circle-down", "Down arrow inside a circle.", ["down", "circle", "south", "download"])(rot(_in_circle_right, 90))
A("arrow-circle-left", "Left arrow inside a circle.", ["back", "previous", "left", "circle"])(rot(_in_circle_right, 180))
A("arrow-circle-up", "Up arrow inside a circle.", ["up", "circle", "north", "top"])(rot(_in_circle_right, 270))


def _in_square_right(S):
    return [shell(rect(3, 3, 18, 18, S.R))] + sarrow(S, [(7.5, 12), (16, 12)], h=3.75, kind=detail)


A("arrow-square-right", "Right arrow inside a square.", ["next", "forward", "right", "square", "box"])(_in_square_right)
A("arrow-square-down", "Down arrow inside a square.", ["down", "square", "box", "south"])(rot(_in_square_right, 90))
A("arrow-square-left", "Left arrow inside a square.", ["back", "previous", "left", "square", "box"])(rot(_in_square_right, 180))
A("arrow-square-up", "Up arrow inside a square.", ["up", "square", "box", "north"])(rot(_in_square_right, 270))


# =========================================================================== chevrons

def chev(S, pts, w=3.25, back=0.25):
    """Open chevron; Filled is a heavier chevron nudged `back` px away from its tip (as v0.1 chevron-right)."""
    if isF(S):
        tx, ty = pts[1]
        mx, my = (pts[0][0] + pts[2][0]) / 2, (pts[0][1] + pts[2][1]) / 2
        L = math.hypot(tx - mx, ty - my)
        dx, dy = (mx - tx) / L * back, (my - ty) / L * back
        return [solid(path_to_d(ST(poly([(x + dx, y + dy) for x, y in pts]), w)))]
    return [line(poly(pts, r=S.r))]


def _chev_right(S):
    return chev(S, [(9, 5), (16, 12), (9, 19)])


A("chevron-left", "Chevron pointing left; back or previous.", ["back", "previous", "collapse", "caret", "left"])(rot(_chev_right, 180))
A("chevron-up", "Chevron pointing up; collapse or scroll up.", ["collapse", "close", "up", "caret", "less"])(rot(_chev_right, 270))


def _chevs_right(S):
    return chev(S, [(5, 6), (11, 12), (5, 18)], w=2.75) + chev(S, [(12, 6), (18, 12), (12, 18)], w=2.75)


A("chevrons-right", "Double chevron pointing right; skip forward or last.", ["forward", "skip", "last", "fast forward", "double", "right"])(_chevs_right)
A("chevrons-down", "Double chevron pointing down; expand all or scroll to bottom.", ["expand", "bottom", "double", "down", "more"])(rot(_chevs_right, 90))
A("chevrons-left", "Double chevron pointing left; skip back or first.", ["back", "rewind", "first", "double", "left"])(rot(_chevs_right, 180))
A("chevrons-up", "Double chevron pointing up; collapse all or scroll to top.", ["collapse", "top", "double", "up", "less"])(rot(_chevs_right, 270))


def _chev_up_down(S):
    return chev(S, [(7, 9), (12, 4), (17, 9)], w=3) + chev(S, [(7, 15), (12, 20), (17, 15)], w=3)


A("chevron-up-down", "Chevrons pointing up and down; a select or sort control.",
  ["select", "dropdown", "sort", "unfold", "vertical", "picker"])(_chev_up_down)
A("chevron-left-right", "Chevrons pointing left and right; horizontal scroll or code.",
  ["horizontal", "code", "scroll", "left right", "carousel"])(rot(_chev_up_down, 90))


# =========================================================================== corner (turn) arrows

TRANSPOSE = (0, 1, 1, 0, 0, 0)


def _corner_up_left(S):
    return sarrow(S, [(20, 21), (20, 9), (4.5, 9)], r=S.r * 2)


A("corner-up-left", "Arrow that goes up and turns left.", ["turn", "left", "bend", "back", "reply"])(_corner_up_left)
A("corner-up-right", "Arrow that goes up and turns right.", ["turn", "right", "bend", "forward"])(mir(_corner_up_left))
A("corner-down-left", "Arrow that goes down and turns left; like the Return key.",
  ["turn", "left", "bend", "return", "enter", "newline"])(mir(_corner_up_left, MIRROR_Y))
A("corner-down-right", "Arrow that goes down and turns right.", ["turn", "right", "bend", "indent", "sub item"])(rot(_corner_up_left, 180))
A("corner-left-up", "Arrow that goes left and turns up.", ["turn", "up", "bend", "left"])(mir(_corner_up_left, TRANSPOSE))
A("corner-right-up", "Arrow that goes right and turns up.", ["turn", "up", "bend", "right"])(
    mir(mir(_corner_up_left, TRANSPOSE), MIRROR_X))


# =========================================================================== move / resize

@A("move", "Four-way arrows; move or reposition.", ["drag", "pan", "reposition", "arrows", "four way", "cross"])
def _(S):
    tips = [((12, 3.5), 270), ((20.5, 12), 0), ((12, 20.5), 90), ((3.5, 12), 180)]
    return heads(S, "M12 4V20M4 12H20", tips, h=3.5, w=2.75)


@A("move-diagonal", "Double-headed diagonal arrow; resize diagonally.", ["resize", "diagonal", "scale", "corner", "stretch"])
def _(S):
    return sarrow(S, [(5, 19), (19, 5)], h=5, both=True)


@A("expand", "Two arrows pointing out to opposite corners; expand or enlarge.", ["enlarge", "grow", "scale up", "open", "maximize"])
def _(S):
    h = 6 / math.sqrt(2)
    return sarrow(S, [(14, 10), (20, 4)], h=h) + sarrow(S, [(10, 14), (4, 20)], h=h)


@A("collapse", "Two arrows pointing in from opposite corners; collapse or shrink.", ["shrink", "reduce", "scale down", "close", "minimize"])
def _(S):
    h = 6 / math.sqrt(2)
    return sarrow(S, [(20.5, 3.5), (14, 10)], h=h) + sarrow(S, [(3.5, 20.5), (10, 14)], h=h)


@A("maximize", "Window with an arrow to its top-right corner; maximize.", ["window", "enlarge", "grow", "full size", "restore"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R))] + sarrow(S, [(8, 16), (16, 8)], h=3 * math.sqrt(2) * 0.75, kind=detail)


@A("minimize", "Window with an arrow to its bottom-left corner; minimize.", ["window", "shrink", "reduce", "dock", "hide"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R))] + sarrow(S, [(16, 8), (8, 16)], h=3 * math.sqrt(2) * 0.75, kind=detail)


def _brackets(S, a, b, inward=False):
    """Four corner brackets; outward corners at a/b or inward corners at a/b (b = 24 - a)."""
    if inward:
        c = [[(3, a), (a, a), (a, 3)], [(b, 3), (b, a), (21, a)], [(21, b), (b, b), (b, 21)], [(a, 21), (a, b), (3, b)]]
    else:
        c = [[(3, a), (3, 3), (a, 3)], [(b, 3), (21, 3), (21, a)], [(21, b), (21, 21), (b, 21)], [(a, 21), (3, 21), (3, b)]]
    return [line(poly(p, r=S.r)) for p in c]


@A("fullscreen", "Four corner brackets pointing outward; enter full screen.", ["full screen", "expand", "video", "enlarge", "presentation"])
def _(S):
    return _brackets(S, 9, 15)


@A("fullscreen-exit", "Four corner brackets pointing inward; leave full screen.", ["exit full screen", "shrink", "video", "reduce", "windowed"])
def _(S):
    return _brackets(S, 9, 15, inward=True)


# =========================================================================== history / rotation

def _undo(S):
    return heads(S, "M4.5 9H14.5A5.5 5.5 0 0 1 14.5 20H10", [((4, 9), 180)], h=5)


A("undo", "Hooked arrow curving back to the left; undo.", ["back", "revert", "history", "step back", "cancel"])(_undo)
A("redo", "Hooked arrow curving forward to the right; redo.", ["forward", "repeat", "history", "step forward", "again"])(mir(_undo))


def _rotate_cw(S):
    # three-quarter turn clockwise from the right, ending at the top pointing right
    return heads(S, arc(12, 13.5, 7, 0, 270), [((12.5, 6.5), 0)], h=4)


A("rotate-cw", "Three-quarter circular arrow turning clockwise; rotate right.",
  ["rotate", "clockwise", "turn right", "spin", "orientation"])(_rotate_cw)
A("rotate-ccw", "Three-quarter circular arrow turning counter-clockwise; rotate left.",
  ["rotate", "counterclockwise", "anticlockwise", "turn left", "spin", "orientation"])(mir(_rotate_cw))


def _refresh_cw(S):
    # same drawing as the v0.1 `refresh`, so the counter-clockwise sibling mirrors it exactly
    hd = [(20.5, 3.5), (20.5, 9.2), (14.8, 9.2)]
    if isF(S):
        tri = P(poly([(21.75, 2.25), (21.75, 10.45), (13.55, 10.45)], closed=True))
        return [solid(path_to_d(U(ST(arc(12, 12, 8, 25, 318), 2.75), tri)))]
    return [line(arc(12, 12, 8, 25, 315) + "L20.5 9.2"), line(poly(hd, r=S.r))]


A("refresh-ccw", "Circular arrow turning counter-clockwise; reload or sync backwards.",
  ["reload", "sync", "counterclockwise", "update", "reset", "anticlockwise"])(mir(_refresh_cw))


def _repeat_loop(S, h=3.75, top=6, bot=18):
    return (sarrow(S, [(4, 12), (4, top), (20, top)], h=h, r=S.r * 2, w=2.75)
            + sarrow(S, [(20, 12), (20, bot), (4, bot)], h=h, r=S.r * 2, w=2.75))


@A("repeat", "Two arrows chasing each other round a loop; repeat or loop playback.", ["loop", "replay", "cycle", "again", "playlist"])
def _(S):
    return _repeat_loop(S)


@A("repeat-once", "Repeat loop with a figure 1; repeat one track.", ["loop one", "repeat one", "single", "replay", "track"])
def _(S):
    one = line(poly([(10.5, 10.5), (12.5, 9), (12.5, 15)], r=S.r * 0.5), stroke_miterlimit="1.5")
    return _repeat_loop(S, h=3, top=5, bot=19) + [one]


@A("shuffle", "Two crossing curved arrows; shuffle or random order.", ["random", "mix", "shuffle play", "crossing", "playlist"])
def _(S):
    a = heads(S, "M3 6H6C11 6 13 18 18 18H20.5", [((21, 18), 0)], h=3.75, w=2.75)
    b = heads(S, "M3 18H6C11 18 13 6 18 6H20.5", [((21, 6), 0)], h=3.75, w=2.75)
    return a + b


def _swap_h(S):
    return sarrow(S, [(4, 8), (20, 8)], h=4, w=2.75) + sarrow(S, [(20, 16), (4, 16)], h=4, w=2.75)


A("swap-horizontal", "Two opposite horizontal arrows; swap or exchange.", ["exchange", "switch", "transfer", "trade", "horizontal"])(_swap_h)
A("swap-vertical", "Two opposite vertical arrows; swap or reorder.", ["exchange", "switch", "reorder", "sort", "vertical"])(rot(_swap_h, 90))


# =========================================================================== sort & trend

def _sort_asc(S):
    bars = [line(seg(14, 7, 17, 7)), line(seg(14, 12, 19, 12)), line(seg(14, 17, 21, 17))]
    return sarrow(S, [(7, 20), (7, 4)], h=4, w=2.75) + bars


A("sort-ascending", "Up arrow beside bars growing from short to long; sort ascending.",
  ["sort", "ascending", "order", "a to z", "increase", "low to high"])(_sort_asc)
A("sort-descending", "Down arrow beside bars shrinking from long to short; sort descending.",
  ["sort", "descending", "order", "z to a", "decrease", "high to low"])(mir(_sort_asc, MIRROR_Y))


def _trend_up(S):
    return sarrow(S, [(3, 17), (9, 11), (13, 15), (21, 7)], h=6 / math.sqrt(2), r=S.r)


A("trending-up", "Zigzag line rising to an arrow; upward trend.", ["growth", "increase", "rise", "stocks", "chart", "profit"])(_trend_up)
A("trending-down", "Zigzag line falling to an arrow; downward trend.", ["decline", "decrease", "fall", "stocks", "chart", "loss"])(mir(_trend_up, MIRROR_Y))


# =========================================================================== sign in / out

@A("login", "Arrow entering a door bracket; sign in.", ["sign in", "log in", "enter", "access", "account"])
def _(S):
    return [line(poly([(13, 3), (20, 3), (20, 21), (13, 21)], r=S.R / 2))] + sarrow(S, [(3, 12), (15, 12)], h=5)


@A("logout", "Arrow leaving a door bracket; sign out.", ["sign out", "log out", "exit", "leave", "account"])
def _(S):
    return [line(poly([(11, 3), (4, 3), (4, 21), (11, 21)], r=S.R / 2))] + sarrow(S, [(9, 12), (20.5, 12)], h=5)


@A("enter", "Arrow going into an open ring; enter or go in.", ["go in", "input", "inside", "join", "access"])
def _(S):
    return [line(arc(15, 12, 6, 240, 120))] + sarrow(S, [(2.5, 12), (11.5, 12)], h=4)


@A("exit", "Arrow leaving an open ring; exit or go out.", ["go out", "leave", "output", "outside", "quit"])
def _(S):
    return [line(arc(9, 12, 6, 60, 300))] + sarrow(S, [(9, 12), (20.5, 12)], h=4)


# =========================================================================== mail actions

def _reply(S):
    return heads(S, "M4 10H12C16.5 10 20 13.5 20 19", [((3.5, 10), 180)], h=5)


A("reply", "Arrow pointing back to the left with a curved tail; reply.", ["respond", "answer", "message", "mail", "back"])(_reply)
A("forward-mail", "Arrow pointing right with a curved tail; forward a message.", ["forward", "send on", "message", "mail", "share"])(mir(_reply))


@A("reply-all", "Double arrow pointing back to the left; reply to all.", ["respond all", "answer all", "message", "mail", "group"])
def _(S):
    outer = [line(poly(head_pts((3, 10), 180, 5), r=S.r))]
    return outer + heads(S, "M9.5 10H13C17 10 21 13.5 21 19", [((9, 10), 180)], h=5, solid_head=False)


# =========================================================================== multi-arrow groups

def _corner_arrows(S, inward, which=(0, 1, 2, 3)):
    """Diagonal arrows between the centre and the four corners (0 = NE, then clockwise)."""
    h = 5 / math.sqrt(2)
    out = []
    for k in which:
        sx, sy = [(1, -1), (1, 1), (-1, 1), (-1, -1)][k]
        inner, outer = (12 + 2 * sx, 12 + 2 * sy), (12 + 8.5 * sx, 12 + 8.5 * sy)
        out += sarrow(S, [outer, inner] if inward else [inner, outer], h=h, w=2.75)
    return out


@A("arrows-maximize", "Four arrows pointing out to the corners; maximize or enlarge.",
   ["maximize", "enlarge", "expand", "full size", "grow", "scale"])
def _(S):
    return _corner_arrows(S, False)


@A("arrows-minimize", "Four arrows pointing in from the corners; minimize or shrink.",
   ["minimize", "shrink", "reduce", "compress", "scale down"])
def _(S):
    return _corner_arrows(S, True)


@A("arrows-shuffle", "Two straight arrows crossing over; shuffle or swap lanes.", ["shuffle", "random", "crossing", "switch", "mix"])
def _(S):
    return (sarrow(S, [(3, 6), (7, 6), (15, 18), (21, 18)], h=3.75, r=S.r, w=2.75)
            + sarrow(S, [(3, 18), (7, 18), (15, 6), (21, 6)], h=3.75, r=S.r, w=2.75))


@A("arrows-cross", "Two diagonal arrows crossing in an X.", ["cross", "intersect", "crossing", "exchange", "x"])
def _(S):
    h = 5 / math.sqrt(2)
    return sarrow(S, [(4, 20), (20, 4)], h=h, w=2.75) + sarrow(S, [(4, 4), (20, 20)], h=h, w=2.75)


@A("arrows-diagonal", "Two parallel diagonal arrows pointing opposite ways.", ["diagonal", "opposite", "exchange", "resize", "both ways"])
def _(S):
    h = 5 / math.sqrt(2)
    return sarrow(S, [(3, 15), (15, 3)], h=h, w=2.75) + sarrow(S, [(21, 9), (9, 21)], h=h, w=2.75)


def _autofit_w(S):
    return [line(seg(3, 5, 3, 19)), line(seg(21, 5, 21, 19))] + sarrow(S, [(7.5, 12), (16.5, 12)], h=3, both=True, w=2.5)


A("arrow-autofit-width", "Double arrow between two bars; fit to width.", ["fit width", "autofit", "stretch", "horizontal", "resize"])(_autofit_w)
A("arrow-autofit-height", "Double arrow between two bars; fit to height.", ["fit height", "autofit", "stretch", "vertical", "resize"])(rot(_autofit_w, 90))


# =========================================================================== turns and curves

def _uturn_left(S):
    return heads(S, "M19 20.5V9.5A5 5 0 0 0 9 9.5V19", [((9, 19.5), 90)], h=4)


A("u-turn-left", "Arrow that goes up, turns back and comes down on the left; U-turn left.",
  ["u-turn", "turn around", "reverse", "back", "left", "road"])(_uturn_left)
A("u-turn-right", "Arrow that goes up, turns back and comes down on the right; U-turn right.",
  ["u-turn", "turn around", "reverse", "back", "right", "road"])(mir(_uturn_left))


def _curve_left(S):
    return heads(S, "M21 14A7 7 0 0 0 7 14V16.5", [((7, 17), 90)], h=4)


A("arrow-curve-left", "Arrow arching over to the left and down.", ["curve", "arc", "bend", "left", "turn", "counterclockwise"])(_curve_left)
A("arrow-curve-right", "Arrow arching over to the right and down.", ["curve", "arc", "bend", "right", "turn", "clockwise"])(mir(_curve_left))


@A("arrow-loop", "Arrow that makes a loop before continuing right.", ["loop", "cycle", "roundabout", "detour", "twist"])
def _(S):
    return heads(S, "M3 14H8.5C12 14 14 12 14 8.5A3.5 3.5 0 0 0 7 8.5C7 12 9 14 12.5 14H20", [((20.5, 14), 0)], h=4)


@A("arrow-zigzag", "Arrow that zigzags up and down before pointing up.", ["zigzag", "path", "winding", "indirect", "detour"])
def _(S):
    parts = sarrow(S, [(5, 20), (5, 10), (14, 19), (14, 4)], h=5, r=S.r)
    if not isF(S):
        parts[0].attrs["stroke_miterlimit"] = "2"  # bevel the two acute bends instead of long spikes
    return parts


@A("arrow-return", "Arrow looping back to the left along the bottom; return.", ["return", "back", "go back", "revert", "enter"])
def _(S):
    return heads(S, "M4 16H15A6 6 0 0 0 15 4H11", [((3.5, 16), 180)], h=5)


# =========================================================================== debugger steps

@A("step-into", "Arrow pointing down into a dot; debugger step into.", ["debug", "step into", "descend", "code", "breakpoint"])
def _(S):
    return sarrow(S, [(12, 2.5), (12, 11.5)], h=4.5) + [shell(circle(12, 18.5, 2.5))]


@A("step-out", "Arrow rising up away from a dot; debugger step out.", ["debug", "step out", "return", "code", "ascend"])
def _(S):
    return sarrow(S, [(12, 13), (12, 3.5)], h=4.5) + [shell(circle(12, 18.5, 2.5))]


# =========================================================================== narrow arrows and carets

def _narrow_right(S):
    return sarrow(S, [(3, 12), (20.5, 12)], h=4, w=2.5)


A("arrow-narrow-right", "Long thin arrow with a small head pointing right.", ["right", "next", "long", "thin", "east"])(_narrow_right)
A("arrow-narrow-down", "Long thin arrow with a small head pointing down.", ["down", "long", "thin", "south"])(rot(_narrow_right, 90))
A("arrow-narrow-left", "Long thin arrow with a small head pointing left.", ["left", "back", "long", "thin", "west"])(rot(_narrow_right, 180))
A("arrow-narrow-up", "Long thin arrow with a small head pointing up.", ["up", "long", "thin", "north"])(rot(_narrow_right, 270))


def _caret_up(S):
    return [shell(poly([(5, 15.5), (12, 8.5), (19, 15.5)], closed=True, r=S.r * 0.6))]


A("caret-up", "Small triangle pointing up; sort or collapse indicator.", ["triangle", "up", "sort", "collapse", "indicator"])(_caret_up)
A("caret-left", "Small triangle pointing left; back or collapse indicator.", ["triangle", "left", "back", "previous", "indicator"])(rot(_caret_up, 270))
A("caret-right", "Small triangle pointing right; next or expand indicator.", ["triangle", "right", "next", "expand", "indicator"])(rot(_caret_up, 90))
A("caret-down", "Small triangle pointing down; dropdown or sort indicator.", ["triangle", "down", "dropdown", "sort", "indicator"])(rot(_caret_up, 180))


# =========================================================================== branching paths

@A("merge", "Two paths joining into one arrow pointing up; merge.", ["join", "combine", "converge", "branch", "git"])
def _(S):
    return heads(S, "M6 21L12 14V3.5M18 21L12 14V13", [((12, 3), 270)], h=5)


@A("split", "One path splitting into two arrows; split or diverge.", ["diverge", "branch", "fork", "separate", "divide"])
def _(S):
    h = 5 / math.sqrt(2)
    return heads(S, "M12 21V12L5.354 5.354M12 12L18.646 5.354", [((5, 5), 225), ((19, 5), 315)], h=h, w=2.75)


@A("fork", "Straight arrow with a branch curving off to the right; fork in the road.",
   ["branch", "fork", "road", "diverge", "path", "junction"])
def _(S):
    return heads(S, "M7 21V4M7 17L19.146 4.854", [((7, 3.5), 270), ((19.5, 4.5), 315)], h=4, w=2.75)


@A("route", "Winding path between a start and an end point; route.", ["path", "journey", "trip", "way", "directions", "map"])
def _(S):
    return [
        shell(circle(6, 18, 2.5)), shell(circle(18, 6, 2.5)),
        line(poly([(8.5, 18), (17, 18), (17, 12), (7, 12), (7, 6), (15.5, 6)], r=S.r * 2)),
    ]


@A("direction", "Signpost with a board pointing right; directions.", ["signpost", "directions", "way", "sign", "guide"])
def _(S):
    return [shell(poly([(4, 4), (16, 4), (20, 8), (16, 12), (4, 12)], closed=True, r=S.r)), line(seg(10, 13, 10, 21))]


def _nav_pts():
    base = [(0, -8.5), (7, 8), (0, 4), (-7, 8)]
    a = math.radians(45)
    return [(12 + x * math.cos(a) - y * math.sin(a) + 1.9, 12 + x * math.sin(a) + y * math.cos(a) - 1.9) for x, y in base]


@A("navigation", "Arrowhead pointing up and to the right; navigate or current location.",
   ["location", "gps", "navigate", "compass", "heading", "pointer"])
def _(S):
    return [shell(poly(_nav_pts(), closed=True, r=S.r * 0.5))]


@A("compass-arrow", "Compass needle in a circle; bearing or explore.", ["compass", "bearing", "explore", "north", "orientation"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(poly([(16.5, 7.5), (13.6, 13.6), (7.5, 16.5), (10.4, 10.4)], closed=True, r=S.r * 0.5))]


# =========================================================================== aiming and zoom

@A("crosshair", "Circle with four crossing ticks; aim or precise position.", ["aim", "precision", "position", "gps", "locate", "sight"])
def _(S):
    ticks = [seg(12, 2, 12, 8), seg(22, 12, 16, 12), seg(12, 22, 12, 16), seg(2, 12, 8, 12)]
    return [line(circle(12, 12, 7))] + [line(t) for t in ticks]


@A("target", "Bullseye of two rings and a centre dot; goal or target.", ["goal", "bullseye", "aim", "objective", "focus"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(circle(12, 12, 5)), dot(12, 12, 1.5 if S.name == "line" else 2)]


@A("focus", "Corner brackets around a centre dot; focus or scan.", ["focus", "scan", "frame", "autofocus", "camera", "center"])
def _(S):
    return _brackets(S, 8, 16) + [shell(circle(12, 12, 3))]


def _lens(S, plus):
    parts = [shell(circle(10.5, 10.5, 6.5)), line(seg(15.4, 15.4, 21, 21)), detail(seg(7.5, 10.5, 13.5, 10.5))]
    if plus:
        parts.append(detail(seg(10.5, 7.5, 10.5, 13.5)))
    return parts


A("zoom-in", "Magnifying glass with a plus; zoom in.", ["magnify", "enlarge", "zoom", "plus", "bigger"])(lambda S: _lens(S, True))
A("zoom-out", "Magnifying glass with a minus; zoom out.", ["reduce", "shrink", "zoom", "minus", "smaller"])(lambda S: _lens(S, False))


# =========================================================================== handles and cursors

def _drag_h(S):
    return (chev(S, [(7.5, 8), (3.5, 12), (7.5, 16)], w=2.75, back=0) + chev(S, [(16.5, 8), (20.5, 12), (16.5, 16)], w=2.75, back=0)
            + [line(seg(12, 5, 12, 19))])


A("drag-horizontal", "Split handle with arrows left and right; drag sideways.", ["drag", "resize", "splitter", "handle", "horizontal"])(_drag_h)
A("drag-vertical", "Split handle with arrows up and down; drag vertically.", ["drag", "resize", "splitter", "handle", "vertical"])(rot(_drag_h, 90))


@A("pointer-hand", "Hand with the index finger pointing up; link cursor.", ["hand", "pointer", "click", "link", "finger", "tap"])
def _(S):
    return [
        shell("M9 15.5V5A2 2 0 0 1 13 5V10.5H16.5A2.5 2.5 0 0 1 19 13V16C19 18.8 16.8 21 14 21H12.8C11 21 9.6 20.3 8.4 19.1"
              "L4.8 15.5A1.5 1.5 0 0 1 7 13.4Z"),
        detail(seg(13, 10.5, 13, 14)), detail(seg(16, 10.5, 16, 13.5)),
    ]


@A("cursor-text", "I-beam text cursor; select or type text.", ["text", "i-beam", "caret", "type", "select", "input"])
def _(S):
    top = [(8.5, 4), (10.5, 4), (12, 5.5), (13.5, 4), (15.5, 4)]
    bot = [(8.5, 20), (10.5, 20), (12, 18.5), (13.5, 20), (15.5, 20)]
    return [line(poly(top, r=S.r)), line(poly(bot, r=S.r)), line(seg(12, 5.5, 12, 18.5))]


@A("grab", "Closed hand gripping; grab or drag to move.", ["hand", "grab", "grip", "drag", "fist", "move"])
def _(S):
    return [
        shell("M4 9A2 2 0 0 1 8 9A2 2 0 0 1 12 9A2 2 0 0 1 16 9A2 2 0 0 1 20 9V14C20 17.9 16.9 21 13 21H11C7.1 21 4 17.9 4 14Z"),
        detail(seg(8, 9, 8, 12)), detail(seg(12, 9, 12, 12)), detail(seg(16, 9, 16, 12)),
        detail(seg(4, 14.5, 10.5, 14.5)),
    ]


@A("redirect", "Arrow that runs along then turns off diagonally; redirect.", ["redirect", "reroute", "divert", "forward", "detour"])
def _(S):
    return sarrow(S, [(3, 16), (10, 16), (19, 7)], h=6 / math.sqrt(2), r=S.r)
