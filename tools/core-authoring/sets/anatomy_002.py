"""TypeIcon Core: anatomy (batch anatomy_002).

Body regions, bones and joints, symptoms and common skin, mouth and hair conditions, drawn from the body
itself. Marked regions follow the body set: a solid zone inside the outline (Line/Rounded) and a solid zone cut
off by a 2 px gap (Filled). Heads in profile face right, like the body set.
"""
import math

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path

from dsl import Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import LINE, D, I, P, ST, U, fmt, path_to_d, polar  # noqa: F401

CAT = "anatomy"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def xf(d, matrix):
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, matrix))
    return pen.getCommands()


def tf(d, k=1.0, dx=0.0, dy=0.0, sx=1.0):
    """Scale by k (sx=-1 mirrors horizontally about x=0) and then move by (dx, dy)."""
    return xf(d, (k * sx, 0, 0, k, dx, dy))


def rot(d, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return xf(d, (c, s, -s, c, cx - c * cx + s * cy, cy - s * cx - c * cy))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def inter(a, b):
    return path_to_d(I(P(a), P(b)))


def sil(d, w=2.0):
    """Filled silhouette of a closed Line outline."""
    return U(P(d), ST(d, w, "butt", "miter"))


def zicon(name, desc, tags, clip, outline, aliases=()):
    """Icon with a marked zone: the part of `outline(S)` inside `clip` is solid.

    Line/Rounded: the zone fills the outline up to its stroke. Filled: the derived design is cut back
    by a 2 px gap around the clip and the zone sits inside that gap."""
    def deco(fn):
        def draw(S):
            return fn(S) + [solid(inter(outline(S), clip))]

        def filled():
            base = filled_region(fn(LINE))
            out = U(P(clip), ST(clip, 4, "butt", "miter"))
            return U(D(base, out), I(sil(outline(LINE)), P(clip)))
        icon(name, CAT, desc, tags=tags, aliases=aliases, filled=filled)(draw)
        return draw
    return deco


def zigzag(x0, y0, x1, y1, n=3, amp=1.0):
    """Zigzag line from (x0, y0) to (x1, y1) with n teeth."""
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln
    pts = [(x0, y0)]
    for i in range(1, 2 * n):
        t = i / (2 * n)
        s = amp if i % 2 else -amp
        pts.append((x0 + dx * t + nx * s, y0 + dy * t + ny * s))
    pts.append((x1, y1))
    return pts


# head in profile (facing right) and a front face, shared with the body set's proportions
HEAD = "M8 21V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.5 12.8L19 13.3V15.5C19 16.6 18.1 17.5 17 17.5H14V21Z"
HEAD_R = ("M8 20V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.2 12Q20.6 12.9 19.7 13.1L19 13.3V15.5"
          "C19 16.6 18.1 17.5 17 17.5H14V20C14 20.6 13.6 21 13 21H9C8.4 21 8 20.6 8 20Z")


def head(S):
    return L(S, HEAD, HEAD_R)


def small_head(S, k=0.7, dx=0.0, dy=0.0, flip=False):
    """Profile head scaled by k and moved; flip=True faces left."""
    if flip:
        return tf(head(S), k, dx, dy, sx=-1)
    return tf(head(S), k, dx, dy)


FACE = ellipse(12, 12, 7, 9)


# torso without arms (front view)
TRUNK = "M9.5 3V5.3C6.5 5.7 4.5 6.4 4.5 9.5L5 13C5.3 15.2 6.5 17 6.5 21H17.5C17.5 17 18.7 15.2 19 13L19.5 9.5C19.5 6.4 17.5 5.7 14.5 5.3V3Z"
TRUNK_R = ("M9.5 3V5.3C6.5 5.7 4.5 6.4 4.5 9.5L5 13C5.3 15.2 6.5 17 6.5 20Q6.5 21 7.5 21H16.5Q17.5 21 17.5 20C17.5 17 18.7 15.2 19 13"
           "L19.5 9.5C19.5 6.4 17.5 5.7 14.5 5.3V3Z")

# torso with arm stubs (front or back view), as in the body set
TORSO = "M9.5 3V5.3C7.3 5.8 5.2 6.3 4 7.6C3.3 8.4 3 9.5 3 10.8V16H5.6L6.5 21H17.5L18.4 16H21V10.8C21 9.5 20.7 8.4 20 7.6C18.8 6.3 16.7 5.8 14.5 5.3V3Z"
TORSO_R = ("M9.5 3V5.3C7.3 5.8 5.2 6.3 4 7.6C3.3 8.4 3 9.5 3 10.8V15Q3 16 4 16H5.6L6.4 20.1Q6.5 21 7.4 21H16.6Q17.5 21 17.6 20.1L18.4 16H20Q21 16 21 15"
           "V10.8C21 9.5 20.7 8.4 20 7.6C18.8 6.3 16.7 5.8 14.5 5.3V3Z")


def torso(S):
    return [shell(L(S, TORSO, TORSO_R)), detail(seg(5.6, 10.5, 5.6, 16)), detail(seg(18.4, 10.5, 18.4, 16))]


def trunk(S):
    return L(S, TRUNK, TRUNK_R)


# ============================================================================ body regions

_OBL = ("M2 10.5L10.3 14.5V18.7L2 14.7Z" "M22 10.5L13.7 14.5V18.7L22 14.7Z")


@zicon("obliques", "Front view of a torso with the side waist muscles marked",
       ["oblique muscles", "abs", "core", "waist", "side abs", "torso", "workout"], _OBL, trunk)
def _(S):
    return [shell(trunk(S)), detail(L(S, "M8.5 9.5C8.8 11 10 11.7 11.2 11.4", "M8.5 9.5C8.8 11 10 11.7 11.2 11.4")),
            detail("M15.5 9.5C15.2 11 14 11.7 12.8 11.4")]


_ARMPIT = ("M3.5 21V14.5C3.5 12 5.5 10.5 8 10.5H13.8L14.6 4.2A2.2 2.2 0 0 1 19 4.2V12C19 13.6 16.5 14 16.5 16V21Z")
_ARMPIT_R = ("M4.5 21Q3.5 21 3.5 20V14.5C3.5 12 5.5 10.5 8 10.5H13.8L14.6 4.2A2.2 2.2 0 0 1 19 4.2V12C19 13.6 16.5 14 16.5 16V20"
             "Q16.5 21 15.5 21Z")


@zicon("armpit", "Upper body with one arm raised and the underarm marked",
       ["underarm", "axilla", "arm raised", "deodorant", "sweat", "armpit"], circle(18.8, 13.6, 3.3),
       lambda S: L(S, _ARMPIT, _ARMPIT_R), aliases=["underarm"])
def _(S):
    return [shell(circle(8.8, 5, 2.75)), shell(L(S, _ARMPIT, _ARMPIT_R)), detail(seg(13.8, 10.5, 13.8, 14))]


_SHIN = ("M8.5 3H14.5C14.8 6.5 14.2 10.5 13.9 13.5L13.7 16.5L19 18C20.3 18.4 21 19.2 21 20.2V21H9.5C9.5 19.3 9.6 18 9.3 16.5"
         "C8.8 14 7 12.5 7 9C7 6.8 7.8 5 8.5 3Z")
_SHIN_R = ("M9.5 3H13.6Q14.6 3 14.6 4C14.6 7.3 14.2 10.8 13.9 13.5L13.7 16.5L19 18C20.3 18.4 21 19.2 21 20.2Q21 21 20.2 21H10.5"
           "Q9.5 21 9.5 20C9.5 18.8 9.6 17.7 9.3 16.5C8.8 14 7 12.5 7 9C7 7 7.6 5.5 8.3 4Q8.6 3 9.5 3Z")


@zicon("shin", "Lower leg in side view with the shin marked",
       ["shinbone", "tibia", "lower leg", "shin splints", "leg", "front of leg"], "M11.6 4.5H17V16H11.4Z",
       lambda S: L(S, _SHIN, _SHIN_R))
def _(S):
    return [shell(L(S, _SHIN, _SHIN_R))]


@zicon("forehead", "Front view of a face with the forehead marked",
       ["brow", "temple", "face", "upper face", "wrinkles", "forehead"], "M2 2H22V7.3H2Z", lambda S: FACE)
def _(S):
    brows = (L(S, seg(8, 10, 10.5, 10), arc(9.3, 11.3, 1.8, 225, 315)), L(S, seg(13.5, 10, 16, 10), arc(14.7, 11.3, 1.8, 225, 315)))
    return [shell(FACE), detail(brows[0]), detail(brows[1]), dot(9.3, 13), dot(14.7, 13), detail(seg(10.5, 17, 13.5, 17))]


@zicon("chin", "Head in profile with the chin marked",
       ["jaw", "chin", "face", "profile", "jawline", "double chin"], circle(18.8, 17.8, 3.2), head)
def _(S):
    return [shell(head(S)), dot(15, 8.8, 1.1)]


@icon("cheek", CAT, "Front view of a face with one cheek marked",
      tags=["cheeks", "face", "blush", "cheekbone", "skin", "rosy cheek"])
def _(S):
    return [shell(FACE), dot(9.3, 9.5), dot(14.7, 9.5), dot(14.2, 14.3, 1.9),
            detail(L(S, seg(9, 17.3, 11.5, 17.3), arc(10.2, 15.3, 2, 45, 135)))]


_SOLE = ("M7.5 11C7.5 9.2 9.6 8 12.5 8C15.6 8 17.5 9.6 17.5 12C17.5 14.8 16.5 16.4 16.5 18.5C16.5 20.3 15 21.5 13 21.5"
         "C11 21.5 9.5 20.3 9.5 18.6C9.5 16.8 10.7 15.8 10.7 14.3C10.7 12.7 7.5 12.8 7.5 11Z")
_SOLE_L = ("M7.5 11C7.5 9.2 9.6 8 12.5 8C15.6 8 17.5 9.6 17.5 12C17.5 14.8 16.5 16.4 16.5 18.5C16.5 20.3 15 21.5 13 21.5"
           "C11 21.5 9.5 20.3 9.5 18.6C9.5 16.8 10.7 15.8 10.7 14.3L7.5 11Z")


@icon("foot-sole", CAT, "Bottom of a bare foot with the heel, arch and toe pads",
      tags=["sole", "underfoot", "foot bottom", "plantar", "reflexology", "heel"], aliases=["sole"])
def _(S):
    return [shell(L(S, _SOLE_L, _SOLE)), detail(L(S, seg(11, 17.3, 15, 17.3), "M11 17.6C12.3 16.9 13.8 16.9 15 17.6")),
            dot(8.6, 4.3, 1.7), dot(12.3, 3.5, 1.2), dot(15.1, 4, 1.1), dot(17.5, 5.2, 1), dot(19.4, 7, 0.9)]


@icon("sense-of-touch", CAT, "Fingertip pressing on a surface with ripples around it",
      tags=["touch", "tactile", "feel", "sensation", "nerve", "fingertip", "senses"], aliases=["tactile"])
def _(S):
    return [line("M8.5 2V12.5A3.5 3.5 0 0 0 15.5 12.5V2"), line("M2 19H22"),
            line(arc(12, 19, 6, 315, 345)), line(arc(12, 19, 6, 195, 225)),
            line(arc(12, 19, 9.5, 312, 338)), line(arc(12, 19, 9.5, 202, 228))]


@icon("ear-nose-throat", CAT, "Head in profile with the ear, nose and airway marked",
      tags=["ent", "otolaryngology", "ear nose and throat", "airway", "sinus", "specialist"], aliases=["ent"])
def _(S):
    return [shell(head(S)), Part("dot", ellipse(10, 10.5, 1.6, 2.3)),
            detail(poly([(18.5, 12.2), (15, 12.2), (13, 14.5), (11, 16.5), (11, 21)], r=S.r))]


@icon("sensory-overload", CAT, "Small head in profile with zigzag signals pointing in from all sides",
      tags=["overstimulation", "overwhelmed", "sensory", "autism", "noise", "stress", "neurodivergent"],
      aliases=["overstimulation"])
def _(S):
    parts = [shell(small_head(S, 0.6, 4.4, 6.6))]
    for x0, y0, x1, y1 in ((2.5, 3, 6, 6.3), (12, 2, 12, 5), (21.5, 3, 18, 6.3), (2, 13.5, 5.5, 13.5),
                           (22, 13.5, 18.8, 13.5), (2.5, 21, 5.5, 18.5)):
        parts.append(line(poly(zigzag(x0, y0, x1, y1, 1, 0.8), r=min(S.r, 0.5))))
    return parts


# ============================================================================ bones and joints

_BONE = union(rect(5, 10.4, 14, 3.2), circle(4.3, 10.2, 2.1), circle(4.3, 13.8, 2.1), circle(19.7, 10.2, 2.1),
               circle(19.7, 13.8, 2.1))
_CRACK = poly([(10, 7), (11, 9.5), (9.6, 12), (11, 14.5), (10, 17), (14, 17), (15, 14.5), (13.6, 12), (15, 9.5), (14, 7)],
              closed=True)


@icon("broken-bone", CAT, "A long bone snapped in two with a jagged break",
      tags=["fracture", "broken", "bone", "injury", "orthopedic", "x-ray", "cast"], aliases=["fracture"])
def _(S):
    pieces = minus(_BONE, _CRACK)
    return [shell(rot(pieces, -45), stroke_miterlimit="2"),
            line(rot(seg(12, 4.5, 12, 7), -45)), line(rot(seg(12, 17, 12, 19.5), -45))]


_KNOB = ("M9.5 21V14.5C9.5 12.8 8.7 11.8 7.4 11C5.4 9.8 4.5 8.2 4.5 6.3C4.5 4.2 6.2 2.7 8.1 2.7C9.8 2.7 10.8 3.7 12 3.7"
         "C13.2 3.7 14.2 2.7 15.9 2.7C17.8 2.7 19.5 4.2 19.5 6.3C19.5 8.2 18.6 9.8 16.6 11C15.3 11.8 14.5 12.8 14.5 14.5V21Z")
_KNOB_R = ("M9.5 20V14.5C9.5 12.8 8.7 11.8 7.4 11C5.4 9.8 4.5 8.2 4.5 6.3C4.5 4.2 6.2 2.7 8.1 2.7C9.8 2.7 10.8 3.7 12 3.7"
           "C13.2 3.7 14.2 2.7 15.9 2.7C17.8 2.7 19.5 4.2 19.5 6.3C19.5 8.2 18.6 9.8 16.6 11C15.3 11.8 14.5 12.8 14.5 14.5V20"
           "Q14.5 21 13.5 21H10.5Q9.5 21 9.5 20Z")


@icon("osteoporosis", CAT, "End of a bone with large holes inside",
      tags=["bone density", "brittle bones", "porous bone", "bone loss", "fragile", "calcium", "aging"])
def _(S):
    return [shell(L(S, _KNOB, _KNOB_R)), dot(8.3, 6.2, 1.3), dot(12, 7.6, 1.3), dot(15.7, 6.2, 1.3),
            dot(12, 13.3, 1), dot(12, 17.8, 1)]


def _hand_outline(S):
    xs = [7.5, 10.9, 14.3, 17.7, 21.1]
    tops = [5.5, 3.5, 4.5, 7]
    d = ""
    seps = []
    for k, top in enumerate(tops):
        r = (xs[k + 1] - xs[k]) / 2
        y0 = top + r
        d += f"V{fmt(y0)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(xs[k + 1])} {fmt(y0)}"
        if k + 1 < len(tops):
            seps.append((xs[k + 1], max(y0, tops[k + 1] + r)))
    if S.name == "line":
        o = "M9 21C8 19.8 6.2 17.6 3.8 15.6A1.7 1.7 0 0 1 5.9 12.7L7.5 15" + d + "V15C21.1 18.3 19 21 16 21Z"
    else:
        o = "M10.5 21C9.3 21 8.5 20.4 7.8 19.4L3.8 15.6A1.7 1.7 0 0 1 5.9 12.7L7.5 15" + d + "V15C21.1 18.3 19 21 16 21Z"
    return o, seps


def hand(S, k=1.0, dx=0.0, dy=0.0, sep_to=12.5):
    """Open hand (palm forward) scaled and moved: (outline, finger separator segments)."""
    o, seps = _hand_outline(S)
    return tf(o, k, dx, dy), [tf(seg(x, y, x, sep_to), k, dx, dy) for x, y in seps]


@icon("arthritis", CAT, "Hand with swollen finger joints and ache lines",
      tags=["joint pain", "rheumatoid", "osteoarthritis", "stiff joints", "knuckles", "rheumatology", "inflammation"])
def _(S):
    o, seps = hand(S, 0.82, -1.3, 4)
    parts = [shell(o)] + [detail(s) for s in seps]
    parts += [dot(8.5, 11.3, 1.1), dot(11.4, 10.2, 1.1), dot(14.2, 10.7, 1.1)]
    parts += [line(seg(18.5, 5.5, 20.5, 3.5)), line(seg(15.5, 3.8, 16, 2)), line(seg(19.5, 9.2, 21.8, 8.8))]
    return parts


_FOOT = ("M6.5 3H11V11.8C11 13.1 11.9 14.2 13.2 14.6L18.6 16.2C20.1 16.7 21 17.8 21 19C21 20.2 20.2 21 19 21H16.8C15.3 21 14.6 20 12.7 20"
         "C10.8 20 10.2 21 8.5 21H6C4.8 21 4 20.2 4 19C4 17.5 5 16.4 5.8 15.4C6.3 14.7 6.5 14 6.5 13Z")
_FOOT_R = ("M7.5 3H10Q11 3 11 4V11.8C11 13.1 11.9 14.2 13.2 14.6L18.6 16.2C20.1 16.7 21 17.8 21 19C21 20.2 20.2 21 19 21H16.8C15.3 21 14.6 20 12.7 20"
           "C10.8 20 10.2 21 8.5 21H6C4.8 21 4 20.2 4 19C4 17.5 5 16.4 5.8 15.4C6.3 14.7 6.5 14 6.5 13V4Q6.5 3 7.5 3Z")


def foot(S):
    return L(S, _FOOT, _FOOT_R)


def wave(x, y0, y1, amp=0.8, n=2):
    """Vertical wavy line from (x, y0) up to (x, y1) with n S-bends."""
    h = (y1 - y0) / n
    d = f"M{fmt(x)} {fmt(y0)}"
    for i in range(n):
        ya = y0 + h * i
        d += (f"C{fmt(x - amp * 1.3)} {fmt(ya + h * 0.25)} {fmt(x - amp * 1.3)} {fmt(ya + h * 0.25)} {fmt(x)} {fmt(ya + h * 0.5)}"
              f"C{fmt(x + amp * 1.3)} {fmt(ya + h * 0.75)} {fmt(x + amp * 1.3)} {fmt(ya + h * 0.75)} {fmt(x)} {fmt(ya + h)}")
    return d


@zicon("gout", "Foot in side view with a swollen big toe joint and heat lines",
       ["big toe", "joint pain", "uric acid", "toe pain", "inflammation", "podiatry", "gouty arthritis"],
       circle(16.6, 17.6, 2.9), foot)
def _(S):
    return [shell(foot(S)), line(wave(14.5, 11.5, 5, 1, 1)), line(wave(18.5, 13, 6.5, 1, 1))]


_BUNION = ("M6.2 11.2C5.6 9.9 6.5 8.8 8 8.6C9.3 8.1 10.8 8 12.5 8C15.6 8 17.5 9.6 17.5 12C17.5 14.8 16.5 16.4 16.5 18.5"
           "C16.5 20.3 15 21.5 13 21.5C11 21.5 9.5 20.3 9.5 18.6C9.5 16.8 10.7 15.8 10.7 14.3C10.7 13 7 12.8 6.2 11.2Z")
_BUNION_L = ("M6.2 11.2C5.6 9.9 6.5 8.8 8 8.6C9.3 8.1 10.8 8 12.5 8C15.6 8 17.5 9.6 17.5 12C17.5 14.8 16.5 16.4 16.5 18.5"
             "C16.5 20.3 15 21.5 13 21.5C11 21.5 9.5 20.3 9.5 18.6C9.5 16.8 10.7 15.8 10.7 14.3L6.2 11.2Z")


@zicon("bunion", "Foot seen from above with the big toe bent inward and a bump at its base",
       ["hallux valgus", "big toe", "toe bump", "foot pain", "podiatry", "bunion"], circle(6, 10.5, 2.5),
       lambda S: L(S, _BUNION_L, _BUNION))
def _(S):
    toe = rot(ellipse(9.8, 4.1, 1.35, 2.2), 32, 9.8, 4.1)
    return [shell(L(S, _BUNION_L, _BUNION)), Part("dot", toe),
            dot(13.4, 3.6, 1.2), dot(15.9, 4.3, 1.1), dot(18, 5.6, 1), dot(19.7, 7.4, 0.9)]


@icon("scoliosis", CAT, "Back of a torso with the spine curving sideways in an S shape",
      tags=["spine curve", "curved spine", "back", "posture", "vertebrae", "orthopedic", "spinal"])
def _(S):
    pts = [(12 + 2.2 * math.sin(2 * math.pi * i / 30), 7.5 + 11.5 * i / 30) for i in range(31)]
    return torso(S) + [detail(poly(pts))]


def _vert(S, y):
    return poly([(8.5, y), (15.5, y), (19, y + 1.75), (15.5, y + 3.5), (8.5, y + 3.5), (5, y + 1.75)], closed=True, r=min(S.r, 1))


@icon("herniated-disc", CAT, "Two vertebrae with the disc between them bulging out past their edge",
      tags=["slipped disc", "disc herniation", "back pain", "spine", "sciatica", "vertebrae", "bulging disc"],
      aliases=["slipped-disc"])
def _(S):
    return [shell(_vert(S, 3), stroke_miterlimit="2"), shell(_vert(S, 17.5), stroke_miterlimit="2"),
            line(seg(6.5, 12, 15.5, 12)), dot(19, 12, 2.3)]


# ============================================================================ feet, muscles and joints

def zig(pts, S):
    return line(poly(pts, r=min(S.r, 0.5)))


@icon("muscle-cramp", CAT, "Lower leg with a knotted calf muscle and zigzag pain marks",
      tags=["cramp", "charley horse", "calf cramp", "muscle spasm", "leg cramp", "pain", "spasm"],
      aliases=["charley-horse"])
def _(S):
    leg = tf(L(S, _SHIN, _SHIN_R), 0.9, 3, 1.5)
    return [shell(leg), Part("dot", circle(12.3, 10.3, 1.5)),
            zig(zigzag(2.5, 6.5, 6.8, 8.5, 1, 0.9), S), zig(zigzag(2.2, 12.5, 6.8, 12.5, 1, 0.9), S)]


_FEMUR = ("M9 2V6C7.2 6.3 6.5 7.3 6.5 8.3C6.5 9.3 7.3 10 8.3 10C9.8 10 10.5 9.4 12 9.4C13.5 9.4 14.2 10 15.7 10"
          "C16.7 10 17.5 9.3 17.5 8.3C17.5 7.3 16.8 6.3 15 6V2Z")
_TIBIA = "M6.5 15.5C6.5 14.6 7.2 14 8 14H16C16.8 14 17.5 14.6 17.5 15.5C17.5 16.6 16.5 17.3 15 17.6V22H9V17.6C7.5 17.3 6.5 16.6 6.5 15.5Z"


@icon("torn-ligament", CAT, "Knee bones with the ligament on one side torn apart",
      tags=["ligament tear", "acl", "sprain", "knee injury", "torn", "sports injury", "rupture"],
      aliases=["ligament-tear"])
def _(S):
    return [shell(L(S, _FEMUR, _FEMUR)), shell(_TIBIA),
            line(seg(3.8, 7, 3.8, 17)),
            line(seg(20.2, 6.5, 20.2, 10.3)),
            line(poly([(20.2, 17.5), (20.2, 13.7)])),
            line(seg(18.6, 11.8, 19.4, 10.8)), line(seg(21.8, 11.8, 21, 10.8)),
            line(seg(18.6, 12.2, 19.4, 13.2)), line(seg(21.8, 12.2, 21, 13.2))]


def arrow(x0, y0, x1, y1, S, head=1.6):
    """Short arrow from (x0, y0) pointing to (x1, y1)."""
    a = math.atan2(y1 - y0, x1 - x0)
    l = (x1 - head * math.cos(a - 0.8), y1 - head * math.sin(a - 0.8))
    r = (x1 - head * math.cos(a + 0.8), y1 - head * math.sin(a + 0.8))
    return [line(seg(x0, y0, x1 - 0.3 * math.cos(a), y1 - 0.3 * math.sin(a))), line(poly([l, (x1, y1), r], r=min(S.r, 0.5)))]


@icon("swelling", CAT, "Puffy hand with arrows pointing outward from its edge",
      tags=["swollen", "edema", "oedema", "inflammation", "puffy", "fluid retention", "swollen hand"],
      aliases=["edema"])
def _(S):
    o, seps = hand(S, 0.72, 2.2, 6.4)
    return [shell(o)] + [detail(s) for s in seps] + arrow(4, 11, 1.8, 8.8, S) + arrow(12, 4.2, 12, 1.5, S) + arrow(19.2, 8.5, 21.6, 6.3, S)


@icon("hand-tremor", CAT, "Hand held up with shake marks on both sides",
      tags=["tremor", "shaking hand", "shaky", "parkinson's", "essential tremor", "trembling", "shake"],
      aliases=["tremor"])
def _(S):
    o, seps = hand(S, 0.58, 5.4, 6.3)
    return ([shell(o)] + [detail(s) for s in seps] +
            [line(arc(12, 13, 8.2, 155, 205)), line(arc(12, 13, 8.2, -25, 25)),
             line(arc(12, 13, 10.8, 165, 195)), line(arc(12, 13, 10.8, -15, 15))])


def star4(cx, cy, r, k=0.3):
    pts = []
    for i in range(8):
        rr = r if i % 2 == 0 else r * k
        pts.append(polar(cx, cy, rr, -90 + i * 45))
    return poly(pts, closed=True)


def sparkle(cx, cy, r):
    return [solid(star4(cx, cy, r))]


@icon("tingling", CAT, "Hand with sparkle marks around the fingertips, like pins and needles",
      tags=["pins and needles", "numbness", "paresthesia", "tingle", "neuropathy", "prickling", "nerve"],
      aliases=["pins-and-needles"])
def _(S):
    o, seps = hand(S, 0.72, 2.2, 6.4)
    return [shell(o)] + [detail(s) for s in seps] + sparkle(4.2, 5.2, 2.6) + sparkle(19.8, 4.6, 2.6) + [dot(12.2, 2.5, 1.1), dot(21, 10.5, 1), dot(2.8, 11, 1)]


# ============================================================================ symptoms: whole body and head

def spiral_eye(cx, cy, S):
    return detail(arc(cx, cy, 2, 0, 270) if S.name == "line" else arc(cx, cy, 2, 20, 290))


@icon("dizziness", CAT, "Face with swirling eyes and a small open mouth",
      tags=["dizzy", "vertigo", "lightheaded", "spinning", "woozy", "balance", "disoriented"],
      aliases=["vertigo"])
def _(S):
    return [shell(circle(12, 12, 9)), spiral_eye(8.6, 10.5, S), spiral_eye(15.4, 10.5, S),
            detail(L(S, ellipse(12, 16.3, 1.6, 1.2), ellipse(12, 16.3, 1.4, 1.4)))]


def snowflake(cx, cy, r, S):
    return [line(seg(*polar(cx, cy, r, a), *polar(cx, cy, r, a + 180))) for a in (90, 30, 150)]


@icon("chills", CAT, "Person wrapped in a blanket, shaking, with a snowflake above",
      tags=["shivering", "cold", "fever", "shiver", "flu", "freezing", "blanket"])
def _(S):
    blanket = L(S, "M10.5 10.5C6.8 10.5 5.3 12.8 4.9 15.5L4 21H17L16.1 15.5C15.7 12.8 14.2 10.5 10.5 10.5Z",
                "M10.5 10.5C6.8 10.5 5.3 12.8 4.9 15.5L4.2 20Q4 21 5 21H16Q17 21 16.8 20L16.1 15.5C15.7 12.8 14.2 10.5 10.5 10.5Z")
    return ([shell(circle(10.5, 6.2, 2.8)), shell(blanket), detail(seg(11.2, 10.8, 8.8, 21))] +
            [line(arc(10.5, 16, 8.5, 160, 200)), line(arc(10.5, 16, 8.5, -20, 20))] + snowflake(19.5, 4.5, 2.6, S))


_DROP = ("M12 2.5C12 2.5 18.5 9.8 18.5 14.5A6.5 6.5 0 0 1 5.5 14.5C5.5 9.8 12 2.5 12 2.5Z")
_DROP_R = "M11.1 3.5Q12 2.5 12.9 3.5C14.5 5.4 18.5 10.3 18.5 14.5A6.5 6.5 0 0 1 5.5 14.5C5.5 10.3 9.5 5.4 11.1 3.5Z"


def drop(S, k, dx, dy):
    return tf(L(S, _DROP, _DROP_R), k, dx, dy)


@icon("dehydration", CAT, "Head in profile beside a water drop that is almost empty",
      tags=["dehydrated", "thirst", "thirsty", "fluids", "hydration", "water", "dry mouth"], aliases=["thirst"])
def _(S):
    return [shell(small_head(S, 0.72, 0, 6.3)), shell(drop(S, 0.5, 12, 0.8), stroke_miterlimit="8"),
            detail(seg(16.8, 9.3, 19.2, 9.3))]


@icon("heatstroke", CAT, "Head in profile under a blazing sun with a sweat drop",
      tags=["heat stroke", "sunstroke", "heat exhaustion", "hot", "heatwave", "overheating", "sun"],
      aliases=["sunstroke"])
def _(S):
    parts = [shell(small_head(S, 0.72, 0, 6.3)), shell(circle(18.2, 5.3, 2.1)),
             Part("dot", drop(S, 0.26, 13.6, 8.8))]
    for a in range(0, 360, 45):
        parts.append(line(seg(*polar(18.2, 5.3, 3.5, a), *polar(18.2, 5.3, 4.6, a))))
    return parts


def fingers(xs, tops, bottom=21.0):
    d = f"M{fmt(xs[0])} {fmt(bottom)}"
    seps = []
    for k, top in enumerate(tops):
        r = (xs[k + 1] - xs[k]) / 2
        y0 = top + r
        d += f"V{fmt(y0)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(xs[k + 1])} {fmt(y0)}"
        if k + 1 < len(tops):
            seps.append((xs[k + 1], max(y0, tops[k + 1] + r)))
    return d + f"V{fmt(bottom)}Z", seps


@zicon("frostbite", "Hand with darkened fingertips and a snowflake beside it",
       ["frostbitten", "frozen fingers", "cold injury", "freezing", "winter", "numb fingers", "chilblains"],
       "M0 0H24V10.3H0Z", lambda S: hand(S, 0.8, -0.2, 4)[0])
def _(S):
    o, seps = hand(S, 0.8, -0.2, 4)
    return [shell(o)] + [detail(x) for x in seps] + snowflake(20.3, 4.6, 2.4, S)


def virus(cx, cy, r, spike):
    parts = [shell(circle(cx, cy, r))]
    for a in range(0, 360, 60):
        parts.append(line(seg(*polar(cx, cy, r + 0.5, a), *polar(cx, cy, r + spike, a))))
    return parts


@icon("contagion", CAT, "Two heads facing each other with a germ passing between them",
      tags=["contagious", "infection", "spread", "transmission", "germs", "cross infection", "catching"],
      aliases=["infection-spread"])
def _(S):
    return [shell(small_head(S, 0.5, -0.5, 11.3)), shell(small_head(S, 0.5, 24.5, 11.3, flip=True))] + virus(12, 6.2, 2, 1.9)


@icon("headache", CAT, "Face with jagged pain lines around the temples",
      tags=["head pain", "tension headache", "sore head", "pain", "ache", "stress", "painkiller"])
def _(S):
    return [shell(circle(12, 13.5, 7)),
            detail(L(S, seg(8.3, 12.3, 10.5, 13), "M8.3 12.3L10.5 13")), detail(L(S, seg(15.7, 12.3, 13.5, 13), "M15.7 12.3L13.5 13")),
            detail(L(S, seg(10, 17.3, 14, 17.3), arc(12, 19.3, 2.2, 230, 310))),
            zig(zigzag(2.5, 3, 5.8, 7, 1, 0.9), S), zig(zigzag(21.5, 3, 18.2, 7, 1, 0.9), S), line(seg(12, 1.8, 12, 4.3))]


_TOOTH = ("M7 3.5C4.5 3.5 3.5 5.5 3.5 8C3.5 11 5 13 6 15L7.5 21L10.5 14L13.5 14L16.5 21L18 15C19 13 20.5 11 20.5 8"
          "C20.5 5.5 19.5 3.5 17 3.5C15 3.5 14 4.5 12 4.5C10 4.5 9 3.5 7 3.5Z")
_TOOTH_R = ("M7 3.5C4.5 3.5 3.5 5.5 3.5 8C3.5 11 5 13 6 15L7 20C7.3 21 8.7 21 9 20L10.5 14.5C10.8 13.5 13.2 13.5 13.5 14.5L15 20"
            "C15.3 21 16.7 21 17 20L18 15C19 13 20.5 11 20.5 8C20.5 5.5 19.5 3.5 17 3.5C15 3.5 14 4.5 12 4.5C10 4.5 9 3.5 7 3.5Z")


def tooth(S):
    return L(S, _TOOTH, _TOOTH_R)


@icon("toothache", CAT, "Tooth with jagged pain lines around it",
      tags=["tooth pain", "dental pain", "sore tooth", "dentist", "ache", "dental", "molar"])
def _(S):
    return [shell(tf(tooth(S), 0.72, 0, 4.9)),
            zig(zigzag(15.5, 7.5, 20, 3, 1, 0.9), S), zig(zigzag(17.5, 11.5, 22, 10.5, 1, 0.9), S),
            zig(zigzag(10.3, 6, 11.5, 2.5, 1, 0.7), S)]


def ear(ox, oy, s):
    X = lambda v: fmt(ox + s * v)  # noqa: E731
    Y = lambda v: fmt(oy + s * v)  # noqa: E731
    outer = (f"M{X(7)} {Y(9)}C{X(7)} {Y(5.7)} {X(9.5)} {Y(3)} {X(13)} {Y(3)}C{X(16.5)} {Y(3)} {X(19)} {Y(5.7)} {X(19)} {Y(9)}"
             f"C{X(19)} {Y(11.8)} {X(17.5)} {Y(13)} {X(16.3)} {Y(14.5)}C{X(15.3)} {Y(15.8)} {X(15.2)} {Y(17.5)} {X(14.4)} {Y(19)}"
             f"C{X(13.5)} {Y(20.7)} {X(11)} {Y(21.5)} {X(9)} {Y(20)}")
    inner = (f"M{X(10.8)} {Y(9.5)}C{X(10.8)} {Y(8)} {X(11.8)} {Y(7)} {X(13)} {Y(7)}C{X(14.3)} {Y(7)} {X(15.2)} {Y(8)} {X(15.2)} {Y(9.2)}"
             f"C{X(15.2)} {Y(10.8)} {X(13.8)} {Y(11.4)} {X(13.1)} {Y(12.8)}")
    return outer, inner


@icon("earache", CAT, "Ear with jagged pain lines coming from it",
      tags=["ear pain", "ear infection", "otitis", "sore ear", "ache", "ent", "ear"])
def _(S):
    o, i = ear(-3.9, 0.8, 0.88)
    return [line(o), line(i), zig(zigzag(14.8, 6, 19.5, 3, 1, 0.9), S), zig(zigzag(16, 10.5, 21.5, 10.5, 1, 0.9), S),
            zig(zigzag(14.8, 15, 19.5, 18, 1, 0.9), S)]


# ============================================================================ symptoms: nose, mouth and throat

@icon("sore-throat", CAT, "Head and neck with a burst of pain on the throat",
      tags=["throat pain", "strep throat", "pharyngitis", "tonsillitis", "scratchy throat", "cold", "flu"],
      aliases=["throat-pain"])
def _(S):
    return [shell(ellipse(12, 5.6, 4.2, 3.7)),
            line(L(S, "M7.8 9.8V13.5C7.8 15 6.8 15.8 5.3 16.2C3.8 16.7 3 18 3 21", "M7.8 9.8V13.5C7.8 15 6.8 15.8 5.3 16.2C3.8 16.7 3 18 3 21")),
            line("M16.2 9.8V13.5C16.2 15 17.2 15.8 18.7 16.2C20.2 16.7 21 18 21 21"),
            solid(star(12, 14.2, 2.9, 6, 0.45))]


_NOSE = "M8 2C9.2 5.2 11.5 8.8 15.8 11.8C16.8 12.5 16.5 14 15.3 14H12.5"


@icon("runny-nose", CAT, "Head in profile with a drip falling from the nose",
      tags=["runny", "cold", "sniffles", "mucus", "allergy", "hay fever", "flu", "snot"], aliases=["sniffles"])
def _(S):
    return [shell(small_head(S, 0.85, -0.8, 1)), shell(drop(S, 0.3, 15.6, 13.3), stroke_miterlimit="8")]


@icon("nosebleed", CAT, "Nose seen from the front with drops of blood falling from one nostril",
      tags=["nose bleed", "epistaxis", "bleeding nose", "blood", "first aid", "injury"], aliases=["epistaxis"])
def _(S):
    return [line("M10 2.5C10 5.8 9.4 8.3 8 10.6C6.9 12.4 6.2 13.9 6.9 15.2C7.6 16.5 9.5 16.6 10.4 15.4C11.1 16.2 12.9 16.2 13.6 15.4"
                 "C14.5 16.6 16.4 16.5 17.1 15.2C17.8 13.9 17.1 12.4 16 10.6C14.6 8.3 14 5.8 14 2.5"),
            Part("dot", drop(S, 0.3, 11.3, 16.8)), Part("dot", drop(S, 0.22, 15, 18.2))]


_BUST = "M3 21V17C3 13.7 5.7 11.5 9 11.5H15C18.3 11.5 21 13.7 21 17V21Z"
_BUST_R = "M5 21Q3 21 3 19V17C3 13.7 5.7 11.5 9 11.5H15C18.3 11.5 21 13.7 21 17V19Q21 21 19 21Z"


def bust(S):
    return L(S, _BUST, _BUST_R)


# ============================================================================ symptoms: organs

_LUNG = "M10 8C7.2 8 4 12 3.5 16.5C3.2 19 4.5 20.7 7 20.2L9.5 19.7C10.2 19.5 10.5 19 10.5 18.3V8.8C10.5 8.3 10.4 8 10 8Z"
_LUNG_R = _LUNG


def lungs_d(k=1.0, dx=0.0, dy=0.0):
    left = _LUNG
    right = tf(_LUNG, 1, 24, 0, sx=-1)
    return tf(left, k, dx, dy), tf(right, k, dx, dy)


@icon("smoker-lungs", CAT, "Pair of lungs with dark spots and a cigarette with a curl of smoke",
      tags=["smoking", "smoker", "tobacco", "lung damage", "cigarette", "lung disease", "quit smoking"],
      aliases=["smokers-lungs"])
def _(S):
    a, b = lungs_d(0.78, -1.2, -1.2)
    cig = rect(9, 18, 12.5, 3, min(S.R, 1))
    return [shell(a), shell(b), line(tf("M12 3V10.5M12 10.5L10.5 12M12 10.5L13.5 12", 0.78, -1.2, -1.2)),
            dot(4.6, 12.3, 1.1), dot(6.3, 9.3, 1), dot(11.5, 12.3, 1.1), dot(9.9, 9.3, 1),
            shell(cig), detail(seg(12.5, 18.5, 12.5, 20.5)), line("M20.5 15.5C18.5 14.5 21.5 12 19.5 10.5C18.6 9.8 18.3 8.8 19 7.8")]


_LUNGS_2 = "".join(lungs_d())


@zicon("pneumonia", "Pair of lungs with cloudy patches filling their lower parts",
       ["lung infection", "chest infection", "pneumonitis", "respiratory", "lungs", "cough", "x-ray"],
       "M0 24V16.3C1.5 14.8 3.5 14.8 5 16.3C6.5 14.8 8.5 14.8 10 16.3H14C15.5 14.8 17.5 14.8 19 16.3C20.5 14.8 22.5 14.8 24 16.3V24Z",
       lambda S: _LUNGS_2)
def _(S):
    a, b = lungs_d()
    return [shell(a), shell(b), line("M12 3V10.5M12 10.5L10.5 12M12 10.5L13.5 12")]


_HEART = ("M7 9.5C8.3 8.3 10 8 11.5 8.8C13.3 7.3 16.3 7.3 18.3 9.3C20.8 11.8 20.6 16.3 17.8 19.1C15.8 21.1 12.5 21.5 10 20.2"
          "C6.5 18.4 4.8 14.5 5.3 11.8C5.5 10.8 6.2 10.2 7 9.5Z")


def bolt(x, y, k=1.0):
    pts = [(1.5, 0), (-2, 5), (0.3, 5), (-1.3, 9.5), (3, 3.5), (0.7, 3.5), (2.8, 0)]
    return poly([(x + k * px, y + k * py) for px, py in pts], closed=True)


@icon("heart-attack", CAT, "Anatomical heart with a lightning bolt beside it",
      tags=["cardiac arrest", "myocardial infarction", "chest pain", "heart disease", "cardiology", "emergency", "heart"],
      aliases=["cardiac-arrest"])
def _(S):
    k, dx, dy = 0.85, -2.3, 2.6
    return [shell(tf(_HEART, k, dx, dy)), line(tf("M9.5 8.3V3.5", k, dx, dy)),
            line(tf("M13 7.9V5.5A2.5 2.5 0 0 1 18 5.5V6.5", k, dx, dy)),
            Part("solid", bolt(18.3, 1.5, 1.1)),
            detail(tf("M12.5 12C12.3 14.5 13.5 16.5 16 18", k, dx, dy))]


_BRAIN = ("M6.5 17C4.3 16.6 3 14.8 3 12.8C3 11.3 3.6 10.2 4.5 9.5C4.3 6.6 6.4 4.5 9 4.5C10.2 3.6 11.5 3.2 13 3.3C15.3 3.4 17 4.6 17.8 6.3"
          "C19.9 7 21 8.8 21 10.8C21 13.3 19.2 15.2 16.8 15.4C16.3 16.8 15 17.7 13.5 17.7L13.5 21H11V17.2Z")


def star(cx, cy, r, n=6, k=0.5, start=-90):
    return poly([polar(cx, cy, r if i % 2 == 0 else r * k, start + i * 180 / n) for i in range(2 * n)], closed=True)


@icon("stroke", CAT, "Brain with a burst blood spot and a crack in one area",
      tags=["brain attack", "cerebrovascular", "brain bleed", "hemorrhage", "neurology", "fast", "brain"],
      aliases=["brain-attack"])
def _(S):
    return [shell(_BRAIN), Part("dot", star(14.2, 9.6, 3, 7, 0.5)),
            detail(poly([(6.5, 8.5), (8.5, 10.5), (7.3, 12), (9.5, 14)], r=min(S.r, 0.5)))]


@icon("epilepsy", CAT, "Head in profile with a lightning bolt inside the brain area",
      tags=["seizure", "epileptic", "convulsion", "neurology", "brain", "fit", "neurological"], aliases=["seizure"])
def _(S):
    return [shell(head(S)), Part("dot", bolt(10.3, 4.8, 1.25))]


@icon("concussion", CAT, "Head in profile with a bump on top and stars around it",
      tags=["head injury", "brain injury", "knocked out", "bump", "tbi", "dazed", "sports injury"])
def _(S):
    h = path_to_d(U(P(small_head(S, 0.8, 1.6, 4.4)), P(circle(11, 6.4, 1.9))))
    return [shell(h), solid(star4(3.8, 4.5, 2.6)), solid(star4(18.5, 3.8, 2.6)), dot(21, 8.5, 1)]


_STOMACH = ("M8 3H11V6C11 7.5 11.8 8.5 13 8.7C14 8.9 15 8.5 15.8 7.7C17.8 5.9 21 7.3 21 10.5C21 16 17 20.5 11.5 20.5C9.8 20.5 8.2 20 7 19"
            "L5 21.2L3.2 19.5L5.5 17.2C4.8 15.3 5.3 13 7 11.5C7.7 10.8 8 10 8 9Z")


@icon("stomach-ache", CAT, "Stomach with jagged pain lines beside it",
      tags=["stomachache", "tummy ache", "abdominal pain", "belly ache", "cramps", "indigestion", "gastric"],
      aliases=["tummy-ache"])
def _(S):
    k, dx, dy = 0.8, -1.3, 3
    return [shell(tf(_STOMACH, k, dx, dy), stroke_miterlimit="2"), detail(tf("M11.5 16.5C14.8 16.5 17 14.3 17.5 11", k, dx, dy)),
            zig(zigzag(17.5, 5, 21.5, 2.8, 1, 0.8), S), zig(zigzag(18.3, 11.5, 22, 11.5, 1, 0.8), S),
            zig(zigzag(17.5, 18, 21.5, 20.2, 1, 0.8), S)]


_FLAME = "M12 22C8.1 22 5.5 19.4 5.5 15.8C5.5 12.9 7.2 11.3 8.3 9.3C8.6 10.9 9.3 12 10.4 12.5C10.2 8.3 12.4 4.8 15.3 2.8C15.2 6.2 18.5 8.7 18.5 14.7C18.5 19 15.9 22 12 22Z"
_FLAME_R = _FLAME


@icon("heartburn", CAT, "Stomach and gullet with a flame rising beside the gullet",
      tags=["acid reflux", "reflux", "gerd", "indigestion", "burning", "acid", "antacid"], aliases=["acid-reflux"])
def _(S):
    k, dx, dy = 0.8, 5, 3.4
    return [shell(tf(_STOMACH, k, dx, dy), stroke_miterlimit="2"), detail(tf("M11.5 16.5C14.8 16.5 17 14.3 17.5 11", k, dx, dy)),
            shell(tf(_FLAME, 0.52, -1, 1.5), stroke_miterlimit="2")]


@icon("nausea", CAT, "Face with closed eyes and a wavy queasy mouth",
      tags=["nauseous", "queasy", "sick", "motion sickness", "morning sickness", "unwell", "green"],
      aliases=["queasy"])
def _(S):
    return [shell(circle(12, 12, 9)),
            detail(L(S, "M6.8 10H10.2", arc(8.5, 11.5, 1.8, 220, 320))), detail(L(S, "M13.8 10H17.2", arc(15.5, 11.5, 1.8, 220, 320))),
            detail(poly(zigzag(7.5, 16, 16.5, 16, 2, 0.9), r=min(S.r, 0.6)))]


@icon("vomiting", CAT, "Head in profile with a stream from the mouth into a bowl",
      tags=["vomit", "throw up", "being sick", "puke", "nausea", "stomach bug", "food poisoning"],
      aliases=["throwing-up"])
def _(S):
    bowl = L(S, "M11.5 16.5H22.5C22.5 19.3 20.2 21.5 17 21.5C13.8 21.5 11.5 19.3 11.5 16.5Z",
             "M12.5 16.5H21.5Q22.5 16.5 22.4 17.5C22 19.8 19.8 21.5 17 21.5C14.2 21.5 12 19.8 11.6 17.5Q11.5 16.5 12.5 16.5Z")
    return [shell(small_head(S, 0.62, -0.5, 0.2)), shell(bowl),
            line("M13.5 9.7C16 10.2 17.5 11.5 17.5 14"), dot(15.3, 13.2, 0.9)]


_KIDNEY = ("M10 3C6.3 3 4 6.5 4 10.5C4 14.8 6.6 18 10 18C12 18 13 16.8 12.7 15.3C12.4 14 11.3 13.2 11.3 11.3C11.3 9.8 12.5 8.8 12.8 7.5"
           "C13.3 5 12.3 3 10 3Z")


@icon("kidney-stone", CAT, "Kidney with a small jagged stone lodged in its drainage tube",
      tags=["renal stone", "kidney stones", "urology", "calculus", "renal colic", "kidney pain", "ureter"],
      aliases=["renal-stone"])
def _(S):
    stone = poly([(17.2, 14.2), (19.3, 15.4), (19.6, 17.8), (17.8, 19.6), (15.4, 19.1), (14.6, 16.5)], closed=True,
                 r=min(S.r, 0.6))
    return [shell(_KIDNEY), line("M11.4 11.2H14C15.4 11.2 16.5 12.3 16.5 13.7V21.5"), Part("solid", stone)]


# ============================================================================ blood vessels

@icon("clogged-artery", CAT, "Artery with plaque built up on its walls, narrowing the channel",
      tags=["atherosclerosis", "plaque", "blocked artery", "cholesterol", "heart disease", "artery", "cardiovascular"],
      aliases=["atherosclerosis"])
def _(S):
    top = inter(union(circle(8.5, 4, 3.8), circle(12.5, 4, 6.2), circle(16.8, 4, 3.4)), "M0 5H24V24H0Z")
    bot = inter(union(circle(7.8, 20, 3.2), circle(11.3, 20, 6.2), circle(15.8, 20, 4.3)), "M0 0H24V19H0Z")
    return [line(seg(2, 4.5, 22, 4.5)), line(seg(2, 19.5, 22, 19.5)), solid(top), solid(bot), dot(3.8, 12, 1.3), dot(20.2, 12, 1.3)]


@icon("blood-clot", CAT, "Blood vessel with a lumpy clot blocking the inside",
      tags=["thrombosis", "clot", "dvt", "embolism", "blood vessel", "thrombus", "circulation"], aliases=["thrombus"])
def _(S):
    lump = union(circle(10.2, 10.6, 2.8), circle(14, 10.4, 2.6), circle(13.3, 13.8, 2.7), circle(9.9, 13.6, 2.5))
    return [line(seg(2, 4.5, 22, 4.5)), line(seg(2, 19.5, 22, 19.5)), shell(lump),
            dot(10.3, 10.8, 1.1), dot(13.6, 13.3, 1.1), dot(4, 12, 1.4), dot(20, 12, 1.4)]


@icon("varicose-veins", CAT, "Lower leg with bulging twisted veins running down the calf",
      tags=["varicose", "spider veins", "veins", "leg veins", "circulation", "vascular", "venous"])
def _(S):
    leg = L(S, _SHIN, _SHIN_R)
    return [shell(leg), detail(L(S, "M11 5C9.6 6.5 12.2 7.8 10.8 9.4C9.5 10.8 12 12.2 11.3 14", "M11 5C9.6 6.5 12.2 7.8 10.8 9.4C9.5 10.8 12 12.2 11.3 14"))]


# ============================================================================ skin

def forearm(S, dy=0.0):
    """Forearm held level, ending in a loose fist on the right; the free area is x 3.5-12.5 around y 13 + dy."""
    d = L(S, "M2 9H12.5C13.6 9 14.3 8.5 15 7.7L16.4 6.1C17 5.4 18 5.4 18.5 6C19 6.6 18.9 7.4 18.4 8L17.2 9.6H20.2"
             "C21.2 9.6 22 10.4 22 11.4V14.2C22 15.3 21.1 16.2 20 16.2H14.5C13.8 16.2 13.3 17 12.5 17H2Z",
          "M3 9H12.5C13.6 9 14.3 8.5 15 7.7L16.4 6.1C17 5.4 18 5.4 18.5 6C19 6.6 18.9 7.4 18.4 8L17.2 9.6H20.2"
          "C21.2 9.6 22 10.4 22 11.4V14.2C22 15.3 21.1 16.2 20 16.2H14.5C13.8 16.2 13.3 17 12.5 17H3Q2 17 2 16V10Q2 9 3 9Z")
    return tf(d, 1, 0, dy), [tf(seg(17.5, 12.9, 22, 12.9), 1, 0, dy)]


def arm_parts(S, dy=0.0):
    o, fs = forearm(S, dy)
    return [shell(o)] + [detail(f) for f in fs]


@icon("rash", CAT, "Forearm with a patch of small dots and itch lines",
      tags=["skin rash", "hives", "eczema", "dermatitis", "allergic reaction", "itchy", "dermatology"])
def _(S):
    return arm_parts(S) + [dot(4.9, 12, 0.95), dot(7.3, 14.2, 0.95), dot(9.7, 12, 0.95), dot(12, 14.2, 0.95),
                           line(seg(4.5, 3.5, 5.5, 6)), line(seg(8.5, 3, 8.5, 5.8)), line(seg(12.5, 3.5, 11.5, 6))]


@icon("bruise", CAT, "Forearm with an irregular round blotch",
      tags=["bruising", "contusion", "black and blue", "injury", "bump", "hematoma", "skin"], aliases=["contusion"])
def _(S):
    blot = union(circle(7.8, 13, 2.2), circle(9.6, 12.2, 1.7), circle(9.4, 14, 1.5), circle(6.4, 12.3, 1.3))
    return arm_parts(S) + [Part("dot", blot)]


@icon("scar", CAT, "Forearm with a long healed line and small ladder marks across it",
      tags=["scarring", "healed wound", "stitches", "scar tissue", "surgery scar", "keloid", "skin"])
def _(S):
    return arm_parts(S) + [detail(seg(3.8, 13, 12.2, 13))] + [detail(seg(x, 11.2, x, 14.8)) for x in (5.5, 8, 10.5)]


@icon("wound", CAT, "Forearm with an open gash and drops of blood below it",
      tags=["cut", "injury", "laceration", "bleeding", "gash", "first aid", "trauma"], aliases=["cut"])
def _(S):
    gash = L(S, "M4 10.5C6.5 9.3 9.5 9.3 12 10.5C9.5 11.7 6.5 11.7 4 10.5Z", "M4.3 10.4C6.7 9.4 9.3 9.4 11.7 10.4Q12 10.5 11.7 10.6C9.3 11.6 6.7 11.6 4.3 10.6Q4 10.5 4.3 10.4Z")
    return arm_parts(S, -3) + [detail(gash), Part("dot", drop(S, 0.26, 3.7, 16.2)), Part("dot", drop(S, 0.21, 8.2, 18))]


@icon("burn-injury", CAT, "Hand with a blistered patch and a flame above it",
      tags=["burn", "scald", "burned hand", "first aid", "fire injury", "heat", "skin burn"], aliases=["scald"])
def _(S):
    o, seps = hand(S, 0.72, -0.4, 6.4)
    return [shell(o)] + [detail(s) for s in seps] + [dot(8.3, 17.3, 1.3), dot(11.3, 18.6, 1),
                                                     shell(tf(_FLAME, 0.55, 10.8, -0.5), stroke_miterlimit="2")]


@icon("animal-bite", CAT, "Forearm with an oval ring of small tooth marks",
      tags=["dog bite", "bite", "bite marks", "rabies", "injury", "tooth marks", "pet"], aliases=["dog-bite"])
def _(S):
    parts = arm_parts(S)
    for a in (200, 245, 295, 340, 20, 65, 115, 160):
        x, y = polar(8, 13, 1, a)
        parts.append(dot(8 + 4.2 * math.cos(math.radians(a)), 13 + 2.2 * math.sin(math.radians(a)), 0.8))
    return parts


@icon("splinter", CAT, "Fingertip with a thin wooden sliver stuck into the skin",
      tags=["sliver", "wood splinter", "tweezers", "first aid", "finger", "thorn"], aliases=["sliver"])
def _(S):
    nail = L(S, "M9.5 11V8.5A2.5 2.5 0 0 1 14.5 8.5V11Z", "M11 11Q9.5 11 9.5 9.5V8.5A2.5 2.5 0 0 1 14.5 8.5V9.5Q14.5 11 13 11Z")
    return [line("M7 21V8.5A5 5 0 0 1 17 8.5V21"), shell(nail), line(seg(21.8, 10.8, 13, 17.3))]


@icon("itch", CAT, "Fingers scratching a forearm with short scratch marks",
      tags=["itchy", "scratch", "scratching", "pruritus", "skin irritation", "bug bite", "allergy"], aliases=["itchy"])
def _(S):
    return arm_parts(S) + [line(seg(x, 2.5, x, 5.8)) for x in (5, 8.5, 12)] + [
        detail(seg(4.5, 14.5, 6, 11.5)), detail(seg(8, 14.5, 9.5, 11.5)), detail(seg(11.5, 14.5, 13, 11.5))]


@icon("skin-mole", CAT, "Magnifier over the skin showing a single dark mole with an uneven edge",
      tags=["mole", "nevus", "birthmark", "skin check", "melanoma", "dermatology", "beauty mark"], aliases=["mole"])
def _(S):
    mole = union(circle(10.3, 10.3, 2.3), circle(11.5, 9.5, 1.8), circle(9.3, 11.3, 1.5), circle(11.2, 11.4, 1.6))
    return [shell(circle(10.5, 10.5, 7.5)), Part("dot", mole),
            line(L(S, seg(16, 16, 21, 21), seg(16, 16, 20.8, 20.8)))]


@icon("dry-skin", CAT, "Patch of skin crossed by a network of fine cracks",
      tags=["dry skin", "xerosis", "flaky skin", "cracked skin", "eczema", "moisturizer", "skincare"],
      aliases=["xerosis"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, S.R))]
    for pts in ([(3, 8.5), (7.5, 10.2), (11, 8.2), (14.5, 10.5), (21, 9)], [(7.5, 10.2), (8.8, 15), (3, 16.5)],
                [(8.8, 15), (13.2, 16.8), (14.5, 21)], [(14.5, 10.5), (16.3, 15), (21, 16.2)], [(11, 8.2), (10.2, 3)]):
        parts.append(detail(poly(pts, r=min(S.r, 0.8))))
    return parts


