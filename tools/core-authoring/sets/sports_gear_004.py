"""TypeIcon Core: sports gear, batch 004 (golf, bowling, protective gear, para sports, winter and water sports).

Generic equipment and athletes only, drawn from the objects themselves. Figures follow the sports set:
head dot r 2.25 and 2 px limbs.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "sports-gear"


def pick(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


def rot(pts, deg, c=(12.0, 12.0)):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


def rot_path(d, deg, c=(12.0, 12.0)):
    """Rotate an absolute M/L/V/H/Q/Z path about c (reads its numbers pairwise)."""
    import re
    toks = re.findall(r"[MLVHQZ]|-?\d+\.?\d*", d)
    out, i, cmd = [], 0, None
    cur = (0.0, 0.0)
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            i += 1
            if cmd == "Z":
                out.append("Z")
            continue
        if cmd == "H":
            cur = (float(t), cur[1]); i += 1
            q = rot([cur], deg, c)[0]; out.append(f"L{fmt(q[0])} {fmt(q[1])}")
        elif cmd == "V":
            cur = (cur[0], float(t)); i += 1
            q = rot([cur], deg, c)[0]; out.append(f"L{fmt(q[0])} {fmt(q[1])}")
        elif cmd == "Q":
            a = [float(v) for v in toks[i:i + 4]]; i += 4
            q = rot([(a[0], a[1]), (a[2], a[3])], deg, c)
            cur = (a[2], a[3])
            out.append(f"Q{fmt(q[0][0])} {fmt(q[0][1])} {fmt(q[1][0])} {fmt(q[1][1])}")
        else:
            cur = (float(t), float(toks[i + 1])); i += 2
            q = rot([cur], deg, c)[0]
            out.append(f"{cmd}{fmt(q[0])} {fmt(q[1])}")
            if cmd == "M":
                cmd = "L"
    return "".join(out)


def mirror(pts, cx=12.0):
    return [(2 * cx - x, y) for x, y in pts]


def head(x, y):
    return dot(x, y, 2.25)


# ============================================================================ golf

@icon("jockey-cap", CAT, "Rounded riding cap with a short peak and a pom on top",
      tags=["jockey", "cap", "horse racing", "riding hat", "equestrian", "silks"])
def _(S):
    return [
        shell("M3 17A8 8 0 0 1 19 17Z"),
        shell(poly([(17, 17), (22.5, 17), (22.5, 19.5), (17, 19.5)], closed=True, r=pick(S, 0, 1))),
        dot(11, 5.5, 1.75),
        detail("M11 9.5V17"),
        detail("M11 9.5C8.5 11 7.5 13.5 7.5 17"),
        detail("M11 9.5C13.5 11 14.5 13.5 14.5 17"),
    ]


@icon("jousting", CAT, "Heater shield with a long lance and pennant",
      tags=["jousting", "joust", "knight", "lance", "medieval", "tournament", "shield"])
def _(S):
    return [
        line(seg(11, 11, 20, 4)),
        shell(poly([(17.5, 2.5), (22, 2.5), (22, 7.5)], closed=True, r=pick(S, 0, 0.5))),
        shell(pick(S, "M2.5 9.5H13.5V15C13.5 18.5 11 20 8 21.5C5 20 2.5 18.5 2.5 15Z",
                   "M2.5 11.5C2.5 10.4 3.4 9.5 4.5 9.5H11.5C12.6 9.5 13.5 10.4 13.5 11.5V15C13.5 18.5 11 20 8 21.5C5 20 2.5 18.5 2.5 15Z")),
        detail(seg(8, 9.5, 8, 18)),
    ]


@icon("compound-bow", CAT, "Compound bow with a pulley cam at each limb tip and a drawn string",
      tags=["compound bow", "archery", "bow", "cam", "hunting", "archer"])
def _(S):
    return [
        line("M14 5.5Q3.5 12 14 18.5"),
        shell(circle(16, 5, 2)),
        shell(circle(16, 19, 2)),
        line(seg(16, 7, 16, 17)),
        line(seg(8.4, 12, 18.5, 12)),
        solid(poly([(21.5, 12), (18.5, 10.2), (18.5, 13.8)], closed=True)),
    ]


@icon("arrow-fletching", CAT, "Tail of an arrow with three feather vanes and a nock",
      tags=["arrow", "fletching", "feathers", "vanes", "archery", "nock", "shaft"])
def _(S):
    def R(pts):
        return rot(pts, 45)
    left = [(12, 9), (7.5, 5.5), (7.5, 15), (12, 18)]
    return [
        line(poly(R([(12, 3), (12, 20.5)]))),
        shell(poly(R(left), closed=True, r=pick(S, 0, 1))),
        shell(poly(R(mirror(left)), closed=True, r=pick(S, 0, 1))),
        line(poly(R([(10.5, 21.5), (12, 20), (13.5, 21.5)]), r=S.r)),
    ]


@icon("clay-target", CAT, "Flying clay disc with motion lines",
      tags=["clay target", "skeet", "trap shooting", "clay pigeon", "shotgun", "shooting"])
def _(S):
    return [
        shell(rot_ellipse(15, 11, 7.5, 3.5, -18)), dot(15, 11, 1.25),
        line(seg(2.5, 10, 5, 10.5)), line(seg(2.5, 14, 6.5, 14)), line(seg(2.5, 18, 7.5, 17.5)),
    ]


def rot_ellipse(cx, cy, rx, ry, deg):
    """Closed ellipse with its major axis turned by deg."""
    a = math.radians(deg)
    dx, dy = rx * math.cos(a), rx * math.sin(a)
    return (f"M{fmt(cx - dx)} {fmt(cy - dy)}A{fmt(rx)} {fmt(ry)} {fmt(deg)} 1 0 {fmt(cx + dx)} {fmt(cy + dy)}"
            f"A{fmt(rx)} {fmt(ry)} {fmt(deg)} 1 0 {fmt(cx - dx)} {fmt(cy - dy)}Z")


@icon("golf-ball-tee", CAT, "Dimpled golf ball resting on a tee",
      tags=["golf ball", "tee", "golf", "dimples", "tee off", "drive"])
def _(S):
    return [
        shell(circle(12, 8.5, 5.5)),
        dot(9.5, 9, 1), dot(13, 6.5, 1), dot(14.2, 10.6, 1),
        shell(poly([(8, 15.5), (16, 15.5), (13, 18), (12, 20.5), (11, 18)], closed=True, r=pick(S, 0, 0.8))),
    ]


@icon("golf-bag", CAT, "Golf bag with three clubs sticking out of the top",
      tags=["golf bag", "clubs", "caddie", "golf", "carry bag", "course"])
def _(S):
    return [
        line(poly([(9.5, 9), (8.5, 4), (5.5, 3.5)], r=S.r)), line(seg(12, 9, 12, 3)), line(poly([(14.5, 9), (15.5, 4), (18.5, 4)], r=S.r)),
        shell(poly([(7.5, 9), (16.5, 9), (15.5, 21.5), (8.5, 21.5)], closed=True, r=pick(S, 0, 1.5))),
        detail(seg(8, 13.5, 16, 17.5)),
    ]


@icon("golf-putter", CAT, "Putter with a flat blade head and a small ball",
      tags=["putter", "golf club", "putt", "green", "golf", "blade"])
def _(S):
    return [
        line(seg(19, 2.5, 9.5, 17.5)),
        shell(rect(3, 17.5, 11, 3.5, pick(S, 0, 1.75))),
        shell(circle(19, 18.5, 2)),
    ]


@icon("golf-tee", CAT, "Golf tee with a cupped top and pointed peg",
      tags=["golf tee", "tee", "peg", "golf", "tee box", "driving"])
def _(S):
    return [
        shell(poly([(5, 3.5), (19, 3.5), (14.5, 9.5), (9.5, 9.5)], closed=True, r=pick(S, 0, 1))),
        line(seg(12, 9.5, 12, 18)),
        solid(poly([(10.3, 16.5), (13.7, 16.5), (12, 21.5)], closed=True)),
    ]


@icon("golf-glove", CAT, "Golf glove with four fingers, a thumb and a wrist tab",
      tags=["golf glove", "glove", "grip", "hand", "golf", "wrist tab"])
def _(S):
    return [
        shell(poly([(8.5, 21.5), (8.5, 16), (4.5, 12.5), (6.2, 10.5), (9.5, 13), (9.5, 4.5), (20, 4.5), (20, 21.5)],
                   closed=True, r=pick(S, 0, 1.2))),
        detail(seg(12.5, 4.5, 12.5, 11)), detail(seg(15, 4.5, 15, 11)), detail(seg(17.5, 4.5, 17.5, 11)),
        detail(seg(8.5, 18, 20, 18)),
    ]


@icon("divot-tool", CAT, "Two-pronged fork used to repair divots and ball marks on a green",
      tags=["divot tool", "pitch fork", "repair", "green", "golf", "ball mark", "turf"])
def _(S):
    return [
        line(poly(rot([(8.5, 3), (8.5, 10.5), (15.5, 10.5), (15.5, 3)], 45), r=S.r)),
        line(poly(rot([(12, 10.5), (12, 17)], 45))),
        shell(poly(rot([(10.2, 17), (13.8, 17), (13.8, 21.5), (10.2, 21.5)], 45), closed=True, r=pick(S, 0, 1))),
    ]


@icon("golf-driver", CAT, "Driver with a large rounded wood head and a long shaft",
      tags=["driver", "wood", "golf club", "tee shot", "golf", "big head"])
def _(S):
    return [
        line(seg(20, 2.5, 11, 14.5)),
        shell(pick(S, "M2.5 17.5L5 13.5H12L14 17L12.5 20.5H4.5Z",
                   "M2.5 18C2.5 15 4.5 13.5 7 13.5H11.5C13.5 13.5 14.5 15 14.5 17C14.5 19.5 13 20.5 11 20.5H5C3.5 20.5 2.5 19.5 2.5 18Z")),
        detail(seg(4.5, 17, 11.5, 17)) if False else dot(8.5, 17, 1),
    ]


@icon("putting-green", CAT, "Oval putting green with a flag in the cup and a ball nearby",
      tags=["putting green", "flag", "cup", "golf", "putt", "hole", "course"])
def _(S):
    return [
        shell(ellipse(12, 17.5, 9.5, 3.5)),
        line(seg(14.5, 4, 14.5, 17.5)),
        shell(poly([(14.5, 3.5), (20.5, 6), (14.5, 8.5)], closed=True, r=pick(S, 0, 0.8))),
        dot(7, 17.5, 1.25),
    ]


@icon("golf-hole-cup", CAT, "Hole cut into the turf with a golf ball dropping in",
      tags=["golf hole", "cup", "birdie", "putt", "hole in one", "golf", "ball drop"])
def _(S):
    return [
        shell(circle(12, 7.5, 4.5)),
        dot(9.8, 8.8, 1), dot(13, 6.2, 1), dot(14.2, 9.6, 1),
        shell(poly([(2.5, 18), (6, 14.5), (18, 14.5), (21.5, 18), (18, 21.5), (6, 21.5)], closed=True, r=pick(S, 0, 3))),
    ]


@icon("golf-bunker", CAT, "Sand trap beside the green with a golf ball",
      tags=["bunker", "sand trap", "golf", "hazard", "sand", "course", "ball"])
def _(S):
    return [
        shell(poly([(2.5, 15.5), (4.5, 11.5), (10, 10.5), (13, 13), (18, 11), (21.5, 14), (19, 19), (12, 20.5), (6, 19.5)],
                   closed=True, r=pick(S, 0, 3))),
        dot(8, 15, 1), dot(12, 17, 1), dot(16, 15, 1),
        shell(circle(18.5, 5, 2.5)),
    ]


@icon("golf-trolley", CAT, "Push cart with a wheel carrying an upright golf bag",
      tags=["golf trolley", "pull cart", "golf bag", "caddie", "golf", "buggy", "push cart"])
def _(S):
    return [
        line(poly([(8, 5), (7, 2)])), line(poly([(10.5, 5), (11.5, 2)])),
        shell(poly([(4.5, 5), (13, 5), (12.5, 15.5), (5, 15.5)], closed=True, r=pick(S, 0, 1.2))),
        detail(seg(5, 9, 12.8, 12)),
        line(poly([(9, 18.5), (15, 11), (21.5, 11)], r=S.r)),
        shell(circle(9, 18.5, 3.2)),
    ]


@icon("bowling-lane", CAT, "Bowling lane in perspective with arrows and pins at the far end",
      tags=["bowling lane", "alley", "bowling", "pins", "strike", "ten pin", "gutter"])
def _(S):
    return [
        line(seg(2.5, 21.5, 8.5, 10.5)), line(seg(21.5, 21.5, 15.5, 10.5)),
        line(poly([(10, 19), (12, 16), (14, 19)], r=S.r)),
        dot(12, 3.5, 1.4), dot(10, 6.5, 1.4), dot(14, 6.5, 1.4), dot(8, 9.5, 1.4), dot(12, 9.5, 1.4), dot(16, 9.5, 1.4),
    ]


@icon("bowling-shoes", CAT, "Lace-up bowling shoe with a two-tone upper and a smooth sole",
      tags=["bowling shoes", "shoe", "alley", "rental shoes", "footwear", "sole", "bowling"])
def _(S):
    return [
        shell(poly([(3, 18), (3, 7.5), (9, 7.5), (10.5, 12), (16, 13), (21, 16), (21, 18)], closed=True, r=pick(S, 0, 1.2))),
        detail("M11.5 13.5V18"),
        detail(seg(5.5, 11.5, 8, 11.5)),
        line(seg(3, 21, 21, 21)),
    ]


@icon("elbow-pads", CAT, "Padded guard wrapped around the middle of an arm",
      tags=["elbow pads", "elbow guard", "protection", "skating", "skateboard", "safety gear", "knee pads"])
def _(S):
    return [
        line(seg(9, 2.5, 9, 8)), line(seg(15, 2.5, 15, 8)),
        line(seg(9, 16, 9, 21.5)), line(seg(15, 16, 15, 21.5)),
        shell(rect(4.5, 8, 15, 8, pick(S, 1.5, 4))),
        detail("M8 12H16"),
    ]


@icon("wrist-guards", CAT, "Fingerless wrist guard with a hard splint along the palm and two straps",
      tags=["wrist guards", "wrist protector", "splint", "skating", "snowboarding", "safety gear", "brace"])
def _(S):
    return [
        shell(poly([(8, 21.5), (8, 16), (4.5, 12.5), (6.2, 10.5), (9.5, 13), (9.5, 4.5), (20, 4.5), (20, 21.5)],
                   closed=True, r=pick(S, 0, 1.2))),
        detail(seg(14.8, 7.5, 14.8, 13)),
        detail(seg(8, 16.5, 20, 16.5)),
    ]


@icon("chest-protector", CAT, "Padded vest with segmented plates over the chest",
      tags=["chest protector", "body armor", "padding", "vest", "catcher", "safety gear", "protection"])
def _(S):
    return [
        shell(poly([(7, 3), (10, 3), (12, 6), (14, 3), (17, 3), (21, 6), (20, 21.5), (4, 21.5), (3, 6)], closed=True, r=pick(S, 0, 1.5))),
        detail(seg(12, 6.5, 12, 21.5)),
        detail(seg(3.5, 11.5, 20.5, 11.5)),
        detail(seg(3.8, 16.5, 20.2, 16.5)),
    ]


@icon("sports-goggles", CAT, "Wraparound protective goggles with a strap on each side",
      tags=["sports goggles", "eye protection", "squash", "safety glasses", "swim goggles", "eyewear", "basketball"])
def _(S):
    return [
        shell(rect(5.5, 7.5, 13, 9, pick(S, 2, 4.5))),
        detail(seg(12, 7.5, 12, 11)),
        line(seg(2, 12, 5.5, 12)), line(seg(18.5, 12, 22, 12)),
    ]


@icon("compression-sleeve", CAT, "Snug tube sleeve worn on the arm",
      tags=["compression sleeve", "arm sleeve", "sportswear", "recovery", "support", "calf sleeve", "athletic"])
def _(S):
    c = (12, 12)
    return [
        shell(poly(rot([(8, 4), (16, 4), (15.5, 20), (8.5, 20)], 38, c), closed=True, r=pick(S, 0, 1.2))),
        detail(poly(rot([(8.2, 8.5), (15.8, 8.5)], 38, c))),
        detail(poly(rot([(8.4, 12), (15.7, 12)], 38, c))),
        detail(poly(rot([(8.5, 15.5), (15.6, 15.5)], 38, c))),
    ]


@icon("wheelchair-basketball", CAT, "Seated player in a sports wheelchair reaching up with a basketball",
      tags=["wheelchair basketball", "para sport", "paralympic", "adaptive sport", "basketball", "disability", "athlete"])
def _(S):
    return [
        head(9.5, 5.5),
        line(poly([(9.5, 8.5), (8.5, 14), (15, 14), (16, 19)], r=S.r)),
        line(poly([(9.5, 10), (13.5, 9), (16, 6.5)], r=S.r)),
        shell(circle(18.5, 4.5, 2.5)),
        line(circle(8, 17, 4.2)),
    ]


@icon("wheelchair-tennis", CAT, "Seated player in a sports wheelchair swinging a tennis racket",
      tags=["wheelchair tennis", "para sport", "paralympic", "adaptive sport", "tennis", "racket", "disability"])
def _(S):
    return [
        head(8.5, 5),
        line(poly([(8.5, 8), (7.5, 13.5), (14, 13.5), (15, 19)], r=S.r)),
        line(poly([(8.5, 9.5), (12.5, 11), (14.5, 11)], r=S.r)),
        line(seg(14.5, 11, 16.3, 8.2)),
        shell(rot_ellipse(18.5, 6, 4.3, 3.2, -50)),
        line(circle(7, 17, 4.2)),
    ]


@icon("sit-ski", CAT, "Seated skier on a single ski with a pole held at the side",
      tags=["sit ski", "para skiing", "paralympic", "adaptive ski", "winter sports", "monoski", "disability"])
def _(S):
    return [
        head(10.5, 4.5),
        line(poly([(10.5, 7.5), (10, 13.5), (16.5, 13.5), (18.5, 16.5)], r=S.r)),
        line(poly([(10.5, 9), (7, 12), (5, 18)], r=S.r)),
        line(seg(12.5, 13.5, 12.5, 19.5)),
        line(poly([(3, 20.5), (18, 20.5), (21.5, 18)], r=S.r)),
    ]


@icon("goalball", CAT, "Player lying on one side to block a ball that has bell holes",
      tags=["goalball", "para sport", "paralympic", "blind sport", "visually impaired", "block", "adaptive sport"])
def _(S):
    return [
        head(4.5, 15),
        line(seg(7.5, 16, 15, 16)),
        line(poly([(15, 16), (21.5, 16)])),
        line(poly([(9, 16), (9, 9.5)], r=S.r)),
        shell(circle(16.5, 7.5, 3.5)),
        dot(15.5, 6.8, 0.9), dot(17.8, 8.3, 0.9),
    ]


@icon("sitting-volleyball", CAT, "Seated player on the floor reaching up to hit a ball near a low net",
      tags=["sitting volleyball", "para sport", "paralympic", "adaptive sport", "volleyball", "net", "disability"])
def _(S):
    return [
        head(7.5, 8),
        line(poly([(7.5, 11), (7.5, 18.5), (15, 18.5)], r=S.r)),
        line(poly([(7.5, 12.5), (11, 9), (12.5, 6)], r=S.r)),
        shell(circle(14.5, 4.5, 2.5)),
        line(seg(20.5, 11.5, 20.5, 21)), line(seg(18, 11.5, 22, 11.5)),
    ]


@icon("blind-football", CAT, "Runner with an eyeshade band dribbling a ball",
      tags=["blind football", "five-a-side", "para sport", "paralympic", "visually impaired", "eyeshade", "adaptive sport"])
def _(S):
    return [
        head(9.5, 4.5),
        solid(rect(6.2, 4, 6.6, 1.5)),
        line(poly([(9.5, 7.5), (10.5, 13)], r=S.r)),
        line(poly([(10.5, 13), (15, 16), (15, 20.5)], r=S.r)),
        line(poly([(10.5, 13), (7.5, 17), (4, 18)], r=S.r)),
        line(poly([(10, 9), (6.5, 11)], r=S.r)),
        line(poly([(10, 9), (14, 11)], r=S.r)),
        shell(circle(19, 18.5, 2.5)),
    ]


# ============================================================================ strength events, ball sports, spectators

def star(cx, cy, ro, ri, n=5):
    pts = []
    for i in range(n * 2):
        r = ro if i % 2 == 0 else ri
        pts.append(polar(cx, cy, r, -90 + i * 180 / n))
    return pts


@icon("boccia", CAT, "Seated player in a wheelchair rolling a ball down a ramp",
      tags=["boccia", "para sport", "paralympic", "ramp", "wheelchair", "ball", "adaptive sport"])
def _(S):
    return [
        head(7.5, 4.5),
        line(poly([(7.5, 7.5), (7, 13.5), (13, 13.5), (14, 19)], r=S.r)),
        line(poly([(7.5, 9.5), (11, 11), (14, 11.5)], r=S.r)),
        line(seg(14, 11.5, 21.5, 15.5)),
        shell(circle(19.5, 11, 2.2)),
        line(circle(7, 17, 4.2)),
    ]


@icon("caber-toss", CAT, "Athlete balancing a tall log upright against the shoulder",
      tags=["caber toss", "highland games", "log", "scottish games", "strongman", "throw", "heavy event"])
def _(S):
    return [
        head(6, 6.5),
        line(poly([(6, 9.5), (7, 15.5)], r=S.r)),
        line(poly([(5, 21.5), (7, 15.5), (10, 21.5)], r=S.r)),
        line(poly([(6.2, 11), (10, 13.5), (13.5, 13)], r=S.r)),
        shell(poly([(12, 2.5), (18, 2.5), (16.5, 16), (13.5, 16)], closed=True, r=pick(S, 0, 1))),
    ]


@icon("atlas-stone", CAT, "Athlete lifting a large round stone onto a platform",
      tags=["atlas stone", "strongman", "stone lift", "heavy lift", "loading", "strength", "platform"])
def _(S):
    return [
        head(5.5, 6.5),
        line(poly([(5.5, 9.5), (6.5, 15.5)], r=S.r)),
        line(poly([(4, 21.5), (6.5, 15.5), (10, 21.5)], r=S.r)),
        line(poly([(6, 11), (8.5, 14), (11, 12.5)], r=S.r)),
        shell(circle(13.5, 9.5, 4)),
        shell(rect(17, 15, 5, 6.5, pick(S, 0, 1.2))),
    ]


@icon("log-rolling", CAT, "Athlete balancing on a floating log with arms out",
      tags=["log rolling", "birling", "lumberjack", "balance", "water sport", "log", "logger sports"])
def _(S):
    return [
        head(12, 3.5),
        line(poly([(4.5, 7), (12, 8.5), (19.5, 5)], r=S.r)),
        line(seg(12, 8.5, 12, 12.5)),
        line(poly([(8.5, 15), (12, 12.5), (15.5, 15)], r=S.r)),
        shell(rect(3, 15.5, 18, 5.5, pick(S, 1, 2.75))),
        detail(seg(7.5, 18.2, 16.5, 18.2)),
    ]


@icon("axe-throwing", CAT, "Axe flying toward a ringed wooden target",
      tags=["axe throwing", "hatchet", "target", "bullseye", "lumberjack", "league", "throwing"])
def _(S):
    c = (9, 15)
    return [
        shell(circle(17.5, 7.5, 4.8)),
        dot(17.5, 7.5, 1.4),
        line(poly(rot([(9, 22), (9, 8)], -40, c))),
        shell(poly(rot([(9, 8), (9, 13), (13.5, 15), (13.5, 6)], -40, c), closed=True, r=pick(S, 0, 1))),
    ]


@icon("wall-ball", CAT, "Athlete throwing a ball up toward a target line on a wall",
      tags=["wall ball", "medicine ball", "crossfit", "target", "workout", "throw", "fitness"])
def _(S):
    return [
        line(seg(21, 2.5, 21, 21.5)),
        line(seg(16.5, 4.5, 21, 4.5)),
        head(7, 9.5),
        line(poly([(7, 12.5), (7, 16.5)])),
        line(poly([(4.5, 21.5), (7, 16.5), (9.5, 21.5)], r=S.r)),
        line(poly([(7, 13.5), (10, 11), (11.5, 8)], r=S.r)),
        shell(circle(13.5, 5.5, 2.5)),
    ]


@icon("sports-balls", CAT, "Three different sports balls grouped together",
      tags=["sports balls", "soccer ball", "basketball", "tennis ball", "equipment", "ball sports", "pe"])
def _(S):
    return [
        shell(circle(12, 6.5, 4.2)),
        Part("dot", poly(regular(12, 6.5, 1.6, 5), closed=True)),
        shell(circle(6.5, 17.3, 4.2)),
        detail(seg(6.5, 13.1, 6.5, 21.5)),
        detail(seg(2.3, 17.3, 10.7, 17.3)),
        shell(circle(17.5, 17.3, 4.2)),
        detail("M13.6 15.3Q17.5 18.5 21.4 15.3"),
    ]


@icon("match-schedule", CAT, "Calendar page with a ball marking the match day",
      tags=["match schedule", "fixtures", "calendar", "game day", "season", "sports calendar", "kickoff"])
def _(S):
    return [
        shell(rect(3, 5, 18, 16, pick(S, 1.5, 4))),
        line(seg(8, 2.5, 8, 7)), line(seg(16, 2.5, 16, 7)),
        detail(seg(3, 10, 21, 10)),
        dot(7.5, 14.2, 1), dot(11.5, 14.2, 1), dot(7.5, 18, 1),
        detail(circle(16, 16, 2.4)),
    ]


@icon("team-crest", CAT, "Shield badge with a star above a ball",
      tags=["team crest", "club badge", "emblem", "shield", "football club", "team logo", "star"])
def _(S):
    return [
        shell(pick(S, "M4 3.5H20V13C20 17 16.5 19.8 12 21.5C7.5 19.8 4 17 4 13Z",
                   "M4 6C4 4.6 5.1 3.5 6.5 3.5H17.5C18.9 3.5 20 4.6 20 6V13C20 17 16.5 19.8 12 21.5C7.5 19.8 4 17 4 13Z")),
        Part("dot", poly(star(12, 8.6, 3.6, 1.6), closed=True)),
        detail(circle(12, 15, 2.3)),
    ]


@icon("league-standings", CAT, "Table of ranked rows with up and down movement arrows",
      tags=["league table", "standings", "rankings", "leaderboard", "positions", "promotion", "relegation"])
def _(S):
    return [
        dot(4, 5.5, 1.5), line(seg(8, 5.5, 15, 5.5)), solid(poly([(19, 3.7), (21.2, 7), (16.8, 7)], closed=True)),
        dot(4, 12, 1.5), line(seg(8, 12, 15, 12)), solid(poly([(19, 13.8), (21.2, 10.5), (16.8, 10.5)], closed=True)),
        dot(4, 18.5, 1.5), line(seg(8, 18.5, 15, 18.5)), solid(poly([(19, 17), (21.2, 20.3), (16.8, 20.3)], closed=True)),
    ]


@icon("medal-table", CAT, "Table with three medal discs as column headers above rows of counts",
      tags=["medal table", "medal count", "olympics", "standings", "gold silver bronze", "ranking", "games"])
def _(S):
    parts = [line(seg(2.5, 9, 21.5, 9))]
    for x in (5.5, 12, 18.5):
        parts.append(shell(circle(x, 5, 1.75)))
        parts.append(line(seg(x - 1.5, 13.5, x + 1.5, 13.5)))
        parts.append(line(seg(x - 1.5, 18.5, x + 1.5, 18.5)))
    return parts


@icon("stadium-wave", CAT, "Row of spectators raising their arms one after another in a wave",
      tags=["stadium wave", "mexican wave", "crowd", "fans", "spectators", "audience", "cheering"])
def _(S):
    parts = [line(seg(2, 21.5, 22, 21.5))]
    for x, hy in ((4.7, 14.5), (12, 11), (19.3, 7.5)):
        parts.append(dot(x, hy, 1.6))
        parts.append(line(poly([(x - 2.9, hy - 2.5), (x, hy + 3.5), (x + 2.9, hy - 2.5)], r=S.r)))
        parts.append(line(seg(x, hy + 3.5, x, 19)))
    return parts


@icon("stadium-horn", CAT, "Long straight plastic horn that flares wide at the bell",
      tags=["stadium horn", "air horn", "vuvuzela", "fan horn", "noise maker", "cheer", "supporter"])
def _(S):
    return [
        shell(poly([(2.5, 10), (7, 10), (7, 14), (2.5, 14)], closed=True, r=pick(S, 0, 1))),
        shell(poly([(7, 10.5), (21, 4.5), (21, 19.5), (7, 13.5)], closed=True, r=pick(S, 0, 1.2))),
        detail(seg(16.5, 6.5, 16.5, 17.5)),
    ]


@icon("penalty-flag", CAT, "Bunched cloth flag with a weighted knot, thrown by an official",
      tags=["penalty flag", "referee", "foul", "yellow flag", "official", "american football", "challenge"])
def _(S):
    return [
        shell(poly([(4.5, 6.5), (10.5, 5.5), (16, 10), (15.5, 17), (9.5, 14.5), (4, 17)], closed=True, r=pick(S, 0, 2.5))),
        shell(circle(19, 5.5, 2.2)),
        line(seg(16.5, 7, 17.5, 7.8)),
    ]


@icon("down-marker", CAT, "Tall pole topped by a box with a large number",
      tags=["down marker", "first down", "sideline", "chain gang", "american football", "yardage", "pole"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 10, pick(S, 1, 2.5))),
        detail(poly([(10, 8.5), (12.5, 6), (12.5, 10.8)])),
        line(seg(12, 12.5, 12, 21.5)),
        line(seg(8, 21.5, 16, 21.5)),
    ]


@icon("tackling-dummy", CAT, "Tall padded upright bag standing on a flat base",
      tags=["tackling dummy", "blocking dummy", "training", "football practice", "rugby", "drill", "padded bag"])
def _(S):
    return [
        shell(rect(7.5, 2.5, 9, 15, pick(S, 1.5, 4.5))),
        detail(seg(7.5, 8, 16.5, 8)),
        shell(rect(4.5, 18, 15, 3.5, pick(S, 0, 1.75))),
    ]


@icon("archery-arm-guard", CAT, "Curved plate strapped along the inside of the forearm",
      tags=["arm guard", "bracer", "archery", "forearm guard", "protection", "bow", "strap"])
def _(S):
    c = (12, 12)
    plate = [(7.5, 3), (16.5, 3), (15, 12), (16, 21), (8, 21), (9, 12)]
    return [
        shell(poly(rot(plate, 30, c), closed=True, r=pick(S, 0, 1.2))),
        line(poly(rot([(8, 7.5), (16, 7.5)], 30, c))),
        line(poly(rot([(8.5, 16.5), (15.5, 16.5)], 30, c))),
    ]


@icon("mma-gloves", CAT, "Fingerless padded glove with the fingers open and a wrist strap",
      tags=["mma gloves", "fingerless gloves", "grappling", "martial arts", "fight", "cage", "sparring"])
def _(S):
    return [
        line(seg(8.5, 3, 8.5, 8)), line(seg(12, 3, 12, 8)), line(seg(15.5, 3, 15.5, 8)), line(seg(19, 3, 19, 8)),
        shell(poly([(6, 8), (20.5, 8), (20.5, 15), (17.5, 18), (8.5, 18), (6, 15)], closed=True, r=pick(S, 0, 2))),
        line(poly([(6, 12), (3, 9.5)], r=S.r)),
        detail(seg(6, 12.5, 20.5, 12.5)),
        shell(rect(7.5, 18, 10, 3.5, pick(S, 0, 1.5))),
    ]


@icon("rash-guard", CAT, "Fitted long-sleeve top with a high neck",
      tags=["rash guard", "rashie", "swim shirt", "surf", "compression top", "sun protection", "long sleeve"])
def _(S):
    return [
        shell(poly([(9, 3), (15, 3), (21, 6.5), (21.5, 18.5), (18, 18.5), (17.5, 9.5), (17, 21.5), (7, 21.5),
                    (6.5, 9.5), (6, 18.5), (2.5, 18.5), (3, 6.5)], closed=True, r=pick(S, 0, 1.2))),
        detail(seg(9, 6.5, 15, 6.5)),
    ]


@icon("mogul-skiing", CAT, "Skier tucked low and bouncing over a row of snow bumps",
      tags=["mogul skiing", "moguls", "bumps", "freestyle", "ski", "winter sports", "slope"])
def _(S):
    return [
        head(10, 4),
        line(poly([(11, 7), (14, 10.5), (10.5, 13), (12.5, 15.5)], r=S.r)),
        line(poly([(11, 8), (7, 10.5), (4.5, 10)], r=S.r)),
        line(seg(8, 15.5, 18, 14)),
        line(poly([(2.5, 21.5), (5.5, 17.5), (8.5, 21.5), (11.5, 17.5), (14.5, 21.5), (17.5, 17.5), (21.5, 21.5)], r=S.r)),
    ]


@icon("slalom-skiing", CAT, "Skier leaning hard into a turn beside a gate pole",
      tags=["slalom", "gate", "alpine skiing", "giant slalom", "racing", "ski", "winter sports"])
def _(S):
    return [
        line(seg(20.5, 3, 20.5, 13)),
        solid(poly([(20.5, 3), (20.5, 8), (16.5, 5.5)], closed=True)),
        head(5.5, 6.5),
        line(poly([(7, 9), (11, 14), (9, 19)], r=S.r)),
        line(poly([(7.5, 10.5), (11.5, 9.5), (14, 11.5)], r=S.r)),
        line(poly([(3.5, 21), (9.5, 20.5), (16, 17.5)], r=S.r)),
    ]


@icon("ski-touring", CAT, "Skier with a backpack climbing uphill on skis with a pole",
      tags=["ski touring", "backcountry", "skinning", "alpine touring", "uphill", "ski mountaineering", "winter sports"])
def _(S):
    return [
        head(10.5, 4.5),
        shell(poly([(4.5, 8), (8.5, 8), (9, 14), (5, 14)], closed=True, r=pick(S, 0, 1))),
        line(poly([(10.5, 7.5), (11.5, 13.5)], r=S.r)),
        line(poly([(11.5, 13.5), (15, 15.5), (14, 19)], r=S.r)),
        line(poly([(11, 9.5), (16, 11.5), (18, 17.5)], r=S.r)),
        line(poly([(5, 21.5), (20, 15)], r=S.r)),
    ]


@icon("telemark-skiing", CAT, "Skier in a deep lunge with the back heel lifted off the ski",
      tags=["telemark", "free heel", "lunge", "ski", "winter sports", "turn", "skier"])
def _(S):
    return [
        head(11, 4.5),
        line(poly([(11, 7.5), (11.5, 12)], r=S.r)),
        line(poly([(11.5, 12), (16, 14), (15.5, 19)], r=S.r)),
        line(poly([(11.5, 12), (8, 16.5), (4.5, 16)], r=S.r)),
        line(poly([(11, 9), (7.5, 11), (5, 13)], r=S.r)),
        line(seg(2.5, 21, 21, 21)),
    ]


@icon("para-ice-hockey", CAT, "Seated player on a low sled holding two short sticks over the ice",
      tags=["para ice hockey", "sledge hockey", "sled hockey", "paralympic", "adaptive sport", "stick", "puck"])
def _(S):
    return [
        head(12, 4.5),
        line(poly([(12, 7.5), (12, 13), (17, 13), (19, 16)], r=S.r)),
        line(poly([(12, 9), (15, 12), (17, 18.5), (20, 18.5)], r=S.r)),
        line(poly([(12, 9), (8.5, 12), (6.5, 18.5), (3.5, 18.5)], r=S.r)),
        line(seg(12, 13, 12, 17)),
        line(poly([(8.5, 20.5), (17, 20.5)])),
    ]


@icon("wheelchair-curling", CAT, "Seated curler pushing a stone forward with a long delivery stick",
      tags=["wheelchair curling", "curling", "para sport", "paralympic", "stone", "delivery stick", "ice"])
def _(S):
    return [
        head(7, 5),
        line(poly([(7, 8), (6, 13.5), (12, 13.5), (13, 19)], r=S.r)),
        line(poly([(7, 9.5), (11, 12), (16, 15.5)], r=S.r)),
        line(circle(6, 17, 4)),
        shell(rect(16, 16.5, 6, 4, pick(S, 0, 1.75))),
        line(seg(19, 16.5, 19, 14.5)),
    ]


# ============================================================================ winter, water, air and wheels

@icon("ice-dancing", CAT, "Two skaters gliding side by side with their raised hands joined",
      tags=["ice dancing", "pairs skating", "figure skating", "couple", "rink", "winter sports", "skaters"])
def _(S):
    return [
        head(6, 6.5), head(18, 6.5),
        line(poly([(6, 9.5), (6, 14.5)])), line(poly([(18, 9.5), (18, 14.5)])),
        line(poly([(6, 10.5), (9.5, 8), (12, 5.5), (14.5, 8), (18, 10.5)], r=S.r)),
        line(poly([(3.5, 20), (6, 14.5), (9.5, 20)], r=S.r)),
        line(poly([(14.5, 20), (18, 14.5), (20.5, 20)], r=S.r)),
        line(seg(2.5, 21.5, 11, 21.5)), line(seg(13, 21.5, 21.5, 21.5)),
    ]


@icon("ice-yachting", CAT, "Sail craft standing on runner blades on flat ice",
      tags=["ice yachting", "iceboat", "ice sailing", "runners", "frozen lake", "winter sports", "sail"])
def _(S):
    return [
        line(seg(11, 2.5, 11, 16)),
        shell(poly([(11.5, 3.5), (20, 15), (11.5, 15)], closed=True, r=pick(S, 0, 1))),
        line(poly([(2.5, 17.5), (21.5, 17.5)])),
        line(seg(5, 17.5, 5, 21)), line(seg(18.5, 17.5, 18.5, 21)),
        line(seg(2.5, 21.5, 8, 21.5)), line(seg(15.5, 21.5, 21.5, 21.5)),
    ]


@icon("toboggan", CAT, "Long flat wooden sled with a curled front and cross slats",
      tags=["toboggan", "sled", "sledge", "snow", "winter", "slide", "coasting"])
def _(S):
    return [
        line(pick(S, "M2.5 12.5H16L21.5 9V5", "M2.5 12.5H17Q21.5 12.5 21.5 6")),
        line(pick(S, "M2.5 19.5H16L21.5 16V12", "M2.5 19.5H17Q21.5 19.5 21.5 13")),
        line(seg(7, 12.5, 7, 19.5)), line(seg(13, 12.5, 13, 19.5)),
    ]


@icon("kick-sled", CAT, "Small chair on two long runners with an upright handlebar",
      tags=["kick sled", "spark sled", "ice sled", "winter transport", "scandinavian", "runners", "push sled"])
def _(S):
    return [
        line(poly([(2.5, 20.5), (17, 20.5), (21, 16.5)], r=S.r)),
        line(poly([(4, 5), (4, 13), (11, 13)], r=S.r)),
        line(seg(5.5, 13, 5.5, 20.5)), line(seg(10, 13, 10, 20.5)),
        line(poly([(17, 19), (17, 4.5)])), line(seg(13.5, 4.5, 20.5, 4.5)),
    ]


@icon("canoe-slalom", CAT, "Paddler in a kayak passing between two hanging gate poles above the water",
      tags=["canoe slalom", "kayak slalom", "whitewater", "gates", "paddle", "river", "olympic"])
def _(S):
    return [
        line(seg(2.5, 2.5, 21.5, 2.5)),
        line(seg(5, 2.5, 5, 9)), line(seg(19, 2.5, 19, 9)),
        head(12, 8),
        line(seg(8, 14, 16, 10)),
        shell(pick(S, "M3.5 16L7 14.5H17L20.5 16L17 18H7Z", "M3.5 16Q5 14.5 8 14.5H16Q19 14.5 20.5 16Q19 18 16 18H8Q5 18 3.5 16Z")),
        line(seg(2.5, 21.5, 21.5, 21.5)),
    ]


@icon("wing-foiling", CAT, "Rider on a board lifted on a hydrofoil, holding a small inflatable wing",
      tags=["wing foiling", "wing foil", "hydrofoil", "foilboard", "watersport", "wind", "sup foil"])
def _(S):
    return [
        head(8, 4.5),
        line(poly([(8, 7.5), (9, 12.5)])),
        line(poly([(9, 12.5), (6.5, 14.5)])),
        line(seg(9, 12.5, 12, 14.5)),
        line(poly([(8.5, 9), (13, 9)])),
        shell(pick(S, "M16 3L20.5 8.5L16 14Z", "M15.5 3Q22.5 8.5 15.5 14Z")),
        line(seg(3, 14.5, 15, 14.5)),
        line(seg(9, 14.5, 9, 19.5)),
        line(seg(5, 20.5, 13, 20.5)),
    ]


@icon("swim-hand-paddles", CAT, "Flat swim training paddle with holes and a finger strap",
      tags=["hand paddles", "swim paddles", "training", "pool", "swimming", "stroke", "freestyle"])
def _(S):
    return [
        shell(pick(S, poly([(3, 15), (6.5, 7), (14, 3.5), (21, 7.5), (20, 16), (12, 20.5), (6, 19.5)], closed=True),
                   rot_ellipse(12, 12, 10, 7.5, -35))),
        dot(8, 14, 1.1), dot(11.5, 11, 1.1), dot(15, 8, 1.1),
        detail(seg(11.5, 17, 17.5, 13.5)),
    ]


@icon("flip-turn", CAT, "Swimmer tumbling over with the feet reaching for the pool wall",
      tags=["flip turn", "tumble turn", "swimming", "pool wall", "lap", "freestyle", "swimmer"])
def _(S):
    return [
        line(seg(21, 2.5, 21, 21.5)),
        head(6.5, 15.5),
        line("M8.5 14Q10 6.5 16 7.5Q18.5 8 19 12"),
        line(poly([(7, 18.5), (10, 20), (14, 19.5)], r=S.r)),
    ]


@icon("surfcasting", CAT, "Angler on the shore casting a very long rod out over the waves",
      tags=["surfcasting", "beach fishing", "surf fishing", "long rod", "angler", "casting", "shore"])
def _(S):
    return [
        head(5.5, 7),
        line(poly([(5.5, 10), (6.5, 15.5)])),
        line(poly([(4, 21.5), (6.5, 15.5), (9.5, 21.5)], r=S.r)),
        line(poly([(6, 11.5), (9, 10.5)], r=S.r)),
        line(seg(7, 12, 20, 3.5)),
        line(poly([(20, 3.5), (21.5, 9)])),
        line(seam(S, [(12.5, 20.5), (15, 18.5), (17.5, 20.5), (20, 18.5), (22, 20)])),
    ]


def seam(S, pts):
    from dsl import poly as _poly
    if S.name == "line":
        return _poly(pts)
    from geometry import fmt as _f
    n = len(pts)
    d = f"M{_f(pts[0][0])} {_f(pts[0][1])}"
    for i in range(n - 1):
        p1, p2 = pts[i], pts[i + 1]
        p0 = pts[i - 1] if i > 0 else p1
        p3 = pts[i + 2] if i + 2 < n else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{_f(c1[0])} {_f(c1[1])} {_f(c2[0])} {_f(c2[1])} {_f(p2[0])} {_f(p2[1])}"
    return d


@icon("indoor-skydiving", CAT, "Flyer floating in a spread pose above a round wind tunnel fan",
      tags=["indoor skydiving", "wind tunnel", "bodyflight", "freefall", "simulator", "flying", "skydive"])
def _(S):
    return [
        head(12, 3.5),
        line(poly([(5, 6.5), (12, 9), (19, 6.5)], r=S.r)),
        line(seg(12, 9, 12, 12.5)),
        line(poly([(7, 16), (12, 12.5), (17, 16)], r=S.r)),
        shell(rect(4, 18.5, 16, 3, pick(S, 0, 1.5))),
    ]


@icon("bike-polo", CAT, "Cyclist swinging a long mallet at a small ball",
      tags=["bike polo", "cycle polo", "mallet", "bicycle", "hardcourt", "cyclist", "ball game"])
def _(S):
    return [
        line(circle(5, 17.5, 3.5)), line(circle(14, 17.5, 3.5)),
        head(9.5, 4.5),
        line(poly([(5, 17.5), (8, 11.5), (12, 11.5), (14, 17.5)], r=S.r)),
        line(poly([(9.5, 7.5), (8.5, 11.5)])),
        line(poly([(9.5, 8.5), (13, 9.5), (15.5, 11)], r=S.r)),
        line(seg(15.5, 11, 20, 15.5)),
        line(seg(18, 18, 22, 14)),
        dot(21, 20, 1.3),
    ]


@icon("aero-helmet", CAT, "Long teardrop cycling helmet with a pointed tail and a visor",
      tags=["aero helmet", "time trial helmet", "cycling helmet", "tt helmet", "triathlon", "head protection", "aerodynamic"])
def _(S):
    return [
        shell(pick(S, "M2.5 16L10 6.5L16 5L21 8.5L21.5 16Z",
                   "M2.5 16C5.5 11 9 5.5 14 5.5C18.5 5.5 21.5 9 21.5 14V16Z")),
        detail(seg(14, 11, 21.5, 11)),
        line(seg(10, 16, 10, 20.5)), line(seg(17, 16, 17, 20.5)),
    ]


@icon("demolition-derby", CAT, "Two dented cars crashing head on with a burst at the impact point",
      tags=["demolition derby", "car crash", "banger racing", "wreck", "motorsport", "collision", "smash"])
def _(S):
    car = [(2, 19), (2, 12.5), (4.5, 10), (7.5, 10), (9, 13), (11, 13.5), (11, 19)]
    return [
        shell(poly(car, closed=True, r=pick(S, 0, 1))),
        shell(poly(mirror(car), closed=True, r=pick(S, 0, 1))),
        line(seg(12, 3, 12, 8)), line(seg(7.5, 4.5, 9.5, 7.5)), line(seg(16.5, 4.5, 14.5, 7.5)),
        dot(5.5, 20.5, 1.3), dot(18.5, 20.5, 1.3),
    ]


@icon("pit-board", CAT, "Signalling board on a pole showing a position number and lap lines",
      tags=["pit board", "signalling", "pit wall", "racing", "lap count", "position", "motorsport"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 11, pick(S, 1, 2.5))),
        detail(poly([(6.5, 8.5), (9, 6), (9, 10.5)])),
        detail(seg(12.5, 6, 17.5, 6)), detail(seg(12.5, 10, 17.5, 10)),
        line(seg(12, 13.5, 12, 17)),
        shell(rect(10, 17, 4, 4.5, pick(S, 0, 1.5))),
    ]


@icon("motorcycle-wheelie", CAT, "Motorcycle and rider balancing on the rear wheel with the front wheel raised",
      tags=["wheelie", "motorcycle", "stunt riding", "motorbike", "rear wheel", "trick", "rider"])
def _(S):
    return [
        line(circle(6.5, 17, 3.7)),
        line(circle(19, 8, 3)),
        head(10, 4),
        line(poly([(6.5, 17), (11, 13), (16.5, 9.5)], r=S.r)),
        line(poly([(10, 7), (10.5, 12)])),
        line(poly([(10, 8.5), (14, 8.5), (16.5, 9.5)], r=S.r)),
        line(seg(2.5, 21.5, 11, 21.5)),
    ]


@icon("double-end-bag", CAT, "Small round punching bag held taut by elastic cords from ceiling and floor",
      tags=["double end bag", "speed bag", "boxing", "reflex bag", "training", "punching", "cords"])
def _(S):
    return [
        line(seg(6, 2.5, 18, 2.5)), line(seg(6, 21.5, 18, 21.5)),
        line(poly([(12, 2.5), (10, 4), (14, 6), (12, 8)])),
        line(poly([(12, 21.5), (10, 20), (14, 18), (12, 16)])),
        shell(circle(12, 12, 4)),
    ]


@icon("grappling-dummy", CAT, "Heavy human-shaped training dummy with a thick torso and splayed limbs",
      tags=["grappling dummy", "bjj dummy", "wrestling", "judo", "throw dummy", "training", "mat"])
def _(S):
    return [
        shell(circle(12, 4.5, 2.4)),
        shell(rect(8.5, 8.5, 7, 8, pick(S, 1, 3))),
        line(poly([(8.5, 10), (4, 14.5)])), line(poly([(15.5, 10), (20, 14.5)])),
        line(poly([(10, 16.5), (8.5, 21.5)])), line(poly([(14, 16.5), (15.5, 21.5)])),
    ]


@icon("boxing-corner", CAT, "Ring corner post with two ropes, a towel on the rope and a bucket",
      tags=["boxing corner", "boxing ring", "bucket", "towel", "cornerman", "ropes", "between rounds"])
def _(S):
    return [
        line(seg(3.5, 2.5, 3.5, 21.5)),
        line(seg(3.5, 6, 21.5, 6)), line(seg(3.5, 11, 21.5, 11)),
        shell(rect(11, 6, 4.5, 7.5, pick(S, 0, 1.2))),
        shell(poly([(14.5, 16.5), (21.5, 16.5), (20.5, 21.5), (15.5, 21.5)], closed=True, r=pick(S, 0, 1))),
    ]


@icon("gymnastics-clubs", CAT, "Two bottle-shaped gymnastics clubs crossed over each other",
      tags=["gymnastics clubs", "rhythmic gymnastics", "indian clubs", "juggling clubs", "apparatus", "clubs", "swinging"])
def _(S):
    def club(deg):
        c = (12, 12)
        body = poly(rot([(11, 8), (13, 8), (14.5, 14), (14.5, 19), (9.5, 19), (9.5, 14)], deg, c), closed=True, r=pick(S, 0, 1.2))
        hd = rot([(12, 4.5)], deg, c)[0]
        return [shell(body), shell(circle(hd[0], hd[1], 2))]
    return club(-28) + club(28)


@icon("split-leap", CAT, "Gymnast in mid-air with the legs stretched in a full split",
      tags=["split leap", "gymnastics", "dance", "jump", "full split", "leap", "cheerleading"])
def _(S):
    return [
        head(12, 4.5),
        line(seg(12, 7.5, 12, 12)),
        line(poly([(5, 10), (12, 8.5), (19, 5.5)], r=S.r)),
        line(poly([(2.5, 16), (12, 12), (21.5, 16)], r=S.r)),
    ]


@icon("flying-trapeze", CAT, "Performer hanging upside down by the knees from a bar on two ropes",
      tags=["flying trapeze", "trapeze artist", "circus", "swing", "aerial", "acrobat", "catcher"])
def _(S):
    return [
        line(seg(5.5, 2.5, 5.5, 7)), line(seg(18.5, 2.5, 18.5, 7)),
        line(seg(5.5, 7, 18.5, 7)),
        line(seg(12, 7, 12, 14.5)),
        line(poly([(12, 10), (8, 14.5)], r=S.r)), line(poly([(12, 10), (16, 14.5)], r=S.r)),
        head(12, 18.5),
    ]


@icon("bodybuilder-pose", CAT, "Bodybuilder flexing both arms in a double biceps pose",
      tags=["bodybuilder", "double biceps", "flex", "muscles", "physique", "bodybuilding", "posing"])
def _(S):
    return [
        head(12, 4),
        line(seg(12, 7.5, 12, 14)),
        line(poly([(12, 9), (4.5, 9), (4.5, 3.5)], r=S.r)),
        line(poly([(12, 9), (19.5, 9), (19.5, 3.5)], r=S.r)),
        line(poly([(8.5, 21.5), (12, 14), (15.5, 21.5)], r=S.r)),
    ]
