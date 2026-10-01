"""TypeIcon Core: space & astronomy."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar  # noqa: F401

CAT = "space"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def axis(origin, deg):
    """Local frame: x runs along `deg` (0 = right, positive = clockwise on screen)."""
    ox, oy = origin
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return lambda x, y: (ox + x * c - y * s, oy + x * s + y * c)


def pts_d(pts, closed=False):
    d = "".join(("M" if i == 0 else "L") + f"{fmt(x)} {fmt(y)}" for i, (x, y) in enumerate(pts))
    return d + ("Z" if closed else "")


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def outline_region(d, w=2.0):
    return U(P(d), ST(d, w))


def ellipse_pts(cx, cy, rx, ry, tilt, t0, t1, step=3.0):
    """Points along a tilted ellipse, parameter t in degrees (t = 90 is the near/front side)."""
    m = axis((cx, cy), tilt)
    n = max(2, int(abs(t1 - t0) / step))
    return [m(rx * math.cos(math.radians(t0 + (t1 - t0) * i / n)), ry * math.sin(math.radians(t0 + (t1 - t0) * i / n)))
            for i in range(n + 1)]


def circle_pts(cx, cy, r, a0, a1, step=3.0):
    n = max(2, int(abs(a1 - a0) / step))
    return [polar(cx, cy, r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]


def runs(pts, keep):
    """Split a point list into the consecutive runs whose points satisfy keep()."""
    out, cur = [], []
    for p in pts:
        if keep(p):
            cur.append(p)
        else:
            if len(cur) > 1:
                out.append(cur)
            cur = []
    if len(cur) > 1:
        out.append(cur)
    return out


def dist_to(p, pts):
    return min(math.hypot(p[0] - q[0], p[1] - q[1]) for q in pts)


# ============================================================================ planets and orbits

def _ringed(cx, cy, r, rx, ry, tilt, gap=3.0, back_gap=3.0):
    """Planet outline runs and ring runs for a planet circled by a tilted ring passing in front."""
    front = ellipse_pts(cx, cy, rx, ry, tilt, 0, 180, 2)
    ring = ellipse_pts(cx, cy, rx, ry, tilt, -90, 270, 2)
    ring_runs = runs(ring, lambda p: math.hypot(p[0] - cx, p[1] - cy) > r + back_gap or dist_to(p, front) < 0.01)
    planet_runs = runs(circle_pts(cx, cy, r, -90, 270, 2), lambda p: dist_to(p, front) > gap)
    return planet_runs, ring_runs, front


def _ringed_filled(cx, cy, r, rx, ry, tilt, extra=()):
    def f():
        planet_runs, ring_runs, front = _ringed(cx, cy, r, rx, ry, tilt)
        body = D(P(circle(cx, cy, r + 1)), ST(pts_d(front), 2.5 + 3))
        return U(body, *[ST(pts_d(rn), 2.5) for rn in ring_runs], *[f() for f in extra])
    return f


@icon("planet-ring", CAT, "Planet circled by a tilted ring, like Saturn",
      tags=["saturn", "planet", "ringed planet", "astronomy", "solar system", "space"], aliases=["saturn", "ringed-planet"],
      filled=_ringed_filled(12, 12, 6.5, 9.5, 2.75, -20))
def _(S):
    planet_runs, ring_runs, _ = _ringed(12, 12, 6.5, 9.5, 2.75, -20)
    return [*[line(pts_d(rn)) for rn in planet_runs], *[line(pts_d(rn)) for rn in ring_runs]]


def _satellite(cx, cy, deg, S):
    """Small satellite: a round body between two solid solar panels running along `deg`."""
    m = axis((cx, cy), deg)
    p1 = [m(3, -1.75), m(6.5, -1.75), m(6.5, 1.75), m(3, 1.75)]
    p2 = [m(-6.5, -1.75), m(-3, -1.75), m(-3, 1.75), m(-6.5, 1.75)]
    return [shell(circle(cx, cy, 1.5)), solid(poly(p1, closed=True)), solid(poly(p2, closed=True))]


@icon("satellite-orbit", CAT, "Satellite travelling on an orbit around a planet",
      tags=["orbit", "satellite", "space", "gps", "earth", "spacecraft"], aliases=["orbiting-satellite"])
def _(S):
    return [
        shell(circle(7, 17, 4)),
        line(arc(7, 17, 8, -110, 20)),
        *_satellite(15.5, 8.5, 45, S),
    ]


@icon("ufo", CAT, "Flying saucer with a domed cockpit and lights",
      tags=["alien", "flying saucer", "spaceship", "extraterrestrial", "sci-fi", "space"], aliases=["flying-saucer"])
def _(S):
    saucer = L(S, "M3 14C5 11.5 8.5 10.5 12 10.5C15.5 10.5 19 11.5 21 14C19 16.5 15.5 17.5 12 17.5C8.5 17.5 5 16.5 3 14Z",
               ellipse(12, 14, 9, 3.5))
    dome = "M7 11.5A5 5 0 0 1 17 11.5Z"
    return [
        shell(union(saucer, dome)),
        dot(8, 14, 1.1), dot(12, 14.5, 1.1), dot(16, 14, 1.1),
        line(seg(8.5, 19.5, 7, 21.5)), line(seg(15.5, 19.5, 17, 21.5)),
    ]


def _star_pts(cx, cy, ro, ri, start=-90):
    return [polar(cx, cy, ro if i % 2 == 0 else ri, start + i * 36) for i in range(10)]


@icon("shooting-star", CAT, "Star streaking across the sky with a trail",
      tags=["falling star", "meteor", "wish", "night sky", "comet", "space"], aliases=["falling-star"])
def _(S):
    return [
        shell(poly(_star_pts(15, 9, 6, 2.7), closed=True, r=S.r * 0.4)),
        line(seg(9.5, 14.5, 3, 21)),
        line(seg(7.5, 11, 3.5, 15)),
        line(seg(12.5, 17.5, 9.5, 20.5)),
    ]


def _spiral(cx, cy, r0, r1, turns, start):
    n = 60
    out = []
    for i in range(n + 1):
        t = i / n
        a = start + 360 * turns * t
        out.append(polar(cx, cy, r0 + (r1 - r0) * t, a))
    return out


def _flat(pts, cx, cy, k, tilt):
    m = axis((cx, cy), tilt)
    return [m(x - cx, (y - cy) * k) for x, y in pts]


@icon("galaxy", CAT, "Spiral galaxy seen at an angle, with a bright core",
      tags=["milky way", "spiral", "cosmos", "universe", "stars", "astronomy"], aliases=["milky-way"])
def _(S):
    arms = [line(pts_d(_flat(_spiral(12, 12, 3.5, 10, 0.55, a), 12, 12, 0.62, -30))) for a in (-10, 170)]
    core = pts_d(_flat([polar(12, 12, 2.4, a) for a in range(0, 360, 10)], 12, 12, 0.7, -30), closed=True)
    return [*arms, Part("dot", core), dot(4.5, 4.5, 1.1), dot(19.5, 19, L(S, 1.1, 1.2))]


_MP = ((6.75, 6.75), (17.25, 6.75), (6.75, 17.25), (17.25, 17.25))
_MR = 3.25


def _lit(i):
    cx, cy = _MP[i]
    disc = circle(cx, cy, _MR)
    if i == 1:
        return minus(disc, circle(cx - 2.75, cy, _MR))
    if i == 2:
        return path_to_d(I(P(disc), P(rect(cx, cy - 5, 5, 10))))
    if i == 3:
        return disc
    return None


@icon("moon-phases", CAT, "Four phases of the moon: new, crescent, half and full",
      tags=["lunar cycle", "moon", "phases", "crescent", "full moon", "astronomy"], aliases=["lunar-phases"])
def _(S):
    x, y = _MP[0]
    new = [line(arc(x, y, _MR, a, a + 24)) for a in range(-102, 258, 45)]
    out = new + [line(circle(x, y, _MR)) for x, y in _MP[1:]]
    for i in (1, 2, 3):
        out.append(solid(_lit(i)))
    return out


def _rays(cx, cy, r0, r1, n=8, start=0):
    return [seg(*polar(cx, cy, r0, a), *polar(cx, cy, r1, a)) for a in [start + k * 360 / n for k in range(n)]]


def _eclipse_filled():
    body = D(P(circle(12, 12, 6)), P(circle(13.25, 10.75, 5)))
    return U(body, *[ST(d, 2.5) for d in _rays(12, 12, 7.75, 10)])


@icon("solar-eclipse", CAT, "The moon covering the sun, leaving a thin bright crescent",
      tags=["eclipse", "sun", "moon", "totality", "astronomy", "corona"], aliases=["eclipse"], filled=_eclipse_filled)
def _(S):
    return [shell(circle(12, 12, 5)), solid(circle(13.25, 10.75, 4.25)), *[line(d) for d in _rays(12, 12, 7.5, 9.75)]]


@icon("black-hole", CAT, "Black hole: a dark core with matter swirling into it",
      tags=["singularity", "event horizon", "gravity", "vortex", "accretion", "astronomy"])
def _(S):
    arms = [line(pts_d(_spiral(12, 12, 9.5, 4, -0.5, a))) for a in (-90, 30, 150)]
    return [*arms, dot(12, 12, 2.5)]


@icon("space-station", CAT, "Space station: a truss with solar panels and a central module",
      tags=["iss", "orbital station", "spacecraft", "orbit", "astronaut", "space"], aliases=["iss"])
def _(S):
    rr = L(S, 0, min(S.R, 1))
    out = [line(seg(3, 12, 9.5, 12)), line(seg(14.5, 12, 21, 12))]
    for x in (3, 16.5):
        out += [shell(rect(x, 3.5, 4.5, 5.5, rr)), shell(rect(x, 15, 4.5, 5.5, rr)), line(seg(x + 2.25, 9, x + 2.25, 15))]
    out += [shell(rect(9.5, 8.5, 5, 7, min(S.R, 1.5)))]
    return out


@icon("astronaut-helmet", CAT, "Astronaut's space helmet with a large visor",
      tags=["astronaut", "spacesuit", "cosmonaut", "helmet", "space", "visor"], aliases=["space-helmet"])
def _(S):
    outer = union(circle(12, 10.5, 8), rect(6, 16, 12, 5, L(S, 0.5, 2)))
    visor = L(S, "M6.5 11C6.5 7.8 9 6 12 6C15 6 17.5 7.8 17.5 11C17.5 13.2 15.5 14.5 12 14.5C8.5 14.5 6.5 13.2 6.5 11Z",
              ellipse(12, 10.25, 5.5, 4.25))
    return [shell(outer), detail(visor), detail("M9 10A3 3 0 0 1 11.5 8"), detail(seg(6, 18, 18, 18))]


_CON = [(4.5, 18.5), (7.5, 10.5), (13, 13), (16, 5), (19.25, 10)]
_CON_E = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 2)]


@icon("constellation", CAT, "Stars joined by lines into a constellation",
      tags=["stars", "star map", "zodiac", "astronomy", "night sky", "asterism"], aliases=["star-map"])
def _(S):
    out = [shell(circle(x, y, 1.75)) for x, y in _CON]
    for a, b in _CON_E:
        (x0, y0), (x1, y1) = _CON[a], _CON[b]
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy)
        ux, uy = dx / ln, dy / ln
        out.append(line(seg(x0 + ux * 3.75, y0 + uy * 3.75, x1 - ux * 3.75, y1 - uy * 3.75)))
    return out


@icon("observatory", CAT, "Domed observatory with a telescope pointing out",
      tags=["telescope", "astronomy", "dome", "stargazing", "planetarium", "science"])
def _(S):
    m = axis((12, 12.5), -50)
    tube = [m(3, -1.5), m(10, -1.5), m(10, 1.5), m(3, 1.5)]
    cut = poly([m(1.5, -3.5), m(12, -3.5), m(12, 3.5), m(1.5, 3.5)], closed=True)
    building = minus(union("M5 13A7 7 0 0 1 19 13Z", rect(3.5, 13, 17, 8, 0)), cut)
    return [
        shell(building),
        shell(poly(tube, closed=True, r=S.r * 0.4)),
        detail(poly([(10, 21), (10, 17.5), (14, 17.5), (14, 21)], r=S.r * 0.5)),
    ]


@icon("lunar-rover", CAT, "Lunar rover with big wheels and an antenna dish",
      tags=["moon buggy", "rover", "moon", "exploration", "vehicle", "space"], aliases=["moon-buggy"])
def _(S):
    return [
        line(seg(3, 11, 21, 11)),
        line(seg(6.5, 11, 6.5, 13.5)), line(seg(17.5, 11, 17.5, 13.5)),
        shell(circle(6.5, 17.5, 3.25)), shell(circle(17.5, 17.5, 3.25)),
        dot(6.5, 17.5, 1.1), dot(17.5, 17.5, 1.1),
        shell(rect(4.5, 6.5, 5, 4.5, min(S.R, 1))),
        line(seg(16, 11, 16, 7)),
        shell(L(S, "M12 7A4 4 0 0 1 20 7Z", "M12.5 7A3.5 3.5 0 0 1 19.5 7A0.5 0.5 0 0 1 19 7.5H13A0.5 0.5 0 0 1 12.5 7Z")),
    ]
