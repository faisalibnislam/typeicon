"""TypeIcon Core: health & medical.

No red-cross emblem: medical crosses are plain plus signs on neutral objects (buildings, kits, boards).
Identifying detail is kept out of the bottom-right quadrant where possible (variant badges sit there).
"""
import math

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path

from dsl import Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import LINE, D, I, P, ST, U, fmt, path_to_d, polar, rotation  # noqa: F401

CAT = "health"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def xf(d, matrix):
    """Apply an affine (a, b, c, d, e, f) to a d-string, keeping open sub-paths open."""
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, matrix))
    return pen.getCommands()


def rot(d, deg, cx=12.0, cy=12.0):
    return xf(d, rotation(deg, cx, cy))


def move(d, dx, dy, s=1.0, ox=12.0, oy=12.0):
    """Scale about (ox, oy) then translate."""
    return xf(d, (s, 0, 0, s, ox - s * ox + dx, oy - s * oy + dy))


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


def plus(cx, cy, a):
    """Plus sign (two strokes) centred on (cx, cy) with arm length a."""
    return f"M{fmt(cx - a)} {fmt(cy)}H{fmt(cx + a)}M{fmt(cx)} {fmt(cy - a)}V{fmt(cy + a)}"


def outline_region(d, w=2.0):
    """Solid region of a closed outline filled to its outer stroke edge."""
    return U(P(d), ST(d, w))


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


HEART = "M12 20L4.4 12.6A4.6 4.6 0 0 1 11 6.3L12 7.3L13 6.3A4.6 4.6 0 0 1 19.6 12.6Z"
HEART_R = ("M10.6 18.6L4.4 12.6A4.6 4.6 0 0 1 11 6.3L11.3 6.6Q12 7.3 12.7 6.6L13 6.3A4.6 4.6 0 0 1 19.6 12.6"
           "L13.4 18.6Q12 20 10.6 18.6Z")


def heart(S):
    return L(S, HEART, HEART_R)


# ============================================================================ places and kits

@icon("hospital", CAT, "Hospital building with a plus sign on the central tower",
      tags=["clinic", "medical center", "infirmary", "building", "emergency", "healthcare"], aliases=["clinic"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 10), (7, 10), (7, 3), (17, 3), (17, 10), (21, 10), (21, 21)], closed=True, r=S.r)),
        detail(plus(12, 8, 2.5)),
        detail(poly([(10, 21), (10, 16.5), (14, 16.5), (14, 21)], r=S.r * 0.5)),
    ]


_AMB_BODY = [(5, 18), (3, 18), (3, 6), (14, 6), (14, 9), (18, 9), (21, 13), (21, 18), (19, 18)]
_AMB_WHEELS = ((7, 18), (17, 18))


def _amb_filled():
    body = outline_region(poly(_AMB_BODY, closed=True))
    cut = U(*[P(circle(x, y, 4)) for x, y in _AMB_WHEELS])
    wheels = U(*[P(circle(x, y, 3)) for x, y in _AMB_WHEELS])
    knock = U(ST(plus(8.5, 11, 2.5)), P(poly([(15, 10.5), (17.4, 10.5), (19.4, 13.5), (15, 13.5)], closed=True)))
    return U(D(body, cut, knock), wheels)


@icon("ambulance", CAT, "Ambulance van with a plus sign on its side",
      tags=["emergency", "paramedic", "vehicle", "rescue", "911", "hospital"], filled=_amb_filled)
def _(S):
    return [
        shell(poly(_AMB_BODY, r=S.r)),
        line(seg(9, 18, 15, 18)),
        *[shell(circle(x, y, 2)) for x, y in _AMB_WHEELS],
        detail(plus(8.5, 11, 2.5)),
        detail(poly([(14, 9), (14, 13), (21, 13)], r=S.r * 0.5)),
    ]


@icon("first-aid", CAT, "First-aid kit: a case with a handle and a plus sign",
      tags=["first aid kit", "medical kit", "emergency", "aid", "case", "health"], aliases=["first-aid-kit", "medkit"])
def _(S):
    return [
        shell(rect(3, 7, 18, 13.5, S.R)),
        line(poly([(9, 7), (9, 4), (15, 4), (15, 7)], r=S.r * 0.66)),
        detail(plus(12, 13.75, 3)),
    ]


@icon("medical-cross", CAT, "Plain medical plus-shaped cross",
      tags=["medical", "health", "plus", "pharmacy", "care", "clinic"], aliases=["health-cross"])
def _(S):
    a, b = 8.75, 15.25
    return [shell(poly([(a, 3), (b, 3), (b, a), (21, a), (21, b), (b, b), (b, 21), (a, 21), (a, b), (3, b), (3, a), (a, a)],
                       closed=True, r=S.r))]


# ============================================================================ instruments

@icon("stethoscope", CAT, "Stethoscope with earpieces, tubing and a chest piece",
      tags=["doctor", "physician", "checkup", "exam", "heart", "listen"])
def _(S):
    return [
        line("M4 3V8.5A4.25 4.25 0 0 0 12.5 8.5V3"),
        dot(4, 3, 1.25), dot(12.5, 3, 1.25),
        line(poly([(8.25, 12.75), (8.25, 20), (18.5, 20), (18.5, 13.5)], r=L(S, 2.5, 5))),
        shell(circle(18.5, 11, 2.5)),
    ]


@icon("syringe", CAT, "Syringe with a needle, graduated barrel and plunger",
      tags=["injection", "needle", "shot", "jab", "vaccination", "medicine"], aliases=["injection"])
