"""TypeIcon Core: property (batch 001). Houses, lots, rooms and listing marks, drawn front-on or in plan."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d  # noqa: F401

CAT = "property"


def L(S, a, b):
    return a if S.name == "line" else b


def win(x, y, w=2.0, h=2.0):
    return Part("dot", rect(x, y, w, h))


def door(S, x0, x1, top, ground=21.0):
    return detail(poly([(x0, ground), (x0, top), (x1, top), (x1, ground)], r=S.r * 0.5))


def arch_door(x0, x1, top, ground=21.0):
    r = (x1 - x0) / 2
    return detail(f"M{fmt(x0)} {fmt(ground)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(ground)}")


def dash_paths(pts, on=2.5, off=4.0, closed=False):
    """Split a polyline into dash polylines (lists of points)."""
    pts = list(pts) + ([pts[0]] if closed else [])
    out, cur, drawing, rem = [], [pts[0]], True, on
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        dx, dy = x2 - x1, y2 - y1
        ln = math.hypot(dx, dy)
        pos = 0.0
        while ln - pos > 1e-9:
            step = min(rem, ln - pos)
            q = (x1 + dx * (pos + step) / ln, y1 + dy * (pos + step) / ln)
            if drawing:
                cur.append(q)
            pos += step
            rem -= step
            if rem <= 1e-9:
                if drawing:
                    out.append(cur)
                    cur = []
                else:
                    cur = [q]
                drawing = not drawing
                rem = on if drawing else off
    if drawing and len(cur) > 1:
        out.append(cur)
    return [c for c in out if len(c) > 1]


def dashed(pts, kind=detail, on=2.5, off=4.0, closed=False):
    return [kind(poly(c)) for c in dash_paths(pts, on, off, closed)]


def _arc_pts(cx, cy, r, a0, a1, n=14):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def house(S, x0, x1, wall, peak, ground=21.0):
    xm = (x0 + x1) / 2
    return shell(poly([(x0, ground), (x0, wall), (xm, peak), (x1, wall), (x1, ground)], closed=True, r=S.r))


# ============================================================================ house types

@icon("split-level-house", CAT, "House with two side-by-side sections at staggered heights",
      tags=["split level", "house", "home", "mid-century", "residential", "two level"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 14), (7.5, 10), (12, 14), (12, 9), (16.5, 5), (21, 9), (21, 21)], closed=True, r=S.r)),
        detail(seg(12, 14, 12, 21)),
        win(6.5, 16.5), door(S, 15, 18, 15),
    ]


@icon("prairie-style-house", CAT, "Long low house with a shallow hipped roof and a band of windows",
      tags=["prairie house", "ranch", "low house", "horizontal", "prairie school", "home", "residential"])
def _(S):
    return [
        shell(poly([(2, 11), (6, 6.5), (18, 6.5), (22, 11)], closed=True, r=S.r)),
        shell(poly([(4, 11), (4, 20), (20, 20), (20, 11)], closed=True, r=S.r)),
        detail(seg(7, 15.5, 17, 15.5)),
    ]


@icon("basement-apartment", CAT, "House cross-section with a unit below the ground line and its own entrance",
      tags=["basement flat", "lower unit", "garden flat", "below ground", "rental", "in-law suite", "apartment"])
def _(S):
    return [
        shell(poly([(4, 21), (4, 8), (11, 3.5), (18, 8), (18, 21)], closed=True, r=S.r)),
        detail(seg(4, 12, 18, 12)),
        line(seg(2, 12, 4, 12)),
        win(7, 7.5, 2, 2), win(7, 15.5, 3, 2.5),
        door(S, 13, 16, 15),
        line(poly([(18, 12), (20, 12), (20, 16), (22, 16)], r=S.r)),
    ]


@icon("accessory-dwelling-unit", CAT, "Main house with a smaller cottage standing behind it on the same lot",
      tags=["adu", "granny flat", "backyard cottage", "in-law unit", "secondary dwelling", "second home", "guest house"],
      aliases=["granny-flat"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 11), (7.5, 6), (12, 11), (12, 21)], closed=True, r=S.r)),
        door(S, 6, 9, 15),
        shell(poly([(16, 21), (16, 16), (18.5, 13), (21, 16), (21, 21)], closed=True, r=S.r * 0.6)),
    ]


@icon("carriage-house", CAT, "Two-storey outbuilding with two garage doors below and windows above",
      tags=["coach house", "garage apartment", "garage flat", "outbuilding", "stable", "garage loft"],
      aliases=["coach-house"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 8), (12, 3.5), (21, 8), (21, 21)], closed=True, r=S.r)),
        win(7, 9, 2, 2), win(15, 9, 2, 2),
        detail(poly([(5.5, 21), (5.5, 14.5), (18.5, 14.5), (18.5, 21)], r=S.r * 0.5)),
        detail(seg(12, 14.5, 12, 21)),
    ]


@icon("mixed-use-building", CAT, "Building with a shop awning on the ground floor and apartments above",
      tags=["shop and flat", "retail and residential", "live work", "storefront apartments", "commercial residential", "high street"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 18.5, S.R)),
        win(7.5, 5), win(11, 5), win(14.5, 5), win(7.5, 8.5), win(11, 8.5), win(14.5, 8.5),
        solid(poly([(3.5, 12.5), (20.5, 12.5), (21.5, 16), (2.5, 16), (3.5, 12.5)], closed=True)),
        win(7, 17.5, 4, 2), win(13, 17.5, 4, 2),
    ]


@icon("penthouse", CAT, "Apartment tower with a set-back top floor and a roof terrace with a tree",
      tags=["top floor", "luxury apartment", "rooftop terrace", "sky home", "high rise", "roof garden"])
def _(S):
    return [
        shell(poly([(4, 21), (4, 10), (20, 10), (20, 21)], closed=True, r=S.r)),
        shell(poly([(4, 10), (4, 4), (12, 4), (12, 10)], closed=True, r=S.r)),
        win(7, 6.2, 2, 2),
        line(seg(17, 10, 17, 7.5)), solid(circle(17, 5.5, 2.5)),
        win(7, 14), win(11, 14), win(15, 14),
    ]


@icon("beach-house", CAT, "House raised on stilts above waves with a palm tree beside it",
      tags=["stilt house", "seaside home", "coastal", "waterfront", "holiday home", "palm tree", "ocean"])
def _(S):
    return [
        shell(poly([(3, 13), (3, 8.5), (8, 4.5), (13, 8.5), (13, 13)], closed=True, r=S.r)),
        line(seg(4.5, 13, 4.5, 18.5)), line(seg(11.5, 13, 11.5, 18.5)),
        win(7, 9, 2, 2),
        line("M2 21q1.5-1.5 3 0t3 0t3 0t3 0"),
        line("M19 20Q20 14 18.5 10"),
        line("M18.5 10q-2-2.5-4.5-1.5"), line("M18.5 10q2-2.5 3.5-1.5"),
    ]


@icon("vacation-rental", CAT, "House with a wheeled suitcase standing beside its door",
      tags=["holiday rental", "short term rental", "rental listing", "holiday let", "stay", "travel", "booking"],
      aliases=["holiday-let"])
def _(S):
    return [
        shell(poly([(2, 21), (2, 10), (6.5, 5), (11, 10), (11, 21)], closed=True, r=S.r)),
        door(S, 5, 8, 15),
        shell(rect(15, 12, 6, 8, min(S.R, 2))),
        line(poly([(16.5, 12), (16.5, 9.5), (19.5, 9.5), (19.5, 12)], r=S.r * 0.5)),
        detail(seg(15, 15.5, 21, 15.5)), dot(16.5, 21.2, 0.8), dot(19.5, 21.2, 0.8),
    ]


@icon("timeshare", CAT, "House above a calendar strip with one week block filled",
      tags=["shared ownership", "fractional ownership", "vacation ownership", "weeks", "holiday home share", "calendar"])
def _(S):
    return [
        shell(poly([(6, 11), (6, 7), (12, 3), (18, 7), (18, 11)], closed=True, r=S.r)),
        shell(rect(3, 14, 18, 7, min(S.R, 2))),
        detail(seg(9, 14, 9, 21)), detail(seg(15, 14, 15, 21)),
        solid(rect(9, 14, 6, 7)),
    ]


@icon("modular-home", CAT, "House module lowered by a crane hook onto a foundation below",
      tags=["prefab", "prefabricated", "factory built", "panelised", "off-site construction", "crane lift", "module"],
      aliases=["prefab-home"])
def _(S):
    return [
        dot(12, 3.5, 1.6),
        shell(poly([(5, 14), (5, 10), (12, 6), (19, 10), (19, 14)], closed=True, r=S.r)),
        win(10.8, 10, 2.4, 2.4),
        line(poly([(4, 17), (4, 21), (20, 21), (20, 17)], r=S.r)),
    ]


@icon("foreclosed-house", CAT, "House with boards nailed across the door and a notice beside it",
      tags=["foreclosure", "repossessed", "boarded up", "bank owned", "seized", "distressed property", "reo"],
      aliases=["repossessed-house"])
def _(S):
    return [
        house(S, 3, 21, 10, 3.5),
        win(5.5, 12.5, 3, 4),
        door(S, 11, 17, 13.5),
        detail(seg(11, 14, 17, 20)), detail(seg(17, 14, 11, 20)),
    ]


@icon("fixer-upper", CAT, "Run-down house with a broken roof, a crooked shutter and a hammer beside it",
      tags=["needs work", "renovation project", "handyman special", "run down", "dilapidated", "diy home", "repair"])
def _(S):
    return [
        shell(poly([(2, 21), (2, 11), (7, 6), (9, 8.5), (10.5, 7.5), (12, 11), (12, 21)], closed=True, r=S.r * 0.5)),
        win(4.5, 14, 2.5, 2.5),
        Part("dot", poly([(8.2, 13.5), (9.6, 13.8), (9, 17.5), (7.6, 17.2)], closed=True)),
        solid(rect(16, 9.5, 5, 3, 0.6)),
        line(seg(18.5, 12.5, 19.5, 21)),
    ]


@icon("chateau", CAT, "French country house with a steep roof and a conical turret at each corner",
      tags=["castle house", "french manor", "mansion", "estate", "turret", "country house", "luxury home"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 11), (5, 4), (7, 11), (12, 7), (17, 11), (19, 4), (21, 11), (21, 21)], closed=True, r=S.r * 0.5)),
        detail(seg(7, 11, 7, 21)), detail(seg(17, 11, 17, 21)),
        win(4, 14, 2, 2), win(18, 14, 2, 2),
        arch_door(10, 14, 14),
    ]


@icon("tenement-building", CAT, "Tall narrow apartment block with a zigzag fire escape down its front",
      tags=["walk-up", "fire escape", "brick apartment", "rowhouse flats", "old apartment block", "inner city housing"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 18.5, S.R)),
        win(6.5, 5.5), win(6.5, 10), win(6.5, 14.5),
        detail(poly([(12, 5.5), (17.5, 5.5), (12, 11), (17.5, 11), (12, 16.5), (17.5, 16.5)])),
    ]


def _cloud():
    parts = [P(circle(7, 11.5, 3.5)), P(circle(12, 8.5, 4.5)), P(circle(17, 11.5, 3.5)), P(rect(7, 11.5, 10, 3.5))]
    return path_to_d(U(*parts))


@icon("dream-home", CAT, "House inside a thought cloud with two small bubbles trailing below",
      tags=["dream house", "wish list", "ideal home", "imagine", "goal", "future home", "thought bubble"],
      aliases=["dream-house"])
def _(S):
    ph = poly([(9, 13), (9, 10.5), (12, 8), (15, 10.5), (15, 13)], closed=True, r=S.r * 0.4)
    return [
        shell(_cloud()),
        Part("dot", ph),
        dot(8, 18.5, 1.6), dot(5, 21, 1.1),
    ]


@icon("garden-office", CAT, "Small flat-roofed garden cabin with a desk and chair visible inside",
      tags=["home office", "backyard office", "garden room", "cabin", "studio shed", "remote work", "outbuilding"])
def _(S):
    return [
        shell(rect(4, 7, 16, 14, S.R)),
        solid(rect(2, 4.5, 20, 3, 1)),
        detail(seg(6.5, 15, 13, 15)), detail(seg(8, 15, 8, 20)),
        detail(poly([(16.5, 11.5), (16.5, 16.5), (18.5, 16.5)])),
    ]


@icon("vacant-lot", CAT, "Empty plot between two building walls with grass tufts and a blank sign on a post",
      tags=["empty lot", "land", "undeveloped", "plot", "parcel", "building site", "for sale land", "infill lot"],
      aliases=["empty-lot"])
def _(S):
    return [
        line(poly([(3, 4), (4.5, 4), (4.5, 21)])), line(poly([(21, 4), (19.5, 4), (19.5, 21)])),
        line(seg(12, 21, 12, 10)),
        shell(rect(8, 3.5, 8, 6.5, min(S.R, 2))),
        line("M8 21v-2l-1.5-2.5M8 19l1.5-2.5"), line("M16 21v-2l-1.5-2.5M16 19l1.5-2.5"),
    ]


@icon("vacant-storefront", CAT, "Shopfront with a taped-over window and a blank sign above the door",
      tags=["empty shop", "closed store", "retail space for lease", "commercial vacancy", "boarded shop", "unit to let"],
      aliases=["empty-storefront"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(rect(13, 5.5, 5.5, 3, 0.5)),
        detail(rect(5.5, 11, 6, 7.5, 0.5)), detail(seg(5.5, 11, 11.5, 18.5)),
        door(S, 14, 18, 13.5),
    ]


@icon("housing-development", CAT, "Tower crane beside a row of half-built house frames",
      tags=["construction site", "new homes", "subdivision", "estate", "builder", "under construction", "residential build"],
      aliases=["new-build-estate"])
def _(S):
    return [
        line(poly([(3, 21), (3, 14.5), (5.5, 12), (8, 14.5), (8, 21)], r=S.r)), line(seg(3, 17.5, 8, 17.5)),
        line(poly([(11, 21), (11, 14.5), (13.5, 12), (16, 14.5), (16, 21)], r=S.r)), line(seg(11, 17.5, 16, 17.5)),
        line(seg(20, 21, 20, 5)), line(poly([(10, 5), (22, 5)])),
        line(seg(12, 5, 12, 8)), dot(12, 9, 1.2),
        solid(rect(18, 2, 4, 3)),
    ]


@icon("real-estate-office", CAT, "Shopfront whose window shows a grid of small house cards",
      tags=["estate agent", "property agency", "realtor office", "listings window", "letting agent", "brokerage", "agency"],
      aliases=["estate-agency"])
def _(S):
    def card(x, y):
        return Part("dot", poly([(x, y + 4), (x, y + 2), (x + 2.2, y), (x + 4.4, y + 2), (x + 4.4, y + 4)], closed=True))
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(3, 8, 21, 8)),
        card(6.5, 10.5), card(13, 10.5), card(6.5, 15.5), card(13, 15.5),
    ]


@icon("barn-conversion", CAT, "Gambrel-roof barn turned into a home, with a glazed front and a chimney",
      tags=["converted barn", "rural home", "farm building", "rustic house", "countryside property", "renovation"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 12), (5.5, 7.5), (12, 3.5), (14.5, 4.9), (14.5, 2.5), (17.5, 2.5), (17.5, 6.5),
                    (18.5, 7.5), (21, 12), (21, 21)], closed=True, r=S.r * 0.6)),
        win(11, 7, 2, 2),
        detail(poly([(6.5, 21), (6.5, 12), (17.5, 12), (17.5, 21)])), detail(seg(12, 12, 12, 21)),
    ]


@icon("machiya-townhouse", CAT, "Narrow Japanese wooden townhouse with a lattice window and a small tiled roof over the ground floor",
      tags=["kyoto townhouse", "japanese house", "wooden townhouse", "lattice facade", "traditional japanese", "narrow house"])
def _(S):
    return [
        shell(poly([(5, 21), (5, 8.5), (12, 3.5), (19, 8.5), (19, 21)], closed=True, r=S.r)),
        detail(rect(8, 9.5, 8, 3.5)), detail(seg(12, 9.5, 12, 13)),
        solid(poly([(2, 18), (4, 14.5), (20, 14.5), (22, 18)], closed=True)),
        door(S, 9.5, 14.5, 19, 21),
    ]


def _ring():
    return path_to_d(D(P(rect(6, 6, 12, 12)), P(rect(9, 9, 6, 6))))


@icon("siheyuan", CAT, "Top view of a walled courtyard compound with a building on each side and a gate gap in one corner",
      tags=["courtyard house", "chinese courtyard", "compound", "quadrangle", "walled house", "plan view", "traditional house"],
      aliases=["courtyard-compound"])
def _(S):
    return [
        line(poly([(21, 15), (21, 3), (3, 3), (3, 21), (15, 21)], r=S.r)),
        solid(_ring()),
    ]


@icon("shophouse", CAT, "Narrow two-storey terrace building with a shop arcade below and shuttered windows above",
      tags=["terrace shop", "southeast asian shophouse", "arcade", "five foot way", "heritage shop", "arches", "row house"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        win(6.5, 5.5, 3, 5), win(14.5, 5.5, 3, 5),
        detail(seg(3, 13, 21, 13)),
        detail("M6 21v-3a3 3 0 0 1 6 0v3"), detail("M12 18a3 3 0 0 1 6 0v3"),
    ]


@icon("warehouse-loft", CAT, "Brick industrial building with tall arched windows converted into homes",
      tags=["loft apartment", "industrial conversion", "factory flat", "converted warehouse", "exposed brick", "urban loft"])
def _(S):
    return [
        shell(rect(3, 4, 18, 17, S.R)),
        detail("M5.5 18V13a2.5 2.5 0 0 1 5 0V18Z"), detail("M13.5 18V13a2.5 2.5 0 0 1 5 0V18Z"),
        detail(seg(5.5, 15.5, 10.5, 15.5)), detail(seg(13.5, 15.5, 18.5, 15.5)),
    ]


@icon("hillside-house", CAT, "House perched on a steep slope with stilts holding up the downhill side",
      tags=["sloped lot", "cliff house", "stilt home", "mountain home", "steep site", "hill home", "slope"])
def _(S):
    return [
        shell(poly([(7, 9), (7, 5.5), (12, 2.5), (17, 5.5), (17, 9)], closed=True, r=S.r)),
        win(11, 5.5, 2, 2),
        line(seg(2, 8, 21, 21.5)),
        line(seg(8.5, 9, 8.5, 12.6)), line(seg(12.5, 9, 12.5, 15.5)), line(seg(16, 9, 16, 18)),
    ]


@icon("shotgun-house", CAT, "Very narrow one-storey house with a steep front gable, a door and a window under a porch roof",
      tags=["narrow house", "new orleans house", "long house", "southern cottage", "front gable", "porch", "row cottage"])
def _(S):
    return [
        shell(poly([(7, 21), (7, 11), (12, 4), (17, 11), (17, 21)], closed=True, r=S.r)),
        dot(12, 8.5, 1.3),
        solid(poly([(4, 15), (6, 12.5), (18, 12.5), (20, 15)], closed=True)),
        door(S, 9, 12, 17), win(14, 17, 2, 2.5),
    ]


@icon("american-foursquare", CAT, "Boxy two-storey house with a hipped roof, a central dormer and a full-width porch",
      tags=["foursquare", "box house", "craftsman", "prairie box", "classic american house", "hip roof", "porch"])
def _(S):
    return [
        shell(poly([(2.5, 11), (6.5, 3.5), (17.5, 3.5), (21.5, 11)], closed=True, r=S.r)),
        win(10.5, 5.5, 3, 3),
        shell(poly([(4.5, 11), (4.5, 21), (19.5, 21), (19.5, 11)], closed=True, r=S.r)),
        win(7, 13, 2, 2), win(15, 13, 2, 2),
        detail(seg(4.5, 17.5, 19.5, 17.5)), detail(seg(7.5, 17.5, 7.5, 21)), detail(seg(16.5, 17.5, 16.5, 21)),
    ]


@icon("multi-family-home", CAT, "Two-storey house with a door on each floor, the upper one reached by an outside staircase",
      tags=["duplex", "two family", "two flat house", "upstairs downstairs", "triple decker", "outside stairs", "rental house"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 8), (9, 3.5), (15, 8), (15, 21)], closed=True, r=S.r)),
        detail(seg(3, 14, 15, 14)),
        win(5.5, 9, 2, 2.5), door(S, 10.5, 13.5, 9.5, 14), door(S, 6, 10, 16.5),
        line(poly([(21, 21), (21, 18.5), (19, 18.5), (19, 16), (17, 16), (17, 13.5)], r=S.r * 0.5)),
    ]


@icon("garage-conversion", CAT, "Garage whose big door opening is filled in with a wall and an ordinary window",
      tags=["garage to room", "converted garage", "bricked up door", "extra room", "extension", "renovation", "infill"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 9), (12, 4), (21, 9), (21, 21)], closed=True, r=S.r)),
        detail(poly([(6.5, 21), (6.5, 12.5), (17.5, 12.5), (17.5, 21)], r=S.r * 0.5)),
        win(10, 15, 4, 3),
    ]


@icon("home-extension", CAT, "House with an added side wing drawn in dashed outline",
      tags=["house extension", "add on", "annex", "side wing", "build out", "new room", "planned addition"],
      aliases=["house-extension"])
def _(S):
    return [
        shell(poly([(2, 21), (2, 10), (7, 4.5), (12, 10), (12, 21)], closed=True, r=S.r)),
        door(S, 5, 9, 15.5),
    ] + dashed([(12.5, 13), (21, 13), (21, 21), (12.5, 21)], line, on=3, off=3)


@icon("door-swing-symbol", CAT, "Floor plan door symbol: a gap in a thick wall with a door leaf and a quarter-circle swing arc",
      tags=["door plan", "floor plan symbol", "door swing", "architectural symbol", "blueprint door", "swing arc", "door opening"])
def _(S):
    return [
        solid(rect(2, 16, 5, 3)), solid(rect(17, 16, 5, 3)),
        line(seg(7, 17.5, 7, 7.5)),
        line("M7 7.5A10 10 0 0 1 17 17.5"),
    ]


@icon("window-plan-symbol", CAT, "Floor plan window symbol: a thick wall broken by a thin glazed opening",
      tags=["window plan", "floor plan symbol", "architectural symbol", "blueprint window", "glazing", "wall opening"])
def _(S):
    return [
        solid(rect(2, 8, 6, 8, L(S, 0, 1.5))), solid(rect(16, 8, 6, 8, L(S, 0, 1.5))),
        line(seg(8, 10, 16, 10)), line(seg(8, 14, 16, 14)),
    ]


@icon("stairs-plan-symbol", CAT, "Floor plan stair symbol: a rectangle of tread lines with an up arrow through the middle",
      tags=["stair plan", "staircase plan", "floor plan symbol", "blueprint stairs", "steps up", "architectural symbol"])
def _(S):
    return [
        shell(rect(4, 3, 16, 18, S.R)),
        detail(seg(4, 9, 20, 9)), detail(seg(4, 13, 20, 13)), detail(seg(4, 17, 20, 17)),
        detail(seg(12, 19, 12, 6.5)),
        detail(poly([(9.5, 9), (12, 6.5), (14.5, 9)])),
    ]


@icon("isometric-floor-plan", CAT, "Isometric view of a roofless floor plan with raised walls dividing it into three rooms",
      tags=["3d floor plan", "isometric plan", "cutaway", "room layout", "apartment plan", "axonometric", "layout"])
def _(S):
    return [
        shell(poly([(12, 10), (21, 14.5), (12, 19), (3, 14.5)], closed=True, r=S.r * 0.5)),
        line(poly([(3, 14.5), (3, 9.5), (12, 5), (21, 9.5), (21, 14.5)], r=S.r * 0.5)),
        line(seg(12, 10, 12, 5)),
        detail(seg(16.5, 12.25, 7.5, 16.75)), detail(seg(12, 14.5, 12, 19)),
    ]


@icon("site-plan", CAT, "Top view of a property boundary holding a house footprint and driveway, with the street along one side",
      tags=["plot plan", "lot plan", "property survey", "parcel plan", "driveway", "footprint", "boundary map"])
def _(S):
    return [
        line(rect(4, 2.5, 16, 14, S.R)),
        solid(rect(6.5, 5.5, 6, 6.5)),
        solid(rect(14.5, 10, 3, 10.5)),
        line(seg(2, 20.5, 22, 20.5)),
    ]


@icon("ceiling-height", CAT, "Room cross-section with a double-headed arrow from floor to ceiling",
      tags=["room height", "headroom", "floor to ceiling", "vertical clearance", "measure height", "interior dimension"],
      aliases=["headroom"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, S.R)),
        detail(seg(12, 6.5, 12, 17.5)),
        detail(poly([(9.5, 9), (12, 6.5), (14.5, 9)])), detail(poly([(9.5, 15), (12, 17.5), (14.5, 15)])),
    ]


@icon("corner-lot", CAT, "Top view of a plot where two streets meet at a right angle with a small house footprint",
      tags=["corner plot", "corner property", "intersection lot", "two streets", "street corner", "plot plan"])
def _(S):
    return [
        line(poly([(4, 3), (4, 20), (21, 20)], r=S.r)),
        line(rect(8, 4, 12, 12, S.R)),
        solid(rect(11, 7, 6, 6)),
    ]


@icon("flag-lot", CAT, "Top view of a flag-shaped plot: a wide rear parcel joined to the street by a long narrow strip",
      tags=["flagpole lot", "panhandle lot", "rear lot", "access strip", "driveway lot", "land parcel", "plot shape"])
def _(S):
    return [
        line(poly([(3, 3), (21, 3), (21, 13), (14, 13), (14, 20), (10, 20), (10, 13), (3, 13)], closed=True, r=S.r)),
        solid(rect(7, 6, 6, 4)),
    ]


@icon("lot-subdivision", CAT, "Top view of a plot outline split by dashed lines into four smaller parcels",
      tags=["subdivide land", "split lot", "parcels", "land division", "plat", "plot split", "survey"],
      aliases=["land-subdivision"])
def _(S):
    return [line(rect(3, 3, 18, 18, S.R))] + dashed([(12, 4), (12, 20)], line, on=3, off=3.5) + dashed([(4, 12), (20, 12)], line, on=3, off=3.5)


@icon("property-easement", CAT, "Top view of two neighbouring plots with a dashed path crossing one of them to reach the other",
      tags=["right of way", "access path", "shared path", "neighbor access", "legal access", "land rights", "easement"],
      aliases=["right-of-way"])
def _(S):
    return [
        line(rect(3, 3, 7, 18, min(S.R, 2))), line(rect(14, 3, 7, 18, min(S.R, 2))),
    ] + dashed([(6.5, 19), (6.5, 12), (16, 12)], line, on=2, off=3.5) + [dot(17.5, 12, 1.5)]


@icon("building-setback", CAT, "Top view of a plot with a dashed inner line set in from the edges and a house footprint inside it",
      tags=["setback line", "yard requirement", "zoning", "buildable area", "lot coverage", "building line", "plot plan"])
def _(S):
    return [line(rect(3, 3, 18, 18, S.R))] + dashed([(7, 7), (17, 7), (17, 17), (7, 17)], line, on=3, off=3.5, closed=True) + [solid(rect(10, 10, 4, 4))]


@icon("building-floor-level", CAT, "Building of four stacked floor bands with the third floor highlighted",
      tags=["floor number", "storey", "which floor", "level", "unit on floor", "stacked floors", "story"],
      aliases=["floor-level"])
def _(S):
    return [
        shell(rect(5, 3, 14, 18, S.R)),
        detail(seg(5, 7.5, 19, 7.5)), detail(seg(5, 12, 19, 12)), detail(seg(5, 16.5, 19, 16.5)),
        Part("dot", rect(5, 8.5, 14, 2.5)),
    ]


@icon("roof-pitch", CAT, "Roof slope triangle with an angle arc at its base",
      tags=["roof slope", "roof angle", "rise over run", "gradient", "pitch ratio", "gable angle", "incline"])
def _(S):
    return [
        shell(poly([(3, 19), (12, 5), (21, 19)], closed=True, r=S.r)),
        detail(arc(3, 19, 6.5, -57, 0)),
    ]


@icon("load-bearing-wall", CAT, "Wall section with a beam resting on top and arrows pressing down onto it",
      tags=["structural wall", "support", "beam load", "structure", "weight", "bearing", "construction"])
def _(S):
    return [
        solid(rect(2, 9, 20, 4, 1)),
        shell(rect(5, 13, 14, 8, min(S.R, 1.5))),
        detail(seg(5, 17, 19, 17)), detail(seg(12, 13, 12, 17)), detail(seg(8.5, 17, 8.5, 21)), detail(seg(15.5, 17, 15.5, 21)),
        line(seg(8, 2.5, 8, 6)), line(poly([(5.8, 4), (8, 6.2), (10.2, 4)])),
        line(seg(16, 2.5, 16, 6)), line(poly([(13.8, 4), (16, 6.2), (18.2, 4)])),
    ]


@icon("sun-orientation", CAT, "House under a dashed arc showing the sun's path, with a small sun on the arc",
      tags=["solar orientation", "sun path", "facing south", "daylight", "passive solar", "sunlight direction", "aspect"],
      aliases=["house-aspect"])
def _(S):
    return dashed(_arc_pts(12, 19, 10, 200, 340), line, on=2.5, off=3.5) + [
        shell(poly([(7, 21), (7, 17), (12, 13.5), (17, 17), (17, 21)], closed=True, r=S.r)),
        solid(circle(5.9, 11.1, 2.3)),
    ]


@icon("kitchen-work-triangle", CAT, "Plan of a fridge, hob and sink placed around a kitchen with a dashed triangle linking them",
      tags=["work triangle", "kitchen layout", "kitchen design", "sink hob fridge", "ergonomic kitchen", "cooking zone"],
      aliases=["golden-triangle-kitchen"])
def _(S):
    return dashed([(5.5, 5.5), (18.5, 5.5), (12, 18)], line, on=3, off=2.5, closed=True) + [
        solid(rect(3, 3, 5, 5, L(S, 0, 1.2))),
        solid(circle(18.5, 5.5, 2.6)),
        solid(rect(9, 16, 6, 4.5, L(S, 0, 2))),
    ]


@icon("galley-kitchen", CAT, "Floor plan of two long parallel counters with a walkway between, a sink on one and a hob on the other",
      tags=["corridor kitchen", "kitchen layout", "parallel counters", "narrow kitchen", "kitchen plan", "walk-through"])
def _(S):
    return [
        shell(rect(2.5, 3, 7, 18, min(S.R, 3))), shell(rect(14.5, 3, 7, 18, min(S.R, 3))),
        win(4.5, 6, 3, 5, ), dot(17, 7, 1.2), dot(17, 11, 1.2),
    ]


@icon("jack-and-jill-bathroom", CAT, "Floor plan of a bathroom between two bedrooms with a door into it from each side",
      tags=["shared bathroom", "connecting bathroom", "two bedroom bath", "bath between bedrooms", "kids bathroom", "floor plan"],
      aliases=["jack-jill-bath"])
def _(S):
    return [
        line(rect(3, 3, 18, 18, S.R)),
        detail(seg(8.5, 3, 8.5, 8)), detail(seg(8.5, 12, 8.5, 21)),
        detail(seg(15.5, 3, 15.5, 12)), detail(seg(15.5, 16, 15.5, 21)),
        Part("dot", rect(10.8, 4.5, 2.4, 5, 1)),
    ]


@icon("en-suite-bathroom", CAT, "Floor plan of a bedroom with a bed and a connected bathroom with a tub behind an internal door",
      tags=["ensuite", "master bath", "attached bathroom", "bedroom bathroom", "private bath", "suite", "floor plan"],
      aliases=["ensuite"])
def _(S):
    return [
        line(rect(3, 3, 18, 18, S.R)),
        detail(seg(14, 3, 14, 11)), detail(seg(14, 15, 14, 21)),
        Part("dot", rect(5.5, 6.5, 5.5, 10.5, 1)),
        Part("dot", rect(16.5, 5.5, 2.5, 7, 1.2)),
    ]


@icon("guest-room", CAT, "Made single bed with a folded towel on it and a small suitcase at its foot",
      tags=["spare room", "guest bedroom", "visitor", "spare bed", "overnight stay", "hospitality", "bedroom"])
def _(S):
    return [
        line(seg(3, 7, 3, 20)),
        shell(rect(3, 12.5, 12, 4.5, min(S.R, 2))),
        line(seg(14, 17, 14, 20)),
        solid(rect(5.5, 9, 5.5, 2.5, 0.8)),
        shell(rect(17.5, 12, 3.5, 8, min(S.R, 1.5))),
    ]


@icon("mudroom", CAT, "Wall bench with boots underneath and coats hanging on hooks above",
      tags=["entryway", "boot room", "coat hooks", "entry bench", "hallway storage", "cloakroom", "foyer"],
      aliases=["boot-room"])
def _(S):
    return [
        line(seg(3, 3, 21, 3)),
        shell(poly([(4.5, 5), (9, 5), (10, 11), (3.5, 11)], closed=True, r=S.r)),
        shell(poly([(15, 5), (19.5, 5), (20.5, 11), (14, 11)], closed=True, r=S.r)),
        shell(rect(3, 14, 18, 3, 1)),
        line(seg(4.5, 17, 4.5, 21)), line(seg(19.5, 17, 19.5, 21)),
        solid(poly([(8, 18), (10, 18), (10, 19.5), (12, 20), (12, 21), (8, 21)], closed=True)),
        solid(poly([(13, 18), (15, 18), (15, 19.5), (17, 20), (17, 21), (13, 21)], closed=True)),
    ]


@icon("utility-room", CAT, "Tall water heater tank beside a furnace cabinet with a duct rising from its top",
      tags=["laundry room", "boiler room", "mechanical room", "furnace", "hot water tank", "plant room", "hvac"],
      aliases=["plant-room"])
def _(S):
    return [
        shell(rect(3, 7, 7, 14, S.R)),
        line(seg(6.5, 7, 6.5, 3)),
        dot(6.5, 12, 1.2), detail(seg(3, 17, 10, 17)),
        shell(rect(13, 12, 8, 9, min(S.R, 2))),
        line(seg(17, 12, 17, 4)),
        dot(17, 16.5, 1.2),
    ]


@icon("half-bathroom", CAT, "Toilet next to a small pedestal sink with no bath or shower",
      tags=["powder room", "guest toilet", "cloakroom", "wc", "washroom", "half bath", "lavatory"],
      aliases=["powder-room"])
def _(S):
    return [
        shell(rect(3, 3, 5, 7, min(S.R, 1.5))),
        shell(poly([(3, 12.5), (11, 12.5), (10.5, 16.5), (8.5, 18), (8.5, 21), (4.5, 21), (4.5, 18), (3, 16.5)], closed=True, r=S.r)),
        shell(poly([(15, 11), (21, 11), (20, 14.5), (16, 14.5)], closed=True, r=S.r)),
        shell(poly([(17, 14.5), (19.5, 14.5), (20, 21), (16.5, 21)], closed=True, r=S.r * 0.5)),
        line(poly([(18, 11), (18, 8.5), (20, 8.5)], r=S.r * 0.5)),
    ]


@icon("kitchenette", CAT, "Short counter with a two-burner hob, a small sink and a mini fridge underneath",
      tags=["small kitchen", "compact kitchen", "studio kitchen", "mini kitchen", "kitchen unit", "office kitchen", "efficiency"],
      aliases=["mini-kitchen"])
def _(S):
    return [
        shell(rect(3, 11, 18, 10, S.R)),
        detail(seg(10.5, 11, 10.5, 21)),
        detail(rect(12.5, 14, 6, 5.5, 0.5)),
        line(poly([(5.5, 11), (5.5, 7), (8.5, 7)], r=S.r * 0.5)),
        solid(ellipse(14, 9, 2, 1)), solid(ellipse(19, 9, 1.8, 1)),
    ]


def rot(pts, deg, cx, cy):
    """Rotate points clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


