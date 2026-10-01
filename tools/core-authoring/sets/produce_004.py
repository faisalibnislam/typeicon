"""TypeIcon Core: produce (batch produce_004): herbs, mushrooms, roots, plants and kitchen produce.

Upright side views drawn from the plant or object itself. Seeds are small solid marks; stems are open strokes.
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
    """Region d expanded by g px (cuts clean gaps between overlapping parts)."""
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def cut(d, *fronts, g=2.4):
    """d with every front shape (grown by g) removed: d seen behind the fronts."""
    return minus(d, *[grow(f, g) for f in fronts])


def thick(d, w, cap="round"):
    """Closed outline of a stroke of width w along d."""
    return path_to_d(ST(d, w, cap, "round"))


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled body."""
    return Part("dot", d)


def _p(p):
    return f"{fmt(p[0])} {fmt(p[1])}"


def tip(a, p, b, r):
    """Corner at p (from a, towards b): sharp when r == 0, softened with a quadratic when r > 0."""
    if r <= 0:
        return "L" + _p(p)
    la = math.hypot(a[0] - p[0], a[1] - p[1])
    lb = math.hypot(b[0] - p[0], b[1] - p[1])
    t = min(r, la / 2, lb / 2)
    s = (p[0] + (a[0] - p[0]) * t / la, p[1] + (a[1] - p[1]) * t / la)
    e = (p[0] + (b[0] - p[0]) * t / lb, p[1] + (b[1] - p[1]) * t / lb)
    return "L" + _p(s) + "Q" + _p(p) + " " + _p(e)


def leaf(x1, y1, x2, y2, bulge):
    """Closed pointed leaf from (x1, y1) to (x2, y2); bulge = half width."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    b = bulge * 2
    return (f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx * b)} {fmt(my + ny * b)} {fmt(x2)} {fmt(y2)}"
            f"Q{fmt(mx - nx * b)} {fmt(my - ny * b)} {fmt(x1)} {fmt(y1)}Z")


def smooth(pts, closed=True, k=1 / 6):
    """Smooth curve through pts (Catmull-Rom as cubics)."""
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
    """Smooth irregular oval: one radius factor per evenly spaced direction."""
    n = len(radii)
    pts = []
    for i, f in enumerate(radii):
        a = math.radians(start + i * 360 / n)
        pts.append((cx + rx * f * math.cos(a), cy + ry * f * math.sin(a)))
    return smooth(pts)


def spiky(cx, cy, rx, ry, n, h, S, skip=(), start=-90.0):
    """Oval outline with n triangular spikes of height h (sharp in Line, softened in Rounded)."""
    pts = []
    for i in range(2 * n):
        a = math.radians(start + i * 180 / n)
        if i % 2 == 1 and (i // 2) not in skip:
            k = 1 + h / ((rx + ry) / 2)
        else:
            k = 1
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    return poly(pts, closed=True, r=L(S, 0, 0.45))


def region(d):
    """Area covered by a closed outline filled to its outer stroke edge."""
    return U(P(d), ST(d, 2))


def layered(ds, gap=1.4):
    """Filled design for overlapping shapes listed back to front: each front shape is separated from those
    behind it by a knocked-out gap."""
    body = None
    for d in ds:
        r = region(d)
        body = r if body is None else U(D(body, U(r, ST(path_to_d(r), 2 * gap, "round", "round"))), r)
    return body


def beads(pts, r):
    """Silhouette of a cluster of touching beads (drupelets)."""
    return union(*[circle(x, y, r) for x, y in pts])


def stem(x1, y1, x2, y2, bend=0.0):
    """Short curved stalk from (x1, y1) to (x2, y2)."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ln = math.hypot(x2 - x1, y2 - y1)
    nx, ny = -(y2 - y1) / ln, (x2 - x1) / ln
    return line(f"M{fmt(x1)} {fmt(y1)}Q{fmt(mx + nx * bend)} {fmt(my + ny * bend)} {fmt(x2)} {fmt(y2)}")



def pt_(cx, cy, r, deg):
    return (cx + r * math.cos(math.radians(deg)), cy + r * math.sin(math.radians(deg)))


