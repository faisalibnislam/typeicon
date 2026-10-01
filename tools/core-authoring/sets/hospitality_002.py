"""TypeIcon Core: hospitality (batch hospitality_002): service ware, carts, bar tools and event gear."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "hospitality"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def hole(d):
    """Solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def bottle(x, top, bottom, w=6.0, neck=3.0, shoulder=3.0, S=None):
    """Closed bottle silhouette centred on x."""
    hw, hn = w / 2, neck / 2
    pts = [(x - hn, top), (x + hn, top), (x + hn, bottom - 0), ]
    return poly([(x - hn, top), (x + hn, top), (x + hn, top + 5), (x + hw, top + 5 + shoulder), (x + hw, bottom),
                 (x - hw, bottom), (x - hw, top + 5 + shoulder), (x - hn, top + 5)], closed=True, r=(S.r if S else 0))


def wheel(x, y, r=1.6):
    return circle(x, y, r)


# ============================================================================ chunk 1

@icon("jam-portion", CAT, "Small tapered plastic tub with a foil lid peeled back and a fruit mark on the side",
      tags=["jam", "jelly", "preserves", "breakfast", "single serve", "portion pack", "marmalade"])
def _(S):
    body = poly([(4, 9.5), (20, 9.5), (20, 11.5), (18, 11.5), (17, 21), (7, 21), (6, 11.5), (4, 11.5)], closed=True, r=S.r * 0.6)
    return [shell(body), line("M20 9C20.5 5.5 17.5 3.5 13.5 5"), detail(circle(12, 16, 1.7))]


@icon("tea-bag-chest", CAT, "Wooden tea box with its lid propped open above a row of compartments",
      tags=["tea chest", "tea box", "tea bags", "tea selection", "cafe", "hotel", "assortment"])
def _(S):
    lid = poly([(7, 2.5), (17, 2.5), (20, 8.5), (4, 8.5)], closed=True, r=S.r)
    box = rect(3, 11.5, 18, 9.5, rr(S, 2))
    return [shell(lid), shell(box), detail(seg(9, 12, 9, 21)), detail(seg(15, 12, 15, 21))]


@icon("bottle-coaster", CAT, "Low round dish with a wine bottle standing in it",
      tags=["wine coaster", "bottle holder", "table", "dining", "drip", "stand", "bar"])
def _(S):
    dish = poly([(3, 16.5), (21, 16.5), (19, 21), (5, 21)], closed=True, r=S.r)
    bt = "M9 16.5V10.5L10.5 8.5V3H13.5V8.5L15 10.5V16.5"
    return [shell(dish), line(bt)]


@icon("wine-bucket-stand", CAT, "Three legged stand holding an ice bucket with a bottle neck sticking out",
      tags=["ice bucket", "champagne", "chiller", "wine cooler", "stand", "restaurant", "table service"])
def _(S):
    bucket = union(poly([(5.5, 9), (18.5, 9), (17, 16), (7, 16)], closed=True, r=S.r),
                   poly([(10.5, 2.5), (13.5, 2.5), (13.5, 10), (10.5, 10)], closed=True))
    return [shell(bucket), line("M8.5 16L5 21.5"), line("M15.5 16L19 21.5"), line(seg(12, 16, 12, 21.5))]


@icon("wine-thermometer", CAT, "Wine bottle with a temperature scale band wrapped around its body",
      tags=["bottle thermometer", "wine temperature", "chill", "serving temperature", "sommelier", "cellar", "degrees"])
def _(S):
    return [shell(bottle(12, 2, 21.5, 8, 3, 3, S)), detail(seg(8, 13.5, 16, 13.5)), detail(seg(8, 18.5, 16, 18.5)),
            dot(12, 16, 1)]


@icon("wine-aerator", CAT, "Funnel shaped aerator with air holes pouring a stream of wine into a glass",
      tags=["aerate", "wine pourer", "decant", "breathe", "sommelier", "pour", "red wine"])
def _(S):
    funnel = poly([(5.5, 2.5), (18.5, 2.5), (14, 8.5), (14, 11.5), (10, 11.5), (10, 8.5)], closed=True, r=S.r)
    bowl = "M7.5 16.5H16.5A4.5 4 0 0 1 7.5 16.5Z"
    return [shell(funnel), hole(circle(10, 5.2, 0.9)), hole(circle(14, 5.2, 0.9)), line(seg(12, 12.5, 12, 15.5)),
            shell(bowl), line(seg(12, 20.5, 12, 21))]


@icon("wine-spittoon", CAT, "Tall bucket with a wide funnel top and drops falling in",
      tags=["spit bucket", "wine tasting", "dump bucket", "sommelier", "cellar door", "tasting room", "winery"])
def _(S):
    body = poly([(3.5, 3), (20.5, 3), (15.5, 10), (15.5, 21), (8.5, 21), (8.5, 10)], closed=True, r=S.r)
    return [shell(body), dot(10.5, 6.2, 1), dot(13.5, 6.2, 1), dot(12, 9.8, 1), detail(seg(8.5, 16, 15.5, 16))]


@icon("wine-glass-charm", CAT, "Wine glass with a small hoop ring on its stem and a bead hanging from it",
      tags=["drink marker", "glass tag", "party favor", "stem ring", "identifier", "wedding", "dinner party"])
def _(S):
    bowl = "M6.5 2.5H17.5C17.5 8 15.5 11.5 12 11.5S6.5 8 6.5 2.5Z"
    return [shell(bowl), line(seg(12, 11.5, 12, 12.5)), line(seg(12, 17.5, 12, 21)), line(seg(8.5, 21, 15.5, 21)),
            shell(circle(12, 15, 2.5)), line(seg(14.2, 16.6, 17.6, 18.2)), dot(18.8, 19, 1.6)]


@icon("caviar-service", CAT, "Small tin of caviar set in a bowl of ice with a shell spoon beside it",
      tags=["caviar", "roe", "fine dining", "luxury", "ice bowl", "appetizer", "delicacy"])
def _(S):
    bowl = union("M3 12.5H21A9 8 0 0 1 3 12.5Z", rect(6, 6, 8, 7, rr(S, 1.5)))
    return [shell(bowl), detail(seg(3, 12.5, 6, 12.5)), detail(seg(14, 12.5, 21, 12.5)),
            dot(9, 16.5, 1), dot(13, 17.2, 1), dot(16.5, 15.8, 1),
            line(seg(20.5, 2.5, 18, 7)), dot(17, 9, 1.8)]


