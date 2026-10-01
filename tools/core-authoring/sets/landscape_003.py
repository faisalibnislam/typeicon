"""TypeIcon Core: landscape (batch 003).

Rocks, fossils, minerals, gem cuts, sky optics, horizon and sun-path scenes, cloud types and a few
atmosphere diagrams. Horizon scenes share one horizon line (y 17) and one half-sun proportion; gem cuts
share one top-view language (girdle outline, table, a few facet lines). Clouds reuse the shared Core cloud.
"""
import math
import re

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, LINE, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "landscape"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled body."""
    return Part("dot", d)


def sparkle(cx, cy, R, r):
    """Four-pointed sparkle star (vertices for poly)."""
    return [polar(cx, cy, R if k % 2 == 0 else r, -90 + k * 45) for k in range(8)]


def spark(S, cx, cy, R=2.5, r=0.8):
    return mark(poly(sparkle(cx, cy, R, r), closed=True, r=L(S, 0, 0.4)))


def leafq(x1, y1, x2, y2, bulge):
    """Pointed leaf from (x1, y1) to (x2, y2) made of two quadratic curves bowing out by bulge px."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    k = 2 * bulge
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx * k)} {fmt(my + ny * k)} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(mx - nx * k)} {fmt(my - ny * k)} {fmt(x1)} {fmt(y1)}Z")


def bone(x0, x1, y, k=1.5, w=2.4):
    """Horizontal bone silhouette from x0 to x1 centred on y (two knobs at each end)."""
    parts = [rect(x0 + k, y - w / 2, x1 - x0 - 2 * k, w)]
    for x in (x0 + k, x1 - k):
        parts += [circle(x, y - k * 0.9, k), circle(x, y + k * 0.9, k)]
    return union(*parts)


def spiral_pts(cx, cy, r0, r1, a0, turns, n=None):
    """Archimedean spiral points from radius r0 at angle a0 (deg) to radius r1 after `turns` turns (clockwise)."""
    n = n or max(12, int(turns * 18))
    out = []
    for i in range(n + 1):
        t = i / n
        out.append(polar(cx, cy, r0 + (r1 - r0) * t, a0 + 360 * turns * t))
    return out


def smooth(pts, closed=False):
    """Smooth curve through points (Catmull-Rom converted to cubic Beziers)."""
    n = len(pts)
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d + ("Z" if closed else "")


# ============================================================================ rocks and fossils

@icon("quarry", CAT, "Stepped terraced pit cut down into a block of rock.",
      tags=["quarry", "open pit", "mine", "terraces", "excavation", "stone"])
def _(S):
    pts = [(2.5, 5.5), (5.5, 5.5), (5.5, 9), (8.5, 9), (8.5, 12.5), (15.5, 12.5), (15.5, 9), (18.5, 9),
           (18.5, 5.5), (21.5, 5.5), (21.5, 20.5), (2.5, 20.5)]
    return [shell(poly(pts, closed=True, r=S.r * 0.6)), detail(seg(2.5, 16.5, 21.5, 16.5))]


@icon("fossil-ammonite", CAT, "Coiled ammonite fossil shell with ribs across its outer whorl.",
      tags=["ammonite", "fossil", "spiral shell", "paleontology", "prehistoric", "geology"])
def _(S):
    sp = spiral_pts(12, 12, 1.2, 9, 90, 2.0, 40)
    parts = [shell(circle(12, 12, 9)), detail(smooth(sp))]
    return parts


@icon("fossil-trilobite", CAT, "Trilobite fossil with a rounded head shield and three lengthwise lobes.",
      tags=["trilobite", "fossil", "arthropod", "paleontology", "cambrian", "prehistoric"])
def _(S):
    if S.name == "line":
        body = "M3.5 10C3.5 5.5 7.5 3 12 3C16.5 3 20.5 5.5 20.5 10L17.5 18.5C16 20.5 14 21.5 12 21.5C10 21.5 8 20.5 6.5 18.5Z"
    else:
        body = "M3.5 9.5C3.5 5.5 7.5 3 12 3C16.5 3 20.5 5.5 20.5 9.5Q20.5 10.5 20.2 11.3L17.5 18.5C16 20.5 14 21.5 12 21.5C10 21.5 8 20.5 6.5 18.5L3.8 11.3Q3.5 10.5 3.5 9.5Z"
    return [shell(body), detail(seg(3.5, 10, 20.5, 10)),
            detail("M9.75 20V8A2.25 2.25 0 0 1 14.25 8V20"),
            detail(seg(4.8, 14.5, 9.75, 14.5)), detail(seg(14.25, 14.5, 19.2, 14.5))]


_SLAB = [(3, 7.5), (8, 3.5), (19, 4), (21, 9.5), (20, 19), (12, 21), (4, 19.5)]


@icon("fossil-leaf", CAT, "Leaf imprint pressed into a flat stone slab.",
      tags=["leaf fossil", "plant fossil", "imprint", "paleobotany", "fossil", "stone"])
def _(S):
    return [shell(poly(_SLAB, closed=True, r=S.r)), detail(leafq(8, 16.5, 16, 8, 2.6)),
            detail(seg(6.5, 18, 13.2, 10.8))]


@icon("fossil-fish", CAT, "Fish skeleton with spine and ribs pressed into a stone slab.",
      tags=["fish fossil", "fossil", "skeleton", "paleontology", "imprint", "stone"])
def _(S):
    slab = [(2.5, 7), (8.5, 4), (20.5, 5), (21.5, 15.5), (17.5, 20), (4, 19.5), (2.5, 13.5)]
    return [shell(poly(slab, closed=True, r=S.r)),
            detail("M8.5 9Q5 12 8.5 15"), detail(seg(8.5, 12, 16, 12)),
            detail(seg(11, 9, 11, 15)), detail(seg(13.5, 9.5, 13.5, 14.5)),
            detail(poly([(18.5, 9), (16, 12), (18.5, 15)], r=S.r * 0.5))]


def _toe(S, deg):
    tipr = L(S, 0, 0.8)
    d = (f"M10 14C10 8.5 10.8 5.5 {fmt(12 - tipr * 0.5)} {fmt(2.5 + tipr)}"
         f"Q12 2.5 {fmt(12 + tipr * 0.5)} {fmt(2.5 + tipr)}C13.2 5.5 14 8.5 14 14Z")
    return rot(d, deg, 12, 15)


@icon("dinosaur-footprint", CAT, "Large three-toed dinosaur track with pointed claw tips.",
      tags=["dinosaur track", "footprint", "dino", "fossil track", "paleontology", "three toed"])
def _(S):
    heel = ellipse(12, 16.5, 4.5, 4.5)
    return [shell(union(heel, _toe(S, 0), _toe(S, -42), _toe(S, 42)))]


@icon("petrified-wood", CAT, "Cross-cut log turned to stone, with growth rings and a crack.",
      tags=["petrified wood", "fossil wood", "tree rings", "stone log", "geology", "fossil"])
