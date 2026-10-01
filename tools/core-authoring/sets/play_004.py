"""TypeIcon Core: play (batch 004) - game props, arcade and carnival rides, pranks and party games."""
from __future__ import annotations

import math

from dsl import LINE, D, I, P, ST, U, Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path

CAT = "play"


def pick(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def mk(d) -> Part:
    return Part("dot", d)


def outline(*regions, **attrs):
    return shell(path_to_d(U(*regions)), **attrs)


def cap(x0, y0, x1, y1, w=3.0):
    return ST(seg(x0, y0, x1, y1), w, "round", "round")


# --------------------------------------------------------------------------- layering (front layer first; what lies behind is cut away with a gap)

def _paint(parts, S):
    regs = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        else:
            regs.append(ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4))))
    return U(*regs)


def _sil(parts, S):
    regs = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        elif p.kind == "shell":
            regs.append(U(P(p.d), ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4)))))
        else:
            regs.append(ST(p.d, 2.0, S.cap, S.join))
    return U(*regs)


def _grow(region, g):
    if g <= 0:
        return region
    return U(region, ST(path_to_d(region), 2 * g, "round", "round"))


def _stroke_layers(S, layers, gap):
    out = list(layers[0])
    cover = _grow(_sil(layers[0], S), gap)
    for parts in layers[1:]:
        if not parts:
            continue
        vis = D(_paint(parts, S), cover)
        if abs(vis.area) > 0.01:
            out.append(solid(path_to_d(vis)))
        cover = U(cover, _grow(_sil(parts, S), gap))
    return out


def _filled_layers(layers, gap):
    result = filled_region(layers[0])
    cover = _grow(result, gap)
    for parts in layers[1:]:
        if not parts:
            continue
        f = filled_region(parts)
        result = U(result, D(f, cover))
        cover = U(cover, _grow(f, gap))
    return result


def scene(name, desc, tags, aliases=(), gap=1.5):
    """Register an icon drawn as layers: fn(S) -> [front parts, parts behind, ...]."""
    def deco(fn):
        icon(name, CAT, desc, tags=tags, aliases=aliases,
             filled=lambda: _filled_layers(fn(LINE), gap))(lambda S: _stroke_layers(S, fn(S), gap))
        return fn
    return deco


# ============================================================================ chunk 1

@icon("battering-ram", CAT, "Heavy log with a capped head hung under a small roofed frame on wheels",
      tags=["battering ram", "siege", "medieval", "castle", "war", "strategy", "gate breaker"])
def _(S):
    return [
        shell(poly([(2.5, 8.5), (12, 3.5), (21.5, 8.5)], closed=True, r=S.r)),
        line(seg(4.5, 8.5, 4.5, 17.5)),
        line(seg(19.5, 8.5, 19.5, 17.5)),
        line(seg(10, 8.5, 10, 12)),
        line(seg(14, 8.5, 14, 12)),
        shell(rect(7.5, 12, 9, 4.5, pick(S, 0.5, 2))),
        shell(circle(4.5, 19.6, 1.8)),
        shell(circle(19.5, 19.6, 1.8)),
    ]


@icon("balloon-stomp", CAT, "Balloon tied by a string to an ankle with a foot stepping down beside it",
      tags=["balloon stomp", "balloon popping", "party game", "stomp", "foot", "birthday", "pop"])
def _(S):
    bal = ellipse(8, 7.5, 4.8, 5.4) if S.name == "rounded" else poly([(8, 2), (11.5, 4.5), (12.8, 7.5), (11.5, 10.5), (8, 12.9), (4.5, 10.5), (3.2, 7.5), (4.5, 4.5)], closed=True)
    return [
        shell(bal),
        line("M8 13.5Q9 16.5 12.5 17"),
        shell(poly([(12, 13.5), (17, 13.5), (17, 18), (21.5, 19), (21.5, 21.5), (12, 21.5)], closed=True, r=S.r)),
    ]


