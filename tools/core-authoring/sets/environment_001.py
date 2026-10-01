"""TypeIcon Core: environment (batch 001).

Weather combinations, conditions and measurements, weather map symbols, weather instruments and seasonal
and calendar marks. The cloud is the shared Core cloud (see sets/nature.py); an object seen behind another
is cut with a 2 px gap.
"""
import math
import re

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, LINE, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "environment"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


_NUM = re.compile(r"[A-Za-z]|-?\d*\.?\d+(?:e-?\d+)?")


def _tx(d, s=1.0, dx=0.0, dy=0.0, cx=12.0, cy=12.0, mirror=False):
    """Uniformly scale a d-string about (cx, cy), optionally mirror it, then translate (absolute M L H V C Q A Z)."""
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
            rx, ry, rt, la, sw, x, y = toks[i:i + 7]
            if mirror:
                sw = "1" if sw == "0" else "0"
            out.append(f"{fmt(float(rx) * s)} {fmt(float(ry) * s)} {rt} {la} {sw} {X(x)} {Y(y)}")
            i += 7
        else:
            raise ValueError(f"unsupported command {cmd}")
    return "".join(out)


_CLOUD_LINE = "M4.5 19H19.5A3.8 3.8 0 0 0 18 11.7A6 6 0 0 0 6.5 10A4.7 4.7 0 0 0 4.5 19Z"
_CLOUD_ROUND = "M7 19H17.5A4.5 4.5 0 0 0 18 10.03A6 6 0 0 0 6.34 9.1A5 5 0 0 0 7 19Z"
_MOON = "M10.47 3.64A8.5 8.5 0 1 0 20.36 13.53A7 7 0 1 1 10.47 3.64Z"


def cloud(S, s=1.0, dx=0.0, dy=0.0, mirror=False):
    """The shared Core cloud, scaled about (12, 12) then moved."""
    return _tx(_CLOUD_LINE if S.name == "line" else _CLOUD_ROUND, s, dx, dy, mirror=mirror)


def top_cloud(S):
    return cloud(S, 0.72, 0, -3.5)


def region(d):
    return U(P(d), ST(d, 2))


def grow(p, g):
    return U(p, ST(path_to_d(p), 2 * g, "round", "round"))


def cut_strokes(S, ds, cutter, gap=2.0, w=2.0):
    """Stroke outlines of ds (in style S) minus grow(cutter, gap): for things seen behind another."""
    body = U(*[ST(d, w, S.cap, S.join) for d in ds])
    return solid(path_to_d(D(body, grow(cutter, gap))))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def sun_rays(cx, cy, r0, r1, n=8, start=0.0):
    return [seg(*polar(cx, cy, r0, start + k * 360 / n), *polar(cx, cy, r1, start + k * 360 / n)) for k in range(n)]


def slant(x, y0, y1, k=0.35):
    """A falling streak from (x, y0) to y1, leaning left as it falls."""
    return seg(x + (y1 - y0) * k / 2, y0, x - (y1 - y0) * k / 2, y1)


def wave(x0, x1, y, amp=1.5, n=3, up_first=True):
    w = (x1 - x0) / n
    s = -1 if up_first else 1
    d = f"M{fmt(x0)} {fmt(y)}"
    for k in range(n):
        a = x0 + k * w
        d += (f"Q{fmt(a + w / 4)} {fmt(y + s * amp * 2)} {fmt(a + w / 2)} {fmt(y)}"
              f"Q{fmt(a + 3 * w / 4)} {fmt(y - s * amp * 2)} {fmt(a + w)} {fmt(y)}")
    return d


def vwave(x, y0, y1, amp=1.5, n=2):
    """Smooth vertical wave from (x, y0) to (x, y1) with n full periods."""
    h = (y1 - y0) / n
    d = f"M{fmt(x)} {fmt(y0)}"
    for k in range(n):
        a = y0 + k * h
        d += (f"Q{fmt(x + amp * 2)} {fmt(a + h / 4)} {fmt(x)} {fmt(a + h / 2)}"
              f"Q{fmt(x - amp * 2)} {fmt(a + 3 * h / 4)} {fmt(x)} {fmt(a + h)}")
    return d


def head(S, tip, deg, size=3.0, spread=45):
    a = polar(*tip, size, deg + 180 - spread)
    b = polar(*tip, size, deg + 180 + spread)
    return poly([a, tip, b], r=S.r * 0.6)


def flake(S, cx, cy, R, branch=False, start=-90):
    parts = []
    for k in range(3):
        a = start + k * 60
        parts.append(line(seg(*polar(cx, cy, R, a), *polar(cx, cy, R, a + 180))))
    if branch:
        for k in range(6):
            a = start + k * 60
            ax, ay = polar(cx, cy, R * 0.6, a)
            parts.append(line(poly([polar(ax, ay, R * 0.36, a - 50), (ax, ay), polar(ax, ay, R * 0.36, a + 50)], r=S.r * 0.5)))
    return parts


def flake_ds(cx, cy, R, start=-90):
    return [seg(*polar(cx, cy, R, start + k * 60), *polar(cx, cy, R, start + k * 60 + 180)) for k in range(3)]


def thermo(S, x, level, top=3.0):
    d = L(S, f"M{x - 2} 14.63V{top}H{x + 2}V14.63A3.5 3.5 0 1 1 {x - 2} 14.63Z",
          f"M{x - 2} 14.63V{top + 2}A2 2 0 0 1 {x + 2} {top + 2}V14.63A3.5 3.5 0 1 1 {x - 2} 14.63Z")
    return [shell(d), detail(seg(x, level, x, 16)), dot(x, 17.5, 1.75)]


def drop_d(S, cx, cy, s=1.0):
    """Water drop with its point at (cx, cy - 7.5 s) and body centred on (cx, cy)."""
    d = L(S, "M12 2.5C12 2.5 16.5 7.5 16.5 10.5A4.5 4.5 0 0 1 7.5 10.5C7.5 7.5 12 2.5 12 2.5Z",
          "M11.3 3.3Q12 2.5 12.7 3.3C13.9 4.8 16.5 8 16.5 10.5A4.5 4.5 0 0 1 7.5 10.5C7.5 8 10.1 4.8 11.3 3.3Z")
    return _tx(d, s, cx - 12, cy - 10.5, 12, 10.5)


def spike(S, pts):
    return poly(pts, closed=True, r=S.r)


# ============================================================================ weather combinations

_SS_CLOUD = dict(s=0.64, dx=2.6, dy=-0.4)


def _sun_behind(S, cloud_kw, sx, sy, r=2.8, rays=(3, 4, 5, 6, 7)):
    c = cloud(S, **cloud_kw)
    sun = [circle(sx, sy, r)] + [sun_rays(sx, sy, r + 2.25, r + 3.5)[k] for k in rays]
    return [cut_strokes(S, sun, region(c)), shell(c)]


@icon("sun-shower", CAT, "Sun peeking out from behind a cloud with short rain streaks falling below.",
      tags=["sun shower", "sunny rain", "shower", "rain", "sun", "cloud", "weather"])