def sun(cx, cy, r, r0, r1, step=45):
    parts = [shell(circle(cx, cy, r))]
    for a in range(0, 360, step):
        parts.append(line(seg(*polar(cx, cy, r0, a), *polar(cx, cy, r1, a))))
    return parts


_SB = "M2.5 21V17C2.5 13.7 5.2 11.5 8.5 11.5H13.5C16.8 11.5 19.5 13.7 19.5 17V21Z"
_SB_R = "M4.5 21Q2.5 21 2.5 19V17C2.5 13.7 5.2 11.5 8.5 11.5H13.5C16.8 11.5 19.5 13.7 19.5 17V19Q19.5 21 17.5 21Z"


@zicon("sunburn", "Head and shoulders with the shoulders marked and a sun above",
       ["sun burn", "sunscreen", "uv", "red skin", "summer", "sun damage", "peeling"], "M0 11.4H24V14.8H0Z",
       lambda S: L(S, _SB, _SB_R))
def _(S):
    return [shell(circle(11, 5.6, 2.9)), shell(L(S, _SB, _SB_R))] + sun(19.2, 4.6, 1.7, 2.8, 3.6)


@zicon("blister", "Foot in side view with a raised bubble on the back of the heel",
       ["heel blister", "friction", "shoe rub", "hiking", "running", "skin", "foot care"], circle(4.6, 16.8, 2.3),
       lambda S: path_to_d(U(P(tf(foot(S), 1, 0.9, 0)), P(circle(4.6, 16.8, 2.3)))))