def _(S):
    out = regular(12, 12, 9.5, 12, -90)
    out = [(x + (0.5 if k % 2 else -0.3), y) for k, (x, y) in enumerate(out)]
    return [shell(poly(out, closed=True, r=L(S, 0, 2.2))), detail(circle(12, 12, 4.5)),
            detail(poly([(20.5, 14), (16.5, 15), (16, 12.5)], r=S.r * 0.4)), dot(12, 12, 1)]


@icon("dinosaur-skull-fossil", CAT, "Long toothy dinosaur skull in side view with an eye socket.",
      tags=["dinosaur skull", "fossil", "t rex", "skull", "paleontology", "museum"])
def _(S):
    skull = [(2.5, 13), (4.5, 8.5), (13, 5), (17.5, 4), (21.5, 7), (21.5, 13), (20, 15.5),
             (17.5, 14.5), (16, 16), (13.5, 14.5), (12, 16), (9.5, 14.5), (8, 16), (5.5, 14.5), (4, 15.5)]
    jaw = [(4.5, 19), (20, 19)]
    return [shell(poly(skull, closed=True, r=L(S, 0, 1))), line(poly(jaw, r=0)),
            detail(circle(16.5, 8.5, 1.7)), detail(ellipse(9.5, 9.5, 1.6, 1))]


@icon("fossil-dig-site", CAT, "Excavation pit marked out with pegs and string, a bone lying half uncovered.",
      tags=["dig site", "excavation", "archaeology", "paleontology", "fossil dig", "survey grid"])
def _(S):
    return [line(poly([(2, 10), (5, 10), (5, 20.5), (19, 20.5), (19, 10), (22, 10)], r=S.r)),
            line(seg(5, 10, 5, 3)), line(seg(19, 10, 19, 3)), line(seg(5, 5, 19, 5)), line(seg(12, 5, 12, 9)),
            shell(bone(7.5, 16.5, 15.5))]


@icon("excavation-brush", CAT, "Small flat brush sweeping dust off a partly exposed bone.",
      tags=["excavation brush", "archaeology", "dig", "fossil", "brush", "paleontology"])
def _(S):
    rr = L(S, 0, 0.8)
    handle = poly(rpts([(11, 1.5), (13, 1.5), (13, 7.5), (11, 7.5)], 40), closed=True, r=rr)
    head = poly(rpts([(8.5, 8.5), (15.5, 8.5), (15.5, 13.5), (8.5, 13.5)], 40), closed=True, r=rr)
    return [shell(handle), shell(head),
            detail(poly(rpts([(12, 10.5), (12, 13.5)], 40))),
            shell(bone(3, 19, 19.5)), dot(4, 13.5, 1), dot(6.5, 10.5, 1)]


@icon("stone-arrowhead", CAT, "Knapped flint arrowhead with flake scars and a notched base.",
      tags=["arrowhead", "flint", "stone age", "artifact", "archaeology", "projectile point"])
def _(S):
    pts = [(12, 2.5), (16.5, 10), (17.5, 17.5), (15, 16), (14.5, 21), (9.5, 21), (9, 16), (6.5, 17.5), (7.5, 10)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 1))),
            detail(poly([(9.5, 9.5), (12, 11.5), (14.5, 9.5)], r=S.r * 0.5)),
            detail(poly([(9, 14), (12, 16), (15, 14)], r=S.r * 0.5))]


@icon("geode", CAT, "Split round rock with a hollow centre lined with pointed crystals.",
      tags=["geode", "crystal", "rock", "mineral", "cavity", "amethyst"])
def _(S):
    out = regular(12, 12, 9.5, 9, -90)
    star = [polar(12, 12, 6.3 if k % 2 == 0 else 3.5, -90 + k * 20) for k in range(18)]
    return [shell(poly(out, closed=True, r=S.r * 1.3)), detail(poly(star, closed=True, r=L(S, 0, 0.5)))]


@icon("basalt-columns", CAT, "Cluster of hexagonal basalt columns rising to stepped heights.",
      tags=["basalt", "columns", "hexagonal", "volcanic rock", "causeway", "geology"])
def _(S):
    cols = [(2.5, 8.5, 9), (8.5, 15.5, 4), (15.5, 21.5, 12)]
    shapes = []
    dets = []
    for a, b, t in cols:
        hexa = [(a, t + 1.5), (a + 1.5, t), (b - 1.5, t), (b, t + 1.5), (b, 21), (a, 21)]
        shapes.append(poly(hexa, closed=True))
        dets.append(detail(poly([(a, t + 1.5), (a + 1.5, t + 3), (b - 1.5, t + 3), (b, t + 1.5)], r=S.r * 0.4)))
    sil = union(*shapes)
    dets.append(detail(seg(8.5, 10.5, 8.5, 21)))
    dets.append(detail(seg(15.5, 13.5, 15.5, 21)))
    return [shell(sil)] + dets


@icon("marble-slab", CAT, "Rectangular marble slab with flowing vein lines.",
      tags=["marble", "slab", "stone", "countertop", "veins", "tile"])
def _(S):
    return [shell(rect(3, 5, 18, 14, min(S.R, 2.5))),
            detail("M3 10C7 10 8.5 14.5 12.5 14C15.5 13.6 17 11 21 11.5"),
            detail("M9.5 19C10.5 17 11.5 15.5 12.5 14")]


@icon("slate-rock", CAT, "Stack of thin flat slate sheets with offset, split edges.",
      tags=["slate", "shale", "layered rock", "sheets", "roofing slate", "geology"])
def _(S):
    l1 = [(6, 5.5), (20.5, 5.5), (19, 10), (4.5, 10)]
    l2 = [(3, 10), (18, 10), (19.5, 14.5), (2.5, 14.5)]
    l3 = [(5, 14.5), (21.5, 14.5), (20, 19), (4, 19)]
    sil = union(*(poly(p, closed=True) for p in (l1, l2, l3)))
    return [shell(sil), detail(seg(4.5, 10, 18, 10)), detail(seg(5, 14.5, 19.5, 14.5))]


@icon("sandstone", CAT, "Rounded rock with fine horizontal bands and speckled grain.",
      tags=["sandstone", "sedimentary rock", "layers", "strata", "sand", "geology"])
def _(S):
    rock = "M3 17C3 11 6.5 6 12 6C17.5 6 21 11 21 17C21 19 20 20 18 20H6C4 20 3 19 3 17Z"
    if S.name == "line":
        rock = "M3 20V17C3 11 6.5 6 12 6C17.5 6 21 11 21 17V20Z"
    return [shell(rock), detail("M4.5 11.5C9 12.5 15 10.5 19.5 11.5"), detail("M3 15.5C9 16.5 15 14.5 21 15.5"),
            dot(9.5, 8.8, 0.9), dot(14.5, 8.6, 0.9), dot(8, 18, 0.9), dot(12.5, 18, 0.9), dot(17, 18, 0.9)]


