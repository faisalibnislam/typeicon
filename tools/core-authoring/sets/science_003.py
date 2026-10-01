"""TypeIcon Core: science (batch 3): lab instruments, microbes, genetics, field gear, hazards, molecules."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, polar, rotation, transform_path

CAT = "science"


def mk(S, x, y, r=1.25):
    """Small mark: round in Rounded, square in Line."""
    if S.name == "rounded":
        return dot(x, y, r)
    return Part("dot", rect(x - r, y - r, 2 * r, 2 * r))


def thick(d, w, S):
    return path_to_d(ST(d, w, S.cap, S.join))


def rot(d, deg, cx=12, cy=12):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def blob(cx, cy, radii, rot0=-90, k=1.0):
    """Smooth closed blob through points at equal angles with the given radii (Catmull-Rom to cubic)."""
    n = len(radii)
    pts = [polar(cx, cy, radii[i], rot0 + i * 360 / n) for i in range(n)]
    d = "M%s %s" % (fmt(pts[0][0]), fmt(pts[0][1]))
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * k, p1[1] + (p2[1] - p0[1]) / 6 * k)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * k, p2[1] - (p3[1] - p1[1]) / 6 * k)
        d += "C%s %s %s %s %s %s" % (fmt(c1[0]), fmt(c1[1]), fmt(c2[0]), fmt(c2[1]), fmt(p2[0]), fmt(p2[1]))
    return d + "Z"


# ============================================================================ instruments

@icon("ammeter", CAT, "Round dial meter with the letter A on its face", tags=["current meter", "amps", "electric current", "meter", "gauge", "physics"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(poly([(8.5, 17), (12, 8), (15.5, 17)], r=S.r * 0.4)),
        detail(seg(9.8, 14, 14.2, 14)),
    ]


@icon("oscilloscope", CAT, "Bench oscilloscope with a sine wave on its screen and knobs at the side", tags=["scope", "waveform", "signal", "electronics", "lab", "measurement"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, S.R)),
        detail(seg(15.5, 4, 15.5, 20)),
        line("M5.5 12q1.75-5 3.5 0t3.5 0"),
        mk(S, 19, 9, 1.2),
        mk(S, 19, 15, 1.2),
    ]


@icon("superconductor", CAT, "Small magnet floating above a shallow dish with cold vapour rising between them", tags=["levitation", "maglev", "magnet", "cryogenic", "zero resistance", "physics"])
def _(S):
    return [
        shell(rect(8, 2, 8, 6, min(S.R, 2))),
        detail(seg(12, 2, 12, 8)),
        line("M8.5 10.5q-1.5 1.75 0 3.5"),
        line("M15.5 10.5q1.5 1.75 0 3.5"),
        shell(poly([(2.5, 15.5), (21.5, 15.5), (19, 21.5), (5, 21.5)], closed=True, r=S.r)),
    ]


@icon("magdeburg-hemispheres", CAT, "Two metal half-spheres pressed together with handles pulling apart", tags=["vacuum", "air pressure", "hemispheres", "physics demo", "atmospheric pressure", "experiment"])
def _(S):
    return [
        shell(circle(12, 12, 5.5)),
        detail(seg(12, 6.5, 12, 17.5)),
        line(poly([(6.5, 12), (3, 12)], r=0)),
        line(poly([(17.5, 12), (21, 12)], r=0)),
        line(poly([(3, 8.5), (3, 15.5)], r=0)),
        line(poly([(21, 8.5), (21, 15.5)], r=0)),
    ]


# ============================================================================ genetics and cell biology

@icon("golgi-apparatus", CAT, "Stack of curved flat sacs with small bubbles budding off", tags=["organelle", "cell biology", "golgi body", "vesicle", "secretion", "cell"], aliases=["golgi-body"])
def _(S):
    return [
        line("M4 7q8-4 16 0"),
        line("M5 12q7-4 14 0"),
        line("M6 17q6-4 12 0"),
        mk(S, 20.5, 18.5, 1.5),
        mk(S, 3.5, 18.5, 1.5),
    ]


@icon("rna-strand", CAT, "Single wavy strand with short bases hanging from it", tags=["ribonucleic acid", "mrna", "genetics", "molecule", "transcription", "biology"])
def _(S):
    parts = [line("M2 8q1.67-5 3.33 0t3.34 0t3.33 0t3.33 0t3.34 0t3.33 0")]
    for x in (7, 13.67, 20.33):
        parts.append(line(seg(x, 10.5, x, 15)))
        parts.append(mk(S, x, 18, 1.5))
    return parts


@icon("dna-replication", CAT, "Double strand unzipping into two arms, each building a new strand", tags=["dna copying", "genetics", "mitosis", "unzipping", "biology", "helix"])
def _(S):
    return [
        line("M9 22C9 18 15 16 15 12C15 9 19 7 19 3"),
        line("M15 22C15 18 9 16 9 12C9 9 5 7 5 3"),
        line(seg(10.7, 19.5, 13.3, 19.5)),
    ]


@icon("plasmid", CAT, "Circular loop of double-stranded DNA with one highlighted segment", tags=["bacteria", "genetic engineering", "circular dna", "vector", "cloning", "biotechnology"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(circle(12, 12, 5)),
        solid(thick(arc(12, 12, 7, -75, -15), 4, S)),
    ]


@icon("gene-editing", CAT, "Scissors cutting a double strand at a gap", tags=["crispr", "genetic engineering", "dna", "genome", "cut", "biotechnology"], aliases=["genome-editing"])
def _(S):
    return [
        shell(circle(7, 4.5, 2)),
        shell(circle(17, 4.5, 2)),
        line(seg(8.2, 6.2, 14, 14)),
        line(seg(15.8, 6.2, 10, 14)),
        line("M2 18q2 5 4 0t4 0"),
        line("M2 18q2-5 4 0t4 0"),
        line("M14 18q2 5 4 0t4 0"),
        line("M14 18q2-5 4 0t4 0"),
    ]


# ============================================================================ microbes and microscopy

@icon("amoeba", CAT, "Irregular cell blob with rounded false-foot lobes and a nucleus dot", tags=["protozoa", "microorganism", "single cell", "pseudopod", "microbe", "biology"])
def _(S):
    body = union(circle(12, 12, 6.2), circle(6.6, 8.2, 3.4), circle(15.5, 5.6, 3.1), circle(18.2, 15, 3.5), circle(9, 18.2, 3.2))
    return [
        shell(body),
        mk(S, 11.5, 11.5, 1.5),
    ]


def _paramecium():
    cx, cy, a, b, ang = 12.0, 12.0, 7.0, 4.0, math.radians(-35)
    ca, sa = math.cos(ang), math.sin(ang)

    def R(x, y):
        return (cx + x * ca - y * sa, cy + x * sa + y * ca)
    ticks = []
    for i in range(8):
        t = math.radians(i * 45 + 22.5)
        px, py = a * math.cos(t), b * math.sin(t)
        nx, ny = math.cos(t) / a, math.sin(t) / b
        ln = math.hypot(nx, ny)
        nx, ny = nx / ln, ny / ln
        p, q = R(px + nx * 0.5, py + ny * 0.5), R(px + nx * 3.2, py + ny * 3.2)
        ticks.append(seg(p[0], p[1], q[0], q[1]))
    return ellipse(0, 0, a, b), ticks, (cx, cy, ang)


@icon("paramecium", CAT, "Slipper-shaped cell fringed with tiny hairs", tags=["ciliate", "protozoa", "microorganism", "cilia", "pond water", "microbe"])
def _(S):
    _, ticks, (cx, cy, ang) = _paramecium()
    body = rot(ellipse(12, 12, 7, 4), -35)
    parts = [shell(body)]
    parts += [line(t) for t in ticks]
    parts.append(mk(S, 12, 12, 1.1))
    return parts


@icon("euglena", CAT, "Teardrop cell with a long whip-like tail at the front and an eyespot", tags=["flagellate", "protist", "microorganism", "flagellum", "algae", "single cell"])
def _(S):
    return [
        shell(rot("M12 9C14 11 17 12.5 17 16A5 5 0 0 1 7 16C7 12.5 10 11 12 9Z", 25, 12, 14)),
        line(rot("M12 9q-2.5-2 0-4t0-3", 25, 12, 14)),
        mk(S, 11.4, 15.4, 1.3),
    ]


@icon("volvox", CAT, "Hollow ball colony of tiny cells with a daughter colony inside", tags=["green algae", "colony", "protist", "microorganism", "freshwater", "sphere"])
def _(S):
    parts = [shell(circle(12, 12, 9)), detail(circle(12, 12, 1.5))]
    for i in range(6):
        x, y = polar(12, 12, 5.6, -90 + i * 60)
        parts.append(mk(S, x, y, 1.0))
    return parts


@icon("stentor", CAT, "Trumpet-shaped cell with a ring of hairs around its wide mouth", tags=["ciliate", "protozoa", "microorganism", "pond life", "trumpet animalcule", "microbe"])
def _(S):
    return [
        line(seg(6, 3, 6, 5.5)),
        line(seg(10, 3, 10, 5.5)),
        line(seg(14, 3, 14, 5.5)),
        line(seg(18, 3, 18, 5.5)),
        shell("M4.5 8Q10.5 10 10.5 15Q10.3 18 11 21H13Q13.7 18 13.5 15Q13.5 10 19.5 8Z"),
    ]


@icon("vorticella", CAT, "Bell-shaped cell with a fringe of hairs on a long coiled stalk", tags=["ciliate", "protozoa", "microorganism", "stalk", "spring", "pond life"])
def _(S):
    return [
        line(seg(8, 2.5, 8, 4)),
        line(seg(12, 2.5, 12, 4)),
        line(seg(16, 2.5, 16, 4)),
        shell("M6 6.5Q6 13 12 13Q18 13 18 6.5Z"),
        line("M12 13V15C16 15 16 20 12 20C9.5 20 9.5 17.3 12 17.3"),
    ]


@icon("foraminifera", CAT, "Round coiled shell of a tiny sea creature with spiral chambers", tags=["forams", "plankton", "microfossil", "shell", "protist", "marine"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail("M12 12a1.7 1.7 0 0 1 3.4 0a3.4 3.4 0 0 1-6.8 0a5.1 5.1 0 0 1 10.2 0"),
    ]


@icon("spirogyra", CAT, "Green algae filament: a tube of cells with a spiral ribbon inside", tags=["algae", "filament", "pond scum", "chloroplast", "freshwater", "microscope"])
def _(S):
    return [
        shell(rect(2, 7, 20, 10, min(S.R, 3))),
        detail("M5 12q2.3-4 4.6 0t4.6 0t4.6 0"),
    ]


@icon("microscope-field-of-view", CAT, "Circular eyepiece view with two cells and a pointer", tags=["microscope view", "specimen", "magnified", "cells", "lens view", "slide"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(circle(9, 10.5, 2.3)),
        detail(circle(14.5, 15, 1.7)),
        line(seg(19, 6, 14.5, 9.5)),
    ]


@icon("pollen-grain", CAT, "Round pollen grain covered in short spikes", tags=["pollen", "allergen", "spore", "flower", "botany", "microscope"])
def _(S):
    parts = [shell(circle(12, 12, 5.5))]
    for i in range(10):
        a = -90 + i * 36
        p, q = polar(12, 12, 6.5, a), polar(12, 12, 9.2, a)
        parts.append(line(seg(p[0], p[1], q[0], q[1])))
    parts.append(mk(S, 12, 12, 1.3))
    return parts


# ============================================================================ ecology and heredity diagrams

@icon("ecological-pyramid", CAT, "Pyramid divided into three feeding levels", tags=["trophic levels", "energy pyramid", "food web", "producers", "consumers", "ecology"], aliases=["trophic-pyramid"])
def _(S):
    return [
        shell(poly([(12, 3), (22, 21), (2, 21)], closed=True, r=S.r)),
        detail(seg(7.5, 13, 16.5, 13)),
        detail(seg(4.7, 17.3, 19.3, 17.3)),
    ]


@icon("phylogenetic-tree", CAT, "Branching family tree diagram with four tips at the same level", tags=["evolution", "cladogram", "species tree", "common ancestor", "taxonomy", "biology"], aliases=["cladogram"])
def _(S):
    return [
        line(poly([(2, 12), (6, 12)], r=0)),
        line(poly([(11, 4.5), (6, 7), (6, 17), (11, 19.5)], r=S.r)),
        line(poly([(21, 4.5), (11, 4.5), (11, 9.5), (21, 9.5)], r=S.r)),
        line(poly([(21, 14.5), (11, 14.5), (11, 19.5), (21, 19.5)], r=S.r)),
        line(seg(6, 7, 11, 7)),
        line(seg(6, 17, 11, 17)),
    ]


@icon("punnett-square", CAT, "Two by two grid with marks along the top and left edges", tags=["genetics", "heredity", "inheritance", "alleles", "cross", "biology class"])
def _(S):
    return [
        shell(rect(8, 8, 13, 13, min(S.R, 2))),
        detail(seg(14.5, 8, 14.5, 21)),
        detail(seg(8, 14.5, 21, 14.5)),
        mk(S, 11.5, 4, 1.2),
        mk(S, 17.5, 4, 1.2),
        mk(S, 4, 11.5, 1.2),
        mk(S, 4, 17.5, 1.2),
    ]


@icon("pedigree-chart", CAT, "Family tree chart of a square and circle with a child square and circle", tags=["family history", "genetics", "inheritance", "genealogy", "heredity", "trait"])
def _(S):
    return [
        shell(rect(3, 3, 6, 6, S.R)),
        shell(circle(17.5, 6, 3)),
        line(seg(9, 6, 14.5, 6)),
        line(poly([(12, 6), (12, 12)], r=0)),
        line(poly([(6, 15), (6, 12), (18, 12), (18, 15)], r=S.r * 1.5)),
        shell(rect(3, 15, 6, 6, S.R)),
        shell(circle(18, 18, 3)),
        solid(circle(18, 18, 1.3)),
    ]


@icon("osmosis", CAT, "U-shaped tube with a membrane across the bottom and the water higher on one side", tags=["diffusion", "membrane", "water movement", "semipermeable", "u-tube", "biology"])
def _(S):
    pts = [(3, 3), (9, 3), (9, 15), (15, 15), (15, 3), (21, 3), (21, 17), (18, 21), (6, 21), (3, 17)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.6)),
        detail(seg(3, 8, 9, 8)),
        detail(seg(15, 12, 21, 12)),
        detail(seg(12, 15, 12, 21)),
    ]


@icon("diffusion", CAT, "Box with crowded dots on the left spreading to the right with an arrow", tags=["spreading", "concentration", "particles", "gradient", "molecules", "chemistry"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, min(S.R, 3))),
        mk(S, 5.5, 8, 1.1),
        mk(S, 5.5, 12, 1.1),
        mk(S, 5.5, 16, 1.1),
        line(poly([(9, 12), (15, 12)], r=0)),
        line(poly([(13, 10), (15, 12), (13, 14)], r=S.r * 0.4)),
        mk(S, 18.5, 9, 1.1),
        mk(S, 18.5, 15, 1.1),
    ]


# ============================================================================ field and lab gear

@icon("dissection-tray", CAT, "Shallow tray with a frog pinned out by its four legs", tags=["dissection", "biology class", "specimen", "frog", "anatomy", "lab"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, min(S.R, 3))),
        detail(ellipse(12, 12, 2.3, 4)),
        detail(poly([(10, 9), (7.5, 7), (6, 7.5)], r=0)),
        detail(poly([(14, 9), (16.5, 7), (18, 7.5)], r=0)),
        detail(poly([(10, 15), (7.5, 17), (6, 16.5)], r=0)),
        detail(poly([(14, 15), (16.5, 17), (18, 16.5)], r=0)),
    ]


@icon("camera-trap", CAT, "Small camera box with a lens strapped to a tree trunk", tags=["trail camera", "wildlife camera", "game camera", "nature", "monitoring", "survey"])
def _(S):
    return [
        shell(rect(2, 6, 13, 12, min(S.R, 3))),
        detail(circle(8, 12, 2.2)),
        mk(S, 12.2, 9.3, 0.9),
        shell(rect(18, 2, 4, 20, min(S.R, 2))),
        line(seg(15, 9, 18, 9)),
        line(seg(15, 15, 18, 15)),
    ]


@icon("tracking-collar", CAT, "Animal collar band with a boxy transmitter and a short antenna", tags=["gps collar", "wildlife tracking", "radio collar", "telemetry", "animal tag", "research"], aliases=["radio-collar"])
def _(S):
    return [
        shell(ellipse(12, 16.5, 9, 4.5)),
        detail(ellipse(12, 16.5, 5.5, 1.3)),
        shell(rect(7, 6, 9, 6, S.R)),
        line(seg(14, 6, 18, 2.5)),
    ]


@icon("plant-press", CAT, "Two boards with straps pressing layers of paper between them", tags=["herbarium", "pressed flowers", "botany", "specimen", "drying plants", "collection"])
def _(S):
    return [
        shell(rect(2, 2.5, 20, 3.5, min(S.R, 1.5))),
        shell(rect(2, 18, 20, 3.5, min(S.R, 1.5))),
        line(seg(4, 10, 20, 10)),
        line(seg(4, 14, 20, 14)),
        line(seg(7, 6, 7, 18)),
        line(seg(17, 6, 17, 18)),
    ]


@icon("plant-tissue-culture", CAT, "Sealed jar with gel at the bottom and a tiny plantlet growing from it", tags=["micropropagation", "plant lab", "in vitro", "seedling", "botany", "agar"], aliases=["tissue-culture"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 3.5, min(S.R, 1.5))),
        shell(rect(5, 6, 14, 15, min(S.R, 4))),
        detail(seg(5, 16, 19, 16)),
        line(seg(12, 16, 12, 9.5)),
        line(seg(12, 13.5, 8.5, 11)),
        line(seg(12, 12, 15.5, 9.5)),
    ]


# ============================================================================ astronomy and weather instruments

@icon("reflecting-telescope", CAT, "Wide tilted telescope tube with a side eyepiece on a tripod", tags=["newtonian telescope", "astronomy", "stargazing", "mirror telescope", "observatory", "space"])
def _(S):
    return [
        shell(rot(rect(7, 2, 10, 12, min(S.R, 2.5)), -25, 12, 14)),
        shell(rot(rect(17, 4, 3.5, 3), -25, 12, 14)),
        line(seg(12, 14, 12, 17)),
        line(poly([(7, 22), (12, 17), (17, 22)], r=S.r * 0.5)),
    ]


def _honeycomb():
    R = 3.6
    w = math.sqrt(3) * R
    centers = [(12, 12)] + [(12 + w * math.cos(math.radians(a)), 12 + w * math.sin(math.radians(a))) for a in range(0, 360, 60)]
    edges = set()
    for cx, cy in centers:
        vs = [polar(cx, cy, R, -90 + 60 * i) for i in range(6)]
        for i in range(6):
            a, b = vs[i], vs[(i + 1) % 6]
            ka = (round(a[0], 2), round(a[1], 2))
            kb = (round(b[0], 2), round(b[1], 2))
            edges.add(tuple(sorted([ka, kb])))
    return "".join("M%s %sL%s %s" % (fmt(a[0]), fmt(a[1]), fmt(b[0]), fmt(b[1])) for a, b in sorted(edges))


@icon("segmented-mirror", CAT, "Honeycomb of seven hexagonal mirror tiles", tags=["telescope mirror", "honeycomb", "hexagon", "observatory", "astronomy", "optics"], aliases=["hexagonal-mirror"])
def _(S):
    return [line(_honeycomb())]


@icon("eclipse-glasses", CAT, "Flat paper viewing glasses with dark lenses under a small crescent sun", tags=["solar eclipse", "sun viewing", "safety glasses", "astronomy", "sun protection", "eclipse viewer"], aliases=["solar-eclipse-glasses"])
def _(S):
    cres = path_to_d(D(P(circle(12, 5.5, 3.6)), P(circle(13.7, 4.3, 3.2))))
    return [
        solid(cres),
        shell(rect(2, 12, 8.5, 8, S.R)),
        shell(rect(13.5, 12, 8.5, 8, S.R)),
        line(seg(10.5, 14, 13.5, 14)),
    ]


@icon("planet-transit", CAT, "Bright star with a small dark planet crossing it and a dip in its light curve below", tags=["exoplanet", "light curve", "astronomy", "star", "kepler", "space"])
def _(S):
    return [
        shell(circle(12, 8, 5.5)),
        dot(12, 8, 2),
        line("M2 17H6.5Q8.5 17 9.5 20.5H14.5Q15.5 17 17.5 17H22"),
    ]


@icon("atomic-timekeeping", CAT, "Clock face with an atom orbit and nucleus behind the hands", tags=["atomic clock", "time standard", "precision time", "cesium", "physics", "clock"], aliases=["atomic-clock"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(rot(ellipse(12, 12, 5.8, 2.2), -35)),
        detail(rot(ellipse(12, 12, 5.8, 2.2), 35)),
        mk(S, 12, 12, 1.6),
        line(seg(12, 4.5, 12, 6)),
        line(seg(12, 18, 12, 19.5)),
    ]


@icon("refractometer", CAT, "Slim handheld tube with an eyepiece at one end and a hinged prism cover at the other", tags=["brix", "sugar meter", "optics", "salinity", "lab tool", "measurement"])
def _(S):
    return [
        shell(rot(rect(9, 7.5, 6, 10, S.R * 0.75), 40)),
        shell(rot(rect(8.5, 2.5, 7, 3.5, S.R * 0.5), 40)),
        line(rot(seg(12, 17.5, 12, 22), 40)),
        detail(rot(seg(10.5, 12.5, 13.5, 12.5), 40)),
    ]


@icon("barometer", CAT, "Round pressure dial with a needle and a row of scale marks", tags=["air pressure", "weather instrument", "aneroid", "forecast", "atmospheric pressure", "meteorology"])
def _(S):
    parts = [shell(circle(12, 12, 9))]
    for i in range(5):
        x, y = polar(12, 12, 5.8, -160 + i * 35)
        parts.append(mk(S, x, y, 0.9))
    parts.append(detail(seg(12, 12, *polar(12, 12, 4.2, -70))))
    return parts


@icon("anemometer", CAT, "Wind speed gauge with cups on a spinning arm above a pole", tags=["wind gauge", "wind speed", "weather station", "meteorology", "cup anemometer", "weather instrument"])
def _(S):
    return [
        shell("M6.5 6A3.8 3.8 0 0 0 6.5 14Z"),
        shell("M20.5 6A3.8 3.8 0 0 0 20.5 14Z"),
        line(seg(6.5, 10, 16.7, 10)),
        line(seg(12, 10, 12, 21)),
        line(seg(8.5, 21, 15.5, 21)),
    ]


@icon("subduction-zone", CAT, "Cross-section of an ocean plate sinking under land beneath a volcano", tags=["tectonic plates", "geology", "earthquake", "volcano", "plate boundary", "earth science"])
def _(S):
    return [
        shell(thick("M3.5 12H7L15 19", 4, S)),
        line(poly([(10, 9), (22, 9)], r=0)),
        line(poly([(14, 9), (17, 3), (20, 9)], r=S.r * 0.6)),
    ]


@icon("continental-drift", CAT, "Two landmasses with matching jagged edges drifting apart", tags=["pangaea", "plate tectonics", "geology", "continents", "earth science", "drifting"])
def _(S):
    return [
        shell(poly([(2, 3.5), (9, 3.5), (10.5, 7.5), (8.5, 10.5), (10.5, 13.5), (8, 16), (2, 16)], closed=True, r=S.r * 0.5)),
        shell(poly([(22, 3.5), (15, 3.5), (16.5, 7.5), (14.5, 10.5), (16.5, 13.5), (14, 16), (22, 16)], closed=True, r=S.r * 0.5)),
        line(poly([(8, 20), (3, 20)], r=0)),
        line(poly([(5, 18), (3, 20), (5, 22)], r=S.r * 0.4)),
        line(poly([(16, 20), (21, 20)], r=0)),
        line(poly([(19, 18), (21, 20), (19, 22)], r=S.r * 0.4)),
    ]


@icon("aquifer", CAT, "Block of ground with a wavy water layer and a well pipe reaching down into it", tags=["groundwater", "water table", "well", "hydrology", "geology", "underground water"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, min(S.R, 3))),
        detail("M2 13q2.5-2 5 0t5 0t5 0t5 0"),
        detail(poly([(9, 3), (9, 17.5), (15, 17.5), (15, 3)], r=S.r * 0.5)),
    ]


# ============================================================================ batch 3b: lab glassware, field and chemistry

def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def tube(x1, y1, x2, y2, w):
    return thick(seg(x1, y1, x2, y2), w, type("St", (), {"cap": "butt", "join": "miter"})())


@icon("karyotype", CAT, "Grid of paired chromosomes laid out in two rows", tags=["chromosomes", "genetics", "cytogenetics", "genome", "chromosome map", "biology"])
def _(S):
    parts = []
    for y in (7, 17):
        for x in (5, 12, 19):
            parts.append(line(seg(x - 2.2, y - 3, x + 2.2, y + 3)))
            parts.append(line(seg(x + 2.2, y - 3, x - 2.2, y + 3)))
    return parts


@icon("bird-band", CAT, "Bird leg with a ring fitted around it and a three-toed foot", tags=["bird ring", "ornithology", "leg band", "bird tracking", "banding", "wildlife research"])
def _(S):
    return [
        line(seg(12, 2, 12, 7)),
        shell(rect(8, 7, 8, 5.5, min(S.R, 2))),
        line(seg(12, 12.5, 12, 16.5)),
        line(poly([(5.5, 21), (12, 16.5), (18.5, 21)], r=S.r * 0.6)),
        line(seg(12, 16.5, 12, 21.5)),
    ]


@icon("rock-tumbler", CAT, "Barrel lying on two rollers with polished stones inside", tags=["rock polishing", "lapidary", "gem polishing", "stones", "hobby", "geology"])
def _(S):
    return [
        shell(rect(2, 3, 20, 10, min(S.R, 4))),
        detail(seg(6.5, 3, 6.5, 13)),
        detail(seg(17.5, 3, 17.5, 13)),
        mk(S, 10.5, 8, 1.2),
        mk(S, 14, 8.6, 1.2),
        shell(circle(7, 18, 2.5)) if S.name == "rounded" else shell(rect(4.5, 15.5, 5, 5, 1)),
        shell(circle(17, 18, 2.5)) if S.name == "rounded" else shell(rect(14.5, 15.5, 5, 5, 1)),
    ]


@icon("magnetosphere", CAT, "Planet with bow-shaped field lines on the sun side and stretched field lines trailing behind", tags=["earth magnetic field", "geomagnetic", "solar wind", "space weather", "aurora", "planet"])
def _(S):
    planet = poly(regular(11, 12, 3.4, 8, -90 + 22.5), closed=True) if S.name == "line" else circle(11, 12, 3.2)
    return [
        shell(planet),
        line(arc(11, 12, 6.5, 145, 215)),
        line(arc(11, 12, 10, 150, 210)),
        line("M14.5 10Q18 7.5 22 7.5"),
        line("M14.5 14Q18 16.5 22 16.5"),
    ]


@icon("three-neck-flask", CAT, "Round-bottom flask with three necks, one upright and two angled outward", tags=["round bottom flask", "chemistry glassware", "reflux", "lab", "synthesis", "triple neck"])
def _(S):
    st = type("St", (), {"cap": "butt", "join": "miter"})()
    body = circle(12, 15.5, 5.8)
    necks = [thick(seg(12, 15.5, 12, 3), 3.4, st), thick(seg(12, 15.5, 4.9, 7.1), 3.4, st), thick(seg(12, 15.5, 19.1, 7.1), 3.4, st)]
    return [shell(union(body, *necks)), detail(seg(8, 18, 16, 18))]


@icon("soxhlet-extractor", CAT, "Extraction chamber with a side arm tube, sitting on a round flask", tags=["extraction", "chemistry glassware", "solvent", "reflux", "lab apparatus", "organic chemistry"])
def _(S):
    shape = union(rect(7.5, 2.5, 9, 9, 1), rect(10.5, 11, 3, 4), circle(12, 18.5, 3.6))
    return [
        shell(shape),
        detail(seg(7.5, 7, 16.5, 7)),
        line(poly([(16.5, 5), (20, 5), (20, 19), (15.6, 19)], r=S.r * 0.6)),
    ]


@icon("heating-mantle", CAT, "Bowl-shaped heater cradling the base of a round flask, with a control knob", tags=["lab heater", "flask heater", "chemistry", "heating", "glassware", "reflux"])
def _(S):
    st = type("St", (), {"cap": "butt", "join": "miter"})()
    flask = union(circle(12, 9, 5.5), rect(10, 2, 4, 5))
    bowl = poly([(3.5, 13), (20.5, 13), (19, 19), (15.5, 21.5), (8.5, 21.5), (5, 19)], closed=True, r=S.r)
    return [
        shell(union(flask, bowl)),
        detail(seg(5, 13, 19, 13)),
        mk(S, 12, 17.5, 1.3),
    ]


@icon("ice-bath", CAT, "Beaker standing in a bowl of ice cubes", tags=["cooling", "cold bath", "chemistry", "lab", "chill", "ice water"])
def _(S):
    return [
        line(poly([(9, 14), (9, 3), (15, 3), (15, 14)], r=S.r * 0.4)),
        shell(poly([(2.5, 14.5), (21.5, 14.5), (19, 21.5), (5, 21.5)], closed=True, r=S.r)),
        shell(rot(rect(2.5, 8.5, 4.5, 4.5, min(S.R, 1)), -12, 4.75, 10.75)),
        shell(rot(rect(17, 8.5, 4.5, 4.5, min(S.R, 1)), 12, 19.25, 10.75)),
    ]


@icon("pipette-bulb", CAT, "Round rubber bulb with valve nubs on each side, fitted to a glass pipette", tags=["pipette filler", "pipette controller", "propipette", "lab pipetting", "chemistry", "suction bulb"])
def _(S):
    return [
        shell(circle(12, 7.5, 5.5)),
        shell(rect(9.5, 13.5, 5, 3.5, min(S.R, 1))),
        shell(circle(5.5, 15.2, 2.2)) if S.name == "rounded" else shell(rect(3.5, 14, 4.5, 2.5)),
        shell(circle(18.5, 15.2, 2.2)) if S.name == "rounded" else shell(rect(16, 14, 4.5, 2.5)),
        shell(poly([(10.5, 17), (13.5, 17), (13.5, 19), (12.5, 21), (11.5, 21), (10.5, 19)], closed=True, r=0)),
    ]


@icon("lab-bench", CAT, "Workbench with a flask and a beaker standing on the countertop", tags=["laboratory", "work surface", "counter", "science class", "workstation", "chemistry"])
def _(S):
    return [
        shell(poly([(5.5, 3), (9.5, 3), (9.5, 7), (12.5, 12.5), (2.5, 12.5), (5.5, 7)], closed=True, r=S.r * 0.6)),
        shell(rect(14, 6, 6.5, 6.5, min(S.R, 1.5))),
        shell(rect(2, 12.5, 20, 3.5, min(S.R, 1.5))),
        line(seg(4.5, 16, 4.5, 21)),
        line(seg(19.5, 16, 19.5, 21)),
        line(seg(4.5, 19, 19.5, 19)),
    ]


@icon("fractionating-column", CAT, "Vertical glass column with notched sides, a thermometer at the top and a side arm", tags=["distillation", "chemistry glassware", "separation", "vigreux", "lab apparatus", "organic chemistry"])
def _(S):
    pts = [(8, 5), (16, 5), (16, 11), (13.5, 12.5), (16, 14), (16, 18.5), (13.5, 20), (16, 21.5), (8, 21.5), (10.5, 20), (8, 18.5), (8, 14), (10.5, 12.5), (8, 11)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        detail(seg(12, 2, 12, 9)),
        line(poly([(16, 7), (20.5, 7), (20.5, 12)], r=S.r * 0.6)),
    ]

# ============================================================================ batch 3c

def flame_d(cx, by, h=8.0, w=6.0):
    top = by - h
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + w * 0.15)} {fmt(top + h * 0.3)} {fmt(cx + w / 2)} {fmt(by - h * 0.45)} "
            f"{fmt(cx + w / 2)} {fmt(by - h * 0.2)}C{fmt(cx + w / 2)} {fmt(by + h * 0.02)} {fmt(cx + w * 0.25)} {fmt(by)} {fmt(cx)} {fmt(by)}"
            f"C{fmt(cx - w * 0.25)} {fmt(by)} {fmt(cx - w / 2)} {fmt(by + h * 0.02)} {fmt(cx - w / 2)} {fmt(by - h * 0.2)}"
            f"C{fmt(cx - w / 2)} {fmt(by - h * 0.45)} {fmt(cx - w * 0.15)} {fmt(top + h * 0.3)} {fmt(cx)} {fmt(top)}Z")


def rr(S, cap):
    """Container radius: small in Line, softened up to cap in Rounded."""
    return min(S.R, cap) if S.name == "rounded" else min(S.R, cap) * 0.3


def atom(S, cx, cy, r):
    """Atom ball outline: octagon in Line, circle in Rounded."""
    if S.name == "rounded":
        return circle(cx, cy, r)
    return poly(regular(cx, cy, r * 1.08, 8, -90 + 22.5), closed=True)


def hazard_tri(S):
    return shell(poly([(12, 3), (22, 20.5), (2, 20.5)], closed=True, r=S.r * 1.2))


@icon("gas-syringe", CAT, "Horizontal glass syringe with scale ticks and its plunger pushed out", tags=["gas volume", "measuring gas", "chemistry", "lab", "plunger", "glassware"])
def _(S):
    return [
        shell(rect(7, 8, 12, 8, min(S.R, 2))),
        detail(seg(11, 8, 11, 16)),
        detail(seg(14, 8, 14, 11)),
        detail(seg(16.5, 8, 16.5, 11)),
        line(seg(2.5, 12, 11, 12)),
        line(seg(2.5, 8.5, 2.5, 15.5)),
        line(seg(19, 12, 22, 12)),
    ]


@icon("gas-collection-trough", CAT, "Water trough with an upturned jar filling with gas bubbles", tags=["pneumatic trough", "collecting gas", "chemistry experiment", "water displacement", "lab", "bubbles"])
def _(S):
    return [
        line(poly([(2, 11), (2, 21), (22, 21), (22, 11)], r=S.r)),
        line("M2 11q2.5-2 5 0t5 0t5 0t5 0"),
        line(poly([(6.5, 17), (6.5, 5), (8.5, 3), (15.5, 3), (17.5, 5), (17.5, 17)], r=S.r * 0.7)),
        mk(S, 12, 14.5, 1.1),
        mk(S, 12, 6.5, 1.1),
    ]


@icon("mass-spectrometer", CAT, "Two curved ion paths of different radius bending through a magnet toward a detector line", tags=["mass spec", "ions", "analytical chemistry", "isotopes", "detector", "magnetic sector"])
def _(S):
    return [
        line("M3 18A9 9 0 0 1 21 18"),
        line("M3 18A4.5 4.5 0 0 1 12 18"),
        line(seg(2, 21, 22, 21)),
        mk(S, 16.5, 16, 1.1),
        mk(S, 16.5, 11.5, 1.1),
    ]


def _diffraction_filled():
    dots = [P(circle(12, 12, 2.1))]
    for i in range(8):
        x, y = polar(12, 12, 5.2, -90 + i * 45)
        dots.append(P(circle(x, y, 1.25)))
    for i in range(12):
        x, y = polar(12, 12, 9, -90 + i * 30 + 15)
        dots.append(P(circle(x, y, 1.25)))
    return U(*dots)


@icon("diffraction-pattern", CAT, "Bright central spot ringed by dots in concentric circles", tags=["x-ray diffraction", "electron diffraction", "crystal", "optics", "physics", "wave interference"], filled=_diffraction_filled)
def _(S):
    parts = [mk(S, 12, 12, 1.9)]
    for i in range(8):
        x, y = polar(12, 12, 5.2, -90 + i * 45)
        parts.append(mk(S, x, y, 1.0))
    for i in range(12):
        x, y = polar(12, 12, 9, -90 + i * 30 + 15)
        parts.append(mk(S, x, y, 1.0))
    return parts


@icon("lab-jack", CAT, "Small platform on a scissor lift with a screw knob at the side", tags=["scissor jack", "lift table", "support stand", "height adjustment", "laboratory", "equipment"], aliases=["scissor-lab-jack"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 3.5, min(S.R, 1.5))),
        shell(rect(3, 18, 18, 3.5, min(S.R, 1.5))),
        line(poly([(7, 6), (17, 18)], r=0)),
        line(poly([(17, 6), (7, 18)], r=0)),
        line(seg(3, 12, 17, 12)),
        shell(rect(18, 9.5, 3.5, 5, min(S.R, 1.5))),
    ]


@icon("flint-striker", CAT, "Spring-handled lighter with a cup holding a flint and sparks flying", tags=["lab lighter", "bunsen lighter", "spark lighter", "ignite", "friction lighter", "chemistry"])
def _(S):
    return [
        line(poly([(6.5, 22), (10.5, 14)], r=0)),
        line(poly([(17.5, 22), (13.5, 14)], r=0)),
        shell(poly([(7.5, 7), (16.5, 7), (14, 14), (10, 14)], closed=True, r=S.r * 0.6)),
        detail(seg(9.5, 10.5, 14.5, 10.5)),
        line(seg(12, 4.5, 12, 2)),
        line(seg(7.5, 4.8, 5.5, 3)),
        line(seg(16.5, 4.8, 18.5, 3)),
    ]


@icon("overhead-stirrer", CAT, "Motor head on a stand with a long shaft and paddle reaching into a beaker", tags=["mechanical stirrer", "mixing", "paddle", "chemistry lab", "agitator", "beaker"])
def _(S):
    return [
        line(seg(3, 2, 3, 22)),
        line(seg(3, 4.5, 8, 4.5)),
        shell(rect(8, 2, 8, 5, min(S.R, 1.5))),
        line(seg(12, 7, 12, 18)),
        line(seg(8.5, 18, 15.5, 18)),
        line(poly([(6.5, 11), (6.5, 22), (17.5, 22), (17.5, 11)], r=S.r * 0.6)),
    ]


@icon("vacuum-pump", CAT, "Boxy motor pump with a cooling grille and a hose connector on top", tags=["lab pump", "suction", "air pump", "vacuum", "chemistry", "equipment"])
def _(S):
    return [
        shell(rect(3, 10, 18, 11, min(S.R, 3))),
        detail(seg(7, 13, 7, 18)),
        detail(seg(10.5, 13, 10.5, 18)),
        detail(seg(14, 13, 14, 18)),
        shell(rect(15, 4.5, 4, 5.5, min(S.R, 1))) if False else line(seg(17, 10, 17, 4.5)),
        line(seg(17, 4.5, 21.5, 4.5)),
        mk(S, 18.2, 15.5, 1.1),
    ]


@icon("ultra-low-freezer", CAT, "Upright lab freezer with a digital display and a snowflake on its door", tags=["-80 freezer", "cold storage", "laboratory", "sample storage", "biobank", "cryo"], aliases=["minus-80-freezer"])
def _(S):
    return [
        shell(rect(3, 2, 15, 20, min(S.R, 3))),
        Part("dot", rect(6, 5, 9, 2.5)),
        detail(seg(10.5, 10.5, 10.5, 18.5)),
        detail(seg(7.2, 12.5, 13.8, 16.5)),
        detail(seg(13.8, 12.5, 7.2, 16.5)),
        line(seg(20.5, 9, 20.5, 15)),
    ]


@icon("pipette-tip-box", CAT, "Box holding rows of cone-shaped pipette tips standing upright", tags=["tip rack", "micropipette", "disposable tips", "lab consumables", "pipetting", "biology lab"])
def _(S):
    parts = [shell(rect(2.5, 12, 19, 9.5, min(S.R, 2.5)))]
    for x in (5.5, 9.8, 14.2, 18.5):
        parts.append(solid(poly([(x - 1.5, 3), (x + 1.5, 3), (x + 0.7, 10.5), (x - 0.7, 10.5)], closed=True)))
    parts.append(detail(seg(5, 16.7, 19, 16.7)))
    return parts


@icon("weighing-boat", CAT, "Small dish with sloped sides holding a heap of powder", tags=["weigh boat", "balance", "powder", "chemistry lab", "scale", "measuring"])
def _(S):
    return [
        line("M7 12C9 6 15 6 17 12"),
        shell(poly([(2, 12), (22, 12), (18.5, 20.5), (5.5, 20.5)], closed=True, r=S.r)),
        mk(S, 12, 16.2, 0.8) if False else detail(seg(9, 16, 15, 16)),
    ]


@icon("gas-jar", CAT, "Tall glass jar with a flat glass disc resting over its mouth", tags=["gas collection", "chemistry", "glassware", "cover slip", "lab", "experiment"])
def _(S):
    return [
        shell(rect(3.5, 3, 17, 3, min(S.R, 1))),
        shell(rect(6, 8, 12, 13.5, min(S.R, 3))) if False else shell(poly([(7, 6), (17, 6), (17, 19), (15.5, 21.5), (8.5, 21.5), (7, 19)], closed=True, r=S.r)),
        mk(S, 12, 12, 1.2),
        mk(S, 12, 16.5, 1.2),
    ]


@icon("deflagrating-spoon", CAT, "Long rod with a small cup at the bottom and a round cover disc partway up", tags=["combustion spoon", "burning", "chemistry experiment", "lab tool", "flame test", "sample"])
def _(S):
    return [
        line(seg(12, 2, 12, 17)),
        shell(rect(6.5, 7.5, 11, 2.5, min(S.R, 1.2))),
        shell("M7.5 17H16.5A4.5 4.5 0 0 1 7.5 17Z") if S.name == "rounded" else shell(poly([(7.5, 17), (16.5, 17), (14, 21.5), (10, 21.5)], closed=True)),
    ]


@icon("clay-triangle", CAT, "Wire triangle with three ceramic sleeves on its sides and twisted ends sticking out", tags=["pipe clay triangle", "crucible support", "bunsen burner", "heating", "chemistry lab", "ring stand"])
def _(S):
    return [
        line(poly([(12, 3.5), (21, 20), (3, 20)], closed=True, r=S.r)),
        solid(thick(seg(9.1, 8.7, 6.4, 13.7), 4.4, S)),
        solid(thick(seg(14.9, 8.7, 17.6, 13.7), 4.4, S)),
        solid(thick(seg(8.5, 20, 15.5, 20), 4.4, S)),
        line(seg(21, 20, 22, 22)) if False else line(seg(12, 3.5, 12, 1.8)),
    ]


@icon("flammables-cabinet", CAT, "Squat safety cabinet with double doors and a flame mark on the front", tags=["flammable storage", "safety cabinet", "fire safety", "chemical storage", "lab safety", "hazmat"], aliases=["flammable-cabinet"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, min(S.R, 2.5))),
        detail(seg(12, 14, 12, 21)),
        Part("dot", flame_d(12, 12.5, 7.5, 5.5)),
        line(seg(5, 21.5, 5, 22)) if False else line(seg(6, 21, 6, 22)),
        line(seg(18, 21, 18, 22)),
    ]


@icon("safety-data-sheet", CAT, "Document page with a hazard diamond in the top corner and lines of numbered sections", tags=["sds", "msds", "chemical safety", "hazard information", "compliance", "lab safety"], aliases=["sds"])
def _(S):
    return [
        shell(rect(4, 2, 16, 20, min(S.R, 3))),
        detail(poly(regular(9.5, 8, 3.2, 4), closed=True)),
        detail(seg(14.5, 7, 17, 7)),
        detail(seg(7, 15, 17, 15)),
        detail(seg(7, 18.5, 14, 18.5)),
    ]


@icon("magnetic-field-hazard", CAT, "Warning triangle with a horseshoe magnet inside", tags=["magnet warning", "strong magnetic field", "pacemaker warning", "safety sign", "mri", "caution"])
def _(S):
    return [
        hazard_tri(S),
        detail("M9.5 17.5V14.5A2.5 2.5 0 0 1 14.5 14.5V17.5"),
    ]


@icon("cryogenic-hazard", CAT, "Warning triangle with a snowflake inside", tags=["extreme cold", "frostbite", "liquid nitrogen", "safety sign", "caution", "cold hazard"])
def _(S):
    parts = [hazard_tri(S)]
    for a in (90, 30, 150):
        p, q = polar(12, 14, 3.4, a), polar(12, 14, -3.4, a)
        parts.append(detail(seg(p[0], p[1], q[0], q[1])))
    return parts


@icon("hot-surface-hazard", CAT, "Warning triangle with wavy heat lines rising over a flat surface", tags=["burn risk", "hot plate", "heat warning", "safety sign", "caution", "high temperature"])
def _(S):
    return [
        hazard_tri(S),
        detail("M10.2 8.5q-1 1.4 0 2.8t0 2.2"),
        detail("M13.8 8.5q-1 1.4 0 2.8t0 2.2"),
        detail(seg(8.5, 17, 15.5, 17)),
    ]


@icon("eye-protection-sign", CAT, "Round sign showing a pair of safety goggles", tags=["goggles required", "safety glasses", "ppe", "lab safety", "mandatory sign", "eye safety"])
def _(S):
    k = 0.5 if S.name == "line" else 2.2
    return [
        shell(circle(12, 12, 9)),
        Part("dot", rect(5.5, 9.5, 5.5, 4.5, k)),
        Part("dot", rect(13, 9.5, 5.5, 4.5, k)),
        Part("dot", rect(11, 10.8, 2, 1.6)),
    ]


@icon("micelle", CAT, "Ring of round heads with tails pointing inward to the centre", tags=["surfactant", "soap", "detergent", "amphiphile", "colloid", "chemistry"])
def _(S):
    parts = []
    for i in range(8):
        a = -90 + i * 45
        x, y = polar(12, 12, 8, a)
        parts.append(mk(S, x, y, 1.7))
        p, q = polar(12, 12, 6.2, a), polar(12, 12, 2.8, a)
        parts.append(line(seg(p[0], p[1], q[0], q[1])))
    return parts


@icon("oxygen-molecule", CAT, "Two equal atoms joined by a double bond", tags=["o2", "diatomic", "gas", "molecule", "chemistry", "double bond"])
def _(S):
    return [
        shell(atom(S, 6.5, 12, 3.6)),
        shell(atom(S, 17.5, 12, 3.6)),
        line(seg(10.9, 10.4, 13.1, 10.4)),
        line(seg(10.9, 13.6, 13.1, 13.6)),
    ]


@icon("caffeine-molecule", CAT, "Skeletal formula of a hexagon fused to a pentagon with short side bonds ending in oxygen marks", tags=["coffee", "stimulant", "chemical structure", "organic chemistry", "xanthine", "molecule"])
def _(S):
    cx, cy, R = 13.5, 12, 4.2
    hexv = [polar(cx, cy, R, -90 + 60 * i) for i in range(6)]
    # pentagon on the left, sharing the vertical edge hexv[5]-hexv[4]
    a, b = hexv[4], hexv[5]  # (left lower?) positions: i=4 -> 150 deg(-90+240), i=5 -> 210 deg(-90+300)
    ex, ey = (b[0] - a[0]), (b[1] - a[1])
    s_len = math.hypot(ex, ey)
    pent = [a, b]
    # build pentagon outward (to the left) from the shared edge
    ang = math.atan2(ey, ex)
    p = b
    for k in range(3):
        ang -= math.radians(72)
        p = (p[0] + s_len * math.cos(ang), p[1] + s_len * math.sin(ang))
        pent.append(p)
    hx = poly(hexv, closed=True, r=S.r * 0.4)
    px = poly(pent, closed=True, r=S.r * 0.4)
    parts = [shell(union(hx, px))]
    parts.append(detail(seg(a[0], a[1], b[0], b[1])))
    for i, tip in ((1, 2.8), (2, 2.8)):
        v = hexv[i]
        dx, dy = v[0] - cx, v[1] - cy
        n = math.hypot(dx, dy)
        e = (v[0] + dx / n * 3.0, v[1] + dy / n * 3.0)
        parts.append(line(seg(v[0] + dx / n * 1.0, v[1] + dy / n * 1.0, e[0], e[1])))
        parts.append(mk(S, e[0] + dx / n * 0.6, e[1] + dy / n * 0.6, 1.2))
    return parts


@icon("amino-acid", CAT, "Central carbon bonded to an amine group, a carboxyl group and a side chain", tags=["protein building block", "peptide", "biochemistry", "molecule", "alpha carbon", "organic chemistry"])
def _(S):
    return [
        line(seg(12, 12, 6.5, 7)),
        line(seg(12, 12, 17.5, 7)),
        line(seg(12, 12, 12, 17.5)),
        mk(S, 12, 12, 1.6),
        shell(atom(S, 5.5, 5.5, 2.6)),
        shell(atom(S, 18.5, 5.5, 2.6)),
        shell(rect(8.8, 17.5, 6.4, 4.3, rr(S, 2))),
    ]


@icon("nucleotide", CAT, "Five-sided sugar ring with a phosphate circle on one side and a rectangular base on the other", tags=["dna building block", "genetics", "phosphate", "sugar", "base", "molecule"])
def _(S):
    return [
        shell(poly(regular(12, 12, 4.2, 5), closed=True, r=S.r * 0.6)),
        line(seg(8.2, 11, 7.2, 11)),
        shell(atom(S, 4.3, 11, 2.3)),
        line(seg(15.9, 11, 17, 11)),
        shell(rect(17, 7.5, 5, 7, rr(S, 1.5))),
    ]


@icon("activation-energy", CAT, "Energy curve rising over a hump and dropping, with an arrow showing the height of the hump", tags=["reaction rate", "energy barrier", "transition state", "chemical kinetics", "catalyst", "chemistry"])
def _(S):
    return [
        line(poly([(3, 3), (3, 21), (21, 21)], r=S.r * 0.6)),
        line("M5.5 17H9C12 17 11.5 5.5 14 5.5C17 5.5 16 19 21 19") if False else line("M6 17H9C11.5 17 11 5.5 14 5.5C17 5.5 16.5 19 21 19"),
        line(seg(6.5, 17, 6.5, 6)) if False else line(seg(6.5, 16, 6.5, 6.5)),
        line(poly([(4.5, 8.5), (6.5, 6.5), (8.5, 8.5)], r=S.r * 0.4)),
    ]
