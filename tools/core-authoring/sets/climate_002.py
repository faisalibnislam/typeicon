"""TypeIcon Core: climate (batch climate_002).

Weather conditions, climate science concepts and field instruments. The cloud, crescent moon and
thermometer reuse the proportions of the library's own weather icons (icons.py and sets/nature.py) so the
set reads as one family. Things seen behind another object (a sun behind a cloud) are cut with a 2 px gap:
the stroke styles emit the cut outline as a solid region and Filled is designed explicitly.
"""
import math
import re

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, LINE, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "climate"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


_NUM = re.compile(r"[A-Za-z]|-?\d*\.?\d+(?:e-?\d+)?")


def _tx(d, s=1.0, dx=0.0, dy=0.0, cx=12.0, cy=12.0, mirror=False):
    """Uniformly scale a d-string about (cx, cy), optionally mirror it horizontally, then translate."""
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
            rx, ry, rot_, la, sw, x, y = toks[i:i + 7]
            if mirror:
                sw = "1" if sw == "0" else "0"
            out.append(f"{fmt(float(rx) * s)} {fmt(float(ry) * s)} {rot_} {la} {sw} {X(x)} {Y(y)}")
            i += 7
        else:
            raise ValueError(f"unsupported command {cmd}")
    return "".join(out)


# The library cloud: Line has a flat base meeting the lobes at corners, Rounded flows.
_CLOUD_LINE = "M4.5 19H19.5A3.8 3.8 0 0 0 18 11.7A6 6 0 0 0 6.5 10A4.7 4.7 0 0 0 4.5 19Z"
_CLOUD_ROUND = "M7 19H17.5A4.5 4.5 0 0 0 18 10.03A6 6 0 0 0 6.34 9.1A5 5 0 0 0 7 19Z"
_CL_X0, _CL_W = 1.69, 20.13  # Line cloud left edge and width (base at y 19)


def cloud(S, s, x0, base, mirror=False):
    """The library cloud scaled by s with its left edge at x0 and its flat base at y = base."""
    d = _CLOUD_LINE if S.name == "line" else _CLOUD_ROUND
    if mirror:
        return _tx(d, s, 24 - x0 - (_CL_X0 + _CL_W) * s, base - 19 * s, cx=0, cy=0, mirror=True)
    return _tx(d, s, x0 - _CL_X0 * s, base - 19 * s, cx=0, cy=0)


_MOON = "M20.5 14.5A8.5 8.5 0 1 1 9.5 3.5A7 7 0 0 0 20.5 14.5Z"  # bounds x 4.08-20.5, y 3.5-19.92


def moon(s, x0, y0):
    """The library crescent scaled by s with its top-left bounds at (x0, y0)."""
    return _tx(_MOON, s, x0 - 4.08 * s, y0 - 3.5 * s, cx=0, cy=0)


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


def sun_rays(cx, cy, r0, r1, n=8, start=0.0, only=None):
    out = []
    for k in range(n):
        if only is not None and k not in only:
            continue
        a = start + k * 360 / n
        out.append(seg(*polar(cx, cy, r0, a), *polar(cx, cy, r1, a)))
    return out


def slant(x, y0, y1, k=0.35):
    """A falling streak from (x, y0) to y1, leaning left as it falls."""
    return seg(x + (y1 - y0) * k / 2, y0, x - (y1 - y0) * k / 2, y1)


def asterisk(cx, cy, r):
    return [seg(*polar(cx, cy, r, a), *polar(cx, cy, r, a + 180)) for a in (-90, -30, 30)]


def thermo(S, x, top, bulb_y, level, w=4.0, br=3.5):
    """Thermometer: tube of width w from top to the bulb (centre bulb_y, radius br), column from level."""
    h = w / 2
    yj = bulb_y - math.sqrt(br * br - h * h)
    if S.name == "line":
        d = f"M{fmt(x - h)} {fmt(yj)}V{fmt(top)}H{fmt(x + h)}V{fmt(yj)}A{fmt(br)} {fmt(br)} 0 1 1 {fmt(x - h)} {fmt(yj)}Z"
    else:
        d = (f"M{fmt(x - h)} {fmt(yj)}V{fmt(top + h)}A{fmt(h)} {fmt(h)} 0 0 1 {fmt(x + h)} {fmt(top + h)}"
             f"V{fmt(yj)}A{fmt(br)} {fmt(br)} 0 1 1 {fmt(x - h)} {fmt(yj)}Z")
    parts = [shell(d)]
    if level is not None:
        parts.append(detail(seg(x, level, x, bulb_y - 1)))
    parts.append(dot(x, bulb_y, br / 2))
    return parts


def arrow_head(x, y, deg, size=2.5):
    """Open chevron arrowhead with its tip at (x, y) pointing along deg."""
    a = polar(x, y, size * math.sqrt(2), deg + 135)
    b = polar(x, y, size * math.sqrt(2), deg - 135)
    return [a, (x, y), b]


def arrow(x1, y1, x2, y2, S, size=2.5):
    """Straight arrow from (x1, y1) to a tip at (x2, y2): shaft plus open head."""
    deg = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return [line(seg(x1, y1, x2, y2)), line(poly(arrow_head(x2, y2, deg, size), r=S.r * 0.5))]


def darrow_v(x, y1, y2, S, size=2.25):
    """Vertical double-headed arrow between y1 (top tip) and y2 (bottom tip)."""
    return [line(seg(x, y1, x, y2)), line(poly(arrow_head(x, y1, -90, size), r=S.r * 0.5)),
            line(poly(arrow_head(x, y2, 90, size), r=S.r * 0.5))]


def calendar(S, x, y, w, h):
    """Calendar page with a header rule and two binder rings."""
    return [shell(rect(x, y, w, h, min(S.R, 2.5))), detail(seg(x, y + 4.5, x + w, y + 4.5)),
            line(seg(x + 3.5, y - 2, x + 3.5, y + 1.5)), line(seg(x + w - 3.5, y - 2, x + w - 3.5, y + 1.5))]


# ============================================================================ sky, cloud and moon conditions

# Sky composites: a sun or moon at the top-left behind a cloud, precipitation below.
_SKY = dict(s=0.7, x0=7.25, base=14.5)


def _sky_cloud(S):
    return cloud(S, **_SKY)


def _sun_back():
    c = (7.5, 7.5)
    rays = sun_rays(*c, 5, 6.25, only=(3, 4, 5, 6, 7))
    return [circle(*c, 3)] + rays, U(P(circle(*c, 4.25)), *[ST(d, 2.5) for d in sun_rays(*c, 5.25, 6.5, only=(3, 4, 5, 6, 7))])


