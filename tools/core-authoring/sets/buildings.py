"""TypeIcon Core: buildings and places.

Generic building types drawn front-on on the ground line y = 21 (outer edge 22).
Buildings take the "common" variant badges (bottom-right box 13–23), so each design keeps
its identifying mark (sign, emblem, roof shape) in the upper and left part of the drawing;
doors and plain windows may sit under the badge.

Windows are small solid blocks (`win`): solid in Line/Rounded, knocked out of Filled walls.
"""
from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d  # noqa: F401

CAT = "buildings"


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def win(x, y, w=2.0, h=2.0):
    """Window block: solid in Line/Rounded, knocked out of a Filled wall."""
    return Part("dot", rect(x, y, w, h))


def tri(pts):
    return Part("dot", poly(pts, closed=True))


def door(S, x0, x1, top, ground=21.0):
    """Square-headed door outline standing on the ground line."""
    return detail(poly([(x0, ground), (x0, top), (x1, top), (x1, ground)], r=S.r * 0.5))


def arch_door(x0, x1, top, ground=21.0):
    """Round-headed door; `top` is the crown of the arch."""
    r = (x1 - x0) / 2
    return detail(f"M{fmt(x0)} {fmt(ground)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(ground)}")


def hexagram(cx, cy, r):
    a = poly([(cx, cy - r), (cx + r * 0.866, cy + r / 2), (cx - r * 0.866, cy + r / 2)], closed=True)
    b = poly([(cx, cy + r), (cx + r * 0.866, cy - r / 2), (cx - r * 0.866, cy - r / 2)], closed=True)
    return path_to_d(U(P(a), P(b)))


# ============================================================================ civic and commercial

@icon("building", CAT, "Generic multi-storey building with windows and a door",
      tags=["building", "company", "business", "property", "address", "block"], aliases=["company"])
def _(S):
    return [
        shell(rect(5, 3, 14, 18, S.R)),
        win(8, 6.5), win(14, 6.5), win(8, 10.5), win(14, 10.5),
        door(S, 10, 14, 16),
    ]


@icon("office", CAT, "Office tower with ribbon windows and a lower side wing",
      tags=["office building", "workplace", "corporate", "headquarters", "business", "work"],
      aliases=["office-building"])
def _(S):
    return [
        shell(rect(3, 3, 11, 18, S.R)),
        shell(poly([(14, 9), (21, 9), (21, 21), (14, 21)], r=S.r)),
        detail(seg(6.5, 7, 10.5, 7)), detail(seg(6.5, 11, 10.5, 11)), detail(seg(6.5, 15, 10.5, 15)),
        win(16.5, 12.5), win(16.5, 16.5),
    ]


@icon("apartment", CAT, "Apartment block with a grid of windows",
      tags=["flats", "residential", "housing", "condo", "block", "home"], aliases=["flats", "condo"])
def _(S):
    parts = [shell(rect(4, 3, 16, 18, S.R))]
    for y in (6.5, 11, 15.5):
        parts += [win(7, y), win(11, y), win(15, y)]
    return parts


@icon("skyscraper", CAT, "Tall stepped skyscraper with an antenna",
      tags=["high-rise", "tower block", "city", "downtown", "tall building", "urban"], aliases=["high-rise"])
def _(S):
    return [
        shell(poly([(7, 21), (7, 9.5), (9, 9.5), (9, 5.5), (15, 5.5), (15, 9.5), (17, 9.5), (17, 21)], closed=True, r=S.r)),
        line(seg(12, 2, 12, 5.5)),
        detail(seg(12, 9.5, 12, 21)),
    ]


@icon("factory", CAT, "Factory with a chimney and a sawtooth roof",
      tags=["industry", "plant", "manufacturing", "industrial", "production", "mill"], aliases=["industry"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 3), (7, 3), (7, 12), (14, 8), (14, 12), (21, 8), (21, 21)], closed=True, r=S.r)),
        win(6, 15.5), win(11, 15.5), win(16, 15.5),
    ]


@icon("warehouse", CAT, "Warehouse with a low gable and a wide roller door",
      tags=["storage", "depot", "logistics", "distribution", "stock", "shed"], aliases=["depot"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 9), (12, 4.5), (21, 9), (21, 21)], closed=True, r=S.r)),
        detail(poly([(7, 21), (7, 12.5), (17, 12.5), (17, 21)], r=S.r * 0.5)),
        detail(seg(7, 16.75, 17, 16.75)),
    ]


