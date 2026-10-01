"""TypeIcon Core: healthcare services (batch healthcare_002).

Patient services, pharmacy, records, public health and care settings. Medical crosses are plain plus
signs on neutral objects (no red-cross emblem). Overlapping objects are drawn in layers: the back layer
is cut away around the front one with a gap so the drawing stays readable at 16 px.
"""
import math

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path

from dsl import LINE, Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar, rotation  # noqa: F401

CAT = "healthcare"


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


def move(d, dx, dy):
    return xf(d, (1, 0, 0, 1, dx, dy))


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


def cross_solid(cx, cy, a, t=1.0):
    """Solid plus shape (arm length a, half thickness t) for use as a small mark."""
    return union(rect(cx - a, cy - t, 2 * a, 2 * t), rect(cx - t, cy - a, 2 * t, 2 * a))


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def sq(x, y, w, h, rx=0.0):
    return Part("dot", rect(x, y, w, h, rx))


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


def drop(cx, cy, r, S=None):
    """Liquid drop: circle of radius r centred at (cx, cy) with its point 2r above the centre."""
    tx, ty = cx, cy - 2 * r
    a = math.radians(30)
    rx_, ry_ = cx + r * math.cos(a), cy - r * math.sin(a)
    lx_, ly_ = cx - r * math.cos(a), ry_
    if S is not None and S.name == "rounded":
        return (f"M{fmt(tx)} {fmt(ty)}Q{fmt(cx + r * 0.55)} {fmt(ty + r * 0.9)} {fmt(rx_)} {fmt(ry_)}"
                f"A{fmt(r)} {fmt(r)} 0 1 1 {fmt(lx_)} {fmt(ly_)}Q{fmt(cx - r * 0.55)} {fmt(ty + r * 0.9)} {fmt(tx)} {fmt(ty)}Z")
    return f"M{fmt(tx)} {fmt(ty)}L{fmt(rx_)} {fmt(ry_)}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(lx_)} {fmt(ly_)}Z"


def leaf(cx, top, bottom, w):
    """Vertical pointed leaf from top to bottom, width w."""
    my = (top + bottom) / 2
    k = w * 0.66
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + k)} {fmt(top + (my - top) * 0.35)} {fmt(cx + k)} {fmt(bottom - (bottom - my) * 0.35)} {fmt(cx)} {fmt(bottom)}"
            f"C{fmt(cx - k)} {fmt(bottom - (bottom - my) * 0.35)} {fmt(cx - k)} {fmt(top + (my - top) * 0.35)} {fmt(cx)} {fmt(top)}Z")


def dashed_stadium(x0, x1, cy, r, n, duty=0.62, phase=0.0):
    """Dashed outline of a horizontal pill (end-circle centres x0 and x1, radius r) with n dashes."""
    Ls = x1 - x0
    A = math.pi * r
    pieces = [("l", (x0, cy - r), (x1, cy - r), Ls), ("a", (x1, cy), -90.0, 90.0, A),
              ("l", (x1, cy + r), (x0, cy + r), Ls), ("a", (x0, cy), 90.0, 270.0, A)]
    total = 2 * Ls + 2 * A
    step = total / n
    out = []

    def emit(s0, s1):
        acc = 0.0
        for pc in pieces:
            ln = pc[-1]
            a0, a1 = max(s0, acc), min(s1, acc + ln)
            if a1 - a0 > 1e-6:
                t0, t1 = (a0 - acc) / ln, (a1 - acc) / ln
                if pc[0] == "l":
                    (ax, ay), (bx, by) = pc[1], pc[2]
                    out.append(seg(ax + (bx - ax) * t0, ay + (by - ay) * t0, ax + (bx - ax) * t1, ay + (by - ay) * t1))
                else:
                    (cx_, cy_), d0, d1 = pc[1], pc[2], pc[3]
                    out.append(arc(cx_, cy_, r, d0 + (d1 - d0) * t0, d0 + (d1 - d0) * t1))
            acc += ln

    for i in range(n):
        s0 = (i * step + phase) % total
        s1 = s0 + step * duty
        if s1 <= total:
            emit(s0, s1)
        else:
            emit(s0, total)
            emit(0, s1 - total)
    return "".join(out)


# --------------------------------------------------------------------------- layered drawings

def _paint(parts, S):
    regs = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        else:
            regs.append(ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4))))
    return U(*regs)


def _sil(parts, S):
    regs = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        elif p.kind == "shell":
            regs.append(U(P(p.d), ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4)))))
        else:
            regs.append(ST(p.d, 2.0, S.cap, S.join))
    return U(*regs)


def _grow(region, g):
    if g <= 0:
        return region
    return U(region, ST(path_to_d(region), 2 * g, "round", "round"))


def _stroke_layers(S, layers, gap):
    out = list(layers[0])
    cover = _grow(_sil(layers[0], S), gap)
    for parts in layers[1:]:
        if not parts:
            continue
        vis = D(_paint(parts, S), cover)
        if abs(vis.area) > 0.01:
            out.append(solid(path_to_d(vis)))
        cover = U(cover, _grow(_sil(parts, S), gap))
    return out


def _filled_layers(layers, gap):
    result = filled_region(layers[0])
    cover = _grow(result, gap)
    for parts in layers[1:]:
        if not parts:
            continue
        f = filled_region(parts)
        result = U(result, D(f, cover))
        cover = U(cover, _grow(f, gap))
    return result


def layered(name, desc, tags, aliases=(), gap=1.5):
    """Register an icon drawn as layers: fn(S) -> [front parts, parts behind, ...]."""
    def deco(fn):
        icon(name, CAT, desc, tags=tags, aliases=aliases,
             filled=lambda: _filled_layers(fn(LINE), gap))(lambda S: _stroke_layers(S, fn(S), gap))
        return fn
    return deco


# ============================================================================ digital health services

@icon("patient-portal", CAT, "Browser window showing a patient avatar beside a medical plus sign",
      tags=["patient login", "health portal", "online records", "patient account", "web", "telehealth"])
def _(S):
    return [
        shell(rect(2, 3.5, 20, 17, S.R)),
        detail(seg(2, 8, 22, 8)),
        dot(8.5, 12.5, 2),
        detail("M4.5 20.5A4 3.5 0 0 1 12.5 20.5"),
        detail(plus(16.75, 14.25, 2.5)),
    ]


@icon("electronic-health-record", CAT, "Computer monitor showing a medical record with a plus sign and text lines",
      tags=["ehr", "emr", "digital record", "patient chart", "medical software", "health data"])
def _(S):
    return [
        shell(rect(2, 2.5, 20, 15, S.R)),
        detail(plus(7, 8, 2)),
        detail(seg(12, 6.5, 18, 6.5)), detail(seg(12, 10, 18, 10)),
        detail(seg(5.5, 13.75, 18, 13.75)),
        line(seg(12, 17.5, 12, 21)), line(seg(8, 21, 16, 21)),
    ]


@icon("home-test-kit", CAT, "Test kit box with a capped sample tube and a swab standing in it",
      tags=["self test", "at home test", "swab test", "sample kit", "diagnostic kit", "mail in test"])
def _(S):
    return [
        shell(rect(3, 12, 18, 9.5, S.R)),
        shell(union(rect(6.5, 2.5, 5, 9.5, L(S, 1, 2.5)), rect(6.5, 9, 5, 3))),
        detail(seg(6.5, 6, 11.5, 6)),
        line(seg(15.5, 12, 15.5, 7)),
        shell(ellipse(15.5, 4.5, 1.75, 2.25)),
        detail(plus(12, 16.75, 2.25)),
    ]


