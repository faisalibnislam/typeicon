"""TypeIcon Core: kids (batch kids_001).

Baby gear, nursery furniture, strollers and carriers, baby and toddler play, dolls, plush, and classic
toddler toys, drawn from the objects themselves. Front or side views; small parts sit inside clear
silhouettes so they survive at 16 px.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, LINE as LINE_S, P, ST, U, fmt, path_to_d, rotation, transform_path  # noqa: F401

CAT = "kids"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rot_pts(points, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * ca - (y - cy) * sa, cy + (x - cx) * sa + (y - cy) * ca) for x, y in points]


def mark(d):
    return Part("dot", d)


def pt_on(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def ring(cx, cy, ro, ri):
    return minus(circle(cx, cy, ro), circle(cx, cy, ri))


def wheel(cx, cy, r):
    return [shell(circle(cx, cy, r)), dot(cx, cy, 0.9)]


def flip(d):
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


# ============================================================================ feeding

@icon("formula-can", CAT, "Squat round tin with a wide snap lid and a small scoop resting on top",
      tags=["formula", "baby formula", "milk powder", "infant milk", "tin", "feeding"])
def _(S):
    return [
        shell(rect(4, 10, 16, 11, rr(S, 3))),
        detail(seg(4, 13.5, 20, 13.5)),
        line("M8.5 6.5a3 3 0 0 0 6 0"),
        line(seg(14.5, 6, 19, 3.5)),
    ]


@icon("baby-food-pouch", CAT, "Soft squeeze pouch with a crimped flat bottom and a round spout cap at the top",
      tags=["baby food", "squeeze pouch", "puree", "spout pouch", "feeding", "toddler snack"])
def _(S):
    body = poly([(6.5, 8), (17.5, 8), (18.5, 21), (5.5, 21)], closed=True, r=S.r)
    neck = rect(9.5, 3, 5, 6, 0)
    return [
        shell(union(body, neck)),
        detail(seg(6, 17, 18, 17)),
        detail(seg(9.5, 5.5, 14.5, 5.5)),
    ]


@icon("teether", CAT, "Ring teether with a chunky scalloped circle and a hole in the middle",
      tags=["teething", "teething ring", "baby", "chew toy", "gums", "infant"])
def _(S):
    lobes = [circle(*pt_on(12, 12, 6, a), L(S, 3, 3.25)) for a in range(-90, 270, 60)]
    body = minus(union(circle(12, 12, 6), *lobes), circle(12, 12, 2.5))
    return [shell(body)]


@icon("pacifier", CAT, "Front view of a pacifier: wide shield with a ring handle above and a round teat below",
      tags=["dummy", "soother", "binky", "baby", "infant", "teat"])
def _(S):
    shield = ellipse(12, 12.5, 9.5, L(S, 3.75, 4.25))
    teat = circle(12, 18.5, L(S, 2.75, 3))
    return [
        shell(union(shield, teat)),
        line(circle(12, 5.75, 3)),
        dot(6.5, 12.5, 1),
        dot(17.5, 12.5, 1),
    ]


@icon("bib", CAT, "Rounded baby bib with a neck cut-out and a small pocket at the bottom edge",
      tags=["baby bib", "feeding", "drool", "mealtime", "infant", "dribble"])
def _(S):
    r = L(S, 2, 4)
    body = (f"M6 3H9A3 3 0 0 0 15 3H18Q18 9 20.5 13V{21 - r}A{r} {r} 0 0 1 {20.5 - r} 21H{3.5 + r}"
            f"A{r} {r} 0 0 1 3.5 {21 - r}V13Q6 9 6 3Z")
    return [
        shell(body),
        detail(poly([(8, 21), (8, 16), (16, 16), (16, 21)], r=S.r * 0.5)),
    ]


@icon("snack-cup", CAT, "Cylinder cup with two handles and a soft flap lid, with a snack peeking through",
      tags=["snack cup", "toddler snack", "spill proof", "cheerios cup", "sippy", "kids"])
def _(S):
    return [
        shell(poly([(6.5, 10), (17.5, 10), (16.5, 21), (7.5, 21)], closed=True, r=S.r)),
        detail(seg(7, 13, 17, 13)),
        line(poly([(6.3, 12), (3, 12), (3, 16.5), (7, 16.5)], r=S.r * 0.5)),
        line(poly([(17.7, 12), (21, 12), (21, 16.5), (17, 16.5)], r=S.r * 0.5)),
        line(poly([(9, 10), (9, 7.5), (15, 7.5), (15, 10)], r=S.r * 0.5)),
        dot(10.5, 4.25, 1.25),
        dot(13.75, 4.75, 1.25),
    ]


@icon("milk-storage-bag", CAT, "Flat upright pouch with a zip seal across the top and measurement lines on its face",
      tags=["breast milk", "milk bag", "storage bag", "freezer bag", "pumping", "nursing"])
def _(S):
    body = poly([(6, 3), (18, 3), (18, 18.5), (15.5, 21), (8.5, 21), (6, 18.5)], closed=True, r=S.r)
    return [
        shell(body),
        detail(seg(6, 7, 18, 7)),
        detail(seg(9.5, 11, 14.5, 11)),
        detail(seg(9.5, 14.5, 12.5, 14.5)),
        detail(seg(9.5, 18, 14.5, 18)),
    ]


@icon("nursing-pillow", CAT, "C shaped padded pillow seen from above, curving around a small baby head",
      tags=["feeding pillow", "breastfeeding pillow", "nursing", "support pillow", "baby", "horseshoe"])
def _(S):
    def band(cx, cy, ro, ri, a0, a1):
        p0, p1 = pt_on(cx, cy, ro, a0), pt_on(cx, cy, ro, a1)
        q1, q0 = pt_on(cx, cy, ri, a1), pt_on(cx, cy, ri, a0)
        large = 1 if (a1 - a0) % 360 > 180 else 0
        return (f"M{fmt(p0[0])} {fmt(p0[1])}A{fmt(ro)} {fmt(ro)} 0 {large} 1 {fmt(p1[0])} {fmt(p1[1])}"
                f"L{fmt(q1[0])} {fmt(q1[1])}A{fmt(ri)} {fmt(ri)} 0 {large} 0 {fmt(q0[0])} {fmt(q0[1])}Z")
    e1, e2 = pt_on(12, 12, 6.25, 320), pt_on(12, 12, 6.25, 220)
    rad = L(S, 2.75, 3.25)
    body = union(band(12, 12, 9, 3.5, 320, 220 + 360), circle(*e1, rad), circle(*e2, rad))
    return [shell(body), dot(12, 12, 1.6)]


@icon("booster-seat", CAT, "Backless car booster cushion with raised arm rests and a belt guide on each side",
      tags=["booster", "car seat", "child seat", "travel", "belt guide", "toddler"])
def _(S):
    body = poly([(3, 8), (8, 8), (8, 13), (16, 13), (16, 8), (21, 8), (21, 20), (3, 20)], closed=True, r=S.r)
    return [
        shell(body),
        dot(5.5, 11, 1),
        dot(18.5, 11, 1),
        detail(seg(8, 16.5, 16, 16.5)),
    ]


@icon("car-seat", CAT, "Infant car seat carrier in side view with a canopy and an arched carry handle",
      tags=["infant seat", "baby carrier", "bucket seat", "car travel", "baby", "safety seat"])
def _(S):
    body = poly([(4, 9), (11, 9), (20, 15), (20, 18.5), (4, 18.5)], closed=True, r=S.r)
    return [
        shell(body),
        detail(poly([(8, 9), (8, 14)], r=0)),
        line("M5.5 9C6.5 2.5 15.5 2.5 18 13"),
        line("M5.5 21.5H18.5"),
    ]


@icon("stroller", CAT, "Side view of a reclining stroller with a folded hood, a curved push handle and small wheels",
      tags=["pushchair", "buggy", "baby", "pram", "toddler", "walk"])
def _(S):
    top = union("M6 12A7 7 0 0 1 13 5V12Z", poly([(4, 12), (20, 12), (20, 14), (16, 17), (4, 17)], closed=True, r=S.r))
    return [
        shell(top),
        line(poly([(4, 12), (3, 6), (1.5, 6)], r=S.r * 0.6)),
        *wheel(8, 19.5, 2.25),
        *wheel(18, 19.5, 2.25),
    ]


@icon("pram", CAT, "Deep bassinet body on a high sprung chassis with a big hood, a curved handle and large wheels",
      tags=["baby carriage", "perambulator", "bassinet", "buggy", "baby", "newborn"])
def _(S):
    body = "M3 9H20C20 13 17 14.25 13 14.25H10C6 14.25 3 13 3 9Z"
    hood = "M3 9A6.5 6.5 0 0 1 9.5 2.5V9Z"
    return [
        shell(union(body, hood)),
        line("M3 7.5C3 5.5 2.5 4.5 1.5 4.5"),
        *wheel(7, 18.5, 3),
        *wheel(17, 18.5, 3),
    ]


@icon("jogging-stroller", CAT, "Three wheel stroller with one large front wheel, rear wheels and a canopy over the seat",
      tags=["jogger", "running stroller", "all terrain", "baby", "outdoor", "three wheel"])
def _(S):
    top = union("M6 9A6 6 0 0 1 12 3V9Z", poly([(5, 9), (15, 9), (15, 12), (11, 14), (5, 14)], closed=True, r=S.r))
    return [
        shell(top),
        line(poly([(5, 9), (3.5, 4), (1.5, 4)], r=S.r * 0.6)),
        line(poly([(14, 14), (18.5, 16)], r=0)),
        *wheel(7, 17.5, 3.5),
        *wheel(18.5, 17.5, 3.5),
    ]


@icon("double-stroller", CAT, "Side by side stroller seen from the front with two seats, two canopies and one handlebar",
      tags=["twin stroller", "two seat stroller", "tandem", "baby", "siblings", "twins"])
def _(S):
    def unit(x0):
        return union(f"M{x0} 10A3.5 3.5 0 0 1 {x0 + 7} 10Z", rect(x0, 10, 7, 5.5, 0))
    return [
        shell(unit(3)),
        shell(unit(14)),
        line(poly([(2.5, 3), (21.5, 3)], r=0)),
        line(seg(12, 3, 12, 17)),
        *wheel(6.5, 19.25, 2.25),
        *wheel(17.5, 19.25, 2.25),
    ]


@icon("bike-trailer", CAT, "Low covered child trailer with two big wheels and a tow arm reaching forward",
      tags=["bicycle trailer", "kids trailer", "cycling", "tow", "child carrier", "bike"])
def _(S):
    body = "M3 13V9.5Q3 5 8 5H12Q17 5 17 9.5V13Z"
    return [
        shell(body),
        detail(poly([(6.5, 10.5), (6.5, 8.5), (13.5, 8.5), (13.5, 10.5)], r=S.r * 0.5)),
        *wheel(10, 17.75, 3),
        line(poly([(10, 17.75), (17, 17.75), (21.5, 12)], r=S.r * 0.5)),
    ]


# ============================================================================ carriers and baby gear

@icon("child-bike-seat", CAT, "Rear bicycle wheel with a high backed child seat mounted over it and small foot rests",
      tags=["bicycle seat", "bike child seat", "cycling with kids", "child carrier", "rear seat", "family cycling"])
def _(S):
    seat = poly([(4.5, 2.5), (9, 2.5), (9, 8), (16, 8), (16, 11), (4.5, 11)], closed=True, r=S.r)
    return [
        shell(seat),
        line(poly([(15.5, 11), (19, 14.5)], r=0)),
        line(circle(11, 17.25, 4.5)),
        dot(11, 17.25, 1),
        line(poly([(11, 17.25), (20, 11.5)], r=0)),
    ]


@icon("hiking-child-carrier", CAT, "Framed backpack with a seat opening on top, a kickstand frame and a small sun canopy",
      tags=["child backpack carrier", "baby backpack", "hiking with kids", "trail carrier", "toddler carrier", "outdoor"])
def _(S):
    body = union(rect(5, 14, 11, 7, rr(S, 2.5)), circle(10.5, 11.25, 2.5))
    return [
        shell("M3.5 7.5A7 4.5 0 0 1 17.5 7.5Z"),
        shell(body),
        line(poly([(5, 15), (3.5, 21.5)], r=0)),
        line(poly([(14.5, 19.5), (20, 21.5)], r=0)),
        dot(9.75, 11, 0.7),
        dot(11.5, 11, 0.7),
    ]


@icon("baby-carrier", CAT, "Soft structured carrier with shoulder straps and a baby head peeking from the pouch",
      tags=["baby wearing", "front carrier", "infant carrier", "sling", "parenting", "newborn"])
def _(S):
    body = union(rect(5.5, 11, 13, 10, rr(S, 3)), circle(12, 8.25, 3.25))
    return [
        shell(body),
        detail(seg(5.5, 16.5, 18.5, 16.5)),
        line(poly([(6.5, 11.5), (4.5, 3.5)], r=0)),
        line(poly([(17.5, 11.5), (19.5, 3.5)], r=0)),
    ]


@icon("baby-sling", CAT, "Fabric sling looped over one shoulder and hanging diagonally as a pouch with a ring at the shoulder",
      tags=["wrap", "baby wrap", "ring sling", "baby wearing", "carrier", "newborn"])
def _(S):
    cloth = "M8 7C14 6.5 19.5 10 20.5 17Q20.7 19.75 18 19.75C12 19.75 7 16 5.5 10.5Q5.5 8 8 7Z"
    return [
        shell(cloth),
        detail("M8.5 10.5C13 10.5 16.5 13 17.5 17"),
        line(circle(5, 5, 2)),
    ]


@icon("baby-on-board-sign", CAT, "Diamond shaped sign hanging from a suction cup, showing a baby face in the center",
      tags=["baby on board", "car sign", "child in car", "window sign", "safety", "driving"])
def _(S):
    return [
        shell(poly([(12, 6.5), (20, 14), (12, 21.5), (4, 14)], closed=True, r=S.r * 1.3)),
        dot(10, 13, 0.95),
        dot(14, 13, 0.95),
        detail("M10 16.25Q12 18 14 16.25"),
        line(seg(12, 3.5, 12, 6.5)),
        solid(circle(12, 3, 1.5)),
    ]


@icon("baby-walker", CAT, "Round wheeled walker with a fabric seat in the middle and a wide tray ring around it",
      tags=["walker", "baby walker", "first steps", "wheels", "infant", "toddler"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 4, rr(S, 2))),
        line("M8 8.5V13A4 4 0 0 0 16 13V8.5"),
        line(seg(4.5, 8.5, 4.5, 17.5)),
        line(seg(19.5, 8.5, 19.5, 17.5)),
        line(seg(3, 17.5, 21, 17.5)),
        solid(circle(6, 19.75, 1.9)),
        solid(circle(18, 19.75, 1.9)),
    ]


@icon("push-walker", CAT, "Small wagon on four wheels with a tall push handle and blocks stacked inside",
      tags=["push toy", "baby walker wagon", "walking toy", "learn to walk", "wagon", "blocks"])
def _(S):
    body = union(rect(6, 10.5, 15, 6.5, rr(S, 2)), rect(9, 5.5, 5, 5, 0), circle(18, 8.25, 2.25))
    return [
        shell(body),
        line(poly([(6.5, 12), (3, 3), (1.5, 3)], r=S.r * 0.6)),
        solid(circle(10, 19.5, 2)),
        solid(circle(18, 19.5, 2)),
    ]


@icon("doorway-jumper", CAT, "Door frame with a clamp at the top and straps holding a small seat hanging in the opening",
      tags=["baby bouncer", "jumper", "door jumper", "exersaucer", "bouncing", "infant"])
def _(S):
    return [
        line(poly([(3.5, 21.5), (3.5, 3), (20.5, 3), (20.5, 21.5)], r=0)),
        shell(rect(9.5, 3, 5, 4, rr(S, 1))),
        line(seg(10.5, 7, 10.5, 12.5)),
        line(seg(13.5, 7, 13.5, 12.5)),
        shell(rect(8, 12.5, 8, 4.5, rr(S, 2))),
        line(seg(10.25, 17, 10.25, 20.5)),
        line(seg(13.75, 17, 13.75, 20.5)),
    ]


@icon("activity-center", CAT, "Round stationary seat set in a wide tray with a few toys standing on the rim",
      tags=["exersaucer", "baby activity center", "jumper", "saucer", "seat", "play"])
def _(S):
    return [
        shell(rect(2.5, 10, 19, 3.5, rr(S, 1.75))),
        line("M8 13.5V16.5A4 4 0 0 0 16 16.5V13.5"),
        line(poly([(6, 10), (6, 8)])),
        shell(circle(6, 6.25, 2)),
        line("M10 10V7.5A2 2 0 0 1 14 7.5V10"),
        shell(rect(16, 5.5, 4, 4, rr(S, 1))),
        line(seg(4, 20.5, 20, 20.5)),
    ]


@icon("corner-guard", CAT, "Table corner with a soft rounded bumper capping its sharp vertical edge",
      tags=["corner protector", "edge bumper", "table corner", "childproofing", "baby proofing", "soft cap"])
def _(S):
    return [
        shell(poly([(12, 3), (21, 7.5), (12, 12), (3, 7.5)], closed=True, r=S.r)),
        line(poly([(3, 7.5), (3, 16.5), (8.75, 19.4)], r=0)),
        line(poly([(21, 7.5), (21, 16.5), (15.25, 19.4)], r=0)),
        shell(rect(8.75, 11, 6.5, 10.5, L(S, 1.5, 3.25))),
    ]


@icon("cabinet-safety-latch", CAT, "Two cabinet doors with knobs bridged by a strap lock",
      tags=["cabinet lock", "child lock", "childproofing", "baby proofing", "cupboard latch", "safety strap"])
def _(S):
    return [
        shell(rect(3, 3, 7, 18, L(S, 0.5, 3))),
        shell(rect(14, 3, 7, 18, L(S, 0.5, 3))),
        line(seg(7.5, 11, 16.5, 11)),
        dot(7.5, 11, 1.5),
        dot(16.5, 11, 1.5),
    ]


@icon("moses-basket", CAT, "Woven oval basket with two carry handles and a small blanket folded over the rim",
      tags=["bassinet", "baby basket", "cradle", "newborn bed", "crib", "sleeping"])
def _(S):
    body = "M4 11.5H20C20 17.5 16.5 20.5 12 20.5C7.5 20.5 4 17.5 4 11.5Z"
    return [
        shell(body),
        shell("M7.5 11.5C8 8 10 6.5 12 6.5C14.5 6.5 16 8 16.5 11.5Z"),
        line(poly([(4.5, 9), (2.5, 9), (2.5, 12.5), (4.5, 12.5)], r=S.r * 0.5)),
        line(poly([(19.5, 9), (21.5, 9), (21.5, 12.5), (19.5, 12.5)], r=S.r * 0.5)),
        detail(seg(5, 15.5, 19, 15.5)),
    ]


@icon("baby-lounger", CAT, "Oval padded nest seen from above with a small swaddled baby lying in the flat middle",
      tags=["baby nest", "infant lounger", "newborn lounger", "co sleeper", "pad", "cushion"])
def _(S):
    baby = union(circle(12, 8.5, 2), rect(9.5, 10.5, 5, 8, 2.5))
    return [
        shell(ellipse(12, 12, 10, L(S, 8.75, 9))),
        detail(baby),
    ]


@icon("lovey", CAT, "Small security blanket with an animal head on top and knotted corners",
      tags=["security blanket", "comfort blanket", "blankie", "baby comfort", "plush", "toddler"])
def _(S):
    body = union(rect(5, 10, 14, 11, rr(S, 2)), circle(12, 7.5, 3.5), circle(4.75, 10.5, 2), circle(19.25, 10.5, 2))
    return [
        shell(body),
        dot(10.75, 7.25, 0.85),
        dot(13.25, 7.25, 0.85),
        detail(seg(5, 16, 19, 16)),
    ]


@icon("diaper-pail", CAT, "Tall bin with a hinged domed lid and a foot pedal at the base",
      tags=["nappy bin", "diaper bin", "trash", "nursery", "baby", "waste"])
def _(S):
    body = union(poly([(6.5, 9.5), (17.5, 9.5), (17, 20.5), (7, 20.5)], closed=True, r=S.r),
                 "M5 9.5A7 5 0 0 1 19 9.5Z")
    return [
        shell(body),
        detail(seg(5.5, 10, 18.5, 10)),
        line(poly([(17, 18), (21.5, 18), (21.5, 21.5)], r=S.r * 0.6)),
    ]


# ============================================================================ furniture and nursery

@icon("learning-tower", CAT, "Tall platform with railings on all sides and a ladder front, so a toddler can stand at a counter",
      tags=["kitchen helper", "toddler tower", "step stool", "standing tower", "counter helper", "toddler"])
def _(S):
    return [
        line(seg(5.5, 2.5, 5.5, 21.5)),
        line(seg(18.5, 2.5, 18.5, 21.5)),
        detail(seg(5.5, 4.5, 18.5, 4.5)),
        detail(seg(5.5, 8.5, 18.5, 8.5)),
        shell(rect(5.5, 12, 13, 3, 0)),
        detail(seg(5.5, 18.5, 18.5, 18.5)),
        line(seg(3, 21.5, 8, 21.5)),
        line(seg(16, 21.5, 21, 21.5)),
    ]


@icon("kids-table", CAT, "Small low table with two small chairs tucked on either side",
      tags=["children's table", "toddler table", "play table", "small chairs", "activity table", "nursery furniture"])
def _(S):
    return [
        shell(rect(7.5, 10, 9, 3, 0)),
        line(seg(9.5, 13, 9.5, 20)),
        line(seg(14.5, 13, 14.5, 20)),
        line(poly([(2.5, 7.5), (2.5, 15.5), (5, 15.5), (5, 20)], r=S.r * 0.5)),
        line(poly([(21.5, 7.5), (21.5, 15.5), (19, 15.5), (19, 20)], r=S.r * 0.5)),
    ]


@icon("race-car-bed", CAT, "Side view of a bed shaped like a race car, with wheels, a spoiler and a mattress inside",
      tags=["car bed", "toddler bed", "kids bed", "bedroom", "racing", "themed bed"])
def _(S):
    body = poly([(2.5, 16), (2.5, 11.5), (8, 10), (11, 6.5), (17, 6.5), (18.5, 10), (21.5, 11.5), (21.5, 16)], closed=True, r=S.r)
    return [
        shell(body),
        detail(poly([(11, 9.5), (12.5, 9.5)])),
        line(poly([(2.5, 11), (2.5, 6.5), (6, 6.5)], r=S.r * 0.5)),
        solid(circle(7, 17.75, 2.4)),
        solid(circle(17, 17.75, 2.4)),
    ]


@icon("diaper-bag", CAT, "Wide tote bag with a carry handle, a front pocket and a bottle poking out of the top",
      tags=["nappy bag", "changing bag", "baby bag", "tote", "parenting", "baby gear"])
def _(S):
    bag = rect(3, 10, 18, 11, rr(S, 3))
    bottle = rot(rect(15.5, 2.5, 4, 10, 1.75), 14, 17.5, 8)
    cutter = U(P(bag), ST(bag, 5, "round", "round"))
    return [
        shell(bag),
        shell(path_to_d(D(P(bottle), cutter))),
        detail(poly([(7, 21), (7, 16), (14, 16), (14, 21)], r=S.r * 0.5)),
        line("M5.5 10C5.5 3.5 11.5 3.5 11.5 10"),
    ]


@icon("diaper-cake", CAT, "Three tier cake built from rolled diapers, tied with a ribbon and topped with a small bottle",
      tags=["nappy cake", "baby shower", "baby shower gift", "diapers", "gift", "newborn present"])
def _(S):
    tiers = union(rect(3.5, 15, 17, 6, rr(S, 2)), rect(6, 10.5, 12, 5, rr(S, 1.5)), rect(8.75, 7, 6.5, 4, rr(S, 1.5)))
    return [
        shell(tiers),
        detail(seg(3.5, 18, 20.5, 18)),
        line(seg(12, 2.5, 12, 5)),
    ]


@icon("ultrasound-photo", CAT, "Printed scan photo with a wedge shaped scan area showing a small curled baby shape",
      tags=["sonogram", "ultrasound", "scan picture", "pregnancy", "prenatal", "baby bump"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, rr(S, 2.5))),
        detail("M12 5.5L6.5 14.5A6.5 6.5 0 0 0 17.5 14.5Z"),
        dot(12, 12.5, 1.6),
    ]


@icon("baby-handprint", CAT, "Small chubby handprint with five short rounded fingers",
      tags=["hand print", "handprint", "baby hand", "keepsake", "footprint craft", "newborn"])
def _(S):
    xs = [7.15, 10.45, 13.75, 17.05]
    tops = [8.25, 6, 7, 9.75]
    parts = [circle(x, t, 1.65) for x, t in zip(xs, tops)]
    parts += [rect(x - 1.65, t, 3.3, 9) for x, t in zip(xs, tops)]
    palm = rect(5.5, 11, 13.2, 9.75, rr(S, 3.5))
    thumb = path_to_d(ST("M6.75 17.5L3.5 13", 3.3, "round", "round"))
    body = union(palm, thumb, *parts)
    return [
        shell(body),
        detail(seg(8.8, 9.75, 8.8, 13.5)),
        detail(seg(12.1, 9, 12.1, 13.5)),
        detail(seg(15.4, 10.5, 15.4, 13.5)),
    ]


@icon("swaddled-baby", CAT, "Baby face peeking out of a tightly wrapped blanket bundle with a crossover fold",
      tags=["swaddle", "newborn", "wrapped baby", "baby blanket", "burrito", "infant"])
def _(S):
    body = union(rect(5.5, 10, 13, 11.5, rr(S, 5)), circle(12, 7.25, 4))
    return [
        shell(body),
        dot(10.5, 7, 0.85),
        dot(13.5, 7, 0.85),
        detail(seg(6, 13.5, 18, 19.5)),
        detail(seg(18, 13.5, 14, 15.5)),
    ]


@icon("sleep-sack", CAT, "Sleeveless wearable blanket shaped like a bell with a zip down the front",
      tags=["wearable blanket", "baby sleeping bag", "sleep bag", "nursery", "safe sleep", "bedtime"])
def _(S):
    r = L(S, 1, 2.5)
    body = f"M7 3H9.5A2.5 2.5 0 0 0 14.5 3H17Q17 7 16.5 9.5L20.5 {21 - r}Q20.7 21 {20.5 - r} 21H{3.5 + r}Q3.3 21 3.5 {21 - r}L7.5 9.5Q7 7 7 3Z"
    return [
        shell(body),
        detail(seg(12, 8, 12, 21)),
        dot(12, 11, 1.25),
    ]


@icon("fairy-wings", CAT, "Pair of double lobed wings with vein lines joined at a small center",
      tags=["wings", "fairy", "costume", "dress up", "pixie", "butterfly wings"])
def _(S):
    up = "M10.5 12C5 11 2.5 7 3.5 3.5C7.5 3 11 6.5 10.5 12Z"
    low = "M10.5 12.5C6 12.5 4 16 5.5 19.5C9 20 11 16.5 10.5 12.5Z"
    left = union(up, low)
    right = flip(left)
    return [
        shell(union(left, right)),
        detail("M10 11C8.5 9 7 7.5 5.5 6"),
    ]


@icon("animal-ears-headband", CAT, "Headband arc with two rounded bear ears on top",
      tags=["ears", "bear ears", "costume", "dress up", "hair band", "kids party"])
def _(S):
    ears = [(7.1, 8.4), (16.9, 8.4)]
    band = ST("M3 21A9 12 0 0 1 21 21", 2, "butt" if S.name == "line" else "round", "round")
    cut = U(*[P(circle(x, y, 3.25)) for x, y in ears])
    parts = [Part("solid", path_to_d(D(band, cut)))]
    for x, y in ears:
        parts.append(shell(circle(x, y, 3.25)))
        parts.append(dot(x, y, 1.1))
    return parts


@icon("crawling-baby", CAT, "Side view of a baby on hands and knees with a round head",
      tags=["crawl", "infant", "tummy time", "milestone", "toddler", "baby moving"])
def _(S):
    body = union(rect(4.5, 7.5, 11.5, 5.5, 2.75), circle(18.5, 8.25, 2.75))
    return [
        shell(body),
        line(poly([(14, 13), (15, 20.5)])),
        line(poly([(7, 13), (9, 18), (3.5, 20.5)], r=S.r * 0.5)),
        dot(19.25, 7.75, 0.75),
    ]


@icon("breastfeeding", CAT, "Parent figure cradling a baby held at the chest",
      tags=["nursing", "feeding baby", "lactation", "mother", "parent and baby", "infant care"])
def _(S):
    torso = f"M3.5 21V15A5.5 5.5 0 0 1 9 9.5A5.5 5.5 0 0 1 14.5 15V21Z"
    baby = rot(rect(10.5, 12.25, 11, 5.5, 2.75), -22, 16, 15)
    cutter = U(P(baby), ST(baby, 5, "round", "round"))
    return [
        shell(circle(9, 5, 2.5)),
        shell(path_to_d(D(P(torso), cutter))),
        shell(baby),
    ]


@icon("bottle-feeding", CAT, "Parent arm cradling a baby head with a bottle tilted toward the mouth",
      tags=["feeding bottle", "formula feeding", "baby bottle", "infant care", "nursing bottle", "feed"])
def _(S):
    bottle = union(rect(13, 8, 8, 4.5, 1.5), rect(11, 9.5, 2.5, 1.5, 0))
    return [
        shell(circle(7, 12, 3.5)),
        shell(rot(bottle, -25, 11, 10.25)),
        dot(6.5, 11.5, 0.8),
        line("M2.5 19C7 19.5 12 18 14.5 14"),
    ]


@icon("twins", CAT, "Two identical baby faces side by side, each with a single curl on top",
      tags=["twin babies", "double", "siblings", "two babies", "pair", "multiples"])
def _(S):
    parts = []
    for cx in (6.5, 17.5):
        parts += [
            shell(circle(cx, 14, 3.75)),
            dot(cx - 1.25, 13.5, 0.8),
            dot(cx + 1.25, 13.5, 0.8),
            line(arc(cx, 7.25, 1.5, 90, 360)),
        ]
    return parts


# ============================================================================ dolls, plush and toys

def thin(d, w=1.1):
    """Thin mark (letters, small details): solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", path_to_d(ST(d, w, "butt", "miter")))


