"""TypeIcon Core: games & entertainment.

Generic game pieces, fantasy props and fairground rides only: no console maker's hardware or logo, no
publisher's characters. Variant badges sit in the bottom-right (13–23), so identifying detail is kept
top/left where the object allows.

Line and Rounded differ deliberately where a shape has no corners: Line uses faceted or square forms
(pixel pips, zigzag hems), Rounded uses the smooth or round equivalent.
"""
import math
import re

from dsl import LINE, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from dsl import D, I, P, ST, U, filled_region
from geometry import fmt, path_to_d, polar

CAT = "games"


# --------------------------------------------------------------------------- helpers

def pick(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def rpt(p, deg, c=(12.0, 12.0)):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca)


def rpts(pts, deg, c=(12.0, 12.0)):
    return [rpt(p, deg, c) for p in pts]


_TOK = re.compile(r"[MLHVCQAZ]|-?(?:\d+\.?\d*|\.\d+)(?:e-?\d+)?")
_NARGS = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "Q": 4, "A": 7}


def rot_d(d, deg, c=(12.0, 12.0)):
    """Rotate an absolute-command path (M L H V C Q A Z) about c."""
    toks = _TOK.findall(d)
    out, i, cmd, cur = [], 0, None, (0.0, 0.0)
    start = cur
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            i += 1
            if cmd == "Z":
                out.append("Z")
                cur = start
                continue
        n = _NARGS[cmd]
        a = [float(v) for v in toks[i:i + n]]
        i += n
        if cmd == "M":
            cur = start = (a[0], a[1])
            out.append("M" + _pp(rpt(cur, deg, c)))
            cmd = "L"
        elif cmd in ("L", "H", "V"):
            if cmd == "H":
                cur = (a[0], cur[1])
            elif cmd == "V":
                cur = (cur[0], a[0])
            else:
                cur = (a[0], a[1])
            out.append("L" + _pp(rpt(cur, deg, c)))
        elif cmd == "C":
            ps = [(a[0], a[1]), (a[2], a[3]), (a[4], a[5])]
            cur = ps[-1]
            out.append("C" + " ".join(_pp(rpt(p, deg, c)) for p in ps))
        elif cmd == "Q":
            ps = [(a[0], a[1]), (a[2], a[3])]
            cur = ps[-1]
            out.append("Q" + " ".join(_pp(rpt(p, deg, c)) for p in ps))
        elif cmd == "A":
            cur = (a[5], a[6])
            out.append(f"A{fmt(a[0])} {fmt(a[1])} {fmt(a[2] + deg)} {int(a[3])} {int(a[4])} " + _pp(rpt(cur, deg, c)))
    return "".join(out)


def _pp(p):
    return f"{fmt(round(p[0], 3))} {fmt(round(p[1], 3))}"


def smooth(pts, closed=False):
    """Catmull-Rom curve through the points, as cubic Béziers."""
    n = len(pts)
    d = "M" + _pp(pts[0])
    segs = n if closed else n - 1
    for i in range(segs):
        p1, p2 = pts[i], pts[(i + 1) % n]
        p0 = pts[i - 1] if (i > 0 or closed) else p1
        p3 = pts[(i + 2) % n] if (i + 2 < n or closed) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += "C" + _pp(c1) + " " + _pp(c2) + " " + _pp(p2)
    return d + ("Z" if closed else "")


def seam(S, pts, closed=False):
    """Faceted in Line, smooth in Rounded."""
    return poly(pts, closed=closed) if S.name == "line" else smooth(pts, closed)


def mirror(pts, cx=12.0):
    return [(2 * cx - x, y) for x, y in pts]


# ---- layering: back parts are cut away around the front silhouette (all styles)

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
    return U(region, ST(path_to_d(region), 2 * g, "round", "round"))


def layered(name, desc, tags, aliases=(), gap=1.5):
    """fn(S) -> (front parts, back parts)."""
    def deco(fn):
        def draw(S):
            front, back = fn(S)
            vis = D(_paint(back, S), _grow(_sil(front, S), gap))
            return list(front) + [solid(path_to_d(vis))]

        def filled():
            front, back = fn(LINE)
            ff = filled_region(front)
            return U(ff, D(filled_region(back), _grow(ff, gap)))
        icon(name, CAT, desc, tags=tags, aliases=aliases, filled=filled)(draw)
        return fn
    return deco




