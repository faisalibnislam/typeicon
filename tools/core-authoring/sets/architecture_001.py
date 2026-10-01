"""TypeIcon Core: architecture (batch 001).

Named building types and house styles drawn front-on on the ground line y = 21 (outer edge 22),
in the same language as sets/buildings.py: closed walls are shells, doors and trim are details,
and windows are small solid blocks (`win`) that are knocked out of Filled walls.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d  # noqa: F401

CAT = "architecture"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def win(x, y, w=2.0, h=2.0):
    """Window block: solid in Line/Rounded, knocked out of a Filled wall."""
    return Part("dot", rect(x, y, w, h))


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled wall."""
    return Part("dot", d)


def rot_pts(pts, deg, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def pt_on_(c, r, deg):
    return (c[0] + r * math.cos(math.radians(deg)), c[1] + r * math.sin(math.radians(deg)))


def door(S, x0, x1, top, ground=21.0):
    """Square-headed door outline standing on the ground line."""
    return detail(poly([(x0, ground), (x0, top), (x1, top), (x1, ground)], r=S.r * 0.5))


def arch_door(x0, x1, top, ground=21.0):
    """Round-headed door; `top` is the crown of the arch."""
    r = (x1 - x0) / 2
    return detail(f"M{fmt(x0)} {fmt(ground)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(ground)}")


def awning_shop(S, top=3.0, eave=9.0):
    """Striped awning over a shop body (walls x 5-19)."""
    return [
        shell(poly([(3, eave), (5, top), (19, top), (21, eave)], closed=True, r=S.r)),
        detail(seg(9.67, top, 9, eave)), detail(seg(14.33, top, 15, eave)),
        shell(poly([(5, eave), (5, 21), (19, 21), (19, eave)], closed=True, r=S.r)),
        detail(seg(3, eave, 21, eave)),
    ]


# ============================================================================ civic

@icon("city-hall", CAT, "Wide civic building with a central clock tower, columns and front steps",
      tags=["town hall", "municipal", "council", "government", "civic", "mayor"], aliases=["town-hall"])
def _(S):
    return [
        shell(poly([(3, 17), (3, 11), (8.5, 11), (8.5, 5.5), (12, 2.5), (15.5, 5.5), (15.5, 11), (21, 11), (21, 17)],
                   closed=True, r=S.r * 0.5)),
        dot(12, 7.75, 1.75),
        *[detail(seg(x, 13.5, x, 17)) for x in (6, 10, 14, 18)],
        line(seg(3, 21, 21, 21)),
    ]


@icon("embassy", CAT, "Columned building with a flag flying from a pole on its pediment",
      tags=["consulate", "diplomatic", "foreign mission", "ambassador", "visa", "government"],
      aliases=["consulate"])
def _(S):
    return [
        line(seg(12, 2, 12, 6.5)),
        solid(rect(12, 2, 4.5, 3)),
        shell(poly([(3, 10.5), (12, 6.5), (21, 10.5)], closed=True, r=S.r * 0.5)),
        *[line(seg(x, 12.5, x, 16.5)) for x in (6, 10, 14, 18)],
        line(seg(3.5, 18, 20.5, 18)),
        line(seg(2, 21, 22, 21)),
    ]


@icon("prison", CAT, "Barred prison block topped with wire beside a corner guard tower",
      tags=["jail", "penitentiary", "correctional facility", "detention", "gaol", "lockup"],
      aliases=["jail", "penitentiary"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 6.5), (5.5, 3.5), (8, 6.5), (8, 21)], closed=True, r=S.r * 0.5)),
        win(4.5, 8.5, 2, 2),
        line(poly([(11, 7.5), (13.5, 5), (16, 7.5), (18.5, 5), (21, 7.5)], r=S.r * 0.5)),
        shell(rect(11, 10.5, 10, 10.5, min(S.R, 2))),
        detail(seg(14.5, 10.5, 14.5, 21)), detail(seg(17.5, 10.5, 17.5, 21)),
    ]


@icon("bunker", CAT, "Low half-buried concrete bunker with a narrow slit window",
      tags=["shelter", "pillbox", "fallout shelter", "military", "concrete", "fortification"],
      aliases=["pillbox"])
def _(S):
    body = L(S, "M2.5 20H21.5L19.5 15C18.5 11.5 15.5 9.5 12 9.5C8.5 9.5 5.5 11.5 4.5 15Z",
             "M2.5 20H21.5C20.5 18 19.8 16.5 19.5 15C18.5 11.5 15.5 9.5 12 9.5C8.5 9.5 5.5 11.5 4.5 15C4.2 16.5 3.5 18 2.5 20Z")
    return [
        shell(body),
        detail(seg(8.5, 14.5, 15.5, 14.5)),
    ]


@icon("community-center", CAT, "Low building with a group of three people on its front",
      tags=["community centre", "civic center", "community hall", "meeting place", "social club", "neighborhood"],
      aliases=["community-centre"])
def _(S):
    center = "M8.5 17.5A3.5 3.5 0 0 1 15.5 17.5Z"
    sides = [f"M{fmt(c - 2.75)} 17.5A2.75 2.75 0 0 1 {fmt(c + 2.75)} 17.5Z" for c in (7.25, 16.75)]
    cut = U(P(center), ST(center, 2))
    return [
        shell(poly([(2.5, 21), (2.5, 8), (7.5, 8), (7.5, 4.5), (16.5, 4.5), (16.5, 8), (21.5, 8), (21.5, 21)],
                   closed=True, r=S.r * 0.5)),
        dot(12, 10, 1.75), dot(7.25, 12, 1.4), dot(16.75, 12, 1.4),
        mark(center),
        *[mark(path_to_d(D(P(d), cut))) for d in sides],
    ]


@icon("laboratory-building", CAT, "Flat-roofed research building with a conical flask on its front",
      tags=["lab", "research center", "science", "laboratory", "research institute", "chemistry"],
      aliases=["research-lab"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(poly([(10.5, 6.5), (10.5, 10.5), (7, 17), (17, 17), (13.5, 10.5), (13.5, 6.5)], r=S.r * 0.5)),
        detail(seg(9.5, 6.5, 14.5, 6.5)),
    ]


@icon("lifeguard-tower", CAT, "Beach lifeguard hut on tall stilts with a ramp and a flag",
      tags=["lifeguard station", "beach", "rescue", "beach patrol", "lookout", "swimming"],
      aliases=["lifeguard-station"])
def _(S):
    return [
        line(seg(12, 2, 12, 5)),
        solid(poly([(12, 2), (15.5, 3), (12, 4)], closed=True)),
        line(poly([(4, 9.5), (12, 5), (20, 9.5)], r=S.r)),
        shell(poly([(6.5, 15), (6.5, 8.1), (12, 5), (17.5, 8.1), (17.5, 15)], closed=True, r=S.r * 0.5)),
        detail(seg(9.5, 11, 14.5, 11)),
        line(seg(8.5, 15, 8, 21)), line(seg(15.5, 15, 16, 21)),
        line(seg(8.3, 18, 15.7, 18)),
        line(seg(17.5, 15, 22, 21)),
    ]


@icon("fire-lookout-tower", CAT, "Steel lattice tower with a glass lookout cab and a pointed roof",
      tags=["fire tower", "forest lookout", "wildfire", "forestry", "observation", "ranger"],
      aliases=["fire-tower"])
def _(S):
    return [
        shell(poly([(8, 9.5), (8, 5), (12, 2), (16, 5), (16, 9.5)], closed=True, r=S.r * 0.5)),
        detail(seg(8, 5, 16, 5)),
        detail(seg(12, 5, 12, 9.5)),
        line(seg(9, 9.5, 5.5, 21)), line(seg(15, 9.5, 18.5, 21)),
        line(poly([(8.4, 12), (15.6, 12)])),
        line(seg(8.2, 12.5, 16.4, 20)), line(seg(15.8, 12.5, 7.6, 20)),
    ]


@icon("watchtower", CAT, "Wooden watchtower on splayed legs with a roofed platform and a ladder",
      tags=["lookout tower", "guard tower", "sentry", "hunting stand", "outpost", "wooden tower"],
      aliases=["lookout-tower", "guard-tower"])
def _(S):
    return [
        shell(poly([(4.5, 7), (12, 2.5), (19.5, 7)], closed=True, r=S.r * 0.5)),
        line(seg(6.5, 7, 6.5, 11)), line(seg(17.5, 7, 17.5, 11)),
        shell(rect(4.5, 11, 15, 2.5, min(S.R, 1))),
        line(seg(6.5, 13.5, 4, 21)), line(seg(17.5, 13.5, 20, 21)),
        line(seg(10.5, 13.5, 10.5, 21)), line(seg(13.5, 13.5, 13.5, 21)),
        line(seg(10.5, 16, 13.5, 16)), line(seg(10.5, 19, 13.5, 19)),
    ]


# ============================================================================ walls and gates

@icon("city-wall", CAT, "Long crenellated stone wall with a square tower in the middle",
      tags=["town wall", "fortification", "rampart", "battlement", "defensive wall", "medieval"],
      aliases=["town-wall", "rampart"])
def _(S):
    pts = [(2, 21), (2, 10.5), (3.75, 10.5), (3.75, 13), (6.75, 13), (6.75, 10.5), (8.5, 10.5), (8.5, 3.5),
           (10.25, 3.5), (10.25, 6), (13.75, 6), (13.75, 3.5), (15.5, 3.5), (15.5, 10.5), (17.25, 10.5), (17.25, 13),
           (20.25, 13), (20.25, 10.5), (22, 10.5), (22, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.4)),
        detail(seg(12, 9, 12, 13)),
    ]


