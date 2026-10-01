"""TypeIcon Core: retail fixtures and store equipment (batch retail_002).

In-store displays, racks, kiosks, carts and retail operations drawn from the objects themselves.
"""
from geometry import circle_d
from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401

CAT = "retail"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def kn(d):
    """Small solid shape: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


# ============================================================================ displays and fixtures

@icon("pallet-display", CAT, "Wooden pallet on the floor with a pyramid of boxes stacked on it",
      tags=["pallet", "box stack", "bulk display", "warehouse club", "promo", "stacked boxes"])
def _(S):
    return [
        shell(rect(3, 11, 8, 7, L(S, 0, 1.5))),
        shell(rect(13, 11, 8, 7, L(S, 0, 1.5))),
        shell(rect(8, 3.5, 8, 7.5, L(S, 0, 1.5))),
        line("M2 18h20"),
        line("M5 18v3.5M12 18v3.5M19 18v3.5"),
    ]


@icon("aisle-marker-sign", CAT, "Number sign hanging from two ceiling wires over a store aisle",
      tags=["aisle", "aisle number", "hanging sign", "wayfinding", "store layout", "signage"])
def _(S):
    return [
        line("M12 2.5L6.5 6M12 2.5L17.5 6"),
        shell(rect(3, 5.5, 18, 15, S.R)),
        detail("M9.5 11a2.5 2.5 0 0 1 5 0c0 2.4-5 3.4-5 6.5h5"),
    ]


@icon("window-display", CAT, "Shop window with a dress on a stand behind the glass",
      tags=["shop window", "storefront", "display window", "merchandising", "boutique", "window shopping"])
def _(S):
    return [
        shell(rect(2, 3.5, 20, 17, S.R)),
        detail("M2 8h20"),
        kn(poly([(10, 10.5), (14, 10.5), (13.6, 13.5), (16.5, 18.5), (7.5, 18.5), (10.4, 13.5)], closed=True, r=S.r * 0.3)),
    ]


@icon("gondola-shelving", CAT, "Freestanding store shelf unit seen from the end with shelves on both sides of a centre panel",
      tags=["gondola", "shelf unit", "store shelf", "aisle shelving", "fixture", "supermarket", "shelves"])
def _(S):
    return [
        line("M12 2.5v15"),
        line("M3.5 6h6.5M14 6h6.5M3.5 10h6.5M14 10h6.5M3.5 14h6.5M14 14h6.5M3.5 18h6.5M14 18h6.5"),
        line("M3 21.5h18"),
    ]


@icon("slatwall-panel", CAT, "Wall panel with horizontal grooves and two hooks hanging in the slots",
      tags=["slatwall", "wall panel", "display hooks", "wall fixture", "merchandising", "retail wall"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail("M3 8h18"),
        detail("M3 13h18"),
        kn(rect(7, 15.5, 10, 2.5, L(S, 0, 1))),
    ]


@icon("peg-hook-display", CAT, "Pegboard side view with two hooks each holding a hanging blister pack",
      tags=["pegboard", "peg hook", "blister pack", "hanging display", "hardware aisle", "hang tab"])
def _(S):
    return [
        line("M4 3v18"),
        line("M4 6.5h9M4 14.5h9"),
        shell(rect(13, 6.5, 7, 5.5, L(S, 0, 1.5))),
        shell(rect(13, 14.5, 7, 5.5, L(S, 0, 1.5))),
        kn(circle_d(16.5, 9.2, 0.8)),
        kn(circle_d(16.5, 17.2, 0.8)),
    ]


@icon("hat-display-stand", CAT, "Tall pole stand with three caps at different heights",
      tags=["hat stand", "cap display", "headwear", "hat rack", "baseball cap", "fixture"])
def _(S):
    return [
        line("M12 2.5v19"),
        line("M8 21.5h8"),
        shell(poly([(3, 8.5), (3.5, 5), (7, 3.5), (10.5, 5), (11, 8.5)], closed=True, r=S.r * 1.5)),
        shell(poly([(13, 14), (13.5, 10.5), (17, 9), (20.5, 10.5), (21, 14)], closed=True, r=S.r * 1.5)),
        shell(poly([(3, 19.5), (3.5, 16), (7, 14.5), (10.5, 16), (11, 19.5)], closed=True, r=S.r * 1.5)),
    ]


@icon("eyewear-display-tower", CAT, "Narrow display tower with three pairs of sunglasses on its ledges",
      tags=["sunglasses", "glasses display", "optical shop", "eyewear", "spinner rack", "tower"])
def _(S):
    parts = [line("M12 2.5v17"), line("M7.5 21.5h9")]
    for y in (3.5, 9.5, 15.5):
        parts.append(solid(rect(4, y, 6.5, 4, L(S, 0.8, 2))))
        parts.append(solid(rect(13.5, y, 6.5, 4, L(S, 0.8, 2))))
    return parts


@icon("ring-display-tray", CAT, "Shallow tray with slots holding two rings standing upright",
      tags=["ring tray", "jewelry display", "jewellery", "rings", "showcase", "engagement ring"])
def _(S):
    return [
        shell(circle(7, 9, 2.8)),
        shell(circle(17, 9, 2.8)),
        solid(poly([(7, 1.8), (8.7, 3.4), (7, 5.2), (5.3, 3.4)], closed=True)),
        solid(poly([(17, 1.8), (18.7, 3.4), (17, 5.2), (15.3, 3.4)], closed=True)),
        shell(rect(2, 13, 20, 8, S.R)),
        detail("M5 17h14"),
    ]


@icon("watch-display-cushion", CAT, "Oval cushion with a wristwatch strap wrapped around it and the face on top",
      tags=["watch", "wristwatch", "cushion", "watch pillow", "jewelry display", "timepiece"])
def _(S):
    return [
        shell(ellipse(12, 17, 9.5, 4.5)),
        line("M9.5 5.5V2.5M14.5 5.5V2.5"),
        shell(circle(12, 9, 4.5)),
        detail("M12 7v2.2l1.5 1"),
    ]


@icon("earring-card", CAT, "Small card with a hanging hole and a pair of stud earrings pushed through it",
      tags=["earrings", "stud earrings", "jewelry card", "hang tab", "packaging", "accessories"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, S.R)),
        kn(circle_d(12, 5.5, 1.2)),
        solid(circle_d(9, 11.5, 2)),
        solid(circle_d(15, 11.5, 2)),
        detail("M8.5 17.5h7"),
    ]


@icon("mannequin-hand", CAT, "Upright hand-shaped display form on a round base",
      tags=["hand form", "glove display", "jewelry display", "mannequin", "hand model", "glove stand"])
def _(S):
    return [
        shell(rect(7.5, 10, 9, 6.5, L(S, 1, 2.5))),
        line("M9.5 10V4M12 10V3M14.5 10V4"),
        line("M7.5 13.5L4 9.5"),
        line("M12 16.5v4"),
        line("M8 21h8"),
    ]


@icon("glass-door-cooler", CAT, "Upright refrigerator with a glass door and bottles on three shelves",
      tags=["drinks cooler", "beverage cooler", "fridge", "bottle fridge", "convenience store", "refrigerated"])
def _(S):
    parts = [shell(rect(4, 2, 16, 20, S.R)), detail("M4 9h16"), detail("M4 15.5h16")]
    for x in (7, 11, 15):
        parts.append(kn(rect(x, 4.5, 2, 3.5, L(S, 0, 0.8))))
        parts.append(kn(rect(x, 11, 2, 3.5, L(S, 0, 0.8))))
    return parts


@icon("open-display-chiller", CAT, "Open front refrigerated case with a canopy and stepped shelves of packs",
      tags=["multideck", "open chiller", "dairy case", "grocery fridge", "refrigerated shelves", "cold case"])
def _(S):
    parts = [
        shell(rect(3, 2.5, 18, 4, L(S, 0.5, 1.5))),
        line("M4 6.5V21.5M20 6.5V21.5"),
        line("M4 12h16M4 17h16"),
        line("M3 21.5h18"),
    ]
    for x in (7, 11, 15):
        parts.append(solid(rect(x, 8, 2.5, 2.5, 0.6)))
        parts.append(solid(rect(x, 13.5, 2.5, 2.5, 0.6)))
    return parts


@icon("deli-counter", CAT, "Deli counter with a curved glass front and two cuts of meat on display inside",
      tags=["deli", "butcher counter", "meat counter", "food counter", "service counter", "sliced meat"])
def _(S):
    return [
        shell(rect(3, 15, 18, 6, L(S, 0.5, 1.5))),
        line("M4.5 15V11.5C4.5 8.5 6.5 7 10 7H20.5V15"),
        kn(ellipse(10, 12, 3, 1.4)),
        kn(ellipse(16.5, 12, 2.4, 1.4)),
    ]


@icon("gravity-bin-dispenser", CAT, "Clear wall-mounted grain bin with a funnel, lever and chute at the bottom",
      tags=["bulk bin", "bulk foods", "dry goods", "grain dispenser", "cereal dispenser", "nuts and candy", "scoop-free"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 11.5, S.R)),
        detail("M5.5 6h13"),
        kn(circle_d(9, 10.5, 1)), kn(circle_d(12.5, 11, 1)), kn(circle_d(15.5, 10, 1)), kn(circle_d(11, 7.5, 1)),
        shell(poly([(7.5, 14), (16.5, 14), (13.5, 18), (10.5, 18)], closed=True, r=S.r * 0.4)),
        line("M12 18v3.5"),
        line("M16 16.5h4.5"),
    ]


@icon("pick-and-mix-bins", CAT, "Row of three sweet bins with their lids propped open",
      tags=["pick and mix", "candy bins", "sweets", "bulk candy", "sweet shop", "self serve candy"])
def _(S):
    return [
        shell(rect(2, 11, 20, 10, S.R)),
        detail("M8.7 11v10M15.3 11v10"),
        line("M3.5 8.5L5 4.5H7M10.5 8.5L12 4.5H14M17.5 8.5L19 4.5H21"),
        kn(circle_d(5.5, 16, 0.9)), kn(circle_d(12, 17, 0.9)), kn(circle_d(18.5, 16, 0.9)),
    ]


@icon("live-seafood-tank", CAT, "Glass tank with a lobster on the bottom, rising bubbles and a wavy waterline",
      tags=["lobster tank", "fish tank", "seafood counter", "live lobster", "aquarium", "fresh seafood", "fishmonger"])
def _(S):
    return [
        shell(rect(2, 3.5, 20, 17, S.R)),
        detail("M2 8q2.5-2.5 5 0t5 0 5 0 5 0"),
        kn(ellipse(12, 16.5, 4, 2)),
        kn(circle_d(6.6, 14.4, 1.4)), kn(circle_d(17.4, 14.4, 1.4)),
        kn(circle_d(6, 11.3, 0.8)), kn(circle_d(18, 11.5, 0.8)),
    ]


@icon("flower-bucket-stand", CAT, "Tiered stand with three buckets of cut flowers rising in steps",
      tags=["florist", "cut flowers", "flower stall", "bouquets", "flower shop", "buckets", "market stand"])
def _(S):
    parts = []
    for i, x in enumerate((2, 9, 16)):
        top = 16 - 4 * i
        parts.append(shell(poly([(x, top), (x + 6, top), (x + 5.2, 21.5), (x + 0.8, 21.5)], closed=True, r=S.r * 0.4)))
        cx = x + 3
        parts.append(line(f"M{cx} {top}v-2.5"))
        parts.append(solid(circle_d(cx, top - 4.2, 1.9)))
    return parts


@icon("paint-chip-rack", CAT, "Wall rack of paint colour cards, each strip made of three shade blocks",
      tags=["paint swatches", "colour samples", "color chips", "paint aisle", "paint colours", "hardware store", "swatch"])
def _(S):
    parts = [line("M2 3.5h20")]
    for x in (3.5, 10, 16.5):
        parts.append(shell(rect(x, 6, 4, 14, L(S, 0, 1))))
        parts.append(detail(f"M{x} 10.7h4"))
        parts.append(detail(f"M{x} 15.3h4"))
    return parts


@icon("lumber-rack", CAT, "Metal rack with long boards resting on its side arms",
      tags=["timber", "wood boards", "lumber yard", "planks", "building supplies", "cantilever rack", "board storage"])
def _(S):
    return [
        line("M4 2.5v19"),
        line("M4 6h3M4 12h3M4 18h3"),
        shell(rect(7, 4, 15, 4, L(S, 0, 1.5))),
        shell(rect(7, 10, 15, 4, L(S, 0, 1.5))),
        shell(rect(7, 16, 15, 4, L(S, 0, 1.5))),
    ]


@icon("rope-spool-rack", CAT, "Frame bar holding three big spools of rope with the ends hanging down",
      tags=["rope", "cable reel", "cordage", "spools", "hardware store", "rope by the foot", "twine"])
def _(S):
    return [
        shell(rect(3, 4, 5, 9, L(S, 0.5, 1.5))),
        shell(rect(9.5, 4, 5, 9, L(S, 0.5, 1.5))),
        shell(rect(16, 4, 5, 9, L(S, 0.5, 1.5))),
        detail("M2 8.5h20"),
        line("M5.5 13v7.5M12 13v5M18.5 13v7.5"),
    ]


@icon("seed-packet-display", CAT, "Rack of seed packets in pockets, each showing a flower picture",
      tags=["seeds", "seed packets", "garden centre", "gardening", "planting", "seed rack", "flower seeds"])
def _(S):
    parts = []
    for x in (3, 14):
        for y in (2.5, 13.5):
            parts.append(shell(rect(x, y, 7, 8, L(S, 0, 1.2))))
            parts.append(kn(circle_d(x + 3.5, y + 3.3, 1.3)))
            parts.append(kn(rect(x + 3.1, y + 4.8, 0.8, 1.2)))
    return parts


@icon("greeting-card-rack", CAT, "Rack with rows of folded greeting cards standing in pockets",
      tags=["cards", "greeting cards", "birthday cards", "stationery", "card shop", "card display", "gift shop"])
def _(S):
    parts = []
    for y in (2.5, 9, 15.5):
        parts.append(shell(rect(4.5, y, 6, 5.5, L(S, 0, 1.2))))
        parts.append(shell(rect(13.5, y, 6, 5.5, L(S, 0, 1.2))))
        parts.append(line(f"M2.5 {y + 5.5}h19"))
    return parts


@icon("clip-strip-display", CAT, "Vertical clip strip hanging from a hook with snack bags clipped one below another",
      tags=["clip strip", "snack bags", "hanging snacks", "impulse buy", "chips display", "hang sell", "merchandising strip"])
def _(S):
    parts = [line("M12 2.5V5M12 9v2M12 15v2"), line("M12 21v1")]
    for y in (5, 11, 17):
        parts.append(shell(rect(7, y, 10, 4, L(S, 0, 1.2))))
    return parts


@icon("nail-polish-display", CAT, "Stepped acrylic rack with three rows of small nail polish bottles",
      tags=["nail polish", "nail varnish", "cosmetics display", "beauty aisle", "manicure", "polish rack", "bottles"])
def _(S):
    parts = [line("M8 8h8M6 14h12M3.5 20h17")]
    for y, xs in ((8, (8.5, 12.5)), (14, (6, 10.5, 15)), (20, (3.5, 8, 12.5, 17))):
        for x in xs:
            parts.append(solid(rect(x, y - 3.2, 3, 3, L(S, 0.3, 1))))
            parts.append(solid(rect(x + 0.75, y - 5, 1.5, 1.8)))
    return parts


@icon("shirt-folding-board", CAT, "Hinged three-panel folding board with a T-shirt shape laid across it",
      tags=["folding board", "shirt folder", "garment folding", "clothing store", "tee fold", "apparel", "retail tool"])
def _(S):
    tee = [(6.5, 11), (8.5, 7.5), (10.5, 7), (13.5, 7), (15.5, 7.5), (17.5, 11), (15.5, 12.8), (15, 11.8), (15, 17), (9, 17), (9, 11.8), (8.5, 12.8)]
    return [
        shell(rect(2.5, 3, 19, 18, S.R)),
        detail("M8.8 3v18M15.2 3v18"),
        kn(poly(tee, closed=True, r=S.r * 0.3)),
    ]


@icon("waterfall-display-arm", CAT, "Sloped bar fixed to a wall panel with two hangers on it, a waterfall clothing display",
      tags=["waterfall arm", "clothing rail", "hanger bar", "slatwall arm", "garment display", "apparel fixture", "wall bar"])
def _(S):
    return [
        line("M3.5 2.5v19"),
        line("M3.5 6L21 12"),
        dot(20.5, 12.2, 1.4),
        line("M9.5 8v1.2M15.5 10.1v1.2"),
        shell(poly([(5.5, 15), (9.5, 10), (13.5, 15)], closed=True, r=S.r * 0.3)),
        shell(poly([(11.5, 18), (15.5, 13), (19.5, 18)], closed=True, r=S.r * 0.3)),
    ]


@icon("floor-shoe-mirror", CAT, "Low tilted mirror on the floor with a shoe standing next to it",
      tags=["shoe mirror", "footwear", "try on shoes", "shoe store", "floor mirror", "sneaker", "fitting"])
def _(S):
    shoe = [(14.5, 20.5), (22, 20.5), (22, 17.5), (19, 16), (17.2, 12.5), (14.5, 13.5)]
    return [
        shell(poly([(2, 20.5), (4.5, 10), (11.5, 10), (9, 20.5)], closed=True, r=S.r * 0.8)),
        detail("M5.5 16.5l2-3.5"),
        shell(poly(shoe, closed=True, r=S.r * 0.8)),
    ]


@icon("makeup-tester-display", CAT, "Sloped counter tray with lipsticks and a compact below a small mirror",
      tags=["makeup", "cosmetics counter", "lipstick", "tester", "beauty display", "compact", "vanity"])
def _(S):
    return [
        shell(poly([(2, 14.5), (22, 14.5), (21, 21), (3, 21)], closed=True, r=S.r * 0.5)),
        shell(rect(8, 2.5, 8, 6, S.R)),
        solid(poly([(3.5, 14), (3.5, 9.5), (4.75, 7.5), (6, 9.5), (6, 14)], closed=True)),
        solid(poly([(18, 14), (18, 9.5), (19.25, 7.5), (20.5, 9.5), (20.5, 14)], closed=True)),
        solid(circle_d(12, 12, 2)),
    ]


@icon("merchandise-table", CAT, "Low display table with two piles of folded shirts",
      tags=["display table", "sales table", "folded clothes", "apparel table", "promo table", "clothing pile", "retail table"])
def _(S):
    return [
        shell(rect(3, 6.5, 8, 7, L(S, 0.3, 1.5))),
        detail("M3 10h8"),
        shell(rect(13.5, 8.5, 7.5, 5, L(S, 0.3, 1.2))),
        line("M2 14.5h20"),
        line("M4.5 14.5V21M19.5 14.5V21"),
    ]


@icon("folded-shirt-stack", CAT, "Stack of four neatly folded T-shirts with a collar showing on the top one",
      tags=["folded shirts", "t-shirts", "clothes pile", "apparel", "tees", "laundry", "garment stack"])
def _(S):
    return [
        shell(rect(4, 3, 16, 18.5, S.R)),
        detail("M4 8h16M4 12.7h16M4 17.2h16"),
        kn(poly([(9.5, 3.5), (12, 6), (14.5, 3.5)], closed=True)),
    ]


@icon("ball-cage-display", CAT, "Wire mesh floor bin filled with sports balls poking above the rim",
      tags=["ball bin", "sports balls", "wire cage", "sporting goods", "football", "basketball", "bulk bin"])
def _(S):
    return [
        shell(circle(7.5, 8.5, 4)),
        shell(circle(16.5, 8, 4)),
        shell(rect(3, 11.5, 18, 9.5, S.R)),
        detail("M9 11.5v9.5M15 11.5v9.5M3 16.2h18"),
    ]


@icon("listening-station", CAT, "Headphones with a small play screen below, a try-before-you-buy audio post",
      tags=["headphones", "listening post", "music store", "demo station", "audio demo", "sound sample", "play button"])
def _(S):
    return [
        line("M6.5 10V8.5a5.5 5.5 0 0 1 11 0V10"),
        shell(rect(4.2, 9, 3.6, 6.5, L(S, 0.5, 1.6))),
        shell(rect(16.2, 9, 3.6, 6.5, L(S, 0.5, 1.6))),
        shell(rect(5, 17.2, 14, 4.8, L(S, 0.5, 1.5))),
        kn(poly([(10.6, 18.6), (10.6, 20.6), (13.2, 19.6)], closed=True)),
    ]


@icon("can-pyramid-display", CAT, "Pyramid of stacked cans, three on the bottom row rising to one on top",
      tags=["can stack", "canned goods", "pyramid", "grocery display", "tins", "end cap", "promotion"])
def _(S):
    parts = []
    for row, n in enumerate((1, 2, 3)):
        y = 6.9 + 6 * row
        for i in range(n):
            x = 12 + (i - (n - 1) / 2) * 6.6
            parts.append(shell(rect(x - 1.8, y - 1.8, 3.6, 3.6, L(S, 0.4, 1.6))))
    return parts


@icon("acrylic-display-riser", CAT, "Three clear stepped blocks of different heights with a small product on each",
      tags=["riser", "acrylic stand", "stepped display", "product stand", "counter display", "tiered display", "showcase"])
def _(S):
    return [
        shell(rect(2.5, 16, 5.2, 5, L(S, 0.3, 1.5))),
        shell(rect(9.4, 12, 5.2, 9, L(S, 0.3, 1.5))),
        shell(rect(16.3, 8, 5.2, 13, L(S, 0.3, 1.5))),
        solid(circle_d(5.1, 13.2, 1.7)),
        solid(rect(11.8, 7.8, 3.2, 3.2, L(S, 0.2, 0.8))),
        solid(poly([(18.9, 2.2), (20.7, 5.6), (17.1, 5.6)], closed=True)),
    ]


@icon("acrylic-sign-holder", CAT, "Clear stand holding an upright card with lines of text on a counter",
      tags=["sign holder", "menu holder", "table tent", "counter sign", "card stand", "price sign", "display card"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 13.5, S.R)),
        detail("M8.5 7h7M8.5 11h4.5"),
        shell(rect(3, 17, 18, 4, L(S, 0.5, 1.8))),
    ]


@icon("poster-floor-stand", CAT, "Poster frame on a single post standing on a heavy round base",
      tags=["poster stand", "floor sign", "banner stand", "advertising", "sandwich board", "promo sign", "signage"])
def _(S):
    return [
        shell(rect(4, 2, 16, 12.5, S.R)),
        detail("M7 11.5l3-3 2 2 2.5-3.5 2.5 4.5"),
        line("M12 14.5v6"),
        line("M6.5 21.5h11"),
    ]


@icon("phone-display-tether", CAT, "Smartphone on a small puck base joined by a coiled security cable",
      tags=["security tether", "phone display", "anti-theft", "demo phone", "electronics store", "puck", "coiled cable"])
def _(S):
    return [
        shell(rect(5, 2, 8, 14, S.R)),
        shell(rect(3.5, 17.5, 11, 3.5, L(S, 0.5, 1.6))),
        line("M14.5 19.2q1.5-4 3 0t3 0"),
        dot(9, 13.5, 0.9),
    ]


# ============================================================================ chunk 2: fixtures, machines and tags

@icon("hosiery-leg-form", CAT, "Leg shaped display form with a stocking band and a hanging loop at the thigh",
      tags=["leg form", "stocking display", "tights", "hosiery", "sock display", "mannequin leg", "lingerie"])
def _(S):
    return [
        shell(poly([(8, 6), (15, 6), (14, 14), (13, 17), (19, 19.5), (19, 21.5), (10, 21.5), (10, 17)], closed=True, r=S.r * 0.8)),
        detail("M8.4 9.5h6.4"),
        line("M9.5 6V4.5a2.5 2.5 0 0 1 5 0V6"),
    ]


@icon("checkout-impulse-rack", CAT, "Small rack of bins holding candy bars and gum next to a checkout counter edge",
      tags=["impulse buy", "candy rack", "checkout display", "gum", "confectionery", "till point", "counter rack"])
def _(S):
    return [
        shell(rect(2.5, 3, 11, 13, L(S, 0, 2))),
        detail("M2.5 9.5h11"),
        kn(rect(5, 5, 3, 2.5, L(S, 0, 0.8))),
        kn(rect(9, 5, 2.5, 2.5, L(S, 0, 0.8))),
        kn(rect(5, 11.5, 3, 2.5, L(S, 0, 0.8))),
        kn(rect(9, 11.5, 2.5, 2.5, L(S, 0, 0.8))),
        line("M8 16v5M5 21h6"),
        shell(rect(16, 12, 6, 9, L(S, 0, 1.5))),
    ]


@icon("rug-flip-rack", CAT, "Wall mounted rack with hinged arms that fan out, each draped with a hanging rug",
      tags=["rug rack", "carpet display", "flip arms", "mat display", "floor covering", "hinged rack", "home store"])
def _(S):
    return [
        line("M3 2.5v19"),
        shell(rect(6, 3, 14, 7, L(S, 0, 1.5))),
        detail("M9 6.5h8"),
        shell(poly([(6, 12.5), (19, 15), (17.5, 21.5), (6, 19)], closed=True, r=S.r)),
    ]


@icon("tag-detacher", CAT, "Dome shaped detacher fixed on a counter with a round security tag on top",
      tags=["tag remover", "security tag", "anti-theft", "checkout", "magnetic detacher", "loss prevention", "alarm tag"])
def _(S):
    return [
        shell(circle(12, 6.5, 2.75)),
        shell("M4.5 16.5a7.5 5.5 0 0 1 15 0z"),
        shell(rect(3, 16.5, 18, 4, L(S, 0.5, 1.8))),
    ]


@icon("ice-merchandiser", CAT, "Outdoor chest freezer with double doors and a snowflake on the front panel",
      tags=["ice freezer", "bagged ice", "outdoor freezer", "frozen", "convenience store", "snowflake", "cold storage"])
def _(S):
    return [
        shell(rect(3, 3.5, 18, 15.5, S.R)),
        detail("M3 8.5h18"),
        detail("M12 11.5v7M8.5 13.5l7 3M15.5 13.5l-7 3"),
        line("M6 19v2.5M18 19v2.5"),
    ]


@icon("paint-shaker", CAT, "Boxy machine with a paint can clamped between two plates and motion lines on both sides",
      tags=["paint mixer", "paint shop", "shake", "mixing machine", "hardware store", "vibrate", "colour mixing"])
def _(S):
    return [
        shell(rect(6, 3, 12, 18, L(S, 0, 2))),
        detail("M6 6.5h12M6 17.5h12"),
        detail(rect(9, 9.5, 6, 5, L(S, 0, 1))),
        line("M3 9v6M21 9v6"),
    ]


@icon("propane-exchange-cage", CAT, "Mesh cage with two rows of gas cylinders stored inside",
      tags=["gas cylinder", "propane tank", "bottle exchange", "lpg", "cage", "outdoor storage", "refill"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, L(S, 0, 3))),
        detail("M2.5 12h19"),
        kn(rect(5.5, 5.5, 4.5, 5, L(S, 0, 1.5))),
        kn(rect(14, 5.5, 4.5, 5, L(S, 0, 1.5))),
        kn(rect(5.5, 14.5, 4.5, 5, L(S, 0, 1.5))),
        kn(rect(14, 14.5, 4.5, 5, L(S, 0, 1.5))),
    ]


@icon("bread-slicer", CAT, "Slicing machine with a loaf of bread in the front slot and vertical blades above",
      tags=["bakery slicer", "bread machine", "loaf", "slice", "bakery", "blades", "supermarket bakery"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail("M8 6.5v2.5M12 6.5v2.5M16 6.5v2.5"),
        detail("M7 18v-3a3 3 0 0 1 3-3h4a3 3 0 0 1 3 3v3z"),
    ]


@icon("fitting-room-tag", CAT, "Plastic tag with a hanging loop and a large number 3 on its face",
      tags=["fitting room", "changing room", "garment limit", "try on", "number tag", "dressing room", "clothing store"])
def _(S):
    return [
        line("M9.5 9V7.5a2.5 2.5 0 0 1 5 0V9"),
        shell(rect(5, 9, 14, 12, S.R)),
        detail("M9.5 12.5h4.5l-2.5 2.5a2.4 2.4 0 1 1-2 4"),
    ]


@icon("shoe-fitting-stool", CAT, "Low stool seen from the side with a sloped foot rest ramp on its front edge",
      tags=["shoe stool", "fitting stool", "footwear", "try on shoes", "shoe store", "ramp", "seat"])
def _(S):
    return [
        shell(rect(3, 7, 9, 4, L(S, 0.5, 1.8))),
        line("M5 11v9.5M10 11v9.5"),
        shell(poly([(14.5, 14), (21, 18), (21, 20.5), (14.5, 20.5)], closed=True, r=S.r * 0.6)),
    ]


@icon("hanger-size-divider", CAT, "Round disc with a slot to its centre hanging on a rail and marked with a letter M",
      tags=["size divider", "size marker", "clothes rail", "garment size", "medium", "rail divider", "apparel"])
def _(S):
    return [
        line("M2 3.5h20"),
        shell("M10 13.5V6.9A7.5 7.5 0 1 0 14 6.9V13.5z"),
        detail("M9.5 19v-3.5l2.5 2.5 2.5-2.5V19"),
    ]


@icon("electronic-shelf-label", CAT, "Small digital price label clipped to a shelf edge with a price line and a tiny barcode",
      tags=["digital price tag", "e-ink label", "shelf edge", "price display", "esl", "barcode", "smart shelf"])
def _(S):
    return [
        shell(rect(3, 5.5, 18, 11.5, S.R)),
        detail("M6.5 9.5h5"),
        kn(rect(6.5, 12, 4, 2.5, L(S, 0, 0.6))),
        kn(rect(14.5, 8.5, 1.5, 5.5)),
        kn(rect(17.5, 8.5, 1, 5.5)),
        line("M2 20.5h20"),
    ]


@icon("price-check-kiosk", CAT, "Small screen on a wall unit with a scanner window below and a beam line under it",
      tags=["price checker", "scan price", "barcode scanner", "self service", "price lookup", "wall kiosk", "scanner"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 10, S.R)),
        detail("M8 7.5h8"),
        shell(rect(8, 14.5, 8, 3.5, L(S, 0, 1.2))),
        line("M4 21h16"),
    ]


@icon("bag-carousel", CAT, "Rotating stand with three shopping bags hanging from arms around a central post",
      tags=["bag stand", "carry bags", "rotating rack", "bag dispenser", "checkout bags", "spinner", "shopping bags"])
def _(S):
    return [
        line("M4.75 8V4h14.5v4"),
        line("M12 4v9"),
        shell(rect(2.5, 8, 4.5, 6, L(S, 0, 1))),
        shell(rect(17, 8, 4.5, 6, L(S, 0, 1))),
        shell(rect(9.5, 13, 5, 7.5, L(S, 0, 1.2))),
    ]


# ============================================================================ chunk 3: bags, kiosks and carts

def _rotd(d, deg, cx, cy):
    from geometry import P as _P, path_to_d, rotation, transform_path
    return path_to_d(transform_path(_P(d), rotation(deg, cx, cy)))


def _cart(S, basket, handle, wheels, r=None):
    """Shopping cart pieces: basket shell, handle line, two wheel dots."""
    r = S.r if r is None else r
    out = [line(poly(handle, r=r)), shell(poly(basket, closed=True, r=r))]
    for x, y in wheels:
        out.append(dot(x, y, 1.5))
    return out


@icon("boutique-bag", CAT, "Stiff rectangular shopping bag with a looped rope handle and a folded top edge",
      tags=["gift bag", "paper bag", "carrier bag", "luxury shopping", "rope handle", "boutique", "purchase"])
def _(S):
    return [
        line("M8.5 8.5C8.5 2.5 15.5 2.5 15.5 8.5"),
        shell(rect(4, 8.5, 16, 12.5, S.R)),
        detail("M4 12.5h16"),
    ]


@icon("u-boat-stocking-cart", CAT, "Long narrow flat cart with upturned ends and boxes stacked in the middle",
      tags=["stock cart", "flatbed cart", "pallet jack", "restocking", "shelf stocking", "trolley", "warehouse cart"])
def _(S):
    return [
        shell(rect(5, 4.5, 6, 6, L(S, 0, 1.2))),
        shell(rect(13.5, 6, 5.5, 4.5, L(S, 0, 1.2))),
        shell(poly([(2.5, 10.5), (21.5, 10.5), (19.5, 16.5), (4.5, 16.5)], closed=True, r=S.r)),
        dot(7.5, 19.8, 1.4),
        dot(16.5, 19.8, 1.4),
    ]


@icon("cart-wipes-dispenser", CAT, "Upright canister of cart wipes with one wipe pulled up and a small bin at its base",
      tags=["sanitizer wipes", "cart wipes", "hygiene", "disinfectant", "cleaning", "wipe dispenser", "supermarket"])
def _(S):
    return [
        shell(poly([(10, 7.5), (9.5, 3), (14.5, 2.5), (14, 7.5)], closed=True, r=S.r * 0.5)),
        shell(rect(6, 7.5, 12, 7.5, S.R)),
        shell(poly([(7, 18.5), (17, 18.5), (16, 21), (8, 21)], closed=True, r=S.r * 0.4)),
    ]


@icon("produce-bag-dispenser", CAT, "Roll of thin plastic bags on a bar with one bag hanging down by a torn edge",
      tags=["produce bags", "plastic bag roll", "grocery", "fruit bags", "bag roll", "supermarket", "pull bag"])
def _(S):
    return [
        line("M2.5 3h19"),
        shell(circle(7, 10, 4)),
        dot(7, 10, 1.1),
        shell(poly([(13, 3), (20.5, 3), (20.5, 19), (18.5, 17.5), (16.75, 19), (15, 17.5), (13, 19)], closed=True, r=S.r * 0.3)),
        detail("M13 7h7.5"),
    ]


@icon("chalkboard-price-card", CAT, "Small chalkboard sign on a spike pushed into a pile of apples with a price dash",
      tags=["price sign", "chalk sign", "farm stand", "market stall", "apples", "produce price", "greengrocer"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 9, S.R)),
        detail("M8.5 7h7"),
        line("M12 11.5v4"),
        shell(circle(6, 18.5, 2.5)),
        shell(circle(12, 18.5, 2.5)),
        shell(circle(18, 18.5, 2.5)),
    ]


@icon("store-hours-sign", CAT, "Door sign hanging from a string with a clock face above a line of opening times",
      tags=["opening hours", "open sign", "business hours", "door sign", "clock", "schedule", "shop door"])
def _(S):
    return [
        line("M8.5 6.5L12 2.5l3.5 4"),
        shell(rect(4, 6.5, 16, 14.5, S.R)),
        detail(circle(12, 12, 2.5)),
        detail("M8.5 18h7"),
    ]


@icon("self-order-kiosk", CAT, "Tall slim kiosk with a touch screen showing a grid of tiles and a card slot below",
      tags=["order kiosk", "touch screen", "self service", "ordering terminal", "fast food", "menu screen", "pos"])
def _(S):
    return [
        shell(rect(5.5, 2, 13, 15.5, S.R)),
        kn(rect(8, 4.5, 3, 3, L(S, 0, 0.8))),
        kn(rect(13, 4.5, 3, 3, L(S, 0, 0.8))),
        kn(rect(8, 9, 3, 3, L(S, 0, 0.8))),
        kn(rect(13, 9, 3, 3, L(S, 0, 0.8))),
        detail("M9 15h6"),
        line("M12 17.5v3.5M7.5 21h9"),
    ]


@icon("customer-service-desk", CAT, "Counter desk with a round question mark sign standing above it",
      tags=["help desk", "information desk", "service counter", "returns desk", "enquiries", "assistance", "front desk"])
def _(S):
    return [
        shell(circle(12, 7.5, 5)),
        detail("M10.5 6.2a1.5 1.5 0 1 1 2.4 1.2c-.6.4-.9.7-.9 1.2"),
        shell(rect(3, 15.5, 18, 5.5, L(S, 0.5, 2))),
    ]


@icon("antique-cash-register", CAT, "Old fashioned cash register with a number flag on top, keys and a drawer",
      tags=["vintage register", "till", "retro", "cash drawer", "old shop", "sale", "checkout"])
def _(S):
    return [
        shell(rect(8, 2.5, 8, 5.5, L(S, 0, 1.5))),
        detail("M10.5 5.25h3"),
        shell(poly([(4.5, 9), (19.5, 9), (21, 20.5), (3, 20.5)], closed=True, r=S.r)),
        kn(rect(7, 11.5, 2, 3)),
        kn(rect(11, 11.5, 2, 3)),
        kn(rect(15, 11.5, 2, 3)),
        detail("M5 17.5h14"),
    ]


@icon("inventory-handheld", CAT, "Rugged handheld scanner computer with a screen and keys and a beam from its top edge",
      tags=["barcode scanner", "stock take", "handheld terminal", "inventory scanner", "mobile computer", "scan gun", "warehouse"])
def _(S):
    return [
        line("M12 5.5V2M9 6L7 3M15 6l2-3"),
        shell(rect(6.5, 8.5, 11, 13, S.R)),
        detail("M9.5 12h5"),
        dot(9.5, 17, 0.9),
        dot(12, 17, 0.9),
        dot(14.5, 17, 0.9),
    ]


@icon("cart-escalator", CAT, "Inclined moving walkway with a shopping cart riding up it at an angle",
      tags=["travelator", "moving walkway", "cart ramp", "inclined conveyor", "mall", "supermarket", "slope"])
def _(S):
    import math
    ang, cx, cy = -29, 12, 14.7
    def rp(x, y):
        t = math.radians(ang)
        return (cx + (x - cx) * math.cos(t) - (y - cy) * math.sin(t), cy + (x - cx) * math.sin(t) + (y - cy) * math.cos(t))
    parts = [
        Part("line", _rotd(poly([(6, 5.5), (8, 5.5), (9, 10)], r=S.r * 0.5), ang, cx, cy)),
        Part("shell", _rotd(poly([(8, 5.5), (18, 5.5), (16.5, 10), (9, 10)], closed=True, r=S.r * 0.5), ang, cx, cy)),
    ]
    for x in (10, 15.5):
        wx, wy = rp(x, 12.6)
        parts.append(dot(wx, wy, 1.25))
    parts.append(shell(poly([(2, 21), (2, 19), (22, 9.5), (22, 11.5)], closed=True, r=S.r * 0.4)))
    return parts


@icon("smart-shopping-cart", CAT, "Shopping cart with a small screen above its handle and a scan beam coming from the screen",
      tags=["scan and go", "self checkout cart", "connected cart", "cart screen", "retail tech", "smart cart", "scanner"])
def _(S):
    return [
        shell(rect(3, 2, 8, 4.5, L(S, 0, 1.5))),
        line("M14 4.25h7"),
    ] + _cart(S, [(5.5, 10), (21, 10), (19.5, 16), (7, 16)], [(2.5, 10), (5.5, 10)], [(9, 19.5), (17, 19.5)])


@icon("kids-shopping-cart", CAT, "Small child sized shopping cart with a tall flag on a pole at the back",
      tags=["toddler cart", "mini cart", "children's cart", "junior trolley", "family shopping", "flag", "kid"])
def _(S):
    return [
        line("M7 11V3"),
        solid(poly([(7, 3), (13, 4.75), (7, 6.5)], closed=True)),
    ] + _cart(S, [(6, 11), (19, 11), (17.5, 16), (7, 16)], [(2.5, 11), (6, 11)], [(9, 19.5), (15, 19.5)])


@icon("wheelchair-shopping-cart", CAT, "Side view wheelchair with a shopping basket frame attached to its front",
      tags=["accessible cart", "mobility cart", "disability shopping", "motorised cart", "wheelchair", "basket", "inclusive store"])
def _(S):
    return [
        line(circle(9, 15.5, 4.75)),
        dot(9, 15.5, 1.2),
        line(poly([(4.5, 3), (6, 10), (14.5, 10)], r=S.r)),
        shell(rect(14.5, 12, 7, 5.5, L(S, 0, 1.5))),
        dot(18, 20.2, 1.2),
    ]


# ============================================================================ chunk 4: kiosks, packaging and retail operations

def _arrow_head(cx, cy, r, deg, size=2.4):
    """Solid triangle at angle deg on a circle, pointing clockwise along it."""
    import math
    px, py = cx + r * math.cos(math.radians(deg)), cy + r * math.sin(math.radians(deg))
    tx, ty = -math.sin(math.radians(deg)), math.cos(math.radians(deg))
    nx, ny = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    tip = (px + tx * size, py + ty * size)
    a = (px + nx * size * 0.9, py + ny * size * 0.9)
    b = (px - nx * size * 0.9, py - ny * size * 0.9)
    return solid(poly([tip, a, b], closed=True))


@icon("produce-plu-sticker", CAT, "Apple with a small oval sticker on its side showing a product number",
      tags=["plu sticker", "fruit label", "produce code", "price look up", "apple", "grocery", "barcode label"])
def _(S):
    return [
        shell("M12 8C10 6.5 5 7 5 12.5c0 4.5 3 9 5.5 9 .8 0 1-.4 1.5-.4s.7.4 1.5.4c2.5 0 5.5-4.5 5.5-9C19 7 14 6.5 12 8z"),
        line("M12 7.5V5c0-1.5 1-2.5 2.5-2.5"),
        kn(ellipse(14, 14, 2.5, 1.75)),
    ]


@icon("bulk-refill-dispenser", CAT, "Row of three wall dispensers with a glass jar underneath the middle nozzle",
      tags=["refill station", "zero waste", "bulk bins", "dry goods", "gravity dispenser", "eco shop", "jar"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 4.5, 8, L(S, 0, 1.5))),
        shell(rect(9.75, 2.5, 4.5, 8, L(S, 0, 1.5))),
        shell(rect(17, 2.5, 4.5, 8, L(S, 0, 1.5))),
        line("M12 10.5V14"),
        shell(rect(8, 15, 8, 6, L(S, 0.5, 2))),
    ]


@icon("photo-kiosk", CAT, "Kiosk with a touch screen showing a picture and a printed photo coming out of the slot",
      tags=["photo printing", "print station", "picture kiosk", "photo booth", "snapshot", "image print", "drugstore"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 12.5, S.R)),
        dot(8.5, 6.5, 1.1),
        detail("M7 12l3-3 2.5 2.5 2-1.5 2.5 2"),
        shell(rect(8.5, 15, 7, 6.5, L(S, 0, 1))),
    ]


@icon("movie-rental-kiosk", CAT, "Kiosk with a screen and a disc dropping out of the slot below it",
      tags=["dvd rental", "disc kiosk", "film rental", "vending", "blu-ray", "video rental", "red box style"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 12.5, S.R)),
        detail(rect(7.5, 5.5, 9, 5, L(S, 0, 1))),
        shell(circle(12, 18.5, 2.75)),
    ]


@icon("windowed-box-packaging", CAT, "Product box with a clear cut out window on the front showing a small toy inside",
      tags=["window box", "toy packaging", "retail packaging", "clear window", "product box", "display box", "boxed toy"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, L(S, 1, 3))),
        detail(rect(7, 5.5, 10, 9, L(S, 0, 1.5))),
        dot(12, 8.5, 1.4),
        kn(rect(10.5, 10.5, 3, 2.5, L(S, 0, 0.8))),
        detail("M7.5 18.25h9"),
    ]


@icon("refurbished-item", CAT, "Box marked with two circling arrows to show a restored and renewed product",
      tags=["refurbished", "renewed", "recycled goods", "second hand", "restored", "reuse", "pre-owned"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(arc(12, 12, 4.25, 205, 335)),
        detail(arc(12, 12, 4.25, 25, 155)),
        _arrow_head(12, 12, 4.25, 335, 2.3),
        _arrow_head(12, 12, 4.25, 155, 2.3),
    ]


@icon("return-authorization", CAT, "Form with two text lines and a large return arrow turning back beside it",
      tags=["rma", "return form", "refund request", "return label", "send back", "exchange", "return slip"])
def _(S):
    return [
        shell(rect(2.5, 3, 10, 18, S.R)),
        detail("M5.5 8h4M5.5 12.5h4"),
        line("M21 8v6a3 3 0 0 1-3 3h-2.5"),
        line("M18 14.5L15.5 17l2.5 2.5"),
    ]


@icon("footfall-counter", CAT, "Door frame with a sensor box above it and a person walking through",
      tags=["people counter", "visitor count", "foot traffic", "entrance sensor", "door counter", "store traffic", "analytics"])
def _(S):
    return [
        line("M4.5 21.5V8h15v13.5"),
        shell(rect(9.5, 2.5, 5, 3.5, L(S, 0, 1))),
        dot(12, 12.5, 1.7),
        line("M12 14.5v3M9.5 21l2.5-3.5 2.5 3.5"),
    ]


@icon("shoplifting", CAT, "Jacket with a collar and a pocket with a small box being slipped into it",
      tags=["theft", "stealing", "loss prevention", "pocketing", "retail crime", "shrinkage", "stolen goods"])
def _(S):
    return [
        shell(poly([(9, 3), (12.5, 7), (16, 3), (21, 6), (21, 21.5), (4, 21.5), (4, 6)], closed=True, r=S.r)),
        detail("M13 16h5"),
        detail(rect(13.5, 10, 4, 4)),
    ]



@icon("mystery-shopper", CAT, "Person in a brimmed hat and sunglasses standing next to a shopping bag",
      tags=["secret shopper", "undercover", "audit", "customer evaluation", "inspector", "survey", "disguise"])
def _(S):
    return [
        line("M3 6.5h13"),
        shell(poly([(6.5, 6.5), (7, 2.5), (12, 2.5), (12.5, 6.5)], closed=True, r=S.r * 0.4)),
        shell(circle(9.5, 10.5, 3.25)),
        kn(rect(7.25, 10, 4.5, 1.6)),
        line("M4.5 21.5v-2.5a5 5 0 0 1 10 0v2.5"),
        shell(rect(16.5, 14.5, 5, 7, L(S, 0, 1))),
        line("M18.25 14.5v-1.5a1.25 1.25 0 0 1 2.5 0v1.5"),
    ]



@icon("price-history", CAT, "Price tag with a small zigzag line chart drawn across its face",
      tags=["price chart", "price tracking", "price drop", "price trend", "price graph", "historic price", "deal tracker"])
def _(S):
    return [
        shell(poly([(4, 6.5), (8, 2.5), (16, 2.5), (20, 6.5), (20, 21.5), (4, 21.5)], closed=True, r=S.r)),
        dot(12, 6, 1.1),
        detail("M7 17.5l3.5-3.5 2.5 2.5 4-5"),
    ]


@icon("handmade-goods", CAT, "Knitted beanie with a pom-pom and a small stitched heart on the front",
      tags=["handmade", "knitted", "craft fair", "artisan", "homemade", "crochet", "etsy style"])
def _(S):
    return [
        shell(circle(12, 3.5, 1.75)),
        shell("M6 14C6 7 8.5 5.5 12 5.5s6 1.5 6 8.5z"),
        shell(rect(5, 14, 14, 4.5, L(S, 0.5, 1.8))),
        kn("M12 12.5l-2.4-2.4a1.6 1.6 0 0 1 2.4-2 1.6 1.6 0 0 1 2.4 2z"),
    ]
