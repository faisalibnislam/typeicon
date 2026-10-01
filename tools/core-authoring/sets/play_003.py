"""TypeIcon Core: play (batch 003) - tabletop, medieval props, party games, carnival and toys."""
import math
import re

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import P, U, D, ST, fmt, path_to_d, rotation, transform_path

CAT = "play"


def pick(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


_TOK = re.compile(r"[MLHVCQAZ]|-?(?:\d+\.?\d*|\.\d+)(?:e-?\d+)?")
_NARGS = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "Q": 4, "A": 7}


def _pp(p):
    return f"{fmt(round(p[0], 3))} {fmt(round(p[1], 3))}"


def rpt(p, deg, c=(12.0, 12.0)):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca)


def rot_d(d, deg, cx=12.0, cy=12.0):
    """Rotate an absolute-command path (M L H V C Q A Z) about (cx, cy)."""
    c = (cx, cy)
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
            cur = (a[0], cur[1]) if cmd == "H" else ((cur[0], a[0]) if cmd == "V" else (a[0], a[1]))
            out.append("L" + _pp(rpt(cur, deg, c)))
        elif cmd == "C":
            ps = [(a[0], a[1]), (a[2], a[3]), (a[4], a[5])]
            cur = ps[-1]
            out.append("C" + " ".join(_pp(rpt(q, deg, c)) for q in ps))
        elif cmd == "Q":
            ps = [(a[0], a[1]), (a[2], a[3])]
            cur = ps[-1]
            out.append("Q" + " ".join(_pp(rpt(q, deg, c)) for q in ps))
        elif cmd == "A":
            cur = (a[5], a[6])
            out.append(f"A{fmt(a[0])} {fmt(a[1])} {fmt(a[2] + deg)} {int(a[3])} {int(a[4])} " + _pp(rpt(cur, deg, c)))
    return "".join(out)


def rotparts(parts, deg, cx=12.0, cy=12.0):
    return [Part(p.kind, rot_d(p.d, deg, cx, cy), p.attrs) for p in parts]


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


# ============================================================================ tabletop and dungeon

@icon("miniature-figure", CAT, "Small cloaked adventurer figure standing on a round base",
      tags=["miniature", "mini", "tabletop", "wargame", "rpg", "figurine", "painted figure"])
def _(S):
    return [
        shell(circle(12, 5, 2.2)),
        shell(poly([(10.5, 10.5), (13.5, 10.5), (17, 17.5), (7, 17.5)], closed=True, r=S.r)),
        shell(ellipse(12, 19.8, 7.5, 1.7) if S.name == "rounded" else poly([(4.5, 19.8), (7, 18.3), (17, 18.3), (19.5, 19.8), (17, 21.3), (7, 21.3)], closed=True)),
        detail(seg(12, 13, 12, 17)),
    ]


@icon("hex-grid-map", CAT, "Cluster of three hexagon map tiles sharing edges",
      tags=["hex map", "hexagon", "tiles", "wargame", "board game", "grid", "territory"])
def _(S):
    outline = [(7.67, 3.25), (12, 5.75), (16.33, 3.25), (20.67, 5.75), (20.67, 10.75), (16.33, 13.25),
               (16.33, 18.25), (12, 20.75), (7.67, 18.25), (7.67, 13.25), (3.33, 10.75), (3.33, 5.75)]
    return [
        shell(poly(outline, closed=True, r=S.r)),
        detail(poly([(12, 5.75), (12, 10.75), (7.67, 13.25)])),
        detail(seg(12, 10.75, 16.33, 13.25)),
        dot(12, 16, 1.5),
    ]


@icon("dungeon-door", CAT, "Arched plank door with an iron band",
      tags=["dungeon", "door", "arch", "castle", "rpg", "gate", "medieval"])
def _(S):
    body = "M5 21V10A7 7 0 0 1 19 10V21Z" if S.name == "rounded" else "M5 21V9.5L8 4.5H16L19 9.5V21Z"
    return [
        shell(body),
        detail(seg(9.5, 4, 9.5, 21)),
        detail(seg(14.5, 4, 14.5, 21)),
        detail(seg(5, 15, 19, 15)),
    ]


@icon("wall-torch", CAT, "Burning torch held in a wall bracket",
      tags=["torch", "flame", "dungeon", "fire", "light", "medieval", "sconce"])
def _(S):
    flame = ("M12 2C13.6 4 15.3 5.3 15.3 7.6A3.3 3.3 0 0 1 8.7 7.6C8.7 5.3 10.4 4 12 2Z" if S.name == "rounded"
             else "M12 2L15.3 6.5V8L13.5 10H10.5L8.7 8V6.5Z")
    return [
        shell(flame),
        shell(poly([(9, 11.5), (15, 11.5), (14, 16), (10, 16)], closed=True, r=S.r)),
        line(seg(12, 16, 12, 21)),
        line(poly([(7, 19), (7, 17.5), (17, 17.5), (17, 19)], r=S.r)),
    ]


@icon("quest-board", CAT, "Notice board on two posts with pinned notes",
      tags=["quest", "notice board", "bounty", "rpg", "job board", "tavern", "missions"])
def _(S):
    return [
        shell(rect(3, 3.5, 18, 12, S.R if S.name == "line" else 3)),
        sq(6, 6.5, 5, 6),
        sq(13, 6.5, 5, 4),
        line(seg(7, 15.5, 7, 21)),
        line(seg(17, 15.5, 17, 21)),
    ]


@icon("tavern-sign", CAT, "Hanging signboard on a wall bracket with a tankard painted on it",
      tags=["tavern", "inn", "pub sign", "signboard", "bracket", "medieval", "rpg"])
def _(S):
    return [
        line(poly([(3, 21), (3, 3), (21, 3)], r=S.r)),
        line(seg(9, 3, 9, 7.5)),
        line(seg(17, 3, 17, 7.5)),
        shell(rect(6, 7.5, 14, 12, pick(S, 1, 3))),
        sq(9.5, 11, 4, 5),
        detail("M13.5 12.2H15.5V14.8H13.5"),
    ]


@icon("coin-pouch", CAT, "Drawstring pouch with a coin beside it",
      tags=["pouch", "coin purse", "gold", "loot", "money bag", "rpg", "treasure"])
def _(S):
    body = ("M7.5 8L5.5 10C3.5 12 3 14 3 16A5 5 0 0 0 8 21H9A5 5 0 0 0 14 16C14 14 13.5 12 11.5 10L9.5 8Z" if S.name == "rounded"
            else "M7.5 8L4.5 11L3 16L5 21H12L14 16L12.5 11L9.5 8Z")
    return [
        shell(body),
        line(poly([(6.5, 8), (5.5, 4.5)], r=0)),
        line(poly([(10.5, 8), (11.5, 4.5)], r=0)),
        shell(circle(18.5, 17.5, 2.7)),
    ]


@icon("amulet", CAT, "Pendant on a chain with a gem in a round setting",
      tags=["amulet", "pendant", "necklace", "talisman", "charm", "gem", "rpg"])
def _(S):
    setting = circle(12, 15, 6) if S.name == "rounded" else poly(regular(12, 15, 6.5, 8, -67.5), closed=True)
    return [
        line(poly([(4.5, 2.5), (9, 9)], r=0)),
        line(poly([(19.5, 2.5), (15, 9)], r=0)),
        shell(setting),
        solid(poly([(12, 11.8), (14.3, 15), (12, 18.2), (9.7, 15)], closed=True)),
    ]


