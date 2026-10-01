"""TypeIcon Core: infrastructure (batch 001): roads, road furniture, bridges, tunnels and railway infrastructure.

Top views draw each road as a closed band (shell) so Filled becomes solid asphalt with the centre dashes
knocked out. Dashes shorten by one pixel per end in Rounded, where round caps would lengthen them.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "infrastructure"


def dash(S, x1, y1, x2, y2):
    """Centre dash: shortened in Rounded so the round caps give the same visible length."""
    if S.name == "rounded":
        L = math.hypot(x2 - x1, y2 - y1)
        if L <= 2.0:
            return dot((x1 + x2) / 2, (y1 + y2) / 2, 1.0)
        k = 1.0 / L
        x1, y1, x2, y2 = x1 + (x2 - x1) * k, y1 + (y2 - y1) * k, x2 - (x2 - x1) * k, y2 - (y2 - y1) * k
    return detail(seg(x1, y1, x2, y2))


def hole(d):
    """Dark mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def wave(x, y, w=6.0, h=1.5):
    """Open wavy line starting at (x, y), two half waves per 4 px."""
    n = max(1, int(round(w / 2)))
    d = f"M{fmt(x)} {fmt(y)}q{fmt(w / (2 * n))} {fmt(-h)} {fmt(w / n)} 0"
    for i in range(1, n):
        d += f"t{fmt(w / n)} 0"
    return d


def inside(pts, x, y):
    c = False
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def clip_lines(pts, lines, n=240):
    """Clip straight lines (x1, y1, x2, y2) to the inside of a polygon; returns list of d strings."""
    out = []
    for x1, y1, x2, y2 in lines:
        start = None
        for i in range(n + 1):
            t = i / n
            x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
            ins = inside(pts, x, y)
            if ins and start is None:
                start = (x, y)
            if start is not None and (not ins or i == n):
                end = (x, y)
                if math.hypot(end[0] - start[0], end[1] - start[1]) > 2.5:
                    out.append(seg(round(start[0], 2), round(start[1], 2), round(end[0], 2), round(end[1], 2)))
                start = None
    return out


def head(tip, deg, length=4.0, half=2.4):
    """Solid arrow head triangle whose tip is at `tip`, pointing along angle `deg` (0 = right, 90 = down)."""
    a = math.radians(deg)
    ux, uy = math.cos(a), math.sin(a)
    bx, by = tip[0] - ux * length, tip[1] - uy * length
    px, py = -uy * half, ux * half
    return poly([tip, (bx + px, by + py), (bx - px, by - py)], closed=True)


def tri(p1, p2, p3):
    return poly([p1, p2, p3], closed=True)


# ============================================================================ junctions and road shapes

@icon("mini-roundabout-sign", CAT, "Round sign with three curved arrows chasing each other in a circle",
      tags=["roundabout", "traffic circle", "road sign", "give way", "circular", "junction", "driving"])
def _(S):
    parts = [shell(circle(12, 12, 9))]
    for k in range(3):
        a0 = -90 + k * 120 + 8
        a1 = a0 + 62
        parts.append(detail(arc(12, 12, 4.4, a0, a1)))
        hx, hy = polar(12, 12, 4.4, a1)
        ux, uy = polar(12, 12, 6.9, a1)
        lx, ly = polar(12, 12, 1.9, a1)
        tx, ty = polar(12, 12, 4.4, a1 + 40)
        parts.append(hole(tri((ux, uy), (lx, ly), (tx, ty))))
    return parts


@icon("y-junction", CAT, "Top view of a single road splitting into two roads that fan out in a Y shape",
      tags=["fork", "split", "road", "junction", "branch", "intersection", "driving"])
def _(S):
    pts = [(8.5, 21), (8.5, 14.5), (3.5, 6.5), (8.6, 3.3), (12, 8.7), (15.4, 3.3), (20.5, 6.5), (15.5, 14.5), (15.5, 21)]
    return [shell(poly(pts, closed=True, r=S.r)), dash(S, 12, 16, 12, 19)]


@icon("staggered-junction", CAT, "Top view of a main road with two side roads joining from opposite sides at offset points",
      tags=["crossroads", "offset junction", "intersection", "road", "side road", "t junction", "driving"])
def _(S):
    pts = [(9, 3), (15, 3), (15, 14), (21, 14), (21, 19), (15, 19), (15, 21), (9, 21), (9, 10), (3, 10), (3, 5), (9, 5)]
    return [shell(poly(pts, closed=True, r=S.r * 0.6))]


@icon("highway-ramp", CAT, "Top view of a road peeling off a straight highway in a smooth curve",
      tags=["exit ramp", "slip road", "off ramp", "highway", "motorway", "exit", "freeway"])
def _(S):
    d = "M4 21V3H11V10C14 10 16.5 8 16.5 4L21 5C21 12 17 18 11 19V21Z"
    return [shell(d), dash(S, 7.5, 13, 7.5, 18)]


@icon("underpass", CAT, "Rounded opening under a road embankment with a footpath running into the arch",
      tags=["subway", "pedestrian tunnel", "road", "embankment", "arch", "passage", "under road"])
def _(S):
    d = "M3 21V9H21V21H17V16A5 5 0 0 0 7 16V21Z"
    return [line(seg(3, 4.5, 21, 4.5)), shell(d), line(seg(12, 21, 12, 17))]


