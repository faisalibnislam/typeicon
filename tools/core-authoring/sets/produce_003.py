"""TypeIcon Core: produce (batch produce_003): grains, mushrooms, herbs, spices and produce containers.

Drawn from the plant or object itself in upright front views. Stalks are open strokes, silhouettes are shells,
and seeds, gills and veins are details or small solid marks that the Filled style knocks out.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, rotation, transform_path  # noqa: F401

CAT = "produce"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def grow(d, g):
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def cut(d, *fronts, g=2.4):
    """d with every front shape (grown by g) removed: d seen behind the fronts."""
    return minus(d, *[grow(f, g) for f in fronts])


def mark(d):
    return Part("dot", d)


def _p(p):
    return f"{fmt(p[0])} {fmt(p[1])}"


def leaf(x1, y1, x2, y2, bulge):
    """Closed pointed leaf from (x1, y1) to (x2, y2); bulge = half width."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    b = bulge * 2
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx * b)} {fmt(my + ny * b)} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(mx - nx * b)} {fmt(my - ny * b)} {fmt(x1)} {fmt(y1)}Z")


def smooth(pts, closed=True, k=1 / 6):
    n = len(pts)
    d = "M" + _p(pts[0])
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        p0 = pts[(i - 1) % n] if closed or i > 0 else pts[0]
        p1, p2 = pts[i], pts[(i + 1) % n]
        p3 = pts[(i + 2) % n] if closed or i + 2 < n else pts[-1]
        c1 = (p1[0] + (p2[0] - p0[0]) * k, p1[1] + (p2[1] - p0[1]) * k)
        c2 = (p2[0] - (p3[0] - p1[0]) * k, p2[1] - (p3[1] - p1[1]) * k)
        d += "C" + _p(c1) + " " + _p(c2) + " " + _p(p2)
    return d + ("Z" if closed else "")


def blob(cx, cy, rx, ry, radii, start=-90.0):
    n = len(radii)
    pts = []
    for i, f in enumerate(radii):
        a = math.radians(start + i * 360 / n)
        pts.append((cx + rx * f * math.cos(a), cy + ry * f * math.sin(a)))
    return smooth(pts)


def beads(pts, r):
    return union(*[circle(x, y, r) for x, y in pts])


def fan(bx, by, r, a1, a2):
    """Fan wedge with apex (bx, by) opening between angles a1 and a2 (degrees, clockwise from right)."""
    p1 = (bx + r * math.cos(math.radians(a1)), by + r * math.sin(math.radians(a1)))
    p2 = (bx + r * math.cos(math.radians(a2)), by + r * math.sin(math.radians(a2)))
    return f"M{_p((bx, by))}L{_p(p1)}A{fmt(r)} {fmt(r)} 0 0 1 {_p(p2)}Z"


def ray(cx, cy, r1, r2, deg):
    a = math.radians(deg)
    return seg(cx + r1 * math.cos(a), cy + r1 * math.sin(a), cx + r2 * math.cos(a), cy + r2 * math.sin(a))


def pile(pts, rx=2.6, ry=1.6):
    """Solid kernels: list of (x, y, angle)."""
    return solid(union(*[rot(ellipse(x, y, rx, ry), a, x, y) for x, y, a in pts]))


# =========================================================================== grains

def grain(x, y, a=0, rx=1.3, ry=2.3):
    return rot(ellipse(x, y, rx, ry), a, x, y)


@icon("oat", CAT, "Oat stalk with loose spikelets dangling from thin branching stems",
      tags=["oats", "cereal", "grain", "porridge", "whole grain", "crop", "produce"])
def _(S):
    return [line("M12 22V11"), line("M12 11Q12 6 5.5 6"), line("M12 11Q12 6 18.5 6"),
            line("M12 16Q12 13 8.4 13"), line("M12 16Q12 13 15.6 13"),
            solid(union(grain(5.5, 9.6), grain(18.5, 9.6), grain(8.4, 16.4), grain(15.6, 16.4), grain(12, 6.4))),
            line("M12 11V8.5")]


@icon("sorghum", CAT, "Sorghum stalk with long leaves and a dense oval head of round grains",
      tags=["milo", "cereal", "grain", "crop", "millet", "fodder", "produce"])
def _(S):
    return [line("M12 22V14"), shell(ellipse(12, 8, 4.6, 6.2)),
            mark(circle(10.2, 5.6, 0.9)), mark(circle(13.8, 5.6, 0.9)), mark(circle(10.2, 9, 0.9)), mark(circle(13.8, 9, 0.9)),
            shell(leaf(12, 21, 3, 15.5, 1.1)), shell(leaf(12, 19, 21, 13.5, 1.1))]


@icon("millet", CAT, "Drooping dense cylindrical millet seed spike on a curved stalk",
      tags=["cereal", "grain", "foxtail millet", "birdseed", "crop", "bajra", "produce"])
def _(S):
    return [line("M7 22V11Q7 4.5 13 4Q17.5 3.8 19 6"), shell(ellipse(19, 12, 3.1, 6.2)),
            shell(leaf(7, 18, 2.5, 13.5, 1.2)), mark(circle(19, 9, 0.9)), mark(circle(19, 12.2, 0.9)), mark(circle(19, 15.4, 0.9))]


@icon("quinoa", CAT, "Quinoa plant with a dense plume of tiny seeds above leafy stalk",
      tags=["quinoa plant", "seeds", "grain", "superfood", "gluten free", "andean", "produce"])
def _(S):
    plume = beads([(12, 3.6), (9.8, 6.6), (14.2, 6.6), (7.6, 9.6), (12, 9.6), (16.4, 9.6)], 2.0)
    return [line("M12 22V11"), shell(plume), shell(leaf(12, 20, 5, 16, 1.1)), shell(leaf(12, 17.5, 19, 13.5, 1.1))]


@icon("whole-grains", CAT, "Wheat ear and oat sprig above a small pile of grain kernels",
      tags=["cereal", "wheat", "oats", "grain", "whole grain", "harvest", "produce"])
def _(S):
    wheat = [grain(4.8, 7.4, -25, 1.2, 2.2), grain(9.2, 7.4, 25, 1.2, 2.2), grain(4.8, 11.4, -25, 1.2, 2.2),
             grain(9.2, 11.4, 25, 1.2, 2.2), grain(7, 3.6, 0, 1.2, 2.2)]
    oat = [grain(14, 8.8, 0, 1.2, 2.2), grain(20, 8.8, 0, 1.2, 2.2)]
    return [line("M7 16V5"), line("M17 16V10"), line("M17 10Q17 6.4 14 6.4"), line("M17 10Q17 6.4 20 6.4"),
            solid(union(*wheat, *oat)),
            pile([(5.8, 20, -12), (11.4, 20.6, 8), (17.2, 20, -10), (8.6, 18.2, 30), (14.4, 18.2, -30)], 2.2, 1.3)]


# =========================================================================== mushrooms

@icon("shiitake", CAT, "Wide flat shiitake cap with radiating crack lines and a short stem",
      tags=["mushroom", "shitake", "fungi", "edible mushroom", "asian cooking", "umami", "produce"])