@icon("teledermatology", CAT, "Smartphone camera frame with focus brackets around a mole",
      tags=["skin check", "mole check", "dermatology app", "remote dermatology", "skin photo", "telehealth"])
def _(S):
    k = S.r * 0.4
    return [
        shell(rect(5, 2, 14, 20, min(S.R, 3))),
        detail(seg(10.5, 4.5, 13.5, 4.5)),
        detail(poly([(8, 10.5), (8, 8), (10.5, 8)], r=k)), detail(poly([(13.5, 8), (16, 8), (16, 10.5)], r=k)),
        detail(poly([(16, 15.5), (16, 18), (13.5, 18)], r=k)), detail(poly([(10.5, 18), (8, 18), (8, 15.5)], r=k)),
        mark(ellipse(12, 13, 2, 1.6)),
    ]


@icon("medical-dictation", CAT, "Microphone on a stand beside a medical note with a plus sign",
      tags=["voice notes", "dictate", "speech to text", "clinical notes", "transcription", "microphone"])
def _(S):
    return [
        shell(rect(2, 4, 9.5, 16, min(S.R, 2.5))),
        detail(plus(6.75, 9, 2)),
        detail(seg(5, 15.5, 8.5, 15.5)),
        shell(rect(16.5, 3, 4, 8.5, 2)),
        line("M14.5 9V10A4 4 0 0 0 22.5 10V9"),
        line(seg(18.5, 14, 18.5, 20)), line(seg(15.5, 20.5, 21.5, 20.5) if S.name == "line" else seg(15.5, 20, 21.5, 20)),
    ]


@layered("interpreter-services", "Two overlapping speech bubbles, one with the letter A and one with a plus sign",
         tags=["medical interpreter", "translation", "language help", "translator", "language access", "multilingual"])
def _(S):
    k = L(S, 0, 1.5)
    front = [shell(poly([(10, 12.5), (22, 12.5), (22, 19.5), (19.5, 19.5), (19.5, 22), (16.5, 19.5), (10, 19.5)], closed=True, r=k)),
             detail(plus(16, 16, 2))]
    back = [shell(poly([(2, 2), (15, 2), (15, 12), (8.5, 12), (5, 15), (5, 12), (2, 12)], closed=True, r=k)),
            detail(poly([(5, 9.5), (8.5, 4.5), (12, 9.5)], r=L(S, 0, 0.8))), detail(seg(6.3, 7.6, 10.7, 7.6))]
    return [front, back]


# ============================================================================ pharmacy

@icon("pharmacy-shelves", CAT, "Shelving unit stocked with bottles and boxes under a plus sign",
      tags=["drugstore shelves", "chemist", "medicine shelf", "pharmacy stock", "dispensary", "store"])
def _(S):
    parts = [shell(rect(3, 8.5, 18, 13.5, min(S.R, 2.5))), detail(seg(3, 15, 21, 15)), line(plus(12, 3.75, 2))]
    q = L(S, 0, 0.6)

    def bottle(x, base):
        return mark(union(rect(x, base - 2.75, 3, 2.75, q), rect(x + 0.75, base - 4, 1.5, 1.5)))
    # top shelf: bottle, box, bottle; bottom shelf: box, bottle, box
    parts += [bottle(5.5, 14), sq(10.25, 11.25, 3.5, 2.75, q), bottle(15.5, 14),
              bottle(5.5, 20.5), sq(10.25, 17.75, 3.5, 2.75, q), bottle(15.5, 20.5)]
    return parts


@icon("pill-pouch-strip", CAT, "Strip of three sealed sachets, each holding a pill",
      tags=["multi dose pouch", "pill packs", "dose packaging", "blister pouch", "medication packets", "adherence"])
def _(S):
    parts = [shell(rect(2, 6, 20, 12, L(S, 1, 3))),
             detail(seg(8.67, 6, 8.67, 18)), detail(seg(15.33, 6, 15.33, 18))]
    for cx in (5.33, 12, 18.67):
        parts.append(mark(stadium(axis((cx, 12), -60), -2.5, 2.5, 1.35, 1.35)))
    return parts


@icon("medication-drop-box", CAT, "Drop box on a post with a pull-down slot and a pill on its front",
      tags=["drug take back", "medicine disposal", "unused medication", "return box", "safe disposal", "pharmacy"])
def _(S):
    m = axis((12, 12.25), -35)
    top = "M3.5 16V7A5 5 0 0 1 8.5 2H15.5A5 5 0 0 1 20.5 7V16Z" if S.name == "rounded" else "M3.5 16V6L7 2.5H17L20.5 6V16Z"
    return [
        shell(top),
        detail(seg(7, 6.5, 17, 6.5)),
        mark(stadium(m, -4, 4, 1.9, 1.9)),
        line(seg(9, 16, 9, 21)), line(seg(15, 16, 15, 21)), line(seg(6.5, 21, 17.5, 21)),
    ]


@icon("drug-interaction", CAT, "Round tablet and capsule side by side with a spark between them",
      tags=["drug clash", "medicine interaction", "contraindication", "side effect", "pharmacist check", "warning"])
def _(S):
    return [
        shell(circle(6.5, 15, 4)),
        detail(seg(2.5, 15, 10.5, 15)),
        shell(rect(14.5, 10, 6, 11, 3)) if S.name == "rounded" else shell(stadium(axis((17.5, 15.5), 90), -5.5, 5.5, 3, 2.25)),
        detail(seg(14.5, 15.5, 20.5, 15.5)),
        line(seg(12.25, 3, 12.25, 7)), line(seg(7.5, 5, 9, 7.5)), line(seg(17, 5, 15.5, 7.5)),
    ]


@icon("dosage-schedule", CAT, "Card split into day and night columns with pill doses under a sun and a moon",
      tags=["medication schedule", "dose times", "morning and evening", "pill timetable", "dosing chart", "reminder"])
def _(S):
    moon = minus(circle(16.75, 7.75, 2.5), circle(18.25, 6.5, 2.25))
    return [
        shell(rect(2.5, 2.5, 19, 19, S.R)),
        detail(seg(12, 2.5, 12, 21.5)),
        detail(circle(7.25, 7.75, 1.75)),
        mark(moon),
        mark(stadium(axis((7.25, 13.25), 0), -2.25, 2.25, 1.1, 1.1)),
        mark(stadium(axis((7.25, 17.25), 0), -2.25, 2.25, 1.1, 1.1)),
        mark(stadium(axis((16.75, 13.25), 0), -2.25, 2.25, 1.1, 1.1)),
    ]


@icon("herbal-remedy", CAT, "Tincture bottle with a dropper cap beside a leaf",
      tags=["herbal medicine", "tincture", "natural remedy", "botanical", "plant medicine", "naturopathy"])
def _(S):
    lf = rot(leaf(0, -6, 6, 5.5), 25, 0, 0)
    lf = move(lf, 17.25, 12)
    return [
        shell(rect(2.5, 11.5, 9, 10, S.R)),
        shell(rect(4, 8, 6, 3.5, min(S.R, 1))),
        shell(rect(5, 2.5, 4, 5.5, L(S, 1.5, 2))),
        shell(lf),
        detail(move(rot(seg(0, -3.5, 0, 6.5), 25, 0, 0), 17.25, 12)),
    ]


@icon("placebo", CAT, "Capsule drawn with a dashed outline and a question mark inside",
      tags=["sugar pill", "dummy pill", "control group", "clinical trial", "inactive pill", "placebo effect"])
