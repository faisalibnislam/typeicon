"""TypeIcon Core: nature and weather.

The plain sun, moon (crescent) and cloud live in icons.py (v0.1); the weather icons here reuse their
proportions: the cloud is the v0.1 cloud scaled with `_tx`, so every weather icon shares one cloud.
Objects drawn behind another (a sun behind a cloud, a cloud behind a bolt) are cut with a 2 px gap:
the stroke styles emit the cut outline as a solid region, and Filled is designed explicitly.
"""
import math
import re

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, LINE, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "nature"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


_NUM = re.compile(r"[A-Za-z]|-?\d*\.?\d+(?:e-?\d+)?")


def _tx(d, s=1.0, dx=0.0, dy=0.0, cx=12.0, cy=12.0, mirror=False):
    """Uniformly scale a d-string about (cx, cy), optionally mirror it horizontally, then translate.
    Handles absolute M L H V C S Q T A Z (enough for the shapes in this module)."""
    toks = _NUM.findall(d)
    out, i, cmd = [], 0, None
    sx = -s if mirror else s

    def X(v):
        return fmt(cx + (float(v) - cx) * sx + dx)

    def Y(v):
        return fmt(cy + (float(v) - cy) * s + dy)

    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            out.append(t)
            i += 1
            if cmd in "Zz":
                continue
        if cmd in "MLT":
            out.append(f"{X(toks[i])} {Y(toks[i + 1])}")
            i += 2
        elif cmd == "H":
            out.append(X(toks[i]))
            i += 1
        elif cmd == "V":
            out.append(Y(toks[i]))
            i += 1
        elif cmd in "CSQ":
            n = {"C": 3, "S": 2, "Q": 2}[cmd]
            out.append(" ".join(f"{X(toks[i + 2 * k])} {Y(toks[i + 2 * k + 1])}" for k in range(n)))
            i += 2 * n
        elif cmd == "A":
            rx, ry, rot, la, sw, x, y = toks[i:i + 7]
            if mirror:
                sw = "1" if sw == "0" else "0"
            out.append(f"{fmt(float(rx) * s)} {fmt(float(ry) * s)} {rot} {la} {sw} {X(x)} {Y(y)}")
            i += 7
        else:
            raise ValueError(f"unsupported command {cmd}")
    return "".join(out)


# The v0.1 cloud (icons.py): Line has a flat base meeting the lobes at corners, Rounded flows.
_CLOUD_LINE = "M4.5 19H19.5A3.8 3.8 0 0 0 18 11.7A6 6 0 0 0 6.5 10A4.7 4.7 0 0 0 4.5 19Z"
_CLOUD_ROUND = "M7 19H17.5A4.5 4.5 0 0 0 18 10.03A6 6 0 0 0 6.34 9.1A5 5 0 0 0 7 19Z"


def cloud(S, s=1.0, dx=0.0, dy=0.0, mirror=False):
    """The shared cloud, scaled about (12, 12) then moved."""
    return _tx(_CLOUD_LINE if S.name == "line" else _CLOUD_ROUND, s, dx, dy, mirror=mirror)


def top_cloud(S):
    """Cloud raised to the top of the canvas, leaving 17–22 for precipitation (base at y 14)."""
    return cloud(S, 0.72, 0, -3.5)


def region(d):
    """Area covered by a closed outline filled to its outer stroke edge."""
    return U(P(d), ST(d, 2))


def grow(p, g):
    """Path region p expanded by g px."""
    return U(p, ST(path_to_d(p), 2 * g, "round", "round"))


def cut_strokes(S, ds, cutter, gap=2.0):
    """Stroke outlines of ds (in style S) with grow(cutter, gap) removed, for things seen behind another."""
    body = U(*[ST(d, 2, S.cap, S.join) for d in ds])
    return solid(path_to_d(D(body, grow(cutter, gap))))


def sun_rays(cx, cy, r0, r1, n=8, start=0.0):
    return [seg(*polar(cx, cy, r0, start + k * 360 / n), *polar(cx, cy, r1, start + k * 360 / n)) for k in range(n)]


def slant(x, y0, y1, k=0.35):
    """A falling streak from (x, y0) to y1, leaning left as it falls."""
    return seg(x + (y1 - y0) * k / 2, y0, x - (y1 - y0) * k / 2, y1)


def weather_filled(draw):
    """Filled design for a top-cloud weather icon: solid cloud + heavier precipitation."""
    def f():
        from dsl import filled_region
        return filled_region(draw(LINE))
    return f


# ============================================================================ precipitation

@icon("cloud-rain", CAT, "Cloud with three falling rain streaks", tags=["rain", "rainy", "shower", "weather", "forecast", "wet"],
      aliases=["rain"])
def _(S):
    return [shell(top_cloud(S)), *[line(slant(x, 17.5, 21)) for x in (8, 12, 16)]]


@icon("drizzle", CAT, "Cloud with fine droplets falling; light rain", tags=["light rain", "rain", "weather", "forecast", "spitting", "shower"])
def _(S):
    return [shell(top_cloud(S)), *[dot(x, 17.9, 1.1) for x in (7.5, 12, 16.5)], *[dot(x, 20.9, 1.1) for x in (9.75, 14.25)]]


@icon("hail", CAT, "Cloud with hailstones falling", tags=["hailstones", "ice", "storm", "weather", "forecast", "sleet"])
def _(S):
    return [shell(top_cloud(S)), dot(7.5, 18.4, 1.75), dot(12, 20.2, 1.75), dot(16.5, 18.4, 1.75)]


