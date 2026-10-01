"""TypeIcon Core: anatomy (batch anatomy_001).

Organs, glands, bones, teeth, body systems, blood and reproductive cells, microbes and muscle groups,
drawn as simple clinical symbols from the anatomy itself.
"""
import math

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar  # noqa: F401

CAT = "anatomy"


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


def mirror(d, cx=12.0):
    return xf(d, (-1, 0, 0, 1, 2 * cx, 0))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def solid_of(d, w=2.0):
    """Filled silhouette of a closed Line outline (fill + outer half of the stroke)."""
    return U(P(d), ST(d, w, "butt", "miter"))


# ============================================================================ digestive organs

@icon("pancreas", CAT, "The pancreas: a long tapering gland with a wide head and a thin tail",
      tags=["pancreatic", "gland", "insulin", "diabetes", "digestion", "organ"])
def _(S):
    d = L(S,
          "M3 13C3 10.5 5 9.2 7.5 9.5C10 9.8 12 9.5 14.5 8.3C17 7 19 5.5 21 5.5L20.5 8.5C19.5 10.5 17 12.5 14 14"
          "C12.5 14.8 11.5 15.5 11 17C10.3 19 8.8 19.5 7 19.5C4.5 19.5 3 16.5 3 13Z",
          "M3 13C3 10.5 5 9.2 7.5 9.5C10 9.8 12 9.5 14.5 8.3C17 7 18.5 5.8 19.8 5.6C21.2 5.4 21.3 7 20.5 8.5"
          "C19.5 10.5 17 12.5 14 14C12.5 14.8 11.5 15.5 11 17C10.3 19 8.8 19.5 7 19.5C4.5 19.5 3 16.5 3 13Z")
    return [shell(d, stroke_miterlimit="2"), detail("M6 15C8.5 14 10.5 12.8 13 11.8")]


@icon("gallbladder", CAT, "The gallbladder: a pear-shaped sac on a duct, holding two gallstones",
      tags=["gallstones", "bile", "biliary", "organ", "digestion", "liver"], aliases=["gall-bladder"])
def _(S):
    sac = L(S, "M12.5 6H16C16.5 8.5 17.5 11 17.5 15C17.5 18.5 15.3 21 12.5 21C9.5 21 7 18.8 7 15.5C7 11 11 9 12.5 6Z",
            "M13.5 6H15C15.8 6 16 6.5 16.2 7.2C16.8 9.5 17.5 11.8 17.5 15C17.5 18.5 15.3 21 12.5 21C9.5 21 7 18.8 7 15.5"
            "C7 11.5 10.3 9.3 12.3 6.8C12.7 6.3 13 6 13.5 6Z")
    return [shell(sac, stroke_miterlimit="2"), line(poly([(14.3, 6), (14.3, 3), (5, 3)], r=S.r)),
            dot(11, 16.2, 1.5), dot(14.2, 13.8, 1.3)]


@icon("esophagus", CAT, "The esophagus: a long food tube running down into the top of the stomach",
      tags=["oesophagus", "gullet", "food pipe", "swallowing", "digestion", "heartburn"], aliases=["oesophagus", "gullet"])
def _(S):
    tube = L(S, rect(6.5, 2.5, 4, 11), rect(6.5, 2.5, 4, 11, 1.5))
    stomach = ("M6.5 11.5H10.5C11 12.5 12 13 13.2 12.8C15 12.5 16 11 17.5 11C19.8 11 21 13 21 15C21 18.8 18 21.5 14 21.5"
               "C11 21.5 8.5 20.5 7 18.5C6 17 6.5 14 6.5 11.5Z")
    return [shell(union(tube, stomach), stroke_miterlimit="2"), detail("M10 18C13 18.8 16.5 17.8 18 15")]


# ============================================================================ airway

@icon("trachea", CAT, "The trachea: a ringed windpipe dividing into two bronchi",
      tags=["windpipe", "airway", "bronchi", "breathing", "respiratory", "throat"], aliases=["windpipe"])
def _(S):
    d = poly([(9.5, 2.5), (14.5, 2.5), (14.5, 13), (20.5, 19), (18, 21.5), (12, 15.5), (6, 21.5), (3.5, 19), (9.5, 13)],
             closed=True, r=S.r * 0.7)
    return [shell(d, stroke_miterlimit="2"), detail(seg(9.5, 6.5, 14.5, 6.5)), detail(seg(9.5, 10.5, 14.5, 10.5))]


@icon("larynx", CAT, "The larynx: a shield of cartilage with a top notch sitting on the windpipe",
      tags=["voice box", "adam's apple", "throat", "cartilage", "voice", "airway"], aliases=["voice-box"])
def _(S):
    shield = poly([(4.5, 3.5), (10, 3.5), (12, 6.5), (14, 3.5), (19.5, 3.5), (18.5, 10), (12, 14.5), (5.5, 10)],
                  closed=True, r=S.r)
    tube = rect(9, 12, 6, 9.5, L(S, 0, 1.5))
    return [shell(union(shield, tube), stroke_miterlimit="2"), detail(seg(9, 17, 15, 17)), detail(seg(12, 9.5, 12, 11))]


@icon("vocal-cords", CAT, "Vocal cords seen from above: two folds in a V inside the throat opening",
      tags=["vocal folds", "voice", "larynx", "speech", "singing", "throat"], aliases=["vocal-folds"])
def _(S):
    return [shell(ellipse(12, 12, 8, 9.5)), detail(poly([(8.3, 19), (12, 5.5), (15.7, 19)], r=L(S, 0, 2.5)))]


@icon("diaphragm", CAT, "The diaphragm: a dome of muscle under the lungs that moves as you breathe",
      tags=["breathing", "respiration", "muscle", "lungs", "hiccups", "breath"])
def _(S):
    lung = L(S, "M10.5 3C7.5 3 3.5 7.5 3.5 12C3.5 13.2 4.3 13.6 5.5 13.3L9.8 12.3C10.3 12.2 10.5 11.8 10.5 11.3Z",
             "M9.5 3C6.5 3.3 3.5 7.5 3.5 12C3.5 13.2 4.3 13.6 5.5 13.3L9.6 12.3C10.2 12.2 10.5 11.8 10.5 11.2V4C10.5 3.4 10.1 3 9.5 3Z")
    return [shell(lung, stroke_miterlimit="2"), shell(mirror(lung), stroke_miterlimit="2"),
            line("M2.5 20.5C5 15.5 9 15.5 12 17.5C15 15.5 19 15.5 21.5 20.5")]


@icon("bronchial-tree", CAT, "The bronchial tree: a windpipe branching again and again into smaller airways",
      tags=["bronchi", "bronchioles", "airways", "lungs", "respiratory", "asthma"], aliases=["bronchi"])
