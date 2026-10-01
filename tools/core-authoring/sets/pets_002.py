"""TypeIcon Core: pets, horses and livestock care (batch pets_002).

Original drawings from the objects themselves: dog sports, pet health, horse tack, feed and farm animal handling.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path

CAT = "pets"


def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def mark(d) -> Part:
    """Small solid shape: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def tf(pts, k=1.0, ox=0.0, oy=0.0):
    """Scale points about the origin then translate."""
    return [(ox + k * x, oy + k * y) for x, y in pts]


def rotd(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rot(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rseg(x1, y1, x2, y2, deg, cx=12.0, cy=12.0):
    """Straight segment turned by deg about (cx, cy) (rotd drops straight open paths)."""
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg, cx, cy)
    return seg(a, b, c, d)


def pawmark(S, cx, cy, s=1.0, deg=0.0):
    """Solid paw print (pad and four toes) centred near (cx, cy); about 8s wide and 8s tall, turned by deg.

    Line has a faceted pad with sharp corners, Rounded a soft pad."""
    pad = poly([(cx, cy + 0.1 * s), (cx + 3.1 * s, cy + 2.9 * s), (cx + 2 * s, cy + 4 * s),
                (cx - 2 * s, cy + 4 * s), (cx - 3.1 * s, cy + 2.9 * s)], closed=True, r=L(S, 0, 1.4 * s))
    parts = [mark(rotd(pad, deg, cx, cy) if deg else pad)]
    a = math.radians(deg)
    for dx, dy in ((-3.2, -0.3), (-1.15, -2.7), (1.15, -2.7), (3.2, -0.3)):
        x, y = dx * s, dy * s
        parts.append(mark(circle(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a), 1.05 * s)))
    return parts


def scl(d, k, cx=12.0, cy=12.0):
    """Scale a d-string by k about (12, 12) then move the centre to (cx, cy)."""
    return path_to_d(transform_path(P(d), (k, 0, 0, k, cx - 12 * k, cy - 12 * k)))


HEART = "M12 20L4.4 12.6A4.6 4.6 0 0 1 11 6.3L12 7.3L13 6.3A4.6 4.6 0 0 1 19.6 12.6Z"
HEART_R = "M10.6 18.6L4.4 12.6A4.6 4.6 0 0 1 11 6.3L11.3 6.6Q12 7.3 12.7 6.6L13 6.3A4.6 4.6 0 0 1 19.6 12.6L13.4 18.6Q12 20 10.6 18.6Z"


def heart(S, k=1.0, cx=12.0, cy=12.0):
    return scl(L(S, HEART, HEART_R), k, cx, cy)


SHIELD = "M12 2.5L20 5.5V11.5C20 16.5 16.5 19.8 12 21.5C7.5 19.8 4 16.5 4 11.5V5.5Z"
SHIELD_R = ("M11.2 2.8Q12 2.5 12.8 2.8L19.2 5.1Q20 5.4 20 6.3V11.5C20 16.5 16.5 19.8 12 21.5C7.5 19.8 4 16.5 4 11.5V6.3"
            "Q4 5.4 4.8 5.1Z")


def plus(cx, cy, r=2.5, w=1.6):
    """Solid plus (medical cross) as a small mark."""
    return mark(poly([(cx - w / 2, cy - r), (cx + w / 2, cy - r), (cx + w / 2, cy - w / 2), (cx + r, cy - w / 2), (cx + r, cy + w / 2),
                      (cx + w / 2, cy + w / 2), (cx + w / 2, cy + r), (cx - w / 2, cy + r), (cx - w / 2, cy + w / 2),
                      (cx - r, cy + w / 2), (cx - r, cy - w / 2), (cx - w / 2, cy - w / 2)], closed=True))


# Dog torso and head in side view, facing right (units 0..20 wide). Legs and tail are separate open strokes.
RUN_B = [(3, 4.5), (11, 4), (13.5, 2.5), (14.5, 0.8), (16.6, 1.4), (20, 4), (20, 5.8), (16.8, 6.6), (15.5, 8.6), (4.5, 8.6), (3, 6.6)]
# Solid standing dog silhouette (for small marks inside signs), units 0..20 by 0..14.
DOG_SIL = [(2, 5), (11.5, 4.6), (13.5, 3.2), (14.3, 0.8), (16.4, 1.4), (20, 4.4), (20, 6.2), (17, 6.8), (15.8, 8.2), (15.8, 14),
           (13.2, 14), (13.2, 9.8), (7.4, 9.8), (7.4, 14), (4.8, 14), (4.8, 9.2), (2, 6.8)]
# Barking dog head in profile, facing right, open mouth, units 0..20 by 0..18.
BARK = [(2, 18), (2, 9), (4, 5), (5.4, 0.5), (8.6, 3.6), (12.5, 4.6), (18.5, 7), (18.5, 9), (12.5, 10), (17.5, 12.2), (17.5, 14.4),
        (11.5, 14), (9, 18)]


def dog_run(S, k, ox, oy):
    """Leaping dog: torso and head as a shell, two legs and a tail as strokes."""
    def T(x, y):
        return (ox + k * x, oy + k * y)
    return [
        shell(poly(tf(RUN_B, k, ox, oy), closed=True, r=S.r)),
        line(poly([T(14, 8), T(18.5, 12.5)], r=0)),
        line(poly([T(6, 8), T(2, 12.5)], r=0)),
        line(poly([T(3.4, 5.4), T(0.5, 2)], r=0)),
    ]


# ============================================================================ dog care and training

@icon("dog-waste-station", CAT, "Dog waste bag dispenser with a paw mark above a lidded bin",
      tags=["poop bag", "dog park", "pet waste", "clean up", "litter", "dispenser"])
def _(S):
    return [
        shell(rect(5.5, 2, 13, 8, rr(S, 2))),
        *pawmark(S, 12, 5.6, 0.5),
        line("M12 10V13"),
        line("M5 14.5H19"),
        shell(rect(7.5, 14.5, 9, 6.5, rr(S, 1.5))),
    ]


@icon("pee-pad", CAT, "Square absorbent training pad with a paw print in the middle",
      tags=["puppy pad", "potty training", "house training", "wee wee pad", "absorbent", "puppy"])
def _(S):
    return [
        shell(rect(3.5, 4.5, 17, 15, rr(S, 3))),
        *pawmark(S, 12, 10.6, 0.95),
        dot(6.5, 7.5, 1), dot(17.5, 7.5, 1), dot(6.5, 16.5, 1), dot(17.5, 16.5, 1),
    ]


@icon("training-clicker", CAT, "Small box clicker with a metal button and a wrist loop, with click marks",
      tags=["dog training", "clicker training", "positive reinforcement", "click", "obedience"])
def _(S):
    return [
        shell(rect(5.5, 9.5, 11, 10, rr(S, 3))),
        detail(circle(11, 14.5, 2.2)),
        line("M5.5 12.5C3 12.5 2.5 16.5 5.5 16.5"),
        line("M18 5.5L19.5 3.5"), line("M20 9.5H22.5"), line("M14.5 4.5L14 2.5"),
    ]