@icon("winding-road", CAT, "Road snaking back and forth into the distance in an S curve",
      tags=["curvy road", "bendy", "s bend", "scenic drive", "road trip", "serpentine", "driving"])
def _(S):
    d = ("M3 21C3 15 14 16 14 11.5C14 8 9.5 8 9.5 3H13.5C13.5 8 19.5 8 19.5 11.5C19.5 16 12 15 12 21Z")
    return [shell(d), dash(S, 7.3, 18, 8.5, 15.6), dash(S, 16.5, 10.8, 16.5, 12.3), dash(S, 11.4, 6.8, 11.5, 5)]


@icon("hairpin-bend", CAT, "Top view of a road that turns back on itself in a tight U shaped loop",
      tags=["switchback", "u turn", "mountain road", "sharp bend", "curve", "bend", "driving"])
def _(S):
    d = "M3 21V12A9 9 0 0 1 21 12V21H14V12A2 2 0 0 0 10 12V21Z"
    return [shell(d), dash(S, 6.5, 15.5, 6.5, 18.5), dash(S, 17.5, 15.5, 17.5, 18.5)]


@icon("dual-carriageway", CAT, "Top view of two parallel roads separated by a narrow grass median strip",
      tags=["divided highway", "motorway", "median", "expressway", "four lane", "road", "central reservation"])
def _(S):
    return [
        shell(poly([(3, 3), (9, 3), (9, 21), (3, 21)], closed=True, r=S.r * 0.5)),
        shell(poly([(15, 3), (21, 3), (21, 21), (15, 21)], closed=True, r=S.r * 0.5)),
        dash(S, 6, 7, 6, 10), dash(S, 6, 14, 6, 17),
        dash(S, 18, 7, 18, 10), dash(S, 18, 14, 18, 17),
    ]


@icon("causeway", CAT, "Narrow raised road running straight across water with wavy lines on both sides",
      tags=["raised road", "bridge road", "water crossing", "embankment", "island road", "sea road", "lake road"])
def _(S):
    return [
        shell(poly([(9, 21), (10.5, 3), (13.5, 3), (15, 21)], closed=True, r=S.r * 0.4)),
        line(wave(3, 7, 4)), line(wave(3, 13, 4)), line(wave(3, 19, 4)),
        line(wave(17, 7, 4)), line(wave(17, 13, 4)), line(wave(17, 19, 4)),
    ]


@icon("ford-crossing", CAT, "Road dipping into a band of wavy water and rising out the other side",
      tags=["river crossing", "low water crossing", "stream", "flooded road", "wade", "water on road", "driving"])
def _(S):
    return [
        line(poly([(3, 7), (6.5, 7), (9, 15), (15, 15), (17.5, 7), (21, 7)], r=S.r)),
        line(wave(8, 11, 8)),
    ]


@icon("gravel-road", CAT, "Road into the distance filled with small scattered dots for loose stones",
      tags=["dirt road", "unpaved", "rural road", "loose stones", "track", "off road", "country road"])
def _(S):
    parts = [shell(poly([(5, 21), (10, 3), (14, 3), (19, 21)], closed=True, r=S.r * 0.5))]
    for x, y in [(12, 7.5), (10.5, 12.5), (14, 12), (8.5, 17.5), (12, 16.5), (15.8, 17.5)]:
        parts.append(dot(x, y, 1.15))
    return parts


@icon("cobblestone-street", CAT, "Top view of a street paved with rows of staggered rounded setts",
      tags=["cobbles", "paving", "setts", "old town", "brick road", "stone street", "pavement"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15)),
        detail(seg(12, 3, 12, 9)), detail(seg(7.5, 9, 7.5, 15)), detail(seg(16.5, 9, 16.5, 15)), detail(seg(12, 15, 12, 21)),
    ]


@icon("pothole", CAT, "Road surface with an irregular broken hole and small cracks radiating from it",
      tags=["road damage", "crack", "repair", "hole in road", "broken road", "maintenance", "bad road"])
def _(S):
    hole_pts = [(9, 10.5), (12, 9), (15, 10.5), (15.5, 13.5), (12.5, 15.5), (9, 14.5)]
    return [
        shell(rect(3, 4, 18, 16, S.R)),
        hole(poly(hole_pts, closed=True)),
        detail(poly([(8.5, 9.5), (6, 7.5)])),
        detail(poly([(16, 14.5), (18.5, 16.5)])),
    ]


# ============================================================================ road furniture and structures

@icon("speed-bump", CAT, "Top view of a road with a raised hump across it marked by diagonal stripes",
      tags=["speed hump", "traffic calming", "road hump", "slow down", "sleeping policeman", "driving", "road"])
def _(S):
    return [
        line(seg(4, 3, 4, 21)), line(seg(20, 3, 20, 21)),
        shell(rect(4, 9, 16, 6, S.R * 0.5)),
        detail(seg(9, 15, 12, 9)), detail(seg(15, 15, 18, 9)),
        dash(S, 12, 3, 12, 6), dash(S, 12, 18, 12, 21),
    ]


@icon("rumble-strip", CAT, "Top view of a road edge with a row of short raised ridges beside the edge line",
      tags=["rumble strips", "edge line", "lane departure", "road safety", "shoulder", "highway", "warning strip"])