def _(S):
    body = "M2.8 13C2.8 7.4 6.8 4.4 12 4.4C17.2 4.4 21.2 7.4 21.2 13H15.2V19Q15.2 21 13.2 21H11.2Q9.2 21 9.2 19V13Z"
    return [shell(body), detail("M8.2 8.2L9.2 10.6"), detail("M12 7V10.4"), detail("M15.8 8.2L14.8 10.6")]


@icon("oyster-mushroom", CAT, "Cluster of overlapping fan shaped oyster mushroom caps with gill lines",
      tags=["mushroom", "pleurotus", "fungi", "edible mushroom", "shelf mushroom", "cooking", "produce"])
def _(S):
    back = fan(8.6, 15.6, 7, -152, -58)
    front = fan(13.4, 21, 11.6, -132, -42)
    return [shell(cut(back, front, g=1.2)), shell(front), detail(ray(13.2, 21, 6, 9, -62)), detail(ray(13.2, 21, 6, 9, -88)),
            detail(ray(13.2, 21, 6, 9, -114))]


@icon("enoki-mushroom", CAT, "Bundle of long thin enoki mushrooms with tiny round caps, tied at the base",
      tags=["mushroom", "enokitake", "fungi", "golden needle", "hot pot", "edible mushroom", "produce"])
def _(S):
    tops = [(5, 8), (8.5, 4.6), (12, 3.6), (15.5, 4.6), (19, 8)]
    out = [line(f"M12 17L{fmt(x)} {fmt(y + 2)}") for x, y in tops]
    out += [dot(x, y, 2.1) for x, y in tops]
    out += [line("M8.6 17H15.4"), line("M11 17.4V22"), line("M13 17.4V22")]
    return out


@icon("morel", CAT, "Tall cone shaped morel cap with honeycomb pits on a thick stem",
      tags=["mushroom", "fungi", "spring mushroom", "foraging", "edible mushroom", "gourmet", "produce"])
def _(S):
    body = "M12 2.5C15.6 2.5 18 7.6 18 13.6H16V20Q16 21.5 14.5 21.5H9.5Q8 21.5 8 20V13.6H6C6 7.6 8.4 2.5 12 2.5Z"
    return [shell(body), mark(circle(12, 6, 1)), mark(circle(9.4, 9.4, 1)), mark(circle(14.6, 9.4, 1)), mark(circle(12, 12.4, 1)),
            mark(circle(8.6, 13.2, 0.0001)), mark(circle(15.4, 13.2, 0.0001))]


@icon("chanterelle", CAT, "Funnel shaped chanterelle with a wavy rim and ridges running down the stem",
      tags=["mushroom", "girolle", "fungi", "foraging", "edible mushroom", "golden mushroom", "produce"])
def _(S):
    body = ("M3.2 6.6Q5.8 5 8 6.4Q10 4.8 12 6.4Q14 4.8 16 6.4Q18.2 5 20.8 6.6C19.6 11 16 12.4 15 16L14.6 20Q14.5 21.5 13 21.5H11"
            "Q9.5 21.5 9.4 20L9 16C8 12.4 4.4 11 3.2 6.6Z")
    return [shell(body), detail("M8.4 9.2L10.4 15.6"), detail("M15.6 9.2L13.6 15.6")]


@icon("truffle-mushroom", CAT, "Lumpy rough truffle next to a slice showing marbled veins",
      tags=["truffle", "fungi", "gourmet", "delicacy", "underground mushroom", "foraging", "produce"])
def _(S):
    ball = blob(9.6, 10.4, 7.4, 6.8, [1, 0.94, 1.04, 0.95, 1.02, 0.94, 1.03, 0.96, 1.0, 0.94])
    sl = blob(16.4, 16.6, 5.4, 4.6, [1, 0.96, 1.03, 0.96, 1.02, 0.96, 1.0, 0.96])
    return [shell(cut(ball, sl, g=1.2)), mark(circle(7.2, 8.4, 0.9)), mark(circle(11, 12.4, 0.9)), shell(sl),
            detail("M13.6 17.6Q15.4 14.8 17.2 16.6Q18.4 17.6 19.2 16.2")]


@icon("portobello", CAT, "Large portobello cap seen from below with radiating gills and a short stem",
      tags=["mushroom", "portabella", "fungi", "edible mushroom", "grilled mushroom", "gills", "produce"])
def _(S):
    body = union(ellipse(12, 9.4, 9.8, 6.2), rect(9.4, 12, 5.2, 9, L(S, 0.4, 1.6)))
    return [shell(body), detail(ray(12, 11.4, 2.6, 6.2, -150)), detail(ray(12, 11.4, 2.6, 6.4, -110)),
            detail(ray(12, 11.4, 2.6, 6.4, -70)), detail(ray(12, 11.4, 2.6, 6.2, -30))]


@icon("king-oyster-mushroom", CAT, "Thick tall king oyster mushroom stem with a small flat cap",
      tags=["mushroom", "king trumpet", "eryngii", "fungi", "edible mushroom", "cooking", "produce"])
def _(S):
    body = "M4 9C4 5.5 7.4 3.5 12 3.5C16.6 3.5 20 5.5 20 9Q20 10.5 18.5 10.5H16.4V20Q16.4 21.5 14.9 21.5H9.1Q7.6 21.5 7.6 20V10.5H5.5Q4 10.5 4 9Z"
    return [shell(body), detail("M8.6 7Q10 5.8 12 5.8")]


@icon("lions-mane-mushroom", CAT, "Round shaggy lion's mane mushroom with long hanging icicle spines",
      tags=["mushroom", "hericium", "fungi", "pom pom mushroom", "nootropic", "edible mushroom", "produce"])
def _(S):
    pts = [(19.5, 10), (18.6, 19), (16.6, 12), (15, 21), (12.8, 12.4), (11, 20), (9, 12), (7.4, 21), (5.6, 12.4), (4.5, 17)]
    body = ("M4.5 10C4.5 4.6 8 3 12 3C16 3 19.5 4.6 19.5 10" + "".join(f"L{_p(p)}" for p in pts[1:]) + "Z")
    return [shell(body), line("M12 3V1.5")]


@icon("wood-ear-mushroom", CAT, "Thin wavy ear shaped wood ear fungus with a folded ruffled edge",
      tags=["mushroom", "cloud ear", "black fungus", "jelly ear", "fungi", "asian cooking", "produce"])
def _(S):
    body = blob(12, 12.4, 9.2, 7.6, [1, 0.94, 1.03, 0.92, 1.04, 0.95, 1.0, 0.9])
    return [shell(body), detail("M7 11.6Q9.4 15.6 14 13.8Q16.4 12.8 17 9.8")]


@icon("puffball", CAT, "Round white puffball mushroom with a stubby base and a few surface bumps",
      tags=["mushroom", "giant puffball", "fungi", "foraging", "edible mushroom", "round mushroom", "produce"])
def _(S):
    body = union(circle(12, 10.8, 8.4), rect(8.6, 15.4, 6.8, 6.2, L(S, 0.5, 2)))
    return [shell(body), mark(circle(9.4, 8.6, 0.9)), mark(circle(14, 7.6, 0.9)), mark(circle(15, 12.2, 0.9))]