@icon("agility-jump", CAT, "Dog leaping over a bar held between two upright stands",
      tags=["dog agility", "hurdle", "obstacle course", "canine sport", "jump", "competition"])
def _(S):
    return [
        line("M4 10.5V21"), line("M20 10.5V21"), line("M2.5 21H5.5"), line("M18.5 21H21.5"),
        line("M4 14H20"),
        *dog_run(S, 0.66, 5.2, 2.5),
        dot(15.3, 4.4, 0.8),
    ]


@icon("weave-poles", CAT, "Row of upright poles on a base with a zigzag line of dots weaving between them",
      tags=["dog agility", "slalom", "obstacle course", "canine sport", "training", "poles"])
def _(S):
    return [
        line("M4.5 3.5V18"), line("M9.5 3.5V18"), line("M14.5 3.5V18"), line("M19.5 3.5V18"),
        line("M2.5 20.5H21.5"),
        dot(7, 9, 1), dot(12, 14, 1), dot(17, 9, 1),
    ]


@icon("agility-seesaw", CAT, "Long tilted plank balanced on a triangle pivot with one end touching the ground",
      tags=["dog agility", "teeter", "teeter-totter", "obstacle", "balance", "canine sport"])
def _(S):
    return [
        line("M2.5 8L21.5 19.5"),
        shell(poly([(12, 14.2), (16.5, 21), (7.5, 21)], closed=True, r=S.r)),
        line("M2.5 21H4.5"), line("M19.5 21H21.5"),
    ]


@icon("tire-jump", CAT, "Round tire hung by two ropes inside a rectangular frame",
      tags=["dog agility", "hoop jump", "obstacle course", "canine sport", "tire", "ring jump"])
def _(S):
    return [
        line("M3.5 21V3.5H20.5V21"),
        line("M9 4V9.6"), line("M15 4V9.6"),
        shell(circle(12, 14.5, 5.6)),
        detail(circle(12, 14.5, 1.8)),
    ]


@icon("dog-fetch", CAT, "Running dog in side view with a ball held in its mouth",
      tags=["play fetch", "retrieve", "ball", "dog play", "exercise", "run"])
def _(S):
    return [
        *dog_run(S, 0.95, 1.2, 5.5),
        dot(15.6, 7.6, 0.85),
        mark(circle(20.6, 11, 1.6)),
    ]


@icon("dog-barking", CAT, "Dog head in profile with an open mouth and curved sound lines",
      tags=["bark", "woof", "noise", "loud dog", "alert", "canine"])
def _(S):
    k = 0.85
    bark = [(2, 17), (2, 8), (5, 3.5), (9.5, 3), (13, 5.5), (19, 7.5), (19, 9.5), (13, 10.5), (18, 13), (18, 15), (12, 15), (9.5, 17)]
    return [
        shell(poly(tf(bark, k, 1.8, 4), closed=True, r=S.r)),
        detail("M6.3 9.5C8 11.5 7.5 14 6.3 15.5"),
        dot(11.4, 9.4, 0.85),
        mark(circle(17.3, 10.6, 1.0)),
        line(arc(16.5, 13, 4, -40, 40)),
        line(arc(16.5, 13, 6.4, -40, 40)),
    ]


@icon("dog-show", CAT, "Scalloped prize rosette with a paw print and two ribbon tails",
      tags=["competition", "award", "best in show", "kennel club", "winner", "dog competition"])
def _(S):
    pts = []
    for i in range(24):
        pts.append(polar(12, 9, 7.2 if i % 2 == 0 else 6, -90 + i * 15))
    return [
        shell(poly(pts, closed=True, r=L(S, 0, 0.9))),
        *pawmark(S, 12, 7.4, 0.62),
        line("M9.5 15.5L7.5 21.5"), line("M14.5 15.5L16.5 21.5"),
    ]


@icon("herding-dog", CAT, "Crouched dog in profile watching a small sheep ahead of it",
      tags=["sheepdog", "border collie", "shepherd", "livestock", "farm dog", "working dog"])
def _(S):
    sheep = path_to_d(U(P(circle(14, 6.6, 2.6)), P(circle(17.4, 5.6, 3)), P(circle(20, 7.6, 2.2))))
    return [
        shell(poly(tf(RUN_B, 0.78, 1.5, 11.5), closed=True, r=S.r)),
        dot(14, 13.6, 0.8),
        line("M13.5 17.8V21"), line("M5.5 17.8V21"),
        shell(sheep),
        line("M15 9.6V11.8"), line("M19 9.6V11.8"),
    ]


@icon("dog-park", CAT, "Fenced dog park with a tree and a post-mounted paw sign",
      tags=["off leash area", "dog run", "play area", "enclosure", "pets allowed", "park"])
def _(S):
    return [
        shell(circle(6.5, 7.5, 4.2)),
        line("M6.5 11.7V15"),
        shell(rect(13, 2.5, 8, 7, rr(S, 1.5))),
        *pawmark(S, 17, 5.8, 0.52),
        line("M17 9.5V15"),
        line("M2 17H22"), line("M2 21H22"),
        line("M5 15V21"), line("M12 15V21"), line("M19 15V21"),
    ]


@icon("leashed-dog-sign", CAT, "Square sign showing a person walking a dog on a leash",
      tags=["keep on leash", "leash required", "dog walking", "rules", "park sign", "notice"])
def _(S):
    dog = poly(tf(DOG_SIL, 0.42, 12.3, 12.5), closed=True, r=0.3)
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        mark(circle(8, 8.3, 1.5)),
        mark(poly([(6.4, 10.5), (9.6, 10.5), (9.6, 15.3), (6.4, 15.3)], closed=True, r=0.4)),
        mark(seg(7, 15, 6, 18.5)), mark(seg(9, 15, 10, 18.5)),
        mark(dog),
        detail("M9.6 11.3L12 13.3"),
    ]


@icon("guard-dog-sign", CAT, "Rectangular plate sign with a barking dog head and four screw holes",
      tags=["beware of dog", "warning", "security", "private property", "caution dog", "fence sign"])
def _(S):
    return [
        shell(rect(2.5, 5, 19, 14, rr(S, 2.5))),
        mark(poly(tf(BARK, 0.56, 6.6, 7.4), closed=True, r=0.4)),
        dot(5.2, 7.7, 0.75), dot(18.8, 7.7, 0.75), dot(5.2, 16.3, 0.75), dot(18.8, 16.3, 0.75),
    ]


# ============================================================================ pet services and health

@icon("paw-print-trail", CAT, "Four paw prints stepping diagonally across the icon",
      tags=["footprints", "tracks", "walking", "pet steps", "animal tracks", "dog walk"])
def _(S):
    out = []
    for i in range(4):
        x, y = 4.4 + 4.9 * i, 18.6 - 4.3 * i
        sgn = -1 if i % 2 == 0 else 1
        out += pawmark(S, x + sgn * 0.9, y + sgn * 1.1 - 0.6, 0.62, 40)
    return out


@icon("pet-adoption", CAT, "House outline with a heart inside that has a paw print cut into it",
      tags=["adopt a pet", "rescue", "shelter", "forever home", "rehoming", "animal shelter"])