@icon("fruit-platter", CAT, "Oval platter holding a fruit slice and a bunch of grapes",
      tags=["fruit tray", "fruit plate", "melon", "buffet", "catering", "fresh fruit", "brunch"])
def _(S):
    return [shell(ellipse(12, 17.5, 9.5, 3.5)), shell(circle(8, 10, 3.6)), dot(8, 10, 0.9),
            dot(15.5, 9.5, 1.7), dot(19, 9.5, 1.7), dot(17.2, 12.7, 1.7), line(seg(17.2, 5, 17.2, 7.5))]


@icon("finger-sandwiches", CAT, "Two slim crustless sandwiches with filling lines resting on a plate",
      tags=["tea sandwiches", "afternoon tea", "high tea", "canape", "snack", "catering", "cucumber"])
def _(S):
    return [shell(rect(3, 3, 16, 6.5, L(S, 0, 2.5))), detail(seg(3, 6.25, 19, 6.25)),
            shell(rect(5, 12.5, 16, 6.5, L(S, 0, 2.5))), detail(seg(5, 15.75, 21, 15.75))]


@icon("tapas", CAT, "Top view of a serving board with four small round dishes",
      tags=["small plates", "spanish food", "appetizers", "sharing plates", "bar snacks", "bites", "meze"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, rr(S))), detail(circle(8.5, 8.5, 2.2)), detail(circle(15.5, 8.5, 2.2)),
            detail(circle(8.5, 15.5, 2.2)), detail(circle(15.5, 15.5, 2.2))]


@icon("verrine", CAT, "Small straight sided glass with three layers inside and a spoon sticking out",
      tags=["layered dessert", "appetizer glass", "mini trifle", "amuse bouche", "parfait", "tasting", "catering"])
def _(S):
    return [shell(rect(5.5, 7, 12, 14.5, rr(S, 1.5))), detail(seg(5.5, 12.5, 17.5, 12.5)),
            detail(seg(5.5, 17, 17.5, 17)), line(seg(19.5, 2.5, 14.5, 10))]


@icon("butter-curler", CAT, "Hooked blade tool drawing a curl of butter from a block",
      tags=["butter curl", "butter ribbon", "garnish", "table setting", "banquet", "bread service", "dairy"])
def _(S):
    return [shell(rect(3, 16, 13, 5, L(S, 0, 1.5))), line("M5 13.5C3 9 8.5 7 10.3 9.8C11.7 12 9 13 8.2 11.5"),
            line("M21 3L16.5 10.5L13.5 15")]


@icon("soy-sauce-dish", CAT, "Small rounded dish with a dark pool of sauce and chopsticks resting above it",
      tags=["dipping sauce", "sushi", "japanese", "condiment", "dip bowl", "chopsticks", "restaurant"])
def _(S):
    return [shell(rect(3, 10.5, 18, 10.5, rr(S, 5))), hole(rect(7, 13.5, 10, 4.5, 2)),
            line("M3.5 3.5L20.5 2.5"), line("M3.5 7L20.5 6")]


# ============================================================================ chunk 2

@icon("hot-stone-grill", CAT, "Flat stone slab on a wooden board with a steak on top and heat lines rising",
      tags=["hot stone", "lava stone", "table grill", "steak", "cook at table", "sizzle", "korean bbq"])
def _(S):
    return [shell(rect(2.5, 18.5, 19, 3, L(S, 0, 1.5))), shell(rect(4, 13, 16, 4, L(S, 0, 1.5))),
            shell(ellipse(12, 9.5, 4.5, 2.5)), line("M5.5 10C4.5 8 6.5 7 5.5 4.5"), line("M18.5 10C17.5 8 19.5 7 18.5 4.5")]


@icon("silver-tea-service", CAT, "Tray holding a pear shaped teapot and a lidded sugar bowl",
      tags=["tea set", "teapot", "high tea", "afternoon tea", "hotel", "silverware", "sugar bowl"])
def _(S):
    pot = "M4.5 18.5C4 13.5 6 10.5 8.5 10.5S13.5 13.5 13 18.5Z"
    bowl = "M16.5 18.5C16.5 14.5 18 13 19.2 13S21.8 14.5 21.8 18.5Z"
    return [shell(rect(2, 19, 20, 2.5, L(S, 0, 1.2))), shell(pot), line(seg(8.5, 7.5, 8.5, 10.5)),
            line("M5 14.5L2.8 11.8"), shell(bowl)]


@icon("gongfu-tea-tray", CAT, "Slatted tea tray with a small teapot and a tiny cup standing on it",
      tags=["tea ceremony", "chinese tea", "gongfu", "cha dao", "tea table", "tea set", "tea house"])
def _(S):
    pot = "M4.5 13.5C4 9.5 6 7.5 8 7.5S12 9.5 11.5 13.5Z"
    cup = "M14.5 9.5H19.5C19.5 12 18.5 13.5 17 13.5S14.5 12 14.5 9.5Z"
    return [shell(rect(2.5, 14.5, 19, 6.5, L(S, 0, 2))), detail(seg(8, 15.5, 8, 20)), detail(seg(12, 15.5, 12, 20)),
            detail(seg(16, 15.5, 16, 20)), shell(pot), line("M5 10.5L3 8.5"), shell(cup)]


@icon("kitchen-pass", CAT, "Wall with a serving opening holding two plates under heat lamps",
      tags=["pass through", "service window", "order window", "heat lamp", "restaurant kitchen", "expo", "plates up"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, rr(S, 3))), detail(rect(5.5, 7.5, 13, 10, L(S, 0, 1.5))),
            hole("M6.8 14.6A2.6 2.8 0 0 1 12 14.6Z"), hole("M13 14.6A2.6 2.8 0 0 1 18.2 14.6Z"),
            hole(rect(6.4, 14.8, 6.4, 1.2)), hole(rect(12.8, 14.8, 6.4, 1.2))]


@icon("bus-tub", CAT, "Rectangular plastic tub with a stack of dirty plates showing above its rim",
      tags=["dish tub", "bussing", "dirty dishes", "dish bin", "restaurant", "cleanup", "busser"])
def _(S):
    tub = poly([(3, 9), (21, 9), (19, 21), (5, 21)], closed=True, r=S.r)
    return [shell(tub), detail(seg(9, 13, 15, 13)), line(seg(6.5, 6, 17.5, 6)), line(seg(8, 2.8, 16, 2.8))]


