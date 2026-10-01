"""TypeIcon Core: astronomy (batch 003).

Moon and sun studies, models of the sky, spacecraft, asterisms and stargazing gear, drawn from the objects
themselves on the 24 px grid.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, filled_region, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import LINE, D, I, P, ST, U, fmt, path_to_d, polar  # noqa: F401

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


def grow(d, g):
    """Region d expanded by g px (to cut clean gaps between parts)."""
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def cut(d, *regions):
    """Open or closed stroke path d with the parts inside `regions` removed (keeps the stroke as a region)."""
    return path_to_d(D(P(d), *[P(r) for r in regions]))


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def pts_d(pts, closed=False):
    d = "".join(("M" if i == 0 else "L") + f"{fmt(x)} {fmt(y)}" for i, (x, y) in enumerate(pts))
    return d + ("Z" if closed else "")


def axis(origin, deg):
    """Local frame: x runs along `deg` (0 = right, positive = clockwise on screen)."""
    ox, oy = origin
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return lambda x, y: (ox + x * c - y * s, oy + x * s + y * c)


def head(S, p, deg, size=3.0, spread=45):
    """Open arrowhead whose tip is p, pointing along deg."""
    a = polar(p[0], p[1], size, deg + 180 - spread)
    b = polar(p[0], p[1], size, deg + 180 + spread)
    return line(poly([a, p, b], r=S.r * 0.5))


def star5(cx, cy, ro, ri=None, start=-90):
    ri = ri if ri is not None else ro * 0.45
    return [polar(cx, cy, ro if i % 2 == 0 else ri, start + i * 36) for i in range(10)]


def sparkle(cx, cy, r, k=0.32):
    """Four-point sparkle outline points."""
    return [polar(cx, cy, r if i % 2 == 0 else r * k, -90 + i * 45) for i in range(8)]


def rays(cx, cy, r0, r1, angles):
    return [seg(*polar(cx, cy, r0, a), *polar(cx, cy, r1, a)) for a in angles]


def orbit(cx, cy, r, gaps, a0=0.0, a1=360.0):
    """Arcs of a circle with gaps: gaps = [(angle, half_width_deg), ...]."""
    marks = sorted(gaps)
    if not marks:
        return [arc(cx, cy, r, a0, a1)] if a1 - a0 < 360 else [circle(cx, cy, r)]
    out = []
    n = len(marks)
    for i in range(n):
        a, w = marks[i]
        b, v = marks[(i + 1) % n]
        s, e = a + w, b - v
        if i == n - 1:
            e += 360
        if e - s > 4:
            out.append(arc(cx, cy, r, s, e))
    return out


def ellipse_arc(cx, cy, rx, ry, t0, t1):
    """Open elliptical arc from parameter t0 to t1 (degrees, clockwise on screen)."""
    a = (cx + rx * math.cos(math.radians(t0)), cy + ry * math.sin(math.radians(t0)))
    b = (cx + rx * math.cos(math.radians(t1)), cy + ry * math.sin(math.radians(t1)))
    large = 1 if (t1 - t0) % 360 > 180 else 0
    return f"M{fmt(a[0])} {fmt(a[1])}A{fmt(rx)} {fmt(ry)} 0 {large} 1 {fmt(b[0])} {fmt(b[1])}"


def gap_deg(r, half):
    """Half-width in degrees of a gap of `half` px on a circle of radius r."""
    return math.degrees(half / r)


def star_link(a, b, pad=3.0):
    """Segment between two star centres, shortened by pad at each end."""
    (x0, y0), (x1, y1) = a, b
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    return seg(x0 + ux * pad, y0 + uy * pad, x1 - ux * pad, y1 - uy * pad)


# ============================================================================ the moon

def _blue_page(S):
    page = rect(12, 11, 10, 11, min(S.R, 2))
    return [
        shell(page),
        detail(seg(12, 14.5, 22, 14.5)),
        line(seg(15, 9, 15, 12)), line(seg(19, 9, 19, 12)),
        mark(circle(15, 18, 1.5)), mark(circle(19, 18, 1.5)),
    ]


def _blue_filled():
    moon = D(U(P(circle(9.5, 9.5, 8.5))), P(grow(rect(12, 11, 10, 11, 2), 3)))
    return U(moon, filled_region(_blue_page(LINE)))


@icon("blue-moon", CAT, "Full moon beside a calendar page marking two full moons in one month",
      tags=["blue moon", "full moon", "second full moon", "lunar calendar", "moon", "month"], filled=_blue_filled)
def _(S):
    return [line(arc(9.5, 9.5, 7.5, 97, 337)), *_blue_page(S)]


def _patch(S, pts):
    return mark(poly(pts, closed=True, r=L(S, 0, 1.2)))


@icon("lunar-maria", CAT, "Moon disk with large dark smooth plains, the lunar seas",
      tags=["lunar maria", "moon seas", "mare", "moon surface", "lunar", "selenography"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        _patch(S, [(7, 7), (11, 6), (12, 9.5), (9.5, 12), (6, 11)]),
        _patch(S, [(14, 9), (17.5, 8), (18.5, 12.5), (15, 13)]),
        _patch(S, [(9, 15), (14, 15.5), (13.5, 18.5), (9.5, 18.5)]),
    ]


@icon("far-side-of-moon", CAT, "Cratered moon with an arrow curving around behind it",
      tags=["far side", "dark side of the moon", "lunar far side", "moon", "craters", "hidden side"])
def _(S):
    c = (12, 13.5)
    tip = polar(c[0], c[1], 9.5, -20)
    return [
        shell(circle(12, 13.5, 6.5)),
        detail(circle(10, 12, 1.75)), detail(circle(14.5, 16, 1.5)),
        line(arc(12, 13.5, 9.5, 195, 338)),
        head(S, tip, 70, 3),
    ]


# ============================================================================ sun and sky

_EARTH_R = 26.0


@icon("orbital-sunrise", CAT, "Sun rising over the curved edge of the Earth seen from orbit",
      tags=["orbital sunrise", "sunrise from space", "earth limb", "horizon", "orbit", "dawn"])
def _(S):
    earth = f"M2 22.5V19.5A{fmt(_EARTH_R)} {fmt(_EARTH_R)} 0 0 1 22 19.5V22.5Z"
    earth = L(S, earth, f"M2 22.5V19.5A{fmt(_EARTH_R)} {fmt(_EARTH_R)} 0 0 1 22 19.5V20.5A2 2 0 0 1 20 22.5H4A2 2 0 0 1 2 20.5Z")
    return [
        shell(earth),
        line(arc(12, 16, 4, 208, 332)),
        *[line(d) for d in rays(12, 16, 6.5, 9, (200, 235, 270, 305, 340))],
        dot(4, 5, 1), dot(20, 4.5, 1),
    ]


@icon("cosmic-calendar", CAT, "Calendar page with a spark of the big bang on the first day and a person on the last",
      tags=["cosmic calendar", "history of the universe", "time scale", "calendar", "big bang", "evolution"])
def _(S):
    page = rect(3, 5, 18, 16.5, S.R)
    return [
        shell(page),
        detail(seg(3, 9.5, 21, 9.5)),
        line(seg(8, 3, 8, 6)), line(seg(16, 3, 16, 6)),
        mark(poly(sparkle(8, 14.5, 3), closed=True)),
        mark(circle(16, 13.25, 1.5)),
        detail(L(S, "M13.5 18.5A2.5 2.5 0 0 1 18.5 18.5", "M13.5 18.5A2.5 2.5 0 0 1 18.5 18.5")),
    ]


@icon("universe-timeline", CAT, "Widening cone of the universe from a bright bang on the left to galaxies on the right",
      tags=["timeline of the universe", "big bang", "cosmic history", "expansion", "cosmology", "universe"])
def _(S):
    return [
        line("M7 12C12 11.5 16 9 21 4"),
        line("M7 12C12 12.5 16 15 21 20"),
        mark(poly(sparkle(4, 12, 3.25, 0.3), closed=True, r=L(S, 0, 0.2))),
        dot(14, 12, 1), dot(19, 9, 1.1), dot(19, 15, 1.1), dot(18, 12, 0.9),
    ]


# ============================================================================ models of the sky

def _earth(S, cx, cy, r):
    return [shell(circle(cx, cy, r)), detail(seg(cx - r, cy, cx + r, cy)), detail(seg(cx, cy - r, cx, cy + r))]


@icon("geocentric-model", CAT, "Earth at the centre with the sun and a planet circling on orbits around it",
      tags=["geocentric", "ptolemaic", "earth centered", "ancient astronomy", "model", "orbits"])
def _(S):
    sun = polar(12, 12.5, 8.25, -45)
    pl = polar(12, 12.5, 8.25, 135)
    return [
        shell(circle(12, 12.5, 3.5)),
        detail(seg(8.5, 12.5, 15.5, 12.5)), detail(seg(12, 9, 12, 16)),
        *[line(d) for d in orbit(12, 12.5, 8.25, [(-45, gap_deg(8.25, 5)), (135, gap_deg(8.25, 3.4))])],
        dot(pl[0], pl[1], 1.5),
        shell(circle(sun[0], sun[1], 1.75)),
        *[line(d) for d in rays(sun[0], sun[1], 3.5, 4.75, (-95, -45, 5))],
    ]


@icon("heliocentric-model", CAT, "Sun at the centre with planets on circular orbits around it",
      tags=["heliocentric", "copernican", "sun centered", "solar system", "orbits", "model"])
def _(S):
    p1 = polar(12, 12, 6, -40)
    p2 = polar(12, 12, 9.5, 130)
    return [
        dot(12, 12, 2.5),
        *[line(d) for d in orbit(12, 12, 6, [(-40, gap_deg(6, 3.2))])],
        *[line(d) for d in orbit(12, 12, 9.5, [(130, gap_deg(9.5, 3.7))])],
        dot(p1[0], p1[1], 1.25),
        dot(p2[0], p2[1], 1.75),
    ]


@icon("epicycle", CAT, "Large circle with a small circle riding on its rim, the old model of planet loops",
      tags=["epicycle", "deferent", "ptolemy", "planetary motion", "ancient astronomy", "retrograde"])
def _(S):
    c = (10, 13.5)
    e = polar(c[0], c[1], 7.5, -45)
    big = [line(d) for d in orbit(c[0], c[1], 7.5, [(-45, gap_deg(7.5, 6))])]
    return [
        *big,
        line(circle(e[0], e[1], 4)),
        dot(e[0], e[1], 1.25),
        dot(c[0], c[1], 1.25),
        dot(*polar(e[0], e[1], 4, L(S, -45, 45)), 1.75),
    ]


# ============================================================================ learning and outreach

@icon("astronomy-book", CAT, "Closed book with a crescent moon and a star on its cover",
      tags=["astronomy book", "star guide", "sky atlas", "reading", "science book", "learning"])
def _(S):
    body = rect(4.5, 2.5, 15, 19, min(S.R, 3))
    moon = minus(circle(13, 10, 4), circle(15, 8.5, 3.5))
    return [
        shell(body),
        detail(seg(8, 2.5, 8, 21.5)),
        mark(moon),
        mark(poly(star5(15.5, 16.5, 2.4, 1.1), closed=True, r=L(S, 0, 0.3))),
    ]


@icon("rocket-launch-viewing", CAT, "Two people on a hill watching a rocket climb on a smoke trail",
      tags=["launch viewing", "watch a launch", "spectators", "rocket", "launch site", "space tourism"])
def _(S):
    m = axis((18, 6), -70)
    rocket = [m(4, 0), m(1.5, -1.75), m(-3, -1.75), m(-3, 1.75), m(1.5, 1.75)]
    return [
        shell(poly(rocket, closed=True, r=S.r * 0.3)),
        line("M16.5 11.5C15.5 14.5 15.5 17 17 19.5"),
        line(seg(2, 21, 22, 21)),
        dot(5, 12, 2), line(L(S, "M2 18.5V17.5A3 3 0 0 1 8 17.5V18.5", "M2 18.5V17.5A3 3 0 0 1 8 17.5V18.5")),
        dot(11.5, 12, 2), line("M8.5 18.5V17.5A3 3 0 0 1 14.5 17.5V18.5"),
    ]


@icon("space-museum", CAT, "Columned museum building with a rocket standing beside it",
      tags=["space museum", "air and space museum", "science museum", "exhibit", "rocket", "gallery"])
def _(S):
    roof = poly([(2.5, 10), (2.5, 8.5), (8.5, 4.5), (14.5, 8.5), (14.5, 10)], closed=True, r=S.r * 0.5)
    rocket = L(S, "M19 2.5C21 4.5 21.5 7.5 21.5 10.5V21H16.5V10.5C16.5 7.5 17 4.5 19 2.5Z",
               "M19 2.5C21 4.5 21.5 7.5 21.5 10.5V20A1 1 0 0 1 20.5 21H17.5A1 1 0 0 1 16.5 20V10.5C16.5 7.5 17 4.5 19 2.5Z")
    return [
        shell(roof),
        line(seg(4.5, 12, 4.5, 18)), line(seg(8.5, 12, 8.5, 18)), line(seg(12.5, 12, 12.5, 18)),
        line(seg(2.5, 21, 14.5, 21)),
        shell(rocket),
        detail(seg(16.5, 16.5, 21.5, 16.5)),
    ]


# ============================================================================ measuring the universe

@icon("light-speed", CAT, "Letter c with speed lines, the speed of light",
      tags=["speed of light", "light speed", "constant c", "physics", "relativity", "fast"])
def _(S):
    return [
        line(arc(16, 12, 5.5, 40, 320)),
        line(seg(4, 7.5, 8.5, 7.5)), line(seg(2, 12, 8, 12)), line(seg(4, 16.5, 8.5, 16.5)),
    ]


@icon("astronomical-unit", CAT, "Sun and Earth with a double-headed arrow measuring the distance between them",
      tags=["astronomical unit", "au", "earth sun distance", "measurement", "distance", "scale"])
def _(S):
    return [
        shell(circle(7, 8.5, 2.5)),
        *[line(d) for d in rays(7, 8.5, 4.25, 5.25, range(0, 360, 45))],
        shell(circle(18.5, 8.5, 2.25)),
        line(seg(4, 17.5, 20, 17.5)),
        head(S, (3, 17.5), 180, 2.75),
        head(S, (21, 17.5), 0, 2.75),
    ]


@icon("cosmic-distance-ladder", CAT, "Ladder with a planet, a star and a galaxy beside its rungs",
      tags=["distance ladder", "cosmic distances", "parallax", "standard candle", "measurement", "cosmology"])
def _(S):
    return [
        line(seg(3.5, 2.5, 3.5, 21.5)), line(seg(10, 2.5, 10, 21.5)),
        line(seg(3.5, 6, 10, 6)), line(seg(3.5, 12, 10, 12)), line(seg(3.5, 18, 10, 18)),
        shell(circle(16.5, 18, 2.25)),
        mark(poly(sparkle(16.5, 12, 3), closed=True)),
        line(path_to_d(__import__("geometry").transform_path(P(ellipse(16.5, 5.5, 4, 2)), __import__("geometry").rotation(-30, 16.5, 5.5)))),
        dot(16.5, 5.5, 1),
    ]


# ============================================================================ the sun and small bodies

@icon("big-crunch", CAT, "Arrows from four sides collapsing the universe into a single point",
      tags=["big crunch", "collapse", "cosmology", "end of the universe", "contraction", "implosion"])
def _(S):
    out = [dot(12, 12, 2.25)]
    for a in (-135, -45, 45, 135):
        p0, p1 = polar(12, 12, 10.5, a), polar(12, 12, 5, a)
        out += [line(seg(*p0, *p1)), head(S, p1, a + 180, 3)]
        out.append(mark(poly(sparkle(*polar(12, 12, 9, a + 45), 2.25, 0.34), closed=True)))
    return out


@icon("solar-cycle", CAT, "Sun above a wave that rises and falls, the eleven-year cycle of solar activity",
      tags=["solar cycle", "sunspot cycle", "solar maximum", "solar minimum", "space weather", "sun activity"])
def _(S):
    return [
        shell(circle(12, 6.5, 2.5)),
        *[line(d) for d in rays(12, 6.5, 4, 5, range(0, 360, 45))],
        line("M2 17C5 13 9 13 12 17C15 21 19 21 22 17"),
    ]


def _clip_seg(a, b, cx, cy, r):
    """Part of segment a-b inside the circle (None if outside)."""
    (x0, y0), (x1, y1) = a, b
    dx, dy = x1 - x0, y1 - y0
    fx, fy = x0 - cx, y0 - cy
    A = dx * dx + dy * dy
    B = 2 * (fx * dx + fy * dy)
    C = fx * fx + fy * fy - r * r
    disc = B * B - 4 * A * C
    if disc <= 0:
        return None
    sq = math.sqrt(disc)
    t0, t1 = max(0.0, (-B - sq) / (2 * A)), min(1.0, (-B + sq) / (2 * A))
    if t1 - t0 < 1e-3 or math.hypot(dx, dy) * (t1 - t0) < 1.5:
        return None
    return (x0 + dx * t0, y0 + dy * t0), (x0 + dx * t1, y0 + dy * t1)


def _soft(d_seg, bend):
    """Replace a straight segment 'Mx yLx y' by a gentle quadratic curve."""
    a, b = d_seg[1:].split("L")
    x0, y0 = map(float, a.split())
    x1, y1 = map(float, b.split())
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    ln = math.hypot(x1 - x0, y1 - y0)
    nx, ny = -(y1 - y0) / ln, (x1 - x0) / ln
    return f"M{fmt(x0)} {fmt(y0)}Q{fmt(mx + nx * bend)} {fmt(my + ny * bend)} {fmt(x1)} {fmt(y1)}"


def _honeycomb(cx, cy, r, s, ox=0.0, oy=0.0):
    edges = set()
    h = math.sqrt(3) * s
    for i in range(-4, 5):
        for j in range(-4, 5):
            x = cx + ox + 1.5 * s * i
            y = cy + oy + h * (j + (i % 2) / 2)
            vs = [polar(x, y, s, k * 60) for k in range(6)]
            for k in range(6):
                a, b = vs[k], vs[(k + 1) % 6]
                key = tuple(sorted([(round(a[0], 2), round(a[1], 2)), (round(b[0], 2), round(b[1], 2))]))
                edges.add(key)
    out = []
    for a, b in sorted(edges):
        c = _clip_seg(a, b, cx, cy, r)
        if c:
            out.append(seg(*c[0], *c[1]))
    return out


@icon("solar-granulation", CAT, "Disk of the sun covered in a honeycomb of convection cells",
      tags=["solar granulation", "granules", "sun surface", "photosphere", "convection cells", "sun"])
def _(S):
    cells = _honeycomb(12, 12, 9.5, 3.9, 1.2, 0.8)
    if S.name == "rounded":
        cells = [_soft(d, 0.8 if i % 2 else -0.8) for i, d in enumerate(cells)]
    return [shell(circle(12, 12, 9.5)), *[detail(d) for d in cells]]


def _peanut(S):
    a = circle(8, 14.5, 5.5)
    b = circle(16.5, 9, 4.5)
    m = axis((12.25, 11.75), math.degrees(math.atan2(9 - 14.5, 16.5 - 8)))
    neck = pts_d([m(-3, -2.75), m(3, -2.25), m(3, 2.25), m(-3, 2.75)], closed=True)
    return union(a, b, neck)


@icon("contact-binary-asteroid", CAT, "Peanut shaped asteroid made of two rounded lobes joined at a narrow neck",
      tags=["contact binary", "asteroid", "bilobed", "peanut asteroid", "small body", "kuiper belt"])
def _(S):
    return [
        shell(_peanut(S)),
        mark(L(S, rect(5.75, 14.25, 2.5, 2.5), circle(7, 15.5, 1.4))),
        mark(L(S, rect(9, 11, 2, 2), circle(10, 12, 1.1))),
        mark(L(S, rect(15.5, 7.5, 2.5, 2.5), circle(16.75, 8.75, 1.4))),
    ]


@icon("binary-sunset", CAT, "Two suns of different sizes setting side by side over sand dunes",
      tags=["binary sunset", "twin suns", "double sunset", "binary star", "alien world", "desert"])
def _(S):
    return [
        line(arc(8, 14.5, 5, 196, 344)),
        shell(circle(17.5, 8.5, 2.5)),
        line("M2 17C5.5 15 9 15 12 16.5C15 18 18.5 18 22 16"),
        line("M6 21C9 19.5 12.5 19.5 15.5 21"),
    ]


@icon("telescope-hand-controller", CAT, "Handheld telescope keypad with a small screen, direction pad and coiled cord",
      tags=["hand controller", "handset", "goto telescope", "keypad", "remote", "telescope mount"])
def _(S):
    return [
        shell(rect(4, 2.5, 10, 16, min(S.R, 3))),
        detail(rect(6.5, 5, 5, 3, 0)),
        detail(seg(9, 10.5, 9, 15.5)), detail(seg(6.5, 13, 11.5, 13)),
        line("M9 18.5V19.5C9 21.5 11.5 21.5 12.5 20C13.5 18.5 15.5 18.5 16.5 20C17.5 21.5 20 21.5 20.5 19.5"),
    ]


@icon("pinhole-eclipse-viewer", CAT, "Box with a pinhole in one end projecting a small crescent sun onto the back wall",
      tags=["pinhole viewer", "pinhole projector", "eclipse viewer", "solar eclipse", "safe viewing", "diy"])
def _(S):
    box = poly([(2.5, 10.5), (2.5, 6), (21.5, 6), (21.5, 18), (2.5, 18), (2.5, 13.5)], r=S.r)
    moon = minus(circle(17.5, 12, 2.75), circle(19, 11, 2.5))
    return [
        line(box),
        line(seg(5.5, 12, 13, 9)), line(seg(5.5, 12, 13, 15)),
        mark(moon),
    ]


@icon("moon-globe", CAT, "Desk globe of the moon on a stand, covered in craters and dark plains",
      tags=["moon globe", "lunar globe", "desk globe", "moon map", "selenography", "education"])
def _(S):
    return [
        shell(circle(12, 10, 6.5)),
        detail(circle(10, 8, 1.5)),
        mark(poly([(12.5, 11), (15.5, 10.5), (16, 13.5), (13, 14)], closed=True, r=L(S, 0, 1))),
        line(arc(12, 10, 9, 40, 220)),
        line(seg(12, 19, 12, 21)), line(seg(8, 21.5, 16, 21.5)),
    ]


@icon("mass-driver", CAT, "Long launch rail on cratered ground flinging a small pod into the sky",
      tags=["mass driver", "electromagnetic launcher", "railgun", "lunar launcher", "space launch", "catapult"])
def _(S):
    m = axis((16.5, 7.5), -40)
    pod = pts_d([m(2.5, 0), m(1, -1.5), m(-2, -1.5), m(-2, 1.5), m(1, 1.5)], closed=True)
    return [
        line(seg(2.5, 18.5, 13, 9.5)),
        line(seg(6.5, 15, 6.5, 19)), line(seg(10.5, 11.5, 10.5, 19)),
        shell(poly([m(2.5, 0), m(1, -1.5), m(-2, -1.5), m(-2, 1.5), m(1, 1.5)], closed=True, r=S.r * 0.3)),
        line("M2 21H13C14 21 14.5 19.5 16.5 19.5S19 21 20 21H22"),
    ]


@icon("planet-size-comparison", CAT, "Row of planets of very different sizes lined up on a baseline",
      tags=["planet sizes", "size comparison", "scale", "planets", "solar system", "relative size"])
def _(S):
    return [
        dot(3.25, 16.75, 1.25),
        shell(circle(8.5, 16, 2)),
        shell(circle(17.75, 14, 4)),
        line(seg(2, 21, 22, 21)),
        detail(arc(17.75, 14, 2, L(S, 190, 195), L(S, 260, 255))),
    ]


@icon("celestial-navigation", CAT, "Sailboat on waves taking a sight on a bright star",
      tags=["celestial navigation", "star sight", "sextant", "navigation", "sailing", "wayfinding"])
def _(S):
    return [
        shell(poly([(3, 15), (15, 15), (13, 18), (5, 18)], closed=True, r=S.r * 0.5)),
        shell(poly([(9, 5), (9, 12.5), (4, 12.5)], closed=True, r=S.r * 0.5)),
        line(seg(9, 12.5, 9, 15)),
        mark(poly(sparkle(19, 4.5, 2.75, 0.32), closed=True, r=L(S, 0, 0.2))),
        dot(11.75, 4.9, 0.9), dot(14.25, 4.75, 0.9),
        line("M2 21C4 20 6 20 8 21S12 22 14 21S18 20 20 21"),
    ]


@icon("meteor-airburst", CAT, "Meteor exploding in a bright flash high above the horizon with a shock ring",
      tags=["airburst", "meteor explosion", "bolide", "fireball", "impact event", "meteor"])
def _(S):
    c = (13.5, 10)
    return [
        mark(poly(sparkle(c[0], c[1], 3.5, 0.35), closed=True, r=L(S, 0, 0.2))),
        *[line(d) for d in rays(c[0], c[1], 5.25, 8, (-90, -45, 0, 45, 90, 135, 180))],
        line(seg(*polar(c[0], c[1], 12, -135), *polar(c[0], c[1], 6, -135))),
        line(seg(2, 21, 22, 21)),
    ]


@icon("edge-of-space", CAT, "Curve of the Earth with a dashed boundary line, a plane below it and a satellite above",
      tags=["edge of space", "karman line", "atmosphere boundary", "altitude", "spaceflight", "suborbital"])
def _(S):
    R = 26.0
    earth = L(S, f"M2 22.5V19.5A{R} {R} 0 0 1 22 19.5V22.5Z",
              f"M2 22.5V19.5A{R} {R} 0 0 1 22 19.5V20.5A2 2 0 0 1 20 22.5H4A2 2 0 0 1 2 20.5Z")
    cy = 17.5 + R
    dashes = [line(arc(12, cy, R + 7.5, a, a + 3.2)) for a in [-106.6 + 6 * k for k in range(6)]]
    return [
        shell(earth),
        *dashes,
        mark(poly([(3, 12), (4.5, 12), (6, 13.5), (10.5, 13.5), (11.75, 14.25), (10.5, 15), (3.5, 15)], closed=True, r=L(S, 0, 0.5))),
        shell(rect(16, 3.25, 2.5, 2.5, 0)),
        solid(rect(12.5, 3.5, 2.5, 2)), solid(rect(19.5, 3.5, 2.5, 2)),
    ]


@icon("pressurized-rover", CAT, "Boxy crewed rover with a rounded cabin, front windows and six wheels",
      tags=["pressurized rover", "crewed rover", "moon rover", "mars rover", "exploration vehicle", "cabin"])
def _(S):
    body = poly([(2.5, 15), (2.5, 7), (16, 7), (21.5, 11), (21.5, 15)], closed=True, r=L(S, 0, 2))
    return [
        shell(body),
        detail(seg(13.5, 10.5, 17, 10.5)),
        detail(seg(5, 10.5, 10, 10.5)),
        shell(circle(5.5, 18.5, 2.25)), shell(circle(12, 18.5, 2.25)), shell(circle(18.5, 18.5, 2.25)),
        line(seg(6, 7, 6, 3.5)), line(seg(4.5, 3.5, 7.5, 3.5)),
    ]


# ============================================================================ spacecraft and missions

@icon("mars-ascent-rocket", CAT, "Small rocket lifting off from a lander platform on rocky ground",
      tags=["ascent vehicle", "mars ascent", "sample return", "liftoff", "lander", "rocket"])
def _(S):
    body = L(S, "M12 2.5C13.8 4 14 6.5 14 8V11H10V8C10 6.5 10.2 4 12 2.5Z",
             "M12 2.5C13.8 4 14 6.5 14 8V10.5A0.5 0.5 0 0 1 13.5 11H10.5A0.5 0.5 0 0 1 10 10.5V8C10 6.5 10.2 4 12 2.5Z")
    return [
        shell(body),
        mark(poly([(10.5, 12.75), (13.5, 12.75), (12, 15.5)], closed=True, r=L(S, 0, 0.4))),
        line(seg(4.5, 17.5, 19.5, 17.5)),
        line(seg(7, 17.5, 5, 21.5)), line(seg(17, 17.5, 19, 21.5)),
        line("M2 21.5H9.5L11 20.5L12.5 21.5H22"),
    ]


@icon("escape-pod", CAT, "Small round escape pod with a window and a thruster flame leaving a larger ship",
      tags=["escape pod", "lifeboat", "emergency capsule", "evacuation", "spaceship", "abandon ship"])
def _(S):
    pod = (17, 17)
    ship = poly([(9.5, 10), (2.5, 10), (2.5, 2.5), (14.5, 2.5), (14.5, 6.5)], r=L(S, 0, 2))
    trail = [line(seg(*polar(pod[0] + dx, pod[1] + dy, 5.25, -135), *polar(pod[0] + dx, pod[1] + dy, 8, -135)))
             for dx, dy in ((-1.75, 1.75), (1.75, -1.75))]
    return [
        line(ship),
        dot(6, 6.25, 1.25), dot(10, 6.25, 1.25),
        shell(circle(pod[0], pod[1], 3.75)),
        mark(circle(pod[0] + 0.25, pod[1] + 0.25, 1.4)),
        *trail,
    ]


@icon("fixed-dish-radio-telescope", CAT, "Huge radio dish set into a valley with a receiver platform hung over it on cables",
      tags=["radio telescope", "fixed dish", "radio astronomy", "dish", "receiver", "observatory"])
def _(S):
    return [
        shell(L(S, "M5 12.5H19A7 7 0 0 1 5 12.5Z", "M6 12.5H18A1 1 0 0 1 19 13.5A7 7 0 0 1 5 13.5A1 1 0 0 1 6 12.5Z")),
        line(seg(2, 3, 2, 21)), line(seg(22, 3, 22, 21)),
        line(seg(3, 3.5, 9.5, 6)), line(seg(21, 3.5, 14.5, 6)),
        shell(poly([(9.5, 6), (14.5, 6), (12, 9.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("roll-off-roof-observatory", CAT, "Small observatory shed with its flat roof rolled back on rails and a telescope inside",
      tags=["roll off roof", "backyard observatory", "shed", "telescope", "stargazing", "amateur astronomy"])
def _(S):
    m = axis((7, 7.5), -35)
    tube = [m(0, -1.5), m(7.5, -1.5), m(7.5, 1.5), m(0, 1.5)]
    return [
        shell(rect(3, 12, 11.5, 9, min(S.R, 2))),
        shell(poly(tube, closed=True, r=S.r * 0.4)),
        line(seg(16.5, 12, 22, 12)),
        shell(rect(15.5, 6.5, 6.5, 3, min(S.R, 1))),
        line(seg(21, 12, 21, 21)),
    ]


def _trefoil(cx, cy, r0, r1, S):
    out = [dot(cx, cy, r0 * 0.8)]
    for a in (-90, 30, 150):
        a0, a1 = a - 30, a + 30
        p = (f"M{fmt(polar(cx, cy, r0 + 0.6, a0)[0])} {fmt(polar(cx, cy, r0 + 0.6, a0)[1])}"
             f"L{fmt(polar(cx, cy, r1, a0)[0])} {fmt(polar(cx, cy, r1, a0)[1])}"
             f"A{fmt(r1)} {fmt(r1)} 0 0 1 {fmt(polar(cx, cy, r1, a1)[0])} {fmt(polar(cx, cy, r1, a1)[1])}"
             f"L{fmt(polar(cx, cy, r0 + 0.6, a1)[0])} {fmt(polar(cx, cy, r0 + 0.6, a1)[1])}Z")
        out.append(mark(p))
    return out


@icon("nuclear-thermal-rocket", CAT, "Rocket stage with a reactor marked by the radiation symbol above its nozzle",
      tags=["nuclear rocket", "nuclear thermal propulsion", "ntr", "reactor", "rocket engine", "propulsion"])
def _(S):
    return [
        shell(L(S, "M12 2.5C15.5 4.5 17 7.5 17 11V15H7V11C7 7.5 8.5 4.5 12 2.5Z",
                "M12 2.5C15.5 4.5 17 7.5 17 11V14A1 1 0 0 1 16 15H8A1 1 0 0 1 7 14V11C7 7.5 8.5 4.5 12 2.5Z")),
        *_trefoil(12, 10, 1.1, 3.75, S),
        shell(poly([(9.5, 16.5), (14.5, 16.5), (17, 21.5), (7, 21.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("cargo-spacecraft", CAT, "Cylinder supply ship with two solar panel wings and a docking ring on the front",
      tags=["cargo ship", "supply vehicle", "resupply", "spacecraft", "docking", "logistics"])
def _(S):
    return [
        shell(rect(4, 9.5, 12.5, 5, min(S.R, 2.5))),
        shell(rect(18.5, 10.5, 2.5, 3, 0)) if S.name == "line" else shell(rect(18.5, 10.5, 2.5, 3, 1)),
        shell(rect(7, 2.5, 6.5, 4, min(S.R, 1))),
        shell(rect(7, 17.5, 6.5, 4, min(S.R, 1))),
        line(seg(10.25, 6.5, 10.25, 9.5)), line(seg(10.25, 14.5, 10.25, 17.5)),
    ]


@icon("cardboard-rocket", CAT, "Homemade cardboard box rocket with a cone top, drawn window and taped fins",
      tags=["cardboard rocket", "box rocket", "pretend play", "kids craft", "toy rocket", "diy"])
def _(S):
    body = union(rect(8, 9, 8, 11.5, 0), poly([(8, 9), (12, 2.5), (16, 9)], closed=True),
                 poly([(8, 15), (4.5, 20.5), (8, 20.5)], closed=True), poly([(16, 15), (19.5, 20.5), (16, 20.5)], closed=True))
    return [
        shell(body),
        detail(seg(8, 9, 16, 9)),
        detail(circle(12, 13, 1.75)),
        detail(seg(8, 17.5, 16, 17.5)),
    ]


@icon("rocket-slide", CAT, "Playground rocket tower with a round window and a slide curving out of its side",
      tags=["rocket slide", "playground", "play structure", "slide", "kids", "park"])
def _(S):
    tower = L(S, "M8.5 2.5C11.5 5 12 8 12 11V21.5H5V11C5 8 5.5 5 8.5 2.5Z",
              "M8.5 2.5C11.5 5 12 8 12 11V20.5A1 1 0 0 1 11 21.5H6A1 1 0 0 1 5 20.5V11C5 8 5.5 5 8.5 2.5Z")
    return [
        shell(tower),
        detail(circle(8.5, 10, 1.5)),
        line("M14.5 12.5C17 13 18.5 15 19.5 18.5C20 20.5 21 21.5 22 21.5"),
        line(seg(14.5, 12.5, 14.5, 21.5)),
    ]


@icon("satellite-train", CAT, "Straight row of evenly spaced satellites crossing the night sky",
      tags=["satellite train", "satellite constellation", "megaconstellation", "night sky", "light pollution", "satellites"])
def _(S):
    return [
        *[dot(*p, 1.25) for p in [(3.5 + 3.4 * k, 16.5 - 2.8 * k) for k in range(6)]],
        mark(poly(sparkle(6, 5.5, 3, 0.32), closed=True, r=L(S, 0, 0.3))),
        mark(poly(sparkle(17.5, 13.5, 2.5, 0.32), closed=True, r=L(S, 0, 0.3))),
        line("M2 21.5C8 19.5 16 19.5 22 21.5"),
    ]


@icon("starshade", CAT, "Flower shaped starshade with long petals floating in front of a small space telescope",
      tags=["starshade", "occulter", "exoplanet imaging", "space telescope", "flower", "star shade"])
def _(S):
    petals = [polar(9.5, 9.5, 7.5 if i % 2 == 0 else 4.25, -90 + i * 22.5) for i in range(16)]
    m = axis((19.5, 19.5), -135)
    tube = [m(0, -1.75), m(5, -1.75), m(5, 1.75), m(0, 1.75)]
    return [
        shell(poly(petals, closed=True, r=L(S, 0, 0.8)), stroke_miterlimit="2"),
        shell(poly(tube, closed=True, r=S.r * 0.4)),
    ]


@icon("solar-probe", CAT, "Small probe tucked behind a flat heat shield that faces the nearby sun",
      tags=["solar probe", "heat shield", "sun mission", "spacecraft", "corona", "space probe"])
def _(S):
    return [
        line(arc(-2, 12, 8, -62, 62)),
        line(seg(7.5, 12, 9.5, 12)),
        shell(rect(11, 4, 2.5, 16, min(S.R, 1.25))),
        shell(rect(15.5, 9.5, 4, 5, min(S.R, 1))),
        line(seg(17.5, 9.5, 17.5, 5.5)),
        line(seg(17.5, 14.5, 17.5, 18.5)),
    ]


@icon("moon-phase-watch", CAT, "Round watch with an arched window in its dial showing the moon",
      tags=["moon phase watch", "moonphase", "wristwatch", "watch complication", "moon", "timepiece"])
def _(S):
    lug = L(S, 0, 1.25)
    return [
        shell(circle(12, 12, 7)),
        shell(rect(8.5, 2, 7, 2.5, lug)), shell(rect(8.5, 19.5, 7, 2.5, lug)),
        detail(L(S, "M8 14.5A4 4 0 0 1 16 14.5Z", "M8 14.5A4 4 0 0 1 16 14.5Z")),
        mark(circle(12, 12.75, 1.25)),
    ]


@icon("telescope-mirror", CAT, "Round telescope mirror with a bevelled rim, a central hole and a reflection highlight",
      tags=["telescope mirror", "primary mirror", "reflector", "optics", "concave mirror", "telescope"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(circle(12, 12, 6)),
        detail(arc(12, 12, 3.25, L(S, 195, 200), L(S, 255, 250))),
        dot(12, 12, 1.25),
    ]


# ============================================================================ orbital mechanics

@icon("orbit-insertion", CAT, "Arrival path bending into a circular orbit around a planet",
      tags=["orbit insertion", "orbital capture", "arrival", "orbit", "trajectory", "burn"])
def _(S):
    tip = polar(12, 13, 7.5, 195)
    return [
        shell(circle(12, 13, 3.25)),
        line("M2 5.5C6 5.5 9 5.5 12 5.5" + arc(12, 13, 7.5, -90, 195)[arc(12, 13, 7.5, -90, 195).index("A"):]),
        head(S, tip, 285, 3),
    ]


@icon("aerobraking", CAT, "Spacecraft path dipping through a planet's thin atmosphere to slow down",
      tags=["aerobraking", "aerocapture", "atmosphere", "drag", "trajectory", "orbit"])
def _(S):
    planet = L(S, "M2 12.5A9.5 9.5 0 0 1 11.5 22H2Z", "M2 12.5A9.5 9.5 0 0 1 11.5 22H4A2 2 0 0 1 2 20Z")
    return [
        shell(planet),
        line(arc(2, 22, 14, -90, 0)),
        line("M6 2.5C7 7 8 10.5 11 13C14 15.5 17 17 20.5 17.5"),
        head(S, (21, 17.5), 5, 3),
    ]


@icon("lunar-hop", CAT, "Astronaut leaping high above cratered ground with small dust puffs",
      tags=["moon jump", "lunar hop", "low gravity", "astronaut", "moonwalk", "leap"])
def _(S):
    return [
        shell(circle(11, 4.5, 2.5)),
        line(seg(11.25, 8.5, 12.25, 13)),
        line(poly([(7, 7.5), (11.4, 9.5), (16, 8)], r=S.r * 0.5)),
        line(poly([(8, 17), (9.5, 14.5), (12.25, 13), (15.5, 15.5), (17.5, 14.5)], r=S.r * 0.5)),
        line("M2 21.5H8C9 21.5 9.5 20 11.5 20S14 21.5 15 21.5H22"),
        dot(5, 18.5, 1), dot(19, 18.5, 1),
    ]


def _eli(cx, cy, a, b, tilt, t):
    m = axis((cx, cy), tilt)
    return m(a * math.cos(math.radians(t)), b * math.sin(math.radians(t)))


def ellipse_arc_rot(cx, cy, a, b, tilt, t0, t1):
    """Arc of a tilted ellipse from parameter t0 to t1 (increasing t, clockwise on screen)."""
    p0, p1 = _eli(cx, cy, a, b, tilt, t0), _eli(cx, cy, a, b, tilt, t1)
    large = 1 if (t1 - t0) % 360 > 180 else 0
    return f"M{fmt(p0[0])} {fmt(p0[1])}A{fmt(a)} {fmt(b)} {fmt(tilt)} {large} 1 {fmt(p1[0])} {fmt(p1[1])}"


@icon("comet-orbit", CAT, "Long thin elliptical orbit around the sun with a comet whose tail points away from it",
      tags=["comet orbit", "elliptical orbit", "periodic comet", "perihelion", "aphelion", "comet"])
def _(S):
    cx, cy, a, b, tilt = 12, 12.5, 9.5, 4.5, -25
    m = axis((cx, cy), tilt)
    sun = m(-5.5, 0)
    tc = -70
    head_p = _eli(cx, cy, a, b, tilt, tc)
    ux, uy = head_p[0] - sun[0], head_p[1] - sun[1]
    ln = math.hypot(ux, uy)
    ux, uy = ux / ln, uy / ln
    return [
        line(ellipse_arc_rot(cx, cy, a, b, tilt, tc + 30, tc + 330)),
        dot(sun[0], sun[1], 2),
        dot(head_p[0], head_p[1], 1.6),
        mark(poly([(head_p[0] + ux * 2.5 - uy * 0.6, head_p[1] + uy * 2.5 + ux * 0.6),
                   (head_p[0] + ux * 7 - uy * 1.8, head_p[1] + uy * 7 + ux * 1.8),
                   (head_p[0] + ux * 7 + uy * 1.8, head_p[1] + uy * 7 - ux * 1.8),
                   (head_p[0] + ux * 2.5 + uy * 0.6, head_p[1] + uy * 2.5 - ux * 0.6)], closed=True)),
    ]


@icon("planet-collision", CAT, "Two planets smashing together with debris bursting from the impact",
      tags=["planet collision", "giant impact", "impact", "cosmic crash", "planets", "catastrophe"])
def _(S):
    big, small = (8, 16), (16.5, 7.5)
    hit = (12.75, 11.25)
    burst = poly(sparkle(*hit, 4, 0.34), closed=True, r=L(S, 0, 0.2))
    keep = grow(burst, 2)
    return [
        shell(minus(circle(*big, 5.5), keep)),
        shell(minus(circle(*small, 4), keep)),
        mark(burst),
        dot(*polar(*hit, 7.5, -135), 1.1), dot(*polar(*hit, 7.5, 45), 1.1),
    ]


# ============================================================================ rocket engines

def _bell(m, S, top=0.0, h=6.0, w0=1.75, w1=3.75):
    return shell(poly([m(-w0, top), m(w0, top), m(w1, top + h), m(-w1, top + h)], closed=True, r=S.r * 0.5))


@icon("shock-diamonds", CAT, "Rocket nozzle with a long exhaust plume showing a chain of bright diamonds",
      tags=["shock diamonds", "mach diamonds", "exhaust plume", "rocket engine", "supersonic", "flame"])
def _(S):
    return [
        shell(poly([(9.5, 2.5), (14.5, 2.5), (16.5, 7.5), (7.5, 7.5)], closed=True, r=S.r * 0.5)),
        line(seg(8, 10, 10.5, 21.5)), line(seg(16, 10, 13.5, 21.5)),
        mark(poly([(12, 10), (13.5, 12), (12, 14), (10.5, 12)], closed=True, r=L(S, 0, 0.4))),
        mark(poly([(12, 15.5), (13.25, 17.25), (12, 19), (10.75, 17.25)], closed=True, r=L(S, 0, 0.4))),
    ]


# ============================================================================ constellations and asterisms

_CROWN = [polar(12, 6, 10, a) for a in (22, 44, 66, 90, 114, 136, 158)]


def _crown_filled():
    return U(*[P(poly(sparkle(x, y, 3.5, 0.34), closed=True)) if i == 3 else P(circle(x, y, 1.75)) for i, (x, y) in enumerate(_CROWN)])


@icon("northern-crown-constellation", CAT, "Seven stars in a gentle semicircular arc, the Northern Crown",
      tags=["corona borealis", "northern crown", "constellation", "star pattern", "night sky", "astronomy"],
      filled=_crown_filled)
def _(S):
    out = []
    for i, (x, y) in enumerate(_CROWN):
        if i == 3:
            out.append(mark(poly(sparkle(x, y, 3, 0.32), closed=True, r=L(S, 0, 0.3))))
        else:
            out.append(dot(x, y, L(S, 1.25, 1.35)))
    return out


_TEAPOT = [(10.5, 2.5), (6.5, 8.5), (14.5, 8.5), (6.5, 18.5), (14.5, 19), (2, 13.5), (21, 8), (21, 17)]
_TEAPOT_E = [(1, 0), (0, 2), (1, 2), (2, 4), (4, 3), (3, 1), (1, 5), (5, 3), (2, 6), (6, 7), (7, 4)]


@icon("teapot-asterism", CAT, "Eight stars joined into the outline of a teapot with a lid, spout and handle",
      tags=["teapot asterism", "sagittarius", "teapot", "asterism", "star pattern", "summer sky"])
def _(S):
    return [*[dot(x, y, L(S, 1.25, 1.35)) for x, y in _TEAPOT], *[line(star_link(_TEAPOT[a], _TEAPOT[b], 2.4)) for a, b in _TEAPOT_E]]


_SQUARE = [(4.5, 5), (19, 4.5), (19.5, 19), (5, 19.5)]


@icon("great-square-asterism", CAT, "Four bright stars joined in a large square with a few faint stars inside",
      tags=["great square", "pegasus", "asterism", "autumn sky", "star pattern", "constellation"])
def _(S):
    return [
        *[shell(circle(x, y, 1.75)) for x, y in _SQUARE],
        *[line(star_link(_SQUARE[i], _SQUARE[(i + 1) % 4], 3.75)) for i in range(4)],
        dot(10, 10.5, L(S, 0.9, 1)), dot(14.5, 14, L(S, 0.9, 1)),
    ]


_DRACO = [(3.5, 4.5), (8, 3), (9, 7.5), (4.5, 8.5), (12.5, 11), (9, 15.5), (13, 19.5), (18.5, 18), (17.5, 12.5), (20.5, 6.5)]
_DRACO_E = [(0, 1), (1, 2), (2, 3), (3, 0), (2, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)]


@icon("draco-constellation", CAT, "Long winding chain of stars ending in a small four star head, the Dragon",
      tags=["draco", "dragon constellation", "constellation", "circumpolar", "star pattern", "night sky"])
def _(S):
    return [*[dot(x, y, L(S, 1.2, 1.3)) for x, y in _DRACO], *[line(star_link(_DRACO[a], _DRACO[b], 2.3)) for a, b in _DRACO_E]]


_CEPH = [(6.5, 19.5), (17.5, 18.5), (18, 9.5), (6, 10.5), (11.5, 3)]
_CEPH_E = [(0, 1), (1, 2), (2, 3), (3, 0), (3, 4), (4, 2)]


@icon("cepheus-constellation", CAT, "Five stars joined into a simple house outline with a pointed roof",
      tags=["cepheus", "king constellation", "constellation", "circumpolar", "star pattern", "house"])
def _(S):
    return [*[shell(circle(x, y, 1.75)) for x, y in _CEPH], *[line(star_link(_CEPH[a], _CEPH[b], 3.75)) for a, b in _CEPH_E]]


_HEX = [(12, 2.5), (19.5, 6.5), (20.5, 15), (13.5, 21), (5, 18.5), (3.5, 9)]


@icon("winter-hexagon", CAT, "Six bright stars joined into a large hexagon with one star in the middle",
      tags=["winter hexagon", "winter circle", "asterism", "winter sky", "star pattern", "orion"])
def _(S):
    return [
        *[dot(x, y, L(S, 1.35, 1.45)) for x, y in _HEX],
        *[line(star_link(_HEX[i], _HEX[(i + 1) % 6], 2.75)) for i in range(6)],
        mark(poly(sparkle(12, 12, 3, 0.32), closed=True, r=L(S, 0, 0.3))),
    ]


# ============================================================================ landers

@icon("lunar-ascent-stage", CAT, "Top half of a lunar lander lifting off on a flame and leaving its legged base behind",
      tags=["ascent stage", "lunar module", "liftoff", "moon landing", "lander", "ascent"])
def _(S):
    return [
        shell(poly([(8.5, 2.5), (15.5, 2.5), (17.5, 5.5), (15.5, 8.5), (8.5, 8.5), (6.5, 5.5)], closed=True, r=S.r * 0.5)),
        detail(seg(10, 5.5, 14, 5.5)),
        mark(poly([(10.5, 10.5), (13.5, 10.5), (12, 13)], closed=True, r=L(S, 0, 0.4))),
        shell(rect(7.5, 15, 9, 3.5, min(S.R, 1))),
        line(poly([(8.5, 18.5), (5, 21.5)])), line(poly([(15.5, 18.5), (19, 21.5)])),
        line(seg(3, 21.5, 7, 21.5)), line(seg(17, 21.5, 21, 21.5)),
    ]


# ============================================================================ observing and safety

_SLASH = seg(20.5, 3.5, 3.5, 20.5)


def _band(w):
    return path_to_d(ST(_SLASH, w, "butt", "miter"))


@icon("sun-viewing-warning", CAT, "Eye beneath a bright sun with a bold slash through them: never look at the sun",
      tags=["do not look at the sun", "eye safety", "solar viewing", "warning", "eclipse safety", "eye damage"])
def _(S):
    eye = L(S, "M3 15.5Q12 6.5 21 15.5Q12 24.5 3 15.5Z", "M3 15.5C6 11 9 10.5 12 10.5S18 11 21 15.5C18 20 15 20.5 12 20.5S6 20 3 15.5Z")
    band = _band(7)
    return [
        shell(minus(eye, band)),
        mark(minus(circle(14.5, 16, 2.25), band)),
        shell(circle(10, 6, 2)),
        *[line(d) for d in rays(10, 6, 3.5, 4.75, (-135, -90, -45, 135, 180))],
        line(_SLASH),
    ]


@icon("eclipse-path", CAT, "Globe crossed by the narrow dark path of totality beneath the moon",
      tags=["eclipse path", "path of totality", "eclipse map", "solar eclipse", "umbra", "shadow track"])
def _(S):
    band = path_to_d(ST("M3 17C7 13 12 11.5 19 11", 3, "butt", "round"))
    return [
        shell(circle(11, 14, 7.5)),
        mark(inter(band, circle(11, 14, 5.5))),
        dot(19.5, 4.5, L(S, 2.25, 2.5)),
    ]


@icon("mountain-observatory", CAT, "Observatory domes on a mountain top under a few stars",
      tags=["mountain observatory", "summit telescope", "observatory", "high altitude", "domes", "astronomy"])
def _(S):
    mtn = union(poly([(2, 21.5), (7, 12.5), (17, 12.5), (22, 21.5)], closed=True),
                circle(10, 12.5, 2.75), circle(15.25, 12.5, 1.75))
    return [
        shell(mtn),
        detail(seg(10, 9.75, 10, 12)),
        dot(4, 5, 1.1), dot(19.5, 4, 1.1),
        mark(poly(sparkle(14, 4.5, 2.25, 0.34), closed=True, r=L(S, 0, 0.2))),
    ]


@icon("airborne-observatory", CAT, "Large jet plane with an open door near its tail showing a telescope",
      tags=["airborne observatory", "flying telescope", "infrared astronomy", "jet", "aircraft", "observatory"])
def _(S):
    body = union(L(S, "M2.5 10H18.5C20.5 10 22 11.5 22 13S20.5 16 18.5 16H4Z",
                   "M2.5 10H18.5C20.5 10 22 11.5 22 13S20.5 16 18.5 16H5A1.5 1.5 0 0 1 3.5 15Z"),
                 poly([(2.5, 10), (2.5, 5), (5, 5), (7.5, 10)], closed=True))
    return [
        shell(minus(body, rect(8, 8, 3.5, 3.5))),
        dot(9.75, 13, 1.25),
        line(seg(13.5, 18, 10, 21)),
    ]


@icon("earth-at-night", CAT, "Dark globe dotted with clusters of city lights",
      tags=["earth at night", "city lights", "night lights", "light pollution", "globe", "night side"])
def _(S):
    r = L(S, 1, 1.1)
    pts = [(7.5, 8), (10, 7), (9, 10.5), (15.5, 9.5), (17, 12), (6.5, 14), (9, 15.5), (13.5, 16.5), (16, 17), (14.5, 13)]
    return [shell(circle(12, 12, 9)), *[dot(x, y, r) for x, y in pts]]


@icon("fast-radio-burst", CAT, "Radio dish receiving a single sharp spike of signal from deep space",
      tags=["fast radio burst", "frb", "radio signal", "radio astronomy", "pulse", "transient"])
def _(S):
    return [
        shell(L(S, "M3 12.5A6.4 6.4 0 0 0 12 21.5Z", "M3.7 11.8A6.4 6.4 0 0 0 12.7 20.8A1 1 0 0 0 12.7 19.4L5.1 11.8A1 1 0 0 0 3.7 11.8Z")),
        line(seg(7.5, 17, 11, 13.5)),
        dot(12, 12.5, 1.25),
        line(poly([(12, 6.5), (15, 6.5), (16.5, 2.5), (18, 10.5), (19.5, 6.5), (22, 6.5)], r=S.r * 0.4), stroke_miterlimit="2"),
    ]


@icon("polar-alignment", CAT, "Telescope mount with its tilted axis pointing along a dashed line to a bright star",
      tags=["polar alignment", "pole star", "equatorial mount", "polaris", "telescope setup", "astrophotography"])
def _(S):
    m = axis((7.5, 16), -50)
    housing = [m(0, -1.75), m(6.5, -1.75), m(6.5, 1.75), m(0, 1.75)]
    return [
        shell(poly(housing, closed=True, r=S.r * 0.4)),
        line(seg(7.5, 18, 4, 21.5)), line(seg(7.5, 18, 11, 21.5)),
        line(seg(*m(8.5, 0), *m(10, 0))), line(seg(*m(12, 0), *m(13.5, 0))),
        mark(poly(sparkle(*m(16.75, 0), 2.9, 0.32), closed=True, r=L(S, 0, 0.2))),
    ]


@icon("moonquake", CAT, "Moon disk with a jagged seismograph trace across its lower half",
      tags=["moonquake", "lunar seismology", "seismograph", "quake", "tremor", "moon"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        mark(poly([(7, 6.5), (11, 5.5), (12, 8.5), (8.5, 10)], closed=True, r=L(S, 0, 1))),
        detail(poly([(3, 14.5), (7, 14.5), (8.5, 11.5), (11, 18.5), (13.5, 11.5), (15, 16.5), (16.5, 14.5), (21, 14.5)], r=S.r * 0.5), stroke_miterlimit="2"),
    ]


@icon("space-meal-tray", CAT, "Food tray with packets held by straps and a spoon clipped at the side",
      tags=["space food", "meal tray", "astronaut food", "food packets", "space station", "eating"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 13, 17, min(S.R, 2.5))),
        detail(rect(5, 6, 8, 4.5, 0)),
        detail(rect(5, 13.5, 8, 4.5, 0)),
        shell(ellipse(19.75, 6, 1.75, 2.5) if S.name == "rounded" else poly([(19.75, 3.5), (21.5, 5), (21.5, 7), (19.75, 8.5), (18, 7), (18, 5)], closed=True)),
        line(seg(19.75, 10.5, 19.75, 20.5)),
    ]


@icon("comet-lander", CAT, "Small box lander on three legs perched on a lumpy icy comet",
      tags=["comet lander", "touchdown", "comet landing", "lander", "probe", "comet"])
def _(S):
    ground = L(S, "M2 22.5V18C4 15.5 6.5 16 8.5 16.5C10.5 15 14 14.5 16 15.5C18.5 14.5 21 16 22 18.5V22.5Z",
               "M2 20.5V18C4 15.5 6.5 16 8.5 16.5C10.5 15 14 14.5 16 15.5C18.5 14.5 21 16 22 18.5V20.5A2 2 0 0 1 20 22.5H4A2 2 0 0 1 2 20.5Z")
    return [
        shell(ground),
        shell(rect(8.5, 3.5, 7, 5, min(S.R, 1))),
        line(seg(9.5, 8.5, 7, 13)), line(seg(14.5, 8.5, 17, 12.5)), line(seg(12, 8.5, 12, 12.5)),
        line(seg(15.5, 6, 19, 6)),
    ]