def drop(S, b, t, hw, k=0.7):
    """Teardrop from round base b to pointed tip t; hw is about the half width. Rounded softens the tip."""
    bx, by = b
    tx, ty = t
    ln = math.hypot(tx - bx, ty - by)
    ux, uy = (tx - bx) / ln, (ty - by) / ln
    nx, ny = -uy, ux
    k = 0 if S.name == "line" else k
    a = (tx - ux * k + nx * k * 0.55, ty - uy * k + ny * k * 0.55)
    c = (tx - ux * k - nx * k * 0.55, ty - uy * k - ny * k * 0.55)

    def P2(x, y, s):
        return (x + nx * s, y + ny * s)
    c1 = P2(tx - ux * ln * 0.35, ty - uy * ln * 0.35, hw * 1.0)
    c2 = P2(bx + ux * ln * 0.05, by + uy * ln * 0.05, hw * 1.35)
    d1 = P2(tx - ux * ln * 0.35, ty - uy * ln * 0.35, -hw * 1.0)
    d2 = P2(bx + ux * ln * 0.05, by + uy * ln * 0.05, -hw * 1.35)
    s = "M" + _p(a)
    s += ("Q" + _p(t) + " " + _p(c)) if k else ("L" + _p(t) + "L" + _p(c))
    s += "C" + _p(d1) + " " + _p(d2) + " " + _p(b) + "C" + _p(c2) + " " + _p(c1) + " " + _p(a) + "Z"
    return s


def ell(cx, cy, rx, ry, deg=0):
    return rot(ellipse(cx, cy, rx, ry), deg, cx, cy) if deg else ellipse(cx, cy, rx, ry)


def sp(x, y, r=0.9):
    return dot(x, y, r)



def _flame(cx, cy, rx, ry, a, S, w=16, h=3.4, lean=24):
    """Pointed scale tip poking out of an ellipse at angle a, leaning towards the top."""
    toward = -1 if (a % 360) < 90 or (a % 360) > 270 else 1
    b1, b2 = math.radians(a - w / 2), math.radians(a + w / 2)
    ta = math.radians(a + toward * lean)
    k = 1 + h / ((rx + ry) / 2)
    return poly([(cx + rx * 0.8 * math.cos(b1), cy + ry * 0.8 * math.sin(b1)),
                 (cx + rx * k * math.cos(ta), cy + ry * k * math.sin(ta)),
                 (cx + rx * 0.8 * math.cos(b2), cy + ry * 0.8 * math.sin(b2))], closed=True, r=L(S, 0, 0.5))


# =========================================================================== chunk 1: herbs, grains, mushrooms

@icon("sea-grapes", CAT, "Three short stalks strung with tiny round bead bubbles",
      tags=["umibudo", "caulerpa", "sea vegetable", "seaweed", "green caviar", "produce"])
def _(S):
    out = []
    for x, top, par in ((5.6, 7.6, 0), (12, 3.6, 1), (18.4, 7.6, 0)):
        out.append(line(seg(x, 21.6, x, top)))
        y = top + 1.4
        side = 1 if par else -1
        while y < 18:
            out.append(dot(x + side * 2.3, y, 1.5))
            side = -side
            y += 3.4
    return out


@icon("microgreens", CAT, "Small tray packed with upright tiny sprouts each topped with two seed leaves",
      tags=["sprouts", "seedlings", "shoots", "baby greens", "tray", "produce"])
def _(S):
    out = [shell(poly([(3.5, 15), (20.5, 15), (18.5, 21), (5.5, 21)], closed=True, r=S.r))]
    for x, t in ((6.8, 8.6), (12, 5.6), (17.2, 8.6)):
        out.append(line(poly([(x - 2.4, t - 2.4), (x, t), (x + 2.4, t - 2.4)], r=S.r)))
        out.append(line(seg(x, t, x, 14.6)))
    return out


@icon("amaranth", CAT, "Leafy stalk with a long drooping rope like tassel of tiny grains",
      tags=["grain", "pseudocereal", "love lies bleeding", "tassel", "greens", "produce"])
def _(S):
    rope = beads([(10, 9.4), (12, 6.8), (15, 5.6), (18, 7), (19.4, 10), (19.4, 13.2), (18.8, 16.2)], 2.2)
    return [shell(rope), line("M8 21.6C8 16 8.4 13.4 9.6 10"), shell(leaf(8.1, 18.4, 3, 14.8, 1.6)),
            shell(leaf(8.4, 15.6, 13.6, 14.6, 1.4))]


