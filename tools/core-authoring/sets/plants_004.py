"""TypeIcon Core: plants (batch plants_004): plant anatomy, care, propagation and growing.

Drawn from the plants themselves. Small potted plants share one pot shape so the care icons read as a set.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, LINE, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "plants"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def leaf(x1, y1, x2, y2, bulge):
    """Pointed leaf from (x1, y1) to (x2, y2), each half bowing out by about bulge px."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    b = bulge * 2
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx * b)} {fmt(my + ny * b)} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(mx - nx * b)} {fmt(my - ny * b)} {fmt(x1)} {fmt(y1)}Z")


def leaf_soft(x1, y1, x2, y2, bulge, k=1.0):
    """Leaf like leaf() but with softly rounded tips (for the Rounded style)."""
    ln = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / ln, (y2 - y1) / ln
    nx, ny = -uy, ux
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    b = bulge * 2
    w = 0.9
    a1 = (x1 + ux * k + nx * w * 0.5, y1 + uy * k + ny * w * 0.5)
    b1 = (x1 + ux * k - nx * w * 0.5, y1 + uy * k - ny * w * 0.5)
    a2 = (x2 - ux * k + nx * w * 0.5, y2 - uy * k + ny * w * 0.5)
    b2 = (x2 - ux * k - nx * w * 0.5, y2 - uy * k - ny * w * 0.5)
    f = fmt
    return (f"M{f(a1[0])} {f(a1[1])}Q{f(mx + nx * b)} {f(my + ny * b)} {f(a2[0])} {f(a2[1])}"
            f"Q{f(x2)} {f(y2)} {f(b2[0])} {f(b2[1])}"
            f"Q{f(mx - nx * b)} {f(my - ny * b)} {f(b1[0])} {f(b1[1])}"
            f"Q{f(x1)} {f(y1)} {f(a1[0])} {f(a1[1])}Z")


def rib(x1, y1, x2, y2, t0=0.0, t1=0.8):
    """Midrib line along a leaf axis."""
    return seg(x1 + (x2 - x1) * t0, y1 + (y2 - y1) * t0, x1 + (x2 - x1) * t1, y1 + (y2 - y1) * t1)


def sun(cx, cy, r, rays=8, r0=None, r1=None, S=None):
    """Sun disc with short rays (parts)."""
    r0 = r0 or r + 2
    r1 = r1 or r + 4
    parts = [shell(circle(cx, cy, r))]
    for k in range(rays):
        a = k * 360 / rays
        p0, p1 = polar(cx, cy, r0, a), polar(cx, cy, r1, a)
        parts.append(line(seg(*p0, *p1)))
    return parts


def pot(S, x0, x1, top, bot, inset=1.3):
    """Flower pot: tapered body (shell)."""
    return shell(poly([(x0, top), (x1, top), (x1 - inset, bot), (x0 + inset, bot)], closed=True, r=S.r))


def sprout(cx, base, h, w=3.6, S=None):
    """Stem with a pair of leaves at its top: list of parts (stem line + two leaf shells)."""
    top = base - h
    return [line(seg(cx, base, cx, top + 1.5)),
            shell(leaf(cx, top + 2.2, cx - w, top - 0.6, 1.3)),
            shell(leaf(cx, top + 2.2, cx + w, top - 0.6, 1.3))]


def ground(x0=2.5, x1=21.5, y=21.5):
    return line(seg(x0, y, x1, y))


def drop(cx, cy, s=1.0):
    """Small water drop outline (closed), tip up."""
    return (f"M{fmt(cx)} {fmt(cy - 2.6 * s)}C{fmt(cx + 0.9 * s)} {fmt(cy - 1.3 * s)} {fmt(cx + 2 * s)} {fmt(cy)} "
            f"{fmt(cx + 2 * s)} {fmt(cy + 0.9 * s)}A{fmt(2 * s)} {fmt(2 * s)} 0 0 1 {fmt(cx - 2 * s)} {fmt(cy + 0.9 * s)}"
            f"C{fmt(cx - 2 * s)} {fmt(cy)} {fmt(cx - 0.9 * s)} {fmt(cy - 1.3 * s)} {fmt(cx)} {fmt(cy - 2.6 * s)}Z")


