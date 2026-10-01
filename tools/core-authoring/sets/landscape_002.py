"""TypeIcon Core: landscape (batch landscape_002).

Volcanoes and geothermal features, caves, ice and glaciers, plate tectonics and earthquakes, rocks, soil
and mining. Drawn from the landforms and objects themselves as simple side views or cross sections.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, polar  # noqa: F401

CAT = "landscape"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def inter(a, b):
    return path_to_d(I(P(a), P(b)))


def grow(d, w):
    """Region d expanded by w on every side (for cutting 2 px gaps)."""
    return path_to_d(U(P(d), ST(d, 2 * w, "round", "round", 4)))


def rot_pts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def wave(x0, x1, y, amp=1.3, n=None):
    """Smooth horizontal wave from x0 to x1 (half-period 3 px by default)."""
    if n is None:
        n = max(2, round((x1 - x0) / 3))
    step = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        xa = x0 + i * step
        sgn = -1 if i % 2 == 0 else 1
        d += (f"C{fmt(xa + step * 0.35)} {fmt(y + sgn * amp)} {fmt(xa + step * 0.65)} {fmt(y + sgn * amp)} "
              f"{fmt(xa + step)} {fmt(y)}")
    return d


def flame(cx, bottom, top, w):
    """Teardrop jet of lava pointing up: round base at `bottom`, tip at `top`."""
    r = w / 2
    cy = bottom - r
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + r * 0.4)} {fmt(top + (cy - top) * 0.45)} {fmt(cx + r)} {fmt(cy - r * 0.9)} "
            f"{fmt(cx + r)} {fmt(cy)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(cx - r)} {fmt(cy)}"
            f"C{fmt(cx - r)} {fmt(cy - r * 0.9)} {fmt(cx - r * 0.4)} {fmt(top + (cy - top) * 0.45)} {fmt(cx)} {fmt(top)}Z")


def snowflake(cx, cy, r):
    """Three crossing strokes (a six-armed flake)."""
    return [seg(*polar(cx, cy, r, a), *polar(cx, cy, r, a + 180)) for a in (-90, -30, 30)]


# ============================================================================ volcanoes

@icon("dormant-volcano", CAT, "Quiet volcanic cone with a flat crater rim and a snow cap, no smoke",
      tags=["volcano", "dormant", "inactive", "mountain", "crater", "snow cap", "geology"])
def _(S):
    cone = poly([(2.5, 20.5), (8.5, 7), (10.5, 7), (12, 8.5), (13.5, 7), (15.5, 7), (21.5, 20.5)], closed=True, r=S.r)
    snow = poly([(6.6, 11.5), (9.5, 14), (12, 12), (14.5, 14), (17.4, 11.5)], r=S.r)
    return [shell(cone), detail(snow)]


@icon("shield-volcano", CAT, "Very wide, gently sloping volcano with a summit vent and a lava trickle",
      tags=["volcano", "lava", "basalt", "hawaii", "dome", "geology", "eruption"])
def _(S):
    dome = ("M2.5 19.5C4.5 15 7.5 11.5 10.5 10.5L12 12L13.5 10.5C16.5 11.5 19.5 15 21.5 19.5Z")
    trickle = "M13 13.5C15 14.5 13.5 16 15.5 17"
    return [shell(dome, stroke_miterlimit="8"), detail(trickle), line(seg(12, 7.5, 12, 4))]


@icon("cinder-cone", CAT, "Small steep cone with a wide bowl crater and loose cinders around its foot",
      tags=["volcano", "scoria cone", "cinders", "crater", "geology", "ash"])
def _(S):
    cone = poly([(5, 20.5), (9, 8), (15, 8), (19, 20.5)], closed=True, r=S.r)
    bowl = "M9.5 7.5C10.5 11.5 13.5 11.5 14.5 7.5"
    body = minus(cone, "M8 6H16V8C14.5 12.5 9.5 12.5 8 8Z")
    return [shell(body), dot(3, 18.5, 1.1), dot(21, 18.5, 1.1), dot(4, 14.5, 1), dot(20, 14.5, 1)]


@icon("stratovolcano", CAT, "Tall steep cone built of layers with smoke rising from its summit",
      tags=["volcano", "composite volcano", "layers", "mountain", "smoke", "geology", "eruption"])
def _(S):
    cone = poly([(3, 21), (10, 7.5), (14, 7.5), (21, 21)], closed=True, r=S.r)
    return [shell(cone),
            detail(seg(7.4, 12.5, 16.6, 12.5)), detail(seg(4.9, 17, 19.1, 17)),
            line("M12 5.5C12 4 13.5 3.8 14.5 3.8C16 3.8 17 3 17.5 2")]


@icon("volcano-cross-section", CAT, "Cut-away volcano with a magma chamber and a conduit rising to the crater",
      tags=["volcano", "diagram", "magma", "conduit", "cutaway", "geology", "science"])
def _(S):
    body = poly([(2.5, 21), (2.5, 13), (6, 13), (10, 4), (14, 4), (18, 13), (21.5, 13), (21.5, 21)], closed=True, r=S.r)
    return [shell(body), detail(ellipse(12, 17, 5, 1.6)), detail(seg(12, 4.5, 12, 15.4))]


@icon("magma-chamber", CAT, "Underground pool of molten rock with a pipe leading up to the surface",
      tags=["magma", "molten rock", "underground", "volcano", "geology", "reservoir"])
def _(S):
    block = rect(2.5, 5.5, 19, 15.5, S.R)
    blob = "M5.5 15.5C5.5 13 8 12 10.8 12.3L10.8 5.5H13.2V12.3C16 12 18.5 13 18.5 15.5C18.5 17.5 16 18 12 18C8 18 5.5 17.5 5.5 15.5Z"
    return [shell(block), Part("dot", blob)]


@icon("lava-flow", CAT, "Thick tongue of lava with crusted ripples flowing down a slope",
      tags=["lava", "molten", "volcano", "magma", "flow", "eruption"])
def _(S):
    tongue = ("M2.5 3C6 3 8.5 5 10 7.5C11 9.2 12.5 10.2 15 10.8C19 11.8 21.5 14.5 21.5 17.5C21.5 20 19.5 21 17 21"
              "C12.5 21 9.5 18.5 8 15C6.8 12.2 5 10 2.5 9.5Z")
    return [shell(tongue),
            detail("M12.5 14C14.5 14 16 15.2 16.5 17"),
            detail("M16.5 13.2C18.3 13.8 19 15 19 16.5"),
            detail("M5.5 6.3C6.5 7 7 8 7.2 9")]


@icon("lava-lake", CAT, "Volcanic crater bowl filled with molten lava and cracked crust",
      tags=["lava", "crater", "volcano", "molten", "magma", "lake"])
def _(S):
    rim = poly([(2, 20.5), (4.5, 9), (19.5, 9), (22, 20.5)], closed=True, r=S.r)
    lake = "M6.5 11H17.5C17.5 15.5 15.5 18 12 18C8.5 18 6.5 15.5 6.5 11Z"
    return [shell(minus(rim, grow(lake, 2))), shell(lake), detail(poly([(9, 13.2), (11, 14.6), (13, 13.2), (15, 14.6)], r=S.r))]


@icon("lava-fountain", CAT, "Jet of lava spraying up from a fissure in flat ground",
      tags=["lava", "eruption", "volcano", "fountain", "magma", "spray"])
def _(S):
    ground = poly([(2.5, 20), (9.5, 20), (12, 22), (14.5, 20), (21.5, 20)], r=S.r)
    return [shell(flame(12, 18, 7, 5)), line(ground),
            dot(6.5, 11, 1.25), dot(17.5, 11, 1.25), dot(8.5, 5, 1.1), dot(15.5, 5, 1.1), dot(12, 2.7, 1.1)]


@icon("lava-tube", CAT, "Rounded tunnel with a flat floor running through solid rock",
      tags=["lava tube", "tunnel", "cave", "volcano", "underground", "geology"])
def _(S):
    block = rect(2.5, 3.5, 19, 17, S.R)
    tube = "M6.5 17V12A5.5 5.5 0 0 1 17.5 12V17Z"
    inner = "M10 17V12.5A2 2 0 0 1 14 12.5V17"
    return [shell(minus(block, tube)), line(inner)]


@icon("volcanic-ash-cloud", CAT, "Billowing ash cloud rising from a volcano with ash falling from it",
      tags=["ash", "ash cloud", "volcano", "eruption", "plume", "smoke", "aviation"])
def _(S):
    cloud = union(circle(7.5, 8, 3.5), circle(12.5, 6, 4), circle(17, 8.5, 3), rect(6, 8, 12, 3.5))
    cone = poly([(3, 21), (7.5, 15.5), (11.5, 15.5), (16, 21)], closed=True, r=S.r)
    return [shell(cloud), shell(cone), line(seg(9.5, 12.5, 9.5, 13.5)),
            dot(15.5, 14.5, 1), dot(19, 14.5, 1), dot(19.5, 18, 1), dot(21, 21, 0.9)]


@icon("fissure-eruption", CAT, "Long crack in flat ground with a curtain of lava spurts along it",
      tags=["fissure", "eruption", "lava", "volcano", "rift", "iceland"])
def _(S):
    return [shell(flame(6, 16, 9, 4)), shell(flame(12, 16, 5, 4)), shell(flame(18, 16, 8, 4)),
            line(seg(2.5, 18.5, 21.5, 18.5)), line(poly([(5, 21.5), (9, 20.5), (13, 21.5), (17, 20.5), (19.5, 21.5)], r=S.r))]


@icon("submarine-volcano", CAT, "Volcano under the sea with bubbles rising from its vent",
      tags=["underwater volcano", "seamount", "ocean", "sea", "volcano", "bubbles"])
def _(S):
    cone = poly([(3, 21), (9.5, 14), (14.5, 14), (21, 21)], closed=True, r=S.r)
    return [shell(cone), line(wave(2.5, 21.5, 4, 1.2, 6)),
            shell(circle(11, 10.5, 1.6)), shell(circle(14.5, 7.8, 1.3))]


@icon("volcanic-island", CAT, "Cone-shaped island rising from the sea with a thin plume of smoke",
      tags=["island", "volcano", "ocean", "sea", "hawaii", "tropical"])
def _(S):
    cone = poly([(4.5, 16.5), (10, 8), (14, 8), (19.5, 16.5)], closed=True, r=S.r)
    return [shell(cone), line("M12 6C11.5 4.5 13 4 14 3.8C15.2 3.6 16 3 16.5 2"),
            line(wave(2.5, 21.5, 20.3, 1.2, 6))]


# ============================================================================ geothermal

@icon("geyser", CAT, "Column of water and steam shooting up from a mound and falling to both sides",
      tags=["geyser", "hot spring", "steam", "eruption", "geothermal", "yellowstone", "water"])
def _(S):
    mound = "M4 21C5 18.5 8 17.5 12 17.5C16 17.5 19 18.5 20 21Z"
    return [shell(mound), line(seg(12, 15.5, 12, 3)),
            line("M10.5 14.5C9.5 9.5 8 7 5 7.5C3.8 7.8 3.2 9 3.2 10.5"),
            line("M13.5 14.5C14.5 9.5 16 7 19 7.5C20.2 7.8 20.8 9 20.8 10.5")]


@icon("hot-spring", CAT, "Round pool with wavy steam rising from its surface",
      tags=["hot spring", "onsen", "thermal pool", "spa", "geothermal", "steam", "bath"])
def _(S):
    return [shell(ellipse(12, 17.5, 9, 3.5)),
            line("M7.5 11.5C6.2 10 8.8 8.5 7.5 7C6.8 6.2 6.8 5 7.5 4"),
            line("M12 11.5C10.7 10 13.3 8.5 12 7C11.3 6.2 11.3 4.5 12 3"),
            line("M16.5 11.5C15.2 10 17.8 8.5 16.5 7C15.8 6.2 15.8 5 16.5 4")]


@icon("mud-pot", CAT, "Pool of bubbling mud with a big bubble and another bursting at the surface",
      tags=["mud pot", "mud pool", "bubbling", "geothermal", "volcanic", "hot mud"])
def _(S):
    pool = union(ellipse(12, 18.5, 9.5, 3), circle(8.5, 14, 3.4))
    return [shell(pool),
            line(seg(17, 13.5, 17, 10)), line(seg(14.3, 14, 13.2, 11.2)), line(seg(19.7, 14, 20.8, 11.2))]


@icon("fumarole", CAT, "Crack in rocky ground releasing curling steam",
      tags=["fumarole", "steam vent", "volcanic gas", "geothermal", "volcano", "sulfur"])
def _(S):
    rock = poly([(2.5, 21), (4.5, 16), (9, 14.5), (11, 16), (13, 14.5), (19, 15.5), (21.5, 21)], closed=True, r=S.r)
    return [shell(rock), detail(poly([(12, 16.5), (11, 18.5), (12.5, 20)], r=S.r)),
            line("M10 12C8.5 10.5 10.8 9 9.8 7.5C9 6.3 9.8 4.5 11 4"),
            line("M14 12C15.5 10 13 8 15 6C15.8 5.2 16.8 4.5 18 4.5")]


@icon("caldera", CAT, "Wide collapsed volcanic basin with a low rim and a small cone in the middle",
      tags=["caldera", "crater", "volcano", "basin", "collapse", "geology"])
def _(S):
    prof = poly([(2.5, 20.5), (6, 11), (8, 15.5), (10, 15.5), (12, 13), (14, 15.5), (16, 15.5), (18, 11), (21.5, 20.5)],
                closed=True, r=S.r)
    return [shell(prof, stroke_miterlimit="8")]

# ============================================================================ lava rock

@icon("obsidian", CAT, "Glassy volcanic stone with curved shell-like fracture lines and a shine mark",
      tags=["obsidian", "volcanic glass", "black stone", "rock", "mineral", "geology"])
def _(S):
    shard = poly([(3.5, 15), (7.5, 5.5), (15, 3), (21, 9), (19.5, 17.5), (12, 21), (5.5, 19.5)], closed=True, r=S.r)
    return [shell(shard), detail(arc(19, 18, 5.5, 195, 265)), detail(arc(19, 18, 10, 200, 255)),
            detail(seg(8.5, 10.5, 10, 7.5))]


@icon("pumice", CAT, "Light porous stone full of holes floating on water",
      tags=["pumice", "volcanic rock", "porous", "floating stone", "scrub", "geology"])
def _(S):
    stone = poly([(3, 12), (5, 6.5), (10, 4.5), (16, 5), (20.5, 8), (21, 12.5), (17, 15.5), (7, 15.5)], closed=True, r=L(S, 0, 3))
    return [shell(stone), dot(8, 9, 1.1), dot(12.5, 8, 1.1), dot(16.5, 10.5, 1.1), dot(11, 12, 1.1),
            line(wave(2.5, 21.5, 19.5, 1.2, 6))]


# ============================================================================ caves

@icon("stalactite", CAT, "Pointed rock spikes hanging from a cave ceiling with a drip below",
      tags=["stalactite", "cave", "cavern", "limestone", "dripstone", "geology"])
def _(S):
    body = poly([(2.5, 2.5), (21.5, 2.5), (21.5, 5.5), (20.5, 5.5), (18.5, 15), (16.5, 5.5), (15.5, 5.5), (13.5, 12),
                 (11.5, 5.5), (10.5, 5.5), (7, 19.5), (3.5, 5.5), (2.5, 5.5)], closed=True, r=S.r)
    return [shell(body, stroke_miterlimit="10"), dot(13.5, 16.5, 1.2)]


@icon("stalagmite", CAT, "Rounded rock cones rising from a cave floor with a drop falling above",
      tags=["stalagmite", "cave", "cavern", "limestone", "dripstone", "geology"])
def _(S):
    body = union(rect(2.5, 18, 19, 3.5, min(S.R, 1.5)),
                 "M8.5 18.5L10.5 8.5A1.5 1.5 0 0 1 13.5 8.5L15.5 18.5Z",
                 "M3.5 18.5L5 13.5A1.2 1.2 0 0 1 7.4 13.5L8 18.5Z",
                 "M16 18.5L16.8 14.5A1.2 1.2 0 0 1 19.2 14.5L20.5 18.5Z")
    return [shell(body), dot(12, 3.5, 1.2)]


@icon("cave-column", CAT, "Stalactite and stalagmite joined into an hourglass column from ceiling to floor",
      tags=["cave column", "pillar", "cave", "stalactite", "stalagmite", "limestone"])
def _(S):
    col = ("M7.5 5C9.8 7.5 10.3 9.8 10.3 12C10.3 14.2 9.8 16.5 7.5 19H16.5C14.2 16.5 13.7 14.2 13.7 12"
           "C13.7 9.8 14.2 7.5 16.5 5Z")
    body = union(rect(2.5, 2.5, 19, 3, min(S.R, 1.5)), rect(2.5, 18.5, 19, 3, min(S.R, 1.5)), col,
                 poly([(18, 5), (19.5, 10), (21, 5)], closed=True), poly([(3, 19), (4.5, 14), (6, 19)], closed=True))
    return [shell(body, stroke_miterlimit="10")]


@icon("cave-pool", CAT, "Underground pool below a cave ceiling with dripping stalactites",
      tags=["cave pool", "underground lake", "cave", "cenote", "stalactite", "drip"])
def _(S):
    body = poly([(2.5, 2.5), (21.5, 2.5), (21.5, 5.5), (18.5, 5.5), (16.5, 10), (14.5, 5.5), (10, 5.5), (7.5, 12.5),
                 (5, 5.5), (2.5, 5.5)], closed=True, r=S.r)
    return [shell(body), dot(7.5, 15, 1.1), shell(ellipse(12, 19, 9, 2.5))]


@icon("ice-cave", CAT, "Arched opening in a wall of ice with icicles hanging inside",
      tags=["ice cave", "glacier cave", "ice", "cave", "frozen", "arctic"])
def _(S):
    outer = poly([(2.5, 21), (3.5, 11), (7, 5.5), (12, 3.5), (17, 5.5), (20.5, 11), (21.5, 21)], closed=True, r=S.r)
    hole = "M7 22V14.5A5 5 0 0 1 17 14.5V22Z"
    ice = union(minus(outer, hole), poly([(9.3, 11), (10.3, 15), (11.3, 10)], closed=True),
                poly([(12.7, 10), (13.7, 14), (14.7, 11)], closed=True))
    return [shell(ice, stroke_miterlimit="10")]


@icon("underground-river", CAT, "Cross section of rock with a river flowing through a tunnel",
      tags=["underground river", "subterranean", "cave", "tunnel", "water", "karst"])
def _(S):
    block = rect(2.5, 3, 19, 18, S.R)
    hole = "M5.5 18V13A6.5 5 0 0 1 18.5 13V18Z"
    return [shell(minus(block, hole)), line(wave(7.5, 16.5, 14.2, 0.9, 3))]


@icon("cave-painting", CAT, "Rock wall with a simple ancient drawing of a horned animal",
      tags=["cave painting", "rock art", "prehistoric", "petroglyph", "ancient", "history"])
def _(S):
    slab = poly([(2.5, 5), (8, 3), (16, 3.5), (21.5, 5), (21, 19.5), (13, 21), (3, 19.5)], closed=True, r=S.r)
    return [shell(slab), detail(poly([(7, 16.5), (7, 11.5), (14.5, 11.5), (14.5, 16.5)], r=S.r)),
            detail(poly([(14.5, 11.5), (17, 9), (15.5, 7)], r=S.r))]


@icon("spelunking-helmet", CAT, "Caving helmet with a headlamp shining forward",
      tags=["caving helmet", "spelunking", "headlamp", "caver", "helmet", "mining"])
def _(S):
    hat = union("M2.5 17C2.5 10 6 6 9.5 6C13 6 16.5 10 16.5 17Z", rect(2.5, 16, 14, 4, min(S.R, 1.5)))
    return [shell(hat), detail(seg(9.5, 6.5, 9.5, 13)), shell(circle(16.5, 11.5, 2.2)),
            line(seg(20.2, 11.5, 22, 11.5)), line(seg(19.8, 8.8, 21.5, 7.6)), line(seg(19.8, 14.2, 21.5, 15.4))]


@icon("rock-shelter", CAT, "Overhanging rock ledge forming a shallow shelter above a small tent",
      tags=["rock shelter", "overhang", "ledge", "cliff", "shelter", "bivouac"])
def _(S):
    rock = poly([(2.5, 21.5), (2.5, 3.5), (21.5, 3.5), (21.5, 9.5), (10.5, 9.5), (8.5, 12.5), (8.5, 21.5)], closed=True, r=S.r)
    tent = poly([(11.5, 21), (15.5, 14.5), (19.5, 21)], closed=True, r=S.r)
    return [shell(rock), shell(tent)]


# ============================================================================ ice

@icon("glacier", CAT, "Mountain peak with a long slope of ice sliding down its flank, split by crevasses",
      tags=["glacier", "ice", "valley glacier", "mountain", "alpine", "climate"])
def _(S):
    body = poly([(2.5, 21.5), (8, 4.5), (12.5, 11), (21.5, 17), (21.5, 21.5)], closed=True, r=S.r)
    return [shell(body), detail(seg(14.5, 12.8, 13.5, 16.2)), detail(seg(18.3, 15.6, 17.4, 19))]


@icon("ice-sheet", CAT, "Vast gently domed sheet of ice ending in a cliff at the sea",
      tags=["ice sheet", "ice cap", "antarctica", "greenland", "polar", "climate"])
def _(S):
    dome = "M2.5 17C3.5 11.5 8 8.5 13 8.5C17 8.5 20 10 21.5 12V17Z"
    return [shell(dome), line(wave(2.5, 21.5, 20.3, 1.2, 6))]


@icon("ice-shelf", CAT, "Thick flat slab of ice floating on the sea with a sheer front face",
      tags=["ice shelf", "antarctica", "polar", "ice", "calving front", "climate"])
def _(S):
    slab = poly([(2.5, 9), (6.5, 5), (21.5, 5), (21.5, 11), (17.5, 15), (2.5, 15)], closed=True, r=S.r)
    return [shell(slab), detail(seg(3, 9, 17.5, 9)), detail(seg(17.5, 9, 17.5, 14.5)), line(wave(2.5, 21.5, 19.5, 1.2, 6))]


@icon("glacier-calving", CAT, "Chunk of ice breaking off a glacier front and splashing into the water",
      tags=["calving", "glacier", "iceberg", "ice", "melting", "climate change"])
def _(S):
    cliff = poly([(2.5, 21), (2.5, 4), (10.5, 4), (9, 8), (10.5, 12), (9.5, 21)], closed=True, r=S.r)
    chunk = poly(rot_pts([(14, 6), (19, 6), (19, 11), (14, 11)], 20, 16.5, 8.5), closed=True, r=L(S, 0, 1.2))
    return [shell(cliff), shell(chunk), line(seg(13.5, 17, 12.8, 15)), line(seg(19.5, 17, 20.2, 15)),
            line(wave(12, 21.5, 20.3, 1.1, 3))]


@icon("crevasse", CAT, "Deep jagged crack splitting a snowfield",
      tags=["crevasse", "crack", "glacier", "snow", "mountaineering", "danger"])
def _(S):
    block = rect(2.5, 6, 19, 15, S.R)
    crack = poly([(8.5, 5), (15.5, 5), (13.8, 10), (14.8, 12.5), (12.3, 17.5), (11.6, 13), (10.2, 10.5)], closed=True)
    return [shell(minus(block, crack))]


@icon("cirque", CAT, "Mountain profile scooped into a bowl under a steep headwall, with a small lake on its floor",
      tags=["cirque", "corrie", "cwm", "tarn", "mountain", "glacial"])
def _(S):
    prof = "M2.5 21.5V4.5L7 3.5C8 9.5 9 13.5 13 13.5C16 13.5 17 10.5 18.5 10.5L21.5 15V21.5Z"
    return [shell(prof, stroke_miterlimit="6"), detail(seg(9, 17.5, 15, 17.5))]


@icon("ice-floe", CAT, "Flat slabs of floating ice drifting on the waves",
      tags=["ice floe", "sea ice", "drift ice", "arctic", "polar", "ice"])
def _(S):
    a = poly([(2.5, 14.5), (3.5, 10.5), (10, 10), (11.5, 14.5)], closed=True, r=L(S, 0, 1.2))
    b = poly([(13.5, 14.5), (14.5, 9), (20.5, 8.5), (21.5, 14.5)], closed=True, r=L(S, 0, 1.2))
    return [shell(a), shell(b), line(wave(2.5, 21.5, 19, 1.2, 6))]


# --------------------------------------------------------------------------- more helpers

def tf(pts, deg, cx, cy):
    """Local points (origin at the shape centre) rotated clockwise by deg and moved to (cx, cy)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


