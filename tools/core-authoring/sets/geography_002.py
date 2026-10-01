"""TypeIcon Core: geography (navigation instruments, globes, routes, roads, trail markers)."""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, path_to_d, poly, rect, regular, seg, shell,
    solid,
)
from geometry import D, I, P, U, fmt, path_to_d, polar  # noqa: F811

CAT = "geography"


def L(S, a, b):
    """Pick a value for Line/Filled (a) or Rounded (b)."""
    return b if S.name == "rounded" else a


def rim(deg, r=9.0, cx=12.0, cy=12.0):
    return polar(cx, cy, r, deg)


def pin_d(S, cx, cy, r, h):
    phi = math.acos(r / h)
    lp = (cx - r * math.sin(phi), cy + r * math.cos(phi))
    rp = (cx + r * math.sin(phi), cy + r * math.cos(phi))
    tip = (cx, cy + h)

    def _p(p):
        return f"{fmt(p[0])} {fmt(p[1])}"
    arc_part = f"A{fmt(r)} {fmt(r)} 0 1 1 {_p(rp)}"
    if S.name != "rounded":
        return f"M{_p(tip)}L{_p(lp)}{arc_part}Z"
    t = 1.3
    ln = math.hypot(lp[0] - tip[0], lp[1] - tip[1])
    a = (tip[0] + (lp[0] - tip[0]) * t / ln, tip[1] + (lp[1] - tip[1]) * t / ln)
    b = (tip[0] + (rp[0] - tip[0]) * t / ln, tip[1] + (rp[1] - tip[1]) * t / ln)
    return f"M{_p(a)}L{_p(lp)}{arc_part}L{_p(b)}Q{_p(tip)} {_p(a)}Z"


def plane_pts(cx, cy, s, deg):
    """Small airplane silhouette (points) centred on (cx, cy), nose pointing along deg (0 = up), size s."""
    base = [(0, -1.0), (0.22, -0.55), (0.22, -0.2), (1.0, 0.25), (1.0, 0.5), (0.22, 0.3), (0.2, 0.75), (0.5, 0.95),
            (0.5, 1.1), (0, 1.0), (-0.5, 1.1), (-0.5, 0.95), (-0.2, 0.75), (-0.22, 0.3), (-1.0, 0.5), (-1.0, 0.25),
            (-0.22, -0.2), (-0.22, -0.55)]
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [(cx + s * (x * c - y * sn), cy + s * (x * sn + y * c)) for x, y in base]


def plane(cx, cy, s, deg, knock=False, r=0.0) -> Part:
    d = poly(plane_pts(cx, cy, s, deg), closed=True, r=r)
    return Part("dot", d) if knock else solid(d)


def rot_pts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c) for x, y in pts]


def rot_seg(x1, y1, x2, y2, deg, cx=12.0, cy=12.0):
    (a, b), (c, d) = rot_pts([(x1, y1), (x2, y2)], deg, cx, cy)
    return seg(a, b, c, d)


def coast(S, pts, k=0.6):
    return detail(poly(pts, r=S.r * k))