@icon("rag-doll", CAT, "Soft doll with yarn hair, button eyes and a simple dress with stitched arms and legs",
      tags=["cloth doll", "soft doll", "yarn hair", "handmade toy", "doll", "plush"])
def _(S):
    head = union(circle(12, 6.5, 3.5), circle(7.25, 6.5, 1.75), circle(16.75, 6.5, 1.75))
    return [
        shell(head),
        dot(10.75, 6.25, 0.8),
        dot(13.25, 6.25, 0.8),
        shell(poly([(9.5, 12.5), (14.5, 12.5), (17.5, 19), (6.5, 19)], closed=True, r=S.r)),
        line(poly([(9.5, 13.5), (5, 15.5)], r=0)),
        line(poly([(14.5, 13.5), (19, 15.5)], r=0)),
        line(seg(9.5, 19, 9.5, 21.5)),
        line(seg(14.5, 19, 14.5, 21.5)),
    ]


@icon("baby-doll", CAT, "Baby doll face in a frilled bonnet with a pacifier button and a ribbon bow under the chin",
      tags=["doll", "baby toy", "nursery play", "pretend play", "toy baby", "bonnet"])
def _(S):
    return [
        shell(circle(12, 10.5, 7)),
        detail(arc(12, 10.5, 4.75, 195, 345)),
        dot(9.75, 11.5, 0.85),
        dot(14.25, 11.5, 0.85),
        dot(12, 14.25, 1.1),
        solid(poly([(12, 20.5), (7.75, 18.25), (7.75, 22.5)], closed=True)),
        solid(poly([(12, 20.5), (16.25, 18.25), (16.25, 22.5)], closed=True)),
    ]