def bez(cmds, deg=0.0, cx=12.0, cy=12.0):
    """Path from local commands [("M", p), ("L", p), ("C", p1, p2, p3), ("Z",)] rotated about a centre."""
    out = []
    for c in cmds:
        if c[0] == "Z":
            out.append("Z")
            continue
        pts = tf(list(c[1:]), deg, cx, cy)
        out.append(c[0] + "".join(f"{fmt(x)} {fmt(y)} " for x, y in pts).rstrip())
    return "".join(out)


def oval(S, cx, cy, rx, ry):
    """Ellipse for Rounded, pointed lens for Line (so the two styles really differ)."""
    if S.name == "line":
        return (f"M{fmt(cx - rx)} {fmt(cy)}Q{fmt(cx)} {fmt(cy - 2 * ry)} {fmt(cx + rx)} {fmt(cy)}"
                f"Q{fmt(cx)} {fmt(cy + 2 * ry)} {fmt(cx - rx)} {fmt(cy)}Z")
    return ellipse(cx, cy, rx, ry)


def diamond(x, y, r):
    return poly([(x, y - r), (x + r, y), (x, y + r), (x - r, y)], closed=True)


# ============================================================================ chunk 2: volcanic bomb, ice and snow

@icon("volcanic-bomb", CAT, "Spindle-shaped lump of cooled lava with twisted ends flying through the air",
      tags=["volcanic bomb", "lava bomb", "ejecta", "volcano", "eruption", "projectile", "rock"])