@icon("rapeseed", CAT, "Tall stem topped with four petal flowers and slender seed pods",
      tags=["canola", "oilseed", "yellow field", "brassica", "flowers", "produce"])
def _(S):
    def clover(cx, cy, r=1.8, o=2.0):
        return union(*[circle(cx + o * math.cos(math.radians(a)), cy + o * math.sin(math.radians(a)), r) for a in (0, 90, 180, 270)])
    return [shell(clover(12, 5.6)), shell(clover(5.6, 9.6, 1.5, 1.7)), shell(clover(18.4, 9.6, 1.5, 1.7)),
            line("M12 10V22"), line("M12 20L7 15.2"), line("M12 17.4L17.4 12.6"),
            line("M12 13.4L9.4 11.4")]


@icon("sorrel-leaf", CAT, "Arrow shaped leaf with two pointed lobes at the base and a long stem",
      tags=["sorrel", "dock", "sour leaf", "herb", "leafy green", "produce"])
def _(S):
    body = ("M12 2.4C16.6 5.4 18 9.6 17.4 13.6C19.4 14.4 21 16.6 22 19.8C19 20.4 15.6 19.4 13 17.6L12 16.8"
            "L11 17.6C8.4 19.4 5 20.4 2 19.8C3 16.6 4.6 14.4 6.6 13.6C6 9.6 7.4 5.4 12 2.4Z")
    return [shell(body), detail("M12 6.6V14"), line("M12 17V22")]


@icon("chamomile", CAT, "Sprig of two daisy flowers with domed centres on thin stems",
      tags=["camomile", "daisy", "herbal tea", "flowers", "calming", "produce"])
def _(S):
    def daisy(cx, cy):
        out = [dot(cx, cy, 1.6)]
        for i in range(8):
            a = -90 + i * 45
            out.append(line(seg(*pt_(cx, cy, 3.0, a), *pt_(cx, cy, 4.8, a))))
        return out
    return [*daisy(7.2, 7.4), *daisy(16.8, 12.4), line("M7.2 12.4C7.2 16.6 9.6 20 12 22"),
            line("M16.8 17.4C16.8 19.6 14.6 21 12 22")]


@icon("elderflower", CAT, "Flat umbrella cluster of many tiny flowers on radiating stalks",
      tags=["elder", "umbel", "cordial", "blossom", "wild flower", "produce"])
def _(S):
    ends = [(4.4, 11), (7.6, 6.4), (12, 4.6), (16.4, 6.4), (19.6, 11)]
    out = [line("M12 22V13.4")]
    for x, y in ends:
        out.append(line(seg(12, 13.4, x, y + (1.4 if abs(x - 12) > 6 else 1.6))))
        out.append(dot(x, y, 1.9))
    out += [dot(9.6, 9.6, 1.4), dot(14.4, 9.6, 1.4)]
    return out


@icon("long-pepper", CAT, "Two small elongated beaded catkin spikes on thin stems",
      tags=["pippali", "piper longum", "spice", "catkin", "peppercorn", "produce"])
def _(S):
    a = beads([(6.6, 4.6), (7.2, 7.4), (7.8, 10.2), (8.4, 13)], 2.0)
    b = beads([(15.4, 3.8), (16, 6.6), (16.6, 9.4), (17.2, 12.2)], 2.0)
    return [shell(a), shell(b), line("M8.4 15L10.6 21.5"), line("M17.2 14.2C16 17 14 19 11.6 21.5")]


@icon("sichuan-pepper", CAT, "Small pile of split open round husks with hollow centres",
      tags=["szechuan pepper", "prickly ash", "mala", "spice", "husk", "produce"])
def _(S):
    out = []
    for cx, cy, sa in ((7, 7.6, 135), (17, 7.6, 45), (12, 15.8, 90)):
        husk = minus(circle(cx, cy, 3.5), poly([(cx, cy - 0.4), (cx - 2.6, cy - 5), (cx + 2.6, cy - 5)], closed=True))
        a, b = pt_(cx, cy, 3.5, sa), pt_(cx, cy, 5.6, sa)
        out += [shell(husk), dot(cx, cy + 0.8, 0.9), line(seg(*a, *b))]
    return out


