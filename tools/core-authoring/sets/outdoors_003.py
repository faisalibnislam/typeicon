"""TypeIcon Core: outdoors (batch 003): water and climbing gear, camping shelters, fishing, travel bits.

Stick figures follow the sports set (solid head r 2.25 over 2 px limbs). Gear is drawn from the object itself in
front or side view. Line keeps corners sharp, Rounded fillets polylines and rounds containers.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "outdoors"


def L(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def wave(x0, x1, y, n=2, h=1.5):
    """Open wave line from x0 to x1 made of n crests (quadratic curves)."""
    w = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        d += f"Q{fmt(x0 + w * (i + 0.25))} {fmt(y - h)} {fmt(x0 + w * (i + 0.5))} {fmt(y)}Q{fmt(x0 + w * (i + 0.75))} {fmt(y + h)} {fmt(x0 + w * (i + 1))} {fmt(y)}"
    return d


# ============================================================================ chunk 1

@icon("wingsuit", CAT, "Flying person seen from above with arms and legs spread and webbing between them forming wings.",
      tags=["wingsuit flying", "skydiving", "base jumping", "flying suit", "extreme sport", "glide"])
def _(S):
    return [
        dot(12, 4.2, 2.25),
        shell(poly([(12, 8.5), (21.5, 12), (18, 21), (12, 17.5), (6, 21), (2.5, 12)], closed=True, r=S.r)),
        detail(seg(12, 12, 12, 16)),
    ]


@icon("beach-sun-shelter", CAT, "Half-dome pop-up beach shelter with an open front, standing on sand.",
      tags=["beach tent", "sun shade", "pop-up shelter", "sunshade", "beach", "sand", "shade"])
def _(S):
    return [
        shell("M3 17A9 9 0 0 1 21 17Z"),
        detail("M8 17A4 4 0 0 1 16 17"),
        line(wave(2, 22, 20.5, 4, 1)),
    ]


@icon("underwater-camera", CAT, "Camera inside a boxy waterproof housing with side handles and a round dome port.",
      tags=["underwater photography", "dive camera", "waterproof camera", "housing", "scuba", "snorkel"])
def _(S):
    return [
        shell(rect(5.5, 8, 13, 11, S.R)),
        detail(circle(12, 13.5, 3)),
        line(poly([(5.5, 11), (2.5, 11), (2.5, 16), (5.5, 16)], r=S.r)),
        line(poly([(18.5, 11), (21.5, 11), (21.5, 16), (18.5, 16)], r=S.r)),
        line(poly([(9.5, 8), (9.5, 4.5), (14.5, 4.5), (14.5, 8)], r=S.r)),
    ]


@icon("dive-computer", CAT, "Chunky wrist dive computer on a strap with a display showing a downward depth arrow.",
      tags=["dive watch", "scuba", "depth gauge", "diving", "wrist computer", "underwater"])
def _(S):
    return [
        shell(rect(5, 7, 14, 10, S.R)),
        detail(poly([(12, 9.5), (12, 14.5)])),
        detail(poly([(9.8, 12.3), (12, 14.5), (14.2, 12.3)], r=S.r * 0.6)),
        line(poly([(8, 7), (8.5, 2.5)])), line(poly([(16, 7), (15.5, 2.5)])),
        line(poly([(8, 17), (8.5, 21.5)])), line(poly([(16, 17), (15.5, 21.5)])),
    ]


@icon("scuba-regulator", CAT, "Diving regulator with a round purge button, a mouthpiece and a curving hose.",
      tags=["scuba", "diving", "second stage", "mouthpiece", "air hose", "underwater breathing"])
def _(S):
    return [
        shell(rect(3.5, 9, 11, 11, L(S, 2.5, 5.5))),
        dot(9, 14.5, 1.7),
        shell(rect(14.5, 12, 6, 5, L(S, 0.8, 2.2))),
        line("M9 9C9 5 12 3.5 19 4"),
    ]


@icon("privacy-tent", CAT, "Tall narrow pop-up tent with a zipped door and a small window, used as a camp shower or toilet.",
      tags=["shower tent", "changing tent", "pop-up tent", "camp toilet", "camping", "privacy shelter"])
def _(S):
    return [
        shell(poly([(5.5, 21), (5.5, 8), (12, 2.5), (18.5, 8), (18.5, 21)], closed=True, r=S.r * 1.3)),
        detail(poly([(9, 21), (9, 12.5), (15, 12.5), (15, 21)], r=S.r)),
        dot(12, 8.3, 1.2),
    ]


@icon("filter-straw", CAT, "Thick drinking straw with a bulging filter section, its lower end dipped in water.",
      tags=["water filter", "personal filter", "drinking straw", "purifier", "hiking water", "survival"])
def _(S):
    body = [(10.5, 2.5), (13.5, 2.5), (13.5, 6.5), (16, 9), (16, 14), (13.5, 16.5), (13.5, 21.5), (10.5, 21.5),
            (10.5, 16.5), (8, 14), (8, 9), (10.5, 6.5)]
    return [
        shell(poly(body, closed=True, r=S.r)),
        detail(seg(9.8, 11.5, 14.2, 11.5)),
        line(wave(2, 7.5, 19, 2, 1)), line(wave(16.5, 22, 19, 2, 1)),
    ]


@icon("climbing-chock", CAT, "Tapered metal wedge on a wire loop, the kind set in a rock crack.",
      tags=["nut", "stopper", "climbing protection", "trad climbing", "rock gear", "wedge"])
def _(S):
    return [
        shell(poly([(7.5, 3.5), (16.5, 3.5), (14, 13), (10, 13)], closed=True, r=S.r)),
        line(poly([(10.5, 13), (9, 17.5)]) + "A3.2 3.2 0 0 0 15 17.5L13.5 13"),
    ]


@icon("ice-screw", CAT, "Threaded tubular ice screw with teeth at the tip and a folding crank at the top.",
      tags=["ice climbing", "ice protection", "screw", "glacier", "mountaineering", "anchor"])
def _(S):
    return [
        shell(poly([(9.5, 7), (14.5, 7), (14.5, 21.5), (12, 19), (9.5, 21.5)], closed=True, r=S.r)),
        detail(seg(9.5, 12, 14.5, 10)), detail(seg(9.5, 16, 14.5, 14)),
        line(poly([(12, 7), (12, 3.5), (19, 3.5), (19, 7)], r=S.r)),
    ]


@icon("glacier-glasses", CAT, "Sunglasses with two lenses and solid dark side shields that cover the sides of the eyes.",
      tags=["sunglasses", "snow goggles", "mountaineering", "eyewear", "sun protection", "snow blindness"])
def _(S):
    return [
        shell(rect(6, 8, 5.5, 8, L(S, 1.5, 2.7))),
        shell(rect(12.5, 8, 5.5, 8, L(S, 1.5, 2.7))),
        line(seg(11.5, 10, 12.5, 10)),
        solid(poly([(6, 8.5), (2.5, 10), (2.5, 15), (6, 15.5)], closed=True)),
        solid(poly([(18, 8.5), (21.5, 10), (21.5, 15), (18, 15.5)], closed=True)),
    ]


# ============================================================================ chunk 2

@icon("clam-rake", CAT, "Short rake with long curved tines and a wire basket behind them, with a short handle.",
      tags=["clamming", "shellfish", "beach", "digging", "shellfish rake", "seafood", "tidal flat"])
def _(S):
    parts = [shell(rect(5, 4.5, 11, 8, S.R)), detail(seg(10.5, 4.5, 10.5, 12.5)),
             line(seg(16, 8.5, 21.5, 3.5))]
    for x in (6.5, 10.5, 14.5):
        parts.append(line(f"M{fmt(x)} 12.5V17Q{fmt(x)} 20.5 {fmt(x - 3)} 20.5"))
    return parts


@icon("fly-box", CAT, "Flat fly fishing box with two foam compartments each holding small flies.",
      tags=["fly fishing", "tackle box", "flies", "fishing", "angling", "lures"])
def _(S):
    parts = [shell(rect(2.5, 5, 19, 14, S.R)), detail(seg(12, 5, 12, 19))]
    for x in (7, 16.5):
        for y in (9.5, 14.5):
            parts.append(dot(x, y, 1.3))
            parts.append(line(seg(x + 1.3, y, x + 2.6, y - 1.2)))
    return parts


@icon("catch-and-release", CAT, "Fish held in a cupped bowl of hands just above a wave line, being returned to the water.",
      tags=["fishing", "release fish", "conservation", "angler", "fish", "hands"])
def _(S):
    fish = "M3.5 7.5C7 3.5 12 4.5 14 7.5C12 10.5 7 11.5 3.5 7.5Z"
    return [
        shell(fish),
        shell(poly([(14, 7.5), (19, 4.5), (19, 10.5)], closed=True, r=S.r * 0.6)),
        dot(6.3, 6.8, 0.9),
        line("M3 13.5C3.5 17 7 18 12 18C17 18 20.5 17 21 13.5"),
        line(wave(3, 21, 21, 3, 0.9)),
    ]


@icon("cliff-jumping", CAT, "Person leaping off a rock ledge in mid air above water, with a splash below.",
      tags=["cliff diving", "jumping", "swimming hole", "adventure", "tombstoning", "water"])
def _(S):
    return [
        dot(15.5, 4.5, 2.25),
        line(seg(11, 9, 20, 9)),
        line(seg(15.5, 7, 15.5, 13.5)),
        line(poly([(12.5, 17.5), (15.5, 13.5), (18.5, 17.5)], r=S.r)),
        line(poly([(2.5, 9), (7, 9), (7, 17), (9, 17)], r=S.r)),
        line(seg(7, 17, 7, 21.5)),
        line(wave(9.5, 22, 21, 3, 1)),
    ]


@icon("inflatable-dinghy", CAT, "Rubber boat with round side tubes and a small outboard motor at the back.",
      tags=["rubber boat", "raft", "zodiac", "boating", "tender", "outboard", "inflatable boat"])
def _(S):
    return [
        shell(rect(2.5, 8, 15.5, 6.5, L(S, 2.5, 3.2))),
        detail(seg(8, 8, 8, 14.5)), detail(seg(13, 8, 13, 14.5)),
        shell(rect(18.5, 6, 3, 5, L(S, 0, 1))),
        line(seg(20, 11, 20, 16.5)),
        line(wave(2, 22, 19.5, 4, 1)),
    ]


@icon("glass-skywalk", CAT, "U-shaped glass-floored platform reaching out from a cliff edge over a canyon.",
      tags=["glass walkway", "canyon", "viewing platform", "observation deck", "cliff", "scenic overlook"])
def _(S):
    u = [(3, 5), (17, 5), (21, 9), (21, 15), (17, 19), (3, 19), (3, 14.5), (15.5, 14.5), (16.5, 13.5), (16.5, 10.5),
         (15.5, 9.5), (3, 9.5)]
    return [
        shell(poly(u, closed=True, r=S.r)),
        line(seg(3, 2.5, 3, 21.5)),
    ]


@icon("dome-tent", CAT, "Rounded dome tent with two poles crossing over the top and a small zipped door.",
      tags=["camping", "tent", "shelter", "backpacking", "campsite", "outdoor sleeping"])
def _(S):
    return [
        shell("M2.5 19.5V17C2.5 10 7 5 12 5C17 5 21.5 10 21.5 17V19.5Z"),
        detail("M6 19.5C6 13 8 9 13.5 5.3"), detail("M18 19.5C18 13 16 9 10.5 5.3"),
        detail("M10 19.5V16.5H14V19.5"),
    ]


@icon("tunnel-tent", CAT, "Long low tent held up by a row of parallel hoops of decreasing height.",
      tags=["camping", "tent", "hoop tent", "family tent", "shelter", "campsite"])
def _(S):
    return [
        shell("M2.5 19.5V8.5C9 6 16 8.5 21.5 14.5V19.5Z"),
        detail(seg(8, 7.5, 8, 19.5)), detail(seg(14, 9.5, 14, 19.5)),
    ]


@icon("hammock-tent", CAT, "Hammock slung between two tree trunks with a peaked rain tarp above it.",
      tags=["hammock camping", "tarp", "rain fly", "backpacking", "camping", "sleeping"])
def _(S):
    return [
        shell(poly([(3.5, 8.5), (12, 3), (20.5, 8.5)], closed=True, r=S.r)),
        line(seg(3.5, 8.5, 3.5, 21.5)), line(seg(20.5, 8.5, 20.5, 21.5)),
        line("M3.5 14.5Q12 21 20.5 14.5"),
    ]


@icon("pop-up-camper", CAT, "Small trailer with a hard box body and canvas tent wings folded out at both ends.",
      tags=["camper trailer", "folding camper", "caravan", "rv", "camping", "tent trailer"])
def _(S):
    return [
        shell(rect(6.5, 9, 11, 8.5, S.R)),
        shell(poly([(6.5, 9), (2, 13), (2, 17.5), (6.5, 17.5)], closed=True, r=S.r * 0.6)),
        shell(poly([(17.5, 9), (22, 13), (22, 17.5), (17.5, 17.5)], closed=True, r=S.r * 0.6)),
        shell(circle(12, 20, 1.5)),
    ]


@icon("helter-skelter", CAT, "Tall striped conical tower with a flag on top and a slide spiralling around it.",
      tags=["fairground", "slide", "amusement park", "funfair", "carnival", "seaside"])
def _(S):
    return [
        shell(poly([(7.5, 21.5), (10, 7), (14, 7), (16.5, 21.5)], closed=True, r=S.r)),
        detail(seg(9.6, 11, 14.4, 12.5)), detail(seg(8.8, 15.5, 15.2, 17.5)),
        line(seg(12, 7, 12, 2.5)),
        solid(poly([(12, 2.5), (17, 4), (12, 5.5)], closed=True)),
    ]


@icon("horseshoe-toss", CAT, "Horseshoe tossed through the air toward a metal stake planted in the ground.",
      tags=["horseshoes", "lawn game", "backyard game", "picnic", "throwing game", "stake"])
def _(S):
    return [
        shell("M4 3.5H8V10.5A2 2 0 0 0 12 10.5V3.5H16V10.5A6 6 0 0 1 4 10.5Z"),
        line(seg(19.5, 21.5, 19.5, 11)),
        line(seg(15, 21.5, 22, 21.5)),
    ]


@icon("disc-golf-basket", CAT, "Metal basket on a pole with chains hanging above it to catch a flying disc.",
      tags=["frisbee golf", "disc golf", "target", "chains", "park game", "goal"])
def _(S):
    return [
        dot(12, 3.2, 1.4),
        line(seg(12, 3.2, 12, 14)),
        line(seg(3.5, 7, 20.5, 7)),
        line(seg(4.5, 7, 8, 14)), line(seg(19.5, 7, 16, 14)),
        shell(poly([(5.5, 14), (18.5, 14), (16.5, 19), (7.5, 19)], closed=True, r=S.r)),
        line(seg(12, 19, 12, 22)),
    ]


@icon("compression-sack", CAT, "Cylindrical stuff sack squeezed by vertical straps, with a cinched drawstring top.",
      tags=["stuff sack", "sleeping bag", "packing", "backpacking", "camping", "gear bag"])
def _(S):
    return [
        shell(rect(5, 8.5, 14, 12.5, S.R)),
        shell(rect(8.5, 4, 7, 4.5, L(S, 0.8, 1.6))),
        detail(seg(9.5, 8.5, 9.5, 21)), detail(seg(14.5, 8.5, 14.5, 21)),
    ]


@icon("portaledge", CAT, "Hanging tent platform suspended by straps from a single anchor point above.",
      tags=["big wall", "hanging tent", "cliff camping", "climbing", "aid climbing", "bivouac"])
def _(S):
    return [
        line(seg(3, 3, 21, 3)),
        dot(12, 3, 1.6),
        line(seg(12, 3, 5, 15)), line(seg(12, 3, 19, 15)),
        shell(rect(3.5, 15, 17, 4, L(S, 1, 1.8))),
        line("M8.5 15A3.5 3.5 0 0 1 15.5 15"),
    ]


# ============================================================================ chunk 3

def bubble(S, x, y, w, h, tail_left=True):
    """Speech bubble with a tail under one corner."""
    if tail_left:
        pts = [(x, y), (x + w, y), (x + w, y + h), (x + 4, y + h), (x + 1.5, y + h + 2.2), (x + 1.5, y + h), (x, y + h)]
    else:
        pts = [(x, y), (x + w, y), (x + w, y + h), (x + w - 1.5, y + h), (x + w - 1.5, y + h + 2.2), (x + w - 4, y + h), (x, y + h)]
    return shell(poly(pts, closed=True, r=S.r * 0.7))


@icon("gravity-water-filter", CAT, "Water bag hanging from a branch with a hose running down into a bottle.",
      tags=["water filter", "hydration", "camping", "backpacking", "purifier", "hose", "drinking water"])
def _(S):
    return [
        line(seg(2.5, 3, 15, 3)),
        line(seg(8, 3, 8, 5.5)),
        shell(rect(3.5, 5.5, 9, 8, S.R)),
        detail(wave(5, 11, 9.5, 1, 1)),
        line("M8 13.5Q8 18.5 15 18.5"),
        shell(rect(15, 14.5, 6, 7, L(S, 1.5, 2.5))),
    ]


@icon("tripod-stool", CAT, "Three-legged folding camp stool with a triangular fabric seat.",
      tags=["camp stool", "folding stool", "camping seat", "fishing stool", "chair", "portable seat"])
def _(S):
    return [
        shell(poly([(4, 7), (20, 7), (12, 12)], closed=True, r=S.r), stroke_miterlimit="2"),
        line(seg(5.5, 9, 7, 21.5)), line(seg(18.5, 9, 17, 21.5)), line(seg(12, 12, 12, 21.5)),
    ]


@icon("tip-up-flag", CAT, "Crossed wooden sticks over an ice fishing hole with a small flag on a spring arm.",
      tags=["ice fishing", "tip-up", "fishing", "winter", "frozen lake", "angling"])
def _(S):
    return [
        shell(ellipse(12, 19.2, 6, 2.2)),
        line(seg(3.5, 14, 20.5, 16.5)), line(seg(3.5, 16.5, 20.5, 14)),
        line("M12 15.3C12 10 13.5 6.5 14.5 3.5"),
        solid(poly([(14.5, 3.5), (20, 5.5), (13.6, 7.5)], closed=True)),
    ]


@icon("fish-trap", CAT, "Conical woven basket trap with a funnel mouth at the wide end.",
      tags=["fishing", "creel", "wicker", "minnow trap", "lobster pot", "catch", "basket"])
def _(S):
    return [
        shell(poly([(3, 5), (21, 9.5), (21, 14.5), (3, 19)], closed=True, r=S.r)),
        detail("M3 5C7 9 7 15 3 19"),
        detail(seg(12, 7.4, 12, 16.6)), detail(seg(17, 8.6, 17, 15.4)),
    ]


@icon("mounted-fish", CAT, "Fish curved as if leaping, mounted on an oval wooden wall plaque.",
      tags=["trophy fish", "taxidermy", "plaque", "wall mount", "fishing", "catch", "decor"])
def _(S):
    plaque = poly([(2.5, 12), (6, 4.5), (18, 4.5), (21.5, 12), (18, 19.5), (6, 19.5)], closed=True, r=L(S, 0, 4))
    return [
        shell(plaque),
        detail("M6.5 13C8 9 12 8.5 14.5 11.5C12 15 8.5 15.5 6.5 13Z"),
        detail(poly([(14.5, 11.5), (18, 8.5), (18, 14.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("postcard-rack", CAT, "Tall spinning wire rack on a pole with postcards standing out on both sides in three tiers.",
      tags=["postcards", "souvenir shop", "gift shop", "tourist", "spinner rack", "display stand"])
def _(S):
    parts = [line(seg(12, 2.5, 12, 21.5)), line(seg(7.5, 21.5, 16.5, 21.5))]
    for y in (3.5, 9.5, 15.5):
        parts.append(solid(rect(3, y, 6.5, 4, L(S, 0, 0.8))))
        parts.append(solid(rect(14.5, y, 6.5, 4, L(S, 0, 0.8))))
    return parts



@icon("bill-folder", CAT, "Leather check folder lying slightly open with a receipt and a pen sticking out.",
      tags=["check presenter", "restaurant bill", "receipt", "tab", "payment", "waiter"])
def _(S):
    return [
        shell(rect(3.5, 9, 17, 12, S.R)),
        detail(seg(3.5, 12.5, 20.5, 12.5)),
        line(poly([(7, 9), (7, 4), (13, 4), (13, 9)], r=S.r)),
        line(seg(17, 9, 17, 2.5)),
    ]


@icon("ski-bag", CAT, "Long padded ski bag with a shoulder strap and the outlines of two ski tips inside.",
      tags=["ski case", "snowboard bag", "luggage", "winter travel", "skis", "equipment bag"])
def _(S):
    return [
        shell(rect(7, 2.5, 10, 19, S.R)),
        detail("M10.5 18.5V8.5Q10.5 6.5 11.5 5.5"), detail("M13.5 18.5V8.5Q13.5 6.5 12.5 5.5"),
        line("M7 6Q2.5 12 7 18"),
    ]


@icon("pocket-translator", CAT, "Small handheld translator device with a speaker grille and two speech bubbles above it.",
      tags=["translation", "language", "travel", "interpreter", "gadget", "speech", "foreign language"])
def _(S):
    return [
        bubble(S, 2.5, 2, 9, 5, True),
        bubble(S, 12.5, 3, 9, 5, False),
        shell(rect(6.5, 13, 11, 8.5, S.R)),
        detail(seg(9.5, 16, 14.5, 16)), detail(seg(9.5, 19, 14.5, 19)),
    ]


@icon("floating-market", CAT, "Narrow boat piled with fruit and a vendor in a conical hat standing at the stern.",
      tags=["boat vendor", "river market", "street food", "southeast asia", "canal", "fruit seller"])
def _(S):
    return [
        shell(poly([(2, 15), (22, 15), (19, 19.5), (5, 19.5)], closed=True, r=S.r)),
        dot(5.5, 12.5, 1.6), dot(9.5, 12.5, 1.6), dot(7.5, 9, 1.6),
        solid(poly([(17.5, 3.5), (21.5, 8), (13.5, 8)], closed=True)),
        line(seg(17.5, 9.5, 17.5, 14)),
    ]


@icon("canyoning", CAT, "Person rappelling down a rope beside a waterfall into a pool below.",
      tags=["canyoneering", "rappel", "abseil", "adventure sport", "gorge", "waterfall", "rope"])
def _(S):
    return [
        line(seg(3.5, 2.5, 3.5, 15.5)),
        line(seg(5.5, 2.5, 9, 9.5)),
        dot(12, 6, 2),
        line(poly([(11, 8.5), (9, 14.5), (5, 15.5)], r=S.r)),
        line(poly([(11.3, 8.5), (8.6, 10)], r=S.r)),
        line("M19.5 2.5Q21 6 19.5 9.5Q18 13 19.5 16.5"),
        line(wave(7, 22, 20, 3, 1)),
    ]


@icon("zorbing", CAT, "Person inside a large clear inflatable ball rolling down a grassy slope.",
      tags=["inflatable ball", "hamster ball", "hill roll", "adventure", "fun", "sphereing"])
def _(S):
    return [
        shell(circle(9.5, 9.5, 6.5)),
        dot(9.5, 6.3, 1.5),
        line(seg(9.5, 8, 9.5, 11.5)),
        line(seg(7.2, 9.2, 11.8, 9.2)),
        line(poly([(8, 13.6), (9.5, 11.5), (11, 13.6)])),
        line(seg(2, 13.7, 22, 21)),
    ]


@icon("camel-ride", CAT, "Two-humped camel with a rider sitting in the saddle between the humps.",
      tags=["desert", "camel trek", "tourist", "caravan", "riding", "sahara"])
def _(S):
    return [
        shell("M3 13C3 10 5.5 9.5 7.5 11C9 12 10.5 12 12 11C14 9.5 17 10 17 13V15.5H3Z"),
        line(poly([(16.5, 12), (19, 8), (19.5, 5.5)], r=S.r)),
        shell(poly([(19, 5), (22, 6.5), (21.5, 8.5), (18.5, 7.5)], closed=True, r=S.r * 0.4)),
        line(seg(5, 15.5, 5, 21.5)), line(seg(9, 15.5, 9, 21.5)), line(seg(13.5, 15.5, 13.5, 21.5)),
        dot(9.8, 4.5, 1.8),
        line(seg(9.8, 6.8, 9.8, 10.5)),
    ]


@icon("ice-climber", CAT, "Person climbing a frozen icefall, holding an ice tool in each raised hand.",
      tags=["ice climbing", "mountaineering", "icefall", "frozen waterfall", "winter sport", "ice axes"])
def _(S):
    return [
        line(poly([(21, 2.5), (19, 7), (21, 12), (19, 17), (21, 21.5)])),
        line(seg(4.5, 4, 8, 4)), line(seg(11, 4, 14.5, 4)),
        dot(9.5, 8, 2.1),
        line(poly([(6.5, 4), (6.5, 7.5), (8.6, 10.5)], r=S.r)),
        line(poly([(12.5, 4), (12.5, 7.5), (10.4, 10.5)], r=S.r)),
        line(seg(9.5, 10.5, 9.5, 15.5)),
        line(poly([(6.5, 21.5), (6.5, 19), (9.5, 15.5), (12.5, 18.5), (13.5, 21.5)], r=S.r)),
    ]


@icon("park-pass", CAT, "Plastic pass card with a mountain and sun, hanging on a cord from a car mirror stem.",
      tags=["national park", "parking permit", "entry pass", "hang tag", "annual pass", "windshield"])
def _(S):
    return [
        line(seg(4, 3.5, 20, 3.5)),
        line(seg(12, 3.5, 12, 9)),
        shell(rect(5, 9, 14, 12, S.R)),
        detail(poly([(7, 18), (10.5, 13), (14, 18)], r=S.r * 0.5)),
        dot(15.5, 13.5, 1.1),
    ]


@icon("trail-register", CAT, "Small wooden box on a post with its lid open showing a notebook inside.",
      tags=["trailhead", "sign-in", "hiking log", "logbook", "summit register", "ranger"])
def _(S):
    return [
        shell(rect(4.5, 11, 15, 6, S.R)),
        line(poly([(5, 11), (6.5, 3.5), (17.5, 3.5), (19, 11)], r=S.r)),
        solid(poly([(9, 6), (15, 6), (15, 9), (9, 9)], closed=True)),
        line(seg(12, 17, 12, 22)),
    ]


# ============================================================================ chunk 4

@icon("rv-dump-station", CAT, "Ground inlet with a flip lid and a hose running into it from a small camper.",
      tags=["sewer hookup", "rv park", "waste tank", "campground", "motorhome", "septic"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 10, 9, S.R)),
        detail(seg(5, 7, 10, 7)),
        shell(circle(6, 14.5, 1.6)),
        line("M12.5 10C18 10 18 13 18 16"),
        shell(rect(14.5, 16, 7, 4.5, L(S, 1, 1.5))),
        line(poly([(14.5, 16), (16.5, 12.5)])),
    ]


@icon("lie-flat-seat", CAT, "Airline seat reclined fully flat into a bed inside a curved privacy shell.",
      tags=["business class", "flight", "sleeper seat", "suite", "air travel", "first class"])
def _(S):
    return [
        line("M2.5 20V9Q2.5 3.5 8 3.5H16Q21.5 3.5 21.5 9V20"),
        shell(rect(4.5, 13, 15, 3.5, L(S, 0.8, 1.7))),
        shell(rect(4.5, 9.5, 4.5, 3, L(S, 0.5, 1.2))),
        line(seg(7, 16.5, 7, 20)), line(seg(17, 16.5, 17, 20)),
    ]


@icon("spoon-lure", CAT, "Curved oval metal spoon lure with a split ring at one end and a hook at the other.",
      tags=["fishing lure", "tackle", "bait", "angling", "fishing", "hook"])
def _(S):
    spoon = "M12 5.5C19 7.5 19 16 12 18C5 16 5 7.5 12 5.5Z" if S.name == "line" else \
        "M12 5.5C16.5 5.5 18 8.5 18 11.7C18 15.2 15.5 18 12 18C8.5 18 6 15.2 6 11.7C6 8.5 7.5 5.5 12 5.5Z"
    return [
        shell(circle(12, 3.4, 1.4)),
        shell(spoon),
        detail(seg(12, 8.5, 12, 15)),
        line("M12 18V20.2"),
        line("M12 20.2Q12 22 9.6 21.4"),
    ]


@icon("phone-dry-pouch", CAT, "Clear waterproof pouch with a sealed top holding a phone, on a neck lanyard.",
      tags=["waterproof case", "dry bag", "phone case", "kayak", "beach", "water sports"])
def _(S):
    return [
        line(poly([(7.5, 8), (12, 2.5), (16.5, 8)], r=S.r)),
        shell(rect(5, 8, 14, 13.5, S.R)),
        detail(seg(5, 11.3, 19, 11.3)),
        detail(rect(9.5, 13.5, 5, 6, L(S, 0.6, 1.2))),
    ]


@icon("fishing-line-spool", CAT, "Spool of fishing line with a loose end trailing off the bottom.",
      tags=["monofilament", "braid", "tackle", "angling", "thread", "line"])
def _(S):
    return [
        shell(rect(3, 4, 3.5, 16, L(S, 0.6, 1.7))),
        shell(rect(17.5, 4, 3.5, 16, L(S, 0.6, 1.7))),
        shell(rect(6.5, 6.5, 11, 11, 0)),
        detail(seg(6.5, 9.2, 17.5, 11.8)), detail(seg(6.5, 13.2, 17.5, 15.8)),
        line("M11 17.5Q11 21.5 16 21"),
    ]


@icon("treble-hook", CAT, "Three barbed fishing hooks joined back to back on one shank with an eye at the top.",
      tags=["fishing hook", "tackle", "barb", "angling", "lure", "triple hook"])
def _(S):
    return [
        shell(circle(12, 3.8, 1.6)),
        line(seg(12, 5.4, 12, 11.5)),
        line("M12 11.5C8 11.5 5.5 14 6 19.5"), line(poly([(6, 19.5), (8.2, 17.5)])),
        line("M12 11.5C16 11.5 18.5 14 18 19.5"), line(poly([(18, 19.5), (15.8, 17.5)])),
        line(seg(12, 11.5, 12, 20)), line(poly([(12, 20), (10, 17.8)])),
    ]


@icon("pocket-chainsaw", CAT, "Flexible toothed saw chain with a ring handle at each end, pulled into a U.",
      tags=["survival saw", "wire saw", "camping", "bushcraft", "cutting", "firewood"])
def _(S):
    parts = [
        shell(circle(6, 4.5, 2)), shell(circle(18, 4.5, 2)),
        line("M6 7.5V12A6 6 0 0 0 18 12V7.5"),
    ]
    for ang in (45, 90, 135):
        a = polar(12, 12, 6, ang)
        b = polar(12, 12, 8.6, ang)
        parts.append(line(seg(a[0], a[1], b[0], b[1])))
    parts.append(line(seg(6, 10, 3.6, 10))); parts.append(line(seg(18, 10, 20.4, 10)))
    return parts


@icon("chuck-box", CAT, "Wooden camp kitchen box with shelves inside and a front door folded down to form a table.",
      tags=["camp kitchen", "camping", "cooking box", "outdoor cooking", "campsite", "supplies"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 9.5, S.R)),
        detail(seg(3.5, 7.2, 20.5, 7.2)), detail(seg(12, 2.5, 12, 7.2)),
        shell(rect(2.5, 14.5, 19, 2.5, L(S, 0, 1.2))),
        line(seg(5, 17, 5, 21.5)), line(seg(19, 17, 19, 21.5)),
    ]


@icon("hot-tent", CAT, "Canvas tent with a stovepipe chimney through its roof and smoke rising.",
      tags=["wood stove", "winter camping", "bushcraft", "tent stove", "chimney", "cold weather camping"])
def _(S):
    return [
        shell(poly([(2.5, 21), (11, 9), (19.5, 21)], closed=True, r=S.r), stroke_miterlimit="2"),
        detail(poly([(8, 21), (11, 15.5), (14, 21)], r=S.r)),
        line(seg(16, 15.5, 16, 6.5)),
        line("M16 4.8C18 3.8 14 2.8 16 2"),
    ]


@icon("swim-raft", CAT, "Square floating platform on a lake with a short ladder on one side.",
      tags=["swimming platform", "lake", "dock", "float", "diving raft", "summer camp"])
def _(S):
    return [
        shell(poly([(6.5, 4.5), (19.5, 4.5), (22, 9.5), (22, 12.5), (2, 12.5), (2, 9.5)], closed=True, r=S.r)),
        detail(seg(2, 9.5, 22, 9.5)),
        line(seg(16, 12.5, 16, 19.5)), line(seg(19.5, 12.5, 19.5, 19.5)), line(seg(16, 16.5, 19.5, 16.5)),
        line(wave(2, 13, 18, 3, 1)),
    ]


@icon("seat-map", CAT, "Top-down aircraft cabin with rows of seats either side of an aisle and one seat enlarged.",
      tags=["seat selection", "flight", "airplane seats", "cabin layout", "booking", "airline"])
def _(S):
    body = "M4 21.5V11L12 2.5L20 11V21.5Z" if S.name == "line" else "M4 21.5V10C4 5.5 8 2.5 12 2.5C16 2.5 20 5.5 20 10V21.5Z"
    parts = [shell(body)]
    for y in (7.5, 12.6, 17.7):
        parts.append(sq(6.5, y, 4, 2.8, L(S, 0, 0.8)))
        if y != 12.6:
            parts.append(sq(13.5, y, 4, 2.8, L(S, 0, 0.8)))
    parts.append(sq(12.8, 12, 5.4, 4.2, L(S, 0, 1)))
    return parts



@icon("rocket-stove", CAT, "L-shaped metal stove with a fuel opening low on the side, a flame in the chimney and a pot on top.",
      tags=["camp stove", "wood burning stove", "cooking", "survival", "backpacking", "efficient stove"])
def _(S):
    flame = "M14 11.5C11.5 10 12.5 8 13.6 6.3C14.4 8 16.6 9.4 14 11.5Z"
    return [
        shell(rect(7, 2.5, 14, 3.5, L(S, 0.6, 1.5))),
        solid(flame),
        shell(poly([(10, 12), (18, 12), (18, 21.5), (3, 21.5), (3, 16.5), (10, 16.5)], closed=True, r=S.r)),
        detail(seg(5.5, 19, 8.5, 19)),
    ]


@icon("freeze-dried-meal", CAT, "Stand-up foil meal pouch with a torn-open top, a spoon sticking out and steam rising.",
      tags=["dehydrated food", "backpacking meal", "camp food", "trail food", "pouch", "instant meal"])
def _(S):
    return [
        shell(poly([(5.5, 9), (8, 7.5), (10.5, 9), (13, 7.5), (15.5, 9), (18.5, 7.5), (19.5, 21), (4.5, 21)], closed=True, r=S.r * 0.6)),
        detail(seg(6, 13, 18, 13)),
        line(seg(15, 8.5, 18, 3.5)),
        solid(ellipse(18.6, 3.2, 1.3, 1.9)),
        line("M9 5.8C7.5 4.6 10.5 3.6 9 2.4"),
    ]


@icon("trail-mix", CAT, "Small resealable bag filled with a jumble of nuts, raisins and candy pieces.",
      tags=["snack", "hiking food", "gorp", "nuts", "dried fruit", "granola"])
def _(S):
    return [
        shell(poly([(5, 4.5), (19, 4.5), (20, 21), (4, 21)], closed=True, r=S.r)),
        detail(seg(5, 8, 19, 8)),
        dot(9, 13, 1.8), dot(14.5, 12.5, 1.5), dot(11.5, 17.3, 1.6), dot(16, 17.5, 1.3),
    ]


@icon("flint-and-steel", CAT, "C-shaped steel striker beside a flint stone with sparks flying between them.",
      tags=["fire starter", "bushcraft", "survival", "camping", "spark", "tinder"])
def _(S):
    return [
        line(poly([(10, 11), (6, 11), (3.5, 13.5), (3.5, 17.5), (6, 20), (10, 20)], r=S.r)),
        shell(poly([(12.5, 15), (16, 11.5), (21, 14.5), (20, 20), (13.5, 20)], closed=True, r=S.r)),
        line(seg(9.5, 7.5, 7.5, 4.5)), line(seg(14, 7.5, 14, 4)), line(seg(18.5, 8, 21, 5.5)),
    ]


@icon("tinder-bundle", CAT, "Loose nest of dry fibers with a glowing ember on top and a curl of smoke.",
      tags=["fire starting", "bird nest", "bushcraft", "survival", "campfire", "ember"])
def _(S):
    return [
        shell("M3.5 12.5Q12 10.5 20.5 12.5Q20.5 19.5 12 20Q3.5 19.5 3.5 12.5Z"),
        detail("M7 15Q9 13.5 11 15.5"), detail("M12.5 16Q15 14.5 17.5 16"),
        dot(12, 8.3, 1.6),
        line("M12 5.5C10.5 4.3 13.5 3.3 12 2.3"),
    ]


@icon("solar-lantern", CAT, "Collapsible cube lantern with a small solar panel on top and light rays around it.",
      tags=["camping light", "solar light", "rechargeable", "lamp", "camp lighting", "inflatable lantern"])
def _(S):
    return [
        shell(poly([(8.5, 4), (15.5, 4), (17, 8), (7, 8)], closed=True, r=S.r * 0.5)),
        shell(rect(6.5, 10, 11, 11, S.R)),
        dot(12, 15.5, 1.6),
        line(seg(2.5, 13, 4.5, 13)), line(seg(19.5, 13, 21.5, 13)),
        line(seg(2.5, 18, 4.5, 18)), line(seg(19.5, 18, 21.5, 18)),
    ]


@icon("uv-water-purifier", CAT, "Pen-shaped UV purifier with a glowing tip dipped into a water bottle.",
      tags=["water purification", "sterilizer", "hiking", "uv light", "travel", "clean water"])
def _(S):
    return [
        shell(poly([(9, 8.5), (15, 8.5), (15, 10.5), (18.5, 13), (18.5, 21.5), (5.5, 21.5), (5.5, 13), (9, 10.5)], closed=True, r=S.r)),
        shell(rect(10.5, 2, 3, 8, L(S, 0.5, 1.4))),
        dot(12, 14.3, 1.3),
        line(seg(8.5, 12.5, 9.8, 13.5)), line(seg(15.5, 12.5, 14.2, 13.5)),
        line(wave(8, 16, 18.5, 2, 0.8)),
    ]


@icon("bear-spray", CAT, "Spray canister with a safety clip on the trigger, held in a belt holster clip.",
      tags=["bear deterrent", "pepper spray", "wildlife safety", "hiking safety", "backcountry", "protection"])
def _(S):
    return [
        shell(rect(8, 9.5, 8.5, 12, S.R)),
        shell(rect(9.5, 5, 5.5, 4.5, L(S, 0.6, 1.4))),
        line(poly([(15, 6.5), (19.5, 6.5)], r=S.r)),
        line(poly([(15, 9.5), (18.5, 11.5)], r=S.r)),
        line(poly([(8, 13), (4.5, 13), (4.5, 19), (8, 19)], r=S.r)),
    ]


# ============================================================================ chunk 5

def rot_d(d, deg, cx=12.0, cy=12.0):
    from geometry import path_to_d, rotation, transform_path
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


@icon("avalanche-airbag", CAT, "Backpack with a large inflated airbag arching up and around the wearer's head.",
      tags=["avalanche safety", "backcountry skiing", "snow safety", "rescue", "mountain", "abs pack"])
def _(S):
    return [
        line("M3.5 14C2 7 6.5 2.5 12 2.5C17.5 2.5 22 7 20.5 14"),
        dot(12, 7.5, 2.1),
        shell(rect(5.5, 12.5, 13, 9, S.R)),
        detail(seg(12, 12.5, 12, 21.5)),
    ]


@icon("rescue-throw-bag", CAT, "Small drawstring bag with a rope trailing out of it in a loose arc, as if thrown.",
      tags=["water rescue", "rope bag", "river safety", "whitewater", "kayak", "lifesaving"])
def _(S):
    return [
        shell("M4.5 9.5H13.5L15 19.5Q15 21.5 13 21.5H5Q3 21.5 3 19.5Z"),
        line(poly([(6, 9.5), (6, 6.5), (12, 6.5), (12, 9.5)], r=S.r)),
        line("M9 6.5C9 2.5 15 2.5 17 5.5C19 8.5 15.5 11 18.5 13.5C21 15.5 21.5 18 21.5 20.5"),
    ]


@icon("climbing-topo", CAT, "Cliff outline with two dotted climbing routes running up it, each ending in a larger anchor dot.",
      tags=["route map", "crag", "rock climbing", "guidebook", "climbing route", "bouldering"])
def _(S):
    parts = [line(poly([(3, 21.5), (3, 8), (6.5, 5.5), (10, 7), (14, 3.5), (18, 6), (21, 5), (21, 21.5)], r=S.r))]
    for pts, top in ((((7.5, 19), (9.3, 15.5), (7.5, 12), (9.3, 8.8)), (8.4, 6.8)),
                     (((16.5, 19), (14.7, 15.5), (16.5, 12), (14.7, 8.8)), (15.6, 6.8))):
        for x, y in pts:
            parts.append(dot(x, y, 1.0))
    return parts


@icon("snow-cannon", CAT, "Cylindrical snowmaking fan on a wheeled stand, spraying a plume of snow.",
      tags=["snowmaking", "ski resort", "artificial snow", "snow gun", "winter", "slope"])
def _(S):
    parts = [
        shell(rect(2.5, 6.5, 10, 7.5, L(S, 1, 2.5))),
        detail(seg(7.5, 6.5, 7.5, 14)),
        line(seg(5, 14, 5, 18.5)), line(seg(10, 14, 10, 18.5)),
        shell(circle(5, 20, 1.5)), shell(circle(10, 20, 1.5)),
    ]
    for x, y, r in ((15.8, 8, 1), (19, 6, 0.9), (21, 9.5, 1), (17.5, 11, 0.9), (20, 13.5, 0.9), (15.5, 14, 0.8)):
        parts.append(dot(x, y, r))
    return parts


@icon("wakeboard", CAT, "Short wide wakeboard seen from above with two foot bindings mounted across the middle.",
      tags=["water sports", "wake", "lake", "towed", "board", "cable park"])
def _(S):
    board = poly([(2, 12), (5.5, 7.5), (18.5, 7.5), (22, 12), (18.5, 16.5), (5.5, 16.5)], closed=True, r=L(S, 0, 3))
    return [
        shell(rot_d(board, -30)),
        Part("dot", rot_d(rect(8.2, 9.5, 2.6, 5, L(S, 0, 0.8)), -30)),
        Part("dot", rot_d(rect(13.2, 9.5, 2.6, 5, L(S, 0, 0.8)), -30)),
    ]


@icon("dive-weight-belt", CAT, "Weight belt laid in a ring with a quick-release buckle at the top and lead weights threaded on it.",
      tags=["scuba", "diving", "ballast", "lead weights", "underwater", "freediving"])
def _(S):
    return [
        line(rect(4, 4, 16, 16, L(S, 6.5, 8))),
        solid(rect(2, 8.5, 4, 7, L(S, 0, 0.8))), solid(rect(18, 8.5, 4, 7, L(S, 0, 0.8))),
        solid(rect(8.5, 18, 7, 4, L(S, 0, 0.8))),
        Part("dot", rect(10, 2.8, 4, 2.4, L(S, 0, 0.6))),
    ]


@icon("fly-tying-vise", CAT, "Small bench vise on a stand holding a tiny hook, with a thread bobbin hanging from it.",
      tags=["fly fishing", "fly tying", "craft", "hook", "angler", "bobbin"])
def _(S):
    return [
        line(seg(3.5, 21.5, 13.5, 21.5)),
        line(seg(8.5, 21.5, 8.5, 14.5)),
        shell(rect(5, 10, 7, 4.5, L(S, 0.8, 1.6))),
        line("M12 12.2H19A2.2 2.2 0 0 0 19 7.8"),
        line(seg(16.5, 12.2, 16.5, 16.5)),
        shell(rect(15, 16.5, 3, 4.5, L(S, 0.5, 1.2))),
    ]


@icon("photo-point", CAT, "Signboard on a post showing a camera symbol, marking a scenic photo spot.",
      tags=["scenic viewpoint", "overlook", "photography", "sign", "tourist", "lookout"])
def _(S):
    return [
        shell(rect(3.5, 3, 17, 12, S.R)),
        detail(rect(7.5, 6.3, 9, 5.4, L(S, 0.6, 1.2))),
        dot(12, 9, 1.25),
        line(seg(12, 15, 12, 22)),
    ]


@icon("scratch-map", CAT, "World map sheet with some landmasses scratched off to show the colour beneath.",
      tags=["travel tracker", "countries visited", "world map", "travel poster", "wall map", "souvenir"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 17, S.R)),
        Part("dot", "M5.5 8.5C7 6.6 9.5 6.8 10.5 8.5C11 11 9 12.8 7 12.5C5.5 12.2 5 10 5.5 8.5Z"),
        detail("M13 7.8Q16.5 6.5 18.5 8.5Q18 12 15.5 12Q12.5 11 13 7.8Z"),
        Part("dot", "M8 15.5Q11 14.5 13 16.3Q12 18 9.5 18Q7.5 17.5 8 15.5Z"),
    ]


@icon("camper-awning", CAT, "Camper side with a striped awning rolled out on two poles over the doorway.",
      tags=["rv awning", "caravan", "campsite", "shade", "motorhome", "camping"])
def _(S):
    return [
        shell(poly([(5, 4.5), (19, 4.5), (22, 11), (2, 11)], closed=True, r=S.r * 0.6)),
        detail(seg(9.5, 4.5, 8.5, 11)), detail(seg(14.5, 4.5, 15.5, 11)),
        line(seg(3, 11, 3, 21.5)), line(seg(21, 11, 21, 21.5)),
        shell(rect(9, 14, 6, 7.5, L(S, 0.5, 1.2))),
    ]


@icon("mobile-boarding-pass", CAT, "Smartphone screen showing a small aircraft above a square QR code.",
      tags=["digital boarding pass", "flight", "airline app", "check-in", "qr code", "e-ticket"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 13, 19, S.R)),
        line(seg(12, 4.2, 12, 10.6)), line(poly([(8.8, 9), (12, 6.6), (15.2, 9)], r=S.r)),
        line(poly([(10.4, 11.6), (12, 10.4), (13.6, 11.6)], r=S.r)),
        sq(8.3, 13.6, 2.6, 2.6), sq(13.1, 13.6, 2.6, 2.6), sq(8.3, 17.6, 2.6, 2.6), sq(13.1, 17.6, 1.1, 1.1),
        sq(14.6, 19.1, 1.1, 1.1),
    ]


@icon("table-number", CAT, "Small stand holding an upright card with a large number one, on a table.",
      tags=["restaurant", "wedding", "reception", "banquet", "seating", "table card"])
def _(S):
    return [
        shell(rect(6.5, 2.5, 11, 13, L(S, 1, 2))),
        detail(poly([(10, 6.8), (12.5, 5.3), (12.5, 12.5)], r=S.r * 0.5)),
        line(seg(12, 15.5, 12, 20)),
        line(seg(7, 20.5, 17, 20.5)),
    ]


@icon("folded-napkin", CAT, "Cloth napkin folded into a tall pleated fan standing in a wine glass.",
      tags=["table setting", "dining", "restaurant", "wedding", "serviette", "tablescape"])
def _(S):
    return [
        line(poly([(8.5, 9), (6.5, 3.5), (9.5, 5.5), (12, 2.5), (14.5, 5.5), (17.5, 3.5), (15.5, 9)], r=S.r)),
        line(seg(12, 5, 12, 9)),
        shell("M6.5 9H17.5Q17.5 16.5 12 16.5Q6.5 16.5 6.5 9Z"),
        line(seg(12, 16.5, 12, 20.5)),
        line(seg(8, 20.5, 16, 20.5)),
    ]


@icon("travertine-terraces", CAT, "Stepped white mineral terraces with shallow pools cascading down a slope.",
      tags=["hot springs", "pamukkale", "thermal pools", "natural wonder", "limestone", "cascade"])
def _(S):
    return [
        shell(poly([(2.5, 4.5), (8, 4.5), (8, 10), (14, 10), (14, 15.5), (21.5, 15.5), (21.5, 21), (2.5, 21)], closed=True, r=S.r)),
        detail(wave(3.5, 7, 7.5, 1, 0.8)),
        detail(wave(9.5, 13, 13, 1, 0.8)),
        detail(wave(15.5, 20.5, 18.3, 1, 0.8)),
    ]


@icon("ropes-course", CAT, "Two trees with platforms joined by a hanging rope net strung between them.",
      tags=["adventure park", "treetop", "challenge course", "zip line", "obstacle", "team building"])
def _(S):
    return [
        line(seg(4, 9, 4, 21.5)), line(seg(20, 9, 20, 21.5)),
        shell(circle(4, 5.2, 2.6)), shell(circle(20, 5.2, 2.6)),
        line(seg(4, 12, 7, 12)), line(seg(17, 12, 20, 12)),
        shell("M7 12Q12 20.5 17 12Z"),
        detail(seg(9.3, 12, 10.8, 16.5)), detail(seg(14.7, 12, 13.2, 16.5)),
    ]


@icon("island-hopping", CAT, "Two small palm islands joined by a dotted curved route with a tiny boat on it.",
      tags=["beach holiday", "tropical", "archipelago", "ferry", "travel route", "sea voyage"])
def _(S):
    return [
        shell("M2 21Q7.5 14 13 21Z"),
        line(seg(7.5, 16, 7.5, 11)),
        line("M7.5 11Q4.5 10 3.5 12"), line("M7.5 11Q10.5 10 11.5 12"),
        shell("M12.5 11.5Q16.8 7 21 11.5Z"),
        line(seg(16.8, 9.3, 16.8, 5.5)),
        line("M16.8 5.5Q14.5 4.6 13.5 6.2"), line("M16.8 5.5Q19 4.6 20 6.2"),
        dot(15.5, 19.3, 0.9), dot(18.3, 17.3, 0.9), dot(20.2, 14.8, 0.9),
    ]
