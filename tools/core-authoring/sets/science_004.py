"""TypeIcon Core: science (batch science_004).

Physics, chemistry, biology and field-science concepts drawn as simple diagrams of the objects themselves.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar  # noqa: F401

CAT = "science"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def pts_d(pts, closed=False):
    d = "".join(("M" if i == 0 else "L") + f"{fmt(x)} {fmt(y)}" for i, (x, y) in enumerate(pts))
    return d + ("Z" if closed else "")


def ah(tip, deg, S, size=2.0):
    """Open arrowhead at `tip` pointing along `deg` (0 = right, 90 = down)."""
    a = polar(tip[0], tip[1], size * 1.414, deg + 135)
    b = polar(tip[0], tip[1], size * 1.414, deg - 135)
    return line(poly([a, tip, b], r=L(S, 0, 0.6)))


def wave(x0, x1, y, amp, n):
    """Horizontal wave from x0 to x1 made of n half-waves (quadratic arcs); starts upward."""
    w = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        sgn = -1 if i % 2 == 0 else 1
        d += f"Q{fmt(x0 + w * (i + 0.5))} {fmt(y + sgn * 2 * amp)} {fmt(x0 + w * (i + 1))} {fmt(y)}"
    return d


def vwave(x, y0, y1, amp, n):
    """Vertical wave from y0 to y1 (n half-waves), starts to the left."""
    h = (y1 - y0) / n
    d = f"M{fmt(x)} {fmt(y0)}"
    for i in range(n):
        sgn = -1 if i % 2 == 0 else 1
        d += f"Q{fmt(x + sgn * 2 * amp)} {fmt(y0 + h * (i + 0.5))} {fmt(x)} {fmt(y0 + h * (i + 1))}"
    return d


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled body."""
    return Part("dot", d)


def sdot(x, y, r, S):
    """Dot that is a small square with sharp corners in Line and a disc in Rounded."""
    return Part("dot", rect(x - r, y - r, 2 * r, 2 * r, L(S, 0, r)))


def minus_sign(x, y, S, w=3.0, h=1.4):
    return Part("dot", rect(x - w / 2, y - h / 2, w, h, L(S, 0, h / 2)))