def _shopfront(S):
    """Striped awning over a shop body (walls x 5–19); the awning is split from the wall in Filled."""
    return [
        shell(poly([(3, 9), (5, 3), (19, 3), (21, 9)], closed=True, r=S.r)),
        detail(seg(9.67, 3, 9, 9)), detail(seg(14.33, 3, 15, 9)),
        shell(poly([(5, 9), (5, 21), (19, 21), (19, 9)], closed=True, r=S.r)),
        detail(seg(3, 9, 21, 9)),
    ]


@icon("bank", CAT, "Bank with a pediment, four columns and a base",
      tags=["finance", "money", "banking", "institution", "savings", "columns"])
def _(S):
    return [
        shell(poly([(3, 9), (3, 8), (12, 3.5), (21, 8), (21, 9)], closed=True, r=S.r * 0.5)),
        dot(12, 6.6, 1),
        *[line(seg(x, 11.5, x, 17.5)) for x in (6, 10, 14, 18)],
        line(seg(3, 20.5, 21, 20.5)),
    ]


@icon("school", CAT, "Schoolhouse with a central gabled tower, a flag and a door",
      tags=["education", "primary school", "classroom", "academy", "kids", "learning"], aliases=["schoolhouse"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 12), (8, 12), (8, 8.5), (12, 5), (16, 8.5), (16, 12), (21, 12), (21, 21)], closed=True, r=S.r)),
        line(seg(12, 5, 12, 2)),
        solid(rect(12, 2, 3.5, 2.5)),
        dot(12, 10.25, 1.25),
        door(S, 10, 14, 16.5),
    ]


@icon("university", CAT, "Columned hall under a mortarboard; a university or college",
      tags=["college", "campus", "higher education", "academy", "faculty", "graduation"], aliases=["college", "campus"])
def _(S):
    return [
        shell(poly([(3, 6), (12, 2.5), (21, 6), (12, 9.5)], closed=True, r=S.r * 0.5), stroke_miterlimit="2"),
        line(seg(19.5, 6.8, 19.5, 10.5)),
        *[line(seg(x, 12.5, x, 17.5)) for x in (6.5, 12, 17.5)],
        line(seg(3, 20.5, 21, 20.5)),
    ]


# ============================================================================ places of worship

@icon("church", CAT, "Church with a steeple topped by a cross and an arched door",
      tags=["chapel", "christian", "worship", "religion", "parish", "steeple"], aliases=["chapel"])
def _(S):
    return [
        shell(poly([(4, 21), (4, 14), (9, 11.5), (9, 10), (12, 6.5), (15, 10), (15, 11.5), (20, 14), (20, 21)], closed=True, r=S.r)),
        line(seg(12, 2, 12, 6.5)), line(seg(10.25, 3.75, 13.75, 3.75)),
        arch_door(10, 14, 16),
    ]


@icon("mosque", CAT, "Mosque with a pointed dome, a crescent finial and two minarets",
      tags=["masjid", "islam", "muslim", "worship", "religion", "minaret"], aliases=["masjid"])
def _(S):
    dome = "M6.5 12.5C6.5 9 9.8 8.2 12 5.5C14.2 8.2 17.5 9 17.5 12.5Z"
    return [
        shell(dome),
        shell(poly([(6.5, 12.5), (6.5, 21), (17.5, 21), (17.5, 12.5)], closed=True, r=S.r)),
        line(seg(12, 3, 12, 5.5)),
        line(seg(3, 9.5, 3, 21)), line(seg(21, 9.5, 21, 21)),
        solid(poly([(2, 9.5), (3, 6), (4, 9.5)], closed=True)), solid(poly([(20, 9.5), (21, 6), (22, 9.5)], closed=True)),
        detail("M10 21V18.2C10 17 11 16.3 12 15.7C13 16.3 14 17 14 18.2V21"),
    ]


@icon("temple", CAT, "Hindu temple: a tiered tower with a finial over a doorway",
      tags=["hindu temple", "mandir", "gopuram", "shrine", "worship", "religion"], aliases=["mandir"])
def _(S):
    pts = [(3.5, 21), (3.5, 15), (5.5, 15), (6.5, 11), (8, 11), (9, 7), (10.5, 7), (10.5, 5), (13.5, 5), (13.5, 7),
           (15, 7), (16, 11), (17.5, 11), (18.5, 15), (20.5, 15), (20.5, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.5)),
        line(seg(12, 5, 12, 2)),
        arch_door(10, 14, 16),
    ]