def _(S):
    hs = path_to_d(U(P(heart(S, 0.66, 12, 14.6))))
    hole = path_to_d(D(P(hs), *[P(x.d) for x in pawmark(S, 12, 13.3, 0.4)]))
    return [
        shell(poly([(3, 11), (12, 3), (21, 11), (21, 21), (3, 21)], closed=True, r=S.r), stroke_miterlimit="4"),
        mark(hole),
    ]


@icon("animal-welfare", CAT, "Large heart outline with a paw print centred inside",
      tags=["animal rights", "pet care", "rescue", "compassion", "charity", "humane"])
def _(S):
    return [shell(heart(S, 1.12, 12, 12.4), stroke_miterlimit="2"), *pawmark(S, 12, 10.4, 0.85)]


@icon("pet-hotel", CAT, "Tall building with a bed sign at the top and a paw print below it",
      tags=["pet boarding", "kennel", "dog hotel", "pet sitting", "overnight stay", "cattery"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, rr(S, 3.5))),
        mark(rect(7.5, 8.4, 9, 1.8, L(S, 0, 0.6))), mark(rect(7.5, 5.8, 1.6, 6.4, L(S, 0, 0.6))), mark(circle(11, 7.1, 1.15)), mark(rect(13.2, 7, 3.3, 1.4)),
        *pawmark(S, 12, 13.6, 0.62),
    ]


@icon("lost-pet-poster", CAT, "Poster pinned with a tack showing a question mark above a small dog",
      tags=["missing pet", "lost dog", "found pet", "flyer", "reward", "missing animal"])
def _(S):
    return [
        shell(rect(4.5, 3, 15, 18.5, rr(S, 1.5))),
        mark(circle(12, 3.2, 1.3)),
        line("M9.8 9.8C9.8 7.3 14.2 7.3 14.2 9.6C14.2 11.4 12 11.6 12 13.4"),
        dot(12, 15.4, 0.9),
        mark(poly(tf(DOG_SIL, 0.46, 7.4, 15.4), closed=True, r=0.3)),
    ]


@icon("pet-memorial", CAT, "Paw print with a halo above it and small wings at each side",
      tags=["pet loss", "rainbow bridge", "remembrance", "sympathy", "in memory", "angel pet"])
def _(S):
    wing = L(S, "M8 12.5C4 12.5 2.5 9 2.5 5C6.2 5.4 8 8.2 8 12.5Z", "M7.6 12.5C4 12.5 2.5 9 2.5 5.4Q2.5 5 2.9 5C6.2 5.4 8 8.2 8 11.6Q8 12.5 7.6 12.5Z")
    flip = path_to_d(transform_path(P(wing), (-1, 0, 0, 1, 24, 0)))
    return [
        line(ellipse(12, 4, 3.4, 1.3)),
        shell(wing), shell(flip),
        *pawmark(S, 12, 11.6, 0.85),
    ]


@icon("pet-insurance", CAT, "Shield with a paw print in the middle",
      tags=["pet cover", "vet bills", "protection", "policy", "animal health plan", "pet plan"])
def _(S):
    return [shell(L(S, SHIELD, SHIELD_R)), *pawmark(S, 12, 9.6, 0.9)]


@icon("pet-passport", CAT, "Small travel booklet with a paw print on the cover and a stamp ring",
      tags=["pet travel", "vaccination booklet", "animal id", "border crossing", "international", "pet documents"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 4))),
        *pawmark(S, 12, 8.6, 0.85),
        detail(circle(12, 17.4, 1.9)),
    ]


@icon("pet-health-record", CAT, "Clipboard with a paw print at the top and lines of notes below",
      tags=["vet records", "vaccination history", "medical chart", "animal health", "checkup", "patient file"])
def _(S):
    return [
        shell(rect(4.5, 4.5, 15, 17, rr(S, 2))),
        shell(rect(9, 2.5, 6, 4, min(S.R, 1.5))),
        *pawmark(S, 12, 10.6, 0.5),
        detail("M8 16H16"), detail("M8 19H13"),
    ]


@icon("veterinarian", CAT, "Person in a coat with a stethoscope holding a small dog",
      tags=["vet", "animal doctor", "pet doctor", "animal care", "veterinary surgeon", "clinic staff"])
def _(S):
    return [
        shell(circle(7.5, 5.5, 3)),
        shell(poly([(2.5, 21), (2.5, 14), (4.5, 10.5), (10.5, 10.5), (12.5, 14), (12.5, 21)], closed=True, r=S.r)),
        detail("M7.5 10.8V16.5"),
        line("M12.5 16L14.5 17"),
        mark(poly(tf(DOG_SIL, 0.52, 12.7, 10.4), closed=True, r=0.3)),
    ]


@icon("vet-clinic", CAT, "Clinic building with a medical cross and a paw print beside it",
      tags=["animal hospital", "veterinary practice", "pet doctor", "surgery", "animal health", "emergency vet"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 12, 16, rr(S, 4))),
        plus(8.5, 11.2, 3, 2),
        detail("M6.5 21.5V17.5H10.5V21.5"),
        *pawmark(S, 18.6, 10.2, 0.72),
    ]


@icon("pet-vaccine", CAT, "Upright syringe with a paw print on its barrel",
      tags=["animal vaccination", "shots", "injection", "rabies shot", "booster", "immunization"])
def _(S):
    return [
        line("M8.5 2.5H15.5"), line("M12 2.5V7.5"), line("M6.5 7.5H17.5"),
        shell(rect(8.5, 7.5, 7, 11.5, min(S.R, 1.5))),
        line("M12 19V22"),
        *pawmark(S, 12, 11.4, 0.5),
    ]


@icon("pet-first-aid-kit", CAT, "Carry case with a handle, a medical cross and a paw print on the front",
      tags=["animal first aid", "emergency", "pet safety", "medical kit", "vet supplies", "rescue kit"])
def _(S):
    return [
        shell(rect(2.5, 8, 19, 13, rr(S, 3))),
        line("M8.5 8V4.5H15.5V8"),
        plus(8.3, 14.5, 2.8, 2),
        *pawmark(S, 16.2, 13.2, 0.58),
    ]


@icon("pet-cone", CAT, "Side view of a flared recovery cone with a dog face showing in its wide round opening",
      tags=["e-collar", "cone of shame", "recovery collar", "after surgery", "lampshade collar", "vet"])
def _(S):
    body = poly([(2.5, 9.5), (14.5, 3), (14.5, 21), (2.5, 14.5)], closed=True, r=L(S, 0, 3))
    sil = path_to_d(U(P(body), P(ellipse(14.5, 12, 6, 9))))
    return [
        shell(sil, stroke_miterlimit="3"),
        detail(ellipse(14.5, 12, 6, 9)),
        dot(13.2, 10.6, 0.85), dot(17.2, 10.6, 0.85), mark(ellipse(15.2, 13.6, 1.3, 1.0)),
        mark(poly([(11.6, 9), (11.2, 6), (14, 7.6)], closed=True, r=0.3)), mark(poly([(18.8, 9), (19.2, 6), (16.4, 7.6)], closed=True, r=0.3)),
    ]


@icon("bandaged-paw", CAT, "Dog paw with toes and a bandage wrapped across the pad, with a small cross on the wrap",
      tags=["injured paw", "paw wrap", "first aid", "sore foot", "vet care", "limp"])
