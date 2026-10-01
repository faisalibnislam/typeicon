"""TypeIcon Core: home maintenance, batch 3 (repairs, finishes and appliance parts)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401

CAT = "maintenance"


def rr(S, cap):
    return min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


def xf(pts, deg, cx, cy, ox, oy):
    """Rotate points clockwise by deg about (cx, cy), then move that centre to (ox, oy)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(ox + (x - cx) * c - (y - cy) * s, oy + (x - cx) * s + (y - cy) * c) for x, y in pts]


@icon("carpet-air-mover", CAT, "Snail-shaped floor fan blowing curved air across the floor",
      tags=["carpet dryer", "air mover", "floor fan", "water damage", "drying", "restoration", "blower"])
def _(S):
    body = poly([(8, 7.5), (15, 7.5), (15, 18.5), (8, 18.5)], r=S.r) + "A5.5 5.5 0 0 1 8 7.5Z"
    return [
        shell(body),
        dot(8, 13, 1.5),
        line("M18.5 10q1.5-1.5 3 0"),
        line("M18.5 15q1.5-1.5 3 0"),
    ]


@icon("crack-stitching", CAT, "Brick wall with a crack held shut by metal bars across it",
      tags=["wall crack", "masonry repair", "stitching", "brick", "structural", "helical bar", "repair"])
def _(S):
    k = 0.5 if S.name == "rounded" else 0
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(poly([(13.5, 3), (11, 9), (14, 13), (10.5, 21)], r=S.r * 0.5)),
        sq(6, 7, 12, 2, k),
        sq(6, 15, 12, 2, k),
    ]


@icon("bird-nest-in-vent", CAT, "Round wall vent with twigs poking out through its slats",
      tags=["bird nest", "vent", "blocked vent", "twigs", "pest", "exhaust", "dryer vent"])
def _(S):
    return [
        shell(circle(11, 12, 8.5)),
        detail(seg(6, 7, 16, 7)),
        detail(seg(6, 17, 16, 17)),
        line(seg(7, 10, 22, 15.5)),
        line(seg(7, 14, 22, 8.5)),
    ]


@icon("light-fixture-wiring", CAT, "Ceiling box with wires hanging down to a flat light fixture",
      tags=["light fixture", "ceiling light", "wiring", "electrical", "install", "junction box", "electrician"])
def _(S):
    return [
        shell(rect(8, 2, 8, 4, rr(S, 1.5))),
        line("M10 6C10 9.5 7 9.5 7 13"),
        line("M14 6C14 9.5 17 9.5 17 13"),
        shell(rect(3, 14, 18, 6, rr(S, 3))),
    ]


@icon("cable-staple", CAT, "U-shaped staple holding a round cable against a wall",
      tags=["cable clip", "wire staple", "fastener", "cable", "nail", "electrical", "secure wire"])
def _(S):
    return [
        line(seg(2, 21, 22, 21)),
        shell(circle(12, 13.5, 3.5)),
        line(poly([(7, 20), (7, 6.5), (17, 6.5), (17, 20)], r=S.r)),
    ]


@icon("damaged-siding", CAT, "House siding with a broken, jagged corner and a missing chunk",
      tags=["siding", "exterior", "cladding", "broken", "storm damage", "house repair", "clapboard"])
def _(S):
    pts = [(3, 3), (21, 3), (21, 12.5), (17, 14.5), (19, 17.5), (14, 18), (12.5, 21), (3, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.6), stroke_miterlimit="3"),
        detail(seg(3, 9, 21, 9)),
        detail(seg(3, 15, 11, 15)),
    ]


@icon("loose-handrail", CAT, "Sloped stair handrail on posts with one post pulled loose and tilted",
      tags=["handrail", "stair rail", "banister", "wobbly", "safety", "balustrade", "stairs"])
def _(S):
    return [
        line(seg(2, 13, 22, 3)),
        line(poly([(2, 21), (8, 21), (8, 18), (14, 18), (14, 15), (20, 15)], r=S.r)),
        line(seg(5, 11.5, 5, 20)),
        line(seg(11, 8.5, 11, 17)),
        line(seg(17, 5.5, 19.5, 12)),
    ]


@icon("sagging-gutter", CAT, "Rain gutter drooping away from the roof edge as water drips out",
      tags=["gutter", "rain gutter", "sagging", "roof edge", "fascia", "drip", "exterior repair"])
def _(S):
    return [
        line(seg(2, 3, 22, 3)),
        shell("M2 5Q12 15 22 5V10Q12 20 2 10Z", stroke_miterlimit="3"),
        dot(12, 20, 1.3),
    ]


@icon("popcorn-ceiling-removal", CAT, "Textured bumpy ceiling being scraped smooth with a long scraper",
      tags=["popcorn ceiling", "acoustic ceiling", "scraper", "ceiling texture", "remodel", "drywall", "stucco"])
def _(S):
    return [
        line("M2 4a1.5 1.5 0 0 0 3 0a1.5 1.5 0 0 0 3 0H22"),
        solid(rect(9, 7.5, 12, 3, 0.5 if S.name == "rounded" else 0)),
        line(seg(15, 10, 19, 21)),
    ]


@icon("paint-stripping", CAT, "Scraper lifting bubbled old paint off a board under heat",
      tags=["paint stripper", "heat gun", "scraping", "old paint", "refinish", "bubbled paint", "remove paint"])
def _(S):
    return [
        shell(rect(2, 17, 20, 4, rr(S, 2))),
        line("M2 15a2.5 2.5 0 0 1 5 0a2.5 2.5 0 0 1 5 0"),
        shell(poly([(12.5, 15), (18, 15), (17, 11.5), (13.5, 11.5)], closed=True, r=S.r * 0.5)),
        line(seg(16.5, 11.5, 21, 4)),
        line("M3 5q1.5-2 3 0t3 0"),
    ]


