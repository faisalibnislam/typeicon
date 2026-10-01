"""TypeIcon Core: outdoors (travel, hotels, beach, water sports, camping and survival gear), batch 001."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt

CAT = "outdoors"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def bar(p0, p1, w, closed=True, r=0.0):
    """Rectangle polygon of width w along the segment p0-p1."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    n = math.hypot(dx, dy)
    nx, ny = -dy / n * w / 2, dx / n * w / 2
    pts = [(p0[0] + nx, p0[1] + ny), (p1[0] + nx, p1[1] + ny), (p1[0] - nx, p1[1] - ny), (p0[0] - nx, p0[1] - ny)]
    return poly(pts, closed=True, r=r)


def rotpts(pts, deg, cx=0.0, cy=0.0, ox=0.0, oy=0.0, s=1.0):
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [(ox + s * ((x - cx) * c - (y - cy) * sn), oy + s * ((x - cx) * sn + (y - cy) * c)) for x, y in pts]


PLANE = [(0, -7), (1.2, -3), (6.5, 1), (6.5, 2.6), (1.3, 1), (1, 4.6), (3, 6), (3, 7), (0, 6.3), (-3, 7), (-3, 6),
         (-1, 4.6), (-1.3, 1), (-6.5, 2.6), (-6.5, 1), (-1.2, -3)]


def plane(S, ox, oy, s=1.0, deg=45.0):
    return shell(poly(rotpts(PLANE, deg, ox=ox, oy=oy, s=s), closed=True, r=S.r * 0.4), stroke_miterlimit="2")


# ============================================================================ travel gear

@icon("bellhop-cart", CAT, "Hotel luggage cart with an arch rail and a suitcase on its base",
      tags=["luggage cart", "bellhop", "bellboy", "hotel", "porter", "baggage", "trolley"])
def _(S):
    return [
        line("M4 15.5V10A8 8 0 0 1 20 10V15.5"),
        shell(rect(3, 15.5, 18, 2.5, rr(S, 1))),
        shell(rect(8.5, 8.5, 7, 5.5, L(S, 0.5, 2))),
        dot(6.5, 21, 1.25), dot(17.5, 21, 1.25),
    ]


@icon("luggage-strap", CAT, "Suitcase wrapped by a wide strap with a square buckle",
      tags=["luggage belt", "suitcase belt", "baggage strap", "travel", "secure", "bag"])
def _(S):
    return [
        line("M9 6V3.5h6V6"),
        shell(rect(3, 6, 18, 15, rr(S, 3))),
        detail(seg(3, 10.5, 9.5, 10.5)), detail(seg(14.5, 10.5, 21, 10.5)),
        detail(seg(3, 16.5, 9.5, 16.5)), detail(seg(14.5, 16.5, 21, 16.5)),
        shell(rect(9.5, 9.5, 5, 8, rr(S, 1))),
    ]


@icon("travel-pillow", CAT, "U-shaped neck pillow with a strap closing the gap",
      tags=["neck pillow", "neck cushion", "flight", "comfort", "sleep", "airplane"])
def _(S):
    return [
        shell(L(S, "M3.5 3.5h4c1 0 1 1 1 2.5v6a3.5 3.5 0 0 0 7 0V6c0-1.5 0-2.5 1-2.5h4V12a8.5 8.5 0 0 1-17 0Z",
                "M5.5 3.5C3.5 3.5 3.5 6 3.5 8v4a8.5 8.5 0 0 0 17 0V8c0-2 0-4.5-2-4.5-2.5 0-3 1.5-3 4V12a3.5 3.5 0 0 1-7 0V7.5C8.5 5 8 3.5 5.5 3.5Z")),
        line(seg(8.5, 7.5, 15.5, 7.5)),
    ]


@icon("money-belt", CAT, "Flat zipped pouch on a waist belt",
      tags=["hidden wallet", "travel wallet", "pouch", "waist pouch", "security", "anti theft", "travel"])
def _(S):
    return [
        line(seg(2, 14.5, 6, 14.5)), line(seg(18, 14.5, 22, 14.5)),
        shell(rect(6, 5.5, 12, 14, rr(S, 4))),
        detail(seg(6, 10, 18, 10)),
        dot(15, 13.5, 1.1) if False else dot(12, 15.5, 1.25),
    ]


@icon("packing-cube", CAT, "Fabric packing cube with a zipper around three sides and a loop handle",
      tags=["luggage organizer", "compression cube", "suitcase organizer", "travel", "zipper", "packing"])
def _(S):
    return [
        line("M10 6.5V4h4v2.5"),
        shell(rect(3, 6.5, 18, 14, rr(S, 4))),
        detail("M7.5 17V11h9v6"),
    ]


@icon("open-suitcase", CAT, "Open suitcase with its lid raised and folded clothes inside",
      tags=["packing", "unpack", "pack", "luggage", "clothes", "trip", "travel"])
def _(S):
    return [
        shell(poly([(7, 2.5), (17, 2.5), (19.5, 9), (4.5, 9)], closed=True, r=S.r)),
        shell(rect(3, 11.5, 18, 9.5, rr(S, 4))),
        detail(seg(7, 16, 17, 16)),
    ]


@icon("travel-guidebook", CAT, "Thick guidebook standing upright with a map pin and mountain on the cover",
      tags=["guide book", "travel guide", "tourist", "sightseeing", "destination", "map pin"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, rr(S, 2))),
        detail(seg(8, 3.5, 8, 20.5)),
        solid("M14 12C12.2 10 11.5 8.8 11.5 7.5a2.5 2.5 0 0 1 5 0C16.5 8.8 15.8 10 14 12Z"),
        detail(poly([(10.5, 19), (13, 16), (14.5, 17.5), (16.5, 15.5)], r=S.r * 0.5)),
    ]


@icon("phrasebook", CAT, "Small book with two overlapping speech bubbles on the cover",
      tags=["language guide", "translation", "dictionary", "foreign language", "travel", "conversation"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, rr(S, 2))),
        detail(rect(6.5, 6, 7, 5, rr(S, 1.5))),
        solid(rect(10.5, 13, 7, 4, L(S, 0.5, 1.5))),
    ]


@icon("travel-journal", CAT, "Notebook held shut by a cord with a small paper plane on the cover",
      tags=["travel diary", "trip log", "notebook", "memories", "writing", "adventure"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, L(S, 2, 4))),
        detail(seg(16, 2.5, 16, 21.5)),
        solid(poly([(7.5, 13), (13, 8.5), (11, 15)], closed=True)),
        dot(16, 17, 1.25),
    ]


@icon("selfie-stick", CAT, "Extendable pole with a grip at the bottom and a phone clamped at the top",
      tags=["monopod", "phone pole", "photo", "tourist", "selfie", "camera pole"])