# ============================================================================ anatomy and cells


@icon("pistil", CAT, "Flower pistil with a round ovary, a thin style and a flat stigma on top",
      tags=["pistil", "flower", "carpel", "stigma", "ovary", "botany", "reproduction"])
def _(S):
    return [shell(circle(12, 17, 4)), dot(12, 17, 1.25), line(seg(12, 13, 12, 7)),
            shell(rect(8, 3, 8, 4, L(S, 1, 2)))]


@icon("flower-cross-section", CAT, "Flower cut in half showing two petals around a central pistil on a short stem",
      tags=["flower anatomy", "cross section", "petals", "pistil", "botany", "half flower", "biology"])
def _(S):
    return [shell(leaf(11, 18.5, 3.5, 5.5, 2.6)), shell(leaf(13, 18.5, 20.5, 5.5, 2.6)),
            line(seg(12, 21.5, 12, 10)), dot(12, 7.5, 1.8)]


@icon("stem-cross-section", CAT, "Round cut stem with a ring of small vascular bundles around the centre",
      tags=["stem", "cross section", "vascular bundle", "xylem", "phloem", "botany", "plant anatomy"])
def _(S):
    parts = [shell(circle(12, 12, 9))]
    for k in range(6):
        x, y = polar(12, 12, 5.2, -90 + k * 60)
        if S.name == "line":
            parts.append(Part("dot", rect(x - 1.2, y - 1.2, 2.4, 2.4)))
        else:
            parts.append(dot(x, y, 1.4))
    parts.append(dot(12, 12, 1.2))
    return parts


def _guard(S, sign):
    """Bean-shaped guard cell: sign -1 left, +1 right."""
    def X(x):
        return 12 + sign * (x - 12)
    t = L(S, 0, 0.8)
    d = (f"M{fmt(X(10.2))} {fmt(4 + t)}C{fmt(X(5))} {fmt(3)} {fmt(X(3))} {fmt(8)} {fmt(X(3))} {fmt(12)}"
         f"S{fmt(X(5))} {fmt(21)} {fmt(X(10.2))} {fmt(20 - t)}C{fmt(X(7.6))} {fmt(16.5)} {fmt(X(7.6))} {fmt(7.5)} {fmt(X(10.2))} {fmt(4 + t)}Z")
    return d


@icon("leaf-stoma", CAT, "Leaf pore made of two bean-shaped guard cells with a slit opening between them",
      tags=["stoma", "stomata", "guard cells", "leaf pore", "transpiration", "botany", "gas exchange"])
def _(S):
    return [shell(_guard(S, -1)), shell(_guard(S, 1)), dot(6.4, 12, 1.2), dot(17.6, 12, 1.2)]


@icon("plant-cell", CAT, "Plant cell with a thick rectangular wall, a large vacuole, a nucleus and a chloroplast",
      tags=["plant cell", "cell wall", "vacuole", "nucleus", "biology", "organelle", "cell"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 17, L(S, 1, 4))),
            detail(rect(6.5, 7, 7.5, 10, L(S, 1, 2.5))),
            dot(17.7, 8.5, 2.1),
            Part("dot", ellipse(17.7, 15.5, 1.7, 1.2))]


@icon("chloroplast", CAT, "Oval chloroplast with two stacks of flat discs inside",
      tags=["chloroplast", "thylakoid", "grana", "organelle", "photosynthesis", "biology", "plant cell"])
def _(S):
    body = L(S, "M2.5 12C7 1.5 17 1.5 21.5 12C17 22.5 7 22.5 2.5 12Z", ellipse(12, 12, 9.5, 8.5))
    parts = [shell(body, stroke_miterlimit="8")]
    for y in (8, 12, 16):
        parts.append(detail(seg(6.5, y, 10, y)))
        parts.append(detail(seg(14, y, 17.5, y)))
    return parts


@icon("photosynthesis", CAT, "Leaf in the sunlight with small gas bubbles rising from it",
      tags=["photosynthesis", "sunlight", "oxygen", "leaf", "biology", "science", "carbon dioxide"])