def _(S):
    r = S.r * 0.6
    return [
        line(seg(12, 2.5, 12, 9)),
        line(poly([(12, 9), (7, 12.5), (3.5, 18)], r=r)), line(poly([(12, 9), (17, 12.5), (20.5, 18)], r=r)),
        line(poly([(7, 12.5), (8.5, 17), (7.5, 21)], r=r)), line(poly([(17, 12.5), (15.5, 17), (16.5, 21)], r=r)),
        line(seg(3.5, 18, 3.5, 21.5)), line(seg(20.5, 18, 20.5, 21.5)),
        line(seg(8.5, 17, 11.5, 20)), line(seg(15.5, 17, 12.5, 20)),
    ]


@icon("alveoli", CAT, "Alveoli: a cluster of tiny round air sacs at the end of a small airway",
      tags=["air sacs", "lungs", "gas exchange", "respiratory", "oxygen", "bronchiole"])
def _(S):
    blobs = union(circle(11, 11, 3.5), circle(17, 10.5, 3.5), circle(9, 17, 3.5), circle(15, 16.5, 3.5), circle(19.5, 15.5, 2.5))
    return [shell(blobs), line(seg(3, 3, 8.6, 8.6))]


@icon("heart-cross-section", CAT, "The heart cut open to show its four chambers and valves",
      tags=["heart chambers", "cardiac", "atrium", "ventricle", "cardiology", "anatomy"], aliases=["heart-chambers"])
def _(S):
    d = ("M5.5 8.5C7.5 6.8 10 6.8 12 8C14 6.8 16.5 6.8 18.5 8.5C21 10.8 20.8 15 18 18C16 20 13.5 21.5 12 21.5"
         "C10.5 21.5 8 20 6 18C3.2 15 3 10.8 5.5 8.5Z")
    return [shell(d), detail(seg(12, 8, 12, 21.5)), detail(L(S, "M4 13H20", "M4 13.2C9 12.2 15 12.2 20 13.2")),
            line(seg(9, 7.3, 9, 2.5)), line(poly([(14.5, 7.2), (14.5, 3), (19, 3), (19, 6)], r=S.r))]


# ============================================================================ glands

@icon("thymus", CAT, "The thymus: a two-lobed gland sitting just above the heart",
      tags=["thymus gland", "immune", "t cells", "gland", "chest", "lymphatic"])
def _(S):
    lobe = L(S, "M10 2.5C6.5 3.5 4 7.5 4 11C4 13.5 6 14.5 10 13.5Z",
             "M8.8 2.9C6 4.3 4 7.9 4 11C4 13.4 5.8 14.4 8.9 13.8Q10 13.6 10 12.5V3.6Q10 2.4 8.8 2.9Z")
    heart = L(S, "M12 21.5L8.3 18A2.4 2.4 0 0 1 11.3 15.7L12 16.4L12.7 15.7A2.4 2.4 0 0 1 15.7 18Z",
              "M11.3 20.8L8.3 18A2.4 2.4 0 0 1 11.3 15.7L12 16.4L12.7 15.7A2.4 2.4 0 0 1 15.7 18L12.7 20.8Q12 21.5 11.3 20.8Z")
    return [shell(lobe), shell(mirror(lobe)), shell(heart, stroke_miterlimit="2")]


@icon("bone-marrow", CAT, "A long bone cut open lengthwise to show the spongy marrow inside",
      tags=["marrow", "bone", "stem cells", "blood cells", "transplant", "hematology"])
def _(S):
    body = union(circle(5, 8, 3), circle(5, 16, 3), circle(19, 8, 3), circle(19, 16, 3), rect(5, 8.5, 14, 7))
    return [shell(body), dot(9, 12, 1.25), dot(12, 12, 1.25), dot(15, 12, 1.25)]


@icon("adrenal-glands", CAT, "A pair of kidneys, each topped by a small adrenal gland",
      tags=["adrenal", "suprarenal", "adrenaline", "cortisol", "hormones", "endocrine"], aliases=["adrenal-gland"])
def _(S):
    k = ("M6.5 9.5C4 9.5 2.5 12 2.5 15C2.5 18.5 4.5 21 7 21C8.5 21 9.3 20 9 18.8C8.8 17.8 8.2 17.2 8.2 15.8"
         "C8.2 14.5 9.2 13.8 9.5 12.6C9.9 11 8.8 9.5 6.5 9.5Z")
    cap = poly([(3.5, 7.5), (6.5, 3), (9.5, 7.5)], closed=True, r=L(S, 0, 1))
    return [shell(k), shell(mirror(k)), solid(cap), solid(mirror(cap))]


@icon("pituitary-gland", CAT, "The brain in side view with the small pituitary gland hanging below it",
      tags=["pituitary", "hypophysis", "hormones", "endocrine", "gland", "brain"], aliases=["pituitary"])
def _(S):
    return _brain(S) + [line(seg(11, 15, 11, 17)), solid(circle(11, 19.3, 2.3))]


@icon("prostate", CAT, "The prostate gland wrapped around the tube leading out of the bladder",
      tags=["prostate gland", "urology", "men's health", "bladder", "gland", "urethra"])
def _(S):
    bl = L(S, "M12 11C8 11 5 9 5 6C5 4 6.5 2.5 8.5 2.8C10 3 11 3.5 12 3.5C13 3.5 14 3 15.5 2.8C17.5 2.5 19 4 19 6C19 9 16 11 12 11Z",
           "M12 11C8 11 5 9 5 6C5 4 6.5 2.5 8.5 2.8C10 3 11 3.5 12 3.5C13 3.5 14 3 15.5 2.8C17.5 2.5 19 4 19 6C19 9 16 11 12 11Z")
    pr = L(S, "M12 14C9 13 6.5 14.3 6.5 16.8C6.5 19 8.5 20 12 19.5C15.5 20 17.5 19 17.5 16.8C17.5 14.3 15 13 12 14Z",
           "M12 14C9 13 6.5 14.3 6.5 16.8C6.5 19 8.5 20 12 19.5C15.5 20 17.5 19 17.5 16.8C17.5 14.3 15 13 12 14Z")
    return [shell(bl), shell(pr), line(seg(12, 11, 12, 14)), detail(seg(12, 14, 12, 19.5)), line(seg(12, 19.5, 12, 22))]


# ============================================================================ senses and nerves

def _spiral(cx, cy, radii, d=2.0):
    """Spiral of alternating half circles: top halves centred at cx, bottom halves at cx + d."""
    x, y = cx - radii[0], cy
    out = f"M{fmt(x)} {fmt(y)}"
    for i, r in enumerate(radii):
        if i % 2 == 0:  # top half, left to right
            x = cx + r
        else:  # bottom half, right to left
            x = cx + d - r
        out += f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x)} {fmt(y)}"
    return out


@icon("cochlea", CAT, "The cochlea: the snail-shaped spiral of the inner ear with its hearing nerve",
      tags=["inner ear", "hearing", "spiral", "audiology", "ear", "deafness"])