def _(S):
    body = bez([("M", (-8, 2)), ("C", (-6, -5), (3, -5.5), (8, -3.5)), ("C", (5, 4), (-3, 5.5), (-8, 2)), ("Z",)],
               -25, 15.5, 9)
    twist = bez([("M", (-1, -4.3)), ("C", (1, -1.5), (1, 1.5), (-1, 4.3))], -25, 15.5, 9)
    return [shell(body, stroke_miterlimit="6"), detail(twist),
            line(seg(6.4, 12.4, 2.4, 14.1)), line(seg(8.8, 17.4, 4.8, 19.1))]


@icon("pack-ice", CAT, "Top view of jagged pieces of sea ice packed together with narrow gaps of water",
      tags=["pack ice", "sea ice", "arctic", "polar", "floes", "frozen sea", "ice"])
def _(S):
    r = L(S, 0, 1.2)
    a = poly([(3, 6), (7, 2.5), (11, 4.5), (10, 10), (5, 11)], closed=True, r=r)
    b = poly([(14.5, 3.5), (21, 3), (21, 9), (18.5, 11), (14.5, 9)], closed=True, r=r)
    c = poly([(3, 15), (8, 14), (10.5, 18), (8.5, 21.5), (3, 20.5)], closed=True, r=r)
    d = poly([(14.5, 15.5), (19, 13.5), (21.5, 17), (20, 21.5), (14.5, 20)], closed=True, r=r)
    return [shell(a), shell(b), shell(c), shell(d)]