def _(S):
    parts = [shell(circle(6, 6, 2.2))]
    for a in (0, 45, 90):
        parts.append(line(seg(*polar(6, 6, 4.2, a), *polar(6, 6, 8.2, a))))
    parts += [shell(leaf(8, 21.5, 21, 13.5, 3.6)), detail(rib(8, 21.5, 21, 13.5, 0.12, 0.75)),
              dot(20, 4.5, 1.5), dot(16.8, 8.5, 1.1)]
    return parts


@icon("phototropism", CAT, "Potted seedling whose curved stem and leaves lean toward a sun at the upper right",
      tags=["phototropism", "light", "seedling", "bending", "growth toward light", "biology", "science"])
def _(S):
    stem = "M8 15.5C8 12.5 9.5 10.5 12 9.2"
    return [pot(S, 3.5, 12.5, 15.5, 21), line(stem),
            shell(leaf(12, 9.2, 11.6, 3.8, 1.4)), shell(leaf(12, 9.2, 17, 11.4, 1.4)),
            shell(circle(19.5, 5, 2.2)),
            line(seg(*polar(19.5, 5, 4.2, 180), *polar(19.5, 5, 5.8, 180))),
            line(seg(*polar(19.5, 5, 4.2, 135), *polar(19.5, 5, 5.8, 135)))]


def _plant_small(S, cx=12, top=15.5, bot=21, hw=5, leaf_y=None, h=6.5):
    """Potted sprout: pot plus stem and two leaves; h = stem height above the pot rim."""
    y = top - h
    return [pot(S, cx - hw, cx + hw, top, bot), *sprout(cx, top, h, 3.8)]


@icon("plant-growth", CAT, "Seed, small sprout and larger leafy plant in a row, rising from a ground line",
      tags=["plant growth", "stages", "seed", "sprout", "growing", "life cycle", "development"])
def _(S):
    return [ground(2, 22), Part("dot", ellipse(4.5, 19.3, 1.9, 1.3)),
            line(seg(10.5, 21.5, 10.5, 16)),
            shell(leaf(10.5, 16.8, 7, 13.6, 1.3)), shell(leaf(10.5, 16.8, 14, 13.6, 1.3)),
            line(seg(18.5, 21.5, 18.5, 4)),
            shell(leaf(18.5, 15.5, 14.8, 11.8, 1.6)), shell(leaf(18.5, 11.5, 22, 8.2, 1.5)),
            shell(leaf(18.5, 8, 15.5, 4.3, 1.3))]


@icon("plant-graft", CAT, "Two stem pieces bound together with a band of tape at the joint, with leaves on the upper piece",
      tags=["graft", "grafting", "scion", "rootstock", "tape", "propagation", "horticulture"])
def _(S):
    return [*sprout(12, 10, 6.5, 4), line(seg(12, 17.5, 12, 21.5)),
            shell(rect(8, 10, 8, 7.5, L(S, 1, 2.5))), detail(seg(9.5, 15.8, 14.5, 11.8))]


@icon("herbarium-specimen", CAT, "Pressed plant with leaves and roots on a paper sheet with a small label in the corner",
      tags=["herbarium", "pressed plant", "specimen", "botany", "collection", "taxonomy", "museum"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 19, L(S, 1, 2.5))),
            detail(seg(10, 7, 10, 15)),
            Part("dot", leaf(10, 12.5, 6.8, 8.8, 1.2)), Part("dot", leaf(10, 10, 14, 6.3, 1.2)),
            detail(poly([(10, 15), (8, 18)], r=0)), detail(poly([(10, 15), (12, 18)], r=0)),
            Part("dot", rect(13.3, 16, 3.7, 2.5))]


@icon("leaf-scan", CAT, "Leaf framed by four corner brackets like a camera scanning viewfinder",
      tags=["leaf scan", "plant identification", "viewfinder", "camera", "scanner", "plant app", "recognition"])
def _(S):
    parts = []
    for (x, y, sx, sy) in ((3, 3, 1, 1), (21, 3, -1, 1), (3, 21, 1, -1), (21, 21, -1, -1)):
        parts.append(line(poly([(x, y + 5 * sy), (x, y), (x + 5 * sx, y)], r=S.r)))
    parts += [shell(leaf(8.5, 16, 15.5, 8, 2.8)), detail(rib(8.5, 16, 15.5, 8, 0.1, 0.75))]
    return parts