@icon("mushroom-slice", CAT, "Mushroom cut in half lengthwise showing cap, gills and stem as one flat shape",
      tags=["mushroom", "sliced mushroom", "cross section", "fungi", "cut", "button mushroom", "produce"])
def _(S):
    body = ("M3.4 11.6C3.4 6.6 7.2 3.4 12 3.4C16.8 3.4 20.6 6.6 20.6 11.6Q20.6 13.2 19 13.2H15.8Q15.2 16.4 15.8 19.6"
            "Q16 21.2 14.4 21.2H9.6Q8 21.2 8.2 19.6Q8.8 16.4 8.2 13.2H5Q3.4 13.2 3.4 11.6Z")
    return [shell(body), detail("M7 9.8Q12 12.4 17 9.8")]


def dome(cx, by, r):
    return f"M{fmt(cx - r)} {fmt(by)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx + r)} {fmt(by)}Z"


@icon("mushroom-basket", CAT, "Foraging basket with a handle and three mushrooms in it",
      tags=["foraging", "mushroom picking", "basket", "fungi", "harvest", "forest", "produce"])
def _(S):
    basket = poly([(3.6, 13.6), (20.4, 13.6), (18.4, 21.2), (5.6, 21.2)], closed=True, r=L(S, 0, 1.2))
    caps = solid(union(dome(8, 12.6, 3), dome(12, 12.6, 3.4), dome(16.2, 12.6, 2.8)))
    return [shell(basket), detail("M6.8 17.4H17.2"), caps, line("M4.6 13.6C4.6 0.6 19.4 0.6 19.4 13.6")]


# =========================================================================== herbs and leaves

@icon("basil", CAT, "Basil sprig with glossy broad leaves in opposite pairs on a stem",
      tags=["herb", "sweet basil", "leaf", "italian cooking", "pesto", "fresh herbs", "produce"])
def _(S):
    return [line("M12 22V9"), shell(leaf(12, 17, 3.5, 13, 2.3)), shell(leaf(12, 17, 20.5, 13, 2.3)),
            shell(leaf(12, 11, 5, 5.6, 2.1)), shell(leaf(12, 11, 19, 5.6, 2.1)), shell(leaf(12, 8, 12, 1.8, 1.8))]


def toothed(x, y, ang, length, width, teeth=3, r=0.0):
    """Serrated pointed leaf with its base at (x, y), tip at `ang` degrees (0 = up, clockwise)."""
    left, right = [], []
    for i in range(1, 2 * teeth + 2):
        t = i / (2 * teeth + 2)
        w = width * math.sin(math.pi * t) ** 0.8
        w += 0.7 if i % 2 == 1 else -0.4
        left.append((-w, -t * length))
        right.append((w, -t * length))
    prof = [(0, 0)] + left + [(0, -length)] + right[::-1]
    return poly(rpts([(x + px, y + py) for px, py in prof], ang, x, y), closed=True, r=r)


@icon("mint-leaves", CAT, "Mint sprig with two serrated pointed leaves and strong vein lines",
      tags=["herb", "peppermint", "spearmint", "leaf", "fresh herbs", "mojito", "produce"])
def _(S):
    r = L(S, 0, 0.35)
    a1 = toothed(11.4, 17, -32, 14, 3.4, 2, r)
    a2 = toothed(12.6, 17, 32, 14, 3.4, 2, r)
    return [line("M12 22V16.4"), shell(a1), shell(a2), detail(ray(11.4, 17, 2.6, 10.6, -32 - 90)),
            detail(ray(12.6, 17, 2.6, 10.6, 32 - 90))]


@icon("parsley", CAT, "Sprig of curly parsley with ruffled leaf clusters on thin stems",
      tags=["herb", "curly parsley", "garnish", "leaf", "fresh herbs", "flat leaf", "produce"])
def _(S):
    def tuft(x, y):
        return beads([(x, y - 1.8), (x - 2, y + 1.2), (x + 2, y + 1.2)], 2.1)
    return [line("M12 22V15"), line("M12 15Q12 11 12 9.6"), line("M12 17Q6.6 16.6 6.6 13.6"), line("M12 17Q17.4 16.6 17.4 13.6"),
            shell(tuft(12, 6.4)), shell(tuft(6.6, 11.6)), shell(tuft(17.4, 11.6))]


def lobed(cx, cy):
    return union(circle(cx - 2.5, cy, 2.1), circle(cx, cy - 2.2, 2.1), circle(cx + 2.5, cy, 2.1),
                 poly([(cx - 3.4, cy + 0.6), (cx, cy + 4.6), (cx + 3.4, cy + 0.6)], closed=True))


@icon("cilantro", CAT, "Cilantro sprig with flat three lobed leaves on thin branching stems",
      tags=["herb", "coriander", "leaf", "fresh herbs", "mexican cooking", "garnish", "produce"])
def _(S):
    def lobed3(cx, cy, k=1.0):
        pts = [(0, 5), (-4.6, 0.8), (-4.2, -2.6), (-1.6, -2.2), (0, -5), (1.6, -2.2), (4.2, -2.6), (4.6, 0.8)]
        return poly([(cx + x * k, cy + y * k) for x, y in pts], closed=True, r=L(S, 0, 0.9))
    return [line("M12 22V13"), line("M12 18.6Q6.6 18 5.6 17"), line("M12 18.6Q17.4 18 18.4 17"),
            shell(lobed3(12, 7.6)), shell(lobed3(5.8, 13.6, 0.8)), shell(lobed3(18.2, 13.6, 0.8))]


@icon("dill", CAT, "Dill sprig with fine feathery threadlike fronds branching from a stem",
      tags=["herb", "fennel fronds", "pickling", "leaf", "fresh herbs", "feathery", "produce"])
def _(S):
    out = [line("M12 22V3")]
    for y, w in ((18, 6), (13, 6.4), (8.4, 5.4)):
        for sgn in (-1, 1):
            out.append(line(f"M12 {y}L{fmt(12 + sgn * w)} {fmt(y - 4)}"))
            out.append(line(f"M{fmt(12 + sgn * w * 0.5)} {fmt(y - 2)}L{fmt(12 + sgn * w * 0.5)} {fmt(y - 5.4)}"))
    return out


@icon("rosemary", CAT, "Woody rosemary stem lined on both sides with short needle shaped leaves",
      tags=["herb", "needles", "evergreen herb", "sprig", "fresh herbs", "roast", "produce"])
def _(S):
    ax, ay, bx, by = 5, 21, 19, 4
    ang = math.degrees(math.atan2(by - ay, bx - ax))
    out = [line(seg(ax, ay, bx, by))]
    for t in (0.22, 0.4, 0.58, 0.76):
        px, py = ax + (bx - ax) * t, ay + (by - ay) * t
        for d in (-52, 52):
            a = math.radians(ang + d)
            out.append(line(seg(px, py, px + 5 * math.cos(a), py + 5 * math.sin(a))))
    out.append(line(seg(bx, by, bx + 1.6, by - 2.4)))
    return out


@icon("thyme", CAT, "Several thin woody thyme stems covered with tiny paired oval leaves",
      tags=["herb", "sprig", "fresh herbs", "leaf", "seasoning", "woody herb", "produce"])