def _moon_back():
    d = moon(0.5, 2.5, 2.5)
    return [d], region(d)


def sky_icon(name, desc, back, precip, tags, aliases=()):
    """Register a sky composite: back() -> (stroke ds, filled region); precip(S) -> parts under the cloud."""
    def f():
        from dsl import filled_region
        _, reg = back()
        cl = _sky_cloud(LINE)
        return U(D(reg, grow(region(cl), 1.75)), filled_region([shell(cl), *precip(LINE)]))

    @icon(name, CAT, desc, tags=tags, aliases=list(aliases), filled=f)
    def _(S):
        ds, _ = back()
        c = _sky_cloud(S)
        return [cut_strokes(S, ds, region(c)), shell(c), *precip(S)]
    return _


def _hail(S):
    return [dot(10, 18.5, 1.6), dot(14.5, 20.5, 1.6), dot(19, 18.5, 1.6)]


def _sleet(S):
    return [line(slant(11, 17, 21)), *[line(d) for d in asterisk(17, 19, 2.6)]]


sky_icon("sun-hail", "Sun behind a cloud with hailstones falling", _sun_back, _hail,
         ["hail", "hail showers", "sunny intervals", "weather", "forecast", "hailstones"])
sky_icon("moon-hail", "Crescent moon behind a cloud with hailstones falling", _moon_back, _hail,
         ["hail", "night hail", "hail showers", "weather", "forecast", "night"])
sky_icon("sun-sleet", "Sun behind a cloud with a raindrop and a snowflake falling", _sun_back, _sleet,
         ["sleet", "wintry showers", "rain and snow", "weather", "forecast", "sunny intervals"])
sky_icon("moon-sleet", "Crescent moon behind a cloud with a raindrop and a snowflake falling", _moon_back, _sleet,
         ["sleet", "night sleet", "rain and snow", "weather", "forecast", "night"])

_BOLT_ISO = [(15.5, 15.5), (13, 18.5), (16.5, 18.5), (14, 21.5)]


def _iso_bolt(S):
    return [line(poly(_BOLT_ISO, r=S.r * 0.6), stroke_miterlimit="8")]


sky_icon("isolated-thunderstorm", "Sun behind a cloud with a single lightning bolt below", _sun_back, _iso_bolt,
         ["isolated thunderstorm", "scattered storms", "thunder", "lightning", "weather", "forecast"])


@icon("severe-thunderstorm", CAT, "Heavy storm cloud with a lightning bolt and hailstones",
      tags=["severe storm", "thunderstorm", "hail", "lightning", "warning", "weather"])
def _(S):
    c = cloud(S, 0.78, 2.3, 13.5)
    bolt = [(13.5, 11), (10, 16), (14, 16), (11.5, 21)]
    return [cut_strokes(S, [c], ST(poly(bolt), 2)), line(poly(bolt, r=S.r * 0.6), stroke_miterlimit="8"),
            dot(6, 18.5, 1.6), dot(18, 18.5, 1.6)]


@icon("hazy-sun", CAT, "Sun with haze lines drawn across its lower half",
      tags=["haze", "hazy", "hazy sunshine", "weather", "forecast", "dust"])
def _(S):
    c = (12, 10)
    body = [circle(*c, 5)] + sun_rays(*c, 7.25, 9, only=(4, 5, 6, 7, 0))
    bands = [seg(2.5, 13, 21.5, 13), seg(4.5, 17, 13, 17), seg(16, 17, 19.5, 17), seg(8, 21, 16, 21)]
    return [cut_strokes(S, body, U(*[ST(d, 2) for d in bands]), gap=1.25), *[line(d) for d in bands]]


@icon("moon-fog", CAT, "Crescent moon above bands of fog", tags=["night fog", "mist", "fog", "night", "weather", "forecast"])
def _(S):
    return [shell(moon(0.52, 6.5, 2)), line(seg(3, 15, 21, 15)), line(seg(3, 19, 12, 19)), line(seg(15, 19, 21, 19))]


@icon("moon-wind", CAT, "Crescent moon with curling gusts of wind below",
      tags=["windy night", "wind", "night", "breeze", "weather", "forecast"])
def _(S):
    return [shell(moon(0.52, 3, 2)),
            line("M3 13H16.5A2.5 2.5 0 1 0 14 10.5"),
            line("M3 17H18.5A2.5 2.5 0 1 1 16 19.5")]


@icon("cloud-ceiling", CAT, "Cloud with a height arrow down to the ground; the cloud base height",
      tags=["ceiling", "cloud base", "cloud height", "aviation", "visibility", "weather"])
def _(S):
    return [shell(cloud(S, 0.5, 7, 8.5)), *darrow_v(12, 11, 18.5, S), line(seg(3, 21, 21, 21))]


@icon("relative-humidity", CAT, "Water drop with a percent sign inside",
      tags=["humidity", "rh", "moisture", "percent", "dew", "weather"])
def _(S):
    d = L(S, "M12 2.5C12 2.5 19 9.5 19 14.5A7 7 0 0 1 5 14.5C5 9.5 12 2.5 12 2.5Z",
          "M11.3 3.3Q12 2.5 12.7 3.3C14.5 5.3 19 10.5 19 14.5A7 7 0 0 1 5 14.5C5 10.5 9.5 5.3 11.3 3.3Z")
    return [shell(d, stroke_miterlimit="8"), detail(seg(14.5, 11.5, 9.5, 18.5)), dot(9.5, 12.25, 1.3), dot(14.5, 17.75, 1.3)]


@icon("tropical-night", CAT, "Crescent moon beside a thermometer reading high; a warm night",
      tags=["warm night", "hot night", "night temperature", "heat", "summer", "weather"])
def _(S):
    return [shell(moon(0.58, 2.5, 3)), *thermo(S, 17, 3, 17.5, 6)]


@icon("degree-days", CAT, "Thermometer beside a calendar page; heating and cooling degree days",
      tags=["degree days", "heating degree days", "cooling degree days", "temperature", "calendar", "energy"])
def _(S):
    return [*thermo(S, 6, 3, 17.5, 9), *calendar(S, 11.5, 5.5, 10, 15.5), *[dot(x, y, 1) for x in (14.5, 18.5) for y in (14.5, 18)]]


@icon("outdoor-temperature", CAT, "Thermometer standing outside beside a house",
      tags=["outside temperature", "outdoor", "temperature", "weather", "home", "thermometer"])