@icon("bussing-cart", CAT, "Three shelf wheeled cart with a bus tub on top and stacked plates below",
      tags=["bus cart", "dish cart", "clearing cart", "restaurant", "utility cart", "busser", "cleanup"])
def _(S):
    return [line("M5 3V18.5"), line("M19 3V18.5"), line(seg(5, 9, 19, 9)), line(seg(5, 16, 19, 16)),
            line("M7.5 9V4.5H16.5V9"), line("M8.5 16V12.5H15.5V16"), dot(5, 21, 1), dot(19, 21, 1)]


@icon("tray-return-rack", CAT, "Tall wheeled frame with slots and cafeteria trays slid in at the right",
      tags=["tray rack", "cafeteria", "canteen", "dining hall", "tray cart", "school lunch", "clearing"])
def _(S):
    return [shell(rect(3.5, 2.5, 13.5, 15, rr(S, 2))), detail(seg(3.5, 7.5, 17, 7.5)), detail(seg(3.5, 12.5, 17, 12.5)),
            line(seg(17, 7.5, 21.5, 7.5)), line(seg(17, 12.5, 21.5, 12.5)), dot(7, 21, 1.1), dot(14, 21, 1.1)]


@icon("glass-rack", CAT, "Crate with divided compartments and upside down glasses standing in it",
      tags=["dishwasher rack", "glassware", "bar glasses", "crate", "bar back", "glass washing", "compartments"])
def _(S):
    return [shell(rect(3, 3, 18, 18, rr(S, 3))), detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
            detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15)), dot(6, 6, 1.2), dot(12, 6, 1.2), dot(18, 6, 1.2),
            dot(6, 12, 1.2), dot(12, 12, 1.2), dot(18, 12, 1.2), dot(6, 18, 1.2), dot(12, 18, 1.2), dot(18, 18, 1.2)]


@icon("heated-plate-dispenser", CAT, "Cylindrical warmer with a stack of plates in its top opening and a spring beneath",
      tags=["plate warmer", "plate dispenser", "buffet", "canteen", "spring loaded", "cafeteria", "stack of plates"])
def _(S):
    return [shell(rect(4, 10.5, 16, 10.5, rr(S, 3))), detail(poly([(7.5, 16), (9.5, 13), (12, 18.5), (14.5, 13), (16.5, 16)])),
            line(seg(6.5, 7, 17.5, 7)), line(seg(8, 3.5, 16, 3.5))]


@icon("soup-kettle", CAT, "Round electric soup warmer with its lid tilted open and a ladle handle sticking out",
      tags=["soup warmer", "kettle", "buffet", "soup station", "ladle", "hot soup", "canteen"])
def _(S):
    return [shell(rect(4, 11, 16, 10, rr(S, 4))), shell("M6.5 11A5.5 5 0 0 1 17.5 11Z"), line(seg(12, 3.5, 12, 6)),
            line(seg(1.5, 15, 4, 15)), line(seg(20, 15, 22.5, 15))]


@icon("carving-station", CAT, "Roast joint on a board under a hanging heat lamp with a knife beside it",
      tags=["carvery", "roast", "buffet", "heat lamp", "chef", "carving board", "sunday roast"])
def _(S):
    lamp = "M3.5 8.5C3.5 5 7 3 12 3S20.5 5 20.5 8.5Z"
    return [shell(lamp), shell(ellipse(12, 14.2, 5, 2.8)), shell(rect(3, 19, 18, 2.5, L(S, 0, 1.2))),
            line(seg(4, 11.5, 4, 17.5)), line(seg(20, 11.5, 20, 17.5))]


@icon("omelette-station", CAT, "Pan with a folded omelette over a portable burner flame",
      tags=["omelet", "egg station", "cook to order", "brunch", "buffet", "breakfast", "live cooking"])
def _(S):
    return [shell("M5 8.5A4.5 4.5 0 0 1 14 8.5Z"), shell(rect(3.5, 8.5, 12, 2.5, L(S, 0, 1.2))),
            line(seg(15.5, 9.75, 21.5, 9.75)), line(seg(6.5, 13.5, 6.5, 15)), line(seg(10, 13.5, 10, 15)),
            line(seg(13.5, 13.5, 13.5, 15)), shell(rect(3, 17, 14, 4, L(S, 0, 1.5)))]


@icon("conveyor-toaster", CAT, "Boxy toaster with a front slot and a slice of toast sliding out of the bottom chute",
      tags=["toaster", "bread toaster", "buffet", "breakfast", "hotel", "conveyor", "toast"])
def _(S):
    return [shell(rect(3, 3, 18, 11, rr(S, 3))), hole(rect(6.5, 6, 11, 2.5, L(S, 0, 1.2))),
            shell("M8 21.5V18.5C6.5 18.5 6.5 16 9 16H15C17.5 16 17.5 18.5 16 18.5V21.5Z")]


@icon("pancake-machine", CAT, "Boxy dispenser with a small screen and a stack of pancakes on a plate beneath it",
      tags=["pancake maker", "breakfast", "hotel buffet", "automatic", "griddle cakes", "flapjacks", "dispenser"])
def _(S):
    return [shell(rect(3, 2.5, 18, 11.5, rr(S, 3))), hole(rect(6, 5.5, 8, 3.5, L(S, 0, 1))), dot(17.5, 7.2, 1.2),
            shell(rect(6, 16, 12, 3.2, L(S, 0, 1.5))), line(seg(4, 21.5, 20, 21.5))]


# ============================================================================ chunk 3

def small_bottle(x, base, h, w=2.8):
    hw = w / 2
    return poly([(x - hw, base), (x - hw, base - h * 0.55), (x - 0.7, base - h * 0.75), (x - 0.7, base - h),
                 (x + 0.7, base - h), (x + 0.7, base - h * 0.75), (x + hw, base - h * 0.55), (x + hw, base)], closed=True)


@icon("straw-dispenser", CAT, "Upright clear cylinder filled with straws on a base with one straw dropping out",
      tags=["straws", "drinking straws", "cafe", "fast food", "condiment station", "dispenser", "self serve"])
def _(S):
    return [shell(rect(3.5, 2.5, 12, 14, rr(S, 3))), detail(seg(7.5, 5, 7.5, 14)), detail(seg(11.5, 5, 11.5, 14)),
            shell(rect(2.5, 17.5, 14, 3.5, L(S, 0, 1.5))), line(seg(20, 11, 20, 20))]


@icon("meal-ticket-machine", CAT, "Vending style box with a screen, buttons and a coin slot and a ticket sticking out",
      tags=["ticket dispenser", "meal voucher", "canteen", "token", "kiosk", "cafeteria", "coupon"])