def _sun(cx, cy, S, r=2.5, rays=8):
    parts = [shell(circle(cx, cy, r))]
    for k in range(rays):
        a = k * 360 / rays
        parts.append(line(seg(*polar(cx, cy, r + 1.5, a), *polar(cx, cy, r + 3, a))))
    return parts


@icon("plant-full-sun", CAT, "Small potted plant under a full sun with rays",
      tags=["full sun", "sunny spot", "light requirement", "plant care", "sun loving", "garden", "bright"])
def _(S):
    return [*_plant_small(S, 7.5, 15.5, 21, 4.5, h=6), *_sun(16.5, 7.5, S)]


@icon("plant-partial-shade", CAT, "Small potted plant under a sun disc that is only half filled",
      tags=["partial shade", "part sun", "half shade", "light requirement", "plant care", "garden", "dappled"])
def _(S):
    half = "M16.5 5.3A2.2 2.2 0 0 0 16.5 9.7Z"
    return [*_plant_small(S, 7.5, 15.5, 21, 4.5, h=6), *_sun(16.5, 7.5, S), Part("dot", half)]


@icon("plant-full-shade", CAT, "Small potted plant beside a cloud with no sun",
      tags=["full shade", "shade loving", "low light", "light requirement", "plant care", "garden", "cloud"])
def _(S):
    cloud = union(circle(14.6, 9.5, 2.3), circle(17.8, 7, 3.3), circle(20.1, 9.6, 2.1), rect(14.6, 9.5, 5.6, 2.2))
    return [*_plant_small(S, 7.5, 15.5, 21, 4.5, h=6), shell(cloud)]


@icon("plant-watering", CAT, "Potted plant with three water drops falling onto its leaves",
      tags=["watering", "water plant", "plant care", "irrigation", "drops", "garden", "houseplant"])
def _(S):
    return [*_plant_small(S, 12, 15.5, 21, 5, h=6),
            Part("solid", drop(6.5, 6.5, 0.8)), Part("solid", drop(12, 3.8, 0.8)), Part("solid", drop(17.5, 6.5, 0.8))]


@icon("plant-humidity", CAT, "Potted plant beside small water droplets and a wavy vapor line",
      tags=["humidity", "moisture", "damp air", "plant care", "tropical plant", "vapor", "houseplant"])
def _(S):
    return [*_plant_small(S, 7.5, 15.5, 21, 4.5, h=6),
            Part("solid", drop(17.5, 5.2, 0.85)), Part("solid", drop(20.3, 11, 0.7)),
            line("M17.5 21C15.5 19 19.5 18 17.5 16C15.5 14 18.5 13.5 17 12.5")]


@icon("plant-temperature", CAT, "Potted plant beside a small thermometer",
      tags=["temperature", "thermometer", "plant care", "climate", "heat", "cold tolerance", "houseplant"])
def _(S):
    th = union(rect(16.6, 3, 2.8, 12, 1.4), circle(18, 17.5, 3))
    return [*_plant_small(S, 7.5, 15.5, 21, 4.5, h=6), shell(th), detail(seg(18, 17, 18, 9))]


@icon("plant-height", CAT, "Plant with a tall vertical double-headed arrow beside it measuring its height",
      tags=["plant height", "measure", "tall", "growth", "dimension", "size", "garden planning"])
def _(S):
    return [*_plant_small(S, 8, 16, 21.5, 5, h=11),
            line(seg(19, 4.5, 19, 19.5)),
            line(poly([(16.8, 6.8), (19, 4.5), (21.2, 6.8)], r=S.r)),
            line(poly([(16.8, 17.2), (19, 19.5), (21.2, 17.2)], r=S.r))]


def _arrow_h(S, x0, x1, y, hs=2.2):
    return [line(seg(x0, y, x1, y)),
            line(poly([(x0 + hs, y - hs), (x0, y), (x0 + hs, y + hs)], r=S.r)),
            line(poly([(x1 - hs, y - hs), (x1, y), (x1 - hs, y + hs)], r=S.r))]