def _(S):
    return [
        line(dashed_stadium(9.5, 14.5, 12, 7.5, 10, duty=0.6, phase=L(S, 0.6, 0.9))),
        line("M10 9.75A2 2 0 1 1 13.1 11.4C12.3 11.9 12 12.4 12 13.5"),
        dot(12, 16.25, 1.25),
    ]


@icon("medication-leaflet", CAT, "Folded patient leaflet with a pill on one panel and text on the other",
      tags=["package insert", "patient information leaflet", "drug label", "instructions", "medicine guide", "pil"])
def _(S):
    m = axis((6.5, 12.5), -50)
    return [
        shell(poly([(2.5, 4.5), (12, 6.5), (21.5, 4.5), (21.5, 19), (12, 21), (2.5, 19)], closed=True, r=S.r * 0.5)),
        detail(seg(12, 6.5, 12, 21)),
        mark(stadium(m, -3.25, 3.25, 1.6, 1.6)),
        detail(seg(15, 10, 18.5, 9.25)), detail(seg(15, 13.5, 18.5, 12.75)), detail(seg(15, 17, 18.5, 16.25)),
    ]


@icon("medication-barcode-scan", CAT, "Handheld barcode scanner beaming onto the label of a pill bottle",
      tags=["bedside scanning", "barcode medication administration", "bcma", "scan medicine", "dispensing check", "pharmacy"])
def _(S):
    gun = union(rect(2, 4.5, 8.5, 5, L(S, 1, 2.5)), poly([(3, 9), (7, 9), (6, 16.5), (3, 16.5)], closed=True))
    return [
        shell(gun),
        line(seg(11.5, 7, 15, 10)), line(seg(11.5, 7, 15, 17)),
        shell(rect(14.5, 3, 7.5, 3.5, min(S.R, 1.5))),
        shell(rect(15, 8.5, 6.5, 13, min(S.R, 2.5))),
        detail(seg(15, 12, 21.5, 12)), detail(seg(15, 17.5, 21.5, 17.5)),
    ]


@icon("medical-folder", CAT, "File folder with a medical plus sign on its front",
      tags=["patient file", "medical file", "health records", "case file", "chart folder", "documents"])
def _(S):
    return [
        shell(poly([(2, 4), (9, 4), (11, 6.5), (22, 6.5), (22, 20), (2, 20)], closed=True, r=S.r)),
        detail(plus(12, 13.5, 3)),
    ]


@layered("x-ray-envelope", "Large envelope with a chest X-ray film sliding out of its open top",
         tags=["radiograph sleeve", "x-ray film", "imaging envelope", "radiology", "scan results", "film jacket"])
def _(S):
    front = [shell(rect(2, 14, 20, 7.5, min(S.R, 2.5))),
             detail(poly([(2, 14), (12, 18.5), (22, 14)], r=S.r))]
    back = [shell(rect(4.5, 2, 15, 13, min(S.R, 2))),
            detail(seg(12, 3, 12, 12))]
    for y in (5, 8.75):
        back += [detail(poly([(12, y), (9, y), (7.5, y + 1.5)], r=S.r * 0.6)),
                 detail(poly([(12, y), (15, y), (16.5, y + 1.5)], r=S.r * 0.6))]
    return [front, back]


@layered("medical-records-archive", "Records box with a plus sign holding patient chart folders with tabs",
         tags=["records room", "medical records", "chart storage", "filing", "patient files", "archive"])
def _(S):
    k = S.r * 0.5
    box = [shell(rect(2.5, 12, 19, 9.5, min(S.R, 2.5))), detail(plus(12, 16.75, 2.25))]
    front_folder = [shell(poly([(4.5, 13), (4.5, 5.5), (8.5, 5.5), (9.75, 7.5), (19.5, 7.5), (19.5, 13)], closed=True, r=k))]
    back_folder = [shell(poly([(6.5, 8), (6.5, 4), (13, 4), (14.25, 2), (18, 2), (19.25, 4), (21, 4), (21, 8)], closed=True, r=k))]
    return [box, front_folder, back_folder]


@layered("treatment-plan", "Clipboard with a pill beside the first line of a numbered list",
         tags=["care plan", "therapy plan", "treatment schedule", "medical plan", "regimen", "clinical plan"])
def _(S):
    clip = [shell(rect(8.5, 2.5, 7, 4, min(S.R, 1.5)))]
    board = [shell(rect(4.5, 4.5, 15, 17, S.R)),
             mark(stadium(axis((8.5, 10.5), -45), -2.25, 2.25, 1.25, 1.25)), detail(seg(11.5, 10.5, 16.5, 10.5)),
             dot(8.5, 14.5, 1.25), detail(seg(11.5, 14.5, 16.5, 14.5)),
             dot(8.5, 18, 1.25), detail(seg(11.5, 18, 16.5, 18))]
    return [clip, board]


@icon("symptom-diary", CAT, "Notebook with a thermometer on its cover and ticked days below",
      tags=["symptom log", "health journal", "symptom tracker", "illness diary", "daily log", "record symptoms"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, S.R)),
        detail(seg(7.5, 2.5, 7.5, 21.5)),
        detail(seg(17, 5.5, 13.75, 8.75)), dot(12.25, 10.25, 2.25),
        detail(poly([(10, 16.25), (11.25, 17.5), (13.25, 15.25)], r=L(S, 0, 0.6))),
        detail(poly([(14.75, 16.25), (16, 17.5), (18, 15.25)], r=L(S, 0, 0.6))),
    ]


def _dollar(cx, cy, r):
    """Dollar sign: an S made of two half loops (radius r) centred on (cx, cy), with a vertical bar."""
    a = math.radians(35)
    top = (cx + r * math.cos(a), cy - r - r * math.sin(a))
    bot = (cx - r * math.cos(a), cy + r + r * math.sin(a))
    s = (f"M{fmt(top[0])} {fmt(top[1])}A{fmt(r)} {fmt(r)} 0 1 0 {fmt(cx)} {fmt(cy)}"
         f"A{fmt(r)} {fmt(r)} 0 1 1 {fmt(bot[0])} {fmt(bot[1])}")
    return s + seg(cx, cy - 2 * r - 1.5, cx, cy + 2 * r + 1.5)


@icon("medical-bill", CAT, "Invoice with a medical plus sign, item lines and a dollar sign by the total",
      tags=["hospital bill", "medical invoice", "healthcare costs", "billing", "charges", "statement"])
def _(S):
    return [
        shell(rect(3.5, 2, 17, 20, min(S.R, 3))),
        detail(plus(8, 6.5, 2)),
        detail(seg(12, 6.5, 17, 6.5)),
        detail(seg(7, 11.5, 11.5, 11.5)), detail(seg(7, 15, 11.5, 15)), detail(seg(7, 18.5, 11.5, 18.5)),
        detail(_dollar(16, 15, 1.75)),
    ]


@icon("hippocratic-oath", CAT, "Open scroll with a rod and serpent beside lines of text",
      tags=["medical ethics", "physician oath", "doctors pledge", "first do no harm", "ethics", "graduation"])
def _(S):
    k = L(S, 1, 1.75)
    return [
        shell(rect(2.5, 2, 19, 3.5, k)),
        shell(rect(2.5, 18.5, 19, 3.5, k)),
        line(seg(4.5, 5.5, 4.5, 18.5)), line(seg(19.5, 5.5, 19.5, 18.5)),
        line(seg(9, 7.5, 9, 16.5)),
        line("M7 8.5C11 9 11 11 9 11.5C7 12 7 14 10.5 14.5"),
        line(seg(13, 9, 17, 9)), line(seg(13, 12, 17, 12)), line(seg(13, 15, 17, 15)),
    ]