def heart_d(cx, cy, w):
    """Heart of width w centred on (cx, cy)."""
    k = [(0, .45), (-.15, .3), (-.5, .1), (-.5, -.15), (-.5, -.32), (-.37, -.42), (-.25, -.42), (-.12, -.42), (-.03, -.35),
         (0, -.25), (.03, -.35), (.12, -.42), (.25, -.42), (.37, -.42), (.5, -.32), (.5, -.15), (.5, .1), (.15, .3), (0, .45)]
    p = [(cx + x * w, cy + y * w) for x, y in k]
    d = "M" + _pp(p[0])
    for i in range(1, len(p), 3):
        d += "C" + " ".join(_pp(q) for q in p[i:i + 3])
    return d + "Z"


def sparkle(cx, cy, r, inner=0.28):
    """Four-pointed sparkle star (points for poly)."""
    return [polar(cx, cy, r if k % 2 == 0 else r * inner, -90 + k * 45) for k in range(8)]


# ============================================================================ tabletop

@icon("dice", CAT, "Die showing five pips",
      tags=["dice", "die", "roll", "board game", "chance", "random"], aliases=["die"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, S.R))]
    for x, y in ((7.5, 7.5), (16.5, 7.5), (12, 12), (7.5, 16.5), (16.5, 16.5)):
        parts.append(sq(x - 1.5, y - 1.5, 3, 3) if S.name == "line" else dot(x, y, 1.7))
    return parts


def _base(S):
    return shell(rect(5, 18, 14, 3, pick(S, 0, 1.5)))


def _body(S, top, wt, wb=3.8, bottom=18):
    return shell(poly([(12 - wt, top), (12 + wt, top), (12 + wb, bottom), (12 - wb, bottom)], closed=True, r=pick(S, 0, 0.8)))


@icon("chess-king", CAT, "Chess king topped with a cross",
      tags=["chess", "king", "checkmate", "board game", "strategy", "piece"])
def _(S):
    return [
        line(seg(12, 2, 12, 7)), line(seg(9.5, 4, 14.5, 4)),
        shell(poly([(7, 8), (17, 8), (15, 13), (9, 13)], closed=True, r=pick(S, 0, 1))),
        _body(S, 13, 2.2), _base(S),
    ]


@icon("chess-queen", CAT, "Chess queen wearing a pointed coronet",
      tags=["chess", "queen", "board game", "strategy", "piece", "checkmate"])
def _(S):
    return [
        shell(poly([(6.5, 4), (9.3, 8), (12, 3), (14.7, 8), (17.5, 4), (15.5, 13), (8.5, 13)], closed=True, r=pick(S, 0, 0.8))),
        _body(S, 13, 2.2), _base(S),
    ]


@icon("chess-rook", CAT, "Chess rook with a battlemented top",
      tags=["chess", "rook", "castle", "board game", "strategy", "piece"])
def _(S):
    top = [(6.5, 3), (9, 3), (9, 5), (11, 5), (11, 3), (13, 3), (13, 5), (15, 5), (15, 3), (17.5, 3), (17.5, 7.5), (15.5, 9.5),
           (15.5, 18), (8.5, 18), (8.5, 9.5), (6.5, 7.5)]
    return [shell(poly(top, closed=True, r=pick(S, 0, 0.6))), detail(seg(8.5, 9.5, 15.5, 9.5)), _base(S)]


@icon("chess-bishop", CAT, "Chess bishop with a slit mitre",
      tags=["chess", "bishop", "board game", "strategy", "piece", "diagonal"])
def _(S):
    mitre = pick(S, "M12 2.5L16 8.5V11L14.5 13H9.5L8 11V8.5Z",
                 "M12 2.5C14.8 4.8 16 7.2 16 9.8C16 11.8 14.8 13 12 13C9.2 13 8 11.8 8 9.8C8 7.2 9.2 4.8 12 2.5Z")
    return [shell(mitre), detail(seg(11, 9, 14, 6.2)), _body(S, 13, 2, 3.8), _base(S)]


@icon("chess-knight", CAT, "Chess knight shaped like a horse's head",
      tags=["chess", "knight", "horse", "board game", "strategy", "piece"])
def _(S):
    head = [(8, 18), (9, 13.5), (6.5, 13.5), (4, 11), (8, 5.5), (9.5, 2.5), (11, 4.5), (13.5, 4.5), (17, 7.5), (18, 12), (17, 18)]
    return [shell(poly(head, closed=True, r=pick(S, 0, 1.2))), dot(10.5, 8, 1.2), _base(S)]