def _(S):
    return [shell(path_to_d(U(P(tf(foot(S), 1, 0.9, 0)), P(circle(4.6, 16.8, 2.3)))))]


@icon("wrinkles", CAT, "Eye corner with crease lines beside it and lines across the forehead",
      tags=["wrinkle", "crow's feet", "fine lines", "aging", "anti aging", "skincare", "forehead lines"],
      aliases=["crows-feet"])
def _(S):
    eye = tf(L(S, _EYE_BIG, _EYE_BIG_R), 0.85, -0.6, 3.6)
    return [shell(eye), dot(9.6, 15.5, 1.7), line(hwave(4, 17, 4.5, 0.6, 2)), line(hwave(4, 17, 8.2, 0.6, 2)),
            line(seg(19.6, 12.6, 21.8, 11.2)), line(seg(20.2, 15.5, 22.4, 15.5)), line(seg(19.6, 18.4, 21.8, 19.8))]


# ============================================================================ face, skin and hair

# ============================================================================ face, skin and hair

@icon("acne", CAT, "Face with small bumps on the cheek and forehead",
      tags=["pimples", "spots", "zits", "breakout", "blemish", "skincare", "dermatology"], aliases=["pimples"])
def _(S):
    return [shell(FACE), detail(L(S, seg(8, 10.2, 10.5, 10.2), "M8 10.2H10.5")), detail(seg(13.5, 10.2, 16, 10.2)),
            detail(L(S, seg(10.5, 17.6, 13.5, 17.6), arc(12, 15.6, 2, 45, 135))),
            dot(10.3, 6, 0.9), dot(13.8, 5.6, 0.9), dot(15.2, 13.5, 0.9), dot(8.8, 13.8, 0.9), dot(13.8, 15.7, 0.9)]


