"""TypeIcon Core: architecture (batch 003).

Street furniture, shop fronts, vaults and ceilings, monuments and vernacular buildings, drawn front-on on
the ground line y = 21 (outer edge 22) in the same language as sets/architecture_001.py: closed walls are
shells, doors and trim are details, and small solid blocks (`win`, `mark`) are knocked out of Filled walls.
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


def union_d(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


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


def shop(S, top=3.0, eave=9.0):
    """Shop front: an awning with two stripe seams over the shop body (walls x 5-19).

    The sign symbol sits inside the body, roughly x 8-16 and y 11.5-18.5.
    """
    return [
        shell(poly([(3, eave), (5, top), (19, top), (21, eave)], closed=True, r=S.r)),
        detail(seg(9.67, top, 9, eave)), detail(seg(14.33, top, 15, eave)),
        shell(poly([(5, eave), (5, 21), (19, 21), (19, eave)], closed=True, r=S.r)),
        detail(seg(3, eave, 21, eave)),
    ]


# ============================================================================ street furniture

@icon("tree-grate", CAT, "Street tree standing in a square metal grate with slots set into the pavement",
      tags=["tree guard", "tree pit", "pavement", "sidewalk", "street tree", "grating"])
def _(S):
    return [
        shell(circle(12, 7, 5)),
        line(seg(12, 12, 12, 17.5)),
        shell(poly([(2, 18), (6, 15), (18, 15), (22, 18), (18, 21), (6, 21)], closed=True, r=S.r * 0.3)),
        detail(seg(5.5, 18, 9.5, 18)), detail(seg(14.5, 18, 18.5, 18)),
    ]


@icon("road-barrier", CAT, "Striped barrier board standing on two legs across a road",
      tags=["roadblock", "road closed", "barricade", "roadworks", "detour", "traffic"])
def _(S):
    return [
        shell(rect(2, 6, 20, 6, min(S.R, 2))),
        detail(seg(8, 6, 5, 12)), detail(seg(13.5, 6, 10.5, 12)), detail(seg(19, 6, 16, 12)),
        line(seg(5, 12, 3, 21)), line(seg(5, 12, 7, 21)),
        line(seg(19, 12, 17, 21)), line(seg(19, 12, 21, 21)),
    ]


@icon("crowd-barrier", CAT, "Portable metal fence panel of vertical bars standing on flat feet",
      tags=["crowd control", "barricade", "event fence", "queue barrier", "police barrier", "fencing"])
def _(S):
    return [
        shell(rect(3, 4, 18, 13, min(S.R, 2))),
        *[detail(seg(x, 4, x, 17)) for x in (7.5, 12, 16.5)],
        line(seg(6, 17, 6, 21)), line(seg(18, 17, 18, 21)),
        line(seg(3, 21, 9, 21)), line(seg(15, 21, 21, 21)),
    ]


@icon("flagpole", CAT, "Tall flagpole on a stepped base with a blank flag and a ball on top",
      tags=["flag pole", "flagstaff", "mast", "flag", "memorial", "ceremony"], aliases=["flagstaff"])
def _(S):
    return [
        dot(7, 2.75, 1.5),
        line(seg(7, 4.5, 7, 18.5)),
        shell(rect(8, 5, 11, 7, min(S.R, 1.5))),
        shell(poly([(3.5, 21), (4.5, 18.5), (9.5, 18.5), (10.5, 21)], closed=True, r=S.r * 0.5)),
    ]


@icon("hand-pump", CAT, "Cast iron hand water pump with a long curved handle and a downward spout",
      tags=["water pump", "village pump", "well pump", "pitcher pump", "water", "rural"])
def _(S):
    return [
        shell(rect(9.5, 7, 5, 12, min(S.R, 1.5))),
        line(seg(8, 7, 16, 7)),
        line("M14.5 7C16.5 5 18.5 3.5 21.5 3"),
        line(poly([(9.5, 10.5), (5, 10.5), (5, 13.5)], r=S.r * 0.5)),
        dot(5, 17, 1.25),
        line(seg(7.5, 21, 16.5, 21)),
        line(seg(12, 19, 12, 21)),
    ]


@icon("public-bookcase", CAT, "Little house-shaped book box on a post with books behind its door",
      tags=["little free library", "book exchange", "book box", "street library", "book swap", "free books"],
      aliases=["book-exchange"])
def _(S):
    return [
        shell(poly([(4.5, 9.5), (12, 3), (19.5, 9.5), (19.5, 16), (4.5, 16)], closed=True, r=S.r * 0.5)),
        detail(seg(8.5, 10, 8.5, 13.5)), detail(seg(11.5, 10, 11.5, 13.5)), detail(seg(14.5, 10.5, 15.8, 13.5)),
        line(seg(12, 16, 12, 21)),
        line(seg(8.5, 21, 15.5, 21)),
    ]


@icon("picnic-shelter", CAT, "Open roofed shelter on posts over a picnic table",
      tags=["pavilion", "picnic area", "gazebo", "park shelter", "covered seating", "rest area"])
def _(S):
    return [
        shell(poly([(3, 9), (12, 3.5), (21, 9)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        line(seg(4.5, 9, 4.5, 21)), line(seg(19.5, 9, 19.5, 21)),
        line(seg(7.5, 14.5, 16.5, 14.5)),
        line(seg(9.5, 14.5, 8.5, 21)), line(seg(14.5, 14.5, 15.5, 21)),
    ]


@icon("beach-shower", CAT, "Tall outdoor shower post with a head at the top spraying water and a tap below",
      tags=["outdoor shower", "rinse", "beach", "pool shower", "shower", "seaside"])
def _(S):
    head = L(S, "M13 6.5H20L18.5 9H14.5Z", "M13 6.5H20A3.5 2.5 0 0 1 13 6.5Z")
    return [
        line(poly([(8, 21), (8, 3.5), (16.5, 3.5), (16.5, 6.5)], r=S.r)),
        shell(head),
        dot(14.5, 12.5, 1.1), dot(18.5, 12.5, 1.1), dot(16.5, 15.5, 1.1), dot(14.5, 18.5, 1.1), dot(18.5, 18.5, 1.1),
        line(seg(8, 16, 11.5, 16)),
        line(seg(5, 21, 11, 21)),
    ]


@icon("wrought-iron-gate", CAT, "Double iron gate of vertical bars with an arched top between two stone pillars",
      tags=["iron gate", "entrance gate", "park gate", "estate gate", "railings", "ornamental gate"])
def _(S):
    return [
        dot(3.5, 3.25, 1.5), dot(20.5, 3.25, 1.5),
        shell(rect(2, 5.5, 3, 15.5, min(S.R, 1))),
        shell(rect(19, 5.5, 3, 15.5, min(S.R, 1))),
        line("M8 10Q12 4.5 16 10"),
        line(seg(9, 8.9, 9, 21)), line(seg(12, 7.25, 12, 21)), line(seg(15, 8.9, 15, 21)),
        line(seg(8, 17, 16, 17)),
    ]


# ============================================================================ shop fronts

@icon("jewelry-store", CAT, "Shop front with an awning and a cut diamond sign",
      tags=["jeweller", "jewelry shop", "jewellery", "diamonds", "rings", "gems"],
      aliases=["jewellery-shop", "jeweler"])
def _(S):
    return [
        *shop(S),
        detail(poly([(9.5, 12.5), (14.5, 12.5), (16.5, 14.75), (12, 19), (7.5, 14.75)], closed=True, r=S.r * 0.3)),
        detail(seg(7.5, 14.75, 16.5, 14.75)),
    ]


@icon("toy-store", CAT, "Shop front with an awning and a teddy bear head sign",
      tags=["toy shop", "toys", "teddy bear", "kids", "games", "children"], aliases=["toy-shop"])
def _(S):
    bear = path_to_d(D(U(P(circle(12, 15.5, 3.5)), P(circle(9.25, 12.75, 1.3)), P(circle(14.75, 12.75, 1.3))),
                         P(ellipse(12, 17, 1.6, 1.2))))
    return [
        *shop(S),
        mark(bear),
    ]


@icon("clothing-store", CAT, "Shop front with an awning and a clothes hanger sign",
      tags=["clothes shop", "fashion", "boutique", "apparel", "garments", "hanger"],
      aliases=["clothes-shop"])
def _(S):
    return [
        *shop(S),
        detail(poly([(12, 14.5), (17, 18.5), (7, 18.5)], closed=True, r=S.r * 0.5)),
        detail("M10.5 12.5A1.5 1.5 0 1 1 12 14V14.5"),
    ]


@icon("shoe-store", CAT, "Shop front with an awning and a shoe sign",
      tags=["shoe shop", "footwear", "shoes", "sneakers", "boots", "cobbler"], aliases=["shoe-shop"])
def _(S):
    shoe = "M7.5 12.5H10.5L11.5 14.5C13.5 15 15.5 15.3 16.5 16.3V18.5H7.5Z"
    return [
        *shop(S),
        mark(shoe),
    ]


@icon("electronics-store", CAT, "Shop front with an awning and an electric plug sign",
      tags=["electronics shop", "electrical", "appliances", "gadgets", "tech store", "plug"],
      aliases=["electronics-shop"])
def _(S):
    return [
        *shop(S),
        detail(seg(10.5, 11.5, 10.5, 13.5)), detail(seg(13.5, 11.5, 13.5, 13.5)),
        mark(rect(8.5, 13.5, 7, 4, 1)),
        detail(seg(12, 17.5, 12, 21)),
    ]


@icon("music-store", CAT, "Shop front with an awning and a guitar sign",
      tags=["music shop", "instruments", "guitar", "records", "musical instruments", "music"],
      aliases=["music-shop"])
def _(S):
    body = union_d(circle(10.25, 16.75, 2.25), circle(12.25, 14.75, 1.75))
    return [
        *shop(S),
        mark(body),
        detail(seg(12.5, 14.5, 16.5, 10.5)),
    ]


@icon("tailor-shop", CAT, "Shop front with an awning and a needle and thread sign",
      tags=["tailor", "alterations", "dressmaker", "sewing", "seamstress", "bespoke"])
def _(S):
    return [
        *shop(S),
        detail(seg(8, 19, 15.5, 11.5)),
        detail("M15 12.5Q18.5 16 15.5 19"),
    ]


# ============================================================================ entertainment and landmarks

def sparkle(cx, cy, r):
    """Four-point sparkle star as a solid mark."""
    k = r * 0.3
    return mark(poly([(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k), (cx, cy + r), (cx - k, cy + k),
                      (cx - r, cy), (cx - k, cy - k)], closed=True))


@icon("nightclub", CAT, "Windowless club building with a disco ball hanging above the door",
      tags=["club", "disco", "dance club", "nightlife", "party", "night club"], aliases=["disco-club"])
def _(S):
    ball = path_to_d(D(P(circle(12, 9.5, 3.25)), ST(seg(8, 9.5, 16, 9.5), 1.2), ST(seg(12, 5, 12, 14), 1.2)))
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(12, 3, 12, 6.25)),
        mark(ball),
        sparkle(7, 8, 1.75), sparkle(17, 11, 1.75),
        door(S, 9.5, 14.5, 15.5),
    ]


@icon("zoo", CAT, "Entrance gate with a sign bar across the top and a giraffe head peeking over it",
      tags=["zoological garden", "wildlife park", "animal park", "safari park", "animals", "menagerie"],
      aliases=["zoological-garden"])
def _(S):
    head = "M13.5 13L13.75 7.25L9.75 7.75C8.5 7.9 8 7 8.6 6.1L9.6 4.8L14.5 3.6C16.2 3.3 17.1 4.2 17.1 5.5L17 13Z"
    head = "M13.5 12L13.75 7.25L9.75 7.75C8.5 7.9 8 7 8.6 6.1L9.6 4.8L14.5 3.6C16.2 3.3 17.1 4.2 17.1 5.5L17 12Z"
    return [
        shell(union_d(head, rect(2.5, 11, 19, 3.5, min(S.R, 1.5)))),
        line(seg(14.25, 3.7, 14, 1.8)), line(seg(16.25, 3.9, 17, 2)),
        line(seg(4.5, 14.5, 4.5, 21)), line(seg(19.5, 14.5, 19.5, 21)),
        line(seg(4.5, 17.5, 19.5, 17.5)),
        line(seg(9.5, 17.5, 9.5, 21)), line(seg(14.5, 17.5, 14.5, 21)),
    ]


@icon("rock-cut-temple", CAT, "Temple front with a pediment and columns carved into a cliff face",
      tags=["cliff temple", "carved temple", "rock temple", "ancient", "facade", "archaeology"])
def _(S):
    cliff = poly([(2, 21), (2, 6), (5, 3.5), (9, 4.5), (13, 2.5), (17, 4), (22, 3), (22, 21)], closed=True, r=S.r * 0.5)
    return [
        shell(cliff),
        detail(poly([(6, 11.5), (12, 8), (18, 11.5)], closed=True, r=S.r * 0.3)),
        *[detail(seg(x, 14, x, 21)) for x in (7.5, 12, 16.5)],
    ]


@icon("rock-cut-dwelling", CAT, "Cone-shaped rock pinnacle with a door and small windows carved into it",
      tags=["cave house", "fairy chimney", "troglodyte", "rock house", "cave dwelling", "cappadocia"],
      aliases=["fairy-chimney"])
def _(S):
    cone = L(S, "M4 21C6 14 8.5 7 12 2.5C15.5 7 18 14 20 21Z",
             "M4 21C6 14 8.5 7.5 10.5 4A1.8 1.8 0 0 1 13.5 4C15.5 7.5 18 14 20 21Z")
    return [
        shell(cone),
        win(11, 8.5, 2, 2), win(8.5, 13, 2, 2), win(13.5, 13, 2, 2),
        arch_door(10, 14, 17),
    ]


# ============================================================================ vaults and ceilings

@icon("coffered-ceiling", CAT, "Ceiling seen from below as a grid of recessed square panels",
      tags=["coffers", "caissons", "lacunar", "ceiling panels", "waffle ceiling", "interior"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)),
        detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15)),
        *[win(x - 1, y - 1, 2, 2) for x in (6, 12, 18) for y in (6, 12, 18)],
    ]


@icon("barrel-vault", CAT, "Half-cylinder vaulted ceiling in perspective with evenly spaced arched ribs",
      tags=["tunnel vault", "vault", "arched ceiling", "wagon vault", "romanesque", "vaulting"],
      aliases=["tunnel-vault"])
def _(S):
    outer = L(S, "M3 21V12A9 9 0 0 1 21 12V21Z", "M3 19V12A9 9 0 0 1 21 12V19A2 2 0 0 1 19 21H5A2 2 0 0 1 3 19Z")
    return [
        shell(outer),
        detail("M7 21V13A5 5 0 0 1 17 13V21"),
        detail("M10.5 21V14.5A1.5 1.5 0 0 1 13.5 14.5V21"),
    ]


@icon("ribbed-vault", CAT, "Square vault bay seen from below with ribs crossing diagonally to a central boss",
      tags=["rib vault", "gothic vault", "groin vault", "cross vault", "cathedral ceiling", "vaulting"],
      aliases=["rib-vault"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(3, 3, 21, 21)), detail(seg(21, 3, 3, 21)),
        detail("M3 3Q12 8 21 3"), detail("M3 21Q12 16 21 21"),
        detail("M3 3Q8 12 3 21"), detail("M21 3Q16 12 21 21"),
        dot(12, 12, 2.25),
    ]


@icon("dome-oculus", CAT, "Dome seen from directly below with a ring of coffers around a round open centre",
      tags=["oculus", "dome", "rotunda", "coffered dome", "skylight", "pantheon"])
def _(S):
    coffers = []
    for k in range(8):
        a0, a1 = 45 * k + 8, 45 * k + 37
        pts = [pt_on_((12, 12), 4.75, a0), pt_on_((12, 12), 6.75, a0), pt_on_((12, 12), 6.75, a1),
               pt_on_((12, 12), 4.75, a1)]
        coffers.append(mark(poly(pts, closed=True, r=L(S, 0, 0.9))))
    return [
        shell(circle(12, 12, 9.5)),
        *coffers,
        detail(circle(12, 12, 2.25)),
    ]


# ============================================================================ building forms

@icon("facade-louvers", CAT, "Building front with deep horizontal sun-shading fins across every floor",
      tags=["louvres", "brise soleil", "sun shading", "fins", "sunshade", "facade"],
      aliases=["brise-soleil", "facade-louvres"])
def _(S):
    parts = [shell(rect(5, 3, 14, 18, min(S.R, 2)))]
    for y in (7.5, 12, 16.5):
        parts += [detail(seg(5, y, 19, y)), line(seg(2, y, 5, y)), line(seg(19, y, 22, y))]
    return parts


@icon("cantilevered-building", CAT, "Building whose long upper block juts far out beyond its narrow base",
      tags=["cantilever", "overhang", "modern architecture", "cantilevered", "floating", "structure"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 4), (21, 4), (21, 11.5), (10, 11.5), (10, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(6, 7.75, 18, 7.75)),
        win(5.25, 14, 2.5, 4),
    ]


@icon("rooftops", CAT, "Cluster of overlapping pitched rooftops at different heights with chimneys",
      tags=["roofs", "old town", "townscape", "houses", "neighbourhood", "skyline"],
      aliases=["roofscape"])
def _(S):
    a = poly([(2, 21), (2, 13.5), (6.5, 9), (11, 13.5), (11, 21)], closed=True)
    b = poly([(7.5, 21), (7.5, 10), (12.5, 5), (17.5, 10), (17.5, 21)], closed=True)
    c = poly([(13.5, 21), (13.5, 14), (17.75, 9.75), (22, 14), (22, 21)], closed=True)
    ch1 = rect(14.5, 3.5, 2, 4)
    ch2 = rect(3, 10, 2, 3)
    outline = path_to_d(U(P(a), P(b), P(c), P(ch1), P(ch2)))
    return [
        shell(outline),
        detail(seg(6.5, 9, 11, 13.5)),
        detail(seg(13.5, 14, 17.75, 9.75)),
        win(5.25, 15.5, 2.5, 2.5), win(16.5, 16, 2.5, 2.5), win(11, 16.5, 2, 4.5),
    ]


# ============================================================================ street furniture 2

@icon("street-planter", CAT, "Large square concrete planter box holding a small round tree",
      tags=["planter", "planter box", "street tree", "urban greenery", "tree planter", "streetscape"])
def _(S):
    return [
        shell(circle(12, 7, 4.5)),
        line(seg(12, 11.5, 12, 14)),
        shell(poly([(4, 14), (20, 14), (19, 21), (5, 21)], closed=True, r=S.r * 0.5)),
    ]


@icon("lamppost-banner", CAT, "Street lamp post with two hanging fabric banners on arms",
      tags=["street banner", "lamp post", "pole banner", "street light", "festival", "wayfinding"])
def _(S):
    return [
        shell(poly([(9.5, 5), (10.5, 2), (13.5, 2), (14.5, 5)], closed=True, r=S.r * 0.4)),
        line(seg(12, 5, 12, 21)),
        line(seg(2.5, 6.5, 21.5, 6.5)),
        shell(poly([(3, 8), (7, 8), (7, 17), (5, 15), (3, 17)], closed=True, r=S.r * 0.4)),
        shell(poly([(17, 8), (21, 8), (21, 17), (19, 15), (17, 17)], closed=True, r=S.r * 0.4)),
        line(seg(9, 21, 15, 21)),
    ]


@icon("bottle-bank", CAT, "Dome-shaped glass recycling container with round bottle holes around its top",
      tags=["bottle bin", "glass recycling", "recycling bank", "bottle igloo", "glass bank", "recycling point"])
def _(S):
    outer = L(S, "M3 21V14A9 7.5 0 0 1 21 14V21Z", "M3 19V14A9 7.5 0 0 1 21 14V19A2 2 0 0 1 19 21H5A2 2 0 0 1 3 19Z")
    bottle = "M11.25 13H12.75V14.5L14 15.75V20H10V15.75L11.25 14.5Z"
    return [
        shell(outer),
        detail(circle(7.5, 12.5, 1)), detail(circle(12, 9.75, 1)), detail(circle(16.5, 12.5, 1)),
        mark(bottle),
    ]


@icon("tower-viewer", CAT, "Coin-operated binocular viewer with two big lenses on a post",
      tags=["coin binoculars", "viewpoint", "telescope", "scenic lookout", "observation deck", "sightseeing"],
      aliases=["coin-binoculars"])
def _(S):
    return [
        shell(rect(3.5, 4, 17, 8, S.R)),
        detail(circle(8.5, 8, 2)), detail(circle(15.5, 8, 2)),
        line(seg(12, 12, 12, 19)),
        shell(rect(8.5, 19, 7, 2, min(S.R, 1))),
    ]


@icon("newspaper-box", CAT, "Metal newspaper vending box on short legs with a front window and a coin slot on top",
      tags=["news box", "newspaper vending", "news rack", "honor box", "street box", "newspapers"],
      aliases=["newspaper-vending-box"])
def _(S):
    return [
        solid(rect(13, 2.5, 4, 2)),
        shell(rect(5, 4.5, 14, 12.5, min(S.R, 2))),
        detail(rect(8, 7.5, 8, 4.5)),
        detail(seg(10, 14.5, 14, 14.5)),
        line(seg(7, 17, 7, 21)), line(seg(17, 17, 17, 21)),
    ]


# ============================================================================ shrines and monuments

@icon("spirit-house", CAT, "Small ornate house shrine with a steep pointed roof on a single pedestal",
      tags=["san phra phum", "shrine", "offering house", "thai shrine", "house shrine", "altar"])
def _(S):
    roof = [(12, 2), (18.5, 9.5), (20.5, 8.5), (19.5, 11), (4.5, 11), (3.5, 8.5), (5.5, 9.5)]
    return [
        shell(poly(roof, closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        shell(rect(7, 11, 10, 5, min(S.R, 1))),
        detail(seg(12, 12.5, 12, 16)),
        line(seg(12, 16, 12, 19)),
        shell(rect(8, 19, 8, 2, min(S.R, 1))),
    ]


@icon("columbarium", CAT, "Wall of square urn niches in a grid, each with a small plaque, under a low gable",
      tags=["urn wall", "niche wall", "cremation", "memorial wall", "cemetery", "funeral"])
def _(S):
    return [
        shell(poly([(2, 7.5), (12, 3), (22, 7.5)], closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        shell(rect(3, 7.5, 18, 13.5, min(S.R, 2))),
        detail(seg(9, 7.5, 9, 21)), detail(seg(15, 7.5, 15, 21)), detail(seg(3, 14.25, 21, 14.25)),
        *[win(x - 1.5, y - 0.75, 3, 1.5) for x in (6, 12, 18) for y in (11, 17.75)],
    ]


@icon("eternal-flame", CAT, "Shallow bowl on a stone pedestal holding a steady flame",
      tags=["memorial flame", "remembrance", "war memorial", "torch", "commemoration", "flame"])
def _(S):
    flame = ("M12 2.5C14.5 5 16 7.2 16 9.5C16 10.1 15.9 10.6 15.7 11H8.3C8.1 10.6 8 10.1 8 9.5"
             "C8 7.2 9.5 5 12 2.5Z")
    bowl = L(S, "M4.5 12H19.5L16.5 16.5H7.5Z", "M4.5 12H19.5C19 15 16 16.5 12 16.5C8 16.5 5 15 4.5 12Z")
    return [
        shell(flame),
        shell(bowl),
        line(seg(12, 16.5, 12, 18.5)),
        shell(rect(7.5, 18.5, 9, 2.5, min(S.R, 1))),
    ]


@icon("lion-statue", CAT, "Seated guardian lion statue on a rectangular pedestal",
      tags=["guardian lion", "stone lion", "statue", "foo dog", "sculpture", "monument"])
def _(S):
    mane = []
    for k in range(20):
        rr = 5 if k % 2 == 0 else 4
        mane.append(pt_on_((12, 7), rr, -90 + k * 18))
    return [
        shell(poly(mane, closed=True, r=L(S, 0, 0.6)), stroke_miterlimit="2"),
        dot(10.4, 7, 0.9), dot(13.6, 7, 0.9),
        shell(poly([(8.5, 12), (15.5, 12), (17, 16), (7, 16)], closed=True, r=S.r * 0.4)),
        detail(seg(12, 13.5, 12, 16)),
        shell(rect(5, 16, 14, 5, min(S.R, 2))),
    ]


@icon("stele", CAT, "Tall upright stone slab with a rounded top and rows of carved inscription",
      tags=["stela", "inscribed stone", "monolith", "ancient monument", "tablet", "archaeology"],
      aliases=["stela"])
def _(S):
    slab = L(S, "M6.5 21V7.5A5.5 5.5 0 0 1 17.5 7.5V21Z",
             "M6.5 19V7.5A5.5 5.5 0 0 1 17.5 7.5V19A2 2 0 0 1 15.5 21H8.5A2 2 0 0 1 6.5 19Z")
    return [
        shell(slab),
        *[detail(seg(9.5, y, 14.5, y)) for y in (8, 11.5, 15, 18)],
    ]


@icon("acropolis", CAT, "Columned temple on top of a steep flat-topped rocky hill",
      tags=["citadel", "hilltop temple", "ancient greece", "parthenon", "classical", "ruins"])
def _(S):
    return [
        shell(poly([(5, 8.5), (12, 4), (19, 8.5)], closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        *[line(seg(x, 8.5, x, 13)) for x in (7, 12, 17)],
        shell(poly([(2, 21), (4.5, 14), (19.5, 14), (22, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(7, 17.5, 17, 17.5)),
    ]


@icon("motte-and-bailey", CAT, "Small wooden tower on a steep round mound beside a fenced yard",
      tags=["motte", "bailey", "norman castle", "earthwork castle", "keep", "medieval"])
def _(S):
    return [
        shell(poly([(6.5, 13), (6.5, 7), (9, 4.5), (11.5, 7), (11.5, 13)], closed=True, r=S.r * 0.4)),
        shell("M2 21C4 21 5 13.5 9 13.5C13 13.5 14 21 16 21Z"),
        shell(poly([(15, 21), (15, 15.5), (16.75, 13.5), (18.5, 15.5), (20.25, 13.5), (22, 15.5), (22, 21)],
                   closed=True, r=S.r * 0.3)),
        detail(seg(18.5, 15.5, 18.5, 21)),
    ]


@icon("clapper-bridge", CAT, "Flat stone slabs resting on stacked stone piers across a stream",
      tags=["stone bridge", "slab bridge", "footbridge", "ancient bridge", "stream crossing", "moorland"])
def _(S):
    return [
        shell(rect(2, 6.5, 20, 3.5, min(S.R, 1))),
        detail(seg(12, 6.5, 12, 10)),
        shell(rect(5, 10, 4.5, 6.5, min(S.R, 1))), shell(rect(14.5, 10, 4.5, 6.5, min(S.R, 1))),
        detail(seg(5, 13.25, 9.5, 13.25)), detail(seg(14.5, 13.25, 19, 13.25)),
        line("M2 20.5Q4 18.75 6 20.5T10 20.5T14 20.5T18 20.5T22 20.5"),
    ]


@icon("bicycle-shelter", CAT, "Curved roof shelter on posts over a parked bicycle",
      tags=["bike shelter", "bike parking", "cycle shelter", "bike rack", "bicycle parking", "cycle park"],
      aliases=["bike-shelter"])
def _(S):
    return [
        shell(L(S, "M2 8.5Q12 1 22 8.5L22 10Q12 3.5 2 10Z", "M2 8.5Q12 1 22 8.5V9.25Q12 3.5 2 9.25Z")),
        line(seg(2.75, 9, 2.75, 21)), line(seg(21.25, 9, 21.25, 21)),
        detail(circle(8, 18, 2.5)), detail(circle(16, 18, 2.5)),
        detail(poly([(8, 18), (10.5, 13.5), (15, 13.5), (16, 18)], r=S.r * 0.5)),
    ]


@icon("woodshed", CAT, "Open lean-to shelter stacked full of round firewood logs",
      tags=["log store", "firewood", "wood store", "lean-to", "logs", "wood pile"], aliases=["log-store"])
def _(S):
    logs = [(7.5, 18.75), (12, 18.75), (16.5, 18.75), (9.75, 14.85), (14.25, 14.85), (12, 10.95)]
    return [
        line(poly([(2, 7.5), (22, 3.5)])),
        line(seg(3.5, 7.2, 3.5, 21)), line(seg(20.5, 3.8, 20.5, 21)),
        *[dot(x, y, 1.75) for x, y in logs],
    ]


@icon("bicycle-shop", CAT, "Shop front with an awning and a bicycle sign",
      tags=["bike shop", "cycle shop", "bike repair", "bicycles", "cycling", "bike store"],
      aliases=["bike-shop"])
def _(S):
    return [
        *shop(S),
        detail(circle(9, 17, 1.75)), detail(circle(15, 17, 1.75)),
        detail(poly([(9, 17), (11, 13), (14, 13), (15, 17)], r=S.r * 0.3)),
    ]


@icon("candy-store", CAT, "Shop front with a striped awning and a wrapped sweet sign",
      tags=["sweet shop", "confectionery", "candy shop", "sweets", "lollies", "confectioner"],
      aliases=["sweet-shop"])
def _(S):
    sweet = union_d(ellipse(12, 15.5, 2.75, 2.25),
                    poly([(10, 15.5), (7, 13), (7, 18)], closed=True),
                    poly([(14, 15.5), (17, 13), (17, 18)], closed=True))
    return [
        *shop(S),
        mark(sweet),
    ]


@icon("wine-shop", CAT, "Shop front with an awning and a wine bottle and glass sign",
      tags=["wine store", "liquor store", "off licence", "bottle shop", "wine merchant", "vintner"],
      aliases=["wine-store"])
def _(S):
    bottle = "M9 11.5H10.5V13.5L11.75 14.75V19H7.75V14.75L9 13.5Z"
    glass = "M13.5 12.5H17C17 14.5 16.2 15.5 15.25 15.75V17.75H16.75V19H13.75V17.75H15.25V15.75C14.3 15.5 13.5 14.5 13.5 12.5Z"
    return [
        *shop(S),
        mark(bottle), mark(glass),
    ]


@icon("sporting-goods-store", CAT, "Shop front with an awning and a football sign",
      tags=["sports shop", "sporting goods", "sports store", "sportswear", "equipment", "athletics"],
      aliases=["sports-shop"])
def _(S):
    return [
        *shop(S),
        detail(circle(12, 15.25, 3.5)),
        mark(poly(regular(12, 15.25, 1.9, 5), closed=True)),
    ]


# ============================================================================ wayside and heritage

@icon("wayside-cross", CAT, "Tall wooden cross under a small peaked roof standing by a path",
      tags=["roadside cross", "calvary", "wayside shrine", "crucifix", "pilgrimage", "rural"],
      aliases=["roadside-cross"])
def _(S):
    return [
        shell(poly([(6.5, 7), (12, 3), (17.5, 7)], closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        line(seg(12, 7, 12, 21)),
        line(seg(8, 11, 16, 11)),
        line(seg(2, 21, 22, 21)),
    ]


@icon("archaeological-site", CAT, "Rectangular dig pit marked out with a string grid, with a trowel and a pottery shard",
      tags=["excavation", "dig site", "archaeology", "ruins", "heritage site", "trench"],
      aliases=["excavation-site", "dig-site"])
def _(S):
    ax = (-1 / math.sqrt(2), 1 / math.sqrt(2))
    px = (1 / math.sqrt(2), 1 / math.sqrt(2))
    base = (19, 5)
    mid = (base[0] + ax[0] * 2.5, base[1] + ax[1] * 2.5)
    tip = (base[0] + ax[0] * 7, base[1] + ax[1] * 7)
    blade = [base, (mid[0] + px[0] * 2.75, mid[1] + px[1] * 2.75), tip, (mid[0] - px[0] * 2.75, mid[1] - px[1] * 2.75)]
    return [
        line(seg(21.5, 2.5, base[0], base[1])),
        shell(poly(blade, closed=True, r=S.r * 0.3)),
        shell(rect(2.5, 11, 13, 10, min(S.R, 2))),
        detail(seg(9, 11, 9, 21)), detail(seg(2.5, 16, 15.5, 16)),
        mark(poly([(4.5, 17.75), (7.5, 17.5), (6, 19.75)], closed=True)),
    ]


@icon("split-gate", CAT, "Tall stepped gateway split into two mirrored halves with a narrow passage between them",
      tags=["candi bentar", "balinese gate", "temple gate", "split gateway", "entrance", "bali"],
      aliases=["candi-bentar"])
def _(S):
    left = [(2.5, 21), (2.5, 16), (4, 16), (4, 11.5), (5.5, 11.5), (5.5, 7), (7, 7), (7, 2.5), (10, 2.5), (10, 21)]
    right = [(24 - x, y) for x, y in left]
    return [
        shell(poly(left, closed=True, r=S.r * 0.3)),
        shell(poly(right, closed=True, r=S.r * 0.3)),
    ]


@icon("rumah-gadang", CAT, "Long raised house whose roof sweeps up into sharp horn-shaped peaks",
      tags=["minangkabau house", "gonjong", "traditional house", "sumatra", "indonesia", "vernacular"],
      aliases=["gonjong-house"])
def _(S):
    roof = "M2.5 3.5Q4.5 8.5 7.5 8.5Q10.5 8.5 12 3.5Q13.5 8.5 16.5 8.5Q19.5 8.5 21.5 3.5L19 12H5Z"
    return [
        shell(roof),
        shell(rect(5, 12, 14, 5, min(S.R, 1.5))),
        win(8, 13.5, 2, 2), win(14, 13.5, 2, 2),
        line(seg(6.5, 17, 6.5, 21)), line(seg(12, 17, 12, 21)), line(seg(17.5, 17, 17.5, 21)),
    ]


@icon("palapa", CAT, "Open-sided shelter with a thick thatched palm roof on four wooden posts",
      tags=["thatched shelter", "beach hut", "tiki hut", "palm roof", "beach umbrella", "cabana"],
      aliases=["tiki-hut"])
def _(S):
    fringe = [(2, 11), (4.5, 12.5), (7, 11), (9.5, 12.5), (12, 11), (14.5, 12.5), (17, 11), (19.5, 12.5), (22, 11)]
    return [
        shell(poly([(12, 2.5), (22, 11)] + fringe[::-1][1:], closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        detail(seg(12, 2.5, 9, 9)), detail(seg(12, 2.5, 15, 9)),
        *[line(seg(x, 12.5, x, 21)) for x in (4.5, 9.5, 14.5, 19.5)],
    ]


@icon("caryatid", CAT, "Column carved as a standing draped figure carrying a stone slab on her head",
      tags=["figure column", "sculpted column", "classical", "greek architecture", "statue column", "atlas"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 3, min(S.R, 1))),
        line(seg(12, 5.5, 12, 6.5)),
        dot(12, 8.25, 1.75),
        shell(poly([(9, 11.5), (15, 11.5), (14, 15), (15, 19), (9, 19), (10, 15)], closed=True, r=S.r * 0.4)),
        detail(seg(12, 14, 12, 19)),
        shell(rect(6.5, 19, 11, 2, min(S.R, 1))),
    ]


@icon("house-foundation", CAT, "House outline resting on a solid foundation slab below the ground line",
      tags=["foundation", "footing", "slab", "basement", "groundwork", "construction"],
      aliases=["building-foundation"])
def _(S):
    return [
        shell(poly([(5, 14.5), (5, 8.5), (12, 3), (19, 8.5), (19, 14.5)], closed=True, r=S.r * 0.5)),
        door(S, 10, 14, 10.5, 14.5),
        line(seg(2, 15.5, 22, 15.5)),
        solid(rect(5, 18, 14, 3)),
    ]


@icon("saddle-roof", CAT, "Building topped by a saddle-shaped roof curving up at two opposite corners",
      tags=["hyperbolic paraboloid", "hypar roof", "saddle", "curved roof", "modern roof", "shell roof"],
      aliases=["hypar-roof"])
def _(S):
    return [
        shell(L(S, "M2 3Q12 11 22 3L21 7.5Q12 14 3 7.5Z", "M2 3.5Q12 11 22 3.5Q22.2 6.2 20.8 7.8Q12 14 3.2 7.8Q1.8 6.2 2 3.5Z")),
        shell(poly([(5.5, 21), (5.5, 12.5), (18.5, 12.5), (18.5, 21)], closed=True, r=S.r * 0.5)),
        door(S, 10, 14, 15.5),
    ]


@icon("jalousie-window", CAT, "Window of stacked horizontal glass slats tilted open",
      tags=["louvre window", "louvered window", "jalousie", "slatted window", "ventilation", "tropical window"],
      aliases=["louvre-window"])
def _(S):
    return [
        shell(rect(4, 3, 16, 18, min(S.R, 2))),
        *[detail(seg(6.5, y + 1, 17.5, y - 1)) for y in (7, 11, 15, 19)][:3],
        line(seg(12, 18, 12, 21)),
    ]


@icon("folding-door", CAT, "Door of hinged panels folded into a zigzag inside its frame",
      tags=["bifold door", "accordion door", "concertina door", "folding panels", "room divider", "closet door"],
      aliases=["bifold-door", "accordion-door"])
def _(S):
    top = [(5.5, 5.5), (8.5, 7), (11.5, 5.5), (14.5, 7)]
    bot = [(14.5, 19), (11.5, 20.5), (8.5, 19), (5.5, 20.5)]
    return [
        line(poly([(2.5, 21), (2.5, 2.5), (21.5, 2.5), (21.5, 21)], r=S.r)),
        shell(poly(top + bot, closed=True, r=S.r * 0.3)),
        detail(seg(8.5, 7, 8.5, 19)), detail(seg(11.5, 5.5, 11.5, 20.5)),
        dot(18.5, 12, 1.2),
    ]


@icon("chain-barrier", CAT, "Row of short posts linked by sagging chains",
      tags=["chain fence", "post and chain", "bollards", "barrier", "rope barrier", "keep out"],
      aliases=["post-and-chain"])
def _(S):
    return [
        *[dot(x, 9, 1.75) for x in (4, 12, 20)],
        *[line(seg(x, 10.5, x, 21)) for x in (4, 12, 20)],
        line("M4 12Q8 19 12 12"), line("M12 12Q16 19 20 12"),
    ]


@icon("historical-marker", CAT, "Plaque with a rounded top on a single post showing lines of raised text",
      tags=["historic marker", "heritage plaque", "landmark sign", "history", "information sign", "commemorative plaque"],
      aliases=["historic-marker"])
def _(S):
    plaque = L(S, "M4 15V7A8 4 0 0 1 20 7V15Z", "M4 13V7A8 4 0 0 1 20 7V13A2 2 0 0 1 18 15H6A2 2 0 0 1 4 13Z")
    return [
        shell(plaque),
        detail(seg(8, 7.5, 16, 7.5)), detail(seg(7.5, 11, 16.5, 11)),
        line(seg(12, 15, 12, 21)),
        line(seg(8.5, 21, 15.5, 21)),
    ]


@icon("vendor-cart", CAT, "Push cart with two wheels, a small umbrella on top and a serving counter",
      tags=["street vendor", "food cart", "hot dog stand", "hawker", "pushcart", "street food"],
      aliases=["pushcart"])
def _(S):
    return [
        shell(L(S, "M4 7L11 3L18 7Z", "M4 7A7 4 0 0 1 18 7Z")),
        line(seg(11, 7, 11, 10.5)),
        shell(rect(3.5, 10.5, 15, 6.5, min(S.R, 2))),
        detail(seg(3.5, 13, 18.5, 13)),
        line(poly([(18.5, 12), (21.5, 9.5)])),
        detail(circle(7.5, 19.5, 1.5)), detail(circle(14.5, 19.5, 1.5)),
    ]


@icon("swing-ride", CAT, "Fairground swing ride with seats hanging on long chains swung outward from a spinning top",
      tags=["chair swing", "wave swinger", "carousel swing", "fairground ride", "amusement park", "funfair"],
      aliases=["chair-swing"])
def _(S):
    return [
        shell(poly([(5, 7), (12, 2.5), (19, 7)], closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        line(seg(12, 7, 12, 21)),
        line(seg(6.5, 7, 3, 14)), line(seg(17.5, 7, 21, 14)),
        line(seg(9.5, 7, 7.75, 16)), line(seg(14.5, 7, 16.25, 16)),
        solid(rect(6, 16, 3.5, 2.5, L(S, 0, 1))), solid(rect(14.5, 16, 3.5, 2.5, L(S, 0, 1))),
        solid(rect(1.5, 14, 3.5, 2.5) if S.name == "line" else rect(1.5, 14, 3.5, 2.5, 1)),
        solid(rect(19, 14, 3.5, 2.5) if S.name == "line" else rect(19, 14, 3.5, 2.5, 1)),
        line(seg(8, 21, 16, 21)),
    ]


@icon("water-slide", CAT, "Tall platform with a tube slide twisting down into a pool",
      tags=["waterslide", "water park", "flume", "aquapark", "pool slide", "splash"], aliases=["flume"])
def _(S):
    return [
        shell(rect(2, 4, 7, 2.5, min(S.R, 1))),
        line(seg(3, 6.5, 3, 21)), line(seg(7.5, 6.5, 7.5, 21)),
        line(seg(3, 11, 7.5, 11)), line(seg(3, 15.5, 7.5, 15.5)),
        line("M9 5.25C17.5 5.25 19 9.5 14.5 12.5C11 14.75 11.5 17.5 16 17.5"),
        line("M11.5 21Q13.75 19.5 16 21T20.5 21"),
    ]


@icon("sentry-box", CAT, "Narrow upright guard booth with a peaked roof beside a gate barrier",
      tags=["guard box", "guard booth", "sentry", "checkpoint", "guard post", "security"],
      aliases=["guard-booth"])
def _(S):
    return [
        shell(poly([(4.5, 21), (4.5, 7.5), (9, 3), (13.5, 7.5), (13.5, 21)], closed=True, r=S.r * 0.5)),
        detail(poly([(7, 21), (7, 11), (11, 11), (11, 21)], r=S.r * 0.3)),
        line(seg(16.5, 12, 16.5, 21)),
        shell(rect(16.5, 10.5, 5.5, 3, min(S.R, 1))),
    ]


@icon("hay-barn", CAT, "Open-sided barn with a curved roof over stacked hay bales",
      tags=["dutch barn", "hay shed", "haystack", "farm", "hay bales", "agriculture"], aliases=["dutch-barn"])
def _(S):
    return [
        shell(L(S, "M2 10.5A10 7.5 0 0 1 22 10.5Z", "M2.2 10.5A10 7.5 0 0 1 21.8 10.5A.9 .9 0 0 1 21 11.5H3A.9 .9 0 0 1 2.2 10.5Z")),
        line(seg(3, 10.5, 3, 21)), line(seg(21, 10.5, 21, 21)),
        *[win(x, y, 5.25, 3) for x in (6, 12.75) for y in (13.5, 17.75)],
    ]


@icon("mastaba", CAT, "Low flat-topped Egyptian tomb with sloping sides and a small doorway",
      tags=["egyptian tomb", "ancient egypt", "tomb", "burial", "necropolis", "archaeology"])
def _(S):
    return [
        shell(poly([(2.5, 21), (5, 11), (19, 11), (21.5, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(5, 14, 19, 14)),
        door(S, 10.5, 13.5, 17),
    ]


@icon("building-dimensions", CAT, "Building front outline with horizontal and vertical dimension lines ending in ticks",
      tags=["dimensions", "measurements", "elevation", "architecture drawing", "floor height", "building size"])
def _(S):
    return [
        shell(rect(3, 8, 12, 13, min(S.R, 2))),
        win(5.5, 10.5, 2.5, 2.5), win(10, 10.5, 2.5, 2.5),
        door(S, 7.5, 10.5, 16),
        line(seg(3, 4, 15, 4)), line(seg(3, 2, 3, 6)), line(seg(15, 2, 15, 6)),
        line(seg(19.5, 8, 19.5, 21)), line(seg(17.5, 8, 21.5, 8)), line(seg(17.5, 21, 21.5, 21)),
    ]


@icon("theater-marquee", CAT, "Projecting sign board rimmed with light bulbs above an entrance",
      tags=["marquee sign", "cinema sign", "theatre marquee", "broadway", "light bulbs", "showtime"],
      aliases=["theatre-marquee"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 9.5, min(S.R, 2))),
        *[dot(x, y, 1) for x in (6, 9.5, 14.5, 18) for y in (5.75, 9.75)],
        line(seg(4.5, 12.5, 4.5, 21)), line(seg(19.5, 12.5, 19.5, 21)),
        detail(poly([(8.5, 21), (8.5, 15.5), (15.5, 15.5), (15.5, 21)], r=S.r * 0.3)),
        detail(seg(12, 15.5, 12, 21)),
    ]


@icon("hanging-shop-sign", CAT, "Iron bracket on a wall holding a swinging sign board on two rings",
      tags=["shop sign", "hanging sign", "pub sign", "tavern sign", "signboard", "storefront"],
      aliases=["bracket-sign"])
def _(S):
    return [
        line(seg(3, 2, 3, 21)),
        line(seg(3, 5, 21, 5)),
        line(L(S, "M3 12L10 5", "M3 12Q4 6 10 5")),
        line(seg(10, 5, 10, 9.5)), line(seg(18, 5, 18, 9.5)),
        shell(rect(8, 9.5, 12, 8, min(S.R, 2))),
    ]


@icon("lightning-rod", CAT, "Pointed rod on a roof peak with a cable running down the wall to the ground",
      tags=["lightning conductor", "lightning protection", "grounding", "earthing", "storm", "surge"],
      aliases=["lightning-conductor"])
def _(S):
    return [
        solid(poly([(8, 1.5), (9, 4.5), (7, 4.5)], closed=True)),
        line(seg(8, 4.5, 8, 7)),
        shell(poly([(2.5, 21), (2.5, 12.5), (8, 7), (13.5, 12.5), (13.5, 21)], closed=True, r=S.r * 0.5)),
        line(poly([(8, 5.5), (18, 5.5), (18, 19)], r=S.r)),
        line(seg(15.5, 19, 20.5, 19)), line(seg(16.5, 21.5, 19.5, 21.5)),
    ]


@icon("abandoned-building", CAT, "Derelict building with broken windows, a boarded-up door and a crack across the wall",
      tags=["derelict", "ruin", "vacant building", "condemned", "decay", "urban exploration"],
      aliases=["derelict-building"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 4), (14, 4), (16, 7), (18, 5), (21, 7.5), (21, 21)], closed=True, r=S.r * 0.3)),
        mark(poly([(6, 8), (10, 8), (10, 10), (8.5, 9.5), (7.5, 12), (6, 12)], closed=True)),
        detail(poly([(18, 9), (15.5, 12), (17.5, 13.5), (15, 16.5)], r=S.r * 0.3)),
        detail(poly([(8, 21), (8, 15), (13, 15), (13, 21)], r=S.r * 0.3)),
        detail(seg(8, 17.5, 13, 20)),
    ]


@icon("recycling-center", CAT, "Building with a looping recycling arrows sign and a row of bins in front",
      tags=["recycling centre", "recycling depot", "waste facility", "tip", "dump", "household waste"],
      aliases=["recycling-centre"])
def _(S):
    c = (12, 8.5)
    r = 3.25
    h1 = [pt_on_(c, r + 1.5, 150), pt_on_(c, r - 1.5, 150), pt_on_(c, r, 195)]
    h2 = [pt_on_(c, r + 1.5, 330), pt_on_(c, r - 1.5, 330), pt_on_(c, r, 15)]
    return [
        shell(rect(3, 3, 18, 11, min(S.R, 2))),
        detail(arc(c[0], c[1], r, 200, 330)), detail(arc(c[0], c[1], r, 20, 150)),
        mark(poly(h1, closed=True)), mark(poly(h2, closed=True)),
        *[shell(rect(x, 17, 4, 4, min(S.R, 1))) for x in (3.5, 10, 16.5)],
    ]


@icon("bottle-kiln", CAT, "Tall bottle-shaped brick kiln with a wide base and a narrow chimney neck",
      tags=["pottery kiln", "bottle oven", "kiln", "potteries", "industrial heritage", "ceramics"],
      aliases=["bottle-oven"])
def _(S):
    body = L(S, "M5 21C5 14.5 7.5 11 10 8.5V2.5H14V8.5C16.5 11 19 14.5 19 21Z",
             "M5 21C5 14.5 7.5 11 10 8.5V4A1.5 1.5 0 0 1 11.5 2.5H12.5A1.5 1.5 0 0 1 14 4V8.5C16.5 11 19 14.5 19 21Z")
    return [
        shell(body),
        detail(seg(10, 7, 14, 7)),
        arch_door(10, 14, 16),
        line(seg(2, 21, 22, 21)),
    ]


@icon("mud-brick-house", CAT, "Boxy adobe house with soft rounded corners and wooden roof beams poking out of its walls",
      tags=["adobe house", "mud house", "pueblo style", "earth building", "vigas", "desert home"],
      aliases=["adobe-house"])
def _(S):
    return [
        shell(rect(4.5, 5, 15, 16, L(S, 2.5, 4))),
        line(seg(2, 8.5, 4.5, 8.5)), line(seg(19.5, 8.5, 22, 8.5)),
        *[dot(x, 8.5, 1.1) for x in (8.5, 12, 15.5)],
        win(7, 12.5, 2.5, 2.5),
        door(S, 12.5, 16, 13),
    ]


@icon("cape-cod-house", CAT, "One-and-a-half storey house with a steep roof, a central chimney and two dormers",
      tags=["cape cod", "cottage", "new england house", "colonial house", "dormer", "family home"])
def _(S):
    return [
        shell(rect(11, 2, 2.5, 3, 0)),
        shell(poly([(2, 13), (6.5, 5), (17.5, 5), (22, 13)], closed=True, r=S.r * 0.5)),
        detail(poly([(6.5, 13), (6.5, 10), (8.25, 8.25), (10, 10), (10, 13)], r=S.r * 0.3)),
        detail(poly([(14, 13), (14, 10), (15.75, 8.25), (17.5, 10), (17.5, 13)], r=S.r * 0.3)),
        shell(poly([(4, 13), (4, 21), (20, 21), (20, 13)], closed=True, r=S.r * 0.5)),
        win(6.5, 15.5, 2.5, 2.5), win(15, 15.5, 2.5, 2.5),
        door(S, 10.5, 13.5, 16),
    ]


@icon("stationery-store", CAT, "Shop front with an awning and a pencil sign",
      tags=["stationery shop", "stationer", "office supplies", "pens", "paper shop", "art supplies"],
      aliases=["stationer"])
def _(S):
    pencil = rot_pts([(10.75, 10.5), (13.25, 10.5), (13.25, 17), (12, 19.5), (10.75, 17)], 45, 12, 15)
    return [
        *shop(S),
        mark(poly(pencil, closed=True)),
    ]


@icon("phone-store", CAT, "Shop front with an awning and a smartphone sign",
      tags=["phone shop", "mobile phone store", "cell phone shop", "smartphones", "mobile repair", "handsets"],
      aliases=["mobile-phone-shop"])
def _(S):
    return [
        *shop(S),
        detail(rect(9.25, 11.5, 5.5, 8.5, 1.25)),
        dot(12, 17.75, 0.75),
    ]


@icon("computer-store", CAT, "Shop front with an awning and a laptop sign",
      tags=["computer shop", "laptops", "pc store", "it shop", "computer repair", "tech"],
      aliases=["computer-shop"])
def _(S):
    return [
        *shop(S),
        detail(rect(8.5, 12, 7, 5, 0.5)),
        detail(seg(7, 18.5, 17, 18.5)),
    ]


@icon("camera-store", CAT, "Shop front with an awning and a camera sign",
      tags=["camera shop", "photography shop", "photo store", "cameras", "photo lab", "lenses"],
      aliases=["camera-shop"])
def _(S):
    body = path_to_d(D(U(P(rect(7.5, 13, 9, 6, 1)), P(rect(9.5, 11.75, 3, 2, 0.5))), P(circle(12, 16, 1.75))))
    return [
        *shop(S),
        mark(body),
    ]


@icon("drop-tower", CAT, "Very tall thin tower with a ring of seats gripping it partway up",
      tags=["drop tower", "free fall ride", "tower ride", "amusement park", "thrill ride", "funfair"],
      aliases=["freefall-tower"])
def _(S):
    return [
        line(poly([(9.5, 12), (9.5, 3), (14.5, 3), (14.5, 12)], r=S.r * 0.5)),
        shell(rect(3.5, 12, 17, 4, min(S.R, 2))),
        detail(seg(9.5, 12, 9.5, 16)), detail(seg(14.5, 12, 14.5, 16)),
        line(seg(5.5, 16, 5.5, 18)), line(seg(18.5, 16, 18.5, 18)),
        line(seg(9.5, 16, 9.5, 21)), line(seg(14.5, 16, 14.5, 21)),
        line(seg(7, 21, 17, 21)),
    ]
