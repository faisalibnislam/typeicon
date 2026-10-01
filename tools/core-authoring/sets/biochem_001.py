"""TypeIcon Core: biochem (batch biochem_001).

Microbes, viruses, protists, algae, fungi and cell structures drawn as simple symbols of the organisms
and organelles themselves. Rods are capsules, cells are circles and blobs, hairs and tails are open strokes.
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


def grow(d, g):
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def thick(d, w, S):
    """Outline of a stroke of width w along d (tubes, curved rods)."""
    return path_to_d(ST(d, w, S.cap, S.join))


def tube(d, w):
    """Outline of a round-ended stroke of width w along d."""
    return path_to_d(ST(d, w, "round", "round"))


def rot(d, deg, cx=12, cy=12):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def mk(S, x, y, r=1.25):
    """Small mark: square in Line, round in Rounded."""
    if S.name == "rounded":
        return dot(x, y, r)
    return Part("dot", rect(x - r, y - r, 2 * r, 2 * r))


def rod(cx, cy, length, width, deg, S, full=None):
    """Rod-shaped cell (capsule). Line has small corner radii, Rounded is fully round-ended."""
    rx = full if full is not None else L(S, min(2, width / 2), width / 2)
    d = rect(cx - length / 2, cy - width / 2, length, width, rx)
    return rot(d, deg, cx, cy) if deg else d


def pt_on(cx, cy, r, deg):
    return polar(cx, cy, r, deg)


def wave(x0, x1, y, amp, n):
    """Horizontal wave from x0 to x1 made of n half-waves; starts upward."""
    w = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        sgn = -1 if i % 2 == 0 else 1
        d += f"Q{fmt(x0 + w * (i + 0.5))} {fmt(y + sgn * 2 * amp)} {fmt(x0 + w * (i + 1))} {fmt(y)}"
    return d


def vwave(x, y0, y1, amp, n):
    """Vertical wave from y0 to y1 (n half-waves); starts to the left."""
    h = (y1 - y0) / n
    d = f"M{fmt(x)} {fmt(y0)}"
    for i in range(n):
        sgn = -1 if i % 2 == 0 else 1
        d += f"Q{fmt(x + sgn * 2 * amp)} {fmt(y0 + h * (i + 0.5))} {fmt(x)} {fmt(y0 + h * (i + 1))}"
    return d


def frame(origin, deg):
    """Local frame: x runs along `deg` (0 = right, 90 = down) from `origin`."""
    ox, oy = origin
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return lambda x, y=0.0: (ox + x * c - y * sn, oy + x * sn + y * c)


def _q(p):
    return f"{fmt(p[0])} {fmt(p[1])}"


def fwave(f, x0, x1, amp, n, y=0.0):
    """Wavy open path in frame f from local x0 to x1 (n half-waves, starts towards +y... alternating)."""
    w = (x1 - x0) / n
    d = "M" + _q(f(x0, y))
    for i in range(n):
        sgn = 1 if i % 2 == 0 else -1
        d += "Q" + _q(f(x0 + w * (i + 0.5), y + sgn * 2 * amp)) + " " + _q(f(x0 + w * (i + 1), y))
    return d


def fseg(f, x0, y0, x1, y1):
    return "M" + _q(f(x0, y0)) + "L" + _q(f(x1, y1))


def fpoly(f, pts, closed=False, r=0.0):
    return poly([f(x, y) for x, y in pts], closed=closed, r=r)


def ah(tip, deg, S, size=2.0):
    """Open arrowhead at tip pointing along deg."""
    a = polar(tip[0], tip[1], size * 1.414, deg + 135)
    b = polar(tip[0], tip[1], size * 1.414, deg - 135)
    return line(poly([a, tip, b], r=L(S, 0, 0.6)))


# ============================================================================ bacteria

@icon("diplococcus", CAT, "Two round cells joined side by side as a pair.",
      tags=["bacteria", "cocci", "pair", "microbiology", "coffee bean", "pneumococcus", "microbe"])
def _(S):
    body = union(circle(7.5, 12, 5.5), circle(16.5, 12, 5.5))
    return [shell(body), detail(seg(12, 9.2, 12, 14.8)), mk(S, 7.5, 12, 1.2), mk(S, 16.5, 12, 1.2)]


@icon("tetrad-cocci", CAT, "Four round cells packed in a flat square of two by two.",
      tags=["bacteria", "cocci", "tetrad", "microbiology", "micrococcus", "cell packet", "microbe"])
def _(S):
    cs = [(7.5, 7.5), (16.5, 7.5), (7.5, 16.5), (16.5, 16.5)]
    body = union(*[circle(x, y, 5) for x, y in cs])
    return [shell(body)] + [mk(S, x, y, 1.2) for x, y in cs]


@icon("streptobacillus", CAT, "A short chain of three rod-shaped cells joined end to end.",
      tags=["bacteria", "bacilli", "chain", "rods", "microbiology", "strepto", "microbe"])
def _(S):
    cs = [(6, 0), (0, 0), (-6, 0)]
    parts = [rod(12 + dx, 12 + dy, 8.5, 6, 0, S) for dx, dy in cs]
    body = rot(union(*parts), -30)
    f = frame((12, 12), -30)
    return [shell(body)] + [detail(fseg(f, 3 * k, -2.6, 3 * k, 2.6)) for k in (-1, 1)]


@icon("vibrio-bacterium", CAT, "A comma-shaped curved rod with one long wavy tail.",
      tags=["bacteria", "vibrio", "comma", "flagellum", "cholera", "microbiology", "microbe"])
def _(S):
    body = tube(arc(13, 9.5, 6, 100, 250), 5.5)
    f = frame((14.2, 17.2), 4)
    return [shell(body), line(fwave(f, 0, 8, 1.3, 4)), mk(S, 9, 9.5, 1.0)]


@icon("peritrichous-bacterium", CAT, "A rod-shaped cell with many short wavy tails sprouting all around it.",
      tags=["bacteria", "flagella", "peritrichous", "rod", "motile", "salmonella", "microbiology"])
def _(S):
    parts = [shell(rod(12, 12, 11, 7, 0, S))]
    for x, deg in ((8, -112), (12, -90), (16, -68), (8, 112), (12, 90), (16, 68)):
        y0 = 8.0 if deg < 0 else 16.0
        parts.append(line(fwave(frame((x, y0), deg), 0, 6, 0.9, 2)))
    parts.append(line(fwave(frame((6.2, 12), 180), 0, 3.5, 0.8, 2)))
    parts.append(line(fwave(frame((17.8, 12), 0), 0, 3.5, 0.8, 2)))
    return parts


@icon("bacterial-endospore", CAT, "A rod-shaped cell with a bold oval spore inside at one end.",
      tags=["bacteria", "endospore", "spore", "dormant", "bacillus", "clostridium", "microbiology"])
def _(S):
    f = frame((12, 12), -30)
    cx, cy = f(4.5, 0)
    spore = rot(ellipse(cx, cy, 3.3, 2.4), -30, cx, cy)
    return [shell(rod(12, 12, 18, 9.5, -30, S)), Part("dot", spore)]


@icon("bacterial-capsule", CAT, "A rod-shaped cell surrounded by a thick soft outer halo.",
      tags=["bacteria", "capsule", "slime layer", "glycocalyx", "virulence", "microbiology", "coat"])
def _(S):
    return [shell(rod(12, 12, 17.5, 12.5, -28, S, full=L(S, 4, 6.25))),
            detail(rod(12, 12, 9, 4.5, -28, S))]


@icon("prokaryotic-cell", CAT, "A capsule-shaped cell with a DNA squiggle, small dots and a tail at one end.",
      tags=["bacteria", "prokaryote", "cell", "nucleoid", "ribosomes", "flagellum", "cell biology"])
def _(S):
    return [shell(rect(2, 5.5, 15, 13, L(S, 3, 6.5))),
            line("M17 12q1.5-2.5 2.75 0t2.75 0"),
            detail("M5.2 12q1.4-3.2 2.8 0t2.8 0"),
            mk(S, 13.2, 9.3, 1.0), mk(S, 13.2, 14.7, 1.0)]


@icon("biofilm", CAT, "A wavy mound of tiny rod cells growing on a flat surface.",
      tags=["bacteria", "slime", "microbes", "surface", "plaque", "colony", "microbiology"])
def _(S):
    mound = "M2.5 19Q2.5 11.5 7 11.5Q7.5 6.5 12 6.5Q16.5 6.5 17 11.5Q21.5 11.5 21.5 19Z"
    return [shell(mound),
            detail(seg(7.5, 16, 10, 14.5)),
            detail(seg(13.5, 14.2, 16.3, 16)),
            mk(S, 12, 10, 1.1), mk(S, 12, 16.3, 1.1)]


@icon("bacterial-colony", CAT, "A round colony seen from above with a scalloped edge and a raised center.",
      tags=["bacteria", "colony", "petri dish", "agar", "culture", "microbiology", "growth"])
def _(S):
    n = L(S, 8, 9)
    cs = [polar(12, 12, 6.2, -90 + 360 * i / n) for i in range(n)]
    body = union(circle(12, 12, 5), *[circle(x, y, 3.2) for x, y in cs])
    return [shell(body), detail(circle(12, 12, 3.2))]


@icon("magnetotactic-bacterium", CAT, "A curved rod cell with a line of small magnet crystals along its length.",
      tags=["bacteria", "magnetosome", "magnet", "compass", "iron", "navigation", "microbiology"])
def _(S):
    body = tube(arc(12, 22, 10.5, 230, 310), 8)
    parts = [shell(body)]
    for a in (240, 260, 280, 300):
        x, y = polar(12, 22, 10.5, a)
        parts.append(Part("dot", rect(x - 1.1, y - 1.1, 2.2, 2.2, L(S, 0, 1.1))))
    return parts


@icon("bacterial-flagellar-motor", CAT, "A spinning rod through a cell membrane carrying a whip-like filament.",
      tags=["bacteria", "flagellum", "rotary motor", "membrane", "filament", "motility", "molecular machine"])
def _(S):
    return [line(vwave(12, 2, 8, 1.2, 3)),
            line(seg(12, 8, 12, 20.5)),
            line(seg(2, 12, 8, 12)), line(seg(16, 12, 22, 12)),
            line(seg(2, 16, 8, 16)), line(seg(16, 16, 22, 16)),
            line(poly([(6.5, 17.5), (6.5, 21), (17.5, 21), (17.5, 17.5)], r=S.r))]


@icon("gut-microbiome", CAT, "A coiled intestine tube with small bacteria dots between its loops.",
      tags=["intestine", "gut flora", "bacteria", "digestive", "probiotic", "microbiota", "health"])
def _(S):
    return [line("M4 5H16.5A3.5 3.5 0 0 1 16.5 12H7.5A3.5 3.5 0 0 0 7.5 19H20"),
            mk(S, 8.5, 8.5, 1.2), mk(S, 12.5, 8.5, 1.2), mk(S, 16.5, 15.5, 1.2), mk(S, 12.5, 15.5, 1.2)]


@icon("caulobacter", CAT, "A curved cell on a thin stalk that ends in a small holdfast foot.",
      tags=["bacteria", "stalk", "holdfast", "crescent", "aquatic", "attachment", "microbiology"])
def _(S):
    body = tube(arc(13.5, 9, 5, 100, 260), 4.5)
    return [shell(body), line("M12.6 16.5q-1.5 1.8 0 3.6"), line(seg(8.5, 21, 16.5, 21))]


@icon("quorum-sensing", CAT, "Three small rod cells in a ring trading signal dots between them.",
      tags=["bacteria", "signalling", "communication", "autoinducer", "biofilm", "cell to cell", "microbiology"])
def _(S):
    parts = []
    for a in (-90, 30, 150):
        x, y = polar(12, 12, 7.2, a)
        parts.append(shell(rod(x, y, 8, 4.8, a + 90, S)))
    for a in (-30, 90, 210):
        x, y = polar(12, 12, 6.0, a)
        parts.append(mk(S, x, y, 1.2))
    return parts


@icon("stromatolite", CAT, "Layered dome-shaped mineral mounds standing in shallow wavy water.",
      tags=["microbial mats", "fossil", "cyanobacteria", "layered rock", "geology", "ancient life", "dome"])
def _(S):
    big = "M2.5 17.5A6.5 10 0 0 1 15.5 17.5Z"
    small = "M14 17.5A4 6.5 0 0 1 22 17.5Z"
    return [shell(union(big, small)), detail("M5.5 17.5A3.5 5.5 0 0 1 12.5 17.5"),
            line("M2 21.5q2.5-1.5 5 0t5 0t5 0t5 0")]


@icon("winogradsky-column", CAT, "A tall capped glass column with layers of mud and water in bands.",
      tags=["microbial ecology", "sediment", "layers", "science experiment", "mud column", "bacteria", "jar"])
def _(S):
    return [shell(rect(7, 6, 10, 15.5, L(S, 1.5, 3.5))),
            line(seg(6, 3.2, 18, 3.2)),
            detail("M7 10q1.67-1.5 3.33 0t3.33 0t3.34 0"),
            detail(seg(7, 14, 17, 14)),
            detail("M7 18q1.67 1.5 3.33 0t3.33 0t3.34 0")]


@icon("bioremediation", CAT, "An oil droplet nibbled by tiny rod cells beside a young green sprout.",
      tags=["oil spill", "cleanup", "bacteria", "pollution", "environment", "biodegradation", "sprout"])
def _(S):
    drop = "M7.5 3.5C9 6.5 13 8.5 13 14A5.5 5.5 0 0 1 2 14C2 8.5 6 6.5 7.5 3.5Z"
    parts = [shell(drop), detail("M4.8 14a2.8 2.8 0 0 0 2.8 2.8")]
    for a in (-35, 5, 45):
        x, y = polar(7.5, 14, 8.2, a)
        f = frame((x, y), a + 90)
        parts.append(line(fseg(f, -1.4, 0, 1.4, 0)))
    parts.append(line(seg(19.5, 21, 19.5, 14)))
    parts.append(shell("M19.5 16Q19.5 11.5 22.6 11Q22.8 15.8 19.5 16Z"))
    return parts


# ============================================================================ viruses

@icon("icosahedral-virus", CAT, "A faceted hexagonal virus shell with short knobbed fibers at its corners.",
      tags=["virus", "capsid", "adenovirus", "polyhedral", "pathogen", "virology", "microbe"])
def _(S):
    hexv = regular(12, 12, 5.8, 6)
    parts = [shell(poly(hexv, closed=True, r=S.r)),
             detail(poly([hexv[0], hexv[2], hexv[4]], closed=True))]
    for i, a in enumerate(range(-90, 270, 60)):
        p0 = polar(12, 12, 5.8, a)
        p1 = polar(12, 12, 8.4, a)
        parts.append(line(seg(p0[0], p0[1], p1[0], p1[1])))
        kx, ky = polar(12, 12, 9.4, a)
        parts.append(mk(S, kx, ky, 1.0))
    return parts


@icon("helical-virus", CAT, "A straight rigid rod virus made of stacked turns with a spiral line through it.",
      tags=["virus", "helix", "tobacco mosaic", "rod", "capsid", "virology", "plant virus"])
def _(S):
    f = frame((12, 12), -40)
    parts = [shell(rod(12, 12, 19, 8, -40, S))]
    for k in (-2, -1, 0, 1, 2):
        parts.append(detail(fseg(f, 4.2 * k - 1.2, 4, 4.2 * k + 1.2, -4)))
    return parts


@icon("filovirus", CAT, "A long thread-like virus curled at one end into a shepherd's crook.",
      tags=["virus", "filament", "ebola", "marburg", "hook", "pathogen", "virology"])
def _(S):
    body = tube("M8 19.5V11.5A4.5 4.5 0 0 1 17 11.5V14.5", 5.5)
    return [shell(body), mk(S, 8, 17, 1.0), mk(S, 8, 13.5, 1.0), mk(S, 12.5, 7.8, 1.0)]


@icon("bullet-shaped-virus", CAT, "A bullet-shaped virus, flat at one end and rounded at the other, with short spikes.",
      tags=["virus", "rabies", "rhabdovirus", "bullet", "spikes", "pathogen", "virology"])
def _(S):
    body = rot("M4.5 7.2H13.8A4.8 4.8 0 0 1 13.8 16.8H4.5Z", -32)
    f = frame((12, 12), -32)
    parts = [shell(body), mk(S, *f(1, 0), 1.3)]
    for x in (-4.5, -0.5, 3.5):
        parts.append(line(fseg(f, x, -5.9, x, -8.4)))
        parts.append(line(fseg(f, x, 5.9, x, 8.4)))
    return parts


@icon("poxvirus", CAT, "A rounded brick-shaped virus with a dumbbell-shaped core inside.",
      tags=["virus", "smallpox", "monkeypox", "vaccinia", "brick", "pathogen", "virology"])
def _(S):
    dumbbell = union(circle(8.2, 12, 2.3), circle(15.8, 12, 2.3), rect(8.2, 11, 7.6, 2))
    return [shell(rect(2, 5, 20, 14, L(S, 2.5, 6))), Part("dot", dumbbell)]


@icon("retrovirus", CAT, "A round spiked virus with a cone-shaped core inside.",
      tags=["virus", "hiv", "capsid", "envelope", "rna virus", "pathogen", "virology"])
def _(S):
    parts = [shell(circle(12, 12, 6.8)),
             detail(poly([(8.4, 8.8), (15.6, 8.8), (12, 15.8)], closed=True, r=S.r * 0.4))]
    for a in range(-90, 270, 45):
        x0, y0 = polar(12, 12, 6.8, a)
        x1, y1 = polar(12, 12, 9.6, a)
        parts.append(line(seg(x0, y0, x1, y1)))
    return parts


@icon("spike-protein", CAT, "A club-shaped protein with a wide head on a slim stalk, standing on a membrane line.",
      tags=["virus", "glycoprotein", "trimer", "receptor", "membrane", "antigen", "molecular biology"])
def _(S):
    club = ("M10.8 20.5V12.5C6.2 11.5 4.6 7 7.2 4.4C9.6 2.2 14.4 2.2 16.8 4.4C19.4 7 17.8 11.5 13.2 12.5V20.5Z")
    return [shell(club), line(seg(2, 21, 22, 21))]


@icon("prion", CAT, "A normal coiled protein on the left turning into a misfolded stack of flat arrows on the right.",
      tags=["misfolded protein", "mad cow", "amyloid", "protein folding", "infectious protein", "disease", "neurodegeneration"])
def _(S):
    parts = [line("M5 3.5Q9.5 5 5 7.5T5 11.5T5 15.5T5 19.5")]
    parts.append(line(seg(9.5, 12, 12, 12)))
    parts.append(ah((12.8, 12), 0, S, 1.3))
    for y in (6.5, 12, 17.5):
        parts.append(line(seg(15, y, 19.5, y)))
        parts.append(ah((21, y), 0, S, 1.4))
    return parts


@icon("viral-replication", CAT, "A cell with one virus entering on the left and new virus particles budding out on the right.",
      tags=["virus", "infection", "host cell", "budding", "life cycle", "replication", "virology"])
def _(S):
    parts = [shell(circle(11.5, 12, 7)), mk(S, 2.6, 12, 1.5)]
    for x, y in ((9, 10), (13, 9.5), (11.5, 14.5)):
        parts.append(mk(S, x, y, 1.1))
    parts.append(shell(circle(21, 7.5, 1.5)))
    parts.append(shell(circle(21, 16.5, 1.5)))
    return parts


# ============================================================================ protozoa

@icon("giardia", CAT, "A pear-shaped single cell seen from the front with two round nuclei like eyes and trailing tails.",
      tags=["protozoa", "parasite", "flagellate", "protist", "waterborne", "microscopy", "gut parasite"])
def _(S):
    body = "M12 2.8C17.2 2.8 19 7 17.6 11.5C16.6 14.6 14 16.5 12 16.5C10 16.5 7.4 14.6 6.4 11.5C5 7 6.8 2.8 12 2.8Z"
    parts = [shell(body), mk(S, 9.3, 8.2, 1.5), mk(S, 14.7, 8.2, 1.5)]
    for x, deg in ((10, 105), (12, 90), (14, 75)):
        parts.append(line(fwave(frame((x, 16.8), deg), 0, 5, 0.7, 2)))
    return parts


@icon("didinium", CAT, "A barrel-shaped ciliate with a pointed snout and two bands of hairs.",
      tags=["protozoa", "ciliate", "predator", "protist", "cilia", "pond life", "microscopy"])
def _(S):
    body = union(ellipse(12, 14, 6.5, 7), poly([(8.8, 8.5), (15.2, 8.5), (12, 2.5)], closed=True))
    parts = [shell(body), detail("M5.5 12.2Q12 14.7 18.5 12.2"), detail("M6 17.3Q12 19.8 18 17.3")]
    for y in (12.7, 17.8):
        parts.append(line(seg(5.3, y, 2.8, y)))
        parts.append(line(seg(18.7, y, 21.2, y)))
    return parts


@icon("malaria-parasite", CAT, "A round red blood cell with a small signet-ring shaped parasite inside.",
      tags=["plasmodium", "mosquito", "blood cell", "infection", "parasite", "protozoa", "disease"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(circle(10.8, 12.6, 3.2)), mk(S, 13.6, 10.2, 1.6)]


@icon("toxoplasma", CAT, "A banana-shaped crescent cell with a pointed end and a round nucleus in the middle.",
      tags=["protozoa", "parasite", "cat parasite", "crescent", "toxoplasmosis", "cell", "microscopy"])
def _(S):
    body = "M2.8 6.5C5 20.5 19 20.5 21.2 6.5C17.5 12.5 6.5 12.5 2.8 6.5Z" if S.name == "line" else \
        "M3.6 7.2C6 20 18 20 20.4 7.2C20.8 5.4 18.8 5.2 17.8 6.8C15.2 11.8 8.8 11.8 6.2 6.8C5.2 5.2 3.2 5.4 3.6 7.2Z"
    cx, cy = polar(12, 12, 3.1, 90 - 30)
    return [shell(rot(body, -28, 12, 12)), Part("dot", rot(circle(12, 14, 1.5) if S.name == "rounded" else rect(10.5, 12.5, 3, 3), -28, 12, 12))]


@icon("trichomonas", CAT, "A teardrop-shaped cell with whip tails at the front and a wavy fin along one side.",
      tags=["protozoa", "parasite", "flagellate", "undulating membrane", "protist", "microscopy", "single cell"])
def _(S):
    body = "M12 21.5C8.5 18 7 14.5 7 11.5A5 5 0 0 1 17 11.5C17 14.5 15.5 18 12 21.5Z"
    parts = [shell(body), detail("M14 10q1.5 1.8 0 3.6t0 3.6")]
    for x, deg in ((9.6, -140), (12, -90), (14.4, -40)):
        parts.append(line(fwave(frame((x, 6.8), deg), 0, 5.2, 0.8, 2)))
    return parts


@icon("choanoflagellate", CAT, "An oval cell topped by a funnel collar of fine lines with one long tail rising from the center.",
      tags=["protist", "collar cell", "flagellum", "plankton", "animal ancestor", "microscopy", "single cell"])
def _(S):
    parts = [shell(ellipse(12, 17, 5.2, 4.2)), mk(S, 12, 17, 1.3),
             line(seg(8.5, 12.8, 4.8, 6.5)), line(seg(10.8, 12.4, 8.4, 7.5)),
             line(seg(13.2, 12.4, 15.6, 7.5)), line(seg(15.5, 12.8, 19.2, 6.5)),
             line(vwave(12, 12.3, 2.3, 1.1, 3))]
    return parts


@icon("testate-amoeba", CAT, "A dome-shaped shell with blunt false feet poking out of its opening.",
      tags=["protozoa", "shell", "pseudopod", "arcella", "amoeba", "pond life", "microscopy"])
def _(S):
    dome = "M3 16.5A9 11 0 0 1 21 16.5H16Q12 11.5 8 16.5Z"
    parts = [shell(dome), mk(S, 7.5, 11.5, 1.1), mk(S, 12.5, 7.8, 1.1), mk(S, 16.5, 11.5, 1.1)]
    parts.append(line(seg(12, 15.5, 12, 21)))
    parts.append(line(seg(10.5, 16.5, 7.5, 20.5)))
    parts.append(line(seg(13.5, 16.5, 16.5, 20.5)))
    return parts


@icon("suctorian", CAT, "A round cell on a thin stalk with straight tentacles, each ending in a small knob.",
      tags=["protozoa", "ciliate", "tentacles", "predator", "stalk", "pond life", "microscopy"])
def _(S):
    parts = [shell(circle(12, 10.5, 4.2)), line(seg(12, 14.7, 12, 20.2)), line(seg(8, 21, 16, 21))]
    for a in (-155, -122, -90, -58, -25):
        x0, y0 = polar(12, 10.5, 4.2, a)
        x1, y1 = polar(12, 10.5, 6.9, a)
        kx, ky = polar(12, 10.5, 8.4, a)
        parts.append(line(seg(x0, y0, x1, y1)))
        parts.append(mk(S, kx, ky, 1.0))
    return parts


# ============================================================================ algae

@icon("pennate-diatom", CAT, "A long narrow boat-shaped diatom with a central line and fine stripes on both sides.",
      tags=["algae", "diatom", "silica", "phytoplankton", "microscopy", "plankton", "frustule"])
def _(S):
    boat = "M2.5 12Q12 3.5 21.5 12Q12 20.5 2.5 12Z" if S.name == "line" else ellipse(12, 12, 9.5, 5.6)
    parts = [shell(boat), detail(seg(5.5, 12, 18.5, 12))]
    for x in (8.5, 15.5):
        parts.append(detail(seg(x, 9.4, x, 10.8)))
        parts.append(detail(seg(x, 13.2, x, 14.6)))
    return parts


@icon("chlorella", CAT, "Three tiny round green-alga cells, each with a dot-sized chloroplast inside.",
      tags=["algae", "green algae", "microalgae", "single cell", "chloroplast", "microscopy", "phytoplankton"])
def _(S):
    return [shell(circle(12, 6.8, 4)), shell(circle(6, 17.2, 4)), shell(circle(18, 17.2, 4)),
            mk(S, 12, 6.8, 1.0), mk(S, 6, 17.2, 1.0), mk(S, 18, 17.2, 1.0)]


@icon("pediastrum", CAT, "A flat star-shaped colony of cells in rings, with horned cells around the edge.",
      tags=["algae", "green algae", "colony", "freshwater", "plankton", "microscopy", "star"])
def _(S):
    pts = []
    for i in range(16):
        r = 9.6 if i % 2 == 0 else 6.6
        pts.append(polar(12, 12, r, -90 + i * 22.5))
    parts = [shell(poly(pts, closed=True, r=S.r * 0.6)), detail(circle(12, 12, 2.6))]
    return parts


@icon("scenedesmus", CAT, "Four narrow cells lined up side by side, the two end cells carrying long curved spines.",
      tags=["algae", "green algae", "colony", "coenobium", "freshwater", "microscopy", "spines"])
def _(S):
    parts = [shell(rect(5, 7, 14, 10, L(S, 2, 4.5)))]
    for x in (8.5, 12, 15.5):
        parts.append(detail(seg(x, 7, x, 17)))
    parts.append(line("M6.2 7Q5.5 4 2.5 3"))
    parts.append(line("M6.2 17Q5.5 20 2.5 21"))
    parts.append(line("M17.8 7Q18.5 4 21.5 3"))
    parts.append(line("M17.8 17Q18.5 20 21.5 21"))
    return parts


@icon("closterium", CAT, "A slender crescent-moon shaped cell with a small nucleus in the middle.",
      tags=["algae", "desmid", "crescent", "freshwater", "microscopy", "single cell", "moon"])
def _(S):
    body = "M1.8 8.5Q12 28 22.2 8.5Q12 19.5 1.8 8.5Z" if S.name == "line" else \
        "M2.6 9Q12 26.5 21.4 9C21.7 7.4 20 7.2 19.3 8.5C16.5 14 7.5 14 4.7 8.5C4 7.2 2.3 7.4 2.6 9Z"
    nuc = circle(12, 15.6, 1.1) if S.name == "rounded" else rect(10.9, 14.5, 2.2, 2.2)
    return [shell(rot(body, -32, 12, 12)), Part("dot", rot(nuc, -32, 12, 12))]


@icon("micrasterias", CAT, "A flat disc-shaped alga cut into many lobes and divided in half by a narrow waist.",
      tags=["algae", "desmid", "green algae", "freshwater", "microscopy", "lobed", "single cell"])
def _(S):
    cs = [polar(12, 12, 6.4, -90 + 36 * i) for i in range(10)]
    body = union(circle(12, 12, 5), *[circle(x, y, 3.0) for x, y in cs])
    body = minus(body, rect(10.9, 0, 2.2, 5.6), rect(10.9, 18.4, 2.2, 6))
    return [shell(body), detail(seg(12, 6, 12, 18))]


@icon("red-algae", CAT, "A branching feathery seaweed frond with forked side branches.",
      tags=["seaweed", "algae", "rhodophyta", "marine", "frond", "ocean plant", "dulse"])
def _(S):
    parts = [line("M11 21.5Q13 14 12 6"), line(seg(12, 6, 10, 3.6)), line(seg(12, 6, 14, 3.6))]
    for y, sg in ((18, 1), (14, -1), (10.5, 1)):
        x0 = 12.1
        x1, y1 = x0 + sg * 5, y - 5
        parts.append(line(seg(x0, y, x1, y1)))
        parts.append(line(seg(x1, y1, x1 + sg * 0.2, y1 - 2.4)))
        parts.append(line(seg(x1, y1, x1 + sg * 2.4, y1 - 0.2)))
    return parts


@icon("bladderwrack", CAT, "A forked flat seaweed frond with a midrib and round air bladders along its branches.",
      tags=["seaweed", "brown algae", "kelp", "fucus", "air bladders", "intertidal", "marine"])
def _(S):
    parts = [line(seg(12, 21.5, 12, 13)), line(seg(12, 13, 6, 3.5)), line(seg(12, 13, 18, 3.5)),
             mk(S, 9.2, 18, 1.5), mk(S, 14.8, 18, 1.5)]
    for sg in (-1, 1):
        parts.append(mk(S, 12 + sg * -2.2, 9.2 + 0, 0.0) if False else mk(S, 12 + sg * 4.6, 10.6, 1.5))
        parts.append(mk(S, 12 + sg * 7.2, 6.6, 1.5))
        parts.append(mk(S, 12 + sg * 2.0, 5.4 + 1.2, 1.5))
    return parts


def hex_pts(cx, cy, R):
    return [polar(cx, cy, R, 60 * i) for i in range(6)]


_HEX_CELLS = [(6.9, 8.3), (6.9, 14.7), (12.45, 11.5), (18, 8.3), (18, 14.7)]


def _net_filled():
    return U(*[ST(poly(hex_pts(x, y, 3.7), closed=True), 2.7, "round", "round") for x, y in _HEX_CELLS])


@icon("hydrodictyon", CAT, "A small net of green cells forming hexagonal openings, like a fishing net.",
      tags=["algae", "water net", "green algae", "colony", "freshwater", "mesh", "microscopy"], filled=_net_filled)
def _(S):
    rings = [thick(poly(hex_pts(x, y, 3.7), closed=True, r=L(S, 0, 1.5)), 2, S) for x, y in _HEX_CELLS]
    return [solid(union(*rings))]


@icon("stonewort", CAT, "An upright stem with rings of thin straight branches spaced along it like a bottle brush.",
      tags=["algae", "chara", "charophyte", "whorl", "freshwater", "aquatic plant", "pond"])
def _(S):
    parts = [line(seg(12, 21.5, 12, 3))]
    for y in (7, 12.5, 18):
        for sg in (-1, 1):
            parts.append(line(seg(12, y, 12 + sg * 6.5, y + 2.6)))
    parts.append(line(seg(12, 3, 9.8, 1.6)))
    parts.append(line(seg(12, 3, 14.2, 1.6)))
    return parts


@icon("candida-yeast", CAT, "A chain of oval yeast cells with round buds branching off at the joints.",
      tags=["fungus", "yeast", "pseudohypha", "budding", "microbiology", "thrush", "microscopy"])
def _(S):
    ells = [rot(ellipse(c[0], c[1], 4.6, 3.0), -45, c[0], c[1]) for c in ((6.8, 17.2), (12, 12), (17.2, 6.8))]
    return [shell(union(*ells)), shell(circle(18, 17, 2.4))]


@icon("ascus", CAT, "A narrow sac-shaped fungal pod holding a row of round spores.",
      tags=["fungus", "ascospores", "spore sac", "sac fungi", "ascomycete", "mycology", "microscopy"])
def _(S):
    f = frame((12, 12), -28)
    parts = [shell(rod(12, 12, 20, 8, -28, S))]
    for x in (-6.3, -2.1, 2.1, 6.3):
        parts.append(mk(S, *f(x, 0), 1.4))
    return parts


@icon("basidium", CAT, "A club-shaped fungal cell with four small prongs on top, each carrying a round spore.",
      tags=["fungus", "basidiospores", "mushroom gills", "club fungi", "basidiomycete", "mycology", "microscopy"])
def _(S):
    club = "M10.4 21.5V14.5C6.8 13 6.8 8.5 9.8 8.5H14.2C17.2 8.5 17.2 13 13.6 14.5V21.5Z"
    parts = [shell(club)]
    for x0, x1 in ((9.6, 7.2), (11.4, 10.2), (12.6, 13.8), (14.4, 16.8)):
        parts.append(line(seg(x0, 8.5, x1, 5)))
    for x in (6.6, 9.7, 14.3, 17.4):
        parts.append(mk(S, x, 3.3, 1.3))
    return parts


@icon("zygospore", CAT, "A dark spiky-walled round spore sitting between two short threads joining from each side.",
      tags=["fungus", "mold", "conjugation", "resting spore", "zygomycete", "mycology", "microscopy"])
def _(S):
    pts = [polar(12, 12, 6.6 if i % 2 == 0 else 5.2, -90 + i * 20) for i in range(18)]
    return [shell(poly(pts, closed=True)), mk(S, 12, 12, 2.4),
            line(seg(2, 12, 5.3, 12)), line(seg(18.7, 12, 22, 12))]


@icon("chytrid-fungus", CAT, "A round spore body with thin root-like threads below and a single whip tail.",
      tags=["fungus", "zoospore", "amphibian disease", "flagellum", "rhizoids", "aquatic fungus", "microscopy"])
def _(S):
    parts = [shell(circle(10.5, 8.5, 4.5)),
             line(fwave(frame((15.2, 7.4), -22), 0, 8, 1.0, 3)),
             line(seg(10.5, 13, 10.5, 21.5)), line(seg(10.5, 16.5, 6, 20.5)), line(seg(10.5, 16.5, 15, 20.5))]
    return parts


@icon("mycorrhiza", CAT, "A root tip wrapped in fine fungal threads that spread out into the soil.",
      tags=["fungus", "roots", "symbiosis", "soil", "mycelium", "plant nutrition", "hyphae"])
def _(S):
    parts = [shell(rect(9, 2.5, 6, 10, L(S, 2, 3)))]
    for p0, deg, ln in (((12, 13.5), 90, 8), ((10, 13), 125, 9), ((14, 13), 55, 9), ((9, 7), 165, 7), ((15, 7), 15, 7)):
        parts.append(line(fwave(frame(p0, deg), 0, ln, 0.9, 3)))
    return parts


@icon("powdery-mildew", CAT, "A leaf spotted with white powdery patches of tiny dots.",
      tags=["fungus", "plant disease", "leaf", "blight", "garden", "mold", "spores"])
def _(S):
    leaf = "M3.5 20.5C3 11 9.5 3.5 20.5 3.5C21 14.5 13.5 21 3.5 20.5Z"
    return [shell(leaf), detail(seg(4.5, 19.5, 14, 10)),
            mk(S, 9, 10.5, 1.1), mk(S, 12.5, 7.5, 1.1), mk(S, 16.5, 6.5, 1.1),
            mk(S, 13, 15.5, 1.1), mk(S, 17, 12.5, 1.1)]


# ============================================================================ cell structures

@icon("cell-nucleus", CAT, "A round nucleus with a double outline and a solid nucleolus inside.",
      tags=["organelle", "dna", "cell", "nuclear envelope", "nucleolus", "cell biology", "chromatin"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(circle(12, 12, 5.6)), mk(S, 11, 12, 2.2)]


@icon("endoplasmic-reticulum", CAT, "Stacked wavy membrane sheets studded with tiny ribosome dots.",
      tags=["organelle", "rough er", "ribosomes", "membrane", "cell", "cell biology", "protein synthesis"])
def _(S):
    parts = []
    for y in (8, 14, 20):
        parts.append(line(wave(2, 22, y, 1.2, 4)))
        for x in (4.5, 14.5):
            parts.append(mk(S, x, y - 1.2 - 2.4, 1.0))
    return parts


@icon("lysosome", CAT, "A round membrane sac holding small dots and tiny cross marks of digestive enzymes.",
      tags=["organelle", "enzymes", "digestion", "cell", "cell biology", "vesicle", "waste"])
def _(S):
    return [shell(circle(12, 12, 9)), mk(S, 8, 8.5, 1.2), mk(S, 15.5, 8, 1.2), mk(S, 8.5, 15.5, 1.2),
            mk(S, 15.8, 15.2, 1.2),
            detail(seg(10.9, 10.9, 13.1, 13.1)), detail(seg(10.9, 13.1, 13.1, 10.9))]


@icon("peroxisome", CAT, "A round membrane sac with a small square crystal core in the center.",
      tags=["organelle", "enzymes", "catalase", "cell", "cell biology", "vesicle", "oxidation"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(rect(8.7, 8.7, 6.6, 6.6, L(S, 0.5, 1.8)))]


@icon("centriole", CAT, "Two short barrel-shaped cylinders set at right angles, each with ribbed walls.",
      tags=["organelle", "centrosome", "cell division", "microtubules", "cell", "cell biology", "spindle"])
def _(S):
    return [shell(rect(2.5, 15, 14.5, 6.5, L(S, 1.5, 3))), detail(seg(7.3, 15, 7.3, 21.5)), detail(seg(12.2, 15, 12.2, 21.5)),
            shell(rect(15.5, 2.5, 6, 9.5, L(S, 1.5, 3))), detail(seg(15.5, 7.2, 21.5, 7.2))]


def edot(x, y, rx, ry, deg=0):
    """Small solid oval mark (nucleus, granule), optionally turned."""
    d = ellipse(x, y, rx, ry)
    return Part("dot", rot(d, deg, x, y) if deg else d)


@icon("cytoskeleton", CAT, "A round cell outline with a web of filament lines radiating from a central dot.",
      tags=["cell", "filaments", "scaffold", "cell structure", "cell biology", "network", "cytoplasm"])
def _(S):
    parts = [shell(circle(12, 12, 9)), mk(S, 12, 12, 1.8)]
    for a in (-80, -8, 64, 136, 208):
        x0, y0 = polar(12, 12, 3.8, a)
        x1, y1 = polar(12, 12, 8.6, a)
        parts.append(detail(seg(x0, y0, x1, y1)))
    return parts


@icon("microtubule", CAT, "A hollow tube with an open end, built from rows of small beads.",
      tags=["cytoskeleton", "tubulin", "protein", "cell structure", "cell biology", "polymer", "spindle"])
def _(S):
    f = frame((12, 12), -35)
    body = rot(rect(3.5, 8, 14.5, 8, L(S, 1, 2)), -35, 12, 12)
    parts = [shell(body), shell(rot(ellipse(18, 12, 2.4, 4), -35, 12, 12))]
    for x, y in ((-5.6, -1.3), (-3.2, 1.3), (-0.8, -1.3), (1.6, 1.3)):
        parts.append(mk(S, *f(x, y), 0.85))
    return parts


def _actin_pts():
    pts = [(3, 12), (9, 12), (15, 12), (21, 12)]
    for x, sg in ((6, -1), (12, 1), (18, -1)):
        pts += [(x, 12 + sg * 4.4), (x, 12 - sg * 4.4)]
    return pts


def _actin_filled():
    return U(*[P(circle(x, y, 1.9)) for x, y in _actin_pts()], ST(wave(3, 21, 12, 4.4, 3), 1.4, "round", "round"),
             ST(wave(3, 21, 12, -4.4, 3), 1.4, "round", "round"))


@icon("actin-filament", CAT, "Two strings of round beads twisting around each other like a thin rope.",
      tags=["cytoskeleton", "microfilament", "protein", "muscle", "cell biology", "polymer", "double helix"],
      filled=_actin_filled)
def _(S):
    parts = [line(wave(3, 21, 12, 4.4, 3)), line(wave(3, 21, 12, -4.4, 3))]
    for x, y in _actin_pts():
        parts.append(mk(S, x, y, 1.6))
    return parts


@icon("cilia", CAT, "A row of cells along a flat surface with short curved hairs on top bending in a wave.",
      tags=["cell", "hairs", "epithelium", "airway", "motile", "cell biology", "ciliated"])
def _(S):
    parts = [shell(rect(2.5, 15, 19, 6.5, L(S, 1.5, 3))), detail(seg(12, 15, 12, 21.5))]
    for i, x in enumerate((5, 9, 13, 17, 21 - 0.0)):
        if x > 20:
            x = 19.5
        parts.append(line(f"M{fmt(x)} 14.2Q{fmt(x - 1 + i * 0.7)} 9.5 {fmt(x + 1.5 + i * 0.5)} 5.5"))
    return parts


@icon("motor-protein", CAT, "A two-legged protein walking along a track while carrying a round vesicle on its back.",
      tags=["kinesin", "dynein", "myosin", "transport", "molecular motor", "cell biology", "cargo"])
def _(S):
    return [shell(circle(12, 6.3, 4.4)), line(seg(12, 10.7, 12, 12.5)),
            line("M12 12.5L8.5 15.5L8.5 18.8"), line("M12 12.5L15.5 15.5L15.5 18.8"),
            mk(S, 8.5, 19.2, 1.5), mk(S, 15.5, 19.2, 1.5),
            line(seg(2, 21.7, 22, 21.7))]


@icon("vesicle-transport", CAT, "A small round vesicle budding off a membrane with an arrow pointing toward a second membrane.",
      tags=["membrane", "trafficking", "bud", "cargo", "cell biology", "transport", "secretion"])
def _(S):
    return [line("M3.5 2.5V8.5A3.5 3.5 0 0 1 3.5 15.5V21.5"), shell(circle(11, 12, 2.6)),
            line(seg(14.8, 12, 17.2, 12)), ah((18.4, 12), 0, S, 1.5),
            line(seg(21.5, 2.5, 21.5, 21.5))]


@icon("exocytosis", CAT, "A membrane line with a vesicle fused into it, opening outward and releasing small dots.",
      tags=["secretion", "vesicle", "membrane", "release", "cell biology", "neurotransmitter", "cell"])
def _(S):
    return [line("M2 11H7A5 7 0 0 0 17 11H22"), mk(S, 12, 15, 1.3),
            mk(S, 8.5, 6.5, 1.2), mk(S, 15.5, 6.5, 1.2), mk(S, 12, 3.5, 1.2)]


@icon("apoptosis", CAT, "A round cell with a crack across it, shedding small round blebs around it.",
      tags=["cell death", "programmed cell death", "blebbing", "cell", "cell biology", "fragmentation", "necrosis"])
def _(S):
    return [shell(circle(12, 12, 4.8)), detail(poly([(7.7, 10), (10.6, 12.6), (13, 10.2), (16.6, 14)], r=S.r * 0.6)),
            dot(4.5, 4.5, 2.2), dot(19.5, 4.5, 2.2), dot(19.5, 19.5, 2.2), dot(4.5, 19.5, 2.2)]


@icon("dendritic-cell", CAT, "A small cell body with long uneven branching arms spreading out in all directions.",
      tags=["immune cell", "antigen presenting", "branched", "white blood cell", "immunology", "cell", "arms"])
def _(S):
    parts = [shell(circle(12, 12, 3.8))]
    for a, ln, forks in ((-100, 7.4, (-38, 38)), (-35, 6, (30,)), (30, 7.4, (-38, 38)), (100, 5.6, (-30,)),
                         (160, 7.4, (-38, 38)), (215, 6, (35,))):
        x0, y0 = polar(12, 12, 3.8, a)
        x1, y1 = polar(12, 12, 3.8 + ln - 2.6, a)
        parts.append(line(seg(x0, y0, x1, y1)))
        for da in forks:
            x2, y2 = polar(x1, y1, 3.0, a + da)
            parts.append(line(seg(x1, y1, x2, y2)))
    return parts


@icon("t-cell", CAT, "A round immune cell with a large nucleus and short Y-shaped receptors around its surface.",
      tags=["lymphocyte", "immune cell", "white blood cell", "receptor", "immunology", "cell", "adaptive immunity"])
def _(S):
    parts = [shell(circle(12, 12, 5.8)), mk(S, 12, 12, 2.6)]
    for a in range(-90, 270, 60):
        x0, y0 = polar(12, 12, 5.8, a)
        x1, y1 = polar(12, 12, 8.0, a)
        parts.append(line(seg(x0, y0, x1, y1)))
        for da in (-42, 42):
            x2, y2 = polar(x1, y1, 2.2, a + da)
            parts.append(line(seg(x1, y1, x2, y2)))
    return parts


@icon("mast-cell", CAT, "An oval cell packed with round granules, a few granules bursting out of one side.",
      tags=["immune cell", "histamine", "allergy", "granules", "degranulation", "immunology", "cell"])
def _(S):
    parts = [shell(ellipse(9.5, 12, 7, 6.2))]
    for x, y in ((6.5, 10), (10, 8.8), (13, 11), (7.5, 14.5), (11, 15)):
        parts.append(mk(S, x, y, 1.1))
    for x, y in ((20, 8.5), (21.2, 13), (19.6, 17.2)):
        parts.append(mk(S, x, y, 1.0))
    return parts


@icon("fat-cell", CAT, "A large round cell filled by one big droplet, with a small flat nucleus pressed against the edge.",
      tags=["adipocyte", "lipid", "fat", "adipose tissue", "cell biology", "droplet", "storage"])
def _(S):
    nuc = Part("dot", rect(4.5, 9.4, 1.8, 5.2, 0)) if S.name == "line" else edot(5.4, 12, 0.9, 2.6)
    return [shell(circle(12, 12, 9)), detail(circle(13.4, 12, 5.8)), nuc]


@icon("goblet-cell", CAT, "A wine-goblet shaped cell with a wide top full of mucus droplets and a narrow stem holding the nucleus.",
      tags=["mucus", "epithelium", "secretion", "cell biology", "airway", "intestine", "histology"])
def _(S):
    body = poly([(3.5, 3.5), (20.5, 3.5), (20, 8), (14.5, 12.5), (14.5, 19.5), (9.5, 19.5), (9.5, 12.5), (4, 8)], closed=True, r=S.r)
    return [shell(body), mk(S, 8.5, 7, 1.2), mk(S, 12, 6.6, 1.2), mk(S, 15.5, 7, 1.2), mk(S, 10.5, 10, 1.1),
            mk(S, 13.5, 10, 1.1), edot(12, 16.8, 1.3, 1.5)]


@icon("epithelial-tissue", CAT, "A row of tall column-shaped cells side by side, each with an oval nucleus near the base.",
      tags=["histology", "tissue", "columnar", "cells", "lining", "cell biology", "membrane"])
def _(S):
    parts = [shell(rect(2.5, 3, 19, 15, L(S, 1.5, 3))), detail(seg(8.83, 3, 8.83, 18)), detail(seg(15.17, 3, 15.17, 18)),
             line(seg(2.5, 21.5, 21.5, 21.5))]
    for x in (5.66, 12, 18.34):
        parts.append(edot(x, 14.2, 1.1, 1.5))
    return parts


@icon("rod-and-cone-cells", CAT, "Two slim light-sensing cells side by side, one topped by a long rod and the other by a short cone.",
      tags=["retina", "photoreceptor", "eye", "vision", "histology", "cell biology", "light sensing"])
def _(S):
    rod_c = poly([(5.5, 2.5), (8, 2.5), (8, 12), (10, 12), (10, 21.5), (3.5, 21.5), (3.5, 12), (5.5, 12)], closed=True, r=S.r * 0.5)
    cone = poly([(17, 8), (19.5, 12), (20.5, 12), (20.5, 21.5), (13.5, 21.5), (13.5, 12), (15, 12)], closed=True, r=S.r * 0.5)
    return [shell(rod_c), shell(cone), mk(S, 6.75, 17, 1.2), mk(S, 17, 17, 1.2)]


@icon("myelinated-axon", CAT, "A long nerve fiber wrapped in a row of sausage-shaped sheath segments with small gaps between them.",
      tags=["neuron", "nerve", "myelin sheath", "node of ranvier", "schwann cell", "neuroscience", "axon"])
def _(S):
    parts = [line(seg(2, 12, 22, 12))]
    for x in (2.2, 9.8, 17.4):
        parts.append(shell(rect(x, 6.5, 4.4, 11, L(S, 1.2, 2.2))))
    return parts


@icon("sarcomere", CAT, "A muscle unit between two zigzag end lines, with a thick bar overlapped by thin filament lines.",
      tags=["muscle", "myofibril", "actin", "myosin", "contraction", "cell biology", "z line"])
def _(S):
    return [line(poly([(4.5, 3), (3, 7.5), (4.5, 12), (3, 16.5), (4.5, 21)], r=0)),
            line(poly([(19.5, 3), (21, 7.5), (19.5, 12), (21, 16.5), (19.5, 21)], r=0)),
            line(seg(5, 7.5, 12, 7.5)), line(seg(5, 16.5, 12, 16.5)),
            line(seg(12, 7.5, 19, 7.5)),
            line(seg(12, 16.5, 19, 16.5)),
            solid(rect(8, 10.2, 8, 3.6, L(S, 0, 1.8)))]


@icon("root-hair-cell", CAT, "A rectangular plant cell with one long finger-like extension growing out of its side.",
      tags=["plant cell", "root", "absorption", "water uptake", "botany", "cell biology", "hair"])
def _(S):
    body = union(rect(2.5, 7, 11, 11, L(S, 1.5, 3)), thick("M12 11.5Q17.5 11.5 20 4.5", 4, S))
    return [shell(body), mk(S, 7.5, 12.5, 1.5)]


@icon("xylem-vessel", CAT, "A tall tube with slanted ring-like thickening bands along its walls.",
      tags=["plant", "water transport", "vascular tissue", "botany", "wood", "cell biology", "tube"])
def _(S):
    return [line(seg(6, 2, 6, 22)), line(seg(18, 2, 18, 22)),
            line(seg(6, 6.5, 18, 4)), line(seg(6, 12.5, 18, 10)), line(seg(6, 18.5, 18, 16))]


@icon("plasmolysis", CAT, "A rectangular plant cell wall with the shrunken inner membrane pulled away into a small rounded blob.",
      tags=["plant cell", "osmosis", "cell wall", "shrinking", "salt", "botany", "cell biology"])
def _(S):
    return [shell(rect(2.5, 4, 19, 16, L(S, 1.5, 3))), detail(ellipse(12, 12, 5.2, 4.2)), mk(S, 12, 12, 1.3)]


@icon("gap-junction", CAT, "Two membrane bands side by side joined by short paired tube channels running between them.",
      tags=["cell connection", "connexon", "channel", "cell communication", "membrane", "cell biology", "heart"])
def _(S):
    parts = [shell(rect(2.5, 2.5, 19, 5, L(S, 1.5, 2.5))), shell(rect(2.5, 16.5, 19, 5, L(S, 1.5, 2.5)))]
    for x in (5, 15):
        parts.append(shell(rect(x, 7.5, 4, 9, 0)))
        parts.append(detail(seg(x, 12, x + 4, 12)))
    return parts


@icon("mitotic-spindle", CAT, "A lemon-shaped set of fiber lines between two pole dots with X-shaped chromosomes in the middle.",
      tags=["cell division", "mitosis", "chromosomes", "metaphase", "microtubules", "cell biology", "centrosome"])
def _(S):
    lens = "M4.5 12Q12 2.5 19.5 12Q12 21.5 4.5 12Z"
    parts = [shell(lens), mk(S, 2.4, 12, 1.3), mk(S, 21.6, 12, 1.3)]
    for y in (9.4, 14.6):
        parts.append(detail(seg(10.8, y - 1.1, 13.2, y + 1.1)))
        parts.append(detail(seg(10.8, y + 1.1, 13.2, y - 1.1)))
    return parts


@icon("endosymbiosis", CAT, "A large cell with a small oval organelle inside and another small cell moving in along a short arrow.",
      tags=["organelle origin", "mitochondria", "symbiosis", "evolution", "engulf", "cell biology", "chloroplast"])
def _(S):
    return [shell(circle(14, 13.5, 7.6)), edot(17, 17, 2.7, 1.8, -30),
            shell(rot(ellipse(5, 5, 3, 2), 35, 5, 5)),
            line(seg(8.2, 8.4, 11.6, 11.8)), ah((12.4, 12.6), 45, S, 1.5)]