@icon("breakfast-nook", CAT, "Built-in bench seat under a window with a small pedestal table in front",
      tags=["dining nook", "banquette", "window seat", "kitchen corner", "booth seating", "small dining area", "eating area"],
      aliases=["dining-nook"])
def _(S):
    return [
        shell(rect(5, 3, 14, 7, min(S.R, 2))), detail(seg(12, 3, 12, 10)),
        shell(rect(3, 14, 10, 7, min(S.R, 3))),
        solid(rect(15, 15, 7, 2, 1)), line(seg(18.5, 17, 18.5, 21)),
    ]


@icon("linen-closet", CAT, "Open cupboard door revealing shelves of folded towels and sheets",
      tags=["airing cupboard", "towel storage", "bedding storage", "hall closet", "shelves", "storage cupboard", "bathroom storage"],
      aliases=["airing-cupboard"])
def _(S):
    return [
        shell(rect(3, 3, 14, 18, min(S.R, 2))),
        detail(seg(3, 9, 17, 9)), detail(seg(3, 15, 17, 15)),
        Part("dot", rect(5, 5.5, 7, 3, 0.8)), Part("dot", rect(5, 11.5, 9, 3, 0.8)), Part("dot", rect(5, 17.5, 8, 2.5, 0.8)),
        shell(poly([(17, 3), (21, 5), (21, 19), (17, 21)], closed=True, r=S.r * 0.5)),
    ]


