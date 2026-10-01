"""TypeIcon Core: family (batch family_001).

Pregnancy, birth, nursing, baby feeding, nappies, bathing, baby clothes, baby health, child safety and nursery
furniture, drawn as simple symbols from the objects themselves.
"""
import math

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar, rotation  # noqa: F401

CAT = "family"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def tf(d, m):
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def mv(d, dx, dy):
    return tf(d, (1, 0, 0, 1, dx, dy))


def sc(d, s, ox=0.0, oy=0.0):
    return tf(d, (s, 0, 0, s, ox, oy))


def rot(d, deg, cx=12.0, cy=12.0):
    return tf(d, rotation(deg, cx, cy))


def flip(d):
    return tf(d, (-1, 0, 0, 1, 24, 0))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def bump_torso(S):
    """Torso from the side, facing right: flat back at x 6, chest, then a round pregnant bump."""
    return L(S,
             "M6 2.5H11.5C11.5 6 13 7.7 16 9.5C19.5 11.5 19.5 17 17 19.5C15.5 21 12 21 6 21Z",
             "M8 2.5H11.5C11.5 6 13 7.7 16 9.5C19.5 11.5 19.5 17 17 19.5C15.5 21 12 21 8 21Q6 21 6 19V4.5Q6 2.5 8 2.5Z")


def preg_figure(S, dx=0.0, k=1.0, dy=0.0):
    """Standing pregnant figure in side profile (head, torso with bump)."""
    body = L(S,
             "M8.5 8.5H11.8C12.8 8.5 13.5 9.2 13.7 10C16.8 10.8 18.5 12.8 18.5 15C18.5 17 16.8 18.3 14.5 18.3H13.5V21H8C8 17 7.4 13.3 7.4 10.5C7.4 9.4 7.7 8.5 8.5 8.5Z",
             "M8.5 8.5H11.8C12.8 8.5 13.5 9.2 13.7 10C16.8 10.8 18.5 12.8 18.5 15C18.5 17 16.8 18.3 14.5 18.3H13.5V20Q13.5 21 12.5 21H9Q8 21 8 20C8 16.5 7.4 13.3 7.4 10.5C7.4 9.4 7.7 8.5 8.5 8.5Z")
    def m(d):
        return sc(d, k, dx + (1 - k) * 12, dy + (1 - k) * 12)
    return [shell(m(circle(10.5, 4.5, 2.5))), shell(m(body)),
            detail(m(poly([(10, 10.5), (10.4, 14.8), (13.8, 15.2)], r=S.r)))]


def mark(d):
    return Part("dot", d)


def bottle_d(S, x, y, w, h):
    """Baby bottle silhouette (body, collar, nipple) with its top-left corner at x, y."""
    cw = w * 0.5
    body = rect(x, y + h * 0.3, w, h * 0.7, rr(S, 2))
    nip = poly([(x + w / 2 - cw / 2, y + h * 0.3), (x + w / 2 - cw / 2, y + h * 0.12), (x + w / 2, y), (x + w / 2 + cw / 2, y + h * 0.12),
                (x + w / 2 + cw / 2, y + h * 0.3)], closed=True, r=S.r * 0.5)
    return union(body, nip)


def heart_d(cx, cy, s=1.0):
    return sc("M0 3.2C-3.2 0.6 -3.4 -2.4 -1.6 -3.2C-0.6 -3.6 0 -2.8 0 -2.2C0 -2.8 0.6 -3.6 1.6 -3.2C3.4 -2.4 3.2 0.6 0 3.2Z", s, cx, cy)


# ============================================================================ pregnancy and birth

@icon("maternity-dress", CAT, "A sleeveless V-neck dress with a seam under the chest and a rounded bump curve on the skirt",
      tags=["pregnancy dress", "maternity wear", "expecting", "baby bump", "clothing", "empire waist", "gown"])
def _(S):
    d = poly([(8, 2.5), (12, 6), (16, 2.5), (16, 8.5), (19.5, 21), (4.5, 21), (8, 8.5)], closed=True, r=S.r)
    return [shell(d), detail(seg(8, 8.5, 16, 8.5)), detail(L(S, "M9 12.5C9.5 17.5 14.5 17.5 15 12.5", "M9 12.5C9.5 17.5 14.5 17.5 15 12.5"))]


@icon("maternity-jeans", CAT, "Jeans with a tall ribbed stretch panel at the top in place of a waistband",
      tags=["pregnancy trousers", "maternity pants", "denim", "stretch panel", "expecting", "clothing", "bump"])
def _(S):
    d = poly([(6, 2.5), (18, 2.5), (19, 21), (13.5, 21), (12, 14.5), (10.5, 21), (5, 21)], closed=True, r=S.r)
    return [shell(d), detail(seg(6.2, 7, 17.8, 7)), detail(seg(12, 7, 12, 14.5))]


@icon("maternity-support-belt", CAT, "A pregnant figure in profile with a wide support band across the underside of the bump and a fastening tab at the back",
      tags=["belly band", "pregnancy support", "back support", "maternity belt", "bump support", "brace", "pelvic"])
def _(S):
    f = preg_figure(S, 0)
    body = P(f[1].d)
    tab = rect(4, 13, 4, 3.5, rr(S, 1.5))
    return [f[0], shell(union(f[1].d, tab)), detail(seg(7.4, 14.8, 18.6, 14.8))]


@icon("prenatal-vitamins", CAT, "A pill bottle with a person on the label, beside a capsule and a round tablet",
      tags=["pregnancy supplements", "folic acid", "pills", "maternity vitamins", "prenatal", "capsules", "medicine"])
def _(S):
    cap = rect(3.5, 2.5, 7, 3, rr(S, 1.2))
    body = rect(2.5, 5.5, 9, 15.5, rr(S, 2))
    caps = rot(rect(14.5, 12.3, 6, 9.4, 3), 45, 17.5, 17)
    return [shell(union(cap, body)), mark(heart_d(7, 14.2, 1.7)),
            shell(caps), shell(circle(17, 6.5, 2.8))]


@icon("morning-sickness", CAT, "A pregnant figure in profile with a queasy swirl beside the head",
      tags=["nausea", "pregnancy symptom", "queasy", "sick", "vomiting", "expecting", "first trimester"])
def _(S):
    return preg_figure(S, -2.5) + [line("M16.5 8.5C14.7 8.2 14.5 4.7 17.7 4.5C21.5 4.3 21.5 8.8 18.8 8.8C17.2 8.8 16.9 7 18 6.3")]