@icon("chess-pawn", CAT, "Chess pawn",
      tags=["chess", "pawn", "board game", "strategy", "piece", "sacrifice"])
def _(S):
    return [
        shell(circle(12, 7, 3.5)),
        line(seg(8.5, 12, 15.5, 12)),
        _body(S, 12.5, 1.8, 3.8), _base(S),
    ]


@layered("playing-cards", "Two fanned playing cards with a heart",
         tags=["cards", "playing cards", "poker", "deck", "casino", "solitaire"], aliases=["cards-playing"])
def _(S):
    front = [shell(rot_d(rect(10, 4, 10, 15, pick(S, 1, 2)), 12, (15, 11.5))),
             Part("dot", rot_d(heart_d(15, 11.8, 5), 12, (15, 11.5)))]
    back = [shell(rot_d(rect(4, 4, 10, 15, pick(S, 1, 2)), -12, (9, 11.5)))]
    return front, back


@icon("poker-chip", CAT, "Casino chip with an edge pattern",
      tags=["poker chip", "casino", "gambling", "bet", "token", "chips"], aliases=["casino-chip"])
def _(S):
    inner = poly(regular(12, 12, 5, 8, -90 + 22.5), closed=True) if S.name == "line" else circle(12, 12, 4.8)
    parts = [shell(circle(12, 12, 9)), detail(inner)]
    for a in range(-90, 270, 60):
        parts.append(detail(seg(*polar(12, 12, 5.5, a), *polar(12, 12, 9, a))))
    return parts


# ============================================================================ video games

@icon("arcade", CAT, "Arcade cabinet with a screen and control deck",
      tags=["arcade", "arcade machine", "retro", "coin-op", "video game", "cabinet"], aliases=["arcade-machine"])
def _(S):
    body = [(6, 3), (18, 3), (18, 13), (20, 15), (20, 17.5), (18, 17.5), (18, 21), (6, 21), (6, 17.5), (4, 17.5), (4, 15), (6, 13)]
    return [
        shell(poly(body, closed=True, r=pick(S, 0, 1))),
        detail(rect(8.5, 6, 7, 5, pick(S, 0, 1.5))),
        dot(9, 15.5, 1), dot(12, 15.5, 1), dot(15, 15.5, 1),
    ]


@icon("controller-retro", CAT, "Flat retro game controller with a direction pad and two buttons",
      tags=["retro controller", "gamepad", "8-bit", "classic", "joypad", "video game"], aliases=["retro-gamepad"])
def _(S):
    return [
        shell(rect(2.5, 7, 19, 10, pick(S, 1.5, 3.5))),
        Part("dot", poly([(5, 11), (6.5, 11), (6.5, 9.5), (8.5, 9.5), (8.5, 11), (10, 11), (10, 13), (8.5, 13), (8.5, 14.5),
                          (6.5, 14.5), (6.5, 13), (5, 13)], closed=True, r=pick(S, 0, 0.4))),
        dot(15.5, 13, 1.5), dot(18.5, 11, 1.5),
    ]


@icon("game-cartridge", CAT, "Game cartridge with a label and grip ridges",
      tags=["cartridge", "game cart", "retro", "rom", "video game", "8-bit"], aliases=["cartridge"])
def _(S):
    body = [(4.5, 3), (19.5, 3), (19.5, 21), (6.5, 21), (4.5, 19)]
    return [
        shell(poly(body, closed=True, r=pick(S, 0, 1.5))),
        detail(rect(7.5, 9, 9, 7.5, pick(S, 0, 1.5))),
        detail(seg(9, 3, 9, 6)), detail(seg(12, 3, 12, 6)), detail(seg(15, 3, 15, 6)),
    ]


@icon("ghost", CAT, "Ghost with a wavy hem and two eyes",
      tags=["ghost", "spooky", "boo", "halloween", "spirit", "haunted"], aliases=["boo"])
def _(S):
    hem = [(19, 21), (16.7, 19), (14.3, 21), (12, 19), (9.7, 21), (7.3, 19), (5, 21)]
    hem_d = poly(hem) if S.name == "line" else smooth(hem)
    return [
        shell("M5 21V10A7 7 0 0 1 19 10V21" + hem_d.replace("M19 21", "", 1) + "Z"),
        dot(9.5, 10.5, 1.5), dot(14.5, 10.5, 1.5),
    ]