@icon("paint-roller-grid", CAT, "Wire grid screen standing in a paint bucket",
      tags=["roller grid", "paint tray", "paint bucket", "painting", "screen", "diy", "paint"])
def _(S):
    return [
        line(poly([(3, 8), (5.5, 21), (18.5, 21), (21, 8)], r=S.r)),
        shell(rect(8, 2, 8, 13.5, rr(S, 1.5))),
        detail(seg(8, 7, 16, 7)),
        detail(seg(8, 11, 16, 11)),
        detail(seg(12, 2, 12, 15.5)),
    ]



@icon("concealed-cabinet-hinge", CAT, "Cabinet door edge with a round cup hinge and its mounting plate",
      tags=["cabinet hinge", "cup hinge", "euro hinge", "kitchen cabinet", "door adjustment", "hardware", "cupboard"])
def _(S):
    return [
        shell(rect(2, 3, 10, 18, rr(S, 3))),
        dot(7, 12, 2.5),
        line(seg(9.5, 12, 15, 12)),
        shell(rect(15, 7, 6, 10, rr(S, 3))),
        dot(18, 10, 1.1),
        dot(18, 14, 1.1),
    ]


@icon("fridge-door-seal", CAT, "Refrigerator door with its rubber gasket peeling away at one corner",
      tags=["fridge gasket", "refrigerator seal", "door gasket", "rubber seal", "appliance repair", "cold leak", "freezer"])
def _(S):
    return [
        shell(rect(2, 2, 20, 20, rr(S, 4))),
        detail(poly([(12.5, 18), (7, 18), (7, 6), (17, 6), (17, 11)], r=S.r)),
        detail("M17 11C20 12 20 15 17.5 17.5"),
    ]


@icon("dishwasher-filter", CAT, "Cylindrical mesh filter with a twist handle above a flat round screen",
      tags=["dishwasher", "filter", "mesh", "screen", "appliance maintenance", "clean filter", "drain"])
def _(S):
    return [
        line(seg(8.5, 3, 15.5, 3)),
        shell(rect(7, 5, 10, 8, rr(S, 2))),
        detail(seg(12, 5, 12, 13)),
        detail(seg(7, 9, 17, 9)),
        shell(rect(3, 16.5, 18, 4, rr(S, 2))),
    ]


@icon("range-hood-filter", CAT, "Metal baffle filter panel with slanted slats and grease drips below",
      tags=["range hood", "grease filter", "kitchen exhaust", "baffle filter", "vent hood", "cooker hood", "clean filter"])
def _(S):
    return [
        shell(rect(2, 3, 20, 13, rr(S, 3))),
        detail(seg(6, 16, 9, 3)),
        detail(seg(11, 16, 14, 3)),
        detail(seg(16, 16, 19, 3)),
        dot(7, 20, 1.3),
        dot(14, 20, 1.3),
    ]


@icon("fin-comb", CAT, "Comb tool with teeth straightening a row of bent cooling fins",
      tags=["fin comb", "condenser fins", "air conditioner", "coil", "straighten", "hvac", "heat exchanger"])
def _(S):
    return [
        shell(rect(3, 3, 18, 5, rr(S, 2))),
        line(seg(6, 8, 6, 13)),
        line(seg(12, 8, 12, 13)),
        line(seg(18, 8, 18, 13)),
        line(seg(6, 15, 6, 21)),
        line(poly([(12, 15), (12, 17), (10, 21)], r=S.r * 0.5)),
        line(poly([(18, 15), (18, 17), (20, 21)], r=S.r * 0.5)),
    ]


@icon("dripping-ceiling-light", CAT, "Pendant light shade with water drops falling from it",
      tags=["leak", "ceiling leak", "light fixture", "water damage", "pendant", "drip", "roof leak"])
def _(S):
    return [
        line(seg(5, 3, 19, 3)),
        line(seg(12, 3, 12, 6)),
        shell("M5 13A7 7 0 0 1 19 13Z"),
        dot(8, 17.5, 1.3),
        dot(16, 17.5, 1.3),
        dot(12, 20.5, 1.3),
    ]


@icon("wallpaper-scorer", CAT, "Palm-sized scoring tool with a spiked wheel under a domed body",
      tags=["wallpaper", "perforator", "paper tiger", "scoring", "wall stripping", "redecorating", "steamer prep"])
def _(S):
    star = []
    for i in range(16):
        r = 4.3 if i % 2 == 0 else 2.8
        a = math.radians(-90 + i * 22.5)
        star.append((12 + r * math.cos(a), 16.5 + r * math.sin(a)))
    return [
        shell("M6.5 9A5.5 5.5 0 0 1 17.5 9Z"),
        shell(poly(star, closed=True), stroke_miterlimit="3"),
        dot(3.5, 17, 1),
        dot(20.5, 17, 1),
    ]


@icon("self-leveling-floor", CAT, "Tipped bucket pouring liquid compound that spreads flat across a floor",
      tags=["self leveling", "floor compound", "screed", "concrete", "pour", "flooring", "subfloor"])
def _(S):
    b = xf([(2.5, 3), (11.5, 3), (10, 12), (4, 12)], 100, 7, 7.5, 8, 7.5)
    return [
        shell(poly(b, closed=True, r=S.r * 0.6)),
        line(seg(13.5, 11, 13.5, 16.5)),
        shell(rect(2, 17, 20, 4, rr(S, 2))),
    ]