def _(S):
    return [shell(rect(3, 2.5, 13, 19, rr(S, 3))), hole(rect(6, 5.5, 7, 3, L(S, 0, 1))), dot(7, 12, 1.1), dot(12, 12, 1.1),
            dot(7, 15.5, 1.1), dot(12, 15.5, 1.1), hole(rect(6.5, 18, 6, 1.2, 0.6)), line("M16 12.5H21.5V18H16")]


@icon("food-sample-display", CAT, "Glass display box with two shelves of modeled dishes and price tags below",
      tags=["plastic food", "menu display", "window display", "restaurant", "sample dishes", "showcase", "japan"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, rr(S, 3))), detail(seg(2.5, 9.5, 21.5, 9.5)), detail(seg(2.5, 15.5, 21.5, 15.5)),
            dot(7, 6.5, 1.3), dot(12, 6.5, 1.3), dot(17, 6.5, 1.3), dot(7, 12.7, 1.3), dot(12, 12.7, 1.3), dot(17, 12.7, 1.3),
            hole(rect(5.5, 18.3, 3, 1.2)), hole(rect(10.5, 18.3, 3, 1.2)), hole(rect(15.5, 18.3, 3, 1.2))]


@icon("dessert-trolley", CAT, "Two shelf wheeled cart with a cake on top and small desserts below",
      tags=["dessert cart", "pastry cart", "cake trolley", "sweet cart", "restaurant", "fine dining", "tableside"])
def _(S):
    return [shell(rect(7, 4.5, 10, 5.5, L(S, 0, 2))), dot(12, 2.8, 0.9),
            line(seg(4, 11, 20, 11)), line(seg(4, 17, 20, 17)), line("M4 11V18.5"), line("M20 11V5.5H22.5"),
            dot(8.5, 14.3, 1.3), dot(12.5, 14.3, 1.3), dot(16.5, 14.3, 1.3), dot(5, 21, 1), dot(19, 21, 1)]


@icon("flambe-trolley", CAT, "Wheeled cart with a burner and pan on top and tall flames rising from the pan",
      tags=["flambe", "tableside cooking", "flame", "fine dining", "crepe suzanne", "gueridon", "cart"])
def _(S):
    flame = "M10.5 2.5C12.5 5 14 6 14 8A3.5 3.5 0 0 1 7 8C7 6 8.5 5 10.5 2.5Z"
    return [shell(flame), shell(rect(4, 11, 11, 2.5, L(S, 0, 1.2))), line(seg(15, 12.25, 21.5, 12.25)),
            line(seg(3, 16, 21, 16)), line(seg(5, 16, 5, 19.5)), line(seg(19, 16, 19, 19.5)), dot(5, 21, 1), dot(19, 21, 1)]


@icon("carving-trolley", CAT, "Wheeled cart with a silver dome cover rolled partly back to show a roast",
      tags=["gueridon", "silver dome", "tableside carving", "roast trolley", "fine dining", "cloche", "joint of meat"])
def _(S):
    return [shell(ellipse(15, 7.7, 4.5, 2.8)), shell(rect(3, 11, 18, 3, L(S, 0, 1.2))), line("M3.5 10C3.5 5.5 6.5 3 10.5 3"),
            line(seg(5, 14, 5, 19)), line(seg(19, 14, 19, 19)), dot(5, 21, 1), dot(19, 21, 1)]


@icon("dim-sum-cart", CAT, "Push cart stacked with bamboo steamer baskets with steam rising above them",
      tags=["yum cha", "steamer basket", "chinese restaurant", "dumplings", "bamboo", "push cart", "cantonese"])
def _(S):
    return [shell(rect(3.5, 7, 11.5, 4.5, L(S, 0, 2))), shell(rect(3.5, 12.5, 11.5, 4.5, L(S, 0, 2))),
            line(seg(6.5, 2.5, 6.5, 4.5)), line(seg(11.5, 2.5, 11.5, 4.5)),
            line("M15 7.5H20V18.5"), line(seg(3, 18.5, 20, 18.5)), dot(6, 21, 1), dot(17, 21, 1)]


@icon("teppanyaki-counter", CAT, "Flat griddle counter with a mound of rice and a spatula and round seat shapes along the front",
      tags=["teppan", "hibachi", "griddle", "japanese steakhouse", "chef show", "grill counter", "iron plate"])
def _(S):
    return [shell(rect(2.5, 9, 19, 4, L(S, 0, 1.5))), shell("M5.5 9A3.5 4 0 0 1 12.5 9Z"),
            line("M21 3L15.5 7.5"), line(seg(3.5, 17.5, 9.5, 17.5)), line(seg(6.5, 17.5, 6.5, 21.5)),
            line(seg(14.5, 17.5, 20.5, 17.5)), line(seg(17.5, 17.5, 17.5, 21.5))]


@icon("sushi-counter", CAT, "Counter with a raised glass case holding pieces of fish",
      tags=["sushi bar", "omakase", "fish case", "japanese restaurant", "deli counter", "display case", "seafood"])
def _(S):
    return [shell(poly([(4, 12), (5.5, 4), (18.5, 4), (20, 12)], closed=True, r=S.r)), hole(ellipse(9.5, 8.7, 2.4, 1.3)),
            hole(ellipse(14.5, 8.7, 2.4, 1.3)), shell(rect(2.5, 13.5, 19, 7.5, L(S, 0, 2)))]


@icon("hot-dog-cart", CAT, "Street cart with a striped umbrella over a box body, two wheels and a sausage mark",
      tags=["street food", "food cart", "vendor", "stand", "hot dog stand", "hotdog", "umbrella"])
def _(S):
    return [shell("M3.5 8.5A8.5 6 0 0 1 20.5 8.5Z"), detail(seg(8.2, 3.5, 8.2, 8.5)), detail(seg(15.8, 3.5, 15.8, 8.5)),
            line(seg(12, 8.5, 12, 11.5)), shell(rect(4, 11.5, 16, 6.5, L(S, 0, 2))), hole(rect(8, 13.8, 8, 2, 1)),
            dot(8, 20.5, 1.5), dot(16, 20.5, 1.5)]


@icon("beer-garden-table", CAT, "Long table with two attached bench seats and a beer mug on top",
      tags=["biergarten", "picnic table", "outdoor seating", "pub", "oktoberfest", "bench table", "patio"])
