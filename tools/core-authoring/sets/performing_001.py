"""TypeIcon Core: performing arts (batch 001): folk dance, circus acts, magic and illusions, clowning and stagecraft.

People are stick figures in the style of the people and activities sets: a solid head (r 2.25) over 2 px limbs
(faceted in Line, filleted in Rounded). Props are shells so Filled turns them solid while limbs get heavier.
"""
import math

from dsl import LINE, D, P, ST, U, Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "performing"
HR = 2.25


def pick(S, a, b):
    return a if S.name == "line" else b


def limb(S, *pts):
    return line(poly(list(pts), r=S.r))


def u(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


def flame(cx, cy, deg, ln=4.5, w=3.0):
    """Teardrop flame with its base centre at (cx, cy) and its tip `ln` away in direction deg (0 = right, 90 = down)."""
    a = math.radians(deg)
    dx, dy = math.cos(a), math.sin(a)
    nx, ny = -dy, dx
    tip = (cx + dx * ln, cy + dy * ln)
    b1 = (cx + nx * w / 2, cy + ny * w / 2)
    b2 = (cx - nx * w / 2, cy - ny * w / 2)
    c1 = (cx + dx * ln * 0.2 + nx * w * 0.8, cy + dy * ln * 0.2 + ny * w * 0.8)
    c2 = (cx + dx * ln * 0.2 - nx * w * 0.8, cy + dy * ln * 0.2 - ny * w * 0.8)
    m1 = (cx + dx * ln * 0.78 + nx * w * 0.3, cy + dy * ln * 0.78 + ny * w * 0.3)
    m2 = (cx + dx * ln * 0.78 - nx * w * 0.3, cy + dy * ln * 0.78 - ny * w * 0.3)
    f = lambda p: f"{fmt(p[0])} {fmt(p[1])}"
    back = (cx - dx * w * 0.55, cy - dy * w * 0.55)
    return f"M{f(b1)}C{f(c1)} {f(m1)} {f(tip)}C{f(m2)} {f(c2)} {f(b2)}Q{f(back)} {f(b1)}Z"


# --------------------------------------------------------------------------- folk and stage dance

@icon("robot-dance", CAT, "Dancer with a square head, arms bent at sharp right angles and stiff straight legs",
      tags=["robot", "dance", "popping", "mechanical", "street dance", "stiff"], aliases=["robot-dancer"])
def _(S):
    return [
        sq(9.75, 1.75, 4.5, 4.5, pick(S, 0, 1)),
        limb(S, (12, 8), (12, 15)),
        limb(S, (12, 9.5), (7.5, 9.5), (7.5, 5)),
        limb(S, (12, 9.5), (16.5, 9.5), (16.5, 14)),
        limb(S, (12, 15), (9, 21.5)),
        limb(S, (12, 15), (15, 21.5)),
        line(seg(2.5, 9.5, 4.5, 9.5)), line(seg(19.5, 9.5, 21.5, 9.5)),
    ]


@icon("highland-fling", CAT, "Dancer in a pleated kilt balanced on one foot with both arms curved overhead",
      tags=["highland dance", "scottish", "kilt", "dance", "folk dance", "scotland"], aliases=["highland-dancer"])
def _(S):
    kilt = poly([(9, 11.5), (15, 11.5), (16.5, 16.5), (7.5, 16.5)], closed=True, r=pick(S, 0, 1))
    return [
        dot(12, 4, HR),
        limb(S, (12, 6.5), (12, 11.5)),
        limb(S, (12, 8), (7.5, 6.5), (6, 2)),
        limb(S, (12, 8), (16.5, 6.5), (18, 2)),
        shell(kilt),
        limb(S, (10, 16.5), (10, 21.5)),
        limb(S, (14, 16.5), (16.5, 18.5), (13, 19)),
    ]


@icon("vogue-dance", CAT, "Dancer framing the face with both hands in angular poses and one hip pushed out",
      tags=["vogue", "dance", "pose", "ballroom", "runway", "street dance"], aliases=["voguing"])
def _(S):
    return [
        dot(11, 5, HR),
        limb(S, (11, 8.5), (12.5, 14)),
        limb(S, (11.5, 9.5), (5.5, 10), (6.5, 4.5)),
        limb(S, (11.5, 9.5), (17.5, 10), (16, 4.5)),
        limb(S, (12.5, 14), (9, 17.5), (8, 21.5)),
        limb(S, (12.5, 14), (16, 21.5)),
    ]


@icon("twist-dance", CAT, "Dancer with bent knees turned to one side and arms swinging the other way, with curved twist lines",
      tags=["twist", "dance", "swing", "rock and roll", "retro", "sixties"], aliases=["the-twist"])
def _(S):
    return [
        dot(11, 4.5, HR),
        limb(S, (11, 8), (12, 14)),
        limb(S, (11.5, 9.5), (6.5, 10), (3.5, 6.5)),
        limb(S, (12, 14), (16, 17.5), (13.5, 21.5)),
        limb(S, (12, 14), (18.5, 14.5), (21, 19)),
        line(arc(10, 15.5, 7, 150, 210)),
    ]


@icon("pole-dance", CAT, "Dancer holding a vertical pole with one hand and hooking one knee around it while leaning out",
      tags=["pole", "dance", "fitness", "aerial", "spin", "dancer"], aliases=["pole-dancer"])
def _(S):
    return [
        line(seg(18, 2, 18, 22)),
        dot(10.5, 6, HR),
        limb(S, (11, 9.5), (13, 15)),
        limb(S, (11.5, 10.5), (15, 8), (18, 7.5)),
        limb(S, (13, 15), (17.5, 17.5), (15, 20.5)),
        limb(S, (13, 15), (8, 18), (4, 17)),
    ]


@icon("bhangra-dance", CAT, "Dancer in a loose tunic with both arms raised high and one knee lifted",
      tags=["bhangra", "punjabi", "folk dance", "dance", "celebration", "india"], aliases=["bhangra-dancer"])
def _(S):
    tunic = poly([(9.5, 9), (14.5, 9), (15.5, 15), (8.5, 15)], closed=True, r=pick(S, 0, 1))
    return [
        dot(12, 4.8, HR),
        limb(S, (9.5, 9.5), (6.5, 6.5), (6, 2)),
        limb(S, (14.5, 9.5), (17.5, 6.5), (18, 2)),
        shell(tunic),
        limb(S, (10, 15), (10, 21.5)),
        limb(S, (14, 15), (18.5, 16.5), (17.5, 21.5)),
    ]


@icon("samba-dancer", CAT, "Dancer with a wide semicircular fan of feathers behind the whole body and one hip cocked",
      tags=["samba", "carnival", "feathers", "dance", "brazil", "costume"], aliases=["carnival-dancer"])
def _(S):
    rays = []
    for a in range(190, 351, 20):
        x0, y0 = polar(12, 15.5, 8.5, a)
        x1, y1 = polar(12, 15.5, 11, a)
        rays.append(line(seg(x0, y0, x1, y1)))
    return rays + [
        dot(12, 10, HR),
        limb(S, (12, 13), (12.5, 17.5)),
        limb(S, (12.5, 14.5), (8.5, 15), (9.5, 17.5)),
        limb(S, (12.5, 17.5), (10, 22)),
        limb(S, (12.5, 17.5), (15, 22)),
    ]


@icon("folklorico-dance", CAT, "Dancer holding a very wide ruffled skirt out to both sides, with a flower in the hair",
      tags=["folklorico", "skirt", "mexican", "folk dance", "dance", "ballet folklorico"], aliases=["folklorico-dancer"])
def _(S):
    skirt = ("M10.5 11.5H13.5L21.5 19.5A2.4 2.4 0 0 1 16.75 19.5A2.4 2.4 0 0 1 12 19.5A2.4 2.4 0 0 1 7.25 19.5"
             "A2.4 2.4 0 0 1 2.5 19.5Z")
    return [
        dot(12, 4.5, HR),
        dot(15.8, 2.8, 1.1),
        limb(S, (12, 7.5), (12, 11.5)),
        limb(S, (12, 8.5), (7.5, 9), (4.5, 12.5)),
        limb(S, (12, 8.5), (16.5, 9), (19.5, 12.5)),
        shell(skirt),
    ]


@icon("fire-knife-dance", CAT, "Short staff with flames at both ends held in a hand, with curved motion lines either side",
      tags=["fire", "knife dance", "staff", "poi", "samoan", "fire dancing", "spin"], aliases=["fire-dance"])
def _(S):
    return [
        line(seg(8.5, 15.5, 15.5, 8.5)),
        dot(12, 12, 1.5),
        shell(flame(15.5, 8.5, 315, 6, 4.4)),
        shell(flame(8.5, 15.5, 135, 6, 4.4)),
        line(arc(12, 12, 10, 25, 65)),
        line(arc(12, 12, 10, 205, 245)),
    ]


@icon("roller-disco", CAT, "Skater gliding on roller skates with one arm pointing up towards a small disco ball",
      tags=["roller skating", "disco", "rink", "skates", "dance", "retro"], aliases=["roller-skater"])
def _(S):
    return [
        circle_ball(S, 19, 6),
        dot(8, 4.5, HR),
        limb(S, (8.5, 8), (9.5, 14)),
        limb(S, (8.5, 9), (11, 5.5), (12, 2.5)),
        limb(S, (8.5, 9.5), (4.5, 12)),
        limb(S, (9.5, 14), (7, 17.5)),
        limb(S, (9.5, 14), (14, 15.5), (15, 17.5)),
        line(seg(5, 18.5, 9.5, 18.5)), dot(5.5, 20.75, 1), dot(9, 20.75, 1),
        line(seg(12.5, 18.5, 17, 18.5)), dot(13, 20.75, 1), dot(16.5, 20.75, 1),
    ]


def circle_ball(S, cx, cy):
    return shell(circle(cx, cy, 3))


@icon("hopak-dance", CAT, "Dancer in a deep squat with arms folded across the chest kicking one leg straight out",
      tags=["hopak", "cossack", "squat dance", "kick", "folk dance", "ukrainian"], aliases=["cossack-dance"])
def _(S):
    return [
        dot(9.5, 5, HR),
        limb(S, (9.5, 8.5), (8.5, 14.5)),
        limb(S, (5.5, 11), (12.5, 11)),
        limb(S, (8.5, 14.5), (5, 18), (9, 21.5)),
        limb(S, (8.5, 14.5), (15.5, 15), (21.5, 12)),
    ]


@icon("tap-dancer", CAT, "Dancer in a bowler hat holding a short cane out while one heel is kicked up",
      tags=["tap dance", "tap", "cane", "bowler hat", "broadway", "musical"], aliases=["tap-dancing"])
def _(S):
    return [
        solid("M8.2 4.2A2.3 2.3 0 0 1 12.8 4.2Z"),
        line(seg(6.5, 4.5, 14.5, 4.5)),
        dot(10.5, 7.5, 2),
        limb(S, (11, 10.5), (12, 15)),
        limb(S, (11.5, 11.5), (15.5, 13), (19.5, 10.5)),
        limb(S, (12, 15), (12.5, 21.5)),
        limb(S, (12, 15), (8, 18.5), (4.5, 15.5)),
        line(seg(15.5, 19.5, 17, 19.5)), line(seg(15.5, 21.5, 17.5, 21.5)),
    ]


# --------------------------------------------------------------------------- circus acts and props

def rot_pts(pts, deg, c):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


def rot_rect(S, cx, cy, w, h, deg, r=None):
    pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)]
    return poly(rot_pts(pts, deg, (cx, cy)), closed=True, r=pick(S, 0, 1) if r is None else r)