@icon("maitake", CAT, "Frilly rosette mushroom made of overlapping wavy fronds from one base",
      tags=["hen of the woods", "ruffled mushroom", "fungus", "mushroom", "forage", "produce"])
def _(S):
    cap = union(circle(12, 12.6, 6.8), circle(5.6, 12.4, 3.4), circle(18.4, 12.4, 3.4), circle(8.2, 7.6, 3.2),
                circle(15.8, 7.6, 3.2), circle(12, 6.2, 3.2))
    return [shell(cap), shell(rect(9.4, 17, 5.2, 4.6, L(S, 0.4, 2))),
            detail("M6.6 11.4Q8.4 9.4 10.2 11.4T13.8 11.4T17.4 11.4"),
            detail("M7.8 15.2Q9.6 13.4 11.4 15.2T15 15.2")]


@icon("shimeji", CAT, "Cluster of small round capped mushrooms on short stems from one shared base",
      tags=["beech mushroom", "clamshell mushroom", "buna", "mushroom", "fungus", "produce"])
def _(S):
    def cap(cx, cy, r):
        return f"M{fmt(cx - r)} {fmt(cy)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx + r)} {fmt(cy)}Z"
    return [shell(cap(6, 12, 3.2)), shell(cap(12, 6.4, 3.4)), shell(cap(18, 12, 3.2)),
            line("M6 12C6 16 9.6 17.6 10.6 20.4"), line("M12 6.4V20.4"), line("M18 12C18 16 14.4 17.6 13.4 20.4"),
            line("M8.4 21.6H15.6")]


def _cotw():
    def fan(y, w, h):
        return (f"M5 {fmt(y)}L{fmt(5 + w)} {fmt(y + h * 0.35)}C{fmt(5 + w + 1)} {fmt(y + h * 0.8)} {fmt(5 + w * 0.45)} {fmt(y + h)} 5 {fmt(y + h)}Z")
    return fan(2.6, 13, 7.6), fan(8.8, 17, 7.6), fan(15, 13, 6.6)


@icon("chicken-of-the-woods", CAT, "Stacked fan shaped shelf fungus brackets growing from a tree edge",
      tags=["sulphur shelf", "bracket fungus", "shelf mushroom", "forage", "wild mushroom", "produce"],
      filled=lambda: layered(_cotw()))
def _(S):
    a, b, c = _cotw()
    return [shell(cut(a, b, c, g=0.001)), shell(cut(b, c, g=0.001)), shell(c), line("M3.5 2.4V21.6")]


@icon("black-trumpet", CAT, "Tall hollow trumpet shaped mushroom with a ruffled flared rim",
      tags=["trumpet of death", "horn of plenty", "craterellus", "mushroom", "fungus", "produce"])
def _(S):
    pts = [(10.6, 21.6), (10.6, 16.6), (8.4, 11.6), (4.4, 6.4), (7, 4.6), (9.6, 6.6), (12, 4.2), (14.4, 6.6),
           (17, 4.6), (19.6, 6.4), (15.6, 11.6), (13.4, 16.6), (13.4, 21.6)]
    return [shell(smooth(pts)), detail("M8.4 7.6Q12 11.2 15.6 7.6")]


# =========================================================================== chunk 2: plants, roots, kitchen

def _straw():
    egg = "M12 2.8C15.8 2.8 17.4 7.6 17.4 10.6C17.4 14.2 15 16.4 12 16.4C9 16.4 6.6 14.2 6.6 10.6C6.6 7.6 8.2 2.8 12 2.8Z"
    cup = "M4.6 13.8C4.6 19 8 21.4 12 21.4C16 21.4 19.4 19 19.4 13.8C17.4 15 6.6 15 4.6 13.8Z"
    return egg, cup


@icon("straw-mushroom", CAT, "Egg shaped closed mushroom cap emerging from a cup shaped sac at its base",
      tags=["paddy straw mushroom", "volvariella", "mushroom", "fungus", "asian cooking", "produce"],
      filled=lambda: layered(_straw()))
def _(S):
    egg, cup = _straw()
    return [shell(cut(egg, cup, g=0.001)), shell(cup)]


@icon("pea-plant", CAT, "Climbing stem with a curly tendril, oval leaves and two hanging pea pods",
      tags=["peas", "garden pea", "pod", "vine", "legume", "produce"])