@icon("frozen-lake", CAT, "Rounded lake covered in ice with a crack and a snowflake on the surface",
      tags=["frozen lake", "ice", "winter", "skating", "pond", "crack", "snowflake"])
def _(S):
    lake = "M3 12C3 7.5 7 5.5 11.5 5.5C16 5.5 21 7 21.5 11.5C22 16 17 18.5 11.5 18.5C6 18.5 3 16 3 12Z"
    return [shell(lake), *[detail(d) for d in snowflake(8, 12, 2.5)],
            detail(poly([(15, 5.8), (13.5, 9.8), (17, 12.3), (14.5, 18.2)], r=S.r))]


@icon("icicles", CAT, "Row of pointed icicles hanging from the edge of a roof",
      tags=["icicles", "ice", "roof", "winter", "frozen", "eaves", "cold"])
def _(S):
    eave = rect(2.5, 3, 19, 3.5, min(S.R, 1.5))
    sp = lambda x, n: poly([(x - 1.6, 6), (x + 1.6, 6), (x, n)], closed=True)
    body = union(eave, sp(5, 16.5), sp(12, 19.5), sp(19, 12))
    return [shell(body)]


@icon("permafrost", CAT, "Ground cross section with a thin layer of soil over frozen ground holding lenses of ice",
      tags=["permafrost", "frozen ground", "tundra", "soil", "arctic", "climate", "ice"])