def _(S):
    return [line(_spiral(12, 11, [9, 7, 5, 3])), line(poly([(3, 11), (3, 16), (6.5, 21)], r=S.r))]


@icon("eye-anatomy", CAT, "Side cross-section of the eyeball with the lens at the front and the optic nerve at the back",
      tags=["eyeball", "lens", "retina", "optic nerve", "ophthalmology", "vision"], aliases=["eye-cross-section"])
def _(S):
    ball = union(circle(12.5, 12, 8), L(S, rect(19, 10, 3, 4), rect(19, 10, 3, 4, 1)))
    return [shell(ball), detail(ellipse(7.5, 12, 1.3, 3.2)), line(arc(12.5, 12, 10.5, 150, 210))]


_BRAIN = ("M6.5 16.5C4.3 16.2 3 14.5 3 12.5C3 11 3.6 10 4.5 9.3C4.5 6.3 6.7 4.2 9.3 4.3C10.3 3.5 11.5 3 13 3.1"
          "C15.3 3.2 17 4.4 17.8 6C19.9 6.8 21 8.6 21 10.6C21 12.3 20.2 13.5 18.8 13.5H13.8C13 13.5 12.6 14 12.3 14.8"
          "C11.9 15.9 11.1 16.5 10 16.5Z")


def _brain(S, lobes=False):
    parts = [shell(_BRAIN, stroke_miterlimit=L(S, "4", "4"))]
    if lobes:
        parts += [detail("M12.8 3.2L11 9.5"), detail("M5 12.8C7.5 11.3 10.5 10.8 14 11"), detail("M17.8 6L16.5 9.5")]
    else:
        parts += [detail("M7.5 8.3C9 8.3 10.3 9.3 10.5 10.8"), detail("M13.5 6.5C13.8 8 15 9 16.8 9"), detail("M6 13C7.5 13.2 9 12.8 10 12")]
    return parts


@icon("brain-lobes", CAT, "Side view of the brain divided into its four lobes, with the cerebellum below",
      tags=["frontal lobe", "temporal lobe", "parietal", "occipital", "neurology", "brain map"])
def _(S):
    return _brain(S, lobes=True) + [shell(_cbl_shell(S))]


def _cbl_shell(S):
    return L(S, "M15 16.5H20.5C20.5 19 19.2 21 17.8 21C16.3 21 15 19 15 16.5Z",
             "M16 16.5H19.5Q20.5 16.5 20.4 17.5C20.1 19.5 19 21 17.8 21C16.5 21 15.4 19.5 15.1 17.5Q15 16.5 16 16.5Z")


@icon("cerebellum", CAT, "Side view of the brain with the small striped cerebellum at the lower back highlighted",
      tags=["hindbrain", "balance", "coordination", "neurology", "brain", "motor control"])
def _(S):
    c = L(S, "M14.5 16H20.5C20.5 19 19 21 17.5 21C16 21 14.5 19 14.5 16Z", "M15.5 16H19.5Q20.5 16 20.4 17C20.1 19.3 18.9 21 17.5 21C16.1 21 14.9 19.3 14.6 17Q14.5 16 15.5 16Z")
    striped = path_to_d(D(P(c), ST("M14 18.2H21", 1.2, "butt", "miter")))
    return _brain(S) + [solid(striped), line(seg(10.5, 16.5, 11.5, 21.5))]


@icon("brainstem", CAT, "Side view of the brain with the stalk-like brainstem below it highlighted",
      tags=["brain stem", "medulla", "pons", "neurology", "brain", "spinal cord"], aliases=["brain-stem"])
def _(S):
    stem = L(S, "M9 16H12.5L13 21.5H10.5Z", "M9.8 16H11.7Q12.5 16 12.6 16.8L13 20.5Q13 21.5 12 21.5H11.3Q10.5 21.5 10.4 20.7L9.2 16.8Q9 16 9.8 16Z")
    return _brain(S) + [solid(stem), shell(_cbl_shell(S))]


@icon("brain-hemispheres", CAT, "The brain seen from above, split down the middle into left and right halves",
      tags=["left brain", "right brain", "cerebral hemispheres", "neurology", "brain", "psychology"])
def _(S):
    half = L(S, "M10.5 2.5C6.3 2.5 3.5 6.5 3.5 12C3.5 17.5 6.3 21.5 10.5 21.5Z",
             "M9 2.6C5.6 3.3 3.5 7.2 3.5 12C3.5 16.8 5.6 20.7 9 21.4Q10.5 21.7 10.5 20.2V3.8Q10.5 2.3 9 2.6Z")
    folds = ["M3.8 9.5C5.5 9.5 7 8.5 7.5 6.5", "M10.5 11C8.5 11 7 12 6.5 14", "M4.7 16.8C6.5 17 8 18 8.3 20"]
    return [shell(half), shell(mirror(half))] + [detail(f) for f in folds] + [detail(mirror(f)) for f in folds]


@icon("synapse", CAT, "A synapse: two nerve endings meeting across a small gap with chemical messengers crossing it",
      tags=["neurotransmitter", "nerve", "neuron", "neuroscience", "signal", "brain chemistry"])
def _(S):
    bulb = L(S, "M2 10.5H4.5C5 7.5 6.5 5.5 8.5 5.5H10V18.5H8.5C6.5 18.5 5 16.5 4.5 13.5H2Z",
             "M3 10.5H4.5C5 7.5 6.5 5.5 8.5 5.5H9Q10 5.5 10 6.5V17.5Q10 18.5 9 18.5H8.5C6.5 18.5 5 16.5 4.5 13.5H3Q2 13.5 2 12.5V11.5Q2 10.5 3 10.5Z")
    cup = L(S, "M22 10.5H20.5C20 7.5 18.5 5.5 16.5 5.5H14C15 8.5 15 15.5 14 18.5H16.5C18.5 18.5 20 16.5 20.5 13.5H22Z",
            "M21 10.5H20.5C20 7.5 18.5 5.5 16.5 5.5H15.3Q14.2 5.5 14.5 6.6C15.1 10 15.1 14 14.5 17.4Q14.2 18.5 15.3 18.5H16.5C18.5 18.5 20 16.5 20.5 13.5H21Q22 13.5 22 12.5V11.5Q22 10.5 21 10.5Z")
    return [shell(bulb, stroke_miterlimit="2"), shell(cup, stroke_miterlimit="2"), dot(7, 9.5, 1.1), dot(7, 14.5, 1.1),
            dot(12, 8.5, 0.9), dot(12, 12, 0.9), dot(12, 15.5, 0.9)]


@icon("spinal-cord", CAT, "The spinal cord with pairs of nerve roots branching out on both sides",
      tags=["spinal nerves", "nerve roots", "central nervous system", "neurology", "spine", "back"])