def tilt(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


# ============================================================================ chemistry and atomic

@icon("redox-reaction", CAT, "Two atoms with an electron travelling between them along a curved arrow",
      tags=["redox", "electron transfer", "oxidation", "reduction", "chemistry", "reaction"])
def _(S):
    return [shell(circle(6, 17, 4)), shell(circle(18, 17, 4)),
            line("M6 10.5Q12 -1.5 18 10.5"), ah((18, 10.5), 60, S),
            dot(6, 17, 1.5)]


@icon("dissolving", CAT, "Sugar cube dissolving in a glass of water with particles drifting away",
      tags=["dissolve", "solution", "solute", "solvent", "chemistry", "sugar", "stir"])
def _(S):
    return [shell(poly([(5, 3), (19, 3), (17, 21), (7, 21)], closed=True, r=S.r)),
            detail(seg(5.6, 8, 18.4, 8)),
            Part("dot", rect(8.5, 16, 3.5, 3.5, L(S, 0, 1))),
            dot(14, 17.5, 1.1), dot(15, 13.5, 1.1), dot(11, 12, 1.1)]


@icon("sublimation", CAT, "Solid block with vapor wisps rising straight off its top",
      tags=["sublimate", "dry ice", "solid to gas", "phase change", "vapor", "chemistry"])
def _(S):
    return [shell(rect(3, 15, 18, 6, S.R if S.name == "line" else 3)),
            line(vwave(7, 12, 3, 1.4, 3)), line(vwave(12, 12, 3, 1.4, 3)), line(vwave(17, 12, 3, 1.4, 3))]


@icon("chain-reaction", CAT, "Branching cascade where one nucleus splits and sets off two more",
      tags=["nuclear", "fission", "cascade", "branching", "neutron", "reaction"])
def _(S):
    return [shell(circle(12, 5, 2.5)), shell(circle(6, 13, 2.5)), shell(circle(18, 13, 2.5)),
            line(seg(10.3, 7, 7.7, 11)), line(seg(13.7, 7, 16.3, 11)),
            sdot(3, 20.5, 1.3, S), sdot(9, 20.5, 1.3, S), sdot(15, 20.5, 1.3, S), sdot(21, 20.5, 1.3, S)]


@icon("isotope", CAT, "Three nuclei in a row, each holding one more neutron than the last",
      tags=["isotopes", "neutron", "nucleus", "atomic mass", "nuclide", "chemistry"])
def _(S):
    cols = [(5, [11]), (12, [8.5, 13.5]), (19, [6, 11, 16])]
    out = [Part("dot", rect(x - 1.9, y - 1.9, 3.8, 3.8, L(S, 0, 1.9))) for x, ys in cols for y in ys]
    return out + [line(seg(2, 20.5, 21, 20.5)), ah((21.5, 20.5), 0, S, 1.8)]


@icon("radioactive-decay", CAT, "Nucleus emitting a small particle along a line, with a wavy ray below",
      tags=["decay", "radioactivity", "alpha particle", "nuclear", "emission", "half life"])
def _(S):
    return [shell(circle(7, 9, 4)), dot(5.8, 8, 1.1), dot(8.4, 10.4, 1.1),
            line(seg(13.5, 9, 16.5, 9)), dot(20, 9, 2),
            line(wave(4, 22, 19, 1.5, 4))]


@icon("radiation-penetration", CAT, "Three arrows meeting a sheet, a plate and a thick block, stopping at different ones",
      tags=["radiation", "shielding", "alpha beta gamma", "penetration", "nuclear", "stopping power"])
def _(S):
    return [line(seg(2, 5, 22, 5)), ah((22, 5), 0, S, 1.8), line(seg(8, 2, 8, 8)),
            line(seg(2, 12, 11, 12)), ah((11, 12), 0, S, 1.8), Part("solid", rect(14, 8.5, 3, 7)),
            line(seg(2, 19, 12, 19)), ah((12, 19), 0, S, 1.8), Part("solid", rect(15, 15.5, 6, 6))]


@icon("atomic-orbital", CAT, "Two teardrop lobes meeting at a point on crossed axes, like a figure eight",
      tags=["orbital", "p orbital", "electron cloud", "quantum", "chemistry", "lobes"])
def _(S):
    up = "M12 12C6 10.5 6 3.5 12 3.5C18 3.5 18 10.5 12 12Z"
    dn = "M12 12C6 13.5 6 20.5 12 20.5C18 20.5 18 13.5 12 12Z"
    return [shell(up), shell(dn), line(seg(2, 12, 22, 12))]


@icon("galvanic-cell", CAT, "Two beakers with metal strips joined by a wire through a meter",
      tags=["battery", "electrochemistry", "voltaic cell", "electrodes", "chemistry", "circuit"])
def _(S):
    r = L(S, 0, 1.5)
    return [shell(poly([(2.5, 11), (2.5, 20), (10.5, 20), (10.5, 11)], r=r)), shell(poly([(13.5, 11), (13.5, 20), (21.5, 20), (21.5, 11)], r=r)),
            line("M6.5 16V6H9"), line("M17.5 16V6H15"),
            shell(circle(12, 6, 3)), line(seg(12, 7, 13.2, 4.8))]


@icon("corrosion", CAT, "Metal bolt with rough eaten edges and flakes falling away",
      tags=["rust", "oxidation", "decay", "metal", "erosion", "bolt"])
def _(S):
    return [shell(poly([(3, 6), (8, 6), (8, 9), (21, 9), (21, 15), (18, 13.5), (15.5, 15), (13, 13.5), (10.5, 15), (8, 15), (8, 18), (3, 18)], closed=True, r=S.r * 0.6)),
            dot(15, 19.5, 1.1), dot(11.5, 21, 1.1), dot(19, 18.5, 1.1)]


@icon("oil-and-water", CAT, "Glass holding a separate layer of oil floating on water with a few drops",
      tags=["immiscible", "oil", "water", "layers", "density", "liquid separation"])
def _(S):
    return [shell(poly([(5, 3), (19, 3), (17, 21), (7, 21)], closed=True, r=S.r)),
            detail(seg(5.9, 10, 18.1, 10)),
            dot(10.5, 15, 1.3), dot(13.8, 17.5, 1.3), dot(13.5, 13.5, 1.1)]


@icon("energy-levels", CAT, "Stack of horizontal levels with an electron jumping down and a wavy photon leaving",
      tags=["bohr model", "electron transition", "photon emission", "quantum", "atomic", "spectral line"])
def _(S):
    return [line(seg(2, 5, 12, 5)), line(seg(2, 12, 12, 12)), line(seg(2, 19, 12, 19)),
            dot(4.5, 9.5, 1.5), line(seg(7, 14, 7, 17.5)), ah((7, 18.2), 90, S, 1.4),
            line(wave(14, 22, 15.5, 1.5, 4))]


@icon("plum-pudding-model", CAT, "Large sphere dotted evenly with small minus signs inside",
      tags=["thomson model", "atomic model", "electrons", "history of atom", "physics", "chemistry"])
def _(S):
    pts = [(12, 7.5), (7.5, 11), (16.5, 11), (12, 13), (8.5, 16.5), (15.5, 16.5)]
    return [shell(circle(12, 12, 9))] + [minus_sign(x, y, S) for x, y in pts]


@icon("phase-diagram", CAT, "Graph with three regions divided by curved lines meeting at one point",
      tags=["triple point", "solid liquid gas", "pressure temperature", "states of matter", "chart", "thermodynamics"])
def _(S):
    return [line(poly([(3, 3), (3, 21), (21, 21)], r=S.r)),
            line("M8.5 15.5C8 11 9.5 7 10 3.5"), line("M8.5 15.5C7 17 6 18 5.5 19.5"),
            line("M8.5 15.5C14 15.5 18 12 21 6"), dot(8.5, 15.5, 1.5)]


@icon("boiling-point", CAT, "Pot of hot water with steam bubbles above it and a thermometer reading high",
      tags=["boiling", "water", "heat", "temperature", "100 degrees", "thermometer", "steam"])
def _(S):
    return [shell(rect(2.5, 12, 11, 9, L(S, 1, 3))),
            dot(5.5, 8, 1.2), dot(8.5, 5.5, 1.2), dot(11, 8.5, 1.2),
            shell("M17 14V5a2 2 0 0 1 4 0v9a3 3 0 1 1-4 0Z"), detail(seg(19, 16, 19, 8))]


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


# ============================================================================ light and optics

@icon("light-polarization", CAT, "Wavy light passing through a slotted filter and leaving as a flatter wave",
      tags=["polarizer", "polarised light", "polarized", "filter", "optics", "wave plane"])
def _(S):
    return [line(wave(2, 10, 12, 3.2, 2)), line(seg(12, 3, 12, 9)), line(seg(12, 15, 12, 21)),
            line(wave(14, 22, 12, 1.2, 2))]


@icon("optical-fiber", CAT, "Curved glass strand with a zigzag light ray bouncing along the inside",
      tags=["fiber optic", "fibre optic", "total internal reflection", "light guide", "cable", "optics"])
def _(S):
    p = [(2, 7), (10, 7), (10, 17), (22, 17)]
    ds = [dot(*bez(*p, t), 1.2) for t in (0.12, 0.38, 0.62, 0.88)]
    return [line("M2 2.5C10 2.5 10 12.5 22 12.5"), line("M2 11.5C10 11.5 10 21.5 22 21.5")] + ds


@icon("concave-mirror", CAT, "Curved mirror with parallel rays reflecting to meet at a focal point",
      tags=["mirror", "focal point", "reflection", "rays", "optics", "focus"])
def _(S):
    return [line("M20 3Q12 12 20 21"),
            line(seg(2, 6.6, 17.4, 6.6)), line(seg(17.4, 6.6, 11, 12)),
            line(seg(2, 17.4, 17.4, 17.4)), line(seg(17.4, 17.4, 11, 12)),
            ]


@icon("standing-wave", CAT, "Two mirrored wave curves pinned at both ends with still nodes between loops",
      tags=["wave", "node", "antinode", "resonance", "string vibration", "harmonics"])
def _(S):
    return [line("M3 12Q7.5 3 12 12Q16.5 21 21 12"), line("M3 12Q7.5 21 12 12Q16.5 3 21 12"),
            sdot(3, 12, 1.4, S), sdot(12, 12, 1.4, S), sdot(21, 12, 1.4, S)]


@icon("optical-bench", CAT, "Straight rail with a candle, a lens on a stand and a screen along it",
      tags=["lens", "candle", "screen", "image formation", "optics experiment", "physics lab"])
def _(S):
    return [line(seg(2, 21, 22, 21)),
            Part("solid", rect(3, 14.5, 3.5, 6.5)), dot(4.75, 11.5, 1.4),
            shell("M12 4.5C8.5 8.5 8.5 15.5 12 19.5C15.5 15.5 15.5 8.5 12 4.5Z"),
            Part("solid", rect(19, 7, 2.5, 14))]


@icon("light-dispersion", CAT, "White beam entering a triangular prism and fanning out into separate rays",
      tags=["prism", "rainbow", "spectrum", "refraction", "colors of light", "optics"])
def _(S):
    return [shell(poly([(12, 4), (20, 19), (4, 19)], closed=True, r=S.r)),
            line(seg(2, 15, 7, 13.5)),
            line(seg(16, 12.5, 22, 8)), line(seg(16.5, 13.5, 22, 13.5)), line(seg(17, 14.8, 22, 18.5))]


@icon("airfoil-lift", CAT, "Wing cross-section with air streamlines curving over and under it",
      tags=["wing", "aerodynamics", "aircraft", "bernoulli", "streamlines", "lift"])
def _(S):
    return [shell("M3 13C5 9 11 8 21 12.5C13 14.5 7 15.5 3 13Z"),
            line("M2 6.5C8 3 16 3 22 7"), line("M2 19.5C9 21 16 20.5 22 17")]


@icon("laser-interferometer", CAT, "Two arms at a right angle ending in mirrors with a laser at the corner",
      tags=["ligo", "interference", "michelson", "gravitational waves", "laser", "physics instrument"])
def _(S):
    return [shell(rect(2, 16.5, 6, 6, L(S, 0, 1.5))), line(seg(5, 16.5, 5, 6)), line(seg(8, 19.5, 18, 19.5)),
            line(seg(2, 4.5, 8, 4.5)), line(seg(19.5, 16.5, 19.5, 22.5))]


# ============================================================================ mechanics and fields

@icon("heat-conduction", CAT, "Metal rod heated by a flame at one end with heat marks spreading along it",
      tags=["conduction", "thermal", "heat transfer", "metal rod", "flame", "physics"])
def _(S):
    return [shell(rect(3, 9.5, 18, 5, L(S, 0.5, 2.5))),
            shell("M6.5 22C3.5 22 3.5 19 6.5 16.8C7.5 18 9.5 18.5 9.5 20C9.5 21.2 8.5 22 6.5 22Z"),
            line(vwave(11, 6.5, 2.5, 1, 2)), line(vwave(15.5, 6.5, 2.5, 1, 2)), line(vwave(20, 6.5, 2.5, 1, 2))]


@icon("elastic-collision", CAT, "Two balls bumping with sparks above and arrows showing them bounce apart",
      tags=["collision", "momentum", "impact", "bounce", "billiard", "mechanics"])
def _(S):
    return [shell(circle(8, 12, 3)), shell(circle(16, 12, 3)),
            line(seg(12, 2.5, 12, 6.5)), line(seg(8.5, 4, 10, 7)), line(seg(15.5, 4, 14, 7)),
            line(seg(10, 19, 3.5, 19)), ah((3, 19), 180, S, 1.8), line(seg(14, 19, 20.5, 19)), ah((21, 19), 0, S, 1.8)]


@icon("centripetal-force", CAT, "Ball circling along a round path with an arrow pulling it toward the centre",
      tags=["circular motion", "orbit", "inward force", "rotation", "physics", "string"])
def _(S):
    return [shell(circle(12, 5.5, 2.5)), line(arc(12, 14, 8.5, -62, 242)),
            line(seg(12, 8.5, 12, 13)), ah((12, 14.2), 90, S, 1.8)]


@icon("potential-energy", CAT, "Ball resting on a raised ledge with a height arrow down to the ground",
      tags=["gravity", "stored energy", "height", "ledge", "physics", "energy"])
def _(S):
    return [shell(circle(7.5, 5.5, 2.5)), shell(rect(3, 10, 9, 11, L(S, 0, 2))),
            line(seg(17, 6, 17, 18.5)), ah((17, 19), 90, S, 1.8), line(seg(14.5, 5, 19.5, 5)), line(seg(14.5, 21, 21, 21))]


@icon("electroscope", CAT, "Glass jar with a rod through the top ending in two leaves spread apart",
      tags=["static charge", "gold leaf", "electrostatics", "jar", "charge detector", "physics lab"])
def _(S):
    return [shell(rect(4, 9, 16, 12, L(S, 0, 3))), line(seg(12, 6, 12, 9)), dot(12, 4, 2),
            detail(seg(12, 9, 12, 13)), detail(seg(12, 13, 8.5, 18.5)), detail(seg(12, 13, 15.5, 18.5))]


@icon("electromagnetic-induction", CAT, "Bar magnet moving toward a wire coil connected to a small meter",
      tags=["faraday", "coil", "magnet", "induced current", "generator", "physics"])
def _(S):
    return [shell(rect(2, 5, 8, 5, L(S, 0, 1.5))), detail(seg(6, 5, 6, 10)),
            line("M11 10A1.67 1.67 0 0 1 14.3 10A1.67 1.67 0 0 1 17.7 10A1.67 1.67 0 0 1 21 10"),
            line("M11 10V19H13"), line("M21 10V19H19"), shell(circle(16, 19, 2.2))]


@icon("damped-oscillation", CAT, "Wave that starts tall and shrinks step by step toward a flat line",
      tags=["damping", "decay", "ringing", "oscillator", "wave", "vibration"])
def _(S):
    amps = [8, 5.5, 3.5, 2.2, 1.2]
    d = "M2 12"
    x = 2
    for i, a in enumerate(amps):
        sg = -1 if i % 2 == 0 else 1
        d += f"Q{fmt(x + 2)} {fmt(12 + sg * 2 * a)} {fmt(x + 4)} 12"
        x += 4
    return [line(d)]


@icon("magnetic-repulsion", CAT, "Two bar magnets facing like poles with arrows pushing them apart",
      tags=["like poles", "repel", "magnets", "magnetism", "force", "physics"])
def _(S):
    return [shell(rect(2, 6, 8, 6, L(S, 0, 1.5))), shell(rect(14, 6, 8, 6, L(S, 0, 1.5))),
            detail(seg(6, 6, 6, 12)), detail(seg(18, 6, 18, 12)),
            line(seg(10, 18.5, 3.5, 18.5)), ah((3, 18.5), 180, S, 1.8), line(seg(14, 18.5, 20.5, 18.5)), ah((21, 18.5), 0, S, 1.8)]


@icon("cyclotron", CAT, "Two D-shaped halves facing each other with a spiral particle path in the middle",
      tags=["particle accelerator", "dees", "spiral", "physics instrument", "magnet", "collider"])
def _(S):
    sp = [polar(12, 12, 0.65 * t, t * 57.3) for t in [0.8 + 0.6 * i for i in range(11)]]
    return [shell("M9 4C4 4 2 8 2 12s2 8 7 8Z"), shell("M15 4C20 4 22 8 22 12s-2 8-7 8Z"),
            line(poly(sp, r=L(S, 0, 0.5)))]


@icon("cloud-chamber", CAT, "Box tank with a dark base and thin particle trails crossing inside",
      tags=["particle tracks", "wilson chamber", "radiation detector", "physics lab", "trails", "vapor"])
def _(S):
    return [shell(rect(3, 3, 18, 18, L(S, 0, 3))), Part("solid", rect(5, 16, 14, 3)),
            detail("M7 6Q9.5 9 8.5 12.5"), detail(seg(17, 6, 11.5, 12.5))]


@icon("ferrofluid", CAT, "Spiky blob of liquid standing up in points above a magnet",
      tags=["magnetic fluid", "spikes", "liquid magnet", "magnetism", "physics demo", "peaks"])
def _(S):
    return [shell(poly([(3, 17), (5, 15), (7, 8), (9, 15), (12, 4), (15, 15), (17, 8), (19, 15), (21, 17)], closed=True, r=S.r * 0.4)),
            Part("solid", rect(3, 19.5, 18, 2.5))]


@icon("string-telephone", CAT, "Two paper cups joined by a taut string with sound arcs at one cup",
      tags=["tin can phone", "sound", "cups", "vibration", "toy", "communication"])
def _(S):
    return [shell(poly([(7, 7), (10, 9), (10, 15), (7, 17)], closed=True, r=S.r * 0.3)),
            shell(poly([(21, 7), (18, 9), (18, 15), (21, 17)], closed=True, r=S.r * 0.3)),
            line(seg(10, 12, 18, 12)), line(arc(7, 12, 3, 150, 210)), line(arc(7, 12, 5.8, 150, 210))]


def dah(tip, deg, S, size=1.8):
    """Arrowhead as a detail (knocked out of a Filled body)."""
    a = polar(tip[0], tip[1], size * 1.414, deg + 135)
    b = polar(tip[0], tip[1], size * 1.414, deg - 135)
    return detail(poly([a, tip, b], r=L(S, 0, 0.6)))


def oval(cx, cy, rx, ry, S):
    """Rounded: true ellipse. Line: squarer lobe (rounded rectangle)."""
    if S.name == "rounded":
        return ellipse(cx, cy, rx, ry)
    return rect(cx - rx, cy - ry, 2 * rx, 2 * ry, min(rx, ry) * 0.6)


# ============================================================================ states of matter, particles, waves

@icon("freezing-point", CAT, "Thermometer with a low level beside an ice cube",
      tags=["freezing", "ice", "cold", "zero degrees", "thermometer", "melting point", "water"])
def _(S):
    return [shell("M5 14V4.5a2 2 0 0 1 4 0V14a3 3 0 1 1-4 0Z"), detail(seg(7, 17, 7, 14.5)),
            shell(rect(13, 9.5, 8.5, 8.5, L(S, 1, 3))), detail(seg(15.5, 13, 18.5, 13))]


@icon("tornado-bottle", CAT, "Two bottles joined neck to neck with a vortex swirling in the top one",
      tags=["vortex", "water tornado", "science experiment", "bottle", "whirlpool", "demonstration"])
def _(S):
    top = poly([(5, 3), (19, 3), (19, 8), (14.5, 10.5), (9.5, 10.5), (5, 8)], closed=True, r=S.r)
    bot = poly([(9.5, 13.5), (14.5, 13.5), (19, 16), (19, 21), (5, 21), (5, 16)], closed=True, r=S.r)
    return [shell(top), shell(bot), shell(rect(9.5, 10.5, 5, 3, 0)),
            detail(seg(8.5, 6, 15.5, 6)), detail(seg(10.5, 8.8, 13.5, 8.8)),
            dot(10, 18, 1), dot(14, 18, 1)]


@icon("sand-filter", CAT, "Funnel-shaped filter with layered grit and clean drops falling out below",
      tags=["water filter", "filtration", "gravel", "charcoal", "clean water", "purify", "experiment"])
def _(S):
    return [shell(poly([(4, 3), (20, 3), (14.5, 12), (14.5, 14), (9.5, 14), (9.5, 12)], closed=True, r=S.r)),
            detail(seg(7.5, 7.5, 16.5, 7.5)),
            dot(12, 17.5, 1.4), dot(12, 21, 1.2)]


@icon("absorption-spectrum", CAT, "Spectrum band crossed by a few thin dark lines above a wavelength scale",
      tags=["spectrum", "spectroscopy", "fraunhofer lines", "dark lines", "wavelength", "light analysis"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 11, L(S, 1, 3))),
            detail(seg(7, 3.5, 7, 14.5)), detail(seg(13, 3.5, 13, 14.5)), detail(seg(16.5, 3.5, 16.5, 14.5)),
            line(seg(2.5, 20, 21.5, 20)), line(seg(2.5, 18, 2.5, 22)), line(seg(21.5, 18, 21.5, 22))]


