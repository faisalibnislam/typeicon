"""TypeIcon Core: sports & fitness.

Generic equipment and athletes only: no league, team, tournament or brand marks. Variant badges sit in
the bottom-right (13–23), so identifying detail is kept top/left where the object allows.

Balls share one rule for their seams so Line and Rounded really differ: Line seams are faceted
(straight segments meeting at sharp corners), Rounded seams are smooth curves through the same points.
Athletes follow the people figures (head dot r 2.25, 2 px limbs).
"""
import math
import re

from dsl import LINE, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from dsl import D, I, P, ST, U, filled_region
from geometry import fmt, path_to_d, polar

CAT = "sports"


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


# ============================================================================ balls

@icon("soccer-ball", CAT, "Soccer ball with a central pentagon, seams and edge panels",
      tags=["soccer", "football", "ball", "goal", "match", "futbol"], aliases=["soccer"])
def _(S):
    rr = pick(S, 0, 0.8)
    parts = [shell(circle(12, 12, 9)), Part("dot", poly(regular(12, 12, 3.4, 5), closed=True, r=rr))]
    disc = P(circle(12, 12, 8.5))
    for k in range(5):
        a = -90 + k * 72
        parts.append(detail(seg(*polar(12, 12, 3.2, a), *polar(12, 12, 6.2, a))))
        c = polar(12, 12, 9, a)
        patch = I(P(poly(regular(c[0], c[1], 3.2, 5, a + 180), closed=True, r=rr)), disc)
        parts.append(Part("dot", path_to_d(patch)))
    return parts


@icon("basketball", CAT, "Basketball with its crossing seams",
      tags=["basketball", "ball", "hoop", "nba", "court", "dribble"])
def _(S):
    left = [(5.2, 5.6), (7.8, 12), (5.2, 18.4)]
    return [
        shell(circle(12, 12, 9)),
        detail(seg(12, 3, 12, 21)), detail(seg(3, 12, 21, 12)),
        detail(seam(S, left)), detail(seam(S, mirror(left))),
    ]


@icon("baseball", CAT, "Baseball with curved stitched seams",
      tags=["baseball", "ball", "softball", "pitch", "mlb", "stitches"], aliases=["softball"])
def _(S):
    left = [(8.4, 3.9), (7, 12), (8.4, 20.1)]
    parts = [shell(circle(12, 12, 9)), detail(seam(S, left)), detail(seam(S, mirror(left)))]
    for y in (7.5, 12, 16.5):
        x = 7.25 if y != 12 else 7
        parts.append(detail(seg(x, y, x + 2.6, y - pick(S, 0.8, 0))))
        parts.append(detail(seg(24 - x, y, 24 - x - 2.6, y - pick(S, 0.8, 0))))
    return parts


@icon("tennis-ball", CAT, "Tennis ball with its curving seam",
      tags=["tennis", "ball", "court", "racket", "wimbledon", "padel"])
def _(S):
    left = pick(S, [(4.2, 7.4), (7.4, 9), (8.8, 12), (7.4, 15), (4.2, 16.6)], [(4.2, 7.4), (8.8, 12), (4.2, 16.6)])
    return [shell(circle(12, 12, 9)), detail(seam(S, left)), detail(seam(S, mirror(left)))]


@icon("volleyball", CAT, "Volleyball with three swirling panel seams",
      tags=["volleyball", "ball", "beach volleyball", "net", "spike", "court"])
def _(S):
    parts = [shell(circle(12, 12, 9))]
    for a in (-90, 30, 150):
        parts.append(detail(seam(S, [(12, 12), polar(12, 12, 5, a + 10), polar(12, 12, 9, a + 55)])))
    return parts


@icon("golf", CAT, "Golf flag in the hole on a green, with a ball",
      tags=["golf", "green", "hole", "flagstick", "course", "putt"])
def _(S):
    return [
        line(seg(8, 3, 8, 19)),
        shell(poly([(8, 3), (17, 6.5), (8, 10)], closed=True, r=pick(S, 0, 1))),
        shell(ellipse(8, 19.5, 5, 1.5) if S.name == "rounded" else rect(3, 18.5, 10, 2)),
        shell(circle(17.5, 17.5, 2.5)),
    ]


