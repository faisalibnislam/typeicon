"""TypeIcon Core: landscape (batch 001).

Landforms, coasts, rivers and the sea floor. Scenes are drawn in side view on a ground or water line
near y 20, or as a top view (map) where the plan asks for one. Water is always a gentle wave line;
rock and land masses are shells, so Filled turns them solid. Objects seen behind another are cut with
a 2 px gap, and those icons get an explicit Filled design.
"""
import math

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


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def region(d, miter=4.0):
    """Area covered by a closed outline filled to its outer stroke edge."""
    return U(P(d), ST(d, 2, "butt", "miter", miter))


def grow(p, g):
    """Path region p expanded by g px."""
    return U(p, ST(path_to_d(p), 2 * g, "round", "round"))


def cut_strokes(S, ds, cutter, gap=2.0):
    """Stroke outlines of ds (in style S) with grow(cutter, gap) removed, for things seen behind another."""
    body = U(*[ST(d, 2, S.cap, S.join) for d in ds])
    return solid(path_to_d(D(body, grow(cutter, gap))))


def wave(x0, x1, y, amp=0.6, n=4):
    """Horizontal wave line from x0 to x1 with n half-waves (amp = peak height in px)."""
    w = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        sgn = -1 if i % 2 == 0 else 1
        d += f"Q{fmt(x0 + w * (i + 0.5))} {fmt(y + sgn * amp * 2)} {fmt(x0 + w * (i + 1))} {fmt(y)}"
    return d


def xat(p0, p1, y):
    """x on the segment p0-p1 at height y."""
    (x0, y0), (x1, y1) = p0, p1
    return x0 + (x1 - x0) * (y - y0) / (y1 - y0)


def heavy(d):
    return ST(d, 2.5, "butt", "miter")


# ============================================================================ mountains and rock

_PASS = [(2, 20), (2, 13), (7, 4.5), (12, 11.5), (17, 6), (22, 13), (22, 20)]


@icon("mountain-pass", CAT, "Two mountains meeting at a low saddle with a winding road climbing through it",
      tags=["pass", "col", "saddle", "mountain road", "crossing", "gap"])