@icon("safe-room", CAT, "House outline with a heavy vault door and round wheel handle inside it",
      tags=["panic room", "storm shelter", "secure room", "vault door", "shelter", "bunker", "tornado room"],
      aliases=["panic-room"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 10), (12, 3), (21, 10), (21, 21)], closed=True, r=S.r)),
        detail(poly([(7, 21), (7, 11.5), (17, 11.5), (17, 21)], r=S.r * 0.5)),
        detail(circle(12, 16.5, 2.5)), dot(12, 16.5, 0.9),
    ]


@icon("wet-room", CAT, "Open floor with a long drain slot and a wall shower head, with no tray or curtain",
      tags=["walk-in shower", "open shower", "tiled shower", "linear drain", "level access shower", "accessible bathroom", "shower room"])
def _(S):
    return [
        line(poly([(21, 3), (15, 3), (15, 5)], r=S.r * 0.5)),
        solid(poly([(11.5, 5.5), (18.5, 5.5), (16.5, 8.5), (13.5, 8.5)], closed=True)),
        line(seg(12, 11, 12, 13.5)), line(seg(15, 12, 15, 15)), line(seg(18, 11, 18, 13.5)),
        line(seg(2, 18, 8, 18)), line(seg(16, 18, 22, 18)),
        solid(rect(9, 17, 6, 2.5, 1)),
    ]