def _(S):
    out = [line("M12 22V6C12 3.4 14.6 2.4 16 3.8C17 4.8 16 6 14.8 5.6"), line("M12 9.6H6.6V11.2"), line("M12 9.6H17.4V11.2"),
           shell(beads([(6.6, 14.2), (6.6, 17.4), (6.6, 20.6)], 2.0)), shell(beads([(17.4, 14.2), (17.4, 17.4), (17.4, 20.6)], 2.0)),
           shell(rot(ellipse(7.6, 5.4, 3.2, 1.9), -25, 7.6, 5.4))]
    return out


@icon("pumpkin-vine", CAT, "Small pumpkin on a curling vine with a broad lobed leaf and a spiral tendril",
      tags=["pumpkin", "squash", "vine", "garden", "autumn", "produce"])
def _(S):
    lf = union(circle(17.4, 10.6, 2.6), circle(20.2, 14, 2.6), circle(18, 18, 2.6), circle(14.6, 15, 2.6), circle(17.6, 14.4, 3.2))
    return [shell(ellipse(8.4, 16.4, 5.4, 4.6)), detail("M8.4 12C6.8 14.4 6.8 18.4 8.4 20.8"),
            line("M8.4 11.8V9.6C8.4 6.4 12 4.6 16.2 5.4"), line("M16.2 5.4L17.4 8.2"), shell(lf),
            line("M8.4 8.6C6.6 8.2 4.8 7.6 4.4 5.8C4.2 4.6 5.6 3.8 6.6 4.6")]


@icon("carrot-in-ground", CAT, "Carrot buried below a soil line with its feathery leafy top above ground",
      tags=["carrot", "root vegetable", "soil", "garden", "harvest", "produce"])
def _(S):
    root = "M7 12.8H17C16.6 16.2 14.4 19.2 12 20.8C9.6 19.2 7.4 16.2 7 12.8Z"
    return [shell(root), line("M2 12.8H5.4"), line("M18.6 12.8H22"), line("M12 12V3.4"), line("M12 11.6C11.4 8.6 9.6 6.6 7.2 5.4"),
            line("M12 11.6C12.6 8.6 14.4 6.6 16.8 5.4")]


@icon("celeriac", CAT, "Knobbly round root with a tangle of roots below and short cut stalks on top",
      tags=["celery root", "root vegetable", "knob celery", "winter vegetable", "soup", "produce"])
def _(S):
    body = blob(12, 10.8, 8.4, 5.8, [1, 0.95, 1.05, 0.95, 1.02, 0.94, 1.04, 0.96, 1.0, 0.94, 1.05, 0.96])
    return [shell(body), line("M9.2 5.6L8.6 2.6"), line("M14.8 5.6L15.4 2.6"), line("M12 5.2V2.4"),
            line("M7.4 15.8C7 18.4 5.8 20 4 20.8"), line("M10 16.6C9.8 19 9 20.6 7.8 21.8"), line("M12 16.8V22"),
            line("M14 16.6C14.2 19 15 20.6 16.2 21.8"), line("M16.6 15.8C17 18.4 18.2 20 20 20.8")]


@icon("parsnip", CAT, "Wide shouldered tapering root with fine ring lines and short cut stalks",
      tags=["root vegetable", "winter vegetable", "roast", "white carrot", "tapering", "produce"])
def _(S):
    tipd = "L12 22" if S.name == "line" else "L12.4 21.4Q12 22.4 11.6 21.4"
    body = ("M7 7.6C7 6 9.4 5.8 12 6.8C14.6 5.8 17 6 17 7.6C17 12 14.6 16.6 12.6 21.2" +
            ("L12 22L11.4 21.2" if S.name == "line" else "Q12 22.6 11.4 21.2") +
            "C9.4 16.6 7 12 7 7.6Z")
    return [shell(body), line("M10.4 6.2L9.8 2.6"), line("M13.8 6L14.6 2.6"), detail(seg(9.4, 11.4, 12.4, 11.4)),
            detail(seg(10.4, 14.8, 12.6, 14.8))]


@icon("horseradish", CAT, "Long gnarled uneven root with a small heap of grated shreds beside it",
      tags=["root", "condiment", "grated", "spicy", "wasabi", "produce"])