def union_d(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def clip_disc(d, cx=12.0, cy=12.0, r=8.2):
    return path_to_d(I(P(d), P(circle(cx, cy, r))))


def star4(cx, cy, r, k=0.38):
    pts = []
    for i in range(8):
        a = math.radians(-90 + i * 45)
        rr = r if i % 2 == 0 else r * k
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return poly(pts, closed=True)


def globe(S, lands, extra=()):
    """Globe with solid land masses clipped inside the rim. Line/Rounded: ring + solid land. Filled: land knocked out."""
    ds = [clip_disc(poly(pts, closed=True, r=L(S, 0, 2.2))) for pts in lands]
    return [shell(circle(12, 12, 9))] + [solid(d) for d in ds] + list(extra)


def globe_filled(lands):
    def f():
        body = P(circle(12, 12, 10))
        cut = [I(P(poly(pts, closed=True, r=0.9)), P(circle(12, 12, 8.0))) for pts in lands]
        return D(body, *cut)
    return f


# =========================================================================== continents and globes

@icon("south-america-continent", CAT, "Solid silhouette of South America tapering to a point",
      tags=["south america", "continent", "brazil", "argentina", "map", "atlas", "americas"])
def _(S):
    k = S.r * 0.45
    pts = [(7.5, 3), (11.5, 3.5), (15, 6), (20, 8.5), (19.5, 11.5), (15.5, 14.5), (14, 18.5), (12, 21.5), (10.5, 20),
           (10.5, 15), (8.5, 11), (5.5, 7.5)]
    return [shell(poly(pts, closed=True, r=k))]


AMERICAS = [[(3, 7), (9, 3.5), (16, 4), (19, 8), (15.5, 9.5), (14.5, 11.5), (15, 13.5), (18, 15), (16.5, 18.5),
              (13.5, 21.5), (12, 17), (12.5, 14), (11.5, 12), (8, 11), (4, 10)]]
EURAF = [[(8, 4), (14, 2), (18, 5), (15.5, 7), (11.5, 7), (9, 6.5)],
         [(5, 10), (10, 9), (15, 9.5), (19, 12), (16.5, 14.5), (15, 18), (13.5, 21), (11.5, 18), (11, 14.5), (6.5, 14),
          (4.5, 12)]]
ASIAAUS = [[(4, 6), (10, 3), (18, 4), (21, 8), (18, 11), (16, 11.5), (14, 16), (12.5, 11.5), (9, 11), (5, 9)],
           [(14.5, 16.5), (18, 16), (18, 19), (14.5, 19.5)]]
PACIFIC = [[(3, 7), (6.5, 9), (7, 14), (3, 16)], [(21, 8), (17.5, 10), (17.5, 15), (21, 17)]]


def island(S, cx, cy, r):
    if S.name == "rounded":
        return solid(circle(cx, cy, r))
    return solid(poly([(cx, cy - r * 1.3), (cx + r * 1.3, cy), (cx, cy + r * 1.3), (cx - r * 1.3, cy)], closed=True))


@icon("globe-americas", CAT, "Globe showing North and South America facing the viewer",
      tags=["globe", "americas", "western hemisphere", "earth", "world", "north america", "south america"],
      filled=globe_filled(AMERICAS))
def _(S):
    return globe(S, AMERICAS)


@icon("globe-europe-africa", CAT, "Globe showing Europe and Africa facing the viewer",
      tags=["globe", "europe", "africa", "earth", "world", "eastern hemisphere", "emea"],
      filled=globe_filled(EURAF))
def _(S):
    return globe(S, EURAF)


@icon("globe-asia-australia", CAT, "Globe showing Asia and Australia facing the viewer",
      tags=["globe", "asia", "australia", "oceania", "earth", "world", "eastern hemisphere", "apac"],
      filled=globe_filled(ASIAAUS))
def _(S):
    return globe(S, ASIAAUS)


@icon("globe-pacific", CAT, "Globe mostly covered by ocean with small islands and continent edges at the rims",
      tags=["globe", "pacific", "ocean", "islands", "earth", "world", "polynesia", "sea"],
      filled=lambda: D(globe_filled(PACIFIC)(), P(circle(10.5, 10, 1.5)), P(circle(13.5, 14.5, 1.5)),
                       P(circle(8.5, 17, 1.2))))
def _(S):
    return globe(S, PACIFIC, [island(S, 10.5, 10, 1.4), island(S, 13.5, 14.5, 1.4), island(S, 9, 17, 1.1)])


@icon("celestial-globe", CAT, "Globe on a stand covered with stars and constellation lines instead of land",
      tags=["celestial", "star globe", "astronomy", "constellation", "sky", "stars", "planetarium"])
def _(S):
    return [shell(circle(12, 9.5, 7.5)),
            detail(poly([(8, 11.5), (10.5, 7.5), (15, 9), (15.5, 12.5)])),
            dot(8, 11.5, 1.4), dot(10.5, 7.5, 1.4), dot(15, 9, 1.4), dot(15.5, 12.5, 1.4),
            line("M6 18Q12 21.5 18 18"), line(seg(12, 19.3, 12, 21.5)), line(seg(8.5, 21.5, 15.5, 21.5))]


@icon("around-the-world", CAT, "Globe with a small airplane flying along a dashed orbit around it",
      tags=["around the world", "world tour", "global travel", "flight", "international", "worldwide", "orbit"])
def _(S):
    return [shell(circle(12, 12, 5)), detail(ellipse(12, 12, 2.2, 5)), detail(seg(7, 12, 17, 12)),
            line(arc(12, 12, 9.5, 95, 130)), line(arc(12, 12, 9.5, 150, 185)), line(arc(12, 12, 9.5, 205, 240)),
            line(arc(12, 12, 9.5, 260, 295)),
            plane(19, 6.2, 3.6, 130, r=S.r * 0.3)]


@icon("wall-map", CAT, "Pull-down classroom map hanging from a roller bar with a cord at the bottom",
      tags=["wall map", "classroom map", "school map", "pull down map", "geography class", "atlas", "world map"])
def _(S):
    return [line(seg(3, 3.5, 21, 3.5)),
            shell(rect(5, 6, 14, 11, S.R * 0.5)),
            detail(poly([(8, 13), (8, 10.5), (11, 9.5), (12.5, 12), (10.5, 14.5)], closed=True, r=S.r * 0.3)),
            dot(15.5, 12.5, 1.2),
            line(seg(12, 18, 12, 19.5)), dot(12, 20.5, 1.25)]


@icon("tactile-map", CAT, "Map outline covered with raised dots and a row of braille-style dots along the bottom",
      tags=["tactile map", "braille", "accessible map", "blind", "raised dots", "touch map", "visually impaired"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, S.R)), detail("M3 12Q7.5 8 12 12T21 12")]
    for x in (8, 12, 16):
        parts.append(dot(x, 7, 1.1))
    for x, y in [(7.5, 16), (12, 15.5), (16.5, 16)]:
        parts.append(dot(x, y, 1.1))
    return parts


@icon("baseplate-compass", CAT, "Rectangular baseplate compass with a direction-of-travel arrow and a round housing",
      tags=["compass", "baseplate", "orienteering", "hiking", "navigation", "map reading", "outdoors"])
def _(S):
    needle = "M12 10.5L13.3 15L12 19.5L10.7 15Z"
    return [shell(union_d(rect(7.5, 2.5, 9, 19, S.R * 0.5), circle(12, 15, 6))),
            detail(circle(12, 15, 4)),
            Part("dot", needle),
            detail(poly([(10.5, 7), (12, 5.2), (13.5, 7)], r=S.r * 0.3)), detail(seg(12, 5.6, 12, 8.6))]


@icon("lensatic-compass", CAT, "Folding compass with an upright hinged lid holding a sighting wire over a round dial",
      tags=["lensatic", "military compass", "sighting", "folding compass", "navigation", "bearing", "field compass"])
def _(S):
    return [shell(poly([(7, 2.5), (17, 2.5), (19.5, 10), (4.5, 10)], closed=True, r=S.r * 0.4)),
            detail(seg(12, 4, 12, 9)),
            shell(rect(4, 10, 16, 11.5, S.R * 0.5)),
            detail(circle(12, 16, 3.3)), Part("dot", "M12 13.5L13 16L12 18.5L11 16Z")]


@icon("binnacle", CAT, "Ship's compass on a waist-high pedestal with a domed glass top and two iron balls",
      tags=["binnacle", "ship compass", "nautical", "helm", "navigation", "boat", "compass stand"])
def _(S):
    return [shell("M6.5 10A5.5 5.5 0 0 1 17.5 10Z"), dot(12, 7.5, 1.1),
            shell(poly([(9, 10), (15, 10), (16, 19.5), (8, 19.5)], closed=True, r=S.r * 0.3)),
            line(seg(6, 21.5, 18, 21.5)),
            shell(circle(3.5, 13, 1.5)), shell(circle(20.5, 13, 1.5)),
            line(seg(5, 13, 8.7, 13)), line(seg(15.3, 13, 19, 13))]


@icon("wrist-compass", CAT, "Small round compass dial mounted on a watch strap",
      tags=["wrist compass", "watch compass", "hiking", "strap compass", "navigation", "outdoor", "wearable"])
