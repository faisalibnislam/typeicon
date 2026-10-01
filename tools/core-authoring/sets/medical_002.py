"""TypeIcon Core: medical equipment (batch medical_002).

Orthopedic supports, prosthetics, mobility and toileting aids, dental and surgical instruments and
theatre equipment, drawn from the objects themselves. Long instruments lean on one diagonal.
"""
import math

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, polar  # noqa: F401

CAT = "medical"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def xf(d, matrix):
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, matrix))
    return pen.getCommands()


def rot(d, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return xf(d, (c, s, -s, c, cx - c * cx + s * cy, cy - s * cx - c * cy))


def axis(origin, deg):
    """Local frame: x runs along `deg` (0 = right, positive = clockwise on screen)."""
    ox, oy = origin
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return lambda x, y: (ox + x * c - y * s, oy + x * s + y * c)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def stadium(m, x0, x1, h, rx):
    """Closed rounded bar in a local frame m, from x0 to x1, half-height h, corner radius rx."""
    k = 0.5523 * rx
    pts = [
        ("M", m(x0 + rx, -h)), ("L", m(x1 - rx, -h)),
        ("C", m(x1 - rx + k, -h), m(x1, -h + rx - k), m(x1, -h + rx)), ("L", m(x1, h - rx)),
        ("C", m(x1, h - rx + k), m(x1 - rx + k, h), m(x1 - rx, h)), ("L", m(x0 + rx, h)),
        ("C", m(x0 + rx - k, h), m(x0, h - rx + k), m(x0, h - rx)), ("L", m(x0, -h + rx)),
        ("C", m(x0, -h + rx - k), m(x0 + rx - k, -h), m(x0 + rx, -h)),
    ]
    out = ""
    for cmd, *ps in pts:
        out += cmd + " ".join(f"{fmt(x)} {fmt(y)}" for x, y in ps)
    return out + "Z"


def mseg(m, x0, y0, x1, y1):
    return seg(*m(x0, y0), *m(x1, y1))


def mpoly(m, pts, closed=False, r=0.0):
    return poly([m(x, y) for x, y in pts], closed=closed, r=r)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


# ============================================================================ orthopedic supports

@icon("external-fixator", CAT, "Lower leg with two rings around it joined by side rods",
      tags=["ilizarov", "bone fixation", "fracture", "orthopedic", "frame", "leg", "surgery"])
def _(S):
    return [
        shell(rect(9, 2.5, 6, 19, L(S, 1.5, 3))),
        line(rect(3.5, 7, 17, 10, L(S, 0, 1.5))),
    ]


@icon("iud", CAT, "Small T-shaped intrauterine device with a thin string at the base",
      tags=["coil", "contraception", "birth control", "intrauterine", "gynecology", "family planning"])
def _(S):
    return [
        line(poly([(4.5, 9), (6, 6), (12, 5.5), (18, 6), (19.5, 9)], r=L(S, 0, 2))),
        shell(rect(10, 6, 4, 10, L(S, 0.5, 2))),
        line(poly([(12, 16), (10.5, 18), (13.5, 19.5), (12, 21.5)], r=L(S, 0, 1.5))),
    ]


@icon("leg-cast", CAT, "Leg in a plaster cast with the toes showing at the end of the foot",
      tags=["plaster cast", "broken leg", "fracture", "orthopedic", "injury", "bone"])
def _(S):
    body = [(6.5, 2.5), (15.5, 2.5), (15.5, 15), (19, 15), (19, 21.5), (6.5, 21.5)]
    return [
        shell(poly(body, closed=True, r=S.r)),
        detail(seg(6.5, 7, 15.5, 7)),
        detail(seg(6.5, 11, 15.5, 11)),
        solid(circle(21.75, 16.75, 0.9)),
        solid(circle(21.75, 19.25, 0.9)),
    ]


@icon("walking-boot", CAT, "Tall rigid walking boot with three wide fastening straps",
      tags=["cam boot", "orthopedic boot", "fracture boot", "foot injury", "ankle", "recovery"])
def _(S):
    body = [(6.5, 2.5), (15.5, 2.5), (15.5, 14), (21.5, 16.5), (21.5, 21.5), (6.5, 21.5)]
    return [
        shell(poly(body, closed=True, r=S.r)),
        detail(seg(6.5, 6, 15.5, 6)),
        detail(seg(6.5, 10, 15.5, 10)),
        detail(seg(6.5, 17.5, 21.5, 17.5)),
    ]


@icon("knee-brace", CAT, "Leg with a wide knee sleeve that has an open circle over the kneecap and side hinges",
      tags=["knee support", "patella", "sports injury", "orthopedic", "ligament", "recovery"])
def _(S):
    return [
        line(poly([(8.5, 2.5), (8.5, 7)])), line(poly([(15.5, 2.5), (15.5, 7)])),
        line(poly([(8.5, 17), (8.5, 21.5)])), line(poly([(15.5, 17), (15.5, 21.5)])),
        shell(rect(4.5, 7, 15, 10, L(S, 1.5, 3))),
        detail(circle(12, 12, 2.25)),
    ]


@icon("back-brace", CAT, "Wide corset-style back belt with two vertical stays and a row of front fasteners",
      tags=["lumbar support", "back support", "spine", "corset", "orthopedic", "posture"])
def _(S):
    body = [(4, 3.5), (20, 3.5), (18, 12), (20, 20.5), (4, 20.5), (6, 12)]
    return [
        shell(poly(body, closed=True, r=S.r)),
        detail(seg(8.5, 7, 8.5, 17)),
        detail(seg(15.5, 7, 15.5, 17)),
        dot(12, 8, 1.1), dot(12, 12, 1.1), dot(12, 16, 1.1),
    ]


@icon("wrist-brace", CAT, "Wrist support around the hand and forearm with a thumb hole and two straps",
      tags=["wrist splint", "carpal tunnel", "sprain", "hand support", "orthopedic", "tendon"])
def _(S):
    hand = [(7, 21.5), (7, 11), (8, 4.5), (16, 4.5), (17, 11), (17, 21.5)]
    return [
        shell(poly(hand, closed=True, r=L(S, 0, 2.5))),
        detail(circle(12, 9, 1.75)),
        detail(seg(7, 15.5, 17, 15.5)),
        detail(seg(7, 19, 17, 19)),
        line(seg(17, 15.5, 20.5, 15.5)),
        line(seg(17, 19, 20.5, 19)),
    ]


@icon("ankle-brace", CAT, "Lace-up ankle support sleeve with a figure eight strap across the ankle",
      tags=["ankle support", "sprain", "lace up", "sports injury", "foot", "orthopedic"])
def _(S):
    body = [(7, 4), (15.5, 4), (15.5, 13), (21.5, 16), (21.5, 21.5), (7, 21.5)]
    return [
        shell(poly(body, closed=True, r=S.r)),
        detail(seg(7, 8, 15.5, 13)),
        detail(seg(15.5, 8, 7, 13)),
        detail(seg(7, 18, 21.5, 18)) if False else detail(seg(11.5, 17, 21.5, 17)),
    ]


@icon("cervical-collar", CAT, "Head and shoulders with a rigid collar band around the neck",
      tags=["neck brace", "whiplash", "spine injury", "trauma", "neck support", "emergency"])
def _(S):
    return [
        shell(circle(12, 6.5, 3.75)),
        shell(rect(7.5, 12, 9, 4.5, L(S, 1.5, 2.25))),
        line("M3 21.5Q3.5 18 8 17") if S.name == "rounded" else line(poly([(3, 21.5), (3.5, 18), (8, 17)])),
        line("M21 21.5Q20.5 18 16 17") if S.name == "rounded" else line(poly([(21, 21.5), (20.5, 18), (16, 17)])),
    ]


@icon("finger-splint", CAT, "Straight finger held against a rigid splint with two tape bands",
      tags=["finger brace", "jammed finger", "fracture", "hand injury", "tape", "first aid"])
def _(S):
    return [
        shell(rect(6, 2.5, 7, 19, L(S, 3, 3.5))),
        detail(seg(6, 8, 13, 8)),
        detail(seg(6, 15.5, 13, 15.5)),
        line(seg(17.5, 4.5, 17.5, 19.5)),
        line(seg(13, 8, 17.5, 8)), line(seg(13, 15.5, 17.5, 15.5)),
    ]


@icon("arm-sling", CAT, "Triangular cloth sling cradling a forearm with its hand showing and a strap over the neck",
      tags=["broken arm", "shoulder injury", "first aid", "support", "fracture", "recovery"])
def _(S):
    cl = poly([(3, 11.5), (21, 11.5), (21, 14), (9, 21)], closed=True, r=S.r)
    return [
        shell(cl),
        shell(rect(15.5, 5.5, 5, 6, L(S, 1.5, 2.5))),
        line(poly([(4, 11.5), (7, 4), (12, 3)], r=S.r)),
    ]


@icon("traction", CAT, "Raised leg in a cast hanging from a cord over a pulley with a weight",
      tags=["orthopedic traction", "fracture", "hospital", "leg", "pulley", "bed rest"])
def _(S):
    m = axis((3.5, 18.5), -28)
    return [
        shell(stadium(m, 0, 11, 2.5, L(S, 1, 2.5))),
        line(poly([(14.5, 10.5), (18, 5.5)])),
        shell(circle(18.5, 5, 1.6)),
        line(poly([(20.1, 5), (20.1, 15)])),
        shell(rect(18, 15, 4.2, 5.5, L(S, 0.5, 1.8))),
    ]


@icon("compression-stocking", CAT, "Knee-high compression stocking with a ribbed top band and an open toe",
      tags=["support hose", "varicose veins", "circulation", "dvt", "leg", "medical sock"])
def _(S):
    body = [(7, 2.5), (16, 2.5), (15, 13.5), (15, 15), (21, 18.5), (21, 21.5), (7, 21.5)]
    return [
        shell(poly(body, closed=True, r=S.r)),
        detail(seg(7, 6, 16, 6)),
        detail(seg(11, 10, 14.5, 10)),
        detail(seg(11, 13.3, 14.5, 13.3)) if False else detail(seg(16.5, 21.5, 16.5, 17.8)),
    ]


@icon("prosthetic-leg", CAT, "Prosthetic leg with a socket cup, a slim pylon and a foot",
      tags=["artificial leg", "amputee", "limb", "below knee", "rehabilitation", "disability"])
def _(S):
    socket = [(7, 2.5), (17, 2.5), (15.5, 10.5), (8.5, 10.5)]
    foot = [(9.5, 16.5), (14.5, 16.5), (14.5, 18), (20.5, 19), (20.5, 21.5), (9.5, 21.5)]
    return [
        shell(poly(socket, closed=True, r=S.r)),
        line(seg(12, 10.5, 12, 16.5)),
        shell(poly(foot, closed=True, r=S.r * 0.6)),
    ]


@icon("prosthetic-arm", CAT, "Prosthetic arm with a forearm socket and a mechanical hand with jointed fingers",
      tags=["artificial arm", "bionic", "amputee", "limb", "robotic hand", "disability"])
def _(S):
    socket = [(7.5, 21.5), (16.5, 21.5), (15.5, 14.5), (8.5, 14.5)]
    return [
        shell(poly(socket, closed=True, r=S.r)),
        shell(rect(6, 10, 12, 4.5, L(S, 1, 2))),
        line(seg(8.25, 10, 8.25, 5)), line(seg(12, 10, 12, 2.5)), line(seg(15.75, 10, 15.75, 4.5)),
        line(seg(6, 11.5, 3, 8)),
    ]


@icon("running-blade", CAT, "Running blade prosthesis with a socket on top curving into a long J-shaped blade",
      tags=["sports prosthesis", "carbon fiber", "paralympic", "amputee", "athlete", "artificial leg"])
def _(S):
    socket = [(5.5, 2.5), (13.5, 2.5), (12.5, 9.5), (6.5, 9.5)]
    return [
        shell(poly(socket, closed=True, r=S.r)),
        line("M9.5 9.5V13Q9.5 20.5 20.5 20.5") if S.name == "rounded" else line(poly([(9.5, 9.5), (9.5, 14), (13, 19.5), (21.5, 20.5)], r=3)),
        line(seg(9.5, 13, 9.5, 14)) if False else line(seg(18.5, 17.5, 21.5, 17.5)) if False else line(seg(20.5, 20.5, 21.5, 20.5)),
    ]


@icon("exoskeleton", CAT, "Pair of legs in a powered frame with a waist belt and round motor joints at the knees",
      tags=["powered orthosis", "walking aid", "paralysis", "rehabilitation", "robotic legs", "mobility"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 4.5, L(S, 1, 2))),
        line(poly([(8, 7), (8, 11.5)])), line(poly([(16, 7), (16, 11.5)])),
        shell(circle(8, 14, 2.5)), shell(circle(16, 14, 2.5)),
        line(poly([(8, 16.5), (8, 21.5), (11.5, 21.5)], r=S.r * 0.6)),
        line(poly([(16, 16.5), (16, 21.5), (19.5, 21.5)], r=S.r * 0.6)),
    ]