@icon("crawl-space", CAT, "House cross-section with a low empty space under the floor and a small vent in the foundation",
      tags=["under floor", "foundation vent", "subfloor", "underfloor void", "pier and beam", "foundation", "inspection access"],
      aliases=["subfloor-void"])
def _(S):
    return [
        shell(poly([(3, 14), (3, 8), (12, 3), (21, 8), (21, 14)], closed=True, r=S.r)),
        win(10.8, 8, 2.4, 2.4),
        line(poly([(3, 14), (3, 21), (21, 21), (21, 14)], r=S.r)),
        solid(rect(6.5, 16.5, 4, 2.5, 0.5)),
    ]


@icon("indoor-pool", CAT, "Swimming pool with a ladder under a pitched glass roof frame",
      tags=["swimming pool", "heated pool", "pool house", "natatorium", "spa", "leisure centre", "lap pool"])
def _(S):
    return [
        line(poly([(3, 10), (12, 3.5), (21, 10)], r=S.r)),
        line(seg(12, 3.5, 12, 10)),
        shell(rect(4, 14, 16, 7, min(S.R, 2))),
        detail("M6.5 18q1.5-1.5 3 0t3 0"),
        line("M16 18V13.5a2 2 0 0 1 3 0V18"),
    ]


@icon("cathedral-ceiling", CAT, "Room cross-section with a tall peaked ceiling following the roof line and a pendant light",
      tags=["vaulted ceiling", "high ceiling", "pitched ceiling", "open beam", "great room", "tall room", "pendant lamp"],
      aliases=["vaulted-ceiling"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 10), (12, 3), (21, 10), (21, 21)], closed=True, r=S.r)),
        detail(seg(12, 5, 12, 10)),
        Part("dot", poly([(10, 10.5), (14, 10.5), (15.2, 13.5), (8.8, 13.5)], closed=True)),
        win(5.5, 14, 2, 4), win(16.5, 14, 2, 4),
    ]