@icon("freckles", CAT, "Face with a band of small dots across the nose and cheeks",
      tags=["freckle", "sun spots", "ephelides", "skin", "complexion", "face", "beauty"])
def _(S):
    return [shell(FACE), detail(arc(9.3, 10.5, 1.4, 200, 340)), detail(arc(14.7, 10.5, 1.4, 200, 340)),
            detail(L(S, seg(10, 17.3, 14, 17.3), arc(12, 15.3, 2.3, 50, 130))),
            dot(7.4, 13.3, 0.8), dot(9.8, 14.4, 0.8), dot(12, 13, 0.8), dot(14.2, 14.4, 0.8), dot(16.6, 13.3, 0.8)]


def _drop_small(cx, top, k):
    return tf(_DROP, k, cx - 12 * k, top - 2.5 * k)


@icon("oily-skin", CAT, "Face with shine marks and small oil drops on the forehead and nose",
      tags=["oily", "greasy skin", "shine", "sebum", "skincare", "t zone", "complexion"])
def _(S):
    return [shell(FACE), dot(8.8, 10.8), dot(15.2, 10.8), Part("dot", _drop_small(12, 4.6, 0.3)),
            Part("dot", _drop_small(12, 11.5, 0.3)),
            detail(L(S, seg(7.2, 15.2, 8.2, 13.8), "M7.2 15.2L8.2 13.8")), detail(seg(16.8, 15.2, 15.8, 13.8)),
            detail(seg(10.5, 18, 13.5, 18))]