def _(S):
    m = axis((12, 12), -45)
    barrel = [m(-5, -3), m(5.5, -3), m(5.5, 3), m(-5, 3)]
    return [
        shell(poly(barrel, closed=True, r=S.r * 0.5)),
        detail(mseg(m, -2, -3, -2, -0.5)), detail(mseg(m, 1.5, -3, 1.5, -0.5)),
        line(mseg(m, 5.5, -5.5, 5.5, 5.5)),
        line(mseg(m, 5.5, 0, 9, 0)), line(mseg(m, 9, -3, 9, 3)),
        line(mseg(m, -9.5, 0, -5, 0)),
    ]


@icon("pill", CAT, "Oblong pill split into two halves",
      tags=["medicine", "tablet", "drug", "medication", "pharmacy", "dose"], aliases=["tablet-pill"])
def _(S):
    m = axis((12, 12), -45)
    return [shell(stadium(m, -8.5, 8.5, 4, L(S, 3, 4))), detail(mseg(m, 0, -4, 0, 4))]


@icon("pills", CAT, "A capsule and a round tablet",
      tags=["medicine", "tablets", "drugs", "medication", "pharmacy", "prescription"], aliases=["medication"])
def _(S):
    m = axis((8, 16), -45)
    return [
        shell(stadium(m, -5.5, 5.5, 3, L(S, 2.25, 3))), detail(mseg(m, 0, -3, 0, 3)),
        shell(circle(17, 7, 3.75)), detail(seg(13.25, 7, 20.75, 7)),
    ]


@icon("capsule", CAT, "Medicine capsule with granules in one half",
      tags=["medicine", "pill", "gel cap", "drug", "medication", "supplement"], aliases=["gel-cap"])
def _(S):
    m = axis((12, 12), -45)
    return [shell(stadium(m, -8.5, 8.5, 4, L(S, 3, 4))), detail(mseg(m, 0, -4, 0, 4)),
            dot(*m(3.25, -1.25), 1), dot(*m(5.75, 0.5), 1), dot(*m(3.5, 1.75), 1)]


@icon("bandage", CAT, "Roll of gauze bandage partly unrolled",
      tags=["gauze", "dressing", "wrap", "roll", "wound", "first aid"], aliases=["gauze"])
def _(S):
    strip = poly([(9, 12), (21, 12), (20, 14), (21, 16), (9, 16)], closed=True, r=S.r * 0.5)
    return [shell(union(circle(9, 10, 6), strip)), detail(circle(9, 10, 2))]


@icon("medical-thermometer", CAT, "Digital clinical thermometer with a display",
      tags=["thermometer", "temperature", "fever", "digital", "body temperature", "clinical"],
      aliases=["clinical-thermometer"])
def _(S):
    m = axis((12, 12), -45)
    return [
        shell(stadium(m, -3.5, 9.5, 3, L(S, 1.5, 3))),
        detail(mseg(m, 0.5, 0, 5.5, 0)),
        line(mseg(m, -9, 0, -3.5, 0)),
        dot(*m(-9.5, 0), 1.35),
    ]


# ============================================================================ heart and vitals

@icon("heart-pulse", CAT, "Heart with a pulse line across it",
      tags=["heart rate", "pulse", "cardio", "health", "vital signs", "cardiology"], aliases=["heart-rate"])
def _(S):
    return [shell(heart(S)),
            detail(poly([(6.5, 12.5), (9, 12.5), (10.5, 10), (13, 15.5), (14.5, 12.5), (17.5, 12.5)], r=S.r * 0.5))]


@icon("heartbeat", CAT, "Beating heart with pulse marks on both sides",
      tags=["pulse", "heart", "beat", "cardio", "alive", "rhythm"])
def _(S):
    small = move(heart(S), 0, -0.3, 0.72, 12, 13)
    return [
        shell(small),
        line(L(S, "M4.5 8.5C2.5 10.8 2.5 14.2 4.5 16.5", "M4.5 8.5C2.5 10.8 2.5 14.2 4.5 16.5")),
        line("M19.5 8.5C21.5 10.8 21.5 14.2 19.5 16.5"),
    ]


@icon("ecg", CAT, "Monitor showing an electrocardiogram trace",
      tags=["electrocardiogram", "ekg", "heart monitor", "cardiogram", "pulse", "vital signs"],
      aliases=["ekg", "electrocardiogram"])
def _(S):
    return [
        shell(rect(2.5, 4, 19, 16, S.R)),
        detail(poly([(5.5, 12.5), (8, 12.5), (9.5, 9.5), (11.5, 16.5), (13.5, 7.5), (15, 12.5), (18.5, 12.5)], r=S.r * 0.4)),
    ]


@icon("blood-pressure", CAT, "Blood-pressure gauge with an inflation bulb",
      tags=["sphygmomanometer", "hypertension", "bp", "gauge", "vital signs", "cuff"],
      aliases=["sphygmomanometer"])
def _(S):
    m = axis((18.5, 6.75), 90)
    return [
        shell(circle(9.5, 14.5, 6.5)),
        detail(seg(9.5, 14.5, 12.25, 11.75)), dot(9.5, 14.5, 1.5),
        line(poly([(16, 14.5), (18.5, 14.5), (18.5, 11)], r=L(S, 0, 2))),
        shell(stadium(m, -3.75, 4.25, 2.25, L(S, 1.5, 2.25))),
    ]


# ============================================================================ laboratory

@icon("microscope", CAT, "Laboratory microscope with a tilted tube, stage and base",
      tags=["lab", "laboratory", "science", "research", "biology", "magnify"])