@icon("monkey-in-the-middle", CAT, "Ball arcing high over a small center figure with arms up, between two figures on the sides",
      tags=["monkey in the middle", "piggy in the middle", "keep away", "catch", "throwing game", "playground", "ball game"])
def _(S):
    return [
        line("M4.5 8Q5.5 5 9.3 4.3"),
        line("M14.7 4.3Q18.5 5 19.5 8"),
        shell(circle(12, 4, 2.2)),
        dot(4, 11.5, 2),
        line(seg(4, 14.5, 4, 21.5)),
        dot(20, 11.5, 2),
        line(seg(20, 14.5, 20, 21.5)),
        dot(12, 14.5, 1.7),
        line(seg(12, 17.5, 12, 21.5)),
        line(poly([(8.3, 13), (12, 18), (15.7, 13)], r=S.r * 0.3)),
    ]


@icon("tile-map", CAT, "Square grid of terrain tiles: wavy water cells, plain grass cells and a few small tree cells",
      tags=["tile map", "tilemap", "terrain", "level design", "grid map", "game map", "tiles"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(12, 3, 12, 21)),
        detail(seg(3, 12, 21, 12)),
        detail("M5 7.8q1.25-2.2 2.5 0t2.5 0"),
        mk(poly([(16.5, 5.3), (14.3, 9.7), (18.7, 9.7)], closed=True)),
        dot(7.5, 16.5, 1.3),
        mk(poly([(16.5, 14.3), (14.3, 18.7), (18.7, 18.7)], closed=True)),
    ]