@icon("chickenpox", CAT, "Torso covered in small round spots",
      tags=["chicken pox", "varicella", "spots", "childhood illness", "rash", "itchy spots", "virus"],
      aliases=["varicella"])
def _(S):
    return torso(S) + [dot(9.2, 9.8, 1), dot(14.6, 9.4, 1), dot(12, 13, 1), dot(9, 16.3, 1), dot(15, 16, 1), dot(12, 19, 1)]


_HIPS = "M5 3H19C19.8 6 20.5 9 20.5 12.5L19.5 21H13.5L12.5 13.5H11.5L10.5 21H4.5L3.5 12.5C3.5 9 4.2 6 5 3Z"
_HIPS_R = ("M6 3H18Q19 3 19.3 4C19.9 6.5 20.5 9.3 20.5 12.5L19.6 20Q19.5 21 18.5 21H14.4Q13.5 21 13.4 20.1L12.5 13.5H11.5L10.6 20.1"
           "Q10.5 21 9.6 21H5.5Q4.5 21 4.4 20L3.5 12.5C3.5 9.3 4.1 6.5 4.7 4Q5 3 6 3Z")


def hwave(x0, x1, y, amp=0.8, n=2):
    w = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        xa = x0 + w * i
        d += (f"C{fmt(xa + w * 0.25)} {fmt(y - amp * 1.3)} {fmt(xa + w * 0.25)} {fmt(y - amp * 1.3)} {fmt(xa + w * 0.5)} {fmt(y)}"
              f"C{fmt(xa + w * 0.75)} {fmt(y + amp * 1.3)} {fmt(xa + w * 0.75)} {fmt(y + amp * 1.3)} {fmt(xa + w)} {fmt(y)}")
    return d