@icon("floor-to-ceiling-windows", CAT, "Wall of full-height glass panes with a small potted plant beside it for scale",
      tags=["glass wall", "picture window", "full height glazing", "curtain wall", "panoramic window", "big windows", "light"],
      aliases=["glass-wall"])
def _(S):
    return [
        shell(rect(3, 3, 13, 18, S.R)),
        detail(seg(7.5, 3, 7.5, 21)), detail(seg(11.5, 3, 11.5, 21)),
        solid(poly([(18.5, 17.5), (22, 17.5), (21.2, 21), (19.3, 21)], closed=True)),
        line(seg(20.2, 17.5, 20.2, 12)), line("M20.2 14.5q-2-.5-2.5-2.8"), line("M20.2 12.5q2-.5 2-2.8"),
    ]


@icon("sunken-living-room", CAT, "Section view of a sofa set in a lowered floor area with two steps leading down",
      tags=["conversation pit", "step down lounge", "lowered floor", "split level lounge", "sofa", "retro lounge", "pit"],
      aliases=["conversation-pit"])
def _(S):
    return [
        line(poly([(2, 8), (4, 8), (4, 13), (7, 13), (7, 18), (22, 18)], r=S.r * 0.5)),
        shell(poly([(11, 17), (11, 13), (13, 13), (13, 10), (19, 10), (19, 13), (21, 13), (21, 17)], closed=True, r=S.r * 0.5)),
    ]


