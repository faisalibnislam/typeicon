"""TypeIcon Core: science (batch science_005).

Astronomy concepts, bench instruments, field and earth-science kit, lab glassware, physics demos,
circuits, molecular biology, microscopic life and small classroom experiments. Drawn from the objects
and textbook diagrams themselves.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "science"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def sdot(d):
    """Solid glyph: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def arrow_head(tip, deg, size=2.0):
    """Open arrowhead at `tip` pointing along `deg` (0 = right, 90 = down)."""
    a = polar(tip[0], tip[1], size * 1.414, deg + 135)
    b = polar(tip[0], tip[1], size * 1.414, deg - 135)
    return poly([a, tip, b])


def arrow(x1, y1, x2, y2, size=2.0):
    """Line with an open arrowhead at (x2, y2)."""
    deg = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return seg(x1, y1, x2, y2) + arrow_head((x2, y2), deg, size)


def sine(x0, x1, y, amp, cycles, steps=10, phase=0.0):
    n = int(cycles * steps)
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append((x0 + (x1 - x0) * t, y - amp * math.sin(2 * math.pi * cycles * t + phase)))
    return pts


def pts_d(pts, closed=False):
    d = "".join(("M" if i == 0 else "L") + f"{fmt(x)} {fmt(y)}" for i, (x, y) in enumerate(pts))
    return d + ("Z" if closed else "")


def smooth(pts):
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    n = len(pts)
    for i in range(n - 1):
        p0 = pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d


def wave_h(x0, x1, y, amp=1.2, n=2):
    """Horizontal wavy line with n half waves."""
    w = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        s = -amp if i % 2 == 0 else amp
        d += f"C{fmt(x0 + w * (i + 0.25))} {fmt(y + s)} {fmt(x0 + w * (i + 0.75))} {fmt(y + s)} {fmt(x0 + w * (i + 1))} {fmt(y)}"
    return d


def star_pts(cx, cy, ro, ri, n, start=-90.0):
    return [polar(cx, cy, ro if i % 2 == 0 else ri, start + i * 180 / n) for i in range(2 * n)]


def ring(cx, cy, r, S, lo=None):
    """Circle outline as a shell."""
    return shell(circle(cx, cy, r))


