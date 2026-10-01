"""TypeIcon Core: utilities (batch 002)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "utilities"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def kn(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def sq(x, y, w, h, S):
    return Part("dot", rect(x, y, w, h, L(S, 0, 0.5)))


def hole(S, x, y, r=1.1):
    return dot(x, y, r) if S.name == "rounded" else Part("dot", rect(x - r, y - r, 2 * r, 2 * r))


# ============================================================================ chunk 1

@icon("manhole-cover-lifter", CAT, "Round manhole cover with a long hooked lifting key and a T-handle.",
      tags=["manhole key", "cover lifter", "sewer", "drain cover", "utility access", "lifting key"])
def _(S):
    return [
        shell(ellipse(9, 17, 7.5, 3.5)),
        hole(S, 7, 17, 1),
        line("M20 4L11 15"),
        line("M17.5 2.5L22.5 6.5"),
        line("M11 15L8.5 14"),
    ]


@icon("ground-penetrating-radar", CAT, "Small wheeled radar cart on a handle with signal waves going down to a buried pipe.",
      tags=["gpr", "ground radar", "subsurface scan", "buried pipe", "utility locating", "survey"])
def _(S):
    return [
        shell(rect(3, 6, 9, 5, L(S, 1, 2))),
        line("M12 8L20 3"),
        dot(5.5, 13.5, 1.5),
        dot(10.5, 13.5, 1.5),
        line("M2 16H22"),
        line(arc(7.5, 16, 3.5, 50, 130)),
        line(arc(7.5, 16, 6.5, 55, 125)),
        dot(17.5, 20, 1.6),
    ]


@icon("gas-compressor-station", CAT, "Small building with two roof vent stacks and a pipe with a valve running out of its side.",
      tags=["compressor", "gas pipeline", "pumping station", "natural gas", "plant", "valve"])
def _(S):
    return [
        shell(rect(2, 11, 13, 10, L(S, 1, 2))),
        line("M6 11V5"),
        line("M11 11V5"),
        line("M15 17H22"),
        line("M19 17V13"),
        line("M17 13H21"),
        kn(rect(6, 15, 4, 6, 0)),
    ]


@icon("pipeline-marker-post", CAT, "Upright post with a slanted cap and a flame mark on its face, flagging a buried pipeline.",
      tags=["pipeline marker", "buried gas line", "warning post", "utility marker", "gas main", "dig safe"])
def _(S):
    flame = "M12 19C10.2 18.5 9.6 16.5 10.6 15C11.2 14.2 11.5 13.4 11.8 12.4C13 13.3 14.3 14.8 14.2 16.7C14.1 18 13.2 19 12 19Z"
    return [
        shell(poly([(7.5, 6), (16.5, 3), (16.5, 21), (7.5, 21)], closed=True, r=S.r * 0.6)),
        kn(flame),
    ]


@icon("gas-cylinder-cage", CAT, "Mesh storage cage with a latch holding two upright gas cylinders.",
      tags=["cylinder storage", "gas bottles", "lpg cage", "propane exchange", "compressed gas", "secure storage"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, L(S, 1, 2))),
        detail("M7 18V10.5A1.75 1.75 0 0 1 10.5 10.5V18"),
        detail("M13.5 18V10.5A1.75 1.75 0 0 1 17 10.5V18"),
        detail("M7.5 7H9.5"),
    ]


@icon("lpg-bulk-tank", CAT, "Long horizontal capsule tank on two saddle feet with a domed valve cover on top.",
      tags=["propane tank", "lpg storage", "bulk gas", "fuel tank", "gas storage", "pressure vessel"])
def _(S):
    return [
        shell(rect(2, 8, 20, 9, L(S, 3.5, 4.5))),
        shell(rect(10, 4.5, 4, 3.5, L(S, 0.5, 1.5))),
        line("M7 17V20.5"),
        line("M17 17V20.5"),
        line("M4.5 21H9.5"),
        line("M14.5 21H19.5"),
    ]


@icon("coal-scuttle", CAT, "Tall metal bucket with a sloping open lip and a carry handle, lumps of coal showing above the rim.",
      tags=["coal bucket", "fireplace", "fuel", "hod", "solid fuel", "coal"])
def _(S):
    return [
        line("M6 12C6 2.5 18 2.5 18 10"),
        shell(poly([(3, 13), (19, 10), (17, 21), (7, 21)], closed=True, r=S.r * 0.6)),
        solid(poly([(8, 11.5), (9.5, 8), (12.5, 7.5), (13.5, 11), (9, 12)], closed=True)),
        solid(poly([(13, 11), (14.5, 8.5), (17, 9), (17, 10.5)], closed=True)),
    ]


@icon("charcoal-kiln", CAT, "Earth-covered dome mound with a small door and smoke curling from a vent on top.",
      tags=["charcoal burning", "earth kiln", "clamp kiln", "wood fuel", "smoke", "carbonizing"])
def _(S):
    door = "M10 20V17.5H14V20" if S.name == "line" else "M10 20V18A2 2 0 0 1 14 18V20"
    return [
        shell("M3 20A9 9 0 0 1 21 20Z"),
        line("M12 11V9"),
        line("M12 8C9.5 6.5 14.5 4.5 12 2.5"),
        detail(door),
    ]


@icon("fuel-briquettes", CAT, "Small stack of pillow-shaped briquettes, two below and one on top.",
      tags=["briquette", "charcoal", "solid fuel", "biomass", "barbecue", "heating"])
def _(S):
    return [
        shell(rect(8, 3, 8, 6, L(S, 2, 3))),
        shell(rect(2, 13, 8, 8, L(S, 2, 3.5))),
        shell(rect(14, 13, 8, 8, L(S, 2, 3.5))),
    ]


@icon("wood-chips", CAT, "Mound of angular wood chips with a few loose chips on either side.",
      tags=["woodchip", "mulch", "biomass", "bark", "wood fuel", "chipped wood"])
def _(S):
    return [
        shell(poly([(5, 20), (8.5, 12), (12, 8.5), (15.5, 12), (19, 20)], closed=True, r=S.r)),
        detail("M9 17L12 14.5L14.5 17"),
        solid(poly([(1.5, 19), (3.5, 17), (5.5, 18.5), (3.5, 20.5)], closed=True)),
        solid(poly([(18.5, 17), (21, 15.5), (22.5, 18), (20, 19)], closed=True)),
    ]


@icon("open-pit-mine", CAT, "Terraced open pit in cross section with stepped benches and a dump truck on the pit floor.",
      tags=["quarry", "surface mining", "mine pit", "excavation", "terraced pit", "mining"])
def _(S):
    return [
        shell(poly([(2, 4), (6, 4), (8, 8), (10, 8), (12, 12), (14, 12), (15.5, 16), (22, 16), (22, 21), (2, 21)],
                   closed=True, r=S.r * 0.5)),
        solid(poly([(16.5, 14), (16.5, 11), (19.5, 11), (19.5, 9.5), (21.5, 9.5), (21.5, 14)], closed=True)),
    ]


@icon("landfill-compactor", CAT, "Heavy compactor with a front blade and a large spiked steel wheel.",
      tags=["trash compactor", "garbage compactor", "landfill", "dump site", "waste vehicle", "heavy machinery"])
def _(S):
    cx, cy = 13, 16
    spikes = [line(f"M{fmt(polar(cx, cy, 4.7, a)[0])} {fmt(polar(cx, cy, 4.7, a)[1])}L{fmt(polar(cx, cy, 6.3, a)[0])} {fmt(polar(cx, cy, 6.3, a)[1])}")
              for a in range(0, 360, 45)]
    return [
        shell(rect(8, 3, 13, 6, L(S, 1, 2.5))),
        shell(circle(cx, cy, 3.25)),
        line("M4 4V13"),
        line("M4 8H8"),
    ] + spikes


@icon("compost-windrow", CAT, "Long rounded ridge of compost with steam wisps rising from the top.",
      tags=["compost heap", "composting", "organic waste", "windrow", "soil", "steam"])
def _(S):
    return [
        shell("M2 20C4 12 8 10 12 10C16 10 20 12 22 20Z"),
        line("M8 7C6.5 5.5 9.5 4.5 8 3"),
        line("M12 7C10.5 5.5 13.5 4.5 12 3"),
        line("M16 7C14.5 5.5 17.5 4.5 16 3"),
    ]


@icon("scrapyard", CAT, "Crane arm lowering a magnet over a crushed car and scrap pile.",
      tags=["junkyard", "scrap metal", "salvage yard", "car crusher", "metal recycling", "magnet crane"])
def _(S):
    return [
        line("M3 3H17"),
        line("M12 3V8"),
        shell(rect(9.5, 8, 5, 2.5, L(S, 0.5, 1.2))),
        shell(poly([(2, 21), (2, 17), (7, 15), (14, 15), (16, 17.5), (22, 18), (22, 21)], closed=True, r=S.r * 0.6)),
        detail("M7 18H13"),
    ]


@icon("illegal-dumping", CAT, "Heap of rubbish bags dumped beside a no dumping sign on a post.",
      tags=["fly tipping", "littering", "waste dumping", "rubbish dump", "dumped trash", "no dumping"])
def _(S):
    return [
        shell(circle(18, 7, 4)),
        detail("M15.2 9.8L20.8 4.2"),
        line("M18 11V21"),
        shell("M2 21C2 16.5 3.5 14 7 14C10.5 14 12 16.5 12 21Z"),
        line("M5.5 14L4 11"),
        line("M8.5 14L10 11"),
    ]


# ============================================================================ chunk 2

@icon("bulky-waste", CAT, "Old sofa on short legs with a rolled mattress standing beside it, waiting for bulky item collection.",
      tags=["bulky item collection", "furniture disposal", "sofa", "old couch", "mattress", "large waste"])
def _(S):
    return [
        line("M4 11V9A2 2 0 0 1 6 7H12A2 2 0 0 1 14 9V11"),
        shell(rect(2, 11, 14, 6, L(S, 1.5, 2.5))),
        line("M4 17V20"),
        line("M14 17V20"),
        shell(rect(18, 5, 4, 15, L(S, 1.5, 2))),
        detail("M18 9H22"),
    ]


@icon("bin-collection-day", CAT, "Calendar page with a wheeled trash bin drawn on it.",
      tags=["trash day", "bin day", "garbage schedule", "waste pickup", "collection calendar", "rubbish collection"])
def _(S):
    return [
        shell(rect(3, 4, 18, 17, L(S, 2, 3))),
        line("M8 2V6"),
        line("M16 2V6"),
        detail("M3 9H21"),
        detail("M8.5 12.5H15.5"),
        detail("M9.5 12.5L10.5 18.5H13.5L14.5 12.5"),
    ]


@icon("underground-bin", CAT, "Ground cross section with a short chute post above ground and a large container buried below.",
      tags=["buried bin", "semi underground container", "waste container", "street bin", "recycling point", "chute"])
def _(S):
    return [
        shell(rect(9, 3, 6, 6, L(S, 1, 2))),
        kn(rect(10.5, 4.5, 3, 1.5, 0)),
        line("M2 9H22"),
        shell(rect(4, 13, 16, 8, L(S, 1.5, 3))),
        detail("M12 13V21"),
    ]


@icon("bin-shelter", CAT, "Small roofed enclosure sheltering two wheeled bins.",
      tags=["bin store", "bin enclosure", "waste shelter", "trash enclosure", "wheelie bin", "refuse store"])
def _(S):
    return [
        shell(poly([(2, 10), (5, 4), (19, 4), (22, 10)], closed=True, r=S.r * 0.6)),
        shell(rect(4.5, 13, 6, 8, L(S, 1, 1.5))),
        shell(rect(13.5, 13, 6, 8, L(S, 1, 1.5))),
    ]


@icon("recycling-station", CAT, "Row of three bins with different lids, marked with a bottle, a sheet of paper and a can.",
      tags=["recycling point", "sorting bins", "bottle bank", "waste sorting", "separate collection", "recycling centre"])
def _(S):
    return [
        shell(rect(2, 4, 20, 17, L(S, 2, 3))),
        detail("M8.67 4V21"),
        detail("M15.33 4V21"),
        detail("M2 9H22"),
        kn(rect(4.6, 12.5, 1.6, 6.5, 0.6)),
        kn(rect(4.9, 11.5, 1, 1.5, 0)),
        kn(rect(10.7, 12, 2.6, 6.5, 0)),
        kn(circle(18.7, 15.5, 1.7)),
    ]


@icon("curbside-recycling-box", CAT, "Open-topped box with a bottle and a folded newspaper sticking out.",
      tags=["recycling crate", "kerbside box", "blue box", "bottle bank", "paper recycling", "household recycling"])
def _(S):
    return [
        line("M8.5 10V7.5L10 5.5V3H13V5.5L14.5 7.5V10"),
        line("M17.5 10V4.5H20.5V10"),
        shell(poly([(3, 10), (21, 10), (19, 21), (5, 21)], closed=True, r=S.r * 0.6)),
        detail("M9 14H15"),
    ]


@icon("dog-waste-bin", CAT, "Small bin on a post with a paw print on its front.",
      tags=["pet waste bin", "poop bin", "dog litter bin", "paw print", "park bin", "dog park"])
def _(S):
    return [
        shell(rect(5, 3, 14, 11, L(S, 2, 4))),
        kn(circle(12, 11, 1.8)),
        kn(circle(9, 8.2, 1)),
        kn(circle(12, 6.8, 1)),
        kn(circle(15, 8.2, 1)),
        line("M12 14V21"),
        line("M8 21H16"),
    ]


@icon("wall-ashtray", CAT, "Slim wall-mounted canister with a vented top and a cigarette resting on it.",
      tags=["cigarette bin", "smoking area", "butt bin", "cigarette disposal", "ash bin", "stub out"])
def _(S):
    return [
        line("M3 4V21"),
        line("M3 12H7"),
        shell(rect(7, 10, 6, 11, L(S, 1.5, 3))),
        detail("M7 14H13"),
        line("M8 7H20"),
        line("M17 5V9"),
    ]


@icon("trash-chute", CAT, "Wall panel with a hatch pulled open to show a chute opening and a handle.",
      tags=["garbage chute", "rubbish chute", "waste hatch", "apartment trash", "refuse chute", "building waste"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, L(S, 2, 4))),
        detail("M7 7H17"),
        detail("M7 7L8.5 15H15.5L17 7"),
        kn(rect(10, 16.5, 4, 1.5, 0.4 if S.name == "rounded" else 0)),
    ]


@icon("river-trash-boom", CAT, "Curved floating boom across a river holding back a cluster of bottles and bags.",
      tags=["litter boom", "river cleanup", "floating barrier", "plastic catcher", "waterway litter", "debris barrier"])
def _(S):
    return [
        line("M2 13C7 18.5 17 18.5 22 13"),
        solid(circle(8.5, 9.5, 2.2)),
        solid(rect(11.2, 6.5, 2.6, 6, 1.2)),
        solid(circle(16.5, 9.8, 2.2)),
        line("M3 21C5 19.7 6.5 22.3 8.5 21C10.5 19.7 12 22.3 14 21C16 19.7 17.5 22.3 19.5 21"),
    ]


@icon("garden-waste-bag", CAT, "Large fabric sack with two side handles and leaves spilling from the open top.",
      tags=["yard waste bag", "leaf bag", "green waste", "garden refuse", "grass clippings", "compostable bag"])
def _(S):
    return [
        shell("M6 9C4 13 4 18 6 21H18C20 18 20 13 18 9Z"),
        line("M5 12C2 12 2 16 5 16"),
        line("M19 12C22 12 22 16 19 16"),
        shell("M9 9C6 8 4.5 5.5 5 3C8 3.5 10 6 9 9Z"),
        shell("M15 9C15.5 6 18 4.5 20.5 5C20 8 18 9.5 15 9Z"),
        line("M12 9V4"),
    ]


@icon("recycling-bale", CAT, "Compressed cube of crushed cans held tight by two straps.",
      tags=["baled cans", "compressed metal", "scrap bale", "aluminium cans", "bailing", "recycled material"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, L(S, 1.5, 3.5))),
        detail("M9 3V21"),
        detail("M15 3V21"),
        kn(circle(6, 9, 0.9)),
        kn(circle(6, 15, 0.9)),
        kn(circle(12, 12, 0.9)),
        kn(circle(18, 9, 0.9)),
        kn(circle(18, 15, 0.9)),
    ]


@icon("waste-hierarchy", CAT, "Inverted triangle split into horizontal bands, widest at the top.",
      tags=["reduce reuse recycle", "waste pyramid", "circular economy", "prevention", "waste management", "priorities"])
def _(S):
    return [
        shell(poly([(2, 4), (22, 4), (12, 21)], closed=True, r=S.r * 0.6)),
        detail("M4.94 9H19.06"),
        detail("M7.88 14H16.12"),
    ]


@icon("overflowing-trash-can", CAT, "Trash can stuffed so full that bags bulge above the rim and litter spills around it.",
      tags=["full bin", "overflowing bin", "litter", "rubbish", "waste overflow", "full trash"])
def _(S):
    return [
        line("M8 10C7 6.5 9 4.5 12 4.5C15 4.5 17 6.5 16 10"),
        shell(poly([(5.5, 10), (18.5, 10), (17, 21), (7, 21)], closed=True, r=S.r * 0.6)),
        solid(poly([(1.5, 19), (4, 18.2), (4.5, 20.5), (2, 21)], closed=True)),
        solid(poly([(19.5, 16.5), (22.5, 17.5), (21, 19.5)], closed=True)),
    ]


@icon("street-cleaner-cart", CAT, "Two-wheeled push cart with a tall bin, a broom clipped to its side and a handle bar.",
      tags=["street sweeper cart", "cleaner trolley", "sanitation worker", "litter picker cart", "janitor cart", "sweeping"])
def _(S):
    return [
        shell(poly([(5, 3), (15, 3), (14, 14), (6, 14)], closed=True, r=S.r * 0.6)),
        shell(circle(10, 18.5, 2.5)),
        line("M5 6L2 3"),
        line("M18 3L20 15"),
        shell(poly([(18.5, 15), (22, 15), (22, 21), (18, 21)], closed=True, r=S.r * 0.4)),
    ]


# ============================================================================ chunk 3

@icon("disguised-cell-tower", CAT, "Cell tower made to look like a pine tree, with antenna panels hidden among the branches and signal arcs beside it.",
      tags=["fake tree tower", "stealth tower", "camouflaged mast", "monopine", "mobile mast", "cell site"])
def _(S):
    return [
        shell(poly([(11, 2.5), (15, 8), (13, 8), (17.5, 14), (13, 14), (13, 21), (9, 21), (9, 14), (4.5, 14), (9, 8), (7, 8)],
                   closed=True, r=S.r * 0.5)),
        kn(rect(10, 9.5, 2, 3, 0)),
        line("M18.5 4.5C20 5.5 20 7.5 18.5 8.5"),
        line("M20.5 3C22.2 5 22.2 8 20.5 10"),
    ]


@icon("mobile-cell-tower", CAT, "Wheeled trailer carrying a tall telescopic mast topped with antenna panels.",
      tags=["cell on wheels", "temporary mast", "cow tower", "portable tower", "emergency network", "trailer mast"])
def _(S):
    return [
        line("M12 15V6"),
        solid(rect(8, 2.5, 2, 5, 0)),
        solid(rect(14, 2.5, 2, 5, 0)),
        line("M10 5H14"),
        shell(rect(2, 15, 17, 3, L(S, 0.5, 1.4))),
        line("M19 16.5H22"),
        dot(7.5, 20, 1.6),
        dot(13.5, 20, 1.6),
    ]


@icon("telecom-street-cabinet", CAT, "Tall pavement cabinet with double doors, vent slots on one and a signal symbol on the other.",
      tags=["fibre cabinet", "broadband cabinet", "green box", "cross connect", "network node", "roadside cabinet"])
def _(S):
    return [
        shell(rect(5, 2, 14, 19, L(S, 1.5, 3))),
        detail("M12 2V21"),
        detail("M7.5 14H10"),
        detail("M7.5 17H10"),
        dot(14.5, 11, 0.9),
        detail("M16.5 8A3 3 0 0 1 16.5 12"),
    ]


@icon("street-light", CAT, "Tall pole with a curved arm ending in a flat lamp head that casts a cone of light.",
      tags=["lamp post", "street lamp", "road lighting", "lamppost", "outdoor lighting", "pole light"])
def _(S):
    return [
        line("M7 21V8C7 4.5 9.5 3.5 13 3.5"),
        shell(rect(13, 3, 8, 2.5, L(S, 0.5, 1.2))),
        line("M14.5 8L12.5 13.5"),
        line("M19.5 8L21.5 13.5"),
        line("M17 8V14"),
        line("M4 21H10"),
    ]


@icon("suspended-street-lamp", CAT, "Lamp hanging from a wire strung across a street between two poles, light shining down.",
      tags=["catenary lamp", "wire hung light", "overhead street lamp", "hanging light", "span wire", "old town lighting"])
def _(S):
    return [
        line("M3 3V21"),
        line("M21 3V21"),
        line("M3 4.5C8 9 16 9 21 4.5"),
        line("M12 7.5V9.5"),
        shell(poly([(9, 15), (15, 15), (13.5, 9.5), (10.5, 9.5)], closed=True, r=S.r * 0.5)),
        line("M9 18L8 20.5"),
        line("M12 17.5V20.5"),
        line("M15 18L16 20.5"),
    ]


@icon("street-steam-vent", CAT, "Tall striped tube standing in the road with a plume of steam rising from its top.",
      tags=["steam stack", "city steam", "manhole steam", "traffic cone steam", "underground steam", "vent pipe"])
def _(S):
    return [
        shell(poly([(9, 10), (15, 10), (16, 20), (8, 20)], closed=True, r=S.r * 0.4)),
        detail("M8.8 13.5H15.2"),
        detail("M8.4 17H15.6"),
        line("M5 21H19"),
        line("M10 7.5C8 5.5 11 4.5 10 2"),
        line("M14 7.5C12 5.5 15 4.5 14 2"),
    ]


@icon("utility-marking-flags", CAT, "Three small flags on thin stems stuck in the ground beside a dashed painted line.",
      tags=["locate flags", "dig safe flags", "survey flags", "buried utility markers", "ground paint", "call before you dig"])
def _(S):
    return [
        line("M5 3V18"),
        line("M11 3V18"),
        line("M17 3V18"),
        solid(poly([(5, 3), (10, 5.5), (5, 8)], closed=True)),
        solid(poly([(11, 3), (16, 5.5), (11, 8)], closed=True)),
        solid(poly([(17, 3), (22, 5.5), (17, 8)], closed=True)),
        line("M2 21H5M8 21H11M14 21H17M20 21H22"),
    ]


@icon("cable-locator", CAT, "Handheld locator wand with a display on top sweeping the ground, signal waves going below the surface.",
      tags=["cable detector", "pipe locator", "utility scanner", "buried cable finder", "underground detection", "wand"])
def _(S):
    return [
        shell(rect(8, 2, 8, 5, L(S, 1, 2))),
        line("M12 7V12"),
        shell(rect(8.5, 12, 7, 2.5, L(S, 0.5, 1.2))),
        line("M2 17H22"),
        line(arc(12, 17, 2.5, 40, 140)),
        line(arc(12, 17, 5, 45, 135)),
    ]


@icon("directional-drilling", CAT, "Drill rig on the surface boring a curved path under the ground to exit on the other side.",
      tags=["horizontal drilling", "trenchless", "hdd", "boring rig", "pipe under road", "underground drilling"])
def _(S):
    return [
        line("M2 9H22"),
        shell(rect(2.5, 3.5, 5, 5, L(S, 0.5, 1.5))),
        line("M7.5 5L10.5 9"),
        line("M5 9C6 21 18 21 19 9"),
        line("M16.7 11.5L19 9L21.7 11"),
    ]


@icon("solar-panel-cleaning", CAT, "Tilted solar panel with a roller brush bar sweeping across its surface and drops of water below.",
      tags=["pv cleaning", "panel washing", "solar maintenance", "dust removal", "brush robot", "photovoltaic"])
def _(S):
    return [
        shell(poly([(5, 17.5), (8, 3.5), (20, 3.5), (17, 17.5)], closed=True, r=S.r * 0.5)),
        detail("M14 3.5L11 17.5"),
        shell(rect(3, 9, 18, 3.5, 1.75)),
        dot(8, 20.8, 0.9),
        dot(12.5, 20.8, 0.9),
        dot(17, 20.8, 0.9),
    ]


@icon("service-drop", CAT, "Utility pole with a single wire sagging across to a house wall that carries a small meter box.",
      tags=["service line", "overhead service", "power drop", "house connection", "electric meter", "utility wire"])
def _(S):
    return [
        line("M4 2V21"),
        line("M2 5H7"),
        line("M5 5C9 12 12 11 15 8"),
        shell(rect(15, 8, 7, 13, L(S, 0.5, 1.5))),
        kn(rect(17.5, 12.5, 2, 3.5, 0)),
    ]


@icon("bottle-filling-station", CAT, "Wall unit with a spout and display, and a water bottle being filled beneath it.",
      tags=["water refill", "drinking fountain", "refill station", "water dispenser", "reusable bottle", "hydration"])
def _(S):
    return [
        shell(rect(3, 2, 18, 10, L(S, 1.5, 3))),
        kn(rect(14.5, 4.5, 4, 3, 0)),
        line("M9 12V15.5"),
        shell(poly([(6, 21), (6, 18.5), (8, 16.5), (10, 16.5), (12, 18.5), (12, 21)], closed=True, r=S.r * 0.5)),
        kn(rect(5.5, 4.5, 5, 3, 0)),
    ]


@icon("water-cart", CAT, "Two-wheeled hand cart carrying a horizontal water barrel with a tap at the back.",
      tags=["water barrel cart", "water carrier", "drum cart", "water hauling", "village water", "tap barrel"])
def _(S):
    return [
        shell(rect(4, 4, 13, 8, L(S, 3, 4))),
        detail("M8.5 4V12"),
        detail("M12.5 4V12"),
        shell(circle(10.5, 17, 3.5)),
        dot(10.5, 17, 1),
        line("M17 9H20V12"),
        line("M4.5 10L2.5 17"),
        dot(20, 16, 1),
    ]


@icon("trench-drain", CAT, "Long narrow channel set in paving covered by a slotted grate, with water drops falling into it.",
      tags=["channel drain", "grate drain", "linear drain", "surface water", "drainage grate", "runoff"])
def _(S):
    return [
        shell(rect(2, 10, 20, 6, L(S, 1, 2.5))),
        detail("M6.5 10V16"),
        detail("M11 10V16"),
        detail("M15.5 10V16"),
        dot(7, 4, 1),
        dot(12, 6, 1),
        dot(17, 4, 1),
        line("M2 20H22"),
    ]


@icon("drug-take-back-box", CAT, "Mailbox-style drop box with a slot and a pill capsule on its front for returning unused medicine.",
      tags=["medicine disposal", "pharmacy drop box", "unused medication", "prescription take back", "drug disposal", "safe disposal"])
def _(S):
    from dsl import ST as _ST
    from geometry import path_to_d
    cap = path_to_d(_ST(seg(9.5, 17.5, 14.5, 12.5), 3.4, "round", "round"))
    return [
        shell(rect(4, 3, 16, 18, L(S, 1.5, 3))),
        detail("M8 7H16"),
        kn(cap),
    ]


# ============================================================================ chunk 4

@icon("parabolic-solar-cooker", CAT, "Open parabolic reflector bowl on a stand with a cooking pot held at its centre and sun rays coming down.",
      tags=["solar cooker", "sun oven", "solar cooking", "reflector dish", "off grid cooking", "concentrated sunlight"])
def _(S):
    return [
        line("M2.5 9C3.5 16 7.5 19 12 19C16.5 19 20.5 16 21.5 9"),
        shell(rect(9.5, 10, 5, 4, L(S, 0.5, 1.5))),
        line("M4.5 11L9.5 12"),
        line("M19.5 11L14.5 12"),
        line("M12 19V22"),
        line("M12 2V6.5"),
        line("M6 2.5L8.5 6.5"),
        line("M18 2.5L15.5 6.5"),
    ]


@icon("pipe-rack", CAT, "Steel frame with legs and a cross beam carrying parallel pipes along its top.",
      tags=["pipe bridge", "pipeway", "refinery pipes", "plant piping", "industrial pipes", "steel support"])
def _(S):
    return [
        line("M2 4H22"),
        line("M2 8H22"),
        line("M2 12H22"),
        line("M5 12V21"),
        line("M19 12V21"),
        line("M5 20L19 13"),
    ]


@icon("lead-pipe", CAT, "Straight pipe with flanged ends marked with the letters Pb.",
      tags=["lead plumbing", "lead service line", "old pipe", "toxic pipe", "pb", "water safety"])
def _(S):
    from dsl import ST as _ST
    from geometry import path_to_d

    def stroke(d, w=1.5):
        return path_to_d(_ST(d, w, "butt", "miter"))
    return [
        shell(rect(5, 6, 14, 12, L(S, 1, 2))),
        shell(rect(2, 4, 3, 16, L(S, 0.5, 1))),
        shell(rect(19, 4, 3, 16, L(S, 0.5, 1))),
        kn(stroke("M8.5 9V15M8.5 9H10.8V12.2H8.5")),
        kn(stroke("M13.5 9V15M13.5 15H15.6V11.8H13.5")),
    ]


@icon("radial-gate", CAT, "Curved gate face held by two arms pivoting on a dam pier, with water held back on its upstream side.",
      tags=["tainter gate", "spillway gate", "dam gate", "sluice", "water control", "dam crest"])
def _(S):
    return [
        line("M7 4C3 8 3 14 7 18"),
        line("M7 4L17 11"),
        line("M7 18L17 11"),
        shell(rect(17, 3, 5, 18, L(S, 0.5, 1.5))),
        line("M2 21H17"),
    ]


@icon("guy-wire-anchor", CAT, "Utility pole with a slanted guy wire running down to a ground anchor wrapped in a striped guard.",
      tags=["stay wire", "pole brace", "anchor guard", "guy guard", "utility pole support", "tension cable"])
def _(S):
    return [
        line("M6 2V21"),
        line("M6 5L18 13"),
        shell(rect(15, 13, 6, 8, L(S, 0.5, 1.5))),
        detail("M15 16.5H21"),
        line("M2 21H15"),
    ]


@icon("cable-laying-ship", CAT, "Ship with a large cable drum on deck and a cable trailing from its stern into the sea.",
      tags=["submarine cable ship", "subsea cable", "undersea cable", "cable layer", "fibre optic cable", "offshore vessel"])
def _(S):
    return [
        shell(poly([(2, 12), (18, 12), (15.5, 17), (5, 17)], closed=True, r=S.r * 0.5)),
        shell(rect(2.5, 7, 3.5, 5, 0)),
        shell(rect(9, 5.5, 6, 6.5, L(S, 1, 2))),
        line("M13 8C20 8 21 12 21 20"),
        line("M2 20.5C4 19.5 5.5 21.5 7.5 20.5C9.5 19.5 11 21.5 13 20.5C15 19.5 16 21 18 20.5"),
    ]


@icon("algae-bioreactor", CAT, "Rack of clear horizontal tubes joined end to end in a zigzag.",
      tags=["photobioreactor", "algae farm", "algae tubes", "microalgae", "biofuel", "algae culture"])
def _(S):
    return [
        shell(rect(5, 3, 14, 4, L(S, 1.5, 2))),
        shell(rect(5, 10, 14, 4, L(S, 1.5, 2))),
        shell(rect(5, 17, 14, 4, L(S, 1.5, 2))),
        line("M19 5H21V12H19"),
        line("M5 12H3V19H5"),
    ]


@icon("direct-air-capture", CAT, "Box-shaped unit with two round fans on its face and arrows flowing in from the left.",
      tags=["dac", "carbon capture", "co2 removal", "air scrubber", "carbon removal", "climate tech"])
def _(S):
    return [
        shell(rect(9, 3, 13, 18, L(S, 1.5, 3))),
        detail(circle(15.5, 8.5, 2.5)),
        detail(circle(15.5, 15.5, 2.5)),
        line("M2 8.5H6"),
        line("M2 15.5H6"),
        solid(poly([(5, 6.5), (7.5, 8.5), (5, 10.5)], closed=True)),
        solid(poly([(5, 13.5), (7.5, 15.5), (5, 17.5)], closed=True)),
    ]


@icon("linear-fresnel-collector", CAT, "Rows of flat mirror strips on the ground reflecting sun rays up to a single raised receiver pipe.",
      tags=["fresnel reflector", "solar thermal", "concentrated solar", "mirror field", "receiver tube", "solar power plant"])
def _(S):
    return [
        shell(poly([(8.5, 2.5), (15.5, 2.5), (13.5, 7), (10.5, 7)], closed=True, r=S.r * 0.5)),
        line("M12 7V15"),
        solid(rect(2, 18.5, 5, 2.5, L(S, 0, 1.2))),
        solid(rect(9.5, 18.5, 5, 2.5, L(S, 0, 1.2))),
        solid(rect(17, 18.5, 5, 2.5, L(S, 0, 1.2))),
        line("M4.5 16L10.5 8.5"),
        line("M19.5 16L13.5 8.5"),
    ]


@icon("wind-blade-transport", CAT, "Low trailer truck carrying one very long curved turbine blade that extends past its rear.",
      tags=["turbine blade truck", "wind turbine delivery", "oversize load", "blade carrier", "wind farm logistics", "heavy haulage"])
def _(S):
    return [
        shell(poly([(2, 17), (2, 11), (5, 8), (8, 8), (8, 17)], closed=True, r=S.r * 0.5)),
        line("M8 17H19"),
        shell("M8 14.5C11 10.5 17 10.5 20.5 13C16.5 13 11 13.5 8 14.5Z"),
        dot(5, 20, 1.6),
        dot(13, 20, 1.6),
        dot(17, 20, 1.6),
    ]


@icon("sidewalk-grate", CAT, "Rectangular metal ventilation grate set in the pavement with warm air lines rising from it.",
      tags=["subway grate", "vent grate", "pavement grille", "metro vent", "street grating", "warm air vent"])
def _(S):
    return [
        shell(rect(3, 13, 18, 8, L(S, 1, 2.5))),
        detail("M7.5 13V21"),
        detail("M12 13V21"),
        detail("M16.5 13V21"),
        line("M7 10C5.5 8.5 8.5 7 7 5.5"),
        line("M12 10C10.5 8.5 13.5 7 12 5.5"),
        line("M17 10C15.5 8.5 18.5 7 17 5.5"),
    ]


# ============================================================================ chunk 5

@icon("off-peak-electricity", CAT, "Crescent moon beside a lightning bolt, standing for cheaper night-time power.",
      tags=["night tariff", "economy 7", "off peak rate", "cheap electricity", "time of use", "night power"])
def _(S):
    return [
        shell("M12 4A8 8 0 1 0 12 20A5.5 5.5 0 0 1 12 4Z"),
        shell(poly([(19, 4), (15.5, 11.5), (18.5, 11.5), (17, 19.5), (21.5, 10.5), (18.5, 10.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("green-electricity", CAT, "Electric plug with a leaf growing from its cord.",
      tags=["renewable power", "clean energy", "eco electricity", "green tariff", "sustainable power", "leaf plug"])
def _(S):
    return [
        line("M8.5 2.5V6"),
        line("M13.5 2.5V6"),
        shell(rect(6, 6, 10, 6, L(S, 1, 2.5))),
        line("M11 12V20.5"),
        shell("M11 20.5C11 16.5 14 14.5 20 14.5C20 18.5 16 20.5 11 20.5Z"),
    ]


@icon("treadle-pump", CAT, "Two foot pedals on a frame working a pair of pump cylinders, with water flowing from a spout.",
      tags=["foot pump", "irrigation pump", "manual pump", "step pump", "smallholder irrigation", "water lifting"])
def _(S):
    return [
        shell(rect(5, 3, 5, 9, L(S, 0.5, 1.5))),
        shell(rect(14, 3, 5, 9, L(S, 0.5, 1.5))),
        line("M7.5 12V17"),
        line("M16.5 12V14.5"),
        shell(rect(2.5, 17, 8, 3, L(S, 0.5, 1.4))),
        shell(rect(13.5, 14.5, 8, 3, L(S, 0.5, 1.4))),
        line("M19 6H21.5V9"),
    ]


@icon("stockbridge-damper", CAT, "Power line with a small dumbbell-shaped weight hanging below it on a short clamp.",
      tags=["vibration damper", "line damper", "conductor weight", "overhead line", "aeolian vibration", "transmission line"])
def _(S):
    return [
        line("M2 5H22"),
        line("M12 5V13"),
        line("M6.5 13H17.5"),
        shell(rect(2, 10, 4.5, 6, L(S, 1, 2))),
        shell(rect(17.5, 10, 4.5, 6, L(S, 1, 2))),
    ]


@icon("monopole-power-tower", CAT, "Tall tapered single steel pole with three short arms on each side holding hanging insulators.",
      tags=["steel pole", "transmission pole", "power pylon", "single pole tower", "electric pylon", "overhead line"])
def _(S):
    return [
        shell(poly([(10, 2.5), (14, 2.5), (15, 21), (9, 21)], closed=True, r=S.r * 0.5)),
        line("M3 5H21"),
        line("M5 11H19"),
        line("M7 17H17"),
        line("M3.5 5V7.5"),
        line("M20.5 5V7.5"),
        line("M5.5 11V13.5"),
        line("M18.5 11V13.5"),
        line("M7.5 17V19.5"),
        line("M16.5 17V19.5"),
    ]


@icon("buttress-dam", CAT, "Dam wall seen from downstream, held up by a row of triangular buttresses.",
      tags=["dam wall", "concrete dam", "support buttresses", "hydro dam", "reservoir wall", "downstream face"])
def _(S):
    return [
        shell(rect(2, 3, 20, 5.5, L(S, 1, 2))),
        shell(poly([(3, 21), (5.5, 10.5), (8, 21)], closed=True, r=S.r * 0.4)),
        shell(poly([(9.5, 21), (12, 10.5), (14.5, 21)], closed=True, r=S.r * 0.4)),
        shell(poly([(16, 21), (18.5, 10.5), (21, 21)], closed=True, r=S.r * 0.4)),
    ]


@icon("french-drain", CAT, "Ground cross section of a gravel-filled trench with a perforated pipe along its bottom.",
      tags=["land drain", "gravel drain", "perforated pipe", "yard drainage", "subsurface drain", "seepage"])
def _(S):
    return [
        shell(poly([(3, 4), (21, 4), (18, 21), (6, 21)], closed=True, r=S.r * 0.6)),
        detail(circle(12, 16, 2.6)),
        kn(circle(8.5, 8.5, 1)),
        kn(circle(12, 8, 1)),
        kn(circle(15.5, 8.5, 1)),
    ]


@icon("stormwater-pond", CAT, "Pond with sloped banks and a drain pipe from the street feeding runoff into it.",
      tags=["retention pond", "detention basin", "runoff pond", "flood control", "surface water", "drain outfall"])
def _(S):
    return [
        shell(rect(2, 3, 5, 3.5, L(S, 0.5, 1.2))),
        dot(9.5, 8, 1),
        line("M2 10H5L8.5 18H15.5L19 10H22"),
        line("M8 14C9.5 13 10.5 15 12 14S14.5 13 16 14"),
    ]


@icon("check-dam", CAT, "Low pile of stacked stones across a small channel with a little water trickling over the top.",
      tags=["stone dam", "gully dam", "erosion control", "rock check", "stream restoration", "water harvesting"])
def _(S):
    return [
        shell(rect(8, 9, 8, 5, L(S, 1.5, 2.5))),
        shell(rect(3, 16.5, 8, 4.5, L(S, 1.5, 2.2))),
        shell(rect(13, 16.5, 8, 4.5, L(S, 1.5, 2.2))),
        line("M2 6C3.5 4.5 5 7.5 6.5 6"),
        dot(19, 9, 1),
        dot(21, 12.5, 1),
    ]


@icon("tide-flap-gate", CAT, "Pipe outlet through a wall with a hinged flap hanging over its mouth, pushed open by outflowing water.",
      tags=["tidal flap", "non return valve", "flood gate", "sea wall outfall", "drain flap", "backflow preventer"])
def _(S):
    return [
        shell(rect(12, 2, 5, 6, L(S, 0.5, 1.2))),
        shell(rect(12, 16, 5, 5, L(S, 0.5, 1.2))),
        line("M2 8H12"),
        line("M2 16H12"),
        line("M4 12H9.5"),
        solid(poly([(9, 10), (11.5, 12), (9, 14)], closed=True)),
        line("M17 8L21 16"),
    ]


@icon("misting-pole", CAT, "Street pole with a ring of nozzles near the top spraying fine mist downward.",
      tags=["cooling mist", "mist fan", "outdoor cooling", "misting system", "heat relief", "spray pole"])
def _(S):
    return [
        shell(ellipse(12, 5, 6, 2)),
        line("M12 7V21"),
        line("M8 21H16"),
        line("M7 8.5L5.5 11"),
        line("M17 8.5L18.5 11"),
        dot(4.5, 14, 0.9),
        dot(7, 13.5, 0.9),
        dot(19.5, 14, 0.9),
        dot(17, 13.5, 0.9),
        dot(5.5, 18, 0.9),
        dot(18.5, 18, 0.9),
    ]