@icon("plant-spacing", CAT, "Two small plants on a ground line with a double-headed arrow above showing the distance between them",
      tags=["plant spacing", "distance", "row spacing", "planting", "garden planning", "gap", "measure"])
def _(S):
    return [ground(2, 22), *sprout(5.5, 21.5, 8, 3.2), *sprout(18.5, 21.5, 8, 3.2), *_arrow_h(S, 4.5, 19.5, 6.5)]


def _skull():
    head = union(circle(12, 11.3, 2.9), rect(10.3, 12.6, 3.4, 3.3))
    return minus(head, circle(10.8, 11.2, 0.9), circle(13.2, 11.2, 0.9))


@icon("poisonous-plant", CAT, "Large leaf with a small skull symbol on it",
      tags=["poisonous plant", "toxic", "skull", "danger", "warning", "hazard", "unsafe to eat"])
def _(S):
    return [shell(leaf(3.5, 20.5, 20.5, 3.5, L(S, 5.4, 6.3))), Part("dot", _skull())]


@icon("wilted-plant", CAT, "Potted plant with limp drooping stems and leaves hanging over the sides",
      tags=["wilted plant", "dying", "drooping", "thirsty", "dehydrated", "plant care", "unhealthy"])
def _(S):
    return [pot(S, 7, 17, 14.5, 21),
            line("M10.5 14.5C10.5 9 8 7.5 5.5 9.5"), shell(leaf(5.5, 9.5, 4.3, 16.2, 1.6)),
            line("M13.5 14.5C13.5 8 16 6.5 18.5 8.5"), shell(leaf(18.5, 8.5, 19.7, 15.2, 1.6))]


@icon("plant-cutting", CAT, "Stem cutting with two leaves standing in a glass of water with small roots growing at the bottom",
      tags=["cutting", "propagation", "water propagation", "root growth", "glass", "houseplant", "clone"])
def _(S):
    return [*sprout(12, 9.5, 6, 3.8),
            shell(poly([(7, 9.5), (17, 9.5), (16, 21), (8, 21)], closed=True, r=S.r)),
            detail(seg(12, 9.5, 12, 15.5)),
            detail(poly([(12, 15.5), (9.6, 18)], r=0)), detail(poly([(12, 15.5), (14.4, 18)], r=0))]


@icon("leaf-propagation", CAT, "Single plump succulent leaf lying on soil with tiny roots below and a new rosette growing at its base",
      tags=["leaf propagation", "succulent", "new plant", "baby plant", "roots", "cutting", "propagation"])
def _(S):
    return [line(seg(2, 17.5, 22, 17.5)),
            shell(leaf(13, 16.5, 4.5, 8.5, 3.6)),
            line(poly([(13, 17.5), (11, 21.5)], r=0)), line(poly([(13, 17.5), (15, 21.5)], r=0)),
            *sprout(19, 17.5, 6.5, 3)]


def _half(S, left=True):
    d = f"M3 10.5H10V20.5C{L(S, '5.5 20.5', '6 20.5')} 3 {L(S, '17', '16.5')} 3 12.5Z"
    return d if left else path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


@icon("plant-division", CAT, "Plant clump cut into two halves with a gap between them, each half with its own sprout",
      tags=["division", "divide plant", "split clump", "propagation", "perennial", "roots", "garden"])
def _(S):
    return [*sprout(6.5, 10.5, 7, 3.4), *sprout(17.5, 10.5, 7, 3.4),
            shell(_half(S, True)), shell(_half(S, False))]


@icon("repotting", CAT, "Plant in a small pot with a curved arrow to a larger empty pot",
      tags=["repotting", "transplant", "larger pot", "move plant", "plant care", "potting up", "gardening"])
def _(S):
    return [pot(S, 2.5, 9.5, 15, 21), *sprout(6, 15, 6, 3.2),
            pot(S, 12.5, 21.5, 13.5, 21, 1.6),
            line("M8.5 6.5C12 3 17.5 4.5 17 9.5"),
            line(poly([(14.9, 7.4), (17, 10), (19.2, 7.4)], r=S.r))]