def _(S):
    pad = poly([(12, 9.5), (17.5, 14), (16, 19), (8, 19), (6.5, 14)], closed=True, r=L(S, 1, 2.5))
    toes = [rotd(ellipse(4.8, 9, 1.7, 2.3), -25, 4.8, 9), rotd(ellipse(9, 4.2, 1.8, 2.4), -8, 9, 4.2),
            rotd(ellipse(15, 4.2, 1.8, 2.4), 8, 15, 4.2), rotd(ellipse(19.2, 9, 1.7, 2.3), 25, 19.2, 9)]
    band = rotd(rect(3.5, 13.5, 17, 5.5, rr(S, 2.5)), -8, 12, 16.2)
    return [shell(pad), *[shell(t) for t in toes], shell(band), plus(12, 16.2, 1.5, 1)]


@icon("pet-wheelchair", CAT, "Dog in profile with its hind end supported by a two-wheeled cart frame",
      tags=["dog mobility cart", "disabled pet", "rear support", "paralysis", "handicapped dog", "wheels"])
def _(S):
    dog = [(6.5, 5.6), (11.5, 5.2), (13.5, 3.8), (14.3, 1.4), (16.4, 2), (20, 5), (20, 6.8), (17, 7.4), (15.8, 8.8), (15.8, 16.5),
           (13.2, 16.5), (13.2, 10.6), (6.5, 10.6)]
    return [
        mark(poly(tf(dog, 1, 1.5, 1.5), closed=True, r=0.4)),
        line("M7.5 12.3L4.6 17.4"), line("M3 12.3H9.5"),
        shell(circle(4.6, 18, 3.2)),
    ]


@icon("vet-exam-table", CAT, "Steel exam table on a central pedestal with a cat sitting on top",
      tags=["examination", "checkup", "veterinary clinic", "procedure table", "consultation", "pet visit"])
def _(S):
    return [
        shell(rect(2.5, 12, 19, 3, rr(S, 1.5))),
        shell(poly([(10, 15), (14, 15), (15.5, 21.5), (8.5, 21.5)], closed=True, r=S.r * 0.6)),
        shell(poly([(9.2, 6.4), (9.2, 2.2), (11.4, 3.6), (12.6, 3.6), (14.8, 2.2), (14.8, 6.4), (13.5, 8.2), (10.5, 8.2)], closed=True, r=S.r * 0.5)),
        shell(poly([(9, 9), (15, 9), (16.5, 12), (7.5, 12)], closed=True, r=S.r * 0.5)),
        line("M16.5 11.4C19.6 11 20 6.8 18 6.4"),
    ]


@icon("pet-x-ray", CAT, "X-ray film panel showing a dog in side view with its ribcage and legs picked out",
      tags=["radiograph", "skeleton", "bone scan", "vet imaging", "fracture", "animal x-ray"])
def _(S):
    dog = poly(tf(DOG_SIL, 0.72, 4.8, 6.6), closed=True, r=0.3)
    ribs = [rect(x, 8.6, 1, 3.6) for x in (7.3, 9.2, 11.1)]
    cut = path_to_d(D(P(dog), *[P(r) for r in ribs]))
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 3))),
        mark(cut),
    ]


@icon("pet-scale", CAT, "Low flat platform scale with a display and a dog standing on it",
      tags=["weigh in", "weight check", "pet weight", "vet scale", "diet", "body weight"])
def _(S):
    return [
        mark(poly(tf(DOG_SIL, 0.78, 3.2, 4.6), closed=True, r=0.3)),
        shell(rect(2.5, 16.5, 19, 5, rr(S, 2))),
        detail("M14 19H19"),
    ]


@icon("pet-microchip", CAT, "Small capsule chip with signal arcs rising toward a paw print",
      tags=["id chip", "implant", "rfid", "pet identification", "lost pet recovery", "tracking"])
def _(S):
    return [
        shell(rect(2.5, 14.5, 11, 5.5, 2.75)),
        detail("M8 15.5V19"),
        line(arc(8, 14, 4.2, -150, -60)), line(arc(8, 14, 7.4, -150, -60)),
        *pawmark(S, 17.4, 8, 0.85),
    ]


@icon("microchip-scanner", CAT, "Handheld scanner with a round reader head and signal arcs toward a paw print",
      tags=["chip reader", "rfid reader", "animal id", "found pet", "shelter", "vet check"])
def _(S):
    return [
        shell(circle(8, 7.5, 4.6)),
        shell(rect(5.5, 12.8, 5, 8.7, rr(S, 2))),
        mark(rect(6.9, 14.6, 2.2, 2)),
        line(arc(8, 7.5, 7.6, -30, 30)),
        *pawmark(S, 17.6, 15.6, 0.62),
    ]


@icon("flea-drops", CAT, "Squeeze pipette dripping a drop onto the curved back of a dog",
      tags=["spot on", "flea treatment", "tick treatment", "parasite control", "pipette", "topical"])
def _(S):
    return [
        shell(poly([(9, 2.5), (15, 2.5), (15, 8), (13, 11), (11, 11), (9, 8)], closed=True, r=S.r * 0.7)),
        detail("M9 5.5H15"),
        mark("M12 12.6C12 12.6 10.2 14.7 10.2 15.8A1.8 1.8 0 0 0 13.8 15.8C13.8 14.7 12 12.6 12 12.6Z"),
        line("M2.5 21.5C6.5 16.8 17.5 16.8 21.5 21.5"),
    ]


@icon("pet-recovery-suit", CAT, "Body suit for a pet seen from above with four sleeves and snaps down the middle",
      tags=["surgical suit", "post-op onesie", "after surgery", "cone alternative", "wound cover", "dog clothing"])
def _(S):
    pts = [(8, 3.5), (16, 3.5), (16, 5), (21, 5), (21, 9), (16, 9), (16, 14.5), (21, 14.5), (21, 18.5), (16, 18.5), (16, 21), (8, 21),
           (8, 18.5), (3, 18.5), (3, 14.5), (8, 14.5), (8, 9), (3, 9), (3, 5), (8, 5)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.7)),
        detail("M9.6 3.6A2.4 2.4 0 0 0 14.4 3.6"),
        dot(12, 9, 0.85), dot(12, 12.5, 0.85), dot(12, 16, 0.85),
    ]


@icon("drench-gun", CAT, "Pistol-grip dosing gun with a long nozzle and a tube running up to a small bottle",
      tags=["drenching", "oral dosing", "livestock medicine", "wormer", "dispensing gun", "sheep and cattle"])
def _(S):
    return [
        shell(poly([(3, 9.5), (15, 9.5), (15, 13.5), (10.5, 13.5), (9.6, 20), (5.4, 20), (6.4, 13.5), (3, 13.5)], closed=True, r=S.r)),
        line("M15 11.5H22"),
        line("M11.6 13.5V16.5"),
        shell(rect(3.5, 2, 5, 5.5, rr(S, 2))),
        line("M8.5 5C11 5 12 6.5 12 9.5"),
    ]