@icon("quad-cane", CAT, "Walking cane with an offset handle and a wide base with four short feet",
      tags=["walking stick", "four point cane", "mobility aid", "elderly", "balance", "rehabilitation"])
def _(S):
    return [
        line(poly([(12, 16.5), (12, 6), (11, 3), (7, 2.5), (4.5, 4)], r=S.r * 1.3)) if S.name == "rounded" else line(poly([(12, 16.5), (12, 3), (4, 3)])),
        line(seg(4, 16.5, 20, 16.5)),
        line(seg(4, 16.5, 4, 21.5)), line(seg(8.5, 16.5, 8.5, 21.5)),
        line(seg(15.5, 16.5, 15.5, 21.5)), line(seg(20, 16.5, 20, 21.5)),
    ]


@icon("forearm-crutch", CAT, "Forearm crutch with a straight shaft, a hand grip and an open cuff at the top",
      tags=["elbow crutch", "canadian crutch", "walking aid", "mobility", "injury", "disability"])
def _(S):
    parts = [
        line(arc(11, 6.5, 4.75, 60, 300)),
        line(seg(11, 11.25, 11, 21.5)),
        shell(rect(11, 13.5, 7, 3.5, L(S, 1, 1.75))),
    ]
    for p_ in parts:
        p_.d = rot(p_.d, 14)
    return parts