def _(S):
    block = rect(2.5, 6, 19, 15.5, S.R)
    return [shell(block), detail(seg(3, 10, 21, 10)),
            Part("dot", diamond(7.5, 15.5, 2)), Part("dot", diamond(12.5, 18, 1.8)), Part("dot", diamond(17, 15, 2)),
            line(seg(6, 3.5, 5, 1.8)), line(seg(12, 3.5, 12, 1.8)), line(seg(18, 3.5, 19, 1.8))]


@icon("snowdrift", CAT, "Smooth curved mound of snow piled against a fence post with wind lines",
      tags=["snowdrift", "snow", "winter", "blizzard", "wind", "fence", "snowbank"])
def _(S):
    mound = "M2.5 20.5C7 20.5 9 15 13 12.5C15 11.3 17 11 19.5 11V20.5Z"
    body = union(mound, rect(15.5, 3.5, 4, 17, min(S.R, 1.5)))
    return [shell(body), line("M3 9H9.5C11.2 9 11.2 6.3 9.5 6.3")]


@icon("snow-cornice", CAT, "Overhanging curl of snow on a mountain ridge above a steep drop",
      tags=["cornice", "snow", "ridge", "avalanche", "mountaineering", "overhang", "winter"])
def _(S):
    d = ("M2.5 21.5L8.5 8C10 4.5 15 3.5 18.5 4.5C21.5 5.5 22 9.5 19 10.3C17.5 10.7 16 10 16 9L13 11.5V21.5Z")
    return [shell(d), dot(18, 16, 1.1), dot(20.5, 19.5, 1)]


@icon("hoarfrost-branch", CAT, "Bare twig covered in spiky frost crystals along its length",
      tags=["hoarfrost", "frost", "rime", "branch", "twig", "winter", "ice crystals"])
def _(S):
    ax, ay, bx, by = 3.5, 20.5, 19.5, 4.5
    parts = [line(seg(ax, ay, bx, by))]
    for f in (0.28, 0.5, 0.72):
        px, py = ax + (bx - ax) * f, ay + (by - ay) * f
        for sgn in (1, -1):
            a = math.radians(-45 + sgn * 48)
            parts.append(line(seg(px, py, px + 4 * math.cos(a), py + 4 * math.sin(a))))
    parts.append(line(seg(bx, by, bx + 2, by - 0.0)))
    return parts


@icon("glacial-erratic", CAT, "Large lone boulder sitting on flat ground, far from any cliff",
      tags=["erratic", "boulder", "glacier", "rock", "glacial", "geology", "lone stone"])
def _(S):
    rock = poly([(7.5, 18.5), (6.5, 12), (10.5, 6), (16, 4.5), (20.5, 8.5), (19.5, 18.5)], closed=True, r=S.r)
    return [shell(rock), detail("M14.5 5.5C13 9 15.5 11.5 13.5 15.5"),
            line(seg(2.5, 18.5, 7.5, 18.5)), line(seg(19.5, 18.5, 21.5, 18.5))]


@icon("frozen-waterfall", CAT, "Cliff face with a waterfall frozen into hanging columns of ice",
      tags=["frozen waterfall", "ice fall", "icefall", "ice climbing", "winter", "cliff", "icicles"])