def _(S):
    return [*_sun_behind(S, _SS_CLOUD, 7.5, 8.5), *[line(slant(x, 17.5, 21.5)) for x in (11, 14.5, 18)]]


@icon("heavy-rain", CAT, "Cloud with four long slanted rain streaks pouring beneath it.",
      tags=["heavy rain", "downpour", "pouring", "rain", "storm", "cloud", "weather"])
def _(S):
    return [shell(top_cloud(S)), *[line(slant(x, 16.5, 22)) for x in (6.5, 10, 13.5, 17)]]


_BOLT2 = [(13.3, 11.5), (10, 16.3), (14, 16.3), (11.2, 21)]


@icon("rain-thunderstorm", CAT, "Cloud with a lightning bolt in the middle and a rain streak on each side.",
      tags=["thunderstorm", "thunder and rain", "lightning", "storm", "rain", "cloud", "weather"])
def _(S):
    bolt = poly(_BOLT2, r=S.r)
    return [cut_strokes(S, [top_cloud(S)], ST(poly(_BOLT2), 2)), line(bolt, stroke_miterlimit="8"),
            line(slant(5.5, 17.5, 21)), line(slant(18.5, 17.5, 21))]


@icon("snow-shower", CAT, "Sun peeking out from behind a cloud with two small snowflakes falling below.",
      tags=["snow shower", "flurries", "snow", "sun", "cloud", "winter", "weather"])
def _(S):
    return [*_sun_behind(S, _SS_CLOUD, 7.5, 8.5), *flake(S, 11.5, 19.3, 2.6), *flake(S, 18, 19.3, 2.6)]


@icon("heavy-snow", CAT, "Cloud with a dense field of snow dots falling beneath it in two rows.",
      tags=["heavy snow", "blizzard", "snowfall", "snow", "cloud", "winter", "weather"])
def _(S):
    return [shell(top_cloud(S)), *[dot(x, 18, 1.25) for x in (6.5, 12, 17.5)], *[dot(x, 21.3, 1.25) for x in (9.25, 14.75)],
            dot(3.8, 21.3, 1.25), dot(20.2, 21.3, 1.25)]


@icon("light-snow", CAT, "Cloud with two small snowflakes spaced widely beneath it.",
      tags=["light snow", "flurries", "snow", "cloud", "winter", "weather", "dusting"])
def _(S):
    return [shell(top_cloud(S)), *flake(S, 7.5, 19.5, 2.8), *flake(S, 16.5, 19.5, 2.8)]


_MN_MOON = dict(s=0.72, dx=-3.4, dy=-3.6)
_MN_CLOUD = dict(s=0.64, dx=2.6, dy=-0.4)


def _moon_behind(S):
    c = cloud(S, **_MN_CLOUD)
    return [cut_strokes(S, [_tx(_MOON, **_MN_MOON)], region(c)), shell(c)]


@icon("moon-rain", CAT, "Crescent moon behind a cloud with rain streaks falling below.",
      tags=["rainy night", "night rain", "moon", "rain", "cloud", "night", "weather"])
def _(S):
    return [*_moon_behind(S), *[line(slant(x, 17.5, 21.5)) for x in (11, 14.5, 18)]]


@icon("moon-snow", CAT, "Crescent moon behind a cloud with two small snowflakes falling below.",
      tags=["snowy night", "night snow", "moon", "snow", "cloud", "night", "weather"])
def _(S):
    return [*_moon_behind(S), *flake(S, 11.5, 19.3, 2.6), *flake(S, 18, 19.3, 2.6)]


_BOLT3 = [(15.5, 15), (12.3, 18.6), (16, 18.6), (13.5, 22)]


@icon("moon-thunderstorm", CAT, "Crescent moon behind a cloud with a lightning bolt beneath it.",
      tags=["night storm", "thunderstorm", "lightning", "moon", "cloud", "night", "weather"])
def _(S):
    return [*_moon_behind(S), line(poly(_BOLT3, r=S.r * 0.4), stroke_miterlimit="8")]


@icon("windy-cloud", CAT, "Cloud with wind lines sweeping out beneath it, the ends curling.",
      tags=["windy", "breezy", "gusty", "wind", "cloud", "weather", "blow"])
def _(S):
    return [shell(cloud(S, 0.66, 0, -5.5)), line("M3 15.5H16A2 2 0 1 1 14 17.5"), line("M3 19.5H10"),
            line("M14 19.5H19")]


@icon("snow-wind", CAT, "Snowflake with curling wind lines blowing across below and beside it.",
      tags=["blowing snow", "snowstorm", "wind", "snow", "winter", "blizzard", "weather"])
def _(S):
    return [*flake(S, 8, 8, 5), line("M13.5 9H18A2.5 2.5 0 1 0 15.5 6.5"), line("M3 17H17A2.5 2.5 0 1 1 14.5 19.5")]


@icon("smoke-haze", CAT, "Pale sun above three wavy plumes of smoke rising from the bottom edge.",
      tags=["smoke", "haze", "wildfire smoke", "smog", "air quality", "sun", "weather"])
def _(S):
    rays = sun_rays(12, 6.5, 4.5, 5.75)
    return [shell(circle(12, 6.5, 2.5)), *[line(rays[k]) for k in (0, 1, 3, 4, 5)],
            line(vwave(6, 21.5, 14.5, 1, 2)), line(vwave(12, 21.5, 11.5, 1, 2)), line(vwave(18, 21.5, 14.5, 1, 2))]


@icon("freezing-fog", CAT, "Three bars of fog with a small snowflake above them.",
      tags=["freezing fog", "ice fog", "fog", "mist", "snowflake", "cold", "weather"])
def _(S):
    return [*flake(S, 12, 6, 3.6), line(seg(3, 13, 21, 13)), line(seg(5, 17, 19, 17)), line(seg(3, 21, 21, 21))]


@icon("black-ice", CAT, "Road narrowing into the distance with a glossy patch on it and a snowflake above.",
      tags=["black ice", "icy road", "slippery road", "ice", "road", "winter", "driving"])
def _(S):
    road = poly([(9, 11), (15, 11), (21.5, 21.5), (2.5, 21.5)], closed=True, r=S.r * 0.6)
    return [*flake(S, 12, 5, 3.3), shell(road), detail(ellipse(12, 17, 4, 2.2))]


@icon("rime-ice", CAT, "Thin branch with a row of spiky ice needles growing along one side.",
      tags=["rime", "hoar frost", "frost", "ice needles", "branch", "winter", "freezing"])
def _(S):
    parts = [line(seg(3, 20, 21, 8)), line(seg(10, 15.3, 6.5, 10.5))]
    for t in (0.3, 0.52, 0.74, 0.95):
        x, y = 3 + 18 * t, 20 - 12 * t
        parts.append(line(seg(x, y, x - 2.2, y - 5.2)))
    return parts


# ============================================================================ ground level conditions


def _bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


@icon("dew-drops", CAT, "Bending blade of grass with three round droplets hanging along it.",
      tags=["dew", "morning dew", "droplets", "grass", "moisture", "condensation", "humidity"])