def _(S):
    m = axis((9, 7.5), 63.4)
    tube = [m(-5, -2), m(4, -2), m(4, 2), m(-5, 2)]
    return [
        shell(poly(tube, closed=True, r=S.r * 0.5)),
        line(mseg(m, 4, 0, 6, 0)),
        line(seg(5.5, 16, 13, 16)),
        line(L(S, "M14 11C19 12 20 18 15.5 20.5", "M14 11C19 12 20 18 15.5 20.5")),
        line(seg(4.5, 20.5, 19.5, 20.5)),
    ]


_TT = "M9 3.5H15V16A3 3 0 0 1 9 16Z"
_TT_LIQ = "M9 11H15V16A3 3 0 0 1 9 16Z"


def _tt_filled():
    tube = rot(_TT, 30)
    ring = D(outline_region(tube), P(tube))
    return U(ring, P(rot(_TT_LIQ, 30)), ST(rot("M7.5 3.5H16.5", 30), 2.5))


@icon("test-tube", CAT, "Test tube holding liquid",
      tags=["lab", "laboratory", "sample", "chemistry", "experiment", "blood test"], filled=_tt_filled)
def _(S):
    walls = poly([(9, 3.5), (9, 16)], r=0) + "A3 3 0 0 0 15 16V3.5"
    return [
        line(rot(walls, 30)),
        line(rot("M7.5 3.5H16.5" if S.name == "line" else "M8 3.5H16", 30)),
        detail(rot("M9 11H15", 30)),
    ]


@icon("flask", CAT, "Conical laboratory flask with liquid",
      tags=["erlenmeyer", "lab", "chemistry", "experiment", "science", "potion"], aliases=["erlenmeyer-flask"])
def _(S):
    return [
        shell(poly([(9.5, 3), (14.5, 3), (14.5, 9), (20.5, 20.5), (3.5, 20.5), (9.5, 9)], closed=True, r=S.r)),
        detail(seg(6.6, 15, 17.4, 15)),
    ]