@icon("kokeshi-doll", CAT, "Wooden doll with a cylinder body and a large round head with painted hair",
      tags=["japanese doll", "wooden doll", "folk toy", "peg doll", "traditional toy", "souvenir"])
def _(S):
    body = union(circle(12, 7.5, 5.5), poly([(7.5, 11), (16.5, 11), (16.5, 21), (7.5, 21)], closed=True, r=S.r))
    return [
        shell(body),
        detail(arc(12, 7.5, 3.75, 200, 340)),
        dot(10.25, 9, 0.85),
        dot(13.75, 9, 0.85),
        detail(seg(7.5, 16.5, 16.5, 16.5)),
    ]


@icon("paper-dolls", CAT, "Chain of three joined paper figures holding hands, cut from folded paper",
      tags=["paper chain", "cutout dolls", "paper cut", "craft", "kids craft", "folded paper"])
def _(S):
    bodies = [poly([(c - 1.5, 10), (c + 1.5, 10), (c + 2.75, 20.5), (c - 2.75, 20.5)], closed=True) for c in (5.5, 12, 18.5)]
    bridge = rect(5.5, 12, 13, 2)
    return [
        shell(union(*bodies, bridge)),
        shell(circle(5.5, 6, 2)),
        shell(circle(12, 6, 2)),
        shell(circle(18.5, 6, 2)),
    ]