def _(S):
    return [
        shell(bar((4, 20.5), (8, 17.5), 2.5, r=S.r * 0.3)),
        line(seg(8.5, 17, 14, 13)),
        shell(rect(12, 2.5, 9, 11, rr(S, 2))),
        dot(16.5, 10.5, 1),
    ]


@icon("travel-itinerary", CAT, "Trip plan sheet with a small plane and a timeline of stops",
      tags=["trip plan", "schedule", "agenda", "travel plan", "route", "stops", "timeline"])
def _(S):
    return [
        shell(rect(4, 2, 16, 20, rr(S, 2))),
        solid(poly([(7, 8.5), (11.5, 5), (10.5, 9.5)], closed=True)),
        detail(seg(13.5, 7, 17, 7)),
        dot(8.5, 12.5, 1.25), detail(seg(12, 12.5, 17, 12.5)),
        dot(8.5, 17.5, 1.25), detail(seg(12, 17.5, 17, 17.5)),
    ]


def _ticket(S, x0, y0, x1, y1, n_r=2.0):
    r = L(S, 0.0, 2.5)
    cy = (y0 + y1) / 2
    top = f"M{fmt(x0 + r)} {fmt(y0)}H{fmt(x1 - r)}" + (f"a{fmt(r)} {fmt(r)} 0 0 1 {fmt(r)} {fmt(r)}" if r else "")
    right = f"V{fmt(cy - n_r)}a{fmt(n_r)} {fmt(n_r)} 0 0 0 0 {fmt(2 * n_r)}V{fmt(y1 - r)}"
    bottom = (f"a{fmt(r)} {fmt(r)} 0 0 1 {fmt(-r)} {fmt(r)}" if r else "") + f"H{fmt(x0 + r)}"
    left = (f"a{fmt(r)} {fmt(r)} 0 0 1 {fmt(-r)} {fmt(-r)}" if r else "") + f"V{fmt(cy + n_r)}a{fmt(n_r)} {fmt(n_r)} 0 0 0 0 {fmt(-2 * n_r)}V{fmt(y0 + r)}"
    close = (f"a{fmt(r)} {fmt(r)} 0 0 1 {fmt(r)} {fmt(-r)}" if r else "") + "Z"
    return top + right + bottom + left + close


@icon("train-ticket", CAT, "Rail ticket with a perforated stub and a small train front",
      tags=["rail ticket", "railway", "commuter", "transit pass", "journey", "perforated", "travel"])
def _(S):
    return [
        shell(_ticket(S, 2, 4.5, 22, 19.5)),
        detail("M16.5 6.5v2M16.5 10.5v2M16.5 14.5v2"),
        detail(rect(5, 8, 7, 5, rr(S, 2))),
        dot(6.5, 16.3, 1), dot(10.5, 16.3, 1),
    ]


@icon("travel-insurance", CAT, "Umbrella canopy held over a suitcase",
      tags=["trip protection", "cover", "cancellation", "coverage", "protect luggage", "policy", "safe travel"])
def _(S):
    return [
        shell("M3 10A9 8 0 0 1 21 10a3 2.5 0 0 0-6 0a3 2.5 0 0 0-6 0a3 2.5 0 0 0-6 0Z"),
        line(seg(12, 10, 12, 12.5)),
        line("M10 15.5V13.5h4v2"),
        shell(rect(6, 15.5, 12, 6, rr(S, 2))),
    ]


@icon("jet-lag", CAT, "Airplane flying above a crescent moon with sleepy z letters",
      tags=["time zone", "tired", "sleepy", "fatigue", "flight", "night", "insomnia"])
def _(S):
    return [
        shell("M10.75 10.2A5.5 5.5 0 1 0 13.4 16A4.2 4.2 0 0 1 10.75 10.2Z"),
        plane(S, 17, 6.5, 0.62, 45),
        line("M17 14h4l-4 4.5h4"),
    ]


@icon("fasten-seatbelt-sign", CAT, "Lit cabin sign panel showing a seated person wearing a belt",
      tags=["seat belt sign", "cabin sign", "airplane", "flight safety", "turbulence", "buckle up", "warning light"])
def _(S):
    return [
        shell(rect(3, 7, 18, 10, rr(S, 4))),
        detail(seg(3, 12, 10, 12)), detail(seg(14, 12, 21, 12)),
        solid(rect(9.5, 9.5, 5, 5, L(S, 0.5, 1.5))),
        line(seg(12, 1.5, 12, 4)), line(seg(5.5, 2.5, 7, 4.5)), line(seg(18.5, 2.5, 17, 4.5)),
        line(seg(12, 20, 12, 22.5)),
    ]


# ============================================================================ airport and hotel

@icon("air-traffic-control-tower", CAT, "Slim control tower with a wide flared glass cab and an antenna",
      tags=["atc", "airport tower", "control tower", "aviation", "airfield", "flight control", "runway"])
def _(S):
    return [
        line(seg(12, 5, 12, 1.5)),
        shell(poly([(10, 10), (14, 10), (14.5, 21.5), (9.5, 21.5)], closed=True, r=S.r * 0.4)),
        shell(poly([(7, 5), (17, 5), (20.5, 10), (3.5, 10)], closed=True, r=S.r)),
        line(seg(6.5, 21.5, 17.5, 21.5)),
    ]


@icon("airport-seats", CAT, "Row of three connected waiting chairs on a shared frame",
      tags=["waiting area", "gate seating", "terminal chairs", "bench", "lounge", "departure lounge", "seats"])
def _(S):
    return [
        shell(rect(3, 3.5, 18, 8, rr(S, 4))),
        detail(seg(9, 3.5, 9, 11.5)), detail(seg(15, 3.5, 15, 11.5)),
        shell(rect(3, 13.5, 18, 4, rr(S, 2))),
        line(seg(6, 17.5, 6, 21.5)), line(seg(18, 17.5, 18, 21.5)),
    ]


@icon("hotel-room-key", CAT, "Old-style metal key hanging from a ring with an oval number fob",
      tags=["room key", "door key", "hotel key", "keyring", "fob", "check in", "guest"])
def _(S):
    return [
        shell(circle(5.5, 6, 3.25)),
        line(seg(8.75, 6, 21, 6)),
        line(seg(18, 6, 18, 9)), line(seg(21, 6, 21, 8.5)),
        line(seg(5.5, 9.25, 5.5, 14)),
        shell(ellipse(10, 17.75, 7, 4)),
        detail(seg(10, 15.75, 10, 19.75)),
    ]


@icon("door-hanger", CAT, "Door hanger card with a round hole near the top and a crescent moon",
      tags=["do not disturb", "privacy sign", "hotel sign", "sleeping", "quiet", "door sign", "room"])