@icon("clerestory-window", CAT, "House cross-section with a raised roof section holding a strip of small windows high up",
      tags=["high window", "roof lantern", "raised roof", "daylighting", "light strip", "upper windows", "natural light"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 13), (8, 9.5), (8, 5.5), (12, 3), (16, 5.5), (16, 9.5), (21, 13), (21, 21)], closed=True, r=S.r)),
        win(9.5, 6.8, 2, 2.4), win(12.5, 6.8, 2, 2.4),
        door(S, 10.5, 13.5, 15),
    ]


@icon("door-canopy", CAT, "Front door with a small pitched hood roof above it on two supports",
      tags=["porch roof", "entrance canopy", "door hood", "awning", "front entrance", "door cover", "porch"],
      aliases=["porch-canopy"])
def _(S):
    return [
        shell(poly([(4, 10), (8, 5), (16, 5), (20, 10)], closed=True, r=S.r)),
        line(seg(5.5, 10, 5.5, 21)), line(seg(18.5, 10, 18.5, 21)),
        shell(rect(9, 14, 6, 7, min(S.R, 2))),
    ]


@icon("sidelight-entry-door", CAT, "Front door flanked by a narrow vertical glass panel on each side",
      tags=["door with side windows", "entry door glass", "sidelites", "front door", "entrance door", "glazed panels", "entryway"],
      aliases=["sidelite-door"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, S.R)),
        detail(poly([(8.5, 21), (8.5, 5.5), (15.5, 5.5), (15.5, 21)])),
        win(4.3, 7, 2.5, 12), win(17.2, 7, 2.5, 12),
        dot(13, 14, 1),
    ]