@icon("synagogue", CAT, "Synagogue with a Star of David and an arched door",
      tags=["jewish", "judaism", "shul", "worship", "religion", "temple"], aliases=["shul"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 10), (12, 4), (21, 10), (21, 21)], closed=True, r=S.r)),
        Part("dot", hexagram(12, 11, 3.2)),
        arch_door(10, 14, 17),
    ]


# ============================================================================ homes and shelters

@icon("castle", CAT, "Castle with two turrets, a battlement and a gate",
      tags=["fortress", "palace", "kingdom", "medieval", "fort", "fairy tale"], aliases=["fortress"])
def _(S):
    pts = [(3, 21), (3, 8.5), (5.5, 4.25), (8, 8.5), (8, 10.5), (10, 10.5), (10, 8.5), (14, 8.5), (14, 10.5),
           (16, 10.5), (16, 8.5), (18.5, 4.25), (21, 8.5), (21, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.5)),
        win(4.5, 12, 2, 2.5),
        arch_door(10, 14, 16),
    ]


_TENT_ROOF = "M3.5 11L12 4L20.5 11A2.83 2.83 0 0 1 14.83 11A2.83 2.83 0 0 1 9.17 11A2.83 2.83 0 0 1 3.5 11Z"
_TENT_DOOR = [(9.5, 21), (12, 16.5), (14.5, 21)]


def _tent_filled():
    roof = U(P(_TENT_ROOF), ST(_TENT_ROOF, 2))
    body = P(rect(4, 15, 16, 7))
    return U(roof, D(body, P(poly(_TENT_DOOR, closed=True)), ST(poly(_TENT_DOOR), 1.5), ST(_TENT_ROOF, 5)))


@icon("tent", CAT, "Event marquee tent with a scalloped roof and a tied-back door",
      tags=["marquee", "pavilion", "party tent", "event", "canopy", "fair"], aliases=["pavilion"],
      filled=_tent_filled)
def _(S):
    return [
        shell(_TENT_ROOF),
        line(poly([(5, 15.5), (5, 21), (19, 21), (19, 15.5)], r=S.r)),
        detail(poly(_TENT_DOOR, r=S.r * 0.5)),
    ]


def _house(S, body_top=9.22):
    """Home-style roof line with an overhang plus a gabled body (walls x 5–19)."""
    return [
        line(poly([(3, 11), (12, 3), (21, 11)], r=S.r)),
        shell(poly([(5, body_top), (12, 3), (19, body_top), (19, 21), (5, 21)], closed=True, r=S.r * 0.5)),
    ]


@icon("cabin", CAT, "Log cabin with a chimney and stacked log walls",
      tags=["log cabin", "cottage", "chalet", "lodge", "woods", "hut"], aliases=["log-cabin", "cottage"])
def _(S):
    return [
        *_house(S),
        line(seg(7.5, 3.5, 7.5, 7)),
        detail(seg(5, 13, 19, 13)), detail(seg(5, 17, 19, 17)),
    ]


@icon("hotel", CAT, "Hotel building with an H sign and an entrance",
      tags=["lodging", "accommodation", "inn", "stay", "travel", "motel"], aliases=["inn", "motel"])
def _(S):
    return [
        shell(rect(5, 3, 14, 18, S.R)),
        detail(seg(9, 6, 9, 12)), detail(seg(15, 6, 15, 12)), detail(seg(9, 9, 15, 9)),
        door(S, 10, 14, 16.5),
    ]


# ============================================================================ food, culture and leisure

@icon("restaurant", CAT, "Restaurant building with a fork and knife on the front",
      tags=["dining", "eatery", "food", "dinner", "bistro", "eat out"], aliases=["eatery"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 10), (12, 4), (21, 10), (21, 21)], closed=True, r=S.r)),
        detail("M7 10.5V13A2 2 0 0 0 11 13V10.5"), detail(seg(9, 15, 9, 19)),
        detail("M15 19V10.5C16.8 11.5 17 13.5 17 15.5H15"),
    ]


@icon("cafe", CAT, "Cafe front with a striped awning and a coffee cup in the window",
      tags=["coffee shop", "coffee house", "bistro", "espresso", "tea room", "snack bar"], aliases=["coffee-shop"])
def _(S):
    return [
        *_shopfront(S),
        detail("M7.5 13H13.5V15.5A3 3 0 0 1 10.5 18.5A3 3 0 0 1 7.5 15.5Z"),
        detail("M13.5 13.75H14A1.5 1.5 0 0 1 14 16.75H13"),
    ]