@icon("hockey", CAT, "Two crossed ice hockey sticks with a puck",
      tags=["ice hockey", "hockey", "puck", "stick", "nhl", "rink"], aliases=["ice-hockey"])
def _(S):
    a = [(3.5, 2.5), (14.5, 18), (20.5, 18)]
    return [
        line(poly(a, r=S.r)), line(poly(mirror(a), r=S.r)),
        shell(rect(9, 3, 6, 2.5, pick(S, 0.5, 1.25))),
    ]


@icon("cricket", CAT, "Cricket bat with a ball",
      tags=["cricket", "bat", "ball", "wicket", "innings", "test match"])
def _(S):
    blade = [(11, 8), (13, 8), (15, 10), (15, 20), (9, 20), (9, 10)]
    bd = poly(blade, closed=True, r=pick(S, 0, 1.5))
    return [
        shell(rot_d(bd, 40, (12, 13))),
        line(rot_d(seg(12, 3, 12, 8), 40, (12, 13))),
        shell(circle(6, 5.5, 2.5)),
    ]


@icon("rugby", CAT, "Oval rugby ball with panel seams",
      tags=["rugby", "rugby ball", "union", "league", "try", "scrum"], aliases=["rugby-ball"])
def _(S):
    top = [(3.2, 12), (12, 9.4), (20.8, 12)]
    bot = [(3.2, 12), (12, 14.6), (20.8, 12)]
    return [
        shell(rot_d(ellipse(12, 12, 9.3, 6.2), -45)),
        detail(rot_d(seam(S, top), -45)), detail(rot_d(seam(S, bot), -45)),
    ]


@icon("american-football", CAT, "American football with laces",
      tags=["american football", "nfl", "gridiron", "touchdown", "football", "superbowl"], aliases=["gridiron"])
def _(S):
    r = 9.5
    lens = f"M3 12A{r} {r} 0 0 1 21 12A{r} {r} 0 0 1 3 12Z"
    parts = [shell(rot_d(lens, -45)), detail(rot_d(seg(7.5, 12, 16.5, 12), -45))]
    for x in (9, 12, 15):
        parts.append(detail(rot_d(seg(x, 10.2, x, 13.8), -45)))
    return parts


_PIN = ("M17 2.5C18.3 2.5 19.1 3.6 19.1 5C19.1 6.5 18.2 7.3 18.2 8.7C18.2 10.5 20.4 11.8 20.4 14.8"
        "C20.4 17 19.6 19 19.3 21H14.7C14.4 19 13.6 17 13.6 14.8C13.6 11.8 15.8 10.5 15.8 8.7"
        "C15.8 7.3 14.9 6.5 14.9 5C14.9 3.6 15.7 2.5 17 2.5Z")
_PIN_R = ("M17 2.5C18.3 2.5 19.1 3.6 19.1 5C19.1 6.5 18.2 7.3 18.2 8.7C18.2 10.5 20.4 11.8 20.4 14.8"
          "C20.4 16.8 19.9 18.5 19.6 19.6Q19.3 21 18.2 21H15.8Q14.7 21 14.4 19.6"
          "C14.1 18.5 13.6 16.8 13.6 14.8C13.6 11.8 15.8 10.5 15.8 8.7"
          "C15.8 7.3 14.9 6.5 14.9 5C14.9 3.6 15.7 2.5 17 2.5Z")


@layered("bowling", "Bowling ball in front of a bowling pin",
         tags=["bowling", "ten pin", "strike", "alley", "pin", "ball"])
def _(S):
    ball = [shell(circle(8.5, 15, 5.8)), dot(7, 12.6, 1), dot(10.4, 12.6, 1), dot(8.7, 15.8, 1)]
    return ball, [shell(pick(S, _PIN, _PIN_R))]


# ============================================================================ strength

@icon("boxing-glove", CAT, "Boxing glove with its thumb and cuff",
      tags=["boxing", "glove", "punch", "fight", "boxer", "martial arts"])
