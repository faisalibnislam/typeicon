"""TypeIcon Core: landscape (batch landscape_004).

Weather oddities, planets and moons, eclipses, stars, deep-sky objects, star patterns, sky instruments and
spacecraft, drawn from the objects themselves on the 24 px grid.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar, transform_path  # noqa: F401

CAT = "landscape"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def inter(a, b):
    return path_to_d(I(P(a), P(b)))


def grow(d, g):
    """Region d expanded by g px (to cut clean gaps between parts)."""
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def soften(d, k):
    """Round the convex corners of closed region d with radius k (erode then dilate)."""
    p = P(d)
    inset = D(p, ST(d, 2 * k, "round", "round"))
    back = U(inset, ST(path_to_d(inset), 2 * k, "round", "round"))
    return path_to_d(back)


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def pit(S, x, y, r):
    """Small crater or grain: a square in Line, a disc in Rounded."""
    if S.name == "line":
        return Part("dot", rect(x - r, y - r, 2 * r, 2 * r))
    return dot(x, y, r)


def pts_d(pts, closed=False):
    d = "".join(("M" if i == 0 else "L") + f"{fmt(x)} {fmt(y)}" for i, (x, y) in enumerate(pts))
    return d + ("Z" if closed else "")


def axis(origin, deg):
    """Local frame: x runs along `deg` (0 = right, positive = clockwise on screen)."""
    ox, oy = origin
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return lambda x, y: (ox + x * c - y * s, oy + x * s + y * c)


def ell_pts(cx, cy, rx, ry, tilt, t0, t1, step=6.0):
    """Points along a tilted ellipse, parameter t in degrees."""
    m = axis((cx, cy), tilt)
    n = max(2, int(abs(t1 - t0) / step))
    return [m(rx * math.cos(math.radians(t0 + (t1 - t0) * i / n)), ry * math.sin(math.radians(t0 + (t1 - t0) * i / n)))
            for i in range(n + 1)]


def tilted_ellipse(cx, cy, rx, ry, tilt):
    return pts_d(ell_pts(cx, cy, rx, ry, tilt, 0, 360, 6)[:-1], closed=True)


def arc_pts(cx, cy, r, a0, a1, step=5.0):
    n = max(2, int(abs(a1 - a0) / step))
    return [polar(cx, cy, r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]


def runs(pts, keep):
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


def clear_of(pts, circles):
    """Runs of a polyline that stay clear of the given (cx, cy, r) circles."""
    return runs(pts, lambda p: all(math.hypot(p[0] - c[0], p[1] - c[1]) > c[2] for c in circles))


def spark(cx, cy, ro, ri=None, S=None, rot=0.0):
    """Four-point sparkle star."""
    ri = ro * 0.36 if ri is None else ri
    pts = [polar(cx, cy, ro if i % 2 == 0 else ri, -90 + rot + i * 45) for i in range(8)]
    return poly(pts, closed=True, r=0 if S is None else L(S, 0, 0.5))


def star5(cx, cy, ro, ri=None, S=None):
    ri = ro * 0.45 if ri is None else ri
    pts = [polar(cx, cy, ro if i % 2 == 0 else ri, -90 + i * 36) for i in range(10)]
    return poly(pts, closed=True, r=0 if S is None else L(S, 0, 0.4))


def smooth_closed(pts, k=0.5):
    """Closed Catmull-Rom style smooth path through points (cubic Beziers)."""
    n = len(pts)
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) * k / 3, p1[1] + (p2[1] - p0[1]) * k / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * k / 3, p2[1] - (p3[1] - p1[1]) * k / 3)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d + "Z"


def lumpy(cx, cy, radii, rot=0.0):
    n = len(radii)
    return [polar(cx, cy, r, rot + i * 360 / n) for i, r in enumerate(radii)]


def rock(cx, cy, radii, rot, S):
    """Lumpy rock: angular in Line, smooth in Rounded."""
    pts = lumpy(cx, cy, radii, rot)
    return poly(pts, closed=True) if S.name == "line" else smooth_closed(pts)


def wave_pts(p0, p1, amp, waves, n=30, taper=None):
    """Points of a sine wave running from p0 to p1 (amp in px, `waves` full periods)."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln
    out = []
    for i in range(n + 1):
        t = i / n
        a = amp * (taper(t) if taper else 1.0) * math.sin(2 * math.pi * waves * t)
        out.append((p0[0] + dx * t + nx * a, p0[1] + dy * t + ny * a))
    return out


def lens(cx, cy, rx, ry, tilt, S, rt=None):
    """Lens (two arcs meeting in tips): pointed tips in Line, softened tips in Rounded."""
    m = axis((cx, cy), tilt)
    r = L(S, 0, 1.2) if rt is None else rt
    R = (rx * rx + ry * ry) / (2 * ry)
    a0 = math.degrees(math.asin(rx / R))
    n = 16
    top = []
    for i in range(n + 1):
        a = -a0 + 2 * a0 * i / n
        top.append((R * math.sin(math.radians(a)), -(R * math.cos(math.radians(a)) - (R - ry))))
    bot = [(x, -y) for x, y in top[::-1]]
    pts = top[:-1] + bot[:-1]
    return poly([m(x, y) for x, y in pts], closed=True, r=r)


def arrow_head(tip, deg, size=2.0):
    """Open arrowhead at `tip` pointing along `deg`."""
    a = polar(tip[0], tip[1], size * 1.414, deg + 135)
    b = polar(tip[0], tip[1], size * 1.414, deg - 135)
    return poly([a, tip, b])


def near(p, pts, dist):
    return any(math.hypot(p[0] - q[0], p[1] - q[1]) < dist for q in pts)


def chord_half(cx, cy, r, y):
    return math.sqrt(max(0.0, r * r - (y - cy) ** 2))


def zig(cx, cy, a, r0, r1, amp=1.3):
    """Elbow spark running outward from a centre along angle a: out, kink sideways, out again."""
    p0 = polar(cx, cy, r0, a)
    p2 = polar(cx, cy, r1, a)
    nx, ny = -math.sin(math.radians(a)), math.cos(math.radians(a))
    m = (p0[0] + (p2[0] - p0[0]) * 0.5 + nx * amp, p0[1] + (p2[1] - p0[1]) * 0.5 + ny * amp)
    return [p0, m, p2]


def heart_d(cx, cy, w, h):
    t = cy - h / 2
    b = cy + h / 2
    return (f"M{fmt(cx)} {fmt(b)}C{fmt(cx - w * 0.6)} {fmt(cy + h * 0.1)} {fmt(cx - w * 0.6)} {fmt(t)} {fmt(cx - w * 0.27)} {fmt(t)}"
            f"C{fmt(cx - w * 0.1)} {fmt(t)} {fmt(cx)} {fmt(t + h * 0.15)} {fmt(cx)} {fmt(t + h * 0.3)}"
            f"C{fmt(cx)} {fmt(t + h * 0.15)} {fmt(cx + w * 0.1)} {fmt(t)} {fmt(cx + w * 0.27)} {fmt(t)}"
            f"C{fmt(cx + w * 0.6)} {fmt(t)} {fmt(cx + w * 0.6)} {fmt(cy + h * 0.1)} {fmt(cx)} {fmt(b)}Z")