@icon("granite-rock", CAT, "Blocky rock speckled with scattered mineral grains.",
      tags=["granite", "igneous rock", "speckled", "stone", "countertop", "geology"])
def _(S):
    pts = [(3, 18.5), (3.5, 9), (8.5, 4.5), (17.5, 5), (21, 10), (20.5, 19), (12, 20.5)]
    return [shell(poly(pts, closed=True, r=S.r)),
            dot(8, 9.5, 1.1), dot(13, 8.5, 0.9), dot(17, 11, 1.1), dot(10.5, 13, 0.9), dot(7, 16, 1),
            dot(15, 15.5, 1.2), mark(rect(12, 16.8, 1.8, 1.8)), mark(rect(5.8, 12, 1.6, 1.6))]


@icon("conglomerate-rock", CAT, "Rock packed with rounded embedded pebbles.",
      tags=["conglomerate", "pebbles", "sedimentary rock", "gravel", "puddingstone", "geology"])
def _(S):
    pts = [(2.5, 16), (4.5, 8), (10, 4.5), (17.5, 5), (21.5, 11), (20, 19.5), (7, 20)]
    return [shell(poly(pts, closed=True, r=S.r)),
            mark(ellipse(8, 11, 2.2, 1.8)), mark(ellipse(15, 9.5, 1.8, 1.5)), mark(ellipse(13.5, 15.5, 2.5, 2)),
            mark(ellipse(7.5, 16.5, 1.5, 1.3)), mark(ellipse(18, 14, 1.3, 1.3))]


@icon("limestone", CAT, "Pale limestone block with a small embedded shell and pits.",
      tags=["limestone", "sedimentary rock", "chalk", "calcium", "building stone", "geology"])
def _(S):
    return [shell(rect(3, 5.5, 18, 14, min(S.R, 2.5))),
            detail("M7 16A3.5 3.5 0 0 1 14 16Z"), detail(seg(10.5, 16, 10.5, 13)),
            dot(16.5, 9.5, 1), dot(7.5, 9.5, 1), dot(12.5, 9, 0.9), dot(17.5, 15.5, 1)]


@icon("coal-lump", CAT, "Angular lump of coal with flat shiny faces.",
      tags=["coal", "fossil fuel", "carbon", "mining", "fuel", "anthracite"])
def _(S):
    pts = [(3, 15.5), (5.5, 7.5), (12, 3), (19, 5.5), (21.5, 13), (17, 20.5), (8, 20.5)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 2.6))),
            detail(poly([(5.5, 7.5), (12.5, 11), (19, 5.5)], r=S.r * 0.5)), detail(seg(12.5, 11, 13.5, 20.5)),
            detail(seg(12.5, 11, 21.5, 13))]


# ============================================================================ standing stones and crystals

@icon("standing-stones", CAT, "Two upright stones capped by a lintel beside a third standing stone.",
      tags=["standing stones", "stone circle", "stonehenge", "megalith", "prehistoric", "monument"])
def _(S):
    tri = union(rect(2.5, 4.5, 12, 4), rect(2.5, 4.5, 4, 15.5), rect(10.5, 4.5, 4, 15.5))
    third = [(18, 20), (17.5, 9.5), (20, 6.5), (22, 9.5), (22, 20)]
    return [shell(tri), shell(poly(third, closed=True, r=L(S, 0, 1))), line(seg(2, 20, 22, 20))]


@icon("menhir", CAT, "Single tall upright standing stone tapering upward from the ground.",
      tags=["menhir", "standing stone", "megalith", "monolith", "prehistoric", "stone"])
def _(S):
    pts = [(7.5, 20), (8.5, 8.5), (11, 3), (15, 4.5), (16.5, 20)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 1.2))), detail(poly([(10.5, 10), (12.5, 13.5), (11.5, 17)], r=S.r * 0.4)),
            line(seg(3, 20, 21, 20))]


@icon("quartz-crystal", CAT, "Single six-sided quartz prism with a pointed pyramid tip and a bright glint.",
      tags=["quartz", "crystal", "mineral", "prism", "clear quartz", "healing crystal", "gemstone"])
def _(S):
    pts = [(5, 21), (5, 10), (10, 3.5), (16, 10), (16, 21)]
    return [shell(poly(pts, closed=True, r=S.r * 0.7)), detail(poly([(10, 3.5), (10, 21)])),
            detail(seg(5, 10, 10, 10)), spark(S, 19.5, 6, 2.6, 0.8)]


@icon("amethyst-geode", CAT, "Tall arched geode whose cavity is filled with small pointed crystals.",
      tags=["amethyst", "geode", "crystal cave", "purple crystals", "gemstone", "mineral"])
def _(S):
    arch = L(S, "M3 21V11C3 6 7 3 12 3C17 3 21 6 21 11V21Z", "M3 21V11C3 6 7 3 12 3C17 3 21 6 21 11V21Z")
    zig = [(3, 16), (6, 10.5), (8.5, 16), (12, 8), (15.5, 16), (18, 11), (21, 16)]
    return [shell(arch), detail(poly(zig, r=L(S, 0, 0.6)))]


@icon("double-terminated-crystal", CAT, "Six-sided crystal pointed at both ends, lying on a diagonal.",
      tags=["double terminated crystal", "quartz point", "crystal", "mineral", "gemstone", "prism"])
def _(S):
    pts = [(12, 2.5), (17, 8.5), (17, 15.5), (12, 21.5), (7, 15.5), (7, 8.5)]
    return [shell(poly(rpts(pts, 32), closed=True, r=S.r * 0.6)), detail(poly(rpts([(12, 2.5), (12, 21.5)], 32)))]


def _cube(cx, cy, r):
    k = 0.866 * r
    hexa = [(cx, cy - r), (cx + k, cy - r / 2), (cx + k, cy + r / 2), (cx, cy + r), (cx - k, cy + r / 2), (cx - k, cy - r / 2)]
    y = [(cx - k, cy - r / 2), (cx, cy), (cx + k, cy - r / 2)], [(cx, cy), (cx, cy + r)]
    return hexa, y


@icon("pyrite-cubes", CAT, "Two interlocking cubes of pyrite, one large and one small.",
      tags=["pyrite", "fool's gold", "cubes", "mineral", "crystal", "gold"])
def _(S):
    bh, by = _cube(9.5, 13.5, 7.5)
    sh, sy = _cube(17, 8, 4.6)
    sil = union(poly(bh, closed=True), poly(sh, closed=True))
    return [shell(sil), detail(poly(by[0])), detail(poly(by[1])), detail(poly([(13.1, 5.7), (17, 8), (20.9, 5.7)]))]


@icon("fluorite-octahedron", CAT, "Eight-faced octahedron crystal: two pyramids joined at a flat ridge.",
      tags=["fluorite", "octahedron", "crystal", "mineral", "eight faces", "gemstone"])