@icon("sleet", CAT, "Cloud with rain streaks mixed with ice pellets", tags=["rain and snow", "freezing rain", "ice", "weather", "forecast", "wintry mix"])
def _(S):
    return [shell(top_cloud(S)), line(slant(8, 17.5, 21)), line(slant(15, 17.5, 21)), dot(11.3, 20.2, 1.25), dot(18.3, 20.2, 1.25)]


def _asterisk(cx, cy, r):
    return [seg(cx, cy - r, cx, cy + r), seg(*polar(cx, cy, r, -30), *polar(cx, cy, r, 150)), seg(*polar(cx, cy, r, 30), *polar(cx, cy, r, 210))]


_SNOW_C = (12, 18.6, 3.3)


def _snow_flake_ds():
    cx, cy, r = _SNOW_C
    return [seg(*polar(cx, cy, r, a), *polar(cx, cy, r, a + 180)) for a in (-90, -30, 30)]


def _snow_filled():
    flake = U(*[ST(d, 2.2, "round", "round") for d in _snow_flake_ds()])
    return U(D(region(top_cloud(LINE)), grow(flake, 1.5)), flake, P(circle(5.5, 19.2, 1.3)), P(circle(18.5, 19.2, 1.3)))


@icon("cloud-snow", CAT, "Cloud with a snowflake falling", tags=["snow", "snowy", "snowfall", "winter", "weather", "forecast"],
      aliases=["snow"], filled=_snow_filled)
def _(S):
    flakes = _snow_flake_ds()
    return [cut_strokes(S, [top_cloud(S)], U(*[ST(d, 2) for d in flakes])), *[line(d) for d in flakes],
            dot(5.5, 19.2, 1.2), dot(18.5, 19.2, 1.2)]


_BOLT = [(13.5, 11), (9.5, 16.5), (14, 16.5), (11, 21)]


def _cloud_bolt_parts(S):
    bolt = poly(_BOLT, r=S.r)
    return [cut_strokes(S, [top_cloud(S)], ST(poly(_BOLT), 2)), line(bolt, stroke_miterlimit="8")]


@icon("cloud-lightning", CAT, "Storm cloud with a lightning bolt", tags=["thunderstorm", "storm", "lightning", "thunder", "weather", "forecast"],
      aliases=["thunderstorm"],
      filled=lambda: U(D(region(top_cloud(LINE)), grow(ST(poly(_BOLT), 2.5, "butt", "miter", 8), 1.5)),
                       ST(poly(_BOLT), 2.5, "butt", "miter", 8)))
def _(S):
    return _cloud_bolt_parts(S)


# ============================================================================ sun, moon and cloud

def _sun_small(S, cx, cy, s):
    """The v0.1 sun (circle r 4, rays 7.25–9.75) scaled by s."""
    return [circle(cx, cy, 4 * s)] + sun_rays(cx, cy, 7.25 * s, 9.75 * s)


_CS_CLOUD = dict(s=0.74, dx=2.4, dy=2.9)


@icon("cloud-sun", CAT, "Sun partly hidden behind a cloud; partly cloudy", tags=["partly cloudy", "sunny intervals", "weather", "forecast", "cloud", "sun"],
      aliases=["partly-cloudy", "sun-cloud"],
      filled=lambda: U(D(U(P(circle(8.75, 8.75, 4)), *[ST(d, 2.5) for d in sun_rays(8.75, 8.75, 5.4, 6.75)[3:]]),
                         grow(region(cloud(LINE, **_CS_CLOUD)), 1.75)),
                       region(cloud(LINE, **_CS_CLOUD))))
def _(S):
    c = cloud(S, **_CS_CLOUD)
    sun = [circle(8.75, 8.75, 3)] + sun_rays(8.75, 8.75, 5.25, 6.5)[3:]
    return [cut_strokes(S, sun, region(c)), shell(c)]


_MOON = "M20.5 14.5A8.5 8.5 0 1 1 9.5 3.5A7 7 0 0 0 20.5 14.5Z"
_CM_CLOUD = dict(s=0.74, dx=-2.2, dy=2.9)
_CM_MOON = dict(s=0.56, dx=3.7, dy=-3.6)


@icon("cloud-moon", CAT, "Crescent moon partly hidden behind a cloud; cloudy night", tags=["night", "cloudy night", "partly cloudy", "weather", "forecast", "moon"],
      aliases=["cloudy-night"],
      filled=lambda: U(D(region(_tx(_MOON, **_CM_MOON)), grow(region(cloud(LINE, **_CM_CLOUD)), 1.75)),
                       region(cloud(LINE, **_CM_CLOUD))))
def _(S):
    c = cloud(S, **_CM_CLOUD)
    return [cut_strokes(S, [_tx(_MOON, **_CM_MOON)], region(c)), shell(c)]


@icon("fog", CAT, "Cloud over drifting bands of mist", tags=["mist", "haze", "foggy", "weather", "forecast", "visibility"],
      aliases=["mist"])
def _(S):
    return [shell(cloud(S, 0.62, 0, -5.2)), line(seg(3, 16.5, 14, 16.5)), line(seg(17, 16.5, 21, 16.5)),
            line(seg(6, 20.5, 19, 20.5))]


# ============================================================================ wind and storms

@icon("wind", CAT, "Gusts of wind curling at their ends", tags=["windy", "breeze", "gust", "air", "weather", "blow"],
      aliases=["windy"])
def _(S):
    return [line("M3 9.5H14.5A2.5 2.5 0 1 0 12 7"),
            line("M3 13.5H18.5A2.5 2.5 0 1 1 16 16"),
            line("M3 17.5H10")]


@icon("tornado", CAT, "Funnel of stacked winds; a tornado", tags=["twister", "cyclone", "funnel", "storm", "weather", "disaster"],
      aliases=["twister"])