def star_pts(cx, cy, R, r, n=5):
    pts = []
    for i in range(2 * n):
        rad = R if i % 2 == 0 else r
        pts.append(polar(cx, cy, rad, -90 + i * 180 / n))
    return pts


@icon("aerial-silks", CAT, "Performer hanging upside down between two long fabric strips that fall from one rigging point",
      tags=["aerial silks", "aerial fabric", "tissu", "circus", "aerialist", "acrobat", "silk"], aliases=["aerial-tissu"])
def _(S):
    return [
        dot(12, 2.5, 1.2),
        line("M12 3.5C4 6 9 11 5.5 14C3.5 16 5.5 19 4.5 21.5"),
        line("M12 3.5C20 6 15 11 18.5 14C20.5 16 18.5 19 19.5 21.5"),
        limb(S, (9.5, 7.5), (12, 11), (14.5, 7.5)),
        limb(S, (12, 11), (12, 14.2)),
        dot(12, 17, 2),
    ]


@icon("teeterboard", CAT, "Seesaw board on a low fulcrum with one acrobat standing on the raised end and another flying tucked above",
      tags=["teeterboard", "seesaw", "teeter", "circus", "acrobat", "catapult", "flip"], aliases=["russian-swing-board"])
def _(S):
    return [
        line(seg(3, 20, 21, 15)),
        shell(poly([(12, 17.5), (9, 21.5), (15, 21.5)], closed=True, r=pick(S, 0, 0.5))),
        dot(19, 7.5, 1.8),
        limb(S, (19, 10), (19.5, 14)),
        solid(ellipse(8, 6, 2.8, 2.2)),
        dot(11.2, 4.2, 1.5),
    ]