@icon("baby-kick", CAT, "A pregnant figure in profile with a small foot pressing out of the bump and two motion marks",
      tags=["fetal movement", "kicking", "pregnancy", "quickening", "bump", "unborn baby", "movement"])
def _(S):
    f = preg_figure(S, -3)
    foot = ellipse(17.3, 13.8, 2.3, 1.6)
    return [f[0], shell(union(f[1].d, foot)), f[2], line(seg(20.5, 11, 22, 10)), line(seg(20.5, 17, 22, 18))]


@icon("birth-plan", CAT, "A clipboard with a round clip on top and three ticked lines",
      tags=["labour plan", "labor plan", "delivery plan", "checklist", "childbirth", "midwife", "preferences"])
def _(S):
    board = rect(4.5, 4.5, 15, 17, rr(S, 2.5))
    clip = circle(12, 4.5, 2.5)
    out = [shell(union(board, clip))]
    for y in (10, 14, 18):
        out.append(detail(poly([(7.3, y), (8.4, y + 1.1), (10.3, y - 1.2)], r=S.r * 0.4)))
        out.append(detail(seg(12.5, y, 17, y)))
    return out


@icon("hospital-go-bag", CAT, "A zipped holdall with a carry handle and a small tag hanging from the base",
      tags=["hospital bag", "overnight bag", "maternity bag", "packed bag", "labour bag", "duffel", "ready to go"])
def _(S):
    bag = rect(2.5, 8, 19, 8.5, rr(S, 3))
    handle = poly([(7.5, 8), (7.5, 4.5), (16.5, 4.5), (16.5, 8)], r=S.r)
    return [shell(bag), line(handle), detail(seg(2.5, 11.5, 21.5, 11.5)), line(seg(16.5, 16.5, 16.5, 18)), solid(circle(16.5, 19.8, 2))]


@icon("contraction-timer", CAT, "A stopwatch with a single rising and falling peak across the dial",
      tags=["contractions", "labour timer", "labor", "stopwatch", "timing", "childbirth", "waves"])
def _(S):
    return [shell(circle(12, 14, 8)), line(seg(12, 6, 12, 3)), line(seg(9.5, 3, 14.5, 3)),
            detail(poly([(6.5, 16.5), (9, 16.5), (12, 10.5), (15, 16.5), (17.5, 16.5)], r=S.r))]


@icon("doula", CAT, "A standing helper with a hand on the back of a pregnant figure beside them",
      tags=["birth support", "birth partner", "midwife", "labour coach", "pregnancy support", "carer", "helper"])
def _(S):
    f = preg_figure(S, 3.5)
    return [shell(circle(5.5, 4.5, 2.5)), shell(rect(2.5, 8.5, 6, 12.5, rr(S, 3))), f[0], f[1], f[2],
            line(seg(8.5, 13, 10.9, 13))]


@icon("gender-reveal-balloon", CAT, "A balloon with a question mark, with confetti dots flying around it",
      tags=["reveal party", "boy or girl", "surprise", "baby gender", "pop", "confetti", "celebration"])
def _(S):
    ball = L(S, "M12 2.5C16 2.5 18.5 5.5 18.5 9C18.5 12.5 15.5 15.5 12 17C8.5 15.5 5.5 12.5 5.5 9C5.5 5.5 8 2.5 12 2.5Z",
            ellipse(12, 9.5, 6.5, 7))
    return [shell(ball), detail("M10.3 8C10.3 5.8 13.7 5.8 13.7 8C13.7 9.6 12 9.6 12 11.2"), dot(12, 13.2, 0.9),
            solid("M12 17.5L10.6 19.6H13.4Z"), line("M12 19.6C13.4 20.4 10.6 21 12 22"),
            dot(3, 3.5, 1.2), dot(21, 3.5, 1.2), dot(2.8, 14, 1.1), dot(21.2, 14, 1.1)]


@icon("baby-shower", CAT, "A wrapped gift with a bow beside a baby bottle",
      tags=["gift", "present", "party", "new baby", "celebration", "expecting", "shower"])
def _(S):
    gift = rect(2.5, 11, 10, 10, rr(S, 2))
    return [shell(gift), detail(seg(7.5, 11, 7.5, 21)), line(poly([(7.5, 11), (4.5, 8.2), (6, 7), (7.5, 11), (9, 7), (10.5, 8.2), (7.5, 11)], r=S.r * 0.3)),
            shell(bottle_d(S, 15.5, 8, 5.5, 13)), detail(seg(15.5, 13.5, 21, 13.5))]


@icon("birth-announcement-card", CAT, "A folded greeting card with two tiny footprints and a heart on the front",
      tags=["new baby card", "greeting card", "birth notice", "it's a baby", "newborn", "congratulations", "stationery"])
def _(S):
    foot1 = rot(ellipse(12.5, 11, 1.2, 1.8), -10, 12.5, 11)
    foot2 = rot(ellipse(16.2, 9.5, 1.2, 1.8), 10, 16.2, 9.5)
    return [shell(rect(4.5, 2.5, 15, 19, rr(S, 3))), detail(seg(8.5, 2.5, 8.5, 21.5)),
            mark(foot1), mark(foot2), mark(circle(12.3, 7.9, 0.75)), mark(circle(16.4, 6.4, 0.75)), mark(heart_d(14, 17, 1.0))]


@icon("breech-baby", CAT, "A womb outline holding a curled baby with its head up and bottom down",
      tags=["breech", "fetal position", "pregnancy", "birth position", "ultrasound", "womb", "unborn baby"])
def _(S):
    womb = L(S, "M12 2.5C16.5 2.5 20 6 20 10.5C20 15 16 19 12 21.5C8 19 4 15 4 10.5C4 6 7.5 2.5 12 2.5Z", ellipse(12, 12, 8, 9.5))
    return [shell(womb), mark(circle(12, 8, 2)), detail("M10.2 11.5C7.8 14 9 18 12.3 18C14.8 18 16 16 15.3 13.8")]


@icon("belly-cast", CAT, "A plaster cast of a pregnant torso seen from the front, with a rough torn edge at the neck and hips",
      tags=["bump cast", "plaster", "pregnancy keepsake", "belly mould", "maternity art", "torso cast", "memento"])
