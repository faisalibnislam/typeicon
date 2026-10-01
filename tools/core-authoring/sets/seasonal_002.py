"""TypeIcon Core: seasonal (batch 002), summer pool and beach, winter gear and seasonal covers."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt

CAT = "seasonal"


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


def wave(x0, x1, y, amp=1.2, n=3):
    """Open wave line from x0 to x1 made of n half-waves."""
    w = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        d += f"q{fmt(w / 2)} {fmt(-amp if i % 2 == 0 else amp)} {fmt(w)} 0"
    return d


@icon("row-cover-hoops", CAT, "Garden bed with a fabric cover stretched over wire hoops",
      tags=["row cover", "garden", "frost protection", "hoop tunnel", "plants", "winter", "greenhouse"])
def _(S):
    return [
        shell("M3 17.5C3 9 21 9 21 17.5Z"),
        detail("M9.5 17C9.5 13.5 10.5 11.5 12 10.5"),
        detail("M14.5 17C14.5 13.5 13.5 11.5 12 10.5"),
        line(seg(2, 21, 22, 21)),
    ]


@icon("beach-towel", CAT, "Striped beach towel with fringe at both ends",
      tags=["towel", "beach", "sunbathing", "swim", "summer", "stripes", "pool"])
def _(S):
    return [
        shell(rect(6, 5, 12, 14, rr(S, 2))),
        detail(seg(6, 9.5, 18, 9.5)),
        detail(seg(6, 14.5, 18, 14.5)),
        line(seg(2.5, 7, 3.5, 7)), line(seg(2.5, 12, 3.5, 12)), line(seg(2.5, 17, 3.5, 17)),
        line(seg(20.5, 7, 21.5, 7)), line(seg(20.5, 12, 21.5, 12)), line(seg(20.5, 17, 21.5, 17)),
    ]


@icon("boogie-board", CAT, "Bodyboard with a rounded nose and a leash coil",
      tags=["bodyboard", "surf", "wave", "beach", "summer", "foam board", "leash"])
def _(S):
    return [
        shell("M7 7C7 1.5 17 1.5 17 7V14Q12 16 7 14Z"),
        detail(seg(12, 5, 12, 10)),
        line("M12 17.5V18.5"),
        line(circle(12, 20, 1.5)),
    ]


@icon("stand-up-paddleboard", CAT, "Person standing on a long board holding a paddle in the water",
      tags=["sup", "paddleboarding", "paddle", "water sport", "lake", "summer", "board"])
def _(S):
    return [
        dot(8, 4.5, 2),
        line(poly([(8, 8), (8, 14)])),
        line(poly([(8, 10), (14, 8)])),
        line(seg(14, 3, 19.5, 17.5)),
        shell(rect(2, 15, 14, 2, rr(S, 1))),
        line(wave(2, 22, 21.5, 1, 4)),
    ]


@icon("parasailing", CAT, "Parachute canopy lifting a rider on a line from a motorboat",
      tags=["parasail", "parachute", "towed", "water sport", "beach", "summer", "boat", "resort"])
def _(S):
    return [
        shell("M3 10A9 7 0 0 1 21 10Q16.5 8 12 10Q7.5 8 3 10Z"),
        line(poly([(6, 10), (12, 14), (18, 10)])),
        dot(12, 14.5, 1.5),
        line(seg(12, 16, 12, 18)),
        shell(poly([(6, 19), (18, 19), (16, 21.5), (8, 21.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("pool-float", CAT, "Inflatable lounger with ribbed sections and a raised pillow end on water",
      tags=["inflatable", "lilo", "lounger", "swimming pool", "float", "raft", "summer"])
def _(S):
    return [
        shell("M3 15V8.5Q3 6 5.5 6Q8 6 8 8.5V15Z"),
        shell(rect(8, 11, 13, 4, rr(S, 1.5))),
        detail(seg(12.5, 11, 12.5, 15)),
        detail(seg(16.5, 11, 16.5, 15)),
        line(wave(2, 22, 20, 1.2, 4)),
    ]


@icon("pool-ladder", CAT, "Pool ladder with two handrails and steps entering the water",
      tags=["swimming pool", "steps", "handrail", "ladder", "swim", "summer", "water access"])
def _(S):
    return [
        line("M8 15V6Q8 3 11 3Q14 3 14 6"),
        line("M14 6V15"),
        line(seg(8, 8, 14, 8)),
        line(seg(8, 11.5, 14, 11.5)),
        line(wave(2, 22, 18, 1.2, 5)),
        line(seg(8, 15, 8, 21)), line(seg(14, 15, 14, 21)),
    ]


@icon("pool-thermometer", CAT, "Floating pool thermometer with a buoy top dipping into the water",
      tags=["water temperature", "swimming pool", "thermometer", "temperature", "float", "summer", "heat"])
def _(S):
    return [
        shell(rect(8.5, 2.5, 7, 5, rr(S, 2.5))),
        shell(rect(10.5, 7.5, 3, 9, rr(S, 1.5))),
        line(seg(12, 12, 12, 15)),
        line(wave(2, 22, 18.5, 1.2, 5)),
        line(wave(5, 19, 21.5, 1.2, 3)),
    ]


@icon("pool-cover", CAT, "Pool covered by a taut sheet with straps and a fallen leaf",
      tags=["swimming pool", "winterize", "tarp", "closing the pool", "debris", "straps", "cover"])
def _(S):
    return [
        shell(poly([(2, 8), (22, 8), (22, 17), (2, 17)], closed=True, r=S.r)),
        detail(seg(8, 8, 8, 17)),
        detail(seg(16, 8, 16, 17)),
        line(seg(5, 8, 5, 4)), line(seg(19, 8, 19, 4)),
        line(seg(5, 17, 5, 20.5)), line(seg(19, 17, 19, 20.5)),
        dot(12, 12.5, 1.5),
    ]


@icon("chlorine-floater", CAT, "Round floating chlorine dispenser with a domed cap and vents",
      tags=["chlorine", "swimming pool", "sanitizer", "tablet dispenser", "pool care", "float", "chemicals"])
def _(S):
    return [
        shell("M5 13C5 4 19 4 19 13Z"),
        shell(rect(3, 13, 18, 4, rr(S, 2))),
        detail(seg(9, 13, 9, 17)), detail(seg(15, 13, 15, 17)),
        line(wave(2, 22, 21.5, 1, 4)),
    ]


@icon("pool-test-kit", CAT, "Case holding two vials of tinted water and a colour comparison strip",
      tags=["water test", "ph", "chlorine test", "swimming pool", "testing kit", "vials", "pool care"])
def _(S):
    return [
        shell(rect(2.5, 14, 19, 7, rr(S, 2))),
        shell(rect(5, 3, 4, 11)),
        shell(rect(11, 3, 4, 11)),
        detail(seg(5, 8, 9, 8)),
        detail(seg(11, 8, 15, 8)),
        line(seg(18, 3, 18, 11)),
    ]


@icon("pool-vacuum", CAT, "Wide vacuum head on a long pole with a hose trailing behind",
      tags=["pool cleaner", "swimming pool", "vacuum", "cleaning", "pole", "hose", "maintenance"])
def _(S):
    return [
        line(poly([(19, 2.5), (11, 15)])),
        shell(rect(3.5, 15, 12, 4, rr(S, 2))),
        detail(seg(7, 17, 12, 17)),
        line("M15.5 18C18 18 18 21.5 21 21.5"),
    ]


@icon("horseshoe-pitching", CAT, "Metal stake in a sand pit with a horseshoe ringer around it",
      tags=["horseshoes", "lawn game", "backyard game", "ringer", "stake", "summer", "picnic"])
def _(S):
    return [
        line(seg(12, 3, 12, 14)),
        line("M5.5 15A6.5 6.5 0 1 1 18.5 15"),
        line(seg(5.5, 15, 5.5, 16)),
        line(seg(18.5, 15, 18.5, 16)),
        line("M2 21Q12 18 22 21"),
    ]


@icon("beach-bag", CAT, "Open straw tote with rope handles and a rolled towel peeking out",
      tags=["tote", "straw bag", "beach", "summer", "carry", "vacation", "holiday"])
def _(S):
    return [
        line("M8 9V6Q8 3 12 3Q16 3 16 6V9"),
        shell(poly([(3, 10), (21, 10), (19, 21), (5, 21)], closed=True, r=S.r)),
        detail(seg(4, 14.5, 20, 14.5)),
    ]


@icon("beach-mat", CAT, "Rolled woven mat with a strap and a short unrolled section",
      tags=["straw mat", "sunbathing", "beach", "picnic", "woven", "roll", "summer"])
def _(S):
    return [
        shell(circle(7, 12, 4.5)),
        dot(7, 12, 1.2),
        shell(poly([(7, 7.5), (21, 7.5), (21, 16.5), (7, 16.5)], closed=True, r=S.r * 0.5)),
        detail(seg(14, 7.5, 14, 16.5)),
    ]


@icon("sand-sifter", CAT, "Round sieve with a handle and sand falling through the holes",
      tags=["sieve", "sand", "beach", "sand toy", "kids", "summer", "strainer"])
def _(S):
    return [
        shell(circle(9, 9, 6)),
        line(seg(14, 14, 20, 20)),
        dot(7, 8, 1), dot(11, 8, 1), dot(9, 11.5, 1),
        dot(5, 19, 0.9),
        dot(9, 20, 0.9),
        dot(12.5, 21, 0.9),
    ]


@icon("umbrella-sand-anchor", CAT, "Corkscrew spike twisted into the sand holding an umbrella pole",
      tags=["beach umbrella", "sand anchor", "auger", "parasol", "wind", "beach", "summer"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 11)),
        shell(rect(9.5, 11, 5, 3.5, rr(S, 1))),
        line("M12 14.5L8 16.5L16 18.5L9 20.5"),
        line(seg(3, 14.5, 6, 14.5)),
        line(seg(18, 14.5, 21, 14.5)),
    ]


@icon("screen-tent", CAT, "Gazebo-style tent with a peaked roof and mesh wall panels",
      tags=["gazebo", "canopy", "camping", "bug screen", "shelter", "outdoor", "summer"])
def _(S):
    return [
        shell(poly([(12, 4), (20, 9.5), (4, 9.5)], closed=True, r=S.r), stroke_miterlimit="2"),
        line(seg(4, 9, 4, 21)), line(seg(20, 9, 20, 21)),
        line(seg(12, 9, 12, 21)),
        line(seg(4, 15, 20, 15)),
    ]


@icon("sangria", CAT, "Glass pitcher of fruit punch with citrus slices and a long spoon",
      tags=["pitcher", "wine punch", "fruit drink", "party", "cocktail", "summer", "orange slice"])
def _(S):
    return [
        shell(poly([(5, 6), (17, 6), (16, 21), (6, 21)], closed=True, r=S.r)),
        line("M17 8H20Q21 8 21 10V13Q21 15 19 15H16.5"),
        detail(seg(5.5, 10, 16.5, 10)),
        dot(9.5, 14, 1.5), dot(13, 17, 1.5),
        line(seg(10, 6, 13, 2)),
    ]


@icon("lemonade-pitcher", CAT, "Pitcher of lemonade with ice cubes inside and a lemon wedge on the rim",
      tags=["lemonade", "pitcher", "citrus", "cold drink", "summer", "lemon slice", "ice"])
def _(S):
    return [
        shell(poly([(4, 8), (16, 8), (15, 21), (5, 21)], closed=True, r=S.r)),
        line("M16 10H19Q20 10 20 12V15Q20 17 18 17H15.5"),
        line("M14 5A3 3 0 0 1 20 5Z"),
        sq(7, 13, 3, 3), sq(11, 16, 3, 3),
    ]


@icon("panama-hat", CAT, "Straw hat with a pinched crown, dark band and medium brim",
      tags=["straw hat", "sun hat", "summer", "fedora", "beach", "brim", "headwear"])
def _(S):
    return [
        shell("M6.5 14C6.5 8 8.5 5 12 5.5C15.5 5 17.5 8 17.5 14Z" if S.name == "rounded" else "M6.5 14L7.5 7Q10 5.5 12 7Q14 5.5 16.5 7L17.5 14Z"),
        shell(rect(2, 14, 20, 3.5, rr(S, 1.75))),
        detail(seg(6.5, 11, 17.5, 11)),
    ]


@icon("sundress", CAT, "Sleeveless dress with thin straps, fitted top and flared skirt",
      tags=["summer dress", "dress", "clothing", "fashion", "straps", "warm weather", "outfit"])
def _(S):
    return [
        line("M9 2.5V6M15 2.5V6"),
        shell(poly([(8, 6), (16, 6), (15, 11), (21, 21), (3, 21), (9, 11)], closed=True, r=S.r)),
        detail(seg(9, 11, 15, 11)),
    ]


@icon("swim-trunks", CAT, "Loose shorts with a drawstring waist and a side stripe",
      tags=["swimwear", "board shorts", "shorts", "swimming", "beach", "summer", "clothing"])
def _(S):
    return [
        shell(poly([(4, 4), (20, 4), (21, 20), (14, 20), (12, 11), (10, 20), (3, 20)], closed=True, r=S.r)),
        detail(seg(4, 7.5, 20, 7.5)),
        detail(seg(6.5, 11, 6, 17)),
    ]


@icon("misting-fan", CAT, "Pedestal fan with fine water droplets spraying out in front of the blades",
      tags=["mister", "cooling", "heat", "patio", "fan", "summer", "water spray"])
def _(S):
    return [
        shell(circle(9, 9, 6)),
        dot(9, 9, 1.5),
        line(seg(9, 15, 9, 20)),
        line(seg(5, 21, 13, 21)),
        dot(18, 6, 0.9), dot(21, 9, 0.9), dot(18, 12, 0.9), dot(21, 15, 0.9),
    ]


@icon("ac-unit-cover", CAT, "Outdoor air conditioner box wrapped in a fitted cover with a gathered hem",
      tags=["air conditioner", "winter", "outdoor unit", "hvac", "protect", "dust cover", "condenser"])
def _(S):
    return [
        shell(poly([(3, 7), (21, 7), (21, 20), (3, 20)], closed=True, r=S.r)),
        detail(seg(3, 17, 21, 17)),
        detail(circle(12, 12, 3)),
        line(seg(2.5, 20.5, 6, 20.5)),
        line(seg(18, 20.5, 21.5, 20.5)),
    ]


@icon("grill-cover", CAT, "Kettle grill on legs draped in a fitted cover with a handle bump",
      tags=["bbq", "barbecue", "winter", "protection", "weather cover", "kettle grill", "patio"])
def _(S):
    return [
        shell("M3.5 12C3.5 5 18.5 5 18.5 12Z"),
        line(seg(18.5, 9, 21.5, 9)),
        line(poly([(8, 12), (7, 21)])), line(poly([(14, 12), (15, 21)])),
        line(seg(5, 21, 17, 21)),
    ]


@icon("patio-furniture-cover", CAT, "Table and chairs shape under a single fitted cover with tie-down straps",
      tags=["outdoor furniture", "winter storage", "tarp", "patio", "garden", "weather protection", "straps"])
def _(S):
    return [
        shell("M2.5 20V15Q2.5 8 8.5 8H15.5Q21.5 8 21.5 15V20Z"),
        detail(seg(8, 8, 8, 20)),
        detail(seg(16, 8, 16, 20)),
        line(seg(8, 4, 16, 4)),
    ]


@icon("mulch-bag", CAT, "Bag of wood chips lying on its side with mulch spilling out of one end",
      tags=["wood chips", "garden", "landscaping", "soil", "bark", "gardening", "spring"])
def _(S):
    return [
        shell(poly([(2.5, 7), (14, 7), (14, 17), (2.5, 17)], closed=True, r=S.r)),
        detail(seg(5.5, 11, 11, 11)),
        line("M14 11.5C16 11.5 18 13.5 19 17"),
        dot(17, 19, 1.1), dot(20, 19.5, 1.1), dot(14.5, 20, 1.1), dot(21, 16, 1),
    ]


@icon("cooler-bag", CAT, "Soft insulated bag with a zip lid, front pocket and shoulder strap",
      tags=["lunch bag", "insulated", "picnic", "cold storage", "summer", "food carrier", "beach"])
def _(S):
    return [
        line("M7 9Q7 3.5 12 3.5Q17 3.5 17 9"),
        shell(rect(3, 9, 18, 12, rr(S, 3))),
        detail(seg(3, 12.5, 21, 12.5)),
        detail(seg(9, 16, 15, 16)),
    ]


@icon("screen-porch", CAT, "Porch with a roof overhang, corner posts, mesh panels and a screen door",
      tags=["screened porch", "veranda", "mesh", "bug screen", "house", "summer", "patio"])
def _(S):
    return [
        shell(poly([(12, 4), (20, 9.5), (4, 9.5)], closed=True, r=S.r), stroke_miterlimit="2"),
        line(seg(4, 9.5, 4, 21)), line(seg(20, 9.5, 20, 21)),
        line(poly([(9, 21), (9, 13), (15, 13), (15, 21)], r=S.r * 0.5)),
        dot(13, 17, 0.8),
    ]


@icon("above-ground-pool", CAT, "Round pool with straight walls, water line and an A-frame ladder",
      tags=["swimming pool", "backyard pool", "summer", "ladder", "water", "garden", "round pool"])
def _(S):
    return [
        shell(poly([(2.5, 10), (13, 10), (13, 21), (2.5, 21)], closed=True, r=S.r * 0.6)),
        line(wave(4.5, 11, 14.5, 1, 2)),
        line("M17 21V6Q17 3.5 19 3.5Q21 3.5 21 6V21"),
        line(seg(17, 11, 21, 11)),
        line(seg(17, 16, 21, 16)),
    ]


@icon("lifeguard-rescue-tube", CAT, "Long foam rescue tube with a clip at one end and a looped strap at the other",
      tags=["lifeguard", "rescue", "swimming", "beach safety", "pool safety", "float", "water rescue"])
def _(S):
    return [
        shell(rect(2.5, 9, 14, 6, rr(S, 3))),
        detail(seg(7, 9, 7, 15)),
        detail(seg(12, 9, 12, 15)),
        line("M16.5 12H19"),
        line(circle(20, 12, 1.5)) if S.name == "rounded" else line(rect(18.5, 10.5, 3, 3)),
    ]


@icon("bulb-forcing-vase", CAT, "Hourglass vase with a bulb in the neck, roots in the water and a sprout on top",
      tags=["forcing bulbs", "hyacinth", "amaryllis", "indoor gardening", "winter", "flower bulb", "glass vase"])
def _(S):
    return [
        line("M12 6V3.5"),
        shell("M9 10C9 7 11 6 12 6C13 6 15 7 15 10Z"),
        shell("M7.5 10H16.5L14 14L17.5 21H6.5L10 14Z" if S.name == "line" else "M7.5 10H16.5Q15 13 14 14Q16 17 17.5 21H6.5Q8 17 10 14Q9 13 7.5 10Z"),
        line(seg(10.5, 17.5, 13.5, 17.5)),
    ]


@icon("sun-tea-jar", CAT, "Big glass jar with a spigot and tea bags steeping, with a sun beside it",
      tags=["iced tea", "sun tea", "summer drink", "dispenser", "jar", "tea bags", "brewing"])
def _(S):
    return [
        shell(rect(3.5, 6, 13, 15, rr(S, 3))),
        line(seg(6, 3, 14, 3)),
        detail(seg(10, 9, 10, 12)),
        sq(8, 12, 4, 4),
        line(seg(16.5, 17, 20.5, 17)),
        line(seg(20.5, 15, 20.5, 19)),
    ]


@icon("firewood-moisture-meter", CAT, "Handheld meter with two pins pressed into a split log",
      tags=["moisture meter", "firewood", "seasoned wood", "wood stove", "winter", "log", "dryness"])
def _(S):
    return [
        shell(rect(7, 2.5, 10, 7, rr(S, 2.5))),
        detail(seg(10, 6, 14, 6)),
        line(seg(9.5, 9.5, 9.5, 14)), line(seg(14.5, 9.5, 14.5, 14)),
        shell(rect(3, 14, 18, 7, rr(S, 3))),
    ]


@icon("ice-fishing-jig-rod", CAT, "Short fishing rod with a small reel, its line dropping into a hole in the ice",
      tags=["ice fishing", "winter", "fishing rod", "jigging", "frozen lake", "angling", "hole"])
def _(S):
    return [
        line(poly([(3, 9), (8, 6), (17, 3.5)], r=S.r)),
        shell(circle(8.5, 11, 2.5)),
        line("M17 3.5V17"),
        shell(ellipse(15, 20, 7, 2)),
    ]


@icon("mitten-clips", CAT, "Pair of mittens joined by a strap with a clip at each end",
      tags=["mittens", "winter", "gloves", "kids", "keep together", "clip", "cold weather"])
def _(S):
    return [
        shell(rect(3, 4, 5, 8, rr(S, 2.5))),
        shell(rect(16, 4, 5, 8, rr(S, 2.5))),
        line("M5.5 12V15Q5.5 18 12 18Q18.5 18 18.5 15V12"),
        solid(rect(4, 12.5, 3, 2.5)),
    ]


@icon("snow-pants", CAT, "Insulated bib pants with shoulder straps, a chest panel and padded knees",
      tags=["snow bibs", "ski pants", "winter clothing", "snowsuit", "overalls", "cold weather", "snowboarding"])
def _(S):
    return [
        line(seg(8, 2.5, 8, 5)), line(seg(16, 2.5, 16, 5)),
        shell(poly([(7, 5), (17, 5), (17, 9), (19, 21.5), (13, 21.5), (12, 13), (11, 21.5), (5, 21.5), (7, 9)], closed=True, r=S.r)),
        detail(seg(7, 9, 17, 9)),
    ]


@icon("backyard-rink", CAT, "Small ice rink framed by low boards with a hockey stick leaning on one side",
      tags=["ice rink", "hockey", "skating", "winter", "backyard", "boards", "outdoor"])
def _(S):
    return [
        shell(rect(2.5, 11, 15, 9, rr(S, 2))),
        detail(seg(10, 11, 10, 20)),
        line("M21 3V18Q21 20 19.5 20"),
    ]


@icon("water-wings", CAT, "Pair of puffy inflatable arm bands side by side",
      tags=["arm bands", "floaties", "swimming aid", "kids", "pool", "learn to swim", "inflatable"])
def _(S):
    return [
        shell(circle(7, 12, 5)),
        shell(circle(17, 12, 5)),
        detail(circle(7, 12, 1.2)) if S.name == "rounded" else detail(seg(7, 10.5, 7, 13.5)),
        detail(circle(17, 12, 1.2)) if S.name == "rounded" else detail(seg(17, 10.5, 17, 13.5)),
    ]


@icon("salt-water-taffy", CAT, "Wrapped candy with twisted paper ends and a stripe",
      tags=["taffy", "candy", "boardwalk", "sweets", "seaside treat", "wrapped sweet", "beach"])
def _(S):
    return [
        shell(rect(7, 8, 10, 8, rr(S, 3))),
        detail(seg(12, 8, 12, 16)),
        line(poly([(7, 12), (3, 9.5)])), line(poly([(7, 12), (3, 14.5)])),
        line(poly([(17, 12), (21, 9.5)])), line(poly([(17, 12), (21, 14.5)])),
    ]


@icon("skate-sharpener", CAT, "Handheld sharpener sliding along an ice skate blade with sparks",
      tags=["ice skate", "blade", "sharpening", "hockey", "figure skating", "winter sports", "edge"])
def _(S):
    return [
        line(seg(2.5, 17.5, 21.5, 17.5)),
        shell(rect(8, 8, 8, 7, rr(S, 2))),
        line(seg(12, 3, 12, 8)),
        dot(4.5, 12.5, 1),
        dot(19.5, 12.5, 1),
    ]


@icon("pool-fence", CAT, "Row of tall safety fence panels on posts with water ripples behind",
      tags=["safety fence", "mesh fence", "child safety", "swimming pool", "barrier", "pool safety", "gate"])
def _(S):
    return [
        line(seg(4, 3, 4, 17)), line(seg(12, 3, 12, 17)), line(seg(20, 3, 20, 17)),
        line(seg(4, 7, 20, 7)), line(seg(4, 12, 20, 12)),
        line(wave(2, 22, 20.5, 1, 5)),
    ]