def _(S):
    root = smooth([(3.4, 6.4), (5.6, 4.2), (8.8, 4.8), (11.8, 6.6), (15.2, 7.8), (18.6, 9.4), (21.6, 11.2), (18.6, 12.4),
                   (14.8, 11.6), (11.2, 11.2), (7.4, 10.8), (4.2, 10)])
    shreds = [((4.6, 20.4), 20), ((8, 20.6), -30), ((11.4, 20.4), 40), ((14.8, 20.6), -15),
              ((6.2, 17.6), -40), ((9.6, 17.8), 25), ((13, 17.6), -35), ((8, 15), 35), ((11.4, 15.2), -20)]
    out = [shell(root), line("M17.2 12.4L19.6 15.6"), line("M13 11.6L14 14.4")]
    for (x, y), a in shreds:
        dx, dy = 1.3 * math.cos(math.radians(a)), 1.3 * math.sin(math.radians(a))
        out.append(line(seg(x - dx, y - dy, x + dx, y + dy)))
    return out


@icon("radicchio", CAT, "Round compact head of leaves with bold branching vein lines",
      tags=["chicory", "italian chicory", "red salad leaf", "lettuce", "salad", "produce"])
def _(S):
    return [shell(circle(12, 12.4, 8.8)), detail("M12 20.4C6.4 18.4 5.4 11 8.6 5"), detail("M12 20.4C17.6 18.4 18.6 11 15.4 5"),
            detail(poly([(12, 20.4), (12, 6)], r=S.r))]


@icon("luffa", CAT, "Long cylindrical gourd with sharp lengthwise ridges from stem to tip",
      tags=["loofah", "sponge gourd", "vegetable", "bath sponge", "gourd", "produce"])
def _(S):
    def rp_(pts):
        return rpts(pts, 28, 12, 13)
    body = smooth(rp_([(10.4, 4.8), (13.6, 4.8), (15.2, 9), (16.8, 14), (16.4, 19), (14, 21.6), (10, 21.6), (7.6, 19),
                       (7.2, 14), (8.8, 9)]))
    (a, b), (c, d) = rp_([(12, 4.8), (12, 2.2)])
    r1 = rp_([(10, 8), (9.6, 13), (10.2, 18)])
    r2 = rp_([(14, 8), (14.4, 13), (13.8, 18)])
    return [shell(body), line(seg(a, b, c, d)), detail(smooth(r1, closed=False)), detail(smooth(r2, closed=False))]


@icon("preserving-jar", CAT, "Glass jar with a screw band lid holding halved fruit pieces",
      tags=["canning jar", "mason jar", "preserves", "jam", "pickling", "produce"])
def _(S):
    body = rect(5, 9.2, 14, 12.4, L(S, 2, 4))
    lid = rect(6.6, 3.4, 10.8, 4.6, L(S, 1, 2))
    return [shell(body), shell(lid), dot(9.6, 16.8, 1.9), dot(14.4, 16.8, 1.9), dot(12, 13.2, 1.5)]


@icon("spice-rack", CAT, "Small wall shelf holding three spice jars with lids in a row",
      tags=["spice jars", "spices", "shelf", "kitchen storage", "seasoning", "produce"])
def _(S):
    out = [line("M2 20.6H22")]
    for x in (3, 10, 17):
        out.append(shell(rect(x, 9.2, 3.6, 9, L(S, 0.6, 1.4))))
        out.append(solid(rect(x - 0.7, 5, 5, 3.2, L(S, 0, 1))))
    return out


@icon("banana-hanger", CAT, "Stand with a curved hook arm holding a hanging bunch of bananas",
      tags=["banana stand", "fruit hook", "kitchen", "counter", "bananas", "produce"])
def _(S):
    b1 = "M16.2 8.6C12.6 11.8 12.4 16.2 14.4 19.8C16.2 17 16.4 12.6 18 9.2Z"
    b2 = "M17.6 8.8C16 12.2 16.4 16.2 18.4 20C20 16.6 19.8 12.2 18.8 9Z"
    b3 = "M18.8 8.6C21.4 11.4 22.2 15 21.2 18.8C19.6 16 19.2 12.6 18.2 9.2Z"
    return [line("M10 21.6V6.4C10 4.2 11.6 3 13.6 3C15.6 3 17.2 4 17.2 6V8.6"), line("M5.4 21.6H14.6"),
            solid(b1), solid(b2), solid(b3)]