def _(S):
    parts = [shell(rect(10, 2, 4, 20, L(S, 0.5, 2)))]
    for y in (4, 9, 14):
        parts += [line(f"M10 {y}C7.5 {y} 5.5 {y + 1.5} 4 {y + 4}"), line(f"M14 {y}C16.5 {y} 18.5 {y + 1.5} 20 {y + 4}")]
    return parts


# ============================================================================ skin and hair

@icon("skin-layers", CAT, "A block of skin in cross-section with three layers and a hair growing from a root",
      tags=["epidermis", "dermis", "dermatology", "skin", "subcutaneous", "skincare"], aliases=["skin-cross-section"])
def _(S):
    top = "M3 9.5C5 8.5 7 10.5 9 9.5S13 8.5 15 9.5S19 10.5 21 9.5"
    block = top + L(S, "V21.5H3Z", "V20Q21 21.5 19.5 21.5H4.5Q3 21.5 3 20Z")
    return [shell(block), detail("M3 13C5 12 7 14 9 13S13 12 15 13S19 14 21 13"),
            detail(L(S, "M3 17.5H5.5A2 2 0 0 1 9.5 17.5A2 2 0 0 1 13.5 17.5A2 2 0 0 1 17.5 17.5A2 2 0 0 1 21 17.5",
                     "M3 17.5H5.5A2 2 0 0 1 9.5 17.5A2 2 0 0 1 13.5 17.5A2 2 0 0 1 17.5 17.5A2 2 0 0 1 21 17.5")),
            line(poly([(12, 9), (12, 5.5), (14.5, 2.5)], r=S.r))]


@icon("hair-follicle", CAT, "A single hair growing out of its bulb-shaped follicle below the skin surface",
      tags=["hair root", "hair growth", "hair loss", "dermatology", "scalp", "follicle"])
def _(S):
    pocket = L(S, "M2 9H9V15.5C7.5 16.5 7 18 7.5 19.5C8 21 10 21.5 12 21.5C14 21.5 16 21 16.5 19.5C17 18 16.5 16.5 15 15.5V9H22",
               "M2 9H8Q9 9 9 10V15.5C7.5 16.5 7 18 7.5 19.5C8 21 10 21.5 12 21.5C14 21.5 16 21 16.5 19.5C17 18 16.5 16.5 15 15.5V10Q15 9 16 9H22")
    return [line(pocket), line("M12 17V5.5C12 4 13 3 14.5 2.5"), dot(12, 18, 1.8)]


# ============================================================================ teeth

@icon("tooth-anatomy", CAT, "A molar cut in half showing the enamel crown, the pulp inside and two roots below the gum line",
      tags=["tooth cross-section", "pulp", "enamel", "root canal", "dentistry", "dental"], aliases=["tooth-cross-section"])
def _(S):
    d = L(S, "M7 3C4.5 3 3.5 5 3.5 7.5C3.5 10.5 5 12.5 6 14.5L7.5 21.5L10.5 14.5H13.5L16.5 21.5L18 14.5C19 12.5 20.5 10.5 20.5 7.5"
             "C20.5 5 19.5 3 17 3C15 3 14 4 12 4C10 4 9 3 7 3Z",
          "M7 3C4.5 3 3.5 5 3.5 7.5C3.5 10.5 5 12.5 6 14.5L7 20.5C7.3 21.5 8.4 21.6 8.8 20.6L10.5 15.5C10.8 14.5 13.2 14.5 13.5 15.5"
             "L15.2 20.6C15.6 21.6 16.7 21.5 17 20.5L18 14.5C19 12.5 20.5 10.5 20.5 7.5C20.5 5 19.5 3 17 3C15 3 14 4 12 4C10 4 9 3 7 3Z")
    return [shell(d, stroke_miterlimit="2"), detail(L(S, "M8 18L8.5 12V8H15.5V12L16 18", "M8 18L8.5 12V10A2 2 0 0 1 10.5 8H13.5A2 2 0 0 1 15.5 10V12L16 18")),
            line(seg(1.5, 12, 4.5, 12)), line(seg(19.5, 12, 22.5, 12))]


def _gum_teeth(S):
    xs = [(2.5, 6.3), (10.1, 13.9), (17.7, 21.5)]
    teeth = []
    for a, b in xs:
        w = b - a
        r = w / 2
        teeth.append(L(S, f"M{fmt(a)} 19.5V{fmt(12 + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(b)} {fmt(12 + r)}V19.5Z",
                       f"M{fmt(a)} 18.5V{fmt(12 + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(b)} {fmt(12 + r)}V18.5Q{fmt(b)} 19.5 {fmt(b - 1)} 19.5"
                       f"H{fmt(a + 1)}Q{fmt(a)} 19.5 {fmt(a)} 18.5Z"))
    return teeth


@icon("gums", CAT, "A row of front teeth set into the bold scalloped band of the gums",
      tags=["gum", "gingiva", "gum disease", "gingivitis", "dental", "periodontal"], aliases=["gingiva"])
def _(S):
    top = "M3 14A3 3 0 0 1 9 14A3 3 0 0 1 15 14A3 3 0 0 1 21 14"
    teeth = L(S, top + "V21.5H3Z", top + "V20Q21 21.5 19.5 21.5H4.5Q3 21.5 3 20Z")
    tp = P(teeth)
    gum = I(D(U(tp, ST(teeth, 13, "round", "round")), U(tp, ST(teeth, 6, "round", "round"))), P(rect(1.5, 2, 21, 13.5)))
    return [solid(path_to_d(gum)), shell(teeth), detail(seg(9, 14, 9, 21.5)), detail(seg(15, 14, 15, 21.5))]


@icon("incisor", CAT, "A single flat front tooth with a straight biting edge and one long root",
      tags=["front tooth", "incisors", "dental", "tooth", "dentistry", "bite"])
def _(S):
    d = L(S, "M7 2.5H17L17 8C17 10 16 11.5 14.8 12.5L14.3 17C14 19.5 13 21.5 12 21.5C11 21.5 10 19.5 9.7 17L9.2 12.5"
             "C8 11.5 7 10 7 8Z",
          "M8.5 2.5H15.5Q17 2.5 17 4V8C17 10 16 11.5 14.8 12.5L14.3 17C14 19.5 13 21.5 12 21.5C11 21.5 10 19.5 9.7 17L9.2 12.5"
             "C8 11.5 7 10 7 8V4Q7 2.5 8.5 2.5Z")
    return [shell(d, stroke_miterlimit="2"), line(seg(2.5, 12.5, 6.5, 12.5)), line(seg(17.5, 12.5, 21.5, 12.5))]


@icon("canine-tooth", CAT, "A single pointed canine tooth with a sharp tip and one long tapering root",
      tags=["canine", "cuspid", "eye tooth", "fang", "dental", "tooth"], aliases=["cuspid"])
