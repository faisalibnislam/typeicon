"""TypeIcon Core: materials 002 (leather, paper, stone, concrete, material tests, performance fabrics, recycling).

Swatches, cut-away views and test set-ups. Textures are inner details so that Filled knocks them out.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar, path_to_d

CAT = "materials"


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def sdot(x, y, rx, ry) -> Part:
    return Part("dot", ellipse(x, y, rx, ry))


def rr(S, cap):
    return min(S.R, cap)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def arrow(x1, y1, x2, y2, h=2.2):
    """Open arrow path from (x1,y1) to (x2,y2) with a head at the end."""
    a = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - h * math.cos(a - 0.6), y2 - h * math.sin(a - 0.6))
    p2 = (x2 - h * math.cos(a + 0.6), y2 - h * math.sin(a + 0.6))
    return (f"M{fmt(x1)} {fmt(y1)}L{fmt(x2)} {fmt(y2)}M{fmt(p1[0])} {fmt(p1[1])}L{fmt(x2)} {fmt(y2)}L{fmt(p2[0])} {fmt(p2[1])}")


def drop(cx, cy, s=1.0):
    """Water drop path centred near (cx, cy), height about 6*s."""
    return (f"M{fmt(cx)} {fmt(cy - 3 * s)}C{fmt(cx - 0.5 * s)} {fmt(cy - 2 * s)} {fmt(cx - 2.5 * s)} {fmt(cy)} {fmt(cx - 2.5 * s)} {fmt(cy + 1 * s)}"
            f"A{fmt(2.5 * s)} {fmt(2.5 * s)} 0 0 0 {fmt(cx + 2.5 * s)} {fmt(cy + 1 * s)}C{fmt(cx + 2.5 * s)} {fmt(cy)} {fmt(cx + 0.5 * s)} {fmt(cy - 2 * s)} {fmt(cx)} {fmt(cy - 3 * s)}Z")


def flame(cx, cy, s=1.0):
    """Flame path with base centred at (cx, cy+3s)."""
    def p(x, y):
        return f"{fmt(cx + x * s)} {fmt(cy + y * s)}"
    return (f"M{p(1, -4.2)}C{p(1.5, -2.5)} {p(3, -1.2)} {p(3, 1.5)}A{fmt(3 * s)} {fmt(3 * s)} 0 0 1 {p(-3, 1.5)}"
            f"C{p(-3, 0)} {p(-2.5, -1)} {p(-2, -2.2)}C{p(-1, -1.7)} {p(-0.8, -1)} {p(-0.8, 0)}C{p(-0.8, -1.8)} {p(0, -3.2)} {p(1, -4.2)}Z")


def cloth(S, x, y, w, h, cap=2):
    """Fabric swatch: a rounded rectangle with a cross-weave."""
    return [shell(rect(x, y, w, h, rr(S, cap))),
            detail(seg(x + w / 2, y, x + w / 2, y + h)),
            detail(seg(x, y + h / 2, x + w, y + h / 2))]


def carrow(cx, cy, r, a0, a1, h=2.0):
    """Clockwise arc from a0 to a1 degrees with an open arrow head at the end (use a1 < a0 for counter-clockwise)."""
    d = arc(cx, cy, r, a0, a1) if a1 > a0 else arc(cx, cy, r, a1, a0)
    # arc() always runs clockwise a->b; for ccw we reverse the intent and put the head at a1 (start of the path)
    tip = polar(cx, cy, r, a1)
    tang = a1 + (90 if a1 > a0 else -90)
    pts = []
    for off in (-145, 145):
        t = math.radians(tang + off)
        pts.append((tip[0] + h * math.cos(t), tip[1] + h * math.sin(t)))
    head = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}L{fmt(tip[0])} {fmt(tip[1])}L{fmt(pts[1][0])} {fmt(pts[1][1])}"
    return d + head


def qarrow(p0, c, p1, h=2.0):
    """Quadratic curve p0 -> p1 (control c) with an open arrow head at p1."""
    a = math.atan2(p1[1] - c[1], p1[0] - c[0])
    pts = [(p1[0] - h * math.cos(a + o), p1[1] - h * math.sin(a + o)) for o in (-0.6, 0.6)]
    return (f"M{fmt(p0[0])} {fmt(p0[1])}Q{fmt(c[0])} {fmt(c[1])} {fmt(p1[0])} {fmt(p1[1])}"
            f"M{fmt(pts[0][0])} {fmt(pts[0][1])}L{fmt(p1[0])} {fmt(p1[1])}L{fmt(pts[1][0])} {fmt(pts[1][1])}")


# ============================================================================ leather

@icon("jute-fiber", CAT, "Hank of long wavy fibers hanging from a bar",
      tags=["jute", "burlap", "natural fiber", "hemp", "hank", "twine", "raw fiber", "sisal"])
def _(S):
    return [
        shell(rect(3, 3, 18, 4, rr(S, 1.5))),
        line("M6 7C4.5 11 7.5 15 6 21"),
        line("M10.5 7C9 11 12 15 10.5 21"),
        line("M15 7C13.5 11 16.5 15 15 21"),
        line("M19 7C17.5 11 20.5 15 19 21"),
    ]


@icon("spinneret", CAT, "Nozzle plate extruding fine parallel filaments",
      tags=["spinning", "extrusion", "synthetic fiber", "filament", "nozzle", "fiber production", "textile mill"])
def _(S):
    return [
        shell(poly([(3, 3), (21, 3), (18, 8), (6, 8)], closed=True, r=S.r)),
        line(seg(8, 11, 8, 21)),
        line(seg(12, 11, 12, 21)),
        line(seg(16, 11, 16, 21)),
    ]


@icon("suede-leather", CAT, "Leather square with short brushed nap strokes",
      tags=["suede", "nubuck", "velvety leather", "brushed", "nap", "leather swatch", "soft leather"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(7.5, 9.5, 10, 7)),
        detail(seg(13.5, 9.5, 16, 7)),
        detail(seg(10.5, 14.5, 13, 12)),
        detail(seg(7.5, 18, 10, 15.5)),
        detail(seg(13.5, 18, 16, 15.5)),
    ]


@icon("patent-leather", CAT, "Glossy leather square with strong mirror shine streaks",
      tags=["patent", "shiny leather", "glossy", "lacquered", "gloss", "leather swatch", "shine"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(7, 14, 14, 7)),
        detail(seg(10.5, 17.5, 17.5, 10.5)),
    ]


@icon("vegan-leather", CAT, "Hide outline with a small plant leaf inside",
      tags=["vegan", "faux leather", "plant based", "cruelty free", "synthetic leather", "pu leather", "eco"])
def _(S):
    return [
        shell(poly([(8, 3), (10, 5), (14, 5), (16, 3), (21, 8), (18, 10.5), (18, 16), (21, 20), (15, 21), (12, 19), (9, 21), (3, 20), (6, 16), (6, 10.5), (3, 8)], closed=True, r=S.r * 0.6)),
        Part("dot", "M12 17C9 15.5 9 11 14.5 9.5C16 13.5 15 16 12 17Z"),
    ]


@icon("crocodile-leather", CAT, "Leather square embossed with large rectangular scales",
      tags=["crocodile", "alligator", "embossed", "exotic leather", "reptile", "scales", "croc"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(3, 9, 21, 9)),
        detail(seg(3, 15, 21, 15)),
        detail(seg(12, 3, 12, 21)),
        dot(7.5, 6, 0.9), dot(16.5, 6, 0.9), dot(7.5, 12, 0.9), dot(16.5, 12, 0.9), dot(7.5, 18, 0.9), dot(16.5, 18, 0.9),
    ]


@icon("snakeskin-leather", CAT, "Leather strip with rows of small diamond scales",
      tags=["snakeskin", "python", "reptile", "diamond scales", "exotic leather", "snake", "pattern"])
def _(S):
    return [
        shell(rect(2, 6, 20, 12, S.R)),
        detail(poly([(2, 12), (7, 8), (12, 12), (17, 8), (22, 12)])),
        detail(poly([(2, 12), (7, 16), (12, 12), (17, 16), (22, 12)])),
    ]


@icon("tannery-vat", CAT, "Round tanning vat with liquid and a hide draped over its rim",
      tags=["tannery", "tanning", "vat", "pit", "hide", "leather making", "curing"])
def _(S):
    return [
        shell(union("M4 10V18Q4 21 7 21H17Q20 21 20 18V10Z", ellipse(12, 10, 8, 3))),
        detail(ellipse(12, 10, 8, 3)) if False else detail("M4 15Q6 13.5 8 15T12 15T16 15T20 15"),
        line(poly([(14, 3), (20, 5), (20, 12)], r=S.r)),
    ]


@icon("hide-stretching-frame", CAT, "Square frame with a hide laced to it by cords",
      tags=["stretching frame", "hide", "rawhide", "drying rack", "tanning", "lacing", "leatherwork"])
def _(S):
    return [
        shell(rect(2, 2, 20, 20, rr(S, 2))),
        shell(poly([(8, 7), (16, 7), (17, 10), (15, 12), (17, 14), (16, 17), (8, 17), (7, 14), (9, 12), (7, 10)], closed=True, r=S.r * 0.5)),
    ]


@icon("leather-patch", CAT, "Rectangular leather label with a stitched border",
      tags=["patch", "label", "tag", "debossed", "stitched", "leather label", "badge"])
def _(S):
    return [
        shell(rect(2, 6, 20, 12, rr(S, 3))),
        detail(rect(5, 9, 14, 6, rr(S, 1))),
    ]


@icon("shearling", CAT, "Leather panel with a curly fleece lining along its edge",
      tags=["shearling", "sheepskin", "fleece lining", "wool lining", "fur", "leather", "curly"])
def _(S):
    return [
        shell(rect(3, 3, 18, 8, rr(S, 2))),
        line("M3 14A3 3 0 0 0 9 14A3 3 0 0 0 15 14A3 3 0 0 0 21 14"),
        line("M3 14V13"),
        line("M21 14V13"),
    ]


@icon("vellum", CAT, "Translucent sheet with a faint drawing showing through",
      tags=["vellum", "tracing paper", "parchment", "translucent", "drafting", "transparent paper", "see through"])
def _(S):
    return [
        shell(poly([(4, 3), (15, 3), (20, 8), (20, 21), (4, 21)], closed=True, r=S.r)),
        detail(poly([(14, 3), (14, 9), (20, 9)])) if False else detail(poly([(15, 3), (15, 8), (20, 8)])),
        detail(poly([(7, 18), (10, 13), (13, 17), (16, 12)])),
    ]


@icon("crepe-paper", CAT, "Streamer roll with a crinkled strip unrolled below",
      tags=["crepe", "streamer", "party decoration", "crinkled", "craft paper", "crepe paper roll", "ridges"])
def _(S):
    return [
        shell(union(rect(3, 3, 18, 5, rr(S, 2)), rect(6, 7, 12, 14, 0))),
        detail("M10 11Q8.5 13 10 15T10 19"),
        detail("M14 11Q12.5 13 14 15T14 19"),
    ]


@icon("seed-paper", CAT, "Paper square with scattered seeds and a sprout growing from the top",
      tags=["seed paper", "plantable paper", "sprout", "eco paper", "biodegradable", "growing", "seeds"])
def _(S):
    return [
        shell(rect(3, 10, 18, 11, rr(S, 2))),
        sdot(8, 15, 1.3, 0.9),
        sdot(13, 14.5, 1.3, 0.9),
        sdot(17, 17.5, 1.3, 0.9),
        line(seg(12, 10, 12, 6)),
        shell("M12 7C12 4 9 3.5 7 4.5C7.5 6.5 9.5 7.5 12 7Z"),
        shell("M12 6C12 3.5 15 3 17 4C16.5 5.5 14.5 6.5 12 6Z") if False else line("M12 6C13 4 15 3.5 17 4"),
    ]


@icon("watercolor-paper", CAT, "Spiral-bound sheet with a paint wash and a dotted texture",
      tags=["watercolor", "watercolour", "art paper", "cold press", "paint wash", "sketchbook", "painting"])
def _(S):
    return [
        shell(rect(4, 4, 16, 17, rr(S, 2))),
        line(seg(8, 2, 8, 6)), line(seg(12, 2, 12, 6)), line(seg(16, 2, 16, 6)),
        detail("M7 12C9 10 11 10 12 12S15 14 17 12"),
        dot(8, 17, 0.9), dot(12, 17, 0.9), dot(16, 17, 0.9),
    ]


@icon("foam-board", CAT, "Board edge showing a thick foam core between two thin paper faces",
      tags=["foam board", "foamcore", "foam core", "mounting board", "display board", "model making", "lightweight board"])
def _(S):
    return [
        shell(rect(2, 6, 20, 12, rr(S, 3))),
        detail(seg(2, 9, 22, 9)),
        detail(seg(2, 15, 22, 15)),
        dot(7, 12, 0.8), dot(12, 12, 0.8), dot(17, 12, 0.8),
    ]


@icon("recycled-paper", CAT, "Paper sheet with a recycling loop of arrows in its centre",
      tags=["recycled paper", "recycling", "eco paper", "reuse", "post consumer", "green paper", "sustainable"])
def _(S):
    return [
        shell(poly([(4, 2), (15, 2), (20, 7), (20, 22), (4, 22)], closed=True, r=S.r)),
        detail(poly([(15, 2), (15, 7), (20, 7)])) if False else detail(seg(15, 2, 15, 7)),
        detail(carrow(12, 14.5, 3.8, 200, 340, 1.8)),
        detail(carrow(12, 14.5, 3.8, 20, 160, 1.8)),
    ]


@icon("paper-reel", CAT, "Large paper roll on its side with a sheet unwinding flat",
      tags=["paper roll", "reel", "web paper", "paper mill", "newsprint", "industrial roll", "unwinding"])
def _(S):
    return [
        shell(union(circle(8, 9, 6), rect(8, 14, 13, 6, 0))),
        dot(8, 9, 2),
    ]


@icon("tissue-paper", CAT, "Thin soft sheets fanned out with a soft fold",
      tags=["tissue", "tissue paper", "wrapping", "gift wrap", "soft paper", "napkin", "thin sheets"])
def _(S):
    return [
        shell(poly([(8, 6), (18, 4), (21, 16), (11, 20)], closed=True, r=S.r)),
        line(poly([(5, 17), (3, 8), (11, 3)], r=S.r)),
        detail("M10.5 11.5Q14 9.5 18 12"),
    ]


@icon("flagstone-paving", CAT, "Ground surface of large irregular stones with gaps between",
      tags=["flagstone", "paving", "stone paving", "patio", "crazy paving", "path", "garden path"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(poly([(3, 11), (9, 9), (14, 13), (21, 10)])),
        detail(poly([(9, 9), (11, 3)])),
        detail(poly([(14, 13), (12, 21)])),
        detail(poly([(17, 10.5), (16.5, 3)])),
    ]


@icon("ashlar-wall", CAT, "Wall of neat squared stone blocks in even courses",
      tags=["ashlar", "masonry", "cut stone", "stone wall", "blockwork", "courses", "stonework"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, S.R)),
        detail(seg(2, 9.3, 22, 9.3)),
        detail(seg(2, 14.7, 22, 14.7)),
        detail(seg(9, 4, 9, 9.3)), detail(seg(16, 4, 16, 9.3)),
        detail(seg(6, 9.3, 6, 14.7)), detail(seg(13, 9.3, 13, 14.7)), detail(seg(19, 9.3, 19, 14.7)),
        detail(seg(9, 14.7, 9, 20)), detail(seg(16, 14.7, 16, 20)),
    ]


@icon("gabion-wall", CAT, "Wire mesh cage box filled with round stones",
      tags=["gabion", "wire cage", "stone cage", "retaining wall", "landscaping", "rock filled", "mesh basket"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        dot(8, 8, 1.8), dot(13.5, 8, 1.4), dot(17, 9, 1.2),
        dot(7.5, 13.5, 1.3), dot(12.5, 13, 1.8), dot(17, 14.5, 1.5),
        dot(8.5, 17.5, 1.2), dot(14, 17.5, 1.2),
    ]


@icon("slump-test", CAT, "Metal cone lifted beside a slumped concrete mound with a drop marker",
      tags=["slump", "slump cone", "concrete test", "workability", "abrams cone", "fresh concrete", "quality control"])
def _(S):
    return [
        shell(poly([(4, 3), (9, 3), (11, 10), (2, 10)], closed=True, r=S.r * 0.5)),
        shell("M13 21C13 17 15 14.5 18 14.5C21 14.5 22 18 22 21Z"),
        line(seg(14, 3, 20, 3)),
        line(arrow(17, 3, 17, 10.5)),
    ]


@icon("concrete-formwork", CAT, "Wooden form boards with braces holding a poured concrete wall",
      tags=["formwork", "shuttering", "concrete forms", "pour", "braces", "boards", "construction"])
def _(S):
    return [
        shell(rect(8, 4, 8, 15, rr(S, 1))),
        line(seg(5, 3, 5, 19)),
        line(seg(19, 3, 19, 19)),
        line(seg(5, 11, 2.5, 18)),
        line(seg(19, 11, 21.5, 18)),
        line(seg(2, 21, 22, 21)),
    ]


@icon("precast-concrete-panel", CAT, "Flat wall panel with lifting cables hanging from a crane hook",
      tags=["precast", "prefab", "panel", "crane", "lifting", "concrete slab", "tilt up"])
def _(S):
    return [
        line(seg(12, 2, 12, 4)),
        line(poly([(5, 12), (12, 4), (19, 12)])),
        shell(rect(3, 12, 18, 9, rr(S, 2))),
        detail(seg(12, 12, 12, 21)) if False else detail(seg(8, 16.5, 16, 16.5)),
    ]


@icon("reinforced-concrete", CAT, "Concrete block cross-section with a row of round rebar dots",
      tags=["reinforced", "rebar", "steel bars", "concrete section", "beam", "structural", "reinforcement"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, S.R)),
        dot(6.5, 15, 1.6), dot(10.2, 15, 1.6), dot(13.8, 15, 1.6), dot(17.5, 15, 1.6),
        dot(8, 8, 0.8), dot(16, 8, 0.8),
    ]


@icon("concrete-aggregate", CAT, "Concrete block cross-section with mixed size stones embedded",
      tags=["aggregate", "gravel", "concrete mix", "crushed stone", "exposed aggregate", "cement", "stones"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, S.R)),
        dot(7, 9, 2),
        Part("dot", poly([(12, 8), (16, 7), (17.5, 10.5), (14, 12)], closed=True)),
        dot(18.5, 16, 1.3), dot(9, 15.5, 1.6), dot(14, 16.5, 1.0),
    ]


@icon("hempcrete-block", CAT, "Building block with a speckled fibrous face and a hemp leaf",
      tags=["hempcrete", "hemp", "hemp lime", "bio composite", "natural building", "insulating block", "eco construction"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, S.R)),
        detail(seg(12, 15, 12, 8)), detail(seg(12, 15, 8.5, 9.5)), detail(seg(12, 15, 15.5, 9.5)),
        dot(5.5, 8, 0.8), dot(18.5, 8, 0.8), dot(5.5, 16.5, 0.8), dot(18.5, 16.5, 0.8),
    ]


@icon("rammed-earth-wall", CAT, "Wall section with wavy compressed soil layers of varying thickness",
      tags=["rammed earth", "pise", "earth wall", "adobe", "soil layers", "sustainable building", "compacted earth"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, S.R)),
        detail("M2 8Q7 6 12 8T22 8"),
        detail("M2 13Q7 15 12 13T22 13"),
        detail("M2 17.5Q7 16 12 17.5T22 17.5"),
    ]


@icon("clay-roof-tile", CAT, "Rows of overlapping rounded roof tiles",
      tags=["roof tile", "terracotta", "clay tile", "roofing", "shingle", "pantile", "roof"])
def _(S):
    return [
        line("M3 3V7M9 3V7M15 3V7M21 3V7"),
        line("M3 7A3 3 0 0 0 9 7A3 3 0 0 0 15 7A3 3 0 0 0 21 7"),
        line("M6 10V14M12 10V14M18 10V14"),
        line("M3 17A3 3 0 0 1 6 14M6 14A3 3 0 0 0 12 14A3 3 0 0 0 18 14M18 14A3 3 0 0 1 21 17"),
        line("M3 17V21M9 17V21M15 17V21M21 17V21"),
    ]


@icon("firebrick", CAT, "Single brick with small flames licking along its top edge",
      tags=["firebrick", "fire brick", "refractory", "kiln brick", "furnace", "heat resistant", "fireplace"])
def _(S):
    return [
        shell(rect(2, 13, 20, 8, rr(S, 2))),
        shell(flame(12, 6.55, 1.1)),
        shell(flame(5.5, 8.35, 0.7)),
        shell(flame(18.5, 8.35, 0.7)),
    ]


# ============================================================================ mechanical and surface tests

@icon("hardness-test", CAT, "Pyramid indenter pressing into a sample and leaving a square dent",
      tags=["hardness", "indentation", "vickers", "indenter", "material testing", "durometer", "dent"])
def _(S):
    return [
        shell(poly([(9, 2.5), (15, 2.5), (15, 6.5), (12, 12), (9, 6.5)], closed=True, r=S.r * 0.5)),
        shell(poly([(3, 14.5), (9.5, 14.5), (12, 18), (14.5, 14.5), (21, 14.5), (21, 21), (3, 21)], closed=True, r=S.r * 0.5)),
    ]


@icon("scratch-hardness-test", CAT, "Pointed stylus dragging across a stone sample leaving a scratch line",
      tags=["scratch test", "mohs", "scratch hardness", "stylus", "stone sample", "scribe", "material testing"])
def _(S):
    return [
        shell(rect(2, 12, 20, 9, rr(S, 3))),
        line(seg(20, 2.5, 14.5, 9.5)),
        detail(seg(4.5, 16.5, 14.5, 16.5)),
    ]


@icon("pendulum-impact-test", CAT, "Swinging pendulum hammer striking a notched bar on supports",
      tags=["impact test", "charpy", "izod", "pendulum", "toughness", "hammer", "notched bar", "material testing"])
def _(S):
    return [
        dot(12, 3, 1.5),
        line(seg(12, 3, 6, 12.5)),
        shell(circle(5.5, 14.5, 2.6)),
        line(arc(12, 3, 12, 62, 100)),
        shell(rect(3, 19, 18, 3, rr(S, 1))),
    ]


@icon("compression-test", CAT, "Sample squeezed between two flat plates by inward arrows",
      tags=["compression", "crush test", "compressive strength", "plates", "press", "material testing", "load"])
def _(S):
    return [
        line(arrow(12, 1.5, 12, 5)),
        line(seg(5, 7.5, 19, 7.5)),
        shell(rect(8, 10, 8, 4, rr(S, 1))),
        line(seg(5, 16.5, 19, 16.5)),
        line(arrow(12, 22.5, 12, 19)),
    ]


@icon("bend-test", CAT, "Bar resting on two supports and bending under a centre load",
      tags=["bend", "flexural test", "three point bend", "bending strength", "beam", "deflection", "material testing"])
def _(S):
    return [
        line(arrow(12, 2, 12, 8.5)),
        line("M3 11Q12 17 21 11"),
        line(seg(4, 13, 4, 20)),
        line(seg(20, 13, 20, 20)),
    ]


@icon("fatigue-test", CAT, "Bar with a small crack beside a repeating wave load symbol",
      tags=["fatigue", "cyclic load", "crack", "endurance", "wear", "stress cycles", "material testing"])
def _(S):
    return [
        shell(rect(2, 3, 20, 8, rr(S, 3))),
        detail(poly([(13, 11), (11.5, 8), (13, 6.5)])),
        line("M3 18Q6 13 9 18T15 18T21 18"),
    ]


@icon("torsion-test", CAT, "Rod with curved arrows at each end twisting in opposite directions",
      tags=["torsion", "twist", "torque", "shear stress", "rotation", "rod", "material testing"])
def _(S):
    return [
        shell(rect(7, 9.5, 10, 5, rr(S, 2))),
        line(qarrow((6, 4), (1.5, 12), (6, 20), 2.2)),
        line(qarrow((18, 20), (22.5, 12), (18, 4), 2.2)),
    ]


@icon("shear-test", CAT, "Block split along a line with opposite arrows sliding the halves apart",
      tags=["shear", "sliding", "shear strength", "cut", "slip", "shear stress", "material testing"])
def _(S):
    return [
        shell(rect(6, 2.5, 15, 8, rr(S, 2))),
        shell(rect(3, 13.5, 15, 8, rr(S, 2))),
        detail(arrow(9.5, 6.5, 17.5, 6.5, 2)),
        detail(arrow(14.5, 17.5, 6.5, 17.5, 2)),
    ]


@icon("drop-test", CAT, "Box falling toward a hard floor with motion lines and a height arrow",
      tags=["drop test", "fall", "impact", "shock", "packaging test", "drop height", "material testing"])
def _(S):
    return [
        line(seg(8.5, 2, 8.5, 3.5)),
        line(seg(12, 2, 12, 3.5)),
        shell(rect(6, 6, 9, 8, rr(S, 2))),
        line(seg(2, 21, 22, 21)),
        line(seg(19, 7, 19, 18)),
        line(arrow(19, 11, 19, 7, 1.8)),
        line(arrow(19, 14, 19, 18, 1.8)),
    ]


@icon("abrasion-test", CAT, "Circular rubbing head moving in a loop over a round fabric sample",
      tags=["abrasion", "rub test", "martindale", "wear resistance", "rubbing", "fabric wear", "material testing"])
def _(S):
    return [
        shell(circle(12, 12, 9.5) if S.name == "rounded" else poly(regular(12, 12, 10, 12, 0), closed=True)),
        detail(carrow(12, 12, 5.5, 40, 320, 2)),
        dot(12, 12, 1.4),
    ]


@icon("pilling-test", CAT, "Fabric swatch with small fuzzy balls viewed under a magnifier",
      tags=["pilling", "pills", "fuzz balls", "bobbles", "sweater", "fabric wear", "material testing"])
def _(S):
    return [
        shell(rect(2, 2, 10, 10, rr(S, 2))),
        dot(5.5, 6, 1.0), dot(8.5, 5.5, 0.9), dot(6.5, 9, 0.9),
        shell(circle(16.5, 16.5, 4.5)),
        line(seg(20, 20, 22, 22)),
    ]


@icon("colorfastness-test", CAT, "Fabric swatch above a row of grey scale steps from dark to light",
      tags=["colorfastness", "colour fastness", "color fastness", "fading", "grey scale", "dye test", "material testing"])
def _(S):
    return cloth(S, 3, 3, 18, 10, 2) + [
        solid(rect(3, 16, 5, 5)),
        shell(rect(9.5, 16, 5, 5, 0)),
        dot(12, 18.5, 0.9),
        shell(rect(16, 16, 5, 5, 0)),
    ]


@icon("shrinkage-test", CAT, "Fabric square with arrows pointing inward from all four sides",
      tags=["shrinkage", "shrink", "dimensional change", "washing test", "fabric size", "measure", "material testing"])
def _(S):
    return [
        shell(rect(2, 2, 20, 20, rr(S, 3))),
        detail(arrow(5, 12, 9.5, 12, 2)),
        detail(arrow(19, 12, 14.5, 12, 2)),
        detail(arrow(12, 5, 12, 9.5, 2)),
        detail(arrow(12, 19, 12, 14.5, 2)),
    ]


@icon("dye-penetrant-test", CAT, "Metal part with a spray can revealing a bright crack line",
      tags=["dye penetrant", "crack detection", "ndt", "non destructive testing", "flaw", "inspection", "spray"])
def _(S):
    return [
        shell(rect(2, 13, 11, 8, rr(S, 2))),
        detail(poly([(7, 13), (5.5, 16), (8, 18), (6.5, 21)])),
        shell(rect(16, 9, 5, 12, rr(S, 1.5))),
        line(seg(17.5, 5, 19.5, 5)),
        line(seg(18.5, 5, 18.5, 7)),
        dot(12, 8, 0.9), dot(8.5, 9, 0.9), dot(14.5, 11, 0.8), dot(5.5, 8, 0.8),
    ]


@icon("ultrasonic-flaw-detection", CAT, "Probe on a metal block with sound waves reflecting off a hidden flaw",
      tags=["ultrasonic", "ultrasound test", "flaw detection", "ndt", "non destructive testing", "probe", "sound waves"])
def _(S):
    return [
        shell(rect(9, 2.5, 6, 6, rr(S, 1.5))),
        shell(rect(2, 10, 20, 11, rr(S, 3))),
        detail(arc(12, 10, 4, 50, 130)),
        detail(arc(12, 10, 7.5, 55, 125)) if False else detail(arc(12, 10, 7, 60, 120)),
        dot(17, 17, 1.4),
    ]


@icon("salt-spray-test", CAT, "Test cabinet with a mist nozzle spraying droplets onto hanging samples",
      tags=["salt spray", "salt fog", "corrosion test", "cabinet", "mist", "corrosion resistance", "material testing"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, rr(S, 3))),
        detail(seg(12, 3, 12, 7)),
        Part("dot", drop(7.5, 11.5, 0.5)), Part("dot", drop(16.5, 11.5, 0.5)), Part("dot", drop(12, 12.5, 0.5)),
        detail(seg(7.5, 16, 7.5, 19.5)),
        detail(seg(16.5, 16, 16.5, 19.5)),
    ]


@icon("uv-weathering-test", CAT, "Sample panel under a sun and rain drops",
      tags=["uv test", "weathering", "weather resistance", "ultraviolet", "sun and rain", "ageing", "material testing"])
def _(S):
    return [
        shell(rect(3, 16, 18, 5, rr(S, 2))),
        shell(circle(7.5, 8, 2.5)) if S.name == "line" else shell(circle(7.5, 8, 2.8)),
        line(seg(7.5, 2.5, 7.5, 3.5)), line(seg(2.5, 8, 3.5, 8)), line(seg(11.5, 8, 12.5, 8)),
        line(seg(4, 4.5, 4.8, 5.3)), line(seg(11, 4.5, 10.2, 5.3)),
        line(seg(16, 4, 15, 7)), line(seg(20, 4, 19, 7)), line(seg(18, 9, 17, 12)),
    ]


@icon("metal-grain-structure", CAT, "Circular microscope view showing irregular polygon metal grains",
      tags=["grain structure", "microstructure", "metallography", "crystal grains", "microscope", "alloy", "metal"])
def _(S):
    return [
        shell(circle(12, 12, 9.5) if S.name == "rounded" else poly(regular(12, 12, 10, 10, 0), closed=True)),
        detail(poly([(10, 2.5), (10.5, 9), (15.5, 12), (21.5, 9.5)])),
        detail(poly([(10.5, 9), (2.5, 11.5)])),
        detail(poly([(15.5, 12), (13, 17.5), (12, 21.5)])),
        detail(poly([(13, 17.5), (7.5, 16), (3.5, 17)])),
        detail(poly([(7.5, 16), (6.5, 11)])) if False else detail(poly([(7.5, 16), (5.5, 12.5)])),
    ]


@icon("thermal-conductivity", CAT, "Metal bar with a flame at one end and heat waves fading along its length",
      tags=["thermal conductivity", "heat transfer", "conduction", "heat flow", "metal bar", "thermal", "physics"])
def _(S):
    return [
        shell(flame(5, 12, 0.8)),
        shell(rect(10, 9.5, 12, 5, rr(S, 2))),
        line("M13 7.5q-1.5 -1.5 0 -3t0 -3"),
        line("M17 7.5q-1.5 -1.5 0 -3"),
        line(seg(21, 7.5, 21, 6)),
    ]


@icon("burst-test", CAT, "Fabric clamped in a ring and bulging into a dome with an arrow beneath",
      tags=["burst test", "bursting strength", "mullen", "diaphragm", "pressure test", "dome", "material testing"])
def _(S):
    return [
        shell(rect(2, 12, 6, 5, rr(S, 1.5))),
        shell(rect(16, 12, 6, 5, rr(S, 1.5))),
        line("M8 12C8 3 16 3 16 12"),
        line(arrow(12, 21.5, 12, 15.5)),
    ]


@icon("peel-test", CAT, "Tape strip peeled up from a surface at a right angle",
      tags=["peel", "peel strength", "adhesion", "tape", "adhesive test", "lift", "material testing"])
def _(S):
    return [
        shell(rect(2, 16, 20, 5, rr(S, 2))),
        line("M3 12.5H12Q16 12.5 16 8.5V3"),
        line("M13.5 5.5L16 3L18.5 5.5"),
    ]


@icon("cross-cut-adhesion-test", CAT, "Coated square cut with a lattice of lines and a few flaked squares",
      tags=["cross cut", "cross hatch", "adhesion test", "coating", "paint adhesion", "lattice cut", "material testing"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
        detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15)),
        sq(10.2, 10.2, 3.6, 3.6), sq(16.2, 4.2, 3.6, 3.6),
    ]


@icon("tear-test", CAT, "Fabric square with a ragged tear and arrows pulling the two sides apart",
      tags=["tear", "tear strength", "rip", "split", "elmendorf", "fabric tear", "material testing"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(poly([(3, 12), (7, 10), (10, 13), (13, 11), (15.5, 12)])),
        detail(arrow(17, 8, 17, 5, 1.8)),
        detail(arrow(17, 16, 17, 19, 1.8)),
    ]


@icon("density-test", CAT, "Solid object submerged in a graduated cylinder with the water level marked",
      tags=["density", "displacement", "water displacement", "volume", "specific gravity", "cylinder", "material testing"])
def _(S):
    return [
        shell(rect(7, 3, 10, 18, rr(S, 3))),
        detail(seg(7, 10, 17, 10)),
        dot(12, 16, 2.4),
        line(seg(19.5, 10, 22, 10)),
    ]


# ============================================================================ performance fabrics

SHIELD = "M12 2.5L19.5 5.5V11.5C19.5 16.5 16 19.5 12 21.5C8 19.5 4.5 16.5 4.5 11.5V5.5Z"


def shield(S):
    return shell(poly([(12, 2.5), (19.5, 5.5), (19.5, 11.5), (17, 17), (12, 21.5), (7, 17), (4.5, 11.5), (4.5, 5.5)], closed=True, r=S.r * 2)) \
        if S.name == "line" else shell(SHIELD)


@icon("waterproof-fabric", CAT, "Fabric swatch with water drops falling onto it",
      tags=["waterproof", "water repellent", "rain", "water resistant", "drops", "coated fabric", "weatherproof"])
def _(S):
    return [
        Part("dot", drop(6.5, 7, 0.6)), Part("dot", drop(12, 4.5, 0.6)), Part("dot", drop(17.5, 7, 0.6)),
        shell(rect(3, 13, 18, 8, rr(S, 3))),
        detail(seg(3, 17, 21, 17)),
    ]


@icon("breathable-fabric", CAT, "Fabric layer with wavy vapor lines rising through it",
      tags=["breathable", "vapor", "air permeable", "ventilation", "moisture vapour", "membrane", "sweat"])
def _(S):
    parts = [shell(rect(3, 9, 18, 6, rr(S, 2)))]
    for x in (7, 12, 17):
        parts.append(line(f"M{x} 21q-1.5 -1.5 0 -3"))
        parts.append(line(f"M{x} 6q-1.5 -1.5 0 -2.5"))
        parts.append(dot(x, 12, 0.8))
    return parts


@icon("stretch-fabric", CAT, "Fabric pulled outward by arrows with curved stretched edges",
      tags=["stretch", "elastic", "spandex", "elastane", "stretchy", "flexible fabric", "four way stretch"])
def _(S):
    return [
        shell("M8 5Q12 8.5 16 5V19Q12 15.5 8 19Z") if S.name == "rounded" else shell(poly([(8, 5), (12, 8), (16, 5), (16, 19), (12, 16), (8, 19)], closed=True)),
        line(arrow(5.5, 12, 2.2, 12, 1.8)),
        line(arrow(18.5, 12, 21.8, 12, 1.8)),
    ]


@icon("flame-retardant-fabric", CAT, "Shield with a flame inside, marking fire resistant fabric",
      tags=["flame retardant", "fire resistant", "fireproof", "fr clothing", "heat protection", "safety", "protective"])
def _(S):
    return [
        shield(S),
        Part("dot", flame(12, 11.5, 0.9)),
    ]


@icon("antimicrobial-fabric", CAT, "Shield protecting a small bacterium, marking antibacterial fabric",
      tags=["antimicrobial", "antibacterial", "germ free", "hygienic", "bacteria", "odor control", "clean fabric"])
def _(S):
    return [
        shield(S),
        Part("dot", rect(8.5, 9.5, 7, 4.5, 2.2)),
        detail(seg(12, 8, 12, 6.5)) if False else Part("dot", rect(11.4, 6.5, 1.2, 2.2, 0.5)),
        Part("dot", rect(11.4, 15.3, 1.2, 2.2, 0.5)),
    ]


@icon("uv-protective-fabric", CAT, "Sun rays bouncing off a fabric surface",
      tags=["uv protection", "upf", "sun protective", "sunscreen fabric", "ultraviolet", "sun block", "reflect"])
def _(S):
    return [
        shell(rect(3, 15, 18, 6, rr(S, 2))),
        dot(5, 5, 2.2),
        line(seg(7.5, 7.5, 11.5, 12.5)),
        line(arrow(11.5, 12.5, 18, 5, 2)),
    ]


@icon("windproof-fabric", CAT, "Fabric layer with wind lines hitting it and curving away",
      tags=["windproof", "wind resistant", "windbreaker", "wind block", "outerwear", "breeze", "shell fabric"])
def _(S):
    return [
        shell(rect(14, 3, 5, 18, rr(S, 2))),
        line("M2 6H8Q11 6 11 3"),
        line("M2 12H11"),
        line("M2 18H8Q11 18 11 21"),
    ]


@icon("quick-dry-fabric", CAT, "Fabric swatch with a water drop and speed lines leaving it",
      tags=["quick dry", "fast drying", "dry fit", "sportswear", "evaporate", "athletic fabric", "drying"])
def _(S):
    return cloth(S, 2, 5, 11, 14, 2) + [
        shell(drop(18.5, 8.5, 1.0)),
        line(seg(16, 15, 21.5, 15)),
        line(seg(16, 18.5, 20, 18.5)),
    ]


@icon("moisture-wicking-fabric", CAT, "Fabric layer with drops moving through it along arrows",
      tags=["moisture wicking", "wicking", "sweat", "sweat wicking", "performance fabric", "dry", "sportswear"])
def _(S):
    parts = [shell(rect(3, 10, 18, 4, rr(S, 1.5)))]
    for x in (6, 12, 18):
        parts.append(Part("dot", drop(x, 18.5, 0.5)))
        parts.append(line(arrow(x, 7.5, x, 3, 1.8)))
    return parts


@icon("thermal-insulation-layer", CAT, "Stacked layers turning a heat arrow back at the outer layer",
      tags=["thermal insulation", "insulation", "heat barrier", "warmth", "keeps heat in", "layers", "thermal"])
def _(S):
    return [
        shell(rect(16, 3, 5, 18, rr(S, 2))),
        detail(seg(16, 9, 21, 9)),
        detail(seg(16, 15, 21, 15)),
        line("M2 8H9Q12 8 12 11.5Q12 15 9 15H3"),
        line("M5.5 12.8L3 15L5.5 17.2"),
    ]


@icon("non-slip-surface", CAT, "Sole surface with a row of raised grip teeth",
      tags=["non slip", "anti slip", "grip", "traction", "tread", "slip resistant", "rubber sole"])
def _(S):
    return [
        shell(poly([(2, 21), (2, 15), (5, 11), (8, 15), (11, 11), (14, 15), (17, 11), (20, 15), (22, 15), (22, 21)], closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
        detail(seg(2, 18, 22, 18)),
    ]


@icon("anti-static-material", CAT, "Fabric square with a crossed out spark",
      tags=["anti static", "antistatic", "static free", "esd", "electrostatic", "no static", "conductive fabric"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(poly([(13, 5.5), (8, 12.5), (12, 12.5), (10.5, 18.5), (16, 10.5), (12, 10.5), (13, 5.5)], closed=True)),
        detail(seg(4.5, 19.5, 19.5, 4.5)),
    ]


@icon("shock-absorbing-material", CAT, "Foam pad compressed by a downward arrow with a spring inside",
      tags=["shock absorbing", "cushion", "impact protection", "foam", "padding", "damping", "spring"])
def _(S):
    return [
        line(arrow(12, 2, 12, 9, 2)),
        shell(rect(3, 11, 18, 10, rr(S, 3))),
        detail(poly([(6, 16), (9, 13.5), (12, 18.5), (15, 13.5), (18, 16)])),
    ]


@icon("tear-resistant-fabric", CAT, "Reinforced fabric pulled by opposing arrows with a small cut that stays closed",
      tags=["tear resistant", "ripstop", "reinforced", "strong fabric", "rip stop", "durable", "grid weave"])
def _(S):
    return cloth(S, 6, 4, 12, 16, 2) + [
        sdot(8.8, 7, 1.2, 0.7),
        line(arrow(4.5, 12, 2.6, 12, 1.6)),
        line(arrow(19.5, 12, 21.4, 12, 1.6)),
    ]


# ============================================================================ recycled and composite

@icon("recycled-polyester", CAT, "Plastic bottle shown turning into a folded T-shirt",
      tags=["recycled polyester", "rpet", "plastic bottle", "recycled fabric", "upcycled", "sustainable textile", "bottle to shirt"])
def _(S):
    return [
        shell(poly([(4, 3), (6, 3), (6, 6), (8, 8), (8, 21), (2, 21), (2, 8), (4, 6)], closed=True, r=S.r * 0.6)),
        line(arrow(9.5, 13.5, 13, 13.5, 2)),
        shell(poly([(14, 7), (16.5, 6), (19.5, 6), (22, 7), (22, 10.5), (20.5, 11), (20.5, 18), (15.5, 18), (15.5, 11), (14, 10.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("recycled-rubber-crumb", CAT, "Tyre turning into a small pile of rubber granules",
      tags=["rubber crumb", "recycled rubber", "tire recycling", "granules", "playground surface", "rubber mulch", "tyre"])
def _(S):
    return [
        shell(circle(6.5, 12, 5)),
        dot(6.5, 12, 1.4),
        line(arrow(13, 12, 15.5, 12, 1.6)) if False else line(arrow(12.5, 8, 15.5, 8, 1.6)),
        dot(15.5, 19.5, 1.2), dot(18.8, 19.5, 1.2), dot(22 - 0.6, 19.5, 1.2) if False else dot(21, 19.5, 1.2),
        dot(17, 16.5, 1.2), dot(20, 16.5, 1.2), dot(18.5, 13.5, 1.2),
    ]


@icon("rag-rug", CAT, "Oval rug of braided fabric strips coiled in rings",
      tags=["rag rug", "braided rug", "rug", "carpet", "upcycled textile", "handmade", "oval rug"])
def _(S):
    oval = rect(2, 5, 20, 14, 5.5) if S.name == "line" else ellipse(12, 12, 10, 7)
    inner = rect(6.5, 9, 11, 6, 2.5) if S.name == "line" else ellipse(12, 12, 5.5, 3)
    return [shell(oval), detail(inner)]


@icon("organic-cotton", CAT, "Open cotton boll with a small leaf beside it",
      tags=["organic cotton", "cotton boll", "natural fiber", "eco cotton", "sustainable", "plant fibre", "cotton"])
def _(S):
    puffs = [circle(6, 9.5, 3.4), circle(14, 9.5, 3.4), circle(10, 6, 3.4), circle(10, 10.5, 3.4)]
    calyx = poly([(4.5, 13), (10, 16), (15.5, 13), (14, 19), (10, 21), (6, 19)], closed=True)
    return [
        shell(union(*puffs, calyx)),
        Part("dot", "M18 21C17.5 18 19 16 22 16C22 19 20.5 21 18 21Z"),
    ]


@icon("composite-laminate", CAT, "Slab edge in perspective showing stacked layers with crossing fibres",
      tags=["composite", "laminate", "carbon fiber", "fibreglass", "layers", "plies", "layup"])
def _(S):
    return [
        shell(poly([(2, 8), (12, 4), (22, 8), (22, 16), (12, 20), (2, 16)], closed=True, r=S.r * 0.5)),
        detail(poly([(2, 8), (12, 12), (22, 8)])),
        detail(seg(12, 12, 12, 20)) if False else detail(poly([(2, 12), (12, 16), (22, 12)])),
    ]


@icon("cane-webbing", CAT, "Square panel of woven cane strands forming an open octagon lattice",
      tags=["cane webbing", "rattan", "wicker", "woven cane", "chair seat", "lattice", "caning"])
def _(S):
    return [
        shell(rect(2, 2, 20, 20, rr(S, 3))),
        detail(seg(8, 2, 8, 22)), detail(seg(16, 2, 16, 22)),
        detail(seg(2, 8, 22, 8)), detail(seg(2, 16, 22, 16)),
        detail(seg(8, 8, 16, 16)), detail(seg(16, 8, 8, 16)),
    ]