@icon("alien", CAT, "Alien head with large almond eyes",
      tags=["alien", "extraterrestrial", "ufo", "martian", "space invader", "sci-fi"], aliases=["extraterrestrial"])
def _(S):
    head = pick(S, "M12 21.5L6 16C4.7 14.6 4 12.4 4 10C4 5.5 7.5 3 12 3C16.5 3 20 5.5 20 10C20 12.4 19.3 14.6 18 16Z",
                "M12 21.5C8.5 21.5 4 15 4 10C4 5.5 7.5 3 12 3C16.5 3 20 5.5 20 10C20 15 15.5 21.5 12 21.5Z")
    return [
        shell(head),
        Part("dot", rot_d(ellipse(8.7, 11.5, 2.6, 1.5), 30, (8.7, 11.5))),
        Part("dot", rot_d(ellipse(15.3, 11.5, 2.6, 1.5), -30, (15.3, 11.5))),
    ]


@icon("boss-skull", CAT, "Horned skull marking a boss enemy",
      tags=["boss", "enemy", "skull", "horns", "villain", "danger"], aliases=["boss"])
def _(S):
    head = pick(S, "M12 6C8 6 5.5 8.8 5.5 12C5.5 14 6.4 15.6 7.8 16.4V21H16.2V16.4C17.6 15.6 18.5 14 18.5 12C18.5 8.8 16 6 12 6Z",
                "M12 6C8 6 5.5 8.8 5.5 12C5.5 14 6.4 15.6 7.8 16.4V19.5C7.8 20.3 8.5 21 9.3 21H14.7C15.5 21 16.2 20.3 16.2 19.5V16.4"
                "C17.6 15.6 18.5 14 18.5 12C18.5 8.8 16 6 12 6Z")
    horn_l = "M6.4 9.2C4.2 8.3 3 6.3 3.3 3.8C4.4 5.4 6.2 6.3 8.6 6.6"
    horn_r = "M17.6 9.2C19.8 8.3 21 6.3 20.7 3.8C19.6 5.4 17.8 6.3 15.4 6.6"
    return [
        shell(head), shell(horn_l + "Z", stroke_miterlimit="2"), shell(horn_r + "Z", stroke_miterlimit="2"),
        dot(9.5, 12.3, 1.8), dot(14.5, 12.3, 1.8),
        detail(seg(10.5, 18, 10.5, 21)), detail(seg(13.5, 18, 13.5, 21)),
    ]


@icon("heart-game", CAT, "Pixel-art heart: a life in a video game",
      tags=["life", "extra life", "hp", "pixel heart", "8-bit", "health"], aliases=["pixel-heart"])
def _(S):
    pts = [(5, 4), (9, 4), (9, 6), (11, 6), (11, 8), (13, 8), (13, 6), (15, 6), (15, 4), (19, 4), (19, 6), (21, 6), (21, 12),
           (19, 12), (19, 14), (17, 14), (17, 16), (15, 16), (15, 18), (13, 18), (13, 20), (11, 20), (11, 18), (9, 18), (9, 16),
           (7, 16), (7, 14), (5, 14), (5, 12), (3, 12), (3, 6), (5, 6)]
    return [shell(poly(pts, closed=True, r=pick(S, 0, 0.5))), sq(6, 7, 2, 2, pick(S, 0, 0.6))]


@icon("health-bar", CAT, "Heart beside a partly full health bar",
      tags=["health", "hp", "hit points", "life bar", "energy", "status"], aliases=["hp-bar"])
def _(S):
    return [
        solid(heart_d(5.5, 12.2, 7.5)),
        shell(rect(10.5, 8, 10.5, 8, pick(S, 1, 2))),
        sq(13, 10.5, 4.5, 3, pick(S, 0, 1)),
    ]


@icon("level-up", CAT, "Upward arrow over rising level bars",
      tags=["level up", "upgrade", "rank up", "promotion", "progress", "xp"], aliases=["rank-up"])
def _(S):
    return [
        shell(poly([(12, 2.5), (19, 9.5), (15, 9.5), (15, 13.5), (9, 13.5), (9, 9.5), (5, 9.5)], closed=True, r=pick(S, 0, 1))),
        line(seg(7, 17, 17, 17)),
        line(seg(9, 21, 15, 21) if S.name == "line" else seg(9.5, 21, 14.5, 21)),
    ]


@icon("coin", CAT, "Spinning game coin",
      tags=["coin", "gold", "points", "score", "currency", "collect"], aliases=["game-coin"])