def _(S):
    p = [(3, 21), (5, 11), (12, 7), (21, 6)]
    drops = []
    for t, off in ((0.3, 3.6), (0.58, 3.4), (0.86, 3.2)):
        x, y = _bez(*p, t)
        drops.append(dot(x, y + off, 1.7))
    return [line("M3 21C5 11 12 7 21 6"), *drops]


@icon("puddle", CAT, "Flat puddle on the ground with a raindrop splashing into it.",
      tags=["puddle", "splash", "raindrop", "wet", "rain", "water", "ripple"])
def _(S):
    return [shell(drop_d(S, 12, 7, 0.62)), line("M6.5 14.5C6 12.5 7 11.5 8 11"), line("M17.5 14.5C18 12.5 17 11.5 16 11"),
            shell(ellipse(12, 18, 9, 3))]


@icon("rain-on-window", CAT, "Window pane with drops and wavy rain trails running down the glass.",
      tags=["rainy window", "raindrops on glass", "wet window", "rain", "glass", "weather", "trails"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(vwave(8.5, 7.5, 13, 0.6, 1)), dot(8.5, 16.5, 1.3),
            detail(vwave(15.5, 9.5, 14, 0.6, 1)), dot(15.5, 17.5, 1.3), dot(12, 8.5, 1.3)]


@icon("snow-accumulation", CAT, "Rounded mound of settled snow on the ground with flakes still falling above.",
      tags=["snow depth", "snow cover", "snowfall", "snowpack", "settled snow", "winter", "drift"])
def _(S):
    mound = L(S, "M2 21C2 16 6 13 12 13C18 13 22 16 22 21Z",
              "M2 19C2 15.5 6 13 12 13C18 13 22 15.5 22 19A2 2 0 0 1 20 21H4A2 2 0 0 1 2 19Z")
    return [shell(mound), dot(6.5, 5.5, 1.25), dot(12, 8.5, 1.25), dot(17.5, 5.5, 1.25), dot(3.5, 9.5, 1.25), dot(20.5, 9.5, 1.25)]


@icon("virga", CAT, "Cloud with curved rain streaks that fade out in the air before reaching the ground line.",
      tags=["virga", "dry rain", "evaporating rain", "rain shaft", "cloud", "desert", "weather"])
def _(S):
    return [shell(top_cloud(S)), line("M7.5 16.5Q6 19 7.5 21.5"), line("M12 16.5Q10.5 18.5 12 20"), line("M16.5 16.5Q15.5 17.5 16.5 18.5")]


# ============================================================================ cloud forms and storms

@icon("wall-cloud", CAT, "Wide flat cloud base with a lowered blocky step hanging beneath its middle, above a ground line.",
      tags=["wall cloud", "supercell", "tornado warning", "storm cloud", "lowering", "severe weather", "cloud"])
def _(S):
    body = L(S, "M7 17V11H2V9.5C2 8 3 7 4.5 7C5 4.8 7 4 9 4.5C10.5 3 13.5 3 15 4.5C17 4 19 4.8 19.5 7C21 7 22 8 22 9.5V11H17V17Z",
             "M8.5 17A1.5 1.5 0 0 1 7 15.5V11H4A2 2 0 0 1 2 9.5C2 8 3 7 4.5 7C5 4.8 7 4 9 4.5C10.5 3 13.5 3 15 4.5C17 4 19 4.8 19.5 7C21 7 22 8 22 9.5A2 2 0 0 1 20 11H17V15.5A1.5 1.5 0 0 1 15.5 17Z")
    return [shell(body), line(seg(2, 21.5, 22, 21.5))]


@icon("supercell", CAT, "Tall storm cloud with a wide flat anvil top and curved bands around its rotating column.",
      tags=["supercell", "thunderstorm", "rotating storm", "anvil cloud", "severe weather", "tornado", "cumulonimbus"])
def _(S):
    cl = L(S, "M3 9L6 6.2C9 4.5 15 4.5 18 6.2L21 9L15.5 9.6L17 21H7L8.5 9.6Z",
           "M2.5 9.5C3 8 4.5 7 6 6.2C9 4.5 15 4.5 18 6.2C19.5 7 21 8 21.5 9.5C21.7 10.5 21 10.8 20 10.6L15.8 9.8L17 20A1 1 0 0 1 16 21H8A1 1 0 0 1 7 20L8.2 9.8L4 10.6C3 10.8 2.3 10.5 2.5 9.5Z")
    return [shell(cl), detail("M9.5 13.5Q12 15.5 14.5 13.5"), detail("M9 17.3Q12 19.3 15 17.3")]


@icon("microburst", CAT, "Cloud with a downdraft shaft falling to the ground and spreading outward in curls.",
      tags=["microburst", "downburst", "downdraft", "wind shear", "storm", "aviation", "cloud"])
def _(S):
    return [shell(cloud(S, 0.62, 0, -6.2)), line("M10.5 12Q10.5 19 4.5 19.5"), line("M13.5 12Q13.5 19 19.5 19.5"),
            line(head(S, (4.5, 19.5), 175, 3)), line(head(S, (19.5, 19.5), 5, 3))]


@icon("noctilucent-cloud", CAT, "Crescent moon over thin rippled cloud bands high above the dark horizon line.",
      tags=["noctilucent", "night shining cloud", "twilight", "mesosphere", "polar clouds", "night sky", "cloud"])
def _(S):
    return [shell(_tx(_MOON, 0.45, 4.5, -5.2)), line(wave(3, 21, 13.5, 0.7, 3)), line(wave(3, 21, 17, 0.7, 3)),
            line(seg(2, 21.5, 22, 21.5))]


@icon("altocumulus", CAT, "Staggered pattern of small domed cloudlets arranged in regular rows.",
      tags=["altocumulus", "mackerel sky", "cloudlets", "sky pattern", "mid level cloud", "cloud", "weather"])
def _(S):
    return [shell(cloud(S, 0.45, -5.6, -5.6)), shell(cloud(S, 0.45, 5.6, -5.6)),
            shell(cloud(S, 0.45, -5.6, 5.6)), shell(cloud(S, 0.45, 5.6, 5.6))]


@icon("nimbostratus", CAT, "Thick flat rain cloud layer with a steady veil of rain lines falling beneath.",
      tags=["nimbostratus", "rain cloud", "steady rain", "overcast", "grey sky", "cloud layer", "cloud"])
def _(S):
    sheet = L(S, "M2 12H22V10.5A3.3 3.3 0 0 0 19 7.2A4.2 4.2 0 0 0 11.5 5.8A3.8 3.8 0 0 0 6 7.4A3.3 3.3 0 0 0 2 10.5Z",
              "M4 12A2 2 0 0 1 2 10A3.3 3.3 0 0 1 6 7.4A3.8 3.8 0 0 1 11.5 5.8A4.2 4.2 0 0 1 19 7.2A3.3 3.3 0 0 1 22 10A2 2 0 0 1 20 12Z")
    return [shell(sheet), *[line(slant(x, 15.5, 21.5, 0.25)) for x in (5, 9, 13, 17)]]


@icon("fogbow", CAT, "Broad arc drawn as short dashes above two horizontal bars of fog.",
      tags=["fogbow", "white rainbow", "fog", "mist", "optical phenomenon", "sky", "weather"])
def _(S):
    return [*[line(arc(12, 15, 9.5, a, a + 24)) for a in (183, 219, 255, 291, 327)], line(seg(3, 18.5, 21, 18.5)),
            line(seg(5, 22, 19, 22))]


@icon("whiteout", CAT, "Square view full of driving snow streaks with a faint walking figure in the middle.",
      tags=["whiteout", "blizzard", "snowstorm", "low visibility", "snow", "winter", "weather"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), dot(12, 9.5, 1.5), detail(seg(12, 12.5, 12, 17)),
            detail(seg(6.5, 7, 8.5, 9)), detail(seg(15.5, 6.5, 17.5, 8.5)), detail(seg(16, 14, 18, 16)), detail(seg(6, 14, 8, 16))]


@icon("dew-point", CAT, "Thermometer with a water drop forming beside it, the temperature where dew appears.",
      tags=["dew point", "condensation", "humidity", "temperature", "moisture", "thermometer", "weather"])
def _(S):
    return [*thermo(S, 7.5, 10), shell(drop_d(S, 17, 12.5, 0.85))]


# ============================================================================ measurements and readings

def sun_ds(cx, cy, r, r0, r1, n=8, start=0.0, skip=()):
    return [circle(cx, cy, r)] + [d for k, d in enumerate(sun_rays(cx, cy, r0, r1, n, start)) if k not in skip]


@icon("uv-index", CAT, "Small sun with rays above three rising bars, the ultraviolet exposure scale.",
      tags=["uv index", "ultraviolet", "sun exposure", "sunburn", "sunscreen", "radiation level", "weather"])
def _(S):
    rays = sun_rays(7.5, 7.5, 4.6, 6.2)
    return [shell(circle(7.5, 7.5, 2.4)), *[line(r) for k, r in enumerate(rays) if k in (2, 3, 4, 5, 6)],
            line(seg(10.5, 21, 10.5, 16.5)), line(seg(15, 21, 15, 12.5)), line(seg(19.5, 21, 19.5, 8.5))]


def _petals(cx, cy, pr, r, n=5):
    return union(*[circle(*polar(cx, cy, pr, -90 + k * 360 / n), r) for k in range(n)])


@icon("pollen-count", CAT, "Flower head on a stem with small pollen dots drifting off to the side.",
      tags=["pollen", "hay fever", "allergy", "allergen", "pollen level", "flower", "spring"])
def _(S):
    return [shell(_petals(8, 9, 3.4, 2.5)), dot(8, 9, 1.3), line(seg(8, 14.5, 8, 21.5)), line("M8 20Q12.5 20 12.5 16"),
            dot(16.5, 6.5, 1.25), dot(20, 10.5, 1.25), dot(15.5, 13, 1.25), dot(19.5, 17, 1.25), dot(15, 19.5, 1.25)]


@icon("air-quality-index", CAT, "Semicircle gauge in three graded segments with a needle at its hub pointing up.",
      tags=["air quality", "aqi", "pollution level", "smog", "air index", "gauge", "environment"])
def _(S):
    return [line(arc(12, 17, 9.5, 181, 233)), line(arc(12, 17, 9.5, 243, 297)), line(arc(12, 17, 9.5, 307, 359)),
            line(seg(12, 17, 12, 11.5)), dot(12, 17, 2)]


@icon("precipitation-chance", CAT, "Open umbrella with a small percent sign beside its handle.",
      tags=["chance of rain", "rain probability", "percent", "umbrella", "forecast", "showers", "weather"])
def _(S):
    canopy = "M3 12A9 9 0 0 1 21 12A3 3 0 0 0 15 12A3 3 0 0 0 9 12A3 3 0 0 0 3 12Z"
    return [shell(_tx(canopy, 0.78, -2.6, -2)), line(_tx("M12 12V18.5A2 2 0 0 1 8 18.5", 0.78, -2.6, -2)),
            dot(15.8, 15.6, 1.3), dot(20, 20.4, 1.3), line(seg(19.6, 14.8, 16.2, 21.2))]


@icon("wind-speed", CAT, "Two wind lines of different length above a small speedometer arc with its needle.",
      tags=["wind speed", "wind velocity", "anemometer", "knots", "mph", "breeze", "weather"])
def _(S):
    return [line(seg(3, 4.5, 14, 4.5)), line(seg(3, 8.5, 20, 8.5)), line(arc(12, 21, 7.5, 180, 360)),
            line(seg(12, 21, 15.5, 16)), dot(12, 21, 1.5)]


@icon("wind-gust", CAT, "Two sharp curling wind lines bursting in from the left with speed dashes.",
      tags=["gust", "strong wind", "wind burst", "squall", "gale", "windy", "weather"])
def _(S):
    return [line("M7.5 9H16A3 3 0 1 0 13 6"), line("M7.5 15H18A3 3 0 1 1 15 18"), line(seg(2, 9, 4.5, 9)), line(seg(2, 15, 4.5, 15))]


@icon("wind-direction", CAT, "Compass circle with a north marker and a wind arrow with a feathered tail crossing it.",
      tags=["wind direction", "compass", "wind vane", "bearing", "heading", "north", "weather"])
def _(S):
    tip = (16, 8.3)
    return [shell(circle(12, 12, 9)), dot(12, 5.6, 1.3), detail(seg(8, 16, *tip)), detail(head(S, tip, -45, 3.4)),
            detail(seg(6.8, 14.8, 9.2, 17.2)), detail(seg(9.3, 11.7, 11.7, 14.1))]


@icon("wind-chill", CAT, "Thermometer reading low with wind lines blowing past it and a small snowflake.",
      tags=["wind chill", "windchill", "cold wind", "freezing", "temperature", "winter", "weather"])
def _(S):
    return [*thermo(S, 7, 14), *flake(S, 17, 6, 3.3), line(wave(11.5, 21.5, 13.5, 1.2, 1)), line(wave(11.5, 21.5, 19, 1.2, 1))]


@icon("heat-index", CAT, "Thermometer reading high with a small sun and a water drop beside it.",
      tags=["heat index", "humidex", "humidity", "hot weather", "temperature", "summer", "weather"])
def _(S):
    rays = sun_rays(16, 5.5, 3.5, 4.6)
    return [*thermo(S, 7, 6), shell(circle(16, 5.5, 1.6)), *[line(r) for r in rays],
            shell(drop_d(S, 17, 16.5, 0.85))]


def _behind_filled(back, front, knock=()):
    """Filled design for an object behind another: back minus a 1.75 px gap around front, knocks, then front."""
    def f():
        b = D(back, grow(front, 1.75), *knock) if knock else D(back, grow(front, 1.75))
        return U(b, front)
    return f


@icon("feels-like-temperature", CAT, "Side view of a head and neck next to a thermometer, how warm or cold it feels.",
      tags=["feels like", "apparent temperature", "perceived temperature", "comfort", "thermometer", "weather", "person"])
def _(S):
    head_d = ("M3.5 21V17C3 15.5 2.5 14 2.5 12C2.5 7.5 5 4.5 8 4.5C10.5 4.5 12 6.2 12 8.5L12.6 11L11.2 11.8V13.6L10.6 14.6H9.4V21Z")
    return [shell(head_d), *thermo(S, 17.5, 9, 3.5)]


@icon("air-pressure", CAT, "Round dial with a needle and tick marks around its top edge, a barometer.",
      tags=["air pressure", "barometer", "atmospheric pressure", "hpa", "millibar", "dial", "weather"])
def _(S):
    ticks = [line(seg(*polar(12, 13.5, 9.6, a), *polar(12, 13.5, 11.2, a))) for a in (200, 235, 270, 305, 340)]
    return [shell(circle(12, 13.5, 6.5)), detail(seg(12, 13.5, 14.8, 10.7)), dot(12, 13.5, 1.6), *ticks]


@icon("daylight-hours", CAT, "Half sun rising over a horizon line with a small clock face in the upper corner.",
      tags=["daylight", "day length", "sunrise sunset", "hours of sun", "clock", "sun", "time"])
def _(S):
    rays = sun_rays(16, 17, 6.2, 8)
    return [line(seg(2, 17, 22, 17)), line(arc(16, 17, 3.5, 180, 360)), line(rays[6]), line(rays[7]),
            shell(circle(7, 7, 4.2)), detail("M7 4.8V7H9.2")]


@icon("temperature-high-low", CAT, "Thermometer with an upward marker at the top and a downward marker at the bottom of its scale.",
      tags=["high low", "temperature range", "max min", "daily range", "highest lowest", "thermometer", "forecast"])
def _(S):
    up = poly([(17.5, 5), (20.5, 10), (14.5, 10)], closed=True)
    dn = poly([(17.5, 19), (20.5, 14), (14.5, 14)], closed=True)
    return [*thermo(S, 7.5, 8), solid(up), solid(dn)]


# ============================================================================ forecasts


def _tile_sun_cloud(cx, cy):
    """Filled sun disc (partly hidden) and solid cloud inside a box, as knock-out regions (list of d strings)."""
    cl = _tx(_CLOUD_LINE, 0.5, cx + 2.2 - 12, cy + 1.9 - 12)
    sun = path_to_d(D(P(circle(cx - 2.4, cy - 1.5, 2.3)), grow(P(cl), 1.2)))
    return sun, cl


@icon("weather-forecast", CAT, "Calendar page holding a sun partly hidden behind a cloud.",
      tags=["forecast", "weather forecast", "weather calendar", "outlook", "daily weather", "sun and cloud", "planner"])
def _(S):
    sun, cl = _tile_sun_cloud(12, 15)
    return [shell(rect(3, 4, 18, 17, S.R)), detail(seg(3, 9.5, 21, 9.5)), line(seg(8, 2, 8, 5.5)), line(seg(16, 2, 16, 5.5)),
            Part("dot", sun), Part("dot", cl)]


@icon("weekly-forecast", CAT, "Calendar page with a row of three small symbols for sun, cloud and rain.",
      tags=["weekly forecast", "week ahead", "multi day forecast", "outlook", "sun cloud rain", "7 day", "planner"])
def _(S):
    cl = _tx(_CLOUD_LINE, 0.36, 0, 4)
    return [shell(rect(3, 4, 18, 17, S.R)), detail(seg(3, 9.5, 21, 9.5)), line(seg(8, 2, 8, 5.5)), line(seg(16, 2, 16, 5.5)),
            dot(6.6, 15.4, 1.6), Part("dot", cl), detail(seg(18.3, 13.6, 16.8, 17)), ]


@icon("hourly-forecast", CAT, "Clock face with a small cloud overlapping its lower right edge.",
      tags=["hourly forecast", "hour by hour", "next hours", "timeline", "clock", "cloud", "weather"])
def _(S):
    c = cloud(S, 0.58, 4.6, 4.4)
    face = circle(9.5, 9.5, 7)
    hands = ST("M9.5 5.5V9.5H12.5", 2)
    return [cut_strokes(S, [face], region(c)), line("M9.5 5.5V9.5H12.5"), shell(c)]


# ============================================================================ weather map symbols

_FRONT = [(2, 17), (9, 17), (14, 12.5), (22, 12.5)]


def _front_at(t, w):
    """Point and unit tangent/normal on the front curve; base endpoints a, b are w apart on the tangent."""
    (x, y) = _bez(*_FRONT, t)
    (x2, y2) = _bez(*_FRONT, min(1, t + 0.01))
    (x1, y1) = _bez(*_FRONT, max(0, t - 0.01))
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    tx, ty = dx / n, dy / n
    nx, ny = ty, -tx
    a = (x - tx * w / 2, y - ty * w / 2)
    b = (x + tx * w / 2, y + ty * w / 2)
    return (x, y), (nx, ny), a, b


def _tri(t, w=6.4, h=6.4, side=1):
    _, (nx, ny), a, b = _front_at(t, w)
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    apex = (mx + side * nx * h, my + side * ny * h)
    return poly([a, b, apex], closed=True)


def _semi(t, w=6.4, side=1):
    _, _, a, b = _front_at(t, w)
    sweep = 1 if side == 1 else 0
    return f"M{fmt(a[0])} {fmt(a[1])}A{fmt(w / 2)} {fmt(w / 2)} 0 0 {sweep} {fmt(b[0])} {fmt(b[1])}Z"


_FRONT_D = "M2 17C9 17 14 12.5 22 12.5"


@icon("cold-front", CAT, "Curved front line with solid triangles spaced along its upper side, a cold front on a weather map.",
      tags=["cold front", "weather front", "frontal boundary", "synoptic chart", "meteorology", "triangles", "forecast map"])
def _(S):
    return [line(_FRONT_D), *[solid(_tri(t)) for t in (0.14, 0.5, 0.86)]]


@icon("warm-front", CAT, "Curved front line with solid half circles spaced along its upper side, a warm front on a weather map.",
      tags=["warm front", "weather front", "frontal boundary", "synoptic chart", "meteorology", "semicircles", "forecast map"])
def _(S):
    return [line(_FRONT_D), *[solid(_semi(t)) for t in (0.14, 0.5, 0.86)]]


@icon("occluded-front", CAT, "Curved front line with triangles and half circles alternating on the same side.",
      tags=["occluded front", "occlusion", "weather front", "synoptic chart", "meteorology", "mixed front", "forecast map"])
def _(S):
    return [line(_FRONT_D), solid(_tri(0.15, 5.6, 5.6)), solid(_semi(0.47, 5.6)), solid(_tri(0.83, 5.6, 5.6))]


@icon("stationary-front", CAT, "Front line with triangles on one side and half circles on the other, alternating along it.",
      tags=["stationary front", "quasi stationary", "weather front", "synoptic chart", "meteorology", "stalled front", "forecast map"])
def _(S):
    return [line(_FRONT_D), solid(_tri(0.18, 5.6, 5.6)), solid(_tri(0.74, 5.6, 5.6)), solid(_semi(0.46, 5.6, -1))]


def _oval(S, cx, cy, rx, ry):
    if S.name == "line":
        k = 0.4
        pts = [(cx - rx * 0.55, cy - ry), (cx + rx * 0.55, cy - ry), (cx + rx, cy - ry * k), (cx + rx, cy + ry * k),
               (cx + rx * 0.55, cy + ry), (cx - rx * 0.55, cy + ry), (cx - rx, cy + ry * k), (cx - rx, cy - ry * k)]
        return poly(pts, closed=True)
    return ellipse(cx, cy, rx, ry)


@icon("high-pressure", CAT, "Capital H centred inside an oval isobar ring, the high pressure centre on a weather map.",
      tags=["high pressure", "anticyclone", "clear weather", "fair weather", "isobar", "weather map", "pressure system"])
def _(S):
    return [shell(_oval(S, 12, 12, 9.5, 8.5)), detail("M9 8.5V15.5"), detail("M15 8.5V15.5"), detail("M9 12H15")]


@icon("low-pressure", CAT, "Capital L centred inside an oval isobar ring, the low pressure centre on a weather map.",
      tags=["low pressure", "cyclone", "depression", "stormy weather", "isobar", "weather map", "pressure system"])
def _(S):
    return [shell(_oval(S, 12, 12, 9.5, 8.5)), detail(poly([(10, 8.5), (10, 15.5), (14.5, 15.5)], r=S.r * 0.4))]


_ISO_OUT = [(3.5, 11), (5, 6), (10, 3.5), (15.5, 4.5), (20, 8), (20.5, 14), (17, 19.5), (11, 20.5), (6, 18)]
_ISO_IN = [(8.5, 11), (10, 8), (13.5, 8.2), (15.5, 11.5), (13.5, 15), (10, 15.5)]


@icon("isobars", CAT, "Two nested irregular closed contour lines like the pressure rings on a weather chart.",
      tags=["isobars", "pressure contours", "pressure lines", "weather chart", "synoptic", "contour map", "meteorology"])
def _(S):
    k = S.r * 2
    return [line(poly(_ISO_OUT, closed=True, r=k)), line(poly(_ISO_IN, closed=True, r=k))]


@icon("weather-map", CAT, "Folded map in three panels with a sun dot on one panel and a front line with a triangle on another.",
      tags=["weather map", "forecast map", "synoptic chart", "weather chart", "front", "sun", "meteorology"])
def _(S):
    mp = poly([(2, 5), (8, 3), (16, 5), (22, 3), (22, 19), (16, 21), (8, 19), (2, 21)], closed=True, r=S.r)
    tri = poly([(9.8, 15), (13.2, 15), (11.5, 11.8)], closed=True)
    return [shell(mp), detail(seg(8, 3, 8, 19)), detail(seg(16, 5, 16, 21)), dot(19.3, 11.5, 1.3), Part("dot", tri)]


@icon("wind-barb", CAT, "Diagonal shaft with a small station circle at one end and two feather ticks at the other.",
      tags=["wind barb", "wind feather", "station model", "wind symbol", "meteorology", "weather chart", "knots"])
def _(S):
    return [shell(circle(9, 18.5, 2.5)), line(seg(9, 16, 9, 3.5)), solid(poly([(9, 3.5), (9, 9), (19, 6.25)], closed=True)),
            line(seg(9, 12, 17, 9.5)), line(seg(9, 15.5, 14, 14))]


@icon("beaufort-scale", CAT, "Four rising steps with wind lines above the low steps, the Beaufort wind force scale.",
      tags=["beaufort", "wind force", "wind scale", "gale scale", "wind strength", "steps", "meteorology"])
def _(S):
    st = poly([(2, 21), (2, 16), (7, 16), (7, 12), (12, 12), (12, 8), (17, 8), (17, 4), (22, 4), (22, 21)], closed=True, r=S.r)
    return [shell(st), line(seg(3, 4.5, 9.5, 4.5)), line(seg(3, 8, 9.5, 8))]


@icon("storm-warning-flag", CAT, "Flagpole flying a square flag with a solid square in its centre, the storm warning signal.",
      tags=["storm warning", "gale warning", "warning flag", "maritime flag", "signal flag", "coast guard", "small craft"])
def _(S):
    return [shell(rect(4, 3.5, 16, 10, min(S.R, 2))), Part("dot", rect(9.5, 6, 5, 5)), line(seg(4, 13.5, 4, 21.5))]


@icon("hurricane-warning-flags", CAT, "Flagpole flying two stacked square flags, each with a solid square in its centre.",
      tags=["hurricane warning", "storm signal", "two flags", "warning flags", "maritime", "coastal warning", "tropical cyclone"])
def _(S):
    return [shell(rect(4, 2.5, 16, 8, min(S.R, 3))), shell(rect(4, 13, 16, 8, min(S.R, 3))), line(seg(4, 10.5, 4, 13)),
            Part("dot", rect(10, 4.5, 4, 4)), Part("dot", rect(10, 15, 4, 4))]


# ============================================================================ instruments

@icon("barograph", CAT, "Recording drum with a zigzag pressure trace and a pen arm resting against it.",
      tags=["barograph", "pressure recorder", "barometer chart", "drum recorder", "meteorology", "instrument", "weather station"])
def _(S):
    return [shell(rect(3, 6, 12, 14, S.R)), detail(poly([(5.5, 15), (8, 11), (10, 16), (12.5, 10)], r=S.r * 0.5)),
            line(seg(21, 4.5, 16.4, 11.6)), dot(21, 4.5, 1.5), line(seg(21, 21, 21, 4.5))]


@icon("pyranometer", CAT, "Glass dome on a flat round base with two levelling feet, a solar radiation sensor.",
      tags=["pyranometer", "solar radiation", "sunshine sensor", "irradiance", "solar sensor", "instrument", "weather station"])
def _(S):
    dome = "M4.5 12.5A7.5 7.5 0 0 1 19.5 12.5Z"
    return [shell(dome), shell(rect(5, 14, 14, 3.5, min(S.R, 1.5))), line(seg(12, 17.5, 12, 21.5)), line(seg(7.5, 21.5, 16.5, 21.5)),
            dot(12, 9.5, 1.5)]


@icon("weather-radar", CAT, "Round radar dome on top of a lattice tower with two cross rungs.",
      tags=["weather radar", "doppler", "radar tower", "radome", "rain radar", "storm tracking", "meteorology"])
def _(S):
    return [shell(circle(12, 7, 4.6)), detail(seg(8, 7, 16, 7)), line(seg(10, 11.5, 6.5, 21.5)), line(seg(14, 11.5, 17.5, 21.5)),
            line(seg(8.6, 16, 15.4, 16)), line(seg(7.3, 20, 16.7, 20))]


@icon("radar-sweep", CAT, "Round radar screen with a sweeping arm from the centre and two echo blips.",
      tags=["radar screen", "radar sweep", "weather radar display", "echo", "scan", "precipitation radar", "tracking"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(seg(12, 12, 16.3, 7.7)), dot(12, 12, 1.5), dot(7.5, 14.5, 1.3), dot(15.5, 16, 1.3)]


@icon("weather-satellite", CAT, "Satellite with two solar panel wings looking down toward a curve of the Earth.",
      tags=["weather satellite", "earth observation", "meteorological satellite", "orbit", "cloud imagery", "remote sensing", "space"])
def _(S):
    return [shell(rect(9, 3, 6, 6.5, min(S.R, 1.5))), shell(rect(2, 4, 4.5, 4.5, 1)), shell(rect(17.5, 4, 4.5, 4.5, 1)),
            line(seg(6.5, 6.25, 9, 6.25)), line(seg(15, 6.25, 17.5, 6.25)), line(seg(10, 12, 8.5, 15.5)), line(seg(14, 12, 15.5, 15.5)),
            line("M2.5 22C6 18.5 18 18.5 21.5 22")]


@icon("snow-gauge", CAT, "Tall measuring stake with depth marks standing in a mound of snow.",
      tags=["snow gauge", "snow depth", "snow stake", "snowfall measurement", "snow pole", "ruler", "winter"])
def _(S):
    mound = L(S, "M2 21.5C2 18 6 16.5 12 16.5C18 16.5 22 18 22 21.5Z",
              "M2 20C2 17.5 6 16.5 12 16.5C18 16.5 22 17.5 22 20A1.5 1.5 0 0 1 20.5 21.5H3.5A1.5 1.5 0 0 1 2 20Z")
    return [line(poly([(9, 16.5), (9, 2.5), (15, 2.5), (15, 16.5)])), shell(mound), line(seg(9, 6.5, 12, 6.5)),
            line(seg(9, 10, 12, 10)), line(seg(9, 13.5, 12, 13.5))]


@icon("storm-glass", CAT, "Sealed glass bottle with a long neck and feathery crystals growing inside, a weather prediction glass.",
      tags=["storm glass", "weather glass", "crystals", "camphor", "fitzroy", "barometer", "vintage instrument"])
def _(S):
    body = L(S, "M10.5 3H13.5V7.2C16.8 8.7 18.3 11 18.3 13.5A6.3 6.3 0 0 1 5.7 13.5C5.7 11 7.2 8.7 10.5 7.2Z",
             "M10.5 4.5Q10.5 3 12 3Q13.5 3 13.5 4.5V7.2C16.8 8.7 18.3 11 18.3 13.5A6.3 6.3 0 0 1 5.7 13.5C5.7 11 7.2 8.7 10.5 7.2Z")
    return [shell(body), detail(seg(12, 10, 12, 18)), detail(seg(12, 13.2, 9.6, 11)), detail(seg(12, 13.2, 14.4, 11))]


@icon("weather-house", CAT, "Small chalet with two doorways, a sun mark in one and a little umbrella in the other.",
      tags=["weather house", "weather cottage", "folk barometer", "weatherhouse", "chalet", "forecast toy", "vintage"])
def _(S):
    house = poly([(3, 21), (3, 11), (12, 3.5), (21, 11), (21, 21)], closed=True, r=S.r)
    return [shell(house), detail(poly([(5.5, 21), (5.5, 14), (10.5, 14), (10.5, 21)])), detail(poly([(13.5, 21), (13.5, 14), (18.5, 14), (18.5, 21)])),
            dot(8, 17.5, 1.3), Part("dot", "M14.7 18.3A1.8 1.8 0 0 1 18.3 18.3Z")]


@icon("weather-buoy", CAT, "Floating buoy on wavy water with a mast carrying a small cup anemometer.",
      tags=["weather buoy", "ocean buoy", "sea monitoring", "marine sensor", "anemometer", "offshore", "float"])
def _(S):
    body = poly([(7, 16.5), (9, 11.5), (15, 11.5), (17, 16.5)], closed=True, r=S.r)
    return [shell(body), line(seg(12, 11.5, 12, 5)), line(seg(8.5, 4.5, 15.5, 4.5)), dot(8.5, 4.5, 1.5), dot(15.5, 4.5, 1.5),
            line(wave(2, 22, 20.5, 0.9, 3))]


@icon("lightning-detector", CAT, "Handheld box with an antenna on top and a small lightning bolt on its screen.",
      tags=["lightning detector", "storm detector", "strike sensor", "thunder alert", "antenna", "handheld", "storm warning"])
def _(S):
    bolt = poly([(13.3, 11), (9.6, 15.3), (12.2, 15.3), (10.7, 19), (14.6, 14.2), (12, 14.2)], closed=True)
    return [shell(rect(5.5, 8, 13, 13, S.R)), line(seg(9, 8, 9, 2.5)), Part("dot", bolt)]


@icon("ceilometer", CAT, "Small box instrument on the ground sending a dashed beam straight up to a cloud.",
      tags=["ceilometer", "cloud base", "cloud height", "lidar", "laser beam", "aviation weather", "sensor"])
def _(S):
    return [shell(cloud(S, 0.52, 0, -5.4)), line(seg(12, 12.5, 12, 14.3)), line(seg(12, 15.7, 12, 16.4)),
            shell(rect(6.5, 18.5, 11, 3, 1))]


# ============================================================================ seasons and calendars

def _leaf(cx, cy, w, h, deg):
    d = f"M{fmt(cx - w)} {fmt(cy)}Q{fmt(cx)} {fmt(cy - h)} {fmt(cx + w)} {fmt(cy)}Q{fmt(cx)} {fmt(cy + h)} {fmt(cx - w)} {fmt(cy)}Z"
    return rot(d, deg, cx, cy)


@icon("four-seasons", CAT, "Circle divided into four parts holding a flower, a sun, a leaf and a snowflake.",
      tags=["four seasons", "seasons", "spring summer autumn winter", "annual cycle", "climate", "year", "quarters"])
def _(S):
    flower = _petals(7.2, 7.2, 1.5, 1.3)
    sun = path_to_d(U(P(circle(16.8, 7.2, 1.2)), *[ST(seg(*polar(16.8, 7.2, 1.9, a), *polar(16.8, 7.2, 3, a)), 1.0) for a in range(0, 360, 90)]))
    leaf = _leaf(7.2, 16.8, 2.8, 1.5, -45)
    snow = path_to_d(U(*[ST(seg(*polar(16.8, 16.8, 2.7, a), *polar(16.8, 16.8, 2.7, a + 180)), 1.0) for a in (-90, -30, 30)]))
    return [shell(circle(12, 12, 9.5)), *[detail(seg(*polar(12, 12, 1.8, a), *polar(12, 12, 7.3, a))) for a in (0, 90, 180, 270)],
            Part("dot", flower), Part("dot", sun), Part("dot", leaf), Part("dot", snow)]


@icon("harvest-moon", CAT, "Large full moon sitting low over the horizon beside a stalk of ripe wheat.",
      tags=["harvest moon", "autumn moon", "full moon", "wheat", "harvest", "september", "night sky"])
def _(S):
    ears = [solid(_leaf(18, 5.5, 2.4, 1.1, 90)), solid(_leaf(16.2, 9, 2.4, 1.1, -55)), solid(_leaf(19.8, 9, 2.4, 1.1, 55)),
            solid(_leaf(16.2, 12.6, 2.4, 1.1, -55)), solid(_leaf(19.8, 12.6, 2.4, 1.1, 55))]
    return [shell(circle(8, 11.5, 5.5)), line(seg(2, 18, 22, 18)), line(seg(18, 18, 18, 8)), *ears]


@icon("hibernation", CAT, "Bear curled up asleep inside a cave opening with a small Z floating above it.",
      tags=["hibernation", "sleeping bear", "winter sleep", "cave", "torpor", "dormant", "animals in winter"])
def _(S):
    cave = "M3 21V12A9 9 0 0 1 21 12V21Z"
    z = poly([(14, 6.5), (18, 6.5), (14, 10), (18, 10)], r=S.r * 0.3)
    return [shell(cave), detail(z), Part("dot", ellipse(11, 18, 5.2, 3)), dot(7.5, 14.2, 1.5), dot(14.5, 14.2, 1.5)]


@icon("rainy-season", CAT, "Calendar page with a cloud and a few rain streaks drawn on it.",
      tags=["rainy season", "wet season", "monsoon season", "rain calendar", "rainfall months", "weather season", "planner"])
def _(S):
    cl = _tx(_CLOUD_LINE, 0.5, 0, 2.2)
    return [shell(rect(3, 4, 18, 17, S.R)), detail(seg(3, 9.5, 21, 9.5)), line(seg(8, 2, 8, 5.5)), line(seg(16, 2, 16, 5.5)),
            Part("dot", cl), detail(seg(9, 18.6, 8.2, 20.2)), detail(seg(12.4, 18.6, 11.6, 20.2)), detail(seg(15.8, 18.6, 15, 20.2))]


@icon("daylight-saving-time", CAT, "Clock face with a curved arrow looping around its left side and a small sun in the corner.",
      tags=["daylight saving", "dst", "clocks change", "spring forward", "fall back", "time change", "summer time"])
def _(S):
    return [shell(circle(10.5, 13.5, 5.3)), detail("M10.5 10.5V13.5H12.8"), line(arc(10.5, 13.5, 9, 100, 262)),
            line(head(S, polar(10.5, 13.5, 9, 262), 352, 3)), dot(19, 5.5, 2.4)]


@icon("lap-timer", CAT, "Stopwatch with a small flag on its face, used to time laps and splits.",
      tags=["lap timer", "stopwatch", "split time", "race timer", "lap counter", "sports timing", "chronometer"])
def _(S):
    flag = poly([(11.2, 10.4), (15.6, 12.4), (11.2, 14.4)], closed=True)
    return [shell(circle(12, 13.5, 8)), line(seg(12, 5.5, 12, 3)), line(seg(9.5, 2.5, 14.5, 2.5)), detail(seg(9.6, 10, 9.6, 17.5)),
            Part("dot", flag)]


@icon("wall-calendar", CAT, "Calendar page hanging from a nail on two cords, with a grid of day dots.",
      tags=["wall calendar", "hanging calendar", "monthly calendar", "planner", "dates", "nail", "schedule"])
def _(S):
    dots = [dot(x, y, 1.15) for y in (14, 18) for x in (8, 12, 16)]
    return [shell(rect(4, 7, 16, 14.5, S.R)), detail(seg(4, 11, 20, 11)), line(poly([(7.5, 7), (12, 2.8), (16.5, 7)], r=S.r * 0.5)),
            *dots]


@icon("lunar-calendar", CAT, "Calendar page with a crescent moon where the date number would be.",
      tags=["lunar calendar", "moon calendar", "moon dates", "lunar month", "lunisolar", "moon phase calendar", "planner"])
def _(S):
    moon = _tx(_MOON, 0.5, 0, 3.4)
    return [shell(rect(3, 4, 18, 17, S.R)), detail(seg(3, 9.5, 21, 9.5)), line(seg(8, 2, 8, 5.5)), line(seg(16, 2, 16, 5.5)),
            Part("dot", moon)]


@icon("advent-calendar", CAT, "Grid of small doors in three rows with the middle door opened.",
      tags=["advent calendar", "countdown calendar", "christmas calendar", "doors", "december", "holiday countdown", "surprise"])
def _(S):
    return [shell(rect(3, 3, 18, 18, S.R)), detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)), detail(seg(3, 9, 21, 9)),
            detail(seg(3, 15, 21, 15)), Part("dot", rect(10, 10, 4, 4)), dot(6, 6, 0.9), dot(18, 6, 0.9), dot(6, 18, 0.9), dot(18, 18, 0.9)]