def _(S):
    d = ("M8 3L10 4.5L12 3L14 4.5L16 3C18 4 19.5 5.5 19.5 8C19.5 10.5 19 11.5 19 14C19 17 19 18 18.5 21L16.5 19.5L14.5 21"
         "L12.5 19.5L10.5 21L8.5 19.5L6.5 21L5.5 19.5C5 18 5 17 5 14C5 11.5 4.5 10.5 4.5 8C4.5 5.5 6 4 8 3Z")
    return [shell(d, stroke_miterlimit="2"), detail(circle(12, 14, 3.4))]


@icon("bump-heart-hands", CAT, "A pregnant figure in profile with a heart drawn on the bump",
      tags=["baby bump", "love", "expecting", "pregnancy", "maternity", "motherhood", "heart"])
def _(S):
    f = preg_figure(S, -0.5)
    return [f[0], f[1], detail(heart_d(13.2, 14.4, 1.35))]


@icon("prenatal-yoga", CAT, "A pregnant figure sitting cross-legged with hands resting on the knees",
      tags=["pregnancy yoga", "meditation", "exercise", "expecting", "stretching", "relaxation", "maternity fitness"])
def _(S):
    torso = union(rect(9.3, 7, 5.4, 4, 1), ellipse(12, 12.6, 4.9, 4.4))
    legs = poly([(3, 20.5), (5.5, 16.8), (10, 15.8), (14, 15.8), (18.5, 16.8), (21, 20.5)], closed=True, r=S.r)
    return [shell(circle(12, 4.2, 2.3)), shell(union(torso, legs)), line(poly([(8, 9), (5.2, 13.5), (5.5, 16.5)], r=S.r)),
            line(poly([(16, 9), (18.8, 13.5), (18.5, 16.5)], r=S.r))]


@icon("pregnancy-cravings", CAT, "A pickle and an ice cream cone leaning together",
      tags=["pickles and ice cream", "food cravings", "expecting", "snack", "midnight snack", "hungry", "pregnancy food"])
def _(S):
    pickle = rot(rect(4.2, 6, 5, 14.5, 2.5), -12, 6.7, 13)
    cone = rot(poly([(12.8, 11.5), (20.2, 11.5), (16.5, 21.5)], closed=True, r=S.r * 0.6), 8, 16.5, 14)
    return [shell(pickle), mark(circle(5.8, 10, 0.8)), mark(circle(7.6, 13.5, 0.8)), mark(circle(6.4, 16.8, 0.8)),
            shell(circle(16.7, 7.8, 4)), shell(cone)]


@icon("pregnancy-alcohol-warning", CAT, "A prohibition circle with a slash, a pregnant figure at the lower left and a wine glass at the upper right",
      tags=["no alcohol", "drinking warning", "fetal alcohol", "label", "avoid", "expecting", "health warning"])
def _(S):
    body = poly([(6.6, 12.3), (9, 12.3), (12.2, 15), (12.2, 17.2), (10.2, 17.4), (10.2, 19.8), (6.6, 19.8)], closed=True, r=S.r * 1.3)
    return [shell(circle(12, 12, 9.5)), mark(circle(7.6, 10, 1.5)), mark(body),
            mark(poly([(14.4, 5.5), (19.2, 5.5), (18.6, 9.5), (16.8, 11), (15, 9.5)], closed=True, r=S.r * 0.7)), mark(rect(16.2, 10.5, 1.3, 4.5, 0)),
            mark(rect(14.3, 14.6, 5.1, 1.2, 0)), detail(seg(5.3, 5.3, 18.7, 18.7))]


@icon("home-birth", CAT, "A house with a pitched roof and a swaddled newborn in the doorway",
      tags=["birth at home", "midwife", "homebirth", "newborn", "labour", "labor", "birthing"])
def _(S):
    body = rect(5.5, 10, 13, 11, rr(S, 2))
    roof = poly([(2.5, 11.5), (12, 3), (21.5, 11.5)], r=S.r)
    return [line(roof), shell(body), mark(circle(12, 13.8, 1.7)), mark(rect(10, 16, 4, 4, 1.8))]


@icon("ovulation-test", CAT, "A test stick with two result lines and a round egg cell on the handle",
      tags=["fertility test", "ovulation predictor", "trying to conceive", "lh test", "conception", "test strip", "fertile"])
def _(S):
    return [shell(rect(2, 7, 20, 10, rr(S, 3))), detail(seg(6, 9.5, 6, 14.5)), detail(seg(10, 9.5, 10, 14.5)),
            detail(seg(14, 7, 14, 17)), mark(circle(18.2, 12, 2.2))]


@icon("fetal-heartbeat", CAT, "A pregnant figure with a small heart in the bump and a pulse line running out of it",
      tags=["baby heartbeat", "doppler", "ultrasound", "heart rate", "pregnancy scan", "prenatal", "monitor"])
def _(S):
    f = preg_figure(S, -3.5)
    return [f[0], f[1], mark(heart_d(9.6, 14.2, 1.1)),
            line(poly([(15.8, 14.4), (17.4, 14.4), (18.4, 11.5), (19.8, 17), (20.8, 14.4), (22, 14.4)], r=S.r * 0.3))]


@icon("pregnancy-seatbelt", CAT, "A seated pregnant figure in a car seat with the lap belt low under the bump and the strap beside it",
      tags=["car safety", "seat belt", "driving while pregnant", "travel", "expecting", "road safety", "maternity"])
def _(S):
    body = ("M6.5 7.5H10C11 7.5 11.6 8.2 11.8 9C15 9.7 16.5 11.5 16.5 13.5C16.5 15 16 15.8 15 16H19.5Q21.5 16 21.5 18V22H18.5V19H6.5Z")
    return [shell(circle(8.8, 4, 2.3)), shell(body), line(seg(3.5, 5.5, 3.5, 19.5)),
            detail(poly([(8.3, 7.5), (11.6, 11.5), (11.6, 16.5)], r=S.r * 0.5)), detail(seg(11.6, 16.5, 18, 16.5))]


@icon("waters-breaking", CAT, "A pregnant figure in profile with three drops falling beside the legs",
      tags=["water broke", "labour starting", "labor", "amniotic fluid", "contractions", "birth", "drops"])
def _(S):
    f = preg_figure(S, -3.5)
    drop = "M0 -2.2L1.5 0.6A1.6 1.6 0 0 1 -1.5 0.6Z"
    return [f[0], f[1], f[2], solid(mv(drop, 12.8, 19.2)), solid(mv(drop, 17, 20)), solid(mv(drop, 19.2, 15.2))]