@icon("rola-bola", CAT, "Performer balancing with arms out on a flat board that rests on a rolling cylinder",
      tags=["rola bola", "balance board", "roller board", "circus", "balancing", "juggler"], aliases=["rolla-bolla"])
def _(S):
    return [
        line(seg(3, 15, 21, 15)),
        shell(circle(12, 19, 3.2)),
        dot(12, 3.8, HR),
        limb(S, (12, 7), (12, 11.5)),
        limb(S, (5.5, 8), (12, 8.5), (18.5, 8)),
        limb(S, (10, 14), (12, 11.5), (14, 14)),
    ]


@icon("human-cannonball", CAT, "Wheeled cannon pointing upward with a performer shooting out of the muzzle in a straight line",
      tags=["human cannonball", "cannon", "circus", "stunt", "daredevil", "launch"], aliases=["cannonball-act"])
def _(S):
    return [
        shell(rot_rect(S, 8.5, 13.5, 11, 5.5, -38)),
        shell(circle(7, 19, 3)),
        dot(7, 19, 0.8),
        dot(19.5, 4.3, 2),
        limb(S, (17.8, 6.5), (15.8, 9.2)),
    ]


@icon("fire-juggling", CAT, "Three flaming torches fanning up out of two open cupped hands",
      tags=["fire juggling", "torches", "juggler", "circus", "flames", "fire show"], aliases=["torch-juggling"])
def _(S):
    parts = []
    for ang in (-42, 0, 42):
        a = math.radians(ang)
        d = (math.sin(a), -math.cos(a))
        x0, y0 = 12 + d[0] * 3.5, 16 + d[1] * 3.5
        x1, y1 = 12 + d[0] * 7.5, 16 + d[1] * 7.5
        parts.append(line(seg(x0, y0, x1, y1)))
        parts.append(shell(flame(x1, y1, 270 + ang, 6, 3.2)))
    parts.append(line(arc(6.5, 15.5, 4, 30, 150)))
    parts.append(line(arc(17.5, 15.5, 4, 30, 150)))
    return parts