@icon("action-figure", CAT, "Small posable figure with visible joints at shoulders and knees, standing in a heroic pose",
      tags=["toy figure", "superhero toy", "collectible", "poseable", "boys toy", "figurine"])
def _(S):
    return [
        shell(circle(12, 4.75, 2.25)),
        shell(poly([(8, 8.5), (16, 8.5), (14.5, 14.5), (9.5, 14.5)], closed=True, r=S.r)),
        line(poly([(8, 9.5), (5, 12), (8.75, 13.5)], r=S.r * 0.6)),
        line(poly([(16, 9.5), (19, 12), (15.25, 13.5)], r=S.r * 0.6)),
        line(poly([(10.25, 14.5), (9.5, 18), (9.75, 21.5)], r=S.r * 0.6)),
        line(poly([(13.75, 14.5), (14.5, 18), (14.25, 21.5)], r=S.r * 0.6)),
        detail(seg(9.75, 12.5, 14.25, 12.5)),
    ]


@icon("toy-soldier", CAT, "Wooden toy soldier with a tall hat, round face and a belted coat",
      tags=["nutcracker", "wooden soldier", "tin soldier", "christmas toy", "military toy", "figurine"])
def _(S):
    head = union(rect(8.75, 2.5, 6.5, 5, rr(S, 1.5)), rect(7.5, 6.5, 9, 1.5, 0), circle(12, 10.5, 2.75))
    return [
        shell(head),
        dot(10.9, 10.25, 0.8),
        dot(13.1, 10.25, 0.8),
        shell(rect(7.5, 14.5, 9, 7, rr(S, 1.5))),
        detail(poly([(8.5, 15.5), (15.5, 20.5)])),
    ]