@icon("sold-property-sign", CAT, "Hanging real estate sign on a post arm with a diagonal band across the panel",
      tags=["sold sign", "yard sign", "sale agreed", "property sold", "estate agent board", "just sold", "closed sale"],
      aliases=["sold-sign"])
def _(S):
    return [
        line(poly([(4, 21), (4, 3), (18, 3)], r=S.r)),
        line(seg(8, 3, 8, 7)), line(seg(16, 3, 16, 7)),
        shell(rect(6, 7, 13, 10, min(S.R, 2))),
        detail(seg(8, 15.5, 17, 8.5)),
    ]


@icon("for-rent-sign", CAT, "Hanging sign panel on a post arm with a key on its face",
      tags=["to let sign", "rental sign", "property for rent", "letting board", "available to rent", "lease sign", "key sign"],
      aliases=["to-let-sign"])
def _(S):
    return [
        line(poly([(4, 21), (4, 3), (18, 3)], r=S.r)),
        line(seg(8, 3, 8, 6)), line(seg(16, 3, 16, 6)),
        shell(rect(6, 6, 14, 11.5, min(S.R, 2))),
        detail(circle(10.5, 11.7, 1.6)), detail(seg(12, 11.7, 17, 11.7)), detail(seg(15.5, 11.7, 15.5, 14)),
    ]


@icon("price-reduced-home", CAT, "House with a price tag hanging from its roof and a downward arrow on the tag",
      tags=["price drop", "price cut", "reduced price", "discount home", "lower price", "bargain", "markdown"],
      aliases=["price-drop-home"])
def _(S):
    return [
        shell(poly([(2, 21), (2, 11), (7.5, 5.5), (13, 11), (13, 21)], closed=True, r=S.r)),
        door(S, 5.5, 9.5, 15.5),
        line(poly([(18.5, 10), (18.5, 7.5), (10.5, 7.5)], r=S.r * 0.5)),
        shell(poly([(16, 10), (21, 10), (21, 18), (18.5, 20.5), (16, 18)], closed=True, r=S.r * 0.5)),
        detail(seg(18.5, 12.5, 18.5, 16.5)), detail(poly([(17, 15), (18.5, 16.5), (20, 15)])),
    ]


@icon("property-auction", CAT, "Auction gavel striking its block beside a small house",
      tags=["house auction", "bidding", "gavel", "auctioneer", "foreclosure sale", "hammer", "going once"],
      aliases=["house-auction"])