def _(S):
    out = [line("M12 22Q11 12 5.6 4.6"), line("M12 22V2.6"), line("M12 22Q13 12 18.4 4.6")]
    leaves = []
    for (sx, sy, ex, ey) in ((12, 22, 5.6, 4.6), (12, 22, 12, 2.6), (12, 22, 18.4, 4.6)):
        for t in (0.45, 0.66, 0.86):
            x, y = sx + (ex - sx) * t, sy + (ey - sy) * t
            for sgn in (-1, 1):
                leaves.append(rot(ellipse(x + sgn * 1.9, y, 0.9, 1.6), sgn * 35, x + sgn * 1.9, y))
    return out + [solid(union(*leaves))]


@icon("oregano", CAT, "Oregano stem with small round leaves on short stalks and a tiny flower cluster on top",
      tags=["herb", "origanum", "marjoram", "fresh herbs", "italian cooking", "seasoning", "produce"])
def _(S):
    return [line("M12 22V7"), line("M12 18H9.6"), line("M12 14.4H14.4"), line("M12 10.6H9.6"),
            shell(circle(7, 18, 2.6)), shell(circle(17, 14.4, 2.6)), shell(circle(7, 10.6, 2.6)),
            dot(10.6, 3.6, 1.3), dot(13.4, 3.6, 1.3), dot(12, 5.8, 1.3)]


@icon("sage-herb", CAT, "Sage sprig with long oval soft leaves and a central vein",
      tags=["herb", "salvia", "leaf", "fresh herbs", "culinary sage", "sprig", "produce"])
def _(S):
    mid = leaf(12, 19, 12, 2.6, 3.4)
    sides = [leaf(12, 21, 3.8, 10.4, 2.4), leaf(12, 21, 20.2, 10.4, 2.4)]
    return [shell(cut(mid, *sides, g=1.2)), shell(sides[0]), shell(sides[1]), detail("M12 15.6V6.4"), line("M12 21V23")]


@icon("bay-leaf", CAT, "Single smooth pointed bay leaf with a center midrib and a short stem",
      tags=["laurel", "herb", "leaf", "seasoning", "dried herb", "cooking", "produce"])
def _(S):
    return [shell(leaf(8, 19, 17.4, 3.4, 4.4)), line("M8 19L5.4 22"), detail("M9.6 16.4L15.8 6.2")]


@icon("curry-leaf", CAT, "Curry leaf stem with a row of small pointed leaflets alternating along it",
      tags=["herb", "kadi patta", "leaf", "indian cooking", "seasoning", "fresh herbs", "produce"])
def _(S):
    return [line("M12 22V7"), shell(leaf(12, 18.4, 4.6, 14.2, 1.5)), shell(leaf(12, 14.6, 19.4, 10.4, 1.5)),
            shell(leaf(12, 10.6, 4.6, 6.4, 1.5)), shell(leaf(12, 7.4, 12, 1.6, 1.5))]


@icon("chives", CAT, "Bundle of thin chive stems tied together with one round pom pom blossom",
      tags=["herb", "allium", "spring onion tops", "garnish", "fresh herbs", "chive blossom", "produce"])
def _(S):
    return [line("M12 17.6L5.6 5"), line("M12 17.6L9.6 2.6"), line("M12 17.6L15.4 10"), line("M12 17.6L19 6"),
            shell(circle(15.6, 6.4, 3.2)), mark(circle(15.6, 6.4, 0.9)), line("M9.6 17.6H14.4"), line("M12 17.6V22")]


@icon("lemongrass", CAT, "Lemongrass stalk with a bulbous pale base and long narrow blades splaying at the top",
      tags=["herb", "tom yum", "thai cooking", "stalk", "fresh herbs", "citronella", "produce"])
def _(S):
    return [shell(ellipse(12, 17, 2.8, 5)), line("M12 12Q11 6.4 4.6 3"), line("M12 12Q12 6 12.4 2"), line("M12 12Q13 6.4 19.4 3"),
            detail("M12 15V19")]


@icon("lavender-sprig", CAT, "Tall thin lavender stem topped with a spike of small buds and two narrow leaves",
      tags=["herb", "flower", "purple flower", "aromatherapy", "fragrance", "sprig", "produce"])
def _(S):
    buds = []
    for k, y in enumerate((4.4, 7.4, 10.4, 13.4)):
        for sgn in (-1, 1):
            buds.append(rot(ellipse(12 + sgn * 1.9, y, 1.1, 1.8), sgn * 25, 12 + sgn * 1.9, y))
    buds.append(ellipse(12, 2.8, 1, 1.4))
    return [line("M12 22V6"), solid(union(*buds)), shell(leaf(12, 21.4, 6, 14.4, 1)), shell(leaf(12, 21.4, 18, 14.4, 1))]


@icon("lime-leaf", CAT, "Double lime leaf shaped like an hourglass with one leaf joined end to end to another",
      tags=["herb", "kaffir lime", "makrut", "thai cooking", "citrus leaf", "fresh herbs", "produce"])
def _(S):
    body = union(leaf(12, 12, 12, 2.4, 3.6), leaf(12, 12, 12, 21.6, 4.4))
    return [shell(body), detail("M12 5V19")]


@icon("banana-leaf", CAT, "Large oblong banana leaf with a thick midrib and parallel side veins",
      tags=["leaf", "tropical leaf", "wrapping", "southeast asian cooking", "serving leaf", "plantain leaf", "produce"])
def _(S):
    out = [shell(leaf(4.6, 20.4, 19.4, 3.6, 5.2)), detail(seg(6.4, 18.4, 17.6, 5.6))]
    ang = math.degrees(math.atan2(5.6 - 18.4, 17.6 - 6.4))
    for t in (0.28, 0.5, 0.72):
        px, py = 6.4 + (17.6 - 6.4) * t, 18.4 + (5.6 - 18.4) * t
        for d in (-58, 58):
            a = math.radians(ang + d)
            out.append(detail(seg(px, py, px + 3.6 * math.cos(a), py + 3.6 * math.sin(a))))
    return out


@icon("grape-leaf", CAT, "Broad grape leaf with five pointed lobes and palm like veins",
      tags=["vine leaf", "dolma", "leaf", "mediterranean cooking", "vineyard", "five lobes", "produce"])
def _(S):
    pts = [(12, 2.4), (14.4, 7.6), (20.8, 8.2), (17.4, 12.4), (18.2, 18), (13, 16.6), (12, 17.2),
           (11, 16.6), (5.8, 18), (6.6, 12.4), (3.2, 8.2), (9.6, 7.6)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 0.6))), line("M12 17.2V22"), detail("M12 15V7"), detail("M12 13.6L17.4 9.6"),
            detail("M12 13.6L6.6 9.6")]


@icon("fig-leaf", CAT, "Broad fig leaf with deep rounded lobes and a short stem",
      tags=["leaf", "mediterranean", "fig tree", "lobed leaf", "garden", "botanical", "produce"])