@icon("stuffed-bunny", CAT, "Plush rabbit sitting with long floppy ears and stitched seams",
      tags=["plush rabbit", "bunny toy", "soft toy", "easter bunny", "cuddly toy", "stuffed animal"])
def _(S):
    body = union(circle(12, 9.5, 4), ellipse(12, 17, 5.75, 4.5),
                 rect(7.25, 2.5, 3.25, 8, 1.6), rect(13.5, 2.5, 3.25, 8, 1.6))
    return [
        shell(body),
        dot(10.5, 9.25, 0.8),
        dot(13.5, 9.25, 0.8),
        dot(12, 11.25, 0.8),
        detail(seg(12, 14.5, 12, 19.5)),
    ]


@icon("sock-monkey", CAT, "Plush monkey face made from a sock with a heel colored mouth patch and round ears",
      tags=["sock toy", "handmade toy", "monkey toy", "plush monkey", "stitched toy", "stuffed animal"])
def _(S):
    head = union(circle(12, 11, 6.5), circle(4.5, 11.5, 2.5), circle(19.5, 11.5, 2.5))
    return [
        shell(head),
        detail("M7.5 8.25C10 6.5 14 6.5 16.5 8.25"),
        detail(ellipse(12, 14.5, 3.5, 2.25)),
        dot(9.75, 11, 0.85),
        dot(14.25, 11, 0.85),
    ]