def _(S):
    return [shell(rect(9.5, 2.5, 5, 5.5, L(S, 0, 1.5))), line("M14.5 4.2H17.5V6.4H14.5"), shell(rect(3.5, 8, 17, 2.5, L(S, 0, 1.2))),
            line(seg(7, 10.5, 7, 21)), line(seg(17, 10.5, 17, 21)), line(seg(1.5, 15.5, 8.5, 15.5)), line(seg(15.5, 15.5, 22.5, 15.5))]


@icon("back-bar", CAT, "Two bar shelves lined with bottles of different heights",
      tags=["liquor shelf", "bottle display", "spirits", "bar", "pub", "bartender", "shelving"])
def _(S):
    parts = [line(seg(2.5, 10.5, 21.5, 10.5)), line(seg(2.5, 19, 21.5, 19))]
    for x, h in ((6, 6.5), (12, 5), (18, 6.5)):
        parts.append(shell(small_bottle(x, 10.5, h)))
    for x, h in ((6, 5), (12, 6.5), (18, 5)):
        parts.append(shell(small_bottle(x, 19, h)))
    return parts


@icon("speed-rail", CAT, "Narrow rail along a bar front with a row of bottles standing in it",
      tags=["speed rack", "well bottles", "pour spouts", "bartender", "bar", "liquor", "well spirits"])
def _(S):
    parts = [shell(rect(2.5, 14.5, 19, 4.5, L(S, 0, 1.5)))]
    for x in (6, 12, 18):
        parts.append(shell(small_bottle(x, 15, 11, 3.6)))
        parts.append(line(seg(x - 1.4, 2.8, x + 1.4, 2.8)))
    return parts


@icon("bar-mat", CAT, "Ribbed rubber mat seen at an angle with a glass standing on it",
      tags=["rubber mat", "drip mat", "spill mat", "bar top", "bartender", "service mat", "glass"])
def _(S):
    mat = poly([(5, 12), (22, 12), (19, 20), (2, 20)], closed=True, r=S.r)
    glass = poly([(8.5, 2.5), (15.5, 2.5), (14.5, 13), (9.5, 13)], closed=True, r=S.r)
    return [shell(union(mat, glass)), detail(seg(3.5, 15, 20, 15)), detail(seg(2.8, 18, 18.8, 18))]


@icon("bar-caddy", CAT, "Compartment organizer holding straws, napkins and cocktail picks",
      tags=["garnish caddy", "straw holder", "napkin holder", "bar organizer", "condiment holder", "bartender", "cocktail picks"])
def _(S):
    return [shell(rect(3, 12, 18, 9, rr(S, 2))), detail(seg(9, 12, 9, 21)), detail(seg(15, 12, 15, 21)),
            line(seg(5, 12, 4, 4)), line(seg(7.5, 12, 8.5, 4)), line("M10.8 12V7.5H13.2V12"),
            line(seg(17, 12, 17, 6)), dot(17, 4.3, 1.3), line(seg(19.5, 12, 19.5, 8)), dot(19.5, 6.5, 1)]


@icon("garnish-tray", CAT, "Long compartment tray with its lid lifted above lemon, olive and cherry sections",
      tags=["bar tray", "lemon wedge", "olives", "cherries", "bartender", "cocktail garnish", "condiment tray"])
def _(S):
    return [shell(poly([(5, 3), (19, 3), (21.5, 8), (2.5, 8)], closed=True, r=S.r)),
            shell(rect(2.5, 11.5, 19, 9.5, rr(S, 2))), detail(seg(9, 11.5, 9, 21)), detail(seg(15, 11.5, 15, 21)),
            hole(circle(6, 16.5, 1.5)), hole(poly([(10.8, 18.5), (13.2, 18.5), (12, 14.3)], closed=True)),
            hole(circle(18, 16.5, 1.5))]


# ============================================================================ chunk 4

@icon("glass-rimmer", CAT, "Three stacked shallow trays with an upside down glass pressed onto the top one",
      tags=["salt rim", "sugar rim", "margarita", "cocktail prep", "bartender", "garnish station", "rimming"])
def _(S):
    return [shell(poly([(8, 2.5), (16, 2.5), (17, 11), (7, 11)], closed=True, r=S.r)),
            shell(rect(3.5, 11.5, 17, 3.2, L(S, 0, 1.5))), shell(rect(3.5, 15, 17, 3.2, L(S, 0, 1.5))),
            shell(rect(3.5, 18.5, 17, 3, L(S, 0, 1.5)))]


@icon("channel-knife", CAT, "Small hooked blade tool beside a lemon with a long spiral peel hanging from it",
      tags=["citrus peel", "lemon twist", "zester", "garnish", "bartender", "cocktail garnish", "peeler"])
def _(S):
    return [shell(ellipse(9, 9.5, 6, 5)), line("M7 14.5C5.5 18 10.5 17.5 9 20.5"),
            line("M21.5 3L16.5 9.5"), line("M16.5 9.5L15 12.5")]


@icon("ice-pick", CAT, "Wooden handled steel spike stuck into a block of ice",
      tags=["ice chipper", "ice block", "bar tool", "bartender", "chip ice", "spike", "ice carving"])
def _(S):
    def tp(pts):
        c, sn = math.cos(math.radians(-30)), math.sin(math.radians(-30))
        return [(12 + (x - 12) * c - (y - 12) * sn, 12 + (x - 12) * sn + (y - 12) * c) for x, y in pts]
    handle = poly(tp([(10, 1.5), (14, 1.5), (14.8, 8.5), (9.2, 8.5)]), closed=True, r=S.r)
    spike = poly(tp([(12, 8.5), (12, 18.5)]))
    return [shell(handle), line(spike), shell(rect(3, 15.5, 18, 6, rr(S, 2.5)))]


@icon("lewis-bag", CAT, "Canvas drawstring bag standing next to a wooden mallet",
      tags=["ice bag", "crushing ice", "mallet", "bartender", "cocktail", "crushed ice", "muddler"])
def _(S):
    bag = poly([(3.5, 8.5), (12, 8.5), (13.5, 21), (2, 21)], closed=True, r=S.r)
    return [shell(bag), line("M5 5.5L7.7 8.5L10.5 5.5"), detail(seg(4.5, 12.5, 11, 12.5)),
            shell(rect(15.5, 3, 6.5, 5.5, rr(S, 1.5))), line(seg(18.8, 8.5, 18.8, 21))]


@icon("ice-crusher", CAT, "Hand crank ice crusher with a top hopper, a side crank handle and a bowl below",
      tags=["ice shaver", "crushed ice", "snow cone", "hand crank", "bar tool", "bartender", "shaved ice"])