def _(S):
    rows = [(3, 21, 4), (5, 19, 8), (7.5, 17, 12), (10, 15.5, 16), (12, 14.5, 20)]
    return [line(seg(a, y, b, y)) for a, b, y in rows]


@icon("hurricane", CAT, "Tropical cyclone symbol: an eye with two spiral arms", tags=["cyclone", "typhoon", "storm", "tropical storm", "weather", "disaster"],
      aliases=["cyclone", "typhoon"])
def _(S):
    return [shell(circle(12, 12, 3.25)),
            line("M12 8.75C6.5 8.75 3 11.5 2.5 17"),
            line("M12 15.25C17.5 15.25 21 12.5 21.5 7")]


# ============================================================================ snow, water, heat

def _flake(S, cx, cy, R, branch=True):
    parts = []
    for k in range(6):
        a = -90 + k * 60
        parts.append(line(seg(cx, cy, *polar(cx, cy, R, a))))
        if branch:
            ax, ay = polar(cx, cy, R * 0.6, a)
            b1 = polar(ax, ay, R * 0.34, a - 50)
            b2 = polar(ax, ay, R * 0.34, a + 50)
            parts.append(line(poly([b1, (ax, ay), b2], r=S.r * 0.5)))
    return parts


@icon("snowflake", CAT, "Six-armed snowflake", tags=["snow", "winter", "cold", "frost", "freeze", "ice"])
def _(S):
    return _flake(S, 12, 12, 9)


@icon("umbrella", CAT, "Open umbrella with a hooked handle", tags=["rain", "protection", "weather", "parasol", "insurance", "shelter"])
def _(S):
    canopy = "M3 12A9 9 0 0 1 21 12A3 3 0 0 0 15 12A3 3 0 0 0 9 12A3 3 0 0 0 3 12Z"
    return [shell(canopy), line("M12 12V18.5A2 2 0 0 1 8 18.5")]


@icon("rainbow", CAT, "Rainbow of three arcs", tags=["weather", "colors", "pride", "hope", "sky", "spectrum"])
def _(S):
    return [line(arc(12, 17.5, r, 180, 360)) for r in (9.5, 6, 2.5)]


@icon("water-drop", CAT, "A drop of water above a ripple", tags=["water", "droplet", "liquid", "humidity", "hydration", "aqua"],
      aliases=["droplet", "raindrop"])
def _(S):
    d = L(S, "M12 2.5C12 2.5 16.5 7.5 16.5 10.5A4.5 4.5 0 0 1 7.5 10.5C7.5 7.5 12 2.5 12 2.5Z",
          "M11.3 3.3Q12 2.5 12.7 3.3C13.9 4.8 16.5 8 16.5 10.5A4.5 4.5 0 0 1 7.5 10.5C7.5 8 10.1 4.8 11.3 3.3Z")
    return [shell(d, stroke_miterlimit="8" if S.name == "line" else "4"),
            line("M3 19.5C5 17.8 7 17.8 9 19.5C11 21.2 13 21.2 15 19.5C17 17.8 19 17.8 21 19.5")]


def _thermo(S, x, level):
    d = L(S, f"M{x - 2} 14.63V3H{x + 2}V14.63A3.5 3.5 0 1 1 {x - 2} 14.63Z",
          f"M{x - 2} 14.63V5A2 2 0 0 1 {x + 2} 5V14.63A3.5 3.5 0 1 1 {x - 2} 14.63Z")
    return [shell(d), detail(seg(x, level, x, 16)), dot(x, 17.5, 1.75)]


@icon("thermometer-hot", CAT, "Thermometer reading high beside a sun", tags=["hot", "heat", "temperature", "warm", "summer", "weather"],
      aliases=["hot-weather"])
def _(S):
    return [*_thermo(S, 7.5, 7), shell(circle(17, 7.5, 2.2)), *[line(d) for d in sun_rays(17, 7.5, 4.3, 5.8)]]


@icon("thermometer-cold", CAT, "Thermometer reading low beside a snowflake", tags=["cold", "freezing", "temperature", "winter", "frost", "weather"],
      aliases=["cold-weather"])
def _(S):
    return [*_thermo(S, 7.5, 14), *_flake(S, 17, 7.5, 4.5, branch=False)]


@icon("heatwave", CAT, "Blazing sun above rising heat shimmer", tags=["heat", "hot", "heat wave", "summer", "drought", "weather"],
      aliases=["heat-wave"])
def _(S):
    wav = "M{x} 21C{a} 19.75 {a} 18.75 {x} 17.5C{b} 16.25 {b} 15.25 {x} 14"
    rays = sun_rays(12, 7.5, 4.5, 5.75)
    return [shell(circle(12, 7.5, 2.5)), *[line(rays[k]) for k in (0, 4, 5, 6, 7)],
            *[line(wav.format(x=x, a=fmt(x - 1.6), b=fmt(x + 1.6))) for x in (7, 12, 17)]]


# ============================================================================ sky and space

def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def sparkle(cx, cy, R, r):
    """Four-pointed sparkle star."""
    return [polar(cx, cy, R if k % 2 == 0 else r, -90 + k * 45) for k in range(8)]


@icon("star-night", CAT, "Crescent moon with twinkling stars; a clear night", tags=["night", "starry", "clear night", "stars", "moon", "weather"],
      aliases=["starry-night"])
def _(S):
    return [shell(_tx(_MOON, 0.74, -2.6, 2.6)),
            Part("dot", poly(sparkle(17.5, 6.5, 4, 1.25), closed=True, r=L(S, 0, 0.5))),
            Part("dot", poly(sparkle(19.5, 14, 2.5, 0.85), closed=True, r=L(S, 0, 0.4)))]