def heart_sharp(cx, cy, w):
    """Geometric heart: a square turned on its corner with two round lobes (straight sides, sharp tip)."""
    d = w / 2.414
    yc = cy - 1.207 * d + d * 0.0
    yc = cy + (d - 1.207 * d) / 2  # centre the heart vertically
    sq = poly([(cx, yc + d), (cx - d, yc), (cx, yc - d), (cx + d, yc)], closed=True)
    rr = d / math.sqrt(2)
    return union(sq, circle(cx - d / 2, yc - d / 2, rr), circle(cx + d / 2, yc - d / 2, rr))


def tband(cx, cy, r, d, deg, inset=0.0):
    """Line across a disc along direction `deg`, offset d from the centre, stopping short of the rim by `inset`."""
    a = math.radians(deg)
    hw = math.sqrt(max(0.0, r * r - d * d)) - inset
    nx, ny = -math.sin(a), math.cos(a)
    ox, oy = cx + nx * d, cy + ny * d
    return seg(ox - math.cos(a) * hw, oy - math.sin(a) * hw, ox + math.cos(a) * hw, oy + math.sin(a) * hw)


def band(cx, cy, r, y, inset=0.0):
    """Horizontal line across a disc at height y, stopping short of the rim by `inset`."""
    hw = chord_half(cx, cy, r, y) - inset
    return seg(cx - hw, y, cx + hw, y)


# ============================================================================ weather and sky oddities

@icon("sandstorm", CAT, "Wall of billowing dust over a dune with grains of sand flying",
      tags=["dust storm", "haboob", "sand blowing", "desert wind", "weather", "dune"],
      aliases=["dust-storm"])
def _(S):
    wall = union(rect(4, 9, 16, 5.5, L(S, 0, 2.5)), circle(8, 9.5, 3.5), circle(13.5, 8, 4.8), circle(18.25, 10.75, 3.25))
    return [
        shell(wall),
        detail("M8 11.5H16"),
        line("M2 21C6 18.5 10 18.5 13 20.5C15.5 19 19 19 22 21"),
    ]


@icon("waterspout", CAT, "Funnel cloud hanging from a storm cloud down to the choppy sea",
      tags=["tornado over water", "funnel cloud", "sea storm", "twister", "weather", "ocean"])
def _(S):
    slab = rect(3, 5.5, 18, 3.5, 1.75)
    cloud = union(slab, circle(9, 6.2, 2.6), circle(15, 5.8, 2.8))
    funnel = poly([(6.5, 8), (17.5, 8), (12.8, 16.5), (11.2, 16.5)], closed=True, r=S.r * 0.4)
    wave = poly([(2, 21), (5.5, 19), (9, 21), (12.5, 19), (16, 21), (19.5, 19), (22, 21)], r=S.r)
    return [shell(union(cloud, funnel)), line(wave)]


@icon("ball-lightning", CAT, "Glowing ball with two jagged sparks crackling away from it",
      tags=["lightning orb", "electric sphere", "plasma ball", "thunderstorm", "weather", "spark"])
def _(S):
    k = S.r * 0.5
    return [
        shell(circle(11.5, 12.5, 4.5)),
        line(poly([(15, 9.5), (18, 9), (16.5, 5.5), (20.5, 3.5)], r=k)),
        line(poly([(8, 15.5), (5, 16), (6.5, 19.5), (3, 21)], r=k)),
    ]


@icon("mirage", CAT, "Upside down palm tree floating over a shimmering desert horizon",
      tags=["desert illusion", "heat shimmer", "optical illusion", "oasis", "palm", "reflection"])
def _(S):
    return [
        line("M12 2.5V8.5"),
        line("M12 8.5C9.5 12.5 6.5 12.5 4 8"),
        line("M12 8.5C14.5 12.5 17.5 12.5 20 8"),
        pit(S, 10.5, 11.5, 1.0), pit(S, 13.5, 11.5, 1.0),
        line("M2 17.5H22"),
        line("M4 21C6 19.5 8 19.5 10 21S14 22.5 16 21S18 19.5 20 21"),
    ]


def _halo_crescent(S):
    cx, cy, R = 12, 12, 5.8
    d = minus(circle(cx, cy, R), circle(cx + 3.2, cy - 1.8, 4.6))
    return soften(d, 1.0) if S.name != "line" else d


@icon("moon-halo", CAT, "Crescent moon inside a large thin ring of light",
      tags=["lunar halo", "ice crystals", "ring around moon", "night sky", "weather", "22 degree halo"])
def _(S):
    return [shell(_halo_crescent(S)), line(circle(12, 12, 9.5))]


@icon("jet-stream", CAT, "Globe with a wavy band of fast wind running across it, ending in an arrow",
      tags=["high altitude wind", "weather", "air current", "atmosphere", "polar vortex", "meteorology"])
def _(S):
    wave = wave_pts((4.5, 12), (17.5, 12), 2.3, 1.0, 34)
    (x0, y0), (x1, y1) = wave[-2], wave[-1]
    deg = math.degrees(math.atan2(y1 - y0, x1 - x0))
    return [shell(circle(12, 12, 9)), detail(pts_d(wave)), detail(arrow_head((x1 + 1.2, y1), deg, 2.2))]


@icon("mercury-planet", CAT, "Small grey planet covered in round craters",
      tags=["mercury", "planet", "solar system", "craters", "inner planet", "astronomy"])
def _(S):
    return [shell(circle(12, 12, 9)), pit(S, 8.5, 9, 1.6), pit(S, 15.5, 10.5, 2.0), pit(S, 11, 16, 1.4), pit(S, 17, 16, 1.0)]


@icon("venus-planet", CAT, "Planet wrapped in thick swirling cloud bands",
      tags=["venus", "planet", "solar system", "clouds", "inner planet", "astronomy"])
def _(S):
    def swirl(y, amp):
        hw = chord_half(12, 12, 9, y) - 2.2
        return pts_d(wave_pts((12 - hw, y), (12 + hw, y), amp, 1.25, 26))
    return [shell(circle(12, 12, 9)), detail(swirl(8.3, 1.3)), detail(swirl(12.5, 1.3)), detail(swirl(16.7, 1.3))]


@icon("mars-planet", CAT, "Red planet with a white polar cap and a long canyon scar",
      tags=["mars", "red planet", "planet", "solar system", "canyon", "astronomy"])
def _(S):
    k = S.r * 0.4
    cap = inter(circle(12, 12, 8.4), rect(0, 0, 24, 6.6))
    return [
        shell(circle(12, 12, 9)),
        mark(cap),
        detail(poly([(4.8, 14), (9, 12.2), (12.5, 15), (19.5, 12.8)], r=k)),
        pit(S, 14.5, 18, 1.0),
    ]


@icon("jupiter-planet", CAT, "Giant banded planet with an oval storm spot",
      tags=["jupiter", "gas giant", "planet", "great red spot", "solar system", "astronomy"])
def _(S):
    ins = L(S, 0, 2.0)
    spot = lens(14, 12, 3.4, 1.7, 0, S, 0) if S.name == "line" else ellipse(14, 12, 3.2, 1.7)
    return [
        shell(circle(12, 12, 9.5)),
        detail(band(12, 12, 9.5, 7.5, ins)),
        detail(band(12, 12, 9.5, 16.5, ins)),
        mark(spot),
    ]