@icon("scepter", CAT, "Royal rod topped with an orb and cross",
      tags=["scepter", "sceptre", "royal", "king", "regal", "staff", "monarch"])
def _(S):
    parts = [
        line(seg(12, 1.5, 12, 4.5)),
        line(seg(10.5, 3, 13.5, 3)),
        shell(circle(12, 8, 3) if S.name == "rounded" else poly(regular(12, 8, 3.4, 8, -67.5), closed=True)),
        line(seg(12, 11, 12, 21)),
        line(seg(10, 15, 14, 15)),
        dot(12, 21, 1.4),
    ]
    return rotparts(parts, 45)


@icon("lockpick", CAT, "Hooked lockpick beside an L shaped tension wrench",
      tags=["lockpick", "lock pick", "rogue", "thief", "picking locks", "rpg", "heist"])
def _(S):
    pick_parts = [
        line(seg(9, 15, 17, 7)),
        line("M17 7Q20.5 4.5 20.5 8"),
        shell(poly([(2.5, 17.5), (5, 15), (9, 19), (6.5, 21.5)], closed=True, r=S.r)),
    ]
    return pick_parts + [line(poly([(15.5, 14), (15.5, 21), (21, 21)], r=S.r))]


@icon("crossed-swords", CAT, "Two swords crossed in an X with their hilts at the bottom",
      tags=["swords", "battle", "duel", "combat", "fight", "versus", "pvp", "arena"])
def _(S):
    def sword():
        return [
            shell(poly([(12, 1.5), (13.6, 4), (13.6, 14.5), (10.4, 14.5), (10.4, 4)], closed=True, r=pick(S, 0, 0.8))),
            line(seg(8, 16, 16, 16)),
            line(seg(12, 17, 12, 20)),
            dot(12, 21, 1.3),
        ]
    return rotparts(sword(), 45) + rotparts(sword(), -45)


@icon("war-hammer", CAT, "Long handled hammer with a flat face on one side and a spike on the other",
      tags=["war hammer", "warhammer", "mallet", "weapon", "dwarf", "medieval", "rpg"])
def _(S):
    parts = [
        shell(poly([(5.5, 4), (12, 4), (12, 10.5), (5.5, 10.5)], closed=True, r=S.r)),
        shell(poly([(12, 4.5), (18.5, 7.25), (12, 10)], closed=True)),
        line(seg(12, 10, 12, 20)),
    ]
    return rotparts(parts, 45)


@icon("crossbow", CAT, "Crossbow from the side with a stock, curved limb and loaded bolt",
      tags=["crossbow", "bolt", "archer", "ranged weapon", "medieval", "rpg", "hunting"])
def _(S):
    return [
        shell(rect(2.5, 10.5, 8, 3.5, pick(S, 0, 1.2))),
        line(seg(6, 14, 6, 19)),
        line("M16 3Q22.5 12 16 21"),
        line(poly([(16, 3), (10.5, 12), (16, 21)], r=0)),
        line(seg(10.5, 12, 18, 12)),
        solid(poly([(23, 12), (18.5, 10), (18.5, 14)], closed=True)),
    ]


@icon("quiver", CAT, "Tall quiver with a strap and three arrows poking out",
      tags=["quiver", "arrows", "archer", "archery", "bow", "hunting", "ranger"])
def _(S):
    return [
        shell(poly([(9, 10), (15, 10), (14.5, 21), (9.5, 21)], closed=True, r=S.r)),
        line(seg(10.5, 10, 9, 4)),
        line(seg(12, 10, 12, 3)),
        line(seg(13.5, 10, 15, 4)),
        line(poly([(7.7, 3), (9, 5), (10.3, 3)], r=0)),
        line(poly([(10.7, 2), (12, 4), (13.3, 2)], r=0)),
        line(poly([(13.7, 3), (15, 5), (16.3, 3)], r=0)),
        line("M9.3 13C4 13 4 20 9.4 19"),
    ]


@icon("catapult", CAT, "Wheeled siege catapult with a throwing arm and cup",
      tags=["catapult", "siege", "launcher", "medieval", "war machine", "trebuchet", "castle"])
def _(S):
    return [
        shell(rect(4, 14.5, 14, 3, pick(S, 0, 1))),
        shell(circle(7, 19.3, 2.3)),
        shell(circle(15.5, 19.3, 2.3)),
        line(seg(7.5, 14.5, 16.5, 5.5)),
        line("M13.5 4.5Q17 9 20.5 4.5"),
        dot(17, 3, 1.5),
    ]


def arrowhead(cx, cy, r, ang, size=2.6, cw=True):
    """Open chevron at the end of a circular arc (angle in degrees, clockwise on screen)."""
    a = math.radians(ang)
    px, py = cx + r * math.cos(a), cy + r * math.sin(a)
    t = a + (math.pi / 2 if cw else -math.pi / 2)  # tangent direction
    tx, ty = math.cos(t), math.sin(t)
    nx, ny = math.cos(a), math.sin(a)
    tip = (px + tx * size * 0.5, py + ty * size * 0.5)
    b1 = (px - tx * size * 0.5 + nx * size * 0.9, py - ty * size * 0.5 + ny * size * 0.9)
    b2 = (px - tx * size * 0.5 - nx * size * 0.9, py - ty * size * 0.5 - ny * size * 0.9)
    return poly([b1, tip, b2])


@icon("cannon", CAT, "Old cannon on a wheeled carriage with a cannonball beside it",
      tags=["cannon", "artillery", "pirate", "siege", "gunpowder", "fort", "historic weapon"])
def _(S):
    barrel = poly([(3.5, 8), (16, 8), (18, 7), (18, 13), (16, 12), (3.5, 12)], closed=True, r=S.r)
    return rotparts([shell(barrel)], -22, 11, 10) + [
        shell(circle(9.5, 17, 3.8)),
        dot(9.5, 17, 1.1),
        shell(circle(19.5, 19.5, 2.2)),
    ]


@icon("knight-helmet", CAT, "Closed great helm with an eye slit, center ridge and breathing holes",
      tags=["helm", "helmet", "knight", "armor", "medieval", "visor", "great helm"])
def _(S):
    body = ("M5 21L6 9A6 6 0 0 1 18 9L19 21Z" if S.name == "rounded"
            else "M5 21L6 8L9 3.5H15L18 8L19 21Z")
    return [
        shell(body),
        detail(seg(5.6, 11, 18.4, 11)),
        detail(seg(12, 3.5, 12, 11)),
        dot(8.5, 15.5, 1.1), dot(15.5, 15.5, 1.1), dot(8.5, 18.6, 1.1), dot(15.5, 18.6, 1.1),
    ]


@icon("horned-helmet", CAT, "Round helmet with a nose guard and a curved horn on each side",
      tags=["viking", "horned helmet", "helmet", "warrior", "norse", "armor", "barbarian"])
def _(S):
    dome = "M5 16.5V12A7 7 0 0 1 19 12V16.5Z" if S.name == "rounded" else "M5 16.5V11L8.5 6H15.5L19 11V16.5Z"
    return [
        shell(dome),
        detail(seg(5, 13.5, 19, 13.5)),
        line(seg(12, 16.5, 12, 20.5)),
        line("M5 12C1.5 12 1.5 7.5 3 3"),
        line("M19 12C22.5 12 22.5 7.5 21 3"),
    ]


@icon("chestplate", CAT, "Front view of a metal breastplate with flared shoulder guards and a center ridge",
      tags=["breastplate", "armor", "cuirass", "knight", "medieval", "rpg", "plate armor"])
