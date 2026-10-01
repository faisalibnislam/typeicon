"""TypeIcon Core: hospital and lab supplies (batch medical_003).

Patient transport, hospital furniture and fixtures, clinical waste, laboratory tools and everyday medicine
containers, drawn from the objects themselves. No red-cross emblem.
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


def drop(cx, cy, r, S=None):
    """Liquid drop: circle of radius r centred at (cx, cy) with its point 2r above the centre."""
    tx, ty = cx, cy - 2 * r
    a = math.radians(30)
    rx_, ry_ = cx + r * math.cos(a), cy - r * math.sin(a)
    lx_, ly_ = cx - r * math.cos(a), ry_
    if S is not None and S.name == "rounded":
        return (f"M{fmt(tx)} {fmt(ty)}Q{fmt(cx + r * 0.55)} {fmt(ty + r * 0.9)} {fmt(rx_)} {fmt(ry_)}"
                f"A{fmt(r)} {fmt(r)} 0 1 1 {fmt(lx_)} {fmt(ly_)}Q{fmt(cx - r * 0.55)} {fmt(ty + r * 0.9)} {fmt(tx)} {fmt(ty)}Z")
    return (f"M{fmt(tx)} {fmt(ty)}L{fmt(rx_)} {fmt(ry_)}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(lx_)} {fmt(ly_)}Z")


def cross(cx, cy, a=2.5):
    """Plus sign as two detail strokes."""
    return [detail(seg(cx - a, cy, cx + a, cy)), detail(seg(cx, cy - a, cx, cy + a))]


# ============================================================================ protective wear

@icon("hospital-gown", CAT, "Patient gown with short sleeves, a V neck and a dot pattern",
      tags=["patient gown", "johnny", "hospital", "ward", "admitted", "scrubs", "inpatient"])
def _(S):
    body = poly([(8, 3), (3, 7), (5, 11), (7, 10), (7, 21), (17, 21), (17, 10), (19, 11), (21, 7), (16, 3)],
                closed=True, r=S.r)
    return [
        shell(body),
        detail(poly([(8, 3), (12, 8), (16, 3)], r=S.r * 0.5)),
        dot(10.5, 14.5, 1), dot(13.5, 14.5, 1), dot(12, 18, 1),
    ]


@icon("medical-gloves", CAT, "Disposable exam glove with a long cuff",
      tags=["exam gloves", "latex", "nitrile", "hygiene", "ppe", "disposable", "hand protection"])
def _(S):
    m = axis((7.5, 15.5), -135)
    tops = [(7, 6.5), (9.5, 4), (12, 3.25), (14.5, 5)]
    body = union(*[rect(x, y, 2.5, 15 - y, 1.25) for x, y in tops], rect(7, 11, 10, 6.5), stadium(m, 0, 6.5, 1.5, 1.5))
    return [
        shell(body),
        shell(rect(6, 17.5, 12, 3.5, L(S, 1, 1.75))),
        detail(seg(9.5, 9, 9.5, 13)),
        detail(seg(12, 9, 12, 13)),
        detail(seg(14.5, 9, 14.5, 13)),
    ]

@icon("glove-box", CAT, "Box of disposable gloves with an oval opening and a glove sticking out",
      tags=["dispenser", "exam gloves", "box", "supplies", "clinic", "ppe", "stock"])
def _(S):
    return [
        line("M7.5 10V5.5A2.25 2.25 0 0 1 12 5.5A2.25 2.25 0 0 1 16.5 5.5V10"),
        shell(rect(3, 10, 18, 11, L(S, 1.5, 3))),
        Part("dot", ellipse(12, 14.5, 5, 1.5)),
    ]

@icon("n95-respirator", CAT, "Cup-shaped respirator mask with a nose clip, a centre crease and ear loops",
      tags=["respirator", "mask", "ffp2", "kn95", "ppe", "filtering facepiece", "dust mask"])
def _(S):
    cup = "M4.5 10.5Q4.5 7 12 7Q19.5 7 19.5 10.5V13.5Q19.5 17.5 12 17.5Q4.5 17.5 4.5 13.5Z"
    cup_r = "M4.5 11Q4.5 7 12 7Q19.5 7 19.5 11V13.5Q19.5 17.5 12 17.5Q4.5 17.5 4.5 13.5Z"
    return [
        shell(L(S, cup, cup_r)),
        detail(seg(8, 12.25, 16, 12.25)),
        line("M4.5 9.75Q1.25 12.25 4.5 14.75"), line("M19.5 9.75Q22.75 12.25 19.5 14.75"),
        solid(rect(9.5, 3.5, 5, 2, L(S, 0.25, 1))),
    ]


@icon("shoe-covers", CAT, "Disposable shoe cover bootie with an elastic opening",
      tags=["booties", "overshoes", "shoe protectors", "clean room", "ppe", "disposable", "hygiene"])
def _(S):
    body = poly([(5, 4), (11.5, 4), (11.5, 10), (15.5, 12), (20, 14), (20, 20), (4, 20)], closed=True, r=S.r * 1.3)
    return [
        shell(body),
        detail(seg(5, 7.5, 11.5, 7.5)),
        detail(seg(15, 15, 15, 20)),
    ]


@icon("surgical-loupes", CAT, "Surgical loupes: glasses with a small telescope tube on each lens",
      tags=["magnifying glasses", "dental loupes", "surgery", "magnifier", "eyewear", "optics", "operating"])
def _(S):
    return [
        shell(circle(6.25, 15.25, 4.25)),
        shell(circle(17.75, 15.25, 4.25)),
        shell(rect(4.25, 3.5, 4, 8, L(S, 0.5, 1.75))),
        shell(rect(15.75, 3.5, 4, 8, L(S, 0.5, 1.75))),
        line("M10.5 15.25H13.5"),
    ]

# ============================================================================ patient transport

@icon("gurney", CAT, "Wheeled gurney with a flat mattress and a raised backrest",
      tags=["trolley", "stretcher", "hospital bed", "ambulance", "emergency", "patient transport", "cot"])
def _(S):
    return [
        shell(rect(9, 8, 12, 3.5, L(S, 1, 1.75))),
        shell(poly([(8, 8), (8, 11.5), (3, 9.5), (3, 4.5)], closed=True, r=S.r * 0.7)),
        line("M11 13V17"), line("M19 13V17"),
        dot(11, 19.5, 1.75), dot(19, 19.5, 1.75),
    ]


@icon("stretcher", CAT, "Carry stretcher: a canvas bed with a patient's head, between two poles with handles",
      tags=["litter", "rescue", "carry", "emergency", "first aid", "casualty", "transport"])
def _(S):
    return [
        shell(rect(5.5, 8, 13, 8, L(S, 0, 2))),
        line("M2 8H5.5"), line("M18.5 8H22"), line("M2 16H5.5"), line("M18.5 16H22"),
        dot(9.5, 12, 2),
    ]

@icon("spine-board", CAT, "Long spinal board with hand holes along both edges",
      tags=["backboard", "rescue", "trauma", "immobilization", "paramedic", "ems", "emergency"])
def _(S):
    out = [shell(rect(2, 6, 20, 12, L(S, 1.5, 4)))]
    for x in (5, 10.5, 16):
        out.append(Part("dot", rect(x, 8.5, 3, 2, 1)))
        out.append(Part("dot", rect(x, 13.5, 3, 2, 1)))
    return out

@icon("stokes-basket", CAT, "Rescue basket stretcher with a tapered wire rim and cross ribs",
      tags=["rescue basket", "litter", "mountain rescue", "lifting", "wire basket", "stretcher", "emergency"])
def _(S):
    return [
        shell(poly([(2.5, 6.5), (21.5, 8), (21.5, 16), (2.5, 17.5)], closed=True, r=S.r * 2)),
        detail(seg(8.5, 7, 8.5, 17)),
        detail(seg(15, 7.6, 15, 16.4)),
        detail(seg(4, 12, 20, 12)),
    ]

@icon("evacuation-chair", CAT, "Stair evacuation chair on tracks with a long tilting handle",
      tags=["stair chair", "fire escape", "mobility", "evacuate", "emergency exit", "disabled", "rescue"])
def _(S):
    return [
        shell(poly([(5, 7), (9, 7), (9, 11), (16, 11), (16, 14), (5, 14)], closed=True, r=S.r * 0.8)),
        line("M9 8L17 2.5"),
        shell(rect(3, 17, 18, 4.5, 2.25)),
        dot(8, 19.25, 0.85), dot(12, 19.25, 0.85), dot(16, 19.25, 0.85),
    ]


# ============================================================================ hospital furniture

@icon("exam-table", CAT, "Exam table with a padded top, a raised head end, a pedestal and a step",
      tags=["examination table", "couch", "treatment table", "clinic", "doctor", "patient", "bed"])
def _(S):
    return [
        shell(rect(9, 6.5, 12, 3.5, L(S, 1, 1.75))),
        shell(poly([(9, 6.5), (9, 10), (3.5, 8.5), (3.5, 4)], closed=True, r=S.r * 0.7)),
        line("M15 10V18"),
        shell(rect(10, 18, 10, 3.5, L(S, 1, 1.75))),
        shell(rect(3, 16.5, 4.5, 5, L(S, 0.5, 1.5))),
    ]

@icon("overbed-table", CAT, "Overbed table: a tabletop on a single post with a wheeled base",
      tags=["bedside table", "tray table", "hospital", "patient", "meal", "furniture", "ward"])
def _(S):
    return [
        shell(rect(3, 4, 18, 3.5, L(S, 1, 1.75))),
        line("M16 7.5V18"),
        line("M5 18H19"),
        dot(6, 20.25, 1.25), dot(18, 20.25, 1.25),
    ]


@icon("privacy-curtain", CAT, "Hospital privacy curtain hanging in folds from a ceiling track",
      tags=["curtain", "divider", "screen", "ward", "bedside", "privacy", "partition"])
def _(S):
    wave = "M4 7H20V19Q18 21.5 16 19Q14 16.5 12 19Q10 21.5 8 19Q6 16.5 4 19Z"
    zig = "M4 7H20V19L18 20.5L16 18.5L14 20.5L12 18.5L10 20.5L8 18.5L6 20.5L4 19Z"
    return [
        line("M2 4H22"),
        shell(L(S, zig, wave)),
        detail(seg(9, 10, 9, 16)),
        detail(seg(15, 10, 15, 16)),
    ]


@icon("nurse-call-button", CAT, "Nurse call handset with a plus on its face and a cord going up",
      tags=["call bell", "help button", "hospital", "nurse", "assistance", "pendant", "alert"])
def _(S):
    return [
        line("M12 9V6Q12 3.5 14.5 3.5H19"),
        shell(rect(6.5, 9, 11, 12, L(S, 2, 4.5))),
        *cross(12, 15, 2.5),
    ]


def biohazard(cx, cy, k=1.0):
    """Trefoil of three solid discs around a hub (small biohazard mark)."""
    out = [dot(cx, cy, 0.9 * k)]
    for a in (-90, 30, 150):
        x, y = polar(cx, cy, 3.0 * k, a)
        out.append(dot(x, y, 1.3 * k))
    return out


# ============================================================================ clinical equipment

@icon("iv-pole", CAT, "IV pole with a hooked top, a hanging fluid bag and a wheeled base",
      tags=["drip stand", "infusion", "intravenous", "drip", "saline", "hospital", "ward"])
def _(S):
    return [
        line("M12 3V19"),
        line("M12 4H17"),
        line("M17 4V6.5"),
        shell(rect(14.5, 6.5, 5, 7.5, L(S, 1.5, 2.5))),
        line("M5.5 19H18.5"),
        dot(5.5, 20.75, 1.25), dot(12, 20.75, 1.25), dot(18.5, 20.75, 1.25),
    ]


@icon("infusion-pump", CAT, "Infusion pump box with a screen and keys, clamped to a pole with a tube through it",
      tags=["iv pump", "drip", "medication", "intravenous", "icu", "fluid", "controller"])
def _(S):
    return [
        shell(rect(3, 5, 12, 13.5, L(S, 2, 3.5))),
        Part("dot", rect(5.5, 7.5, 7, 3.5, 0.5)),
        dot(6.75, 14.5, 1), dot(11.25, 14.5, 1),
        line("M9 5V2.5"), line("M9 18.5V21.5"),
        line("M19.5 2V22"),
        line("M15 11H19.5"),
    ]


@icon("syringe-pump", CAT, "Syringe driver: a flat box holding a syringe with a pusher block behind the plunger",
      tags=["syringe driver", "infusion", "icu", "medication", "pump", "palliative", "dosing"])
def _(S):
    return [
        shell(rect(7, 3.5, 10, 4.5, L(S, 0.5, 1.75))),
        line("M17 5.75H21.5"),
        line("M7 5.75H4"),
        line("M4 3.5V8"),
        shell(rect(3, 11, 18, 9, L(S, 2, 3.5))),
        Part("dot", rect(5.5, 13.5, 6, 3.5, 0.5)),
        dot(16, 15.25, 1.4),
    ]


@icon("dialysis-machine", CAT, "Dialysis machine cart with a screen, a round pump and a filter cylinder",
      tags=["kidney", "renal", "hemodialysis", "blood filter", "nephrology", "treatment", "machine"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 11.5, 16, L(S, 2, 3.5))),
        Part("dot", rect(6, 5, 6.5, 3.5, 0.5)),
        detail(circle(9.25, 13.75, 2.5)),
        shell(rect(17, 6.5, 4, 10, 2)),
        line("M15 9.5H17"),
        dot(6, 20.75, 1.25), dot(13, 20.75, 1.25),
    ]


@icon("baby-incubator", CAT, "Infant incubator: a clear hood with a baby inside, arm ports and a wheeled base",
      tags=["nicu", "newborn", "neonatal", "premature", "infant care", "hospital"])
def _(S):
    body = union(rect(3.5, 3.5, 17, 10, L(S, 2.5, 5)), rect(2.5, 12, 19, 6, L(S, 1, 2)))
    return [
        shell(body),
        dot(8, 8, 1.75),
        line("M11 8H17"),
        dot(9, 15, 1.1), dot(15, 15, 1.1),
        line("M7 18V20"), line("M17 18V20"),
        dot(7, 20.75, 1.25), dot(17, 20.75, 1.25),
    ]

@icon("hospital-bassinet", CAT, "Hospital bassinet: a clear tub cot with a baby, on a small wheeled stand",
      tags=["newborn cot", "crib", "maternity", "baby bed", "nursery", "infant", "ward"])
def _(S):
    tub = ("M3 6H21L18.5 14.5H5.5Z" if S.name == "line" else "M3 6H21L18.75 14Q18.4 16 16.5 16H7.5Q5.6 16 5.25 14Z")
    return [
        shell(tub),
        dot(12, 10.75, 2),
        line("M7.5 16V20"), line("M16.5 16V20"),
        dot(7.5, 20.75, 1.25), dot(16.5, 20.75, 1.25),
    ]


@icon("crash-cart", CAT, "Emergency crash cart with stacked drawers, a defibrillator on top and a push handle",
      tags=["resuscitation", "code blue", "emergency trolley", "cardiac arrest", "drawers", "defibrillator", "er"])
def _(S):
    return [
        shell(rect(5, 3, 8, 4.5, L(S, 0.5, 1.5))),
        shell(rect(3, 10, 14, 10, L(S, 1, 2))),
        detail(seg(3, 13.25, 17, 13.25)),
        detail(seg(3, 16.5, 17, 16.5)),
        line("M17 11H21.5V15"),
        dot(6, 21, 1), dot(14, 21, 1),
    ]


@icon("medical-waste-bin", CAT, "Clinical waste pedal bin with a lid, a biohazard mark and a foot pedal",
      tags=["clinical waste", "biohazard bin", "trash", "disposal", "infectious", "hospital", "garbage"])
def _(S):
    return [
        shell(rect(4, 3.5, 16, 3.5, L(S, 1, 1.75))),
        shell(rect(5, 9, 14, 12, L(S, 1.5, 3))),
        *biohazard(12, 15, 1.0),
        line("M19 20H22"),
    ]


@icon("sharps-container", CAT, "Sharps disposal box with a slotted lid and a syringe dropping in",
      tags=["needle disposal", "syringe bin", "biohazard", "clinical waste", "safety box", "lancet", "sharps bin"])
def _(S):
    m = axis((12, 11.5), -60)
    box = union(rect(3.5, 11, 17, 4, L(S, 1, 1.75)), rect(5, 14, 14, 7, L(S, 1, 1.75)))
    return [
        shell(box),
        detail(seg(5, 15, 19, 15)),
        Part("dot", rect(8.5, 12, 7, 1.25, 0.5)),
        line(mseg(m, 0, 0, 2.5, 0)),
        shell(mpoly(m, [(2.5, -1.75), (8.5, -1.75), (8.5, 1.75), (2.5, 1.75)], closed=True, r=S.r * 0.3)),
        line(mseg(m, 8.5, 0, 10.5, 0)),
        line(mseg(m, 10.5, -2.5, 10.5, 2.5)),
    ]


@icon("biohazard-bag", CAT, "Tied waste bag with a twisted neck and a biohazard mark on its side",
      tags=["clinical waste", "infectious waste", "red bag", "sack", "hazmat", "garbage", "disposal"])
def _(S):
    body = "M9.5 8C6 9.5 3.5 12.5 3.5 16Q3.5 21 12 21Q20.5 21 20.5 16C20.5 12.5 18 9.5 14.5 8Z"
    return [
        shell(body),
        line(L(S, "M10 8L8.5 3.5", "M10 8Q10 5 8.5 3.5")),
        line(L(S, "M14 8L15.5 3.5", "M14 8Q14 5 15.5 3.5")),
        *biohazard(12, 15.25, 1.05),
    ]

@icon("autoclave", CAT, "Autoclave sterilizer box with steam above, a round door and control dots",
      tags=["sterilizer", "sterilisation", "steam", "instruments", "dental", "surgical", "infection control"])
def _(S):
    return [
        line("M9 5.5Q7.5 4 9 2.5"), line("M15 5.5Q13.5 4 15 2.5"),
        shell(rect(3, 7.5, 18, 13.5, L(S, 2, 3.5))),
        detail(circle(9.75, 14.25, 3.75)),
        dot(17, 11, 1.1),
        dot(17, 14.5, 0.9), dot(17, 18, 0.9),
    ]

@icon("hospital-pager", CAT, "Pager: small landscape device with a screen, two buttons and a belt clip",
      tags=["beeper", "page", "alert", "on call", "doctor", "radio", "paging"])
def _(S):
    return [
        shell(rect(5.5, 6, 16, 12, L(S, 1.5, 3.5))),
        line("M5.5 9H2.5V15H5.5"),
        Part("dot", rect(8, 8.5, 7.5, 4.5, 0.5)),
        dot(18.25, 10.5, 1.1), dot(18.25, 14.5, 1.1),
        dot(9.5, 15.5, 0.85), dot(12, 15.5, 0.85),
    ]


@icon("patient-wristband", CAT, "Patient ID wristband: a loop of band with a barcode label across the front",
      tags=["id band", "hospital bracelet", "patient id", "barcode", "admission", "identification", "tag"])
def _(S):
    ring = (minus(rect(2.5, 4.5, 19, 14, 3), rect(6.5, 8.5, 11, 6, 1)) if S.name == "line"
            else minus(ellipse(12, 11.5, 9.5, 7), ellipse(12, 11.5, 6, 3.5)))
    return [
        shell(ring),
        detail(seg(9, 15, 9, 18)), detail(seg(12, 15, 12, 18)), detail(seg(15, 15, 15, 18)),
    ]

@icon("paramedic-bag", CAT, "Paramedic backpack with side pockets, a top handle and a cross on the flap",
      tags=["trauma bag", "ems", "first responder", "ambulance", "medic", "kit", "emergency"])
def _(S):
    body = union(rect(6, 5.5, 12, 15.5, L(S, 1.5, 3.5)), rect(3, 12, 4, 7, L(S, 0.5, 1.5)), rect(17, 12, 4, 7, L(S, 0.5, 1.5)))
    return [
        line("M9.5 5.5V3H14.5V5.5"),
        shell(body),
        detail(seg(7, 9.25, 17, 9.25)),
        *cross(12, 14.75, 2.25),
    ]


@icon("hyperbaric-chamber", CAT, "Horizontal hyperbaric chamber capsule on legs with a door seam and a patient lying inside",
      tags=["oxygen therapy", "diving", "decompression", "pressure chamber", "hbot", "wound healing", "chamber"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 19, 12, L(S, 4, 6))),
        dot(6.5, 11.5, 1.75),
        line("M9.5 11.5H13"),
        detail(seg(17, 5.5, 17, 17.5)),
        line("M6 17.5V20"), line("M18 17.5V20"),
    ]

HEART = "M12 20L4.4 12.6A4.6 4.6 0 0 1 11 6.3L12 7.3L13 6.3A4.6 4.6 0 0 1 19.6 12.6Z"
HEART_R = ("M10.6 18.6L4.4 12.6A4.6 4.6 0 0 1 11 6.3L11.3 6.6Q12 7.3 12.7 6.6L13 6.3A4.6 4.6 0 0 1 19.6 12.6"
           "L13.4 18.6Q12 20 10.6 18.6Z")


def small_heart(S, cx, cy, k):
    """Heart scaled by k with the centre of its box at (cx, cy)."""
    return xf(L(S, HEART, HEART_R), (k, 0, 0, k, cx - 12 * k, cy - 13 * k))


# ============================================================================ rescue and emergency

@icon("iron-lung", CAT, "Iron lung: a large horizontal cylinder on legs with a patient's head out of one end",
      tags=["negative pressure ventilator", "polio", "respirator", "ventilation", "historic", "breathing", "tank"])
def _(S):
    return [
        shell(union(rect(8.5, 5.5, 13, 12, L(S, 3.5, 5.5)), circle(5, 11.5, 3))),
        detail(seg(13, 5.5, 13, 17.5)),
        detail(seg(18, 5.5, 18, 17.5)),
        line("M12 17.5V20.5"), line("M19 17.5V20.5"),
    ]

@icon("medical-drone", CAT, "Delivery drone with two visible rotors carrying a box with a cross",
      tags=["uav", "quadcopter", "aerial delivery", "supplies", "blood delivery", "emergency", "flying"])
def _(S):
    return [
        shell(rect(7, 6.5, 10, 4.5, L(S, 1, 2))),
        line("M7 8.75H4.5V5"), line("M2 4.5H7.5"),
        line("M17 8.75H19.5V5"), line("M16.5 4.5H22"),
        line("M9.5 11V14"), line("M14.5 11V14"),
        shell(rect(7, 14, 10, 7, L(S, 1, 2))),
        *cross(12, 17.5, 2),
    ]


@icon("medical-tent", CAT, "Field hospital tent with a gabled roof, a cross on the front and a door flap",
      tags=["field hospital", "relief", "disaster response", "camp", "triage", "emergency shelter", "clinic"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 10), (12, 3.5), (21, 10), (21, 21)], closed=True, r=S.r * 1.3)),
        *cross(12, 11, 2),
        detail(poly([(9, 21), (9, 16.5), (15, 16.5), (15, 21)])),
    ]


@icon("organ-transport-box", CAT, "Organ transport cooler with a carry handle and a heart on its side",
      tags=["transplant", "donor organ", "cool box", "cooler", "organ donation", "surgery", "logistics"])
def _(S):
    return [
        line("M8.5 9V5H15.5V9"),
        shell(rect(3, 9, 18, 12, L(S, 1.5, 3))),
        Part("dot", small_heart(S, 12, 15.5, 0.55)),
    ]


@icon("medical-alert-bracelet", CAT, "Medical alert bracelet: an oval tag with a staff mark between chain links",
      tags=["medical id", "alert band", "allergy", "diabetes", "emergency info", "tag", "jewelry"])
def _(S):
    return [
        shell(ellipse(12, 12, 5.25, 6.5)),
        detail(seg(12, 8.5, 12, 15.5)),
        shell(rect(2, 10.25, 5, 3.5, L(S, 0.5, 1.75))),
        shell(rect(17, 10.25, 5, 3.5, L(S, 0.5, 1.75))),
    ]


@icon("fall-alert-pendant", CAT, "Personal alarm pendant: a round button on a neck cord with signal arcs",
      tags=["sos", "panic button", "elderly", "alarm", "emergency call", "seniors", "help"])
def _(S):
    return [
        line("M6 2.5L12 11"), line("M18 2.5L12 11"),
        shell(circle(12, 16, 4.5)),
        dot(12, 16, 1.6),
        line(arc(12, 16, 8, -40, 40)),
        line(arc(12, 16, 8, 140, 220)),
    ]


@icon("triage-tag", CAT, "Triage tag with clipped corners, a string hole and tear-off strips along the bottom",
      tags=["casualty", "emergency", "mass casualty", "priority", "paramedic", "label", "disaster"])
def _(S):
    return [
        shell(poly([(9, 4.5), (15, 4.5), (18, 7.5), (18, 21.5), (6, 21.5), (6, 7.5)], closed=True, r=S.r)),
        dot(12, 8.25, 1.25),
        line("M12.5 7.5L19.5 2.5"),
        detail(seg(6, 13.5, 18, 13.5)),
        detail(seg(6, 17.5, 18, 17.5)),
    ]

@icon("emergency-blanket", CAT, "Crinkled foil emergency blanket with a shine line and a sparkle",
      tags=["foil blanket", "thermal blanket", "warmth", "survival", "hypothermia"])
def _(S):
    star = poly([(15.5, 8), (16.6, 10.4), (19, 11.5), (16.6, 12.6), (15.5, 15), (14.4, 12.6), (12, 11.5), (14.4, 10.4)], closed=True)
    return [
        shell(poly([(3, 7), (6, 4.5), (9, 6), (13, 4), (17, 6), (21, 5), (19, 12), (21, 18), (17, 19.5), (13, 18),
                    (9, 20), (5, 18.5), (4, 13)], closed=True, r=S.r * 0.6)),
        detail(seg(7, 15, 9.5, 10.5)),
        Part("dot", star),
    ]

@icon("trauma-shears", CAT, "Trauma shears: blades bent at the pivot with blunt tips and two big handle rings",
      tags=["bandage scissors", "ems", "paramedic", "clothing cutter", "emergency", "first aid", "cutting"])
def _(S):
    return [
        line("M7.5 8.5L12 12L21 15"),
        line("M7.5 15.5L12 12L21 9"),
        shell(circle(5, 6.25, 3)),
        shell(circle(5, 17.75, 3)),
    ]


# ============================================================================ hot and cold therapy

@icon("ice-pack", CAT, "Gel ice pack with a sealed top edge and a snowflake",
      tags=["cold pack", "cold compress", "injury", "swelling", "cryotherapy", "sprain", "first aid"])
def _(S):
    out = [shell(rect(3.5, 3.5, 17, 17, L(S, 2.5, 5.5))), detail(seg(3.5, 7.5, 20.5, 7.5))]
    for a in (90, 30, 150):
        x1, y1 = polar(12, 14, 3.5, a)
        x2, y2 = polar(12, 14, 3.5, a + 180)
        out.append(detail(seg(x1, y1, x2, y2)))
    return out


@icon("heating-pad", CAT, "Quilted heating pad with heat waves above and a cord to a small hand controller",
      tags=["heat pad", "warmer", "electric", "muscle pain", "back pain", "hot compress", "therapy"])
def _(S):
    return [
        line("M6 8Q4.5 6.5 6 5Q7.5 3.5 6 2.5"),
        line("M9.5 8Q8 6.5 9.5 5Q11 3.5 9.5 2.5"),
        line("M13 8Q11.5 6.5 13 5Q14.5 3.5 13 2.5"),
        shell(rect(2, 10, 13.5, 10.5, L(S, 2, 3.5))),
        detail(seg(2, 15.25, 15.5, 15.25)),
        line("M15.5 13H19.5V14.5"),
        shell(rect(17.5, 14.5, 4, 7, L(S, 1, 2))),
    ]

@icon("cpr-manikin", CAT, "CPR training manikin lying down with a tilted head and two hands pressing the chest",
      tags=["resuscitation", "first aid training", "dummy", "chest compressions", "lifesaving", "aed", "course"])
def _(S):
    return [
        shell(rect(9.5, 14, 12, 6, L(S, 1.5, 3))),
        shell(circle(5.25, 17, 3)),
        shell(rect(12, 8.5, 6, 3, L(S, 0.5, 1.5))),
        line("M15 2.5V6"),
        line("M13 4.25L15 6.25L17 4.25"),
    ]

# ============================================================================ laboratory

@icon("ivf", CAT, "IVF: a fine needle pipette touching a round egg cell held by a blunt pipette",
      tags=["in vitro fertilization", "fertility", "embryo", "icsi", "egg cell", "reproductive", "laboratory"])
def _(S):
    return [
        shell(circle(13.5, 13, 4.5)),
        dot(13.5, 13, 1.4),
        shell(poly([(2, 9), (7, 11), (7, 15), (2, 17)], closed=True, r=S.r * 0.6)),
        line("M16.7 9.8L21.5 5"),
    ]


@icon("petri-dish", CAT, "Shallow round petri dish seen at an angle with a few colony dots inside",
      tags=["culture dish", "bacteria", "agar", "microbiology", "laboratory", "colonies", "sample"])
def _(S):
    ry = L(S, 4, 5)
    body = union(ellipse(12, 10.5, 9, ry), f"M3 10.5V{fmt(15 + ry - 4)}A9 {fmt(ry)} 0 0 0 21 {fmt(15 + ry - 4)}V10.5Z")
    return [
        shell(body),
        dot(9.5, 10.25, 1), dot(14, 11, 1), dot(12.5, 8.75, 0.8),
    ]


@icon("micropipette", CAT, "Micropipette with a plunger button, a grip body and a disposable tip",
      tags=["pipettor", "lab", "liquid handling", "dispensing", "biology", "pcr", "microliter"])
def _(S):
    return [
        shell(rect(9.5, 2.5, 5, 3, L(S, 0.5, 1.5))),
        shell(poly([(9, 6), (15, 6), (15.5, 14), (13.5, 17), (10.5, 17), (8.5, 14)], closed=True, r=S.r)),
        detail(seg(9, 13, 15, 13)),
        Part("dot", rect(10.5, 8, 3, 3, L(S, 0, 0.75))),
        shell(poly([(10.75, 17.5), (13.25, 17.5), (12.6, 21.5), (11.4, 21.5)], closed=True)),
    ]


@icon("centrifuge", CAT, "Benchtop centrifuge seen from above with sample tubes spaced around the rotor",
      tags=["spin", "rotor", "laboratory", "separation", "sample prep", "blood test", "lab equipment"])
def _(S):
    out = [shell(rect(2.5, 2.5, 19, 19, L(S, 2.5, 5.5))), detail(circle(12, 12, 7.5))]
    for i in range(6):
        x, y = polar(12, 12, 3.9, -90 + 60 * i)
        out.append(dot(x, y, 1.1))
    return out


@icon("test-tube-rack", CAT, "Rack holding three upright test tubes with liquid levels",
      tags=["tubes", "laboratory", "chemistry", "samples", "holder", "science", "experiment"])
def _(S):
    body = union(rect(3, 3, 4, 8.5, L(S, 0.5, 1.75)), rect(10, 3, 4, 8.5, L(S, 0.5, 1.75)),
                 rect(17, 3, 4, 8.5, L(S, 0.5, 1.75)), rect(2, 10.5, 20, 4, L(S, 0.5, 1.75)))
    return [
        shell(body),
        detail(seg(3, 6.25, 7, 6.25)), detail(seg(10, 6.25, 14, 6.25)), detail(seg(17, 6.25, 21, 6.25)),
        line("M4.5 14.5V20.5"), line("M19.5 14.5V20.5"),
    ]

@icon("microplate", CAT, "Well plate tray with a grid of round wells and one clipped corner",
      tags=["96 well plate", "assay", "elisa", "laboratory", "screening", "sample tray", "biochemistry"])
def _(S):
    out = [shell(poly([(6, 4.5), (21.5, 4.5), (21.5, 19.5), (2.5, 19.5), (2.5, 8)], closed=True, r=S.r * 1.6))]
    for yy in (9, 12, 15.25):
        for xx in (7, 10.4, 13.8, 17.2):
            out.append(dot(xx, yy, 1.1))
    return out


@icon("microscope-slide", CAT, "Microscope slide: a long glass strip with a frosted label end and a small cover slip",
      tags=["glass slide", "specimen", "cover slip", "histology", "pathology", "microscopy", "lab"])
def _(S):
    return [
        shell(rect(2.5, 7.5, 19, 9, L(S, 1, 2.5))),
        detail(seg(7.5, 7.5, 7.5, 16.5)),
        detail(rect(10.5, 9.75, 6, 4.5)),
    ]


@icon("specimen-cup", CAT, "Specimen cup with a ridged screw lid and a label panel",
      tags=["urine sample", "sample container", "stool sample", "lab test", "collection cup", "screw cap", "diagnostic"])
def _(S):
    return [
        shell(rect(5, 3, 14, 5, L(S, 1, 2))),
        shell(poly([(6, 10.5), (18, 10.5), (17, 21), (7, 21)], closed=True, r=S.r)),
        Part("dot", rect(9, 13.5, 6, 4.5, L(S, 0, 0.75))),
    ]


@icon("blood-collection-tube", CAT, "Blood collection tube with a wide rubber stopper and blood filling the lower half",
      tags=["blood draw", "phlebotomy", "sample", "lab test", "venipuncture", "vial"])
def _(S):
    tube = "M9.25 6.5H14.75V18.75A2.75 2.75 0 0 1 9.25 18.75Z"
    return [
        shell(rect(7.5, 2.5, 9, 4, L(S, 0.5, 1.5))),
        shell(tube),
        Part("dot", "M10.5 13H13.5V18.5A1.5 1.5 0 0 1 10.5 18.5Z"),
    ]


@icon("swab-test", CAT, "Long swab stick with a cotton tip next to an open sample tube",
      tags=["nasal swab", "throat swab", "covid test", "pcr sample", "collection", "diagnostic", "specimen"])
def _(S):
    m = axis((11.5, 7.5), -55)
    return [
        line(mseg(m, 0, 0, -13.5, 0)),
        shell(stadium(m, 0, 4.5, 1.7, 1.7)),
        shell(f"M16.5 10H21.5V18.75A2.5 2.5 0 0 1 16.5 18.75Z"),
    ]


@icon("rapid-test", CAT, "Rapid test cassette with a round sample well and two result lines",
      tags=["antigen test", "lateral flow", "home test", "covid", "diagnostic", "result", "self test"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 19, 11, L(S, 1.5, 4))),
        detail(circle(7.5, 12, 2)),
        detail(seg(11.5, 9.25, 11.5, 14.75)),
        Part("dot", rect(14, 9.5, 1.6, 5)),
        Part("dot", rect(17.6, 9.5, 1.6, 5)),
    ]


@icon("pregnancy-test", CAT, "Pregnancy test stick with a cap end and two result lines, set on a diagonal",
      tags=["home test", "hpht", "urine test", "fertility", "maternity", "result stick", "expecting"])
def _(S):
    return [
        shell(rot(rect(2, 9, 20, 6, L(S, 1, 2.75)), -40)),
        detail(rot(seg(8, 9, 8, 15), -40)),
        Part("dot", rot(rect(12, 10.75, 1.5, 2.5), -40)),
        Part("dot", rot(rect(15.5, 10.75, 1.5, 2.5), -40)),
    ]


@icon("inoculation-loop", CAT, "Inoculation loop: a thin wire ending in a small open ring on a grip handle",
      tags=["wire loop", "streak plate", "microbiology", "culture", "bacteria", "laboratory", "sterile"])
def _(S):
    m = axis((3, 3), 45)
    return [
        line(circle(*m(3, 0), 3)),
        line(mseg(m, 6, 0, 13, 0)),
        shell(L(S, mpoly(m, [(13, -1.6), (23.5, -1.6), (23.5, 1.6), (13, 1.6)], closed=True), stadium(m, 13, 23.5, 1.6, 1.6))),
    ]


@icon("liquid-nitrogen-dewar", CAT, "Cryogenic dewar: a squat round tank with a narrow neck and cold vapor rising",
      tags=["cryogenic", "cryo storage", "cold", "sperm bank", "freezer", "laboratory", "vapor"])
def _(S):
    return [
        line("M10 5.5Q8.5 4 10 2.5"), line("M14 5.5Q12.5 4 14 2.5"),
        shell(union(rect(4, 12, 16, 9.5, L(S, 4, 4.75)), rect(9.25, 7.5, 5.5, 5, L(S, 0.5, 1.5)))),
        detail(seg(4, 15.5, 20, 15.5)),
    ]


@icon("biosafety-cabinet", CAT, "Biosafety cabinet front with a sloped glass sash above an open work slot",
      tags=["fume hood", "laminar flow", "lab hood", "containment", "sterile workstation", "safety cabinet", "bsl"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, L(S, 2, 3.5))),
        detail(poly([(7, 5.5), (17, 5.5), (19, 13), (5, 13)], closed=True)),
        Part("dot", rect(6.5, 16.5, 11, 2.25, L(S, 0, 1))),
    ]


@icon("pcr-machine", CAT, "PCR thermal cycler with its lid propped open above a block of sample tube wells",
      tags=["thermocycler", "dna amplification", "molecular biology", "genetics", "lab instrument", "diagnostics", "polymerase"])
def _(S):
    out = [
        shell(poly([(5, 8), (19, 8), (17.5, 3.5), (6.5, 3.5)], closed=True, r=S.r * 0.6)),
        shell(rect(2.5, 10.5, 19, 10, L(S, 1.5, 3))),
        Part("dot", rect(5, 16, 5.5, 2.5, L(S, 0, 0.75))),
        dot(16.5, 17.25, 1.3),
    ]
    for xx in (6, 9, 12, 15, 18):
        out.append(dot(xx, 13.25, 1))
    return out


@icon("gel-electrophoresis", CAT, "Electrophoresis gel slab with three lanes of separated bands",
      tags=["dna gel", "agarose", "protein gel", "bands", "molecular biology", "genetics", "lab"])
def _(S):
    out = [shell(rect(2.5, 2.5, 19, 19, L(S, 2, 3.5)))]
    for x, ys in ((5, (9, 15)), (10.25, (7, 12, 17)), (15.5, (11,))):
        for y in ys:
            out.append(Part("dot", rect(x, y, 3.5, 2, L(S, 0, 0.75))))
    return out


@icon("vortex-mixer", CAT, "Vortex mixer with a round base, a tube held in a cup and motion arcs on each side",
      tags=["shaker", "lab mixer", "agitator", "sample mixing", "test tube", "laboratory", "swirl"])
def _(S):
    tube = "M10 2.5H14V11A2 2 0 0 1 10 11Z"
    cup = poly([(6, 10.5), (18, 10.5), (16, 15), (8, 15)], closed=True, r=S.r * 0.4)
    return [
        shell(union(tube, cup)),
        shell(rect(3.5, 17.5, 17, 4, L(S, 1.5, 2))),
        detail(seg(10, 6.5, 14, 6.5)),
    ]



@icon("wash-bottle", CAT, "Lab wash bottle: a squeezable bottle with a long bent spout tube from the cap",
      tags=["squeeze bottle", "rinse", "laboratory", "chemistry", "distilled water", "solvent", "dispenser"])
def _(S):
    return [
        line("M9.5 7V4H18.5V8"),
        shell(union(rect(4, 10, 11, 11, L(S, 2, 3.5)), rect(7, 6.5, 5, 4.5, L(S, 0.5, 1)))),
        detail(seg(4, 15, 15, 15)),
    ]


@icon("lab-incubator", CAT, "Lab incubator cabinet with a glass door and shelf, and a display and dial below",
      tags=["culture incubator", "warming cabinet", "microbiology", "cell culture", "temperature control", "lab equipment", "oven"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, L(S, 2, 3.5))),
        detail(rect(5.5, 5, 13, 10.5)),
        detail(seg(5.5, 10.25, 18.5, 10.25)),
        Part("dot", rect(6.5, 18, 6, 2)),
        dot(16.5, 19, 1.1),
    ]


@icon("ampoule", CAT, "Glass ampoule with a narrow neck and a sealed pointed tip",
      tags=["vial", "injection", "glass vial", "sealed", "medicine", "drug", "pharmacy"])
def _(S):
    return [
        shell(poly([(12, 2.5), (13.5, 6), (13.5, 9), (17, 12), (17, 19.5), (7, 19.5), (7, 12), (10.5, 9), (10.5, 6)],
                   closed=True, r=S.r * 1.5)),
        detail(seg(7, 15.5, 17, 15.5)),
    ]


@icon("vaccination-card", CAT, "Vaccination record card with a small syringe and rows of check boxes",
      tags=["immunization record", "vaccine passport", "shot record", "covid card", "health record", "proof", "booster"])
def _(S):
    m = axis((6.5, 8.5), -25)
    return [
        shell(rect(3, 3, 18, 18, L(S, 2, 3.5))),
        detail(mseg(m, 0, 0, 7, 0)),
        detail(mseg(m, 7, -2, 7, 2)),
        detail(mseg(m, 7, 0, 10, 0)),
        Part("dot", rect(6, 12, 2.5, 2.5)),
        detail(seg(11, 13.25, 18, 13.25)),
        Part("dot", rect(6, 16, 2.5, 2.5)),
        detail(seg(11, 17.25, 18, 17.25)),
    ]


@icon("vaccine-cooler", CAT, "Vaccine carrier: an insulated box with a lid line, a handle and a snowflake",
      tags=["cold chain", "cool box", "immunization", "insulated", "transport", "vaccine storage", "carrier"])
def _(S):
    out = [
        line("M8.5 8V4.5H15.5V8"),
        shell(rect(3, 8, 18, 13.5, L(S, 1.5, 3))),
        detail(seg(3, 11.5, 21, 11.5)),
    ]
    for a in (90, 30, 150):
        x1, y1 = polar(12, 16.25, 3, a)
        x2, y2 = polar(12, 16.25, 3, a + 180)
        out.append(detail(seg(x1, y1, x2, y2)))
    return out


@icon("microneedle-patch", CAT, "Microneedle patch seen from the side with a row of tiny cone spikes underneath",
      tags=["transdermal", "needle free", "skin patch", "vaccine delivery", "drug delivery", "microarray", "painless"])
def _(S):
    out = [shell(rect(3, 5, 18, 5.5, L(S, 1, 2.5)))]
    for x in (5, 8.6, 12.2, 15.8):
        out.append(solid(poly([(x, 10), (x + 3, 10), (x + 1.5, 18)], closed=True)))
    return out


@icon("softgel", CAT, "Glossy oval softgel capsule set on a diagonal with a shine mark",
      tags=["gel capsule", "capsule", "supplement", "fish oil", "vitamin", "pill", "medicine"])
def _(S):
    body = L(S, rect(2.5, 7.25, 19, 9.5, 4.75), ellipse(12, 12, 9.5, 5.5))
    return [
        shell(rot(body, -35)),
        detail(rot("M7.5 10.75Q8.6 9.4 11.5 9.2", -35)),
    ]

@icon("lozenge", CAT, "Throat lozenge: a diamond-shaped sweet with a twisted wrapper at each end",
      tags=["cough drop", "throat sweet", "candy", "sore throat", "menthol", "hard candy", "remedy"])
def _(S):
    return [
        shell(poly([(12, 6.5), (17, 12), (12, 17.5), (7, 12)], closed=True, r=S.r * 1.5)),
        shell(poly([(7.5, 12), (2.5, 8), (2.5, 16)], closed=True, r=S.r * 0.6)),
        shell(poly([(16.5, 12), (21.5, 8), (21.5, 16)], closed=True, r=S.r * 0.6)),
    ]


@icon("syrup-bottle", CAT, "Cough syrup bottle with a label and a dosing cup upside down on the cap",
      tags=["cough medicine", "liquid medicine", "cold remedy", "elixir", "pharmacy", "tonic", "suspension"])
def _(S):
    cup = poly([(8.5, 2.5), (15.5, 2.5), (16.5, 7), (7.5, 7)], closed=True, r=S.r * 0.4)
    body = union(rect(5, 10, 14, 11.5, L(S, 2, 3.5)), rect(8.5, 6.5, 7, 4, 0.5), cup)
    return [
        shell(body),
        detail(rect(7.75, 13, 8.5, 5)),
    ]


@icon("medicine-cup", CAT, "Dosing cup: a small plastic cup with measuring lines up its side",
      tags=["measuring cup", "dose", "liquid medicine", "ml", "pharmacy", "syrup", "graduated"])
def _(S):
    return [
        shell(poly([(5, 3.5), (19, 3.5), (17, 21), (7, 21)], closed=True, r=S.r)),
        detail(seg(7.75, 8, 11.5, 8)),
        detail(seg(7.5, 12, 11.5, 12)),
        detail(seg(7.25, 16, 11.5, 16)),
    ]


@icon("oral-syringe", CAT, "Oral dosing syringe with a short round nozzle, scale marks and a plunger",
      tags=["needle free", "liquid dose", "infant medicine", "pediatric", "pharmacy", "measure", "dropper"])
def _(S):
    m = axis((11.5, 12.5), -45)
    return [
        line(mseg(m, -10, 0, -6, 0)),
        shell(mpoly(m, [(-6, -2.75), (5, -2.75), (5, 2.75), (-6, 2.75)], closed=True, r=S.r * 0.5)),
        detail(mseg(m, -3, -2.75, -3, -0.5)),
        detail(mseg(m, 0, -2.75, 0, -0.5)),
        line(mseg(m, 5, -4.5, 5, 4.5)),
        line(mseg(m, 5, 0, 10, 0)),
        line(mseg(m, 10, -3.5, 10, 3.5)),
    ]


@icon("dosing-spoon", CAT, "Medicine spoon with a tube handle marked in measures and a scooped end",
      tags=["measuring spoon", "liquid dose", "teaspoon", "pharmacy", "pediatric", "syrup", "dose"])
def _(S):
    m = axis((3, 21), -45)
    handle = mpoly(m, [(0, -1.75), (14.5, -1.75), (14.5, 1.75), (0, 1.75)], closed=True, r=S.r * 0.4)
    return [
        shell(union(handle, circle(*m(17.5, 0), 3.75))),
        detail(mseg(m, 4, -1.75, 4, 1.75)),
        detail(mseg(m, 8, -1.75, 8, 1.75)),
    ]


@icon("nasal-spray", CAT, "Nasal spray bottle with a short upright nozzle and a fan of mist from its tip",
      tags=["nose spray", "decongestant", "allergy", "saline", "rhinitis", "cold", "pump bottle"])
def _(S):
    out = [
        shell(rect(5, 12, 9, 9.5, L(S, 1.5, 3))),
        shell(rect(7.5, 8.5, 4, 3.5, L(S, 0.5, 1))),
        line("M9.5 8.5V4.5H12.5"),
    ]
    for a in (-35, 0, 35):
        x1, y1 = polar(14.5, 4.5, 2.2, a)
        x2, y2 = polar(14.5, 4.5, 5.2, a)
        out.append(line(seg(x1, y1, x2, y2)))
    return out


@icon("throat-spray", CAT, "Throat spray bottle with a long curved spray arm and a mist cloud at its end",
      tags=["sore throat", "oral spray", "mouth spray", "pump", "anesthetic", "pharyngitis", "remedy"])
def _(S):
    return [
        shell(rect(3.5, 11, 9, 10.5, L(S, 1.5, 3))),
        shell(rect(6, 7.5, 4, 3.5, L(S, 0.5, 1))),
        line("M8 7.5V5.5Q8 3.5 10 3.5H15"),
        dot(18, 3.5, 1.2), dot(21, 3.5, 1.2), dot(19.5, 6.25, 1.2),
    ]


@icon("suppository", CAT, "Smooth bullet-shaped suppository with a rounded tip, shown on a diagonal",
      tags=["rectal", "pessary", "medication", "dosage form", "pharmacy", "insert", "torpedo"])
def _(S):
    body = L(S, "M4 7.5H13Q21.5 9 21.5 12Q21.5 15 13 16.5H4Z", "M4.5 7.5H13Q21.5 9 21.5 12Q21.5 15 13 16.5H4.5Q3 16.5 3 15V9Q3 7.5 4.5 7.5Z")
    return [
        shell(rot(body, -30)),
        detail(rot("M7.5 11H12", -30)),
    ]


@icon("transdermal-patch", CAT, "Square adhesive skin patch with a corner peeled back and a drug pad in the centre",
      tags=["nicotine patch", "medicated patch", "hormone patch", "pain relief", "skin", "adhesive", "drug delivery"])
def _(S):
    return [
        shell(poly([(3.5, 5.5), (13, 5.5), (20.5, 13), (20.5, 20), (3.5, 20)], closed=True, r=S.r * 1.3)),
        detail(poly([(13, 6), (13, 13), (20, 13)])),
        Part("dot", rect(6.5, 14, 6, 3.5, L(S, 0.5, 1.75))),
    ]

@icon("powder-sachet", CAT, "Medicine sachet with crimped ends, a torn top corner and powder spilling out",
      tags=["stick pack", "packet", "oral rehydration", "powder medicine", "dose", "single use", "pouch"])
def _(S):
    return [
        shell(poly([(4, 5.5), (13, 5.5), (16.5, 8.5), (16.5, 21), (4, 21)], closed=True, r=S.r)),
        detail(seg(4, 9.25, 12.5, 9.25)),
        detail(seg(4, 17.25, 16.5, 17.25)),
        dot(19, 5, 1.1), dot(21, 8, 1.1), dot(19.25, 11, 1.1),
    ]

@icon("blister-pack", CAT, "Pill blister pack: a foil card with two rows of bubbles and one empty ring",
      tags=["pill strip", "tablet pack", "foil card", "medication", "pills", "dispenser", "pharmacy"])
def _(S):
    out = [shell(rect(2.5, 5, 19, 14, L(S, 1.5, 4)))]
    for yy in (9.75, 14.25):
        for i, xx in enumerate((6.75, 12, 17.25)):
            if yy == 14.25 and i == 1:
                out.append(detail(circle(xx, yy, 1.4)))
            else:
                out.append(dot(xx, yy, 1.6))
    return out


@icon("contraceptive-pill-pack", CAT, "Round birth control pill dial case with pills arranged in a ring",
      tags=["birth control", "oral contraceptive", "family planning", "pill dispenser", "women's health", "dial pack", "tablets"])
def _(S):
    out = [shell(union(circle(12, 10.75, 8.75), rect(9, 16.5, 6, 5, L(S, 0, 1.75))))]
    for i in range(10):
        x, y = polar(12, 10.75, 5.4, -90 + 36 * i)
        out.append(dot(x, y, 1.15))
    out.append(dot(12, 10.75, 1.15))
    return out


@icon("pill-organizer", CAT, "Weekly pill organizer box with a row of seven compartment lids and one flipped open",
      tags=["pill box", "medication planner", "daily dose", "weekday pills", "pillbox", "tablets", "reminder"])
def _(S):
    out = [
        shell(rect(2, 9.5, 20, 10, L(S, 1.5, 3.5))),
        shell(poly([(15.5, 9.5), (15.5, 4), (20.5, 5.5), (20.5, 9.5)], closed=True, r=S.r * 0.5)),
    ]
    for i in range(6):
        out.append(dot(4.75 + i * 2.05, 14.5, 0.7))
    return out