@layered("surgical-checklist", "Clipboard with a scalpel at the top and a column of ticked boxes",
         tags=["surgical safety checklist", "pre op checklist", "operating room", "time out", "surgery", "safety check"])
def _(S):
    clip = [shell(rect(8.5, 2.5, 7, 4, min(S.R, 1.5)))]
    blade = "M11.5 8.75H17.5Q17.5 11.75 11.5 11.75Z" if S.name == "rounded" else "M11.5 8.75H17.5L15.5 11.75H11.5Z"
    board = [shell(rect(4.5, 4.5, 15, 17, S.R)),
             detail(seg(7, 10.25, 11.5, 10.25)), mark(blade),
             detail(poly([(7.5, 14.5), (8.75, 15.75), (10.75, 13.5)], r=L(S, 0, 0.6))), detail(seg(13, 14.75, 16.5, 14.75)),
             detail(poly([(7.5, 18.25), (8.75, 19.5), (10.75, 17.25)], r=L(S, 0, 0.6))), detail(seg(13, 18.5, 16.5, 18.5))]
    return [clip, board]


def _shield(S):
    if S.name == "rounded":
        return "M12 2.5L19.5 5.25Q20.5 5.6 20.5 6.7V11.5C20.5 16.5 16.75 19.75 12 21.5C7.25 19.75 3.5 16.5 3.5 11.5V6.7Q3.5 5.6 4.5 5.25Z"
    return "M12 2.5L20.5 5.5V11.5C20.5 16.5 16.75 19.75 12 21.5C7.25 19.75 3.5 16.5 3.5 11.5V5.5Z"


@icon("vision-insurance", CAT, "Shield with an eye drawn inside it",
      tags=["eye insurance", "vision plan", "eye care cover", "optical insurance", "vision benefits", "coverage"])
def _(S):
    return [
        shell(_shield(S)),
        detail("M6.75 11.5Q12 5 17.25 11.5Q12 18 6.75 11.5Z"),
        dot(12, 11.5, 1.5),
    ]


@icon("health-savings-account", CAT, "Piggy bank with a medical plus sign on its side and a coin above the slot",
      tags=["hsa", "medical savings", "health fund", "fsa", "healthcare savings", "save for care"])
def _(S):
    body = union(ellipse(12.5, 14, 8, 5.5), rect(2, 11.5, 3.5, 5, L(S, 0, 1.25)), poly([(15, 9), (17.5, 5.5), (18.5, 10)], closed=True))
    return [
        shell(body),
        detail(plus(13, 14.5, 2.25)),
        dot(8, 12.25, 1),
        shell(circle(11, 3.75, 2)) if S.name == "rounded" else shell(regular(11, 3.75, 2.2, 8, -67.5) and poly(regular(11, 3.75, 2.2, 8, -67.5), closed=True)),
        line(seg(7.5, 19, 7.5, 21.5)), line(seg(17.5, 19, 17.5, 21.5)),
    ]


_PLANE = [(0, -6), (1, -4.8), (1, -1.6), (5.5, 1.2), (5.5, 2.6), (1, 1.2), (1, 3.6), (2.6, 4.8), (2.6, 6),
          (0, 5.2), (-2.6, 6), (-2.6, 4.8), (-1, 3.6), (-1, 1.2), (-5.5, 2.6), (-5.5, 1.2), (-1, -1.6), (-1, -4.8)]


@icon("medical-tourism", CAT, "Airplane flying over a globe beside a medical plus sign",
      tags=["health travel", "treatment abroad", "medical travel", "overseas care", "surgery abroad", "global health"])
def _(S):
    m = axis((16.75, 7.25), 45)
    plane = [m(y, -x) for x, y in _PLANE]
    return [
        shell(circle(10, 14.5, 7)),
        detail(ellipse(10, 14.5, 3, 7)), detail(seg(3, 14.5, 17, 14.5)),
        mark(poly(plane, closed=True, r=L(S, 0, 0.4))),
        line(plus(5, 4.5, 2.25)),
    ]


def _letter_a(x0, y0, w, h):
    return poly([(x0, y0 + h), (x0 + w / 2, y0), (x0 + w, y0 + h)]) + seg(x0 + w * 0.22, y0 + h * 0.62, x0 + w * 0.78, y0 + h * 0.62)


@icon("blood-type", CAT, "Blood drop with the letters AB inside it",
      tags=["blood group", "abo", "blood typing", "donor", "transfusion", "rhesus"])
def _(S):
    b = "M13.25 17.75V12H14.9A1.45 1.45 0 0 1 14.9 14.9H13.25M15.1 14.9A1.43 1.43 0 0 1 15.1 17.75H13.25"
    return [
        shell(drop(12, 15.25, 6.5, S)),
        detail(_letter_a(7.5, 12, 4, 5.75)),
        detail(b),
    ]


@icon("reference-range", CAT, "Horizontal bar with a shaded normal band and a triangle marker pointing to a value",
      tags=["normal range", "lab range", "test result", "healthy range", "within limits", "lab values"])
def _(S):
    return [
        shell(rect(2, 11.5, 20, 6.5, L(S, 1, 3.25))),
        sq(8.5, 11.5, 7, 6.5),
        mark(poly([(13, 9.5), (10, 4.5), (16, 4.5)], closed=True, r=L(S, 0, 0.8))),
    ]


@icon("dna-test-kit", CAT, "Capped sample tube with a DNA helix on its label",
      tags=["genetic test", "ancestry test", "dna kit", "cheek swab", "genome test", "saliva test"])
def _(S):
    return [
        shell(union(rect(6.5, 2, 11, 4.5, min(S.R, 1.5)), rect(7.5, 5, 9, 17, L(S, 2, 4.5)))),
        detail(seg(6.5, 6.5, 17.5, 6.5)),
        detail("M9.75 9.5C9.75 12.75 14.25 12.25 14.25 15.5C14.25 18.25 9.75 17.75 9.75 20"),
        detail("M14.25 9.5C14.25 12.75 9.75 12.25 9.75 15.5C9.75 18.25 14.25 17.75 14.25 20"),
    ]


# ============================================================================ shared shapes (batch part 2)

def bust(S, cx, hy, hr, top, hw, bottom=21.5):
    """Head and open shoulders: a head circle above a rounded shoulder line."""
    rr = L(S, min(hw - 1.5, 2), hw - 0.5)
    body = (f"M{fmt(cx - hw)} {fmt(bottom)}V{fmt(top + rr)}A{fmt(rr)} {fmt(rr)} 0 0 1 {fmt(cx - hw + rr)} {fmt(top)}"
            f"H{fmt(cx + hw - rr)}A{fmt(rr)} {fmt(rr)} 0 0 1 {fmt(cx + hw)} {fmt(top + rr)}V{fmt(bottom)}")
    return [shell(circle(cx, hy, hr)), line(body)]


def heart_d(cx, cy, s):
    """Small heart about 2.2 s wide, centred on (cx, cy)."""
    pts = [(0, 1), (-0.6, 0.55), (-1.1, 0.2), (-1.1, -0.3), (-1.1, -0.85), (-0.45, -1.05), (0, -0.55),
           (0.45, -1.05), (1.1, -0.85), (1.1, -0.3), (1.1, 0.2), (0.6, 0.55), (0, 1)]
    q = [(cx + x * s, cy + y * s) for x, y in pts]
    out = f"M{fmt(q[0][0])} {fmt(q[0][1])}"
    for i in range(1, 13, 3):
        out += "C" + " ".join(f"{fmt(x)} {fmt(y)}" for x, y in q[i:i + 3])
    return out + "Z"