def _(S):
    outline = pick(S, poly([(9.5, 3), (14.5, 3), (18.5, 7.5), (18.5, 16.5), (14.5, 21), (9.5, 21), (5.5, 16.5), (5.5, 7.5)], closed=True),
                   ellipse(12, 12, 6.8, 9))
    return [shell(outline), detail(seg(12, 8, 12, 16))]


@icon("gem", CAT, "Cut gemstone with facets",
      tags=["gem", "diamond", "jewel", "gemstone", "treasure", "premium"], aliases=["jewel"])
def _(S):
    return [
        shell(poly([(7, 4), (17, 4), (21, 9.5), (12, 20.5), (3, 9.5)], closed=True, r=pick(S, 0, 2.2))),
        detail(seg(3, 9.5, 21, 9.5)),
        detail(poly([(9.5, 9.5), (12, 20.5), (14.5, 9.5)])),
        detail(poly([(9.5, 4), (9.5, 9.5)])) if False else detail(poly([(7, 4), (9.5, 9.5)])),
        detail(poly([(17, 4), (14.5, 9.5)])),
    ]


@icon("crown-game", CAT, "Jewelled crown with orbs on its points",
      tags=["crown", "winner", "leader", "king", "champion", "vip"], aliases=["leaderboard-crown"])
def _(S):
    return [
        shell(poly([(4, 9), (8, 13), (12, 7.5), (16, 13), (20, 9), (18.5, 20), (5.5, 20)], closed=True, r=pick(S, 0, 1))),
        dot(4, 6.5, 1.6), dot(12, 5, 1.6), dot(20, 6.5, 1.6),
        detail(seg(5.5, 16.5, 18.5, 16.5)),
    ]


# ============================================================================ fantasy

@icon("sword", CAT, "Sword with a crossguard",
      tags=["sword", "blade", "attack", "weapon", "rpg", "knight"], aliases=["blade"])
def _(S):
    blade = poly([(12, 2), (14, 5), (14, 15), (10, 15), (10, 5)], closed=True, r=pick(S, 0, 1))
    parts = [
        shell(blade),
        line(seg(7, 16, 17, 16)),
        line(seg(12, 17, 12, 20)),
        dot(12, 21, 1.5),
    ]
    return [Part(p.kind, rot_d(p.d, 45), p.attrs) for p in parts]


@icon("shield-game", CAT, "Knight's shield divided into quarters",
      tags=["shield", "defense", "armor", "knight", "rpg", "heraldry"], aliases=["knight-shield"])
def _(S):
    body = pick(S, "M4 3.5H20V11C20 16 16.5 19.5 12 21.5C7.5 19.5 4 16 4 11Z",
                "M6 3.5H18C19.1 3.5 20 4.4 20 5.5V11C20 16 16.5 19.5 12 21.5C7.5 19.5 4 16 4 11V5.5C4 4.4 4.9 3.5 6 3.5Z")
    return [shell(body), detail(seg(12, 3.5, 12, 21.5)), detail(seg(4, 10.5, 20, 10.5))]


@icon("potion", CAT, "Round-bottomed potion bottle with bubbles",
      tags=["potion", "elixir", "magic", "flask", "rpg", "alchemy"], aliases=["elixir"])
def _(S):
    level = seg(6.2, 13, 17.8, 13) if S.name == "line" else "M6.2 13C8 12 10 12 12 13C14 14 16 14 17.8 13"
    return [
        shell("M10 4.5V7.8A6.5 6.5 0 1 0 14 7.8V4.5Z"),
        line(seg(8.5, 3, 15.5, 3) if S.name == "line" else seg(9, 3, 15, 3)),
        detail(level),
        dot(10.5, 16.5, 1.1), dot(13.8, 17.8, 0.9),
    ]


@icon("treasure-chest", CAT, "Treasure chest with a domed lid and lock",
      tags=["treasure", "chest", "loot", "reward", "pirate", "rpg"], aliases=["loot-chest"])
def _(S):
    body = pick(S, "M3.5 21V8L6 4H18L20.5 8V21Z",
                "M3.5 21V8C3.5 5.5 5.5 3.5 8 3.5H16C18.5 3.5 20.5 5.5 20.5 8V21Z")
    return [
        shell(body),
        detail(seg(3.5, 10, 20.5, 10)),
        detail(seg(7.5, 4, 7.5, 21)), detail(seg(16.5, 4, 16.5, 21)),
        Part("dot", rect(10.5, 8.5, 3, 4.5, pick(S, 0, 1))),
    ]


