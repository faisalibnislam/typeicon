"""TypeIcon Core: outdoors (batch 002).

Camping, trekking, climbing, fishing, snow and travel gear drawn from the objects themselves.
Long tools are designed upright and turned clockwise so the handle points to the bottom-left.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path

CAT = "outdoors"


def pick(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def rot(pts, deg=45, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rp(pts, closed=True, r=0.0, deg=45):
    return poly(rot(pts, deg), closed=closed, r=r)


def rotd(d, deg=45):
    """Rotate a closed shape given as a d-string."""
    return path_to_d(transform_path(P(d), rotation(deg)))


def rs(x1, y1, x2, y2, deg=45):
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg)
    return seg(a, b, c, d)


# ============================================================================ camp gear


@icon("folding-shovel", CAT, "Compact shovel with a pointed blade that folds at a hinge and a D-shaped grip",
      tags=["entrenching tool", "camp shovel", "dig", "camping", "survival", "trench"])
def _(S):
    blade = rp([(7.5, 10), (7.5, 7), (12, 1.5), (16.5, 7), (16.5, 10)], r=S.r * 0.6)
    return [
        shell(blade),
        detail(rs(9.5, 6.5, 14.5, 6.5)),
        line(rs(12, 10, 12, 16)),
        shell(rp([(8.5, 16), (15.5, 16), (15.5, 21.5), (8.5, 21.5)], r=S.r * 0.8)),
    ]


@icon("solar-shower", CAT, "Hanging water bag with a hose and shower head under a sun",
      tags=["camp shower", "outdoor shower", "water bag", "camping", "wash", "sun heated"])
def _(S):
    return [
        line("M7.5 2.5V4"),
        shell(rect(3, 4, 9, 7, pick(S, 2, 3))),
        detail("M3 7.5h9"),
        line("M7.5 11v3.5"),
        shell("M3.5 18A4 3.5 0 0 1 11.5 18Z"),
        line("M4.5 21v0.5"), line("M7.5 21v0.5"), line("M10.5 21v0.5"),
        shell(circle(17.5, 7, 2)),
        line("M17.5 2.25v1.5"), line("M17.5 10.25v1.5"), line("M12.75 7h1.5"), line("M20.75 7h1.5"),
    ]


@icon("canopy-tent", CAT, "Pop-up canopy with a peaked scalloped roof on four straight legs",
      tags=["pop up canopy", "gazebo", "shade tent", "market stall", "tailgate", "event tent", "shelter"])
def _(S):
    roof = "M3 10L12 3L21 10A3 3 0 0 1 15 10A3 3 0 0 1 9 10A3 3 0 0 1 3 10Z"
    return [
        shell(roof),
        line("M5 13.5V21"), line("M9 14.5V21"), line("M15 14.5V21"), line("M19 13.5V21"),
    ]


@icon("rv-hookup", CAT, "Utility post with a power socket and water tap connected to a hose",
      tags=["campsite pedestal", "power post", "water hookup", "rv park", "campground", "electric hookup", "caravan"])
def _(S):
    return [
        shell(rect(3.5, 3, 9, 18, pick(S, 1.5, 3))),
        dot(6.5, 8, 1), dot(9.5, 8, 1),
        detail("M3.5 11.5h9"),
        dot(8, 16, 1.75),
        line(poly([(12.5, 16), (17, 16), (17, 21)], r=S.r * 2)),
        line("M19 21h-4"),
    ]


@icon("frame-backpack", CAT, "Hiking pack strapped to an exposed external frame",
      tags=["external frame pack", "hiking pack", "rucksack", "trekking", "backpacking", "camping", "load carrying"])
def _(S):
    return [
        line("M5.5 2.5V21.5"), line("M18.5 2.5V21.5"),
        line("M5.5 5.5h13"),
        shell(rect(8.5, 9, 7, 9, pick(S, 1.5, 3))),
        detail("M8.5 13h7"),
    ]


@icon("head-net", CAT, "Brimmed hat with a mesh net hanging around the face and neck",
      tags=["mosquito net", "bug net", "insect protection", "beekeeping", "hat veil", "outdoors", "bug hat"])
def _(S):
    return [
        shell("M7.5 9V8A4.5 4.5 0 0 1 16.5 8V9Z"),
        line("M2.5 9.5h19"),
        shell(poly([(5.5, 12), (18.5, 12), (16.5, 21), (7.5, 21)], closed=True, r=S.r * 0.8)),
        detail("M8 15.5L16 19"), detail("M16 15.5L8 19"),
    ]


@icon("survival-kit", CAT, "Small tin box with its lid open and a match and a cross inside",
      tags=["emergency kit", "first aid tin", "bushcraft", "camping", "preparedness", "altoids tin", "escape"])
def _(S):
    return [
        shell(rect(3.5, 12, 17, 9, pick(S, 1, 2.5))),
        line(poly([(5.5, 12), (7.5, 3.5), (16.5, 3.5), (18.5, 12)], r=S.r)),
        line("M11 11V8"), dot(11, 6.25, 1.25),
        detail("M12 14.5v4M10 16.5h4"),
    ]


@icon("portable-solar-panel", CAT, "Folding solar panel of three sections with a cable to a phone",
      tags=["solar charger", "phone charging", "camping power", "off grid", "renewable", "foldable panel"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 8, pick(S, 1, 2))),
        detail("M9 2.5v8"), detail("M15 2.5v8"), detail("M3 6.5h18"),
        line(poly([(9, 10.5), (9, 19), (12.5, 19)], r=S.r * 2)),
        shell(rect(12.5, 15.5, 6, 6.5, pick(S, 1, 1.5))),
    ]


@icon("crank-radio", CAT, "Compact radio with a speaker, antenna and a hand crank on the side",
      tags=["hand crank radio", "emergency radio", "weather radio", "survival", "wind up", "preparedness"])
def _(S):
    return [
        line("M6 9L13 2.5"),
        shell(rect(3, 9, 15, 12, pick(S, 1.5, 3))),
        detail(circle(8.5, 15, 2.5)),
        dot(14, 12.5, 1), dot(14, 16, 1),
        line(poly([(18, 14), (21.5, 14), (21.5, 19)], r=S.r)),
    ]


@icon("bear-hang", CAT, "Food bag hanging from a rope under a high tree branch, well above the ground",
      tags=["bear bag", "food storage", "food hang", "backcountry", "camp food", "wildlife safety", "pct method"])
def _(S):
    return [
        line(poly([(5, 21), (5, 3.5), (20, 3.5)], r=S.r * 2)),
        line("M14 3.5V9"),
        shell(poly([(11, 9), (17, 9), (19, 13), (17, 17.5), (11, 17.5), (9, 13)], closed=True, r=S.r * 1.2)),
        detail("M11 11.5h6"),
        line("M2.5 21.5h19"),
    ]


@icon("chopping-stump", CAT, "Tree stump with an axe stuck in its top and a split log beside it",
      tags=["chopping block", "wood splitting", "firewood", "axe", "lumber", "log", "campfire wood"])
def _(S):
    return [
        shell("M3 10V19A5 2.5 0 0 0 13 19V10A5 2.5 0 0 0 3 10Z"),
        detail("M3 10A5 2.5 0 0 0 13 10"),
        line("M8 10L17 2.5"),
        shell(poly([(5.5, 7.5), (8.5, 5), (11, 8.5)], closed=True, r=S.r * 0.4)),
        shell(rect(17, 13.5, 4.5, 7.5, pick(S, 1, 2))),
    ]


@icon("bow-drill", CAT, "Bow with its string wrapped round an upright spindle on a fireboard",
      tags=["friction fire", "fire starting", "bushcraft", "survival", "primitive fire", "spindle", "fireboard"])
def _(S):
    return [
        line("M3 15Q12 3 21 15"),
        line("M3 15H21"),
        line("M12 7V18"),
        line("M12 2.5q2 1 0 2q-2 1 0 2"),
        shell(rect(3.5, 19, 17, 2.5, pick(S, 0.5, 1.25))),
    ]


@icon("hiking-boot", CAT, "Ankle-high boot with a lugged sole and laces",
      tags=["trail boot", "walking boot", "footwear", "trekking", "mountaineering", "shoe", "hike"])
def _(S):
    pts = [(5, 3), (13, 3), (13, 9.5), (21, 14), (21, 19), (19, 19), (19, 21), (16.5, 21), (16.5, 19), (14.5, 19),
           (14.5, 21), (12, 21), (12, 19), (10, 19), (10, 21), (7.5, 21), (7.5, 19), (5, 19)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.35)),
        detail("M5 15.5H21"),
        dot(16, 12.5, 0.9),
        detail("M5 7h8"),
    ]


@icon("trekking-poles", CAT, "Two crossed hiking poles with grips at the top and baskets near the tips",
      tags=["walking poles", "hiking sticks", "nordic walking", "trekking", "hiking", "mountain", "trail"])
def _(S):
    def pole(flip):
        def X(x):
            return 24 - x if flip else x
        grip = path_to_d(ST(seg(X(5.5), 2.5, X(8), 6.2), 1.5, S.cap, S.join))
        return [line(seg(X(5.5), 2.5, X(18.5), 21.5)), shell(grip),
                line(seg(X(14.5), 20, X(18.5), 17.2))]
    return pole(False) + pole(True)


@icon("gaiters", CAT, "Fabric leg cover over a boot with a strap under the sole",
      tags=["snow gaiters", "leg cover", "hiking", "mountaineering", "boot cover", "trekking", "debris guard"])
def _(S):
    return [
        shell(poly([(6, 3), (15, 3), (15, 10.5), (20.5, 13), (20.5, 17), (6, 17)], closed=True, r=S.r * 0.8)),
        detail("M6 7h9"),
        line(poly([(9, 18), (9, 21.5), (17.5, 21.5), (17.5, 18)], r=S.r)),
    ]


# ============================================================================ parks and signs


@icon("park-entrance", CAT, "Rustic log archway with a sign board hanging between two upright posts",
      tags=["park gate", "national park", "trailhead", "camp entrance", "welcome sign", "wooden arch", "gateway"])
def _(S):
    return [
        line("M5 4V21.5"), line("M19 4V21.5"),
        line("M2.5 4h19"),
        line("M9.5 4v3.5"), line("M14.5 4v3.5"),
        shell(rect(7.5, 7.5, 9, 5.5, pick(S, 0.5, 1.5))),
        line("M2.5 21.5h19"),
    ]


@icon("fire-danger-sign", CAT, "Semicircle gauge sign with a pointer and bands from low to extreme on a post",
      tags=["fire risk", "wildfire warning", "forest fire", "danger level", "ranger sign", "fire rating", "campfire ban"])
def _(S):
    return [
        shell("M2.5 16A9.5 9.5 0 0 1 21.5 16Z"),
        detail(seg(*polar(12, 16, 5.5, 230), *polar(12, 16, 9.5, 230))),
        detail(seg(*polar(12, 16, 5.5, 310), *polar(12, 16, 9.5, 310))),
        line("M12 16V11"),
        line("M12 16V21.5"),
    ]


@icon("interpretive-sign", CAT, "Angled reading panel on a post showing a leaf picture and lines of text",
      tags=["trail sign", "information board", "nature sign", "park info", "educational sign", "wayfinding", "museum outdoor"])
def _(S):
    return [
        shell(poly([(2.5, 6), (21.5, 3.5), (21.5, 14), (2.5, 16.5)], closed=True, r=S.r)),
        detail("M6 12.5C6 9 8 7.5 11 7.5C11 11 9 12.5 6 12.5Z"),
        detail("M14.5 7.5h4"), detail("M14.5 10.5h4"),
        line("M12 15.5V21.5"), line("M8.5 21.5h7"),
    ]


@icon("bear-box", CAT, "Metal food storage locker with a heavy latched lid and a bear head on the front",
      tags=["bear locker", "food locker", "campground", "food storage", "wildlife", "bear proof", "camp safety"])
def _(S):
    return [
        shell(rect(3, 3.5, 18, 18, pick(S, 1.5, 3))),
        detail("M3 8.5h18"),
        dot(12, 6, 0.9),
        dot(12, 15.5, 3), dot(9, 12.25, 1.2), dot(15, 12.25, 1.2),
    ]


@icon("boat-ramp", CAT, "Concrete slope running down into water with a boat floating off its end",
      tags=["launch ramp", "boat launch", "slipway", "marina", "lake access", "trailer", "dock"])
def _(S):
    return [
        shell(poly([(2.5, 8), (7, 8), (14, 21.5), (2.5, 21.5)], closed=True, r=S.r)),
        shell(poly([(12.5, 5), (21.5, 5), (19.5, 9), (14.5, 9)], closed=True, r=S.r * 0.5)),
        line("M15.5 14.5q1.5-1.5 3 0t3 0"),
        line("M17.5 19.5q1.5-1.5 2.5 0t2 0"),
    ]


@icon("field-guide", CAT, "Small book with a leaf and a bird on the cover",
      tags=["nature guide", "identification book", "birding", "plant guide", "naturalist", "handbook", "wildlife book"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, pick(S, 1.5, 3))),
        detail("M8.5 2.5v19"),
        detail("M11.5 12C11.5 8.5 13 7 16 7C16 10.5 14.5 12 11.5 12Z"),
        detail("M11.5 17q1.5-1.5 2.5 0q1-1.5 2.5 0"),
    ]


@icon("slackline", CAT, "Webbing line stretched between two trees with a person balancing on it",
      tags=["slacklining", "balance", "tightrope", "highline", "park activity", "trick line", "balancing"])
def _(S):
    return [
        line("M3.5 2.5V21.5"), line("M20.5 2.5V21.5"),
        line("M3.5 18.5Q12 20.5 20.5 18.5"),
        dot(12, 5.5, 1.75),
        line("M12 8.5V14.5"),
        line(poly([(7, 8.5), (12, 10), (17, 8.5)], r=S.r * 0.5)),
        line(poly([(10, 19), (12, 14.5), (14, 19)], r=S.r * 0.5)),
    ]


@icon("cornhole-board", CAT, "Slanted board with a round hole near the top and a bean bag below it",
      tags=["bean bag toss", "yard game", "lawn game", "tailgate game", "backyard", "toss game", "picnic game"])
def _(S):
    return [
        shell(poly([(6, 3), (18, 3), (21, 17.5), (3, 17.5)], closed=True, r=S.r * 0.8)),
        detail(circle(12, 7.5, 1.5)),
        sq(9.5, 12, 5, 3, pick(S, 0.5, 1.2)),
        line("M6.5 17.5V21.5"), line("M17.5 17.5V21.5"),
    ]


# ============================================================================ climbing


@icon("quickdraw", CAT, "Two carabiners joined by a short stitched sling",
      tags=["climbing", "sport climbing", "carabiner", "protection", "rock climbing", "sling", "draw"])
def _(S):
    return [
        line("M16.6 4.2A3.5 3.5 0 0 0 13.5 2.5H10.5A3.5 3.5 0 0 0 7 6V7A3.5 3.5 0 0 0 10.5 10.5H13.5A3.5 3.5 0 0 0 17 7"),
        shell(rect(10.5, 10, 3, 4, pick(S, 0.3, 1))),
        line("M7.4 15.2A3.5 3.5 0 0 1 10.5 13.5H13.5A3.5 3.5 0 0 1 17 17V18A3.5 3.5 0 0 1 13.5 21.5H10.5A3.5 3.5 0 0 1 7 18"),
    ]


@icon("belay-device", CAT, "Tube belay device with two slots and a carabiner clipped to it",
      tags=["belay", "climbing", "rappel device", "abseil", "rope brake", "belaying", "tube device"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 9, pick(S, 3, 4))),
        detail("M8.5 5.5v3"), detail("M15.5 5.5v3"),
        line("M12 11.5V14"),
        shell(rect(8, 14, 8, 7.5, pick(S, 3, 3.5))),
    ]


@icon("climbing-harness", CAT, "Waist belt with two leg loops and a central tie-in point",
      tags=["climbing", "rock climbing", "sit harness", "belay", "safety gear", "mountaineering", "rope"])
def _(S):
    return [
        shell(rect(3, 3, 18, 4.5, pick(S, 1, 2))),
        shell(rect(3.5, 11, 6, 10.5, 3)),
        shell(rect(14.5, 11, 6, 10.5, 3)),
        line("M12 7.5V14"),
        dot(12, 16.5, 1.5),
    ]


@icon("chalk-bag", CAT, "Drawstring pouch for climbing chalk with a brush loop on the side",
      tags=["chalk", "climbing", "bouldering", "grip", "magnesium", "gym", "rock climbing gear"])
def _(S):
    return [
        shell(poly([(5.5, 9), (18.5, 9), (17, 21.5), (7, 21.5)], closed=True, r=S.r * 1.3)),
        line("M5.5 9C8 4 16 4 18.5 9"),
        detail("M6.2 13h11.6"),
        dot(12, 17, 1.2),
    ]


@icon("climbing-shoe", CAT, "Tight downturned shoe with a pointed toe and a hook-and-loop strap",
      tags=["climbing", "bouldering", "rock shoe", "footwear", "gym", "rubber sole", "sport"])
def _(S):
    return [
        shell(poly([(3.5, 4), (10, 4), (13, 8.5), (19, 11.5), (21.5, 18), (19, 20.5), (3.5, 20.5)], closed=True, r=S.r * 0.8)),
        detail("M3.5 17H18"),
        detail("M9 5V14"),
    ]


@icon("ice-axe", CAT, "Mountaineering axe with a straight shaft, a curved pick and a flat adze",
      tags=["ice climbing", "mountaineering", "alpine", "axe", "glacier", "winter climbing", "piolet"])
def _(S):
    return [
        line(rs(12, 6, 12, 22)),
        line(rp([(3.5, 10.5), (6.5, 7), (9, 5.5), (12, 5.5)], closed=False, r=S.r)),
        shell(rp([(12, 4.5), (18, 4.5), (18, 8.5), (12, 8.5)], r=S.r * 0.5)),
    ]


@icon("piton", CAT, "Flat metal spike with an eye hole at the top, hammered into a rock crack",
      tags=["climbing", "rock climbing", "peg", "anchor", "mountaineering", "protection", "spike"])
def _(S):
    return [
        shell(rp([(8.5, 3), (15.5, 3), (15.5, 13), (12, 21.5), (8.5, 13)], r=S.r * 0.7)),
        detail(circle(*rot([(12, 7.5)])[0], 1.2)),
    ]


@icon("climbing-cam", CAT, "Spring-loaded camming device with two curved lobes, a stem and a sling",
      tags=["climbing", "friend", "protection", "trad climbing", "rock climbing", "gear", "anchor"])
def _(S):
    return [
        shell("M10.5 11L3.5 8.5A8 8 0 0 1 10.5 3Z"),
        shell("M13.5 11L20.5 8.5A8 8 0 0 0 13.5 3Z"),
        line("M12 11V16"),
        line("M9.5 14h5"),
        shell(rect(9, 17, 6, 4.5, pick(S, 1.5, 2.2))),
    ]


@icon("rappelling", CAT, "Person leaning back against a cliff face and descending a rope",
      tags=["abseiling", "climbing", "cliff", "canyoning", "rope descent", "adventure", "mountaineering"])
def _(S):
    return [
        line("M3.5 2.5V21.5"),
        dot(16.5, 6, 2),
        line("M15 9.5L11 14"),
        line(poly([(11, 14), (7.5, 13), (6, 17)], r=S.r * 0.5)),
        line(poly([(6, 2.5), (11, 14), (9.5, 21.5)], r=S.r * 0.5)),
    ]


@icon("crash-pad", CAT, "Thick foam bouldering mat lying at the base of a boulder",
      tags=["bouldering", "climbing", "mat", "landing pad", "rock climbing", "safety", "foam pad"])
def _(S):
    return [
        line(poly([(4.5, 14), (6, 8), (11, 3.5), (16.5, 5), (19.5, 10), (19.5, 14)], r=S.r * 1.5)),
        shell(rect(2.5, 14.5, 19, 7, pick(S, 1.5, 3))),
        detail("M12 14.5v7"),
    ]


@icon("climbing-hold", CAT, "Irregular resin hold bolted to a climbing wall panel",
      tags=["climbing wall", "bouldering", "gym", "grip", "handhold", "jug", "indoor climbing"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, pick(S, 1, 2.5))),
        detail("M7 16.5C6 11.5 8 8 12 8C16 8 18 10.5 17 13.5C16 16.5 12 17.5 7 16.5Z"),
        dot(12, 12.5, 1.25),
    ]


@icon("hangboard", CAT, "Wooden training board above a doorway with pockets and edges to grip",
      tags=["fingerboard", "climbing training", "finger strength", "door frame", "pull up", "hang", "campus"])
def _(S):
    return [
        shell(rect(2.5, 4, 19, 10.5, pick(S, 1, 2.5))),
        detail("M6.5 7.5h4"), detail("M13.5 7.5h4"),
        detail("M6.5 11h11"),
        line("M5 14.5v7"), line("M19 14.5v7"),
    ]


@icon("snowshoes", CAT, "Pair of oval snowshoes with laced webbing and binding straps",
      tags=["winter hiking", "snow", "walking in snow", "trekking", "winter sports", "raquettes", "trail"])
def _(S):
    return [
        shell(ellipse(7, 10.5, 4, 8)),
        shell(ellipse(17, 10.5, 4, 8)),
        detail("M4 9h6"), detail("M4 13h6"),
        detail("M14 9h6"), detail("M14 13h6"),
        line("M7 18.5V22"), line("M17 18.5V22"),
    ]


@icon("avalanche-beacon", CAT, "Handheld rescue transceiver with a direction arrow and signal waves above it",
      tags=["avalanche transceiver", "backcountry", "snow safety", "search and rescue", "ski touring", "signal", "locator"])
def _(S):
    return [
        shell(rect(6, 10, 12, 11.5, pick(S, 2, 3))),
        detail("M12 18.5V13.5"), detail("M9.5 15.5L12 13L14.5 15.5"),
        line(arc(12, 10, 4, 235, 305)),
        line(arc(12, 10, 7.5, 240, 300)),
    ]


@icon("base-camp", CAT, "Two small dome tents at the foot of a snowy mountain peak",
      tags=["mountaineering", "expedition", "camp", "alpine", "everest", "summit", "basecamp"])
def _(S):
    return [
        line(poly([(3.5, 15), (12, 3.5), (20.5, 15)], r=S.r * 0.5)),
        line("M9 8.5l1.7 2 1.3-1.8 1.4 1.8 1.6-2"),
        shell("M3 21.5A3.75 3.75 0 0 1 10.5 21.5Z"),
        shell("M13.5 21.5A3.75 3.75 0 0 1 21 21.5Z"),
    ]


@icon("figure-eight-knot", CAT, "Rope tied in a figure-eight knot with two loops crossing",
      tags=["climbing knot", "rope", "tie in", "stopper knot", "sailing", "rescue", "rock climbing"])
def _(S):
    a, b, c = pick(S, (8.8, 9, 4.2), (9.2, 9, 4.0))
    return [
        line(f"M{a} {b}A{c} {c} 0 1 1 {24 - a} {b}L{a} {24 - b}A{c} {c} 0 1 0 {24 - a} {24 - b}Z"),
    ]


@icon("ski-pass", CAT, "Plastic lift pass card with a skier symbol hanging from a lanyard clip",
      tags=["lift ticket", "ski resort", "season pass", "winter", "chairlift", "access card", "skiing"])
def _(S):
    return [
        shell(circle(12, 4.5, 1.75)),
        line("M12 6.25V9"),
        shell(rect(5, 9, 14, 12.5, pick(S, 1.5, 3))),
        dot(14.5, 12.75, 1.2),
        line(poly([(13.5, 14.5), (11, 17)], r=0)),
        line("M8.5 18.5h7"),
    ]


@icon("ski-boot", CAT, "Tall rigid boot with buckles along the shell and a flat sole",
      tags=["skiing", "snowboarding", "winter sports", "footwear", "alpine", "boot", "binding"])
def _(S):
    return [
        shell(poly([(6, 2.5), (14, 2.5), (14, 11), (21, 15), (21, 21), (4.5, 21), (6, 16)], closed=True, r=S.r * 0.8)),
        detail("M6 6h8"), detail("M6 9.5h8"),
        detail("M16.5 15.5l.5 3"),
    ]


@icon("skis", CAT, "Pair of long skis crossed in an X with bindings",
      tags=["skiing", "alpine skiing", "winter sports", "snow", "downhill", "cross country", "slopes"])
def _(S):
    def ski(flip):
        def X(x):
            return 24 - x if flip else x
        a = (X(5.5), 3.5)
        b = (X(18.5), 20.5)
        p1 = (a[0] + (b[0] - a[0]) * 0.27, a[1] + (b[1] - a[1]) * 0.27)
        p2 = (a[0] + (b[0] - a[0]) * 0.4, a[1] + (b[1] - a[1]) * 0.4)
        return [line(seg(*a, *b)), solid(path_to_d(ST(seg(*p1, *p2), 3.6, "butt", "miter")))]
    return ski(False) + ski(True)


@icon("fishing-reel", CAT, "Spinning reel with a dome, a wound spool, a crank handle and a foot mount",
      tags=["angling", "fishing", "spinning reel", "rod and reel", "tackle", "line", "lake"])
def _(S):
    return [
        line("M9 3.5h6"), line("M12 3.5V6.5"),
        shell(circle(11.5, 14, 7.5)),
        detail(circle(11.5, 14, 2.8)),
        line(poly([(19, 12), (21.5, 12), (21.5, 18)], r=S.r * 0.5)),
    ]


# ============================================================================ fishing and boating


@icon("fishing-hook", CAT, "J-shaped hook with a barbed point and an eye at the top",
      tags=["angling", "fishing", "tackle", "catch", "bait hook", "barb", "lake"])
def _(S):
    return [
        shell(circle(14, 4.5, 1.75)),
        line("M14 6.25V16A5 5 0 0 1 4 16V12"),
        line("M4 12L6.5 9.5"),
    ]


@icon("fishing-lure", CAT, "Fish-shaped crankbait with a diving lip at the front and two hooks below",
      tags=["crankbait", "angling", "fishing", "tackle", "bait", "plug", "bass"])
def _(S):
    return [
        shell(poly([(3.5, 9), (7, 5), (15, 5), (18, 8), (21.5, 5.5), (21.5, 12.5), (18, 10), (15, 13), (7, 13)], closed=True, r=S.r * 1.2)),
        dot(8, 8.5, 1.1),
        line(poly([(4.5, 11.5), (2.5, 14.5)], r=0)),
        line("M9.5 13v4.5a2 2 0 0 0 4 0"),
        line("M17 11v5a2 2 0 0 0 4 0"),
    ]


@icon("fishing-fly", CAT, "Tiny fly lure with feather hackle, a tail and a hook curling beneath",
      tags=["fly fishing", "angling", "dry fly", "trout", "tackle", "feather", "lure"])
def _(S):
    return [
        shell("M12.5 6.5C9.5 4 6 5 4 9C8 10.5 11.5 9.5 12.5 6.5Z"),
        line("M16.5 3.5V14a3.5 3.5 0 0 1-7 0V12"),
        line("M12.5 6.5L16.5 9"),
    ]


@icon("fishing-bobber", CAT, "Round float split into two halves with a stem on top, sitting on water ripples",
      tags=["float", "angling", "fishing", "tackle", "bob", "lake", "pond"])
def _(S):
    return [
        line("M12 4V2.5"),
        shell(ellipse(12, 10, pick(S, 6.5, 6), pick(S, 6.5, 6.5))),
        detail("M5.5 10h13"),
        line("M3 20q2-1.6 4 0t4 0 4 0 4 0"),
    ]


@icon("landing-net", CAT, "Hoop net with a long handle and a deep mesh bag hanging below it",
      tags=["fishing net", "angling", "catch and release", "dip net", "net", "fish", "tackle"])
def _(S):
    return [
        shell("M8.5 7C8.5 19.5 21.5 19.5 21.5 7Z"),
        detail("M15 7v8"), detail("M11 11h8"),
        line("M9 7.5L3 21.5"),
    ]


@icon("tackle-box", CAT, "Box with stepped trays fanned out above the base",
      tags=["fishing box", "angling", "gear box", "lures", "storage", "tray", "fishing gear"])
def _(S):
    return [
        shell(rect(3, 14, 18, 7.5, pick(S, 1, 2.5))),
        dot(12, 17.75, 1),
        shell(rect(5, 8.5, 14, 5.5, pick(S, 0.5, 1.5))),
        detail("M12 8.5v5.5"),
        shell(rect(8, 3, 8, 5.5, pick(S, 0.5, 1.5))),
    ]


@icon("fishing-sinker", CAT, "Teardrop lead weight with a small loop at the top for tying to a line",
      tags=["weight", "lead", "angling", "fishing", "tackle", "split shot", "drop"])
def _(S):
    cx = pick(S, 9, 9.5)
    cy = pick(S, 11.5, 11)
    return [
        shell(circle(12, 4.5, 1.5)),
        shell(f"M12 8C{cx} {cy} 7 13 7 15.5A5 5 0 0 0 17 15.5C17 13 {24 - cx} {cy} 12 8Z"),
    ]


@icon("bait-bucket", CAT, "Bucket with a lid, a handle and a small fish visible through a side slot",
      tags=["live bait", "angling", "fishing", "minnow bucket", "worms", "tackle", "pail"])
def _(S):
    return [
        line("M6 5.5C6 0.5 18 0.5 18 5.5"),
        shell(rect(3.5, 5.5, 17, 3.5, pick(S, 0.5, 1.5))),
        shell(poly([(4.5, 9.5), (19.5, 9.5), (17.5, 21.5), (6.5, 21.5)], closed=True, r=S.r * 0.8)),
        detail("M8.5 13h7"),
        solid(ellipse(11, 17, 2.5, 1.3)),
        solid("M13.2 17L15 15.8V18.2Z"),
    ]


@icon("fishing-vest", CAT, "Sleeveless vest covered in pockets with a patch on the chest",
      tags=["angler vest", "fly fishing", "outdoor clothing", "pockets", "utility vest", "gilet", "tackle"])
def _(S):
    pts = [(7, 3), (9.5, 3), (12, 7.5), (14.5, 3), (17, 3), (20.5, 8), (20.5, 21.5), (3.5, 21.5), (3.5, 8)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail("M12 7.5V21.5"),
        detail(rect(5.5, 13.5, 4, 5, pick(S, 0, 1))),
        detail(rect(14.5, 13.5, 4, 5, pick(S, 0, 1))),
    ]


@icon("fishing-creel", CAT, "Wicker basket with a shoulder strap and a fish tail poking out of the lid",
      tags=["fish basket", "angling", "fishing", "wicker", "catch", "tackle", "trout"])
def _(S):
    return [
        line("M4.5 11C4.5 1 19.5 1 19.5 11"),
        shell(poly([(4.5, 11), (19.5, 11), (20.5, 21.5), (3.5, 21.5)], closed=True, r=S.r)),
        detail("M4 16h16"),
        line("M10 6L12 8.5L14 6"),
    ]


@icon("fish-on-hook", CAT, "Fish dangling vertically from a line with a hook through its mouth",
      tags=["catch", "angling", "fishing", "hooked", "caught fish", "reel in", "bite"])
def _(S):
    return [
        line("M12 2.5V8"),
        shell(ellipse(12, 12.5, 4.5, 5 + pick(S, 0, 0.5))),
        shell(poly([(12, 17), (8, 21.5), (16, 21.5)], closed=True, r=S.r * 0.6)),
        dot(10.3, 11.5, 0.9),
    ]


@icon("fly-fishing", CAT, "Angler standing in water casting a line that loops in a large S curve overhead",
      tags=["angling", "casting", "fishing", "trout", "river", "rod", "stream"])
def _(S):
    return [
        dot(6.5, 7, 1.75),
        line("M6.5 10V16"),
        line(poly([(6.5, 12), (9.5, 11)], r=0)),
        line("M9.5 11L14 3.5"),
        line("M14 3.5C21 2 21.5 7.5 16.5 8.5C12.5 9.5 15.5 14 21 12.5"),
        line("M6.5 16L5.5 19.5"), line("M6.5 16L8.5 19.5"),
        line("M2.5 20.5q2-1.6 4 0t4 0 4 0 4 0 3.5 0"),
    ]


@icon("rowboat", CAT, "Small wooden boat with two oars raised in oarlocks, seen from the side",
      tags=["boat", "row", "rowing boat", "dinghy", "lake", "oars", "water"])
def _(S):
    return [
        shell("M2.5 12H21.5Q19.5 17.5 14 17.5H10Q4.5 17.5 2.5 12Z"),
        line("M8 12L3.5 4.5"), line("M16 12L20.5 4.5"),
        solid(path_to_d(ST(seg(3.2, 4.2, 4.6, 6.6), 3, "butt", "miter"))),
        solid(path_to_d(ST(seg(20.8, 4.2, 19.4, 6.6), 3, "butt", "miter"))),
        line("M2.5 21q2-1.6 4 0t4 0 4 0 4 0 3.5 0"),
    ]


@icon("canoe-paddle", CAT, "Single paddle with a T-grip at the top and one wide rounded blade",
      tags=["paddle", "canoeing", "paddling", "oar", "water sports", "river", "camp"])
def _(S):
    return [
        line(rs(12, 3.5, 12, 10)),
        line(rs(9.5, 3.5, 14.5, 3.5)),
        shell(rotd("M12 9.5C16.5 10.5 16.5 17 15 19.5A3.1 3.1 0 0 1 9 19.5C7.5 17 7.5 10.5 12 9.5Z")),
    ]


@icon("kayak-paddle", CAT, "Long shaft with an angled blade at each end",
      tags=["paddle", "kayaking", "double paddle", "paddling", "water sports", "canoe", "river"])
def _(S):
    return [
        line(rs(12, 8, 12, 16)),
        shell(rotd(ellipse(12, 5, 3.3, 4.2))),
        shell(rotd(ellipse(12, 19.5, 1.4, 4.2))),
    ]


@icon("cast-net", CAT, "Round fishing net spreading open in the air with weights along its edge",
      tags=["throw net", "fishing net", "angling", "bait net", "mesh", "shrimp net", "catch"])
def _(S):
    c = pick(S, 5.5, 6.5)
    return [
        shell(f"M12 3C{c} 5.5 3.5 10.5 3.5 16H20.5C20.5 10.5 {24 - c} 5.5 12 3Z"),
        detail("M12 4.5V16"), detail("M12 5L8 16"), detail("M12 5L16 16"),
        detail("M5.2 10.5Q12 13 18.8 10.5"),
        dot(5.5, 19.75, 1), dot(8.75, 19.75, 1), dot(12, 19.75, 1), dot(15.25, 19.75, 1), dot(18.5, 19.75, 1),
    ]


@icon("ice-fishing", CAT, "Hole cut in the ice with a short rod and a line dropping into the water",
      tags=["winter fishing", "ice hole", "angling", "frozen lake", "rod", "tip up", "snow"])
def _(S):
    return [
        line("M4 13.5L13 4.5"),
        line("M13 4.5V17"),
        shell(ellipse(13, 18.5, pick(S, 7.5, 7), 3)),
        line("M2.5 18.5h1.5"),
    ]


@icon("ice-auger", CAT, "Hand ice drill with a crank handle and a spiral blade boring into ice",
      tags=["ice drill", "ice fishing", "winter", "hand auger", "frozen lake", "crank", "hole"])
def _(S):
    return [
        line(poly([(12, 4), (19, 4), (19, 9)], r=S.r * 0.5)),
        line("M12 4V12"),
        shell(poly([(8.5, 12), (15.5, 12), (12, 20)], closed=True, r=S.r * 0.6)),
        detail("M10.5 14.6h3"),
        line("M2.5 15h4"), line("M17.5 15h4"),
    ]


@icon("dry-bag", CAT, "Roll-top waterproof bag with its folded top held by a buckle",
      tags=["waterproof bag", "kayaking", "paddling", "camping", "rafting", "roll top", "stuff sack"])
def _(S):
    return [
        shell(rect(6.5, 3.5, 11, 4.5, pick(S, 1.5, 2.2))),
        shell(rect(5, 9, 14, 12.5, pick(S, 1.5, 3))),
        dot(12, 14.5, 1.6),
        detail("M12 9V12"),
    ]


@icon("river-tubing", CAT, "Inner tube floating on a river with a person sitting in the ring",
      tags=["tubing", "float trip", "lazy river", "inner tube", "summer", "water fun", "rafting"])
def _(S):
    return [
        dot(12, 3.75, 1.75),
        line("M12 6.5V11"),
        shell(ellipse(12, 15, 9.5, 6)),
        detail(ellipse(12, 15, 4.25, 2)),
    ]


@icon("bungee-jumping", CAT, "Person falling head-first from a platform on a stretched coiled cord",
      tags=["bungy", "extreme sports", "jump", "adventure", "thrill", "free fall", "cord"])
def _(S):
    return [
        line("M2.5 3.5H8"), line("M2.5 3.5V8"),
        line(poly([(6.5, 3.5), (9, 5.5), (7.5, 7), (10.5, 8.5), (13.5, 9.5)], r=S.r * 0.3)),
        line(poly([(12.5, 8.5), (14, 12), (15.5, 8.5)], r=S.r * 0.5)),
        line("M14 12V17"),
        dot(14, 19.75, 1.75),
        line(poly([(11.5, 17.5), (14, 15), (16.5, 17.5)], r=S.r * 0.5)),
    ]


@icon("passport-stamp", CAT, "Round ink stamp with a double border and a small plane in the middle",
      tags=["travel stamp", "visa", "border control", "immigration", "arrival", "airport", "customs"])
def _(S):
    plane = [(12, 7.5), (13, 9.5), (13, 11), (17.5, 13.5), (17.5, 15), (13, 13.8), (13, 16.5), (14.8, 17.8),
             (14.8, 18.8), (12, 18), (9.2, 18.8), (9.2, 17.8), (11, 16.5), (11, 13.8), (6.5, 15), (6.5, 13.5),
             (11, 11), (11, 9.5)]
    pts = [(12 + (x - 12) * 0.78, 12.6 + (y - 13) * 0.78) for x, y in plane]
    return [
        shell(circle(12, 12, pick(S, 9.25, 9))),
        detail(circle(12, 12, pick(S, 6, 6.25))),
        Part("dot", poly(pts, closed=True)),
    ]


@icon("vintage-suitcase", CAT, "Boxy leather suitcase with two buckled straps, a top handle and a round sticker",
      tags=["old suitcase", "retro luggage", "travel", "trunk", "case", "trip", "nostalgia"])
def _(S):
    return [
        line(poly([(9, 8), (9, 4.5), (15, 4.5), (15, 8)], r=S.r * 0.5)),
        shell(rect(3, 8, 18, 13.5, pick(S, 1.5, 3))),
        detail("M7.5 8v13.5"), detail("M16.5 8v13.5"),
        detail(circle(12, 15, 1.4)),
    ]


@icon("bag-sizer", CAT, "Open metal frame cage with a small suitcase fitting inside it to check cabin bag size",
      tags=["cabin bag", "carry on", "baggage check", "airline", "luggage size", "gate", "hand luggage"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, pick(S, 1, 3))),
        detail(poly([(10, 8), (10, 5.5), (14, 5.5), (14, 8)], r=S.r * 0.3)),
        detail(rect(7, 8, 10, 10.5, pick(S, 1, 2.2))),
    ]


@icon("wrapped-luggage", CAT, "Suitcase wrapped in diagonal bands of plastic film with its handle poking out",
      tags=["luggage wrap", "baggage wrap", "airport", "travel protection", "suitcase", "shrink wrap", "security"])
def _(S):
    return [
        line(poly([(9, 8), (9, 4.5), (15, 4.5), (15, 8)], r=S.r * 0.5)),
        shell(rect(4, 8, 16, 13.5, pick(S, 1.5, 3))),
        detail("M4 16L12 8"), detail("M4 21L17 8"), detail("M9 21.5L20 10.5"),
    ]


@icon("key-safe", CAT, "Small wall box with a push-button keypad and a key hanging below its open flap",
      tags=["lockbox", "key lock box", "realtor", "rental access", "keypad", "spare key", "airbnb"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 12, pick(S, 1.5, 3))),
        dot(9, 6.5, 1), dot(12, 6.5, 1), dot(15, 6.5, 1),
        dot(9, 10, 1), dot(12, 10, 1), dot(15, 10, 1),
        shell(circle(12, 18.25, 1.6)),
        line("M12 19.85V22"),
    ]


@icon("swim-up-bar", CAT, "Bar counter with round stools standing in pool water and waves across their legs",
      tags=["pool bar", "resort", "tiki bar", "poolside", "cocktails", "vacation", "swimming pool"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 4, pick(S, 0.5, 2))),
        shell(rect(4.5, 10, 6, 2.5, pick(S, 0.5, 1.25))),
        shell(rect(13.5, 10, 6, 2.5, pick(S, 0.5, 1.25))),
        line("M7.5 12.5V21"), line("M16.5 12.5V21"),
        line("M2.5 17q2.25-1.75 4.5 0t4.5 0 4.5 0 4.5 0"),
    ]


@icon("sky-lantern", CAT, "Tall paper lantern floating upward with a small flame glowing at its open base",
      tags=["floating lantern", "wish lantern", "festival", "celebration", "paper lantern", "night", "flame"])
def _(S):
    return [
        shell(poly([(8, 2.5), (16, 2.5), (19, 15.5), (5, 15.5)], closed=True, r=S.r * 1.2)),
        detail("M7 8h10"),
        shell("M12 17.2C10.8 18.4 10.2 19.3 10.2 20A1.8 1.8 0 0 0 13.8 20C13.8 19 12.8 18.4 12 17.2Z"),
    ]


@icon("face-in-hole-board", CAT, "Painted standing board with a cartoon body and an oval cutout where a face goes",
      tags=["photo board", "cutout board", "fairground", "photo prop", "funny photo", "carnival", "selfie"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 16, pick(S, 1, 3))),
        detail(ellipse(12, 7.25, 2.6, 3)),
        detail("M7.5 18.5V15.5C7.5 13 9.5 12.5 12 12.5S16.5 13 16.5 15.5V18.5"),
        line("M7 18.5L4.5 21.5"), line("M17 18.5L19.5 21.5"),
    ]


@icon("banana-boat", CAT, "Long inflatable tube with riders sitting in a row, towed by a rope",
      tags=["water sports", "towable tube", "beach", "inflatable", "boat ride", "tow", "summer fun"])
def _(S):
    return [
        shell(rect(2.5, 13, 15, 5.5, 2.75)),
        dot(6, 7, 1.4), dot(10, 7, 1.4), dot(14, 7, 1.4),
        line("M6 9.5V13"), line("M10 9.5V13"), line("M14 9.5V13"),
        line("M17.5 15.75L21.5 12"),
        line("M2.5 21.5q2-1.5 4 0t4 0 4 0 4 0 3.5 0"),
    ]


@icon("caving", CAT, "Person crawling through a low cave passage with a helmet lamp beam ahead",
      tags=["spelunking", "cave", "exploration", "underground", "potholing", "adventure", "headlamp"])
def _(S):
    return [
        line("M2.5 21.5V11A9.5 9.5 0 0 1 21.5 11V21.5"),
        line("M2.5 21.5H21.5"),
        line("M6 16.5H12"),
        dot(14, 15.75, 1.75),
        line("M16.5 14.5L19 13"), line("M16.5 16.5H19"),
        line("M11.5 17L12 20"),
        line("M6 16.5L5 19.5"),
    ]


@icon("sandboarding", CAT, "Person riding a board down the slope of a sand dune with a spray of sand behind",
      tags=["dune", "desert", "sand surfing", "adventure sport", "slide", "board", "extreme sports"])
def _(S):
    return [
        line("M2.5 11C8 12 15 15 21.5 21.5"),
        line("M8 9.8L16 14.3"),
        line("M12 9.5L10.5 5.5"),
        dot(10, 3.5, 1.5),
        line(poly([(7.5, 6.5), (10.8, 7.3), (13.5, 5.5)], r=S.r * 0.5)),
        dot(3.5, 5.5, 0.9), dot(5.5, 7.5, 0.9), dot(3.2, 8, 0.9),
    ]


@icon("handheld-gps", CAT, "Rugged handheld device with a stubby antenna on top and a map screen with a route",
      tags=["gps unit", "navigation", "hiking", "geocaching", "trail map", "location", "outdoor navigation"])
def _(S):
    return [
        line("M8 5.5V2.5"),
        shell(rect(4, 5.5, 16, 16, pick(S, 2, 4))),
        detail(rect(8, 9, 8, 6, pick(S, 0.5, 1))),
        dot(12, 12, 1.1),
        dot(9, 18.5, 0.9), dot(12, 18.5, 0.9), dot(15, 18.5, 0.9),
    ]


@icon("ranger-hat", CAT, "Flat-brimmed campaign hat with a pinched crown and a hat band",
      tags=["park ranger", "campaign hat", "scout hat", "smokey", "forest service", "uniform", "brim hat"])
def _(S):
    return [
        line(poly([(7, 14.5), (8, 7), (12, 3), (16, 7), (17, 14.5)], r=S.r * 0.8)),
        line("M12 3.5V7"),
        line("M7.3 11.5h9.4"),
        shell(ellipse(12, 16, pick(S, 9.5, 9.2), 3.3)),
    ]


@icon("crampons", CAT, "Metal frame with sharp downward spikes and front points, strapped over the boot",
      tags=["ice climbing", "mountaineering", "glacier", "winter hiking", "spikes", "traction", "alpine"])
def _(S):
    pts = [(2.5, 8), (21.5, 8), (21.5, 11), (19.5, 11), (17.5, 20.5), (15.5, 11), (13.5, 11), (11.5, 20),
           (9.5, 11), (7.5, 11), (5.5, 20), (3.5, 11), (2.5, 11)]
    return [
        line(poly([(6, 8), (6, 3.5), (18, 3.5), (18, 8)], r=S.r * 0.8)),
        shell(poly(pts, closed=True)),
    ]
