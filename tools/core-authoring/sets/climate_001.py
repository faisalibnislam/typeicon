"""TypeIcon Core: climate (batch 001).

Cloud types, fog, ice forms, winds, storm and radar signatures, sky optics, weather map symbols and
climate charts. The cloud outline is the shared Core cloud (see sets/nature.py) so these icons sit
next to the weather set. Objects seen behind another are cut with a 2 px gap.
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


def cloud(S, s=1.0, dx=0.0, dy=0.0, mirror=False):
    """The shared Core cloud, scaled about (12, 12) then moved."""
    return _tx(_CLOUD_LINE if S.name == "line" else _CLOUD_ROUND, s, dx, dy, mirror=mirror)


def region(d):
    """Area covered by a closed outline filled to its outer stroke edge."""
    return U(P(d), ST(d, 2))


def grow(p, g):
    """Path region p expanded by g px."""
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


def head(S, tip, deg, size=3.0, spread=45):
    """Open arrowhead at tip; deg is the direction the arrow travels (0 = right, 90 = down)."""
    a = polar(*tip, size, deg + 180 - spread)
    b = polar(*tip, size, deg + 180 + spread)
    return poly([a, tip, b], r=S.r * 0.6)


def wave(x0, x1, y, amp=1.5, n=3, up_first=True):
    """Smooth wave from x0 to x1 about y with n full periods."""
    w = (x1 - x0) / n
    s = -1 if up_first else 1
    d = f"M{fmt(x0)} {fmt(y)}"
    for k in range(n):
        a = x0 + k * w
        d += (f"Q{fmt(a + w / 4)} {fmt(y + s * amp * 2)} {fmt(a + w / 2)} {fmt(y)}"
              f"Q{fmt(a + 3 * w / 4)} {fmt(y - s * amp * 2)} {fmt(a + w)} {fmt(y)}")
    return d


def bumps(x0, x1, y, n, up=True):
    """Row of n semicircular bumps on the line y from x0 to x1 (open path)."""
    r = (x1 - x0) / (2 * n)
    d = f"M{fmt(x0)} {fmt(y)}"
    for k in range(n):
        d += f"A{fmt(r)} {fmt(r)} 0 0 {1 if up else 0} {fmt(x0 + (k + 1) * 2 * r)} {fmt(y)}"
    return d


def flake(S, cx, cy, R, branch=False, start=-90):
    """Snowflake: six spokes, optionally with side branches."""
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


def mountain(S, pts):
    return shell(poly(pts, closed=True, r=S.r))


# ============================================================================ cloud types

@icon("altostratus-cloud", CAT, "Flat sheet of mid-level cloud with a dim sun disk showing through it.",
      tags=["altostratus", "cloud", "overcast", "sheet cloud", "mid level", "weather"])
def _(S):
    sheet = L(S, "M2 15V8.5C3.5 7 5 6.5 7 6.7C9 5 11 4.5 13 5.5C15 4.5 17.5 4.7 19 6.3C20.5 6.5 22 7.5 22 8.5V15Z",
              "M4 15A2 2 0 0 1 2 13V8.5C3.5 7 5 6.5 7 6.7C9 5 11 4.5 13 5.5C15 4.5 17.5 4.7 19 6.3C20.5 6.5 22 7.5 22 8.5V13A2 2 0 0 1 20 15Z")
    return [shell(sheet), detail(circle(12, 10.25, 2.25)), line(seg(12, 18, 12, 21)), line(seg(7.5, 18, 6, 20.5)),
            line(seg(16.5, 18, 18, 20.5))]


@icon("stratocumulus-cloud", CAT, "Low layer of lumpy cloud rolls packed side by side in two rows.",
      tags=["stratocumulus", "cloud", "low cloud", "cloud rolls", "overcast", "weather"])
def _(S):
    def band(x0, x1, y, h):
        d = bumps(x0, x1, y, 3)
        if S.name == "line":
            return shell(d + f"V{fmt(y + h)}H{fmt(x0)}Z")
        return shell(d + f"V{fmt(y + h - 1.5)}A1.5 1.5 0 0 1 {fmt(x1 - 1.5)} {fmt(y + h)}H{fmt(x0 + 1.5)}A1.5 1.5 0 0 1 {fmt(x0)} {fmt(y + h - 1.5)}Z")
    return [band(2, 17, 8, 3.5), band(7, 22, 17, 3.5)]


def _tower(S):
    if S.name == "line":
        return "M5 21H19A3.2 3.2 0 0 0 17.9 15.2A3.3 3.3 0 0 0 16 9.2A4 4 0 0 0 8 9.2A3.3 3.3 0 0 0 6.1 15.2A3.2 3.2 0 0 0 5 21Z"
    return "M7 21H17A3 3 0 0 0 17.9 15.2A3.3 3.3 0 0 0 16 9.2A4 4 0 0 0 8 9.2A3.3 3.3 0 0 0 6.1 15.2A3 3 0 0 0 7 21Z"


@icon("towering-cumulus", CAT, "Tall cauliflower cloud with stacked lobes rising from a flat base.",
      tags=["cumulus congestus", "towering cumulus", "cloud", "convection", "tall cloud", "weather"])
def _(S):
    return [shell(_tower(S)), detail("M9.5 13A3 3 0 0 1 12 11"), detail("M14.5 17.5A3 3 0 0 0 12 15.5")]


@icon("pileus-cloud", CAT, "Rounded cumulus with a thin smooth cap cloud arched just above its top.",
      tags=["pileus", "cap cloud", "scarf cloud", "cumulus", "cloud", "weather"])
def _(S):
    dome = L(S, "M3 21H21A3.6 3.6 0 0 0 17.4 15.4A5.5 5.5 0 0 0 6.6 15.4A3.6 3.6 0 0 0 3 21Z",
             "M6 21H18A3.3 3.3 0 0 0 17.4 15.4A5.5 5.5 0 0 0 6.6 15.4A3.3 3.3 0 0 0 6 21Z")
    return [shell(dome), line(arc(12, 16.5, 10, 212, 328))]


@icon("roll-cloud", CAT, "Long tube shaped cloud rolling low over a flat horizon.",
      tags=["roll cloud", "arcus", "volutus", "morning glory", "tube cloud", "weather"])
def _(S):
    tube = L(S, "M7 4H22V14H7A5 5 0 0 1 7 4Z", "M7 4H19A3 3 0 0 1 22 7V11A3 3 0 0 1 19 14H7A5 5 0 0 1 7 4Z")
    return [shell(tube), detail("M18.5 10.75H7A1.9 1.9 0 1 1 8.9 8.85"), line(seg(2, 19.5, 22, 19.5))]


@icon("asperitas-cloud", CAT, "Cloud whose base hangs in deep rolling waves, like a rough sea seen from below.",
      tags=["asperitas", "undulatus", "wavy cloud", "cloud base", "cloud", "weather"])
def _(S):
    top = "C2 6 4 4.5 7 5C9 3 12.5 2.5 14.5 4.5C17 3.5 21 4.5 22 8V13"
    base = "C20.5 18 17.5 18 16.5 14.5C15.5 11.5 13 11.5 12 14.5C11 17.5 8.5 17.5 7.5 14.5C6.5 11.5 3.5 11.5 2 14Z"
    return [shell("M2 14V9.5" + top + base), line(wave(2, 22, 20, 0.8, 3))]


@icon("kelvin-helmholtz-cloud", CAT, "Row of cloud crests curling over like breaking waves along one layer.",
      tags=["kelvin helmholtz", "billow cloud", "fluctus", "wave cloud", "shear", "weather"])
def _(S):
    band = rect(2, 17, 20, 4, min(S.R, 2))
    crests = []
    for x in (2.5, 9, 15.5):
        crests.append(line(f"M{fmt(x)} 15C{fmt(x + 0.5)} 10 {fmt(x + 2)} 6 {fmt(x + 4.5)} 6A2.5 2.5 0 1 1 {fmt(x + 3.2)} 10.8"))
    return [shell(band), *crests]


_FS_OUT_L = ("M2 9.5A3 3 0 0 1 6.5 6A3.6 3.6 0 0 1 12 5A3.6 3.6 0 0 1 17.5 6A3 3 0 0 1 22 9.5V14.5"
             "A3 3 0 0 1 17.5 18A3.6 3.6 0 0 1 12 19A3.6 3.6 0 0 1 6.5 18A3 3 0 0 1 2 14.5Z")
_FS_OUT_R = ("M2.8 8A3 3 0 0 1 6.5 6A3.6 3.6 0 0 1 12 5A3.6 3.6 0 0 1 17.5 6A3 3 0 0 1 21.2 8A4 4 0 0 1 21.2 16"
             "A3 3 0 0 1 17.5 18A3.6 3.6 0 0 1 12 19A3.6 3.6 0 0 1 6.5 18A3 3 0 0 1 2.8 16A4 4 0 0 1 2.8 8Z")
_FS_HOLE = ellipse(12, 12, 6, 3.5)
_FS_WISPS = ["M10 8.5C10 10 11 10.5 10.5 12.5", "M14 8.5C14 10 15 10.5 14.5 12.5"]


@icon("fallstreak-hole", CAT, "Cloud layer with a clear oval hole and wispy streaks trailing down inside it.",
      tags=["fallstreak hole", "hole punch cloud", "cavum", "cloud hole", "ice crystals", "weather"],
      filled=lambda: U(D(region(_FS_OUT_L), P(ellipse(12, 12, 6.8, 4.3))), *[ST(w, 2.5, "round", "round") for w in _FS_WISPS]))
def _(S):
    return [shell(_FS_OUT_L), detail(_FS_HOLE), *[detail(w) for w in _FS_WISPS]]


@icon("pyrocumulus-cloud", CAT, "Puffy cloud billowing up from a smoke column above a wildfire.",
      tags=["pyrocumulus", "fire cloud", "flammagenitus", "wildfire", "smoke", "weather"])
def _(S):
    c = cloud(S, 0.62, 0, -6.2)
    fire = poly([(5, 21.5), (6.5, 17.5), (9, 19.5), (12, 16), (15, 19.5), (17.5, 17.5), (19, 21.5)], closed=True, r=S.r * 0.6)
    return [shell(c), line("M10.5 11.5C9.5 12.5 11.5 13.5 10.5 14.5"), line("M13.5 11.5C12.5 12.5 14.5 13.5 13.5 14.5"),
            shell(fire)]


_CAP_LENS = "M4 8.5C7 4.5 17 4.5 20 8.5C17 10.5 7 10.5 4 8.5Z"


@icon("cap-cloud", CAT, "Mountain with a smooth lens shaped cloud sitting on its summit.",
      tags=["cap cloud", "orographic cloud", "mountain cloud", "lenticular", "summit", "weather"])
def _(S):
    lens = L(S, "M4 7.5C7.5 3.5 16.5 3.5 20 7.5C16.5 10 7.5 10 4 7.5Z", "M4.3 7.8C7.5 3.5 16.5 3.5 19.7 7.8C16.8 9.9 7.2 9.9 4.3 7.8Z")
    mtn = poly([(2.5, 21), (12, 12), (15.5, 15.3), (17.5, 13.8), (21.5, 21)], closed=True, r=S.r)
    return [shell(lens), shell(mtn)]


_BAN_MTN = [(2, 21), (8.5, 4), (17, 21)]



_BAN_FLAG = "M9.5 10.5C9.5 8 12 6.5 14 7.5C15.5 5.5 18.5 5.3 19.8 7.3C21.2 7.3 22 8.5 22 10C19 10.5 17 12.2 14 12.8C12 13 10.3 12.3 9.5 10.5Z"


@icon("banner-cloud", CAT, "Mountain peak with a cloud streaming sideways from its lee side like a flag.",
      tags=["banner cloud", "flag cloud", "orographic cloud", "mountain", "peak", "weather"],
      filled=lambda: U(region(_BAN_FLAG), D(region(poly(_BAN_MTN, closed=True)), grow(region(_BAN_FLAG), 1.75))))
def _(S):
    mtn = poly(_BAN_MTN, closed=True, r=S.r)
    return [shell(_BAN_FLAG), cut_strokes(S, [mtn], region(_BAN_FLAG))]


@icon("cloud-streets", CAT, "Parallel rows of small puffy clouds lined up and receding into the distance.",
      tags=["cloud streets", "convective rolls", "cumulus rows", "cloud lines", "sky", "weather"])
def _(S):
    def row(x0, x1, y, n):
        d = bumps(x0, x1, y, n)
        return shell(d + "Z") if S.name == "line" else shell(d + "Z")
    return [row(2, 22, 20.5, 3), row(4.5, 19.5, 13.5, 3), row(7, 17, 7, 3)]


@icon("cloud-levels-chart", CAT, "Altitude axis with high wispy cloud, a lumpy mid-level cloud and a flat low layer.",
      tags=["cloud types", "cloud heights", "cloud chart", "cirrus", "stratus", "altitude"])
def _(S):
    axis = poly([(3, 3), (3, 21), (21, 21)], r=S.r)
    cirrus = [line("M8 5.5C11 5.5 13 3.5 16 3.5"), line("M13 7C16 7 18 5 20.5 5")]
    mid = L(S, "M8 14.5V12.5A2 2 0 0 1 11.5 11A2.5 2.5 0 0 1 16 11.5A2 2 0 0 1 18 14.5Z",
            "M9 14.5A1.5 1.5 0 0 1 8 12.5A2 2 0 0 1 11.5 11A2.5 2.5 0 0 1 16 11.5A2 2 0 0 1 17 14.5Z")
    return [line(axis), *cirrus, shell(mid), line(seg(8, 18, 20, 18))]


# ============================================================================ fog and mist

def _tree(S, cx, top, base, w):
    return shell(poly([(cx, top), (cx + w / 2, base), (cx - w / 2, base)], closed=True, r=S.r * 0.6))


@icon("forest-mist", CAT, "Row of pointed conifers with soft bands of mist drifting above them.",
      tags=["forest mist", "fog", "woodland", "conifers", "after rain", "haze"])
def _(S):
    trees = []
    for cx, top in ((5, 11), (12, 9.5), (19, 11)):
        trees += [_tree(S, cx, top, 18.5, 5.6), line(seg(cx, 18.5, cx, 21.5))]
    return [*trees, line(wave(3, 21, 6.5, 0.7, 3)), line(wave(6, 18, 3, 0.7, 2))]


@icon("valley-fog", CAT, "Fog lying in the valley between two hills under a clear sun.",
      tags=["valley fog", "radiation fog", "inversion", "hills", "fog", "morning"])
def _(S):
    hills = "M2 14C3 10.5 5 8.5 7 8.5C9 8.5 10.5 10.5 12 13C13.5 11 15 10 17 10C19 10 21 11.5 22 14"
    return [line(hills), line(seg(4, 17.5, 20, 17.5)), line(seg(7, 21, 17, 21)), shell(circle(12, 4, 1.75))]


_LH = [(14.5, 18), (15.5, 8.5), (15.5, 6), (17, 3.5), (18.5, 6), (18.5, 8.5), (19.5, 18)]
_SF_FOG = [seg(2, 11.5, 22, 11.5), seg(2, 15, 22, 15)]


_LH = [(15, 18), (16, 8.5), (16, 6), (17.5, 3.5), (19, 6), (19, 8.5), (20, 18)]
_SF_FOG = [seg(2, 11, 18.5, 11), seg(2, 15, 18.5, 15)]


_LH = [(15, 19), (16, 8.5), (16, 6), (17.5, 3.5), (19, 6), (19, 8.5), (20, 19)]
_SF_FOG = [seg(2, 10, 22, 10), seg(2, 14, 22, 14)]


@icon("sea-fog", CAT, "Bands of fog drifting over the sea, half hiding a lighthouse.",
      tags=["sea fog", "marine fog", "advection fog", "coastal fog", "lighthouse", "haar"],
      filled=lambda: U(D(region(poly(_LH, closed=True)), *[grow(ST(f, 2), 1.5) for f in _SF_FOG]),
                       *[ST(f, 2.5) for f in _SF_FOG], ST(wave(2, 22, 21, 0.6, 3), 2.5)))
def _(S):
    tower = poly(_LH, closed=True, r=S.r * 0.5)
    fog = [line(f) for f in _SF_FOG]
    return [cut_strokes(S, [tower], U(*[ST(f, 2) for f in _SF_FOG]), gap=1.5), *fog, line(wave(2, 22, 21, 0.6, 3))]


@icon("steam-fog", CAT, "Calm lake with curling wisps of vapor rising from the water.",
      tags=["steam fog", "sea smoke", "evaporation fog", "arctic sea smoke", "lake", "vapor"])
def _(S):
    wisp = "M{x} 15C{a} 13.5 {b} 12 {x} 10.5C{a} 9 {a} 6.5 {c} 5"
    ws = [line(wisp.format(x=x, a=fmt(x - 1.5), b=fmt(x + 1.5), c=fmt(x + 1))) for x in (7, 12, 17)]
    return [*ws, line(seg(2, 18.5, 22, 18.5)), line(seg(6, 21.5, 18, 21.5))]


@icon("hexagonal-plate-snowflake", CAT, "Flat six sided plate of ice with an inner hexagon and ridges to each corner.",
      tags=["plate crystal", "hexagonal plate", "snow crystal", "ice crystal", "snowflake", "hexagon"])
def _(S):
    outer = poly(regular(12, 12, 9.5, 6), closed=True, r=S.r)
    inner = poly(regular(12, 12, 4, 6), closed=True, r=S.r * 0.5)
    ridges = [detail(seg(*polar(12, 12, 4, a), *polar(12, 12, 7.2, a))) for a in range(-90, 270, 60)]
    return [shell(outer), detail(inner), *ridges]


@icon("column-snowflake", CAT, "Short upright six sided ice column with a hexagon end face.",
      tags=["column crystal", "hexagonal column", "snow crystal", "ice crystal", "prism", "snowflake"])
def _(S):
    out = poly([(8, 3.5), (16, 3.5), (20, 6), (20, 18), (16, 20.5), (8, 20.5), (4, 18), (4, 6)], closed=True, r=S.r)
    face = poly([(4, 6), (8, 8.5), (16, 8.5), (20, 6)], r=S.r)
    return [shell(out), detail(face), detail(seg(8, 8.5, 8, 20.5)), detail(seg(16, 8.5, 16, 20.5))]


def _lumpy(cx, cy, r, n, amp):
    pts = [polar(cx, cy, r, -90 + k * 360 / n) for k in range(n)]
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for k in range(n):
        q = pts[(k + 1) % n]
        d += f"A{fmt(r * math.sin(math.pi / n) + amp)} {fmt(r * math.sin(math.pi / n) + amp)} 0 0 1 {fmt(q[0])} {fmt(q[1])}"
    return d + "Z"


def _lumpy(cx, cy, r, n, k):
    pts = [polar(cx, cy, r, -90 + i * 360 / n) for i in range(n)]
    ch = 2 * r * math.sin(math.pi / n)
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(n):
        q = pts[(i + 1) % n]
        d += f"A{fmt(ch * k)} {fmt(ch * k)} 0 0 1 {fmt(q[0])} {fmt(q[1])}"
    return d + "Z"


@icon("hailstone-cross-section", CAT, "Hailstone cut in half showing layered growth rings around a small core.",
      tags=["hailstone", "hail", "growth rings", "cross section", "ice layers", "storm"])
def _(S):
    return [shell(_lumpy(12, 12, 8.8, 7, L(S, 0.8, 0.7))), detail(_lumpy(12, 12, 5, 5, 0.8)), dot(12, 12, 1.8)]


def _spark(cx, cy, R, r=0.9):
    return poly([polar(cx, cy, R if k % 2 == 0 else r, -90 + k * 45) for k in range(8)], closed=True)


def _spark(cx, cy, R, r=0.9):
    return poly([polar(cx, cy, R if k % 2 == 0 else r, -90 + k * 45) for k in range(8)], closed=True)


def _glint(cx, cy, R):
    k = R * 0.18
    pts = [(cx, cy - R), (cx + R, cy), (cx, cy + R), (cx - R, cy)]
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(4):
        q = pts[(i + 1) % 4]
        sx = 1 if i in (0, 1) else -1
        sy = -1 if i in (0, 3) else 1
        d += f"Q{fmt(cx + sx * k)} {fmt(cy + sy * k)} {fmt(q[0])} {fmt(q[1])}"
    return d + "Z"


@icon("diamond-dust", CAT, "Low sun on the horizon with tiny ice glints sparkling in the clear air.",
      tags=["diamond dust", "ice crystals", "ice fog", "clear sky precipitation", "sparkle", "arctic"])
def _(S):
    rays = [line(seg(*polar(7, 19.5, 5.5, a), *polar(7, 19.5, 7, a))) for a in (225, 270, 315)]
    ml = dict(stroke_miterlimit="2")
    return [line(seg(2, 19.5, 22, 19.5)), shell(arc(7, 19.5, 3.5, 180, 360) + "Z"), *rays,
            shell(_glint(15.5, 8.5, 5), **ml), shell(_glint(7.5, 6, 3), **ml), shell(_glint(19.5, 15, 2.8), **ml)]


@icon("lake-effect-snow", CAT, "Cloud band forming over a lake and dropping snow on the far shore.",
      tags=["lake effect snow", "snow band", "snow squall", "great lakes", "snowfall", "winter"])
def _(S):
    c = cloud(S, 0.6, 0, -6.5)
    return [shell(c), line(wave(2, 11, 20, 0.7, 2)), line("M13.5 21.5C15 20 17 19.5 22 19.5"),
            *flake(S, 17.5, 14.3, 3)]


@icon("wind-driven-rain", CAT, "Cloud with rain streaks slanting sharply sideways in a strong wind.",
      tags=["driving rain", "sideways rain", "wind and rain", "rainstorm", "gale", "weather"])
def _(S):
    c = cloud(S, 0.62, 2.8, -6.2)
    streaks = [line(seg(x, 14, x - 4.5, 21)) for x in (12, 16.5, 21)]
    return [shell(c), *streaks, line("M2 12.5H6A2 2 0 1 0 4 10.5"), line(seg(2, 16, 6.5, 16))]


@icon("snow-roller", CAT, "Hollow cylinder of wind rolled snow resting on a snowy surface.",
      tags=["snow roller", "snow bale", "snow doughnut", "wind", "snow", "winter"])
def _(S):
    face = L(S, ellipse(15.5, 12.5, 4, 5.5), ellipse(15.5, 12.5, 4.2, 5.5))
    body = union(face, "M15.5 7H8A5.5 5.5 0 0 0 8 18H15.5Z" if S.name == "line" else "M15.5 7H7.5A5.5 5.5 0 0 0 7.5 18H15.5Z")
    return [shell(body), detail(face), detail(ellipse(15.5, 12.5, 1.5, 2.3)), line(seg(2, 20.5, 22, 20.5))]


@icon("sastrugi", CAT, "Snow surface carved by the wind into sharp wavy ridges.",
      tags=["sastrugi", "snow ridges", "wind erosion", "snow dunes", "polar", "wind"])
def _(S):
    prof = [(2, 17.5), (7.5, 11.5), (8.5, 15.5), (14, 12), (15, 16), (20.5, 13), (22, 15)]
    d = poly([*prof, (22, 21), (2, 21)], closed=True, r=S.r * 0.6)
    return [shell(d), line("M3 7H16.5A2.25 2.25 0 1 0 14.25 4.75")]


_SL_HOUSE = [(5, 21), (5, 14), (12, 9), (19, 14), (19, 21)]


@icon("snow-load", CAT, "House with a heavy mound of snow on its roof pressing down.",
      tags=["snow load", "roof load", "heavy snow", "structural load", "winter", "house"])
def _(S):
    out = L(S, "M3 14V12.5C5 8 8.5 4.5 12 4.5C15.5 4.5 19 8 21 12.5V14H19V21H5V14Z",
            "M3 13.5V12.5C5 8 8.5 4.5 12 4.5C15.5 4.5 19 8 21 12.5V13.5Q21 14 20.5 14H19V19A2 2 0 0 1 17 21H7A2 2 0 0 1 5 19V14H3.5Q3 14 3 13.5Z")
    return [shell(out), detail(poly([(5, 14), (12, 9), (19, 14)], r=S.r)),
            detail(seg(12, 13, 12, 18.5)), detail(head(S, (12, 18.5), 90, 2.5))]


@icon("frost-depth", CAT, "Ground cross section with a dashed frost line below the surface.",
      tags=["frost depth", "frost line", "freezing depth", "frozen ground", "soil", "foundation"])
def _(S):
    dashes = [line(seg(a, 18, b, 18)) for a, b in ((7, 10), (13, 16), (19, 22))]
    arrow = [line(seg(3.5, 8.5, 3.5, 17)), line(head(S, (3.5, 17), 90, 2.3))]
    return [line(seg(2, 5, 22, 5)), *flake(S, 14, 11.5, 3.2), *dashes, *arrow]


_DROP = "M19 8.5C19 8.5 21.5 11.3 21.5 13A2.5 2.5 0 0 1 16.5 13C16.5 11.3 19 8.5 19 8.5Z"


@icon("freeze-thaw-cycle", CAT, "Two curved arrows cycling between a snowflake and a water drop.",
      tags=["freeze thaw", "frost weathering", "freezing and melting", "ice cycle", "thaw", "cycle"])
def _(S):
    c, r = (12, 12), 8.2
    top = arc(*c, r, 215, 322)
    bot = arc(*c, r, 35, 145)
    drop = L(S, _DROP, "M18.6 8.9Q19 8.4 19.4 8.9C20.2 9.9 21.5 11.6 21.5 13A2.5 2.5 0 0 1 16.5 13C16.5 11.6 17.8 9.9 18.6 8.9Z")
    return [*flake(S, 5, 12, 2.8), shell(drop), line(top), line(head(S, polar(*c, r, 322), 322 + 90, 2.4)),
            line(bot), line(head(S, polar(*c, r, 145), 145 + 90, 2.4))]


@icon("snowpack", CAT, "Mountain slope covered in stacked layers of snow.",
      tags=["snowpack", "snow layers", "snow depth", "avalanche", "slope", "winter"])
def _(S):
    ground = poly([(2, 21), (22, 21), (22, 11.5)], closed=True, r=S.r)
    return [shell(ground), line(seg(2, 16.8, 22, 7.3)), line(seg(2, 12.3, 22, 2.8)), *flake(S, 6, 5.5, 3)]


@icon("rope-tornado", CAT, "Thin twisting rope of a tornado hanging from a flat cloud base.",
      tags=["rope tornado", "tornado", "funnel cloud", "twister", "dissipating tornado", "storm"])
def _(S):
    base = L(S, "M3 8C3 5.5 5 4 7 4.5C8.5 2.5 12 2 14 3.5C16 2.5 19.5 3 20.5 5.5C21.5 6 21.5 8 21 8Z",
             "M4.5 8C2.5 8 3 5 7 4.5C8.5 2.5 12 2 14 3.5C16 2.5 19.5 3 20.5 5.5C22 6.2 21.5 8 20 8Z")
    rope = "M12.5 10C15.5 12 10 13.5 11.5 16C12.5 17.5 10 19.5 8 21"
    return [shell(base), line(rope), line(seg(3, 21, 21, 21))]


@icon("multiple-vortex-tornado", CAT, "Wide tornado funnel with smaller spinning vortices around its base.",
      tags=["multiple vortex", "wedge tornado", "suction vortices", "tornado", "twister", "storm"])
def _(S):
    rows = [(3, 21, 3.5), (4.5, 19.5, 7.5), (6.5, 17.5, 11.5), (8.5, 15.5, 15.5), (10, 14, 19.5)]
    return [*[line(seg(a, y, b, y)) for a, b, y in rows],
            line("M4.5 13C3 15.5 5.5 17 3.5 20.5"), line("M19.5 13C21 15.5 18.5 17 20.5 20.5")]


@icon("wind-shear", CAT, "Height axis with wind arrows of different lengths and directions at each level.",
      tags=["wind shear", "vertical shear", "wind profile", "turbulence", "aviation", "wind"])
def _(S):
    return [line(poly([(3, 3), (3, 21), (21, 21)], r=S.r)),
            line(seg(6.5, 5.5, 20, 5.5)), line(head(S, (20, 5.5), 0, 2.6)),
            line(seg(17, 11, 7.5, 11)), line(head(S, (7.5, 11), 180, 2.6)),
            line(seg(6.5, 16.5, 13, 16.5)), line(head(S, (13, 16.5), 0, 2.6))]


@icon("sea-breeze", CAT, "Coast with the sun over the land and a breeze blowing in from the sea.",
      tags=["sea breeze", "onshore wind", "coastal wind", "lake breeze", "coast", "wind"])
def _(S):
    land = poly([(12, 22), (13.5, 17), (22, 17), (22, 22)], closed=True, r=S.r * 0.5)
    rays = [line(r) for r in sun_rays(17.5, 6, 4, 5.25)]
    return [line(wave(2, 10, 19, 0.7, 2)), shell(land), shell(circle(17.5, 6, 2.2)), *rays,
            line("M2.5 14.5C5 9.5 9 9 12.5 12.5"), line(head(S, (12.5, 12.5), 45, 2.5))]


@icon("foehn-wind", CAT, "Rain cloud on one side of a mountain and warm dry wind sweeping down the other side.",
      tags=["foehn", "fohn wind", "chinook", "rain shadow", "downslope wind", "warm wind"])
def _(S):
    mtn = poly([(2, 21), (9, 9), (16, 21)], closed=True, r=S.r)
    c = cloud(S, 0.42, -6.8, -7.2)
    return [shell(mtn), shell(c), line("M12 6C15 6 17.5 8.5 18.5 12.5"), line(head(S, (18.5, 12.5), 78, 2.4)),
            shell(circle(19.5, 18.5, 2))]


@icon("katabatic-wind", CAT, "Cold air flowing downhill along the surface of a glacier slope.",
      tags=["katabatic wind", "fall wind", "drainage wind", "glacier wind", "cold air", "downslope"])
def _(S):
    ice = poly([(2, 7), (2, 21), (21.5, 21)], closed=True, r=S.r)
    return [shell(ice, stroke_miterlimit="2"), detail(seg(7, 10.75, 7, 15)), detail(seg(12, 14.5, 12, 17.5)),
            line(seg(6, 3.5, 13.5, 9.1)), line(head(S, (13.5, 9.1), 36.9, 2.5)),
            line(seg(13, 4.5, 20.5, 10.1)), line(head(S, (20.5, 10.1), 36.9, 2.5))]


@icon("trade-winds", CAT, "Globe with winds on both sides of the equator blowing toward it.",
      tags=["trade winds", "easterlies", "tropics", "equator", "global winds", "sailing"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(seg(3.5, 12, 20.5, 12)),
            detail(seg(16.5, 5.5, 9, 9)), detail(head(S, (9, 9), 155, 2.6)),
            detail(seg(16.5, 18.5, 9, 15)), detail(head(S, (9, 15), 205, 2.6))]


@icon("doldrums", CAT, "Sailboat with a slack, sagging sail on flat water under a blazing sun.",
      tags=["doldrums", "becalmed", "no wind", "calm sea", "intertropical", "sailing"])
def _(S):
    hull = poly([(3, 15.5), (15, 15.5), (13, 18.5), (5, 18.5)], closed=True, r=S.r * 0.5)
    sail = L(S, "M10 4Q11 11 15 13H10Z", "M10 5Q10 4 10.5 4.8Q11.5 11 14.5 12.3Q15 13 14 13H11Q10 13 10 12Z")
    rays = [line(r) for r in sun_rays(18, 6, 3.6, 4.6)]
    return [shell(hull), line(seg(8, 3, 8, 15.5)), shell(sail), shell(circle(18, 6, 1.9)), *rays, line(seg(2, 21.5, 22, 21.5))]


@icon("thermal-updraft", CAT, "Spiral of rising warm air above sunlit ground with a bird circling at the top.",
      tags=["thermal", "updraft", "rising air", "convection", "gliding", "soaring"])
def _(S):
    spiral = "M12 19C6.5 19 6.5 15 12 15C17.5 15 17.5 11 12 11C6.5 11 6.5 7.5 12 7.5V5"
    return [line(seg(2, 21.5, 22, 21.5)), line(spiral), line(head(S, (12, 4.5), -90, 2.5)),
            line("M15.5 5Q17 3.5 18.5 5Q20 3.5 21.5 5")]


@icon("atmospheric-river", CAT, "Narrow band of moisture streaming over the ocean onto a coastal mountain.",
      tags=["atmospheric river", "pineapple express", "moisture plume", "heavy rain", "flooding", "storm"])
def _(S):
    band = path_to_d(ST("M3 7C8 7 10 12.5 15 12.5", 4.5, S.cap, S.join))
    mtn = poly([(13, 21), (18.5, 12), (22, 17.5), (22, 21)], closed=True, r=S.r)
    return [shell(band), shell(mtn), line(wave(2, 11, 19.5, 0.7, 2))]


@icon("omega-block", CAT, "Jet stream bulging into an omega shaped loop around a high pressure center.",
      tags=["omega block", "blocking high", "jet stream", "heat dome", "high pressure", "weather map"])
def _(S):
    om = "M2 19H6C8 19 7.5 15.5 6.2 13.5A6.5 6.5 0 1 1 17.8 13.5C16.5 15.5 16 19 18 19H22"
    return [line(om), line(seg(9.75, 7, 9.75, 13)), line(seg(14.25, 7, 14.25, 13)), line(seg(9.75, 10, 14.25, 10))]


@icon("cold-wave", CAT, "Snowflake with wavy lines of cold air streaming behind it.",
      tags=["cold wave", "cold snap", "cold spell", "arctic blast", "freeze", "winter"])
def _(S):
    return [*flake(S, 16.5, 12, 5.5, branch=True), line(wave(2, 8.5, 7.5, 0.6, 1)), line(wave(2, 8.5, 12, 0.6, 1)),
            line(wave(2, 8.5, 16.5, 0.6, 1))]


@icon("saffir-simpson-scale", CAT, "Hurricane symbol beside five rising bars for the storm categories.",
      tags=["saffir simpson", "hurricane category", "hurricane scale", "wind scale", "cyclone rating", "storm"])
def _(S):
    bars = [line(seg(x, 21, x, t)) for x, t in ((5, 18.5), (9, 16), (13, 13.5), (17, 11), (21, 8.5))]
    return [shell(circle(7, 7.5, 2)), line("M7 5.5C4 5.5 2.5 7.5 2.3 10.5"), line("M7 9.5C10 9.5 11.5 7.5 11.7 4.5"), *bars]


@icon("enhanced-fujita-scale", CAT, "Tornado funnel beside six rising bars like a rating scale.",
      tags=["enhanced fujita", "ef scale", "tornado rating", "tornado scale", "damage scale", "storm"])
def _(S):
    xs = [3.5 + k * 3.6 for k in range(6)]
    bars = [line(seg(x, 21, x, 19 - k * 2)) for k, x in enumerate(xs)]
    funnel = [line(seg(2, 3, 11, 3)), line(seg(3.5, 6.5, 9.5, 6.5)), line(seg(5.5, 10, 8, 10))]
    return [*funnel, *bars]


@icon("hook-echo", CAT, "Radar storm echo with a curling hook at its lower corner inside a radar ring.",
      tags=["hook echo", "radar", "supercell", "tornado signature", "doppler", "storm"])
def _(S):
    blob = union(ellipse(13.5, 9.5, 4.5, 3.5), path_to_d(ST("M11 12C9 13 7.5 15 8.3 16.6C9 17.8 11 17.4 10.9 15.8", 2.6, "round", "round")))
    ring = [line(arc(12, 12, 10, a, a + 60)) for a in (-60 + 15, 30 + 15, 120 + 15, 210 + 15)]
    return [shell(blob), *ring]


@icon("bow-echo", CAT, "Line of storms on radar bent into a bow with wind pushing out from its middle.",
      tags=["bow echo", "derecho", "squall line", "radar", "damaging winds", "storm"])
def _(S):
    outer = "M8 3C11 4 13 5 14 6.5A2.2 2.2 0 0 1 16.2 9.8A2.2 2.2 0 0 1 16.2 14.2A2.2 2.2 0 0 1 14 17.5C13 19 11 20 8 21"
    inner = "C10.5 17.5 12 15 12 12C12 9 10.5 6.5 8 3Z"
    return [shell(outer + inner, stroke_miterlimit="3"), line(seg(2.5, 12, 8.5, 12)), line(head(S, (8.5, 12), 0, 2.5))]


@icon("sprite-lightning", CAT, "Storm cloud with a jellyfish shaped glow of tendrils flaring above it.",
      tags=["red sprite", "sprite", "upper atmospheric lightning", "transient luminous event", "thunderstorm", "lightning"])
def _(S):
    c = cloud(S, 0.62, 0, 6.3)
    bell = L(S, "M6.5 7.5A5.5 4.5 0 0 1 17.5 7.5Z", "M8 7.5A1.5 1.5 0 0 1 6.6 5.6A5.5 4.5 0 0 1 17.4 5.6A1.5 1.5 0 0 1 16 7.5Z")
    return [shell(c), shell(bell), line(seg(8.5, 7.5, 8, 10)), line(seg(12, 7.5, 12, 10)), line(seg(15.5, 7.5, 16, 10))]


@icon("st-elmos-fire", CAT, "Top of a ship mast with a glowing flame and sparks around its tip.",
      tags=["st elmos fire", "corona discharge", "plasma glow", "mast", "sailing", "static electricity"])
def _(S):
    flame = L(S, "M12 2.5C14.5 5 15 7 15 8.5A3 3 0 0 1 9 8.5C9 7 9.5 5 12 2.5Z",
              "M11.6 3Q12 2.6 12.4 3C14.5 5.2 15 7 15 8.5A3 3 0 0 1 9 8.5C9 7 9.5 5.2 11.6 3Z")
    sparks = [line(seg(*polar(12, 8, 5.2, a), *polar(12, 8, 6.8, a))) for a in (180, 220, 320, 0)]
    return [shell(flame), *sparks, line(seg(12, 13.5, 12, 22)), line(seg(6, 17, 18, 17))]


@icon("intracloud-lightning", CAT, "Two clouds side by side with a lightning bolt jagging between them.",
      tags=["intracloud lightning", "cloud to cloud lightning", "sheet lightning", "thunderstorm", "lightning", "storm"])
def _(S):
    a = cloud(S, 0.42, -6.2, -5.5)
    b = cloud(S, 0.42, 6.2, -5.5)
    bolt = poly([(5.5, 12.5), (9, 18), (12, 14), (15, 18.5), (18.5, 12.5)], r=S.r * 0.4)
    return [shell(a), shell(b), line(bolt, stroke_miterlimit="8")]


@icon("fulgurite", CAT, "Lightning striking sand and leaving a branching glassy tube buried below.",
      tags=["fulgurite", "petrified lightning", "lightning glass", "sand", "geology", "lightning strike"])
def _(S):
    bolt = poly([(13.5, 2), (10.5, 6), (13.5, 6), (12, 8.5)], r=S.r * 0.4)
    roots = [line(poly([(12, 12.5), (12, 15), (8, 18.5), (7, 21.5)], r=S.r)), line(poly([(12, 15), (15.5, 17.5), (17, 21)], r=S.r)),
             line(seg(9.5, 17.2, 11, 21.5)), line(seg(14.5, 16.8, 19.5, 15.5))]
    return [line(bolt, stroke_miterlimit="8"), line(seg(2, 10.5, 22, 10.5)), *roots]


_PLANE = [(12, 7.5), (12.8, 10.3), (16.8, 12.6), (16.8, 13.6), (12.8, 12.6), (12.6, 15), (14.2, 16.1), (14.2, 16.8), (12, 16.3),
          (9.8, 16.8), (9.8, 16.1), (11.4, 15), (11.2, 12.6), (7.2, 13.6), (7.2, 12.6), (11.2, 10.3)]


@icon("glory-halo", CAT, "Airplane shadow on a cloud top ringed by two circular halos.",
      tags=["glory", "optical glory", "brocken spectre", "halo", "airplane", "cloud"])
def _(S):
    plane = poly(_PLANE, closed=True)
    if S.name != "line":
        plane = path_to_d(U(P(plane), ST(plane, 0.9, "round", "round")))
    return [line(circle(12, 12, 10)), line(circle(12, 12, 6.5)), solid(plane)]


@icon("circumzenithal-arc", CAT, "Upturned rainbow arc high in the sky above a low sun on the horizon.",
      tags=["circumzenithal arc", "upside down rainbow", "sky smile", "halo", "ice crystals", "optics"])
def _(S):
    return [line(arc(12, -3, 12, 45, 135)), line(arc(12, -3, 15.5, 55, 125)), line(seg(2, 20.5, 22, 20.5)),
            shell(arc(12, 20.5, 3.5, 180, 360) + "Z")]


@icon("green-flash", CAT, "Sun setting into the sea with a brief bright flash bursting from its top edge.",
      tags=["green flash", "sunset", "sunrise", "refraction", "horizon", "optics"])
def _(S):
    return [shell(arc(12, 15, 5, 180, 360) + "Z"), line(seg(2, 15, 22, 15)), line(wave(5, 19, 19.5, 0.6, 2)),
            shell(_glint(12, 5, 3), stroke_miterlimit="2"), line(seg(*polar(12, 15, 7, 225), *polar(12, 15, 8.5, 225))),
            line(seg(*polar(12, 15, 7, 315), *polar(12, 15, 8.5, 315)))]


@icon("lightning-distance", CAT, "Lightning bolt with a dashed line leading to a stopwatch counting to the thunder.",
      tags=["lightning distance", "flash to bang", "thunder", "count seconds", "storm safety", "stopwatch"])
def _(S):
    bolt = poly([(8, 2), (3, 10.5), (7.5, 10.5), (4, 19)], r=S.r * 0.4)
    dashes = [line(seg(a, 21.5, b, 21.5)) for a, b in ((8, 10), (12.5, 14.5), (17, 19))]
    return [line(bolt, stroke_miterlimit="8"), shell(circle(16.5, 12.5, 5)), line(seg(16.5, 5.5, 16.5, 6.5)),
            line(seg(14.5, 4.5, 18.5, 4.5)), detail(seg(16.5, 12.5, 16.5, 10)), *dashes]


@icon("station-model", CAT, "Weather station plot: a half filled circle with a wind barb and data marks.",
      tags=["station model", "station plot", "wind barb", "weather map", "synoptic", "meteorology"])
def _(S):
    return [shell(circle(12, 15.5, 3.5)), solid(arc(12, 15.5, 2.6, 90, 270) + "Z"), line(seg(12, 12, 12, 3)),
            line(seg(12, 3, 16.5, 1.8 + 0.7)), line(seg(12, 6.5, 16.5, 5.3 + 0.7)),
            line(seg(17.5, 12.5, 21, 12.5)), line(seg(17.5, 18.5, 21, 18.5)), line(seg(3, 12.5, 6.5, 12.5))]


def _okta_pie(r):
    return f"M12 12V{fmt(12 - r)}" + arc(12, 12, r, 270, 540)[arc(12, 12, r, 270, 540).index("A"):] + "Z"


@icon("cloud-cover-okta", CAT, "Sky cover symbol: a circle with three of its four quarters shaded.",
      tags=["okta", "cloud cover", "sky cover", "cloud amount", "station model", "meteorology"],
      filled=lambda: D(P(circle(12, 12, 10)), P("M13.5 10.5V4A8 8 0 0 1 20 10.5Z")))
def _(S):
    pie = L(S, "M12 12V5.5A6.5 6.5 0 1 0 18.5 12Z", "M12 11V6.5A1 1 0 0 1 13 5.5A6.5 6.5 0 1 1 5.5 12A6.5 6.5 0 0 1 11 5.6Z")
    if S.name != "line":
        pie = "M12 10.5V6.5A1 1 0 0 0 11 5.58A6.5 6.5 0 1 0 18.42 13A1 1 0 0 0 17.5 12H13.5A1.5 1.5 0 0 1 12 10.5Z"
    return [shell(circle(12, 12, 9)), solid(pie)]


def _thermo(S, x, top, cy, rb=3.2, half=1.8, level=None):
    """Thermometer: tube from top to a bulb of radius rb centred at (x, cy)."""
    yj = cy - math.sqrt(rb * rb - half * half)
    d = L(S, f"M{fmt(x - half)} {fmt(yj)}V{fmt(top)}H{fmt(x + half)}V{fmt(yj)}A{fmt(rb)} {fmt(rb)} 0 1 1 {fmt(x - half)} {fmt(yj)}Z",
          f"M{fmt(x - half)} {fmt(yj)}V{fmt(top + half)}A{fmt(half)} {fmt(half)} 0 0 1 {fmt(x + half)} {fmt(top + half)}V{fmt(yj)}"
          f"A{fmt(rb)} {fmt(rb)} 0 1 1 {fmt(x - half)} {fmt(yj)}Z")
    lv = top + 2.5 if level is None else level
    return [shell(d), detail(seg(x, lv, x, cy)), dot(x, cy, rb * 0.5)]


@icon("isotherm", CAT, "Wavy contour lines of equal temperature beside a thermometer.",
      tags=["isotherm", "temperature contour", "isoline", "weather map", "temperature map", "contour"])
def _(S):
    return [line("M2 8C4.5 5 7.5 11 10 8C11.5 6.2 12.5 6 14 6.5"), line("M2 15C4.5 12 7.5 18 10 15C11.5 13.2 12.5 13 14 13.5"),
            *_thermo(S, 18.5, 3, 17.5, level=9)]


def _zig(p0, p1, n, amp):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    ln = math.hypot(dx, dy)
    nx, ny = -dy / ln, dx / ln
    pts = []
    for k in range(n + 1):
        t = k / n
        s = 0 if k in (0, n) else (amp if k % 2 else -amp)
        pts.append((p0[0] + dx * t + nx * s, p0[1] + dy * t + ny * s))
    return pts


@icon("high-pressure-ridge", CAT, "Zigzag ridge axis stretching out from a large letter H.",
      tags=["ridge", "high pressure ridge", "ridge axis", "anticyclone", "weather map", "high pressure"])
def _(S):
    return [line(seg(3.5, 3, 3.5, 11)), line(seg(9.5, 3, 9.5, 11)), line(seg(3.5, 7, 9.5, 7)),
            line(poly(_zig((12.5, 12.5), (21, 21), 6, 1.6), r=S.r * 0.3))]


@icon("low-pressure-trough", CAT, "Dashed trough axis extending out from a large letter L.",
      tags=["trough", "low pressure trough", "trough axis", "weather map", "low pressure", "front"])
def _(S):
    dashes = [line(seg(12 + k * 3.5, 12.5 + k * 3.5, 14 + k * 3.5, 14.5 + k * 3.5)) for k in range(3)]
    return [line(poly([(4, 3), (4, 11), (10, 11)], r=S.r)), *dashes]


@icon("dryline", CAT, "Line with open half circles along one side, the dry line weather map symbol.",
      tags=["dryline", "dry line", "dew point front", "weather map", "front", "severe weather"])
def _(S):
    return [line(seg(2, 15, 22, 15)), *[line(arc(x, 15, 2.75, 180, 360)) for x in (6, 12, 18)]]


@icon("thunderstorm-map-symbol", CAT, "Weather map thunderstorm symbol: an R shaped mark whose leg ends in a lightning arrow.",
      tags=["thunderstorm symbol", "weather map", "synoptic symbol", "present weather", "lightning", "meteorology"])
def _(S):
    leg = poly([(15, 3.5), (10.5, 11.5), (16, 11.5), (12.5, 19.5)], r=S.r * 0.4)
    return [line(poly([(6, 21), (6, 3.5), (15, 3.5)], r=S.r)), line(leg, stroke_miterlimit="8"),
            line(head(S, (12.5, 19.5), 113.6, 2.8))]


@icon("shower-map-symbol", CAT, "Downward triangle with a dot above it, the rain shower map symbol.",
      tags=["shower symbol", "rain shower", "weather map", "synoptic symbol", "present weather", "meteorology"])
def _(S):
    return [shell(poly([(4.5, 9), (19.5, 9), (12, 20.5)], closed=True, r=S.r)), dot(12, 4.25, 2)]


@icon("skew-t-chart", CAT, "Chart with slanted grid lines and two jagged profile curves side by side.",
      tags=["skew t", "skew t log p", "sounding", "atmospheric profile", "radiosonde", "meteorology"])
def _(S):
    return [line(poly([(3, 3), (3, 21), (21, 21)], r=S.r)), line(seg(14, 17, 21, 10)), line(seg(16, 7, 20, 3)),
            line(poly([(9.5, 18), (8, 14), (9, 11), (7, 7.5), (7.5, 3.5)], r=S.r)),
            line(poly([(14, 13), (12.5, 10), (13, 7.5), (11.5, 3.5)], r=S.r))]


@icon("meteogram", CAT, "Stacked mini charts of temperature, wind and rain along a shared time axis.",
      tags=["meteogram", "forecast chart", "weather forecast", "time series", "temperature", "rainfall"])
def _(S):
    temp = poly([(3, 7), (7, 4), (11, 6), (15, 3), (21, 5.5)], r=S.r)
    barbs = [line(poly([(x, 13.5), (x, 10), (x + 2.5, 9)], r=S.r * 0.4)) for x in (4.5, 11, 17.5)]
    bars = [line(seg(x, 21, x, t)) for x, t in ((5, 18), (9, 16.5), (13, 19), (17, 17))]
    return [line(temp), *barbs, *bars, line(seg(21, 21, 21, 18.5))]


@icon("lapse-rate", CAT, "Height axis with a line slanting to colder as it rises beside a mountain.",
      tags=["lapse rate", "temperature gradient", "altitude", "adiabatic", "cooling with height", "atmosphere"])
def _(S):
    mtn = poly([(8, 21), (13, 13), (15.5, 16), (17.5, 13.5), (21.5, 21)], r=S.r)
    return [line(poly([(3, 3), (3, 21), (21, 21)], r=S.r)), line(mtn), line(seg(20, 9.5, 7.5, 3.5)), dot(20, 9.5, 1.6)]


@icon("spaghetti-plot", CAT, "Bundle of forecast lines starting at one point and spreading apart.",
      tags=["spaghetti plot", "ensemble forecast", "hurricane track", "model runs", "forecast spread", "uncertainty"])
def _(S):
    ends = [4, 9.5, 15, 20.5]
    lines = [line(f"M4 12C10 12 13 {fmt(y)} 21 {fmt(y)}") for y in ends]
    return [dot(3.5, 12, 2), *lines]


@icon("climate-projection", CAT, "Line chart that widens into a fan of possible futures after a now line.",
      tags=["climate projection", "scenario", "forecast", "uncertainty range", "future warming", "model"])
def _(S):
    past = poly([(3, 17), (5.5, 14.5), (7.5, 16), (10.5, 12.5)], r=S.r)
    fan = L(S, "M14 11L21 4V17Z", "M14.3 10.7Q14 11 14.4 11.2L20 16.5Q21 17 21 16V5Q21 4 20.3 4.7Z")
    now = [line(seg(12, 3, 12, 6)), line(seg(12, 9, 12, 12)), line(seg(12, 15, 12, 18))]
    return [line(past), shell(fan), *now, line(seg(3, 21, 21, 21))]


@icon("climograph", CAT, "Monthly rainfall bars with a curved temperature line running over them.",
      tags=["climograph", "climate graph", "climate diagram", "rainfall", "temperature", "monthly average"])
def _(S):
    bars = [line(seg(x, 21, x, t)) for x, t in ((4, 18), (8, 16), (12, 14.5), (16, 16), (20, 18.5))]
    return [*bars, line("M3 12C7 3.5 17 3.5 21 12")]


@icon("keeling-curve", CAT, "Graph with a sawtooth line steadily climbing from lower left to upper right.",
      tags=["keeling curve", "co2 concentration", "carbon dioxide", "mauna loa", "rising co2", "climate change"])
def _(S):
    pts = [(5, 17.5)]
    for k in range(5):
        x0, y0 = 5 + k * 3.2, 17.5 - k * 2.6
        pts += [(x0 + 2, y0 - 3.4), (x0 + 3.2, y0 - 2.6)]
    return [line(poly([(3, 3), (3, 21), (21, 21)], r=S.r)), line(poly(pts, r=S.r * 0.3))]


@icon("temperature-distribution-shift", CAT, "Two overlapping bell curves with the second shifted toward warmer.",
      tags=["distribution shift", "bell curve", "warming", "more hot extremes", "normal distribution", "climate change"])
def _(S):
    b1 = "M2 18C5 18 6 9 8.5 9C11 9 12 18 15 18"
    b2 = "M9 18C12 18 13 9 15.5 9C18 9 19 18 22 18"
    return [line(b1), line(b2), line(seg(8.5, 4.5, 14, 4.5)), line(head(S, (14.5, 4.5), 0, 2.5)), line(seg(3, 21.5, 21, 21.5))]


@icon("temperature-record", CAT, "Thermometer reading at its very top beside a prize medal.",
      tags=["record high", "record temperature", "hottest day", "heat record", "all time high", "temperature"])
def _(S):
    return [*_thermo(S, 7, 3, 17.5, rb=3.5, half=2, level=5.5), line(seg(14, 3, 16, 10)), line(seg(20.5, 3, 18.5, 10)),
            shell(circle(17.25, 15, 3.75))]


@icon("extreme-weather", CAT, "Storm cloud with a lightning bolt, a flame and a water drop beneath it.",
      tags=["extreme weather", "severe weather", "natural hazards", "climate risk", "disaster", "storm"])
def _(S):
    c = cloud(S, 0.62, 0, -6.4)
    bolt = poly([(13, 12), (10.5, 16.5), (13.5, 16.5), (11.5, 21.5)], r=S.r * 0.4)
    flame = L(S, "M5 13.5C7 15.5 7.8 17 7.8 18.5A2.8 2.8 0 0 1 2.2 18.5C2.2 17 3 15.5 5 13.5Z",
              "M4.6 13.9Q5 13.5 5.4 13.9C7 15.6 7.8 17 7.8 18.5A2.8 2.8 0 0 1 2.2 18.5C2.2 17 3 15.6 4.6 13.9Z")
    drop = L(S, "M19 13.5C19 13.5 21.8 16.8 21.8 18.5A2.8 2.8 0 0 1 16.2 18.5C16.2 16.8 19 13.5 19 13.5Z",
             "M18.6 14Q19 13.5 19.4 14C20.5 15.4 21.8 17.2 21.8 18.5A2.8 2.8 0 0 1 16.2 18.5C16.2 17.2 17.5 15.4 18.6 14Z")
    return [shell(c), line(bolt, stroke_miterlimit="8"), shell(flame), shell(drop)]


@icon("el-nino", CAT, "Ocean wave under a hot sun with an arrow pushing warm water east.",
      tags=["el nino", "enso", "warm phase", "pacific ocean", "sea surface temperature", "climate pattern"])
def _(S):
    rays = [line(r) for r in sun_rays(7, 6, 3.8, 5)]
    return [shell(circle(7, 6, 2)), *rays, line(wave(2, 22, 13.5, 0.8, 3)), line(seg(4, 18.5, 19.5, 18.5)),
            line(head(S, (20, 18.5), 0, 2.8))]


def _dashed_ellipse(cx, cy, rx, ry, n=8, frac=0.55):
    out = []
    for k in range(n):
        a0 = 2 * math.pi * k / n
        a1 = a0 + 2 * math.pi / n * frac
        p0 = (cx + rx * math.cos(a0), cy + ry * math.sin(a0))
        p1 = (cx + rx * math.cos(a1), cy + ry * math.sin(a1))
        out.append(f"M{fmt(p0[0])} {fmt(p0[1])}A{fmt(rx)} {fmt(ry)} 0 0 1 {fmt(p1[0])} {fmt(p1[1])}")
    return out


@icon("la-nina", CAT, "Ocean wave under a snowflake with a pool of cold water below the surface.",
      tags=["la nina", "enso", "cool phase", "pacific ocean", "cold water", "climate pattern"])
def _(S):
    return [*flake(S, 12, 5.5, 3.5), line(wave(2, 22, 11.5, 0.8, 3)), *[line(d) for d in _dashed_ellipse(12, 17.5, 7.5, 3.5, 8, 0.5)]]


@icon("thermohaline-circulation", CAT, "Ocean conveyor loop flowing along the surface, sinking deep and returning.",
      tags=["thermohaline circulation", "ocean conveyor belt", "amoc", "gulf stream", "ocean currents", "deep water"])
def _(S):
    surf = "M3.5 15C3.5 10.5 5 8.5 9 8.5H15.5"
    deep = "M19.5 10C21.5 13 21 20 15.5 20H9"
    return [line(wave(2, 22, 4, 0.6, 3)), line(surf), line(head(S, (16, 8.5), 0, 2.6)), line(deep), line(head(S, (8.5, 20), 180, 2.6))]


@icon("ice-thickness", CAT, "Cross section of a frozen lake with a ruler measuring the ice layer.",
      tags=["ice thickness", "lake ice", "ice safety", "frozen lake", "ice fishing", "measurement"])
def _(S):
    slab = rect(2, 7, 12.5, 5, min(S.R, 1.5))
    ruler = rect(17, 3, 4.5, 18, min(S.R, 1.5))
    ticks = [detail(seg(17, y, 19, y)) for y in (7, 12, 17)]
    return [shell(slab), line(wave(2, 14.5, 16, 0.6, 2)), line(wave(2, 14.5, 20, 0.6, 2)), shell(ruler), *ticks]


def _meander(cx, cy, r, amp, lobes, n=90):
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n
        rr = r + amp * math.cos(lobes * t)
        pts.append((cx + rr * math.cos(t), cy + rr * math.sin(t)))
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}" + "".join(f"L{fmt(x)} {fmt(y)}" for x, y in pts[1:]) + "Z"
    return d


@icon("polar-vortex", CAT, "Globe seen from above the pole with a wavy ring of cold air circling a snowflake.",
      tags=["polar vortex", "arctic blast", "cold outbreak", "jet stream", "arctic", "winter"],
      filled=lambda: U(D(P(circle(12, 12, 10.75)), region(_meander(12, 12, 6.1, 0.9, 5))),
                       *[ST(p.d, 2.2, "round", "round") for p in flake(LINE, 12, 12, 2.6)]))
def _(S):
    return [shell(circle(12, 12, 9.75)), detail(_meander(12, 12, 6.1, 0.9, 5)), *[detail(p.d) for p in flake(S, 12, 12, 2.6)]]