@icon("peri-bottle", CAT, "A squeeze bottle with a long bent spout and drops of water leaving the tip",
      tags=["postpartum", "perineal care", "squirt bottle", "recovery", "wash bottle", "after birth", "rinse"])
def _(S):
    body = poly([(5.5, 10.5), (13.5, 10.5), (14, 21), (5, 21)], closed=True, r=S.r * 1.5)
    neck = rect(7.5, 7, 4, 3.5, 0)
    return [shell(union(body, neck)), line(poly([(9.5, 7), (9.5, 4.5), (16, 3)], r=S.r)), solid(circle(18.3, 6, 1.1)),
            solid(circle(19.3, 10.2, 1.1)), solid(circle(18.6, 14.4, 1.1))]


@icon("nursing-bra", CAT, "A bra with the right cup unclipped and folded down along a flap line, with a clip on the strap",
      tags=["breastfeeding bra", "maternity bra", "feeding bra", "drop-down cup", "lactation", "underwear", "clip"])
def _(S):
    cup = L(S, "M2.5 10.5H11.5C11.5 15.5 9.2 18.5 7 18.5C4.8 18.5 2.5 15.5 2.5 10.5Z",
            "M4.5 10.5H11.5C11.5 15.5 9.2 18.5 7 18.5C4.8 18.5 2.5 15.5 2.5 12.5C2.5 11.4 3.2 10.5 4.5 10.5Z")
    return [shell(cup), shell(flip(cup)), line(seg(4.8, 10.5, 4.8, 3)), line(seg(19.2, 10.5, 19.2, 3)),
            detail(seg(12.5, 13.5, 21.5, 13.5)), mark(rect(17.9, 6.8, 2.6, 2.8, 0.6))]




# ============================================================================ nursing and feeding

def grow(d, g):
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def spark(cx, cy, r):
    pts = [(0, -1), (0.28, -0.28), (1, 0), (0.28, 0.28), (0, 1), (-0.28, 0.28), (-1, 0), (-0.28, -0.28)]
    return poly([(cx + x * r, cy + y * r) for x, y in pts], closed=True)


@icon("nipple-shield", CAT, "A side view of a thin shield with a raised teat in the middle of a wide flat brim",
      tags=["breastfeeding aid", "latch", "silicone", "nursing", "feeding", "lactation", "newborn"])
def _(S):
    d = poly([(2.5, 18.5), (8.5, 16.5), (9.3, 8.5), (12, 5), (14.7, 8.5), (15.5, 16.5), (21.5, 18.5)], closed=True, r=S.r * 0.8)
    return [shell(d), mark(circle(12, 11, 0.9))]


@icon("nursing-pads", CAT, "Two round breast pads overlapping slightly, the front one with a stitched ring",
      tags=["breast pads", "leak protection", "lactation", "postpartum", "maternity", "absorbent", "feeding"])
def _(S):
    a = circle(8.5, 14.5, 6.5)
    b = minus(circle(15.5, 9.5, 6.5), grow(a, 2.5))
    return [shell(a), shell(b), detail(circle(8.5, 14.5, 3.2))]


@icon("breast-milk-cooler-bag", CAT, "An insulated cooler bag with two milk bottles standing in the top and a snowflake on the front",
      tags=["milk storage", "pumped milk", "insulated bag", "travel", "expressing", "cold", "bottles"])
def _(S):
    body = rect(2.5, 10, 19, 11, rr(S, 3))
    b1 = bottle_d(S, 6, 3, 4, 8)
    b2 = bottle_d(S, 14, 3, 4, 8)
    return [shell(union(body, b1, b2)), detail(seg(2.5, 13, 21.5, 13)), detail(seg(12, 14.8, 12, 19.6)),
            detail(seg(9.9, 16, 14.1, 18.4)), detail(seg(9.9, 18.4, 14.1, 16))]


@icon("feeding-timer", CAT, "A baby bottle with a small clock face overlapping its lower corner",
      tags=["feed tracker", "nursing timer", "bottle time", "schedule", "newborn", "logging feeds", "clock"])
def _(S):
    clock = circle(16.5, 16.5, 5)
    bottle = minus(bottle_d(S, 3, 2.5, 9, 18.5), grow(clock, 1.8))
    return [shell(bottle), shell(clock), detail(poly([(16.5, 13.8), (16.5, 16.5), (18.5, 17.6)], r=S.r * 0.4))]


@icon("night-feeding", CAT, "A baby bottle beside a crescent moon and two small stars",
      tags=["night feed", "midnight", "bedtime bottle", "newborn", "sleep", "nighttime", "3am feed"])
def _(S):
    moon = minus(circle(16, 7.5, 5.5), circle(18.8, 6, 4.6))
    return [shell(bottle_d(S, 3, 2.5, 8, 18.5)), shell(moon), solid(spark(19, 17, 2.4)), solid(spark(14.3, 19.2, 1.5))]


@icon("nursery-glider", CAT, "A padded armchair seen from the side on curved glider runners, with a small footstool in front",
      tags=["rocking chair", "nursing chair", "nursery furniture", "armchair", "feeding chair", "rocker", "baby room"])
def _(S):
    chair = poly([(5, 3), (9, 3), (9.8, 11), (16.5, 11), (16.5, 15), (5, 15)], closed=True, r=S.r)
    return [shell(chair), line(seg(7.5, 15, 7.5, 19.8)), line(seg(14, 15, 14, 20)), line("M2.5 18.5C8 22.3 16 22.3 21.5 18.5"),
            shell(rect(18.5, 14.5, 3.5, 3, rr(S, 1)))]


@icon("formula-scoop", CAT, "A round measuring scoop with a short handle, heaped with powder",
      tags=["baby formula", "powder milk", "measuring scoop", "infant feeding", "milk powder", "bottle prep", "heaped"])
def _(S):
    bowl = L(S, "M3.5 13H16.5C16.5 17.5 13 20 10 20C7 20 3.5 17.5 3.5 13Z", "M3.5 13H16.5C16.5 17.5 13 20 10 20C7 20 3.5 17.5 3.5 13Z")
    mound = "M5 13C5 9.5 7.5 8 10 8C12.5 8 15 9.5 15 13Z"
    return [shell(union(bowl, mound)), detail(seg(3.5, 13, 16.5, 13)), line(poly([(16.5, 14), (20, 14), (21.5, 8)], r=S.r)),
            solid(circle(8.5, 4.8, 0.9)), solid(circle(12, 4.2, 0.9)), solid(circle(15, 5.2, 0.9))]