def _(S):
    body = union_d(rect(9, 2.5, 6, 10, S.R * 0.5), rect(9, 11.5, 6, 10, S.R * 0.5), circle(12, 12, 6.3))
    return [shell(body), Part("dot", "M12 8.3L13.4 12L12 15.7L10.6 12Z")]


# =========================================================================== navigation instruments

@icon("compass-rose", CAT, "Eight-pointed star with long cardinal points and shorter intercardinal points",
      tags=["compass rose", "north", "cardinal directions", "map", "navigation", "wind rose", "orientation"])
def _(S):
    pts = []
    for i in range(8):
        a = -90 + 45 * i
        pts.append(polar(12, 12, 9.4 if i % 2 == 0 else 6.4, a))
        pts.append(polar(12, 12, L(S, 3.2, 3.9), a + 22.5))
    return [shell(poly(pts, closed=True, r=S.r * 0.2), stroke_miterlimit="2")]


@icon("wind-rose", CAT, "Circular diagram with spokes of different lengths radiating from the centre showing wind directions",
      tags=["wind rose", "wind direction", "meteorology", "frequency diagram", "climate", "sailing", "radial chart"])
def _(S):
    parts = [shell(circle(12, 12, 2.5))]
    for deg, ln in [(-90, 9.5), (-45, 6.5), (0, 8.5), (45, 5.5), (90, 9), (135, 6), (180, 7.5), (225, 5.5)]:
        a = polar(12, 12, 3.5, deg)
        b = polar(12, 12, ln, deg)
        parts.append(line(seg(a[0], a[1], b[0], b[1])))
    return parts


@icon("quadrant-instrument", CAT, "Quarter-circle plate with a degree scale on its arc and a plumb bob hanging from the corner",
      tags=["quadrant", "astronomy", "old navigation", "plumb bob", "angle measuring", "surveying", "sextant"])
def _(S):
    parts = [shell("M12 3L3.5 11.5A12 12 0 0 0 20.5 11.5Z")]
    for deg in (-36, -18, 18, 36):
        a = polar(12, 3, 7.8, 90 + deg)
        b = polar(12, 3, 9.6, 90 + deg)
        parts.append(detail(seg(a[0], a[1], b[0], b[1])))
    parts += [detail(seg(12, 4.5, 12, 15)), line(seg(12, 15, 12, 18.2)), shell(circle(12, 20, 1.3))]
    return parts


@icon("marine-chronometer", CAT, "Round clock dial set in a square wooden box with its lid open",
      tags=["chronometer", "marine clock", "ship clock", "longitude", "navigation", "timekeeper", "nautical"])
def _(S):
    return [shell(rect(3, 9, 18, 12, S.R * 0.5)),
            shell(poly([(3, 9), (6, 3), (21, 3), (18, 9)], closed=True, r=S.r * 0.3)),
            detail(circle(12, 15, 3.6)), detail(poly([(12, 12.9), (12, 15), (13.6, 15)]))]


