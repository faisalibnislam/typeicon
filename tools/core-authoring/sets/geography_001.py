"""TypeIcon Core: geography (batch 001) - map furniture, projections, location marks, surveying and landforms."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, polar

CAT = "geography"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def dashes(x1, y1, x2, y2, dash=2.5, gap=2.5, start=0.0):
    """Dashed straight line as one multi-subpath d-string."""
    ln = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / ln, (y2 - y1) / ln
    out, t = [], start
    while t < ln - 0.3:
        e = min(ln, t + dash)
        out.append(f"M{fmt(x1 + ux * t)} {fmt(y1 + uy * t)}L{fmt(x1 + ux * e)} {fmt(y1 + uy * e)}")
        t += dash + gap
    return "".join(out)


def dash_arc(cx, cy, r, a0, a1, n, frac=0.55):
    """n dashes spread over an arc from angle a0 to a1 (degrees, clockwise on screen)."""
    step = (a1 - a0) / n
    return "".join(arc(cx, cy, r, a0 + i * step, a0 + i * step + step * frac) for i in range(n))


def smooth(points, closed=True, tension=0.5):
    """Smooth Catmull-Rom style path through points (closed by default)."""
    n = len(points)
    d = f"M{fmt(points[0][0])} {fmt(points[0][1])}"
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = points[(i - 1) % n] if (closed or i > 0) else points[0]
        p1 = points[i]
        p2 = points[(i + 1) % n]
        p3 = points[(i + 2) % n] if (closed or i + 2 < n) else points[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) * tension / 3 * 2 / 2, p1[1] + (p2[1] - p0[1]) * tension / 3 * 2 / 2)
        c2 = (p2[0] - (p3[0] - p1[0]) * tension / 3 * 2 / 2, p2[1] - (p3[1] - p1[1]) * tension / 3 * 2 / 2)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d + ("Z" if closed else "")


def pin_d(cx, cy, r):
    d = r * 2.4
    a = math.degrees(math.acos(r / d))
    p1, p2 = polar(cx, cy, r, 90 + a), polar(cx, cy, r, 90 - a)
    return f"M{fmt(cx)} {fmt(cy + d)}L{fmt(p1[0])} {fmt(p1[1])}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(p2[0])} {fmt(p2[1])}Z"


def pin(cx, cy, r, S, hole=None):
    """Map pin: head circle of radius r centred (cx, cy), tip below. Returns [shell, dot]."""
    parts = [shell(pin_d(cx, cy, r))]
    h = r * 0.38 if hole is None else hole
    if h > 0:
        parts.append(dot(cx, cy, h))
    return parts


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def globe_outline(cx=12, cy=12, r=9):
    return circle(cx, cy, r)


def lat_line(y, cx=12, cy=12, r=9):
    hw = math.sqrt(r * r - (y - cy) ** 2)
    return seg(cx - hw, y, cx + hw, y)


# ============================================================================ map furniture

@icon("map-legend", CAT, "Framed legend box with three rows, each a small symbol beside a text bar",
      tags=["map key", "legend", "key", "symbols", "cartography", "explanation"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        sq(6, 6.5, 3, 3), detail(seg(11.5, 8, 18, 8)),
        detail(seg(6, 12, 9, 12)), detail(seg(11.5, 12, 18, 12)),
        dot(7.5, 16, 1.5), detail(seg(11.5, 16, 18, 16)),
    ]


@icon("scale-bar", CAT, "Horizontal map scale bar of alternating filled and empty segments with ticks above",
      tags=["map scale", "scale", "distance", "cartography", "ruler", "kilometers", "miles"])
def _(S):
    return [
        shell(rect(3, 13, 18, 6, L(S, 0, 1.5))),
        sq(4, 14, 4, 4), sq(16, 14, 4, 4),
        detail(seg(9, 13, 9, 19)), detail(seg(15, 13, 15, 19)),
        line(seg(3, 4.5, 3, 9)), line(seg(12, 6.5, 12, 9)), line(seg(21, 4.5, 21, 9)),
    ]


@icon("north-arrow", CAT, "Slim map arrow pointing up with the letter N above its tip",
      tags=["north", "compass", "map arrow", "orientation", "cartography", "direction"])
def _(S):
    return [
        line(poly([(9, 8), (9, 3.5), (15, 8), (15, 3.5)], r=0)),
        shell(poly([(12, 11), (17, 21), (12, 17.6), (7, 21)], closed=True, r=S.r * 0.5)),
    ]


@icon("map-inset", CAT, "Map frame with a coastline and a small boxed inset map in one corner",
      tags=["inset map", "locator", "detail map", "cartography", "overview", "zoom"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail("M3 14C7 13 8 16.5 10.5 17.5C12.5 18.3 12 20 12.5 21"),
        detail(rect(11.5, 6.5, 6, 5, 0)),
    ]


@icon("map-cartouche", CAT, "Decorative banner with folded ends around a blank title plate, as on antique maps",
      tags=["title banner", "ribbon", "scroll", "antique map", "cartography", "label", "title"])
def _(S):
    return [
        shell(rect(6, 6.5, 12, 11, L(S, 0, 2))),
        line(poly([(6, 10), (2.5, 10), (4.5, 14.5), (2.5, 19), (6, 19)], r=S.r * 0.6)),
        line(poly([(18, 10), (21.5, 10), (19.5, 14.5), (21.5, 19), (18, 19)], r=S.r * 0.6)),
        detail(seg(9.5, 12, 14.5, 12)),
    ]


@icon("contour-lines", CAT, "Nested irregular closed loops like a hill on a topographic map",
      tags=["topographic", "elevation", "hill", "relief", "height lines", "topo map", "terrain"])
def _(S):
    if S.name == "line":
        outer = poly([(3, 11), (5, 5.5), (11, 3.5), (18, 5), (21.5, 10.5), (19.5, 18), (13, 21), (6, 19)], closed=True)
        mid = poly([(8, 11.5), (9.5, 8), (13.5, 8), (16, 11), (14.5, 15.5), (10.5, 16)], closed=True)
    else:
        outer = smooth([(3, 11), (5, 5.5), (11, 3.5), (18, 5), (21.5, 10.5), (19.5, 18), (13, 21), (6, 19)])
        mid = smooth([(8, 11.5), (9.5, 8), (13.5, 8), (16, 11), (14.5, 15.5), (10.5, 16)])
    return [shell(outer), detail(mid), dot(12, 12, 1.2)]


@icon("survey-benchmark", CAT, "Round survey marker disk seen from above with a triangle and centre point",
      tags=["survey marker", "benchmark", "geodetic", "control point", "elevation mark", "surveying", "datum"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(poly([(12, 6.5), (16.5, 15.5), (7.5, 15.5)], closed=True, r=S.r * 0.6)),
        dot(12, 12.6, 1.1),
    ]


@icon("map-grid-reference", CAT, "Map square split into a three by three grid with one cell shaded",
      tags=["grid reference", "grid square", "coordinates", "cell", "cartography", "index map"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
        detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15)),
        sq(15, 15, 5, 5),
    ]


@icon("boundary-stone", CAT, "Short upright stone with a rounded top and a carved line, standing on the ground",
      tags=["boundary marker", "border stone", "landmark", "property line", "survey", "marker stone", "milestone"])
def _(S):
    stone = "M7.5 19V9.5C7.5 6.8 9.4 4.5 12 4.5C14.6 4.5 16.5 6.8 16.5 9.5V19Z"
    return [shell(stone), detail(seg(12, 9, 12, 14)), line(seg(3, 21.5, 21, 21.5))]


@icon("border-checkpoint", CAT, "Small guard booth beside a barrier arm lowered across a road",
      tags=["border crossing", "customs", "frontier", "barrier", "gate", "toll", "border control"])
def _(S):
    return [
        shell(rect(3, 5, 7, 14, L(S, 0, 1.5))),
        detail(seg(5.5, 9, 7.5, 9)),
        shell(rect(11.5, 11, 9.5, 4, 0)),
        detail(seg(15, 11, 15, 15)), detail(seg(18, 11, 18, 15)),
        line(seg(3, 21.5, 21, 21.5)),
    ]


@icon("tripoint", CAT, "Three dash dot boundary lines meeting at a marker post in the centre",
      tags=["boundary", "border", "three countries", "junction", "frontier", "cartography", "meeting point"])
def _(S):
    parts = [shell(circle(12, 12, 2.8))]
    for ang in (90, 210, 330):
        a0, a1 = polar(12, 12, 5.8, ang), polar(12, 12, 8.6, ang)
        b0, b1 = polar(12, 12, 10.2, ang), polar(12, 12, 10.9, ang)
        parts.append(line(seg(*a0, *a1)))
        parts.append(line(seg(*b0, *b1)))
    return parts


@icon("capital-city-marker", CAT, "Map symbol of a five pointed star inside a circle",
      tags=["capital", "capital city", "map symbol", "government seat", "star in circle", "cartography"])
def _(S):
    star = []
    for i in range(10):
        rr_ = 5.6 if i % 2 == 0 else 2.4
        star.append(polar(12, 12.4, rr_, -90 + i * 36))
    return [shell(circle(12, 12, 9)), Part("dot", poly(star, closed=True, r=S.r * 0.4))]


@icon("city-marker", CAT, "Map symbol of a solid centre mark inside a ring",
      tags=["city", "town", "settlement", "map symbol", "ring dot", "cartography", "place"])
def _(S):
    mark = circle(12, 12, 3.6) if S.name == "rounded" else rect(8.5, 8.5, 7, 7)
    return [shell(circle(12, 12, 8.5)), Part("dot", mark)]


@icon("choropleth-map", CAT, "Map split into four adjacent regions with different shading densities",
      tags=["thematic map", "shaded map", "regions", "density map", "statistics", "data map", "cartography"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(poly([(12, 3), (11.5, 12), (13, 21)])),
        detail(poly([(3, 12.5), (11.5, 12), (21, 13)])),
        Part("dot", poly([(4, 4), (10.5, 4), (10.3, 10.5), (4, 11)], closed=True)),
        dot(17, 7.5, 1.3),
        detail(seg(14.5, 19.5, 19.5, 14.5)),
    ]


def loop(cx, cy, radii, S, start=-90.0):
    """Closed irregular ring through given radii; angular for Line, smooth for Rounded."""
    n = len(radii)
    pts = [polar(cx, cy, r, start + i * 360 / n) for i, r in enumerate(radii)]
    return poly(pts, closed=True) if S.name == "line" else smooth(pts)


def thick(d, w, S):
    return path_to_d(ST(d, w, S.cap, S.join))


@icon("cartogram", CAT, "World shown as solid blocks of different sizes instead of real coastlines",
      tags=["data map", "distorted map", "blocks", "tile map", "statistics", "world map", "infographic"])
def _(S):
    rx = L(S, 0, 2)
    return [shell(rect(3, 5, 8, 8, rx)), shell(rect(15, 3, 6, 6, rx)), shell(rect(15, 13, 6, 8, rx)),
            shell(rect(3, 17, 8, 4, rx))]


@icon("flow-map", CAT, "Origin dot with a thick and a thin curved arrow flowing out to other places",
      tags=["migration map", "flows", "arrows", "trade routes", "movement", "origin destination", "data map"])
def _(S):
    return [
        dot(4.5, 12.5, 2.2),
        solid(thick("M6.5 10C8.5 6.5 12 5.5 15 5.5", 3.6, S)),
        solid(poly([(14.5, 1.8), (21.5, 5.5), (14.5, 9.2)], closed=True, r=S.r * 0.5)),
        line("M7.5 15C11 16 14.5 18 17 19.5"),
        line(poly([(14.6, 20.5), (17.6, 19.8), (17.4, 16.8)], r=0)),
    ]


@icon("voronoi-map", CAT, "Square divided into irregular polygon cells, each with a small dot inside",
      tags=["voronoi", "territories", "catchment", "service areas", "nearest neighbor", "cells", "diagram"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(poly([(10, 3), (9, 10), (3, 13)])),
        detail(poly([(9, 10), (15, 12), (21, 8)])),
        detail(seg(15, 12, 13, 21)),
        dot(6, 7, 1.1), dot(16, 7, 1.1), dot(8, 17, 1.1), dot(18, 17, 1.1),
    ]


@icon("isochrone-map", CAT, "Map pin at the centre of two nested wobbly rings showing travel time bands",
      tags=["travel time", "reachability", "catchment", "time zones on map", "commute", "service area", "isochrone"])
def _(S):
    return [
        shell(loop(12, 12, [9.4, 8.6, 9.6, 8.4, 9.4, 8.8, 9.6, 8.8], S)),
        detail(loop(12, 12, [5.8, 5.3, 6.0, 5.2, 5.8, 5.4], S)),
        Part("dot", pin_d(12, 10.2, 1.7)),
    ]


@icon("map-centroid", CAT, "Irregular region outline with a crosshair marking its centre point",
      tags=["centroid", "center point", "region", "polygon", "gis", "geometric center", "crosshair"])
def _(S):
    region = poly([(3.5, 9), (8, 3.5), (15, 4.5), (21, 8.5), (19, 17), (13, 20.5), (6, 19)], closed=True, r=S.r)
    return [shell(region), detail(circle(12, 12, 4.2)), dot(12, 12, 1.1)]


@icon("raster-map", CAT, "Map drawn as a coarse grid of square cells with a blocky stepped coastline",
      tags=["raster", "pixels", "grid data", "gis", "cells", "bitmap map", "low resolution"])
def _(S):
    rx = L(S, 0, 1.4)
    cells = [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2)]
    return [shell(rect(2.3 + cx * 7.3, 2.3 + cy * 7.3, 5.4, 5.4, rx)) for cx, cy in cells]


@icon("relief-map", CAT, "Raised terrain model with a peak and ridges on a flat base slab",
      tags=["terrain model", "3d map", "topography", "physical map", "landform", "elevation", "raised relief"])
def _(S):
    terrain = poly([(3, 18), (3, 14), (7.5, 10), (10.5, 13), (15.5, 5), (21, 12.5), (21, 18)], closed=True, r=S.r)
    return [shell(terrain), detail(poly([(15.5, 5.5), (14.5, 10.5), (17, 13)])), line(seg(3, 21.5, 21, 21.5))]


@icon("nautical-chart", CAT, "Sea chart with a stretch of coast on one side and scattered depth soundings",
      tags=["sea chart", "marine chart", "navigation", "depth soundings", "coastline", "sailing", "hydrography"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail("M3 13C6.5 12.5 7.5 9 8 3"),
        dot(14, 8, 1.2), dot(18, 13, 1.2), dot(12.5, 16.5, 1.2), dot(8, 18, 1.2),
    ]


@icon("portolan-chart", CAT, "Old sea chart with straight rhumb lines radiating from a small compass star",
      tags=["portolan", "rhumb lines", "antique chart", "compass rose", "medieval map", "navigation", "sea chart"])
def _(S):
    cx, cy = 12, 12
    parts = [shell(rect(3, 3, 18, 18, S.R))]
    for x, y in [(3, 6), (21, 6), (3, 17), (21, 18), (12, 3), (12, 21)]:
        pass
    parts += [detail(seg(3, 7, 21, 17)), detail(seg(3, 17, 21, 7)), detail(seg(12, 3, 12, 21))]
    parts.append(Part("dot", poly([(12, 8), (13.2, 10.8), (16, 12), (13.2, 13.2), (12, 16), (10.8, 13.2), (8, 12), (10.8, 10.8)], closed=True)))
    return parts


@icon("t-and-o-map", CAT, "Circle divided by a T shape into three parts, the medieval T and O world map",
      tags=["medieval map", "mappa mundi", "world map", "three continents", "old map", "cartography", "history"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(seg(3, 12, 21, 12)), detail(seg(12, 12, 12, 21)),
        Part("dot", circle(12, 7.3, 1.3)) if S.name == "rounded" else sq(10.8, 6.1, 2.4, 2.4),
        Part("dot", circle(7.4, 16.6, 1.3)) if S.name == "rounded" else sq(6.2, 15.4, 2.4, 2.4),
        Part("dot", circle(16.6, 16.6, 1.3)) if S.name == "rounded" else sq(15.4, 15.4, 2.4, 2.4),
    ]


@icon("street-map", CAT, "City map square with a street grid and a map pin marking a place",
      tags=["city map", "streets", "roads", "directions", "navigation", "town plan", "location"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(9, 3, 9, 21)), detail(seg(3, 15, 21, 15)),
        Part("dot", pin_d(15.8, 7.6, 2.6)),
    ]


@icon("subway-map", CAT, "Transit map with two crossing lines and round station stops",
      tags=["metro map", "transit map", "underground", "rail network", "stations", "lines", "public transport"])
def _(S):
    return [
        line(poly([(3, 18), (9, 18), (15, 6), (21, 6)], r=S.r)),
        line(poly([(3, 6), (8, 6), (16, 18), (21, 18)], r=S.r)),
        shell(circle(12, 12, 2.6)),
    ]


@icon("you-are-here-map", CAT, "Map board on two legs with a bold dot and a small arrow marking the viewer's position",
      tags=["you are here", "directory", "map board", "information sign", "wayfinding", "location", "visitor map"])
def _(S):
    return [
        shell(rect(3, 3, 18, 12, L(S, 0, 2))),
        line(seg(7.5, 15, 7.5, 21.5)), line(seg(16.5, 15, 16.5, 21.5)),
        dot(8, 9, 1.6),
        detail(poly([(12, 9), (17, 9)])),
        detail(poly([(15, 7), (17, 9), (15, 11)], r=0)),
    ]


@icon("trailhead-board", CAT, "Roofed notice board on two posts showing a trail map with a dashed path",
      tags=["trail map", "hiking", "notice board", "trailhead", "park sign", "path", "outdoors"])
def _(S):
    return [
        line(poly([(2.5, 8), (12, 3), (21.5, 8)], r=S.r * 0.4)),
        shell(rect(4.5, 9, 15, 7, L(S, 0, 1))),
        line(seg(8, 16, 8, 21.5)), line(seg(16, 16, 16, 21.5)),
        detail(dashes(7.5, 14, 16.5, 11, dash=2.2, gap=2.2)),
    ]


@icon("mercator-projection", CAT, "Rectangular world grid whose rows grow taller toward the top and bottom edges",
      tags=["map projection", "world map grid", "cylindrical", "latitude", "longitude", "flat map", "distortion"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
        detail(seg(3, 10, 21, 10)), detail(seg(3, 14, 21, 14)),
    ]


# ============================================================================ projections and views

def lens(cx, top, bottom, half):
    return f"M{fmt(cx)} {fmt(top)}Q{fmt(cx + 2 * half)} {fmt((top + bottom) / 2)} {fmt(cx)} {fmt(bottom)}Q{fmt(cx - 2 * half)} {fmt((top + bottom) / 2)} {fmt(cx)} {fmt(top)}Z"


@icon("globe-gores", CAT, "Row of pointed lens-shaped map strips that would wrap into a globe",
      tags=["gores", "globe map", "unfolded globe", "map strips", "cartography", "projection", "globe making"])
def _(S):
    return [shell(lens(6, 3.5, 20.5, 3.4)), shell(lens(12, 3.5, 20.5, 3.4)), shell(lens(18, 3.5, 20.5, 3.4))]


@icon("azimuthal-projection", CAT, "Circular map centred on a pole with a ring and straight lines radiating outward",
      tags=["polar map", "azimuthal", "map projection", "circular map", "pole", "radial", "flat map"])
def _(S):
    parts = [shell(circle(12, 12, 9)), detail(circle(12, 12, 4.6)), dot(12, 12, 1.2)]
    if S.name == "line":
        parts += [detail(seg(3, 12, 7.4, 12)), detail(seg(16.6, 12, 21, 12)), detail(seg(12, 3, 12, 7.4)), detail(seg(12, 16.6, 12, 21))]
    else:
        parts += [detail(seg(5.6, 5.6, 8.7, 8.7)), detail(seg(15.3, 15.3, 18.4, 18.4)),
                  detail(seg(18.4, 5.6, 15.3, 8.7)), detail(seg(8.7, 15.3, 5.6, 18.4))]
    return parts


@icon("conic-projection", CAT, "Fan shaped map segment with curved parallels and straight meridians converging above",
      tags=["cone projection", "map projection", "lambert", "fan", "meridians", "parallels", "flat map"])
def _(S):
    ax, ay = 12, 2
    a0, a1 = 55, 125
    i0, i1 = polar(ax, ay, 8, a1), polar(ax, ay, 8, a0)
    o0, o1 = polar(ax, ay, 19, a0), polar(ax, ay, 19, a1)
    path = (f"M{fmt(i0[0])} {fmt(i0[1])}A8 8 0 0 0 {fmt(i1[0])} {fmt(i1[1])}L{fmt(o0[0])} {fmt(o0[1])}"
            f"A19 19 0 0 1 {fmt(o1[0])} {fmt(o1[1])}Z")
    mid = arc(ax, ay, 13.5, a0 - 1, a1 + 1)
    return [shell(path), detail(mid), detail(seg(*polar(ax, ay, 7, 76), *polar(ax, ay, 20, 76))),
            detail(seg(*polar(ax, ay, 7, 104), *polar(ax, ay, 20, 104)))]


@icon("interrupted-projection", CAT, "World map split into rounded lobes joined along the equator like a peeled globe",
      tags=["goode", "map projection", "peeled globe", "flat world map", "lobes", "interrupted", "cartography"])
def _(S):
    def lobe(x0, x1, up):
        rx = (x1 - x0) / 2
        ry = 8.5
        if S.name == "line":
            xm, sgn = (x0 + x1) / 2, (-1 if up else 1)
            pts = [(x0, 12), (x0 + rx * 0.3, 12 + sgn * 5.5), (xm, 12 + sgn * ry), (x1 - rx * 0.3, 12 + sgn * 5.5), (x1, 12)]
            return poly(pts, closed=True)
        sweep = 1 if up else 0
        return f"M{fmt(x0)} 12A{fmt(rx)} {fmt(ry)} 0 0 {sweep} {fmt(x1)} 12Z"
    outline = union(lobe(2.5, 11, True), lobe(11, 21.5, True), lobe(2.5, 13, False), lobe(13, 21.5, False))
    return [shell(outline), detail(seg(3, 12, 21, 12))]


@icon("icosahedral-map", CAT, "Flat world map built from joined triangles unfolded from a polyhedron",
      tags=["triangles", "icosahedron", "polyhedron map", "unfolded", "map projection", "geodesic", "flat map"])
def _(S):
    return [shell(poly([(2.5, 6), (21.5, 6), (16.75, 19), (7.25, 19)], closed=True, r=S.r * 0.5)),
            detail(poly([(7.25, 19), (12, 6), (16.75, 19)]))]


@icon("satellite-view", CAT, "Square aerial tile with irregular field patches and a tiny satellite in the corner",
      tags=["aerial view", "satellite image", "imagery", "remote sensing", "earth observation", "fields", "orbit"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(poly([(3, 15), (10, 12.5), (12, 21)])),
        detail(poly([(10, 12.5), (13, 15), (21, 14)])),
        detail(seg(14.5, 10.5, 19.5, 5.5)),
        Part("dot", poly([(17, 6.5), (18.6, 8.2), (16.9, 9.8), (15.3, 8.2)], closed=True)),
    ]


@icon("map-perspective", CAT, "Map plane tilted in perspective with small three dimensional buildings rising from it",
      tags=["3d map", "tilted map", "city view", "buildings", "isometric", "perspective view", "urban"])
def _(S):
    return [
        shell(poly([(6.5, 14), (17.5, 14), (21.5, 20.5), (2.5, 20.5)], closed=True, r=S.r * 0.6)),
        line(poly([(7.5, 14), (7.5, 7), (11.5, 7), (11.5, 14)])),
        line(poly([(13, 14), (13, 3.5), (17, 3.5), (17, 14)])),
    ]


@icon("indoor-map", CAT, "Building floor plan with several rooms and a map pin standing in one room",
      tags=["floor plan", "building map", "rooms", "indoor navigation", "mall map", "airport map", "wayfinding"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(10, 3, 10, 21)), detail(seg(10, 11, 21, 11)),
        Part("dot", pin_d(15.5, 14.2, 2.0)),
    ]


@icon("live-location", CAT, "Map pin with a curved signal arc radiating from each side",
      tags=["live tracking", "real time location", "share location", "gps", "broadcast", "position", "signal"])
def _(S):
    return pin(12, 9, 3.6, S, hole=1.2) + [
        line(arc(12, 9, 8.2, 145, 215)), line(arc(12, 9, 8.2, -35, 35)),
    ]


@icon("nearby-radius", CAT, "Solid dot at the centre of two dashed concentric circles",
      tags=["nearby", "radius", "search area", "distance ring", "around me", "range", "proximity"])
def _(S):
    return [dot(12, 12, 2.2), line(dash_arc(12, 12, 5.6, 0, 360, 6, 0.58)), line(dash_arc(12, 12, 9.5, 0, 360, 10, 0.58))]


@icon("geofence", CAT, "Dashed circular boundary on a map with a pin at its centre",
      tags=["geo fence", "virtual boundary", "perimeter", "zone", "location alert", "area trigger", "gps boundary"])
def _(S):
    return pin(12, 10, 2.8, S, hole=1.0) + [line(dash_arc(12, 12, 9.5, 0, 360, 12, 0.6))]


@icon("location-heading", CAT, "Solid dot with a wide beam spreading upward showing the direction faced",
      tags=["heading", "facing direction", "orientation", "compass beam", "you are here", "view direction", "navigation"])
def _(S):
    ax, ay, R = 12, 13.5, 10
    p1, p2 = polar(ax, ay, R, -125), polar(ax, ay, R, -55)
    wedge = f"M{ax} {ay}L{fmt(p1[0])} {fmt(p1[1])}A{R} {R} 0 0 1 {fmt(p2[0])} {fmt(p2[1])}Z"
    return [shell(wedge), solid(circle(12, 19.3, 2.4))]


@icon("map-pins-cluster", CAT, "Three overlapping map pins of different sizes grouped together",
      tags=["pins", "multiple locations", "cluster", "places", "markers", "group", "points of interest"])
def _(S):
    return [shell(pin_d(4.8, 13.5, 2.2)), shell(pin_d(19.2, 13.5, 2.2)),
            shell(pin_d(12, 8.2, 3.8)), dot(12, 8.2, 1.4)]


@icon("gps-track", CAT, "Squiggly recorded track line starting at a hollow circle and ending at a solid dot",
      tags=["route", "recorded path", "trail", "activity track", "gps", "trace", "tracking"])
def _(S):
    return [shell(circle(5, 19, 2.3)),
            line("M7.2 18.3C11 19 15 18 14.5 14.5C14 11.3 8.5 12.3 8.5 8.8C8.5 6 12 5.5 14.5 6.3"),
            solid(circle(19.3, 5.5, 2.2))]


@icon("measure-distance", CAT, "Two map pins joined by a line with a small ruler beneath",
      tags=["distance", "measure", "between places", "route length", "ruler", "how far", "map tool"])
def _(S):
    return [
        shell(pin_d(5, 6.5, 2.4)), shell(pin_d(19, 6.5, 2.4)),
        line(seg(9.2, 7.5, 14.8, 7.5)),
        shell(rect(3, 15.5, 18, 5, L(S, 0, 1.5))),
        detail(seg(8, 15.5, 8, 18.2)), detail(seg(12, 15.5, 12, 18.2)), detail(seg(16, 15.5, 16, 18.2)),
    ]


# ============================================================================ globe, bearings and surveying

def mark(S, x, y, r=1.4):
    """Small solid marker: square for Line, round for Rounded (knocked out of Filled shells)."""
    if S.name == "rounded":
        return dot(x, y, r)
    return Part("dot", rect(x - r, y - r, 2 * r, 2 * r))


def half_ellipse(cx, cy, rx, ry, y0, y1, right=True):
    """Meridian arc on the right (or left) half of an ellipse between two y values."""
    def xat(y):
        k = max(0.0, 1 - ((y - cy) / ry) ** 2)
        return cx + (1 if right else -1) * rx * math.sqrt(k)
    return f"M{fmt(xat(y0))} {fmt(y0)}A{fmt(rx)} {fmt(ry)} 0 0 {1 if right else 0} {fmt(xat(y1))} {fmt(y1)}"


def dash_poly(pts, dash=2.4, gap=2.2):
    """Dashes along a sampled polyline (list of points)."""
    out, draw, rem = [], True, dash
    cur = pts[0]
    seg_start = None
    for nxt in pts[1:]:
        dx, dy = nxt[0] - cur[0], nxt[1] - cur[1]
        ln = math.hypot(dx, dy)
        pos = 0.0
        while ln - pos > 1e-6:
            step = min(rem, ln - pos)
            a = (cur[0] + dx * pos / ln, cur[1] + dy * pos / ln)
            b = (cur[0] + dx * (pos + step) / ln, cur[1] + dy * (pos + step) / ln)
            if draw:
                out.append(f"M{fmt(a[0])} {fmt(a[1])}L{fmt(b[0])} {fmt(b[1])}")
            pos += step
            rem -= step
            if rem <= 1e-6:
                draw = not draw
                rem = dash if draw else gap
        cur = nxt
    return "".join(out)


def quad_pts(p0, p1, p2, n=30):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / n for i in range(n + 1)]]


@icon("geo-coordinates", CAT, "Globe with one latitude line and one longitude line crossing at a marked point",
      tags=["latitude", "longitude", "coordinates", "lat lng", "gps position", "globe grid", "location"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(lat_line(15)), detail(half_ellipse(12, 12, 5, 9, 3.6, 20.4)),
            mark(S, 16.6, 15, 1.6)]


@icon("longitude-lines", CAT, "Globe with curved vertical meridians and no horizontal lines",
      tags=["meridians", "longitude", "globe lines", "north south lines", "prime meridian", "earth grid", "geography"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(seg(12, 6, 12, 18)),
            detail(half_ellipse(12, 12, 6, 9, 5.5, 18.5, True)), detail(half_ellipse(12, 12, 6, 9, 5.5, 18.5, False))]


@icon("antipode", CAT, "Globe with two dots on opposite sides joined by a dashed line through the centre",
      tags=["opposite side of earth", "antipodal", "other side of the world", "globe", "dig to china", "opposite point"])
def _(S):
    return [shell(circle(12, 12, 9)), mark(S, 7.3, 7.3, 1.7), mark(S, 16.7, 16.7, 1.7),
            detail(dashes(9.6, 9.6, 14.4, 14.4, dash=1.8, gap=1.4))]


@icon("great-circle-route", CAT, "Globe with a dashed arc curving between two dots on its surface",
      tags=["flight path", "shortest route", "arc route", "air route", "geodesic", "globe", "long distance"])
def _(S):
    pts = quad_pts((6.3, 16), (12, 3), (17.7, 16))
    return [shell(circle(12, 12, 9)), mark(S, 6.3, 16, 1.6), mark(S, 17.7, 16, 1.6),
            detail(dash_poly(pts, 2.4, 2.0))]


@icon("climate-zones", CAT, "Globe split into horizontal bands with different marks for polar, temperate and tropical zones",
      tags=["climate bands", "latitude zones", "polar", "temperate", "tropical", "globe", "earth zones"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(lat_line(8.4)), detail(lat_line(15.6)),
            mark(S, 12, 5.3, 1.0), mark(S, 12, 18.8, 1.0),
            detail(poly([(7, 13.2), (9.5, 10.8), (12, 13.2), (14.5, 10.8), (17, 13.2)]))]


def head(tip, deg, size=2.3, spread=38):
    """Open arrowhead polyline: tip point, travel direction in degrees (0 = right, 90 = down)."""
    a = math.radians(deg)
    pts = []
    for sgn in (-1, 1):
        b = a + math.pi + sgn * math.radians(spread)
        pts.append((tip[0] + size * math.cos(b), tip[1] + size * math.sin(b)))
    return poly([pts[0], tip, pts[1]])


@icon("coriolis-effect", CAT, "Globe with a straight dashed path and a curved arrow bending away from it in each hemisphere",
      tags=["coriolis", "earth rotation", "wind deflection", "curved flow", "hemispheres", "globe", "weather"])
def _(S):
    return [shell(circle(12, 12, 9)),
            detail(dashes(8, 10.5, 8, 5.2, 1.8, 1.4)), detail("M8 10.5C8 7.5 11 6 15.3 6.2"), detail(head((16.3, 6.2), 5, 3.0, 42)),
            detail(dashes(16, 13.5, 16, 18.8, 1.8, 1.4)), detail("M16 13.5C16 16.5 13 18 8.7 17.8"), detail(head((7.7, 17.8), 185, 3.0, 42))]


@icon("earth-magnetic-field", CAT, "Small globe with looping field lines arching from pole to pole on both sides",
      tags=["magnetosphere", "field lines", "magnet", "earth", "poles", "geomagnetic", "compass"])
def _(S):
    return [shell(circle(12, 12, 3.6)), mark(S, 12, 12, 1.4),
            line("M12 5.5C1.5 2 1.5 22 12 18.5"), line("M12 5.5C22.5 2 22.5 22 12 18.5")]


@icon("magnetic-declination", CAT, "Two lines from one point, one tipped with a star for true north and one angled for magnetic north, with an angle arc",
      tags=["declination", "true north", "magnetic north", "compass correction", "orienteering", "bearing", "angle"])
def _(S):
    ox, oy = 6, 21
    mx, my = polar(ox, oy, 14, -50)
    star = [polar(6, 4.6, 3.1 if i % 2 == 0 else 1.3, -90 + i * 36) for i in range(10)]
    return [line(seg(ox, oy, 6, 8.5)),
            line(seg(ox, oy, mx, my)),
            line(poly([(mx - 4.6, my - 0.2), (mx, my), (mx + 0.2, my + 4.6)])),
            line(arc(ox, oy, 9, -90, -50)),
            Part("solid", poly(star, closed=True))]


@icon("compass-bearing", CAT, "Vertical north line and a second line to a target dot with a curved angle arc between them",
      tags=["bearing", "azimuth", "heading angle", "direction", "navigation", "orienteering", "degrees from north"])
def _(S):
    return [line(seg(7, 20, 7, 3.5)), line(poly([(4.5, 6), (7, 3.5), (9.5, 6)])),
            line(seg(7, 20, 16, 11)), dot(18.5, 8.5, 2.1),
            line(arc(7, 20, 7.5, -90, -45))]


def vx(x, y, S, r=2.4):
    return circle(x, y, r) if S.name == "rounded" else rect(x - r, y - r, 2 * r, 2 * r)


@icon("triangulation", CAT, "Two sighting lines from two base points meeting at a third point to form a triangle",
      tags=["surveying", "sighting", "position fixing", "triangle", "baseline", "land survey", "measurement"])
def _(S):
    return [shell(poly([(4.5, 18.5), (19.5, 18.5), (14, 5.5)], closed=True, r=S.r * 0.5)),
            solid(vx(4.5, 18.5, S)), solid(vx(19.5, 18.5, S)), solid(vx(14, 5.5, S))]


@icon("trilateration", CAT, "Three overlapping circles whose rings all cross at one marked point",
      tags=["gps", "positioning", "distance circles", "satellites", "position fix", "three circles", "locate"])
def _(S):
    return [line(circle(12, 8.4, 4.8)), line(circle(8, 15.3, 4.8)), line(circle(16, 15.3, 4.8)),
            mark(S, 12, 13.1, 2.2)]


@icon("earth-circumference", CAT, "Globe with a measuring tape wrapped around its middle",
      tags=["circumference", "earth size", "measure the earth", "equator", "tape measure", "eratosthenes", "globe"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(ellipse(12, 12, 9, 3.6)), mark(S, 12, 15.6, 1.7)]


@icon("elevation-above-sea-level", CAT, "Mountain above a wavy sea line with a vertical arrow from the water to the peak",
      tags=["altitude", "height", "sea level", "elevation", "mountain height", "above water", "metres"])
def _(S):
    return [shell(poly([(2.5, 17), (7, 6.5), (10, 12), (12.5, 9), (15.5, 17)], closed=True, r=S.r)),
            line("M2.5 20.5Q4.5 18.5 6.5 20.5T10.5 20.5T14.5 20.5T18.5 20.5"),
            line(seg(20, 4, 20, 17.5)), line(poly([(18, 6), (20, 4), (22, 6)])), line(poly([(18, 15.5), (20, 17.5), (22, 15.5)]))]


@icon("slope-gradient", CAT, "Right triangle slope with an angle arc at its base and a small percent sign above",
      tags=["gradient", "incline", "steepness", "grade", "percent slope", "angle", "rise over run"])
def _(S):
    return [shell(poly([(3, 19.5), (21, 19.5), (21, 9)], closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
            detail(arc(3, 19.5, 9.5, -30, 0)),
            dot(5.5, 5.6, 1.3), dot(10.5, 10.6, 1.3), line(seg(10.6, 5, 5.4, 11.2))]


@icon("viewshed", CAT, "Eye on a hilltop with a shaded cone showing the area visible below",
      tags=["line of sight", "visibility", "view analysis", "terrain", "eye", "gis", "sightline"])
def _(S):
    return [shell("M2.5 20.5C3.5 15.5 5.5 12.5 8 12.5C11 12.5 13 16 17 18C19 19 20.5 20 21.5 20.5Z"),
            shell(ellipse(8, 7, 3.4, 2.2)), dot(8, 7, 0.9),
            Part("solid", poly([(12, 6.5), (21.5, 6.5), (21.5, 17.5), (17, 15.5)], closed=True, r=S.r * 0.4)),
            ]


@icon("halfway-point", CAT, "Two map pins standing on a line with a star at its midpoint",
      tags=["midpoint", "meet in the middle", "halfway", "between two places", "center point", "meeting place", "star"])
def _(S):
    star = [polar(12, 15.5, 4.6 if i % 2 == 0 else 1.9, -90 + i * 36) for i in range(10)]
    return [shell(pin_d(4.5, 5.5, 2.3)), shell(pin_d(19.5, 5.5, 2.3)),
            line(seg(3, 15.5, 21, 15.5)),
            Part("solid", poly(star, closed=True, r=S.r * 0.3))]


@icon("waypoint", CAT, "Diamond marker on a dashed route line between two end dots",
      tags=["route stop", "via point", "intermediate stop", "checkpoint", "navigation", "marker", "path"])
def _(S):
    return [dot(4.5, 19.5, 1.9), dot(19.5, 4.5, 1.9),
            shell(poly([(12, 8), (16, 12), (12, 16), (8, 12)], closed=True, r=S.r * 0.4)),
            line(dashes(6.6, 17.4, 9.4, 14.6, dash=1.9, gap=1.4)),
            line(dashes(14.6, 9.4, 17.4, 6.6, dash=1.9, gap=1.4))]


@icon("compass-calibration", CAT, "Phone with a figure eight loop drawn around it",
      tags=["calibrate compass", "figure 8", "sensor calibration", "phone", "magnetometer", "wave phone", "navigation"])
def _(S):
    eight = "M12 12C14 3.5 21.5 3.5 21.5 12C21.5 20.5 14 20.5 12 12C10 3.5 2.5 3.5 2.5 12C2.5 20.5 10 20.5 12 12Z"
    ring = path_to_d(ST(eight, 2.0, S.cap, S.join, 4.0))
    cut = rect(8.2, 7.2, 7.6, 9.6, L(S, 1.5, 2.4))
    return [solid(minus(ring, cut)), shell(rect(9.7, 8.7, 4.6, 6.6, L(S, 0.6, 1.4)))]


@icon("map-bounding-box", CAT, "Dashed rectangle with square corner handles framing a small coastline shape",
      tags=["bounding box", "extent", "selection area", "crop map", "bbox", "gis", "frame"])
def _(S):
    parts = [line(dashes(5, 3.5, 19, 3.5, 2.4, 2.2)), line(dashes(5, 20.5, 19, 20.5, 2.4, 2.2)),
             line(dashes(3.5, 5.5, 3.5, 18.5, 2.4, 2.2)), line(dashes(20.5, 5.5, 20.5, 18.5, 2.4, 2.2))]
    for x, y in ((3.5, 3.5), (20.5, 3.5), (3.5, 20.5), (20.5, 20.5)):
        parts.append(Part("solid", rect(x - 1.6, y - 1.6, 3.2, 3.2, L(S, 0, 0.6))))
    parts.append(shell(poly([(8, 14.5), (9, 9.5), (13.5, 8), (16.5, 11.5), (14.5, 16)], closed=True, r=S.r)))
    return parts


@icon("map-tiles", CAT, "Square map split into a two by two grid of tiles with one tile lifted and offset",
      tags=["tiles", "map grid", "tile layer", "slippy map", "tile server", "zoom tiles", "map chunks"])
def _(S):
    rx = L(S, 0, 1.5)
    return [shell(rect(3, 4, 7.5, 7, rx)), shell(rect(13.5, 2, 7.5, 7, rx)),
            shell(rect(3, 15, 7.5, 6, rx)), shell(rect(13.5, 13, 7.5, 8, rx))]


# ============================================================================ landforms and continents

@icon("pangaea", CAT, "Globe showing one single large merged supercontinent shape",
      tags=["supercontinent", "continental drift", "ancient earth", "plate tectonics", "geology", "landmass", "history of earth"])
def _(S):
    pts = [(7.5, 9), (10, 6.3), (13.5, 7), (16.5, 9), (16, 12.5), (17, 15), (13, 17), (10, 15.5), (8, 13)]
    land = poly(pts, closed=True) if S.name == "line" else smooth(pts)
    return [shell(circle(12, 12, 9)), Part("dot", land)]


@icon("population-pyramid", CAT, "Horizontal bars widening toward the bottom on both sides of a centre gap, forming a pyramid",
      tags=["demographics", "age structure", "population chart", "age groups", "census", "statistics", "chart"])
def _(S):
    parts = []
    for y, w in ((4.5, 4.5), (9, 6.8), (13.5, 8.8), (18, 10)):
        parts.append(line(seg(10.8, y, 12 - w, y)))
        parts.append(line(seg(13.2, y, 12 + w, y)))
    return parts


@icon("treeline", CAT, "Mountain with small conifers below a dashed line and bare rock above it",
      tags=["tree line", "timberline", "alpine", "altitude limit", "forest edge", "mountain", "elevation"])
def _(S):
    mountain = poly([(3, 21), (14, 4), (21, 21)], closed=True, r=S.r)
    tree = lambda cx: poly([(cx - 1.8, 19.4), (cx, 15), (cx + 1.8, 19.4)], closed=True, r=S.r * 0.3)
    return [shell(mountain), detail(dashes(9.5, 12, 17.5, 12, 2.6, 1.4)),
            Part("dot", tree(10.5)), Part("dot", tree(14.5))]


@icon("strait", CAT, "Narrow channel of water between two land masses that almost touch",
      tags=["channel", "narrow sea", "waterway", "sound", "passage", "bosphorus", "geography"])
def _(S):
    left = poly([(2.5, 3), (8.5, 3), (9.5, 8), (10, 12), (9.5, 16), (8.5, 21), (2.5, 21)], closed=True, r=S.r)
    right = poly([(21.5, 3), (15.5, 3), (14.5, 8), (14, 12), (14.5, 16), (15.5, 21), (21.5, 21)], closed=True, r=S.r)
    return [shell(left), shell(right)]


@icon("polder", CAT, "Low flat field held below the level of the canal water by a raised dike",
      tags=["dike", "dyke", "reclaimed land", "netherlands", "below sea level", "flood defence", "farmland"])
def _(S):
    ground = poly([(2.5, 21.5), (2.5, 14.5), (5.5, 14.5), (8, 9.5), (11, 9.5), (14, 16), (21.5, 16), (21.5, 21.5)], closed=True, r=S.r * 0.6)
    return [shell(ground), line("M2.5 10.8q1.5-1.6 3 0"), line(seg(17, 11.5, 17, 13.8)), line(seg(20.2, 11.5, 20.2, 13.8))]


@icon("alluvial-fan", CAT, "Fan shaped spread of streams opening out from a mountain gap onto a plain",
      tags=["fan delta", "sediment fan", "river deposit", "landform", "piedmont", "geology", "stream spread"])
def _(S):
    ax, ay, R = 12, 7.5, 14
    p1, p2 = polar(ax, ay, R, 52), polar(ax, ay, R, 128)
    fan = f"M{ax} {ay}L{fmt(p1[0])} {fmt(p1[1])}A{R} {R} 0 0 1 {fmt(p2[0])} {fmt(p2[1])}Z"
    return [shell(fan), detail(seg(*polar(ax, ay, 4, 90), *polar(ax, ay, 9.5, 90))),
            detail(seg(*polar(ax, ay, 4.5, 68), *polar(ax, ay, 9.2, 68))), detail(seg(*polar(ax, ay, 4.5, 112), *polar(ax, ay, 9.2, 112))),
            line(poly([(2.5, 7.5), (6, 2.8), (9.3, 7.5)], r=0)), line(poly([(14.7, 7.5), (18, 2.8), (21.5, 7.5)], r=0))]


@icon("rift-valley", CAT, "Valley floor dropped between two steep parallel fault cliffs, with a downward arrow",
      tags=["graben", "fault", "tectonic valley", "rift", "escarpment", "east africa", "geology"])
def _(S):
    block = poly([(2.5, 9), (8, 9), (8.5, 16), (15.5, 16), (16, 9), (21.5, 9), (21.5, 21.5), (2.5, 21.5)], closed=True, r=S.r * 0.5)
    return [shell(block), line(seg(12, 2.8, 12, 11)), line(poly([(9.8, 8.8), (12, 11), (14.2, 8.8)]))]


@icon("inselberg", CAT, "Lone rounded rock mountain rising abruptly from a flat plain",
      tags=["monadnock", "isolated hill", "rock dome", "bornhardt", "landform", "desert", "outcrop"])
def _(S):
    dome = poly([(6, 19.5), (7, 10.5), (9.5, 6), (14.5, 6), (17, 10.5), (18, 19.5)], closed=True, r=S.r * 1.6)
    return [shell(dome), detail(poly([(11, 9.5), (12.6, 12.5), (11.4, 16)])),
            line(seg(2.5, 19.5, 6, 19.5)), line(seg(18, 19.5, 21.5, 19.5))]


@icon("tidal-causeway", CAT, "Small island joined to the shore by a low road running across the water",
      tags=["causeway", "island road", "tidal island", "sea crossing", "low tide", "holy island", "saint michael's mount"])
def _(S):
    shore = "M2.5 15V11.5C3.5 9.5 6 9 8 10.5L9.5 15Z"
    island = "M14.5 15C14.5 10 17 7.5 19.3 7.5C21 7.5 22 10 22 15Z"
    return [shell(shore), shell(island), line(seg(2.5, 15, 22, 15)),
            line("M2.5 19.5q1.5-1.6 3 0t3 0t3 0t3 0t3 0t3 0")]


@icon("cloud-forest", CAT, "Conifer trees below a long horizontal band of cloud wrapped around the slope",
      tags=["montane forest", "mist forest", "fog forest", "tropical mountain", "rainforest", "clouds", "canopy"])
def _(S):
    cloud = "M3 10C3 8.3 4.6 7.3 6.3 8C6.8 5.8 9.6 5.2 10.8 7C12 5.4 15 5.6 15.5 7.6C18 6.8 20 8.3 20 10C20 11 19 11.6 18 11.6H5C3.8 11.6 3 11 3 10Z"
    tree = lambda cx: poly([(cx - 2.6, 19.5), (cx, 13.8), (cx + 2.6, 19.5)], closed=True, r=S.r * 0.4)
    return [shell(cloud), shell(tree(5)), shell(tree(12)), shell(tree(19)),
            line(seg(5, 19.5, 5, 21.5)), line(seg(12, 19.5, 12, 21.5)), line(seg(19, 19.5, 19, 21.5))]


@icon("slot-canyon", CAT, "Very narrow deep canyon with smooth winding walls and a thin gap of sky between them",
      tags=["narrow canyon", "gorge", "desert canyon", "antelope canyon", "ravine", "rock walls", "hiking"])
def _(S):
    left = poly([(2.5, 3), (8.5, 3), (8, 7.5), (10, 11), (9, 15), (10.5, 18.5), (10, 21.5), (2.5, 21.5)], closed=True, r=S.r)
    right = poly([(21.5, 3), (15.5, 3), (15.5, 7.5), (14, 11), (15, 15), (13.8, 18.5), (14.2, 21.5), (21.5, 21.5)], closed=True, r=S.r)
    return [shell(left), shell(right)]


@icon("moorland", CAT, "Low rolling hills with heather tufts and a lone boulder",
      tags=["moor", "heath", "heather", "uplands", "highlands", "rough grazing", "landscape"])
def _(S):
    hills = "M2.5 21V16C4.5 13 8 12.5 11 14.8C13 16.4 16.5 16 21.5 13V21Z"
    return [shell(hills), shell(ellipse(16.5, 8.6, 3.2, 2.2)),
            line("M7.5 10.8V7.4"), line("M5.8 11.2L4.6 8.8"), line("M9.2 11.2L10.4 8.8")]


def _silhouette(S, pts):
    return poly(pts, closed=True, r=S.r * 0.7) if S.name == "rounded" else poly(pts, closed=True)


@icon("africa-continent", CAT, "Silhouette of the African continent",
      tags=["africa", "continent", "sahara", "african", "map", "landmass", "geography"])
def _(S):
    pts = [(7, 4), (12, 3.5), (16, 5), (18.5, 6.2), (20, 9.5), (21.5, 11.5), (19.5, 14.3), (17.5, 18), (15, 21), (12.5, 20.5),
           (11.5, 16), (10.5, 12.8), (6.5, 12.8), (3, 10.5), (3.5, 7)]
    return [shell(_silhouette(S, pts))]


@icon("antarctica-continent", CAT, "Silhouette of Antarctica seen from above the South Pole",
      tags=["antarctica", "south pole", "continent", "ice sheet", "polar", "map", "landmass"])
def _(S):
    radii = [8.6, 8.4, 8.8, 7.6, 6.4, 8.2, 8.9, 8.6, 8.0, 8.6, 8.8, 8.4, 8.0, 8.8, 9.2, 9.6, 9.8, 9.0, 8.4, 8.6]
    pts = [polar(12.3, 12, r, -90 + i * 18) for i, r in enumerate(radii)]
    return [shell(_silhouette(S, pts))]


@icon("asia-continent", CAT, "Silhouette of the Asian continent",
      tags=["asia", "continent", "eurasia", "asian", "map", "landmass", "geography"])
def _(S):
    pts = [(3, 8), (6, 4.5), (12, 3.5), (18, 3.5), (21.5, 6), (21, 9.5), (18.5, 11.5), (19, 14.5), (17, 17.5), (15.5, 14.5),
           (14, 16), (12.5, 20.5), (10.5, 14.5), (7, 14.5), (4, 12.5), (5, 10)]
    return [shell(_silhouette(S, pts))]


@icon("australia-continent", CAT, "Silhouette of the Australian continent",
      tags=["australia", "continent", "oceania", "down under", "map", "landmass", "outback"])
def _(S):
    pts = [(2.5, 12), (3.5, 8.5), (6.5, 7.5), (9, 8.5), (11.5, 6.5), (13.5, 7.5), (14, 9.8), (15.3, 9), (15.8, 5), (18, 5), (18.7, 9),
           (20.8, 11.5), (21.5, 14.5), (19.5, 18), (16, 19.5), (13, 18), (10, 19.5), (6, 18.5), (3, 15.5)]
    return [shell(_silhouette(S, pts))]