@icon("olive-oil", CAT, "Tall bottle with a narrow neck and a small olive and leaf on its front",
      tags=["cooking oil", "extra virgin", "bottle", "mediterranean", "salad dressing", "produce"])
def _(S):
    body = ("M10.4 3.4H13.6V8C13.6 10.4 17.4 10.6 17.4 14.4V20C17.4 21 16.6 21.8 15.6 21.8H8.4C7.4 21.8 6.6 21 6.6 20"
            "V14.4C6.6 10.6 10.4 10.4 10.4 8Z")
    return [shell(body), solid(ellipse(10.8, 17, 1.7, 2.2)), detail("M12.4 15.6C13.4 14.2 14.4 13.6 15.6 13.4"),
            line("M9.6 3.4H14.4")]


# =========================================================================== chunk 3: groups, leaves and kitchen scenes

def _stone():
    peach = ("M7 12.4C5 10.8 2.6 12.4 2.6 15.6C2.6 18.6 4.6 20.2 7 20.2C9.4 20.2 11.4 18.6 11.4 15.6C11.4 12.4 9 10.8 7 12.4Z")
    plum = ellipse(16.8, 16.2, 3.2, 3.9)
    return peach, plum


@icon("stone-fruits", CAT, "A peach, a plum and a pair of cherries grouped together",
      tags=["drupes", "peach", "plum", "cherry", "summer fruit", "produce"])
def _(S):
    peach, plum = _stone()
    return [shell(peach), shell(plum), detail("M15.6 14.6C16.4 15.6 16.4 17.2 15.8 18.2"), dot(8.8, 7.2, 2.2), dot(15.2, 7.2, 2.2),
            line("M8.8 5L12 2.6"), line("M15.2 5L12 2.6")]


def _alliums():
    leek = rect(16.2, 5.4, 4, 15.4, 1.4)
    onion = ("M7 7.6C8.4 9.6 11.4 10.8 11.4 14.8C11.4 17.8 9.4 19.8 7 19.8C4.6 19.8 2.6 17.8 2.6 14.8C2.6 10.8 5.6 9.6 7 7.6Z")
    garlic = ("M13.4 9.8C14.4 11.6 17.6 13 17.6 16.6C17.6 19.6 15.8 21.2 13.4 21.2C11 21.2 9.2 19.6 9.2 16.6C9.2 13 12.4 11.6 13.4 9.8Z")
    return leek, onion, garlic


@icon("alliums", CAT, "An onion, a garlic bulb and a leek grouped together",
      tags=["onion", "garlic", "leek", "aromatics", "vegetables", "produce"],
      filled=lambda: layered(_alliums()))
def _(S):
    leek, onion, garlic = _alliums()
    return [shell(cut(leek, onion, garlic, g=0.001)), shell(cut(onion, garlic, g=0.001)), shell(garlic),
            line("M18.2 5.4L16.2 2.6"), line("M18.2 5.4L20.2 2.6"), line("M18.2 5.4V2.4"), line("M7 7.8L7 4.4"), line("M7 20L6 22"), detail("M13.4 12.6C12 14.6 12 17.8 13.4 19.8")]


@icon("herbs-and-spices", CAT, "A basil sprig, a cinnamon stick and a star anise grouped together",
      tags=["basil", "cinnamon", "star anise", "seasoning", "cooking", "produce"])
def _(S):
    pts = []
    for i in range(16):
        a = math.radians(-90 + i * 22.5)
        r = 4.8 if i % 2 == 0 else 2.9
        pts.append((7.4 + r * math.cos(a), 8 + r * math.sin(a)))
    star = poly(pts, closed=True, r=S.r * 0.4)
    stick = rot(rect(12.8, 3.4, 4.8, 12, L(S, 1, 2.4)), 40, 15.2, 9.4)
    return [shell(star), dot(7.4, 8, 1.1), shell(stick),
            line("M3.6 21.6C5 19.2 7.4 17.2 10.4 16.2"), shell(leaf(6.2, 19, 2.4, 14.6, 1.6)),
            shell(leaf(8.4, 17.4, 13.8, 17.6, 1.8))]


@icon("splattered-tomato", CAT, "Squashed tomato bursting into a splat shape with droplets flying out",
      tags=["splat", "squashed", "rotten tomato", "mess", "throwing", "produce"])