def rpts(pts, deg, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rotd(d, deg, cx=12.0, cy=12.0):
    """Rotate a closed shape's path data clockwise about (cx, cy)."""
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def glyph(d, w=1.4):
    """Thin solid letter or symbol drawn from stroke data: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", path_to_d(ST(d, w, "butt", "miter", 4.0)))


def dashed_ellipse(cx, cy, rx, ry, n=8, fill=0.55, start=0.0):
    """Dashed ellipse as one path made of short polylines."""
    d = ""
    for i in range(n):
        a0 = start + i * 360 / n
        a1 = a0 + fill * 360 / n
        pts = [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * k / 3)),
                cy + ry * math.sin(math.radians(a0 + (a1 - a0) * k / 3))) for k in range(4)]
        d += "".join(("M" if j == 0 else "L") + f"{fmt(x)} {fmt(y)}" for j, (x, y) in enumerate(pts))
    return d


# ============================================================================ astronomy, instruments, earth science

@icon("lagrange-points", CAT, "Large body and a small orbiting body with five marked points around them",
      tags=["lagrange", "orbit", "l1", "l2", "equilibrium", "astronomy", "space"])
def _(S):
    return [shell(circle(8, 12, 2.4)), line(arc(8, 12, 9, -28, 28)), sdot(circle(17, 12, 1.5)),
            dot(13, 12, 1), dot(21, 12, 1), dot(3, 12, 1), dot(12.5, 4.5, 1), dot(12.5, 19.5, 1)]


@icon("redshift", CAT, "Spectrum band with dark lines and an arrow showing them shifted to one side",
      tags=["spectrum", "doppler", "astronomy", "galaxy", "wavelength", "cosmology"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 9, S.R * 0.5)),
            detail(seg(7, 3.5, 7, 12.5)), detail(seg(11, 3.5, 11, 12.5)), detail(seg(15, 3.5, 15, 12.5)),
            line(arrow(5, 18.5, 19, 18.5, 2.2))]


@icon("stellar-parallax", CAT, "Near star seen along two sight lines from opposite ends of a baseline against far stars",
      tags=["parallax", "distance", "astronomy", "star", "measurement", "triangulation"])
def _(S):
    return [line(seg(5.5, 20, 18.5, 20)), dot(3.5, 20, 1.5), dot(20.5, 20, 1.5),
            line(seg(4.3, 18, 10.3, 11.6)), line(seg(19.7, 18, 13.7, 11.6)),
            solid(poly(star_pts(12, 9, 3.4, 1.4, 4), closed=True)),
            dot(4.5, 3.5, 1.1), dot(19.5, 3.5, 1.1), dot(12, 2.5, 0.9)]


@icon("cosmic-background-map", CAT, "Oval sky map filled with mottled blotches",
      tags=["cmb", "microwave background", "big bang", "cosmology", "sky map", "all-sky"])
def _(S):
    oval = L(S, "M2 12Q12 2.5 22 12Q12 21.5 2 12Z", ellipse(12, 12, 10, 7))
    return [shell(oval), sdot(circle(9, 10.5, 1.4)), sdot(circle(14.5, 9.5, 1.2)), sdot(circle(15.5, 14, 1.4)),
            sdot(circle(9.5, 14.5, 1.1)), sdot(circle(12, 12, 0.9))]


def dish(vx, vy, R, th=-50, span=60):
    """Shallow dish bowl whose back vertex is at (vx, vy) and whose open side faces `th`."""
    c = polar(vx, vy, R, th)
    bowl = arc(c[0], c[1], R, th + 180 - span, th + 180 + span) + "Z"
    return bowl, polar(vx, vy, R * 0.55, th), polar(vx, vy, R * 1.15, th)


@icon("radio-telescope-array", CAT, "One large and two small dish antennas pointing at the sky",
      tags=["radio astronomy", "dish", "antenna array", "telescope", "observatory", "interferometer"])
def _(S):
    parts = []
    for vx, vy, R, post in ((7, 14, 6, 21), (16.5, 17.5, 3.4, 21), (19.5, 8, 2.4, None)):
        bowl, a, b = dish(vx, vy, R, span=62)
        parts += [shell(bowl), dot(*b, 0.9)]
        if post:
            parts.append(line(seg(vx, vy, vx, post)))
    return parts


@icon("min-max-thermometer", CAT, "U-shaped thermometer with a bulb on each arm and a marker pin in each tube",
      tags=["thermometer", "temperature", "minimum maximum", "weather", "greenhouse", "u-tube"])
def _(S):
    return [shell(circle(6.5, 5.2, 2.4)), shell(circle(17.5, 5.2, 2.4)),
            line("M6.5 7.6V16a5.5 5.5 0 0 0 11 0V7.6"),
            line(seg(4, 11, 9, 11)), line(seg(15, 14, 20, 14))]


@icon("data-logger", CAT, "Small box with a screen showing a line graph and a probe on a cable",
      tags=["sensor", "recorder", "measurement", "science lab", "probe", "graph"])
def _(S):
    return [shell(rect(2.5, 5, 13, 14, S.R)),
            detail(poly([(5.5, 14), (8, 11), (10, 13), (13, 9)], r=S.r)),
            line("M15.5 16c3 0 3-3 3-6s0-2.5 1.5-4.5")]


@icon("function-generator", CAT, "Bench instrument with a sine wave on its screen, wave buttons and a knob",
      tags=["signal generator", "waveform", "electronics", "oscilloscope", "bench", "sine wave"])
def _(S):
    return [shell(rect(2, 4, 20, 16, S.R)),
            detail(smooth(sine(4.5, 12.5, 9, 1.8, 1, 8))),
            dot(5.5, 16, 1), dot(8.5, 16, 1), dot(11.5, 16, 1),
            detail(circle(17.5, 12.5, 2.2))]


@icon("bench-power-supply", CAT, "Box instrument with two digital readouts, a knob and red and black terminals",
      tags=["power supply", "dc supply", "electronics", "bench", "voltage", "terminals"])
def _(S):
    return [shell(rect(2, 4, 20, 16, S.R)),
            detail(rect(4.5, 7, 6, 3.5, 0)), detail(rect(13.5, 7, 6, 3.5, 0)),
            dot(6, 16, 1.4), dot(11, 16, 1.4), detail(circle(17, 16, 1.6))]


@icon("sunshine-recorder", CAT, "Glass ball in a curved bracket focusing a sunbeam onto a card",
      tags=["campbell stokes", "sunshine", "weather station", "meteorology", "glass sphere", "sun hours"])
def _(S):
    return [shell(circle(12, 9, 4.2)), line(arc(12, 9, 9, 25, 155)),
            line(seg(2.5, 2.5, 7, 6)), line(seg(21.5, 2.5, 17, 6))]


@icon("stevenson-screen", CAT, "Louvered white weather box on four legs",
      tags=["weather station", "meteorology", "thermometer shelter", "louvers", "instrument shelter", "temperature"])
def _(S):
    return [shell(poly([(2, 6), (4.5, 2.5), (19.5, 2.5), (22, 6)], closed=True, r=S.r * 0.5)),
            shell(rect(4, 6, 16, 9.5, S.R * 0.5)),
            detail(seg(4, 10.7, 20, 10.7)),
            line(seg(6.5, 15.5, 6.5, 22)), line(seg(17.5, 15.5, 17.5, 22))]


@icon("aquifer-well", CAT, "Ground cross-section with a water-bearing layer and a well pipe reaching into it",
      tags=["groundwater", "borehole", "water table", "hydrology", "geology", "well"])
def _(S):
    return [shell(rect(2, 7, 20, 14, S.R * 0.5)),
            detail(seg(12, 2, 12, 18)),
            detail(wave_h(3.5, 9.5, 15, 1, 2)), detail(wave_h(14.5, 20.5, 15, 1, 2))]


@icon("mantle-convection", CAT, "Globe cutaway with looping arrows circling in the mantle layer",
      tags=["earth interior", "plate tectonics", "geology", "currents", "core", "mantle"])
def _(S):
    top = arc(12, 12, 6.2, 200, 345)
    bot = arc(12, 12, 6.2, 20, 165)
    return [shell(circle(12, 12, 9.5)),
            detail(top + arrow_head(polar(12, 12, 6.2, 345), 75, 1.6)),
            detail(bot + arrow_head(polar(12, 12, 6.2, 165), 255, 1.6)), dot(12, 12, 1.8)]


@icon("rock-thin-section", CAT, "Microscope slide carrying a thin slice of rock split into angular crystals",
      tags=["petrography", "geology", "mineral", "slide", "crystals", "microscope"])
def _(S):
    rock = poly([(6, 9), (12, 7.5), (18, 9.5), (17.5, 15), (11, 16.5), (6.5, 14.5)], closed=True, r=S.r)
    return [shell(rect(2, 4, 20, 16, S.R)), detail(rock),
            detail(seg(10, 7.8, 13.5, 16)), detail(seg(6.3, 12.2, 17.8, 11.5))]


@icon("acid-fizz-test", CAT, "Dropper releasing a drop onto a rock that fizzes with small bubbles",
      tags=["carbonate test", "hydrochloric acid", "geology", "mineral", "limestone", "reaction"])
def _(S):
    rock = poly([(3, 21), (5, 17.5), (10, 16), (15, 16.2), (19, 18), (21, 21)], closed=True, r=S.r)
    return [shell(rect(10, 2, 4, 4.5, 2)), line(seg(8.5, 7.2, 15.5, 7.2)), line(seg(12, 7.2, 12, 10.5)),
            dot(12, 12.8, 1.1), shell(rock),
            dot(6, 12, 1), dot(18, 12, 1), dot(20.5, 8, 0.9), dot(3.8, 8, 0.9)]


@icon("soil-texture-triangle", CAT, "Large triangle chart divided into irregular zones for sand, silt and clay",
      tags=["soil", "texture", "ternary", "agriculture", "classification", "geology", "loam"])
def _(S):
    return [shell(poly([(12, 2.5), (22, 21), (2, 21)], closed=True, r=S.r), stroke_miterlimit="3"),
            detail(seg(5.3, 15, 18.7, 15)), detail(seg(10, 15, 13.5, 21)), detail(seg(12.8, 15, 14.5, 7))]


@icon("sediment-jar", CAT, "Jar of water with settled layers of gravel, sand and silt at the bottom",
      tags=["sedimentation", "soil test", "settling", "layers", "geology", "water", "experiment"])
def _(S):
    return [shell(rect(7, 2, 10, 3, min(S.R, 1))), shell(rect(4.5, 5, 15, 16, S.R)), detail(seg(4.5, 11, 19.5, 11)),
            detail(seg(4.5, 15, 19.5, 15)), dot(8.5, 18.2, 0.8), dot(12, 18.2, 0.8), dot(15.5, 18.2, 0.8)]


@icon("increment-borer", CAT, "T-handled hollow drill reaching the centre of a tree trunk cross-section with growth rings",
      tags=["tree rings", "dendrochronology", "forestry", "core sample", "tree age", "drill"])
def _(S):
    return [shell(circle(15.5, 12, 6.5)), detail(circle(15.5, 12, 2.6)),
            line(seg(3.5, 12, 11.8, 12)), line(seg(3.5, 6.5, 3.5, 17.5))]


@icon("balloon-rocket", CAT, "Balloon taped under a string with air rushing out behind it",
      tags=["newton third law", "thrust", "physics", "classroom", "propulsion", "experiment", "reaction"])
def _(S):
    body = union(ellipse(16.5, 14.5, 5, 4.5), poly([(11.8, 14.5), (8.8, 12.2), (8.8, 16.8)], closed=True))
    return [line(seg(2, 4, 22, 4)), line(seg(16.5, 4, 16.5, 10)),
            shell(body), line(seg(2, 12.2, 5.8, 12.2)), line(seg(2, 16.8, 5.8, 16.8))]


@icon("homemade-compass", CAT, "Magnetized needle on a floating leaf in a bowl of water pointing north",
      tags=["magnet", "needle", "navigation", "classroom", "diy", "magnetism", "experiment"])
def _(S):
    leaf = rotd(ellipse(12, 12, 7, 3.4), -45)
    return [shell(circle(12, 12, 9.5)), detail(leaf),
            sdot(poly([(15.2, 8.8), (13.7, 12.7), (11.3, 10.3)], closed=True)), line(seg(12, 12, 8.8, 15.2))]


@icon("walking-water", CAT, "Two cups joined by a paper strip arching between them as liquid climbs up",
      tags=["capillary action", "color mixing", "paper towel", "classroom", "experiment", "absorption", "cups"])
def _(S):
    cups = []
    for cx in (6, 18):
        cups.append(shell(poly([(cx - 3.8, 11.5), (cx - 3, 21), (cx + 3, 21), (cx + 3.8, 11.5)], closed=True, r=S.r * 0.4)))
    return cups + [detail(seg(3, 15.5, 9, 15.5)), line("M6 10.5C6 1.5 18 1.5 18 10.5")]


@icon("florence-flask", CAT, "Round flask with a flat bottom and a long straight neck",
      tags=["boiling flask", "glassware", "chemistry", "laboratory", "round bottom", "liquid"])
def _(S):
    body = "M10 2V8A7 7 0 0 0 8.57 20.8H15.43A7 7 0 0 0 14 8V2"
    return [shell(body + "Z"), detail(wave_h(6.5, 17.5, 15.5, 1, 3)), line(seg(8.5, 2, 15.5, 2))]


@icon("beaker-tongs", CAT, "Crossed tongs gripping the rim of a beaker",
      tags=["beaker holder", "hot glassware", "lab safety", "heating", "chemistry", "grip"])
def _(S):
    return [shell(poly([(3.5, 11), (3.5, 21.5), (20.5, 21.5), (20.5, 11)], r=min(S.r, 1.5))),
            detail(seg(3.5, 16, 8, 16)),
            line(seg(7.5, 2, 17, 11.5)), line(seg(17, 2, 7.5, 11.5)), dot(12.25, 6.75, 1.1)]


@icon("burette-clamp", CAT, "Clamp on a stand rod holding two burettes side by side",
      tags=["titration", "retort stand", "chemistry", "laboratory", "glassware", "support"])
def _(S):
    return [shell(rect(8.5, 2.5, 4, 14, min(S.R, 1))), shell(rect(16.5, 2.5, 4, 14, min(S.R, 1))),
            line(seg(10.5, 16.5, 10.5, 21.5)), line(seg(18.5, 16.5, 18.5, 21.5)),
            line(seg(2.5, 2.5, 2.5, 21.5)), line(seg(2.5, 8, 18.5, 8))]


@icon("filter-paper", CAT, "Paper circle folded into quarters and opened into a cone with fold lines showing",
      tags=["filtration", "funnel", "chemistry", "laboratory", "coffee", "separation", "fold"])
def _(S):
    return [shell(ellipse(12, 6.5, 9, 3)), line(poly([(3, 6.5), (12, 21.5), (21, 6.5)], r=S.r)),
            line(seg(12, 9.5, 12, 18.5))]


@icon("glassware-drying-rack", CAT, "Rack with an upside-down test tube and round flask resting on pegs",
      tags=["lab", "glassware", "drying", "pegs", "cleaning", "chemistry", "bench"])
def _(S):
    return [shell(rect(2, 17, 20, 4, S.R * 0.5)), line("M3.5 16.5V9.5a2.5 2.5 0 0 1 5 0V16.5"),
            line("M14.5 16.5V13.9A4.8 4.8 0 1 1 17.5 13.9V16.5")]


@icon("kipps-apparatus", CAT, "Three stacked glass bulbs with a tap on the side for generating gas",
      tags=["gas generator", "chemistry", "glassware", "hydrogen sulfide", "laboratory", "tap"])
def _(S):
    body = union(circle(12, 5.6, 3.3), circle(12, 12, 3.7), circle(12, 18.4, 3.9))
    return [shell(body), line(seg(15.7, 12, 21, 12)), line(seg(19.5, 9.8, 19.5, 14.2))]


@icon("cryo-box", CAT, "Square storage box seen from above with a grid of round vial caps",
      tags=["freezer box", "vials", "sample storage", "biobank", "laboratory", "tubes", "cold"])
def _(S):
    box = poly([(3, 8), (8, 3), (21, 3), (21, 21), (3, 21)], closed=True, r=S.r)
    ds = [dot(x, y, 1.3) for x in (8, 12.5, 17) for y in (8.5, 12.5, 17)]
    return [shell(box)] + ds


@icon("anaerobic-jar", CAT, "Tall jar with a lid and knob holding a stack of petri dishes and a gas sachet",
      tags=["microbiology", "oxygen free", "culture", "incubation", "laboratory", "agar plates"])
def _(S):
    return [shell(rect(5, 7, 14, 14.5, S.R)), shell(rect(4, 3, 16, 4, min(S.R, 1.5))), line(seg(10.5, 1.5, 13.5, 1.5)),
            detail(seg(8.5, 11, 15.5, 11)), detail(seg(8.5, 14.5, 15.5, 14.5)), sdot(rect(9.5, 17.5, 5, 1.8, 0))]


@icon("hemocytometer", CAT, "Thick glass slide with an H-shaped groove and a tiny counting grid in the centre",
      tags=["cell counter", "counting chamber", "microscope", "blood", "laboratory", "grid"])
def _(S):
    return [shell(rect(2, 5, 20, 14, S.R)), detail(seg(8, 8.5, 8, 15.5)), detail(seg(16, 8.5, 16, 15.5)),
            detail(seg(8, 12, 16, 12)), sdot(rect(10.7, 10.2, 2.6, 2.6, 0))]


@icon("dissecting-microscope", CAT, "Stereo microscope with two angled eyepieces over a wide flat stage",
      tags=["stereo microscope", "dissection", "biology", "laboratory", "magnifier", "binocular", "specimen"])
def _(S):
    return [line(seg(9, 9, 6, 2.5)), line(seg(13.5, 9, 16.5, 2.5)),
            shell(rect(6.5, 9, 10, 4.5, min(S.R, 1.5))), shell(rect(9.5, 13.5, 4, 3.5, 0)),
            line(seg(19.5, 20.5, 19.5, 11)), line(seg(16.5, 11, 19.5, 11)), line(seg(2.5, 20.5, 21.5, 20.5))]


@icon("agar-slant", CAT, "Test tube lying at an angle with a sloped gel surface inside and a cap",
      tags=["culture tube", "microbiology", "slope", "nutrient agar", "laboratory", "gel", "bacteria"])
def _(S):
    deg = 40
    P_ = lambda pts: rpts(pts, deg)
    tube = poly(P_([(8, 6.5), (8, 18), (16, 18), (16, 6.5)]), r=3.9)
    cap = poly(P_([(7, 3.4), (17, 3.4), (17, 6.5), (7, 6.5)]), closed=True, r=S.r * 0.4)
    gel = poly(P_([(9.6, 11.5), (14.4, 16.5), (14.4, 17), (9.6, 17)]), closed=True)
    return [line(tube), shell(cap), sdot(gel)]


@icon("bacterial-streak-plate", CAT, "Petri dish seen from above with zigzag streaks of bacteria",
      tags=["petri dish", "microbiology", "agar", "culture", "colonies", "laboratory", "inoculation"])
def _(S):
    return [shell(circle(12, 12, 9.5)),
            detail(poly([(6.5, 9), (9, 6.5), (11.5, 9), (14, 6.5), (16.5, 9)])),
            detail(poly([(6.5, 17), (9, 14.5), (11.5, 17), (14, 14.5), (16.5, 17)]))]


@icon("antibiotic-disc-test", CAT, "Petri dish with paper discs, two surrounded by a clear halo",
      tags=["susceptibility", "kirby bauer", "zone of inhibition", "microbiology", "agar", "laboratory", "resistance"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(circle(8.3, 8.3, 2.6)), detail(circle(15.7, 15.7, 2.6)),
            *[sdot(rect(x - w, y - w, 2 * w, 2 * w, 0)) if S.name == "line" else dot(x, y, w * 1.05)
              for x, y, w in ((8.3, 8.3, 0.9), (15.7, 15.7, 0.9), (15.5, 8, 1.2))]]


@icon("nmr-spectrometer", CAT, "Tall cylindrical magnet on legs with a sample tube going in the top",
      tags=["nmr", "magnetic resonance", "spectroscopy", "chemistry", "laboratory", "instrument", "analysis"])
def _(S):
    return [shell(rect(4.5, 8, 15, 10, min(S.R, 3))), detail(seg(4.5, 11.5, 19.5, 11.5)),
            detail(seg(4.5, 14.5, 19.5, 14.5)), line(seg(12, 2, 12, 8)),
            line(seg(8, 18, 7, 22)), line(seg(16, 18, 17, 22))]


# ============================================================================ optics, physics and circuits

@icon("color-disc", CAT, "Round disc divided into rainbow segments with a spin arrow around it",
      tags=["newton disc", "colour wheel", "color wheel", "light", "spectrum", "optics", "physics", "spinning"])
def _(S):
    spokes = "".join(seg(12, 12, *polar(12, 12, 7, a)) for a in range(0, 360, 60))
    tip = polar(12, 12, 10.5, 335)
    return [shell(circle(12, 12, 7)), detail(spokes), dot(12, 12, 1.4),
            line(arc(12, 12, 10.5, 205, 335) + arrow_head(tip, 65, 1.8))]


@icon("burning-glass", CAT, "Magnifying glass focusing converging sun rays onto a small smoking spot",
      tags=["magnifier", "lens", "focus", "sunlight", "heat", "optics", "experiment", "convex lens"])
def _(S):
    return [shell(circle(8.5, 8.5, 5)), line(seg(5, 12, 2.5, 14.5)),
            line(seg(13, 11.5, 17.5, 16.7)), line(seg(11.5, 13.2, 16.4, 18.4)),
            dot(18.5, 18.5, 1.4), line("M19 15.5c-1.6-1.4 1.4-2.4 0-4")]


@icon("raindrop-refraction", CAT, "Round drop with a ray entering, reflecting inside and leaving as a fan of rays",
      tags=["rainbow", "refraction", "light", "dispersion", "optics", "water drop", "physics", "reflection"])
def _(S):
    c = (13, 12)
    e, b, x = polar(*c, 7.5, 240), polar(*c, 7.5, 5), polar(*c, 7.5, 140)
    return [shell(circle(*c, 7.5)), detail(poly([e, b, x]), stroke_miterlimit="1.2"),
            line(seg(2.5, 2.5, e[0], e[1])),
            line(seg(x[0], x[1], 2.5, 14.5)), line(seg(x[0], x[1], 3.5, 21))]


@icon("resonance-tube", CAT, "Tube standing in water with a tuning fork held above its open top",
      tags=["sound", "tuning fork", "resonance", "acoustics", "physics", "air column", "experiment"])
def _(S):
    return [shell(rect(3.5, 4, 7, 17, min(S.R, 2))), detail(seg(3.5, 14, 10.5, 14)),
            line("M16.5 2.5v6.5a2.25 2.25 0 0 0 4.5 0V2.5"), line(seg(18.75, 11.2, 18.75, 15.5))]


@icon("sonometer", CAT, "Long hollow box with a wire stretched over two bridges and a weight hanging at the end",
      tags=["string", "vibration", "sound", "physics", "wire", "tension", "frequency", "monochord"])
def _(S):
    bridge = lambda x: sdot(poly([(x - 1.6, 12.5), (x + 1.6, 12.5), (x, 9.6)], closed=True))
    return [shell(rect(2, 12.5, 15, 7, min(S.R, 2))), bridge(5), bridge(14),
            line(poly([(2, 9), (19.5, 9), (19.5, 14.5)])), shell(rect(17.5, 14.5, 4, 6, 0.5))]


@icon("stirling-engine", CAT, "Small engine with a flywheel and frame above a cylinder sitting over a hot cup",
      tags=["heat engine", "thermodynamics", "flywheel", "piston", "physics", "model", "mechanics"])
def _(S):
    return [shell(rect(5, 3.5, 6, 9.5, min(S.R, 2))), shell(poly([(3.5, 21), (4.5, 16.5), (11.5, 16.5), (12.5, 21)],
                                                                 closed=True, r=S.r * 0.5)),
            line(seg(8, 13, 8, 16.5)), shell(circle(18, 9, 4)), line(seg(11, 8, 18, 8)),
            line(seg(18, 13, 18, 21)), line(seg(14, 21, 22, 21))]


@icon("torsion-balance", CAT, "Rod with small balls on each end hanging from a thin fiber, large balls nearby",
      tags=["cavendish", "gravity", "gravitation", "experiment", "physics", "measurement", "mass", "attraction"])
def _(S):
    return [line(seg(12, 2, 12, 9.5)), line(seg(5, 10, 19, 10)), dot(4.5, 10, 1.9), dot(19.5, 10, 1.9),
            shell(circle(5, 18, 3.2)), shell(circle(19, 18, 3.2))]


@icon("tensile-test", CAT, "Dog-bone shaped sample held in grips at both ends with arrows pulling apart",
      tags=["materials testing", "strength", "stress", "engineering", "specimen", "tension", "pull test"])
def _(S):
    bone = poly([(5.5, 8), (9, 8), (10, 10.5), (14, 10.5), (15, 8), (18.5, 8), (18.5, 16), (15, 16), (14, 13.5),
                 (10, 13.5), (9, 16), (5.5, 16)], closed=True, r=S.r * 0.5)
    return [shell(bone), line(seg(3.5, 6, 3.5, 18)), line(seg(20.5, 6, 20.5, 18)),
            line(arrow(10, 3.5, 4, 3.5, 2)), line(arrow(14, 3.5, 20, 3.5, 2))]


@icon("stress-strain-curve", CAT, "Graph line rising straight, curving over a peak, then dropping to a break mark",
      tags=["materials", "engineering", "yield", "elastic", "plastic", "graph", "fracture", "strength"])
def _(S):
    return [line(poly([(3, 2.5), (3, 21), (21.5, 21)], r=S.r)),
            line("M3.5 20.5L8.5 8C10 4.5 13.5 4 15.5 6.5C17 8.5 17.5 10.5 18 12.5"),
            line(seg(16.5, 12.5, 20.5, 16.5)), line(seg(20.5, 12.5, 16.5, 16.5))]


@icon("series-circuit", CAT, "Single loop of wire with a battery and two bulbs one after the other",
      tags=["electric circuit", "bulbs", "battery", "current", "physics", "electricity", "classroom"])
def _(S):
    rr_ = S.r * 0.8
    return [line(poly([(6.6, 5), (3, 5), (3, 10)], r=rr_)), line(poly([(3, 14), (3, 19), (21, 19), (21, 5), (18.4, 5)], r=rr_)),
            line(seg(11.4, 5, 13.6, 5)), shell(circle(9, 5, 2.4)), shell(circle(16, 5, 2.4)),
            line(seg(0.8, 10, 5.2, 10)), line(seg(1.8, 14, 4.2, 14))]


@icon("parallel-circuit", CAT, "Battery wired to two bulbs on separate side-by-side branches",
      tags=["electric circuit", "bulbs", "battery", "branches", "physics", "electricity", "classroom"])
def _(S):
    rr_ = S.r * 0.8
    parts = [line(poly([(3, 10), (3, 4), (18, 4), (18, 9.6)], r=rr_)), line(poly([(3, 14), (3, 20), (18, 20), (18, 14.4)], r=rr_)),
             line(seg(10, 4, 10, 9.6)), line(seg(10, 14.4, 10, 20)),
             shell(circle(10, 12, 2.4)), shell(circle(18, 12, 2.4)),
             line(seg(0.8, 10, 5.2, 10)), line(seg(1.8, 14, 4.2, 14))]
    return parts


@icon("charge-attraction", CAT, "Plus charge ball and minus charge ball with arrows pointing toward each other",
      tags=["electrostatics", "opposite charges", "electric force", "physics", "positive negative", "coulomb"])
def _(S):
    return [shell(circle(6, 8, 4.6)), shell(circle(18, 8, 4.6)),
            glyph(seg(6, 6.2, 6, 9.8) + seg(4.2, 8, 7.8, 8), 1.3), glyph(seg(16.2, 8, 19.8, 8), 1.3),
            line(arrow(3.5, 18.5, 10, 18.5, 2)), line(arrow(20.5, 18.5, 14, 18.5, 2))]


@icon("current-magnetic-field", CAT, "Vertical wire with a current arrow and rings of circular field lines around it",
      tags=["electromagnetism", "right hand rule", "magnetic field", "physics", "oersted", "current", "wire"])
def _(S):
    return [line(seg(12, 5, 12, 22)), line(arrow(12, 6, 12, 2.2, 2.2)),
            line(ellipse(12, 10.5, 8.5, 2.8)), line(ellipse(12, 17.5, 8.5, 2.8))]


@icon("wave-particle-duality", CAT, "Small ball with a wave line running behind it and trailing off",
      tags=["quantum", "photon", "electron", "physics", "wave", "particle", "double nature"])
def _(S):
    return [line(smooth(sine(2, 12.5, 12, 3, 1.5, 8))), shell(circle(17, 12, 4.5)), dot(17, 12, 1.3)]


@icon("particle-spin", CAT, "Two small spheres, one with an up arrow and one with a down arrow through its center",
      tags=["quantum", "spin up", "spin down", "electron", "physics", "magnetic moment", "arrows"])
def _(S):
    parts = [shell(circle(6.5, 12, 4.5)), shell(circle(17.5, 12, 4.5))]
    parts += [line(seg(6.5, 3.5, 6.5, 7.5) + arrow_head((6.5, 3), -90, 1.8)), detail(seg(6.5, 9, 6.5, 15)),
              line(seg(6.5, 16.5, 6.5, 20.5)),
              line(seg(17.5, 20.5, 17.5, 16.5) + arrow_head((17.5, 21), 90, 1.8)), detail(seg(17.5, 9, 17.5, 15)),
              line(seg(17.5, 7.5, 17.5, 3.5))]
    return parts


@icon("expanding-universe", CAT, "Balloon with dots on its surface and small arrows pointing outward",
      tags=["cosmology", "big bang", "galaxies", "hubble", "balloon analogy", "space", "inflation"])
def _(S):
    body = union(ellipse(12, 12, 6.8, 7.3), poly([(10.6, 18.8), (13.4, 18.8), (12, 20.6)], closed=True))
    return [shell(body), dot(9.6, 11, 1), dot(14.6, 10, 1), dot(12.2, 15, 1),
            line(arrow(5.5, 5.5, 2.4, 2.4, 1.6)), line(arrow(18.5, 5.5, 21.6, 2.4, 1.6))]


# ============================================================================ cells, genes and microscopic life

@icon("ion-channel", CAT, "Membrane band with a tube-shaped protein through it and small dots passing inside",
      tags=["cell membrane", "protein", "transport", "neuron", "biology", "pore", "sodium potassium"])
def _(S):
    return [shell(rect(8, 3, 8, 18, min(S.R, 2))),
            line(seg(1.5, 8.5, 8, 8.5)), line(seg(1.5, 15.5, 8, 15.5)),
            line(seg(16, 8.5, 22.5, 8.5)), line(seg(16, 15.5, 22.5, 15.5)),
            dot(12, 7, 1.1), dot(12, 12, 1.1), dot(12, 17, 1.1)]


@icon("chromatin", CAT, "DNA strand wound around a row of round beads like a string of pearls",
      tags=["nucleosome", "dna", "histone", "genetics", "chromosome", "beads on a string", "biology"])
def _(S):
    parts = [shell(circle(5.5, 16.5, 3.4)), shell(circle(12, 8, 3.4)), shell(circle(18.5, 16.5, 3.4)),
             line(seg(*polar(5.5, 16.5, 4.6, -57), *polar(12, 8, 4.6, 123))),
             line(seg(*polar(12, 8, 4.6, 57), *polar(18.5, 16.5, 4.6, 237))),
             line(seg(2.2, 21, 3.5, 19.2)), line(seg(21.8, 21, 20.5, 19.2))]
    return parts


@icon("telomere", CAT, "X-shaped chromosome with the four arm tips capped by highlighted bands",
      tags=["chromosome", "aging", "dna", "genetics", "cap", "biology", "cell division", "ends"])
def _(S):
    x = union(path_to_d(ST(seg(5.5, 4.5, 18.5, 19.5), 5, "round", "round")),
              path_to_d(ST(seg(18.5, 4.5, 5.5, 19.5), 5, "round", "round")))
    bands = "".join(seg(*polar(cx, cy, 2.6, a + 90), *polar(cx, cy, 2.6, a - 90))
                    for cx, cy, a in ((7.6, 7, 49), (16.4, 7, 131), (7.6, 17, -49), (16.4, 17, -131)))
    return [shell(x), detail(bands)]


@icon("codon-wheel", CAT, "Circle of nested rings divided into wedges for reading the genetic code",
      tags=["genetic code", "amino acid", "rna", "translation", "dna", "biology", "mrna", "triplet"])
def _(S):
    r0, r1 = L(S, 6.2, 7.3), L(S, 9.4, 8.6)
    spokes = "".join(seg(*polar(12, 12, r0, a), *polar(12, 12, r1, a)) for a in range(22, 360, 45))
    return [shell(circle(12, 12, 9.5)), detail(circle(12, 12, 6)), detail(spokes), dot(12, 12, L(S, 2, 1.6))]


@icon("dna-microarray", CAT, "Small glass chip with a dense grid of dots, some filled and some empty",
      tags=["gene chip", "genomics", "biotechnology", "expression", "laboratory", "spots", "bioinformatics"])
def _(S):
    chip = poly([(2.5, 8), (8, 2.5), (21.5, 2.5), (21.5, 21.5), (2.5, 21.5)], closed=True, r=S.r)
    spots = [(x, y) for y in (9.5, 13.5, 17.5) for x in (7, 11, 15, 19)]
    missing = {(11, 9.5), (19, 13.5), (7, 17.5)}
    return [shell(chip)] + [dot(x, y, 1.2) for x, y in spots if (x, y) not in missing]


@icon("genetically-modified-plant", CAT, "Young plant with a small double helix on one of its leaves",
      tags=["gmo", "genetic engineering", "crop", "biotechnology", "dna", "agriculture", "transgenic"])
def _(S):
    leaf = "M11.5 19.5C8.5 11 12.5 4.5 21 3C22 11.5 17.5 19 11.5 19.5Z"
    small = poly([(11.5, 17), (8, 12.5), (3, 12), (3.5, 15.5), (7, 17.5)], closed=True, r=S.r * 0.6)
    return [shell(leaf), shell(small), line(seg(11.5, 17, 11.5, 22)),
            detail("M14.5 15.5C14.5 12 18.5 12 18.5 8.5"), detail("M18.5 15.5C18.5 12 14.5 12 14.5 8.5")]


@icon("cultured-meat", CAT, "Petri dish holding a small steak shape",
      tags=["lab grown meat", "cultivated meat", "cell culture", "food technology", "steak", "biotechnology"])
def _(S):
    steak = "M4.5 7C4.5 3.5 9 2.5 12.5 4C16 2.5 20.5 4 19.5 8C19 11 14 11.5 11 10.5C7.5 11.5 4.5 10.5 4.5 7Z"
    return [shell(steak), dot(15, 6.8, 1.2),
            shell(rect(2.5, 13.5, 19, 7.5, S.R * 0.5))]


@icon("bacterial-conjugation", CAT, "Two rod-shaped bacteria side by side joined by a thin bridge tube",
      tags=["gene transfer", "plasmid", "pilus", "microbiology", "bacteria", "antibiotic resistance", "horizontal"])
def _(S):
    return [shell(rect(3, 3.5, 6.5, 17, S.R * 0.8)), shell(rect(14.5, 3.5, 6.5, 17, S.R * 0.8)),
            line(seg(9.5, 12, 14.5, 12)), dot(6.25, 16, 1)]


@icon("dinoflagellate", CAT, "Armored round cell with a groove around its middle and a trailing flagellum",
      tags=["plankton", "algae", "red tide", "bioluminescence", "marine biology", "microscopic", "flagellum"])
def _(S):
    cell = union(circle(10.5, 10, 6.5), poly([(9, 4.3), (10.5, 1.8), (12, 4.3)], closed=True, r=S.r * 0.4))
    return [shell(cell), detail("M4.5 10.5q6 3.5 12 0"),
            line("M13 15.5c3 1.5 0 3.5 3 5s2.5-1 5 .5")]


@icon("ostracod", CAT, "Bean-shaped two-part shell with small legs and antennae poking out",
      tags=["seed shrimp", "crustacean", "microfossil", "plankton", "pond life", "microscopic", "bivalve"])
def _(S):
    return [shell(ellipse(10.5, 10, 7.5, 5.5)), detail(seg(10.5, 4.6, 10.5, 15.4)),
            line(seg(18, 8, 22, 5)), line(seg(18, 11.5, 22, 13)),
            line(seg(6.5, 15.5, 5.5, 20.5)), line(seg(10.5, 15.5, 10.5, 21)), line(seg(14.5, 15.5, 15.5, 20.5))]


@icon("brine-shrimp", CAT, "Tiny slender shrimp with a row of leaf-like legs and stalked eyes",
      tags=["sea monkey", "artemia", "crustacean", "aquarium", "plankton", "hatchery", "microscopic"])
def _(S):
    return [shell(rect(4.5, 9, 13, 5, 2.5)), line(seg(17.5, 11.5, 21.5, 8.5)), line(seg(17.5, 11.5, 21.5, 14.5)),
            line(seg(7.5, 14, 7, 19)), line(seg(11, 14, 10.5, 19.5)), line(seg(14.5, 14, 14.5, 19)),
            line(seg(6, 9, 5, 5.5)), line(seg(9.5, 9, 10.5, 5.5)), dot(5, 4.2, 1.2), dot(10.5, 4.2, 1.2)]


@icon("gravitropism", CAT, "Pot lying on its side with the shoot curving up and the roots curving down",
      tags=["plant growth", "tropism", "gravity", "roots", "botany", "experiment", "seedling"])
def _(S):
    return [shell(poly([(2.5, 7.5), (13, 5.5), (13, 18.5), (2.5, 16.5)], closed=True, r=S.r * 0.6)),
            line("M13 9C17.5 9 19.5 7 19.5 2.5"), line("M13 15C17.5 15 19.5 17 19.5 21.5")]


@icon("kick-net", CAT, "D-shaped net on a long pole held against a stream bed with water lines",
      tags=["stream sampling", "macroinvertebrates", "freshwater", "ecology", "fieldwork", "river", "survey"])
def _(S):
    return [shell("M4 17A8 8 0 0 1 20 17Z"), detail(seg(12, 9.5, 12, 17)),
            line(seg(17.7, 11.3, 21.5, 3)), line(wave_h(2, 22, 20.8, 0.9, 4))]


# ============================================================================ earth, space and instruments

@icon("geologic-time-scale", CAT, "Tall bar divided into bands of different heights with small fossils beside it",
      tags=["geology", "eras", "periods", "strata", "earth history", "paleontology", "timeline", "fossil"])
def _(S):
    return [shell(rect(3, 2.5, 8, 19, min(S.R, 1.5))), detail(seg(3, 6.5, 11, 6.5)), detail(seg(3, 11, 11, 11)),
            detail(seg(3, 17, 11, 17)),
            shell(circle(18, 7, 3.6)), dot(18, 7, 1.1),
            shell(poly([(15, 14.5), (21, 14.5), (18, 21)], closed=True, r=S.r * 0.5))]


@icon("frost-wedging", CAT, "Rock split by a crack with an ice wedge pushing it apart",
      tags=["weathering", "freeze thaw", "erosion", "geology", "ice", "rock", "physical weathering"])
def _(S):
    rock = poly([(2.5, 7), (7.5, 2.8), (17, 2.8), (21.5, 8), (21.5, 17.5), (16, 21.5), (7, 21.5), (2.5, 17.5)],
                closed=True, r=S.r)
    return [shell(rock), sdot(poly([(9, 3), (15.5, 3), (12.4, 12.5)], closed=True)),
            detail(poly([(12.4, 12.5), (11, 16.5), (12.2, 21.5)]))]


@icon("longshore-drift", CAT, "Zigzag arrow of sand moving along a shoreline under angled waves",
      tags=["coast", "beach", "sediment transport", "geography", "erosion", "waves", "shoreline"])
def _(S):
    zz = poly([(2.5, 4.5), (7, 10), (10, 5.5), (14.5, 11), (17.5, 7), (21, 12.5)])
    return [line(zz + arrow_head((21, 12.5), 55, 2.2)), line(wave_h(2, 22, 18, 1.1, 4)), line(wave_h(2, 22, 22, 1.1, 4))]


@icon("ocean-conveyor-belt", CAT, "World map outline with a long looping ribbon of arrows through the oceans",
      tags=["thermohaline", "ocean currents", "climate", "geography", "circulation", "global", "atlantic"])
def _(S):
    loop = "M5.5 15C8.5 18 12 13 14 11C16 9 18.5 9 19 12C19.5 15 16 16 13 14.5C10 13 7 9.5 5.5 9"
    return [shell(rect(2, 4, 20, 16, S.R * 0.5)),
            detail(loop + arrow_head((5.5, 9), 220, 1.5))]


@icon("adaptive-optics-laser", CAT, "Observatory dome shooting a straight laser beam up to a bright dot in the sky",
      tags=["telescope", "laser guide star", "astronomy", "observatory", "atmosphere", "beam", "optics"])
def _(S):
    return [shell(rect(3, 17.5, 18, 4, min(S.R, 1.5))), shell("M5.5 17.5A6.5 6.5 0 0 1 18.5 17.5Z"),
            detail(seg(12, 11.5, 12, 17.5)), line(seg(12, 9, 12, 6.5)),
            solid(poly(star_pts(12, 3.8, 2.6, 0.9, 4), closed=True))]


@icon("axial-precession", CAT, "Tilted globe whose axis traces a circular arrow above the north pole",
      tags=["earth", "wobble", "axis", "astronomy", "milankovitch", "tilt", "orbit", "climate cycles"])
def _(S):
    c = (10, 15.5)
    return [shell(circle(*c, 5.8)), detail(seg(5.2, 13.3, 14.8, 17.7)),
            line(seg(7.1, 21.7, 13, 9.2)),
            line("M4.5 7A5.5 2.4 0 1 1 15.5 7" + arrow_head((15.5, 7), 75, 1.8))]


@icon("tidal-locking", CAT, "Moon with one marked face always turned toward a larger planet along its orbit",
      tags=["moon", "orbit", "rotation", "astronomy", "synchronous", "planet", "near side"])
def _(S):
    return [shell(circle(6, 12, 4.5)), shell(circle(17.5, 12, 3.9)), dot(15.4, 12, 1),
            line(arc(6, 12, 11.5, -62, -30)), line(arc(6, 12, 11.5, 30, 62))]


@icon("gravity-assist", CAT, "Probe path curving around a planet and leaving at a new angle with an arrow",
      tags=["slingshot", "flyby", "spacecraft", "orbit", "astronomy", "trajectory", "space probe"])
def _(S):
    return [shell(circle(13, 14.5, 4.5)), line("M2.5 20C3 10 8 6 14 5.5C17 5.3 19 5.8 20.5 6.6" + arrow_head((20.5, 6.6), 28, 2)),
            dot(4.4, 14, 1.2)]


@icon("galvanometer", CAT, "Dial meter with its needle resting at the zero mark in the middle of the scale and the letter G",
      tags=["meter", "current", "electricity", "measurement", "zero centre", "physics", "instrument", "dial"])
def _(S):
    g = arc(12, 18.2, 1.6, 20, 320) + seg(12, 18.7, 13.5, 18.7)
    return [shell(rect(2.5, 2.5, 19, 19, S.R)), detail(arc(12, 14, 7.5, 215, 325)),
            line(seg(12, 14, 12, 8.8)), dot(12, 14, 1.2), glyph(g, 1.1)]


@icon("ohmmeter", CAT, "Analog dial meter with a tilted needle and an omega symbol on the face",
      tags=["resistance", "meter", "ohms", "electronics", "measurement", "multimeter", "instrument", "dial"])
def _(S):
    w = poly([polar(12, 18.2, 2, 125 + 0)]) if False else ""
    p1, p2 = polar(12, 18, 1.8, 125), polar(12, 18, 1.8, 55)
    omega = arc(12, 18, 1.8, 125, 55) + seg(*p1, p1[0] - 1.4, p1[1]) + seg(*p2, p2[0] + 1.4, p2[1])
    return [shell(rect(2.5, 2.5, 19, 19, S.R)), detail(arc(12, 14, 7.5, 215, 325)),
            line(seg(12, 14, 16, 8.7)), dot(12, 14, 1.2), glyph(omega, 1.1)]


@icon("sling-psychrometer", CAT, "Handle with a swiveling frame holding two thermometers, one with a wet sleeve",
      tags=["humidity", "weather", "wet bulb", "dry bulb", "meteorology", "thermometer", "fieldwork"])
def _(S):
    return [shell(rect(3.5, 2.5, 17, 10, S.R * 0.5)), detail(seg(8.5, 5, 8.5, 8)), detail(seg(15.5, 5, 15.5, 8)),
            dot(8.5, 9.5, 1.1), dot(15.5, 9.2, 1.6),
            line(seg(12, 12.5, 12, 15.5)), shell(rect(10, 15.5, 4, 6, min(S.R, 1.5)))]


@icon("molecular-model-kit", CAT, "Open tray with loose balls with holes and a short connecting stick",
      tags=["chemistry", "molecule", "ball and stick", "classroom", "organic chemistry", "atoms", "bonds"])
def _(S):
    return [shell(circle(6, 8, 3.5)), shell(circle(15, 8, 3.5)), dot(6, 8, 0.9), dot(15, 8, 0.9),
            line(seg(20.5, 3.5, 20.5, 10.5)),
            shell(poly([(2.5, 13.5), (3.5, 21), (20.5, 21), (21.5, 13.5)], closed=True, r=S.r * 0.6))]


@icon("crystal-radio", CAT, "Board with a wire coil, a tuning slider and an earphone on a cord",
      tags=["radio", "antique radio", "electronics", "classroom", "diy", "coil", "earphone", "receiver"])
def _(S):
    return [shell(rect(2, 17.5, 20, 4, min(S.R, 1.5))), shell(rect(4, 7, 9, 10.5, 1)),
            detail(seg(4, 10.5, 13, 10.5)), detail(seg(4, 14, 13, 14)),
            line(seg(3, 3.5, 13, 3.5)), shell(circle(18.5, 8.5, 3)), line(seg(18.5, 11.5, 18.5, 17.5))]


@icon("egg-drop-experiment", CAT, "Egg in a padded cage hanging from a small parachute",
      tags=["physics", "classroom", "gravity", "parachute", "stem", "challenge", "air resistance", "protection"])
def _(S):
    return [shell("M3 10C3 4.5 7 2.5 12 2.5S21 4.5 21 10Z"),
            line(seg(4, 10.5, 9.5, 15.8)), line(seg(20, 10.5, 14.5, 15.8)), line(seg(12, 10.5, 12, 15.8)),
            shell(rect(8.5, 15.8, 7, 6, S.R * 0.6)), sdot(ellipse(12, 18.9, 1.3, 1.8))]


@icon("solar-oven", CAT, "Box with a propped-up reflective lid bouncing sun rays onto a dish inside",
      tags=["solar cooker", "sun", "reflector", "energy", "cooking", "renewable", "diy", "experiment"])
def _(S):
    return [shell(rect(3, 15, 18, 6, S.R * 0.5)), sdot(poly([(8, 15.8), (15, 15.8), (13.5, 18.5), (9.5, 18.5)], closed=True)),
            line(seg(21, 14, 12.5, 3.5)), dot(4, 4, 1.8),
            line(seg(7.5, 4.5, 12.5, 6.8)), line(seg(5, 8, 10, 12)),
            line(seg(15.8, 9, 14, 12.5))]