@icon("baby-food-blender", CAT, "A squat blender jar on a motor base, with a small steaming puree pot beside it",
      tags=["puree maker", "weaning", "baby food maker", "steamer blender", "homemade baby food", "mash", "appliance"])
def _(S):
    jar = poly([(3.5, 5), (14.5, 5), (13, 14), (5, 14)], closed=True, r=S.r * 0.6)
    lid = rect(3, 2.5, 12, 2.5, rr(S, 1))
    base = rect(4, 14, 10, 6.5, rr(S, 2))
    pot = "M16.5 14H22V18C22 20.2 20.7 21 19.2 21C17.7 21 16.5 20.2 16.5 18Z"
    return [shell(union(jar, lid)), shell(base), shell(pot), line("M18 11.5C17 10.5 19.2 10 18.2 8.8"), line("M20.5 11.5C19.5 10.5 21.7 10 20.7 8.8")]


@icon("baby-led-weaning", CAT, "A small fist gripping the stalk of a broccoli floret held upright",
      tags=["self feeding", "finger food", "solids", "toddler", "broccoli", "first foods", "grabbing"])
def _(S):
    cloud = union(circle(8.5, 8.2, 3.6), circle(12, 6.5, 3.9), circle(15.5, 8.4, 3.6), rect(9, 8.5, 6, 6.5, 0))
    fist = rect(7.5, 14.8, 9, 6.7, rr(S, 3))
    return [shell(union(cloud, fist)), detail(seg(10.5, 17.2, 10.5, 21)), detail(seg(13.5, 17.2, 13.5, 21)), mark(circle(12, 7.5, 0.8))]


@icon("suction-plate", CAT, "A toddler plate divided into three sections, tilted forward on a suction cup base",
      tags=["divided plate", "toddler dish", "silicone", "mealtime", "stay-put plate", "kids tableware", "weaning"])
def _(S):
    cup = poly([(7, 21), (8.8, 17.5), (15.2, 17.5), (17, 21)], closed=True, r=S.r * 0.8)
    return [shell(ellipse(12, 9, 9.5, 6)), detail(seg(12, 9, 12, 3)), detail(seg(12, 9, 5, 12.8)), detail(seg(12, 9, 19, 12.8)),
            line(seg(12, 15, 12, 17.5)), shell(cup)]


@icon("baby-food-freezer-tray", CAT, "A tray with six square compartments and its lid hinged open behind it",
      tags=["puree cubes", "batch cooking", "weaning", "ice cube tray", "freezing", "baby food storage", "portions"])
def _(S):
    lid = poly([(5.5, 3), (18.5, 3), (21, 7.5), (3, 7.5)], closed=True, r=S.r * 0.6)
    tray = rect(3, 11, 18, 10, rr(S, 2.5))
    return [shell(lid), shell(tray), detail(seg(9, 11, 9, 21)), detail(seg(15, 11, 15, 21)), detail(seg(3, 16, 21, 16))]


@icon("mesh-feeder", CAT, "A round mesh bag on a stem with a ring handle, for safely sucking on fruit",
      tags=["fruit feeder", "teething", "baby feeder", "silicone mesh", "weaning", "choke safe", "first foods"])
def _(S):
    return [shell(circle(12, 9, 6)), detail(seg(9.6, 3, 9.6, 15)), detail(seg(14.4, 3, 14.4, 15)), detail(seg(6, 9, 18, 9)),
            line(seg(12, 15, 12, 17.3)), shell(circle(12, 19.8, 2.2))]


@icon("cloth-diaper", CAT, "A shaped reusable nappy seen from the front with a row of snaps along the waist band",
      tags=["reusable nappy", "cloth nappy", "washable", "eco", "baby", "snaps", "changing"])
def _(S):
    d = poly([(3, 4), (21, 4), (21, 9), (16.5, 13), (16, 20.5), (8, 20.5), (7.5, 13), (3, 9)], closed=True, r=S.r * 1.2)
    return [shell(d), detail(seg(3.5, 9.3, 20.5, 9.3)), mark(circle(7.5, 6.6, 0.9)), mark(circle(12, 6.6, 0.9)), mark(circle(16.5, 6.6, 0.9))]


@icon("diaper-cream", CAT, "A squeeze tube with a wide flip cap and a small nappy shape on the front",
      tags=["nappy cream", "rash cream", "ointment", "baby care", "barrier cream", "tube", "changing"])
def _(S):
    tube = poly([(7.5, 6.5), (16.5, 6.5), (17.5, 21), (6.5, 21)], closed=True, r=S.r * 0.6)
    cap = rect(8.5, 2.5, 7, 4, rr(S, 1.2))
    nappy = poly([(9.3, 10.5), (14.7, 10.5), (14.7, 12.5), (13.3, 14), (13.3, 16.5), (10.7, 16.5), (10.7, 14), (9.3, 12.5)], closed=True)
    return [shell(union(tube, cap)), detail(seg(6.8, 19, 17.2, 19)), mark(nappy)]


# ============================================================================ changing, bathing and baby clothes

def star_d(cx, cy, R, r=None):
    r = r or R * 0.45
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        rad = R if i % 2 == 0 else r
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return poly(pts, closed=True)


@icon("training-pants", CAT, "Pull-up style pants with an elastic waist, short wide legs and a star on the front",
      tags=["pull-ups", "potty training", "toilet training", "toddler", "underwear", "nappy", "pants"])
def _(S):
    d = poly([(4, 4), (20, 4), (21.5, 18.5), (14, 18.5), (12, 14), (10, 18.5), (2.5, 18.5)], closed=True, r=S.r)
    return [shell(d), detail(seg(4, 7.5, 20, 7.5)), mark(star_d(12, 11, 2.3))]


@icon("diaper-caddy", CAT, "An open fabric caddy with a carry handle across the top and two rolled nappies inside",
      tags=["nappy organiser", "changing basket", "nursery storage", "diaper organizer", "baby supplies", "tote", "storage"])
def _(S):
    body = poly([(3, 10), (21, 10), (19.5, 20.5), (4.5, 20.5)], closed=True, r=S.r * 1.2)
    return [shell(body), line(poly([(5, 10), (5, 4.5), (19, 4.5), (19, 10)], r=S.r)), detail(seg(12, 10, 12, 20.5)),
            mark(circle(7.8, 14.8, 1.9)), mark(circle(16.2, 14.8, 1.9))]