def _(S):
    top, bot, left, right = (12, 2.5), (12, 21.5), (2.5, 12), (21.5, 12)
    return [shell(poly([top, right, bot, left], closed=True, r=L(S, 0, 3))), detail(seg(L(S, 2.5, 5), 12, L(S, 21.5, 19), 12)),
            detail(seg(12, 2.5, 12, 12))]


@icon("calcite-rhomb", CAT, "Slanted rhombohedral calcite block with three parallelogram faces.",
      tags=["calcite", "rhombohedron", "crystal", "mineral", "iceland spar", "block"])
def _(S):
    p0, p1, p2, p3 = (5.5, 9.5), (14.5, 10.5), (12.5, 21.5), (3.5, 20.5)
    w = (6, -5.5)
    a = (p0[0] + w[0], p0[1] + w[1])
    b = (p1[0] + w[0], p1[1] + w[1])
    c = (p2[0] + w[0], p2[1] + w[1])
    sil = [p0, a, b, c, p2, p3]
    return [shell(poly(sil, closed=True, r=S.r * 0.6)), detail(poly([p0, p1, b])), detail(poly([p1, p2]))]


@icon("salt-crystal", CAT, "Cube-shaped salt crystal with stepped hollow hopper faces.",
      tags=["salt", "hopper crystal", "halite", "cube", "mineral", "crystal"])
def _(S):
    inner = rect(8, 8, 8, 8)
    return [shell(rect(3, 3, 18, 18, S.R * 0.8)), detail(inner), detail(seg(3.5, 3.5, 8, 8)), detail(seg(20.5, 3.5, 16, 8)),
            detail(seg(3.5, 20.5, 8, 16)), detail(seg(20.5, 20.5, 16, 16))]


@icon("desert-rose", CAT, "Rosette of flat bladed crystal plates fanning out from one base.",
      tags=["desert rose", "gypsum", "barite", "rosette", "mineral", "crystal"])
def _(S):
    blades = []
    for ang, ln in ((-58, 9.5), (-29, 12), (0, 13.5), (29, 12), (58, 9.5)):
        tipx, tipy = polar(12, 20, ln, -90 + ang)
        blades.append(leafq(12, 20, tipx, tipy, 2.4))
    return [shell(union(*blades)), detail(seg(12, 20, 12, 8.5)), line(seg(6, 21, 18, 21))]


@icon("mica-sheets", CAT, "Stack of thin flat mica layers with the top sheet peeling up into a curl.",
      tags=["mica", "sheets", "layers", "peeling", "flaky mineral", "thin layers"])
def _(S):
    base = union(rect(3, 13, 16, 4.2), rect(3, 17, 16, 4.2))
    return [shell(union(rect(3, 12.5, 18, 8.5, S.R * 0.3))), detail(seg(3, 16.75, 21, 16.75)),
            line("M3 8.5H14C18.5 8.5 20 3.5 17 3.5C15 3.5 15 6.5 17 6.5")]


@icon("tourmaline", CAT, "Long striated tourmaline prism with lengthwise grooves, a flat end and a rough break.",
      tags=["tourmaline", "crystal", "prism", "striations", "gemstone", "mineral"])
def _(S):
    pts = [(6.5, 20.5), (7, 7), (8.5, 4), (14.5, 4), (16, 7), (16.5, 17.5)]
    return [shell(poly(rpts(pts, 22), closed=True, r=S.r * 0.6)), detail(poly(rpts([(7, 7), (16, 7)], 22))),
            detail(poly(rpts([(11.7, 7), (11.7, 18.5)], 22)))]


@icon("raw-gemstone", CAT, "Rough uncut gemstone with a few flat polished faces and a glint.",
      tags=["raw gemstone", "uncut gem", "rough stone", "rock", "mineral", "jewel"])
def _(S):
    pts = [(2.5, 15), (4.5, 9), (9.5, 6), (14.5, 7), (17.5, 12), (16, 19), (9, 21), (4, 19.5)]
    return [shell(poly(pts, closed=True, r=S.r)), detail(poly([(4.5, 9), (9, 12.5), (14.5, 7)], r=S.r * 0.4)),
            detail(seg(9, 12.5, 9.5, 20.5)), spark(S, 19, 5.5, 2.8, 0.8)]


@icon("cabochon", CAT, "Smooth domed oval gemstone in side view with a highlight on its curve.",
      tags=["cabochon", "gemstone", "jewel", "polished stone", "dome", "jewellery"])
def _(S):
    body = L(S, "M3 18.5V15C3 8.5 7 5 12 5C17 5 21 8.5 21 15V18.5Z",
             "M3 16.5C3 8.5 7 5 12 5C17 5 21 8.5 21 16.5A2 2 0 0 1 19 18.5H5A2 2 0 0 1 3 16.5Z")
    return [shell(body), detail("M7.5 13C7.5 10.5 9 9.3 11 8.8")]


# ============================================================================ pearls and cut gems

def scl(d, k, cx=12.0, cy=12.0, ky=None):
    """Scale path d by k about (cx, cy)."""
    ky = k if ky is None else ky
    return path_to_d(transform_path(P(d), (k, 0, 0, ky, cx * (1 - k), cy * (1 - ky))))


def facets(pts_out, pts_in):
    """Facet lines joining matching points of the girdle and the table."""
    return [detail(seg(a[0], a[1], b[0], b[1])) for a, b in zip(pts_out, pts_in)]


@icon("pearl-oyster", CAT, "Open oyster with its lid raised and a round pearl resting in the lower shell.",
      tags=["oyster", "pearl", "shell", "mollusc", "seafood", "jewel", "sea"])
def _(S):
    if S.name == "line":
        bowl = "M2.5 15H21.5C21.5 19 17.5 21.5 12 21.5C6.5 21.5 2.5 19 2.5 15Z"
        lid = rot("M3 14C3 9.5 6 7 9.5 7C13 7 15.5 9.5 15.5 14Z", -34, 3, 14.5)
    else:
        bowl = "M3.5 15.5A1 1 0 0 1 4.5 14.5H19.5A1 1 0 0 1 20.5 15.5C20.5 19 17 21.5 12 21.5C7 21.5 3.5 19 3.5 15.5Z"
        lid = rot("M4 14C4 9.8 6.5 7.3 9.5 7.3C12.5 7.3 15 9.8 15 14Z", -34, 4, 14.5)
    return [shell(bowl), shell(lid), shell(circle(15.6, 11.6, 2.4))]


@icon("pearl", CAT, "Single round pearl with a sparkling highlight.",
      tags=["pearl", "gem", "jewel", "bead", "sphere", "jewellery", "ocean"])
def _(S):
    return [shell(circle(12, 12, 9.5)), spark(S, 8.8, 8.8, 3.3, 1.0), detail(arc(12, 12, 5.5, 20, 75))]


@icon("jade-stone", CAT, "Smooth rounded jade pebble with a hole bored through it.",
      tags=["jade", "green stone", "pebble", "amulet", "gemstone", "carved stone", "pendant"])