@icon("hydroponic-plant", CAT, "Plant in a net cup above a water tank with bare roots hanging into the water and bubbles",
      tags=["hydroponics", "soilless", "water culture", "nutrient tank", "roots", "indoor growing", "bubbles"])
def _(S):
    return [line(poly([(3, 13), (3, 21), (21, 21), (21, 13)], r=S.r)),
            shell(poly([(8, 9.5), (16, 9.5), (14.8, 13.5), (9.2, 13.5)], closed=True, r=S.r)),
            *sprout(12, 9.5, 6.5, 3.8),
            line(poly([(10.4, 13.5), (10, 18)], r=0)), line(poly([(13.6, 13.5), (14, 18)], r=0)),
            dot(6.3, 17, 1.2), dot(18, 16.2, 1.2), dot(17.4, 19, 0.8)]


def _mini(cx, base, h, w=2.4):
    top = base - h
    return [line(seg(cx, base, cx, top + 1)),
            Part("solid", leaf(cx, top + 1.6, cx - w, top - 0.6, 0.9)),
            Part("solid", leaf(cx, top + 1.6, cx + w, top - 0.6, 0.9))]


@icon("seedling-tray", CAT, "Seedling tray with three cells, each holding a tiny two-leaf sprout",
      tags=["seedling tray", "seed starting", "nursery", "cell tray", "plug tray", "sprouts", "gardening"])
def _(S):
    return [shell(poly([(2.5, 13.5), (21.5, 13.5), (20, 21), (4, 21)], closed=True, r=S.r)),
            detail(seg(8.9, 13.5, 8.6, 21)), detail(seg(15.1, 13.5, 15.4, 21)),
            *_mini(5.7, 13.5, 6.5), *_mini(12, 13.5, 6.5), *_mini(18.3, 13.5, 6.5)]


@icon("plant-marker", CAT, "Pointed plant label stake pushed into the soil beside a young sprout",
      tags=["plant label", "garden marker", "stake", "tag", "plant identification", "seedling", "gardening"])
def _(S):
    return [shell(poly([(3, 3), (12, 3), (12, 14), (7.5, 21.5), (3, 14)], closed=True, r=S.r)),
            detail(seg(5.6, 7.5, 9.4, 7.5)),
            line(seg(14, 19.5, 22, 19.5)), *sprout(18, 19.5, 7, 3.6)]


@icon("climbing-plant", CAT, "Vine with leaves winding up between the rungs of a trellis",
      tags=["climbing plant", "vine", "trellis", "creeper", "lattice", "garden", "climber"])
def _(S):
    return [line(seg(4.5, 2.5, 4.5, 21.5)), line(seg(19.5, 2.5, 19.5, 21.5)),
            line(seg(4.5, 8.5, 19.5, 8.5)), line(seg(4.5, 15.5, 19.5, 15.5)),
            line("M12 21.5C12 18 15.5 17.5 15 14C14.5 10.5 9 11 9.5 7.5C10 4.5 13 5 13 2.5"),
            Part("solid", leaf(15.3, 17.5, 18.4, 18.8, 1.0)), Part("solid", leaf(9.3, 10.6, 6.2, 11.8, 1.0)),
            Part("solid", leaf(13.2, 5, 16.2, 4.2, 1.0))]


@icon("espalier-tree", CAT, "Tree trained flat with a straight trunk and horizontal arms in tiers turned up at the ends",
      tags=["espalier", "trained tree", "fruit tree", "wall tree", "pruning", "tiers", "orchard"])
def _(S):
    return [ground(2, 22),
            line(seg(12, 21.5, 12, 4)),
            line(poly([(4, 13.5), (4, 17), (20, 17), (20, 13.5)], r=S.r)),
            line(poly([(6.5, 8), (6.5, 11.5), (17.5, 11.5), (17.5, 8)], r=S.r)),
            dot(12, 3.5, 1.4), dot(4, 12.4, 1.4), dot(20, 12.4, 1.4), dot(6.5, 6.9, 1.4), dot(17.5, 6.9, 1.4)]


@icon("plant-mister", CAT, "Small spray bottle misting fine droplets toward a leaf",
      tags=["mister", "spray bottle", "misting", "plant care", "humidity", "houseplant", "water spray"])
