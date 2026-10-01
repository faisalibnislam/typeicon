"""TypeIcon Core: hospitality (batch hospitality_001).

Front-of-house, housekeeping, room-service and fine-dining objects drawn from the things themselves.
Flat items are shown face-on, tools and cutlery from the front or side.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, polar  # noqa: F401

CAT = "hospitality"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def hole(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


# ============================================================================ front desk and arrival

@icon("hotel-key-rack", CAT, "Wall rack of pigeonhole cubbies with room keys hanging below",
      tags=["room keys", "reception", "front desk", "pigeonholes", "hotel", "key board"])
def _(S):
    k = L(S, 0.5, 1.5)
    return [
        shell(rect(3, 3, 18, 10, S.R)),
        detail(seg(9, 3, 9, 13)), detail(seg(15, 3, 15, 13)), detail(seg(3, 8, 21, 8)),
        line(seg(7, 13, 7, 16)), line(seg(17, 13, 17, 16)),
        shell(rect(5.5, 16, 3, 5, k)), shell(rect(15.5, 16, 3, 5, k)),
    ]


@icon("keycard-sleeve", CAT, "Paper key card wallet with a card poking out and a line for the room number",
      tags=["key card", "room key", "check in", "hotel", "wallet", "folder"])
def _(S):
    return [
        line(poly([(7, 10), (7, 3), (17, 3), (17, 10)], r=S.r)),
        shell(poly([(3, 10), (9, 10), (12, 12.5), (15, 10), (21, 10), (21, 21), (3, 21)], closed=True, r=S.r)),
        detail(seg(7, 17, 13, 17)),
    ]


@icon("guest-registration-card", CAT, "Registration card with form lines, a signature line and a pen across it",
      tags=["check in form", "guest card", "sign in", "registration", "hotel", "pen", "form"])
def _(S):
    return [
        shell(rect(3, 3, 13, 18, rr(S, 2))),
        detail(seg(6, 8, 13, 8)), detail(seg(6, 12, 13, 12)), detail(seg(6, 17, 10, 17)),
        shell(poly([(18, 8), (21, 11), (14.5, 18), (11.5, 19.5), (12.5, 16.5)], closed=True, r=S.r)),
    ]


@icon("late-checkout", CAT, "Door with a clock showing a late hour over its lower corner",
      tags=["check out", "extended stay", "departure", "hotel", "clock", "time", "door"])
def _(S):
    return [
        line(poly([(13, 8.5), (13, 3), (3, 3), (3, 21), (10, 21)], r=S.r)),
        dot(8, 12, 1.25),
        shell(circle(16, 15.5, 5.5)),
        detail(poly([(16, 12.5), (16, 15.5), (18.5, 17)], r=S.r)),
    ]


@icon("room-number-sign", CAT, "Door plaque showing a three digit room number",
      tags=["door number", "room sign", "plaque", "hotel", "101", "suite"])
def _(S):
    return [
        shell(rect(3, 5, 18, 14, rr(S, 3))),
        detail(seg(7, 9, 7, 15)),
        detail(ellipse(12, 12, 1.5, 3.5)),
        detail(seg(17, 9, 17, 15)),
    ]


@icon("room-direction-sign", CAT, "Two stacked corridor panels with arrows pointing opposite ways",
      tags=["wayfinding", "corridor", "hallway sign", "hotel", "this way", "arrow signs"])
def _(S):
    return [
        shell(poly([(3, 3), (17, 3), (21, 6.5), (17, 10), (3, 10)], closed=True, r=S.r)),
        shell(poly([(21, 14), (7, 14), (3, 17.5), (7, 21), (21, 21)], closed=True, r=S.r)),
        detail(seg(6, 6.5, 12, 6.5)), detail(seg(12, 17.5, 18, 17.5)),
    ]


@icon("key-card-encoder", CAT, "Desktop card encoder with a key card half inserted and an indicator light",
      tags=["key card", "encoder", "reception", "hotel", "issue key", "card writer"])
def _(S):
    return [
        line(poly([(9, 12), (8, 4.5), (16, 3), (17.5, 12)], r=S.r)),
        shell(rect(3, 12, 18, 9, rr(S, 2))),
        dot(17, 16.5, 1.25),
        detail(seg(6, 16.5, 12, 16.5)),
    ]


@icon("valet-ticket", CAT, "Claim ticket with a string loop, a tear-off stub and a car on the stub",
      tags=["valet parking", "claim check", "car park", "parking stub", "hotel", "ticket"])
def _(S):
    return [
        line("M10 6V4.5a2 2 0 0 1 4 0V6"),
        shell(rect(5, 6, 14, 15, rr(S, 2))),
        detail("M6 11h2M10 11h2M14 11h2M18 11h1"),
        hole(poly([(7.5, 17.5), (7.5, 16), (9.5, 16), (10.5, 14), (13.5, 14), (14.5, 16), (16.5, 16), (16.5, 17.5)], closed=True)),
        dot(9.5, 18, 1), dot(14.5, 18, 1),
    ]


@icon("valet-podium", CAT, "Narrow podium with a car key on its front face",
      tags=["valet stand", "parking attendant", "key cabinet", "hotel entrance", "lectern", "podium"])
def _(S):
    return [
        shell(poly([(2.5, 3), (21.5, 3), (21.5, 7), (2.5, 7)], closed=True, r=S.r * 0.5)),
        shell(poly([(5.5, 7), (18.5, 7), (17.5, 21), (6.5, 21)], closed=True, r=S.r * 0.5)),
        dot(12, 12, 1.8),
        detail(seg(12, 13.5, 12, 18.5)), detail(seg(12, 16.5, 14.5, 16.5)),
    ]


@icon("hotel-entrance-canopy", CAT, "Building entrance with a flat canopy on two poles over the doors",
      tags=["porte cochere", "entrance", "front door", "hotel", "awning", "arrival", "lobby"])
def _(S):
    return [
        shell(rect(2, 3, 20, 4, rr(S, 1.5))),
        line(seg(5, 7, 5, 21)), line(seg(19, 7, 19, 21)),
        shell(rect(8.5, 11, 7, 10, rr(S, 1))),
        detail(seg(12, 11, 12, 21)),
    ]


@icon("safe-deposit-boxes", CAT, "Grid of small numbered locker doors, each with a keyhole",
      tags=["lockers", "vault", "secure storage", "bank", "hotel safe", "keyhole", "valuables"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, S.R)),
             detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
             detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15))]
    for cx in (6, 12, 18):
        for cy in (6, 12, 18):
            parts.append(dot(cx, cy, 1))
    return parts


@icon("guest-directory", CAT, "Closed guest information binder with a bell emblem and a ribbon bookmark",
      tags=["hotel info", "service directory", "binder", "guest book", "bell", "room folder"])
def _(S):
    return [
        shell(rect(5, 3, 14, 15, S.R)),
        detail(seg(8.5, 3, 8.5, 18)),
        hole("M11 14.5Q11 9.5 13.75 9.5Q16.5 9.5 16.5 14.5Z"),
        solid(poly([(14, 18), (17.5, 18), (17.5, 22), (15.75, 20.5), (14, 22)], closed=True)),
    ]


@icon("hotel-stationery", CAT, "Notepad with a crest mark and a pen beside it",
      tags=["notepad", "letterhead", "writing set", "hotel room", "pen", "memo pad"])
def _(S):
    return [
        shell(rect(3, 5, 11, 16, rr(S, 2))),
        dot(8.5, 10, 1.5),
        detail(seg(6, 15, 11, 15)),
        shell(poly([(17.5, 4), (21, 4), (21, 16), (19.25, 19.5), (17.5, 16)], closed=True, r=S.r)),
    ]


@icon("comment-card", CAT, "Folded table card with text lines and a row of five rating dots",
      tags=["feedback card", "guest survey", "rating", "review", "restaurant", "tent card"])
def _(S):
    parts = [
        shell(poly([(3, 21), (5, 4), (19, 4), (21, 21)], closed=True, r=S.r)),
        detail(seg(8.5, 8, 15.5, 8)), detail(seg(8.5, 11.5, 13, 11.5)),
    ]
    for i in range(5):
        parts.append(dot(6.5 + i * 2.75, 16.5, 0.9))
    return parts


@icon("lost-and-found", CAT, "Open box with an umbrella tip and a glove poking out of the top",
      tags=["lost property", "left behind", "missing items", "hotel", "box", "umbrella", "glove"])
def _(S):
    return [
        shell(poly([(7, 2.5), (10, 10), (4, 10)], closed=True, r=S.r)),
        line("M15 10V6a2 2 0 0 1 4 0V10"),
        shell(poly([(3, 10), (21, 10), (19, 21), (5, 21)], closed=True, r=S.r)),
        detail(seg(9, 15.5, 15, 15.5)),
    ]

# ============================================================================ guest services and room amenities

@icon("umbrella-bag-stand", CAT, "Stand with a dispenser of plastic sleeves and a wet umbrella in a sleeve",
      tags=["wet umbrella", "plastic sleeve", "lobby", "rainy day", "dispenser", "hotel entrance"])
def _(S):
    return [
        shell(rect(2.5, 3, 10, 6, rr(S, 2))),
        detail(seg(5, 6, 10, 6)),
        line(seg(7.5, 9, 7.5, 21)), line(seg(3.5, 21, 11.5, 21)),
        shell(rect(15, 4, 5, 13, rr(S, 2))),
        line("M17.5 17V19a1.5 1.5 0 0 1 -3 0"),
    ]


@icon("taxi-whistle", CAT, "Metal whistle with three short sound lines above it",
      tags=["doorman", "call a cab", "taxi", "hotel entrance", "signal", "referee", "sound"])
def _(S):
    body = union(rect(2.5, 12.5, 8, 5, 1), circle(15, 15, 5.5))
    return [
        shell(body),
        dot(15, 15, 1.4),
        line(seg(15, 3, 15, 6)), line(seg(10, 4.5, 11.5, 7)), line(seg(20, 4.5, 18.5, 7)),
    ]


@icon("wifi-voucher", CAT, "Printed ticket slip with a wifi symbol and two code lines",
      tags=["internet access", "wifi code", "guest wifi", "password slip", "hotel", "network", "receipt"])
def _(S):
    return [
        shell(rect(4, 2, 16, 20, rr(S, 2))),
        detail("M8.5 8.6a5 5 0 0 1 7 0"),
        detail("M10.4 10.8a2.2 2.2 0 0 1 3.2 0"),
        dot(12, 12.2, 0.9),
        detail(seg(8, 15.5, 16, 15.5)), detail(seg(8, 18.5, 13, 18.5)),
    ]


@icon("evacuation-map", CAT, "Framed floor plan with a you are here dot and a dashed route to an exit",
      tags=["fire exit plan", "emergency route", "escape plan", "floor plan", "safety", "you are here"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 2))),
        dot(7.5, 16.5, 1.5),
        detail(poly([(7.5, 13.5), (7.5, 8.5), (13, 8.5)], r=S.r * 0.5)),
        hole(rect(15.5, 6, 3.5, 6, 0.5)),
    ]


@icon("room-status-panel", CAT, "Wall panel with a doorbell button and two status lamps",
      tags=["do not disturb", "make up room", "doorbell", "hotel door", "status light", "housekeeping"])
def _(S):
    return [
        shell(rect(4, 2, 16, 20, S.R)),
        detail(circle(12, 7.5, 2.5)),
        detail(circle(8.5, 16, 2)),
        dot(15.5, 16, 2),
    ]


@icon("hospitality-tray", CAT, "Room tray with a kettle and a cup",
      tags=["tea tray", "coffee tray", "kettle", "in room", "refreshments", "hotel room", "cup"])
def _(S):
    return [
        shell(poly([(3, 9), (10, 9), (10.5, 17), (2.5, 17)], closed=True, r=S.r)),
        line("M10 11.5h2.5a1.5 1.5 0 0 1 0 4H10.5"),
        line(seg(3, 6, 10, 6)),
        shell(poly([(14, 12), (21, 12), (20, 17), (15, 17)], closed=True, r=S.r)),
        shell(rect(2, 18.5, 20, 3, rr(S, 1.5))),
    ]


@icon("toiletry-set", CAT, "Three miniature bottles of different heights on a small tray",
      tags=["amenities", "shampoo", "bath products", "hotel bathroom", "mini bottles", "guest supplies"])
def _(S):
    k = L(S, 0.3, 1.5)
    return [
        shell(rect(3, 11, 4, 8, k)), solid(rect(4, 7.5, 2, 3)),
        shell(rect(10, 6.5, 4, 12.5, k)), solid(rect(11, 2.5, 2, 3)),
        shell(rect(17, 13, 4, 6, k)), solid(rect(18, 10, 2, 2)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("wrapped-soap", CAT, "Bar of soap in a paper wrapper with a band and a leaf mark",
      tags=["hotel soap", "bathroom amenity", "bar soap", "hygiene", "wrapped", "guest supplies"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 19, 11, S.R)),
        detail(seg(8.5, 6.5, 8.5, 17.5)), detail(seg(15.5, 6.5, 15.5, 17.5)),
        hole("M12 15Q9.8 12 12 9Q14.2 12 12 15Z"),
    ]


@icon("cotton-ball-jar", CAT, "Glass jar with a round lid filled with cotton balls",
      tags=["cotton pads", "bathroom", "makeup removal", "apothecary jar", "hotel amenity", "cotton wool"])
def _(S):
    return [
        shell(rect(6, 3.5, 12, 3.5, rr(S, 1.5))),
        shell(poly([(5, 7), (5, 21), (19, 21), (19, 7)], r=S.r)),
        dot(9.5, 17, 1.4), dot(14.5, 17, 1.4), dot(12, 13, 1.4),
    ]


@icon("dental-kit", CAT, "Toothbrush and toothpaste tube standing in a small pouch",
      tags=["toothbrush", "toothpaste", "amenity kit", "hotel bathroom", "oral care", "travel kit"])
def _(S):
    return [
        shell(rect(5, 2.5, 3.5, 5, rr(S, 1))),
        line(seg(6.75, 7.5, 6.75, 13)),
        solid(rect(14, 3, 3, 2)),
        shell(poly([(12.5, 5), (18.5, 5), (17.5, 13), (13.5, 13)], closed=True, r=S.r * 0.5)),
        shell(rect(3, 12.5, 18, 8.5, S.R)),
        detail(seg(7, 16.8, 17, 16.8)),
    ]


@icon("shaving-kit", CAT, "Disposable razor and a can of shaving foam in a small pouch",
      tags=["razor", "shaving cream", "amenity kit", "grooming", "hotel bathroom", "travel kit"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 5, 3, rr(S, 1))),
        line(seg(7, 5.5, 7, 13)),
        solid(rect(14.5, 2.5, 3, 2)),
        shell(rect(13, 4.5, 6, 8.5, rr(S, 2))),
        shell(rect(3, 12.5, 18, 8.5, S.R)),
        detail(seg(7, 16.8, 17, 16.8)),
    ]


@icon("bathtub-caddy", CAT, "Bathtub with a tray across its rim holding a book and a candle",
      tags=["bath tray", "spa", "relaxing bath", "hotel bathroom", "candle", "book", "soak"])
def _(S):
    return [
        shell(rect(4, 9, 16, 3, rr(S, 1.5))),
        shell(rect(6, 2.5, 5, 6, rr(S, 1))),
        shell(rect(14, 6, 4, 3, 0.5)),
        dot(16, 3.8, 1),
        shell(poly([(2, 13), (22, 13), (19.5, 20), (4.5, 20)], closed=True, r=S.r)),
    ]


@icon("toilet-paper-fold", CAT, "Toilet paper roll with the loose end folded to a neat point",
      tags=["housekeeping", "bathroom", "tissue roll", "fresh", "hotel service", "folded point"])
def _(S):
    return [
        shell(rect(3, 3, 18, 9, S.R)),
        detail(seg(7, 3, 7, 12)),
        shell(poly([(8, 12), (16, 12), (16, 18.5), (12, 22), (8, 18.5)], closed=True, r=S.r)),
    ]


@icon("sanitized-seat-band", CAT, "Toilet seen from above with a paper strip wrapped across the closed seat",
      tags=["sanitized", "hygiene band", "cleaned toilet", "hotel bathroom", "restroom", "housekeeping"])
def _(S):
    lid = path_to_d(D(P(ellipse(12, 14, 7.5, 7.5)), P(rect(0, 11, 24, 6))))
    return [
        shell(rect(6, 2, 12, 4, L(S, 0.5, 2))),
        shell(lid),
        shell(rect(2.5, 11.5, 19, 5, L(S, 0.5, 2.5))),
    ]


@icon("sanitized-glass-cap", CAT, "Drinking tumbler with a pleated paper cap over its rim",
      tags=["sanitised", "clean glass", "hotel room", "tumbler", "paper cover", "hygiene"])
def _(S):
    return [
        shell(poly([(7.5, 10), (8.5, 21), (15.5, 21), (16.5, 10)], r=S.r * 0.5)),
        shell(poly([(4, 10), (20, 10), (17, 3.5), (7, 3.5)], closed=True, r=S.r)),
        detail(seg(10, 4, 10, 10)), detail(seg(14, 4, 14, 10)),
    ]


# ============================================================================ housekeeping, rooms and views

@icon("miniature-liquor-bottle", CAT, "Tiny flat-sided spirits bottle with a screw cap next to a coin",
      tags=["minibar", "mini bottle", "airline bottle", "spirits", "hotel room", "small bottle", "nip"])
def _(S):
    return [
        shell(rect(9, 2.5, 3.5, 3, 0.5)),
        shell(poly([(7.5, 10), (7.5, 21), (14, 21), (14, 10), (12, 6.5), (9.5, 6.5)], closed=True, r=S.r)),
        detail(seg(7.5, 15.5, 14, 15.5)),
        shell(circle(19, 17.5, 2.5)),
    ]


@icon("dry-cleaning-bag", CAT, "Hanger under a clear plastic cover over a shirt, tied at the bottom",
      tags=["laundry service", "garment bag", "valet", "pressed shirt", "hotel laundry", "plastic cover"])
def _(S):
    return [
        line("M12 8V5.5a1.8 1.8 0 1 0 -1.8 -1.8"),
        shell(poly([(12, 8), (20, 11.5), (19, 20), (5, 20), (4, 11.5)], closed=True, r=S.r)),
        detail(poly([(9, 11.5), (12, 14.5), (15, 11.5)], r=S.r)),
        line(seg(12, 20, 12, 22)),
    ]


@icon("anti-theft-hanger", CAT, "Hook-less clothes hanger with a ring at the top threaded on a short rail stud",
      tags=["wardrobe", "closet", "hotel room", "security hanger", "coat hanger", "ring hanger"])
def _(S):
    return [
        line(seg(8, 2.5, 16, 2.5)),
        shell(circle(12, 6.5, 2.2)),
        shell(poly([(2.5, 19), (12, 10.5), (21.5, 19)], closed=True, r=S.r)),
    ]


@icon("linen-cart", CAT, "Wheeled bin with folded sheets piled above its rim",
      tags=["housekeeping cart", "laundry", "sheets", "hotel", "trolley", "towels", "maid cart"])
def _(S):
    return [
        shell(rect(5, 3.5, 14, 6, rr(S, 2))),
        detail(seg(5, 6.5, 19, 6.5)),
        shell(poly([(4, 10), (20, 10), (18.5, 19), (5.5, 19)], closed=True, r=S.r)),
        dot(7.5, 21.3, 1.1), dot(16.5, 21.3, 1.1),
    ]


@icon("linen-chute", CAT, "Wall hatch with a flap tilted open and linen dropping into the opening",
      tags=["laundry chute", "hotel", "dirty linen", "service hatch", "housekeeping", "drop"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        hole(rect(7, 6.5, 10, 3.5, 1)),
        shell(poly([(7, 11), (17, 11), (18.5, 16.5), (5.5, 16.5)], closed=True, r=S.r)),
    ]


@icon("bed-making", CAT, "Bed with a sheet billowing in the air above the mattress",
      tags=["housekeeping", "fresh sheets", "make the bed", "hotel room", "linen", "turn down"])
def _(S):
    return [
        shell("M3.5 6C6.5 2 9 8 12 5S17.5 2.5 20.5 6V10C17.5 6.5 15 12 12 9S6.5 6 3.5 10Z"),
        shell(rect(3, 14, 18, 4, rr(S, 1.5))),
        line(seg(5, 18, 5, 21)), line(seg(19, 18, 19, 21)),
    ]


@icon("bed-runner", CAT, "Made bed seen from the foot with a wide contrasting band across its lower part",
      tags=["bed scarf", "bed throw", "hotel room", "made bed", "linen", "decor"])
def _(S):
    return [
        shell(rect(5, 3.5, 6, 4, L(S, 0.5, 2))), shell(rect(13, 3.5, 6, 4, L(S, 0.5, 2))),
        shell(rect(3, 10, 18, 10, S.R)),
        hole(rect(3.5, 14, 17, 3.5)),
    ]


@icon("pillow-menu", CAT, "Upright card menu showing three differently shaped pillows",
      tags=["pillow choice", "hotel room", "bedding options", "sleep", "guest comfort", "menu card"])
def _(S):
    return [
        shell(rect(5, 2, 14, 20, S.R)),
        hole(rect(7.5, 5.5, 9, 3, 1.5)),
        hole(rect(9, 10.5, 6, 4, 2)),
        hole(ellipse(12, 18.5, 3.5, 1.7)),
    ]


@icon("sea-view", CAT, "Window frame showing a low sun and two wavy water lines",
      tags=["ocean view", "sea", "beach", "room view", "hotel room", "waves", "seaside"])
def _(S):
    return [
        shell(rect(3, 2, 18, 16, S.R)), line(seg(2, 21, 22, 21)),
        dot(15.5, 6.5, 2),
        detail("M5.5 11q1.75-2 3.5 0t3.5 0t3.5 0t3.5 0"),
        detail("M5.5 14.7q1.75-2 3.5 0t3.5 0t3.5 0t3.5 0"),
    ]


@icon("city-view", CAT, "Window frame showing a skyline of buildings of different heights",
      tags=["skyline", "urban", "room view", "hotel room", "downtown", "high rise", "cityscape"])
def _(S):
    return [
        shell(rect(3, 2, 18, 16, S.R)), line(seg(2, 21, 22, 21)),
        detail(poly([(6, 18), (6, 11), (9, 11), (9, 6), (13, 6), (13, 13), (16, 13), (16, 9), (18, 9), (18, 18)])),
    ]


@icon("mountain-view", CAT, "Window frame showing two overlapping peaks, the taller with a snow cap",
      tags=["mountains", "alpine", "scenic", "room view", "hotel room", "peaks", "landscape"])
def _(S):
    return [
        shell(rect(3, 2, 18, 16, S.R)), line(seg(2, 21, 22, 21)),
        detail(poly([(5, 16), (10, 6.5), (14, 12.5), (16.5, 10), (19, 16)], r=S.r)),
    ]


@icon("garden-view", CAT, "Window frame showing a round-topped tree and a low hedge",
      tags=["garden", "park", "greenery", "room view", "hotel room", "tree", "landscape"])
def _(S):
    return [
        shell(rect(3, 2, 18, 16, S.R)), line(seg(2, 21, 22, 21)),
        detail(circle(9.5, 7.5, 3.2)),
        detail(seg(9.5, 10.7, 9.5, 18)),
        hole(rect(13.5, 12, 5, 4, 2)),
    ]


@icon("door-newspaper", CAT, "Cloth bag hanging from a door handle with a rolled newspaper in it",
      tags=["morning paper", "doorknob bag", "delivery", "hotel room", "news", "daily paper"])
def _(S):
    return [
        line("M6.5 9V6.5a2.5 2.5 0 0 1 5 0V9"),
        shell(poly([(14, 9.5), (17.5, 2.5), (20.5, 4), (17, 11)], closed=True, r=S.r * 0.5)),
        shell(poly([(4, 9), (20, 9), (18.5, 21), (5.5, 21)], closed=True, r=S.r)),
        detail(seg(9, 14, 15, 14)),
    ]


@icon("welcome-drink", CAT, "Tall glass with a straw and a flower garnish on a small tray",
      tags=["cocktail", "arrival drink", "greeting", "hotel", "resort", "punch", "straw"])
def _(S):
    return [
        shell(poly([(7, 8), (17, 8), (15.5, 18), (8.5, 18)], closed=True, r=S.r * 0.5)),
        line(seg(13, 14, 16, 3)),
        shell(circle(8, 5.5, 2.2)),
        line(seg(3, 20.5, 21, 20.5)),
    ]


@icon("tray-jack", CAT, "Folding X-shaped stand holding a serving tray",
      tags=["tray stand", "room service", "butler stand", "folding stand", "serving", "luggage rack"])
def _(S):
    return [
        shell(rect(3, 3, 18, 4, rr(S, 1.5))),
        line(seg(6, 11, 18, 11)),
        line(seg(6, 11, 18, 21)), line(seg(18, 11, 6, 21)),
    ]


# ============================================================================ restaurant service

@icon("sunbed-service-flag", CAT, "Sun lounger in side view with a small flag raised on a pole at its arm",
      tags=["pool service", "call waiter", "beach club", "resort", "lounger", "flag", "sunbed"])
def _(S):
    return [
        shell(poly([(3, 8), (5.5, 6.5), (10, 13), (21, 13), (21, 17), (8.5, 17)], closed=True, r=S.r)),
        line(seg(7, 17, 7, 21)), line(seg(19, 17, 19, 21)),
        line(seg(16, 13, 16, 3)),
        shell(poly([(16, 3), (21, 5.5), (16, 8)], closed=True, r=S.r)),
    ]


@icon("event-wristband", CAT, "Fabric wristband loop with a small plastic locking bead at the join",
      tags=["entry band", "festival", "resort band", "all inclusive", "access band", "bracelet", "ticket"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 15, L(S, 5, 7.5))),
        detail(rect(7.5, 9, 9, 6, L(S, 2, 3))),
        hole(rect(9.5, 15.5, 5, 3.2, L(S, 0, 1.4))),
    ]


@icon("drink-token", CAT, "Round token with a cocktail glass cut through its centre",
      tags=["drink ticket", "bar chip", "coupon", "event", "cocktail", "free drink", "coin"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        hole(poly([(7.5, 7), (16.5, 7), (12, 13)], closed=True, r=S.r * 0.5)),
        hole(rect(11, 12.5, 2, 5.5)),
        hole(rect(8.5, 17.5, 7, 1.3)),
    ]


@icon("crumb-scraper", CAT, "Slim curved metal blade with a handle sweeping crumbs across a table",
      tags=["table crumber", "restaurant", "fine dining", "clean table", "waiter tool", "crumbs"])
def _(S):
    return [
        shell("M3 15C3.5 10 8 6.5 14 6.5V10C10.5 10.5 8 12 7 15Z"),
        shell(rect(14, 5.5, 7, 5, L(S, 0.3, 2.5))),
        dot(9, 19.5, 1), dot(13, 18.5, 1), dot(17, 19.5, 1),
    ]


@icon("silent-butler", CAT, "Lidded crumb pan on a long handle with the hinged lid tilted open",
      tags=["crumb pan", "ashtray", "table service", "restaurant", "dustpan", "fine dining"])
def _(S):
    return [
        shell("M3.5 13.5C3.5 9 6 5.5 10.5 6L13.5 13.5Z"),
        shell(rect(3, 14, 12, 6, S.R)),
        shell(rect(15, 15.5, 7, 3, 1.5)),
        dot(7, 17, 0.8), dot(11, 17, 0.8),
    ]


@icon("order-pad", CAT, "Spiral-top notepad with scribbled lines and a pencil tucked beside it",
      tags=["waiter pad", "take order", "notes", "restaurant", "notebook", "server", "pencil"])
def _(S):
    return [
        shell(rect(4, 5, 13, 16, rr(S, 2))),
        line(seg(7, 3, 7, 6.5)), line(seg(10.5, 3, 10.5, 6.5)), line(seg(14, 3, 14, 6.5)),
        detail(seg(7, 11, 14, 11)), detail(seg(7, 15, 12, 15)),
        line(seg(20.5, 5, 17.5, 19)),
    ]


@icon("tip-jar", CAT, "Glass jar with coins inside and a folded banknote sticking out of the mouth",
      tags=["gratuity", "tips", "donation", "cash", "restaurant", "coins", "cafe"])
def _(S):
    return [
        shell(rect(8.5, 2.5, 7, 6.5, rr(S, 1))),
        line(poly([(5, 8), (5, 21), (19, 21), (19, 8)], r=S.r)),
        line(seg(5, 8, 8, 8)), line(seg(16, 8, 19, 8)),
        dot(9.5, 17.5, 1.7), dot(14.5, 17.5, 1.7), dot(12, 13.5, 1.7),
    ]


@icon("carrying-plates", CAT, "Raised forearm balancing a stack of three plates",
      tags=["waiter", "server", "restaurant", "dishes", "serving", "banquet", "tray hand"])
def _(S):
    return [
        line(seg(8, 3.5, 20, 3.5)), line(seg(8, 7, 20, 7)), line(seg(8, 10.5, 20, 10.5)),
        shell(poly([(2.5, 21), (3.5, 15), (9, 13.5), (14, 13.5), (17, 15.5), (13, 17.5), (9, 17.5), (8, 21)], closed=True, r=S.r)),
    ]


@icon("wine-presentation", CAT, "Wine bottle held on its side with the label facing out over a folded napkin",
      tags=["sommelier", "wine service", "show label", "restaurant", "bottle", "fine dining"])
def _(S):
    return [
        shell(poly([(2.5, 9), (8, 9), (10, 7), (21.5, 7), (21.5, 14), (10, 14), (8, 12), (2.5, 12)], closed=True, r=S.r)),
        hole(rect(12.5, 8.5, 5, 3, 0.5)),
        shell(poly([(7, 16), (20, 16), (18, 21), (9, 21)], closed=True, r=S.r)),
    ]


@icon("wine-list", CAT, "Tall narrow menu cover with a wine bottle embossed on the front",
      tags=["wine menu", "sommelier", "drinks menu", "restaurant", "bottle", "cellar list"])
def _(S):
    return [
        shell(rect(5, 2, 14, 20, S.R)),
        detail(seg(8.5, 2, 8.5, 22)),
        hole(poly([(13.5, 5.5), (15.5, 5.5), (15.5, 10), (17, 12), (17, 19), (12, 19), (12, 12), (13.5, 10)], closed=True, r=S.r * 0.4)),
    ]


@icon("kids-menu", CAT, "Menu card with a smiley face and two crossed crayons below",
      tags=["children", "kids", "family restaurant", "colouring menu", "coloring", "crayons", "smiley"])
def _(S):
    return [
        shell(rect(4, 2, 16, 20, S.R)),
        detail(circle(12, 8, 3.2)),
        dot(10.9, 7.5, 0.7), dot(13.1, 7.5, 0.7),
        line(seg(7, 20, 10.5, 14.5)), line(seg(13.5, 20, 17, 14.5)),
    ]


@icon("qr-menu", CAT, "Standing table card with a square QR code pattern on its face",
      tags=["digital menu", "scan to order", "contactless", "restaurant", "table card", "barcode", "tent card"])
def _(S):
    return [
        shell(rect(3, 2, 18, 16, S.R)),
        hole(rect(6, 5, 4, 4, 0.5)), hole(rect(14, 5, 4, 4, 0.5)), hole(rect(6, 11, 4, 4, 0.5)),
        hole(rect(13, 11.5, 2, 2)), hole(rect(16, 14, 2, 2)),
        line(seg(7, 18, 7, 21)), line(seg(17, 18, 17, 21)),
    ]


@icon("glass-polishing", CAT, "Wine glass with a cloth wrapped round its bowl and small sparkle marks",
      tags=["polish", "clean glassware", "restaurant", "stemware", "sparkle", "fine dining", "wine glass"])
def _(S):
    return [
        shell(poly([(7, 3), (17, 3), (17, 9), (15.5, 12), (12, 13.5), (8.5, 12), (7, 9)], closed=True, r=S.r)),
        detail("M7.5 7q1.5-1.5 3 0t3 0t3 0"),
        line(seg(12, 13.5, 12, 19.5)), line(seg(8, 20.5, 16, 20.5)),
        line(seg(20.5, 3, 20.5, 7)), line(seg(18.5, 5, 22.5, 5)),
    ]


@icon("table-call-button", CAT, "Small table unit with a large push dome and signal arcs above it",
      tags=["call waiter", "service bell", "request service", "restaurant", "buzzer", "wireless", "hospitality"])
def _(S):
    return [
        shell(rect(4, 15, 16, 6, S.R)),
        shell("M6.5 15a5.5 5.5 0 0 1 11 0Z"),
        line("M9.4 6.2a3.6 3.6 0 0 1 5.2 0"),
        line("M6.7 4a7 7 0 0 1 10.6 0"),
    ]


@icon("rolled-hot-towel", CAT, "Rolled white towel lying in a narrow tray with steam rising",
      tags=["oshibori", "hot towel", "refreshing towel", "restaurant", "spa", "steam", "hand towel"])
def _(S):
    return [
        line("M8 2q-1.5 1.5 0 3t0 3"), line("M12 2q-1.5 1.5 0 3t0 3"), line("M16 2q-1.5 1.5 0 3t0 3"),
        shell(rect(5, 10, 14, 6, S.R)),
        dot(8.5, 13, 1.2),
        shell(rect(2.5, 16.5, 19, 4, rr(S, 1.5))),
    ]


# ============================================================================ tableware and cutlery

def rot(pts, deg=45.0, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rrect(x, y, w, h, deg=45.0, r=0.0):
    return poly(rot([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], deg), closed=True, r=r)


def rpoly(pts, deg=45.0, closed=True, r=0.0):
    return poly(rot(pts, deg), closed=closed, r=r)


@icon("chopstick-sleeve", CAT, "Pair of chopsticks slid halfway into a slim paper sleeve",
      tags=["chopsticks", "asian restaurant", "takeout", "wrapper", "cutlery", "sushi", "paper sleeve"])
def _(S):
    return [
        line(seg(9, 10, 11.5, 2.5)), line(seg(13, 10, 15.5, 2.5)),
        shell(rect(6.5, 10, 11, 11.5, S.R)),
        detail(seg(6.5, 15.5, 17.5, 15.5)),
    ]


@icon("rolled-silverware", CAT, "Napkin rolled round a fork, knife and spoon with a paper band, handles showing",
      tags=["napkin roll", "cutlery set", "banquet", "catering", "restaurant", "table setting", "silverware"])
def _(S):
    return [
        shell(rect(2.5, 8.5, 15, 10, S.R)),
        detail(seg(10, 8.5, 10, 18.5)),
        line(seg(17.5, 11, 21.5, 9)), line(seg(17.5, 13.5, 21.5, 13.5)), line(seg(17.5, 16, 21.5, 18)),
    ]


@icon("charger-plate", CAT, "Large plate with a beaded rim and a smaller dinner plate on top",
      tags=["service plate", "place setting", "underplate", "fine dining", "table setting", "dinnerware", "banquet"])
def _(S):
    parts = [shell(circle(12, 12, 9.5)), shell(circle(12, 12, 4.8))]
    for i in range(10):
        x, y = polar(12, 12, 7.1, i * 36)
        parts.append(hole(rect(x - 0.9, y - 0.9, 1.8, 1.8, L(S, 0, 0.9))))
    return parts


@icon("bread-plate", CAT, "Small side plate with a bread roll on it and a butter knife across the top",
      tags=["side plate", "butter knife", "roll", "restaurant", "table setting", "bread and butter", "bakery"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 6, 3, L(S, 0.5, 1.5))),
        line(seg(8.5, 5, 21.5, 5)),
        shell("M7.5 15C7.5 9.5 16.5 9.5 16.5 15Z"),
        shell(poly([(2.5, 15), (21.5, 15), (19.5, 19.5), (4.5, 19.5)], closed=True, r=S.r)),
    ]


@icon("fish-knife", CAT, "Fish knife with a wide flat unserrated blade and a pointed tip",
      tags=["fish", "seafood", "cutlery", "table setting", "silverware", "fine dining", "flatware"])
def _(S):
    return [
        shell(rpoly([(9, 13), (9, 3), (12, 5.5), (15.5, 9.5), (15.5, 13)], r=S.r)),
        shell(rrect(10, 13, 3.5, 8.5, r=L(S, 0, 1.2))),
    ]


@icon("steak-knife", CAT, "Steak knife with a pointed serrated blade and a thick riveted handle",
      tags=["serrated knife", "meat", "cutlery", "table setting", "silverware", "restaurant", "flatware"])
def _(S):
    blade = [(14.5, 13), (14.5, 5.5), (13.5, 3), (10.8, 6), (12, 6.8), (10, 10), (11.2, 10.8), (9.5, 13)]
    return [
        shell(rpoly(blade, r=S.r * 0.4), stroke_miterlimit="3"),
        shell(rrect(9.5, 13, 5, 8.5, r=L(S, 0.5, 2))),
        hole(poly(rot([(12, 15.8), (12.01, 15.8)]), closed=False)) if False else dot(*rot([(12, 16)])[0], 0.8),
        dot(*rot([(12, 19)])[0], 0.8),
    ]


@icon("cake-fork", CAT, "Small pastry fork with three tines, the left tine wider and flattened",
      tags=["pastry fork", "dessert fork", "cake", "cutlery", "table setting", "silverware", "flatware"])
def _(S):
    return [
        shell(rrect(6.2, 2.5, 3, 6.5, r=L(S, 0, 1))),
        line(rpoly([(12.2, 2.5), (12.2, 10)], closed=False)), line(rpoly([(15.7, 2.5), (15.7, 10)], closed=False)),
        line(rpoly([(7.7, 10), (15.7, 10)], closed=False)),
        line(rpoly([(11.7, 10), (11.7, 21)], closed=False)),
    ]


@icon("oyster-fork", CAT, "Short slim three-tined fork beside an open oyster shell",
      tags=["seafood fork", "shellfish", "cocktail fork", "raw bar", "cutlery", "restaurant", "oyster"])
def _(S):
    return [
        line(seg(3.5, 3, 3.5, 8.5)), line(seg(6.5, 3, 6.5, 8.5)), line(seg(9.5, 3, 9.5, 8.5)),
        line(poly([(3.5, 8), (3.5, 9.5), (6.5, 11), (9.5, 9.5), (9.5, 8)], r=S.r)),
        line(seg(6.5, 11, 6.5, 21)),
        shell("M16.5 21C11.5 21 11 14.5 13 10.5C14.5 7.5 19.5 7.5 20.5 12C21.5 17 20 21 16.5 21Z"),
        detail("M16.5 18.5Q15.5 14 16.8 11.5"),
    ]


@icon("fondue-fork", CAT, "Two long two-pronged forks crossed, each with a round coloured tip on its handle",
      tags=["fondue", "cheese fondue", "chocolate fondue", "skewer", "dipping", "swiss", "long fork"])
def _(S):
    def fork(deg):
        d = "M10.2 2.5V5a1.8 1.8 0 0 0 3.6 0V2.5M12 6.8V19.5"
        return d
    parts = []
    for deg in (-32, 32):
        pts_h = rot([(12, 6.8), (12, 19.5)], deg)
        parts.append(line(seg(pts_h[0][0], pts_h[0][1], pts_h[1][0], pts_h[1][1])))
        a = rot([(10.2, 2.5), (10.2, 5.5)], deg)
        b = rot([(13.8, 2.5), (13.8, 5.5)], deg)
        parts.append(line(poly([a[0], a[1], b[1], b[0]], r=S.r * 0.7)))
        t = rot([(12, 20.8)], deg)[0]
        parts.append(dot(t[0], t[1], 1.4))
    return parts


@icon("snail-tongs", CAT, "Spring-loaded tongs with two cupped jaws holding a spiral snail shell",
      tags=["escargot", "french restaurant", "tongs", "shellfish", "gripper", "fine dining", "snail"])
def _(S):
    return [
        line(poly([(11, 21), (8.5, 12), (7, 5)], r=S.r)),
        line(poly([(13, 21), (15.5, 12), (17, 5)], r=S.r)),
        shell(circle(12, 7.5, 3.6)),
        dot(12, 7.5, 1.1),
    ]


@icon("escargot-plate", CAT, "Round plate seen from above with six small dimples in a ring",
      tags=["snail plate", "snail dish", "escargot", "french restaurant", "baking dish", "appetizer", "starter"])
def _(S):
    parts = [shell(circle(12, 12, 9.5))]
    for i in range(6):
        x, y = polar(12, 12, 5, i * 60 - 90)
        parts.append(hole(rect(x - 1.5, y - 1.5, 3, 3, L(S, 0, 1.5))))
    return parts


@icon("lobster-cracker", CAT, "Hinged cracker with two jaws closing on a lobster claw",
      tags=["nutcracker", "seafood", "shellfish", "crab cracker", "tool", "restaurant", "claw"])
def _(S):
    return [
        line(poly([(21, 5), (4, 12), (21, 19)], r=S.r)),
        shell(ellipse(13, 12, 4.2, 3.2)),
        detail(seg(11, 12, 15, 12)),
    ]


@icon("lobster-bib", CAT, "Bib with a round neck cut-out and a simple lobster printed on its front",
      tags=["seafood bib", "shellfish", "restaurant", "eating", "apron", "clam bake", "crab"])
def _(S):
    body = ("M5.5 3H9.5A2.5 2.5 0 0 0 14.5 3H18.5L20.5 9V21H3.5V9Z" if S.name == "line"
            else "M5.5 3H9.5A2.5 2.5 0 0 0 14.5 3H18.5L20.5 9V17.5Q20.5 21 17 21H7Q3.5 21 3.5 17.5V9Z")
    return [
        shell(body),
        hole(ellipse(12, 14.5, 1.6, 3.2)),
        hole(poly([(10.2, 18.5), (13.8, 18.5), (14.5, 20), (9.5, 20)], closed=True)),
        hole(poly([(10.8, 11.5), (7, 9.5), (8.5, 6.5), (10.8, 8)], closed=True)),
        hole(poly([(13.2, 11.5), (17, 9.5), (15.5, 6.5), (13.2, 8)], closed=True)),
    ]


@icon("finger-bowl", CAT, "Shallow round bowl of water with a lemon slice floating in it",
      tags=["hand wash", "rinse bowl", "fine dining", "seafood", "lemon", "table service", "water bowl"])
def _(S):
    body = ("M2.5 9L5.5 17.5L9.5 19.5H14.5L18.5 17.5L21.5 9" if S.name == "line"
            else "M2.5 9Q3.5 19.5 12 19.5Q20.5 19.5 21.5 9")
    return [
        shell(ellipse(12, 9, 9.5, 3.5)),
        line(body),
        hole(ellipse(12, 9, 3.2, 0.9)),
    ]


@icon("cruet-stand", CAT, "Table stand with a central ring handle holding two stoppered bottles",
      tags=["oil and vinegar", "condiments", "caddy", "dining table", "cruets", "dressing", "restaurant"])
def _(S):
    k = L(S, 0.5, 1.5)
    return [
        shell(circle(12, 4.5, 2.2)),
        line(seg(12, 7, 12, 18)),
        shell(rect(3.5, 8.5, 5, 9.5, k)), solid(rect(4.75, 5, 2.5, 3)),
        shell(rect(15.5, 8.5, 5, 9.5, k)), solid(rect(16.75, 5, 2.5, 3)),
        shell(rect(2, 18, 20, 3.5, rr(S, 1.75))),
    ]


@icon("condiment-caddy", CAT, "Small carrier holding a squeeze bottle, a salt shaker and a napkin stack",
      tags=["table caddy", "ketchup", "salt", "diner", "napkins", "restaurant", "sauce"])
def _(S):
    return [
        shell(poly([(4.5, 12), (4.5, 8), (6.5, 3.5), (8.5, 8), (8.5, 12)], closed=True, r=S.r * 0.5)),
        shell(rect(10.5, 7, 3.5, 5, L(S, 0.3, 1.2))),
        shell(rect(16, 6, 3.5, 6, L(S, 0.3, 1))),
        shell(rect(3, 12, 18, 9, S.R)),
        detail(seg(8, 16.5, 16, 16.5)),
    ]


@icon("sugar-caddy", CAT, "Small holder with upright paper sugar packets standing in it",
      tags=["sugar packets", "sweetener", "cafe", "coffee shop", "table", "tea", "sachets"])
def _(S):
    k = L(S, 0.5, 1.5)
    return [
        shell(rect(5, 3.5, 5, 9.5, k)),
        shell(rect(13.5, 2.5, 5, 10.5, k)),
        detail(seg(5, 7, 10, 7)),
        shell(rect(3, 12, 18, 9, S.R)),
    ]


@icon("toothpick-holder", CAT, "Small cup holding upright toothpicks with one leaning out",
      tags=["toothpicks", "picks", "restaurant counter", "diner", "dispenser", "cup", "table"])
def _(S):
    return [
        line(seg(9.5, 11, 9.5, 3)), line(seg(12.5, 11, 12.5, 2.5)), line(seg(15.5, 11, 18, 4)),
        shell(poly([(6.5, 10), (7.8, 21), (16.2, 21), (17.5, 10)], closed=True, r=S.r)),
    ]


@icon("salt-cellar", CAT, "Tiny open dish on short feet heaped with salt and a miniature spoon resting in it",
      tags=["salt dish", "salt bowl", "seasoning", "table", "pinch", "fine dining", "spoon"])
def _(S):
    return [
        shell(poly([(3, 12), (21, 12), (19.5, 17), (4.5, 17)], closed=True, r=S.r)),
        line(seg(6.5, 17.5, 5.5, 20.5)), line(seg(17.5, 17.5, 18.5, 20.5)),
        hole("M7 12Q12 6 17 12Z"),
        line(seg(13.5, 8, 20.5, 3.5)),
    ]


@icon("cheese-shaker", CAT, "Glass jar with a domed pierced lid and grated cheese inside",
      tags=["parmesan", "pizza", "grated cheese", "pizzeria", "shaker", "condiment", "italian restaurant"])
def _(S):
    return [
        shell("M6 9Q6 3 12 3Q18 3 18 9Z"),
        shell(poly([(6, 9), (6, 21), (18, 21), (18, 9)], closed=False, r=S.r)),
        dot(10, 6.3, 0.8), dot(14, 6.3, 0.8),
        dot(9.5, 17, 1.2), dot(13.5, 18, 1.2), dot(14.5, 13.5, 1.2),
    ]
