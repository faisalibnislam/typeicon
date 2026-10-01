"""TypeIcon Core: play (batch 002), dice, puzzles, arcade hardware and video game concepts."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import P, U, fmt, path_to_d, rotation, transform_path

CAT = "play"


def rot(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rbox(cx, cy, w, h, deg, r=0.0):
    """Rotated rectangle as a closed poly."""
    pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]
    return poly(rot(pts, deg, cx, cy), closed=True, r=r)


# ============================================================================ dice

@icon("die-face-one", CAT, "Die face showing one pip",
      tags=["dice", "die", "one", "single", "pip", "roll", "board game"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), dot(12, 12, 1.75)]


@icon("die-face-two", CAT, "Die face showing two pips on a diagonal",
      tags=["dice", "die", "two", "pip", "roll", "board game"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), dot(8, 8, 1.5), dot(16, 16, 1.5)]


@icon("die-face-three", CAT, "Die face showing three pips on a diagonal",
      tags=["dice", "die", "three", "pip", "roll", "board game"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), dot(8, 8, 1.5), dot(12, 12, 1.5), dot(16, 16, 1.5)]


@icon("die-face-four", CAT, "Die face showing four pips in the corners",
      tags=["dice", "die", "four", "pip", "roll", "board game"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), dot(8, 8, 1.5), dot(16, 8, 1.5), dot(8, 16, 1.5), dot(16, 16, 1.5)]


@icon("die-face-six", CAT, "Die face showing six pips in two columns",
      tags=["dice", "die", "six", "pip", "roll", "board game"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R))] + [dot(x, y, 1.4) for x in (8, 16) for y in (7.5, 12, 16.5)]


@icon("dice-pair", CAT, "Two dice, one tilted behind the other",
      tags=["dice", "pair", "craps", "roll", "gambling", "board game", "luck"])
def _(S):
    return [
        shell(rect(2.5, 12.5, 9, 9, min(S.R, 3))),
        dot(5.5, 15.5, 1.2), dot(8.5, 18.5, 1.2),
        shell(rbox(16.5, 8, 8.5, 8.5, 20, r=S.r)),
        dot(16.5, 8, 1.3),
    ]


@icon("dice-cup", CAT, "Shaker cup tipped over with two dice tumbling out",
      tags=["dice cup", "shaker", "roll", "craps", "board game", "gambling", "tumble"])
def _(S):
    body = [(3, 7), (13, 4.5), (13, 15.5), (3, 13)]
    return [
        shell(poly(body, closed=True, r=S.r)),
        shell(rbox(18.5, 6, 4.5, 4.5, 15, r=0)),
        shell(rbox(18, 15.5, 4.5, 4.5, -20, r=0)),
        detail(seg(10.5, 5.2, 10.5, 14.8)),
    ]


@icon("dice-tower", CAT, "Dice tower with a ramp inside and a tray at the base",
      tags=["dice tower", "roll", "board game", "tabletop", "ramp", "tray", "random"])
def _(S):
    return [
        shell(poly([(3, 2.5), (12, 2.5), (12, 14), (21, 14), (21, 21.5), (3, 21.5)], closed=True, r=S.r)),
        detail(seg(3, 7.5, 12, 12.5)),
        Part("dot", rbox(16.5, 17.8, 3.4, 3.4, 12)),
    ]


@icon("dice-tray", CAT, "Hexagonal dice tray seen from above with one die inside",
      tags=["dice tray", "roll", "board game", "tabletop", "hexagon", "random"])
def _(S):
    hexa = regular(12, 12, 9.5, 6, start=-90)
    inner = regular(12, 12, 6, 6, start=-90)
    return [
        shell(poly(hexa, closed=True, r=S.r * 1.5)),
        detail(poly(inner, closed=True, r=S.r)),
        Part("dot", rbox(12, 12, 4, 4, 15)),
    ]


@icon("dice-bag", CAT, "Drawstring pouch with dice peeking out of the top",
      tags=["dice bag", "pouch", "drawstring", "tabletop", "board game", "sack", "storage"])
def _(S):
    if S.name == "line":
        body = poly([(9, 9), (4.5, 16), (5.5, 21), (18.5, 21), (19.5, 16), (15, 9)], closed=True)
    else:
        body = "M9 9C5 11 3.5 14.5 4.5 18Q5.2 21 8.5 21H15.5Q18.8 21 19.5 18C20.5 14.5 19 11 15 9Z"
    return [
        shell(body),
        line(seg(8.5, 9, 15.5, 9)),
        Part("solid", rbox(9.3, 5, 4, 4, -12)),
        Part("solid", rbox(14.7, 5.3, 4, 4, 14)),
    ]


@icon("fudge-dice", CAT, "Cube with a plus sign on the front and a minus on top",
      tags=["fudge dice", "fate dice", "dice", "plus minus", "rpg", "tabletop", "roll"])
def _(S):
    return [
        shell(poly([(3, 9), (15, 9), (15, 21), (3, 21)], closed=True, r=S.r * 0.6)),
        shell(poly([(3, 9), (7, 3.5), (19, 3.5), (15, 9)], closed=True, r=S.r * 0.4)),
        shell(poly([(15, 9), (19, 3.5), (19, 15.5), (15, 21)], closed=True, r=S.r * 0.4)),
        detail(seg(6.5, 15, 11.5, 15)),
        detail(seg(9, 12.5, 9, 17.5)),
        detail(seg(9.5, 6.25, 14.5, 6.25)),
    ]


@icon("long-die", CAT, "Long stick die lying diagonally with pips on one face",
      tags=["long die", "stick die", "four sided", "dice", "tabletop", "roll", "rpg"])
def _(S):
    cx, cy = 12, 12
    return [shell(rbox(cx, cy, 8, 20, 45, r=S.r * 0.6))] + [
        dot(*rot([(cx, cy + d)], 45, cx, cy)[0], 1.2) for d in (-5.5, 0, 5.5)]


@icon("coin-flip", CAT, "Coin spinning in the air above a thumb with motion arcs",
      tags=["coin flip", "coin toss", "heads or tails", "toss", "chance", "decide", "flip a coin"])
def _(S):
    return [
        shell(ellipse(12, 8.5, 3.5, 6)),
        line(arc(12, 8.5, 9, 160, 200)),
        line(arc(12, 8.5, 9, -20, 20)),
        line("M4 18.5Q12 25 20 18.5"),
    ]


@icon("drawing-straws", CAT, "Fist holding four straws with one shorter than the rest",
      tags=["drawing straws", "short straw", "lots", "pick", "chance", "decide", "unlucky"])
def _(S):
    return [
        shell(rect(4, 13.5, 16, 8, S.R)),
        detail(seg(8.5, 17.5, 8.5, 21.5)), detail(seg(12, 17.5, 12, 21.5)), detail(seg(15.5, 17.5, 15.5, 21.5)),
        line(seg(7.5, 3, 7.5, 13.5)),
        line(seg(11.5, 3, 11.5, 13.5)),
        line(seg(15.5, 8.5, 15.5, 13.5)),
        line(seg(19.5, 3, 19.5, 13.5)),
    ]


@icon("draw-from-hat", CAT, "Upturned hat with folded paper slips, one lifted out",
      tags=["draw from hat", "raffle", "lottery", "lots", "pick a name", "random", "draw names"])
def _(S):
    hat = "M7.5 9.5V17.5H3.5Q3 21 6 21H18Q21 21 20.5 17.5H16.5V9.5"
    return [
        shell(hat),
        Part("solid", rbox(9.5, 6.5, 3.5, 6, 0)),
        shell(rbox(15.5, 5.5, 5, 6.5, 22, r=S.r * 0.5)),
    ]


# ============================================================================ puzzles

@icon("sudoku-grid", CAT, "Number grid split into boxes with a few cells marked",
      tags=["sudoku", "number puzzle", "logic puzzle", "grid", "brain teaser", "numbers", "puzzle"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
        detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15)),
        dot(6, 6, 1), dot(12, 12, 1), dot(18, 18, 1), dot(18, 6, 1),
    ]


@icon("crossword-grid", CAT, "Word grid with black blocked-out squares",
      tags=["crossword", "word puzzle", "clues", "grid", "black squares", "newspaper", "puzzle"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
        detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15)),
        Part("dot", rect(10, 10, 4, 4)), Part("dot", rect(16, 4, 4, 4)), Part("dot", rect(4, 16, 4, 4)),
    ]


@icon("nonogram-grid", CAT, "Picture grid with number clues on the top and left and some cells filled",
      tags=["nonogram", "picross", "griddler", "logic puzzle", "pixel puzzle", "clues", "puzzle"])
def _(S):
    return [
        shell(rect(9, 9, 12, 12, min(S.R, 2))),
        detail(seg(13, 9, 13, 21)), detail(seg(17, 9, 17, 21)),
        detail(seg(9, 13, 21, 13)), detail(seg(9, 17, 21, 17)),
        Part("dot", rect(10, 10, 2, 2)), Part("dot", rect(14, 14, 2, 2)), Part("dot", rect(18, 18, 2, 2)),
        line(seg(11, 3, 11, 6.5)), line(seg(15, 4.5, 15, 6.5)), line(seg(19, 3, 19, 6.5)),
        line(seg(3, 11, 6.5, 11)), line(seg(4.5, 15, 6.5, 15)), line(seg(3, 19, 6.5, 19)),
    ]


@icon("kakuro-grid", CAT, "Grid with diagonal-split clue cells and empty boxes",
      tags=["kakuro", "cross sums", "number puzzle", "logic puzzle", "clue cells", "grid", "puzzle"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
        detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15)),
        detail(seg(3, 3, 9, 9)), detail(seg(9, 3, 15, 9)), detail(seg(3, 9, 9, 15)),
    ]


@icon("mine-grid-puzzle", CAT, "Four raised tiles showing a flag, a mine and a number",
      tags=["minesweeper", "mine", "flag", "logic puzzle", "grid", "tiles", "puzzle game"])
def _(S):
    rr = min(S.R, 2)
    return [
        shell(rect(3, 3, 8.5, 8.5, rr)), shell(rect(12.5, 3, 8.5, 8.5, rr)),
        shell(rect(3, 12.5, 8.5, 8.5, rr)), shell(rect(12.5, 12.5, 8.5, 8.5, rr)),
        detail(seg(6.5, 5.5, 6.5, 9)), Part("dot", poly([(6.5, 5), (9.5, 6.25), (6.5, 7.5)], closed=True)),
        dot(16.75, 7.25, 1.6),
        detail(seg(7.25, 15, 7.25, 19)),
    ]


@icon("matchstick-puzzle", CAT, "Matchsticks forming a sum with one stick lifted and tilted",
      tags=["matchstick", "matches", "equation", "brain teaser", "logic puzzle", "move one stick", "puzzle"])
def _(S):
    parts = [line(seg(4, 11, 4, 20)), dot(4, 10, 1.6)]
    parts += [line(seg(9, 15.5, 15, 15.5)), line(seg(12, 12.5, 12, 18.5))]
    (a, b), (c, d) = rot([(18, 3), (18, 10.5)], 35, 18, 6.5)
    parts += [line(seg(a, b, c, d)), dot(a, b, 1.6)]
    return parts


@icon("twisty-pyramid", CAT, "Triangular twisting puzzle divided into smaller triangles",
      tags=["pyraminx", "pyramid puzzle", "twisty puzzle", "triangle", "speedcube", "brain teaser", "puzzle"])
def _(S):
    return [
        shell(poly([(12, 3), (21, 20), (3, 20)], closed=True, r=S.r)),
        detail(poly([(7.5, 11.5), (16.5, 11.5), (12, 20)], closed=True)),
    ]


@icon("escape-room", CAT, "Locked door with a padlock and a puzzle piece beside it",
      tags=["escape room", "locked door", "padlock", "puzzle", "mystery", "lock", "adventure"])
def _(S):
    return [
        shell(rect(3, 2.5, 13, 19, min(S.R, 3))),
        Part("dot", rect(6, 13, 7, 5.5, min(S.R, 1.5))),
        detail("M7.5 13V11Q7.5 8.5 9.5 8.5Q11.5 8.5 11.5 11V13"),
        Part("solid", rect(18, 10, 4, 4)), dot(20, 9.5, 1.3),
    ]


@icon("box-pushing-puzzle", CAT, "Figure pushing a crate toward a target marked with an X",
      tags=["sokoban", "push box", "crate", "puzzle game", "warehouse", "target", "logic puzzle"])
def _(S):
    return [
        shell(circle(4.5, 7, 2.2)),
        line(seg(4.5, 10, 4.5, 16)), line(seg(4.5, 12, 8, 12)), line(seg(4.5, 16, 3, 21)), line(seg(4.5, 16, 7, 21)),
        shell(rect(8, 8, 9, 9, min(S.R, 2))),
        line(seg(18.5, 19, 21.5, 22)), line(seg(21.5, 19, 18.5, 22)),
    ]


@icon("marble-run", CAT, "Zigzag ramp tower with a ball rolling down",
      tags=["marble run", "marble track", "ball run", "toy", "ramp", "rolling ball", "gravity"])
def _(S):
    return [
        line(seg(3, 3, 3, 21)), line(seg(21, 3, 21, 21)),
        line(seg(3, 9, 16, 12)), line(seg(21, 15, 8, 18)),
        line(seg(2, 21.5, 22, 21.5)),
        dot(7, 4.5, 2),
    ]


# ============================================================================ arcade and controller hardware

@icon("arcade-button", CAT, "Large round arcade push button in a base ring",
      tags=["arcade button", "push button", "big red button", "buzzer", "arcade", "press", "game controls"])
def _(S):
    return [
        shell(rect(3, 16, 18, 5, min(S.R, 2.5))),
        shell("M6 16C6 5.5 18 5.5 18 16Z"),
        detail("M9.5 13Q10 10 12.5 9"),
    ]


@icon("cocktail-arcade-table", CAT, "Sit-down arcade cabinet with a screen under the glass top and a joystick at each end",
      tags=["cocktail table", "arcade table", "arcade cabinet", "retro", "two player", "joystick", "arcade"])
def _(S):
    return [
        shell(poly([(5, 6.5), (19, 6.5), (22, 13), (2, 13)], closed=True, r=S.r)),
        shell(rect(4.5, 13, 15, 8.5, min(S.R, 2))),
        Part("dot", poly([(9.5, 8.5), (14.5, 8.5), (15.5, 11), (8.5, 11)], closed=True)),
        dot(5.8, 9.6, 1.1), dot(18.2, 9.6, 1.1),
    ]


@icon("pinball-machine", CAT, "Pinball machine with a backbox, sloped playfield and legs",
      tags=["pinball", "flipper", "arcade", "retro", "bumper", "ball", "machine"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 7, min(S.R, 2))),
        shell(poly([(3.5, 11), (20.5, 11), (22, 16.5), (2, 16.5)], closed=True, r=S.r * 0.6)),
        line(seg(5, 16.5, 5, 21.5)), line(seg(19, 16.5, 19, 21.5)),
        Part("dot", rect(8, 5, 8, 2.5)), dot(12, 13.8, 1),
    ]


@icon("air-hockey-table", CAT, "Air hockey table with goal gaps, a centre line, a puck and a mallet",
      tags=["air hockey", "puck", "mallet", "table game", "arcade", "goal", "rink"])
def _(S):
    return [
        line(poly([(2.5, 9), (2.5, 4.5), (21.5, 4.5), (21.5, 9)])),
        line(poly([(2.5, 15), (2.5, 19.5), (21.5, 19.5), (21.5, 15)])),
        line(seg(12, 7, 12, 17)),
        shell(circle(7.5, 12, 2.8)), dot(7.5, 12, 0.9),
        dot(17, 12, 1.8),
    ]


@icon("racing-wheel-controller", CAT, "Steering wheel game controller on a base with pedals",
      tags=["racing wheel", "steering wheel", "driving game", "sim racing", "controller", "pedals", "gaming"])
def _(S):
    return [
        shell(circle(12, 9, 7)),
        detail(seg(5, 9, 19, 9)), detail(seg(12, 9, 12, 16)),
        Part("dot", rect(10.4, 7.4, 3.2, 3.2)) if S.name == "line" else dot(12, 9, 1.8),
        line(seg(12, 16, 12, 18.5)),
        shell(rect(7, 18.5, 10, 3, 0.2 if S.name == "line" else 1.5)),
    ]


@icon("motion-wand-controller", CAT, "Slim motion controller wand with a button and a wrist strap",
      tags=["motion controller", "wand", "remote", "wrist strap", "gaming", "console", "wireless"])
def _(S):
    return [
        shell(rect(8.5, 2.5, 7, 16, S.R)),
        dot(12, 7, 1.5), Part("dot", rect(10.5, 11.5, 3, 1.6)),
        line("M12 18.5V20Q12 22 14.5 22Q19 22 19 17V14"),
    ]


@icon("vr-controller", CAT, "Hand controller with a thumbstick and a tracking ring arching over the top",
      tags=["vr controller", "virtual reality", "tracking ring", "hand controller", "thumbstick", "xr", "gaming"])
def _(S):
    return [
        shell(rbox(9, 16, 6.5, 12, 25, r=S.r * 1.5 if S.name == "rounded" else 0)),
        line(arc(14.5, 8.5, 6, 100, 400)),
        dot(9.8, 13, 1.3),
    ]


def _union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


@icon("guitar-controller", CAT, "Toy guitar game controller with fret lines on the neck and a strum bar",
      tags=["guitar controller", "rhythm game", "toy guitar", "music game", "strum", "frets", "gaming"])
def _(S):
    body = _union(circle(12, 17.5, 4.5), circle(12, 12.8, 3.3))
    neck = rot([(9.5, 2.5), (14.5, 2.5), (14.5, 11), (9.5, 11)], 45, 12, 12)
    bodyrot = path_to_d(transform_path(P(body), rotation(45, 12, 12)))
    frets = [rot([(9.5, y), (14.5, y)], 45, 12, 12) for y in (5, 7.5, 10)]
    strum = rot([(9.6, 17), (14.4, 17)], 45, 12, 12)
    return [
        shell(bodyrot),
        shell(poly(neck, closed=True, r=S.r * 0.4)),
        *[detail(seg(a[0], a[1], b[0], b[1])) for a, b in frets],
        detail(seg(strum[0][0], strum[0][1], strum[1][0], strum[1][1])),
    ]


@icon("d-pad", CAT, "Plus-shaped directional pad with an arrow on each arm",
      tags=["d-pad", "dpad", "directional pad", "cross pad", "controller", "console", "direction keys"])
def _(S):
    a, b = 3, 9  # arm half-width, arm length from centre
    cross = [(12 - a, 12 - b), (12 + a, 12 - b), (12 + a, 12 - a), (12 + b, 12 - a), (12 + b, 12 + a), (12 + a, 12 + a),
             (12 + a, 12 + b), (12 - a, 12 + b), (12 - a, 12 + a), (12 - b, 12 + a), (12 - b, 12 - a), (12 - a, 12 - a)]
    t = 1.6
    return [
        shell(poly(cross, closed=True, r=S.r * 0.8)),
        Part("dot", poly([(12, 4.6), (12 - t, 7.4), (12 + t, 7.4)], closed=True)),
        Part("dot", poly([(12, 19.4), (12 - t, 16.6), (12 + t, 16.6)], closed=True)),
        Part("dot", poly([(4.6, 12), (7.4, 12 - t), (7.4, 12 + t)], closed=True)),
        Part("dot", poly([(19.4, 12), (16.6, 12 - t), (16.6, 12 + t)], closed=True)),
    ]


@icon("action-buttons", CAT, "Four round face buttons in a diamond, each with a different mark",
      tags=["face buttons", "action buttons", "abxy", "controller", "console", "gamepad", "buttons"])
def _(S):
    r = 3.1

    def btn(cx, cy):
        if S.name == "line":
            return shell(poly(regular(cx, cy, r + 0.3, 8, start=22.5), closed=True))
        return shell(circle(cx, cy, r))
    return [
        btn(12, 5), btn(19, 12), btn(12, 19), btn(5, 12),
        Part("dot", poly([(12, 3.6), (10.7, 6), (13.3, 6)], closed=True)),
        dot(19, 12, 1.0),
        Part("dot", rect(11.1, 18.1, 1.8, 1.8)),
        Part("dot", poly([(5, 10.7), (6.3, 12), (5, 13.3), (3.7, 12)], closed=True)),
    ]


@icon("game-disc-case", CAT, "Slim game case with a spine and a disc visible in the window",
      tags=["game case", "disc case", "video game", "dvd case", "physical copy", "cartridge", "collection"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, min(S.R, 3))),
        detail(seg(8.5, 4, 8.5, 20)),
        detail(circle(14, 12, 3.3)),
        dot(14, 12, 0.9),
    ]


@icon("virtual-pet", CAT, "Egg-shaped keychain gadget with a small screen and three buttons",
      tags=["virtual pet", "digital pet", "egg", "keychain", "retro toy", "handheld", "nineties"])
def _(S):
    egg = "M12 6.5C7.5 6.5 4.5 11.5 4.5 15.5C4.5 19.5 7.5 22 12 22S19.5 19.5 19.5 15.5C19.5 11.5 16.5 6.5 12 6.5Z"
    if S.name == "line":
        egg = poly([(12, 6), (16.5, 9.5), (19.5, 15.5), (16.5, 20.5), (12, 22), (7.5, 20.5), (4.5, 15.5), (7.5, 9.5)], closed=True)
    return [
        shell(egg),
        line(circle(12, 4, 1.7)),
        Part("dot", rect(8.5, 10.5, 7, 4.5, 1)),
        dot(8.7, 18.3, 1), dot(12, 18.8, 1), dot(15.3, 18.3, 1),
    ]


@icon("racing-simulator-seat", CAT, "Bucket seat on a frame facing a steering wheel and a screen",
      tags=["racing simulator", "sim rig", "racing seat", "driving simulator", "cockpit", "sim racing", "bucket seat"])
def _(S):
    return [
        shell(poly([(3, 4), (7, 4), (8, 13), (14, 13), (14, 17.5), (3, 17.5)], closed=True, r=S.r)),
        line(seg(2, 21.5, 15, 21.5)),
        line(seg(5, 17.5, 5, 21.5)),
        shell(rect(18.5, 3, 3.5, 11, min(S.R, 1.5))),
        line(seg(20.25, 14, 20.25, 21.5)),
        line(seg(15, 12, 17, 15)),
    ]


@icon("laser-tag-vest", CAT, "Sleeveless vest with round sensor pads on the chest and shoulders",
      tags=["laser tag", "vest", "sensor", "tag game", "arena", "team game", "party"])
def _(S):
    body = poly([(7.5, 3), (10.5, 3), (12, 6), (13.5, 3), (16.5, 3), (20, 6.5), (18, 21.5), (6, 21.5), (4, 6.5)], closed=True, r=S.r)
    return [shell(body), dot(7.5, 7.5, 1.3), dot(16.5, 7.5, 1.3), dot(12, 13, 1.6), detail(seg(12, 6, 12, 10))]


@icon("coin-slot", CAT, "Coin entering the slot of an arcade coin door plate",
      tags=["coin slot", "insert coin", "coin door", "arcade", "credit", "token", "vending"])
def _(S):
    return [
        dot(12, 5.2, 2.6),
        shell(rect(5, 10.5, 14, 11, S.R)),
        Part("dot", rect(11, 13.5, 2, 5.5)),
    ]


@icon("arcade-basketball", CAT, "Arcade basketball cabinet with a hoop, backboard and balls on the ramp",
      tags=["arcade basketball", "hoops", "shooting game", "arcade", "basketball", "fairground", "carnival"])
def _(S):
    return [
        shell(rect(6.5, 2.5, 11, 6.5, min(S.R, 2))),
        line(seg(9, 10.5, 15, 10.5)),
        shell(rect(3, 13, 18, 8.5, min(S.R, 2.5))),
        dot(8, 17.2, 1.4), dot(12, 17.2, 1.4), dot(16, 17.2, 1.4),
    ]


@icon("platformer-game", CAT, "Small figure jumping between two raised block platforms",
      tags=["platformer", "jump", "side scroller", "retro game", "blocks", "video game", "level"])
def _(S):
    return [
        shell(rect(2.5, 15, 6, 6.5, min(S.R, 1.5))),
        shell(rect(15.5, 11, 6, 10.5, min(S.R, 1.5))),
        dot(12, 5.5, 2),
        line(seg(12, 9, 12, 13)), line(seg(12, 13, 10, 15.5)), line(seg(12, 13, 14, 15)),
        line(seg(9.5, 10.5, 14.5, 10.5)),
    ]


@icon("rhythm-game", CAT, "Three lanes with note circles falling toward a target line",
      tags=["rhythm game", "music game", "notes", "lanes", "beat", "tap", "dance game"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, S.R)),
        detail(seg(9, 2.5, 9, 21.5)), detail(seg(15, 2.5, 15, 21.5)),
        detail(seg(3, 17, 21, 17)),
        dot(6, 6, 1.6), dot(18, 11, 1.6), dot(12, 9, 1.6),
    ]


@icon("voxel-block", CAT, "Isometric block with a jagged grass layer across the top",
      tags=["voxel", "cube block", "sandbox game", "blocky", "minecraft style", "pixel block", "building game"])
def _(S):
    hexa = [(12, 3), (20, 7.5), (20, 16.5), (12, 21), (4, 16.5), (4, 7.5)]
    zig = [(4, 11.5), (6, 14), (8, 11.5), (10, 14), (12, 11.5), (14, 14), (16, 11.5), (18, 14), (20, 11.5)]
    return [
        shell(poly(hexa, closed=True, r=S.r * 0.6)),
        detail(poly(zig)),
        detail(seg(12, 14, 12, 21)),
    ]


@icon("tower-defense", CAT, "Small turret tower with a dashed range circle around it",
      tags=["tower defense", "turret", "range", "strategy game", "defend", "castle", "wave"])
def _(S):
    tower = [(9.5, 16.5), (9.5, 8.5), (10.8, 8.5), (10.8, 10), (13.2, 10), (13.2, 8.5), (14.5, 8.5), (14.5, 16.5)]
    return [
        shell(poly(tower, closed=True)),
        *[line(arc(12, 12, 9.5, a, a + 28)) for a in range(0, 360, 45)],
    ]


@icon("battle-royale-zone", CAT, "Map square with a dashed shrinking-zone circle and a safe circle inside",
      tags=["battle royale", "shrinking zone", "safe zone", "storm circle", "map", "last one standing", "shooter"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, S.R)),
        *[line(arc(12, 12, 6.3, a, a + 28)) for a in range(0, 360, 45)],
        dot(13.3, 10.7, 2),
    ]


@icon("moba-map", CAT, "Square map with lanes along two edges and a diagonal, and a base in opposite corners",
      tags=["moba", "lanes", "minimap", "strategy map", "base", "arena map", "team game"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        line(seg(7, 17, 17, 7)),
        dot(6.3, 17.7, 2.2), dot(17.7, 6.3, 2.2),
    ]


@icon("match-three", CAT, "Row of three matching gems above a swap between two different pieces",
      tags=["match three", "match 3", "puzzle game", "gems", "candy", "swap", "casual game"])
def _(S):
    gem = lambda cx, cy: Part("solid", poly([(cx, cy - 3.2), (cx + 3.2, cy), (cx, cy + 3.2), (cx - 3.2, cy)], closed=True, r=S.r * 0.5))
    return [
        gem(4.5, 6), gem(12, 6), gem(19.5, 6),
        gem(4.5, 17.5),
        Part("solid", circle(19.5, 17.5, 2.9)),
        line(seg(9.5, 17.5, 14.5, 17.5)),
        line(poly([(11, 15.5), (9, 17.5), (11, 19.5)])), line(poly([(13, 15.5), (15, 17.5), (13, 19.5)])),
    ]


@icon("snake-game", CAT, "Blocky snake bending through a grid frame toward a single food dot",
      tags=["snake game", "snake", "retro game", "pixel", "food", "grid", "arcade"])
def _(S):
    cells = [(0, 3), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1)]
    k = 0 if S.name == "line" else 0.8
    return [shell(rect(2.5, 2.5, 19, 19, S.R))] + [Part("dot", rect(4.5 + 4 * c, 4.5 + 4 * r, 3, 3, k)) for c, r in cells] + [dot(18, 18, 1.3)]


@icon("brick-breaker", CAT, "Rows of bricks at the top of a frame, a ball and a paddle at the bottom",
      tags=["brick breaker", "breakout", "paddle", "ball", "bricks", "retro game", "arcade"])
def _(S):
    k = 0 if S.name == "line" else 0.8
    parts = [shell(rect(2.5, 2.5, 19, 19, S.R))]
    parts += [Part("dot", rect(x, y, 4, 2.4, k)) for y in (5.5, 9) for x in (5, 10, 15)]
    parts += [dot(12, 13.8, 1.3), Part("dot", rect(8, 17, 8, 2, k))]
    return parts


@icon("endless-runner", CAT, "Running figure with speed lines behind and a hurdle ahead",
      tags=["endless runner", "runner game", "running", "hurdle", "speed", "mobile game", "sprint"])
def _(S):
    return [
        dot(11, 5, 2),
        line(poly([(10.5, 8), (9, 14)])),
        line(poly([(10, 9.5), (13.5, 11.5)])), line(poly([(10, 9.5), (6.5, 10.5)])),
        line(poly([(9, 14), (12.5, 16.5), (12.5, 21)])), line(poly([(9, 14), (5.5, 16), (4, 20)])),
        line(seg(2, 4.5, 5, 4.5)), line(seg(2, 8, 4.5, 8)),
        line(poly([(17.5, 21.5), (17.5, 16), (22, 16)])), line(seg(21.5, 16, 21.5, 21.5)),
    ]


@icon("visual-novel", CAT, "Screen with a character bust above a wide dialogue box",
      tags=["visual novel", "dialogue", "dating sim", "story game", "character", "text box", "anime game"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 18, S.R)),
        dot(12, 7.3, 2.3),
        Part("dot", poly([(8, 12.5), (8.6, 10.5), (12, 9.8), (15.4, 10.5), (16, 12.5)], closed=True, r=1)),
        detail(rect(5.5, 14.5, 13, 4, min(S.R, 1))),
    ]


@icon("city-builder-game", CAT, "Tile of ground with tall and short block buildings on it",
      tags=["city builder", "simulation game", "buildings", "skyline", "tile", "town", "management game"])
def _(S):
    tile = poly([(12, 13.5), (20.5, 17.5), (12, 21.5), (3.5, 17.5)], closed=True)
    k = 0.5 if S.name == "line" else 1.5
    t1, t2 = rect(5.5, 4, 5.5, 12, k), rect(12.5, 8, 5.5, 9, k)
    return [
        shell(path_to_d(U(P(tile), P(t1), P(t2)))),
        Part("dot", rect(7.2, 7, 2.2, 2)), Part("dot", rect(7.2, 11, 2.2, 2)), Part("dot", rect(14.2, 11.5, 2.2, 2)),
    ]


@icon("dungeon-map", CAT, "Top-down map of square rooms joined by narrow corridors",
      tags=["dungeon map", "rooms", "corridors", "roguelike", "floor plan", "rpg", "labyrinth"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 8, 7, 0 if S.name == "line" else 2.5)),
        shell(rect(13.5, 12.5, 8, 9, 0 if S.name == "line" else 2.5)),
        shell(rect(2.5, 14, 8, 7.5, 0 if S.name == "line" else 2.5)),
        line(poly([(10.5, 6), (17.5, 6), (17.5, 12.5)])),
        line(seg(6.5, 9.5, 6.5, 14)),
        line(seg(10.5, 17.75, 13.5, 17.75)),
    ]


@icon("strategy-map", CAT, "Map square with two flags and a curved movement arrow between them",
      tags=["strategy map", "campaign map", "troop movement", "flags", "war game", "route", "tactics"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, S.R)),
        line(seg(6.5, 19, 6.5, 13)), Part("dot", poly([(6.5, 13), (10.2, 14.5), (6.5, 16)], closed=True)),
        line(seg(17.5, 12, 17.5, 6)), Part("dot", poly([(17.5, 6), (14, 7.5), (17.5, 9)], closed=True)),
        detail("M10 18Q16 18 16 14.5"),
    ]


@icon("space-shooter", CAT, "Arrow-shaped ship firing shots up at a row of blocky targets",
      tags=["space shooter", "spaceship", "shoot em up", "invaders", "arcade", "retro game", "blaster"])
def _(S):
    return [
        *[Part("solid", rect(x, 3, 4, 3.5, 0 if S.name == "line" else 1)) for x in (3, 10, 17)],
        line(seg(12, 8.5, 12, 10.5)), line(seg(12, 12, 12, 14)),
        shell(poly([(12, 14.5), (17, 21.5), (12, 19.5), (7, 21.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("stealth-game", CAT, "Crouching figure behind a crate while a vision cone sweeps past",
      tags=["stealth", "sneak", "hide", "vision cone", "crate", "spy game", "tactical"])
def _(S):
    return [
        shell(poly([(3, 3), (21, 4), (19, 10)], closed=True, r=S.r * 0.6)),
        shell(rect(11, 13, 10, 8.5, min(S.R, 2))),
        dot(5.5, 13.5, 1.8),
        line(poly([(5.5, 16), (5.5, 19.5)])), line(poly([(5.5, 19.5), (8, 21.5)])), line(poly([(5.5, 19.5), (3, 21.5)])),
    ]


@icon("fighting-game", CAT, "Two health bars above two fighters facing each other",
      tags=["fighting game", "versus", "health bar", "brawler", "street fighter", "arcade", "combat"])
def _(S):
    k = 0 if S.name == "line" else 1
    def fighter(x, d):
        return [
            dot(x, 10, 1.7),
            line(seg(x, 12, x, 17)),
            line(poly([(x, 13.5), (x + 4.5 * d, 12.3)])),
            line(poly([(x, 17), (x - 2.5 * d, 21.5)])), line(poly([(x, 17), (x + 2.5 * d, 21.5)])),
        ]
    return [
        Part("solid", rect(2.5, 3, 9, 3, k)), Part("solid", rect(14.5, 3, 7, 3, k)),
        *fighter(6, 1), *fighter(18, -1),
    ]


@icon("bubble-shooter", CAT, "Small cannon aiming a dotted line at a cluster of bubbles",
      tags=["bubble shooter", "bubble pop", "cannon", "aim", "puzzle game", "casual game", "balls"])
def _(S):
    return [
        dot(5, 4.5, 2.5), dot(11, 4.5, 2.5), dot(17, 4.5, 2.5), dot(8, 10, 2.5), dot(14, 10, 2.5),
        dot(12, 13.3, 0.9), dot(12, 15.5, 0.9),
        shell(poly([(8.5, 22), (8.5, 17.8), (15.5, 17.8), (15.5, 22)], closed=True) if S.name == "line" else "M8.5 22V20Q8.5 17.8 10.5 17.8H13.5Q15.5 17.8 15.5 20V22Z"),
    ]


@icon("clicker-game", CAT, "Big round button being pressed by a pointer cursor with a plus floating up",
      tags=["clicker game", "idle game", "incremental", "tap", "click", "cursor", "button"])
def _(S):
    return [
        shell(circle(9, 10.5, 6)),
        Part("solid", poly([(12, 12), (12, 21), (14.3, 18.8), (15.8, 22), (17.8, 21), (16.3, 18), (19.5, 17.6)], closed=True, r=S.r * 0.4)),
        line(seg(19, 2.5, 19, 7.5)), line(seg(16.5, 5, 21.5, 5)),
    ]

def node(S, x, y, r):
    """Solid marker: square in Line, round in Rounded."""
    if S.name == "line":
        return Part("dot", rect(x - r * 0.9, y - r * 0.9, r * 1.8, r * 1.8))
    return dot(x, y, r)


def node_ring(S, x, y, r):
    if S.name == "line":
        return shell(rect(x - r, y - r, 2 * r, 2 * r))
    return shell(circle(x, y, r))


def _unit(dx, dy):
    n = math.hypot(dx, dy)
    return dx / n, dy / n


def _chevron(x, y, tx, ty, size=2.6):
    """Open arrowhead poly at (x, y) pointing along (tx, ty)."""
    tx, ty = _unit(tx, ty)
    px, py = -ty, tx
    bx, by = x - tx * size, y - ty * size
    return poly([(bx + px * size, by + py * size), (x, y), (bx - px * size, by - py * size)])


def _star4(cx, cy, r, k=0.35):
    pts = []
    for i in range(8):
        a = math.radians(-90 + i * 45)
        rr = r if i % 2 == 0 else r * k
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return pts


@icon("text-adventure", CAT, "Screen with a compass star, a prompt arrow and a blinking cursor",
      tags=["text adventure", "interactive fiction", "terminal game", "command prompt", "compass", "cursor", "retro game"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 18, S.R)),
        Part("dot", poly(_star4(12, 8, 3.8), closed=True)),
        line(poly([(6, 14), (8.8, 16.3), (6, 18.6)])),
        Part("dot", rect(11, 17.5, 5, 2)),
    ]


@icon("level-select", CAT, "Winding dotted path linking round level nodes with a star above the last one",
      tags=["level select", "world map", "stages", "progress", "levels", "path", "star rating"])
def _(S):
    return [
        node(S, 5, 19, 2.3), node(S, 13.5, 17, 2.3), node(S, 6.5, 11, 2.3), node_ring(S, 17, 11, 2.3),
        dot(9, 18.2, 0.9), dot(10.5, 17.8, 0.9), dot(11, 12.8, 0.9), dot(9.5, 13.3, 0.9),
        dot(14.5, 11.3, 0.9), dot(12.8, 11.1, 0.9),
        Part("solid", poly(_star4(17, 4.5, 3.2, 0.45 if S.name == "line" else 0.6), closed=True, r=0 if S.name == "line" else 0.5)),
    ]


@icon("respawn", CAT, "Person silhouette inside a circular arrow that loops almost all the way round",
      tags=["respawn", "revive", "spawn", "new life", "retry", "restart", "reborn"])
def _(S):
    end = 215
    ex, ey = 12 + 9 * math.cos(math.radians(end)), 12 + 9 * math.sin(math.radians(end))
    tx, ty = -math.sin(math.radians(end)), math.cos(math.radians(end))
    return [
        line(arc(12, 12, 9, -45, end)),
        line(_chevron(ex, ey, tx, ty)),
        dot(12, 9.3, 2),
        Part("solid", "M8.3 17Q8.3 12.5 12 12.5Q15.7 12.5 15.7 17Z"),
    ]


@icon("save-point", CAT, "Floating crystal above a short pedestal with small sparkles",
      tags=["save point", "checkpoint", "crystal", "save game", "pedestal", "rpg", "progress"])
def _(S):
    return [
        shell(poly([(12, 2.5), (17, 7), (12, 14), (7, 7)], closed=True, r=S.r * 0.6)),
        detail(seg(7, 7, 17, 7)),
        shell(rect(6.5, 17, 11, 4.5, min(S.R, 2))),
        dot(3.8, 9.5, 1), dot(20.2, 5, 1), dot(19.5, 12.5, 0.9),
    ]


@icon("quest-marker", CAT, "Exclamation mark floating above a small diamond marker",
      tags=["quest marker", "exclamation", "quest giver", "objective", "waypoint", "rpg", "mission"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 10)), dot(12, 13, 1.4),
        shell(poly([(12, 16), (17, 19), (12, 22), (7, 19)], closed=True, r=S.r * 0.4)),
    ]


@icon("skill-tree", CAT, "Tree of round nodes branching upward from a root, some filled",
      tags=["skill tree", "talents", "upgrades", "perks", "progression", "rpg", "unlock"])
def _(S):
    return [
        node(S, 12, 19.5, 2.4), node(S, 5, 11.5, 2.4), node(S, 12, 11.5, 2.4), node_ring(S, 19, 11.5, 2.3), node_ring(S, 12, 4, 2.3),
        line(seg(11, 17.5, 6, 13.5)), line(seg(13, 17.5, 18, 13.5)), line(seg(12, 17, 12, 14)),
        line(seg(12, 9, 12, 6.5)),
    ]


@icon("crafting-bench", CAT, "Workbench with a hammer lying across the top",
      tags=["crafting bench", "workbench", "crafting table", "hammer", "build", "survival game", "craft"])
def _(S):
    return [
        shell(rect(2.5, 11.5, 19, 3.5, min(S.R, 1.5))),
        line(seg(5, 15, 5, 21.5)), line(seg(19, 15, 19, 21.5)), line(seg(5, 19, 19, 19)),
        line(seg(4, 6.5, 15.5, 6.5)),
        shell(rect(15.5, 3, 4.5, 5.5, min(S.R, 1.5))),
    ]


@icon("pixel-sprite", CAT, "Small blocky figure built from square pixels with a stepped outline",
      tags=["pixel sprite", "pixel art", "8 bit", "retro", "character", "sprite", "blocky"])
def _(S):
    rows = ["..XX..", ".XXXX.", "..XX..", "XXXXXX", "..XX..", ".X..X."]
    cells = [rect(3 + 3 * c, 3 + 3 * r, 3, 3) for r, row in enumerate(rows) for c, ch in enumerate(row) if ch == "X"]
    return [shell(path_to_d(U(*[P(d) for d in cells])))]


@icon("sprite-sheet", CAT, "Four animation frames each holding the same small figure in a different pose",
      tags=["sprite sheet", "animation frames", "walk cycle", "pixel art", "frames", "game art", "spritesheet"])
def _(S):
    r = 0 if S.name == "line" else 2.2
    out = []
    for (px, py), w in zip([(3, 3), (12.5, 3), (3, 12.5), (12.5, 12.5)], (1.5, 0.3, 1.0, 0.0)):
        out.append(shell(rect(px, py, 8.5, 8.5, r)))
        cx, cy = px + 4.25, py + 4.25
        out.append(dot(cx, cy - 1.2, 0.95))
        out.append(Part("dot", poly([(cx - 0.5, cy), (cx + 0.5, cy), (cx + 0.5 + w, cy + 1.9), (cx - 0.5 - w, cy + 1.9)], closed=True)))
    return out


@icon("hitbox", CAT, "Figure outline inside a dashed rectangle with corner handles",
      tags=["hitbox", "collision box", "bounding box", "debug", "game dev", "collider", "handles"])
def _(S):
    k = 0 if S.name == "line" else 0.7
    return [
        *[Part("solid", rect(x, y, 3, 3, k)) for x in (2, 19) for y in (2, 19)],
        line(seg(7.5, 3.5, 10, 3.5)), line(seg(14, 3.5, 16.5, 3.5)),
        line(seg(7.5, 20.5, 10, 20.5)), line(seg(14, 20.5, 16.5, 20.5)),
        line(seg(3.5, 7.5, 3.5, 10)), line(seg(3.5, 14, 3.5, 16.5)),
        line(seg(20.5, 7.5, 20.5, 10)), line(seg(20.5, 14, 20.5, 16.5)),
        dot(12, 7.5, 1.8), line(seg(12, 10, 12, 14.5)), line(seg(9, 11.5, 15, 11.5)),
        line(poly([(9.5, 18), (12, 14.5), (14.5, 18)])),
    ]


@icon("versus-badge", CAT, "Circle split by a zigzag line with V on one side and S on the other",
      tags=["versus", "vs", "matchup", "head to head", "duel", "battle", "fight card"])
def _(S):
    return [
        shell(circle(12, 12, 9.5)),
        detail(poly([(12.5, 2.5), (11, 8), (13, 11), (11, 15.5), (12.5, 21.5)])),
        line(poly([(4.5, 9), (7, 15), (9.5, 9)], r=S.r)),
        line(poly([(19.5, 9), (15.3, 9), (15.3, 12), (19.5, 12), (19.5, 15), (15.3, 15)], r=S.r * 0.4)),
    ]


@icon("item-hotbar", CAT, "Row of item slots with one raised slot selected and an item inside another",
      tags=["hotbar", "inventory bar", "item slots", "quick slots", "toolbar", "survival game", "inventory"])
def _(S):
    return [
        shell(rect(2.5, 8.5, 19, 7, 0 if S.name == "line" else 2.5)),
        detail(seg(7.25, 8.5, 7.25, 15.5)), detail(seg(16.75, 8.5, 16.75, 15.5)),
        shell(rect(7.4, 5.5, 4.6, 13, 0 if S.name == "line" else 1.8)),
        dot(14.4, 12, 1.1),
    ]


@icon("character-select", CAT, "Grid of portrait squares with a pointer cursor over one",
      tags=["character select", "roster", "fighter select", "portraits", "choose character", "cursor", "lobby"])
def _(S):
    k = 0 if S.name == "line" else 2
    out = []
    for x in (2.5, 9.35, 16.2):
        for y in (3, 12.5):
            out.append(shell(rect(x, y, 5.3, 7, k)))
    out = [o for i, o in enumerate(out)]
    out += [dot(5.15, 7.5, 0.9), dot(12, 7.5, 0.9), dot(18.85, 7.5, 0.9), dot(5.15, 17, 0.9), dot(18.85, 17, 0.9),
            Part("solid", poly([(11.5, 14.5), (11.5, 22), (13.4, 20.2), (14.8, 23), (16.2, 22.3), (14.8, 19.5), (17.4, 19.3)], closed=True, r=S.r * 0.3))]
    return out


@icon("cooldown", CAT, "Rounded square ability icon with a pie-shaped sweep covering part of it",
      tags=["cooldown", "ability", "skill timer", "recharge", "spell", "timer sweep", "wait"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        Part("dot", "M12 12V5A7 7 0 0 1 18.06 15.5Z"),
    ]


@icon("tournament-bracket", CAT, "Bracket lines joining four slots into two and then into one final slot",
      tags=["tournament", "bracket", "playoffs", "knockout", "esports", "competition", "final"])
def _(S):
    r = S.r * 0.3
    return [
        line(poly([(2.5, 4.5), (8, 4.5), (8, 9.5), (2.5, 9.5)])),
        line(seg(8, 7, 12.5, 7)),
        line(poly([(2.5, 14.5), (8, 14.5), (8, 19.5), (2.5, 19.5)])),
        line(seg(8, 17, 12.5, 17)),
        line(seg(12.5, 7, 12.5, 17)), line(seg(12.5, 12, 16, 12)),
        shell(rect(16, 9, 5.5, 6, min(S.R, 1.5))),
    ]


@icon("fuse-bomb", CAT, "Round cartoon bomb with a short neck and a lit curling fuse",
      tags=["bomb", "fuse", "explosive", "dynamite", "cartoon bomb", "boom", "blast"])
def _(S):
    return [
        shell(circle(10, 14.5, 7.3)),
        shell(rbox(14.6, 7.8, 5.2, 3.6, -40, r=S.r * 0.8)),
        line("M16.7 6Q18.8 3.6 21 4.6"),
        dot(21.2, 2.8, 1.2),
        detail("M5.5 15Q5.8 12 8 10.8"),
    ]


@icon("mystery-box", CAT, "Cube with a large question mark on its front face",
      tags=["mystery box", "loot box", "question block", "random reward", "surprise", "unknown", "gacha"])
def _(S):
    return [
        shell(poly([(3, 9), (15, 9), (15, 21), (3, 21)], closed=True, r=S.r * 0.6)),
        shell(poly([(3, 9), (7, 3.5), (19, 3.5), (15, 9)], closed=True, r=S.r * 0.4)),
        shell(poly([(15, 9), (19, 3.5), (19, 15.5), (15, 21)], closed=True, r=S.r * 0.4)),
        detail("M6.8 13.3Q6.8 11.8 9 11.8Q11.2 11.8 11.2 13.4Q11.2 14.6 9 15.6V16.6"),
        dot(9, 19, 0.9),
    ]


@icon("grappling-hook", CAT, "Three-pronged hook with curved tines and a rope coiled at its shank",
      tags=["grappling hook", "grapnel", "rope", "climb", "hook", "adventure", "tool"])
def _(S):
    return [
        shell(circle(12, 4.8, 2.4)),
        line(seg(12, 7.2, 12, 16)),
        line("M12 16Q7.5 16.5 5.5 11.5"), line("M12 16Q16.5 16.5 18.5 11.5"),
        line(seg(12, 16, 12, 21.5)),
        line("M14.4 4.8Q20 4.8 20 10"),
    ]


@icon("game-master-screen", CAT, "Three-panel folding screen standing upright with a die on the centre panel",
      tags=["game master screen", "dm screen", "gm screen", "tabletop rpg", "screen", "dungeon master", "panels"])
def _(S):
    outline = [(2.5, 5), (8.5, 3.5), (15.5, 3.5), (21.5, 5), (21.5, 21), (15.5, 19.5), (8.5, 19.5), (2.5, 21)]
    return [
        shell(poly(outline, closed=True, r=S.r * 0.5)),
        detail(seg(8.5, 3.5, 8.5, 19.5)), detail(seg(15.5, 3.5, 15.5, 19.5)),
        Part("dot", rect(10.3, 9, 3.4, 3.4, 0.6)),
    ]


@icon("battle-mat", CAT, "Gridded mat with a miniature on a round base standing on one square",
      tags=["battle mat", "battlemap", "miniature", "tabletop", "grid", "wargame", "rpg"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
        detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15)),
        dot(12, 10.6, 1.4), Part("dot", poly([(10.4, 14), (12, 12), (13.6, 14)], closed=True)),
    ]