def _(S):
    d = L(S, "M12 2L17 7.5C17.3 9.8 16.2 11.5 14.8 12.5L14.3 17C14 19.5 13 21.5 12 21.5C11 21.5 10 19.5 9.7 17L9.2 12.5"
             "C7.8 11.5 6.7 9.8 7 7.5Z",
          "M11.3 2.8Q12 2 12.7 2.8L16.3 6.7Q17 7.5 17 8.5C17 10.2 16 11.6 14.8 12.5L14.3 17C14 19.5 13 21.5 12 21.5C11 21.5 10 19.5 9.7 17"
             "L9.2 12.5C8 11.6 7 10.2 7 8.5Q7 7.5 7.7 6.7Z")
    return [shell(d, stroke_miterlimit="2"), line(seg(2.5, 12.5, 6.5, 12.5)), line(seg(17.5, 12.5, 21.5, 12.5))]


_MOLAR = ("M8.5 4C7 4 6 5.2 6 7C6 8.8 6.8 10 7.3 11.2L8 16L9.5 12.3H10.5L12 16L12.7 11.2C13.2 10 14 8.8 14 7"
          "C14 5.2 13 4 11.5 4C10.8 4 10.5 4.5 10 4.5C9.5 4.5 9.2 4 8.5 4Z")


@icon("wisdom-tooth", CAT, "An impacted wisdom tooth lying tilted under the gum and pushing against the tooth next to it",
      tags=["impacted tooth", "third molar", "tooth extraction", "dental", "oral surgery", "molar"], aliases=["third-molar"])
def _(S):
    m = _MOLAR if S.name == "line" else _MOLAR.replace("L8 16L9.5 12.3H10.5L12 16L12.7", "L7.8 15.2Q8 16.3 8.5 15.3L9.5 12.8Q10 12 10.5 12.8L11.5 15.3Q12 16.3 12.2 15.2L12.7")
    up = xf(m, (1, 0, 0, 1, -3.5, -1))
    tilt = rot(xf(m, (0.85, 0, 0, 0.85, 16 - 8.5, 15 - 8.5)), -62, 16, 15)
    return [
        shell(up, stroke_miterlimit="2"), shell(tilt, stroke_miterlimit="2"), line(seg(12.5, 7.5, 22, 7.5))]


@icon("dental-arch", CAT, "A horseshoe-shaped row of teeth seen from above, as on a dental chart",
      tags=["dental chart", "teeth", "jaw", "orthodontics", "dentistry", "bite"], aliases=["tooth-chart"])
def _(S):
    band = L(S, "M3 21.5V11.5A9 9 0 0 1 21 11.5V21.5H16.5V11.5A4.5 4.5 0 0 0 7.5 11.5V21.5Z",
             "M4.5 21.5Q3 21.5 3 20V11.5A9 9 0 0 1 21 11.5V20Q21 21.5 19.5 21.5H18Q16.5 21.5 16.5 20V11.5A4.5 4.5 0 0 0 7.5 11.5V20Q7.5 21.5 6 21.5Z")
    parts = [shell(band, stroke_miterlimit="2")]
    for a in (212, 241, 270, 299, 328):
        x0, y0 = polar(12, 11.5, 4.5, a)
        x1, y1 = polar(12, 11.5, 9, a)
        parts.append(detail(seg(x0, y0, x1, y1)))
    parts += [detail(seg(3, 15, 7.5, 15)), detail(seg(16.5, 15, 21, 15)), detail(seg(3, 18.5, 7.5, 18.5)), detail(seg(16.5, 18.5, 21, 18.5))]
    return parts


# ============================================================================ body systems

_TORSO = ("M9.5 2.5V4.5C7 5 5 5.8 4 7.3C3.3 8.3 3 9.5 3 11V21.5H21V11C21 9.5 20.7 8.3 20 7.3C19 5.8 17 5 14.5 4.5V2.5Z")
_TORSO_R = ("M9.5 2.5V4.5C7 5 5 5.8 4 7.3C3.3 8.3 3 9.5 3 11V20Q3 21.5 4.5 21.5H19.5Q21 21.5 21 20V11C21 9.5 20.7 8.3 20 7.3"
            "C19 5.8 17 5 14.5 4.5V2.5Z")


@icon("respiratory-system", CAT, "A head joined by the windpipe to a pair of lungs",
      tags=["breathing", "lungs", "airway", "respiration", "pulmonary", "trachea"], aliases=["respiratory-tract"])
def _(S):
    lung = L(S, "M10.3 11C7.5 11 4 14 3.5 18C3.3 20 4.5 21.5 6.5 21.2L9.5 20.7C10 20.6 10.3 20.2 10.3 19.7Z",
             "M9.3 11C6.8 11.3 4 14.3 3.5 18C3.3 20 4.5 21.5 6.5 21.2L9.4 20.7C10 20.6 10.3 20.2 10.3 19.6V12Q10.3 10.9 9.3 11Z")
    return [shell(circle(12, 4.8, 3)), shell(lung, stroke_miterlimit="2"), shell(mirror(lung), stroke_miterlimit="2"),
            line(seg(12, 7.8, 12, 16))]


@icon("circulatory-system", CAT, "A figure whose heart sends blood vessels out to the arms and legs",
      tags=["cardiovascular", "blood circulation", "heart", "blood vessels", "arteries", "veins"], aliases=["cardiovascular-system"])
def _(S):
    heart = L(S, "M12 16.5L7.9 12.5A2.7 2.7 0 0 1 11.5 8.6L12 9.1L12.5 8.6A2.7 2.7 0 0 1 16.1 12.5Z",
              "M11.2 15.7L7.9 12.5A2.7 2.7 0 0 1 11.5 8.6L12 9.1L12.5 8.6A2.7 2.7 0 0 1 16.1 12.5L12.8 15.7Q12 16.5 11.2 15.7Z")
    r = S.r * 0.6
    return [shell(circle(12, 4, 2.5)), shell(heart, stroke_miterlimit="2"),
            line(poly([(7.6, 10.5), (4.5, 12), (2.5, 15.5)], r=r)), line(poly([(16.4, 10.5), (19.5, 12), (21.5, 15.5)], r=r)),
            line(poly([(12, 16.5), (8.5, 21.5)], r=r)), line(poly([(12, 16.5), (15.5, 21.5)], r=r))]


# ============================================================================ bones and joints

@icon("femur", CAT, "The femur: the long thigh bone with a ball-shaped head on an angled neck",
      tags=["thigh bone", "bone", "leg", "hip", "skeleton", "orthopedic"], aliases=["thigh-bone"])
def _(S):
    neck = poly([(6.2, 3.8), (8.2, 3), (13.5, 7.5), (11, 9.5)], closed=True)
    shaft = rect(10.5, 7, 3.5, 11, L(S, 0, 1))
    body = union(circle(6.8, 4.8, 2.6), neck, shaft, circle(14.6, 6.8, 1.8), circle(9.8, 18.8, 2.7), circle(14.7, 18.8, 2.7))
    return [shell(body, stroke_miterlimit="2")]


