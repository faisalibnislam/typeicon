"""TypeIcon Core: architecture (batch 004).

Shops, services, and traditional and historic building types, drawn front-on on the ground line y = 21
(outer edge 22) in the language of sets/architecture_001.py: closed walls are shells, doors and trim are
details, and windows and signs are small solid blocks (`mark`) that are knocked out of Filled walls.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d  # noqa: F401

CAT = "architecture"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def mark(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled wall."""
    return Part("dot", d)


def win(x, y, w=2.0, h=2.0):
    return mark(rect(x, y, w, h))


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


def awning_shop(S, top=2.5, eave=8.5):
    """Striped awning over a shop body (walls x 5-19); the sign symbol sits in x 7.5-16.5, y 11-19."""
    return [
        shell(poly([(3, eave), (5, top), (19, top), (21, eave)], closed=True, r=S.r)),
        detail(seg(9.67, top, 9, eave)), detail(seg(14.33, top, 15, eave)),
        shell(poly([(5, eave), (5, 21), (19, 21), (19, eave)], closed=True, r=S.r)),
        detail(seg(3, eave, 21, eave)),
    ]


# ============================================================================ shops

@icon("perfume-shop", CAT, "Shop front with an awning and a round perfume bottle on the sign",
      tags=["perfumery", "fragrance shop", "scent", "cologne", "cosmetics", "beauty store"],
      aliases=["perfumery"])
def _(S):
    return [
        *awning_shop(S),
        detail(circle(12, 16.25, 2.75)),
        mark(rect(10.75, 11, 2.5, 2.5, L(S, 0, 0.6))),
    ]


@icon("tattoo-parlor", CAT, "Shop front with an awning and a tattoo machine on the sign",
      tags=["tattoo shop", "tattoo studio", "ink", "body art", "tattoo artist", "piercing"],
      aliases=["tattoo-parlour", "tattoo-shop"])
def _(S):
    def tf(pts):  # upright machine drawn about (12, 15), scaled and turned so the needle points down-left
        return rot_pts([(12 + (x - 12) * 0.85, 15 + (y - 15) * 0.85) for x, y in pts], 40, 12, 15)
    coil = lambda x: mark(poly(tf([(x, 13), (x, 10.25), (x + 2.25, 10.25), (x + 2.25, 13)]), closed=True))
    return [
        *awning_shop(S),
        coil(9.25), coil(12.5),
        mark(poly(tf([(8.75, 12.5), (15.25, 12.5), (15.25, 14.5), (8.75, 14.5)]), closed=True)),
        detail(poly(tf([(12, 14.5), (12, 21)]))),
        mark(poly(tf([(10.6, 16.25), (13.4, 16.25), (13.4, 19.25), (10.6, 19.25)]), closed=True)),
    ]


@icon("dry-cleaner", CAT, "Shop front with an awning and a clothes hanger under a plastic cover on the sign",
      tags=["dry cleaning", "laundry service", "cleaners", "garment care", "pressing", "launderette"],
      aliases=["dry-cleaners"])