def _(S):
    pts = [(3.5, 13), (6, 7), (12.5, 4), (18.5, 6), (20.5, 13), (17, 19.5), (11, 20.5), (6, 18.5)]
    body = poly(pts, closed=True) if S.name == "line" else smooth(pts, closed=True)
    return [shell(body), detail(circle(12.5, 12, 3))]


@icon("round-brilliant-cut", CAT, "Top view of a round brilliant gem with an octagonal table and radiating facets.",
      tags=["brilliant cut", "round gem", "diamond", "facets", "gemstone", "jewel"])
def _(S):
    table = regular(12, 12, 4.4, 8, -90 + 22.5)
    out = regular(12, 12, 9.5, 8, -90 + 22.5)
    girdle = poly(regular(12, 12, 9.5, 12, -90), closed=True) if S.name == "line" else circle(12, 12, 9.5)
    t = poly(table, closed=True) if S.name == "line" else circle(12, 12, 4.2)
    return [shell(girdle), detail(t)] + facets(out, table)


@icon("emerald-cut", CAT, "Top view of a rectangular step-cut gem with clipped corners and a stepped table.",
      tags=["emerald cut", "step cut", "rectangular gem", "gemstone", "jewel", "facets"])
def _(S):
    def octo(x0, y0, x1, y1, c):
        return [(x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1 - c), (x1 - c, y1), (x0 + c, y1), (x0, y1 - c), (x0, y0 + c)]
    if S.name == "line":
        return [shell(poly(octo(5, 3, 19, 21, 4), closed=True)), detail(poly(octo(9, 7.5, 15, 16.5, 1.8), closed=True))]
    return [shell(rect(5, 3, 14, 18, 4.5)), detail(rect(9, 7.5, 6, 9, 2.2))]


@icon("princess-cut", CAT, "Top view of a square gem with a diamond table and facets running to the corners.",
      tags=["princess cut", "square gem", "square diamond", "facets", "gemstone", "jewel"])
def _(S):
    diamond = [(12, 7), (17, 12), (12, 17), (7, 12)]
    return [shell(rect(3.5, 3.5, 17, 17, S.R * 0.4)), detail(poly(diamond, closed=True, r=S.r * 0.3)),
            detail(seg(4, 4, 9.5, 9.5)), detail(seg(20, 4, 14.5, 9.5)), detail(seg(4, 20, 9.5, 14.5)),
            detail(seg(20, 20, 14.5, 14.5))]


_PEAR = "M12 2.5C14.5 7 18.5 9.5 18.5 14.5A6.5 6.5 0 0 1 5.5 14.5C5.5 9.5 9.5 7 12 2.5Z"


@icon("pear-cut", CAT, "Top view of a teardrop shaped gem with a small table and facet lines.",
      tags=["pear cut", "teardrop gem", "gemstone", "jewel", "facets", "pendant"])
def _(S):
    return [shell(_PEAR), detail(scl(_PEAR, 0.42, 12, 13.5)), detail(seg(12, 3, 12, 8.6)), detail(seg(12, 18.4, 12, 21)),
            detail(seg(5.5, 14.5, 9.4, 14.5)), detail(seg(14.6, 14.5, 18.5, 14.5))]


_MARQ = "M12 2.5C22 7 22 17 12 21.5C2 17 2 7 12 2.5Z"


@icon("marquise-cut", CAT, "Top view of a pointed football shaped gem with a long table and facet lines.",
      tags=["marquise cut", "navette", "boat shaped gem", "gemstone", "jewel", "facets"])
def _(S):
    table = poly([(12, 7.5), (15.6, 12), (12, 16.5), (8.4, 12)], closed=True) if S.name == "line" else scl(_MARQ, 0.45, 12, 12)
    return [shell(_MARQ), detail(table), detail(seg(12, 3, 12, 7.3)), detail(seg(12, 16.7, 12, 21)),
            detail(seg(5.5, 12, 8.7, 12)), detail(seg(15.3, 12, 18.5, 12))]


_OVAL = ellipse(12, 12, 7.5, 9.5)


@icon("oval-cut", CAT, "Top view of an oval gem with a central table and facet lines.",
      tags=["oval cut", "oval gem", "gemstone", "jewel", "facets", "diamond"])
def _(S):
    if S.name == "line":
        ang = [-90 + k * 30 for k in range(12)]
        girdle = poly([(12 + 7.5 * math.cos(math.radians(a)), 12 + 9.5 * math.sin(math.radians(a))) for a in ang], closed=True)
        table = poly([(12 + 3.3 * math.cos(math.radians(a)), 12 + 4.6 * math.sin(math.radians(a))) for a in ang[::2]], closed=True)
    else:
        girdle, table = _OVAL, ellipse(12, 12, 3.3, 4.6)
    return [shell(girdle), detail(table), detail(seg(12, 3, 12, 7.4)), detail(seg(12, 16.6, 12, 21)),
            detail(seg(4.5, 12, 8.7, 12)), detail(seg(15.3, 12, 19.5, 12))]


@icon("cushion-cut", CAT, "Top view of a rounded square gem with a table and facets running to the soft corners.",
      tags=["cushion cut", "pillow cut", "rounded square gem", "gemstone", "jewel", "facets"])
def _(S):
    rx = L(S, 4.5, 6.5)
    return [shell(rect(3.5, 3.5, 17, 17, rx)), detail(rect(8.5, 8.5, 7, 7, L(S, 0.5, 2))),
            detail(seg(5.6, 5.6, 8.5, 8.5)), detail(seg(18.4, 5.6, 15.5, 8.5)), detail(seg(5.6, 18.4, 8.5, 15.5)),
            detail(seg(18.4, 18.4, 15.5, 15.5))]


_TRI = "M12 3A26 26 0 0 1 21 19A26 26 0 0 1 3 19A26 26 0 0 1 12 3Z"


@icon("trillion-cut", CAT, "Top view of a triangular gem with gently curved sides and a small table.",
      tags=["trillion cut", "triangle gem", "trilliant", "gemstone", "jewel", "facets"])
def _(S):
    c = (12, 13.7)

    def tv(p):
        return (c[0] + 0.45 * (p[0] - c[0]), c[1] + 0.45 * (p[1] - c[1]))
    verts = [(12, 3), (21, 19), (3, 19)]
    girdle = poly(verts, closed=True, r=0) if S.name == "line" else _TRI
    table = poly([tv(v) for v in verts], closed=True) if S.name == "line" else scl(_TRI, 0.45, *c)
    return [shell(girdle), detail(table)] + facets(verts, [tv(v) for v in verts])


@icon("baguette-cut", CAT, "Top view of a long narrow rectangular gem with clipped corners and step facets.",
      tags=["baguette cut", "step cut", "rectangular gem", "gemstone", "jewel", "facets"])
def _(S):
    pts = [(8, 3), (16, 3), (18, 5), (18, 19), (16, 21), (8, 21), (6, 19), (6, 5)]
    body = poly(pts, closed=True) if S.name == "line" else rect(6, 3, 12, 18, 3.5)
    return [shell(body), detail(seg(6, 8, 18, 8)), detail(seg(6, 16, 18, 16))]