@icon("hoof-knife", CAT, "Hoof knife with a hooked blade and a wooden handle, shown at a slant",
      tags=["farrier tool", "hoof trimming", "horse care", "hoof care", "trimming knife", "blade"])
def _(S):
    R = lambda d: rotd(d, 45)
    return [
        shell(R("M10.6 11V6C10.6 3.4 13.2 2.4 16 3.6C14.8 4.8 14 6.2 14 8.4V11Z"), stroke_miterlimit="3"),
        shell(R(rect(10.6, 11, 3.4, 10.5, rr(S, 1.7)))),
    ]


@icon("livestock-ear-tag", CAT, "Cow face from the front with a rectangular numbered tag hanging from one ear",
      tags=["cattle id", "ear tagging", "herd management", "identification", "cow tag", "traceability"])
def _(S):
    return [
        shell(rect(8, 4.5, 8, 15.5, rr(S, 4))),
        line("M8 7.5L3.6 6.8"), line("M16 7.5L20.4 6.8"),
        line("M8.6 4.8L7.4 2"), line("M15.4 4.8L16.6 2"),
        shell(rect(1.8, 8, 3.8, 6.2, 1)),
        dot(10.7, 10, 0.85), dot(13.3, 10, 0.85),
        detail("M9 15.5H15"),
    ]


# ============================================================================ horse tack and stable

@icon("farrier", CAT, "Horseshoe with nail holes beside an upright farrier hammer",
      tags=["horseshoe", "horse hoof", "blacksmith", "shoeing", "equine care", "hoof trimmer"])
def _(S):
    shoe = "M2.5 21V13.8A5.5 5.5 0 0 1 13.5 13.8V21H9.5V13.8A1.5 1.5 0 0 0 6.5 13.8V21Z"
    if S.name != "line":
        shoe = "M3.5 21Q2.5 21 2.5 20V13.8A5.5 5.5 0 0 1 13.5 13.8V20Q13.5 21 12.5 21H10.5Q9.5 21 9.5 20V13.8A1.5 1.5 0 0 0 6.5 13.8V20Q6.5 21 5.5 21Z"
    return [
        shell(shoe),
        dot(4.5, 17.2, 0.7), dot(11.5, 17.2, 0.7),
        shell(rect(14, 3.5, 8, 5, rr(S, 2))),
        line("M18 8.5V21.5"),
    ]


@icon("saddle", CAT, "Side view of an English saddle with a raised cantle, a flat seat, a flap and a hanging stirrup",
      tags=["english saddle", "horse riding", "equestrian", "tack", "riding gear", "dressage"])
def _(S):
    seat = ("M2.5 10.5C2.5 8.3 4 7.6 5.6 8.6C8 10 13 10 16.4 8.4C18.4 7.4 21 7.8 21.5 10C21.5 11.5 20 12 18 12H4.5C3.3 12 2.5 11.4 2.5 10.5Z")
    flap = poly([(7.5, 12), (7.5, 20), (15.5, 20), (16, 12)], closed=True, r=L(S, 0.5, 2.5))
    return [
        shell(seat),
        shell(flap),
        line("M19 12V16.2"),
        shell(rect(17.4, 16.2, 3.6, 4.2, L(S, 0.5, 1.6))),
    ]


@icon("western-saddle", CAT, "Western saddle with a tall horn at the front, a deep seat, wide skirts and a hanging stirrup",
      tags=["stock saddle", "cowboy", "rodeo", "ranch", "horn", "trail riding"])
def _(S):
    body = ("M3 16V10.6C3 8.4 4 6.8 5.6 7.4C7.4 8.2 8.6 9.6 11 9.6C13.2 9.6 14.4 8.4 15.6 7.6H17.2C18.4 7.6 19 8.4 19 9.6V16"
            "C19 17 18.2 17.6 17.2 17.6H4.8C3.8 17.6 3 17 3 16Z")
    return [
        shell(body),
        line("M17 7.6V5"), shell(ellipse(17, 3.9, 2.4, 1.3)),
        line("M11 17.6V19.6"), shell(rect(8.6, 19.6, 4.8, 2.2, L(S, 0.5, 1))),
    ]


@icon("bridle", CAT, "Horse head in profile wearing a bridle with cheek, brow and nose straps",
      tags=["horse tack", "bit and bridle", "reins", "equestrian", "riding gear", "headstall"])
def _(S):
    head = L(S, "M12.5 2.5L15 5.5C18.5 7.5 20.5 13 20.5 21.5H11.5C11.5 19 10.5 18 9 18.6C6.5 19.8 3.5 18.8 3.5 16C3.5 13.5 5 11.8 6.5 9.5C8 7 9.5 5 12.5 2.5Z",
              "M12.2 3Q12.8 2.4 13.2 3L15 5.5C18.5 7.5 20.5 13 20.5 21.5H11.5C11.5 19 10.5 18 9 18.6C6.5 19.8 3.5 18.8 3.5 16C3.5 13.5 5 11.8 6.5 9.5C8 7 9.5 5 12.2 3Z")
    return [
        shell(head),
        detail("M13.6 6.4C12 9.6 10.4 12.6 9 16.6"),
        detail("M3.8 13.4L9.6 14.6"),
        dot(9.6, 9.6, 0.85),
    ]


@icon("halter", CAT, "Horse face from the front wearing a halter with a noseband, cheek straps and a brow strap",
      tags=["lead rope", "horse halter", "head collar", "leading", "tack", "stable gear"])
def _(S):
    face = L(S, "M7 6.2C7 4.4 9 3.8 12 3.8C15 3.8 17 4.4 17 6.2L17.6 14.5C17.7 18.6 15.4 21.5 12 21.5C8.6 21.5 6.3 18.6 6.4 14.5Z",
             "M7 6.2C7 4.4 9 3.8 12 3.8C15 3.8 17 4.4 17 6.2L17.6 14.5C17.7 18.6 15.4 21.5 12 21.5C8.6 21.5 6.3 18.6 6.4 14.5Z")
    return [
        shell(face),
        mark(poly([(7.4, 5), (6.2, 1.8), (9.8, 3.6)], closed=True, r=L(S, 0, 0.5))),
        mark(poly([(16.6, 5), (17.8, 1.8), (14.2, 3.6)], closed=True, r=L(S, 0, 0.5))),
        detail("M6.6 14.6H17.4"),
        detail("M9.8 7.4V14.6"), detail("M14.2 7.4V14.6"),
        dot(10.6, 18.6, 0.7), dot(13.4, 18.6, 0.7),
    ]


@icon("stirrup", CAT, "Metal stirrup iron with a slotted top bar, arched sides and a flat tread",
      tags=["riding stirrup", "saddle", "foot rest", "tack", "equestrian", "iron"])
def _(S):
    outer = "M8.5 3H15.5V6.2C18.2 9.6 20 14 20 18V21.5H4V18C4 14 5.8 9.6 8.5 6.2Z"
    if S.name != "line":
        outer = ("M9.5 3H14.5Q15.5 3 15.5 4V6.2C18.2 9.6 20 14 20 18V20.5Q20 21.5 19 21.5H5Q4 21.5 4 20.5V18C4 14 5.8 9.6 8.5 6.2V4Q8.5 3 9.5 3Z")
    return [
        shell(outer),
        detail("M8.2 17.6C8.2 14.6 9.6 11.6 12 9.4C14.4 11.6 15.8 14.6 15.8 17.6Z"),
    ]


