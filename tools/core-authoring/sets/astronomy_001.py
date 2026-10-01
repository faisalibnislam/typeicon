"""TypeIcon Core: astronomy (batch astronomy_001).

Deep sky objects, planets and moons, orbital mechanics, telescopes and astronaut gear. Drawn from the
objects and diagrams themselves; no mission logos or agency insignia.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar  # noqa: F401

CAT = "astronomy"


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


def axis(origin, deg):
    """Local frame: x runs along `deg` (0 = right, positive = clockwise on screen)."""
    ox, oy = origin
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return lambda x, y: (ox + x * c - y * s, oy + x * s + y * c)


def pts_d(pts, closed=False):
    d = "".join(("M" if i == 0 else "L") + f"{fmt(x)} {fmt(y)}" for i, (x, y) in enumerate(pts))
    return d + ("Z" if closed else "")


def ell_pts(cx, cy, rx, ry, tilt, t0, t1, step=4.0):
    """Points along a tilted ellipse, parameter t in degrees."""
    m = axis((cx, cy), tilt)
    n = max(2, int(abs(t1 - t0) / step))
    return [m(rx * math.cos(math.radians(t0 + (t1 - t0) * i / n)), ry * math.sin(math.radians(t0 + (t1 - t0) * i / n)))
            for i in range(n + 1)]


def tilted_ellipse(cx, cy, rx, ry, tilt):
    return pts_d(ell_pts(cx, cy, rx, ry, tilt, 0, 360, 6)[:-1], closed=True)


def lens(cx, cy, rx, ry, tilt, S, rt=None):
    """Lens (two arcs meeting in tips): pointed tips in Line, softened tips in Rounded."""
    m = axis((cx, cy), tilt)
    r = L(S, 0, 1.2) if rt is None else rt
    # circle arc through the tips (+-rx, 0) and the crown (0, -ry)
    R = (rx * rx + ry * ry) / (2 * ry)
    top, bot = [], []
    a0 = math.degrees(math.asin(rx / R))
    n = 16
    for i in range(n + 1):
        a = -a0 + 2 * a0 * i / n
        x, y = R * math.sin(math.radians(a)), -(R * math.cos(math.radians(a)) - (R - ry))
        top.append((x, y))
    bot = [(x, -y) for x, y in top[::-1]]
    pts = top[:-1] + bot[:-1]
    return poly([m(x, y) for x, y in pts], closed=True, r=r)


def dashes(pts, on=2.0, off=2.0, phase=0.0):
    """Cut a polyline into dash segments (list of d-strings)."""
    out, cur, pos, draw = [], [], -phase, True
    seglen = on
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        ln = math.hypot(x1 - x0, y1 - y0)
        t = 0.0
        while t < ln:
            need = seglen - pos
            step = min(need, ln - t)
            a = (x0 + (x1 - x0) * t / ln, y0 + (y1 - y0) * t / ln)
            b = (x0 + (x1 - x0) * (t + step) / ln, y0 + (y1 - y0) * (t + step) / ln)
            if draw:
                if not cur:
                    cur = [a]
                cur.append(b)
            t += step
            pos += step
            if pos >= seglen - 1e-9:
                if draw and len(cur) > 1:
                    out.append(pts_d(cur))
                cur = []
                draw = not draw
                seglen = on if draw else off
                pos = 0.0
    if draw and len(cur) > 1:
        out.append(pts_d(cur))
    return out


def arc_pts(cx, cy, r, a0, a1, step=4.0):
    n = max(2, int(abs(a1 - a0) / step))
    return [polar(cx, cy, r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]


def spark(cx, cy, ro, ri=None, S=None, rot=0.0):
    """Four-point sparkle star (a bright star point)."""
    ri = ro * 0.36 if ri is None else ri
    pts = [polar(cx, cy, ro if i % 2 == 0 else ri, -90 + rot + i * 45) for i in range(8)]
    return poly(pts, closed=True, r=0 if S is None else L(S, 0, 0.5))


def star5(cx, cy, ro, ri=None, S=None):
    ri = ro * 0.45 if ri is None else ri
    pts = [polar(cx, cy, ro if i % 2 == 0 else ri, -90 + i * 36) for i in range(10)]
    return poly(pts, closed=True, r=0 if S is None else L(S, 0, 0.4))


def arrow_head(tip, deg, size=2.0):
    """Open arrowhead at `tip` pointing along `deg`."""
    a = polar(tip[0], tip[1], size * 1.414, deg + 135)
    b = polar(tip[0], tip[1], size * 1.414, deg - 135)
    return poly([a, tip, b])


def lumpy(cx, cy, radii, rot=0.0):
    """Irregular rock outline from a list of radii (evenly spaced angles)."""
    n = len(radii)
    return [polar(cx, cy, r, rot + i * 360 / n) for i, r in enumerate(radii)]


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


def rock(cx, cy, radii, rot, S):
    """Lumpy rock: angular in Line, smooth in Rounded."""
    pts = lumpy(cx, cy, radii, rot)
    return poly(pts, closed=True) if S.name == "line" else smooth_closed(pts)


def gap_cut(d, w):
    """Region of a stroke of width w along d (used to cut clean gaps)."""
    return ST(d, w, "round", "round")


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


def outside(pts, circles):
    """Runs of a polyline that stay clear of the given (cx, cy, r) circles."""
    return runs(pts, lambda p: all(math.hypot(p[0] - c[0], p[1] - c[1]) > c[2] for c in circles))


def drop(tip, cx, cy, r, S):
    """Teardrop: circle (cx, cy, r) drawn out to a tip point; tip sharp in Line, soft in Rounded."""
    dx, dy = tip[0] - cx, tip[1] - cy
    dd = math.hypot(dx, dy)
    base = math.degrees(math.atan2(dy, dx))
    off = math.degrees(math.acos(r / dd))
    p1, p2 = polar(cx, cy, r, base + off), polar(cx, cy, r, base - off)
    body = f"M{fmt(p1[0])} {fmt(p1[1])}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(p2[0])} {fmt(p2[1])}"
    rr = L(S, 0, 1.5)
    if rr == 0:
        return body + f"L{fmt(tip[0])} {fmt(tip[1])}Z"
    t = rr / math.hypot(tip[0] - p2[0], tip[1] - p2[1])
    s = (tip[0] + (p2[0] - tip[0]) * t, tip[1] + (p2[1] - tip[1]) * t)
    e = (tip[0] + (p1[0] - tip[0]) * t, tip[1] + (p1[1] - tip[1]) * t)
    return body + f"L{fmt(s[0])} {fmt(s[1])}Q{fmt(tip[0])} {fmt(tip[1])} {fmt(e[0])} {fmt(e[1])}Z"


# ============================================================================ stars and deep sky

@icon("brown-dwarf", CAT, "Brown dwarf: a dim banded ball with a faint glow, bigger than a planet but too small to be a star",
      tags=["failed star", "substellar object", "star", "astronomy", "infrared", "deep space"])
def _(S):
    cx, cy, r = 12, 13.5, 6.25
    glow = [line(seg(*polar(cx, cy, 8.5, a), *polar(cx, cy, 10.25, a))) for a in (-160, -125, -90, -55, -20)]
    return [
        shell(circle(cx, cy, r)),
        detail("M6.4 11.5C9 10.7 15 10.7 17.6 11.5"),
        detail("M6.4 15.5C9 16.3 15 16.3 17.6 15.5"),
        *glow,
    ]


@icon("protoplanetary-disk", CAT, "Young star glowing inside a flat disk of dust with a gap ring",
      tags=["planet formation", "dust disk", "young star", "accretion disk", "astronomy", "stellar nursery"],
      aliases=["protoplanetary-disc"])
def _(S):
    tilt = -12
    star = spark(12, 12, 6.5, 1.6, S)
    ring = D(P(tilted_ellipse(12, 12, 10, 4.5, tilt)), P(tilted_ellipse(12, 12, 6.75, 2.6, tilt)),
             ST(star, 4, "round", "round"))
    return [shell(path_to_d(ring)), Part("dot", star)]


@icon("star-lifecycle", CAT, "Life cycle of a star: a small star swelling into a red giant and ending as a tiny dwarf",
      tags=["stellar evolution", "red giant", "white dwarf", "star life", "astronomy", "sun"])
def _(S):
    return [
        shell(circle(5, 14.5, 2.25)),
        shell(circle(12.5, 8, 5)),
        dot(19.75, 14.5, 1.6),
        line(seg(4, 20, 19, 20)),
        line(arrow_head((20, 20), 0, 1.7)),
    ]


def mirror_v(d, cy=12.0):
    from geometry import transform_path
    return path_to_d(transform_path(P(d), (1, 0, 0, -1, 0, 2 * cy)))


def mirror_h(d, cx=12.0):
    from geometry import transform_path
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 2 * cx, 0)))


@icon("bipolar-nebula", CAT, "Bipolar nebula: two gas lobes blown out from a bright central star, like an hourglass",
      tags=["nebula", "hourglass nebula", "butterfly nebula", "planetary nebula", "astronomy", "deep sky"])
def _(S):
    if S.name == "line":
        top = "M12 9.5L7 7L4.5 4L7 2.5L12 3.5L17 2.5L19.5 4L17 7Z"
    else:
        top = ("M12 9.5C9 8.5 5 7 4.5 4.5C4.2 2.8 6 2 8.5 2.6C10 3 11 3.3 12 3.6"
               "C13 3.3 14 3 15.5 2.6C18 2 19.8 2.8 19.5 4.5C19 7 15 8.5 12 9.5Z")
    return [shell(top), shell(mirror_v(top)), dot(12, 12, 1.25), line(seg(5.5, 12, 9, 12)), line(seg(15, 12, 18.5, 12))]


@icon("supernova-remnant", CAT, "Supernova remnant: a broken shell of gas expanding around the small core left by an exploded star",
      tags=["supernova", "remnant", "exploded star", "shock wave", "nebula", "astronomy"])
def _(S):
    frags = [(9.5, -120, -70), (7, -95, -40), (9.5, -45, 5), (6.75, -10, 40), (9.25, 25, 80), (7.25, 60, 115),
             (9.5, 100, 150), (6.75, 135, 185), (9.25, 170, 220), (7, 205, 250)]
    return [line(arc(12, 12, r, a0, a1)) for r, a0, a1 in frags] + [dot(12, 12, 1.1)]


@icon("nebula-pillars", CAT, "Tall pillars of gas and dust rising in a nebula, with young stars around them",
      tags=["pillars of creation", "nebula", "gas column", "star forming region", "astronomy", "deep sky"])
def _(S):
    pts = [(3, 21), (3.5, 13), (4.5, 7.5), (6.5, 5), (8.5, 6.5), (8.8, 10), (9.4, 15.5), (10, 14), (11.5, 10.5),
           (13.5, 11), (14, 14), (14.9, 18.2), (15.5, 17), (17, 14.5), (19, 15), (19.5, 18), (21, 21)]
    return [
        shell(poly(pts, closed=True, r=L(S, 0, 1.2))),
        dot(14.5, 5, 1.2), dot(19.5, 9, 1.2), dot(18, 3.5, 0.9),
    ]


@icon("lenticular-galaxy", CAT, "Lenticular galaxy: a lens-shaped disk with a bright bulge and no spiral arms",
      tags=["galaxy", "s0 galaxy", "lens galaxy", "disk galaxy", "astronomy", "deep sky"])
def _(S):
    disk = lens(12, 12, 10, 2.2, -25, S, L(S, 0, 1.2))
    bulge = tilted_ellipse(12, 12, 5, 4, -25)
    return [shell(union(disk, bulge)), dot(12, 12, 1.6)]


@icon("irregular-galaxy", CAT, "Irregular galaxy: a shapeless clump of stars and gas clouds with no arms",
      tags=["galaxy", "dwarf galaxy", "magellanic cloud", "star cloud", "astronomy", "deep sky"])
def _(S):
    pts = [(4, 10), (7, 5.5), (11, 6.5), (14, 3.5), (18.5, 5.5), (20, 10), (18, 13.5), (20.5, 17.5), (16, 20.5),
           (11.5, 18), (7, 20), (3.5, 16)]
    outline = poly(pts, closed=True, r=L(S, 0, 2)) if S.name == "line" else smooth_closed(pts, 0.8)
    return [
        shell(outline),
        dot(8.5, 10.5, 1.5), dot(15.5, 8.5, 1.2), dot(12.5, 13, 1.7), dot(16.5, 15.5, 1.1), dot(8, 15.5, 1.1),
    ]


@icon("ring-galaxy", CAT, "Ring galaxy: a bright ring of stars around an empty gap with a small core",
      tags=["galaxy", "collisional ring", "hoag's object", "cartwheel galaxy", "astronomy", "deep sky"])
def _(S):
    ring = minus(tilted_ellipse(12, 12, 10, 7.5, -15), tilted_ellipse(12, 12, 6.25, 4, -15))
    core = Part("dot", spark(12, 12, 2.2, 0.9, S)) if S.name == "line" else dot(12, 12, 1.5)
    return [shell(ring), core]


@icon("edge-on-galaxy", CAT, "Spiral galaxy seen edge on: a thin disk with a central bulge and a dark dust lane",
      tags=["galaxy", "edge on", "dust lane", "sombrero", "disk galaxy", "astronomy"])
def _(S):
    disk = lens(12, 12, 9.75, 2.4, 0, S, L(S, 0, 1.2))
    bulge = ellipse(12, 12, 4.25, 4)
    return [shell(union(disk, bulge)), detail(seg(6, 12, 18, 12))]


@icon("galaxy-cluster", CAT, "Galaxy cluster: a large galaxy with smaller galaxies grouped around it",
      tags=["cluster", "galaxy group", "galaxies", "supercluster", "astronomy", "deep sky"])
def _(S):
    def small(cx, cy, tilt):
        return shell(lens(cx, cy, 2.6, 1.4, tilt, S, 0) if S.name == "line" else tilted_ellipse(cx, cy, 2.4, 1.4, tilt))
    return [
        shell(tilted_ellipse(12, 12, 4.5, 3, -20)),
        dot(12, 12, 1.1),
        small(5, 5, 30), small(19, 5.5, -40), small(5.5, 18.5, -10), small(18.5, 18.5, 35),
        dot(12, 4, 1), dot(12, 20, 1),
    ]


_WEB = [(7.5, 8), (15, 6.5), (18, 13.5), (11.5, 16.5), (5, 14.5)]
_WEB_OUT = [(3, 3), (16, 2), (22, 12.5), (12.5, 22), (2, 20)]


@icon("cosmic-web", CAT, "Cosmic web: glowing filaments linking knots of galaxies into a vast net",
      tags=["large scale structure", "filaments", "dark matter", "universe", "cosmology", "astronomy"])
def _(S):
    out = []
    n = len(_WEB)
    for i in range(n):
        out.append(line(seg(*_WEB[i], *_WEB[(i + 1) % n])))
        out.append(line(seg(*_WEB[i], *_WEB_OUT[i])))
    for i, (x, y) in enumerate(_WEB):
        out.append(dot(x, y, 2.4 if i in (0, 2) else 1.8))
    return out


def _mini_spiral(cx, cy, r):
    return [line(arc(cx, cy, r, 180, 360)), line(arc(cx + r * 0.45, cy, r * 0.55, 0, 180))]


@icon("multiverse", CAT, "Multiverse: a cluster of bubble universes, each holding its own galaxy",
      tags=["parallel universes", "bubble universes", "cosmology", "universe", "sci-fi", "theory"])
def _(S):
    return [
        shell(circle(9, 14.5, 6.25)),
        shell(circle(17.75, 6.25, 3.75)),
        shell(circle(18.75, 17.25, 2.75)),
        *[p for p in [detail(arc(9, 14.5, 2.75, 180, 360)), detail(arc(10.25, 14.5, 1.5, 0, 180))]],
        dot(17.75, 6.25, 1.2),
        dot(18.75, 17.25, 0.9),
    ]


@icon("observable-universe", CAT, "Observable universe: an observer at the centre of nested shells of galaxies",
      tags=["cosmology", "universe", "cosmic horizon", "light horizon", "observer", "astronomy"])
def _(S):
    ring_dots = [dot(*polar(12, 12, 6.25, a), 1.05) for a in range(0, 360, 36)]
    eye = lens(12, 12, 3, 1.9, 0, S, L(S, 0, 0.8))
    return [line(circle(12, 12, 9.5)), *ring_dots, shell(eye)]


@icon("time-dilation", CAT, "Time dilation: a stretched clock beside a heavy mass bending space",
      tags=["relativity", "spacetime", "gravity well", "slow time", "einstein", "physics"])
def _(S):
    return [
        shell(ellipse(7, 8, 4, 5.5)),
        detail(poly([(7, 5.25), (7, 8), (8.75, 9.5)], r=S.r * 0.4)),
        shell(circle(17, 9.5, 3.5)),
        line("M2 17H6.5C10 17 11.5 20.5 15 20.5H17C19 20.5 20.5 17 22 17"),
    ]


def wave_pts(p0, p1, amp, waves, n=36, taper=None):
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


@icon("spaghettification", CAT, "Spaghettification: an object stretched into a thin wavy strand as it falls into a black hole",
      tags=["black hole", "tidal force", "gravity", "event horizon", "stretching", "astrophysics"])
def _(S):
    strand = wave_pts((2.5, 2.5), (11.25, 11.25), 1.6, 2.5, 40, lambda t: 1 - 0.75 * t)
    return [
        dot(15, 15, 3.25),
        line(arc(15, 15, 6.5, 250, 200)),
        line(pts_d(strand)),
    ]


@icon("hr-diagram", CAT, "Hertzsprung-Russell diagram: stars plotted as a diagonal main sequence with giants in a clump",
      tags=["hertzsprung russell", "main sequence", "star chart", "stellar classification", "astronomy", "plot"],
      aliases=["hertzsprung-russell-diagram"])
def _(S):
    return [
        line(poly([(3, 2.5), (3, 21), (21.5, 21)], r=S.r)),
        dot(7, 6, 1.7), dot(9.75, 9.25, 1.45), dot(12.25, 12.25, 1.3), dot(14.75, 15, 1.1), dot(17.25, 17.25, 0.95),
        dot(16, 5.5, 1.6), dot(19.5, 5, 1.3), dot(18.25, 8.75, 1.3),
        dot(7.25, 17, 0.9),
    ]


@icon("stellar-magnitude-scale", CAT, "Stellar magnitude scale: stars shrinking from bright to faint above a ruler",
      tags=["magnitude", "brightness", "apparent magnitude", "star brightness", "astronomy", "scale"])
def _(S):
    xs = (6, 13, 18.75)
    return [
        Part("dot", spark(6, 9.5, 4.25, 1.3, S)),
        Part("dot", spark(13, 10.25, 3.25, 1.0, S)),
        Part("dot", spark(18.75, 11, 2.1, 0.75, S)),
        line(seg(3, 17.5, 21, 17.5)),
        *[line(seg(x, 17.5, x, 20.5)) for x in xs],
    ]


@icon("interstellar-object", CAT, "Interstellar object: a long cigar-shaped rock tumbling through space with a motion trail",
      tags=["interstellar visitor", "oumuamua", "asteroid", "comet", "rock", "astronomy"])
def _(S):
    m = axis((14.5, 9.5), -35)
    pts = [m(x, y) for x, y in [(-7, 0), (-5.5, -1.9), (-2, -2.5), (2, -2.3), (5.5, -1.8), (7, 0.2), (5.5, 2), (1.5, 2.4),
                                (-2.5, 2.3), (-5.5, 1.8)]]
    body = poly(pts, closed=True, r=0.6) if S.name == "line" else smooth_closed(pts, 0.8)
    return [
        shell(body),
        line(seg(*m(-9.5, 0), *m(-15.5, 0))),
        line(seg(*m(-8.5, 3.75), *m(-12, 3.75))),
        line(seg(*m(-8.5, -3.75), *m(-12, -3.75))),
    ]


@icon("hot-jupiter", CAT, "Hot Jupiter: a large banded gas giant orbiting very close to its star, with heat between them",
      tags=["exoplanet", "gas giant", "close orbit", "hot planet", "astronomy", "star"])
def _(S):
    heat = wave_pts((8.5, 6.5), (8.5, 17.5), 0.9, 2, 32)
    return [
        line(arc(-3, 12, 8.5, -50, 50)),
        line(pts_d(heat)),
        shell(circle(16.75, 12, 5.25)),
        detail("M11.9 10H21.6"),
        detail("M11.9 14H21.6"),
    ]


@icon("lava-planet", CAT, "Lava planet: a world covered in glowing cracks of molten rock",
      tags=["molten planet", "volcanic world", "exoplanet", "magma", "hot planet", "astronomy"])
def _(S):
    k = S.r * 0.3
    return [
        shell(circle(12, 12, 9)),
        detail(poly([(3.5, 11), (7, 10), (9, 12.5), (12.5, 11), (15, 7), (17, 4.5)], r=k)),
        detail(poly([(9, 12.5), (8, 16), (10, 19.5), (9.5, 21)], r=k)),
        detail(poly([(12.5, 11), (16.5, 13.5), (20.5, 13)], r=k)),
    ]


@icon("ocean-planet", CAT, "Ocean planet: a world covered entirely in water waves with no land",
      tags=["water world", "exoplanet", "ocean", "sea", "waves", "astronomy"])
def _(S):
    out = [shell(circle(12, 12, 9))]
    for y in (8, 12, 16):
        hw = math.sqrt(81 - (y - 12) ** 2) - 2.5
        out.append(detail(pts_d(wave_pts((12 - hw, y), (12 + hw, y), 0.9, 2 if y == 12 else 1.5, 30))))
    return out


@icon("oort-cloud", CAT, "Oort cloud: a small sun and its orbit inside a vast spherical shell of icy bodies",
      tags=["comet cloud", "solar system", "icy bodies", "outer solar system", "comets", "astronomy"])
def _(S):
    shell_dashes = [line(arc(12, 12, 9.25, a, a + 6)) for a in range(0, 360, 20)]
    return [*shell_dashes, line(tilted_ellipse(12, 12, 5.25, 2.6, -20)), dot(12, 12, 1.6)]


@icon("io-moon", CAT, "Io: a volcanic moon with a plume of gas arching off its edge",
      tags=["io", "jupiter moon", "volcano", "volcanic moon", "plume", "astronomy"])
def _(S):
    c, r, a = (10.5, 13.5), 7.75, -45
    p = polar(*c, r + 1.5, a)
    return [
        shell(circle(*c, r)),
        dot(8, 11, 1.4), dot(12.5, 17, 1.6), dot(6.75, 16, 0.9), dot(13.5, 10.5, 0.9),
        line(arc(*polar(*c, r + 0.5, a), 4, a - 80, a + 80)),
        line(seg(*p, *polar(*c, r + 3.75, a))),
    ]


@icon("europa-moon", CAT, "Europa: an icy moon crossed by long crisscrossing crack lines",
      tags=["europa", "jupiter moon", "ice moon", "ocean moon", "cracks", "astronomy"])
def _(S):
    if S.name == "line":
        cracks = [poly([(3.5, 9), (8, 10), (13, 8.5), (20.5, 9.5)]), poly([(4, 16), (9, 14), (14, 16.5), (20, 15)]),
                  poly([(8.5, 3.8), (10.5, 9.5), (12.5, 15), (16.5, 20.2)])]
    else:
        cracks = ["M3.5 9C8.5 11 14.5 7.5 20.5 9.5", "M4 16C9 13.5 14 17.5 20 15", "M8.5 3.8C10.5 9.5 12 15 16.5 20.2"]
    return [shell(circle(12, 12, 9)), *[detail(c) for c in cracks]]


@icon("enceladus-geysers", CAT, "Enceladus: a small icy moon with jets of water spray fanning from its south pole",
      tags=["enceladus", "saturn moon", "geyser", "ice plume", "cryovolcano", "astronomy"])
def _(S):
    c, r, pole = (13.5, 9.5), 7, 125
    jets = []
    for d, ln in ((-42, 4), (-14, 5.5), (14, 5.5), (42, 4)):
        s = polar(*c, r + 2, pole + d * 0.45)
        jets.append(line(seg(*s, *polar(*s, ln, pole + d))))
    return [shell(circle(*c, r)), *jets]


@icon("binary-asteroid", CAT, "Binary asteroid: a small moonlet orbiting a larger lumpy asteroid",
      tags=["double asteroid", "moonlet", "asteroid", "orbit", "space rock", "astronomy"])
def _(S):
    big = (11.5, 12.5)
    small = ell_pts(big[0], big[1], 9.5, 6.5, -20, -55, -55)[0]
    orbit = ell_pts(big[0], big[1], 9.5, 6.5, -20, -55, 305, 2)
    keep = outside(orbit, [(small[0], small[1], 4.5)])
    ds = [d for rn in keep for d in dashes(rn, 1.5, 2.1)]
    return [
        shell(rock(big[0], big[1], [4.4, 3.8, 4.6, 3.9, 4.3, 3.6, 4.5, 4], 10, S)),
        shell(rock(small[0], small[1], [2.4, 2, 2.5, 2.1, 2.3], 0, S)),
        *[line(d) for d in ds],
    ]


@icon("comet-nucleus", CAT, "Comet nucleus: a lumpy icy rock venting small jets of gas",
      tags=["comet", "nucleus", "icy rock", "outgassing", "jets", "astronomy"])
def _(S):
    a = lumpy(9.5, 14.5, [5, 4.4, 5.1, 4.6, 4.9, 4.3, 5, 4.5], 0)
    b = lumpy(15, 10, [3.6, 3.2, 3.8, 3.3, 3.5, 3.1], 20)
    if S.name == "line":
        body = union(poly(a, closed=True), poly(b, closed=True))
    else:
        body = union(smooth_closed(a), smooth_closed(b))
    return [
        shell(body),
        dot(8.5, 15, 1.3),
        line(seg(18.5, 5.5, 20.5, 3.5)), line(seg(20, 8.5, 22, 7.5)), line(seg(15.5, 4.25, 16.25, 2)),
    ]


@icon("near-earth-asteroid", CAT, "Near-Earth asteroid: a space rock on a path that swings close past Earth",
      tags=["neo", "asteroid", "near miss", "flyby", "planetary defense", "astronomy"])
def _(S):
    def bez(t, p0=(16, 8.5), p1=(13, 13), p2=(15, 18), p3=(20.5, 20.5)):
        u = 1 - t
        return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])
    path = dashes([bez(i / 30) for i in range(31)], 1.75, 2)
    return [
        shell(circle(7, 15, 5)),
        detail("M2.5 13.5C5.5 15 8.5 15 11.8 13.2"),
        shell(rock(18.5, 5, [3, 2.5, 3.1, 2.6, 2.9, 2.4, 3], 10, S)),
        *[line(d) for d in path],
    ]


# ============================================================================ sky events and the sun

def _crescent(cx, cy, r, ox, oy, r2):
    return minus(circle(cx, cy, r), circle(cx + ox, cy + oy, r2))


@icon("planetary-alignment", CAT, "Planetary alignment: planets lined up in a row beside the sun",
      tags=["planet parade", "alignment", "syzygy", "solar system", "planets", "astronomy"], aliases=["planet-parade"])
def _(S):
    sun = inter(circle(-1.5, 12, 7.5), rect(2.5, 0, 20, 24))
    rays = [line(seg(*polar(-1.5, 12, 9.25, a), *polar(-1.5, 12, 11, a))) for a in (-52, -28, 28, 52)]
    return [shell(sun), *rays, dot(10, 12, 1.25), shell(circle(14.5, 12, 2)), dot(19.75, 12, 1.75)]


@icon("planetary-conjunction", CAT, "Planetary conjunction: two bright planets appearing close together beside the crescent moon",
      tags=["conjunction", "planets", "crescent moon", "night sky", "stargazing", "astronomy"])
def _(S):
    return [
        shell(_crescent(9.5, 12.5, 7.5, 4, -3, 6.5)),
        Part("dot", spark(17.5, 7, 3, 1, S)),
        Part("dot", spark(20, 12.5, 2.25, 0.8, S)),
    ]


@icon("retrograde-motion", CAT, "Retrograde motion: a planet's path across the stars looping back on itself",
      tags=["retrograde", "apparent motion", "planet path", "mercury retrograde", "astrology", "astronomy"])
def _(S):
    path = "M2.5 18.5C7.5 16.5 11 9.5 14.5 9.5C17.5 9.5 18 14.5 15 14.5C12 14.5 12 8.5 19.5 6.25"
    return [line(path), line(arrow_head((21, 5.75), -18, 2)), dot(5.5, 5, 1.1), dot(20.5, 19, 1.1), dot(9.5, 20.5, 0.9)]


@icon("occultation", CAT, "Occultation: the moon sliding in front of a bright star and hiding it",
      tags=["lunar occultation", "star", "moon", "eclipse", "transit", "astronomy"])
def _(S):
    moon = (10, 11.5)
    star = spark(18, 5.5, 4.25, 1.35, S)
    star_cut = path_to_d(D(P(star), P(circle(*moon, 8.75))))
    return [
        shell(circle(*moon, 6)),
        Part("dot", star_cut),
        line(seg(4.5, 20.5, 15, 20.5)),
        line(arrow_head((16.5, 20.5), 0, 1.75)),
    ]


@icon("eclipse-diamond-ring", CAT, "Diamond ring effect: the dark moon ringed by light with one bright bead flashing at its edge",
      tags=["solar eclipse", "totality", "diamond ring", "baily's beads", "corona", "astronomy"])
def _(S):
    c, r, a = (11, 13), 8, -45
    bead = polar(*c, r, a)
    return [
        dot(*c, 5.5),
        line(arc(*c, r, a + 28, a - 28)),
        Part("dot", spark(*bead, 4.5, 1.4, S)),
    ]


@icon("umbra-penumbra", CAT, "Umbra and penumbra: the sun, moon and Earth in a row with the moon's dark shadow cones",
      tags=["shadow", "eclipse diagram", "umbra", "penumbra", "sun moon earth", "astronomy"])
def _(S):
    return [
        shell(circle(4.5, 12, 2.75)),
        dot(11, 12, 1.6),
        shell(circle(19.5, 12, 2.5)),
        solid(poly([(12.75, 10.75), (17, 12), (12.75, 13.25)], closed=True)),
        line(seg(13, 9.5, 21.5, 6)),
        line(seg(13, 14.5, 21.5, 18)),
    ]


@icon("coronal-mass-ejection", CAT, "Coronal mass ejection: the sun blasting a cloud of plasma toward Earth and its magnetic shield",
      tags=["cme", "solar storm", "space weather", "solar flare", "geomagnetic storm", "sun"])
def _(S):
    blob = ("M5.25 8.25C7.5 6.25 10.5 5.75 12 7.25C14 6.25 16 8.25 15 10.25C16.5 11.75 16 14.25 14 14.5"
            "C13.5 16.5 10.5 17.5 9 16C7.5 16.75 6 16 5.25 15.25")
    return [
        line(arc(-3, 12, 8.5, -50, 50)),
        line(blob),
        dot(20.25, 12, 1.75),
        line(arc(20.25, 12, 4.25, 130, 230)),
    ]


@icon("heliosphere", CAT, "Heliosphere: the sun inside a comet-shaped bubble of solar wind with a bow shock in front",
      tags=["solar wind", "bow shock", "heliopause", "interstellar space", "sun", "astronomy"])
def _(S):
    return [
        shell(drop((22, 12), 11.5, 12, 4.75, S)),
        dot(11.5, 12, 1.6),
        line(arc(11.5, 12, 8.5, 125, 235)),
    ]


def _field(Lv, R, side):
    """Dipole field line r = L sin^2(theta) on one side of Earth, clear of radius R."""
    t0 = math.asin(math.sqrt(R / Lv))
    n = 30
    out = []
    for i in range(n + 1):
        th = t0 + (math.pi - 2 * t0) * i / n
        s = math.sin(th)
        r = Lv * s * s
        out.append((12 + side * r * s, 12 - r * math.cos(th)))
    return pts_d(out)


@icon("radiation-belts", CAT, "Radiation belts: Earth wrapped in two nested rings of trapped charged particles",
      tags=["van allen belts", "magnetosphere", "earth", "charged particles", "space weather", "astronomy"])
def _(S):
    return [
        shell(circle(12, 12, 3)),
        *[line(_field(Lv, 5.5, s)) for s in (-1, 1) for Lv in (6.75, 10)],
    ]


@icon("moonbow", CAT, "Moonbow: a faint rainbow made by moonlight over a waterfall, under a crescent moon",
      tags=["lunar rainbow", "rainbow", "moon", "waterfall", "night", "weather"], aliases=["lunar-rainbow"])
def _(S):
    return [
        line(arc(12, 19.5, 9.5, 180, 360)),
        line(arc(12, 19.5, 6, 180, 360)),
        line(seg(10, 16.5, 10, 21)), line(seg(14, 16.5, 14, 21)),
        shell(_crescent(18.5, 4.75, 2.75, 1.6, -1.2, 2.4)),
    ]


@icon("earthshine", CAT, "Earthshine: a thin bright crescent moon with the rest of its disk faintly lit",
      tags=["ashen glow", "crescent moon", "moon", "da vinci glow", "night sky", "astronomy"])
def _(S):
    cres = _crescent(12, 12, 9, 4.5, 0, 8.5)
    rest = dashes(arc_pts(12, 12, 9, -62, 62, 2), 2.2, 2.2, 0.8)
    return [shell(cres), *[line(d) for d in rest]]


# ============================================================================ orbits and trajectories

@icon("transfer-orbit", CAT, "Transfer orbit: a half-ellipse path carrying a spacecraft from a low orbit to a higher one",
      tags=["hohmann transfer", "orbit change", "trajectory", "orbital maneuver", "spaceflight", "astronomy"],
      aliases=["hohmann-transfer"])
def _(S):
    rin, rout = 4.5, 9.5
    cx = 12 + (rin - rout) / 2
    rx, ry = (rin + rout) / 2, math.sqrt(rin * rout)
    path = [(cx + rx * math.cos(math.radians(-t)), 12 + ry * math.sin(math.radians(-t))) for t in range(0, 181, 5)]
    return [
        dot(12, 12, 1.5),
        line(circle(12, 12, rin)),
        line(pts_d(path)),
        line(arc(12, 12, rout, 20, 160)),
        line(arrow_head(path[18], 180, 1.75)),
    ]


@icon("orbital-inclination", CAT, "Orbital inclination: an orbit tilted against a flat reference plane, with the angle marked",
      tags=["inclination", "orbit tilt", "orbital plane", "angle", "orbit", "astronomy"])
def _(S):
    tilt = -28
    orbit = ell_pts(12, 12, 10, 3.5, tilt, 0, 360, 3)
    plane = [(2.5, 12), (21.5, 12)]
    return [
        dot(12, 12, 2),
        line(pts_d(orbit)),
        *[line(d) for d in dashes(plane, 1.5, 2)],
        line(arc(12, 12, 6.5, tilt + 4, -4)),
    ]


@icon("apogee-perigee", CAT, "Apogee and perigee: the nearest and farthest points of an elliptical orbit around Earth",
      tags=["apogee", "perigee", "elliptical orbit", "orbit", "closest approach", "astronomy"])
def _(S):
    rx, ry = 9.5, 7.5
    c = math.sqrt(rx * rx - ry * ry)
    ex = 12 - c
    pts = ell_pts(12, 12, rx, ry, 0, 0, 360, 3)
    keep = outside(pts, [(2.5, 12, 3.2), (21.5, 12, 3.2)])
    return [
        *[line(pts_d(rn)) for rn in keep],
        shell(circle(ex, 12, 2)),
        dot(2.5, 12, 1.6), dot(21.5, 12, 1.6),
        *[line(d) for d in dashes([(ex + 3.5, 12), (18.5, 12)], 1.5, 1.75)],
    ]


def _satellite(cx, cy, deg, S, span=4.5):
    """Tiny satellite: square body with two solid panels running along `deg`."""
    m = axis((cx, cy), deg)
    p1 = [m(2.4, -1.5), m(span, -1.5), m(span, 1.5), m(2.4, 1.5)]
    p2 = [m(-span, -1.5), m(-2.4, -1.5), m(-2.4, 1.5), m(-span, 1.5)]
    body = [m(-1.4, -1.4), m(1.4, -1.4), m(1.4, 1.4), m(-1.4, 1.4)]
    return [Part("dot", poly(body, closed=True)), solid(poly(p1, closed=True)), solid(poly(p2, closed=True))]


@icon("geostationary-orbit", CAT, "Geostationary orbit: a satellite on a wide ring that stays fixed above one spot on Earth",
      tags=["geostationary", "geosynchronous", "satellite", "communications satellite", "orbit", "earth"],
      aliases=["geosynchronous-orbit"])
def _(S):
    c, r = (12, 12.75), 8.75
    return [
        shell(circle(*c, 3)),
        line(arc(*c, r, -90 + 44, -90 - 44)),
        *_satellite(12, c[1] - r, 0, S, 6),
        line(seg(12, 6.5, 12, 8.25)),
    ]


def split_inside(pts, c, r):
    """Split a polyline into runs inside and outside the circle (c, r)."""
    ins = runs(pts, lambda p: math.hypot(p[0] - c[0], p[1] - c[1]) < r)
    outs = runs(pts, lambda p: math.hypot(p[0] - c[0], p[1] - c[1]) >= r)
    return ins, outs


@icon("polar-orbit", CAT, "Polar orbit: an orbit ring that passes over Earth's north and south poles",
      tags=["polar orbit", "sun synchronous", "satellite orbit", "earth observation", "orbit", "earth"])
def _(S):
    c, r = (12, 12), 5.75
    front = ell_pts(*c, 3.25, 10, 15, -90, 90, 3)
    back = ell_pts(*c, 3.25, 10, 15, 90, 270, 3)
    ins, outs = split_inside(front, c, r + 1)
    back_outs = outside(back, [(c[0], c[1], r + 2.5)])
    return [
        shell(circle(*c, r)),
        detail(seg(6.25, 12, 17.75, 12)),
        *[detail(pts_d(rn)) for rn in ins],
        *[line(pts_d(rn)) for rn in outs + back_outs],
    ]


def _spiral_pts(cx, cy, r0, r1, a0, a1, n=40):
    return [polar(cx, cy, r0 + (r1 - r0) * i / n, a0 + (a1 - a0) * i / n) for i in range(n + 1)]


@icon("orbital-decay", CAT, "Orbital decay: a satellite spiralling inward toward a planet on a tightening path",
      tags=["decaying orbit", "reentry", "atmospheric drag", "satellite", "spiral", "orbit"])
def _(S):
    c = (12.5, 13)
    sp = _spiral_pts(*c, 8.75, 5.25, -60, 250, 48)
    tip = sp[-1]
    ang = math.degrees(math.atan2(tip[1] - sp[-2][1], tip[0] - sp[-2][0]))
    sat = polar(*c, 8.75, -60)
    return [
        shell(circle(*c, 2.75)),
        line(pts_d(sp[5:-1])),
        line(arrow_head(tip, ang, 1.5)),
        dot(*sat, 1.9),
    ]


@icon("equal-area-orbit", CAT, "Kepler's second law: an elliptical orbit around the sun with two wedges of equal area",
      tags=["kepler's law", "second law", "equal areas", "elliptical orbit", "orbital mechanics", "physics"],
      aliases=["keplers-second-law"])
def _(S):
    rx, ry = 10, 7.5
    c = math.sqrt(rx * rx - ry * ry)
    sun = (12 - c, 12)
    near = [sun] + ell_pts(12, 12, rx, ry, 0, 138, 222, 6)
    far = [sun] + ell_pts(12, 12, rx, ry, 0, -17, 17, 4)
    k = L(S, 0, 0.9)
    return [
        line(ellipse(12, 12, rx, ry)),
        dot(*sun, 1.4),
        solid(poly(near, closed=True, r=k)),
        solid(poly(far, closed=True, r=k)),
    ]


@icon("escape-velocity", CAT, "Escape velocity: thrown objects fall back to a planet while one arrow flies free into space",
      tags=["escape speed", "gravity", "launch", "orbital mechanics", "physics", "trajectory"])
def _(S):
    ground = inter(circle(12, 31, 12), rect(1.5, 0, 21, 21.5))
    return [
        shell(ground),
        line("M9.5 17.5C8.5 13 6 12 4.5 16.25"),
        line("M11 17C10.5 8 5.5 5.5 3 10.5"),
        line(seg(13.5, 16.5, 20, 4)),
        line(arrow_head((20.5, 3), -62.5, 2)),
    ]


@icon("tidal-bulge", CAT, "Tidal bulge: Earth with its oceans pulled into bulges on both sides, lined up with the moon",
      tags=["tides", "tidal force", "moon", "ocean", "gravity", "earth"])
def _(S):
    c = (9.5, 12)
    env = ell_pts(*c, 8, 4.75, 0, 0, 360, 2)
    caps = runs(env, lambda p: abs(p[0] - c[0]) > 5)
    return [shell(circle(*c, 3.5)), *[line(pts_d(rn)) for rn in caps], dot(21, 12, 1.5)]


@icon("free-return-trajectory", CAT, "Free-return trajectory: a figure-eight path looping around Earth and the moon",
      tags=["figure eight", "lunar flyby", "moon mission", "trajectory", "spaceflight", "orbit"])
def _(S):
    a = 9.5
    pts = []
    n = 72
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        d = 1 + math.sin(t) ** 2
        x = a * math.cos(t) / d
        y = a * math.sin(t) * math.cos(t) / d
        pts.append((12 + x, 12 + y * (1.75 if x < 0 else 1.15)))
    k = 60
    tip = pts[k]
    ang = math.degrees(math.atan2(tip[1] - pts[k - 1][1], tip[0] - pts[k - 1][0]))
    return [
        line(pts_d(pts[:-1], closed=True)),
        shell(circle(5.25, 12, 2)),
        dot(18.75, 12, 1.25),
        line(arrow_head(tip, ang, 1.75)),
    ]


def _rocket(S, cx, top, h=8.0, w=3.5):
    hw = w / 2
    body = (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + hw * 1.1)} {fmt(top + h * 0.2)} {fmt(cx + hw)} {fmt(top + h * 0.45)} "
            f"{fmt(cx + hw)} {fmt(top + h * 0.8)}H{fmt(cx - hw)}C{fmt(cx - hw)} {fmt(top + h * 0.45)} "
            f"{fmt(cx - hw * 1.1)} {fmt(top + h * 0.2)} {fmt(cx)} {fmt(top)}Z")
    fins = [line(seg(cx - hw, top + h * 0.6, cx - hw - 1.25, top + h)), line(seg(cx + hw, top + h * 0.6, cx + hw + 1.25, top + h))]
    return [shell(body), *fins]


@icon("launch-trajectory", CAT, "Launch trajectory: a curved path rising from a rocket on the ground up into orbit",
      tags=["launch", "rocket launch", "ascent", "gravity turn", "spaceflight", "trajectory"])
def _(S):
    def bez(t, p0=(6, 10.5), p1=(7, 5), p2=(13, 3.5), p3=(20.5, 3.5)):
        u = 1 - t
        return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
                u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])
    path = [bez(i / 30) for i in range(31)]
    return [
        *_rocket(S, 5.5, 12.5, 8, 3.5),
        line(seg(2, 21.5, 22, 21.5)),
        *[line(d) for d in dashes(path, 1.6, 2)],
        line(arrow_head((21.5, 3.5), 0, 1.75)),
    ]


@icon("orbital-velocity", CAT, "Orbital velocity: a satellite on its orbit with an arrow pointing along its path",
      tags=["orbital speed", "tangent velocity", "orbit", "satellite", "physics", "vector"])
def _(S):
    c, r = (11, 13.5), 7.5
    top = (c[0], c[1] - r)
    return [
        shell(circle(*c, 2.75)),
        line(arc(*c, r, -90 + 22, -90 - 22)),
        dot(*top, 1.9),
        line(seg(top[0] + 3.5, top[1], 20, top[1])),
        line(arrow_head((21.25, top[1]), 0, 2)),
    ]


@icon("earth-rotation", CAT, "Earth's rotation: a globe on its tilted axis with an arrow circling around it",
      tags=["earth spin", "rotation", "axis tilt", "day and night", "globe", "planet"])
def _(S):
    c, r, tilt = (12, 11.5), 5.5, -23.5
    ax = tilt - 90
    arrow = arc_pts(*c, 8.75, 25, 155, 3)
    tip = arrow[-1]
    ang = math.degrees(math.atan2(tip[1] - arrow[-2][1], tip[0] - arrow[-2][0]))
    return [
        shell(circle(*c, r)),
        detail(seg(*polar(*c, r, tilt), *polar(*c, r, tilt + 180))),
        line(seg(*polar(*c, r + 1.75, ax), *polar(*c, 10, ax))),
        line(pts_d(arrow)),
        line(arrow_head(tip, ang, 1.75)),
    ]


@icon("analemma", CAT, "Analemma: the figure-eight the sun traces in the sky over a year, above the horizon",
      tags=["sun path", "figure eight", "equation of time", "solar year", "sundial", "astronomy"])
def _(S):
    pts = []
    n = 72
    for i in range(n + 1):
        t = 2 * math.pi * i / n
        s = math.sin(t)
        pts.append((12 + 3.5 * math.sin(2 * t) * (0.65 if s > 0 else 1.0), 10 - 7 * s))
    sun = pts[45]
    keep = outside(pts, [(sun[0], sun[1], 3.75)])
    return [
        *[line(pts_d(rn)) for rn in keep],
        shell(circle(*sun, 1.75)),
        line(seg(3, 20.5, 21, 20.5)),
    ]


@icon("alt-azimuth-coordinates", CAT, "Altitude and azimuth: a sky dome over the horizon with a star and its angles marked",
      tags=["altazimuth", "horizontal coordinates", "altitude", "azimuth", "celestial sphere", "astronomy"],
      aliases=["altitude-azimuth"])
def _(S):
    c = (12, 16.5)
    star = polar(*c, 9.5, -52)
    return [
        line(arc(*c, 9.5, 180, 360)),
        line(ellipse(c[0], c[1], 9.5, 3.5)),
        line(seg(*c, *polar(*c, 6.25, -52))),
        line(arc(*c, 3.75, -48, -4)),
        dot(*c, 1.3),
        Part("dot", spark(*star, 3, 1, S)),
    ]


# ============================================================================ telescopes and instruments

def tube(m, x0, x1, hw, S, rr=None):
    """Rectangle along a local axis (a telescope tube)."""
    r = L(S, 0, 1.25) if rr is None else rr
    return poly([m(x0, -hw), m(x1, -hw), m(x1, hw), m(x0, hw)], closed=True, r=r)


@icon("dobsonian-telescope", CAT, "Dobsonian telescope: a fat open tube resting in a boxy rocker base on the ground",
      tags=["dobsonian", "reflector telescope", "stargazing", "amateur astronomy", "telescope", "newtonian"])
def _(S):
    m = axis((10.5, 14.5), -50)
    t = tube(m, -3, 11, 3.25, S)
    box = poly([(5.5, 14.5), (15.5, 14.5), (15.5, 20.5), (5.5, 20.5)], closed=True, r=L(S, 0, 1.25))
    box_cut = path_to_d(D(P(box), U(P(t), ST(t, 4, "round", "round"))))
    return [
        shell(t),
        shell(box_cut),
        line(seg(*m(7.5, -3.25), *m(7.5, -6))),
        line(seg(3.5, 21.75, 17.5, 21.75)),
    ]


@icon("catadioptric-telescope", CAT, "Catadioptric telescope: a short stubby tube with a round front plate on a fork arm",
      tags=["schmidt cassegrain", "sct", "compound telescope", "goto telescope", "telescope", "stargazing"])
def _(S):
    m = axis((10.5, 9.5), -35)
    body = union(tube(m, -5, 3, 4, S, 0), tilted_ellipse(*m(3, 0), 1.9, 4, -35))
    return [
        shell(body),
        detail(tilted_ellipse(*m(3, 0), 1.9, 4, -35)),
        dot(*m(3, 0), 1.1),
        line(poly([(16.5, 20.5), (16.5, 14), (13.5, 11.5)], r=S.r)),
        line(seg(7.5, 20.75, 20, 20.75)),
    ]


@icon("telescope-eyepiece", CAT, "Telescope eyepiece: a short ridged cylinder with a lens on top and a narrow barrel below",
      tags=["eyepiece", "ocular", "telescope lens", "magnification", "optics", "stargazing"])
def _(S):
    if S.name == "line":
        body = union(ellipse(12, 5.5, 5.5, 2), rect(6.5, 5.5, 11, 8.5), ellipse(12, 14, 5.5, 2))
    else:
        body = union(ellipse(12, 5.5, 5.5, 2), rect(6.5, 5.5, 11, 8.5, 0), ellipse(12, 14, 5.5, 2))
    return [
        shell(body),
        detail(ellipse(12, 5.5, 5.5, 2)),
        detail(seg(9.5, 9.5, 9.5, 13.5)), detail(seg(14.5, 9.5, 14.5, 13.5)),
        shell(rect(9, 16.5, 6, 5, L(S, 0, 1.25))),
    ]


@icon("neutrino-detector", CAT, "Neutrino detector: a huge sphere lined inside with rows of round light sensors",
      tags=["neutrino observatory", "particle detector", "photomultiplier", "physics", "detector", "science"])
def _(S):
    c = (12, 10.75)
    sensors = [dot(*polar(*c, 5.5, a), 1.05) for a in range(0, 360, 45)] + [dot(*polar(*c, 2.5, a), 1.05) for a in (45, 165, 285)]
    return [
        shell(circle(*c, 8.5)),
        *sensors,
        line(seg(*polar(*c, 9.5, 115), 6.5, 21.5)),
        line(seg(*polar(*c, 9.5, 65), 17.5, 21.5)),
    ]


@icon("astrophotography", CAT, "Astrophotography: a camera fixed to the back of a small telescope, aimed at a star",
      tags=["astrophoto", "night photography", "camera", "telescope", "deep sky imaging", "stars"])
def _(S):
    m = axis((14.5, 10.5), -35)
    return [
        shell(rect(2.5, 12.5, 8, 7, L(S, 0, 1.75))),
        shell(tube(m, -3.5, 6.5, 2.5, S, L(S, 0, 1))),
        dot(6.5, 16, 1.5),
        Part("dot", spark(5.5, 5.5, 3.25, 1, S)),
    ]


@icon("solar-telescope", CAT, "Solar telescope: a telescope with a dark filter over its front, pointed at the sun",
      tags=["solar filter", "sun observing", "telescope", "solar viewing", "sunspots", "astronomy"])
def _(S):
    m = axis((9.5, 13), -35)
    base = m(-0.5, 2.25)
    return [
        shell(tube(m, -6, 4.75, 2.25, S, L(S, 0, 1))),
        solid(tube(m, 5.75, 7.75, 3, S, L(S, 0, 0.75))),
        line(seg(*base, 6, 21.5)), line(seg(*base, 13, 21.5)),
        shell(circle(20, 4, 2)),
        *[line(seg(*polar(20, 4, 3.75, a), *polar(20, 4, 5.25, a))) for a in (90, 135, 180)],
    ]


@icon("telescope-finder-scope", CAT, "Finder scope: a small sighting tube mounted on top of a larger telescope tube",
      tags=["finderscope", "finder", "red dot finder", "telescope", "aiming", "stargazing"], aliases=["finderscope"])
def _(S):
    m = axis((11, 15.5), -20)
    return [
        shell(tube(m, -8.5, 8.5, 3.25, S)),
        shell(poly([m(0.5, -9.25), m(8, -9.25), m(8, -5.75), m(0.5, -5.75)], closed=True, r=L(S, 0, 0.75))),
        line(seg(*m(2.5, -5.75), *m(2.5, -4.25))),
        line(seg(*m(6.5, -5.75), *m(6.5, -4.25))),
        detail(seg(*m(5.75, -3.25), *m(5.75, 3.25))),
        line(seg(*m(-2, 4.25), 7, 21.5)), line(seg(*m(-2, 4.25), 14, 21.5)),
    ]


@icon("transit-instrument", CAT, "Transit instrument: a telescope swinging on a horizontal axle between two stone piers",
      tags=["transit telescope", "meridian circle", "observatory", "timekeeping", "historic instrument", "astronomy"])
def _(S):
    m = axis((12, 12), -72)
    rr = L(S, 0, 1)
    return [
        shell(rect(2.5, 11, 4.5, 10.5, rr)),
        shell(rect(17, 11, 4.5, 10.5, rr)),
        line(seg(7, 12, 8.75, 12)), line(seg(15.25, 12, 17, 12)),
        shell(tube(m, -7.5, 8.5, 2, S, L(S, 0, 1))),
        dot(12, 12, 0.9),
    ]


@icon("nocturnal-instrument", CAT, "Nocturnal: an old dial with a long pointer arm for telling time at night by the stars",
      tags=["nocturnal", "nocturlabe", "star clock", "night time", "historic instrument", "navigation"],
      aliases=["nocturlabe"])
def _(S):
    c = (10, 10)
    arm_in = seg(*c, *polar(*c, 5.5, -35))
    return [
        shell(union(circle(*c, 6.5), rect(8.5, 15, 3, 6.5, L(S, 0, 1.25)))),
        detail(arm_in),
        line(seg(*polar(*c, 7.5, -35), *polar(*c, 13, -35))),
        dot(*c, 1.4),
        *[detail(seg(*polar(*c, 4.25, a), *polar(*c, 6.5, a))) for a in (140, 180, 220)],
    ]


@icon("astronomy-red-flashlight", CAT, "Red astronomy flashlight: a small torch with a red filter cap that keeps night vision",
      tags=["red light", "night vision", "torch", "stargazing", "flashlight", "astronomy"], aliases=["red-torch"])
def _(S):
    m = axis((12.5, 12.5), -45)
    body = poly([m(-9, -2), m(0, -2), m(2, -3.25), m(5.5, -3.25), m(5.5, 3.25), m(2, 3.25), m(0, 2), m(-9, 2)],
                closed=True, r=L(S, 0, 1))
    return [
        shell(body),
        solid(tube(m, 6.5, 8.25, 3.25, S, L(S, 0, 0.6))),
        detail(seg(*m(-6.5, -2), *m(-6.5, 2))),
        Part("dot", spark(5.25, 5.25, 3.25, 1, S)),
    ]


@icon("all-sky-camera", CAT, "All-sky camera: a fisheye dome camera on a post looking straight up at the night sky",
      tags=["fisheye camera", "meteor camera", "sky monitor", "cloud camera", "observatory", "astronomy"])
def _(S):
    return [
        shell(union("M7 11.5A5 5 0 0 1 17 11.5Z", rect(5.5, 11.5, 13, 3.5, L(S, 0, 1)))),
        detail(arc(12, 11.5, 2.5, 190, 350)),
        line(seg(12, 15, 12, 20)),
        line(seg(7.5, 21, 16.5, 21)),
        Part("dot", spark(4, 4.5, 2.25, 0.75, S)), Part("dot", spark(20, 3.5, 2.25, 0.75, S)),
    ]


# ============================================================================ astronaut gear

@icon("spacesuit-glove", CAT, "Spacesuit glove: a bulky padded glove with a metal ring at the wrist",
      tags=["eva glove", "astronaut glove", "pressure glove", "spacesuit", "spacewalk", "astronaut"])
def _(S):
    rr = L(S, 0, 2.5)
    hand = union(rect(8.5, 3.5, 9.5, 14, rr), path_to_d(ST("M9 13L5 8.5", 3.75, S.cap, S.join)))
    return [
        shell(hand),
        detail(seg(11.75, 4, 11.75, 8.5)), detail(seg(14.75, 4, 14.75, 8.5)),
        shell(rect(7, 17.5, 12, 4, L(S, 0, 1.25))),
    ]


@icon("space-boot", CAT, "Space boot: a chunky padded boot with a thick ridged sole and an ankle ring",
      tags=["moon boot", "astronaut boot", "eva boot", "spacesuit", "footprint", "astronaut"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 10.5, 3.5, L(S, 0, 1.25))),
        shell(poly([(6.5, 6), (15, 6), (15, 10.5), (19, 11.5), (21, 14), (21, 17), (6.5, 17)], closed=True, r=L(S, 0, 1.5))),
        shell(rect(5.5, 17, 16.5, 4.5, L(S, 0, 1.25))),
        detail(seg(10, 19.75, 10, 21.5)), detail(seg(14, 19.75, 14, 21.5)), detail(seg(18, 19.75, 18, 21.5)),
    ]


@icon("launch-entry-suit", CAT, "Launch and entry suit: a full-body pressure suit with a round helmet and a chest hose connector",
      tags=["pressure suit", "flight suit", "pumpkin suit", "spacesuit", "astronaut", "launch"])
def _(S):
    limbs = ["M8 11L6 17", "M16 11L18 17", "M10 15.5L9.5 21", "M14 15.5L14.5 21"]
    body = U(P(rect(7.5, 9.5, 9, 7, L(S, 0, 2))), *[ST(d, 3.75, S.cap, S.join) for d in limbs])
    return [
        shell(circle(12, 5, 3.25)),
        shell(path_to_d(body)),
        dot(12, 12.25, 1.2),
    ]


@icon("retro-space-helmet", CAT, "Retro space helmet: a round fishbowl glass helmet with a small antenna on top",
      tags=["fishbowl helmet", "retro sci-fi", "space helmet", "astronaut", "costume", "vintage"])
def _(S):
    c = (12, 11.5)
    return [
        shell(union(circle(*c, 7.25), rect(6.5, 17, 11, 4.5, L(S, 0, 1.5)))),
        detail(arc(*c, 4.5, 195, 255)),
        detail(seg(6.5, 18.5, 17.5, 18.5)),
        line(seg(*polar(*c, 8.25, -55), *polar(*c, 10, -55))),
        dot(*polar(*c, 11, -55), 1.3),
    ]


@icon("space-food-pouch", CAT, "Space food pouch: a flat foil pouch with a drinking spout, as eaten on a space station",
      tags=["astronaut food", "food pouch", "freeze dried", "space station", "drink pouch", "astronaut"])
def _(S):
    return [
        shell(rect(6, 7, 12, 14.5, L(S, 0, 2))),
        detail(seg(6, 10, 18, 10)),
        shell(rect(10.25, 2.5, 3.5, 4.5, L(S, 0, 0.75))),
        detail(star5(12, 15.25, 3, 1.35)),
    ]


@icon("parabolic-flight", CAT, "Parabolic flight: an airplane flying an arched path that gives a moment of weightlessness",
      tags=["zero gravity flight", "vomit comet", "weightlessness", "microgravity", "astronaut training", "airplane"],
      aliases=["zero-g-flight"])
def _(S):
    arch = [(2 + 20 * t, 20.5 - 15 * (1 - (2 * t - 1) ** 2)) for t in [i / 30 for i in range(31)]]
    keep = outside(arch, [(12, 5.5, 5)])
    k = L(S, 0, 0.75)
    body = poly([(6.5, 7), (6.5, 3), (8, 3), (9.75, 5), (16, 5), (17.5, 6), (16, 7)], closed=True, r=k)
    return [*[line(d) for rn in keep for d in dashes(rn, 1.75, 2)], shell(body), line(seg(12.5, 7, 11, 9.5))]


@icon("mission-patch", CAT, "Mission patch: an oval embroidered badge with a stitched border and a rocket in the middle",
      tags=["space mission", "embroidered patch", "crew patch", "badge", "emblem", "astronaut"])
def _(S):
    stitch = ell_pts(12, 12, 5.25, 7.25, 0, 0, 360, 3)
    return [
        shell(ellipse(12, 12, 7.75, 9.75)),
        *[detail(d) for d in dashes(stitch, 1.2, 1.6)],
        detail("M12 7.5C13.5 9 13.75 11 13.75 14H10.25C10.25 11 10.5 9 12 7.5Z"),
        detail(seg(12, 15.5, 12, 16.5)),
    ]


@icon("astronaut-wings", CAT, "Astronaut wings: a pin badge with spread wings and a star in the middle",
      tags=["astronaut badge", "wings pin", "flight badge", "insignia", "award", "astronaut"])
def _(S):
    k = L(S, 0, 0.8)
    wing = [(8.5, 10), (2, 7.5), (2.5, 9.75), (4, 11.5), (6, 12.75), (8.5, 13.5)]
    rwing = [(24 - x, y) for x, y in wing]
    return [
        shell(poly(wing, closed=True, r=k)),
        shell(poly(rwing, closed=True, r=k)),
        shell(star5(12, 11.25, 3.25, 1.45, S)),
        line(seg(12, 15.75, 12, 20)),
    ]