@icon("heart-shaped-gem", CAT, "Top view of a faceted gem in a heart outline with a small table.",
      tags=["heart cut", "heart gem", "gemstone", "jewel", "love", "facets", "valentine"])
def _(S):
    heart = "M12 21C5 15.8 3 12 3 8.3A4.6 4.6 0 0 1 12 6.6A4.6 4.6 0 0 1 21 8.3C21 12 19 15.8 12 21Z"
    return [shell(heart), detail(scl(heart, 0.4, 12, 12.5)), detail(seg(12, 6.8, 12, 9.6)), detail(seg(12, 15.6, 12, 20.3))]


@icon("mineral-specimen", CAT, "Rock specimen with a crystal point standing on a small display plinth with a label.",
      tags=["mineral specimen", "rock collection", "museum", "display", "geology", "sample", "rock"])
def _(S):
    rock = [(4.5, 13.5), (5.5, 8.5), (9, 6.5), (12, 8), (14.5, 3.5), (18.5, 8.5), (19.5, 13.5)]
    return [shell(poly(rock, closed=True, r=S.r * 0.8)), shell(rect(3, 15, 18, 6, min(S.R, 1.5))),
            detail(seg(8.5, 18, 15.5, 18))]


# ============================================================================ sky, sun paths and light

HORIZON = 17  # shared horizon line for the sun-path scenes
MOON = "M20.5 14.5A8.5 8.5 0 1 1 9.5 3.5A7 7 0 0 0 20.5 14.5Z"


def place(d, k, tx, ty):
    """Scale path d by k about the origin, then move it by (tx, ty)."""
    return path_to_d(transform_path(P(d), (k, 0, 0, k, tx, ty)))


def moon_at(cx, cy, size):
    """Crescent moon of about `size` px centred on (cx, cy)."""
    k = size / 17.0
    return place(MOON, k, cx - 12 * k, cy - 12 * k)


def half_sun(cx, y, r):
    return f"M{fmt(cx - r)} {fmt(y)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx + r)} {fmt(y)}Z"


def ray(cx, cy, r0, r1, deg):
    a = polar(cx, cy, r0, deg)
    b = polar(cx, cy, r1, deg)
    return seg(a[0], a[1], b[0], b[1])


@icon("aurora", CAT, "Wavy vertical curtains of light hanging in the night sky over a dark line of hills.",
      tags=["aurora", "northern lights", "aurora borealis", "polar lights", "night sky", "southern lights"])
def _(S):
    def curtain(x0, y0, y1, amp, phase):
        n = 7
        pts = [(x0 + amp * math.sin(phase + i * 0.95), y0 + (y1 - y0) * i / (n - 1)) for i in range(n)]
        return smooth(pts)
    return [line(curtain(5.5, 4, 14, 1.5, 0.3)), line(curtain(11.5, 2.5, 14, 1.6, 2.2)), line(curtain(17.5, 4, 14, 1.5, 4.0)),
            dot(21, 4, 1.1),
            line(poly([(2, 20.5), (7, 17), (11, 19.5), (16, 16.5), (22, 20.5)], r=S.r))]


@icon("sun-halo", CAT, "Sun disk ringed by a large thin broken circle of ice-crystal light.",
      tags=["sun halo", "22 degree halo", "ice crystals", "sky optics", "ring around the sun", "atmospheric optics"])
def _(S):
    parts = [dot(12, 12, 3.2)]
    for c in (0, 90, 180, 270):
        parts.append(line(arc(12, 12, 9, c - 32, c + 32)))
    return parts


@icon("sun-dog", CAT, "Sun on a faint halo ring with a bright spot on the ring at each side.",
      tags=["sun dog", "parhelion", "mock sun", "sky optics", "halo", "atmospheric optics"])
def _(S):
    return [dot(12, 12, 3), line(arc(12, 12, 8.8, 212, 328)), line(arc(12, 12, 8.8, 32, 148)),
            dot(3.3, 12, 1.9), dot(20.7, 12, 1.9)]


@icon("light-pillar", CAT, "Tall narrow beam of light rising straight up from a glow on the horizon.",
      tags=["light pillar", "sun pillar", "beam", "sky optics", "ice crystals", "atmospheric optics"])
def _(S):
    beam = L(S, poly([(9.5, 16.5), (9.5, 3), (14.5, 3), (14.5, 16.5)], closed=True),
             rect(9.5, 3, 5, 13.5, 2.5))
    return [shell(beam), line(seg(2, 20, 22, 20)), line(arc(12, 20, 8, 195, 232)), line(arc(12, 20, 8, 308, 345))]


@icon("crepuscular-rays", CAT, "Sun hidden behind a cloud with straight rays fanning down past it.",
      tags=["crepuscular rays", "sunbeams", "god rays", "light shafts", "cloud", "sky optics"])
def _(S):
    cloud = L(S, "M5.5 9.5H18.5A3 3 0 0 0 18.5 3.5A4 4 0 0 0 11.5 2.5A3.5 3.5 0 0 0 7 5A2.3 2.3 0 0 0 5.5 9.5Z",
              "M6 9.5H18.5A3 3 0 0 0 18.5 3.5A4 4 0 0 0 11.5 2.5A3.5 3.5 0 0 0 7 5A2.3 2.3 0 0 0 6 9.5Z")
    return [shell(cloud)] + [line(ray(12, 6, 6.5, 14.5, a)) for a in (48, 69, 90, 111, 132)]


@icon("double-rainbow", CAT, "Two concentric rainbow arcs, the larger one arching over the smaller, above a horizon line.",
      tags=["double rainbow", "rainbow", "weather", "sky optics", "secondary rainbow", "after rain"])
def _(S):
    return [line(arc(12, 19, 9.5, 180, 360)), line(arc(12, 19, 5, 180, 360)), line(seg(2, 19, 22, 19))]


@icon("moonrise", CAT, "Half moon with craters rising over the horizon with an upward arrow beside it.",
      tags=["moonrise", "moon rising", "evening", "night", "horizon", "lunar"])
def _(S):
    return [shell(half_sun(9, HORIZON, 5.5)), line(seg(2, HORIZON, 22, HORIZON)), line(seg(6, 21, 16, 21)),
            dot(8.2, 13.6, 1), line(seg(19, 12, 19, 5)), line(poly([(16.7, 7.3), (19, 5), (21.3, 7.3)], r=S.r * 0.5))]


@icon("golden-hour", CAT, "Low sun with horizontal glow bands cutting across its face above the horizon.",
      tags=["golden hour", "magic hour", "sunset", "sunrise", "warm light", "photography"])
def _(S):
    return [shell(half_sun(12, HORIZON, 7)), detail(seg(5, 13.3, 19, 13.3)), line(seg(2, HORIZON, 22, HORIZON)),
            line(seg(6, 20.5, 18, 20.5))]