@icon("hoof-pick", CAT, "Hoof pick with a hooked steel tip, a rubber handle and a fan of stiff brush bristles, shown at a slant",
      tags=["hoof cleaning", "horse grooming", "stable tool", "hoof care", "farrier", "pick"])
def _(S):
    R = lambda d: rotd(d, 40)
    return [
        line(R("M12 9V5.5C12 3.5 13.2 2.6 15 2.6")),
        shell(R(rect(9.2, 9, 5.6, 7.5, rr(S, 2.5)))),
        line(rseg(10, 16.5, 8, 21, 40)), line(rseg(12, 16.5, 12, 21.5, 40)), line(rseg(14, 16.5, 16, 21, 40)),
    ]


@icon("curry-comb", CAT, "Oval rubber curry comb with rings of small teeth nubs on its face",
      tags=["horse grooming", "currycomb", "stable brush", "coat care", "massage brush", "pet grooming"])
def _(S):
    out = [shell(rect(2.5, 4, 19, 16, L(S, 5, 8)))]
    for i in range(10):
        a = math.radians(i * 36)
        out.append(dot(12 + 5.6 * math.cos(a), 12 + 4.4 * math.sin(a), 0.9))
    for i in range(4):
        a = math.radians(45 + i * 90)
        out.append(dot(12 + 2 * math.cos(a), 12 + 1.6 * math.sin(a), 0.85))
    return out


@icon("horse-blanket", CAT, "Horse in side view wearing a rug with front and rear edges and belly straps",
      tags=["horse rug", "turnout rug", "winter blanket", "stable rug", "equestrian", "horse clothing"])
def _(S):
    body = [(3.5, 8), (12.5, 7.4), (14, 3.8), (15.6, 2.4), (16.6, 4.2), (19.5, 7), (21.5, 8.6), (21.5, 10.4), (19.4, 10.8), (17.6, 9.8),
            (16.4, 13.6), (3.8, 13.6)]
    return [
        shell(poly(body, closed=True, r=S.r * 0.6)),
        detail("M7.4 7.8V13.6"), detail("M12.4 7.6V13.6"),
        line("M5 13.6V21"), line("M8.4 13.6V21"), line("M13.4 13.6V21"), line("M16.4 13.6V21"),
        line("M3.6 8.6C2 10 2 12 2.6 14"),
    ]


HORSE_HEAD = ("M12.5 2.5L15 5.5C18.5 7.5 20.5 13 20.5 21.5H11.5C11.5 19 10.5 18 9 18.6C6.5 19.8 3.5 18.8 3.5 16C3.5 13.5 5 11.8 6.5 9.5"
              "C8 7 9.5 5 12.5 2.5Z")
HORSE_HEAD_R = ("M12.2 3Q12.8 2.4 13.2 3L15 5.5C18.5 7.5 20.5 13 20.5 21.5H11.5C11.5 19 10.5 18 9 18.6C6.5 19.8 3.5 18.8 3.5 16"
                "C3.5 13.5 5 11.8 6.5 9.5C8 7 9.5 5 12.2 3Z")


@icon("horse-fly-mask", CAT, "Horse head in profile wearing a mesh fly mask over the eye and ears",
      tags=["fly protection", "insect mask", "horse gear", "summer turnout", "eye protection", "equestrian"])
def _(S):
    return [
        shell(L(S, HORSE_HEAD, HORSE_HEAD_R)),
        detail("M13.2 4.6C15.6 8.8 14.6 12 10 12.4C6.8 12.2 6.6 8.6 8.6 6.6"),
        dot(10.2, 8.4, 0.75), dot(12.6, 9.6, 0.75),
    ]


@icon("hay-net", CAT, "Bulging net bag full of hay hung from a single rope",
      tags=["haynet", "slow feeder", "stable", "forage", "horse feed", "hanging net"])
def _(S):
    bag = "M12 7C17 7 20 10.6 20 14.6C20 18.8 16.6 21.5 12 21.5C7.4 21.5 4 18.8 4 14.6C4 10.6 7 7 12 7Z"
    return [
        shell(bag),
        line("M12 7V2.8"),
        line("M8.6 6.4L7.6 3.6"), line("M15.4 6.4L16.4 3.6"),
        detail("M6.6 11.8L14.6 20"), detail("M11 8.6L18.4 16"), detail("M17.4 11.8L9.4 20"), detail("M13 8.6L5.6 16"),
    ]


@icon("horse-trailer", CAT, "Two-horse trailer in side view with a rounded roof, a window, a rear ramp and a hitch",
      tags=["horsebox", "float", "transport", "equestrian", "towing", "horse transport"])
def _(S):
    body = "M3.5 17V8C3.5 5.4 5.4 4.5 8 4.5H17.5C19.5 4.5 20.5 5.6 20.5 7.6V17Z"
    return [
        shell(body),
        shell(rect(7, 7.6, 5, 3.6, L(S, 0.6, 1.4))),
        detail("M16 7.4V17"),
        line("M3.5 17L2.3 21"),
        line("M20.5 15.5L23 18.5"),
        shell(circle(11, 18.6, 2.6)),
    ]


@icon("horse-stable", CAT, "Stable stall front with a half door and a horse head looking over it",
      tags=["stall", "barn", "box stall", "horse housing", "livery", "equestrian"])
def _(S):
    head = scl(L(S, HORSE_HEAD, HORSE_HEAD_R), 0.42, 12, 7.6)
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 3.5))),
        mark(head),
        detail("M3 12.5H21"),
        detail("M8.2 12.5V21.5"), detail("M12 12.5V21.5"), detail("M15.8 12.5V21.5"),
    ]


@icon("horse-nosebag", CAT, "Horse head in profile with a feed bag hanging over its muzzle on a strap over the ears",
      tags=["feed bag", "feeding horse", "grain bag", "muzzle feeder", "trail feeding", "equestrian"])
def _(S):
    return [
        shell(L(S, HORSE_HEAD, HORSE_HEAD_R)),
        detail(poly([(2.6, 13.4), (10.2, 13.4), (9.2, 21), (3.6, 21)], closed=True, r=S.r * 0.4)),
        detail("M10.2 13.6C11 10.6 12 8.2 13.4 5.6"),
        dot(10.6, 9.8, 0.85),
    ]


@icon("riding-helmet", CAT, "Riding helmet with a short peak at the front, a band and a chin strap",
      tags=["equestrian helmet", "horse riding", "safety hat", "jockey cap", "head protection", "show jumping"])
def _(S):
    dome = "M3.5 16C3.5 8.4 7.4 4.5 12.5 4.5C17.4 4.5 20.4 8.2 20.4 13L22 15V16Z"
    if S.name != "line":
        dome = "M3.5 16C3.5 8.4 7.4 4.5 12.5 4.5C17.4 4.5 20.4 8.2 20.4 13L21.4 14.2Q22 15 21.2 15.6L20.4 16Z"
    return [
        shell(dome),
        detail("M3.8 12.6H20.3"),
        line("M7 16V20.5"), dot(7, 20.8, 1.1),
    ]