def shoe(S, x, y):
    heel = poly([(x, y), (x + 5, y), (x + 5.5, y + 3), (x, y + 3)], closed=True, r=0)
    foot = rect(x, y + 3, 11.5, 4.6, pick(S, 1.2, 2.3))
    toe = circle(x + 15.5, y + 4.7, 3.4)
    return u(heel, foot, toe)


@icon("clown-shoes", CAT, "Pair of oversized clown shoes with long soles and big round toes",
      tags=["clown shoes", "big shoes", "clown", "circus", "costume", "funny", "oversized"], aliases=["big-shoes"])
def _(S):
    def sh(x, y):
        return (f"M{x} {y}H{x + 5}V{y + 2}C{x + 7.5} {y + 2} {x + 10} {y + 1} {x + 14} {y + 1}"
                f"A3 3 0 0 1 {x + 14} {y + 7}H{x}Z")
    return [
        shell(sh(3.5, 3), stroke_miterlimit="2"),
        shell(sh(3.5, 14), stroke_miterlimit="2"),
    ]


@icon("squirting-flower", CAT, "Flower pinned to a jacket lapel squirting a thin arc of water drops",
      tags=["squirting flower", "lapel flower", "prank", "clown", "water", "joke", "gag"], aliases=["lapel-flower"])
def _(S):
    petals = u(*[circle(*polar(9.5, 10, 2.9, a), 1.9) for a in range(-90, 270, 72)])
    return [
        line("M3 3V21"),
        line(seg(9, 14.5, 6, 19.5)),
        shell(petals), dot(9.5, 10, 1.1),
        dot(14.3, 7.2, 0.9), dot(17, 5.8, 0.9), dot(19.7, 6.5, 1), dot(21, 9.5, 1.1),
    ]


@icon("circus-pedestal", CAT, "Drum-shaped animal stand with a star on the side and a scalloped top rim",
      tags=["pedestal", "circus", "animal act", "stand", "drum", "lion tamer", "platform"], aliases=["circus-stool"])
def _(S):
    rim = "M4 10V7A1.6 1.6 0 0 1 7.2 7A1.6 1.6 0 0 1 10.4 7A1.6 1.6 0 0 1 13.6 7A1.6 1.6 0 0 1 16.8 7A1.6 1.6 0 0 1 20 7V10Z"
    return [
        shell(rim),
        shell(rect(5.5, 10, 13, 10.5, pick(S, 0.5, 2.5))),
        Part("dot", poly(star_pts(12, 15.4, 3.6, 1.6), closed=True)),
    ]


@icon("circus-wagon", CAT, "Circus cage wagon with vertical bars, a scalloped roof edge and two large wheels",
      tags=["circus wagon", "cage", "carriage", "circus", "menagerie", "caravan", "bars"], aliases=["menagerie-wagon"])
def _(S):
    top = "M3 6.5A1.5 1.5 0 0 1 6 6.5A1.5 1.5 0 0 1 9 6.5A1.5 1.5 0 0 1 12 6.5A1.5 1.5 0 0 1 15 6.5A1.5 1.5 0 0 1 18 6.5A1.5 1.5 0 0 1 21 6.5V15H3Z"
    return [
        shell(top),
        detail(seg(7.5, 8.5, 7.5, 15)), detail(seg(12, 8.5, 12, 15)), detail(seg(16.5, 8.5, 16.5, 15)),
        shell(circle(7.5, 18.5, 3.2)), shell(circle(16.5, 18.5, 3.2)),
        dot(7.5, 18.5, 0.8), dot(16.5, 18.5, 0.8),
    ]


@icon("bed-of-nails", CAT, "Performer lying flat on a board covered with upright spikes",
      tags=["bed of nails", "fakir", "spikes", "sideshow", "stunt", "circus", "nails"], aliases=["fakir-bed"])
def _(S):
    spikes = [solid(poly([(x, 17), (x + 2, 13.8), (x + 4, 17)], closed=True)) for x in (3.5, 8.5, 13.5)]
    return [
        dot(4.5, 8, HR),
        limb(S, (8, 8.8), (20.5, 8.8)),
        *spikes,
        solid(poly([(18.5, 17), (20.5, 13.8), (22, 17)], closed=True)),
        shell(rect(2, 17, 20, 4, pick(S, 0.5, 1.5))),
    ]


@icon("escape-artist", CAT, "Standing figure wrapped in crossing chains with a padlock on the chest",
      tags=["escape artist", "chains", "padlock", "magic", "stunt", "bound"], aliases=["chain-escape"])
def _(S):
    return [
        dot(12, 3.8, HR),
        shell(rect(7, 7, 10, 14, pick(S, 1, 4))),
        detail(seg(7, 9.5, 17, 18.5)),
        detail(seg(17, 9.5, 7, 18.5)),
        Part("dot", rect(9.2, 12.6, 5.6, 4.4, 0.6)),
        detail(arc(12, 12.6, 1.9, 180, 360)),
    ]


@icon("levitation-illusion", CAT, "Figure lying horizontally in mid air above a low table with a hoop passing around the body",
      tags=["levitation", "floating", "illusion", "magic trick", "hoop", "magician", "hover"], aliases=["floating-lady"])