@icon("wipe-warmer", CAT, "A rounded box with a wipe popping out of the lid and wavy heat lines rising beside it",
      tags=["baby wipes", "warm wipes", "changing table", "heater", "nursery", "nappy change", "warmth"])
def _(S):
    body = rect(3.5, 12, 17, 9, rr(S, 3))
    wipe = rect(9.5, 6, 5, 6.5, rr(S, 1.2))
    return [shell(union(body, wipe)), detail(seg(3.5, 15.2, 20.5, 15.2)), line("M5.5 9.5C4.5 8.3 6.7 7.2 5.7 5.5"),
            line("M18.5 9.5C17.5 8.3 19.7 7.2 18.7 5.5")]


@icon("baby-rinse-cup", CAT, "A tipped cup pouring a stream of water, used to rinse a baby's hair at bath time",
      tags=["bath cup", "hair rinse", "bath time", "pouring", "newborn bath", "jug", "water"])
def _(S):
    body = mv(rot(poly([(3.5, 3), (14, 3), (12.5, 15), (5, 15)], closed=True, r=S.r * 0.8), 35, 9, 9), 2, 1.5)
    return [shell(body), line("M16 12.5C18.5 15 18.5 18 17.5 21.5"), solid(circle(21, 15, 1.1)), solid(circle(21, 20, 1.1))]


@icon("tummy-tub", CAT, "A tall bucket-shaped baby bath with a rounded rim and a baby's head poking above it",
      tags=["bucket bath", "newborn bath", "baby bathing", "soak", "bath time", "infant tub", "bathtub"])
def _(S):
    body = poly([(4.5, 11), (19.5, 11), (17.5, 21.5), (6.5, 21.5)], closed=True, r=S.r * 0.8)
    rim = rect(3, 9, 18, 3, rr(S, 1.5))
    return [shell(circle(12, 4.3, 2.6)), shell(union(body, rim)), detail(seg(5.2, 15.5, 18.8, 15.5))]


@icon("baby-hairbrush", CAT, "A soft round-headed baby brush with bristle rows beside a small wide-tooth comb",
      tags=["brush and comb", "grooming", "cradle cap", "newborn hair", "baby care", "soft bristles", "set"])
def _(S):
    return [shell(ellipse(8, 8.5, 5, 5.7)), detail(seg(6, 6, 6, 11)), detail(seg(10, 6, 10, 11)),
            shell(rect(6.5, 14.2, 3, 7.3, rr(S, 1.5))), shell(rect(14, 3, 7, 5, rr(S, 1.5))),
            line(seg(15.5, 8, 15.5, 20.5)), line(seg(19.5, 8, 19.5, 20.5))]


@icon("scratch-mittens", CAT, "A pair of small rounded mittens with no thumbs and ribbed elastic cuffs, tilted like two little hands",
      tags=["baby mittens", "newborn gloves", "no scratch", "hands", "soft mitts", "infant clothing", "cuffs"])
def _(S):
    m = union(circle(7, 8.5, 4.6), rect(2.4, 8.5, 9.2, 5, 0), rect(3.4, 13, 7.2, 7.5, 0))
    cuff = seg(3.4, 16, 10.6, 16)
    return [shell(rot(m, -12, 7, 14)), detail(rot(cuff, -12, 7, 14)), shell(rot(flip(m), 12, 17, 14)), detail(rot(flip(cuff), 12, 17, 14))]


def sock_d(k, ox, oy):
    d = "M0 0H7V9.5C7 10.8 7.8 11.6 9.3 12C13 12.8 15.5 14 15.5 16.3C15.5 18 14.2 19 12.7 19H3C1.2 19 0 17.7 0 16Z"
    return sc(d, k, ox, oy)


@icon("baby-socks", CAT, "A pair of tiny socks with ribbed cuffs, one tucked slightly behind the other",
      tags=["booties", "infant socks", "newborn clothes", "feet", "baby clothing", "tiny", "pair"])
def _(S):
    a = sock_d(0.72, 2, 2)
    b = minus(sock_d(0.72, 9, 7.5), grow(a, 1.8))
    return [shell(a, stroke_miterlimit="2"), detail(seg(2, 5, 7, 5)), shell(b, stroke_miterlimit="2"), detail(seg(9, 10.5, 14, 10.5))]


@icon("footed-sleepsuit", CAT, "A one-piece baby sleepsuit with long sleeves, closed feet and snaps down the front",
      tags=["babygrow", "romper", "pajamas", "pyjamas", "sleeper", "newborn clothes", "onesie with feet"])
def _(S):
    d = poly([(9, 3), (15, 3), (19.5, 6), (21.5, 14), (18.5, 14.8), (17, 9.5), (17, 16), (17.5, 21), (12.7, 21), (12, 17),
              (11.3, 21), (6.5, 21), (7, 16), (7, 9.5), (5.5, 14.8), (2.5, 14), (4.5, 6)], closed=True, r=S.r * 0.8)
    return [shell(d), detail("M9 3C10 6 14 6 15 3"), mark(circle(12, 10, 0.9)), mark(circle(12, 13, 0.9)), mark(circle(12, 16, 0.9))]


@icon("christening-gown", CAT, "A long baby gown with puffed sleeves, a short bodice and a scalloped lace hem",
      tags=["baptism gown", "dress", "naming ceremony", "heirloom", "baby dress", "lace", "religious"])
def _(S):
    gown = ("M10 3H14L15.3 10L21 19.5A2.25 2 0 0 1 16.5 19.5A2.25 2 0 0 1 12 19.5A2.25 2 0 0 1 7.5 19.5A2.25 2 0 0 1 3 19.5L8.7 10Z")
    sleeves = union(circle(6.5, 6.8, 2.7), circle(17.5, 6.8, 2.7))
    return [shell(union(gown, sleeves)), detail(seg(8.7, 10.5, 15.3, 10.5))]


@icon("baby-fever", CAT, "A baby's face with closed eyes, a thermometer in the mouth and a drop of sweat",
      tags=["sick baby", "temperature", "thermometer", "illness", "feverish", "infant health", "unwell"])