@icon("city-gate", CAT, "Large arched gateway in a crenellated wall between two towers",
      tags=["town gate", "gateway", "fortified gate", "medieval", "entrance", "portal"],
      aliases=["town-gate"])
def _(S):
    pts = [(2.5, 21), (2.5, 4), (4.25, 4), (4.25, 5.5), (6.25, 5.5), (6.25, 4), (8, 4), (8, 8.5), (10, 8.5), (10, 10),
           (14, 10), (14, 8.5), (16, 8.5), (16, 4), (17.75, 4), (17.75, 5.5), (19.75, 5.5), (19.75, 4), (21.5, 4),
           (21.5, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.4)),
        arch_door(8.5, 15.5, 13),
        detail(seg(5.25, 9, 5.25, 12)), detail(seg(18.75, 9, 18.75, 12)),
    ]


# ============================================================================ small public buildings

@icon("information-kiosk", CAT, "Freestanding booth under a roof with a large letter i on the front",
      tags=["info booth", "information desk", "help desk", "tourist information", "visitor center", "kiosk"],
      aliases=["info-kiosk", "info-booth"])
def _(S):
    return [
        shell(poly([(3.5, 8), (5.5, 3.5), (18.5, 3.5), (20.5, 8)], closed=True, r=S.r * 0.5)),
        shell(rect(6, 10, 12, 11, min(S.R, 2))),
        dot(12, 12.75, 1.25),
        detail(seg(12, 15, 12, 19)),
    ]


@icon("ranger-station", CAT, "Log ranger cabin with a badge by the door beside a tall pine",
      tags=["park ranger", "forest station", "national park", "ranger cabin", "warden", "forestry"],
      aliases=["ranger-cabin"])
def _(S):
    return [
        line(poly([(2, 12), (8.5, 6), (15, 12)], r=S.r)),
        shell(poly([(4, 10.2), (8.5, 6), (13, 10.2), (13, 21), (4, 21)], closed=True, r=S.r * 0.5)),
        mark("M6.5 13H10.5V15.5C10.5 17 9.6 17.8 8.5 18.4C7.4 17.8 6.5 17 6.5 15.5Z"),
        shell(poly([(18.5, 2.5), (22, 9), (20.5, 9), (22, 14.5), (15, 14.5), (16.5, 9), (15, 9)], closed=True, r=S.r * 0.5)),
        line(seg(18.5, 14.5, 18.5, 21)),
    ]


@icon("butcher-shop", CAT, "Shop front with an awning and a meat cleaver sign",
      tags=["butcher", "meat shop", "butchery", "deli", "meat market", "cleaver"], aliases=["butchery"])
def _(S):
    blade = poly(rot_pts([(9.5, 11), (16.5, 11), (16.5, 16.5), (10.5, 16.5), (9.5, 15.5)], -25, 12, 15), closed=True)
    hole = circle(*rot_pts([(14.75, 12.75)], -25, 12, 15)[0], 0.9)
    handle = rot_pts([(9.5, 12.25), (5.5, 12.25)], -25, 12, 15)
    return [
        *awning_shop(S),
        mark(path_to_d(D(P(blade), P(hole)))),
        detail(poly(handle)),
    ]


@icon("florist-shop", CAT, "Shop front with an awning and a bucket of flowers",
      tags=["florist", "flower shop", "flowers", "bouquet", "garden shop", "flower stall"],
      aliases=["flower-shop"])
def _(S):
    return [
        *awning_shop(S),
        dot(8.5, 12, 1.5), dot(12, 11.25, 1.5), dot(15.5, 12, 1.5),
        detail(seg(12, 12.5, 12, 16.5)), detail(seg(9.2, 13.2, 10.5, 16.5)), detail(seg(14.8, 13.2, 13.5, 16.5)),
        detail(poly([(8, 16.5), (16, 16.5), (15, 21), (9, 21)], r=S.r * 0.5)),
    ]


@icon("bookshop", CAT, "Shop front with an awning and an open book sign",
      tags=["bookstore", "book shop", "books", "bookseller", "reading", "literature"], aliases=["bookstore"])
def _(S):
    book = ("M7 12.5C8.8 11.9 10.6 12.2 12 13.3C13.4 12.2 15.2 11.9 17 12.5V18C15.2 17.4 13.4 17.7 12 18.8"
            "C10.6 17.7 8.8 17.4 7 18Z")
    return [
        *awning_shop(S),
        detail(book), detail(seg(12, 13.3, 12, 18.8)),
    ]


@icon("barbershop", CAT, "Small shop with a striped barber pole beside the door",
      tags=["barber", "barber shop", "haircut", "men's grooming", "shave", "barber pole"],
      aliases=["barber-shop"])
def _(S):
    return [
        shell(poly([(2.5, 21), (2.5, 8), (8.5, 4), (14.5, 8), (14.5, 21)], closed=True, r=S.r * 0.5)),
        door(S, 6, 11, 14),
        shell(rect(17, 5.5, 4, 12, min(S.R, 2))),
        detail(seg(17, 9.5, 21, 7)), detail(seg(17, 14, 21, 11.5)),
        line(seg(19, 2.5, 19, 5.5)), line(seg(19, 17.5, 19, 21)),
    ]


@icon("hair-salon", CAT, "Shop front with an awning and a large pair of scissors",
      tags=["hairdresser", "salon", "beauty salon", "haircut", "stylist", "hair"])
def _(S):
    return [
        *awning_shop(S),
        detail(circle(9.5, 17.25, 1.75)), detail(circle(14.5, 17.25, 1.75)),
        detail(seg(10.4, 15.6, 15, 11)), detail(seg(13.6, 15.6, 9, 11)),
    ]


@icon("market-stall", CAT, "Market stall with a striped awning on poles over a counter of produce",
      tags=["stall", "market", "farmers market", "vendor", "street market", "booth"])