@icon("baby-rattle", CAT, "Handle with a round head holding beads and short shake lines around it",
      tags=["rattle", "shaker", "baby toy", "infant toy", "newborn gift", "noise maker"])
def _(S):
    return [
        shell(circle(9.5, 9.5, 5.5)),
        dot(8, 8.25, 1),
        dot(11.5, 8.75, 1),
        dot(9.5, 11.75, 1),
        line(seg(13.4, 13.4, 16.8, 16.8)),
        shell(circle(18.5, 18.5, 2.25)),
        line(seg(15, 4.5, 17.5, 2.5)),
        line(seg(17.5, 8, 20.5, 7)),
        line(seg(3, 15.5, 4, 18)),
    ]


@icon("toy-keys", CAT, "Ring holding three chunky plastic keys of different shapes fanned out from it",
      tags=["baby keys", "toy keys", "teething keys", "pretend play", "infant toy", "rattle keys"])
def _(S):
    px, py = 7.25, 7.25
    cap_a = rot(rect(px, py - 2, 13.25, 4, 2), 8, px, py)
    cap_b = rot(rect(px, py - 2, 13.5, 4, L(S, 0.5, 2)), 45, px, py)
    cap_c = rot(rect(px, py - 2, 13.25, 4, 2), 82, px, py)
    ringc = P(circle(px, py, 3.5))

    def grow(d, g):
        return U(P(d), ST(d, 2 * g, "round", "round"))
    front_b = grow(cap_b, 2.5)
    front_r = U(ringc, ST(circle(px, py, 3.5), 2 * 2.5, "round", "round"))
    a = path_to_d(D(P(cap_a), front_b, front_r))
    c = path_to_d(D(P(cap_c), front_b, front_r))
    b = path_to_d(D(P(cap_b), front_r))
    holes = [dot(*pt_on(px, py, 11, ang), 0.8) for ang in (8, 45, 82)]
    return [
        shell(a), shell(b), shell(c),
        shell(circle(px, py, 3.5)),
        dot(px, py, 1.1),
        *holes,
    ]


@icon("cloth-book", CAT, "Soft padded book with rounded corners and stitched page edges",
      tags=["soft book", "fabric book", "baby book", "crinkle book", "quiet book", "infant toy"])
def _(S):
    return [
        shell(rect(4, 3, 16, 18, L(S, 3, 5.5))),
        detail(seg(8.5, 3, 8.5, 21)),
        detail(circle(14.25, 9.75, 2.5)),
        detail(seg(11.75, 16.5, 16.75, 16.5)),
    ]


@icon("pop-up-book", CAT, "Open book with a paper house and tree standing up from the pages",
      tags=["pop up", "3d book", "storybook", "paper engineering", "picture book", "reading"])
def _(S):
    return [
        shell(poly([(3, 12), (12, 14.5), (21, 12), (21, 19.5), (12, 21.5), (3, 19.5)], closed=True, r=S.r)),
        detail(seg(12, 14.5, 12, 21.5)),
        line(poly([(5, 12.5), (5, 8), (7.75, 5), (10.5, 8), (10.5, 13.5)], r=S.r * 0.5)),
        line(seg(16.5, 14, 16.5, 9)),
        shell(circle(16.5, 6.25, 3)),
    ]


@icon("sensory-ball", CAT, "Ball covered in raised knobs and bumps all around its surface",
      tags=["textured ball", "spiky ball", "bumpy ball", "sensory toy", "baby ball", "infant toy"])
def _(S):
    bumps = [circle(*pt_on(12, 12, 8, a), 1.5) for a in range(15, 375, 60)]
    body = union(circle(12, 12, 7.5), *bumps)
    parts = [shell(body), dot(12, 12, 1.1)]
    for a in range(-90, 270, 60):
        x, y = pt_on(12, 12, 4.1, a)
        parts.append(dot(x, y, 1.1))
    return parts


@icon("toy-blocks", CAT, "Three stacked wooden cubes showing the letters A, B and C",
      tags=["abc blocks", "alphabet blocks", "wooden blocks", "building blocks", "letter blocks", "toddler toy"])
def _(S):
    body = union(rect(3, 12.5, 18, 9, L(S, 0.5, 2.5)), rect(7.5, 3.5, 9, 9, L(S, 0.5, 2.5)))
    return [
        shell(body),
        detail(seg(12, 12.5, 12, 21.5)),
        detail(seg(7.5, 12.5, 16.5, 12.5)),
        thin("M5.9 19.4L7.5 14.8L9.1 19.4M6.4 18H8.6"),
        thin("M14.1 14.7V19.3H15.5A1.2 1.2 0 0 0 15.5 17H14.1M15.5 17A1.1 1.1 0 0 0 15.5 14.7H14.1"),
        thin("M13.6 6.2A2.1 2.1 0 1 0 13.6 9.8"),
    ]