def _(S):
    bottom = pick(S, "H17.5V16.5", "H16C17 21 17.5 20.5 17.5 19.5V16.5")
    body = ("M8 21" + bottom + "C19.2 15.2 20 13.5 20 11V8.5C20 5.2 17.8 3 14.5 3H11.5C8.3 3 6.5 5 6.5 8V9.4"
            "C4.8 9.3 3.5 10.5 3.5 12.3C3.5 14.4 5.4 16 8 16.5Z" if S.name == "line" else
            "M9.5 21" + bottom + "C19.2 15.2 20 13.5 20 11V8.5C20 5.2 17.8 3 14.5 3H11.5C8.3 3 6.5 5 6.5 8V9.4"
            "C4.8 9.3 3.5 10.5 3.5 12.3C3.5 14.4 5.4 16 8 16.5V19.5C8 20.5 8.5 21 9.5 21Z")
    return [shell(body), detail(seg(8, 16.5, 17.5, 16.5)), detail("M6.5 9.4C8.6 9.8 10 11 10.5 13.2")]


@icon("dumbbell", CAT, "Dumbbell with a weight plate at each end",
      tags=["dumbbell", "weights", "gym", "fitness", "workout", "strength"], aliases=["weights"])
def _(S):
    rr = pick(S, 1, 2)
    return [
        shell(rot_d(rect(4.5, 6.5, 4, 11, rr), -45)), shell(rot_d(rect(15.5, 6.5, 4, 11, rr), -45)),
        line(rot_d(seg(8.5, 12, 15.5, 12), -45)),
        line(rot_d(seg(2, 12, 4.5, 12), -45)), line(rot_d(seg(19.5, 12, 22, 12), -45)),
    ]


@icon("kettlebell", CAT, "Kettlebell with its handle",
      tags=["kettlebell", "weights", "gym", "swing", "fitness", "strength"])
def _(S):
    return [
        line(poly([(8, 10.5), (8, 3.5), (16, 3.5), (16, 10.5)], r=pick(S, 1.5, 3.5))),
        shell("M7.8 20.8A6.7 6.7 0 1 1 16.2 20.8Z"),
    ]


@icon("barbell", CAT, "Barbell with heavy plates at both ends",
      tags=["barbell", "weights", "gym", "powerlifting", "bench press", "strength"])
def _(S):
    rr = pick(S, 1, 1.75)
    return [
        shell(rect(5, 4.5, 3.5, 15, rr)), shell(rect(15.5, 4.5, 3.5, 15, rr)),
        line(seg(8.5, 12, 15.5, 12)),
        line(seg(2, 12, 5, 12)), line(seg(19, 12, 22, 12)),
    ]


# ============================================================================ athletes

@icon("yoga", CAT, "Person holding a yoga warrior pose with arms outstretched",
      tags=["yoga", "warrior pose", "stretch", "pilates", "fitness", "balance"])
def _(S):
    return [
        dot(12, 4.5, 2.25),
        line(seg(3, 9.5, 21, 9.5)),
        line(seg(12, 9.5, 12, 14)),
        line(poly([(5, 21), (12, 14), (16.5, 16), (17.5, 21)], r=S.r)),
    ]


@icon("swimming", CAT, "Swimmer doing front crawl above the waves",
      tags=["swim", "swimming", "pool", "freestyle", "water", "triathlon"], aliases=["swimmer"])
def _(S):
    wave = [(3, 18.5), (6, 16.5), (9, 18.5), (12, 16.5), (15, 18.5), (18, 16.5), (21, 18.5)]
    return [
        dot(17, 8, 2.25),
        line(poly([(3.5, 12.5), (9, 12.5), (13.5, 9.5)], r=S.r)),
        line(poly([(9, 12.5), (8, 6.5), (12.5, 4.5)], r=S.r)),
        line(seam(S, wave)),
    ]


@icon("cycling", CAT, "Cyclist riding a bicycle",
      tags=["cycling", "bike", "bicycle", "cyclist", "ride", "tour"], aliases=["cyclist"])
def _(S):
    return [
        line(circle(6, 16.5, 3.5)), line(circle(18, 16.5, 3.5)),
        dot(15.5, 4.5, 2.25),
        line(poly([(15.5, 11.5), (13.5, 8), (9.5, 11), (12, 16.5)], r=S.r)),
        line(seg(6, 16.5, 9.5, 11)),
        line(seg(15.5, 11.5, 18, 16.5)),
    ]


