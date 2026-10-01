"""TypeIcon Core: geography (batch 003).

Landforms, map tools, survey and navigation instruments, routes and map types. Closed silhouettes are
shells, inner lines are details, open strokes are lines; small solid marks are `dot`s that are knocked
out of Filled shells. Heavy drawings stay at most 4 to 6 parts so they read at 16 px.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path  # noqa: F401

CAT = "geography"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rp(pts, deg, closed=False, r=0.0, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    q = [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]
    return poly(q, closed=closed, r=r)


def wave(x, y, w, a=1.2, n=2):
    """Sine-like wave of n half periods of width w/n starting at (x, y)."""
    h = w / n
    s = f"M{fmt(x)} {fmt(y)}q{fmt(h / 2)} {fmt(-a)} {fmt(h)} 0"
    for i in range(1, n):
        s += f"t{fmt(h)} 0"
    return s


def pt_on_(cx, cy, r, deg):
    return (cx + r * math.cos(math.radians(deg)), cy + r * math.sin(math.radians(deg)))


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def smooth(pts, closed=True, t=0.5):
    """Catmull-Rom spline through pts as cubic Beziers (closed loop by default)."""
    n = len(pts)
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[0]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3 * 1.0, p1[1] + (p2[1] - p0[1]) * t / 3 * 1.0)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3 * 1.0, p2[1] - (p3[1] - p1[1]) * t / 3 * 1.0)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d + ("Z" if closed else "")


def dashed_ellipse(cx, cy, rx, ry, n=8, frac=0.55, pts=4):
    """List of short open polylines (d strings) that dash an ellipse."""
    out = []
    for k in range(n):
        a0 = 2 * math.pi * k / n
        a1 = a0 + 2 * math.pi / n * frac
        ps = [(cx + rx * math.cos(a0 + (a1 - a0) * i / (pts - 1)), cy + ry * math.sin(a0 + (a1 - a0) * i / (pts - 1)))
              for i in range(pts)]
        out.append(poly(ps))
    return out


def tree(cx, base, h=5, w=2.5):
    """Narrow conifer spire: apex at top, base width 2w."""
    return poly([(cx - w, base), (cx, base - h), (cx + w, base)], closed=True)


# ============================================================================ chunk 1

@icon("boardwalk", CAT, "Raised plank walkway on posts above wet ground",
      tags=["boardwalk", "wooden walkway", "marsh", "wetland", "trail", "pier", "footpath"])
def _(S):
    return [shell(rect(2, 7, 20, 4, L(S, 0, 2))),
            detail(seg(8, 7, 8, 11)), detail(seg(16, 7, 16, 11)),
            line(seg(6, 11, 6, 17)), line(seg(18, 11, 18, 17)),
            line(wave(2, 20, 20, 1.2, 4))]


@icon("meeting-point", CAT, "Four arrows pointing inward to a central dot",
      tags=["meeting point", "rally point", "gather", "converge", "muster", "assembly point", "meet"])
def _(S):
    out = []
    for k in range(4):
        a = 90 * k
        out.append(line(rp([(12, 2.5), (12, 7.5)], a)))
        out.append(line(rp([(9.5, 5.5), (12, 8), (14.5, 5.5)], a, r=S.r)))
    out.append(dot(12, 12, 1.75))
    return out


@icon("dam", CAT, "Concrete dam wall holding back a reservoir, with a stream running out below",
      tags=["dam", "reservoir", "hydroelectric", "barrage", "spillway", "weir", "water wall"])
def _(S):
    return [shell(poly([(9, 4), (14, 4), (19, 18), (9, 18)], closed=True, r=S.r)),
            line(wave(2, 8, 5, 1.2, 2)), line(wave(2, 13, 5, 1.2, 2)),
            line(wave(2, 21, 20, 1.2, 4))]


@icon("aqueduct", CAT, "Stone arch bridge carrying a water channel along its top",
      tags=["aqueduct", "roman", "arches", "water channel", "viaduct", "ancient", "conduit"])
def _(S):
    out = [shell(rect(2, 4, 20, 3, L(S, 0, 1.5))), line(seg(2, 21, 22, 21))]
    for x in (3, 9, 15):
        out.append(line(f"M{x} 21V14A3 3 0 0 1 {x + 6} 14V21"))
    return out


@icon("ancient-ruins", CAT, "Broken column and a partial arch standing on a stone base",
      tags=["ruins", "ancient ruins", "column", "archaeology", "temple", "antiquity", "heritage site"])
def _(S):
    return [shell(rect(2, 18, 20, 3, L(S, 0, 1.5))),
            shell(poly([(4, 18), (4, 10), (6, 12), (8, 9), (8, 18)], closed=True, r=S.r * 0.5)),
            line("M14 18V14a4 4 0 0 1 4-4"),
            line(seg(22, 18, 22, 15))]


@icon("atlas-book", CAT, "Thick book with a globe on its cover",
      tags=["atlas", "book", "world atlas", "geography book", "globe", "maps", "reference"])
def _(S):
    return [shell(rect(4, 2, 16, 20, S.R)),
            detail(seg(7, 2, 7, 22)),
            detail(circle(13.5, 10.5, 4.5)),
            detail("M13.5 6Q10.5 10.5 13.5 15"),
            detail(seg(9, 10.5, 18, 10.5)),
            line(seg(10, 18, 17, 18))]


@icon("water-compass", CAT, "Bowl of water with a leaf floating on it carrying a needle",
      tags=["water compass", "floating needle", "wet compass", "ancient compass", "bowl", "leaf", "navigation"])
def _(S):
    leaf = rot(L(S, "M6.5 9Q12 5 17.5 9Q12 13 6.5 9Z", "M6.5 9A5.5 3 0 0 1 17.5 9A5.5 3 0 0 1 6.5 9Z"), -15, 12, 9)
    return [shell(ellipse(12, 9, 9.5, 5)),
            line("M3 10C3 19 21 19 21 10"),
            mark(leaf)]


@icon("cartographer", CAT, "Person leaning over a large map on a table with a pen",
      tags=["cartographer", "mapmaker", "map maker", "surveyor", "draw map", "geographer", "chart"])
def _(S):
    return [shell(circle(6, 6, 2.5)),
            line("M4 20V14C4 11 7 9.5 9 10.5L15 14"),
            shell(rect(10, 15, 12, 2, L(S, 0, 1))),
            line(seg(12, 17, 12, 21)), line(seg(20, 17, 20, 21)),
            line(seg(15, 14, 17, 9))]


@icon("shadow-stick-compass", CAT, "Stick casting shadows with pebbles marking the shadow tips",
      tags=["shadow stick", "gnomon", "sun compass", "find north", "survival", "shadow tip", "pebbles"])
def _(S):
    return [dot(5, 12, 2.25),
            line(seg(7.5, 11, 17, 6.5)), line(seg(7.5, 13, 17, 17.5)),
            dot(19, 5.5, 2), dot(19, 18.5, 2),
            line("M19 8.5Q21.5 12 19 15.5")]


@icon("distance-sign", CAT, "Road sign on two posts with two lines of text ending in distances",
      tags=["distance sign", "mileage sign", "road sign", "signpost", "kilometres", "miles to", "direction sign"])
def _(S):
    return [shell(rect(2, 2, 20, 13, S.R * 0.5)),
            detail(seg(5, 6.5, 12, 6.5)), detail(seg(16, 6.5, 19, 6.5)),
            detail(seg(5, 10.5, 12, 10.5)), detail(seg(16, 10.5, 19, 10.5)),
            line(seg(7, 15, 7, 21)), line(seg(17, 15, 17, 21))]


def _runways():
    a = rot(rect(9, 2, 6, 20, 0), -25)
    b = rot(rect(9, 2, 6, 20, 0), 55)
    return a, b


@icon("geoid", CAT, "Lumpy uneven globe inside a dashed smooth ellipse",
      tags=["geoid", "earth shape", "gravity model", "ellipsoid", "geodesy", "datum", "sea level"])
def _(S):
    n = 10
    pts = []
    for i in range(n):
        th = 2 * math.pi * i / n
        r = 5.6 + 0.9 * math.sin(3 * th + 0.4) + 0.5 * math.sin(2 * th + 1)
        pts.append((12 + r * math.cos(th), 12 + r * math.sin(th)))
    return [shell(smooth(pts))] + [line(d) for d in dashed_ellipse(12, 12, 10, 9, 8, 0.55)]


@icon("enclave", CAT, "Small territory completely surrounded by a larger one",
      tags=["enclave", "exclave", "territory", "border", "surrounded country", "region", "boundary"])
def _(S):
    big = [(3, 6), (9, 3), (16, 4), (21, 8), (20, 16), (14, 21), (7, 20), (3, 14)]
    return [shell(poly(big, closed=True, r=S.r)),
            detail(poly([(9, 10), (14, 9), (16, 13), (11, 15.5)], closed=True, r=S.r * 0.5))]


def _spire(x, top, base, hw=2.4):
    m = top + (base - top) * 0.5
    return [(x, top), (x + hw * 0.65, m), (x + hw * 0.3, m), (x + hw, base), (x - hw, base), (x - hw * 0.3, m), (x - hw * 0.65, m)]


@icon("taiga", CAT, "Rows of tall narrow conifers on snowy ground",
      tags=["taiga", "boreal forest", "conifers", "snow forest", "spruce", "pine forest", "biome"])
def _(S):
    return [shell(poly(_spire(4.5, 7, 19), closed=True, r=S.r * 0.4)),
            shell(poly(_spire(12, 3, 19), closed=True, r=S.r * 0.4)),
            shell(poly(_spire(19.5, 8, 19), closed=True, r=S.r * 0.4)),
            line(seg(2, 21.5, 22, 21.5))]


@icon("braided-river", CAT, "River splitting into many interwoven channels around sandbars",
      tags=["braided river", "river channels", "sandbar", "delta", "watercourse", "gravel bar", "floodplain"])
def _(S):
    out = []
    for ph in (0, 120, 240):
        pts = [(2 + 20 * i / 6, 12 + 4 * math.sin(math.radians(ph + 360 * i / 6 * 1.0))) for i in range(7)]
        out.append(line(smooth(pts, closed=False)))
    return out


@icon("shortcut-route", CAT, "Long curved road with a dashed straight line cutting across it",
      tags=["shortcut", "short cut", "direct route", "quick route", "cut through", "bypass", "faster way"])
def _(S):
    return [line("M4 19C20 20 20 13 20 5"),
            line(seg(6.5, 17, 9, 14.8)), line(seg(11, 13, 13, 11.2)), line(seg(15, 9.3, 17.3, 7.2)),
            dot(4, 19, 2), dot(20, 5, 2)]


@icon("hub-and-spoke-routes", CAT, "Central dot with straight routes reaching out to outer dots",
      tags=["hub and spoke", "hub", "network map", "routes", "distribution", "airline hub", "star network"])
def _(S):
    out = [dot(12, 12, 2.5)]
    for k in range(5):
        a = -90 + 72 * k
        ox, oy = 12 + 9 * math.cos(math.radians(a)), 12 + 9 * math.sin(math.radians(a))
        x0, y0 = 12 + 3.5 * math.cos(math.radians(a)), 12 + 3.5 * math.sin(math.radians(a))
        x1, y1 = 12 + 7.3 * math.cos(math.radians(a)), 12 + 7.3 * math.sin(math.radians(a))
        out += [line(seg(x0, y0, x1, y1)), dot(ox, oy, 1.75)]
    return out


@icon("railroad-track", CAT, "Top view of two rails on crossties running into the distance",
      tags=["railroad", "railway", "train track", "rails", "crossties", "sleepers", "tracks"])
def _(S):
    return [line(seg(7, 22, 10.5, 2)), line(seg(17, 22, 13.5, 2)),
            line(seg(4.5, 19, 19.5, 19)), line(seg(5.6, 14, 18.4, 14)),
            line(seg(7.6, 9.5, 16.4, 9.5)), line(seg(9, 5.5, 15, 5.5))]


@icon("rope-bridge", CAT, "Sagging plank bridge with rope handrails between two cliffs",
      tags=["rope bridge", "suspension bridge", "hanging bridge", "gorge", "canyon crossing", "adventure", "trail"])
def _(S):
    return [shell(rect(2, 11, 4, 10, L(S, 0, 1.5))), shell(rect(18, 11, 4, 10, L(S, 0, 1.5))),
            line("M6 15Q12 19 18 15"), line("M4 8Q12 12 20 8"),
            line(seg(4, 8, 4, 11)), line(seg(20, 8, 20, 11)),
            line(seg(8.5, 9.6, 8.5, 16.6)), line(seg(15.5, 9.6, 15.5, 16.6))]


# ============================================================================ chunk 3

def _blob(cx, cy, r, amp, seed, n=8, angular=False):
    pts = []
    for i in range(n):
        th = 2 * math.pi * i / n
        rr = r + amp * math.sin(3 * th + seed) + amp * 0.6 * math.sin(2 * th + seed * 2)
        pts.append((cx + rr * math.cos(th), cy + rr * math.sin(th)))
    return poly(pts, closed=True) if angular else smooth(pts)


def dashed_bez(p0, c1, c2, p3, n=4, frac=0.6, pts=4):
    out = []
    def at(t):
        u = 1 - t
        return (u ** 3 * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t ** 3 * p3[0],
                u ** 3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t ** 3 * p3[1])
    for k in range(n):
        t0 = k / n
        t1 = t0 + frac / n
        out.append(poly([at(t0 + (t1 - t0) * i / (pts - 1)) for i in range(pts)]))
    return out


@icon("globe-polar-view", CAT, "Globe seen from above the pole with land around an ice cap",
      tags=["polar view", "north pole", "arctic", "globe", "top down globe", "ice cap", "polar projection"])
def _(S):
    out = [shell(circle(12, 12, 9.5)), mark(circle(12, 12, 1.75))]
    for k, (a, rr, sz) in enumerate(((5, 6.2, 1.7), (95, 6.0, 2.2), (185, 6.3, 1.5), (275, 5.9, 2.0))):
        x, y = pt_on_(12, 12, rr, a)
        out.append(mark(_blob(x, y, sz, 0.4, k + 1, angular=(S.name == 'line'))))
    return out


@icon("burial-mound", CAT, "Low grassy earth mound with a small stone entrance at its base",
      tags=["burial mound", "barrow", "tumulus", "passage grave", "ancient tomb", "earthwork", "neolithic"])
def _(S):
    return [shell("M2 20A10 13 0 0 1 22 20Z"),
            detail("M9.5 20V15.5H14.5V20")]


@icon("hill-fort", CAT, "Plan of a hilltop ringed by concentric earthwork ditches and banks",
      tags=["hill fort", "hillfort", "earthwork", "rampart", "iron age", "ditch and bank", "ringfort"])
def _(S):
    return [shell(_blob(12, 12, 9.4, 0.6, 1.3, n=10, angular=S.name == 'line')),
            detail(_blob(12, 12, 5.4, 0.4, 2.1, n=8, angular=S.name == 'line')),
            mark(circle(12, 12, 1.75))]


@icon("dead-reckoning", CAT, "Course line with time ticks from a start dot to an estimated position marker",
      tags=["dead reckoning", "navigation", "estimated position", "course line", "plotting", "chart work", "ded reckoning"])
def _(S):
    x0, y0, x1, y1 = 4.5, 19.5, 16, 8
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux
    out = [dot(x0, y0, 2), line(seg(x0 + ux * 2.5, y0 + uy * 2.5, x1, y1))]
    for f in (0.36, 0.64):
        cx, cy = x0 + dx * f, y0 + dy * f
        out.append(line(seg(cx - nx * 2.5, cy - ny * 2.5, cx + nx * 2.5, cy + ny * 2.5)))
    ang = math.atan2(uy, ux)
    tip = (x1 + ux * 5.5, y1 + uy * 5.5)
    pts = [(tip[0] + ux * 2.0, tip[1] + uy * 2.0),
           (tip[0] - ux * 2.2 + nx * 2.6, tip[1] - uy * 2.2 + ny * 2.6),
           (tip[0] - ux * 2.2 - nx * 2.6, tip[1] - uy * 2.2 - ny * 2.6)]
    out.append(shell(poly(pts, closed=True, r=S.r * 0.4)))
    return out


@icon("search-pattern", CAT, "Square spiral path growing outward from a centre dot, as in a rescue search",
      tags=["search pattern", "expanding square", "search and rescue", "sar", "spiral search", "grid search", "coverage"])
def _(S):
    return [line(poly([(12, 12), (16, 12), (16, 16), (8, 16), (8, 8), (20, 8), (20, 20), (4, 20)], r=S.r)),
            dot(12, 12, 2)]


@icon("south-pole-marker", CAT, "Short striped ceremonial pole topped with a mirrored ball on flat snow",
      tags=["south pole", "ceremonial pole", "antarctica", "pole marker", "polar", "mirror ball", "expedition"])
def _(S):
    return [shell(circle(12, 5.5, 3.5)),
            shell(rect(10, 10, 4, 10, L(S, 0, 1))),
            detail(seg(10, 13, 14, 13)), detail(seg(10, 17, 14, 17)),
            line(seg(2, 21.5, 22, 21.5))]


@icon("tissot-indicatrix", CAT, "World grid frame with circles stretching into wider ellipses toward top and bottom",
      tags=["tissot", "indicatrix", "map distortion", "projection", "cartography", "map projection", "distortion ellipses"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R * 0.5)),
            detail(seg(12, 3, 12, 21)),
            mark(ellipse(7, 7.5, 2.75, 1.5)), mark(ellipse(17, 7.5, 2.75, 1.5)),
            mark(circle(7, 12, 1.5)), mark(circle(17, 12, 1.5)),
            mark(ellipse(7, 16.5, 2.75, 1.5)), mark(ellipse(17, 16.5, 2.75, 1.5))]


def _sine(x0, x1, n=4):
    return [(x, 12 - 4.5 * math.sin((x - 3) / 18 * 2 * math.pi)) for x in [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]]


@icon("satellite-ground-track", CAT, "Wavy track crossing a flat world map frame with a satellite on it",
      tags=["ground track", "satellite path", "orbit", "sine wave", "map", "orbital track", "tracking"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R * 0.5)),
            detail(smooth(_sine(10.2, 21, 7), closed=False)),
            mark(poly([(7.5, 4.6), (10, 7.5), (7.5, 10.4), (5, 7.5)], closed=True))]


@icon("migration-route", CAT, "Three small birds flying along a long curved dashed arrow",
      tags=["migration", "migration route", "bird migration", "flyway", "seasonal movement", "birds flying", "journey"])
def _(S):
    def bird(x, y):
        return line(f"M{fmt(x - 3.4)} {fmt(y + 1.4)}Q{fmt(x - 1.7)} {fmt(y - 2.6)} {fmt(x)} {fmt(y + 0.8)}"
                    f"Q{fmt(x + 1.7)} {fmt(y - 2.6)} {fmt(x + 3.4)} {fmt(y + 1.4)}")
    dashes = dashed_bez((3, 21), (10, 21), (14, 17), (19, 12), 4, 0.55)
    return [bird(5, 7), bird(11.5, 4), bird(18, 5.5), *[line(d) for d in dashes],
            line(poly([(15.5, 11.5), (19.5, 11), (19, 15)], r=S.r))]


# ============================================================================ chunk 4

@icon("protected-area", CAT, "Region outline enclosing small conifers, marking a protected nature reserve",
      tags=["protected area", "nature reserve", "national park", "conservation", "wildlife reserve", "forest reserve", "preserve"])
def _(S):
    big = [(3, 7), (9, 3), (16, 4), (21, 9), (20, 16), (14, 21), (7, 20), (3, 14)]
    return [shell(poly(big, closed=True, r=S.r * 2.2)),
            mark(poly([(7.5, 15), (10, 8.5), (12.5, 15)], closed=True)),
            mark(poly([(12.5, 17), (15.5, 10), (18.5, 17)], closed=True))]


@icon("plane-table", CAT, "Drawing board on a tripod with a sighting ruler lying on top",
      tags=["plane table", "plane tabling", "surveying", "alidade", "survey board", "tripod", "mapping field"])
def _(S):
    return [shell(rect(2, 9, 20, 3, L(S, 0, 1.5))),
            line(seg(5, 7, 19, 7)), line(seg(5, 7, 5, 3.5)), line(seg(19, 7, 19, 3.5)),
            line(seg(8, 12, 5, 21)), line(seg(12, 12, 12, 21)), line(seg(16, 12, 19, 21))]


@icon("chip-log", CAT, "Quarter circle wooden float on a knotted line wound on a hand reel",
      tags=["chip log", "ship log", "speed log", "knots", "nautical", "sailing instrument", "log line"])
def _(S):
    return [shell("M3 3V12A9 9 0 0 0 12 3Z"),
            line(seg(9, 9, 15, 15)), dot(11.5, 11.5, 1.25),
            shell(circle(18, 18, 4)), dot(18, 18, 1.25)]


@icon("mapping-car", CAT, "Car with a tall mast on its roof topped by a round camera ball",
      tags=["mapping car", "street view", "survey vehicle", "camera car", "lidar car", "road imaging", "360 camera"])
def _(S):
    return [shell(poly([(2, 18), (2, 14), (6, 14), (8.5, 10.5), (16, 10.5), (19, 14), (22, 14), (22, 18)],
                       closed=True, r=S.r)),
            line(seg(12, 10.5, 12, 6)),
            shell(circle(12, 4, 2.25)),
            mark(circle(7, 18.5, 2.25)), mark(circle(17, 18.5, 2.25))]


@icon("dashboard-compass", CAT, "Ball compass in a clear dome on a small angled dashboard mount",
      tags=["dashboard compass", "car compass", "ball compass", "vehicle compass", "dome compass", "marine compass", "heading"])
def _(S):
    needle = rot("M12 4.5L13.2 9L12 13.5L10.8 9Z", 30, 12, 9)
    return [shell(circle(12, 9, 6)),
            mark(needle),
            shell(poly([(5, 21), (19, 21), (17, 16.5), (7, 16.5)], closed=True, r=S.r * 0.5))]


@icon("dot-density-map", CAT, "Region outline filled with scattered dots, crowded in one part and sparse in another",
      tags=["dot density map", "dot map", "population map", "distribution map", "thematic map", "density", "choropleth alternative"])
def _(S):
    big = [(3, 7), (9, 3), (16, 4), (21, 9), (20, 16), (14, 21), (7, 20), (3, 14)]
    dots = [(7, 9), (10.5, 7.5), (7, 13), (10.5, 12), (8, 16.5), (11.5, 16.5), (17, 10), (15.5, 15.5)]
    return [shell(poly(big, closed=True, r=S.r * 2.2)), *[mark(circle(x, y, 1.1)) for x, y in dots]]


@icon("bubble-map", CAT, "Map frame with circles of clearly different sizes over its regions",
      tags=["bubble map", "proportional symbol map", "symbol map", "thematic map", "data map", "sized circles", "cartography"])
def _(S):
    return [shell(rect(2, 3, 20, 18, S.R)),
            mark(circle(9, 11, 3.75)), mark(circle(17, 7.5, 2.25)), mark(circle(16.5, 16, 1.5))]


@icon("hexbin-map", CAT, "Map built from hexagon tiles, some filled and some empty",
      tags=["hexbin map", "hex map", "tile grid map", "hexagon map", "cartogram", "honeycomb", "binned map"])
def _(S):
    def hexd(cx, cy, r):
        return poly([(cx + r * math.cos(math.radians(60 * i - 30)), cy + r * math.sin(math.radians(60 * i - 30))) for i in range(6)], closed=True, r=S.r * 0.5)
    return [solid(hexd(7.5, 7, 4.2)), line(hexd(16.5, 7, 3.3)),
            line(hexd(7.5, 16, 3.3)), solid(hexd(16.5, 16, 4.2))]


@icon("strip-map", CAT, "Tall narrow route map with a road down the middle and landmarks at its sides",
      tags=["strip map", "route strip", "linear map", "road map", "itinerary map", "trail guide", "landmarks"])
def _(S):
    return [shell(rect(5, 2, 14, 20, S.R * 0.5)),
            detail("M12 2C8.5 8 15.5 15 12 22"),
            mark(rect(6.5, 6, 2, 2.5)), mark(rect(15.5, 10.5, 2, 2.5)), mark(rect(6.5, 15, 2, 2.5))]


@icon("territorial-waters", CAT, "Coastline with a dashed boundary running parallel to it out at sea",
      tags=["territorial waters", "maritime boundary", "exclusive economic zone", "eez", "sea border", "offshore limit", "coastal waters"])
def _(S):
    A = ((2, 9), (6, 6), (9, 13), (13, 12))
    B = ((13, 12), (17, 11), (19, 6), (22, 8))
    def sh(c):
        return tuple((x, y + 6.5) for x, y in c)
    dashes = dashed_bez(*sh(A), 3, 0.6) + dashed_bez(*sh(B), 3, 0.6)
    return [shell("M2 3H22V8C19 6 17 11 13 12C9 13 6 6 2 9Z"),
            *[line(d) for d in dashes]]


@icon("earth-curvature", CAT, "Curved horizon with ship sails showing above it and the hull hidden below",
      tags=["earth curvature", "curvature of the earth", "round earth", "horizon", "hull down", "ship over horizon", "flat earth debate"])
def _(S):
    return [line("M3 19Q12 10 21 19"),
            shell(poly([(11, 6), (11, 12), (6.5, 12)], closed=True, r=S.r * 0.4)),
            shell(poly([(13, 5), (13, 12), (17.5, 12)], closed=True, r=S.r * 0.4)),
            line(seg(12, 4.5, 12, 14.5))]


@icon("dirt-track", CAT, "Two wheel ruts with a grass strip between them curving into the distance",
      tags=["dirt track", "dirt road", "farm track", "rutted road", "country lane", "unpaved road", "trail"])
def _(S):
    return [line("M4 22C5 15 12 13 8.5 2"), line("M20 22C19 15 18 13 14.5 2"),
            line(poly([(10.5, 20), (12, 16.5), (13.5, 20)], r=S.r * 0.5)),
            line(poly([(11, 10), (12.3, 7), (13.6, 10)], r=S.r * 0.5))]


@icon("tree-lined-avenue", CAT, "Straight road running into the distance between rows of round trees",
      tags=["tree lined avenue", "boulevard", "tree lined road", "alley of trees", "promenade", "avenue", "allee"])
def _(S):
    return [line(seg(9.5, 22, 10.8, 4)), line(seg(14.5, 22, 13.2, 4)),
            shell(circle(4, 16.5, 2.75)), shell(circle(5.5, 8.5, 1.75)),
            shell(circle(20, 16.5, 2.75)), shell(circle(18.5, 8.5, 1.75))]


@icon("orientation-table", CAT, "Round engraved table on a stone pedestal with lines pointing to surrounding peaks",
      tags=["orientation table", "viewpoint indicator", "panorama table", "lookout", "summit table", "peak finder", "scenic viewpoint"])
def _(S):
    return [line(poly([(2, 7.5), (6, 3.5), (9.5, 6.5), (13, 3.5), (16.5, 6), (19, 4), (22, 7.5)], r=S.r)),
            shell(ellipse(12, 13.5, 9, 3.5)),
            detail(seg(12, 11.5, 12, 15.5)),
            shell(poly([(9.5, 17), (14.5, 17), (16, 21), (8, 21)], closed=True, r=S.r * 0.4))]


@icon("walled-city", CAT, "Cluster of rooftops enclosed by fortified walls with round towers",
      tags=["walled city", "fortified city", "city walls", "medieval town", "citadel", "old town", "fortress city"])
def _(S):
    return [shell(rect(2, 11, 4, 10, L(S, 0, 2))), shell(rect(18, 11, 4, 10, L(S, 0, 2))),
            line(poly([(2, 11), (4, 6.5), (6, 11)], r=S.r * 0.4)),
            line(poly([(18, 11), (20, 6.5), (22, 11)], r=S.r * 0.4)),
            shell(rect(6, 15, 12, 6, L(S, 0, 1))),
            shell(poly([(9, 15), (9, 12), (12, 8), (15, 12), (15, 15)], closed=True, r=S.r * 0.4)),
            mark(rect(10.5, 17.5, 3, 3.5))]