def _(S):
    pts = [(8, 3), (12, 6.5), (16, 3), (21, 5), (21, 10), (17.5, 13), (16.5, 21), (7.5, 21), (6.5, 13), (3, 10), (3, 5)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(12, 9.5, 12, 21)),
        detail("M6.5 15Q12 12.5 17.5 15" if S.name == "rounded" else "M6.5 15L12 13L17.5 15"),
    ]


@icon("gauntlet", CAT, "Armored glove with finger plates and a flared cuff",
      tags=["gauntlet", "armored glove", "knight", "armor", "medieval", "fist", "rpg"])
def _(S):
    return [
        shell(poly([(6.5, 16), (6.5, 4.5), (18, 4.5), (18, 16)], closed=True, r=S.r)),
        detail(seg(10.3, 4.5, 10.3, 10.5)),
        detail(seg(14.2, 4.5, 14.2, 10.5)),
        detail(seg(6.5, 10.5, 18, 10.5)),
        line(poly([(6.5, 13), (3, 10.5), (3, 7)], r=S.r)),
        shell(poly([(7.5, 16.5), (17, 16.5), (19.5, 21.5), (5, 21.5)], closed=True, r=S.r)),
    ]


@icon("chainmail-shirt", CAT, "Short sleeved shirt filled with a pattern of small rings",
      tags=["chainmail", "chain mail", "mail armor", "hauberk", "armor", "medieval", "rings"])
def _(S):
    body = [(8, 3), (3, 6), (5, 10), (7, 9), (7, 21), (17, 21), (17, 9), (19, 10), (21, 6), (16, 3)]
    return [
        shell(poly(body, closed=True, r=S.r)),
        detail("M8 3Q12 7.5 16 3"),
        dot(10.3, 13, 1.1), dot(13.7, 13, 1.1), dot(12, 16, 1.1), dot(10.3, 19, 1.1), dot(13.7, 19, 1.1),
    ]


@icon("life-counter", CAT, "Round dial with a number window and up and down arrows",
      tags=["life counter", "score dial", "tally", "life points", "card game", "tabletop", "counter"])
def _(S):
    ring = circle(12, 12, 10) if S.name == "rounded" else poly(regular(12, 12, 10.2, 10, -90), closed=True)
    return [
        shell(ring),
        detail(rect(7.5, 9.5, 9, 5, pick(S, 0, 1.5))),
        detail(poly([(10, 7), (12, 5.2), (14, 7)], r=0)),
        detail(poly([(10, 17), (12, 18.8), (14, 17)], r=0)),
    ]


@icon("photo-booth-props", CAT, "Mustache and a pair of glasses each held up on a stick",
      tags=["photo booth", "props", "mustache", "glasses", "party", "selfie", "costume"])
def _(S):
    stache = ("M2.5 11.5C2.5 8 5 7 6.5 8.5C8 7 10.5 8 10.5 11.5C9 10 7.8 10 6.5 11C5.2 10 4 10 2.5 11.5Z"
              if S.name == "rounded" else "M2.5 11.5L3 7.5L6.5 9L10 7.5L10.5 11.5L8 10L6.5 11L5 10Z")
    return [
        shell(stache),
        shell(circle(15.7, 7.5, 2.2)),
        shell(circle(19.3, 7.5, 2.2)),
        line(seg(6.5, 11.5, 8, 21.5)),
        line(seg(17.5, 10, 16, 21.5)),
    ]


@icon("blindfold", CAT, "Cloth band tied across a face outline with its ends trailing",
      tags=["blindfold", "eye mask", "pin the tail", "surprise", "guessing game", "party game", "cover eyes"])
def _(S):
    return [
        shell(circle(10.5, 12.5, 8) if S.name == "rounded" else poly(regular(10.5, 12.5, 8.3, 10, -90), closed=True)),
        detail(rect(3, 8.5, 15, 5, pick(S, 0, 1.5))),
        line(seg(8, 18, 13, 18)),
        line(poly([(18, 10), (21.5, 7.5)], r=0)),
        line(poly([(18, 12), (21.5, 15.5)], r=0)),
    ]


@icon("bobbing-for-apples", CAT, "Tub of water with two apples floating in it",
      tags=["bobbing apples", "apple bobbing", "halloween", "party game", "water tub", "autumn", "fair game"])
def _(S):
    return [
        shell(poly([(3, 11), (21, 11), (19.5, 21.5), (4.5, 21.5)], closed=True, r=S.r)),
        detail("M6.5 16Q8.5 14.5 10.5 16T14.5 16T18 16" if S.name == "rounded" else "M6.5 16L8.5 14.5L10.5 16L12.5 14.5L14.5 16L16.5 14.5L18 16"),
        shell(circle(8, 7.3, 2.4)),
        shell(circle(15.5, 7.3, 2.4)),
        line(seg(8, 4.9, 8.8, 2.8)),
        line(seg(15.5, 4.9, 16.3, 2.8)),
    ]


@icon("charades", CAT, "Figure miming with one raised arm beside a question mark speech bubble",
      tags=["charades", "mime", "acting game", "guessing game", "party game", "gesture", "pantomime"])
def _(S):
    return [
        shell(circle(6, 11.5, 2.2)),
        line(seg(6, 14, 6, 18.5)),
        line(poly([(3, 22), (6, 18.5), (9, 22)], r=S.r)),
        line(poly([(6, 15.5), (9.5, 13.5), (11, 11)], r=S.r)),
        line(seg(6, 15.5, 3, 17)),
        shell(poly([(10.5, 2), (22, 2), (22, 9.5), (15.5, 9.5), (12.5, 12.5), (12.5, 9.5), (10.5, 9.5)], closed=True, r=S.r)),
        detail("M14.5 4.8A1.7 1.7 0 1 1 17 6.4Q16.4 6.8 16.4 7.8"),
    ]


def glyph(outer, inner=None):
    p = P(outer)
    if inner:
        p = D(p, P(inner))
    return Part("dot", path_to_d(p))


@icon("truth-or-dare", CAT, "Two tilted cards, one marked T and one marked D",
      tags=["truth or dare", "party game", "cards", "dare", "question cards", "sleepover", "challenge"])
def _(S):
    t = glyph(poly([(6, 8.5), (10, 8.5), (10, 10.3), (9, 10.3), (9, 15), (7, 15), (7, 10.3), (6, 10.3)], closed=True))
    left = [shell(rect(3, 4.5, 8.5, 14, pick(S, 0, 2))), Part("dot", poly([(5.2, 8), (9.8, 8), (9.8, 9.8), (8.6, 9.8), (8.6, 15), (6.4, 15), (6.4, 9.8), (5.2, 9.8)], closed=True))]
    right = [shell(rect(12.5, 5.5, 8.5, 14, pick(S, 0, 2))),
             glyph("M14.6 9H16.8A3 3 0 0 1 16.8 15H14.6Z", "M16.4 10.6A1.4 1.4 0 0 1 16.4 13.4Z")]
    return rotparts(left, -10, 7.25, 11.5) + rotparts(right, 10, 16.75, 12.5)


@icon("spin-the-bottle", CAT, "Bottle lying on its side with circular arrows around it",
      tags=["spin the bottle", "party game", "bottle", "spinner", "rotate", "game night", "spin"])
