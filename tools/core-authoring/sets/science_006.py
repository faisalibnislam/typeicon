"""TypeIcon Core: science (batch science_006).

Physical chemistry, lab technique and evolution diagrams, drawn as simple symbols.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar  # noqa: F401

CAT = "science"


def rotp(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def head_to(S, tip, deg, size=3.0, role=line):
    a = polar(tip[0], tip[1], size, deg + 180 - 45)
    b = polar(tip[0], tip[1], size, deg + 180 + 45)
    return role(poly([a, tip, b], r=S.r * 0.4))


# ---------------------------------------------------------------------------

@icon("non-ionizing-radiation", CAT, "Warning triangle with a small antenna sending out wave arcs.",
      tags=["emf", "rf", "radio waves", "microwave", "electromagnetic", "hazard", "warning"])
def _(S):
    tri = poly([(12, 2), (22.5, 20.5), (1.5, 20.5)], closed=True, r=S.r + 0.5)
    return [shell(tri), detail(seg(12, 14.5, 12, 18.5)), dot(12, 12.5, 1.1),
            detail(arc(12, 12.5, 3.4, -55, 55)), detail(arc(12, 12.5, 3.4, 125, 235))]


@icon("metallic-bond", CAT, "Four positive metal ions in a grid with free electrons moving between them.",
      tags=["metal", "electron sea", "cations", "lattice", "chemical bonding", "delocalized electrons"])
def _(S):
    out = []
    for cx, cy in [(6.5, 6.5), (17.5, 6.5), (6.5, 17.5), (17.5, 17.5)]:
        out.append(shell(circle(cx, cy, 3.3)))
        out.append(detail(seg(cx - 1.3, cy, cx + 1.3, cy)))
        out.append(detail(seg(cx, cy - 1.3, cx, cy + 1.3)))
    out += [dot(12, 12, 1), dot(12, 6.5, 0.8), dot(6.5, 12, 0.8), dot(17.5, 12, 0.8), dot(12, 17.5, 0.8)]
    return out


@icon("decanting", CAT, "A tilted beaker pouring clear liquid into an upright beaker, sediment left behind.",
      tags=["pour", "separation", "sediment", "settling", "laboratory technique", "transfer liquid", "chemistry"])
def _(S):
    tilt = rotp([(5, 4), (11, 4), (11, 12), (5, 12)], 60, 8, 8)
    sed = rotp([(6.8, 10), (9.4, 10.2)], 60, 8, 8)
    pour = "M13.6 8.8Q16 10 16.6 14.5"
    cup = poly([(13, 14), (13, 19), (15, 21), (19, 21), (21, 19), (21, 14)], r=S.r * 0.6)
    return [shell(poly(tilt, closed=True, r=S.r * 0.6)),
            *[dot(x, y, 0.8) for x, y in sed],
            line(pour), detail(seg(13, 17, 21, 17)), shell(poly([(13, 14), (21, 14), (21, 19), (19, 21), (15, 21), (13, 19)], closed=True, r=S.r * 0.6)),
            ]


@icon("magnetic-separation", CAT, "Horseshoe magnet over a low pile of sand pulling iron filings upward.",
      tags=["magnet", "iron filings", "sorting", "separate mixture", "attract", "physical separation", "chemistry"])
def _(S):
    mag = ("M5 12.5L5 9A7 7 0 0 1 19 9L19 12.5L15 12.5L15 9A3 3 0 0 0 9 9L9 12.5Z")
    return [shell(mag), detail(seg(5, 10.5, 9, 10.5)), detail(seg(15, 10.5, 19, 10.5)),
            dot(7, 16.5, 0.9), dot(17, 16.5, 0.9), dot(12, 15.5, 0.9),
            line("M3 21C8 21 9 18 12 18C15 18 16 21 21 21")]


@icon("heating-curve", CAT, "Graph with a line climbing in steps, flat at two plateaus between the rises.",
      tags=["phase change", "melting point", "boiling point", "temperature graph", "latent heat", "states of matter"])
def _(S):
    return [line(poly([(3, 3), (3, 21), (21, 21)], r=S.r)),
            line(poly([(6, 18), (9, 12.5), (12, 12.5), (15, 7), (18, 7), (20.5, 4)], r=S.r))]


@icon("gas-discharge-tube", CAT, "Sealed glass tube with an electrode at each end and a spark glowing between them.",
      tags=["neon tube", "plasma", "spectrum tube", "vacuum tube", "electrode", "glow", "physics"])
def _(S):
    return [shell(rect(4, 6, 16, 12, S.R)),
            line(seg(2, 12, 7, 12)), line(seg(17, 12, 22, 12)),
            detail(seg(7, 9, 7, 15)), detail(seg(17, 9, 17, 15)),
            detail(poly([(7, 12), (10, 12), (11.5, 9.5), (13, 14.5), (14, 12), (17, 12)]))]


@icon("cell-cycle", CAT, "Circle cut into unequal wedges with an arrow looping around it.",
      tags=["mitosis", "interphase", "cell division", "biology", "phases", "growth", "cycle"])
def _(S):
    end = polar(12, 12, 9, 215)
    return [shell(circle(12, 12, 5)),
            detail(seg(12, 12, 12, 7)), detail(polar_seg(12, 12, 5, 30)), detail(polar_seg(12, 12, 5, 150)),
            line(arc(12, 12, 9, -80, 215)),
            head_to(S, end, 215 + 90, 3.2)]


def polar_seg(cx, cy, r, deg):
    x, y = polar(cx, cy, r, deg)
    return seg(cx, cy, x, y)


@icon("non-newtonian-fluid", CAT, "A thick blob of goo squeezed between two curved finger marks with drips falling below.",
      tags=["oobleck", "cornstarch", "slime", "viscosity", "shear thickening", "goo", "rheology"])
def _(S):
    return [shell(ellipse(12, 8, 8.5, 5)),
            line(seg(7.5, 13, 7.5, 16)), dot(7.5, 19.5, 1.6),
            line(seg(12, 13, 12, 18)), dot(12, 21, 1.2),
            line(seg(16.5, 13, 16.5, 15)), dot(16.5, 18.5, 1.6)]


@icon("electroplating", CAT, "Beaker with two electrodes wired to a battery, metal coating one electrode.",
      tags=["plating", "electrolysis", "electrode", "battery", "anode", "cathode", "coating", "chemistry"])
def _(S):
    return [line(poly([(3, 10), (3, 21), (21, 21), (21, 10)], r=S.r)),
            line(poly([(8, 4), (8, 9)])), shell(ellipse(8, 14, 2.3, 3.3)),
            line(poly([(16, 4), (16, 17)])),
            line(seg(8, 4, 10, 4)), line(seg(14, 4, 16, 4)),
            line(seg(10, 2, 10, 6)), line(seg(14, 3, 14, 5))]


@icon("homologous-limbs", CAT, "Three bones from one shoulder shape ending in fingers, a wing and a flipper.",
      tags=["evolution", "comparative anatomy", "forelimb", "wing", "flipper", "arm", "vertebrate"])
def _(S):
    return [dot(4.5, 4, 1.6), line(seg(4.5, 4, 4.5, 13)), line(poly([(2, 20), (4.5, 13), (7, 20)], r=S.r)),
            dot(12, 4, 1.6), line(seg(12, 4, 12, 10)), shell(poly([(12, 10), (8.5, 21), (15.5, 21)], closed=True, r=S.r)),
            dot(19.5, 4, 1.6), line(seg(19.5, 4, 19.5, 10)), shell(ellipse(19.5, 16, 2.8, 5.5))]


@icon("natural-selection", CAT, "Bark panel with a pale moth standing out and a dark moth blending in.",
      tags=["evolution", "camouflage", "adaptation", "moth", "survival", "darwin", "peppered moth"])
def _(S):
    def moth(x, y):
        return poly([(x - 4, y - 3.5), (x, y - 1), (x + 4, y - 3.5), (x + 4, y + 3.5), (x, y + 1), (x - 4, y + 3.5)],
                    closed=True, r=S.r * 0.4)
    return [line(rect(2, 2, 20, 20, S.R)), shell(moth(8.5, 8.5)), solid(moth(15.5, 15.5))]