"""TypeIcon Core: healthcare services (batch healthcare_001).

Care settings, therapies, dental and eye procedures, clinics and digital health services. Medical crosses are
plain plus signs (no red-cross emblem). Overlapping objects are drawn as layers (front first): back layers are
cut away around the front silhouette with a gap so the drawing stays readable at 16 px.
"""
import math

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path

from dsl import Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import LINE, D, I, P, ST, U, fmt, path_to_d, polar, rotation  # noqa: F401

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


def move(d, dx, dy, s=1.0, ox=12.0, oy=12.0):
    """Scale about (ox, oy) then translate."""
    return xf(d, (s, 0, 0, s, ox - s * ox + dx, oy - s * oy + dy))


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


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def plus(cx, cy, a):
    """Plus sign (two strokes) centred on (cx, cy) with arm length a."""
    return f"M{fmt(cx - a)} {fmt(cy)}H{fmt(cx + a)}M{fmt(cx)} {fmt(cy - a)}V{fmt(cy + a)}"


def cross_d(cx, cy, a, t):
    """Closed plus-shaped outline: arm half-length a, arm half-width t."""
    return poly([(cx - t, cy - a), (cx + t, cy - a), (cx + t, cy - t), (cx + a, cy - t), (cx + a, cy + t), (cx + t, cy + t),
                 (cx + t, cy + a), (cx - t, cy + a), (cx - t, cy + t), (cx - a, cy + t), (cx - a, cy - t), (cx - t, cy - t)],
                closed=True)


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


HEART = "M12 20L4.4 12.6A4.6 4.6 0 0 1 11 6.3L12 7.3L13 6.3A4.6 4.6 0 0 1 19.6 12.6Z"
HEART_R = ("M10.6 18.6L4.4 12.6A4.6 4.6 0 0 1 11 6.3L11.3 6.6Q12 7.3 12.7 6.6L13 6.3A4.6 4.6 0 0 1 19.6 12.6"
           "L13.4 18.6Q12 20 10.6 18.6Z")


def heart(S, cx=12.0, cy=12.0, s=1.0):
    """Heart centred near (cx, cy); s = 1 is 15 px wide."""
    return move(L(S, HEART, HEART_R), cx - 12, cy - 12.6, s, 12, 12.6)


def sparkle(cx, cy, r):
    k = r * 0.18
    return (f"M{fmt(cx)} {fmt(cy - r)}Q{fmt(cx + k)} {fmt(cy - k)} {fmt(cx + r)} {fmt(cy)}"
            f"Q{fmt(cx + k)} {fmt(cy + k)} {fmt(cx)} {fmt(cy + r)}Q{fmt(cx - k)} {fmt(cy + k)} {fmt(cx - r)} {fmt(cy)}"
            f"Q{fmt(cx - k)} {fmt(cy - k)} {fmt(cx)} {fmt(cy - r)}Z")


def pulse(x0, y, x1, h=3.0, r=0.0, simple=False):
    """Heartbeat trace from x0 to x1 on baseline y with a spike of height h (simple: one peak, for small screens)."""
    w = x1 - x0
    if simple:
        return poly([(x0, y), (x0 + w * 0.3, y), (x0 + w * 0.5, y - h), (x0 + w * 0.7, y), (x1, y)], r=r)
    pts = [(x0, y), (x0 + w * 0.3, y), (x0 + w * 0.42, y - h * 0.55), (x0 + w * 0.56, y + h * 0.75),
           (x0 + w * 0.7, y - h), (x0 + w * 0.8, y), (x1, y)]
    return poly(pts, r=r)