def _(S):
    radii = [8.2, 4.8, 6.2, 4.6, 8, 4.6, 5.6, 5, 7.6, 4.6, 6.4, 4.8]
    pts = [(12 + r * math.cos(math.radians(-90 + i * 30)), 12 + r * math.sin(math.radians(-90 + i * 30))) for i, r in enumerate(radii)]
    body = smooth(pts) if S.name == "rounded" else poly(pts, closed=True)
    return [shell(body), dot(12.4, 12, 1.5), dot(3.6, 4, 1.3), dot(20.6, 3.8, 1.1), dot(21, 20.4, 1.3), dot(3.2, 19.6, 1.1)]


@icon("nasturtium-leaf", CAT, "Round shield shaped leaf with veins radiating from a central stem point, beside a small flower",
      tags=["nasturtium", "edible flower", "peppery leaf", "garden", "salad", "produce"])
def _(S):
    out = [shell(circle(8, 9.6, 6.2)), line("M8 10.4C8 15 8.6 18.4 9.6 21.8")]
    for a in (-160, -120, -80, -40, 0):
        out.append(detail(seg(*pt_(8, 9.6, 1.4, a), *pt_(8, 9.6, 4.2, a))))
    bloom = union(*[circle(*pt_(18.4, 15, 2.5, -90 + i * 72), 1.7) for i in range(5)])
    out += [shell(bloom), dot(18.4, 15, 1.0), line("M18.4 19.6L17.4 22")]
    return out


@icon("wild-garlic", CAT, "Two broad lance shaped leaves with a stalk topped by a small cluster of star flowers",
      tags=["ramsons", "bear's garlic", "allium ursinum", "forage", "spring herb", "produce"])
def _(S):
    out = [shell(leaf(10.8, 21.6, 3.6, 11.2, 3.2)), shell(leaf(13.2, 21.6, 20.4, 11.2, 3.2)), line("M12 22V9.4"),
           detail("M9.6 18.4L6.4 13.6"), detail("M14.4 18.4L17.6 13.6")]
    for x, y in ((12, 3.8), (8.8, 5.6), (15.2, 5.6), (10.2, 9), (13.8, 9)):
        out.append(dot(x, y, 1.5))
    return out


@icon("annatto-pod", CAT, "Spiky heart shaped pod split open showing a mass of small seeds inside",
      tags=["achiote", "urucum", "bixa", "seed pod", "natural dye", "produce"])
def _(S):
    pts = []
    n = 22
    for i in range(n):
        t = 2 * math.pi * i / n
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        cx, cy = 12 + x * 0.44, 12.6 + y * 0.44
        if i % 2 == 1:
            dx, dy = cx - 12, cy - 12.6
            ln = math.hypot(dx, dy)
            cx, cy = cx + dx / ln * 2.0, cy + dy / ln * 2.0
        pts.append((cx, cy))
    seeds = [(9.4, 9.4), (12.6, 10.4), (15.2, 9.2), (8.4, 12.6), (11.2, 13.4), (14.2, 12.8), (16.2, 12.6), (10.4, 16.2),
             (13.2, 16.6), (12, 19.4)]
    return [shell(poly(pts, closed=True, r=L(S, 0, 0.5))), *[dot(x, y, 0.9) for x, y in seeds]]


@icon("sprouting-jar", CAT, "Glass jar tipped on its side with a mesh lid and small seeds sprouting tiny tails inside",
      tags=["sprouts", "seed sprouting", "mason jar", "alfalfa", "mung bean", "produce"])
def _(S):
    A = -105

    def rt(pts):
        return rpts(pts, A, 12, 12)
    body = rot(rect(5.8, 7.8, 12.4, 12.6, L(S, 2, 4)), A, 12, 12)
    lid = rot(rect(7.4, 3.4, 9.2, 4.2, L(S, 0.6, 1.4)), A, 12, 12)
    out = [shell(body), shell(lid)]
    for (x, y) in ((9, 13.6), (13.4, 12), (11, 17.4)):
        p0, p1, p2 = rt([(x, y), (x + 1.8, y + 1.4), (x + 3, y + 3.6)])
        out.append(dot(*p0, 1.2))
        out.append(line("M" + _p(p0) + "Q" + _p(p1) + " " + _p(p2)))
    return out