def _(S):
    body = union(ellipse(12, 8.2, 3.6, 6), rot(ellipse(6.2, 11.6, 3.4, 5.4), -45, 6.2, 11.6),
                 rot(ellipse(17.8, 11.6, 3.4, 5.4), 45, 17.8, 11.6), circle(12, 14.4, 5))
    return [shell(body), line("M12 19V22.4"), detail("M9.2 7L9.6 12.6"), detail("M14.8 7L14.4 12.6")]


@icon("tea-leaves", CAT, "Two young tea leaves and a bud at the tip of a short tea plant stem",
      tags=["tea plant", "camellia sinensis", "green tea", "leaf bud", "tea garden", "herbal", "produce"])
def _(S):
    return [line("M12 22V14"), shell(leaf(12, 15, 4.4, 8, 2.3)), shell(leaf(12, 15, 19.6, 8, 2.3)), shell(leaf(12, 13, 12, 2.4, 1.7))]


@icon("herb-bundle", CAT, "Small bouquet of mixed herb sprigs tied together with string",
      tags=["bouquet garni", "fresh herbs", "sprigs", "bundle", "kitchen herbs", "seasoning", "produce"])
def _(S):
    return [shell(leaf(11, 15.6, 4.2, 6, 2)), shell(leaf(12, 15, 12, 2.4, 2)), shell(leaf(13, 15.6, 19.8, 6, 2)),
            line("M9 17.8H15"), line("M10.6 18.2L9.4 22.6"), line("M13.4 18.2L14.6 22.6")]


@icon("drying-herbs", CAT, "Two bunches of herbs hanging upside down from a line by string ties",
      tags=["herb drying", "hanging herbs", "preserving herbs", "dried herbs", "harvest", "kitchen", "produce"])
def _(S):
    return [line("M2.4 3.8H21.6"), line("M7 3.8V9"), line("M17 3.8V9"),
            shell(leaf(7, 9, 4, 21.4, 1.8)), shell(leaf(7, 9, 10, 21.4, 1.8)),
            shell(leaf(17, 9, 14, 21.4, 1.8)), shell(leaf(17, 9, 20, 21.4, 1.8))]


@icon("cinnamon-stick", CAT, "Two rolled cinnamon bark quills lying side by side with spiral ends",
      tags=["cinnamon", "spice", "bark", "quill", "baking spice", "mulling spice", "produce"])
def _(S):
    q1 = rot(rect(2.8, 4.4, 18.4, 6, L(S, 1.4, 3)), -24)
    q2 = rot(rect(2.8, 13.6, 18.4, 6, L(S, 1.4, 3)), -24)
    return [shell(q1), shell(q2), mark(rot(circle(5.6, 7.4, 0.9), -24)), mark(rot(circle(5.6, 16.6, 0.9), -24))]


@icon("star-anise", CAT, "Eight pointed star anise pod with a seed chamber in each point",
      tags=["spice", "anise", "badiane", "pod", "chinese five spice", "mulled wine", "produce"])
def _(S):
    pts = []
    for i in range(16):
        a = math.radians(-90 + i * 22.5)
        rr = 8.8 if i % 2 == 0 else 4.9
        pts.append((12 + rr * math.cos(a), 12 + rr * math.sin(a)))
    out = [shell(poly(pts, closed=True, r=L(S, 0, 0.5))), detail(circle(12, 12, 2.4))]
    return out


@icon("clove-spice", CAT, "Dried clove bud with a round ball head, crown prongs and a tapering stalk",
      tags=["cloves", "spice", "dried bud", "baking spice", "aromatic", "syzygium", "produce"])
def _(S):
    body = union(circle(12, 6.6, 3.2), poly([(9.8, 9), (14.2, 9), (12.9, 21.6), (11.1, 21.6)], closed=True))
    return [shell(body), line("M9.6 9.4L5.6 7.6"), line("M14.4 9.4L18.4 7.6"), line("M9.8 7.4L7.6 3.6"), line("M14.2 7.4L16.4 3.6")]


@icon("nutmeg", CAT, "Oval nutmeg wrapped in a lacy web of mace next to a small cut half",
      tags=["spice", "mace", "seed", "baking spice", "grated", "myristica", "produce"])
def _(S):
    nut = rot(ellipse(9.6, 11.6, 5.8, 7.6), 18, 9.6, 11.6)
    return [shell(nut), detail(rot("M5.2 8.6Q9 11.6 14 9", 18, 9.6, 11.6)), detail(rot("M5.6 14.4Q9.6 17 14 14.6", 18, 9.6, 11.6)),
            shell(ellipse(18.2, 17.4, 2.8, 3.8)), mark(circle(18.2, 17.4, 0.8))]


@icon("cardamom", CAT, "Small ribbed cardamom pod with a pointed tip next to a split pod showing seeds",
      tags=["spice", "cardamon", "green cardamom", "chai", "pod", "baking spice", "produce"])
def _(S):
    return [shell(leaf(7, 20.6, 9.6, 3.4, 3.4)), detail("M8 17.2Q9.2 11.6 9 7.2"),
            shell(leaf(16.4, 20.6, 17.6, 5.6, 3.6)), mark(circle(17, 9.6, 0.9)), mark(circle(17, 12.8, 0.9)), mark(circle(16.8, 16, 0.9))]


@icon("saffron", CAT, "Small crocus flower with three long thread stigmas trailing from its center",
      tags=["spice", "crocus", "threads", "paella", "golden spice", "expensive spice", "produce"])
def _(S):
    return [shell(leaf(12, 21, 4.8, 11.4, 2.4)), shell(leaf(12, 21, 19.2, 11.4, 2.4)), shell(leaf(12, 21, 12, 9.6, 2.4)),
            line("M12 9.6Q9.6 6.4 6 4.6"), line("M12 9.6Q12.8 6 12 2.4"), line("M12 9.6Q14.4 6.4 18 4.6")]


@icon("peppercorn", CAT, "Small heap of round peppercorns stacked in a pyramid",
      tags=["spice", "black pepper", "pepper", "seasoning", "whole spice", "peppercorns", "produce"])
def _(S):
    cs = [(5.6, 18.4), (12, 18.4), (18.4, 18.4), (8.8, 12), (15.2, 12), (12, 5.8)]
    return [shell(poly(regular(x, y, 2.7, 8, -90 + 22.5), closed=True) if S.name == "line" else circle(x, y, 2.5)) for x, y in cs]


@icon("spice-jar", CAT, "Small glass jar with a shaker lid and a blank label band",
      tags=["spice rack", "seasoning", "shaker", "kitchen", "pantry", "herbs and spices", "produce"])
def _(S):
    return [shell(rect(6.4, 2.4, 11.2, 4, L(S, 0.6, 1.6))), shell(rect(4.6, 7.6, 14.8, 14, L(S, 1.5, 3.4))),
            detail(rect(8, 12.2, 8, 5, L(S, 0.4, 1))), mark(circle(9.6, 4.4, 0.7)), mark(circle(14.4, 4.4, 0.7))]


@icon("mortar-and-pestle", CAT, "Round stone mortar bowl with a thick pestle leaning inside it",
      tags=["grinding", "spices", "kitchen tool", "pharmacy", "crush", "herbs", "produce"])