def _(S):
    return [
        shell(poly([(2.5, 8), (4.5, 3), (19.5, 3), (21.5, 8)], closed=True, r=S.r)),
        detail(seg(9.5, 3, 9, 8)), detail(seg(14.5, 3, 15, 8)),
        line(seg(4.5, 8, 4.5, 15.5)), line(seg(19.5, 8, 19.5, 15.5)),
        dot(8.5, 12, 1.6), dot(12, 12, 1.6), dot(15.5, 12, 1.6),
        shell(rect(3, 15.5, 18, 5.5, min(S.R, 1.5))),
    ]


@icon("market-hall", CAT, "Market hall with a barrel-vaulted roof and a large arched end window",
      tags=["covered market", "food hall", "market", "arcade", "halle", "iron and glass"],
      aliases=["covered-market"])
def _(S):
    c = (12, 15)
    return [
        shell("M3 21V12A9 9 0 0 1 21 12V21Z" if S.name == "line" else "M3 19V12A9 9 0 0 1 21 12V19A2 2 0 0 1 19 21H5A2 2 0 0 1 3 19Z"),
        detail("M6 15A6 6 0 0 1 18 15Z"),
        *[detail(seg(c[0], c[1], *pt_on_(c, 6, a))) for a in (225, 270, 315)],
        door(S, 10, 14, 18),
    ]


@icon("food-kiosk", CAT, "Food kiosk with its service flap propped open and a menu board beside it",
      tags=["snack bar", "food stand", "street food", "concession stand", "takeaway", "snack kiosk"],
      aliases=["snack-kiosk", "food-stand"])
def _(S):
    return [
        shell(poly([(2, 8.5), (4, 4.5), (13, 4.5), (15, 8.5)], closed=True, r=S.r)),
        shell(rect(3, 10.5, 11, 10.5, min(S.R, 2))),
        detail(rect(5.5, 12.75, 6, 3.5, min(S.R, 1))),
        shell(rect(16.5, 9, 5, 6.5, min(S.R, 1.5))),
        line(seg(19, 15.5, 19, 21)),
    ]


@icon("newsstand", CAT, "Roofed news booth with rows of magazines on racks",
      tags=["news kiosk", "newsagent", "magazines", "newspapers", "press", "kiosk"], aliases=["news-kiosk"])
def _(S):
    parts = [
        shell(poly([(2.5, 7), (4.5, 3), (19.5, 3), (21.5, 7)], closed=True, r=S.r)),
        shell(rect(4, 9, 16, 12, min(S.R, 2))),
        detail(seg(4, 14.75, 20, 14.75)),
    ]
    for y in (10.5, 16.25):
        for x in (6.5, 10.75, 15):
            parts.append(mark(rect(x, y, 2.5, 3.25)))
    return parts


@icon("roadside-diner", CAT, "Long low diner with rounded ends like a rail car beside a tall pole sign",
      tags=["diner", "roadside restaurant", "truck stop", "cafe", "road trip", "burger joint"],
      aliases=["diner"])
def _(S):
    return [
        shell(rect(2.5, 10, 13.5, 8.5, L(S, 3, 4))),
        win(5, 12.5, 2, 2.5), win(8.25, 12.5, 2, 2.5), win(11.5, 12.5, 2, 2.5),
        line(seg(3.5, 21, 15, 21)),
        shell(rect(17, 3, 4.5, 5.5, min(S.R, 1.5))),
        line(seg(19.25, 8.5, 19.25, 21)),
    ]


@icon("ice-cream-parlor", CAT, "Ice cream shop with a giant cone sign on its roof",
      tags=["ice cream shop", "gelato", "creamery", "parlour", "dessert", "sweet shop"],
      aliases=["ice-cream-parlour", "ice-cream-shop"])
def _(S):
    drip = "M16.5 7.5A1.5 1.5 0 0 1 13.5 7.5A1.5 1.5 0 0 1 10.5 7.5A1.5 1.5 0 0 1 7.5 7.5"
    scoop = "M7.5 7.5A4.5 4.5 0 0 1 16.5 7.5" + drip[drip.index("A"):] + "Z"
    cone = poly([(9, 8), (15, 8), (12, 14)], closed=True)
    return [
        shell(path_to_d(U(P(scoop), P(cone)))),
        detail(drip),
        shell(rect(3, 16, 18, 5, min(S.R, 2))),
        win(5.5, 17.5, 2.5, 2), win(10.75, 17.5, 2.5, 2), win(16, 17.5, 2.5, 2),
    ]


@icon("teahouse", CAT, "Japanese teahouse with a curved roof, sliding paper doors and a veranda",
      tags=["tea house", "japanese house", "chashitsu", "tea ceremony", "tea room", "machiya"],
      aliases=["tea-house"])
def _(S):
    return [
        shell("M2 10.5Q5.5 10.5 7 6.5H17Q18.5 10.5 22 10.5Z"),
        shell(rect(5, 12.5, 14, 7.5, min(S.R, 1))),
        detail(seg(9.67, 12.5, 9.67, 20)), detail(seg(14.33, 12.5, 14.33, 20)),
        detail(seg(5, 16.25, 19, 16.25)),
        line(seg(2.5, 20.5, 21.5, 20.5)),
    ]


@icon("drive-in-theater", CAT, "Outdoor movie screen on posts with cars parked in front",
      tags=["drive-in", "drive in movie", "outdoor cinema", "open air cinema", "movies", "film"],
      aliases=["drive-in-cinema"])
def _(S):
    car = lambda x: poly([(x, 21), (x, 18.5), (x + 1.5, 18.5), (x + 2.5, 16.5), (x + 5.5, 16.5), (x + 6.5, 18.5),
                          (x + 8, 18.5), (x + 8, 21)], closed=True, r=S.r * 0.6)
    return [
        shell(rect(3, 2.5, 18, 9, min(S.R, 2))),
        mark(poly([(10.5, 5), (14, 7), (10.5, 9)], closed=True)),
        line(seg(7, 11.5, 7, 14.5)), line(seg(17, 11.5, 17, 14.5)),
        shell(car(2.5)), shell(car(13.5)),
    ]


@icon("opera-house", CAT, "Grand opera house with three tall arched doorways and a low dome",
      tags=["opera", "concert hall", "theatre", "theater", "performing arts", "symphony hall"])
def _(S):
    return [
        line(seg(12, 2, 12, 4)),
        shell("M8.5 7.5A3.5 3.5 0 0 1 15.5 7.5Z"),
        shell(poly([(3, 21), (3, 9.5), (21, 9.5), (21, 21)], closed=True, r=S.r * 0.5)),
        line(seg(2, 7.5, 22, 7.5)),
        arch_door(5.5, 8.5, 12.5), arch_door(10.5, 13.5, 12.5), arch_door(15.5, 18.5, 12.5),
    ]


@icon("amphitheater", CAT, "Semicircular tiers of stone seats around a flat stage",
      tags=["amphitheatre", "open air theater", "arena", "greek theater", "roman theater", "auditorium"],
      aliases=["amphitheatre"])
def _(S):
    c = (12, 16.5)
    return [
        line(arc(c[0], c[1], 9.5, 180, 360)),
        line(arc(c[0], c[1], 5.75, 180, 360)),
        line(arc(c[0], c[1], 2, 180, 360)),
        *[line(seg(*pt_on_(c, 5.75, a), *pt_on_(c, 9.5, a))) for a in (240, 300)],
        line(seg(4, 20.5, 20, 20.5)),
    ]


@icon("bandstand", CAT, "Raised bandstand platform under a pointed roof on slim posts",
      tags=["band shell", "gazebo", "pavilion", "park stage", "brass band", "music"])