@icon("hay-bale", CAT, "Rectangular hay bale in perspective with two binding bands around it",
      tags=["straw bale", "square bale", "farm", "fodder", "harvest", "bedding"])
def _(S):
    return [
        shell(rect(2.5, 9, 14, 11.5, rr(S, 1.5))),
        shell(poly([(2.5, 9), (7, 4), (21.5, 4), (16.5, 9)], closed=True, r=L(S, 0.8, 1.6))),
        shell(poly([(16.5, 9), (21.5, 4), (21.5, 15.5), (16.5, 20.5)], closed=True, r=L(S, 0.8, 1.6))),
        detail("M7.4 9V20.5"), detail("M12 9V20.5"),
    ]


@icon("round-hay-bale", CAT, "Large round hay bale seen end-on with a spiral of rolled hay on its face",
      tags=["round bale", "big bale", "silage", "harvest", "field", "fodder"])
def _(S):
    pts = []
    for i in range(41):
        t = i / 40
        a = t * 4.2 * math.pi
        rad = 1 + t * 5.3
        pts.append((12 + rad * math.cos(a), 12 + rad * math.sin(a)))
    outer = poly(regular(12, 12, 9.4, 14), closed=True, r=L(S, 0.3, 6)) if S.name == "line" else circle(12, 12, 9.4)
    return [shell(outer), detail(poly(pts))]


# ============================================================================ feed, dairy and livestock handling

@icon("feed-trough", CAT, "Long trough on short splayed legs heaped with feed",
      tags=["feeding trough", "livestock feeder", "pig trough", "farm", "animal feed", "manger"])
def _(S):
    return [
        shell(poly([(2.5, 11.5), (21.5, 11.5), (19.5, 17.5), (4.5, 17.5)], closed=True, r=S.r * 0.6)),
        line("M5 11C6.5 6.6 17.5 6.6 19 11"),
        line("M6.4 17.5L5 21.5"), line("M17.6 17.5L19 21.5"),
    ]


@icon("water-trough", CAT, "Rectangular metal stock tank with wavy water lines inside",
      tags=["stock tank", "livestock water", "drinking trough", "farm", "cattle", "horse water"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 19, 14, rr(S, 3.5))),
        detail("M5.8 11.6C7.4 9.9 9 9.9 10.6 11.6S13.8 13.3 15.4 11.6S18.4 10.4 18.4 10.4"),
        detail("M5.8 16C7.4 14.3 9 14.3 10.6 16S13.8 17.7 15.4 16S18.4 14.8 18.4 14.8"),
    ]


@icon("feed-bucket", CAT, "Flat-sided bucket with a hanging hook at the rim and a mound of grain in it",
      tags=["grain bucket", "feed pail", "horse feed", "stable", "hanging bucket", "pail"])
def _(S):
    return [
        shell(poly([(3.5, 8), (20.5, 8), (18.6, 20), (17.6, 21.5), (6.4, 21.5), (5.4, 20)], closed=True, r=S.r * 0.6)),
        line("M6.5 7.6C8 4.2 16 4.2 17.5 7.6"),
        line("M19 8V3.6C19 2.8 19.6 2.4 20.4 2.4H21.6"),
    ]


@icon("feed-sack", CAT, "Tied sack with a tuft at the neck and an ear of grain on the front",
      tags=["grain sack", "burlap", "animal feed", "bag of feed", "farm supplies", "seed bag"])
def _(S):
    sack = ("M9 5H15L16.4 8C19.4 9.8 20.6 13 20.6 16.6C20.6 19.8 18.6 21.5 15.6 21.5H8.4C5.4 21.5 3.4 19.8 3.4 16.6"
            "C3.4 13 4.6 9.8 7.6 8Z")
    grains = [mark(rotd(ellipse(x, y, 0.85, 1.5), a, x, y)) for x, y, a in
              ((10.4, 15.4, -30), (13.6, 15.4, 30), (10.4, 18, -30), (13.6, 18, 30), (12, 13, 0))]
    return [
        shell(sack),
        detail("M7.6 8.4H16.4"),
        line("M10 5L9 2.8"), line("M14 5L15 2.8"),
        *grains,
        mark(rect(11.5, 14, 1, 6.5)),
    ]


@icon("salt-lick", CAT, "Square mineral block in perspective with an oval lick groove worn into its top",
      tags=["mineral block", "livestock salt", "horse lick", "cattle", "supplement", "farm"])
def _(S):
    return [
        shell(rect(2.5, 10, 14.5, 11, rr(S, 1.5))),
        shell(poly([(2.5, 10), (6.5, 5), (21.5, 5), (17, 10)], closed=True, r=L(S, 0.8, 1.6))),
        shell(poly([(17, 10), (21.5, 5), (21.5, 16), (17, 21)], closed=True, r=L(S, 0.8, 1.6))),
        mark(ellipse(12, 7.5, 3.6, 1)),
    ]


@icon("chicken-feeder", CAT, "Tube feeder with a pointed lid on top and a round pan at the bottom holding grain",
      tags=["poultry feeder", "hen feeder", "coop", "grain dispenser", "chicken supplies", "backyard chickens"])
def _(S):
    return [
        shell(poly([(8, 6), (12, 2.4), (16, 6)], closed=True, r=S.r * 0.6)),
        shell(rect(8.5, 6, 7, 8.5, rr(S, 1.5))),
        shell(poly([(3, 17.5), (21, 17.5), (19.4, 21.5), (4.6, 21.5)], closed=True, r=S.r * 0.5)),
        mark(poly([(9, 17.5), (12, 14.8), (15, 17.5)], closed=True)),
    ]


@icon("poultry-waterer", CAT, "Domed drinker with a carry handle on top standing in a shallow ring of water",
      tags=["chicken waterer", "hen drinker", "coop", "bird water", "backyard chickens", "gravity waterer"])
def _(S):
    dome = "M5 16.5C5 9.8 8 6.4 12 6.4C16 6.4 19 9.8 19 16.5Z"
    return [
        shell(dome),
        line("M9 6.4V4.6C9 3.4 10 2.6 12 2.6C14 2.6 15 3.4 15 4.6V6.4"),
        shell(rect(2.5, 16.5, 19, 5, rr(S, 2.5))),
        mark("M12 9.6C12 9.6 10.3 11.6 10.3 12.8A1.7 1.7 0 0 0 13.7 12.8C13.7 11.6 12 9.6 12 9.6Z"),
    ]


@icon("nest-box", CAT, "Wooden nest box with an open front, straw along the bottom and an egg resting inside",
      tags=["laying box", "hen house", "chicken coop", "egg laying", "poultry", "nesting"])
def _(S):
    egg = "M12 8.6C14.6 8.6 15.8 12 15.8 13.8C15.8 16.2 14.2 17.6 12 17.6C9.8 17.6 8.2 16.2 8.2 13.8C8.2 12 9.4 8.6 12 8.6Z"
    return [
        shell(rect(3, 3.5, 18, 18, rr(S, 3.5))),
        detail("M3 7.6H21"),
        detail(egg),
        line("M6.6 20L8.2 18.4"), line("M17.4 20L15.8 18.4"),
    ]