def _(S):
    bowl = "M3 11.4H21Q21 21.2 12 21.2Q3 21.2 3 11.4Z"
    pestle = rot(rect(12.4, 0.8, 3.8, 13.6, L(S, 0.6, 1.8)), 28, 14, 8)
    return [shell(cut(pestle, bowl, g=1.0)), shell(bowl)]


@icon("ground-spice", CAT, "Small cone shaped mound of ground spice powder with a measuring spoon beside it",
      tags=["powder", "seasoning", "spice mound", "measuring spoon", "baking", "turmeric", "produce"])
def _(S):
    mound = "M2.4 20.8C5.2 20.8 7.2 19.6 8.2 16.4Q9.2 12.8 9.8 10.8Q10.2 9.8 10.8 10.8Q11.6 12.8 12.6 16.4C13.6 19.6 15.2 20.8 16.6 20.8Z"
    return [shell(mound), shell(rot(ellipse(18, 15.4, 2.6, 3.4), 14, 18, 15.4)), line("M18.4 12.4L20 4")]


@icon("pineapple-plant", CAT, "Rosette of long spiky leaves with a single pineapple growing from the center",
      tags=["pineapple", "tropical plant", "farm", "crop", "fruit plant", "bromeliad", "produce"])
def _(S):
    return [shell(leaf(12, 21.6, 3.2, 11.8, 1.2)), shell(leaf(12, 21.6, 20.8, 11.8, 1.2)),
            shell(leaf(12, 21.6, 3, 19, 1)), shell(leaf(12, 21.6, 21, 19, 1)),
            shell(ellipse(12, 10.4, 3.8, 5.6)), mark(circle(12, 8.6, 0.8)), mark(circle(12, 12.2, 0.8)),
            line("M12 15.8V21"), line("M10.4 4.6L9.2 1.8"), line("M12 4.4V1.4"), line("M13.6 4.6L14.8 1.8")]


@icon("grapevine", CAT, "Twisted grape vine with a curling tendril, one leaf and a hanging bunch of grapes",
      tags=["grapes", "vineyard", "winemaking", "vine", "wine", "harvest", "produce"])
def _(S):
    def lobed3(cx, cy, k=1.0):
        pts = [(0, 5), (-4.6, 0.8), (-4.2, -2.6), (-1.6, -2.2), (0, -5), (1.6, -2.2), (4.2, -2.6), (4.6, 0.8)]
        return poly([(cx + x * k, cy + y * k) for x, y in pts], closed=True, r=L(S, 0, 0.9))
    grapes = [(11.8, 11.4), (16, 11.4), (20, 11.4), (13.8, 15.4), (18, 15.4), (15.8, 19.4)]
    return [line("M2.4 6C6 2.4 9.6 7.6 13.4 5C16 3.2 19 3.4 21.6 5.4"), line("M6.4 6.4V9"),
            shell(lobed3(6.2, 13.6, 0.85)), solid(union(*[circle(x, y, 1.9) for x, y in grapes])), line("M15.6 5.4V9.6")]


@icon("berry-bush", CAT, "Round leafy bush dotted with small round berries",
      tags=["shrub", "blueberry bush", "garden", "fruit bush", "harvest", "berries", "produce"])
def _(S):
    body = union(circle(8, 12.8, 5.2), circle(16, 12.8, 5.2), circle(12, 8.8, 5.8), circle(12, 14.8, 5))
    return [shell(body), line("M12 19.6V22.4"), mark(circle(9.6, 8.6, 1.1)), mark(circle(14.8, 8, 1.1)), mark(circle(7.4, 13, 1.1)),
            mark(circle(12.4, 12.8, 1.1)), mark(circle(16.8, 13.4, 1.1)), mark(circle(12, 17, 1.1))]


# =========================================================================== produce containers and tools

@icon("fruit-bowl", CAT, "Shallow bowl heaped with an apple, a banana and a bunch of grapes",
      tags=["fruit", "bowl", "fruit salad", "healthy snack", "kitchen", "apple banana grapes", "produce"])
def _(S):
    bowl = "M2.6 13.6H21.4Q21 20.6 12 20.6Q3 20.6 2.6 13.6Z"
    apple = circle(7.6, 9.2, 3.8)
    return [shell(cut(apple, bowl, g=0.4)), line("M7.6 5.4Q7.8 3.8 9.2 3.2"),
            solid(union(circle(13.8, 10.2, 1.5), circle(16.6, 10.2, 1.5), circle(19.2, 10.6, 1.5), circle(15.2, 12.4, 1.2), circle(18, 12.6, 1.2))),
            shell(bowl)]


@icon("fruit-basket", CAT, "Woven basket with a handle filled with apples, a pear and grapes",
      tags=["fruit", "gift basket", "harvest", "apples", "pear", "grapes", "produce"])
def _(S):
    basket = poly([(3.6, 13.6), (20.4, 13.6), (18.4, 21.2), (5.6, 21.2)], closed=True, r=L(S, 0, 1.2))
    apple = circle(8, 10.2, 3.2)
    pear = union(circle(14.2, 11, 3), circle(14.2, 7.6, 1.9))
    return [shell(cut(apple, pear, g=0.8)), shell(pear), solid(union(circle(18.6, 10, 1.1), circle(19.6, 12, 1.1))),
            shell(basket), detail("M6.8 17.4H17.2"), line("M4.6 13.6C4.6 0.6 19.4 0.6 19.4 13.6")]


@icon("produce-crate", CAT, "Slatted wooden crate filled with round fruits",
      tags=["fruit crate", "wooden box", "market", "harvest", "wholesale", "apples", "produce"])
def _(S):
    return [solid(union(circle(6.6, 8.6, 2.9), circle(12, 7.2, 2.9), circle(17.4, 8.6, 2.9))),
            shell(rect(3, 11.8, 18, 10, L(S, 0.6, 2))), detail("M3 16.8H21")]


@icon("produce-sack", CAT, "Burlap sack tied at the top with a few potatoes spilling out beside it",
      tags=["burlap", "potato sack", "bag", "farm", "harvest", "grain sack", "produce"])
def _(S):
    sack = "M7 7.8C4 10.4 2.8 13.2 2.8 16.8C2.8 20 4 21.6 6.6 21.6H11.6C14.2 21.6 15.4 20 15.4 16.8C15.4 13.2 14.2 10.4 11.2 7.8Z"
    return [shell(sack), shell(poly([(7, 7.8), (6, 3.4), (9.2, 5), (12.2, 3.4), (11.2, 7.8)], closed=True, r=L(S, 0, 0.6))),
            detail("M7.4 9.6H10.8"),
            solid(union(rot(ellipse(19, 20.4, 2.6, 1.7), -12, 19, 20.4), rot(ellipse(19.2, 16.8, 2.2, 1.6), 16, 19.2, 16.8)))]


@icon("produce-stand", CAT, "Market stall with a scalloped awning above crates of produce",
      tags=["farmers market", "fruit stand", "stall", "greengrocer", "street market", "vendor", "produce"])