@icon("blackbody-radiation", CAT, "Graph with a curve that rises to a peak then falls away",
      tags=["planck", "thermal radiation", "emission curve", "spectrum", "intensity", "wavelength", "physics graph"])
def _(S):
    return [line(poly([(3, 2), (3, 21), (22, 21)], r=S.r)),
            line("M6 20C8 20 9 5 12 5C15 5 15 15 21 18")]


@icon("photoelectric-effect", CAT, "Wavy light arriving at a metal plate while an electron shoots away from it",
      tags=["photon", "electron emission", "einstein", "light", "metal plate", "quantum"])
def _(S):
    return [line(vwave(6, 2, 13.5, 1.3, 3)), ah((6, 16), 90, S, 1.8),
            Part("solid", rect(2, 18.5, 20, 3)),
            line(seg(13, 17, 16, 12)), dot(18, 8.5, 2)]


@icon("bloch-sphere", CAT, "Sphere with an equator ring and a state arrow from the centre to the surface",
      tags=["qubit", "quantum", "quantum computing", "state vector", "sphere", "superposition"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(ellipse(12, 12, 9.5, 3.2)),
            detail(seg(12, 12, 17, 6.5)), dah((17.6, 5.9), -48, S, 1.7), dot(12, 12, 1.2)]


@icon("cosmic-ray-shower", CAT, "A single track from above splitting into a widening cascade of particle tracks",
      tags=["air shower", "cosmic rays", "particles", "cascade", "high energy", "physics", "detector"])
def _(S):
    return [line(seg(12, 2.5, 12, 7)),
            line(seg(12, 7, 5, 14)), line(seg(12, 7, 12, 14)), line(seg(12, 7, 19, 14)),
            line(seg(5, 14, 3, 21)), line(seg(5, 14, 7.5, 21)), line(seg(12, 14, 10, 21)), line(seg(12, 14, 14.5, 21)),
            line(seg(19, 14, 17, 21)), line(seg(19, 14, 21, 21))]


@icon("antimatter", CAT, "Particle marked plus beside its mirror particle marked minus with a spark above",
      tags=["antiparticle", "positron", "annihilation", "particle physics", "plus minus", "opposite"])
def _(S):
    star = [(12, 2.5), (13.2, 5.8), (16.5, 7), (13.2, 8.2), (12, 11.5), (10.8, 8.2), (7.5, 7), (10.8, 5.8)]
    return [shell(circle(6.5, 16.5, 4.2)), shell(circle(17.5, 16.5, 4.2)),
            Part("dot", rect(4.9, 15.8, 3.2, 1.4, L(S, 0, 0.7))), Part("dot", rect(5.8, 14.9, 1.4, 3.2, L(S, 0, 0.7))),
            Part("dot", rect(15.9, 15.8, 3.2, 1.4, L(S, 0, 0.7))),
            solid(poly(star, closed=True, r=L(S, 0, 0.3)))]


@icon("vector-addition", CAT, "Two arrows placed tip to tail with a third arrow closing the triangle",
      tags=["vectors", "resultant", "tip to tail", "physics", "force diagram", "math"])
def _(S):
    return [line(seg(3, 19, 10.5, 6.5)), ah((11, 5.8), -59, S, 1.8),
            line(seg(11, 5.8, 19.5, 15)), ah((20.5, 16), 47, S, 1.8),
            line(seg(3, 19, 19, 19)), ah((21, 19), 0, S, 1.8)]


@icon("free-fall", CAT, "Large and small balls falling side by side with equal speed lines above",
      tags=["gravity", "falling objects", "galileo", "acceleration", "drop", "physics"])
def _(S):
    return [shell(circle(7.5, 13.5, 4.5)), shell(circle(17.5, 13.5, 2.5)),
            line(seg(5.5, 3, 5.5, 6.5)), line(seg(9.5, 3, 9.5, 6.5)), line(seg(17.5, 5.5, 17.5, 8.5)),
            line(seg(2, 21, 22, 21))]


@icon("beam-splitter", CAT, "Glass cube with a diagonal mirror splitting one beam into a straight and a sideways beam",
      tags=["optics", "laser", "interferometer", "half mirror", "light beam", "prism cube"])
def _(S):
    return [shell(rect(7.5, 7.5, 9, 9, L(S, 0.5, 2))), detail(seg(8.5, 15.5, 15.5, 8.5)),
            line(seg(2, 12, 7.5, 12)), line(seg(16.5, 12, 22, 12)), line(seg(12, 7.5, 12, 2))]


@icon("chladni-plate", CAT, "Square plate on a central post with sand drawn into a symmetric pattern",
      tags=["sound vibration", "resonance", "sand pattern", "cymatics", "acoustics", "nodal lines"])
def _(S):
    return [shell(rect(3, 3, 18, 13, L(S, 1, 3))),
            detail(poly([(12, 6.5), (16.5, 9.5), (12, 12.5), (7.5, 9.5)], closed=True)),
            line(seg(12, 16, 12, 21)), line(seg(8, 21.5, 16, 21.5))]


@icon("turbulent-flow", CAT, "Smooth flow lines passing a round obstacle and breaking into swirling eddies",
      tags=["fluid", "eddies", "vortex", "aerodynamics", "flow", "wake", "reynolds"])
def _(S):
    return [line(seg(2, 8.5, 5, 8.5)), line(seg(2, 15.5, 5, 15.5)), shell(circle(9, 12, 2.8)),
            line("M13 5H18A2.5 2.5 0 1 1 15.5 7.5"), line("M13 19H18A2.5 2.5 0 1 0 15.5 16.5")]


@icon("surface-tension", CAT, "Small paperclip resting on the water surface that dips slightly beneath it",
      tags=["water", "meniscus", "liquid", "paperclip", "cohesion", "floating", "physics"])
def _(S):
    return [shell(rect(8, 7.5, 8, 4, L(S, 0.5, 2))),
            line("M2 12.5H6Q12 20 18 12.5H22"),
            line(seg(4, 20, 8, 20)), line(seg(14, 20, 20, 20))]


# ============================================================================ fluids

@icon("viscosity", CAT, "Two pouring edges, one with a long slow thick drip and one with fast thin drops",
      tags=["thick liquid", "honey", "flow resistance", "fluid", "drip", "syrup", "physics"])
def _(S):
    return [shell(rect(3, 2.5, 8, 3.5, L(S, 0.5, 1.7))), shell(rect(14, 2.5, 8, 3.5, L(S, 0.5, 1.7))),
            line(seg(7, 6.5, 7, 15)), shell(circle(7, 18, 2.6)),
            dot(18, 10, 1.3), dot(18, 15, 1.3), dot(18, 20, 1.3)]


@icon("fluid-pressure", CAT, "Tall container with three holes and water jets arcing farther from the lower holes",
      tags=["water pressure", "depth", "hydrostatics", "jets", "container", "torricelli", "physics"])
def _(S):
    return [shell(rect(2.5, 2.5, 8, 19, L(S, 0.5, 2.5))),
            line("M12.5 6.5Q15 6.5 16 9"), line("M12.5 12Q17 12 18.5 15.5"), line("M12.5 17.5Q18.5 17.5 21.5 21")]


# ============================================================================ cells and genetics

@icon("ribosome", CAT, "Two-lobed particle, a small lobe on a large one, sitting on a thin strand",
      tags=["protein synthesis", "translation", "mrna", "organelle", "cell biology", "subunit"])
def _(S):
    return [shell(oval(12, 14, 8, 4.5, S)), shell(oval(12, 6.5, 5, 3.5, S)),
            line("M2 21.5Q7 19.5 12 21.5T22 21.5")]


@icon("meiosis", CAT, "One cell dividing into two and then into four smaller cells",
      tags=["cell division", "gametes", "sex cells", "reproduction", "chromosomes", "biology", "haploid"])
def _(S):
    return [shell(circle(12, 5, 3)),
            line(seg(10.4, 8.2, 7.4, 10)), line(seg(13.6, 8.2, 16.6, 10)),
            shell(circle(6, 13.5, 2.8)), shell(circle(18, 13.5, 2.8)),
            sdot(3.5, 20.5, 1.5, S), sdot(8.5, 20.5, 1.5, S), sdot(15.5, 20.5, 1.5, S), sdot(20.5, 20.5, 1.5, S)]


@icon("dna-sequence", CAT, "Horizontal strip of four cells with base markers above and below",
      tags=["genetic code", "bases", "nucleotides", "genome", "gene sequencing", "atgc", "genetics"])
def _(S):
    return [shell(rect(2.5, 8, 19, 8, L(S, 1, 3))),
            detail(seg(7.25, 8, 7.25, 16)), detail(seg(12, 8, 12, 16)), detail(seg(16.75, 8, 16.75, 16)),
            dot(5, 4, 1.2), dot(14.5, 4, 1.2), dot(9.5, 20, 1.2), dot(19, 20, 1.2)]


@icon("dna-fingerprint", CAT, "Gel with several lanes of horizontal bars at different heights",
      tags=["gel electrophoresis", "dna profiling", "forensics", "bands", "genetic testing", "barcode"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, L(S, 1, 3))),
            detail(seg(5, 7, 8.5, 7)), detail(seg(5, 12.5, 8.5, 12.5)), detail(seg(5, 17, 8.5, 17)),
            detail(seg(10.3, 9, 13.7, 9)), detail(seg(10.3, 14.5, 13.7, 14.5)),
            detail(seg(15.5, 7, 19, 7)), detail(seg(15.5, 12, 19, 12)), detail(seg(15.5, 17, 19, 17))]