@icon("vertebra", CAT, "A single vertebra seen from above: a round body, a ring behind it and three bony spurs",
      tags=["vertebrae", "spine", "backbone", "spinal", "bone", "chiropractic"])
def _(S):
    r = L(S, 0, 1)
    spur = poly([(10.3, 13), (12, 21.5), (13.7, 13)], closed=True, r=r)
    wing = poly([(8.5, 10.5), (2.5, 15.5), (4, 17), (9.5, 14)], closed=True, r=r)
    body = union(ellipse(12, 7, 7.5, 4.5), circle(12, 12.5, 4.2), spur, wing, mirror(wing))
    return [shell(body, stroke_miterlimit="2"), detail(L(S, poly([(10.5, 11.5), (13.5, 11.5), (12, 14)], closed=True), ellipse(12, 12.4, 1.6, 1.4)))]


@icon("hand-skeleton", CAT, "The bones of the hand: small wrist bones with five chains of finger bones",
      tags=["hand bones", "phalanges", "metacarpals", "x-ray", "skeleton", "wrist"], aliases=["hand-bones"])
def _(S):
    parts = [shell(L(S, rect(7, 17.5, 9, 4, 1), rect(7, 17.5, 9, 4, 2)))]
    fingers = [(8.3, 15.5, 6.5, 6.5, 2), (10.8, 15.5, 10, 2.5, 3), (13.3, 15.5, 14, 3, 3), (15.8, 15.5, 18, 5, 3)]
    for x0, y0, x1, y1, n in fingers:
        # dashes from (x0, y0) to (x1, y1) in n + 1 bones
        k = n + 1
        for i in range(k):
            t0, t1 = i / k + 0.1 / k, (i + 1) / k - 0.35 / k
            parts.append(line(seg(x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0, x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1)))
    parts += [line(seg(6.5, 17, 4, 14)), line(seg(3.2, 12.8, 2.2, 10.5))]
    return parts


@icon("ball-and-socket-joint", CAT, "A ball-and-socket joint: a rounded bone head sitting in a cup-shaped socket",
      tags=["joint", "hip joint", "shoulder joint", "orthopedic", "bone", "arthritis"], aliases=["ball-socket-joint"])
def _(S):
    head = union(circle(12, 10, 4), L(S, rect(10, 2, 4, 7), rect(10, 2, 4, 7, 1.5)))
    ring = path_to_d(D(P(circle(12, 10, 9)), P(circle(12, 10, 7)), P(rect(0, 0, 24, 11.5))))
    cup = union(ring, L(S, rect(10, 17, 4, 4.5), rect(10, 17, 4, 4.5, 1.5)))
    return [shell(head), shell(cup, stroke_miterlimit="2")]


# ============================================================================ blood cells

@icon("red-blood-cell", CAT, "A red blood cell shown face on as a dimpled disc and edge on as a pinched oval",
      tags=["erythrocyte", "rbc", "blood cell", "hematology", "anemia", "blood"], aliases=["erythrocyte"])
def _(S):
    edge = L(S, "M18 3.5C20.5 3.5 21.5 5.5 21.5 8C21.5 10 20.5 11 20.5 12C20.5 13 21.5 14 21.5 16C21.5 18.5 20.5 20.5 18 20.5"
                "C15.5 20.5 17.5 18.5 17.5 16C17.5 14 18.5 13 18.5 12C18.5 11 17.5 10 17.5 8C17.5 5.5 15.5 3.5 18 3.5Z",
             "M19.5 3.5C21 3.5 21.5 5.5 21.5 8C21.5 10 20.5 11 20.5 12C20.5 13 21.5 14 21.5 16C21.5 18.5 21 20.5 19.5 20.5"
                "C18 20.5 17.5 18.5 17.5 16C17.5 14 18.5 13 18.5 12C18.5 11 17.5 10 17.5 8C17.5 5.5 18 3.5 19.5 3.5Z")
    return [shell(circle(8.5, 12, 6)), detail(circle(8.5, 12, 2.3)), shell(edge)]


def _scallop(cx, cy, r, n, bulge):
    pts = [polar(cx, cy, r, -90 + i * 360 / n) for i in range(n)]
    chord = 2 * r * math.sin(math.pi / n)
    rr = (chord / 2) / math.sin(math.radians(bulge))
    out = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(1, n + 1):
        x, y = pts[i % n]
        out += f"A{fmt(rr)} {fmt(rr)} 0 0 1 {fmt(x)} {fmt(y)}"
    return out + "Z"


@icon("white-blood-cell", CAT, "A white blood cell with a bumpy edge and a large lobed nucleus",
      tags=["leukocyte", "wbc", "immune cell", "neutrophil", "immunity", "blood"], aliases=["leukocyte"])
def _(S):
    outline = _scallop(12, 12, 8.8, 10, L(S, 70, 50))
    nucleus = path_to_d(U(P(circle(8.5, 13.2, 2.1)), P(circle(12, 10, 2.1)), P(circle(15.5, 13, 2.1)),
                          ST("M8.5 13.2L12 10L15.5 13", 2.2, "round", "round")))
    return [shell(outline, stroke_miterlimit="2"), detail(nucleus)]


@icon("sickle-cell", CAT, "A crescent-shaped sickle red blood cell next to a normal round cell",
      tags=["sickle cell disease", "sickle cell anemia", "blood disorder", "hematology", "red blood cell", "genetic"])
def _(S):
    moon = path_to_d(D(P(circle(10, 12, 8)), P(circle(14.5, 9.5, 7))))
    return [shell(moon, stroke_miterlimit=L(S, "2", "4")), shell(circle(17, 9, 3.5)), dot(17, 9, 1)]


@icon("antibody", CAT, "A Y-shaped antibody molecule with two arms and a stem",
      tags=["immunoglobulin", "immune system", "antigen", "immunity", "igg", "vaccine"], aliases=["immunoglobulin"])
def _(S):
    y = poly([(9.8, 13.5), (4, 6.5), (6.5, 4.5), (12, 10.5), (17.5, 4.5), (20, 6.5), (14.2, 13.5), (14.2, 21.5), (9.8, 21.5)],
             closed=True, r=S.r * 0.5)
    return [shell(y, stroke_miterlimit="2"), line(seg(2, 9.5, 6, 14)),
            line(seg(22, 9.5, 18, 14))]


def _rod(S, pts, w=4.5):
    cap = "round" if S.name == "rounded" else "butt"
    return path_to_d(ST(poly(pts, r=S.r), w, cap, "round"))


@icon("chromosome", CAT, "An X-shaped chromosome: two banded arms pinched together at the centre",
      tags=["genetics", "dna", "gene", "karyotype", "biology", "heredity"])
def _(S):
    left = _rod(S, [(5.5, 3.5), (10, 12), (5.5, 20.5)])
    right = mirror(left)
    return [shell(left), shell(right), detail("M4.9 7.1L8.8 5.6"),
            detail(mirror("M4.9 7.1L8.8 5.6")), detail("M4.9 16.9L8.8 18.4"), detail(mirror("M4.9 16.9L8.8 18.4"))]