@icon("knee-scooter", CAT, "Knee scooter with a padded knee platform, a low frame, small wheels and a handlebar",
      tags=["knee walker", "leg scooter", "foot injury", "mobility aid", "recovery", "broken ankle"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 10, 4, L(S, 1, 2))),
        line(seg(7.5, 9.5, 7.5, 15.5)),
        line(seg(7.5, 15.5, 18.5, 15.5)),
        line(seg(18.5, 3, 18.5, 15.5)),
        line(seg(15, 3, 21.5, 3)),
        shell(circle(7.5, 19.25, 2.25)), shell(circle(18.5, 19.25, 2.25)),
    ]


@icon("mobility-scooter", CAT, "Mobility scooter from the side with a seat and backrest, a long base, wheels and a front tiller",
      tags=["electric scooter", "disability scooter", "elderly", "motorized", "accessibility", "transport"])
def _(S):
    return [
        line(poly([(4.5, 3), (4.5, 9.5), (12, 9.5)], r=S.r)),
        shell(rect(3, 12.5, 17, 4, L(S, 1, 2))),
        line(poly([(17, 12.5), (18, 6), (21, 6)], r=S.r)),
        shell(circle(6.5, 19.5, 2)), shell(circle(17, 19.5, 2)),
    ]


@icon("power-wheelchair", CAT, "Power wheelchair from the side with a padded seat, a joystick, big rear wheel and a small front caster",
      tags=["electric wheelchair", "motorized wheelchair", "disability", "mobility", "accessibility", "joystick"])
def _(S):
    return [
        line(poly([(4.5, 2.5), (5, 11), (14, 11), (18, 17)], r=S.r)),
        shell(circle(9.5, 16.5, 4.5)),
        line(seg(9, 6.5, 14, 6.5)),
        line(seg(14, 6.5, 14, 3.5)),
        shell(circle(19, 19.75, 1.75)),
    ]


@icon("sports-wheelchair", CAT, "Sports wheelchair from the front with a low seat between two big wheels tilted inward",
      tags=["racing wheelchair", "basketball wheelchair", "paralympic", "athlete", "adaptive sport", "camber"])
def _(S):
    return [
        shell(rot(ellipse(4.5, 13.5, 2.25, 8.5), 16, 4.5, 13.5)),
        shell(rot(ellipse(19.5, 13.5, 2.25, 8.5), -16, 19.5, 13.5)),
        line(poly([(9, 6), (9, 14), (15, 14), (15, 6)], r=S.r)),
        line(seg(7, 18.5, 17, 18.5)),
    ]


@icon("patient-lift", CAT, "Patient hoist with a wheeled base, a tall mast and a boom holding a hanging sling",
      tags=["hoist", "transfer lift", "hoyer lift", "caregiving", "nursing", "mobility"])