def _comet_tail(cx, cy, k, t0, t1, deg=135):
    u = (math.cos(math.radians(deg)), math.sin(math.radians(deg)))
    n = (-u[1], u[0])
    bx, by = cx + n[0] * k, cy + n[1] * k
    return seg(bx + u[0] * t0, by + u[1] * t0, bx + u[0] * t1, by + u[1] * t1)


@icon("comet", CAT, "Comet with a glowing head and a long tail", tags=["space", "astronomy", "halley", "sky", "tail", "celestial"])
def _(S):
    cx, cy = 16, 8
    return [shell(circle(cx, cy, 3.5)),
            line(_comet_tail(cx, cy, 0, 5.5, 16)),
            line(_comet_tail(cx, cy, 3.3, 4.6, 10.5)),
            line(_comet_tail(cx, cy, -3.3, 4.6, 10.5))]


@icon("meteor", CAT, "Rocky meteor burning through the sky with speed trails", tags=["meteorite", "asteroid", "space", "impact", "fireball", "astronomy"],
      aliases=["meteorite"])
def _(S):
    rock = poly([(4, 13), (7.5, 9.5), (12, 10.5), (14, 14.5), (12, 19), (7, 20.5), (3.5, 17.5)], closed=True, r=S.r)
    return [shell(rock), dot(8.5, 15.5, 1.5),
            line(seg(13, 8, 18.5, 2.5)), line(seg(16.5, 11.5, 21, 7)), line(seg(9.5, 6.5, 12, 4))]


@icon("planet", CAT, "Banded gas-giant planet with a small moon", tags=["space", "jupiter", "astronomy", "solar system", "gas giant", "world"])
def _(S):
    # Bands follow the sphere: faceted in Line, smooth in Rounded.
    b1 = [(3.62, 11.5), (7.5, 12.9), (13.5, 12.9), (17.38, 11.5)]
    b2 = [(4.4, 16.6), (8, 17.8), (13, 17.8), (16.6, 16.6)]
    return [shell(circle(10.5, 13.5, 7)), detail(poly(b1, r=L(S, 0, 4))), detail(poly(b2, r=L(S, 0, 4))),
            shell(circle(19.5, 4.5, 1.75))]


_EARTH_LAND = [
    [(0, 4), (5.5, 5), (8.5, 6.5), (9, 9), (7, 10.5), (7.5, 13), (9.5, 15), (8, 18.5), (6.5, 22), (0, 22)],
    [(12, 0), (12, 4.5), (14.5, 6), (13.5, 8.5), (15.5, 10.5), (18.5, 10), (20, 12.5), (24, 12.5), (24, 0)],
]


def _earth_land(S):
    disc = P(circle(12, 12, 9))
    return [path_to_d(I(P(poly(pts, closed=True, r=S.r * 1.3)), disc)) for pts in _EARTH_LAND]


@icon("earth", CAT, "Planet Earth with continents", tags=["world", "globe", "planet", "geography", "international", "global"],
      aliases=["planet-earth"],
      filled=lambda: D(P(circle(12, 12, 10)), *[I(P(poly(pts, closed=True)), P(circle(12, 12, 8))) for pts in _EARTH_LAND]))
def _(S):
    return [shell(circle(12, 12, 9)), *[detail(d) for d in _earth_land(S)]]