def frame(d, origin, deg):
    """Place a d-string drawn in a local frame (x along `deg`) at `origin`."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return xf(d, (c, s, -s, c, origin[0], origin[1]))


@icon("bacteria", CAT, "Rod-shaped bacterium with a whip-like tail",
      tags=["germ", "microbe", "bacterium", "infection", "microbiology", "bacillus"], aliases=["germ", "bacterium"])
def _(S):
    o, a = (10, 14), -40
    m = axis(o, a)
    return [
        shell(stadium(m, -7.5, 5, 3.75, L(S, 3, 3.75))),
        dot(*m(-4, 0.75), 1), dot(*m(-1, -1.25), 1), dot(*m(2, 0.75), 1),
        line(frame("M5 0C6.5 -1.75 7.5 -1.75 8.5 0S10.5 1.75 12 0", o, a)),
    ]


@icon("vaccine", CAT, "Vaccine vial beside a syringe",
      tags=["vaccination", "immunization", "shot", "jab", "vial", "injection"], aliases=["vaccination", "immunization"])
def _(S):
    vial = [(5, 3.5), (9, 3.5), (9, 6.5), (10.5, 8), (10.5, 21), (3.5, 21), (3.5, 8), (5, 6.5)]
    return [
        shell(poly(vial, closed=True, r=S.r * 0.5)),
        detail(seg(5, 6.5, 9, 6.5)), detail(seg(3.5, 12.5, 10.5, 12.5)), detail(seg(3.5, 16.5, 10.5, 16.5)),
        line(seg(17, 2, 17, 6)),
        shell(rect(14.5, 6, 5, 10, min(S.R, 1))),
        detail(seg(17, 9, 19.5, 9)), detail(seg(17, 12, 19.5, 12)),
        line(seg(13.5, 16, 20.5, 16)), line(seg(17, 16, 17, 19.5)), line(seg(15, 20, 19, 20)),
    ]


@icon("face-mask", CAT, "Surgical face mask with pleats and ear loops",
      tags=["mask", "surgical mask", "covid", "protection", "respirator", "hygiene"], aliases=["surgical-mask"])
def _(S):
    body = [(6.5, 7.5), (12, 6.5), (17.5, 7.5), (17.5, 15), (12, 17.5), (6.5, 15)]
    return [
        shell(poly(body, closed=True, r=S.r)),
        detail(seg(9, 10.5, 15, 10.5)), detail(seg(9, 13.5, 15, 13.5)),
        line("M6.5 8.5C4.2 8.5 3 9.8 3 11.5C3 13.2 4.2 14.5 6.5 14.5"),
        line("M17.5 8.5C19.8 8.5 21 9.8 21 11.5C21 13.2 19.8 14.5 17.5 14.5"),
    ]


@icon("wheelchair", CAT, "Wheelchair seen from the side",
      tags=["accessibility", "disability", "mobility", "accessible", "handicap", "chair"])
def _(S):
    return [
        line(circle(9.5, 15.5, 5.5)), dot(9.5, 15.5, 1.5),
        line(poly([(4.5, 2.5), (6, 7.5), (15.5, 7.5), (17.5, 17.5), (20.5, 17.5)], r=S.r)),
        dot(17.5, 20.5, 1.5),
    ]


@icon("crutch", CAT, "Underarm crutch with a padded top, hand grip and rubber tip",
      tags=["injury", "mobility", "walking aid", "broken leg", "support", "rehab"])
def _(S):
    t = lambda d: rot(d, 30)  # noqa: E731
    return [
        shell(t(rect(7.5, 2, 9, 2.5, L(S, 0.5, 1.25)))),
        line(t(poly([(9.5, 4.5), (10, 14), (12, 16.5), (14, 14), (14.5, 4.5)], r=S.r * 0.5))),
        line(t(seg(9.8, 10, 14.2, 10))),
        line(t(seg(12, 16.5, 12, 19))),
        shell(t(rect(10.5, 19, 3, 2.5, L(S, 0.5, 1.25)))),
    ]


@icon("x-ray", CAT, "Chest X-ray film showing the spine and ribs",
      tags=["xray", "radiology", "radiograph", "scan", "ribs", "imaging"], aliases=["xray", "radiograph"])
def _(S):
    out = [shell(rect(3, 3, 18, 18, S.R)), detail(seg(12, 5.5, 12, 18.5))]
    for y in (7, 11, 15):
        out.append(detail(poly([(12, y), (8.5, y), (6.5, y + 2)], r=S.r)))
        out.append(detail(poly([(12, y), (15.5, y), (17.5, y + 2)], r=S.r)))
    return out


@icon("body-scan", CAT, "Full standing figure inside scanner brackets with a scan line",
      tags=["scan", "mri", "ct scan", "full body", "screening", "imaging"], aliases=["full-body-scan"])
def _(S):
    corners = [
        [(3, 7), (3, 3), (7, 3)], [(17, 3), (21, 3), (21, 7)],
        [(21, 17), (21, 21), (17, 21)], [(7, 21), (3, 21), (3, 17)],
    ]
    figure = poly([(9, 8.5), (15, 8.5), (15, 14), (13.5, 14), (13.5, 19.5), (10.5, 19.5), (10.5, 14), (9, 14)], closed=True, r=S.r * 0.5)
    return [*[line(poly(c, r=S.r)) for c in corners],
            shell(circle(12, 5.5, 1.75)), shell(figure), line(seg(5.5, 12, 7, 12)), line(seg(17, 12, 18.5, 12))]


_TOOTH = ("M5.5 4C3.8 4 3 5.5 3 7.5C3 10 4 11.5 4.8 13L6 19.5C6.2 20.5 7.5 20.5 7.7 19.5L9 14.5H10L11.3 19.5"
          "C11.5 20.5 12.8 20.5 13 19.5L14.2 13C15 11.5 16 10 16 7.5C16 5.5 15.2 4 13.5 4C12 4 11 4.8 9.5 4.8C8 4.8 7 4 5.5 4Z")
_TOOTH_LINE = ("M5.5 4C3.8 4 3 5.5 3 7.5C3 10 4 11.5 4.8 13L6.2 20.5H7.5L9 14.5H10L11.5 20.5H12.8L14.2 13C15 11.5 16 10 16 7.5"
               "C16 5.5 15.2 4 13.5 4C12 4 11 4.8 9.5 4.8C8 4.8 7 4 5.5 4Z")


def _sparkle(cx, cy, r):
    k = r * 0.18
    return (f"M{fmt(cx)} {fmt(cy - r)}Q{fmt(cx + k)} {fmt(cy - k)} {fmt(cx + r)} {fmt(cy)}"
            f"Q{fmt(cx + k)} {fmt(cy + k)} {fmt(cx)} {fmt(cy + r)}Q{fmt(cx - k)} {fmt(cy + k)} {fmt(cx - r)} {fmt(cy)}"
            f"Q{fmt(cx - k)} {fmt(cy - k)} {fmt(cx)} {fmt(cy - r)}Z")


@icon("dental", CAT, "Clean tooth with a sparkle",
      tags=["dentist", "tooth", "teeth", "dental care", "oral health", "hygiene"], aliases=["dentistry"])
def _(S):
    tooth = move(L(S, _TOOTH_LINE, _TOOTH), 0, 0, 0.92, 3, 21)
    return [shell(tooth), solid(_sparkle(19, 5, 3))]


@icon("eye-chart", CAT, "Eye test chart with a large letter E",
      tags=["snellen", "eye test", "vision", "optometry", "eyesight", "optician"], aliases=["snellen-chart"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 18.5, min(S.R, 2.5))),
        detail(poly([(14.5, 6), (9.5, 6), (9.5, 13), (14.5, 13)], r=S.r * 0.3)),
        detail(seg(9.5, 9.5, 14, 9.5)),
        detail(seg(7.5, 17, 9.5, 17)), detail(seg(11, 17, 13, 17)), detail(seg(14.5, 17, 16.5, 17)),
    ]


@icon("glasses", CAT, "Pair of eyeglasses with full-rim lenses",
      tags=["eyeglasses", "spectacles", "vision", "optician", "eyewear", "sight"], aliases=["eyeglasses"])
def _(S):
    rr = L(S, 2, 3.5)
    return [
        line(rect(3, 9, 7.5, 7, rr)), line(rect(13.5, 9, 7.5, 7, rr)),
        line("M10.5 11.25C11.3 10.4 12.7 10.4 13.5 11.25"),
        line(poly([(3, 10), (3, 7.5), (4.5, 6.5)] if S.name == "line" else [(3, 10), (3, 8.5), (4.5, 6.5)], r=S.r)),
        line(poly([(21, 10), (21, 7.5), (19.5, 6.5)] if S.name == "line" else [(21, 10), (21, 8.5), (19.5, 6.5)], r=S.r)),
    ]


@icon("hearing-aid", CAT, "Behind-the-ear hearing aid with its tube and ear tip",
      tags=["hearing", "deaf", "audiology", "ear", "hard of hearing", "assistive"])
def _(S):
    body = L(S, "M14.5 3C18 3 20.5 5.8 20.5 9.5C20.5 13.8 18.4 17.5 15.2 19.8L13 18C15 15.8 16 13.5 16 11C16 9 15 7.8 13.5 7.5L12.5 3.4C13.1 3.1 13.8 3 14.5 3Z",
             "M14.5 3C18 3 20.5 5.8 20.5 9.5C20.5 13.8 18.4 17.5 15.2 19.8C14.4 20.4 13.3 19.5 13.8 18.6C15.2 16.2 16 13.7 16 11C16 9.3 15.2 8 13.6 7.6C12.4 7.3 11.9 6.2 12.2 5C12.5 3.8 13.4 3 14.5 3Z")
    return [
        shell(body),
        line("M12.2 5.2C8.2 5.2 6 7.5 6 11"),
        shell(L(S, "M3.5 12H8.5V14.5A2.5 2.5 0 0 1 3.5 14.5Z",
                "M4.5 12H7.5A1 1 0 0 1 8.5 13V14.5A2.5 2.5 0 0 1 3.5 14.5V13A1 1 0 0 1 4.5 12Z")),
    ]


@icon("prescription", CAT, "Prescription sheet marked with the Rx symbol",
      tags=["rx", "medicine", "pharmacy", "doctor", "script", "medication"], aliases=["rx"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, min(S.R, 2.5))),
        detail(L(S, "M8.5 17.5V6.5H11.5A2.75 2.75 0 0 1 11.5 12H8.5", "M8.5 17.5V6.5H11.5A2.75 2.75 0 0 1 11.5 12H8.5")),
        detail(seg(10.5, 12, 16, 18)), detail(seg(16, 13, 11.5, 18)),
    ]


_BOARD = (4.5, 4, 15, 17.5)
_CLIP = (8.5, 2.5, 7, 4)


def _clipboard_filled(*details):
    def f():
        x, y, w, h = _BOARD
        cx, cy, cw, ch = _CLIP
        board = outline_region(rect(x, y, w, h, 2))
        clip = outline_region(rect(cx, cy, cw, ch, 1.5))
        body = U(D(board, P(rect(cx - 2.5, cy - 2.5, cw + 5, ch + 5, 2.5))), clip)
        return D(body, *[ST(dd, 2.0) for dd in details])
    return f


@icon("medical-clipboard", CAT, "Clipboard with a medical plus sign",
      tags=["medical record", "chart", "patient", "health report", "checkup", "form"], aliases=["medical-record"],
      filled=_clipboard_filled(plus(12, 13.5, 3)))
def _(S):
    x, y, w, h = _BOARD
    cx, _, cw, _ = _CLIP
    return [shell(poly([(cx, y), (x, y), (x, y + h), (x + w, y + h), (x + w, y), (cx + cw, y)], r=S.R)),
            shell(rect(*_CLIP, min(S.R, 1.5))), detail(plus(12, 13.5, 3))]


@icon("dropper", CAT, "Medicine dropper with a rubber bulb releasing a drop",
      tags=["eye drops", "pipette", "dose", "liquid", "medicine", "drop"], aliases=["medicine-dropper"])
def _(S):
    m = axis((13.5, 10.5), 135)
    return [
        shell(stadium(m, -9.5, -4, 3, L(S, 2.25, 3))),
        line(mseg(m, -3.5, -4, -3.5, 4)),
        shell(poly([m(-3.5, -1.75), m(3.5, -1.75), m(6.5, 0), m(3.5, 1.75), m(-3.5, 1.75)], closed=True, r=S.r * 0.4)),
        solid("M4.5 16.5Q6.3 18.8 6.3 19.7A1.8 1.8 0 0 1 2.7 19.7Q2.7 18.8 4.5 16.5Z"),
    ]


@icon("iv-bag", CAT, "Intravenous drip bag with measuring marks and a tube",
      tags=["iv", "drip", "saline", "infusion", "intravenous", "hospital"], aliases=["iv-drip", "drip"])
def _(S):
    bag = [(5.5, 3), (18.5, 3), (18.5, 12), (14.5, 16), (9.5, 16), (5.5, 12)]
    return [
        shell(poly(bag, closed=True, r=S.r)),
        detail(seg(10.5, 6, 13.5, 6)),
        detail(seg(5.5, 9, 8.5, 9)), detail(seg(5.5, 12, 8.5, 12)),
        line(poly([(12, 16), (12, 20.5), (4, 20.5)], r=L(S, 0, 2.5))),
    ]


@icon("hospital-bed", CAT, "Hospital bed with a raised backrest and wheels",
      tags=["patient", "ward", "inpatient", "bed", "admission", "care"], aliases=["patient-bed"])
def _(S):
    return [
        line(poly([(3, 4), (3, 17), (21, 17), (21, 11)], r=S.r)),
        line(poly([(5.5, 8), (9.5, 13), (19, 13)], r=S.r)),
        dot(6, 20, 1.5), dot(18, 20, 1.5),
    ]


@icon("scalpel", CAT, "Surgical scalpel with a curved blade",
      tags=["surgery", "knife", "surgeon", "operation", "cut", "blade"], aliases=["surgical-knife"])
def _(S):
    m = axis((12, 12), -45)
    handle = stadium(m, -9.5, 1, 1.75, L(S, 0.75, 1.75))
    blade = frame(L(S, "M0 -1.75H9.5C8 1.5 5 3 0 3Z", "M0 -1.75H8.5Q9.5 -1.75 9 -0.9C7.5 1.5 4.5 3 1 3H0Z"), (12, 12), -45)
    return [shell(union(handle, blade))]


@icon("band-aid", CAT, "Adhesive bandage strip with a central pad",
      tags=["plaster", "adhesive bandage", "wound", "cut", "first aid", "sticking plaster"], aliases=["plaster", "adhesive-bandage"])
def _(S):
    m = axis((12, 12), -45)
    return [
        shell(stadium(m, -9.5, 9.5, 3.75, L(S, 2.5, 3.75))),
        detail(mseg(m, -3.5, -3.75, -3.5, 3.75)), detail(mseg(m, 3.5, -3.75, 3.5, 3.75)),
        dot(*m(-1, -1), 0.9), dot(*m(1, 1), 0.9),
    ]


@icon("dna-helix", CAT, "DNA double helix with base-pair rungs",
      tags=["dna", "genetics", "gene", "genome", "biology", "chromosome"], aliases=["double-helix"])
def _(S):
    return [
        line("M7 3C7 7.5 17 7.5 17 12C17 16.5 7 16.5 7 21"),
        line("M17 3C17 7.5 7 7.5 7 12C7 16.5 17 16.5 17 21"),
        line(seg(7.6, 4.75, 16.4, 4.75)), line(seg(7.6, 10.25, 16.4, 10.25)),
        line(seg(7.6, 13.75, 16.4, 13.75)), line(seg(7.6, 19.25, 16.4, 19.25)),
    ]


# ============================================================================ medicines and equipment

@icon("inhaler", CAT, "Asthma inhaler: a canister in an L-shaped body with a mouthpiece",
      tags=["asthma", "puffer", "respiratory", "breathing", "copd", "medicine"], aliases=["puffer"])
def _(S):
    return [
        shell(rect(11, 2.5, 5.5, 6, min(S.R, 1.5))),
        shell(poly([(9.5, 8.5), (18, 8.5), (18, 17), (14.5, 20.5), (4, 20.5), (4, 15.5), (9.5, 15.5)], closed=True, r=S.r)),
        detail(seg(11, 8.5, 16.5, 8.5)),
    ]


@icon("pill-bottle", CAT, "Prescription pill bottle with a cap and label",
      tags=["medicine bottle", "pills", "pharmacy", "prescription", "medication", "vitamins"], aliases=["medicine-bottle"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 4.5, min(S.R, 1.5))),
        shell(rect(6, 9, 12, 12, S.R)),
        detail(seg(6, 12.5, 18, 12.5)), detail(seg(6, 17.5, 18, 17.5)),
    ]


@icon("ointment", CAT, "Tube of ointment with a crimped end and cap",
      tags=["cream", "gel", "tube", "topical", "lotion", "skin care"], aliases=["cream-tube"])
def _(S):
    m = axis((12.5, 11.5), -45)
    body = [m(-5, -1.75), m(-3, -3.75), m(8, -4.5), m(8, 4.5), m(-3, 3.75), m(-5, 1.75)]
    cap = [m(-9.5, -2), m(-5, -2), m(-5, 2), m(-9.5, 2)]
    return [
        shell(poly(body, closed=True, r=S.r * 0.5)),
        detail(mseg(m, 5.75, -4.4, 5.75, 4.4)),
        shell(poly(cap, closed=True, r=S.r * 0.5)),
    ]


@icon("splint", CAT, "Limb held by a splint board with two straps",
      tags=["fracture", "immobilize", "brace", "injury", "first aid", "support"], aliases=["brace-splint"])
def _(S):
    m = axis((12, 12), -45)
    limb = stadium(m, -9.5, 9.5, 2.75, L(S, 2, 2.75))
    board = poly([m(-6, -4.5), m(6, -4.5), m(6, 4.5), m(-6, 4.5)], closed=True, r=S.r * 0.5)
    return [shell(union(limb, board)), detail(mseg(m, -3, -4.5, -3, 4.5)), detail(mseg(m, 3, -4.5, 3, 4.5))]


@icon("cast-arm", CAT, "Bent arm in a plaster cast with the hand showing",
      tags=["broken arm", "fracture", "plaster cast", "injury", "orthopedic", "bone"], aliases=["arm-cast"])
def _(S):
    rr = L(S, 0.5, 2)
    arm = union(rect(3, 3, 5, 15.5, rr), rect(3, 13.5, 18, 5, L(S, 1, 2.5)), rect(9.5, 12, 8, 8, L(S, 0.5, 1.5)))
    return [shell(arm), detail(seg(12.25, 12, 12.25, 20)), detail(seg(14.75, 12, 14.75, 20))]


def _mini_heart(S, cx, cy, s):
    return move(heart(S), cx - 12, cy - 13, s, 12, 13)


def _heart_bolt(S):
    h = _mini_heart(S, 12, 14, 0.66)
    bolt = "M13 10.5L10.75 14.25H13.25L11 18"
    return path_to_d(D(P(h), ST(bolt, 1.5, "butt", "miter")))


@icon("defibrillator", CAT, "Defibrillator case with a heart and lightning bolt",
      tags=["aed", "cardiac arrest", "shock", "heart", "resuscitation", "emergency"], aliases=["aed"])
def _(S):
    return [
        shell(rect(2.5, 6, 19, 15, S.R)),
        line(poly([(8.5, 6), (8.5, 3), (15.5, 3), (15.5, 6)], r=S.r * 0.66)),
        Part("dot", _heart_bolt(S)),
    ]


@icon("oxygen-tank", CAT, "Oxygen cylinder with a valve and pressure gauge",
      tags=["oxygen", "o2", "cylinder", "respiratory", "gas", "breathing"], aliases=["oxygen-cylinder"])
def _(S):
    return [
        shell(rect(6, 8, 9, 13, L(S, 2, 4.5))),
        shell(rect(9, 5, 3, 3, min(S.R, 0.75))),
        line(seg(7, 3, 14, 3)),
        line(seg(12, 6.5, 15.75, 6.5)),
        shell(circle(18, 6.5, 2.25)),
        detail(seg(6, 12, 15, 12)),
    ]


_DROP = "M12 7.5C13.8 9.8 15 11.5 15 12.9A3 3 0 0 1 9 12.9C9 11.5 10.2 9.8 12 7.5Z"
_DROP_R = "M11.4 8.3Q12 7.5 12.6 8.3C14.1 10.2 15 11.6 15 12.9A3 3 0 0 1 9 12.9C9 11.6 9.9 10.2 11.4 8.3Z"


def _bag(S):
    return [shell(poly([(5.5, 3), (18.5, 3), (18.5, 12), (14.5, 16), (9.5, 16), (5.5, 12)], closed=True, r=S.r)),
            line(poly([(12, 16), (12, 20.5), (4, 20.5)], r=L(S, 0, 2.5)))]


@icon("blood-bag", CAT, "Blood bag marked with a drop, with its tube",
      tags=["blood donation", "donor", "blood bank", "plasma", "blood", "hospital"], aliases=["blood-pack"])
def _(S):
    return [*_bag(S), Part("dot", move(L(S, _DROP, _DROP_R), 0, -3, 1.0))]


@icon("transfusion", CAT, "Blood bag with a tube running to a patient",
      tags=["blood transfusion", "blood", "donation", "infusion", "drip", "hospital"], aliases=["blood-transfusion"])
def _(S):
    bag = [(12.5, 2.5), (21, 2.5), (21, 9), (19, 11.5), (14.5, 11.5), (12.5, 9)]
    return [
        shell(poly(bag, closed=True, r=S.r * 0.66)),
        Part("dot", move(L(S, _DROP, _DROP_R), 4.75, -5.75, 0.62, 12, 12)),
        line(poly([(16.75, 11.5), (16.75, 16), (12, 16)], r=L(S, 0, 2))),
        shell(circle(6.5, 9.5, 2.75)),
        shell(L(S, "M2.5 21V19A4 4 0 0 1 6.5 15A4 4 0 0 1 10.5 19V21Z", "M2.5 20V19A4 4 0 0 1 6.5 15A4 4 0 0 1 10.5 19V20A1 1 0 0 1 9.5 21H3.5A1 1 0 0 1 2.5 20Z")),
    ]


# ============================================================================ conditions

def _virus(cx, cy, r=2.25, spikes=6, spike=2.0, start=-90, knob=1.1):
    parts = [detail(circle(cx, cy, r))]
    for i in range(spikes):
        a = start + i * 360 / spikes
        parts.append(detail(seg(*polar(cx, cy, r, a), *polar(cx, cy, r + spike, a))))
        parts.append(dot(*polar(cx, cy, r + spike + knob * 0.5, a), knob))
    return parts


@icon("allergy", CAT, "Flower releasing pollen; an allergen",
      tags=["pollen", "hay fever", "allergen", "sneezing", "seasonal", "hives"], aliases=["hay-fever", "pollen"])
def _(S):
    cx, cy = 9, 10
    petals = union(*[circle(*polar(cx, cy, 3.25, a), 2.5) for a in range(-90, 270, 72)])
    return [
        shell(petals), detail(circle(cx, cy, 1.25)),
        line(poly([(9, 15.75), (9, 21)], r=0)),
        dot(16.5, 4, 1.25), dot(19.5, 8, 1.25), dot(16, 11.5, 1.25), dot(20, 13.5, 1.25),
    ]


@icon("fever", CAT, "Face with a thermometer in its mouth",
      tags=["temperature", "sick", "ill", "flu", "hot", "thermometer"], aliases=["high-temperature"])
def _(S):
    m = axis((11, 14.5), 135)
    therm = stadium(m, 0, 9.5, 1.5, 1.5)
    gap = stadium(m, -2, 11.5, 3.5, 3.5)
    face = minus(circle(12.5, 10.5, 8), gap)
    return [shell(face), detail(seg(8.5, 8.5, 11, 8.5)), detail(seg(14, 8.5, 16.5, 8.5)),
            shell(therm), detail(mseg(m, 4.5, 0, 7.5, 0))]


def _sick_face(cx=9.5, cy=12, r=7):
    return [shell(circle(cx, cy, r)), detail(seg(cx - 4, cy - 2, cx - 1.5, cy - 2)), detail(seg(cx + 1, cy - 2, cx + 3.5, cy - 2))]


@icon("cough", CAT, "Face coughing, with puff lines from the mouth",
      tags=["cold", "flu", "sick", "respiratory", "illness", "symptom"])
def _(S):
    return [*_sick_face(), detail(circle(11, 15.5, 1)),
            line(seg(18.5, 8, 21, 6.5)), line(seg(18.5, 12, 21.5, 12)), line(seg(18.5, 16, 21, 17.5))]


@icon("sneeze", CAT, "Face sneezing, with a spray of droplets",
      tags=["achoo", "cold", "allergy", "sick", "germs", "flu"], aliases=["achoo"])
def _(S):
    return [*_sick_face(), detail(L(S, "M8 15.5H13", "M8 15.5H13")),
            dot(18.5, 9, 1.1), dot(21, 7, 1.1), dot(19, 12.5, 1.1), dot(21.5, 11, 1.1), dot(21.2, 14.8, 1.1), dot(18.6, 16, 1.1)]


def _shield(S):
    return L(S, "M12 2.5L20 5.5V11C20 16 16.5 19.5 12 21.5C7.5 19.5 4 16 4 11V5.5Z",
             "M11.3 2.8Q12 2.5 12.7 2.8L18.8 5Q20 5.5 20 6.8V11C20 16 16.5 19.5 12 21.5C7.5 19.5 4 16 4 11V6.8Q4 5.5 5.2 5Z")


@icon("virus-shield", CAT, "Shield protecting against a virus",
      tags=["immunity", "protection", "antiviral", "vaccine", "prevention", "defense"], aliases=["immunity"])
def _(S):
    return [shell(_shield(S)), *_virus(12, 11.5)]


@icon("quarantine", CAT, "House with a virus inside; stay home",
      tags=["isolation", "stay home", "lockdown", "self-isolate", "pandemic", "virus"], aliases=["self-isolation"])
def _(S):
    return [shell(poly([(12, 2.5), (21, 10), (21, 21), (3, 21), (3, 10)], closed=True, r=S.r)),
            *_virus(12, 14.25)]


# ============================================================================ wellbeing

_HEAD = "M8 21V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.2 3 19.3 6 19.5 9.8L21 13.3H19.5V16A2 2 0 0 1 17.5 18H15V21"
_HEAD_R = ("M8 21V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.2 3 19.3 6 19.5 9.8L20.6 12.1Q21 13.3 19.9 13.3H19.5V16"
           "A2 2 0 0 1 17.5 18H15V21")


@icon("mental-health", CAT, "Head in profile with a heart inside",
      tags=["wellbeing", "mind", "psychology", "emotional health", "therapy", "self care"], aliases=["wellbeing"])
def _(S):
    return [shell(L(S, _HEAD, _HEAD_R)), Part("dot", _mini_heart(S, 11.5, 11, 0.5))]


@icon("meditation", CAT, "Person sitting cross-legged in meditation",
      tags=["yoga", "mindfulness", "calm", "zen", "relax", "lotus"], aliases=["lotus-pose"])
def _(S):
    return [
        shell(circle(12, 5, 2.25)),
        shell(poly([(9.5, 9.5), (14.5, 9.5), (15.5, 15.5), (8.5, 15.5)], closed=True, r=S.r * 0.66)),
        line(poly([(9.5, 10.5), (5, 16)], r=0)), line(poly([(14.5, 10.5), (19, 16)], r=0)),
        shell(L(S, "M3 18.5C7 16.5 17 16.5 21 18.5C17 20.5 7 20.5 3 18.5Z",
                "M4.5 17.6C8.5 16.3 15.5 16.3 19.5 17.6C21 18.1 21 18.9 19.5 19.4C15.5 20.7 8.5 20.7 4.5 19.4C3 18.9 3 18.1 4.5 17.6Z")),
    ]


@icon("sleep", CAT, "Crescent moon with the letters Z Z",
      tags=["rest", "bedtime", "night", "insomnia", "zzz", "nap"], aliases=["zzz"])
def _(S):
    moon = minus(circle(10, 13.5, 7.5), circle(14.5, 9.5, 6))
    return [
        shell(moon),
        line(poly([(14.5, 3), (20.5, 3), (14.5, 8.5), (20.5, 8.5)], r=S.r * 0.3)),
        line(poly([(17.5, 12), (21, 12), (17.5, 15.5), (21, 15.5)], r=S.r * 0.2)),
    ]


_FLAME = "M12 5.5C14.5 8 16.5 10.5 16.5 13.5A4.5 4.5 0 0 1 7.5 13.5C7.5 11.5 8.5 10 9.5 9C9.8 10.5 10.5 11.3 11.2 11.5C11 9.5 11.2 7.5 12 5.5Z"


@icon("calories", CAT, "Flame inside a progress ring; calories burned",
      tags=["kcal", "burn", "energy", "fitness", "diet", "metabolism"], aliases=["kcal"])
def _(S):
    return [line(arc(12, 12, 9, 135, 405) if S.name == "line" else arc(12, 12, 9, 135, 405)),
            shell(move(_FLAME, 0, 0.5, 1.0) if S.name == "rounded" else
                  move("M12 5.5C14.5 8 16.5 10.5 16.5 13.5A4.5 4.5 0 0 1 7.5 13.5C7.5 11.5 8.5 10 9.5 8.5L11.2 11.5C11 9.5 11.2 7.5 12 5.5Z", 0, 0.5, 1.0))]


@icon("weight-scale", CAT, "Bathroom scale with a dial",
      tags=["weight", "scale", "bathroom scale", "weigh", "bmi", "diet"], aliases=["bathroom-scale"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail("M7.5 11A4.5 4.5 0 0 1 16.5 11Z"), detail(seg(12, 11, 14, 8))]


@icon("nutrition", CAT, "Plate divided into food portions beside a fork",
      tags=["diet", "healthy eating", "balanced diet", "food", "meal plan", "nutritionist"], aliases=["healthy-eating"])
def _(S):
    cx, cy, r = 15, 12, 6
    return [
        shell(circle(cx, cy, r)),
        detail(seg(cx, cy - r, cx, cy + r)), detail(seg(cx, cy, cx + r, cy)),
        line(L(S, "M3 3V8H6V3", "M3 3V6.5A1.5 1.5 0 0 0 6 6.5V3")),
        line(seg(4.5, 8, 4.5, 21)),
    ]