@icon("toy-bricks", CAT, "Interlocking building brick with round studs on top",
      tags=["building brick", "construction toy", "snap bricks", "block", "stud", "kids toy"])
def _(S):
    body = union(rect(3, 10.5, 18, 10, rr(S, 2)), rect(4.5, 6.5, 3.5, 4.5, rr(S, 1.25)),
                 rect(10.25, 6.5, 3.5, 4.5, rr(S, 1.25)), rect(16, 6.5, 3.5, 4.5, rr(S, 1.25)))
    return [
        shell(body),
        detail(seg(3, 17, 21, 17)),
    ]


# ============================================================================ games and people

def grown(d, g=2.5):
    """Region of d expanded by g (for cutting a clear gap around a front shape)."""
    return U(P(d), ST(d, 2 * g, "round", "round"))


@icon("peekaboo", CAT, "Round child face with two small hands covering the eyes",
      tags=["peek a boo", "baby game", "hiding face", "playing", "infant play", "surprise"])
def _(S):
    face = circle(12, 12.5, 9)
    hands = [rot(rect(4, 5.5, 7.5, 8, L(S, 2.5, 3.5)), -14, 7.75, 9.5), rot(rect(12.5, 5.5, 7.5, 8, L(S, 2.5, 3.5)), 14, 16.25, 9.5)]
    cut = U(*[grown(h, 1.75) for h in hands])
    return [
        shell(path_to_d(D(P(face), cut))),
        shell(hands[0]), shell(hands[1]),
        detail("M9.5 18Q12 20.25 14.5 18"),
    ]


@icon("piggyback-ride", CAT, "Adult figure walking with a small child riding on the back, arms around the shoulders",
      tags=["piggy back", "carry child", "parent and child", "fun", "family", "playtime"])
def _(S):
    adult = rot(rect(12, 8.5, 5, 7.5, 2.5), 10, 14.5, 12)
    child = rot(rect(5.5, 8.5, 3.5, 5.5, 1.75), 10, 7.25, 11)
    return [
        shell(circle(16, 4.75, 2.5)),
        shell(adult),
        shell(circle(7.5, 5.75, 1.9)),
        shell(child),
        line(seg(9.25, 9.25, 13, 8.75)),
        line(poly([(14.25, 16), (17.5, 18), (17, 21.5)], r=S.r * 0.6)),
        line(poly([(13.75, 16), (11.5, 18.5), (9.5, 21.5)], r=S.r * 0.6)),
    ]


@icon("hide-and-seek", CAT, "Tree trunk with a child peeking out from behind one side",
      tags=["hiding", "peeking", "kids game", "playground game", "outdoor play", "seek"])
def _(S):
    tree = union(circle(9.5, 8, 5.5), rect(7.25, 12, 4.5, 9.5, 0))
    kid = union(circle(16.5, 13.5, 2.5), rect(14.5, 16, 4.5, 5.5, rr(S, 1.5)))
    return [
        shell(tree),
        shell(path_to_d(D(P(kid), grown(tree, 2.25)))),
        dot(17.5, 13, 0.8),
    ]


@icon("snow-angel", CAT, "Figure lying flat with the wing and skirt shape swept into the snow around it",
      tags=["snow", "winter play", "angel", "lying in snow", "winter fun", "kids"])
def _(S):
    wing = "M10.5 9.5C6 8.5 3 11 3 15C6.5 14.5 9 13 10.5 11.5Z"
    body = union(wing, flip(wing), poly([(10.75, 8), (13.25, 8), (13.25, 13), (17, 21), (7, 21), (10.75, 13)], closed=True))
    return [
        shell(circle(12, 4.75, 2.25)),
        shell(body),
    ]


@icon("three-legged-race", CAT, "Two children side by side with their inner legs tied together by a band",
      tags=["sports day", "school race", "party game", "teamwork", "tied legs", "field day"])
def _(S):
    return [
        shell(circle(6.5, 4.75, 2.25)),
        shell(circle(17.5, 4.75, 2.25)),
        shell(rect(4.5, 8.5, 4, 6.5, 2)),
        shell(rect(15.5, 8.5, 4, 6.5, 2)),
        line(seg(8.5, 11, 15.5, 11)),
        line(seg(5.5, 15, 4.5, 21.5)),
        line(seg(18.5, 15, 19.5, 21.5)),
        line(poly([(7.5, 15), (10.75, 21.5)])),
        line(poly([(16.5, 15), (13.25, 21.5)])),
        dot(12, 20, 1.4),
    ]


@icon("sack-race", CAT, "Child jumping inside a tall sack held up at the waist",
      tags=["potato sack race", "jumping race", "sports day", "party game", "field day", "kids game"])
def _(S):
    return [
        shell(circle(12, 4.25, 2.25)),
        line(seg(12, 7, 12, 10)),
        line(poly([(12, 9), (6.5, 6)])),
        line(poly([(12, 9), (17.5, 6)])),
        shell(poly([(8, 10), (16, 10), (18, 21), (6, 21)], closed=True, r=S.r)),
        detail(seg(8.5, 13.5, 15.5, 13.5)),
    ]


@icon("egg-and-spoon-race", CAT, "Hand holding a long spoon with an egg balanced in the bowl, motion lines above",
      tags=["spoon race", "sports day", "balance game", "party game", "field day", "kids game"])
def _(S):
    return [
        shell(rect(2, 14.5, 5, 5, L(S, 1.5, 2.5))),
        line(poly([(7, 16.5), (11, 14.5)], r=0)),
        line("M10.5 13C10.5 17.5 13 20 16 20C19 20 21.5 17.5 21.5 13"),
        shell(ellipse(16, 10.25, 3, 4)),
        line(seg(3, 5.5, 7, 5.5)),
        line(seg(5.5, 9, 9, 9)),
    ]


# ============================================================================ toddler toys

@icon("magnetic-tiles", CAT, "Flat square and triangle frame tiles leaning together to form a small house",
      tags=["magnet tiles", "building tiles", "magna tiles", "stem toy", "construction toy", "kids building"])
def _(S):
    return [
        shell(poly([(3.5, 10.5), (12, 3), (20.5, 10.5)], closed=True, r=S.r)),
        dot(12, 8, 1),
        shell(rect(5, 13.5, 14, 8, rr(S, 1.5))),
        detail(rect(10, 16, 4, 3, 0)),
    ]


@icon("stacking-rings", CAT, "Cone post on a base with rings stacked from largest at the bottom to smallest at the top",
      tags=["ring stacker", "stacking toy", "baby toy", "toddler toy", "rings", "motor skills"])