@icon("map-treasure", CAT, "Treasure map scroll with a dotted trail to an X",
      tags=["treasure map", "map", "x marks the spot", "quest", "pirate", "adventure"], aliases=["treasure-map"])
def _(S):
    return [
        shell(rect(5, 5.5, 14, 13)),
        shell(rect(3, 3, 18, 3.5, pick(S, 1, 1.75))), shell(rect(3, 17.5, 18, 3.5, pick(S, 1, 1.75))),
        detail(seg(13, 9.5, 16, 12.5)), detail(seg(16, 9.5, 13, 12.5)),
        dot(8, 14.2, 1), dot(10.8, 12.8, 1),
    ]


@icon("castle-game", CAT, "Fairytale castle with spired towers and a gate",
      tags=["castle", "kingdom", "fortress", "level", "fairytale", "palace"], aliases=["fairytale-castle"])
def _(S):
    sil = [(3, 21), (3, 10), (5.5, 4.5), (8, 10), (8, 13), (9.5, 13), (9.5, 9), (12, 3), (14.5, 9), (14.5, 13), (16, 13),
           (16, 10), (18.5, 4.5), (21, 10), (21, 21)]
    gate = "M10 21V18A2 2 0 0 1 14 18V21" if S.name == "rounded" else "M10 21V16.5L12 15L14 16.5V21"
    return [
        shell(poly(sil, closed=True, r=pick(S, 0, 0.8))),
        detail(seg(3, 10, 8, 10)), detail(seg(16, 10, 21, 10)), detail(seg(9.5, 9, 14.5, 9)),
        detail(gate),
    ]


@icon("dragon-game", CAT, "Horned dragon head in profile",
      tags=["dragon", "monster", "fantasy", "boss", "rpg", "beast"], aliases=["dragon-head"])
def _(S):
    pts = [(6, 21), (6, 19), (3.5, 17.5), (6, 16), (3.5, 14.5), (6, 13), (6, 10.5), (3, 3), (9.5, 7), (14, 6.5), (21, 10),
           (21, 13), (15, 13.5), (12, 15.5), (12, 21)]
    return [
        shell(poly(pts, closed=True, r=pick(S, 0, 0.4))),
        dot(11.5, 9.5, 1.3),
        detail(seg(15.5, 11, 19, 11) if S.name == "line" else seg(16, 11, 19, 11)),
    ]


@icon("magic-book", CAT, "Spellbook with a sparkle on its cover",
      tags=["spellbook", "grimoire", "magic", "spell", "wizard", "rpg"], aliases=["spellbook", "grimoire"])
def _(S):
    return [
        shell(rect(4.5, 3, 15, 18, pick(S, 1, 2.5))),
        detail(seg(8, 3, 8, 21)),
        Part("dot", poly(sparkle(13.8, 11, 4.2), closed=True, r=pick(S, 0, 0.3))),
    ]


@icon("crystal-ball", CAT, "Crystal ball on a stand",
      tags=["crystal ball", "fortune", "future", "psychic", "magic", "prediction"], aliases=["fortune-ball"])
def _(S):
    return [
        shell(circle(12, 10.5, 7.5)),
        shell(poly([(8.5, 17.5), (15.5, 17.5), (18, 21), (6, 21)], closed=True, r=pick(S, 0, 1))),
        Part("dot", poly(sparkle(9.8, 8.5, 3), closed=True, r=pick(S, 0, 0.3))),
        dot(14, 12.5, 1),
    ]


@icon("tarot", CAT, "Tarot card with a crescent moon",
      tags=["tarot", "fortune", "card", "divination", "oracle", "mystic"], aliases=["tarot-card"])
def _(S):
    moon = D(P(circle(12, 10.5, 4)), P(circle(14, 8.8, 3.3)))
    return [
        shell(rect(5.5, 3, 13, 18, pick(S, 1, 2.5))),
        Part("dot", path_to_d(moon)),
        Part("dot", poly(sparkle(14.5, 16.5, 2.2, 0.35), closed=True)) if S.name == "line" else dot(14.5, 16.5, 1.2),
        dot(9, 16.8, 0.9),
    ]


# ============================================================================ party & fair

@icon("balloon", CAT, "Party balloon on a string",
      tags=["balloon", "party", "birthday", "celebration", "float", "festive"])
