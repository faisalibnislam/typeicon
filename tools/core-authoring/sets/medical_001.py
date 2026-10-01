"""TypeIcon Core: medical equipment (batch medical_001).

Examination instruments, diagnostic and imaging equipment, respiratory aids and implants, drawn from the
objects themselves. No red-cross emblem. Handheld instruments stand upright or lean on one diagonal.
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


def pulse(x0, x1, y, amp=2.5):
    """Heartbeat trace from x0 to x1 around baseline y (points for poly)."""
    w = x1 - x0
    return [(x0, y), (x0 + w * 0.3, y), (x0 + w * 0.42, y - amp), (x0 + w * 0.58, y + amp), (x0 + w * 0.7, y), (x1, y)]


HEART = "M12 20L4.4 12.6A4.6 4.6 0 0 1 11 6.3L12 7.3L13 6.3A4.6 4.6 0 0 1 19.6 12.6Z"
HEART_R = ("M10.6 18.6L4.4 12.6A4.6 4.6 0 0 1 11 6.3L11.3 6.6Q12 7.3 12.7 6.6L13 6.3A4.6 4.6 0 0 1 19.6 12.6"
           "L13.4 18.6Q12 20 10.6 18.6Z")


def small_heart(S, cx, cy, k):
    """Heart scaled by k with the centre of its box at (cx, cy)."""
    return xf(L(S, HEART, HEART_R), (k, 0, 0, k, cx - 12 * k, cy - 13 * k))


# ============================================================================ examination instruments

@icon("otoscope", CAT, "Otoscope with a grip handle and a cone-shaped ear tip",
      tags=["ear exam", "auriscope", "ear", "doctor", "checkup", "ent"], aliases=["auriscope"])
def _(S):
    m = axis((9, 10), -35)
    cone = mpoly(m, [(1, -3.25), (11, -1.25), (11, 1.25), (1, 3.25)], closed=True, r=S.r * 0.4)
    head = circle(9, 10, 4.25)
    handle = rect(6.5, 12.5, 5, 9, L(S, 1, 2.5))
    return [
        shell(union(head, cone, handle)),
        detail(circle(9, 10, 1.25)) if S.name == "rounded" else sq(7.75, 8.75, 2.5, 2.5),
        detail(seg(6.5, 17, 11.5, 17)),
    ]


@icon("ophthalmoscope", CAT, "Ophthalmoscope with a slim handle and a flat head with a viewing hole",
      tags=["eye exam", "fundoscope", "eye", "optometry", "retina", "doctor"], aliases=["fundoscope"])
def _(S):
    head = rect(6.5, 2.5, 11, 10, L(S, 2, 4.5))
    handle = rect(9.5, 11, 5, 10.5, L(S, 1, 2.5))
    return [
        shell(union(head, handle)),
        detail(circle(12, 7.5, 1.75)),
        detail(seg(9.5, 15.5, 14.5, 15.5)),
    ]


@icon("reflex-hammer", CAT, "Reflex hammer with a triangular rubber head on a thin handle",
      tags=["knee reflex", "neurology", "percussion hammer", "reflex test", "doctor", "exam"],
      aliases=["percussion-hammer"])
def _(S):
    head = rot(poly([(4.5, 7), (19, 4), (19, 10)], closed=True, r=L(S, 0.8, 2)), 45)
    return [
        shell(head),
        line(rot(seg(14, 10, 14, 20.5), 45)),
    ]


@icon("tuning-fork", CAT, "Tuning fork with two long prongs and a short stem",
      tags=["hearing test", "vibration", "neurology", "rinne", "weber", "sound"])
def _(S):
    return [
        line(poly([(7.5, 2.5), (7.5, 13), (16.5, 13), (16.5, 2.5)], r=L(S, 2.5, 4.5))),
        line(seg(12, 13, 12, 18)),
        shell(circle(12, 20, 1.75)),
    ]


@icon("penlight", CAT, "Medical penlight with a pocket clip shining light from its tip",
      tags=["pen torch", "pupil check", "flashlight", "torch", "light", "exam"], aliases=["pen-torch"])
def _(S):
    m = axis((10.5, 13.5), -45)
    return [
        shell(stadium(m, -9, 4, 2.25, L(S, 1, 2.25))),
        detail(mseg(m, 1.5, -2.25, 1.5, 2.25)),
        line(mpoly(m, [(-7, -2.25), (-7, -4.75), (-2.5, -4.75)], r=S.r * 0.5)),
        line(mseg(m, 7, 0, 9.5, 0)),
        line(mseg(m, 6.25, -3.5, 8.25, -5.25)),
        line(mseg(m, 6.25, 3.5, 8.25, 5.25)),
    ]


def _band_arc(cx, cy, rx, ry, mx, my, mr):
    """Split an ellipse (cx, cy, rx, ry) into the arc outside a circle (mx, my, mr): returns a d-string."""
    ts = []
    n = 720
    inside = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = cx + rx * math.cos(t), cy + ry * math.sin(t)
        inside.append(math.hypot(x - mx, y - my) < mr)
    for i in range(n):
        if inside[i - 1] and not inside[i]:
            ts.append(("out", 2 * math.pi * i / n))
        if not inside[i - 1] and inside[i]:
            ts.append(("in", 2 * math.pi * i / n))
    t0 = [t for k, t in ts if k == "out"][0]
    t1 = [t for k, t in ts if k == "in"][0]
    x0, y0 = cx + rx * math.cos(t0), cy + ry * math.sin(t0)
    x1, y1 = cx + rx * math.cos(t1), cy + ry * math.sin(t1)
    span = (t1 - t0) % (2 * math.pi)
    large = 1 if span > math.pi else 0
    return f"M{fmt(x0)} {fmt(y0)}A{fmt(rx)} {fmt(ry)} 0 {large} 1 {fmt(x1)} {fmt(y1)}"


@icon("head-mirror", CAT, "Doctor's head mirror with a centre hole on a headband",
      tags=["ent", "doctor", "mirror", "headband", "ear nose throat", "exam"], aliases=["forehead-mirror"])
def _(S):
    return [
        line(_band_arc(12, 15, 9.5, 5.5, 12, 8.5, 7.5)),
        shell(circle(12, 8.5, 5.75)),
        detail(circle(12, 8.5, 1.5)) if S.name == "rounded" else sq(10.5, 7, 3, 3),
    ]


@icon("pulse-oximeter", CAT, "Fingertip pulse oximeter clip on a finger showing a pulse wave",
      tags=["oximeter", "spo2", "oxygen saturation", "finger clip", "pulse", "vital signs"], aliases=["oximeter"])
def _(S):
    return [
        line("M9 6.5V5A3 3 0 0 1 15 5V6.5"),
        shell(rect(3.5, 6.5, 17, 10, S.R)),
        detail(poly(pulse(6.5, 17.5, 11.5), r=S.r * 0.4)),
        line(seg(9, 16.5, 9, 21.5)), line(seg(15, 16.5, 15, 21.5)),
    ]


@icon("lancing-device", CAT, "Pen-shaped lancing device with a blood drop at its tip",
      tags=["lancet", "finger prick", "blood sugar", "glucose test", "diabetes", "blood sample"],
      aliases=["lancet-pen"])
def _(S):
    m = axis((12.5, 11.5), 135)
    body = [(-9.5, -2.75), (2.5, -2.75), (5.5, -1.5), (5.5, 1.5), (2.5, 2.75), (-9.5, 2.75)]
    return [
        shell(mpoly(m, body, closed=True, r=S.r * 0.6)),
        detail(mseg(m, 2.5, -2.75, 2.5, 2.75)),
        line(mseg(m, -9.5, 0, -11.5, 0)),
        shell(drop(4.5, 19.5, 2, S)),
    ]


@icon("urine-dipstick", CAT, "Urine test strip with a row of square reagent pads",
      tags=["urinalysis", "test strip", "urine test", "reagent strip", "lab test", "dipstick"],
      aliases=["urine-test-strip"])
def _(S):
    out = [shell(rect(8, 2.5, 8, 19, L(S, 1, 3)))]
    for y in (9, 12.75, 16.5):
        out.append(sq(10, y, 4, 2, L(S, 0, 0.75)))
    return out


@icon("peak-flow-meter", CAT, "Peak flow meter tube with a mouthpiece and a slider on its scale",
      tags=["asthma", "lung function", "breathing test", "pef", "respiratory", "airflow"])
def _(S):
    body = union(rect(7, 8.5, 14.5, 8, min(S.R, 2.5)), rect(2.5, 10.5, 5.5, 4, L(S, 0.5, 1.5)))
    return [
        shell(body),
        detail(seg(10.5, 8.5, 10.5, 11.5)), detail(seg(14, 8.5, 14, 11.5)), detail(seg(17.5, 8.5, 17.5, 11.5)),
        solid(poly([(12.5, 3.5), (15.5, 3.5), (14, 6)], closed=True, r=L(S, 0, 0.4))),
    ]


@icon("spirometer", CAT, "Handheld spirometer with a screen and a sideways mouthpiece tube",
      tags=["lung function", "breathing test", "pulmonary", "respiratory", "fev1", "copd"])
def _(S):
    body = union(rect(3, 4, 10, 17.5, S.R), rect(11, 7, 10.5, 5.5, min(S.R, 1.5)))
    return [
        shell(body),
        detail(rect(5.5, 7, 5, 5, min(S.R, 1))),
        detail(seg(17.5, 7, 17.5, 12.5)),
        dot(8, 16.5, 1.4),
    ]


@icon("incentive-spirometer", CAT, "Incentive spirometer cylinder with a piston and a hose to a mouthpiece",
      tags=["breathing exercise", "lung exercise", "post-surgery", "respiratory therapy", "deep breathing", "recovery"])
def _(S):
    return [
        shell(rect(3, 3.5, 9, 17, min(S.R, 2.5))),
        sq(5, 10.5, 5, 2.5, L(S, 0, 0.75)),
        detail(seg(7.5, 13, 7.5, 17)),
        line(poly([(12, 17.5), (17.5, 17.5), (17.5, 8.5)], r=L(S, 0, 3))),
        shell(rect(15.5, 3, 4, 5.5, L(S, 0.5, 1.5))),
    ]


@icon("holter-monitor", CAT, "Holter monitor box with three wires to round electrode pads",
      tags=["ecg recorder", "heart monitor", "24 hour ecg", "ambulatory ecg", "cardiology", "arrhythmia"],
      aliases=["holter"])
def _(S):
    return [
        shell(rect(6, 2.5, 12, 8, S.R)),
        detail(seg(9, 6.5, 15, 6.5)),
        line(poly([(8.5, 10.5), (8.5, 12.5), (5, 15)], r=S.r)),
        line(seg(12, 10.5, 12, 15.5)),
        line(poly([(15.5, 10.5), (15.5, 12.5), (19, 15)], r=S.r)),
        shell(circle(4.5, 18.5, 2.5)), shell(circle(12, 19, 2.5)), shell(circle(19.5, 18.5, 2.5)),
    ]


def _scallop(cx, cy, r, n, bump):
    pts = [polar(cx, cy, r, -90 + i * 360 / n) for i in range(n)]
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(n):
        x, y = pts[(i + 1) % n]
        d += f"A{fmt(bump)} {fmt(bump)} 0 0 1 {fmt(x)} {fmt(y)}"
    return d + "Z"


@icon("ecg-electrode", CAT, "Round ECG electrode pad with a scalloped edge and a snap stud",
      tags=["ekg electrode", "electrode pad", "sensor", "heart monitor", "adhesive pad", "cardiology"],
      aliases=["ekg-electrode"])
def _(S):
    return [
        shell(_scallop(12, 12, 8.25, 12, 2.6)),
        detail(circle(12, 12, 4)),
        dot(12, 12, 1.5) if S.name == "rounded" else sq(10.5, 10.5, 3, 3),
    ]


@icon("defibrillator-pads", CAT, "Two defibrillator pads with wires joined to one plug",
      tags=["aed pads", "electrode pads", "shock pads", "cardiac arrest", "resuscitation", "emergency"],
      aliases=["aed-pads"])
def _(S):
    out = []
    for x in (2.5, 13.5):
        out.append(shell(rect(x, 2.5, 8, 10, min(S.R, 2.5))))
        cx = x + 4
        out.append(detail(poly([(cx + 0.75, 4.75), (cx - 1.25, 7.75), (cx + 1.25, 7.25), (cx - 0.75, 10.25)], r=S.r * 0.2)))
    out += [
        line(poly([(6.5, 12.5), (6.5, 15.5), (10.5, 15.5), (10.5, 17)], r=S.r)),
        line(poly([(17.5, 12.5), (17.5, 15.5), (13.5, 15.5), (13.5, 17)], r=S.r)),
        shell(rect(9, 17, 6, 4.5, min(S.R, 1.5))),
    ]
    return out


@icon("ear-thermometer", CAT, "Ear thermometer with a short cone probe and a small screen",
      tags=["tympanic thermometer", "temperature", "fever", "ear", "infrared thermometer", "child"],
      aliases=["tympanic-thermometer"])
def _(S):
    m = axis((12, 9.5), -125)
    probe = mpoly(m, [(0, -3), (7, -1.75), (7, 1.75), (0, 3)], closed=True, r=S.r * 0.4)
    body = rect(9.5, 8, 9.5, 13.5, S.R)
    return [
        shell(union(body, probe)),
        detail(mseg(m, 5, -2.1, 5, 2.1)),
        detail(rect(12, 11.5, 4.5, 3.5, min(S.R, 1))),
        dot(14.25, 18, 1.25),
    ]


@icon("fetal-doppler", CAT, "Fetal doppler unit showing a heart, with a cable to a round probe",
      tags=["pregnancy", "baby heartbeat", "prenatal", "obstetrics", "ultrasound", "midwife"],
      aliases=["baby-heartbeat-monitor"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 11.5, 12, S.R)),
        Part("dot", small_heart(S, 8.25, 8.5, 0.5)),
        line(poly([(14, 8.5), (17, 8.5), (17, 16)], r=L(S, 0, 2.5))),
        shell(L(S, "M12.5 21.5A4.5 5 0 0 1 21.5 21.5Z", "M13.5 21.5A1 1 0 0 1 12.5 20.5A4.5 4.5 0 0 1 21.5 20.5A1 1 0 0 1 20.5 21.5Z")),
    ]


@icon("pinard-horn", CAT, "Pinard horn: a trumpet-shaped fetal stethoscope with an earpiece disc",
      tags=["fetal stethoscope", "midwife", "pregnancy", "prenatal", "obstetrics", "listening"],
      aliases=["pinard-stethoscope"])
def _(S):
    horn = "M10.5 6V11C10.5 15 8 18 5 21H19C16 18 13.5 15 13.5 11V6Z"
    if S.name == "rounded":
        horn = "M10.5 6V11C10.5 15 8 18 5.8 20.2Q5 21 6.2 21H17.8Q19 21 18.2 20.2C16 18 13.5 15 13.5 11V6Z"
    return [
        shell(union(horn, rect(6, 2.5, 12, 3.5, L(S, 0.5, 1.75)))),
        detail(seg(10.5, 6, 13.5, 6)),
    ]


@icon("dermatoscope", CAT, "Dermatoscope with a round magnifying lens ringed by small lights",
      tags=["skin exam", "dermatology", "mole check", "dermoscopy", "magnifier", "skin cancer"],
      aliases=["dermoscope"])
def _(S):
    out = [shell(union(circle(12, 9, 7), rect(9.5, 14, 5, 7.5, L(S, 1, 2.5)))), detail(circle(12, 9, 2))]
    for i in range(8):
        out.append(dot(*polar(12, 9, 4.6, i * 45), 0.7))
    return out


@icon("laryngoscope", CAT, "Laryngoscope with a straight handle and a curved blade",
      tags=["intubation", "airway", "anesthesia", "anaesthesia", "emergency", "throat"])
def _(S):
    blade = L(S, "M8 3H15C18.5 3 21 6 21.5 10.5H18.5C18 7.8 16.5 6.5 14.5 6.5H8Z",
              "M8 3H15C18.5 3 21 6 21.5 9.5Q21.6 10.5 20.6 10.5H19.4Q18.6 10.5 18.4 9.8C17.8 7.6 16.4 6.5 14.5 6.5H8Z")
    handle = rect(3.5, 3, 5.5, 18.5, L(S, 1, 2.75))
    return [
        shell(union(handle, blade)),
        detail(seg(3.5, 10, 9, 10)), detail(seg(3.5, 14, 9, 14)),
    ]


@icon("audiometer", CAT, "Hearing test headphones with a hand response button on a cord",
      tags=["hearing test", "audiology", "audiogram", "hearing screening", "ear", "headphones"],
      aliases=["hearing-test"])
def _(S):
    return [
        line("M3.5 12.5V10.5A7.5 7.5 0 0 1 18.5 10.5V12.5"),
        shell(rect(2.5, 11.5, 4, 6.5, min(S.R, 1.5))),
        shell(rect(15.5, 11.5, 4, 6.5, min(S.R, 1.5))),
        line(poly([(4.5, 18), (4.5, 20.5), (11, 20.5)], r=L(S, 0, 2))),
        shell(rect(11, 18.5, 10.5, 4, L(S, 1, 2))),
        dot(18.5, 20.5, 1),
    ]


@icon("stadiometer", CAT, "Height measuring rod with tick marks and a headpiece resting on a person",
      tags=["height measurement", "height rod", "measure height", "growth", "pediatrics", "clinic"],
      aliases=["height-rod"])
def _(S):
    return [
        shell(rect(15.5, 2.5, 3.5, 19, min(S.R, 1))),
        line(seg(19, 6, 21.5, 6)), line(seg(19, 10, 21.5, 10)), line(seg(19, 14, 21.5, 14)),
        line(seg(3.5, 5.5, 15.5, 5.5)),
        shell(circle(9, 10, 2.25)),
        shell(L(S, "M4.5 21.5V17.5A4.5 4.5 0 0 1 13.5 17.5V21.5Z",
                "M5.5 21.5A1 1 0 0 1 4.5 20.5V17.5A4.5 4.5 0 0 1 13.5 17.5V20.5A1 1 0 0 1 12.5 21.5Z")),
    ]


@icon("hand-dynamometer", CAT, "Hand grip dynamometer with a round dial gauge above a D-shaped grip",
      tags=["grip strength", "hand strength", "physiotherapy", "rehab", "occupational therapy", "force gauge"],
      aliases=["grip-dynamometer"])
def _(S):
    return [
        shell(circle(12, 7.5, 5.5)),
        detail(seg(12, 7.5, 14.5, 5)), dot(12, 7.5, 1.25),
        line(poly([(8.5, 11.5), (5, 21), (19, 21), (15.5, 11.5)], r=S.r)),
        line(seg(8, 16.5, 16, 16.5)),
    ]


@icon("goniometer", CAT, "Goniometer: a round protractor disc with two long hinged arms",
      tags=["joint angle", "range of motion", "physiotherapy", "angle measure", "rehab", "orthopedics"])
def _(S):
    m = axis((7, 15), -42)
    return [
        shell(circle(7, 15, 4.5)),
        dot(7, 15, 1.4),
        line(seg(11.5, 15, 21.5, 15)),
        line(mseg(m, 4.5, 0, 15, 0)),
        detail(seg(2.5, 15, 4.25, 15)) if S.name == "line" else detail(seg(7, 10.5, 7, 12.25)),
    ]


@icon("neuro-pinwheel", CAT, "Neurological pinwheel with a spiked wheel on a pen handle",
      tags=["wartenberg wheel", "sensation test", "neurology", "nerve test", "pinwheel", "exam"],
      aliases=["wartenberg-wheel"])
def _(S):
    pts = []
    for i in range(20):
        pts.append(polar(15.5, 8.5, 6 if i % 2 == 0 else 3.75, -90 + i * 18))
    m = axis((3.5, 20.5), -45)
    return [
        shell(poly(pts, closed=True, r=L(S, 0, 0.3)), stroke_miterlimit="2"),
        dot(15.5, 8.5, 1.25),
        shell(stadium(m, 0, 10, 2, L(S, 1, 2))),
        line(mseg(m, 10, 0, 13, 0)),
    ]


@icon("baby-scale", CAT, "Infant weighing scale with a curved cradle tray on a low base",
      tags=["infant scale", "baby weight", "newborn", "pediatrics", "weighing", "clinic"],
      aliases=["infant-scale"])
def _(S):
    tray = L(S, "M2.5 9H21.5C21 11.8 18.5 13.5 15 13.5H9C5.5 13.5 3 11.8 2.5 9Z",
             "M3.5 9H20.5Q21.6 9 21.3 10C20.6 12.2 18.2 13.5 15 13.5H9C5.8 13.5 3.4 12.2 2.7 10Q2.4 9 3.5 9Z")
    return [
        shell(circle(7.5, 5.25, 2.25)),
        line("M11 9A3.75 3 0 0 1 18.5 9"),
        shell(tray),
        line(seg(12, 13.5, 12, 16)),
        shell(rect(4, 16, 16, 5.5, S.R)),
        detail(seg(10, 18.75, 14, 18.75)),
    ]


@icon("pain-scale", CAT, "Pain scale: a happy face and a sad face above a graded bar",
      tags=["pain rating", "pain level", "faces scale", "pain assessment", "discomfort", "symptom"],
      aliases=["pain-rating"])
def _(S):
    return [
        shell(circle(6.5, 7.5, 4.5)), shell(circle(17.5, 7.5, 4.5)),
        detail("M4.75 8.25A1.9 1.9 0 0 0 8.25 8.25"),
        detail("M15.75 9.5A1.9 1.9 0 0 1 19.25 9.5"),
        dot(5.25, 5.9, 0.85), dot(7.75, 5.9, 0.85), dot(16.25, 5.9, 0.85), dot(18.75, 5.9, 0.85),
        shell(rect(2.5, 15.5, 19, 5.5, min(S.R, 2.75))),
        detail(seg(8.83, 15.5, 8.83, 21)), detail(seg(15.17, 15.5, 15.17, 21)),
    ]


@icon("growth-chart", CAT, "Growth chart with percentile curves fanning out and a plotted dot",
      tags=["percentile", "child growth", "pediatrics", "height weight chart", "development", "growth curve"],
      aliases=["percentile-chart"])
def _(S):
    return [
        line(poly([(3, 2.5), (3, 21), (21.5, 21)], r=S.r)),
        line("M7 17C11 15 15 10 20.5 4"),
        line("M7 17C12 16.5 16 14.5 20.5 11.5"),
        solid(circle(15.5, 16.75, 1.75)) if S.name == "rounded" else solid(rect(13.75, 15, 3.5, 3.5)),
    ]


@icon("breathalyzer", CAT, "Breathalyzer with a screen and a straight mouthpiece tube on top",
      tags=["alcohol test", "breath test", "bac", "drink driving", "sobriety", "police"],
      aliases=["breath-alcohol-tester"])
def _(S):
    return [
        shell(union(rect(6.5, 8.5, 11, 13, S.R), rect(10, 2.5, 4, 7, L(S, 0.5, 1.5)))),
        detail(rect(9, 11.5, 6, 4, min(S.R, 1))),
        dot(12, 18.5, 1.25),
    ]


# ============================================================================ scopes and eye tests

@icon("capsule-endoscope", CAT, "Pill camera: a capsule with a clear dome lens and a camera eye",
      tags=["pill camera", "capsule camera", "endoscopy", "gastroenterology", "digestive", "camera pill"],
      aliases=["pill-camera"])
def _(S):
    m = axis((10.5, 13.5), -45)
    return [
        shell(stadium(m, -8.5, 6.5, 4, L(S, 3, 4))),
        detail(mseg(m, 0.5, -4, 0.5, 4)),
        dot(*m(3.5, 0), 1.3),
        line(mseg(m, 9.5, 0, 11.5, 0)),
        line(mseg(m, 8.5, -3.5, 10.25, -5)),
        line(mseg(m, 8.5, 3.5, 10.25, 5)),
    ]


@icon("phoropter", CAT, "Phoropter: a wide eye test device with two round lens windows",
      tags=["refraction", "eye test", "optometry", "vision test", "optician", "lenses"],
      aliases=["refractor"])
def _(S):
    body = union(circle(6.75, 13, 4.75), circle(17.25, 13, 4.75), rect(6.75, 10, 10.5, 6, 0))
    return [
        shell(body),
        detail(circle(6.75, 13, 1.75)), detail(circle(17.25, 13, 1.75)),
        line(seg(12, 10, 12, 4.5)),
        shell(rect(7.5, 2.5, 9, 2.5, L(S, 0.5, 1.25))),
        dot(12, 13.5, 1.1),
    ]


@icon("sonogram", CAT, "Ultrasound printout with a fan-shaped scan showing a curled baby",
      tags=["ultrasound scan", "baby scan", "pregnancy", "prenatal", "sonography", "fetus"],
      aliases=["baby-scan"])
def _(S):
    ax, ay, r = 12, 5.5, 13
    p1, p2 = polar(ax, ay, r, 52), polar(ax, ay, r, 128)
    fan = f"M{fmt(ax)} {fmt(ay)}L{fmt(p1[0])} {fmt(p1[1])}A{r} {r} 0 0 1 {fmt(p2[0])} {fmt(p2[1])}Z"
    baby = "M10 12.5A2 2 0 1 1 13.5 11.5C15.5 12.5 16 15 14 16.5C12 17.5 9.5 16.5 9.5 14.5Z"
    return [
        shell(rect(2.5, 3, 19, 18, S.R)),
        detail(fan),
        Part("dot", baby),
    ]


@icon("lab-report", CAT, "Lab report sheet with a test tube and result rows, one flagged",
      tags=["lab results", "blood test results", "test results", "pathology", "medical report", "laboratory"],
      aliases=["lab-results"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, min(S.R, 2.5))),
        detail(L(S, "M7.5 5V8.5H10.5V5", "M7.5 5V8A1.5 1.5 0 0 0 10.5 8V5")),
        detail(seg(13, 6.75, 16.5, 6.75)),
        detail(seg(7.5, 12, 16.5, 12)),
        detail(seg(7.5, 15.5, 12.5, 15.5)), dot(16, 15.5, 1.25),
        detail(seg(7.5, 19, 16.5, 19)),
    ]


# ============================================================================ imaging

def _notch(d, cut, gap=7.5):
    """Region d with room cut out around the closed shape `cut` (gap = stroke-to-stroke width)."""
    return path_to_d(D(P(d), U(P(cut), ST(cut, gap))))


def _table(S, top, w0, w1):
    y0 = top
    return poly([(12 - w0, y0), (12 + w0, y0), (12 + w1, 21.5), (12 - w1, 21.5)], closed=True, r=S.r * 0.5)


@icon("mri-scanner", CAT, "MRI scanner: a large square housing with a round bore and a patient table",
      tags=["mri", "magnetic resonance", "scan", "radiology", "imaging", "hospital"],
      aliases=["mri"])
def _(S):
    table = _table(S, 15.75, 3, 5.5)
    return [
        shell(_notch(rect(2.5, 2.5, 19, 16.5, S.R), table)),
        detail(circle(12, 9, 4.25)),
        detail(seg(8.5, 10.5, 15.5, 10.5)),
        shell(table),
    ]


@icon("ct-scanner", CAT, "CT scanner: an upright ring gantry with a narrow table through the centre",
      tags=["ct scan", "cat scan", "computed tomography", "radiology", "imaging", "hospital"],
      aliases=["cat-scanner"])
def _(S):
    table = _table(S, 15.5, 3, 6)
    return [
        shell(_notch(circle(12, 10, 8), table)),
        detail(circle(12, 10, 3.5)),
        detail(seg(9, 11.5, 15, 11.5)),
        shell(table),
    ]


@icon("x-ray-machine", CAT, "X-ray machine: a tube head on a column arm above a patient table",
      tags=["radiography", "x-ray", "xray", "radiology", "imaging", "hospital"],
      aliases=["xray-machine"])
def _(S):
    head = union(rect(9.5, 2.5, 8, 4, L(S, 0.5, 1.5)), poly([(10.5, 6), (16.5, 6), (18, 9.5), (9, 9.5)], closed=True))
    return [
        line(poly([(4, 21.5), (4, 4.5), (9.5, 4.5)], r=S.r)),
        shell(head),
        detail(seg(11.5, 12, 11, 13.5)), detail(seg(16, 12, 16.5, 13.5)),
        shell(rect(7.5, 15.5, 14, 2.5, L(S, 0.5, 1.25))),
        line(seg(14.5, 18, 14.5, 21.5)),
    ]


@icon("c-arm", CAT, "C-arm X-ray unit: a large C-shaped arm on a wheeled base",
      tags=["fluoroscopy", "fluoroscope", "x-ray", "surgery imaging", "operating room", "radiology"],
      aliases=["fluoroscope"])
def _(S):
    return [
        line(arc(12, 9.5, 7, 60, 300)),
        shell(rect(12.5, 2, 7, 3, L(S, 0.5, 1.5))),
        shell(rect(13.5, 14.5, 5, 3.5, L(S, 0.5, 1.5))),
        line(seg(5.9, 13, 5, 18.5)),
        line(seg(2.5, 18.5, 11, 18.5)),
        dot(4, 21, 1.25), dot(9.5, 21, 1.25),
    ]


@icon("ultrasound-machine", CAT, "Ultrasound machine: a cart with a screen, a console and wheels",
      tags=["sonography", "ultrasound", "scanner", "imaging", "hospital", "echo"],
      aliases=["sonography-machine"])
def _(S):
    ax, ay, r = 12, 4.75, 4.25
    p1, p2 = polar(ax, ay, r, 55), polar(ax, ay, r, 125)
    fan = f"M{fmt(ax)} {fmt(ay)}L{fmt(p1[0])} {fmt(p1[1])}A{r} {r} 0 0 1 {fmt(p2[0])} {fmt(p2[1])}Z"
    return [
        shell(rect(4.5, 2.5, 15, 9, min(S.R, 2.5))),
        detail(fan),
        shell(poly([(3, 13.5), (21, 13.5), (19.5, 16.5), (4.5, 16.5)], closed=True, r=S.r * 0.5)),
        line(seg(12, 16.5, 12, 19)),
        line(seg(5, 19, 19, 19)),
        dot(6.5, 21.25, 1), dot(17.5, 21.25, 1),
    ]


@icon("ultrasound-probe", CAT, "Ultrasound probe with a curved face sending out sound waves",
      tags=["transducer", "sonography", "ultrasound", "scan", "probe", "imaging"],
      aliases=["ultrasound-transducer"])
def _(S):
    cy = 11 - math.sqrt(64 - 5.5 ** 2)
    body = L(S, "M10 4H14L17.5 11A8 8 0 0 1 6.5 11Z",
             "M10.6 4H13.4Q14 4 14.3 4.6L17.5 11A8 8 0 0 1 6.5 11L9.7 4.6Q10 4 10.6 4Z")
    return [
        shell(body),
        line(arc(12, cy, 12, 65, 115)),
        line(arc(12, cy, 16, 70, 110)),
        line("M12 4V2.5H17"),
    ]


def _trefoil(cx, cy, r0, r1, S=None):
    out = []
    for c in (-90, 30, 150):
        a0, a1 = c - 30, c + 30
        p0, p1 = polar(cx, cy, r1, a0), polar(cx, cy, r1, a1)
        q1, q0 = polar(cx, cy, r0, a1), polar(cx, cy, r0, a0)
        out.append(Part("dot", f"M{fmt(p0[0])} {fmt(p0[1])}A{fmt(r1)} {fmt(r1)} 0 0 1 {fmt(p1[0])} {fmt(p1[1])}"
                               f"L{fmt(q1[0])} {fmt(q1[1])}A{fmt(r0)} {fmt(r0)} 0 0 0 {fmt(q0[0])} {fmt(q0[1])}Z"))
    out.append(dot(cx, cy, 0.9))
    return out


@icon("lead-apron", CAT, "Lead X-ray apron with a radiation symbol on the chest",
      tags=["radiation protection", "x-ray apron", "lead vest", "radiology", "shielding", "safety"],
      aliases=["x-ray-apron"])
def _(S):
    apron = poly([(5.5, 3), (9, 3), (10, 6), (14, 6), (15, 3), (18.5, 3), (18.5, 8), (20, 10), (19, 21.5),
                  (5, 21.5), (4, 10), (5.5, 8)], closed=True, r=S.r * 0.6)
    return [shell(apron), *_trefoil(12, 14, 1.7, 4.25)]


@icon("dosimeter-badge", CAT, "Radiation dosimeter badge with a clip, a radiation symbol and a window",
      tags=["radiation badge", "film badge", "dosimetry", "radiation monitor", "radiology", "safety"],
      aliases=["film-badge"])
def _(S):
    return [
        line(poly([(10, 7), (10, 3), (14, 3), (14, 7)], r=S.r * 0.5)),
        shell(rect(2.5, 7, 19, 13, S.R)),
        *_trefoil(8.5, 13.5, 1.4, 3.6),
        detail(rect(14.5, 10.5, 3.5, 6, min(S.R, 1))),
    ]


# ============================================================================ breathing and airway

_MASK = "M9.5 4H14.5L18.5 12.5C19.2 15.5 16.5 17.5 12 17.5C7.5 17.5 4.8 15.5 5.5 12.5Z"
_MASK_R = "M10.2 4H13.8Q14.5 4 14.8 4.7L18.5 12.5C19.2 15.5 16.5 17.5 12 17.5C7.5 17.5 4.8 15.5 5.5 12.5L9.2 4.7Q9.5 4 10.2 4Z"


@icon("oxygen-mask", CAT, "Oxygen face mask over nose and mouth with a strap and a tube",
      tags=["oxygen", "o2 mask", "breathing", "respiratory", "ventilation", "hospital"],
      aliases=["o2-mask"])
def _(S):
    return [
        shell(L(S, _MASK, _MASK_R)),
        line(seg(7.2, 9, 2.5, 9)), line(seg(16.8, 9, 21.5, 9)),
        line(seg(12, 17.5, 12, 21.5)),
    ]


@icon("nebulizer", CAT, "Nebulizer: a compressor box with a tube to a mask and medicine cup",
      tags=["nebuliser", "asthma", "breathing treatment", "respiratory", "inhalation", "copd"],
      aliases=["nebuliser"])
def _(S):
    mask = "M14 2.5H18L21 9C21.3 11 19.5 12 16 12C12.5 12 10.7 11 11 9Z"
    return [
        shell(mask),
        shell(rect(14, 12, 4, 3.5, L(S, 0, 1))),
        line(poly([(16, 15.5), (16, 17.5), (11.5, 17.5)], r=S.r)),
        shell(rect(2.5, 14, 9, 7.5, S.R)),
        dot(7, 17.75, 1.25),
    ]


@icon("inhaler-spacer", CAT, "Inhaler spacer chamber with a mouthpiece and an inhaler fitted at the end",
      tags=["spacer", "holding chamber", "asthma", "inhaler", "valved holding chamber", "respiratory"],
      aliases=["spacer-device"])
def _(S):
    chamber = union(rect(6, 8, 11, 9, L(S, 2.5, 4.5)), rect(2.5, 10.5, 4.5, 4, L(S, 0.5, 1.25)))
    return [
        shell(chamber),
        shell(rect(17, 4, 4.5, 14, min(S.R, 1.5))),
        detail(seg(17, 8, 21.5, 8)),
    ]


@icon("nasal-cannula", CAT, "Nasal cannula: a tube loop with two short nose prongs",
      tags=["oxygen tube", "nasal prongs", "oxygen therapy", "o2", "breathing", "respiratory"],
      aliases=["oxygen-cannula"])
def _(S):
    return [
        shell(rect(7.5, 6.5, 9, 3, L(S, 0.5, 1.5))),
        line(seg(10, 6.5, 10, 3.5)), line(seg(14, 6.5, 14, 3.5)),
        line("M7.5 8C3.5 8 2.5 10.5 2.5 12.5C2.5 15.5 7 17.5 12 17.5C17 17.5 21.5 15.5 21.5 12.5C21.5 10.5 20.5 8 16.5 8"),
        line(seg(12, 17.5, 12, 21.5)),
    ]


@icon("oxygen-concentrator", CAT, "Home oxygen concentrator on wheels with a handle, a knob and tubing",
      tags=["oxygen machine", "o2 concentrator", "home oxygen", "copd", "respiratory", "breathing"],
      aliases=["o2-concentrator"])
def _(S):
    return [
        line(poly([(7.5, 5), (7.5, 2.5), (12.5, 2.5), (12.5, 5)], r=S.r * 0.6)),
        shell(rect(3, 5, 14, 14, S.R)),
        detail(seg(6.5, 9, 13.5, 9)),
        detail(seg(6.5, 12.5, 13.5, 12.5)),
        detail(seg(6.5, 16, 13.5, 16)),
        dot(6, 21, 1.25), dot(14, 21, 1.25),
        line("M17 9.5H18.5C20.5 9.5 21.5 11 21.5 13V21.5"),
    ]


@icon("oxygen-flowmeter", CAT, "Wall oxygen flowmeter: a clear tube with a floating ball, a knob and a nozzle",
      tags=["oxygen flow", "flow meter", "o2", "oxygen therapy", "rotameter", "hospital"],
      aliases=["o2-flowmeter"])
def _(S):
    body = union(rect(8.5, 5.5, 7, 11.5, min(S.R, 2.5)), rect(7, 2.5, 10, 3.5, L(S, 0.5, 1.5)),
                 poly([(10, 16.5), (14, 16.5), (13.25, 21.5), (10.75, 21.5)], closed=True, r=S.r * 0.3))
    return [
        shell(body),
        detail(seg(8.5, 6, 15.5, 6)),
        dot(12, 12.5, 1.5),
        line(seg(3, 11, 8.5, 11)),
    ]


@icon("suction-unit", CAT, "Medical suction unit: a gauge piped to a canister jar with a hanging tube",
      tags=["suction", "aspirator", "suction canister", "airway", "hospital", "vacuum regulator"],
      aliases=["aspirator"])
def _(S):
    return [
        shell(circle(6.5, 6.5, 4)),
        detail(seg(6.5, 6.5, 8.5, 4.5)),
        line(poly([(10.5, 6.5), (15, 6.5), (15, 9.5)], r=L(S, 0, 2))),
        shell(rect(10, 9.5, 11.5, 12, S.R)),
        detail(seg(10, 12.5, 21.5, 12.5)),
        line(poly([(10, 16), (5, 16), (5, 21.5)], r=L(S, 0, 2.5))),
    ]


@icon("bag-valve-mask", CAT, "Manual resuscitator: an oval squeeze bag joined through a valve to a face mask",
      tags=["resuscitator bag", "bvm", "resuscitation", "cpr", "ventilation", "emergency"],
      aliases=["manual-resuscitator"])
def _(S):
    mask = L(S, "M15.5 14H19.5L21.5 19.5C21.5 20.8 19.8 21.5 17.5 21.5C15.2 21.5 13.5 20.8 13.5 19.5Z",
             "M16 14H19Q19.6 14 19.8 14.6L21.5 19.5C21.5 20.8 19.8 21.5 17.5 21.5C15.2 21.5 13.5 20.8 13.5 19.5L15.2 14.6Q15.4 14 16 14Z")
    return [
        shell(ellipse(8, 8.5, 5.5, 4.5)),
        shell(rect(13.5, 7, 4, 3, L(S, 0, 1))),
        line(poly([(17.5, 8.5), (19.5, 8.5), (17.5, 8.5)])) if False else line(seg(17.5, 10, 17.5, 14)),
        shell(mask),
    ]


@icon("pocket-mask", CAT, "CPR pocket mask with a one-way valve port in the centre",
      tags=["cpr mask", "rescue breathing", "resuscitation", "first aid", "face shield", "emergency"],
      aliases=["cpr-mask"])
def _(S):
    tri = poly([(12, 3), (21, 20), (3, 20)], closed=True, r=L(S, 2.5, 4.5))
    return [
        shell(tri),
        detail(circle(12, 14, 3)),
        dot(12, 14, 1),
    ]


def _tube(d, w, S):
    return path_to_d(ST(d, w, L(S, "butt", "round"), "round"))


@icon("oropharyngeal-airway", CAT, "Oral airway: a curved plastic tube with a flat flange at the straight end",
      tags=["opa", "guedel airway", "airway adjunct", "first aid", "anesthesia", "emergency"],
      aliases=["guedel-airway"])
def _(S):
    body = union(_tube("M9 6V10C9 15.5 12.5 19.5 18.5 19.5H19.5", 4.5, S), rect(4, 2.5, 10, 3.5, L(S, 0.5, 1.5)))
    return [shell(body), detail(seg(9, 6, 9, 10))]


@icon("endotracheal-tube", CAT, "Breathing tube: a long curved tube with a cuff near the tip and a top connector",
      tags=["et tube", "intubation", "ventilator", "airway", "anesthesia", "icu"],
      aliases=["et-tube", "breathing-tube"])
def _(S):
    cx, cy, r = 19.5, 6.5, 13
    a = 120
    px, py = polar(cx, cy, r, a)
    ang = a + 90
    span = math.degrees(3.25 / r)
    cuff = xf(ellipse(0, 0, 3.25, 2.25), (math.cos(math.radians(ang)), math.sin(math.radians(ang)),
                                          -math.sin(math.radians(ang)), math.cos(math.radians(ang)), px, py))
    return [
        shell(rect(4.5, 2.5, 4, 4, L(S, 0.5, 1.25))),
        line(arc(cx, cy, r, a + span, 180)),
        shell(cuff),
        line(arc(cx, cy, r, 92, a - span)),
    ]


@icon("tracheostomy-tube", CAT, "Tracheostomy tube: a winged neck plate with a short curved tube",
      tags=["trach tube", "tracheotomy", "airway", "icu", "breathing", "neck"],
      aliases=["trach-tube"])
def _(S):
    m = axis((12, 0), 0)
    plate = stadium(lambda x, y: (x, 7 + y), 2.5, 21.5, 2.5, L(S, 1.5, 2.5))
    tube = _tube("M12 9V12.5C12 16.5 14.5 19.5 18.5 19.5", 4.5, S)
    return [
        shell(union(plate, tube)),
        detail(seg(5.5, 6, 5.5, 8)), detail(seg(18.5, 6, 18.5, 8)),
        dot(12, 7, 1.1),
    ]


# ============================================================================ diabetes and injectors

@icon("insulin-pen", CAT, "Insulin pen with a dose dial, a cartridge window and a short needle",
      tags=["insulin", "diabetes", "injection pen", "dose", "diabetic", "medication"],
      aliases=["injection-pen"])
def _(S):
    m = axis((12, 12), -45)
    return [
        shell(union(stadium(m, -7.5, 5.5, 2.75, L(S, 1, 2.75)), stadium(m, -10.5, -6, 2, L(S, 0.5, 2)))),
        detail(mseg(m, -7.5, -2.75, -7.5, 2.75)),
        detail(mseg(m, 0, 0, 3, 0)),
        shell(stadium(m, 5.5, 7.25, 1.25, L(S, 0, 0.5))) if False else line(mseg(m, 5.5, 0, 10, 0)),
    ]


@icon("insulin-pump", CAT, "Insulin pump with a screen and buttons, tubing leading out of the top",
      tags=["insulin", "diabetes", "infusion pump", "diabetic", "pump", "glucose"],
      aliases=["diabetes-pump"])
def _(S):
    return [
        shell(rect(3, 8, 13, 13.5, S.R)),
        detail(rect(5.5, 10.5, 8, 4.5, min(S.R, 1))),
        dot(7, 18.25, 1.1), dot(12, 18.25, 1.1),
        line("M12.5 8V6C12.5 3.5 14 2.5 16 2.5C18.5 2.5 19.5 4.5 19.5 6.5V21.5"),
    ]


@icon("cgm-sensor", CAT, "Continuous glucose sensor: a round skin patch with a drop and a wireless signal",
      tags=["cgm", "glucose monitor", "diabetes", "blood sugar", "sensor", "wearable"],
      aliases=["glucose-sensor"])
def _(S):
    return [
        shell(circle(9.5, 14.5, 7)),
        Part("dot", drop(9.5, 16, 2, S)),
        line(arc(9.5, 14.5, 10.5, -75, -15)),
        line(arc(9.5, 14.5, 13.75, -70, -25)),
    ]


@icon("auto-injector", CAT, "Emergency auto-injector pen with a safety cap and a rounded tip",
      tags=["epinephrine", "adrenaline", "anaphylaxis", "allergy emergency", "injector pen", "allergy"],
      aliases=["epinephrine-injector"])
def _(S):
    m = axis((12, 12), -45)
    return [
        shell(stadium(m, -6, 10, 3.5, L(S, 1.5, 3.5))),
        detail(mseg(m, 6, -3.5, 6, 3.5)),
        detail(mseg(m, -2, 0, 3, 0)),
        shell(stadium(m, -10.5, -6, 2.25, L(S, 0.5, 2))),
    ]


# ============================================================================ implants

@icon("pacemaker", CAT, "Pacemaker: a rounded metal case with a lead wire running to the heart",
      tags=["cardiac pacemaker", "heart device", "cardiology", "implant", "arrhythmia", "heart rhythm"],
      aliases=["cardiac-pacemaker"])
def _(S):
    return [
        shell(rect(2.5, 10.5, 11, 11, L(S, 2.5, 5))),
        detail(seg(2.5, 14, 13.5, 14)),
        line(poly([(13.5, 17.5), (17.5, 17.5), (17.5, 11.5)], r=L(S, 0, 2.5))),
        shell(small_heart(S, 17.5, 6.5, 0.62)),
    ]


@icon("stent", CAT, "Coronary stent: a short mesh tube with a diamond lattice",
      tags=["coronary stent", "angioplasty", "artery", "cardiology", "mesh tube", "heart"],
      aliases=["coronary-stent"])
def _(S):
    m = axis((12, 12), -45)
    zig1 = [(-9, -4), (-4.5, 4), (0, -4), (4.5, 4), (9, -4)]
    zig2 = [(-9, 4), (-4.5, -4), (0, 4), (4.5, -4), (9, 4)]
    return [
        line(mseg(m, -9, -4, 9, -4)), line(mseg(m, -9, 4, 9, 4)),
        detail(mpoly(m, zig1, r=S.r * 0.3)), detail(mpoly(m, zig2, r=S.r * 0.3)),
    ]


@icon("cochlear-implant", CAT, "Cochlear implant: an ear with a round coil above joined by a wire",
      tags=["hearing implant", "deaf", "hearing loss", "audiology", "ear", "bionic ear"],
      aliases=["bionic-ear"])
def _(S):
    return [
        line("M3.5 10.5A5.5 5.5 0 0 1 14.5 10.5C14.5 13.5 12.5 14 12.5 17C12.5 19.5 11 21 8.5 21"),
        detail("M7 10.5A2 2 0 0 1 11 10.5"),
        shell(circle(18, 5.5, 3)),
        dot(18, 5.5, 1),
        line("M18 8.5V11"),
        shell(rect(16.5, 11, 3.5, 7, L(S, 0.5, 1.75))),
    ]


@icon("hip-implant", CAT, "Hip replacement: a metal stem with a ball head in a round cup",
      tags=["hip replacement", "prosthesis", "orthopedics", "joint replacement", "arthroplasty", "implant"],
      aliases=["hip-prosthesis"])
def _(S):
    stem = poly([(8, 8), (12.5, 9.5), (17, 14), (17.5, 21.5), (14.5, 21.5), (12, 13.5), (6.5, 11)], closed=True, r=S.r * 0.6)
    return [
        line(arc(7.5, 7.5, 5.75, 135, 300)),
        shell(union(circle(7.5, 7.5, 2.75), stem)),
    ]


@icon("bone-plate", CAT, "Orthopedic bone plate: a waisted metal strip with a row of screw holes",
      tags=["fracture fixation", "orthopedics", "surgical plate", "bone fixation", "osteosynthesis", "implant"],
      aliases=["fracture-plate"])
def _(S):
    m = axis((12, 12), -45)
    xs = (-7.5, -2.5, 2.5, 7.5)
    body = union(*[circle(*m(x, 0), 2.75) for x in xs], stadium(m, -7.5, 7.5, 1.75, 0))
    if S.name == "line":
        body = union(*[poly([m(x - 2.5, -2.75), m(x + 2.5, -2.75), m(x + 2.5, 2.75), m(x - 2.5, 2.75)], closed=True) for x in xs],
                     stadium(m, -7.5, 7.5, 1.75, 0))
    return [shell(body), *[dot(*m(x, 0), 1) for x in xs]]


@icon("bone-screw", CAT, "Orthopedic bone screw with a wide flat head and deep coarse threads",
      tags=["orthopedic screw", "cortical screw", "fracture fixation", "surgical screw", "orthopedics", "implant"],
      aliases=["orthopedic-screw"])
def _(S):
    m = axis((12, 12), -45)
    top, bot = [], []
    x = -5.5
    while x < 6.5:
        top += [(x, -1.25), (x + 1.5, -3)]
        bot += [(x, 1.25), (x + 1.5, 3)]
        x += 3
    pts = top + [(8.5, -1.25), (10, 0), (8.5, 1.25)] + bot[::-1]
    head = stadium(m, -10.5, -5.5, 4, L(S, 0.5, 1.5))
    return [
        shell(union(mpoly(m, pts, closed=True), head), stroke_miterlimit="2"),
        detail(mseg(m, -8, -2, -8, 2)),
    ]