@icon("leap-year", CAT, "Calendar page showing the date 29, the extra day added in a leap year.",
      tags=["leap year", "february 29", "leap day", "extra day", "29", "calendar", "every four years"])
def _(S):
    two = poly([(6, 13), (9.5, 13), (9.5, 15.5), (6, 15.5), (6, 18), (9.5, 18)], r=S.r * 0.4)
    nine = poly([(18, 18), (18, 13), (14.5, 13), (14.5, 15.5), (18, 15.5)], r=S.r * 0.4)
    return [shell(rect(3, 4, 18, 17, S.R)), detail(seg(3, 9.5, 21, 9.5)), line(seg(8, 2, 8, 5.5)), line(seg(16, 2, 16, 5.5)),
            detail(two), detail(nine)]


@icon("calendar-year", CAT, "Calendar page holding twelve small dots in four columns and three rows, one for each month.",
      tags=["calendar year", "year view", "twelve months", "annual calendar", "months", "yearly planner", "12 months"])
def _(S):
    dots = [dot(x, y, 1.25) for y in (9.5, 13.5, 17.5) for x in (6.5, 10.2, 13.8, 17.5)]
    return [shell(rect(3, 4, 18, 17, S.R)), line(seg(8, 2, 8, 5.5)), line(seg(16, 2, 16, 5.5)), *dots]


@icon("monsoon", CAT, "Rain cloud pouring over a palm tree whose fronds bend in the wind above a ground line.",
      tags=["monsoon", "tropical rain", "rainy season", "palm tree", "storm wind", "heavy rain", "tropics"])
def _(S):
    return [shell(cloud(S, 0.6, -4.6, -6)), line(slant(4.5, 11.5, 15.5)), line(slant(8, 11.5, 15.5)), line(slant(11.5, 11.5, 15.5)),
            line("M18 21.5Q17.5 16 19.5 11"), line("M19.5 11Q16.5 9.5 14.5 11.5"), line("M19.5 11Q22 9.5 22.5 12"),
            line("M19.5 11Q20.5 8 18.5 6"), line(seg(2, 21.5, 22, 21.5))]