def _(S):
    string = poly([(12, 17.5), (13.2, 19), (11, 20.3), (12, 22)]) if S.name == "line" else "M12 17.5C13.5 18.8 10.5 20.5 12 22"
    return [
        shell("M12 2.5C16 2.5 18.5 5.5 18.5 9C18.5 13 15 16 12 16C9 16 5.5 13 5.5 9C5.5 5.5 8 2.5 12 2.5Z"),
        solid(poly([(10.8, 17.8), (13.2, 17.8), (12, 16)], closed=True)),
        line(string),
        detail("M8.5 9C8.5 7.2 9.6 6 11.3 5.7" if S.name == "rounded" else "M8.5 9L10 6.2"),
    ]


@icon("party-popper", CAT, "Party popper bursting with confetti",
      tags=["party popper", "celebration", "confetti", "congratulations", "tada", "party"], aliases=["tada"])
def _(S):
    return [
        shell(poly([(3, 21), (7, 10), (14, 17)], closed=True, r=pick(S, 0, 1))),
        detail(seg(5, 15.5, 8.5, 19)),
        line(seam(S, [(10.5, 9), (11.5, 6.5), (10.5, 4.5), (12, 2.5)])),
        line(seam(S, [(15, 13.5), (17.5, 12.5), (19.5, 13.5), (21.5, 12.5)])),
        dot(15, 7.5, 1.25), dot(19.5, 4.5, 1.25), dot(19, 9, 1.1),
    ]


@icon("confetti", CAT, "Scattered confetti pieces and streamers",
      tags=["confetti", "celebration", "party", "festive", "congratulations", "streamers"])
def _(S):
    if S.name == "line":
        bits = [Part("dot", rot_d(rect(3.5, 3.5, 2.8, 2.8), 20, (4.9, 4.9))), Part("dot", rot_d(rect(15.5, 9.5, 2.8, 2.8), -25, (16.9, 10.9))),
                Part("dot", rot_d(rect(6, 16, 2.8, 2.8), 35, (7.4, 17.4)))]
    else:
        bits = [dot(5, 5, 1.6), dot(17, 11, 1.6), dot(7.5, 17.5, 1.6)]
    return bits + [
        line(seam(S, [(9.5, 4), (12, 5.5), (14.5, 4), (17, 5.5), (19.5, 4)])),
        line(seam(S, [(4, 12.5), (6.5, 11), (9, 12.5), (11.5, 11)])),
        line(seam(S, [(12.5, 19.5), (15, 18), (17.5, 19.5), (20, 18)])),
        dot(20, 14.5, 1.1), dot(11.5, 15, 1.1),
    ]


def _mask(S, x0, y0, w=8.5, h=11.5):
    x1 = x0 + w
    top = (f"M{fmt(x0)} {fmt(y0)}H{fmt(x1)}" if S.name == "line" else
           f"M{fmt(x0 + 1.5)} {fmt(y0)}H{fmt(x1 - 1.5)}Q{fmt(x1)} {fmt(y0)} {fmt(x1)} {fmt(y0 + 1.5)}")
    side = (f"V{fmt(y0 + h * 0.45)}C{fmt(x1)} {fmt(y0 + h * 0.8)} {fmt(x0 + w * 0.75)} {fmt(y0 + h)} {fmt(x0 + w / 2)} {fmt(y0 + h)}"
            f"C{fmt(x0 + w * 0.25)} {fmt(y0 + h)} {fmt(x0)} {fmt(y0 + h * 0.8)} {fmt(x0)} {fmt(y0 + h * 0.45)}")
    end = "Z" if S.name == "line" else f"V{fmt(y0 + 1.5)}Q{fmt(x0)} {fmt(y0)} {fmt(x0 + 1.5)} {fmt(y0)}Z"
    return top + side + end


@layered("theater-masks", "Comedy and tragedy theatre masks",
         tags=["theatre", "drama", "masks", "comedy", "tragedy", "acting"], aliases=["drama-masks", "comedy-tragedy"])
def _(S):
    fx, fy = 12.5, 9.5
    front = [shell(_mask(S, fx, fy)), dot(fx + 2.5, fy + 3.8, 1.1), dot(fx + 6, fy + 3.8, 1.1),
             detail(f"M{fx + 2.2} {fy + 6.8}Q{fx + 4.25} {fy + 9.4} {fx + 6.3} {fy + 6.8}")]
    bx, by = 3, 3
    back = [shell(_mask(S, bx, by)), dot(bx + 2.5, by + 3.8, 1.1), dot(bx + 6, by + 3.8, 1.1),
            detail(f"M{bx + 2.2} {by + 8.6}Q{bx + 4.25} {by + 6} {bx + 6.3} {by + 8.6}")]
    return front, back