@icon("skiing", CAT, "Skier crouching downhill with a pole",
      tags=["ski", "skiing", "skier", "slope", "winter sports", "downhill"], aliases=["skier"])
def _(S):
    return [
        dot(9.5, 4.5, 2.25),
        line(poly([(10.5, 7.5), (14.5, 11), (10.5, 13.5), (13, 16.5)], r=S.r)),
        line(poly([(10.5, 7.5), (7, 10.5)], r=S.r)),
        line(seg(7, 10.5, 4.5, 16.5)),
        line(poly([(2.5, 17.5), (4, 19.2), (21, 13.5)], r=S.r)),
    ]


@icon("snowboard", CAT, "Snowboard with two bindings",
      tags=["snowboarding", "snowboard", "board", "winter sports", "slope", "halfpipe"], aliases=["snowboarding"])
def _(S):
    board = pick(S, "M9 3.5A3 3 0 0 1 15 3.5L14.5 12L15 20.5A3 3 0 0 1 9 20.5L9.5 12Z",
                 "M8.5 5A3.5 3.5 0 0 1 15.5 5C15.5 7.5 14.6 9.5 14.6 12C14.6 14.5 15.5 16.5 15.5 19A3.5 3.5 0 0 1 8.5 19"
                 "C8.5 16.5 9.4 14.5 9.4 12C9.4 9.5 8.5 7.5 8.5 5Z")
    return [
        shell(rot_d(board, 40)),
        Part("dot", rot_d(rect(10.5, 6.5, 3, 2.5, pick(S, 0, 0.8)), 40)),
        Part("dot", rot_d(rect(10.5, 15, 3, 2.5, pick(S, 0, 0.8)), 40)),
    ]


_BOOT = [(5.5, 3), (11.5, 3), (12, 9), (17.5, 11), (19.5, 13), (19.5, 16), (5.5, 16)]


@icon("ice-skating", CAT, "Ice skate: a laced boot on a blade",
      tags=["ice skate", "skating", "figure skating", "rink", "winter", "blade"], aliases=["ice-skate"])
def _(S):
    return [
        shell(poly(_BOOT, closed=True, r=S.r)),
        detail(seg(8, 7, 11.5, 7)),
        line(seg(8, 16, 8, 19.5)), line(seg(16.5, 16, 16.5, 19.5)),
        line(poly([(3.5, 19.5), (18.5, 19.5), (21, 17)], r=S.r)),
    ]


@icon("skates", CAT, "Roller skate: a boot on four wheels",
      tags=["roller skates", "roller skating", "quad skates", "roller derby", "skate", "wheels"], aliases=["roller-skate"])
def _(S):
    return [
        shell(poly(_BOOT[:-2] + [(19.5, 16.5), (5.5, 16.5)], closed=True, r=S.r)),
        detail(seg(8, 7, 11.5, 7)),
        shell(circle(8, 19.25, 1.75)), shell(circle(16.5, 19.25, 1.75)),
    ]


@icon("surfing", CAT, "Surfboard gliding over a wave",
      tags=["surf", "surfing", "surfboard", "wave", "beach", "ocean"], aliases=["surfboard"])
def _(S):
    board = pick(S, "M21.5 10L15 13H6C4.3 13 3 11.9 3 10.5C3 9.1 4.3 8 6 8H15Z",
                 "M21.5 10C19.5 12 17 13 14 13H6C4.3 13 3 11.9 3 10.5C3 9.1 4.3 8 6 8H14C17 8 19.5 8.7 21.5 10Z")
    c = (12, 10.5)
    return [
        shell(rot_d(board, -25, c)),
        line(seam(S, [(3, 19.5), (6, 17.5), (9, 19.5), (12, 17.5), (15, 19.5), (18, 17.5), (21, 19.5)])),
    ]


@icon("climbing", CAT, "Climber scaling a wall",
      tags=["climbing", "rock climbing", "bouldering", "climber", "wall", "mountaineering"], aliases=["rock-climbing"])
def _(S):
    return [
        line(seg(20.5, 2, 20.5, 22)),
        dot(12, 6.5, 2.25),
        line(poly([(8, 4), (9.5, 9.5), (13.5, 11)], r=S.r)),
        line(poly([(13.5, 11), (15.5, 7), (17.5, 4)], r=S.r)),
        line(seg(13.5, 11, 12.5, 15)),
        line(poly([(12.5, 15), (17, 15.5), (17.5, 19)], r=S.r)),
        line(poly([(12.5, 15), (9.5, 18.5), (10.5, 21.5)], r=S.r)),
    ]