def _(S):
    return [shell(circle(10.5, 13, 7.5)), line("M10.5 5.5C10.5 3.8 12 3 13.2 4"), detail("M5.8 12C6.6 13.2 8.2 13.2 9 12"),
            detail("M12.2 12C13 13.2 14.6 13.2 15.4 12"), line(poly([(11, 16.6), (20.5, 12.6)], r=0)), solid("M19.5 3.2L21 6A1.7 1.7 0 0 1 18 6Z")]


@icon("crying-baby", CAT, "A round baby face with a tuft of hair, squeezed shut eyes, a wide open mouth and tears",
      tags=["baby crying", "tantrum", "colic", "fussy", "wailing", "sad", "upset"])
def _(S):
    return [shell(circle(12, 13, 8.2)), line("M12 4.8C12 3 13.4 2.5 14.5 3.4"),
            detail(poly([(6.8, 9.5), (9.6, 11.2), (6.8, 12.9)], r=S.r * 0.4)), detail(poly([(17.2, 9.5), (14.4, 11.2), (17.2, 12.9)], r=S.r * 0.4)),
            mark(ellipse(12, 17.2, 2.8, 2)), mark("M6.8 14.8L7.8 16.8A1 1 0 0 1 5.8 16.8Z"), mark("M17.2 14.8L18.2 16.8A1 1 0 0 1 16.2 16.8Z")]


@icon("sleeping-baby", CAT, "A round baby head resting on a pillow with closed curved eyes and a small z above",
      tags=["baby asleep", "nap", "bedtime", "sweet dreams", "newborn sleep", "zzz", "rest"])
def _(S):
    pillow = rect(2.5, 14.5, 17, 6.5, rr(S, 3))
    return [shell(union(pillow, circle(10.5, 11, 6.5))), detail("M5.8 10C6.6 11.4 8.2 11.4 9 10"), detail("M12.4 10C13.2 11.4 14.8 11.4 15.6 10"),
            line(poly([(17, 3), (21, 3), (17, 7), (21, 7)], r=0))]


# ============================================================================ baby health and care

@icon("infant-vaccination", CAT, "A swaddled baby bundle with a head, beside a syringe angled in towards it",
      tags=["baby jab", "immunisation", "immunization", "shot", "needle", "newborn health", "injection"])
def _(S):
    syringe = [shell(rect(17, 4, 3.6, 8, rr(S, 0.8))), line(seg(16.5, 2.5, 21.1, 2.5)), line(seg(18.8, 2.5, 18.8, 4)), line(seg(18.8, 12, 18.8, 16.5))]
    syringe = [Part(p.kind, mv(rot(p.d, 28, 18.8, 9), -1.6, 1.8), p.attrs) for p in syringe]
    return [shell(circle(8.5, 6.5, 3)), shell(rect(4, 10.3, 9, 11.2, rr(S, 4))), detail(seg(4.3, 14.5, 12.7, 14.5))] + syringe


@icon("safe-sleep", CAT, "A top view of a baby lying on its back in a crib with nothing else in it",
      tags=["sids", "cot safety", "back to sleep", "empty crib", "infant sleep", "bare cot", "newborn"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, rr(S, 3))), detail(rect(5.5, 5.5, 13, 13, rr(S, 1.5))),
            mark(circle(12, 8.8, 2.3)), mark(rect(9.8, 11.5, 4.4, 5.5, 2))]


@icon("infant-cpr", CAT, "A baby lying on its back with two fingertips pressing the chest over a small heart",
      tags=["baby resuscitation", "first aid", "chest compressions", "emergency", "life saving", "infant rescue", "newborn safety"])
def _(S):
    body = rect(8.5, 12.5, 13, 7, rr(S, 3.5))
    return [shell(circle(5, 16, 3)), shell(body), line(seg(12.2, 2.5, 12.2, 11.8)), line(seg(16.8, 2.5, 16.8, 11.8)), mark(heart_d(14.5, 16.4, 1.0))]


@icon("newborn-hearing-test", CAT, "A newborn's head above a swaddle, a small ear cup on its ear and sound waves beside it",
      tags=["ear screening", "audiology", "sound test", "infant hearing", "otoacoustic", "newborn screening", "ears"])
def _(S):
    return [shell(union(circle(9.5, 9.5, 6), rect(3.5, 14.5, 12, 7, rr(S, 3)))), mark(circle(7.6, 10.2, 1.9)),
            line("M18.5 6.8C19.8 8.8 19.8 11.2 18.5 13.2"), line("M21 4.5C23 8 23 12 21 15.5")]


@icon("cord-blood-bag", CAT, "A medical blood bag with a looped tube at the top and a small swaddled baby on the label",
      tags=["cord blood banking", "stem cells", "umbilical cord", "blood donation", "newborn", "storage", "medical"])
def _(S):
    return [shell(rect(5, 8, 14, 13.5, rr(S, 3))), line(poly([(12, 8), (12, 4.8), (16.5, 4.8), (16.5, 2.5)], r=S.r)),
            mark(circle(12, 12.8, 1.7)), mark(rect(10, 15, 4, 4, 1.8))]


@icon("baby-first-tooth", CAT, "A line of gum with one small tooth breaking through the middle and a sparkle beside it",
      tags=["teething", "milestone", "tooth", "gums", "baby teeth", "dental", "growing up"])
def _(S):
    gum = "M2.5 16C7 14.2 17 14.2 21.5 16V21.5H2.5Z"
    tooth = rect(9.3, 9, 5.4, 8, rr(S, 2.7))
    return [shell(union(gum, tooth)), solid(spark(19, 6.5, 3)), solid(spark(5.5, 8, 1.8))]


# ============================================================================ child safety and gear

@icon("child-safety-harness", CAT, "A small backpack with a top handle and a pocket, with a curling tether strap leading to a hand loop",
      tags=["toddler reins", "walking harness", "leash backpack", "keep close", "kid safety", "wrist strap", "outing"])
def _(S):
    return [shell(rect(2.5, 6, 10.5, 15, rr(S, 3.5))), detail(seg(2.5, 14, 13, 14)), line(poly([(5.5, 6), (5.5, 3.5), (10, 3.5), (10, 6)], r=S.r)),
            line("M13 11C17.5 11 15.5 17 19 17"), shell(circle(20, 17, 2.4))]


@icon("kids-gps-watch", CAT, "A chunky wristwatch with a map pin on its screen and a signal arc at the corner",
      tags=["child tracker", "location watch", "smartwatch for kids", "safety", "find my child", "wearable", "map pin"])