@icon("museum", CAT, "Museum hall with a pediment, three columns and front steps",
      tags=["gallery", "exhibition", "history", "culture", "heritage", "art"])
def _(S):
    return [
        shell(poly([(3, 9), (3, 8), (12, 3.5), (21, 8), (21, 9)], closed=True, r=S.r * 0.5)),
        *[line(seg(x, 11.5, x, 15.5)) for x in (6.5, 12, 17.5)],
        line(seg(4.5, 17.5, 19.5, 17.5)),
        line(seg(3, 21, 21, 21)),
    ]


@icon("library-building", CAT, "Library building with an open book on the front",
      tags=["library", "public library", "books", "reading", "archive", "study"], aliases=["public-library"])
def _(S):
    book = "M6.5 12C8.5 11.3 10.5 11.5 12 12.8C13.5 11.5 15.5 11.3 17.5 12V17.5C15.5 16.8 13.5 17 12 18.3C10.5 17 8.5 16.8 6.5 17.5Z"
    return [
        shell(poly([(3, 21), (3, 10), (12, 4), (21, 10), (21, 21)], closed=True, r=S.r)),
        detail(book), detail(seg(12, 12.8, 12, 18.3)),
    ]


@icon("stadium", CAT, "Stadium bowl with tiered stands around the pitch",
      tags=["sports ground", "football", "soccer", "match", "venue", "field"], aliases=["sports-ground"])
def _(S):
    return [
        shell("M2.5 10.5C2.5 7.7 6.8 5.5 12 5.5C17.2 5.5 21.5 7.7 21.5 10.5V15.5C21.5 18.3 17.2 20.5 12 20.5"
              "C6.8 20.5 2.5 18.3 2.5 15.5Z"),
        detail("M2.5 10.5C2.5 13.3 6.8 15.5 12 15.5C17.2 15.5 21.5 13.3 21.5 10.5"),
        Part("dot", poly([(7.5, 10.5), (9.5, 9), (14.5, 9), (16.5, 10.5), (14.5, 12), (9.5, 12)], closed=True)
             if S.name == "line" else ellipse(12, 10.5, 4.6, 1.6)),
        detail(seg(7, 15, 7, 20)), detail(seg(17, 15, 17, 20)),
    ]


@icon("theater", CAT, "Theatre stage framed by draped curtains",
      tags=["theatre", "stage", "playhouse", "drama", "performance", "curtains"], aliases=["theatre", "playhouse"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(3, 7, 21, 7)),
        detail("M10 7C10 11.5 8 14.5 3 16"), detail("M14 7C14 11.5 16 14.5 21 16"),
    ]


