"""TypeIcon Core: wellness (batch 001): strength machines, benches, racks, cardio machines, bars and rings,
balls and rollers, conditioning gear, boxing and gym accessories, tracking tools and training figures.

Equipment is drawn flat from the side or front with 2 px strokes; moving or hanging parts are simplified.
Figures follow the shared stick-figure style (solid head r 2.25, 2 px limbs).
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import P, path_to_d, rotation, transform_path

CAT = "wellness"


def rot_d(d, deg, cx=12.0, cy=12.0):
    """Rotate a path string clockwise by deg about (cx, cy)."""
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def pick(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


def pl(S, pts):
    return line(poly(pts, r=S.r))


def hd(x, y):
    return dot(x, y, 2.25)


def sq(x, y, w, h):
    return Part("dot", rect(x, y, w, h))


def rrect(cx, cy, w, h, deg, r=0.0):
    """Rectangle w x h centred on (cx, cy), turned clockwise by deg, as a closed polygon (corners filleted by r)."""
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    pts = [(cx + x * c - y * sn, cy + x * sn + y * c) for x, y in
           [(-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)]]
    return poly(pts, closed=True, r=r)


def rr(S, cap=2):
    """Corner radius for small rectangles: tight in Line, up to cap in Rounded."""
    return min(cap / 2, 0.75) if S.name == "line" else cap


# =========================================================================== strength equipment

@icon("weight-plate", CAT, "Front view of a round barbell weight plate with a ring groove and a centre hole.",
      tags=["weight plate", "barbell plate", "iron plate", "weights", "gym", "strength", "lifting"],
      aliases=["barbell-plate"])
def _(S):
    hole = Part("dot", rect(10.5, 10.5, 3, 3)) if S.name == "line" else dot(12, 12, 1.6)
    return [shell(circle(12, 12, 9)), detail(circle(12, 12, 5)), hole]


@icon("ez-curl-bar", CAT, "Side view of a short barbell whose middle section zigzags in a W shape, with a plate on each end.",
      tags=["ez bar", "curl bar", "zigzag bar", "barbell", "biceps", "triceps", "gym"], aliases=["ez-bar"])
def _(S):
    return [shell(rect(2, 6.5, 3.5, 11, rr(S, 1.5))), shell(rect(18.5, 6.5, 3.5, 11, rr(S, 1.5))),
            pl(S, [(5.5, 12), (8, 12), (9.75, 16), (12, 8), (14.25, 16), (16, 12), (18.5, 12)])]


@icon("trap-bar", CAT, "Top view of a hexagonal bar frame with two parallel handles inside and sleeves sticking out of both ends.",
      tags=["trap bar", "hex bar", "hexagonal bar", "deadlift", "shrug", "barbell", "gym"], aliases=["hex-bar"])
def _(S):
    return [shell(poly([(5, 12), (8, 4.5), (16, 4.5), (19, 12), (16, 19.5), (8, 19.5)], closed=True, r=S.r)),
            detail(seg(9, 9, 15, 9)), detail(seg(9, 15, 15, 15)),
            line(seg(1.5, 12, 5, 12)), line(seg(19, 12, 22.5, 12))]


@icon("weight-bench", CAT, "Side view of a flat padded bench on an upright front leg and a wider rear foot.",
      tags=["weight bench", "flat bench", "bench press", "gym bench", "padded bench", "strength", "gym"],
      aliases=["flat-bench"])
def _(S):
    return [shell(rect(2.5, 7, 19, 5, rr(S, 2))),
            pl(S, [(6, 12), (6, 21)]), pl(S, [(3.5, 21.5), (8.5, 21.5)]),
            pl(S, [(18, 12), (18, 21)]), pl(S, [(14.5, 21.5), (21.5, 21.5)])]


@icon("incline-bench", CAT, "Side view of a bench whose backrest is raised at an angle with a short flat seat and a base frame.",
      tags=["incline bench", "adjustable bench", "backrest", "gym bench", "chest", "strength"],
      aliases=["adjustable-bench"])
def _(S):
    return [shell(poly([(2.5, 5.5), (5.5, 3), (11.5, 9.5), (8.5, 12.5)], closed=True, r=S.r)),
            shell(rect(12, 11, 9.5, 4.5, rr(S, 1.5))),
            pl(S, [(9, 14.5), (6, 21.5)]), pl(S, [(17, 15.5), (17, 21.5)]),
            pl(S, [(3, 21.5), (21, 21.5)])]


@icon("preacher-curl-bench", CAT, "Side view of a small seat facing a sloped padded arm rest that rises toward the lifter, on a post and base.",
      tags=["preacher curl", "preacher bench", "scott bench", "biceps", "arm curl", "gym"],
      aliases=["scott-bench"])
def _(S):
    return [shell(poly([(2.5, 10.5), (13, 6), (13, 10), (2.5, 14.5)], closed=True, r=S.r)),
            pl(S, [(8, 12.5), (8, 21.5)]),
            shell(rect(15.5, 13, 6, 3.5, rr(S, 1.5))), pl(S, [(18.5, 16.5), (18.5, 21.5)]),
            pl(S, [(4, 21.5), (21, 21.5)])]


@icon("roman-chair", CAT, "Side view of a hyperextension bench: angled frame with a hip pad at the top and ankle rollers at the bottom.",
      tags=["roman chair", "hyperextension", "back extension", "ab bench", "lower back", "gym"],
      aliases=["hyperextension-bench"])
def _(S):
    return [shell(poly([(13, 5.5), (19.5, 8.5), (17.5, 12), (11, 9)], closed=True, r=S.r)),
            pl(S, [(15, 11), (6, 17)]),
            pl(S, [(18, 11), (18, 21.5)]),
            pl(S, [(3, 21.5), (21, 21.5)]),
            dot(3.5, 13.5, 1.75), dot(3.5, 18.5, 1.75)]


@icon("squat-rack", CAT, "Front view of two tall upright posts on a base with J hooks holding a barbell across them.",
      tags=["squat rack", "barbell rack", "squat stand", "power rack", "barbell", "gym", "strength"],
      aliases=["squat-stand"])
def _(S):
    return [pl(S, [(3.5, 21.5), (7, 21.5), (7, 3)]), pl(S, [(20.5, 21.5), (17, 21.5), (17, 3)]),
            pl(S, [(7, 12.5), (10, 12.5), (10, 10.5)]), pl(S, [(17, 12.5), (14, 12.5), (14, 10.5)]),
            line(seg(4, 8, 20, 8)), sq(1.5, 4.5, 2.5, 7), sq(20, 4.5, 2.5, 7)]


@icon("power-cage", CAT, "Three-quarter view of a four-post box cage with crossbars at the top and a barbell resting inside.",
      tags=["power cage", "power rack", "safety rack", "cage", "barbell", "squat", "gym"],
      aliases=["half-rack"])
def _(S):
    return [pl(S, [(5, 21.5), (5, 8), (9, 4), (21, 4), (21, 16)]),
            pl(S, [(5, 8), (15, 8), (15, 21.5)]),
            pl(S, [(15, 8), (21, 4)]),
            line(seg(2, 14.5, 18, 14.5)), sq(1.5, 11.5, 2, 6)]


@icon("smith-machine", CAT, "Front view of a barbell fixed to two vertical guide rails inside a tall frame.",
      tags=["smith machine", "guided barbell", "smith rack", "squat machine", "barbell", "gym"],
      aliases=["smith-rack"])
def _(S):
    return [pl(S, [(8, 21.5), (8, 3), (16, 3), (16, 21.5)]), pl(S, [(4.5, 21.5), (19.5, 21.5)]),
            line(seg(2, 12, 22, 12)), sq(1.5, 8.5, 2.5, 7), sq(20, 8.5, 2.5, 7),
            sq(6.5, 10.5, 3, 3), sq(14.5, 10.5, 3, 3)]


@icon("cable-machine", CAT, "Front view of a tall frame with a pulley at the top, a cable running down and a D handle hanging from it.",
      tags=["cable machine", "cable crossover", "pulley", "cable station", "gym", "strength", "handle"],
      aliases=["cable-station"])
def _(S):
    return [pl(S, [(4, 22), (4, 3), (15, 3)]), shell(circle(15, 6.5, 2.5)),
            line(seg(17.5, 6.5, 17.5, 16)),
            shell(rect(14.5, 16, 6.5, 4.5, rr(S, 2)))]


@icon("lat-pulldown-machine", CAT, "Side view of a seat with knee pads under a tall frame, a wide bar hanging from a cable above.",
      tags=["lat pulldown", "pulldown machine", "back", "lats", "cable", "gym", "strength"],
      aliases=["lat-pulldown"])
def _(S):
    return [pl(S, [(4, 21.5), (4, 3), (15, 3)]), line(seg(15, 3, 15, 6.5)),
            pl(S, [(10.5, 5.5), (12, 9), (18, 9), (19.5, 5.5)]),
            line(seg(4, 13.5, 7, 13.5)), shell(rect(7, 11.5, 4, 3.5, 1)),
            shell(rect(11, 17.5, 10, 4, rr(S, 1.5)))]


@icon("leg-press-machine", CAT, "Side view of a reclined seat facing a large angled footplate on diagonal rails.",
      tags=["leg press", "leg machine", "sled press", "quads", "glutes", "gym", "strength"],
      aliases=["leg-press"])
def _(S):
    return [pl(S, [(2.5, 21.5), (21.5, 21.5)]),
            pl(S, [(6, 18), (17, 7)]),
            shell(rrect(17.5, 6.5, 10, 3.5, 45, rr(S, 1))),
            shell(rrect(8.5, 10.5, 8, 3.5, 45, rr(S, 1)))]


@icon("multi-gym", CAT, "Front view of a home gym station: weight stack in a tall frame, a bench seat and a pulley arm.",
      tags=["multi gym", "home gym", "gym station", "weight machine", "fitness station", "strength"],
      aliases=["home-gym"])
def _(S):
    return [shell(rect(2.5, 2.5, 8, 19, rr(S, 2))), detail(seg(2.5, 8.5, 10.5, 8.5)), detail(seg(2.5, 14.5, 10.5, 14.5)),
            pl(S, [(10.5, 5), (20, 5), (20, 10)]), dot(20, 12, 1.5),
            shell(rect(13, 16, 8.5, 3, rr(S, 1))), pl(S, [(17, 19), (17, 21.5)])]


@icon("weight-stack", CAT, "Front view of a vertical stack of rectangular weight plates with a pin in one slot and a rod through the middle.",
      tags=["weight stack", "selectorized", "stack pin", "machine weights", "plates", "gym"],
      aliases=["selector-pin"])
def _(S):
    return [shell(rect(7, 2.5, 12, 19, rr(S, 2))), detail(seg(7, 8.5, 19, 8.5)), detail(seg(7, 14.5, 19, 14.5)),
            line(seg(2, 11.5, 12, 11.5))]

@icon("dumbbell-rack", CAT, "Front view of a two-tier rack holding a row of dumbbell heads on each shelf.",
      tags=["dumbbell rack", "weight rack", "dumbbell stand", "free weights", "gym storage", "gym"],
      aliases=["dumbbell-stand"])
def _(S):
    heads = [dot(x, y, 2) for y in (7.5, 17) for x in (7, 12, 17)]
    return heads + [pl(S, [(2.5, 12), (21.5, 12)]), pl(S, [(2.5, 21.5), (21.5, 21.5)]),
                    pl(S, [(3, 12), (3, 21.5)]), pl(S, [(21, 12), (21, 21.5)])]


@icon("plate-tree", CAT, "Front view of an upright post on a base with round weight plates hanging on pegs at both sides.",
      tags=["plate tree", "plate rack", "weight tree", "plate storage", "weights", "gym"],
      aliases=["weight-tree"])
def _(S):
    peg = (lambda x, y: Part("dot", rect(x - 1, y - 1, 2, 2))) if S.name == "line" else (lambda x, y: dot(x, y, 1.1))
    plates = [shell(circle(x, y, 3.75)) for x in (5.5, 18.5) for y in (6.5, 15.5)]
    pegs = [peg(x, y) for x in (5.5, 18.5) for y in (6.5, 15.5)]
    return plates + pegs + [pl(S, [(12, 2.5), (12, 21.5)]), pl(S, [(6.5, 21.5), (17.5, 21.5)])]


@icon("barbell-collar", CAT, "Side view of a spring clip collar: a coiled ring with two handles sticking out.",
      tags=["barbell collar", "spring collar", "clip collar", "bar clamp", "weight lock", "gym"],
      aliases=["spring-collar"])
def _(S):
    return [line(arc(12, 14, 6, 295, 245)), pl(S, [(17.4, 11.5), (19.5, 3.5)]), pl(S, [(6.6, 11.5), (4.5, 3.5)]),
            dot(12, 14, 2.25)]


# =========================================================================== cardio machines

@icon("exercise-bike", CAT, "Side view of an upright stationary bike with a front flywheel, handlebars and a seat on a fixed base.",
      tags=["exercise bike", "stationary bike", "spin bike", "indoor cycling", "cardio", "gym"],
      aliases=["stationary-bike"])
def _(S):
    return [pl(S, [(3, 21.5), (21, 21.5)]), shell(circle(16, 15.5, 4)),
            pl(S, [(19.5, 4), (16, 4), (16, 11.5)]),
            pl(S, [(4.5, 7), (10.5, 7)]), pl(S, [(7.5, 7), (8, 21.5)]),
            pl(S, [(8, 16), (13, 16)])]


@icon("recumbent-bike", CAT, "Side view of a stationary bike with a low seat with backrest and pedals out in front.",
      tags=["recumbent bike", "reclined bike", "seated bike", "cardio", "low impact", "gym"],
      aliases=["recumbent-exercise-bike"])
def _(S):
    return [shell(poly([(3, 4.5), (6, 4), (7, 12), (3.5, 12.5)], closed=True, r=S.r)),
            shell(rect(3.5, 13.5, 8, 3, rr(S, 1.5))),
            pl(S, [(8, 16.5), (8, 21.5)]), pl(S, [(3, 21.5), (21, 21.5)]),
            pl(S, [(11, 16), (19, 12.5), (19, 21.5)]),
            line(seg(16, 8, 21.5, 8)), pl(S, [(18.5, 8), (18.5, 12)])]


@icon("air-bike", CAT, "Side view of a stationary bike with a large round fan wheel at the front and long moving handles.",
      tags=["air bike", "fan bike", "assault bike", "cardio", "hiit", "gym"],
      aliases=["fan-bike"])
def _(S):
    return [shell(circle(16.5, 9.5, 6)), detail(seg(16.5, 5, 16.5, 14)), detail(seg(12, 9.5, 21, 9.5)),
            pl(S, [(16.5, 15.5), (11, 21.5)]), pl(S, [(3, 21.5), (21, 21.5)]),
            pl(S, [(3.5, 12.5), (9.5, 12.5)]), pl(S, [(6.5, 12.5), (6.5, 21.5)]),
            pl(S, [(6, 3.5), (9, 6.5), (11, 16)])]


@icon("rowing-machine", CAT, "Side view of a long low rail with a sliding seat, foot straps and a round flywheel housing at the front.",
      tags=["rowing machine", "rower", "erg", "ergometer", "cardio", "indoor rowing", "gym"],
      aliases=["indoor-rower"])
def _(S):
    return [pl(S, [(2, 20), (22, 20)]), shell(circle(17.5, 12.5, 5)), dot(17.5, 12.5, 1.25),
            shell(rect(3.5, 13, 6.5, 2.5, rr(S, 1))),
            pl(S, [(11.5, 17), (11.5, 11)])]


@icon("elliptical-trainer", CAT, "Side view of a machine with two long foot pedals, tall moving arm poles and an oval track base.",
      tags=["elliptical", "cross trainer", "elliptical machine", "cardio", "low impact", "gym"],
      aliases=["cross-trainer"])
def _(S):
    return [line(ellipse(11, 18, 8.5, 3)),
            pl(S, [(15, 3), (19.5, 18)]), pl(S, [(12, 3), (18, 3)]),
            line(seg(10, 12.5, 18, 12.5)), shell(rect(3.5, 10.5, 7, 3, rr(S, 1.5)))]


# =========================================================================== bars, rings and bands

@icon("pull-up-bar", CAT, "Front view of a straight bar spanning a doorway frame with two grips.",
      tags=["pull-up bar", "chin-up bar", "doorway bar", "calisthenics", "bar", "home gym"],
      aliases=["chin-up-bar"])
def _(S):
    return [pl(S, [(3, 21.5), (3, 3.5), (21, 3.5), (21, 21.5)]),
            line(seg(3, 9.5, 21, 9.5)), sq(7, 7.5, 3, 4), sq(14, 7.5, 3, 4)]


@icon("dip-station", CAT, "Three-quarter view of a stand with two parallel raised bars on legs.",
      tags=["dip station", "dip bars", "parallel bars", "calisthenics", "triceps", "gym"],
      aliases=["dip-bars"])
def _(S):
    return [shell(rect(9, 5.5, 12, 3, rr(S, 1.5))), pl(S, [(10, 8.5), (10, 15)]), pl(S, [(20, 8.5), (20, 15)]),
            shell(rect(3, 11.5, 12, 3, rr(S, 1.5))), pl(S, [(4, 14.5), (4, 21.5)]), pl(S, [(14, 14.5), (14, 21.5)])]


@icon("push-up-bars", CAT, "Side view of a pair of low stands, each a horizontal grip bar on two short feet.",
      tags=["push-up bars", "push up stands", "pushup handles", "calisthenics", "chest", "home gym"],
      aliases=["push-up-stands"])
def _(S):
    return [pl(S, [(3, 21.5), (3, 12), (11, 12), (11, 21.5)]), pl(S, [(13, 21.5), (13, 12), (21, 12), (21, 21.5)])]


@icon("gymnastic-rings", CAT, "Two round rings hanging side by side from long straps.",
      tags=["gymnastic rings", "gym rings", "still rings", "calisthenics", "strap", "gymnastics"],
      aliases=["gym-rings"])
def _(S):
    return [shell(circle(6.5, 16, 4.5)), shell(circle(17.5, 16, 4.5)),
            line(seg(6.5, 2, 6.5, 10)), line(seg(17.5, 2, 17.5, 10))]


@icon("suspension-trainer", CAT, "Two straps hanging from one anchor point in a V shape, each ending in a handle.",
      tags=["suspension trainer", "strap trainer", "trx style straps", "bodyweight", "straps", "functional fitness"],
      aliases=["suspension-straps"])
def _(S):
    return [pl(S, [(12, 2.5), (12, 4.5)]), line(seg(12, 4.5, 6.5, 15)), line(seg(12, 4.5, 17.5, 15)),
            shell(rect(3.5, 15, 6.5, 4.5, rr(S, 2))), shell(rect(14, 15, 6.5, 4.5, rr(S, 2)))]


@icon("resistance-band", CAT, "A flat looped exercise band drawn as a wide oval ring with an inner edge showing its width.",
      tags=["resistance band", "loop band", "stretch band", "exercise band", "mini band", "physio"],
      aliases=["loop-band"])
def _(S):
    return [shell(rect(2.5, 6.5, 19, 11, pick(S, 3, 5.5))), detail(rect(7, 10.5, 10, 3, pick(S, 0.5, 1.5)))]


@icon("resistance-tube", CAT, "A long curved rubber tube with a grip handle at each end.",
      tags=["resistance tube", "exercise tube", "tube band", "handles", "stretch", "physio"],
      aliases=["exercise-tube"])
def _(S):
    return [line("M6.5 14C6.5 4 17.5 4 17.5 14"),
            shell(rect(2.5, 13.5, 8, 6, rr(S, 2.5))), shell(rect(13.5, 13.5, 8, 6, rr(S, 2.5)))]


# =========================================================================== balls and rollers

@icon("medicine-ball", CAT, "A round ball with curved seam lines and two small grip handles on the sides.",
      tags=["medicine ball", "slam ball", "weighted ball", "wall ball", "core", "strength", "gym"],
      aliases=["slam-ball"])
def _(S):
    return [shell(circle(12, 12, 7.5)), shell(rect(1.5, 9.5, 3, 5, rr(S, 1.25))), shell(rect(19.5, 9.5, 3, 5, rr(S, 1.25))),
            detail("M12 4.5V19.5"), detail("M6.5 7.5Q12 12 6.5 16.5"), detail("M17.5 7.5Q12 12 17.5 16.5")]


@icon("stability-ball", CAT, "A large round exercise ball with a highlight arc resting on the floor line.",
      tags=["stability ball", "exercise ball", "swiss ball", "gym ball", "core", "balance", "pilates"],
      aliases=["swiss-ball"])
def _(S):
    return [shell(circle(12, 10.5, 8.5)), line(arc(12, 10.5, 4.5, 190, 260)), line(seg(2, 21.5, 22, 21.5))]


@icon("balance-trainer", CAT, "Side view of a half dome ball upside down, its flat platform facing up.",
      tags=["balance trainer", "half ball", "dome trainer", "bosu style", "stability", "core", "gym"],
      aliases=["half-ball-trainer"])
def _(S):
    return [shell(rect(2.5, 6.5, 19, 3.5, rr(S, 1.5))), shell("M4.5 10A7.5 7.5 0 0 0 19.5 10Z")]


@icon("balance-board", CAT, "Side view of a flat board resting on a round roller underneath.",
      tags=["balance board", "wobble board", "roller board", "stability", "core", "surfing training"],
      aliases=["wobble-board"])
def _(S):
    return [shell(rect(2.5, 8, 19, 3.5, rr(S, 1.5))), shell(circle(12, 16.5, 4.5))]


@icon("foam-roller", CAT, "Three-quarter view of a cylinder roller with a textured grid on its surface.",
      tags=["foam roller", "muscle roller", "myofascial", "recovery", "massage roller", "stretching"],
      aliases=["muscle-roller"])
def _(S):
    return [shell(ellipse(18, 12, 3, 8)), shell("M18 4H6A3 8 0 0 0 6 20H18"), detail("M9 5.5Q12 12 9 18.5"), detail("M13 4.5V19.5")]

@icon("massage-ball", CAT, "A small round ball covered in short spikes.",
      tags=["massage ball", "spiky ball", "trigger point ball", "lacrosse ball", "recovery", "self massage", "myofascial"],
      aliases=["spiky-massage-ball"])
def _(S):
    spikes = [line(seg(12 + 6.25 * math.cos(math.radians(a)), 12 + 6.25 * math.sin(math.radians(a)),
                       12 + 9.5 * math.cos(math.radians(a)), 12 + 9.5 * math.sin(math.radians(a))))
              for a in range(0, 360, 45)]
    return [shell(circle(12, 12, 5.5))] + spikes


@icon("ab-wheel", CAT, "Front view of a single wheel with a handle bar sticking out on both sides.",
      tags=["ab wheel", "ab roller", "core wheel", "abs", "core", "rollout", "home gym"],
      aliases=["ab-roller"])
def _(S):
    return [shell(rect(8.5, 3, 7, 18, rr(S, 3))), line(seg(8, 12, 16, 12)),
            Part("dot", rect(2, 9.5, 5, 5, rr(S, 1.5))), Part("dot", rect(17, 9.5, 5, 5, rr(S, 1.5)))]


@icon("hula-hoop", CAT, "A large tilted hoop ring seen at a slight angle, drawn as a wide band.",
      tags=["hula hoop", "hoop", "waist hoop", "weighted hoop", "fitness hoop", "core", "play"],
      aliases=["fitness-hoop"])
def _(S):
    return [shell(rot_d(ellipse(12, 12, 10, 6.5), -35)), detail(rot_d(ellipse(12, 12, pick(S, 5.5, 5), pick(S, 2.5, 2.2)), -35))]


@icon("battle-ropes", CAT, "Two thick ropes anchored at one point, lying on the ground in tall wave shapes.",
      tags=["battle ropes", "heavy ropes", "training ropes", "conditioning", "hiit", "crossfit", "gym"],
      aliases=["heavy-ropes"])
def _(S):
    return [line(seg(3, 3, 3, 21)),
            line("M4 7Q7 1.5 10 7T16 7T22 7"), line("M4 17Q7 11.5 10 17T16 17T22 17")]


@icon("plyo-box", CAT, "Three-quarter view of a wooden box with a cut out hand hole on the front face.",
      tags=["plyo box", "jump box", "plyometric box", "box jump", "step up", "crossfit", "gym"],
      aliases=["jump-box"])
def _(S):
    return [shell(rect(3, 9, 13, 12, rr(S, 1.5))), pl(S, [(3, 9), (7.5, 4.5), (21, 4.5), (21, 16.5), (16, 21)]),
            pl(S, [(16, 9), (21, 4.5)]), detail(seg(7.5, 14.5, 11.5, 14.5))]


@icon("agility-ladder", CAT, "Top view of a flat rope ladder lying on the ground in perspective with evenly spaced rungs.",
      tags=["agility ladder", "speed ladder", "footwork", "sports training", "drills", "speed", "coordination"],
      aliases=["speed-ladder"])
def _(S):
    rungs = [line(seg(x1, y, x2, y)) for x1, x2, y in
             [(7.4, 16.6, 4), (6.6, 17.4, 9), (5.4, 18.6, 15), (4.2, 19.8, 21)]]
    return [pl(S, [(7.5, 3), (3, 21.5)]), pl(S, [(16.5, 3), (21, 21.5)])] + rungs


@icon("training-sled", CAT, "Side view of a low weighted sled on runners with two tall push poles.",
      tags=["training sled", "prowler", "push sled", "weight sled", "sprint training", "strength", "conditioning"],
      aliases=["prowler-sled"])
def _(S):
    return [shell(rect(4, 15.5, 15, 3.5, rr(S, 1.5))),
            pl(S, [(2.5, 18.5), (3.5, 21.5), (20, 21.5)]),
            pl(S, [(7, 15.5), (9, 3.5)]), pl(S, [(14, 15.5), (16, 3.5)]),
            line(seg(7.5, 12, 15.5, 12))]


@icon("weighted-vest", CAT, "Front view of a sleeveless vest covered in rectangular weight pockets with a strap across the waist.",
      tags=["weighted vest", "weight vest", "plate carrier", "resistance training", "rucking", "crossfit", "gym"],
      aliases=["weight-vest"])
def _(S):
    pockets = [sq(x, y, 2.75, 2.75) for x in (8.75, 12.5) for y in (11, 15)]
    return [shell(poly([(8, 3), (10, 3), (12, 6), (14, 3), (16, 3), (19.5, 7.5), (17.5, 10), (17.5, 21), (6.5, 21),
                        (6.5, 10), (4.5, 7.5)], closed=True, r=S.r))] + pockets


@icon("ankle-weights", CAT, "A curved padded cuff wrapped in a ring with a velcro strap and small weight pockets.",
      tags=["ankle weights", "wrist weights", "leg weights", "cuff weights", "resistance", "toning", "pilates"],
      aliases=["wrist-weights"])
def _(S):
    cuff = ("M3 9Q12 3 21 9V15Q12 21 3 15Z" if S.name == "line" else
            "M4.5 9.5Q12 4 19.5 9.5Q21 10.5 21 12Q21 13.5 19.5 14.5Q12 20 4.5 14.5Q3 13.5 3 12Q3 10.5 4.5 9.5Z")
    return [shell(cuff), detail(seg(8.5, 6.5, 8.5, 17.5)), detail(seg(15.5, 6.5, 15.5, 17.5))]


@icon("training-sandbag", CAT, "A long cylinder bag with two side handles and a zip.",
      tags=["sandbag", "training sandbag", "strongman bag", "weighted bag", "carry", "conditioning", "gym"],
      aliases=["weight-bag"])
def _(S):
    return [shell(rect(2.5, 8, 19, 11, pick(S, 2, 5))), detail(seg(8, 8, 8, 19)), detail(seg(16, 8, 16, 19)),
            pl(S, [(9.5, 8), (9.5, 4), (14.5, 4), (14.5, 8)])]


@icon("steel-mace", CAT, "A long straight handle with a ball weight at one end, drawn diagonally.",
      tags=["steel mace", "macebell", "gada", "mace", "swing training", "grip", "strength"],
      aliases=["macebell"])
def _(S):
    pommel = Part("dot", rect(2, 19, 3, 3)) if S.name == "line" else dot(3.5, 20.5, 1.6)
    return [solid(circle(16.5, 7.5, 5)), line(seg(13, 11, 3.5, 20.5)), pommel]


@icon("hand-gripper", CAT, "A hand grip strengthener: two handles joined by a coiled spring at the top.",
      tags=["hand gripper", "grip strengthener", "grip trainer", "forearm", "squeeze", "hand exercise", "rehab"],
      aliases=["grip-strengthener"])
def _(S):
    return [shell(circle(12, 6, 3.5)), dot(12, 6, 1),
            shell(rrect(8.2, 15.5, 4, 11, 12, rr(S, 1.5))), shell(rrect(15.8, 15.5, 4, 11, -12, rr(S, 1.5)))]


@icon("climbing-rope", CAT, "A thick braided rope hanging from a ceiling hook, ending in a knot.",
      tags=["climbing rope", "gym rope", "rope climb", "crossfit rope", "braided rope", "grip", "conditioning"],
      aliases=["rope-climb"])
def _(S):
    return [line(seg(4, 2.5, 20, 2.5)), shell(rect(8, 2.5, 8, 15.5, rr(S, 2))),
            detail(poly([(9, 7.5), (12, 10), (15, 7.5)])), detail(poly([(9, 12), (12, 14.5), (15, 12)])),
            dot(12, 20.5, 2)]


@icon("inversion-table", CAT, "Side view of a tilted padded board on an A frame pivot with ankle holders at the high end.",
      tags=["inversion table", "back stretch", "decompression", "spine", "hang upside down", "back pain", "recovery"],
      aliases=["inversion-bench"])
def _(S):
    return [shell(rrect(12, 9.5, 20, 4.5, -30, rr(S, 1.5))), pl(S, [(5.5, 21.5), (12, 11), (18.5, 21.5)]),
            pl(S, [(2.5, 21.5), (21.5, 21.5)]), dot(19, 13.5, 1.5)]


@icon("vibration-plate", CAT, "Three-quarter view of a platform base with wavy vibration lines and a handle column.",
      tags=["vibration plate", "vibration platform", "whole body vibration", "power plate", "recovery", "toning", "gym"],
      aliases=["vibration-platform"])
def _(S):
    return [shell(rect(2.5, 16, 19, 4.5, rr(S, 2))), pl(S, [(18, 16), (18, 4), (13, 4)]),
            line("M4 12Q5.5 9.5 7 12T10 12"), line("M4 7Q5.5 4.5 7 7T10 7")]


@icon("mini-trampoline", CAT, "Three-quarter view of a small round rebounder with short legs and a stretched mat.",
      tags=["mini trampoline", "rebounder", "fitness trampoline", "bounce", "cardio", "low impact", "gym"],
      aliases=["rebounder"])
def _(S):
    return [shell(ellipse(12, 9.5, 9.5, 4.5)), Part("dot", ellipse(12, 9.5, 4.5, 1.2)),
            pl(S, [(4, 12.5), (4, 20.5)]), pl(S, [(20, 12.5), (20, 20.5)]), pl(S, [(12, 14), (12, 21)])]


@icon("step-platform", CAT, "Side view of a low rectangular aerobic step on two raised blocks.",
      tags=["step platform", "aerobic step", "step board", "step aerobics", "cardio", "gym", "riser"],
      aliases=["aerobic-step"])
def _(S):
    return [shell(rect(2.5, 9, 19, 4.5, rr(S, 2))), shell(rect(5, 15, 4, 6, rr(S, 1))), shell(rect(15, 15, 4, 6, rr(S, 1)))]


@icon("pilates-reformer", CAT, "Side view of a long bed frame with a sliding carriage, shoulder blocks and a foot bar.",
      tags=["pilates reformer", "reformer", "pilates machine", "carriage", "studio pilates", "core", "spring resistance"],
      aliases=["reformer"])
def _(S):
    return [shell(rect(2, 15, 20, 4, rr(S, 2))), pl(S, [(4, 19), (4, 21.5)]), pl(S, [(20, 19), (20, 21.5)]),
            shell(rect(6.5, 10, 9, 3, rr(S, 1.5))), dot(3.75, 12, 1),
            pl(S, [(20, 15), (20, 7), (17, 7)])]


@icon("pilates-ring", CAT, "A flexible circle ring with a small padded handle on opposite sides.",
      tags=["pilates ring", "magic circle", "fitness ring", "resistance ring", "inner thigh", "toning", "pilates"])
def _(S):
    return [line(circle(12, 12, 7.5)), shell(rect(3, 8.5, 3, 7, rr(S, 1.5))), shell(rect(18, 8.5, 3, 7, rr(S, 1.5)))]


@icon("ballet-barre", CAT, "Side view of a horizontal rail on two wall brackets with a figure resting one leg on it.",
      tags=["ballet barre", "barre", "dance rail", "stretch rail", "ballet", "dance studio", "barre workout"],
      aliases=["dance-barre"])
def _(S):
    return [line(seg(2.5, 12.5, 10.5, 12.5)), pl(S, [(4, 12.5), (4, 17)]),
            hd(17, 4.5), line(seg(17, 9, 17, 14.5)), pl(S, [(17, 14.5), (17, 21.5)]),
            pl(S, [(17, 14.5), (10.5, 12.5)]), pl(S, [(17, 10), (21.5, 6.5)])]


# =========================================================================== boxing and gym accessories

@icon("punching-bag", CAT, "A tall cylinder heavy bag hanging from chains that meet at a hook.",
      tags=["punching bag", "heavy bag", "boxing bag", "kickboxing", "mma", "boxing gym", "training"],
      aliases=["heavy-bag"])
def _(S):
    return [pl(S, [(8, 6.5), (12, 2.5), (16, 6.5)]), shell(rect(6.5, 6.5, 11, 15, rr(S, 3))),
            detail(seg(6.5, 10, 17.5, 10)), detail(seg(6.5, 18, 17.5, 18))]


@icon("speed-bag", CAT, "A small teardrop bag hanging under a round horizontal platform.",
      tags=["speed bag", "speed ball", "boxing", "reflex bag", "hand speed", "boxing gym", "training"],
      aliases=["speed-ball"])
def _(S):
    return [shell(rect(3, 2.5, 18, 3.5, rr(S, 1.5))), line(seg(12, 6, 12, 9)),
            shell("M10.5 9.5H13.5L17 14A5.5 5.5 0 1 1 7 14Z")]


@icon("focus-mitts", CAT, "A pair of padded mitts shaped like round targets with a centre circle.",
      tags=["focus mitts", "boxing pads", "punch mitts", "hand pads", "boxing coach", "sparring", "training"],
      aliases=["boxing-pads"])
def _(S):
    return [shell(rect(2.5, 4.5, 8, 15, rr(S, 4))), shell(rect(13.5, 4.5, 8, 15, rr(S, 4))),
            dot(6.5, 12, 1.8), dot(17.5, 12, 1.8)]


@icon("lifting-belt", CAT, "A wide weightlifting belt with a buckle and holes along one end.",
      tags=["lifting belt", "weight belt", "powerlifting belt", "back support", "squat belt", "strength", "gym"],
      aliases=["weightlifting-belt"])
def _(S):
    return [shell(rect(2.5, 7.5, 18, 9, rr(S, 3))), shell(rect(13.5, 5.5, 6, 13, rr(S, 2))),
            dot(5.5, 12, 1.1), dot(8.5, 12, 1.1)]


@icon("workout-gloves", CAT, "Back view of a fingerless padded glove with a wrist strap.",
      tags=["workout gloves", "gym gloves", "lifting gloves", "fingerless gloves", "grip", "weights", "training"],
      aliases=["gym-gloves"])
def _(S):
    return [shell(rect(7, 3.5, 11.5, 17.5, rr(S, 3))), detail(seg(10.75, 3.5, 10.75, 9)), detail(seg(14.5, 3.5, 14.5, 9)),
            pl(S, [(7, 15.5), (3.5, 12.5), (3.5, 8.5)]), detail(seg(7, 16.5, 18.5, 16.5))]


@icon("sweatband", CAT, "A thick terry wristband ring seen at an angle, with ribbed texture lines.",
      tags=["sweatband", "wristband", "headband", "terry band", "sweat", "tennis", "gym"],
      aliases=["wrist-sweatband"])
def _(S):
    return [shell(ellipse(17, 12, 3, 6)), shell("M17 6H8A3 6 0 0 0 8 18H17"), detail(seg(8, 9, 14, 9)), detail(seg(8, 12, 14, 12)),
            detail(seg(8, 15, 14, 15))]


@icon("kinesiology-tape", CAT, "A shoulder outline with two strips of stretchy tape applied in a Y shape.",
      tags=["kinesiology tape", "kt tape", "sports tape", "muscle tape", "physio tape", "recovery", "injury support"],
      aliases=["kt-tape"])
def _(S):
    return [pl(S, [(2.5, 21.5), (2.5, 14.5), (4, 12), (9, 10)]), pl(S, [(21.5, 21.5), (21.5, 14.5), (20, 12), (15, 10)]),
            pl(S, [(9, 10), (9, 6), (15, 6), (15, 10)]),
            line(seg(12, 21.5, 12, 16.5)), line(seg(12, 16.5, 7.5, 13)), line(seg(12, 16.5, 16.5, 13))]


@icon("gym-locker", CAT, "Front view of two tall narrow metal lockers side by side with vent slots at the top and handles.",
      tags=["gym locker", "locker room", "locker", "changing room", "storage", "fitness club", "lockers"],
      aliases=["locker-room"])
def _(S):
    return [shell(rect(3, 2.5, 18, 19, rr(S, 2))), detail(seg(12, 2.5, 12, 21.5)),
            detail(seg(5.5, 6.5, 9.5, 6.5)), detail(seg(14.5, 6.5, 18.5, 6.5)),
            dot(9.5, 14, 1.1), dot(14.5, 14, 1.1)]


# =========================================================================== tracking and measuring

@icon("chest-strap-monitor", CAT, "A torso outline with a band across the chest and a small oval sensor in the middle.",
      tags=["heart rate strap", "chest strap", "heart rate monitor", "hrm", "fitness tracker", "cardio", "sensor"],
      aliases=["heart-rate-strap"])
def _(S):
    return [shell(poly([(8, 2.5), (16, 2.5), (21, 6), (21, 21.5), (3, 21.5), (3, 6)], closed=True, r=S.r)),
            detail(seg(3, 11.5, 21, 11.5)), Part("dot", ellipse(12, 11.5, 3.5, 2.5))]


@icon("pedometer", CAT, "A small clip-on device with a rectangular display and a footprint mark.",
      tags=["pedometer", "step counter", "step tracker", "walking", "steps", "fitness tracker", "activity tracker"],
      aliases=["step-counter"])
def _(S):
    return [shell(rect(5, 2.5, 14, 19, rr(S, 4))), detail(rect(8.5, 6, 7, 4)),
            Part("dot", ellipse(12, 14.5, 2, 1.6)), dot(12, 18, 1.1)]


@icon("skinfold-caliper", CAT, "A pinch caliper with two jaws and a round dial on the handle.",
      tags=["skinfold caliper", "body fat caliper", "body fat", "pinch test", "measurement", "composition", "fitness assessment"],
      aliases=["body-fat-caliper"])
def _(S):
    return [shell(circle(9.5, 8.5, 5.5)), detail(seg(9.5, 8.5, 12, 6)),
            pl(S, [(8, 14), (7, 21.5)]), pl(S, [(13, 13), (19, 15.5), (19, 21.5)])]


@icon("waist-measurement", CAT, "A torso outline with a measuring tape wrapped around the waist.",
      tags=["waist measurement", "tape measure", "waistline", "body measurement", "circumference", "weight loss", "progress"],
      aliases=["waist-tape"])
def _(S):
    return [shell(poly([(8, 2.5), (16, 2.5), (17.5, 8), (16, 13), (17.5, 21.5), (6.5, 21.5), (8, 13), (6.5, 8)],
                       closed=True, r=S.r)),
            detail(ellipse(12, 13, 8.5, 2.5))]


@icon("workout-plan", CAT, "A clipboard with a small dumbbell at the top and checklist lines below.",
      tags=["workout plan", "training plan", "exercise routine", "fitness program", "workout log", "checklist", "routine"],
      aliases=["workout-log"])
def _(S):
    return [shell(rect(3, 4, 18, 18, rr(S, 3))), shell(rect(8.5, 2.5, 7, 3.5, rr(S, 1.5))),
            line(seg(9, 10.5, 15, 10.5)), sq(6.2, 8.8, 1.8, 3.4), sq(16, 8.8, 1.8, 3.4),
            detail(seg(7, 15, 17, 15)), detail(seg(7, 18.5, 13, 18.5))]


@icon("personal-trainer", CAT, "A person holding a clipboard with a whistle on a cord around the neck.",
      tags=["personal trainer", "fitness coach", "gym coach", "instructor", "whistle", "clipboard", "trainer"],
      aliases=["fitness-coach"])
def _(S):
    return [hd(8, 4.5), line(seg(8, 8.5, 8, 15)), pl(S, [(5, 21.5), (8, 15), (11, 21.5)]),
            pl(S, [(8, 10.5), (13, 12.5)]), shell(rect(13, 8, 8, 11, rr(S, 1.5))),
            detail(seg(15.5, 12, 18.5, 12)), detail(seg(15.5, 15, 18.5, 15))]


@icon("fitness-class", CAT, "An instructor with both arms raised in front of two smaller figures behind, as in a group exercise class.",
      tags=["fitness class", "group exercise", "aerobics class", "workout class", "group fitness", "gym class", "instructor"],
      aliases=["group-fitness"])
def _(S):
    back = []
    for x in (4.5, 19.5):
        back += [dot(x, 8.5, 1.75), pl(S, [(x - 3, 17), (x, 12.5), (x + 3, 17)])]
    return back + [hd(12, 5.5), pl(S, [(7.5, 3.5), (12, 10), (16.5, 3.5)]), line(seg(12, 10, 12, 15)),
                   pl(S, [(8.5, 21.5), (12, 15), (15.5, 21.5)])]


@icon("tens-unit", CAT, "A small handheld device with a screen and two wires ending in square electrode pads.",
      tags=["tens unit", "tens machine", "nerve stimulation", "electrode pads", "pain relief", "physio", "electrotherapy"],
      aliases=["electrode-pads"])
def _(S):
    return [shell(rect(2.5, 4, 8, 15, rr(S, 2))), sq(4.5, 6.5, 4, 3), dot(6.5, 14, 1.1),
            line("M10.5 8Q13 8 14 5.5"), line("M10.5 15Q13 15 14 17.5"),
            shell(rect(14.5, 2.5, 7, 5, rr(S, 1.5))), shell(rect(14.5, 16.5, 7, 5, rr(S, 1.5)))]


@icon("compression-boots", CAT, "Side view of a tall inflatable leg sleeve with horizontal chamber bands and a hose.",
      tags=["compression boots", "recovery boots", "leg compression", "air compression", "pneumatic", "recovery", "circulation"],
      aliases=["recovery-boots"])
def _(S):
    return [shell(poly([(6, 2.5), (15, 2.5), (15, 15), (21, 17), (21, 21.5), (6, 21.5)], closed=True, r=S.r)),
            detail(seg(6, 7, 15, 7)), detail(seg(6, 11.5, 15, 11.5)), detail(seg(6, 16, 15, 16)),
            line("M15 5Q19.5 5 19.5 10")]


# =========================================================================== training figures

@icon("push-up", CAT, "Side view figure in a straight body plank with arms extended, lowering toward the floor.",
      tags=["push-up", "pushup", "press up", "chest", "bodyweight", "calisthenics", "exercise"],
      aliases=["press-up"])
def _(S):
    return [hd(20, 7), line(seg(17.5, 11, 3.5, 19.5)), line(seg(17, 11.5, 17.5, 21)), line(seg(2, 21.5, 22, 21.5))]


@icon("sit-up", CAT, "Side view figure lying with knees bent, torso curling up and hands behind the head.",
      tags=["sit-up", "situp", "crunch", "abs", "core", "bodyweight", "exercise"],
      aliases=["crunches"])
def _(S):
    return [hd(7, 5.5), line(seg(11, 19, 7.5, 10.5)), pl(S, [(11, 19), (16.5, 12.5), (20, 19)]),
            pl(S, [(7.5, 11), (3.5, 8)]), line(seg(2, 21.5, 22, 21.5))]


@icon("plank-exercise", CAT, "Side view figure holding a straight body on forearms and toes.",
      tags=["plank", "forearm plank", "core hold", "isometric", "abs", "bodyweight", "exercise"],
      aliases=["plank"])
def _(S):
    return [hd(19.5, 9.5), line(seg(15.5, 14.5, 3.5, 19.5)), pl(S, [(15.5, 14.5), (15.5, 20), (21, 20)]),
            line(seg(2, 21.5, 22, 21.5))]


@icon("side-plank", CAT, "Front view figure balanced on one forearm with the body in a straight diagonal and the other arm raised.",
      tags=["side plank", "oblique", "core hold", "balance", "abs", "bodyweight", "exercise"],
      aliases=["side-plank-pose"])
def _(S):
    return [hd(4.5, 9), line(seg(8, 13, 20.5, 20.5)), pl(S, [(8, 13), (8, 20), (3.5, 20)]),
            line(seg(9.5, 12, 11, 3.5)), line(seg(2, 21.5, 22, 21.5))]