@icon("uranus-planet", CAT, "Planet circled by a thin ring tilted nearly upright",
      tags=["uranus", "ice giant", "planet", "tilted ring", "solar system", "astronomy"])
def _(S):
    cx, cy, pr = 12, 12, 5.5
    front = ell_pts(cx, cy, 10.3, 2.6, 78, 0, 180, 5)
    back = ell_pts(cx, cy, 10.3, 2.6, 78, 180, 360, 5)
    parts = [line(pts_d(front))] + [line(pts_d(r)) for r in clear_of(back, [(cx, cy, pr + 1.3)])]
    return [shell(circle(cx, cy, pr)), *parts]


@icon("neptune-planet", CAT, "Blue planet with a tilted cloud band, a dark oval storm and a short bright streak",
      tags=["neptune", "ice giant", "planet", "great dark spot", "solar system", "astronomy"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(tband(12, 12, 9, -4.3, -18, 0)),
        mark(ellipse(9, 14.5, 3, 1.8)),
        detail(tband(12, 12, 9, 3.5, -18, 5.2)),
    ]


@icon("pluto-planet", CAT, "Small dwarf planet with a large heart shaped plain",
      tags=["pluto", "dwarf planet", "kuiper belt", "heart", "solar system", "astronomy"])
def _(S):
    h = heart_sharp(12, 12.3, 9.5) if S.name == "line" else soften(heart_d(12, 12.3, 9.5, 8.6), 1.2)
    return [shell(circle(12, 12, 8.5)), mark(h)]


@icon("planet-orbit", CAT, "Tilted orbit ring around a central star with a planet on it",
      tags=["solar system", "orbit", "star", "planet", "astronomy", "orbital path"])
def _(S):
    c = (12, 12)
    ring = ell_pts(*c, 10, 5, -25, 0, 360, 4)
    pl = ring[int(len(ring) * 0.62)]
    parts = [line(pts_d(r)) for r in clear_of(ring, [(pl[0], pl[1], 3.0)])]
    return [*parts, shell(circle(*pl, 1.9)), dot(*c, 2.3)]


@icon("asteroid-belt", CAT, "Half ring of small rocks between two orbit lines around a sun",
      tags=["main belt", "asteroids", "solar system", "orbit", "space rocks", "astronomy"])
def _(S):
    c = (12, 19)
    rocks = [(-166, 7.5, 1.0), (-140, 8.6, 1.2), (-118, 7.6, 1.0), (-96, 8.8, 1.1), (-72, 7.6, 1.2), (-50, 8.8, 1.0),
             (-26, 7.6, 1.0)]
    return [
        line(arc(*c, 5, 200, 340)),
        line(arc(*c, 11.5, 200, 340)),
        dot(*c, 2.2),
        *[pit(S, *polar(*c, r, a), s) for a, r, s in rocks],
    ]


# ============================================================================ shooting stars, craters, moon phases

def _streak(S, x, y, length, head=1.6):
    """Falling streak: glowing head at (x, y), tail running up and to the right."""
    tx, ty = x + length * 0.7071, y - length * 0.7071
    return [dot(x, y, head), line(seg(x + 2.2 * 0.7071, y - 2.2 * 0.7071, tx, ty))]


@icon("meteor-shower", CAT, "Three parallel streaks with glowing heads falling diagonally across the night sky",
      tags=["shooting stars", "perseids", "leonids", "falling stars", "night sky", "astronomy"])
def _(S):
    return [*_streak(S, 4, 11, 8), *_streak(S, 10, 17, 11), *_streak(S, 15.5, 11, 6.5, 1.4)]


@icon("meteorite-impact", CAT, "Rock with a fiery tail hitting the ground, throwing up debris beside a shallow crater",
      tags=["asteroid strike", "space rock", "collision", "crater", "disaster", "astronomy"])
def _(S):
    rk = rock(8.5, 11, [3.9, 3.3, 4.0, 3.5, 3.9, 3.4, 3.8], 15, S)
    return [
        shell(rk),
        line("M12.5 8L17.5 3"),
        line("M13.5 12L20 5.5"),
        line(poly([(2, 19.5), (6, 19.5), (8, 21.5), (16, 21.5), (18, 19.5), (22, 19.5)], r=S.r)),
        pit(S, 4.2, 15.5, 1.0), pit(S, 19.8, 15.5, 1.0), pit(S, 15.5, 16.5, 1.0),
    ]


@icon("impact-crater", CAT, "Cross section of the ground dug into a bowl with raised rims and a central peak",
      tags=["crater", "moon crater", "meteor crater", "impact site", "pit", "astronomy"])
def _(S):
    pts = [(2.5, 12), (4.5, 12), (6.5, 10), (9, 16), (10.8, 16), (12, 13.6), (13.2, 16), (15, 16), (17.5, 10), (19.5, 12),
           (21.5, 12), (21.5, 21), (2.5, 21)]
    return [shell(poly(pts, closed=True, r=S.r))]


def _holes(S, pts):
    """Regions of small square (Line) or round (Rounded) holes."""
    return [rect(x - r, y - r, 2 * r, 2 * r) if S.name == "line" else circle(x, y, r) for x, y, r in pts]


def _phase_filled(lit_d, holes=()):
    body = D(P(circle(12, 12, 10)), D(P(circle(12, 12, 8)), P(lit_d)))
    for x, y, r in holes:
        body = D(body, P(circle(x, y, r)))
    return body


_HALF_LIT = inter(circle(12, 12, 9), rect(12, 0, 12, 24))
_HALF_HOLES = [(16, 8.5, 1.2), (15.5, 15, 1.4)]
_GIB_LIT = inter(circle(12, 12, 9), circle(18.75, 12, 11.25))
_GIB_HOLES = [(14, 8, 1.2), (16.5, 14.5, 1.3), (11.5, 16.5, 1.0)]
_ECL_SHADOW = inter(circle(12, 12, 9), circle(3, 17, 9.5))


@icon("half-moon", CAT, "Moon with its right half lit and craters on the lit side, the first quarter phase",
      tags=["first quarter", "quarter moon", "moon phase", "lunar phase", "night sky", "astronomy"],
      filled=lambda: _phase_filled(_HALF_LIT, _HALF_HOLES))
def _(S):
    return [shell(circle(12, 12, 9)), solid(minus(_HALF_LIT, *_holes(S, _HALF_HOLES)))]


@icon("gibbous-moon", CAT, "Moon that is mostly lit with a thin dark crescent on its left edge",
      tags=["waxing gibbous", "waning gibbous", "moon phase", "lunar phase", "night sky", "astronomy"],
      filled=lambda: _phase_filled(_GIB_LIT, _GIB_HOLES))
def _(S):
    return [shell(circle(12, 12, 9)), solid(minus(_GIB_LIT, *_holes(S, _GIB_HOLES)))]


def _new_moon_filled():
    ring = D(P(circle(12, 12, 10)), P(circle(12, 12, 8)))
    disc = D(P(circle(12, 12, 5.8)), P(circle(10, 10.5, 1.0)), P(circle(14.2, 14, 1.2)))
    return U(ring, disc)


@icon("new-moon", CAT, "Dark moon disc inside a thin outline ring, the phase with no lit face",
      tags=["dark moon", "moon phase", "lunar phase", "no moon", "night sky", "astronomy"],
      filled=_new_moon_filled)
def _(S):
    disc = minus(circle(12, 12, 5.8), *_holes(S, [(10, 10.5, 1.0), (14.2, 14, 1.2)]))
    return [shell(circle(12, 12, 9)), solid(disc)]


@icon("blood-moon", CAT, "Full moon crossed by curved bands of shadow with a red drop, for a total lunar eclipse",
      tags=["red moon", "total lunar eclipse", "eclipse", "moon", "night sky", "astronomy"])
def _(S):
    arcs = []
    for r in (5.5, 9.5):
        pts = arc_pts(4, 4, r, -10, 100, 3)
        for run in runs(pts, lambda p: math.hypot(p[0] - 12, p[1] - 12) < 6.4):
            arcs.append(detail(pts_d(run)))
    tip = (15.3, 11.6)
    drop = f"M{fmt(tip[0])} {fmt(tip[1])}C{fmt(tip[0] + 0.6)} {fmt(tip[1] + 1.2)} {fmt(tip[0] + 1.9)} {fmt(tip[1] + 2.0)} {fmt(tip[0] + 1.9)} {fmt(tip[1] + 3.3)}A1.9 1.9 0 0 1 {fmt(tip[0] - 1.9)} {fmt(tip[1] + 3.3)}C{fmt(tip[0] - 1.9)} {fmt(tip[1] + 2.0)} {fmt(tip[0] - 0.6)} {fmt(tip[1] + 1.2)} {fmt(tip[0])} {fmt(tip[1])}Z"
    return [shell(circle(12, 12, 9)), *arcs, mark(drop)]


@icon("lunar-eclipse", CAT, "Moon disc partly hidden by the curved dark shadow of the Earth",
      tags=["moon eclipse", "earth shadow", "partial eclipse", "umbra", "night sky", "astronomy"],
      filled=lambda: _phase_filled(_ECL_SHADOW, []))
def _(S):
    return [shell(circle(12, 12, 9)), solid(_ECL_SHADOW), pit(S, 15.5, 8, 1.2), pit(S, 16.5, 14, 1.0)]


@icon("annular-eclipse", CAT, "Dark disc centred on a larger ring of sun leaving a bright thin ring with corona dots",
      tags=["ring of fire", "solar eclipse", "annulus", "sun", "eclipse", "astronomy"],
      filled=lambda: U(D(P(circle(12, 12, 7.5)), P(circle(12, 12, 5.1))), P(circle(12, 12, 3.6)),
                       *[P(circle(*polar(12, 12, 9.6, a), 1.0)) for a in range(0, 360, 45)]))
def _(S):
    return [shell(circle(12, 12, 6.3)), solid(circle(12, 12, 3.5)), *[pit(S, *polar(12, 12, 9.6, a), 0.9) for a in range(0, 360, 45)]]


@icon("supermoon", CAT, "Huge full moon rising behind the horizon with a tiny tree silhouetted in front of it",
      tags=["big moon", "moonrise", "full moon", "perigee moon", "horizon", "night sky"])
def _(S):
    moon = inter(circle(12, 10, 9), rect(0, 0, 24, 17.5))
    crown = circle(15.5, 11.6, 2.4)
    return [shell(moon), line("M2 17.5H22"), mark(crown), mark(rect(14.5, 13.5, 2, 4))]


@icon("earthrise", CAT, "Earth hanging above the curved horizon of the moon with a few stars",
      tags=["earth from moon", "lunar horizon", "apollo", "blue marble", "moon", "astronomy"])
def _(S):
    land = poly([(9.3, 7.5), (11.8, 6.6), (13.2, 8.4), (11.4, 10.4), (9, 10)], closed=True, r=S.r * 0.3)
    return [
        shell(circle(12, 9.5, 6.25)),
        mark(land),
        line("M2 21C6 17.5 18 17.5 22 21"),
        dot(3.5, 5, 1.0), dot(20.5, 4.5, 1.0),
    ]


@icon("lunar-surface", CAT, "Dusty moon ground with craters and rocks under a small Earth in the dark sky",
      tags=["moon ground", "regolith", "moonscape", "craters", "earth in sky", "astronomy"])
def _(S):
    dome = "M2.8 21C4 15.5 7.5 13.5 12 13.5S20 15.5 21.2 21Z"
    return [
        shell(dome),
        pit(S, 8.5, 18, 1.1), pit(S, 14.5, 17.5, 1.4),
        mark(poly([(17.3, 19), (18.3, 17.3), (19.3, 19)], closed=True)),
        shell(circle(17, 5.5, 3)),
        dot(5, 6, 1.0), dot(9.5, 9.5, 0.9),
    ]


@icon("sunspots", CAT, "Sun disc marked with several dark irregular spots",
      tags=["solar activity", "sun", "photosphere", "solar cycle", "star", "astronomy"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        mark(rock(9, 9, [3.0, 2.3, 3.1, 2.4, 2.8, 2.2], 10, S)),
        mark(rock(15.5, 13.5, [2.3, 1.7, 2.4, 1.8, 2.2], 40, S)),
        mark(rock(9.5, 16, [1.7, 1.3, 1.8, 1.4], 70, S)),
    ]


@icon("solar-flare", CAT, "Arch of hot plasma rising off the edge of the sun with blobs flung upward",
      tags=["solar storm", "coronal loop", "plasma", "sun", "space weather", "prominence"])
def _(S):
    dome = "M2.8 21C3.8 17.5 7.5 15.5 12 15.5S20.2 17.5 21.2 21Z"
    return [
        shell(dome),
        line("M7.5 15.5C6.5 9.5 9 7 12 7C15 7 17.5 9.5 16.5 15.5"),
        dot(12, 3.6, 1.1), dot(6, 6.5, 1.0), dot(18, 6.5, 1.0),
    ]


@icon("solar-wind", CAT, "Sun on the left with streams of particles curling past a small planet",
      tags=["particle stream", "space weather", "sun", "magnetosphere", "planet", "charged particles"])
def _(S):
    return [
        shell(circle(5.5, 12, 3.6)),
        line("M11.5 9C14 8.5 15 5.5 19 5"),
        line("M11.5 15C14 15.5 15 18.5 19 19"),
        line("M11 12H13.5"),
        shell(circle(19.25, 12, 2.6)),
    ]


# ============================================================================ stars, nebulae and galaxies

def rot180(d):
    return path_to_d(transform_path(P(d), (-1, 0, 0, -1, 24, 24)))


@icon("supernova", CAT, "Exploding star drawn as a jagged burst with a bright core",
      tags=["exploding star", "stellar explosion", "nova", "star death", "blast", "astronomy"])
def _(S):
    pts = [polar(12, 12, 8.6 if i % 2 == 0 else 4.2, -90 + i * 22.5) for i in range(16)]
    return [shell(poly(pts, closed=True, r=S.r * 0.4)), dot(12, 12, 1.6)]


@icon("nebula", CAT, "Irregular gas cloud with a swirl through it and a few stars",
      tags=["gas cloud", "interstellar cloud", "star forming", "deep sky", "space", "astronomy"])
def _(S):
    pts = [(3.5, 12), (5, 6.5), (10, 4), (15, 4.5), (20, 7.5), (20.5, 13), (17, 18.5), (11, 20), (6, 17.5)]
    body = smooth_closed(pts, 0.9) if S.name != "line" else poly(pts, closed=True)
    return [shell(body), detail("M7.5 14C10 10.5 14 13.5 16.5 9.5"), pit(S, 10, 7.5, 1.0), pit(S, 16, 15.5, 1.0)]


@icon("planetary-nebula", CAT, "Glowing ring shell of gas around a small star at its centre",
      tags=["ring nebula", "dying star", "gas shell", "deep sky", "space", "astronomy"])
def _(S):
    ring = minus(circle(12, 12, 9.5), circle(12, 12, 5.6))
    core = Part("dot", spark(12, 12, 2.6, 1.0, S)) if S.name == "line" else dot(12, 12, 1.6)
    return [shell(ring), core]


@icon("pulsar", CAT, "Small star with two narrow beams sweeping out of opposite sides and a spin arc",
      tags=["neutron star", "radio pulsar", "lighthouse star", "beam", "rotating star", "astronomy"])
def _(S):
    k = S.r * 0.3
    return [
        shell(circle(12, 12, 3)),
        solid(poly([(13.4, 10.2), (19.4, 2.6), (21.6, 4.8), (14.2, 10.9)], closed=True, r=k)),
        solid(poly([(10.6, 13.8), (4.6, 21.4), (2.4, 19.2), (9.8, 13.1)], closed=True, r=k)),
        line(arc(12, 12, 6.3, 20, 100)),
        line(arc(12, 12, 6.3, 200, 280)),
    ]


@icon("quasar", CAT, "Bright core inside a flat disk with two long jets shooting out opposite ways",
      tags=["active galactic nucleus", "black hole jet", "agn", "distant galaxy", "deep space", "astronomy"])
def _(S):
    disk = lens(12, 12, 10, 2.6, 0, S, L(S, 0, 1.3)) if S.name == "line" else ellipse(12, 12, 9.5, 2.8)
    return [shell(disk), dot(12, 12, 1.4), line("M12 9V2.5"), line("M12 15V21.5")]


@icon("red-giant", CAT, "Very large star circle beside a tiny sun circle for comparison",
      tags=["giant star", "dying star", "star size", "stellar evolution", "big star", "astronomy"])
def _(S):
    return [shell(circle(9.5, 11.5, 7.5)), pit(S, 7.5, 9.5, 1.3), pit(S, 11.5, 13.5, 1.3), dot(20, 18.5, 1.9)]


@icon("white-dwarf", CAT, "Tiny bright star with rays beside a much larger faint dashed circle",
      tags=["dwarf star", "dead star", "stellar remnant", "small star", "star size", "astronomy"])
def _(S):
    dashes = [line(arc(15.5, 12, 7, a, a + 24)) for a in range(0, 360, 45)]
    return [Part("dot", spark(6, 12, 3.6, 1.1, S)), *dashes]


@icon("double-star-system", CAT, "Two stars circling each other on a shared tilted orbit",
      tags=["binary star", "twin stars", "star pair", "orbit", "binary system", "astronomy"])
def _(S):
    ring = ell_pts(12, 12, 10, 5.2, -25, 0, 360, 4)
    a, b = ring[int(len(ring) * 0.12)], ring[int(len(ring) * 0.62)]
    parts = [line(pts_d(r)) for r in clear_of(ring, [(a[0], a[1], 3.3), (b[0], b[1], 3.0)])]
    return [*parts, shell(circle(*a, 2.0)), dot(*b, 1.7)]


@icon("star-cluster", CAT, "Dense round group of small stars bunched together inside a dashed outline",
      tags=["globular cluster", "open cluster", "star group", "stars", "deep sky", "astronomy"])
def _(S):
    spots = [(12, 12, 1.6), (8.5, 8.5, 1.1), (15.5, 8.8, 1.2), (16, 14.5, 1.1), (9, 15, 1.2), (12, 6.2, 0.9), (18, 11.5, 0.9),
             (6, 12, 0.9), (12.5, 17.8, 0.9)]
    ring = [line(arc(12, 12, 9.4, a, a + 22)) for a in range(0, 360, 36)]
    return [*ring, *[pit(S, x, y, r) for x, y, r in spots]]


@icon("elliptical-galaxy", CAT, "Smooth oval galaxy glowing brighter toward its centre",
      tags=["galaxy", "oval galaxy", "old stars", "deep sky", "space", "astronomy"])
def _(S):
    if S.name == "line":
        outer, inner = lens(12, 12, 10.5, 5.8, -25, S, 0), lens(12, 12, 5.6, 3.0, -25, S, 0)
    else:
        outer, inner = tilted_ellipse(12, 12, 10, 5.8, -25), tilted_ellipse(12, 12, 5, 2.8, -25)
    return [shell(outer), detail(inner), dot(12, 12, 0.9)]


@icon("barred-galaxy", CAT, "Spiral galaxy with a straight bar across its core and an arm curling from each end",
      tags=["galaxy", "spiral galaxy", "milky way", "deep sky", "bar", "astronomy"])
def _(S):
    pts = []
    for i in range(33):
        t = i / 32
        pts.append(polar(12, 12, 5.4 + t * 4.8, -25 + t * 215))
    arm = pts_d(pts)
    return [line("M7.6 14L16.4 10"), line(arm), line(rot180(arm))]


@icon("accretion-disk", CAT, "Swirling flat disk of matter spiralling into a dark sphere at the centre",
      tags=["black hole disk", "gas disk", "infall", "spiral", "gravity", "astronomy"])
def _(S):
    m = axis((12, 12), -25)
    arms = []
    for off in (0, 180):
        pts = []
        for i in range(31):
            t = i / 30
            ang = math.radians(off + t * 300)
            r = 10.5 - t * 6.0
            pts.append(m(r * math.cos(ang), r * 0.6 * math.sin(ang)))
        arms.append(line(pts_d(pts)))
    return [*arms, dot(12, 12, 2.2)]


@icon("wormhole", CAT, "Funnel shaped tunnel pinching to a narrow throat and opening out again, like an hourglass",
      tags=["einstein rosen bridge", "space tunnel", "portal", "spacetime", "sci-fi", "astronomy"])
def _(S):
    return [
        line("M3.5 5.5C9 7 10 9.5 10 12C10 14.5 9 17 3.5 18.5"),
        line("M20.5 5.5C15 7 14 9.5 14 12C14 14.5 15 17 20.5 18.5"),
        line(lens(12, 5.2, 8.2, 1.7, 0, S, 0) if S.name == "line" else ellipse(12, 5.2, 8.6, 1.6)),
        line(lens(12, 18.8, 8.2, 1.7, 0, S, 0) if S.name == "line" else ellipse(12, 18.8, 8.6, 1.6)),
        line("M10.2 12H13.8"),
    ]


@icon("big-bang", CAT, "Tiny bright point bursting outward with expanding arcs and scattered specks",
      tags=["origin of universe", "cosmic explosion", "expansion", "cosmology", "singularity", "astronomy"])
def _(S):
    arcs = [line(arc(12, 12, 5.5, a, a + 50)) for a in (-75, 45, 165)]
    specks = [pit(S, *polar(12, 12, 9.2, a), 1.0) for a in (10, 70, 130, 190, 250, 310)]
    return [dot(12, 12, 2.0), *arcs, *specks]


@icon("gravitational-lensing", CAT, "Heavy mass in the middle bending distant light into curved arcs around it",
      tags=["einstein ring", "light bending", "dark matter", "cosmology", "galaxy cluster", "astronomy"])
def _(S):
    return [dot(12, 12, 2.6), line(arc(12, 12, 6.3, -75, -5)), line(arc(12, 12, 6.3, 105, 175)),
            line(arc(12, 12, 10, -60, -30)), line(arc(12, 12, 10, 120, 150))]


# ============================================================================ orbits, star patterns and the sky sphere

def _stars_on(pts, sizes):
    return [dot(x, y, r) for (x, y), r in zip(pts, sizes)]


def _pit_stars(S, pts, sizes):
    return [pit(S, x, y, r) for (x, y), r in zip(pts, sizes)]


def _links(pairs, pts, sizes, gap=1.2):
    """Constellation lines between star dots, stopped short of each dot."""
    out = []
    for i, j in pairs:
        (x0, y0), (x1, y1) = pts[i], pts[j]
        ln = math.hypot(x1 - x0, y1 - y0)
        a, b = sizes[i] + gap, sizes[j] + gap
        if ln - a - b < 1.0:
            continue
        ux, uy = (x1 - x0) / ln, (y1 - y0) / ln
        out.append(line(seg(x0 + ux * a, y0 + uy * a, x1 - ux * b, y1 - uy * b)))
    return out


def _chain(n, closed_to=None):
    pairs = [(i, i + 1) for i in range(n - 1)]
    if closed_to is not None:
        pairs.append((n - 1, closed_to))
    return pairs


@icon("spacetime-grid", CAT, "Curved sheet dipping into a well beneath a heavy sphere",
      tags=["gravity well", "general relativity", "curved space", "mass", "physics", "einstein"])
def _(S):
    return [shell(circle(12, 6, 3)), line("M2 11C8 11 10 19.5 12 19.5C14 19.5 16 11 22 11")]


@icon("exoplanet", CAT, "Star with a small planet crossing in front of it and a dip in the light curve below",
      tags=["transit", "planet hunting", "light curve", "kepler", "alien world", "astronomy"])
def _(S):
    return [
        shell(circle(12, 8.5, 6.2)),
        mark(circle(9.6, 8.5, 2.2)),
        line(poly([(2, 18), (7, 18), (8.5, 21), (15.5, 21), (17, 18), (22, 18)], r=S.r)),
    ]


@icon("habitable-zone", CAT, "Star with a shaded ring band between two orbit circles where water can stay liquid",
      tags=["goldilocks zone", "life zone", "star", "orbit", "exoplanet", "astronomy"])
def _(S):
    star = Part("dot", spark(12, 12, 2.4, 0.9, S)) if S.name == "line" else dot(12, 12, 1.5)
    return [star, line(circle(12, 12, 4.2)), solid(minus(circle(12, 12, 9.4), circle(12, 12, 6.8)))]


@icon("kuiper-belt", CAT, "Wide ring of scattered small rocks far outside the inner planet orbits",
      tags=["trans neptunian", "icy objects", "outer solar system", "dwarf planets", "orbit", "astronomy"])
def _(S):
    rocks = [pit(S, *polar(12, 12, 8.6 + (i % 3) * 0.7, a), 0.9 + (i % 2) * 0.2) for i, a in enumerate(range(0, 360, 30))]
    return [dot(12, 12, 1.5), line(circle(12, 12, 4.2)), *rocks]


@icon("polaris", CAT, "Bright star with long cross spikes above two pointer stars",
      tags=["north star", "pole star", "navigation", "star", "night sky", "astronomy"])
def _(S):
    return [Part("dot", spark(12, 8, 6.5, 1.4, S)), pit(S, 7, 19, 1.6), pit(S, 15.5, 17.5, 1.6), line("M9.4 18.6L12.6 18.1"), line("M14.3 15.2L13.3 14.3")]


@icon("big-dipper", CAT, "Seven stars joined in the ladle shape of the dipper",
      tags=["ursa major", "plough", "asterism", "stars", "constellation", "night sky"])
def _(S):
    pts = [(3.5, 5.5), (7.5, 8), (11, 10.5), (14, 12), (20.5, 11), (20.5, 17.5), (14.5, 17.5)]
    sz = [1.5] * 7
    return [*_links(_chain(7, 3), pts, sz), *_pit_stars(S, pts, sz)]


@icon("little-dipper", CAT, "Seven small stars in a smaller ladle shape ending at a bright star",
      tags=["ursa minor", "asterism", "stars", "constellation", "night sky", "polaris"])
def _(S):
    pts = [(20, 4.5), (16.5, 7), (13.5, 10), (10.5, 12.5), (10, 18.5), (4.5, 18), (5, 12)]
    sz = [1.6, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3]
    return [*_links(_chain(7, 3), pts, sz), *_pit_stars(S, pts, sz)]


@icon("orion-constellation", CAT, "Star dots in the hunter pattern with three belt stars in a line",
      tags=["orion", "hunter", "belt", "betelgeuse", "rigel", "constellation"])
def _(S):
    pts = [(7.5, 4.5), (16.5, 4.5), (9.8, 11.5), (12, 12.3), (14.2, 13.1), (8.5, 20), (16, 20)]
    sz = [1.6, 1.4, 1.1, 1.1, 1.1, 1.4, 1.7]
    pairs = [(0, 2), (2, 5), (1, 4), (4, 6), (2, 3), (3, 4)]
    return [*_links(pairs, pts, sz, 1.0), *_pit_stars(S, pts, sz)]


@icon("cassiopeia", CAT, "Five stars joined in a W zigzag",
      tags=["w shape", "queen", "asterism", "stars", "constellation", "night sky"])
def _(S):
    pts = [(3.5, 8), (8, 16), (12, 10), (16.5, 17), (20.5, 7.5)]
    sz = [1.6] * 5
    return [*_links(_chain(5), pts, sz), *_pit_stars(S, pts, sz)]


@icon("southern-cross", CAT, "Four bright stars in a kite cross pattern with a small fifth star",
      tags=["crux", "southern hemisphere", "navigation", "stars", "constellation", "night sky"])
def _(S):
    pts = [(12, 3.8), (12, 20), (6.5, 11.5), (17.5, 8.5)]
    sz = [1.7, 1.7, 1.5, 1.5]
    return [*_links([(0, 1), (2, 3)], pts, sz), *_pit_stars(S, pts, sz), pit(S, 16.3, 15.5, 1.0)]


@icon("pleiades", CAT, "Tight group of seven star dots in a small dipper shape with a hazy arc either side",
      tags=["seven sisters", "star cluster", "messier 45", "open cluster", "stars", "night sky"])
def _(S):
    pts = [(7, 14), (10, 12.5), (13, 11), (16, 9.5), (13, 15), (16.5, 14.5), (10, 8.5)]
    return [*_pit_stars(S, pts, [1.3, 1.6, 1.5, 1.3, 1.5, 1.2, 1.1]), line(arc(12, 12, 10, 150, 200)), line(arc(12, 12, 10, -30, 20))]


@icon("celestial-sphere", CAT, "Sphere with a tilted axis through its poles and an equator ring",
      tags=["sky sphere", "equator", "ecliptic", "astronomy model", "coordinates", "celestial equator"])
def _(S):
    a, b = polar(12, 12, 10.6, -67), polar(12, 12, 10.6, 113)
    return [shell(circle(12, 12, 8)), detail(tilted_ellipse(12, 12, 8, 2.8, 23)), line(seg(*a, *b))]


@icon("light-year", CAT, "Star and planet joined by a long measuring line with arrowheads",
      tags=["distance", "space distance", "measure", "stellar distance", "parsec", "astronomy"])
def _(S):
    return [
        Part("dot", spark(5, 7, 3.4, 1.1, S)), shell(circle(19.5, 7, 2.4)),
        line("M3 17H21"),
        line(poly([(6, 14.5), (3, 17), (6, 19.5)])), line(poly([(18, 14.5), (21, 17), (18, 19.5)])),
    ]


@icon("dark-matter", CAT, "Faint dashed halo around a small spiral galaxy",
      tags=["invisible mass", "galaxy halo", "cosmology", "gravity", "physics", "astronomy"])
def _(S):
    halo = [line(arc(12, 12, 9.5, a, a + 26)) for a in range(0, 360, 40)]
    return [*halo, dot(12, 12, 1.4), line(arc(12, 12, 4, 200, 340)), line(arc(12, 12, 4, 20, 160))]


@icon("galaxy-collision", CAT, "Two galaxies overlapping with a tidal tail of stars streaming between them",
      tags=["merging galaxies", "galaxy merger", "interaction", "tidal tail", "deep sky", "astronomy"])
def _(S):
    def gal(cx, cy, tilt):
        return shell(lens(cx, cy, 4.6, 2.3, tilt, S, 0) if S.name == "line" else tilted_ellipse(cx, cy, 4.4, 2.3, tilt))
    return [gal(7.5, 16, -40), gal(16.5, 8, 40), dot(7.5, 16, 0.9), dot(16.5, 8, 0.9),
            line("M11.5 17C15 18.5 19 17.5 20.5 14"), line("M12.5 7C9 5.5 5 6.5 3.5 10")]


# ============================================================================ planets in motion and sky instruments

_NIGHT = inter(circle(12, 12, 9), circle(3, 12, 11))
_NIGHT_HOLES = [(6.5, 8.5, 1.0), (8, 15.5, 1.1)]


@icon("sun-cross-section", CAT, "Sun cut open showing its core and the layers around it",
      tags=["sun layers", "solar interior", "core", "convection zone", "star structure", "astronomy"])
def _(S):
    core = Part("dot", spark(12, 12, 3.0, 1.1, S)) if S.name == "line" else dot(12, 12, 2.0)
    return [shell(circle(12, 12, 9)), detail(circle(12, 12, 5.8)), core]


@icon("earth-axis-tilt", CAT, "Globe leaning on a slanted axis beside an upright reference line",
      tags=["seasons", "obliquity", "earth tilt", "axial tilt", "earth", "geography"])
def _(S):
    a, b = polar(12, 13, 10, -66.5), polar(12, 13, 10, 113.5)
    land = poly([(9.5, 10), (12.5, 9.2), (13.5, 11.5), (11, 13), (9, 12.5)], closed=True, r=S.r * 0.3)
    return [shell(circle(12, 13, 6.5)), mark(land), line(seg(*a, *b)), line("M12 2.2V4.6")]


@icon("day-night-terminator", CAT, "Globe with its night side solid, starry holes in the dark and a curved edge where day meets night",
      tags=["terminator", "day and night", "sunrise line", "earth", "shadow line", "geography"],
      filled=lambda: _phase_filled(_NIGHT, _NIGHT_HOLES))
def _(S):
    return [shell(circle(12, 12, 9)), solid(minus(_NIGHT, *_holes(S, _NIGHT_HOLES))), detail("M17 5.5C19 9.5 19 14.5 17 18.5")]


@icon("moon-orbit", CAT, "Earth circle with a smaller moon travelling on a ring around it",
      tags=["lunar orbit", "satellite", "earth and moon", "month", "orbit", "astronomy"])
def _(S):
    ring = arc_pts(12, 12, 9, 0, 360, 4)
    m = polar(12, 12, 9, -45)
    parts = [line(pts_d(r)) for r in clear_of(ring, [(m[0], m[1], 3.3)])]
    return [*parts, shell(circle(12, 12, 4)), pit(S, *m, 1.7)]


@icon("radio-telescope", CAT, "Large dish on an A shaped frame with a feed on its arm, aimed at the sky",
      tags=["antenna", "dish", "radio astronomy", "observatory", "signal", "space listening"])
def _(S):
    bowl = "M3.5 4C3.5 10 7.5 13 12 13C16.5 13 20.5 10 20.5 4Z" if S.name != "line" else "M3.5 4L7 11L12 13L17 11L20.5 4Z"
    return [
        shell(bowl),
        line("M12 13V9"), dot(12, 7.6, 1.2),
        line("M12 15L7 21.5"), line("M12 15L17 21.5"), line("M8.8 19H15.2"),
    ]


@icon("space-telescope", CAT, "Cylinder telescope tube with two solar panels and an open aperture door",
      tags=["orbital telescope", "hubble style", "observatory", "satellite", "deep space", "astronomy"])
def _(S):
    return [
        shell(rect(2.5, 9.5, 14, 6, min(S.R, 1.5))),
        shell(rect(6, 2.5, 7, 4.5, min(S.R, 1.5))),
        shell(rect(6, 18, 7, 4, min(S.R, 1.5))),
        line("M9.5 7V9.5"), line("M9.5 15.5V18"),
        line("M16.5 9.5L21 5.5"),
    ]


@icon("armillary-sphere", CAT, "Nested metal rings around a central ball on a small stand",
      tags=["ring sphere", "old astronomy model", "zodiac", "sky model", "antique", "navigation"])
def _(S):
    return [
        line(circle(12, 10.5, 8)),
        line(ellipse(12, 10.5, 8, 2.8)),
        line(ellipse(12, 10.5, 2.8, 8)),
        dot(12, 10.5, 1.5),
        line("M12 19.5V21.5"), line("M8 21.5H16"),
    ]


@icon("astrolabe", CAT, "Round disk with a hanging ring, a pointer rule through the centre and scale marks",
      tags=["old navigation", "star finder", "medieval instrument", "altitude", "antique", "astronomy"])
def _(S):
    ticks = [detail(seg(*polar(12, 14, 4.6, a), *polar(12, 14, 6.0, a))) for a in (0, 90, 180, 270)]
    return [
        shell(union(circle(12, 14, 7.8), circle(12, 4.4, 2.3))),
        detail(seg(*polar(12, 14, 6.0, -35), *polar(12, 14, 6.0, 145))),
        *ticks, dot(12, 14, 1.2),
    ]


@icon("orrery", CAT, "Mechanical model with a central sun ball and planet balls on arms around it",
      tags=["solar system model", "clockwork planets", "planetarium", "mechanical", "antique", "astronomy"])
def _(S):
    return [
        dot(12, 11.5, 2.4),
        line("M13.5 10L18 6.5"), shell(circle(19.6, 5.3, 1.9)),
        line("M10.5 13L6.5 15.5"), dot(4.6, 16.6, 1.8),
        line("M13.6 13.4L17.2 17"), shell(circle(18.7, 18.4, 1.6)),
        line("M12 14V21.5"), line("M8 21.5H16"),
    ]


@icon("planisphere", CAT, "Round star wheel with an oval window showing stars and an outer date scale",
      tags=["star wheel", "star chart", "sky map", "stargazing", "night sky finder", "astronomy"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(ellipse(12, 12, 6.2, 4.6)), pit(S, 10, 11, 1.0), pit(S, 14, 10.6, 1.0), pit(S, 12.3, 14, 1.0)]


@icon("sextant", CAT, "Pie shaped navigation instrument with a scale arc, pointer arm and sighting mirror",
      tags=["navigation", "ship", "star sighting", "altitude", "antique", "celestial navigation"])
def _(S):
    a, b = polar(12, 4, 16.5, 58), polar(12, 4, 16.5, 122)
    frame = f"M12 4L{fmt(b[0])} {fmt(b[1])}A16.5 16.5 0 0 0 {fmt(a[0])} {fmt(a[1])}Z"
    return [shell(frame), detail(seg(12, 4, *polar(12, 4, 13, 76))), mark(rect(10.5, 6.2, 3, 2.6, 0.5))]


@icon("space-probe", CAT, "Small spacecraft body with a large dish antenna and a long boom arm",
      tags=["deep space probe", "voyager style", "spacecraft", "antenna", "explorer", "robotic mission"])
def _(S):
    dish = lens(7, 6.5, 5.2, 2.3, -50, S, 0) if S.name == "line" else tilted_ellipse(7, 6.5, 5, 2.3, -50)
    return [
        shell(rect(8.5, 11, 7, 7, min(S.R, 1.5))),
        shell(dish),
        line("M8.5 9.5L10.5 11"),
        line("M15.5 14.5H21"), mark(rect(19.5, 12.3, 3, 4.4)),
        line("M12 18V21"),
    ]


@icon("mars-rover", CAT, "Six wheeled rover with a tall mast camera and a folded robot arm",
      tags=["rover", "planetary explorer", "robotic vehicle", "mars", "science vehicle", "spacecraft"])
def _(S):
    return [
        shell(rect(6, 10.5, 12, 4.8, min(S.R, 1.5))),
        dot(6.5, 19, 2.0), dot(12, 19, 2.0), dot(17.5, 19, 2.0),
        line("M15 10.5V6"), mark(rect(13, 3, 4, 2.8, 0.6)),
        line(poly([(6.5, 11.5), (3.5, 8.5), (5.5, 5.5)], r=S.r * 0.5)),
    ]


@icon("lunar-lander", CAT, "Boxy lander body on four angled legs with foot pads and an engine bell below",
      tags=["moon lander", "apollo style", "spacecraft", "landing module", "touchdown", "astronomy"])
def _(S):
    nozzle = poly([(10.3, 14), (13.7, 14), (14.8, 17), (9.2, 17)], closed=True, r=S.r * 0.3)
    return [
        shell(rect(7.5, 6, 9, 8, min(S.R, 2.5))),
        line("M12 6V2.8"),
        line("M8.5 14L4 20"), line("M15.5 14L20 20"),
        line("M2.5 20.5H6"), line("M18 20.5H21.5"),
        mark(nozzle),
    ]


@icon("space-capsule", CAT, "Cone shaped crew capsule with a round window and a curved heat shield",
      tags=["crew capsule", "re-entry vehicle", "spacecraft", "command module", "astronaut ship", "splashdown"])
def _(S):
    body = poly([(9.8, 3.5), (14.2, 3.5), (19, 17), (5, 17)], closed=True, r=S.r * 0.6)
    return [shell(body), detail(circle(12, 10.6, 2.4)), line("M5 19.5C8 21.5 16 21.5 19 19.5")]


@icon("space-shuttle", CAT, "Winged orbiter seen from the side with a tall tail fin and a pointed nose",
      tags=["orbiter", "spaceplane", "reusable spacecraft", "shuttle", "nasa era", "space travel"])
def _(S):
    pts = [(2.5, 14.5), (5.5, 12), (10, 11.5), (18, 11.5), (18.5, 4), (21.5, 4), (21.5, 17), (14, 17), (10, 21), (7, 17), (3.5, 16.5)]
    return [shell(poly(pts, closed=True, r=S.r * 0.6)), detail("M10.5 14.5H16.5")]


@icon("solar-sail", CAT, "Small craft at the centre of a large square sail held by diagonal struts",
      tags=["light sail", "photon sail", "spacecraft", "propulsion", "future travel", "interstellar"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R * 0.5)), detail("M4.5 4.5L9.5 9.5"), detail("M19.5 4.5L14.5 9.5"),
            detail("M4.5 19.5L9.5 14.5"), detail("M19.5 19.5L14.5 14.5"), mark(rect(10, 10, 4, 4, L(S, 0, 1)))]


@icon("space-debris", CAT, "Broken satellite shards and a bolt drifting above the curve of a planet",
      tags=["orbital junk", "space junk", "satellite fragments", "collision", "clutter", "orbit"])
def _(S):
    k = S.r * 0.3
    return [
        mark(poly([(3, 7), (8.5, 6), (6, 11.5)], closed=True, r=k)),
        mark(poly([(12, 3.8), (16.5, 3.2), (14.2, 7)], closed=True, r=k)),
        pit(S, 7, 17, 1.3),
        line("M7 21.5A14.5 14.5 0 0 1 21.5 7"),
    ]


@icon("spacewalk", CAT, "Astronaut in a suit floating in space with a curly tether line trailing behind",
      tags=["eva", "astronaut", "space suit", "tether", "floating", "extravehicular"])
def _(S):
    tether = wave_pts((10.3, 15.5), (2.5, 18.5), 1.3, 1.5, 24)
    return [
        shell(circle(13.5, 6.5, 3.2)), mark(rect(12.6, 5.8, 3, 1.6, 0.5)),
        shell(rect(10.8, 11, 5.4, 6.5, min(S.R, 2))),
        line("M10.8 12.5L6.5 11"), line("M16.2 12.5L20.5 10.5"),
        line("M11.8 17.5L10 21.5"), line("M15.2 17.5L18 21"),
        line(pts_d(tether)),
    ]


@icon("moon-landing-flag", CAT, "Flag on a pole with a horizontal top bar planted in cratered ground",
      tags=["lunar flag", "moon mission", "apollo style", "landing site", "exploration", "astronaut"])
def _(S):
    return [
        line("M8 3V18.5"),
        shell(rect(8, 4.5, 12, 7, min(S.R, 1.5))),
        line("M2.5 20C8 17.5 16 17.5 21.5 20"),
        pit(S, 16, 20.6, 0.9),
    ]