@icon("cinema", CAT, "Cinema building with a play sign over the entrance",
      tags=["movie theater", "movies", "film", "pictures", "screening", "multiplex"], aliases=["movie-theater"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(rect(6.5, 6.5, 11, 6.5, min(S.R, 1))),
        tri([(10.5, 8), (14, 9.75), (10.5, 11.5)]),
        door(S, 10, 14, 16.5),
    ]


# ============================================================================ landmarks and structures

@icon("lighthouse", CAT, "Lighthouse tower with a lantern room and light beams",
      tags=["beacon", "coast", "harbor light", "navigation", "sea", "guide"])
def _(S):
    return [
        shell(poly([(8, 21), (9.5, 10), (14.5, 10), (16, 21)], closed=True, r=S.r * 0.5)),
        shell(poly([(10, 10), (10, 6), (12, 3.5), (14, 6), (14, 10)], closed=True, r=S.r * 0.5)),
        detail(seg(8.9, 14.5, 15.1, 14.5)),
        line(seg(3, 5, 6.5, 6.5)), line(seg(3, 10, 6.5, 8.5)),
        line(seg(21, 5, 17.5, 6.5)), line(seg(21, 10, 17.5, 8.5)),
    ]


@icon("bridge", CAT, "Arched bridge with a railing",
      tags=["arch bridge", "crossing", "river", "viaduct", "road", "span"], aliases=["viaduct"])
def _(S):
    return [
        shell("M2 11H22V20H18A6 6 0 0 0 6 20H2Z" if S.name == "line" else
              "M4 11H20A2 2 0 0 1 22 13V20H18A6 6 0 0 0 6 20H2V13A2 2 0 0 1 4 11Z"),
        line(seg(2, 5.5, 22, 5.5)),
        *[line(seg(x, 5.5, x, 11)) for x in (5, 12, 19)],
    ]


@icon("tower", CAT, "Observation tower with a viewing pod and an antenna",
      tags=["tv tower", "observation tower", "lookout", "telecom tower", "landmark", "city"],
      aliases=["observation-tower"])
def _(S):
    return [
        shell(rect(7.5, 7, 9, 4, min(S.R, 2))),
        line(seg(12, 2, 12, 7)),
        line(poly([(9.5, 21), (11, 11)])), line(poly([(14.5, 21), (13, 11)])),
        line(seg(9, 21, 15, 21) if S.name == "line" else seg(10, 21, 14, 21)),
    ]


@icon("windmill", CAT, "Traditional windmill with four sails",
      tags=["mill", "wind", "farm", "dutch", "countryside", "grain"], aliases=["mill"])
def _(S):
    hub = (12, 9)
    return [
        shell(poly([(8, 21), (9.5, 12), (14.5, 12), (16, 21)], closed=True, r=S.r * 0.5)),
        *[line(seg(hub[0] + dx * 1.5, hub[1] + dy * 1.5, hub[0] + dx * 7, hub[1] + dy * 7))
          for dx, dy in ((-0.7071, -0.7071), (0.7071, -0.7071), (-0.7071, 0.7071), (0.7071, 0.7071))],
        dot(12, 9, 1.5),
        arch_door(10.5, 13.5, 17),
    ]


@icon("barn", CAT, "Farm barn with a gambrel roof, a hayloft and a braced door",
      tags=["farm", "ranch", "stable", "agriculture", "countryside", "shed"], aliases=["farm"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 11), (5.5, 6), (12, 3), (18.5, 6), (21, 11), (21, 21)], closed=True, r=S.r)),
        win(11, 7, 2, 2),
        detail(poly([(7.5, 21), (7.5, 12.5), (16.5, 12.5), (16.5, 21)], r=S.r * 0.5)),
        detail(seg(7.5, 12.5, 16.5, 21)), detail(seg(16.5, 12.5, 7.5, 21)),
    ]


@icon("igloo", CAT, "Snow-block igloo with an entrance",
      tags=["ice house", "snow", "arctic", "winter", "inuit", "shelter"])
def _(S):
    return [
        shell("M3 20A9 11 0 0 1 21 20Z"),
        detail(seg(5.8, 12, 18.2, 12)),
        detail(seg(12, 9, 12, 12)),
        arch_door(9, 15, 15),
    ]


@icon("pyramid", CAT, "Ancient stone pyramid with a shaded face",
      tags=["egypt", "ancient", "tomb", "wonder", "desert", "giza"])
def _(S):
    return [
        shell(poly([(3.5, 20), (12, 4), (20.5, 20)], closed=True, r=S.r)),
        detail(seg(12, 4, 15, 20)),
    ]


@icon("monument", CAT, "Obelisk monument on a pedestal",
      tags=["obelisk", "memorial", "landmark", "tribute", "historic", "statue"], aliases=["obelisk", "memorial"])
def _(S):
    return [
        shell(poly([(9.5, 17), (10.5, 5.5), (12, 3), (13.5, 5.5), (14.5, 17)], closed=True, r=S.r * 0.5)),
        shell(rect(6, 17, 12, 4, min(S.R, 1.5))),
    ]


@icon("fountain", CAT, "Tiered fountain with water arcing into a basin",
      tags=["water feature", "plaza", "park", "garden", "spring", "square"])
def _(S):
    return [
        shell("M3 15H21C21 18.5 17 20.5 12 20.5C7 20.5 3 18.5 3 15Z"),
        shell("M8.5 9.5H15.5C15.5 11.3 14 12.3 12 12.3C10 12.3 8.5 11.3 8.5 9.5Z"),
        line(seg(12, 12.3, 12, 15)),
        line(seg(12, 4, 12, 9.5)),
        line("M12 4C9 4 6 6 5 12.5"), line("M12 4C15 4 18 6 19 12.5"),
    ]


@icon("park", CAT, "Park with a leafy tree and a bench",
      tags=["garden", "green space", "outdoors", "nature", "recreation", "public park"], aliases=["public-park"])
def _(S):
    return [
        shell(circle(16.5, 8, 4.5)),
        line(seg(16.5, 12.5, 16.5, 21)),
        line(seg(2.5, 12.5, 11.5, 12.5)), line(seg(2.5, 16.5, 11.5, 16.5)),
        line(seg(4, 12.5, 4, 21)), line(seg(10, 12.5, 10, 21)),
    ]