def pin_d(cx, cy, r, tip_y):
    """Map pin: circle head (cx, cy, r) narrowing to a point at (cx, tip_y)."""
    d = tip_y - cy
    a = math.degrees(math.acos(r / d))
    p1, p2 = polar(cx, cy, r, 90 - a), polar(cx, cy, r, 90 + a)
    return (f"M{fmt(cx)} {fmt(tip_y)}L{fmt(p1[0])} {fmt(p1[1])}A{fmt(r)} {fmt(r)} 0 1 0 {fmt(p2[0])} {fmt(p2[1])}Z")


def calendar(S, x=2.5, y=4, w=19, h=17.5, head=5):
    return [shell(rect(x, y, w, h, S.R)), detail(seg(x, y + head, x + w, y + head)),
            line(seg(x + w * 0.27, y - 2, x + w * 0.27, y + 2)), line(seg(x + w * 0.73, y - 2, x + w * 0.73, y + 2))]


# ============================================================================ services and planning

@icon("contact-tracing", CAT, "Smartphone linked by network lines to three people around it",
      tags=["exposure notification", "trace contacts", "infection tracking", "outbreak response", "public health", "app"])
def _(S):
    parts = [shell(rect(2.5, 3, 8, 18, min(S.R, 3))), detail(seg(5.25, 5.75, 7.75, 5.75)), dot(6.5, 12.5, 1.75)]
    for hy in (4.5, 12, 19.5):
        parts.append(shell(circle(19.25, hy, 2.25)))
    parts += [line(seg(10.5, 12, 17, 12)), line(seg(10.5, 9, 17.25, 5.5)), line(seg(10.5, 15, 17.25, 18.5))]
    return parts


@icon("pharmacy-counter", CAT, "Pharmacist behind a counter marked with a plus sign, with bottles on shelves",
      tags=["pharmacy desk", "chemist counter", "dispensary", "pharmacist", "drugstore", "prescription pickup"])
def _(S):
    q = L(S, 0, 0.6)

    def bottle(x, base):
        return mark(union(rect(x, base - 2.75, 3, 2.75, q), rect(x + 0.75, base - 4, 1.5, 1.5)))
    return [
        shell(rect(2, 14.5, 20, 7, min(S.R, 2.5))),
        detail(plus(12, 18, 1.75)),
        *bust(S, 12, 5.5, 2.25, 9.5, 3.5, 12.5),
        line(seg(2, 11, 5.5, 11)), line(seg(18.5, 11, 22, 11)),
        bottle(2.5, 9), bottle(18.5, 9),
    ]


@icon("blood-culture-bottle", CAT, "Squat round bottle with a flip-off cap and a barcode label",
      tags=["blood culture", "culture bottle", "sepsis test", "lab bottle", "specimen bottle", "microbiology"])
def _(S):
    return [
        shell(rect(8, 2, 8, 3.5, min(S.R, 1.5))),
        shell(union(rect(9.5, 5, 5, 4, 0), rect(4, 8.5, 16, 13, L(S, 3, 5)))),
        sq(7.5, 12.5, 1, 5), sq(9.5, 12.5, 2, 5), sq(12.5, 12.5, 1, 5), sq(14.5, 12.5, 2, 5),
    ]


@icon("clinical-trial", CAT, "Laboratory flask above a row of three people",
      tags=["medical research", "trial participants", "drug trial", "study volunteers", "research study", "clinical research"])
def _(S):
    parts = [shell(poly([(10, 2.5), (14, 2.5), (14, 6), (18, 12), (6, 12), (10, 6)], closed=True, r=S.r * 0.6)),
             detail(seg(8.5, 9.5, 15.5, 9.5))]
    for cx in (4.5, 12, 19.5):
        parts += [dot(cx, 16, 1.6), line(f"M{fmt(cx - 2.25)} 21.5A2.25 2.25 0 0 1 {fmt(cx + 2.25)} 21.5")]
    return parts


@icon("patient-journey", CAT, "Dotted path leading from a house to a map pin with a plus sign",
      tags=["care pathway", "patient path", "care journey", "patient experience", "referral route", "treatment path"])
def _(S):
    return [
        shell(poly([(2.5, 21.5), (2.5, 15.5), (6.5, 12), (10.5, 15.5), (10.5, 21.5)], closed=True, r=S.r * 0.6)),
        shell(pin_d(17, 7, 4.75, 15.5)),
        detail(plus(17, 7, 2)),
        dot(13.5, 20.25, 1), dot(16.25, 19.5, 1), dot(18.25, 17.5, 1),
    ]


@icon("medical-appointment", CAT, "Calendar page with a solid medical cross beside a few date dots",
      tags=["doctor appointment", "clinic visit", "book appointment", "medical schedule", "checkup date", "booking"])
def _(S):
    return calendar(S) + [dot(6.5, 13, 1.25), dot(10, 13, 1.25), dot(6.5, 17.5, 1.25), dot(10, 17.5, 1.25),
                          mark(cross_solid(16, 15.25, 3.25, 1.2))]


@layered("immunization-schedule", "Calendar page with a syringe lying diagonally across it",
         tags=["vaccination schedule", "vaccine calendar", "shot schedule", "immunisation", "booster date", "jab"])
def _(S):
    m = axis((15.5, 15), -45)
    k = S.r * 0.5
    syr = [shell(poly([m(-4, -2.25), m(4, -2.25), m(4, 2.25), m(-4, 2.25)], closed=True, r=k)),
           detail(poly([m(-1.25, -2.25), m(-1.25, 0)])), detail(poly([m(1.25, -2.25), m(1.25, 0)])),
           line(poly([m(4, 0), m(8.5, 0)])), line(poly([m(-4, 0), m(-7, 0)])), line(poly([m(-7, -2.25), m(-7, 2.25)]))]
    cal = calendar(S, 2.5, 4, 15, 14.5, 4.5)
    return [syr, cal]


@icon("doctor-consultation", CAT, "Doctor and patient seated on opposite sides of a desk under a plus sign",
      tags=["doctor visit", "consultation", "medical appointment", "gp visit", "patient meeting", "clinic"])
def _(S):
    return [
        *bust(S, 6, 7.5, 2.25, 11.5, 3.25, 13.5),
        *bust(S, 18, 7.5, 2.25, 11.5, 3.25, 13.5),
        detail(plus(12, 5, 1.75)),
        line(seg(2, 16, 22, 16)), line(seg(4.5, 16, 4.5, 21.5)), line(seg(19.5, 16, 19.5, 21.5)),
    ]


@layered("care-team", "Three people side by side under a heart, the middle one with a plus sign",
         tags=["healthcare team", "medical staff", "care providers", "multidisciplinary team", "clinicians", "support team"])
def _(S):
    mid = bust(S, 12, 10.5, 2.25, 14.5, 4) + [detail(plus(12, 18.25, 1.5))]
    sides = bust(S, 4.75, 9, 2, 13, 3) + bust(S, 19.25, 9, 2, 13, 3)
    return [mid + [mark(heart_d(12, 4, 1.6))], sides]


@icon("hospital-meal-tray", CAT, "Tray holding a covered plate and a lidded cup",
      tags=["patient meal", "hospital food", "meal service", "room service", "cloche", "diet tray"])
def _(S):
    return [
        shell("M3 14.5A5 5 0 0 1 13 14.5Z" if S.name == "line" else "M3.5 14.5A4.5 5 0 0 1 12.5 14.5Z"),
        line(seg(8, 6.5, 8, 9.5)),
        shell(rect(14.5, 9, 5, 5.5, L(S, 0.5, 1.5))),
        detail(seg(14.5, 11, 19.5, 11)),
        line("M19.5 10.25A2 2 0 0 1 19.5 14.25"),
        line(poly([(2, 16.5), (3.5, 19.5), (20.5, 19.5), (22, 16.5)], r=S.r)),
    ]