def _(S):
    block = rect(2.5, 3.5, 19, 17.5, S.R)
    col = lambda x, n: Part("dot", poly([(x - 1.5, 4.5), (x + 1.5, 4.5), (x, n)], closed=True))
    return [shell(block), col(7, 15), col(12, 18.5), col(17, 12)]


def head(x, y, ang, size=3.0, spread=40):
    """Open arrowhead chevron with its tip at (x, y) pointing along ang degrees (0 = right, 90 = down)."""
    pts = []
    for sgn in (1, -1):
        a = math.radians(ang + 180 + sgn * spread)
        pts.append((x + size * math.cos(a), y + size * math.sin(a)))
    return poly([pts[0], (x, y), pts[1]], r=0)


# ============================================================================ tectonics and earthquakes

@icon("tectonic-plates", CAT, "Two slabs of crust meeting at a jagged boundary with arrows pushing them together",
      tags=["tectonic plates", "plate boundary", "convergent", "crust", "geology", "earthquake", "continental drift"])
def _(S):
    r = L(S, 0, 1)
    left = poly([(2.5, 11.5), (10, 11.5), (9, 14.5), (10, 17.5), (9, 21), (2.5, 21)], closed=True, r=r)
    right = poly([(21.5, 11.5), (14, 11.5), (15, 14.5), (14, 17.5), (15, 21), (21.5, 21)], closed=True, r=r)
    return [shell(left), shell(right),
            line(seg(3, 6, 9.5, 6)), line(head(9.5, 6, 0)), line(seg(21, 6, 14.5, 6)), line(head(14.5, 6, 180))]


@icon("geological-fault", CAT, "Block of ground split by a slanted crack with one side dropped lower",
      tags=["fault", "fault line", "earthquake", "geology", "rift", "crack", "slip"])
def _(S):
    r = L(S, 0, 1)
    left = poly([(2.5, 4.5), (12, 4.5), (8.4, 21.5), (2.5, 21.5)], closed=True, r=r)
    right = poly([(15.2, 8.5), (21.5, 8.5), (21.5, 21.5), (12.4, 21.5)], closed=True, r=r)
    return [shell(left), shell(right), detail(seg(5.3, 17, 5.3, 9.5)), detail(head(5.3, 9.5, 270, 2.6)),
            detail(seg(18.5, 12, 18.5, 18)), detail(head(18.5, 18, 90, 2.6))]


@icon("rock-strata", CAT, "Block of ground made of stacked rock layers with a pebble and a rough bottom band",
      tags=["strata", "rock layers", "sedimentary", "stratigraphy", "geology", "layers", "cross section"])
def _(S):
    block = rect(2.5, 3.5, 19, 17.5, S.R)
    return [shell(block), detail("M3 9C8 8 14 10.5 21 9"), detail("M3 15C9 16 15 13.5 21 15"),
            dot(8, 12.4, 1.1), dot(15.5, 12, 1.1), dot(11.5, 18.3, 1.1)]


@icon("rock-folds", CAT, "Layers of rock bent into a wavy arch and trough fold",
      tags=["fold", "folded rock", "anticline", "syncline", "geology", "strata", "compression"])
def _(S):
    block = rect(2.5, 3.5, 19, 17.5, S.R)
    return [shell(block), detail(wave(3, 21, 9.5, 2.6, 2)), detail(wave(3, 21, 14.8, 2.6, 2))]


@icon("earth-layers", CAT, "Globe with a wedge cut out showing the crust, mantle and core in rings",
      tags=["earth layers", "earth structure", "crust", "mantle", "core", "geology", "planet", "cutaway"])
def _(S):
    globe = "M21.5 12H14.6A2.6 2.6 0 0 0 12 9.4V2.5A9.5 9.5 0 1 0 21.5 12Z"
    return [shell(globe), detail(arc(12, 12, 5.8, 0, 270))]


@icon("seismograph", CAT, "Seismograph with a drum of paper, a zigzag trace and a pen arm",
      tags=["seismograph", "seismometer", "earthquake", "tremor", "recorder", "geology", "trace"])
def _(S):
    drum = rect(7.5, 10, 14, 11.5, S.R)
    return [shell(drum),
            detail(poly([(9, 16), (11, 16), (12.5, 12.6), (14.5, 19.4), (16, 14), (17, 16), (20, 16)], r=L(S, 0, 0.5))),
            line(poly([(3, 21.5), (3, 4), (15, 4), (15, 9.5)], r=S.r))]


@icon("seismic-wave", CAT, "Flat line with a burst of sharp zigzag spikes in the middle",
      tags=["seismic wave", "earthquake", "tremor", "waveform", "shock", "vibration", "signal"])
def _(S):
    return [line(poly([(2.5, 12), (5, 12), (7.5, 7), (10.5, 17), (13.5, 4), (16.5, 20), (18.5, 12), (21.5, 12)], r=L(S, 0, 0.5)))]


@icon("earthquake", CAT, "Cracked house with shaking marks on both sides",
      tags=["earthquake", "quake", "tremor", "shaking", "damage", "disaster", "cracked building"])
def _(S):
    house = poly([(6.5, 21), (6.5, 10.5), (12, 5), (17.5, 10.5), (17.5, 21)], closed=True, r=S.r)
    return [shell(house), detail(poly([(12, 5.5), (10.3, 10), (13.7, 13), (11.3, 16.5), (12.6, 21)], r=L(S, 0, 0.5))),
            line("M3.5 9C2.3 10.5 2.3 14 3.5 15.5"), line("M20.5 9C21.7 10.5 21.7 14 20.5 15.5")]


@icon("epicenter", CAT, "Dot at the centre of broken rings spreading outward",
      tags=["epicenter", "epicentre", "earthquake", "quake origin", "seismic", "waves", "focus"])
def _(S):
    parts = [dot(12, 12, 2)]
    for a in (45, 135, 225, 315):
        parts.append(line(arc(12, 12, 9.5, a - 25, a + 25)))
    for a in (0, 90, 180, 270):
        parts.append(line(arc(12, 12, 5.5, a - 35, a + 35)))
    return parts


@icon("richter-scale", CAT, "Scale bar with tick marks, a pointer above it and a small seismic zigzag",
      tags=["richter scale", "magnitude", "earthquake", "seismic", "measurement", "scale", "intensity"])