def _(S):
    return [
        shell(rect(6, 2, 12, 20, rr(S, 4))),
        detail(circle(12, 6.75, 1.75)),
        solid("M14.5 12.5A3.5 3.5 0 1 0 14.5 18.5A3.5 3.5 0 0 1 14.5 12.5Z"),
    ]


@icon("room-service-cart", CAT, "Wheeled serving cart with a cloth, a domed food cover and a flower",
      tags=["hotel cart", "trolley", "meal delivery", "food cover", "cloche", "catering", "guest service"])
def _(S):
    return [
        shell("M4.5 10.5a4.5 4.5 0 0 1 9 0Z"),
        dot(9, 4.75, 1),
        line(seg(18, 12, 18, 8)), dot(18, 6.5, 1.5),
        shell(poly([(3, 12), (21, 12), (19, 19), (5, 19)], closed=True, r=S.r * 0.5)),
        dot(7, 21.25, 1), dot(17, 21.25, 1),
    ]


@icon("minibar", CAT, "Small fridge opened to show bottles on the top shelf and cans below",
      tags=["mini fridge", "hotel fridge", "drinks", "refrigerator", "snacks", "room fridge", "beverages"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 4))),
        solid(rect(7, 5.5, 2.5, 5, 0.5)), solid(rect(10.75, 5.5, 2.5, 5, 0.5)), solid(rect(14.5, 5.5, 2.5, 5, 0.5)),
        detail(seg(4, 12.75, 20, 12.75)),
        solid(rect(7, 15.5, 4, 3.5, 0.5)), solid(rect(13, 15.5, 4, 3.5, 0.5)),
    ]


@icon("towel-animal", CAT, "Towel folded into a swan with a curved neck",
      tags=["towel swan", "folded towel", "hotel", "housekeeping", "decoration", "origami", "room"])
