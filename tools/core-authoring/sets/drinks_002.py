"""TypeIcon Core: drinks (batch drinks_002).

Bottles, jugs, dispensers, beer and wine gear, barrels and stemware, drawn from the objects themselves.
Side views on a flat base; tall vessels are centred on x = 12.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, I, P, ST, U, fmt, path_to_d, rotation, transform_path  # noqa: F401

CAT = "drinks"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def blob(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


# ============================================================================ mugs, cups, bottles

@icon("root-beer-float", CAT, "Frosted mug with a scoop of ice cream on top and a straw",
      tags=["float", "ice cream soda", "soda float", "dessert drink", "mug", "straw"])
def _(S):
    return [
        shell(rect(4, 11, 10, 10, S.R)),
        line("M14 13.5h2a2.25 2.25 0 0 1 0 4.5h-2"),
        line(arc(9, 11, 4, 180, 360)),
        line(seg(11, 8.5, 15, 3)),
    ]


@icon("coconut-drink", CAT, "Coconut with the top cut off, a straw and a small umbrella",
      tags=["coconut", "tropical drink", "beach", "straw", "umbrella", "cocktail", "summer"])
def _(S):
    return [
        shell(poly([(5, 10), (5, 14), (8, 19.5), (12, 21), (16, 19.5), (19, 14), (19, 10)], closed=True, r=S.r + 2)),
        line(seg(15, 10, 18, 3)),
        shell("M3.5 7a3.25 3.25 0 0 1 6.5 0Z"),
        line(seg(6.75, 7, 6.75, 10)),
    ]


@icon("pineapple-drink", CAT, "Hollowed pineapple with its leafy crown pushed aside and a straw",
      tags=["pineapple", "tropical drink", "luau", "straw", "summer", "cocktail", "beach"])
def _(S):
    return [
        shell(rect(6, 10, 12, 11, L(S, 3, 5.5))),
        detail(seg(8.5, 18.5, 13.5, 12.5)),
        detail(seg(11.5, 19.5, 16, 14)),
        line(poly([(7, 8), (5, 5), (8, 5.5), (9, 3.5), (11, 7)], r=S.r * 0.5)),
        line(seg(15, 9.5, 18.5, 4)),
    ]


@icon("fountain-drink-cup", CAT, "Tall paper cup with a flat lid and a straw",
      tags=["soda cup", "fast food drink", "lid", "straw", "takeaway", "paper cup", "restaurant"])
def _(S):
    return [
        shell(poly([(5, 6), (19, 6), (19, 8.5), (5, 8.5)], closed=True, r=S.r * 0.4)),
        shell(poly([(6.5, 8.5), (17.5, 8.5), (16, 21), (8, 21)], closed=True, r=S.r)),
        detail(seg(7.3, 14, 16.7, 14)),
        line(seg(13, 6, 15.5, 2.5)),
    ]


@icon("party-cup", CAT, "Tapered plastic party cup with ridges near the rim and the base",
      tags=["plastic cup", "red cup", "party", "disposable", "tumbler", "drinks"])
def _(S):
    return [
        shell(poly([(5, 4), (19, 4), (16.5, 21), (7.5, 21)], closed=True, r=S.r)),
        detail(seg(5.6, 8, 18.4, 8)),
        detail(seg(6.9, 16.5, 17.1, 16.5)),
    ]


@icon("water-bottle", CAT, "Reusable metal water bottle with a narrow neck and a cap with a carry loop",
      tags=["reusable bottle", "flask", "hydration", "steel bottle", "gym", "hiking", "eco"])
def _(S):
    return [
        shell(poly([(10, 4), (14, 4), (14, 8.5), (17, 11), (17, 21), (7, 21), (7, 11), (10, 8.5)], closed=True, r=S.r)),
        detail(seg(7, 16, 17, 16)),
        detail(seg(10, 6.5, 14, 6.5)),
        line(poly([(14, 4.5), (17.5, 4.5), (17.5, 7.5)], r=S.r)),
    ]


@icon("plastic-water-bottle", CAT, "Disposable plastic bottle with a label band and a small cap",
      tags=["pet bottle", "bottled water", "disposable", "drink", "label", "cap", "single use"])
def _(S):
    return [
        shell(rect(10, 2.5, 4, 3, L(S, 0.5, 1.5))),
        shell(poly([(10.5, 5.5), (13.5, 5.5), (13.5, 8), (17, 11), (17, 21), (7, 21), (7, 11), (10.5, 8)], closed=True, r=S.r)),
        detail(seg(7, 13.5, 17, 13.5)),
        detail(seg(7, 17.5, 17, 17.5)),
    ]


@icon("sports-bottle", CAT, "Squeezable sports bottle with a pull-up nozzle cap and a pinched grip",
      tags=["squeeze bottle", "cycling bottle", "gym bottle", "nozzle", "hydration", "running", "fitness"])
def _(S):
    return [
        shell(poly([(8, 9.5), (16, 9.5), (14.5, 15.5), (16, 21), (8, 21), (9.5, 15.5)], closed=True, r=S.r)),
        shell(rect(9, 6.5, 6, 3, L(S, 0.5, 1.5))),
        line(poly([(10.5, 6.5), (10.5, 3.5), (13.5, 3.5), (13.5, 6.5)], r=S.r * 0.5)),
    ]


@icon("shaker-bottle", CAT, "Protein shaker bottle with a flip spout cap and a wire mixing ball inside",
      tags=["protein shaker", "gym", "mixing ball", "fitness", "supplement", "shake"])
def _(S):
    return [
        shell(poly([(8, 5.5), (16, 5.5), (16, 8), (17, 9.5), (17, 21), (7, 21), (7, 9.5), (8, 8)], closed=True, r=S.r)),
        detail(seg(8, 8, 16, 8)),
        line(seg(12, 5.5, 12, 2.5)),
        detail(circle(12, 15, 2.5)),
    ]


@icon("water-jug", CAT, "Large five gallon water jug with a narrow neck and a grip loop",
      tags=["water jug", "five gallon", "office water", "bulk water", "bottled water", "camping", "container"])
def _(S):
    return [
        shell(poly([(9, 3), (13, 3), (13, 5.5), (17, 8.5), (17, 21), (5, 21), (5, 8.5), (9, 5.5)], closed=True, r=S.r)),
        line(poly([(17, 11), (20, 11), (20, 16), (17, 16)], r=S.r)),
        detail(seg(5, 13.5, 17, 13.5)),
    ]


@icon("water-cooler", CAT, "Floor water dispenser with an upside-down jug on top and two taps",
      tags=["water dispenser", "office", "watercooler", "jug", "drinking water", "taps", "hot and cold"])
def _(S):
    return [
        shell(poly([(7, 2.5), (17, 2.5), (17, 6), (14, 8), (10, 8), (7, 6)], closed=True, r=S.r)),
        shell(rect(6.5, 9, 11, 12.5, S.R)),
        blob(9, 12, 4, 2),
        blob(9, 15.5, 4, 2),
        detail(seg(9, 19, 15, 19)),
    ]


@icon("water-filter-pitcher", CAT, "Pitcher with a filter cartridge in its top reservoir and a flip lid",
      tags=["filter jug", "purifier", "drinking water", "pitcher", "kitchen", "filtration"])
def _(S):
    return [
        shell(rect(4, 7, 12, 14, S.R)),
        line(poly([(16, 10), (20, 10), (20, 17), (16, 17)], r=S.r)),
        line(poly([(4, 4.5), (16, 4.5)])),
        detail(rect(8, 10.5, 4, 5, 1)),
        line(poly([(4, 7.5), (2.5, 4.5)])),
    ]


@icon("infused-water-bottle", CAT, "Clear bottle with a central infuser tube holding fruit slices",
      tags=["fruit infuser", "detox water", "flavored water", "hydration", "lemon water", "sports", "bottle"])
def _(S):
    return [
        shell(poly([(9, 3), (15, 3), (15, 6), (18, 8.5), (18, 21), (6, 21), (6, 8.5), (9, 6)], closed=True, r=S.r)),
        detail(rect(10, 9, 4, 8, L(S, 0.5, 2))),
        dot(12, 12, 1),
        dot(12, 15, 1),
    ]


@icon("water-carafe", CAT, "Glass carafe with a tumbler turned upside down over its neck",
      tags=["carafe", "bedside water", "glass", "pitcher", "tumbler", "water", "decanter"])
def _(S):
    return [
        shell("M10 8V10C10 12 6 13 6 16.5C6 19.5 8.5 21 12 21C15.5 21 18 19.5 18 16.5C18 13 14 12 14 10V8Z"),
        shell(poly([(9, 3), (15, 3), (16, 8), (8, 8)], closed=True, r=S.r * 0.5)),
    ]


@icon("water-canteen", CAT, "Round flat canteen with a cover, a strap loop and a screw cap",
      tags=["canteen", "camping", "hiking", "military", "flask", "outdoors", "water bottle"])
def _(S):
    return [
        shell(rect(10, 2.5, 4, 3.5, L(S, 0.5, 1.5))),
        shell(circle(12, 14, 7.5)),
        detail(circle(12, 14, 3.5)),
        line(poly([(14, 4.5), (18, 4.5), (19.5, 8)], r=S.r)),
    ]


@icon("bottle-refill-station", CAT, "Wall mounted refill station with a spout filling a bottle underneath",
      tags=["water fountain", "refill", "bottle filler", "drinking fountain", "school", "gym", "sensor spout"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 7, S.R)),
        dot(8, 6, 1),
        line(seg(12, 9.5, 12, 13)),
        shell(poly([(10.5, 14.5), (13.5, 14.5), (13.5, 16), (16, 17.5), (16, 21.5), (8, 21.5), (8, 17.5), (10.5, 16)], closed=True, r=S.r * 0.6)),
    ]


@icon("soda-siphon", CAT, "Glass seltzer siphon with a metal head, a squeeze lever and a curved spout",
      tags=["seltzer bottle", "seltzer", "club soda", "carbonated water", "bar", "vintage", "sparkling"])
def _(S):
    return [
        shell(poly([(9.5, 9.5), (13.5, 9.5), (13.5, 11), (16.5, 13), (16.5, 21), (6.5, 21), (6.5, 13), (9.5, 11)], closed=True, r=S.r)),
        shell(rect(8.5, 4, 6, 5.5, L(S, 0.5, 1.5))),
        line(poly([(14.5, 5.5), (19, 4)], r=0)),
        line(poly([(14.5, 8), (18.5, 8), (18.5, 11)], r=S.r)),
    ]


@icon("soda-maker", CAT, "Countertop carbonation machine with a bottle clipped under its head",
      tags=["sparkling water maker", "carbonator", "seltzer machine", "fizzy water", "kitchen", "appliance", "co2"])
def _(S):
    return [
        shell(poly([(3.5, 3), (20, 3), (20, 21), (14.5, 21), (14.5, 8), (3.5, 8)], closed=True, r=S.r)),
        shell(poly([(6.5, 8.5), (9.5, 8.5), (9.5, 11), (11, 12.5), (11, 21), (5, 21), (5, 12.5), (6.5, 11)], closed=True, r=S.r * 0.6)),
        dot(17, 12, 1.2),
    ]


@icon("two-liter-bottle", CAT, "Large plastic soda bottle with a label band and a lobed foot",
      tags=["soda bottle", "family size", "pop", "cola", "big bottle", "party", "plastic"])
def _(S):
    return [
        shell(rect(10, 2.5, 4, 2.5, L(S, 0.5, 1))),
        shell(poly([(10.5, 5), (13.5, 5), (13.5, 7), (17, 10), (17, 19.5), (15.5, 21.5), (13.5, 21.5), (12, 20), (10.5, 21.5), (8.5, 21.5), (7, 19.5), (7, 10), (10.5, 7)], closed=True, r=S.r * 0.7)),
        detail(seg(7, 11.5, 17, 11.5)),
        detail(seg(7, 16.5, 17, 16.5)),
        dot(12, 14, 1.2),
    ]


@icon("soda-fountain", CAT, "Drink dispenser with a row of nozzles and a cup under one of them",
      tags=["fountain drink", "self serve", "soda dispenser", "restaurant", "fast food", "beverage station", "cup"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 8.5, S.R)),
        dot(7, 6.75, 1.1),
        dot(12, 6.75, 1.1),
        dot(17, 6.75, 1.1),
        line(seg(7, 11, 7, 14.5)),
        line(seg(12, 11, 12, 14.5)),
        line(seg(17, 11, 17, 14.5)),
        shell(poly([(8.5, 17), (15.5, 17), (14.5, 21.5), (9.5, 21.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("slush-machine", CAT, "Frozen drink machine with two clear tanks on top and a tap under each",
      tags=["slushie machine", "granita", "frozen drink", "convenience store", "dispenser", "ice"])
def _(S):
    return [
        shell(rect(3, 11, 18, 10.5, S.R)),
        shell(rect(3.5, 2.5, 7, 8.5, L(S, 1, 2.5))),
        shell(rect(13.5, 2.5, 7, 8.5, L(S, 1, 2.5))),
        detail("M5.25 6.5q1.25-1.5 2.5 0t2.5 0"),
        blob(5.5, 14.5, 3, 2.5),
        blob(15.5, 14.5, 3, 2.5),
    ]


@icon("drink-pouch", CAT, "Flat stand-up drink pouch with a straw poked in at the top corner",
      tags=["juice pouch", "kids drink", "lunchbox", "straw", "pouch", "packaged drink"])
def _(S):
    return [
        shell(rect(5, 6.5, 14, 15, S.R)),
        detail(seg(6, 10, 18, 10)),
        line(seg(15.5, 6.5, 18.5, 2.5)),
        detail(circle(12, 15.5, 2.5)),
    ]


@icon("milk-bottle", CAT, "Glass milk bottle with a wide mouth, a foil cap and milk filling most of it",
      tags=["milk", "dairy", "milkman", "glass bottle", "farm", "breakfast", "cream"])
def _(S):
    return [
        shell(poly([(9, 3.5), (15, 3.5), (15, 6), (17, 9), (17, 21), (7, 21), (7, 9), (9, 6)], closed=True, r=S.r)),
        detail(seg(9, 6, 15, 6)),
        detail(seg(7, 11.5, 17, 11.5)),
    ]


@icon("milk-churn", CAT, "Tall dairy milk churn with a wide shoulder, a lid and side handles",
      tags=["milk can", "dairy", "farm", "churn", "milk pail", "rural", "cream can"])
def _(S):
    return [
        shell(poly([(9.5, 5.5), (14.5, 5.5), (14.5, 7.5), (17, 10), (17, 19), (18.5, 21.5), (5.5, 21.5), (7, 19), (7, 10), (9.5, 7.5)], closed=True, r=S.r * 0.6)),
        shell(rect(9, 2.5, 6, 3, L(S, 0.5, 1.5))),
        line(poly([(7, 10.5), (3.5, 10.5), (3.5, 14), (7, 14)], r=S.r * 0.5)),
        line(poly([(17, 10.5), (20.5, 10.5), (20.5, 14), (17, 14)], r=S.r * 0.5)),
        detail(seg(7, 17, 17, 17)),
    ]


@icon("beverage-dispenser", CAT, "Glass drink jar with a lid on a stand and a spigot tap",
      tags=["agua fresca", "lemonade dispenser", "party drinks", "buffet", "spigot", "jar", "cold drink"])
def _(S):
    return [
        shell(rect(5, 5.5, 14, 11.5, S.R)),
        shell(rect(8, 2.5, 8, 3, L(S, 0.5, 1.5))),
        shell(rect(6, 19, 12, 2, L(S, 0.5, 1))),
        detail(seg(5, 10, 19, 10)),
        line(poly([(19, 13.5), (21, 13.5), (21, 16.5)], r=S.r * 0.5)),
    ]


@icon("drink-pitcher", CAT, "Tall pitcher with a pinched spout and a large loop handle, filled halfway",
      tags=["jug", "lemonade", "water pitcher", "juice", "serving", "sangria", "jar"])
def _(S):
    return [
        shell(poly([(3.5, 3.5), (6.5, 5.5), (6.5, 21), (15.5, 21), (15.5, 3.5)], closed=True, r=S.r)),
        line(poly([(15.5, 6.5), (19.5, 6.5), (19.5, 17), (15.5, 17)], r=S.r)),
        detail(seg(6.5, 12, 15.5, 12)),
    ]


@icon("lemonade-stand", CAT, "Small booth with a striped awning and a lemon slice on the front",
      tags=["lemonade", "kids business", "summer", "street vendor", "market stall", "booth", "kiosk"])
def _(S):
    return [
        shell(poly([(3, 9), (5, 3.5), (19, 3.5), (21, 9)], closed=True, r=S.r * 0.5)),
        detail(seg(9.3, 3.5, 8.3, 9)),
        detail(seg(14.7, 3.5, 15.7, 9)),
        line(seg(6, 9, 6, 13.5)),
        line(seg(18, 9, 18, 13.5)),
        shell(rect(4, 13.5, 16, 8, L(S, 1, 2))),
        detail(circle(12, 17.5, 2)),
    ]


@icon("cooler-box", CAT, "Lidded cooler box with a swing handle across the top",
      tags=["ice chest", "picnic", "camping", "beach", "cold storage", "tailgate"])
def _(S):
    return [
        shell(rect(3, 8, 18, 13, S.R)),
        detail(seg(3, 12, 21, 12)),
        line(poly([(8, 8), (8, 4.5), (16, 4.5), (16, 8)], r=S.r)),
        blob(10.5, 15, 3, 2),
    ]


@icon("can-cooler", CAT, "Foam sleeve wrapped around a drink can with the can top showing",
      tags=["beer sleeve", "can holder", "insulator", "drink sleeve", "party", "foam"])
def _(S):
    return [
        shell(poly([(8, 3), (16, 3), (17.5, 5), (17.5, 21), (6.5, 21), (6.5, 5)], closed=True, r=S.r * 0.6)),
        detail(seg(6.5, 9.5, 17.5, 9.5)),
        detail(seg(6.5, 17.5, 17.5, 17.5)),
    ]


@icon("pilsner-glass", CAT, "Tall slender beer glass that flares wide at the top with a foam head",
      tags=["beer glass", "lager", "pilsner", "pint", "bar", "brewery", "foam"])
def _(S):
    return [
        shell(poly([(6.5, 3.5), (17.5, 3.5), (13.5, 17), (10.5, 17)], closed=True, r=S.r)),
        detail("M7.6 7.5q1.6 1.4 3.2 0t3.2 0t2.3 .7"),
        line(seg(12, 17, 12, 20.5)),
        line(seg(8.5, 20.5, 15.5, 20.5)),
    ]


# ============================================================================ beer

@icon("weizen-glass", CAT, "Tall vase-shaped wheat beer glass, narrow at the base and curving out to a foam head",
      tags=["wheat beer", "hefeweizen", "weissbier", "german beer", "beer glass", "foam", "brewery"])
def _(S):
    return [
        shell("M10 21H14C14 16 18 13 18 3.5H6C6 13 10 16 10 21Z"),
        detail("M7 7q1.7 1.5 3.4 0t3.4 0t3.2 .5"),
    ]


@icon("snifter", CAT, "Short stemmed brandy glass with a wide round bowl, a narrow rim and a little amber liquid",
      tags=["brandy glass", "cognac", "whiskey", "liquor", "spirits", "after dinner drink", "bar"])
def _(S):
    return [
        shell("M9 5C4.5 8 4.5 15 9 17H15C19.5 15 19.5 8 15 5Z"),
        detail(seg(5.6, 12.5, 18.4, 12.5)),
        line(seg(12, 17, 12, 20.5)),
        line(seg(8, 20.5, 16, 20.5)),
    ]


@icon("beer-flight", CAT, "Wooden paddle holding a row of small tasting glasses",
      tags=["tasting flight", "sampler", "beer tasting", "brewery", "taproom", "paddle", "samples"])
def _(S):
    return [
        shell(rect(2, 17.5, 20, 4, L(S, 1, 2))),
        shell(rect(3, 7.5, 4, 8.5, L(S, 0.5, 1.5))),
        shell(rect(10, 7.5, 4, 8.5, L(S, 0.5, 1.5))),
        shell(rect(17, 7.5, 4, 8.5, L(S, 0.5, 1.5))),
    ]


@icon("beer-tap", CAT, "Bar faucet with a tall tap handle and a drop falling from the spout",
      tags=["draft beer", "draught", "faucet", "bar", "pub", "pour", "tap handle"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 3, 7.5, L(S, 0.5, 1.5))),
        shell(poly([(3.5, 10), (19, 10), (19, 13), (18, 13), (18, 16.5), (14, 16.5), (14, 13), (3.5, 13)], closed=True, r=S.r * 0.5)),
        dot(16, 20, 1.4),
    ]


@icon("beer-hand-pump", CAT, "Bar hand pull with a long tilted handle, a pump column and a swan neck spout",
      tags=["cask ale", "hand pull", "real ale", "pub", "bar pump", "beer engine", "british pub"])
def _(S):
    return [
        shell(poly([(12.5, 2.5), (15.5, 4.5), (11, 11), (8, 9)], closed=True, r=S.r * 0.8)),
        line(seg(9.5, 10.5, 8, 15)),
        shell(rect(5, 15, 6, 6.5, L(S, 1, 2))),
        line("M11 18h5a2.5 2.5 0 0 1 2.5 2.5v1.5"),
    ]


@icon("beer-tower", CAT, "Tall clear tube tower filled with beer on a base with a tap",
      tags=["table tap", "beer dispenser", "party beer", "tap tower", "pub", "draft", "tube"])
def _(S):
    return [
        shell(rect(8, 2.5, 8, 14.5, L(S, 1.5, 3))),
        shell(rect(5, 17, 14, 4.5, L(S, 1, 2))),
        detail("M9.5 6.5q1.25 1.3 2.5 0t2.5 0"),
        line(poly([(16, 12), (19.5, 12), (19.5, 14.5)], r=S.r * 0.5)),
    ]


@icon("keg", CAT, "Metal beer keg with ridged bands and a coupler valve on top",
      tags=["beer keg", "barrel", "brewery", "draft", "party", "pub", "cask"])
def _(S):
    return [
        shell(rect(9.5, 2.5, 5, 4.5, L(S, 0.5, 1.5))),
        shell(rect(5, 7, 14, 14.5, L(S, 2, 3.5))),
        detail(seg(5, 10.5, 19, 10.5)),
        detail(seg(5, 18, 19, 18)),
    ]


@icon("growler", CAT, "Round shouldered jug with a finger loop at the neck and a screw cap",
      tags=["beer jug", "takeaway beer", "refill", "craft beer", "brewery", "glass jug", "taproom"])
def _(S):
    return [
        shell("M9.5 5.5H14.5V7.5C18.5 9 18 10.5 18 13V19a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V13C6 10.5 5.5 9 9.5 7.5Z"),
        shell(rect(9, 2.5, 6, 3, L(S, 0.5, 1.5))),
        line("M9.5 7.5H7a2 2 0 0 0-2 2v2"),
        detail(seg(6, 15, 18, 15)),
    ]


@icon("six-pack", CAT, "Cardboard carrier with a centre handle holding six bottles, necks showing",
      tags=["beer carrier", "bottle pack", "beer", "soda", "takeaway", "carrier", "bottles"])
def _(S):
    return [
        shell(rect(3, 12, 18, 9.5, L(S, 1, 2.5))),
        line(poly([(9, 12), (9, 4.5), (15, 4.5), (15, 12)], r=S.r)),
        line(seg(5, 6.5, 5, 12)),
        line(seg(19, 6.5, 19, 12)),
        detail(circle(7, 16.75, 1.6)),
        detail(circle(12, 16.75, 1.6)),
        detail(circle(17, 16.75, 1.6)),
    ]


def _scallop(n, r_out, r_in, cx=12.0, cy=12.0):
    pts = []
    for i in range(n * 2):
        a = math.radians(-90 + i * 180 / n)
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


@icon("bottle-cap", CAT, "Crown bottle cap with a crimped fluted edge",
      tags=["crown cap", "beer cap", "soda cap", "bottle top", "crimped", "bottle", "recycling"])
def _(S):
    return [
        shell(poly(_scallop(10, 9.5, 7.8, 12, 12), closed=True, r=S.r * 0.7)),
        detail(circle(12, 12, 4.5)),
    ]


@icon("beer-boot", CAT, "Glass boot shaped mug filled with beer and topped with foam",
      tags=["das boot", "oktoberfest", "german beer", "drinking game", "novelty glass", "foam", "stein"])
def _(S):
    return [
        shell(poly([(6.5, 3), (14.5, 3), (14.5, 13), (19.5, 14.5), (21, 17), (21, 21), (6.5, 21)], closed=True, r=S.r)),
        detail("M7.5 7q1.4 1.4 2.8 0t2.8 0"),
    ]


@icon("yard-glass", CAT, "Very long thin glass with a round bulb at the bottom and a wide trumpet top",
      tags=["yard of ale", "long glass", "drinking challenge", "pub", "beer", "novelty", "trumpet glass"])
def _(S):
    return [
        shell("M7.5 2.5H16.5C14 7 13.5 10 13.5 13.5A4 4 0 1 1 10.5 13.5C10.5 10 10 7 7.5 2.5Z"),
        detail(seg(10.6, 10.5, 13.4, 10.5)),
    ]


@icon("beer-pong", CAT, "Triangle of party cups with a small ball bouncing toward them",
      tags=["party game", "drinking game", "college", "red cups", "ping pong ball", "cups", "game"])
def _(S):
    return [
        shell(poly([(2.5, 13), (10.5, 13), (9.5, 21), (3.5, 21)], closed=True, r=S.r * 0.5)),
        shell(poly([(13.5, 13), (21.5, 13), (20.5, 21), (14.5, 21)], closed=True, r=S.r * 0.5)),
        shell(poly([(8, 4), (16, 4), (15, 12), (9, 12)], closed=True, r=S.r * 0.5)),
        dot(20, 6, 1.6),
    ]


@icon("hop-cone", CAT, "Single hop flower cone made of overlapping scales with a leaf at the stem",
      tags=["hops", "beer ingredient", "brewing", "craft beer", "ipa", "humulus", "brewery"])
def _(S):
    return [
        shell("M12 7C18.5 8.5 19 14 12 21.5C5 14 5.5 8.5 12 7Z"),
        detail(poly([(8, 11.5), (12, 14.5), (16, 11.5)], r=S.r * 0.5)),
        detail(poly([(9, 16), (12, 18.5), (15, 16)], r=S.r * 0.5)),
        shell("M12 5C13 2.8 16 2.3 18.5 3.2C17.5 5.3 14 5.8 12 5Z"),
    ]


# ============================================================================ wine and spirits making

@icon("carboy", CAT, "Large glass fermenting jug with a stopper and an S shaped airlock",
      tags=["fermenter", "homebrew", "demijohn", "airlock", "winemaking", "brewing", "glass jug"])
def _(S):
    return [
        shell("M9.5 7H14.5V9C19 10.5 19 13 19 15V18a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3V15C5 13 5 10.5 9.5 9Z"),
        shell(rect(10, 4.5, 4, 2.5, L(S, 0.5, 1))),
        line(poly([(12, 4.5), (12, 3), (16.5, 3), (16.5, 5.5)], r=S.r * 0.5)),
        detail(seg(5, 14.5, 19, 14.5)),
    ]


@icon("conical-fermenter", CAT, "Steel tank with a cone bottom on legs and a valve at the tip",
      tags=["homebrew", "brewery", "fermentation", "tank", "beer making", "steel", "cone"])
def _(S):
    return [
        shell(poly([(6, 4), (18, 4), (18, 12.5), (12.8, 18), (11.2, 18), (6, 12.5)], closed=True, r=S.r)),
        detail(seg(6, 8, 18, 8)),
        line(seg(6.5, 12, 4.5, 21.5)),
        line(seg(17.5, 12, 19.5, 21.5)),
        line(seg(12, 18, 12, 21.5)),
    ]


@icon("brew-kettle", CAT, "Large steel pot with a ball valve near the bottom and a dial thermometer",
      tags=["brewing", "homebrew", "boil kettle", "stockpot", "thermometer", "brewery", "beer making"])
def _(S):
    return [
        shell(rect(5, 8, 13, 12.5, L(S, 2, 3.5))),
        line("M5 8Q11.5 2.5 18 8"),
        detail(seg(9, 11, 9, 15.5)),
        dot(9, 18, 1.2),
        line(poly([(5, 11), (2.5, 11), (2.5, 14)], r=S.r * 0.5)),
        line(seg(18, 18, 21.5, 18)),
        line(seg(21.5, 15.5, 21.5, 20.5)),
    ]


@icon("wine-barrel", CAT, "Wooden wine barrel lying on its side with metal hoops and a bung on top",
      tags=["oak barrel", "cask", "winery", "cellar", "aging", "whiskey barrel", "wood"])
def _(S):
    return [
        shell(L(S, "M3.5 7C8 3.5 16 3.5 20.5 7V17C16 20.5 8 20.5 3.5 17Z", "M4.5 8C8.5 3.5 15.5 3.5 19.5 8V16C15.5 20.5 8.5 20.5 4.5 16Z")),
        detail(seg(8, 5.3, 8, 18.7)),
        detail(seg(16, 5.3, 16, 18.7)),
    ]


@icon("sake-barrel", CAT, "Straw wrapped sake barrel with rope ties and a wooden lid",
      tags=["komodaru", "japanese", "rice wine", "festival", "cask", "kagami biraki", "barrel"])
def _(S):
    return [
        shell("M5 6.5C4 10 4 16 5 19.5H19C20 16 20 10 19 6.5Z"),
        shell(ellipse(12, 6, L(S, 7, 6.2), L(S, 2.6, 3))),
        detail(seg(4.3, 11.5, 19.7, 11.5)),
        detail(seg(4.3, 16, 19.7, 16)),
    ]


@icon("wine-press", CAT, "Wooden slatted basket press with a screw and a crank on top",
      tags=["grape press", "winemaking", "cider press", "vineyard", "pressing", "harvest", "basket press"])
def _(S):
    return [
        shell("M6 10C4.5 13 4.5 18 6 21H18C19.5 18 19.5 13 18 10Z"),
        detail(seg(10, 10, 10, 21)),
        detail(seg(14, 10, 14, 21)),
        line(seg(12, 8, 12, 4)),
        line(seg(7, 4, 17, 4)),
    ]


@icon("pot-still", CAT, "Copper pot still with a round pot, a swan neck and a coil condenser beside it",
      tags=["distillery", "moonshine", "whiskey still", "distilling", "copper", "spirits", "alembic"])
def _(S):
    return [
        shell(circle(8, 16, 5.5)),
        line("M8 10.5V7C8 4 10.5 3.5 12 3.5H17.5V5.5"),
        shell(rect(14.5, 5.5, 6, 15.5, L(S, 1.5, 2.5))),
        detail(seg(16, 10, 19.5, 10)),
        detail(seg(16, 14, 19.5, 14)),
        detail(seg(16, 18, 19.5, 18)),
    ]


@icon("champagne-flute", CAT, "Tall narrow flute glass on a thin stem with bubbles rising",
      tags=["sparkling wine", "toast", "prosecco", "celebration", "bubbles", "wedding", "new year"])
def _(S):
    return [
        shell("M9 3H15C15 8 14 12 12 13.5C10 12 9 8 9 3Z"),
        line(seg(12, 13.5, 12, 20.5)),
        line(seg(8.5, 20.5, 15.5, 20.5)),
        dot(11.3, 9, 0.9),
        dot(13, 6.5, 0.9),
    ]


@icon("coupe-glass", CAT, "Shallow wide saucer glass on a stem",
      tags=["champagne coupe", "cocktail glass", "vintage", "martini", "stemware", "bar", "retro"])
def _(S):
    return [
        shell("M4.5 5H19.5C19.5 10.5 16 13.5 12 13.5C8 13.5 4.5 10.5 4.5 5Z"),
        detail(seg(5.6, 8.5, 18.4, 8.5)),
        line(seg(12, 13.5, 12, 20.5)),
        line(seg(8, 20.5, 16, 20.5)),
    ]


@icon("champagne-tower", CAT, "Pyramid of coupe glasses stacked in three rows",
      tags=["champagne pyramid", "wedding", "celebration", "coupes", "toast", "party", "stemware"])
def _(S):
    bowls = [(12, 4)] + [(8.5, 10), (15.5, 10)] + [(5, 16), (12, 16), (19, 16)]
    parts = [shell(f"M{fmt(x - 2.5)} {fmt(y)}H{fmt(x + 2.5)}a2.5 2.5 0 0 1 -5 0Z") for x, y in bowls]
    parts.append(line(seg(3, 21.5, 21, 21.5)))
    return parts


@icon("wine-decanter", CAT, "Wide low bellied glass decanter with a long narrow neck",
      tags=["wine", "aerating", "carafe", "dinner", "sommelier", "red wine", "crystal"])
def _(S):
    return [
        shell(L(S, "M10 3H14V10C14 11 19 13.5 19 17C19 20 17 21 15 21H9C7 21 5 20 5 17C5 13.5 10 11 10 10Z",
                "M10.5 3H13.5V10C13.5 11 18 13 18 16.5C18 20 16.5 21 15 21H9C7.5 21 6 20 6 16.5C6 13 10.5 11 10.5 10Z")),
        detail(seg(5.4, 16.5, 18.6, 16.5)),
    ]


@icon("whiskey-decanter", CAT, "Square cut crystal decanter with a round ball stopper",
      tags=["liquor decanter", "scotch", "bourbon", "crystal", "spirits", "bar", "cut glass"])
def _(S):
    return [
        shell(poly([(9, 7.5), (15, 7.5), (15, 9), (19, 11.5), (19, 21), (5, 21), (5, 11.5), (9, 9)], closed=True, r=S.r)),
        shell(circle(12, 4.6, 2)),
        detail(seg(6.5, 18, 9.5, 15)),
        detail(seg(14.5, 19, 17.5, 16)),
    ]


def _cork_pts(cx, cy, length, width, deg):
    a = math.radians(deg)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    h, w = length / 2, width / 2
    return [(cx + ux * h + nx * w, cy + uy * h + ny * w), (cx + ux * h - nx * w, cy + uy * h - ny * w),
            (cx - ux * h - nx * w, cy - uy * h - ny * w), (cx - ux * h + nx * w, cy - uy * h + ny * w)]


@icon("wine-cork", CAT, "Cylindrical wine cork shown at an angle with a stained end",
      tags=["cork", "stopper", "wine bottle", "sommelier", "corked wine", "bottle closure", "cellar"])
def _(S):
    c = _cork_pts(12, 12, 15, 7, -45)
    mid = _cork_pts(12, 12, 10, 7, -45)
    return [
        shell(poly(c, closed=True, r=S.r * 0.6)),
        detail(seg(mid[0][0], mid[0][1], mid[1][0], mid[1][1])),
    ]


@icon("wine-rack", CAT, "Wooden wine rack with diamond cells and bottle ends showing",
      tags=["wine storage", "cellar", "bottles", "lattice", "shelf", "sommelier", "home bar"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, L(S, 1.5, 3))),
        detail(poly([(12, 3), (21, 12), (12, 21), (3, 12)], closed=True)),
        detail(circle(12, 12, 2.3)),
    ]


@icon("wine-fridge", CAT, "Tall glass door cabinet with bottles lying on its shelves",
      tags=["wine cooler", "wine cabinet", "cellar", "bottle storage", "beverage fridge", "appliance", "sommelier"])
def _(S):
    parts = [shell(rect(4.5, 2.5, 15, 19, L(S, 2, 3.5))),
             detail(seg(4.5, 8.5, 19.5, 8.5)),
             detail(seg(4.5, 14.5, 19.5, 14.5))]
    for y in (5.5, 11.5, 18):
        for x in (8.5, 12, 15.5):
            parts.append(dot(x, y, 1.1))
    return parts


@icon("ice-bucket", CAT, "Metal bucket with side handles and ice cubes on top",
      tags=["champagne bucket", "wine cooler", "chiller", "ice", "party", "bar", "cooler bucket"])
def _(S):
    return [
        shell(poly([(5, 10.5), (19, 10.5), (17.5, 21), (6.5, 21)], closed=True, r=S.r)),
        line(poly([(5.3, 12.5), (2.5, 12.5), (2.5, 15)], r=S.r * 0.5)),
        line(poly([(18.7, 12.5), (21.5, 12.5), (21.5, 15)], r=S.r * 0.5)),
        shell(rect(7, 4.5, 4.5, 4, L(S, 0.5, 1.25))),
        shell(rect(13, 5, 4.5, 4, L(S, 0.5, 1.25))),
    ]


@icon("sake-set", CAT, "Small narrow necked flask beside a tiny round cup",
      tags=["tokkuri", "ochoko", "japanese rice wine", "izakaya", "warm sake", "flask", "cup"])
def _(S):
    return [
        shell("M6.5 3H10V8C12.5 9 13 11 13 14V18a3 3 0 0 1-3 3H6.5a3 3 0 0 1-3-3V14C3.5 11 4 9 6.5 8Z"),
        shell("M16.5 14.5H21.5V16.5A2.5 2.5 0 0 1 16.5 16.5Z"),
    ]


@icon("masu-cup", CAT, "Square wooden box cup with a small glass standing inside it",
      tags=["masu", "sake cup", "japanese", "wooden box", "overflowing glass", "izakaya", "sake"])
def _(S):
    return [
        shell(poly([(9, 2.5), (15, 2.5), (14, 9), (10, 9)], closed=True, r=S.r * 0.4)),
        shell(rect(3.5, 9, 17, 12, L(S, 1, 2))),
        detail(seg(9.4, 6, 14.6, 6)),
    ]


@icon("boxed-wine", CAT, "Cardboard wine box with a carry handle cut out and a small tap at the bottom",
      tags=["bag in box", "cask wine", "casual wine", "party", "cardboard", "tap", "value wine"])
def _(S):
    return [
        shell(rect(4, 3, 16, 18.5, L(S, 1.5, 3))),
        detail(rect(8.5, 6, 7, 2.5, 1.25)),
        blob(10.5, 14.5, 3, 3),
    ]


@icon("goblet", CAT, "Heavy goblet with a wide bowl, a knobbed stem and a broad foot",
      tags=["chalice", "medieval", "cup", "royal", "wine cup", "fantasy", "toast"])
def _(S):
    return [
        shell("M6 3H18V7C18 11 15 13 12 13C9 13 6 11 6 7Z"),
        detail(seg(6, 6.5, 18, 6.5)),
        line(seg(12, 13, 12, 18)),
        dot(12, 15.5, 1.8),
        shell(poly([(10.5, 18), (13.5, 18), (17, 21), (7, 21)], closed=True, r=S.r * 0.5)),
    ]


@icon("drinking-horn", CAT, "Curved animal horn cup with a metal rim band",
      tags=["viking", "mead", "medieval", "horn cup", "nordic", "tankard", "feast"])
def _(S):
    tip = L(S, 20.5, 19.5)
    return [
        shell(f"M4 5C4 13.5 9.5 19.5 {tip} 20.5C15.5 17 13.5 12 13.5 5Z"),
        detail(seg(4.2, 8.5, 13.3, 8.5)),
    ]


@icon("wineskin", CAT, "Teardrop shaped leather bottle with a nozzle cap and a cord strap",
      tags=["wine skin", "bota bag", "leather flask", "travel", "camping", "ancient", "pilgrim"])
def _(S):
    return [
        shell("M13.5 7.5C10.5 9.5 10 10.5 8.5 12C5 14.5 4.5 20 9 21C13 22 19 20 19 15C19 11.5 17 9.5 15.5 7.5Z"),
        shell(rect(12.5, 3, 4, 4.5, L(S, 0.5, 1.25))),
        line("M16.5 4.5Q21.5 4 21.5 10"),
    ]


@icon("porron", CAT, "Glass wine pitcher with a wide base, a tall neck and a long thin spout angled out",
      tags=["spanish wine", "catalan", "communal drinking", "wine pitcher", "glass", "fiesta", "sangria"])
def _(S):
    return [
        shell("M9 4.5V9C5 10.5 4.5 14 4.5 17C4.5 19.5 6 21 8 21H13C15 21 16.5 19.5 16.5 17C16.5 14 13 10.5 13 9V4.5Z"),
        line(seg(15.5, 14.5, 21, 8.5)),
    ]


@icon("demijohn", CAT, "Big round bottle wrapped in wicker with a short neck and side handles",
      tags=["wicker bottle", "carboy", "wine jug", "fermenting", "rustic", "basket", "large bottle"])
def _(S):
    return [
        shell(circle(12, 15, 7)),
        shell(rect(10, 3.5, 4, 4, L(S, 0.5, 1.25))),
        detail(seg(5.5, 13, 18.5, 13)),
        detail(seg(6.5, 17.5, 17.5, 17.5)),
        line(poly([(5.3, 11.5), (3, 11.5), (3, 15)], r=S.r * 0.5)),
        line(poly([(18.7, 11.5), (21, 11.5), (21, 15)], r=S.r * 0.5)),
    ]


@icon("stoneware-jug", CAT, "Round clay jug with a big side handle, a narrow neck and a cork",
      tags=["clay jug", "cider jug", "ceramic", "rustic", "moonshine", "pottery", "crock"])
def _(S):
    return [
        shell("M9.5 6V8C5 9.5 4.5 13 4.5 16C4.5 19.5 7 21 9.5 21H14.5C17 21 19.5 19.5 19.5 16C19.5 13 19 9.5 14.5 8V6Z"),
        shell(rect(10, 2.5, 4, 3.5, L(S, 0.5, 1.25))),
        line("M19 10.5h1.5a1.5 1.5 0 0 1 1.5 1.5v2a1.5 1.5 0 0 1-1.5 1.5H19.5"),
        detail(seg(5, 13.5, 19, 13.5)),
    ]


@icon("swing-top-bottle", CAT, "Glass bottle with a wire bail and a ceramic stopper clamped on top",
      tags=["flip top", "lemonade bottle", "homebrew", "stopper", "wire clasp", "kombucha"])
def _(S):
    return [
        shell(poly([(10.2, 7), (13.8, 7), (13.8, 10), (17, 12.5), (17, 21), (7, 21), (7, 12.5), (10.2, 10)], closed=True, r=S.r)),
        shell(rect(9, 3, 6, 4, L(S, 1, 2))),
        line(poly([(9, 5), (6, 5), (6, 9.5)], r=S.r * 0.5)),
    ]


@icon("highball-glass", CAT, "Tall straight glass with an ice cube and a lemon wedge on the rim",
      tags=["collins glass", "tumbler", "mixed drink", "cocktail", "gin and tonic", "bar", "lemon"])
def _(S):
    return [
        shell(poly([(5.5, 6), (17.5, 6), (16.5, 21), (6.5, 21)], closed=True, r=S.r)),
        detail(rect(9, 10, 4.5, 4.5, 0.6)),
        shell("M15 6a3.5 3.5 0 0 1 7 0Z"),
    ]


@icon("rocks-glass", CAT, "Short heavy tumbler with one large ice cube",
      tags=["old fashioned glass", "whiskey glass", "lowball", "on the rocks", "scotch", "bourbon", "bar"])
def _(S):
    return [
        shell(poly([(4.5, 7), (19.5, 7), (17.5, 21), (6.5, 21)], closed=True, r=S.r)),
        detail(rect(9.5, 10.5, 5.5, 5.5, 0.6)),
    ]


@icon("shot-glass", CAT, "Small thick bottomed glass filled to the brim",
      tags=["shooter", "tequila", "vodka", "bar", "liquor", "party", "drink"])
def _(S):
    return [
        shell(poly([(6.5, 7), (17.5, 7), (16, 20.5), (8, 20.5)], closed=True, r=S.r)),
        detail(seg(7.2, 16, 16.8, 16)),
    ]


@icon("layered-shot", CAT, "Shot glass with three horizontal color bands",
      tags=["pousse cafe", "rainbow shot", "layers", "liqueur", "shooter", "bar"])
def _(S):
    return [
        shell(poly([(6.5, 3.5), (17.5, 3.5), (16, 21), (8, 21)], closed=True, r=S.r)),
        detail(seg(7, 9.5, 17, 9.5)),
        detail(seg(7.4, 15, 16.6, 15)),
    ]


@icon("margarita-glass", CAT, "Stepped wide rim glass on a stem",
      tags=["cocktail glass", "tequila", "salted rim", "lime", "mexican", "tropical", "bar"])
def _(S):
    return [
        shell(poly([(3.5, 4.5), (20.5, 4.5), (14.7, 10), (15.5, 11.5), (14.5, 14), (9.5, 14), (8.5, 11.5), (9.3, 10)], closed=True, r=S.r * 0.6)),
        line(seg(12, 14, 12, 20.5)),
        line(seg(8, 20.5, 16, 20.5)),
    ]


@icon("hurricane-glass", CAT, "Tall curvy glass with a narrow waist and a short stem",
      tags=["tropical cocktail", "pina colada", "tiki", "daiquiri", "bar", "new orleans", "curvy glass"])
def _(S):
    return [
        shell("M7 3H17C19 6 19 9 16.5 11.5C14.5 13.5 14.5 15 16 16.5C15 17.5 13.5 18 12 18C10.5 18 9 17.5 8 16.5C9.5 15 9.5 13.5 7.5 11.5C5 9 5 6 7 3Z"),
        line(seg(12, 18, 12, 20.5)),
        line(seg(8.5, 20.5, 15.5, 20.5)),
    ]


@icon("balloon-glass", CAT, "Big round stemmed glass with ice and a cucumber ribbon inside",
      tags=["gin glass", "copa", "gin and tonic", "spanish gin", "goblet", "cucumber", "bar"])
def _(S):
    return [
        shell("M7 4H17C21 8 20 14 15.5 15.5C14 16 10 16 8.5 15.5C4 14 3 8 7 4Z"),
        detail("M8.5 11.5q1.75-2.5 3.5 0t3.5 0"),
        line(seg(12, 16, 12, 20.5)),
        line(seg(8, 20.5, 16, 20.5)),
    ]