@icon("transfer-rna", CAT, "Cloverleaf molecule with three rounded loops and an open-ended stem on top",
      tags=["trna", "translation", "anticodon", "amino acid", "rna", "molecular biology"])
def _(S):
    return [line("M10.2 2.5V11.5H8"), line("M13.8 2.5V11.5H16"), line(seg(10.2, 11.5, 13.8, 11.5)),
            shell(circle(5.2, 11.5, 2.8)), shell(circle(18.8, 11.5, 2.8)),
            line(seg(12, 11.5, 12, 16)), shell(circle(12, 19, 2.8))]


@icon("action-potential", CAT, "Axes with a smooth spike that rises sharply, dips below rest and returns",
      tags=["nerve impulse", "neuron firing", "membrane potential", "spike", "neuroscience", "electrophysiology"])
def _(S):
    return [line(poly([(2, 2), (2, 22), (22, 22)], r=S.r)),
            line("M5 14H8C9 14 9.5 3.5 12 3.5C14.5 3.5 14.5 17.5 16.5 17.5C17.5 17.5 18 14 19.5 14H22")]


@icon("transpiration", CAT, "Plant with an arrow rising from the roots and vapour leaving the leaves",
      tags=["water transport", "plant", "evaporation", "leaves", "roots", "stomata", "botany"])