@icon("stretch-marks", CAT, "Hips and thighs with wavy streak lines on one hip",
      tags=["striae", "stretchmarks", "pregnancy", "skin", "hips", "weight gain", "skincare"], aliases=["striae"])
def _(S):
    return [shell(L(S, _HIPS, _HIPS_R))] + [detail(rot(hwave(5.2, 10.2, y, 0.6, 1), -25, 7.7, y)) for y in (6.8, 10, 13.2)]


_EYE_BIG = "M3 14C5.5 10.7 8.5 9 12 9C15.5 9 18.5 10.7 21 14C18.5 17.3 15.5 19 12 19C8.5 19 5.5 17.3 3 14Z"
_EYE_BIG_R = "M3.6 13.2C6 10.5 8.8 9 12 9C15.2 9 18 10.5 20.4 13.2Q21.1 14 20.4 14.8C18 17.5 15.2 19 12 19C8.8 19 6 17.5 3.6 14.8Q2.9 14 3.6 13.2Z"


@icon("dark-circles", CAT, "Tired half-closed eye with a dark half-moon shadow beneath it",
      tags=["under eye circles", "eye bags", "tired eyes", "puffy eyes", "sleep", "fatigue", "skincare"],
      aliases=["eye-bags"])
def _(S):
    eye = tf(L(S, _EYE_BIG, _EYE_BIG_R), 1, 0, -4)
    iris = inter(circle(12, 11.5, 2.6), "M0 11H24V24H0Z")
    return [shell(eye), detail(L(S, "M4 9.4C8 11.2 16 11.2 20 9.4", "M4 9.4C8 11.2 16 11.2 20 9.4")), Part("dot", iris),
            solid("M4.5 17.3C8 19 16 19 19.5 17.3C17.5 22 6.5 22 4.5 17.3Z")]