@icon("radar-screen", CAT, "Round scope with a range ring, a rotating sweep line and a few echo dots",
      tags=["radar", "scope", "sweep", "echo", "ping", "air traffic", "detection"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(circle(12, 12, 4.2)),
            detail(seg(12, 12, 17.3, 6.7)), dot(7.5, 9, 1.1), dot(15.5, 15.5, 1.1)]


@icon("sonar-ping", CAT, "Ship hull on the water surface sending curved sound arcs down to the seabed",
      tags=["sonar", "echo sounder", "depth", "ping", "underwater", "sounding", "seabed"])
def _(S):
    return [shell(poly([(6, 3.5), (18, 3.5), (15.5, 7.5), (8.5, 7.5)], closed=True, r=S.r * 0.4)),
            line(arc(12, 8, 3.8, 50, 130)), line(arc(12, 8, 6.8, 50, 130)), line(arc(12, 8, 9.8, 50, 130)),
            line("M3 21.5Q7.5 19.5 12 21.5T21 21.5")]


@icon("chart-dividers", CAT, "Two-legged navigation dividers with sharp points, opened in an upside-down V",
      tags=["dividers", "chart dividers", "compass", "measuring", "navigation", "distance", "drafting"])
def _(S):
    return [shell(circle(12, 4.5, 2.2)), line(seg(11.1, 6.6, 6, 21.5)), line(seg(12.9, 6.6, 18, 21.5)),
            line(seg(8.4, 14.5, 15.6, 14.5))]


@icon("parallel-rulers", CAT, "Two straight rulers joined by two pivoting arms",
      tags=["parallel rule", "rulers", "chart work", "course plotting", "navigation", "drafting", "bearings"])
def _(S):
    return [shell(rect(3, 3.5, 18, 5, S.R * 0.5)), shell(rect(3, 15.5, 18, 5, S.R * 0.5)),
            line(seg(7.5, 8.5, 11.5, 15.5)), line(seg(13.5, 8.5, 17.5, 15.5))]


@icon("heading-indicator", CAT, "Round aircraft gauge with a compass card and a small airplane silhouette fixed in the centre",
      tags=["heading indicator", "directional gyro", "aircraft instrument", "cockpit", "compass card", "avionics", "flight"])
def _(S):
    parts = [shell(circle(12, 12, 9))]
    for deg in (-90, 0, 90, 180):
        c = polar(12, 12, 6, deg)
        parts.append(dot(c[0], c[1], 0.9) if S.name == "rounded" else
                     Part("dot", poly([(c[0] - 0.9, c[1] - 0.9), (c[0] + 0.9, c[1] - 0.9), (c[0] + 0.9, c[1] + 0.9), (c[0] - 0.9, c[1] + 0.9)], closed=True)))
    parts.append(Part("dot", poly(plane_pts(12, 12, 3.4, 0), closed=True, r=S.r * 0.25)))
    return parts


def _halfplane(side, tilt):
    # side: +1 lower half, -1 upper half, rotated by tilt degrees about the centre
    y0, y1 = (12, 30) if side > 0 else (-6, 12)
    return poly(rot_pts([(-6, y0), (30, y0), (30, y1), (-6, y1)], tilt), closed=True)


def _wings(rx=0.0):
    return [rect(5.5, 11, 4, 2, rx), rect(14.5, 11, 4, 2, rx), circle(12, 12, 1.4)]


def _ah_filled():
    disc = P(circle(12, 12, 8.0))
    tilt = -14
    upper = I(P(_halfplane(-1, tilt)), disc)
    lower = I(P(_halfplane(1, tilt)), disc)
    W = U(*[P(d) for d in _wings()])
    return D(P(circle(12, 12, 10)), D(upper, W), I(lower, W))


@icon("artificial-horizon", CAT, "Round aircraft gauge split into sky and ground halves by a tilted horizon line with a fixed wing symbol",
      tags=["artificial horizon", "attitude indicator", "aircraft instrument", "cockpit", "pitch and roll", "avionics", "flight"],
      filled=_ah_filled)
def _(S):
    disc = P(circle(12, 12, 8.2))
    lower = I(P(_halfplane(1, -14)), disc)
    W = U(*[P(d) for d in _wings(L(S, 0, 1))])
    sym = U(D(lower, W), D(W, lower))
    return [shell(circle(12, 12, 9)), solid(path_to_d(sym))]


@icon("chart-plotter", CAT, "Marine display screen with buttons below, showing a coastline and a boat symbol",
      tags=["chart plotter", "marine gps", "boat navigation", "sea chart", "helm display", "sailing", "electronics"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(rect(6, 6, 12, 8, S.R * 0.25)),
            Part("dot", poly([(14.5, 8), (16, 12), (14.5, 11), (13, 12)], closed=True)),
            dot(8, 18, 1), dot(12, 18, 1), dot(16, 18, 1)]


@icon("locator-beacon", CAT, "Small handheld emergency beacon with a stubby antenna and a strobe light on top",
      tags=["beacon", "locator beacon", "emergency", "plb", "epirb", "rescue", "distress signal"])
def _(S):
    return [shell(rect(6, 10, 12, 11.5, S.R)), detail(circle(12, 16, 2)),
            line(seg(15.5, 10, 15.5, 4)),
            shell("M6.5 10A3.2 3.2 0 0 1 12.9 10Z"),
            line(seg(9.7, 4.2, 9.7, 2.8)), line(seg(5.8, 5.6, 4.6, 4.4)), line(seg(13.6, 5.6, 14, 5))]


def qpt(p0, c, p1, t):
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * c[0] + t * t * p1[0], u * u * p0[1] + 2 * u * t * c[1] + t * t * p1[1])


def qcross(a, b, n=240):
    """Approximate crossing point of two quadratic curves a and b, each (p0, ctrl, p1)."""
    best, bp = 1e9, None
    pa = [qpt(*a, i / n) for i in range(n + 1)]
    pb = [qpt(*b, i / n) for i in range(n + 1)]
    for x in pa:
        for y in pb:
            d = (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2
            if d < best:
                best, bp = d, ((x[0] + y[0]) / 2, (x[1] + y[1]) / 2)
    return bp


def qd(c):
    return f"M{fmt(c[0][0])} {fmt(c[0][1])}Q{fmt(c[1][0])} {fmt(c[1][1])} {fmt(c[2][0])} {fmt(c[2][1])}"


@icon("stick-chart", CAT, "Lattice of crossed curved sticks tied together with small shells at the joints",
      tags=["stick chart", "marshall islands", "wave navigation", "traditional navigation", "ocean swells", "polynesian", "wayfinding"])
def _(S):
    h1 = ((3, 8), (12, 4.5), (21, 8))
    h2 = ((3, 16), (12, 19.5), (21, 16))
    v1 = ((8, 3), (5.5, 12), (8, 21))
    v2 = ((16, 3), (18.5, 12), (16, 21))
    parts = [line(qd(c)) for c in (h1, h2, v1, v2)]
    for a in (h1, h2):
        for b in (v1, v2):
            x, y = qcross(a, b)
            parts.append(shell(circle(x, y, 1.6)))
    return parts


@icon("luopan-compass", CAT, "Round dial with concentric marked rings and a small central needle, set on a square base plate",
      tags=["luopan", "feng shui compass", "chinese compass", "geomancy", "ring dial", "direction", "traditional"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(circle(12, 12, 7.3)), detail(circle(12, 12, 4)),
            Part("dot", "M12 9.8L13 12L12 14.2L11 12Z")]


@icon("qibla-compass", CAT, "Round compass dial with a needle and a small mosque dome marker near the rim",
      tags=["qibla", "prayer direction", "muslim", "islamic", "mecca", "salah", "compass"])
def _(S):
    k = S.r * 0.3
    return [shell(circle(12, 12, 9)),
            Part("dot", "M9.6 9A2.4 2.4 0 0 1 14.4 9Z"), Part("dot", rect(11.5, 5.4, 1, 1.6)),
            Part("dot", poly([(12, 11.3), (13.6, 15.3), (12, 19), (10.4, 15.3)], closed=True, r=k))] + [
        (dot(c[0], c[1], 0.9) if S.name == "rounded" else
         Part("dot", rect(c[0] - 0.9, c[1] - 0.9, 1.8, 1.8)))
        for c in (polar(12, 12, 6.6, 0), polar(12, 12, 6.6, 90), polar(12, 12, 6.6, 180))]


@icon("ground-control-target", CAT, "Square ground marker split into a black and white checkerboard of four squares, seen from above",
      tags=["ground control point", "gcp", "survey marker", "drone mapping", "photogrammetry", "aerial survey", "target"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R * 0.5)), Part("dot", rect(4, 4, 8, 8)), Part("dot", rect(12, 12, 8, 8))]


@icon("lidar-scan", CAT, "Small aircraft emitting a fan of laser lines down onto dotted terrain",
      tags=["lidar", "laser scan", "terrain mapping", "aerial survey", "drone", "elevation", "point cloud"])
def _(S):
    parts = [plane(12, 5, 3.6, 0, r=S.r * 0.3)]
    for x in (4.5, 12, 19.5):
        parts.append(line(seg(12, 9, x, 17.5)))
    for x in (4, 8, 12, 16, 20):
        parts.append(dot(x, 21, 0.9))
    return parts


@icon("survey-gps-antenna", CAT, "Round dome antenna mounted on top of a tripod for precise survey positioning",
      tags=["gnss", "gps antenna", "surveying", "rtk", "tripod", "base station", "geodesy"])
def _(S):
    return [shell("M6.5 8.5A5.5 5.5 0 0 1 17.5 8.5Z"), line(seg(12, 8.5, 12, 13)), line(seg(12, 13, 6, 21.5)),
            line(seg(12, 13, 18, 21.5)), line(seg(12, 13, 12, 21.5))]


@icon("buoy", CAT, "Navigation buoy floating on water with a tapered body, a lattice top and a light",
      tags=["buoy", "sea marker", "navigation aid", "lighted buoy", "harbour", "float", "channel"])
def _(S):
    return [shell(poly([(6, 13), (18, 13), (15.5, 18.5), (8.5, 18.5)], closed=True, r=S.r * 0.3)),
            line(poly([(8.8, 13), (10.5, 6.5), (13.5, 6.5), (15.2, 13)])), line(seg(9.6, 9.8, 14.4, 9.8)),
            shell(circle(12, 4, 1.4)),
            line("M2.5 21.5Q5 20 7.5 21.5T12.5 21.5T17.5 21.5T21.5 21.5")]


@icon("channel-markers", CAT, "Two posts in water, one topped with a flat can shape and one with a cone",
      tags=["channel markers", "port and starboard", "buoys", "fairway", "can and nun", "harbor entrance", "waterway"])
def _(S):
    return [shell(rect(3.5, 5, 7, 6, S.R * 0.3)), line(seg(7, 11, 7, 19)),
            shell(poly([(14, 11), (17.5, 4.5), (21, 11)], closed=True, r=S.r * 0.3)), line(seg(17.5, 11, 17.5, 19)),
            line("M2.5 21.5Q5 20 7.5 21.5T12.5 21.5T17.5 21.5T21.5 21.5")]


@icon("lightship", CAT, "Short ship hull with a tall central lattice mast carrying a big lamp",
      tags=["lightship", "light vessel", "lighthouse ship", "navigation light", "anchored ship", "maritime", "beacon"])
def _(S):
    return [shell(poly([(3, 15.5), (21, 15.5), (18, 20.5), (6, 20.5)], closed=True, r=S.r * 0.3)),
            line(poly([(9, 15.5), (12, 7.5), (15, 15.5)])), line(seg(10.4, 11.6, 13.6, 11.6)),
            shell(circle(12, 4.8, 2))]


@icon("ships-wheel", CAT, "Wooden ship's steering wheel with eight spokes ending in handles around the rim",
      tags=["ship's wheel", "helm", "steering", "nautical", "captain", "sailing", "boat"])
def _(S):
    parts = [line(circle(12, 12, 5.4))]
    for i in range(8):
        a = polar(12, 12, 1, -90 + 45 * i)
        b = polar(12, 12, 7.8, -90 + 45 * i)
        c = polar(12, 12, 9, -90 + 45 * i)
        parts.append(line(seg(a[0], a[1], b[0], b[1])))
        parts.append(dot(c[0], c[1], 1.3))
    return parts


@icon("windsock", CAT, "Striped cone windsock on a pole, blowing out horizontally",
      tags=["windsock", "wind direction", "airfield", "airport", "weather vane", "wind indicator", "aviation"])
def _(S):
    return [line(seg(4, 3, 4, 21.5)),
            shell(poly([(5.5, 5), (21, 7.5), (21, 12.5), (5.5, 15)], closed=True, r=S.r * 0.25)),
            detail(seg(10.4, 5.7, 10.4, 14.3)), detail(seg(15.6, 6.6, 15.6, 13.4))]


@icon("gyroscope", CAT, "Spinning disc inside nested gimbal rings on a small stand",
      tags=["gyroscope", "gyro", "gimbal", "orientation", "inertial navigation", "spinning", "physics"])
def _(S):
    return [shell(circle(12, 10.5, 8)), detail(ellipse(12, 10.5, 4, 8)),
            shell(ellipse(12, 10.5, 5.2, 1.8)),
            line(seg(12, 18.5, 12, 21.5)), line(seg(7.5, 21.5, 16.5, 21.5))]


@icon("wind-head", CAT, "Round face with puffed cheeks blowing a stream of air lines, as drawn in old map corners",
      tags=["wind", "blowing", "north wind", "old map", "weather", "breeze", "gust"])
def _(S):
    return [shell(circle(8, 12, 6.5)), dot(6, 10.2, 1), dot(10, 10.2, 1), detail(circle(8, 14.3, 1.2)),
            line("M16.5 8.5H19.5a1.8 1.8 0 1 0-1.8-1.8"), line(seg(16.5, 12, 21.5, 12)),
            line("M16.5 15.5H19.5a1.8 1.8 0 1 1-1.8 1.8")]


@icon("flight-route", CAT, "Dashed curved arc between two dots with a small airplane on the arc",
      tags=["flight path", "flight route", "air route", "travel", "airline", "trip", "itinerary"])
def _(S):
    cy, r = 14.67, 8.67
    return [dot(4, 18, 1.8), dot(20, 18, 1.8),
            line(arc(12, cy, r, 170, 195)), line(arc(12, cy, r, 212, 238)), line(arc(12, cy, r, 308, 334)),
            line(arc(12, cy, r, 350, 375)),
            plane(12, 6.3, 4, 90, r=S.r * 0.3)]


@icon("holding-pattern", CAT, "Racetrack-shaped oval flight path with an arrowhead and a small plane on it",
      tags=["holding pattern", "racetrack", "air traffic", "flight path", "loop", "aviation", "circling"])
def _(S):
    return [line("M16 7A5 5 0 0 1 16 17H8A5 5 0 0 1 8 7"), plane(12, 7, 4.4, 90, r=S.r * 0.3),
            solid(poly([(9, 17), (13, 14.6), (13, 19.4)], closed=True, r=S.r * 0.3))]


# =========================================================================== roads and junctions (top views)

def dash_v(x, y0, y1):
    return detail(seg(x, y0, x, y1))


def dash_h(y, x0, x1):
    return detail(seg(x0, y, x1, y))


@icon("crossroads", CAT, "Top view of two roads crossing at right angles with dashed centre lines",
      tags=["crossroads", "intersection", "four way", "junction", "road", "crossing", "traffic"])
def _(S):
    pts = [(8, 2.5), (16, 2.5), (16, 8), (21.5, 8), (21.5, 16), (16, 16), (16, 21.5), (8, 21.5), (8, 16), (2.5, 16),
           (2.5, 8), (8, 8)]
    return [shell(poly(pts, closed=True, r=S.r * 0.5)),
            dash_v(12, 4.5, 6.5), dash_v(12, 17.5, 19.5), dash_h(12, 4.5, 6.5), dash_h(12, 17.5, 19.5)]


@icon("t-junction", CAT, "Top view of a road ending at a perpendicular through road, forming a T",
      tags=["t junction", "t intersection", "three way", "road end", "junction", "give way", "road"])
def _(S):
    pts = [(2.5, 3.5), (21.5, 3.5), (21.5, 11.5), (16, 11.5), (16, 21.5), (8, 21.5), (8, 11.5), (2.5, 11.5)]
    return [shell(poly(pts, closed=True, r=S.r * 0.5)),
            dash_h(7.5, 4.5, 7), dash_h(7.5, 17, 19.5), dash_v(12, 14.5, 17.5)]


@icon("roundabout", CAT, "Top view of a circular island with four roads meeting the ring around it",
      tags=["roundabout", "traffic circle", "rotary", "circular junction", "road", "intersection", "gyratory"])
def _(S):
    body = union_d(circle(12, 12, 7), rect(8.5, 2.5, 7, 19, S.R * 0.3), rect(2.5, 8.5, 19, 7, S.R * 0.3))
    return [shell(body), detail(circle(12, 12, 2.4))]


@icon("cul-de-sac", CAT, "Top view of a dead-end street ending in a round turning bulb",
      tags=["cul de sac", "dead end", "no through road", "turning circle", "street", "road", "residential"])
def _(S):
    body = union_d(circle(12, 7.5, 5.5), rect(9, 10, 6, 8, S.R * 0.3), rect(2.5, 16, 19, 5.5, S.R * 0.3))
    return [shell(body), dash_v(12, 13, 15.5), dash_h(18.75, 4.5, 7), dash_h(18.75, 17, 19.5)]


@icon("cloverleaf-interchange", CAT, "Top view of two highways crossing with four looping ramps forming a clover shape",
      tags=["cloverleaf", "interchange", "highway", "motorway junction", "ramps", "freeway", "flyover"])
def _(S):
    parts = [line(seg(12, 2, 12, 22)), line(seg(2, 12, 22, 12))]
    for dx, dy in ((-5, -5), (5, -5), (-5, 5), (5, 5)):
        parts.append(line(circle(12 + dx, 12 + dy, 3)))
    return parts


@icon("ring-road", CAT, "Circular road looping around a small cluster of buildings with roads radiating out",
      tags=["ring road", "beltway", "bypass", "orbital", "city loop", "ring", "outer road"])
def _(S):
    parts = [line(circle(12, 12, 6))]
    for deg in (-90, 0, 90, 180):
        a, b = polar(12, 12, 6.5, deg), polar(12, 12, 10, deg)
        parts.append(line(seg(a[0], a[1], b[0], b[1])))
    parts.append(solid(rect(8.4, 8.2, 3, 7)))
    parts.append(solid(rect(12.6, 10.6, 3, 4.6)))
    return parts


@icon("lane-merge", CAT, "Top view of two lanes narrowing into one with converging lane lines",
      tags=["lane merge", "merge", "narrowing road", "lane reduction", "zipper merge", "road", "traffic"])
def _(S):
    pts = [(4, 2.5), (20, 2.5), (20, 8), (15.5, 15), (15.5, 21.5), (8.5, 21.5), (8.5, 15), (4, 8)]
    return [shell(poly(pts, closed=True, r=S.r * 0.5)), dash_v(12, 4.5, 8), dash_v(12, 12, 13)]


def _arrow_up(cx, top, bot, w=1.7, h=3):
    return [(cx, top), (cx + w, top + h), (cx + w * 0.35, top + h), (cx + w * 0.35, bot), (cx - w * 0.35, bot),
            (cx - w * 0.35, top + h), (cx - w, top + h)]


@icon("lane-guidance", CAT, "Three road lanes with arrows painted in them and one lane highlighted",
      tags=["lane guidance", "lane assist", "navigation", "which lane", "road arrows", "driving", "gps lanes"])
def _(S):
    return [shell(rect(3, 2.5, 18, 19, S.R * 0.5)),
            solid(path_to_d(D(P(rect(9, 3.5, 6, 17)), P(poly(_arrow_up(12, 7, 17), closed=True))))),
            Part("dot", poly(_arrow_up(6, 9, 17, 1.5, 2.6), closed=True)),
            Part("dot", poly(_arrow_up(18, 9, 17, 1.5, 2.6), closed=True))]


@icon("divided-highway", CAT, "Top view of two parallel roadways separated by a grassy median strip",
      tags=["divided highway", "dual carriageway", "median", "motorway", "freeway", "road", "central reservation"])
def _(S):
    return [shell(rect(2.5, 2.5, 7, 19, S.R * 0.5)), shell(rect(14.5, 2.5, 7, 19, S.R * 0.5)),
            dash_v(6, 5, 8), dash_v(6, 13, 16), dash_v(18, 5, 8), dash_v(18, 13, 16),
            dot(12, 6, 0.9), dot(12, 12, 0.9), dot(12, 18, 0.9)]


@icon("overpass", CAT, "Top view of one road passing over another on a short bridge deck with side rails",
      tags=["overpass", "flyover", "bridge over road", "grade separation", "road", "crossing", "viaduct"])
def _(S):
    return [line(seg(2.5, 8.5, 9, 8.5)), line(seg(15, 8.5, 21.5, 8.5)), line(seg(2.5, 15.5, 9, 15.5)),
            line(seg(15, 15.5, 21.5, 15.5)),
            shell(rect(9, 2.5, 6, 19, S.R * 0.3)), dash_v(12, 5, 8), dash_v(12, 16, 19)]


@icon("bike-lane", CAT, "Road lane with a bicycle symbol painted on it beside a solid edge line",
      tags=["bike lane", "cycle lane", "cycleway", "bicycle path", "cycling", "road marking", "bike path"])
def _(S):
    return [line(seg(2.5, 3.5, 21.5, 3.5)), line(seg(2.5, 20.5, 21.5, 20.5)),
            line(circle(7, 14, 3)), line(circle(17, 14, 3)),
            line(poly([(7, 14), (10, 8), (14, 14)])), line(seg(8.4, 8, 11.4, 8)),
            line(poly([(14, 14), (15.4, 8)])), line(seg(14.6, 8, 17.2, 8))]


@icon("road-tunnel", CAT, "Road entering an arched tunnel opening cut into a hillside",
      tags=["tunnel", "road tunnel", "mountain pass", "underpass", "highway tunnel", "hill", "portal"])
def _(S):
    hill = ("M2.5 21.5V13A9.5 9.5 0 0 1 21.5 13V21.5Z" if S.name == "rounded" else
            "M2.5 21.5V15L7 6.5H17L21.5 15V21.5Z")
    return [shell(hill), detail("M8 21.5V16A4 4 0 0 1 16 16V21.5")]


@icon("highway-gantry-sign", CAT, "Wide rectangular sign on a gantry spanning the lanes, with down arrows over each lane",
      tags=["gantry", "overhead sign", "highway sign", "motorway sign", "lane signs", "road sign", "variable message"])
def _(S):
    parts = [shell(rect(2.5, 3, 19, 8.5, S.R * 0.3)), line(seg(4.5, 11.5, 4.5, 21.5)), line(seg(19.5, 11.5, 19.5, 21.5))]
    for x in (7.5, 12, 16.5):
        parts.append(Part("dot", poly([(x - 1.9, 5.4), (x + 1.9, 5.4), (x, 9.2)], closed=True)))
    return parts


@icon("level-crossing", CAT, "Railway track crossing a road with a crossbuck X sign on a post beside it",
      tags=["level crossing", "railroad crossing", "grade crossing", "railway", "train crossing", "crossbuck", "rail safety"])
def _(S):
    parts = [line(seg(3.5, 3.5, 12.5, 10.5)), line(seg(12.5, 3.5, 3.5, 10.5)), line(seg(8, 7, 8, 15.5)),
             line(seg(2.5, 15.5, 21.5, 15.5)), line(seg(2.5, 20.5, 21.5, 20.5)),
             line(seg(15, 2.5, 15, 21.5)), line(seg(20, 2.5, 20, 21.5))]
    for y in (4.5, 8.5, 12.5):
        parts.append(line(seg(15, y, 20, y)))
    return parts


# =========================================================================== routes and trail markers

def footprint(cx, cy, deg):
    d = union_d(ellipse(cx, cy, 1.7, 2.5), ellipse(cx, cy + 4.1, 1.25, 1.15))
    from geometry import rotation, transform_path
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


@icon("alternative-route", CAT, "Two separate paths leaving one dot and rejoining at a map pin",
      tags=["alternative route", "alternate route", "route options", "detour", "directions", "two routes", "navigation"])
def _(S):
    return [dot(5, 19.5, 1.9),
            line("M5 16.2V10a4 4 0 0 1 4-4H13"), line("M8.2 19.5H14a3 3 0 0 0 3-3V15"),
            shell(pin_d(S, 17, 6.6, 3.3, 6)), dot(17, 6.6, 1.1)]


@icon("round-trip-route", CAT, "Closed loop route that starts and ends at the same map pin",
      tags=["round trip", "loop route", "circular route", "return trip", "there and back", "directions", "looped trail"])
def _(S):
    return [line(circle(12.5, 14.8, 6.5)), shell(pin_d(S, 12.5, 4.8, 3, 4.6)), dot(12.5, 4.8, 1),
            solid(poly([(16.6, 14.4), (21, 14.4), (18.8, 18)], closed=True, r=S.r * 0.3))]


@icon("sea-route", CAT, "Dashed wavy line across water with a small ship sailing along it",
      tags=["sea route", "shipping lane", "ocean route", "ferry route", "maritime", "voyage", "crossing"])
def _(S):
    parts = [shell(poly([(5.5, 10.5), (18.5, 10.5), (15.5, 15), (8.5, 15)], closed=True, r=S.r * 0.3)),
             line(poly([(10, 10.5), (10, 6.5), (14, 6.5), (14, 10.5)]))]
    parts.append(line("M3 20Q4.6 18.3 6.2 20T9.4 20"))
    parts.append(line("M14.6 20Q16.2 18.3 17.8 20T21 20"))
    return parts


@icon("walking-route", CAT, "Line of alternating footprints leading to a map pin",
      tags=["walking route", "footsteps", "pedestrian route", "on foot", "walk directions", "hike", "footprints"])
def _(S):
    return [solid(footprint(5, 15, 25)), solid(footprint(11, 11, 45)),
            shell(pin_d(S, 17, 5.8, 3.4, 5.8)), dot(17, 5.8, 1.1)]


@icon("bus-route", CAT, "Bus on a route line with round stop dots along it",
      tags=["bus route", "bus line", "public transit", "bus stops", "transit map", "timetable", "commute"])
def _(S):
    return [shell(rect(5, 2.5, 14, 10.5, S.R * 0.5)), detail(seg(5, 7, 19, 7)),
            dot(8.5, 10.2, 1), dot(15.5, 10.2, 1),
            solid(rect(6.5, 13.6, 3, 2.4)), solid(rect(14.5, 13.6, 3, 2.4)),
            line(seg(4.5, 20, 19.5, 20)), shell(circle(4.5, 20, 1.5)), shell(circle(12, 20, 1.5)), shell(circle(19.5, 20, 1.5))]


@icon("ar-navigation", CAT, "Phone held up with a large arrow floating over the street scene on its screen",
      tags=["ar navigation", "augmented reality", "live view", "walking directions", "phone", "camera navigation", "wayfinding"])
def _(S):
    return [shell(rect(6, 2.5, 12, 19, S.R)),
            detail(seg(8.6, 20, 10.3, 14.5)), detail(seg(15.4, 20, 13.7, 14.5)),
            Part("dot", poly([(12, 5), (15.6, 9.2), (13.2, 9.2), (13.2, 12), (10.8, 12), (10.8, 9.2), (8.4, 9.2)],
                             closed=True, r=S.r * 0.2))]


@icon("orienteering-flag", CAT, "Hanging square prism marker divided diagonally into two halves, on a short stake",
      tags=["orienteering", "control flag", "checkpoint", "trail marker", "race marker", "outdoor sport", "kite flag"])
def _(S):
    return [shell(rect(4.5, 3.5, 15, 13, S.R * 0.3)),
            Part("dot", poly([(5.2, 4.2), (5.2, 15.8), (18.8, 15.8)], closed=True)),
            line(seg(12, 16.5, 12, 21.5))]


@icon("map-and-compass", CAT, "Folded paper map with a baseplate compass resting on top",
      tags=["map and compass", "navigation", "orienteering", "hiking", "trekking", "outdoors", "land navigation"])
def _(S):
    mp = D(P("M2.5 6L8.5 4L15.5 6.5L21.5 4.5V18.5L15.5 20.5L8.5 18L2.5 20Z"), P(circle(15.5, 14.5, 5.6)))
    return [shell(path_to_d(mp)), detail(seg(8.5, 5, 8.5, 17)),
            shell(circle(15.5, 14.5, 3.6)), Part("dot", "M15.5 12.4L16.3 14.5L15.5 16.6L14.7 14.5Z")]


@icon("geocache", CAT, "Small ammo-style box with a latched lid and a map pin above it",
      tags=["geocache", "geocaching", "treasure hunt", "hidden box", "gps game", "outdoor game", "cache"])
def _(S):
    return [shell(pin_d(S, 12, 5.2, 3, 5.2)), dot(12, 5.2, 1),
            shell(rect(4, 13.5, 16, 8, S.R * 0.5)), detail(seg(4, 16.5, 20, 16.5)),
            Part("dot", rect(10.8, 15.6, 2.4, 2.4))]


@icon("waymarker-post", CAT, "Short wooden post with a small arrow disc near its top",
      tags=["waymarker", "trail marker", "hiking post", "footpath sign", "direction post", "bridleway", "trail sign"])
def _(S):
    return [shell(union_d(rect(9.5, 7, 5, 14.5, S.R * 0.3), circle(12, 7, 4.6))),
            detail(poly([(10.3, 8.2), (12, 5.6), (13.7, 8.2)], r=S.r * 0.3)), line(seg(2.5, 21.5, 21.5, 21.5))]


@icon("summit-cross", CAT, "Tall cross standing on a pointed mountain peak",
      tags=["summit cross", "summit", "mountain top", "peak", "gipfelkreuz", "hiking goal", "alpine"])
def _(S):
    return [shell(poly([(2.5, 21.5), (12, 9.5), (21.5, 21.5)], closed=True, r=S.r * 0.3)),
            line(seg(12, 2, 12, 9.5)), line(seg(8.8, 4.6, 15.2, 4.6))]


@icon("mountain-hut", CAT, "Small alpine A-frame hut with a steep roof, a door and a window",
      tags=["mountain hut", "alpine hut", "refuge", "cabin", "hiking shelter", "bothy", "mountain shelter"])
def _(S):
    return [shell(poly([(3.5, 21.5), (12, 3.5), (20.5, 21.5)], closed=True, r=S.r * 0.3)),
            detail("M9.8 21.5V16.5H14.2V21.5"), dot(12, 11.2, 1.1)]


@icon("via-ferrata", CAT, "Steep rock face with a steel cable and metal rungs climbing up it",
      tags=["via ferrata", "iron way", "climbing route", "fixed cable", "rungs", "rock climbing", "mountaineering"])
def _(S):
    return [shell(poly([(2.5, 21.5), (2.5, 7), (8, 2.5), (21.5, 2.5), (21.5, 21.5)], closed=True, r=S.r * 0.3)),
            detail(seg(15, 4.5, 15, 19.5)), detail(seg(9.5, 8, 15, 8)), detail(seg(9.5, 12.5, 15, 12.5)), detail(seg(9.5, 17, 15, 17))]


@icon("cattle-guard", CAT, "Top view of a road crossed by a row of parallel metal bars set in a pit",
      tags=["cattle guard", "cattle grid", "livestock barrier", "ranch road", "farm gate", "road", "grid"])
def _(S):
    return [line(seg(5.5, 2.5, 5.5, 6.5)), line(seg(18.5, 2.5, 18.5, 6.5)), line(seg(5.5, 17.5, 5.5, 21.5)),
            line(seg(18.5, 17.5, 18.5, 21.5)),
            shell(rect(2.5, 6.5, 19, 11, S.R * 0.3)), detail(seg(2.5, 10, 21.5, 10)), detail(seg(2.5, 14, 21.5, 14))]


@icon("river-ford", CAT, "Road dipping into shallow river water and rising out on the far bank, with a depth post",
      tags=["river ford", "ford", "water crossing", "shallow crossing", "depth gauge", "stream", "road"])
def _(S):
    return [line("M2.5 8H6.5Q8 17 12 17T17.5 8H21.5"),
            line("M8 12.5Q10 11 12 12.5T16 12.5"), line(seg(12, 3.5, 12, 11)), line(seg(12, 5.5, 14.5, 5.5))]


@icon("highway-exit", CAT, "Top view of a straight highway with an exit ramp curving off one side",
      tags=["highway exit", "off ramp", "motorway exit", "slip road", "junction exit", "freeway exit", "road"])
def _(S):
    body = union_d(rect(4.5, 2.5, 8.5, 19, S.R * 0.3), poly([(13, 12), (21.5, 5.5), (21.5, 12), (13, 19.5)], closed=True, r=S.r * 0.3))
    return [shell(body), dash_v(8.75, 4.5, 8), dash_v(8.75, 15.5, 19), detail(seg(14.5, 15, 19.5, 10.5))]