def _(S):
    return [shell("M12 14C7 14 6 10 6 8C10 8 12 10 12 14Z"), shell("M12 14C17 14 18 10 18 8C14 8 12 10 12 14Z"),
            line(seg(12, 14, 12, 18.5)), line("M12 18.5Q9.5 19.5 7.5 21.5"), line("M12 18.5Q14.5 19.5 16.5 21.5"),
            line(vwave(9, 6, 2, 1, 2)), line(vwave(15, 6, 2, 1, 2)),
            line(seg(3, 21, 3, 9)), ah((3, 8.2), -90, S, 1.5)]


@icon("phagocytosis", CAT, "Large blobby cell reaching two arms around a small rod-shaped bacterium",
      tags=["immune cell", "engulf", "white blood cell", "macrophage", "pathogen", "cell biology"])
def _(S):
    return [shell(circle(8, 12, 6)),
            line("M11.5 6.5Q17.5 3 21 7"), line("M11.5 17.5Q17.5 21 21 17"),
            shell(rect(14.5, 10, 5, 4, L(S, 1, 2)))]


@icon("coccolithophore", CAT, "Round alga covered in overlapping button-like plates",
      tags=["plankton", "algae", "calcium carbonate", "coccoliths", "marine", "microscopic"])
def _(S):
    cs = [(12, 12)] + [polar(12, 12, 5.6, -90 + 60 * i) for i in range(6)]
    body = union(*[circle(x, y, 3.8) for x, y in cs])
    return [shell(body)] + [dot(x, y, 1.1) for x, y in cs]