def _(S):
    return [
        shell("M3.5 15C3.5 14 4.5 13.5 6 13.5H15C17 13.5 19 12 21 9.5C21 15 18 18.5 12 18.5C7 18.5 3.5 17 3.5 15Z"),
        line("M8 13.5C3.5 12.5 3.5 8.5 5.5 7"),
        dot(5.5, 5.75, 1.6),
        solid(poly([(4.3, 4.6), (1.6, 5.8), (4.3, 6.9)], closed=True)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("rollaway-bed", CAT, "Folding guest bed on wheels with the mattress folded partly upright",
      tags=["folding bed", "cot", "extra bed", "guest bed", "camp bed", "portable bed", "hotel"])
def _(S):
    return [
        shell(rect(3, 11.5, 12, 3.5, rr(S, 1.5))),
        shell(bar((15.5, 13), (20.5, 5), 3.5, r=S.r * 0.4)),
        line(seg(5.5, 15, 11.5, 20.5)), line(seg(11.5, 15, 5.5, 20.5)),
        dot(4.5, 21.5, 1.25), dot(12.5, 21.5, 1.25),
    ]


@icon("housekeeping-cart", CAT, "Cleaning cart with a shelf, folded towels on top and a hanging linen bag",
      tags=["maid cart", "janitor cart", "cleaning trolley", "hotel cleaning", "towels", "linen", "room attendant"])
def _(S):
    return [
        solid(rect(5, 4.5, 8, 3.5, 0.6)),
        shell(rect(3, 9.5, 13, 9, rr(S, 4))),
        detail(seg(3, 14, 16, 14)),
        shell(rect(17.5, 6.5, 4.5, 12, rr(S, 2))),
        dot(6.5, 21.25, 1.1), dot(13, 21.25, 1.1),
    ]


@icon("wake-up-call", CAT, "Desk telephone with twin alarm bells above the handset and ring marks",
      tags=["alarm call", "morning call", "hotel phone", "reception", "reminder", "alarm phone", "early call"])
def _(S):
    return [
        line(seg(1.5, 4.5, 3.5, 6)), line(seg(22.5, 4.5, 20.5, 6)),
        solid("M5 9a3 3 0 0 1 6 0Z"), solid("M13 9a3 3 0 0 1 6 0Z"),
        shell(poly([(3, 9.5), (21, 9.5), (21, 14), (17.5, 14), (17.5, 12), (6.5, 12), (6.5, 14), (3, 14)], closed=True, r=S.r * 0.5)),
        shell(poly([(6, 16), (18, 16), (21, 21.5), (3, 21.5)], closed=True, r=S.r)),
    ]


@icon("cloakroom-ticket", CAT, "Numbered claim ticket hanging from a coat hanger",
      tags=["coat check", "claim tag", "coat hanger", "cloak room", "check ticket", "theatre", "cloakroom"])
def _(S):
    return [
        line("M12 7.5V6.5a2.2 2.2 0 1 0-2.2-2.2"),
        line(poly([(3, 12.5), (12, 7.5), (21, 12.5)])),
        line(seg(12, 12.5, 12, 15)),
        shell(rect(7.5, 15, 9, 6.5, rr(S, 2))),
        dot(12, 18.25, 1.1),
    ]


@icon("motel-sign", CAT, "Roadside pole sign with an arrow-shaped panel lined with bulbs",
      tags=["roadside sign", "vacancy", "neon sign", "highway", "lodging", "inn", "pole sign"])
def _(S):
    return [
        shell(poly([(3, 2.5), (16, 2.5), (21.5, 8), (16, 13.5), (3, 13.5)], closed=True, r=S.r)),
        dot(7.5, 8, 1.25), dot(11.5, 8, 1.25), dot(15.5, 8, 1.25),
        line(seg(8, 13.5, 8, 21.5)), line(seg(4.5, 21.5, 11.5, 21.5)),
    ]


@icon("bed-and-breakfast", CAT, "Small cottage with a steaming coffee cup in front of the door",
      tags=["b&b", "guesthouse", "inn", "lodging", "breakfast", "homestay", "cottage"])
def _(S):
    return [
        line(poly([(2, 11), (12, 3), (22, 11)])),
        line("M4.5 10.5V21.5h15V10.5"),
        shell(poly([(8, 14.5), (14, 14.5), (13.5, 19.5), (8.5, 19.5)], closed=True, r=S.r * 0.4)),
        line("M14 15.5h1.5a1.5 1.5 0 0 1 0 3H13.8"),
        line("M11 12.5c-1.2-1 1.2-2 0-3.2"),
    ]


@icon("ryokan", CAT, "Japanese inn with a two-tier curved roof and a split curtain over the door",
      tags=["japanese inn", "traditional inn", "onsen", "tatami", "noren", "japan", "guesthouse"])
def _(S):
    return [
        shell("M5 7C9 6.5 11 4.5 12 2.5C13 4.5 15 6.5 19 7Z"),
        shell("M2 14C7.5 13.5 10.5 11.5 12 9.5C13.5 11.5 16.5 13.5 22 14Z"),
        line(seg(5.5, 14.5, 5.5, 21.5)), line(seg(18.5, 14.5, 18.5, 21.5)),
        shell(rect(8.5, 16, 7, 5.5, rr(S, 1.5))),
        detail(seg(12, 16, 12, 21.5)),
    ]


@icon("bell-tent", CAT, "Round canvas tent with one tall centre pole, a sloped conical roof and a zipped door",
      tags=["glamping", "yurt style", "canvas tent", "round tent", "camping", "festival", "pole tent"])
def _(S):
    r = L(S, 0.0, 2.0)
    return [
        line(seg(12, 4, 12, 1.5)),
        shell(f"M12 3.5C13.5 7.5 17 11 21 13.5V{21.5 - r}" + (f"A{r} {r} 0 0 1 {21 - r} 21.5H{3 + r}A{r} {r} 0 0 1 3 {21.5 - r}" if r else "V21.5H3V21.5") + "V13.5C7 11 10.5 7.5 12 3.5Z"),
        detail("M9.25 21.5V17a2.75 2.75 0 0 1 5.5 0V21.5"),
    ]


@icon("safari-tent", CAT, "Canvas tent with an open door flap pitched on a raised deck",
      tags=["glamping", "luxury tent", "camp", "safari lodge", "canvas tent", "deck", "wildlife camp"])
def _(S):
    return [
        shell(poly([(4, 15), (12, 4), (20, 15)], closed=True, r=S.r * 0.6)),
        detail(poly([(9.5, 15), (12, 10.5), (14.5, 15)])),
        shell(rect(2, 17, 20, 2.5, rr(S, 1))),
        line(seg(5, 19.5, 5, 22)), line(seg(19, 19.5, 19, 22)),
    ]


# ============================================================================ pool, beach and water

def arrow_head(cx, cy, r, deg, size=3.0):
    """Solid arrowhead at angle deg on a circle, pointing clockwise along the arc."""
    a = math.radians(deg)
    px, py = cx + r * math.cos(a), cy + r * math.sin(a)
    tx, ty = -math.sin(a), math.cos(a)
    nx, ny = math.cos(a), math.sin(a)
    tip = (px + tx * size * 0.9, py + ty * size * 0.9)
    return solid(poly([tip, (px + nx * size * 0.8, py + ny * size * 0.8), (px - nx * size * 0.8, py - ny * size * 0.8)], closed=True))


WAVE = "q1.5-1.5 3 0t3 0"


@icon("swimming-pool", CAT, "Pool with a ripple line and a curved metal ladder rising over the edge",
      tags=["pool", "swim", "lido", "water", "resort", "hotel pool", "swimming", "ladder"])
def _(S):
    return [
        line("M7.5 13.5V6A3 3 0 0 1 10.5 3"), line("M13.5 13.5V6A3 3 0 0 1 16.5 3"),
        line("M3 11v7a3 3 0 0 0 3 3h12a3 3 0 0 0 3-3v-7"),
        line("M5 17.5q1.75-1.75 3.5 0t3.5 0t3.5 0t3.5 0"),
    ]


@icon("poolside-cabana", CAT, "Flat-roofed cabana with curtains tied back at the corner posts",
      tags=["cabana", "pavilion", "canopy", "resort", "sun shade", "gazebo", "beach hut"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 3.5, L(S, 1, 1.75))),
        shell("M5 6.5H10C10 10 8 11.5 8 14C8 17 10 18.5 10 21.5H5Z"),
        shell("M19 6.5H14C14 10 16 11.5 16 14C16 17 14 18.5 14 21.5H19Z"),
    ]


@icon("turndown-service", CAT, "Plump pillow with a wrapped chocolate resting on top",
      tags=["chocolate", "pillow mint", "hotel evening", "bedtime", "housekeeping", "sweet", "good night"])
def _(S):
    return [
        shell(rect(3, 11, 18, 10, rr(S, 5))),
        shell(rect(9.25, 4.5, 5.5, 4, rr(S, 1))),
        solid(poly([(9.25, 6.5), (6, 4.5), (6, 8.5)], closed=True)),
        solid(poly([(14.75, 6.5), (18, 4.5), (18, 8.5)], closed=True)),
    ]


@icon("towel-reuse", CAT, "Folded towel surrounded by two circular arrows",
      tags=["reuse towel", "eco hotel", "green choice", "sustainability", "recycle", "laundry", "save water"])
def _(S):
    return [
        line(arc(12, 12, 9.5, 205, 330)), arrow_head(12, 12, 9.5, 330),
        line(arc(12, 12, 9.5, 25, 150)), arrow_head(12, 12, 9.5, 150),
        shell(rect(7.5, 9, 9, 6, rr(S, 2))),
    ]


@icon("reservation-book", CAT, "Open booking ledger with time slots, one checked, on a narrow stand",
      tags=["booking", "host stand", "restaurant", "table booking", "appointments", "guest list", "reserve"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 13, rr(S, 2))),
        detail(seg(12, 3, 12, 16)),
        detail(seg(5.5, 7.5, 9.5, 7.5)), detail(seg(5.5, 12, 9.5, 12)),
        detail("M14.5 7.5l1.75 1.75L19.5 6"), detail(seg(14.5, 12, 19, 12)),
        line(seg(12, 16, 12, 20)), line(seg(7.5, 21, 16.5, 21)),
    ]


@icon("diving-board", CAT, "Springboard reaching out over the pool from a base, with water below",
      tags=["springboard", "dive", "pool", "jump", "swimming", "platform", "splash"])
def _(S):
    return [
        shell(rect(3, 11, 5.5, 10, rr(S, 1.5))),
        shell(rect(6, 8, 16, 3, rr(S, 1.5))),
        line("M12 16.5q1.5-1.5 3 0t3 0t3 0"),
        line("M12 20.5q1.5-1.5 3 0t3 0t3 0"),
    ]


@icon("flamingo-float", CAT, "Inflatable pool ring with a flamingo neck and head rising from one side",
      tags=["pool float", "inflatable", "flamingo", "pool toy", "swim ring", "summer", "pink flamingo"])
def _(S):
    return [
        shell(ellipse(10.5, 16.5, 8.5, 4.5)),
        detail(ellipse(10.5, 16.5, L(S, 3.8, 3.4), L(S, 1.9, 2.1))),
        line("M17.5 12.5C22 11 22 6.5 19 5.5"),
        dot(18.25, 4.6, 1.5),
        solid(poly([(17.2, 3.6), (14, 5.4), (17.4, 5.8)], closed=True)),
    ]


