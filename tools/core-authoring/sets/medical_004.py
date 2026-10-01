"""TypeIcon Core: medical equipment (batch medical_004).

Pharmacy items, care and rehab aids, small surgical and lab instruments, implants and mobility equipment,
drawn from the objects themselves. No red-cross emblem; a plain plus marks medical contents.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, polar  # noqa: F401

CAT = "medical"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def axis(origin, deg):
    """Local frame: x runs along `deg` (0 = right, positive = clockwise on screen)."""
    ox, oy = origin
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return lambda x, y: (ox + x * c - y * s, oy + x * s + y * c)


def mseg(m, x0, y0, x1, y1):
    return seg(*m(x0, y0), *m(x1, y1))


def mpoly(m, pts, closed=False, r=0.0):
    return poly([m(x, y) for x, y in pts], closed=closed, r=r)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def plus(cx, cy, k):
    """Plain plus sign strokes (two detail parts)."""
    return [detail(seg(cx, cy - k, cx, cy + k)), detail(seg(cx - k, cy, cx + k, cy))]


# ============================================================================ pharmacy

@icon("pill-cutter", CAT, "Pill splitter with a blade in the lid held above a round tablet on its base",
      tags=["pill splitter", "tablet cutter", "half tablet", "medication", "dose", "pharmacy"],
      aliases=["pill-splitter"])
def _(S):
    lid = poly([(3, 2.5), (21, 2.5), (21, 5), (14, 5), (12, 8), (10, 5), (3, 5)], closed=True, r=S.r * 0.5)
    return [
        shell(union(rect(3, 17, 18, 4, L(S, 1, 2)), circle(12, 13.5, 3.75))),
        shell(lid),
    ]


@icon("medicine-box", CAT, "Medicine carton with a plus sign and a blister pack sliding out of its side",
      tags=["drug box", "medication", "pharmacy", "tablets", "prescription", "blister pack"])
def _(S):
    return [
        shell(rect(2.5, 4, 12.5, 16, L(S, 1, 2.5))),
        *plus(8.75, 12, 3),
        shell(rect(15, 8.5, 6.5, 9, L(S, 0, 1.5))),
        dot(18.25, 11.5, 1.1),
        dot(18.25, 14.5, 1.1),
    ]


@icon("medicine-bag", CAT, "Folded paper pharmacy bag with a plus sign on the front",
      tags=["pharmacy bag", "prescription bag", "drugstore", "pickup", "medication", "chemist"],
      aliases=["pharmacy-bag"])
def _(S):
    return [
        shell(rect(5, 3.5, 14, 17.5, L(S, 1, 3))),
        detail(seg(5, 8, 19, 8)),
        *plus(12, 14.5, 2.75),
    ]


@icon("pill-counting-tray", CAT, "Pharmacy counting tray with a side channel, three pills and a spatula",
      tags=["pill counter", "pharmacy tray", "tablets", "dispensing", "spatula", "count"])
def _(S):
    return [
        shell(rect(2.5, 9, 12.5, 12, L(S, 1, 3))),
        detail(seg(11, 9, 11, 21)),
        dot(5.75, 13, 1.25),
        dot(5.75, 17.25, 1.25),
        dot(8.25, 15.25, 1.25),
        shell(rect(18.5, 3, 3, 8, L(S, 0.5, 1.5))),
        line(seg(20, 11, 20, 21)),
    ]


@icon("apothecary-jar", CAT, "Waisted lidded apothecary jar with a blank label",
      tags=["pharmacy jar", "chemist", "remedy", "old pharmacy", "herbal", "storage jar"])
def _(S):
    r = L(S, 1, 3)
    body = (f"M8 8H16C18.5 9.5 19 12 19 14.5V{21 - r}"
            f"{'a%s %s 0 0 1 -%s %s' % (r, r, r, r) if r else ''}H{5 + r}"
            f"{'a%s %s 0 0 1 -%s -%s' % (r, r, r, r) if r else ''}V14.5C5 12 5.5 9.5 8 8Z")
    return [
        shell(rect(8, 3, 8, 5, L(S, 1, 2))),
        shell(body),
        detail(rect(8, 13.5, 8, 4.5)),
    ]


@icon("enema-bulb", CAT, "Squeezable rubber bulb syringe with a long tapered nozzle",
      tags=["bulb syringe", "rubber bulb", "irrigation", "douche", "squeeze bulb", "rinse"],
      aliases=["bulb-syringe"])
def _(S):
    m = axis((8, 16), -45)
    nozzle = mpoly(m, [(4.5, -1.9), (16.5, -0.7), (16.5, 0.7), (4.5, 1.9)], closed=True, r=S.r * 0.4)
    return [
        shell(union(circle(8, 16, 5.5), nozzle)),
        detail(mseg(m, 5.2, -2.2, 5.2, 2.2)),
    ]


@icon("nasal-aspirator", CAT, "Baby nasal aspirator with a round squeeze bulb and a short soft tip",
      tags=["baby", "snot sucker", "nose cleaner", "infant", "congestion", "newborn", "bulb"])
def _(S):
    tip = poly([(9.5, 11), (10.75, 3.5), (13.25, 3.5), (14.5, 11)], closed=True, r=S.r * 0.4)
    return [
        shell(union(circle(12, 16, 5.5), tip)),
        detail(seg(8.5, 11, 15.5, 11)) if S.name == "line" else detail(arc(12, 16, 3, 20, 160)),
    ]


@icon("breast-pump", CAT, "Breast pump with a funnel shaped flange, a collection bottle and a short stem",
      tags=["nursing", "lactation", "milk", "baby", "breastfeeding", "expressing", "mother"])
def _(S):
    flange = poly([(2.5, 4), (9, 8.5), (9, 12), (2.5, 16.5)], closed=True, r=S.r * 0.6)
    stem = rect(9, 8.5, 9, 3.5, L(S, 0.5, 1.5))
    bottle = rect(12.5, 11.5, 8.5, 9.5, L(S, 1, 3))
    return [
        shell(union(flange, stem, bottle)),
        detail(seg(12.5, 16.5, 21, 16.5)),
    ]


@icon("umbilical-clamp", CAT, "Umbilical cord clamp with two jaws joined at a hinge and a locking tooth at the tip",
      tags=["newborn", "cord clamp", "birth", "delivery", "midwife", "obstetrics", "baby"],
      aliases=["cord-clamp"])
def _(S):
    return [
        shell(poly([(3, 6), (21, 6), (21, 11.5), (17.5, 11.5), (17.5, 10), (7, 10), (7, 14), (17.5, 14),
                    (17.5, 18), (3, 18)], closed=True, r=S.r)),
    ]


@icon("bowl-of-hygieia", CAT, "Stemmed bowl with a snake winding up past the rim, the pharmacy symbol",
      tags=["pharmacy symbol", "snake", "cup", "pharmacist", "medicine emblem", "chemist", "serpent"],
      aliases=["hygieia-bowl"])
def _(S):
    return [
        shell("M3 8.5H17c0 4.2-3 7-7 7S3 12.7 3 8.5Z"),
        line(seg(10, 15.5, 10, 19.5)),
        line(seg(6.5, 20, 13.5, 20)),
        line("M9 17.5C15 17.5 16 13.5 19.5 13.5C22 13.5 21.5 9 19.5 6.5"),
        dot(19.5, 4.75, 1.4),
    ]


@icon("plague-doctor-mask", CAT, "Plague doctor mask in profile with a long curved beak, round eye and a hat",
      tags=["beak mask", "plague", "history", "doctor", "medieval", "costume", "pandemic"])
def _(S):
    face = ("M9.5 10.5C12 8.5 15 8.5 17 10C19.5 12 19.5 17 17 19.5H12L11 17Q5 17.5 2.5 16.5Q4.5 12.5 9.5 10.5Z")
    return [
        shell(face),
        detail(circle(12, 13.25, 1.25)) if S.name == "line" else dot(12, 13.25, 1.25),
        shell(poly([(9, 8), (10, 3.5), (17, 3.5), (18, 8)], closed=True, r=S.r * 0.5)),
        line(seg(6.5, 8, 20.5, 8)),
    ]


@icon("alcohol-swab", CAT, "Small alcohol prep sachet with a torn corner, a wet pad peeking out and a drop",
      tags=["prep pad", "antiseptic wipe", "sanitizer", "injection prep", "sterile", "wipe", "first aid"],
      aliases=["alcohol-prep-pad"])
def _(S):
    return [
        shell(poly([(4, 21), (4, 7), (13, 7), (16.5, 3.5), (21, 8), (17.5, 11.5), (20, 14), (20, 21)],
                   closed=True, r=S.r * 0.5)),
        detail(seg(13, 7, 17.5, 11.5)),
        Part("dot", "M10 11.5L12.3 15.2A2.3 2.3 0 1 1 7.7 15.2Z"),
    ]


@icon("medical-tape", CAT, "Roll of adhesive medical tape with a torn strip pulled out below",
      tags=["surgical tape", "adhesive tape", "bandage", "dressing", "first aid", "wound care", "micropore"])
def _(S):
    strip = poly([(9, 17), (21.5, 17), (20, 19.25), (21.5, 21.5), (9, 21.5)], closed=True, r=S.r * 0.4)
    return [
        shell(union(circle(9.5, 10.5, 7.5), strip)),
        detail(circle(9.5, 10.5, 2.5)),
    ]


@icon("gauze-pad", CAT, "Square gauze pad with a woven grid pattern",
      tags=["gauze", "dressing", "compress", "sterile pad", "wound care", "first aid", "swab"],
      aliases=["gauze-swab"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, L(S, 1, 4))),
        detail(seg(9, 3, 9, 21)),
        detail(seg(15, 3, 15, 21)),
        detail(seg(3, 9, 21, 9)),
        detail(seg(3, 15, 21, 15)),
    ]


@icon("medical-scale", CAT, "Doctor's balance beam scale with a sliding weight, a tall column and a platform",
      tags=["weighing scale", "weight check", "clinic", "bmi", "physician scale", "weigh in", "patient weight"],
      aliases=["beam-scale"])
def _(S):
    return [
        line(seg(3, 4.5, 21, 4.5)),
        shell(rect(15.5, 4.5, 4, 4, L(S, 0, 1))),
        shell(union(rect(10, 4.5, 3, 14), rect(3, 18, 18, 3, L(S, 0.5, 1.5)))),
    ]


# ============================================================================ clinic equipment

@icon("health-insurance-card", CAT, "Rounded health insurance card with a plus sign in one corner and lines of text",
      tags=["medical card", "insurance", "coverage", "patient id", "policy", "member card", "healthcare"],
      aliases=["medical-card"])
def _(S):
    return [
        shell(rect(2.5, 5, 19, 14, L(S, 1.5, 3.5))),
        *plus(7.75, 10, 2.25),
        detail(seg(13, 9.5, 18.5, 9.5)),
        detail(seg(6, 15, 18.5, 15)),
    ]


@icon("pill-crusher", CAT, "Two part pill crusher with a tablet squeezed between its ridged halves",
      tags=["tablet crusher", "grind pills", "medication", "swallowing aid", "pharmacy", "powder", "dose"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 6, L(S, 1, 3))),
        detail(seg(9, 2.5, 9, 8.5)),
        detail(seg(15, 2.5, 15, 8.5)),
        shell(rect(5, 15.5, 14, 6, L(S, 1, 3))),
        shell(ellipse(12, 12, 4.25, 2.25)) if S.name == "line" else shell(ellipse(12, 12, 3.75, 2.25)),
    ]


@icon("medical-ventilator", CAT, "Ventilator on a stand with a waveform screen and a looping breathing hose",
      tags=["respirator", "life support", "icu", "breathing machine", "intubated", "hospital", "critical care"],
      aliases=["respirator-machine"])
def _(S):
    return [
        shell(rect(3, 3, 13, 10, L(S, 1, 2.5))),
        detail(poly([(5, 8), (8, 8), (9.5, 5.75), (11, 10.25), (12.5, 8), (14, 8)], r=S.r * 0.5)),
        line(seg(9.5, 13, 9.5, 20)),
        line(seg(5, 20.5, 14, 20.5)),
        line("M16 6H19.5A2 2 0 0 1 21.5 8V14A2 2 0 0 1 19.5 16H16"),
        line("M16 10H18"),
    ]


@icon("vein-finder", CAT, "Handheld vein finder projecting light onto a forearm that shows branching veins",
      tags=["venipuncture", "blood draw", "infrared", "nurse", "iv placement", "arm", "phlebotomy"],
      aliases=["vein-scanner"])
def _(S):
    return [
        shell(rect(6.5, 2.5, 11, 4.5, L(S, 1, 2.25))),
        line(seg(9, 9, 5.5, 13)),
        line(seg(15, 9, 18.5, 13)),
        shell(rect(2.5, 14, 19, 7.5, L(S, 1.5, 3.5))),
        detail(poly([(6, 18.5), (11, 18.5), (15.5, 16.5)], r=S.r * 0.5)),
        detail(seg(11, 18.5, 15.5, 20)),
    ]


@icon("amsler-grid", CAT, "Square grid of fine lines with a solid dot at its centre",
      tags=["macular degeneration", "eye test", "vision check", "distortion", "retina", "ophthalmology", "self test"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, L(S, 1, 3.5)))]
    for v in (7.5, 12, 16.5):
        parts.append(detail(seg(v, 3, v, 21)))
        parts.append(detail(seg(3, v, 21, v)))
    parts.append(dot(12, 12, 2))
    return parts


@icon("stool-test", CAT, "Stool sample tube with a screw cap and the collection scoop inside",
      tags=["faecal test", "fecal sample", "specimen", "lab sample", "bowel screening", "collection kit", "gut health"],
      aliases=["stool-sample-tube"])
def _(S):
    r = L(S, 1, 4)
    body = f"M8 9V{21 - r}" + (f"a{r} {r} 0 0 0 {r} {r}H{16 - r}a{r} {r} 0 0 0 {r} -{r}" if r else "H16") + "V9Z"
    return [
        shell(rect(7, 3, 10, 6, L(S, 1, 2))),
        shell(body),
        detail(seg(12, 9.5, 12, 14)),
        dot(12, 16.25, 1.2),
    ]


@icon("fetal-monitor", CAT, "Fetal monitor with a screen, a paper strip below it and two belt sensors on cables",
      tags=["cardiotocography", "ctg", "labour", "labor", "pregnancy", "heartbeat", "maternity", "obstetrics"],
      aliases=["ctg-machine"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 13, 9.5, L(S, 1, 2.5))),
        detail(rect(6, 5, 6, 4, L(S, 0, 1))),
        shell(rect(5, 14, 8, 7, L(S, 0.5, 1.5))),
        detail(poly([(6.5, 17.5), (8.25, 16), (9.75, 19), (11.5, 17.5)], r=S.r * 0.4)),
        line("M15.5 6H17.5"),
        line("M15.5 17H19V12.5"),
        shell(circle(19.5, 5.75, 2.25)),
        shell(circle(19, 10.25, 0.01)) if False else dot(19.5, 10.5, 1.4),
    ]


@icon("ecg-machine", CAT, "ECG cart with a heartbeat screen, a paper slot and lead wires ending in electrodes",
      tags=["electrocardiogram", "ekg", "heart test", "cardiology", "leads", "cardiac monitor", "clinic"],
      aliases=["ekg-machine"])
def _(S):
    return [
        shell(rect(2.5, 3, 15, 13, L(S, 1, 2.5))),
        detail(poly([(5, 8), (7.5, 8), (9, 5.5), (11, 10.5), (12.5, 8), (15, 8)], r=S.r * 0.5)),
        detail(seg(2.5, 12.5, 17.5, 12.5)),
        line(seg(10, 16, 10, 20)),
        line(seg(5.5, 20.5, 14.5, 20.5)),
        line("M17.5 7H19.5A1.5 1.5 0 0 1 21 8.5V16"),
        line("M17.5 10H18.5A1 1 0 0 1 19.5 11V17"),
        dot(21, 18.25, 1.25),
        dot(19.5, 19.25, 1.25),
    ]


@icon("sponge-forceps", CAT, "Long forceps crossing at a pivot with a ring at each handle and each jaw",
      tags=["surgical forceps", "ring forceps", "foerster", "swab holder", "operating room", "instrument", "clamp"],
      aliases=["ring-forceps"])
def _(S):
    def ring(cx, cy, r=2.25):
        return poly(regular(cx, cy, r + 0.35, 8, start=22.5), closed=True) if S.name == "line" else circle(cx, cy, r)
    return [
        shell(ring(8, 18.5)),
        shell(ring(16, 18.5)),
        shell(ring(8.5, 5.25)),
        shell(ring(15.5, 5.25)),
        line(seg(9.2, 16.6, 15.1, 7.4)),
        line(seg(14.8, 16.6, 8.9, 7.4)),
    ]


@icon("suction-tip", CAT, "Rigid curved suction tube with a rounded bulb tip and a hose connector at the back",
      tags=["yankauer", "suction", "surgery", "oral suction", "aspirator", "dental", "theatre"],
      aliases=["yankauer"])
def _(S):
    return [
        shell(rect(3, 15.5, 4, 6, L(S, 0.5, 1.5))),
        line("M5 15.5V12C5 8 8 5.5 12 5.5H15"),
        shell(ellipse(18.5, 5.5, 3.5, 2.75)),
        dot(18.5, 5.5, 0.9),
    ]


@icon("operating-microscope", CAT, "Floor stand operating microscope with a boom arm holding a binocular head pointing down",
      tags=["surgical microscope", "microsurgery", "theatre", "neurosurgery", "ophthalmic surgery", "magnification", "surgeon"],
      aliases=["surgical-microscope"])
def _(S):
    return [
        line(seg(3, 21, 11, 21)),
        line(seg(7, 21, 7, 5)),
        line(seg(7, 5, 14, 5)),
        shell(rect(13.5, 3.5, 7.5, 8.5, L(S, 1, 2.5))),
        shell(poly([(15.5, 12), (19, 12), (18.5, 18), (16, 18)], closed=True, r=S.r * 0.5)),
    ]


@icon("cold-spray", CAT, "Aerosol can with a snowflake on its label spraying a cloud of cold mist",
      tags=["ice spray", "sports injury", "cryotherapy", "pain relief", "aerosol", "cooling", "first aid"],
      aliases=["ice-spray"])
def _(S):
    return [
        shell(rect(3, 8.5, 9, 12.5, L(S, 1, 3))),
        shell(rect(5, 4, 5, 4.5, L(S, 0.5, 1.5))),
        line(seg(10, 5.5, 13, 5.5)),
        detail(seg(7.5, 12, 7.5, 18)),
        detail(seg(5, 13.5, 10, 16.5)),
        detail(seg(5, 16.5, 10, 13.5)),
        dot(16, 4, 1.2), dot(19.5, 6.5, 1.2), dot(16, 8.5, 1.2), dot(20, 11, 1.2), dot(16.5, 13, 1.2),
    ]


@icon("patient-trapeze", CAT, "Hospital bed with an overhead frame and a triangular grab handle hanging from a strap",
      tags=["bed handle", "hospital bed", "mobility aid", "pull up", "overhead bar", "rehabilitation", "nursing"],
      aliases=["bed-trapeze"])
def _(S):
    return [
        shell(rect(3, 17, 18, 3.5, L(S, 0.5, 1.75))),
        line(poly([(4.5, 17), (4.5, 3.5), (16, 3.5)], r=S.r)),
        line(seg(16, 3.5, 16, 7)),
        shell(poly([(16, 7.5), (19.5, 13.5), (12.5, 13.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("medical-fridge", CAT, "Tall medical refrigerator with a plus sign on top and vials on the shelf below",
      tags=["vaccine fridge", "cold storage", "pharmacy fridge", "samples", "vials", "lab refrigerator", "cold chain"],
      aliases=["vaccine-fridge"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, L(S, 1.5, 3.5))),
        detail(seg(5, 11.25, 19, 11.25)),
        *plus(12, 6.75, 2),
        sq(8, 14, 2, 4.5), sq(11, 14, 2, 4.5), sq(14, 14, 2, 4.5),
    ]


@icon("beach-wheelchair", CAT, "Wheelchair on a simple frame with fat balloon wheels for sand",
      tags=["all terrain wheelchair", "sand", "accessible beach", "disability", "mobility", "seaside", "balloon tyres"],
      aliases=["sand-wheelchair"])
def _(S):
    return [
        shell(circle(8.5, 16.5, 4.75)),
        dot(8.5, 16.5, 1.1),
        shell(circle(19, 18.5, 2.75)),
        line(poly([(6, 3.5), (7.5, 12), (15, 12), (18.5, 16)], r=S.r)),
        line(seg(6.5, 7.5, 11, 7.5)),
    ]


@icon("wheelchair-lift", CAT, "Raised platform lift with a side rail and a wheelchair on it beside a lift column",
      tags=["platform lift", "accessibility", "elevator", "disability", "vertical lift", "mobility", "access"],
      aliases=["platform-lift"])
def _(S):
    return [
        shell(rect(2.5, 17, 14, 3.5, L(S, 0.5, 1.75))),
        line(seg(19.5, 3, 19.5, 21.5)),
        line(seg(16.5, 18.75, 19.5, 18.75)),
        shell(circle(8, 12.5, 3)),
        line(poly([(6, 3.5), (6, 10), (11.5, 10), (13.5, 14)], r=S.r)),
    ]


@icon("halo-brace", CAT, "Head inside a halo ring held by rods that run down to a chest vest",
      tags=["cervical brace", "neck fracture", "spinal injury", "halo vest", "orthopedic", "immobilization", "neck support"],
      aliases=["halo-vest"])
def _(S):
    ring = "M4.5 8A7.5 2.5 0 1 0 19.5 8A7.5 2.5 0 1 0 4.5 8Z"
    return [
        shell(circle(12, 9.75, 3.75)),
        line(ring),
        line(seg(4.5, 8, 4.5, 16.5)),
        line(seg(19.5, 8, 19.5, 16.5)),
        shell(poly([(4, 16.5), (20, 16.5), (18, 21.5), (6, 21.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("ankle-foot-orthosis", CAT, "L shaped plastic brace running up the back of the calf and under the foot with a strap",
      tags=["afo", "drop foot", "leg brace", "orthotic", "splint", "gait", "rehabilitation"],
      aliases=["afo-brace"])
def _(S):
    return [
        shell(poly([(5, 3), (10, 3), (10, 14.5), (20.5, 14.5), (20.5, 20), (5, 20)], closed=True, r=S.r)),
        line(seg(3, 8, 12, 8)),
    ]


@icon("cell-culture-flask", CAT, "Flat culture flask lying on its side with a slanted neck and a vented cap",
      tags=["tissue culture", "lab", "cells", "petri", "biology", "growth medium", "incubator"],
      aliases=["culture-flask"])
def _(S):
    m = axis((14.5, 10.5), -45)
    return [
        shell(rect(3, 10, 12, 10.5, L(S, 1, 2.5))),
        detail(seg(3, 15, 15, 15)),
        dot(7, 18, 0.9), dot(11, 18, 0.9),
        shell(mpoly(m, [(0, -1.75), (3, -1.75), (3, 1.75), (0, 1.75)], closed=True)),
        shell(mpoly(m, [(3, -2.75), (5.5, -2.75), (5.5, 2.75), (3, 2.75)], closed=True, r=S.r * 0.4)),
    ]


@icon("multichannel-pipette", CAT, "Handheld pipette with a wide head bar holding a row of pipette tips",
      tags=["lab pipette", "liquid handling", "laboratory", "96 well plate", "sampling", "science", "chemistry"],
      aliases=["multi-pipette"])
def _(S):
    return [
        shell(rect(9, 2.5, 6, 9, L(S, 1, 3))),
        shell(rect(3, 11.5, 18, 4, L(S, 0.5, 2))),
        line(seg(5.25, 15.5, 5.25, 21.5)),
        line(seg(9.75, 15.5, 9.75, 21.5)),
        line(seg(14.25, 15.5, 14.25, 21.5)),
        line(seg(18.75, 15.5, 18.75, 21.5)),
    ]


@icon("laser-eye-surgery", CAT, "Eye seen from the front with a laser beam from above hitting the pupil with small sparks",
      tags=["lasik", "eye operation", "vision correction", "ophthalmology", "refractive surgery", "retina laser", "sight"],
      aliases=["lasik"])
def _(S):
    return [
        shell("M2.5 15.5Q12 7.5 21.5 15.5Q12 23.5 2.5 15.5Z"),
        detail(circle(12, 15.5, 3)),
        line(seg(12, 2.5, 12, 8.5)),
        line(seg(8.5, 6, 6.5, 4.5)),
        line(seg(15.5, 6, 17.5, 4.5)),
    ]


@icon("nasal-strip", CAT, "Nose in profile with a flexible adhesive strip stuck across the bridge",
      tags=["breathe right", "snoring", "congestion", "nasal dilator", "sleep aid", "nose", "airflow"],
      aliases=["nasal-dilator"])
def _(S):
    m = axis((13.8, 9), 30)
    return [
        line("M16.5 2.5C16.5 4.5 15.8 6 14.8 7.3"),
        line("M12.8 10.7C11.5 12 10 13 9.5 14C8 15.5 8.7 17.5 11 17.5H16"),
        shell(mpoly(m, [(-6.5, -2), (6.5, -2), (6.5, 2), (-6.5, 2)], closed=True, r=S.r * 0.6)),
    ]


@icon("pacifier-thermometer", CAT, "Baby pacifier with a small digital display on its shield and a ring handle",
      tags=["baby thermometer", "infant", "fever", "temperature", "dummy", "soother", "newborn"],
      aliases=["dummy-thermometer"])
def _(S):
    return [
        shell(rect(3, 3.5, 18, 11.5, L(S, 2.5, 5.75))),
        detail(rect(8, 7, 8, 4.5, L(S, 0, 1.25))),
        line(arc(12, 15.75, 3.5, 0, 180)),
    ]


@icon("saliva-collection-tube", CAT, "Slim sample tube with a wide funnel on top and a cap hanging on a strap",
      tags=["saliva test", "dna kit", "spit tube", "genetic test", "specimen", "covid test", "lab sample"],
      aliases=["spit-tube"])
def _(S):
    r = L(S, 1, 3)
    tube = f"M9 10V{21.5 - r}" + (f"a{r} {r} 0 0 0 {r} {r}H{15 - r}a{r} {r} 0 0 0 {r} -{r}" if r else "H15") + "V10Z"
    return [
        shell(union(poly([(5.5, 3), (18.5, 3), (15, 10), (9, 10)], closed=True, r=S.r * 0.4), tube)),
        line("M18 5.5C21.5 5.5 21.5 9 20.5 11"),
        shell(rect(18.5, 11.25, 4, 4, L(S, 0.5, 1.5))) if False else shell(rect(18.25, 11.5, 4.5, 4, L(S, 0.5, 1.25))),
    ]


@icon("heel-prick-test", CAT, "Sole of a newborn foot with a single blood drop falling from the heel",
      tags=["newborn screening", "baby blood test", "infant", "foot", "neonatal", "guthrie", "blood sample"],
      aliases=["newborn-screening"])
def _(S):
    foot = ("M6.5 9C6.5 6.5 9 5.5 11.5 5.5C14.5 5.5 16.5 7 16.5 10C16.5 12 14 12.5 13.5 14.5"
            "C13 16.5 12 17.5 10.25 17.5C8.5 17.5 7.75 16 8 14C8.25 12 6.5 11 6.5 9Z")
    return [
        shell(foot),
        *([sq(7.5, 2, 2, 2), sq(10.5, 1.5, 2, 2), sq(13.25, 2, 2, 2), sq(15.5, 3.5, 1.8, 1.8)] if S.name == "line" else
          [dot(8.5, 3, 1.1), dot(11.5, 2.5, 1.1), dot(14.25, 3, 1.1), dot(16.5, 4.5, 1.0)]),
        Part("dot", "M10.25 18.75L11.85 21.1A1.9 1.9 0 1 1 8.65 21.1Z" if S.name == "line" else
             "M10.25 18.75Q11.05 19.8 11.85 21.1A1.9 1.9 0 1 1 8.65 21.1Q9.45 19.8 10.25 18.75Z"),
    ]


@icon("blood-spot-card", CAT, "Paper screening card with two empty printed circles and two circles filled with blood",
      tags=["dried blood spot", "newborn screening", "filter paper", "sample card", "lab test", "finger prick", "specimen"],
      aliases=["dried-blood-spot-card"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, L(S, 1.5, 3.5))),
        detail(circle(8, 8.5, 3)),
        detail(circle(16, 8.5, 3)),
        dot(8, 15.5, 2.75),
        dot(16, 15.5, 2.75),
    ]


@icon("heart-valve", CAT, "Mechanical heart valve ring holding two half disc leaflets hinged open in the middle",
      tags=["valve replacement", "cardiac surgery", "prosthesis", "heart implant", "cardiology", "bileaflet", "implant"],
      aliases=["prosthetic-heart-valve"])
def _(S):
    return [
        shell(circle(12, 12, 9.5)) if S.name == "rounded" else shell(poly(regular(12, 12, 9.75, 12, start=15), closed=True)),
        detail("M10 8.5A3.5 3.5 0 0 0 10 15.5Z"),
        detail("M14 8.5A3.5 3.5 0 0 1 14 15.5Z"),
    ]


@icon("intraocular-lens", CAT, "Small round replacement eye lens with two thin curved spring arms on opposite sides",
      tags=["iol", "cataract surgery", "eye implant", "lens implant", "ophthalmology", "haptics", "vision"],
      aliases=["iol-lens"])
def _(S):
    return [
        shell(circle(12, 12, 5.25)),
        line("M16.6 9.6C20 9 21.5 6 19 3.5"),
        line("M7.4 14.4C4 15 2.5 18 5 20.5"),
    ]


@icon("spinal-fusion", CAT, "Two stacked vertebrae joined by a vertical rod held in place with two screws",
      tags=["spine surgery", "back surgery", "orthopedic implant", "rod and screws", "vertebrae", "fixation", "neurosurgery"],
      aliases=["spine-fixation"])
def _(S):
    return [
        shell(rect(8, 3.5, 8, 6.5, L(S, 1, 3))),
        shell(rect(8, 14, 8, 6.5, L(S, 1, 3))),
        line(seg(8, 6.75, 3.5, 6.75)),
        line(seg(8, 17.25, 3.5, 17.25)),
        line(seg(20.5, 3, 20.5, 21)),
        line(seg(11.5, 6.75, 20.5, 6.75)),
        line(seg(11.5, 17.25, 20.5, 17.25)),
    ]


@icon("laryngeal-mask-airway", CAT, "Airway tube ending in an oval inflatable cuffed mask with an open centre",
      tags=["lma", "supraglottic airway", "anesthesia", "airway device", "intubation", "breathing tube", "theatre"],
      aliases=["lma"])
def _(S):
    mask = ("M12 10.5C6.5 10.5 3.5 14 4.5 17.5C5.5 20.5 10 21.5 12 20C14 21.5 18.5 20.5 19.5 17.5"
            "C20.5 14 17.5 10.5 12 10.5Z")
    return [
        line("M20.5 3.5H16C13.5 3.5 12 5 12 7.5V10.5"),
        shell(mask),
        detail(ellipse(12, 16, 3.25, 1.75)),
    ]


@icon("sock-aid", CAT, "Curved plastic sock aid trough with a sock stretched over it and two long pull cords",
      tags=["dressing aid", "putting on socks", "mobility aid", "arthritis", "occupational therapy", "elderly", "assistive"],
      aliases=["stocking-aid"])
def _(S):
    return [
        shell("M6 9.5H14V13C14 15.5 16 17 19.5 17V21H13C8.5 21 6 18 6 14Z"),
        line(seg(8, 9.5, 8, 4.5)),
        line(seg(12.5, 9.5, 12.5, 4.5)),
        dot(8, 3.25, 1.3), dot(12.5, 3.25, 1.3),
    ]


@icon("two-handled-cup", CAT, "Training cup with a spouted lid and a handle on each side",
      tags=["sippy cup", "toddler cup", "drinking aid", "grip cup", "spout cup", "baby", "assistive"],
      aliases=["sippy-cup-handles"])
def _(S):
    return [
        shell(poly([(6.5, 9.5), (17.5, 9.5), (16.5, 21), (7.5, 21)], closed=True, r=S.r * 0.8)),
        shell(rect(5.5, 6.25, 13, 3.25, L(S, 0.5, 1.5))),
        shell(poly([(10, 6.25), (10.75, 3), (13.25, 3), (14, 6.25)], closed=True, r=S.r * 0.4)),
        line("M6.75 12H3.5V16.5H7.25"),
        line("M17.25 12H20.5V16.5H16.75"),
    ]


@icon("biohazard", CAT, "Biohazard warning symbol made of three open crescent rings around a small centre ring",
      tags=["biological hazard", "infection risk", "contamination", "warning", "lab safety", "infectious", "hazmat"],
      aliases=["biological-hazard"])
def _(S):
    parts = []
    for a in (-90, 30, 150):
        cx, cy = polar(12, 12, 4.75, a)
        parts.append(line(arc(cx, cy, 4, a + 230, a + 130 + 360)))
    parts.append(line(circle(12, 12, 1.5)))
    return parts


@icon("wheelchair-ramp", CAT, "Sloped ramp up to a raised landing with a handrail running alongside",
      tags=["accessible entrance", "access ramp", "disability", "step free", "mobility", "building access", "ada"],
      aliases=["access-ramp"])
def _(S):
    return [
        shell(poly([(4.5, 20.5), (14.5, 12.5), (21, 12.5), (21, 20.5)], closed=True, r=S.r * 0.4)),
        line(poly([(5, 13), (14.5, 6.5), (21, 6.5)], r=S.r * 0.5)),
        line(seg(5, 13, 5, 17.5)),
        line(seg(14.5, 6.5, 14.5, 12)),
    ]


@icon("pedal-exerciser", CAT, "Small pedal exerciser on the floor with two pedals on a central crank",
      tags=["mini bike", "leg exerciser", "physiotherapy", "seated cycling", "rehabilitation", "elderly", "under desk bike"],
      aliases=["mini-exercise-bike"])
def _(S):
    return [
        line(seg(2.5, 21.5, 21.5, 21.5)),
        line(seg(12, 12, 12, 21.5)),
        line(seg(6.5, 17, 17.5, 7)),
        shell(rect(2.5, 16.5, 7, 3.5, L(S, 0.5, 1.5))),
        shell(rect(14.5, 4, 7, 3.5, L(S, 0.5, 1.5))),
        shell(circle(12, 12, 2)),
    ]


@icon("shoulder-pulley", CAT, "Rope running over a pulley hung on a door top with a handle at each end",
      tags=["shoulder exercise", "physiotherapy", "rotator cuff", "range of motion", "rehab", "door pulley", "stretching"],
      aliases=["door-pulley"])
def _(S):
    return [
        line(seg(3, 3, 21, 3)),
        line(seg(12, 3, 12, 5.25)),
        shell(circle(12, 8.25, 3)),
        line(seg(9, 8.25, 9, 17)),
        line(seg(15, 8.25, 15, 14.5)),
        shell(rect(6, 17, 6, 3, L(S, 0.5, 1.5))),
        shell(rect(12, 14.5, 6, 3, L(S, 0.5, 1.5))),
    ]


@icon("rehab-stairs", CAT, "Short training staircase that steps up and down with handrails above it",
      tags=["physiotherapy", "gait training", "step practice", "rehabilitation", "parallel bars", "mobility", "balance"],
      aliases=["training-steps"])
def _(S):
    return [
        shell(poly([(2.5, 21.5), (2.5, 17.5), (7, 17.5), (7, 13.5), (17, 13.5), (17, 17.5), (21.5, 17.5), (21.5, 21.5)],
                   closed=True, r=S.r * 0.5)),
        line(poly([(3, 12), (7, 7.5), (17, 7.5), (21, 12)], r=S.r * 0.6)),
        line(seg(7, 7.5, 7, 12.5)),
        line(seg(17, 7.5, 17, 12.5)),
    ]


@icon("cheek-retractor", CAT, "Dental cheek retractor, an oval frame that holds the lips apart around two rows of teeth",
      tags=["lip retractor", "dentistry", "dental photography", "orthodontics", "mouth opener", "teeth", "dentist"],
      aliases=["lip-retractor"])
def _(S):
    parts = [shell(rect(2.5, 4.5, 19, 15, L(S, 2, 7.5)))]
    for i in range(4):
        x = 6.1 + i * 3.1
        parts.append(sq(x, 8.5, 2.5, 3.25, L(S, 0, 0.8)))
        parts.append(sq(x, 12.25, 2.5, 3.25, L(S, 0, 0.8)))
    return parts


@icon("ambulance-motorcycle", CAT, "Motorbike seen from the side with a plus marked box on the back and a roof light",
      tags=["paramedic bike", "emergency", "first responder", "rapid response", "medic", "rescue", "motorcycle ambulance"],
      aliases=["medic-motorbike"])
def _(S):
    return [
        shell(circle(6, 18.5, 3)),
        shell(circle(19, 18.5, 3)),
        line(poly([(6, 18.5), (9.5, 14.5), (15, 14.5), (19, 18.5)], r=S.r)),
        line(poly([(15, 14.5), (16.5, 9), (20, 9)], r=S.r)),
        shell(rect(2.5, 7, 9, 7, L(S, 1, 2))),
        *plus(7, 10.5, 1.75),
        line(seg(4.5, 3.5, 9.5, 3.5)),
    ]


@icon("automatic-pill-dispenser", CAT, "Round pill dispenser with a ring of small medicine cups around a centre dial",
      tags=["pill organizer", "medication reminder", "smart dispenser", "dosage", "elderly care", "carousel", "adherence"],
      aliases=["smart-pill-dispenser"])
def _(S):
    parts = [shell(circle(12, 12, 9.5) if S.name == "rounded" else poly(regular(12, 12, 10.25, 8, start=22.5), closed=True))]
    for i in range(6):
        x, y = polar(12, 12, 5.75, -90 + i * 60)
        parts.append(dot(x, y, 1.5))
    parts.append(dot(12, 12, 1.5))
    return parts


@icon("exam-stool", CAT, "Round padded rolling stool on a single lift post with a wheeled base",
      tags=["doctor stool", "clinic seat", "rolling stool", "adjustable stool", "gas lift", "swivel", "exam room"],
      aliases=["rolling-exam-stool"])
def _(S):
    return [
        shell(rect(3.5, 3.5, 17, 5.5, L(S, 1.5, 2.75))),
        line(seg(12, 9, 12, 16)),
        line(poly([(4.5, 19), (12, 16), (19.5, 19)], r=S.r * 0.5)),
        line(seg(12, 16, 12, 19.5)),
        dot(4.5, 20.5, 1.5), dot(12, 21, 1.5), dot(19.5, 20.5, 1.5),
    ]


@icon("vacuum-extractor", CAT, "Obstetric vacuum cup on a short stem with a cross handle and a pump hose",
      tags=["ventouse", "childbirth", "assisted delivery", "obstetrics", "labour", "labor", "midwife"],
      aliases=["ventouse"])
def _(S):
    return [
        line(seg(8, 3.5, 16, 3.5)),
        line(seg(12, 3.5, 12, 9.5)),
        shell("M4 19C4 12.5 8 9.5 12 9.5C16 9.5 20 12.5 20 19Z"),
        line("M18 15C21.5 14 21.5 9 20.5 6"),
    ]


@icon("ear-syringe", CAT, "Large ear irrigation syringe with a blunt nozzle, two side finger rings and a thumb ring",
      tags=["ear wash", "earwax", "ear irrigation", "ent", "cleaning", "nurse", "wax removal"],
      aliases=["ear-irrigator"])
def _(S):
    def ring(cx, cy, r=2.25):
        return poly(regular(cx, cy, r + 0.35, 8, start=22.5), closed=True) if S.name == "line" else circle(cx, cy, r)
    return [
        line(seg(12, 2.5, 12, 5.5)),
        shell(rect(8, 5.5, 8, 10.5, L(S, 1, 2.5))),
        line(seg(8, 8.5, 6.5, 8.5)),
        line(seg(16, 8.5, 17.5, 8.5)),
        shell(ring(4.5, 8.5, 2)),
        shell(ring(19.5, 8.5, 2)),
        line(seg(12, 16, 12, 18)),
        shell(ring(12, 19.75, 2)),
    ]


@icon("oxygen-tent", CAT, "Clear plastic canopy over the head end of a bed, fed by a hose from an oxygen tank",
      tags=["oxygen therapy", "canopy", "respiratory care", "hospital bed", "breathing support", "pediatric ward", "tank"])
def _(S):
    return [
        shell(rect(2.5, 16, 19, 3.5, L(S, 0.5, 1.75))),
        line("M3.5 16C3.5 9 6.5 5.5 10.5 5.5C14 5.5 15.5 9 15.5 16"),
        line("M13.5 7.5C17 7.5 18 9 18 11"),
        shell(rect(16, 11, 4.5, 5, L(S, 0.5, 1.5))),
    ]


@icon("emesis-bag", CAT, "Tall plastic bag hanging from a round rigid ring opening with volume marks inside",
      tags=["vomit bag", "sick bag", "nausea", "motion sickness", "airsickness", "barf bag", "hospital"],
      aliases=["vomit-bag"])
def _(S):
    return [
        shell(ellipse(12, 5, 6.5, 2.25)),
        shell("M5.5 5C5.5 12 7 21 12 21C17 21 18.5 12 18.5 5"),
        detail(seg(12.5, 11.5, 16, 11.5)),
        detail(seg(11.5, 16, 15, 16)),
    ]


@icon("post-op-shoe", CAT, "Flat rigid sole open toe post operative shoe seen from the side with a heel cup and two wide straps",
      tags=["surgical shoe", "foot surgery", "bunion", "healing", "orthopedic shoe", "walking boot", "recovery"],
      aliases=["surgical-shoe"])
def _(S):
    return [
        shell(rect(2.5, 16.5, 19, 4.5, L(S, 1, 2.25))),
        line("M4.5 16.5V8.5H8.5"),
        line("M10 16.5C10 6.5 15.25 6.5 15.25 16.5"),
        line("M16.25 16.5C16.25 9.5 20.5 9.5 20.5 16.5"),
    ]
