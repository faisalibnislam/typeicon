"""TypeIcon Core: biochem (batch biochem_003).

Lab apparatus, assays and molecular machinery drawn as simple symbols of the objects themselves.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "biochem"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12, cy=12):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def mk(S, x, y, r=1.25):
    """Small mark: square in Line, round in Rounded."""
    if S.name == "rounded":
        return dot(x, y, r)
    return Part("dot", rect(x - r, y - r, 2 * r, 2 * r))


def ah(tip, deg, S, size=2.0):
    """Open arrowhead at tip pointing along deg."""
    a = polar(tip[0], tip[1], size * 1.414, deg + 135)
    b = polar(tip[0], tip[1], size * 1.414, deg - 135)
    return line(poly([a, tip, b], r=L(S, 0, 0.6)))


def wave(x0, x1, y, amp, n):
    w = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        sgn = -1 if i % 2 == 0 else 1
        d += f"Q{fmt(x0 + w * (i + 0.5))} {fmt(y + sgn * 2 * amp)} {fmt(x0 + w * (i + 1))} {fmt(y)}"
    return d


# ============================================================================ lab tools, chunk 1

@icon("gel-comb", CAT, "A flat bar with a row of evenly spaced teeth used to form wells in a gel.",
      tags=["electrophoresis", "wells", "gel", "comb", "lab tool", "molecular biology", "dna"])
def _(S):
    body = union(rect(3, 3, 18, 6, L(S, 0, 2)), rect(3.5, 8, 3, 11, L(S, 0, 1.5)),
                 rect(10.5, 8, 3, 11, L(S, 0, 1.5)), rect(17.5, 8, 3, 11, L(S, 0, 1.5)))
    return [shell(body)]


@icon("uv-transilluminator", CAT, "A light box with a gel slab on top showing bright bands under UV rays.",
      tags=["uv", "gel", "bands", "electrophoresis", "light box", "dna", "imaging"])
def _(S):
    return [shell(rect(3, 15, 18, 6, S.R)),
            shell(rect(6, 10, 12, 3, min(S.R, 1.5))),
            line(seg(7, 6, 7, 3)), line(seg(12, 6, 12, 2)), line(seg(17, 6, 17, 3))]


@icon("centrifuge-pellet", CAT, "A conical tube with a small solid pellet at the tip and a curved spin arrow.",
      tags=["centrifuge", "pellet", "spin", "tube", "separation", "lab", "sediment"])
def _(S):
    body = poly([(3, 3), (11, 3), (11, 9), (8.5, 20), (5.5, 20), (3, 9)], closed=True, r=S.r)
    return [shell(body), detail(seg(3, 7, 11, 7)),
            solid(poly([(5.6, 16.2), (8.4, 16.2), (8.2, 18), (5.8, 18)], closed=True)),
            line(arc(17, 12, 4, -70, 150)), ah(polar(17, 12, 4, 150), 240, S, 1.8)]


@icon("electroporation", CAT, "A round cell with pores opening in its membrane beside a lightning bolt.",
      tags=["electric pulse", "cell", "membrane", "pores", "transfection", "dna delivery", "lab"])
def _(S):
    return [line(arc(8.5, 13, 6.5, 25, 155)), line(arc(8.5, 13, 6.5, 205, 335)),
            mk(S, 8.5, 13, 1.5),
            line(poly([(19, 2.5), (15.5, 9), (20, 9), (16.5, 16)], r=S.r))]


@icon("microfluidic-chip", CAT, "A small rectangular chip with a winding channel between round inlet and outlet ports.",
      tags=["lab on a chip", "channel", "microfluidics", "inlet", "outlet", "device", "lab"])
def _(S):
    return [shell(rect(2.5, 5, 19, 14, min(S.R, 3))),
            detail(poly([(7, 12), (9, 12), (10.5, 9), (13.5, 15), (15, 12), (17, 12)], r=S.r)),
            mk(S, 6, 12, 1.3), mk(S, 18, 12, 1.3)]


@icon("bioprinter", CAT, "A printer nozzle depositing a row of small cell dots onto a plate.",
      tags=["3d bioprinting", "nozzle", "tissue engineering", "cells", "print", "lab", "additive"])
def _(S):
    nozzle = poly([(8, 2), (16, 2), (16, 7), (13, 11), (11, 11), (8, 7)], closed=True, r=S.r)
    return [shell(nozzle), detail(seg(8, 5, 16, 5)),
            mk(S, 8, 15, 1.3), mk(S, 12, 15, 1.3), mk(S, 16, 15, 1.3),
            line(seg(3, 20, 21, 20))]


@icon("microscope-objective", CAT, "A stepped microscope lens barrel tapering to a small tip over a drop of oil.",
      tags=["objective lens", "microscope", "optics", "magnification", "oil immersion", "lab"])
def _(S):
    body = poly([(7, 2), (17, 2), (17, 7), (15, 7), (15, 12), (13, 17), (11, 17), (9, 12), (9, 7), (7, 7)],
                closed=True, r=S.r)
    return [shell(body), detail(seg(7, 4.5, 17, 4.5)), mk(S, 12, 20.5, 1.2)]


@icon("tissue-cassette", CAT, "A flat plastic box with a slanted writing edge and slots in its lid.",
      tags=["histology", "pathology", "biopsy", "embedding", "cassette", "tissue", "lab"])
def _(S):
    body = poly([(3, 20), (3, 10), (6, 5), (21, 5), (21, 20)], closed=True, r=S.r)
    return [shell(body), detail(seg(3, 10, 21, 10)),
            detail(seg(9, 13, 9, 17)), detail(seg(13.5, 13, 13.5, 17)), detail(seg(18, 13, 18, 17))]


@icon("durham-tube", CAT, "A test tube of broth with a small inverted tube inside holding a trapped gas bubble.",
      tags=["gas production", "fermentation", "broth", "test tube", "microbiology", "bubble", "lab"])
def _(S):
    tube = union("M6 3V15a6 6 0 0 0 12 0V3Z", rect(4, 2, 16, 3, L(S, 0, 1.5)))
    inner = "M10 16V11a2 2 0 0 1 4 0V16"
    return [shell(tube), detail(inner)]


@icon("loop-sterilizer", CAT, "A short heater with an inoculation loop held in its glowing opening.",
      tags=["inoculation loop", "sterilize", "flame", "heater", "microbiology", "aseptic", "lab"])
def _(S):
    return [shell(rect(4, 13, 13, 8, S.R)), detail(seg(8, 17, 13, 17)),
            line(circle(10.5, 8, 2.5)), line(seg(12.4, 6.3, 21, 2))]


@icon("lab-mouse-cage", CAT, "A box cage with a wire lid and a small mouse inside.",
      tags=["mouse", "cage", "animal facility", "rodent", "research", "vivarium", "lab"])
def _(S):
    return [shell(rect(3, 5, 18, 16, S.R)), detail(seg(3, 10, 21, 10)),
            detail(seg(9, 5, 9, 10)), detail(seg(15, 5, 15, 10)),
            solid(ellipse(10.5, 16.8, 4, 2.4)), solid(circle(15.2, 15.8, 1.8)),
            line(poly([(6.5, 17), (5, 15.5)], r=0))]


@icon("fly-vial", CAT, "A narrow vial with a foam plug on top, a food layer at the bottom and two small flies.",
      tags=["drosophila", "fruit fly", "vial", "genetics", "foam plug", "lab", "insect"])
def _(S):
    body = union(rect(7, 2, 10, 5, L(S, 0.5, 2)), rect(8, 6, 8, 11, 0), f"M8 15V17a4 4 0 0 0 8 0V15Z")
    return [shell(body), detail(seg(8, 17, 16, 17)), mk(S, 10.8, 11.8, 1.0), mk(S, 13.6, 10.2, 1.0)]


# ============================================================================ lab tools, chunk 2

@icon("cryo-electron-grid", CAT, "A tiny round disc covered by a fine square mesh of grid lines.",
      tags=["cryo-em", "grid", "electron microscopy", "tweezers", "sample prep", "mesh", "lab"])
def _(S):
    a, b = L(S, 4, 6.5), L(S, 20, 17.5)
    return [shell(circle(12, 12, 9)), detail(seg(9.2, a, 9.2, b)), detail(seg(14.8, a, 14.8, b)),
            detail(seg(a, 9.2, b, 9.2)), detail(seg(a, 14.8, b, 14.8))]


@icon("pycnometer", CAT, "A small pear-shaped glass bottle with a ground stopper that has a thin capillary hole.",
      tags=["density", "specific gravity", "flask", "stopper", "glassware", "measurement", "lab"])
def _(S):
    body = union(circle(12, 15.5, 6), rect(10, 7, 4, 8, 0))
    return [shell(body), shell(rect(8.5, 2, 7, 4, L(S, 0, 1.5))), detail(seg(12, 2, 12, 6)),
            detail(seg(6.3, 15.5, 17.7, 15.5))]


@icon("thiele-tube", CAT, "A glass tube with a looped side arm holding a thermometer and a small capillary sample.",
      tags=["melting point", "oil bath", "thermometer", "glassware", "heating", "lab", "side arm"])
def _(S):
    return [line(rect(3.5, 10, 17, 11, S.R)), line(seg(8, 10, 8, 2.5)), line(seg(16, 10, 16, 2.5)),
            line(seg(12, 2, 12, 14)), mk(S, 12, 15.5, 1.6)]


@icon("melting-point-apparatus", CAT, "A compact heater box with a viewing lens and three capillary tubes in its slot.",
      tags=["melting point", "capillary", "heating block", "chemistry", "instrument", "lab", "sample"])
def _(S):
    return [shell(rect(3, 10, 18, 11, S.R)), detail(circle(8.5, 15.5, 2.2)),
            line(seg(12, 3, 12, 10)), line(seg(15.7, 3, 15.7, 10)), line(seg(19.4, 3, 19.4, 10))]


@icon("microbial-air-sampler", CAT, "A perforated sampler head held above an open agar dish.",
      tags=["air quality", "agar plate", "contamination", "cleanroom", "monitoring", "microbiology", "lab"])
def _(S):
    return [shell(rect(4, 2.5, 16, 7, S.R)), shell(rect(10, 9, 4, 4, 0)), shell(rect(3.5, 15, 17, 6, S.R)),
            mk(S, 8, 6, 1.1), mk(S, 12, 6, 1.1), mk(S, 16, 6, 1.1), detail(seg(7, 18, 17, 18))]


@icon("water-sample-bottle", CAT, "A sterile wide-mouth bottle with a cap and label held under a dripping tap.",
      tags=["water testing", "sampling", "environmental", "tap", "bottle", "sterile", "lab"])
def _(S):
    body = union(rect(9, 10, 6, 3, 0), rect(5, 12.5, 14, 9, S.R))
    return [shell(body), detail(seg(5, 17.5, 19, 17.5)),
            line(poly([(3, 3), (12, 3), (12, 5)], r=S.r)), mk(S, 12, 7.8, 1.2)]


@icon("roller-bottle", CAT, "A long cylindrical culture bottle lying on its side across two rollers.",
      tags=["cell culture", "bottle", "rolling", "bioreactor", "culture vessel", "biotech", "lab"])
def _(S):
    body = union(rect(2.5, 3, 15, 11, L(S, 2, 4.5)), rect(17, 6, 4.5, 5, 0))
    return [shell(body), detail(seg(14, 3, 14, 14)),
            shell(circle(7, 18.5, 2)), shell(circle(14.5, 18.5, 2))]


@icon("square-archaeon", CAT, "A flat square cell with thin walls and a few small gas vesicles inside.",
      tags=["haloquadratum", "archaea", "microbe", "square cell", "gas vesicle", "extremophile", "microbiology"])
def _(S):
    return [shell(rect(3, 3, 18, 18, L(S, 1, 3.5))),
            Part("dot", ellipse(9, 9.5, 2.2, 1.4)), Part("dot", ellipse(15.5, 12, 2.2, 1.4)),
            Part("dot", ellipse(9.5, 15.5, 2.2, 1.4))]


@icon("myxobacteria-fruiting-body", CAT, "A short branching stalk topped by round spore clusters like a tiny tree of balls.",
      tags=["myxococcus", "spores", "fruiting body", "stalk", "bacteria", "development", "microbiology"])
def _(S):
    def ball(x, y):
        return shell(rect(x - 2.6, y - 2.6, 5.2, 5.2, L(S, 1.5, 2.6)))
    return [line(seg(12, 21.5, 12, 11)), line(poly([(12, 17), (7, 14)], r=0)), line(poly([(12, 17), (17, 14)], r=0)),
            ball(12, 5.5), ball(5, 11), ball(19, 11)]


@icon("phage-plaque-assay", CAT, "A round dish seen from above with a dotted bacterial lawn and clear round holes.",
      tags=["bacteriophage", "plaque", "petri dish", "lawn", "virus", "titer", "microbiology"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(circle(9, 9, 2.2)), detail(circle(15.5, 13.5, 2.2)),
            mk(S, 14, 7, 1), mk(S, 7.5, 15, 1), mk(S, 11.5, 17.5, 1)]


@icon("bacterial-transformation", CAT, "A rod bacterium with a small DNA ring outside it and a curved arrow into the cell.",
      tags=["plasmid", "dna uptake", "competent cells", "genetic engineering", "bacteria", "cloning", "microbiology"])
def _(S):
    return [shell(rect(6, 12, 15, 9, L(S, 3, 4.5))), mk(S, 13.5, 16.5, 1.3),
            line(circle(6, 6, 3)), line("M10 5.5Q15 5.5 15.5 9.5"), ah((15.5, 10.2), 90, S, 1.8)]


@icon("spore-germination", CAT, "An oval spore split open at one end with a thin branching thread growing out of it.",
      tags=["germination", "hypha", "spore", "fungus", "growth", "sprout", "microbiology"])
def _(S):
    return [line(arc(8.5, 15.5, 5.5, -20, 290)),
            line("M12.4 11.6Q16 10 16.5 6.5Q17 4 20 3.5"), line("M16.5 7.5L21 9.5")]


# ============================================================================ cell machinery and assays

@icon("nuclear-pore", CAT, "A round ring with eight evenly spaced spokes around a central opening.",
      tags=["nucleus", "nuclear envelope", "transport", "pore complex", "cell biology", "import export", "organelle"])
def _(S):
    ring = minus(circle(12, 12, 9.5), circle(12, 12, 3.2))
    sp = [detail(f"M{fmt(polar(12, 12, 4.8, a)[0])} {fmt(polar(12, 12, 4.8, a)[1])}L{fmt(polar(12, 12, 8.4, a)[0])} {fmt(polar(12, 12, 8.4, a)[1])}")
          for a in range(0, 360, 45)]
    return [shell(ring)] + sp


@icon("proteasome", CAT, "A short barrel of stacked rings with a cap on each end and a thin chain entering the top.",
      tags=["protein degradation", "ubiquitin", "barrel", "enzyme complex", "cell biology", "recycling", "protein"])
def _(S):
    return [shell(rect(7, 8, 10, 11, L(S, 1, 2))), detail(seg(7, 11.7, 17, 11.7)), detail(seg(7, 15.3, 17, 15.3)),
            line(seg(5, 6, 19, 6)), line(seg(5, 21, 19, 21)),
            line("M12 1.5Q14 2.5 12 4Q10 5.5 12 7")]


@icon("atp-synthase", CAT, "A rotor block with a stalk rising to a lobed knob head and a curved rotation arrow.",
      tags=["atp", "enzyme", "mitochondria", "energy", "rotor", "proton pump", "molecular machine"])
def _(S):
    head = union(circle(12, 5, 2.6), circle(9.3, 8, 2.6), circle(14.7, 8, 2.6), rect(10.5, 8, 3, 7, 0))
    return [shell(union(head, rect(5, 14, 14, 6, L(S, 1, 3)))),
            line(arc(12, 17, 7.5, 200, 340)), ah(polar(12, 17, 7.5, 340), 70, S, 1.6)]


@icon("krebs-cycle", CAT, "A circle of curved arrows with a molecule dot at each step and a short arrow feeding in at the top.",
      tags=["citric acid cycle", "tca cycle", "metabolism", "respiration", "biochemistry", "cycle", "mitochondria"])
def _(S):
    cx, cy, r = 12, 14, 6.5
    parts = [line(seg(12, 1.5, 12, 5)), ah((12, 5.2), 90, S, 1.6)]
    for k in range(4):
        a0 = k * 90 - 90
        parts.append(line(arc(cx, cy, r, a0 + 26, a0 + 62)))
        parts.append(ah(polar(cx, cy, r, a0 + 66), a0 + 66 + 90, S, 1.5))
        x, y = polar(cx, cy, r, a0)
        parts.append(mk(S, x, y, 1.6))
    return parts


@icon("cellular-respiration", CAT, "A bean-shaped mitochondrion below a hexagon sugar and a lightning bolt of energy.",
      tags=["mitochondria", "glucose", "atp", "energy", "metabolism", "oxygen", "biology"])
def _(S):
    return [shell(rect(3, 11, 18, 10, 5)),
            detail(poly([(7, 16), (9, 13.5), (12, 18.5), (15, 13.5), (17, 16)], r=S.r)),
            line(poly(regular(6.5, 5.2, 3.2, 6, 0), closed=True, r=S.r)),
            line(poly([(18.5, 2), (15.5, 6), (18.5, 6), (16, 9.5)], r=S.r))]


@icon("oxytocin-molecule", CAT, "A ring of six linked beads with a bridge across it and a short tail of three beads.",
      tags=["hormone", "peptide", "love hormone", "bonding", "molecule", "neuropeptide", "biochemistry"])
def _(S):
    c = (9, 9)
    v = [polar(c[0], c[1], 6, -90 + 60 * i) for i in range(6)]
    parts = [line(poly(v, closed=True, r=S.r)), detail(seg(v[1][0], v[1][1], v[5][0], v[5][1]))]
    parts += [mk(S, x, y, 1.6) for x, y in v]
    parts.append(line(poly([v[3], (14, 18), (19.5, 20)], r=S.r)))
    parts += [mk(S, 14, 18, 1.6), mk(S, 19.5, 20, 1.6)]
    return parts


@icon("reagent-reservoir", CAT, "A long shallow trough with a sloped bottom and a wavy liquid surface.",
      tags=["multichannel pipette", "trough", "liquid handling", "reagent", "basin", "pipetting", "lab"])
def _(S):
    body = poly([(2.5, 5), (21.5, 5), (21.5, 19), (18, 19), (2.5, 12)], closed=True, r=S.r)
    return [shell(body), detail(wave(5.5, 19, 10, 1, 3))]


@icon("microplate-reader", CAT, "A boxy benchtop instrument with a small display and a drawer holding a well plate.",
      tags=["plate reader", "elisa", "absorbance", "assay", "spectrophotometer", "instrument", "lab"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 9, S.R)), solid(rect(5, 5.5, 6, 3, 0)), mk(S, 16, 7, 1.2), mk(S, 19, 7, 1.2),
            shell(rect(4.5, 14, 15, 7.5, S.R)),
            mk(S, 8.5, 17.7, 1.1), mk(S, 12, 17.7, 1.1), mk(S, 15.5, 17.7, 1.1)]


@icon("amplification-curve", CAT, "Two S-shaped curves rising from a flat baseline and crossing a dashed threshold line.",
      tags=["qpcr", "real-time pcr", "ct value", "threshold", "dna", "fluorescence", "graph"])
def _(S):
    return [line(poly([(3, 2.5), (3, 21), (21.5, 21)], r=S.r)),
            line("M5 19H6C9.5 19 9 4.5 13 4.5H21"), line("M10 19H12C15.5 19 15 9.5 19 9.5H21"),
            line(seg(5.5, 14.5, 8, 14.5)), line(seg(10.5, 14.5, 13, 14.5)), line(seg(15.5, 14.5, 18, 14.5))]


@icon("aseptic-technique", CAT, "A tilted open test tube with its mouth over a small flame and a cap held aside.",
      tags=["flaming", "sterile technique", "bunsen", "test tube", "microbiology", "contamination", "lab"])
def _(S):
    tube = rot("M5 9H17a3 3 0 0 1 0 6H5", -35, 16.5, 7.5)
    flame = "M5 22C2 22 1.5 19 5 16C8.5 19 8 22 5 22Z"
    return [line(tube), shell(flame), shell(rect(2.5, 2.5, 5, 4, L(S, 0.5, 1.8)))]


@icon("dialysis-tubing", CAT, "A clipped membrane bag hanging in a beaker of liquid with small dots passing out.",
      tags=["dialysis", "semipermeable", "membrane", "diffusion", "beaker", "osmosis", "lab"])
def _(S):
    beaker = f"M3 4V19a2 2 0 0 0 2 2H19a2 2 0 0 0 2-2V4"
    return [line(beaker), shell(rect(9.5, 8.5, 5, 9, L(S, 1.5, 2.5))), line(seg(12, 2, 12, 8)),
            line(seg(8.5, 8.5, 15.5, 8.5)), mk(S, 5.8, 13, 1.1), mk(S, 18.2, 15.5, 1.1), mk(S, 18.2, 10.5, 1.1)]