def _(S):
    return [
        dot(4.5, 8.5, HR),
        limb(S, (8, 9), (10.5, 9)),
        limb(S, (17.5, 9), (21, 9)),
        line(ellipse(14, 9, 2.4, 5.5)),
        shell(rect(3, 16, 18, 3, pick(S, 0, 1.2))),
        line(seg(5.5, 19.5, 5.5, 22)), line(seg(18.5, 19.5, 18.5, 22)),
    ]


# --------------------------------------------------------------------------- magic, mime and clowning

def crescent(cx, cy, r, off, r2):
    return path_to_d(D(P(circle(cx, cy, r)), P(circle(cx + off, cy - off * 0.6, r2))))


@icon("hypnosis-pendulum", CAT, "Pocket watch with a spiral on its face swinging from a chain between two curved swing lines",
      tags=["hypnosis", "pendulum", "pocket watch", "hypnotist", "swinging", "trance", "mesmerize"], aliases=["hypnotist-watch"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 6)),
        solid(rect(10.5, 5.5, 3, 2.5, 0.5)),
        shell(circle(12, 14.5, 6.5)),
        dot(12, 14.5, 1),
        detail(arc(12, 14.5, 3, 30, 340)),
        line(arc(12, 14.5, 9.5, 160, 200)),
        line(arc(12, 14.5, 9.5, -20, 20)),
    ]


@icon("mentalist", CAT, "Face with fingertips pressed to both temples and short rays shooting out from the forehead",
      tags=["mentalist", "mind reading", "psychic", "telepathy", "concentration", "mind power", "magic"], aliases=["mind-reader"])
def _(S):
    rays = [line(seg(*polar(12, 14, 9.3, a), *polar(12, 14, 12, a))) for a in (-125, -90, -55)]
    return rays + [
        shell(circle(12, 14, 6.3)),
        dot(9.8, 14, 0.9), dot(14.2, 14, 0.9),
        limb(S, (3, 21), (2.8, 15), (5.2, 12)),
        limb(S, (21, 21), (21.2, 15), (18.8, 12)),
    ]


@icon("magic-cabinet", CAT, "Upright cabinet on short legs with a star on one door and a crescent moon on the other",
      tags=["magic cabinet", "vanishing cabinet", "illusion", "magician", "star", "moon", "box"], aliases=["magician-cabinet"])
def _(S):
    return [
        shell(rect(4.5, 3, 15, 14.5, pick(S, 0.5, 2.5))),
        detail(seg(12, 3, 12, 17.5)),
        Part("dot", poly(star_pts(8.2, 10.4, 2.7, 1.2), closed=True)),
        Part("dot", crescent(15.8, 10.4, 2.5, 1.1, 2.1)),
        line(seg(7, 17.5, 7, 21.5)), line(seg(17, 17.5, 17, 21.5)),
    ]


@icon("vanishing-act", CAT, "Standing figure dissolving into scattered dots on one side with a small puff of smoke at the feet",
      tags=["vanishing", "disappear", "magic trick", "magician", "illusion", "dissolve", "smoke"], aliases=["disappearing-act"])
def _(S):
    return [
        dot(7.5, 4.8, HR),
        limb(S, (7.5, 8.2), (7.5, 14)),
        limb(S, (7.5, 9.8), (4, 13)),
        limb(S, (7.5, 14), (5, 19.5)),
        limb(S, (7.5, 14), (10, 19.5)),
        dot(12.8, 5.5, 0.9), dot(15.5, 8, 0.9), dot(12.6, 10.6, 0.9), dot(18.2, 10.3, 0.9),
        dot(15.5, 13.6, 0.9), dot(19.5, 14.8, 0.9), dot(11.5, 14.8, 0.8),
        line("M12.5 20.5A1.7 1.7 0 0 1 15.9 20.5A1.7 1.7 0 0 1 19.3 20.5A1.7 1.7 0 0 1 22 20.5"),
    ]


@icon("rising-rope-trick", CAT, "Rope curling straight up out of a woven basket and fading into dots at the top",
      tags=["rope trick", "snake charmer", "basket", "indian rope trick", "magic", "illusion", "rising rope"], aliases=["indian-rope-trick"])
def _(S):
    return [
        shell(poly([(5, 13.5), (19, 13.5), (17.5, 21.5), (6.5, 21.5)], closed=True, r=pick(S, 0, 1))),
        detail(seg(5.8, 17.5, 18.2, 17.5)),
        line("M11 13.5V3.5"),
        dot(15.8, 6.5, 1.7),
        limb(S, (15.8, 8.5), (15.6, 12)),
    ]


@icon("spoon-bending", CAT, "Spoon with its handle bent over at a sharp angle and curved lines around the bend",
      tags=["spoon bending", "psychokinesis", "mentalism", "uri", "telekinesis", "bent spoon", "magic trick"], aliases=["bent-spoon"])
def _(S):
    bowl = ellipse(8, 6.2, 3.3, 4.2)
    return [
        shell(bowl),
        limb(S, (8, 10.4), (8, 14), (19.5, 20.5)),
        line(arc(8, 14, 4.8, 140, 220)),
    ]


@icon("pie-in-face", CAT, "Round face with a cream pie pressed flat across it and drips of cream running down",
      tags=["pie in the face", "custard pie", "slapstick", "prank", "cream", "comedy", "clown"], aliases=["pie-face"])
