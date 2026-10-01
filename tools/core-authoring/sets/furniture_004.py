"""TypeIcon Core: furniture (batch furniture_004).

Original drawings of outdoor shade and living structures, interior trim and surfaces, rooms, lighting,
doors, stairs, seating and play furniture. Masses are shells, inner divisions are details, legs and
frames are open strokes.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "furniture"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    """Container corner radius for the style, optionally capped for small shapes."""
    if cap is None:
        return S.R
    return min(S.R, cap) if S.name == "rounded" else min(S.R, cap) * 0.4


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def mark(d) -> Part:
    return Part("dot", d)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def flip(d):
    """Mirror a d-string across the vertical centre line."""
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


# ============================================================================ outdoor shade and living

@icon("shade-sail", CAT, "Triangular fabric sail stretched between three posts over a patio.",
      tags=["sun shade", "shade cloth", "canopy", "garden shade", "outdoor", "patio", "sail shade"])
def _(S):
    return [
        shell(poly([(4, 5.5), (20, 3.5), (13.5, 13)], closed=True, r=S.r * 0.6)),
        line(seg(4, 5.5, 4, 21)), line(seg(20, 3.5, 20, 21)), line(seg(13.5, 13, 13.5, 21)),
    ]


@icon("window-awning", CAT, "Striped fabric awning with a scalloped edge projecting over a window.",
      tags=["awning", "canopy", "sun shade", "shop front", "window cover", "cafe", "storefront"])
def _(S):
    top = "M5 3H19L22 9A2.5 2.5 0 0 1 17 9A2.5 2.5 0 0 1 12 9A2.5 2.5 0 0 1 7 9A2.5 2.5 0 0 1 2 9Z"
    return [
        shell(top),
        detail(seg(15.5, 3, 17, 9)), detail(seg(12, 3, 12, 9)), detail(seg(8.5, 3, 7, 9)),
        shell(rect(5, 15, 14, 6, rr(S, 2))),
        detail(seg(12, 15, 12, 21)),
    ]


@icon("cantilever-umbrella", CAT, "Patio umbrella hanging from a curved side arm on a post with a base.",
      tags=["offset umbrella", "patio umbrella", "garden umbrella", "parasol", "outdoor", "sun shade"])
def _(S):
    return [
        line(poly([(4, 21), (4, 4), (15, 4), (15, 6.5)], r=S.r)),
        line(seg(2, 21, 8, 21)),
        shell("M7 14A8 7.5 0 0 1 23 14Z"),
        detail(seg(15, 6.5, 15, 14)),
    ]


@icon("decking", CAT, "Outdoor wooden deck of parallel boards in perspective with a short railing.",
      tags=["deck", "wood deck", "terrace", "boardwalk", "patio", "outdoor floor", "railing"])
def _(S):
    return [
        line(seg(8, 5, 20, 5)),
        line(seg(8, 5, 8, 12)), line(seg(14, 5, 14, 12)), line(seg(20, 5, 20, 12)),
        shell(poly([(2, 21), (6, 13), (22, 13), (18, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(7.3, 21, 11.3, 13)), detail(seg(12.7, 21, 16.7, 13)),
    ]


@icon("patio", CAT, "Paved outdoor area of square slabs with a small table and a parasol.",
      tags=["paving", "terrace", "garden furniture", "outdoor seating", "backyard", "slabs", "parasol"])
def _(S):
    return [
        shell("M6 9A6 6 0 0 1 18 9Z"),
        line(seg(12, 9, 12, 16)),
        line(seg(8.5, 12.5, 15.5, 12.5)),
        shell(poly([(2, 21), (5, 16), (19, 16), (22, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(9.5, 16, 8.5, 21)), detail(seg(14.5, 16, 15.5, 21)),
    ]


@icon("sunroom", CAT, "Glass-walled garden room with a peaked glazed roof divided into panes.",
      tags=["conservatory", "solarium", "glass room", "garden room", "extension", "orangery", "home addition"])
def _(S):
    return [
        shell(poly([(2.5, 21), (2.5, 11), (12, 4.2), (21.5, 11), (21.5, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(8.5, 7.6, 8.5, 21)), detail(seg(15.5, 7.6, 15.5, 21)),
        detail(seg(2.5, 14.8, 21.5, 14.8)),
    ]


@icon("exposed-beams", CAT, "Room ceiling in perspective with thick wooden beams running across it.",
      tags=["ceiling beams", "rafters", "timber beams", "rustic", "barn style", "vaulted ceiling", "wooden ceiling"])
def _(S):
    return [
        shell(poly([(2, 3), (22, 3), (16, 11), (8, 11)], closed=True, r=S.r * 0.3)),
        detail(seg(10.3, 3, 9.7, 11)), detail(seg(13.7, 3, 14.3, 11)),
        detail(seg(5.6, 7.5, 18.4, 7.5)),
        line(seg(2, 3, 2, 21)), line(seg(22, 3, 22, 21)),
    ]


@icon("wainscoting", CAT, "Lower wall covered in raised rectangular panels with a chair rail on top.",
      tags=["wall paneling", "wall panels", "chair rail", "wood paneling", "wall trim", "interior", "dado"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 18, rr(S, 3))),
        detail(seg(2.5, 10, 21.5, 10)),
        detail(rect(5.5, 13, 5, 5, rr(S, 1))),
        detail(rect(13.5, 13, 5, 5, rr(S, 1))),
    ]


@icon("crown-molding", CAT, "Close view of the corner where wall meets ceiling with a stepped curved molding profile.",
      tags=["cornice", "ceiling trim", "coving", "moulding", "wall trim", "interior", "carpentry"])
def _(S):
    return [
        shell("M2 3H21V6.5H18Q8 6.5 6.5 14H2Z"),
        line(seg(2, 14, 2, 21)),
    ]


@icon("baseboard", CAT, "Wall meeting the floor with a tall profiled skirting board running along the bottom.",
      tags=["skirting board", "skirting", "wall trim", "floor trim", "moulding", "interior", "carpentry"])
def _(S):
    return [
        shell("M2 21V6H5.5Q5.5 9.5 10 9.5V21Z"),
        line(seg(2, 6, 2, 2.5)),
        line(seg(10, 21, 22, 21)),
        detail(seg(2, 14.5, 10, 14.5)),
    ]


@icon("ceiling-rose", CAT, "Round ornamental ceiling medallion with a petal pattern and a light cord hanging from it.",
      tags=["ceiling medallion", "ceiling plate", "chandelier mount", "plasterwork", "decorative", "ornament", "pendant"])
def _(S):
    body = circle(12, 8, 7) if S.name == "rounded" else poly(regular(12, 8, 7.4, 8, -90 + 22.5), closed=True)
    rays = [detail(seg(*polar(12, 8, 3.2, a), *polar(12, 8, 5.6, a))) for a in range(0, 360, 60)]
    return [
        shell(body), dot(12, 8, 1.2), *rays,
        line(seg(12, 15, 12, 17.5)),
        shell(circle(12, 20, 2.2)),
    ]


@icon("wall-niche", CAT, "Arched recess set into a wall holding a small vase.",
      tags=["recess", "alcove", "arched niche", "wall recess", "display nook", "decor", "shelf alcove"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        detail("M7 19V10A5 5 0 0 1 17 10V19Z"),
        mark("M10.3 17.5Q9 15 11 13.2V11.2H13V13.2Q15 15 13.7 17.5Z"),
    ]


@icon("subway-tiles", CAT, "Wall of glossy rectangular tiles laid in an offset brick pattern.",
      tags=["brick tiles", "metro tiles", "wall tiles", "backsplash", "tiling", "kitchen wall", "bathroom wall"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 18, rr(S, 2.5))),
        detail(seg(2.5, 9, 21.5, 9)), detail(seg(2.5, 15, 21.5, 15)),
        detail(seg(12, 3, 12, 9)), detail(seg(7.5, 9, 7.5, 15)), detail(seg(16.5, 9, 16.5, 15)),
        detail(seg(12, 15, 12, 21)),
    ]


@icon("terrazzo", CAT, "Square slab speckled with irregular chips of different sizes.",
      tags=["terrazzo floor", "speckled", "stone chips", "composite stone", "flooring", "countertop", "surface"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        mark("M6 8L9 6.5L10 9L7.3 10.3Z"),
        mark("M14 6.5L17 7.5L15.8 10Z"),
        mark(circle(16.5, 14.5, 1.6)),
        mark("M9 14L11.8 15L10.6 17.8L8 16.8Z"),
        mark(circle(13, 10.8, 0.9)),
        mark(circle(6.5, 13.5, 0.9)),
    ]


@icon("bathroom", CAT, "Bathroom scene with a bathtub, a faucet and a round mirror on the wall.",
      tags=["bath", "restroom", "washroom", "bathtub", "wc", "toilet room", "home room"])
def _(S):
    return [
        shell("M2 13H22V15A5 5 0 0 1 17 20H7A5 5 0 0 1 2 15Z"),
        line(seg(6, 20, 5, 22)), line(seg(18, 20, 19, 22)),
        line(poly([(4, 13), (4, 6), (8, 6)], r=S.r)),
        shell(circle(17, 6, 3.5)),
    ]


# ============================================================================ rooms and workspaces

@icon("kitchen", CAT, "Kitchen scene with wall cabinets above and a counter with a stove holding a pot.",
      tags=["kitchen room", "cooking", "cabinets", "counter", "stove", "home room", "cookery"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 4, rr(S, 2))),
        detail(seg(12, 2.5, 12, 6.5)),
        shell(rect(2.5, 15, 19, 6, rr(S, 2))),
        detail(seg(14, 15, 14, 21)),
        shell(rect(5, 10.5, 7, 4.5, rr(S, 1.5))),
        line(seg(12, 12.5, 15, 12.5)),
    ]


@icon("pantry", CAT, "Walk-in closet of shelves stocked with jars, cans and a sack on the floor.",
      tags=["larder", "food storage", "kitchen storage", "stockroom", "cupboard", "groceries", "shelves"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        detail(seg(2.5, 9.5, 21.5, 9.5)), detail(seg(2.5, 15.5, 21.5, 15.5)),
        sq(5.5, 5.3, 3, 2.7, 0.5), sq(10.2, 4.6, 3.4, 3.4, 0.5), mark(circle(17.3, 6.6, 1.4)),
        sq(6, 11.6, 3.4, 2.7, 0.5), mark(circle(13.5, 12.8, 1.5)),
        mark("M8.5 19.3Q7 17.3 9.5 16.9H14.5Q17 17.3 15.5 19.3Z"),
    ]


@icon("cubicle", CAT, "Office cubicle with low partition walls around a desk with a monitor.",
      tags=["office cubicle", "workstation", "partition", "open plan office", "work pod", "desk", "workspace"])
def _(S):
    return [
        line(poly([(2.5, 21), (2.5, 4), (21.5, 4), (21.5, 21)], r=S.r)),
        shell(rect(8.5, 8.5, 7, 4.5, rr(S, 1.5))),
        line(seg(12, 13, 12, 15)),
        line(seg(5.5, 16, 18.5, 16)),
        line(seg(7, 16, 7, 21)), line(seg(17, 16, 17, 21)),
    ]


@icon("dressing-room", CAT, "Vanity mirror framed by round bulbs above a small stool.",
      tags=["makeup mirror", "hollywood mirror", "vanity", "backstage", "changing room", "green room", "lighted mirror"])
def _(S):
    bulbs = [dot(x, y, 1.2) for x in (3.4, 20.6) for y in (5, 9.5, 14)]
    return [
        shell(rect(6.5, 3, 11, 13, rr(S, 3))),
        *bulbs,
        shell(rect(7.5, 17.5, 9, 2, rr(S, 1))),
        line(seg(9, 19.5, 8, 22)), line(seg(15, 19.5, 16, 22)),
    ]


@icon("furniture-store", CAT, "Shop front with a striped awning and a large window showing a sofa inside.",
      tags=["furniture shop", "home store", "showroom", "retail", "interiors", "sofa shop", "store front"])
def _(S):
    top = "M5 2.5H19L22 8A2.5 2.5 0 0 1 17 8A2.5 2.5 0 0 1 12 8A2.5 2.5 0 0 1 7 8A2.5 2.5 0 0 1 2 8Z"
    return [
        shell(top),
        detail(seg(15.5, 2.5, 17, 8)), detail(seg(12, 2.5, 12, 8)), detail(seg(8.5, 2.5, 7, 8)),
        shell(rect(3, 11.5, 18, 9.5, rr(S, 2))),
        mark("M8 14.5H16V17H18V19.3H6V17H8Z"),
    ]


@icon("dollhouse", CAT, "Open-fronted toy house with a peaked roof and small rooms on two floors.",
      tags=["doll house", "toy house", "miniature house", "play house", "kids toy", "playroom", "model home"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 10), (12, 3), (21, 10), (21, 21)], closed=True, r=S.r)),
        detail(seg(3, 15.5, 21, 15.5)),
        detail(seg(12, 15.5, 12, 21)),
        mark(circle(12, 11.3, 1.5)),
    ]


@icon("height-chart", CAT, "Tall wall ruler with measurement ticks, a few marker lines and a small star at the top.",
      tags=["growth chart", "kids height", "wall ruler", "measuring height", "growth ruler", "child growth", "nursery decor"])
def _(S):
    star = poly([polar(9.5, 6.3, 2.6 if i % 2 == 0 else 1.1, -90 + i * 36) for i in range(10)], closed=True)
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 2.5))),
        mark(star),
        detail(seg(13, 8, 17, 8)), detail(seg(15, 12, 17, 12)), detail(seg(13, 16, 17, 16)), detail(seg(15, 20, 17, 20)),
        detail(seg(8, 13, 11, 13)),
    ]


@icon("office-pod", CAT, "Enclosed soundproof booth with a seat and a small desk inside.",
      tags=["phone booth", "work booth", "soundproof booth", "focus pod", "meeting pod", "quiet room", "privacy booth"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 3.5))),
        detail(poly([(6.5, 8.5), (6.5, 16.5), (10.5, 16.5)], r=S.r)),
        detail(seg(11.5, 12.5, 17.5, 12.5)), detail(seg(14.5, 12.5, 14.5, 17)),
    ]


@icon("hot-desk", CAT, "Shared desk with a laptop and a small reservation calendar tag.",
      tags=["shared desk", "flexible workspace", "coworking", "desk booking", "hotdesking", "office desk"])
def _(S):
    return [
        shell(rect(2.5, 15, 19, 2.5, rr(S, 1))),
        line(seg(4.5, 17.5, 4.5, 21.5)), line(seg(19.5, 17.5, 19.5, 21.5)),
        shell(rect(4.5, 7.5, 8.5, 6, rr(S, 1.5))),
        shell(rect(15.5, 5, 5, 7, rr(S, 1))),
        detail(seg(15.5, 7.8, 20.5, 7.8)),
    ]


@icon("luggage-rack", CAT, "Folding stand on crossed legs with straps across the top holding a suitcase.",
      tags=["suitcase stand", "bag rack", "hotel room", "baggage stand", "luggage stand", "guest room", "folding rack"])
def _(S):
    return [
        line(poly([(10, 5.5), (10, 3), (14, 3), (14, 5.5)], r=S.r)),
        shell(rect(5.5, 5.5, 13, 7, rr(S, 2))),
        line(seg(3, 14.5, 21, 14.5)),
        line(seg(6, 14.5, 18, 21.5)), line(seg(18, 14.5, 6, 21.5)),
    ]


@icon("draft-stopper", CAT, "Long stuffed fabric tube lying along the bottom of a door.",
      tags=["door snake", "draught excluder", "door draft blocker", "door stopper", "energy saving", "insulation", "winter"])
def _(S):
    return [
        line(poly([(5, 16.5), (5, 3), (19, 3), (19, 16.5)], r=S.r)),
        dot(16, 10, 1.3),
        shell(rect(2.5, 16.5, 19, 5, 2.5)),
        detail(seg(7.5, 16.5, 7.5, 21.5)), detail(seg(12, 16.5, 12, 21.5)), detail(seg(16.5, 16.5, 16.5, 21.5)),
    ]


@icon("headboard", CAT, "Upholstered bed headboard with button tufting standing on two short legs.",
      tags=["bed head", "tufted headboard", "bedroom", "bed frame", "upholstered", "padded headboard", "bed back"])
def _(S):
    return [
        shell(rect(3.5, 3.5, 17, 13.5, rr(S, 5))),
        dot(8, 8, 1.2), dot(12, 8, 1.2), dot(16, 8, 1.2), dot(10, 12.5, 1.2), dot(14, 12.5, 1.2),
        line(seg(6.5, 17, 6.5, 21.5)), line(seg(17.5, 17, 17.5, 21.5)),
    ]


@icon("arched-mirror", CAT, "Tall floor mirror with a rounded arched top and a thin frame leaning on a wall.",
      tags=["floor mirror", "full length mirror", "arch mirror", "standing mirror", "dressing mirror", "leaning mirror", "bedroom decor"])
def _(S):
    return [
        shell("M6 19.5V9A6 6 0 0 1 18 9V19.5Z"),
        detail(seg(9.5, 15, 13, 11.5)),
        line(seg(8, 19.5, 7, 22)), line(seg(16, 19.5, 17, 22)),
    ]


@icon("oval-frame", CAT, "Oval portrait frame topped with a ribbon bow and holding a head and shoulders silhouette.",
      tags=["portrait frame", "cameo frame", "picture frame", "vintage frame", "photo frame", "victorian", "wall decor"])
def _(S):
    bow = [solid(poly([(12, 4.5), (7.5, 2.5), (7.5, 6.5)], closed=True, r=S.r * 0.6)),
           solid(poly([(12, 4.5), (16.5, 2.5), (16.5, 6.5)], closed=True, r=S.r * 0.6)),
           solid(circle(12, 4.5, 1.3))]
    return [
        *bow,
        shell(ellipse(12, 14, 7, 7.5)),
        mark(circle(12, 11.8, 2.1)),
        mark("M8.5 18.3Q8.5 14.8 12 14.8Q15.5 14.8 15.5 18.3Z"),
    ]


@icon("shadow-box", CAT, "Deep square frame with a pinned butterfly displayed inside.",
      tags=["display frame", "memory box", "frame box", "butterfly frame", "keepsake", "wall art", "collection display"])
def _(S):
    wl = "M11.3 12.4Q7.5 6.5 5.8 9Q5.5 12.4 11.3 12.6Z"
    ll = "M11.3 13.5Q7.3 13.4 8 16.3Q9 18 11.3 15.6Z"
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        mark(wl), mark(flip(wl)), mark(ll), mark(flip(ll)),
        mark(rect(11.3, 8.8, 1.4, 8.4, 0.7)),
    ]


# ============================================================================ displays, lighting, doors

@icon("jewelry-stand", CAT, "Tree-shaped stand with a crossbar holding necklaces and a small dish at the base.",
      tags=["jewellery stand", "necklace holder", "jewelry tree", "jewelry organizer", "accessory display", "vanity", "necklace stand"])
def _(S):
    return [
        line(seg(4.5, 4, 19.5, 4)),
        line(seg(12, 4, 12, 18)),
        line("M5.5 4C5.5 11 9 11 9 4"),
        line("M15 4C15 11 18.5 11 18.5 4"),
        shell("M5 21H19Q19 18.3 12 18.3Q5 18.3 5 21Z"),
    ]


@icon("led-panel", CAT, "Slim square ceiling panel light with a flat glowing face and rays below.",
      tags=["panel light", "ceiling light", "flat light", "office lighting", "led light", "troffer", "lighting"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 4, rr(S, 1.5))),
        *[line(seg(*polar(12, 4.5, r1, a), *polar(12, 4.5, r2, a))) for a, r1, r2 in
          ((90, 4, 15), (62, 4, 13), (118, 4, 13), (34, 5, 10), (146, 5, 10))],
    ]


@icon("photo-string", CAT, "String hung between two nails with small photos clipped to it by pegs.",
      tags=["photo garland", "photo line", "picture clips", "polaroid wall", "photo display", "clothesline photos", "wall decor"])
def _(S):
    return [
        line("M3 4.5Q12 9.5 21 4.5"),
        dot(3, 4.5, 1.2), dot(21, 4.5, 1.2),
        line(seg(7, 6.7, 7, 10.5)), line(seg(17, 6.7, 17, 10.5)),
        shell(rect(4, 10.5, 6, 8.5, rr(S, 1.5))),
        shell(rect(14, 10.5, 6, 8.5, rr(S, 1.5))),
    ]


@icon("floating-stairs", CAT, "Staircase of separate thick treads jutting out from a wall with no risers.",
      tags=["cantilever stairs", "open stairs", "modern staircase", "stair treads", "steps", "minimalist", "wall mounted stairs"])
def _(S):
    return [
        shell(rect(2.5, 17.5, 9, 3, rr(S, 1.2))),
        shell(rect(7.5, 11.5, 9, 3, rr(S, 1.2))),
        shell(rect(12.5, 5.5, 9, 3, rr(S, 1.2))),
    ]


@icon("wine-cellar", CAT, "Vaulted cellar with a wine barrel and a stack of bottle ends.",
      tags=["wine room", "wine storage", "cellar", "wine vault", "bottle rack", "wine barrel", "vineyard"])
def _(S):
    bottles = [dot(x, y, 1.2) for x, y in ((12.8, 18.9), (15.7, 18.9), (18.6, 18.9), (14.25, 16.1), (17.15, 16.1), (15.7, 13.3))]
    return [
        line("M2.8 21.5V12A9.2 9.2 0 0 1 21.2 12V21.5"),
        shell(rect(5.4, 13.5, 4.8, 7, rr(S, 2.4))),
        detail(seg(5.4, 17, 10.2, 17)),
        *bottles,
    ]


@icon("baby-play-gym", CAT, "Soft play mat with an arch over it from which small toys dangle.",
      tags=["activity gym", "play mat", "baby gym", "infant toys", "tummy time", "nursery", "hanging toys"])
def _(S):
    return [
        line("M2.8 18A9.2 14 0 0 1 21.2 18"),
        line(seg(7, 7.2, 7, 10.5)), solid(circle(7, 12.3, 1.9)),
        line(seg(12, 4, 12, 8)),
        solid(poly([(12, 8), (14.3, 11), (12, 14), (9.7, 11)], closed=True, r=S.r * 0.4)),
        line(seg(17, 7.2, 17, 10.5)), solid(circle(17, 12.3, 1.9)),
        shell(rect(2.5, 18.5, 19, 3, rr(S, 1.5))),
    ]


@icon("ball-pit", CAT, "Square padded pit filled with a heap of small balls.",
      tags=["ball pool", "play pit", "soft play", "kids play area", "playroom", "balls", "playground"])
def _(S):
    balls = [solid(circle(x, y, 2.3)) for x, y in ((7, 10.3), (12, 10.3), (17, 10.3), (9.5, 6.1), (14.5, 6.1))]
    return [
        *balls,
        shell(rect(2.5, 13, 19, 8.5, rr(S, 3))),
        dot(7.5, 17.3, 1.3), dot(12, 17.3, 1.3), dot(16.5, 17.3, 1.3),
    ]


@icon("stone-lantern", CAT, "Garden stone lantern with a wide peaked cap, a light box and a pedestal.",
      tags=["japanese lantern", "toro", "garden lantern", "zen garden", "stone light", "temple garden", "landscaping"])
def _(S):
    return [
        shell("M2.5 10.5Q10 9.5 12 3.5Q14 9.5 21.5 10.5Z"),
        shell(rect(8, 12.5, 8, 4, rr(S, 1.5))),
        line(seg(12, 16.5, 12, 19)),
        shell(rect(6, 19, 12, 3, rr(S, 1.5))),
    ]


@icon("table-runner", CAT, "Table with a narrow cloth strip laid along its top and hanging down past both ends.",
      tags=["table cloth", "dining table decor", "table linen", "runner", "table setting", "dinner party", "tablecloth"])
def _(S):
    return [
        line(poly([(3, 17), (3, 8), (21, 8), (21, 17)], r=S.r)),
        shell(rect(5.5, 10, 13, 2.5, rr(S, 1))),
        line(seg(8, 12.5, 8, 21.5)), line(seg(16, 12.5, 16, 21.5)),
    ]


@icon("swing-arm-lamp", CAT, "Wall lamp on a folding hinged arm with a cone shade.",
      tags=["wall lamp", "articulated lamp", "bedside light", "reading light", "folding arm lamp", "wall sconce", "adjustable lamp"])
def _(S):
    return [
        line(seg(3, 4.5, 3, 12.5)),
        line(poly([(3, 8.5), (9, 4), (14, 9.5)], r=S.r)),
        shell(poly([(11, 9), (16.5, 9), (21, 16.5), (6.5, 16.5)], closed=True, r=S.r * 0.5)),
        line(seg(9.5, 19.3, 8.3, 21.5)), line(seg(13.75, 19.3, 13.75, 21.5)), line(seg(18, 19.3, 19.2, 21.5)),
    ]


@icon("fanlight", CAT, "Front door with a semicircular window above it divided by radiating bars.",
      tags=["transom window", "arched window", "door window", "fan window", "georgian door", "entrance", "front door"])
def _(S):
    rays = [detail(seg(*polar(12, 10.5, 2.2, a), *polar(12, 10.5, 6.6, a))) for a in (-140, -90, -40)]
    return [
        line("M4.5 10.5A7.5 7.5 0 0 1 19.5 10.5"),
        *rays,
        shell(rect(4.5, 10.5, 15, 11, rr(S, 1.5))),
        dot(16.3, 16.5, 1.2),
    ]


@icon("double-doors", CAT, "Pair of tall doors meeting in the middle, each with its own handle.",
      tags=["french doors", "double door", "entrance doors", "wide doorway", "patio doors", "interior doors", "hallway"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 3))),
        detail(seg(12, 2.5, 12, 21.5)),
        dot(9.5, 13, 1.2), dot(14.5, 13, 1.2),
    ]


@icon("pocket-door", CAT, "Door slab in a wall opening with an arrow showing it sliding into the wall.",
      tags=["sliding door", "door into wall", "space saving door", "recessed door", "wall door", "interior door", "hidden door track"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 18.5, rr(S, 3))),
        detail(rect(5, 7, 8, 14.5, rr(S, 1))),
        dot(7.5, 15.5, 1.0),
        detail(seg(10.5, 10.5, 18, 10.5)),
        detail(poly([(15.7, 8.2), (18, 10.5), (15.7, 12.8)], r=S.r * 0.4)),
    ]


@icon("cellar-door", CAT, "Pair of slanted bulkhead doors set against a house foundation at ground level.",
      tags=["bulkhead door", "storm cellar", "basement entrance", "outside cellar door", "root cellar", "slanted doors", "underground"])
def _(S):
    return [
        line(seg(2, 5, 22, 5)),
        shell(poly([(2.5, 21.5), (6, 9), (18, 9), (21.5, 21.5)], closed=True, r=S.r * 0.4)),
        detail(seg(12, 9, 12, 21.5)),
        detail(seg(4.3, 15.2, 19.7, 15.2)),
        dot(10, 12, 1.0), dot(14, 12, 1.0),
    ]


@icon("secret-door", CAT, "Bookcase swung partly open like a door, revealing a dark passage behind it.",
      tags=["hidden door", "bookcase door", "secret passage", "hidden room", "panic room", "speakeasy", "mystery"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 3))),
        mark(rect(12.5, 7, 6, 12)),
        shell(poly([(3, 2.5), (11, 5.5), (11, 19), (3, 21.5)], closed=True, r=S.r * 0.3)),
        detail(seg(3, 9.5, 11, 10.8)), detail(seg(3, 15.3, 11, 14.3)),
    ]


# ============================================================================ stairs, rooms and home features

def flame(cx, top, bottom, w) -> str:
    mid = top + (bottom - top) * 0.55
    return (f"M{fmt(cx)} {fmt(top)}Q{fmt(cx + w)} {fmt(mid)} {fmt(cx + w * 0.8)} {fmt(bottom)}"
            f"H{fmt(cx - w * 0.8)}Q{fmt(cx - w)} {fmt(mid)} {fmt(cx)} {fmt(top)}Z")


@icon("grand-staircase", CAT, "Wide staircase rising to the right with a railing on balusters and a curled start.",
      tags=["staircase", "stairway", "sweeping stairs", "mansion stairs", "stairs with railing", "hotel lobby", "entrance hall"])
def _(S):
    return [
        shell(poly([(6, 21.5), (6, 17.5), (10, 17.5), (10, 13.5), (14, 13.5), (14, 9.5), (18, 9.5), (18, 5.5), (21.5, 5.5), (21.5, 21.5)],
                   closed=True, r=S.r * 0.4)),
        line("M7 13L19 2.8"),
        line("M7 13Q2.8 13.5 2.8 18"),
    ]


@icon("electric-fireplace", CAT, "Wide slim wall-mounted fireplace unit with a row of flames behind glass.",
      tags=["wall fireplace", "led fireplace", "fake fire", "heater", "living room", "flame effect", "linear fireplace"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 19, 13, rr(S, 3))),
        mark(flame(7.5, 9, 15.5, 2.3)), mark(flame(12, 8, 15.5, 2.5)), mark(flame(16.5, 9, 15.5, 2.3)),
        line(seg(6, 18.5, 6, 21)), line(seg(18, 18.5, 18, 21)),
    ]


@icon("laundry-room", CAT, "Laundry room with a front-loading washer, a shelf with detergent and a drying rack.",
      tags=["utility room", "washing machine", "laundry", "drying rack", "washer", "home room", "chores"])
def _(S):
    return [
        line(seg(2.5, 7, 21.5, 7)),
        sq(4, 3, 4, 3, 0.6),
        shell(rect(2.5, 10.5, 11, 11, rr(S, 2.5))),
        detail(circle(8, 16.5, 3)),
        line(poly([(16.5, 21.5), (16.5, 11), (21.5, 11), (21.5, 21.5)], r=S.r)),
        line(seg(16.5, 15, 21.5, 15)), line(seg(16.5, 18.5, 21.5, 18.5)),
    ]


@icon("globe-bar", CAT, "Globe on a stand opened at the equator, lid tilted up, with bottles standing inside.",
      tags=["globe bar", "drinks globe", "vintage bar", "liquor cabinet", "mini bar", "home bar", "bar globe"])
def _(S):
    return [
        shell("M6.5 12.5A5.5 5.5 0 0 1 14.9 5.4Z"),
        shell("M6.5 12.5H17.5A5.5 5.5 0 0 1 6.5 12.5Z"),
        mark(rect(11.4, 9.4, 1.6, 3.6, 0.5)), mark(rect(14.6, 10.2, 1.6, 2.8, 0.5)),
        line(seg(12, 18, 12, 20.6)), line(seg(8, 21.2, 16, 21.2)),
    ]


@icon("rope-shelf", CAT, "Wooden plank hanging from two ropes looped over wall hooks, holding a small plant.",
      tags=["hanging shelf", "rope hanging shelf", "boho decor", "plant shelf", "macrame shelf", "wall decor", "suspended shelf"])
def _(S):
    return [
        line(seg(6, 3, 6, 19.5)), line(seg(18, 3, 18, 19.5)),
        shell(rect(3, 14, 18, 2.5, rr(S, 1))),
        shell(poly([(9.5, 14), (14.5, 14), (13.6, 10.6), (10.4, 10.6)], closed=True, r=S.r * 0.3)),
        line("M12 10.6C12 8 10.5 6.5 8.8 6.3"), line("M12 10.6C12 8 13.5 6.5 15.2 6.3"),
    ]


@icon("elevator", CAT, "Pair of closed sliding elevator doors in a frame with up and down call buttons beside them.",
      tags=["lift", "lift doors", "elevator doors", "building lift", "call buttons", "hotel", "floor access"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 12.5, 19, rr(S, 2.5))),
        detail(seg(8.75, 2.5, 8.75, 21.5)),
        mark("M20 6L21.9 9H18.1Z"), mark("M18.1 15H21.9L20 18Z"),
    ]


@icon("escalator", CAT, "Side view of a moving staircase rising diagonally with a sloped handrail.",
      tags=["moving staircase", "mall escalator", "airport escalator", "moving stairs", "shopping centre", "station", "stairs"])
def _(S):
    return [
        line(poly([(2.5, 21), (6.5, 21), (6.5, 17), (10.5, 17), (10.5, 13), (14.5, 13), (14.5, 9), (18.5, 9)], r=S.r * 0.5)),
        line(seg(2.5, 12.5, 11.5, 3.5)),
        line(seg(9.5, 21, 21.5, 9)),
    ]


@icon("balcony", CAT, "Building wall with a door opening onto a small railed balcony platform.",
      tags=["terrace", "juliet balcony", "balustrade", "apartment balcony", "veranda", "railing", "window door"])
def _(S):
    return [
        shell(rect(7.5, 2.5, 9, 9, rr(S, 2))),
        line(seg(2.5, 11.5, 21.5, 11.5)),
        line(seg(6, 11.5, 6, 15)), line(seg(10, 11.5, 10, 15)), line(seg(14, 11.5, 14, 15)), line(seg(18, 11.5, 18, 15)),
        shell(rect(2.5, 15, 19, 2.5, rr(S, 1))),
        line(seg(6, 17.5, 6, 21.5)), line(seg(18, 17.5, 18, 21.5)),
    ]


@icon("front-porch", CAT, "Covered house entrance with a small roof on two posts, a door and steps.",
      tags=["porch", "entryway", "veranda", "entrance", "home exterior", "doorstep", "curb appeal"])
def _(S):
    return [
        shell(poly([(2.5, 9), (12, 3.8), (21.5, 9)], closed=True, r=S.r * 0.5)),
        line(seg(5, 9, 5, 17.5)), line(seg(19, 9, 19, 17.5)),
        shell(rect(9.5, 10.5, 5, 7, rr(S, 1.5))),
        line(seg(2.5, 17.5, 21.5, 17.5)),
        shell(rect(6.5, 19, 11, 2, rr(S, 1))),
    ]


@icon("kitchen-hutch", CAT, "Tall cupboard with closed doors below and open shelves above showing standing plates.",
      tags=["dresser", "china hutch", "welsh dresser", "plate rack", "kitchen cabinet", "sideboard hutch", "dining room"])
def _(S):
    return [
        line(seg(2.5, 3, 21.5, 3)),
        shell(rect(4.5, 3, 15, 9, rr(S, 2))),
        mark(ellipse(8.5, 7.6, 1.4, 2.6)), mark(ellipse(12, 7.6, 1.4, 2.6)), mark(ellipse(15.5, 7.6, 1.4, 2.6)),
        shell(rect(3.5, 13, 17, 8.5, rr(S, 3))),
        detail(seg(12, 13, 12, 21.5)),
        dot(10, 17.3, 1.1), dot(14, 17.3, 1.1),
    ]


@icon("c-table", CAT, "Side view of a C-shaped side table whose base slides under a sofa seat.",
      tags=["sofa side table", "snack table", "laptop table", "bedside table", "couch table", "end table", "slide under table"])
def _(S):
    return [
        shell(rect(2.5, 10.5, 10.5, 5, rr(S, 2))),
        line(seg(4.5, 15.5, 4.5, 21.5)),
        shell(rect(9, 4.5, 12, 2.5, rr(S, 1))),
        shell(rect(9, 18, 12, 2.5, rr(S, 1))),
        line(seg(19.5, 7, 19.5, 18)),
    ]


@icon("round-bed", CAT, "Circular bed seen at an angle with a curved headboard and two pillows.",
      tags=["circle bed", "circular bed", "round mattress", "bedroom", "romantic", "hotel suite", "luxury bed"])
def _(S):
    return [
        line("M4.8 11.8V8.5Q4.8 4 12 4Q19.2 4 19.2 8.5V11.8"),
        shell("M3.5 13A8.5 3.8 0 0 1 20.5 13V17.5A8.5 3.8 0 0 1 3.5 17.5Z"),
        detail("M3.5 13A8.5 3.8 0 0 0 20.5 13"),
        mark(poly([(7.4, 12.7), (8, 10.6), (11.4, 10.6), (11.4, 12.7)], closed=True, r=S.r * 0.6)),
        mark(poly([(12.6, 12.7), (12.6, 10.6), (16, 10.6), (16.6, 12.7)], closed=True, r=S.r * 0.6)),
    ]


@icon("suncatcher", CAT, "Faceted crystal hanging on a string in a window, casting small sparkles.",
      tags=["crystal prism", "window crystal", "rainbow maker", "hanging crystal", "sun catcher", "prism", "window decor"])
def _(S):
    def spark(cx, cy, r):
        k = r * 0.3
        return poly([(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k), (cx, cy + r), (cx - k, cy + k), (cx - r, cy), (cx - k, cy - k)], closed=True)
    return [
        line(seg(12, 2.5, 12, 6)),
        shell(poly([(12, 6), (17, 10.5), (12, 20), (7, 10.5)], closed=True, r=S.r * 0.5)),
        detail(seg(7, 10.5, 17, 10.5)), detail(seg(12, 10.5, 12, 20)),
        solid(spark(20, 17, 2.2)), solid(spark(4, 6.5, 2)),
    ]


@icon("under-stairs-storage", CAT, "Staircase in side view with a small door and drawers built into the space beneath it.",
      tags=["stair storage", "understairs cupboard", "stair drawers", "closet under stairs", "hallway storage", "built in storage", "space saving"])
def _(S):
    return [
        shell(poly([(2.5, 21.5), (2.5, 18), (7, 18), (7, 14), (11.5, 14), (11.5, 10), (16, 10), (16, 6), (21.5, 6), (21.5, 21.5)],
                   closed=True, r=S.r * 0.4)),
        detail(rect(14, 12.5, 5, 7, rr(S, 1))),
        detail(seg(7.5, 18, 11.5, 18)),
    ]


# ============================================================================ seating, lighting, rugs and garden rooms

@icon("slipper-chair", CAT, "Front view of an armless upholstered chair with a tall rounded back and short legs.",
      tags=["armless chair", "accent chair", "bedroom chair", "upholstered chair", "boudoir chair", "vanity chair", "low chair"])
def _(S):
    return [
        shell("M6.5 13V8.5A5.5 5.5 0 0 1 17.5 8.5V13Z"),
        shell(rect(4, 13, 16, 4.5, rr(S, 2))),
        dot(12, 8.5, 1.2),
        line(seg(6.5, 17.5, 5.5, 21.5)), line(seg(17.5, 17.5, 18.5, 21.5)),
    ]


@icon("hall-tree", CAT, "Entry unit with a bench seat, a tall back panel with coat pegs and a small arched mirror on top.",
      tags=["entryway bench", "coat rack", "hat stand", "mudroom", "hall stand", "coat hooks", "entrance furniture"])
def _(S):
    return [
        shell("M9 7.8V6.3A3 3 0 0 1 15 6.3V7.8Z"),
        shell(rect(5, 7.8, 14, 8.2, rr(S, 2))),
        detail(seg(8.5, 10.2, 8.5, 12)), dot(8.5, 13.1, 1.1),
        detail(seg(12, 10.2, 12, 12)), dot(12, 13.1, 1.1),
        detail(seg(15.5, 10.2, 15.5, 12)), dot(15.5, 13.1, 1.1),
        shell(rect(3.5, 16.5, 17, 2.5, rr(S, 1))),
        line(seg(5.5, 19, 5.5, 21.5)), line(seg(18.5, 19, 18.5, 21.5)),
    ]


@icon("wagon-wheel-chandelier", CAT, "Wooden wagon wheel hung flat from a chain with candle bulbs standing around its rim.",
      tags=["wheel chandelier", "rustic chandelier", "farmhouse lighting", "ranch decor", "candle chandelier", "western decor", "rim lights"])
def _(S):
    candles = []
    for a in (-152, -122, -58, -28):
        x, y = polar(12, 16.5, 9, a)[0], 16.5 + 4.4 * math.sin(math.radians(a))
        candles += [line(seg(x, y, x, y - 3.3)), dot(x, y - 4.6, 1.15)]
    return [
        line(seg(12, 2.5, 12, 14)),
        shell(ellipse(12, 16.5, 9, 4.4)),
        detail(seg(3, 16.5, 21, 16.5)), detail(seg(12, 12.3, 12, 20.7)),
        *candles,
    ]


@icon("rattan-pendant", CAT, "Woven dome pendant light with a crisscross basket texture hanging from a cord.",
      tags=["wicker pendant", "woven lamp", "boho lighting", "basket light", "rattan lamp shade", "ceiling light", "natural decor"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 6.5)),
        shell("M3 19C3 11.5 7 7 12 7C17 7 21 11.5 21 19Z"),
        detail(seg(8, 19, 15.5, 9.5)), detail(seg(16, 19, 8.5, 9.5)),
        detail(seg(3, 14.5, 21, 14.5)),
    ]


@icon("cowhide-rug", CAT, "Irregular hide-shaped rug with large dark patches like cow markings.",
      tags=["cow rug", "animal hide rug", "cowskin", "western decor", "ranch decor", "spotted rug", "leather rug"])
def _(S):
    hide = poly([(7, 3.5), (17, 3.5), (17.5, 8), (21.5, 10), (19.5, 14), (21, 18.5), (16.5, 19.5), (13.5, 21.5), (10.5, 21.5),
                 (7.5, 19.5), (3, 18.5), (4.5, 14), (2.5, 10), (6.5, 8)], closed=True, r=S.r * 1.5)
    return [
        shell(hide),
        mark("M8.5 7.5Q11.5 6 12.5 8.8Q11.5 11.5 8.5 11Z"),
        mark("M14.5 12.5Q17.5 11.8 17.6 15Q15.8 17 13.8 15.6Z"),
        mark("M6 14Q8.6 13.3 9.2 16Q7.4 17.8 5.6 16.2Z"),
        mark(circle(15, 7.3, 1.2)),
    ]


@icon("gazebo", CAT, "Open garden pavilion with a peaked roof and finial on slim posts above a raised floor.",
      tags=["garden pavilion", "summerhouse", "bandstand", "outdoor shelter", "garden structure", "park pavilion", "belvedere"])
def _(S):
    return [
        shell(poly([(3.8, 10), (8.5, 5), (15.5, 5), (20.2, 10)], closed=True, r=S.r * 0.5)),
        line(seg(12, 5, 12, 2.5)),
        line(seg(6, 10, 6, 19)), line(seg(10.5, 10, 10.5, 19)), line(seg(13.5, 10, 13.5, 19)), line(seg(18, 10, 18, 19)),
        shell(rect(2.5, 19, 19, 2.5, rr(S, 1))),
    ]


@icon("pergola", CAT, "Garden frame of four posts supporting a flat grid of crossbeams overhead.",
      tags=["garden arbor", "trellis", "pergola roof", "patio cover", "outdoor structure", "vine frame", "backyard"])
def _(S):
    return [
        shell(poly([(2.5, 10), (7.5, 4), (21.5, 4), (16.5, 10)], closed=True, r=S.r * 0.4)),
        detail(seg(14.4, 4, 9.4, 10)),
        detail(seg(5, 7, 19, 7)),
        line(seg(2.5, 10, 2.5, 21.5)), line(seg(16.5, 10, 16.5, 21.5)),
        line(seg(7.5, 4, 7.5, 14)), line(seg(21.5, 4, 21.5, 14)),
    ]


@icon("majlis-seating", CAT, "Low floor sofa running along a wall with thick seat cushions and back pillows.",
      tags=["arabic seating", "floor sofa", "arabian majlis", "low sofa", "lounge seating", "diwan", "middle eastern"])
def _(S):
    return [
        shell(rect(3.5, 6.5, 17, 5.5, rr(S, 2.5))),
        shell(rect(2.5, 12.5, 19, 6, rr(S, 2.5))),
        detail(seg(9, 6.5, 9, 18.5)), detail(seg(15, 6.5, 15, 18.5)),
        line(seg(2.5, 21, 21.5, 21)),
    ]


@icon("mashrabiya", CAT, "Window screen filled with an intricate wooden lattice of diamond shapes.",
      tags=["lattice screen", "arabic screen", "wooden lattice", "jali", "privacy screen", "islamic architecture", "window screen"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        detail(seg(4, 12, 12.5, 3.5)), detail(seg(4, 20, 20, 4)), detail(seg(11.5, 20.5, 20, 12)),
        detail(seg(4, 12, 12.5, 20.5)), detail(seg(4, 4, 20, 20)), detail(seg(11.5, 3.5, 20, 12)),
    ]


@icon("moon-gate", CAT, "Circular doorway opening in a garden wall with a path leading through it.",
      tags=["circular gate", "chinese garden gate", "round doorway", "garden wall", "zen garden", "round door", "landscape"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        detail(circle(12, 11.5, 6)),
        mark("M8.4 16.2L11.2 11.6H12.8L15.6 16.2Z"),
    ]


@icon("mood-board", CAT, "Board pinned with a fabric swatch, a photo, a paint chip strip and a small sketch.",
      tags=["inspiration board", "vision board", "design board", "sample board", "interior design", "swatches", "collage"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        mark(rect(5.5, 5.5, 7, 5, rr(S, 1))),
        mark(circle(16.5, 8, 2.6)),
        mark(rect(5.5, 13.5, 3, 5.5, rr(S, 0.8))),
        mark("M11.5 19L14.5 13.5L17.5 19Z"),
    ]


@icon("magnifier-lamp", CAT, "Desk lamp on an articulated arm ending in a round magnifying lens ring with a light.",
      tags=["magnifying lamp", "craft lamp", "hobby light", "task light", "beauty lamp", "workshop lamp", "magnifying glass lamp"])
def _(S):
    return [
        shell(rect(2.5, 19.5, 9, 2, rr(S, 1))),
        line(poly([(6.5, 19.5), (6.5, 7), (12, 3.5), (16.5, 3.5), (16.5, 7)], r=S.r)),
        shell(circle(16.5, 12.5, 5)),
        dot(6.5, 7, 1.1),
    ]


@icon("picture-ledge", CAT, "Narrow wall shelf with a front lip holding framed pictures leaning against the wall.",
      tags=["photo ledge", "gallery shelf", "picture shelf", "frame shelf", "wall shelf", "art display", "gallery wall"])
def _(S):
    return [
        shell(rect(4.5, 8, 6.5, 9.5, rr(S, 1.5))),
        mark(rect(6.6, 10.2, 2.3, 5.1, 0.4)),
        shell(rect(12.5, 4, 7, 13.5, rr(S, 1.5))),
        mark(rect(14.8, 6.3, 2.4, 8.9, 0.4)),
        shell(rect(2.5, 17.5, 19, 3, rr(S, 1.2))),
    ]


@icon("extending-table", CAT, "Dining table pulled apart in the middle with an extra leaf being dropped into the gap.",
      tags=["expandable table", "table leaf", "dining table", "drop leaf extension", "extendable table", "butterfly leaf", "hosting"])
def _(S):
    return [
        shell(rect(9.5, 4, 5, 2.5, rr(S, 1))),
        line(seg(12, 8.5, 12, 13)),
        line(poly([(9.7, 11), (12, 13.3), (14.3, 11)], r=S.r * 0.3)),
        shell(rect(2.5, 15, 7, 2.5, rr(S, 1))),
        shell(rect(14.5, 15, 7, 2.5, rr(S, 1))),
        line(seg(4, 17.5, 4, 21.5)), line(seg(8, 17.5, 8, 21.5)),
        line(seg(16, 17.5, 16, 21.5)), line(seg(20, 17.5, 20, 21.5)),
    ]


@icon("picnic-blanket", CAT, "Checkered blanket spread flat in perspective.",
      tags=["picnic rug", "picnic mat", "gingham blanket", "outdoor blanket", "park", "checkered cloth", "summer picnic"])
def _(S):
    return [
        shell(poly([(2.5, 19.5), (7, 6.5), (21.5, 6.5), (17, 19.5)], closed=True, r=S.r * 0.4)),
        detail(seg(11.8, 6.5, 7.9, 19.5)), detail(seg(16.6, 6.5, 12.6, 19.5)),
        detail(seg(4.7, 13, 19.3, 13)),
    ]


@icon("pool-table", CAT, "Billiard table on sturdy legs with a cue stick and a few balls on the felt.",
      tags=["billiard table", "snooker table", "billiards", "game room", "cue sports", "pub games", "rec room"])
def _(S):
    return [
        shell(poly([(2.5, 13.5), (6.5, 4.5), (17.5, 4.5), (21.5, 13.5)], closed=True, r=S.r * 0.5)),
        shell(rect(2.5, 13.5, 19, 3, rr(S, 1))),
        line(seg(5, 10.8, 10, 8.4)),
        dot(13.8, 8.3, 1.1), dot(16.3, 8.3, 1.1), dot(15, 10.4, 1.1),
        line(seg(4.5, 16.5, 4.5, 21.5)), line(seg(19.5, 16.5, 19.5, 21.5)),
    ]


@icon("foosball-table", CAT, "Table football game seen from above with rods crossing the field, each holding small players.",
      tags=["table football", "soccer table", "babyfoot", "game room", "arcade game", "rods", "pub game"])
def _(S):
    rods = []
    for x in (6.5, 12, 17.5):
        rods += [detail(seg(x, 7.5, x, 16.5)), line(seg(x, 3.5, x, 7.5)), line(seg(x, 16.5, x, 20.5)),
                 mark(rect(x - 1.4, 9.3, 2.8, 1.8, 0.4)), mark(rect(x - 1.4, 12.9, 2.8, 1.8, 0.4))]
    return [shell(rect(2.5, 7.5, 19, 9, rr(S, 2))), *rods]


def egg(cx, y0, y1, hw) -> str:
    h = y1 - y0
    yw = y0 + h * 0.66
    return (f"M{fmt(cx)} {fmt(y0)}C{fmt(cx + hw * 0.8)} {fmt(y0)} {fmt(cx + hw)} {fmt(y0 + h * 0.4)} {fmt(cx + hw)} {fmt(yw)}"
            f"C{fmt(cx + hw)} {fmt(y1 - h * 0.02)} {fmt(cx + hw * 0.55)} {fmt(y1)} {fmt(cx)} {fmt(y1)}"
            f"C{fmt(cx - hw * 0.55)} {fmt(y1)} {fmt(cx - hw)} {fmt(y1 - h * 0.02)} {fmt(cx - hw)} {fmt(yw)}"
            f"C{fmt(cx - hw)} {fmt(y0 + h * 0.4)} {fmt(cx - hw * 0.8)} {fmt(y0)} {fmt(cx)} {fmt(y0)}Z")


@icon("nesting-dolls", CAT, "Three rounded painted wooden dolls in a row, decreasing in size, with scarf bands.",
      tags=["matryoshka", "russian dolls", "stacking dolls", "babushka dolls", "wooden dolls", "folk art", "souvenir"])
def _(S):
    return [
        shell(egg(6.4, 3, 21, 3.7)),
        detail(seg(2.7, 10, 10.1, 10) if S.name == "line" else "M2.7 10Q6.4 11.6 10.1 10"),
        shell(egg(14.2, 8, 21, 2.9)),
        detail(seg(11.3, 14, 17.1, 14) if S.name == "line" else "M11.3 14Q14.2 15.4 17.1 14"),
        shell(egg(19.9, 13, 21, 2.0)),
    ]


@icon("kids-bedroom", CAT, "Children's room scene with a bunk bed, a toy block on the floor and a star on the wall.",
      tags=["children's room", "nursery", "bunk bed", "kids room", "playroom", "child bedroom", "toy room"])
def _(S):
    star = poly([polar(19, 6.3, 2.7 if i % 2 == 0 else 1.15, -90 + i * 36) for i in range(10)], closed=True)
    return [
        line(seg(4, 3, 4, 21.5)), line(seg(15, 3, 15, 21.5)),
        shell(rect(4, 7, 11, 2.5, rr(S, 1))),
        shell(rect(4, 14, 11, 2.5, rr(S, 1))),
        solid(star),
        shell(rect(17, 17, 4.5, 4.5, rr(S, 1))),
    ]


@icon("home-library", CAT, "Room wall of full bookshelves with a rolling ladder beside it.",
      tags=["reading room", "study", "book wall", "bookcase room", "personal library", "library ladder", "bookshelves"])
def _(S):
    row = lambda y: [mark(rect(x, y, 1.3, h, 0.3)) for x, h in ((5, 2.6), (7.2, 2.2), (9.4, 2.6), (11.6, 2.3))]
    return [
        shell(rect(2.5, 2.5, 13.5, 19, rr(S, 2.5))),
        detail(seg(2.5, 8.8, 16, 8.8)), detail(seg(2.5, 15.2, 16, 15.2)),
        *row(5.4 - 0.6), *row(11.6 - 0.2), *row(18.0 - 0.9),
        line(seg(18.5, 2.5, 18.5, 21.5)), line(seg(21.5, 2.5, 21.5, 21.5)),
        line(seg(18.5, 7, 21.5, 7)), line(seg(18.5, 12, 21.5, 12)), line(seg(18.5, 17, 21.5, 17)),
    ]