def _(S):
    parts = [line(seg(13, 3, 13, 21))]
    for y in (4.5, 9.5, 14.5, 19.5):
        parts.append(line(seg(4, y, 10, y)))
    parts += [dash(S, 19, 5, 19, 9), dash(S, 19, 15, 19, 19)]
    return parts


@icon("guardrail", CAT, "Corrugated steel crash barrier rail running along short posts beside a road",
      tags=["crash barrier", "safety barrier", "roadside", "highway", "w beam", "railing", "motorway"])
def _(S):
    return [
        shell(rect(3, 5, 18, 7, S.R * 0.5)),
        detail(seg(3, 8.5, 21, 8.5)),
        line(seg(6.5, 12, 6.5, 20)), line(seg(12, 12, 12, 20)), line(seg(17.5, 12, 17.5, 20)),
    ]


@icon("road-median", CAT, "Top view of two opposing lanes divided by a raised curbed strip with small trees",
      tags=["central reservation", "divider", "traffic divider", "planted median", "boulevard", "avenue", "road"])
def _(S):
    return [
        line(seg(3, 3, 3, 21)), line(seg(21, 3, 21, 21)),
        shell(rect(9, 3, 6, 18, S.R * 0.5)),
        dot(12, 8, 1.4), dot(12, 16, 1.4),
    ]


@icon("pedestrian-refuge", CAT, "Top view of a crossing with bars on both sides of a small raised island in the middle of the road",
      tags=["crossing island", "zebra crossing", "crosswalk", "median refuge", "road crossing", "pedestrians", "safe crossing"])
def _(S):
    parts = [line(seg(3, 3, 3, 21)), line(seg(21, 3, 21, 21)), shell(rect(10, 5, 4, 14, S.R * 0.5))]
    for y in (8, 12, 16):
        parts += [line(seg(3, y, 7, y)), line(seg(17, y, 21, y))]
    return parts


@icon("curb-ramp", CAT, "Side view of a dropped kerb sloping from the pavement down to the road with a wheel rolling down it",
      tags=["dropped kerb", "wheelchair ramp", "sidewalk ramp", "accessibility", "curb cut", "accessible", "pavement ramp"])
def _(S):
    return [
        shell(poly([(3, 11), (9, 11), (14, 17), (21, 17), (21, 21), (3, 21)], closed=True, r=S.r * 0.5)),
        shell(circle(14.6, 8.2, 2.6)),
        dot(14.6, 8.2, 0.8),
    ]


@icon("tactile-paving", CAT, "Square paving slab covered in a grid of raised round studs",
      tags=["blister paving", "detectable warning", "visually impaired", "accessibility", "pavement", "tactile tiles", "crossing"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, S.R))]
    for x in (7.5, 12, 16.5):
        for y in (7.5, 12, 16.5):
            parts.append(dot(x, y, 1.3))
    return parts


@icon("storm-drain", CAT, "Rectangular grate with parallel slots set into the gutter at the edge of a kerb",
      tags=["drain grate", "gutter", "sewer grate", "catch basin", "rainwater", "street drain", "gully"])
def _(S):
    return [
        line(seg(3, 4.5, 21, 4.5)),
        shell(rect(3, 8.5, 18, 10, S.R * 0.5)),
        detail(seg(7.5, 8.5, 7.5, 18.5)), detail(seg(12, 8.5, 12, 18.5)), detail(seg(16.5, 8.5, 16.5, 18.5)),
    ]


@icon("snow-pole", CAT, "Tall thin striped marker pole beside a road half buried in a snowbank",
      tags=["road marker", "winter", "roadside", "snow marker", "delineator", "snowdrift", "stick"])
def _(S):
    return [
        shell(rect(10, 3, 4, 14, S.R * 0.5)),
        Part("dot", rect(11, 6, 2, 2.5)), Part("dot", rect(11, 11, 2, 2.5)),
        shell("M3 21C5 18 8 16.5 12 16.5C16 16.5 19 18 21 21Z"),
        dot(5.5, 8, 1), dot(18.5, 7, 1), dot(19, 13, 1), dot(6, 13.5, 1),
    ]


@icon("noise-barrier", CAT, "Tall wall of panels beside a highway with sound waves stopped against it",
      tags=["sound wall", "acoustic barrier", "noise wall", "highway", "soundproof", "traffic noise", "motorway"])
def _(S):
    return [
        dot(4, 12, 1.4),
        line(arc(4, 12, 3.6, -50, 50)), line(arc(4, 12, 7.2, -50, 50)),
        shell(rect(14.5, 3, 5, 18, S.R * 0.5)),
        detail(seg(14.5, 9, 19.5, 9)), detail(seg(14.5, 15, 19.5, 15)),
    ]


@icon("wildlife-crossing-bridge", CAT, "Planted bridge over a highway with a deer standing on top",
      tags=["animal bridge", "green bridge", "ecoduct", "deer", "wildlife overpass", "nature", "conservation"])
def _(S):
    body = "M5 9.5H11.5L13 6.5L13.3 4.5L15.3 5.5L15.6 7.3L13.3 10.5V12.5H11.9V11H6.6V12.5H5.2Z"
    return [
        solid(body),
        line("M13.6 4.2L12.6 2.5"), line("M14.8 4.2L16 2.5"),
        shell("M3 21V14H21V21H16.5V19A4.5 4.5 0 0 0 7.5 19V21Z"),
    ]