def _(S):
    bottle = ("M6.5 9.6H12.5L15 11H18V13H15L12.5 14.4H6.5Z" if S.name == "line"
              else "M8 9.6H12.5Q14 9.6 15 11H17.5V13H15Q14 14.4 12.5 14.4H8A1.6 1.6 0 0 1 6.5 12.8V11.2A1.6 1.6 0 0 1 8 9.6Z")
    return [
        shell(bottle),
        line(arc(12, 12, 9.5, 215, 325)),
        line(arrowhead(12, 12, 9.5, 325, 3)),
        line(arc(12, 12, 9.5, 35, 145)),
        line(arrowhead(12, 12, 9.5, 145, 3)),
    ]


@icon("hot-potato", CAT, "Steaming potato caught between two open hands",
      tags=["hot potato", "pass the parcel", "party game", "toss", "potato", "heat", "kids game"])
def _(S):
    potato = ("M4.5 12C4.5 9.5 8 8 12 8C16.5 8 19.5 10 19 13.2C18.5 16.2 15 17 11.5 17C7.5 17 4.5 15.2 4.5 12Z"
              if S.name == "rounded" else "M4.5 12L7.5 9L13 8L19.5 10.5L19 14.5L14 17L8 16.5L4.5 12Z")
    return [
        shell(potato),
        dot(9.5, 12, 1), dot(14.5, 13.3, 1),
        line("M8.5 5.5Q7 4.3 8.5 3"), line("M12.5 5.5Q11 4.3 12.5 3"), line("M16.5 5.5Q15 4.3 16.5 3"),
        line("M2.5 15.5Q3 21 9.5 21"),
        line("M21.5 15.5Q21 21 14.5 21"),
    ]


@icon("egg-toss", CAT, "Egg flying along a dotted arc between two open hands",
      tags=["egg toss", "egg throwing", "party game", "picnic game", "catch", "egg", "field day"])
def _(S):
    n = 9 if S.name == "line" else 22
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n - math.pi / 2
        pts.append((13.8 + 4.6 * math.cos(t) * (1 + 0.13 * math.sin(t)), 8.6 + 5.8 * math.sin(t)))
    return [
        shell(poly(pts, closed=True, r=0 if S.name == "line" else 0.6)),
        dot(4.2, 13.5, 1.1), dot(5, 10, 1.1), dot(6.5, 7, 1.1),
        line("M2.5 16Q3 21 9 21"),
        line("M21.5 16Q21 21 15 21"),
    ]


def blob(S, cx, cy, r, n=8):
    """Circle for Rounded, faceted polygon for Line."""
    return circle(cx, cy, r) if S.name == "rounded" else poly(regular(cx, cy, r * 1.05, n, -90 + 180 / n), closed=True)


# ============================================================================ yard and field games

@icon("kick-the-can", CAT, "Tin can knocked through the air by a swinging foot above the ground",
      tags=["kick the can", "tin can", "street game", "hide and seek", "kick", "backyard game", "kids game"])
def _(S):
    can = [shell(rect(13.5, 3, 5.5, 8.5, pick(S, 0, 1.5))), detail(seg(13.5, 5.5, 19, 5.5))]
    return rotparts(can, 28, 16.2, 7.2) + [
        line(seg(3.5, 6.5, 7, 14)),
        shell(poly([(6, 14.5), (11.5, 16), (11.5, 19), (6, 19)], closed=True, r=S.r)),
        line(seg(2.5, 21.5, 21.5, 21.5)),
        line(seg(11, 9, 12.5, 7.5)),
    ]


@icon("capture-the-flag", CAT, "Field split by a center line with a flag standing on each side",
      tags=["capture the flag", "field game", "team game", "flag", "outdoor game", "camp game", "territory"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, S.R if S.name == "line" else 4)),
        detail(seg(12, 3.5, 12, 20.5)),
        detail(seg(8.5, 6.5, 8.5, 17)),
        Part("dot", poly([(8.5, 6.5), (4.8, 8.6), (8.5, 10.7)], closed=True)),
        detail(seg(15.5, 6.5, 15.5, 17)),
        Part("dot", poly([(15.5, 6.5), (19.2, 8.6), (15.5, 10.7)], closed=True)),
    ]


@icon("king-of-the-hill", CAT, "Figure with raised arms under a crown standing on top of a mound",
      tags=["king of the hill", "mound", "winner", "top", "champion", "crown", "playground game"])
def _(S):
    mound = "M2.5 21C2.5 17 7 14.5 12 14.5C17 14.5 21.5 17 21.5 21Z" if S.name == "rounded" else "M2.5 21L7 16L9 14.5H15L17 16L21.5 21Z"
    return [
        shell(mound),
        line(poly([(9.5, 6.5), (9.5, 4), (11, 5.5), (12, 3.5), (13, 5.5), (14.5, 4), (14.5, 6.5)], r=0)),
        dot(12, 9.8, 2),
        line(poly([(8, 9.5), (12, 14.5), (16, 9.5)], r=S.r)),
    ]


@icon("dodgeball", CAT, "Figure leaning away from a ball flying in with motion lines",
      tags=["dodgeball", "dodge", "ball game", "gym class", "playground", "avoid", "throw"])
def _(S):
    return [
        dot(5, 6.5, 2),
        line(poly([(5.5, 9.5), (4.5, 15.5)], r=0)),
        line(poly([(2, 21), (4.5, 15.5), (8.5, 21)], r=S.r)),
        line(poly([(5.3, 10.8), (8.3, 8.6)], r=0)),
        line(poly([(5.2, 11.5), (2.6, 14)], r=0)),
        shell(blob(S, 14.2, 11, 3.3)),
        line(seg(19, 8, 22, 8)),
        line(seg(19, 14, 22, 14)),
    ]


@icon("gaga-pit", CAT, "Octagonal walled pit seen from above with a ball in the middle",
      tags=["gaga", "gaga ball", "pit", "octagon", "ball game", "camp game", "arena"])
def _(S):
    return [
        shell(poly(regular(12, 12, 10.4, 8, -67.5), closed=True, r=S.r)),
        detail(poly(regular(12, 12, 6.2, 8, -67.5), closed=True)),
        dot(12, 12, 2.2),
    ]


@icon("obstacle-course", CAT, "Tire, traffic cone and low hurdle in a row with a dotted path over them",
      tags=["obstacle course", "race", "agility", "field day", "training course", "cone", "tire", "hurdle"])
def _(S):
    return [
        shell(blob(S, 5.5, 16.3, 3.4)),
        shell(poly([(12, 12), (14.6, 19.5), (9.4, 19.5)], closed=True)),
        line(poly([(17.5, 20), (17.5, 14.5), (21.5, 14.5), (21.5, 20)], r=S.r)),
        line(seg(2.5, 21.5, 21.5, 21.5)),
        dot(3, 8.5, 1), dot(7.5, 5.5, 1), dot(12, 8, 1), dot(16.5, 5.5, 1), dot(21, 8, 1),
    ]


@icon("button-whirligig", CAT, "Large button spinning on a looped string stretched between two hands",
      tags=["button whirligig", "button spinner", "buzzer toy", "string toy", "spin", "vintage toy", "craft"])
def _(S):
    return [
        shell(blob(S, 12, 12, 4.4)),
        dot(12, 10.4, 1), dot(12, 13.6, 1),
        line(poly([(3, 12), (7.4, 10.2)], r=0)),
        line(poly([(3, 12), (7.4, 13.8)], r=0)),
        line(poly([(21, 12), (16.6, 10.2)], r=0)),
        line(poly([(21, 12), (16.6, 13.8)], r=0)),
        dot(3, 12, 1.6), dot(21, 12, 1.6),
    ]