@icon("playground", CAT, "Playground swing set with a hanging seat",
      tags=["swing", "play area", "kids", "children", "recreation", "school yard"], aliases=["swing-set"])
def _(S):
    return [
        line(poly([(3, 21), (5.5, 4), (18.5, 4), (21, 21)], r=S.r)),
        line(seg(9.5, 4, 9.5, 15)), line(seg(14.5, 4, 14.5, 15)),
        shell(rect(8.5, 15, 7, 2, min(S.R, 1))),
    ]


# ============================================================================ services and transport

@icon("gas-station", CAT, "Filling station: a fuel pump under a canopy",
      tags=["petrol station", "fuel", "gas", "filling station", "service station", "refuel"],
      aliases=["petrol-station", "filling-station"])
def _(S):
    return [
        shell(rect(3, 3, 18, 3.5, min(S.R, 1.5))),
        line(seg(4.5, 6.5, 4.5, 21)), line(seg(19.5, 6.5, 19.5, 21)),
        shell(rect(8.5, 10.5, 6, 10.5, min(S.R, 1.5))),
        win(10.5, 12.5, 2, 2),
        line(poly([(14.5, 13), (16.5, 13), (16.5, 18)], r=S.r * 0.5)),
    ]


@icon("parking", CAT, "Parking sign: a letter P on a square panel",
      tags=["car park", "parking lot", "park", "garage", "sign", "vehicle"], aliases=["car-park", "parking-lot"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(poly([(9.5, 17), (9.5, 7), (13, 7)], r=S.r * 0.5) + "A3 3 0 0 1 13 13H9.5"),
    ]


def _star_d(cx, cy, ro, ri):
    return poly([pt for i in range(5) for pt in (polar_pt(cx, cy, ro, -90 + 72 * i), polar_pt(cx, cy, ri, -54 + 72 * i))], closed=True)


def polar_pt(cx, cy, r, deg):
    import math
    return (cx + r * math.cos(math.radians(deg)), cy + r * math.sin(math.radians(deg)))


@icon("police-station", CAT, "Police station with a roof light and a star badge",
      tags=["police", "precinct", "law enforcement", "sheriff", "cops", "security"], aliases=["precinct"])
def _(S):
    return [
        shell(rect(3, 6, 18, 15, S.R)),
        shell("M9.5 6V5.5A2.5 2.5 0 0 1 14.5 5.5V6Z"),
        Part("dot", _star_d(12, 11.8, 3.6, 1.5)),
        door(S, 10, 14, 17),
    ]


@icon("fire-station", CAT, "Fire station with a flame sign over a wide engine bay",
      tags=["fire department", "firehouse", "fire brigade", "emergency", "firefighter", "rescue"],
      aliases=["firehouse", "fire-department"])
def _(S):
    flame = ("M12 4.5C12.3 6.3 15 7.3 15 10.2A3 3 0 0 1 9 10.2C9 9 9.6 8.1 10.4 7.5"
             "C10.5 8.5 11 9.1 11.6 9.3C11.2 7.8 11.3 6 12 4.5Z")
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        Part("dot", flame),
        detail(poly([(6.5, 21), (6.5, 15), (17.5, 15), (17.5, 21)], r=S.r * 0.5)),
        detail(seg(6.5, 18, 17.5, 18)),
    ]