@icon("goosebumps", CAT, "Forearm with a bumpy top edge and small hairs standing up",
      tags=["goose bumps", "goose pimples", "chills", "cold", "shiver", "skin", "hair standing"],
      aliases=["goose-pimples"])
def _(S):
    o, fs = forearm(S)
    bumps = "M2 9Q3.3 7 4.6 9Q5.9 7 7.2 9Q8.5 7 9.8 9Q11.1 7 12.4 9"
    o = o.replace("M2 9H12.5", bumps + "H12.5").replace("M3 9H12.5", "M3 9Q3.8 7.6 4.6 9Q5.9 7 7.2 9Q8.5 7 9.8 9Q11.1 7 12.4 9H12.5")
    return [shell(o)] + [detail(f) for f in fs] + [line(seg(3.3, 2.8, 3.3, 5.2)), line(seg(7.2, 2.5, 7.2, 5.2)),
                                                    line(seg(11.1, 2.8, 11.1, 5.2)), dot(5.5, 13, 0.9), dot(9.8, 13, 0.9)]


@icon("split-ends", CAT, "Lock of hair strands with one end splitting into two frayed tips",
      tags=["split end", "hair damage", "damaged hair", "haircare", "trim", "frizz", "dry hair"])
def _(S):
    return [line("M2.5 17C5 14 5.5 10.5 8.5 7.5C10 6 11 4.5 11.5 2"),
            line("M6.5 20.5C9 17.5 9.5 14.5 12.5 11.5L13.6 10.4"),
            line(L(S, "M13.6 10.4L14.6 5.5", "M13.6 10.4C14.1 8.8 14.4 7.2 14.6 5.5")),
            line(L(S, "M13.6 10.4L18.6 8", "M13.6 10.4C15.2 9.4 16.9 8.6 18.6 8")),
            line("M11 22C13.5 19 14.5 17 17 15C18.5 13.8 20 13.2 22 12.8")]