@icon("fridge-magnet", CAT, "Souvenir magnet shaped like a sun with rays on a square plate",
      tags=["souvenir", "gift", "magnet", "holiday memento", "tourist shop", "sun", "keepsake"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 5))),
        solid(circle(12, 12, 3.2)),
        dot(12, 6.3, 1), dot(12, 17.7, 1), dot(6.3, 12, 1), dot(17.7, 12, 1),
        dot(8, 8, 1), dot(16, 8, 1), dot(8, 16, 1), dot(16, 16, 1),
    ]


@icon("spyglass", CAT, "Collapsible telescope extended into three tube sections",
      tags=["telescope", "pirate", "lookout", "scope", "monocular", "sailing", "exploring"])
def _(S):
    return [
        shell(bar((3.5, 20.5), (8.4, 15.6), 3, r=S.r * 0.3)),
        shell(bar((8, 16), (13.5, 10.5), 5, r=S.r * 0.3)),
        shell(bar((13.1, 10.9), (19.5, 4.5), 7, r=S.r * 0.3)),
    ]


@icon("message-in-a-bottle", CAT, "Corked glass bottle lying on its side with a rolled note inside",
      tags=["bottle", "letter", "castaway", "sea mail", "drift", "note", "ocean message"])
def _(S):
    return [
        shell(poly([(18.5, 10.5), (15.5, 10.5), (12.5, 7), (2.5, 7), (2.5, 17), (12.5, 17), (15.5, 13.5), (18.5, 13.5)], closed=True, r=S.r)),
        shell(rect(18.5, 10, 3, 4, L(S, 0.5, 1.5))),
        detail(seg(6, 12, 11.5, 12)),
    ]


@icon("whale-watching", CAT, "Small boat on waves beside a whale tail rising from the water",
      tags=["whale tail", "boat trip", "marine tour", "ocean wildlife", "fluke", "sea", "eco tour"])
def _(S):
    return [
        shell(poly([(2, 14.5), (10, 14.5), (8.5, 17.5), (3.5, 17.5)], closed=True, r=S.r * 0.4)),
        shell(rect(3.5, 10.5, 4.5, 4, rr(S, 1))),
        line(seg(17, 11.5, 17, 19)),
        shell("M17 11.5C14.5 11.5 13 10 12 7C14.5 7.5 16 8 17 9C18 8 19.5 7.5 22 7C21 10 19.5 11.5 17 11.5Z"),
        line("M2 20.5" + WAVE + "t3 0t3 0t3 0t3 0"),
    ]


@icon("canopy-walkway", CAT, "Rope bridge strung between two tall tree trunks",
      tags=["rope bridge", "treetop walk", "suspension bridge", "rainforest", "zip line park", "adventure", "forest"])
def _(S):
    return [
        line(seg(4.5, 2, 4.5, 22)), line(seg(19.5, 2, 19.5, 22)),
        line("M4.5 8Q12 13 19.5 8"),
        line("M4.5 14Q12 19 19.5 14"),
        line(seg(9.5, 10.2, 9.5, 15.4)), line(seg(14.5, 10.2, 14.5, 15.4)),
    ]


@icon("beach-windbreak", CAT, "Fabric screen stretched between three poles pushed into the sand",
      tags=["wind screen", "beach shelter", "sand", "shield", "sun protection", "beach gear", "screen"])
def _(S):
    return [
        line(seg(4, 3, 4, 21.5)), line(seg(12, 3, 12, 21.5)), line(seg(20, 3, 20, 21.5)),
        line("M4 6Q8 9 12 6Q16 9 20 6"),
        line("M4 15Q8 18 12 15Q16 18 20 15"),
    ]


@icon("rescue-buoy", CAT, "Lifeguard rescue can, a torpedo-shaped float with bands and a rope loop",
      tags=["lifeguard", "life saver", "float", "rescue can", "water rescue", "beach safety", "drowning"])
def _(S):
    body = [(0, -3.2), (11, -3.2), (16, 0), (11, 3.2), (0, 3.2)]
    pts = rotpts(body, -40, ox=5.5, oy=18.5)
    a = rotpts([(4, -3.2), (4, 3.2)], -40, ox=5.5, oy=18.5)
    b = rotpts([(9.5, -3.2), (9.5, 3.2)], -40, ox=5.5, oy=18.5)
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(*a[0], *a[1])), detail(seg(*b[0], *b[1])),
        line("M4 17C1.5 13 3.5 9.5 7 9.5"),
    ]


@icon("snorkel", CAT, "Diving mask with one wide lens and a J-shaped breathing tube at the side",
      tags=["diving mask", "snorkeling", "goggles", "underwater", "reef", "swim gear", "mask"])
def _(S):
    return [
        shell(poly([(2.5, 5), (15.5, 5), (15.5, 13), (12, 13), (10.5, 16.5), (7.5, 16.5), (6, 13), (2.5, 13)], closed=True, r=S.r)),
        line(seg(15.5, 8, 20.5, 8)),
        line("M20.5 3V16a3 3 0 0 1-3 3H13"),
    ]


# ============================================================================ diving, boards and beach life

@icon("scuba-tank", CAT, "Air cylinder with a top valve, a hose to the regulator and a strap band",
      tags=["diving tank", "oxygen tank", "air cylinder", "dive gear", "underwater", "compressed air", "regulator"])
def _(S):
    return [
        line(seg(12, 8, 12, 5)),
        shell(rect(9.5, 2.5, 5, 2.5, rr(S, 1))),
        line("M14.5 3.75h2.5a2.5 2.5 0 0 1 2.5 2.5V11"),
        shell(rect(6.5, 8, 11, 13.5, L(S, 2.5, 5.5))),
        detail(seg(6.5, 13, 17.5, 13)),
    ]


@icon("swim-fins", CAT, "Pair of diving fins with narrow foot pockets and wide ribbed blades",
      tags=["flippers", "snorkeling fins", "diving fins", "swimming gear", "scuba", "water sports", "paddle feet"])
def _(S):
    return [
        shell(poly([(4.5, 3), (8, 3), (8.5, 8), (10, 21.5), (2.5, 21.5), (4, 8)], closed=True, r=S.r)),
        shell(poly([(16, 3), (19.5, 3), (20, 8), (21.5, 21.5), (14, 21.5), (15.5, 8)], closed=True, r=S.r)),
        detail(seg(6.25, 12, 6.25, 18)), detail(seg(17.75, 12, 17.75, 18)),
    ]


@icon("dive-flag", CAT, "Rectangular flag on a pole with one diagonal stripe corner to corner",
      tags=["diver down", "diving flag", "scuba flag", "marker", "warning flag", "water safety", "stripe"])