@icon("fog-of-war", CAT, "Square map with one corner revealed showing terrain and the rest covered by a cloudy edge",
      tags=["fog of war", "hidden map", "unexplored", "strategy game", "map reveal", "exploration", "rts"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        mk(poly([(5, 9.5), (8, 5.5), (11, 9.5)], closed=True)),
        detail("M13.5 3.2A2.4 2.4 0 0 1 13.5 8A2.4 2.4 0 0 1 10 12.2A2.4 2.4 0 0 1 5.5 12.4A2.4 2.4 0 0 1 3 14"),
        dot(16.5, 15, 1.4),
        dot(10.5, 18, 1.4),
    ]


@icon("mana-orb", CAT, "Round glass globe filled halfway with liquid and a small highlight glint on the glass",
      tags=["mana", "mana orb", "potion globe", "magic", "rpg", "resource bar", "energy orb"])
def _(S):
    return [
        shell(circle(12, 9.8, 7.8)),
        detail("M5 11.5q1.75-2 3.5 0t3.5 0t3.5 0t3.5 0"),
        mk(circle(9.5, 15, 1.1)),
        mk(circle(14.5, 14.4, 1.0)),
        detail("M8.4 7.6Q9.2 6 10.8 5.4"),
        shell(poly([(7.5, 21), (9.5, 17.8), (14.5, 17.8), (16.5, 21)], closed=True, r=S.r * 0.5)),
    ]


@icon("pull-lever", CAT, "Floor lever with a ball knob tilted to one side on a small base plate",
      tags=["lever", "pull lever", "switch", "dungeon puzzle", "handle", "trigger", "mechanism"])
def _(S):
    return [
        shell(poly([(3.5, 21), (6, 17.5), (18, 17.5), (20.5, 21)], closed=True, r=S.r * 0.6)),
        line(seg(10.5, 17.5, 16.3, 8.5)),
        shell(circle(17.6, 6, 2.6)),
        line("M5.5 13.5Q5.5 9.5 8.5 7", ),
    ]


@icon("jump-pad", CAT, "Flat round pad on a coiled spring with an upward arrow above it",
      tags=["jump pad", "bounce pad", "spring", "trampoline", "launch pad", "platformer", "boost"])
def _(S):
    return [
        line(seg(12, 6.2, 12, 3)),
        line(poly([(8.8, 6), (12, 2.8), (15.2, 6)], r=S.r * 0.6)),
        shell(rect(4, 9, 16, 3.2, pick(S, 0.5, 1.6))),
        line(poly([(8, 12.5), (16, 15), (8, 17.5), (16, 20)], r=S.r * 0.4)),
    ]


@icon("component-organizer", CAT, "Open box insert with square compartments holding small tokens and cubes",
      tags=["component organizer", "game box insert", "tray", "tokens", "board game", "storage", "sorting tray"])
def _(S):
    return [
        shell(rect(3, 4, 18, 16, S.R)),
        detail(seg(12, 4, 12, 20)),
        detail(seg(3, 12, 12, 12)),
        dot(7.5, 8.2, 1.5),
        sq(6, 14.5, 3, 3, 0.4),
        dot(16.5, 8.5, 1.5),
        sq(15, 13.8, 3, 3, 0.4),
    ]


@icon("token-punchboard", CAT, "Cardboard sheet with round and square tokens punched out and one token popping free",
      tags=["punchboard", "punch board", "tokens", "cardboard", "board game", "components", "counters"])
def _(S):
    return [
        shell(poly([(3, 3), (21, 3), (21, 11), (11, 11), (11, 21), (3, 21)], closed=True, r=S.r)),
        detail(circle(7, 7, 1.6)),
        detail(rect(14, 5.8, 4, 2.6, 0.4)),
        detail(rect(5.5, 14.5, 3, 3, 0.4)),
        shell(circle(17, 17, 3)),
    ]


@icon("linking-rings", CAT, "Three large metal rings linked together, the classic magic trick rings",
      tags=["linking rings", "magic trick", "rings", "chain", "magician", "interlocked", "illusion"],
      filled=lambda: U(*[ST(circle(cx, cy, 5), 3.0, "butt", "miter") for cx, cy in [(8.5, 9), (15.5, 9), (12, 15.2)]]))
def _(S):
    cs = [(8.5, 9), (15.5, 9), (12, 15.2)]
    if S.name == "line":
        return [shell(poly(regular(cx, cy, 5.4, 8, -67.5), closed=True)) for cx, cy in cs]
    return [shell(circle(cx, cy, 5)) for cx, cy in cs]


# ============================================================================ chunk 2

@icon("capsule-toy", CAT, "Round two tone plastic capsule split across the middle with a small toy peeking out",
      tags=["capsule toy", "gashapon", "gacha", "vending prize", "surprise", "toy capsule", "machine toy"])
def _(S):
    body = circle(12, 12.5, 8.5) if S.name == "rounded" else poly(regular(12, 12.5, 9.2, 8, -67.5), closed=True)
    return [
        shell(body),
        detail(seg(3.5, 12.5, 20.5, 12.5)),
        detail("M7.6 9.6Q8.4 7.3 10.6 6.4"),
        dot(12, 17, 1.8),
        dot(9.9, 15.3, 0.9),
        dot(14.1, 15.3, 0.9),
    ]


@icon("coin-operated-ride", CAT, "Small car shaped kiddie ride on a pedestal base with a coin on the front",
      tags=["coin operated ride", "kiddie ride", "mechanical ride", "arcade ride", "mall ride", "amusement", "toy car"])
def _(S):
    return [
        shell(poly([(2.5, 12), (2.5, 9.5), (6, 9), (8.5, 4.5), (15, 4.5), (18, 9), (21.5, 9.5), (21.5, 12)], closed=True, r=S.r)),
        detail(seg(12, 4.5, 12, 9)),
        shell(circle(7, 12.5, 1.9)),
        shell(circle(17, 12.5, 1.9)),
        shell(rect(7, 17.5, 10, 4, pick(S, 0.5, 1.5))),
        dot(12, 19.5, 1.0),
    ]


@icon("thumb-wrestling", CAT, "Two hands gripping fingers with both thumbs raised facing each other",
      tags=["thumb wrestling", "thumb war", "hands", "playground game", "kids game", "duel", "grip"])
def _(S):
    r = pick(S, 0.8, 2.5)
    body = outline(P(rect(3, 12.5, 18, 8.5, r)), cap(7.2, 13.5, 9, 5.5, 2.8))
    body2 = outline(P(rect(3, 12.5, 18, 8.5, r)), cap(16.8, 13.5, 15, 5.5, 2.8))
    both = shell(path_to_d(U(P(rect(3, 12.5, 18, 8.5, r)), cap(7.2, 13.5, 9, 5.5, 2.6), cap(16.8, 13.5, 15, 5.5, 2.6))))
    return [both, detail(seg(9, 16.5, 9, 21)), detail(seg(15, 16.5, 15, 21))]


@icon("start-select-buttons", CAT, "Two small slanted pill shaped buttons side by side on a controller face",
      tags=["start", "select", "start select", "controller buttons", "gamepad", "menu buttons", "retro console"])
def _(S):
    def pill(cx, cy):
        return mk(path_to_d(transform_path(P(rect(cx - 3.4, cy - 1.5, 6.8, 3, 1.5)), rotation(-28, cx, cy))))
    return [
        shell(rect(2.5, 6.5, 19, 11, pick(S, 2, 4.5))),
        pill(8, 12),
        pill(16, 12),
    ]


@icon("yut-sticks", CAT, "Four half round wooden sticks lying side by side, two flat side up and two round side up",
      tags=["yut", "yutnori", "sticks", "korean game", "throwing sticks", "traditional game", "fortune sticks"])
def _(S):
    return [
        shell(rect(3.5, 4, 3, 15, pick(S, 0.5, 1.5))),
        line(seg(10, 6.5, 10, 21)),
        shell(rect(14.5, 3, 3, 16, pick(S, 0.5, 1.5))),
        line(seg(21, 5, 21, 20)),
    ]


@icon("paddle-controller", CAT, "Small box controller with a large rotary knob and one round button on top",
      tags=["paddle controller", "rotary controller", "pong", "dial", "knob", "retro console", "arcade"])
def _(S):
    return [
        shell(rect(3, 6, 18, 13, pick(S, 2, 4))),
        detail(circle(9.5, 12.5, 3.8)),
        mk(rect(9, 9.7, 1, 2.3)),
        dot(17, 12.5, 2),
    ]


@icon("peg-drop-board", CAT, "Upright board with staggered pegs and a disc bouncing down toward slots at the bottom",
      tags=["peg board", "plinko", "drop game", "pegs", "chance game", "galton", "disc drop"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(circle(12, 6.7, 1.9)),
        dot(7.5, 10.5, 1.1),
        dot(16.5, 10.5, 1.1),
        dot(12, 13.8, 1.1),
        detail(seg(9, 16.5, 9, 21)),
        detail(seg(15, 16.5, 15, 21)),
    ]


@icon("fidget-cube", CAT, "Cube in three quarter view with a toggle switch on one face and small buttons on another",
      tags=["fidget cube", "fidget toy", "stress toy", "sensory toy", "desk toy", "clicker", "cube"])
def _(S):
    hexv = regular(12, 12, 9.5, 6, -90)
    return [
        shell(poly(hexv, closed=True, r=S.r)),
        detail(poly([hexv[4], (12, 12), hexv[1]])),
        detail(seg(12, 12, 12, 21.5)),
        mk(rect(7, 12.6, 1.6, 3.2)),
        dot(15.6, 14.2, 1.1),
        dot(15.6, 17.2, 1.1),
    ]


@icon("typing-game", CAT, "Keyboard at the bottom with letters falling from above toward it",
      tags=["typing game", "typing practice", "keyboard game", "falling letters", "type racer", "speed typing", "words per minute"])
def _(S):
    return [
        line(poly([(3.5, 9), (6.5, 3), (9.5, 9)], r=S.r * 0.3)),
        line(seg(4.8, 7, 8.2, 7)),
        line(seg(14, 3.5, 20, 3.5)),
        line(seg(17, 3.5, 17, 9)),
        shell(rect(3, 13.5, 18, 7.5, pick(S, 1.5, 3))),
        mk(rect(5.2, 15.5, 2, 2)),
        mk(rect(8.7, 15.5, 2, 2)),
        mk(rect(12.2, 15.5, 2, 2)),
        mk(rect(15.7, 15.5, 2, 2)),
    ]


@icon("river-rapids-ride", CAT, "Round inflatable raft with ring seats and a center hub riding on wavy water",
      tags=["river rapids", "raft ride", "water ride", "log flume", "theme park", "whitewater", "amusement ride"])
def _(S):
    body = circle(12, 9.3, 7) if S.name == "rounded" else poly(regular(12, 9.3, 7.6, 8, -67.5), closed=True)
    return [
        shell(body),
        dot(12, 9.3, 1.6),
        dot(15.2, 12.5, 1.0),
        dot(8.8, 12.5, 1.0),
        dot(15.2, 6.1, 1.0),
        dot(8.8, 6.1, 1.0),
        line("M2.5 20.5q2.25-2.6 4.5 0t4.5 0t4.5 0t4.5 0"),
    ]


@icon("reverse-bungee-ride", CAT, "Round seat capsule held on cords between two tall leaning towers",
      tags=["reverse bungee", "slingshot ride", "catapult ride", "thrill ride", "amusement park", "launch ride", "human slingshot"])
def _(S):
    return [
        line(seg(3.5, 21.5, 7, 3)),
        line(seg(20.5, 21.5, 17, 3)),
        line(seg(7, 4, 10.6, 13.2)),
        line(seg(17, 4, 13.4, 13.2)),
        shell(circle(12, 16, 3) if S.name == "rounded" else poly(regular(12, 16, 3.4, 8, -67.5), closed=True)),
    ]


@icon("seven-stones", CAT, "Short stack of flat stones piled on each other with a small ball rolling toward the stack",
      tags=["seven stones", "lagori", "pittu", "stone stack", "ball game", "traditional game", "tag game"])
def _(S):
    stones = [(20.5, 13), (17.3, 11), (14.1, 9), (10.9, 7.5), (7.7, 6), (4.5, 4.5)]
    return [line(seg(9 - w / 2 + 1, y, 9 + w / 2 - 1, y)) for y, w in stones] + [
        shell(circle(19, 19, 2.3)),
    ]


@icon("hanetsuki-paddle", CAT, "Rectangular wooden paddle with a short handle beside a small feathered shuttle",
      tags=["hanetsuki", "hagoita", "battledore", "shuttlecock", "new year game", "japanese game", "paddle"])
def _(S):
    return [
        shell(rect(3.5, 3, 9, 12, pick(S, 0.5, 2))),
        line(seg(8, 15, 8, 21)),
        detail(poly([(6, 12), (8, 7), (10, 12)], r=0)) if False else mk(circle(8, 9, 1.5)),
        shell(circle(17.5, 19, 1.9)),
        line(poly([(15, 12), (16.4, 17)], r=0)),
        line(poly([(20, 12), (18.6, 17)], r=0)),
        line(seg(17.5, 11, 17.5, 17)),
    ]


# ============================================================================ chunk 3

@icon("ring-and-hook-game", CAT, "Metal ring on a long string swinging in an arc toward a small hook on a wall board",
      tags=["ring and hook", "ring toss", "hook game", "swinging ring", "pub game", "string game", "wall hook"])
def _(S):
    return [
        shell(rect(14.5, 3, 6.5, 18, pick(S, 0.5, 2))),
        line(poly([(14.5, 13.5), (11.3, 13.5), (11.3, 11.3)], r=S.r * 0.3)),
        line("M4 2.5Q2.5 8 4.6 10.6"),
        shell(circle(6.3, 13.4, 2.6)),
    ]


@icon("level-editor", CAT, "Grid canvas with a few placed blocks and a small column of tile swatches beside it",
      tags=["level editor", "map editor", "level design", "tile palette", "game maker", "sandbox builder", "block placement"])
def _(S):
    return [
        shell(rect(3, 4, 12.5, 16, S.R)),
        mk(rect(5.5, 14.5, 3.5, 3.5)),
        mk(rect(9.2, 10.8, 3.5, 3.5)),
        mk(rect(9.2, 14.5, 3.5, 3.5)),
        sq(18, 4.5, 3.5, 3.5),
        sq(18, 10.3, 3.5, 3.5),
        sq(18, 16.1, 3.5, 3.5),
    ]


@icon("move-piece", CAT, "Game pawn lifted above a board space with a curved arrow toward the next space",
      tags=["move piece", "pawn", "game piece", "turn", "board game", "take turn", "token move"])
def _(S):
    return [
        shell(circle(6.5, 4.8, 2.3)),
        shell(poly([(5, 8.8), (8, 8.8), (9.3, 14), (3.7, 14)], closed=True, r=S.r * 0.6)),
        line("M11.5 5.5Q16.5 2 19.3 9"),
        solid(poly([(16.4, 8.6), (19.5, 10.6), (20.4, 7.2)], closed=True)),
        shell(rect(2.5, 16.5, 8, 4.5, pick(S, 0.5, 1.2))),
        shell(rect(13.5, 16.5, 8, 4.5, pick(S, 0.5, 1.2))),
    ]


@icon("knight-move", CAT, "Three by three board of squares with an L shaped arrow bending from one corner square",
      tags=["knight move", "chess knight", "l shaped move", "chess move", "board squares", "chess puzzle", "knight tour"])
def _(S):
    cells = [(12, 6), (18, 6), (12, 12), (18, 12), (18, 18)]
    return [
        dot(6, 6, 2.1),
        line(poly([(6, 6), (6, 18), (9, 18)], r=S.r * 2.4)),
        solid(poly([(9, 15.3), (13, 18), (9, 20.7)], closed=True)),
    ] + [mk(rect(x - 1.9, y - 1.9, 3.8, 3.8, pick(S, 0.2, 1.7))) for x, y in cells]


@icon("devil-sticks", CAT, "Center baton tilted in the air between two short hand sticks held below it",
      tags=["devil sticks", "juggling", "flower stick", "baton", "circus skill", "toy", "sticks"])
def _(S):
    bulge = path_to_d(transform_path(P(ellipse(12, 8.75, 3.3, 1.6)), rotation(19, 12, 8.75)))
    return [
        line(seg(4, 6, 20, 11.5)),
        mk(bulge),
        dot(4, 6, 1.5),
        dot(20, 11.5, 1.5),
        line(seg(5, 21, 10.3, 13)),
        line(seg(19, 21, 13.7, 13)),
    ]


@icon("hand-buzzer", CAT, "Round flat prank buzzer disc in an open palm with small zap lines around it",
      tags=["hand buzzer", "joy buzzer", "prank", "shock", "practical joke", "zap", "gag"])
def _(S):
    hand = outline(P(rect(3, 16.5, 15, 4.5, pick(S, 0.8, 2))), cap(16, 17.8, 20.5, 14.2, 2.6))
    return [
        hand,
        shell(circle(10.5, 11.6, 3.3)),
        line(poly([(18, 3), (16, 7), (19.5, 7.5), (17.5, 11)], r=0)),
        line(seg(3.5, 6, 5.3, 7.4)),
        line(seg(10.5, 3, 10.5, 4.6)),
    ]


@icon("prank-snake-can", CAT, "Open can with a coiled spring snake bursting out of the top",
      tags=["snake in a can", "prank", "jump scare", "spring snake", "joke can", "gag", "surprise"])
def _(S):
    return [
        line(poly([(12, 11), (17, 8.6), (7, 6.2), (16.5, 3.8)], r=S.r * 0.4)),
        dot(16.5, 3.8, 1.6),
        shell(rect(5.5, 11, 13, 10, pick(S, 1, 3))),
        detail(seg(5.5, 14, 18.5, 14)),
    ]


@icon("boxing-arcade-machine", CAT, "Upright cabinet with a punching ball on a swing arm and a score display above it",
      tags=["boxing machine", "punch machine", "arcade", "strength tester", "punching bag", "fairground", "score"])
def _(S):
    return [
        shell(rect(3, 3, 12, 18, pick(S, 1.5, 3))),
        mk(rect(5.5, 5.5, 7, 3.2, 0.5)),
        detail(seg(3, 14, 15, 14)),
        line(poly([(15, 10.5), (18.6, 10.5), (18.6, 12)], r=S.r * 0.4)),
        shell(circle(18.6, 15.2, 2.5)),
    ]


@icon("dice-throw", CAT, "Open hand releasing two dice that tumble through the air with curved motion",
      tags=["dice throw", "roll dice", "craps", "tabletop", "chance", "roll", "gambling"])
def _(S):
    def die(cx, cy, size, deg, pips):
        d = path_to_d(transform_path(P(rect(cx - size / 2, cy - size / 2, size, size, pick(S, 0.6, 1.4))), rotation(deg, cx, cy)))
        return [shell(d)] + [mk(path_to_d(transform_path(P(circle(cx + px, cy + py, 0.9)), rotation(deg, cx, cy)))) for px, py in pips]
    hand = outline(P(rect(2.5, 16, 7, 5, pick(S, 0.8, 2))), cap(8, 17.3, 12.5, 15.2, 2.4), cap(8, 20, 12.5, 19.5, 2.4))
    return [hand] + die(8.5, 8, 6.4, 14, [(-1.1, -1.1), (1.1, 1.1)]) + die(17, 9, 6.4, -18, [(-1.2, -1.2), (0, 0), (1.2, 1.2)]) + [
        line("M13.5 17Q17 17 19.5 14.5"),
    ]


@scene("dice-jail", "Small barred cage with a single die locked inside it.",
       ["dice jail", "locked die", "cage", "prison", "tabletop", "bad roll", "trapped"])
def _(S):
    die = [shell(rect(8.5, 8.5, 7, 7, pick(S, 0.8, 2))), dot(12, 12, 1.1)]
    cage = [shell(rect(3, 3, 18, 18, pick(S, 1.5, 4))), detail(seg(7, 3, 7, 21)), detail(seg(12, 3, 12, 21)), detail(seg(17, 3, 17, 21))]
    return [die, cage]


@icon("board-game-shelf", CAT, "Shelf unit with flat game boxes stacked horizontally in each cubby",
      tags=["board game shelf", "game storage", "game collection", "shelving", "game library", "cubby", "game boxes"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, S.R)), detail(seg(12, 3, 12, 21)), detail(seg(3, 12, 21, 12))]
    for x0 in (4.6, 13.6):
        for y0 in (4.6, 13.6):
            parts += [mk(rect(x0, y0 + 4.0, 5.8, 2.2)), mk(rect(x0 + 0.6, y0 + 1.2, 4.6, 2.2))]
    return parts


# ============================================================================ chunk 4

@icon("teleport-pad", CAT, "Flat round pad on the floor with vertical light rays rising in a column from it",
      tags=["teleport", "teleporter", "transporter pad", "warp pad", "sci-fi", "beam", "portal"])
def _(S):
    pad = ellipse(12, 18.5, 8.5, 2.6) if S.name == "rounded" else poly([(3, 18.5), (6, 16), (18, 16), (21, 18.5), (18, 21), (6, 21)], closed=True)
    return [
        shell(pad),
        line(seg(12, 3, 12, 14)),
        line(seg(7.5, 7, 7.5, 14)),
        line(seg(16.5, 7, 16.5, 14)),
    ]


@icon("card-playmat", CAT, "Long rectangular mat with an outlined card zone and a small card placed in another zone",
      tags=["playmat", "card mat", "trading card game", "card zones", "tcg", "duel mat", "game mat"])
def _(S):
    card = path_to_d(transform_path(P(rect(14.2, 9, 4, 6, pick(S, 0.4, 1))), rotation(-10, 16.2, 12)))
    return [
        shell(rect(2.5, 4.5, 19, 15, pick(S, 1.5, 3.5))),
        detail(rect(5.5, 7.5, 6, 9, pick(S, 0.4, 1.2))),
        mk(card),
    ]


@scene("weapon-rack", "Upright wooden rack holding a sword, a spear and an axe standing side by side.",
       ["weapon rack", "armory", "sword", "spear", "axe", "medieval", "rpg", "weapons"])
def _(S):
    sword = [line(seg(5, 4.5, 5, 14)), solid(poly([(5, 2.5), (6.6, 5), (3.4, 5)], closed=True)),
             line(seg(2.6, 14.6, 7.4, 14.6)), line(seg(5, 15, 5, 19.5))]
    spear = [line(seg(12, 8, 12, 21.5)), solid("M12 2.3Q14.6 5 13.6 8.4H10.4Q9.4 5 12 2.3Z")]
    axe = [line(seg(18, 3.5, 18, 21.5)), shell(poly([(18, 4), (21.4, 3), (21.4, 9.5), (18, 8.5)], closed=True, r=S.r * 0.5))]
    rack = [line(seg(2.5, 12.5, 21.5, 12.5)), line(seg(2.5, 19, 21.5, 19))]
    return [sword + spear + axe, rack]


@icon("training-dummy", CAT, "Straw stuffed dummy on a wooden post with a round head and a target on its chest",
      tags=["training dummy", "practice dummy", "target dummy", "scarecrow", "combat practice", "rpg", "dojo"])
def _(S):
    return [
        shell(circle(12, 5, 2.5)),
        line(seg(3.5, 10.5, 20.5, 10.5)),
        shell(rect(8, 11, 8, 7.5, pick(S, 0.8, 2.5))),
        dot(12, 14.7, 1.5),
        line(seg(12, 18.5, 12, 21.5)),
        line(seg(8, 21.5, 16, 21.5)),
    ]


@icon("follow-the-leader", CAT, "Row of three small figures in single file behind a front figure holding up a flag",
      tags=["follow the leader", "single file", "line up", "kids game", "parade", "march", "group game"])
def _(S):
    return [
        dot(4, 8, 1.4), line(seg(4, 10.4, 4, 13.5)),
        dot(7.9, 9.5, 1.7), line(seg(7.9, 12.3, 7.9, 16.5)),
        dot(11.9, 11, 2.0), line(seg(11.9, 14.2, 11.9, 19.5)),
        dot(16, 12.6, 2.3), line(seg(16, 16, 16, 21.5)),
        line(seg(20.5, 3, 20.5, 14)),
        solid(poly([(20.3, 3.2), (15, 5.2), (20.3, 7.2)], closed=True)),
    ]


@icon("mud-pie", CAT, "Round pie tin filled with lumpy mud and a small twig and leaf stuck on top",
      tags=["mud pie", "playing house", "outdoor play", "pretend cooking", "garden play", "kids", "mud kitchen"])
def _(S):
    return [
        shell(poly([(3, 12), (21, 12), (19, 20.5), (5, 20.5)], closed=True, r=S.r)),
        line("M4.5 11.5C4.5 7.5 8 7 9.5 9C10.5 5.8 15 5.8 15.6 9C18 8 20 9.5 19.5 11.5"),
        line(seg(13, 7.3, 16.5, 3.8)),
        solid("M16.5 3.6Q20.6 3.4 21 7.3Q16.8 7.4 16.5 3.6Z"),
    ]


@icon("cake-walk", CAT, "Ring of numbered floor squares around a cake on a small stand in the center",
      tags=["cake walk", "cakewalk", "musical squares", "carnival game", "party game", "fundraiser", "number squares"])
def _(S):
    pts = [(5, 5), (12, 5), (19, 5), (5, 12), (19, 12), (5, 19), (12, 19), (19, 19)]
    return [mk(rect(x - 2.3, y - 2.3, 4.6, 4.6, pick(S, 0.3, 1.1))) for x, y in pts] + [shell(circle(12, 12, 2.3))]