@icon("culvert", CAT, "Round concrete pipe opening under a road embankment with a stream flowing out",
      tags=["drainage pipe", "stormwater", "water pipe", "road drainage", "creek", "embankment", "tunnel pipe"])
def _(S):
    embank = "M3 16L7 4H17L21 16Z" + "M14.7 11A2.7 2.7 0 0 0 9.3 11A2.7 2.7 0 0 0 14.7 11Z"
    return [shell(embank), line(wave(3, 20.3, 18, 1.2))]


@icon("retaining-wall", CAT, "Stepped wall of stacked blocks holding back a sloping bank of earth",
      tags=["earth wall", "embankment", "hillside", "slope", "masonry", "civil engineering", "landscaping"])
def _(S):
    return [
        line(poly([(3, 13), (12, 5)])),
        shell(rect(13, 4, 8, 17, S.R * 0.5)),
        detail(seg(13, 9.7, 21, 9.7)), detail(seg(13, 15.3, 21, 15.3)),
        detail(seg(17, 4, 17, 9.7)), detail(seg(15, 9.7, 15, 15.3)), detail(seg(17, 15.3, 17, 21)),
        line(seg(3, 21, 12, 21)),
    ]


# ============================================================================ mountain roads, bays and markings

@icon("avalanche-gallery", CAT, "Road running under a sloped concrete roof on columns built into a mountainside, with snow above",
      tags=["snow shed", "avalanche shelter", "mountain road", "snow gallery", "rockfall", "alpine road", "winter"])
def _(S):
    return [
        shell(poly([(4, 8), (21, 14), (21, 18), (4, 12)], closed=True, r=S.r * 0.4)),
        line(seg(8, 13.4, 8, 21)), line(seg(14, 15.5, 14, 21)), line(seg(20, 17.7, 20, 21)),
        dot(8, 4.5, 1.1), dot(13, 6.5, 1.1), dot(18, 8.5, 1.1),
        line(seg(3, 21, 21, 21)),
    ]


_CLIFF = [(3, 17), (3, 9), (7, 5), (12, 8), (17, 4), (21, 9), (21, 17)]


@icon("rockfall-net", CAT, "Steep rock face covered with a diamond mesh net above a road",
      tags=["rock netting", "slope protection", "landslide", "rockfall barrier", "mesh", "cliff", "mountain road"])
def _(S):
    lines = [(0, c, 24, 24 + c) for c in (-12, -4, 4, 12)] + [(0, c, 24, c - 24) for c in (14, 22, 30, 38)]
    return [shell(poly(_CLIFF, closed=True, r=S.r * 0.5))] + [detail(d) for d in clip_lines(_CLIFF, lines)] + [line(seg(3, 21, 21, 21))]


@icon("lay-by", CAT, "Top view of a road with a lozenge shaped pull-in bay beside it holding a parked car",
      tags=["pull in", "roadside parking", "parking bay", "stopping place", "rest stop", "road", "pull over"])
def _(S):
    edge = [(11, 3), (11, 6), (14, 8), (21, 8), (21, 16), (14, 16), (11, 18), (11, 21)]
    return [
        line(seg(3, 3, 3, 21)),
        line(poly(edge, r=S.r * 0.5)),
        Part("dot", rect(15.5, 9.5, 3.5, 5, 1)),
        dash(S, 7, 6, 7, 9), dash(S, 7, 15, 7, 18),
    ]


@icon("hard-shoulder", CAT, "Top view of a highway with a wide hatched emergency lane along the outside edge",
      tags=["emergency lane", "breakdown lane", "motorway", "highway shoulder", "verge", "safety lane", "road"])
def _(S):
    return [
        line(seg(3, 3, 3, 21)),
        dash(S, 8, 4, 8, 8), dash(S, 8, 10, 8, 14), dash(S, 8, 16, 8, 20),
        shell(rect(14, 3, 7, 18, S.R * 0.5)),
        detail(seg(14, 9, 21, 6)), detail(seg(14, 15, 21, 12)), detail(seg(14, 21, 21, 18)),
    ]


@icon("emergency-phone-box", CAT, "Small roadside call box on a post with a handset and a panel for the emergency button",
      tags=["sos phone", "roadside telephone", "call box", "highway emergency", "breakdown help", "help point", "telephone"])
def _(S):
    return [
        shell(rect(6, 3, 12, 13, S.R * 0.6)),
        detail(seg(6, 7.5, 18, 7.5)),
        detail("M9.5 10.5V11.5C9.5 12.5 10.5 13 11.5 13H14.5V12"),
        line(seg(12, 16, 12, 21)),
    ]


@icon("rest-area", CAT, "Picnic table beside a tree at a roadside stopping place",
      tags=["picnic area", "roadside stop", "layby", "service stop", "highway rest", "picnic table", "stopping place"])
def _(S):
    return [
        shell(circle(7.5, 8, 4.5)),
        line(seg(7.5, 12.5, 7.5, 20)),
        line(seg(11.5, 12, 21, 12)),
        line(seg(13, 12, 11.5, 20)), line(seg(19.5, 12, 21, 20)),
        line(seg(12.3, 16, 20.2, 16)),
        line(seg(3, 21, 21, 21)),
    ]


@icon("bus-lane", CAT, "Top view of a lane between solid lines with a bus shape painted on it",
      tags=["bus priority", "public transport lane", "bus only", "transit lane", "road marking", "buses", "city road"])