def _(S):
    awning = ("M5 3H19L21.6 9A2.4 2.4 0 0 1 16.8 9A2.4 2.4 0 0 1 12 9A2.4 2.4 0 0 1 7.2 9A2.4 2.4 0 0 1 2.4 9Z")
    return [shell(awning), detail("M9 3.4L8.2 8"), detail("M15 3.4L15.8 8"),
            solid(union(circle(6.4, 14, 1.6), circle(9, 14, 1.6), circle(15, 14, 1.6), circle(17.6, 14, 1.6))),
            shell(rect(4.2, 15.4, 6.6, 6.2, L(S, 0.4, 1.2))), shell(rect(13.2, 15.4, 6.6, 6.2, L(S, 0.4, 1.2)))]


@icon("berry-punnet", CAT, "Small square carton container filled with round berries",
      tags=["berries", "strawberries", "blueberries", "punnet", "fruit carton", "grocery", "produce"])
def _(S):
    box = poly([(3.6, 11.8), (20.4, 11.8), (18.6, 21.4), (5.4, 21.4)], closed=True, r=L(S, 0, 1.2))
    return [solid(union(circle(7, 9.4, 2.3), circle(12, 9, 2.3), circle(17, 9.4, 2.3), circle(9.6, 5, 2.2), circle(14.4, 5, 2.2))),
            shell(box), detail("M9 15V18.4"), detail("M12 15V18.4"), detail("M15 15V18.4")]


@icon("mesh-produce-bag", CAT, "Net bag with a diamond mesh pattern, gathered and tied at the top",
      tags=["net bag", "oranges", "citrus", "string bag", "reusable bag", "grocery", "produce"])
def _(S):
    return [shell(rect(4, 9.6, 16, 12, L(S, 2, 4.4))), line("M9.4 9.6L12 4.8L14.6 9.6"), dot(12, 4.2, 1.3),
            detail("M4 14L11.6 21.6"), detail("M9.6 9.6L20 20"), detail("M20 14L12.4 21.6"), detail("M14.4 9.6L4 20")]


@icon("pickle-jar", CAT, "Tall jar with a lid holding upright pickles and a few floating seeds",
      tags=["pickles", "gherkins", "cucumber", "preserves", "fermented", "canning", "produce"])
def _(S):
    return [shell(rect(6, 2.4, 12, 3.8, L(S, 0.6, 1.6))), shell(rect(4.6, 7, 14.8, 14.6, L(S, 1.5, 3.4))),
            detail(rect(7.8, 10, 3.6, 8.4, 1.8)), detail(rect(13, 11.8, 3.6, 6.6, 1.8)), mark(circle(12.2, 9.8, 0.7))]


@icon("produce-scale", CAT, "Hanging spring scale with a round dial and a pan holding vegetables",
      tags=["weighing", "grocery scale", "market", "hanging scale", "weight", "greengrocer", "produce"])
def _(S):
    return [line("M12 1.6V3.6"), shell(circle(12, 8, 4.6)), detail("M12 8L13.8 5.8"), line("M10 12.4L5.8 17.4"), line("M14 12.4L18.2 17.4"),
            solid(union(circle(9.6, 15.2, 1.8), circle(14.6, 15.2, 1.8))), shell("M4 17.8H20Q19.2 21.8 12 21.8Q4.8 21.8 4 17.8Z")]


@icon("fruit-picker", CAT, "Long pole with a wire cage basket at the top holding a picked fruit",
      tags=["fruit picking", "orchard", "harvest", "reach pole", "tree", "apple picker", "produce"])
def _(S):
    cage = poly([(10, 9.6), (21, 9.6), (18.6, 15.8), (12.4, 15.8)], closed=True, r=L(S, 0, 1))
    return [line("M3 22L13.2 14.8"), shell(circle(15.6, 6.2, 3.2)), shell(cage), detail("M15.6 10.4V15")]


@icon("strawberry-plant", CAT, "Low strawberry plant with a three part leaf and two hanging strawberries",
      tags=["strawberries", "berry plant", "garden", "fruit plant", "runner", "crop", "produce"])
def _(S):
    def berry(x, y):
        if S.name == "line":
            return (f"M{fmt(x)} {fmt(y - 3.6)}C{fmt(x + 4.8)} {fmt(y - 3.6)} {fmt(x + 3.8)} {fmt(y + 3)} {fmt(x)} {fmt(y + 5)}"
                    f"C{fmt(x - 3.8)} {fmt(y + 3)} {fmt(x - 4.8)} {fmt(y - 3.6)} {fmt(x)} {fmt(y - 3.6)}Z")
        return (f"M{fmt(x)} {fmt(y - 3.6)}C{fmt(x + 4.8)} {fmt(y - 3.6)} {fmt(x + 4.6)} {fmt(y + 2)} {fmt(x + 1.4)} {fmt(y + 4.6)}"
                f"Q{fmt(x)} {fmt(y + 5.4)} {fmt(x - 1.4)} {fmt(y + 4.6)}C{fmt(x - 4.6)} {fmt(y + 2)} {fmt(x - 4.8)} {fmt(y - 3.6)} {fmt(x)} {fmt(y - 3.6)}Z")
    return [shell(leaf(12, 8.6, 4.6, 3.6, 2)), shell(leaf(12, 8.6, 19.4, 3.6, 2)), shell(leaf(12, 7.4, 12, 1.6, 1.8)),
            line("M12 8.6V10.4"), line("M12 10.4Q6.4 10.4 6.2 13.6"), line("M12 10.4Q17.6 10.4 17.8 13.6"),
            shell(berry(6.2, 16.8)), shell(berry(17.8, 16.8)), mark(circle(6.2, 17.6, 0.8)), mark(circle(17.8, 17.6, 0.8)),
            line("M4.2 13.4H8.2"), line("M15.8 13.4H19.8")]


@icon("root-vegetables", CAT, "A carrot, a beet and a radish with their leafy tops",
      tags=["carrot", "beetroot", "radish", "vegetables", "root crops", "bunch", "produce"])
def _(S):
    return [line("M6.2 9L4.8 3"), line("M6.2 9L8 3"), line("M12 10L10.4 3"), line("M12 10L13.6 3"),
            line("M18 10.4L16.6 4.6"), line("M18 10.4L19.6 4.6"),
            shell(poly([(3.6, 9.4), (8.8, 9.4), (6.2, 21.4)], closed=True, r=L(S, 0, 1))),
            shell(circle(12, 14.2, 3.8)), line("M12 18V21.8"), shell(ellipse(18, 15, 2.8, 4)), line("M18 19V21.6")]


@icon("leafy-greens", CAT, "Bunch of mixed leafy greens fanned out: a serrated leaf, a veined leaf and a rounded leaf",
      tags=["kale", "spinach", "lettuce", "salad greens", "vegetables", "bunch", "produce"])
def _(S):
    r = L(S, 0, 0.35)
    return [shell(toothed(11.2, 21, -34, 17, 3.6, 3, r)), shell(leaf(12.8, 21, 20.4, 6.4, 3.6)),
            shell(leaf(12, 21, 12, 2.6, 2.8)), detail("M12 18V7")]


@icon("yuzu", CAT, "Lumpy uneven yuzu citrus with a bumpy knobbly peel, a short stem and one leaf",
      tags=["citrus", "japanese citrus", "fruit", "bumpy peel", "aromatic", "winter fruit", "produce"])