# ============================================================================ winning & officiating

@icon("trophy", CAT, "Trophy cup with two handles on a base",
      tags=["trophy", "cup", "winner", "award", "champion", "prize"], aliases=["cup-trophy"])
def _(S):
    cup = pick(S, "M6.5 3H17.5V8.5C17.5 11.8 15 14.5 12 14.5C9 14.5 6.5 11.8 6.5 8.5Z",
               "M8.5 3H15.5C16.6 3 17.5 3.9 17.5 5V8.5C17.5 11.8 15 14.5 12 14.5C9 14.5 6.5 11.8 6.5 8.5V5C6.5 3.9 7.4 3 8.5 3Z")
    return [
        shell(cup),
        line(poly([(6.5, 5), (3, 5), (3, 8), (6.8, 10.5)], r=S.r)),
        line(poly([(17.5, 5), (21, 5), (21, 8), (17.2, 10.5)], r=S.r)),
        line(seg(12, 14.5, 12, 18)),
        shell(rect(7.5, 18, 9, 3, pick(S, 0, 1.5))),
    ]


@icon("medal", CAT, "Medal with a star, hanging from a ribbon",
      tags=["medal", "award", "winner", "olympics", "achievement", "gold"])
def _(S):
    star = [polar(12, 15.5, 2.6 if k % 2 == 0 else 1.15, -90 + k * 36) for k in range(10)]
    ribbon = [(5.5, 3), (9.5, 3), (12, 7), (14.5, 3), (18.5, 3), (14.5, 10), (9.5, 10)]
    return [
        shell(poly(ribbon, closed=True, r=pick(S, 0, 1))),
        shell(circle(12, 15.5, 5.5)),
        Part("dot", poly(star, closed=True, r=pick(S, 0, 0.3))),
    ]


@icon("podium", CAT, "Winners' podium with first, second and third steps",
      tags=["podium", "ranking", "winners", "leaderboard", "first place", "competition"], aliases=["winners-podium"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 12), (8.5, 12), (8.5, 7), (15.5, 7), (15.5, 15), (21, 15), (21, 21)], closed=True, r=S.r)),
        detail(seg(8.5, 12, 8.5, 21)), detail(seg(15.5, 15, 15.5, 21)),
        detail(poly([(10.8, 11), (12.5, 10), (12.5, 16)], r=S.r)),
    ]


@icon("whistle", CAT, "Referee's whistle",
      tags=["whistle", "referee", "coach", "signal", "foul", "umpire"], aliases=["referee-whistle"])
def _(S):
    end = pick(S, "H21V12.5", "H19.5A1.5 1.5 0 0 1 21 10V11A1.5 1.5 0 0 1 19.5 12.5")
    return [
        shell("M9 8.5" + end + "H14.29A5.5 5.5 0 1 1 9 8.5Z"),
        dot(9, 14, 1.6),
        detail(seg(13.5, 8.5, 13.5, 10.5)),
    ]


@layered("dartboard", "Dartboard with a dart in the bullseye",
         tags=["darts", "dartboard", "bullseye", "pub game", "aim", "throw"], aliases=["darts"])
def _(S):
    board = [shell(circle(11, 13, 8.5)), detail(circle(11, 13, 4.5)), dot(11, 13, 1.5)]
    for a in range(0, 360, 45):
        board.append(detail(seg(*polar(11, 13, 5.5, a + 22.5), *polar(11, 13, 8.5, a + 22.5))))
    dart = [line(seg(11, 13, 18.5, 5.5)),
            shell(poly([(17.5, 6.5), (18, 3), (21, 6)], closed=True, r=pick(S, 0, 0.5)))]
    return dart, board


@icon("bow-arrow", CAT, "Drawn bow with an arrow",
      tags=["bow", "arrow", "archer", "hunting", "longbow", "aim"], aliases=["bow-and-arrow"])
