"""TypeIcon Core: objects, batch 002 (household fixings, hangers, baskets, phone and smoking accessories, bedding)."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "objects"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def flip(d):
    """Mirror a d-string across the vertical centre line."""
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def rseg(x1, y1, x2, y2, deg, cx=12.0, cy=12.0):
    """Line segment rotated clockwise by deg about (cx, cy) (open paths cannot go through rot())."""
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    pts = [(cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c) for x, y in ((x1, y1), (x2, y2))]
    return seg(pts[0][0], pts[0][1], pts[1][0], pts[1][1])


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


# ============================================================================ chunk 1

@icon("paste-brush", CAT, "Wide flat paste brush beside an open pot of paste",
      tags=["paste", "glue brush", "wallpaper paste", "craft", "adhesive", "diy"])
def _(S):
    head = union(rect(2.5, 3, 8, 10, L(S, 0.5, 2)), rect(4.75, 12, 3.5, 9, L(S, 0, 1.5)))
    return [
        shell(head),
        detail(seg(4.5, 8.5, 8.5, 8.5)),
        shell(rect(13, 15, 9, 6, L(S, 1, 2.5))),
        line("M14.5 15Q17.5 8.5 20.5 15"),
    ]


@icon("rubber-cement", CAT, "Glass jar of rubber cement with a brush under the screw lid",
      tags=["glue", "adhesive", "cement", "craft", "paste jar", "brush"])
def _(S):
    return [
        shell(union(rect(4, 8, 16, 13, S.R), rect(6.5, 3, 11, 6, L(S, 0.5, 1.5)))),
        detail(seg(6.5, 8, 17.5, 8)),
        detail(seg(12, 11, 12, 14)),
        sq(10, 14, 4, 4, L(S, 0, 1)),
    ]


@icon("caulk-gun", CAT, "Caulk gun with a trigger grip, a long cartridge and a pointed nozzle",
      tags=["caulking", "sealant gun", "sealing", "bathroom", "diy", "construction"])
def _(S):
    tube = union(rect(6, 4, 11, 7, S.R), poly([(16, 5.5), (20.5, 7.5), (16, 9.5)], closed=True))
    return [
        shell(tube),
        line(seg(2.5, 7.5, 6, 7.5)),
        shell(poly([(6.5, 11), (11.5, 11), (10.5, 21), (5.5, 21)], closed=True, r=S.r)),
        line(poly([(14, 11), (14, 14.5), (12, 17)], r=S.r)),
    ]


@icon("sealant-tube", CAT, "Soft tube with a pointed nozzle and a bead of sealant coming out",
      tags=["caulk", "silicone", "adhesive tube", "squeeze tube", "glue", "diy"])
def _(S):
    body = union(poly([(2.5, 6), (13.5, 7.5), (13.5, 13.5), (2.5, 15)], closed=True, r=S.r),
                 poly([(13, 8.5), (20, 10.5), (13, 12.5)], closed=True))
    return [
        shell(body),
        detail(seg(5.5, 7.5, 5.5, 13.5)),
        line("M20.5 14 Q22.5 15.75 20.5 17.5 Q18.5 19.25 20.5 21"),
    ]


@icon("iron-on-patch", CAT, "Embroidered badge patch with a clothes iron hovering above it",
      tags=["patch", "iron-on", "embroidery", "badge", "sewing", "mend"])
def _(S):
    iron = "M3 9.5V8.5Q3 5 7 5H13Q16.5 5 21 9.5Z"
    return [
        shell(iron),
        line(poly([(8, 5), (8, 3), (13, 3), (13, 5)], r=S.r)),
        shell(poly([(6, 14), (18, 14), (18, 17.5), (12, 21.5), (6, 17.5)], closed=True, r=L(S, 0, 1.5))),
        dot(12, 17, 1.25),
    ]


@icon("sticker-roll", CAT, "Roll of round stickers on a backing strip with the end pulled out",
      tags=["stickers", "labels", "adhesive", "roll", "backing paper", "craft"])
def _(S):
    return [
        shell(circle(9, 12.5, 7)),
        detail(circle(9, 12.5, 2.5)),
        line(poly([(9, 19.5), (21.5, 19.5)], r=S.r)),
        shell(circle(17, 14.5, 2.5)),
    ]


@icon("reinforcement-label", CAT, "Punched paper with a small ring sticker around the hole",
      tags=["hole reinforcer", "hole ring", "binder", "paper", "stationery", "sticker"])
def _(S):
    paper = minus(rect(3, 3, 18, 18, S.R), circle(9.5, 12, 1.25))
    return [
        shell(paper),
        detail(circle(9.5, 12, 4.75)),
    ]


@icon("price-gun", CAT, "Handheld price labeller with a grip, trigger and a strip of labels",
      tags=["labeller", "label gun", "price tag", "retail", "pricing", "stock"])
def _(S):
    gun = union(rect(2.5, 4, 15, 8, S.R), poly([(3.5, 11), (10, 11), (9, 21), (4.5, 21)], closed=True, r=S.r))
    return [
        shell(gun),
        detail(seg(6, 8, 12.5, 8)),
        line(poly([(13.5, 12), (13.5, 15.5)], r=S.r)),
        shell(rect(18.5, 8, 3.5, 7, L(S, 0.5, 1.5))),
    ]


@icon("bow-knot", CAT, "Simple bow tied in a string with two loops and two tails",
      tags=["bow", "tie", "ribbon", "lace", "shoelace", "gift"])
def _(S):
    lp = "M12 12C9 4.5 2.5 5.5 3 10.5C3.5 15.5 9.5 14.5 12 12Z"
    return [
        shell(lp),
        shell(flip(lp)),
        line(poly([(12, 12), (9, 20)], r=S.r)),
        line(poly([(12, 12), (15, 20)], r=S.r)),
        dot(12, 12, 2),
    ]


@icon("tangled-string", CAT, "Messy loop of string knotted in the middle with loose ends",
      tags=["knot", "tangle", "twine", "yarn", "mess", "thread"])
def _(S):
    return [line("M2.5 17C8 17 15 14 16 9C17 4 10 3 8.5 8C7 13 14 18 19 15C21 13.5 21.5 11 21.5 9")]


@icon("tangled-cable", CAT, "Knot of tangled cable running to a plug",
      tags=["knot", "tangle", "cord", "wire", "mess", "charger"])
def _(S):
    return [
        line(seg(16.5, 2.5, 16.5, 5)),
        line(seg(19.5, 2.5, 19.5, 5)),
        shell(rect(15, 5, 6, 5, L(S, 0.5, 1.5))),
        line("M18 10V12C18 17 5 13 5 17C5 21 14 20 13 15C12 11 7 12 3 15"),
    ]


@icon("cable-organizer", CAT, "Row of cables held side by side in a slotted holder",
      tags=["cable clips", "cable management", "desk", "cord holder", "wires", "organiser"], aliases=["cable-organiser"])
def _(S):
    return [
        shell(rect(3, 13, 18, 6, L(S, 2, 3))),
        detail(seg(9, 13, 9, 19)),
        detail(seg(15, 13, 15, 19)),
        line("M6 13C6 9 4 7 4 3"), line("M12 13V3"), line("M18 13C18 9 20 7 20 3"),
    ]


@icon("paper-fastener", CAT, "Brass split pin with a round head and two legs spread apart",
      tags=["split pin", "brad", "paper brad", "stationery", "craft", "fixing"])
def _(S):
    top = union("M7.5 10C7.5 3.5 16.5 3.5 16.5 10Z", rect(3, 10, 18, 3.5, L(S, 0, 1.75)))
    return [
        shell(top),
        line(poly([(3.5, 18.5), (12, 14.5), (20.5, 18.5)], r=S.r)),
    ]


@icon("ball-chain", CAT, "Short length of beaded ball chain ending in a small connector",
      tags=["bead chain", "dog tag chain", "necklace", "keychain", "chain", "beads"])
def _(S):
    pts = [(4.5, 19.5), (4.5, 15.5), (5.5, 11.5), (8, 8.5), (11.5, 7), (15, 6.5)]
    return [dot(x, y, 1.6) for x, y in pts] + [
        shell(rect(17, 4, 4.5, 5, L(S, 0.5, 1.5))),
    ]


@icon("phone-strap", CAT, "Phone with a short wrist loop cord attached at the side",
      tags=["wrist strap", "lanyard", "cord", "loop", "mobile", "smartphone"])
def _(S):
    return [
        shell(rect(10, 3, 11, 18, S.R)),
        detail(seg(13.5, 6.5, 17.5, 6.5)),
        line(poly([(10, 17.5), (6.5, 17.5), (3.5, 14.5), (6.5, 11.5), (10, 11.5)], r=S.r + 1)),
    ]


# ============================================================================ chunk 2

@icon("over-door-hook", CAT, "Strap hook that loops over the top of a door with two hooks on the front",
      tags=["door hook", "hanger", "coat hook", "towel hook", "bathroom", "storage"])
def _(S):
    return [
        shell(rect(10, 8, 6, 13, L(S, 0.5, 1.5))),
        line("M6.5 19V6C6.5 3.75 8 3 10 3H15C17 3 18 3.75 18 6V11"),
        line(poly([(6.5, 10), (3.5, 10), (3.5, 8)], r=S.r)),
        line(poly([(6.5, 16), (3.5, 16), (3.5, 14)], r=S.r)),
    ]


@icon("adhesive-hook", CAT, "Small hook on a square adhesive pad",
      tags=["sticky hook", "wall hook", "peel and stick hook", "no drill", "hanging", "damage free"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail("M10 7V13.5C10 17 14 17 14.5 14C14.8 12.5 14 12 13 12"),
    ]


@icon("suction-hook", CAT, "Round suction cup with a hook underneath",
      tags=["suction cup", "bathroom hook", "tile hook", "window hook", "hanging", "no drill"])
def _(S):
    return [
        shell(circle(12, 8.5, 6)),
        detail(circle(12, 8.5, 2.25)),
        line("M12 14.5V19C12 21.5 14.5 21.5 16 20.5C17.5 19.5 17 18 16 18"),
    ]


@icon("bike-hook", CAT, "Wall hook holding a bicycle wheel by the rim",
      tags=["bike rack", "bicycle storage", "wall mount", "garage", "cycling", "wheel"])
def _(S):
    return [
        shell(circle(12, 15, 6.5)),
        detail(seg(12, 8.5, 12, 21.5)),
        detail(seg(5.5, 15, 18.5, 15)),
        line("M12 2.5V5.5C12 7.5 9.5 8 8 7.5"),
        line(seg(8.5, 2.5, 15.5, 2.5)),
    ]


@icon("hook-rail", CAT, "Wooden board with a row of four peg hooks",
      tags=["peg rail", "coat rack", "wall hooks", "hallway", "entryway", "hanging"])
def _(S):
    parts = [shell(rect(2.5, 3, 19, 5.5, S.R if S.name == "line" else 2.75))]
    for x in (5.5, 10, 14, 18.5):
        parts.append(line(seg(x, 8.5, x, 17)))
        parts.append(dot(x, 18.75, 1.75))
    return parts


@icon("curtain-ring", CAT, "Ring with a small clip hanging from a curtain pole",
      tags=["curtain clip", "drapery ring", "rod", "window", "home decor", "hanging"])
def _(S):
    return [
        line(poly([(2.5, 6), (21.5, 6)], r=S.r)),
        shell(circle(12, 7, 4)),
        shell(rect(9.5, 13.5, 5, 7.5, L(S, 0.5, 1.75))),
        detail(seg(12, 15.5, 12, 19)),
    ]


@icon("meat-hook", CAT, "S-shaped butcher hook with sharp pointed ends",
      tags=["butcher hook", "s hook", "hanging", "smokehouse", "kitchen", "carcass"])
def _(S):
    return [line("M6.5 8C6 2.5 16.5 2.5 16.5 8C16.5 12 8.5 12 8.5 16C8.5 21.5 18.5 21.5 18 16")]


@icon("wreath-hanger", CAT, "Thin metal hanger over a door top holding a wreath",
      tags=["door hanger", "wreath hook", "christmas", "holiday", "decoration", "front door"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(12, 3, 12, 8)),
        detail(circle(12, 14, 4.25)),
    ]


@icon("shepherds-hook", CAT, "Tall garden rod with a curled top holding a hanging lantern",
      tags=["garden hook", "plant hanger", "bird feeder pole", "lantern", "outdoor", "yard"])
def _(S):
    return [
        line("M7 21.5V6C7 3.5 9 2.5 11.5 2.5C14.5 2.5 16 4 16 6"),
        line(seg(16, 6, 16, 8)),
        shell(rect(12.5, 8, 7, 9.5, L(S, 1, 2.5))),
        detail(seg(12.5, 12.75, 19.5, 12.75)),
    ]


@icon("headphone-hook", CAT, "Under-desk hook holding a pair of headphones by the band",
      tags=["headphone stand", "desk hook", "gaming", "audio", "storage", "office"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 3.5, L(S, 0.5, 1.5))),
        line(seg(12, 6, 12, 9)),
        line("M6.5 19V14.5C6.5 11 9 9 12 9C15 9 17.5 11 17.5 14.5V19"),
        shell(rect(3.5, 14.5, 4, 6.5, L(S, 1, 2))),
        shell(rect(16.5, 14.5, 4, 6.5, L(S, 1, 2))),
    ]


@icon("scarf-hanger", CAT, "Hanger bar with round holes and a scarf threaded through one",
      tags=["scarf holder", "tie rack", "closet", "organiser", "wardrobe", "accessories"])
def _(S):
    bar = union(rect(2.5, 3, 19, 7.5, S.R), rect(9, 8, 6, 13, L(S, 0, 1.5)))
    return [
        shell(bar),
        dot(6, 6.75, 1.4),
        dot(18, 6.75, 1.4),
        detail(seg(9, 17.5, 15, 17.5)),
    ]


@icon("belt-hanger", CAT, "Hanger bar with small hooks holding three belts",
      tags=["belt rack", "tie hanger", "closet", "organiser", "wardrobe", "accessories"])
def _(S):
    parts = [shell(rect(2.5, 2.5, 19, 4.5, L(S, 0.5, 2)))]
    for x in (3.5, 10.5, 17.5):
        parts.append(line(seg(x + 1.5, 7, x + 1.5, 10)))
        parts.append(shell(rect(x, 10, 3, 11, L(S, 0.5, 1.5))))
    return parts


@icon("cascading-hanger", CAT, "Vertical chain of hangers linked one below another",
      tags=["stacked hangers", "space saving", "closet", "wardrobe", "clothes", "organiser"])
def _(S):
    parts = [line("M12 6V4.5C12 2.5 14.25 2.5 14.25 4")]
    for y in (6, 12, 18):
        parts.append(shell(poly([(5, y + 3), (12, y), (19, y + 3)], closed=True, r=S.r * 0.4), stroke_miterlimit="3"))
    return parts


@icon("shirt-on-hanger", CAT, "Button-up shirt draped on a coat hanger",
      tags=["shirt", "hanger", "wardrobe", "dry cleaning", "laundry", "clothes"])
def _(S):
    shirt = poly([(8.5, 8), (3, 10.5), (3, 14.5), (6, 14.5), (6, 21), (18, 21), (18, 14.5), (21, 14.5), (21, 10.5), (15.5, 8)],
                 closed=True, r=S.r)
    return [
        line("M12 6.5V5C12 3.5 13 2.75 14.25 2.75"),
        shell(shirt),
        detail(poly([(9.5, 8), (12, 11), (14.5, 8)], r=S.r * 0.5)),
        detail(seg(12, 11, 12, 21)),
    ]
# ============================================================================ chunk 3

@icon("hanging-shoe-organizer", CAT, "Fabric panel of pockets holding shoes, hung over a door",
      tags=["shoe rack", "over door", "storage", "closet", "entryway", "organiser"], aliases=["shoe-organiser"])
def _(S):
    return [
        line("M7.5 7V3H16.5V7"),
        shell(rect(3.5, 7, 17, 14, S.R)),
        detail(seg(12, 7, 12, 21)),
        detail(seg(3.5, 14, 20.5, 14)),
        sq(6, 9.5, 4, 2), sq(14, 9.5, 4, 2), sq(6, 16.5, 4, 2), sq(14, 16.5, 4, 2),
    ]


@icon("hanging-closet-organizer", CAT, "Fabric shelf column hanging from a rail with folded clothes in its cubbies",
      tags=["closet shelves", "hanging shelves", "wardrobe", "sweater storage", "folded clothes", "organiser"],
      aliases=["hanging-closet-organiser"])
def _(S):
    return [
        line(seg(2.5, 3, 21.5, 3)),
        line(seg(8, 3, 8, 5.5)),
        line(seg(16, 3, 16, 5.5)),
        shell(rect(5.5, 5.5, 13, 15.5, L(S, 1.5, 3))),
        detail(seg(5.5, 10.75, 18.5, 10.75)),
        detail(seg(5.5, 16, 18.5, 16)),
        sq(8, 7.75, 8, 1.75), sq(8, 13, 8, 1.75), sq(8, 18.25, 8, 1.75),
    ]


@icon("closet-rod", CAT, "Horizontal closet rod with end brackets and three hangers on it",
      tags=["wardrobe rail", "clothes rail", "hanging rod", "closet", "hangers", "storage"])
def _(S):
    parts = [
        line(seg(3, 2.5, 3, 8.5)),
        line(seg(21, 2.5, 21, 8.5)),
        line(seg(3, 5.5, 21, 5.5)),
    ]
    for x in (6.5, 12, 17.5):
        parts.append(line(seg(x, 5.5, x, 11.5)))
        parts.append(line(poly([(x - 3, 18.5), (x, 11.5), (x + 3, 18.5)], closed=True, r=S.r * 0.5), stroke_miterlimit="3"))
    return parts


@icon("wire-basket", CAT, "Open metal grid basket with two fold-down handles",
      tags=["metal basket", "mesh basket", "storage", "kitchen", "pantry", "shelf basket"])
def _(S):
    return [
        line("M4.5 10C4.5 5 7.5 4 10 4"),
        line("M19.5 10C19.5 5 16.5 4 14 4"),
        shell(poly([(3, 10), (21, 10), (18.5, 21), (5.5, 21)], closed=True, r=S.r * 0.6)),
        detail(seg(9.5, 10, 9, 21)),
        detail(seg(14.5, 10, 15, 21)),
        detail(seg(4.25, 15.5, 19.75, 15.5)),
    ]


@icon("sewing-basket", CAT, "Round lidded sewing basket with a needle and thread stuck in the lid",
      tags=["needlework", "craft basket", "thread", "needle", "tailor", "sewing kit"])
def _(S):
    lid = "M3.5 12C3.5 6.5 20.5 6.5 20.5 12Z"
    body = poly([(4.5, 12), (6, 21), (18, 21), (19.5, 12)], closed=True, r=S.r * 0.5)
    return [
        shell(union(lid, body)),
        detail(seg(5.5, 16.5, 18.5, 16.5)),
        line(seg(14, 7.5, 19, 2.5)),
        line("M19 2.5C22 4 21 7 18.5 7.25"),
    ]


@icon("back-basket", CAT, "Tall woven basket with shoulder straps, worn on the back",
      tags=["backpack basket", "carrying basket", "foraging", "harvest", "gathering", "market"])
def _(S):
    return [
        line("M7.25 6.5C4.5 8.5 4.5 13.5 7.25 16.5"),
        line("M16.75 6.5C19.5 8.5 19.5 13.5 16.75 16.5"),
        shell(poly([(7, 3.5), (17, 3.5), (16.5, 21), (7.5, 21)], closed=True, r=S.r * 0.6)),
        detail(seg(7.25, 9, 16.75, 9)),
        detail(seg(7.25, 15, 16.75, 15)),
    ]


@icon("log-basket", CAT, "Low wide woven basket with rope handles holding firewood logs",
      tags=["firewood", "fireplace", "wood basket", "logs", "hearth", "winter"])
def _(S):
    return [
        shell(circle(8.5, 7, 3.5)),
        shell(circle(15.5, 7, 3.5)),
        shell(poly([(4.5, 11), (19.5, 11), (18, 20.5), (6, 20.5)], closed=True, r=S.r * 0.5)),
        detail(seg(5.5, 15.75, 18.5, 15.75)),
        line("M4.5 12.5C2 12.5 2 16.5 4.75 16.5"),
        line("M19.5 12.5C22 12.5 22 16.5 19.25 16.5"),
    ]


@icon("cat-basket", CAT, "Round woven basket bed with a cat curled up inside",
      tags=["pet bed", "cat bed", "kitten", "sleeping cat", "pet", "cosy"])
def _(S):
    cat = union(circle(15.5, 8.5, 3.5), "M4.5 12C4.5 6 11.5 5 15 8L15.5 12Z",
                poly([(12.75, 6), (13.25, 2.75), (15.75, 5)], closed=True),
                poly([(15.25, 5), (17.75, 2.75), (18.25, 6)], closed=True))
    bowl = "M3 12H21C21 17.5 17 21 12 21C7 21 3 17.5 3 12Z"
    return [
        shell(union(cat, bowl)),
        dot(16.75, 8.75, 0.85),
        detail(seg(5, 16.25, 19, 16.25)),
    ]


@icon("wine-cradle", CAT, "Angled wicker holder cradling a wine bottle on its side",
      tags=["wine bottle holder", "wine basket", "wine rack", "bottle", "dining", "dinner party"])
def _(S):
    bottle = rot(poly([(2.5, 8), (11.5, 8), (15, 10.25), (21.5, 10.25), (21.5, 13.75), (15, 13.75), (11.5, 16), (2.5, 16)],
                      closed=True, r=S.r * 0.7), -14)
    return [
        shell(bottle),
        shell(poly([(3.5, 18), (16, 18), (14.5, 21.5), (5, 21.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("carry-caddy", CAT, "Open tote tray with a central handle and divided sections of supplies",
      tags=["cleaning caddy", "organiser", "supplies tray", "craft caddy", "carry handle", "storage"],
      aliases=["supply-caddy"])
def _(S):
    return [
        line("M9 11V4.5H15V11"),
        shell(rect(3, 11, 18, 10, L(S, 2, 3))),
        detail(seg(9, 11, 9, 21)),
        detail(seg(15, 11, 15, 21)),
    ]


@icon("wallet-chain", CAT, "Wallet with a curved chain running up to a belt clip",
      tags=["biker wallet", "chain wallet", "belt chain", "keychain", "accessories", "trucker"])
def _(S):
    parts = [shell(rect(3, 12.5, 13, 9, L(S, 1.5, 3))), detail(seg(3, 16, 11, 16))]
    for x, y in [(6.5, 9.5), (7.25, 6.5), (9.5, 4.25), (12.5, 3.5)]:
        parts.append(dot(x, y, 1.3))
    parts.append(shell(rect(15.5, 2.5, 5, 7, L(S, 0.5, 1.75))))
    return parts


@icon("phone-stand", CAT, "Angled stand holding a smartphone upright on a desk",
      tags=["phone holder", "desk stand", "mobile", "smartphone", "dock", "video call"])
def _(S):
    phone = rot(rect(7.5, 2.5, 9, 15, L(S, 2, 3)), 10, 12, 18)
    base = rect(4.5, 17, 15, 4, L(S, 1, 2))
    return [
        shell(union(phone, base)),
        detail(seg(7.5, 17, 16.5, 17)),
        detail(rseg(10.5, 6, 13.5, 6, 10, 12, 18)),
    ]


@icon("phone-ring-holder", CAT, "Back of a phone with a small fold-out ring grip",
      tags=["phone grip", "finger ring", "kickstand", "mobile", "smartphone", "accessory"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, S.R)),
        dot(8.75, 6.25, 1.25),
        detail(circle(12, 14, 3.25)),
        detail(seg(12, 9.5, 12, 10.75)),
    ]


@icon("phone-wallet", CAT, "Back of a phone with a stick-on card pocket holding a card",
      tags=["card holder", "phone case wallet", "credit card", "id holder", "mobile", "accessory"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, S.R)),
        dot(8.75, 6.25, 1.25),
        detail("M8 12.5V18.5H16V12.5"),
        detail("M10.5 15V8.5H14V15"),
    ]


@icon("phone-armband", CAT, "Stretch band around an upper arm holding a phone in a clear window",
      tags=["running armband", "jogging", "gym", "exercise", "workout", "phone holder"])
def _(S):
    return [
        line(seg(6, 2.5, 6, 6.5)), line(seg(18, 2.5, 18, 6.5)),
        line(seg(6, 17.5, 6, 21.5)), line(seg(18, 17.5, 18, 21.5)),
        shell(rect(3.5, 6.5, 17, 11, L(S, 2, 3.5))),
        detail(rect(8.5, 9, 7, 6, L(S, 0.5, 1.5))),
    ]


# ============================================================================ chunk 4

@icon("charging-dock", CAT, "Dock with slots holding a phone and an earbuds case, a cable behind",
      tags=["charging stand", "wireless charger", "earbuds", "phone dock", "desk", "power"])
def _(S):
    return [
        shell(rect(3.5, 3, 7, 11, L(S, 1.5, 2.5))),
        shell(rect(14, 7, 6, 7, L(S, 1, 2.25))),
        shell(rect(2.5, 14.5, 19, 6, L(S, 1.5, 3))),
        dot(12, 17.5, 1.1),
    ]


@icon("tablet-stand", CAT, "Folding stand holding a tablet at an angle",
      tags=["tablet holder", "tablet holder stand", "desk", "reading", "video", "kitchen"])
def _(S):
    tab = rot(rect(3.5, 3, 16, 11.5, L(S, 1.5, 2.75)), 8, 12, 9)
    return [
        shell(tab),
        line(poly([(5, 21), (10.5, 15)], r=S.r)),
        line(poly([(10.5, 15), (19, 21)], r=S.r)),
    ]


@icon("screen-protector", CAT, "Clear film being peeled onto a phone screen at one corner",
      tags=["tempered glass", "phone film", "screen guard", "mobile", "smartphone", "accessory"])
def _(S):
    return [
        shell(rect(3, 4.5, 14, 17, S.R)),
        detail("M7 10H12C18 10 20 7 20.5 2.5"),
    ]


@icon("clip-on-sunglasses", CAT, "Dark flip-up lenses clipped over a pair of regular glasses",
      tags=["flip-up shades", "sun clip", "eyewear", "glasses", "sun protection", "driving"])
def _(S):
    return [
        solid(rect(3.5, 2.5, 7.75, 6, L(S, 1.25, 3))),
        solid(rect(12.75, 2.5, 7.75, 6, L(S, 1.25, 3))),
        shell(circle(7, 15.5, 4.5)),
        shell(circle(17, 15.5, 4.5)),
        line(seg(11, 15, 13, 15)),
        line(seg(12, 8.5, 12, 14)),
    ]


@icon("eyeglass-screwdriver", CAT, "Tiny screwdriver beside the hinge of a pair of glasses",
      tags=["glasses repair", "optician", "tiny screw", "hinge", "eyewear", "fix"])
def _(S):
    driver = rot(union(rect(17, 12, 3.5, 9.5, L(S, 1, 1.75))), 25, 18.75, 16)
    return [
        shell(circle(8, 14.5, 5.5)),
        line(poly([(12.5, 9.5), (14, 6), (21, 6)], r=S.r)),
        dot(14, 6, 1),
        shell(driver),
        line(rseg(18.75, 6.5, 18.75, 12, 25, 18.75, 16)),
    ]


@icon("tobacco-pipe", CAT, "Curved smoking pipe with a round bowl and a long stem",
      tags=["pipe", "smoking", "briar", "gentleman", "tobacco", "vintage"])
def _(S):
    bowl = rect(3, 3.5, 9, 12, L(S, 2, 4))
    stem = rot(rect(6, 13, 16, 4, L(S, 0.5, 2)), -12, 6, 15)
    return [
        shell(union(bowl, stem)),
        detail(seg(5.5, 6.75, 9.5, 6.75)),
    ]


@icon("cigar", CAT, "Thick rolled cigar with a band near one end and a glowing tip",
      tags=["smoking", "tobacco", "havana", "luxury", "celebration", "lounge"])
def _(S):
    body = rot(poly([(6.5, 9.5), (15, 9.5), (21, 11.5), (21, 13.5), (15, 15.5), (6.5, 15.5)], closed=True, r=L(S, 0.3, 2.5)), -28)
    return [
        shell(body),
        detail(rseg(12.5, 9.5, 12.5, 15.5, -28)),
        line(rseg(1.25, 9.5, 3.75, 10.5, -28)),
        line(rseg(0.75, 12.5, 3.5, 12.5, -28)),
        line(rseg(1.25, 15.5, 3.75, 14.5, -28)),
    ]


@icon("cigarette", CAT, "Single cigarette with a filter end and a wisp of smoke",
      tags=["smoking", "tobacco", "smoke", "nicotine", "butt", "habit"])
def _(S):
    body = rot(rect(2, 12, 16, 3.5, L(S, 0.5, 1.75)), -30, 10, 12)
    return [
        shell(body),
        detail(rseg(7, 12, 7, 15.5, -30, 10, 12)),
        line("M18 8C16.5 6 20 5 18.75 2.5"),
    ]


@icon("cigar-cutter", CAT, "Guillotine cigar cutter with a central hole and two finger holes",
      tags=["cigar tip", "guillotine", "smoking accessory", "humidor", "tobacconist", "luxury"])
def _(S):
    body = union(circle(6.25, 12, 4.25), circle(17.75, 12, 4.25), rect(6.25, 7.5, 11.5, 9, 0))
    return [
        shell(minus(body, circle(5.75, 12, 1.5), circle(18.25, 12, 1.5), circle(12, 12, 2.5))),
    ]


@icon("rolling-paper", CAT, "Thin sheet of rolling paper with a line of loose tobacco along it",
      tags=["roll up", "papers", "tobacco", "hand rolled", "sheet", "smoking"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 19, 11, L(S, 1, 2.5))),
        detail(seg(2.5, 9.5, 21.5, 9.5)),
        dot(6.25, 13.5, 1.1), dot(10, 13.5, 1.1), dot(13.75, 13.5, 1.1), dot(17.5, 13.5, 1.1),
    ]


@icon("hookah", CAT, "Tall water pipe with a glass base, a bowl on top and a coiled hose",
      tags=["shisha", "narghile", "water pipe", "lounge", "smoking", "arabic"])
def _(S):
    return [
        shell(poly([(6, 2.5), (14, 2.5), (12.5, 7), (7.5, 7)], closed=True, r=S.r * 0.5)),
        line(seg(10, 7, 10, 13)),
        shell(circle(10, 17, 4.25)),
        line("M10.75 10C18 9 21 13 20.5 21"),
    ]


@icon("vape", CAT, "Slim vaping pen with a mouthpiece and a cloud of vapor",
      tags=["e-cigarette", "vaping", "vapor", "electronic cigarette", "pen", "nicotine"])
def _(S):
    cloud = union(circle(8.5, 8, 2.5), circle(13, 6.25, 3), circle(17.5, 8.25, 2.5), rect(8.5, 8, 11.5, 2.5, 1.25))
    return [
        shell(cloud),
        shell(rect(2.5, 14.5, 15, 5, L(S, 1.5, 2.5))),
        shell(rect(17.5, 15.75, 4, 2.5, L(S, 0.5, 1.25))),
    ]


@icon("ashtray", CAT, "Round shallow dish with notches on the rim and a resting cigarette",
      tags=["cigarette butt", "smoking", "ash", "tray", "bar", "lounge"])
def _(S):
    return [
        line("M18.5 7C17 5 20.5 4 19 2.5"),
        shell(rect(5.5, 7.5, 12, 3, L(S, 0.5, 1.5))),
        shell(poly([(2.5, 11.5), (21.5, 11.5), (19, 20), (5, 20)], closed=True, r=S.r)),
        detail(seg(10, 11.5, 14, 11.5)),
    ]


@icon("nicotine-patch", CAT, "Square skin patch with rounded corners stuck on an upper arm",
      tags=["transdermal patch", "quit smoking", "stop smoking", "medication", "skin patch", "cessation"])
def _(S):
    return [
        line("M6 2.5C3.5 8 3.5 16 6 21.5"),
        line("M18 2.5C20.5 8 20.5 16 18 21.5"),
        shell(rect(8, 8, 8, 8, L(S, 1.5, 3))),
        dot(12, 12, 1.3),
    ]


@icon("ring-holder", CAT, "Tapered cone stand with rings stacked on it",
      tags=["ring stand", "jewellery tree", "jewelry display", "rings", "dresser", "accessories"])
def _(S):
    return [
        shell(poly([(12, 3), (14.25, 17), (9.75, 17)], closed=True, r=S.r * 0.5), stroke_miterlimit="3"),
        shell(rect(5.5, 17, 13, 3.5, L(S, 1, 1.75))),
        line(ellipse(12, 8, 4, 1.6)),
        line(ellipse(12, 12.5, 5, 1.75)),
    ]


# ============================================================================ chunk 5

@icon("watch-winder", CAT, "Box with a turning cushion holding a wristwatch and rotation arrows",
      tags=["automatic watch", "watch box", "timepiece", "collector", "luxury", "rotating"])
def _(S):
    return [
        shell(rect(3, 11, 18, 10, L(S, 2, 3.5))),
        detail(circle(12, 16, 2.75)),
        line(arc(12, 12, 7, 215, 320)),
        line(poly([(15.5, 4.5), (18.25, 6.5), (14.75, 8.25)], r=S.r * 0.3)),
    ]


@icon("jewelry-roll", CAT, "Fabric roll partly unrolled with rings and earrings in pockets",
      tags=["jewellery roll", "travel organiser", "jewelry case", "rings", "earrings", "packing"],
      aliases=["jewellery-roll"])
def _(S):
    return [
        shell(circle(6.75, 12, 4.75)),
        detail(circle(6.75, 12, 1.25)),
        shell(rect(11.5, 6, 10, 12, L(S, 1, 2))),
        detail(seg(11.5, 12, 21.5, 12)),
        dot(15, 9, 1.1), dot(18.25, 9, 1.1),
        dot(16.5, 15, 1.1),
    ]


@icon("drawer-organizer", CAT, "Top-down view of an open drawer divided into small compartments",
      tags=["drawer divider", "drawer insert", "tray", "kitchen drawer", "tidy", "storage"],
      aliases=["drawer-organiser"])
def _(S):
    return [
        shell(rect(2.5, 4, 19, 16, S.R)),
        detail(seg(9, 4, 9, 20)),
        detail(seg(9, 12, 21.5, 12)),
    ]


@icon("under-bed-storage", CAT, "Low flat zipped storage box sliding under a bed frame",
      tags=["underbed box", "storage bag", "bedroom", "closet", "zip", "space saving"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 4, L(S, 0.5, 2))),
        line(seg(4.5, 7.5, 4.5, 21)),
        line(seg(19.5, 7.5, 19.5, 21)),
        shell(rect(8, 12.5, 8, 6.5, L(S, 1, 2.5))),
        detail(seg(8, 15.75, 16, 15.75)),
    ]


@icon("bin-label", CAT, "Storage bin with a label holder on the front",
      tags=["tote label", "storage box", "organising", "labelled bin", "pantry", "garage"],
      aliases=["tote-label"])
def _(S):
    return [
        shell(poly([(3, 5), (21, 5), (19, 20.5), (5, 20.5)], closed=True, r=S.r * 0.7)),
        detail(seg(3.5, 9, 20.5, 9)),
        detail(rect(8, 12.25, 8, 4.25, L(S, 0.5, 1.5))),
    ]


@icon("boot-tray", CAT, "Shallow rimmed tray holding a pair of wet boots",
      tags=["shoe tray", "mud room", "entryway", "rain boots", "wellies", "winter"])
def _(S):
    boot = [(3.5, 3), (8, 3), (8, 10.5), (11.5, 11.5), (11.5, 15), (3.5, 15)]
    boot2 = [(x + 9.5, y) for x, y in boot]
    return [
        shell(union(poly(boot, closed=True, r=S.r * 0.7), poly(boot2, closed=True, r=S.r * 0.7))),
        shell(rect(2.5, 15.5, 19, 5, L(S, 1, 2.5))),
    ]


@icon("hand-fan", CAT, "Round rigid paddle fan with a short handle and radiating ribs",
      tags=["paddle fan", "uchiwa", "cooling", "summer", "handheld fan", "festival"])
def _(S):
    return [
        shell(union(circle(12, 9.5, 7), rect(10.5, 15, 3, 6.5, L(S, 0.5, 1.5)))),
        detail(seg(12, 13.5, 12, 5)),
        detail(seg(12, 13.5, 7.5, 7.5)),
        detail(seg(12, 13.5, 16.5, 7.5)),
    ]


@icon("neck-fan", CAT, "Horseshoe-shaped fan worn around the neck with vents on both arms",
      tags=["bladeless fan", "portable fan", "wearable fan", "cooling", "summer", "hands free"])
def _(S):
    ring = minus(circle(12, 10.5, 9.5), circle(12, 10.5, 5), rect(8, 12, 8, 12))
    return [
        shell(ring),
        dot(4.5, 13.25, 0.9), dot(5.75, 16.25, 0.9),
        dot(19.5, 13.25, 0.9), dot(18.25, 16.25, 0.9),
    ]


@icon("cooling-towel", CAT, "Towel draped around a neck with a small snowflake beside it",
      tags=["cold towel", "neck towel", "heat relief", "summer", "sports", "chill"])
def _(S):
    towel = "M2.5 4H14.5V21H10.5V11.5Q10.5 9.5 8.5 9.5Q6.5 9.5 6.5 11.5V21H2.5Z"
    sn = []
    for a in (90, 150, 210):
        pass
    return [
        shell(towel),
        detail(seg(2.5, 16.5, 6.5, 16.5)),
        line(seg(19, 10, 19, 17)),
        line(seg(15.9, 11.75, 22.1, 15.25)),
        line(seg(15.9, 15.25, 22.1, 11.75)),
    ]


@icon("furniture-pads", CAT, "Chair leg with a round felt pad on its foot",
      tags=["felt pads", "floor protector", "chair glides", "scratch guard", "hardwood", "furniture"])
def _(S):
    return [
        shell(union(rect(8.5, 2.5, 7, 12.5, L(S, 0.5, 1.5)), rect(5, 15, 14, 4, L(S, 1, 2)))),
        detail(seg(8.5, 15.5, 15.5, 15.5)),
        line(seg(2.5, 21.5, 21.5, 21.5)),
    ]


@icon("curtain-tieback", CAT, "Curtain gathered to one side by a tasseled cord",
      tags=["curtain tie", "drapery", "window dressing", "tassel", "home decor", "living room"])
def _(S):
    return [
        line(seg(2.5, 3, 21.5, 3)),
        shell("M3.5 5.5H14C14 9 10.5 10.5 10.5 12.5C10.5 14.5 14 16 14 21H3.5Z"),
        line(seg(10.5, 12.5, 18, 12.5)),
        line(seg(18, 12.5, 18, 16)),
        dot(18, 18, 2),
    ]


@icon("valet-tray", CAT, "Shallow tray holding a watch, a key and a coin",
      tags=["catchall", "entryway tray", "key tray", "dresser", "everyday carry", "wallet tray"])
def _(S):
    return [
        shell(circle(7.5, 7, 3.25)),
        line(seg(7.5, 2.5, 7.5, 3.75)),
        shell(circle(16.5, 8.5, 2.5)),
        dot(12.25, 9, 1.2),
        shell(poly([(2.5, 12), (21.5, 12), (19.5, 20.5), (4.5, 20.5)], closed=True, r=S.r * 0.7)),
    ]


@icon("paper-straw", CAT, "Drinking straw with diagonal stripes standing in a cup",
      tags=["eco straw", "drinking straw", "biodegradable", "cup", "cocktail", "party"])
def _(S):
    straw = rot(rect(10, 1.5, 4, 12), 14, 12, 12)
    return [
        shell(straw),
        detail(rseg(10, 4.5, 14, 6.5, 14, 12, 12)),
        detail(rseg(10, 9, 14, 11, 14, 12, 12)),
        shell(poly([(5.5, 10), (18.5, 10), (16.5, 21), (7.5, 21)], closed=True, r=S.r * 0.6)),
    ]


@icon("bedsheet", CAT, "Flat sheet folded into a neat rectangle with a hem line along one edge",
      tags=["bed linen", "sheets", "bedding", "folded", "laundry", "bedroom"])
def _(S):
    return [
        shell(rect(3, 5.5, 18, 13, L(S, 1.5, 3))),
        detail(seg(3, 9.5, 21, 9.5)),
        detail(seg(12, 9.5, 12, 18.5)),
    ]


@icon("fitted-sheet", CAT, "Fitted sheet with elasticated corners pulled over a mattress corner",
      tags=["mattress cover", "bed linen", "elastic corners", "bedding", "bedroom", "sheets"])
def _(S):
    return [
        shell(poly([(3, 9), (12, 4.5), (21, 9), (21, 15), (12, 19.5), (3, 15)], closed=True, r=L(S, 0, 2.5))),
        detail(poly([(3.5, 9.25), (12, 13.5), (20.5, 9.25)], r=S.r)),
        detail(seg(12, 13.5, 12, 19.5)),
    ]


@icon("bolster-pillow", CAT, "Long cylindrical pillow with gathered ends lying on a bed",
      tags=["neck roll", "cushion", "bedding", "yoga bolster", "sofa", "cylinder pillow"])
def _(S):
    body = union(rect(6, 6.5, 12, 10, L(S, 2, 4)),
                 poly([(6.5, 9.5), (2.5, 7), (2.5, 16), (6.5, 13.5)], closed=True),
                 poly([(17.5, 9.5), (21.5, 7), (21.5, 16), (17.5, 13.5)], closed=True))
    return [
        shell(body),
        detail(seg(6, 6.5, 6, 16.5)),
        detail(seg(18, 6.5, 18, 16.5)),
        line(seg(2.5, 20.5, 21.5, 20.5)),
    ]


@icon("bed-rail", CAT, "Low fold-down safety rail fixed along the side of a bed",
      tags=["safety rail", "toddler bed", "fall prevention", "bed guard", "child safety", "hospital bed"])
def _(S):
    return [
        shell(rect(4, 3.5, 16, 9.5, L(S, 2, 3.5))),
        detail(seg(8.5, 3.5, 8.5, 13)),
        detail(seg(12, 3.5, 12, 13)),
        detail(seg(15.5, 3.5, 15.5, 13)),
        line(seg(2.5, 17, 21.5, 17)),
        line(seg(4.5, 17, 4.5, 21.5)),
        line(seg(19.5, 17, 19.5, 21.5)),
    ]


@icon("kamidana", CAT, "Small wall shelf shrine with a miniature roof and a hanging rope",
      tags=["shinto", "household shrine", "japanese", "altar", "shelf shrine", "kami"])
def _(S):
    return [
        line(poly([(10, 2.5), (12, 5), (14, 2.5)])),
        shell(union(poly([(3, 11), (12, 5.5), (21, 11)], closed=True, r=S.r * 0.4), rect(6.5, 10, 11, 8.5, 0)),
              stroke_miterlimit="2"),
        detail(seg(6.5, 13.5, 17.5, 13.5)),
        detail(poly([(10, 13.5), (10, 16), (11.5, 17.5)])),
        detail(poly([(14, 13.5), (14, 16), (12.5, 17.5)])),
        line(seg(2.5, 21, 21.5, 21)),
    ]


@icon("omikuji", CAT, "Folded paper fortune strip tied in a knot on a string line",
      tags=["fortune", "temple", "shrine", "japanese", "paper strip", "luck"])
def _(S):
    return [
        line(seg(2.5, 4.5, 21.5, 4.5)),
        shell(rect(8.5, 8, 7, 13, L(S, 0.5, 2))),
        detail(seg(12, 11.5, 12, 17.5)),
        dot(12, 4.5, 2),
        line(seg(12, 4.5, 12, 8)),
    ]