@icon("croquet-set", CAT, "Croquet mallet beside a wire hoop with a ball in front of it",
      tags=["croquet", "mallet", "hoop", "wicket", "lawn game", "garden game", "yard game"])
def _(S):
    return [
        shell(rect(2, 3, 9, 5, pick(S, 0, 2))),
        line(seg(6.5, 8, 6.5, 21)),
        line("M13 21V15A4.5 4.5 0 0 1 22 15V21" if S.name == "rounded" else "M13 21V14.5L15 11.5H20L22 14.5V21"),
        shell(blob(S, 17.5, 18, 2.2)),
    ]


@icon("bocce-balls", CAT, "Two large balls resting beside a small target ball on the ground",
      tags=["bocce", "boules", "petanque", "lawn game", "target ball", "pallino", "bowls"])
def _(S):
    return [
        shell(blob(S, 6, 13.8, 3.9)),
        shell(blob(S, 15, 13.8, 3.9)),
        dot(20.3, 16.5, 1.6),
        line(seg(2, 20, 22, 20)),
    ]


@icon("kubb", CAT, "Small wooden blocks flanking a taller crowned king block",
      tags=["kubb", "viking chess", "lawn game", "wooden blocks", "king", "throwing game", "yard game"])
def _(S):
    king = [(8.5, 21), (8.5, 5), (10.6, 7.3), (12, 4), (13.4, 7.3), (15.5, 5), (15.5, 21)]
    return [
        shell(poly(king, closed=True, r=0)),
        sq(2.5, 14.5, 3.6, 6.5, pick(S, 0, 1)),
        sq(17.9, 14.5, 3.6, 6.5, pick(S, 0, 1)),
    ]


@icon("shuffleboard-table", CAT, "Long narrow table with a scoring zone at the far end and a puck sliding toward it",
      tags=["shuffleboard", "table shuffleboard", "puck", "bar game", "scoring zone", "sliding game", "pub game"])
def _(S):
    return [
        shell(poly([(6.5, 5.5), (21.5, 5.5), (18, 13), (2.5, 13)], closed=True, r=S.r)),
        detail(seg(14.2, 13, 17.8, 5.5)),
        dot(8.2, 9.3, 1.7),
        line(seg(4.5, 13, 4.5, 20.5)),
        line(seg(16, 13, 16, 20.5)),
    ]


@icon("ladder-toss", CAT, "Ladder frame with rungs and a two ball bola draped over the middle rung",
      tags=["ladder toss", "ladder ball", "bola", "tailgate game", "yard game", "throwing game", "backyard"])
def _(S):
    return [
        line(poly([(8, 21.5), (8, 3), (16, 3), (16, 21.5)], r=S.r)),
        line(seg(8, 7.5, 16, 7.5)),
        line(seg(8, 16.5, 16, 16.5)),
        line(poly([(3.5, 17), (3.5, 12), (20.5, 12), (20.5, 17)], r=0)),
        dot(3.5, 18.8, 1.6), dot(20.5, 18.8, 1.6),
    ]


@icon("roundnet", CAT, "Small round net on short legs with a ball bouncing above it",
      tags=["roundnet", "beach game", "net game", "trampoline net", "bounce", "backyard sport"])
def _(S):
    rim = ellipse(12, 14.5, 9, 3.6) if S.name == "rounded" else poly(regular(12, 14.5, 9.6, 8, -67.5), closed=True)
    if S.name == "line":
        rim = poly([(3, 14.5), (6, 11), (18, 11), (21, 14.5), (18, 18), (6, 18)], closed=True)
    return [
        shell(rim),
        detail(seg(5.5, 14.5, 18.5, 14.5)),
        line(seg(7, 18.2, 6, 21.5)),
        line(seg(17, 18.2, 18, 21.5)),
        shell(blob(S, 12, 5, 2.4)),
    ]


@icon("high-striker", CAT, "Tall strength tester with a bell on top, a sliding puck and a mallet at the base",
      tags=["high striker", "strength tester", "test your strength", "carnival game", "fairground", "bell", "mallet"])
def _(S):
    bell = "M9.5 5.5C9.5 3 10.5 2 12 2C13.5 2 14.5 3 14.5 5.5Z" if S.name == "rounded" else "M9.5 5.5L10.5 3L13.5 3L14.5 5.5Z"
    return [
        shell(bell),
        shell(rect(8.5, 7.5, 7, 13, pick(S, 0, 2))),
        detail(seg(12, 10, 12, 17.5)),
        dot(12, 15, 1.7),
        line(seg(3, 21.5, 15, 21.5)),
        line(seg(18, 21, 20.5, 13)),
        Part("solid", rot_d(rect(17.4, 8.6, 5.6, 3.6, pick(S, 0, 1)), 15, 20, 10.4)),
    ]


@icon("bottle-knockdown", CAT, "Pyramid of six bottles on a stand with a ball flying toward them",
      tags=["milk bottles", "bottle toss", "knock down", "carnival game", "fairground", "ball throw", "pyramid"])
def _(S):
    def bottle(x, y):
        y = y - 1
        pts = [(x - 1.7, y + 4), (x - 1.7, y + 1.7), (x - 0.8, y + 0.9), (x - 0.8, y), (x + 0.8, y), (x + 0.8, y + 0.9),
               (x + 1.7, y + 1.7), (x + 1.7, y + 4)]
        return Part("dot", poly(pts, closed=True, r=pick(S, 0, 0.4)))
    bottles = [bottle(x, 15.3) for x in (11, 15.6, 20.2)] + [bottle(x, 10.1) for x in (13.3, 17.9)] + [bottle(15.6, 4.9)]
    return bottles + [
        line(seg(9, 21, 22, 21)),
        shell(blob(S, 5.5, 10, 3)),
        line(seg(2, 15, 6, 15)),
    ]


# ============================================================================ carnival, rides and toys

@icon("dunk-tank", CAT, "Tank of water with a seat above it and a round target on a post beside it",
      tags=["dunk tank", "dunking booth", "carnival game", "fundraiser", "target", "water", "fair"])
def _(S):
    return [
        shell(rect(2.5, 11, 11.5, 10.5, pick(S, 0, 2))),
        detail("M4.5 15.5Q6 14 7.5 15.5T10.5 15.5T13 15.5" if S.name == "rounded" else "M4.5 15.5L6 14L7.5 15.5L9 14L10.5 15.5L12 14L13 15.5"),
        line(seg(3.5, 6.5, 13, 6.5)),
        shell(blob(S, 18.5, 6.5, 3.2)),
        dot(18.5, 6.5, 0.9),
        line(seg(18.5, 9.7, 18.5, 21.5)),
    ]


@icon("mole-whacking-game", CAT, "Mole popping out of a hole with a mallet raised above it",
      tags=["mole whacking", "mole", "mallet", "arcade game", "carnival game", "hammer game", "reflex game"])
def _(S):
    dome = "M6 18A5 5 0 0 1 16 18Z" if S.name == "rounded" else "M6 18L7.5 12.5L10 10.5H12L14.5 12.5L16 18Z"
    return [
        shell(dome),
        dot(9.3, 14.3, 0.9), dot(12.7, 14.3, 0.9),
        line(seg(2.5, 20.5, 19, 20.5)),
        Part("shell", rot_d(rect(11, 2.6, 8, 4.6, pick(S, 0, 1.5)), 20, 15, 4.9)),
        line(seg(15.3, 7.6, 18.2, 14.5)),
    ]