def _(S):
    body = blob(12, 13.6, 8.2, 7.6, [1, 0.94, 1.04, 0.95, 1.03, 0.94, 1.04, 0.95, 1.03, 0.94, 1.04, 0.95, 1.02, 0.94])
    return [shell(body), line("M12 6.6V3.8"), shell(leaf(13, 4.6, 19.6, 2.8, 1.5)),
            mark(circle(9, 11.6, 0.9)), mark(circle(14.4, 13, 0.9)), mark(circle(10.6, 17, 0.9))]


@icon("tamarillo", CAT, "Two egg shaped tamarillo fruits with pointed tips hanging from long thin stems",
      tags=["tree tomato", "fruit", "red fruit", "new zealand", "exotic fruit", "hanging", "produce"])
def _(S):
    def egg(cx, cy):
        return (f"M{fmt(cx)} {fmt(cy - 6.4)}C{fmt(cx + 5.2)} {fmt(cy - 6.4)} {fmt(cx + 4.6)} {fmt(cy + 3)} {fmt(cx)} {fmt(cy + 6.8)}"
                f"C{fmt(cx - 4.6)} {fmt(cy + 3)} {fmt(cx - 5.2)} {fmt(cy - 6.4)} {fmt(cx)} {fmt(cy - 6.4)}Z")
    return [line("M6.8 8Q6.8 4 12 2.6"), line("M17.2 8Q17.2 4 12 2.6"),
            shell(rot(egg(6.8, 14.8), 6, 6.8, 14.8)), shell(rot(egg(17.2, 14.4), -6, 17.2, 14.4)),
            line("M4.6 8.6H9.2"), line("M14.8 8.2H19.4")]


@icon("juniper-berries", CAT, "Sprig of short sharp juniper needles with three round berries clustered on it",
      tags=["gin", "spice", "evergreen", "berries", "conifer", "foraging", "produce"])
def _(S):
    out = [line("M12 22V3")]
    for y in (4.4, 7.8, 11.2):
        out.append(line(f"M12 {fmt(y + 2)}L{fmt(7.8)} {fmt(y - 1.2)}"))
        out.append(line(f"M12 {fmt(y + 2)}L{fmt(16.2)} {fmt(y - 1.2)}"))
    return out + [shell(circle(7.4, 18, 2.8)), shell(circle(16.6, 18, 2.8)), shell(circle(12, 16, 2.4))]


@icon("noni", CAT, "Lumpy oval noni fruit covered in small eye marks, with a short stem",
      tags=["indian mulberry", "cheese fruit", "tropical fruit", "juice", "superfruit", "polynesian", "produce"])
def _(S):
    body = blob(12, 13.4, 6.8, 8.2, [1, 0.95, 1.03, 0.95, 1.03, 0.94, 1.03, 0.95, 1.02, 0.95, 1.03, 0.94])
    return [shell(body), line("M12 5.2V2.6"), mark(circle(9.6, 9.6, 0.9)), mark(circle(14.2, 11, 0.9)), mark(circle(9.8, 14.6, 0.9)),
            mark(circle(14.4, 17, 0.9)), mark(circle(11.2, 18.6, 0.0001))]


@icon("jabuticaba", CAT, "Short tree trunk with many round berries growing directly on its bark",
      tags=["brazilian grape tree", "fruit", "tropical", "cauliflorous", "berries", "tree", "produce"])
def _(S):
    trunk = "M8.8 22L9.6 9Q9.8 7.8 11 7.8H13Q14.2 7.8 14.4 9L15.2 22Z"
    return [shell(trunk), shell(leaf(12, 7.4, 5.6, 2.6, 1.6)), shell(leaf(12, 7.4, 18.4, 2.6, 1.6)),
            mark(circle(10.8, 11.4, 1.3)), mark(circle(13.4, 14.2, 1.3)), mark(circle(10.8, 17.4, 1.3)), mark(circle(13.4, 20, 1.3)),
            solid(union(circle(6.6, 12.4, 1.9), circle(17.4, 10.4, 1.9), circle(6.8, 17.8, 1.9), circle(17.6, 16, 1.9)))]


@icon("lemon-branch", CAT, "Branch with two pointed leaves, a hanging lemon and a small five petal blossom",
      tags=["lemon", "citrus", "blossom", "orchard", "branch", "mediterranean", "produce"])
def _(S):
    lemon = rot(union(ellipse(9.4, 15, 6, 4.8), circle(3, 15, 0.9), circle(15.8, 15, 0.9)), -22, 9.4, 15)
    flower = beads([(19.4 + 2.2 * math.cos(math.radians(-90 + i * 72)), 11.2 + 2.2 * math.sin(math.radians(-90 + i * 72))) for i in range(5)], 1.4)
    return [line("M2.4 4.4Q10 2.4 21.6 4.8"), line("M9 4.2L9.8 9.4"), shell(lemon),
            shell(leaf(14.6, 4, 18, 8.4, 1.2)), shell(leaf(5, 3.6, 3.4, 8.8, 1.2)), shell(flower)]


@icon("water-chestnut", CAT, "Flattened round water chestnut corm with ring lines and a short pointed sprout",
      tags=["asian vegetable", "corm", "stir fry", "crunchy", "aquatic", "chinese cooking", "produce"])
def _(S):
    body = union(ellipse(12, 14.6, 8.6, 6.4), poly([(9.6, 9.4), (12, 4.6), (14.4, 9.4)], closed=True))
    return [shell(body), detail("M5 13.4Q12 16.6 19 13.4"), detail("M6.4 17.8Q12 20 17.6 17.8")]


@icon("fava-bean", CAT, "Thick wide fava bean pod split open showing three large flat beans",
      tags=["broad bean", "faba", "legume", "pod", "spring vegetable", "pulses", "produce"])
def _(S):
    pod = L(S, "M2.8 12C2.8 8.6 4.8 7 8 7H15.4L22 12L15.4 17H8C4.8 17 2.8 15.4 2.8 12Z",
            "M2.8 12C2.8 8.6 4.8 7 8 7H15.4Q20.6 7 22 12Q20.6 17 15.4 17H8C4.8 17 2.8 15.4 2.8 12Z")
    return [shell(pod), mark(ellipse(8.2, 12, 1.8, 2.6)), mark(ellipse(12.6, 12, 1.8, 2.6)), mark(ellipse(17, 12, 1.6, 2.4))]


@icon("winged-bean", CAT, "Winged bean pod with frilly ridges along both of its sides",
      tags=["goa bean", "four angled bean", "legume", "tropical vegetable", "pod", "frilly", "produce"])
def _(S):
    return [shell(rect(2.8, 8.8, 18.4, 6.4, L(S, 1.5, 3.2))),
            line("M3.6 6.6Q5.4 3.6 7.2 6.6Q9 3.6 10.8 6.6Q12.6 3.6 14.4 6.6Q16.2 3.6 18 6.6Q19.4 4.4 20.6 6.2"),
            line("M3.6 17.4Q5.4 20.4 7.2 17.4Q9 20.4 10.8 17.4Q12.6 20.4 14.4 17.4Q16.2 20.4 18 17.4Q19.4 19.6 20.6 17.8")]
