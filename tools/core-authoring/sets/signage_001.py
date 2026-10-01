"""TypeIcon Core: public signage (batch signage_001).

Wayfinding, accessibility and facility signs, plus round prohibition signs. Figures are a head disc over
2 px limbs. Prohibition signs share one ring and slash; the pictogram sits inside the ring.
"""
from __future__ import annotations

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401

CAT = "signage"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def pl(S, pts, k=1.0):
    return poly(pts, r=S.r * k)


def sq(S, x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle (knocked out of a Filled shell); corners are crisper in Line than in Rounded."""
    return Part("dot", rect(x, y, w, h, 0.0 if S.name == "line" else max(rx, 0.8)))


def blob(d) -> Part:
    """Solid mark that is knocked out of a Filled shell."""
    return Part("dot", d)


def tri(S, pts) -> Part:
    return Part("dot", poly(pts, closed=True, r=S.r * 0.7))


def wch(S, ox, oy, k=1.0, knock=False):
    """Wheelchair user symbol in a 10 x 15 box at (ox, oy), scaled by k. knock=True uses details (for use inside a shell)."""
    def p(x, y):
        return (ox + k * x, oy + k * y)
    cx, cy = p(4.2, 11.4)
    ln = detail if knock else line
    return [
        dot(*p(3, 1.8), 1.7),
        ln(pl(S, [p(3, 4.8), p(3, 9.6), p(8, 9.6), p(9.6, 13.6)])),
        ln(pl(S, [p(3, 6.6), p(6.4, 6.6)])),
        ln(arc(cx, cy, 3.6 * k, 20, 300)),
    ]


def ring(S):
    return shell(circle(12, 12, 9))


def slash(S):
    a = 5.6 if S.name == "line" else 8.0
    return detail(seg(a, a, 24 - a, 24 - a))


# ============================================================================ accessibility and facilities

@icon("left-luggage", CAT, "Suitcase on a counter shelf with a claim tag hanging from its handle.",
      tags=["baggage storage", "luggage room", "cloakroom", "bag drop", "station", "claim ticket", "locker"])
def _(S):
    return [
        shell(rect(3, 8, 11, 9.5, min(S.R, 2))),
        line(pl(S, [(6, 8), (6, 4.5), (11, 4.5), (11, 8)])),
        line(seg(11, 6, 15.5, 9.5)),
        shell(poly([(15, 11), (18, 9.5), (21, 14), (18, 15.5)], closed=True)),
        line(seg(2, 20.5, 22, 20.5)),
    ]


@icon("accessible-ramp", CAT, "Wheelchair user rolling up a sloped ramp.",
      tags=["wheelchair ramp", "step free", "slope", "access", "disabled access", "incline", "mobility"])
def _(S):
    return [
        shell(poly([(2, 20), (22, 20), (22, 10)], closed=True, r=S.r)),
        dot(8.2, 4.5, 1.7),
        line(pl(S, [(8.2, 7.5), (8.2, 11.5), (12.5, 11.5), (14, 14.5)])),
        line(pl(S, [(8.2, 9), (11, 9)])),
        line(arc(9.5, 13.4, 3.3, 20, 300)),
    ]


@icon("family-restroom", CAT, "Adult figure holding the hand of a small child figure.",
      tags=["family toilet", "parent and child", "baby room", "family bathroom", "restroom sign", "wc", "toilets"])
def _(S):
    return [
        dot(7, 4.5, 2),
        line(pl(S, [(7, 8), (7, 13.5)])),
        line(pl(S, [(4, 20), (7, 13.5), (10, 20)])),
        line(pl(S, [(7, 9.5), (11, 13), (14.5, 13)])),
        dot(17.5, 9.5, 1.6),
        line(pl(S, [(17.5, 12.5), (17.5, 16)])),
        line(pl(S, [(15.5, 20.5), (17.5, 16), (19.5, 20.5)])),
        line(pl(S, [(14.5, 13), (17.5, 13)])),
    ]


@icon("accessible-toilet", CAT, "Wheelchair symbol beside a side-view toilet.",
      tags=["disabled toilet", "accessible restroom", "wheelchair wc", "handicap bathroom", "toilets", "grab bar", "access"])
def _(S):
    return wch(S, 2, 4.5, 0.95) + [
        shell(rect(18.5, 3.5, 3, 7, min(S.R, 1))),
        shell(poly([(13.5, 11.5), (21.5, 11.5), (21.5, 14), (18, 17.5), (14.5, 17.5)], closed=True, r=S.r)),
        line(seg(17, 17.5, 17, 21)),
    ]


@icon("phone-charging-station", CAT, "Smartphone with a lightning bolt, plugged by a cable into a wall box.",
      tags=["charge point", "usb charging", "power point", "mobile charger", "charging kiosk", "airport", "recharge"])
def _(S):
    return [
        shell(rect(2.5, 4, 9.5, 16, min(S.R, 2.5))),
        solid(poly([(8, 7.5), (5, 13), (7, 13), (6, 17), (9.5, 11), (7.5, 11)], closed=True)),
        shell(rect(17, 9, 5, 7, min(S.R, 1.5))),
        line(pl(S, [(12, 18), (14.5, 18), (14.5, 12.5), (17, 12.5)])),
    ]


@icon("stroller-parking", CAT, "Baby stroller in side view with a bold letter P above it.",
      tags=["pram parking", "buggy park", "pushchair", "stroller bay", "baby", "parking", "storage"])
def _(S):
    return [
        line("M5 9V3h3a2.5 2.5 0 0 1 0 5H5"),
        shell("M9 15A6 6 0 0 1 21 15Z"),
        line(pl(S, [(9, 15), (9, 12), (6, 12)])),
        dot(10.5, 19.5, 1.75), dot(19, 19.5, 1.75),
    ]


@icon("quiet-zone", CAT, "Head in profile with a finger raised to the lips and a sound arc beside it.",
      tags=["silence", "hush", "be quiet", "library", "quiet carriage", "shh", "no noise"])
def _(S):
    return [
        shell(poly([(3.5, 20), (3.5, 9), (6.5, 4.5), (11.5, 4.5), (14, 8), (15, 11.5), (13, 12.5), (13, 15), (11, 15), (11, 20)],
                   closed=True, r=S.r)),
        dot(9.5, 9, 1.1),
        line(seg(16.5, 13, 16.5, 20)),
        line("M19.5 7.5a4.5 4.5 0 0 1 0 6"),
    ]


@icon("accessible-entrance", CAT, "Wheelchair symbol facing an open doorway with a level threshold.",
      tags=["step free entrance", "wheelchair entry", "level access", "accessible door", "disabled entrance", "doorway", "access"])
def _(S):
    return wch(S, 2.5, 5, 1.0) + [
        line(pl(S, [(14.5, 21), (14.5, 3.5), (21.5, 3.5), (21.5, 21)])),
        line(seg(2, 21, 22, 21)),
    ]


@icon("sensory-room", CAT, "Small room with a beanbag on the floor and soft wavy light rays hanging from the ceiling.",
      tags=["calm room", "snoezelen", "autism friendly", "relaxation room", "multisensory", "quiet space", "chill out"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, min(S.R, 3))),
        detail("M7.5 5c-1.8 1.8 1.8 3.4 0 5.5"),
        detail("M12.5 5c-1.8 1.8 1.8 3.4 0 5.5"),
        detail("M11.5 18.5v-1a3.7 3 0 0 1 7.4 0v1Z"),
    ]


@icon("adult-changing-room", CAT, "Adult changing bench with a ceiling track hoist and sling hanging above it.",
      tags=["changing places", "hoist", "adult changing table", "accessible toilet", "care", "disability", "bench"])
def _(S):
    return [
        line(seg(2, 3, 22, 3)),
        line(pl(S, [(7, 9), (12, 4), (17, 9)])),
        shell("M7 9Q12 14.5 17 9Z"),
        shell(rect(3, 15, 18, 3, min(S.R, 1.5))),
        line(seg(5.5, 18, 5.5, 21.5)), line(seg(18.5, 18, 18.5, 21.5)),
    ]


@icon("wheelchair-space", CAT, "Wheelchair symbol inside a floor marked space with dashed corner lines.",
      tags=["wheelchair bay", "reserved space", "train", "theatre", "floor marking", "accessible seating", "bay"])
def _(S):
    return wch(S, 7, 4.5, 1.0) + [
        line(pl(S, [(2, 8), (2, 3), (7, 3)])),
        line(pl(S, [(17, 3), (22, 3), (22, 8)])),
        line(pl(S, [(2, 16), (2, 21), (7, 21)])),
        line(pl(S, [(17, 21), (22, 21), (22, 16)])),
    ]


@icon("fast-track-lane", CAT, "Walking figure moving through a short lane marked by posts, with double chevrons ahead.",
      tags=["priority lane", "express queue", "fast pass", "security fast track", "skip the line", "vip lane", "airport"])
def _(S):
    return [
        dot(8, 5, 1.9),
        line(pl(S, [(8, 8.5), (7, 14)])),
        line(pl(S, [(7, 14), (4, 20.5)])),
        line(pl(S, [(7, 14), (10, 17), (9.5, 20.5)])),
        line(pl(S, [(8, 10), (11.5, 12.5)])),
        line(pl(S, [(14.5, 7), (17.5, 12), (14.5, 17)])),
        line(pl(S, [(18.5, 7), (21.5, 12), (18.5, 17)])),
    ]


@icon("directory-board", CAT, "Freestanding board listing floors as stacked bars with level dots on the left.",
      tags=["floor directory", "building directory", "wayfinding", "tenant list", "lobby", "floor guide", "signpost"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 14.5, min(S.R, 2.5))),
        detail(seg(11, 6.5, 16.5, 6.5)), detail(seg(11, 10, 16.5, 10)), detail(seg(11, 13.5, 16.5, 13.5)),
        dot(7.5, 6.5, 1), dot(7.5, 10, 1), dot(7.5, 13.5, 1),
        line(seg(12, 17, 12, 21.5)), line(seg(8, 21, 16, 21)),
    ]


@icon("occupancy-indicator", CAT, "Door lock plate with a small window split in two halves, one half shaded to show engaged.",
      tags=["vacant engaged", "toilet lock", "restroom occupied", "in use", "bathroom lock", "cubicle", "engaged sign"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, min(S.R, 3))),
        detail(rect(8, 6.5, 8, 5)),
        sq(S, 12, 6.5, 4, 5),
        dot(12, 16.5, 1.5),
    ]


@icon("staff-only-sign", CAT, "Closed door with a small figure wearing a lanyard badge on the door panel.",
      tags=["employees only", "authorised personnel", "private door", "no entry", "back of house", "staff entrance", "restricted"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, min(S.R, 3))),
        dot(12, 7, 1.8),
        detail(pl(S, [(10, 11), (12, 14.5), (14, 11)])),
        sq(S, 10.5, 15, 3, 3.5),
    ]


@icon("reserved-table-card", CAT, "Folded tent card standing on a table top with a bold letter R on its front.",
      tags=["reserved sign", "table reservation", "booked", "restaurant", "place card", "tent card", "reservation"])
def _(S):
    return [
        shell(poly([(4, 17.5), (6, 3.5), (18, 3.5), (20, 17.5)], closed=True, r=S.r)),
        detail("M10 15V7h3.5a2.25 2.25 0 0 1 0 4.5H10M13 11.5l2 3.5"),
        line(seg(2, 21, 22, 21)),
    ]


@icon("book-exchange-box", CAT, "Small house-shaped box on a post with a row of book spines inside.",
      tags=["little free library", "book swap", "take a book", "street library", "book share", "community library", "bookcase"])
def _(S):
    return [
        shell(poly([(4, 9.5), (12, 3), (20, 9.5), (20, 18), (4, 18)], closed=True, r=S.r)),
        detail(seg(8.5, 11, 8.5, 15.5)), detail(seg(12, 11, 12, 15.5)), detail(seg(15.5, 11, 15.5, 15.5)),
        line(seg(12, 18, 12, 21.5)), line(seg(8, 21.5, 16, 21.5)),
    ]


@icon("tax-refund", CAT, "Shopping bag with a coin above it and a curved arrow returning toward the bag.",
      tags=["vat refund", "tax free shopping", "duty free refund", "gst refund", "tourist refund", "receipt", "cash back"])
def _(S):
    return [
        shell(rect(2.5, 9, 11, 12, min(S.R, 2))),
        line("M5.5 9V7a2.5 2.5 0 0 1 5 0v2"),
        shell(circle(18, 5.5, 3.25)),
        line("M19.5 11.5C21 15 19 18 16 19.5"),
        line(pl(S, [(16, 16.5), (16, 19.5), (19, 19.5)])),
    ]


@icon("women-only-car", CAT, "Train carriage side view with a female figure symbol in its window.",
      tags=["ladies carriage", "female only coach", "women's coach", "train", "metro", "safe travel", "rail"])
def _(S):
    return [
        shell(rect(2, 3.5, 20, 14, min(S.R, 3))),
        dot(12, 6.8, 1.5),
        detail(pl(S, [(12, 9.5), (8.5, 14.5), (15.5, 14.5)], 0) if False else poly([(12, 9.5), (8.5, 14.5), (15.5, 14.5)], closed=True)),
        dot(6.5, 20.5, 1.5), dot(17.5, 20.5, 1.5),
    ]


@icon("visitor-center", CAT, "Small building with a pitched roof and a lowercase letter i on its front wall.",
      tags=["tourist information", "info point", "welcome centre", "visitor information", "tourism office", "park centre", "help desk"])
def _(S):
    return [
        shell(poly([(3, 9.5), (12, 3), (21, 9.5), (21, 20), (3, 20)], closed=True, r=S.r)),
        dot(12, 10.5, 1.4),
        detail(seg(12, 13.5, 12, 17)),
    ]


@icon("shoe-shine", CAT, "Shoe in side view on a footrest block with sparkle marks above the toe.",
      tags=["boot polish", "shoeshine stand", "polish shoes", "cobbler", "leather care", "footwear", "shiny"])
def _(S):
    return [
        shell(poly([(2.5, 15), (2.5, 7), (7, 7), (9, 10.5), (14, 11.5), (19.5, 15)], closed=True, r=S.r)),
        shell(rect(5, 17, 14, 4, min(S.R, 1.5))),
        line("M20 3v4M18 5h4"),
    ]


@icon("connecting-rooms", CAT, "Two hotel doors side by side with a double-headed arrow linking them.",
      tags=["adjoining rooms", "interconnecting door", "family suite", "hotel", "adjacent rooms", "link door", "accommodation"])
def _(S):
    return [
        shell(rect(2.5, 3, 8, 18, min(S.R, 2))),
        shell(rect(13.5, 3, 8, 18, min(S.R, 2))),
        detail(seg(6.5, 12, 17.5, 12)),
        detail(pl(S, [(9, 9.5), (6.5, 12), (9, 14.5)])),
        detail(pl(S, [(15, 9.5), (17.5, 12), (15, 14.5)])),
    ]


@icon("ski-storage", CAT, "Pair of skis and poles standing upright in a slotted wall rack.",
      tags=["ski locker", "ski room", "ski rack", "winter sports", "boot room", "snow", "equipment storage"])
def _(S):
    return [
        line("M5.5 15V6C5.5 4 4.5 3.5 3 3.5"),
        line("M10 15V6C10 4 9 3.5 7.5 3.5"),
        line(seg(15, 15, 15, 4)), line(seg(19.5, 15, 19.5, 4)),
        shell(rect(2, 15, 20, 5, min(S.R, 2))),
    ]


@icon("beach-access", CAT, "Walking figure at the top of a short flight of steps leading to the sea and a beach umbrella.",
      tags=["path to beach", "seaside", "shore", "steps to beach", "coast access", "sand", "sea"])
def _(S):
    return [
        dot(5, 3.8, 1.6),
        line(pl(S, [(5, 6.5), (5, 10)])),
        line(pl(S, [(2, 12), (6, 12), (6, 15), (10, 15), (10, 18), (13, 18)])),
        shell("M14 12.5a4.25 4.25 0 0 1 8.5 0Z"),
        line(seg(18.25, 12.5, 18.25, 17)),
        line("M2 21c1.5-1.5 3-1.5 4.5 0s3 1.5 4.5 0 3-1.5 4.5 0 3 1.5 4.5 0"),
    ]


@icon("soundproof-room", CAT, "Room with sound arcs from a speaker inside that stop at a thick padded wall.",
      tags=["acoustic room", "recording booth", "sound insulation", "noise isolation", "quiet booth", "studio", "silent room"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, min(S.R, 3))),
        dot(6.5, 12, 1.5),
        detail(arc(6.5, 12, 4, -55, 55)),
        detail(arc(6.5, 12, 7, -45, 45)),
        sq(S, 17, 6, 2.5, 12),
    ]


@icon("ski-in-ski-out", CAT, "Skier gliding straight up to the front door of a chalet.",
      tags=["ski chalet", "slope side", "ski access", "winter resort", "ski lodge", "piste", "mountain accommodation"])
def _(S):
    return [
        dot(5.5, 4.5, 1.7),
        line(pl(S, [(5.5, 7.5), (7, 12.5), (4.5, 16)])),
        line(pl(S, [(7, 12.5), (10, 16)])),
        line(pl(S, [(6, 9.5), (9.5, 11)])),
        line(seg(2, 19.5, 12, 19.5)),
        shell(poly([(14, 10.5), (18, 6), (22, 10.5), (22, 20), (14, 20)], closed=True, r=S.r)),
        detail(seg(18, 14, 18, 20)),
    ]


@icon("infinity-pool", CAT, "Pool seen from the side with water spilling over a vanishing edge toward a horizon line.",
      tags=["edge pool", "vanishing edge", "rooftop pool", "resort", "swimming pool", "hotel pool", "horizon"])
def _(S):
    return [
        line(seg(2, 3.5, 22, 3.5)),
        line(pl(S, [(2, 8), (2, 19), (15, 19), (15, 10)])),
        line("M4.5 12.5c1.5-1 3-1 4.5 0s3 1 4.5 0"),
        line("M18 11v4"), line("M21 11v7"),
    ]


@icon("lazy-river", CAT, "Swimmer floating in an inflatable ring along a wavy water channel.",
      tags=["water park", "tube ride", "float ring", "inner tube", "river ride", "resort pool", "drifting"])
def _(S):
    return [
        dot(12, 5.5, 1.9),
        shell(ellipse(12, 11.5, 8, 4)),
        line(seg(12, 8, 12, 9.5)),
        line("M2 19.5c2-1.5 4-1.5 6 0s4 1.5 6 0 4-1.5 6 0 2 1 2 1"),
    ]


@icon("outdoor-seating", CAT, "Cafe table with two chairs under a tall parasol.",
      tags=["terrace", "patio", "al fresco", "cafe table", "garden seating", "beer garden", "sunshade"])
def _(S):
    return [
        shell("M3 9.5A9 7.5 0 0 1 21 9.5Z"),
        line(seg(12, 9.5, 12, 21.5)),
        line(seg(8.5, 14.5, 15.5, 14.5)),
        line(pl(S, [(2.5, 12), (2.5, 21.5)])), line(seg(2.5, 17.5, 6, 17.5)),
        line(pl(S, [(21.5, 12), (21.5, 21.5)])), line(seg(21.5, 17.5, 18, 17.5)),
    ]


@icon("umbrella-bag-dispenser", CAT, "Wall dispenser beside a long plastic sleeve with a closed umbrella inside.",
      tags=["wet umbrella", "rain", "umbrella cover", "plastic sleeve", "shop entrance", "lobby", "drip free"])
def _(S):
    return [
        shell(rect(2.5, 3, 8, 12, min(S.R, 2))),
        detail(seg(5, 12, 8, 12)),
        shell(rect(13.5, 3, 8, 17, min(S.R, 3))),
        detail("M19 17V8a1.5 1.5 0 0 0-3 0"),
        line(seg(6.5, 15, 6.5, 21)),
    ]


@icon("book-return-slot", CAT, "Wall box with a slot and a book standing halfway out of it.",
      tags=["library", "drop box", "return books", "book drop", "after hours return", "borrowed books", "slot"])
def _(S):
    return [
        line(pl(S, [(9, 14), (9, 3), (15, 3), (15, 14)])),
        shell(rect(2, 13, 20, 8, min(S.R, 2))),
        detail(seg(5.5, 17, 18.5, 17)),
    ]


@icon("cart-corral", CAT, "Shopping cart parked inside a U-shaped railing bay.",
      tags=["trolley bay", "cart return", "trolley park", "supermarket", "car park", "shopping trolley", "cart storage"])
def _(S):
    return [
        line(pl(S, [(2, 3), (2, 21), (22, 21), (22, 3)])),
        shell(poly([(5.5, 8), (18.5, 8), (16.5, 14), (7.5, 14)], closed=True, r=S.r)),
        line(pl(S, [(3.5, 5), (5.5, 5), (7.5, 14)])) if False else line(pl(S, [(5.5, 8), (5.5, 5)])),
        dot(8.5, 17.5, 1.3), dot(15.5, 17.5, 1.3),
    ]


@icon("shopping-basket-stack", CAT, "Three hand baskets stacked inside each other.",
      tags=["baskets", "hand baskets", "supermarket", "store entrance", "take a basket", "shop", "stacked"])
def _(S):
    return [
        line(pl(S, [(3, 3), (5.5, 7.5), (18.5, 7.5), (21, 3)])),
        line(pl(S, [(3, 8.5), (5.5, 13), (18.5, 13), (21, 8.5)])),
        line(pl(S, [(3, 14), (5.5, 18.5), (18.5, 18.5), (21, 14)])),
    ]


@icon("deliveries-entrance-sign", CAT, "Door with a stack of parcels on a hand truck in front of it.",
      tags=["goods in", "loading door", "delivery door", "trade entrance", "service entrance", "hand truck", "parcels"])
def _(S):
    return [
        shell(rect(14.5, 3, 7, 18, min(S.R, 2))),
        shell(rect(6, 5.5, 5.5, 5.5, min(S.R, 1))),
        shell(rect(6, 11.5, 5.5, 5.5, min(S.R, 1))),
        line(pl(S, [(3.5, 2.5), (3.5, 19.5), (8, 19.5)])),
        dot(8, 20.5, 1.3),
    ]


@icon("pet-drinking-fountain", CAT, "Low water bowl at ground level with a paw print above it, beside a taller fountain post.",
      tags=["dog water", "pet water bowl", "dog bowl", "water station", "park", "paw", "drinking water"])
def _(S):
    return [
        dot(5, 8.5, 1.2), dot(8.5, 6, 1.2), dot(12, 8.5, 1.2), dot(8.5, 10.5, 1.8),
        shell(poly([(2.5, 14), (14.5, 14), (13, 19.5), (4, 19.5)], closed=True, r=S.r)),
        shell(rect(17, 8, 4.5, 13, min(S.R, 1.5))),
        line(pl(S, [(17, 8), (17, 5), (14.5, 5)])),
    ]


@icon("misting-station", CAT, "Tall post with a nozzle at the top spraying fine mist dots over a standing figure.",
      tags=["cooling mist", "mist fan", "heat relief", "cool down", "spray", "theme park", "summer"])
def _(S):
    return [
        line(pl(S, [(3.5, 21.5), (3.5, 3.5), (8, 3.5)])),
        dot(11, 4.5, 1.1), dot(11, 8, 1.1), dot(14.5, 3.5, 1.1), dot(14.5, 7, 1.1), dot(18, 5, 1.1), dot(18.5, 9, 1.1),
        dot(14.5, 12.5, 1.8),
        line(pl(S, [(14.5, 15.5), (14.5, 19)])),
        line(pl(S, [(12, 21.5), (14.5, 19), (17, 21.5)])),
    ]


@icon("place-name-sign", CAT, "Wide town entry sign on two posts with a small house and text lines on the panel.",
      tags=["welcome sign", "town sign", "village sign", "entry sign", "city limits", "settlement", "gateway sign"])
def _(S):
    return [
        shell(rect(2, 4, 20, 12, min(S.R, 2.5))),
        detail(pl(S, [(5.5, 12.5), (5.5, 9.5), (8, 7.5), (10.5, 9.5), (10.5, 12.5)])),
        detail(seg(13.5, 8, 19, 8)), detail(seg(13.5, 12, 17.5, 12)),
        line(seg(6, 16, 6, 21.5)), line(seg(18, 16, 18, 21.5)),
    ]


@icon("bicycle-counter", CAT, "Tall upright display with a bicycle symbol at the top and a row of digit boxes below.",
      tags=["cycle counter", "bike count", "cycling totem", "bike path counter", "traffic counter", "eco counter", "trail"])
def _(S):
    return [
        shell(rect(5, 2, 14, 20, min(S.R, 2.5))),
        detail(circle(8.8, 9, 2.2)), detail(circle(15.2, 9, 2.2)),
        detail(pl(S, [(8.8, 9), (11.5, 5.5), (15.2, 9)])),
        sq(S, 7, 15, 2.8, 4), sq(S, 10.6, 15, 2.8, 4), sq(S, 14.2, 15, 2.8, 4),
    ]


@icon("honesty-box", CAT, "Small box with a coin slot and padlock beside a crate of vegetables.",
      tags=["pay here", "farm stand", "self service", "roadside stall", "payment box", "donation box", "trust box"])
def _(S):
    return [
        shell(rect(2, 10, 10, 11, min(S.R, 2))),
        detail(seg(5, 13.5, 9, 13.5)),
        dot(7, 17.5, 1.3),
        shell(rect(14, 14, 8, 7, min(S.R, 1.5))),
        detail(seg(14.5, 17.5, 21.5, 17.5)),
        dot(16.5, 10.8, 1.8), dot(20, 10.2, 1.8),
    ]


@icon("roll-in-shower", CAT, "Wheelchair symbol under a shower head on a flat floor with no step.",
      tags=["accessible shower", "wet room", "step free shower", "wheelchair shower", "disabled bathroom", "level access", "spray"])
def _(S):
    return wch(S, 2.5, 7, 0.95) + [
        line(pl(S, [(21.5, 21.5), (21.5, 3), (14, 3)])),
        shell("M10.5 7a3.5 3 0 0 1 7 0Z"),
        dot(12, 10, 0.9), dot(14, 11.5, 0.9), dot(16, 10, 0.9),
    ]


@icon("accessible-hotel-room", CAT, "Bed seen from the side with a wheelchair symbol beside it.",
      tags=["accessible bedroom", "adapted room", "disabled room", "hotel", "wheelchair friendly room", "guest room", "access"])
def _(S):
    return wch(S, 2, 6.5, 0.95) + [
        line(seg(21.5, 8, 21.5, 21)),
        shell(rect(12, 14, 9.5, 4, min(S.R, 1.5))),
        line(seg(12.5, 18, 12.5, 21)),
    ]


@icon("toilet-child-seat", CAT, "Small child seat with leg holes fixed in a toilet stall, with a toddler sitting in it.",
      tags=["baby seat", "toddler seat", "stall child seat", "family restroom", "potty", "baby holder", "toilet"])
def _(S):
    return [
        dot(11, 4.5, 1.9),
        line(seg(11, 7.5, 11, 10)),
        shell(rect(4, 10, 14, 7, min(S.R, 2))),
        line(seg(8, 17, 8, 21.5)), line(seg(14, 17, 14, 21.5)),
        line(seg(21.5, 2.5, 21.5, 21.5)),
    ]


@icon("sanitary-bin", CAT, "Slim pedal bin with a lid, a small droplet symbol on its front and a foot pedal.",
      tags=["period bin", "feminine hygiene", "pad disposal", "restroom bin", "waste bin", "pedal bin", "toilets"])
def _(S):
    return [
        line(seg(5, 5, 19, 5)),
        shell(poly([(7, 7.5), (17, 7.5), (16, 19.5), (8, 19.5)], closed=True, r=S.r)),
        detail("M12 10.5c-1.5 2-2 3-2 4a2 2 0 0 0 4 0c0-1-.5-2-2-4Z"),
        line(seg(8, 21.5, 16, 21.5)),
    ]


@icon("seat-cover-dispenser", CAT, "Wall dispenser with a paper toilet seat cover half pulled out of its slot.",
      tags=["toilet seat covers", "hygiene", "paper seat cover", "restroom", "dispenser", "public toilet", "sanitary"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 11, min(S.R, 2.5))),
        detail(seg(7.5, 10.5, 16.5, 10.5)),
        shell("M8.5 11.5h7v4.5a3.5 4.5 0 0 1-7 0Z"),
    ]


@icon("wheelchair-charging-point", CAT, "Wheelchair symbol beside a power socket marked with a lightning bolt.",
      tags=["power chair charging", "electric wheelchair", "charge point", "scooter charging", "mobility scooter", "socket", "battery"])
def _(S):
    return wch(S, 2, 4.5, 1.0) + [
        solid(poly([(19, 3), (14.5, 10), (17.5, 10), (16.5, 17), (21.5, 8.5), (18.5, 8.5)], closed=True)),
        line(pl(S, [(10, 18), (14, 18), (14, 21)])) if False else line(seg(12.5, 20, 21.5, 20)),
    ]


@icon("beach-access-mat", CAT, "Wheelchair symbol rolling along a flat ribbed mat laid across the sand.",
      tags=["beach mat", "accessible beach", "sand mat", "wheelchair path", "roll out mat", "seaside access", "boardwalk"])
def _(S):
    return wch(S, 7, 2.5, 1.0) + [
        line(seg(2, 19.5, 22, 19.5)),
        line(seg(5, 19.5, 5, 22)), line(seg(9.5, 19.5, 9.5, 22)), line(seg(14.5, 19.5, 14.5, 22)), line(seg(19, 19.5, 19, 22)),
    ]


@icon("pool-hoist", CAT, "Poolside lift with an upright post, a swinging arm and a seat lowering toward the water.",
      tags=["swimming pool lift", "accessible pool", "water access", "disabled swimming", "chair lift", "pool access", "hydrotherapy"])
def _(S):
    return [
        line(pl(S, [(4, 21), (4, 3.5), (14.5, 3.5), (14.5, 9)])),
        line(pl(S, [(11, 10), (11, 14), (18, 14)])),
        line(seg(11, 9, 18, 9)),
        line("M2 19c1.5-1.5 3-1.5 4.5 0s3 1.5 4.5 0 3-1.5 4.5 0 3 1.5 4.5 0 2-1 2-1"),
    ]


@icon("wheelchair-swing", CAT, "Swing frame with a flat platform hanging by chains and a wheelchair symbol on it.",
      tags=["accessible playground", "inclusive play", "swing", "disabled playground", "platform swing", "park", "playground"])
def _(S):
    return wch(S, 8.2, 4.5, 0.75) + [
        line(seg(2, 3, 22, 3)),
        line(seg(5.5, 3, 5.5, 18.5)), line(seg(18.5, 3, 18.5, 18.5)),
        line(seg(4, 18.5, 20, 18.5)),
        line(seg(2, 3, 2, 21.5)), line(seg(22, 3, 22, 21.5)),
    ]


@icon("lowered-counter", CAT, "Service counter with one section stepped down to wheelchair height and a wheelchair symbol above it.",
      tags=["accessible counter", "low desk", "reception", "wheelchair height", "service desk", "ticket window", "access"])
def _(S):
    return wch(S, 14, 3.5, 0.7) + [
        shell(poly([(2, 12), (11, 12), (11, 16.5), (22, 16.5), (22, 21), (2, 21)], closed=True, r=S.r)),
    ]


@icon("accessible-door-button", CAT, "Square wall push plate with a wheelchair symbol and a door outline beside it.",
      tags=["automatic door", "push to open", "door opener", "access button", "disabled entrance", "wall switch", "door activator"])
def _(S):
    return wch(S, 4, 5.5, 0.85, knock=True) + [
        shell(rect(2, 2.5, 20, 19, min(S.R, 3))),
        detail(pl(S, [(15, 19), (15, 6.5), (19, 6.5), (19, 19)])),
    ]


# ============================================================================ prohibition signs

def no(S, *parts):
    return [ring(S), *parts, slash(S)]


@icon("no-vaping-sign", CAT, "Round prohibition sign with a vape pen and a puff of vapor, crossed by a slash.",
      tags=["no e-cigarettes", "vape ban", "no smoking", "e-cig", "vapor", "tobacco free", "prohibited"])
def _(S):
    return no(S, sq(S, 5.5, 13, 8.5, 3, 1.4), dot(16.5, 10.5, 1.2), dot(18, 14, 1), dot(15, 8, 1))


@icon("no-firearms-sign", CAT, "Round prohibition sign with a handgun silhouette, crossed by a slash.",
      tags=["no guns", "weapons banned", "gun free zone", "no weapons", "pistol", "security", "prohibited"])
def _(S):
    return no(S, sq(S, 6.5, 8.5, 10.5, 3.2, 0.6), tri(S, [(8, 11), (11.5, 11), (10.5, 17), (7.5, 17)]), sq(S, 12, 11.5, 1.2, 2))


@icon("no-feeding-animals-sign", CAT, "Round prohibition sign with a duck beside a piece of bread, crossed by a slash.",
      tags=["do not feed", "wildlife", "ducks", "no feeding birds", "park rules", "zoo", "prohibited"])
def _(S):
    return no(S, dot(15.5, 8.5, 1.5), tri(S, [(17, 8), (19, 8.8), (17, 9.5)]), blob(ellipse(12, 13.8, 4.2, 2.6)),
              sq(S, 6, 8, 3.5, 3, 0.8))


@icon("no-walking-on-grass-sign", CAT, "Round prohibition sign with a footprint pressing on blades of grass, crossed by a slash.",
      tags=["keep off the grass", "lawn", "stay on path", "turf", "park rules", "garden", "prohibited"])
def _(S):
    return no(S, blob(ellipse(12, 9, 2.2, 3.2)), dot(12, 13.8, 1.3),
              detail(seg(7.5, 18, 7.5, 15.5)), detail(seg(12, 18, 12, 16)), detail(seg(16.5, 18, 16.5, 15.5)))


@icon("no-picking-flowers-sign", CAT, "Round prohibition sign with a flower on a stem and leaf, crossed by a slash.",
      tags=["do not pick", "protected plants", "flowers", "garden rules", "nature reserve", "wildflowers", "prohibited"])
def _(S):
    return no(S, dot(12, 7, 1.4), dot(14.6, 9, 1.4), dot(9.4, 9, 1.4), dot(12, 11, 1.4), dot(12, 9, 1.0),
              detail(seg(12, 12, 12, 18)), detail(seg(12, 16, 15.5, 13.5)))


@icon("no-selfie-sticks-sign", CAT, "Round prohibition sign with a phone on a long extendable pole, crossed by a slash.",
      tags=["selfie stick ban", "monopod", "museum rules", "phone pole", "camera pole", "concert rules", "prohibited"])
def _(S):
    return no(S, detail(seg(6.5, 18, 14, 10.5)), sq(S, 13.5, 5.5, 4, 6, 0.8))


@icon("no-tripods-sign", CAT, "Round prohibition sign with a camera on a three-legged tripod, crossed by a slash.",
      tags=["tripod ban", "camera stand", "photography rules", "museum rules", "no camera supports", "stand", "prohibited"])
def _(S):
    return no(S, sq(S, 8, 6.5, 8, 4.5, 1), dot(12, 8.7, 1.1), detail(seg(12, 11, 8, 18)), detail(seg(12, 11, 12, 18)), detail(seg(12, 11, 16, 18)))


@icon("adults-only-sign", CAT, "Round prohibition sign with the number 18 in bold digits, crossed by a slash.",
      tags=["18 plus", "age restriction", "over 18", "no minors", "age limit", "mature", "prohibited"])
def _(S):
    return no(S, detail(seg(7.5, 7.5, 7.5, 16.5)), detail(circle(13.8, 9.3, 2.2)), detail(circle(13.8, 14.7, 2.2)))


@icon("no-flushing-paper-sign", CAT, "Round prohibition sign with a sheet of paper dropping into a toilet bowl, crossed by a slash.",
      tags=["do not flush", "wipes", "blocked drain", "bin only", "toilet rules", "sanitary", "prohibited"])
def _(S):
    return no(S, sq(S, 10, 5.5, 4.5, 3.5, 0.5), tri(S, [(6.5, 11), (17.5, 11), (15.5, 14.5), (12.5, 17), (11.5, 17), (8.5, 14.5)]))


@icon("no-hitchhiking-sign", CAT, "Round prohibition sign with a standing figure holding out an arm with the thumb raised, crossed by a slash.",
      tags=["no lifts", "thumbing a ride", "motorway rules", "pedestrians", "road safety", "highway", "prohibited"])
def _(S):
    return no(S, dot(9.5, 6.5, 1.5), detail(seg(9.5, 9, 9.5, 14)), detail(pl(S, [(7, 18), (9.5, 14), (12, 18)])),
              detail(pl(S, [(9.5, 10.5), (15.5, 9.5), (15.5, 7)])))


@icon("no-snowmobiles-sign", CAT, "Round prohibition sign with a snowmobile in side view, crossed by a slash.",
      tags=["no sleds", "snow scooter", "winter trail", "nature reserve", "motor vehicles", "snow machine", "prohibited"])
def _(S):
    return no(S, sq(S, 10, 14.5, 7, 2.6, 1.2), tri(S, [(7.5, 14), (8.5, 10), (13.5, 9.5), (16, 14)]),
              detail(seg(5.5, 17, 9.5, 17)), detail(seg(10, 10, 10, 7.5)))


@icon("no-off-road-vehicles-sign", CAT, "Round prohibition sign with a four-wheeled quad bike on chunky tires, crossed by a slash.",
      tags=["no quad bikes", "atv ban", "no motorbikes trail", "protected land", "motor vehicles", "all terrain", "prohibited"])
def _(S):
    return no(S, sq(S, 8, 10, 8, 3.2, 1), detail(seg(8.5, 8, 11, 8)), dot(7, 15, 2.2), dot(17, 15, 2.2))


@icon("no-throwing-objects-sign", CAT, "Round prohibition sign with a figure mid-throw and a small object leaving the hand, crossed by a slash.",
      tags=["no throwing", "no projectiles", "stadium rules", "no stones", "playground rules", "ball games", "prohibited"])
def _(S):
    return no(S, dot(8.5, 7, 1.5), detail(seg(8.5, 9.5, 9.5, 14)), detail(pl(S, [(6.5, 18), (9.5, 14), (12, 18)])),
              detail(pl(S, [(9, 10.5), (13, 8.5)])), dot(16.5, 7, 1.4))


@icon("no-sledding-sign", CAT, "Round prohibition sign with a figure seated on a sled, crossed by a slash.",
      tags=["no sleds", "toboggan", "snow", "hill rules", "winter sports ban", "sledge", "prohibited"])
def _(S):
    return no(S, dot(11, 8, 1.5), detail(pl(S, [(11, 10.5), (12, 14)])), detail(pl(S, [(12, 14), (15.5, 12.5)])),
              detail("M6.5 17h10a1.5 1.5 0 0 0 0-3"))


@icon("no-knives-sign", CAT, "Round prohibition sign with a fixed-blade knife pointing up, crossed by a slash.",
      tags=["blades banned", "weapons", "sharp objects", "security", "knife ban", "dagger", "prohibited"])
def _(S):
    return no(S, tri(S, [(12, 5.5), (14.2, 11), (9.8, 11)]), sq(S, 10.7, 11.5, 2.6, 6, 1))


@icon("no-lighters-sign", CAT, "Round prohibition sign with a pocket lighter and a small flame, crossed by a slash.",
      tags=["no matches", "no flames", "fire hazard", "ignition", "no smoking", "naked flame", "prohibited"])
def _(S):
    return no(S, tri(S, [(12, 4.5), (14.3, 8), (12, 10), (9.7, 8)]), sq(S, 9, 11, 6, 6.5, 1.2))


@icon("no-laser-pointers-sign", CAT, "Round prohibition sign with a pen-shaped laser pointer and a beam ending in a dot, crossed by a slash.",
      tags=["laser ban", "laser pen", "pointer", "aircraft safety", "stadium rules", "beam", "prohibited"])
def _(S):
    return no(S, sq(S, 5.5, 14, 6.5, 2.4, 1.2), detail(seg(12.5, 14, 16.5, 10)), dot(17, 9.5, 1.3))


@icon("no-chewing-gum-sign", CAT, "Round prohibition sign with a stick of gum half out of its wrapper, crossed by a slash.",
      tags=["gum ban", "no gum", "litter", "mints", "transit rules", "clean streets", "prohibited"])
def _(S):
    return no(S, sq(S, 11, 11, 6.5, 2.8, 0.6), detail(pl(S, [(12, 9.5), (7, 9.5), (7, 15), (12, 15)])))


@icon("no-durian-sign", CAT, "Round prohibition sign with a spiky round durian fruit, crossed by a slash.",
      tags=["fruit ban", "smelly fruit", "hotel rules", "transit rules", "tropical fruit", "no food smell", "prohibited"])
def _(S):
    pts = [(12 + 4.6 * __import__("math").cos(a * 0.7854), 12 + 4.6 * __import__("math").sin(a * 0.7854)) for a in range(8)]
    return no(S, dot(12, 12, 3.4), *[dot(x, y, 1) for x, y in pts])


@icon("no-lying-down-sign", CAT, "Round prohibition sign with a figure lying flat along a bench, crossed by a slash.",
      tags=["no sleeping", "bench rules", "no loitering", "public seating", "no napping", "park bench", "prohibited"])
def _(S):
    return no(S, dot(7.5, 11.5, 1.5), detail(seg(10, 12.5, 17.5, 12.5)),
              detail(seg(6, 16, 18, 16)), detail(seg(7, 16, 7, 18)), detail(seg(17, 16, 17, 18)))


@icon("no-metal-detecting-sign", CAT, "Round prohibition sign with a figure sweeping a metal detector disc over the ground, crossed by a slash.",
      tags=["detectorists", "treasure hunting", "archaeology site", "heritage protection", "beach rules", "digging", "prohibited"])
def _(S):
    return no(S, dot(8, 6.5, 1.5), detail(seg(8, 9, 8, 14)), detail(pl(S, [(6, 18), (8, 14), (10.5, 18)])),
              detail(seg(9, 10.5, 15, 16)), blob(ellipse(16.5, 17, 2.2, 1.1)))


@icon("no-bill-posting-sign", CAT, "Round prohibition sign with a poster and a paste brush on a wall, crossed by a slash.",
      tags=["no posters", "no flyers", "fly posting", "stick no bills", "graffiti", "wall rules", "prohibited"])
def _(S):
    return no(S, detail(rect(6.5, 7, 6, 9)), detail(seg(13, 12, 15.5, 12)), sq(S, 15, 9.5, 3, 5, 0.5))


@icon("no-feet-on-seats-sign", CAT, "Round prohibition sign with a shoe resting on a seat cushion, crossed by a slash.",
      tags=["feet off seats", "train rules", "bus rules", "cinema rules", "etiquette", "dirty shoes", "prohibited"])
def _(S):
    return no(S, tri(S, [(6.5, 12.5), (6.5, 8), (9.5, 8), (10.5, 10.5), (14, 11), (16, 13)]), detail(seg(5.5, 16, 18.5, 16)))


@icon("no-hoverboards-sign", CAT, "Round prohibition sign with a rider standing on a two-wheeled self-balancing board, crossed by a slash.",
      tags=["self balancing scooter", "balance board", "no boards", "mall rules", "airport rules", "e-scooter", "prohibited"])
def _(S):
    return no(S, dot(12, 6.5, 1.5), detail(seg(12, 9, 12, 13.5)), sq(S, 8, 14.5, 8, 2, 1), dot(6.5, 15.5, 2), dot(17.5, 15.5, 2))


@icon("no-love-locks-sign", CAT, "Round prohibition sign with a padlock clipped to a railing, crossed by a slash.",
      tags=["love padlocks", "bridge rules", "railing", "heritage protection", "no padlocks", "romantic tradition", "prohibited"])
def _(S):
    return no(S, detail(seg(5.5, 8, 18.5, 8)), detail("M9.8 13V8.5a2.2 2.2 0 0 1 4.4 0V13"), sq(S, 8.5, 12.5, 7, 5.5, 1))
