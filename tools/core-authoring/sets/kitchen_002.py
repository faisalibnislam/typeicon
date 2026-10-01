"""TypeIcon Core: kitchen (batch kitchen_002): knives, prep tools, storage, tableware and cooking actions.

Knives and long hand tools are drawn upright and turned 45 degrees clockwise so the handle points to the
bottom-left and the blade to the top-right (edge facing down-right), matching kitchen_001 and the tools set.
Containers and tableware are drawn in side view, or from above when the top is what identifies them.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path.parser import parse_path
from geometry import SCALE, D, I, P, ST, U, fmt, path_to_d, rotation

CAT = "kitchen"
TILT = 45


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def tf(d, m):
    """Apply an affine matrix (a, b, c, d, e, f) to a d-string, keeping open paths open."""
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def rot(d, deg=TILT, cx=12.0, cy=12.0):
    """Rotate a d-string clockwise on screen about (cx, cy)."""
    return tf(d, rotation(deg, cx, cy))


def mv(d, dx, dy):
    return tf(d, (1, 0, 0, 1, dx, dy))


def flip(d):
    """Mirror across the vertical centre line."""
    return tf(d, (-1, 0, 0, 1, 24, 0))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def hole(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def fit(parts, cx=12.0, cy=12.0):
    """Translate parts so their drawn bounds are centred on (cx, cy), snapped to half pixels."""
    regions = []
    for p in parts:
        regions.append(P(p.d) if p.kind in ("shell", "dot", "solid") else ST(p.d, 2.0))
    x0, y0, x1, y1 = U(*regions).bounds
    dx = round((cx - (x0 + x1) / 2 / SCALE) * 2) / 2
    dy = round((cy - (y0 + y1) / 2 / SCALE) * 2) / 2
    if dx == 0 and dy == 0:
        return parts
    return [Part(p.kind, mv(p.d, dx, dy), p.attrs) for p in parts]


def tilt(parts, deg=TILT):
    """Turn an upright utensil (handle down) so the handle points to the bottom-left, then centre it."""
    return fit([Part(p.kind, rot(p.d, deg), p.attrs) for p in parts])


def rpoly(S, pts, closed=True, k=1.0):
    return poly(pts, closed=closed, r=S.r * k)


# ============================================================================ knives

@icon("chef-knife", CAT, "Chef's knife with a broad blade tapering to a point and a riveted handle",
      tags=["cook's knife", "kitchen knife", "chopping", "slicing", "cutting", "cutlery"], aliases=["cooks-knife"])
def _(S):
    blade = f"M9.5 14V{L(S, 1, 1.5)}C14 4 16.5 8.5 16.5 14Z"
    body = union(blade, rect(9.5, 13.5, 4.5, 9, rr(S, 2)))
    return tilt([shell(body, stroke_miterlimit="2"), detail(seg(9.5, 14, 16.5, 14)),
                 dot(11.75, 17.3, 0.9), dot(11.75, 20, 0.9)])


def _scallops(x, y0, y1, n, depth):
    """Serrated edge running up from (x, y0) to (x, y1) as n outward scallops."""
    step = (y0 - y1) / n
    out = ""
    for i in range(n):
        ya = y0 - i * step
        yb = ya - step
        out += f"Q{fmt(x + depth)} {fmt((ya + yb) / 2)} {fmt(x)} {fmt(yb)}"
    return out


@icon("bread-knife", CAT, "Bread knife with a long straight blade, a serrated edge and a handle",
      tags=["serrated knife", "bread", "slicing", "loaf", "baking", "cutlery"])
def _(S):
    edge = "M10 13.5H14" + _scallops(14, 13.5, 5, 4, 1.6)
    top = "A2 2 0 0 0 10 5Z" if S.name == "rounded" else "V4L12.5 2.5H10Z"
    body = union(edge + top, rect(9.75, 13, 4.5, 8.5, rr(S, 2)))
    return tilt([shell(body, stroke_miterlimit="2"), detail(seg(9.75, 13.5, 14.25, 13.5))])


@icon("paring-knife", CAT, "Small paring knife with a short pointed blade and a longer handle",
      tags=["small knife", "peeling", "trimming", "fruit knife", "cutting", "cutlery"])
def _(S):
    blade = f"M10 11.5V{L(S, 3.5, 4)}C12.8 5.5 14 8.5 14 11.5Z"
    body = union(blade, rect(10, 11, 4, 11, rr(S, 2)))
    return tilt([shell(body, stroke_miterlimit="2"), detail(seg(10, 11.5, 14, 11.5))])


@icon("cleaver", CAT, "Meat cleaver with a broad rectangular blade, a hanging hole and a short handle",
      tags=["meat cleaver", "chopper", "butcher", "chopping", "bones", "cutlery"], aliases=["meat-cleaver"])
def _(S):
    blade = rect(9, 5, 12.5, 12, rr(S, 2))
    handle = rect(2, 6.5, 7, 3.5, L(S, 0.5, 1.75))
    return [shell(union(blade, handle)), detail(seg(9, 6.5, 9, 10)), dot(18, 8.5, 1.3)]


@icon("santoku-knife", CAT, "Santoku knife with a straight edge, a rounded tip and dimples along the blade",
      tags=["japanese knife", "granton edge", "chopping", "slicing", "vegetables", "cutlery"], aliases=["santoku"])
def _(S):
    blade = f"M9.5 14V7.5C9.5 4 12 1.5 16 1.5V14Z" if S.name == "rounded" else "M9.5 14V8C9.5 4.5 12 1.5 16 1.5V14Z"
    body = union(blade, rect(9.5, 13.5, 4.5, 9, rr(S, 2)))
    return tilt([shell(body, stroke_miterlimit="2"), detail(seg(9.5, 14, 16, 14)),
                 dot(13.6, 6, 0.9), dot(13.6, 10, 0.9)])


@icon("boning-knife", CAT, "Boning knife with a narrow curved blade, a bolster and a handle",
      tags=["fillet knife", "deboning", "butcher", "meat", "fish", "cutlery"])
def _(S):
    blade = "M10.5 12V1.5C12.8 3 14 6 14 9V12Z"
    bolster = rect(9, 12, 6.5, 2.5, L(S, 0, 1))
    body = union(blade, bolster, rect(10, 14, 4.5, 8.5, rr(S, 2)))
    return tilt([shell(body, stroke_miterlimit="2"), detail(seg(9, 14.5, 15.5, 14.5))])


@icon("butter-knife", CAT, "Butter knife with a short rounded blunt blade and a plain handle",
      tags=["table knife", "spreader", "butter", "breakfast", "dinner knife", "cutlery"], aliases=["table-knife"])
def _(S):
    blade = ("M9.5 11.5V5.5A2.75 2.75 0 0 1 15 5.5V11.5C15 12.5 13.5 13 13.5 14H11C11 13 9.5 12.5 9.5 11.5Z"
             if S.name == "rounded" else "M9.5 11.5V4.5L12 2.8C14 3.3 15 4.8 15 7V11.5L13.5 14H11Z")
    handle = "M11 13.5H13.5L14.2 20.5A1.95 1.95 0 0 1 10.3 20.5Z"
    return tilt([shell(union(blade, handle), stroke_miterlimit="2")])


@icon("oyster-knife", CAT, "Oyster knife with a short stubby pointed blade, a round guard and a bulbous handle",
      tags=["shucking knife", "oyster shucker", "shellfish", "seafood", "clams", "cutlery"], aliases=["oyster-shucker"])
def _(S):
    blade = "M10.5 10V5L12.25 2.5L14 5V10Z" if S.name == "line" else "M10.5 10V5.5C10.5 4 11.25 3 12.25 2.5C13.25 3 14 4 14 5.5V10Z"
    guard = ellipse(12.25, 11, 4.5, 1.6)
    handle = ellipse(12.25, 17, 3.2, 4.8)
    return tilt([shell(union(blade, guard, handle)), detail("M9 11H15.5")])


@icon("carving-fork", CAT, "Carving fork with two long tines, a small guard and a straight handle",
      tags=["meat fork", "roast", "carving", "serving fork", "two prong fork", "cutlery"], aliases=["meat-fork"])
def _(S):
    tines = "M9 1.5V8A3 3 0 0 0 15 8V1.5" if S.name == "rounded" else "M9 1.5V11H15V1.5"
    return tilt([line(tines), line(seg(12, 11, 12, 13)), shell(rect(9.5, 13, 5, 2, L(S, 0, 1))),
                 shell(rect(10.5, 15, 3, 7.5, L(S, 0.5, 1.5)))])


@icon("honing-steel", CAT, "Honing steel: a long ribbed rod with a round guard, a handle and a hanging ring",
      tags=["sharpening steel", "knife sharpener", "honing rod", "butcher's steel", "sharpen", "knife care"],
      aliases=["sharpening-steel"])
def _(S):
    rod = "M10.75 12V2.5A1.25 1.25 0 0 1 13.25 2.5V12Z" if S.name == "rounded" else "M10.75 12V1.5H13.25V12Z"
    ring = circle(12, 21.5, 1.5) if S.name == "rounded" else rect(10.5, 20, 3, 3)
    return tilt([shell(rod), shell(ellipse(12, 13, 3.5, 1.25)), shell(rect(10, 14.25, 4, 5.5, L(S, 0.5, 1.5))),
                 line(ring)])


@icon("mezzaluna", CAT, "Mezzaluna: a curved crescent blade with an upright handle at each end",
      tags=["rocking knife", "herb chopper", "hachoir", "chopping herbs", "crescent knife", "chopper"],
      aliases=["herb-chopper"])
def _(S):
    blade = "M3 12Q12 15.5 21 12A9.8 9.8 0 0 1 3 12Z"
    grip = rect(2.5, 3, 3.5, 6.5, rr(S, 1.75))
    parts = [shell(blade), shell(grip), shell(flip(grip)), line(seg(4.25, 9.5, 4.25, 11.8)),
             line(seg(19.75, 9.5, 19.75, 11.8))]
    return fit([Part(p.kind, rot(p.d, -18), p.attrs) for p in parts])


@icon("ulu-knife", CAT, "Ulu knife: a half-moon blade with a handle joined to the middle of its top edge",
      tags=["ulu", "inuit knife", "half moon knife", "rocking knife", "chopping", "cutting"], aliases=["ulu"])
def _(S):
    blade = ("M4 13H9.5L12 10.5L14.5 13H20C20 17.5 16.5 21 12 21C7.5 21 4 17.5 4 13Z" if S.name == "rounded"
             else "M4 13H9.5L12 10.5L14.5 13H20L18.8 16.8C17.5 19.5 15 21 12 21C9 21 6.5 19.5 5.2 16.8Z")
    parts = [shell(blade, stroke_miterlimit="2"), shell(rect(5, 3, 14, 4, rr(S, 2))), line(seg(12, 7, 12, 10.5))]
    return fit([Part(p.kind, rot(p.d, -18), p.attrs) for p in parts])


# ============================================================================ hand utensils

@icon("chopsticks", CAT, "Pair of long tapered chopsticks lying side by side at a slight angle",
      tags=["eating sticks", "asian food", "noodles", "sushi", "rice", "utensils"])
def _(S):
    a = [(6, 2), (9.5, 2), (10.5, 22), (9.5, 22)]
    b = [(12.5, 2), (16, 2), (14.5, 22), (13.5, 22)]
    return tilt([shell(rpoly(S, a, k=0.4)), shell(rpoly(S, b, k=0.4)),
                 detail(seg(6.2, 6, 9.7, 6)), detail(seg(12.3, 6, 15.8, 6))], deg=30)


@icon("rice-paddle", CAT, "Rice paddle: a flat paddle with a round wide end and a short straight handle",
      tags=["shamoji", "rice spoon", "rice scoop", "rice cooker", "serving rice", "utensil"], aliases=["shamoji"])
def _(S):
    head = "M6.5 9V7.5A5.5 5.5 0 0 1 17.5 7.5V11C17.5 13 15.5 14 13.75 14.5H10.25C8.5 14 6.5 13 6.5 11Z"
    if S.name == "line":
        head = "M6.5 12V7.5A5.5 5.5 0 0 1 17.5 7.5V12L13.75 14.5H10.25Z"
    handle = rect(10.25, 14, 3.5, 8.5, L(S, 0.5, 1.75))
    return tilt([shell(union(head, handle), stroke_miterlimit="2"), detail(seg(10.25, 14.5, 13.75, 14.5))])


@icon("spork", CAT, "Spork: a spoon bowl with three short tines cut into its tip",
      tags=["spoon fork", "camping cutlery", "picnic", "takeaway cutlery", "utensil", "cutlery"])
def _(S):
    head = ellipse(12, 7.5, 4.75, 5.5) if S.name == "rounded" else "M7.25 3H16.75V8C16.75 11 14.75 13 12 13C9.25 13 7.25 11 7.25 8Z"
    return tilt([shell(head), detail(seg(10.4, 1.5, 10.4, 5.5)), detail(seg(13.6, 1.5, 13.6, 5.5)),
                 line(seg(12, 13, 12, 22))])


def tr(parts, deg, cx, cy):
    """Rotate parts clockwise by deg about (cx, cy) without re-centring."""
    return [Part(p.kind, rot(p.d, deg, cx, cy), p.attrs) for p in parts]


# ============================================================================ presses and prep tools

@icon("tortilla-press", CAT, "Tortilla press: two round hinged plates with a long lever handle raised on top",
      tags=["tortilla maker", "masa", "flatbread", "mexican cooking", "corn tortilla", "press"])
def _(S):
    return [shell(rect(2.5, 16.5, 16, 4, rr(S, 2))), shell(rect(3.5, 11, 14, 3, rr(S, 1.5))),
            line(seg(2.5, 12.5, 2.5, 16.5) if S.name == "line" else "M3.5 12.5C2 12.5 2 16.5 3.5 16.5"),
            line(seg(20.5, 18.5, 20.5, 9.5)), line(seg(20.5, 9.5, 8, 3.5)), dot(7, 3, 1.6)]


@icon("sushi-rolling-mat", CAT, "Bamboo sushi mat with parallel slats, partly rolled up at one end",
      tags=["makisu", "bamboo mat", "sushi mat", "maki", "rolling sushi", "japanese cooking"], aliases=["makisu"])
def _(S):
    return [shell(rect(2.5, 5, 12, 14, L(S, 1, 2))), shell(rect(15.5, 3, 6, 18, L(S, 2, 3))),
            detail(seg(6.5, 5, 6.5, 19)), detail(seg(10.5, 5, 10.5, 19)), detail(seg(18.5, 6, 18.5, 18))]


@icon("potato-ricer", CAT, "Potato ricer: two long hinged handles with a plunger pressing strands out of a basket",
      tags=["ricer", "mashed potato", "puree", "masher", "press", "kitchen tool"])
def _(S):
    basket = rpoly(S, [(3, 8.5), (11, 8.5), (10, 15), (4, 15)], k=0.6)
    return [shell(basket), line(seg(7, 4.5, 7, 8.5)), line(rpoly(S, [(3.5, 4.5), (11, 4.5), (21.5, 2.5)], closed=False)),
            line(seg(11, 10.5, 21.5, 12)), line(seg(5.5, 17.5, 5.5, 21)), line(seg(8.5, 17.5, 8.5, 21))]


@icon("food-mill", CAT, "Food mill: a bowl with a hand crank on top and small hooks on the rim",
      tags=["mouli", "passatempo", "puree", "tomato sauce", "hand crank", "kitchen tool"], aliases=["mouli"])
def _(S):
    bowl = "M4 11H20C20 16.5 16.5 20.5 12 20.5C7.5 20.5 4 16.5 4 11Z"
    hook = rpoly(S, [(4, 11), (2, 11), (2, 13.5)], closed=False, k=0.6)
    return [shell(bowl), line(hook), line(flip(hook)), line(seg(12, 11, 12, 4.5)),
            line(rpoly(S, [(11, 4.5), (18.5, 4.5), (18.5, 2)], closed=False)),
            dot(9, 16, 1), dot(12, 17, 1), dot(15, 16, 1)]


def _fluted_square(x0, y0, x1, y1, n):
    """Square outline with n outward half-round flutes along each side."""
    def side(ax, ay, bx, by, ox, oy):
        out = ""
        for i in range(n):
            t1 = (i + 1) / n
            px, py = ax + (bx - ax) * t1, ay + (by - ay) * t1
            r = math.hypot(bx - ax, by - ay) / n / 2
            out += f"A{fmt(r)} {fmt(r)} 0 0 1 {fmt(px)} {fmt(py)}"
        return out
    return (f"M{fmt(x0)} {fmt(y0)}" + side(x0, y0, x1, y0, 0, -1) + side(x1, y0, x1, y1, 1, 0)
            + side(x1, y1, x0, y1, 0, 1) + side(x0, y1, x0, y0, -1, 0) + "Z")


@icon("ravioli-stamp", CAT, "Ravioli stamp seen from above: a square cutter with a fluted edge and a round knob",
      tags=["ravioli cutter", "pasta stamp", "pasta cutter", "fresh pasta", "italian cooking", "dumplings"],
      aliases=["ravioli-cutter"])
def _(S):
    body = _fluted_square(4.5, 4.5, 19.5, 19.5, 4) if S.name == "rounded" else poly(
        [(4.5, 4.5), (6.4, 3.2), (8.2, 4.5), (10.1, 3.2), (12, 4.5), (13.9, 3.2), (15.8, 4.5), (17.6, 3.2), (19.5, 4.5),
         (20.8, 6.4), (19.5, 8.2), (20.8, 10.1), (19.5, 12), (20.8, 13.9), (19.5, 15.8), (20.8, 17.6), (19.5, 19.5),
         (17.6, 20.8), (15.8, 19.5), (13.9, 20.8), (12, 19.5), (10.1, 20.8), (8.2, 19.5), (6.4, 20.8), (4.5, 19.5),
         (3.2, 17.6), (4.5, 15.8), (3.2, 13.9), (4.5, 12), (3.2, 10.1), (4.5, 8.2), (3.2, 6.4)], closed=True)
    return [shell(body, stroke_miterlimit="2"), detail(circle(12, 12, 3.5))]


@icon("pasta-drying-rack", CAT, "Pasta drying rack: an upright stand with arms draped with long noodles",
      tags=["pasta rack", "noodle rack", "fresh pasta", "drying pasta", "homemade noodles", "italian cooking"])
def _(S):
    out = [line(seg(12, 4, 12, 20.5)), line(seg(3, 4, 21, 4)), shell(rect(7, 19.5, 10, 2, L(S, 0, 1)))]
    for x in (4.5, 8.5, 15.5, 19.5):
        out.append(line(f"M{fmt(x)} 4.5C{fmt(x + 1.2)} 7.5 {fmt(x - 1.2)} 10 {fmt(x)} 13.5"))
    return out


@icon("cherry-pitter", CAT, "Cherry pitter: a plunger with a knob pressing down through a cherry held in a small cup",
      tags=["cherry stoner", "pitting", "olive pitter", "stone remover", "fruit", "kitchen tool"],
      aliases=["cherry-stoner"])
def _(S):
    cup = "M4.5 16.5V18A2 2 0 0 0 6.5 20H15.5A2 2 0 0 0 17.5 18V16.5" if S.name == "rounded" else "M4.5 16.5V20H17.5V16.5"
    return [shell(rect(7, 2, 8, 3.5, rr(S, 1.75))), line(seg(11, 5.5, 11, 11)), shell(circle(11, 12.5, 4)),
            line("M15 9.8C16 7.5 18 6 21 6"), line(cup)]


@icon("burger-press", CAT, "Burger press: a round plunger with a knob handle above a shaped patty",
      tags=["patty press", "hamburger press", "patty maker", "burger mold", "minced meat", "grilling"],
      aliases=["patty-press"])
def _(S):
    return [shell(rect(9, 2.5, 6, 3.5, rr(S, 1.75))), line(seg(12, 6, 12, 9)), shell(rect(3.5, 9, 17, 3.5, rr(S, 1.5))),
            shell(rect(4.5, 15.5, 15, 5.5, L(S, 2, 2.75))), detail(seg(8, 18.25, 16, 18.25))]


@icon("bag-clip", CAT, "Bag clip clamping the gathered top of a food bag",
      tags=["chip clip", "bag sealer", "food clip", "snack bag", "keep fresh", "storage"], aliases=["chip-clip"])
def _(S):
    bag = poly([(6.5, 11.5), (3.5, 21.5), (20.5, 21.5), (17.5, 11.5)], closed=True, r=S.r * 0.6)
    ruffle = "M7 8L8 3.5L10.2 6.5L12 3L13.8 6.5L16 3.5L17 8"
    return [shell(bag), line(ruffle), shell(rect(4.5, 8, 15, 3.5, L(S, 0, 1.75))), detail(seg(9, 15, 8, 19)),
            detail(seg(15, 15, 16, 19))]


def _flame(x, y, length, deg):
    """Pointed flame starting at (x, y) and pointing along deg (0 = right)."""
    w = length * 0.36
    d = (f"M{fmt(x)} {fmt(y)}C{fmt(x)} {fmt(y - w)} {fmt(x + length * 0.45)} {fmt(y - w * 1.05)} {fmt(x + length)} {fmt(y)}"
         f"C{fmt(x + length * 0.45)} {fmt(y + w * 1.05)} {fmt(x)} {fmt(y + w)} {fmt(x)} {fmt(y)}Z")
    return rot(d, deg, x, y)


@icon("kitchen-torch", CAT, "Kitchen blowtorch: a small fuel canister with a nozzle and a pointed flame",
      tags=["blowtorch", "creme brulee torch", "culinary torch", "caramelize", "brulee", "butane torch"],
      aliases=["culinary-torch"])
def _(S):
    flame = ("M12 2.5C12.8 5 16.5 5.8 16.5 9C16.5 11 14.5 12 12 12C9.5 12 7.5 11 7.5 9C7.5 7.5 8.5 6.9 9.3 5.6C10.3 6.5 11 6.7 11.5 6.7C11 5.3 11.3 4 12 2.5Z"
             if S.name == "rounded" else
             "M12 2.5L15 5.8L16.5 9L14.5 12H9.5L7.5 9L9.3 5.6L11.5 6.7Z")
    body = union(rect(7, 14.5, 10, 8, rr(S, 2.5)), rect(9.5, 12, 5, 3, L(S, 0, 1)))
    return [shell(flame, stroke_miterlimit="2"), shell(body), detail(seg(7, 18, 17, 18)),
            line("M17 16.5H21.5" if S.name == "line" else "M17 16.5H20.5")]


@icon("cream-whipper", CAT, "Cream whipper: a tall metal canister with a lever head and an angled nozzle",
      tags=["whipped cream dispenser", "siphon", "cream siphon", "whipping siphon", "desserts", "foam"],
      aliases=["cream-siphon"])
def _(S):
    can = rect(7, 10, 8.5, 12, rr(S, 2.5))
    head = rect(8, 6.5, 6.5, 3.5, rr(S, 1))
    nozzle = rot(rpoly(S, [(10, 7), (12.5, 7), (12, 2), (10.5, 2)], k=0.4), 20, 11.25, 6.5)
    return [shell(union(can, head, nozzle)), detail(seg(7, 10, 15.5, 10)),
            line(rpoly(S, [(14.5, 7.5), (19, 8), (19, 12)], closed=False, k=0.8))]


@icon("whetstone", CAT, "Whetstone: a rectangular sharpening stone with a knife blade lying across it",
      tags=["sharpening stone", "water stone", "knife sharpening", "sharpen", "grit", "knife care"],
      aliases=["sharpening-stone"])
def _(S):
    block = rpoly(S, [(6.5, 13.5), (21.5, 13.5), (21.5, 17.5), (18, 21.5), (2.5, 21.5), (2.5, 17.5)], k=0.5)
    blade = poly([(9, 3.5), (20, 3.5), (22, 9.5), (9, 9)], closed=True, r=S.r * 0.4)
    knife = union(blade, rect(2.5, 3.5, 7.5, 4.5, L(S, 0.5, 2)))
    return [shell(block, stroke_miterlimit="3"), detail(seg(2.5, 17.5, 18, 17.5)), detail(seg(18, 17.5, 18, 21.5)),
            detail(seg(18, 17.5, 21.5, 13.5)), shell(knife, stroke_miterlimit="3"), detail(seg(9, 3.5, 9, 9))]


@icon("conical-strainer", CAT, "Conical strainer: a cone-shaped fine mesh sieve pointing down with a long handle",
      tags=["chinois", "china cap", "sieve", "sauce strainer", "fine mesh", "straining"], aliases=["chinois"])
def _(S):
    cone = rpoly(S, [(2.5, 4.5), (15.5, 4.5), (9, 21)], k=0.8)
    return [shell(cone), line(seg(15.5, 5, 21.5, 5)), detail(seg(5, 9, 13, 9)), detail(seg(6.7, 13.3, 11.3, 13.3)),
            detail(seg(9, 5, 9, 16))]


@icon("knife-block", CAT, "Knife block: a slanted wooden block with several knife handles sticking out of slots",
      tags=["knife holder", "knife storage", "knife set", "countertop", "kitchen knives", "cutlery"])
def _(S):
    block = rpoly(S, [(3, 21.5), (21, 21.5), (21, 16.5), (9.5, 7.5), (3, 11.5)], k=0.8)
    out = [shell(block, stroke_miterlimit="2"), detail(seg(6, 17.5, 17, 17.5))]
    for x0, y0 in ((4.5, 9.5), (7.5, 7.5), (10.5, 9.5)):
        out.append(line(seg(x0, y0, x0 - 2.5 + 2.5, y0 - 5.5) if False else seg(x0, y0 + 0.5, x0 - 3, y0 - 5)))
    return out


@icon("magnetic-knife-strip", CAT, "Magnetic knife strip: a wall bar with knives hanging from it",
      tags=["knife rack", "magnetic strip", "knife holder", "wall storage", "kitchen knives", "cutlery"],
      aliases=["knife-magnet"])
def _(S):
    out = [shell(rect(2, 2.5, 20, 3.5, L(S, 0.5, 1.75)))]
    for cx in (5.25, 12, 18.75):
        out.append(line(seg(cx, 6, cx, 10)))
        blade = f"M{fmt(cx - 1.75)} 10H{fmt(cx + 1.75)}V16C{fmt(cx + 1.75)} 19 {fmt(cx)} 21 {fmt(cx - 1.75)} 21.5Z"
        if S.name == "line":
            blade = rpoly(S, [(cx - 1.75, 10), (cx + 1.75, 10), (cx + 1.75, 17), (cx - 1.75, 21.5)])
        out.append(shell(blade, stroke_miterlimit="2"))
    return out


# ============================================================================ grills and cookers

@icon("panini-press", CAT, "Panini press: a hinged grill with ridged plates, its top plate lifted by a long handle",
      tags=["sandwich press", "contact grill", "panini grill", "toastie maker", "grilled sandwich", "appliance"],
      aliases=["sandwich-press"])
def _(S):
    base = rect(2.5, 14, 17, 6, rr(S, 1.5))
    lid = [shell(rect(2.5, 8.5, 17, 4, rr(S, 1))), line(seg(19.5, 10.5, 22, 10.5))]
    ridges = "M6 14V12.5M10 14V12.5M14 14V12.5M18 14V12.5" if S.name == "line" else "M6 14V13M10 14V13M14 14V13M18 14V13"
    return ([shell(base), detail(seg(12, 17, 17, 17)), line("M4.5 20V22M17.5 20V22")] + tr(lid, -18, 3, 12.5)
            + [line(ridges)])


@icon("tandoor", CAT, "Tandoor: a tall clay oven with a narrow open top and a low arched draft door",
      tags=["tandoor oven", "clay oven", "naan", "indian cooking", "tandoori", "flatbread"],
      aliases=["tandoor-oven"])
def _(S):
    body = ("M8 4C8 8 3 9.5 3 15.5C3 19.5 5 22 8 22H16C19 22 21 19.5 21 15.5C21 9.5 16 8 16 4Z" if S.name == "rounded" else
            "M8 4V7L4.5 10.5L3 14V22H21V14L19.5 10.5L16 7V4Z")
    rim = ellipse(12, 4, 4, 1.4)
    return [shell(body), shell(rim), detail("M9.5 22V18.5A2.5 2.5 0 0 1 14.5 18.5V22" if S.name == "rounded" else "M9.5 22V18.5H14.5V22")]


@icon("kamado-grill", CAT, "Kamado grill: an egg-shaped ceramic cooker on a stand with a vent cap on top",
      tags=["ceramic grill", "egg grill", "kamado", "smoker", "barbecue", "outdoor cooking"], aliases=["egg-grill"])
def _(S):
    egg = "M12 3.5C15.8 3.5 18.5 8.5 18.5 12.5C18.5 16 15.8 18 12 18C8.2 18 5.5 16 5.5 12.5C5.5 8.5 8.2 3.5 12 3.5Z"
    cap = rect(10, 1.5, 4, 2.5, L(S, 0, 1))
    stand = rpoly(S, [(4.5, 22), (7, 17), (17, 17), (19.5, 22)], closed=False, k=0.6)
    return [shell(union(egg, cap)), detail(seg(5.6, 11, 18.4, 11)), line(stand), line(seg(18.5, 11, 21.5, 11))]


@icon("yakitori-grill", CAT, "Yakitori grill: a long narrow trough grill with skewers laid across it",
      tags=["skewer grill", "hibachi", "konro", "kebab grill", "charcoal grill", "japanese grilling"],
      aliases=["konro-grill"])
def _(S):
    trough = rpoly(S, [(2, 12), (22, 12), (20.5, 19.5), (3.5, 19.5)], k=0.8)
    out = [shell(trough), detail(seg(5, 15.75, 19, 15.75))]
    for x in (6, 12, 18):
        out.append(line(seg(x - 1.5, 12, x + 1.5, 2.5)))
        out.append(shell(rect(x - 0.6, 5.2, 3, 3.5, L(S, 0, 1))))
    return out


@icon("chafing-dish", CAT, "Chafing dish: a pan with a domed roll-top lid on a stand over a small burner flame",
      tags=["buffet warmer", "food warmer", "catering", "buffet", "roll top", "hotel pan"])
def _(S):
    lid = "M3.5 11A8.5 7 0 0 1 20.5 11Z"
    pan = rect(3, 11, 18, 3.5, L(S, 0, 1.5))
    flame = ("M12 16.5C13.8 18.3 13.8 21.5 12 21.5C10.2 21.5 10.2 18.3 12 16.5Z" if S.name == "rounded"
             else "M12 16.5L13.5 19.5C13.5 21 12.7 21.5 12 21.5C11.3 21.5 10.5 21 10.5 19.5Z")
    return [shell(union(lid, pan)), detail(seg(3, 11, 21, 11)), line("M5 14.5V21.5M19 14.5V21.5"),
            dot(12, 3.2, 1.2), shell(flame)]


# ============================================================================ storage

@icon("storage-canister", CAT, "Storage canister: a glass jar with a wire clamp lid and a rubber seal",
      tags=["clamp jar", "kilner jar", "airtight jar", "canister", "pantry", "food storage"],
      aliases=["clamp-jar"])
def _(S):
    body = union(rect(3, 9.5, 18, 12.5, rr(S, 4)), rect(4, 3.5, 16, 6, L(S, 0, 2)))
    return [shell(body), detail(seg(3, 9.5, 21, 9.5)), detail(rect(9.5, 6.5, 5, 6, L(S, 0.5, 1.5))), detail(seg(3, 17, 21, 17))]


@icon("food-storage-container", CAT, "Food storage container with a snap-on lid and locking tabs on each side",
      tags=["lunch box", "meal prep box", "leftovers", "airtight container", "plastic box", "food storage"],
      aliases=["meal-prep-container"])
def _(S):
    box = union(rect(2, 6, 20, 3.5, L(S, 0, 1.5)), rect(3.5, 9.5, 17, 11.5, rr(S, 2.5)))
    return [shell(box), detail(seg(3.5, 9.5, 20.5, 9.5)), hole(rect(6, 8, 2.5, 5, L(S, 0, 1))),
            hole(rect(15.5, 8, 2.5, 5, L(S, 0, 1)))]


@icon("spice-box", CAT, "Spice box seen from above: a round tin holding seven small bowls of spices",
      tags=["masala dabba", "spice tin", "spice container", "indian spices", "spices", "seasoning"],
      aliases=["masala-dabba"])
def _(S):
    tin = circle(12, 12, 9.5) if S.name == "rounded" else regular(12, 12, 9.9, 12, -90)
    out = [shell(tin if S.name == "rounded" else poly(tin, closed=True))]
    out.append(hole(circle(12, 12, 1.8)))
    for k in range(6):
        x, y = pt_on(12, 12, 5.4, -90 + k * 60)
        out.append(hole(circle(x, y, 1.8)))
    return out


@icon("zipper-bag", CAT, "Resealable zipper bag with a zip track along the top and a slider",
      tags=["zip bag", "resealable bag", "freezer bag", "sandwich bag", "zip lock", "food storage"],
      aliases=["resealable-bag"])
def _(S):
    bag = rect(3.5, 3, 17, 18.5, rr(S, 2.5))
    return [shell(bag), detail(seg(3.5, 7.5, 20.5, 7.5)), hole(rect(13.5, 5.25, 4, 4.5, L(S, 0, 1))),
            detail("M3.5 12L7 14.5L11 12.5L15.5 15L20.5 12.5" if S.name == "line" else "M3.5 13C6 11.5 8.5 11.5 12 13C15.5 14.5 18 14.5 20.5 13")]


@icon("fermenting-crock", CAT, "Fermenting crock: a wide crock with a water-seal rim, a lid and small side handles",
      tags=["pickling crock", "sauerkraut", "kimchi", "fermentation", "water seal", "pickles"],
      aliases=["pickling-crock"])
def _(S):
    body = "M5 10C3.5 13.5 3.8 18.5 6.5 21.5H17.5C20.2 18.5 20.5 13.5 19 10Z"
    channel = rpoly(S, [(2.5, 5.5), (2.5, 8.5), (21.5, 8.5), (21.5, 5.5)], closed=False, k=0.8)
    lid = rect(6.5, 4, 11, 2.5, L(S, 0, 1.25))
    return [shell(body), line(channel), shell(lid), line(seg(12, 1.5, 12, 4)), detail(seg(8, 15, 16, 15))]


@icon("lazy-susan", CAT, "Lazy Susan: a round turntable tray on a base holding a few small jars",
      tags=["turntable", "rotating tray", "spinning tray", "condiment tray", "pantry organiser", "table centrepiece"],
      aliases=["turntable-tray"])
def _(S):
    tray = union(rect(2, 12.5, 20, 3, L(S, 0.5, 1.5)), rect(9, 15.5, 6, 2, 0))
    jars = [(3.5, 6.5, 4.5, 6), (10, 3.5, 4, 9), (16, 7.5, 4.5, 5)]
    out = [shell(tray)]
    for x, y, w, h in jars:
        out += [shell(rect(x, y, w, h, rr(S, 1.25))), detail(seg(x, y + 2, x + w, y + 2))]
    arrow = "M4 18.5C7 21.8 17 21.8 20 18.5"
    head = rpoly(S, [(16.8, 18.2), (20, 18.5), (19.7, 21.5)], closed=False, k=0.4)
    return out + [line(arrow), line(head)]


@icon("tiffin-carrier", CAT, "Tiffin carrier: three stacked round tins held by a clasp frame with a top handle",
      tags=["tiffin", "dabba", "lunch box", "stacked lunch box", "packed lunch", "indian lunch"],
      aliases=["tiffin-box"])
def _(S):
    body = rect(6.5, 9, 11, 12.5, rr(S, 2))
    frame = rpoly(S, [(4.5, 20.5), (2.5, 20.5), (2.5, 5.5), (21.5, 5.5), (21.5, 20.5), (19.5, 20.5)], closed=False, k=0.8)
    handle = rpoly(S, [(9, 5.5), (9, 2.5), (15, 2.5), (15, 5.5)], closed=False, k=0.8)
    return [shell(body), detail(seg(6.5, 13.25, 17.5, 13.25)), detail(seg(6.5, 17.25, 17.5, 17.25)),
            line(frame), line(handle)]


@icon("pot-rack", CAT, "Pot rack: a hanging bar with a pan and a pot hung on hooks",
      tags=["pan rack", "hanging rack", "cookware storage", "ceiling rack", "hooks", "kitchen storage"],
      aliases=["pan-rack"])
def _(S):
    bar = line(seg(2, 3.5, 22, 3.5))
    pan = [line(seg(6, 3.5, 6, 11)), shell(circle(6, 15.5, 4) if S.name == "rounded" else regular(6, 15.5, 4.2, 8, -90))]
    if S.name == "line":
        pan[1] = shell(poly(regular(6, 15.5, 4.2, 8, -67.5), closed=True))
    pot = [line(seg(16.5, 3.5, 16.5, 7.5)), line(rpoly(S, [(13.5, 11.5), (13.5, 7.5), (19.5, 7.5), (19.5, 11.5)], closed=False, k=0.6)),
           shell(rect(12, 11.5, 9, 9, rr(S, 2.5)))]
    return [bar] + pan + pot


@icon("cutlery-tray", CAT, "Cutlery tray seen from above holding a fork, a knife and a spoon side by side",
      tags=["silverware tray", "cutlery organiser", "drawer organizer", "utensil tray", "flatware", "drawer"],
      aliases=["silverware-tray"])
def _(S):
    out = [shell(rect(2, 2, 20, 20, rr(S, 3)))]
    out += [detail("M5.5 5V9.5M8.5 5V9.5M5.5 9.5A1.5 1.5 0 0 0 8.5 9.5M7 10.5V19")]
    out += [detail(seg(12, 5, 12, 19)), hole(rect(11, 5, 2.8, 7.5, L(S, 0, 1.4)))]
    out += [hole(ellipse(17, 7.5, 2, 2.75)), detail(seg(17, 9.5, 17, 19))]
    return out


@icon("utensil-holder", CAT, "Utensil holder: a round crock holding an upright spatula, wooden spoon and whisk",
      tags=["utensil crock", "utensil jar", "tool holder", "kitchen tools", "countertop storage", "spoons"],
      aliases=["utensil-crock"])
def _(S):
    crock = rect(5, 12, 14, 10, rr(S, 2.5))
    spoon = tr([line(seg(8, 12, 8, 7)), shell(ellipse(8, 4.5, 1.8, 2.6))], -18, 8, 12)
    spat = tr([line(seg(16, 12, 16, 8)), shell(rect(14, 2.5, 4, 5.5, L(S, 0, 1)))], 18, 16, 12)
    whisk = [line(seg(12, 12, 12, 9)), shell("M12 9C10.2 7.5 10.2 3.5 12 2.5C13.8 3.5 13.8 7.5 12 9Z")]
    return [shell(crock), detail(seg(5, 15, 19, 15))] + spoon + whisk + spat


@icon("spoon-rest", CAT, "Spoon rest: an oval dish with a wooden spoon lying in it",
      tags=["spoon holder", "utensil rest", "stove top", "ladle rest", "cooking", "countertop"],
      aliases=["spoon-holder"])
def _(S):
    dish = ellipse(10, 15, 8, 5.5) if S.name == "rounded" else rect(2, 9.5, 16, 11, 4)
    spoon = tr([hole(ellipse(10, 16, 2.2, 3)), detail(seg(10, 13, 10, 10.7)), line(seg(10, 8.7, 10, 1))], 45, 10, 15)
    return [shell(dish)] + spoon


@icon("dish-rack", CAT, "Dish rack: a wire rack holding a plate upright and a cup upside down to drain",
      tags=["dish drainer", "drying rack", "plate rack", "washing up", "draining board", "dishes"],
      aliases=["dish-drainer"])
def _(S):
    rack = rect(2, 14, 20, 7.5, rr(S, 2))
    cup = rpoly(S, [(17.5, 6), (21.5, 6), (22, 11.5), (17, 11.5)], k=0.5)
    return [shell(rack), detail("M7 14V21.5M12 14V21.5M17 14V21.5"), line("M2.5 14A6 6 0 0 1 14.5 14"),
            line("M5.5 14A3 3 0 0 1 11.5 14"), shell(cup)]


@icon("compost-caddy", CAT, "Compost caddy: a small bin with a flip lid, a carry handle and a leaf on the front",
      tags=["food waste bin", "compost bin", "kitchen caddy", "scraps", "organic waste", "recycling"],
      aliases=["food-waste-caddy"])
def _(S):
    bin_ = rpoly(S, [(5, 10), (19, 10), (18, 21.5), (6, 21.5)], k=1)
    lid = rect(4, 7, 16, 3, L(S, 0, 1.5))
    handle = rpoly(S, [(7.5, 7), (7.5, 3), (16.5, 3), (16.5, 7)], closed=False, k=1)
    leaf = "M9 19C9 14.5 11.5 12.5 15 12.5C15 16.5 13 19 9 19Z"
    return [shell(union(bin_, lid)), detail(seg(4.5, 10, 19.5, 10)), line(handle), detail(leaf)]


@icon("trivet", CAT, "Trivet seen from above: a round wire rack with a spiral centre and short feet",
      tags=["pot stand", "hot pad", "pan rest", "heat mat", "pot rest", "table protector"], aliases=["pot-stand"])
def _(S):
    spiral = "M13 12A1 1 0 0 0 11 12A3 3 0 0 0 17 12A5 5 0 0 0 7 12"
    feet = "".join(f"M{fmt(pt_on(12, 12, 8.5, a)[0])} {fmt(pt_on(12, 12, 8.5, a)[1])}L{fmt(pt_on(12, 12, 10.5, a)[0])} {fmt(pt_on(12, 12, 10.5, a)[1])}"
                   for a in (-90, 30, 150))
    ring = circle(12, 12, 8) if S.name == "rounded" else poly(regular(12, 12, 8.2, 12, -75), closed=True)
    return [line(ring), line(spiral), line(feet)]


@icon("tin-can", CAT, "Tin can with a label band around the middle and a pull ring on top",
      tags=["can", "canned food", "tinned food", "food can", "pantry", "preserves"], aliases=["food-can"])
def _(S):
    body = union(rect(5, 5, 14, 16, 0), ellipse(12, 5, 7, 2), ellipse(12, 21, 7, 2)) if S.name == "rounded" else \
        rpoly(S, [(5, 5), (7, 3), (17, 3), (19, 5), (19, 21), (17, 23 - 0.5), (7, 22.5), (5, 21)])
    top = "M5 5A7 2 0 0 0 19 5" if S.name == "rounded" else "M5 5L7 7H17L19 5"
    return [shell(body, stroke_miterlimit="2"), detail(top), detail(seg(5, 11, 19, 11)), detail(seg(5, 17, 19, 17))]


@icon("pizza-box", CAT, "Pizza box with its lid partly open and a slice of pizza inside",
      tags=["pizza delivery", "takeaway pizza", "cardboard box", "pizza night", "food delivery", "slice"],
      aliases=["pizza-delivery-box"])
def _(S):
    base = rect(2, 15, 20, 6.5, rr(S, 1.5))
    lid = tr([shell(rect(2, 11.5, 18, 3, L(S, 0, 1.25)))], -38, 2, 14.5)
    slice_ = rpoly(S, [(9, 13), (18.5, 8), (20.5, 12.5)], k=0.3)
    return fit([shell(base), detail(seg(2, 18.25, 22, 18.25))] + lid + [shell(slice_), dot(16.5, 11, 1.1)])


@icon("dinner-plate", CAT, "Dinner plate seen from above with an inner rim circle",
      tags=["plate", "dish", "dinnerware", "tableware", "meal", "crockery"], aliases=["plate"])
def _(S):
    outer = circle(12, 12, 9.5) if S.name == "rounded" else poly(regular(12, 12, 9.8, 16, -90), closed=True)
    return [shell(outer), detail(circle(12, 12, 5.5))]


@icon("serving-platter", CAT, "Serving platter: a large oval dish with a raised rim, seen at an angle",
      tags=["platter", "serving dish", "oval plate", "buffet", "roast dish", "tableware"], aliases=["platter"])
def _(S):
    outer = ellipse(12, 13, 10, 6.5) if S.name == "rounded" else rect(2, 6.5, 20, 13, 5)
    inner = ellipse(12, 13, 5.5, 2.5) if S.name == "rounded" else rect(6.5, 10.5, 11, 5, 2)
    return [shell(outer), detail(inner), line(seg(8, 21.5, 16, 21.5))]


@icon("napkin-ring", CAT, "Napkin ring: a folded cloth napkin fanning out above a round ring",
      tags=["serviette ring", "napkin holder", "table setting", "dinner party", "linen", "tableware"],
      aliases=["serviette-ring"])
def _(S):
    fan = "M9.5 13L3 5.5C6 2 18 2 21 5.5L14.5 13Z" if S.name == "rounded" else "M9.5 13L3 5L8 2.5H16L21 5L14.5 13Z"
    tail = rpoly(S, [(9.5, 19), (8, 22), (16, 22), (14.5, 19)], k=0.4)
    ring = ellipse(12, 16, 5, 3)
    return [shell(fan, stroke_miterlimit="2"), detail("M12 3V13"), detail("M7.5 4L10.5 13M16.5 4L13.5 13"),
            shell(ring), shell(tail)]


@icon("tablecloth", CAT, "Tablecloth draped over a small table with its corners hanging down in points",
      tags=["table linen", "table cover", "dining table", "picnic", "tablecloth", "table setting"],
      aliases=["table-cover"])
def _(S):
    cloth = rpoly(S, [(5, 5), (19, 5), (22, 14), (17, 11.5), (12, 15), (7, 11.5), (2, 14)], k=0.6)
    return [shell(cloth, stroke_miterlimit="2"), line("M6.5 15V21.5M17.5 15V21.5"), detail(seg(12, 5, 12, 11))]


@icon("serving-tray", CAT, "Serving tray with raised sides and two cutout handles carrying two cups",
      tags=["tray", "drinks tray", "waiter tray", "room service", "breakfast tray", "tea tray"])
def _(S):
    tray = rpoly(S, [(2, 14), (22, 14), (20, 20), (4, 20)], k=0.8)
    cups = [rpoly(S, [(6, 7), (11, 7), (10.5, 12), (6.5, 12)], k=0.4), rpoly(S, [(13, 5), (18, 5), (17.5, 12), (13.5, 12)], k=0.4)]
    return [shell(tray), detail(seg(5, 17, 7.5, 17)), detail(seg(16.5, 17, 19, 17))] + [shell(c) for c in cups]


@icon("soup-tureen", CAT, "Soup tureen: a large lidded bowl on a foot with side handles and a ladle handle",
      tags=["tureen", "soup bowl", "serving bowl", "soup", "buffet", "tableware"])
def _(S):
    bowl = "M4 11.5H20C20 16 16.5 19 12 19C7.5 19 4 16 4 11.5Z"
    lid = "M5 11.5A7 5.5 0 0 1 19 11.5Z" if S.name == "rounded" else "M5 11.5L7.5 7.5H16.5L19 11.5Z"
    foot = rect(8.5, 19, 7, 2.5, L(S, 0, 1))
    handles = "M4 13.5H2M20 13.5H22"
    return [shell(union(bowl, lid, foot), stroke_miterlimit="2"), detail(seg(4, 11.5, 20, 11.5)), line(handles),
            line(seg(15, 7, 19.5, 2.5)), dot(12, 4.5, 1.3)]


@icon("salad-servers", CAT, "Salad servers: a large wooden spoon and fork crossed diagonally",
      tags=["salad spoon", "salad fork", "serving utensils", "tossing salad", "wooden servers", "salad"],
      aliases=["salad-tongs"])
def _(S):
    spoon = tr([shell(ellipse(12, 5.5, 3.3, 4)), line(seg(12, 9.5, 12, 22))], -40, 12, 12)
    head = ("M8.5 2V7A3.5 3.5 0 0 0 15.5 7V2" if S.name == "rounded" else "M8.5 2V9.5H15.5V2")
    fork = tr([line(head), line(seg(12, 2, 12, 22))], 40, 12, 12)
    return fit(spoon + fork)


@icon("chinese-soup-spoon", CAT, "Chinese soup spoon: a deep flat-bottomed spoon with a short thick upturned handle",
      tags=["soup spoon", "ceramic spoon", "asian spoon", "ramen spoon", "wonton soup", "tangchi"],
      aliases=["ceramic-soup-spoon"])
def _(S):
    body = ("M2.5 11.5H13L19.5 5.5A1.8 1.8 0 0 1 21.8 8L15 16C14 17.5 12.5 18.5 10 18.5H7C4.5 18.5 2.5 15 2.5 11.5Z"
            if S.name == "rounded" else "M2.5 11.5H13L20 5L22 7.5L14.5 16.5L12.5 18.5H6L3.5 16Z")
    return [shell(body, stroke_miterlimit="2"), detail(seg(3, 11.5, 13, 11.5))]


@icon("thali", CAT, "Thali seen from above: a round metal tray with small bowls around the edge and rice in the middle",
      tags=["thali plate", "indian meal", "platter", "katori", "set meal", "indian food"], aliases=["thali-plate"])
def _(S):
    tray = circle(12, 12, 10) if S.name == "rounded" else poly(regular(12, 12, 10.3, 16, -90), closed=True)
    out = [shell(tray)]
    for a in (-160, -95, -30, 35):
        x, y = pt_on(12, 12, 5.8, a)
        out.append(detail(circle(x, y, 1.8)))
    out.append(hole(ellipse(8.5, 16, 3, 2.2)))
    return out


@icon("bed-tray", CAT, "Bed tray: a tray with raised handle ends and folding legs, holding a cup",
      tags=["breakfast in bed", "lap tray", "serving tray", "room service", "lap desk", "breakfast tray"],
      aliases=["breakfast-tray"])
def _(S):
    tray = rpoly(S, [(2, 8), (2, 13), (22, 13), (22, 8), (19.5, 8), (19.5, 10.5), (4.5, 10.5), (4.5, 8)], k=0.5)
    legs = rpoly(S, [(4.5, 13), (4.5, 21), (8, 21)], closed=False, k=0.6)
    legs2 = rpoly(S, [(19.5, 13), (19.5, 21), (16, 21)], closed=False, k=0.6)
    cup = rpoly(S, [(8.5, 3), (14, 3), (13.5, 8.5), (9, 8.5)], k=0.5)
    return [shell(tray, stroke_miterlimit="2"), line(legs), line(legs2), line(seg(4.5, 17, 19.5, 17)), shell(cup),
            line("M14 4.5H15C16.5 4.5 16.5 7 14.5 7")]


@icon("picnic-basket", CAT, "Picnic basket: a woven hamper with a hinged lid and two handles",
      tags=["picnic hamper", "hamper", "wicker basket", "picnic", "outdoor meal", "summer"], aliases=["picnic-hamper"])
def _(S):
    body = rpoly(S, [(3, 11.5), (21, 11.5), (19.5, 21.5), (4.5, 21.5)], k=0.8)
    lid = rect(2.5, 9, 19, 2.5, L(S, 0, 1.25))
    h1 = "M6 9V7A2.5 2.5 0 0 1 11 7V9" if S.name == "rounded" else "M6 9V4.5H11V9"
    return [shell(union(body, lid)), detail(seg(3, 11.5, 21, 11.5)), detail(seg(4.2, 16.5, 19.8, 16.5)),
            detail(seg(12, 11.5, 12, 21.5)), line(h1), line(flip(h1))]


@icon("stir-fry", CAT, "Stir-fry: a wok with pieces of food tossed up above it along an arc",
      tags=["wok", "tossing", "wok hei", "chinese cooking", "stir fry", "sauteing"], aliases=["wok-toss"])
def _(S):
    wok = "M2.5 14H17.5C17.5 18.5 14.5 21.5 10 21.5C5.5 21.5 2.5 18.5 2.5 14Z"
    return [shell(wok), line(seg(17.5, 14.5, 22, 12.5)), line("M4 10.5C5 6 9.5 3.5 14 4.5"),
            dot(8, 10.5, 1.4), shell(rect(11, 8.5, 3, 2.5, L(S, 0, 1))), dot(17.5, 7.5, 1.4)]


@icon("whisking", CAT, "Whisking: a whisk in a bowl with curved motion lines beside it",
      tags=["whisk", "beating eggs", "mixing", "whipping cream", "batter", "baking"], aliases=["beating"])
def _(S):
    bowl = "M2.5 14H21.5C21.5 18.5 17.5 21.5 12 21.5C6.5 21.5 2.5 18.5 2.5 14Z"
    head = "M12 13C6.5 10.5 7.5 4.5 12 4C16.5 4.5 17.5 10.5 12 13Z"
    whisk = tr([line(seg(12, 4, 12, 0.5)), line(head)], 30, 12, 13)
    return [shell(bowl)] + whisk + [line("M4 5.5C3 7.5 3 9.5 4 11"), line("M20.5 8C21.5 9.5 21.5 10.5 21 11.5")]


@icon("stirring-pot", CAT, "Stirring a pot: a wooden spoon in a pot with a circular motion arrow around it",
      tags=["stir", "stirring", "cooking", "simmering", "sauce", "soup"], aliases=["stir-pot"])
def _(S):
    pot = rect(4, 13, 16, 8.5, rr(S, 2.5))
    arrow = "M17 10.5C19.5 9.5 19.5 7.5 17 6.8C14 6 10 6 7 6.8C4.5 7.5 4.5 9.5 7 10.5"
    head = rpoly(S, [(4.5, 12), (7, 10.5), (5.5, 8.2)], closed=False, k=0.4)
    return [shell(pot), line("M4 15H2M20 15H22"), line(seg(12, 13, 12, 2)), hole(ellipse(12, 17.25, 1.8, 2.3)),
            line(arrow), line(head)]


@icon("rolling-dough", CAT, "Rolling dough: a rolling pin resting on a flat round sheet of dough",
      tags=["rolling pin", "dough", "pastry", "baking", "flatten", "pie crust"], aliases=["rolling-out-dough"])
def _(S):
    pin = rect(6, 8.5, 12, 5, rr(S, 2.5))
    dough = ellipse(12, 16, 10, 5)
    dough = minus(dough, rect(4, 6.5, 16, 9))
    return [shell(dough), shell(pin), line("M6 11H2.5M18 11H21.5")]


@icon("flambe", CAT, "Flambe: a frying pan with tall flames leaping up from the food",
      tags=["flambe", "flaming", "fire", "cognac", "chef", "flambeed dessert"], aliases=["flambeing"])
def _(S):
    pan = rpoly(S, [(2.5, 15.5), (16.5, 15.5), (15, 20.5), (4, 20.5)], k=0.6)
    flame = ("M6 13.5C4 11.5 4 9 6 7C6.5 8.5 7.5 9 8 9.5C8 6 9.5 3.5 11.5 2C11.5 5 14 6.5 14 9.5C14.8 9 15.3 8 15.5 7"
             "C17 9 17 11.5 15 13.5Z")
    return [shell(pan), line(seg(16.5, 16.5, 21.5, 14.5)), shell(flame)]


@icon("carving-roast", CAT, "Carving a roast: a netted roast joint on a board with a carving fork and a knife standing beside it",
      tags=["carving", "roast beef", "sunday roast", "roast dinner", "joint of meat", "slicing meat"],
      aliases=["carving-meat"])
def _(S):
    board = rect(2, 19, 20, 3, L(S, 0.5, 1.5))
    roast = rect(2.5, 6.5, 12, 10.5, rr(S, 5))
    tines = "M17 2V6A2 2 0 0 0 21 6V2" if S.name == "rounded" else "M17 2V7H21V2"
    return [shell(board), shell(roast), detail(seg(6.5, 6.5, 8, 17)), detail(seg(10.5, 6.5, 12, 17)),
            line(tines), line(seg(19, 7.5, 19, 19))]


@icon("cracking-egg", CAT, "Cracking an egg: the upper shell lifted and tilted away from the lower half, which holds the yolk",
      tags=["crack an egg", "break egg", "eggshell", "yolk", "baking", "breakfast"], aliases=["breaking-egg"])
def _(S):
    cup = ("M3.5 12.5L6.5 14.5L9.5 12.5L12 14.5L14.5 12.5L17.5 14.5L20.5 12.5C20.5 18.5 17 22 12 22C7 22 3.5 18.5 3.5 12.5Z"
           if S.name == "rounded" else
           "M3.5 12.5L6.5 14.5L9.5 12.5L12 14.5L14.5 12.5L17.5 14.5L20.5 12.5L19 18L15 22H9L5 18Z")
    cap = ("M-5 0L-2.5 2L0 0L2.5 2L5 0C5 -4.5 3 -7 0 -7C-3 -7 -5 -4.5 -5 0Z" if S.name == "rounded" else
           "M-5 0L-2.5 2L0 0L2.5 2L5 0L3.5 -5L0 -7L-3.5 -5Z")
    cap = rot(mv(cap, 16, 7), 38, 16, 7)
    return fit([shell(cup, stroke_miterlimit="2"), shell(cap, stroke_miterlimit="2"), hole(circle(10, 10, 3))])


@icon("recipe-card", CAT, "Recipe card: an index card with ruled lines and a small spoon in the corner",
      tags=["recipe", "index card", "cooking instructions", "ingredients", "family recipe", "cookbook"],
      aliases=["recipe-index-card"])
def _(S):
    card = rect(2, 3.5, 20, 17, rr(S, 2))
    spoon = tr([hole(ellipse(17, 7.5, 1.7, 2.3)), detail(seg(17, 9.5, 17, 13))], 30, 17, 9)
    return [shell(card), detail(seg(5.5, 8, 12, 8)), detail(seg(5.5, 12.5, 12, 12.5)), detail(seg(5.5, 17, 18.5, 17))] + spoon


@icon("cookbook", CAT, "Cookbook: a closed book with a chef's hat on the cover and a ribbon bookmark",
      tags=["recipe book", "cook book", "recipes", "cooking", "chef", "kitchen"], aliases=["recipe-book"])
def _(S):
    book = rect(4, 2, 16, 18, rr(S, 2))
    hat = ("M10 14V11.5C8 11.5 7.5 8.5 9.5 8C10 6 14 6 14.5 8C16.5 8.5 16 11.5 14 11.5V14Z" if S.name == "rounded"
           else "M10 14V11.5L8.5 10V8H10.5L12 6.5L13.5 8H15.5V10L14 11.5V14Z")
    return [shell(book), detail(seg(7.5, 2, 7.5, 20)), detail(hat), line("M16.5 20V22.5" if False else "M16.5 20V22")]


@icon("fire-blanket", CAT, "Fire blanket: a wall pouch with two pull tabs hanging out of the bottom",
      tags=["fire safety", "kitchen fire", "fire blanket", "emergency", "grease fire", "safety equipment"],
      aliases=["fire-safety-blanket"])
def _(S):
    pouch = rect(3.5, 2.5, 17, 13.5, rr(S, 2.5))
    flame = ("M12 13C9.5 13 9 10.5 10 9C10.5 10 11 10.3 11.5 10.3C11 8.5 12 6.5 13.5 5.5C13.5 7.5 15 8.5 15 10.5C15 12 13.8 13 12 13Z")
    tabs = [rect(6, 16, 3.5, 5.5, L(S, 0.5, 1.75)), rect(14.5, 16, 3.5, 5.5, L(S, 0.5, 1.75))]
    return [shell(pouch), detail(flame), shell(tabs[0]), shell(tabs[1])]


@icon("place-setting", CAT, "Place setting seen from above: a round plate with a fork on the left and a knife on the right",
      tags=["table setting", "dinner table", "cutlery", "plate and cutlery", "dining", "restaurant"],
      aliases=["table-setting"])
def _(S):
    tines = "M2 3V7.5A2 2 0 0 0 6 7.5V3" if S.name == "rounded" else "M2 3V8H6V3"
    knife = "M21 21V3.5C18.5 4.5 18 8.5 18.5 13H21" if S.name == "rounded" else "M21 21V4L18.5 7V13H21"
    return [shell(circle(12, 12, 5.5) if S.name == "rounded" else poly(regular(12, 12, 5.8, 12, -90), closed=True)),
            line(tines), line(seg(4, 8, 4, 21)), line(knife, stroke_miterlimit="2")]


@icon("pancake-flip", CAT, "Pancake flip: a frying pan with a pancake tossed in the air above it along a curved arrow",
      tags=["flipping pancake", "pancake day", "tossing pancake", "frying pan", "breakfast", "cooking"],
      aliases=["flipping-a-pancake"])
def _(S):
    pan = rpoly(S, [(2.5, 16), (16.5, 16), (15, 21), (4, 21)], k=0.6)
    cake = rect(9, 7, 9, 3.5, L(S, 1, 1.75))
    return [shell(pan), line(seg(16.5, 17, 21.5, 15)), shell(cake), line("M5 11C4 7 6.5 4 10 3"), line(rpoly(S, [(7.5, 1.5), (10, 3), (8.5, 5.5)], closed=False, k=0.3))]