def _(S):
    return [shell(poly([(4.5, 2.5), (17.5, 2.5), (14, 9), (8, 9)], closed=True, r=S.r)),
            shell(rect(6.5, 9.5, 9, 4.5, L(S, 0, 1.5))), line("M15.5 11.8H20V16"),
            shell("M4.5 17H17.5A6.5 4.5 0 0 1 4.5 17Z")]


@icon("ice-luge", CAT, "Tall ice block with a zigzag channel down its face and a glass at the bottom",
      tags=["ice sculpture", "drink luge", "wedding", "shots", "party", "vodka", "celebration"])
def _(S):
    return [shell(poly([(6, 2.5), (18, 2.5), (17, 15.5), (7, 15.5)], closed=True, r=S.r)),
            detail(poly([(10, 6), (14.5, 8.5), (9.5, 11), (13.5, 13.5)])),
            shell(poly([(8.5, 17.2), (15.5, 17.2), (14.5, 21.5), (9.5, 21.5)], closed=True, r=S.r))]


@icon("cocktail-smoker", CAT, "Glass covered by a small dome with smoke curling inside and a torch nozzle on top",
      tags=["smoked cocktail", "smoke infuser", "smoking gun", "mixology", "bartender", "wood smoke", "old fashioned"])
def _(S):
    top = union("M5.5 12A6.5 6 0 0 1 18.5 12Z", poly([(6, 11), (18, 11), (17, 21.5), (7, 21.5)], closed=True))
    return [shell(top), detail(seg(5.5, 12, 18.5, 12)), line(seg(12, 2.5, 12, 6)),
            line("M10 19.5C8.6 18 11.4 17 10 15.2"), line("M14 19.5C12.6 18 15.4 17 14 15.2")]


@icon("julep-strainer", CAT, "Round shallow perforated bowl with a short handle like a spoon full of holes",
      tags=["cocktail strainer", "bar tool", "bartender", "perforated", "mint julep", "mixology", "sieve"])
def _(S):
    return [shell(circle(9.5, 12, 6.5)), dot(9.5, 12, 1), dot(6.8, 9.6, 1), dot(12.2, 9.6, 1), dot(6.8, 14.4, 1),
            dot(12.2, 14.4, 1), line("M16 12H21.5")]


@icon("waiters-friend", CAT, "Folding corkscrew with a spiral worm, a hinged lever and a small blade on its handle",
      tags=["corkscrew", "wine key", "sommelier", "bottle opener", "cork puller", "wine opener", "server tool"])
def _(S):
    return [shell(rect(8.5, 2.5, 7, 12.5, rr(S, 3))), line("M15.5 8H19.5V4.5"), line(seg(8.5, 11, 4.5, 11)),
            line(poly([(12, 15), (9.3, 16.4), (14.7, 18), (9.3, 19.6), (12, 21.2)]))]


@icon("last-call-bell", CAT, "Bell hanging from a wall bracket with a short pull rope",
      tags=["bar bell", "pub bell", "closing time", "last orders", "ring bell", "tavern", "time gentlemen"])
def _(S):
    return [line("M3 3.5H12V6"), shell("M6.5 15C6.5 9.5 8.5 6 12 6S17.5 9.5 17.5 15Z"), line(seg(4.5, 15, 19.5, 15)),
            line(seg(12, 15.5, 12, 19.5)), dot(12, 20.6, 1.3)]


@icon("bottle-service", CAT, "Champagne bottle in an ice bucket with a sparkler fizzing from its neck",
      tags=["vip table", "nightclub", "champagne", "sparkler", "celebration", "ice bucket", "club"])
def _(S):
    bucket = union(poly([(5.5, 13.5), (18.5, 13.5), (17, 21.5), (7, 21.5)], closed=True, r=S.r),
                   poly([(10.5, 7.5), (13.5, 7.5), (13.5, 14), (10.5, 14)], closed=True))
    return [shell(bucket), line(seg(12, 2.5, 12, 5)), line(seg(8.2, 3.5, 10.2, 5.4)), line(seg(15.8, 3.5, 13.8, 5.4)),
            detail(seg(5.8, 16.5, 18.2, 16.5))]


@icon("beer-pitcher", CAT, "Straight sided jug with a handle, filled with beer and a bumpy foam head",
      tags=["pitcher of beer", "jug", "pub", "brewery", "lager", "draft", "sharing"])
def _(S):
    body = union(poly([(4.5, 7), (16, 7), (16, 21.5), (4.5, 21.5)], closed=True, r=S.r),
                 "M4.5 7.5C3.5 4.5 6.5 3 8 4.2C9 2.2 12 2.2 12.7 4.2C14.7 3.2 17.2 5 16 7.5Z")
    return [shell(body), detail(seg(4.5, 11.5, 16, 11.5)), line("M16 11H19.5A1.5 1.5 0 0 1 21 12.5V16.5A1.5 1.5 0 0 1 19.5 18H16")]


@icon("shot-tray", CAT, "Small tray with a row of shot glasses standing on it",
      tags=["shots", "shooters", "bar tray", "party", "tequila", "bartender", "serving tray"])
def _(S):
    parts = [shell(rect(2.5, 16.2, 19, 4.5, L(S, 0, 1.8)))]
    for x in (5.5, 12, 18.5):
        parts.append(shell(poly([(x - 1.8, 6), (x + 1.8, 6), (x + 1.4, 16.2), (x - 1.4, 16.2)], closed=True)))
    return parts


@icon("wine-dispenser", CAT, "Glass fronted cabinet holding three upright wine bottles with a tap under each",
      tags=["wine on tap", "wine preservation", "enomatic", "wine bar", "tasting", "pour by glass", "cabinet"])
def _(S):
    parts = [shell(rect(2.5, 2.5, 19, 19, rr(S, 3)))]
    for x in (7, 12, 17):
        parts.append(detail(small_bottle(x, 14.5, 10, 3)))
        parts.append(dot(x, 18, 1))
    return parts


@icon("beer-cask", CAT, "Wooden barrel lying on its side on a cradle with a tap in its end",
      tags=["keg", "firkin", "real ale", "cask ale", "pub", "brewery", "barrel"])
def _(S):
    body = "M4.5 5C2.5 8.5 2.5 12.5 4.5 16H17.5C19.5 12.5 19.5 8.5 17.5 5Z"
    return [shell(body), detail(seg(8.5, 5, 8.5, 16)), detail(seg(13.5, 5, 13.5, 16)),
            line("M19 10.5H21.5V14"), line("M3.5 19.5H18.5"), line(seg(6, 19.5, 6, 21.5)), line(seg(16, 19.5, 16, 21.5))]