def _(S):
    cream = "M5 12C4.5 9.5 6.5 8 8.5 9C9.5 7 14.5 7 15.5 9C17.5 8 19.5 9.5 19 12V14H5Z"
    return [
        line(circle(12, 12, 9.5)),
        shell(cream),
        line(seg(8, 14.5, 8, 17.5)), line(seg(12.5, 14.5, 12.5, 18.5)), line(seg(16.5, 14.5, 16.5, 16.5)),
    ]


@icon("disguise-glasses", CAT, "Novelty glasses with an attached big nose, bushy eyebrows and a thick moustache",
      tags=["disguise", "fake nose", "moustache", "mustache", "novelty", "costume", "funny glasses"], aliases=["nose-glasses"])
def _(S):
    must = "M5 19.5C8 16.8 11 18 12 19C13 18 16 16.8 19 19.5C16 21.5 13.5 20.5 12 20C10.5 20.5 8 21.5 5 19.5Z"
    return [
        line(arc(5.8, 11.5, 5, 220, 320)),
        line(arc(18.2, 11.5, 5, 220, 320)),
        shell(circle(5.8, 11.5, 2.8)), shell(circle(18.2, 11.5, 2.8)),
        line(seg(8.6, 11.5, 15.4, 11.5)),
        shell(ellipse(12, 14.9, 2, 2.3)),
        solid(must),
    ]


@icon("spring-eye-glasses", CAT, "Novelty glasses with two eyeballs bouncing out of the lenses on coiled springs",
      tags=["spring glasses", "googly eyes", "eyeballs", "novelty", "silly glasses", "prank", "costume"], aliases=["googly-eye-glasses"])
def _(S):
    def spring(x):
        return line(poly([(x, 13), (x - 1.6, 11.6), (x + 1.6, 10.2), (x - 1.6, 8.8), (x + 1.6, 7.4), (x, 6.6)]))
    return [
        shell(circle(6.5, 17, 3)), shell(circle(17.5, 17, 3)),
        line(seg(9.5, 17, 14.5, 17)),
        spring(6.5), spring(17.5),
        shell(circle(6.5, 4.6, 2.6)), shell(circle(17.5, 4.6, 2.6)),
        dot(6.5, 4.6, 0.9), dot(17.5, 4.6, 0.9),
    ]


@icon("spring-punch-glove", CAT, "Boxing glove shooting out of a small box on a zigzag spring",
      tags=["boxing glove", "spring", "punch", "prank", "jack in the box", "gag", "surprise"], aliases=["punching-glove-box"])
def _(S):
    x0, y0, x1, y1 = 8.2, 14.2, 13.5, 9.5
    dx, dy = x1 - x0, y1 - y0
    n = math.hypot(dx, dy)
    nx, ny = -dy / n, dx / n
    pts = [(x0, y0)]
    for i in range(1, 6):
        t = i / 6
        sgn = 1 if i % 2 else -1
        pts.append((x0 + dx * t + nx * 1.7 * sgn, y0 + dy * t + ny * 1.7 * sgn))
    pts.append((x1, y1))
    glove = u(path_to_d(transform_path(P(ellipse(17, 7, 5, 3.6)), rotation(-40, 17, 7))),
              rot_rect(S, 13.4, 10.6, 3.6, 3.4, 50, r=0))
    return [
        shell(rect(2.5, 14.5, 9, 7, pick(S, 0.5, 2.5))),
        line(poly(pts)),
        shell(glove),
    ]


@icon("jester-marotte", CAT, "Short stick topped with a carved jester head in a three-pointed hat with bells",
      tags=["marotte", "jester", "fool", "scepter", "court jester", "medieval", "comedy"], aliases=["jester-stick"])
def _(S):
    hat = poly([(8.6, 11), (5.5, 6.5), (10, 7.8), (12, 3.8), (14, 7.8), (18.5, 6.5), (15.4, 11)], closed=True, r=pick(S, 0, 0.8))
    return [
        shell(hat),
        dot(5.2, 5.2, 1.2), dot(12, 2.8, 1.2), dot(18.8, 5.2, 1.2),
        shell(circle(12, 13.5, 3.3)),
        line(seg(12, 16.8, 12, 22)),
    ]


@icon("zanni-mask", CAT, "Half mask with arched brows and a very long pointed nose, as worn in commedia dell'arte",
      tags=["zanni", "commedia dell'arte", "mask", "half mask", "long nose", "theatre mask", "italian comedy"], aliases=["commedia-mask"])
def _(S):
    mask = "M3 8C7 4 17 4 21 8C20.5 11 17.5 12.5 14.5 11.5L12 20.5L9.5 11.5C6.5 12.5 3.5 11 3 8Z"
    return [
        shell(mask),
        Part("dot", ellipse(7.5, 8.6, 1.7, 1.1)),
        Part("dot", ellipse(16.5, 8.6, 1.7, 1.1)),
    ]


@icon("rimshot", CAT, "Snare drum and a crash cymbal on a stand with a drumstick striking the rim and small hit marks",
      tags=["rimshot", "ba dum tss", "drum", "joke", "comedy", "punchline", "cymbal", "snare"], aliases=["ba-dum-tss"])