def _(S):
    return [
        line(poly([(8, 18.5), (8, 3.5), (21, 3.5)], r=S.r)),
        line(seg(3.5, 18.5, 14, 18.5)),
        dot(4.5, 21, 1.5), dot(13, 21, 1.5),
        line(seg(16.5, 3.5, 16.5, 8.5)), line(seg(20.5, 3.5, 20.5, 8.5)),
        shell(poly([(14.5, 8.5), (22, 8.5), (20.5, 14.5), (16, 14.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("transfer-board", CAT, "Long flat slide board with two hand slots bridging a wheelchair seat and a bed",
      tags=["slide board", "patient transfer", "wheelchair", "caregiving", "mobility aid", "bed"])
def _(S):
    return [
        shell(rect(2.5, 8, 19, 6, L(S, 1.5, 3))),
        sq(6, 10, 4, 2, 1), sq(14, 10, 4, 2, 1),
        line(seg(4, 14, 4, 20.5)), line(seg(20, 14, 20, 20.5)),
    ]


@icon("parallel-bars", CAT, "Rehab parallel bars on posts with a person walking between the two rails",
      tags=["walking rehab", "physiotherapy", "gait training", "physical therapy", "handrail", "recovery"])
def _(S):
    return [
        line(seg(2.5, 10, 21.5, 10)), line(seg(2.5, 14, 21.5, 14)),
        line(seg(3.5, 14, 3.5, 21.5)), line(seg(20.5, 14, 20.5, 21.5)),
        shell(circle(12, 4.5, 2)),
        line(seg(12, 8, 12, 15)),
        line(poly([(9, 21.5), (12, 15), (15, 21.5)])),
    ]


@icon("raised-toilet-seat", CAT, "Raised toilet seat riser with two side armrests",
      tags=["toilet riser", "bathroom aid", "elderly", "mobility", "accessibility", "commode"])
def _(S):
    body = union(ellipse(12, 11, 6.5, 4), rect(5.5, 11, 13, 9, L(S, 1.5, 3)))
    return [
        shell(body),
        detail(ellipse(12, 10.5, 3, 1.5)) if False else detail(ellipse(12, 10.5, 3.25, 1.75)),
        line(poly([(2.5, 3.5), (2.5, 15.5), (5.5, 15.5)], r=S.r * 0.6)),
        line(poly([(21.5, 3.5), (21.5, 15.5), (18.5, 15.5)], r=S.r * 0.6)),
    ]


@icon("commode-chair", CAT, "Bedside commode chair with armrests, an open seat and a bucket underneath",
      tags=["toilet chair", "bedside commode", "bathroom aid", "elderly", "caregiving", "accessibility"])
def _(S):
    return [
        line(poly([(5, 21.5), (5, 3), (19, 3), (19, 21.5)], r=S.r)),
        shell(rect(5, 10.5, 14, 3.5, L(S, 0.5, 1.75))),
        shell(rect(8.5, 14, 7, 5.5, L(S, 0.5, 2))),
    ]


@icon("bedpan", CAT, "Flat oval bedpan with a wide rim and a short handle at one end",
      tags=["hospital", "toileting", "bed rest", "patient care", "nursing", "elimination"])
def _(S):
    body = union(ellipse(9.5, 12, 7, 8.5), rect(14, 9.5, 7.5, 5, L(S, 1, 2.5)))
    return [
        shell(body),
        detail(ellipse(9.5, 12, 3.25, 5)),
    ]


@icon("urinal-bottle", CAT, "Urinal bottle lying on its side with an angled neck opening and a top handle",
      tags=["male urinal", "hospital", "bedridden", "patient care", "nursing", "toileting"])
def _(S):
    body = union(rect(3, 9, 13.5, 10, L(S, 1.5, 4)), poly([(15, 10), (20, 6.5), (22, 9.5), (16, 15)], closed=True, r=S.r * 0.4))
    return [
        shell(body),
        line(poly([(6, 9), (6, 5), (11.5, 5), (11.5, 9)], r=S.r)),
        detail(seg(7, 13, 12, 13)),
    ]


# ============================================================================ daily living aids

@icon("reacher-grabber", CAT, "Reacher grabber with a long pole, a trigger grip at one end and small jaws at the other",
      tags=["grabber", "pickup tool", "reaching aid", "mobility aid", "elderly", "daily living"])
def _(S):
    m = axis((4.5, 19.5), -45)
    return [
        shell(stadium(m, -1.5, 6, 2.5, L(S, 1, 2.5))),
        line(mpoly(m, [(1.5, 2.5), (1.5, 5.5)])),
        line(mseg(m, 6, 0, 17, 0)),
        line(mpoly(m, [(17, 0), (20.5, -3)], r=0)),
        line(mpoly(m, [(17, 0), (20.5, 3)], r=0)),
    ]


@icon("adaptive-spoon", CAT, "Spoon with a thick padded handle and a bent neck for easier gripping",
      tags=["eating aid", "built up handle", "arthritis", "tremor", "occupational therapy", "cutlery"])
def _(S):
    m = axis((3.5, 20.5), -45)
    cx, cy = m(17.5, -2.5)
    return [
        shell(stadium(m, -0.5, 8.5, 2.75, L(S, 1.25, 2.75))),
        line(mpoly(m, [(8.5, 0), (12, 0), (14, -2.5)], r=S.r)),
        shell(rot(ellipse(cx, cy, 4.25, 2.75), -45, cx, cy)),
    ]


@icon("hearing-trumpet", CAT, "Old ear trumpet with a wide bell that narrows to a small earpiece",
      tags=["ear horn", "hearing aid", "deaf", "hard of hearing", "antique", "sound amplifier"])
def _(S):
    m = axis((6, 17.5), -45)
    horn = [(0, -5.5), (14, -1.25), (14, 1.25), (0, 5.5)]
    return [
        shell(mpoly(m, horn, closed=True, r=S.r * 0.4)),
        line(mpoly(m, [(14, 0), (19, 0)])),
        detail(mseg(m, 7, -3.4, 7, 3.4)),
    ]


# ============================================================================ dental

@icon("dental-mirror", CAT, "Dental mirror with a slim handle ending in a small round mirror",
      tags=["dentist", "tooth exam", "oral exam", "mouth mirror", "dental tool", "checkup"])
def _(S):
    m = axis((3.5, 20.5), -45)
    cx, cy = m(17, 0)
    return [
        shell(stadium(m, -0.5, 7, 1.75, L(S, 0.75, 1.75))),
        line(mseg(m, 7, 0, 13, 0)),
        shell(circle(cx, cy, 4)),
    ]


@icon("dental-explorer", CAT, "Dental explorer probe with a grip handle and a thin shaft ending in a sharp curved hook",
      tags=["dentist", "probe", "cavity check", "tooth exam", "dental tool", "sickle probe"])
def _(S):
    m = axis((3.5, 20.5), -45)
    return [
        shell(stadium(m, -0.5, 8, 2.25, L(S, 1, 2.25))),
        detail(mseg(m, 2.5, -2.25, 2.5, 2.25)) if False else detail(mseg(m, 3, -2.25, 3, 2.25)),
        line(mpoly(m, [(8, 0), (15, 0), (18, -3.5), (16.5, -6)], r=L(S, 0.5, 2))),
    ]


@icon("dental-scaler", CAT, "Dental scaler with a grip handle and a small sickle-shaped blade at the tip",
      tags=["dentist", "tartar removal", "plaque", "hygienist", "teeth cleaning", "dental tool"])
def _(S):
    m = axis((3.5, 20.5), -45)
    blade = [(13, 0), (16, -0.5), (20, -4), (18, 0.8), (15.5, 1.5)]
    return [
        shell(stadium(m, -0.5, 8, 2.25, L(S, 1, 2.25))),
        detail(mseg(m, 3, -2.25, 3, 2.25)),
        line(mseg(m, 8, 0, 13, 0)),
        shell(mpoly(m, [(13, -1.5), (18.5, -4.5), (17.5, 1.5), (13, 1.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("dental-drill", CAT, "Dental handpiece with an angled head and a tiny bur, a hose trailing from the back",
      tags=["dentist", "handpiece", "tooth drilling", "cavity", "dental tool", "bur"])
def _(S):
    m = axis((7, 19), -40)
    return [
        shell(stadium(m, 0, 11, 2.25, L(S, 1, 2.25))),
        shell(mpoly(m, [(8.5, -2.25), (13, -2.25), (13, -6.5), (8.5, -6.5)], closed=True, r=S.r * 0.5)),
        line(mseg(m, 10.75, -6.5, 10.75, -9.5)),
        line(mpoly(m, [(0, 0), (-3.5, 0)])),
    ]


@icon("dental-chair", CAT, "Reclined dental chair seen from the side with an overhead lamp on an arm",
      tags=["dentist", "dental office", "patient chair", "clinic", "oral care", "treatment room"])
def _(S):
    m = axis((11.5, 14.5), -28)
    return [
        shell(rect(2.5, 12.5, 9, 3.5, L(S, 1, 1.75))),
        shell(stadium(m, 0, 10, 1.75, L(S, 0.75, 1.75))),
        line(seg(7, 16, 7, 21.5)), line(seg(3.5, 21.5, 10.5, 21.5)),
        line(poly([(21.5, 2.5), (14.5, 2.5), (12, 6)], r=S.r)),
        shell(circle(10.5, 8.5, 2.25)),
    ]


@icon("dental-forceps", CAT, "Dental extraction forceps with curved beaks gripping a tooth that has two roots",
      tags=["tooth extraction", "dentist", "pulling a tooth", "oral surgery", "pliers", "dental tool"])
def _(S):
    return [
        line(poly([(8, 21.5), (9.5, 13), (6.5, 9.5), (6.5, 4.5)], r=S.r)),
        line(poly([(16, 21.5), (14.5, 13), (17.5, 9.5), (17.5, 4.5)], r=S.r)),
        shell(poly([(9.75, 3), (14.25, 3), (14.25, 7), (13.25, 11), (12, 8.5), (10.75, 11), (9.75, 7)], closed=True, r=S.r * 0.5)),
    ]


@icon("dental-implant", CAT, "Dental implant with a tooth crown on top of a threaded screw post",
      tags=["tooth replacement", "missing tooth", "dentist", "titanium", "oral surgery", "artificial tooth"])
def _(S):
    crown = rect(5.5, 2.5, 13, 8, L(S, 2.5, 4))
    post = poly([(9, 8), (15, 8), (14, 21.5), (10, 21.5)], closed=True)
    return [
        shell(union(crown, post)),
        detail(seg(9.5, 14, 14.5, 14)),
        detail(seg(9.8, 18, 14.2, 18)),
    ]


@icon("clear-aligner", CAT, "Clear aligner tray, a U-shaped shell with a row of tooth pockets, seen from above",
      tags=["invisalign style", "braces", "orthodontics", "teeth straightening", "retainer", "dentist"])
def _(S):
    outer = "M3 2.5H21V10A9 10 0 0 1 3 10Z"
    inner = "M8.5 2.5H15.5V10A3.5 4.5 0 0 1 8.5 10Z"
    pts = [(5.75, 5.5), (5.75, 9.5)] + [(12 - 6.25 * math.cos(math.radians(a)), 9.5 + 7.6 * math.sin(math.radians(a))) for a in (36, 72, 108, 144)]
    pts = [(12 - 6.25 * math.cos(math.radians(a)), 9.5 + 7.6 * math.sin(math.radians(a))) for a in (30, 60, 90, 120, 150)] + [(5.75, 6), (18.25, 6)]
    return [shell(minus(outer, inner))] + [dot(x, y, 1.0) for x, y in pts]


@icon("dental-bridge", CAT, "Dental bridge of three joined crowns, the middle one over a gap between two tooth stumps",
      tags=["missing tooth", "crowns", "dentist", "tooth replacement", "prosthodontics", "oral care"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 7, L(S, 2, 3))),
        detail(seg(8.75, 2.5, 8.75, 9.5)), detail(seg(15.25, 2.5, 15.25, 9.5)),
        shell(poly([(3.5, 13), (8, 13), (7.5, 21.5), (4, 21.5)], closed=True, r=S.r * 0.4)),
        shell(poly([(16, 13), (20.5, 13), (20, 21.5), (16.5, 21.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("broken-tooth", CAT, "Tooth with a jagged crack line and a corner chipped off",
      tags=["cracked tooth", "chipped tooth", "dental injury", "dentist", "emergency", "toothache"])
def _(S):
    tooth = [(5.5, 6), (7.5, 3.5), (10.5, 3.5), (12, 4.5), (13.5, 3.5), (15, 3.5), (18.5, 7), (18.5, 10),
             (16.5, 21), (14, 21), (12, 14.5), (10, 21), (7.5, 21), (5.5, 10)]
    return [
        shell(poly(tooth, closed=True, r=S.r * 0.7)),
        detail(poly([(12, 4.5), (10.5, 8), (13.5, 10), (11.5, 13)])),
    ]


@icon("dental-impression-tray", CAT, "U-shaped dental impression tray seen from above with a straight handle at the front",
      tags=["dental mold", "impression", "dentist", "prosthodontics", "teeth cast", "orthodontics"])
def _(S):
    outer = "M3.5 3H20.5V10A8.5 8 0 0 1 3.5 10Z"
    tray = union(outer, rect(10.5, 14, 3, 7.5, L(S, 0.5, 1.5)))
    return [
        shell(tray),
        detail("M8 3V9.5A4 3.5 0 0 0 16 9.5V3") if S.name == "rounded" else detail(poly([(8, 3), (8, 10), (16, 10), (16, 3)])),
    ]


@icon("saliva-ejector", CAT, "Bendable saliva ejector tube with a hooked end and a small round tip",
      tags=["dental suction", "dentist", "suction tube", "dental assistant", "mouth", "oral care"])
def _(S):
    return [
        line(poly([(4.5, 21.5), (4.5, 12), (9, 8.5), (16, 8.5), (19.5, 6)], r=S.r * 2)),
        shell(circle(19.5, 3.75, 1.75)),
        shell(rect(2.5, 18, 4, 3.5, L(S, 0.5, 1.25))) if False else detail(seg(4.5, 15, 4.5, 15.1)) if False else line(seg(2.5, 17, 6.5, 17)),
    ]


# ============================================================================ surgical instruments

def pistol(S, top=4.5, bottom=10, x0=2.5, x1=15.5):
    """Pistol body: horizontal barrel with a grip falling from its rear and a trigger line."""
    body = rect(x0, top, x1 - x0, bottom - top, L(S, 1.5, 3))
    grip = poly([(x0, bottom - 1), (x0 + 6, bottom - 1), (x0 + 4.5, 21.5), (x0 - 0.5 + 1, 21.5)], closed=True, r=S.r * 0.5)
    return union(body, grip)


@icon("surgical-scissors", CAT, "Fine straight surgical scissors with blunt blades and two round finger rings",
      tags=["operating room", "surgery", "cutting tool", "suture scissors", "instrument", "theatre"])
def _(S):
    return [
        line(poly([(9.5, 14), (14.5, 2.5)])), line(poly([(14.5, 14), (9.5, 2.5)])),
        shell(circle(7.5, 18, 3)), shell(circle(16.5, 18, 3)),
    ]


@icon("hemostat", CAT, "Hemostat clamp with serrated narrow jaws, finger rings and a ratchet lock",
      tags=["artery forceps", "clamp", "surgery", "locking forceps", "instrument", "operating room"])
def _(S):
    return [
        shell(poly([(10.5, 10), (11, 2.5), (13, 2.5), (13.5, 10)], closed=True, r=S.r * 0.4)),
        detail(seg(11, 5.5, 13, 5.5)),
        line(poly([(11.5, 10), (9, 14)])), line(poly([(12.5, 10), (15, 14)])),
        shell(circle(7, 18, 3)), shell(circle(17, 18, 3)),
        line(poly([(10.3, 18), (11.2, 17), (12, 18), (12.8, 17), (13.7, 18)])) if False else line(seg(10.3, 19.5, 13.7, 19.5)),
    ]


@icon("tissue-forceps", CAT, "Tissue forceps with two long arms joined at the back and small teeth at the tips",
      tags=["tweezers", "surgery", "toothed forceps", "instrument", "operating room", "wound care"])
def _(S):
    return [
        line(poly([(12, 2.5), (11, 6), (8, 19)], r=S.r * 0.8)),
        line(poly([(12, 2.5), (13, 6), (16, 19)], r=S.r * 0.8)),
        line(poly([(8, 19), (9.3, 21.5)])), line(poly([(16, 19), (14.7, 21.5)])),
    ]


@icon("needle-holder", CAT, "Needle holder clamp with ring handles and short jaws gripping a curved suture needle",
      tags=["needle driver", "suturing", "surgery", "instrument", "stitching", "operating room"])
def _(S):
    return [
        line(arc(16, 6.5, 5.5, 135, 270)),
        shell(poly([(10.5, 11), (10.8, 6.5), (13.2, 6.5), (13.5, 11)], closed=True, r=S.r * 0.4)),
        line(poly([(11.5, 11), (9, 14.5)])), line(poly([(12.5, 11), (15, 14.5)])),
        shell(circle(7, 18.5, 3)), shell(circle(17, 18.5, 3)),
    ]


@icon("surgical-retractor", CAT, "Surgical retractor with a flat grip handle ending in a wide right-angled blade",
      tags=["surgery", "wound spreader", "operating room", "instrument", "exposure", "hand held retractor"])
def _(S):
    return [
        shell(poly([(6.5, 2.5), (11.5, 2.5), (11.5, 15.5), (21, 15.5), (21, 21.5), (6.5, 21.5)], closed=True, r=S.r)),
        detail(seg(6.5, 6, 11.5, 6)),
        detail(seg(6.5, 9.5, 11.5, 9.5)),
    ]


@icon("suture-needle", CAT, "Curved suture needle shaped like a half moon with a thread trailing from its back end",
      tags=["stitching", "surgery", "sewing wound", "thread", "surgical needle", "sutures"])
def _(S):
    return [
        line(arc(11.5, 11.5, 8, 105, 315)),
        line("M17.2 5.8Q21.5 6.5 19.5 10.5T21 16") if S.name == "rounded" else line(poly([(17.2, 5.8), (21.5, 8), (19, 11.5), (21, 16)])),
    ]


@icon("stitches", CAT, "Row of cross stitches closing a straight cut line",
      tags=["sutures", "wound closure", "surgery", "sewn wound", "closing a cut", "healing"])
def _(S):
    out = [line(seg(2.5, 12, 21.5, 12))]
    for x in (5.5, 10, 14.5, 19):
        out.append(line(seg(x - 1, 7.5, x + 1, 16.5)))
    return out


@icon("wound-closure-strips", CAT, "Straight vertical cut crossed by three short parallel adhesive strips",
      tags=["steri strips", "butterfly bandage", "wound care", "first aid", "tape", "adhesive"])
def _(S):
    out = [line(seg(12, 2.5, 12, 21.5)) if False else line(seg(12, 6.5, 12, 10.25)), line(seg(12, 13.75, 12, 17.5))]
    for y in (3, 10.25, 17.5):
        out.append(shell(rect(4.5, y, 15, 3.5, L(S, 0.5, 1.5))))
    return out


@icon("surgical-stapler", CAT, "Linear surgical stapler with long slender jaws on a pistol grip and a trigger",
      tags=["skin stapler", "surgery", "wound closure", "staples", "instrument", "operating room"])
def _(S):
    return [
        shell(pistol(S)),
        line(poly([(10.5, 10), (10, 15)])),
        shell(rect(15.5, 5, 6, 2.5, L(S, 0.5, 1.25))),
        line(seg(15.5, 10.5, 21.5, 10.5)),
    ]


@icon("bone-saw", CAT, "Oscillating bone saw, a pistol-shaped power tool with a short flat toothed blade at the front",
      tags=["orthopedic surgery", "amputation", "power tool", "operating room", "cutting bone", "cast saw"])
def _(S):
    return [
        shell(pistol(S)),
        line(poly([(10.5, 10), (10, 15)])),
        shell(poly([(15.5, 5.5), (21.5, 5.5), (21.5, 9), (20, 8), (18.5, 9.5), (17, 8), (15.5, 9)], closed=True, r=0)),
    ]


@icon("surgical-drill", CAT, "Surgical bone drill, a compact pistol-grip power drill with a long thin drill bit",
      tags=["orthopedic surgery", "power tool", "bone drill", "operating room", "instrument", "hole"])
def _(S):
    return [
        shell(pistol(S, x1=14)),
        line(poly([(10, 10), (9.5, 15)])),
        shell(rect(14, 5.5, 2.5, 3, 0.5)) if False else line(seg(14, 7.25, 21.5, 7.25)),
        dot(3, 7.25, 0) if False else detail(seg(6, 7.25, 8, 7.25)),
    ]


@icon("surgical-mallet", CAT, "Surgical mallet with a short handle and a solid cylindrical metal head",
      tags=["orthopedic surgery", "hammer", "bone work", "operating room", "instrument", "tap"])
def _(S):
    m = axis((3.5, 20.5), -45)
    return [
        shell(stadium(m, 0, 13.5, 1.75, L(S, 0.75, 1.75))),
        shell(mpoly(m, [(12, -5), (20, -5), (20, 5), (12, 5)], closed=True, r=S.r * 0.6)),
        detail(mseg(m, 16, -5, 16, 5)),
    ]


@icon("osteotome", CAT, "Osteotome, a long slim chisel with a flat bevelled blade and a round handle cap",
      tags=["bone chisel", "orthopedic surgery", "instrument", "operating room", "cutting bone", "surgery"])
def _(S):
    m = axis((5.5, 18.5), -45)
    return [
        shell(circle(*m(0, 0), 2.75)),
        shell(stadium(m, 2.5, 9, 1.75, L(S, 0.75, 1.75))),
        shell(mpoly(m, [(9, -2), (16, -2), (19, 2), (9, 2)], closed=True, r=S.r * 0.4)),
    ]


@icon("rongeur", CAT, "Rongeur with spring handles and a small cupped biting jaw at the tip",
      tags=["bone cutter", "spine surgery", "instrument", "operating room", "nibbler", "orthopedic"])
def _(S):
    return [
        line(poly([(8.5, 2.5), (8.5, 6), (15.5, 6), (15.5, 2.5)], r=L(S, 0, 2))),
        line(seg(12, 6, 12, 12)),
        line(poly([(12, 12), (7, 21.5)])), line(poly([(12, 12), (17, 21.5)])),
        line(poly([(9, 19), (12, 15.5), (15, 19)], r=S.r)),
    ]


@icon("curette", CAT, "Double-ended curette with a slim handle and a small spoon-shaped loop at each end",
      tags=["scraper", "surgery", "dental", "instrument", "scoop", "operating room"])
def _(S):
    m = axis((4, 20), -45)
    ax, ay = m(3, 0)
    bx, by = m(18, 0)
    return [
        shell(rot(ellipse(ax, ay, 3, 2), -45, ax, ay)),
        shell(stadium(m, 6, 14, 1.5, L(S, 0.5, 1.5))),
        shell(rot(ellipse(bx, by, 3.5, 2.4), -45, bx, by)),
    ]


@icon("speculum", CAT, "Duckbill speculum with two blades open at the front and a handle below",
      tags=["vaginal speculum", "gynecology", "pap smear", "exam instrument", "cervical screening", "nasal"])
def _(S):
    return [
        line(poly([(5.5, 9.5), (20.5, 3.5)])), line(poly([(5.5, 9.5), (20.5, 15)])),
        shell(rect(3.5, 9.5, 4.5, 12, L(S, 1, 2))),
        detail(seg(3.5, 14, 8, 14)),
    ]


@icon("trocar", CAT, "Trocar with a sharp-tipped rod passing through a short tube port with a valve cap on top",
      tags=["laparoscopy", "keyhole surgery", "port", "surgical access", "instrument", "minimally invasive"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 3.5, L(S, 1, 1.75))),
        shell(rect(8.5, 6, 7, 9.5, L(S, 0.5, 1.5))),
        line(seg(15.5, 10, 20, 10)),
        detail(seg(12, 8.5, 12, 13)) if False else line(seg(12, 15.5, 12, 18.5)),
        shell(poly([(10.5, 17.5), (13.5, 17.5), (12, 21.5)], closed=True, r=S.r * 0.3)) if False else solid(poly([(10.5, 17.5), (13.5, 17.5), (12, 21.5)], closed=True)),
    ]


@icon("cautery-pen", CAT, "Electrosurgical pencil with two small buttons, a flat blade tip and a cord out of the back",
      tags=["diathermy", "electrocautery", "bovie", "surgery", "cutting and coagulation", "instrument"])
def _(S):
    m = axis((7.5, 16.5), -45)
    return [
        shell(stadium(m, 0, 11, 2.25, L(S, 1, 2.25))),
        sq(*m(3, -0.5), 1.0, 1.0) if False else dot(*m(3.5, 0), 0.9),
        dot(*m(6.5, 0), 0.9),
        line(mseg(m, 11, 0, 14, 0)),
        shell(mpoly(m, [(14, -1.5), (19, -1.5), (19, 1.5), (14, 1.5)], closed=True, r=S.r * 0.3)),
        line(poly([(6.3, 18.2), (3.5, 19.5), (3.5, 21.5)], r=S.r)),
    ]


@icon("surgical-robot", CAT, "Robotic surgery system with a central column and three jointed arms reaching down to a point",
      tags=["robotic surgery", "da vinci style", "laparoscopic", "operating room", "minimally invasive", "telesurgery"])
def _(S):
    return [
        shell(rect(8, 2.5, 8, 4.5, L(S, 1, 2))),
        line(poly([(9, 7), (4.5, 10.5), (9.5, 17.5)], r=S.r)),
        line(poly([(15, 7), (19.5, 10.5), (14.5, 17.5)], r=S.r)),
        line(seg(12, 7, 12, 17.5)),
        line(seg(8, 21.5, 16, 21.5)),
    ]


@icon("operating-table", CAT, "Operating table with a flat padded top on a single central column and a wide base",
      tags=["surgery", "operating theatre", "surgical bed", "hospital", "operating room", "procedure table"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 19, 5, L(S, 1.5, 2.5))),
        line(seg(12, 10.5, 12, 17.5)),
        shell(rect(5.5, 17.5, 13, 4, L(S, 0.5, 2))),
    ]


@icon("surgical-light", CAT, "Surgical light with a wide lamp head holding several light cells, hanging from a jointed ceiling arm",
      tags=["operating room", "theatre lamp", "overhead light", "surgery", "illumination", "hospital"])
def _(S):
    return [
        line(poly([(3.5, 3), (12, 3), (12, 10)], r=S.r)),
        shell(ellipse(12, 15.5, 9.5, 5.25)),
        dot(7.5, 15.5, 1.25), dot(12, 15.5, 1.25), dot(16.5, 15.5, 1.25),
    ]


@icon("anesthesia-machine", CAT, "Anesthesia machine cart with a screen, gas flow tubes, a hose and a breathing bag",
      tags=["anaesthesia", "ventilator", "operating room", "gas machine", "surgery", "anesthetist"])
def _(S):
    return [
        shell(rect(3, 2.5, 11.5, 19, L(S, 1.5, 3))),
        detail(rect(5.5, 5, 6.5, 4.5, L(S, 0, 1))),
        detail(seg(7, 13, 7, 18)), detail(seg(11, 13, 11, 18)),
        line(poly([(14.5, 7), (18.5, 7), (18.5, 10.5)], r=S.r)),
        shell(ellipse(18.5, 14.5, 2.75, 3.75)),
    ]


@icon("instrument-tray", CAT, "Surgical instrument tray seen from above with a scalpel, forceps and scissors laid side by side",
      tags=["operating room", "surgery", "sterile tray", "tools", "scrub nurse", "medical instruments"])
def _(S):
    return [
        shell(rect(2.5, 4, 19, 16, L(S, 2, 4))),
        detail(seg(7, 8, 7, 16)),
        detail(poly([(11, 8), (12, 16), (13, 8)])) if False else detail(seg(12, 8, 12, 16)),
        detail(seg(17, 8, 17, 16)),
    ]


@icon("kidney-dish", CAT, "Shallow bean-shaped kidney dish basin seen at an angle",
      tags=["emesis basin", "sick bowl", "hospital", "surgery", "nursing", "instrument tray"])
def _(S):
    outer = "M2.5 14C2.5 8.5 6.5 6 12 6C17.5 6 21.5 8.5 21.5 14C21.5 17.5 18.5 18 16.5 16.2C14.5 14.5 9.5 14.5 7.5 16.2C5.5 18 2.5 17.5 2.5 14Z"
    return [
        shell(outer),
        detail("M6.2 11.5C7.5 10 9.5 9.5 12 9.5C14.5 9.5 16.5 10 17.8 11.5") if S.name == "rounded" else detail(poly([(6, 12), (9, 9.5), (15, 9.5), (18, 12)])),
    ]


@icon("surgical-drain", CAT, "Wound drainage bulb shaped like a squeezable grenade with a thin tube coming out of the top",
      tags=["jp drain", "post surgery", "wound drainage", "suction bulb", "hospital", "nursing"])
def _(S):
    return [
        shell(union(ellipse(12, 15, 6.5, 6), rect(10, 8, 4, 3.5, L(S, 0.5, 1)))),
        line("M12 8V5.5Q12 2.5 16 2.5H21") if S.name == "rounded" else line(poly([(12, 8), (12, 2.5), (21, 2.5)])),
        detail(seg(12, 12.5, 12, 19)),
    ]


@icon("catheter", CAT, "Urinary catheter, a long thin tube with a small balloon near the tip and a forked connector at the end",
      tags=["foley", "urology", "drainage tube", "bladder", "hospital", "medical tube"])
def _(S):
    m = axis((3.5, 20.5), -45)
    bx, by = m(17.25, 0)
    return [
        line(mpoly(m, [(5, 0), (14, 0)])),
        line(mpoly(m, [(5, 0), (2, -3)])), line(mpoly(m, [(5, 0), (2, 3)])),
        shell(rot(ellipse(bx, by, 3.25, 2.4), -45, bx, by)),
    ]


@icon("urine-bag", CAT, "Urine drainage bag with volume marks, a short tube at the top and a tap at the bottom",
      tags=["catheter bag", "drainage bag", "urology", "hospital", "nursing", "collection bag"])
def _(S):
    return [
        line(poly([(9, 5.5), (9, 2.5)])),
        shell(rect(5.5, 5.5, 13, 13.5, L(S, 2, 4))),
        detail(seg(8.5, 9.5, 11.5, 9.5)), detail(seg(8.5, 13, 11.5, 13)), detail(seg(8.5, 16.5, 11.5, 16.5)) if False else detail(seg(8.5, 16.5, 11, 16.5)),
        line(poly([(15, 19), (15, 21.5), (18, 21.5)])),
    ]


@icon("ostomy-bag", CAT, "Ostomy pouch, a rounded bag with a circular flange ring near the top",
      tags=["colostomy", "stoma", "stoma bag", "ileostomy", "bowel", "surgery recovery"])
def _(S):
    return [
        shell(union(circle(12, 7.5, 5.5), rect(6, 8, 12, 13.5, L(S, 3, 5.5)))),
        detail(circle(12, 7.5, 2.25)),
    ]


@icon("feeding-tube", CAT, "Nasogastric feeding tube with a funnel connector at one end and a rounded tip at the other",
      tags=["ng tube", "enteral feeding", "gastric tube", "nutrition", "hospital", "nursing"])
def _(S):
    return [
        shell(poly([(3, 2.5), (9, 2.5), (7.5, 7), (4.5, 7)], closed=True, r=S.r * 0.4)),
        line("M6 7V10Q6 15 12 15Q18 15 18 18") if S.name == "rounded" else line(poly([(6, 7), (6, 12), (12, 15), (18, 15), (18, 18)])),
        shell(circle(18, 19.75, 1.5)),
    ]


@icon("iv-cannula", CAT, "IV cannula with a short needle, a winged hub and a coloured port cap on top",
      tags=["intravenous", "drip", "peripheral line", "venous access", "hospital", "nursing"])
def _(S):
    m = axis((3, 21), -45)
    return [
        line(mseg(m, 0, 0, 8)) if False else line(mseg(m, 0, 0, 7.5, 0)),
        shell(stadium(m, 7.5, 14.5, 2.25, L(S, 1, 2.25))),
        shell(mpoly(m, [(9, 2.25), (12.5, 2.25), (13, 5.5), (8.5, 5.5)], closed=True, r=S.r * 0.4)),
        shell(mpoly(m, [(11, -2.25), (14, -2.25), (14, -5.5), (11, -5.5)], closed=True, r=S.r * 0.4)),
        solid(mpoly(m, [(10.5, -5.5), (14.5, -5.5), (14.5, -8), (10.5, -8)], closed=True)),
    ]


@icon("butterfly-needle", CAT, "Butterfly needle with a short needle, two flat plastic wings and a thin tube trailing behind",
      tags=["winged infusion set", "blood draw", "venipuncture", "phlebotomy", "iv", "hospital"])
def _(S):
    return [
        line(seg(12, 14.5, 12, 21.5)),
        shell(rect(10, 9, 4, 5.5, L(S, 0.5, 1.5))),
        shell(poly([(10, 10), (4, 7), (3.5, 12), (10, 13.5)], closed=True, r=S.r * 0.6)),
        shell(poly([(14, 10), (20, 7), (20.5, 12), (14, 13.5)], closed=True, r=S.r * 0.6)),
        line("M12 9V6Q12 3 16 3Q20 3 21.5 6") if S.name == "rounded" else line(poly([(12, 9), (12, 3), (20, 3), (21.5, 6)])),
    ]


@icon("biopsy-needle", CAT, "Biopsy needle with a thick spring-loaded handle and a long thin needle",
      tags=["tissue sample", "core biopsy", "diagnostic", "pathology", "oncology", "hospital"])
def _(S):
    m = axis((4.5, 19.5), -45)
    return [
        shell(stadium(m, -1.5, 7, 3, L(S, 1.25, 3))),
        detail(mseg(m, 2.75, -3, 2.75, 3)),
        line(mpoly(m, [(1, -3), (1, -5.5)])),
        line(mseg(m, 7, 0, 21, 0)),
    ]


@icon("tourniquet", CAT, "Strap loop with a twist rod passing through it, the windlass of an emergency tourniquet",
      tags=["bleeding control", "first aid", "hemorrhage", "trauma", "emergency", "windlass"])
def _(S):
    ring = minus(ellipse(12, 13, 10, 7), ellipse(12, 13, 6.5, 3.75))
    stick = rect(10.25, 2.5, 3.5, 19, L(S, 1, 1.75))
    return [
        shell(union(ring, stick)),
    ]


@icon("surgical-cap", CAT, "Surgical cap, a rounded cloth cap with ties hanging at the back",
      tags=["scrub cap", "hair cover", "operating room", "hygiene", "theatre", "surgeon"])
def _(S):
    cap = "M5 15Q5 4 13 4Q21 4 21 15Z"
    return [
        shell(cap if S.name == "rounded" else poly([(5, 15), (6, 7), (13, 4), (20, 7), (21, 15)], closed=True)),
        detail(seg(5, 11.5, 21, 11.5)),
        line(poly([(5.5, 15), (3.5, 21.5)])), line(poly([(8.5, 15), (8, 21.5)])) if False else line(poly([(9, 15), (9.5, 21.5)])),
    ]


@icon("surgical-gown", CAT, "Surgical gown with long sleeves, knitted cuffs and a tie at the waist",
      tags=["scrubs", "operating room", "protective clothing", "ppe", "surgeon", "hospital"])
def _(S):
    body = [(8.5, 2.5), (12, 6), (15.5, 2.5), (21, 6.5), (21, 15.5), (17.5, 15.5), (17, 21.5), (7, 21.5), (6.5, 15.5), (3, 15.5), (3, 6.5)]
    return [
        shell(poly(body, closed=True, r=S.r * 0.8)),
        detail(seg(3, 12.5, 6.5, 12.5)), detail(seg(17.5, 12.5, 21, 12.5)),
        detail(seg(8.5, 16, 15.5, 16)),
    ]