def _(S):
    tiers = union(rect(9.25, 4.5, 5.5, 3.5, rr(S, 1.5)), rect(7.5, 8, 9, 3.5, rr(S, 1.5)),
                  rect(5.75, 11.5, 12.5, 3.5, rr(S, 1.5)), rect(4, 15, 16, 3.5, rr(S, 1.5)),
                  rect(3, 18.5, 18, 3, rr(S, 1.5)))
    return [
        shell(tiers),
        detail(seg(9.25, 8, 14.75, 8)),
        detail(seg(7.5, 11.5, 16.5, 11.5)),
        detail(seg(5.75, 15, 18.25, 15)),
    ]


@icon("shape-sorter", CAT, "Cube box with a circle, square and triangle hole in the lid",
      tags=["shape sorting", "shape box", "toddler toy", "learning toy", "posting toy", "early learning"])
def _(S):
    return [
        shell(poly([(3.5, 12), (7, 5.5), (20, 5.5), (16.5, 12)], closed=True, r=S.r)),
        shell(rect(3.5, 12, 13, 9.5, rr(S, 1.5))),
        shell(poly([(16.5, 12), (20, 5.5), (20, 15), (16.5, 21.5)], closed=True, r=S.r * 0.5)),
        dot(10, 8.75, 1.1),
        Part("dot", rect(13.1, 7.75, 2, 2, 0)),
        Part("dot", poly([(8, 16.5), (10, 13.5), (12, 16.5)], closed=True)),
    ]


@icon("stacking-cups", CAT, "Tower of upturned cups getting smaller toward the top",
      tags=["nesting cups", "stacking toy", "bath toy", "baby toy", "toddler toy", "cups"])
def _(S):
    cups = union(poly([(3, 21), (21, 21), (20, 14.5), (4, 14.5)], closed=True, r=S.r * 0.5),
                 poly([(6, 14.5), (18, 14.5), (17.25, 9), (6.75, 9)], closed=True, r=S.r * 0.5),
                 poly([(8.5, 9), (15.5, 9), (14.9, 4.5), (9.1, 4.5)], closed=True, r=S.r * 0.5))
    return [
        shell(cups),
        detail(seg(4, 14.5, 20, 14.5)),
        detail(seg(6.5, 9, 17.5, 9)),
    ]


@icon("rainbow-stacker", CAT, "Set of nested arches standing upright, each arch inside a larger one",
      tags=["rainbow toy", "wooden rainbow", "stacking arches", "waldorf toy", "toddler toy", "nesting arches"])
def _(S):
    return [
        line("M3 21.5V12A9 9 0 0 1 21 12V21.5"),
        line("M7.5 21.5V12.5A4.5 4.5 0 0 1 16.5 12.5V21.5"),
        shell(f"M10.75 21.5V14.25A1.25 1.25 0 0 1 13.25 14.25V21.5Z"),
    ]


@icon("bead-maze", CAT, "Looping wire tracks on a wooden base with beads threaded along them",
      tags=["bead track", "wire maze", "roller coaster toy", "toddler toy", "sensory", "fine motor"])
def _(S):
    return [
        shell(rect(3, 18, 18, 3.5, L(S, 0.5, 1.75))),
        line("M5 18C5 5 14.5 5 14.5 18"),
        line("M9.5 18C9.5 8 19.5 8 19.5 18"),
        solid(circle(5.6, 11.5, 1.9)),
        solid(circle(9.5, 8.1, 1.9)),
        solid(circle(14.5, 10.4, 1.9)),
        solid(circle(18.5, 12.9, 1.9)),
    ]


@icon("busy-board", CAT, "Board with a latch, a toggle switch, a spinning wheel and a small zipper mounted on it",
      tags=["sensory board", "activity board", "montessori", "toddler toy", "fidget board", "learning toy"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(rect(5.5, 5.5, 6, 3, 1.5)),
        dot(8.5, 7, 0.9),
        detail(circle(16.5, 7.5, 2.25)),
        dot(16.5, 7.5, 0.9),
        detail(seg(5.5, 16, 10.5, 16)),
        dot(11, 16, 0.9),
        detail(seg(16.5, 13.5, 16.5, 19.5)),
    ]


@icon("pounding-bench", CAT, "Low bench with round pegs sticking up and a toy mallet beside it",
      tags=["hammer bench", "pound a peg", "toddler toy", "peg hammering", "wooden toy", "motor skills"])
def _(S):
    return [
        shell(rect(2.5, 12, 12.5, 4.5, rr(S, 1.5))),
        shell(rect(4, 6.5, 3.5, 5.5, 1.75)),
        shell(rect(10, 6.5, 3.5, 5.5, 1.75)),
        line(seg(4.5, 16.5, 4.5, 21.5)),
        line(seg(13, 16.5, 13, 21.5)),
        shell(rect(17, 3.5, 5, 5, rr(S, 1.5))),
        line(seg(19.5, 8.5, 19.5, 21.5)),
    ]


@icon("peg-puzzle", CAT, "Wooden tray with shaped cut-outs and one piece lifted by a small peg knob",
      tags=["knob puzzle", "wooden puzzle", "shape puzzle", "toddler puzzle", "learning toy", "first puzzle"])
def _(S):
    return [
        shell(rect(3, 11, 18, 10.5, rr(S, 2.5))),
        detail(circle(8, 16.25, 2.25)),
        detail(rect(13, 14, 5, 4.5, 0)),
        shell(poly([(12, 2.5), (16.5, 8), (7.5, 8)], closed=True, r=S.r * 0.5)),
        dot(12, 6.1, 0.8),
    ]


@icon("roly-poly-toy", CAT, "Round bottomed tumbler toy with a smaller head, tilted with rocking lines beside it",
      tags=["weeble", "wobbler", "tumbler toy", "rocking toy", "baby toy", "wobble toy"])
def _(S):
    body = union(circle(11.5, 14.5, 6.5), circle(14.75, 5.75, 3.25))
    return [
        shell(body),
        dot(13.75, 5.5, 0.8),
        dot(16, 5.5, 0.8),
        line(arc(11.5, 14.5, 9.5, 155, 205)),
        line(arc(11.5, 14.5, 9.5, -10, 25)),
    ]


@icon("jack-in-the-box", CAT, "Box with a crank handle on the side and a clown head springing out on a coil",
      tags=["jack in a box", "clown toy", "surprise toy", "music box", "pop up toy", "crank toy"])
def _(S):
    return [
        shell(rect(3, 13, 15, 8.5, rr(S, 1.5))),
        line(poly([(18, 17), (21, 17), (21, 14)], r=S.r * 0.5)),
        dot(21, 13.25, 1.25),
        line(poly([(10.5, 13), (8, 11.5), (13, 10.25), (10.5, 9)], r=0)),
        shell(circle(10.5, 5.75, 3.25)),
        dot(9.5, 5.25, 0.7),
        dot(11.5, 5.25, 0.7),
        line(poly([(3, 13), (3, 9)], r=0)),
    ]