# ============================================================================ chunk 5

@icon("beverage-tub", CAT, "Oval tub with two side handles filled with ice and several bottle necks sticking up",
      tags=["drinks tub", "ice bath", "party cooler", "galvanized", "beer bucket", "bottles on ice", "outdoor event"])
def _(S):
    tub = union(poly([(4, 11.5), (20, 11.5), (18, 21.5), (6, 21.5)], closed=True, r=S.r),
                small_bottle(7.5, 12.5, 8.5, 3), small_bottle(12, 12.5, 9.5, 3), small_bottle(16.5, 12.5, 8.5, 3))
    return [shell(tub), line("M4.6 14H2.5V17H5"), line("M19.4 14H21.5V17H19"), hole(circle(10, 17, 1)),
            hole(circle(14.5, 18.2, 1)), hole(circle(12.2, 15, 0.9))]


@icon("wine-barrel-table", CAT, "Upright wine barrel used as a standing table with two glasses on its round top",
      tags=["barrel table", "cocktail table", "standing table", "winery", "rustic", "high top", "vineyard"])
def _(S):
    body = "M6 8C4.5 12 4.5 17 6 21.5H18C19.5 17 19.5 12 18 8Z"
    return [shell(body), detail(seg(5, 12.5, 19, 12.5)), detail(seg(5, 17.5, 19, 17.5)),
            line("M8.5 3.5V8"), line("M15.5 3.5V8"), shell("M6.5 2.5H10.5C10.5 4.5 9.8 5.2 8.5 5.2S6.5 4.5 6.5 2.5Z"),
            shell("M13.5 2.5H17.5C17.5 4.5 16.8 5.2 15.5 5.2S13.5 4.5 13.5 2.5Z")]


@icon("humidor", CAT, "Wooden box with its lid propped open above a row of cigars and a round gauge on the lid",
      tags=["cigar box", "cigars", "tobacco", "lounge", "smoking room", "hygrometer", "cellar"])
def _(S):
    return [shell(poly([(5, 2.5), (19, 2.5), (20.5, 9.5), (3.5, 9.5)], closed=True, r=S.r)), hole(circle(12, 6, 1.5)),
            shell(rect(3, 11.5, 18, 10, rr(S, 2))), hole(rect(6, 13.8, 12, 2, 1)), hole(rect(6, 17.6, 12, 2, 1))]


@icon("mobile-bar", CAT, "Portable bar counter on small wheels with two bottles and a shaker on top",
      tags=["bar cart", "pop up bar", "event bar", "portable bar", "wedding bar", "catering", "cocktail bar"])
def _(S):
    return [shell(small_bottle(6, 11, 8, 3)), shell(small_bottle(10.5, 11, 6.5, 3)),
            shell(poly([(15, 5.5), (19.5, 5.5), (18.6, 11), (15.9, 11)], closed=True)), line(seg(15.7, 3.3, 18.8, 3.3)),
            shell(rect(3, 11, 18, 8.5, rr(S, 2))), detail(seg(3, 15.2, 21, 15.2)), dot(6, 21.2, 1), dot(18, 21.2, 1)]


@icon("nick-and-nora-glass", CAT, "Small stemmed cocktail glass with a rounded bowl that curves in slightly at the rim",
      tags=["coupe", "cocktail glass", "stemware", "bar", "bartender", "martini", "classic cocktail"])
def _(S):
    return [shell("M8 2.5C5.5 5 5.5 9.5 12 11.5C18.5 9.5 18.5 5 16 2.5Z"), line(seg(12, 11.5, 12, 21)),
            line(seg(8, 21, 16, 21))]


@icon("catering-van", CAT, "Side view of a boxy van with a food cloche on its side panel",
      tags=["food truck", "delivery van", "event catering", "caterer", "transport", "food delivery", "mobile kitchen"])
def _(S):
    body = poly([(2.5, 5), (14.5, 5), (14.5, 9.5), (19, 9.5), (21.5, 13), (21.5, 18), (2.5, 18)], closed=True, r=S.r)
    return [shell(body), hole("M5.2 14A3.4 3.6 0 0 1 12 14Z"), hole(rect(4.6, 14.3, 8, 1.2)),
            hole(poly([(16.6, 11.3), (18.4, 11.3), (19.7, 13.2), (16.6, 13.2)], closed=True)),
            dot(7, 19.5, 2), dot(17, 19.5, 2)]


@icon("insulated-food-carrier", CAT, "Boxy front loading insulated container with a latched door and molded side handles",
      tags=["hot box", "food transport", "catering", "cambro", "thermal carrier", "meal delivery", "event"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 18.5, rr(S, 3))), detail(rect(7.5, 5.5, 9, 12, L(S, 0, 1.5))),
            hole(rect(10.5, 9.5, 3, 2.6, 1)), line("M4.5 7.5H2.5V15H4.5"), line("M19.5 7.5H21.5V15H19.5")]


@icon("chafing-fuel-can", CAT, "Small round tin can with a flame rising from its open top",
      tags=["sterno", "chafing dish", "fuel", "buffet", "catering", "flame", "heat source"])
def _(S):
    return [shell("M12 2.5C14 5 16 6.5 16 9A4 4 0 0 1 8 9C8 6.5 10 5 12 2.5Z"), shell(rect(5.5, 13.5, 13, 8, rr(S, 4))),
            detail(seg(5.5, 16.5, 18.5, 16.5))]


@icon("canape-tray", CAT, "Hand held up with a round tray on it carrying small bite sized canapes",
      tags=["passed appetizers", "server", "cocktail party", "hors d'oeuvres", "waiter", "catering", "reception"])
def _(S):
    return [Part("dot", rect(5, 4.5, 3.4, 3.4, 0.8)), Part("dot", rect(10.3, 4.5, 3.4, 3.4, 0.8)),
            Part("dot", rect(15.6, 4.5, 3.4, 3.4, 0.8)), shell(rect(2.5, 9.2, 19, 2.3, L(S, 0, 1.1))),
            shell("M8.5 12.5H15.5V17C15.5 19.8 13.8 21.5 12 21.5S8.5 19.8 8.5 17Z"), line("M8.5 15L5.5 13.8")]