def _(S):
    return [
        line(seg(12, 1.5, 12, 3)),
        shell(poly([(3, 8.5), (12, 3), (21, 8.5)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        line(seg(5, 8.5, 5, 14)), line(seg(12, 8.5, 12, 14)), line(seg(19, 8.5, 19, 14)),
        shell(rect(3, 14, 18, 7, min(S.R, 2))),
        detail(seg(3, 16.5, 21, 16.5)),
        *[detail(seg(x, 16.5, x, 21)) for x in (7.5, 12, 16.5)],
    ]


@icon("auto-repair-shop", CAT, "Garage with a raised roll-up door and a wrench sign above it",
      tags=["auto repair", "car repair", "mechanic", "garage", "car service", "workshop"],
      aliases=["car-repair-shop", "mechanic-shop"])
def _(S):
    return [
        line(arc(5.5, 5.5, 2.5, -140, 140)), line(arc(18.5, 5.5, 2.5, 40, 320)),
        line(seg(8, 5.5, 16, 5.5)),
        shell(rect(3, 10.5, 18, 10.5, min(S.R, 2))),
        detail(poly([(6.5, 21), (6.5, 13.5), (17.5, 13.5), (17.5, 21)], r=S.r * 0.5)),
        detail(seg(6.5, 16, 17.5, 16)),
    ]


@icon("storage-units", CAT, "Self-storage building with a row of roll-up doors under one flat roof",
      tags=["self storage", "storage unit", "lockup", "storage facility", "garage units", "moving"],
      aliases=["self-storage"])
def _(S):
    return [
        line(seg(2, 4.5, 22, 4.5)),
        shell(rect(3, 7.5, 18, 13.5, min(S.R, 2))),
        *[mark(rect(x, 11, 3.5, 10)) for x in (5, 10.25, 15.5)],
    ]


@icon("drive-through", CAT, "Small building with a side service window and a car pulling up beside it",
      tags=["drive thru", "drive-thru", "fast food", "takeout", "pickup window", "car service"],
      aliases=["drive-thru"])
def _(S):
    return [
        shell(rect(2, 5, 8.5, 16, min(S.R, 2))),
        detail(rect(5, 9, 5.5, 4, min(S.R, 1))),
        shell(poly([(12.5, 18), (12.5, 15), (14.5, 14.5), (16, 11.5), (19.5, 11.5), (21.5, 14.5), (21.5, 18)],
                   closed=True, r=S.r * 0.6)),
        dot(15.25, 19.25, 1.75), dot(19, 19.25, 1.75),
        line("M21.5 7.5A4.5 4.5 0 0 0 14.5 4.5"),
        solid(poly([(12.5, 3), (15.6, 2.4), (15, 6.2)], closed=True)),
    ]


@icon("car-dealership", CAT, "Glass-fronted showroom with a car inside and pennant bunting on the roof",
      tags=["car showroom", "car dealer", "auto dealer", "car sales", "showroom", "motor dealer"],
      aliases=["car-showroom"])
def _(S):
    return [
        line(seg(2, 3, 22, 3)),
        *[solid(poly([(x, 3), (x + 3, 3), (x + 1.5, 5.75)], closed=True)) for x in (3, 8, 13, 18)],
        shell(rect(3, 8, 18, 13, min(S.R, 2))),
        detail(poly([(6, 17.5), (6, 15), (8, 14.5), (9.5, 12), (14.5, 12), (16.5, 14.5), (18, 15), (18, 17.5)],
                    closed=True, r=S.r * 0.5)),
        dot(9, 17.75, 1.25), dot(15, 17.75, 1.25),
    ]


@icon("bathhouse", CAT, "Domed bathhouse with star skylights and steam rising from the top",
      tags=["bath house", "hammam", "turkish bath", "public baths", "sauna", "onsen"],
      aliases=["hammam"])
def _(S):
    return [
        line("M8 7C7 6 9 4.5 8 3"), line("M12 6C11 5 13 3.5 12 2"), line("M16 7C15 6 17 4.5 16 3"),
        shell("M3 21V14H4.5A7.5 5.5 0 0 1 19.5 14H21V21Z"),
        detail(seg(3, 14, 21, 14)),
        dot(8.75, 11.75, 1), dot(12, 10.5, 1), dot(15.25, 11.75, 1),
        arch_door(10, 14, 16.5),
    ]


@icon("public-aquarium", CAT, "Aquarium building with a wave-shaped roof and a large fish on its glass front",
      tags=["aquarium", "marine center", "oceanarium", "marine park", "fish", "sea life"],
      aliases=["oceanarium"])
def _(S):
    return [
        shell("M3 21V7.5C5.5 5 8 5 10.5 7.5S15.5 10 18 7.5C19 6.5 20 6 21 6V21Z" if S.name == "line" else
              "M3 19V7.5C5.5 5 8 5 10.5 7.5S15.5 10 18 7.5C19 6.5 20 6 21 6V19A2 2 0 0 1 19 21H5A2 2 0 0 1 3 19Z"),
        detail("M6 15C8 12.2 12 12.2 14.5 15C12 17.8 8 17.8 6 15Z"),
        detail(poly([(14.5, 15), (18, 12.5), (18, 17.5)], closed=True, r=S.r * 0.4)),
        dot(8.75, 14.5, 0.9),
    ]


@icon("thatched-cottage", CAT, "Small cottage under a thick rounded thatched roof",
      tags=["cottage", "thatch", "country cottage", "rural", "village", "hut"], aliases=["thatch-cottage"])
def _(S):
    return [
        shell("M2.5 13.5C2.5 7.5 6.5 3.5 12 3.5C17.5 3.5 21.5 7.5 21.5 13.5Z"),
        detail("M6.5 13.5C6.5 9.5 9 7.5 12 7.5C15 7.5 17.5 9.5 17.5 13.5"),
        shell(poly([(4.5, 15.5), (4.5, 21), (19.5, 21), (19.5, 15.5)], r=S.r)),
        door(S, 10, 14, 17),
        win(6.5, 17, 2, 2), win(15.5, 17, 2, 2),
    ]


@icon("bungalow", CAT, "Single-storey house with a low wide roof over a front porch on posts",
      tags=["single storey", "one story house", "cottage", "porch", "home", "house"])
def _(S):
    return [
        shell(poly([(2, 10.5), (6, 5), (18, 5), (22, 10.5)], closed=True, r=S.r * 0.5)),
        line(seg(4, 10.5, 4, 21)), line(seg(20, 10.5, 20, 21)),
        door(S, 10, 14, 14),
        win(6.5, 13.5, 2, 2.5), win(15.5, 13.5, 2, 2.5),
        line(seg(2, 21, 22, 21)),
    ]


@icon("villa", CAT, "Mediterranean villa with a low tiled roof, arched windows and a small square tower",
      tags=["mediterranean house", "holiday villa", "country house", "estate", "vacation home", "luxury home"])
def _(S):
    return [
        line(poly([(2, 6.5), (6, 3.5), (10, 6.5)], r=S.r)),
        line(poly([(8.5, 11.5), (15, 8), (22, 11.5)], r=S.r)),
        shell(poly([(3, 21), (3, 6), (9, 6), (9, 10.7), (15, 8.5), (21, 10.7), (21, 21)], closed=True, r=S.r * 0.5)),
        arch_door(4.75, 7.25, 8.5, 12.5),
        arch_door(10.5, 13.5, 15),
        arch_door(16, 19, 13, 17.5),
    ]


@icon("mansion", CAT, "Large symmetrical mansion with a columned entrance and a chimney at each end",
      tags=["stately home", "manor", "estate", "luxury house", "grand house", "residence"],
      aliases=["stately-home"])
def _(S):
    return [
        line(seg(5.5, 2, 5.5, 5)), line(seg(18.5, 2, 18.5, 5)),
        shell(poly([(3, 21), (3, 9), (6.5, 5.5), (17.5, 5.5), (21, 9), (21, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(3, 9, 21, 9)),
        win(5.25, 11.5), win(5.25, 16), win(16.75, 11.5), win(16.75, 16),
        detail(seg(9.5, 11.5, 9.5, 21)), detail(seg(14.5, 11.5, 14.5, 21)),
    ]


@icon("townhouse", CAT, "Narrow three-storey townhouse with steps up to the front door",
      tags=["town house", "terraced house", "row house", "city house", "narrow house", "home"],
      aliases=["town-house"])
def _(S):
    return [
        shell(poly([(6.5, 19), (6.5, 6.5), (12, 2.5), (17.5, 6.5), (17.5, 19)], closed=True, r=S.r * 0.5)),
        win(8.75, 7.5), win(13.25, 7.5), win(8.75, 11), win(13.25, 11),
        door(S, 10.25, 13.75, 14.5, 19),
        line(seg(8, 21, 16, 21)),
    ]


@icon("row-houses", CAT, "Three identical narrow houses joined side by side under matching roofs",
      tags=["terraced houses", "terrace", "rowhouses", "townhouses", "street", "housing"],
      aliases=["terraced-houses"])
def _(S):
    pts = [(2, 21), (2, 9), (5.33, 5), (8.67, 9), (12, 5), (15.33, 9), (18.67, 5), (22, 9), (22, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.5)),
        detail(seg(8.67, 9, 8.67, 21)), detail(seg(15.33, 9, 15.33, 21)),
        *[mark(rect(x - 1, 15.5, 2, 5.5)) for x in (5.33, 12, 18.67)],
        *[win(x - 1, 10.5) for x in (5.33, 12, 18.67)],
    ]


@icon("duplex", CAT, "Two-family house with mirrored front doors and a dividing wall through the roof",
      tags=["semi-detached", "two family house", "twin house", "double house", "semi", "housing"],
      aliases=["semi-detached"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 10), (12, 4), (21, 10), (21, 21)], closed=True, r=S.r * 0.5)),
        line(seg(12, 1.5, 12, 4)),
        detail(seg(12, 4, 12, 21)),
        door(S, 6.5, 9.5, 15.5), door(S, 14.5, 17.5, 15.5),
        win(7, 11), win(15, 11),
    ]


@icon("ranch-house", CAT, "Long low ranch house with a shallow roof and an attached garage",
      tags=["rambler", "single story", "suburban house", "ranch style", "home", "garage"],
      aliases=["rambler"])
def _(S):
    return [
        shell(poly([(2, 21), (2, 13), (5, 9.5), (19, 9.5), (22, 13), (22, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(2, 13, 22, 13)),
        win(4.5, 15.5, 2.5, 2), door(S, 9, 11.5, 15.5),
        detail(poly([(14, 21), (14, 15.5), (20, 15.5), (20, 21)], r=S.r * 0.5)),
        detail(seg(14, 18.25, 20, 18.25)),
    ]


@icon("saltbox-house", CAT, "Saltbox house whose roof has a short front slope and a long rear slope",
      tags=["saltbox", "colonial house", "new england", "lean-to roof", "farmhouse", "house"],
      aliases=["saltbox"])
def _(S):
    return [
        line(seg(10, 2, 10, 4.5)),
        shell(poly([(3, 21), (3, 9), (8.5, 4), (21, 15), (21, 21)], closed=True, r=S.r * 0.5)),
        win(5.5, 10.5), win(9.5, 10.5),
        win(5.5, 15), win(9.5, 15),
        door(S, 14, 17, 17),
    ]


@icon("a-frame-cabin", CAT, "A-frame cabin whose steep roof reaches the ground, with a tall glass gable",
      tags=["a-frame", "cabin", "chalet", "ski lodge", "holiday cabin", "triangle house"],
      aliases=["a-frame"])
def _(S):
    return [
        line(poly([(2, 21), (12, 2.5), (22, 21)], r=S.r), stroke_miterlimit="4"),
        shell(poly([(6.5, 21), (12, 10), (17.5, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(12, 10, 12, 21)), detail(seg(8.5, 17, 15.5, 17)),
    ]


@icon("mobile-home", CAT, "Long trailer home with small windows, a door and skirting underneath",
      tags=["trailer home", "manufactured home", "static caravan", "trailer park", "prefab", "park home"],
      aliases=["trailer-home", "static-caravan"])
def _(S):
    return [
        shell(rect(2, 6.5, 20, 11, min(S.R, 2))),
        win(4.5, 9.5, 3, 2.5), win(14.5, 9.5, 2.5, 2.5), win(18, 9.5, 2, 2.5),
        door(S, 9.5, 12.5, 9.5, 17.5),
        line(seg(3.5, 20.5, 20.5, 20.5)),
    ]


@icon("yurt", CAT, "Round yurt with a low domed roof, a lattice wall and a small door",
      tags=["ger", "mongolian tent", "nomad tent", "glamping", "felt tent", "round tent"], aliases=["ger"])
def _(S):
    return [
        shell("M3.5 21V13H2.5C5 9 8.5 5.5 12 5.5C15.5 5.5 19 9 21.5 13H20.5V21Z"),
        line(seg(10, 3.5, 14, 3.5)),
        detail(seg(3.5, 13, 20.5, 13)),
        detail(poly([(3.5, 15.5), (5.25, 18.5), (7, 15.5), (8.75, 18.5)], r=S.r * 0.4)),
        detail(poly([(20.5, 15.5), (18.75, 18.5), (17, 15.5), (15.25, 18.5)], r=S.r * 0.4)),
        door(S, 10.5, 13.5, 15.5),
    ]


@icon("tipi", CAT, "Tall conical tipi with its poles crossing above the top and a door flap at the base",
      tags=["teepee", "tepee", "lodge", "plains dwelling", "tent", "cone tent"], aliases=["teepee", "tepee"])
def _(S):
    return [
        shell(poly([(5, 21), (12, 6.5), (19, 21)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        line(seg(12, 6.5, 8.5, 2)), line(seg(12, 6.5, 15.5, 2)), line(seg(12, 6.5, 12, 2)),
        detail(seg(8.1, 14.5, 15.9, 14.5)),
        detail("M9.75 21A2.25 3 0 0 1 14.25 21"),
    ]


@icon("wigwam", CAT, "Domed wigwam of bent poles covered with bark panels and a low door",
      tags=["wickiup", "dome hut", "bark house", "woodland dwelling", "lodge", "shelter"])
def _(S):
    return [
        shell("M3 21C3 12.5 7 7.5 12 7.5C17 7.5 21 12.5 21 21Z"),
        line(seg(10, 7.9, 14, 3)), line(seg(14, 7.9, 10, 3)),
        detail("M4.2 13.5C7.5 12 16.5 12 19.8 13.5"),
        detail("M3.3 17.5C4.5 17 6 16.8 7.5 16.7"), detail("M20.7 17.5C19.5 17 18 16.8 16.5 16.7"),
        detail("M9.5 21V18.5A2.5 2.5 0 0 1 14.5 18.5V21"),
    ]


@icon("round-hut", CAT, "Round hut with mud walls under a wide conical straw roof",
      tags=["rondavel", "mud hut", "grass hut", "village hut", "african hut", "thatched hut"],
      aliases=["rondavel"])
def _(S):
    return [
        shell(poly([(2.5, 13), (12, 3), (21.5, 13)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        detail(seg(6.2, 9.2, 17.8, 9.2)),
        shell(poly([(5, 15), (5, 21), (19, 21), (19, 15)], r=S.r)),
        arch_door(10, 14, 16.5),
    ]


@icon("stilt-house", CAT, "Wooden house raised high on posts with a ladder up to the door",
      tags=["house on stilts", "pile dwelling", "raised house", "flood house", "tropical house", "kampong"],
      aliases=["pile-dwelling"])
def _(S):
    return [
        line(poly([(2.5, 8.5), (12, 2.5), (21.5, 8.5)], r=S.r)),
        shell(poly([(5, 13), (5, 7.1), (12, 2.5), (19, 7.1), (19, 13)], closed=True, r=S.r * 0.5)),
        detail(poly([(13, 13), (13, 9), (16, 9), (16, 13)], r=S.r * 0.4)),
        line(seg(6.5, 13, 6.5, 21)), line(seg(17.5, 13, 17.5, 21)),
        line(seg(12.5, 13, 10, 21)), line(seg(15.5, 13, 13, 21)),
        line(seg(11.25, 17, 14.25, 17)),
    ]


@icon("overwater-bungalow", CAT, "Thatched hut on stilts over water joined to the shore by a walkway",
      tags=["water villa", "overwater villa", "maldives", "island resort", "honeymoon", "lagoon"],
      aliases=["water-villa"])
def _(S):
    return [
        shell(poly([(2.5, 9.5), (9.5, 3), (16.5, 9.5)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        shell(rect(4.5, 11.5, 10, 4, min(S.R, 1))),
        line(seg(14.5, 14.5, 22, 14.5)),
        line(seg(6, 15.5, 6, 18.5)), line(seg(13, 15.5, 13, 18.5)), line(seg(20.5, 14.5, 20.5, 18.5)),
        line("M2 20.5C3.5 19.3 5 19.3 6.5 20.5S9.5 21.7 11 20.5S14 19.3 15.5 20.5S18.5 21.7 20 20.5L22 19.6"),
    ]


@icon("longhouse", CAT, "Long narrow longhouse with a curved barrel roof and a door at one end",
      tags=["long house", "iroquois longhouse", "communal house", "viking hall", "bark house", "hall"],
      aliases=["long-house"])
def _(S):
    return [
        shell("M2 21V14A10 7 0 0 1 22 14V21Z" if S.name == "line" else
              "M2 19V14A10 7 0 0 1 22 14V19A2 2 0 0 1 20 21H4A2 2 0 0 1 2 19Z"),
        detail("M2.4 13.5C5 11.2 8 10.5 12 10.5C16 10.5 19 11.2 21.6 13.5"),
        door(S, 4.5, 7.5, 15.5),
        win(11, 17.5, 2, 2), win(16, 17.5, 2, 2),
    ]


@icon("earth-sheltered-house", CAT, "House built into a grassy hill with a round door and round windows",
      tags=["earth house", "hobbit house", "underground house", "hill house", "earth berm", "green roof"],
      aliases=["earth-house"])
def _(S):
    return [
        line(seg(16, 3, 16, 6.5)),
        shell("M2 21C2 12.5 6.5 7.5 12.5 7.5C17.5 7.5 21 11 22 15V21Z"),
        detail(circle(9.5, 16.5, 2.75)),
        dot(15.5, 14.5, 1.25), dot(18.75, 17, 1.25),
    ]


@icon("shipping-container-house", CAT, "Home made of two ribbed shipping containers stacked offset",
      tags=["container home", "container house", "cargo container", "modular home", "prefab", "tiny house"],
      aliases=["container-home"])
def _(S):
    rr = L(S, 0, 2)
    return [
        shell(rect(8, 4, 14, 7.5, rr)),
        shell(rect(2, 13.5, 14, 7.5, rr)),
        detail(seg(11, 4, 11, 11.5)), detail(seg(14, 4, 14, 11.5)),
        win(16.5, 6.5, 3.5, 2.5),
        detail(seg(5, 13.5, 5, 21)), detail(seg(8, 13.5, 8, 21)),
        door(S, 10.5, 13.5, 16),
    ]


@icon("gatehouse", CAT, "Small gatehouse tower sitting over an arched gate passage",
      tags=["gate house", "gate lodge", "gateway", "lodge", "entrance", "porter's lodge"], aliases=["gate-lodge"])
def _(S):
    return [
        line(poly([(3.5, 8), (12, 2.5), (20.5, 8)], r=S.r)),
        shell(poly([(5.5, 21), (5.5, 6.7), (12, 2.5), (18.5, 6.7), (18.5, 21)], closed=True, r=S.r * 0.5)),
        win(11, 7.5, 2, 2.5),
        arch_door(8, 16, 12.5),
        line(seg(2, 21, 5.5, 21)), line(seg(18.5, 21, 22, 21)),
    ]


@icon("beach-hut", CAT, "Small striped beach hut with a peaked roof and double doors",
      tags=["bathing hut", "beach cabin", "seaside hut", "cabana", "changing hut", "beach house"],
      aliases=["bathing-hut"])
def _(S):
    return [
        shell(poly([(5, 21), (5, 8.5), (12, 3), (19, 8.5), (19, 21)], closed=True, r=S.r * 0.5)),
        mark(rect(6.75, 9, 1.75, 12)), mark(rect(15.5, 9, 1.75, 12)),
        detail(poly([(10, 21), (10, 12.5), (14, 12.5), (14, 21)], r=S.r * 0.4)),
        detail(seg(12, 12.5, 12, 21)),
    ]


@icon("boathouse", CAT, "Wooden boathouse at the water's edge with a big open door over the water",
      tags=["boat house", "boat shed", "marina", "dock", "lake house", "rowing club"], aliases=["boat-shed"])
def _(S):
    return [
        shell(poly([(3, 17.5), (3, 9), (12, 3.5), (21, 9), (21, 17.5), (17, 17.5), (17, 11.5), (7, 11.5), (7, 17.5)],
                   closed=True, r=S.r * 0.5)),
        line("M2 20.5C3.5 19.3 5 19.3 6.5 20.5S9.5 21.7 11 20.5S14 19.3 15.5 20.5S18.5 21.7 20 20.5L22 19.6"),
    ]


@icon("hanok", CAT, "Korean hanok house with a curved tiled roof sweeping up at the corners above a wooden porch",
      tags=["korean house", "traditional house", "giwa roof", "korea", "hanok village", "tiled roof"],
      aliases=["korean-house"])
def _(S):
    return [
        shell("M7 4.5H17C18 6.5 19.5 7.5 22 7C20.5 9.5 19 10.5 16 10.5H8C5 10.5 3.5 9.5 2 7C4.5 7.5 6 6.5 7 4.5Z"),
        line(seg(5.5, 11, 5.5, 17)), line(seg(18.5, 11, 18.5, 17)),
        shell(rect(8.5, 12, 7, 5, min(S.R, 1))),
        detail(seg(12, 12, 12, 17)),
        shell(rect(3, 18, 18, 3, min(S.R, 1.5))),
    ]


@icon("trullo", CAT, "Round stone trullo with a conical stacked-stone roof and a small finial",
      tags=["trulli", "stone hut", "apulia", "cone house", "dry stone", "rural house"], aliases=["trulli"])
def _(S):
    return [
        dot(12, 2.75, 1.25),
        shell(poly([(4, 21), (4, 13), (6.5, 13), (11, 5), (13, 5), (17.5, 13), (20, 13), (20, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(4, 13, 20, 13)),
        detail(seg(9.3, 9, 14.7, 9)),
        arch_door(10, 14, 15.5),
    ]


@icon("adobe-pueblo", CAT, "Stacked adobe pueblo dwellings with a ladder between levels",
      tags=["pueblo", "adobe house", "southwest", "mud brick", "taos", "terraced dwelling"], aliases=["pueblo"])
def _(S):
    pts = [(2, 21), (2, 14.5), (5, 14.5), (5, 9.5), (9, 9.5), (9, 4.5), (14, 4.5), (14, 9.5), (16, 9.5), (16, 14.5),
           (22, 14.5), (22, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.3)),
        line(seg(17.5, 14.5, 18.75, 6.5)), line(seg(20.5, 14.5, 21.75, 6.5)),
        line(seg(18.1, 10.5, 21.1, 10.5)),
        mark(rect(10.5, 16.5, 3, 4.5)), win(6.75, 11.5), win(10.5, 6.5),
    ]


@icon("cliff-dwelling", CAT, "Small stone rooms with doorways tucked under a curved cliff overhang",
      tags=["cliff house", "mesa verde", "ancestral pueblo", "cave dwelling", "canyon", "ruins"],
      aliases=["cliff-house"])
def _(S):
    return [
        shell("M2 2.5H22V9.5C18 8 13 8 8.5 10C6 11 4 12.5 2 14.5Z"),
        shell(rect(6, 15, 5.5, 6, min(S.R, 1))),
        shell(rect(13, 12, 6.5, 9, min(S.R, 1))),
        mark(rect(7.75, 17.5, 2, 3.5)), mark(rect(15.25, 14.5, 2, 3)),
    ]


@icon("canal-house", CAT, "Narrow canal house with a stepped gable and a hoist beam at the top",
      tags=["dutch house", "amsterdam house", "gabled house", "step gable", "merchant house", "netherlands"],
      aliases=["dutch-house"])
def _(S):
    pts = [(6.5, 21), (6.5, 10), (8, 10), (8, 7.5), (9.75, 7.5), (9.75, 5), (14.25, 5), (14.25, 7.5), (16, 7.5),
           (16, 10), (17.5, 10), (17.5, 21)]
    return [
        line(seg(12, 2, 12, 5)),
        shell(poly(pts, closed=True, r=S.r * 0.3)),
        win(11, 7), win(8.75, 12), win(13.25, 12), win(8.75, 15.5), win(13.25, 15.5),
        door(S, 10.75, 13.25, 18),
    ]


@icon("victorian-house", CAT, "Two-storey Victorian house with a round turret and steep gables",
      tags=["victorian", "queen anne house", "painted lady", "period house", "turret", "old house"],
      aliases=["queen-anne-house"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 8), (5.75, 2.5), (8.5, 8), (8.5, 11), (14.75, 4.5), (21, 11), (21, 21)],
                   closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
        detail(seg(3, 8, 8.5, 8)),
        win(4.75, 10.5, 2, 3), win(4.75, 15.5, 2, 3),
        dot(14.75, 9.5, 1.25),
        win(11.25, 13), win(16.25, 13),
        door(S, 13, 16.5, 16.5),
    ]


@icon("half-timbered-house", CAT, "Half-timbered house with pale walls crossed by dark timber beams",
      tags=["tudor house", "timber frame", "fachwerk", "medieval house", "cottage", "old house"],
      aliases=["tudor-house", "timber-frame-house"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 10), (12, 3.5), (21, 10), (21, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(3, 13.5, 21, 13.5)),
        detail(seg(8, 6.4, 8, 21)), detail(seg(16, 6.4, 16, 21)),
        detail(seg(8, 13.5, 12, 8.5)), detail(seg(12, 8.5, 16, 13.5)),
        detail(seg(12, 13.5, 12, 21)),
    ]


@icon("modern-house", CAT, "Flat-roofed modern house of stacked offset boxes with large glass windows",
      tags=["contemporary house", "modernist", "minimalist house", "cantilever", "villa", "architect house"],
      aliases=["contemporary-house"])
def _(S):
    return [
        shell(poly([(2, 21), (2, 12.5), (8, 12.5), (8, 4.5), (22, 4.5), (22, 12.5), (15.5, 12.5), (15.5, 21)],
                   closed=True, r=S.r * 0.5)),
        detail(seg(8, 12.5, 15.5, 12.5)),
        mark(rect(10.5, 7, 9, 3)),
        mark(rect(4.5, 15, 8.5, 3.5)),
    ]


@icon("brownstone", CAT, "Narrow brownstone row house with a tall stoop up to an arched front door",
      tags=["row house", "rowhouse", "stoop", "new york house", "townhouse", "city home"])
def _(S):
    return [
        line(seg(3, 2.5, 21, 2.5)),
        shell(poly([(4, 16), (4, 4.5), (20, 4.5), (20, 16), (15, 16), (17, 21), (7, 21), (9, 16)],
                   closed=True, r=S.r * 0.4)),
        win(6.5, 7), win(15.5, 7), win(6.5, 11.5), win(15.5, 11.5),
        arch_door(10, 14, 7.5, 16),
        detail(seg(8.2, 18.5, 15.8, 18.5)),
    ]


@icon("palace", CAT, "Grand palace with a central dome, rows of windows and a wing on each side",
      tags=["royal palace", "residence", "chateau", "king", "queen", "stately building"], aliases=["royal-palace"])
def _(S):
    return [
        line(seg(12, 2, 12, 4.5)),
        shell("M9 8.5A3 3 0 0 1 15 8.5Z" if S.name == "line" else "M9 8.5A3 3.5 0 0 1 15 8.5Z"),
        shell(poly([(2, 21), (2, 11.5), (8.5, 11.5), (8.5, 8.5), (15.5, 8.5), (15.5, 11.5), (22, 11.5), (22, 21)],
                   closed=True, r=S.r * 0.5)),
        *[win(x, y) for x in (4, 6.75, 15.25, 18) for y in (13.5, 17)],
        arch_door(10.25, 13.75, 14),
    ]


@icon("manor-house", CAT, "Country manor house with gabled wings at each end and chimneys",
      tags=["manor", "country house", "estate house", "hall", "gentry", "stately home"], aliases=["country-house"])
def _(S):
    return [
        line(seg(3.5, 3, 3.5, 7.2)), line(seg(20.5, 3, 20.5, 7.2)), line(seg(12, 5.5, 12, 9.5)),
        shell(poly([(2, 21), (2, 9.5), (5.5, 5), (9, 9.5), (15, 9.5), (18.5, 5), (22, 9.5), (22, 21)],
                   closed=True, r=S.r * 0.5)),
        detail(seg(9, 9.5, 9, 21)), detail(seg(15, 9.5, 15, 21)),
        win(4.5, 11), win(4.5, 15.5), win(17.5, 11), win(17.5, 15.5),
        door(S, 10.5, 13.5, 16), win(11, 12),
    ]


@icon("tulou", CAT, "Round earthen tulou with an inner courtyard, a row of small windows and a gate",
      tags=["hakka tulou", "earth building", "round house", "fujian", "communal house", "fortified house"],
      aliases=["earth-building"])
def _(S):
    w = (lambda x, y: win(x, y, 1.75, 2)) if S.name == "line" else (lambda x, y: dot(x + 0.875, y + 1, 1.1))
    return [
        shell("M3 8A9 4 0 0 1 21 8V17.5A9 3.5 0 0 1 3 17.5Z"),
        detail(ellipse(12, 8, 4.5, 1.75)),
        detail("M3 8A9 4 0 0 0 21 8"),
        w(5, 12.25), w(7.75, 13), w(14.5, 13), w(17.25, 12.25),
        arch_door(10.5, 13.5, 15),
    ]


@icon("japanese-castle", CAT, "Tiered Japanese castle with stacked curved roofs on a sloped stone base",
      tags=["castle", "japan", "fortress", "shogun", "samurai", "keep"], aliases=["tenshu"])
def _(S):
    def roof(y, half):
        return line(f"M{fmt(12 - half)} {fmt(y + 1.5)}Q{fmt(12 - half + 2.5)} {fmt(y + 1.5)} {fmt(12 - half + 3.5)} {fmt(y)}"
                    f"H{fmt(12 + half - 3.5)}Q{fmt(12 + half - 2.5)} {fmt(y + 1.5)} {fmt(12 + half)} {fmt(y + 1.5)}")
    return [
        shell(poly([(2.5, 21), (4.5, 16.5), (19.5, 16.5), (21.5, 21)], closed=True, r=S.r * 0.5)),
        shell(poly([(7, 16.5), (7, 13), (17, 13), (17, 16.5)], r=S.r * 0.5)),
        roof(9.5, 8),
        shell(poly([(9, 11), (9, 7.5), (15, 7.5), (15, 11)], r=S.r * 0.5)),
        line("M8 7Q10 7 10.8 4.5H13.2Q14 7 16 7"),
        line(seg(12, 2, 12, 4.5)),
    ]


@icon("windcatcher", CAT, "Flat-roofed house with a tall windcatcher tower with vent slots at the top",
      tags=["wind tower", "badgir", "malqaf", "passive cooling", "persian architecture", "ventilation tower"],
      aliases=["wind-tower", "badgir"])
def _(S):
    return [
        shell(poly([(2.5, 21), (2.5, 12), (13, 12), (13, 3), (21, 3), (21, 21)], closed=True, r=S.r * 0.5)),
        mark(rect(15, 5, 1.5, 5)), mark(rect(17.5, 5, 1.5, 5)),
        win(5, 14.5), win(9, 14.5),
        door(S, 15, 18.5, 15),
    ]


@icon("kasbah", CAT, "Fortified mud-brick kasbah with tapering corner towers and small windows",
      tags=["ksar", "casbah", "citadel", "morocco", "mud brick", "fortress"], aliases=["casbah", "ksar"])
def _(S):
    return [
        shell(poly([(2, 21), (3.5, 4), (8, 4), (8.3, 9), (15.7, 9), (16, 4), (20.5, 4), (22, 21)], closed=True, r=S.r * 0.3)),
        win(4.75, 7), win(17.25, 7), win(4.5, 12), win(17.5, 12),
        win(11, 11.5),
        arch_door(10, 14, 15.5),
    ]


@icon("raised-granary", CAT, "Small granary on mushroom-shaped staddle stones under a pitched roof",
      tags=["granary", "staddle stones", "horreo", "grain store", "barn", "farm"], aliases=["granary-on-stilts"])
def _(S):
    return [
        line(poly([(3, 9), (12, 3), (21, 9)], r=S.r)),
        shell(poly([(5, 13.5), (5, 7.7), (12, 3), (19, 7.7), (19, 13.5)], closed=True, r=S.r * 0.5)),
        *[solid(f"M{fmt(x - 2)} 16.75A2 1.75 0 0 1 {fmt(x + 2)} 16.75Z") for x in (6.5, 12, 17.5)],
        *[line(seg(x, 16.75, x, 21)) for x in (6.5, 12, 17.5)],
        detail(seg(10, 10, 14, 10)),
    ]


@icon("hogan", CAT, "Octagonal log hogan with a low domed earth roof and a single door",
      tags=["navajo hogan", "log house", "earth lodge", "dwelling", "roundhouse", "native home"])
def _(S):
    return [
        shell("M3 21V13.5H3.5C5 10 8 8 12 8C16 8 19 10 20.5 13.5H21V21Z"),
        detail(seg(3, 13.5, 21, 13.5)),
        detail(seg(7.5, 13.5, 7.5, 21)), detail(seg(16.5, 13.5, 16.5, 21)),
        door(S, 10.25, 13.75, 16),
    ]


@icon("art-deco-skyscraper", CAT, "Art deco tower stepping back in tiers to a slender spire, with vertical stripes",
      tags=["art deco", "1930s tower", "stepped skyscraper", "setback tower", "high-rise", "landmark"],
      aliases=["deco-tower"])
def _(S):
    pts = [(5.5, 21), (5.5, 12), (7.25, 12), (7.25, 8.5), (9, 8.5), (9, 5.5), (15, 5.5), (15, 8.5), (16.75, 8.5),
           (16.75, 12), (18.5, 12), (18.5, 21)]
    return [
        line(seg(12, 1.5, 12, 5.5)),
        shell(poly(pts, closed=True, r=S.r * 0.3)),
        detail(seg(10.25, 8.5, 10.25, 21)), detail(seg(13.75, 8.5, 13.75, 21)),
    ]


@icon("twisting-skyscraper", CAT, "Tall skyscraper whose floors rotate as it rises so its outline twists",
      tags=["twisted tower", "spiral tower", "rotating tower", "modern skyscraper", "high-rise", "futuristic"],
      aliases=["twisted-tower"])
def _(S):
    return [
        shell("M7 21C6 15 9.5 8.5 8 2.5H16C17.5 8.5 14 15 17 21Z" if S.name == "line" else
              "M7 21C6 15 9.5 8.5 8 3.5Q7.8 2.5 8.8 2.5H15.2Q16.2 2.5 16 3.5C17.5 8.5 14 15 17 21Z"),
        detail("M10.5 21C8.5 14.5 14.5 9 12.5 2.5"),
        detail("M8.4 10.5L15.1 8.5"),
        detail("M8.1 15.5L15.2 16.5"),
    ]


@icon("brutalist-building", CAT, "Heavy concrete brutalist block with recessed windows and an overhanging upper floor",
      tags=["brutalism", "concrete building", "modernist", "tower block", "civic building", "raw concrete"])
def _(S):
    return [
        shell(poly([(5, 21), (5, 11.5), (2, 11.5), (2, 3), (22, 3), (22, 11.5), (19, 11.5), (19, 21)],
                   closed=True, r=S.r * 0.3)),
        *[mark(rect(x, 5.5, 2.5, 3.5)) for x in (4.5, 8.5, 13, 17)],
        detail(seg(5, 11.5, 19, 11.5)),
        *[mark(rect(x, 14, 2.5, 2.5)) for x in (7.5, 13.5)],
        mark(rect(10.5, 17, 3, 4)),
    ]


@icon("stupa", CAT, "Buddhist stupa with a bell-shaped dome on a stepped base and a tiered spire",
      tags=["chorten", "dagoba", "buddhist shrine", "reliquary", "pagoda", "temple"], aliases=["chorten", "dagoba"])
def _(S):
    return [
        line(seg(12, 2, 12, 7)),
        line(seg(10.25, 4.5, 13.75, 4.5)),
        shell(rect(10, 7, 4, 2.5, min(S.R, 0.5))),
        shell("M5.5 16C5.5 12 8.5 9.5 12 9.5C15.5 9.5 18.5 12 18.5 16Z"),
        shell(poly([(3, 21), (3, 18), (21, 18), (21, 21)], closed=True, r=S.r * 0.5)),
    ]


@icon("gurdwara", CAT, "Gurdwara with a ribbed onion dome over an arched door beside a tall triangular flag",
      tags=["sikh temple", "sikh", "worship", "religion", "nishan sahib", "langar"], aliases=["sikh-temple"])
def _(S):
    return [
        line(seg(20.5, 2, 20.5, 21)),
        solid(poly([(20.5, 2), (20.5, 7), (16.5, 4.5)], closed=True)),
        line(seg(9.5, 2, 9.5, 4)),
        shell("M9.5 4C11.5 6 13.5 7 13.5 9.5V11H5.5V9.5C5.5 7 7.5 6 9.5 4Z"),
        detail(seg(9.5, 6.5, 9.5, 11)),
        shell(rect(2.5, 13, 14, 8, min(S.R, 2))),
        arch_door(7.75, 11.25, 15.5),
    ]