def _(S):
    return [
        line(seg(3.5, 3, 3.5, 21)), line(seg(20.5, 3, 20.5, 21)),
        shell(rect(8, 4, 8, 16, S.R * 0.5)),
        detail(seg(8, 8, 16, 8)), detail(seg(8, 16, 16, 16)),
    ]


@icon("carpool-lane", CAT, "Top view of a lane between solid lines with a diamond painted in the middle",
      tags=["hov lane", "high occupancy", "car share lane", "diamond lane", "ride share", "road marking", "highway"])
def _(S):
    return [
        line(seg(4, 3, 4, 21)), line(seg(20, 3, 20, 21)),
        shell(poly([(12, 4), (17.5, 12), (12, 20), (6.5, 12)], closed=True, r=S.r * 0.6)),
    ]


@icon("tram-tracks-street", CAT, "Street seen in perspective with a pair of rails embedded in the road surface",
      tags=["tramway", "streetcar", "light rail", "embedded rails", "city street", "tram line", "road"])
def _(S):
    return [
        shell(poly([(3, 21), (7, 3), (17, 3), (21, 21)], closed=True, r=S.r * 0.4)),
        detail(seg(8.5, 21, 10.5, 3)), detail(seg(15.5, 21, 13.5, 3)),
    ]


@icon("give-way-marking", CAT, "Top view of a lane with a row of triangular teeth and a painted inverted triangle",
      tags=["yield marking", "shark teeth", "road marking", "priority", "junction", "give way line", "yield"])
def _(S):
    parts = [line(seg(3, 3, 3, 21)), line(seg(21, 3, 21, 21))]
    for x in (8, 12, 16):
        parts.append(solid(poly([(x - 2, 4), (x + 2, 4), (x, 8)], closed=True)))
    parts.append(shell(poly([(6.5, 12), (17.5, 12), (12, 20.5)], closed=True, r=S.r)))
    return parts


@icon("yellow-box-junction", CAT, "Top view of a crossroads whose centre square is filled with crisscross diagonal hatching",
      tags=["box junction", "keep clear", "hatched junction", "intersection", "road marking", "no stopping", "crossroads"])
def _(S):
    pts = [(8, 3), (16, 3), (16, 8), (21, 8), (21, 16), (16, 16), (16, 21), (8, 21), (8, 16), (3, 16), (3, 8), (8, 8)]
    box = [(8, 8), (16, 8), (16, 16), (8, 16)]
    lines = [(0, c, 24, 24 + c) for c in (-8, 0, 8)] + [(0, c, 24, c - 24) for c in (16, 24, 32)]
    return [shell(poly(pts, closed=True, r=S.r * 0.3))] + [detail(d) for d in clip_lines(box, lines)]


@icon("lane-arrow-marking", CAT, "Top view of a lane with a painted arrow that goes straight ahead and branches to one side",
      tags=["road arrow", "straight or turn", "road marking", "lane guidance", "turn lane", "direction", "pavement arrow"])
def _(S):
    return [
        line(seg(3, 3, 3, 21)), line(seg(21, 3, 21, 21)),
        line(seg(9, 21, 9, 8)), solid(head((9, 3.5), -90, 5, 3.2)),
        line(poly([(9, 16), (14, 11)])), solid(head((18, 6.5), -45, 5, 3.2)),
    ]


@icon("chevron-hatching", CAT, "Top view of a road area filled with painted V shaped chevron stripes inside a border",
      tags=["painted island", "road marking", "hatched area", "chevron markings", "divergence zone", "no entry zone", "highway"])
def _(S):
    return [
        shell(rect(5, 3, 14, 18, S.R * 0.5)),
        detail(poly([(5, 10), (12, 6), (19, 10)])), detail(poly([(5, 17), (12, 13), (19, 17)])),
    ]


@icon("parking-bay-lines", CAT, "Top view of three rectangular parking spaces marked by painted lines with a car in one",
      tags=["parking spaces", "car park", "parking lot", "bay markings", "parking stalls", "marked bays", "parking"])
def _(S):
    parts = [line(seg(3, 5, 21, 5))]
    for x in (3, 9, 15, 21):
        parts.append(line(seg(x, 5, x, 19)))
    parts.append(solid(rect(10.5, 9, 3, 7, 1.2)))
    return parts


@icon("accessible-parking-space", CAT, "Top view of a parking space with a wheelchair symbol painted inside it",
      tags=["disabled parking", "handicap parking", "wheelchair", "blue badge", "accessible bay", "reserved parking", "accessibility"])
def _(S):
    return [
        line(poly([(4, 21), (4, 3), (20, 3), (20, 21)], r=S.r * 0.6)),
        dot(10.5, 7, 1.4),
        line("M10.5 10V14H15.5L17 18"),
        line(arc(10.5, 15.5, 3.3, 140, 400)),
    ]


@icon("zigzag-road-marking", CAT, "Top view of a road edge with a painted zigzag line leading up to a crossing",
      tags=["zig zag lines", "no parking zone", "pedestrian crossing approach", "road marking", "kerb markings", "crossing", "no stopping"])
def _(S):
    return [
        line(seg(4, 3, 4, 21)),
        line(poly([(9, 3), (15, 7.5), (9, 12), (15, 16.5), (9, 21)], r=S.r * 0.5)),
    ]


# ============================================================================ bridges and tunnels