@icon("desmid", CAT, "Single-celled alga made of two mirrored lobes pinched at the waist",
      tags=["algae", "green alga", "microscopic", "freshwater", "pond life", "cell", "microbiology"])
def _(S):
    body = union(circle(7, 12, 5.8), circle(17, 12, 5.8))
    return [shell(body), dot(7, 12, 1.6), dot(17, 12, 1.6)]


@icon("bacteria-shapes", CAT, "Three microbes side by side: round cocci, a rod and a corkscrew",
      tags=["cocci", "bacillus", "spirillum", "microbiology", "types of bacteria", "germs", "morphology"])
def _(S):
    return [shell(circle(5, 7.5, 2.3)), shell(circle(5, 16.5, 2.3)),
            shell(rect(10, 3, 4, 18, 2)),
            line(vwave(19.5, 3, 21, 1.5, 4))]


@icon("chlamydomonas", CAT, "Round green alga with two whip tails at the top and a small eyespot",
      tags=["flagellate", "algae", "flagella", "microscopic", "pond", "protist", "eyespot"])
def _(S):
    body = (poly([(12, 7.5), (16.2, 10.5)], r=0) and "M12 7.5L16 10.3A6 6 0 1 1 8 10.3Z") if S.name == "line" else circle(12, 15, 6)
    return [shell(body), dot(9.5, 15.5, 1.5),
            line("M10.5 8.5C8.5 6 9.5 4.5 7 2.5"), line("M13.5 8.5C15.5 6 14.5 4.5 17 2.5")]