def _get_well(S):
    m = axis((15.25, 12), -50)
    band = stadium(m, -5.5, 5.5, 2, L(S, 1, 2))
    pad = poly([m(-1.5, -2), m(1.5, -2), m(1.5, 2), m(-1.5, 2)], closed=True, r=L(S, 0, 0.5))
    front = [shell(rect(9, 2.5, 12.5, 19, min(S.R, 2))), detail(band), detail(pad)]
    back = [shell(poly([(9.5, 4.5), (2.5, 6.5), (2.5, 20.5), (9.5, 19.5)], closed=True, r=S.r * 0.5))]
    return [front, back], band, pad


def _get_well_filled():
    (front, back), band, pad = _get_well(LINE)
    card = filled_region(front[:1])
    card = U(D(card, U(P(band), ST(band, 2.0, "butt", "miter"))), P(pad))
    return U(card, D(filled_region(back), _grow(card, 1.5)))


@icon("get-well-card", CAT, "Folded greeting card standing open with an adhesive bandage on its front",
      tags=["get well soon", "greeting card", "recovery wishes", "feel better", "sympathy card", "patient gift"],
      filled=_get_well_filled)
def _(S):
    return _stroke_layers(S, _get_well(S)[0], 1.5)


@icon("clinic-locator", CAT, "Map pin with a medical plus sign in its round head",
      tags=["find a clinic", "nearby clinic", "hospital location", "doctor near me", "health center map", "directions"])
def _(S):
    return [shell(pin_d(12, 9.5, 7.5, 22) if S.name == "line" else pin_d(12, 9.5, 7.5, 21.5)),
            detail(plus(12, 9.5, 3))]


@icon("bifocals", CAT, "Eyeglasses whose lenses each have a curved reading segment line in the lower half",
      tags=["bifocal glasses", "reading segment", "presbyopia", "varifocals", "spectacles", "optician"])
def _(S):
    k = L(S, 2, 3.5)
    return [
        shell(rect(2, 7.5, 8.5, 9, k)), shell(rect(13.5, 7.5, 8.5, 9, k)),
        line("M10.5 10C11.3 9.2 12.7 9.2 13.5 10"),
        detail("M2 13.5Q6.25 11.25 10.5 13.5"), detail("M13.5 13.5Q17.75 11.25 22 13.5"),
    ]


@icon("quit-smoking", CAT, "Cigarette snapped in two, with a curl of smoke rising from the lit end",
      tags=["stop smoking", "smoking cessation", "no smoking", "quit tobacco", "break the habit", "smoke free"])
def _(S):
    k = S.r * 0.4
    return [
        shell(poly([(2, 13), (10, 13), (9, 15), (10.5, 17), (2, 17)], closed=True, r=k)),
        shell(poly([(13, 13), (22, 13), (22, 17), (13.5, 17), (12.5, 15)], closed=True, r=k)),
        detail(seg(5.5, 13, 5.5, 17)), detail(seg(19, 13, 19, 17)),
        line("M20 10C18.5 8.5 20.5 7 19.25 5.25C18.5 4 19 3 19.75 2.5" if S.name == "rounded"
             else "M20 10.5L18.75 8.5L20.25 6.5L19 4.5L20 2.5"),
    ]


@icon("nurse-cap", CAT, "Traditional folded nurse cap seen from the front with a medical cross on it",
      tags=["nursing cap", "nurse hat", "nursing", "nurse", "caregiver", "nightingale"])
def _(S):
    crown = ("M4.5 15L6 6.5Q12 4 18 6.5L19.5 15Z" if S.name == "line"
             else "M4.5 15L5.8 7.6Q6 6.6 7 6.3Q12 4.5 17 6.3Q18 6.6 18.2 7.6L19.5 15Z")
    return [
        shell(crown),
        shell(rect(2.5, 15, 19, 4.5, L(S, 1, 2.25))),
        mark(cross_solid(12, 10.5, 2.5, 1)),
    ]


def virus_d(cx, cy, r, spike, n=8, start=0.0):
    """Small virus particle: a disc with n short knobbed spikes (for solid marks)."""
    regs = [P(circle(cx, cy, r))]
    for i in range(n):
        a = start + i * 360 / n
        p0, p1 = polar(cx, cy, r - 0.2, a), polar(cx, cy, r + spike, a)
        regs.append(ST(seg(p0[0], p0[1], p1[0], p1[1]), 1.1, "round", "round"))
        regs.append(P(circle(p1[0], p1[1], 0.7)))
    return path_to_d(U(*regs))


# ============================================================================ people and public health

@icon("patient-with-iv-pole", CAT, "Patient in a gown walking beside a wheeled IV pole with a drip bag",
      tags=["iv drip", "walking patient", "infusion", "hospital patient", "inpatient", "drip stand"])
def _(S):
    k = S.r * 0.5
    return [
        shell(circle(6.5, 4.5, 2.25)),
        shell(poly([(4.5, 8.5), (8.5, 8.5), (10.5, 16.5), (2.5, 16.5)], closed=True, r=k)),
        line(seg(4.75, 16.5, 4, 21.5)), line(seg(8.25, 16.5, 9.5, 21.5)),
        line(seg(8.75, 10.5, 15, 12)),
        line(seg(16, 2.5, 16, 20.5)), line(poly([(16, 3), (19.75, 3), (19.75, 5)], r=S.r * 0.5)),
        shell(rect(18, 5, 3.5, 6, L(S, 0.5, 1.5))),
        line(seg(12.5, 21, 19.5, 21)),
    ]


@icon("person-on-crutches", CAT, "Person walking on two underarm crutches with one leg lifted",
      tags=["crutches", "injured leg", "broken leg", "mobility aid", "recovery", "orthopedic"])
def _(S):
    return [
        shell(circle(12, 4.25, 2.25)),
        line(poly([(6.5, 14.5), (12, 9.5), (17.5, 14.5)], r=S.r)),
        line(seg(12, 9.5, 12, 15)),
        line(seg(12, 15, 11, 21.5)),
        line(poly([(12, 15), (14.25, 17.5), (16.5, 16.5)], r=S.r * 0.6)),
        line(seg(7.75, 8.5, 4.75, 21.5)), line(seg(16.25, 8.5, 19.25, 21.5)),
        line(seg(6, 8, 9.5, 8) if S.name == "line" else seg(6.25, 8, 9.25, 8)),
        line(seg(14.5, 8, 18, 8) if S.name == "line" else seg(14.75, 8, 17.75, 8)),
    ]


@icon("vaccination-drive", CAT, "Megaphone with a syringe standing beside its open end",
      tags=["vaccination campaign", "immunization drive", "vaccine campaign", "health campaign", "public health", "jab drive"])
def _(S):
    k = S.r * 0.5
    return [
        shell(poly([(2.5, 9.5), (6.5, 9.5), (13, 4.5), (13, 19.5), (6.5, 14.5), (2.5, 14.5)], closed=True, r=k)),
        line(seg(8, 15.5, 8, 19)),
        shell(rect(16, 7, 5, 10, L(S, 0.5, 1.5))),
        detail(seg(16, 10.5, 18.5, 10.5)), detail(seg(16, 13.5, 18.5, 13.5)),
        line(seg(18.5, 17, 18.5, 21.5)),
        line(seg(18.5, 7, 18.5, 3.5)), line(seg(16, 3, 21, 3) if S.name == "line" else seg(16.5, 3, 20.5, 3)),
    ]


