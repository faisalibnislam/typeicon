"""TypeIcon Core: home & furniture.

Original drawings of generic furniture, fittings and household objects (front or side views).
The category takes the `common` variant badges in the bottom-right box (13–23), so identifying
details (handles, knobs, flames, faces) sit top/left where the object allows.
"""
from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path

CAT = "home"


def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    """Container corner radius for the style, optionally capped for small shapes."""
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def mark(d) -> Part:
    """Small solid shape: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def outline_region(d, miter=4.0):
    """Region of a closed outline filled to its outer stroke edge (for Filled overrides)."""
    return U(P(d), ST(d, 2.0, "butt", "miter", miter))


def stroke_region(d, w=2.5):
    return ST(d, w, "butt", "miter")


def flame(cx, top, bottom, w):
    """Candle flame / teardrop with a pointed top."""
    my = bottom - w / 2
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + w * 0.35)} {fmt(top + (my - top) * 0.45)} {fmt(cx + w / 2)} {fmt(my - (my - top) * 0.25)} "
            f"{fmt(cx + w / 2)} {fmt(my)}A{fmt(w / 2)} {fmt(w / 2)} 0 0 1 {fmt(cx - w / 2)} {fmt(my)}"
            f"C{fmt(cx - w / 2)} {fmt(my - (my - top) * 0.25)} {fmt(cx - w * 0.35)} {fmt(top + (my - top) * 0.45)} {fmt(cx)} {fmt(top)}Z")


# ============================================================================ seating and tables

@icon("sofa", CAT, "Two-seater sofa with arms and back cushions",
      tags=["couch", "settee", "living room", "lounge", "furniture", "seat"], aliases=["couch", "settee"])
def _(S):
    return [
        shell(poly([(3, 9.5), (7, 9.5), (7, 5), (17, 5), (17, 9.5), (21, 9.5), (21, 17), (3, 17)], closed=True, r=S.r)),
        detail(seg(7, 9.5, 7, 17)), detail(seg(17, 9.5, 17, 17)),
        detail(seg(7, 13, 17, 13)), detail(seg(12, 5, 12, 13)),
        line(seg(5, 17, 5, 21)), line(seg(19, 17, 19, 21)),
    ]


def _arc_pts(cx, cy, r, a0, a1, n=8):
    return [polar(cx, cy, r, a0 + (a1 - a0) * i / n) for i in range(n + 1)]


@icon("armchair", CAT, "Upholstered armchair with a rounded back",
      tags=["chair", "easy chair", "lounge chair", "seat", "living room", "furniture"], aliases=["easy-chair"])
def _(S):
    back = _arc_pts(12, 7, 4, 180, 360)
    pts = [(4, 10), (8, 10)] + back + [(16, 10), (20, 10), (20, 17), (4, 17)]
    return [
        shell(poly([pts[0], pts[1], (8, 7)] + back[1:-1] + [(16, 7)] + pts[-4:], closed=True, r=S.r)),
        detail(seg(8, 10, 8, 17)), detail(seg(16, 10, 16, 17)), detail(seg(8, 13.5, 16, 13.5)),
        line(seg(6, 17, 6, 21)), line(seg(18, 17, 18, 21)),
    ]


@icon("chair", CAT, "Dining chair seen from the front",
      tags=["seat", "dining chair", "kitchen chair", "sit", "furniture"])
def _(S):
    return [
        shell(rect(6, 3, 12, 7, rr(S, 2))),
        line(seg(8, 10, 8, 14)), line(seg(16, 10, 16, 14)),
        line(seg(4, 14, 20, 14)),
        line(seg(6, 14, 6, 21)), line(seg(18, 14, 18, 21)),
    ]


@icon("dining-table", CAT, "Table with two chairs drawn up behind it",
      tags=["table", "dining room", "kitchen table", "dinner", "eat", "furniture"], aliases=["kitchen-table"])
def _(S):
    return [
        shell(rect(4, 3, 6, 8, rr(S, 2))), shell(rect(14, 3, 6, 8, rr(S, 2))),
        line(seg(2, 12, 22, 12) if S.name == "line" else seg(3, 12, 21, 12)),
        line(seg(5, 12, 5, 21)), line(seg(19, 12, 19, 21)),
    ]


@icon("desk", CAT, "Work desk with a drawer pedestal",
      tags=["office", "workspace", "writing desk", "study", "table", "furniture"], aliases=["writing-desk"])
def _(S):
    return [
        line(seg(3, 6, 21, 6)),
        shell(poly([(4, 6), (4, 21), (12, 21), (12, 6)], closed=True, r=S.r)),
        detail(seg(4, 13.5, 12, 13.5)),
        detail(seg(6.5, 9.75, 9.5, 9.75)), detail(seg(6.5, 17.25, 9.5, 17.25)),
        line(seg(19, 6, 19, 21)),
    ]


@icon("bed", CAT, "Bed seen from the side with a headboard and pillow",
      tags=["bedroom", "sleep", "hotel", "mattress", "rest", "furniture"])
def _(S):
    return [
        line(seg(3, 4, 3, 21)),
        shell(rect(3, 12, 18, 5, rr(S, 1.5))),
        shell(rect(6, 7.5, 6, 4.5, rr(S, 2))),
        line(seg(21, 17, 21, 21)),
    ]


@icon("crib", CAT, "Baby crib with slatted sides",
      tags=["cot", "baby bed", "nursery", "infant", "baby", "furniture"], aliases=["cot"])
def _(S):
    top = "M4 9Q12 5 20 9V17H4Z"
    return [
        shell(top),
        detail(seg(8, 7.5, 8, 17)), detail(seg(12, 7, 12, 17)), detail(seg(16, 7.5, 16, 17)),
        line(seg(4, 4.5, 4, 21)), line(seg(20, 4.5, 20, 21)),
    ]


# ============================================================================ storage

@icon("wardrobe", CAT, "Tall two-door wardrobe on short legs",
      tags=["closet", "armoire", "cupboard", "clothes", "bedroom", "furniture"], aliases=["armoire", "closet"])
def _(S):
    return [
        shell(rect(5, 3, 14, 15, rr(S, 2))),
        detail(seg(12, 3, 12, 18)),
        detail(seg(9, 8.5, 9, 11.5)), detail(seg(15, 8.5, 15, 11.5)),
        line(seg(7, 18, 7, 21)), line(seg(17, 18, 17, 21)),
    ]


@icon("drawers", CAT, "Chest of drawers with three drawers",
      tags=["chest of drawers", "dresser", "bureau", "storage", "bedroom", "furniture"], aliases=["chest-of-drawers", "dresser"])
def _(S):
    return [
        shell(rect(3, 3, 18, 15, rr(S, 2))),
        detail(seg(3, 8, 21, 8)), detail(seg(3, 13, 21, 13)),
        dot(9, 5.5, 1), dot(15, 5.5, 1), dot(9, 10.5, 1), dot(15, 10.5, 1), dot(9, 15.5, 1), dot(15, 15.5, 1),
        line(seg(5, 18, 5, 21)), line(seg(19, 18, 19, 21)),
    ]


@icon("shelf", CAT, "Wall shelf on brackets holding books and a pot",
      tags=["wall shelf", "shelving", "ledge", "storage", "decor", "furniture"], aliases=["wall-shelf"])
def _(S):
    return [
        shell(rect(5, 5, 4, 7, rr(S, 1))),
        shell(rect(9, 3, 4, 9, rr(S, 1))), detail(seg(9, 5, 9, 12)),
        shell(poly([(15, 7.5), (20, 7.5), (19, 12), (16, 12)], closed=True, r=S.r * 0.5)),
        line(seg(3, 12, 21, 12)),
        line(seg(6, 12, 6, 17)),
        line(seg(18, 12, 18, 17)),
    ]


@icon("bookshelf", CAT, "Bookcase with two shelves of books",
      tags=["bookcase", "books", "library", "shelving", "study", "furniture"], aliases=["bookcase"])
def _(S):
    return [
        shell(rect(4, 3, 16, 18, rr(S, 2))),
        detail(seg(4, 12, 20, 12)),
        detail(seg(8, 6, 8, 12)), detail(seg(11, 7, 11, 12)), detail(seg(13.5, 12, 16.5, 7)),
        detail(seg(8, 15, 8, 21)), detail(seg(11, 16, 11, 21)),
    ]


# ============================================================================ lighting

@icon("floor-lamp", CAT, "Tall floor lamp with a drum shade on a tripod",
      tags=["standard lamp", "light", "lighting", "living room", "shade", "furniture"], aliases=["standard-lamp"])
def _(S):
    return [
        shell(poly([(9, 3), (15, 3), (16.5, 9), (7.5, 9)], closed=True, r=S.r * 0.66)),
        line(seg(12, 9, 12, 21)),
        line(poly([(8, 21), (12, 17), (16, 21)], r=S.r)),
    ]


@icon("desk-lamp", CAT, "Adjustable desk lamp with a jointed arm",
      tags=["reading lamp", "task light", "light", "study", "office", "lamp"], aliases=["reading-lamp"])
def _(S):
    return [
        line(seg(3, 21, 11, 21)),
        line(poly([(7, 21), (5, 12.5), (11.5, 5.5)], r=S.r)),
        dot(5, 12.5, 1.5),
        shell(poly([(12.5, 3.3), (15, 5.8), (21, 10.5), (16.5, 15), (11.8, 9), (9.3, 6.5)], closed=True, r=S.r * 0.66)),
    ]


@icon("ceiling-light", CAT, "Pendant ceiling light with a dome shade",
      tags=["pendant", "light", "lighting", "lamp", "ceiling", "fixture"], aliases=["pendant-light"])
def _(S):
    return [
        line(seg(9, 3, 15, 3)),
        line(seg(12, 3, 12, 7.5)),
        shell("M4 15C4 10.6 7.6 7.5 12 7.5C16.4 7.5 20 10.6 20 15Z"),
        line("M9.5 15A2.5 2.5 0 0 0 14.5 15"),
        line(seg(6, 19, 5, 21) if S.name == "line" else seg(6, 19, 5.2, 20.6)),
        line(seg(18, 19, 19, 21) if S.name == "line" else seg(18, 19, 18.8, 20.6)),
    ]


@icon("chandelier", CAT, "Chandelier hanging from the ceiling with candle arms and a crystal drop",
      tags=["light", "lighting", "ceiling", "candles", "luxury", "fixture"])
def _(S):
    drop = flame(12, 18.5, 22, 2.8) if S.name == "line" else ellipse(12, 20.25, 1.4, 1.75)
    return [
        line(seg(9, 2, 15, 2) if S.name == "line" else seg(9.5, 2, 14.5, 2)),
        line(seg(12, 2, 12, 17)),
        line("M4 10C4 14 7.5 15.5 12 15.5C16.5 15.5 20 14 20 10"),
        line(seg(4, 7.5, 4, 10)), line(seg(20, 7.5, 20, 10)),
        line(seg(8, 12, 8, 15)), line(seg(16, 12, 16, 15)),
        mark(flame(4, 3, 6.5, 2.4)), mark(flame(20, 3, 6.5, 2.4)),
        mark(flame(8, 7.5, 11, 2.4)), mark(flame(16, 7.5, 11, 2.4)),
        mark(drop),
    ]


# ============================================================================ doors, windows, stairs

@icon("door", CAT, "Closed door with a round knob",
      tags=["entrance", "exit", "doorway", "entry", "room", "closed"], aliases=["door-closed"])
def _(S):
    return [
        shell(poly([(6, 21), (6, 3), (18, 3), (18, 21)], closed=True, r=S.r)),
        line(seg(3, 21, 21, 21)),
        dot(9.5, 12.5, 1.4),
    ]


@icon("door-open", CAT, "Door swung open inside its frame",
      tags=["open door", "entrance", "exit", "enter", "welcome", "doorway"], aliases=["open-door"])
def _(S):
    return [
        line(poly([(5, 21), (5, 3), (19, 3), (19, 21)], r=S.r)),
        shell(poly([(5, 3), (12, 5.5), (12, 19.5), (5, 21)], closed=True, r=S.r * 0.66)),
        line(seg(2, 21, 22, 21) if S.name == "line" else seg(3, 21, 21, 21)),
        dot(10, 12.5, 1.25),
    ]


@icon("window-house", CAT, "Four-pane house window with a sill",
      tags=["window", "pane", "glass", "frame", "house", "sill"], aliases=["house-window"])
def _(S):
    return [
        shell(rect(5, 3, 14, 16, rr(S, 2))),
        detail(seg(12, 3, 12, 19)), detail(seg(5, 11, 19, 11)),
        line(seg(3, 19, 21, 19) if S.name == "line" else seg(3, 19.5, 21, 19.5)),
    ]


@icon("stairs", CAT, "Flight of stairs seen from the side",
      tags=["staircase", "steps", "upstairs", "downstairs", "floor", "level"], aliases=["staircase", "steps"])
def _(S):
    pts = [(3, 21), (3, 16.5), (7.5, 16.5), (7.5, 12), (12, 12), (12, 7.5), (16.5, 7.5), (16.5, 3), (21, 3), (21, 21)]
    return [shell(poly(pts, closed=True, r=S.r * 0.66))]


@icon("fireplace", CAT, "Fireplace with a mantel shelf and a fire burning",
      tags=["hearth", "fire", "chimney", "cozy", "warm", "living room"], aliases=["hearth"])
def _(S):
    body = poly([(5, 5), (19, 5), (19, 21), (5, 21)], closed=True, r=S.r * 0.5)
    opening = poly([(8.5, 21), (8.5, 11), (15.5, 11), (15.5, 21)], r=S.r)
    return [
        shell(body),
        line(seg(3, 5, 21, 5)),
        detail(opening),
        mark(flame(12, 13.5, 19, 4)),
    ]


# ============================================================================ bathroom

@icon("bathtub", CAT, "Bathtub on feet with a tap",
      tags=["bath", "tub", "bathroom", "soak", "wash", "hotel"], aliases=["bath", "tub"])
def _(S):
    return [
        shell("M3 11H21V14C21 17 19 18.5 16 18.5H8C5 18.5 3 17 3 14Z" if S.name == "line"
              else "M4.5 11H19.5A1.5 1.5 0 0 1 21 12.5V14C21 17 19 18.5 16 18.5H8C5 18.5 3 17 3 14V12.5A1.5 1.5 0 0 1 4.5 11Z"),
        line(seg(7, 18.5, 6, 21)), line(seg(17, 18.5, 18, 21)),
        line(poly([(5.5, 11), (5.5, 4), (10, 4), (10, 6.5)], r=S.r)),
    ]


@icon("shower", CAT, "Shower head on a wall pipe with falling water",
      tags=["bathroom", "wash", "rain shower", "water", "bathe", "hygiene"])
def _(S):
    return [
        line(poly([(4, 21), (4, 4), (12, 4), (12, 7)], r=S.r)),
        shell("M7 11.5A5 4.5 0 0 1 17 11.5Z"),
        dot(9, 15, 1.1), dot(12, 15, 1.1), dot(15, 15, 1.1),
        dot(10.5, 18.5, 1.1), dot(13.5, 18.5, 1.1),
    ]


@icon("toilet", CAT, "Toilet seen from the side with its cistern",
      tags=["wc", "restroom", "bathroom", "loo", "lavatory", "washroom"], aliases=["wc", "lavatory"])
def _(S):
    bowl = ("M4 11H20V12C20 15.2 17.8 17.3 14.5 17.8L15 21H8.5L9 17.4C6 16.6 4 14.6 4 12Z" if S.name == "line" else
            "M5.5 11H18.5A1.5 1.5 0 0 1 20 12.5C20 15.4 17.8 17.3 14.5 17.8L15 21H8.5L9 17.4C6 16.6 4 14.6 4 12.5A1.5 1.5 0 0 1 5.5 11Z")
    return [shell(rect(4, 3, 6, 8, rr(S, 1.5))), shell(bowl), detail(seg(4, 11, 20, 11))]


@icon("sink", CAT, "Basin set into a counter with a curved tap",
      tags=["basin", "washbasin", "kitchen sink", "tap", "bathroom", "wash"], aliases=["basin", "washbasin"])
def _(S):
    return [
        line("M9.5 11V6.5A2.5 2.5 0 0 1 14.5 6.5V8"),
        line(seg(3, 11, 21, 11)),
        shell("M5 11H19V13C19 16.9 15.9 19 12 19C8.1 19 5 16.9 5 13Z"),
        line(seg(12, 19, 12, 21.5) if S.name == "line" else seg(12, 19, 12, 21)),
    ]


@icon("faucet", CAT, "Wall tap with a turn handle and a falling drop",
      tags=["tap", "spigot", "water", "plumbing", "kitchen", "bathroom"], aliases=["spigot"])
def _(S):
    body = ("M21 9H10C7 9 5 11 5 14V15H9V14C9 13.4 9.4 13 10 13H21Z" if S.name == "line" else
            "M21 9H10C7 9 5 11 5 14A1 1 0 0 0 6 15H8A1 1 0 0 0 9 14C9 13.4 9.4 13 10 13H21Z")
    return [
        shell(body),
        line(seg(15, 9, 15, 5)), line(seg(12, 4.5, 18, 4.5)),
        mark(flame(7, 17.5, 21.5, 3)),
    ]


@icon("mirror", CAT, "Oval standing mirror with a reflection glint",
      tags=["reflection", "vanity", "dressing", "looking glass", "bedroom", "bathroom"], aliases=["looking-glass"])
def _(S):
    return [
        shell(ellipse(12, 10, 6, 7)),
        detail(seg(8.5, 10.5, 11.5, 7.5)),
        line(seg(12, 17, 12, 21)),
        line(seg(8, 21, 16, 21) if S.name == "line" else seg(8.5, 21, 15.5, 21)),
    ]


@icon("towel", CAT, "Folded towel hanging over a rail",
      tags=["bath towel", "bathroom", "towel rail", "dry", "linen", "hotel"], aliases=["bath-towel"])
def _(S):
    return [
        line(seg(2, 5, 22, 5) if S.name == "line" else seg(3, 5, 21, 5)),
        shell(poly([(5, 5), (19, 5), (19, 20), (5, 20)], closed=True, r=S.r)),
        detail(poly([(15, 5), (15, 15), (5, 15)], r=S.r)),
    ]


@icon("washing-machine", CAT, "Front-loading washing machine with water in the drum",
      tags=["washer", "laundry", "wash", "clothes", "appliance", "utility room"], aliases=["washer"])
def _(S):
    return [
        shell(rect(4, 3, 16, 18, rr(S, 3))),
        detail(seg(4, 7.5, 20, 7.5)),
        dot(7.25, 5.25, 1), dot(10.25, 5.25, 1),
        detail(circle(12, 14.5, 4.5)),
        detail("M7.6 15C9 13.8 10.5 13.8 12 15S15 16.2 16.4 15"),
    ]


@icon("dryer", CAT, "Tumble dryer with a slider control and a round door marked with a dot",
      tags=["tumble dryer", "laundry", "dry", "clothes", "appliance", "utility room"], aliases=["tumble-dryer", "clothes-dryer"])
def _(S):
    return [
        shell(rect(4, 3, 16, 18, rr(S, 3))),
        detail(seg(4, 7.5, 20, 7.5)),
        dot(7.25, 5.25, 1), sq(12, 4.75, 5, 1, 0.5),
        detail(circle(12, 14.5, 4.5)),
        dot(12, 14.5, 1.5),
    ]


@icon("fridge", CAT, "Refrigerator with a freezer door on top",
      tags=["refrigerator", "freezer", "kitchen", "cold", "appliance", "food storage"], aliases=["refrigerator"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 3))),
        detail(seg(5, 9.5, 19, 9.5)),
        detail(seg(8.5, 5, 8.5, 7)), detail(seg(8.5, 12.5, 8.5, 16)),
    ]


@icon("dishwasher", CAT, "Dishwasher with a control strip, a handle and water drops",
      tags=["dishes", "kitchen", "clean", "appliance", "wash up", "plates"])
def _(S):
    return [
        shell(rect(4, 3, 16, 18, rr(S, 3))),
        detail(seg(4, 7.5, 20, 7.5)),
        dot(7.25, 5.25, 1), dot(10.25, 5.25, 1),
        detail(seg(8.5, 10.5, 15.5, 10.5)),
        mark(flame(9.5, 13, 18, 3)), mark(flame(14.5, 13, 18, 3)),
    ]


@icon("air-conditioner", CAT, "Wall air-conditioning unit blowing air downwards",
      tags=["ac", "air con", "cooling", "climate", "hvac", "aircon"], aliases=["ac-unit", "aircon"])
def _(S):
    return [
        shell(rect(3, 4, 18, 9, rr(S, 2.5))),
        detail(seg(6, 9.5, 18, 9.5)),
        sq(15, 6.25, 3, 1, 0.5),
        line(seg(8, 16, 7, 20)), line(seg(12, 16, 12, 20)), line(seg(16, 16, 17, 20)),
    ]


@icon("heater", CAT, "Portable heater with a grille, a dial and rising heat",
      tags=["space heater", "heating", "warm", "radiant", "electric heater", "winter"], aliases=["space-heater"])
def _(S):
    return [
        shell(rect(3, 9, 18, 10, rr(S, 2))),
        detail(seg(6, 12.5, 13, 12.5)), detail(seg(6, 15.5, 13, 15.5)),
        detail(circle(17, 14, 1.5)),
        line(seg(6, 19, 6, 21)), line(seg(18, 19, 18, 21)),
        *[line(f"M{x} 6.5C{x - 1.2} 5.6 {x + 1.2} 4.4 {x} 3") for x in (8, 12, 16)],
    ]


@icon("radiator", CAT, "Column radiator with four sections on feet",
      tags=["heating", "central heating", "warm", "radiator heater", "winter", "hvac"])
def _(S):
    r = L(S, 1, 2.25)
    cols = [shell(rect(3 + 4.5 * i, 3, 4.5, 16, r)) for i in range(4)]
    return [
        *cols,
        *[detail(seg(3 + 4.5 * i, 5, 3 + 4.5 * i, 17)) for i in (1, 2, 3)],
        line(seg(5.25, 19, 5.25, 21)), line(seg(18.75, 19, 18.75, 21)),
    ]


@icon("vacuum", CAT, "Canister vacuum cleaner with a hose and floor nozzle",
      tags=["vacuum cleaner", "hoover", "cleaning", "housework", "dust", "floor"], aliases=["vacuum-cleaner", "hoover"])
def _(S):
    body = ("M3 20.5V16C3 13.8 4.8 12 7 12H8C10.2 12 12 13.8 12 16V20.5Z" if S.name == "line" else
            "M4.5 20.5A1.5 1.5 0 0 1 3 19V16C3 13.8 4.8 12 7 12H8C10.2 12 12 13.8 12 16V19A1.5 1.5 0 0 1 10.5 20.5Z")
    return [
        shell(body),
        line("M7.5 12C7.5 7 10 4 14.5 4"),
        line(seg(14.5, 4, 17.5, 18.5)),
        line(seg(14.5, 20, 21, 20) if S.name == "line" else seg(15, 20, 20.5, 20)),
        dot(7.5, 16.5, 1.25),
    ]


@icon("broom", CAT, "Broom with a fanned bristle head",
      tags=["sweep", "cleaning", "housework", "brush", "tidy", "chores"], aliases=["sweep"])
def _(S):
    return [
        line(seg(12, 2, 12, 11)),
        shell(poly([(8.5, 11), (15.5, 11), (19, 21), (5, 21)], closed=True, r=S.r * 0.66)),
        detail(seg(7.8, 14, 16.2, 14)),
        detail(seg(9.5, 17, 9, 21)), detail(seg(14.5, 17, 15, 21)),
    ]


@icon("mop", CAT, "Mop with a long handle and hanging strands",
      tags=["mopping", "cleaning", "floor", "housework", "wash", "chores"])
def _(S):
    return [
        line(seg(12, 2, 12, 10)),
        shell(rect(7.5, 10, 9, 4, rr(S, 1.5))),
        line("M8.5 14Q8 18 6 21"), line("M11 14Q11 18 10 21"), line("M13 14Q13 18 14 21"), line("M15.5 14Q16 18 18 21"),
    ]


@icon("bucket", CAT, "Bucket with a carrying handle",
      tags=["pail", "cleaning", "water", "container", "mop bucket", "garden"], aliases=["pail"])
def _(S):
    return [
        shell(poly([(5, 9), (19, 9), (17.5, 21), (6.5, 21)], closed=True, r=S.r)),
        detail(seg(5.4, 12.5, 18.6, 12.5)),
        line("M5 9C5 3.5 19 3.5 19 9"),
    ]


def _arrow_arc(cx, cy, r, a0, a1):
    head_at = polar(cx, cy, r, a1)
    return arc(cx, cy, r, a0, a1), head_at


@icon("recycle-bin", CAT, "Recycling bin with circular arrows on the front",
      tags=["recycling", "waste", "bin", "eco", "sort", "environment"], aliases=["recycling-bin"])
def _(S):
    cx, cy, r = 12, 13.5, 3.3

    def head(a):
        # small solid arrowhead at angle a, pointing clockwise
        x, y = polar(cx, cy, r, a)
        tx, ty = polar(0, 0, 1, a + 90)
        nx, ny = polar(0, 0, 1, a)
        pts = [(x + tx * 2, y + ty * 2), (x + nx * 2, y + ny * 2), (x - nx * 2, y - ny * 2)]
        return mark(poly(pts, closed=True))
    return [
        line(seg(3, 5.5, 21, 5.5) if S.name == "line" else seg(3.5, 5.5, 20.5, 5.5)),
        line(seg(10, 3, 14, 3)),
        shell(poly([(5, 5.5), (19, 5.5), (17.5, 21), (6.5, 21)], closed=True, r=S.r)),
        detail(arc(cx, cy, r, 200, 320)), detail(arc(cx, cy, r, 20, 140)),
        head(320), head(140),
    ]


def _leaf(cx, top, bottom, w, deg=0.0, pivot=None):
    my = (top + bottom) / 2
    k = w * 0.66
    d = (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + k)} {fmt(top + (my - top) * 0.35)} {fmt(cx + k)} {fmt(bottom - (bottom - my) * 0.35)} {fmt(cx)} {fmt(bottom)}"
         f"C{fmt(cx - k)} {fmt(bottom - (bottom - my) * 0.35)} {fmt(cx - k)} {fmt(top + (my - top) * 0.35)} {fmt(cx)} {fmt(top)}Z")
    if deg:
        px, py = pivot or (cx, bottom)
        d = path_to_d(transform_path(P(d), rotation(deg, px, py)))
    return d


@icon("plant-pot", CAT, "Houseplant with broad leaves in a pot",
      tags=["houseplant", "plant", "pot plant", "indoor plant", "decor", "green"], aliases=["houseplant"])
def _(S):
    return [
        shell(poly([(6.5, 14), (17.5, 14), (16, 21), (8, 21)], closed=True, r=S.r)),
        shell(_leaf(12, 2.5, 11, 5)),
        shell(_leaf(12, 4.5, 11.5, 4.5, -55, (12, 13))),
        shell(_leaf(12, 4.5, 11.5, 4.5, 55, (12, 13))),
        line(seg(12, 11, 12, 14)),
    ]



# ============================================================================ decor, fittings and outdoors

@icon("wall-clock", CAT, "Pendulum wall clock in a tall case",
      tags=["clock", "pendulum", "time", "regulator", "hanging clock", "decor"], aliases=["pendulum-clock"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 2.5))),
        detail(circle(12, 8.75, 4)),
        detail(poly([(12, 6.75), (12, 8.75), (13.75, 8.75)], r=S.r * 0.3)),
        detail(seg(12, 12.75, 12, 16)),
        dot(12, 17.5, 1.6),
    ]


@icon("rug", CAT, "Rug with a diamond pattern and fringed ends",
      tags=["carpet", "mat", "floor", "runner", "textile", "decor"], aliases=["carpet"])
def _(S):
    fr = [line(seg(x, 2.5 if S.name == "line" else 3, x, 5)) for x in (8, 12, 16)]
    fr += [line(seg(x, 19, x, 21.5 if S.name == "line" else 21)) for x in (8, 12, 16)]
    return [
        shell(rect(5, 5, 14, 14, rr(S, 1.5))),
        detail(poly([(12, 8.5), (15.5, 12), (12, 15.5), (8.5, 12)], closed=True, r=S.r * 0.5)),
        *fr,
    ]


@icon("curtains", CAT, "Curtains on a rail, tied back to each side",
      tags=["drapes", "window", "blinds", "interior", "privacy", "decor"], aliases=["drapes"])
def _(S):
    left = "M4 3H10.5C10.5 7 9 10.5 7.5 12.5C9 14.5 9.5 17.5 9.5 21H4Z"
    right = "M20 3H13.5C13.5 7 15 10.5 16.5 12.5C15 14.5 14.5 17.5 14.5 21H20Z"
    if S.name != "line":
        left = "M4 3H10.5C10.5 7 9 10.5 7.5 12.5C9 14.5 9.5 17.5 9.5 19.5A1.5 1.5 0 0 1 8 21H5.5A1.5 1.5 0 0 1 4 19.5Z"
        right = "M20 3H13.5C13.5 7 15 10.5 16.5 12.5C15 14.5 14.5 17.5 14.5 19.5A1.5 1.5 0 0 0 16 21H18.5A1.5 1.5 0 0 0 20 19.5Z"
    return [
        line(seg(2, 3, 22, 3) if S.name == "line" else seg(3, 3, 21, 3)),
        shell(left), shell(right),
    ]


@icon("house-key", CAT, "Key with a house-shaped bow",
      tags=["home key", "key", "property", "real estate", "move in", "keys"], aliases=["home-key"])
def _(S):
    return [
        shell(poly([(12, 2.5), (17, 7), (17, 12), (7, 12), (7, 7)], closed=True, r=S.r)),
        dot(12, 8.25, 1.4),
        line(seg(12, 12, 12, 21)),
        line(seg(8.5, 16, 12, 16)), line(seg(9.5, 19.5, 12, 19.5)),
    ]


@icon("doorbell", CAT, "Doorbell button on a wall plate, ringing",
      tags=["bell", "ring", "button", "visitor", "front door", "chime"], aliases=["door-bell"])
def _(S):
    return [
        shell(rect(8.5, 3, 7, 18, rr(S, 3))),
        detail(circle(12, 14.5, 2)),
        detail(seg(10.5, 7.5, 13.5, 7.5)),
        line(arc(12, 14.5, 7, 150, 210)), line(arc(12, 14.5, 7, 330, 30)),
    ]


def _garage_filled():
    house = poly([(3, 21), (3, 9), (12, 3.5), (21, 9), (21, 21)], closed=True)
    body = D(outline_region(house), P(rect(7, 12, 10, 11)))
    return U(body, P(rect(6, 14.5, 12, 2)), P(rect(6, 18, 12, 2)))


@icon("garage", CAT, "Garage with a roller door",
      tags=["car port", "parking", "roller door", "shed", "house", "storage"], aliases=["carport"], filled=_garage_filled)
def _(S):
    return [
        shell(poly([(3, 21), (3, 9), (12, 3.5), (21, 9), (21, 21)], closed=True, r=S.r)),
        detail(poly([(6, 21), (6, 11), (18, 11), (18, 21)], r=S.r)),
        detail(seg(6, 15.5, 18, 15.5)), detail(seg(6, 19, 18, 19)),
    ]


@icon("fence", CAT, "Picket fence with three pointed boards",
      tags=["picket fence", "yard", "boundary", "garden", "backyard", "property"], aliases=["picket-fence"])
def _(S):
    pk = [shell(poly([(x, 21), (x, 6), (x + 2, 3), (x + 4, 6), (x + 4, 21)], closed=True, r=S.r * 0.66)) for x in (3, 10, 17)]
    return [
        *pk,
        line(seg(7, 10, 10, 10)), line(seg(14, 10, 17, 10)),
        line(seg(7, 16, 10, 16)), line(seg(14, 16, 17, 16)),
    ]


@icon("cabinet", CAT, "Low cabinet with a drawer above two doors",
      tags=["cupboard", "sideboard", "kitchen cabinet", "storage", "credenza", "furniture"], aliases=["cupboard", "sideboard"])
def _(S):
    return [
        shell(rect(3, 4, 18, 14, rr(S, 2))),
        detail(seg(3, 9.5, 21, 9.5)), detail(seg(12, 9.5, 12, 18)),
        detail(seg(10.5, 6.75, 13.5, 6.75)),
        dot(9, 13.5, 1), dot(15, 13.5, 1),
        line(seg(5, 18, 5, 21)), line(seg(19, 18, 19, 21)),
    ]


@icon("nightstand", CAT, "Bedside table with a drawer and a small lamp",
      tags=["bedside table", "night table", "bedroom", "side table", "lamp", "furniture"], aliases=["bedside-table"])
def _(S):
    return [
        shell(poly([(9.5, 3), (13.5, 3), (15, 6.5), (8, 6.5)], closed=True, r=S.r * 0.5)),
        line(seg(11.5, 6.5, 11.5, 10.5)),
        shell(rect(4, 10.5, 16, 8.5, rr(S, 2))),
        detail(seg(4, 15, 20, 15)),
        dot(12, 12.75, 1),
        line(seg(6, 19, 6, 21)), line(seg(18, 19, 18, 21)),
    ]


@icon("bench", CAT, "Park bench with a slatted back",
      tags=["park bench", "seat", "outdoor", "garden", "sit", "furniture"], aliases=["park-bench"])
def _(S):
    return [
        shell(rect(3, 4, 18, 6, rr(S, 1.5))),
        detail(seg(3, 7, 21, 7)),
        line(seg(6, 10, 6, 13.5)), line(seg(18, 10, 18, 13.5)),
        line(seg(2, 13.5, 22, 13.5) if S.name == "line" else seg(3, 13.5, 21, 13.5)),
        line(seg(4.5, 13.5, 4.5, 21)), line(seg(19.5, 13.5, 19.5, 21)),
    ]


@icon("stool", CAT, "Bar stool with splayed legs and a footrest",
      tags=["bar stool", "seat", "kitchen", "counter", "sit", "furniture"], aliases=["bar-stool"])
def _(S):
    return [
        shell(rect(6, 3, 12, 4, rr(S, 2))),
        line(seg(8, 7, 6, 21)), line(seg(16, 7, 18, 21)),
        line(seg(6.86, 15, 17.14, 15)),
    ]


@icon("hammock", CAT, "Hammock slung between two posts",
      tags=["relax", "garden", "summer", "holiday", "rest", "outdoor"])
def _(S):
    net = "M3 8C7 18.5 17 18.5 21 8C17 12 7 12 3 8Z"
    return [
        line(seg(3, 3, 3, 21)), line(seg(21, 3, 21, 21)),
        shell(net),
    ]


@icon("bunk-bed", CAT, "Bunk bed with two stacked mattresses and pillows",
      tags=["bunk", "kids room", "dorm", "hostel", "bedroom", "sleep"], aliases=["bunk"])
def _(S):
    return [
        line(seg(3, 3, 3, 21)), line(seg(21, 3, 21, 21)),
        shell(rect(3, 7, 18, 4, rr(S, 1.5))), sq(6, 3.5, 4.5, 2.5, L(S, 0.5, 1.25)),
        shell(rect(3, 16, 18, 4, rr(S, 1.5))), sq(6, 12.5, 4.5, 2.5, L(S, 0.5, 1.25)),
    ]


@icon("coat-rack", CAT, "Wall coat rack with a coat hanging from the middle peg",
      tags=["coat hooks", "coat stand", "hall", "hanger", "entrance", "furniture"], aliases=["coat-hooks"])
def _(S):
    coat = [(12, 8), (16.5, 10), (17, 20.5), (7, 20.5), (7.5, 10)]
    return [
        line(seg(3, 4, 21, 4) if S.name == "line" else seg(3.5, 4, 20.5, 4)),
        line(seg(5.5, 4, 5.5, 7)), line(seg(18.5, 4, 18.5, 7)), line(seg(12, 4, 12, 8)),
        shell(poly(coat, closed=True, r=S.r)),
        detail(poly([(9.5, 9), (12, 13), (14.5, 9)], r=S.r * 0.5)), detail(seg(12, 13, 12, 20.5)),
    ]


@icon("umbrella-stand", CAT, "Umbrella stand with two crook handles and a cane",
      tags=["umbrellas", "hall", "entrance", "rain", "stand", "furniture"])
def _(S):
    return [
        line("M9 10V4.5A1.75 1.75 0 0 0 5.5 4.5"),
        line("M13 10V6.5A1.75 1.75 0 0 0 9.5 6.5"),
        line(seg(16, 10, 16, 5)), dot(16, 3.75, 1.5),
        shell(rect(6, 10, 12, 11, rr(S, 2))),
        detail(seg(6, 13.5, 18, 13.5)),
    ]


@icon("smoke-detector", CAT, "Ceiling smoke detector with smoke rising towards it",
      tags=["smoke alarm", "fire alarm", "safety", "detector", "ceiling", "fire"], aliases=["smoke-alarm"])
def _(S):
    body = ("M4 3H20V6C20 8 18.5 9.5 16.5 9.5H7.5C5.5 9.5 4 8 4 6Z" if S.name == "line" else
            "M5.5 3H18.5A1.5 1.5 0 0 1 20 4.5V6C20 8 18.5 9.5 16.5 9.5H7.5C5.5 9.5 4 8 4 6V4.5A1.5 1.5 0 0 1 5.5 3Z")
    return [
        shell(body), dot(15.5, 6.25, 1),
        *[line(f"M{x} 21C{x - 1.6} 19.5 {x + 1.6} 17 {x} 15.5C{x - 1.2} 14.5 {x} 13.2 {x} 13.2") for x in (8, 12, 16)],
    ]


@icon("light-switch", CAT, "Wall light switch with a rocker",
      tags=["switch", "light", "on off", "toggle", "electric", "wall"], aliases=["wall-switch"])
def _(S):
    return [
        shell(rect(5, 3, 14, 18, rr(S))),
        detail(rect(9, 7, 6, 10, rr(S, 1.5))),
        sq(10, 8, 4, 3.5, L(S, 0, 1)),
    ]


@icon("ceiling-fan", CAT, "Ceiling fan with two blades and a light",
      tags=["fan", "cooling", "ceiling", "air", "ventilation", "light"])
def _(S):
    return [
        line(seg(9, 2, 15, 2) if S.name == "line" else seg(9.5, 2, 14.5, 2)),
        line(seg(12, 2, 12, 6.5)),
        shell(rect(9, 6.5, 6, 5, rr(S, 1.5))),
        line(seg(2, 10, 9, 8.5) if S.name == "line" else seg(3, 9.8, 9, 8.5)),
        line(seg(15, 8.5, 22, 10) if S.name == "line" else seg(15, 8.5, 21, 9.8)),
        shell("M9.5 11.5H14.5C14.5 13.3 13.4 14.5 12 14.5C10.6 14.5 9.5 13.3 9.5 11.5Z"),
        line(seg(8, 17.5, 7, 19.5)), line(seg(12, 18, 12, 20.5)), line(seg(16, 17.5, 17, 19.5)),
    ]


@icon("candle-holder", CAT, "Lit candle in a candlestick",
      tags=["candle", "candlestick", "flame", "light", "romantic", "decor"], aliases=["candlestick"])
def _(S):
    return [
        mark(flame(12, 2, 6, 3)),
        shell(rect(10, 7.5, 4, 8, rr(S, 1))),
        line(seg(7, 15.5, 17, 15.5) if S.name == "line" else seg(7.5, 15.5, 16.5, 15.5)),
        line(seg(12, 15.5, 12, 20.5)),
        line(seg(8.5, 21, 15.5, 21) if S.name == "line" else seg(9, 21, 15, 21)),
    ]


@icon("vase", CAT, "Rounded vase with a narrow neck and a band",
      tags=["pot", "urn", "ceramic", "flower vase", "decor", "pottery"], aliases=["urn"])
def _(S):
    d = ("M9 3H15V5C15 6 17.5 7.5 18 11C18.6 15.5 16.5 21 12 21C7.5 21 5.4 15.5 6 11C6.5 7.5 9 6 9 5Z" if S.name == "line" else
         "M10 3H14A1 1 0 0 1 15 4V5C15 6 17.5 7.5 18 11C18.6 15.5 16.5 21 12 21C7.5 21 5.4 15.5 6 11C6.5 7.5 9 6 9 5V4A1 1 0 0 1 10 3Z")
    return [shell(d), detail("M6.3 13.5H17.7")]


def _tip(a, p, b, r):
    import math
    if r <= 0:
        return f"L{fmt(p[0])} {fmt(p[1])}"
    la = math.hypot(a[0] - p[0], a[1] - p[1])
    lb = math.hypot(b[0] - p[0], b[1] - p[1])
    s0 = (p[0] + (a[0] - p[0]) * r / la, p[1] + (a[1] - p[1]) * r / la)
    e0 = (p[0] + (b[0] - p[0]) * r / lb, p[1] + (b[1] - p[1]) * r / lb)
    return f"L{fmt(s0[0])} {fmt(s0[1])}Q{fmt(p[0])} {fmt(p[1])} {fmt(e0[0])} {fmt(e0[1])}"


def _puffy(x0, y0, x1, y1, bow, r):
    """Pillow outline: corners pinched out, sides bowed inwards by `bow`; corners softened by r."""
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    c = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    ctrl = [(mx, y0 + bow), (x1 - bow, my), (mx, y1 - bow), (x0 + bow, my)]
    d = ""
    for i in range(4):
        p, q = c[i], c[(i + 1) % 4]
        cin = ctrl[i - 1]
        cout = ctrl[i]
        if r > 0:
            import math
            # start/end points just off the corner along the curve tangents
            la = math.hypot(cout[0] - p[0], cout[1] - p[1])
            lb = math.hypot(cin[0] - p[0], cin[1] - p[1])
            s0 = (p[0] + (cin[0] - p[0]) * r / lb, p[1] + (cin[1] - p[1]) * r / lb)
            e0 = (p[0] + (cout[0] - p[0]) * r / la, p[1] + (cout[1] - p[1]) * r / la)
            d += ("M" if i == 0 else "L") + f"{fmt(s0[0])} {fmt(s0[1])}Q{fmt(p[0])} {fmt(p[1])} {fmt(e0[0])} {fmt(e0[1])}"
            start = e0
        else:
            d += ("M" if i == 0 else "") + (f"{fmt(p[0])} {fmt(p[1])}" if i == 0 else "")
            start = p
        qx, qy = q
        d += f"Q{fmt(cout[0])} {fmt(cout[1])} {fmt(qx)} {fmt(qy)}" if r <= 0 else ""
        if r > 0:
            import math
            nxt_in = cout
            lq = math.hypot(nxt_in[0] - q[0], nxt_in[1] - q[1])
            endp = (q[0] + (nxt_in[0] - q[0]) * r / lq, q[1] + (nxt_in[1] - q[1]) * r / lq)
            d += f"Q{fmt(cout[0])} {fmt(cout[1])} {fmt(endp[0])} {fmt(endp[1])}"
    return d + "Z"


@icon("cushion", CAT, "Square cushion with a centre button",
      tags=["throw pillow", "sofa cushion", "pillow", "soft", "decor", "living room"], aliases=["throw-pillow"])
def _(S):
    return [shell(_puffy(4, 4, 20, 20, 2, L(S, 0, 1.2))), dot(12, 12, 1.5)]


@icon("pillow", CAT, "Bed pillow with soft pinched corners",
      tags=["bed pillow", "sleep", "bedroom", "rest", "soft", "hotel"])
def _(S):
    return [shell(_puffy(3, 6, 21, 18, 1.5, L(S, 0, 1.2)))]


@icon("blanket", CAT, "Blanket folded in three layers",
      tags=["throw", "quilt", "duvet", "warm", "bedding", "folded"], aliases=["throw-blanket"])
def _(S):
    r = L(S, 0, 1.5)
    top = f"M21 {5 + r}" + (f"A{r} {r} 0 0 0 {21 - r} 5" if r else "") + "H6A2.75 2.75 0 0 0 6 10.5H21Z"
    mid = "M3 10.5H18A2.75 2.75 0 0 1 18 16H3Z"
    bot = f"M21 16H6A2.5 2.5 0 0 0 6 21H{21 - r}" + (f"A{r} {r} 0 0 0 21 {21 - r}" if r else "") + "Z"
    return [shell(top), shell(mid), shell(bot), detail(seg(3, 10.5, 21, 10.5)), detail(seg(3, 16, 21, 16))]
