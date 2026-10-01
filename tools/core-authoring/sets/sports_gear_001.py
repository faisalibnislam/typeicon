"""TypeIcon Core: sports gear, part 1 (cricket, baseball, stick and racket sports, ball games, football, rugby).

Objects are drawn flat and simple. People use the shared stick-figure style: head dot r 2.25 and 2 px limbs.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import P, fmt, path_to_d, rotation, transform_path

CAT = "sports-gear"


def pick(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpt(p, deg, c=(12.0, 12.0)):
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))


def rseg(x1, y1, x2, y2, deg, c=(12.0, 12.0)):
    (a, b), (e, f) = rpt((x1, y1), deg, c), rpt((x2, y2), deg, c)
    return seg(a, b, e, f)


def head(x, y, r=2.25):
    return dot(x, y, r)


def ball(x, y, r=2.0):
    return dot(x, y, r)


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


# ============================================================================ cricket and baseball

@icon("cricket-stumps", CAT, "Three cricket stumps with two bails on top",
      tags=["cricket", "wicket", "stumps", "bails", "bowled", "pitch"])
def _(S):
    return [
        line(seg(7, 8, 7, 21)), line(seg(12, 8, 12, 21)), line(seg(17, 8, 17, 21)),
        line(seg(7.5, 4.5, 11.5, 4.5)), line(seg(12.5, 4.5, 16.5, 4.5)),
    ]


@icon("cricket-pads", CAT, "Batting leg pad with ribbed bolsters and straps",
      tags=["cricket", "leg pad", "batting pad", "protection", "guard", "gear"])
def _(S):
    return [
        shell(poly([(8, 2.5), (16, 2.5), (18, 21.5), (6, 21.5)], closed=True, r=pick(S, 0, 2))),
        detail(seg(10, 7, 10, 17.5)), detail(seg(14, 7, 14, 17.5)),
        line(seg(2, 8, 6.5, 8)), line(seg(17.5, 8, 22, 8)),
        line(seg(2, 16, 6, 16)), line(seg(18, 16, 22, 16)),
    ]


@icon("cricket-field", CAT, "Oval cricket ground with a pitch strip in the centre",
      tags=["cricket", "ground", "oval", "pitch", "stadium", "field", "wicket"])
def _(S):
    return [
        shell(pick(S, ellipse(12, 12, 10, 8), rect(2, 4, 20, 16, 8))),
        detail(rect(9.5, 8, 5, 8, pick(S, 0, 1.5))),
    ]


@icon("baseball-glove", CAT, "Baseball fielder's glove with fingers, a thumb and a wrist strap",
      tags=["baseball", "glove", "mitt", "softball", "fielder", "catch", "leather"])
def _(S):
    body = pick(S, "M6 21.5V15.5L3 12.5L4.5 9.5L7 12.5V5H18V21.5Z",
                "M6 21.5V15.8L3.2 13C2.6 12.4 2.8 11.4 3.6 10.8C4.4 10.2 5.4 10.6 6 11.4L7 12.7V6.5C7 5.7 7.7 5 8.5 5H16.5C17.3 5 18 5.7 18 6.5V21.5Z")
    return [
        shell(body),
        detail(seg(10.7, 5, 10.7, 10)), detail(seg(14.3, 5, 14.3, 10)),
        detail(seg(7, 17, 18, 17)),
    ]


@icon("catchers-mitt", CAT, "Round padded catcher's mitt with a deep pocket",
      tags=["baseball", "catcher", "mitt", "glove", "softball", "padded", "behind the plate"])
def _(S):
    return [
        shell(pick(S, rect(4.5, 2.5, 15, 15, 5), circle(12, 10, 7.5))),
        detail(ellipse(12, 10, 2.5, 4)),
        line(seg(8, 21.5, 16, 21.5)),
    ]


@icon("catchers-mask", CAT, "Catcher's mask with a grid of metal bars",
      tags=["baseball", "catcher", "mask", "face guard", "protection", "softball", "umpire"])
def _(S):
    return [
        shell(poly([(4, 3), (20, 3), (20, 14), (15, 21), (9, 21), (4, 14)], closed=True, r=pick(S, 0, 2))),
        detail(seg(5, 8, 19, 8)), detail(seg(5, 12.5, 19, 12.5)),
        detail(seg(12, 4, 12, 20)),
    ]


@icon("batting-helmet", CAT, "Batting helmet with a short brim and an ear flap",
      tags=["baseball", "batter", "helmet", "protection", "softball", "head guard"])
def _(S):
    return [
        shell(pick(S, "M2.5 15.5H5A7 7 0 0 1 19 14.5V20H14.5V15.5Z",
                   "M3.5 15.5H5A7 7 0 0 1 19 14.5V19A1 1 0 0 1 18 20H15.5A1 1 0 0 1 14.5 19V15.5Z")),
        detail(seg(9.5, 9.5, 11.5, 8)),
    ]


@icon("home-plate", CAT, "Five-sided home plate with chalk foul lines",
      tags=["baseball", "plate", "home", "batter's box", "softball", "base", "foul line"])
def _(S):
    return [
        shell(poly([(4, 4), (20, 4), (20, 13), (12, 21), (4, 13)], closed=True, r=pick(S, 0, 2))),
    ]


@icon("baseball-base", CAT, "Square base bag seen at an angle",
      tags=["baseball", "base", "bag", "first base", "second base", "third base", "softball"])
def _(S):
    return [
        shell(poly([(12, 4.5), (21.5, 9.5), (21.5, 14), (12, 19.5), (2.5, 14), (2.5, 9.5)], closed=True, r=pick(S, 0, 1.5))),
        detail(poly([(2.5, 9.5), (12, 14.5), (21.5, 9.5)], r=pick(S, 0, 1.5))),
        detail(seg(12, 14.5, 12, 19.5)),
    ]


@icon("baseball-diamond", CAT, "Diamond infield seen from above with four bases",
      tags=["baseball", "diamond", "infield", "ballpark", "softball", "bases", "field"])
def _(S):
    def base(x, y, h=1.5):
        return Part("dot", poly([(x, y - h), (x + h, y), (x, y + h), (x - h, y)], closed=True))
    return [
        shell(poly([(12, 2.5), (21.5, 12), (12, 21.5), (2.5, 12)], closed=True, r=pick(S, 0, 2))),
        base(12, 7.3), base(16.7, 12), base(7.3, 12), base(12, 16.7),
    ]


@icon("pitching-machine", CAT, "Ball launcher barrel on a tripod firing a ball",
      tags=["baseball", "pitching", "machine", "batting practice", "launcher", "training", "cage"])
def _(S):
    return [
        shell(rot(rect(3.5, 9, 11.5, 6.5, pick(S, 0, 2.5)), -28, 9.5, 12)),
        line(seg(8.5, 15.5, 4.5, 21.5)), line(seg(10.5, 15.5, 14.5, 21.5)),
        ball(19.5, 6, 2),
    ]


# ============================================================================ sticks and mallets

@icon("lacrosse-stick", CAT, "Lacrosse stick with a long shaft and a netted triangular head",
      tags=["lacrosse", "stick", "crosse", "net", "pocket", "head", "field sport"])
def _(S):
    return [
        line(seg(3, 21, 11.5, 12.5)),
        shell("M10.5 13.5L13.5 2.5Q22 2 21.5 10.5Z"),
        detail(seg(12.2, 7.5, 16.6, 11.9)),
    ]


@icon("field-hockey-stick", CAT, "Field hockey stick with a curved hook and a ball",
      tags=["field hockey", "hockey", "stick", "hook", "ball", "turf", "sport"])
def _(S):
    return [
        line(poly([(18, 2.5), (11.5, 16.5), (9.5, 19.5), (4, 19.5)], r=pick(S, 0, 2.5))),
        ball(18, 18.5, 2),
    ]


@icon("hurley-stick", CAT, "Hurling stick with a broad flat blade and a ball",
      tags=["hurling", "hurley", "camogie", "stick", "blade", "sliotar", "gaelic"])
def _(S):
    return [
        line(seg(19, 2.5, 11.5, 14.5)),
        shell(rot(rect(5.5, 13, 7, 8.5, pick(S, 1.5, 3.2)), 25, 9, 17)),
        ball(19, 18.5, 2),
    ]


@icon("polo-mallet", CAT, "Polo mallet with a long cane shaft, a cylindrical head and a ball",
      tags=["polo", "mallet", "horse", "stick", "equestrian", "cane", "sport"])
def _(S):
    return [
        line(rseg(12, 2.5, 12, 15.5, 35)),
        shell(rot(rect(6, 15.5, 12, 4.5, pick(S, 1, 2.2)), 35)),
        ball(19.5, 19.5, 1.8),
    ]


# ============================================================================ racket and net sports

def racket_parts(S, head_d, handle_top, handle_bot, deg=45, w=2.4):
    return [shell(rot(head_d, deg)), line(rot(seg(12, handle_top, 12, handle_bot), deg))]


@icon("pickleball-paddle", CAT, "Solid pickleball paddle with a short handle and a ball",
      tags=["pickleball", "paddle", "racket", "court", "sport", "dink", "wiffle"])
def _(S):
    return [
        shell(rot(rect(7, 2.5, 10, 11.5, pick(S, 2, 4.2)), 45)),
        shell(rot(rect(10.5, 14, 3, 6.5, pick(S, 0.5, 1.5)), 45)),
        ball(5.5, 6, 2.0),
    ]


@icon("padel-racket", CAT, "Solid teardrop padel racket with holes in its face",
      tags=["padel", "racket", "paddle", "tennis", "court", "perforated", "sport"])
def _(S):
    head = pick(S, "M12 2.5L17.5 4.5L18.5 9.5L14.5 15.5H9.5L5.5 9.5L6.5 4.5Z",
                "M12 2.5C16.5 2.5 18.8 5.5 18 9.2C17.3 12.4 14.6 13.8 14.6 15.5H9.4C9.4 13.8 6.7 12.4 6 9.2C5.2 5.5 7.5 2.5 12 2.5Z")
    return [
        shell(rot(head, 45)),
        Part("dot", rot(circle(10, 6, 1.1), 45)), Part("dot", rot(circle(14, 6, 1.1), 45)),
        Part("dot", rot(circle(12, 9.6, 1.1), 45)),
        shell(rot(rect(10.5, 16, 3, 5.5, pick(S, 0.5, 1.5)), 45)),
    ]


@icon("squash-racket", CAT, "Squash racket with a narrow strung head and a small ball",
      tags=["squash", "racket", "racquet", "court", "ball", "strings", "sport"])
def _(S):
    head = pick(S, "M12 2.5L16.5 5L16.5 9.5L13.8 14.5H10.2L7.5 9.5L7.5 5Z",
                "M12 2.5C15 2.5 16.5 5 16.5 8C16.5 11 14.5 12.8 13.8 14.5H10.2C9.5 12.8 7.5 11 7.5 8C7.5 5 9 2.5 12 2.5Z")
    return [
        shell(rot(head, 45)),
        detail(rseg(12, 4.5, 12, 12, 45)),
        line(rseg(12, 14.5, 12, 18.5, 45)),
        shell(rot(rect(10.5, 18.5, 3, 4, pick(S, 0.5, 1.5)), 45)),
        ball(19, 19, 1.8),
    ]


@icon("badminton-racket", CAT, "Light badminton racket with an oval head and a shuttlecock",
      tags=["badminton", "racket", "racquet", "shuttlecock", "birdie", "court", "sport"])
def _(S):
    return [
        shell(rot(ellipse(12, 7.5, 4.5, 5.8), -45)),
        line(rseg(12, 13.3, 12, 21.5, -45)),
        dot(17.2, 8.6, 1.4),
        solid(poly([(18, 7.8), (22, 5.8), (19.6, 2.6)], closed=True)),
    ]


@icon("racquetball-racket", CAT, "Short racquetball racket with a wide head, a wrist cord and a ball",
      tags=["racquetball", "racket", "racquet", "court", "ball", "wrist cord", "sport"])
def _(S):
    return [
        shell(rot(pick(S, rect(6, 2.5, 12, 11, 5), ellipse(12, 8, 6, 5.5)), 45)),
        line(rseg(12, 13.5, 12, 17.5, 45)),
        shell(rot(rect(10.5, 17.5, 3, 4, pick(S, 0.5, 1.5)), 45)),
        ball(19, 19, 1.8),
    ]


@icon("table-tennis-table", CAT, "Table tennis table seen from the side with a net and a ball",
      tags=["table tennis", "ping pong", "table", "net", "ball", "indoor", "sport"])
def _(S):
    return [
        shell(rect(2.5, 11, 19, 3.5, pick(S, 0, 1.5))),
        line(seg(12, 6, 12, 11)),
        line(seg(5, 14.5, 5, 21)), line(seg(19, 14.5, 19, 21)),
        ball(17, 6.5, 1.75),
    ]


@icon("tennis-court", CAT, "Tennis court seen from above with a net line and service boxes",
      tags=["tennis", "court", "net", "service box", "baseline", "clay", "hard court"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, pick(S, 0, 1.5))),
        detail(seg(5, 7.5, 19, 7.5)), detail(seg(5, 16.5, 19, 16.5)), detail(seg(12, 7.5, 12, 16.5)),
        line(seg(2, 12, 22, 12)),
    ]


@icon("tennis-net", CAT, "Low tennis net between two posts with a top band",
      tags=["tennis", "net", "court", "posts", "mesh", "badminton", "sport"])
def _(S):
    return [
        line(seg(3.5, 4.5, 3.5, 21.5)), line(seg(20.5, 4.5, 20.5, 21.5)),
        line(seg(3.5, 7.5, 20.5, 7.5)),
        line(seg(8, 8.5, 8, 17.5)), line(seg(12, 8.5, 12, 17.5)), line(seg(16, 8.5, 16, 17.5)),
        line(seg(3.5, 12.5, 20.5, 12.5)), line(seg(3.5, 17.5, 20.5, 17.5)),
    ]


@icon("tennis-ball-tube", CAT, "Tall ball tube with a lid and rings marking the stacked balls",
      tags=["tennis", "ball", "tube", "can", "pressurised", "stack", "pack"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 3.5, pick(S, 0, 1.5))),
        shell(rect(7, 6, 10, 15.5, pick(S, 0, 2))),
        detail(seg(8, 11.5, 16, 11.5)), detail(seg(8, 16.5, 16, 16.5)),
    ]


@icon("ball-machine", CAT, "Ball launcher on wheels with a hopper and a front chute",
      tags=["ball machine", "launcher", "tennis", "practice", "hopper", "training", "feeder"])
def _(S):
    return [
        shell(poly([(4, 2.5), (14, 2.5), (12, 7), (16, 7), (16, 16), (3.5, 16), (3.5, 7), (6, 7)], closed=True, r=pick(S, 0, 1.2))),
        line(seg(16, 11.5, 19.5, 11.5)),
        ball(21, 11.5, 1.2),
        dot(7, 20, 2), dot(13, 20, 2),
    ]


@icon("basketball-hoop", CAT, "Basketball backboard with a rim and a hanging net",
      tags=["basketball", "hoop", "backboard", "rim", "net", "basket", "goal"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 9.5, pick(S, 0, 2))),
        line(seg(7, 15.5, 17, 15.5)),
        line(poly([(8, 15.5), (10, 21.5), (14, 21.5), (16, 15.5)], r=pick(S, 0, 1))),
        detail(seg(9.5, 19, 14.5, 19)) if False else line(seg(10.5, 18.5, 13.5, 18.5)),
    ]


@icon("basketball-court", CAT, "Half basketball court from above with the key, free-throw arc and three-point arc",
      tags=["basketball", "court", "key", "paint", "three point", "half court", "hardwood"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, pick(S, 0, 2))),
        detail(rect(8.5, 2.5, 7, 6.5)),
        detail(arc(12, 9, 3.5, 0, 180)),
        detail(arc(12, 1.5, 14, 52, 128)),
    ]


@icon("netball-post", CAT, "Tall netball post with a ring and net and a ball beside it",
      tags=["netball", "post", "ring", "net", "goal", "court", "ball"])
def _(S):
    return [
        line(seg(7, 3, 7, 21.5)),
        line(seg(7, 6, 18, 6)),
        line(poly([(9.5, 6.5), (11.2, 12.5), (15.5, 12.5), (17.5, 6.5)], r=pick(S, 0, 1))),
        ball(16, 19, 2.5),
    ]


@icon("korfball-basket", CAT, "Korfball post topped by an open cylindrical basket",
      tags=["korfball", "basket", "post", "wicker", "goal", "netball", "mixed sport"])
def _(S):
    return [
        shell(rect(6.5, 2.5, 11, 9.5, pick(S, 0, 2))),
        detail(seg(10, 4, 10, 11)), detail(seg(14, 4, 14, 11)),
        line(seg(12, 12, 12, 21.5)),
        line(seg(8, 21.5, 16, 21.5)),
    ]


@icon("volleyball-net", CAT, "Volleyball net with a mesh between tall poles and side antennas",
      tags=["volleyball", "net", "poles", "antenna", "beach volleyball", "court", "mesh"])
def _(S):
    return [
        line(seg(3, 2.5, 3, 21.5)), line(seg(21, 2.5, 21, 21.5)),
        line(seg(6.5, 2.5, 6.5, 8.5)), line(seg(17.5, 2.5, 17.5, 8.5)),
        shell(rect(3, 8, 18, 8)),
        detail(seg(8.5, 8.5, 8.5, 15.5)), detail(seg(12, 8.5, 12, 15.5)), detail(seg(15.5, 8.5, 15.5, 15.5)),
    ]


# ============================================================================ other ball sports and soccer kit

def ell_poly(cx, cy, rx, ry, deg=0, n=14):
    pts = []
    a = math.radians(deg)
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    return poly(pts, closed=True)


@icon("sepak-takraw-ball", CAT, "Woven rattan ball made of interlocking bands",
      tags=["sepak takraw", "rattan", "woven", "ball", "kick volleyball", "takraw", "weave"])
def _(S):
    parts = [shell(pick(S, poly([(12 + 9 * math.cos(math.radians(a + 15)), 12 + 9 * math.sin(math.radians(a + 15))) for a in range(0, 360, 30)], closed=True), circle(12, 12, 9)))]
    for deg in (0, 60, 120):
        parts.append(detail(pick(S, ell_poly(12, 12, 8.5, 3.6, deg), ellipse_rot(deg))))
    return parts


def ellipse_rot(deg):
    return rot(ellipse(12, 12, 8.5, 3.6), deg)


@icon("jai-alai-cesta", CAT, "Long curved wicker scoop basket worn on the hand",
      tags=["jai alai", "cesta", "pelota", "basket", "scoop", "wicker", "basque"])
def _(S):
    return [
        shell(pick(S, "M3 21.5L4 14L8.5 8L15 4.5L21.5 3L17.5 8.5L14.5 14L12 21.5Z",
                   "M3 21.5C3 13 9 5.5 21.5 3C16 6 14 14 12 21.5Z")),
        detail(pick(S, "M6.5 19L8 14L11 10.5", "M6.7 19C7.5 15 9 12 11.5 10")),
    ]


@icon("snooker-rest", CAT, "Long rest stick with an X-shaped head and a ball",
      tags=["snooker", "pool", "billiards", "rest", "cue rest", "cross", "bridge"])
def _(S):
    return [
        line(seg(7, 3, 17, 13)), line(seg(17, 3, 7, 13)),
        line(seg(12, 8, 12, 21.5)),
        ball(19, 19, 1.8),
    ]


@icon("pool-pocket", CAT, "Table corner with a pocket and a ball about to drop in",
      tags=["pool", "billiards", "snooker", "pocket", "table", "corner", "pot"])
def _(S):
    return [
        line(poly([(21.5, 2.5), (2.5, 2.5), (2.5, 21.5)], r=pick(S, 0, 1.5))),
        dot(6.3, 6.3, 3.6),
        shell(circle(15, 15, 2.5)),
        line(seg(11.2, 11.2, 10.2, 10.2)),
    ]


@icon("soccer-cleats", CAT, "Low football boot seen from the side with laces and studs",
      tags=["soccer", "football", "boot", "cleats", "studs", "shoe", "footwear"])
def _(S):
    return [
        shell(poly([(3, 5.5), (9, 5.5), (10, 9.5), (15, 11.5), (21, 14.5), (21, 18), (3, 18)], closed=True, r=pick(S, 0, 1.5))),
        detail(seg(10.5, 12.5, 12.5, 14.5)), detail(seg(14, 11.5, 15.5, 14)),
        dot(6, 20.5, 1.3), dot(12, 20.5, 1.3), dot(18, 20.5, 1.3),
    ]


@icon("soccer-shin-guard", CAT, "Curved shin pad with two straps",
      tags=["shin guard", "shin pad", "soccer", "football", "protection", "leg", "hockey"])
def _(S):
    return [
        shell(pick(S, "M8 2.5H16L17 9L16 21.5H8.5L7 9Z", "M8 2.5H16C17.3 8 17.3 15 15.5 21.5H8.5C6.7 15 6.7 8 8 2.5Z")),
        detail(seg(8, 9, 16, 9)), detail(seg(8, 16, 16, 16)),
        line(seg(3, 9, 6.5, 9)), line(seg(17.5, 9, 21, 9)),
        line(seg(3, 16, 6.5, 16)), line(seg(17.5, 16, 21, 16)),
    ]


@icon("goalkeeper-gloves", CAT, "Padded goalkeeper glove with finger slits, a thumb and a wrist strap",
      tags=["goalkeeper", "gloves", "glove", "keeper", "soccer", "football", "save"])
def _(S):
    return [
        shell(poly([(5, 17.5), (5, 4.5), (19, 4.5), (19, 10), (21.5, 12.5), (19, 15), (19, 17.5)], closed=True, r=pick(S, 0, 2))),
        detail(seg(8.5, 4.5, 8.5, 10.5)), detail(seg(12, 4.5, 12, 10.5)), detail(seg(15.5, 4.5, 15.5, 10.5)),
        line(seg(5, 21, 19, 21)),
    ]


@icon("corner-flag", CAT, "Corner flag on a pole with the quarter circle marking at its base",
      tags=["corner flag", "corner kick", "soccer", "football", "pitch", "marker", "flag"])
def _(S):
    return [
        line(seg(4, 2.5, 4, 21.5)),
        shell(poly([(4, 3.5), (15, 6.5), (4, 9.5)], closed=True, r=pick(S, 0, 1))),
        line(arc(4, 21.5, 10, -60, 0)),
    ]


@icon("soccer-field", CAT, "Football pitch from above with halfway line, centre circle and penalty boxes",
      tags=["soccer", "football", "pitch", "field", "penalty box", "halfway", "centre circle"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 15, pick(S, 0, 2))),
        detail(seg(12, 5, 12, 19)),
        detail(circle(12, 12, 2.4)),
        detail(rect(2.5, 7, 5, 10)), detail(rect(17, 7, 5, 10)),
    ]


@icon("penalty-card", CAT, "Raised fist holding up a referee's card",
      tags=["referee", "card", "yellow card", "red card", "foul", "penalty", "booking"])
def _(S):
    return [
        shell(rot(rect(8, 2.5, 8, 10, pick(S, 0, 1.5)), 10, 12, 7.5)),
        dot(12, 16.7, 2.8),
        line(seg(12, 19, 12, 21.5)),
    ]


@icon("captain-armband", CAT, "Armband around an upper arm marked with the letter C",
      tags=["captain", "armband", "leader", "team", "soccer", "football", "arm"])
def _(S):
    return [
        line(seg(7, 2.5, 7, 6)), line(seg(17, 2.5, 17, 6)),
        line(seg(7, 18, 7, 21.5)), line(seg(17, 18, 17, 21.5)),
        shell(rect(3.5, 6.5, 17, 11, pick(S, 0, 2))),
        detail(arc(12, 12, 2.2, 40, 320)),
    ]


@icon("linesman-flag", CAT, "Assistant referee's checked flag on a short handle",
      tags=["linesman", "assistant referee", "offside", "flag", "touchline", "soccer", "checkered"])
def _(S):
    return [
        shell(rect(10, 2.5, 11.5, 11.5, pick(S, 0, 1.5))),
        sq(11, 3.5, 4.75, 4.75), sq(15.75, 8.25, 4.75, 4.75),
        line(seg(3, 21.5, 10.5, 14)),
    ]


@icon("substitution-board", CAT, "Handheld board showing an arrow up and an arrow down",
      tags=["substitution", "sub", "board", "change", "swap", "soccer", "fourth official"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 15, pick(S, 0, 2))),
        detail(seg(8, 13.5, 8, 6)), detail(poly([(6, 8), (8, 6), (10, 8)])),
        detail(seg(16, 6, 16, 13.5)), detail(poly([(14, 11.5), (16, 13.5), (18, 11.5)])),
        line(seg(12, 17.5, 12, 21.5)),
    ]


@icon("ball-pump", CAT, "Hand pump with a hose and needle feeding a ball",
      tags=["pump", "ball pump", "inflate", "air", "needle", "hose", "inflator"])
def _(S):
    return [
        line(seg(3.5, 3.5, 10.5, 3.5)), line(seg(7, 3.5, 7, 9)),
        shell(rect(4, 9, 6, 12.5, pick(S, 0, 2))),
        line(poly([(10, 17), (12, 17), (14.6, 13.5)], r=pick(S, 0, 1))),
        shell(circle(18, 12.5, 3.5)),
    ]


@icon("marker-cones", CAT, "Two low flat training marker cones side by side",
      tags=["marker cones", "disc cones", "training", "drill", "agility", "coach", "football"])
def _(S):
    return [
        shell(poly([(2.5, 19), (4, 12.5), (8.5, 12.5), (10, 19)], closed=True, r=pick(S, 0, 1.2))),
        shell(poly([(14, 19), (15.5, 12.5), (20, 12.5), (21.5, 19)], closed=True, r=pick(S, 0, 1.2))),
    ]


@icon("training-cone", CAT, "Tall traffic-style training cone with a square base and a stripe",
      tags=["cone", "training cone", "agility", "drill", "coach", "marker", "football"])
def _(S):
    return [
        shell(poly([(9.5, 2.5), (14.5, 2.5), (17.5, 16.5), (21, 16.5), (21, 21.5), (3, 21.5), (3, 16.5), (6.5, 16.5)], closed=True, r=pick(S, 0, 1))),
        detail(seg(8.2, 10.5, 15.8, 10.5)),
    ]


@icon("tactics-board", CAT, "Clipboard with crosses, circles and an arrow for planning plays",
      tags=["tactics", "playbook", "coach", "strategy", "clipboard", "formation", "plan"])
def _(S):
    return [
        shell(rect(4, 4.5, 16, 17, pick(S, 0, 2))),
        shell(rect(8.5, 2.5, 7, 3.5, pick(S, 0, 1))),
        detail(seg(7.5, 8.5, 10.5, 11.5)), detail(seg(10.5, 8.5, 7.5, 11.5)),
        detail(circle(16, 10, 1.4)),
        detail(seg(8, 17, 16, 17)), detail(poly([(14, 15), (16, 17), (14, 19)])),
    ]


# ============================================================================ players and scenes

def fl(S, *pts):
    """Limb or body polyline (Line: sharp joints, Rounded: filleted joints)."""
    return line(poly(list(pts), r=S.r))


def oval(cx, cy, deg=0.0, rx=2.7, ry=1.6):
    """Small solid oval (football or rugby ball), tilted by deg."""
    return solid(rot(ellipse(cx, cy, rx, ry), deg, cx, cy))


@icon("lawn-bowling", CAT, "Bowler crouched on one knee rolling a bowl",
      tags=["lawn bowls", "bowling", "bowls", "green", "crown green", "bowler", "jack"])
def _(S):
    return [
        head(7, 4.5),
        fl(S, (7.5, 7.5), (9.5, 13.5)),
        fl(S, (8, 9), (13, 12.5), (16, 16.5)),
        fl(S, (9.5, 13.5), (14, 13.5), (14, 20)),
        fl(S, (9.5, 13.5), (6, 19), (2.5, 19)),
        ball(20, 18.5, 2),
    ]


@icon("handball", CAT, "Player leaping with a raised arm about to throw a ball",
      tags=["handball", "team handball", "throw", "jump shot", "goal", "indoor", "player"])
def _(S):
    return [
        head(9, 6),
        fl(S, (9.5, 9.5), (10.5, 15)),
        fl(S, (9.5, 10.5), (13.5, 8), (16.5, 5)),
        fl(S, (9.5, 10.5), (6, 12.5)),
        fl(S, (10.5, 15), (15, 16.5), (15, 21)),
        fl(S, (10.5, 15), (7.5, 19), (4.5, 18.5)),
        ball(20, 3.8, 1.9),
    ]


@icon("water-polo", CAT, "Swimmer in the water raising an arm to throw a ball",
      tags=["water polo", "pool", "swim", "throw", "goal", "aquatic", "ball"])
def _(S):
    wave = [(2.5, 17), (5, 15.5), (8, 17), (11, 15.5), (14, 17), (17, 15.5), (19.5, 17), (21.5, 16)]
    wave2 = [(2.5, 21), (5, 19.5), (8, 21), (11, 19.5), (14, 21), (17, 19.5), (19.5, 21), (21.5, 20)]
    return [
        head(10, 6.5),
        fl(S, (10, 10), (10, 14)),
        fl(S, (10, 10.5), (14.5, 8), (17.5, 4.5)),
        fl(S, (10, 10.5), (6.5, 12)),
        ball(20.3, 3.2, 1.8),
        line(poly(wave, r=pick(S, 0, 2))),
        line(poly(wave2[:-1], r=pick(S, 0, 2))),
    ]


@icon("water-polo-cap", CAT, "Cloth cap with round ear guards and a chin strap",
      tags=["water polo", "cap", "swim cap", "ear guards", "headgear", "pool", "helmet"])
def _(S):
    return [
        shell(pick(S, "M5.5 15A6.5 6.5 0 0 1 18.5 15Z",
                   "M5.5 14.5A6.5 6.5 0 0 1 18.5 14.5V15.2Q18.5 16 17.7 16H6.3Q5.5 16 5.5 15.2Z")),
        dot(4.6, 15.2, 2.3), dot(19.4, 15.2, 2.3),
        line(poly([(5, 18), (8, 21), (16, 21), (19, 18)], r=pick(S, 0, 2))),
    ]


@icon("penalty-kick", CAT, "Ball on the spot below a goal frame with a crouching keeper",
      tags=["penalty", "penalty kick", "spot kick", "goalkeeper", "shootout", "soccer", "goal"])
def _(S):
    return [
        line(poly([(3, 13.5), (3, 3), (21, 3), (21, 13.5)], r=pick(S, 0, 1.5))),
        head(12, 7, 2),
        fl(S, (7.5, 12.5), (9.5, 10), (14.5, 10), (16.5, 12.5)),
        ball(12, 19.5, 2),
    ]


@icon("bicycle-kick", CAT, "Player upside down in the air kicking a ball over the head",
      tags=["bicycle kick", "overhead kick", "scissor kick", "acrobatic", "soccer", "football", "volley"])
def _(S):
    return [
        head(6.8, 17),
        fl(S, (9.5, 14.5), (14, 10)),
        fl(S, (14, 10), (18, 6.5)),
        fl(S, (14, 10), (10.5, 6.5), (9.5, 3.5)),
        fl(S, (9.5, 14.5), (13, 17.5), (16.5, 18.5)),
        ball(20.5, 3.5, 1.8),
    ]


@icon("soccer-header", CAT, "Player jumping to head a ball",
      tags=["header", "heading", "soccer", "football", "jump", "aerial", "headed goal"])
def _(S):
    return [
        head(10, 8),
        fl(S, (10.5, 11.5), (10, 16.5)),
        fl(S, (10.5, 12.5), (6.5, 11), (4, 13)),
        fl(S, (10.5, 12.5), (14.5, 14.5)),
        fl(S, (10, 16.5), (13.5, 19), (12.5, 21.5)),
        fl(S, (10, 16.5), (6.5, 19), (5.5, 21.5)),
        ball(16.8, 4.8, 2.2),
    ]


@icon("soccer-player", CAT, "Running player swinging a leg forward to kick a ball",
      tags=["soccer", "football", "player", "kick", "striker", "footballer", "shot"], aliases=["footballer"])
def _(S):
    return [
        head(9, 4.5),
        fl(S, (9.5, 8), (9, 14)),
        fl(S, (9.5, 9), (6, 10.5), (4, 13.5)),
        fl(S, (9.5, 9), (13, 10.5), (15, 8.5)),
        fl(S, (9, 14), (8.5, 18.5), (10, 21.5)),
        fl(S, (9, 14), (13.5, 16), (17, 13.5)),
        ball(20.5, 11.5, 2),
    ]


@icon("goalkeeper-save", CAT, "Goalkeeper diving sideways with arms stretched toward a ball",
      tags=["goalkeeper", "save", "dive", "keeper", "soccer", "stop", "stretch"])
def _(S):
    return [
        head(9, 9),
        fl(S, (11, 11), (16.5, 16.5)),
        fl(S, (10.5, 10), (7, 6.5), (6, 5.5)),
        fl(S, (11.5, 12.5), (8, 14)),
        fl(S, (16.5, 16.5), (21, 18.5)),
        fl(S, (16.5, 16.5), (18.5, 21.5)),
        ball(3.8, 3.8, 1.8),
    ]


@icon("throw-in", CAT, "Player holding a ball overhead with both hands for a throw-in",
      tags=["throw in", "touchline", "soccer", "football", "restart", "overhead", "ball"])
def _(S):
    return [
        ball(12, 3, 1.9),
        head(12, 10),
        fl(S, (12, 13), (7.5, 10.5), (9.5, 5.8)),
        fl(S, (12, 13), (16.5, 10.5), (14.5, 5.8)),
        fl(S, (12, 13), (12, 17)),
        fl(S, (12, 17), (8, 19.5), (8, 21.5)),
        fl(S, (12, 17), (16.5, 19), (19.5, 21)),
    ]


@icon("goal-celebration", CAT, "Player sliding on the knees with both arms spread wide",
      tags=["celebration", "goal", "knee slide", "joy", "victory", "soccer", "scorer"])
def _(S):
    return [
        head(12, 5),
        fl(S, (3, 5), (12, 9.5), (21, 5)),
        fl(S, (12, 9.5), (12.5, 14.5)),
        fl(S, (7, 21), (14, 19.5), (12.5, 14.5)),
    ]


@icon("free-kick-wall", CAT, "Row of three defenders standing shoulder to shoulder with a ball ahead",
      tags=["free kick", "wall", "defenders", "set piece", "soccer", "football", "line up"])
def _(S):
    parts = []
    for x in (4.8, 12, 19.2):
        parts += [head(x, 5, 2), fl(S, (x, 8), (x, 13.5)), fl(S, (x - 1.6, 18.5), (x, 13.5), (x + 1.6, 18.5))]
    parts.append(ball(12, 21.2, 1.3))
    return parts


# ============================================================================ american football and rugby

@icon("football-goalpost", CAT, "Y-shaped goalpost with a crossbar and two tall uprights",
      tags=["goalpost", "field goal", "uprights", "american football", "crossbar", "kick", "nfl"])
def _(S):
    return [
        line(poly([(5, 2.5), (5, 11.5), (19, 11.5), (19, 2.5)], r=pick(S, 0, 1.5))),
        line(seg(12, 11.5, 12, 21.5)),
    ]


@icon("football-field", CAT, "Long gridiron field from above with yard lines and end zones",
      tags=["american football", "gridiron", "field", "yard line", "end zone", "stadium", "pitch"])
def _(S):
    return [
        shell(rect(2.5, 5, 19, 14, pick(S, 0, 2))),
        detail(seg(7, 5, 7, 19)), detail(seg(12, 5, 12, 19)), detail(seg(17, 5, 17, 19)),
        detail(seg(9.5, 11, 9.5, 13)), detail(seg(14.5, 11, 14.5, 13)),
    ]


@icon("kicking-tee", CAT, "Football standing upright on a kicking tee",
      tags=["kicking tee", "tee", "kickoff", "football", "american football", "rugby", "placekick"])
def _(S):
    return [
        shell(pick(S, "M12 2.5L16 9L12 16.5L8 9Z", "M12 2.5C15.5 5.5 16.5 10.5 12 16.5C7.5 10.5 8.5 5.5 12 2.5Z")),
        detail(seg(12, 6.5, 12, 11.5)),
        shell(poly([(9, 17.5), (15, 17.5), (13.5, 21.5), (10.5, 21.5)], closed=True, r=pick(S, 0, 1))),
    ]


@icon("shoulder-pads", CAT, "Front view of padded shoulder gear with round caps and a neck opening",
      tags=["shoulder pads", "armor", "protection", "american football", "gear", "padding", "harness"])
def _(S):
    return [
        shell(pick(S, "M2.5 15.5V12L5 7L9.5 5.5H14.5L19 7L21.5 12V15.5H15.5V13H8.5V15.5Z",
                   "M2.5 15.5V13C2.5 8.5 6 5.5 10 5.5H14C18 5.5 21.5 8.5 21.5 13V15.5H15.5V13H8.5V15.5Z")),
    ]


@icon("football-player", CAT, "Helmeted player cocking an arm back to throw a football",
      tags=["quarterback", "american football", "throw", "pass", "helmet", "gridiron", "player"])
def _(S):
    return [
        head(11, 5, 2.6),
        line(seg(13.4, 4.5, 14.4, 6)),
        fl(S, (10.5, 9), (10, 14.5)),
        fl(S, (10.5, 10), (6.5, 9.5), (5, 6)),
        fl(S, (10.5, 10), (14.5, 12), (16.5, 9.5)),
        fl(S, (10, 14.5), (13.5, 18), (15.5, 21.5)),
        fl(S, (10, 14.5), (7, 18.5), (4.5, 21)),
        oval(4.3, 3.2, -35),
    ]


@icon("touchdown", CAT, "Player with both arms raised high holding a football",
      tags=["touchdown", "score", "celebration", "american football", "end zone", "spike", "victory"])
def _(S):
    return [
        oval(12, 3.3, 0, 3, 1.7),
        head(12, 9, 2.25),
        fl(S, (12, 12.5), (7.5, 8), (9, 4.8)),
        fl(S, (12, 12.5), (16.5, 8), (15, 4.8)),
        fl(S, (12, 12.5), (12, 17)),
        fl(S, (7.5, 21.5), (12, 17), (16.5, 21.5)),
    ]


@icon("football-tackle", CAT, "Player diving low to wrap the legs of a running ball carrier",
      tags=["tackle", "american football", "block", "carrier", "dive", "defence", "gridiron"])
def _(S):
    return [
        head(17, 4.5),
        fl(S, (17, 8), (15.5, 13)),
        fl(S, (16.5, 9), (20, 10.5), (21, 8)),
        fl(S, (15.5, 13), (18.5, 17), (21, 18.5)),
        fl(S, (15.5, 13), (12.5, 16)),
        head(4, 14.5),
        fl(S, (6.2, 16.5), (12, 19)),
        fl(S, (7, 15), (11.5, 13.5), (13.5, 16)),
        fl(S, (12, 19), (17, 21)),
    ]


@icon("rugby-posts", CAT, "H-shaped rugby goal posts with two uprights and a crossbar",
      tags=["rugby", "posts", "goal posts", "uprights", "conversion", "kick", "union"])
def _(S):
    return [
        line(seg(6, 2.5, 6, 21.5)), line(seg(18, 2.5, 18, 21.5)),
        line(seg(6, 10, 18, 10)),
    ]


@icon("rugby-scrum", CAT, "Two packs bent over head to head with a ball between them",
      tags=["scrum", "rugby", "pack", "forwards", "set piece", "scrummage", "contest"])
def _(S):
    return [
        head(9.6, 13.5, 2.1), head(14.4, 13.5, 2.1),
        fl(S, (3.5, 17), (8, 10.5)), fl(S, (20.5, 17), (16, 10.5)),
        line(seg(3.5, 17, 3.5, 21.5)), line(seg(20.5, 17, 20.5, 21.5)),
        ball(12, 20, 1.4),
    ]


@icon("rugby-player", CAT, "Running player carrying a ball tucked under one arm",
      tags=["rugby", "player", "run", "carry", "ball carrier", "try line", "sprint"])
def _(S):
    return [
        head(11, 4.5),
        fl(S, (11, 8), (10, 14)),
        fl(S, (11, 9), (14.5, 11)),
        fl(S, (11, 9), (7, 10.5), (5, 8)),
        fl(S, (10, 14), (14, 17), (14.5, 21.5)),
        fl(S, (10, 14), (7, 18), (4, 19.5)),
        oval(16.5, 13, 40),
    ]


@icon("rugby-lineout", CAT, "Jumper lifted high by two teammates to catch the ball",
      tags=["lineout", "rugby", "lift", "jump", "throw in", "catch", "set piece"])
def _(S):
    return [
        oval(12, 3, 0, 2.8, 1.6),
        head(12, 8.2),
        fl(S, (12, 11), (8, 8.5), (9, 4.8)),
        fl(S, (12, 11), (16, 8.5), (15, 4.8)),
        fl(S, (12, 11), (12, 15)),
        head(5.5, 15.2, 2),
        head(18.5, 15.2, 2),
        fl(S, (5.5, 18), (5.5, 21.5)), fl(S, (18.5, 18), (18.5, 21.5)),
        fl(S, (5.5, 18.5), (9.5, 17), (12, 15)), fl(S, (18.5, 18.5), (14.5, 17), (12, 15)),
    ]


@icon("rugby-try", CAT, "Player diving to press the ball down on the try line",
      tags=["try", "rugby", "score", "grounding", "dive", "try line", "touch down"])
def _(S):
    return [
        head(15.5, 11),
        fl(S, (3, 9.5), (8, 12.5), (13, 13.5)),
        fl(S, (13, 13.5), (17, 16.5)),
        oval(20, 17.8, 0, 2.2, 1.5),
        line(seg(2.5, 21.2, 21.5, 21.2)),
    ]


@icon("scrum-cap", CAT, "Soft padded headguard with panels and a chin strap",
      tags=["scrum cap", "headguard", "rugby", "head protection", "padded", "chin strap", "gear"])
def _(S):
    return [
        shell(pick(S, "M4.5 15A7.5 7.5 0 0 1 19.5 15V16.5H4.5Z",
                   "M4.5 14.5A7.5 7.5 0 0 1 19.5 14.5V15.5Q19.5 16.5 18.5 16.5H5.5Q4.5 16.5 4.5 15.5Z")),
        detail(seg(12, 7.5, 12, 15)),
        detail(poly([(6.5, 15), (7.5, 10.5)])), detail(poly([(17.5, 15), (16.5, 10.5)])),
        line(poly([(5.5, 18.5), (8, 21.5), (16, 21.5), (18.5, 18.5)], r=pick(S, 0, 2))),
    ]


# ============================================================================ baseball and racket players

@icon("baseball-batter", CAT, "Batter in a stance with the bat held back over the shoulder",
      tags=["batter", "baseball", "bat", "swing", "stance", "hitter", "softball"])
def _(S):
    return [
        head(8.5, 6),
        fl(S, (9, 9.5), (9.5, 15)),
        fl(S, (9, 10.5), (13, 9.5)),
        solid(poly([(13.49, 10.0), (20.54, 4.28), (18.46, 2.12), (12.51, 9.0)], closed=True)),
        fl(S, (9.5, 15), (13.5, 18), (14, 21.5)),
        fl(S, (9.5, 15), (6.5, 18.5), (4.5, 21.5)),
    ]


@icon("baseball-pitcher", CAT, "Pitcher mid-windup with one knee raised about to throw",
      tags=["pitcher", "baseball", "windup", "throw", "mound", "softball", "pitch"])
def _(S):
    return [
        head(10, 5.5),
        fl(S, (10.5, 9), (10, 15)),
        fl(S, (10.5, 10), (6, 9), (3.5, 12)),
        fl(S, (10.5, 10), (14, 7.5), (17, 5)),
        fl(S, (10, 15), (15, 14.5), (14.5, 19)),
        fl(S, (10, 15), (9, 21.5)),
        ball(19.8, 3.5, 1.8),
    ]


@icon("home-run", CAT, "Ball flying in a high arc over an outfield fence",
      tags=["home run", "homer", "baseball", "fence", "outfield", "slugger", "over the wall"])
def _(S):
    return [
        line("M3.5 14Q8 2.5 16 4.5"),
        ball(19.6, 7.5, 1.9),
        line(seg(2.5, 17.5, 21.5, 17.5)),
        line(seg(6, 17.5, 6, 21.5)), line(seg(12, 17.5, 12, 21.5)), line(seg(18, 17.5, 18, 21.5)),
    ]


@icon("baseball-slide", CAT, "Runner sliding feet first into a base with dust behind",
      tags=["slide", "baseball", "steal", "base", "runner", "safe", "softball"])
def _(S):
    return [
        head(7.5, 8.5),
        fl(S, (8, 11.5), (12, 16)),
        fl(S, (8.5, 12.5), (5.5, 15.5)),
        fl(S, (9, 12), (13, 10.5)),
        fl(S, (12, 16), (16, 16.5), (18, 19)),
        sq(17.5, 19.5, 4.5, 2.5),
        dot(3.2, 19.5, 1.3), dot(6.2, 21, 1.1), dot(2.8, 16.8, 1),
    ]


@icon("batting-cage", CAT, "Netted batting tunnel with a bat and a ball inside",
      tags=["batting cage", "practice", "baseball", "net", "tunnel", "softball", "training"])
def _(S):
    return [
        line(pick(S, "M3 21.5V10L7 4.5H17L21 10V21.5", "M3 21.5V10C3 6.5 6.5 4 12 4C17.5 4 21 6.5 21 10V21.5")),
        detail(seg(12, 6, 12, 21.5)),
        line(seg(7, 20, 12, 12)),
        ball(16.5, 15.5, 1.8),
    ]


@icon("tennis-player", CAT, "Player reaching up with a racket to serve a ball overhead",
      tags=["tennis", "serve", "player", "racket", "overhead", "smash", "court"])
def _(S):
    return [
        head(10, 8),
        fl(S, (10, 11), (10, 16.5)),
        fl(S, (10, 11.5), (14, 7), (16.5, 5)),
        shell(rot(ellipse(18.4, 3.6, 1.8, 2.7), 45, 18.4, 3.6)),
        fl(S, (10, 11.5), (6.5, 9), (6, 7)),
        ball(5.2, 3.5, 1.5),
        fl(S, (10, 16.5), (13, 21.5)), fl(S, (10, 16.5), (7, 21.5)),
    ]


@icon("badminton-player", CAT, "Player leaping to smash a shuttlecock with a racket",
      tags=["badminton", "smash", "jump", "player", "racket", "shuttlecock", "court"])
def _(S):
    return [
        head(10, 6.5),
        fl(S, (10, 9.5), (10, 14)),
        fl(S, (10, 10.5), (14.5, 6.5), (16.5, 4.5)),
        shell(rot(ellipse(18.6, 3.2, 1.7, 2.5), 45, 18.6, 3.2)),
        fl(S, (10, 10.5), (6.5, 12.5)),
        fl(S, (10, 14), (14, 16.5), (13, 20.5)),
        fl(S, (10, 14), (6, 17), (7, 21)),
        ball(5, 3.5, 1.4),
    ]


@icon("table-tennis-player", CAT, "Player behind a small table swinging a paddle at a ball",
      tags=["table tennis", "ping pong", "player", "paddle", "rally", "table", "indoor"])
def _(S):
    return [
        head(8, 5),
        fl(S, (8, 8.5), (8, 13)),
        fl(S, (8, 9.5), (13, 10.5), (15, 8.5)),
        shell(circle(17.8, 7, 2)),
        ball(21, 12.5, 1.3),
        line(seg(2.5, 16.5, 21.5, 16.5)),
        line(seg(12, 13.2, 12, 16.5)),
        line(seg(5, 16.5, 5, 21.5)), line(seg(19, 16.5, 19, 21.5)),
    ]