@icon("cell-division", CAT, "A cell pinching in the middle into two new cells, each with its own nucleus",
      tags=["mitosis", "cell cycle", "biology", "replication", "growth", "cytokinesis"], aliases=["mitosis"])
def _(S):
    body = union(circle(7.5, 12, 5.5), circle(16.5, 12, 5.5))
    if S.name == "rounded":
        body = union(body, ellipse(12, 12, 2, 4))
    return [shell(rot(body, -40), stroke_miterlimit="2"), dot(*polar(12, 12, 5, 140), 1.7), dot(*polar(12, 12, 5, -40), 1.7)]


@icon("mitochondrion", CAT, "A capsule-shaped mitochondrion with its folded inner membrane",
      tags=["mitochondria", "powerhouse", "organelle", "cell biology", "energy", "atp"], aliases=["mitochondria"])
def _(S):
    outer = rot(L(S, rect(2.5, 6.5, 19, 11, 5.5), ellipse(12, 12, 9.5, 5.8)), -30)
    fold = rot(poly([(4.5, 12), (6.5, 8.5), (8.5, 15.5), (11, 8.5), (13, 15.5), (15.5, 8.5), (17.5, 15.5), (19.5, 12)], r=S.r), -30)
    return [shell(outer), detail(fold)]


@icon("cancer-cell", CAT, "An irregular lumpy cancer cell with an oversized nucleus and spiky edges",
      tags=["tumor", "tumour", "oncology", "cancer", "malignant", "carcinoma"], aliases=["tumor-cell"])
def _(S):
    d = ("M11 3.5C13 3.5 14 5 15.5 5C17.5 5 20 6.5 19.5 9C19.2 10.5 20.5 11.5 20.5 13.5C20.5 16 18.5 16.5 17.5 18"
         "C16.5 20 14.5 21 12.5 20C10.5 19 8.5 21 6 19.5C4 18.3 5 16 4 14.5C3 13 3 10.5 4.5 9.5C5.5 8.8 5.5 7 6.5 5.8C7.8 4.3 9.5 3.5 11 3.5Z")
    return [shell(d), detail(L(S, "M9 10.5C9 8.5 11 7.5 13 8C15.5 8.5 16 10.5 15.5 12.5C15 14.5 13 15.5 11 15C9.5 14.6 9 12.5 9 10.5Z",
                               "M9 10.5C9 8.5 11 7.5 13 8C15.5 8.5 16 10.5 15.5 12.5C15 14.5 13 15.5 11 15C9.5 14.6 9 12.5 9 10.5Z")),
            line(L(S, "M21 6L22.5 4.5", "M21 6L22.5 4.5")), line(seg(2.8, 9.2, 1.5, 8)), line(seg(8.8, 20.8, 8.2, 22.5)), line(seg(20.6, 17.5, 22.2, 18.5))]


@icon("stem-cell", CAT, "A stem cell with arrows leading to three different specialised cells",
      tags=["stem cells", "regenerative medicine", "differentiation", "biology", "cell therapy", "pluripotent"])
def _(S):
    r = S.r * 0.4
    return [shell(circle(12, 6, 3.8)), dot(12, 6, 1.3),
            line(seg(9, 9.5, 6.5, 13)), line(seg(12, 10.5, 12, 13.5)), line(seg(15, 9.5, 17.5, 13)),
            shell(circle(4.8, 18.3, 2.5)),
            shell(rect(9.5, 16, 5, 5, L(S, 0, 1.5))),
            shell(poly([(19.2, 15.5), (22, 21), (16.4, 21)], closed=True, r=L(S, 0, 1)), stroke_miterlimit="2")]


@icon("sperm-cell", CAT, "A sperm cell with an oval head and a long wavy tail",
      tags=["sperm", "spermatozoon", "fertility", "reproduction", "ivf", "male fertility"], aliases=["spermatozoon"])
def _(S):
    head = rot(L(S, poly([(3.2, 8), (6, 5.5), (10.5, 5.5), (12.8, 8), (10.5, 10.5), (6, 10.5)], closed=True, r=1.5),
                 ellipse(8, 8, 4.8, 3)), 40, 8, 8)
    return [shell(head), line("M11 11.5C12.5 14 15.5 12 17 14.5S16.5 19.5 19 21.5")]


@icon("ovum", CAT, "An egg cell: a large round cell with a thick outer layer, a nucleus and small cells around it",
      tags=["egg cell", "oocyte", "fertility", "reproduction", "ivf", "ovulation"], aliases=["egg-cell"])
def _(S):
    parts = [shell(circle(12, 12, 7)), detail(circle(12, 12, 5)), dot(13, 11, 1.6)]
    for a in range(0, 360, 45):
        x, y = polar(12, 12, 10, a + 22.5)
        parts.append(dot(x, y, 1.15) if S.name == "rounded" else solid(rect(x - 1.05, y - 1.05, 2.1, 2.1)))
    return parts


@icon("fertilization", CAT, "A sperm cell reaching the surface of a large egg cell",
      tags=["fertilisation", "conception", "ivf", "fertility", "egg and sperm", "pregnancy"], aliases=["fertilisation", "conception"])
def _(S):
    head = rot(L(S, poly([(6.3, 8.8), (7.8, 7.3), (10, 7.3), (11.5, 8.8), (10, 10.3), (7.8, 10.3)], closed=True, r=1),
                 ellipse(8.9, 8.8, 2.7, 1.7)), 45, 8.9, 8.8)
    return [shell(circle(14.5, 14.5, 7)), dot(15.5, 15.5, 1.8), shell(head), line("M7 6.8C6.5 4.5 4.5 5.5 4 3.8S3 1.8 2 2")]


@icon("embryo", CAT, "An early embryo: a tight ball of cells inside a thin outer ring",
      tags=["morula", "ivf", "fertility", "early pregnancy", "embryology", "cells"], aliases=["morula"])
def _(S):
    cs = [circle(9.5, 9.5, 3), circle(14.5, 9.5, 3), circle(9.5, 14.5, 3), circle(14.5, 14.5, 3)]
    if S.name == "rounded":
        cs += [circle(12, 7.4, 0.9), circle(12, 16.6, 0.9), circle(7.4, 12, 0.9), circle(16.6, 12, 0.9)]
    return [shell(circle(12, 12, 9.5)), detail(union(*cs)), detail("M12 8.5V15.5M8.5 12H15.5")]


@icon("fetus", CAT, "A curled fetus inside the round womb, with a large head, tucked knees and the umbilical cord",
      tags=["foetus", "pregnancy", "baby", "womb", "prenatal", "unborn"], aliases=["foetus"])