def _(S):
    body = union(rect(5.5, 6, 13, 12, rr(S, 4)), rect(8.5, 2, 7, 4.5, rr(S, 1)), rect(8.5, 17.5, 7, 4.5, rr(S, 1)))
    pin = "M12 15.2C9.8 13 9.2 11.5 9.2 10.3A2.8 2.8 0 0 1 14.8 10.3C14.8 11.5 14.2 13 12 15.2Z"
    return [shell(body), mark(pin), line("M19 3C20.6 3.4 21.6 4.6 21.8 6.2")]


@icon("doorknob-cover", CAT, "A round doorknob enclosed in a ball-shaped safety cover with two squeeze tabs on the sides",
      tags=["child proof", "door safety", "baby proofing", "toddler lock", "knob guard", "safety cover", "home safety"])
def _(S):
    cover = union(circle(12, 12, 8.5), rect(1.6, 10, 3, 4, S.r * 0.9), rect(19.4, 10, 3, 4, S.r * 0.9))
    return [shell(cover), shell(circle(12, 12, 3.6))]


@icon("stove-guard", CAT, "A stove top with two burners and a barred safety gate fixed across the front",
      tags=["cooker guard", "child proofing", "kitchen safety", "baby gate", "hob guard", "toddler safety", "burners"])
def _(S):
    top = poly([(5.5, 2.5), (18.5, 2.5), (21.5, 10.5), (2.5, 10.5)], closed=True, r=S.r * 0.6)
    return [shell(top), mark(ellipse(9.2, 6.4, 2.5, 1.2)), mark(ellipse(14.8, 6.4, 2.5, 1.2)), shell(rect(2.5, 14, 19, 7.5, rr(S, 2))),
            detail(seg(8.8, 14, 8.8, 21.5)), detail(seg(15.2, 14, 15.2, 21.5))]


@icon("baby-swing", CAT, "A baby seat hanging from the top bar of an A-frame stand, with motion arcs on both sides",
      tags=["infant swing", "rocker", "bouncer", "soothing", "nursery", "baby seat", "motion"])
def _(S):
    seat = L(S, "M7 11H17V13.5C17 16.5 14.5 18 12 18C9.5 18 7 16.5 7 13.5Z", "M7 11H17V13.5C17 16.5 14.5 18 12 18C9.5 18 7 16.5 7 13.5Z")
    return [line(poly([(5, 21.5), (7.2, 4), (16.8, 4), (19, 21.5)], r=S.r)), line(seg(10, 4, 10, 11)), line(seg(14, 4, 14, 11)),
            shell(seat), line("M2.5 9.5C1.7 12 1.7 14.5 2.5 17"), line("M21.5 9.5C22.3 12 22.3 14.5 21.5 17")]


@icon("toddler-bed", CAT, "A low bed close to the floor with a pillow and a short safety rail along the front half",
      tags=["kids bed", "transition bed", "child bed", "bedroom", "nursery", "low bed", "guard rail"])
def _(S):
    bed = union(rect(3, 12.5, 18, 5, rr(S, 2)), rect(4.5, 9, 4.5, 4, rr(S, 1.8)))
    return [shell(bed), line(seg(4.5, 17.5, 4.5, 21)), line(seg(19.5, 17.5, 19.5, 21)),
            line(poly([(11.5, 12.5), (11.5, 7), (19.5, 7), (19.5, 12.5)], r=S.r))]


@icon("montessori-shelf", CAT, "A low open shelf with two tiers, each holding a ball, a block and a basket",
      tags=["toy shelf", "playroom", "child-led learning", "toy storage", "early learning", "kids room", "display"])
def _(S):
    out = [shell(rect(2.5, 3, 19, 18.5, rr(S, 4))), detail(seg(2.5, 12.5, 21.5, 12.5))]
    for y in (0, 8.5):
        out += [mark(circle(7, 9 + y, 1.9)), mark(rect(10.8, 7.3 + y, 3.4, 3.5, 0.5)), mark(poly([(16.3, 7.8 + y), (20, 7.8 + y), (19.2, 10.8 + y), (17.1, 10.8 + y)], closed=True))]
    return out


@icon("house-frame-floor-bed", CAT, "A mattress with a pillow on the floor inside a bed frame shaped like a house with a pitched roof",
      tags=["montessori bed", "floor bed", "kids bedroom", "toddler", "house bed", "low sleeping", "playhouse"])
def _(S):
    return [line(poly([(3, 21.5), (3, 10.5), (12, 3), (21, 10.5), (21.5, 21.5)], r=S.r)), shell(rect(6.5, 15.2, 11, 5, rr(S, 2))),
            mark(rect(8, 16.7, 3.5, 2, 1))]


@icon("toy-chest", CAT, "A wooden chest with its lid thrown open, a ball and a block poking out of the top",
      tags=["toy box", "playroom", "storage trunk", "kids room", "tidy up", "toys", "nursery"])
def _(S):
    body = rect(3.5, 11.5, 17, 10, rr(S, 2.5))
    return [shell(union(body, circle(8.5, 7.8, 3.3), rect(13, 5.5, 5, 7, rr(S, 1)))), detail(seg(3.5, 15.5, 20.5, 15.5)), mark(rect(10.8, 17, 2.4, 2.5, 0.5))]


@icon("cradleboard", CAT, "An upright board with a bent hoop over the top and a bundled baby laced in with crossed ties",
      tags=["baby carrier", "traditional carrier", "swaddle board", "infant transport", "native craft", "papoose", "heritage"])
def _(S):
    return [shell(rect(6.5, 7.5, 11, 14.5, rr(S, 3))), line("M6.5 9.5C6.5 1.8 17.5 1.8 17.5 9.5"), mark(circle(12, 11.2, 1.9)),
            detail(seg(9, 15, 15, 18.2)), detail(seg(15, 15, 9, 18.2))]


@icon("baby-hammock", CAT, "A fabric pouch cradle hung from a single coiled spring, with a baby's head resting inside",
      tags=["bouncer cradle", "spring cradle", "swaying", "nursery", "baby hanging bed", "infant", "soothing"])
def _(S):
    pouch = "M3.5 11H20.5C20.5 17 16.8 21 12 21C7.2 21 3.5 17 3.5 11Z"
    return [line(poly([(12, 2), (10, 3.3), (14, 4.6), (10, 5.9), (12, 7.2)], r=S.r * 0.3)),
            line(poly([(5, 11), (12, 7.2), (19, 11)], r=S.r)), shell(pouch), mark(circle(12, 14.3, 2.3))]