def _(S):
    return [
        shell(rect(2.5, 13.5, 12, 7.5, pick(S, 0.5, 2.5))),
        detail(seg(2.5, 16, 14.5, 16)),
        line(seg(15.5, 6.5, 22, 9)),
        line(seg(18.7, 8, 18.7, 21.5)),
        line(seg(3, 4.5, 9.5, 11)),
        line(seg(11, 8.5, 12.5, 7)), line(seg(12.5, 11, 14.5, 11)),
    ]


@icon("chattering-teeth", CAT, "Wind-up set of big grinning false teeth on little feet with a key on the side",
      tags=["chattering teeth", "wind up toy", "false teeth", "novelty", "joke", "dentures", "toy"], aliases=["wind-up-teeth"])
def _(S):
    return [
        shell(rect(3, 6.5, 14, 9, pick(S, 1, 4))),
        detail(seg(3, 11, 17, 11)),
        detail(seg(7.7, 6.5, 7.7, 11)), detail(seg(12.3, 6.5, 12.3, 11)),
        detail(seg(10, 11, 10, 15.5)),
        line(poly([(6.5, 15.5), (6.5, 19.5), (9.5, 19.5)])),
        line(poly([(13.5, 15.5), (13.5, 19.5), (16.5, 19.5)])),
        line(seg(17, 11, 19, 11)),
        shell(ellipse(20.3, 11, 1.6, 3.3)),
    ]


@icon("arrow-through-head", CAT, "Smiling head with a novelty arrow whose front and back halves stick out either side",
      tags=["arrow through head", "novelty", "joke", "headband", "costume", "silly", "prank"], aliases=["arrow-headband"])
def _(S):
    return [
        shell(circle(12, 13, 6.2)),
        dot(9.8, 13, 0.9), dot(14.2, 13, 0.9),
        detail(arc(12, 14.2, 2.6, 25, 155)),
        line(seg(4.5, 8.5, 6.5, 8.5)),
        line(seg(2.5, 6.5, 4.5, 8.5)), line(seg(2.5, 10.5, 4.5, 8.5)),
        line(seg(17.5, 8.5, 19, 8.5)),
        solid(poly([(19, 6.3), (22, 8.5), (19, 10.7)], closed=True)),
    ]


@icon("surtitle-display", CAT, "Long narrow text screen above a stage arch showing two lines of translated words",
      tags=["surtitles", "supertitles", "captions", "opera", "theatre", "subtitles", "translation"], aliases=["supertitle-display"])
def _(S):
    return [
        shell(rect(3, 2, 18, 9, pick(S, 0.5, 2.5))),
        detail(seg(6.5, 5.3, 17.5, 5.3)),
        detail(seg(6.5, 8, 13.5, 8)),
        line(poly([(3, 14), (3, 21), (21, 21), (21, 14)], r=S.r)),
        line(seg(8, 14, 8, 17)), line(seg(16, 14, 16, 17)),
    ]


@icon("wind-machine-theater", CAT, "Slatted wooden drum on a stand with a crank handle, used to make wind sounds on stage",
      tags=["wind machine", "sound effect", "foley", "backstage", "theatre", "crank", "drum"], aliases=["theatre-wind-machine"])
def _(S):
    return [
        shell(rect(3, 4.5, 14, 9, pick(S, 1, 3.5))),
        detail(seg(7.5, 4.5, 7.5, 13.5)), detail(seg(10, 4.5, 10, 13.5)), detail(seg(12.5, 4.5, 12.5, 13.5)),
        line(seg(6, 13.5, 4, 21.5)), line(seg(14, 13.5, 16, 21.5)),
        line(poly([(17, 9), (20.5, 9), (20.5, 13)], r=S.r)),
    ]


@icon("stage-door", CAT, "Plain door with a star above it, the entrance backstage for performers",
      tags=["stage door", "backstage", "theatre", "entrance", "performers", "star", "door"], aliases=["backstage-door"])
def _(S):
    return [
        solid(poly(star_pts(12, 4.8, 3.4, 1.5), closed=True)),
        shell(rect(6, 9.5, 12, 12, pick(S, 0.5, 2.5))),
        Part("dot", circle(14.8, 16, 1)),
    ]


@icon("theater-seat", CAT, "Padded auditorium seat with a rounded back, armrests and a small number plate",
      tags=["theatre seat", "auditorium", "cinema seat", "stalls", "chair", "ticket", "row"], aliases=["auditorium-seat"])
def _(S):
    return [
        shell(rect(7.5, 2.5, 9, 10.5, pick(S, 1, 3.5))),
        Part("dot", rect(10.5, 5.5, 3, 2.2, 0.4)),
        shell(rect(5.5, 13.5, 13, 4.5, pick(S, 0.5, 2))),
        line(seg(3.5, 9.5, 3.5, 18)), line(seg(20.5, 9.5, 20.5, 18)),
        line(seg(12, 18, 12, 21)), line(seg(8, 21, 16, 21)),
    ]


@icon("play-script", CAT, "Bound script page with brass fasteners showing a character name above each block of dialogue",
      tags=["script", "play script", "screenplay", "lines", "dialogue", "actor", "rehearsal"], aliases=["playscript"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, pick(S, 0.5, 2.5))),
        dot(7.8, 6, 0.9), dot(7.8, 12, 0.9), dot(7.8, 18, 0.9),
        detail(seg(11.5, 6.5, 14, 6.5)), detail(seg(11.5, 9.5, 16.5, 9.5)),
        detail(seg(11.5, 14, 14, 14)), detail(seg(11.5, 17, 16.5, 17)),
    ]