@icon("cyanobacteria", CAT, "Chain of beaded round cells curling into a filament",
      tags=["blue green algae", "filament", "algal bloom", "microbe", "photosynthetic", "anabaena", "bacteria"])
def _(S):
    pts = [(4, 18.5), (8, 14.5), (12.5, 13), (16.5, 16), (19.5, 12), (17.5, 7), (12, 4.5)]
    return [shell(rect(x - 2.1, y - 2.1, 4.2, 4.2, L(S, 0.6, 2.1))) for x, y in pts]


# ============================================================================ field biology and instruments

@icon("trypanosome", CAT, "Slim wavy cell with a ruffled fin along one side and a whip at the front",
      tags=["parasite", "sleeping sickness", "protozoa", "flagellum", "microbiology", "blood parasite"])
def _(S):
    return [shell("M3 20C3.5 15 8.5 15 11 12C13 9.5 15.5 9 18 7C18.5 10 16 13 13.5 15.5C10.5 18.5 7 21 3 20Z"),
            line("M18 7C19.5 5 21 4.5 22 3"),
            line("M8 10Q9.5 7.5 11.5 9Q13 5.5 15 7")]


@icon("penicillium-mold", CAT, "Stalk ending in a brush of branches tipped with chains of round spores",
      tags=["fungus", "mould", "mold", "spores", "antibiotic", "microbiology", "microscope"])