@icon("post-office", CAT, "Post office with an envelope sign over the door",
      tags=["postal", "mail", "post", "letters", "parcel", "courier"], aliases=["postal-office"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(rect(7, 6.5, 10, 6.5, min(S.R, 1))),
        detail(poly([(7, 6.5), (12, 10), (17, 6.5)], r=S.r * 0.5)),
        door(S, 10, 14, 16.5),
    ]


@icon("courthouse", CAT, "Courthouse: the scales of justice under a pediment",
      tags=["court", "justice", "law", "judge", "legal", "tribunal"], aliases=["court-house"])
def _(S):
    return [
        shell(poly([(3, 9), (3, 8), (12, 3.5), (21, 8), (21, 9)], closed=True, r=S.r * 0.5)),
        line(seg(12, 11, 12, 18)), line(seg(5.5, 12.5, 18.5, 12.5)),
        line(seg(7, 12.5, 7, 14)), line(seg(17, 12.5, 17, 14)),
        solid("M4.5 14.5H9.5A2.5 2.5 0 0 1 4.5 14.5Z"), solid("M14.5 14.5H19.5A2.5 2.5 0 0 1 14.5 14.5Z"),
        line(seg(3, 20.5, 21, 20.5)),
    ]


@icon("airport", CAT, "Airport control tower beside a terminal building",
      tags=["terminal", "airfield", "flights", "control tower", "aviation", "travel"], aliases=["air-terminal"])
def _(S):
    return [
        shell(poly([(3, 3.5), (13, 3.5), (11.5, 8), (4.5, 8)], closed=True, r=S.r * 0.5)),
        shell(poly([(6.5, 8), (6.5, 21), (9.5, 21), (9.5, 8)], closed=True, r=S.r * 0.5)),
        shell(poly([(9.5, 13), (21, 13), (21, 21), (9.5, 21)], r=S.r)),
        detail(seg(12.5, 16.5, 18, 16.5)),
    ]


@icon("train-station", CAT, "Train station: a locomotive front under a platform canopy",
      tags=["railway station", "rail", "depot", "platform", "metro", "commute"], aliases=["railway-station"])
def _(S):
    return [
        line(poly([(3, 8.5), (12, 3.5), (21, 8.5)], r=S.r)),
        shell(rect(7, 9.5, 10, 9.5, min(S.R, 3))),
        detail(rect(9, 11.5, 6, 3, min(S.R, 1))),
        dot(9.5, 16.5, 1), dot(14.5, 16.5, 1),
        line(seg(8.5, 19, 6.5, 21.5)), line(seg(15.5, 19, 17.5, 21.5)),
    ]


@icon("bus-stop", CAT, "Bus stop: a roofed shelter with a bench beside a stop sign",
      tags=["bus shelter", "transit", "public transport", "stop", "commute", "station"], aliases=["bus-shelter"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 12.5, 3, min(S.R, 1.5))),
        line(seg(4, 6.5, 4, 21)), line(seg(13.5, 6.5, 13.5, 21)),
        line(seg(4, 15, 13.5, 15)),
        shell(rect(16.5, 3.5, 5, 6, min(S.R, 1.5))),
        line(seg(19, 9.5, 19, 21)),
    ]


@icon("harbor", CAT, "Harbour: an anchor above the waterline",
      tags=["harbour", "port", "marina", "dock", "seaport", "maritime"], aliases=["harbour", "marina"])
def _(S):
    return [
        shell(circle(12, 4.5, 1.75)),
        line(seg(12, 6.25, 12, 16)), line(seg(8.5, 9, 15.5, 9)),
        line("M5.5 11.5A6.5 5 0 0 0 18.5 11.5"),
        line("M3 20.5C5 19 7 19 9 20.5C11 22 13 22 15 20.5C17 19 19 19 21 20.5"),
    ]


@icon("capitol", CAT, "Capitol building with a central dome over a colonnade and wings",
      tags=["government", "parliament", "congress", "legislature", "state house", "politics"],
      aliases=["parliament", "state-house"])
def _(S):
    return [
        line(seg(12, 2, 12, 5)),
        shell("M7.5 10A4.5 4.5 0 0 1 16.5 10Z"),
        shell(poly([(3, 21), (3, 14), (6.5, 14), (6.5, 10), (17.5, 10), (17.5, 14), (21, 14), (21, 21)], closed=True, r=S.r * 0.5)),
        *[detail(seg(x, 13, x, 18)) for x in (9.5, 12, 14.5)],
    ]


@icon("pagoda", CAT, "Pagoda with three tiers of upturned eaves",
      tags=["asian temple", "buddhist", "tower", "stupa", "japan", "china"])
def _(S):
    def roof(y, half):
        return line(f"M{fmt(12 - half)} {fmt(y + 1.5)}Q{fmt(12 - half + 2.5)} {fmt(y + 1.5)} {fmt(12 - half + 3.5)} {fmt(y)}"
                    f"H{fmt(12 + half - 3.5)}Q{fmt(12 + half - 2.5)} {fmt(y + 1.5)} {fmt(12 + half)} {fmt(y + 1.5)}")
    return [
        line(seg(12, 2, 12, 5)),
        roof(5, 6), roof(10, 7.5), roof(15, 9),
        shell(poly([(9, 7), (9, 10), (15, 10), (15, 7)], r=S.r * 0.5)),
        shell(poly([(8, 12), (8, 15), (16, 15), (16, 12)], r=S.r * 0.5)),
        shell(poly([(7, 17), (7, 21), (17, 21), (17, 17)], r=S.r * 0.5)),
    ]