@icon("stage-flying", CAT, "Performer in a harness hanging from two wires in mid air above the stage floor",
      tags=["stage flying", "wires", "harness", "theatre", "aerial", "rigging"], aliases=["flying-actor"])
def _(S):
    return [
        line(seg(3, 2.5, 21, 2.5)),
        line(seg(6, 2.5, 9, 10.5)), line(seg(18, 2.5, 15, 10.5)),
        line(seg(9, 10.5, 15, 10.5)),
        dot(12, 6.3, 2),
        limb(S, (12, 10.5), (12, 15.5)),
        limb(S, (12, 15.5), (8.5, 18.5), (6.5, 17)),
        limb(S, (12, 15.5), (15.5, 18.5), (17.5, 17)),
        line(seg(3, 21, 21, 21)),
    ]


@icon("zig-zag-illusion", CAT, "Tall cabinet in three sections with the middle one shifted sideways and a face in the top window",
      tags=["zig zag girl", "illusion", "magic trick", "cabinet", "magician", "sliced", "box trick"], aliases=["zigzag-illusion"])
def _(S):
    rr = pick(S, 0, 1)
    return [
        shell(rect(4.5, 2, 9, 6.5, rr)),
        shell(rect(10.5, 8.5, 9, 6.5, rr)),
        shell(rect(4.5, 15, 9, 6, rr)),
        Part("dot", circle(7.8, 5.2, 0.8)), Part("dot", circle(10.2, 5.2, 0.8)),
    ]


@icon("sword-basket-illusion", CAT, "Wicker basket pierced by two crossed swords at different angles",
      tags=["sword basket", "indian basket trick", "swords", "magic trick", "illusion", "magician", "wicker"], aliases=["basket-swords"])
def _(S):
    def sword(a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = math.hypot(dx, dy)
        ux, uy = dx / n, dy / n
        px, py = a[0] + ux * 2.6, a[1] + uy * 2.6
        return [line(seg(a[0], a[1], b[0], b[1])), line(seg(px - uy * 2.2, py + ux * 2.2, px + uy * 2.2, py - ux * 2.2))]
    return sword((6, 2.5), (14, 12.5)) + sword((18, 2.5), (10, 12.5)) + [
        shell(poly([(4.5, 12.5), (19.5, 12.5), (17.5, 21.5), (6.5, 21.5)], closed=True, r=pick(S, 0, 1))),
        detail(seg(5.4, 17, 18.6, 17)),
    ]


@icon("high-dive-act", CAT, "Tall thin ladder tower with a tiny diver leaping toward a small tank of water at the bottom",
      tags=["high dive", "diving act", "circus", "daredevil", "stunt", "water tank", "ladder"], aliases=["tank-diving"])
def _(S):
    rungs = [line(seg(5, y, 9, y)) for y in (6, 10, 14, 18)]
    return rungs + [
        line(seg(5, 2.5, 5, 22)), line(seg(9, 2.5, 9, 22)),
        line(seg(3.5, 2.5, 12, 2.5)),
        limb(S, (13, 5.5), (15.5, 9.5)),
        dot(16.8, 11.8, 1.9),
        shell(rect(12.5, 16.5, 9, 5, pick(S, 0, 1.5))),
    ]


@icon("clown-car", CAT, "Tiny car with several clowns in pointed hats squeezed out of the open roof",
      tags=["clown car", "circus", "clowns", "tiny car", "funny", "crowd", "stunt"], aliases=["clown-vehicle"])
def _(S):
    hats = [solid(poly([(x - 1.9, 8), (x, 3), (x + 1.9, 8)], closed=True)) for x in (6.5, 12, 17.5)]
    return hats + [
        dot(6.5, 10.2, 2), dot(12, 10.2, 2), dot(17.5, 10.2, 2),
        shell(rect(2.5, 13.5, 19, 5.5, pick(S, 1, 2.7))),
        shell(circle(7, 19.8, 2.2)), shell(circle(17, 19.8, 2.2)),
    ]


@icon("harlequin-costume", CAT, "Figure in a diamond-patterned suit with a wide bicorne hat",
      tags=["harlequin", "commedia dell'arte", "diamond pattern", "costume", "jester", "carnival", "arlecchino"], aliases=["harlequin-suit"])
def _(S):
    return [
        solid(poly([(4.5, 5), (8, 2), (16, 2), (19.5, 5), (16, 4.2), (8, 4.2)], closed=True)),
        dot(12, 7.4, 2.1),
        shell(poly([(7.5, 10.5), (16.5, 10.5), (16.5, 17), (7.5, 17)], closed=True, r=pick(S, 0, 1))),
        detail(poly([(12, 10.5), (16.5, 13.75), (12, 17), (7.5, 13.75)], closed=True)),
        limb(S, (7.5, 11.5), (4, 15)),
        limb(S, (16.5, 11.5), (20, 15)),
        limb(S, (10, 17), (9, 21.5)), limb(S, (14, 17), (15, 21.5)),
    ]