@icon("moon-full", CAT, "Full moon with craters", tags=["full moon", "lunar", "night", "moon", "astronomy", "month"],
      aliases=["full-moon"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(arc(8.5, 9, 2.5, 100, 40)), detail(arc(15, 15.5, 2.75, 100, 40)), dot(15.5, 8.5, 1.2), dot(8, 15.8, 1)]


# ============================================================================ land and water

@icon("volcano", CAT, "Erupting volcano", tags=["eruption", "lava", "mountain", "magma", "disaster", "geology"])
def _(S):
    body = poly([(2.5, 20.5), (8, 10.5), (10, 12), (12, 10.5), (14, 12), (16, 10.5), (21.5, 20.5)], closed=True, r=S.r)
    return [shell(body), line(seg(12, 7.5, 12, 3)), line(seg(8.5, 8, 6, 4.5)), line(seg(15.5, 8, 18, 4.5))]


@icon("wave", CAT, "Ocean wave curling over", tags=["ocean", "sea", "surf", "tide", "water", "beach"],
      aliases=["ocean-wave"])
def _(S):
    return [line("M3 17C6 17 7.5 14.5 9 11C10.5 7.5 13 5 16.5 5C19 5 21 6.8 21 9C21 11 19.5 12.5 17.5 12.5C16 12.5 15 11.5 15 10"),
            line("M3 21C5 19.7 7 19.7 9 21C11 22.3 13 22.3 15 21C17 19.7 19 19.7 21 21" if False else "M3 20.5C5 19.2 7 19.2 9 20.5C11 21.8 13 21.8 15 20.5C17 19.2 19 19.2 21 20.5")]


@icon("fire", CAT, "Flame with three tongues", tags=["flame", "burn", "hot", "blaze", "campfire", "heat"],
      aliases=["flame"])
def _(S):
    d = ("M12 21.5C7.9 21.5 5 18.6 5 15C5 12.2 5.9 10.1 7 8C7.8 9.3 8.5 10 9.3 10.5C9.3 7.2 10.5 4.8 12 2.5"
         "C13.2 4.6 14.3 6.8 14.3 9.5C15.5 8.6 16.8 7.5 17.5 6.5C18.5 8.8 19 11.5 19 15C19 18.6 16.1 21.5 12 21.5Z")
    return [shell(d, stroke_miterlimit="8"), detail("M9.5 16.5C9.5 15 10.8 13.8 12 12.5C13.2 13.8 14.5 15 14.5 16.5")]


@icon("iceberg", CAT, "Iceberg with most of its mass below the waterline", tags=["ice", "glacier", "arctic", "polar", "cold", "hidden"])
def _(S):
    berg = poly([(10, 5), (12, 7), (14.5, 3.5), (17.5, 11), (20, 14.5), (16.5, 20.5), (8, 20.5), (4, 14.5), (6.5, 11)], closed=True, r=S.r)
    return [shell(berg), detail(seg(6.5, 11, 17.5, 11)), line(seg(2, 11, 4.5, 11)), line(seg(19.5, 11, 22, 11))]


@icon("desert", CAT, "Cactus among sand dunes under the sun", tags=["dunes", "sand", "sahara", "arid", "dry", "hot"])
def _(S):
    return [shell(circle(17.5, 6, 2.5)),
            line(seg(7, 15, 7, 4.5)), line(poly([(7, 11.5), (4, 11.5), (4, 8.5)], r=S.r)), line(poly([(7, 9.5), (10, 9.5), (10, 7)], r=S.r)),
            line("M11.5 15.5C14.5 13 18 12.8 21.5 14.2"),
            line("M2.5 19.5C7 16.5 14 16.5 21.5 20.5")]


@icon("waterfall", CAT, "Water pouring over a ledge into a pool", tags=["falls", "cascade", "river", "water", "nature", "cliff"])
def _(S):
    return [line("M3 3.5H11A6 6 0 0 1 17 9.5V15.5"),
            line("M3 7.5H11A2 2 0 0 1 13 9.5V15.5"),
            line(poly([(3, 11.5), (9, 11.5), (9, 15.5)], r=L(S, 0, 1))),
            line("M3 19.5C5 18.2 7 18.2 9 19.5C11 20.8 13 20.8 15 19.5C17 18.2 19 18.2 21 19.5")]


@icon("river", CAT, "River winding into the distance", tags=["stream", "water", "creek", "flow", "valley", "nature"])
def _(S):
    return [line("M10.5 3C7.5 5.5 7 8.5 9.5 11C12 13.5 10 18 3.5 21"),
            line("M14.5 3C11.8 5.5 12 8.5 14.5 11C17 13.5 17.5 18 12 21")]


@icon("lake", CAT, "Lake below mountains", tags=["pond", "water", "mountains", "landscape", "nature", "reservoir"])
def _(S):
    return [line(poly([(3, 10), (8, 4), (11, 7.5), (14, 4.5), (21, 10)], r=S.r)),
            shell(ellipse(12, 16.5, 9, 4.5)), detail("M7.5 16.5C9 15.3 10.5 15.3 12 16.5C13.5 17.7 15 17.7 16.5 16.5")]


@icon("cave", CAT, "Rocky hill with a cave mouth", tags=["cavern", "grotto", "rock", "shelter", "explore", "mountain"])
def _(S):
    rock = poly([(2.5, 20.5), (4.5, 11), (9, 5), (14.5, 4), (19.5, 8.5), (21.5, 20.5)], closed=True, r=S.r)
    mouth = "M8 23V16A4 4 0 0 1 16 16V23Z"
    return [shell(minus(rock, mouth))]


@icon("canyon", CAT, "Canyon walls with a river between them", tags=["gorge", "valley", "cliff", "grand canyon", "ravine", "landscape"],
      aliases=["gorge"])
def _(S):
    return [line(poly([(2, 5), (6, 5), (7.5, 10), (9.5, 10), (10.5, 16)], r=S.r)),
            line(poly([(22, 8), (18.5, 8), (17, 12.5), (15, 12.5), (13.5, 16)], r=S.r)),
            line("M3 20.5C5 19.2 7 19.2 9 20.5C11 21.8 13 21.8 15 20.5C17 19.2 19 19.2 21 20.5")]


@icon("snowman", CAT, "Snowman with stick arms", tags=["winter", "snow", "christmas", "frosty", "cold", "holiday"])
def _(S):
    body = union(circle(12, 7, 3.5), circle(12, 15.5, 5.5))
    return [shell(body), dot(10.8, 6.5, 0.9), dot(13.2, 6.5, 0.9), dot(12, 14, 1), dot(12, 17.5, 1),
            line(seg(6.5, 13.5, 3, 11)), line(seg(17.5, 13.5, 21, 11))]


@icon("stone", CAT, "A faceted rock", tags=["rock", "boulder", "pebble", "mineral", "geology", "ore"],
      aliases=["rock"])
def _(S):
    outline = [(3, 16), (5.5, 9.5), (10.5, 6), (16.5, 6.5), (20.5, 11), (21, 16.5), (17, 19.5), (7, 19.5)]
    return [shell(poly(outline, closed=True, r=S.r)), detail(poly([(10.5, 6), (12.5, 11.5), (20.5, 11)], r=S.r)), detail(seg(12.5, 11.5, 10, 19.5))]


@icon("crystal", CAT, "Cluster of quartz crystals", tags=["quartz", "gem", "mineral", "geology", "healing", "amethyst"])
def _(S):
    mid = poly([(9.5, 21), (9.5, 7.5), (12, 3.5), (14.5, 7.5), (14.5, 21)], closed=True, r=L(S, 0, 1))
    side = [(3.5, 21), (3.5, 13.5), (5.5, 10.5), (7.5, 13.5), (7.5, 21)]
    left = rot(poly(side, closed=True, r=L(S, 0, 1)), -18, 5.5, 21)
    right = rot(poly([(24 - x, y) for x, y in side], closed=True, r=L(S, 0, 1)), 18, 18.5, 21)
    return [shell(mid), shell(left), shell(right), detail(seg(12, 8, 12, 17))]


# ============================================================================ plants

def leaf_shape(x1, y1, x2, y2, bulge):
    """Pointed leaf from (x1, y1) to (x2, y2), each half bowing out by about bulge px."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    b = bulge * 2
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx * b)} {fmt(my + ny * b)} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(mx - nx * b)} {fmt(my - ny * b)} {fmt(x1)} {fmt(y1)}Z")


@icon("leaf", CAT, "Leaf with a midrib and veins", tags=["nature", "plant", "foliage", "green", "botany", "spring"])
def _(S):
    tip = L(S, "M12 2.5", "M11.2 3.1Q12 2.5 12.8 3.1")
    d = (tip + "C16.5 6 18.5 9.5 18 13.5C17.5 17 15 19 12 19C9 19 6.5 17 6 13.5C5.5 9.5 7.5 6 "
         + L(S, "12 2.5Z", "11.2 3.1Z"))
    return [shell(d, stroke_miterlimit="8"), detail(seg(12, 7, 12, 19)),
            detail(poly([(9, 10), (12, 12.5), (15, 10)], r=S.r * 0.6)), detail(poly([(8.5, 14), (12, 16.5), (15.5, 14)], r=S.r * 0.6)),
            line(seg(12, 19, 12, 21.5))]


@icon("tree", CAT, "Broadleaf tree with a round crown", tags=["nature", "park", "oak", "garden", "forest", "plant"])
def _(S):
    return [shell(ellipse(12, 9.5, 7.5, 7)), detail(poly([(8.8, 9.5), (12, 12.7), (15.2, 9.5)], r=S.r)), detail(seg(12, 12.7, 12, 16.5)),
            line(seg(12, 16.5, 12, 21.5))]


def _pine_pts(cx, top, w, h, tiers=3):
    """Tiered conifer outline: tiers step out towards the base; w = base width, h = height."""
    pts_r = []
    for k in range(tiers):
        y = top + h * (k + 1) / tiers
        half = w / 2 * (k + 1) / tiers
        inner = half - w * 0.18 if k < tiers - 1 else None
        pts_r.append((cx + half, y))
        if inner is not None:
            pts_r.append((cx + inner, y))
    right = [(cx, top)] + pts_r
    left = [(2 * cx - x, y) for x, y in reversed(pts_r)]
    return right + left


@icon("pine-tree", CAT, "Evergreen pine tree with three tiers", tags=["conifer", "evergreen", "fir", "spruce", "forest", "nature"],
      aliases=["conifer", "evergreen"])
def _(S):
    return [shell(poly(_pine_pts(12, 2.5, 16, 16), closed=True, r=S.r * 0.5)), line(seg(12, 18.5, 12, 21.5))]


_FOREST_FRONT = _pine_pts(8, 3, 11, 15, 3)
_FOREST_BACK = _pine_pts(17.5, 7, 8, 10.5, 2)


def _forest_filled():
    front = U(region(poly(_FOREST_FRONT, closed=True)), ST(seg(8, 18, 8, 21.5), 2.5))
    back = U(region(poly(_FOREST_BACK, closed=True)), ST(seg(17.5, 17.5, 17.5, 21.5), 2.5))
    return U(D(back, grow(front, 1.75)), front)


@icon("forest", CAT, "Two pine trees, one behind the other", tags=["woods", "woodland", "trees", "nature", "park", "wilderness"],
      aliases=["woods"], filled=_forest_filled)
def _(S):
    front = poly(_FOREST_FRONT, closed=True, r=S.r * 0.5)
    back = poly(_FOREST_BACK, closed=True, r=S.r * 0.5)
    return [cut_strokes(S, [back], region(poly(_FOREST_FRONT, closed=True))), shell(front),
            line(seg(8, 18, 8, 21.5)), line(seg(17.5, 17.5, 17.5, 21.5))]


@icon("flower", CAT, "Five-petalled flower on a stem with a leaf", tags=["blossom", "bloom", "garden", "spring", "plant", "daisy"],
      aliases=["blossom"])
def _(S):
    cx, cy = 12, 8.5
    petals = [circle(*polar(cx, cy, 3.6, -90 + k * 72), 2.6) for k in range(5)]
    head = union(*petals, circle(cx, cy, 3))
    return [shell(head), detail(circle(cx, cy, 1.6)), line(seg(12, 14.5, 12, 21.5)),
            shell(leaf_shape(12, 19, 17.5, 15.5, 1.3))]


def _spiral(cx, cy, r0, r1, a0, turns, n=40):
    pts = []
    for i in range(n + 1):
        t = i / n
        a = a0 + 360 * turns * t
        pts.append(polar(cx, cy, r0 + (r1 - r0) * t, a))
    d = "M" + " ".join(f"{fmt(x)} {fmt(y)}" for x, y in pts[:1])
    return d + "".join(f"L{fmt(x)} {fmt(y)}" for x, y in pts[1:])


_ROSE_BOWL = "M5.5 6.5C5.5 11.5 8.3 14.5 12 14.5C15.7 14.5 18.5 11.5 18.5 6.5C16.2 6.5 13.8 7.5 12 9.5C10.2 7.5 7.8 6.5 5.5 6.5Z"
_ROSE_BUD = "M12 9C9.8 9 8.5 7.2 8.5 5.5C8.5 3.8 10 2.5 12 2.5C14 2.5 15.5 3.8 15.5 5.5C15.5 7.2 14.2 9 12 9Z"


def _rose_filled():
    bowl = region(_ROSE_BOWL)
    return U(D(region(_ROSE_BUD), grow(bowl, 1.5)), bowl, ST(seg(12, 14.5, 12, 21.5), 2.5), region(leaf_shape(12, 19, 6.5, 16, 1.3)))


@icon("rose", CAT, "Rose bud cupped by two petals on a stem", tags=["flower", "love", "romance", "valentine", "garden", "bloom"],
      filled=_rose_filled)
def _(S):
    return [cut_strokes(S, [_ROSE_BUD, "M12 5.5C11 5.5 10.5 4.5 11.2 3.8"], region(_ROSE_BOWL)), shell(_ROSE_BOWL),
            line(seg(12, 14.5, 12, 21.5)), shell(leaf_shape(12, 19, 6.5, 16, 1.3))]


@icon("tulip", CAT, "Tulip flower with a long leaf", tags=["flower", "spring", "bloom", "garden", "holland", "bulb"])
def _(S):
    top = poly([(7, 4), (9.5, 7), (12, 3), (14.5, 7), (17, 4)], r=L(S, 0, 1.2))
    d = top + "L17 9.5C17 12.5 14.8 14 12 14C9.2 14 7 12.5 7 9.5Z"
    return [shell(d if S.name == "rounded" else d, stroke_miterlimit="8"), line(seg(12, 14, 12, 21.5)),
            shell("M12 21C8.5 20.5 6 18 5.5 14.5C9 15.2 11.2 17.5 12 21Z")]


@icon("sunflower", CAT, "Sunflower head with pointed petals on a stem", tags=["flower", "summer", "sun", "garden", "bloom", "seeds"])
def _(S):
    cx, cy = 12, 9
    pts = [polar(cx, cy, 7 if k % 2 == 0 else 5.1, -90 + k * 18) for k in range(20)]
    return [shell(poly(pts, closed=True, r=S.r * 0.3)), detail(circle(cx, cy, 2.2)), line(seg(12, 16, 12, 21.5)),
            shell(leaf_shape(12, 19.5, 17, 16.5, 1.2))]


def _cactus(S):
    trunk = P("M9.5 21.5V5.5A2.5 2.5 0 0 1 14.5 5.5V21.5Z")
    arm_l = ST(poly([(10, 14.25), (6.25, 14.25), (6.25, 8.5)]), 3.5, "round", S.join)
    arm_r = ST(poly([(14, 11.75), (17.75, 11.75), (17.75, 6.5)]), 3.5, "round", S.join)
    return path_to_d(U(trunk, arm_l, arm_r))


@icon("cactus", CAT, "Saguaro cactus with two arms", tags=["desert", "succulent", "plant", "western", "dry", "arid"])
def _(S):
    return [shell(_cactus(S)), detail(seg(12, 7.5, 12, 18.5))]


@icon("seedling", CAT, "Young seedling with two leaves growing from the soil", tags=["plant", "growth", "sapling", "grow", "garden", "spring"],
      aliases=["sprout", "plant-sprout"])
def _(S):
    return [line(seg(12, 20.5, 12, 11)), shell(leaf_shape(12, 12.5, 4.5, 8, 1.5)), shell(leaf_shape(12, 10.5, 19.5, 5.5, 1.6)),
            line(seg(4, 20.5, 20, 20.5))]


def _heart(tipx, tipy, length, deg):
    """Clover leaflet: a heart whose point sits at (tipx, tipy), lobes pointing along deg."""
    r = length * 0.34
    base = f"M0 0L{fmt(-r * 1.45)} {fmt(-length + r * 1.1)}A{fmt(r)} {fmt(r)} 0 0 1 0 {fmt(-length + r * 0.35)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(r * 1.45)} {fmt(-length + r * 1.1)}Z"
    p = transform_path(P(base), rotation(deg + 90, 0, 0))
    return path_to_d(transform_path(p, (1, 0, 0, 1, tipx, tipy)))


_CLOVER_C = (12, 10)


def _leaflets():
    cx, cy = _CLOVER_C
    return [_heart(*polar(cx, cy, 2.3, a), 6.5, a) for a in (-135, -45, 45, 135)]


@icon("clover", CAT, "Four-leaf clover", tags=["luck", "lucky", "shamrock", "irish", "st patrick", "fortune"],
      aliases=["four-leaf-clover"])
def _(S):
    return [*[shell(d, stroke_miterlimit="2" if S.name == "line" else "4") for d in _leaflets()],
            line("M12 12.5C12.5 15.5 13.5 18.5 15.5 21.5")]


def _feather(S):
    """Feather vane with a notch on each side, drawn along a local axis (u along the shaft, v across) then laid at 45°."""
    right = [(5, 1.2), (6.5, 2.6), (8.5, 3.2), (11, 3.2), (11.6, 1.2), (13.2, 3.1), (15.5, 2.8), (18, 2), (20, 1), (21.5, 0)]
    left = [(20, -1.3), (18, -2.6), (15.5, -3.3), (13, -3.4), (10.5, -3.2), (8.5, -2.8), (6.5, -2.2), (5, -1.2)]
    ang = -45

    def m(u, v):
        a = math.radians(ang)
        return (3 + u * math.cos(a) - v * math.sin(a), 21 + u * math.sin(a) + v * math.cos(a))
    return [m(u, v) for u, v in right + left], m


@icon("feather", CAT, "Bird feather with a notched vane", tags=["bird", "plume", "light", "soft", "nature", "down"],
      aliases=["plume"])
def _(S):
    pts, m = _feather(S)
    return [shell(poly(pts, closed=True, r=S.r * 0.5)), detail(seg(*m(5, 0), *m(17.5, 0))), line(seg(*m(0, 0), *m(5, 0)))]


@icon("seashell", CAT, "Scallop seashell with radiating ribs", tags=["shell", "scallop", "beach", "ocean", "sea", "clam"],
      aliases=["scallop"])
def _(S):
    top = "M3.5 11.5A3 3 0 0 1 6 6.5A3.4 3.4 0 0 1 10 3.8A3.4 3.4 0 0 1 14 3.8A3.4 3.4 0 0 1 18 6.5A3 3 0 0 1 20.5 11.5"
    body = [(20.5, 11.5), (14, 17.5), (17, 18), (17, 20.5), (7, 20.5), (7, 18), (10, 17.5), (3.5, 11.5)]
    d = top + poly(body, r=S.r * 0.6)[len("M20.5 11.5"):] + "Z"
    return [shell(d), detail(seg(12, 17.5, 12, 7)), detail(seg(10.4, 17.5, 7.5, 9.5)), detail(seg(13.6, 17.5, 16.5, 9.5))]


@icon("coral", CAT, "Branching coral", tags=["reef", "ocean", "sea", "marine", "underwater", "aquarium"])
def _(S):
    return [line(seg(12, 21.5, 12, 12)),
            line(poly([(12, 16.5), (7, 12), (7, 5)], r=S.r)), line(poly([(7, 9.5), (3.5, 7), (3.5, 4)], r=S.r)),
            line(poly([(12, 12), (16.5, 8.5), (16.5, 3)], r=S.r)), line(poly([(16.5, 11.5), (20.5, 9.5), (20.5, 6.5)], r=S.r)),
            line(seg(12, 12, 12, 7))]


@icon("bamboo", CAT, "Bamboo stalks with nodes and leaves", tags=["plant", "panda", "asia", "zen", "grass", "garden"])
def _(S):
    k = L(S, 1, 2)
    return [shell(rect(4.5, 2.5, 4.5, 19, k)), detail(seg(4.5, 8.5, 9, 8.5)), detail(seg(4.5, 15, 9, 15)),
            shell(rect(12, 6.5, 4.5, 15, k)), detail(seg(12, 13.5, 16.5, 13.5)),
            shell(leaf_shape(16.5, 10.5, 21.5, 5, 1.3)), shell(leaf_shape(16.5, 17, 21.5, 15, 0.9))]


def _maple():
    right = [(13.4, 6.3), (15.4, 5.2), (15, 9.6), (18.4, 7.6), (20.8, 8.4), (19.4, 10.8), (21.2, 12.4),
             (17.2, 14.2), (17.8, 16), (13.8, 15.6), (12.8, 17)]
    left = [(24 - x, y) for x, y in reversed(right)]
    return [(12 + (x - 12) * 0.92, 11 + (y - 11) * 0.92) for x, y in [(12, 2.5)] + right + left]


@icon("maple-leaf", CAT, "Maple leaf", tags=["autumn", "fall", "canada", "leaf", "tree", "nature"])
def _(S):
    return [shell(poly(_maple(), closed=True, r=S.r * 0.4)), line(seg(12, 16.5, 12, 21.5)), detail(seg(12, 8, 12, 14.5))]


@icon("acorn", CAT, "Acorn with its cap", tags=["oak", "nut", "autumn", "fall", "seed", "squirrel"])
def _(S):
    cap = L(S, "M4.5 9.5C4.5 6 8 4 12 4C16 4 19.5 6 19.5 9.5Z", "M6 9.5A1.5 1.5 0 0 1 4.5 8C4.5 5.8 8 4 12 4C16 4 19.5 5.8 19.5 8A1.5 1.5 0 0 1 18 9.5Z")
    nut = "M6.5 13.5H17.5C17.5 17.5 15.2 20 12 21C8.8 20 6.5 17.5 6.5 13.5Z"
    return [shell(cap), shell(nut), line(seg(12, 4, 13.5, 1.8))]


def clip_seg(shape_d, p0, p1):
    """Part of the segment p0-p1 that lies inside the closed shape (for texture lines that end on an outline)."""
    (x0, y0), (x1, y1) = p0, p1
    ln = math.hypot(x1 - x0, y1 - y0)
    nx, ny = -(y1 - y0) / ln * 0.005, (x1 - x0) / ln * 0.005
    sliver = P(poly([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)], closed=True))
    bx0, by0, bx1, by1 = [v / 100 for v in I(sliver, P(shape_d)).bounds]
    if (x1 - x0) * (y1 - y0) >= 0:
        return seg(bx0, by0, bx1, by1)
    return seg(bx0, by1, bx1, by0)


_CONE = "M12 4.5C16 4.5 18.5 7.6 18.5 11.2C18.5 15.6 15.5 19.4 12 21C8.5 19.4 5.5 15.6 5.5 11.2C5.5 7.6 8 4.5 12 4.5Z"


@icon("pinecone", CAT, "Pine cone with a lattice of scales", tags=["pine", "cone", "autumn", "forest", "seed", "conifer"],
      aliases=["pine-cone"])
def _(S):
    lattice = [clip_seg(_CONE, (12 + c - 12, 12 - c - 12), (12 + c + 12, 12 - c + 12)) for c in (-4, 0, 4)]
    lattice += [clip_seg(_CONE, (12 + c - 12, 12 + c + 12), (12 + c + 12, 12 + c - 12)) for c in (-4, 0, 4)]
    return [shell(_CONE), *[detail(d) for d in lattice], line(seg(12, 4.5, 12, 2))]