@icon("blue-hour", CAT, "Horizon line with a faint glow rising from the hidden sun and a few stars appearing above.",
      tags=["blue hour", "twilight", "dusk", "dawn", "evening sky", "photography"])
def _(S):
    return [line(seg(2, 17, 22, 17)), line(ray(12, 17, 3.5, 7, 235)), line(ray(12, 17, 3.5, 7, 270)),
            line(ray(12, 17, 3.5, 7, 305)), line(seg(6, 21, 18, 21)),
            spark(S, 5.5, 6.5, 3, 0.9), spark(S, 18.5, 6, 2.4, 0.8), dot(12, 3.8, 1.1)]


@icon("midnight-sun", CAT, "Sun sitting low above the horizon beside a small clock pointing to twelve.",
      tags=["midnight sun", "polar day", "arctic summer", "24 hour daylight", "north", "clock"])
def _(S):
    return [shell(half_sun(8, HORIZON, 5)), line(seg(2, HORIZON, 22, HORIZON)), line(seg(5, 21, 15, 21)),
            shell(circle(16.5, 7.5, 4.5)), line(seg(16.5, 7.5, 16.5, 4.8))]


@icon("polar-night", CAT, "Crescent moon and stars over snowy ground with no sun in the sky.",
      tags=["polar night", "arctic winter", "dark season", "moon", "stars", "snow"])
def _(S):
    return [shell(moon_at(8.5, 8, 9.5)), spark(S, 17.5, 6, 3, 0.9), dot(15, 12.5, 1.1),
            line("M2 19C6 15.5 10 16 13 18C16 20 19.5 17.5 22 17.5")]


def arc_pts(cx, cy, r, a0, a1):
    return polar(cx, cy, r, a0), polar(cx, cy, r, a1)


@icon("summer-solstice", CAT, "Sun at the top of a tall arching path above the horizon, marking the longest day.",
      tags=["summer solstice", "longest day", "midsummer", "sun path", "june", "astronomy"])
def _(S):
    return [shell(circle(12, 9.5, 2.6)), line(arc(12, 19, 9.5, 180, 238)), line(arc(12, 19, 9.5, 302, 360)),
            line(seg(2, 19, 22, 19)), line(seg(12, 2.5, 12, 4.2))]


@icon("winter-solstice", CAT, "Sun low on a short flat arc over the horizon with a snowflake above, marking the shortest day.",
      tags=["winter solstice", "shortest day", "midwinter", "sun path", "december", "astronomy"])
def _(S):
    def el(a):
        return (12 + 9.5 * math.cos(math.radians(a)), 19 + 4 * math.sin(math.radians(a)))
    left = smooth([el(a) for a in range(180, 236, 11)])
    right = smooth([el(a) for a in range(305, 361, 11)])
    flake = [line(seg(*polar(12, 6, 3.3, a), *polar(12, 6, 3.3, a + 180))) for a in (90, 30, 150)]
    return [shell(circle(12, 15, 2.2)), line(left), line(right), line(seg(2, 19, 22, 19))] + flake


@icon("equinox", CAT, "Circle split exactly in half, a sun on one side and a moon on the other, for equal day and night.",
      tags=["equinox", "equal day and night", "spring equinox", "autumn equinox", "sun and moon", "astronomy"])
def _(S):
    rim = poly(regular(12, 12, 9.5, 12, -90), closed=True) if S.name == "line" else circle(12, 12, 9.5)
    return [shell(rim), detail(seg(12, 2.5, 12, 21.5)), dot(7.4, 12, 2.0),
            Part("solid", moon_at(16.8, 12, 5.5))]


@icon("horizon", CAT, "Long horizon line with a small half sun on it and ground marks below.",
      tags=["horizon", "skyline", "sky and ground", "edge of the world", "distance", "landscape"])
def _(S):
    return [shell(half_sun(12, 14, 4)), line(seg(2, 14, 22, 14)), line(seg(5, 18, 9, 18)), line(seg(12, 21, 19, 21)),
            line(seg(15, 18, 19, 18))]


@icon("zenith", CAT, "Dome of sky over the ground with a marked point straight overhead and a dashed plumb line.",
      tags=["zenith", "overhead", "straight up", "sky dome", "astronomy", "altitude"])
def _(S):
    return [line(arc(12, 19, 9.5, 180, 360)), line(seg(2, 19, 22, 19)), dot(12, 9.5, 2.1),
            line(seg(12, 13, 12, 14.7)), line(seg(12, 16.7, 12, 19))]


@icon("star-trails", CAT, "Concentric curved star streaks circling a central point over the horizon.",
      tags=["star trails", "long exposure", "night sky", "polaris", "astrophotography", "stars"])
def _(S):
    return [dot(12, 10.5, 1.3), line(arc(12, 10.5, 4.3, 190, 440)), line(arc(12, 10.5, 7.6, 215, 420)),
            line(seg(2, 21, 22, 21))]


# ============================================================================ cloud types

def bumps_row(x0, x1, y, n, up=True):
    """Row of n semicircular bumps on the line y (open path)."""
    r = (x1 - x0) / (2 * n)
    d = f"M{fmt(x0)} {fmt(y)}"
    for k in range(n):
        d += f"A{fmt(r)} {fmt(r)} 0 0 {1 if up else 0} {fmt(x0 + (k + 1) * 2 * r)} {fmt(y)}"
    return d


@icon("mackerel-sky", CAT, "Rows of small rounded cloudlets packed in a rippled pattern across the sky.",
      tags=["mackerel sky", "cirrocumulus", "altocumulus", "cloud ripples", "weather", "sky"])
def _(S):
    return [line(bumps_row(2.5, 21.5, 8.5, 4)), line(bumps_row(5.5, 18.5, 14.5, 3)), line(bumps_row(2.5, 21.5, 20.5, 4))]


@icon("cumulus-cloud", CAT, "Fair weather cumulus with rounded puffy lobes and a flat base.",
      tags=["cumulus", "fair weather cloud", "puffy cloud", "cotton cloud", "weather", "sky"])
def _(S):
    body = L(S, "M3.5 18.5A3.5 3.5 0 0 1 4.6 11.7A4.3 4.3 0 0 1 9.3 7.2A5 5 0 0 1 17.6 8.3A3.6 3.6 0 0 1 19.6 13.4A3 3 0 0 1 19.3 18.5Z",
            "M6.5 18.5A3.5 3.5 0 0 1 4.6 11.7A4.3 4.3 0 0 1 9.3 7.2A5 5 0 0 1 17.6 8.3A3.6 3.6 0 0 1 19.6 13.4A3 3 0 0 1 17.5 18.5Z")
    return [shell(body), detail("M8.3 13.3A2.2 2.2 0 0 1 10.6 11.4"), detail("M15.5 14.6A2 2 0 0 0 13.4 12.8")]


@icon("cumulonimbus", CAT, "Towering storm cloud whose top flattens into a wide anvil above a dark base.",
      tags=["cumulonimbus", "thunderstorm cloud", "anvil cloud", "storm", "weather", "sky"])