@icon("game-booth", CAT, "Carnival stall with a striped scalloped awning over a counter and prize shelf",
      tags=["game booth", "carnival stall", "fairground", "stand", "awning", "midway", "fair game"])
def _(S):
    awning = ("M3 4H21V8.5A1.5 1.5 0 0 1 18 8.5A1.5 1.5 0 0 1 15 8.5A1.5 1.5 0 0 1 12 8.5A1.5 1.5 0 0 1 9 8.5A1.5 1.5 0 0 1 6 8.5A1.5 1.5 0 0 1 3 8.5Z"
              if S.name == "rounded" else "M3 4H21V8L19.5 10L18 8L16.5 10L15 8L13.5 10L12 8L10.5 10L9 8L7.5 10L6 8L4.5 10L3 8Z")
    return [
        shell(awning),
        detail(seg(9, 4, 9, 8.5)),
        detail(seg(15, 4, 15, 8.5)),
        line(seg(4.5, 10, 4.5, 21.5)),
        line(seg(19.5, 10, 19.5, 21.5)),
        line(seg(4.5, 18, 19.5, 18)),
        dot(9, 14.3, 1.6), dot(15, 14.3, 1.6),
    ]


@icon("haunted-house", CAT, "Crooked house with a pointed turret, a tilted door and a ghost at the window",
      tags=["haunted house", "spooky", "halloween", "ghost", "creepy", "mansion", "fairground ride"])
def _(S):
    body = [(3, 21.5), (3, 10), (6.5, 3), (10, 10), (13, 8.5), (21, 11.5), (21, 21.5)]
    return [
        shell(poly(body, closed=True, r=S.r)),
        detail(poly([(6.3, 21.5), (6.6, 16.5), (8.5, 15.8)])),
        detail(rect(13.5, 13, 4.5, 4.5, pick(S, 0, 1))),
        dot(15.7, 15.6, 1.1),
    ]


@icon("drop-tower-ride", CAT, "Very tall slim tower with a ring of seats partway up and a cap on top",
      tags=["drop tower", "free fall ride", "amusement park", "thrill ride", "tower ride", "fairground", "theme park"])
def _(S):
    return [
        shell(poly([(9.5, 6), (12, 2.5), (14.5, 6)], closed=True)),
        shell(rect(10, 6, 4, 15.5, pick(S, 0, 1))),
        sq(4, 11, 16, 3.4, pick(S, 0, 1.2)),
        dot(6.3, 17.3, 1.3), dot(9.2, 17.3, 1.3), dot(14.8, 17.3, 1.3), dot(17.7, 17.3, 1.3),
        line(seg(4, 21.5, 20, 21.5)),
    ]


@icon("log-flume-ride", CAT, "Hollow log boat tilting down a steep chute with a splash at the bottom",
      tags=["log flume", "water ride", "amusement park", "splash", "flume", "theme park", "fairground"])
def _(S):
    return [
        line("M2.5 7L9 17.5Q10.5 19.5 13 19.5H21.5" if S.name == "rounded" else "M2.5 7L9.5 18.5L13 19.5H21.5"),
        Part("shell", rot_d(rect(4.1, 7.9, 8, 4.4, pick(S, 0, 2.2)), 56, 8.1, 10.1)),
        dot(16, 14.5, 1.1), dot(19.5, 12.5, 1.1), dot(21, 16, 1.1),
        line("M14.5 17Q15 15 17 14"),
    ]


@icon("hopper-ball", CAT, "Bouncy ball with two curved horn handles sticking up from the top",
      tags=["hopper ball", "hopper", "bouncy ball", "ride on toy", "jumping ball", "kids toy", "bounce"])
def _(S):
    return [
        shell(blob(S, 12, 15, 7, 10)),
        line("M8.5 9C8 5.5 5.5 4 2.8 5"),
        line("M15.5 9C16 5.5 18.5 4 21.2 5"),
        detail(arc(12, 15, 3.4, 200, 290)),
    ]


@icon("jianzi", CAT, "Feather shuttlecock toy with a weighted round base and a fan of feathers",
      tags=["jianzi", "chinese shuttlecock", "feather kick", "footbag", "kick toy", "shuttle", "street game"])
def _(S):
    return [
        shell(rect(8.5, 16, 7, 4.5, pick(S, 0.5, 2.2))),
        line(seg(12, 16, 5, 4)),
        line(seg(12, 16, 8.5, 3)),
        line(seg(12, 16, 12, 2.5)),
        line(seg(12, 16, 15.5, 3)),
        line(seg(12, 16, 19, 4)),
    ]


@icon("daruma-otoshi", CAT, "Stack of wooden discs topped by a round headed doll with a small mallet at the side",
      tags=["daruma otoshi", "daruma drop", "japanese toy", "stacking game", "mallet", "dexterity", "traditional toy"])
def _(S):
    return [
        shell(rect(3.5, 11, 10, 10, pick(S, 0, 1.5))),
        detail(seg(3.5, 14.3, 13.5, 14.3)),
        detail(seg(3.5, 17.6, 13.5, 17.6)),
        shell(blob(S, 8.5, 6.2, 3.4)),
        Part("solid", rect(16.2, 14.5, 3.6, 6.5, pick(S, 0, 1))),
        line(seg(19.8, 17.8, 22, 17.8)),
    ]


@icon("gilli-danda", CAT, "Short pointed peg on the ground with a long stick raised to strike it",
      tags=["gilli danda", "tipcat", "stick game", "street game", "india", "peg", "traditional game"])
def _(S):
    return [
        shell(poly([(2.5, 18.3), (6.5, 16.3), (11.5, 16.3), (15.5, 18.3), (11.5, 20.3), (6.5, 20.3)], closed=True, r=S.r)),
        line(seg(21, 3.5, 9, 14.5)),
        line(seg(17, 18.5, 20, 18.5)),
        dot(21.3, 14.5, 1.1), dot(18.8, 13, 1.1),
    ]


@icon("slingshot", CAT, "Y shaped fork with a rubber band and pouch pulled back",
      tags=["slingshot", "catapult", "catty", "y fork", "rubber band", "toy weapon", "projectile"])
def _(S):
    return [
        line(seg(12, 21.5, 12, 15)),
        line(poly([(5, 4), (12, 15), (19, 4)], r=S.r)),
        line(poly([(5, 4), (12, 8.5), (19, 4)], r=0)),
        dot(12, 9.8, 1.8),
    ]


@icon("boomerang", CAT, "Curved V shaped boomerang with a small spin arrow beside it",
      tags=["boomerang", "throwing stick", "return", "australia", "spinning toy", "comes back", "throw"])
def _(S):
    body = [(2.5, 21), (2.5, 11), (7, 4.5), (15.5, 3.5), (15.5, 7.5), (10.5, 9), (7, 13.5), (7, 21)]
    return [
        shell(poly(body, closed=True, r=S.r)),
        line(arc(17, 16.5, 3.6, 150, 330)),
        line(arrowhead(17, 16.5, 3.6, 330, 2.8)),
    ]


@icon("footbag", CAT, "Small round stitched beanbag ball with four curved panel seams",
      tags=["footbag", "kick bag", "beanbag", "kick ball", "juggling", "stitched ball", "sack"])
def _(S):
    return [
        shell(blob(S, 12, 12, 9, 10)),
        detail("M3.3 10.3Q12 15 20.7 10.3" if S.name == "rounded" else "M3.3 10.3L12 14.2L20.7 10.3"),
        detail("M10.3 3.3Q15 12 10.3 20.7" if S.name == "rounded" else "M10.3 3.3L14.2 12L10.3 20.7"),
    ]