def arrow_arc(S, cx, cy, r, a0, a1, head=2.5):
    """Clockwise arc from a0 to a1 (degrees) with a chevron head at a1."""
    tip = polar(cx, cy, r, a1)
    t = math.radians(a1)
    back = math.degrees(math.atan2(-math.cos(t), math.sin(t)))  # opposite of the clockwise tangent
    p1, p2 = polar(tip[0], tip[1], head, back - 45), polar(tip[0], tip[1], head, back + 45)
    return [line(arc(cx, cy, r, a0, a1)), line(poly([p1, tip, p2], r=S.r * 0.5))]


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled shell."""
    return Part("dot", d)


# --------------------------------------------------------------------------- layering (front layer first)

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


# ============================================================================ specialties and procedures

@icon("pediatric-care", CAT, "Teddy bear wearing a stethoscope around its neck",
      tags=["pediatrics", "paediatrics", "children", "kids", "pediatrician", "child health"], aliases=["paediatric-care"])
def _(S):
    bear = union(circle(12, 7.5, 4.25), circle(7.4, 4.3, 2.1), circle(16.6, 4.3, 2.1),
                 rect(4.5, 12, 15, 9.5, L(S, 3, 4.75)))
    return [
        shell(bear),
        dot(10.3, 7, 1), dot(13.7, 7, 1),
        detail("M8.5 12.5V14.75A3.5 3.5 0 0 0 15.5 14.75V12.5"),
        dot(12, 18.25, 1.6),
    ]


@layered("family-medicine", "Two adults and a child under a roof with a medical cross",
         tags=["family doctor", "general practice", "gp", "primary care", "family", "clinic"], aliases=["general-practice"])
def _(S):
    def person(cx, hy, hr, top, hw, bottom=21.5):
        rr = L(S, min(hw - 1.5, 2), hw - 0.5)
        body = (f"M{fmt(cx - hw)} {fmt(bottom)}V{fmt(top + rr)}A{fmt(rr)} {fmt(rr)} 0 0 1 {fmt(cx - hw + rr)} {fmt(top)}"
                f"H{fmt(cx + hw - rr)}A{fmt(rr)} {fmt(rr)} 0 0 1 {fmt(cx + hw)} {fmt(top + rr)}V{fmt(bottom)}")
        return [shell(circle(cx, hy, hr)), line(body)]
    return [
        person(12, 15.5, 1.75, 19.25, 2.75),
        person(6.5, 12.5, 2, 16.5, 3.5) + person(17.5, 12.5, 2, 16.5, 3.5),
        [line(poly([(2.5, 10), (12, 2.5), (21.5, 10)], r=S.r)), line(plus(12, 7.5, 1.75))],
    ]


def _sex_heart(S, cx, cy):
    return mark(heart(S, cx, cy + 0.2, 0.36))


@icon("womens-health", CAT, "Female symbol with a heart inside the circle",
      tags=["women", "female", "gynecology", "gynaecology", "obgyn", "wellness"], aliases=["womens-healthcare"])
def _(S):
    return [
        shell(circle(12, 8.5, 6)),
        _sex_heart(S, 12, 8.5),
        line(seg(12, 14.5, 12, 21.5)),
        line(seg(8.5, 18.5, 15.5, 18.5)),
    ]


@icon("mens-health", CAT, "Male symbol with a heart inside the circle",
      tags=["men", "male", "urology", "andrology", "wellness", "screening"], aliases=["mens-healthcare"])
def _(S):
    return [
        shell(circle(9.5, 14.5, 6)),
        _sex_heart(S, 9.5, 14.5),
        line(seg(13.75, 10.25, 20.5, 3.5)),
        line(poly([(14.5, 3.5), (20.5, 3.5), (20.5, 9.5)], r=S.r * 0.5)),
    ]


@icon("heart-surgery", CAT, "Heart with a stitched incision down its front",
      tags=["cardiac surgery", "cardiothoracic", "bypass", "open heart", "cardiology", "operation"],
      aliases=["cardiac-surgery"])
def _(S):
    return [
        shell(heart(S, 12, 12, 1.2)),
        detail(seg(12, 9.5, 12, 18)),
        detail(seg(10, 11.5, 14, 11.5)),
        detail(seg(10, 15.25, 14, 15.25)),
    ]


_KIDNEY = ("M9 4C5.5 4 3.5 7.5 3.5 12C3.5 17 6 20.5 9.5 20.5C12 20.5 13 18.5 12.3 16.5C11.8 15 11 14.2 11 12.5"
           "C11 10.8 11.8 10 12.3 8.5C13 6.3 11.8 4 9 4Z")


@icon("organ-transplant", CAT, "Kidney with a curved transfer arrow beside it",
      tags=["transplant", "organ donation", "donor", "kidney", "transplantation", "surgery"], aliases=["transplant"])
def _(S):
    return [
        shell(_KIDNEY),
        *arrow_arc(S, 12.5, 12.25, 7.5, -65, 65, 3),
    ]


@layered("sports-medicine", "Soccer ball with an adhesive bandage across it",
         tags=["sports injury", "athlete", "physio", "injury", "sports", "football"], aliases=["sports-injury"])
def _(S):
    m = axis((12, 12), -45)
    disc = P(circle(12, 12, 8.5))
    patches = []
    for a in (-135, 45):
        c = polar(12, 12, 9, a)
        patches.append(mark(path_to_d(I(P(poly(regular(c[0], c[1], 3.6, 5, a + 180), closed=True, r=S.r * 0.4)), disc))))
    pad = rect(10.25, 10.25, 3.5, 3.5, L(S, 0, 1.75))
    return [
        [shell(stadium(m, -10.5, 10.5, 3.25, L(S, 1.5, 3.25))), mark(pad)],
        [shell(circle(12, 12, 9)), *patches],
    ]


@icon("occupational-health", CAT, "Hard hat seen from the side with a medical cross on its dome",
      tags=["workplace health", "occupational medicine", "work safety", "employee health", "industrial", "safety"],
      aliases=["workplace-health"])
def _(S):
    return [
        shell(L(S, "M4 16V13.5C4 8.5 7.5 5 12 5C16.5 5 20 8.5 20 13.5V16Z",
                "M4 16V13.5C4 8.5 7.5 5 12 5C16.5 5 20 8.5 20 13.5V16Z")),
        shell(rect(2, 16, 20, 3.5, L(S, 0.5, 1.75))),
        detail(plus(12, 11, 2.5)),
    ]


@layered("travel-vaccination", "Passport with a syringe laid across it",
         tags=["travel vaccine", "immunization", "immunisation", "travel health", "yellow fever", "passport"],
         aliases=["travel-vaccine"])
def _(S):
    m = axis((15, 15), -45)
    return [
        [shell(stadium(m, -4.5, 4, 2.5, L(S, 0.5, 1.5))),
         line(mseg(m, 4, 0, 8.5, 0)),
         line(mseg(m, -8, 0, -4.5, 0)), line(mseg(m, -8, -2.5, -8, 2.5))],
        [shell(rect(3.5, 2.5, 13, 17, L(S, 1.5, 3))),
         detail(circle(10, 8.5, 3.25)), detail(seg(6.75, 8.5, 13.25, 8.5)), detail(seg(7, 15, 10, 15))],
    ]


_TOOTH2 = ("M7 7C5 7 4 8.5 4 10.5C4 12.5 5 14 5.8 15.5L7 20.5C7.3 21.8 8.9 21.8 9.2 20.5L10.3 16.5H13.7L14.8 20.5"
           "C15.1 21.8 16.7 21.8 17 20.5L18.2 15.5C19 14 20 12.5 20 10.5C20 8.5 19 7 17 7C15.2 7 14 7.8 12 7.8"
           "C10 7.8 8.8 7 7 7Z")
_TOOTH2_L = ("M7 7C5 7 4 8.5 4 10.5C4 12.5 5 14 5.8 15.5L7.2 21.5H9L10.3 16.5H13.7L15 21.5H16.8L18.2 15.5"
             "C19 14 20 12.5 20 10.5C20 8.5 19 7 17 7C15.2 7 14 7.8 12 7.8C10 7.8 8.8 7 7 7Z")


@icon("root-canal", CAT, "Tooth with a thin file inserted down one root canal",
      tags=["endodontics", "endodontic", "dentist", "tooth", "canal", "dental treatment"], aliases=["endodontic-treatment"])
def _(S):
    return [
        shell(L(S, _TOOTH2_L, _TOOTH2)),
        shell(rect(6.5, 2, 5, 2.5, L(S, 0, 1.25))),
        line(seg(9, 4.5, 9, 6.5)),
        detail(seg(9, 7.5, 9.1, 17)),
        detail(seg(15, 12, 14.9, 17)),
    ]


def _house(S, x0=3.5, x1=20.5, top=10.5, peak=3.5, bottom=21.5):
    cx = (x0 + x1) / 2
    return poly([(x0, bottom), (x0, top), (cx, peak), (x1, top), (x1, bottom)], closed=True, r=S.r)


@icon("hospice", CAT, "House with a heart inside for end-of-life comfort care",
      tags=["palliative care", "end of life", "comfort care", "care home", "compassion", "terminal care"],
      aliases=["palliative-care"])
def _(S):
    return [shell(_house(S)), mark(heart(S, 12, 14.75, 0.5))]


@icon("prenatal-care", CAT, "Pregnant person in profile with a stethoscope chest piece at the belly",
      tags=["antenatal", "pregnancy", "prenatal", "obstetrics", "expecting", "maternity"], aliases=["antenatal-care"])
def _(S):
    body = L(S, "M6.5 9H10C11 9 11.6 9.7 11.8 10.4C14.3 11.2 15.5 13 15.5 15C15.5 16.8 14.3 18 12.5 18H11.5V21.5H6.5"
                "C6.5 17.5 5.8 13.7 5.8 11C5.8 9.9 6 9 6.5 9Z",
             "M6.8 9H10C11 9 11.6 9.7 11.8 10.4C14.3 11.2 15.5 13 15.5 15C15.5 16.8 14.3 18 12.5 18H11.5V20.5"
                "Q11.5 21.5 10.5 21.5H7.5Q6.5 21.5 6.5 20.5C6.5 17 5.8 13.7 5.8 11C5.8 9.9 6 9 6.8 9Z")
    return [
        shell(circle(8.5, 4.5, 2.5)),
        shell(body),
        shell(circle(19.5, 15, 1.75)),
        line(L(S, "M19.5 13.25V9.5A2.5 2.5 0 0 0 17 7H15", "M19.5 13.25V9.5A2.5 2.5 0 0 0 17 7H15")),
    ]


@icon("egg-freezing", CAT, "Cryogenic vial holding an egg cell with a snowflake beside it",
      tags=["oocyte cryopreservation", "fertility preservation", "ivf", "fertility", "frozen eggs", "cryopreservation"],
      aliases=["oocyte-freezing"])
def _(S):
    flake = "".join(seg(*polar(17.5, 8.5, 3.75, a), *polar(17.5, 8.5, 3.75, a + 180)) for a in (-90, -30, 30))
    return [
        shell(rect(3, 2.5, 9, 3.5, L(S, 0.5, 1.5))),
        shell(L(S, "M4 8.5H11V18A3.5 3.5 0 0 1 4 18Z", "M4 9.5A1 1 0 0 1 5 8.5H10A1 1 0 0 1 11 9.5V18A3.5 3.5 0 0 1 4 18Z")),
        dot(7.5, 14.75, 2),
        line(flake),
    ]


def _spiky_cell(cx, cy, r, n=6, k=1.75, a0=-90):
    parts = [dot(cx, cy, r)]
    parts += [detail(seg(*polar(cx, cy, r + 1.25, a0 + i * 360 / n), *polar(cx, cy, r + 1.25 + k, a0 + i * 360 / n)))
              for i in range(n)]
    return parts


@icon("chemotherapy", CAT, "Drip bag marked with a spiky cell and a tube running down",
      tags=["chemo", "cancer treatment", "oncology", "infusion", "cancer", "drip"], aliases=["chemo"])
def _(S):
    bag = [(4.5, 3), (19.5, 3), (19.5, 13), (15, 17), (9, 17), (4.5, 13)]
    return [
        shell(poly(bag, closed=True, r=S.r)),
        *_spiky_cell(12, 9.75, 1.75, 6, 1.5),
        line(seg(12, 17, 12, 21.5)),
    ]


@icon("neonatal-phototherapy", CAT, "Newborn in a bassinet under a lamp bar shining down",
      tags=["jaundice", "bili light", "newborn", "nicu", "blue light", "neonatal"], aliases=["bili-light"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 3.5, L(S, 0.5, 1.75))),
        line(seg(7, 8.5, 7, 11)), line(seg(12, 8.5, 12, 11)), line(seg(17, 8.5, 17, 11)),
        shell(poly([(2.5, 14), (21.5, 14), (19, 21.5), (5, 21.5)], closed=True, r=S.r)),
        dot(7.75, 17.5, 1.6),
        detail(seg(11, 17.5, 16.5, 17.5)),
    ]


@layered("gene-therapy", "Short DNA double helix with a syringe needle pointing into one strand",
         tags=["genetic therapy", "dna", "genome editing", "crispr", "genetics", "biotech"], aliases=["genetic-therapy"])
def _(S):
    m = axis((13, 11), -45)
    return [
        [line(mseg(m, 0.5, 0, 4, 0)),
         shell(stadium(m, 4, 10, 2.25, L(S, 0.5, 1.5))),
         line(mseg(m, 10, 0, 12, 0)), line(mseg(m, 12, -2.25, 12, 2.25))],
        [line("M3.5 2.5C3.5 7.5 10.5 7.5 10.5 12C10.5 16.5 3.5 16.5 3.5 21.5"),
         line("M10.5 2.5C10.5 7.5 3.5 7.5 3.5 12C3.5 16.5 10.5 16.5 10.5 21.5"),
         line(seg(5, 12, 9, 12)), line(seg(5.5, 3.25, 8.5, 3.25)), line(seg(5.5, 20.75, 8.5, 20.75))],
    ]


@icon("speech-therapy", CAT, "Head in profile speaking into a speech bubble with the letter A",
      tags=["speech language therapy", "slp", "speech pathology", "logopedics", "articulation", "stutter"],
      aliases=["speech-language-therapy"])
def _(S):
    headp = L(S, "M4 21.5V18.5C2.5 17 2 15 2.5 13C3.2 10.3 5.5 9 8 9C10.5 9 12 10.8 12 13L13.5 15.5L12 16V18.5H9V21.5",
              "M4 21.5V18.5C2.5 17 2 15 2.5 13C3.2 10.3 5.5 9 8 9C10.5 9 12 10.8 12 13L13.2 15Q13.5 15.5 13 15.7L12 16V17.5"
              "Q12 18.5 11 18.5H9V21.5")
    bubble = L(S, "M13 2.5H21.5V11H16.5L14 13.5V11H13Z",
               "M14.5 2.5H20A1.5 1.5 0 0 1 21.5 4V9.5A1.5 1.5 0 0 1 20 11H16.5L14 13.5V11A1 1 0 0 1 13 10V4A1.5 1.5 0 0 1 14.5 2.5Z")
    return [
        line(headp),
        shell(bubble),
        detail(poly([(15, 9), (17.25, 4.5), (19.5, 9)], r=S.r * 0.3)),
    ]


@icon("art-therapy", CAT, "Painter's palette with a heart shaped paint dab in the middle",
      tags=["creative therapy", "art", "painting", "expressive therapy", "mental health", "wellbeing"],
      aliases=["creative-arts-therapy"])
def _(S):
    pal = ("M12 2.5C6.5 2.5 2.5 6.5 2.5 12C2.5 17.5 6.5 21.5 11.5 21.5C13.5 21.5 14.3 20.2 13.8 18.7C13.3 17 14.3 15.5 16 15.5"
           "H18C20.3 15.5 21.5 14 21.5 11.5C21.5 6.3 17.3 2.5 12 2.5Z")
    return [
        shell(pal),
        mark(heart(S, 11, 11.5, 0.42)),
        dot(7, 15.5, 1.5), dot(16.5, 7.5, 1.5) if S.name == "rounded" else mark(rect(15, 6, 3, 3)),
    ]


@icon("music-therapy", CAT, "Musical eighth note with a heart for its note head",
      tags=["music", "sound therapy", "wellbeing", "therapy", "healing", "mental health"], aliases=["sound-therapy"])
def _(S):
    return [
        shell(heart(S, 8.5, 16.5, 0.52)),
        line(seg(12, 15.5, 12, 2.5)),
        line(L(S, "M12 2.5L19 7.5V11.5", "M12 2.5C14 5.5 19 5.5 19 11")),
    ]


@icon("vr-therapy", CAT, "Virtual reality headset with a small heart above it",
      tags=["virtual reality", "vr", "exposure therapy", "digital therapy", "rehabilitation", "headset"],
      aliases=["virtual-reality-therapy"])
def _(S):
    body = L(S, "M2.5 11H21.5V20.5H15L13.5 18H10.5L9 20.5H2.5Z",
             "M5.5 11H18.5A3 3 0 0 1 21.5 14V17.5A3 3 0 0 1 18.5 20.5H15L13.5 18H10.5L9 20.5H5.5A3 3 0 0 1 2.5 17.5V14A3 3 0 0 1 5.5 11Z")
    return [shell(body), mark(heart(S, 12, 5.25, 0.45))]


_MOLAR = ("M7.5 3C5 3 3.5 5 3.5 7.5C3.5 10.5 5 12 5.5 14.5L6.5 20C6.8 21.5 8.7 21.5 9 20L10 15.5H14L15 20"
          "C15.3 21.5 17.2 21.5 17.5 20L18.5 14.5C19 12 20.5 10.5 20.5 7.5C20.5 5 19 3 16.5 3C14.8 3 14 4 12 4C10 4 9.2 3 7.5 3Z")
_MOLAR_L = ("M7.5 3C5 3 3.5 5 3.5 7.5C3.5 10.5 5 12 5.5 14.5L6.8 21.5H8.8L10 15.5H14L15.2 21.5H17.2L18.5 14.5"
            "C19 12 20.5 10.5 20.5 7.5C20.5 5 19 3 16.5 3C14.8 3 14 4 12 4C10 4 9.2 3 7.5 3Z")


def molar(S, dx=0, dy=0, s=1.0, ox=12, oy=12):
    return move(L(S, _MOLAR_L, _MOLAR), dx, dy, s, ox, oy)


@icon("tooth-extraction", CAT, "Molar lifted clear above the gum line with an arrow above it",
      tags=["tooth removal", "pulled tooth", "oral surgery", "dentist", "extraction", "wisdom tooth"],
      aliases=["tooth-removal"])
def _(S):
    return [
        shell(molar(S, 0, 1.5, 0.6, 12, 9)),
        line(poly([(9, 4.5), (12, 2), (15, 4.5)], r=S.r * 0.5)),
        line("M2.5 21.5C5 18.5 8 18 12 18C16 18 19 18.5 21.5 21.5"),
    ]


@icon("dental-crown", CAT, "Crown cap hovering above a filed down tooth stump in the gum",
      tags=["tooth crown", "dental cap", "prosthodontics", "dentist", "restoration", "cap"], aliases=["tooth-crown"])
def _(S):
    cap = L(S, "M5.5 10V8C5.5 4.5 8 2.5 12 2.5C16 2.5 18.5 4.5 18.5 8V10Z",
            "M6.5 10A1 1 0 0 1 5.5 9V8C5.5 4.5 8 2.5 12 2.5C16 2.5 18.5 4.5 18.5 8V9A1 1 0 0 1 17.5 10Z")
    return [
        shell(cap),
        shell(poly([(8, 18), (9, 13.5), (15, 13.5), (16, 18)], closed=True, r=S.r * 0.5)),
        line("M2.5 21.5C4 19 5.5 18 8 18H16C18.5 18 20 19 21.5 21.5"),
    ]


@icon("dental-filling", CAT, "Molar with a solid filling patch on its biting surface",
      tags=["cavity filling", "tooth filling", "amalgam", "composite", "dentist", "cavity"], aliases=["tooth-filling"])
def _(S):
    return [shell(molar(S)), mark(rect(9, 7.5, 6, 3.5, L(S, 0, 1.75)))]


@icon("eyeglass-prescription", CAT, "Prescription sheet with a pair of glasses and a grid of values",
      tags=["glasses prescription", "optometry", "optician", "vision test", "lens prescription", "eye exam"],
      aliases=["glasses-prescription"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, min(S.R, 2.5))),
        detail(circle(8.75, 8.5, 2.25)), detail(circle(15.25, 8.5, 2.25)), detail(seg(11, 8.5, 13, 8.5)),
        detail(seg(7, 14, 17, 14)), detail(seg(7, 17.5, 17, 17.5)), detail(seg(12, 13, 12, 18.5)),
    ]


def _e(S, x, y, s, deg):
    """Letter E of size s (facing right when deg = 0) with its top-left corner at (x, y)."""
    d = poly([(x + s, y), (x, y), (x, y + s), (x + s, y + s)], r=S.r * 0.3) + seg(x, y + s / 2, x + s * 0.85, y + s / 2)
    return rot(d, deg, x + s / 2, y + s / 2)


@icon("tumbling-e-chart", CAT, "Eye chart of capital E shapes facing different ways and shrinking row by row",
      tags=["tumbling e", "e chart", "vision test", "eye test", "visual acuity", "optometry"], aliases=["e-chart"])
def _(S):
    return [
        line(_e(S, 7.5, 2.5, 9, 0)),
        line(_e(S, 3.5, 15, 6.5, 90)),
        line(_e(S, 14, 15, 6.5, 180)),
    ]


@icon("audiogram", CAT, "Hearing test graph with a line of circles and a line of crosses sloping down",
      tags=["hearing test", "audiometry", "hearing loss", "audiology", "hearing", "chart"], aliases=["hearing-chart"])
def _(S):
    pts = [(8, 5.5), (13, 8), (18, 12.5)]
    xs = [(8, 12), (13, 14.5), (18, 18)]
    parts = [line(poly([(2.5, 2.5), (2.5, 21.5), (21.5, 21.5)], r=S.r))]
    parts += [shell(circle(x, y, 1.5)) for x, y in pts]
    parts += [line(seg(pts[i][0] + 1.9, pts[i][1] + 0.95, pts[i + 1][0] - 1.9, pts[i + 1][1] - 1.4)) for i in range(2)]
    parts += [line(seg(x - 1.5, y - 1.5, x + 1.5, y + 1.5) + seg(x - 1.5, y + 1.5, x + 1.5, y - 1.5)) for x, y in xs]
    return parts


# ============================================================================ care settings and vehicles

_DROP = "M12 3C12 3 7 9 7 12.5A5 5 0 0 0 17 12.5C17 9 12 3 12 3Z"


def drop(cx, cy, s):
    """Liquid drop centred near (cx, cy); s = 1 is 10 px wide."""
    return move(_DROP, cx - 12, cy - 11.5, s, 12, 11.5)


def bolt(S):
    return poly([(20, 2.5), (16, 10.5), (19, 10.5), (17, 17), (21.5, 8), (18.5, 8), (21, 2.5)], closed=True, r=S.r * 0.2)


@icon("urgent-care", CAT, "Clinic building with a medical cross and a lightning bolt beside it",
      tags=["urgent care center", "walk-in", "same day care", "minor injuries", "clinic", "immediate care"],
      aliases=["urgent-care-center"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 12, 15, min(S.R, 3))),
        detail(plus(8.5, 11, 2.25)),
        detail(poly([(6.5, 21.5), (6.5, 17), (10.5, 17), (10.5, 21.5)], r=S.r * 0.5)),
        shell(poly([(20.5, 2.5), (17, 10), (19.5, 10), (18, 16.5), (22, 7.5), (19.5, 7.5), (21.5, 2.5)], closed=True, r=S.r * 0.2),
              stroke_miterlimit="2"),
    ]


@icon("walk-in-clinic", CAT, "Open doorway under a medical cross with a person walking through",
      tags=["walk in", "no appointment", "drop in clinic", "clinic", "outpatient", "health center"],
      aliases=["walk-in-centre"])
def _(S):
    return [
        line(poly([(3, 21.5), (3, 9), (12, 9), (12, 21.5)], r=S.r)),
        line(plus(7.5, 4.5, 2)),
        dot(17, 8.5, 2),
        line(poly([(14, 15.5), (16.5, 12.5), (19.5, 15)], r=S.r * 0.5)),
        line(seg(16.5, 12.5, 15.5, 17)),
        line(poly([(13.5, 21.5), (15.5, 17), (18.5, 21.5)], r=S.r * 0.5)),
    ]


@icon("maternity-ward", CAT, "Hospital bed with a bassinet holding a baby beside it",
      tags=["labor and delivery", "postnatal", "birth", "obstetrics", "newborn", "maternity unit"],
      aliases=["maternity-unit"])
def _(S):
    return [
        line(seg(2.5, 9, 2.5, 21.5)),
        line(poly([(2.5, 17), (12.5, 17), (12.5, 21.5)], r=S.r)),
        dot(6, 13.5, 1.75),
        line(seg(8.75, 14, 11.5, 14)),
        shell(L(S, "M14 11H21.5V12.5A3.75 3.75 0 0 1 14 12.5Z", "M14.75 11H20.75A0.75 0.75 0 0 1 21.5 11.75V12.5A3.75 3.75 0 0 1 14 12.5V11.75A0.75 0.75 0 0 1 14.75 11Z")),
        dot(17.75, 7.5, 1.75),
        line(seg(15, 21.5, 20.5, 16.5)), line(seg(15, 16.5, 20.5, 21.5)),
    ]


@icon("intensive-care-unit", CAT, "Patient bed with a heart monitor above and an IV bag on a pole",
      tags=["icu", "critical care", "intensive care", "life support", "hospital", "ccu"], aliases=["icu"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 11, 7.5, min(S.R, 2))),
        detail(pulse(4.5, 7.5, 11.5, 3, simple=True)),
        shell(rect(16.5, 2.5, 5, 5.5, min(S.R, 1.5))),
        line(seg(19, 8, 19, 21.5)), line(seg(16.5, 21.5, 21.5, 21.5)),
        line(seg(2.5, 12.5, 2.5, 21.5)),
        line(poly([(2.5, 18), (15, 18), (15, 21.5)], r=S.r)),
        dot(6, 14.75, 1.75),
    ]


@layered("mobile-clinic", "Van with a medical cross on its side and an awning extended from the roof",
         tags=["clinic on wheels", "health van", "outreach", "mobile health unit", "community health", "screening van"],
         aliases=["mobile-health-unit"])
def _(S):
    return [
        [shell(circle(10, 18, 2)), shell(circle(18, 18, 2))],
        [shell(poly([(7, 18), (7, 6), (17, 6), (17, 9.5), (19.5, 9.5), (21.5, 13), (21.5, 18)], closed=True, r=S.r)),
         detail(plus(11.5, 11, 2)),
         line(poly([(6, 6), (2.5, 10), (2.5, 21.5)], r=S.r))],
    ]


@layered("house-call", "House with a doctor's bag standing in front of the door",
         tags=["home visit", "doctor visit", "home care", "domiciliary visit", "visiting nurse", "family doctor"],
         aliases=["home-visit"])
def _(S):
    return [
        [shell(rect(10.5, 13, 11, 8.5, min(S.R, 2.5))), line(poly([(13.5, 13), (13.5, 10.5), (18.5, 10.5), (18.5, 13)], r=S.r * 0.4)),
         detail(plus(16, 17.25, 1.75))],
        [shell(_house(S, 2.5, 17.5, 10, 3, 21.5)), detail(poly([(6, 21.5), (6, 15), (9.5, 15), (9.5, 21.5)], r=S.r * 0.4))],
    ]


@icon("health-post", CAT, "Small hut with a pitched roof beside a flag bearing a medical cross",
      tags=["rural clinic", "health outpost", "community health", "dispensary", "field clinic", "village clinic"],
      aliases=["health-outpost"])
def _(S):
    flag = minus(rect(16, 2.5, 6, 5.5, L(S, 0, 1)), path_to_d(ST(plus(19, 5.25, 1.6), 1.5)))
    return [
        shell(poly([(2.5, 21.5), (2.5, 13), (8, 7.5), (13.5, 13), (13.5, 21.5)], closed=True, r=S.r)),
        detail(poly([(6, 21.5), (6, 16.5), (10, 16.5), (10, 21.5)], r=S.r * 0.4)),
        line(seg(16, 2.5, 16, 21.5)),
        solid(flag),
    ]


@icon("hospital-ward", CAT, "Two beds separated by a curtain hanging from a rail",
      tags=["ward", "inpatient", "patient room", "beds", "hospital", "admission"], aliases=["patient-ward"])
def _(S):
    parts = [line(seg(2.5, 3, 21.5, 3)), shell(poly([(10.5, 3), (13.5, 3), (13.5, 14), (12, 13), (10.5, 14)], closed=True, r=S.r * 0.3))]
    for x0, sgn in ((2.5, 1), (21.5, -1)):
        parts += [line(seg(x0, 10, x0, 21.5)),
                  line(poly([(x0, 17.5), (x0 + sgn * 6.5, 17.5), (x0 + sgn * 6.5, 21.5)], r=S.r)),
                  dot(x0 + sgn * 3.25, 14.25, 1.5)]
    return parts


@icon("childrens-hospital", CAT, "Hospital building with a medical cross and a balloon by the entrance",
      tags=["pediatric hospital", "paediatric hospital", "kids hospital", "children", "hospital", "pediatrics"],
      aliases=["pediatric-hospital"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 13, 15, min(S.R, 3))),
        detail(plus(9, 11, 2.25)),
        detail(poly([(7, 21.5), (7, 17), (11, 17), (11, 21.5)], r=S.r * 0.5)),
        shell(ellipse(19, 6, 2.5, 3.25) if S.name == "rounded" else "M19 2.75C20.5 2.75 21.5 4 21.5 5.75C21.5 7.5 20.3 9.25 19 9.25C17.7 9.25 16.5 7.5 16.5 5.75C16.5 4 17.5 2.75 19 2.75Z"),
        line("M19 10.25C19 12.5 20.5 13.5 20.5 15.5C20.5 17.5 19 18.5 19 21.5"),
    ]


@layered("bloodmobile", "Bus with a large blood drop on its side and an open door",
         tags=["blood drive", "blood donation", "donor bus", "blood bank", "mobile donation", "donate blood"],
         aliases=["blood-drive-bus"])
def _(S):
    return [
        [shell(circle(7, 18.5, 2)), shell(circle(17, 18.5, 2))],
        [shell(rect(2.5, 4.5, 19, 14, S.R)),
         mark(drop(8.5, 11, 0.55)),
         detail(poly([(14.5, 18.5), (14.5, 8.5), (18.5, 8.5), (18.5, 18.5)], r=S.r * 0.4))],
    ]


@icon("prescription-locker", CAT, "Bank of lockers under a medical cross with one compartment holding a pill bottle",
      tags=["pharmacy locker", "pickup locker", "medication pickup", "click and collect", "pharmacy", "24 hour pickup"],
      aliases=["pharmacy-locker"])
def _(S):
    return [
        line(plus(12, 3.75, 1.75)),
        shell(rect(2.5, 8, 19, 13.5, min(S.R, 2.5))),
        detail(seg(12, 8, 12, 21.5)), detail(seg(2.5, 14.75, 21.5, 14.75)),
        mark(rect(15, 10, 4, 1.5)), mark(rect(15.5, 11.5, 3, 1.75, L(S, 0, 0.5))),
        dot(9.5, 11.5, 1), dot(9.5, 18, 1), dot(19, 18, 1),
    ]


@icon("medicine-vending-machine", CAT, "Vending machine with medicine boxes behind glass and a medical cross on top",
      tags=["pharmacy vending", "medication dispenser", "automated pharmacy", "vending", "otc", "self service"],
      aliases=["pharmacy-vending-machine"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, min(S.R, 2.5))),
        detail(plus(8, 6.25, 1.75)),
        mark(rect(6.5, 10.5, 3, 2.5)), mark(rect(11, 10.5, 3, 2.5)),
        mark(rect(6.5, 14.5, 3, 2.5)), mark(rect(11, 14.5, 3, 2.5)),
        detail(seg(17, 10.5, 17, 13.5)),
        detail(seg(6.5, 19, 14, 19)),
    ]


@icon("health-kiosk", CAT, "Freestanding health kiosk with a screen and a blood pressure cuff at its side",
      tags=["health station", "self check", "blood pressure kiosk", "screening", "pharmacy", "vitals"],
      aliases=["health-station"])
def _(S):
    return [
        shell(rect(3, 2.5, 12, 9, min(S.R, 2.5))),
        detail(pulse(5, 8, 13, 3, simple=True)),
        line(seg(9, 11.5, 9, 21.5)), line(seg(4.5, 21.5, 13.5, 21.5)),
        line(poly([(15, 6), (19, 6), (19, 13)], r=L(S, 0, 2))),
        shell(rect(16.5, 13, 5, 6.5, min(S.R, 1.5))),
    ]


@icon("infusion-chair", CAT, "Reclining treatment chair with an IV pole and drip bag beside it",
      tags=["infusion", "chemo chair", "iv therapy", "treatment chair", "dialysis chair", "recliner"],
      aliases=["treatment-chair"])
def _(S):
    return [
        line(poly([(2.5, 5), (5, 15), (13.5, 15), (15, 18.5)], r=S.r)),
        line(seg(5.5, 11.5, 11, 11.5)),
        line(seg(8.5, 15, 8.5, 21.5)), line(seg(4.5, 21.5, 12.5, 21.5)),
        shell(rect(16.5, 2.5, 5, 5.5, min(S.R, 1.5))),
        line(seg(19, 8, 19, 21.5)), line(seg(16.5, 21.5, 21.5, 21.5)),
    ]


def _nurse_cap(cx, cy, w):
    h = w * 0.55
    cap = poly([(cx - w / 2, cy + h / 2), (cx - w * 0.35, cy - h / 2), (cx + w * 0.35, cy - h / 2), (cx + w / 2, cy + h / 2)], closed=True)
    return cap


@icon("nurses-station", CAT, "Curved counter with a monitor on top and a nurse cap on the front panel",
      tags=["nursing station", "nurse desk", "ward desk", "hospital", "nurse", "front desk"], aliases=["nursing-station"])
def _(S):
    return [
        shell(L(S, "M2.5 11.5C8 13.5 16 13.5 21.5 11.5V21.5H2.5Z", "M2.5 13C2.5 12 3 11.6 4 12C9 13.5 15 13.5 20 12C21 11.6 21.5 12 21.5 13V20A1.5 1.5 0 0 1 20 21.5H4A1.5 1.5 0 0 1 2.5 20Z")),
        mark(minus(_nurse_cap(12, 17.25, 6.5), path_to_d(ST(plus(12, 17.25, 1.1), 1.2)))),
        shell(rect(12.5, 2.5, 8, 5.5, min(S.R, 1.5))),
        line(seg(16.5, 8, 16.5, 10.5)),
    ]


@layered("clinic-reception", "Reception desk with a service bell and a medical cross sign on the wall",
         tags=["reception", "front desk", "check in", "waiting room", "clinic", "registration"], aliases=["clinic-front-desk"])
def _(S):
    return [
        [shell(rect(2.5, 14, 19, 7.5, min(S.R, 2)))],
        [shell(L(S, "M4.5 12V11A3.5 3.5 0 0 1 11.5 11V12Z", "M5.5 12A1 1 0 0 1 4.5 11A3.5 3.5 0 0 1 11.5 11A1 1 0 0 1 10.5 12Z")),
         dot(8, 5.75, 1.25),
         shell(L(S, cross_d(17.5, 6, 4, 1.5), poly([(16, 2), (19, 2), (19, 4.5), (21.5, 4.5), (21.5, 7.5), (19, 7.5), (19, 10), (16, 10),
                                                     (16, 7.5), (13.5, 7.5), (13.5, 4.5), (16, 4.5)], closed=True, r=0.8)))],
    ]


@icon("patient-call-display", CAT, "Wall screen showing a queue number and an arrow toward a room",
      tags=["queue display", "now serving", "call screen", "waiting room", "ticket number", "queue management"],
      aliases=["queue-display"])
def _(S):
    return [
        line(seg(7, 2.5, 7, 5)), line(seg(17, 2.5, 17, 5)),
        shell(rect(2.5, 5, 19, 13, min(S.R, 2.5))),
        detail(poly([(5.75, 10), (7.5, 8.5), (7.5, 14.5)], r=S.r * 0.3)),
        detail(poly([(9.5, 9.75), (10.5, 8.5), (12, 8.5), (12.75, 9.75), (9.75, 14.5), (13, 14.5)], r=S.r * 0.3)),
        detail(seg(15, 11.5, 19, 11.5)), detail(poly([(17, 9.5), (19, 11.5), (17, 13.5)], r=S.r * 0.3)),
        line(seg(8.5, 21.5, 15.5, 21.5)),
    ]


@icon("surgical-scrub-sink", CAT, "Deep trough sink with a tall gooseneck faucet and a knee lever below",
      tags=["scrub sink", "surgical hand wash", "operating room", "scrubbing in", "hand hygiene", "theatre"],
      aliases=["scrub-sink"])
def _(S):
    return [
        shell(poly([(2.5, 11), (21.5, 11), (19.5, 17), (4.5, 17)], closed=True, r=S.r)),
        line(L(S, "M9 11V5.5A3 3 0 0 1 15 5.5V7.5", "M9 11V5.5A3 3 0 0 1 15 5.5V7.5")),
        line(poly([(12, 17), (12, 21.5)])), line(seg(12, 20, 16.5, 20)),
    ]


@icon("hospital-ship", CAT, "Ship with a medical cross on its superstructure",
      tags=["hospital ship", "medical ship", "floating hospital", "navy", "relief", "humanitarian"],
      aliases=["floating-hospital"])
def _(S):
    return [
        shell(poly([(2.5, 14.5), (21.5, 14.5), (19, 20.5), (5, 20.5)], closed=True, r=S.r * 0.6)),
        shell(rect(6.5, 6.5, 11, 8, min(S.R, 2))),
        detail(plus(12, 10.5, 2)),
        line(seg(12, 2.5, 12, 6.5)),
    ]


@icon("ambulance-boat", CAT, "Small motorboat with a medical cross on its cabin and a warning light on top",
      tags=["water ambulance", "rescue boat", "marine ambulance", "coast guard", "emergency", "lifeboat"],
      aliases=["water-ambulance"])
def _(S):
    return [
        shell(poly([(2.5, 14), (15, 14), (21.5, 11.5), (18.5, 18.5), (4.5, 18.5)], closed=True, r=S.r * 0.6)),
        shell(poly([(4.5, 14), (4.5, 8), (11.5, 8), (14, 14)], closed=True, r=S.r * 0.6)),
        detail(plus(8.25, 11, 1.6)),
        mark(rect(7, 3.5, 2.5, 2.5, L(S, 0, 1.25))),
        line(seg(4, 3, 5, 4)), line(seg(12.5, 3, 11.5, 4)),
        line(L(S, "M2.5 21.5H21.5", "M2.5 21.5H21.5")),
    ]


@icon("hospital-at-home", CAT, "House containing a hospital bed with a heartbeat line above it",
      tags=["home hospital", "virtual ward", "home care", "acute care at home", "remote care", "home health"],
      aliases=["virtual-ward"])
def _(S):
    return [
        shell(_house(S, 2.5, 21.5, 10, 2.5, 21.5)),
        detail(pulse(7, 11.5, 17, 3)),
        detail(seg(6.5, 16, 6.5, 21.5)),
        detail(poly([(6.5, 18.25), (17.5, 18.25), (17.5, 21.5)], r=S.r * 0.5)),
    ]


@layered("paramedic-bicycle", "Bicycle with a pannier marked with a medical cross and a handlebar light",
         tags=["cycle responder", "bike paramedic", "first responder", "emergency", "bicycle", "event medical"],
         aliases=["cycle-response-unit"])
def _(S):
    box = minus(rect(2.5, 8, 7, 6, L(S, 0, 1.5)), path_to_d(ST(plus(6, 11, 1.6), 1.5)))
    return [
        [solid(box)],
        [shell(circle(6, 17, 4)), shell(circle(18, 17, 4)),
         line(poly([(6, 17), (10.5, 10.5), (16, 10.5), (18, 17)], r=S.r * 0.5)),
         line(poly([(10.5, 17), (10.5, 10.5)])), line(poly([(15, 6.5), (16, 10.5)])),
         line(seg(13.5, 6.5, 17.5, 6.5)), dot(20.5, 7, 1.25)],
    ]


@layered("paramedic-response-car", "Estate car with a light bar on its roof and a medical cross on the door",
         tags=["rapid response vehicle", "first responder", "emergency car", "paramedic car", "ems", "fly car"],
         aliases=["rapid-response-car"])
def _(S):
    return [
        [shell(circle(7, 18, 2.25)), shell(circle(17, 18, 2.25))],
        [shell(poly([(2.5, 18), (2.5, 12.5), (5.5, 8.5), (16, 8.5), (19.5, 12), (21.5, 12.5), (21.5, 18)], closed=True, r=S.r)),
         detail(plus(11.5, 13.25, 2)),
         mark(rect(8, 4, 7, 2.5, L(S, 0, 1.25)))],
    ]


@icon("pit-latrine", CAT, "Small outhouse hut with a slanted roof, a door and a vent pipe",
      tags=["outhouse", "latrine", "sanitation", "toilet", "privy", "wash"], aliases=["outhouse"])
def _(S):
    return [
        shell(poly([(4, 21.5), (4, 9.5), (18, 6.5), (18, 21.5)], closed=True, r=S.r * 0.5)),
        line(seg(2.5, 9.5, 20, 5.75) if S.name == "line" else seg(2.5, 9.5, 20, 5.75)),
        detail(poly([(8, 21.5), (8, 13), (14, 13), (14, 21.5)], r=S.r * 0.4)),
        line(seg(15, 6, 15, 2.5)),
    ]


# ============================================================================ digital health

def phone(S):
    return shell(rect(5.5, 2.5, 13, 19, min(S.R, 3)))


def laptop(S):
    return [shell(rect(4, 4, 16, 11.5, min(S.R, 3))), line(seg(3, 19, 21, 19) if S.name == "rounded" else seg(2, 19, 22, 19))]


def rx(S, x, y, s=1.0):
    """Rx symbol with its top-left at (x, y); s = 1 is about 6.5 x 9 px."""
    d = (f"M{fmt(x)} {fmt(y + 9 * s)}V{fmt(y)}H{fmt(x + 2.75 * s)}A{fmt(2.25 * s)} {fmt(2.25 * s)} 0 0 1 {fmt(x + 2.75 * s)} "
         f"{fmt(y + 4.5 * s)}H{fmt(x)}")
    return [detail(d), detail(seg(x + 2 * s, y + 4.5 * s, x + 6.5 * s, y + 9 * s)),
            detail(seg(x + 6.5 * s, y + 5.5 * s, x + 3 * s, y + 9 * s))]


@icon("video-consultation", CAT, "Laptop screen showing a clinician on a video call with a medical cross",
      tags=["telehealth", "telemedicine", "virtual visit", "online doctor", "video call", "remote consultation"],
      aliases=["telehealth"])
def _(S):
    return [
        *laptop(S),
        detail(circle(12, 7.75, 1.75)),
        detail(plus(16.75, 7.25, 1.25)),
        detail(L(S, "M7.5 15.5V13.5A2 2 0 0 1 9.5 11.5H14.5A2 2 0 0 1 16.5 13.5V15.5", "M7.5 15.5V14A2.5 2.5 0 0 1 10 11.5H14A2.5 2.5 0 0 1 16.5 14V15.5")),
    ]


@icon("doctor-chat", CAT, "Speech bubble with a stethoscope inside it",
      tags=["ask a doctor", "medical chat", "telehealth", "consultation", "message doctor", "online doctor"],
      aliases=["ask-a-doctor"])
def _(S):
    bubble = L(S, "M2.5 3H21.5V17H10L5.5 21V17H2.5Z",
               "M6 3H18A3.5 3.5 0 0 1 21.5 6.5V13.5A3.5 3.5 0 0 1 18 17H10L5.5 21V17A3 3 0 0 1 2.5 14V6.5A3.5 3.5 0 0 1 6 3Z")
    return [
        shell(bubble),
        detail("M7 6.5V8.75A2.5 2.5 0 0 0 12 8.75V6.5"),
        detail(L(S, "M9.5 11.25V13.5H16V11.75", "M9.5 11.25V12A1.5 1.5 0 0 0 11 13.5H14.5A1.5 1.5 0 0 0 16 12V11.75")),
        dot(16, 9.25, 1.5),
    ]


@icon("e-prescription", CAT, "Smartphone whose screen shows a large Rx symbol",
      tags=["electronic prescription", "eprescribing", "digital prescription", "rx", "pharmacy app", "online prescription"],
      aliases=["digital-prescription"])
def _(S):
    return [phone(S), *rx(S, 8.75, 6.5, 1.0), detail(seg(10.5, 18.5, 13.5, 18.5))]


@layered("remote-patient-monitoring", "House sending a heartbeat signal to a monitor",
         tags=["rpm", "remote monitoring", "telemonitoring", "home monitoring", "telehealth", "connected care"],
         aliases=["telemonitoring"])
def _(S):
    return [
        [shell(_house(S, 2.5, 11.5, 15.5, 11, 21.5))],
        [shell(rect(12.5, 2.5, 9, 7.5, min(S.R, 2))), detail(pulse(14, 7.25, 20, 2.75, simple=True)),
         line(arc(7, 16.5, 5, -80, -10)), line(arc(7, 16.5, 8.5, -80, -10))],
    ]


@icon("health-app", CAT, "Smartphone whose screen shows a heart above a heartbeat line",
      tags=["health tracker", "fitness app", "wellness app", "mobile health", "mhealth", "heart rate"],
      aliases=["mobile-health"])
def _(S):
    return [phone(S), mark(heart(S, 12, 8.25, 0.42)), detail(pulse(8, 16, 16, 2.5, simple=True))]


@icon("symptom-checker", CAT, "Smartphone whose screen shows a person with a question mark beside it",
      tags=["symptom check", "triage", "self assessment", "diagnosis app", "health check", "online triage"],
      aliases=["symptom-check"])
def _(S):
    return [
        phone(S),
        dot(9.75, 8.5, 1.75),
        detail(L(S, "M7.5 17V14.5A1.5 1.5 0 0 1 9 13H10.5A1.5 1.5 0 0 1 12 14.5V17", "M7.5 17V15.25A2.25 2.25 0 0 1 12 15.25V17")),
        detail(L(S, "M14 7.5A1.75 1.75 0 1 1 15.75 9.25V11", "M14 7.5A1.75 1.75 0 1 1 15.75 9.25V11")),
        dot(15.75, 14.5, 1),
    ]


@icon("online-pharmacy", CAT, "Laptop whose screen shows a pill bottle",
      tags=["internet pharmacy", "order medicine", "e-pharmacy", "online drugstore", "chemist", "mail order pharmacy"],
      aliases=["e-pharmacy"])
def _(S):
    return [
        *laptop(S),
        mark(rect(9, 6.5, 6, 2, L(S, 0, 0.75))),
        detail(rect(9.75, 10, 4.5, 4, L(S, 0, 1))),
    ]


@icon("prescription-delivery", CAT, "Parcel box marked Rx with speed lines trailing behind it",
      tags=["medicine delivery", "pharmacy delivery", "mail order", "home delivery", "rx delivery", "courier"],
      aliases=["medicine-delivery"])
def _(S):
    return [
        shell(rect(8, 4.5, 13.5, 15, min(S.R, 2.5))),
        *rx(S, 11.75, 8, 0.8),
        line(seg(2.5, 8.5, 5.5, 8.5)), line(seg(3.5, 12, 5.5, 12)), line(seg(2.5, 15.5, 5.5, 15.5)),
    ]


_HANDSET = "M5.5 3H9L10.5 7.5L8.3 9C9.3 11.5 12.5 14.7 15 15.7L16.5 13.5L21 15V18.5C21 20 20 21 18.5 21C10.5 20.5 3.5 13.5 3 5.5C3 4 4 3 5.5 3Z"
_HANDSET_L = "M3 3H9L10.5 7.5L8.3 9C9.3 11.5 12.5 14.7 15 15.7L16.5 13.5L21 15V21C10.5 20.5 3.5 13.5 3 3Z"


@icon("medical-hotline", CAT, "Telephone handset with a speech bubble holding a medical cross",
      tags=["nurse line", "health helpline", "medical advice line", "call doctor", "helpline", "phone triage"],
      aliases=["nurse-hotline"])
def _(S):
    bubble = L(S, "M12 2.5H21.5V11H16L12 13.5Z",
               "M13.5 2.5H20A1.5 1.5 0 0 1 21.5 4V9.5A1.5 1.5 0 0 1 20 11H16L12 13.5V4A1.5 1.5 0 0 1 13.5 2.5Z")
    return [
        shell(move(L(S, _HANDSET_L, _HANDSET), 0, 0, 0.72, 2.5, 21.5)),
        shell(bubble),
        detail(plus(16.75, 6.75, 1.75)),
    ]


@icon("ai-diagnosis", CAT, "Magnifying glass over a heartbeat trace with sparkles around the lens",
      tags=["artificial intelligence", "ai", "machine learning", "diagnostics", "smart diagnosis", "medical ai"],
      aliases=["ai-diagnostics"])
def _(S):
    return [
        shell(circle(10, 11, 7)),
        detail(pulse(5, 11.5, 15, 3.5)),
        line(seg(15, 16, 20.5, 21.5)),
        solid(sparkle(19.5, 4.5, 2.75)),
        solid(sparkle(4, 3.5, 1.75)),
    ]


@icon("wearable-ecg-patch", CAT, "Chest outline with an adhesive patch showing a heartbeat line",
      tags=["ecg patch", "ekg patch", "cardiac monitor", "wearable", "heart monitor", "biosensor"],
      aliases=["ekg-patch"])
def _(S):
    torso = L(S, "M2.5 21.5V10.5C2.5 8 4 6.5 7 6L9 5.5C10 7.5 14 7.5 15 5.5L17 6C20 6.5 21.5 8 21.5 10.5V21.5",
              "M2.5 21.5V10.5C2.5 8 4 6.5 7 6L9 5.5C10 7.5 14 7.5 15 5.5L17 6C20 6.5 21.5 8 21.5 10.5V21.5")
    patch = minus(rect(12, 11, 7.5, 5.5, L(S, 0.5, 2)), path_to_d(ST(pulse(13, 13.75, 18.5, 2.5), 1.25)))
    return [line(torso), solid(patch)]


@icon("care-robot", CAT, "Rounded robot wearing a nurse cap with a cross",
      tags=["robot nurse", "healthcare robot", "assistive robot", "elder care", "automation", "care assistant"],
      aliases=["robot-nurse"])
def _(S):
    cap = minus(_nurse_cap(12, 4.25, 8), path_to_d(ST(plus(12, 4.25, 1.2), 1.2)))
    return [
        solid(cap),
        shell(rect(5, 7.5, 14, 8, L(S, 2, 4))),
        dot(9.5, 11.5, 1.25), dot(14.5, 11.5, 1.25),
        shell(rect(7.5, 17.5, 9, 4, L(S, 1, 2))),
        line(seg(2.5, 12.5, 5, 12.5)), line(seg(19, 12.5, 21.5, 12.5)),
    ]


# ============================================================================ procedures, tests and therapies (batch 2)

def dashes(x0, y0, x1, y1, n, fill=0.5, S=None):
    """n evenly spaced dashes along a straight line; fill is the share of each step that is drawn.
    With a Rounded S the dashes are shortened so the round caps keep the same visible length."""
    out = ""
    ln = math.hypot(x1 - x0, y1 - y0)
    cut = 1.0 / ln if S is not None and S.name == "rounded" else 0.0
    for i in range(n):
        t0 = (i + (1 - fill) / 2) / n + cut
        t1 = (i + (1 + fill) / 2) / n - cut
        if t1 < t0:
            t0 = t1 = (t0 + t1) / 2
        out += seg(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0, x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)
    return out


def syringe(S, tip, deg, needle=3.5, barrel=6.0, h=2.25):
    """Syringe whose needle tip sits at `tip`, pointing along `deg` (the body runs the opposite way)."""
    m = axis(tip, deg + 180)
    b0, b1 = needle, needle + barrel
    return [line(mseg(m, 0, 0, b0, 0)),
            shell(stadium(m, b0, b1, h, L(S, 0.5, 1.5))),
            line(mseg(m, b1, 0, b1 + 2, 0)), line(mseg(m, b1 + 2, -h, b1 + 2, h))]


@icon("plastic-surgery", CAT, "Face in side profile with dashed surgical marking lines on the nose and cheek",
      tags=["cosmetic surgery", "aesthetic surgery", "rhinoplasty", "facelift", "reconstructive surgery", "surgeon"],
      aliases=["cosmetic-surgery"])
def _(S):
    face = L(S, "M6.5 21.5V17.5C4 16 2.5 13.5 2.5 10.5C2.5 6 6 2.5 10.5 2.5C14 2.5 16.5 4.5 17 7.5L21 13L18.5 13.5V15.5"
                "C18.5 16.6 17.6 17.5 16.5 17.5H14V21.5",
             "M6.5 21.5V17.5C4 16 2.5 13.5 2.5 10.5C2.5 6 6 2.5 10.5 2.5C14 2.5 16.5 4.5 17 7.5L20.4 12.2"
                "Q21 13 20 13.2L18.5 13.5V15.5C18.5 16.6 17.6 17.5 16.5 17.5H14V21.5")
    return [
        line(face),
        detail(dashes(13.75, 7, 17.75, 13.5, 2, 0.5, S)),
        detail(dashes(5, 12.5, 14.5, 12.5, 2, 0.55, S)),
    ]


@layered("gastric-band", "Stomach with an adjustable band around its upper part and a thin tube leading off",
         tags=["lap band", "bariatric surgery", "weight loss surgery", "gastric banding", "obesity", "stomach"],
         aliases=["lap-band"])
def _(S):
    stomach = ("M8.5 2.5V9C8.5 10.3 7.8 11.2 6.8 12C5 13.5 4.5 15.5 5 17.3L3 19.3L4.7 21L6.6 19.1C8 20.6 10.2 21.5 12.8 21.5"
               "C17.6 21.5 21.5 17.8 21.5 13C21.5 9.6 19.5 7.5 16.8 7.5C15.2 7.5 14 8.2 13 9C12.2 9.6 11.5 9.2 11.5 8.3V2.5Z")
    return [
        [shell(rect(6.75, 8, 7, 2, min(S.R, 1))),
         line(poly([(6.75, 9), (3.5, 9), (3.5, 7)], r=S.r * 0.5)), shell(circle(3.5, 4.5, 1.75))],
        [shell(stomach, stroke_miterlimit="2")],
    ]


@layered("epidural", "Person seen from behind with the spine marked and a syringe needle entering the lower back",
         tags=["epidural anesthesia", "epidural anaesthesia", "spinal block", "labor pain relief", "anesthesia", "spine"],
         aliases=["epidural-block"])
def _(S):
    torso = L(S, "M3 21.5V12.5C3 10 4.5 8.5 7 8.5H12C14.5 8.5 16 10 16 12.5V21.5Z",
              "M3 20V12.5C3 10 4.5 8.5 7 8.5H12C14.5 8.5 16 10 16 12.5V20Q16 21.5 14.5 21.5H4.5Q3 21.5 3 20Z")
    return [
        syringe(S, (10.5, 18), 165, 3, 5.5, 2.25),
        [shell(circle(9.5, 4.25, 2.25)), shell(torso), detail(dashes(9.5, 10.5, 9.5, 21, 4, 0.5, S))],
    ]


@icon("cardiac-stress-test", CAT, "Person walking on a treadmill beside a screen showing a heartbeat trace",
      tags=["stress test", "exercise ecg", "treadmill test", "exercise stress test", "cardiology", "heart test"],
      aliases=["exercise-stress-test"])
def _(S):
    return [
        dot(7.5, 4.25, 2),
        line(seg(7.5, 7.75, 7, 12.5)),
        line(poly([(4, 16.5), (7, 12.5), (10, 16.5)], r=S.r * 0.5)),
        line(poly([(4.5, 11), (7.5, 8.5), (11, 10)], r=S.r * 0.5)),
        shell(rect(2.5, 18.5, 16, 3, L(S, 0.5, 1.5))),
        line(seg(17, 18.5, 17, 9.5)),
        shell(rect(13, 2.5, 8.5, 7, min(S.R, 2))),
        detail(pulse(14.5, 7, 20, 2.75, simple=True)),
    ]


@icon("sleep-study", CAT, "Person asleep in bed with a wire from the head to a monitor showing a wave",
      tags=["polysomnography", "sleep test", "sleep apnea", "sleep apnoea", "sleep lab", "sleep clinic"],
      aliases=["polysomnography"])
def _(S):
    return [
        line(seg(2.5, 9, 2.5, 21.5)),
        line(poly([(2.5, 18), (21.5, 18), (21.5, 21.5)], r=S.r)),
        dot(6, 14.25, 1.75),
        line(seg(9.5, 14.5, 18.5, 14.5)),
        line(poly([(6, 12.5), (6, 5.75), (11, 5.75)], r=S.r)),
        shell(rect(11, 2.5, 10.5, 7, min(S.R, 2))),
        detail(L(S, "M13 6.5L14.5 4.75L16.25 7.75L18 4.75L19.5 6.5", "M13 6C14 4.25 15 4.25 16.25 6C17.5 7.75 18.5 7.75 19.5 6")),
    ]


@layered("cast-saw", "Handheld cast saw with a round blade cutting into a plaster cast",
         tags=["cast removal", "oscillating saw", "plaster cast", "orthopedics", "orthopaedics", "fracture clinic"],
         aliases=["cast-cutter"])
def _(S):
    m = axis((8.5, 12.5), -40)
    return [
        [shell(circle(8.5, 12.5, 3.5)), dot(8.5, 12.5, 1)],
        [shell(stadium(m, 3, 14.5, 2.5, L(S, 1, 2.5))), detail(mseg(m, 9, -2.5, 9, 2.5))],
        [shell(rect(2.5, 15.5, 19, 6, L(S, 1.5, 3))), detail(seg(17, 15.5, 17, 21.5))],
    ]


@layered("auscultation", "Patient seen from behind with a stethoscope chest piece pressed to the back",
         tags=["listening to lungs", "stethoscope", "chest exam", "physical exam", "check up", "breathing"],
         aliases=["stethoscope-exam"])
def _(S):
    return [
        [shell(circle(9, 14.5, 2)),
         line(L(S, "M11 14.5H17.5V6.5", "M11 14.5H15.5A2 2 0 0 0 17.5 12.5V6.5")),
         line(L(S, "M15 2.5V4.5L17.5 6.5L20 4.5V2.5", "M15 2.5V4A2.5 2.5 0 0 0 20 4V2.5"))],
        [shell(circle(9, 5.5, 3)),
         shell(L(S, "M2.5 21.5V14.5C2.5 12 4 10.5 6.5 10.5H11.5C14 10.5 15.5 12 15.5 14.5V21.5Z",
                 "M2.5 20V14.5C2.5 12 4 10.5 6.5 10.5H11.5C14 10.5 15.5 12 15.5 14.5V20Q15.5 21.5 14 21.5H4Q2.5 21.5 2.5 20Z"))],
    ]


@icon("physical-therapy", CAT, "Patient lying on a table with a raised bent leg supported by a therapist's hand",
      tags=["physiotherapy", "physio", "rehabilitation", "rehab", "physical therapist", "mobility"],
      aliases=["physiotherapy"])
def _(S):
    return [
        line(seg(2.5, 18, 21.5, 18)), line(seg(4.5, 18, 4.5, 21.5)), line(seg(19.5, 18, 19.5, 21.5)),
        dot(4.5, 13.75, 1.75),
        line(poly([(7.5, 14), (13, 14), (16, 8.5), (20.5, 13)], r=S.r * 0.5)),
        line(poly([(20.5, 2.5), (18, 7), (19.5, 8.5)], r=S.r * 0.5)),
    ]


@icon("occupational-therapy", CAT, "Pegboard with pegs standing in it and one peg being placed in the empty hole",
      tags=["ot", "fine motor skills", "pegboard", "hand therapy", "dexterity", "rehabilitation"],
      aliases=["ot-therapy"])
def _(S):
    peg = lambda x, y: rect(x - 1.5, y, 3, 4.5, L(S, 0, 1.5))  # noqa: E731
    return [
        shell(rect(2.5, 16.5, 19, 5, min(S.R, 1.5))),
        shell(peg(5.5, 10)), shell(peg(18.5, 10)),
        shell(rect(10.5, 2.5, 3, 3.5, L(S, 0, 1.5))),
        line(poly([(10.25, 10.25), (12, 12), (13.75, 10.25)], r=S.r * 0.5)),
    ]


@layered("orthodontic-headgear", "Head in profile with a wire facebow at the mouth and a strap around the back",
         tags=["headgear", "braces", "orthodontics", "orthodontist", "facebow", "teeth alignment"],
         aliases=["braces-headgear"])
def _(S):
    return [
        [line(L(S, "M16.5 14.5H21.5V17.5H9", "M16.5 14.5H20A1.5 1.5 0 0 1 21.5 16A1.5 1.5 0 0 1 20 17.5H9"))],
        [shell(L(S, "M6.5 21.5V17.5C4 16 2.5 13.5 2.5 10.5C2.5 6 6 2.5 10.5 2.5C14 2.5 16.5 4.5 17 7.5L19 11.5L17 12V14.5"
                    "C17 15.6 16.1 16.5 15 16.5H13V21.5Z",
                 "M6.5 21.5V17.5C4 16 2.5 13.5 2.5 10.5C2.5 6 6 2.5 10.5 2.5C14 2.5 16.5 4.5 17 7.5L18.6 10.7"
                    "Q19 11.5 18.2 11.7L17 12V14.5C17 15.6 16.1 16.5 15 16.5H13V21.5Z")),
         detail("M13 14.5C10.5 13.5 6.5 13.5 4.5 15.5")],
    ]


@icon("palatal-expander", CAT, "Upper dental arch seen from below with a screw expander bridging the back teeth",
      tags=["orthodontics", "rapid palatal expander", "maxillary expander", "braces", "orthodontist", "palate"],
      aliases=["palate-expander"])
def _(S):
    teeth = [(4.25, 20.25), (4.25, 15.25), (5, 10.25), (8, 5.75), (12, 4), (16, 5.75), (19, 10.25), (19.75, 15.25),
             (19.75, 20.25)]
    parts = [dot(x, y, 1.6) for x, y in teeth]
    return parts + [
        line(seg(6.75, 17.75, 9.5, 17.75)), line(seg(14.5, 17.75, 17.25, 17.75)),
        shell(rect(9.5, 15.25, 5, 5, L(S, 0.5, 1.5))),
        detail(seg(12, 16.5, 12, 19)),
    ]


@layered("eye-shield", "Perforated oval eye shield held on with two strips of tape",
         tags=["eye patch", "eye guard", "eye surgery", "cataract surgery", "eye protection", "ophthalmology"],
         aliases=["eye-guard"])
def _(S):
    holes = [dot(x, y, 1) for y in (10.25, 13.75) for x in (8.75, 12, 15.25)]
    return [
        [shell(stadium(axis((6, 6.5), 45), -3, 3, 1.5, L(S, 0, 1.5))),
         shell(stadium(axis((18, 17.5), 45), -3, 3, 1.5, L(S, 0, 1.5)))],
        [shell(ellipse(12, 12, 8.5, 6.5) if S.name == "rounded" else
               "M3.5 12C3.5 8 7 5.5 12 5.5C17 5.5 20.5 8 20.5 12C20.5 16 17 18.5 12 18.5C7 18.5 3.5 16 3.5 12Z"),
         *holes],
    ]


@layered("pharmacy-drive-through", "Pharmacy service window handing a pill bottle down to a car",
         tags=["drive thru pharmacy", "pharmacy window", "prescription pickup", "curbside pharmacy", "drugstore", "chemist"],
         aliases=["drive-thru-pharmacy"])
def _(S):
    return [
        [shell(circle(9, 19.5, 2)), shell(circle(18, 19.5, 2))],
        [shell(poly([(6.5, 19.5), (6.5, 15), (9, 11.5), (16.5, 11.5), (19, 15), (21.5, 15.5), (21.5, 19.5)], closed=True, r=S.r))],
        [line(poly([(2.5, 21.5), (2.5, 2.5), (13.5, 2.5)], r=S.r)),
         shell(rect(5.5, 4.5, 5, 1.5, L(S, 0, 0.75))), shell(rect(6, 6, 4, 3.5, L(S, 0, 1)))],
    ]


# ============================================================================ remaining procedures (batch 3)

_INCISOR = ("M6.5 6C6.5 3.8 8 3 9.8 3.4C11 3.7 13 3.7 14.2 3.4C16 3 17.5 3.8 17.5 6C17.5 9 16.5 11.5 16 14.5L15.3 20"
            "C15.1 21.6 13.3 21.6 13 20L12 15.5L11 20C10.7 21.6 8.9 21.6 8.7 20L8 14.5C7.5 11.5 6.5 9 6.5 6Z")
_INCISOR_L = ("M6.5 6C6.5 3.8 8 3 9.8 3.4C11 3.7 13 3.7 14.2 3.4C16 3 17.5 3.8 17.5 6C17.5 9 16.5 11.5 16 14.5L15.2 21.5H13.2"
              "L12 15.5L10.8 21.5H8.8L8 14.5C7.5 11.5 6.5 9 6.5 6Z")


def incisor(S, dx=0.0, dy=0.0, s=1.0, ox=12.0, oy=12.0):
    return move(L(S, _INCISOR_L, _INCISOR), dx, dy, s, ox, oy)


@icon("teeth-whitening", CAT, "Front tooth with sparkles shining from its upper corner",
      tags=["tooth whitening", "bleaching", "cosmetic dentistry", "dentist", "bright smile", "shiny teeth"],
      aliases=["tooth-whitening"])
def _(S):
    return [
        shell(incisor(S, -3.5, 1, 0.9, 12, 12)),
        solid(sparkle(18.5, 6, 3.6)),
        solid(sparkle(19.5, 14.5, 2)),
    ]
