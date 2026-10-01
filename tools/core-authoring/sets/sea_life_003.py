"""TypeIcon Core: sea life (batch sea_life_003).

Ocean features, marine science and fishing gear, aquarium kit, conservation scenes and a few more creatures.
Side-view fish face left (head on the left, tail on the right).
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, solid  # noqa: F401
from dsl import shell as _shell
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "sea-life"


# --------------------------------------------------------------------------- local helpers

def shell(d, **attrs):
    attrs.setdefault("stroke_miterlimit", "2.5")
    return _shell(d, **attrs)


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def thick(d, w, S):
    return path_to_d(ST(d, w, S.cap, S.join))


def f(v):
    return fmt(round(v, 2))


def _p(p):
    return f"{f(p[0])} {f(p[1])}"


def pt(c, r, deg):
    return (c[0] + r * math.cos(math.radians(deg)), c[1] + r * math.sin(math.radians(deg)))


def mark(d):
    return Part("dot", d)


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def tube(fn, width, n=28):
    left, right = [], []
    for i in range(n + 1):
        t = i / n
        x, y = fn(t)
        x2, y2 = fn(min(1, t + 1e-3))
        x1, y1 = fn(max(0, t - 1e-3))
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy)
        nx, ny = -dy / ln, dx / ln
        w = width(t) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return left + right[::-1]


def water(x0, x1, y, a=1.2, waves=3):
    """Wavy water line."""
    w = (x1 - x0) / waves
    d = f"M{f(x0)} {f(y)}"
    for i in range(waves):
        xa = x0 + i * w
        d += f"C{f(xa + w * 0.25)} {f(y - a)} {f(xa + w * 0.25)} {f(y - a)} {f(xa + w * 0.5)} {f(y)}"
        d += f"C{f(xa + w * 0.75)} {f(y + a)} {f(xa + w * 0.75)} {f(y + a)} {f(xa + w)} {f(y)}"
    return d


def head(S, p, direction, size=3.0):
    """Open arrowhead (chevron) with its tip at p, pointing along direction (dx, dy)."""
    dx, dy = direction
    n = math.hypot(dx, dy)
    dx, dy = dx / n, dy / n
    bx, by = p[0] - dx * size, p[1] - dy * size
    px, py = -dy, dx
    return line(poly([(bx + px * size * 0.9, by + py * size * 0.9), p, (bx - px * size * 0.9, by - py * size * 0.9)], r=S.r))


def ea(cx, cy, rx, ry, a0, a1):
    """Elliptical arc, clockwise on screen from a0 to a1 (degrees). Returns (d, end point, end tangent)."""
    p0 = (cx + rx * math.cos(math.radians(a0)), cy + ry * math.sin(math.radians(a0)))
    p1 = (cx + rx * math.cos(math.radians(a1)), cy + ry * math.sin(math.radians(a1)))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    d = f"M{_p(p0)}A{f(rx)} {f(ry)} 0 {large} 1 {_p(p1)}"
    t = math.radians(a1)
    return d, p1, (-rx * math.sin(t), ry * math.cos(t))


def rp(pts, deg=45, c=(12, 12)):
    """Rotate points clockwise on screen about c."""
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    return [(c[0] + (x - c[0]) * ca - (y - c[1]) * sa, c[1] + (x - c[0]) * sa + (y - c[1]) * ca) for x, y in pts]


def blob(cx, cy, r, amp, k, ph=0.0, n=36):
    """Points of a gently lobed closed curve r + amp * cos(k * a + ph)."""
    return [(cx + (r + amp * math.cos(k * a + ph)) * math.cos(a), cy + (r + amp * math.cos(k * a + ph)) * math.sin(a))
            for a in (2 * math.pi * i / n for i in range(n))]


def sparkle(x, y, r):
    k = r * 0.32
    return solid(poly([(x, y - r), (x + k, y - k), (x + r, y), (x + k, y + k), (x, y + r), (x - k, y + k), (x - r, y), (x - k, y - k)], closed=True))


def fish_d(cx, cy, w, h, deg=0, flip=False, r=0.0):
    """Small fish silhouette facing left (right when flip), centred on (cx, cy), w wide and h tall; optional rotation."""
    bw = w * 0.36
    bx = cx - w * 0.12
    body_ = ellipse(bx, cy, bw, h / 2)
    tail = poly([(bx + bw - 0.6, cy), (cx + w / 2, cy - h * 0.55), (cx + w / 2, cy + h * 0.55)], closed=True, r=r)
    d = union(body_, tail)
    if flip:
        d = path_to_d(transform_path(P(d), (-1, 0, 0, 1, 2 * cx, 0)))
    return rot(d, deg, cx, cy) if deg else d


def small_fish(cx, cy, w=5.4, h=3.2, deg=0, flip=False, r=0.0):
    return solid(fish_d(cx, cy, w, h, deg, flip, r))


def dashed(ctrl, n=7, frac=0.55, k=4):
    """Dashed line along a cubic: n dashes, each a short polyline of k samples."""
    d = ""
    for i in range(n):
        t0, t1 = i / n, (i + frac) / n
        pts = [bez(*ctrl, t0 + (t1 - t0) * j / (k - 1)) for j in range(k)]
        d += "M" + "L".join(_p(p) for p in pts)
    return d


def fish_outline(x0, x1, cy, h, tail=3.2, th=2.6):
    """Closed outline of a simple fish (nose at x0, body to x1, tail beyond), for use as a detail or a shell."""
    xm = (x0 + x1) / 2
    return (f"M{f(x0)} {f(cy)}C{f(x0 + 1.5)} {f(cy - h)} {f(xm + 1.5)} {f(cy - h)} {f(x1)} {f(cy - 0.8)}"
            f"L{f(x1 + tail)} {f(cy - th)}L{f(x1 + tail)} {f(cy + th)}L{f(x1)} {f(cy + 0.8)}"
            f"C{f(xm + 1.5)} {f(cy + h)} {f(x0 + 1.5)} {f(cy + h)} {f(x0)} {f(cy)}Z")


# --------------------------------------------------------------------------- ocean places and processes

@icon("shipwreck", CAT, "Tilted ship hull resting on the seabed with a snapped mast",
      tags=["wreck", "sunken ship", "sunk", "dive site", "seabed", "ocean"])
def _(S):
    hull = poly([(2.5, 11.5), (20.5, 15), (17, 19.5), (7, 18.5)], closed=True, r=L(S, 0, 1.2))
    return [shell(hull), line(poly([(11.3, 13.2), (10.5, 7), (12.6, 5.8), (11.2, 3.4)], r=S.r)),
            line(seg(2, 21.5, 22, 21.5))]


@icon("ocean-current", CAT, "Three long curving arrows sweeping across the water",
      tags=["current", "flow", "gulf stream", "tide", "drift", "ocean"])
def _(S):
    out = []
    for y in (6.5, 12, 17.5):
        out.append(line(f"M2.5 {f(y + 1)}C7 {f(y - 4)} 11 {f(y + 5)} 19.5 {f(y)}"))
        out.append(head(S, (20.6, y - 0.1), (4, -1.2), 3))
    return out


@icon("ocean-layers", CAT, "Cross section of the sea in three depth bands under a sun",
      tags=["depth zones", "sunlight zone", "twilight zone", "midnight zone", "water column", "ocean"])
def _(S):
    rr = L(S, 1, 3)
    body_ = (water(3, 21, 8.5, 1.2, 3) + f"V{f(21 - rr)}" + (f"L{f(21 - rr)} 21H{f(3 + rr)}L3 {f(21 - rr)}Z" if S.name == "line"
             else f"Q21 21 {f(21 - rr)} 21H{f(3 + rr)}Q3 21 3 {f(21 - rr)}Z"))
    return [shell(body_), detail(water(3, 21, 13.5, 0.8, 3)), detail(water(3, 21, 18, 0.8, 3)), dot(17.5, 4, 1.6)]


@icon("bioluminescence", CAT, "Dark wave line sprinkled with glowing sparkles along its crest",
      tags=["glowing sea", "glow", "plankton glow", "night sea", "light", "ocean"])
def _(S):
    return [line(water(2, 22, 16.5, 1.7, 2)), line(water(2, 22, 21, 1.2, 2)),
            sparkle(7, 8.5, 3.2), sparkle(16.5, 6.5, 2.6), sparkle(13, 12.8, 1.8), sparkle(19.8, 12.3, 1.6), sparkle(3.6, 13.3, 1.5)]


@icon("seabed", CAT, "Sandy seafloor under a wavy surface with a rock, a shell and a sprig of seaweed",
      tags=["seafloor", "ocean floor", "sea bottom", "benthic", "sand", "underwater"])
def _(S):
    rock = poly([(3.5, 19), (4.2, 15.5), (7, 13.5), (9.8, 15), (10.8, 19)], closed=True, r=L(S, 0, 1.5))
    shell_ = "M12.6 19.4A2.4 2.4 0 0 1 17.4 19.4Z"
    return [line(water(2, 22, 4.5, 1, 3)), line(seg(2, 21.5, 22, 21.5)), shell(rock), solid(shell_),
            line("M19.5 20C18 17 20.7 15 19.3 12C18.5 10.5 19.5 9.5 19.5 8.5")]


@icon("blue-hole", CAT, "Top view of a dark round deep hole in the middle of a pale shallow reef",
      tags=["sinkhole", "marine sinkhole", "deep pool", "reef", "diving", "ocean"])
def _(S):
    k, ph = L(S, (3, 0.0), (2, 0.9))
    outer = poly(blob(12, 12, 9, 0.9, k, ph), closed=True)
    inner = poly(blob(12, 12, 4.3, 0.5, k + 1, ph), closed=True)
    return [shell(outer), mark(inner)]


@icon("cove", CAT, "Top view of a small rounded bay tucked into the coastline with a narrow mouth",
      tags=["bay", "inlet", "lagoon", "sheltered", "harbor", "coast"])
def _(S):
    coast = ("M2 9.5C5.5 9.5 8 9.5 8.3 12.2C5.8 14.2 6.5 20.5 12 20.5C17.5 20.5 18.2 14.2 15.7 12.2C16 9.5 18.5 9.5 22 9.5")
    return [line(coast), line(water(9.8, 14.2, 15.5, 0.8, 1)), dot(5, 4.8, 1.1), dot(12, 4.8, 1.1), dot(19, 4.8, 1.1)]


@icon("whale-fall", CAT, "Whale skeleton lying on the seabed with its ribs up and a small fish nearby",
      tags=["whale skeleton", "carcass", "deep sea", "bones", "seabed", "ocean"])
def _(S):
    skull = poly([(2.5, 17.5), (3, 14.2), (7, 14.5), (8, 17.5)], closed=True, r=L(S, 0, 1.2))
    out = [shell(skull), line("M8.5 16.8H20.5"), line(seg(2, 21.5, 22, 21.5))]
    for x in (9, 13.2, 17.4):
        out.append(line(f"M{f(x)} 16.8C{f(x)} 11.5 {f(x + 1.4)} 9.5 {f(x + 1.5)} 8.8C{f(x + 1.6)} 9.5 {f(x + 3)} 11.5 {f(x + 3)} 16.8"))
    out.append(small_fish(5.5, 7, 5.6, 3.2))
    return out


@icon("ocean-upwelling", CAT, "Curved arrows rising from deep water up past a coastal slope to the surface",
      tags=["upwelling", "rising water", "nutrients", "cold water", "coast", "current"])
def _(S):
    slope = poly([(22, 8), (22, 21), (13.5, 21)], closed=True, r=L(S, 0, 1))
    return [line(water(2, 22, 4, 0.9, 3)), shell(slope),
            line("M4.5 20.5C4.5 15 7 13.5 7 8.5"), head(S, (7, 7.4), (0, -1), 2.4),
            line("M10.5 19.5C10.5 15.5 12 14.5 12.5 11"), head(S, (12.6, 9.8), (0.1, -1), 2.4)]


@icon("ocean-gyre", CAT, "Large oval loop of circling arrows with floating debris gathered in the middle",
      tags=["garbage patch", "circulation", "vortex", "swirl", "current", "ocean"])
def _(S):
    d1, p1, t1 = ea(12, 12, 9, 7, 200, 335)
    d2, p2, t2 = ea(12, 12, 9, 7, 20, 155)
    return [line(d1), head(S, p1, t1, 3), line(d2), head(S, p2, t2, 3),
            dot(10.2, 11.2, 1.1), dot(13.8, 10.8, 1.1), dot(12.2, 14, 1.1)]


@icon("marine-snow", CAT, "Specks and flakes drifting down through dark water toward the seabed",
      tags=["detritus", "falling particles", "deep sea", "organic matter", "sinking", "ocean"])
def _(S):
    out = [line(water(2, 22, 21, 0.8, 3))]
    for x, y, r in ((5, 4.5, 1.2), (12, 3.5, 1.1), (18.5, 6, 1.3), (8.5, 9.5, 1.3), (15.5, 11.5, 1.2), (4.5, 14.5, 1.2),
                    (11.5, 16, 1.4), (19, 16.5, 1.1)):
        out.append(dot(x, y, r))
    return out


@icon("fish-tag", CAT, "Fish with a small tracking tag on its back fin and signal arcs above it",
      tags=["tracking", "telemetry", "tagged fish", "satellite tag", "research", "monitoring"])
def _(S):
    b = ellipse(10.5, 16, 7, 3.8)
    t = poly([(15.5, 16), (21, 12.8), (21, 19.2)], closed=True, r=L(S, 0, 0.9))
    return [shell(union(b, t)), dot(6.5, 15, 0.95), line("M11 12.3L12.6 9.2"), dot(12.8, 8.4, 1.5),
            line(arc(12.8, 8.4, 4, -85, -5)), line(arc(12.8, 8.4, 7, -75, -15))]


@icon("fish-measuring-board", CAT, "Fish lying on a long board with a ruler scale marked along its edge",
      tags=["ruler", "length", "catch size", "legal size", "fisheries", "measure"])
def _(S):
    out = [shell(rect(2, 5, 20, 14, L(S, 1, 3))), detail(fish_outline(5.5, 14, 10, 2.4, 3.5, 2.2))]
    for x in (5, 8.5, 12, 15.5, 19):
        out.append(detail(f"M{f(x)} 19V16"))
    return out


@icon("plankton-net", CAT, "Long fine mesh cone with a ring mouth and a small collecting jar at the narrow end",
      tags=["plankton tow", "sampling", "marine biology", "collecting", "research", "survey"])
def _(S):
    cone = poly([(5, 5), (15, 9.5), (15, 14.5), (5, 19)], closed=True, r=L(S, 0, 0.8))
    jar = rect(15, 8.5, 6.5, 7, L(S, 0, 2))
    return [shell(union(cone, jar)), line(ellipse(5, 12, 2, 7)), detail("M10 7.4V16.6")]


@icon("fish-ladder", CAT, "Stepped pools beside a dam with a fish leaping up between the steps",
      tags=["fishway", "dam", "salmon", "river", "migration", "passage"])
def _(S):
    steps = poly([(2, 21), (2, 18), (7, 18), (7, 14), (12, 14), (12, 10), (17, 10), (17, 6), (22, 6), (22, 21)],
                 closed=True, r=L(S, 0, 1))
    return [shell(steps), small_fish(8.2, 8, 7.4, 4.2, -30)]


# --------------------------------------------------------------------------- fishing gear and ocean science

@icon("fish-farm-pen", CAT, "Floating net pen with a mesh net hanging below the water and a fish inside",
      tags=["aquaculture", "fish farm", "sea cage", "net pen", "salmon farm", "fish cage"])
def _(S):
    net = poly([(4.2, 10), (6.8, 20.5), (17.2, 20.5), (19.8, 10)], closed=True, r=L(S, 0, 1.2))
    return [dot(4.2, 7.2, 2.1), dot(19.8, 7.2, 2.1), line(water(6.5, 17.5, 7.4, 0.9, 2)), shell(net),
            detail("M8.8 11.5L9.3 19"), detail("M15.2 11.5L14.7 19"), small_fish(12, 15, 4.4, 2.8)]


@icon("seaweed-farm", CAT, "Rope between two floats with strands of seaweed hanging down from it",
      tags=["kelp farm", "aquaculture", "algae", "longline", "nori", "sea vegetables"])
def _(S):
    out = [dot(3.5, 5.5, 2), dot(20.5, 5.5, 2), line(seg(5, 5.5, 19, 5.5))]
    for x, n in ((7, 12), (12, 15.5), (17, 10.5)):
        out.append(line(f"M{f(x)} 5.5C{f(x - 2.6)} {f(5.5 + n * 0.3)} {f(x + 2.6)} {f(5.5 + n * 0.65)} {f(x)} {f(5.5 + n)}"))
    return out


@icon("trawl-net", CAT, "Long tapering fishing net with a wide open mouth, floats above and weights below",
      tags=["fishing net", "bottom trawl", "dragnet", "commercial fishing", "catch", "seine"])
def _(S):
    net = poly([(6, 5), (17, 10.2), (17, 13.8), (6, 19)], closed=True, r=L(S, 0, 0.8))
    return [shell(union(net, ellipse(19, 12, 2.8, 3))), detail("M9.5 8.2L15 14.5"), detail("M9.5 15.8L15 9.5"),
            dot(4.5, 3, 1.4), dot(4.5, 21, 1.4)]


@icon("hydrophone", CAT, "Underwater microphone hanging on a cable with sound arcs spreading beside it",
      tags=["underwater microphone", "listening", "acoustic", "marine research", "sound", "sonar"])
def _(S):
    return [line("M9 2C9 4.5 11.5 5 9 9"), shell(ellipse(9, 14.2, 3.8, 5.6)), detail("M5.2 12.5H12.8"), detail("M5.2 16H12.8"),
            line(arc(12.5, 14.2, 4.5, -48, 48)), line(arc(12.5, 14.2, 8, -48, 48))]


@icon("secchi-disk", CAT, "Round black and white quartered disk hanging from a rope",
      tags=["water clarity", "turbidity", "visibility", "limnology", "measurement", "lake"])
def _(S):
    cx, cy, r = 12, 15.2, 6.8
    q1 = f"M{cx} {cy}L{cx - 6} {cy}A6 6 0 0 1 {cx} {cy - 6}Z"
    q2 = f"M{cx} {cy}L{cx + 6} {cy}A6 6 0 0 1 {cx} {cy + 6}Z"
    return [line("M12 2V8.4"), shell(circle(cx, cy, r)), mark(q1), mark(q2)]


@icon("profiling-float", CAT, "Tall slim cylinder float standing upright in the water with a short antenna above the surface",
      tags=["argo float", "ocean sensor", "buoy", "oceanography", "drifter", "measurement"])
def _(S):
    return [line("M12 7V3"), dot(12, 2.8, 1.3), shell(rect(9, 7, 6, 14, L(S, 1, 3))), detail("M9 17H15"),
            line(water(2, 9, 10.5, 0.9, 1)), line(water(15, 22, 10.5, 0.9, 1))]


@icon("water-sampling-bottle", CAT, "Tube shaped sampling bottle with caps at both ends clipped to a vertical cable",
      tags=["niskin bottle", "water sample", "rosette", "oceanography", "collecting", "research"])
def _(S):
    return [line("M20 2V22"), shell(rect(7.5, 3.5, 7.5, 17, L(S, 1, 3))), detail("M7.5 7.5H15"), detail("M7.5 16.5H15"),
            line(seg(15, 11, 20, 11)), line(seg(15, 14, 20, 14))]


@icon("sediment-core", CAT, "Clear tube holding a cylinder of seabed mud with stacked horizontal layers",
      tags=["core sample", "mud", "geology", "seabed sample", "layers", "drilling"])
def _(S):
    return [line(seg(6, 3.5, 18, 3.5)), line(seg(12, 3.5, 12, 6)), shell(rect(8, 6, 8, 15.5, L(S, 1, 4))),
            detail("M8 11.2L16 10.4"), detail("M8 16L16 16.8"), dot(11, 8.5, 0.9), dot(13.6, 13.5, 0.9)]


@icon("survey-quadrat", CAT, "Square frame divided into a grid laid on the seabed over a coral and a shell",
      tags=["quadrat", "transect", "ecology survey", "monitoring", "reef survey", "marine biology"])
def _(S):
    return [shell(rect(3, 3, 18, 18, L(S, 0.5, 3))), detail("M12 3V21"), detail("M3 12H21"),
            solid("M5.2 19.6A2.4 2.4 0 0 1 10 19.6Z"), line("M16.5 19.5V16M16.5 18L14.8 16.2M16.5 17L18.3 15.2")]


@icon("underwater-rov", CAT, "Boxy remote underwater vehicle with lights, side thrusters and a tether rising from its top",
      tags=["rov", "robot submarine", "underwater drone", "remote vehicle", "inspection", "ocean exploration"])
def _(S):
    body_ = rect(7, 9.5, 10, 8.5, L(S, 1, 3))
    return [line("M12 9.5V6.5C12 4 15.5 4.5 15.5 2"),
            shell(union(body_, rect(2.5, 11.5, 4.5, 4.5, L(S, 0, 1.5)), rect(17, 11.5, 4.5, 4.5, L(S, 0, 1.5)))),
            detail(circle(12, 13.8, 2.2)), line(seg(9, 21, 15, 21))]


@icon("bathysphere", CAT, "Round steel diving sphere with small round portholes hanging from a cable",
      tags=["deep sea", "diving bell", "submersible", "exploration", "vintage", "ocean depth"])
def _(S):
    return [line("M12 2V6.6"), shell(circle(12, 15, 6.8)), detail(circle(9.6, 14.2, 1.6)), detail(circle(14.8, 15.4, 1.6)),
            dot(12, 7.4, 1.5)]


@icon("seafloor-mapping", CAT, "Boat on the water sending a fan of sonar beams down to an uneven seabed",
      tags=["sonar survey", "bathymetry", "multibeam", "echo sounder", "hydrography", "depth"])
def _(S):
    hull = poly([(8.5, 4), (15.5, 4), (14, 6.8), (10, 6.8)], closed=True, r=L(S, 0, 0.8))
    return [shell(hull), line(water(2, 7, 7.8, 0.7, 1)), line(water(17, 22, 7.8, 0.7, 1)),
            line(seg(12, 9.5, 5.2, 16.5)), line(seg(12, 9.5, 12, 17)), line(seg(12, 9.5, 18.8, 16.5)),
            line(poly([(2, 18), (6, 20.5), (10, 18.5), (14, 21), (18, 19), (22, 20.5)], r=S.r))]


@icon("fish-finder", CAT, "Small sonar screen showing fish shaped arches above the seabed, with a cable to a transducer",
      tags=["sonar", "echo sounder", "angling", "fishing electronics", "depth finder", "display"])
def _(S):
    return [shell(rect(3, 3, 18, 13, L(S, 1, 3))), mark(fish_d(8.5, 8, 5.4, 3.2)), mark(fish_d(15.5, 9.5, 5.4, 3.2, -15)),
            detail("M4 13.2L9 12L13 13.5L20 12.2"),
            line("M12 16V19C12 20.5 14 21 17 21"), dot(19.2, 21, 1.4)]


@icon("specimen-jar", CAT, "Lidded glass jar with a preserved small fish floating inside",
      tags=["preserved", "museum", "laboratory", "collection", "biology", "marine specimen"])
def _(S):
    return [shell(rect(5.5, 7, 13, 14.5, L(S, 1, 3.5))), shell(rect(7, 3, 10, 3, L(S, 0, 1))),
            detail(fish_outline(8, 13, 14.2, 2.2, 3.2, 2))]


@icon("aquarium-tank", CAT, "Glass fish tank with a lid, gravel, a plant and a fish",
      tags=["fish tank", "aquarium", "pet fish", "fishkeeping", "glass tank", "aquascape"])
def _(S):
    return [line("M2.5 3.8H21.5"), shell(rect(3, 7, 18, 14, L(S, 1, 3))), detail("M3 17.5H21"),
            detail("M17.5 17.5V11.5"), detail("M17.5 14.5L15.2 12.5"), mark(fish_d(9, 12.3, 6, 3.6))]

# --------------------------------------------------------------------------- aquarium kit

@icon("aquarium-net", CAT, "Small rectangular fish scoop net on a straight handle",
      tags=["fish net", "scoop", "landing net", "fishkeeping", "aquarium", "tank maintenance"])
def _(S):
    frame = poly(rp([(8, 3), (16, 3), (16, 12), (8, 12)]), closed=True, r=L(S, 0, 1.2))
    return [shell(frame), detail(poly(rp([(12, 3), (12, 12)]))), detail(poly(rp([(8, 7.5), (16, 7.5)]))),
            line(poly(rp([(12, 12), (12, 21.5)])))]


@icon("aquarium-filter", CAT, "Box filter hanging on the tank wall with water pouring back in from its spout",
      tags=["tank filter", "hang on back filter", "water pump", "fishkeeping", "clean water", "aquarium"])
def _(S):
    return [shell(rect(2.5, 5.5, 8, 13.5, L(S, 1, 2.5))), line(poly([(14, 9.5), (14, 21), (21.5, 21)], r=S.r)),
            line(poly([(10.5, 7), (18, 7), (18, 10.5)], r=S.r)), line(water(15.5, 21.5, 15.5, 0.8, 1))]


@icon("aquarium-heater", CAT, "Slim glass tube heater with a control dial at the top and suction cup clips on the side",
      tags=["tank heater", "thermostat", "warm water", "temperature", "fishkeeping", "aquarium"])
def _(S):
    body_ = union(rect(8.5, 2.8, 7, 5, L(S, 0.5, 2)), rect(9.5, 7.5, 5, 14, L(S, 0, 2.5)))
    return [shell(body_), detail("M12 12V18"), dot(12, 5.3, 0.9), line(seg(14.5, 12, 18, 12)), line(seg(14.5, 18, 18, 18)),
            dot(19.2, 12, 1.5), dot(19.2, 18, 1.5)]


@icon("aquarium-air-stone", CAT, "Small cylinder stone on the tank floor with an air tube and a column of bubbles rising from it",
      tags=["bubbler", "airstone", "aerator", "oxygen", "air pump", "aquarium"])
def _(S):
    return [line(seg(2, 21, 22, 21)), shell(rect(4, 16, 8, 4.4, L(S, 1, 2.2))),
            line("M12 18C16.5 18 19 16 19 12V8"), dot(8, 12.3, 1.1), dot(9.6, 8.6, 1.4), dot(7.6, 4.6, 1.7)]


@icon("aquarium-test-kit", CAT, "Small dropper bottle beside a water test color chart card with swatches",
      tags=["water test", "ph test", "ammonia test", "nitrate", "water quality", "fishkeeping"])
def _(S):
    bottle = union(rect(3, 9.5, 7.5, 11, L(S, 1, 2.5)), rect(4.8, 5.5, 3.9, 4.5, 0))
    return [shell(bottle), shell(rect(13, 3.5, 8.5, 17, L(S, 1, 2.5))), mark(rect(15, 6.2, 4.5, 2.6, 0)),
            mark(rect(15, 10.7, 4.5, 2.6, 0)), mark(rect(15, 15.2, 4.5, 2.6, 0))]


@icon("gravel-siphon", CAT, "Wide tube dipped into tank gravel with a hose leading over to a bucket",
      tags=["gravel vacuum", "water change", "tank cleaning", "aquarium maintenance", "hose", "siphon"])
def _(S):
    bucket = poly([(14, 13), (22, 13), (20.8, 21.5), (15.2, 21.5)], closed=True, r=L(S, 0, 1))
    return [shell(rect(3.5, 2.5, 6, 14.5, L(S, 0.5, 2.5))), line("M9.5 5C14 3 18 4.5 18 10V14"), shell(bucket),
            dot(3.8, 20.6, 1.2), dot(7, 19.6, 1.2), dot(10, 20.8, 1.2)]


@icon("fish-bag", CAT, "Clear plastic bag tied at the top and filled with water with a small fish inside",
      tags=["pet shop", "buying fish", "transport", "water bag", "goldfish", "plastic bag"])
def _(S):
    bag = "M10 7.5C6 9.5 4.5 14 6 18C7 20.5 9 21.5 12 21.5C15 21.5 17 20.5 18 18C19.5 14 18 9.5 14 7.5Z"
    return [shell(bag), line(poly([(8.7, 3.2), (12, 7.5), (15.3, 3.2)], r=S.r)), mark(fish_d(12, 15.5, 7, 4))]


# --------------------------------------------------------------------------- conservation and threats

@icon("marine-reserve", CAT, "Dashed boundary circle around a fish and a coral branch inside protected water",
      tags=["marine protected area", "mpa", "no take zone", "sanctuary", "protected sea", "conservation"])
def _(S):
    out = [line(arc(12, 12, 9.5, a, a + 28)) for a in range(0, 360, 45)]
    out += [small_fish(10.5, 9.2, 6, 3.6), line("M13.5 18.5V14.2M13.5 16.5L11.7 14.7M13.5 15.5L15.3 13.7")]
    return out


@icon("ocean-conservation", CAT, "Two cupped hands holding a wave with a small fish above it",
      tags=["protect the sea", "save the ocean", "marine protection", "stewardship", "care", "environment"])
def _(S):
    bowl = ("M2.5 11.5C2.5 17.5 7 21 12 21C17 21 21.5 17.5 21.5 11.5L18 13.2C16.5 15.5 14 16.5 12 16.5C10 16.5 7.5 15.5 6 13.2Z")
    return [shell(bowl), line("M6.5 12.2C6.5 8 10 6.8 12.8 8.4C14.6 9.5 14.4 11.6 12.6 11.4"), small_fish(17, 5.2, 5.6, 3.4)]


@icon("sustainable-seafood", CAT, "Side view of a fish with a leaf growing from its back in place of a dorsal fin",
      tags=["responsible fishing", "eco friendly", "certified seafood", "green", "food", "sustainable"])
def _(S):
    b = ellipse(10.5, 15, 7, 4.3)
    t = poly([(16, 15), (21.5, 11.8), (21.5, 18.2)], closed=True, r=L(S, 0, 0.9))
    leaf = "M10.3 11C8.8 6.8 12 3.2 17.5 3C17.5 8.5 14.5 11.3 10.3 11Z"
    return [shell(union(b, t, leaf)), detail("M11.6 9.6L15 5.6"), dot(6.2, 14, 1)]


@icon("overfishing", CAT, "Bulging net overflowing with fish beside a downward arrow",
      tags=["fish stocks", "depletion", "bycatch", "commercial fishing", "overfished", "decline"])
def _(S):
    bag = "M5.5 8H13.5C17.5 11 17 18 13.5 21H5.5C2 18 1.8 11 5.5 8Z"
    return [shell(bag), detail("M4.5 14L9 18.8"), detail("M9 11L14.5 17.5"),
            small_fish(6, 5, 5.6, 3.2, -15), small_fish(12, 4.2, 5.6, 3.2, 12),
            line("M19.5 3.5V15"), head(S, (19.5, 17), (0, 1), 2.6)]


@icon("ocean-plastic", CAT, "Plastic bottle and a bag floating on a wavy water line with a fish swimming beneath",
      tags=["marine litter", "trash in the sea", "pollution", "garbage", "waste", "environment"])
def _(S):
    bottle = poly([(5.7, 3), (8.3, 3), (8.3, 5.5), (10, 7), (10, 12), (4, 12), (4, 7), (5.7, 5.5)], closed=True, r=L(S, 0, 1))
    bag = poly([(14, 12), (14.5, 6.8), (19.5, 6.8), (20, 12)], closed=True, r=L(S, 0, 0.8))
    return [shell(bottle), shell(bag), line("M15.6 6.8C15.6 4 18.4 4 18.4 6.8"),
            line(water(2, 22, 13, 1, 3)), small_fish(12, 18.6, 7, 4)]


@icon("microplastics", CAT, "Water drop filled with tiny irregular plastic fragments",
      tags=["plastic pollution", "nanoplastics", "contamination", "particles", "water pollution", "fragments"])
def _(S):
    if S.name == "line":
        dropd = "M12 2.5L6.2 11C4.2 14 4.5 18 7 20.2C9.6 22.5 14.4 22.5 17 20.2C19.5 18 19.8 14 17.8 11Z"
    else:
        dropd = "M12 2.5C11 4 5 10.5 5 15C5 19 8.2 21.5 12 21.5C15.8 21.5 19 19 19 15C19 10.5 13 4 12 2.5Z"
    return [shell(dropd), mark(poly([(9.4, 11.6), (12.6, 10.6), (13.4, 13.4), (10.6, 14.4)], closed=True)),
            mark(poly([(13.6, 16), (16, 15.2), (15.8, 18), (13.4, 18.4)], closed=True)), dot(9, 17.6, 1.2)]


@icon("oil-spill", CAT, "Dark oil slick spreading across the water surface below a falling drop",
      tags=["petroleum", "crude oil", "tanker spill", "marine pollution", "disaster", "slick"])
def _(S):
    slick = poly([(3.5, 17), (5, 14.5), (8.5, 14.2), (10.5, 12.6), (14, 13), (15.5, 14.8), (19, 14.4), (21, 17), (18, 19.6), (12, 19.4), (7, 19.8)],
                 closed=True, r=L(S, 0, 2.2))
    drop = "M12 2.5C11.4 3.6 9.2 5.8 9.2 7.8C9.2 9.5 10.4 10.6 12 10.6C13.6 10.6 14.8 9.5 14.8 7.8C14.8 5.8 12.6 3.6 12 2.5Z"
    return [solid(drop), solid(slick), line(water(2, 22, 21.8, 0.7, 3))]


@icon("ghost-net", CAT, "Torn tangled fishing net drifting in the water with a fish caught in its mesh",
      tags=["lost fishing gear", "abandoned net", "entanglement", "bycatch", "marine debris", "derelict"])
def _(S):
    net = poly([(3, 5), (19, 3.5), (21, 12), (17, 15), (18.5, 21), (12, 17.5), (8, 21), (3, 14)], closed=True, r=L(S, 0, 1.2))
    return [shell(net), detail("M3.5 11L10 4.5"), detail("M12.5 16.8L20.5 8.5"), mark(fish_d(10.5, 11.2, 5.6, 3.4, 10))]


# --------------------------------------------------------------------------- ocean measures, sound and movement

@icon("ocean-acidification", CAT, "Ridged scallop shell with a water drop and bubbles above it",
      tags=["ph", "co2", "carbon dioxide", "shell loss", "climate change", "chemistry"])
def _(S):
    fan = "M12 21.5L3.5 15C3.5 11.5 7.5 10.5 12 10.5C16.5 10.5 20.5 11.5 20.5 15Z"
    drop = "M17 2.3C16.4 3.4 14.8 5.2 14.8 6.6C14.8 7.8 15.8 8.6 17 8.6C18.2 8.6 19.2 7.8 19.2 6.6C19.2 5.2 17.6 3.4 17 2.3Z"
    return [shell(fan), detail("M12 20V12"), detail("M12 20L7.6 13.2"), detail("M12 20L16.4 13.2"), solid(drop), dot(8, 5.6, 1.1), dot(11.4, 3.6, 0.9)]


@icon("sea-temperature", CAT, "Thermometer standing in the sea with its bulb below the wavy surface",
      tags=["water temperature", "ocean warming", "marine heatwave", "thermometer", "climate", "measurement"])
def _(S):
    stem = union(rect(10, 2.5, 4, 14, 2), circle(12, 17, 3.6))
    return [shell(stem), dot(12, 17, 1.3), line(water(2, 8, 11.5, 0.8, 1)), line(water(16, 22, 11.5, 0.8, 1)),
            line(water(2, 8, 17, 0.8, 1)), line(water(16, 22, 17, 0.8, 1))]


@icon("salinity", CAT, "Water drop with a few small salt crystal cubes inside it",
      tags=["salt", "salty water", "brine", "sodium chloride", "seawater", "chemistry"])
def _(S):
    if S.name == "line":
        dropd = "M12 2.5L6 11C4 14 4.4 18 7 20.4C9.6 22.6 14.4 22.6 17 20.4C19.6 18 20 14 18 11Z"
    else:
        dropd = "M12 2.5C11 4 5 10.5 5 15C5 19 8.2 21.5 12 21.5C15.8 21.5 19 19 19 15C19 10.5 13 4 12 2.5Z"
    return [shell(dropd), mark(rect(9.6, 11.4, 3, 3, 0)), mark(rect(13.2, 14.6, 3, 3, 0)), mark(rect(8.6, 16.4, 2.6, 2.6, 0))]


@icon("ocean-depth", CAT, "Double headed vertical arrow with tick marks between the wavy surface and the seabed",
      tags=["depth", "fathoms", "metres", "sounding", "bathymetry", "how deep"])
def _(S):
    return [line(water(2, 22, 3.8, 0.9, 3)), line(seg(2, 21.5, 22, 21.5)), line(seg(9, 8, 9, 17.5)),
            head(S, (9, 6.6), (0, -1), 2.6), head(S, (9, 18.8), (0, 1), 2.6),
            line(seg(14, 9, 20, 9)), line(seg(14, 13, 18, 13)), line(seg(14, 17, 20, 17))]


def whale_d(S, cx=10.5, cy=16.8, sc=1.0, ox=0.0, oy=0.0):
    """Whale in side view (head left) as one region; scaled about (cx, cy) then shifted by (ox, oy)."""
    body_ = ellipse(cx, cy, 8, 4.4)
    tail = thick(f"M{f(cx + 5)} {f(cy - 0.6)}C{f(cx + 8.1)} {f(cy - 1)} {f(cx + 9.1)} {f(cy - 3.8)} {f(cx + 8.5)} {f(cy - 6.3)}", 3, S)
    flukes = poly([(cx + 5.3, cy - 8.8), (cx + 8.7, cy - 6.2), (cx + 11.9, cy - 8.8), (cx + 11.1, cy - 4.6), (cx + 8.7, cy - 5.2),
                   (cx + 6.1, cy - 4.6)], closed=True, r=L(S, 0, 0.8))
    d = union(body_, tail, flukes)
    if sc != 1.0 or ox or oy:
        d = path_to_d(transform_path(P(d), (sc, 0, 0, sc, cx - cx * sc + ox, cy - cy * sc + oy)))
    return d


@icon("whale-song", CAT, "Side view of a whale with curved sound arcs rising from its head",
      tags=["whale call", "humpback", "underwater sound", "bioacoustics", "singing", "marine mammal"])
def _(S):
    return [shell(whale_d(S)), dot(6.2, 16, 0.95), line(arc(7, 12, 2.8, -140, -40)), line(arc(7, 12, 5.6, -140, -40)),
            line(arc(7, 12, 8.4, -135, -55))]


@icon("echolocation", CAT, "Dolphin head sending sound arcs toward a small fish, with the echo coming back",
      tags=["sonar", "clicks", "dolphin", "biosonar", "navigation", "marine mammal"])
def _(S):
    headd = "M2.5 19.5C2 13 6 10 9.5 11C11.2 11.5 12 13 14.5 14.5L14.5 16.3C12.5 16.5 11 17 10 18C8.5 20 5 20.5 2.5 19.5Z"
    return [shell(headd), dot(8.4, 14.6, 0.9), line(arc(14.5, 15.3, 4, -80, -20)), line(arc(14.5, 15.3, 7, -80, -25)),
            small_fish(18.6, 6, 6.4, 3.8)]


@icon("fish-migration", CAT, "Fish following a long curved dashed route that ends in an arrowhead",
      tags=["route", "spawning run", "swimming path", "journey", "tracking", "movement"])
def _(S):
    ctrl = ((10, 17.5), (15, 18.5), (6, 5), (18.5, 5.5))
    return [small_fish(5.2, 17.8, 7, 4.2), line(dashed(ctrl, 6, 0.6, 4)), head(S, (21, 5.5), (1, 0.05), 3)]

# --------------------------------------------------------------------------- beach, fish parts and runs

@icon("beach-cleanup", CAT, "Trash bag and a litter grabber stick standing on a sand line",
      tags=["litter pick", "shoreline cleanup", "volunteer", "rubbish", "coastal", "recycling"])
def _(S):
    bag = "M3.5 13C3.5 10.5 5.5 10 7 7.8C8.5 10 10.5 10.5 10.5 13C11.8 17 10 20.5 7 20.5C4 20.5 2.2 17 3.5 13Z"
    return [line(seg(2, 21.5, 22, 21.5)), shell(bag), line(poly([(4.8, 4.4), (7, 7.8), (9.2, 4.4)], r=S.r)),
            line(poly([(13.2, 5.2), (17.4, 6.8), (16, 10.4)], r=S.r)), line(seg(21, 19.5, 16.4, 8.6))]


@icon("reef-safe-sunscreen", CAT, "Sunscreen squeeze tube with a small coral branch on its label",
      tags=["sun cream", "spf", "ocean friendly", "coral safe", "snorkeling", "beach"])
def _(S):
    body_ = union(poly([(7, 5), (17, 5), (16, 18), (8, 18)], closed=True, r=L(S, 0, 1)), rect(9.5, 17.5, 5, 3.8, L(S, 0, 1)))
    return [shell(body_), detail("M7 7.5H17"), detail("M12 16V11.5"), detail("M12 14L9.8 11.8"), detail("M12 12.8L14.2 10.6")]


@icon("sea-glass", CAT, "Three small smooth rounded frosted glass pebbles with soft highlights",
      tags=["beach glass", "pebbles", "frosted glass", "treasure", "shoreline", "collecting"])
def _(S):
    k, ph = L(S, (3, 0.4), (2, 1.2))
    out = []
    for cx, cy, r in ((7.5, 15.5, 4.6), (15.5, 7.5, 4.4), (17, 17, 3.8)):
        out.append(shell(poly(blob(cx, cy, r, 0.5, k, ph + cx), closed=True)))
        out.append(dot(cx - r * 0.2, cy - r * 0.25, 0.9))
    return out


@icon("fish-tail", CAT, "Single forked tail fin with fin rays fanning out from the stem",
      tags=["caudal fin", "fin", "fish part", "swimming", "anatomy", "tail"])
def _(S):
    tail = "M2.5 10.5L7 10.8C12 9.5 17 7 21.5 3.8C18.6 8 16.6 10 16.2 12C16.6 14 18.6 16 21.5 20.2C17 17 12 14.5 7 13.2L2.5 13.5Z"
    return [shell(tail), detail("M8.5 11.4L16 7.4"), detail("M8.5 12H12.8"), detail("M8.5 12.6L16 16.6")]


@icon("fish-scales", CAT, "Pattern of overlapping rounded fish scales in staggered rows",
      tags=["scale pattern", "scaly", "skin", "texture", "mermaid", "fish skin"])
def _(S):
    out = []
    for r_, y in enumerate((6, 10, 14, 18)):
        if r_ % 2 == 0:
            for cx in (6, 12, 18):
                out.append(line(arc(cx, y, 3, 0, 180)))
        else:
            out.append(line(arc(3, y, 3, 0, 90)))
            for cx in (9, 15):
                out.append(line(arc(cx, y, 3, 0, 180)))
            out.append(line(arc(21, y, 3, 90, 180)))
    return out


@icon("fish-skeleton", CAT, "Side view of a fish skeleton with a head, a spine, rib bones and a tail fin",
      tags=["fish bones", "fishbone", "bones", "dead fish", "leftover", "anatomy"])
def _(S):
    out = [shell(ellipse(5.8, 12, 3.8, 3.2)), line("M9.6 12H17.4"), dot(5, 11.2, 0.8),
           shell(poly([(17.4, 12), (21.8, 7.6), (21.8, 16.4)], closed=True, r=L(S, 0, 0.9)))]
    for x in (11.2, 13.4, 15.6):
        out.append(line(f"M{f(x)} 12L{f(x + 1.4)} 8"))
        out.append(line(f"M{f(x)} 12L{f(x + 1.4)} 16"))
    return out


@icon("fish-eggs", CAT, "Cluster of round fish eggs each with a dark dot inside",
      tags=["roe", "caviar", "spawn", "spawning", "hatchery", "reproduction"])
def _(S):
    out = []
    for cx, cy in ((6.5, 7), (15, 6.2), (10.5, 14.2), (19, 14.8)):
        out.append(shell(circle(cx, cy, 2.9) if S.name == "rounded" else poly(regular(cx, cy, 2.9, 10, -90), closed=True)))
        out.append(dot(cx, cy, 0.9))
    return out


@icon("fish-gills", CAT, "Close up side view of a fish head with a curved gill cover and arched gill slits behind it",
      tags=["gill", "breathing", "respiration", "fish anatomy", "head", "operculum"])
def _(S):
    return [line("M21.5 6.4C14 4.2 6.8 6 2.8 12C6.8 18 14 19.8 21.5 17.6"), line("M11.5 6.8C9.2 9.6 9.2 14.4 11.5 17.2"),
            line("M15 6.2C13.4 9.4 13.4 14.6 15 17.8"), line("M18.4 6.2C17.4 9.4 17.4 14.6 18.4 17.8"),
            dot(6.2, 10.4, 1), line("M2.8 13.6H6.4")]


@icon("salmon-run", CAT, "Salmon leaping upstream in an arc over a small stepped waterfall",
      tags=["spawning", "river", "migration", "leaping fish", "waterfall", "wild salmon"])
def _(S):
    falls = poly([(22, 21.5), (22, 14), (18, 14), (18, 18), (14.5, 18), (14.5, 21.5)], closed=True, r=L(S, 0, 1))
    return [shell(falls), small_fish(8, 13.5, 10, 5.4, -40, flip=True), small_fish(15.5, 6, 7.4, 4.2, -15, flip=True),
            line(water(2, 11.5, 21.2, 0.7, 2))]

# --------------------------------------------------------------------------- creatures and scenes

def poly_path_union(ds):
    return union(*ds)


def jelly(S, x, y, r, tl=4.2):
    dome = f"M{f(x - r)} {f(y)}A{f(r)} {f(r * 0.95)} 0 0 1 {f(x + r)} {f(y)}Z"
    out = [shell(dome)]
    for dx in (-r * 0.45, r * 0.45):
        out.append(line(f"M{f(x + dx)} {f(y + 1)}C{f(x + dx - 1.1)} {f(y + 1 + tl * 0.35)} {f(x + dx + 1.1)} {f(y + 1 + tl * 0.7)} {f(x + dx)} {f(y + 1 + tl)}"))
    return out


@icon("bait-ball", CAT, "Tight round ball made of many tiny fish swirling around each other",
      tags=["fish school", "shoal", "sardine run", "predator prey", "swirl", "baitfish"])
def _(S):
    rr = L(S, 0, 0.5)
    out = [shell(circle(12, 12, 9.6))]
    rows = ((6.9, (12,)), (10.3, (7.2, 16.8)), (13.7, (12,)), (17.1, (8, 16)))
    for i, (y, xs) in enumerate(rows):
        for j, x in enumerate(xs):
            out.append(mark(fish_d(x, y, 4.6, 2.6, 0, (i + j) % 2 == 1, rr)))
    return out


@icon("clownfish-anemone", CAT, "Small banded clownfish nestled among the wavy tentacles of a sea anemone",
      tags=["nemo", "anemonefish", "symbiosis", "coral reef", "tropical", "marine life"])
def _(S):
    b = ellipse(11.5, 9.5, 5.6, 3.7)
    t = poly([(16, 9.5), (20.5, 6.6), (20.5, 12.4)], closed=True, r=L(S, 0, 0.9))
    out = [shell(union(b, t)), detail("M9 6.2C8.4 8 8.4 11 9 12.8"), detail("M13.6 6.2C14.2 8 14.2 11 13.6 12.8"), dot(7.3, 8.6, 0.8)]
    for x in (4.5, 9, 13.5, 18.5):
        out.append(line(f"M{f(x)} 21.5C{f(x - 1.8)} 19.5 {f(x + 1.8)} 18.5 {f(x)} 16.2"))
    return out


@icon("neon-tetra", CAT, "Side view of a tiny slim fish with one bold stripe from eye to tail",
      tags=["tetra", "aquarium fish", "freshwater", "tropical fish", "schooling fish", "pet fish"])
def _(S):
    b = ellipse(10.5, 12, 7.8, 3.8)
    t = poly([(17.5, 12), (21.8, 8.2), (21.8, 15.8)], closed=True, r=L(S, 0, 0.9))
    d = poly([(9, 8.6), (11.4, 6), (13, 8.8)], closed=True, r=L(S, 0, 0.5))
    a = poly([(10, 15.4), (12, 17.6), (13.5, 15.2)], closed=True, r=L(S, 0, 0.5))
    return [shell(union(b, t, d, a)), detail("M7.5 13H16"), dot(5.6, 10.8, 0.8)]


@icon("arowana", CAT, "Side view of a long flat fish with large scales, an upturned mouth and two chin barbels",
      tags=["dragon fish", "silver arowana", "aquarium", "freshwater", "predator", "pet fish"])
def _(S):
    b = "M2.5 9.6C3.5 8.4 7 8 11 8C15 8 18 9.4 19.5 11.5L19.5 12.8C18 14.8 15 16 11 16C7 16 4.5 14.8 3.5 13.4Z"
    t = poly([(19, 11.2), (22, 9.4), (22, 14.6), (19, 13)], closed=True, r=L(S, 0, 0.8))
    fn = poly([(14.5, 8.2), (17.4, 8.6), (17.4, 10)], closed=True, r=L(S, 0, 0.4))
    return [shell(union(b, t, fn)), line("M3.8 14.2C2.8 15.6 2.9 17.4 4 18.8"), line("M5.6 15C5.2 16.8 5.8 18.4 7 19.4"),
            detail("M8.6 10.4C9.6 11.4 9.6 12.8 8.6 13.8"), detail("M12 10.2C13 11.4 13 12.8 12 13.9"), dot(5.6, 10.8, 0.8)]


@icon("hagfish", CAT, "Side view of an eel like fish with a blunt head fringed by short barbels and slime drips below",
      tags=["slime eel", "jawless fish", "deep sea", "scavenger", "slime", "primitive fish"])
def _(S):
    def c(t):
        return (6.5 + 14.5 * t, 11 + 2.2 * math.sin(t * 2 * math.pi))

    def w(t):
        return 4.6 - 2.8 * t
    b = poly(tube(c, w, 36), closed=True, r=0)
    hd = ellipse(6.4, 11, 2.7, 2.4)
    return [shell(union(b, hd)), dot(6.8, 10.4, 0.8), line("M3.9 10L2.3 8.4"), line("M3.7 11.4H2"), line("M4 12.8L2.6 14.4"),
            dot(8.5, 18, 1.1), dot(13, 20, 1.1), dot(17.5, 18, 1.1)]


@icon("frilled-shark", CAT, "Side view of an eel shaped shark with frilly ruffled gill slits behind its head",
      tags=["living fossil", "deep sea shark", "eel shark", "prehistoric", "gills", "rare"])
def _(S):
    def c(t):
        return (4 + 15 * t, 12 + 1.4 * math.sin(t * 2 * math.pi))

    def w(t):
        return 4.2 - 2.6 * t
    b = poly(tube(c, w, 36), closed=True, r=0)
    snout = poly([(2, 12.2), (4.8, 10), (4.8, 14)], closed=True, r=L(S, 0, 0.8))
    tail = poly([(18.5, 12.2), (22, 8.4), (21, 12.4), (22, 16.4)], closed=True, r=L(S, 0, 0.8))
    return [shell(union(b, snout, tail)), dot(5, 11.2, 0.8), detail("M8 9.4C7 10.6 9 11.2 8 12.2C7 13.2 9 13.8 8 14.8"),
            detail("M10.8 9.8C9.8 11 11.8 11.6 10.8 12.6C9.8 13.6 11.8 14.2 10.8 15.2")]


@icon("marine-flatworm", CAT, "Top view of a thin flat oval worm with ruffled wavy edges and two ear like flaps at the front",
      tags=["sea worm", "nudibranch lookalike", "reef", "invertebrate", "polyclad", "ruffled"])
def _(S):
    pts = []
    n = 44
    for i in range(n):
        a = 2 * math.pi * i / n
        w_ = 1 + 0.1 * math.sin(a * 9)
        pts.append((13 + 8.6 * w_ * math.cos(a), 13 + 4.6 * w_ * math.sin(a)))
    ears = [poly([(6.6, 10), (4.4, 5), (8.8, 8.2)], closed=True, r=L(S, 0, 0.6)), poly([(6.6, 16), (4.4, 21), (8.8, 17.8)], closed=True, r=L(S, 0, 0.6))]
    return [shell(union(poly(pts, closed=True), *ears)), detail("M10 13H20")]


@icon("salp-chain", CAT, "Chain of linked transparent barrel shaped bodies each with a small dark spot",
      tags=["tunicate", "plankton", "gelatinous", "colony", "sea squirt relative", "zooplankton"])
def _(S):
    out = []
    for i, x in enumerate((2.5, 9.8, 17.1)):
        out.append(shell(rect(x, 8.5, 4.4, 7, L(S, 1.2, 2.2))))
        out.append(mark(circle(x + 2.2, 12, 0.8)))
    out += [line(seg(6.9, 12, 9.8, 12)), line(seg(14.2, 12, 17.1, 12))]
    return out


@icon("cuttlebone", CAT, "Flat oval chalky bone with a thick rim and fine curved growth lines across it",
      tags=["cuttlefish bone", "bird supplement", "calcium", "squid", "beach find", "shell"])
def _(S):
    if S.name == "line":
        d = "M12 2.5C17 3.5 18.5 9 18.5 13C18.5 17 15.5 20 12 22C8.5 20 5.5 17 5.5 13C5.5 9 7 3.5 12 2.5Z"
    else:
        d = "M12 2.5C17 3.5 18.5 9 18.5 13C18.5 18 15.5 21.5 12 21.5C8.5 21.5 5.5 18 5.5 13C5.5 9 7 3.5 12 2.5Z"
    return [shell(d), detail("M8 8.5C10.5 10 13.5 10 16 8.5"), detail("M8 12.5C10.5 14 13.5 14 16 12.5"), detail("M9 16.4C11 17.4 13 17.4 15 16.4")]


@icon("aquarium-castle", CAT, "Small ornamental castle with two pointed towers and an arched doorway, with bubbles rising",
      tags=["tank decoration", "ornament", "fish tank castle", "aquascape", "decor", "fishkeeping"])
def _(S):
    parts = [rect(3, 11, 5.5, 10, 0), rect(15.5, 11, 5.5, 10, 0), rect(8, 10, 8, 11, 0),
             poly([(2.5, 11), (5.75, 5.8), (9, 11)], closed=True), poly([(15, 11), (18.25, 5.8), (21.5, 11)], closed=True)]
    return [shell(poly_path_union(parts)), detail("M10.6 21V16.8A1.4 1.4 0 0 1 13.4 16.8V21"), dot(12.2, 6.2, 1.1), dot(13.8, 3.2, 0.9)]


@icon("koi-pond", CAT, "Top view of a curved garden pond edged with stones and two koi swimming in a circle",
      tags=["garden pond", "fish pond", "water garden", "japanese garden", "koi carp", "landscaping"])
def _(S):
    k, ph = L(S, (3, 0.5), (2, 0.2))
    pond = [(12 + (8 + 0.6 * math.cos(k * a + ph)) * math.cos(a), 12 + (6 + 0.5 * math.cos(k * a + ph)) * math.sin(a))
            for a in (2 * math.pi * i / 36 for i in range(36))]
    out = [shell(poly(pond, closed=True)), small_fish(9.4, 11, 5.4, 3, 12, flip=True), small_fish(14.8, 13.4, 5.4, 3, 12)]
    for i in range(12):
        a = math.radians(i * 30 + 15)
        out.append(dot(12 + 10.4 * math.cos(a), 12 + 8.5 * math.sin(a), 1))
    return out


@icon("aquarium-tunnel", CAT, "Arched glass tunnel seen from the front with fish swimming overhead",
      tags=["public aquarium", "walkthrough", "ocean tunnel", "sea life centre", "zoo", "attraction"])
def _(S):
    R = L(S, 9, 6.5)
    d = f"M3 21V{f(3 + R)}A{f(R)} {f(R)} 0 0 1 {f(3 + R)} 3H{f(21 - R)}A{f(R)} {f(R)} 0 0 1 21 {f(3 + R)}V21Z"
    return [shell(d), mark(fish_d(9.2, 9.4, 5.6, 3.2)), mark(fish_d(15.4, 13.6, 5.6, 3.2, 0, True))]


@icon("beached-whale", CAT, "Whale lying stranded on the sand with the waves far behind it",
      tags=["stranding", "stranded whale", "marine mammal rescue", "beach", "washed up", "conservation"])
def _(S):
    return [line(seg(2, 21.5, 22, 21.5)), shell(whale_d(S, 10.5, 16.7, 1, 0.5, 0)), dot(6.8, 16, 0.9),
            line(water(2, 9, 5, 0.9, 2))]


@icon("blue-carbon", CAT, "Seagrass growing from the seabed with a downward arrow carrying a carbon bubble into its roots",
      tags=["carbon storage", "seagrass", "mangroves", "carbon sink", "climate", "coastal habitat"])
def _(S):
    out = [line(seg(2, 16, 22, 16))]
    for x, h in ((5, 11), (9, 8), (13, 10)):
        out.append(line(f"M{f(x)} 16C{f(x - 2.4)} {f(16 - h * 0.35)} {f(x + 2.4)} {f(16 - h * 0.65)} {f(x)} {f(16 - h)}"))
    out += [shell(circle(19.2, 5.8, 3.2) if S.name == "rounded" else poly(regular(19.2, 5.8, 3.2, 10, -90), closed=True)),
            line(seg(19.2, 10.4, 19.2, 18.6)), head(S, (19.2, 20.6), (0, 1), 2.6)]
    return out


@icon("ocean-dead-zone", CAT, "Empty water below a wavy surface with a fish skeleton lying on the seabed",
      tags=["hypoxia", "low oxygen", "algal bloom", "eutrophication", "lifeless sea", "pollution"])
def _(S):
    out = [line(water(2, 22, 3.8, 0.9, 3)), line(seg(2, 21.5, 22, 21.5)), shell(ellipse(5.8, 15.8, 3.4, 2.8)), dot(5, 15.2, 0.7),
           line("M9.4 15.8H16.4"), shell(poly([(16.4, 15.8), (20.8, 11.8), (20.8, 19.4)], closed=True, r=L(S, 0, 0.9)))]
    for x in (11.4, 13.8):
        out.append(line(f"M{f(x)} 15.8L{f(x + 1.2)} 12.6"))
        out.append(line(f"M{f(x)} 15.8L{f(x + 1.2)} 19"))
    return out


@icon("whale-and-calf", CAT, "Large whale swimming with a small calf close beside and slightly above it",
      tags=["mother and baby", "humpback", "marine mammal", "family", "nursery", "migration"])
def _(S):
    return [shell(whale_d(S, 10.5, 16.8, 0.8, 0.2, 1.0)), dot(5.9, 17.2, 0.85),
            shell(whale_d(S, 10.5, 16.8, 0.42, -3.2, -8.4)), dot(7.9, 8.9, 0.6)]


@icon("jellyfish-bloom", CAT, "Crowd of several small jellyfish drifting together at different heights",
      tags=["jellyfish swarm", "smack of jellyfish", "plankton bloom", "sea", "stinging", "marine"])
def _(S):
    return jelly(S, 6.8, 6.5, 3.4, 4) + jelly(S, 17.2, 8.5, 3.4, 4) + jelly(S, 11.8, 16.2, 3.6, 4)


def crab_bits(S, cx, cy, sc=1.0):
    """Crab seen from above: returns body ellipse path and leg/claw strokes."""
    return None


@icon("crab-molt", CAT, "Soft new crab backing out of its empty old shell, which stays behind with an open split at its rear",
      tags=["moulting", "shedding", "exoskeleton", "growth", "soft shell crab", "crustacean"])
def _(S):
    d1, _p1, _t1 = ea(7.5, 7.8, 4.6, 3.4, 75, 375)
    return [line(d1), line("M3.4 6.2L2.4 3.6"), line("M11.6 6.2L12.6 3.6"), line("M3 9.2L2 11.2"), line("M5.2 10.8L4.4 12.8"),
            shell(ellipse(16, 16.2, 4.6, 3.4)), mark(circle(11.4, 11.8, 1.7)), mark(circle(20.6, 11.8, 1.7)),
            line("M12.4 14.6L11.4 12.8"), line("M19.6 14.6L20.6 12.8"), line("M12.8 18.4L11 20.4"), line("M19.2 18.4L21 20.4"), dot(14.6, 15.4, 0.7), dot(17.4, 15.4, 0.7)]