@icon("arena", CAT, "Indoor arena with a shallow domed roof over arched entrances",
      tags=["indoor stadium", "sports hall", "concert venue", "dome", "events", "coliseum"], aliases=["sports-hall"])
def _(S):
    return [
        shell("M3 12.5C3 8.5 7 5.5 12 5.5C17 5.5 21 8.5 21 12.5Z"),
        shell(poly([(3, 12.5), (3, 21), (21, 21), (21, 12.5)], closed=True, r=S.r)),
        detail(seg(12, 5.5, 12, 12.5)),
        arch_door(5.5, 8.5, 15.5), arch_door(10.5, 13.5, 15.5), arch_door(15.5, 18.5, 15.5),
    ]


@icon("mall", CAT, "Shopping mall with a shopping-bag sign over a double door",
      tags=["shopping mall", "shopping centre", "retail", "plaza", "outlet", "stores"],
      aliases=["shopping-mall", "shopping-center"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(poly([(8.5, 8), (15.5, 8), (16.5, 13), (7.5, 13)], closed=True, r=S.r * 0.5)),
        detail("M10.25 8V7.5A1.75 1.75 0 0 1 13.75 7.5V8"),
        door(S, 9, 15, 17), detail(seg(12, 17, 12, 21)),
    ]


@icon("supermarket", CAT, "Supermarket building with a shopping cart on the front",
      tags=["grocery store", "groceries", "market", "hypermarket", "food shop", "retail"],
      aliases=["grocery-store"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(3, 7, 21, 7)),
        detail(poly([(6, 10.5), (8, 10.5), (9.5, 15.5), (16, 15.5), (17.5, 11.5), (8.7, 11.5)], r=S.r * 0.5)),
        dot(10.25, 18.25, 1.1), dot(15.25, 18.25, 1.1),
    ]


@icon("pharmacy", CAT, "Pharmacy front with an awning and a medical cross",
      tags=["chemist", "drugstore", "apothecary", "medicine", "prescription", "health"], aliases=["chemist", "drugstore"])
def _(S):
    return [*_shopfront(S), detail(seg(12, 11.5, 12, 18.5)), detail(seg(8.5, 15, 15.5, 15))]


@icon("gym-building", CAT, "Gym building with a dumbbell sign over the door",
      tags=["gym", "fitness center", "health club", "workout", "training", "sport"], aliases=["fitness-center"])
def _(S):
    left = poly([(5, 8.5), (7, 8.5), (7, 6.5), (9, 6.5), (9, 12.5), (7, 12.5), (7, 10.5), (5, 10.5)], closed=True)
    right = poly([(19, 8.5), (17, 8.5), (17, 6.5), (15, 6.5), (15, 12.5), (17, 12.5), (17, 10.5), (19, 10.5)], closed=True)
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        Part("dot", left), Part("dot", right), detail(seg(9, 9.5, 15, 9.5)),
        door(S, 10, 14, 16),
    ]


@icon("spa", CAT, "Lotus flower over still water; a spa or wellness centre",
      tags=["wellness", "lotus", "relax", "massage", "sauna", "beauty"], aliases=["wellness"])
def _(S):
    return [
        shell("M12 4.5C14.3 6.8 14.8 10.8 12 15C9.2 10.8 9.7 6.8 12 4.5Z"),
        line("M12 15C8.5 15 5.5 12.5 4 8.5C7.5 8.8 10.2 10.8 11 13.2"),
        line("M12 15C15.5 15 18.5 12.5 20 8.5C16.5 8.8 13.8 10.8 13 13.2"),
        line(seg(4, 19, 20, 19) if S.name == "line" else seg(5, 19, 19, 19)),
    ]


@icon("garage-building", CAT, "Garage: a car under a pitched roof",
      tags=["garage", "car port", "auto repair", "workshop", "parking", "vehicle"])
def _(S):
    return [
        line(poly([(3, 10), (12, 3.5), (21, 10)], r=S.r)),
        shell(poly([(6, 19), (6, 15), (8, 11), (16, 11), (18, 15), (18, 19)], closed=True, r=S.r)),
        detail(seg(6, 15, 18, 15)),
        dot(8.75, 17, 1), dot(15.25, 17, 1),
        solid(rect(6.5, 19, 2.5, 2)), solid(rect(15, 19, 2.5, 2)),
    ]