@icon("outbreak-map", CAT, "Folded map with a virus particle marking a cluster of cases",
      tags=["disease map", "epidemic map", "case map", "hotspot", "epidemiology", "pandemic tracking"])
def _(S):
    k = S.r * 0.4
    return [
        shell(poly([(2, 5), (7.5, 3), (16.5, 5), (22, 3), (22, 19), (16.5, 21), (7.5, 19), (2, 21)], closed=True, r=k)),
        detail(seg(7.5, 3, 7.5, 19)), detail(seg(16.5, 5, 16.5, 21)),
        mark(virus_d(12, 10.5, 1.75, 1.25)),
        dot(10.5, 16.25, 1), dot(13.75, 17, 1),
    ]


@layered("herd-immunity", "Shield standing in front of a group of three people",
         tags=["community immunity", "population immunity", "group protection", "vaccination coverage", "public health", "herd protection"])
def _(S):
    sh = xf(_shield(S), (0.6, 0, 0, 0.6, 4.8, 9.1))
    front = [shell(sh), detail(plus(12, 15, 2))]
    people = bust(S, 4.5, 8, 2, 12, 3) + bust(S, 19.5, 8, 2, 12, 3) + [shell(circle(12, 4.5, 2))]
    return [front, people]


@icon("surface-disinfection", CAT, "Spray bottle misting a virus particle on a flat surface",
      tags=["disinfect surfaces", "sanitize", "cleaning", "disinfectant spray", "infection control", "sanitise"])
def _(S):
    k = S.r * 0.5
    return [
        shell(poly([(3, 2.5), (10, 2.5), (12, 4.5), (10, 6.5), (3, 6.5)], closed=True, r=k)),
        shell(rect(3, 9.5, 7.5, 12, L(S, 1, 3))),
        line(seg(6.25, 6.5, 6.25, 9.5)),
        line(poly([(10, 6.5), (11.5, 9)], r=0)),
        dot(15, 4.5, 1), dot(17, 7, 1), dot(14.5, 8.5, 1),
        mark(virus_d(17.5, 15, 2, 1.25)),
        line(seg(13.5, 21, 22, 21)),
    ]


@icon("uv-disinfection-robot", CAT, "Tall wheeled robot column with light tubes giving off rays",
      tags=["uv robot", "ultraviolet disinfection", "uv-c", "room disinfection", "germicidal light", "infection control"])
def _(S):
    return [
        shell(rect(8, 2.5, 8, 14.5, L(S, 1, 3))),
        detail(seg(10.75, 5.5, 10.75, 14)), detail(seg(13.25, 5.5, 13.25, 14)),
        shell(rect(6.5, 17, 11, 3.5, min(S.R, 1.5))),
        line(seg(2.5, 6, 5, 7)), line(seg(2.5, 10, 5, 10)), line(seg(2.5, 14, 5, 13)),
        line(seg(21.5, 6, 19, 7)), line(seg(21.5, 10, 19, 10)), line(seg(21.5, 14, 19, 13)),
    ]


@icon("baby-weighing-sling", CAT, "Hanging dial scale with a baby's head peeking out of a cloth sling below it",
      tags=["salter scale", "hanging scale", "infant weighing", "growth monitoring", "baby weight", "community health"])
def _(S):
    return [
        shell(circle(12, 6, 3.5)),
        detail(seg(12, 6, 13.75, 4.5)),
        line(seg(12, 9.5, 12, 11.5)),
        line(poly([(4.5, 15.5), (12, 11.5), (19.5, 15.5)], r=S.r)),
        dot(12, 14.25, 1.5),
        shell("M3.5 16H20.5C20 20 16.5 21.5 12 21.5C7.5 21.5 4 20 3.5 16Z" if S.name == "rounded"
              else "M3.5 16H20.5L18 21.5H6Z"),
    ]


@icon("nightingale-lamp", CAT, "Old oil lamp with a long spout and a small flame at its tip",
      tags=["lady with the lamp", "oil lamp", "nursing symbol", "nursing", "nightingale", "lamp of care"])
def _(S):
    body = ("M3.5 15C3.5 12.25 6.5 11 10.5 11C13.5 11 15.5 12 17 13L20.5 13.5V15.5H17C15.5 17 13 17.75 10.5 17.75C6.5 17.75 3.5 16.75 3.5 15Z")
    return [
        shell(body),
        line(seg(8.5, 17.75, 8, 20.5)), line(seg(12.5, 17.75, 13, 20.5)), line(seg(6.5, 21, 14.5, 21)),
        line("M10.5 11V9.5"),
        mark(drop(20.25, 9, 1.75, S)),
    ]


@icon("breast-milk-bag", CAT, "Flat storage pouch with a zip top, measurement lines and a milk drop",
      tags=["milk storage bag", "breastmilk", "pumped milk", "breastfeeding", "freezer bag", "lactation"])
def _(S):
    k = S.r * 0.6
    return [
        shell(poly([(5.5, 2.5), (18.5, 2.5), (18.5, 19), (16, 21.5), (8, 21.5), (5.5, 19)], closed=True, r=k)),
        detail(seg(5.5, 6.5, 18.5, 6.5)),
        detail(seg(5.5, 10.5, 8.5, 10.5)), detail(seg(5.5, 14, 8.5, 14)), detail(seg(5.5, 17.5, 8.5, 17.5)),
        mark(drop(13.5, 15, 2.5, S)),
    ]


# ============================================================================ equipment, maternity and care

@icon("sterile-instrument-pack", CAT, "Instrument pack wrapped envelope style with a band of striped indicator tape",
      tags=["sterile pack", "surgical pack", "autoclave", "sterilization", "instrument tray wrap", "cssd"])
def _(S):
    parts = [shell(rect(2.5, 3.5, 19, 17, S.R)),
             detail(poly([(2.5, 3.5), (12, 10), (21.5, 3.5)], r=S.r * 0.5)),
             detail(rect(2.5, 13.5, 19, 3.5, 0))]
    for x in (5.5, 9.5, 13.5, 17.5):
        parts.append(mark(poly([(x, 13.5), (x + 1.75, 13.5), (x + 0.25, 17), (x - 1.5, 17)], closed=True)))
    return parts


@icon("anatomy-model", CAT, "Human torso model on a stand with one side of the chest opened to show a lung",
      tags=["anatomical model", "torso model", "medical teaching", "anatomy class", "organs", "biology model"])
def _(S):
    torso = ("M10 7.5H14L19 9.5C19.5 12.5 18 15 16.5 17.5H7.5C6 15 4.5 12.5 5 9.5Z" if S.name == "line"
             else "M10 7.5H14L18 9C18.8 9.3 19.1 9.7 19.1 10.5C19.1 13 17.8 15.3 16.5 17.5H7.5C6.2 15.3 4.9 13 4.9 10.5C4.9 9.7 5.2 9.3 6 9Z")
    lung = "M13.5 10C15.5 10 17 11.5 16.5 15H13.5Z"
    return [
        shell(circle(12, 3.75, 2)),
        shell(torso),
        detail(seg(12, 7.5, 12, 17.5)),
        mark(lung if S.name == "line" else "M13.5 11A1 1 0 0 1 14.5 10C16 10.2 16.9 11.8 16.5 14.2A1 1 0 0 1 15.5 15H14.5A1 1 0 0 1 13.5 14Z"),
        line(seg(12, 17.5, 12, 20.5)), line(seg(8.5, 21, 15.5, 21)),
    ]