def _(S):
    return [line(seg(12, 22, 12, 12)),
            line(seg(12, 12, 6.5, 8)), line(seg(12, 12, 12, 8)), line(seg(12, 12, 17.5, 8)),
            dot(5, 5, 1.2), dot(12, 5, 1.2), dot(19, 5, 1.2),
            dot(3.2, 8, 1.1), dot(8.4, 4.2, 1.0), dot(15.6, 4.2, 1.0), dot(20.8, 8, 1.1)]


@icon("nematode", CAT, "Slender worm curving in an S shape inside a microscope field",
      tags=["roundworm", "worm", "microscope", "parasite", "soil organism", "biology slide"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail("M6 15.5C9 7 14 17 18 8.5")]


@icon("pitfall-trap", CAT, "Cup sunk into the ground with its rim level with the soil and a raised cover above",
      tags=["insect trap", "ground beetles", "fieldwork", "sampling", "ecology", "invertebrate survey"])
def _(S):
    return [line(seg(2, 12, 6.5, 12)), line(seg(17.5, 12, 22, 12)),
            shell(poly([(7.5, 12), (16.5, 12), (15, 21), (9, 21)], closed=True, r=S.r)),
            line(seg(4.5, 4.5, 19.5, 4.5)), line(seg(7, 4.5, 7, 8)), line(seg(17, 4.5, 17, 8))]


@icon("mist-net", CAT, "Fine net strung between two poles with a small bird caught in it",
      tags=["bird ringing", "bird banding", "ornithology", "fieldwork", "wildlife survey", "net"])
def _(S):
    return [line(seg(3, 2, 3, 22)), line(seg(21, 2, 21, 22)),
            line("M3 5Q12 8 21 5"), line("M3 19Q12 22 21 19"),
            solid(union(ellipse(11.5, 12.5, 4.5, 3), circle(16.2, 10.4, 2), poly([(8, 12), (4.5, 10.5), (5.5, 14.5)], closed=True)))]


@icon("bat-detector", CAT, "Handheld box with a small speaker and dial below a flying bat",
      tags=["ultrasound", "echolocation", "bat survey", "wildlife", "fieldwork", "ecology"])
def _(S):
    return [solid("M2 5.5C5 3.5 8 4 9.5 6.5C10.5 4.5 11 3.5 12 4C13 3.5 13.5 4.5 14.5 6.5C16 4 19 3.5 22 5.5C20 6 19.5 8 19 9.5C17.5 8 15.5 8 14 9.5C13 8.5 11 8.5 10 9.5C8.5 8 6.5 8 5 9.5C4.5 8 4 6 2 5.5Z"),
            shell(rect(6, 12.5, 12, 9, L(S, 1, 2.5))),
            dot(9.8, 17, 1.5), detail(seg(13.5, 15.5, 15.5, 15.5)), detail(seg(13.5, 18.5, 15.5, 18.5))]


@icon("telemetry-antenna", CAT, "Handheld directional antenna with crossbars on a boom and a small receiver",
      tags=["radio tracking", "wildlife tracking", "yagi", "radio collar", "fieldwork", "signal"])
def _(S):
    return [line(seg(3, 12, 22, 12)),
            line(seg(12, 5, 12, 19)), line(seg(16.5, 7, 16.5, 17)), line(seg(21, 9, 21, 15)),
            line(seg(6, 12, 5.5, 15)), shell(rect(2.5, 15.5, 6, 5.5, L(S, 0.5, 2)))]


@icon("plaster-track-cast", CAT, "Round plaster cast with a raised animal paw print on it",
      tags=["footprint", "animal tracks", "paw print", "fieldwork", "wildlife", "cast", "tracking"])
def _(S):
    return [shell(circle(12, 12, 9.5)),
            sdot(7.5, 9.5, 1.5, S), sdot(10.8, 6.8, 1.5, S), sdot(14.4, 6.8, 1.5, S), sdot(17.5, 9.5, 1.5, S),
            Part("dot", ellipse(12.5, 14.8, 3.6, 2.8) if S.name == "rounded" else rect(8.9, 12.2, 7.2, 5.2, 1.5))]


# ============================================================================ graphs and astronomy

@icon("population-growth-curve", CAT, "S-shaped growth curve rising slowly, then steeply, then levelling under a dashed limit",
      tags=["logistic growth", "carrying capacity", "ecology", "population", "sigmoid", "biology graph"])
def _(S):
    return [line(poly([(2.5, 2), (2.5, 21.5), (22, 21.5)], r=S.r)),
            line("M5.5 19C10 19 10 9.5 14 9.5H21"),
            line("M6 4.5H8.5M11 4.5H13.5M16 4.5H18.5")]


@icon("predator-prey-cycle", CAT, "Axes with two offset waves, one following the other",
      tags=["lotka volterra", "population cycles", "ecology", "oscillation", "predator", "prey", "food web"])
def _(S):
    return [line(poly([(2, 2), (2, 22), (22, 22)], r=S.r)),
            line(wave(4.5, 20.5, 12, 3.6, 4)), line(wave(7, 22, 12, 3.6, 4))]


@icon("stellar-wobble", CAT, "Star tracing a small circle around a point while a planet circles far out",
      tags=["exoplanet", "radial velocity", "planet detection", "star", "orbit", "astronomy"])
def _(S):
    return [line(circle(12, 12, 9.5)), dot(18.7, 5.3, 2),
            line(arc(12, 12, 4.8, 20, 320)), dot(13.2, 10.8, 1.8)]


@icon("elliptical-orbit", CAT, "Oval orbit path with a sun at one focus and a planet on the path",
      tags=["kepler", "planet", "sun", "ellipse", "orbit", "astronomy", "solar system"])
def _(S):
    return [line(ellipse(12, 12, 9.5, 8)), sdot(7, 12, 2, S), dot(18, 5.9, 2)]
