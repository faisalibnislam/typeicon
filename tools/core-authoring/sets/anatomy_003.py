"""TypeIcon Core: anatomy (batch 003): conditions of the teeth, eyes, skin and body.

Eyes share one almond outline (pointed corners in Line, softened corners in Rounded). Full figures are
stick figures (head r 2 over 2 px limbs) like the accessibility and health sets. Where one stroke passes
behind another it is cut away with a gap, so the Filled style stays readable.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, rotation, transform_path  # noqa: F401

CAT = "anatomy"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def inter(a, b):
    return path_to_d(I(P(a), P(b)))


def xf(d, k=1.0, dx=0.0, dy=0.0, sx=1.0):
    """Scale a closed path by k about the origin (sx=-1 mirrors), then shift it."""
    return path_to_d(transform_path(P(d), (k * sx, 0, 0, k, dx, dy)))


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpts(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def grow(d, g):
    """Region d expanded by g px (to cut a clean gap behind a front shape)."""
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def cut_stroke(d, S, *cuts):
    """A 2 px stroke along d with the regions `cuts` removed: drawn as a solid mark in every style."""
    reg = ST(d, 2.0, S.cap, S.join)
    return solid(path_to_d(D(reg, *[P(c) for c in cuts])))


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def _p(x, y):
    return f"{fmt(x)} {fmt(y)}"


def eye(cx, cy, w, h, S):
    """Almond eye outline centred on (cx, cy): pointed corners in Line, softened in Rounded."""
    sx, sy = w / 18, h / 10

    def q(x, y):
        return _p(cx + x * sx, cy + y * sy)
    if S.name == "line":
        return (f"M{q(-9, 0)}C{q(-6.5, -3.3)} {q(-3.5, -5)} {q(0, -5)}C{q(3.5, -5)} {q(6.5, -3.3)} {q(9, 0)}"
                f"C{q(6.5, 3.3)} {q(3.5, 5)} {q(0, 5)}C{q(-3.5, 5)} {q(-6.5, 3.3)} {q(-9, 0)}Z")
    return (f"M{q(-8.4, -0.8)}C{q(-6, -3.5)} {q(-3.2, -5)} {q(0, -5)}C{q(3.2, -5)} {q(6, -3.5)} {q(8.4, -0.8)}"
            f"Q{q(9.1, 0)} {q(8.4, 0.8)}C{q(6, 3.5)} {q(3.2, 5)} {q(0, 5)}C{q(-3.2, 5)} {q(-6, 3.5)} {q(-8.4, 0.8)}"
            f"Q{q(-9.1, 0)} {q(-8.4, -0.8)}Z")


def drop(cx, top, r, S):
    """Tear or blood drop: point at `top`, round bottom of radius r."""
    cy = top + r * 2.3
    a = math.degrees(math.asin(r / (cy - top)))
    p1 = (cx - r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a)))
    p2 = (cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a)))
    if S.name == "line":
        return f"M{_p(cx, top)}L{_p(*p2)}A{fmt(r)} {fmt(r)} 0 1 1 {_p(*p1)}Z"
    t = 0.18
    s1 = (cx + (p1[0] - cx) * t, top + (p1[1] - top) * t)
    s2 = (cx + (p2[0] - cx) * t, top + (p2[1] - top) * t)
    return f"M{_p(*s1)}Q{_p(cx, top)} {_p(*s2)}L{_p(*p2)}A{fmt(r)} {fmt(r)} 0 1 1 {_p(*p1)}Z"


_TOOTH = ("M7 3.5C4.5 3.5 3.5 5.5 3.5 8C3.5 11 5 13 6 15L7.5 21L10.5 14L13.5 14L16.5 21L18 15C19 13 20.5 11 20.5 8"
          "C20.5 5.5 19.5 3.5 17 3.5C15 3.5 14 4.5 12 4.5C10 4.5 9 3.5 7 3.5Z")
_TOOTH_R = ("M7 3.5C4.5 3.5 3.5 5.5 3.5 8C3.5 11 5 13 6 15L7 20C7.3 21 8.7 21 9 20L10.5 14.5C10.8 13.5 13.2 13.5 13.5 14.5"
            "L15 20C15.3 21 16.7 21 17 20L18 15C19 13 20.5 11 20.5 8C20.5 5.5 19.5 3.5 17 3.5C15 3.5 14 4.5 12 4.5"
            "C10 4.5 9 3.5 7 3.5Z")


def tooth(S, k=1.0, dx=0.0, dy=0.0):
    return xf(L(S, _TOOTH, _TOOTH_R), k, dx, dy)


def snowflake(cx, cy, r):
    return [line(seg(*pt(cx, cy, r, a), *pt(cx, cy, r, a + 180))) for a in (90, 30, -30)]


def pt(cx, cy, r, deg):
    return (cx + r * math.cos(math.radians(deg)), cy + r * math.sin(math.radians(deg)))


def arrow_head(tip, deg, size, S, spread=40):
    """Open arrowhead at `tip` pointing towards angle `deg`."""
    a = pt(*tip, size, deg + 180 - spread)
    b = pt(*tip, size, deg + 180 + spread)
    return line(poly([a, tip, b], r=min(S.r, 0.8)))


# --------------------------------------------------------------------------- teeth

@icon("sensitive-teeth", CAT, "A tooth with a snowflake and a lightning bolt for sensitivity to cold",
      tags=["tooth sensitivity", "cold", "dental pain", "dentist", "enamel", "toothache"])
def _(S):
    return [shell(tooth(S, 0.68, -0.2, 6.6))] + snowflake(18, 5.3, 3.5) + [
        line(poly([(20.8, 11.5), (17.8, 15.5), (21, 16), (18.3, 20.5)], r=min(S.r, 0.6)))]


def _grin(S):
    return L(S, "M3 6.5H21C21 13.5 17 18.5 12 18.5C7 18.5 3 13.5 3 6.5Z",
             "M5 6.5H19Q21 6.5 20.9 8.5C20.4 14.3 16.6 18.5 12 18.5C7.4 18.5 3.6 14.3 3.1 8.5Q3 6.5 5 6.5Z")


@icon("missing-tooth", CAT, "A grin with a row of upper front teeth and one tooth missing",
      tags=["gap", "lost tooth", "tooth loss", "dentist", "dental", "implant"], aliases=["tooth-gap"])
def _(S):
    return [shell(_grin(S)), detail(seg(3.5, 12.5, 20.5, 12.5)),
            detail(seg(7.5, 6.5, 7.5, 12.5)), detail(seg(16.5, 6.5, 16.5, 12.5)),
            mark(rect(11, 6.5, 5.5, 6, 0))]


@icon("crooked-teeth", CAT, "A grin whose upper front teeth sit at uneven, overlapping angles",
      tags=["misaligned teeth", "orthodontics", "braces", "overlapping teeth", "dental", "crowding"])
def _(S):
    edge = [(3.5, 11.5), (7.2, 13.8), (11.2, 11.5), (15.6, 14), (20.5, 11.8)]
    return [shell(_grin(S)), detail(poly(edge, r=min(S.r, 0.8))),
            detail(seg(6.2, 6.5, 7.2, 13.8)), detail(seg(12.4, 6.5, 11.2, 11.5)), detail(seg(14.2, 6.5, 15.6, 14))]


@icon("teething", CAT, "A baby face with one small tooth and a drop of drool",
      tags=["baby tooth", "infant", "first tooth", "drool", "toddler", "milk teeth"])
def _(S):
    face = union(circle(11.5, 11.5, 8), drop(16.8, 16.5, 1.9, S))
    mouth = L(S, "M7.8 12.5H15.2C15.2 15.4 13.5 17.5 11.5 17.5C9.5 17.5 7.8 15.4 7.8 12.5Z", ellipse(11.5, 14.6, 3.6, 2.9))
    tooth_cut = rect(10.3, 14.6, 2.4, 4, L(S, 0, 1.1))
    return [shell(face), line("M11.5 3.5C11.5 1.9 13.4 1.5 14.2 2.7"), dot(8.6, 9, 1.2), dot(14.4, 9, 1.2),
            mark(minus(mouth, tooth_cut))]


# --------------------------------------------------------------------------- eyes

@icon("cataract", CAT, "An eye whose pupil is clouded over by a hazy disc",
      tags=["cloudy lens", "eye condition", "vision loss", "ophthalmology", "blurry vision", "eye surgery"])
def _(S):
    stripes = []
    iris = P(circle(12, 12, 4.8))
    for off in (-1.8, 1.8):
        a, b = pt(12, 12, 7, 135), pt(12, 12, 7, -45)
        n = (off * math.cos(math.radians(45)), off * math.sin(math.radians(45)))
        stripes.append(ST(seg(a[0] + n[0], a[1] + n[1], b[0] + n[0], b[1] + n[1]), 1.5, "butt", "miter"))
    haze = path_to_d(D(iris, *stripes))
    return [shell(eye(12, 12, 19.5, 12.5, S)), mark(haze)]


@icon("pink-eye", CAT, "An eye with swollen lids, red vessel lines and a tear",
      tags=["conjunctivitis", "red eye", "eye infection", "itchy eye", "irritated eye", "allergy"],
      aliases=["conjunctivitis"])
def _(S):
    return [shell(eye(12, 10.5, 19, 11, S)), dot(12, 10.5, 2.4),
            line("M3.5 3.8C8.5 1.5 15.5 1.5 20.5 3.8"),
            detail(poly([(4.8, 10.8), (6.8, 10.3), (7.8, 11.8)], r=min(S.r, 0.6))),
            detail(poly([(19.2, 10.2), (17.2, 10.7), (16.2, 9.2)], r=min(S.r, 0.6))),
            shell(drop(5, 16.5, 1.9, S))]


@icon("stye", CAT, "An eye with a small round bump on the edge of the upper eyelid",
      tags=["sty", "hordeolum", "eyelid bump", "eye infection", "swollen eyelid", "chalazion"], aliases=["sty"])
def _(S):
    e = eye(12, 13, 19, 11, S)
    return [shell(union(e, circle(15.5, 8.2, 2.5))), dot(11.5, 13.5, 2.4),
            line("M3.5 7.5C5.3 5 7.8 3.7 10.5 3.5")]


@icon("eye-strain", CAT, "A tired half-closed eye above a glowing screen",
      tags=["tired eyes", "screen time", "digital eye strain", "computer vision", "sore eyes", "blue light"])
def _(S):
    rays = [line(seg(*pt(15.5, 6, 2.6, ang), *pt(15.5, 6, 4.8, ang))) for ang in (-40, 0)]
    return [shell(eye(8.5, 6, 13, 8, S)), dot(8.5, 6, 2), *rays,
            shell(rect(9, 12.5, 12.5, 6, min(S.R, 2))), line(seg(15.25, 18.5, 15.25, 21)), line(seg(12.5, 21, 18, 21))]


@icon("watery-eyes", CAT, "An open eye with two tears running down from the lower lid",
      tags=["tears", "teary eyes", "crying", "allergy", "hay fever", "eye irritation"])
def _(S):
    return [shell(eye(12, 8, 19, 11, S)), dot(12, 8, 2.4),
            shell(drop(8.5, 13.6, 2, S)), shell(drop(15.5, 15.6, 2, S))]


@icon("black-eye", CAT, "A face with a dark bruised ring around one eye",
      tags=["bruise", "shiner", "injury", "punch", "swollen eye", "fight"], aliases=["shiner"])
def _(S):
    ring = minus(circle(15.2, 10.5, 4), circle(15.2, 10.5, 2.1))
    return [shell(circle(12, 12, 9)), dot(8.5, 10.5, 1.3), mark(ring), dot(15.2, 10.5, 1),
            detail("M9 16.8C10.8 15.9 13.2 15.9 15 16.8")]


@icon("double-vision", CAT, "Two offset copies of the same eye, as if seen double",
      tags=["diplopia", "blurred vision", "seeing double", "vision problem", "dizziness", "eye condition"],
      aliases=["diplopia"])
def _(S):
    front = eye(14.5, 14, 15, 9, S)
    back = eye(9.5, 9.5, 15, 9, S)
    return [shell(front), dot(14.5, 14, 2.2), cut_stroke(back, S, grow(front, 2)),
            mark(minus(circle(9.5, 9.5, 2.2), grow(front, 2)))]


# --------------------------------------------------------------------------- ears, cycle, whole body

def _ear(ox, oy, s):
    def X(v):
        return fmt(ox + s * v)

    def Y(v):
        return fmt(oy + s * v)
    outer = (f"M{X(7)} {Y(9)}C{X(7)} {Y(5.7)} {X(9.5)} {Y(3)} {X(13)} {Y(3)}C{X(16.5)} {Y(3)} {X(19)} {Y(5.7)} {X(19)} {Y(9)}"
             f"C{X(19)} {Y(11.8)} {X(17.5)} {Y(13)} {X(16.3)} {Y(14.5)}C{X(15.3)} {Y(15.8)} {X(15.2)} {Y(17.5)} {X(14.4)} {Y(19)}"
             f"C{X(13.5)} {Y(20.7)} {X(11)} {Y(21.5)} {X(9)} {Y(20)}")
    inner = (f"M{X(10.8)} {Y(9.5)}C{X(10.8)} {Y(8)} {X(11.8)} {Y(7)} {X(13)} {Y(7)}C{X(14.3)} {Y(7)} {X(15.2)} {Y(8)} {X(15.2)} {Y(9.2)}"
             f"C{X(15.2)} {Y(10.8)} {X(13.8)} {Y(11.4)} {X(13.1)} {Y(12.8)}")
    return outer, inner


@icon("tinnitus", CAT, "An ear with a sharp zigzag ringing sound beside it",
      tags=["ringing ears", "ear ringing", "hearing", "buzzing", "noise", "audiology"])
def _(S):
    o, i = _ear(-4.2, 0.4, 0.95)
    zig = [(17.5, 4.5), (20.5, 7), (17.5, 9.5), (20.5, 12), (17.5, 14.5), (20.5, 17), (17.5, 19.5)]
    return [line(o), line(i), line(poly(zig, r=min(S.r, 0.6)))]


@icon("menstrual-cycle", CAT, "A circular arrow with a blood drop at the top and phase dots",
      tags=["period", "cycle tracker", "ovulation", "menstruation", "fertility", "women's health"])
def _(S):
    c, r = (12, 12), 8.5
    end = pt(*c, r, 240)
    return [line(arc(*c, r, -60, 240)), arrow_head(end, 240 + 90 + 12, 3.2, S),
            shell(drop(12, 7, 2.4, S))]


@icon("fatigue", CAT, "A slumped person with drooping head and arms under an empty battery",
      tags=["tired", "exhausted", "exhaustion", "low energy", "burnout", "weary"])
def _(S):
    return [line(rect(11.5, 2.5, 8.5, 4.5, min(S.R, 1.2))), solid(rect(20.5, 3.8, 1.5, 1.9, 0)),
            shell(circle(7.5, 11, 2)),
            line("M10 10C12.8 10.5 14.3 12.5 14.3 16"),
            line(poly([(11, 11), (9.8, 17.5)], r=0)),
            line(poly([(14.3, 16), (13, 21)], r=0)), line(poly([(14.3, 16), (16.8, 21)], r=0))]


@icon("restless-legs", CAT, "Legs under a blanket with motion lines around the calves",
      tags=["restless leg syndrome", "rls", "leg twitching", "sleep disorder", "night", "jerking legs"])
def _(S):
    cover = L(S, "M3 18.5V14.5H11V12.5C11 11.7 11.7 11 12.5 11H16C16.5 9.3 19 8.8 20.3 10.3C20.8 10.8 21 11.5 21 12.3V18.5Z",
              "M4 18.5Q3 18.5 3 17.5V15.5Q3 14.5 4 14.5H11V12.5C11 11.7 11.7 11 12.5 11H16C16.5 9.3 19 8.8 20.3 10.3"
              "C20.8 10.8 21 11.5 21 12.3V17.5Q21 18.5 20 18.5Z")
    return [shell(cover), line(seg(3, 5.5, 3, 21)), line(seg(21, 18.5, 21, 21)), shell(circle(7, 10.5, 2.2)),
            line(arc(18.2, 11.3, 5, 195, 250)), line(arc(18.2, 11.3, 5, 290, 345))]


# --------------------------------------------------------------------------- feet, gait and bed rest

@icon("ingrown-toenail", CAT, "A big toe from above with the nail edge curving down into swollen skin",
      tags=["toenail", "ingrown nail", "podiatry", "toe pain", "foot care", "nail infection"])
def _(S):
    toe = "M5 21V10.5A6.5 6.5 0 0 1 16.8 6.8C19.8 7.8 20.8 11 19.5 13.5C18.8 14.8 18 15.8 18 17.5V21"
    nail = L(S, "M8 13.5V9.5A3.5 3.5 0 0 1 15 9.5V11C15 12.5 15.5 13.5 16.5 14.5Z",
             "M9 13.5Q8 13.5 8 12.5V9.5A3.5 3.5 0 0 1 15 9.5V11C15 12.3 15.3 13 15.8 13.5Q16.3 14.5 15.3 14.5Z")
    return [line(toe), shell(nail),
            line(seg(*pt(17.5, 9, 3.4, -65), *pt(17.5, 9, 5.2, -65))), line(seg(*pt(17.5, 9, 3.6, -20), *pt(17.5, 9, 5.2, -20)))]


@icon("limping", CAT, "A person walking with one stiff leg and a pain mark on it",
      tags=["limp", "leg injury", "hobbling", "gait", "walking pain", "hurt leg"], aliases=["limp"])
def _(S):
    knee = (14.2, 17.2)
    rays = [line(seg(*pt(*knee, 2.2, a), *pt(*knee, 4.4, a))) for a in (-45, 0, 45)]
    return [shell(circle(11, 4.5, 2)),
            line(poly([(11.5, 8), (13, 13.5)], r=0)),
            line(poly([(13, 13.5), (10.2, 16.8), (10.5, 21)], r=S.r)),
            line(poly([(13, 13.5), (15.5, 21)], r=0)),
            line(poly([(11.8, 9.2), (8, 12.5)], r=0)), line(poly([(12.2, 9.2), (15.5, 11.5)], r=0))] + rays


@icon("sick-in-bed", CAT, "A person lying in bed with a thermometer in the mouth and an ice pack on the head",
      tags=["ill", "bed rest", "flu", "sick day", "fever", "recovering"])
def _(S):
    cover = L(S, "M3 18.5V14.5H10.5V13H21V18.5Z", "M4 18.5Q3 18.5 3 17.5V15.5Q3 14.5 4 14.5H10.5V14Q10.5 13 11.5 13H20Q21 13 21 14V17.5Q21 18.5 20 18.5Z")
    return [shell(cover), line(seg(3, 5.5, 3, 21)), line(seg(21, 18.5, 21, 21)),
            shell(circle(7.5, 11.2, 2.3)), shell(rect(5, 4, 5, 3, min(S.R, 1.2))),
            line(seg(10.2, 10.6, 14.5, 8.2)), dot(15, 7.9, 1.2)]


# --------------------------------------------------------------------------- body regions

@icon("bloating", CAT, "A belly in side view puffed out with arrows pointing outward",
      tags=["bloated", "swollen belly", "gas", "indigestion", "stomach", "distension"], aliases=["bloated"])
def _(S):
    front = "M6.5 3C6.5 5.5 7 7 8.5 8C12.5 9.2 14 11.5 14 14C14 16.5 12 18.3 9 18.8C8 19.5 8 20.3 8 21"
    arrows = []
    for a in (-35, 0, 35):
        s0, s1 = pt(9, 13.5, 7.2, a), pt(9, 13.5, 12, a)
        arrows += [line(seg(*s0, *s1)), arrow_head(s1, a, 2.4, S)]
    return [line(seg(2.5, 3, 2.5, 21)), line(front)] + arrows


@icon("adams-apple", CAT, "A head and neck in side profile with the bump of the voice box at the front of the throat",
      tags=["larynx", "voice box", "throat", "neck", "laryngeal prominence", "anatomy"])
def _(S):
    head = L(S, "M6 21V15.5C4 14.3 3 12.3 3 10C3 6.1 6 3 10 3C13.6 3 16 5.6 16 8.6L17.3 11.3L16 11.7V13"
                "C16 14 15.2 14.7 14.2 14.7H12.3L12.8 16.3L14.4 17.8L12.8 19.2V21Z",
             "M6 20V15.5C4 14.3 3 12.3 3 10C3 6.1 6 3 10 3C13.6 3 16 5.6 16 8.6L17 10.7Q17.4 11.5 16.6 11.6L16 11.7V13"
                "C16 14 15.2 14.7 14.2 14.7H12.3L12.8 16.3L13.9 17.3Q14.4 17.8 13.9 18.3L12.8 19.2V20Q12.8 21 11.8 21H7Q6 21 6 20Z")
    return [shell(head, stroke_miterlimit="2"), line(seg(21.5, 17.8, 17.5, 17.8)), arrow_head((17.5, 17.8), 180, 2.4, S)]


@icon("staphylococcus", CAT, "A grape-like cluster of round bacteria packed tightly together",
      tags=["staph", "bacteria", "cocci", "infection", "microbiology", "germ"], aliases=["staph"])
def _(S):
    r = 2.6
    cs = [(7, 6.5), (12.8, 5.5), (18, 8.2), (9.5, 12), (15.3, 12.8), (6.3, 17.5), (12, 17.8), (17.6, 18.3)]
    parts = [shell(circle(x, y, r)) for x, y in cs]
    parts.append(detail(arc(12.8, 5.5, 1.1, 180, 270)) if S.name == "line" else detail(arc(12.8, 5.5, 1.1, 170, 280)))
    return parts


@icon("joint-dislocation", CAT, "A ball-and-socket joint with the ball popped out of its cup",
      tags=["dislocated joint", "dislocation", "shoulder dislocation", "hip", "orthopedics", "injury"],
      aliases=["dislocation"])
def _(S):
    socket = L(S, "M2 10H5.5C6.5 7.3 8.5 5.5 11 5.5V8C9.5 8 8.5 10 8.5 12C8.5 14 9.5 16 11 16V18.5C8.5 18.5 6.5 16.7 5.5 14H2Z",
               "M3 10H5.5C6.5 7.3 8.5 5.5 11 5.5Q11.8 5.5 11.8 6.3V7.2Q11.8 8 11 8C9.5 8 8.5 10 8.5 12C8.5 14 9.5 16 11 16"
               "Q11.8 16 11.8 16.8V17.7Q11.8 18.5 11 18.5C8.5 18.5 6.5 16.7 5.5 14H3Q2 14 2 13V11Q2 10 3 10Z")
    shaft = rot(rect(14.6, 8, 3.8, 12, L(S, 0, 1.5)), -20, 16.5, 8)
    ball = union(circle(16.5, 7.5, 3.3), shaft)
    return [shell(socket), shell(ball), line(poly([(13.2, 1.8), (11.8, 3.6), (13.6, 4.2), (12.4, 6)], r=min(S.r, 0.5)))]


@icon("migraine", CAT, "A head in profile with a zigzag flicker in front of the eyes and pain at the temple",
      tags=["headache", "aura", "head pain", "neurology", "throbbing", "visual aura"])
def _(S):
    head = L(S, "M8 21V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.5 12.8L19 13.3V15.5C19 16.6 18.1 17.5 17 17.5H14V21Z",
             "M8 20V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.2 12Q20.6 12.9 19.7 13.1L19 13.3V15.5C19 16.6 18.1 17.5 17 17.5H14V20C14 20.6 13.6 21 13 21H9C8.4 21 8 20.6 8 20Z")
    head = xf(head, 0.8, -1.2, 3.8)
    zig = [pt(12, 11, 9.5 + (1.3 if i % 2 else 0), -60 + i * 15) for i in range(8)]
    return [shell(head), detail(poly([(7.5, 6.5), (9.8, 8.8), (8, 10), (10.5, 12.5)], r=min(S.r, 0.5))),
            line(poly(zig, r=min(S.r, 0.5)))]


@icon("aneurysm", CAT, "A blood vessel with a round balloon-like bulge swelling from one wall",
      tags=["artery", "bulge", "vascular", "blood vessel", "stroke risk", "cardiology"])
def _(S):
    return [shell(ellipse(4, 15.75, 1.8, 3.25)),
            line("M4 12.5H7.6A5.5 5.5 0 1 1 16.4 12.5H22"), line(seg(4, 19, 22, 19))]


_STOMACH = ("M8 3H11V6C11 7.5 11.8 8.5 13 8.7C14 8.9 15 8.5 15.8 7.7C17.8 5.9 21 7.3 21 10.5C21 16 17 20.5 11.5 20.5"
            "C9.8 20.5 8.2 20 7 19L5 21.2L3.2 19.5L5.5 17.2C4.8 15.3 5.3 13 7 11.5C7.7 10.8 8 10 8 9Z")


@icon("stomach-ulcer", CAT, "The stomach with a small round crater sore on its wall",
      tags=["ulcer", "peptic ulcer", "gastric ulcer", "stomach pain", "gastritis", "digestion"],
      aliases=["peptic-ulcer"])
def _(S):
    return [shell(_STOMACH, stroke_miterlimit="2"), detail(circle(13.5, 14, 2.6)), dot(13.5, 14, 1)]


@icon("wart", CAT, "A fingertip with a rough round bump growing on its side",
      tags=["verruca", "skin growth", "dermatology", "skin", "hpv", "wart removal"], aliases=["verruca"])
def _(S):
    bump = union(*[circle(*pt(17.5, 13, 1.7, a), 1.6) for a in range(-90, 100, 45)], circle(17.5, 13, 2))
    finger = "M6 21V9.5A6 6 0 0 1 18 9.5V21"
    nail = L(S, "M9.5 13.5V9A2.5 2.5 0 0 1 14.5 9V13.5Z", "M11 13.5Q9.5 13.5 9.5 12V9A2.5 2.5 0 0 1 14.5 9V12Q14.5 13.5 13 13.5Z")
    return [cut_stroke(finger, S, grow(bump, 1.8)), shell(bump), shell(nail)]


@icon("body-odor", CAT, "A person with one arm raised and wavy odor lines coming from the armpit",
      tags=["body odour", "sweat", "smell", "stink", "armpit", "deodorant"], aliases=["body-odour"])
def _(S):
    waves = [line(f"M{fmt(x)} {fmt(y)}C{fmt(x + 1.2)} {fmt(y - 1.6)} {fmt(x + 2.3)} {fmt(y - 1.6)} {fmt(x + 3.5)} {fmt(y)}"
                  f"S{fmt(x + 5.8)} {fmt(y + 1.6)} {fmt(x + 7)} {fmt(y)}") for x, y in ((12, 10.5), (12, 14.5))]
    return [shell(circle(6.5, 5.5, 2.2)),
            line(seg(6.5, 9, 6.5, 16.5)),
            line(poly([(6.5, 16.5), (4.2, 21)], r=0)), line(poly([(6.5, 16.5), (8.8, 21)], r=0)),
            line(poly([(6.5, 10), (3, 14.5)], r=0)),
            line(poly([(6.5, 10), (10, 7), (10.5, 2.5)], r=S.r))] + waves


# --------------------------------------------------------------------------- teeth, organs and joints (2)

@icon("teeth-grinding", CAT, "Clenched upper and lower teeth pressed together with zigzag marks at each side",
      tags=["bruxism", "clenching", "jaw clenching", "tmj", "night grinding", "dental"], aliases=["bruxism"])
def _(S):
    parts = [shell(rect(6.5, 5, 11, 14, min(S.R, 3))), detail(seg(6.5, 12, 17.5, 12))]
    for x in (10.2, 13.8):
        parts.append(detail(seg(x, 5, x, 12)))
    parts.append(detail(seg(12, 12, 12, 19)))
    for sx in (1, -1):
        zig = [(12 + sx * 8.5, 7), (12 + sx * 10, 9.5), (12 + sx * 8.5, 12), (12 + sx * 10, 14.5), (12 + sx * 8.5, 17)]
        parts.append(line(poly(zig, r=min(S.r, 0.6))))
    return parts


@icon("period-cramps", CAT, "A uterus with jagged pain marks at its sides and a drop below",
      tags=["menstrual cramps", "period pain", "dysmenorrhea", "menstruation", "pelvic pain", "women's health"])
def _(S):
    body = L(S, "M8 4H16C17.1 4 17.7 5 17.3 6L15 12C14.6 13 13.8 13.5 12.8 13.5H11.2C10.2 13.5 9.4 13 9 12L6.7 6C6.3 5 6.9 4 8 4Z",
             "M8.5 4H15.5C17 4 17.8 5.2 17.3 6.5L15 12C14.6 13 13.8 13.5 12.8 13.5H11.2C10.2 13.5 9.4 13 9 12L6.7 6.5C6.2 5.2 7 4 8.5 4Z")
    parts = [shell(body, stroke_miterlimit="2"), line("M6.8 5C5 4.3 3.3 5 3 7"), line("M17.2 5C19 4.3 20.7 5 21 7"),
             shell(drop(12, 15.5, 1.9, S))]
    for sx in (1, -1):
        zig = [(12 + sx * 7.5, 10), (12 + sx * 9.5, 11.8), (12 + sx * 7.5, 13.6), (12 + sx * 9.5, 15.4)]
        parts.append(line(poly(zig, r=min(S.r, 0.6))))
    return parts


def _lung(sx, k=1.0, dy=0.0):
    d = "M10 8C7.2 8 4 12 3.5 16.5C3.2 19 4.5 20.7 7 20.2L9.5 19.7C10.2 19.5 10.5 19 10.5 18.3V8.8C10.5 8.3 10.4 8 10 8Z"
    d = xf(d, 1, 0, dy)
    return d if sx > 0 else xf(d, 1, 24, 0, sx=-1)


@icon("asthma", CAT, "A pair of lungs with a narrowed windpipe and short wheeze lines",
      tags=["wheezing", "breathing difficulty", "inhaler", "respiratory", "airway", "shortness of breath"])
def _(S):
    return [shell(_lung(1, dy=1)), shell(_lung(-1, dy=1)),
            line(poly([(12, 2.5), (12, 11.5)], r=0)), line("M12 11.5L10.5 13M12 11.5L13.5 13"),
            line("M3 5.5C4 4.3 5 4.3 6 5.5S8 6.7 9 5.5"), line("M15 5.5C16 4.3 17 4.3 18 5.5S20 6.7 21 5.5")]


_FOOT = ("M6.5 3H11V11.8C11 13.1 11.9 14.2 13.2 14.6L18.6 16.2C20.1 16.7 21 17.8 21 19C21 20.2 20.2 21 19 21H16.8C15.3 21 14.6 20 12.7 20"
         "C10.8 20 10.2 21 8.5 21H6C4.8 21 4 20.2 4 19C4 17.5 5 16.4 5.8 15.4C6.3 14.7 6.5 14 6.5 13Z")
_FOOT_R = ("M7.5 3H10Q11 3 11 4V11.8C11 13.1 11.9 14.2 13.2 14.6L18.6 16.2C20.1 16.7 21 17.8 21 19C21 20.2 20.2 21 19 21H16.8C15.3 21 14.6 20 12.7 20"
           "C10.8 20 10.2 21 8.5 21H6C4.8 21 4 20.2 4 19C4 17.5 5 16.4 5.8 15.4C6.3 14.7 6.5 14 6.5 13V4Q6.5 3 7.5 3Z")


@icon("sprained-ankle", CAT, "An ankle wrapped in a crossed elastic bandage with swelling marks",
      tags=["sprain", "ankle injury", "twisted ankle", "compression bandage", "sports injury", "first aid"])
def _(S):
    foot = xf(L(S, _FOOT, _FOOT_R), 1, 1.5, 0)
    return [shell(foot), detail(seg(8, 7, 12.5, 7)), detail(seg(8, 9.5, 12.5, 14.3)), detail(seg(8, 14.3, 12.5, 9.5)),
            line(seg(2, 9.5, 4.8, 10.5)), line(seg(2, 13.5, 4.8, 13))]


@icon("slouching", CAT, "A person sitting in side view with a rounded, hunched back and the head pushed forward",
      tags=["bad posture", "hunched", "slumped", "sitting posture", "back pain", "ergonomics"], aliases=["slouch"])
def _(S):
    return [shell(circle(15, 6.5, 2.2)),
            line("M7.5 14.5C6 11 8.5 8 12.5 8.3"),
            line(poly([(7.5, 14.5), (14.5, 14.5), (14.5, 20.5)], r=S.r)),
            line(poly([(11, 9), (14.5, 11.8)], r=0)),
            line(poly([(4, 8), (4, 21)], r=0)), line(seg(5, 17, 12, 17))]


@icon("insomnia", CAT, "A head on a pillow with both eyes wide open under a crescent moon",
      tags=["sleepless", "can't sleep", "sleep disorder", "awake at night", "restless night", "sleep problems"],
      aliases=["sleeplessness"])
def _(S):
    face = circle(10.5, 12.5, 6)
    pillow = rect(2, 15.5, 20, 6, min(S.R, 3))
    moon = minus(circle(18.5, 5, 3.5), circle(20.5, 3.3, 3))
    return [shell(face), shell(minus(pillow, grow(face, 2))), detail(circle(7.9, 12, 1.4)), detail(circle(13.1, 12, 1.4)),
            shell(moon)]


@icon("achilles-tendon", CAT, "A lower leg and heel in side view with the tendon from calf to heel drawn solid",
      tags=["achilles", "heel", "tendon", "tendonitis", "calf", "running injury"])
def _(S):
    leg = L(S, "M5.5 3H12C11.8 6 11.2 9 11.5 11.5C11.7 13 12.5 13.9 14 14.3L19 16C20.3 16.5 21 17.5 21 18.8C21 20.2 20.2 21 19 21"
               "H6.5C5 21 4 20 4 18.5C4 17 5 15.5 5.3 13.5C5.6 11 3.8 9 3.6 6.5C3.5 5 4.1 3.8 5.5 3Z",
            "M6.5 3H11Q12 3 12 4C11.8 6.5 11.2 9 11.5 11.5C11.7 13 12.5 13.9 14 14.3L19 16C20.3 16.5 21 17.5 21 18.8C21 20.2 20.2 21 19 21"
               "H6.5C5 21 4 20 4 18.5C4 17 5 15.5 5.3 13.5C5.6 11 3.8 9 3.6 6.5C3.5 5.2 4.3 3.9 5 3.4Q5.6 3 6.5 3Z")
    tendon = "M5.9 8.8C7.1 10.8 7.5 13.8 6.9 18.3H8.7C9.3 13.8 8.9 10.8 7.8 8.8Z"
    return [shell(leg), mark(tendon)]


def _piece(x, y, k=1.0):
    return union(rect(x, y, 4.2 * k, 4.2 * k), circle(x + 2.1 * k, y - 0.4 * k, 1.3 * k), circle(x + 4.6 * k, y + 2.1 * k, 1.3 * k))


@icon("memory-loss", CAT, "A head in profile with a puzzle piece missing from the brain area and floating away",
      tags=["forgetfulness", "dementia", "alzheimer's", "amnesia", "cognitive decline", "brain health"],
      aliases=["forgetfulness"])
def _(S):
    head = L(S, "M8 21V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.5 12.8L19 13.3V15.5C19 16.6 18.1 17.5 17 17.5H14V21Z",
             "M8 20V17.2C5.6 15.8 4 13.3 4 10.5C4 6.4 7.6 3 12 3C16.1 3 19 5.9 19 9.5L20.2 12Q20.6 12.9 19.7 13.1L19 13.3V15.5C19 16.6 18.1 17.5 17 17.5H14V20C14 20.6 13.6 21 13 21H9C8.4 21 8 20.6 8 20Z")
    head = xf(head, 0.8, -1.5, 4.4)
    hole = _piece(8.5, 5.5)
    fly = rot(_piece(17, 2.5, 0.9), 20, 19, 4.5)
    return [shell(minus(head, grow(hole, 1))), shell(fly)]


@icon("side-stitch", CAT, "A runner pressing one hand against the side of the waist, with a pain mark",
      tags=["stitch", "cramp", "running", "side pain", "abdominal cramp", "jogging"])
def _(S):
    hip = (11, 13.5)
    rays = [line(seg(*pt(8.8, 12.2, 2.2, a), *pt(8.8, 12.2, 4.2, a))) for a in (150, 195, 240)]
    return [shell(circle(15, 4.5, 2)),
            line(seg(14, 8, 11, 13.5)),
            line(poly([hip, (15, 16), (14, 21)], r=S.r)),
            line(poly([hip, (8.5, 17.5), (5, 18)], r=S.r)),
            line(poly([(13.5, 9), (17, 11.5), (19.5, 9.5)], r=S.r)),
            line(poly([(13.5, 9), (10.5, 10.5), (11.2, 12)], r=S.r))] + rays


@icon("body-map", CAT, "Two small standing figures side by side, one seen from the front and one from the back",
      tags=["body chart", "pain map", "front and back", "body diagram", "symptom map", "anatomy"])
def _(S):
    def fig(cx):
        body = L(S, f"M{fmt(cx - 3.5)} 16V10.5C{fmt(cx - 3.5)} 9.4 {fmt(cx - 2.6)} 8.5 {fmt(cx - 1.5)} 8.5H{fmt(cx + 1.5)}"
                    f"C{fmt(cx + 2.6)} 8.5 {fmt(cx + 3.5)} 9.4 {fmt(cx + 3.5)} 10.5V16H{fmt(cx + 2)}V21H{fmt(cx - 2)}V16Z",
                 f"M{fmt(cx - 3.5)} 15V10.5C{fmt(cx - 3.5)} 9.4 {fmt(cx - 2.6)} 8.5 {fmt(cx - 1.5)} 8.5H{fmt(cx + 1.5)}"
                    f"C{fmt(cx + 2.6)} 8.5 {fmt(cx + 3.5)} 9.4 {fmt(cx + 3.5)} 10.5V15Q{fmt(cx + 3.5)} 16 {fmt(cx + 2.5)} 16"
                    f"H{fmt(cx + 2)}V20Q{fmt(cx + 2)} 21 {fmt(cx + 1)} 21H{fmt(cx - 1)}Q{fmt(cx - 2)} 21 {fmt(cx - 2)} 20V16"
                    f"H{fmt(cx - 2.5)}Q{fmt(cx - 3.5)} 16 {fmt(cx - 3.5)} 15Z")
        return [shell(circle(cx, 5, 2.2)), shell(body)]
    return fig(6.5) + fig(17.5) + [dot(6.5, 12.5, 0.9), detail(seg(17.5, 10, 17.5, 16))]


@icon("gene-mutation", CAT, "A short DNA double helix with one rung broken and a mismatched piece in its place",
      tags=["mutation", "genetics", "dna damage", "genetic disorder", "gene", "variant"])
def _(S):
    return [line("M3 7C7.5 7 7.5 17 12 17C16.5 17 16.5 7 21 7"),
            line("M3 17C7.5 17 7.5 7 12 7C16.5 7 16.5 17 21 17"),
            line(seg(3.8, 8.5, 3.8, 15.5)), line(seg(20.2, 8.5, 20.2, 15.5)),
            line(seg(12, 8.5, 12, 10.2)), solid(rot(rect(10.4, 12.2, 3.2, 3.2, L(S, 0, 0.8)), 45, 12, 13.8))]