def _(S):
    head = poly([(12, 2), (14.2, 5.8), (9.8, 5.8)], closed=True, r=pick(S, 0, 0.5))
    parts = [
        line("M4 13.5Q12 3.5 20 13.5"),
        line(poly([(4, 13.5), (12, 18), (20, 13.5)], r=S.r)),
        line(seg(12, 5, 12, 21)),
        solid(head),
        line(poly([(9.8, 21), (12, 18.5), (14.2, 21)], r=S.r)),
    ]
    return [Part(p.kind, rot_d(p.d, 45), p.attrs) for p in parts]


@layered("archery", "Archery target on a stand with an arrow in the gold",
         tags=["archery", "target", "archer", "arrow", "bullseye", "range"])
def _(S):
    target = [shell(circle(11, 10, 7.5)), detail(circle(11, 10, 3.5)), dot(11, 10, 1.25),
              line(seg(7.5, 16.5, 5, 21.5)), line(seg(14.5, 16.5, 17, 21.5))]
    arrow = [line(seg(11, 10, 19.5, 3)),
             line(poly([(17, 2.5), (19.5, 3), (20, 5.5)], r=S.r)) if S.name == "rounded" else line(poly([(16.5, 2.5), (19.5, 3), (20.5, 6)]))]
    return arrow, target


# ============================================================================ equipment

@icon("ping-pong", CAT, "Table-tennis paddle with a ball",
      tags=["table tennis", "ping pong", "paddle", "bat", "racket", "ball"], aliases=["table-tennis"])
def _(S):
    c = polar(13.5, 10.5, 7, 135)
    pts = [(-2, -1), (2, -1), (2, 5), (-2, 5)]
    handle = poly([rpt((c[0] + x, c[1] + y), 45, c) for x, y in pts], closed=True, r=pick(S, 0, 1.5))
    return [
        shell(circle(13.5, 10.5, 7)),
        shell(handle),
        shell(circle(4, 4, 1.75)),
    ]


@icon("badminton", CAT, "Badminton shuttlecock",
      tags=["badminton", "shuttlecock", "shuttle", "birdie", "racket sport", "smash"], aliases=["shuttlecock"])
def _(S):
    top = [(4.5, 4.5), (7, 3), (9.5, 4.5), (12, 3), (14.5, 4.5), (17, 3), (19.5, 4.5)]
    skirt = seam(S, top) + "L14.5 15.5H9.5Z"
    return [
        shell(skirt),
        detail(seg(12, 4, 12, 15.5)),
        detail(seg(7.2, 9.5, 16.8, 9.5)),
        shell(pick(S, "M9.5 15.5H14.5V18.5L12 21L9.5 18.5Z", "M9.5 15.5H14.5V18.5A2.5 2.5 0 0 1 9.5 18.5Z")),
    ]


@icon("jersey", CAT, "Sports jersey with a number on the front",
      tags=["jersey", "kit", "shirt", "team", "uniform", "number"], aliases=["sports-jersey"])
def _(S):
    body = [(8.5, 3), (3, 6), (4.5, 10.5), (7, 9.5), (7, 20.5), (17, 20.5), (17, 9.5), (19.5, 10.5), (21, 6), (15.5, 3)]
    return [
        shell(poly(body, closed=True, r=S.r)),
        detail(poly([(8.5, 3), (12, 7), (15.5, 3)], r=S.r)),
        detail(poly([(10, 10.5), (14, 10.5), (11.5, 17)], r=S.r)),
    ]


@icon("finish-flag", CAT, "Chequered finish flag on a pole",
      tags=["finish", "chequered flag", "checkered flag", "race", "racing", "goal"], aliases=["checkered-flag", "chequered-flag"])
def _(S):
    parts = [line(seg(4, 3, 4, 21.5)), shell(rect(4, 3, 16, 10.5, pick(S, 0, 2)))]
    for c in range(4):
        for r in range(3):
            if (c + r) % 2 == 0:
                x, y = 4 + c * 4, 3 + r * 3.5
                parts.append(sq(x, y, 4, 3.5))
    return parts


@icon("scoreboard", CAT, "Scoreboard showing two scores",
      tags=["scoreboard", "score", "match", "result", "points", "tally"], aliases=["score"])
