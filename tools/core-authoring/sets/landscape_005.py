"""TypeIcon Core: landscape (batch 005).

Natural hazards and climate scenes, fungi and mushrooms, map reading and trail marks, Earth cycles and
ice and tree records. Ground lines sit at y 20 to 21.5; ground and water are kept 2 px clear of the
objects standing on them. Mushrooms share one cap language (dome cap, 2 px stem, ring where the species has one).
"""
import math
import re

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, LINE, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "landscape"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled body."""
    return Part("dot", d)


def smooth(pts, closed=False):
    """Smooth curve through points (Catmull-Rom converted to cubic Beziers)."""
    n = len(pts)
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if (closed or i > 0) else pts[i]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if (closed or i + 2 < n) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d + ("Z" if closed else "")


def wave(x0, x1, y, amp=1.2, n=3, up_first=True):
    """Smooth wave from x0 to x1 about y with n full periods."""
    w = (x1 - x0) / n
    s = -1 if up_first else 1
    d = f"M{fmt(x0)} {fmt(y)}"
    for k in range(n):
        a = x0 + k * w
        d += (f"Q{fmt(a + w / 4)} {fmt(y + s * amp * 2)} {fmt(a + w / 2)} {fmt(y)}"
              f"Q{fmt(a + 3 * w / 4)} {fmt(y - s * amp * 2)} {fmt(a + w)} {fmt(y)}")
    return d


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


def house(x0, x1, eave, apex, base):
    """House outline vertices: walls from base up to eave, roof to apex."""
    xm = (x0 + x1) / 2
    return [(x0, base), (x0, eave), (xm, apex), (x1, eave), (x1, base)]


def pine(cx, top, base, hw, tiers=2):
    """Pine tree outline (vertices): stacked triangles."""
    pts = [(cx, top)]
    h = base - top
    right, left = [], []
    for t in range(tiers):
        y0 = top + h * t / tiers
        y1 = top + h * (t + 1) / tiers
        w0 = hw * (0.55 + 0.45 * t / max(1, tiers - 1)) if tiers > 1 else hw
        right += [(cx + w0 * (0.6 if t else 0.45), y0 + (y1 - y0) * 0.5 if t else y0 + (y1 - y0) * 0.6), (cx + w0, y1)]
        left = [(cx - w0, y1), (cx - w0 * (0.6 if t else 0.45), y0 + (y1 - y0) * 0.5 if t else y0 + (y1 - y0) * 0.6)] + left
    return pts + right + left


def flame(cx, base, w, h):
    """Flame outline (d-string) standing on y=base with a main tongue and a small side tongue."""
    hw = w / 2
    top = base - h
    return (f"M{fmt(cx)} {fmt(base)}"
            f"C{fmt(cx - hw)} {fmt(base)} {fmt(cx - hw)} {fmt(base - h * 0.35)} {fmt(cx - hw * 0.6)} {fmt(base - h * 0.55)}"
            f"C{fmt(cx - hw * 0.5)} {fmt(base - h * 0.7)} {fmt(cx - hw * 0.15)} {fmt(base - h * 0.78)} {fmt(cx - hw * 0.1)} {fmt(top)}"
            f"C{fmt(cx + hw * 0.5)} {fmt(top + h * 0.15)} {fmt(cx + hw * 0.7)} {fmt(base - h * 0.55)} {fmt(cx + hw * 0.75)} {fmt(base - h * 0.55)}"
            f"C{fmt(cx + hw)} {fmt(base - h * 0.4)} {fmt(cx + hw)} {fmt(base)} {fmt(cx)} {fmt(base)}Z")


_NUM = re.compile(r"[A-Za-z]|-?\d*\.?\d+(?:e-?\d+)?")


def _tx(d, s=1.0, dx=0.0, dy=0.0, cx=12.0, cy=12.0):
    """Uniformly scale an absolute d-string (M L H V C Q A Z) about (cx, cy), then translate."""
    toks = _NUM.findall(d)
    out, i, cmd = [], 0, None

    def X(v):
        return fmt(cx + (float(v) - cx) * s + dx)

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
        if cmd in "ML":
            out.append(f"{X(toks[i])} {Y(toks[i + 1])}")
            i += 2
        elif cmd == "H":
            out.append(X(toks[i]))
            i += 1
        elif cmd == "V":
            out.append(Y(toks[i]))
            i += 1
        elif cmd in "CQ":
            n = {"C": 3, "Q": 2}[cmd]
            out.append(" ".join(f"{X(toks[i + 2 * k])} {Y(toks[i + 2 * k + 1])}" for k in range(n)))
            i += 2 * n
        elif cmd == "A":
            rx, ry, rt, la, sw, x, y = toks[i:i + 7]
            out.append(f"{fmt(float(rx) * s)} {fmt(float(ry) * s)} {rt} {la} {sw} {X(x)} {Y(y)}")
            i += 7
        else:
            raise ValueError(f"unsupported command {cmd}")
    return "".join(out)


_CLOUD_LINE = "M4.5 19H19.5A3.8 3.8 0 0 0 18 11.7A6 6 0 0 0 6.5 10A4.7 4.7 0 0 0 4.5 19Z"
_CLOUD_ROUND = "M7 19H17.5A4.5 4.5 0 0 0 18 10.03A6 6 0 0 0 6.34 9.1A5 5 0 0 0 7 19Z"


def cloud(S, s=1.0, dx=0.0, dy=0.0):
    """The shared Core cloud, scaled about (12, 12) then moved."""
    return _tx(_CLOUD_LINE if S.name == "line" else _CLOUD_ROUND, s, dx, dy)


def tube(d, w):
    """Open path thickened to a capsule-ended band of width w (d-string of its outline)."""
    return path_to_d(ST(d, w, "round", "round"))


def spiral_pts(cx, cy, r0, r1, a0, sweep, n=16):
    """Spiral arm points from radius r0 at angle a0 to radius r1 at a0 + sweep (degrees, screen angles)."""
    return [polar(cx, cy, r0 + (r1 - r0) * i / n, a0 + sweep * i / n) for i in range(n + 1)]


# ============================================================================ hazards and disasters

def rock(cx, cy, r, turn=0.0):
    """Small irregular solid rock (d-string): a chunky five-sided stone around (cx, cy)."""
    base = [(-1.0, -0.55), (-0.1, -1.0), (0.95, -0.45), (0.75, 0.75), (-0.55, 0.95)]
    pts = [(cx + x * r, cy + y * r) for x, y in base]
    return poly(rpts(pts, turn, cx, cy), closed=True, r=0.4)


@icon("moon-footprint", CAT, "Ribbed boot sole print pressed into dusty lunar ground.",
      tags=["moon", "footprint", "boot print", "astronaut", "lunar", "space", "apollo"])
def _(S):
    fore = [(8, 5), (10, 2.5), (14, 2.5), (16.5, 5), (17.5, 10), (15.5, 12.5), (9, 12.5), (7, 10)]
    heel = [(8.5, 15.5), (15, 15.5), (15.5, 21), (8.5, 21)]
    return [shell(poly(fore, closed=True, r=S.r * 1.3)), shell(poly(heel, closed=True, r=S.r)),
            detail(seg(8, 7.8, 16.5, 7.8)), dot(3.5, 17, 1), dot(20, 15, 1), dot(20.5, 20, 0.9)]


@icon("light-pollution", CAT, "City skyline under a glowing dome of light with a few faded stars.",
      tags=["light pollution", "skyglow", "city lights", "night sky", "astronomy", "dark sky", "urban glow"])
def _(S):
    rr = L(S, 0, 0.8)
    blocks = [rect(2.5, 14.5, 5, 7, rr), rect(7.5, 10, 4.5, 11.5, rr), rect(12, 15.5, 4.5, 6, rr), rect(16.5, 12.5, 5, 9, rr)]
    return [solid(union(*blocks)),
            line(arc(12, 10.5, 8.5, 195, 345)),
            dot(4.5, 3.8, 1), dot(19.5, 3.8, 1)]


@icon("landslide", CAT, "Hillside with a stepped scar near the top and rocks sliding down the slope.",
      tags=["landslide", "slope failure", "rockslide", "hazard", "earth movement", "disaster", "erosion"])
def _(S):
    ground = [(2, 4.5), (7, 4.5), (7.5, 8.5), (22, 17.5), (22, 21.5), (2, 21.5)]
    return [shell(poly(ground, closed=True, r=S.r * 0.6)),
            solid(rock(12, 6.2, 1.6)), solid(rock(16.3, 9.2, 1.9, 30)), solid(rock(20, 11.6, 1.5, 60))]


@icon("mudslide", CAT, "Wavy flow of mud pouring down a slope and burying the lower half of a small house.",
      tags=["mudslide", "mudflow", "debris flow", "landslide", "flood", "hazard", "disaster"])
def _(S):
    mud_top = [(2, 15.5), (5.5, 12.5), (9, 15.5), (13, 12), (17, 10), (22, 9)]
    mud = smooth(mud_top) + "L22 21.5L2 21.5Z"
    hp = house(3, 11, 8, 3, 13)
    return [shell(mud), cut_strokes(S, [poly(hp, r=S.r * 0.6)], P(mud), gap=2.0),
            detail("M7 19H14")]


@icon("rockfall", CAT, "Rocks tumbling off a cliff face past motion lines toward the road below.",
      tags=["rockfall", "falling rocks", "rockslide", "cliff", "hazard", "road danger", "boulders"])
def _(S):
    cliff = [(2, 2.5), (8, 2.5), (8, 7), (10, 10), (8.5, 14), (9.5, 20.5), (2, 20.5)]
    return [shell(poly(cliff, closed=True, r=S.r * 0.5)),
            solid(rock(14.5, 7.5, 2.4)), solid(rock(18.5, 14, 2.6, 40)),
            line(seg(16.5, 3, 17.5, 5)), line(seg(21, 8.5, 21, 10.5)),
            line(seg(12, 20.5, 22, 20.5))]


@icon("avalanche", CAT, "Steep peak with streaks of snow and a billowing cloud rushing down its slope.",
      tags=["avalanche", "snow slide", "snowslide", "mountain hazard", "winter", "backcountry", "disaster"])
def _(S):
    cloud = ("M9.5 21.5H19.5A2.6 2.6 0 0 0 20 16.4A3.6 3.6 0 0 0 13.6 14.4A3.7 3.7 0 0 0 9.5 21.5Z"
             if S.name == "line" else
             "M11 21.5H19A3 3 0 0 0 20 15.8A3.8 3.8 0 0 0 13.6 14A4 4 0 0 0 11 21.5Z")
    return [line(poly([(2, 21), (8, 4), (13, 12)], r=S.r * 0.4)), shell(cloud),
            line(seg(12, 3.5, 15.5, 9.5)), line(seg(16.5, 4.5, 19.5, 10))]


@icon("wildfire", CAT, "Pine tree beside a big flame rising from the forest floor.",
      tags=["wildfire", "forest fire", "bushfire", "blaze", "burning", "disaster", "evacuation"])
def _(S):
    pn = pine(6, 4, 17, 4.2, 2)
    return [shell(poly(pn, closed=True, r=S.r * 0.4)), line(seg(6, 17, 6, 21)),
            shell(flame(15.5, 21, 9, 14)), dot(20.5, 7.5, 1),
            line(seg(2.5, 21.5, 21.5, 21.5))]


@icon("flash-flood", CAT, "Surging water rushing out of a narrow canyon and spreading in waves.",
      tags=["flash flood", "flood", "canyon", "surge", "torrent", "rising water", "hazard"])
def _(S):
    left = [(2, 2.5), (6, 2.5), (9.5, 13), (2, 13)]
    right = [(22, 2.5), (18, 2.5), (14.5, 13), (22, 13)]
    return [shell(poly(left, closed=True, r=S.r * 0.5)), shell(poly(right, closed=True, r=S.r * 0.5)),
            line(wave(2, 22, 17, 1.2, 4)), line(wave(2, 22, 21, 1.2, 4))]


@icon("flooded-house", CAT, "House standing in floodwater with wave lines across its lower walls.",
      tags=["flooded house", "flood", "water damage", "home insurance", "disaster", "rising water", "flood zone"])
def _(S):
    hp = [(4.5, 13), (4.5, 9.5), (12, 3), (19.5, 9.5), (19.5, 13)]
    return [shell(poly(hp, closed=True, r=S.r * 0.6)), mark(rect(10.8, 7.3, 2.4, 2.4)),
            line(wave(2, 22, 17, 1.2, 3)), line(wave(2, 22, 21, 1.2, 3))]


@icon("flood-gauge", CAT, "Tall gauge post with level ticks and water rising around its lower half.",
      tags=["flood gauge", "water level", "staff gauge", "river level", "flood warning", "measurement", "hydrology"])
def _(S):
    return [shell(rect(9, 2.5, 6, 19, min(S.R, 2))),
            detail(seg(9, 6, 13, 6)), detail(seg(9, 9.5, 13, 9.5)),
            line(wave(2, 9, 14.5, 1.0, 1)), line(wave(15, 22, 14.5, 1.0, 1)),
            line(wave(2, 9, 19, 1.0, 1)), line(wave(15, 22, 19, 1.0, 1))]


@icon("drought", CAT, "Dried-out ground broken into cracked plates with a withered sprig above it.",
      tags=["drought", "dry", "parched", "cracked earth", "dead plant", "water shortage", "desert"])
def _(S):
    return [shell(rect(2.5, 13, 19, 8.5, min(S.R, 2.5))),
            detail(poly([(8.5, 13), (10, 16.5), (8, 18.5), (9, 21.5)])),
            detail(poly([(10, 16.5), (15, 17.5), (16, 13)])),
            detail(seg(15, 17.5, 17, 21.5)),
            line("M12 13C12 10 12.5 8 15.5 6.5"), line(seg(12.4, 9.8, 9.5, 8)), line(seg(14, 7.6, 14.6, 4.6))]
@icon("storm-surge", CAT, "Tall leaning wall of sea water rearing over a lower seawall, with spray above.",
      tags=["storm surge", "sea wall", "coastal flood", "hurricane surge", "tidal wave", "flood hazard", "coast"])
def _(S):
    surge = ("M2 21.5V15C2 11 5 8 9 7C12 6.3 15 6.8 16 9.5C14 9 12.5 10.5 12.5 13C12.5 16 14 19 14 21.5Z")
    return [shell(surge), shell(rect(18.5, 13, 3.5, 8.5, L(S, 0, 1))),
            dot(19.5, 8, 1), dot(21, 4.8, 0.9), dot(16, 4.2, 0.9)]


@icon("blizzard", CAT, "Strong wind lines curling past streaks of driven snow.",
      tags=["blizzard", "snowstorm", "whiteout", "winter storm", "wind", "heavy snow", "severe weather"])
def _(S):
    return [line("M2.5 8H11.5A2.5 2.5 0 1 0 9 5.5"), line("M2.5 13.5H14A2.5 2.5 0 1 1 11.5 16"), line("M2.5 19H10"),
            line(seg(17, 4, 15.5, 7)), line(seg(21, 8, 19.5, 11)), line(seg(17.5, 13, 16, 16)),
            line(seg(21.5, 17, 20, 20))]


@icon("ice-storm", CAT, "Ice-coated branch hung with icicles while freezing rain drops fall below.",
      tags=["ice storm", "freezing rain", "icicles", "glaze ice", "winter storm", "frozen branch", "sleet"])
def _(S):
    bar = rect(2.5, 4.5, 19, 4.5, L(S, 1, 2.2))
    ic = [poly([(4.5, 8.5), (8.5, 8.5), (6.5, 14.5)], closed=True), poly([(10, 8.5), (14, 8.5), (12, 16.5)], closed=True),
          poly([(15.5, 8.5), (19.5, 8.5), (17.5, 12.5)], closed=True)]
    body = rot(union(bar, *ic), -4, 12, 10)
    return [shell(body), line(seg(16.5, 4, 19.5, 1.8)), dot(6.5, 18.5, 1.1), dot(14.5, 20.5, 1.1), dot(19.5, 17, 1.1)]


@icon("heat-dome", CAT, "Dome of trapped air over flat ground with a low sun and rays inside.",
      tags=["heat dome", "heatwave", "extreme heat", "trapped heat", "hot weather", "high pressure", "climate"])
def _(S):
    cx, cy = 12, 19.5
    rays = [detail(seg(*polar(cx, cy - 1, 4.8, a), *polar(cx, cy - 1, 6.6, a))) for a in (200, 235, 270, 305, 340)]
    return [shell(f"M2 {cy}A10 10 0 0 1 22 {cy}Z")] + rays + [mark("M9.5 17.5A2.5 2.5 0 0 1 14.5 17.5Z")]


@icon("lightning-strike-tree", CAT, "Bushy tree cracked from crown to trunk with a bolt of lightning striking beside it.",
      tags=["lightning", "tree strike", "split tree", "thunderstorm", "storm damage", "bolt", "hazard"])
def _(S):
    tree = union(circle(5.8, 11, 3.6), circle(9.5, 7.8, 4.2), circle(13, 11.5, 3.6), circle(9.3, 13, 4.3), rect(7.5, 15, 3.5, 6.5))
    bolt = [(20.5, 2), (16.5, 9.5), (19.3, 9.5), (17.5, 16), (21.8, 8), (19, 8)]
    return [shell(tree), detail(poly([(9.8, 4.5), (8, 9.5), (10.8, 13), (8.5, 16.5), (9.3, 21.5)])),
            solid(poly(bolt, closed=True, r=L(S, 0, 0.3)))]


@icon("volcano-hazard-sign", CAT, "Triangular warning sign showing an erupting volcano.",
      tags=["volcano", "eruption", "warning sign", "hazard sign", "volcanic", "danger", "lava"])
def _(S):
    tri = [(12, 3), (21.5, 20.5), (2.5, 20.5)]
    return [shell(poly(tri, closed=True, r=S.r * 1.3)),
            mark(poly([(8.3, 18.3), (10.6, 14), (13.4, 14), (15.7, 18.3)], closed=True)),
            dot(11, 11.4, 0.9), dot(13.3, 10.8, 0.9), dot(12.1, 8.6, 0.8)]


@icon("tsunami-hazard-sign", CAT, "Diamond warning sign with a rolling wave above a small standing figure.",
      tags=["tsunami", "tidal wave", "warning sign", "hazard sign", "coast", "evacuate", "wave"])
def _(S):
    dia = [(12, 2), (22, 12), (12, 22), (2, 12)]
    return [shell(poly(dia, closed=True, r=S.r * 1.3)),
            detail(wave(6.5, 17.5, 10.2, 1.4, 2)),
            dot(12, 14.6, 1.1), detail(seg(12, 16, 12, 18))]


@icon("earthquake-safe-zone", CAT, "Square sign with a person sheltering beneath a sturdy table.",
      tags=["earthquake", "drop cover hold", "shelter", "safe zone", "table", "duck and cover", "safety"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, min(S.R, 3))),
            detail(seg(6.5, 8.5, 17.5, 8.5)), detail(seg(7.5, 8.5, 7.5, 17.5)), detail(seg(16.5, 8.5, 16.5, 17.5)),
            dot(12, 12.8, 1.4), detail("M12 14.8V17.8")]


@icon("evacuation-route", CAT, "Square sign with a running figure beside an arrow curving uphill.",
      tags=["evacuation", "escape route", "run", "emergency exit", "flee", "safety sign", "uphill"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, min(S.R, 3))),
            dot(8.3, 7.5, 1.3), detail("M8.8 10L10.8 13.5"), detail("M10.8 13.5L8 17"), detail("M10.8 13.5L13 16.5"),
            detail("M14 17C17.5 16 18 12.5 17.5 8.8"), detail("M15.3 10.6L17.5 8.4L19.4 10.6")]


@icon("emergency-go-bag", CAT, "Backpack marked with a first aid cross and a flashlight strapped to its side.",
      tags=["go bag", "emergency kit", "bug out bag", "first aid", "disaster preparedness", "survival", "backpack"])
def _(S):
    pack = rect(3, 7, 12, 14.5, min(S.R, 3))
    torch = [(17, 7), (22, 7), (21, 10.5), (21, 19), (18, 19), (18, 10.5)]
    return [shell(pack), line("M6.5 7V5.5A2.5 2.5 0 0 1 9 3H9A2.5 2.5 0 0 1 11.5 5.5V7"),
            detail(seg(9, 10.8, 9, 17.2)), detail(seg(5.8, 14, 12.2, 14)),
            shell(poly(torch, closed=True, r=S.r * 0.4))]


@icon("sandbags", CAT, "Stack of plump sandbags laid in an overlapping wall pattern.",
      tags=["sandbags", "flood defence", "flood barrier", "sand bag wall", "emergency", "levee repair", "flood protection"])
def _(S):
    rx = L(S, 2.2, 3.2)
    wall = union(rect(2.5, 14, 9.5, 7.5, rx), rect(12, 14, 9.5, 7.5, rx), rect(7, 6.5, 10, 7.5, rx))
    return [shell(wall), detail(seg(12, 14, 12, 21.5)), detail(seg(7.5, 14, 16.5, 14))]


@icon("levee", CAT, "Raised earth embankment with river waves lapping one side and dry land on the other.",
      tags=["levee", "dike", "embankment", "flood defence", "river bank", "dyke", "flood wall"])
def _(S):
    bank = [(10.5, 21.5), (13, 10.5), (18, 10.5), (20.5, 21.5)]
    return [shell(poly(bank, closed=True, r=S.r * 0.5)),
            line(wave(2, 8.5, 12.5, 1.1, 1)), line(wave(2, 8, 17, 1.1, 1)), line(wave(2, 7.5, 21.5, 1.1, 1))]


@icon("storm-shelter", CAT, "Slanted cellar doors set into a grassy mound beneath a dark storm cloud.",
      tags=["storm shelter", "storm cellar", "tornado shelter", "bunker", "cellar doors", "safe room", "tornado"])
def _(S):
    doors = [(3, 21.5), (5.5, 15.5), (18.5, 15.5), (21, 21.5)]
    return [line(cloud(S, 0.7, 0, -5.4)),
            shell(poly(doors, closed=True, r=S.r * 0.5)), detail(seg(12, 15.5, 12, 21.5)),
            mark(rect(8.8, 17.6, 1.4, 2.2)), mark(rect(13.8, 17.6, 1.4, 2.2))]


@icon("liquefaction", CAT, "Building tilting as it sinks into rippling, waterlogged ground.",
      tags=["liquefaction", "soil liquefaction", "sinking building", "earthquake damage", "quicksand", "tilted building", "ground failure"])
def _(S):
    cx, cy = 12, 15
    bld = poly(rpts([(8, 15), (8, 3.5), (16, 3.5), (16, 15)], 8, cx, cy), r=S.r * 0.4)
    return [line(bld), line(wave(2, 22, 16.5, 1.2, 4)), line(wave(2, 22, 21, 1.2, 4)), dot(4, 10, 1), dot(20.5, 11.5, 1)]


@icon("ground-subsidence", CAT, "Flat ground sagging into a shallow dip with a downward arrow above it.",
      tags=["subsidence", "sinkhole", "ground sinking", "land settling", "sagging ground", "geology hazard", "collapse"])
def _(S):
    top = [(2, 11), (6.5, 11), (9.5, 14), (12, 15.5), (14.5, 14), (17.5, 11), (22, 11)]
    ground = smooth(top) + "L22 21.5L2 21.5Z"
    return [shell(ground), line(seg(12, 2.5, 12, 8.5)), line(poly([(9.5, 6.3), (12, 8.8), (14.5, 6.3)], r=S.r * 0.6))]


@icon("cyclone-eye", CAT, "Top view of a storm with three spiral arms curling around a small clear eye.",
      tags=["cyclone", "hurricane", "typhoon", "eye of the storm", "tropical storm", "satellite view", "spiral storm"])
def _(S):
    arms = [line(smooth(spiral_pts(12, 12, 5.2, 10, a, -120, 10))) for a in (-90, 30, 150)]
    return arms + [shell(circle(12, 12, 1.4))]


@icon("smog", CAT, "City skyline rising out of thick horizontal bands of haze.",
      tags=["smog", "air pollution", "haze", "polluted city", "fog", "poor air quality", "urban smog"])
def _(S):
    rr = L(S, 0, 0.8)
    blocks = [rect(2.5, 7, 5, 6, rr), rect(7.5, 3, 4.5, 10, rr), rect(12, 8.5, 4.5, 4.5, rr), rect(16.5, 5, 5, 8, rr)]
    return [solid(union(*blocks)), line(seg(2.5, 16, 21.5, 16)), line(seg(5.5, 19, 21.5, 19)),
            line(seg(2.5, 22, 17.5, 22))]


@icon("acid-rain", CAT, "Rain falling from a cloud beside a bare tree with drooping branches.",
      tags=["acid rain", "pollution", "dying tree", "dead tree", "environment", "rain damage", "acidification"])
def _(S):
    return [line(cloud(S, 0.75, -2.6, -4.6)),
            line(seg(6, 15.2, 5, 17.6)), line(seg(9.5, 15.2, 8.5, 17.6)), line(seg(13, 15.2, 12, 17.6)),
            line(seg(7.5, 19.4, 6.5, 21.8)), line(seg(11, 19.4, 10, 21.8)),
            line("M19 21.5V9.5"), line("M19 13.5L22 16.2"), line("M19 17.5L15.8 20"), line("M19 11.5L16.5 9")]


@icon("sea-level-rise", CAT, "Small house on the shore with waves and an upward arrow showing the water climbing.",
      tags=["sea level rise", "climate change", "rising seas", "coastal flooding", "global warming", "tide", "shoreline"])
def _(S):
    hp = [(13.5, 17), (13.5, 11.5), (17.25, 7.5), (21, 11.5), (21, 17)]
    return [shell(poly(hp, closed=True, r=S.r * 0.5)),
            line(wave(2, 11, 17.5, 1.0, 2)), line(wave(2, 22, 21.5, 1.0, 4)),
            line(seg(5.5, 13, 5.5, 3.5)), line(poly([(3, 6), (5.5, 3.5), (8, 6)], r=S.r * 0.6))]


def dashed(pts, on=3.0, off=2.6):
    """Dash segments (d-strings) along a polyline."""
    out = []
    pos, draw = 0.0, True
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        ln = math.hypot(x1 - x0, y1 - y0)
        t = 0.0
        while t < ln - 1e-6:
            step = min((on if draw else off) - pos, ln - t)
            if draw:
                a, b = t / ln, (t + step) / ln
                out.append(seg(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a, x0 + (x1 - x0) * b, y0 + (y1 - y0) * b))
            t += step
            pos += step
            if pos >= (on if draw else off) - 1e-6:
                draw, pos = not draw, 0.0
    return out


@icon("glacier-retreat", CAT, "Tapering glacier tongue with a dashed outline showing how far it used to reach.",
      tags=["glacier retreat", "melting glacier", "shrinking ice", "climate change", "ice loss", "glacier", "global warming"])
def _(S):
    body = [(2, 3), (6, 3), (11, 8), (11, 16), (6, 21), (2, 21)]
    ghost = [(12.5, 3), (15, 3), (21, 9), (21, 15), (15, 21), (12.5, 21)]
    return [shell(poly(body, closed=True, r=S.r * 0.5)), detail(seg(2.5, 10, 7, 10)), detail(seg(2.5, 14.5, 7.5, 14.5))] + \
        [line(d) for d in dashed(ghost)]


@icon("coral-bleaching", CAT, "Hollow branching coral drawn in outline beside a thermometer.",
      tags=["coral bleaching", "dying coral", "reef", "ocean warming", "climate change", "heat stress", "thermometer"])
def _(S):
    coral = union(tube("M7.5 21V12", 3.4), tube("M7.5 14L3.8 8.5", 3), tube("M7.5 12L11.5 7", 3), tube("M7.5 15.5L11.8 12.8", 2.8))
    therm = union(rect(17.6, 3, 3.6, 11.5, 1.8), circle(19.4, 17, 3.2))
    return [shell(coral), shell(therm), detail("M19.4 17V9")]


# ============================================================================ fungi

def dome(S, cx, yb, hw, h, rc=1.6):
    """Mushroom cap: dome of half-width hw and height h resting on y=yb (sharp base corners in Line, rounded in Rounded)."""
    t = yb - h
    k = 0.0 if S.name == "line" else rc
    y0 = yb - k
    d = (f"M{fmt(cx - hw)} {fmt(y0)}C{fmt(cx - hw)} {fmt(yb - h * 0.72)} {fmt(cx - hw * 0.55)} {fmt(t)} {fmt(cx)} {fmt(t)}"
         f"C{fmt(cx + hw * 0.55)} {fmt(t)} {fmt(cx + hw)} {fmt(yb - h * 0.72)} {fmt(cx + hw)} {fmt(y0)}")
    if k:
        d += f"Q{fmt(cx + hw)} {fmt(yb)} {fmt(cx + hw - k)} {fmt(yb)}H{fmt(cx - hw + k)}Q{fmt(cx - hw)} {fmt(yb)} {fmt(cx - hw)} {fmt(y0)}"
    return d + "Z"


def stem_rect(S, cx, y0, w, h, cap=2.0):
    return rect(cx - w / 2, y0, w, h, min(S.R, cap))


def rosette(cx, cy, r, n, rot0=-90):
    """Scalloped round outline: n outward arcs between points on a circle of radius r."""
    pts = [polar(cx, cy, r, rot0 + i * 360 / n) for i in range(n)]
    chord = 2 * r * math.sin(math.pi / n)
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(1, n + 1):
        p = pts[i % n]
        d += f"A{fmt(chord * 0.62)} {fmt(chord * 0.62)} 0 0 1 {fmt(p[0])} {fmt(p[1])}"
    return d + "Z"


@icon("fly-agaric", CAT, "Red toadstool with white spots on its dome cap and a ring on the stem.",
      tags=["fly agaric", "toadstool", "amanita", "poisonous mushroom", "spotted mushroom", "fungus", "forest"])
def _(S):
    return [shell(dome(S, 12, 12.5, 9.5, 9.5)), shell(stem_rect(S, 12, 12.5, 5, 9)),
            detail(seg(9.5, 16.5, 14.5, 16.5)),
            dot(7.6, 8.8, 1.2), dot(12, 6.6, 1.1), dot(16.4, 9, 1.2), dot(11.6, 10.4, 0.8)]


@icon("porcini", CAT, "Porcini mushroom with a thick rounded cap over a fat bulging stem.",
      tags=["porcini", "cep", "king bolete", "penny bun", "edible mushroom", "forest mushroom", "foraging"])
def _(S):
    cap = dome(S, 12, 10, 9, 6.5)
    stem = ("M9 10C8 13.5 6.5 16 7 19.3C7.3 21 9 21.5 12 21.5C15 21.5 16.7 21 17 19.3C17.5 16 16 13.5 15 10Z")
    return [shell(union(cap, stem)), detail(seg(9.3, 10, 14.7, 10))]


@icon("enoki", CAT, "Bundle of long thin pale stems each topped with a tiny round cap.",
      tags=["enoki", "enokitake", "needle mushroom", "golden needle", "edible mushroom", "asian cooking", "hot pot"])
def _(S):
    stems = ["M6 7.5C6 14 9.5 16 10.5 21.5", "M10 6C10 13 11 16 11.5 21.5", "M14 6.8C14 13 13 16 12.5 21.5",
             "M18 8.5C18 14 14.5 16 13.5 21.5"]
    return [line(d) for d in stems] + [solid(circle(6, 5.8, 1.9)), solid(circle(10, 4.2, 1.9)),
                                       solid(circle(14, 5, 1.9)), solid(circle(18, 6.8, 1.9))]


@icon("bracket-fungus", CAT, "Two half-round shelf fungi with growth rings, stacked on a tree trunk.",
      tags=["bracket fungus", "shelf fungus", "polypore", "tree fungus", "turkey tail", "rotting wood", "forest"])
def _(S):
    return [shell(rect(2.5, 2.5, 6, 19, L(S, 0, 2.5))),
            shell("M8.5 5H21.5A6.5 5.5 0 0 1 8.5 5Z"), detail("M12 5A3 2.4 0 0 0 18 5"),
            shell("M8.5 14H19.5A5.5 4.5 0 0 1 8.5 14Z")]


@icon("shaggy-ink-cap", CAT, "Tall bell-shaped shaggy cap with a ragged lower fringe on a slender stem.",
      tags=["shaggy ink cap", "lawyer's wig", "inky cap", "coprinus", "edible mushroom", "lawn mushroom", "fungus"])
def _(S):
    cap = ("M7 14V9C7 5.5 9 3 12 3C15 3 17 5.5 17 9V14L15.3 16.8L13.7 14.3L12 17L10.3 14.3L8.7 16.8Z")
    return [shell(cap), detail(seg(9.3, 7, 11, 7)), detail(seg(13, 10.3, 14.7, 10.3)),
            line(seg(12, 17.5, 12, 21.5))]


@icon("parasol-mushroom", CAT, "Wide flat-topped scaly cap on a tall thin stem with a loose ring.",
      tags=["parasol mushroom", "macrolepiota", "edible mushroom", "umbrella mushroom", "field mushroom", "fungus", "foraging"])
def _(S):
    cap = dome(S, 12, 11, 10, 6.5)
    return [shell(cap), dot(12, 7.5, 1.1), dot(7, 9, 0.9), dot(17, 9, 0.9),
            line(seg(12, 11, 12, 21.5)), line(seg(9.5, 15.5, 14.5, 15.5))]


def mini_mushroom(x, y, r):
    """Tiny solid mushroom standing on y (d-string): semicircle cap with a short stem."""
    cap = f"M{fmt(x - r)} {fmt(y - r * 0.8)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x + r)} {fmt(y - r * 0.8)}Z"
    return union(cap, rect(x - r * 0.35, y - r * 0.8, r * 0.7, r * 0.8 + 0.2))


@icon("fairy-ring", CAT, "Ring of small mushrooms growing in a circle on the grass.",
      tags=["fairy ring", "mushroom circle", "toadstool ring", "fungus", "folklore", "meadow", "magic circle"])
def _(S):
    ms = []
    n = 8
    for k in range(n):
        a = -90 + k * 360 / n
        px, py = polar(12, 11.5, 1, a)
        x = 12 + (px - 12) * 8.5
        y = 11.5 + (py - 11.5) * 4.6
        r = 1.5 + 0.5 * ((y - 6.9) / 9.2)
        ms.append(mini_mushroom(x, y + 1.5, r * 1.15))
    return [solid(union(*ms)), line(wave(2, 22, 21, 0.9, 4))]


@icon("mycelium", CAT, "Small mushroom above the soil with fine branching threads spreading beneath.",
      tags=["mycelium", "fungal network", "hyphae", "mushroom roots", "soil", "underground", "fungus"])
def _(S):
    return [shell(dome(S, 12, 7.5, 6, 4.5)), line(seg(12, 7.5, 12, 11.5)),
            line(wave(2, 10, 12.5, 0.7, 2)), line(wave(14, 22, 12.5, 0.7, 2)),
            line("M12 12.5V16L7.5 19L3.5 19.5"), line("M12 16L16.5 19L20.5 19.5"), line(seg(7.5, 19, 8, 22)),
            line(seg(16.5, 19, 16, 22))]


@icon("spore-print", CAT, "Paper card carrying a radiating spore print, with a mushroom cap resting beside it.",
      tags=["spore print", "mushroom identification", "gills", "paper print", "mycology", "fungus", "spore colour"])
def _(S):
    c = (8.5, 8.5)
    return [shell(rect(2.5, 2.5, 12, 12, min(S.R, 2))),
            detail(seg(*polar(*c, 3.4, 0), *polar(*c, 3.4, 180))), detail(seg(*polar(*c, 3.4, 60), *polar(*c, 3.4, 240))),
            detail(seg(*polar(*c, 3.4, 120), *polar(*c, 3.4, 300))),
            shell(dome(S, 18, 21.5, 4.3, 4.3)), ]


@icon("mushroom-gills", CAT, "Underside of a mushroom cap with gills radiating out from the stem.",
      tags=["mushroom gills", "lamellae", "underside", "cap underside", "mycology", "fungus", "radial lines"])
def _(S):
    g = [detail(seg(*polar(12, 12, 4.4, a), *polar(12, 12, 7.3, a))) for a in range(0, 360, 45)]
    return [shell(circle(12, 12, 9.5)), shell(circle(12, 12, 1.6))] + g


@icon("truffle", CAT, "Lumpy warty truffle cut open to show its marbled interior veins.",
      tags=["truffle", "black truffle", "tuber", "gourmet mushroom", "fungus", "foraging", "delicacy"])
def _(S):
    polar_pts = [(-95, 9.6), (-58, 8.0), (-28, 9.9), (8, 8.3), (36, 9.6), (68, 8.1), (100, 9.8), (138, 8.2), (172, 9.7), (208, 8.3), (243, 9.6)]
    pts = [polar(12, 12, r, a) for a, r in polar_pts]
    return [shell(smooth(pts, closed=True)), detail("M7 11C9 8.5 11 12 13.5 10C15.5 8.5 16.5 10 17.5 9.3"),
            detail("M6.8 15.5C9 13.8 11 17 13.3 15C15 13.6 16.5 14.6 17.3 14")]


@icon("coral-fungus", CAT, "Upright branching fungus with many blunt clubbed tips, like a small coral.",
      tags=["coral fungus", "clavaria", "club fungus", "branching mushroom", "fungus", "forest floor", "ramaria"])
def _(S):
    br = ["M12 21.5V14", "M12 14L7.5 9.5L4.2 6", "M7.5 9.5L8.6 5", "M12 14V5", "M12 14L16.5 9.5L19.8 6", "M16.5 9.5L15.4 5"]
    tips = [(4.2, 5.2), (8.6, 4.2), (12, 4.2), (15.4, 4.2), (19.8, 5.2)]
    return [line(d) for d in br] + [dot(x, y, 1.4) for x, y in tips]


@icon("earthstar-fungus", CAT, "Star of pointed rays splayed open around a round central spore sac.",
      tags=["earthstar", "geastrum", "star fungus", "puffball", "spore sac", "fungus", "forest floor"])
def _(S):
    star = [polar(12, 12, 10.3 if k % 2 == 0 else 6.6, -90 + k * 360 / 14) for k in range(14)]
    return [shell(poly(star, closed=True, r=L(S, 0, 0.8)), stroke_miterlimit="2"), detail(circle(12, 12, 3.1)), dot(12, 12, 0.7)]


@icon("lichen", CAT, "Boulder with a scalloped leafy lichen patch, a round crust and scattered specks.",
      tags=["lichen", "crustose lichen", "foliose lichen", "rock growth", "symbiosis", "moss", "nature"])
def _(S):
    rock = ("M2.5 21.5V14.5C2.5 9 7 5 12 5C17 5 21.5 9 21.5 14.5V21.5Z" if S.name == "line" else
            "M2.5 19V14.5C2.5 9 7 5 12 5C17 5 21.5 9 21.5 14.5V19Q21.5 21.5 19 21.5H5Q2.5 21.5 2.5 19Z")
    return [shell(rock), detail(rosette(9.5, 13.5, 3.4, 6)), dot(17, 10.5, 1.2), dot(15.5, 17, 1.1), dot(19, 15.3, 0.9), dot(11.5, 18.7, 0.9)]


@icon("mold-spores", CAT, "Fuzzy round mould colony with spore heads rising on thin stalks.",
      tags=["mold", "mould", "spores", "fungus", "mildew", "colony", "contamination", "penicillium"])
def _(S):
    stalks = []
    for a in (-140, -115, -90, -65, -40):
        stalks.append(line(seg(*polar(12, 15, 5.4, a), *polar(12, 15, 8.4, a))))
        stalks.append(dot(*polar(12, 15, 10, a), 1.3))
    return [shell(circle(12, 15, 4.4)), dot(10.7, 14.3, 0.8), dot(13.3, 16, 0.8)] + stalks


@icon("yeast-cells", CAT, "Cluster of oval yeast cells, each with a small bud attached.",
      tags=["yeast", "budding yeast", "cells", "microscope", "fermentation", "microbiology", "fungus"])
def _(S):
    k = L(S, 1.0, 0.92)
    a = union(ellipse(7.5, 7, 4 * k, 3 * k), circle(12.6, 5.8, L(S, 1.6, 2.0)))
    b = union(ellipse(16.8, 14.8, 3.5 * k, 4 * k), circle(19.6, 9.2, L(S, 1.5, 1.9)))
    c = union(ellipse(7.5, 17.8, 3.6 * k, 3.1 * k), circle(3.2, 14.6, L(S, 1.4, 1.8)))
    return [shell(a), shell(b), shell(c)]


@icon("mushroom-cluster", CAT, "Three mushrooms of different sizes growing together from one patch of ground.",
      tags=["mushroom cluster", "mushroom group", "fungi", "toadstools", "forest floor", "foraging", "wild mushrooms"])
def _(S):
    return [shell(dome(S, 12, 10, 5.5, 6.5)), shell(stem_rect(S, 12, 10, 4, 11.5)),
            shell(dome(S, 4.8, 17, 3, 3.8, 1.2)), line(seg(4.8, 17, 4.8, 21.5)),
            shell(dome(S, 19.2, 16.5, 3, 3.6, 1.2)), line(seg(19.2, 16.5, 19.2, 21.5)),
            line(seg(2, 21.5, 22, 21.5))]


@icon("toadstool-house", CAT, "Fairy-tale toadstool home with a round-topped door and a round window in its stem.",
      tags=["toadstool house", "fairy house", "gnome home", "mushroom house", "fantasy", "storybook", "woodland"])
def _(S):
    return [shell(dome(S, 12, 11, 9.5, 8)), shell(stem_rect(S, 12, 11, 9, 10.5)),
            mark("M10.3 21.5V18.2A1.7 1.7 0 0 1 13.7 18.2V21.5Z"), mark(circle(12, 14.3, 1.3)),
            dot(7.5, 7.8, 1), dot(14.5, 6.3, 1), dot(17.4, 9, 0.9)]


@icon("mushroom-log", CAT, "Fallen log with a row of small mushrooms growing along its top.",
      tags=["mushroom log", "fallen log", "rotting wood", "shiitake log", "fungi", "forest", "decay"])
def _(S):
    def mini(x, r):
        return solid(f"M{fmt(x - r)} 10.5A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x + r)} 10.5Z")
    body = union(rect(7, 13.5, 14.5, 8, L(S, 0.5, 3)), ellipse(6.5, 17.5, 3.6, 4))
    return [shell(body), dot(6.5, 17.5, 1.1), detail(seg(12, 17.5, 18, 17.5)),
            mini(9, 2.3), mini(14, 3.0), mini(19, 2.4),
            line(seg(9, 10.5, 9, 12.5)), line(seg(14, 10.5, 14, 12.5)), line(seg(19, 10.5, 19, 12.5))]


@icon("death-cap", CAT, "Smooth domed pale cap on a stem with a ring and a cup-shaped sac at its base.",
      tags=["death cap", "amanita phalloides", "poisonous mushroom", "deadly fungus", "toxic", "volva", "mushroom warning"])
def _(S):
    cap = dome(S, 12, 10.5, 8.5, 7.5)
    body = union(cap, rect(10, 10.5, 4, 8.5), "M7 18.3H17C17 20.6 15 21.5 12 21.5C9 21.5 7 20.6 7 18.3Z")
    return [shell(body), detail(seg(10, 13.8, 14, 13.8)), detail(seg(8.6, 18.4, 15.4, 18.4))]


@icon("jelly-fungus", CAT, "Wobbly translucent ear-shaped fungus growing on a bare branch.",
      tags=["jelly fungus", "wood ear", "jelly ear", "tremella", "gelatinous fungus", "edible fungus", "branch"])
def _(S):
    ear = [(6, 14), (4.6, 9.5), (8, 5.3), (13, 4.2), (18, 6), (19.3, 10.5), (16.7, 14.2), (12.3, 13.3), (9.3, 15)]
    return [shell(smooth(ear, closed=True)), detail("M9.3 11.5C8.8 8.8 11.2 7 14.3 7.8C15.3 8.1 15.6 9 15.2 9.8"),
            line(seg(2.5, 20.5, 21.5, 17.5))]


@icon("cordyceps", CAT, "Curled segmented caterpillar with thin club-tipped fungal stalks sprouting from its back.",
      tags=["cordyceps", "zombie fungus", "caterpillar fungus", "parasitic fungus", "entomopathogenic", "yarsagumba", "insect"])
def _(S):
    body = P(tube("M3.8 17.2C4.5 20.8 10.5 21.6 14.2 20C18 18.4 20.4 15.5 18.6 13.4", L(S, 3.6, 4.0)))
    cuts = U(*[P(rect(x, 15, 0.9, 8)) for x in (7.6, 11.4, 15.2)])
    return [solid(path_to_d(D(body, cuts))),
            line(seg(7, 18.5, 5.4, 8.6)), line(seg(11.2, 19.5, 11.4, 5.6)), line(seg(15.6, 18.2, 17.4, 8.8)),
            solid(ellipse(5.2, 7.2, L(S, 1.3, 1.5), 2.2)), solid(ellipse(11.4, 4.6, L(S, 1.3, 1.5), 2.2)),
            solid(ellipse(17.6, 7.4, L(S, 1.3, 1.5), 2.2))]


@icon("slime-mold", CAT, "Blob with a branching network of vein-like strands spreading out from it.",
      tags=["slime mold", "slime mould", "physarum", "network", "protist", "amoeba", "organism"])
def _(S):
    blob = smooth([(4.5, 16), (6.5, 13), (10, 13.5), (11.5, 17), (9.5, 20.5), (5.5, 20.3)], closed=True)
    return [shell(blob), line("M10.5 14.5L14 11L18 10"), line("M14 11L15.5 6.5"), line("M18 10L21 6.5"),
            line("M18 10L21.5 12.5"), line("M7 12.5V7.5L10 4"), line("M7 7.5L3.5 5"),
            dot(15.5, 5.3, 1.2), dot(21.3, 5.6, 1.1), dot(10.8, 2.9, 1.1), dot(2.8, 4.2, 1.1)]


# ============================================================================ maps, trails, cycles, ice and trees

def head(S, tip, deg, size=3.0, spread=42):
    """Open arrowhead at tip; deg is the direction the arrow travels (0 = right, 90 = down)."""
    a = polar(*tip, size, deg + 180 - spread)
    b = polar(*tip, size, deg + 180 + spread)
    return poly([a, tip, b], r=S.r * 0.6)


def bone(x0, x1, y, k=1.5, w=2.4):
    """Horizontal bone silhouette from x0 to x1 centred on y (two knobs at each end)."""
    parts = [rect(x0 + k, y - w / 2, x1 - x0 - 2 * k, w)]
    for x in (x0 + k, x1 - k):
        parts += [circle(x, y - k * 0.9, k), circle(x, y + k * 0.9, k)]
    return union(*parts)


@icon("topographic-map", CAT, "Folded map sheet carrying nested wavy contour lines around a summit.",
      tags=["topographic map", "contour map", "terrain map", "hiking map", "elevation lines", "cartography", "trail map"])
def _(S):
    sheet = [(2.5, 5.5), (8.5, 3.5), (15.5, 6), (21.5, 4), (21.5, 18.5), (15.5, 20.5), (8.5, 18), (2.5, 20)]
    ring = smooth([(12, 6.6), (16.3, 8.3), (17.4, 12.3), (14.8, 15.6), (10.5, 16), (7.3, 13), (8, 9)], closed=True)
    return [shell(poly(sheet, closed=True, r=S.r * 0.4)), detail(ring), dot(12.3, 11.4, 1.3)]


@icon("elevation-profile", CAT, "Jagged mountain elevation profile drawn as a filled area above a baseline.",
      tags=["elevation profile", "altitude chart", "hiking profile", "terrain profile", "climb chart", "mountain stage", "gradient"])
def _(S):
    pts = [(2.5, 20), (2.5, 14.5), (6.5, 9.5), (10, 13.5), (14, 4.5), (17.5, 11), (21.5, 8), (21.5, 20)]
    return [shell(poly(pts, closed=True, r=S.r * 0.5)), detail(seg(9.5, 20, 9.5, 17)), detail(seg(16, 20, 16, 14.5)),
            detail(seg(5.3, 20, 5.3, 16.5))]


@icon("trig-point", CAT, "Short tapered concrete survey pillar with a flat plate and marker on top.",
      tags=["trig point", "triangulation pillar", "survey marker", "benchmark", "summit marker", "ordnance survey", "geodetic"])
def _(S):
    body = union(poly([(8, 21), (9, 10), (15, 10), (16, 21)], closed=True), rect(6.5, 6.3, 11, 3.7))
    return [shell(body), detail(seg(9.3, 10, 14.7, 10)), dot(12, 15.3, 1.1), solid(poly([(10.3, 6), (12, 2.8), (13.7, 6)], closed=True)),
            line(seg(2.5, 21.5, 21.5, 21.5))]


@icon("altimeter", CAT, "Round altitude gauge with a pointer needle and a small mountain on its dial.",
      tags=["altimeter", "altitude gauge", "elevation meter", "height gauge", "mountaineering", "barometric", "aviation"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(seg(12, 10.5, 16, 6.3)), dot(12, 10.5, 1.4),
            detail(poly([(7.6, 17.3), (10.6, 13.6), (12.6, 15.8), (14.2, 14.4), (16.4, 17.3)], r=S.r * 0.3))]


@icon("trail-blaze", CAT, "Tree trunk flaring at its base with a painted rectangular trail marker and bark lines.",
      tags=["trail blaze", "trail marker", "paint blaze", "waymark", "hiking trail", "tree mark", "wayfinding"])
def _(S):
    trunk = [(7, 2.5), (17, 2.5), (17, 17), (19.5, 21.5), (4.5, 21.5), (7, 17)]
    return [shell(poly(trunk, closed=True, r=S.r * 0.5)), mark(rect(10, 5.5, 4, 7.5, L(S, 0, 0.8))),
            detail(seg(9.3, 15.5, 9.3, 19)), detail(seg(14.7, 15.5, 14.7, 19)),
            line(seg(17, 8, 20.5, 5)), line(seg(7, 10, 3.5, 7.2))]


@icon("hiking-trail", CAT, "Winding footpath climbing a rounded hill to a flag on the summit.",
      tags=["hiking trail", "footpath", "trek", "summit path", "mountain walk", "trailhead", "outdoors"])
def _(S):
    hill = "M2.5 21.5C2.5 14 7 9 12.5 9C17 9 20.5 14 21.5 21.5Z"
    path = [(7.5, 19.8), (16, 17.6), (9.8, 14.8), (14.8, 12.6), (12.5, 10.6)]
    return [shell(hill), detail(smooth(path)),
            line(seg(12.5, 9, 12.5, 2.5)), solid(poly([(12.5, 2.5), (18.5, 4.4), (12.5, 6.3)], closed=True))]


@icon("switchback-trail", CAT, "Steep peak with a zigzag path doubling back and forth up its face.",
      tags=["switchback", "zigzag trail", "steep path", "mountain trail", "climbing path", "hairpin", "ascent"])
def _(S):
    peak = [(2, 21.5), (13, 3), (22, 21.5)]
    return [shell(poly(peak, closed=True, r=S.r * 0.5)),
            detail(poly([(16, 19), (9.5, 15.8), (15, 12.8), (11.6, 9.8)], r=S.r * 0.4))]


@icon("scenic-viewpoint", CAT, "Coin-operated viewing scope on a post looking out toward a distant mountain.",
      tags=["scenic viewpoint", "viewing scope", "telescope", "lookout", "sightseeing", "overlook", "tower viewer"])
def _(S):
    scope = [(2.5, 7.3), (2.5, 10.7), (14, 12.7), (14, 5.3)]
    return [shell(poly(scope, closed=True, r=S.r * 0.6)), line(seg(8, 10.5, 8, 21.5)), line(seg(3.5, 21.5, 12.5, 21.5)),
            line(poly([(14.5, 21.5), (18, 15.5), (20.3, 18.8), (22, 21.5)], r=S.r * 0.4))]


@icon("watershed", CAT, "Ridge line with rain falling on the crest and water flowing away down both slopes.",
      tags=["watershed", "drainage divide", "catchment", "ridge", "water flow", "hydrology", "basin"])
def _(S):
    return [line(poly([(2, 17), (12, 8), (22, 17)], r=S.r * 0.4)),
            dot(12, 2.8, 1.1),
            line(seg(6.6, 6, 3.6, 9.4)), line(poly([(3.4, 6.6), (3.4, 9.6), (6.4, 9.6)], r=S.r * 0.5)),
            line(seg(17.4, 6, 20.4, 9.4)), line(poly([(20.6, 6.6), (20.6, 9.6), (17.6, 9.6)], r=S.r * 0.5)),
            line(wave(2, 22, 21, 1.0, 4))]


def solid_cloud(cx, cy, s=1.0):
    """Small solid cloud mark centred on (cx, cy), about 8 px wide at s = 1."""
    return union(circle(cx - 2.6 * s, cy + 0.6 * s, 1.9 * s), circle(cx - 0.2 * s, cy - 0.7 * s, 2.5 * s),
                 circle(cx + 2.7 * s, cy + 0.7 * s, 1.8 * s), rect(cx - 4.5 * s, cy + 0.6 * s, 9 * s, 1.9 * s, 0.9 * s))


def cycle_arcs(S, n=3, r=8.6, sweep=76, start=-100):
    out = []
    for k in range(n):
        a0 = start + k * 360 / n
        out.append(line(arc(12, 12, r, a0, a0 + sweep)))
        out.append(line(head_at(S, 12, 12, r, a0 + sweep)))
    return out


def head_at(S, cx, cy, r, a, size=2.8):
    """Arrowhead at angle a on a circle, pointing clockwise along the tangent."""
    tip = polar(cx, cy, r, a)
    return head(S, tip, a + 90, size, 42)


@icon("water-cycle", CAT, "Three circular arrows around a small cloud, raindrops and lake waves.",
      tags=["water cycle", "hydrologic cycle", "evaporation", "precipitation", "condensation", "rain cycle", "earth science"])
def _(S):
    return cycle_arcs(S) + [solid(solid_cloud(12, 9.2, 0.95)), dot(9.6, 13.6, 0.85), dot(13.6, 13.8, 0.85),
                            dot(11.6, 15.6, 0.8)]


@icon("carbon-cycle", CAT, "Three circular arrows around a tree, a cloud and a factory chimney.",
      tags=["carbon cycle", "co2 cycle", "photosynthesis", "emissions", "carbon dioxide", "ecology", "earth science"])
def _(S):
    return cycle_arcs(S) + [solid(circle(9.3, 10.3, 2.4)), solid(rect(8.6, 12, 1.4, 3.8)),
                            solid(rect(13.2, 11.2, 3, 4.6)), solid(rect(14.2, 8.8, 1, 2.5)), dot(15.9, 7.4, 0.8)]


@icon("latitude-lines", CAT, "Globe crossed by evenly spaced horizontal parallels of latitude.",
      tags=["latitude", "parallels", "globe lines", "geography", "equator", "coordinates", "map grid"])
def _(S):
    def chord(y):
        w = math.sqrt(9.5 ** 2 - (y - 12) ** 2) - L(S, 0, 2.6)
        return detail(seg(12 - w, y, 12 + w, y))
    return [shell(circle(12, 12, 9.5)), chord(7.5), chord(12), chord(16.5)]


@icon("arctic-circle", CAT, "Tilted globe with a dashed ring circling its northern cap.",
      tags=["arctic circle", "polar circle", "north pole", "latitude 66", "polar region", "globe", "geography"])
def _(S):
    ring = [polar(12, 7.6, 1, a) for a in range(0, 361, 15)]
    ring = [(12 + (x - 12) * 5.6, 7.6 + (y - 7.6) * 2.0) for x, y in ring]
    return [shell(circle(12, 12, 9.5)), detail("M2.5 13.5A9.5 3.2 0 0 0 21.5 13.5")] + [detail(d) for d in dashed(ring, 5.2, 3.6)]


@icon("north-pole", CAT, "Top of the globe with a flag on a pole standing inside a ring at its peak.",
      tags=["north pole", "polar", "pole marker", "arctic", "top of the world", "geographic pole", "expedition"])
def _(S):
    return [shell("M2.5 20A9.5 9.5 0 0 1 21.5 20Z"), detail(ellipse(12, 14.3, 4.6, 1.8)),
            line(seg(12, 11, 12, 2.5)), solid(poly([(12, 2.5), (18, 4.3), (12, 6.1)], closed=True))]


@icon("ice-core", CAT, "Long cylinder of ice with horizontal yearly layers and trapped air bubbles.",
      tags=["ice core", "glacier sample", "climate record", "paleoclimate", "annual layers", "air bubbles", "polar research"])
def _(S):
    ry = L(S, 1.8, 2.4)
    body = f"M7.5 4.5A4.5 {ry} 0 0 1 16.5 4.5V19.5A4.5 {ry} 0 0 1 7.5 19.5Z"
    rb = L(S, 0.8, 1.0)
    return [shell(body), detail(f"M7.5 4.5A4.5 {ry} 0 0 0 16.5 4.5"), detail(f"M7.5 10A4.5 {ry} 0 0 0 16.5 10"),
            detail(f"M7.5 15A4.5 {ry} 0 0 0 16.5 15"), dot(10.4, 12.9, rb), dot(13.6, 12.6, rb), dot(12, 7.6, rb)]


@icon("tree-rings", CAT, "Cut stump top showing concentric growth rings and a crack running in from the bark.",
      tags=["tree rings", "growth rings", "dendrochronology", "stump", "cross section", "tree age", "annual rings"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(circle(12, 12, 4.4)), dot(12, 12, 1.1),
         detail(poly([polar(12, 12, 9.5, 28), polar(12, 12, 7.8, 20), polar(12, 12, 7.0, 30)], r=S.r * 0.3))]


@icon("carbon-dating", CAT, "Fossil bone above a small axes chart with a falling decay curve.",
      tags=["carbon dating", "radiocarbon", "half life", "decay curve", "fossil age", "archaeology", "isotope"])
def _(S):
    return [shell(bone(3, 21, 6, 1.9, 2.6)), line(poly([(4, 12), (4, 21), (21, 21)])),
            line("M6.5 13.5C8 19 12.5 19.5 20 19.5")]


@icon("martian-landscape", CAT, "Rocky desert ground with a distant crater rim and two small moons in the sky.",
      tags=["mars", "martian landscape", "red planet", "desert planet", "crater", "phobos", "space exploration"])
def _(S):
    ground = [(2, 21.5), (2, 17), (6, 15.5), (9.5, 17.2), (14, 15), (18, 16.6), (22, 15), (22, 21.5)]
    return [shell(poly(ground, closed=True, r=S.r * 0.6)), mark(rock(7, 19.3, 1.3)), mark(rock(15, 19, 1.5, 40)),
            line("M3.5 12.5Q7 8.8 10.5 12.5"),
            solid(ellipse(16.5, 6.5, 2.2, 1.8)), solid(ellipse(20.5, 10.6, 1.1, 0.9))]