@icon("suspension-bridge", CAT, "Two tall towers with a deep curved main cable between them and a hanger down to a flat deck",
      tags=["bridge", "cable bridge", "golden gate style", "span", "river crossing", "engineering", "landmark"])
def _(S):
    return [
        line(seg(3, 16, 21, 16)),
        line(seg(7, 3, 7, 21)), line(seg(17, 3, 17, 21)),
        line("M7 4C10 14 14 14 17 4"),
        line(seg(12, 11, 12, 16)),
        line("M7 4Q5 10 3 14"), line("M17 4Q19 10 21 14"),
    ]


@icon("cable-stayed-bridge", CAT, "One tall central pylon with straight cables fanning down diagonally to a flat deck",
      tags=["bridge", "pylon", "stay cables", "modern bridge", "river crossing", "engineering", "span"])
def _(S):
    return [
        line(seg(3, 17, 21, 17)),
        line(seg(12, 3, 12, 21)),
        line(seg(12, 5, 3.5, 16)), line(seg(12, 5, 7.5, 16)),
        line(seg(12, 5, 20.5, 16)), line(seg(12, 5, 16.5, 16)),
    ]


@icon("arch-bridge", CAT, "Steel arch rising above a flat deck with vertical hangers connecting them",
      tags=["bridge", "tied arch", "steel bridge", "river crossing", "engineering", "span", "landmark"])
def _(S):
    return [
        line(seg(3, 16, 21, 16)),
        line("M3 16C3 3 21 3 21 16"),
        line(seg(8.2, 8.5, 8.2, 16)), line(seg(15.8, 8.5, 15.8, 16)),
        line(seg(3, 20, 3, 16)), line(seg(21, 20, 21, 16)),
    ]


@icon("truss-bridge", CAT, "Flat deck topped by a steel frame of repeated triangles",
      tags=["bridge", "steel truss", "girder", "railway bridge", "warren truss", "engineering", "span"])
def _(S):
    return [
        line(poly([(3, 16), (7.5, 6), (12, 16), (16.5, 6), (21, 16)], r=S.r)),
        line(seg(7.5, 6, 16.5, 6)),
        line(seg(3, 16, 21, 16)),
        line(seg(3, 16, 3, 21)), line(seg(21, 16, 21, 21)),
    ]


@icon("beam-bridge", CAT, "Flat straight deck resting on three simple square piers over water",
      tags=["bridge", "girder bridge", "viaduct", "overpass", "river crossing", "engineering", "piers"])
def _(S):
    return [
        shell(rect(3, 6, 18, 4, S.R * 0.5)),
        line(seg(6, 10, 6, 20)), line(seg(12, 10, 12, 20)), line(seg(18, 10, 18, 20)),
        line(wave(3, 20, 18, 1.2)),
    ]


@icon("bascule-bridge", CAT, "Bridge whose two deck leaves are tilted upward in the middle to let a boat pass",
      tags=["drawbridge", "opening bridge", "lifting bridge", "tower bridge style", "river", "boat passing", "movable bridge"])
def _(S):
    return [
        line(seg(3, 14, 8, 14)), line(seg(16, 14, 21, 14)),
        line(poly([(8, 14), (11, 4)])), line(poly([(16, 14), (13, 4)])),
        line(seg(8, 14, 8, 19)), line(seg(16, 14, 16, 19)),
        line(wave(3, 20, 18, 1.2)),
    ]


@icon("swing-bridge", CAT, "Top view of a bridge deck pivoted sideways on a central pier with a curved arrow showing it turning",
      tags=["rotating bridge", "pivot bridge", "movable bridge", "canal", "river", "opening bridge", "turning"])
def _(S):
    a = math.radians(-32)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    L, W = 8.5, 2.2
    cx, cy = 11, 10.5
    deck = [(cx - ux * L - nx * W, cy - uy * L - ny * W), (cx + ux * L - nx * W, cy + uy * L - ny * W),
            (cx + ux * L + nx * W, cy + uy * L + ny * W), (cx - ux * L + nx * W, cy - uy * L + ny * W)]
    ex, ey = polar(12, 12, 8.5, 84)
    return [
        shell(poly(deck, closed=True, r=S.r * 0.3)),
        dot(cx, cy, 1.0),
        line(arc(12, 12, 8.5, 6, 56)), solid(head((ex, ey), 84 + 90, 5.5, 3.2)),
    ]


@icon("vertical-lift-bridge", CAT, "Two tall towers with a flat deck section raised high between them above a boat",
      tags=["lift bridge", "movable bridge", "raised deck", "canal", "river", "boat passing", "tower bridge"])
def _(S):
    return [
        shell(rect(3, 3, 4, 18, S.R * 0.4)), shell(rect(17, 3, 4, 18, S.R * 0.4)),
        line(seg(7, 8, 17, 8)),
        shell(poly([(8, 15), (16, 15), (14, 19), (10, 19)], closed=True, r=S.r * 0.5)),
    ]


@icon("footbridge", CAT, "Narrow arched walkway with a small walking person on it",
      tags=["pedestrian bridge", "walkway", "walking", "park bridge", "arched bridge", "crossing", "path"])
def _(S):
    return [
        line("M3 19C8 12 16 12 21 19"),
        dot(12, 5.5, 1.5),
        line("M12 8.5V12"),
        line(seg(3, 19, 3, 21)), line(seg(21, 19, 21, 21)),
    ]