def _(S):
    return [shell(rect(3.5, 12.5, 8, 9, L(S, 1.5, 3))),
            shell(rect(4.5, 6, 7, 4, L(S, 1, 2))), line(seg(7.5, 10, 7.5, 12.5)),
            line(seg(11.5, 7.8, 13.8, 7.8)),
            dot(17, 5.3, 1.1), dot(17.6, 9, 1.1), dot(20.6, 7, 1.1),
            shell(leaf(14, 21.5, 21, 14, 2.6)), detail(rib(14, 21.5, 21, 14, 0.15, 0.7))]


@icon("sowing-seeds", CAT, "Hand held over the ground letting seeds fall into a furrow in the soil",
      tags=["sowing", "sow seeds", "planting seeds", "furrow", "seed drop", "gardening", "farming"])
def _(S):
    hand = ("M2.5 4.5H9C11 4.5 12.2 5.5 13.2 6.8C14.6 8.5 15.2 9.7 15.2 11C15.2 12.2 14.3 12.8 13.5 12.8"
            "C12.3 12.8 11.6 11.8 10.6 10.5H2.5Z")
    return [shell(hand), detail(seg(5.5, 4.5, 5.5, 10.5)),
            dot(14.8, 16, 1.15), dot(17.6, 17.4, 1.15),
            line(poly([(2, 18.5), (12, 18.5), (14, 21.5), (19, 21.5), (21, 18.5)], r=S.r))]


@icon("sowing-depth", CAT, "Soil cross-section with a seed buried below the surface and a vertical arrow measuring its depth",
      tags=["sowing depth", "seed depth", "planting depth", "soil", "measure", "seed spacing", "gardening"])
def _(S):
    return [shell(rect(3, 6.5, 18, 15, L(S, 1, 2.5))),
            Part("dot", ellipse(8, 15, 2.3, 1.7)),
            detail(seg(16, 9.5, 16, 17)),
            detail(poly([(14, 11.5), (16, 9.5), (18, 11.5)], r=S.r)),
            detail(poly([(14, 15), (16, 17), (18, 15)], r=S.r))]


@icon("sprout-in-hands", CAT, "Two cupped hands holding a small mound of soil with a sprout growing from it",
      tags=["care", "nurture", "growth", "hands", "sprout", "eco", "sustainability"])
def _(S):
    bowl = f"M2.5 12.5H21.5C21.5 17.5 17.5 21 12 21C6.5 21 2.5 17.5 2.5 12.5Z"
    return [shell(bowl), detail("M6 14.8C6.6 17.3 9 19 12 19C15 19 17.4 17.3 18 14.8"),
            line("M7.5 12.5C7.5 10 9.5 9 12 9C14.5 9 16.5 10 16.5 12.5"),
            *sprout(12, 9, 6, 3.6)]


@icon("reforestation", CAT, "Row of three young saplings of growing size on a ground line",
      tags=["reforestation", "tree planting", "afforestation", "saplings", "forest restoration", "young trees", "environment"])
def _(S):
    def crown(cx, bot, top, b):
        return shell(L(S, leaf(cx, bot, cx, top, b), leaf_soft(cx, bot, cx, top, b, 1.0)))
    return [ground(2, 22),
            line(seg(5, 21.5, 5, 17.5)), crown(5, 17.6, 12.5, 2.3),
            line(seg(12, 21.5, 12, 15)), crown(12, 15.2, 7.5, 3.1),
            line(seg(19, 21.5, 13.5)) if False else line(seg(19, 21.5, 19, 13.5)), crown(19, 13.7, 3, 3.6)]


@icon("living-wall", CAT, "Wall panel divided into a grid of pockets, each holding a small leafy plant",
      tags=["living wall", "green wall", "vertical garden", "plant wall", "biophilic", "architecture", "greenery"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, L(S, 1.5, 3.5))),
             detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
             detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15))]
    for cy in (6, 12, 18):
        for cx in (6, 12, 18):
            parts.append(Part("dot", leaf(cx - 1.3, cy + 1.3, cx + 1.3, cy - 1.3, 0.75)))
    return parts