@icon("bad-breath", CAT, "Head in profile with wavy odour lines coming from the mouth",
      tags=["halitosis", "breath", "mouth odor", "odour", "smell", "oral hygiene", "garlic"], aliases=["halitosis"])
def _(S):
    return [shell(small_head(S, 0.72, -1, 2.3)), line(hwave(15.5, 22, 9.5, 0.7, 1)), line(hwave(15.5, 22, 13, 0.7, 1)),
            line(hwave(15.5, 22, 16.5, 0.7, 1))]


@icon("tooth-decay", CAT, "Molar with a dark hole eaten into its top",
      tags=["cavity", "caries", "dental decay", "rotten tooth", "dentist", "filling", "tooth"], aliases=["cavity"])
def _(S):
    hole = union(circle(9.5, 8, 1.9), circle(11.2, 9.2, 1.5), circle(8.6, 9.8, 1.3))
    return [shell(tooth(S)), Part("dot", hole)]


@icon("loose-tooth", CAT, "Front tooth tilted in the gum with wiggle marks on each side",
      tags=["wobbly tooth", "baby tooth", "tooth fairy", "dental", "kids", "teeth", "milk tooth"],
      aliases=["wobbly-tooth"])
def _(S):
    gum = L(S, "M3 3H21V6.5C19.5 6.5 18.5 8 17 8C15.5 8 14.5 6.5 12 6.5C9.5 6.5 8.5 8 7 8C5.5 8 4.5 6.5 3 6.5Z",
            "M5 3H19Q21 3 21 5V6.5C19.5 6.5 18.5 8 17 8C15.5 8 14.5 6.5 12 6.5C9.5 6.5 8.5 8 7 8C5.5 8 4.5 6.5 3 6.5V5Q3 3 5 3Z")
    t = rot(L(S, "M9 10.5H15V17.5C15 19.2 13.7 20.5 12 20.5C10.3 20.5 9 19.2 9 17.5Z",
              "M10 10.5H14Q15 10.5 15 11.5V17.5C15 19.2 13.7 20.5 12 20.5C10.3 20.5 9 19.2 9 17.5V11.5Q9 10.5 10 10.5Z"), 14, 12, 10.5)
    return [shell(gum), shell(t), line(arc(12, 15.5, 7.8, 155, 200)), line(arc(12, 15.5, 7.8, -20, 25))]


_LIPS = ("M2.5 12C5 8.5 7.5 6.5 9.5 6.5C10.6 6.5 11.4 7.1 12 7.8C12.6 7.1 13.4 6.5 14.5 6.5C16.5 6.5 19 8.5 21.5 12"
         "C19 15.5 16 17.5 12 17.5C8 17.5 5 15.5 2.5 12Z")
_LIPS_R = ("M3.2 11.2C5.5 8.2 7.8 6.5 9.5 6.5C10.6 6.5 11.4 7.1 12 7.8C12.6 7.1 13.4 6.5 14.5 6.5C16.2 6.5 18.5 8.2 20.8 11.2"
           "Q21.4 12 20.8 12.8C18.5 15.8 15.8 17.5 12 17.5C8.2 17.5 5.5 15.8 3.2 12.8Q2.6 12 3.2 11.2Z")


def lips(S):
    return L(S, _LIPS, _LIPS_R)


@icon("cold-sore", CAT, "Closed lips with a small cluster of blisters at one corner",
      tags=["fever blister", "herpes", "lip sore", "hsv", "blister", "mouth", "lips"], aliases=["fever-blister"])
def _(S):
    k, dx, dy = 0.78, -0.8, 3
    return [shell(tf(lips(S), k, dx, dy), stroke_miterlimit="2"), detail(tf("M6.5 12.3C10 13.1 14 13.1 17.5 12.3", k, dx, dy)),
            dot(19.2, 9.2, 1.15), dot(21.3, 12.2, 1.15), dot(18.9, 14.9, 1.15)]


@icon("chapped-lips", CAT, "Lips with small vertical cracks",
      tags=["dry lips", "cracked lips", "lip balm", "winter", "lips", "dehydration"], aliases=["dry-lips"])
def _(S):
    return [shell(lips(S), stroke_miterlimit="2"), detail("M6.5 12.3C10 13.1 14 13.1 17.5 12.3"),
            detail(seg(8.6, 9, 9.3, 10.6)), detail(seg(8, 14.3, 7.5, 15.4)), detail(seg(12.3, 14.6, 11.9, 16.1)),
            detail(seg(16.2, 14.3, 16.7, 15.4))]