@icon("plate-spinning", CAT, "Plate spinning flat on top of a thin upright stick with motion marks",
      tags=["plate spinning", "spinning plate", "circus", "juggling", "balance", "juggler", "stick trick"])
def _(S):
    plate = ellipse(12, 6.5, 8.5, 2.8) if S.name == "rounded" else poly([(3.5, 6.5), (7, 4), (17, 4), (20.5, 6.5), (17, 9), (7, 9)], closed=True)
    return [
        shell(plate),
        line(seg(12, 9.5, 12, 21.5)),
        line("M6.5 13Q4.5 16 6.5 19"),
        line("M17.5 13Q19.5 16 17.5 19"),
    ]


@icon("cup-stacking", CAT, "Pyramid of stacked cups with three on the bottom row, two above and one on top",
      tags=["cup stacking", "stack racing", "sport stacking", "cups", "pyramid", "stack", "plastic cups"])
def _(S):
    def cup(x, y):
        pts = [(x - 2.7, y), (x + 2.7, y), (x + 1.9, y + 4.6), (x - 1.9, y + 4.6)]
        return Part("dot", poly(pts, closed=True, r=pick(S, 0, 0.5)))
    cups = [cup(x, 15.2) for x in (5.5, 12, 18.5)] + [cup(x, 9.6) for x in (8.75, 15.25)] + [cup(12, 4)]
    return cups + [line(seg(2, 21, 22, 21))]


# ============================================================================ desk games, cue sports, cards and puzzles

@icon("paper-football", CAT, "Folded paper triangle flicked toward a finger goalpost",
      tags=["paper football", "finger football", "desk game", "flick", "goalpost", "classroom game", "triangle"])
def _(S):
    return [
        shell(poly([(2.5, 19.5), (9.5, 19.5), (6, 13.5)], closed=True, r=S.r)),
        dot(9.5, 9.5, 1), dot(12.5, 7.5, 1),
        line(poly([(14.5, 3.5), (14.5, 13), (21.5, 13), (21.5, 3.5)], r=S.r)),
        line(seg(18, 13, 18, 21.5)),
    ]


@icon("milk-caps", CAT, "Stack of round cardboard caps with a thicker slammer disc on top",
      tags=["milk caps", "slammer", "caps game", "flip game", "90s toy", "discs"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 6, pick(S, 1, 3))),
        shell(rect(3.5, 10.5, 17, 4, pick(S, 1, 2))),
        shell(rect(3, 16.5, 18, 4, pick(S, 1, 2))),
    ]


@icon("model-kit-sprue", CAT, "Rectangular plastic frame with small parts attached by thin gates",
      tags=["model kit", "sprue", "plastic model", "scale model", "hobby", "snap kit", "parts frame"])
def _(S):
    return [
        line(rect(2.5, 3, 19, 18, pick(S, 0, 2)), ),
        line(seg(9.5, 4, 9.5, 7.5)),
        Part("solid", rect(7, 7.5, 5, 4.5, pick(S, 0, 1))),
        line(seg(16.5, 4, 16.5, 7.5)),
        Part("solid", circle(16.5, 9.5, 2.2)),
        line(seg(9.5, 15.5, 9.5, 20)),
        Part("solid", rect(6.8, 12.8, 5.4, 3.5, pick(S, 0, 1))),
        line(seg(16.5, 16.5, 16.5, 20)),
        Part("solid", circle(16.5, 14.6, 2.2)),
    ]


@icon("whoopee-cushion", CAT, "Flat round rubber cushion with a short spout and a puff of air rising",
      tags=["whoopee cushion", "prank", "fart cushion", "joke", "gag gift", "party trick", "rubber"])
def _(S):
    body = (ellipse(10.5, 15, 8, 5.2) if S.name == "rounded"
            else poly([(2.5, 15), (5.5, 10), (15.5, 10), (18.5, 15), (15.5, 20), (5.5, 20)], closed=True))
    return [
        shell(body),
        detail("M6.5 14.2Q10.5 12.2 14.5 14.2" if S.name == "rounded" else "M6.5 14.2L10.5 12.5L14.5 14.2"),
        shell(rect(19, 13.3, 3, 3.4, pick(S, 0, 1))),
        dot(18.5, 7.5, 1.1), dot(20.8, 5.2, 1.5), dot(17.2, 4, 1.1),
    ]


@icon("christmas-cracker", CAT, "Paper tube twisted closed at both ends like a large sweet",
      tags=["christmas cracker", "bon bon", "party cracker", "holiday", "xmas", "pull", "surprise"])
def _(S):
    return [
        shell(rect(7.5, 8, 9, 8, pick(S, 0, 2))),
        shell(poly([(7.5, 9), (2.5, 6.5), (2.5, 17.5), (7.5, 15)], closed=True, r=S.r)),
        shell(poly([(16.5, 9), (21.5, 6.5), (21.5, 17.5), (16.5, 15)], closed=True, r=S.r)),
        detail(seg(12, 8, 12, 16)),
    ]


@icon("eight-ball", CAT, "Solid ball with a small white circle holding the number 8",
      tags=["eight ball", "8 ball", "billiards", "pool ball", "black ball", "snooker", "billiard ball"])
def _(S):
    return [
        shell(blob(S, 12, 12, 9.5, 10)),
        detail(circle(12, 10.5, 4.6)),
        dot(12, 9.2, 1.1), dot(12, 12, 1.3),
    ]


@icon("billiard-triangle", CAT, "Triangular rack frame with balls packed tightly inside it",
      tags=["billiard rack", "pool rack", "triangle rack", "racking balls", "snooker", "billiards", "break"])
def _(S):
    return [
        shell(poly([(12, 2.5), (22, 21), (2, 21)], closed=True, r=S.r)),
        dot(12, 11.5, 1.5),
        dot(9.8, 15.5, 1.5), dot(14.2, 15.5, 1.5),
        dot(7.6, 18.6, 1.5), dot(12, 18.6, 1.5), dot(16.4, 18.6, 1.5),
    ]


@icon("cue-chalk", CAT, "Small chalk cube with a hollow worn into its top and a little dust",
      tags=["cue chalk", "pool chalk", "billiards", "chalk cube", "snooker", "cue tip", "bar game"])
def _(S):
    body = ("M4.5 20.5V8.5H8.5A3.5 3.5 0 0 0 15.5 8.5H19.5V20.5Z" if S.name == "rounded"
            else "M4.5 20.5V8.5H8.5L12 12L15.5 8.5H19.5V20.5Z")
    return [
        shell(body),
        detail(seg(4.5, 15.5, 19.5, 15.5)),
        dot(10, 4, 1), dot(13.5, 3, 1), dot(15.5, 5.5, 1),
    ]


@icon("pool-cue", CAT, "Long tapered cue stick with a wrapped butt and a small chalked tip",
      tags=["pool cue", "cue stick", "billiards", "snooker", "pool", "bar game", "cue"])
def _(S):
    parts = [
        shell(poly([(10, 22), (14, 22), (12.9, 6.5), (11.1, 6.5)], closed=True, r=S.r * 0.3)),
        detail(seg(10.3, 17.5, 13.7, 17.5)),
        Part("dot", rect(11, 2, 2, 3.4, pick(S, 0, 0.8))),
    ]
    return rotparts(parts, 45)