@icon("covered-bridge", CAT, "Wooden bridge with a pitched roof and walls like a barn spanning a stream",
      tags=["wooden bridge", "timber bridge", "rural", "heritage", "barn bridge", "river crossing", "new england"])
def _(S):
    pts = [(3, 18), (3, 10), (12, 4.5), (21, 10), (21, 18), (17, 18), (17, 13), (7, 13), (7, 18)]
    return [shell(poly(pts, closed=True, r=S.r * 0.5)), line(wave(3, 21, 18, 1.0))]


@icon("stone-arch-bridge", CAT, "Stone bridge with two round arches over water and a block line along the deck",
      tags=["masonry bridge", "viaduct", "roman bridge", "arched bridge", "heritage", "river crossing", "old bridge"])
def _(S):
    d = "M3 19V7H21V19H19V17A3 3 0 0 0 13 17V19H11V17A3 3 0 0 0 5 17V19Z"
    return [shell(d)]


@icon("pontoon-bridge", CAT, "Flat roadway resting on a row of floating boats on wavy water",
      tags=["floating bridge", "boat bridge", "temporary bridge", "military bridge", "river", "crossing", "barges"])
def _(S):
    parts = [line(seg(3, 10, 21, 10))]
    for x0 in (3, 9.5, 16):
        parts.append(shell(poly([(x0, 12), (x0 + 5, 12), (x0 + 4, 16), (x0 + 1, 16)], closed=True, r=S.r * 0.4)))
    parts.append(line(wave(3, 20, 18, 1.2)))
    return parts


@icon("railway-tunnel", CAT, "Round arched tunnel mouth in a rock face with railway tracks leading into it",
      tags=["train tunnel", "rail tunnel", "mountain tunnel", "portal", "tracks", "hill", "underground"])
def _(S):
    d = "M3 21V13C3 7 7 4 12 4C17 4 21 7 21 13V21H16V14A4 4 0 0 0 8 14V21Z"
    return [shell(d), line(seg(10.5, 21, 11.3, 15.5)), line(seg(13.5, 21, 12.7, 15.5))]


@icon("underwater-tunnel", CAT, "Tube shaped tunnel running under wavy water lines with a car inside",
      tags=["subsea tunnel", "immersed tunnel", "channel tunnel", "road tunnel", "under river", "seabed", "crossing"])
def _(S):
    return [
        line(wave(3, 6, 18, 1.3)),
        shell(rect(3, 11, 18, 9, S.R * 1.5)),
        Part("dot", rect(8, 14.5, 8, 3, 1.2)),
    ]