@icon("buffet-label", CAT, "Small tent card on a table with a name line and a row of tiny symbols below it",
      tags=["food label", "allergen card", "table tent", "menu card", "buffet sign", "catering", "dietary"])
def _(S):
    return [shell(poly([(5, 3.5), (19, 3.5), (21, 17), (3, 17)], closed=True, r=S.r)), detail(seg(8, 7.5, 16, 7.5)),
            dot(8.5, 12.7, 1), dot(12, 12.7, 1), dot(15.5, 12.7, 1), line(seg(2.5, 20.5, 21.5, 20.5))]


@icon("candy-buffet", CAT, "Two tall glass jars of sweets of different heights with lids",
      tags=["sweets table", "lolly buffet", "dessert table", "wedding candy", "jars", "sweet shop", "party"])
def _(S):
    return [shell(rect(3, 8.5, 8, 12.5, rr(S, 2))), line(seg(4.5, 5.5, 9.5, 5.5)), dot(7, 14.5, 1.1), dot(6, 18, 1.1),
            shell(rect(13, 4.5, 8, 16.5, rr(S, 2))), line(seg(14.5, 2.5, 19.5, 2.5)), dot(17, 12, 1.1), dot(16, 15.5, 1.1),
            dot(18, 18.2, 1.1)]


@icon("donut-wall", CAT, "Tall board with a grid of donuts hung on pegs and short feet",
      tags=["doughnut wall", "donut display", "wedding dessert", "party", "pegboard", "bakery", "sweet table"])
def _(S):
    return [shell(rect(3.5, 2.5, 17, 16.5, rr(S, 2.5))), detail(circle(8, 7.5, 2.3)), detail(circle(16, 7.5, 2.3)),
            detail(circle(8, 14, 2.3)), detail(circle(16, 14, 2.3)), line(seg(7, 19, 6, 21.5)), line(seg(17, 19, 18, 21.5))]


@icon("coffee-station", CAT, "Table with a tall urn with a tap, a stack of cups and a skirted leg set",
      tags=["coffee urn", "self serve", "break room", "catering", "conference", "coffee service", "meeting"])
def _(S):
    return [shell(rect(3, 3.5, 8, 13.5, rr(S, 2.5))), detail(seg(3, 8, 11, 8)), line("M11 13H13.5"),
            shell(poly([(14.5, 10), (20, 10), (19, 16), (15.5, 16)], closed=True, r=S.r * 0.5)),
            shell(rect(2, 17.5, 20, 2.5, L(S, 0, 1.2))), line(seg(4, 20, 4, 21.5)), line(seg(20, 20, 20, 21.5))]


@icon("registration-table", CAT, "Draped table with a small sign on a stand and name badges laid out in front",
      tags=["check in desk", "event desk", "sign in", "name tags", "conference", "reception", "welcome table"])
def _(S):
    return [shell(rect(8, 2.5, 8, 5, rr(S, 1.5))), line(seg(12, 7.5, 12, 11)),
            Part("dot", rect(3, 8.5, 3.2, 2, 0.5)), Part("dot", rect(17.8, 8.5, 3.2, 2, 0.5)),
            shell(rect(2.5, 11, 19, 2.8, L(S, 0, 1.2))), shell(poly([(3.5, 14), (20.5, 14), (21.5, 21.5), (2.5, 21.5)], closed=True)),
            detail(seg(8, 16, 7.6, 21.5)), detail(seg(12, 16, 12, 21.5)), detail(seg(16, 16, 16.4, 21.5))]


@icon("easel-sign", CAT, "Tall three legged easel holding a large sign board with lines of text",
      tags=["welcome sign", "standing sign", "wedding sign", "event signage", "a frame", "display stand", "menu board"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 11.5, rr(S, 1.5))), detail(seg(8, 6.5, 16, 6.5)), detail(seg(8, 10, 13.5, 10)),
            line(seg(8, 14, 5, 21.5)), line(seg(16, 14, 19, 21.5)), line(seg(12, 14, 12, 21.5))]


@icon("step-and-repeat", CAT, "Large banner backdrop on two stands with a repeating pattern of small marks",
      tags=["backdrop", "photo wall", "red carpet", "press wall", "event banner", "photo booth", "premiere"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 12.5, rr(S, 2))), dot(7, 6.2, 1), dot(12, 6.2, 1), dot(17, 6.2, 1),
            dot(9.5, 10.6, 1), dot(14.5, 10.6, 1), line(seg(6, 15, 6, 21)), line(seg(18, 15, 18, 21)),
            line(seg(3, 21.5, 9, 21.5)), line(seg(15, 21.5, 21, 21.5))]


@icon("card-box", CAT, "Gift shaped box with a slot in its lid and an envelope being dropped in",
      tags=["wedding card box", "card holder", "gift cards", "reception", "envelope", "party", "money box"])
def _(S):
    return [shell(rect(7.5, 2.5, 9, 5.5, rr(S, 1.5))), shell(rect(4.5, 14, 15, 7.5, rr(S, 4))),
            shell(rect(3, 9.2, 18, 4.5, rr(S, 4))), hole(rect(8.5, 10.8, 7, 1.3, 0.6))]


@icon("cake-topper", CAT, "Two small stick figures on picks standing on top of a single cake tier",
      tags=["wedding cake", "bride and groom", "couple", "celebration", "cake decoration", "figurines", "anniversary"])
def _(S):
    return [dot(8.2, 3.8, 1.6), line(seg(8.2, 5.5, 8.2, 13.5)), line(seg(5.8, 8, 10.6, 8)),
            dot(15.8, 3.8, 1.6), line(seg(15.8, 5.5, 15.8, 13.5)), line(seg(13.4, 8, 18.2, 8)),
            shell(rect(3, 13.5, 18, 8, rr(S, 2.5))), detail(seg(3, 17.5, 21, 17.5))]


@icon("chiavari-chair", CAT, "Slim chair with a ladder back of thin spindles and a row of thin spindles under the seat",
      tags=["ballroom chair", "wedding chair", "event seating", "banquet chair", "rental chair", "ladder back", "reception"])
def _(S):
    return [shell(rect(6, 2.5, 12, 8, L(S, 0, 2))), detail(seg(10, 2.5, 10, 10.5)), detail(seg(14, 2.5, 14, 10.5)),
            shell(rect(4, 11.5, 16, 3, L(S, 0, 1.2))), line(seg(6, 14.5, 6, 21.5)), line(seg(18, 14.5, 18, 21.5)),
            line(seg(10, 14.5, 10, 18)), line(seg(14, 14.5, 14, 18))]