@icon("throwing-dart", CAT, "Single dart with a needle tip, slim barrel and four tail flights",
      tags=["dart", "darts", "throwing dart", "pub game", "arrow", "bullseye", "flight"])
def _(S):
    parts = [
        line(seg(12, 1.5, 12, 6)),
        shell(rect(10.4, 6, 3.2, 7, pick(S, 0, 1))),
        line(seg(12, 13, 12, 16.5)),
        shell(poly([(12, 21.5), (12, 16), (7.5, 12.5), (7.5, 18.5)], closed=True, r=S.r * 0.5)),
        shell(poly([(12, 21.5), (12, 16), (16.5, 12.5), (16.5, 18.5)], closed=True, r=S.r * 0.5)),
    ]
    return rotparts(parts, 45)


@icon("card-up-sleeve", CAT, "Shirt cuff at a wrist with the top of a playing card peeking out of the sleeve",
      tags=["card up sleeve", "cheating", "magic trick", "cheat", "ace", "sleight of hand", "poker"])
def _(S):
    return [
        shell(rect(8, 2, 8, 10, pick(S, 0, 1.5))),
        dot(11, 5.6, 1.1),
        shell(rect(5, 11.5, 14, 4.5, pick(S, 0, 1.5))),
        line(seg(6.5, 16, 2.8, 21.5)),
        line(seg(17.5, 16, 21.2, 21.5)),
    ]


@icon("card-trick", CAT, "Deck resting on a hand with one card rising out of it and a sparkle",
      tags=["card trick", "magic", "deck of cards", "magician", "sleight of hand", "pick a card", "conjure"])
def _(S):
    star = [(20.5, 3), (21.4, 5.1), (23.5, 6), (21.4, 6.9), (20.5, 9), (19.6, 6.9), (17.5, 6), (19.6, 5.1)]
    return [
        shell(rect(9, 2.5, 6.5, 9.5, pick(S, 0, 1.5))),
        shell(rect(5.5, 11, 13, 6.5, pick(S, 0, 1.5))),
        line("M3 20Q12 23 21 20" if S.name == "rounded" else "M3 20L12 22L21 20"),
        Part("solid", poly(star, closed=True)),
    ]


@icon("graded-card-slab", CAT, "Trading card sealed in a thick rigid case with a label strip across the top",
      tags=["graded card", "slab", "trading card", "card grading", "collectible", "case", "certified"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, pick(S, 1, 3))),
        detail(seg(3.5, 7.5, 20.5, 7.5)),
        detail(rect(7, 10.5, 10, 8, pick(S, 0, 1))),
    ]


@icon("game-of-goose", CAT, "Square spiral track winding inward to a round goal marker at the center",
      tags=["game of goose", "goose game", "spiral board", "board game", "race game", "track", "roll and move"])
def _(S):
    return [
        line(poly([(3, 21), (3, 3), (21, 3), (21, 21), (8, 21), (8, 8), (16, 8), (16, 14)], r=S.r)),
        dot(12, 14.2, 2.3),
    ]


@icon("logic-grid", CAT, "Square grid of four blocks with crosses in some cells and a dot in another",
      tags=["logic grid", "logic puzzle", "grid puzzle", "deduction", "einstein puzzle", "brain teaser", "elimination"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, pick(S, 0, 3))),
        detail(seg(12, 2.5, 12, 21.5)),
        detail(seg(2.5, 12, 21.5, 12)),
        detail(seg(5.3, 5.3, 9.2, 9.2)), detail(seg(9.2, 5.3, 5.3, 9.2)),
        detail(seg(14.8, 14.8, 18.7, 18.7)), detail(seg(18.7, 14.8, 14.8, 18.7)),
        dot(16.75, 7.25, 1.7),
    ]


@icon("word-wheel", CAT, "Ring of letter segments around a highlighted center letter",
      tags=["word wheel", "letter wheel", "anagram", "word puzzle", "word game", "spin", "letters"])
def _(S):
    parts = [
        shell(blob(S, 12, 12, 9.7, 12)),
        detail(circle(12, 12, 3.6)),
        dot(12, 12, 1.6),
    ]
    for i in range(6):
        a = math.radians(i * 60 + 30)
        parts.append(detail(seg(12 + 3.6 * math.cos(a), 12 + 3.6 * math.sin(a), 12 + 9.7 * math.cos(a), 12 + 9.7 * math.sin(a))))
        b = math.radians(i * 60)
        parts.append(dot(12 + 6.6 * math.cos(b), 12 + 6.6 * math.sin(b), 1.0))
    return parts


@icon("dialogue-tree", CAT, "Speech bubble at the top branching down into two smaller speech bubbles",
      tags=["dialogue tree", "conversation tree", "branching dialogue", "choices", "narrative", "visual novel", "chat options"])
def _(S):
    return [
        shell(rect(6, 2, 12, 7, pick(S, 1, 3))),
        dot(9.5, 5.5, 0.9), dot(12, 5.5, 0.9), dot(14.5, 5.5, 0.9),
        line(seg(12, 9, 12, 12)),
        line(poly([(6.5, 15), (6.5, 12), (17.5, 12), (17.5, 15)], r=0)),
        shell(rect(2.5, 15, 8.5, 6.5, pick(S, 1, 3))),
        shell(rect(13, 15, 8.5, 6.5, pick(S, 1, 3))),
    ]


@icon("battle-standard", CAT, "Tall pole with a crossbar holding a hanging banner with a swallowtail bottom",
      tags=["battle standard", "war banner", "banner", "standard bearer", "flag", "medieval", "rpg"])
def _(S):
    return [
        line(seg(12, 2, 12, 5)),
        dot(12, 2, 1.3),
        line(seg(4.5, 5, 19.5, 5)),
        shell(poly([(6.5, 6), (17.5, 6), (17.5, 17.5), (12, 14), (6.5, 17.5)], closed=True, r=S.r * 0.6)),
        dot(12, 9.5, 1.7),
        line(seg(12, 14, 12, 21.5)),
    ]


@icon("siege-tower", CAT, "Tall wooden tower on wheels with a hinged drop ramp near its top",
      tags=["siege tower", "belfry", "castle assault", "war machine", "medieval", "ramp", "wheels"])
def _(S):
    return [
        shell(rect(3.5, 3, 11.5, 14.5, pick(S, 0, 1.5))),
        detail(seg(3.5, 8, 15, 8)),
        detail(seg(3.5, 12.8, 15, 12.8)),
        shell(blob(S, 6.3, 19.6, 2.3)),
        shell(blob(S, 13, 19.6, 2.3)),
        line(poly([(15, 5.5), (22, 9.5)], r=0)),
        line(seg(19, 7.7, 19, 4)),
    ]


@icon("trebuchet", CAT, "Tall A frame with a long throwing arm, a counterweight box and a sling",
      tags=["trebuchet", "siege engine", "catapult", "counterweight", "medieval", "castle", "war machine"])
def _(S):
    return [
        line(poly([(8, 21.5), (12, 6.5), (16, 21.5)], r=S.r * 0.5)),
        line(seg(9.6, 15.2, 14.4, 15.2)),
        line(seg(4.3, 8.6, 21.5, 3.6)),
        line(seg(4.3, 8.6, 4.3, 10.5)),
        shell(rect(2, 10.5, 4.6, 4.6, pick(S, 0, 1))),
        line(poly([(21.5, 3.6), (21.5, 6.5)], r=0)),
        dot(20, 8.6, 1.5),
    ]