@icon("circus", CAT, "Striped circus big top with a flag",
      tags=["circus", "big top", "tent", "carnival", "show", "fair"], aliases=["big-top"])
def _(S):
    return [
        line(seg(12, 2, 12, 5.5)),
        solid(poly([(12, 2), (15.5, 3), (12, 4.2)], closed=True)),
        shell(poly([(12, 5.5), (21, 11), (3, 11)], closed=True, r=pick(S, 0, 1)), stroke_miterlimit="1.5"),
        detail(seg(12, 5.5, 8.5, 11)), detail(seg(12, 5.5, 15.5, 11)),
        shell(rect(4.5, 11, 15, 10, pick(S, 0, 1.5))),
        detail(poly([(9.5, 21), (12, 15), (14.5, 21)], r=S.r)),
    ]


@icon("ferris-wheel", CAT, "Ferris wheel with gondolas on a stand",
      tags=["ferris wheel", "fairground", "amusement park", "carnival", "big wheel", "ride"], aliases=["big-wheel"])
def _(S):
    c = (12, 10.5)
    parts = [shell(circle(*c, 6.8)), dot(*c, 1.5)]
    for a in (-90, -30, 30):
        parts.append(detail(seg(*polar(*c, 6.8, a), *polar(*c, 6.8, a + 180))))
    for a in range(-90, 270, 60):
        parts.append(dot(*polar(*c, 6.8, a), 1.7))
    parts.append(line(poly([(7, 21.5), c, (17, 21.5)], r=S.r)))
    return parts


@icon("roller-coaster", CAT, "Roller coaster car approaching a loop in the track",
      tags=["roller coaster", "rollercoaster", "theme park", "ride", "thrill", "amusement"], aliases=["rollercoaster"])
def _(S):
    loop = ("M2 19.5H13C17.5 19.5 20.5 16 20.5 11.5C20.5 7.5 18 5 15 5C12 5 9.5 7.5 9.5 11.5C9.5 16 12.5 19.5 17 19.5H22"
            if S.name == "rounded" else
            "M2 19.5H13L18.5 17L20.5 11.5L19 6.5L15 5L11 6.5L9.5 11.5L11.5 17L17 19.5H22")
    return [
        line(loop),
        shell(poly([(3, 13), (6, 13), (8, 17.5), (3, 17.5)], closed=True, r=pick(S, 0, 1))),
    ]


def _puzzle(S):
    c = pick(S, 0, 2)
    tl = f"M3 {7 + c}" + (f"A{c} {c} 0 0 1 {3 + c} 7" if c else "")
    s = (tl + "H8.99A2.2 2.2 0 1 1 11.51 7H" + fmt(16.5 - c) + (f"A{c} {c} 0 0 1 16.5 {7 + c}" if c else "") +
         "V12.74A2.2 2.2 0 1 1 16.5 15.26V" + fmt(21 - c) + (f"A{c} {c} 0 0 1 {fmt(16.5 - c)} 21" if c else "") +
         "H11.01A2.2 2.2 0 1 0 8.49 21H" + fmt(3 + c) + (f"A{c} {c} 0 0 1 3 {21 - c}" if c else "") + "Z")
    return s


@icon("puzzle-piece", CAT, "Single jigsaw puzzle piece",
      tags=["jigsaw", "puzzle", "piece", "solve", "fit", "game"], aliases=["jigsaw-piece"])
def _(S):
    return [shell(_puzzle(S))]


@icon("slot-machine", CAT, "Slot machine with three reels and a lever",
      tags=["slot machine", "casino", "jackpot", "one-armed bandit", "gambling", "777"], aliases=["jackpot"])
def _(S):
    return [
        shell(rect(3, 4, 14, 17, pick(S, 1, 2.5))),
        detail(rect(5.5, 8, 9, 6, pick(S, 0, 1.5))),
        detail(seg(8.5, 8, 8.5, 14)), detail(seg(11.5, 8, 11.5, 14)),
        detail(seg(6.5, 17.5, 13.5, 17.5)),
        line(poly([(17, 15), (20, 15), (20, 7)], r=S.r)),
        dot(20, 5, 1.8),
    ]