@icon("tunnel-portal-sign", CAT, "Rectangular sign showing a tunnel arch with a road going in",
      tags=["tunnel ahead", "road sign", "traffic sign", "tunnel entrance", "warning sign", "highway sign", "tunnel"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail("M7.5 18V12.5A4.5 4.5 0 0 1 16.5 12.5V18"),
        detail(seg(12, 18, 12, 15)),
    ]


# ============================================================================ railway infrastructure

def _board(cx, cy, length, width, deg):
    a = math.radians(deg)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    l, w = length / 2, width / 2
    return [(cx - ux * l - nx * w, cy - uy * l - ny * w), (cx + ux * l - nx * w, cy + uy * l - ny * w),
            (cx + ux * l + nx * w, cy + uy * l + ny * w), (cx - ux * l + nx * w, cy - uy * l + ny * w)]


@icon("crossbuck-sign", CAT, "Two white boards crossed in an X on a post, the railroad crossing sign",
      tags=["railroad crossing", "level crossing sign", "railway crossing", "grade crossing", "train warning", "road sign", "x sign"])
def _(S):
    return [
        line(seg(12, 11, 12, 21)),
        shell(poly(_board(12, 9, 17, 4.5, 33), closed=True, r=S.r * 0.3)),
        shell(poly(_board(12, 9, 17, 4.5, -33), closed=True, r=S.r * 0.3)),
    ]


@icon("level-crossing-lights", CAT, "Post with two round warning lamps side by side under a crossbuck",
      tags=["railroad crossing", "flashing lights", "railway crossing", "train warning", "signal lamps", "grade crossing", "crossing signal"])
def _(S):
    return [
        line(seg(5, 3.5, 19, 9.5)), line(seg(5, 9.5, 19, 3.5)),
        line(seg(12, 8, 12, 21)),
        line(seg(6, 14.5, 18, 14.5)),
        dot(6, 14.5, 2.4), dot(18, 14.5, 2.4),
    ]


@icon("level-crossing-barrier", CAT, "Long striped boom lowered across a road from a pivot post",
      tags=["railroad crossing gate", "boom barrier", "crossing gate", "train crossing", "railway gate", "road closed", "level crossing"])
def _(S):
    return [
        shell(rect(3, 6, 4, 15, S.R * 0.5)),
        dot(5, 11.5, 0.8),
        shell(rect(7, 9.5, 14, 4, S.R * 0.4)),
        detail(seg(11.5, 9.5, 11.5, 13.5)), detail(seg(15.5, 9.5, 15.5, 13.5)), detail(seg(19, 9.5, 19, 13.5)),
    ]


@icon("railway-track", CAT, "Two parallel rails on evenly spaced wooden sleepers running into the distance",
      tags=["train track", "rails", "railroad", "sleepers", "ties", "rail line", "perspective"])
def _(S):
    return [
        line(seg(7, 21, 9, 3)), line(seg(17, 21, 15, 3)),
        line(seg(4.5, 18.5, 19.5, 18.5)), line(seg(5.3, 12.5, 18.7, 12.5)), line(seg(6, 6.5, 18, 6.5)),
    ]


@icon("railway-switch", CAT, "Top view of a railway track dividing into a straight track and a curved diverging track with crossties",
      tags=["points", "turnout", "railroad switch", "track fork", "rail junction", "diverging track", "train"])
def _(S):
    return [
        line(seg(10, 21, 10, 3)),
        line("M10 14C10 9 14 8 19 3"),
        line(seg(6.5, 19, 13.5, 19)), line(seg(6.5, 16, 13.5, 16)),
        solid(poly([(10, 14), (8.5, 10), (11.5, 11)], closed=True)),
    ]


@icon("buffer-stop", CAT, "End of a railway track with a heavy beam holding two round buffers",
      tags=["end of line", "track end", "bumper", "dead end", "railway", "train terminus", "stop block"])
def _(S):
    return [
        line(seg(9, 13, 9, 21)), line(seg(15, 13, 15, 21)),
        line(seg(6.5, 17, 17.5, 17)),
        shell(rect(3, 5, 18, 4, S.R * 0.5)),
        shell(circle(8, 11.5, 2.2)), shell(circle(16, 11.5, 2.2)),
    ]


@icon("railway-signal", CAT, "Tall post with a narrow signal head holding three round lamps",
      tags=["train signal", "rail signal", "colour light signal", "railroad signal", "stop go", "track signal", "block signal"])
def _(S):
    return [
        shell(rect(8.5, 2.5, 7, 14.5, S.R * 0.5)),
        dot(12, 6.2, 1.5), dot(12, 9.8, 1.5), dot(12, 13.4, 1.5),
        line(seg(12, 17, 12, 21)),
        line(seg(8, 21, 16, 21)),
    ]


@icon("semaphore-signal", CAT, "Tall post with a flat signal arm sticking out sideways near the top",
      tags=["railway semaphore", "signal arm", "train signal", "mechanical signal", "railroad", "vintage signal", "heritage railway"])
def _(S):
    return [
        line(seg(8, 3, 8, 21)),
        shell(poly([(8, 5), (20, 8), (20, 11.5), (8, 8.5)], closed=True, r=S.r * 0.3)),
        dot(17.5, 9.2, 0.9),
        line(seg(4, 21, 12, 21)),
    ]


@icon("signal-box", CAT, "Two storey railway building with a row of windows on the upper floor and an outside stair",
      tags=["signal cabin", "railway building", "control tower", "train control", "interlocking", "station", "heritage railway"])
def _(S):
    return [
        shell(rect(3, 4, 14, 7, S.R * 0.5)),
        detail(seg(7.7, 4, 7.7, 11)), detail(seg(12.3, 4, 12.3, 11)),
        shell(rect(5, 11, 10, 10, S.R * 0.3)),
        detail("M8.5 21V16H11.5V21"),
        line(seg(18, 21, 21, 12)),
    ]


@icon("train-platform", CAT, "Raised platform with a warning line, a canopy on posts and a hanging station sign",
      tags=["railway platform", "train station", "boarding", "canopy", "waiting area", "rail station", "commuter"])
def _(S):
    return [
        shell(rect(3, 3, 18, 3.5, S.R * 0.4)),
        line(seg(5.5, 6.5, 5.5, 15)), line(seg(18.5, 6.5, 18.5, 15)),
        line(seg(12, 6.5, 12, 9)), solid(rect(9.5, 9, 5, 3, 0.6)),
        shell(rect(3, 15, 18, 6, S.R * 0.4)),
        detail(seg(3, 18, 21, 18)),
    ]


@icon("overhead-catenary", CAT, "Tall mast with a cantilever arm holding the overhead wire above a rail track",
      tags=["overhead line", "electric railway", "pantograph wire", "traction power", "electrified track", "mast", "train power"])
def _(S):
    return [
        line(seg(6, 3, 6, 21)),
        line(seg(6, 5, 18, 5)), line(seg(6, 11, 12.5, 5)),
        line(seg(18, 5, 18, 10)), line(seg(10, 10, 21, 10)),
        line(seg(10, 19, 21, 19)),
    ]


@icon("rail-yard", CAT, "Top view of many parallel tracks fanning out from a single track",
      tags=["marshalling yard", "classification yard", "sidings", "freight yard", "railway depot", "train tracks", "switching yard"])
def _(S):
    parts = [line(seg(12, 21, 12, 15)), line(seg(9, 19, 15, 19))]
    for x in (3, 7.5, 12, 16.5, 21):
        parts.append(line(seg(12, 15, x, 3)))
    return parts


@icon("engine-shed", CAT, "Long railway shed with an arched doorway and tracks running inside",
      tags=["locomotive shed", "train depot", "roundhouse", "rail depot", "engine house", "maintenance shed", "railway"])
def _(S):
    d = "M3 21V9L12 3.5L21 9V21H17V14A5 5 0 0 0 7 14V21Z"
    return [shell(d), line(seg(10.5, 21, 11.3, 16.5)), line(seg(13.5, 21, 12.7, 16.5)), line(seg(17.5, 6.8, 17.5, 3))]