def _(S):
    bar = rect(2.5, 13, 19, 7.5, min(S.R, 2))
    return [shell(bar), detail(seg(7.5, 13.5, 7.5, 16.5)), detail(seg(12, 13.5, 12, 16.5)), detail(seg(16.5, 13.5, 16.5, 16.5)),
            shell(poly([(14.5, 3), (19.5, 3), (17, 8.5)], closed=True, r=S.r)),
            line(poly([(2.5, 8), (4.5, 8), (6, 4.8), (8, 9.5), (9.5, 6), (11, 8)], r=L(S, 0, 0.4)))]


def rc_arrow(cx, cy, r, a0, a1):
    tip = polar(cx, cy, r, a1)
    return [line(arc(cx, cy, r, a0, a1)), line(head(tip[0], tip[1], a1 + 90 + 12, 3.0))]


@icon("rock-cycle", CAT, "Three different rocks linked in a triangle by circular arrows",
      tags=["rock cycle", "igneous", "sedimentary", "metamorphic", "geology", "earth science", "cycle"])
def _(S):
    cx, cy, r = 12, 13, 8
    top = polar(cx, cy, r, -90)
    br = polar(cx, cy, r, 30)
    bl = polar(cx, cy, r, 150)
    parts = [solid(poly(regular(top[0], top[1], 3.2, 5, -90), closed=True, r=L(S, 0, 0.8))),
             solid(poly(regular(br[0], br[1], 3.3, 4, -45), closed=True, r=L(S, 0, 0.8))),
             Part("dot", circle(bl[0], bl[1], 2.8))]
    for a in (-90, 30, 150):
        parts += rc_arrow(cx, cy, r, a + 27, a + 120 - 27)
    return parts


# ============================================================================ soil, rocks and mining

@icon("soil-profile", CAT, "Vertical cut of ground showing grass on top, then layers of soil, subsoil and bedrock",
      tags=["soil profile", "soil layers", "horizons", "topsoil", "bedrock", "geology", "agriculture"])
def _(S):
    block = poly([(4, 5.5), (20, 5.5), (20, 21.5), (4, 21.5)], closed=True, r=S.r)
    return [shell(block), detail(wave(4.5, 19.5, 10, 0.9, 4)), detail(seg(4.5, 14, 19.5, 14)),
            detail(poly([(4.5, 18), (8, 19.4), (12, 17.8), (16, 19.4), (19.5, 18)])),
            line(poly([(5.3, 2.6), (7.2, 5.5), (9.1, 2.6)])), line(poly([(14.9, 2.6), (16.8, 5.5), (18.7, 2.6)]))]


@icon("erosion", CAT, "Rock face with a jagged worn edge, wind lines blowing at it and bits breaking away",
      tags=["erosion", "weathering", "wind erosion", "rock", "geology", "wear", "cliff"])
def _(S):
    rock = poly([(21.5, 21.5), (21.5, 4), (12.5, 4), (10.5, 7.5), (13.5, 10.5), (10.5, 13.5), (13.5, 17), (11.5, 21.5)],
                closed=True, r=S.r)
    return [shell(rock), line("M2.5 8.5H6.5C8.2 8.5 8.2 5.8 6.5 5.8"), line(seg(2.5, 12.5, 7.5, 12.5)),
            dot(6.3, 17, 1.1), dot(3.6, 20, 1)]


@icon("gravel", CAT, "Heap of many small angular stones resting on the ground",
      tags=["gravel", "stones", "pebbles", "crushed rock", "aggregate", "road", "rubble"])
def _(S):
    rr = L(S, 0, 0.8)
    def st(x, y, r, rot):
        return solid(poly(regular(x, y, r, 5, rot), closed=True, r=rr))
    return [st(5.5, 16.4, 2.6, -90), st(12, 16.6, 2.6, -60), st(18.5, 16.4, 2.6, -110),
            st(8.8, 10.9, 2.5, -80), st(15.2, 10.9, 2.6, -100), st(12, 5.4, 2.5, -70),
            line(seg(2.5, 21.2, 21.5, 21.2))]


@icon("sand-pile", CAT, "Cone-shaped heap of fine sand with loose grains around it",
      tags=["sand", "sand pile", "sand heap", "dune", "grains", "beach", "construction"])
def _(S):
    heap = "M3 20.5C6 20.5 9 18 10.5 13.5C11.4 10.8 12 8.5 12 8.5C12 8.5 12.6 10.8 13.5 13.5C15 18 18 20.5 21 20.5Z"
    return [shell(heap), dot(12, 15.5, 1.1), dot(9.3, 18.4, 0.9), dot(14.7, 18.4, 0.9),
            dot(4, 14.5, 1), dot(20, 14.5, 1), dot(6.5, 9.5, 0.9), dot(17.5, 9.5, 0.9)]


@icon("clay-lump", CAT, "Smooth lump of modelling clay with a thumb dent pressed into it",
      tags=["clay", "lump of clay", "pottery", "modelling clay", "sculpting", "ceramics", "dough"])
def _(S):
    lump = poly([(3, 20), (3.5, 14), (8, 9.5), (15, 9), (20.5, 13), (21, 20)], closed=True, r=L(S, 1.5, 5))
    return [shell(lump), detail(ellipse(10.5, 14.5, 2.3, 1.4))]


@icon("rock-cairn", CAT, "Stack of four flat stones decreasing in size toward the top",
      tags=["cairn", "rock stack", "trail marker", "stacked stones", "hiking", "balance", "zen"])
def _(S):
    rr = min(S.R, 2.5)
    body = union(rect(3, 16.5, 18, 5, rr), rect(5.5, 11.5, 13, 5.5, rr), rect(8, 7, 8, 5, rr), rect(9.7, 3, 4.6, 4.5, 2.2))
    return [shell(body), detail(seg(6, 16.8, 18, 16.8)), detail(seg(8.5, 11.7, 15.5, 11.7)), detail(seg(10.2, 7.2, 13.8, 7.2))]


@icon("rock-sample-bag", CAT, "Small cloth sample bag tied at the neck with a label on the front",
      tags=["sample bag", "specimen bag", "rock sample", "field kit", "geology", "collection", "pouch"])
def _(S):
    body = "M8.5 8.5C5.5 11 4.5 15 5 18.5C5.3 20 6.5 21 8.5 21H15.5C17.5 21 18.7 20 19 18.5C19.5 15 18.5 11 15.5 8.5Z"
    tuft = poly([(9.3, 8.6), (8, 3.5), (16, 3.5), (14.7, 8.6)], closed=True)
    return [shell(union(body, tuft)), detail(seg(8.6, 8.3, 15.4, 8.3)), detail(rect(9, 13, 6, 4.5, 1))]