def _(S):
    d = ("M9 9.5C5 9.5 2.5 8.5 2.5 6.5C2.5 4.7 5 4.3 7 4.6C9 3 15 3 17 4.6C19 4.3 21.5 4.7 21.5 6.5C21.5 8.5 19 9.5 15 9.5"
         "C17.4 11.5 17.6 14 16.6 16C17.6 17 17.6 19 16 20H8C6.4 19 6.4 17 7.4 16C6.4 14 6.6 11.5 9 9.5Z")
    return [shell(d)]


@icon("cirrus-cloud", CAT, "Thin wispy cloud streaks that hook upward at their ends.",
      tags=["cirrus", "wispy cloud", "mares tails", "high cloud", "weather", "sky"])
def _(S):
    return [line("M3 8H13.5C17.5 8 19.8 6 18.6 4"), line("M7 13H21"), line("M3 18H13C16.5 18 18 19.8 17.2 21.5")]


@icon("stratus-cloud", CAT, "Flat uniform layers of grey cloud stretched in staggered bands.",
      tags=["stratus", "layer cloud", "overcast", "grey sky", "low cloud", "weather"])
def _(S):
    rx = L(S, 0.6, 1.75)
    return [shell(rect(2, 4.5, 15, 3.5, rx)), shell(rect(7, 10.25, 15, 3.5, rx)), shell(rect(3, 16, 16, 3.5, rx))]


@icon("lenticular-cloud", CAT, "Smooth lens-shaped cloud discs stacked above a mountain peak.",
      tags=["lenticular cloud", "lens cloud", "ufo cloud", "wave cloud", "mountain", "weather"])
def _(S):
    big = "M2.5 6C6.5 2.8 17.5 2.8 21.5 6C17.5 9.2 6.5 9.2 2.5 6Z"
    small = "M5.5 12.5C8.5 10.6 15.5 10.6 18.5 12.5C15.5 14.4 8.5 14.4 5.5 12.5Z"
    return [shell(big), shell(small), line(poly([(2, 21), (9, 16.5), (12, 18.5), (15.5, 16), (22, 21)], r=S.r))]


@icon("mammatus-cloud", CAT, "Puffy cloud base hung with a row of rounded pouches bulging downward.",
      tags=["mammatus", "pouch cloud", "storm cloud", "cloud base", "weather", "sky"])
def _(S):
    d = "M3.5 9.5A3 3 0 0 1 5.5 4.6A3.6 3.6 0 0 1 12 3.8A3.6 3.6 0 0 1 18.5 4.6A3 3 0 0 1 20.5 9.5"
    x = 20.5
    for k in range(3):
        d += f"A2.667 5.5 0 0 1 {fmt(x - 5.667)} 9.5"
        x -= 5.667
    d += "Z"
    return [shell(d)]


@icon("shelf-cloud", CAT, "Low wedge of cloud with a sloping shelf-like front edge over the horizon.",
      tags=["shelf cloud", "arcus", "gust front", "storm front", "weather", "sky"])
def _(S):
    d = L(S, "M2.5 18V11C2.5 8 6 7 8.5 8C10 5 15 5 16.5 8C19.5 8 21.5 10 21.5 13L9 18Z",
          "M2.5 16V11C2.5 8 6 7 8.5 8C10 5 15 5 16.5 8C19.5 8 21.5 10 21.5 13L21.5 13.5C21.5 14.5 20.5 15 19.5 15.3L8 18A3.5 3.5 0 0 1 2.5 16Z")
    return [shell(d), line(seg(2, 21, 22, 21))]


# ============================================================================ atmosphere diagrams

def earth_arcs(S, cx, cy, radii, half_w=9.5):
    parts = []
    for r in radii:
        th = math.degrees(math.asin(min(1, half_w / r)))
        parts.append(line(arc(cx, cy, r, 270 - th, 270 + th)))
    return parts


@icon("atmosphere-layers", CAT, "Curved edge of the Earth with stacked arcs for the layers of the atmosphere above it.",
      tags=["atmosphere", "troposphere", "stratosphere", "layers of the atmosphere", "earth", "sky"])
def _(S):
    cx, cy = 12, 25
    ground = f"M{fmt(cx - 6.3)} 22A7 7 0 0 1 {fmt(cx + 6.3)} 22Z"
    return [shell(ground)] + earth_arcs(S, cx, cy, (11, 15, 19))


@icon("ozone-layer", CAT, "Globe wrapped by a protective arc shell with sun rays arriving from above.",
      tags=["ozone layer", "uv protection", "atmosphere", "sun rays", "earth", "environment"])
def _(S):
    return [shell(circle(12, 18, 3.6)), line(arc(12, 18, 7.4, 195, 345))] + [
        line(ray(12, 18, 10.4, 15.2, a)) for a in (238, 270, 302)]


@icon("ozone-hole", CAT, "Globe seen from above the pole with a dark oval gap torn in its outer shell ring.",
      tags=["ozone hole", "ozone depletion", "antarctica", "atmosphere", "pole", "environment"])
def _(S):
    ang = math.radians(55)
    hole = path_to_d(transform_path(P(ellipse(0, 0, 4, 2.2)), (math.cos(ang), math.sin(ang), -math.sin(ang), math.cos(ang),
                                                                 *polar(12, 12, 9, -35))))
    return [shell(circle(12, 12, 4.3)), line(arc(12, 12, 9, 15, 280)), dot(12, 12, 1.2), Part("solid", hole)]


@icon("rain-shadow", CAT, "Mountain with a rain cloud over its wet windward slope and a sunny, bare dry slope beyond.",
      tags=["rain shadow", "orographic rain", "mountain", "dry side", "windward", "climate"])
def _(S):
    cloud = "M4 8.5H9.5A2 2 0 0 0 9.8 4.6A3 3 0 0 0 4.3 5A1.8 1.8 0 0 0 4 8.5Z"
    return [shell(poly([(3, 21), (13, 7.5), (22, 21)], closed=True, r=S.r)), shell(cloud),
            line(seg(4.6, 11.2, 3.8, 13.2)), line(seg(8, 11.2, 7.2, 13.2)),
            dot(19, 5.5, 2.2)]


@icon("dust-devil", CAT, "Narrow twisting column of dust spiralling up from flat dry ground.",
      tags=["dust devil", "whirlwind", "dust whirl", "desert", "wind", "weather"])
def _(S):
    rows = [(3.5, 7.5, 16.5), (8, 6.5, 15.5), (12.5, 7.5, 16.5), (17, 8.5, 15.5)]
    parts = [line(f"M{fmt(x0)} {fmt(y)}Q{fmt((x0 + x1) / 2)} {fmt(y + 2.4)} {fmt(x1)} {fmt(y)}") for y, x0, x1 in rows]
    return parts + [line(seg(3, 21, 21, 21)), dot(5.5, 17.8, 1), dot(19, 18.4, 1)]