def _(S):
    return [
        *awning_shop(S),
        detail("M10.75 12.5A1.25 1.25 0 1 1 12 13.75V14"),
        detail(poly([(12, 14), (8, 16.5), (8, 19), (16, 19), (16, 16.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("print-shop", CAT, "Shop front with an awning and a printer on the sign",
      tags=["printing", "copy shop", "print centre", "copies", "printer", "photocopy"],
      aliases=["copy-shop", "print-center"])
def _(S):
    return [
        *awning_shop(S),
        detail(poly([(9.5, 13), (9.5, 11), (14.5, 11), (14.5, 13)], r=S.r * 0.4)),
        detail(rect(7.5, 13, 9, 4.5, min(S.R, 1.5))),
        mark(rect(9.5, 16.5, 5, 3.5)),
    ]


@icon("travel-agency", CAT, "Shop front with an awning and a small airplane on the sign",
      tags=["travel agent", "holidays", "vacation", "tour operator", "flights", "booking"],
      aliases=["travel-agent"])
def _(S):
    plane = [(12, 10.75), (13, 12), (13, 14), (16.75, 16), (16.75, 17.25), (13, 16.25), (13, 18.25), (14.5, 19.25),
             (14.5, 20), (12, 19.5), (9.5, 20), (9.5, 19.25), (11, 18.25), (11, 16.25), (7.25, 17.25), (7.25, 16),
             (11, 14), (11, 12)]
    return [
        *awning_shop(S),
        mark(poly(plane, closed=True)),
    ]


@icon("game-store", CAT, "Shop front with an awning and a game controller on the sign",
      tags=["video game shop", "games shop", "gaming", "console", "gamepad", "arcade"],
      aliases=["video-game-store"])
def _(S):
    pad = ("M9.5 13H14.5C15.8 13 16.4 14 16.6 15.2L17 17.6C17.2 18.8 15.9 19.4 15.1 18.6L14 17.5H10L8.9 18.6"
           "C8.1 19.4 6.8 18.8 7 17.6L7.4 15.2C7.6 14 8.2 13 9.5 13Z")
    return [
        *awning_shop(S),
        detail(pad),
        dot(14.25, 15.25, 0.9),
        dot(9.75, 15.25, 0.9),
    ]


def _horn():
    """Gramophone horn: sides from the throat above the box, tangent to a round mouth (upper right)."""
    tx, ty, cx, cy, r = 10.25, 17.25, 14.5, 12.5, 2.6
    dist = math.hypot(cx - tx, cy - ty)
    base = math.atan2(cy - ty, cx - tx)
    off = math.acos(r / dist)
    p1 = (cx + r * math.cos(base + math.pi - off), cy + r * math.sin(base + math.pi - off))
    p2 = (cx + r * math.cos(base + math.pi + off), cy + r * math.sin(base + math.pi + off))
    return poly([p1, (tx, ty), p2]), circle(cx, cy, r)


@icon("antique-shop", CAT, "Shop front with an awning and a gramophone with a flared horn on the sign",
      tags=["antiques", "vintage shop", "curio shop", "collectibles", "second hand", "retro"],
      aliases=["antiques-shop"])
def _(S):
    throat, mouth = _horn()
    return [
        *awning_shop(S),
        mark(throat), detail(mouth),
        mark(rect(7.5, 17.25, 5.5, 2.75)),
    ]


@icon("thrift-store", CAT, "Shop front with an awning and a price tag on the sign",
      tags=["charity shop", "second hand store", "secondhand", "op shop", "used goods", "bargain"],
      aliases=["charity-shop", "second-hand-store"])
def _(S):
    return [
        *awning_shop(S),
        detail(poly([(7.5, 15.5), (10.25, 12.5), (16.5, 12.5), (16.5, 18.5), (10.25, 18.5)], closed=True, r=S.r * 0.5)),
        dot(11, 15.5, 1),
    ]


@icon("paint-store", CAT, "Shop front with an awning and paint dripping down the sign",
      tags=["paint shop", "decorating store", "hardware", "paints", "home improvement", "diy"],
      aliases=["paint-shop"])
def _(S):
    drips = [P(rect(7.5, 11, 9, 2.5))]
    for x, y in ((8, 17.5), (11.25, 15), (14.5, 16.5)):
        drips += [P(rect(x, 12, 2, y - 12)), P(circle(x + 1, y, 1))]
    return [
        *awning_shop(S),
        mark(path_to_d(U(*drips))),
    ]


# ============================================================================ services

@icon("tire-shop", CAT, "Garage with an open bay door beside a stack of tires",
      tags=["tyre shop", "tire center", "tyres", "wheel shop", "car service", "garage"],
      aliases=["tyre-shop"])
def _(S):
    return [
        shell(poly([(2, 21), (2, 8.5), (7, 4.5), (12, 8.5), (12, 21)], closed=True, r=S.r * 0.5)),
        mark(rect(4.25, 13, 5.5, 8)),
        detail(seg(4.25, 10.75, 9.75, 10.75)),
        shell(circle(17.5, 16.5, 4.5)),
        detail(circle(17.5, 16.5, 1.5)),
    ]


@icon("ambulance-station", CAT, "Station with an ambulance in its open bay and a star of life sign above",
      tags=["ems station", "paramedic station", "emergency medical", "ambulance depot", "rescue", "999"],
      aliases=["ems-station"])
def _(S):
    bar = lambda a: rot_pts([(11, 4.25), (13, 4.25), (13, 9.75), (11, 9.75)], a, 12, 7)
    star = U(*[P(poly(bar(a), closed=True)) for a in (0, 60, 120)])
    return [
        shell(rect(2.5, 2.5, 19, 18.5, S.R)),
        mark(path_to_d(star)),
        detail(poly([(5.5, 21), (5.5, 12.5), (18.5, 12.5), (18.5, 21)], r=S.r * 0.5)),
        mark(rect(8.5, 15, 7, 2.5, L(S, 0, 0.75))),
        dot(9.5, 19.25, 1), dot(14.5, 19.25, 1),
    ]


@icon("dental-clinic", CAT, "Small building with a tooth symbol on the front above the door",
      tags=["dentist", "dental office", "dental surgery", "orthodontist", "teeth", "clinic"],
      aliases=["dentist-office"])
def _(S):
    tooth = ("M9.8 8.7C11 8.2 11.5 8.9 12 8.9C12.5 8.9 13 8.2 14.2 8.7C15.3 9.2 15.2 10.8 14.6 12.1L13.9 13.9"
             "C13.7 14.4 13.1 14.4 13 13.9L12.6 12.5C12.4 11.9 11.6 11.9 11.4 12.5L11 13.9C10.9 14.4 10.3 14.4 10.1 13.9"
             "L9.4 12.1C8.8 10.8 8.7 9.2 9.8 8.7Z")
    return [
        shell(poly([(3, 21), (3, 9), (12, 3), (21, 9), (21, 21)], closed=True, r=S.r * 0.5)),
        mark(tooth),
        door(S, 10, 14, 16.5),
    ]


@icon("animal-shelter", CAT, "Small building with a paw print inside a heart on the sign above the door",
      tags=["animal rescue", "pet shelter", "dog shelter", "pet adoption", "humane society", "pound"],
      aliases=["pet-shelter", "animal-rescue"])
def _(S):
    heart = P("M12 16C8 13.5 6 11.5 6 9C6 7.2 7.4 5.8 9.1 5.8C10.4 5.8 11.4 6.5 12 7.6C12.6 6.5 13.6 5.8 14.9 5.8"
              "C16.6 5.8 18 7.2 18 9C18 11.5 16 13.5 12 16Z")
    paw = U(P(ellipse(12, 11.6, 1.9, 1.5)), P(circle(9.6, 9.6, 1)), P(circle(12, 8.5, 1)), P(circle(14.4, 9.6, 1)))
    return [
        shell(poly([(2.5, 21), (2.5, 3), (21.5, 3), (21.5, 21)], closed=True, r=S.r * 0.5)),
        mark(path_to_d(D(heart, paw))),
        door(S, 10, 14, 18),
    ]


@icon("nursing-home", CAT, "Low building with a heart on its front and a ramp with a handrail up to the door",
      tags=["care home", "retirement home", "elderly care", "assisted living", "aged care", "senior living"],
      aliases=["care-home", "retirement-home"])
def _(S):
    heart = ("M7 14.5C5 13.1 4 12.1 4 10.9C4 10 4.7 9.4 5.5 9.4C6.2 9.4 6.7 9.8 7 10.3"
             "C7.3 9.8 7.8 9.4 8.5 9.4C9.3 9.4 10 10 10 10.9C10 12.1 9 13.1 7 14.5Z")
    return [
        shell(poly([(2, 21), (2, 8), (8.5, 3.5), (15, 8), (15, 18.5), (21, 21)], closed=True, r=S.r * 0.5)),
        mark(heart),
        detail(seg(2, 18.5, 15, 18.5)),
        detail(poly([(10.75, 18.5), (10.75, 12.5), (13.25, 12.5), (13.25, 18.5)], r=S.r * 0.4)),
        line(poly([(15, 14.75), (21, 17.25), (21, 19.5)], r=S.r * 0.5)),
    ]


# ============================================================================ stages, pavilions and structures

@icon("band-shell", CAT, "Outdoor stage under a large shell roof of nested arches",
      tags=["bandshell", "outdoor stage", "concert shell", "open air stage", "amphitheater stage", "park concert"],
      aliases=["bandshell"])
def _(S):
    return [
        shell("M2 21V16H2.5A9.5 11.5 0 0 1 21.5 16H22V21Z" if S.name == "line" else
              "M2 19.5V16H2.5A9.5 11.5 0 0 1 21.5 16H22V19.5A1.5 1.5 0 0 1 20.5 21H3.5A1.5 1.5 0 0 1 2 19.5Z"),
        detail(seg(2, 16, 22, 16)),
        detail("M6 16A6 7.75 0 0 1 18 16"),
        detail("M9.75 16A2.25 3.5 0 0 1 14.25 16"),
    ]


@icon("bell-pavilion", CAT, "Large temple bell hanging under a small curved roof on posts",
      tags=["bell tower", "temple bell", "belfry", "shoro", "bell house", "buddhist temple"],
      aliases=["temple-bell-pavilion"])
def _(S):
    return [
        shell("M2 8.5Q5.5 8.5 7 4H17Q18.5 8.5 22 8.5Z"),
        line(seg(4.5, 8.5, 4.5, 21)), line(seg(19.5, 8.5, 19.5, 21)),
        line(seg(12, 8.5, 12, 10.5)),
        shell("M8 18.5C9 17.5 9.25 16.5 9.25 14.5A2.75 2.75 0 0 1 14.75 14.5C14.75 16.5 15 17.5 16 18.5Z"),
        line(seg(2, 21, 22, 21)),
    ]


@icon("corbel-arch", CAT, "Stepped arch of overlapping stone courses meeting at the top",
      tags=["corbelled arch", "false arch", "corbel vault", "stepped arch", "mayan arch", "masonry"],
      aliases=["corbelled-arch"])
def _(S):
    pts = [(3, 21), (3, 3), (21, 3), (21, 21), (18, 21), (18, 16), (16, 16), (16, 12), (14, 12), (14, 8), (10, 8),
           (10, 12), (8, 12), (8, 16), (6, 16), (6, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.3)),
    ]


@icon("tensile-canopy", CAT, "Fabric membrane roof pulled up into two peaks by masts",
      tags=["tensile structure", "membrane roof", "fabric roof", "shade sail", "tent roof", "canopy"],
      aliases=["membrane-roof"])
def _(S):
    top = "M2 13C4.5 12 6 9 7 3.5C8.5 8.5 10 10 12 10C14 10 15.5 8.5 17 3.5C18 9 19.5 12 22 13"
    return [
        shell(top + "C17 11.5 15 14 12 14C9 14 7 11.5 2 13Z"),
        line(seg(7, 12.5, 7, 21)), line(seg(17, 12.5, 17, 21)),
        line(seg(2.5, 21, 21.5, 21)),
    ]


# ============================================================================ towers and traditional houses

@icon("tower-house", CAT, "Tall narrow stone tower house with a pitched roof inside its parapet and a window on each floor",
      tags=["tower house", "peel tower", "keep", "fortified house", "scottish tower", "irish tower"],
      aliases=["peel-tower"])
def _(S):
    return [
        shell(poly([(7, 21), (7, 7.5), (9, 7.5), (12, 3), (15, 7.5), (17, 7.5), (17, 21)], closed=True, r=S.r * 0.4)),
        detail(seg(7, 9.5, 17, 9.5)),
        win(11, 11.5, 2, 2.5), win(11, 15, 2, 2.5),
        arch_door(10.75, 13.25, 18),
    ]


@icon("round-tower", CAT, "Tall slender round stone tower with a conical cap and a doorway high above the ground",
      tags=["irish round tower", "bell tower", "monastic tower", "stone tower", "belfry", "medieval tower"],
      aliases=["irish-round-tower"])
def _(S):
    return [
        shell(poly([(9, 21), (9.5, 7.5), (12, 3), (14.5, 7.5), (15, 21)], closed=True, r=S.r * 0.4)),
        detail(seg(9.5, 7.5, 14.5, 7.5)),
        mark(rect(11, 10, 2, 2)),
        mark("M11 17V14A1 1 0 0 1 13 14V17Z"),
        line(seg(3, 21, 21, 21)),
    ]


@icon("turf-house", CAT, "Low house with grass-covered walls and roof and a wooden gable front with a door",
      tags=["sod house", "turf roof", "icelandic house", "grass roof", "earth house", "nordic house"],
      aliases=["sod-house"])
def _(S):
    mound = P("M2 21C2 15 4.5 11 12 11C19.5 11 22 15 22 21Z")
    gable = P(poly([(8, 21), (8, 12), (12, 7.5), (16, 12), (16, 21)], closed=True))
    return [
        shell(path_to_d(U(mound, gable))),
        detail(poly([(8, 21), (8, 12), (12, 7.5), (16, 12), (16, 21)], r=S.r * 0.4)),
        door(S, 10.75, 13.25, 15.5),
        win(11, 10.75, 2, 2),
    ]


@icon("bedouin-tent", CAT, "Long low tent with a sagging roof held up by several poles",
      tags=["desert tent", "black tent", "nomad tent", "goat hair tent", "bedu", "camp"],
      aliases=["black-tent"])
def _(S):
    return [
        shell("M2 20L4.5 8.5Q8.25 12 12 8Q15.75 12 19.5 8.5L22 20Z"),
        detail(poly([(6.5, 20), (6.5, 14), (17.5, 14), (17.5, 20)], r=S.r * 0.4)),
        detail(seg(12, 14, 12, 20)),
    ]


@icon("swinging-ship-ride", CAT, "Boat-shaped gondola hanging from an A-frame and swinging in an arc",
      tags=["pirate ship ride", "swinging ship", "funfair ride", "amusement park", "pendulum ride", "fairground"],
      aliases=["pirate-ship-ride"])
def _(S):
    return [
        line(seg(12, 3, 9.19, 10.5)), line(seg(12, 3, 14.81, 10.5)),
        line(seg(7.31, 15.5, 5.25, 21)), line(seg(16.69, 15.5, 18.75, 21)),
        dot(12, 3, 1.5),
        shell(poly([(2.5, 8.5), (5, 10.5), (19, 10.5), (21.5, 8.5), (18.5, 15), (5.5, 15)], closed=True, r=S.r * 0.5)),
        line(seg(3, 21, 21, 21)),
    ]


@icon("jail-cell", CAT, "Cell front of vertical bars with a lock plate on the barred door",
      tags=["prison cell", "cell", "lockup", "holding cell", "behind bars", "custody"],
      aliases=["prison-cell"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(7.5, 3, 7.5, 21)), detail(seg(12, 3, 12, 21)), detail(seg(16.5, 3, 16.5, 21)),
        mark(rect(13, 10.5, 4.5, 3.5, L(S, 0, 0.75))),
    ]


@icon("chinese-temple", CAT, "Temple hall with a sweeping double-eaved roof on a raised platform with front steps",
      tags=["chinese temple", "temple hall", "buddhist temple", "taoist temple", "pavilion", "palace hall"],
      aliases=["temple-hall"])
def _(S):
    return [
        shell("M5.5 6.5Q7.5 6.5 8.5 3H15.5Q16.5 6.5 18.5 6.5Z"),
        shell("M2 11.5Q5 11.5 6.5 8.25H17.5Q19 11.5 22 11.5Z"),
        line(seg(9.5, 6.5, 9.5, 8.25)), line(seg(14.5, 6.5, 14.5, 8.25)),
        *[line(seg(x, 11.5, x, 16.5)) for x in (5.5, 10, 14, 18.5)],
        shell(poly([(3, 21), (3, 16.5), (21, 16.5), (21, 21)], closed=True, r=S.r * 0.4)),
        mark(rect(9.5, 18.5, 5, 2.5)),
    ]


@icon("dogtrot-house", CAT, "Two small cabins under one long roof joined by an open breezeway between them",
      tags=["dog trot house", "breezeway house", "double pen house", "log cabin", "southern house", "cabin"],
      aliases=["breezeway-house"])
def _(S):
    pts = [(3, 21), (3, 10), (2, 10), (6, 4.5), (18, 4.5), (22, 10), (21, 10), (21, 21), (14.5, 21), (14.5, 12.5),
           (9.5, 12.5), (9.5, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.4)),
        detail(seg(3, 10, 21, 10)),
        win(5.25, 14.5, 2, 2.5), win(16.75, 14.5, 2, 2.5),
    ]


@icon("ribbed-dome", CAT, "Dome divided by curved ribs rising to a small lantern on top",
      tags=["dome", "ribbed cupola", "renaissance dome", "cathedral dome", "cupola", "lantern"],
      aliases=["ribbed-cupola"])
def _(S):
    return [
        line(seg(12, 1.5, 12, 3.5)),
        shell(rect(10.25, 3.5, 3.5, 4.5, min(S.R, 1))),
        shell("M3 17A9 9 0 0 1 21 17Z"),
        detail("M7.25 17A4.75 9 0 0 1 12 8"), detail("M16.75 17A4.75 9 0 0 0 12 8"),
        shell(rect(3, 17, 18, 4, min(S.R, 1.5))),
    ]


# ============================================================================ gates, signs and sacred places

@icon("lych-gate", CAT, "Roofed wooden gateway with a small pitched roof over a gate in a low wall",
      tags=["lychgate", "churchyard gate", "roofed gate", "covered gate", "church entrance", "gateway"],
      aliases=["lychgate"])
def _(S):
    return [
        shell(poly([(3, 11), (12, 3), (21, 11)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        line(seg(5.5, 11, 5.5, 21)), line(seg(18.5, 11, 18.5, 21)),
        line(seg(5.5, 14.5, 18.5, 14.5)), line(seg(5.5, 19.5, 18.5, 19.5)),
        line(seg(12, 14.5, 12, 19.5)),
        line(seg(6.5, 19.5, 11, 14.5)), line(seg(17.5, 19.5, 13, 14.5)),
    ]


@icon("sandwich-board", CAT, "Folding A-frame sign board standing on the pavement",
      tags=["a-frame sign", "pavement sign", "sidewalk sign", "chalkboard sign", "menu board", "street sign"],
      aliases=["a-frame-sign", "pavement-sign"])
def _(S):
    return [
        shell(poly([(7, 3.5), (17, 3.5), (19.5, 20), (4.5, 20)], closed=True, r=S.r * 0.5)),
        detail(seg(9.5, 8.5, 14.5, 8.5)), detail(seg(9, 12, 15, 12)), detail(seg(8.5, 15.5, 13, 15.5)),
    ]


@icon("domed-shrine", CAT, "Small cube-shaped shrine building topped by a single round dome",
      tags=["qubba", "tomb shrine", "mausoleum", "saint's tomb", "domed tomb", "marabout"],
      aliases=["qubba"])
def _(S):
    dome = P("M6.5 11A5.5 5.5 0 0 1 17.5 11Z")
    base = P(poly([(4.5, 21), (4.5, 11), (19.5, 11), (19.5, 21)], closed=True))
    return [
        line(seg(12, 2, 12, 5.5)),
        shell(path_to_d(U(dome, base))),
        detail(seg(4.5, 11, 19.5, 11)),
        detail("M9.5 21V16.5C9.5 15 10.5 14 12 13.25C13.5 14 14.5 15 14.5 16.5V21"),
    ]


@icon("mihrab", CAT, "Pointed arch niche set into a wall with a small lamp hanging inside",
      tags=["prayer niche", "qibla", "mosque", "islamic architecture", "niche", "prayer direction"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(L(S, "M7.5 21V12.5C7.5 9.5 9.5 7.5 12 6C14.5 7.5 16.5 9.5 16.5 12.5V21",
                 "M7.5 21V12.5C7.5 9.5 9.5 7.5 11.3 6.4Q12 6 12.7 6.4C14.5 7.5 16.5 9.5 16.5 12.5V21")),
        detail(seg(12, 6, 12, 10)),
        mark("M10.5 10H13.5L13 12.5A1 1 0 0 1 11 12.5Z"),
    ]


@icon("minbar", CAT, "Narrow stepped pulpit staircase rising to a small canopy with a pointed dome",
      tags=["mimbar", "pulpit", "mosque pulpit", "khutbah", "sermon", "islamic architecture"],
      aliases=["mimbar"])
def _(S):
    pts = [(3, 21), (3, 18.5), (5.5, 18.5), (5.5, 16), (8, 16), (8, 13.5), (10.5, 13.5), (10.5, 11), (20, 11), (20, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.3)),
        line(seg(13.5, 11, 13.5, 8)), line(seg(18.5, 11, 18.5, 8)),
        shell("M12.5 8C12.5 5.5 14.5 4 16 2.5C17.5 4 19.5 5.5 19.5 8Z"),
        detail("M13.5 21V17A2.25 2.25 0 0 1 18 17V21"),
    ]


@icon("reflecting-pool", CAT, "Long rectangular pool in perspective leading to an obelisk that is mirrored in the water",
      tags=["reflection pool", "reflecting basin", "memorial pool", "water feature", "monument", "formal garden"],
      aliases=["reflection-pool"])
def _(S):
    return [
        shell(poly([(10.5, 11), (11, 5), (12, 3), (13, 5), (13.5, 11)], closed=True, r=S.r * 0.3)),
        shell(poly([(7.5, 13), (16.5, 13), (21, 21), (3, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(12, 13, 12, 18)),
    ]


@icon("hacienda", CAT, "Long low house with a tiled roof and an arched arcade porch along the front",
      tags=["ranch house", "spanish colonial", "mission style", "estate", "adobe house", "arcade"],
      aliases=["estancia"])
def _(S):
    return [
        shell(poly([(2, 10), (4.5, 5.5), (19.5, 5.5), (22, 10)], closed=True, r=S.r * 0.5)),
        detail(seg(3.25, 7.75, 20.75, 7.75)),
        shell(poly([(3, 12), (3, 21), (21, 21), (21, 12)], r=S.r * 0.5)),
        arch_door(5.5, 9, 14), arch_door(10.25, 13.75, 14), arch_door(15, 18.5, 14),
    ]


@icon("octagon-house", CAT, "Two-storey eight-sided house with angled side walls and a small cupola on the roof",
      tags=["octagonal house", "eight sided house", "victorian house", "cupola", "octagon", "period house"],
      aliases=["octagonal-house"])
def _(S):
    return [
        shell(poly([(9.5, 6), (9.5, 3), (14.5, 3), (14.5, 6)], closed=True, r=S.r * 0.3)),
        shell(poly([(3, 10), (6.5, 6), (17.5, 6), (21, 10)], closed=True, r=S.r * 0.5)),
        shell(poly([(3.5, 10), (3.5, 21), (20.5, 21), (20.5, 10)], r=S.r * 0.5)),
        detail(seg(7.5, 10, 7.5, 21)), detail(seg(16.5, 10, 16.5, 21)),
        win(4.75, 12.5, 1.5, 2.5), win(17.75, 12.5, 1.5, 2.5), win(4.75, 16.5, 1.5, 2.5), win(17.75, 16.5, 1.5, 2.5),
        win(9.25, 12.5), win(12.75, 12.5),
        door(S, 10.75, 13.25, 16.5),
    ]


# ============================================================================ late additions

@icon("capsule-hotel", CAT, "Wall of stacked rounded sleeping pods, each with a small round door",
      tags=["pod hotel", "sleeping pod", "capsule", "budget hotel", "hostel", "sleep box"],
      aliases=["pod-hotel"])
def _(S):
    rr = L(S, 2, 3.25)
    parts = []
    for x in (2.5, 14):
        for y in (3.5, 14.5):
            parts += [shell(rect(x, y, 7.5, 6.5, rr)), dot(x + 3.75, y + 3.25, 1.75)]
    return parts


@icon("oriel-window", CAT, "Window box projecting from an upper floor, carried on a tapering bracket below",
      tags=["bay window", "oriel", "projecting window", "upper floor window", "corbel", "tudor"],
      aliases=["oriel"])
def _(S):
    body = [(2, 2), (6, 2), (6, 4), (19, 7.5), (19, 14), (6, 20), (6, 22), (2, 22)]
    return [
        shell(poly(body, closed=True, r=S.r * 0.4)),
        detail(seg(6, 7.5, 19, 7.5)), detail(seg(6, 14, 19, 14)),
        win(8.5, 9.5, 2, 2.5), win(12, 9.5, 2, 2.5), win(15.5, 9.5, 2, 2.5),
    ]