def _(S):
    head = rot([(11, 7.75), (19, 7.75), (19, 12.25), (11, 12.25)], 45, 15, 10)
    return [
        shell(poly([(2, 21), (2, 15), (5, 12), (8, 15), (8, 21)], closed=True, r=S.r * 0.5)),
        shell(poly(head, closed=True, r=S.r * 0.5)),
        line(poly(rot([(15, 8), (15, 2.5)], 45, 15, 10))),
        shell(rect(11, 17.5, 10, 3.5, min(S.R, 1.5))),
    ]


@icon("property-deal", CAT, "Handshake beneath a house roof outline",
      tags=["agreement", "sale closed", "buyer and seller", "contract", "handshake", "closing", "real estate deal"],
      aliases=["house-handshake"])
def _(S):
    return [
        line(poly([(3, 9), (12, 3), (21, 9)], r=S.r)),
        shell(rect(2.5, 13, 3.5, 7, min(S.R, 1.5))), shell(rect(18, 13, 3.5, 7, min(S.R, 1.5))),
        shell(poly([(6.5, 14), (10, 12.5), (14, 12.5), (17.5, 14), (17.5, 18), (14, 19.5), (10, 19.5), (6.5, 18)], closed=True, r=S.r)),
        detail(seg(10.5, 15.5, 13.5, 17.5)),
    ]


@icon("compare-homes", CAT, "Balance scale with a small house resting on each pan",
      tags=["house comparison", "weigh options", "home value comparison", "side by side", "trade off", "compare listings", "balance"],
      aliases=["compare-listings"])
def _(S):
    def hs_(cx):
        return solid(poly([(cx - 2.3, 14.5), (cx - 2.3, 11), (cx, 8.5), (cx + 2.3, 11), (cx + 2.3, 14.5)], closed=True))
    return [
        line(seg(4, 4, 20, 4)), line(seg(12, 4, 12, 19)), line(seg(8, 20, 16, 20)),
        line(poly([(2.5, 16), (5, 4), (7.5, 16)], r=S.r * 0.3)), line(seg(2, 16, 8, 16)),
        line(poly([(16.5, 16), (19, 4), (21.5, 16)], r=S.r * 0.3)), line(seg(16, 16, 22, 16)),
        hs_(5), hs_(19),
    ]


@icon("aerial-property-photo", CAT, "Quadcopter drone with a camera hovering above a house roof",
      tags=["drone photography", "aerial view", "roof photo", "drone shot", "uav", "listing photos", "bird's eye"],
      aliases=["drone-listing"])
def _(S):
    return [
        line(seg(4.5, 5.5, 19.5, 5.5)),
        line(seg(2.5, 3.2, 6.5, 3.2)), line(seg(4.5, 3.2, 4.5, 5.5)),
        line(seg(17.5, 3.2, 21.5, 3.2)), line(seg(19.5, 3.2, 19.5, 5.5)),
        shell(rect(9.5, 3.5, 5, 4, min(S.R, 1.5))), dot(12, 9.6, 1.2),
        shell(poly([(4, 21), (4, 17), (12, 12.8), (20, 17), (20, 21)], closed=True, r=S.r)),
    ]


@icon("real-estate-photography", CAT, "Camera whose rear screen shows a small house",
      tags=["listing photos", "property photos", "photographer", "camera", "house picture", "virtual tour", "photo shoot"],
      aliases=["listing-photography"])
def _(S):
    return [
        shell(rect(3, 6, 18, 14, S.R)),
        line(poly([(9, 6), (10, 3.5), (14, 3.5), (15, 6)], r=S.r * 0.4)),
        detail(rect(5.5, 8.5, 13, 9, 1)),
        Part("dot", poly([(9.5, 15), (9.5, 12.5), (12, 10.5), (14.5, 12.5), (14.5, 15)], closed=True)),
    ]


@icon("property-location-pin", CAT, "Map pin with a house shape in its round head",
      tags=["map marker", "address", "home location", "listing location", "where", "gps", "house pin"],
      aliases=["house-pin"])
def _(S):
    tip = ("M12 21.5C7.5 16 5 13 5 9.5a7 7 0 0 1 14 0c0 3.5-2.5 6.5-7 12Z" if S.name == "line" else
           "M10.9 20.3C7.3 16 5 13 5 9.5a7 7 0 0 1 14 0c0 3.5-2.3 6.5-5.9 10.8a1.6 1.6 0 0 1-2.2 0Z")
    return [
        shell(tip),
        Part("dot", poly([(9, 12), (9, 9.7), (12, 7), (15, 9.7), (15, 12)], closed=True)),
    ]


@icon("flyer-box", CAT, "Clear brochure box fixed to a sign post with a stack of folded flyers inside",
      tags=["brochure holder", "info box", "leaflet box", "take one", "flyer holder", "listing sheets", "yard sign box"],
      aliases=["brochure-box"])
def _(S):
    return [
        line(seg(5, 21, 5, 3)), line(seg(5, 10, 8, 10)),
        shell(rect(8, 5, 13, 12, min(S.R, 2))),
        Part("dot", rect(10.5, 8, 3, 6, 0.5)), Part("dot", rect(15, 8, 3, 6, 0.5)),
    ]


@icon("housewarming-party", CAT, "House with confetti and streamers bursting above its roof",
      tags=["new home celebration", "moving in party", "celebrate", "confetti", "open house party", "party", "new house"],
      aliases=["house-party"])
def _(S):
    return [
        shell(poly([(5, 21), (5, 14), (12, 9), (19, 14), (19, 21)], closed=True, r=S.r)),
        door(S, 10, 14, 17),
        line("M8.5 7.5q-2-2.5 0-5"), line("M15.5 7.5q2-2.5 0-5"),
        dot(12, 3.5, 1.1), dot(4.5, 6, 1.1), dot(19.5, 6, 1.1), dot(3.5, 10.5, 0.9), dot(20.5, 10.5, 0.9),
    ]


@icon("loft-conversion", CAT, "House cross-section with a bed in the attic under a new roof dormer",
      tags=["attic conversion", "attic bedroom", "dormer", "roof room", "loft room", "extra bedroom", "top floor extension"],
      aliases=["attic-conversion"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 12), (12, 4), (15, 6.7), (15, 4.5), (19, 4.5), (19, 10.1), (21, 12), (21, 21)], closed=True, r=S.r * 0.6)),
        detail(seg(3, 14.5, 21, 14.5)),
        Part("dot", rect(7.5, 11.5, 6.5, 2, 0.6)), Part("dot", rect(7.5, 9.8, 1.8, 3.7, 0.6)),
        win(16, 6.5, 2, 3),
        win(6, 17, 3, 2.5), door(S, 14, 17.5, 17),
    ]