def _(S):
    return [shell(poly(_PASS, closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
            detail("M8.5 20C8.5 17.5 15 17.5 15 15.5C15 14 12 14 12 11.5")]


_RIDGE = [(2, 20), (2, 14.5), (5, 9.5), (7.5, 13), (11, 5.5), (14, 11), (16.5, 8), (19.5, 12.5), (22, 9.5), (22, 20)]


@icon("mountain-ridge", CAT, "Long jagged ridgeline of sawtooth crests over a flat base",
      tags=["ridgeline", "crest", "arete", "sierra", "summits", "skyline"])
def _(S):
    return [shell(poly(_RIDGE, closed=True, r=S.r * 0.6), stroke_miterlimit="2")]


_HILL_F = "M2 20C2.5 14.5 6 12.5 9.5 12.5C13 12.5 16 15 17 20Z"
_HILL_B = "M9 20C10 12 14.5 7.5 17.5 7.5C20.5 7.5 21.5 13 22 20Z"


def _hills_filled():
    f = region(_HILL_F)
    return U(f, D(region(_HILL_B), grow(f, 2)))


@icon("rolling-hills", CAT, "Smooth rounded hills, one behind the other, above flat ground",
      tags=["hills", "countryside", "downs", "hillside", "green hills", "rural"], filled=_hills_filled)
def _(S):
    return [shell(_HILL_F), cut_strokes(S, [_HILL_B], P(_HILL_F))]


_MESA = [(2, 20), (5, 13), (5.5, 7.5), (18.5, 7.5), (19, 13), (22, 20)]


@icon("mesa", CAT, "Wide flat-topped rock formation with steep sides and banded layers",
      tags=["table mountain", "tableland", "desert rock", "southwest", "flat top", "strata"])
def _(S):
    y = 16.5
    return [shell(poly(_MESA, closed=True, r=S.r * 0.6)), detail(seg(5, 13, 19, 13)),
            detail(seg(xat((5, 13), (2, 20), y), y, xat((19, 13), (22, 20), y), y))]


_BUTTE = [(6.5, 20), (8.5, 15), (9, 4.5), (15, 4.5), (15.5, 15), (17.5, 20)]


@icon("butte", CAT, "Narrow flat-topped rock tower standing alone on flat ground",
      tags=["rock tower", "pillar rock", "desert", "monument", "flat top", "southwest"])
def _(S):
    return [shell(poly(_BUTTE, closed=True, r=S.r * 0.6)), detail(seg(8.5, 15, 15.5, 15)), detail(seg(9, 10, 15, 10)),
            line(seg(2, 20, 4.5, 20)), line(seg(19.5, 20, 22, 20))]


def _hoodoo(S):
    cap = rect(6, 3.5, 12, 4.5, L(S, 1, 2))
    stem = poly([(10.5, 7), (9.5, 10), (10.5, 13), (8.5, 20), (15.5, 20), (13.5, 13), (14.5, 10), (13.5, 7)], closed=True, r=S.r * 0.6)
    return union(cap, stem)


@icon("hoodoo", CAT, "Thin stacked rock pillar balancing a wider cap stone",
      tags=["rock pillar", "fairy chimney", "tent rock", "earth pyramid", "erosion", "canyon"])
def _(S):
    return [shell(_hoodoo(S)), detail(seg(10.8, 13, 13.2, 13)),
            line(seg(2, 20, 6, 20)), line(seg(18, 20, 22, 20))]


_ARCH_OUT = [(4.5, 17.5), (5, 12), (4.5, 8.5), (7, 5), (11, 3.5), (15.5, 4), (18.5, 6), (19.5, 9.5), (19, 12.5), (19.5, 17.5)]
_ARCH_IN = "M9 17.5V13C9 10.5 10.3 8.5 12.2 8.5C14 8.5 15 10.2 15 13V17.5Z"


@icon("natural-arch", CAT, "Rock arch framing an open window of sky above a rock ledge",
      tags=["rock arch", "stone arch", "arch", "desert", "erosion", "national park"])
def _(S):
    body = minus(union(poly(_ARCH_OUT, closed=True, r=S.r * 0.6), rect(2, 17, 20, 4, L(S, 0, 1.5))), _ARCH_IN)
    return [shell(body)]


_SEA_ARCH = [(3, 16), (4, 10), (7, 6), (13, 4.5), (18, 5.5), (21, 9.5), (20.5, 16)]
_SEA_ARCH_IN = "M8 18V14C8 11 10.5 9.5 13 9.5C15.5 9.5 16.5 11.5 16.5 14V18Z"


@icon("sea-arch", CAT, "Rock arch standing in the sea with waves running through its opening",
      tags=["sea arch", "rock arch", "coast", "erosion", "ocean", "cliff"])
def _(S):
    body = minus(poly(_SEA_ARCH, closed=True, r=S.r * 0.6), _SEA_ARCH_IN)
    return [shell(body), line(wave(2, 22, 19.8, 0.6, 6))]


_STACK = [(13, 16), (13.5, 10), (12.5, 7.5), (14.5, 4), (18, 4), (19, 8), (18, 11.5), (19, 16)]
_STACK_CLIFF = [(2, 7), (6.5, 7), (8, 10.5), (7, 13), (8.5, 16), (2, 16)]


@icon("sea-stack", CAT, "Lone rock column rising from the sea beside a cliff",
      tags=["stack", "rock pillar", "coast", "erosion", "ocean", "cliff"])
def _(S):
    return [shell(poly(_STACK, closed=True, r=S.r * 0.6)), shell(poly(_STACK_CLIFF, closed=True, r=S.r * 0.6)),
            line(wave(2, 22, 19.8, 0.6, 6))]


_CLIFF = [(2, 5), (13, 5), (13.5, 10), (12.5, 14.5), (14, 20), (2, 20)]


@icon("cliff", CAT, "Side view of a flat-topped rock face dropping sharply to the ground",
      tags=["cliff face", "precipice", "drop", "escarpment", "rock face", "edge"])
def _(S):
    return [shell(poly(_CLIFF, closed=True, r=S.r * 0.6)),
            detail(poly([(8.5, 8), (6.5, 11), (8.5, 13.5), (7, 16.5)], r=S.r * 0.5)),
            line(seg(17, 20, 22, 20))]


_SEA_CLIFF = [(2, 3.5), (10, 3.5), (10.5, 8), (9, 12), (10.5, 16.5), (9.5, 21.5), (2, 21.5)]


@icon("sea-cliff", CAT, "Tall rock face dropping straight into the waves",
      tags=["cliff", "coast", "shore", "sea", "ocean", "headland"])
def _(S):
    return [shell(poly(_SEA_CLIFF, closed=True, r=S.r * 0.6)),
            line(wave(14, 22, 9.5, 0.6, 2)), line(wave(14, 22, 14.5, 0.6, 2)), line(wave(14, 22, 19.5, 0.6, 2))]


_FJORD_L = [(2, 17.5), (2, 9), (7, 3.5), (9.5, 17.5)]
_FJORD_R = [(22, 17.5), (22, 10.5), (17, 5.5), (14.5, 17.5)]


@icon("fjord", CAT, "Narrow sea inlet between two steep mountain walls",
      tags=["inlet", "sound", "norway", "glacial valley", "sea", "mountains"])
def _(S):
    return [shell(poly(_FJORD_L, closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
            shell(poly(_FJORD_R, closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
            line(wave(10.5, 13.5, 14, 0.4, 2)), line(wave(2, 22, 20.5, 0.6, 6))]


def _valley(S, floor):
    pts = [(2, 20), (2, 8), (4.5, 4.5), (7, 7.5)]
    right = [(17, 7.5), (19.5, 4.5), (22, 8), (22, 20)]
    return "M" + poly(pts, r=S.r * 0.6)[1:] + floor + poly(right, r=S.r * 0.6)[len("M17 7.5"):] + "Z"


@icon("u-shaped-valley", CAT, "Cross section of a broad U-shaped glacial valley with a river at its floor",
      tags=["glacial valley", "trough", "valley", "glacier", "geography", "cross section"])
def _(S):
    return [shell(_valley(S, "C7 14 8.5 16 12 16C15.5 16 17 14 17 7.5")), Part("dot", "M9.5 16A2.5 2 0 0 0 14.5 16Z")]


@icon("v-shaped-valley", CAT, "Cross section of a steep V-shaped river valley",
      tags=["river valley", "ravine", "valley", "erosion", "geography", "cross section"])
def _(S):
    return [shell(_valley(S, "L10.5 16H13.5L17 7.5"), stroke_miterlimit="2"), Part("dot", "M9.5 16A2.5 2 0 0 0 14.5 16Z")]


# ============================================================================ dry lands, grasslands and forests

def clip_h(pts, y, inset=0.0):
    """Horizontal detail lines at height y inside the closed polygon pts (one per piece)."""
    xs = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        if (y0 - y) * (y1 - y) < 0:
            xs.append(x0 + (x1 - x0) * (y - y0) / (y1 - y0))
    xs.sort()
    return [seg(xs[i] + inset, y, xs[i + 1] - inset, y) for i in range(0, len(xs) - 1, 2) if xs[i + 1] - xs[i] - 2 * inset > 1.5]


def leaf_shape(x1, y1, x2, y2, bulge):
    """Pointed leaf from (x1, y1) to (x2, y2), each half bowing out by about bulge px."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    b = bulge * 2
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx * b)} {fmt(my + ny * b)} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(mx - nx * b)} {fmt(my - ny * b)} {fmt(x1)} {fmt(y1)}Z")


def palm(x, y, s=1.0, base=None):
    """Small palm: crown at (x, y), fronds of size s, trunk curving down to base."""
    k = s
    parts = [line(f"M{fmt(x)} {fmt(y)}C{fmt(x - 1.5 * k)} {fmt(y - 2.2 * k)} {fmt(x - 4 * k)} {fmt(y - 2.2 * k)} {fmt(x - 5.5 * k)} {fmt(y - 0.5 * k)}"),
             line(f"M{fmt(x)} {fmt(y)}C{fmt(x + 1.5 * k)} {fmt(y - 2.2 * k)} {fmt(x + 4 * k)} {fmt(y - 2.2 * k)} {fmt(x + 5.5 * k)} {fmt(y - 0.5 * k)}"),
             line(f"M{fmt(x)} {fmt(y)}C{fmt(x - 2.5 * k)} {fmt(y)} {fmt(x - 4 * k)} {fmt(y + 1.2 * k)} {fmt(x - 4.5 * k)} {fmt(y + 3 * k)}"),
             line(f"M{fmt(x)} {fmt(y)}C{fmt(x + 2.5 * k)} {fmt(y)} {fmt(x + 4 * k)} {fmt(y + 1.2 * k)} {fmt(x + 4.5 * k)} {fmt(y + 3 * k)}")]
    if base:
        bx, by = base
        parts.append(line(f"M{fmt(x)} {fmt(y)}C{fmt(x + 0.8)} {fmt((y + by) / 2)} {fmt(bx)} {fmt(by - 3)} {fmt(bx)} {fmt(by)}"))
    return parts


_DUNE = "M2 20C5 15.5 9 10 13 10C15.5 10 18 13 22 20Z"


@icon("sand-dune", CAT, "Sand dune with a sharp crest dividing its two slopes",
      tags=["dunes", "sand", "desert", "sahara", "erg", "wind"])
def _(S):
    return [shell(_DUNE), detail("M13 10C14 13.5 13.5 17 11.5 20"), line("M2 7.5C4 6.3 6 6.3 8 7.5") ]


@icon("oasis", CAT, "Palm tree beside a small pool among low sand dunes",
      tags=["desert spring", "palm", "water", "desert", "sahara", "refuge"])
def _(S):
    return [*palm(7.5, 7, 1.0, (8.5, 18.5)), shell(ellipse(16, 17, 5.5, 3)),
            line("M2 20.5C3.5 19.3 5.5 18.6 8.5 18.6"), line("M13 10.5C15.5 8.8 18.5 8.3 22 9")]


_BADLANDS = [(2, 20), (4, 12.5), (5.5, 8.5), (7.5, 8.5), (9, 12), (10.5, 14.5), (12, 9.5), (13.5, 5), (16, 4.5), (17.5, 8), (19.5, 13), (22, 20)]


@icon("badlands", CAT, "Eroded striped hills cut by sharp gullies",
      tags=["eroded hills", "gullies", "strata", "desert", "erosion", "painted hills"])
def _(S):
    d = poly(_BADLANDS, closed=True, r=S.r * 0.6)
    return [shell(d, stroke_miterlimit="2"), *[detail(x) for x in clip_h(_BADLANDS, 12, 0.2)], *[detail(x) for x in clip_h(_BADLANDS, 16.5, 0.2)]]


def _honeycomb(S):
    """Honeycomb cracks: three zigzag rows of pointy-top hexagons joined by verticals."""
    w, a = 10, 1.2
    ds = []
    rows = (9, 15, 21)
    for k, y in enumerate(rows):
        off = 0 if k % 2 == 0 else w / 2
        pts = []
        x = 2 - (w / 2 if k % 2 else 0)
        i = 0
        while x <= 22.01:
            pts.append((x, y - a if (i % 2 == 0) == (k % 2 == 0) else y + a))
            x += w / 2
            i += 1
        pts = [(max(2, min(22, px)), py) for px, py in pts]
        ds.append(poly(pts, r=S.r * 0.4))
    for k in range(2):
        y0, y1 = rows[k] + a, rows[k + 1] - a
        xs = [2 + w * j for j in range(3)] if k == 0 else [2 + w / 2 + w * j for j in range(2)]
        ds += [seg(x, y0, x, y1) for x in xs]
    return ds


@icon("salt-flat", CAT, "Flat salt pan cracked into a honeycomb pattern below a low horizon",
      tags=["salt pan", "salt lake", "playa", "dry lake", "desert", "crust"])
def _(S):
    return [line(seg(2, 4.5, 22, 4.5)), *[line(d) for d in _honeycomb(S)]]


@icon("savanna", CAT, "Flat-topped acacia tree over a grassy plain",
      tags=["savannah", "acacia", "grassland", "africa", "safari", "plain"])
def _(S):
    crown = L(S, "M3.5 9L6 5.5H18L20.5 9Z", "M5 9A1.5 1.5 0 0 1 3.8 6.6L4.8 5.5H19.2L20.2 6.6A1.5 1.5 0 0 1 19 9Z")
    return [shell(crown), line(poly([(12, 20), (12, 15), (8.5, 11)], r=S.r)), line(seg(12, 15, 15.5, 11)),
            line(seg(2, 20, 22, 20)), line(poly([(3.5, 16), (4.5, 18), (5.5, 16)], r=S.r * 0.3)),
            line(poly([(17.5, 16), (18.5, 18), (19.5, 16)], r=S.r * 0.3))]


@icon("prairie", CAT, "Tall wavy grass blades in front of a wide flat horizon",
      tags=["grassland", "plains", "steppe", "pampas", "tall grass", "great plains"])
def _(S):
    blades = ["M4 21C4 17 5 14 7.5 11.5", "M8 21C8 16.5 8.5 12.5 7 8.5", "M12 21C12 16.5 13 13 15.5 10",
              "M16.5 21C16.5 16.5 17.5 13.5 20 11"]
    return [line(seg(2, 5, 22, 5)), *[line(b) for b in blades]]


@icon("meadow", CAT, "Gently rolling ground dotted with small flowers and grass",
      tags=["field", "wildflowers", "grassland", "pasture", "spring", "countryside"])
def _(S):
    return [line("M2 19C6 16.5 10 16.5 13 18C16 19.5 19 19.5 22 17.5"),
            shell(circle(7, 7.5, 2.5)), line(seg(7, 10, 7, 16.5)),
            shell(circle(16.5, 9.5, 2.5)), line(seg(16.5, 12, 16.5, 17.8)),
            line(poly([(10.5, 13.5), (11.5, 16.5), (12.5, 13.5)], r=S.r * 0.3))]


@icon("jungle", CAT, "Dense tropical foliage with broad leaves and a hanging vine",
      tags=["rainforest", "tropical forest", "tropics", "foliage", "wild", "amazon"])
def _(S):
    return [line("M4 2.5C4 7 5 10 3.5 14"), shell(leaf_shape(4.2, 7.5, 8.5, 9.5, 1.0)),
            shell(leaf_shape(12, 21, 5, 13.5, 2.3)), shell(leaf_shape(12, 21, 20.5, 11, 2.6)),
            shell(leaf_shape(12.5, 16, 14, 4, 2.2))]


@icon("mangrove", CAT, "Mangrove tree on arching stilt roots standing in water",
      tags=["mangroves", "swamp tree", "coast", "wetland", "tropical", "roots"])
def _(S):
    crown = union(circle(7.5, 8, 3.5), circle(12, 6.5, 4.5), circle(16.5, 8, 3.5), rect(7.5, 7, 9, 4.5))
    return [shell(crown), line(seg(12, 11.5, 12, 13)),
            line("M12 13C7 13 4.5 15 4 19"), line("M12 13C10 13.8 9 16 9 19"),
            line("M12 13C14 13.8 15 16 15 19"), line("M12 13C17 13 19.5 15 20 19"),
            line(wave(2, 22, 21.5, 0.5, 6))]


# ============================================================================ coasts and islands (top views)

@icon("peninsula", CAT, "Map view of a tongue of land reaching into the sea",
      tags=["cape", "promontory", "land", "coast", "map", "geography"])
def _(S):
    land = "M2 2V22H6.5C6.5 18 9 16 13 15.5C17.5 15 21 14 21 12C21 10 17.5 9 13 8.5C9 8 6.5 6 6.5 2Z"
    return [shell(land), line(wave(11, 17, 4.5, 0.5, 2)), line(wave(11, 17, 19.5, 0.5, 2))]


_ISTH_A = [(2.5, 8), (4.5, 3.5), (9.5, 2.5), (12.5, 5), (11.5, 9), (8, 11.5), (4, 11.5)]
_ISTH_B = [(12, 15), (15.5, 12.5), (20, 13), (21.5, 17), (19, 21), (14, 21.5), (11.5, 18.5)]


_ISTH_A = [(2.5, 8), (4.5, 3.5), (9.5, 2.5), (12.5, 5), (11.5, 9), (8, 11.5), (4, 11.5)]
_ISTH_B = [(12, 15), (15.5, 12.5), (20, 13), (21.5, 17), (19, 21), (14, 21.5), (11.5, 18.5)]


@icon("isthmus", CAT, "Map view of two landmasses joined by a narrow strip of land with sea on either side",
      tags=["land bridge", "neck", "strip", "coast", "map", "geography", "panama"])
def _(S):
    neck = path_to_d(ST("M9 9C11 10.5 12.5 12 14 14.5", 4, "round", "round"))
    land = union(poly(_ISTH_A, closed=True, r=S.r * 0.8), poly(_ISTH_B, closed=True, r=S.r * 0.8), neck)
    return [shell(land), line(wave(16, 21, 6, 0.5, 2)), line(wave(3, 8, 17.5, 0.5, 2))]


@icon("archipelago", CAT, "Map view of a scattered chain of small islands",
      tags=["islands", "island chain", "isles", "ocean", "map", "geography"])
def _(S):
    big = poly([(2.5, 17), (4, 13.5), (7, 12.5), (9, 13.5), (10.5, 16.5), (9, 20), (5, 20.5)], closed=True, r=S.r * 0.8 + 0.4)
    mid = poly([(13, 8.5), (15, 5), (18, 4.5), (21, 6.5), (20.5, 9.5), (17.5, 11), (14.5, 11.5)], closed=True, r=S.r * 0.8 + 0.4)
    return [shell(big), shell(mid), shell(circle(15, 17, 2)), dot(6.5, 6.5, 1.5), dot(20, 15.5, 1.3), dot(10.5, 8.5, 1.2)]


@icon("atoll", CAT, "Map view of a ring of small coral islets around a central lagoon",
      tags=["coral island", "ring island", "lagoon", "pacific", "reef", "tropical"])
def _(S):
    def islet(a0, a1):
        return shell(path_to_d(ST(arc(12, 12, 7.5, a0, a1), 4, S.cap, S.join)))
    return [islet(-70, 10), islet(35, 115), islet(145, 195), islet(215, 255), line(wave(9.5, 14.5, 12, 0.5, 2))]


# ============================================================================ chunk 3: plateaus, coasts, wetlands, rivers

_PLATEAU = [(2, 20), (2, 15), (8, 15), (11.5, 7.5), (22, 7.5), (22, 20)]


@icon("plateau", CAT, "Raised flat tableland with one sloping edge descending to a lower plain",
      tags=["tableland", "highland", "upland", "high plain", "escarpment", "geography"])
def _(S):
    y = 12
    x0 = xat((8, 15), (11.5, 7.5), y)
    return [shell(poly(_PLATEAU, closed=True, r=S.r * 0.6)), detail(seg(x0, y, 22, y))]


@icon("tundra", CAT, "Flat frozen plain with a low sun on the horizon, grass tufts and a patch of snow",
      tags=["arctic", "polar", "permafrost", "frozen plain", "taiga", "cold"])
def _(S):
    return [line("M7.5 11A4.5 4.5 0 0 1 16.5 11"), line(seg(2, 11, 22, 11)),
            shell("M2.5 20C3.5 14.5 10 14.5 11 20Z"), shell("M14 20C14.5 16.5 18 16.5 19 20Z")]


@icon("lagoon", CAT, "Calm shallow water sheltered behind a curved sandbar with a palm tree",
      tags=["sandbar", "shallow water", "tropical", "palm", "reef", "atoll"])
def _(S):
    return [*palm(16, 7, 0.9, (16.5, 14.5)),
            line("M8 15C11 13 20 13 22 15"),
            line(wave(2, 22, 18.5, 0.6, 6)), line(wave(2, 22, 21.5, 0.6, 6))]


@icon("bay", CAT, "Map view of a rounded body of sea curving into the coastline",
      tags=["gulf", "cove", "inlet", "coast", "sea", "shoreline", "map"])
def _(S):
    land = minus(rect(2, 2, 20, 20, L(S, 1, 3)), circle(22, 12, 8.5))
    return [shell(land), line(wave(17, 22, 9.5, 0.5, 2)), line(wave(17, 22, 14.5, 0.5, 2))]


@icon("sandbar", CAT, "Low sand ridge breaking the water surface between wave lines",
      tags=["shoal", "sand bank", "shallows", "spit", "river", "coast"])
def _(S):
    return [line(wave(2, 22, 6.5, 0.6, 6)), shell("M3 15.5C6 11 18 11 21 15.5Z"), line(wave(2, 22, 20, 0.6, 6))]


def _star(cx, cy, ro, ri):
    pts = []
    for i in range(10):
        a = -90 + 36 * i
        pts.append(polar(cx, cy, ro if i % 2 == 0 else ri, a))
    return poly(pts, closed=True)


@icon("tide-pool", CAT, "Rocky basin of seawater holding a starfish",
      tags=["rock pool", "starfish", "shore", "intertidal", "sea life", "coast"])
def _(S):
    rocks = "M2 21V9.5C2 6.5 5.5 6 6.5 8.5L8 11H16L17.5 8.5C18.5 6 22 6.5 22 9.5V21Z"
    return [shell(rocks, stroke_miterlimit="2") if S.name == "line" else shell(rocks), detail(wave(7, 17, 13.3, 0.5, 4)),
            Part("dot", _star(12, 17.2, 2.4, 1.0))]


@icon("mudflat", CAT, "Flat shore of soft mud with shallow water streaks and bird footprints",
      tags=["tidal flat", "wetland", "shore", "estuary", "mud", "wader"])
def _(S):
    def track(x, y):
        return line(poly([(x - 3, y - 3), (x, y), (x + 3, y - 3)], r=S.r * 0.3) + f"M{fmt(x)} {fmt(y - 3)}V{fmt(y + 3)}")
    return [line(wave(2, 22, 5, 0.6, 6)), line(wave(10, 22, 9.5, 0.5, 3)), track(7.5, 15.5), track(16.5, 19)]


@icon("marsh", CAT, "Cattails and reeds rising from flat water",
      tags=["wetland", "bulrush", "reeds", "fen", "cattail", "bog"])
def _(S):
    return [shell(rect(6, 3.5, 4, 7, 2)), line(seg(8, 10.5, 8, 18)),
            shell(rect(14, 6.5, 4, 7, 2)), line(seg(16, 13.5, 16, 18)),
            line("M3 18C3 14 4 11 5.5 8.5"), line("M21 18C21 15 20.5 12 19.5 9.5"),
            line(wave(2, 22, 20.5, 0.6, 6))]


@icon("swamp", CAT, "Bald cypress with a flared trunk standing in still water with hanging moss",
      tags=["bayou", "wetland", "bog", "cypress", "mangrove", "moss", "louisiana"])
def _(S):
    crown = union(circle(7.5, 7.5, 3.5), circle(12, 6, 4.5), circle(16.5, 7.5, 3.5), rect(7.5, 7, 9, 4))
    trunk = poly([(10.5, 10), (13.5, 10), (14, 14.5), (17, 19), (7, 19), (10, 14.5)], closed=True, r=S.r * 0.6)
    return [shell(union(crown, trunk)), line("M4.5 10.5C6 12 3.5 13.5 5 15.5"), line("M19.5 10.5C21 12 18.5 13.5 20 15.5"),
            line(wave(2, 22, 21.5, 0.5, 6))]


@icon("river-delta", CAT, "Map view of a river splitting into branching channels that fan out to the sea",
      tags=["distributaries", "river mouth", "channels", "nile", "sediment", "map"])
def _(S):
    return [line(seg(12, 2, 12, 6.5)), line(poly([(4, 17), (7, 11.5), (12, 6.5), (17, 11.5), (20, 17)], r=S.r)),
            line(poly([(9.5, 17), (7, 11.5)], r=S.r)), line(poly([(14.5, 17), (17, 11.5)], r=S.r)),
            line(wave(2, 22, 21, 0.6, 6))]


@icon("estuary", CAT, "Map view of a river widening into a funnel-shaped mouth that meets the sea",
      tags=["river mouth", "tidal river", "firth", "inlet", "sea", "map"])
def _(S):
    return [line("M8 2C8 11 7 15 2 18.5"), line("M16 2C16 11 17 15 22 18.5"),
            line(wave(2, 22, 21, 0.6, 6)), line(wave(8, 16, 12.5, 0.5, 2))]


@icon("river-meander", CAT, "Map view of a river looping in tight S-shaped bends",
      tags=["meandering river", "bends", "winding river", "stream", "curves", "map"])
def _(S):
    return [line("M2 6C8 1.5 13 5 13 9C13 13.5 6 13 6 17C6 21 13 22 22 17")]


@icon("oxbow-lake", CAT, "Map view of a crescent lake cut off beside a river",
      tags=["cutoff lake", "crescent lake", "river bend", "floodplain", "meander", "map"])
def _(S):
    return [shell("M11 3C0.5 6 0.5 18 11 21C5.5 16.5 5.5 7.5 11 3Z"), line("M17 2C14 8 20 14 17 22")]


# ============================================================================ chunk 4: rivers, lakes, terrain

@icon("river-rapids", CAT, "River water breaking into jagged white crests over rocks",
      tags=["white water", "rapids", "whitewater", "rafting", "stream", "rocks", "kayaking"])
def _(S):
    crest1 = poly([(2, 8), (5, 4.5), (8, 8), (11, 4.5), (14, 8), (17, 4.5), (20, 8), (22, 6)], r=S.r * 0.4)
    crest2 = poly([(2, 13.5), (5, 10), (8, 13.5), (11, 10), (14, 13.5), (17, 10), (20, 13.5), (22, 11.5)], r=S.r * 0.4)
    return [line(crest1), line(crest2), shell("M3 21C3.5 16.5 9 16.5 10 21Z"), shell("M13.5 21C14.5 17.5 19 17.5 20 21Z")]


@icon("cascade-falls", CAT, "Water stepping down a staircase of three rock ledges in short falls",
      tags=["cascade", "waterfall", "stepped falls", "rapids", "river", "rock ledges"])
def _(S):
    return [line(poly([(2, 4.5), (8, 4.5), (8, 10), (14, 10), (14, 15.5), (22, 15.5)], r=S.r * 0.4)),
            line("M11 4.5C12 6.2 10 7.8 11 9.5"), line("M17 10C18 11.7 16 13.3 17 15"),
            line(wave(2, 22, 20.5, 0.6, 6))]


@icon("plunge-pool", CAT, "Waterfall stream dropping into a round pool with splashes at the base",
      tags=["waterfall", "pool", "splash", "falls", "swimming hole", "river"])
def _(S):
    return [line(seg(2, 3.5, 10, 3.5)), line(seg(14, 3.5, 22, 3.5)),
            line(seg(10, 3.5, 10, 12)), line(seg(14, 3.5, 14, 12)),
            shell(ellipse(12, 18, 9, 3.5)),
            line("M8 13C6.5 12.5 5.5 11 5.5 9.5"), line("M16 13C17.5 12.5 18.5 11 18.5 9.5")]


@icon("natural-spring", CAT, "Water welling up in jets from a spring between two stones",
      tags=["spring", "freshwater", "source", "bubbling water", "well", "spa", "groundwater"])
def _(S):
    return [line(seg(12, 15, 12, 4.5)), line("M12 15C12 11 8 10 7.5 6"), line("M12 15C12 11 16 10 16.5 6"),
            dot(12, 2.6, 1.0), shell("M2 21C2 18 3.5 17 5.5 17C7.5 17 8.5 19 8.5 21Z"),
            shell("M15.5 21C15.5 18 17 17 19 17C21 17 22 19 22 21Z"), line(wave(9.5, 14.5, 19.5, 0.5, 2))]


@icon("river-confluence", CAT, "Map view of two rivers joining into one wider channel",
      tags=["tributary", "junction", "river junction", "merge", "meeting of rivers", "map"])
def _(S):
    y = "M2 2H8C8.5 5.5 11 7.5 12 8.5C13 7.5 15.5 5.5 16 2H22C22 8 15 9 15 14V22H9V14C9 9 2 8 2 2Z"
    return [shell(y)]


@icon("wadi", CAT, "Map view of a dry riverbed winding between banks with cracks and pebbles",
      tags=["dry riverbed", "arroyo", "dry wash", "desert", "ravine", "ephemeral stream"])
def _(S):
    return [line("M4 2C4 8 13 9 10 14C8.5 17 5 19 6 22"), line("M14 2C14 8 23 9 20 14C18.5 17 15 19 16 22"),
            dot(9, 6, 1.2), dot(14, 10.5, 1.2), dot(11.5, 18, 1.2), dot(9, 11, 1.0)]


def _spiral(cx, cy, n=4, step=2.0, r0=1.5):
    """Semicircle spiral (clockwise outward) from the centre: radii r0, r0+step, ..."""
    x = cx
    d = f"M{fmt(x)} {fmt(cy)}"
    for k in range(n):
        r = r0 + step * k
        top = (k % 2 == 0)
        x2 = x + 2 * r if k % 2 == 0 else x - 2 * r
        d += f"A{fmt(r)} {fmt(r)} 0 0 {1 if top else 1} {fmt(x2)} {fmt(cy)}"
        x = x2
    return d


@icon("whirlpool", CAT, "Top view of a water vortex spiralling in toward its centre",
      tags=["vortex", "maelstrom", "eddy", "swirl", "sea", "drain", "spiral"])
def _(S):
    return [line(_spiral(12.5, 10.5)), line(wave(2, 22, 21, 0.6, 6))]


@icon("floodplain", CAT, "Flat land beside a river with floodwater spilling over its banks",
      tags=["flood", "river flooding", "flooded field", "overflow", "wetland", "flat land"])
def _(S):
    return [line(poly([(2, 15), (7.5, 15), (9.5, 19.5), (14.5, 19.5), (16.5, 15), (22, 15)], r=S.r * 0.4)),
            line(wave(2, 22, 11, 0.6, 6)), line(wave(2, 22, 6.5, 0.6, 6))]


@icon("alpine-lake", CAT, "Still lake mirroring snowy mountain peaks above it",
      tags=["mountain lake", "reflection", "tarn", "peaks", "scenic", "water"])
def _(S):
    return [shell(poly([(2, 11), (8, 4), (12, 8.5), (15.5, 4.5), (22, 11)], closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
            line(seg(6, 15, 18, 15)), line(seg(9, 19, 15, 19))]


@icon("crater-lake", CAT, "Volcano cone with a round lake of water filling its crater",
      tags=["caldera lake", "volcano", "crater", "lake", "volcanic", "water"])
def _(S):
    return [shell(poly([(2, 20), (5, 7), (8.5, 12.5), (15.5, 12.5), (19, 7), (22, 20)], closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
            line(wave(9.5, 14.5, 9.3, 0.4, 2))]


@icon("rice-terraces", CAT, "Hillside cut into curved stepped terraces with water glints",
      tags=["terraces", "paddy", "rice paddies", "terraced fields", "hillside farming", "agriculture", "asia"])
def _(S):
    hill = "M2 20C6 20 7.5 5.5 12 5.5C16.5 5.5 18 20 22 20Z"
    def xl(y):
        # x on the left curve at height y (bisect the bezier)
        p0, p1, p2, p3 = (2, 20), (6, 20), (7.5, 5.5), (12, 5.5)
        lo, hi = 0.0, 1.0
        for _i in range(40):
            t = (lo + hi) / 2
            mt = 1 - t
            yy = mt**3 * p0[1] + 3 * mt * mt * t * p1[1] + 3 * mt * t * t * p2[1] + t**3 * p3[1]
            if yy > y:
                lo = t
            else:
                hi = t
        t = (lo + hi) / 2
        mt = 1 - t
        return mt**3 * p0[0] + 3 * mt * mt * t * p1[0] + 3 * mt * t * t * p2[0] + t**3 * p3[0]
    ds = []
    for y, sag in ((10.5, 1.5), (14.5, 1.8), (18, 0)):
        if sag == 0:
            continue
        a = xl(y)
        ds.append(detail(f"M{fmt(a)} {fmt(y)}Q12 {fmt(y + sag * 2)} {fmt(24 - a)} {fmt(y)}"))
    return [shell(hill), *ds]


@icon("farm-fields", CAT, "Patchwork of farm fields seen in perspective divided by boundary lines",
      tags=["farmland", "crops", "patchwork", "agriculture", "countryside", "plots", "field rows"])
def _(S):
    field = poly([(7, 4.5), (17, 4.5), (22, 20), (2, 20)], closed=True, r=S.r * 0.6)
    return [shell(field), detail(seg(xat((7, 4.5), (2, 20), 9.5), 9.5, xat((17, 4.5), (22, 20), 9.5), 9.5)),
            detail(seg(xat((7, 4.5), (2, 20), 14.5), 14.5, xat((17, 4.5), (22, 20), 14.5), 14.5)),
            detail(seg(12, 4.5, 12, 20))]


@icon("scree-slope", CAT, "Steep mountain slope with loose stones fanning out at its foot",
      tags=["talus", "rockfall", "loose rock", "debris", "mountain slope", "stones"])
def _(S):
    return [shell(poly([(2, 20), (2, 8), (7, 4), (14, 20)], closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
            dot(15.5, 11.5, 1.4), dot(19, 14, 1.4), dot(17, 16.8, 1.5), dot(20.5, 18.5, 1.4), dot(14.5, 19, 1.2)]


_KARST_A = "M2 17L3.5 8C3.8 5 5.3 3.5 6.8 3.5C8.3 3.5 9.8 5 10 8L11.5 17Z"
_KARST_B = "M15.5 17L16 12C16.3 10 17.3 9 18.7 9C20.2 9 21.2 10 21.5 12L22 17Z"
_KARST_W = wave(2, 22, 20.5, 0.5, 6)


def _karst_filled():
    return U(region(_KARST_A), region(_KARST_B), heavy(_KARST_W))


@icon("karst-towers", CAT, "Tall rounded limestone pinnacles rising steeply from flat water",
      tags=["limestone towers", "pinnacles", "karst", "haystack hills", "halong", "guilin", "peaks"], filled=_karst_filled)
def _(S):
    return [shell(_KARST_A), shell(_KARST_B), line(_KARST_W)]


@icon("cenote", CAT, "Cross section of a round sinkhole with vines hanging down into its pool of water",
      tags=["sinkhole", "swimming hole", "yucatan", "cave pool", "limestone", "vines"])
def _(S):
    return [line(seg(2, 7, 7, 7)), line(seg(17, 7, 22, 7)),
            line(poly([(7, 7), (7, 13)], r=0) + "C7 17.5 9 20 12 20C15 20 17 17.5 17 13V7"),
            line("M10.5 7C11.5 8.7 9.5 10.3 10.5 12"), line("M13.8 7C14.8 8.4 12.8 9.6 13.8 11"),
            line(wave(9.5, 14.5, 16, 0.5, 2))]


def _rim():
    mult = [1.0, 0.92, 1.05, 0.95, 1.0, 0.9, 1.05, 0.95, 1.0, 0.92, 1.05, 0.95]
    return [(12 + 8.5 * m * math.cos(math.radians(30 * i)), 12.5 + 6 * m * math.sin(math.radians(30 * i))) for i, m in enumerate(mult)]


@icon("sinkhole", CAT, "Block of ground with a rough pit collapsed into it and stones falling in",
      tags=["collapse", "subsidence", "pit", "hole", "cave-in", "ground collapse", "karst"])
def _(S):
    pit = poly([(6.5, 6), (8, 10.5), (7.5, 15), (10, 19), (14, 19), (16.5, 15), (16, 10.5), (17.5, 6)], closed=True)
    ground = minus(rect(2, 6, 20, 14, L(S, 0, 2)), pit)
    return [shell(ground), dot(11, 10.5, 1.3), dot(13.5, 14, 1.3)]


_TEPUI = [(2, 20), (4, 16), (4, 7), (6, 4.5), (18, 4.5), (20, 7), (20, 16), (22, 20)]


@icon("tepui", CAT, "Steep-sided flat-topped table mountain with a thin waterfall off its edge",
      tags=["table mountain", "plateau", "venezuela", "waterfall", "sheer cliffs", "angel falls", "mesa"])
def _(S):
    return [shell(poly(_TEPUI, closed=True, r=S.r * 0.6), stroke_miterlimit="2"), detail("M14 5.5C15 8.5 13 11 14 14.5")]


# ============================================================================ chunk 5: sea floor, tides and coasts

@icon("ocean-trench", CAT, "Cross section of the sea floor with a deep narrow trench under the waves",
      tags=["deep sea", "marianas", "abyss", "seafloor", "subduction", "oceanography"])
def _(S):
    return [line(wave(2, 22, 4.5, 0.6, 6)),
            shell(poly([(2, 9), (8, 9), (10.5, 17), (13.5, 17), (16, 9), (22, 9), (22, 21), (2, 21)], closed=True, r=S.r * 0.6))]


@icon("seamount", CAT, "Underwater mountain cone rising from the sea floor far below the waves",
      tags=["underwater mountain", "guyot", "seabed", "ocean floor", "volcano", "oceanography"])
def _(S):
    return [line(wave(2, 22, 4.5, 0.6, 6)),
            shell(poly([(2, 18), (6, 18), (9.5, 10.5), (14.5, 10.5), (18, 18), (22, 18), (22, 21), (2, 21)], closed=True, r=S.r * 0.6))]


@icon("mid-ocean-ridge", CAT, "Cross section of the sea floor with a raised ridge split by a rift valley",
      tags=["rift", "spreading ridge", "plate boundary", "tectonics", "seafloor", "oceanography"])
def _(S):
    return [line(wave(2, 22, 4.5, 0.6, 6)),
            shell(poly([(2, 15), (6, 15), (8.5, 8.5), (10.5, 8.5), (12, 12.5), (13.5, 8.5), (15.5, 8.5), (18, 15), (22, 15), (22, 21), (2, 21)], closed=True, r=S.r * 0.6))]


@icon("hydrothermal-vent", CAT, "Chimney-shaped rock tower on the sea floor puffing a dark plume",
      tags=["black smoker", "deep sea vent", "chimney", "seafloor", "geothermal", "ocean"])
def _(S):
    plume = union(circle(11.5, 6, 2.2), circle(14, 4.3, 2), circle(12, 2.8, 1.6))
    return [solid(plume), shell(poly([(7, 20), (9.5, 10.5), (14.5, 10.5), (17, 20)], closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
            detail(seg(9.3, 15.5, 14.7, 15.5)), line(seg(2, 20, 4, 20)), line(seg(20, 20, 22, 20))]


@icon("continental-shelf", CAT, "Cross section of a coast with a shallow shelf dropping off a steep slope into deep water",
      tags=["continental slope", "shelf break", "coast", "seafloor", "oceanography", "deep water"])
def _(S):
    return [line(wave(7, 22, 5, 0.6, 5)),
            shell(poly([(2, 7), (5, 10), (11, 11), (15, 18), (22, 18), (22, 21), (2, 21)], closed=True, r=S.r * 0.6))]


@icon("coral-reef", CAT, "Branching coral and a fan coral on the sea floor with a small fish swimming above",
      tags=["reef", "coral", "fish", "snorkel", "diving", "marine life", "tropical sea"])
def _(S):
    fish = "M8.5 6.5C10 4 13.5 4 15 6.5C13.5 9 10 9 8.5 6.5Z"
    tail = poly([(15, 6.5), (18.5, 4.3), (18.5, 8.7)], closed=True, r=S.r * 0.3)
    return [shell(fish), shell(tail),
            line("M6 20V12.5M6 16.5L3 13M6 14L9 10.5"), shell("M12.5 20C12.5 14.5 21.5 14.5 21.5 20Z"),
            detail("M17 20V16.5")]


@icon("kelp-forest", CAT, "Tall wavy kelp strands with float bulbs rising from the sea floor",
      tags=["seaweed", "kelp", "underwater forest", "algae", "sea plants", "ocean"])
def _(S):
    return [line("M5 21C2.5 17.5 7.5 15 5 11C3 8 6.5 5.5 5 3"), line("M12 21C14.5 17.5 9.5 14 12 10.5C14 7 10.5 5.5 12 3"),
            line("M19 21C16.5 17.5 21.5 15 19 11C17.5 8 20.5 5.5 19 3"),
            dot(5, 3.4, 1.8), dot(12, 3.4, 1.8), dot(19, 3.4, 1.8), dot(5, 11, 1.6), dot(12, 10.5, 1.6), dot(19, 11, 1.6)]


@icon("tsunami", CAT, "Huge curling wave towering over a low shoreline with a small house",
      tags=["tidal wave", "giant wave", "flood", "disaster", "seismic sea wave", "coast"])
def _(S):
    wave_body = "M2 21C2 12 5 4.5 11 4.5C15 4.5 16.5 7.5 15.5 10C14.5 8.5 12.5 9 12.5 11C12.5 14 14.5 17 14.5 21Z"
    house = poly([(17.5, 21), (17.5, 16.5), (19.75, 14.5), (22, 16.5), (22, 21)], closed=True, r=S.r * 0.3)
    return [shell(wave_body), shell(house)]


def _beach_slope(level, S):
    slope = poly([(2, 6), (5, 6), (14, 17), (22, 17), (22, 21), (2, 21)], closed=True, r=S.r * 0.6)
    return slope


@icon("high-tide", CAT, "Shore slope almost covered by water with an arrow showing the tide rising",
      tags=["tide", "rising tide", "flood tide", "sea level", "coast", "beach"])
def _(S):
    return [shell(_beach_slope(0, S)), line(wave(10.5, 22, 9, 0.5, 4)), line(wave(14, 22, 12.7, 0.5, 3)),
            solid(poly([(19.5, 2.5), (22, 7), (17, 7)], closed=True))]


@icon("low-tide", CAT, "Shore slope with the water drawn back to its lowest level and an arrow pointing down",
      tags=["tide", "ebb tide", "falling tide", "sea level", "coast", "beach", "exposed sand"])
def _(S):
    return [shell(_beach_slope(0, S)), line(wave(16.5, 22, 13.7, 0.4, 2)),
            solid(poly([(19.5, 7.5), (22, 3), (17, 3)], closed=True))]


@icon("tide-chart", CAT, "Smooth tide curve over a time axis with its high and low points marked",
      tags=["tide table", "tide times", "tidal graph", "sea level graph", "high water", "low water", "chart"])
def _(S):
    return [line(poly([(3, 2.5), (3, 21), (22, 21)], r=S.r * 0.4)), line("M5 12C7 6.5 11 6.5 13 12C15 17.5 19 17.5 21 12"),
            dot(9, 7.9, 1.6), dot(17, 16.1, 1.6)]


@icon("coastline", CAT, "Map view of an irregular shoreline with land above and waves offshore",
      tags=["shoreline", "coast", "shore", "seaside", "coastal", "map", "land and sea"])
def _(S):
    land = poly([(2, 2), (22, 2), (22, 9), (19.5, 10), (17.5, 13), (14.5, 11.5), (12, 14.5), (9, 13), (6.5, 15.5), (3.5, 14), (2, 15)], closed=True, r=S.r * 0.6)
    return [shell(land), line(wave(2, 22, 20.5, 0.6, 6))]


@icon("pebble-beach", CAT, "Shore of rounded pebbles of different sizes meeting small waves",
      tags=["shingle beach", "stones", "pebbles", "rocks", "shore", "coast", "gravel"])
def _(S):
    def peb(cx, cy, rx, ry):
        pts = [(cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))) for a in (200, 270, 340, 50, 130)]
        return poly(pts, closed=True, r=S.r + 0.4)
    return [line(wave(2, 22, 4.5, 0.6, 6)), line(wave(2, 22, 9, 0.6, 6)),
            shell(peb(6, 17, 4.5, 3.6)), shell(peb(14.5, 17.5, 5, 3.5)), shell(peb(20, 15.5, 2.2, 2))]


@icon("sandy-beach", CAT, "Smooth sand slope meeting a gentle wave with a shell lying on the sand",
      tags=["beach", "sand", "seashore", "seaside", "shell", "coast", "summer"])
def _(S):
    return [line(wave(2, 22, 4.5, 0.6, 6)), line(wave(2, 22, 8.5, 0.6, 6)),
            line("M2 20C8 20 14 21 22 21"), shell("M6.5 19C6.5 10.5 17.5 10.5 17.5 19Z"), detail("M12 19V14.5M12 19L9.5 15.5M12 19L14.5 15.5")]


@icon("coastal-erosion", CAT, "Crumbling cliff edge with a chunk breaking away and waves hitting its base",
      tags=["cliff collapse", "landslide", "eroding coast", "sea level rise", "climate", "shoreline retreat"])
def _(S):
    cliff = poly([(2, 4), (10.5, 4), (10.5, 8), (8.5, 11), (9.5, 15), (8, 20), (2, 20)], closed=True, r=S.r * 0.6)
    return [shell(cliff), solid(poly([(14, 7), (18, 6), (19, 10), (15, 11)], closed=True, r=0.4)),
            line(wave(12, 22, 16, 0.5, 2)), line(wave(10.5, 22, 20.5, 0.5, 4))]


@icon("breakwater", CAT, "Mound of stacked rocks standing in the sea with waves breaking on each side",
      tags=["seawall", "jetty", "rock armour", "harbor wall", "coast defence", "groyne", "harbour"])
def _(S):
    mound = poly([(7, 20), (8.8, 11), (15.2, 11), (17, 20)], closed=True, r=S.r * 0.6)
    return [shell(mound), detail(seg(12, 11, 12, 15.5)), detail(seg(7.9, 15.5, 16.1, 15.5)),
            line(wave(2, 4.5, 17.5, 0.4, 2)), line(wave(19.5, 22, 17.5, 0.4, 2)), dot(3.5, 12.5, 1.2), dot(20.5, 12.5, 1.2)]


@icon("driftwood", CAT, "Weathered branching log lying on the sand",
      tags=["washed up log", "beach wood", "log", "branch", "shore", "flotsam", "sea wood"])
def _(S):
    main = path_to_d(ST("M3.5 17.5L20.5 15", 4.5, S.cap, S.join))
    return [shell(main), line(poly([(8.5, 16), (7, 10.5), (4.5, 7.5)], r=S.r)), line(seg(7, 10.5, 9.5, 7)),
            line(poly([(14.5, 15), (16, 10), (19.5, 7.5)], r=S.r)), line(seg(21, 21, 2, 21))]


@icon("rip-current", CAT, "Waves running to a beach with a narrow channel of water flowing back out to sea",
      tags=["rip tide", "undertow", "beach safety", "swimming danger", "surf", "lifeguard", "current"])
def _(S):
    return [line(wave(2, 8, 11, 0.5, 2)), line(wave(16, 22, 11, 0.5, 2)), line(wave(2, 8, 6, 0.5, 2)), line(wave(16, 22, 6, 0.5, 2)),
            line(seg(12, 19, 12, 7)), solid(poly([(12, 3), (15, 8), (9, 8)], closed=True)), line(seg(2, 21, 22, 21))]


@icon("sea-cave", CAT, "Cliff face with a dark arched cave opening at the waterline and waves flowing in",
      tags=["cave", "grotto", "coastal cave", "cliff", "blue grotto", "ocean", "sea"])
def _(S):
    mass = minus(rect(2, 3, 20, 15, L(S, 0, 2)), "M7.5 19V13C7.5 10 9.5 8.5 12 8.5C14.5 8.5 16.5 10 16.5 13V19Z")
    return [shell(mass), line(wave(2, 22, 21, 0.5, 6))]


@icon("volcanic-eruption", CAT, "Volcano cone erupting with a plume of ash and flying lava fragments",
      tags=["eruption", "volcano", "lava", "ash", "explosion", "magma", "disaster"])
def _(S):
    cone = poly([(2, 21), (8, 13.5), (10, 15), (14, 15), (16, 13.5), (22, 21)], closed=True, r=S.r * 0.6)
    plume = union(circle(9.5, 9.5, 2.6), circle(12, 7, 3.4), circle(14.6, 9.5, 2.6), rect(9.5, 9, 5, 2))
    return [shell(cone), shell(plume), dot(4.5, 7, 1.3), dot(19.5, 7, 1.3), dot(3.5, 11.5, 1.1), dot(20.5, 11.5, 1.1), dot(7, 3.5, 1.1)]