def _(S):
    return [
        shell(rect(2.5, 4, 19, 12.5, S.R)),
        detail(rect(6, 7.5, 4, 5.5, pick(S, 0, 1.5))), detail(rect(14, 7.5, 4, 5.5, pick(S, 0, 1.5))),
        dot(12, 8.8, 0.9), dot(12, 11.8, 0.9),
        line(seg(7, 16.5, 7, 21)), line(seg(17, 16.5, 17, 21)),
    ]


def _clip(p, dvec, box):
    """Clip the infinite line p + t*d to the box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    t0, t1 = -1e9, 1e9
    for pc, dc, lo, hi in ((p[0], dvec[0], x0, x1), (p[1], dvec[1], y0, y1)):
        if abs(dc) < 1e-9:
            continue
        a, b = (lo - pc) / dc, (hi - pc) / dc
        t0, t1 = max(t0, min(a, b)), min(t1, max(a, b))
    if t1 <= t0:
        return None
    return (p[0] + t0 * dvec[0], p[1] + t0 * dvec[1]), (p[0] + t1 * dvec[0], p[1] + t1 * dvec[1])


@icon("goal-net", CAT, "Goal frame with its net",
      tags=["goal", "net", "soccer goal", "score", "posts", "crossbar"], aliases=["soccer-goal"])
def _(S):
    parts = [line(poly([(3, 21.5), (3, 4), (21, 4), (21, 21.5)], r=S.r))]
    for k in range(-4, 5):
        for dv in ((1, 1), (1, -1)):
            c = _clip((12 + k * 7, 12.75), dv, (3, 4, 21, 21.5))
            if c and math.dist(*c) > 2:
                parts.append(detail(seg(*c[0], *c[1])))
    return parts


@icon("baseball-bat", CAT, "Baseball bat with a ball",
      tags=["baseball bat", "bat", "baseball", "softball", "slugger", "swing"])
def _(S):
    bat = pick(S, "M9.5 5A2.5 2.5 0 0 1 14.5 5L13 15.5V19.5H14V21.5H10V19.5H11V15.5Z",
               "M9.5 5A2.5 2.5 0 0 1 14.5 5L13 15.5V19.5H13.2A.8.8 0 0 1 14 20.3V20.7A.8.8 0 0 1 13.2 21.5H10.8"
               "A.8.8 0 0 1 10 20.7V20.3A.8.8 0 0 1 10.8 19.5H11V15.5Z")
    return [shell(rot_d(bat, 45)), shell(circle(5.5, 5.5, 2.5))]


@icon("golf-club", CAT, "Golf club with a ball on the ground",
      tags=["golf club", "iron", "driver", "golf", "swing", "caddie"], aliases=["golf-iron"])
def _(S):
    head = poly([(7.5, 16.5), (9.5, 18.5), (8.5, 21), (3, 21), (3, 19)], closed=True, r=pick(S, 0, 1))
    return [
        line(seg(19, 2.5, 8.2, 17.4)),
        shell(head),
        shell(circle(16, 19, 2)),
    ]


@icon("hockey-stick", CAT, "Ice hockey stick with a taped blade",
      tags=["hockey stick", "stick", "ice hockey", "field hockey", "blade", "slapshot"])
def _(S):
    blade = pick(S, "M10 14.5L12.5 15.7L11 20.5H3V18H9Z", "M10 14.5L12.5 15.7L11.4 19.1C11.1 20 10.4 20.5 9.5 20.5H4.5C3.7 20.5 3 19.8 3 19C3 18.4 3.5 18 4.2 18H9Z")
    return [
        line(seg(18, 2.5, 11.2, 15)),
        shell(blade),
        detail(seg(6.5, 18, 6.5, 20.5)),
    ]


@icon("tennis-racket", CAT, "Tennis racket with strings and a ball",
      tags=["tennis racket", "racquet", "tennis", "squash", "padel", "court"], aliases=["tennis-racquet"])
def _(S):
    c = (14, 10)
    parts = [shell(rot_d(ellipse(14, 10, 5.5, 7), 45, c))]
    for d in (seg(11.75, 4, 11.75, 16), seg(16.25, 4, 16.25, 16), seg(8.5, 7, 19.5, 7), seg(8.5, 13, 19.5, 13)):
        parts.append(detail(rot_d(d, 45, c)))
    parts.append(line(rot_d(seg(14, 17, 14, 19), 45, c)))
    parts.append(shell(rot_d(rect(12.5, 19, 3, 6.5, pick(S, 0.5, 1.5)), 45, c)))
    parts.append(shell(circle(5, 5, 2)))
    return parts


@icon("helmet-sports", CAT, "Sports helmet with a face guard",
      tags=["helmet", "football helmet", "face mask", "protection", "gridiron", "safety"], aliases=["football-helmet"])
def _(S):
    shell_d = pick(S, "M21 17V11.5C21 6.5 17.3 3 12.5 3C8 3 4.6 6 4 10.5H11L12.5 17Z",
                   "M21 15V11.5C21 6.5 17.3 3 12.5 3C8 3 4.6 6 4 10.5H11L12.1 15.3C12.4 16.4 13 17 14 17H19C20.1 17 21 16.1 21 15Z")
    return [
        shell(shell_d),
        dot(16.5, 11.5, 1.5),
        line(poly([(8, 10.5), (3, 13), (3, 17.5), (10, 17.5)], r=S.r)),
        line(seg(3, 14.5 if S.name == "line" else 14.5, 9.5, 14.5)),
    ]


@icon("treadmill", CAT, "Treadmill with its running belt and console",
      tags=["treadmill", "running machine", "gym", "cardio", "fitness", "workout"], aliases=["running-machine"])
def _(S):
    return [
        shell(rect(2.5, 16.5, 17, 4.5, pick(S, 1.5, 2.25))),
        line(poly([(17, 16.5), (19.5, 5.5)], r=S.r)),
        line(poly([(14, 6.5), (21, 4.5)], r=S.r)),
        dot(6, 18.75, 1), dot(16, 18.75, 1),
    ]


@icon("jump-rope", CAT, "Skipping rope with two handles",
      tags=["jump rope", "skipping rope", "skipping", "cardio", "fitness", "playground"], aliases=["skipping-rope"])
def _(S):
    hl = rot_d(rect(4, 2.5, 3.5, 7.5, pick(S, 0.5, 1.75)), -20, (5.75, 10))
    hr = rot_d(rect(16.5, 2.5, 3.5, 7.5, pick(S, 0.5, 1.75)), 20, (18.25, 10))
    return [
        shell(hl), shell(hr),
        line("M5.75 10C5.75 26 18.25 26 18.25 10"),
    ]


@icon("weightlifting", CAT, "Weightlifter holding a barbell overhead",
      tags=["weightlifting", "lifter", "barbell", "olympic lifting", "strength", "gym"], aliases=["weightlifter"])
def _(S):
    return [
        line(seg(2.5, 5, 21.5, 5)),
        line(seg(3.5, 2.5, 3.5, 7.5)), line(seg(20.5, 2.5, 20.5, 7.5)),
        dot(12, 9.5, 2.25),
        line(poly([(6, 5), (8.5, 13), (15.5, 13), (18, 5)], r=S.r)),
        line(seg(12, 13, 12, 16)),
        line(poly([(7.5, 21.5), (12, 16), (16.5, 21.5)], r=S.r)),
    ]


@icon("karate", CAT, "Martial artist throwing a high side kick",
      tags=["karate", "martial arts", "kick", "taekwondo", "judo", "self defense"], aliases=["martial-arts"])
def _(S):
    return [
        dot(7.5, 4.5, 2.25),
        line(poly([(3, 12), (5, 8.5), (9.5, 8), (12, 5.5)], r=S.r)),
        line(seg(8.5, 8.2, 9.5, 14)),
        line(poly([(9.5, 14), (15, 12), (20.5, 10)], r=S.r)),
        line(poly([(9.5, 14), (7, 21)], r=S.r)),
    ]


@icon("fishing-rod", CAT, "Fishing rod with a reel, line and hook",
      tags=["fishing", "rod", "angling", "reel", "hook", "fisherman"], aliases=["fishing"])
def _(S):
    return [
        line(seg(3.5, 20.5, 19, 3.5)),
        line(seg(19, 3.5, 19, 13)),
        line(pick(S, "M19 13V17.5H15.5V15.5", "M19 13V16A2 2 0 0 1 15 16V15.5")),
        shell(circle(9.5, 16.5, 2)),
    ]