def _(S):
    return [
        line(seg(4.5, 2, 4.5, 22)),
        shell(rect(4.5, 3.5, 16, 12, rr(S, 2))),
        detail(seg(4.5, 15.5, 20.5, 3.5)),
    ]


@icon("bodyboard", CAT, "Short foam board with a curved nose and a coiled leash at the tail",
      tags=["boogie board", "surf", "wave riding", "foam board", "beach", "waves", "surfing"])
def _(S):
    board = [(0, -3.6), (10, -3.6), (15, -1.5), (15, 1.5), (10, 3.6), (0, 3.6)]
    pts = rotpts(board, -45, ox=6, oy=17)
    ax = rotpts([(3, 0), (11, 0)], -45, ox=6, oy=17)
    return [
        shell(poly(pts, closed=True, r=S.r)),
        detail(seg(*ax[0], *ax[1])),
        line("M4 18.5C1.5 18 1.5 21 4.5 21.5C6.5 21.5 6.5 19.5 5 19.5"),
    ]


@icon("kitesurfing", CAT, "Rider on a small board pulled by a crescent kite on long lines",
      tags=["kiteboarding", "kite", "wind sport", "water sport", "board", "kite board", "surf"])
def _(S):
    return [
        shell("M3.5 6C8 1 16 1 20.5 6C16 4 8 4 3.5 6Z"),
        line(seg(5.5, 5.2, 12, 10)), line(seg(18.5, 5.2, 12, 10)),
        line(seg(10, 10, 14, 10)),
        dot(12, 14, 1.6),
        line(seg(12, 15.5, 12, 18.5)),
        shell(rect(6, 19, 12, 2.25, rr(S, 1))),
    ]


@icon("water-skiing", CAT, "Skier leaning back on two skis, holding a tow handle with the rope running ahead",
      tags=["waterski", "skis", "tow rope", "boat sport", "lake", "wakeboard", "summer sport"])
def _(S):
    return [
        dot(11, 5.5, 1.9),
        line("M11 9L9.5 15.5"),
        line("M11 10.5L17 12.5"),
        line("M9.5 15.5L8 19"),
        line(seg(3, 20.5, 13, 20.5)),
        line(seg(17, 10, 17, 14.5)), line(seg(17, 12.25, 22, 12.25)),
        dot(3.5, 16, 1), dot(6, 14, 1), dot(3, 12.5, 1),
    ]


@icon("beach-warning-flag", CAT, "Triangular warning flag on a pole in the sand beside wave lines",
      tags=["lifeguard flag", "swim warning", "surf safety", "danger flag", "rip current", "beach safety", "sea conditions"])
def _(S):
    return [
        line(seg(8, 2.5, 8, 19.5)),
        shell(poly([(8, 4), (19, 8.5), (8, 13)], closed=True, r=S.r * 0.6)),
        line(seg(3, 21, 13, 21)),
        line("M13.5 18q1.25-1.25 2.5 0t2.5 0t2.5 0"),
    ]


@icon("tiki-bar", CAT, "Thatched roof bar on posts with a counter and two stools in front",
      tags=["beach bar", "cocktail hut", "thatched", "tropical", "drinks", "resort bar", "island"])
def _(S):
    return [
        shell(poly([(3, 9), (12, 3.5), (21, 9)], closed=True, r=S.r * 0.6), stroke_miterlimit="2"),
        line(seg(5.5, 9, 5.5, 12.5)), line(seg(18.5, 9, 18.5, 12.5)),
        shell(rect(3, 12.5, 18, 3.5, rr(S, 1.5))),
        solid(rect(5.75, 18, 5, 1.5, 0.5)), line(seg(8.25, 19.5, 8.25, 21.5)),
        solid(rect(13.25, 18, 5, 1.5, 0.5)), line(seg(15.75, 19.5, 15.75, 21.5)),
    ]


@icon("sunbather", CAT, "Person lying on a beach towel under a sun shown with dots for rays",
      tags=["sunbathing", "tanning", "beach", "relax", "sun tan", "lounging", "summer holiday"])
def _(S):
    return [
        shell(circle(5.25, 13.5, 2.25)),
        line(seg(8.5, 14.5, 16, 14.5)), line(seg(16, 14.5, 20.5, 12.5)),
        shell(rect(2, 17.5, 20, 3.5, rr(S, 1.75))),
        solid(circle(17, 5.5, 2.25)),
        dot(17, 1.5, 0.9), dot(21, 5.5, 0.9), dot(13, 5.5, 0.9), dot(20, 2.5, 0.9), dot(14, 2.5, 0.9),
    ]


@icon("beach-wagon", CAT, "Folding fabric cart on two fat balloon wheels with a pull handle",
      tags=["beach cart", "wagon", "trolley", "cooler cart", "sand cart", "folding cart", "haul gear"])
def _(S):
    return [
        line("M6.5 13H2.5V5.5"),
        shell(rect(6.5, 6.5, 15, 10, rr(S, 4))),
        detail(seg(11.5, 6.5, 11.5, 16.5)) if False else detail(seg(6.5, 11, 21.5, 11)),
        shell(circle(9, 18.5, 2.5)), shell(circle(18, 18.5, 2.5)),
    ]


# ============================================================================ camp gear

@icon("sleeping-bag", CAT, "Mummy sleeping bag lying flat with a rounded hood and a zipper",
      tags=["mummy bag", "camping", "bedroll", "outdoor bed", "hiking", "overnight", "tent sleep"])
def _(S):
    r = L(S, 0.6, 2.6)
    return [
        shell(f"M12 2.5C8.5 2.5 7 4.5 7 7L5.5 19.4A{r} {r} 0 0 0 {5.5 + r} 21.5H{18.5 - r}A{r} {r} 0 0 0 18.5 19.4L17 7C17 4.5 15.5 2.5 12 2.5Z"),
        detail("M8.75 9.5a3.25 3.25 0 0 1 6.5 0"),
        detail(seg(12, 9.5, 12, 21.5)),
    ]


@icon("sleeping-pad", CAT, "Foam camping mat rolled into a cylinder and tied with two straps",
      tags=["sleep mat", "camp mat", "foam roll", "insulated pad", "camping", "bedroll", "trail gear"])
def _(S):
    return [
        shell(rect(3, 7, 18, 10, L(S, 2, 5))),
        dot(7.75, 12, 1.6),
        detail(seg(12.5, 7, 12.5, 17)), detail(seg(17.5, 7, 17.5, 17)),
    ]


@icon("tent-stake", CAT, "Metal tent peg with a hooked top driven into the ground with a guy line tied on",
      tags=["tent peg", "peg", "ground anchor", "guy line", "camping", "pitch tent", "spike"])