def _(S):
    house = poly([(2.5, 12), (8.5, 6.5), (14.5, 12), (14.5, 21), (2.5, 21)], closed=True, r=S.r)
    return [shell(house), detail(rect(6.5, 15, 4, 6, min(S.R, 1))), *thermo(S, 19.5, 3, 17.5, 9, w=3.5, br=3)]


@icon("cloud-in-a-jar", CAT, "Glass jar with a lid and a small cloud inside; a classroom experiment",
      tags=["cloud in a jar", "science experiment", "jar", "cloud", "classroom", "condensation"])
def _(S):
    return [shell(rect(7, 2.5, 10, 3, min(S.R, 1))), shell(rect(5, 7.5, 14, 14, min(S.R, 3))),
            detail(cloud(S, 0.42, 7.75, 17))]


@icon("cut-off-low", CAT, "Wavy jet stream with a closed low pressure circle cut off below it",
      tags=["cut off low", "upper low", "low pressure", "jet stream", "meteorology", "weather map"])
def _(S):
    return [line("M2 6C5 2.5 8 2.5 12 6S19 9.5 22 6"), shell(circle(12, 16, 5.5)),
            detail(poly([(10.5, 13), (10.5, 19), (14.5, 19)], r=S.r * 0.5))]


@icon("albedo", CAT, "Sunlight striking an ice sheet and reflecting back up",
      tags=["albedo", "reflection", "reflectivity", "ice", "sunlight", "climate"])
def _(S):
    return [shell(circle(5, 5, 2.5)), shell(rect(2.5, 17.5, 19, 3.5, min(S.R, 1.5))),
            line(poly([(7.5, 8.5), (11.5, 14.5), (15.5, 8.5)], r=S.r)), *arrow(15.5, 8.5, 19, 3.25, S, 2.25)]


@icon("climate-tipping-point", CAT, "Ball balanced on the crest of a hill beside a thermometer",
      tags=["tipping point", "threshold", "climate change", "instability", "risk", "global warming"])
def _(S):
    return [line("M2 20.5C6 20.5 7 13.5 11 13.5C15 13.5 16 20.5 20 20.5"), shell(circle(11, 9.5, 2.75)),
            *thermo(S, 19, 2.5, 11, None, w=3, br=2.5)]


