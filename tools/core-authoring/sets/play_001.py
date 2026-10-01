"""TypeIcon Core: play, card and board games (batch 1)."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from dsl import D, I, P, ST, U
from geometry import fmt, path_to_d, polar

CAT = "play"


# --------------------------------------------------------------------------- helpers

def pick(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def sdot(d) -> Part:
    return Part("dot", d)


def _rot(p, deg, c):
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


def rrect(x, y, w, h, deg, c, rx=0.0):
    """Rectangle (optionally rounded) turned by deg about c, as a path."""
    return path_to_d(_turn(P(rect(x, y, w, h, rx)), deg, c))


def _turn(path, deg, c):
    from geometry import rotation, transform_path
    return transform_path(path, rotation(deg, c[0], c[1]))


def turn(d, deg, cx=12.0, cy=12.0):
    return path_to_d(_turn(P(d), deg, (cx, cy)))


def pts_at(pts, cx, cy, s=1.0):
    return [(cx + x * s, cy + y * s) for x, y in pts]


SPADE = [(0, -9), (7.5, -1), (7.5, 3), (5.2, 5.6), (1.4, 5.6), (3.6, 9), (-3.6, 9), (-1.4, 5.6), (-5.2, 5.6),
         (-7.5, 3), (-7.5, -1)]
HEARTP = [(0, 8.5), (-7.5, 1), (-7.5, -4), (-4.5, -7.5), (-1.8, -7), (0, -4.5), (1.8, -7), (4.5, -7.5), (7.5, -4),
          (7.5, 1)]
DIAMOND = [(0, -9), (6, 0), (0, 9), (-6, 0)]


def suit_d(kind, cx, cy, s, S):
    """Card suit centred on (cx, cy); s = 1 is 18 high. Faceted in Line, soft in Rounded."""
    r = S.r * max(s, 0.35) * 1.3
    if kind == "spade":
        return poly(pts_at(SPADE, cx, cy, s), closed=True, r=r)
    if kind == "heart":
        return poly(pts_at(HEARTP, cx, cy, s), closed=True, r=r)
    if kind == "diamond":
        return poly(pts_at(DIAMOND, cx, cy, s), closed=True, r=r * 0.6)
    # club: three lobes and a flared stem
    lobes = [(0, -4.6), (-4.6, 2.2), (4.6, 2.2)]
    rad = 4.3
    ds = []
    for x, y in lobes:
        c = (cx + x * s, cy + y * s)
        if S.name == "line":
            ds.append(poly(regular(c[0], c[1], rad * s, 8, -90 + 22.5), closed=True))
        else:
            ds.append(circle(c[0], c[1], rad * s))
    ds.append(poly(pts_at([(0, 1), (2, 6), (3.6, 9), (-3.6, 9), (-2, 6)], cx, cy, s), closed=True))
    ds.append(poly(pts_at([(-4.6, 2.2), (0, -4.6), (4.6, 2.2), (0, 3.5)], cx, cy, s), closed=True))
    return union(*ds)


def card(S, x=5, y=3, w=14, h=18):
    return shell(rect(x, y, w, h, pick(S, 1, 2)))


# ============================================================================ suits and cards

@icon("spade-suit", CAT, "Playing card spade suit symbol",
      tags=["spade", "spades", "suit", "playing card", "poker", "bridge", "cards"])
def _(S):
    return [shell(suit_d("spade", 12, 12, 1.0, S))]


@icon("club-suit", CAT, "Playing card club suit symbol",
      tags=["club", "clubs", "suit", "playing card", "poker", "bridge", "trefoil"])
def _(S):
    return [shell(suit_d("club", 12, 12, 1.0, S))]


def _suits_filled():
    from geometry import LINE
    cells = [("spade", 7.3, 7.3), ("heart", 16.7, 7.3), ("diamond", 7.3, 16.7), ("club", 16.7, 16.7)]
    return D(P(rect(2, 2, 20, 20, 3)), *[P(suit_d(k, x, y, 0.4, LINE)) for k, x, y in cells])


@icon("card-suits", CAT, "The four card suits in a two by two grid",
      tags=["suits", "spade", "heart", "diamond", "club", "playing cards", "poker"], filled=_suits_filled)
def _(S):
    return [sdot(suit_d("spade", 7, 7, 0.42, S)), sdot(suit_d("heart", 17, 7, 0.42, S)),
            sdot(suit_d("diamond", 7, 17, 0.42, S)), sdot(suit_d("club", 17, 17, 0.42, S))]


@icon("joker-card", CAT, "Playing card with a jester cap and three bells",
      tags=["joker", "jester", "wild card", "playing card", "cards", "fool"])
def _(S):
    return [card(S), line("M8.5 17H15.5"), line("M10 17Q9.3 11.5 8 13"), line("M12 17V10.5"),
            line("M14 17Q14.7 11.5 16 13"), dot(8, 14.3, 1.1), dot(12, 9, 1.2), dot(16, 14.3, 1.1)]


@icon("ace-card", CAT, "Playing card with one large spade in the middle",
      tags=["ace", "playing card", "spade", "cards", "poker", "high card"])
def _(S):
    return [card(S), sdot(suit_d("spade", 12, 13, 0.52, S)), dot(8.5, 7.3, 1.0)]


@icon("king-card", CAT, "Playing card with a crown in the middle",
      tags=["king", "playing card", "court card", "face card", "crown", "cards"])
def _(S):
    crown = poly([(8, 16), (8, 10), (10, 12.5), (12, 9), (14, 12.5), (16, 10), (16, 16)], closed=True, r=S.r * 0.4)
    return [card(S), sdot(crown), dot(8.5, 7.0, 0.0) if False else dot(9, 7, 0.9)]


@icon("queen-card", CAT, "Playing card with a pearl-tipped crown in the middle",
      tags=["queen", "playing card", "court card", "face card", "tiara", "cards"])
def _(S):
    crown = poly([(8, 16), (8, 12.5), (10, 14), (12, 11), (14, 14), (16, 12.5), (16, 16)], closed=True, r=S.r * 0.4)
    return [card(S), detail(crown), dot(8, 10.6, 1.1), dot(12, 8.8, 1.1), dot(16, 10.6, 1.1)]


@icon("jack-card", CAT, "Playing card with a feathered cap in the middle",
      tags=["jack", "knave", "playing card", "court card", "face card", "feather", "cards"])
def _(S):
    cap = "M8.5 15.5Q8 11 12 10.5Q15 10.5 15.5 15.5Z"
    feather = "M12 10.5Q13 7 16 6.5"
    return [card(S), sdot(cap), line(feather)]


@icon("wild-card", CAT, "Playing card with a circle split in four and four corner marks",
      tags=["wild card", "wild", "playing card", "any", "joker", "cards"])
def _(S):
    return [card(S), shell(circle(12, 12, 3.4)), detail(seg(12, 8.6, 12, 15.4)), detail(seg(8.6, 12, 15.4, 12)),
            dot(8.3, 6.7, 0.9), dot(15.7, 6.7, 0.9), dot(8.3, 17.3, 0.9), dot(15.7, 17.3, 0.9)]


@icon("card-back", CAT, "Face down playing card with a diamond pattern on its back",
      tags=["card back", "face down", "hidden card", "playing card", "cards", "deck"])
def _(S):
    dia = poly([(12, 7), (15, 12), (12, 17), (9, 12)], closed=True, r=S.r * 0.4)
    return [card(S), detail(dia), dot(12, 12, 1.0)]


def layered_parts(back, front, S, gap=1.5):
    """Back parts are cut away around the front silhouette (same trick as the games set)."""
    from geometry import ST as _ST
    def paint(parts):
        regs = []
        for p in parts:
            if p.kind in ("dot", "solid"):
                regs.append(P(p.d))
            else:
                regs.append(_ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4))))
        return U(*regs)

    def sil(parts):
        regs = []
        for p in parts:
            if p.kind == "shell":
                regs.append(U(P(p.d), _ST(p.d, 2.0, S.cap, S.join)))
            elif p.kind in ("dot", "solid"):
                regs.append(P(p.d))
            else:
                regs.append(_ST(p.d, 2.0, S.cap, S.join))
        return U(*regs)
    front_sil = sil(front)
    grown = U(front_sil, _ST(path_to_d(front_sil), 2 * gap, "round", "round"))
    return list(front) + [solid(path_to_d(D(paint(back), grown)))]


def layered_filled(back, front, gap=1.5):
    from dsl import filled_region, LINE
    from geometry import ST as _ST
    ff = filled_region(front)
    grown = U(ff, _ST(path_to_d(ff), 2 * gap, "round", "round"))
    return U(ff, D(filled_region(back), grown))


def two_layer(fn):
    """Helper turning fn(S) -> (back, front) into (draw, filled) for @icon."""
    def draw(S):
        back, front = fn(S)
        return layered_parts(back, front, S)

    def filled():
        from dsl import LINE
        back, front = fn(LINE)
        return layered_filled(back, front)
    return draw, filled


def layered_icon(name, desc, tags, aliases=()):
    def deco(fn):
        draw, filled = two_layer(fn)
        icon(name, CAT, desc, tags=tags, aliases=aliases, filled=filled)(draw)
        return fn
    return deco


# ============================================================================ card handling

@icon("card-deal", CAT, "A playing card flying through the air with speed lines behind it",
      tags=["deal", "dealing", "deal cards", "card", "throw card", "flick", "poker"])
def _(S):
    return [shell(rrect(9, 5, 9, 12, 25, (13.5, 11), pick(S, 1, 2))), line("M2.5 10H6.5"), line("M2.5 14H5.5"),
            line("M3.5 18H7.5"), dot(14.5, 11, 0) if False else sdot(suit_d("spade", 13.5, 11.2, 0.3, S))]


@layered_icon("draw-card", "Small deck of cards with the top card lifted off it",
              tags=["draw card", "draw", "deck", "pick up card", "take card", "cards"])
def _(S):
    back = [shell(rect(3, 11, 11, 10, pick(S, 1, 2))), detail("M3 15H14")]
    front = [shell(rrect(11, 3, 8.5, 12, 18, (15, 9), pick(S, 1, 2)))]
    return back, front


@icon("house-of-cards", CAT, "Two tiers of leaning playing cards built into a fragile tower",
      tags=["house of cards", "card tower", "fragile", "unstable", "card castle", "precarious"])
def _(S):
    return [line("M3 21L7 14L11 21"), line("M13 21L17 14L21 21"), line("M3.5 11.5H20.5"),
            line("M8.5 9.5L12 3.5L15.5 9.5")]


@icon("booster-pack", CAT, "Sealed foil card pack with crimped ends and a star",
      tags=["booster pack", "card pack", "trading cards", "foil pack", "collectible", "blind pack", "loot"])
def _(S):
    zig = poly([(6, 3), (8, 5), (10, 3), (12, 5), (14, 3), (16, 5), (18, 3), (18, 21), (16, 19), (14, 21), (12, 19),
                (10, 21), (8, 19), (6, 21)], closed=True, r=S.r * 0.5)
    pts = []
    for k in range(10):
        pts.append(polar(12, 12, 4.3 if k % 2 == 0 else 1.9, -90 + k * 36))
    return [shell(zig), sdot(poly(pts, closed=True, r=S.r * 0.3))]


@icon("card-sleeve", CAT, "Trading card sitting in a protective sleeve that wraps its lower half",
      tags=["card sleeve", "sleeve", "protect card", "trading card", "collectible", "card protector"])
def _(S):
    return [shell(rect(7, 3, 10, 14, pick(S, 1, 2))), line(poly([(3, 9), (3, 21), (21, 21), (21, 9)], r=S.r))]


@icon("card-binder", CAT, "Card collector binder page with pockets and ring hooks",
      tags=["binder", "card binder", "collection", "trading cards", "album", "pockets", "collector"])
def _(S):
    parts = [shell(rect(7, 3, 14, 18, pick(S, 1, 2)))]
    for y in (6.5, 12, 17):
        parts.append(line(seg(3, y, 9, y)))
    for x, y in ((9.7, 6), (15, 6), (9.7, 12.5), (15, 12.5)):
        parts.append(sq(x, y, 3.8, 5))
    return parts


@icon("mahjong-tile", CAT, "Upright game tile with a bamboo stalk and a thick base",
      tags=["mahjong", "mah-jong", "tile", "bamboo", "game tile", "chinese game", "majiang"])
def _(S):
    return [shell(rect(5, 2.5, 14, 19, pick(S, 1.5, 3))), detail(seg(5, 17, 19, 17)),
            sq(10.5, 5, 3, 3.5, pick(S, 0, 0.8)), sq(10.5, 10.5, 3, 3.5, pick(S, 0, 0.8))]


@icon("tile-rack", CAT, "Angled rack holding a row of letter tiles",
      tags=["tile rack", "letter tiles", "word game", "spelling", "letters", "tiles", "scrabble-style"])
def _(S):
    rack = poly([(2, 13.5), (22, 13.5), (20, 20), (4, 20)], closed=True, r=S.r * 0.6)
    return [shell(rack), sq(3, 5, 5, 5, pick(S, 0, 1)), sq(9.5, 5, 5, 5, pick(S, 0, 1)), sq(16, 5, 5, 5, pick(S, 0, 1))]


def ell_pts(cx, cy, rx, ry, a0=0, a1=360, n=12):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def ell(S, cx, cy, rx, ry):
    """Closed ellipse: faceted in Line, smooth in Rounded."""
    if S.name == "line":
        return poly(ell_pts(cx, cy, rx, ry, 0, 360, 12)[:-1], closed=True)
    return ellipse(cx, cy, rx, ry)


def ell_arc(S, cx, cy, rx, ry, a0, a1):
    """Open elliptical arc (angles clockwise on screen, 0 = right)."""
    if S.name == "line":
        return poly(ell_pts(cx, cy, rx, ry, a0, a1, max(2, round((a1 - a0) / 30))))
    p0 = (cx + rx * math.cos(math.radians(a0)), cy + ry * math.sin(math.radians(a0)))
    p1 = (cx + rx * math.cos(math.radians(a1)), cy + ry * math.sin(math.radians(a1)))
    return f"M{fmt(p0[0])} {fmt(p0[1])}A{fmt(rx)} {fmt(ry)} 0 {1 if a1 - a0 > 180 else 0} 1 {fmt(p1[0])} {fmt(p1[1])}"


# ============================================================================ boards

@icon("score-pad", CAT, "Spiral-topped notepad with two score columns and tally dots",
      tags=["score pad", "scorecard", "score sheet", "scoring", "tally", "notepad", "game night", "keep score"])
def _(S):
    parts = [shell(rect(4, 5, 16, 16, pick(S, 1, 2))), line(seg(8, 3, 8, 7)), line(seg(12, 3, 12, 7)),
             line(seg(16, 3, 16, 7)), detail(seg(12, 10, 12, 21))]
    for y in (12.5, 16.5):
        parts.append(dot(8, y, 1.1))
        parts.append(dot(16, y, 1.1))
    return parts


@icon("chess-board", CAT, "Square board with a checker pattern of alternating squares",
      tags=["chess board", "chessboard", "checkerboard", "draughts", "checkers", "board game", "squares"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, pick(S, 1, 3)))]
    for x, y in ((4, 4), (12, 4), (8, 8), (16, 8), (4, 12), (12, 12), (8, 16), (16, 16)):
        parts.append(sq(x, y, 4, 4))
    return parts


@icon("chess-checkmate", CAT, "Chess king toppled on its side, the cross pointing sideways",
      tags=["checkmate", "chess", "king down", "resign", "game over", "defeat", "toppled king", "chess king"])
def _(S):
    body = poly([(3, 7.5), (6.5, 7.5), (11, 10), (16, 9.5), (16, 15.5), (11, 15), (6.5, 17.5), (3, 17.5)], closed=True,
                r=S.r * 0.7)
    return [shell(body), line("M16 12.5H22"), line("M19.3 10V15"), line("M2 21H22")]


@icon("checkers-piece", CAT, "Round draughts piece seen from a low angle with a raised ring on top",
      tags=["checkers", "draughts", "game piece", "disc", "counter", "board game", "token"])
def _(S):
    return [shell(ell(S, 12, 9, 9, 5)), line(ell_arc(S, 12, 14, 9, 5, 0, 180) if False else
                                              (poly([(3, 9), (3, 14)]) )),
            line(poly([(21, 9), (21, 14)])), line(ell_arc(S, 12, 14, 9, 5, 0, 180)), detail(ell(S, 12, 9, 4.6, 1.5))]


@icon("checkers-king", CAT, "Two stacked draughts pieces with a small crown on top",
      tags=["checkers king", "draughts king", "kinged piece", "stacked discs", "crowned piece", "board game"])
def _(S):
    crown = poly([(9.5, 10.5), (9.5, 7), (11, 8.5), (12, 6.5), (13, 8.5), (14.5, 7), (14.5, 10.5)], closed=True)
    return [shell(ell(S, 12, 9, 8.5, 4.5)), line(poly([(3.5, 9), (3.5, 14)])), line(poly([(20.5, 9), (20.5, 14)])),
            line(ell_arc(S, 12, 14, 8.5, 4.5, 0, 180)), line(poly([(3.5, 14), (3.5, 18.5)])),
            line(poly([(20.5, 14), (20.5, 18.5)])), line(ell_arc(S, 12, 18.5, 8.5, 4.5, 0, 180)), sdot(crown)]


@layered_icon("go-board", "Square grid board with a black stone and a white stone on the crossings",
              tags=["go", "weiqi", "baduk", "go board", "stones", "strategy", "board game", "grid"])
def _(S):
    back = [shell(rect(3, 3, 18, 18, pick(S, 1, 3))), detail(seg(9, 4, 9, 20)), detail(seg(15, 4, 15, 20)),
            detail(seg(4, 9, 20, 9)), detail(seg(4, 15, 20, 15))]
    front = [dot(9, 9, 2.6), shell(circle(15, 15, 1.8))]
    return back, front


@icon("go-stone-bowl", CAT, "Round bowl heaped with flat stones, its domed lid beside it",
      tags=["go stones", "stone bowl", "go", "weiqi", "baduk", "bowl", "lid", "board game"])
def _(S):
    bowl = "M2 11H13C13 16.5 10.5 20 7.5 20C4.5 20 2 16.5 2 11Z"
    lid = "M15 20A3.6 3.6 0 0 1 22 20Z"
    heap = "M4 11Q4.5 6 7.5 6Q10.5 6 11 11Z"
    return [shell(bowl), shell(lid), sdot(heap)]


@icon("backgammon-board", CAT, "Open folding board with triangle points along both sides and a centre bar",
      tags=["backgammon", "board", "points", "dice game", "tables", "folding board", "board game"])
def _(S):
    parts = [shell(rect(2, 4, 20, 16, pick(S, 1, 3))), detail(seg(12, 4, 12, 20))]
    for x in (4.5, 8.5):
        parts.append(sdot(poly([(x, 5), (x + 2.6, 5), (x + 1.3, 11)], closed=True)))
        parts.append(sdot(poly([(x, 19), (x + 2.6, 19), (x + 1.3, 13)], closed=True)))
    for x in (14.9, 18.9):
        parts.append(sdot(poly([(x, 5), (x + 2.6, 5), (x + 1.3, 11)], closed=True)))
        parts.append(sdot(poly([(x, 19), (x + 2.6, 19), (x + 1.3, 13)], closed=True)))
    return parts


@icon("mancala-board", CAT, "Long rounded board with two rows of pits and an oblong store at each end",
      tags=["mancala", "kalah", "pits", "seeds", "sowing game", "board game", "store"])
def _(S):
    parts = [shell(rect(2, 6, 20, 12, pick(S, 4, 6)))]
    parts += [sdot(ellipse(5.3, 12, 1.4, 3.2)), sdot(ellipse(18.7, 12, 1.4, 3.2))]
    for x in (9, 12, 15):
        parts.append(dot(x, 10, 1.0))
        parts.append(dot(x, 14, 1.0))
    return parts


@icon("nine-mens-morris", CAT, "Nested squares joined at their midpoints with a small square in the middle",
      tags=["nine men's morris", "morris", "mill", "merels", "board game", "strategy", "squares"])
def _(S):
    r = pick(S, 0, 1.5)
    return [shell(rect(3, 3, 18, 18, pick(S, 1, 3))), detail(rect(7, 7, 10, 10, pick(S, 0, 1.5))),
            detail(seg(12, 4, 12, 10)), detail(seg(12, 14, 12, 20)), detail(seg(4, 12, 10, 12)),
            detail(seg(14, 12, 20, 12)), sq(10, 10, 4, 4, r)]


@icon("tic-tac-toe", CAT, "Hash grid with an X in one corner cell and an O in the opposite corner cell",
      tags=["tic tac toe", "noughts and crosses", "xo", "x and o", "grid game", "hash", "naughts"])
def _(S):
    return [line(seg(9, 2, 9, 22)), line(seg(15, 2, 15, 22)), line(seg(2, 9, 22, 9)), line(seg(2, 15, 22, 15)),
            line(seg(3.2, 3.2, 6.8, 6.8)), line(seg(6.8, 3.2, 3.2, 6.8)), shell(circle(19, 19, 2.1))]


@icon("four-in-a-row", CAT, "Upright grid frame on two feet with discs stacked in its columns",
      tags=["connect four", "four in a row", "drop discs", "vertical grid", "board game", "discs", "strategy"])
def _(S):
    parts = [shell(rect(3, 3, 18, 15, pick(S, 1, 2))), line(seg(6, 18, 6, 21)), line(seg(18, 18, 18, 21))]
    for x in (7.5, 12, 16.5):
        parts.append(dot(x, 14, 1.5))
    for x in (7.5, 12):
        parts.append(dot(x, 9.5, 1.5))
    return parts


@icon("dots-and-boxes", CAT, "Grid of dots joined by a few lines with one completed box filled in",
      tags=["dots and boxes", "pencil game", "paper game", "squares", "grid", "connect the dots", "boxes"])
def _(S):
    parts = [sdot(rect(4, 4, 8, 8)), line(rect(4, 4, 8, 8, pick(S, 0, 1.5))), line(seg(12, 12, 20, 12)),
             line(seg(20, 12, 20, 20))]
    for x in (4, 12, 20):
        for y in (4, 12, 20):
            parts.append(sq(x - 1.5, y - 1.5, 3, 3) if S.name == "line" else dot(x, y, 1.7))
    return parts


@icon("ludo-board", CAT, "Cross-shaped track with a square home base in each corner",
      tags=["ludo", "pachisi", "parcheesi", "home base", "race game", "board game", "cross track"])
def _(S):
    cross = poly([(9, 2), (15, 2), (15, 9), (22, 9), (22, 15), (15, 15), (15, 22), (9, 22), (9, 15), (2, 15), (2, 9),
                  (9, 9)], closed=True, r=S.r * 0.5)
    c = pick(S, 0, 1)
    return [shell(cross), sq(2.5, 2.5, 3.5, 3.5, c), sq(18, 2.5, 3.5, 3.5, c), sq(2.5, 18, 3.5, 3.5, c),
            sq(18, 18, 3.5, 3.5, c), dot(12, 12, 1.4)]


@icon("chinese-checkers", CAT, "Six-pointed star board with a ring of marbles around the centre hole",
      tags=["chinese checkers", "star board", "marbles", "hexagram", "board game", "jumping game", "holes"])
def _(S):
    pts = []
    for k in range(12):
        pts.append(polar(12, 12, 10 if k % 2 == 0 else 6, -90 + k * 30))
    parts = [shell(poly(pts, closed=True, r=S.r * 0.5))]
    parts.append(dot(12, 12, 1.3))
    for k in range(6):
        x, y = polar(12, 12, 4.4, -90 + k * 60)
        parts.append(dot(x, y, 1.0) if False else dot(x, y, 0.0 + 1.0))
    return parts


def stack_parts(groups, S, gap=1.3):
    """groups run back to front; each group is cut away around every group in front of it."""
    from geometry import ST as _ST

    def paint(parts):
        regs = []
        for p in parts:
            if p.kind in ("dot", "solid"):
                regs.append(P(p.d))
            else:
                regs.append(_ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4))))
        return U(*regs)

    def sil(parts):
        regs = []
        for p in parts:
            if p.kind == "shell":
                regs.append(U(P(p.d), _ST(p.d, 2.0, S.cap, S.join)))
            elif p.kind in ("dot", "solid"):
                regs.append(P(p.d))
            else:
                regs.append(_ST(p.d, 2.0, S.cap, S.join))
        return U(*regs)
    out = list(groups[-1])
    for i in range(len(groups) - 1):
        front = U(*[sil(g) for g in groups[i + 1:]])
        grown = U(front, _ST(path_to_d(front), 2 * gap, "round", "round"))
        out.append(solid(path_to_d(D(paint(groups[i]), grown))))
    return out


def stack_filled(groups, gap=1.3):
    from dsl import filled_region
    from geometry import ST as _ST
    regs = [filled_region(g) for g in groups]
    res = regs[-1]
    for i in range(len(groups) - 2, -1, -1):
        grown = U(res, _ST(path_to_d(res), 2 * gap, "round", "round"))
        res = U(res, D(regs[i], grown))
    return res


def stack_icon(name, desc, tags, aliases=()):
    def deco(fn):
        def draw(S):
            return stack_parts(fn(S), S)

        def filled():
            from dsl import LINE
            return stack_filled(fn(LINE))
        icon(name, CAT, desc, tags=tags, aliases=aliases, filled=filled)(draw)
        return fn
    return deco


# ============================================================================ game pieces and props

@layered_icon("board-game-box", "Game box with its lid tipped off to one side and a die pip pattern on the lid",
              tags=["board game", "game box", "boxed game", "tabletop", "game night", "lid", "games"])
def _(S):
    back = [shell(rect(3, 11, 18, 10, pick(S, 1, 2)))]
    front = [shell(rrect(5, 3, 14, 6, -9, (12, 6), pick(S, 1, 2))), dot(9, 6.7, 1.0), dot(12, 5.6, 1.0),
             dot(15, 4.5, 1.0)]
    return back, front


def _tiles_filled():
    from geometry import LINE
    ds = []
    for x, y in ((5, 2.5), (11, 2.5), (17, 2.5), (17, 9.5), (11, 9.5), (5, 9.5), (5, 16.5), (11, 16.5)):
        ds.append(P(rect(x - 1, y - 1, 6, 6, 1)))
    return U(*ds)


@icon("game-board-path", CAT, "Winding track of square spaces from a start circle to a finish star",
      tags=["game path", "board game track", "start to finish", "spaces", "race game", "path", "winding track"],
      filled=_tiles_filled)
def _(S):
    parts = [dot(6, 5, 2.4)]
    c = pick(S, 0, 0.9)
    for x, y in ((10.5, 3), (16, 3), (16, 10), (10.5, 10), (5, 10), (5, 17), (10.5, 17)):
        parts.append(sq(x, y, 4, 4, c))
    star = [polar(19, 19, 3.2 if k % 2 == 0 else 1.4, -90 + k * 36) for k in range(10)]
    parts.append(sdot(poly(star, closed=True)))
    return parts


@icon("game-spinner", CAT, "Square card with a four-section dial and a pointer pinned in the middle",
      tags=["spinner", "game spinner", "dial", "random", "chance", "board game", "arrow spinner"])
def _(S):
    tip = polar(12, 12, 4.6, -45)
    return [shell(rect(2.5, 2.5, 19, 19, pick(S, 1, 3))), detail(ell(S, 12, 12, 5.6, 5.6)),
            detail(seg(12, 6.4, 12, 17.6)), detail(seg(6.4, 12, 17.6, 12)), line(seg(12, 12, tip[0], tip[1])),
            dot(12, 12, 1.5)]


@icon("meeple", CAT, "Stubby person-shaped game token with a round head and splayed limbs",
      tags=["meeple", "token", "pawn", "worker placement", "board game", "game piece", "tabletop"])
def _(S):
    body = poly([(9.5, 9), (14.5, 9), (21.5, 11), (20, 15.5), (15.5, 14.5), (17.5, 21), (12, 18.3), (6.5, 21),
                 (8.5, 14.5), (4, 15.5), (2.5, 11)], closed=True, r=S.r * 0.8)
    return [shell(union(body, circle(12, 6, 3.2)))]


@icon("house-token", CAT, "Small pitched-roof house piece shown from the corner",
      tags=["house piece", "house token", "hotel", "property", "monopoly-style", "board game", "building piece"])
def _(S):
    outline = poly([(3, 11), (9, 5), (15, 2.5), (21, 8), (21, 18), (15, 21), (3, 21)], closed=True, r=S.r * 1.1)
    return [shell(outline), detail(poly([(3, 11), (15, 11), (21, 8)])), detail(seg(15, 11, 15, 21)),
            detail(seg(9, 5, 15, 11))]


@icon("tumbling-tower", CAT, "Tower of crisscrossed wooden blocks with one block pushed out of the middle",
      tags=["tumbling tower", "block tower", "jenga-style", "wooden blocks", "stack game", "balance", "party game"])
def _(S):
    sil = poly([(5, 3), (19, 3), (19, 7.5), (22, 7.5), (22, 12), (19, 12), (19, 21), (5, 21), (5, 12), (8, 12),
                (8, 7.5), (5, 7.5)], closed=True, r=S.r * 0.4)
    return [shell(sil), detail(seg(8, 7.5, 19, 7.5)), detail(seg(8, 12, 19, 12)), detail(seg(5, 16.5, 19, 16.5)),
            detail(seg(10, 3, 10, 7.5)), detail(seg(14, 3, 14, 7.5)), detail(seg(10, 12, 10, 16.5)),
            detail(seg(14, 12, 14, 16.5))]


@icon("domino-tile", CAT, "Upright domino split in two halves with dots on each side",
      tags=["domino", "dominoes", "tile", "pips", "dots", "game piece", "tabletop"])
def _(S):
    return [shell(rect(6, 2, 12, 20, pick(S, 1.5, 3))), detail(seg(6, 12, 18, 12)), dot(9.5, 6.5, 1.3),
            dot(14.5, 6.5, 1.3), dot(9.5, 15.5, 1.3), dot(14.5, 15.5, 1.3), dot(12, 18.5, 1.3)]


@stack_icon("domino-chain", "Row of dominoes, the first ones already toppling onto the next",
            tags=["domino chain", "domino effect", "falling dominoes", "chain reaction", "cascade", "toppling"])
def _(S):
    def dom(x, ang):
        return shell(rrect(x, 7, 4.4, 13.5, ang, (x + 4.4, 20.5), pick(S, 0.6, 1.4)))
    return [[dom(2, 62)], [dom(9.5, 32)], [dom(17, 0)]]


@icon("tetromino", CAT, "T-shaped puzzle block made of four squares",
      tags=["tetromino", "tetris-style", "puzzle block", "falling blocks", "t block", "video game", "squares"])
def _(S):
    t = poly([(3, 6), (21, 6), (21, 12), (15, 12), (15, 18), (9, 18), (9, 12), (3, 12)], closed=True, r=S.r * 0.5)
    return [shell(t), detail(seg(9, 6, 9, 12)), detail(seg(15, 6, 15, 12)), detail(seg(9, 12, 15, 12))]


@icon("shogi-piece", CAT, "Flat five-sided wedge piece pointing up with a mark on its face",
      tags=["shogi", "japanese chess", "wedge piece", "game piece", "board game", "strategy", "tile"])
def _(S):
    w = poly([(12, 2.5), (18.5, 7), (20, 21), (4, 21), (5.5, 7)], closed=True, r=S.r * 0.6)
    return [shell(w), detail(seg(12, 9, 12, 16.5)), detail(seg(10.3, 11.7, 13.7, 11.7)), detail(seg(8.5, 16.5, 15.5, 16.5))]


@icon("xiangqi-piece", CAT, "Round flat game piece with a double ring border and a cross mark",
      tags=["xiangqi", "chinese chess", "round piece", "disc", "board game", "strategy", "counter"])
def _(S):
    def ring(r):
        return poly(regular(12, 12, r, 16), closed=True) if S.name == "line" else circle(12, 12, r)
    return [shell(ring(9)), detail(ring(5.4)), detail(seg(9.8, 12, 14.2, 12)), detail(seg(12, 9.8, 12, 14.2))]


@icon("reversi", CAT, "Round disc half dark and half light with a curved flip arrow",
      tags=["reversi", "othello-style", "flip", "disc", "two sided", "black and white", "board game"])
def _(S):
    half = "M11 6.5A6.5 6.5 0 0 0 11 19.5Z"
    ang0, ang1 = -80, -15
    a = polar(11, 13, 9.2, ang0)
    b = polar(11, 13, 9.2, ang1)
    arc_d = f"M{fmt(a[0])} {fmt(a[1])}A9.2 9.2 0 0 1 {fmt(b[0])} {fmt(b[1])}"
    head = poly([(b[0] - 3.2, b[1] - 0.5), (b[0], b[1]), (b[0] + 0.6, b[1] - 3.4)], r=0)
    return [shell(circle(11, 13, 6.5)), Part("dot", half), line(arc_d), line(head)]


@icon("tower-of-hanoi", CAT, "Base with three rods and a stack of shrinking discs on the left rod",
      tags=["tower of hanoi", "hanoi", "discs", "rods", "puzzle", "logic puzzle", "stack"])
def _(S):
    c = pick(S, 0, 0.9)
    return [sq(2, 19, 20, 2.5, c), line(seg(6, 4.5, 6, 19)), line(seg(12, 4.5, 12, 19)), line(seg(18, 4.5, 18, 19)),
            sq(2.3, 15.8, 7.4, 2.6, c), sq(3.3, 12.2, 5.4, 2.6, c), sq(4.2, 8.6, 3.6, 2.6, c)]


@icon("puzzle-box", CAT, "Wooden box with a side panel slid partly out and a keyhole on the front",
      tags=["puzzle box", "secret box", "trick box", "brain teaser", "keyhole", "hidden compartment", "wooden box"])
def _(S):
    keyhole = poly([(8, 15), (6.6, 18.5), (9.4, 18.5)], closed=True)
    return [shell(rect(3, 9, 18, 12, pick(S, 1, 2.5))), line(poly([(14, 9), (14, 4), (21, 4), (21, 9)], r=S.r * 0.6)),
            dot(8, 14.3, 1.4), sdot(keyhole)]


@icon("shut-the-box", CAT, "Wooden tray with a row of flip tiles, the last one folded down",
      tags=["shut the box", "flip tiles", "dice game", "tray", "numbers", "pub game", "tiles"])
def _(S):
    parts = [shell(rect(2, 4, 20, 15, pick(S, 1, 2.5)))]
    parts += [sq(4.6, 7, 3.2, 9), sq(10.4, 7, 3.2, 9), sq(16.2, 13.5, 3.2, 2.5)]
    return parts


@icon("tafl-board", CAT, "Square board with a dot for the king in the middle and marked corner squares",
      tags=["tafl", "hnefatafl", "viking chess", "king piece", "corner squares", "board game", "strategy"])
def _(S):
    c = pick(S, 0, 0.8)
    return [shell(rect(3, 3, 18, 18, pick(S, 1, 3))), detail(seg(9, 4, 9, 20)), detail(seg(15, 4, 15, 20)),
            detail(seg(4, 9, 20, 9)), detail(seg(4, 15, 20, 15)), sq(4.5, 4.5, 3, 3, c), sq(16.5, 4.5, 3, 3, c),
            sq(4.5, 16.5, 3, 3, c), sq(16.5, 16.5, 3, 3, c), dot(12, 12, 1.7)]


@icon("carrom-board", CAT, "Square board with a pocket in each corner and small discs in the middle circle",
      tags=["carrom", "carom", "striker", "pockets", "disc game", "board game", "flick game"])
def _(S):
    parts = [shell(rect(2, 2, 20, 20, pick(S, 1, 3))), detail(ell(S, 12, 12, 5.6, 5.6))]
    for x, y in ((5.5, 5.5), (18.5, 5.5), (5.5, 18.5), (18.5, 18.5)):
        parts.append(dot(x, y, 1.6))
    for k in range(4):
        x, y = polar(12, 12, 2.3, 45 + 90 * k)
        parts.append(dot(x, y, 0.95))
    return parts


@icon("crokinole-board", CAT, "Round board with a ring of small posts around a central hole",
      tags=["crokinole", "disc flicking", "posts", "round board", "tabletop", "flick game", "board game"])
def _(S):
    outer = poly(regular(12, 12, 9, 16), closed=True) if S.name == "line" else circle(12, 12, 9)
    parts = [shell(outer)]
    for k in range(8):
        x, y = polar(12, 12, 5.6, -90 + 45 * k)
        parts.append(dot(x, y, 1.0))
    parts.append(dot(12, 12, 1.7))
    return parts


@icon("tilt-maze", CAT, "Square box maze with inner walls, a rolling ball and a knob on two sides",
      tags=["tilt maze", "labyrinth", "ball maze", "rolling ball", "knobs", "dexterity", "puzzle toy"])
def _(S):
    return [shell(rect(3, 3, 16, 16, pick(S, 1, 2))), detail(seg(8, 4, 8, 12)), detail(seg(8, 12, 14, 12)),
            detail(seg(14, 12, 14, 18)), dot(13, 7, 1.7), line(seg(19, 11, 21.5, 11)), line(seg(11, 19, 11, 21.5))]


@icon("bingo-card", CAT, "Bingo card grid with a star in the centre and a few covered cells",
      tags=["bingo", "bingo card", "numbers game", "grid", "lotto", "free space", "markers"])
def _(S):
    star = [polar(12, 12, 2.6 if k % 2 == 0 else 1.2, -90 + k * 36) for k in range(10)]
    return [shell(rect(3, 3, 18, 18, pick(S, 1, 3))), detail(seg(9, 4, 9, 20)), detail(seg(15, 4, 15, 20)),
            detail(seg(4, 9, 20, 9)), detail(seg(4, 15, 20, 15)), sdot(poly(star, closed=True)), dot(6, 6, 1.3),
            dot(18, 18, 1.3), dot(18, 6, 1.3)]


@icon("game-show-buzzer", CAT, "Big domed push button on a short base with sound marks above it",
      tags=["buzzer", "game show", "quiz buzzer", "push button", "answer button", "trivia", "contestant"])
def _(S):
    dome = (poly([(5.5, 15), (7, 11), (12, 9), (17, 11), (18.5, 15)], closed=True) if S.name == "line"
            else "M5.5 15A6.5 5.5 0 0 1 18.5 15Z")
    return [shell(rect(3, 15, 18, 6, pick(S, 1, 2.5))), shell(dome), line(seg(12, 2, 12, 4.5)),
            line(seg(5, 4.5, 6.8, 6.3)), line(seg(19, 4.5, 17.2, 6.3))]


@icon("rulebook", CAT, "Thin booklet with a die on the cover and a bullet line below",
      tags=["rulebook", "rules", "instructions", "game manual", "booklet", "how to play", "handbook"])
def _(S):
    return [shell(rect(5, 2.5, 14, 19, pick(S, 1, 2))), detail(rect(8.5, 6, 7, 6.5, pick(S, 0, 1.5))),
            dot(12, 9.2, 1.0), dot(8.6, 17, 1.0), detail(seg(11.5, 17, 15.5, 17))]


@icon("cardboard-standee", CAT, "Flat cutout figure standing upright in a small plastic stand",
      tags=["standee", "cardboard cutout", "miniature stand", "figure", "token", "tabletop", "paper figure"])
def _(S):
    body = poly([(5.5, 9.5), (18.5, 9.5), (18.5, 14), (15.5, 14), (15.5, 17.5), (8.5, 17.5), (8.5, 14), (5.5, 14)],
                closed=True, r=S.r * 0.5)
    return [shell(union(body, circle(12, 5.3, 2.7))), shell(rect(4, 18.5, 16, 3, pick(S, 0.8, 1.5)))]


@icon("sequence-memory-game", CAT, "Round toy with four quadrant buttons, one of them lit",
      tags=["memory game", "simon-style", "sequence game", "four buttons", "pattern memory", "electronic toy", "lit button"])
def _(S):
    from geometry import I as _I
    lit = path_to_d(_I(P(circle(12, 12, 7.3)), P(rect(13.6, 3, 7, 7.6))))
    circ = poly(regular(12, 12, 9, 16), closed=True) if S.name == "line" else circle(12, 12, 9)
    return [shell(circ), detail(seg(12, 3, 12, 21)), detail(seg(3, 12, 21, 12)), sdot(lit)]


# ============================================================================ polyhedral dice

@icon("dice-d4", CAT, "Four-sided die drawn as a triangle with lines to its centre point",
      tags=["d4", "four sided die", "tetrahedron", "pyramid die", "tabletop rpg", "polyhedral dice", "dungeon dice"])
def _(S):
    tri = poly([(12, 3), (21.5, 19.5), (2.5, 19.5)], closed=True, r=S.r * 0.8)
    return [shell(tri), detail(seg(12, 14, 12, 3.5)), detail(seg(12, 14, 3.5, 19)), detail(seg(12, 14, 20.5, 19))]


@icon("dice-d8", CAT, "Eight-sided die drawn as a diamond with a facet outline inside",
      tags=["d8", "eight sided die", "octahedron", "tabletop rpg", "polyhedral dice", "dungeon dice", "gem"])
def _(S):
    dia = poly([(12, 2.5), (21, 12), (12, 21.5), (3, 12)], closed=True, r=S.r * 0.8)
    return [shell(dia), detail(poly([(7.5, 12), (12, 4), (16.5, 12), (12, 20), ], closed=True))]


@icon("dice-d10", CAT, "Ten-sided die drawn as a kite with a zigzag band across the middle",
      tags=["d10", "ten sided die", "trapezohedron", "tabletop rpg", "polyhedral dice", "dungeon dice", "percentile"])
def _(S):
    kite = poly([(12, 2), (20.5, 10), (12, 22), (3.5, 10)], closed=True, r=S.r * 0.8)
    return [shell(kite), detail(poly([(3.5, 10), (8, 13), (12, 10), (16, 13), (20.5, 10)])),
            detail(seg(12, 2.5, 12, 9.5))]


@icon("dice-d12", CAT, "Twelve-sided die with a pentagon face ringed by five more faces",
      tags=["d12", "twelve sided die", "dodecahedron", "tabletop rpg", "polyhedral dice", "dungeon dice", "pentagon"])
def _(S):
    outer = poly(regular(12, 12, 9.5, 10), closed=True, r=S.r * 2.4)
    parts = [shell(outer), detail(poly(regular(12, 12, 4.6, 5), closed=True))]
    for k in range(5):
        a = polar(12, 12, 4.6, -90 + 72 * k)
        b = polar(12, 12, 9.3, -90 + 72 * k)
        parts.append(detail(seg(a[0], a[1], b[0], b[1])))
    return parts


@icon("dice-d20", CAT, "Twenty-sided die drawn as a hexagon with a triangle face in the middle",
      tags=["d20", "twenty sided die", "icosahedron", "tabletop rpg", "polyhedral dice", "dungeon dice", "critical hit"])
def _(S):
    outer = poly(regular(12, 12, 9.6, 6), closed=True, r=S.r * 0.8)
    T = [polar(12, 12, 4.4, -90 + 120 * k) for k in range(3)]
    V = [polar(12, 12, 9.4, -90 + 60 * k) for k in range(6)]
    parts = [shell(outer), detail(poly(T, closed=True))]
    for t, vs in ((0, (1, 5)), (1, (0, 2)), (2, (4, 2))):
        pass
    links = ((0, 1), (0, 5), (1, 3), (1, 1), (2, 3), (2, 5))
    for ti, vi in links:
        parts.append(detail(seg(T[ti][0], T[ti][1], V[vi][0], V[vi][1])))
    return parts


@icon("percentile-dice", CAT, "Two ten-sided dice side by side, used together to roll 1 to 100",
      tags=["percentile dice", "d100", "two d10", "tens and units", "tabletop rpg", "polyhedral dice", "hundred sided"])
def _(S):
    def kite(dx):
        k = poly([(dx + 4, 3.5), (dx + 8, 10), (dx + 4, 20.5), (dx, 10)], closed=True, r=S.r * 0.6)
        return [shell(k), detail(seg(dx + 4, 4, dx + 4, 10)), detail(poly([(dx, 10), (dx + 4, 13), (dx + 8, 10)]))]
    return kite(2) + kite(14)
