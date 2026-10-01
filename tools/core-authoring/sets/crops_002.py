"""TypeIcon Core: crop handling, drying, machinery and farm work (batch crops_002).

Original drawings from the objects themselves, simplified to read at 24 px.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path

CAT = "crops"
ROLL_DEG = -28


def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def mark(d) -> Part:
    """Small solid shape: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def rotd(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rot(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def orect(cx, cy, w, h, rx=0.0, deg=0.0):
    """Rounded rectangle centred on (cx, cy), turned clockwise by deg about its own centre."""
    return rotd(rect(cx - w / 2, cy - h / 2, w, h, rx), deg, cx, cy)


# ============================================================================ storage and drying

def sun(cx, cy, reach=4.6, angles=(0, 90, 180, 270)):
    """Small sun: solid disc with short rays."""
    out = [dot(cx, cy, 1.8)]
    start = 3.5 if reach > 4.3 else 3.1
    for a in angles:
        p, q = polar(cx, cy, start, a), polar(cx, cy, reach, a)
        out.append(line(seg(p[0], p[1], q[0], q[1])))
    return out


def sprout(x, y, h=5, w=2.5, S=None):
    """Seedling: stem rising from (x, y) with a V of two leaves."""
    return [line(seg(x, y, x, y - h)), line(poly([(x - w, y - h - 1.5), (x, y - h + 1.0), (x + w, y - h - 1.5)], r=S.r * 0.5 if S else 0))]


# ============================================================================ storage and drying

@icon("silage-bag", CAT, "Long ribbed plastic tube of silage lying on the ground with a tied end",
      tags=["silage", "ag bag", "forage storage", "fodder", "farm", "feed", "bunker"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 16, 10, L(S, 4, 5))),
        detail(seg(8, 6.5, 8, 16.5)),
        detail(seg(13, 6.5, 13, 16.5)),
        line(poly([(19.5, 9), (22, 11.5), (19.5, 14)], r=S.r * 0.5)),
        line(seg(2, 20, 22, 20)),
    ]


@icon("grain-probe", CAT, "Long slotted probe spear pushed diagonally into a heap of grain",
      tags=["grain sampler", "grain trier", "sampling", "grain quality", "moisture", "bin", "inspection"])
def _(S):
    mound = "M2.5 21C4.5 15 8 12.5 12 12.5C16 12.5 19.5 15 21.5 21Z"
    probe = orect(14.5, 9.5, 3.5, 16, L(S, 0.5, 1.7), 28)
    return [
        shell(minus(probe, mound)),
        shell(mound),
        mark(orect(16.7, 6, 1, 3, 0, 28)),
    ]


@icon("grain-pile", CAT, "Conical heap of grain with a few kernels scattered at its base",
      tags=["grain heap", "stockpile", "harvest", "cereal", "wheat", "storage", "mound"])
def _(S):
    return [
        shell(L(S, "M3 18C6 18 8.5 8 12 8C15.5 8 18 18 21 18Z", "M3.5 18C6 18 8.5 8.5 12 8.5C15.5 8.5 18 18 20.5 18Z")),
        detail("M9 14C10.5 14.8 13.5 14.8 15 14"),
        dot(5, 21, 1),
        dot(10, 21, 1),
        dot(15, 21, 1),
        dot(20, 21, 1),
    ]


@icon("sun-drying-grain", CAT, "Grain spread in a flat layer on a mat with a rake and the sun overhead",
      tags=["drying grain", "sun drying", "threshing floor", "post-harvest", "drying mat", "rake", "dry"])
def _(S):
    return [
        *sun(18.5, 5.5),
        shell(poly([(2.5, 20.5), (6, 14.5), (21.5, 14.5), (21.5, 20.5)], closed=True, r=S.r * 0.5)),
        dot(10, 17.5, 1),
        dot(15.5, 17.5, 1),
        line(seg(2.5, 3.5, 9, 11.5)),
        line(seg(7, 8, 11, 11)),
    ]


@icon("solar-dryer", CAT, "Legged drying box with a sloped glass lid, a tray of sliced produce and the sun above",
      tags=["solar drying", "food dryer", "dehydrator", "fruit drying", "preservation", "dried fruit", "sun"])
def _(S):
    return [
        *sun(17.5, 5, 4.2),
        shell(poly([(3, 8.5), (21, 12.5), (21, 18), (3, 18)], closed=True, r=S.r * 0.5)),
        detail(seg(5.5, 15, 18.5, 15)),
        dot(8, 12.3, 0.9),
        dot(12, 13, 0.9),
        dot(16, 13.8, 0.9),
        line(seg(5, 18, 5, 22)),
        line(seg(19, 18, 19, 22)),
    ]


@icon("rice-drying-rack", CAT, "Horizontal pole between two posts with bundles of harvested rice hanging in a row",
      tags=["rice", "drying", "harvest", "bundles", "sheaves", "paddy", "hanging", "rack"])
def _(S):
    return [
        line(seg(2.5, 3, 2.5, 21.5)),
        line(seg(21.5, 3, 21.5, 21.5)),
        line(seg(2.5, 6, 21.5, 6)),
        shell(poly([(7.5, 7), (5.5, 18), (10.5, 18), (8.5, 7)], closed=True, r=S.r * 0.4)),
        shell(poly([(15.5, 7), (13.5, 18), (18.5, 18), (16.5, 7)], closed=True, r=S.r * 0.4)),
        detail(seg(8, 10, 8, 16)),
        detail(seg(16, 10, 16, 16)),
    ]


@icon("hay-drying-rack", CAT, "Wooden rail rack with a thick layer of hay draped over its top rail",
      tags=["hay", "drying", "forage", "fodder", "haymaking", "rack", "rails", "farm"])
def _(S):
    return [
        shell(poly([(3, 9), (3, 6), (7, 4), (17, 4), (21, 6), (21, 9), (21, 13), (18, 11), (15, 14), (12, 11), (9, 14), (6, 11), (3, 13)],
                   closed=True, r=S.r * 0.6)),
        line(seg(5.5, 14, 5.5, 21.5)),
        line(seg(18.5, 14, 18.5, 21.5)),
        line(seg(5.5, 18, 18.5, 18)),
    ]


@icon("tobacco-curing-barn", CAT, "Tall barn with a ventilated roof ridge and an open side showing hanging leaves",
      tags=["tobacco", "curing", "barn", "drying shed", "leaf", "tobacco farm", "flue cured", "air cured"])
def _(S):
    return [
        shell(poly([(4.5, 21), (4.5, 10), (12, 5.5), (19.5, 10), (19.5, 21)], closed=True, r=S.r)),
        line(seg(9.5, 3, 14.5, 3)),
        detail(poly([(8.5, 21), (8.5, 12.5), (15.5, 12.5), (15.5, 21)])),
        dot(10.75, 16, 1),
        dot(13.25, 16, 1),
    ]


@icon("coffee-drying-bed", CAT, "Raised mesh bed on legs covered with a layer of coffee cherries",
      tags=["coffee", "cherries", "drying bed", "african bed", "natural process", "beans", "drying", "farm"])
def _(S):
    return [
        dot(6, 10, 1.5),
        dot(11, 10, 1.5),
        dot(16, 10, 1.5),
        dot(8.5, 6.5, 1.5),
        dot(13.5, 6.5, 1.5),
        shell(rect(2, 13, 20, 3.5, rr(S, 1.5))),
        line(seg(5, 16.5, 5, 21.5)),
        line(seg(19, 16.5, 19, 21.5)),
        line(seg(5, 19, 19, 19)),
    ]


@icon("cotton-module", CAT, "Large rounded block of harvested cotton wrapped in plastic and strapped, sitting on the ground",
      tags=["cotton", "module", "harvest", "bale", "wrapped", "gin", "field", "fibre"])
def _(S):
    return [
        shell("M3 19V12C3 7.5 7 5 12 5C17 5 21 7.5 21 12V19Z"),
        detail("M8.5 6.5C7.5 9 7.5 15 8.5 19"),
        detail("M15.5 6.5C16.5 9 16.5 15 15.5 19"),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("grain-engulfment", CAT, "Warning triangle with a person sinking chest-deep into a heap of grain",
      tags=["grain bin", "entrapment", "safety", "danger", "warning", "farm accident", "suffocation", "hazard"])
def _(S):
    return [
        shell(poly([(12, 2.5), (22, 20), (2, 20)], closed=True, r=S.r * 1.2)),
        detail(poly([(9.5, 11), (12, 13.5), (14.5, 11)])),
        dot(12, 8.5, 1.4),
        detail("M5.5 18C8 15.8 10 15 12 15C14 15 16 15.8 18.5 18"),
    ]


@icon("tractor-rollover", CAT, "Tractor tipping over on a slope, with a roll bar frame over the seat",
      tags=["rollover", "tractor", "safety", "roll bar", "rops", "accident", "slope", "farm hazard"])
def _(S):
    def r(d):
        return rotd(d, -25, 12, 14)
    return [
        shell(r(circle(8, 15, 4.5))),
        shell(r(circle(19.5, 18, 2.5))),
        shell(r(rect(13.5, 9, 7.5, 5, rr(S, 1.5)))),
        line(r(poly([(5, 9.5), (5, 4.5), (10.5, 4.5), (10.5, 10)], r=S.r * 0.4))),
    ]


@icon("cotton-gin", CAT, "Box-shaped ginning machine with a hand crank, raw cotton feeding in at the top and a roller inside",
      tags=["gin", "cotton", "ginning", "seed removal", "fibre", "machine", "textile", "processing"])
def _(S):
    return [
        line("M7 9C5.5 9 4.5 7.5 5.5 6C6.5 4.5 8.5 5 9.5 5C10 3.5 12.5 3.5 13.5 5C15 4.5 17.5 5 17.5 7C17.5 8.2 16.5 9 15.5 9"),
        shell(rect(3.5, 9, 14, 11, rr(S, 2.5))),
        detail(circle(10.5, 14.5, 2.8)),
        dot(10.5, 14.5, 0.9),
        line(poly([(17.5, 15), (21.5, 15), (21.5, 10.5)], r=S.r * 0.5)),
        line(seg(2.5, 21.5, 19, 21.5)),
    ]


@icon("sugarcane-crusher", CAT, "Pair of rollers with a crank handle crushing cane stalks over a pan that catches the juice",
      tags=["sugarcane", "cane juice", "crusher", "mill", "press", "roller", "juice", "sugar"])
def _(S):
    return [
        line(seg(7, 2, 12, 6)),
        shell(rect(6, 6, 12, 10, rr(S, 2.5))),
        detail(seg(12, 6, 12, 16)),
        line(poly([(18, 9), (22, 9), (22, 4)], r=S.r * 0.5)),
        dot(12, 18.7, 1),
        line(poly([(5, 19.5), (7, 21.5), (17, 21.5), (19, 19.5)], r=S.r * 0.4)),
    ]


# ============================================================================ processing machines

@icon("seed-oil-press", CAT, "Screw press with a threaded shaft and a crossbar handle pressing seeds in a slotted cage, with oil dripping below",
      tags=["oil press", "oil extraction", "seeds", "screw press", "cold press", "expeller", "cooking oil", "mill"])
def _(S):
    return [
        line(seg(5, 3.5, 19, 3.5)),
        shell(rect(10.5, 3.5, 3, 9, rr(S, 1))),
        shell(rect(6, 12.5, 12, 5, rr(S, 1.5))),
        dot(9.5, 15, 0.9),
        dot(14.5, 15, 0.9),
        dot(12, 21, 1.2),
    ]


@icon("rice-huller", CAT, "Rice hulling machine with a hopper on top, one spout pouring rice and another blowing out husks",
      tags=["rice mill", "hulling", "husk", "paddy", "polishing", "milling", "processing", "huller"])
def _(S):
    return [
        shell(poly([(7, 2.5), (17, 2.5), (14, 8), (10, 8)], closed=True, r=S.r * 0.6)),
        shell(rect(4.5, 8, 15, 8, rr(S, 2.5))),
        detail(circle(12, 12, 2)),
        line(seg(8.5, 16, 8.5, 18)),
        dot(6.5, 20.5, 1),
        dot(10.5, 20.5, 1),
        line(seg(19.5, 11, 22, 11)),
        line(seg(19.5, 14, 22, 14)),
    ]


@icon("fanning-mill", CAT, "Box machine on legs with a top hopper and hand crank, grain falling out below while chaff blows out the side",
      tags=["winnowing", "chaff", "grain cleaner", "fan mill", "cleaning grain", "hand crank", "threshing", "farm"])
def _(S):
    return [
        shell(poly([(5.5, 2.5), (17.5, 2.5), (14.5, 8), (8.5, 8)], closed=True, r=S.r * 0.6)),
        shell(rect(5.5, 8, 12, 8, rr(S, 2))),
        line(poly([(5.5, 12), (2.5, 12), (2.5, 8)], r=S.r * 0.5)),
        line(seg(7.5, 16, 7.5, 21.5)),
        line(seg(15.5, 16, 15.5, 21.5)),
        dot(11.5, 19, 1),
        line(seg(17.5, 10.5, 22, 10.5)),
        line(seg(17.5, 13.5, 21, 13.5)),
    ]


@icon("chaff-cutter", CAT, "Spoked cutting wheel with curved blades at the end of a trough holding straw",
      tags=["fodder cutter", "straw cutter", "feed", "livestock", "blade wheel", "hand crank", "hay", "farm"])
def _(S):
    return [
        shell(circle(16.5, 11, 5.5)),
        detail(seg(16.5, 5.5, 16.5, 16.5)),
        detail(seg(11, 11, 22, 11)),
        shell(rect(2, 13, 10, 5, rr(S, 1.5))),
        line(seg(3.5, 13, 4.5, 8.5)),
        line(seg(7, 13, 8, 8.5)),
        line(seg(4.5, 18, 4.5, 21.5)),
        line(seg(16.5, 16.5, 16.5, 21.5)),
    ]


@icon("pedal-thresher", CAT, "Drum studded with wire loops on a stand with a foot pedal, a bundle of stalks held against it",
      tags=["threshing", "rice", "foot pedal", "treadle", "paddy", "wire loop", "drum", "hand tool"])
def _(S):
    return [
        shell(rect(6, 8, 16, 6, rr(S, 3))),
        detail(seg(11, 8, 11, 14)),
        detail(seg(16, 8, 16, 14)),
        line(seg(2.5, 3, 8, 8)),
        line(seg(5.5, 2.5, 10, 6)),
        line(seg(9, 14, 7, 21.5)),
        line(seg(19, 14, 21, 21.5)),
        line(seg(3, 19.5, 11, 19.5)),
    ]


@icon("potato-harvester", CAT, "Digging machine with a sloped conveyor belt lifting potatoes, a wheel below and a tow hitch",
      tags=["potato", "digger", "lifting", "root crop", "harvest", "conveyor", "tractor drawn", "machine"])
def _(S):
    return [
        shell(poly([(3, 15), (17, 5), (17, 11), (3, 21)], closed=True, r=S.r * 0.6)),
        dot(9, 13.5, 1.1),
        dot(13.5, 10.3, 1.1),
        shell(circle(16.5, 18.5, 3)),
        line(seg(17, 8, 22, 8)),
    ]


@icon("swather", CAT, "Self-propelled machine with a wide reel header at the front and an operator cab",
      tags=["windrower", "hay", "cutting", "header", "reel", "harvest", "forage", "mower"])
def _(S):
    return [
        shell(circle(6, 11.5, 4.5)),
        detail(seg(6, 7, 6, 16)),
        detail(seg(1.5, 11.5, 10.5, 11.5)),
        line(seg(2, 18.5, 10, 18.5)),
        shell(rect(12, 6.5, 9.5, 9.5, rr(S, 2.5))),
        detail(rect(14.5, 9, 4.5, 3.5, 0)),
        shell(circle(17, 19.5, 2.2)),
    ]


# ============================================================================ hand and tractor implements

@icon("subsoiler", CAT, "Single long steel shank with a pointed foot hanging from a tractor frame and reaching deep below the soil line",
      tags=["subsoiling", "ripper", "deep tillage", "soil", "compaction", "tractor implement", "shank", "plow"])
def _(S):
    return [
        shell(rect(4, 2.5, 14, 4.5, rr(S, 1.5))),
        line(seg(2, 11, 8, 11)),
        line(seg(16, 11, 22, 11)),
        line(poly([(11, 7), (11, 15), (11.5, 17.5)], r=S.r)),
        shell(poly([(11, 16.5), (18.5, 18.5), (11, 21.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("jab-planter", CAT, "Long-handled hand planter with a seed box and pointed jaws jabbed into the soil",
      tags=["hand planter", "seed", "corn", "maize", "sowing", "dibber", "planting stick", "smallholder"])
def _(S):
    return [
        line(seg(8, 3, 16, 3)),
        line(seg(12, 3, 12, 12)),
        shell(rect(13, 5.5, 6, 6, rr(S, 1.5))),
        shell(poly([(9.5, 12), (14.5, 12), (14, 18), (12, 21.5), (10, 18)], closed=True, r=S.r * 0.5)),
        detail(seg(12, 15, 12, 20)),
        line(seg(2, 17, 7, 17)),
        line(seg(17, 17, 22, 17)),
    ]


@icon("push-seeder", CAT, "Single-wheel push seeder with a small hopper above the wheel, a long handle and seeds dropping in a row",
      tags=["hand seeder", "garden seeder", "walk behind", "sowing", "seed drill", "vegetable", "planting", "row"])
def _(S):
    return [
        shell(poly([(4.5, 3.5), (13.5, 3.5), (11.5, 8.5), (6.5, 8.5)], closed=True, r=S.r * 0.5)),
        line(seg(9, 8.5, 9, 12)),
        shell(circle(9, 16.5, 4.5)),
        dot(9, 16.5, 1),
        line(seg(9, 16.5, 20.5, 6)),
        dot(15.5, 21, 1),
        dot(19.5, 21, 1),
    ]


@icon("three-point-hitch", CAT, "Rear tractor housing with two lower lift arms and an upper link arm joined at a mast in a triangle",
      tags=["hitch", "tractor", "linkage", "implement", "lift arms", "top link", "category", "attachment"])
def _(S):
    return [
        shell(rect(2.5, 3, 5.5, 14.5, rr(S, 2.5))),
        line(seg(8, 8, 19.5, 12.5)),
        line(seg(8, 16, 19.5, 17.5)),
        line(seg(19.5, 12.5, 19.5, 17.5)),
        dot(19.5, 12.5, 1.8),
        dot(19.5, 17.5, 1.8),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("pto-shaft", CAT, "Telescoping drive shaft with a ribbed safety guard and a yoke joint at each end",
      tags=["pto", "power take-off", "driveshaft", "cardan", "universal joint", "tractor", "guard", "implement"])
def _(S):
    return [
        line(poly([(2, 8.5), (4.5, 8.5), (4.5, 15.5), (2, 15.5)])),
        line(seg(4.5, 12, 8, 12)),
        shell(rect(8, 7.5, 8, 9, rr(S, 2))),
        detail(seg(10.7, 7.5, 10.7, 16.5)),
        detail(seg(13.3, 7.5, 13.3, 16.5)),
        line(seg(16, 12, 19.5, 12)),
        line(poly([(22, 8.5), (19.5, 8.5), (19.5, 15.5), (22, 15.5)])),
    ]


# ============================================================================ fruit handling

@icon("molded-fruit-tray", CAT, "Molded pulp tray with rows of round cups, some holding apples",
      tags=["fruit tray", "packing", "apples", "pulp", "cups", "packaging", "orchard", "shipping"])
def _(S):
    parts = [shell(rect(2.5, 3, 19, 18, rr(S, 3)))]
    for cx, cy in ((7.8, 8), (16.2, 8), (7.8, 16), (16.2, 16)):
        parts.append(detail(circle(cx, cy, 2.5)))
    parts.append(dot(16.2, 8, 1.1))
    parts.append(dot(7.8, 16, 1.1))
    return parts


@icon("orchard-bin", CAT, "Large wooden bin on skids heaped with apples, with forklift gaps at the base",
      tags=["apple bin", "bulk bin", "harvest", "orchard", "fruit", "forklift", "crate", "storage"])
def _(S):
    return [
        dot(8.5, 8.3, 2.3),
        dot(15.5, 8.3, 2.3),
        dot(12, 5, 2.3),
        shell(rect(3, 11.5, 18, 7, rr(S, 1.5))),
        detail(seg(6, 15, 18, 15)),
        shell(rect(3, 18.5, 5, 3, 0)),
        shell(rect(16, 18.5, 5, 3, 0)),
    ]


@icon("apple-barrel", CAT, "Wooden barrel with hoops, heaped with apples above the rim",
      tags=["barrel", "apples", "cider", "harvest", "cask", "hoop", "orchard", "autumn"])
def _(S):
    return [
        dot(8.7, 7.5, 2.2),
        dot(15.3, 7.5, 2.2),
        dot(12, 4.7, 2.2),
        shell(poly([(6, 11), (18, 11), (20, 14), (20, 18.5), (18, 21.5), (6, 21.5), (4, 18.5), (4, 14)], closed=True, r=S.r)
              if S.name == "line" else "M6 11H18C20.2 14 20.2 18 18 21.5H6C3.8 18 3.8 14 6 11Z"),
        detail(seg(4.5, 14.2, 19.5, 14.2)),
        detail(seg(4.5, 18.2, 19.5, 18.2)),
    ]


@icon("berry-flat", CAT, "Shallow tray holding a row of small square berry baskets, each filled with berries",
      tags=["strawberries", "punnet", "berries", "flat", "crate", "farm stand", "picking", "pint"])
def _(S):
    return [
        dot(6.3, 4.2, 1.1),
        dot(9, 4.2, 1.1),
        dot(15, 4.2, 1.1),
        dot(17.7, 4.2, 1.1),
        shell(rect(4, 7, 7, 6, L(S, 0, 1.5))),
        shell(rect(13, 7, 7, 6, L(S, 0, 1.5))),
        shell(rect(2, 13, 20, 7, L(S, 1, 3.5))),
    ]


@icon("farm-share-box", CAT, "Open cardboard box with leafy greens, a carrot and a leek sticking out above the flaps",
      tags=["csa", "veg box", "produce box", "subscription", "vegetables", "farm share", "delivery", "organic"])
def _(S):
    return [
        shell(rect(4, 13, 16, 8, rr(S, 1.5))),
        line(seg(4, 13, 2.5, 10)),
        line(seg(20, 13, 21.5, 10)),
        shell("M6 13C4.8 10.5 5.2 7 8 5C10.5 6.5 10.5 10.5 9.5 13Z"),
        shell(poly([(11, 7), (14.5, 7), (12.75, 13)], closed=True, r=S.r * 0.4)),
        line(seg(12.75, 7, 12.75, 3.5)),
        line(seg(17.5, 13, 17.5, 4)),
    ]


@icon("fruit-sizing-ring", CAT, "Flat grading card with a row of round holes of increasing size and a fruit passing through one",
      tags=["fruit grading", "size gauge", "sizing", "apple", "packing", "quality", "diameter", "sorting"])
def _(S):
    return [
        shell(rect(2, 11, 20, 9, rr(S, 2.5))),
        mark(circle(6, 15.5, 1.1)),
        mark(circle(11.5, 15.5, 1.7)),
        mark(circle(17.5, 15.5, 2.4)),
        shell(circle(17.5, 6.5, 3.2)),
    ]


# ============================================================================ fields and growing

def tulip(cx, cy, w, h, S):
    """Tulip bloom: a notched cup whose base sits at (cx, cy) and whose petal tips are h above it."""
    hw = w / 2
    top = cy - h
    pts = [(cx - hw, top), (cx - hw * 0.4, top + h * 0.38), (cx, top), (cx + hw * 0.4, top + h * 0.38), (cx + hw, top),
           (cx + hw * 0.85, cy - h * 0.3), (cx, cy), (cx - hw * 0.85, cy - h * 0.3)]
    return poly(pts, closed=True, r=S.r * 0.8)


@icon("tulip-field", CAT, "Rows of tulip blooms on stems receding toward a horizon line, nearer blooms larger",
      tags=["tulips", "flower field", "bulbs", "flowers", "spring", "netherlands", "rows", "farm"])
def _(S):
    return [
        line(seg(2, 5, 22, 5)),
        shell(tulip(12, 11.5, 4, 4, S)),
        line(seg(12, 11.5, 12, 14.5)),
        shell(tulip(6, 18, 5.6, 5.4, S)),
        line(seg(6, 18, 6, 22)),
        shell(tulip(18, 18, 5.6, 5.4, S)),
        line(seg(18, 18, 18, 22)),
    ]


@icon("sugarcane-field", CAT, "Dense row of tall jointed cane stalks with long arching leaves at the top above the ground line",
      tags=["sugarcane", "cane", "plantation", "stalks", "sugar", "crop", "tall grass", "field"])
def _(S):
    return [
        line(seg(7, 21.5, 7, 9)),
        line(seg(12, 21.5, 12, 6)),
        line(seg(17, 21.5, 17, 9)),
        line(seg(5.5, 16, 8.5, 16)),
        line(seg(10.5, 14, 13.5, 14)),
        line(seg(15.5, 16, 18.5, 16)),
        line("M12 7Q10.5 3.5 5 3"),
        line("M12 7Q13.5 3.5 19 3"),
        line("M7 10Q6 7.5 2.5 7.5"),
        line("M17 10Q18 7.5 21.5 7.5"),
    ]


@icon("fallow-field", CAT, "Unplanted field of rough soil clods with a scattered weed sprig and a horizon line behind",
      tags=["fallow", "bare field", "resting land", "unplanted", "weeds", "soil", "rotation", "idle"])
def _(S):
    return [
        line(seg(2, 8, 22, 8)),
        shell("M3 15.5A2.5 2.5 0 0 1 8 15.5Z"),
        shell("M10 15.5A2.5 2.5 0 0 1 15 15.5Z"),
        shell("M5.5 21.5A2.5 2.5 0 0 1 10.5 21.5Z"),
        shell("M13 21.5A2.5 2.5 0 0 1 18 21.5Z"),
        line(seg(19.5, 16, 19.5, 11.5)),
        line(poly([(17.5, 10), (19.5, 12.5), (21.5, 10)], r=S.r * 0.5)),
    ]


@icon("rice-fish-farming", CAT, "Flooded paddy with rice plants rising above a wavy water line and a small fish swimming below",
      tags=["aquaculture", "paddy", "rice", "fish", "integrated farming", "flooded field", "aquaponics", "water"])
def _(S):
    return [
        line("M5.5 13V4.5"),
        line("M5.5 13C5.5 9 4.5 6.5 2.8 5"),
        line("M5.5 13C5.5 9 6.5 6.5 8.2 5"),
        line("M18.5 13V4.5"),
        line("M18.5 13C18.5 9 17.5 6.5 15.8 5"),
        line("M18.5 13C18.5 9 19.5 6.5 21.2 5"),
        line("M2 13C4 11.8 5.5 11.8 7.5 13C9.5 14.2 11 14.2 13 13C15 11.8 16.5 11.8 18.5 13C20 13.8 21 13.8 22 13"),
        shell(ellipse(10.5, 18, 4.2, 2.6)),
        shell(poly([(14.5, 18), (18.5, 15.2), (18.5, 20.8)], closed=True, r=S.r * 0.4)),
        dot(8.7, 17.4, 0.7),
    ]


@icon("floating-garden", CAT, "Raft of matted plant material floating on water with a row of small vegetable plants growing on top",
      tags=["chinampa", "raft garden", "hydroponic", "floating farm", "water", "vegetables", "wetland", "garden"])
def _(S):
    return [
        line(seg(7, 12.5, 7, 8.5)),
        line(poly([(4.8, 6.5), (7, 9), (9.2, 6.5)], r=S.r * 0.5)),
        line(seg(12, 12.5, 12, 7.5)),
        line(poly([(9.8, 5.5), (12, 8), (14.2, 5.5)], r=S.r * 0.5)),
        line(seg(17, 12.5, 17, 8.5)),
        line(poly([(14.8, 6.5), (17, 9), (19.2, 6.5)], r=S.r * 0.5)),
        shell(rect(2.5, 12.5, 19, 3.5, rr(S, 1.5))),
        line("M2 20C4.5 18.5 7 18.5 9.5 20C12 21.5 14.5 21.5 17 20C19 18.8 20.5 18.8 22 19.5"),
    ]


@icon("potato-hilling", CAT, "Soil ridge mounded around the stem of a leafy potato plant with a hoe blade pulling soil toward it",
      tags=["hilling", "earthing up", "potato", "hoe", "ridge", "mound", "soil", "gardening"])
def _(S):
    return [
        shell("M8.5 21C10 15.5 12 13.5 15.5 13.5C19 13.5 21 15.5 22 21Z"),
        line(seg(15.5, 13.5, 15.5, 9)),
        line(poly([(13, 6.5), (15.5, 9.5), (18, 6.5)], r=S.r * 0.5)),
        line(seg(2.5, 3, 5.5, 14)),
        shell(orect(5.8, 17, 5.5, 2.6, L(S, 0.3, 1.2), -15)),
    ]


@icon("hand-pollination", CAT, "Small paintbrush touching the centre of an open flower, with pollen dots on its tip",
      tags=["pollination", "pollinate", "paintbrush", "flower", "pollen", "greenhouse", "seed saving", "garden"])
def _(S):
    petals = union(*[circle(*polar(9, 15, 4.3, -90 + i * 72), 2.6) for i in range(5)])
    return [
        shell(petals),
        dot(9, 15, 1.4),
        shell(orect(15.6, 8.6, 3, 6, rr(S, 1), 45)),
        line(seg(17.9, 6.1, 21, 3)),
        dot(19.5, 13, 0.8),
        dot(21.3, 10.5, 0.8),
    ]


@icon("fertilizer-spike", CAT, "Tapered fertilizer spike pushed into the soil beside a young plant stem, its flat head above ground",
      tags=["plant food spike", "feeding", "slow release", "houseplant", "garden", "nutrients", "fertiliser", "soil"])
def _(S):
    return [
        line(seg(6.5, 14.5, 6.5, 8)),
        line(poly([(4, 5.5), (6.5, 8.5), (9, 5.5)], r=S.r * 0.5)),
        line(seg(2, 14.5, 11, 14.5)),
        shell(rect(13, 8.5, 8, 3.5, rr(S, 1.2))),
        shell(poly([(14, 14.5), (20, 14.5), (17, 21)], closed=True, r=S.r * 0.4)),
    ]


@icon("rockwool-cube", CAT, "Small fibrous cube seen from above and the side, with a seedling growing out of the top",
      tags=["rockwool", "grow cube", "hydroponics", "seedling", "stonewool", "propagation", "starter plug", "cultivation"])
def _(S):
    return [
        line(seg(12.5, 10.5, 12.5, 6)),
        line(poly([(9.5, 4), (12.5, 7), (15.5, 4)], r=S.r * 0.5)),
        shell(poly([(3.5, 13), (7, 10.5), (20, 10.5), (17, 13)], closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
        shell(rect(3.5, 13, 13.5, 8.5, L(S, 0.3, 1.5))),
        shell(poly([(17, 13), (20, 10.5), (20, 19), (17, 21.5)], closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
        detail("M7 17.5C9 17 10.5 18 13 17"),
    ]


# ============================================================================ farm work

@icon("hoeing", CAT, "Person bent forward swinging a long-handled hoe at the ground",
      tags=["weeding", "hoe", "farmer", "cultivating", "garden work", "tilling", "manual labour", "field work"])
def _(S):
    return [
        dot(6.5, 4.5, 2.1),
        line(seg(7.7, 8, 11, 14)),
        line(poly([(7.5, 21.5), (11, 14), (14.5, 21.5)], r=S.r * 0.6)),
        line(seg(9.2, 9.5, 20, 20)),
        line(seg(17.5, 22, 22, 17.5)),
    ]


@icon("harvesting-grain", CAT, "Person holding a bunch of cut grain stalks in one hand and a curved sickle in the other",
      tags=["reaping", "sickle", "wheat", "harvest", "farmer", "cutting grain", "sheaf", "field work"])
def _(S):
    return [
        dot(12, 4.5, 2.1),
        line(seg(12, 8, 12, 15)),
        line(poly([(9, 21.5), (12, 15), (15, 21.5)], r=S.r * 0.6)),
        line(poly([(12, 9.5), (8, 11)], r=0)),
        line(seg(8, 11, 5, 4)),
        line(seg(8, 11, 8, 3)),
        line(seg(12, 9.5, 16.5, 11.5)),
        line("M16.5 11.5C21.5 12 22 6 18 4.5"),
    ]


@icon("tea-plucking", CAT, "Person with a basket on the back plucking leaves from the flat top of a waist-high tea bush",
      tags=["tea", "picking", "plantation", "leaves", "basket", "harvest", "tea picker", "field work"])
def _(S):
    return [
        dot(8, 4.5, 2.1),
        line(seg(8, 8, 8, 14.5)),
        shell(rect(2.5, 8.5, 3.5, 5.5, rr(S, 1))),
        line(poly([(8, 9.5), (12.5, 11.5), (14, 13)], r=0)),
        line(poly([(6, 21.5), (8, 14.5), (10, 21.5)], r=S.r * 0.4)),
        shell(rect(12, 14.5, 10, 7, rr(S, 3))),
        dot(15.5, 17.5, 0.9),
        dot(19, 18.5, 0.9),
    ]


@icon("sowing-calendar", CAT, "Wall calendar page with a seedling in one cell and other planting days marked",
      tags=["planting schedule", "planting calendar", "seed", "garden planner", "dates", "sow", "season", "farming"])
def _(S):
    return [
        shell(rect(3, 4.5, 18, 16.5, rr(S, 3))),
        detail(seg(3, 9.5, 21, 9.5)),
        line(seg(8, 2.5, 8, 6)),
        line(seg(16, 2.5, 16, 6)),
        line(seg(7.5, 18, 7.5, 14.5)),
        line(poly([(5.3, 12.8), (7.5, 15.3), (9.7, 12.8)], r=S.r * 0.4)),
        dot(14, 13.5, 1),
        dot(18, 13.5, 1),
        dot(14, 17.5, 1),
    ]


@icon("picking-bag", CAT, "Canvas bag worn on the chest with crossed shoulder straps, filled with apples",
      tags=["fruit picking", "orchard", "harvest bag", "apples", "straps", "picker", "satchel", "farm"])
def _(S):
    return [
        line(seg(7, 11.5, 15.5, 2.5)),
        line(seg(17, 11.5, 8.5, 2.5)),
        shell(poly([(4.5, 11.5), (19.5, 11.5), (18, 21.5), (6, 21.5)], closed=True, r=S.r)),
        dot(9, 15.5, 1.6),
        dot(15, 15.5, 1.6),
        dot(12, 18.5, 1.6),
    ]


@icon("wheat-wreath", CAT, "Two curved wheat stalks forming an open wreath with the ears meeting near the top",
      tags=["wreath", "harvest", "wheat", "grain", "autumn decoration", "thanksgiving", "bakery", "laurel"])
def _(S):
    cy = 13.5
    parts = [
        line(arc(12, cy, 6.2, 90, 255)),
        line(arc(12, cy, 6.2, -75, 90)),
    ]
    for a in (125, 160, 195, 230):
        for sign in (-1, 1):
            ang = a if sign < 0 else 180 - a
            cx, cy2 = polar(12, cy, 8.4, ang)
            tangent = math.degrees(math.atan2(math.cos(math.radians(a)), -math.sin(math.radians(a))))
            rot_deg = tangent - 90 + (-25 if sign < 0 else 25)
            if sign > 0:
                rot_deg = -(tangent - 90) * 1 + 0
                rot_deg = 180 - tangent - 90 + 25 + 0
            parts.append(shell(rotd(ellipse(cx, cy2, 1.2, 2.1), rot_deg, cx, cy2)))
    return parts