def leaf(x0, y0, x1, y1, bulge):
    """Leaf outline from base (x0, y0) to tip (x1, y1); bulge is the half width (sign picks the side first)."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln * bulge * 2, dx / ln * bulge * 2
    return (f"M{fmt(x0)} {fmt(y0)}Q{fmt(mx + nx)} {fmt(my + ny)} {fmt(x1)} {fmt(y1)}"
            f"Q{fmt(mx - nx)} {fmt(my - ny)} {fmt(x0)} {fmt(y0)}Z")


def wavy_up(x, y0, y1, amp=1.25):
    """Wavy vertical line rising from y0 to y1 (y1 < y0) with an arrowhead at the top."""
    n = 2
    h = (y0 - y1 - 1.5) / n
    d = f"M{fmt(x)} {fmt(y0)}"
    for k in range(n):
        ya = y0 - k * h
        d += f"C{fmt(x - amp * 1.4)} {fmt(ya - h / 3)} {fmt(x + amp * 1.4)} {fmt(ya - 2 * h / 3)} {fmt(x)} {fmt(ya - h)}"
    d += f"L{fmt(x)} {fmt(y1)}"
    return d


# ============================================================================ climate science and land

@icon("solar-radiation", CAT, "Sun in the corner with parallel rays striking the ground",
      tags=["solar radiation", "insolation", "sunlight", "irradiance", "uv", "climate"])
def _(S):
    parts = [shell(circle(5.5, 5.5, 3)), line(seg(2, 21, 22, 21))]
    for (x1, y1), (x2, y2) in (((4, 13.5), (8, 17.5)), ((8.5, 11.5), (14, 17)), ((13, 9.5), (20, 16.5))):
        parts += arrow(x1, y1, x2, y2, S, 2.25)
    return parts


@icon("freezing-level", CAT, "Mountain with a dashed freezing line across it and a snowflake above",
      tags=["freezing level", "snow line", "zero degree line", "altitude", "mountain", "forecast"])
def _(S):
    mtn = poly([(2, 21), (9.5, 5.5), (17, 21)], closed=True, r=S.r)
    return [shell(mtn), detail(seg(7.5, 14, 11.5, 14)), line(seg(2, 14, 3.5, 14)), line(seg(15.5, 14, 17.5, 14)),
            line(seg(19.5, 14, 22, 14)), *[line(d) for d in asterisk(18.5, 5.5, 3)]]


@icon("temperature-inversion", CAT, "Valley with smoke trapped and spreading under a flat warm lid",
      tags=["inversion", "temperature inversion", "smog", "air pollution", "valley", "weather"])
def _(S):
    return [line(seg(2, 4.5, 22, 4.5)), line(poly([(2, 12), (7, 20.5), (17, 20.5), (22, 12)], r=S.r)),
            shell(rect(10.5, 14, 3, 6.5, min(S.R, 0.75))),
            line("M12 11.5C12 9 10 8.5 4 8.5"), line("M12 11.5C12 9 14 8.5 20 8.5")]


@icon("growing-season", CAT, "Calendar page with a seedling sprouting inside",
      tags=["growing season", "planting season", "frost free", "garden", "calendar", "agriculture"])
def _(S):
    return [*calendar(S, 3, 5, 18, 16), detail(seg(12, 19, 12, 14)),
            detail(leaf(12, 15.5, 7.5, 13, -1)), detail(leaf(12, 14.5, 16.5, 12.5, 1))]


@icon("plant-hardiness-zone", CAT, "Potted plant beside a map divided into climate bands",
      tags=["hardiness zone", "plant zone", "growing zone", "gardening", "map", "climate zone"])
def _(S):
    pot = poly([(2.5, 15.5), (10, 15.5), (9, 21), (3.5, 21)], closed=True, r=S.r * 0.5)
    return [shell(rect(10.5, 3, 11, 10, min(S.R, 2))), detail("M10.5 6.5C13 5.5 15 7.5 17 6.5S20 5.5 21.5 6.5"),
            detail("M10.5 9.75C13 8.75 15 10.75 17 9.75S20 8.75 21.5 9.75"),
            shell(pot), line(seg(6.25, 13.5, 6.25, 10)), shell(leaf(6.25, 10.5, 3, 6.5, -0.9))]


@icon("soil-moisture", CAT, "Soil block with a water drop inside under a gauge needle",
      tags=["soil moisture", "soil water", "irrigation", "drought", "agriculture", "sensor"])
def _(S):
    drop = "M12 14C12 14 14.5 16.5 14.5 18A2.5 2.5 0 0 1 9.5 18C9.5 16.5 12 14 12 14Z"
    return [shell(rect(2.5, 11.5, 19, 9.5, min(S.R, 2))), Part("dot", drop),
            line(arc(12, 8.5, 5.5, 200, 340)), line(seg(12, 8.5, 15, 4.5)), dot(12, 8.5, 1.4)]


@icon("evapotranspiration", CAT, "Plant with wavy vapour rising from its leaves and the soil",
      tags=["evapotranspiration", "transpiration", "evaporation", "water cycle", "plant", "vapor"])
def _(S):
    return [line(seg(2, 21, 22, 21)), line(seg(12, 21, 12, 13.5)), shell(leaf(12, 16.5, 7, 13, -1.1)),
            shell(leaf(12, 15, 17, 11.5, 1.1)),
            line(wavy_up(4.5, 18.5, 5)), line(poly(arrow_head(4.5, 5, -90, 2), r=S.r * 0.5)),
            line(wavy_up(19.5, 18.5, 5)), line(poly(arrow_head(19.5, 5, -90, 2), r=S.r * 0.5))]


@icon("surface-runoff", CAT, "Rain falling on a slope with water running down into a stream",
      tags=["runoff", "surface runoff", "stormwater", "flooding", "drainage", "hydrology"])
def _(S):
    ground = poly([(2, 13), (15, 19), (22, 19), (22, 21), (2, 21)], closed=True, r=S.r * 0.5)
    return [*[line(slant(x, 2.5, 6.5)) for x in (5, 9.5, 14)], shell(ground), *arrow(7, 10, 15.5, 14, S, 2.25)]


@icon("wind-erosion", CAT, "Plowed field with soil blowing off it on the wind",
      tags=["wind erosion", "dust", "soil loss", "dust bowl", "drought", "farming"])
def _(S):
    field = poly([(2, 21), (4, 16), (15, 16), (17, 21)], closed=True, r=S.r * 0.5)
    return [shell(field), detail(seg(7, 17, 6, 20)), detail(seg(11, 17, 11.5, 20)),
            line("M2 12H13C16 12 17.5 10.5 17.5 8.5S16 5.5 14 6"), dot(20.5, 11.5, 1.2), dot(18.5, 15, 1.2), dot(21.5, 17, 1.2)]


@icon("wet-bulb-thermometer", CAT, "Thermometer whose bulb is wrapped in a wick dipping into water",
      tags=["wet bulb", "psychrometer", "humidity", "heat stress", "thermometer", "dew point"])
def _(S):
    return [*thermo(S, 12, 2.5, 10.5, 5.5, w=3.5, br=3), line(seg(12, 14.5, 12, 19)),
            line(poly([(5, 14), (5, 21), (19, 21), (19, 14)], r=S.r)), line(seg(7.5, 17, 9.5, 17)), line(seg(14.5, 17, 16.5, 17))]


@icon("evaporation-pan", CAT, "Shallow round pan of water on a low stand with a measuring hook",
      tags=["evaporation pan", "class a pan", "evaporation", "rain gauge", "weather station", "hydrology"])
def _(S):
    pan = "M2.5 8.5A9.5 2.5 0 0 1 21.5 8.5V13A9.5 2.5 0 0 1 2.5 13Z"
    return [shell(pan), detail("M2.5 8.5A9.5 2.5 0 0 0 21.5 8.5"), line(seg(12, 2.5, 12, 7)),
            line(seg(3, 19, 21, 19)), line(seg(5.5, 16.5, 5.5, 21.5)), line(seg(18.5, 16.5, 18.5, 21.5)), line(seg(12, 17, 12, 21.5))]


@icon("dropsonde", CAT, "Small instrument tube hanging below a square parachute",
      tags=["dropsonde", "parachute sensor", "hurricane research", "atmosphere", "sounding", "meteorology"])
def _(S):
    canopy = L(S, "M3 9.5A9 6.5 0 0 1 21 9.5L18 8.5L15 9.5L12 8.5L9 9.5L6 8.5Z", "M3 9.5A9 6.5 0 0 1 21 9.5Q19.5 8 18 8.5Q16.5 9 15 9.5Q13.5 8 12 8.5Q10.5 9 9 9.5Q7.5 8 6 8.5Q4.5 9 3 9.5Z")
    return [shell(canopy), line(seg(4.5, 11, 10, 15.5)), line(seg(19.5, 11, 14, 15.5)),
            shell(rect(10, 15.5, 4, 6, min(S.R, 1.5)))]


@icon("argo-float", CAT, "Slim ocean float bobbing upright in the waves with an antenna on top",
      tags=["argo float", "ocean float", "ocean sensor", "buoy", "oceanography", "profiling float"])
def _(S):
    return [line(seg(12, 6.5, 12, 2)), shell(rect(9.5, 6.5, 5, 15, min(S.R, 2.5))),
            line("M2 12.5C3.5 11 5 11 6.5 12.5"), line("M17.5 12.5C19 11 20.5 11 22 12.5")]


@icon("flux-tower", CAT, "Tall lattice tower rising above the treetops with instruments on an arm",
      tags=["flux tower", "eddy covariance", "carbon flux", "research tower", "forest", "measurement"])
def _(S):
    return [line(seg(10, 21, 10, 5)), line(seg(14, 21, 14, 5)), line(seg(10, 9, 14, 9)), line(seg(10, 14, 14, 14)),
            line(seg(14, 5, 19, 5)), shell(rect(18.5, 6.5, 3, 3, min(S.R, 1))),
            shell(circle(4.75, 14.5, 2.75)), line(seg(4.75, 18.25, 4.75, 21)), shell(circle(19.25, 15.5, 2.75)), line(seg(19.25, 19.25, 19.25, 21))]


@icon("weather-station-display", CAT, "Tabletop weather display showing a sun and a temperature readout",
      tags=["weather station", "home weather station", "display", "forecast", "temperature", "indoor outdoor"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 14, min(S.R, 2.5))), line(poly([(8, 21), (9.5, 17.5)])), line(poly([(16, 21), (14.5, 17.5)])),
            line(seg(6.5, 21, 17.5, 21)),
            detail(circle(8, 9, 1.75)), detail(seg(12.5, 7.5, 18, 7.5)), detail(seg(12.5, 11, 16, 11)), detail(seg(6, 13.75, 10, 13.75))]


def rotd(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def movd(d, dx, dy):
    return path_to_d(transform_path(P(d), (1, 0, 0, 1, dx, dy)))


# ============================================================================ instruments, vessels and people

_PLANE = [(0, -6.5), (1.25, -5), (1.25, -1.5), (6.5, 1.5), (6.5, 3), (1.25, 1.5), (1.25, 4), (3.5, 5.5), (3.5, 6.75),
          (0, 6), (-3.5, 6.75), (-3.5, 5.5), (-1.25, 4), (-1.25, 1.5), (-6.5, 3), (-6.5, 1.5), (-1.25, -1.5), (-1.25, -5)]


@icon("hurricane-hunter-aircraft", CAT, "Propeller aircraft flying toward a hurricane spiral",
      tags=["hurricane hunter", "reconnaissance aircraft", "storm research", "hurricane", "airplane", "meteorology"])
def _(S):
    plane = rotd(poly([(x * 0.85 + 8, y * 0.85 + 15.5) for x, y in _PLANE], closed=True, r=S.r * 0.4), 45, 8, 15.5)
    c = (17, 7)
    return [shell(plane), shell(circle(*c, 2)),
            line(f"M{fmt(c[0])} {fmt(c[1] - 2.25)}C{fmt(c[0] - 3)} {fmt(c[1] - 2.25)} {fmt(c[0] - 4.75)} {fmt(c[1] - 1)} {fmt(c[0] - 5)} {fmt(c[1] + 2)}"),
            line(f"M{fmt(c[0])} {fmt(c[1] + 2.25)}C{fmt(c[0] + 3)} {fmt(c[1] + 2.25)} {fmt(c[0] + 4.75)} {fmt(c[1] + 1)} {fmt(c[0] + 5)} {fmt(c[1] - 2)}")]


@icon("weather-ship", CAT, "Ship with a radar dome on its cabin and a weather balloon rising from the deck",
      tags=["weather ship", "research vessel", "ocean station", "radiosonde", "ship", "marine forecast"])
def _(S):
    hull = poly([(2, 15), (22, 15), (19.5, 20.5), (4.5, 20.5)], closed=True, r=S.r * 0.6)
    return [shell(hull), line(poly([(5.5, 15), (5.5, 10.5), (13, 10.5), (13, 15)], r=S.r * 0.6)),
            line("M7.25 10.5A2 2 0 0 1 11.25 10.5"), shell(circle(18, 5, 2.75)), line(seg(18, 7.75, 18, 15))]


@icon("hail-net", CAT, "Fruit tree under a hail net stretched between poles with hailstones bouncing off",
      tags=["hail net", "anti hail net", "orchard", "crop protection", "hail", "agriculture"])
def _(S):
    return [line(seg(3.5, 9, 3.5, 21)), line(seg(20.5, 9, 20.5, 21)), line("M3.5 9Q12 14.5 20.5 9"),
            detail(seg(8, 10.25, 8, 12.25)), detail(seg(12, 11.25, 12, 11.75)), detail(seg(16, 10.25, 16, 12.25)),
            shell(circle(12, 16.5, 2.5)), line(seg(12, 19, 12, 21)), dot(6.5, 4, 1.4), dot(12, 5, 1.4), dot(17.5, 3.5, 1.4)]


@icon("hail-cannon", CAT, "Upright cone cannon pointing at the sky with sound rings rising from its mouth",
      tags=["hail cannon", "anti hail", "shock wave", "orchard", "vineyard", "hail"])
def _(S):
    cone = poly([(6.5, 11), (17.5, 11), (13.5, 18), (10.5, 18)], closed=True, r=S.r * 0.6)
    return [shell(cone), line(seg(12, 18, 12, 21)), line(seg(7, 21, 17, 21)),
            line(arc(12, 12, 5, 235, 305)), line(arc(12, 12, 8.75, 240, 300))]


@icon("polar-research-station", CAT, "Boxy research station raised on stilts above the snow with an antenna mast",
      tags=["polar station", "antarctic base", "research station", "arctic", "expedition", "science"])
def _(S):
    return [shell(rect(2.5, 6.5, 13, 7, min(S.R, 1.5))), Part("dot", rect(5, 9, 2.5, 2)), Part("dot", rect(10.5, 9, 2.5, 2)),
            line(seg(5, 13.5, 5, 18.5)), line(seg(13, 13.5, 13, 18.5)),
            line("M2 20.5C5 19.25 8 19.25 11 20.5S17 21.75 22 20.5"), line(seg(19.5, 3, 19.5, 19.5)), line(seg(17.5, 5.5, 21.5, 5.5))]


@icon("weather-wheel", CAT, "Round classroom weather chart in four segments with a pointer in the middle",
      tags=["weather wheel", "weather chart", "classroom", "today's weather", "teaching", "kids"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(seg(12, 3, 12, 8.5)), detail(seg(12, 15.5, 12, 21)),
            detail(seg(3, 12, 8.5, 12)), detail(seg(15.5, 12, 21, 12)), dot(12, 12, 2),
            detail(seg(13.5, 10.5, 16.5, 7.5)), dot(7.5, 7.5, 1.6),
            detail(seg(6, 15.5, 9, 18.5)), detail(seg(9, 15.5, 6, 18.5)), Part("dot", "M16.5 14.5C16.5 14.5 18.25 16.3 18.25 17.4A1.75 1.75 0 0 1 14.75 17.4C14.75 16.3 16.5 14.5 16.5 14.5Z")]


@icon("cloud-watching", CAT, "Person lying on their back in the grass looking up at a cloud",
      tags=["cloud watching", "daydreaming", "relax", "lying down", "outdoors", "summer"])
def _(S):
    return [shell(cloud(S, 0.55, 10, 9)), shell(circle(4.5, 15, 2.25)), line(poly([(7, 16.5), (13.5, 16.5), (16.5, 13), (20, 16.5)], r=S.r)),
            line(seg(2, 20.5, 22, 20.5))]


@icon("storm-chasing", CAT, "Van with a roof instrument rack driving toward a tornado",
      tags=["storm chasing", "storm chaser", "tornado", "severe weather", "field research", "van"])
def _(S):
    van = poly([(2, 18.5), (2, 12), (10.5, 12), (13.5, 15), (13.5, 18.5)], closed=True, r=S.r * 0.6)
    return [shell(van), shell(circle(5, 19.5, 1.5)), shell(circle(10.5, 19.5, 1.5)), line(seg(4, 12, 4, 9)), line(seg(2.5, 9, 8.5, 9)),
            line(seg(13, 3.5, 22, 3.5)), line(seg(14.5, 7.5, 21, 7.5)), line(seg(16.5, 11.5, 20.5, 11.5)), line(seg(18, 15.5, 20, 15.5))]


@icon("rain-ripple", CAT, "Raindrops falling onto water with a ripple ring spreading",
      tags=["rain ripple", "raindrops", "puddle", "rain on water", "splash", "rain"])
def _(S):
    return [line(ellipse(12, 17.5, 9.5, 3.75)), Part("dot", ellipse(12, 17.5, 3.5, 1.25)),
            *[line(slant(x, 3, 9)) for x in (7, 12.5, 18)]]


@icon("scud-cloud", CAT, "Low cloud base with ragged torn wisps hanging below it",
      tags=["scud", "fractus", "ragged cloud", "storm cloud", "cloud type", "weather"])
def _(S):
    w1 = poly([(3.5, 14), (10, 14), (8.5, 15.5), (10, 17.5), (5, 17)], closed=True, r=S.r * 0.4)
    w2 = poly([(12.5, 16.5), (20.5, 16), (18.5, 18), (19.5, 20.5), (14, 19.5)], closed=True, r=S.r * 0.4)
    return [shell(cloud(S, 0.66, 4, 11)), shell(w1), shell(w2)]


@icon("black-globe-thermometer", CAT, "Black globe on a short stand with a thermometer through its top",
      tags=["black globe", "globe thermometer", "wbgt", "heat stress", "radiant heat", "thermometer"])
def _(S):
    return [shell(circle(12, 13, 5.5)), dot(12, 13, 2), line(seg(12, 2.5, 12, 11)), line(seg(12, 18.5, 12, 21)), line(seg(8, 21, 16, 21))]


@icon("thermoscope", CAT, "Glass bulb on a long thin tube dipped upside down into a flask of water",
      tags=["thermoscope", "galileo", "air thermometer", "history of science", "temperature", "experiment"])
def _(S):
    return [shell(circle(12, 5.5, 3.25)), line(seg(12, 8.75, 12, 19)), line(poly([(6.5, 12.5), (6.5, 21), (17.5, 21), (17.5, 12.5)], r=S.r)),
            line(seg(8.5, 16, 10, 16)), line(seg(14, 16, 15.5, 16))]


@icon("propeller-anemometer", CAT, "Streamlined wind sensor with a propeller in front and a tail fin on a pole",
      tags=["propeller anemometer", "wind monitor", "aerovane", "wind speed", "wind direction", "weather station"])
def _(S):
    body = L(S, "M6.5 9L9 7H14.5V11H9Z", "M6.5 9Q7.5 7 9.5 7H14.5V11H9.5Q7.5 11 6.5 9Z")
    return [shell(body), line(seg(4.5, 3.5, 4.5, 14.5)), line(seg(14.5, 9, 18, 9)),
            shell(poly([(17.5, 11), (17.5, 5), (21.5, 3.5), (21.5, 11)], closed=True, r=S.r * 0.5)), line(seg(11, 11, 11, 21)), line(seg(7.5, 21, 14.5, 21))]


@icon("pyrheliometer", CAT, "Long narrow tube on a tracking mount pointed straight at the sun",
      tags=["pyrheliometer", "solar tracker", "direct sunlight", "solar radiation", "radiometer", "solar energy"])
def _(S):
    tube = rotd(rect(3.5, 12.25, 11, 3.5, min(S.R, 1)), -45, 9, 14)
    return [shell(circle(18, 6.5, 2.5)), *[line(d) for d in sun_rays(18, 6.5, 4.25, 5.25, only=(0, 1, 5, 6, 7))],
            shell(tube), line(seg(9, 16.5, 9, 21)), line(seg(5, 21, 13, 21))]


@icon("weather-logbook", CAT, "Notebook with a small sun at the top and ruled columns of weather entries",
      tags=["weather log", "weather diary", "observation log", "logbook", "record", "journal"])
def _(S):
    return [shell(rect(5, 2.5, 15, 19, min(S.R, 2))), *[line(seg(3, y, 7, y)) for y in (6.5, 12, 17.5)],
            detail(circle(11, 7, 1.75)), detail(seg(14.5, 7, 17, 7)),
            detail(seg(9, 12.5, 17, 12.5)), detail(seg(9, 16.5, 17, 16.5)), detail(seg(13, 11, 13, 19))]


# ============================================================================ ice, wind, snow and volcanoes

@icon("penitentes", CAT, "Tall narrow pointed snow blades leaning toward the sun",
      tags=["penitentes", "snow spikes", "ice blades", "high altitude", "andes", "glacier"])
def _(S):
    spikes = [((2, 21), (6, 9.5), (5.5, 21)), ((8.5, 21), (13, 6), (12, 21)), ((15, 21), (18.5, 12), (18.5, 21))]
    return [*[shell(poly([a, b, c], closed=True, r=S.r * 0.4)) for a, b, c in spikes],
            shell(circle(19.5, 4.5, 2.25)), *[line(d) for d in sun_rays(19.5, 4.5, 4, 5, only=(2, 3, 4))]]


@icon("frost-heave", CAT, "Road surface pushed up into a bulge by an ice lens in the soil below",
      tags=["frost heave", "ice lens", "pothole", "road damage", "permafrost", "freeze thaw"])
def _(S):
    return [line("M2 8H6C8 8 9 4.5 12 4.5S16 8 18 8H22"), line("M2 12H6C8 12 9 8.5 12 8.5S16 12 18 12H22"),
            shell(rect(6.5, 14.5, 11, 3.5, min(S.R, 1.75))), line(seg(2, 21, 22, 21))]


@icon("headwind", CAT, "Cyclist leaning forward into wind blowing straight at them",
      tags=["headwind", "head wind", "cycling", "wind resistance", "against the wind", "bike"])
def _(S):
    return [shell(circle(5, 17.5, 3)), shell(circle(14, 17.5, 3)), line(poly([(5, 17.5), (8, 12.5), (11.5, 17.5)], r=S.r * 0.5)),
            line(poly([(8, 12.5), (12.5, 12.5), (14, 17.5)], r=S.r * 0.5)), line(poly([(7, 11.5), (11, 7.5), (13, 11)], r=S.r * 0.5)),
            shell(circle(13, 4.5, 1.75)), line(seg(17, 5, 22, 5)), line(seg(18, 9.5, 22, 9.5)), line(seg(19, 14, 22, 14))]


@icon("wind-load", CAT, "Tall building with arrows of wind pushing against one side",
      tags=["wind load", "wind pressure", "structural engineering", "building", "wind force", "design load"])
def _(S):
    parts = [shell(rect(12.5, 2.5, 9, 19, min(S.R, 1.5))), detail(seg(15.5, 6.5, 15.5, 17.5)), detail(seg(18.5, 6.5, 18.5, 17.5))]
    for y in (6, 12, 18):
        parts += arrow(2, y, 9.5, y, S, 2.25)
    return parts


@icon("volcanic-winter", CAT, "Volcano spreading an ash veil across the sky with a snowflake below",
      tags=["volcanic winter", "ash cloud", "global cooling", "eruption", "climate", "cold"])
def _(S):
    ash = L(S, "M3 10H21A2.5 2.5 0 0 0 19.5 5.5A3 3 0 0 0 14 4.5A3.5 3.5 0 0 0 7.5 5A2.75 2.75 0 0 0 3 10Z",
            "M5 10H19.5A2.25 2.25 0 0 0 19.5 5.5A3 3 0 0 0 14 4.5A3.5 3.5 0 0 0 7.5 5A2.5 2.5 0 0 0 5 10Z")
    return [shell(ash), shell(poly([(2, 21), (6, 14), (10, 14), (14, 21)], closed=True, r=S.r * 0.6)),
            *[line(d) for d in asterisk(18.5, 17, 3.25)]]


@icon("carbon-budget", CAT, "Measuring cylinder nearly full of carbon cloud with a limit line near the top",
      tags=["carbon budget", "emissions limit", "co2", "carbon dioxide", "climate target", "net zero"])
def _(S):
    return [line(poly([(7, 3), (7, 19), (17, 19), (17, 3)], r=S.r)), line(seg(5, 21, 19, 21)), line(seg(7, 11.5, 9.5, 11.5)),
            line(seg(2, 7.5, 5, 7.5)), line(seg(9, 7.5, 15, 7.5)), line(seg(19, 7.5, 22, 7.5)), shell(cloud(S, 0.3, 9.5, 16.5))]


@icon("wave-height", CAT, "Ocean wave with a double-headed arrow from trough to crest",
      tags=["wave height", "swell", "sea state", "surf forecast", "ocean", "marine"])
def _(S):
    return [line("M2 12C4 5.5 7.5 5.5 9.5 12S15 18.5 17 12"), *darrow_v(20.5, 6.5, 17.5, S)]


@icon("melting-snowman", CAT, "Snowman slumped into a puddle under the sun",
      tags=["melting snowman", "thaw", "warm winter", "spring", "melt", "climate change"])
def _(S):
    body = path_to_d(U(P("M5 19C5 14 8 11.5 12 11.5S19 14 19 19Z"), P(rect(2.5, 18.5, 19, 2.5, 1.25))))
    return [shell(body), shell(circle(10.5, 7.5, 2.75)), line(seg(6.5, 4.5, 11, 3)),
            shell(circle(19, 4.5, 2)), *[line(d) for d in sun_rays(19, 4.5, 3.75, 4.75, only=(1, 2, 3, 4))]]


@icon("snow-covered-car", CAT, "Car with a thick rounded layer of snow piled on its roof and hood",
      tags=["snow covered car", "snowed in", "winter driving", "snowstorm", "car", "clear snow"])
def _(S):
    car = poly([(2, 18), (2, 14), (5, 13), (7.5, 10), (16.5, 10), (19, 13), (22, 14), (22, 18)], closed=True, r=S.r * 0.6)
    snow = L(S, "M6.5 8C6.5 4.5 17.5 4.5 17.5 8Z", "M8 8C6 8 6.5 4.5 12 4.5S18 8 16 8Z")
    return [shell(car), shell(snow), shell(circle(6.5, 19, 2)), shell(circle(17.5, 19, 2))]


@icon("weather-drone", CAT, "Quadcopter drone carrying a sensor pod below a cloud",
      tags=["weather drone", "atmospheric drone", "uav", "meteorology", "sensor", "profiling"])
def _(S):
    return [shell(cloud(S, 0.45, 7.5, 7.5)), shell(rect(9, 13, 6, 3.5, min(S.R, 1.25))), line(seg(4.5, 12.5, 19.5, 12.5)),
            line(seg(4.5, 12.5, 4.5, 10.5)), line(seg(19.5, 12.5, 19.5, 10.5)), line(seg(2, 10.5, 7, 10.5)), line(seg(17, 10.5, 22, 10.5)),
            line(seg(12, 16.5, 12, 18)), shell(circle(12, 20, 1.75))]


@icon("volcanic-lightning", CAT, "Volcano with a tall ash plume lit by two lightning bolts",
      tags=["volcanic lightning", "dirty thunderstorm", "eruption", "lightning", "ash plume", "volcano"])
def _(S):
    plume = cloud(S, 0.8, 3.9, 12)
    return [shell(plume), detail(poly([(9.5, 5.5), (7.5, 8), (10, 8), (8.5, 10.5)], r=S.r * 0.3)),
            detail(poly([(16, 7), (14, 9.5), (16.5, 9.5), (15, 11.5)], r=S.r * 0.3)),
            shell(poly([(2, 21.5), (8, 15), (16, 15), (22, 21.5)], closed=True, r=S.r * 0.6))]


@icon("hodograph", CAT, "Polar grid with a curving line of dots spiralling out from the centre",
      tags=["hodograph", "wind shear", "storm forecasting", "sounding", "meteorology", "polar plot"])
def _(S):
    pts = [(12, 12), (14.5, 12.5), (16.5, 10.5), (17, 7.5)]
    return [line(circle(12, 12, 9.5)), line(circle(12, 12, 5)), line(seg(1.5, 12, 22.5, 12)), line(seg(12, 1.5, 12, 22.5)),
            line(L(S, poly(pts), "M12 12C14 12 17 12.5 17 7.5")),
            *[(Part("dot", rect(x - 1.5, y - 1.5, 3, 3)) if S.name == "line" else dot(x, y, 1.6)) for x, y in pts[1:]]]


# ============================================================================ cloud types and diagrams

def _castle(S):
    base = P(rect(2.5, 14, 19, 6, 3))
    turrets = []
    for x, top in ((4, 10), (10.25, 6), (16.5, 9)):
        if S.name == "line":
            turrets.append(P(rect(x, top, 3.5, 16 - top, 1)))
        else:
            turrets.append(U(P(rect(x, top + 1.75, 3.5, 14.25 - top)), P(circle(x + 1.75, top + 1.75, 1.75))))
    return path_to_d(U(base, *turrets))


@icon("castellanus-cloud", CAT, "Flat cloud layer with a row of turret towers rising from its top",
      tags=["castellanus", "castellatus", "turret cloud", "cloud type", "instability", "thunderstorm sign"])
def _(S):
    return [shell(_castle(S))]


def _horseshoe(S):
    cap = "butt" if S.name == "line" else "round"
    tube = ST(arc(12, 16, 6.5, 180, 360), 5, cap, "round")
    bumps = [P(circle(*polar(12, 16, 8, a), 2.25)) for a in (215, 270, 325)]
    return path_to_d(U(tube, *bumps))


@icon("horseshoe-cloud", CAT, "Small arched cloud shaped like an upside down U",
      tags=["horseshoe cloud", "horseshoe vortex", "arch cloud", "rare cloud", "cloud type", "sky"])
def _(S):
    return [shell(_horseshoe(S))]


_FLAMES = ("M6 13C4.5 10 5.5 7.5 7.5 5.5C8 7 8.75 8 10 8.75C9.75 6 10.75 3.75 12.5 2C13 4.5 14.25 6 15.25 7.5"
           "C15.75 6.75 16 5.75 16 4.5C18 6.5 19.5 9.5 18 13Z")


def _burn_filled():
    g = circle(12, 15.5, 6.5)
    return U(D(region(_FLAMES), grow(region(g), 1.5)),
             D(region(g), ST("M12 9V22", 2), ST(ellipse(12, 15.5, 3, 6.5), 2), ST("M5.5 15.5H18.5", 2)))


@icon("burning-earth", CAT, "Globe with flames rising from its top edge",
      tags=["burning earth", "global warming", "climate crisis", "heat", "planet on fire", "climate change"],
      filled=_burn_filled)
def _(S):
    g = circle(12, 15.5, 6.5)
    return [cut_strokes(S, [_FLAMES], region(g), gap=1.5), shell(g), detail(ellipse(12, 15.5, 3, 6.5)), detail(seg(5.5, 15.5, 18.5, 15.5))]


@icon("earth-hourglass", CAT, "Hourglass with a small globe in the top bulb and sand gathered below",
      tags=["time running out", "climate deadline", "hourglass", "earth", "urgency", "sustainability"])
def _(S):
    glass = "M7 4.5C7 9 10.75 10.25 10.75 12S7 15 7 19.5H17C17 15 13.25 13.75 13.25 12S17 9 17 4.5Z"
    return [shell(glass), line(seg(4.5, 2.5, 19.5, 2.5)), line(seg(4.5, 21.5, 19.5, 21.5)), detail(circle(12, 7.5, 1.75)),
            Part("dot", poly([(9, 18.5), (12, 16), (15, 18.5)], closed=True, r=S.r * 0.3))]


@icon("avalanche-danger-scale", CAT, "Snowy mountain beside five rising bars of an avalanche danger rating",
      tags=["avalanche danger", "avalanche risk", "danger level", "hazard scale", "snow safety", "backcountry"])
def _(S):
    parts = [shell(poly([(2, 12), (5.5, 6), (7.5, 8.5), (10, 3.5), (13.5, 12)], closed=True, r=S.r * 0.5))]
    for k, x in enumerate((3, 7, 11, 15, 19)):
        parts.append(line(seg(x, 21, x, 19 - 2 * k)))
    return parts


def _plate(y0, S):
    return poly([(3, y0 + 2.5), (7, y0), (17, y0), (21, y0 + 2.5), (17, y0 + 5), (7, y0 + 5)], closed=True, r=S.r * 0.6)


@icon("capped-column-snowflake", CAT, "Short ice column capped by a wide flat hexagonal plate at each end",
      tags=["capped column", "snow crystal", "ice crystal", "snowflake type", "tsuzumi", "snow science"])
def _(S):
    return [shell(_plate(2.5, S)), shell(_plate(16.5, S)), line(seg(8.5, 7.5, 8.5, 16.5)), line(seg(15.5, 7.5, 15.5, 16.5)),
            line(seg(12, 7.5, 12, 16.5))]


@icon("grass-minimum-thermometer", CAT, "Thermometer lying on two forked stands just above the grass",
      tags=["grass minimum", "ground frost", "minimum thermometer", "frost", "weather station", "temperature"])
def _(S):
    parts = []
    for part in thermo(S, 12, 3, 17.5, 9, w=3.5, br=3):
        parts.append(Part(part.kind, movd(rotd(part.d, 90, 12, 12), 0, -3.5), part.attrs))
    for x in (9, 17):
        parts.append(line(poly([(x - 1.75, 9.5), (x, 12), (x + 1.75, 9.5)], r=S.r * 0.5)))
        parts.append(line(seg(x, 12, x, 18)))
    parts.append(line(poly([(2, 21), (3.5, 18), (5, 21), (6.5, 18), (8, 21)], r=S.r * 0.5)))
    parts.append(line(poly([(11, 21), (12.5, 18), (14, 21)], r=S.r * 0.5)))
    parts.append(line(poly([(19, 21), (20.5, 18), (22, 21)], r=S.r * 0.5)))
    return parts


@icon("intertropical-convergence-zone", CAT, "Globe with a band of clouds along the equator and winds meeting it from north and south",
      tags=["itcz", "doldrums", "trade winds", "equator", "tropics", "convergence"])
def _(S):
    band = "M3.5 13.5A2.1 2.1 0 0 1 7.75 13.5A2.1 2.1 0 0 1 12 13.5A2.1 2.1 0 0 1 16.25 13.5A2.1 2.1 0 0 1 20.5 13.5"
    return [shell(circle(12, 12, 9.5)), detail(band), detail(seg(12, 4, 12, 8.5)), detail(poly(arrow_head(12, 8.5, 90, 1.75), r=S.r * 0.4)),
            detail(seg(12, 21, 12, 17)), detail(poly(arrow_head(12, 17, -90, 1.75), r=S.r * 0.4))]


@icon("front-cross-section", CAT, "Side view of cold air wedging under warm air that rises into a cloud",
      tags=["weather front", "cold front", "frontal lifting", "air mass", "cross section", "meteorology"])
def _(S):
    wedge = L(S, "M2 21V12.5C8 12.5 12.5 16 15.5 21Z", "M2 19.5V14A1.5 1.5 0 0 1 3.5 12.5C8.5 12.5 12.5 16 15.5 21H3.5A1.5 1.5 0 0 1 2 19.5Z")
    return [shell(wedge), *arrow(21, 19.5, 14.5, 11, S, 2.25), shell(cloud(S, 0.45, 5.5, 8.5))]