def _(S):
    return [
        line(seg(7.5, 20.5, 16.5, 9.5)),
        line("M16.5 9.5C14.5 7 17 4 19.5 6"),
        line("M18.5 7L22 2.5"),
        line(seg(2, 21.5, 11, 21.5)),
    ]


@icon("backpacking-stove", CAT, "Small burner with folding pot supports screwed onto a gas canister",
      tags=["camp stove", "gas stove", "trail stove", "cooking", "burner", "hiking", "canister stove"])
def _(S):
    return [
        line(poly([(3, 6.5), (6, 6.5), (9.5, 11)])), line(poly([(21, 6.5), (18, 6.5), (14.5, 11)])),
        shell(rect(9, 11, 6, 3.5, rr(S, 1))),
        shell(rect(6.5, 15.5, 11, 6, rr(S, 4))),
    ]


@icon("fuel-canister", CAT, "Squat round gas canister with a threaded valve on top",
      tags=["gas canister", "propane", "butane", "camp fuel", "gas cylinder", "stove fuel", "camping"])
def _(S):
    r = L(S, 0.6, 3)
    return [
        shell(rect(9.5, 3.5, 5, 6.5, rr(S, 1))),
        shell(f"M5.5 13C5.5 11.2 8.2 10 12 10S18.5 11.2 18.5 13V{21.5 - r}A{r} {r} 0 0 1 {18.5 - r} 21.5H{5.5 + r}A{r} {r} 0 0 1 5.5 {21.5 - r}Z"),
        detail(seg(5.5, 16.5, 18.5, 16.5)),
    ]


@icon("mess-kit", CAT, "Camping pot with a lid and folding handle, a small cup peeking out above",
      tags=["camp cookware", "pot", "billycan", "cook set", "hiking kitchen", "camping", "canteen"])
def _(S):
    return [
        shell(rect(7.5, 2.5, 7, 4.5, rr(S, 1.5))),
        shell(rect(3, 8.5, 16, 2.75, rr(S, 1.25))),
        shell(rect(4, 11.25, 14, 9.25, rr(S, 4))),
        line(seg(18, 14, 22, 14)),
    ]


@icon("portable-water-filter", CAT, "Hand pump water filter with an intake hose and an outlet tube",
      tags=["water purifier", "pump filter", "hiking", "drinking water", "backpacking", "clean water", "survival"])
def _(S):
    return [
        line(seg(11.5, 7, 11.5, 3)), line(seg(8.5, 3, 14.5, 3)),
        shell(rect(8, 7, 7, 13.5, rr(S, 3))),
        line("M8 17H5.5A2.5 2.5 0 0 1 3 14.5V12"),
        line("M15 10.5h3.5a2.5 2.5 0 0 1 2.5 2.5v4"),
    ]


@icon("camp-chair", CAT, "Folding camp chair with a fabric seat and back, armrests and crossed legs",
      tags=["folding chair", "outdoor chair", "camping seat", "picnic", "tailgate", "portable seat", "director chair"])
def _(S):
    return [
        shell(rect(6.5, 2.5, 11, 8.5, rr(S, 3))),
        shell(rect(4.5, 12.25, 15, 3, rr(S, 1.5))),
        line(seg(4.5, 8.5, 4.5, 12.25)), line(seg(19.5, 8.5, 19.5, 12.25)),
        line(seg(6.5, 15.25, 17.5, 21.5)), line(seg(17.5, 15.25, 6.5, 21.5)),
    ]


@icon("camp-table", CAT, "Low folding table with a slatted top on X-shaped legs",
      tags=["folding table", "picnic table", "outdoor table", "camping", "cookout", "slatted", "portable table"])
def _(S):
    return [
        shell(rect(3, 7.5, 18, 4.5, rr(S, 2))),
        detail(seg(9, 7.5, 9, 12)), detail(seg(15, 7.5, 15, 12)),
        line(seg(6, 12, 18, 21)), line(seg(18, 12, 6, 21)),
    ]


@icon("lean-to", CAT, "Simple log shelter with one sloping roof and an open front",
      tags=["shelter", "bushcraft", "wilderness shelter", "survival", "debris hut", "forest camp", "roof"])