@icon("milking-stool", CAT, "Small three-legged stool with a round seat, seen from the side",
      tags=["dairy", "milking", "farm stool", "three-legged", "cow", "barn"])
def _(S):
    return [
        shell(rect(2.5, 5, 19, 4.5, L(S, 2, 2.25))),
        line("M7 9.5L4.2 21.5"), line("M17 9.5L19.8 21.5"), line("M12 9.5V21.5"),
    ]


@icon("milking-machine", CAT, "Milking claw with a round collector, two hoses above and four teat cups below",
      tags=["dairy", "cow milking", "milking cluster", "teat cup", "dairy farm", "milking parlour"])
def _(S):
    return [
        shell(circle(12, 10.5, 3.2)),
        line("M10.6 7.6L7 2.8"), line("M13.4 7.6L17 2.8"),
        line("M10 12.6L4.6 21"), line("M11.3 13.6L8.6 21.5"), line("M12.7 13.6L15.4 21.5"), line("M14 12.6L19.4 21"),
    ]


@icon("cow-bell", CAT, "Tapered square bell with a wide strap loop on top and a clapper hanging below",
      tags=["cattle bell", "farm bell", "alpine", "livestock", "pasture", "neck bell"])
def _(S):
    return [
        line("M8.6 7.5V4.4C8.6 3.2 9.2 2.6 10.4 2.6H13.6C14.8 2.6 15.4 3.2 15.4 4.4V7.5"),
        shell(poly([(7.4, 7.5), (16.6, 7.5), (19.6, 18), (4.4, 18)], closed=True, r=S.r)),
        detail("M6.4 14H17.6"),
        mark(circle(12, 20.8, 1.3)),
    ]


@icon("branding-iron", CAT, "Long rod with a T handle at one end and a diamond brand face at the other, shown at a slant",
      tags=["cattle brand", "ranch", "hot iron", "livestock marking", "cowboy", "western"])
def _(S):
    R = lambda d: rotd(d, 45)
    return [
        shell(R(poly([(12, 2.4), (16.4, 6.6), (12, 10.8), (7.6, 6.6)], closed=True, r=S.r * 0.6))),
        line(rseg(12, 10.8, 12, 20, 45)),
        line(rseg(8, 21, 16, 21, 45)),
    ]


@icon("bull-nose-ring", CAT, "Bull face from the front with curved horns and a large ring through its nose",
      tags=["bull ring", "cattle handling", "livestock", "nose ring", "farm", "bull"])
def _(S):
    return [
        shell(rect(7.5, 5, 9, 11.5, rr(S, 4))),
        line("M7.5 7.5C4 8 2.8 5.6 3.4 3"), line("M16.5 7.5C20 8 21.2 5.6 20.6 3"),
        dot(10.6, 9.6, 0.85), dot(13.4, 9.6, 0.85),
        dot(10.8, 13.6, 0.7), dot(13.2, 13.6, 0.7),
        line(circle(12, 17.6, 2.8)),
    ]


@icon("shepherds-crook", CAT, "Tall staff with a round hook curled over at the top",
      tags=["shepherd", "crook", "staff", "sheep handling", "pastoral", "flock"])
def _(S):
    return [line("M8.5 21.5V9C8.5 4.6 11 2.5 14 2.5C17 2.5 19 4.4 19 7C19 9 17.6 10.4 15.8 10.4")]


@icon("pitchfork", CAT, "Long handle with three long curved tines",
      tags=["hay fork", "farm tool", "manure fork", "stable", "agriculture", "garden fork"])
def _(S):
    return [
        line("M6 2.5V9C6 11.4 8.4 12.8 12 12.8C15.6 12.8 18 11.4 18 9V2.5"),
        line("M12 2.5V12.8"),
        line("M12 12.8V21.5"),
    ]


@icon("cattle-grid", CAT, "Road crossing made of parallel metal bars laid over a pit, seen in perspective",
      tags=["cattle guard", "stock grid", "livestock barrier", "farm road", "rural", "gate alternative"])
def _(S):
    return [
        shell(poly([(7, 3), (17, 3), (22, 21), (2, 21)], closed=True, r=S.r * 0.6)),
        detail("M5.6 8H18.4"), detail("M4.4 12.5H19.6"), detail("M3.1 17H20.9"),
    ]


@icon("livestock-trailer", CAT, "Long trailer with slatted sides, wheels and a hitch, a cow head showing through a slot",
      tags=["cattle trailer", "animal transport", "stock trailer", "haulage", "farm vehicle", "towing"])
def _(S):
    return [
        shell(rect(2.5, 5, 18, 12, rr(S, 2))),
        detail("M2.5 8.6H20.5"), detail("M2.5 13.4H20.5"),
        mark(ellipse(8, 11, 2.6, 1.3)),
        mark(poly([(6, 10), (5.4, 8.8), (7, 9.4)], closed=True)), mark(poly([(10, 10), (10.6, 8.8), (9, 9.4)], closed=True)),
        line("M20.5 14.5L23 17.5"),
        shell(circle(8, 19, 2.4)), shell(circle(15.5, 19, 2.4)),
    ]


@icon("squeeze-chute", CAT, "Metal cattle chute of barred panels with a U-shaped head gate at the front",
      tags=["cattle crush", "livestock handling", "head catch", "vet restraint", "ranch", "headgate"])
def _(S):
    return [
        shell(rect(3, 3, 18, 16, S.R)),
        detail("M7.4 3V19"), detail("M11 3V19"),
        detail("M14.8 3V9.6A2.2 2.2 0 0 0 19.2 9.6V3"),
        line("M5 19V21.5"), line("M19 19V21.5"),
    ]


@icon("electric-fence", CAT, "Fence posts with two live wire strands on insulators and a sign showing a lightning bolt",
      tags=["electric wire", "livestock fence", "paddock", "pasture fence", "shock warning", "farm"])
def _(S):
    return [
        shell(rect(7.5, 2.5, 9, 7, rr(S, 1.5))),
        mark(poly([(12.8, 3.8), (9.8, 6.6), (11.8, 6.6), (11, 8.8), (14.2, 5.8), (12.2, 5.8)], closed=True)),
        line("M4 12.5V21.5"), line("M20 12.5V21.5"),
        line("M2.5 15H21.5"), line("M2.5 19H21.5"),
        dot(4, 15, 1.2), dot(20, 15, 1.2), dot(4, 19, 1.2), dot(20, 19, 1.2),
    ]


@icon("pigpen", CAT, "Low wooden pen fence with a pig standing behind the rails",
      tags=["pig pen", "sty", "hog pen", "swine", "farm", "pig enclosure"])
def _(S):
    pig = path_to_d(U(P(ellipse(11.5, 8.2, 6, 3.6)), P(circle(18.2, 8.6, 2.6)), P(rect(7, 9.5, 2, 4.5)), P(rect(14, 9.5, 2, 4.5)),
                       P(poly([(18.5, 5.6), (20.6, 4.6), (20.2, 7.4)], closed=True))))
    return [
        mark(pig),
        line("M2 15.5H22"), line("M2 20H22"),
        line("M4 13V21.5"), line("M12 13V21.5"), line("M20 13V21.5"),
    ]