@icon("infant-length-board", CAT, "Baby lying on a measuring board between a fixed headboard and a sliding footboard",
      tags=["length board", "infant measuring", "baby length", "growth monitoring", "measuring board", "pediatrics"])
def _(S):
    return [
        shell(rect(2, 17, 20, 4.5, min(S.R, 1.5))),
        detail(seg(7, 17, 7, 19)), detail(seg(12, 17, 12, 19)), detail(seg(17, 17, 17, 19)),
        line(seg(3.5, 8, 3.5, 17)),
        line(seg(20, 10, 20, 17)),
        shell(union(circle(7.5, 12.5, 2.5), rect(9.5, 11, 8.5, 3.5, L(S, 0, 1.75)))),
    ]


@icon("pregnancy-wheel", CAT, "Round dial calculator with an inner rotating disc and a pointer",
      tags=["due date calculator", "gestation wheel", "obstetric wheel", "pregnancy calculator", "edd", "midwife"])
def _(S):
    parts = [shell(circle(12, 12, 9.5)), detail(circle(12, 12, 5)), detail(seg(12, 12, 12, 8.5))]
    for a in range(-45, 225, 45):
        if a == 90:
            continue
        p = polar(12, 12, 7.25, a)
        parts.append(dot(p[0], p[1], 0.9))
    parts.append(mark(poly([(12, 2.5), (13.75, 5.25), (10.25, 5.25)], closed=True, r=L(S, 0, 0.5))))
    return parts


@icon("birthing-pool", CAT, "Inflatable birthing tub with thick rounded walls and water waves inside",
      tags=["birth pool", "water birth", "labor pool", "labour", "midwife", "home birth"])
def _(S):
    tub = ("M2 10.5A2 2 0 0 1 6 10.5V17H18V10.5A2 2 0 0 1 22 10.5V21.5H2Z" if S.name == "line"
           else "M2 10.5A2 2 0 0 1 6 10.5V17H18V10.5A2 2 0 0 1 22 10.5V19A2.5 2.5 0 0 1 19.5 21.5H4.5A2.5 2.5 0 0 1 2 19Z")
    return [
        shell(tub),
        line("M8.5 14Q10.25 12.75 12 14Q13.75 15.25 15.5 14"),
        line("M8.5 10Q10.25 8.75 12 10Q13.75 11.25 15.5 10"),
    ]


@icon("hospital-visit", CAT, "Patient resting in a hospital bed beside a vase of flowers",
      tags=["visiting hours", "visit patient", "hospital stay", "bedside", "get well", "inpatient"])
def _(S):
    return [
        line(seg(2.5, 7, 2.5, 21.5)),
        line(poly([(2.5, 17), (14.5, 17), (14.5, 21.5)], r=S.r)),
        shell(circle(6, 12.5, 2)),
        line(seg(9.5, 13.5, 14.5, 13.5)),
        shell(rect(17, 15.5, 4.5, 6, L(S, 0.5, 1.75))),
        line(seg(19.25, 15.5, 19.25, 10)), line(seg(19.25, 13, 17, 10.5)), line(seg(19.25, 13, 21.5, 10.5)),
        dot(19.25, 8.5, 1.75), dot(16.75, 9, 1.25), dot(21.75, 9, 1.25),
    ]


# ============================================================================ chunk 3: people, measuring and care aids

@icon("second-opinion", CAT, "Two doctors facing each other under two speech bubbles, one holding a check mark",
      tags=["second opinion", "another doctor", "medical review", "consult", "specialist review", "diagnosis check", "peer review"])
def _(S):
    k = S.r * 0.5
    return [
        shell(poly([(2.5, 2.5), (10.5, 2.5), (10.5, 8.5), (5.25, 8.5), (2.5, 11.25)], closed=True, r=k)),
        shell(poly([(21.5, 2.5), (13.5, 2.5), (13.5, 8.5), (18.75, 8.5), (21.5, 11.25)], closed=True, r=k)),
        detail(poly([(15.75, 5.5), (17.25, 7), (19.5, 4.25)], r=0)),
        shell(circle(6.5, 14.25, 2)), line("M3.25 21.5A3.25 3.25 0 0 1 9.75 21.5"),
        shell(circle(17.5, 14.25, 2)), line("M14.25 21.5A3.25 3.25 0 0 1 20.75 21.5"),
    ]


@layered("hospital-discharge", "Person carrying a small bag walking out through a doorway marked with a plus sign",
         tags=["discharge", "leaving hospital", "going home", "release from care", "patient leaves", "check out", "exit"])
def _(S):
    door = [line(poly([(14.5, 21.5), (14.5, 3.5), (21.5, 3.5), (21.5, 21.5)], r=S.r)),
            detail(plus(18, 10, 1.75))]
    person = [shell(circle(6.5, 5, 2.25)), line(seg(6.5, 8.5, 6.5, 15.5)),
              line(seg(6.5, 15.5, 4, 21.5)), line(seg(6.5, 15.5, 9.5, 21.5)),
              line(poly([(6.5, 10.5), (9.75, 13)], r=0)),
              shell(rect(9.5, 13, 3, 3.5, L(S, 0.5, 1)))]
    return [person, door]


@icon("fall-risk", CAT, "Person tipping backward off balance with one leg kicked up and motion lines by the feet",
      tags=["fall", "falling", "slip", "trip", "falls prevention", "balance", "patient safety", "stumble"])
def _(S):
    return [
        shell(circle(16.5, 4.5, 2.25)),
        line(poly([(14.25, 8.5), (10.5, 15.5)])),
        line(poly([(13.25, 10), (19.5, 9)], r=0)), line(poly([(12, 12.25), (6.5, 10.25)], r=0)),
        line(poly([(10.5, 15.5), (15.5, 16.5), (18, 13.75)], r=S.r)),
        line(seg(10.5, 15.5, 10.75, 21.5)),
        line(seg(2.5, 18.5, 6, 18.5)), line(seg(2.5, 21.5, 7, 21.5)),
    ]


@icon("urine-color-chart", CAT, "Vertical strip of three swatches from pale to dark with a drop and a pointer beside it",
      tags=["urine colour", "hydration chart", "pee color", "dehydration", "colour scale", "urinalysis", "urine test"])
def _(S):
    return [
        shell(rect(12.5, 2.5, 9, 19, L(S, 1, 2.5))),
        detail(seg(12.5, 8.83, 21.5, 8.83)), detail(seg(12.5, 15.17, 21.5, 15.17)),
        sq(15, 11, 4, 2), sq(14.5, 17.5, 5, 2.5),
        mark(drop(6, 6.5, 2.25, S)),
        mark(poly([(2.5, 15.75), (9, 18.75), (2.5, 21.75)], closed=True, r=0)),
    ]


@layered("wheelchair-escort", "Standing person pushing a wheelchair with someone seated in it",
         tags=["wheelchair assistance", "pushing wheelchair", "patient transport", "porter", "mobility help", "hospital transport", "escort"])
def _(S):
    chair = [shell(circle(14.5, 18, 3.5)),
             line(poly([(9, 8.5), (10.5, 15), (17.5, 15), (19, 18.5)], r=S.r * 0.5))]
    seated = [shell(circle(15, 4.5, 2)), line(poly([(13.5, 8), (13, 15)], r=0))]
    pusher = [shell(circle(4, 4.5, 2)), line(seg(4, 8, 4, 15)), line(seg(4, 15, 2.5, 21.5)), line(seg(4, 15, 6.5, 21.5)),
              line(seg(4, 10, 9, 8.5))]
    return [pusher, chair, seated]