def _(S):
    return [
        shell(poly([(2.5, 12), (21.5, 4.5), (21.5, 8), (2.5, 15.5)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        line(seg(4.5, 14.5, 4.5, 21.5)), line(seg(19.5, 8, 19.5, 21.5)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("folding-saw", CAT, "Pocket saw with a toothed blade swung half open from its handle",
      tags=["pocket saw", "camp saw", "bushcraft", "cut branches", "wood", "hiking tool", "survival"])
def _(S):
    blade = [(0, -1.4), (12, -1.4), (12, 1), (11, 2.4), (10, 1), (9, 2.4), (8, 1), (7, 2.4), (6, 1), (5, 2.4), (4, 1), (3, 2.4), (2, 1), (0, 1)]
    pts = rotpts(blade, -48, ox=11, oy=15)
    return [
        shell(bar((11, 15), (4, 20), 4, r=S.r * 0.5)),
        shell(poly(pts, closed=True), stroke_miterlimit="2"),
    ]


@icon("ferro-rod", CAT, "Short ferrocerium fire starter with a handle, struck to throw sparks",
      tags=["fire starter", "flint", "firesteel", "spark", "bushcraft", "survival", "campfire"])
def _(S):
    return [
        shell(bar((3.5, 20.5), (9, 15), 4.5, r=S.r * 0.5)),
        line(seg(9, 15, 16, 8)),
        line(seg(18, 6.5, 21.5, 3)), line(seg(18.5, 9, 22, 9)),
        dot(16.5, 3.5, 1.1), dot(21, 12, 1),
    ]


@icon("matchbox", CAT, "Small matchbox with a sliding tray and a lit match beside it",
      tags=["matches", "lighter", "fire", "flame", "strike", "light a fire", "camping"])
def _(S):
    return [
        shell(rect(2.5, 11.5, 12.5, 10, rr(S, 2))),
        detail(seg(9, 11.5, 9, 21.5)),
        line(seg(19.5, 21.5, 19.5, 11)),
        solid(circle(19.5, 9.75, 1.6)),
        solid("M19.5 2.5C22 4.8 21.5 7 19.5 8C17.5 7 17 4.8 19.5 2.5Z"),
    ]


@icon("headlamp", CAT, "Head strap with a small lamp on the front throwing a fan of light rays",
      tags=["head torch", "headlight", "hands free light", "caving", "night hike", "camping light", "lamp"])
def _(S):
    return [
        line(seg(1.5, 11.5, 4.5, 11.5)),
        shell(rect(4.5, 6.5, 10, 10, rr(S, 3.5))),
        dot(9.5, 11.5, 2),
        line(seg(17.5, 8, 21.5, 5.5)), line(seg(17.5, 11.5, 22, 11.5)), line(seg(17.5, 15, 21.5, 17.5)),
    ]


@icon("insect-repellent", CAT, "Spray bottle with a bug on the label and a mist from the nozzle",
      tags=["bug spray", "mosquito spray", "deet", "pest", "outdoors", "camping", "repel insects"])
def _(S):
    return [
        shell(rect(3.5, 10, 10.5, 11.5, rr(S, 4))),
        shell(rect(6, 6.5, 5, 3.5, rr(S, 1))),
        shell(rect(5, 3, 8.5, 3.5, rr(S, 1.25))),
        dot(8.75, 16, 1.6),
        detail(seg(8.75, 16, 11.5, 13)), detail(seg(8.75, 16, 6, 19)),
        dot(16.5, 4.75, 1), dot(19.5, 3.5, 1), dot(18, 7.25, 1), dot(21, 6.5, 1), dot(19.5, 9.75, 1),
    ]


# ============================================================================ blades, signals and bear safety

@icon("multitool", CAT, "Folding pliers multitool opened with jaws at the top and handles spread",
      tags=["pliers", "swiss tool", "all in one tool", "camping tool", "utility tool", "edc"])
def _(S):
    return [
        shell(poly([(12, 2.5), (14.75, 6), (14.25, 11.5), (9.75, 11.5), (9.25, 6)], closed=True, r=S.r * 0.6)),
        detail(seg(12, 3.5, 12, 11)),
        shell(bar((10.6, 12.5), (6.3, 21), 3, r=S.r * 0.5)),
        shell(bar((13.4, 12.5), (17.7, 21), 3, r=S.r * 0.5)),
    ]


@icon("pocket-knife", CAT, "Folding pocket knife with a rounded handle, one blade opened and a tool slot",
      tags=["folding knife", "penknife", "jackknife", "swiss knife", "camping", "edc", "blade"])
def _(S):
    blade = [(0, -1.8), (8.5, -1.8), (11, 1.2), (0, 1.8)]
    pts = rotpts(blade, -55, ox=15, oy=14.5)
    return [
        shell(poly(pts, closed=True), stroke_miterlimit="2"),
        shell(rect(2.5, 14, 14, 7, rr(S, 3.5))),
        detail(seg(6, 17.5, 13, 17.5)),
    ]


@icon("sheath-knife", CAT, "Fixed-blade bushcraft knife standing beside its leather sheath",
      tags=["bushcraft knife", "hunting knife", "survival knife", "fixed blade", "camping", "belt knife", "scabbard"])
def _(S):
    return [
        shell(poly([(5.5, 13), (5.5, 3), (9.5, 7.5), (9.5, 13)], closed=True), stroke_miterlimit="2"),
        line(seg(4, 13.5, 11, 13.5)),
        shell(rect(5.75, 14.5, 3.5, 7, rr(S, 1.5))),
        shell(poly([(13.5, 6), (20.5, 6), (19.5, 16), (17, 21.5), (14.5, 16)], closed=True, r=S.r)),
        detail(seg(13.5, 10, 20.5, 10)),
    ]


@icon("machete", CAT, "Long broad slightly curved blade with a short handle, lying on the diagonal",
      tags=["cutlass", "jungle knife", "bush knife", "clearing", "blade", "cutting brush", "survival"])
def _(S):
    blade = [(0, -2), (8, -2.6), (14, -3.6), (19, -3.5), (14, 2.2), (8, 2.8), (0, 2)]
    pts = rotpts(blade, -40, ox=7.1, oy=17.6)
    return [
        shell(poly(pts, closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        shell(bar((2.5, 21.5), (7.1, 17.6), 3.4, r=S.r * 0.5)),
    ]


@icon("paracord", CAT, "Tight hank of cord wound round and round with two loose ends hanging out",
      tags=["rope", "cord", "survival cord", "550 cord", "string", "knots", "bracelet"])
def _(S):
    return [
        shell(rect(3.5, 6.5, 13.5, 10, rr(S, 4))),
        detail("M8 7.5Q7 11.5 8 15.5"), detail("M12.5 7.5Q11.5 11.5 12.5 15.5"),
        line("M17 12.5C20.5 12.5 20 17 22 18.5"),
        line("M15 16.5C16.5 19.5 16.5 21 19.5 21.5"),
    ]


@icon("signal-mirror", CAT, "Small square mirror with a sighting hole in the centre and light rays flashing off it",
      tags=["survival mirror", "heliograph", "rescue signal", "reflect light", "emergency", "sos", "wilderness"])
def _(S):
    return [
        shell(rect(3, 8.5, 11.5, 11.5, rr(S, 2.5))),
        dot(8.75, 14.25, 1.6),
        line(seg(17, 6.5, 20.5, 3)), line(seg(17.5, 10, 22, 9)), line(seg(14.5, 5, 14.5, 2)),
    ]


@icon("signal-flare", CAT, "Handheld flare stick with a burning tip, sparks flying off",
      tags=["flare", "distress flare", "emergency signal", "rescue", "road flare", "fire", "sos"])
def _(S):
    return [
        solid("M12 2C15.5 5 16 7.5 12 9.75C8 7.5 8.5 5 12 2Z"),
        shell(rect(9, 10, 6, 11.5, rr(S, 2.5))),
        detail(seg(9, 16.5, 15, 16.5)),
        dot(5.5, 5, 1), dot(18.5, 5.5, 1), dot(4.5, 9.5, 1), dot(19.5, 10, 1),
    ]


@icon("bear-canister", CAT, "Hard-sided food container with a twist lid and two ridges",
      tags=["bear can", "bear proof", "food storage", "backpacking", "wildlife safety", "campsite", "canister"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 4, rr(S, 1.75))),
        shell(rect(6, 6.5, 12, 15, rr(S, 3))),
        detail(seg(6, 12, 18, 12)), detail(seg(6, 16.5, 18, 16.5)),
    ]


@icon("bear-bell", CAT, "Small bell hanging from a clip with ring marks on both sides",
      tags=["hiking bell", "trail bell", "wildlife safety", "noise maker", "backpack bell", "camping", "alert"])
def _(S):
    return [
        line("M9.5 9V5a2.5 2.5 0 0 1 5 0V9"),
        shell("M5 18.5A7 9 0 0 1 19 18.5Z"),
        dot(12, 21, 1.3),
        line(arc(12, 14, 9.75, 163, 197)), line(arc(12, 14, 9.75, -17, 17)),
    ]