def _(S):
    body = path_to_d(U(P(circle(10, 9, 3.4)), P(rot(ellipse(13.5, 14.8, 4.3, 3.4), 40, 13.5, 14.8)), P(circle(11, 17.3, 1.8))))
    body = path_to_d(D(P(body), ST("M9.8 14.2C11 14.8 12.5 14.5 13.3 13.3", 1.2, "round", "round")))
    ring = L(S, circle(12, 12, 9.8), circle(12, 12, 9.8))
    return [shell(ring), Part("dot", body), detail(L(S, "M17.5 11.5L20.5 9", "M17.5 11.5C18.5 11.5 19.5 10.5 20.5 9"))]


@icon("rna", CAT, "An RNA molecule: a single wavy strand with base rungs sticking out on one side",
      tags=["ribonucleic acid", "mrna", "genetics", "molecule", "biology", "vaccine"], aliases=["mrna"])
def _(S):
    parts = [line("M8 2.5C5 5.5 5 8.5 8 12S11 18.5 8 21.5")]
    for y, x in ((5, 6.6), (9, 6.9), (15, 9.1), (19, 9.2)):
        parts.append(line(seg(x + 1, y, 18, y)))
    return parts


@icon("bacteriophage", CAT, "A bacteriophage virus with an angular head, a straight tail and jointed legs",
      tags=["phage", "virus", "microbiology", "bacteria", "biology", "infection"], aliases=["phage"])
def _(S):
    head = poly(regular(12, 6, 4.3, 6), closed=True, r=L(S, 0, 1))
    tail = rect(10.5, 11.5, 3, 5.5, L(S, 0, 1))
    r = S.r * 0.5
    return [shell(head, stroke_miterlimit="4"), shell(tail), line(seg(8.5, 17, 15.5, 17)),
            line(poly([(9, 17), (5, 18.5), (3.5, 21.5)], r=r)), line(poly([(15, 17), (19, 18.5), (20.5, 21.5)], r=r))]


@icon("spiral-bacteria", CAT, "A corkscrew-shaped spiral bacterium with a thin whip tail at each end",
      tags=["spirillum", "spirochete", "bacteria", "microbiology", "germ", "infection"], aliases=["spirillum"])
def _(S):
    body = "M6.5 17.5C7.5 13.5 9 11.5 10.5 13.5S12.5 17 14 14S15.5 8 17.5 6.5"
    cap = "round" if S.name == "rounded" else "butt"
    return [shell(path_to_d(ST(body, 3.5, cap, "round"))), line("M6.3 19.5C5.8 21 4 21 3 22"), line("M18.8 5.3C19.5 3.8 20.5 3 21.8 2.5")]


@icon("streptococcus", CAT, "A chain of small round bacteria linked in a gentle curve",
      tags=["strep", "bacteria", "strep throat", "cocci", "microbiology", "infection"], aliases=["strep"])
def _(S):
    parts = []
    for a in (200, 235, 270, 305, 340):
        x, y = polar(12, 17, 9, a)
        parts.append(shell(circle(x, y, 2.3) if S.name == "rounded" else poly(regular(x, y, 2.45, 8, a + 22.5), closed=True)))
    return parts


# ============================================================================ muscle groups

def _hl_filled(outline, regions):
    """Filled design: solid silhouette with a 2 px gap around each solid muscle region."""
    def f():
        body = solid_of(outline)
        cut = U(*[U(P(r), ST(r, 4, "round", "round")) for r in regions])
        return U(D(body, cut), *[P(r) for r in regions])
    return f


_LOWER = "M5 3H19C19.8 6 20.5 9 20.5 12.5L19.5 21.5H13.5L12.5 15H11.5L10.5 21.5H4.5L3.5 12.5C3.5 9 4.2 6 5 3Z"
_LOWER_R = ("M6 3H18Q19 3 19.3 4C19.9 6.5 20.5 9.3 20.5 12.5L19.6 20.5Q19.5 21.5 18.5 21.5H14.4Q13.5 21.5 13.4 20.6L12.5 15H11.5"
            "L10.6 20.6Q10.5 21.5 9.6 21.5H5.5Q4.5 21.5 4.4 20.5L3.5 12.5C3.5 9.3 4.1 6.5 4.7 4Q5 3 6 3Z")
_GLUTE = "M11.3 7C11.3 5.8 9.5 5.3 7.8 5.8C6.3 6.3 5.8 8 5.8 10C5.8 11.8 7 13 8.8 13C10.5 13 11.3 11.8 11.3 10.5Z"


@icon("glutes", CAT, "Rear view of the hips with the buttock muscles highlighted",
      tags=["gluteus", "buttocks", "glute workout", "hips", "muscles", "fitness"], aliases=["gluteus"],
      filled=_hl_filled(_LOWER, [_GLUTE, mirror(_GLUTE)]))
def _(S):
    return [shell(L(S, _LOWER, _LOWER_R)), solid(_GLUTE), solid(mirror(_GLUTE))]


_BACK = ("M9.5 2.5V4.5C7 5 5 5.8 4 7.3C3.3 8.3 3 9.5 3 11V16H5.6L6.5 21.5H17.5L18.4 16H21V11C21 9.5 20.7 8.3 20 7.3"
         "C19 5.8 17 5 14.5 4.5V2.5Z")
_BACK_R = ("M9.5 2.5V4.5C7 5 5 5.8 4 7.3C3.3 8.3 3 9.5 3 11V15Q3 16 4 16H5.6L6.4 20.6Q6.5 21.5 7.4 21.5H16.6Q17.5 21.5 17.6 20.6"
           "L18.4 16H20Q21 16 21 15V11C21 9.5 20.7 8.3 20 7.3C19 5.8 17 5 14.5 4.5V2.5Z")
_LAT = "M7.8 8.5C9 9 10 10 10.8 11.2V17.5C10 18.3 9.3 18.8 8.8 19.2C8.3 16.5 7.8 13.5 7.8 11Z"
_TRAP = "M12 6C13 7.2 16 8 17.8 8.8L13.3 11.5L12 17.5L10.7 11.5L6.2 8.8C8 8 11 7.2 12 6Z"


@icon("lats", CAT, "Rear view of a torso with the wide latissimus muscles on each side of the back highlighted",
      tags=["latissimus dorsi", "back muscles", "v taper", "back workout", "muscles", "fitness"], aliases=["latissimus-dorsi"],
      filled=_hl_filled(_BACK, [_LAT, mirror(_LAT)]))
def _(S):
    return [
        shell(L(S, _BACK, _BACK_R)), solid(_LAT), solid(mirror(_LAT))]


@icon("traps", CAT, "Rear view of the neck and shoulders with the diamond-shaped trapezius muscle highlighted",
      tags=["trapezius", "upper back", "shoulders", "neck muscles", "muscles", "fitness"], aliases=["trapezius"],
      filled=_hl_filled(_BACK, [_TRAP]))
def _(S):
    return [shell(L(S, _BACK, _BACK_R)), solid(_TRAP)]