@icon("core-sample", CAT, "Drilled cylinder of rock showing bands of layers, lying at an angle",
      tags=["core sample", "drill core", "borehole", "rock core", "geology", "sediment", "drilling"])
def _(S):
    cyl = bez([("M", (-8, -4)), ("L", (6, -4)), ("C", (7.1, -4), (8, -2.2), (8, 0)), ("C", (8, 2.2), (7.1, 4), (6, 4)),
               ("L", (-8, 4)), ("Z",)], -40, 12, 12)
    cap = bez([("M", (6, -4)), ("C", (5.2, -4), (4.5, -2.2), (4.5, 0)), ("C", (4.5, 2.2), (5.2, 4), (6, 4))], -40, 12, 12)
    b1 = bez([("M", (-5, -4)), ("C", (-3.8, -1.5), (-3.8, 1.5), (-5, 4))], -40, 12, 12)
    b2 = bez([("M", (-1, -4)), ("C", (0.2, -1.5), (0.2, 1.5), (-1, 4))], -40, 12, 12)
    return [shell(cyl), detail(cap), detail(b1), detail(b2)]


@icon("streak-plate", CAT, "White tile with a dark streak of powder and a small mineral chip beside it",
      tags=["streak plate", "mineral test", "streak test", "geology", "mineral", "identification", "powder"])
def _(S):
    tile = rect(2.5, 6, 19, 12, min(S.R, 3))
    return [shell(tile), Part("dot", poly([(5, 12), (9, 10.8), (13.5, 11.4), (14, 13.6), (9.5, 14), (5.5, 14.4)], closed=True)),
            Part("dot", poly([(17, 10.2), (19.5, 11.6), (18.8, 14), (16.2, 13.6)], closed=True))]


@icon("mohs-scale", CAT, "Rising steps of increasing height with a cut gem on the highest step",
      tags=["mohs scale", "hardness", "mineral hardness", "scratch test", "gem", "geology", "diamond"])
def _(S):
    steps = poly([(2.5, 21.5), (2.5, 18), (7.25, 18), (7.25, 15.5), (12, 15.5), (12, 13), (16.75, 13), (16.75, 10.5),
                  (21.5, 10.5), (21.5, 21.5)], closed=True, r=S.r)
    return [shell(steps), solid(poly([(17, 5), (18.6, 3), (20.6, 3), (22.2, 5), (19.6, 8)], closed=True))]


@icon("mineral-vein", CAT, "Slab of rock crossed by a bright branching vein of mineral",
      tags=["mineral vein", "vein", "quartz", "ore", "lode", "geology", "rock"])
def _(S):
    slab = poly([(2.5, 8), (6, 4), (13, 5), (18, 3.5), (21.5, 9), (20.5, 16), (16, 20.5), (7, 19.5), (3, 14.5)], closed=True, r=S.r)
    vein = path_to_d(ST("M2.6 12L8 11L10.5 14L15.5 9L21.3 9.5M10.5 14L11.6 19.3", 2.4, "butt", "miter", 4))
    return [shell(slab), Part("dot", vein)]


@icon("ore-rock", CAT, "Lumpy rock with shiny metallic flecks embedded in it",
      tags=["ore", "ore rock", "mineral", "metal ore", "mining", "rock", "shiny"])
def _(S):
    rock = poly([(3, 16.5), (3.5, 10), (7, 8.5), (9, 4.5), (13, 6), (16, 3.5), (20, 8), (21.5, 14), (18, 19.5), (9, 20.5)],
                closed=True, r=L(S, 0, 2))
    return [shell(rock), Part("dot", diamond(9, 13, 1.7)), Part("dot", diamond(15.5, 9.5, 1.6)), Part("dot", diamond(14.5, 15.5, 1.7))]


@icon("gold-nugget", CAT, "Irregular lumpy nugget of gold with a shine mark and a sparkle",
      tags=["gold", "gold nugget", "nugget", "precious metal", "prospecting", "treasure", "mining"])
def _(S):
    lump = poly([(4, 16), (7, 10.5), (12, 8.5), (16, 7), (20, 10.5), (21.5, 16), (17, 20), (8, 20.5)], closed=True, r=L(S, 1.2, 4))
    return [shell(lump), detail("M10 12.5C11 11.2 12.3 10.8 13.5 11"),
            solid("M5.5 2L6.5 4.2L8.7 5.2L6.5 6.2L5.5 8.4L4.5 6.2L2.3 5.2L4.5 4.2Z")]


@icon("gold-panning", CAT, "Shallow round pan with water, gravel and a few flecks of gold",
      tags=["gold panning", "prospecting", "pan", "placer", "gold rush", "sifting", "mining"])
def _(S):
    if S.name == "line":
        bowl = union(ellipse(12, 10.5, 9.5, 3.8), "M2.5 10.5L6.5 18.5H17.5L21.5 10.5Z")
    else:
        bowl = union(ellipse(12, 10.5, 9.5, 3.8), "M2.5 10.5C3 16 7 19 12 19C17 19 21 16 21.5 10.5Z")
    return [shell(bowl), detail("M2.5 10.5A9.5 3.8 0 0 0 21.5 10.5"), dot(8.5, 10, 1), dot(12.5, 8.8, 1), dot(15.5, 10.3, 1)]


@icon("mine-cart", CAT, "Mining cart on a rail, heaped with lumps of ore",
      tags=["mine cart", "minecart", "ore cart", "mining", "rail", "tram", "coal"])
def _(S):
    bucket = poly([(2.5, 7.5), (21.5, 7.5), (19, 14), (5, 14)], closed=True, r=L(S, 0, 1.2))
    heap = union(bucket, circle(7.5, 5.5, 2.8), circle(12, 4.6, 3), circle(16.5, 5.5, 2.8))
    return [shell(heap), dot(8, 18.3, 2), dot(16, 18.3, 2), line(seg(2.5, 21, 21.5, 21))]


@icon("mine-entrance", CAT, "Timber-framed tunnel opening in a hillside with rails running into it",
      tags=["mine entrance", "mine", "tunnel", "adit", "mining", "hillside", "rails"])
def _(S):
    hill = "M2.5 21.5V14C2.5 8.5 7 5 12 5C17 5 21.5 8.5 21.5 14V21.5Z"
    door = poly([(7, 10.5), (17, 10.5), (17, 22.5), (7, 22.5)], closed=True)
    return [shell(minus(hill, door)), line(seg(10, 21.5, 11, 14.5)), line(seg(14, 21.5, 13, 14.5)),
            line(seg(9, 19.6, 15, 19.6)), line(seg(10.2, 16.6, 13.8, 16.6))]