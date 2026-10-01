"""TypeIcon Core: architecture (batch 002).

Sacred buildings, monuments, fortifications, classical elements, roof types and street furniture,
drawn front-on on the ground line y = 21 (outer edge 22) in the language of sets/buildings.py and
sets/architecture_001.py: closed walls are shells, doors and trim are details, and small window
blocks (`win`) are knocked out of Filled walls.
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


def door(S, x0, x1, top, ground=21.0):
    """Square-headed door outline standing on the ground line."""
    return detail(poly([(x0, ground), (x0, top), (x1, top), (x1, ground)], r=S.r * 0.5))


def arch_door(x0, x1, top, ground=21.0):
    """Round-headed door; `top` is the crown of the arch."""
    r = (x1 - x0) / 2
    return detail(f"M{fmt(x0)} {fmt(ground)}V{fmt(top + r)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x1)} {fmt(top + r)}V{fmt(ground)}")


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def onion(cx, yb, a, h):
    """Onion dome: base half-width a at y = yb, swelling out and tapering to a tip h above the base."""
    yt = yb - h
    return (f"M{fmt(cx - a)} {fmt(yb)}C{fmt(cx - a * 1.9)} {fmt(yb - h * 0.45)} {fmt(cx - a * 0.2)} {fmt(yt + h * 0.35)} "
            f"{fmt(cx)} {fmt(yt)}C{fmt(cx + a * 0.2)} {fmt(yt + h * 0.35)} {fmt(cx + a * 1.9)} {fmt(yb - h * 0.45)} "
            f"{fmt(cx + a)} {fmt(yb)}Z")


def cross_line(x, y0, y1, arm=1.5, ya=None):
    """Small cross drawn with open strokes (upright from y0 to y1, arm at ya)."""
    ya = y0 + (y1 - y0) * 0.35 if ya is None else ya
    return [line(seg(x, y0, x, y1)), line(seg(x - arm, ya, x + arm, ya))]


def bell(cx, top, w, h):
    """Small church bell outline with a flared lip (closed)."""
    x0, x1 = cx - w / 2, cx + w / 2
    return (f"M{fmt(x0)} {fmt(top + h)}C{fmt(x0 + w * 0.2)} {fmt(top + h * 0.75)} {fmt(x0 + w * 0.15)} {fmt(top)} {fmt(cx)} {fmt(top)}"
            f"C{fmt(x1 - w * 0.15)} {fmt(top)} {fmt(x1 - w * 0.2)} {fmt(top + h * 0.75)} {fmt(x1)} {fmt(top + h)}Z")


# ============================================================================ sacred buildings

@icon("shinto-shrine", CAT, "Small wooden shrine under a thick sweeping roof with crossed beams at the ridge ends",
      tags=["shinto", "jinja", "japanese shrine", "kami", "shrine", "japan"])
def _(S):
    return [
        line(poly([(5, 3), (7.5, 8), (10, 3)])),
        line(poly([(14, 3), (16.5, 8), (19, 3)])),
        shell("M2 12.5Q5.5 12.5 7 8H17Q18.5 12.5 22 12.5Z"),
        shell(rect(5, 15, 14, 6, min(S.R, 1.5))),
        detail(seg(12, 15, 12, 21)),
    ]


@icon("wayside-shrine", CAT, "Small roofed box on a post with a candle in its niche",
      tags=["roadside shrine", "wayside cross", "chapel", "devotion", "candle", "pilgrimage"],
      aliases=["roadside-shrine"])
def _(S):
    return [
        shell(poly([(5, 8.5), (12, 3), (19, 8.5)], closed=True, r=S.r * 0.5)),
        shell(rect(6.5, 11, 11, 7, min(S.R, 2))),
        mark(rect(11, 14, 2, 2.5)),
        mark("M12 11.4C12.9 12.1 12.9 12.9 12 13.1C11.1 12.9 11.1 12.1 12 11.4Z"),
        line(seg(12, 18, 12, 21)),
        line(seg(9, 21, 15, 21)),
    ]


@icon("orthodox-church", CAT, "Church with a cluster of onion domes each topped with a small cross",
      tags=["orthodox", "russian church", "cathedral", "onion dome", "eastern orthodox", "christian"])
def _(S):
    return [
        *cross_line(12, 1.5, 5),
        shell(onion(12, 10.5, 2.25, 5)),
        shell(rect(9.5, 10.5, 5, 4, 0)),
        *cross_line(5, 6.5, 9.5, arm=1.25),
        shell(onion(5, 14.5, 1.75, 4.5)),
        *cross_line(19, 6.5, 9.5, arm=1.25),
        shell(onion(19, 14.5, 1.75, 4.5)),
        shell(rect(3, 14.5, 18, 6.5, min(S.R, 1.5))),
        arch_door(10, 14, 16.5),
    ]


@icon("stave-church", CAT, "Tall wooden church with stacked steep roofs and dragon heads on the gable ends",
      tags=["stave church", "norway", "wooden church", "medieval", "scandinavian", "viking"])
def _(S):
    pts = [(5, 21), (5, 16.5), (2.5, 16.5), (7, 12), (6, 12), (9.5, 8), (8.5, 8), (12, 2.5),
           (15.5, 8), (14.5, 8), (18, 12), (17, 12), (21.5, 16.5), (19, 16.5), (19, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
        line("M2.5 16.5Q1.5 15.5 2 14"), line("M21.5 16.5Q22.5 15.5 22 14"),
        arch_door(10, 14, 16.5),
    ]


@icon("mission-church", CAT, "Adobe church with a curved scalloped gable pierced by an open bell arch",
      tags=["mission", "adobe church", "spanish mission", "mission revival", "chapel", "southwest"])
def _(S):
    body = ("M3 21V12H6C7.5 12 7.5 9.5 8 8.5V6.5A4 4 0 0 1 16 6.5V8.5C16.5 9.5 16.5 12 18 12H21V21Z")
    return [
        shell(body),
        detail("M10 11V7.5A2 2 0 0 1 14 7.5V11Z"),
        arch_door(10, 14, 15),
    ]


@icon("thai-temple", CAT, "Temple with layered steep roofs whose gable ends curl up into slender horns",
      tags=["wat", "thai temple", "buddhist temple", "thailand", "ubosot", "chofa"], aliases=["wat"])
def _(S):
    return [
        line("M12 5.5Q12 3 13.5 2"),
        shell(poly([(4, 14), (12, 5.5), (20, 14)], closed=True, r=S.r * 0.4)),
        line("M4 14L1.5 16.5Q1.5 14.5 2.5 13.5"), line("M20 14L22.5 16.5Q22.5 14.5 21.5 13.5"),
        detail(poly([(8.5, 14), (12, 10), (15.5, 14)])),
        shell(rect(5.5, 16, 13, 5, min(S.R, 1))),
        detail(seg(12, 16, 12, 21)),
    ]


@icon("ziggurat", CAT, "Three stepped terraces with a central stairway up to a small shrine on top",
      tags=["mesopotamia", "sumerian", "babylon", "ancient temple", "terraced", "ur"])
def _(S):
    pts = [(2, 21), (2, 17), (5, 17), (5, 13), (8, 13), (8, 9), (10, 9), (10, 5.5), (14, 5.5), (14, 9), (16, 9),
           (16, 13), (19, 13), (19, 17), (22, 17), (22, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.4)),
        detail(seg(10.5, 21, 11, 9)), detail(seg(13.5, 21, 13, 9)),
    ]


@icon("mausoleum", CAT, "Small stone tomb building with two columns, a triangular pediment and a heavy door",
      tags=["tomb", "crypt", "sepulchre", "memorial", "burial", "vault"], aliases=["tomb"])
def _(S):
    return [
        shell(poly([(4.5, 9), (12, 2.5), (19.5, 9)], closed=True, r=S.r * 0.4)),
        shell(rect(6, 11, 12, 7, min(S.R, 1))),
        detail(seg(8.5, 11, 8.5, 18)), detail(seg(15.5, 11, 15.5, 18)),
        mark(rect(10.5, 12.5, 3, 5.5)),
        line(seg(3.5, 20.5, 20.5, 20.5)),
    ]


@icon("cemetery", CAT, "Rounded headstone and a cross standing in a graveyard",
      tags=["graveyard", "churchyard", "burial ground", "cemetery", "funeral", "memorial"],
      aliases=["graveyard"])
def _(S):
    cross = [(15.5, 21), (15.5, 10), (12.5, 10), (12.5, 7), (15.5, 7), (15.5, 3.5), (18.5, 3.5), (18.5, 7),
             (21.5, 7), (21.5, 10), (18.5, 10), (18.5, 21)]
    return [
        shell("M2.5 21V14A4 4 0 0 1 10.5 14V21Z" if S.name == "line" else "M2.5 20V14A4 4 0 0 1 10.5 14V20A1 1 0 0 1 9.5 21H3.5A1 1 0 0 1 2.5 20Z"),
        detail(seg(5, 15.5, 8, 15.5)),
        shell(poly(cross, closed=True, r=S.r * 0.4)),
    ]


@icon("gravestone", CAT, "Single upright rounded headstone with an engraved cross and line, set in the ground",
      tags=["headstone", "tombstone", "grave", "rip", "memorial", "burial"], aliases=["headstone", "tombstone"])
def _(S):
    return [
        shell("M6 21V9A6 6 0 0 1 18 9V21Z"),
        detail(seg(12, 7, 12, 12)), detail(seg(9.5, 9, 14.5, 9)),
        detail(seg(9, 15.5, 15, 15.5)),
        line(seg(2.5, 21, 21.5, 21)),
    ]


@icon("bell-tower", CAT, "Square tower with an open belfry where a hanging bell is visible",
      tags=["belfry", "campanile", "church bell", "bell", "steeple", "chime"], aliases=["belfry", "campanile"])
def _(S):
    return [
        shell(poly([(5, 7), (12, 2.5), (19, 7)], closed=True, r=S.r * 0.4)),
        line(seg(7, 7, 7, 13.5)), line(seg(17, 7, 17, 13.5)),
        solid(bell(12, 8.5, 5, 3.5)),
        dot(12, 12.6, 0.9),
        shell(rect(6, 13.5, 12, 7.5, min(S.R, 1.5))),
        arch_door(10, 14, 16.5),
    ]


@icon("clock-tower", CAT, "Tall square tower with a large round clock face near the top and a pointed roof",
      tags=["clock", "tower clock", "town clock", "big clock", "landmark", "time"])
def _(S):
    return [
        shell(poly([(6, 21), (6, 7.5), (12, 2), (18, 7.5), (18, 21)], closed=True, r=S.r * 0.4)),
        detail(circle(12, 12, 3.25)),
        detail(poly([(12, 10.5), (12, 12), (13.5, 12)])),
        door(S, 10.5, 13.5, 17.5),
    ]


@icon("paifang", CAT, "Ornamental gateway of four columns under stacked curved tiled roofs",
      tags=["pailou", "chinese gate", "memorial arch", "chinatown gate", "archway", "gateway"],
      aliases=["pailou"])
def _(S):
    return [
        shell("M6 7Q8 7 9 3H15Q16 7 18 7Z"),
        shell("M2 11.5Q4 11.5 5 8.5H19Q20 11.5 22 11.5Z"),
        line(seg(5, 11.5, 5, 21)), line(seg(19, 11.5, 19, 21)),
        line(seg(10, 11.5, 10, 21)), line(seg(14, 11.5, 14, 21)),
        line(seg(4, 14.5, 20, 14.5)),
    ]


@icon("egyptian-temple", CAT, "Two sloping pylon towers flanking a doorway with a winged disc above it",
      tags=["egypt", "pylon", "karnak", "luxor", "ancient temple", "pharaoh"])
def _(S):
    pts = [(2.5, 21), (4.5, 4), (10, 4), (10, 8.5), (14, 8.5), (14, 4), (19.5, 4), (21.5, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.4)),
        dot(12, 11.25, 1.25),
        detail(seg(7, 11.25, 9.75, 11.25)), detail(seg(14.25, 11.25, 17, 11.25)),
        door(S, 10, 14, 15),
    ]


@icon("chhatri", CAT, "Small dome raised on four slim pillars on a square platform",
      tags=["chattri", "cenotaph", "pavilion", "rajasthan", "canopy", "indian architecture"])
def _(S):
    return [
        line(seg(12, 1.5, 12, 3.5)),
        shell("M5.5 9A6.5 6 0 0 1 18.5 9Z"),
        shell(rect(4, 9, 16, 2.5, min(S.R, 1))),
        line(seg(6, 11.5, 6, 17)), line(seg(10, 11.5, 10, 17)),
        line(seg(14, 11.5, 14, 17)), line(seg(18, 11.5, 18, 17)),
        shell(rect(3, 17, 18, 4, min(S.R, 1))),
    ]


@icon("cenotaph", CAT, "Tall rectangular stone monument on a stepped base with a wreath at its foot",
      tags=["war memorial", "memorial", "remembrance", "monument", "tribute", "veterans"])
def _(S):
    return [
        shell(poly([(7.5, 17), (8, 3), (16, 3), (16.5, 17)], closed=True, r=S.r * 0.4)),
        detail(circle(12, 12.75, 2)),
        shell(poly([(3, 21), (3, 19), (5, 19), (5, 17), (19, 17), (19, 19), (21, 19), (21, 21)], closed=True,
                   r=S.r * 0.3)),
    ]


@icon("equestrian-statue", CAT, "Rider on a rearing horse standing on a tall pedestal",
      tags=["horse statue", "statue", "monument", "rider", "general", "public art"])
def _(S):
    horse = poly([(7.5, 15.5), (7.5, 12.5), (6.5, 10.5), (8, 8.8), (12.5, 7.8), (14, 5), (15, 3.2), (18, 5),
                  (17.5, 6.2), (15.8, 6.4), (15.8, 8.2), (19, 8.4), (19, 10.6), (17.6, 10.6), (17.4, 9.8),
                  (15, 10.8), (12, 12), (10.8, 12.4), (10.8, 15.5), (9.4, 15.5), (9.2, 13.2), (8.9, 13.2),
                  (8.9, 15.5)], closed=True)
    rider = poly([(9.8, 8.4), (10.3, 5.8), (12.3, 5.8), (12.6, 8)], closed=True)
    return [
        mark(horse),
        mark(rider),
        dot(11.3, 4.1, 1.2),
        shell(rect(5.5, 17, 13, 4, L(S, 0.5, 2))),
    ]


@icon("victory-column", CAT, "Tall single column on a pedestal topped by a small winged figure",
      tags=["memorial column", "monument", "triumphal column", "statue", "landmark", "commemorative"])
def _(S):
    return [
        dot(12, 2.25, 1.25),
        solid("M11 3.75H13L13.5 6.5H10.5Z"),
        solid("M11.2 4.2L8.5 2.8L9.5 5.5Z"), solid("M12.8 4.2L15.5 2.8L14.5 5.5Z"),
        line(seg(8.5, 8, 15.5, 8)),
        shell(rect(10, 8.5, 4, 8, 0)),
        shell(rect(7.5, 16.5, 9, 4.5, min(S.R, 1))),
    ]


# ============================================================================ industry and utility

def _taper(y, y0, y1, x0, x1):
    return x0 + (x1 - x0) * (y - y0) / (y1 - y0)


@icon("oil-derrick", CAT, "Tall tapered lattice drilling tower on a small platform",
      tags=["oil rig", "drilling rig", "oil well", "petroleum", "derrick", "crude oil"])
def _(S):
    lx = lambda y: _taper(y, 21, 3.5, 5, 10.5)
    rx = lambda y: 24 - lx(y)
    parts = [
        line(poly([(lx(19), 19), (lx(3.5), 3.5), (rx(3.5), 3.5), (rx(19), 19)], r=S.r * 0.3)),
        line(seg(9.5, 2, 14.5, 2)),
        line(seg(lx(10), 10, rx(10), 10)),
        line(seg(lx(10) + 0.8, 10.8, rx(18.3) - 0.6, 18.3)), line(seg(rx(10) - 0.8, 10.8, lx(18.3) + 0.6, 18.3)),
        shell(rect(3, 19, 18, 2, L(S, 0, 1))),
    ]
    return parts


@icon("rooftop-water-tank", CAT, "Wooden barrel tank with a conical cap on a steel stand on a flat roof",
      tags=["water tank", "rooftop tank", "cistern", "water storage", "new york", "barrel tank"])
def _(S):
    return [
        shell(poly([(5.5, 7.5), (12, 2.5), (18.5, 7.5)], closed=True, r=S.r * 0.4)),
        shell(rect(6.5, 9.5, 11, 6.5, min(S.R, 1.5))),
        detail(seg(6.5, 12.75, 17.5, 12.75)),
        line(seg(8, 16, 7, 19.5)), line(seg(16, 16, 17, 19.5)), line(seg(12, 16, 12, 19.5)),
        line(seg(2, 20.5, 22, 20.5)),
    ]


@icon("grain-silo", CAT, "Tall cylindrical silo with a domed cap and a ladder running up its side",
      tags=["silo", "grain store", "farm", "agriculture", "grain bin", "storage"])
def _(S):
    parts = [
        shell("M3.5 21V8A5 5 0 0 1 13.5 8V21Z"),
        detail(seg(3.5, 11, 13.5, 11)), detail(seg(3.5, 16, 13.5, 16)),
        line(seg(16.5, 5, 16.5, 21)), line(seg(20.5, 5, 20.5, 21)),
    ]
    for y in (8.5, 12.5, 16.5):
        parts.append(line(seg(16.5, y, 20.5, y)))
    return parts


@icon("quonset-hut", CAT, "Half-cylinder metal hut with a door and two small windows on its end wall",
      tags=["nissen hut", "quonset", "military hut", "prefab", "arched shelter", "metal building"],
      aliases=["nissen-hut"])
def _(S):
    return [
        shell("M2 21A10 11 0 0 1 22 21Z"),
        detail("M5.5 14.5A7 7.5 0 0 1 18.5 14.5"),
        door(S, 10, 14, 16.5),
        win(5.5, 17, 2.5, 2), win(16, 17, 2.5, 2),
    ]


@icon("sawmill", CAT, "Open shed with a large circular saw blade and a log on the feed table",
      tags=["lumber mill", "timber mill", "saw mill", "lumber", "wood", "logging"], aliases=["lumber-mill"])
def _(S):
    teeth = []
    for i in range(9):
        a = -90 + i * 40
        teeth.append((16 + 4.7 * math.cos(math.radians(a)), 14 + 4.7 * math.sin(math.radians(a))))
        teeth.append((16 + 3.2 * math.cos(math.radians(a + 6)), 14 + 3.2 * math.sin(math.radians(a + 6))))
    return [
        shell(poly([(2, 7.5), (12, 2.5), (22, 7.5)], closed=True, r=S.r * 0.4)),
        shell(poly(teeth, closed=True)),
        dot(16, 14, 1.1),
        shell(rect(3, 12.5, 7.5, 4, 2)),
        line(seg(2.5, 18.5, 21.5, 18.5)),
        line(seg(4, 18.5, 4, 21)), line(seg(20, 18.5, 20, 21)),
    ]


@icon("radar-dome", CAT, "Large ball-shaped radome with a panel pattern on a short braced base",
      tags=["radome", "radar station", "radar", "weather radar", "air defense", "tracking station"],
      aliases=["radome"])
def _(S):
    return [
        shell(circle(12, 9.5, 7.5)),
        detail(seg(5.2, 7.5, 18.8, 7.5)), detail(seg(5.2, 11.5, 18.8, 11.5)),
        detail(poly([(6.5, 11.5), (8.5, 7.5), (10.5, 11.5), (12.5, 7.5), (14.5, 11.5), (16.5, 7.5)])),
        line(seg(8.5, 16.5, 7, 21)), line(seg(15.5, 16.5, 17, 21)),
        line(seg(7.5, 19.5, 16.5, 19.5)),
    ]


# ============================================================================ fortifications

@icon("star-fort", CAT, "Star-shaped fortress seen from above with arrowhead bastions at each corner",
      tags=["bastion fort", "trace italienne", "fortress", "citadel", "fortification", "military"],
      aliases=["bastion-fort"])
def _(S):
    pts = []
    for i in range(5):
        th = -90 + i * 72
        for rr, dth in ((5.6, -22), (7.2, -24), (10.2, 0), (7.2, 24), (5.6, 22)):
            pts.append((12 + rr * math.cos(math.radians(th + dth)), 12.3 + rr * math.sin(math.radians(th + dth))))
    return [
        shell(poly(pts, closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        detail(poly(regular(12, 12.3, 2.5, 5), closed=True, r=S.r * 0.3)),
    ]


@icon("stockade-fort", CAT, "Wall of pointed vertical logs with a square blockhouse at the corner",
      tags=["stockade", "palisade", "frontier fort", "wooden fort", "log fort", "outpost"],
      aliases=["palisade"])
def _(S):
    logs = [(2.5, 21), (2.5, 11)]
    for x in (4.25, 7.75, 11.25):
        logs += [(x, 9), (x + 1.75, 11)]
    logs[-1] = (13.5, 11)
    logs += [(13.5, 21)]
    return [
        shell(poly(logs, closed=True, r=S.r * 0.3), stroke_miterlimit="2"),
        detail(seg(6, 11, 6, 21)), detail(seg(9.5, 11, 9.5, 21)),
        shell(poly([(13.5, 4), (22, 4), (22, 9), (21, 9), (21, 21), (14.5, 21), (14.5, 9), (13.5, 9)], closed=True,
                   r=S.r * 0.3)),
        detail(seg(16.5, 6.5, 19, 6.5)),
    ]


@icon("drawbridge", CAT, "Castle gate tower with a wooden bridge lowered on chains across a moat",
      tags=["castle bridge", "moat", "castle gate", "medieval", "fortress", "lowered bridge"])
def _(S):
    return [
        shell(poly([(2.5, 21), (2.5, 3.5), (4.5, 3.5), (4.5, 5.5), (6.5, 5.5), (6.5, 3.5), (8.5, 3.5), (8.5, 21)],
                   closed=True, r=S.r * 0.3)),
        detail(seg(5.5, 9, 5.5, 12)),
        line(seg(8.5, 15.5, 21.5, 15.5)),
        line(seg(8.5, 6.5, 20.5, 15)),
        line("M10 20.5Q12 19 14 20.5T18 20.5T22 20.5"),
    ]


@icon("portcullis", CAT, "Arched gateway with a heavy iron grid gate half raised, spikes along its bottom",
      tags=["castle gate", "gate", "iron gate", "medieval", "fortress", "security"])
def _(S):
    parts = [
        line("M3.5 21V11A8.5 8.5 0 0 1 20.5 11V21"),
        line(seg(4.5, 8, 19.5, 8)), line(seg(3.5, 12, 20.5, 12)),
    ]
    for x in (8, 12, 16):
        top = 11 - math.sqrt(max(0.0, 8.5 ** 2 - (x - 12) ** 2)) + 0.5
        parts.append(line(seg(x, top, x, 14.5)))
        parts.append(solid(poly([(x - 1, 14.4), (x + 1, 14.4), (x, 16.5)], closed=True)))
    return parts


@icon("arrow-slit", CAT, "Narrow cross-shaped slit window in a stone block wall",
      tags=["arrow loop", "loophole", "castle window", "embrasure", "medieval", "fortification"],
      aliases=["loophole"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, min(S.R, 2))),
        detail(seg(3, 8, 9, 8)), detail(seg(15, 8, 21, 8)),
        detail(seg(3, 16, 9, 16)), detail(seg(15, 16, 21, 16)),
        mark(poly([(11, 5.5), (13, 5.5), (13, 10), (15.5, 10), (15.5, 12), (13, 12), (13, 18.5), (11, 18.5),
                   (11, 12), (8.5, 12), (8.5, 10), (11, 10)], closed=True)),
    ]


@icon("castle-keep", CAT, "Tall square stone tower with a crenellated top and a few small windows",
      tags=["keep", "donjon", "castle tower", "tower", "medieval", "stronghold"], aliases=["donjon"])
def _(S):
    pts = [(5.5, 21), (5.5, 3), (8, 3), (8, 5.5), (10.75, 5.5), (10.75, 3), (13.25, 3), (13.25, 5.5), (16, 5.5),
           (16, 3), (18.5, 3), (18.5, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.3)),
        win(8.5, 9, 2, 3), win(13.5, 9, 2, 3),
        arch_door(10, 14, 15.5),
    ]


@icon("column-ruins", CAT, "Row of broken columns of different heights standing on a stone base",
      tags=["ruins", "ancient ruins", "archaeology", "roman", "greek", "antiquity"], )
def _(S):
    return [
        shell(poly([(3.5, 18), (3.5, 5.5), (5.5, 4), (7.5, 6.5), (7.5, 18)], closed=True, r=S.r * 0.3)),
        shell(poly([(10, 18), (10, 12), (11.5, 13), (14, 11), (14, 18)], closed=True, r=S.r * 0.3)),
        shell(poly([(16.5, 18), (16.5, 8.5), (18.5, 10), (20.5, 8), (20.5, 18)], closed=True, r=S.r * 0.3)),
        shell(rect(2, 18, 20, 3, L(S, 0, 1.5))),
    ]


# ============================================================================ monuments and markers

@icon("triumphal-arch", CAT, "Massive rectangular monument with a large central arch and a flat top band",
      tags=["arc de triomphe", "victory arch", "memorial arch", "roman arch", "monument", "landmark"],
      aliases=["victory-arch"])
def _(S):
    return [
        shell(rect(2.5, 4, 19, 17, min(S.R, 1))),
        detail(seg(2.5, 8.5, 21.5, 8.5)),
        arch_door(8.5, 15.5, 11.5),
        detail(seg(5.5, 11.5, 5.5, 21)), detail(seg(18.5, 11.5, 18.5, 21)),
    ]


@icon("step-pyramid", CAT, "Stepped pyramid with a steep central staircase and a small temple on top",
      tags=["mayan pyramid", "aztec pyramid", "mesoamerican", "temple pyramid", "chichen itza", "teocalli"],
      aliases=["mayan-pyramid"])
def _(S):
    pts = [(2, 21), (3, 18), (4.5, 18), (5.5, 15), (7, 15), (8, 12), (9, 12), (9, 5.5), (15, 5.5), (15, 12),
           (16, 12), (17, 15), (18.5, 15), (19.5, 18), (21, 18), (22, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.3)),
        detail(poly([(10.75, 12), (10.75, 9), (13.25, 9), (13.25, 12)])),
        detail(seg(10.5, 21, 10.75, 12)), detail(seg(13.5, 21, 13.25, 12)),
    ]


@icon("cairn", CAT, "Pile of stacked rounded stones narrowing to a peak",
      tags=["stone stack", "rock pile", "trail marker", "hiking", "stacked stones", "landmark"])
def _(S):
    def stone(cx, cy, rx, ry):
        if S.name == "rounded":
            return shell(ellipse(cx, cy, rx, ry))
        pts = [(cx - rx, cy + ry * 0.2), (cx - rx * 0.75, cy - ry), (cx + rx * 0.8, cy - ry), (cx + rx, cy - ry * 0.1),
               (cx + rx * 0.8, cy + ry), (cx - rx * 0.7, cy + ry)]
        return shell(poly(pts, closed=True, r=min(rx, ry) * 0.8))
    return [
        stone(12, 18.5, 8.5, 2.5),
        stone(11.5, 13.25, 6, 2.25),
        stone(12.5, 8.25, 4.25, 2),
        stone(12, 3.75, 2.5, 1.5),
    ]


@icon("totem-pole", CAT, "Tall carved pole of stacked faces with outstretched wings at the top",
      tags=["totem", "carved pole", "pacific northwest", "first nations", "indigenous art", "wood carving"])
def _(S):
    return [
        shell(poly([(2.5, 4.5), (9, 6.5), (15, 6.5), (21.5, 4.5), (19, 9.5), (15, 9.5), (15, 21), (9, 21),
                    (9, 9.5), (5, 9.5)], closed=True, r=S.r * 0.3)),
        shell(poly([(9.5, 6.5), (9.5, 3.5), (12, 2), (14.5, 3.5), (14.5, 6.5)], closed=True, r=S.r * 0.3)),
        detail(seg(9, 15, 15, 15)),
        dot(12, 12.25, 1.1), dot(12, 18, 1.1),
    ]


# ============================================================================ columns

def _flutes(x0, x1, y0, y1, n=2):
    step = (x1 - x0) / (n + 1)
    return [detail(seg(x0 + step * (i + 1), y0, x0 + step * (i + 1), y1)) for i in range(n)]


@icon("doric-column", CAT, "Fluted column with a plain cushion capital under a square slab",
      tags=["doric", "classical column", "greek column", "pillar", "order", "architecture"])
def _(S):
    body = poly([(4.5, 3), (19.5, 3), (19.5, 5.5), (17, 5.5), (16, 8), (16, 21), (8, 21), (8, 8), (7, 5.5),
                 (4.5, 5.5)], closed=True, r=S.r * 0.3)
    return [
        shell(body),
        detail(seg(7, 5.5, 17, 5.5)),
        *_flutes(8, 16, 10, 21),
    ]


@icon("ionic-column", CAT, "Fluted column with a capital of two spiral scrolls curling outward",
      tags=["ionic", "classical column", "greek column", "volute", "pillar", "architecture"])
def _(S):
    return [
        shell(circle(5.5, 7, 2.75)),
        shell(circle(18.5, 7, 2.75)),
        dot(5.5, 7, 0.9), dot(18.5, 7, 0.9),
        line(seg(7, 3.5, 17, 3.5)),
        shell(poly([(8.25, 5.5), (15.75, 5.5), (15.75, 18.5), (8.25, 18.5)], closed=True, r=S.r * 0.3)),
        *_flutes(8.25, 15.75, 8, 18.5),
        shell(rect(6, 18.5, 12, 2.5, L(S, 0, 1))),
    ]


@icon("corinthian-column", CAT, "Fluted column with a flared bell capital of curled leaves",
      tags=["corinthian", "classical column", "acanthus", "roman column", "pillar", "architecture"])
def _(S):
    cap = "M3.5 3H20.5L18.5 5.5Q16.5 6.5 15.5 10H8.5Q7.5 6.5 5.5 5.5Z"
    return [
        shell(cap),
        detail("M9 5.5Q10.5 7 10.5 8.5"), detail("M15 5.5Q13.5 7 13.5 8.5"),
        shell(poly([(8.5, 10), (15.5, 10), (15.5, 18.5), (8.5, 18.5)], closed=True, r=S.r * 0.3)),
        *_flutes(8.5, 15.5, 12, 18.5),
        shell(rect(6, 18.5, 12, 2.5, L(S, 0, 1))),
    ]


@icon("twisted-column", CAT, "Column with a spiraling corkscrew shaft on a square base",
      tags=["solomonic column", "barley twist", "spiral column", "baroque", "pillar", "architecture"],
      aliases=["solomonic-column"])
def _(S):
    parts = [
        shell(rect(6, 2.5, 12, 2.5, L(S, 0, 1))),
        shell(rect(6, 18.5, 12, 2.5, L(S, 0, 1))),
    ]
    parts.append(shell(poly([(9, 5), (15, 5), (16.2, 7.25), (15, 9.5), (16.2, 11.75), (15, 14), (16.2, 16.25),
                              (15, 18.5), (9, 18.5), (7.8, 16.25), (9, 14), (7.8, 11.75), (9, 9.5), (7.8, 7.25)],
                             closed=True, r=S.r * 0.6)))
    for y in (7, 11.5, 16):
        parts.append(detail(seg(9, y + 1.6, 15, y - 1.6)))
    return parts


@icon("egyptian-column", CAT, "Thick column of bundled stalks with an open papyrus flower capital",
      tags=["papyrus column", "lotus column", "ancient egypt", "karnak", "pillar", "architecture"],
      aliases=["papyrus-column"])
def _(S):
    cap = "M3 3H21Q18 5.5 16.5 9.5H7.5Q6 5.5 3 3Z"
    return [
        shell(cap),
        shell(poly([(7.5, 11.5), (16.5, 11.5), (16, 21), (8, 21)], closed=True, r=S.r * 0.3)),
        detail(seg(10.5, 14, 10.5, 21)), detail(seg(13.5, 14, 13.5, 21)),
    ]


# ============================================================================ arches and domes

@icon("pointed-arch", CAT, "Gothic doorway arch of two curves meeting in a point at the top",
      tags=["gothic arch", "lancet arch", "ogival", "gothic", "cathedral", "doorway"], aliases=["gothic-arch"])
def _(S):
    return [
        shell(L(S, "M4 21V13A9.5 9.5 0 0 1 12 3.62A9.5 9.5 0 0 1 20 13V21Z",
                "M4 19.5V13A9.5 9.5 0 0 1 12 3.62A9.5 9.5 0 0 1 20 13V19.5A1.5 1.5 0 0 1 18.5 21H5.5A1.5 1.5 0 0 1 4 19.5Z")),
        detail("M7.5 21V13A6 6 0 0 1 12 7.14A6 6 0 0 1 16.5 13V21"),
    ]


@icon("horseshoe-arch", CAT, "Moorish arch whose curve runs past a half circle and narrows toward its base, in a square frame",
      tags=["moorish arch", "islamic arch", "keyhole arch", "andalusian", "alhambra", "doorway"],
      aliases=["moorish-arch"])
def _(S):
    c, r = (12, 11.5), 5.5
    dx = 3.6
    dy = math.sqrt(r * r - dx * dx)
    return [
        shell(rect(2.5, 2.5, 19, 18.5, L(S, 1, 3))),
        detail(f"M{fmt(c[0] - dx)} 21V{fmt(c[1] + dy)}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(c[0] + dx)} {fmt(c[1] + dy)}V21"),
    ]


@icon("ogee-arch", CAT, "Arch with an S-curved outline on each side rising to a sharp point",
      tags=["ogee", "gothic arch", "venetian arch", "keel arch", "tudor", "doorway"])
def _(S):
    return [
        shell(L(S, "M4 21V13C4 9.5 12 9 12 2.5C12 9 20 9.5 20 13V21Z",
                "M4 19.5V13C4 9.5 12 9 12 2.5C12 9 20 9.5 20 13V19.5A1.5 1.5 0 0 1 18.5 21H5.5A1.5 1.5 0 0 1 4 19.5Z")),
        detail("M7.5 21V13.5C7.5 11.5 12 11 12 7.5C12 11 16.5 11.5 16.5 13.5V21"),
    ]


def _circle_isect(c1, r1, c2, r2, upper=True):
    (x1, y1), (x2, y2) = c1, c2
    d = math.hypot(x2 - x1, y2 - y1)
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(max(0.0, r1 * r1 - a * a))
    mx, my = x1 + a * (x2 - x1) / d, y1 + a * (y2 - y1) / d
    p1 = (mx + h * (y2 - y1) / d, my - h * (x2 - x1) / d)
    p2 = (mx - h * (y2 - y1) / d, my + h * (x2 - x1) / d)
    return min(p1, p2, key=lambda p: p[1]) if upper else max(p1, p2, key=lambda p: p[1])


def _trefoil(x0, x1, spring, rs, rt, top_c):
    lc, rc = (x0 + rs, spring), (x1 - rs, spring)
    a = _circle_isect(lc, rs, top_c, rt)
    b = _circle_isect(top_c, rt, rc, rs)
    return (f"M{fmt(x0)} 21V{fmt(spring)}A{fmt(rs)} {fmt(rs)} 0 0 1 {fmt(a[0])} {fmt(a[1])}"
            f"A{fmt(rt)} {fmt(rt)} 0 0 1 {fmt(b[0])} {fmt(b[1])}"
            f"A{fmt(rs)} {fmt(rs)} 0 0 1 {fmt(x1)} {fmt(spring)}V21")


@icon("trefoil-arch", CAT, "Arch with three rounded lobes forming its top edge",
      tags=["trefoil", "cusped arch", "gothic arch", "three lobed arch", "tracery", "doorway"],
      aliases=["cusped-arch"])
def _(S):
    outer = _trefoil(3.5, 20.5, 12, 4.25, 4.25, (12, 7.25)) + "Z"
    if S.name == "rounded":
        outer = outer.replace("V21Z", "V19.5A1.5 1.5 0 0 1 19 21H5A1.5 1.5 0 0 1 3.5 19.5Z", 1)
        outer = outer.replace("M3.5 21V12", "M3.5 19.5V12", 1)
    return [
        shell(outer),
        detail(seg(7, 21, 7, 14.5)), detail(seg(17, 21, 17, 14.5)),
        detail("M7 14.5A5 5 0 0 1 17 14.5"),
    ]


@icon("keystone", CAT, "Round arch of stone blocks with the wedge-shaped top stone highlighted",
      tags=["keystone", "arch", "voussoir", "masonry", "stonework", "key element"])
def _(S):
    c = (12, 14)
    R, r = 9, 5
    parts = [
        shell(L(S, f"M3 21V14A9 9 0 0 1 21 14V21H17V14A5 5 0 0 0 7 14V21Z",
                f"M3 19.5V14A9 9 0 0 1 21 14V19.5A1.5 1.5 0 0 1 19.5 21H18.5A1.5 1.5 0 0 1 17 19.5V14A5 5 0 0 0 7 14"
                f"V19.5A1.5 1.5 0 0 1 5.5 21H4.5A1.5 1.5 0 0 1 3 19.5Z")),
    ]
    for a in (-150, -30):
        p0 = (c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a)))
        p1 = (c[0] + R * math.cos(math.radians(a)), c[1] + R * math.sin(math.radians(a)))
        parts.append(detail(seg(*p0, *p1)))
    ks = [(c[0] + rr * math.cos(math.radians(a)), c[1] + rr * math.sin(math.radians(a)))
          for rr, a in ((r, -104), (R + 1.5, -106), (R + 1.5, -74), (r, -76))]
    parts.append(solid(poly(ks, closed=True, r=S.r * 0.3)))
    return parts


@icon("onion-dome", CAT, "Bulbous dome swelling outward then tapering to a pointed tip, on a drum",
      tags=["onion dome", "cupola", "russian dome", "bulbous dome", "orthodox", "mughal"])
def _(S):
    return [
        line(seg(12, 1.5, 12, 4)),
        shell(onion(12, 15, 4, 11)),
        shell(rect(6.5, 15, 11, 6, min(S.R, 1))),
        win(8.75, 17, 1.75, 2.5), win(13.5, 17, 1.75, 2.5),
    ]


@icon("geodesic-dome", CAT, "Dome built from a lattice of triangles",
      tags=["buckminster fuller", "geodesic", "dome", "biodome", "lattice", "sphere"])
def _(S):
    c, r = (12, 18), 10
    def x_at(y):
        return math.sqrt(r * r - (y - c[1]) ** 2)
    y1 = 14.5
    xb = x_at(21)
    parts = [shell(f"M{fmt(c[0] - xb)} 21A{r} {r} 0 1 1 {fmt(c[0] + xb)} 21Z")]
    parts.append(detail(seg(c[0] - x_at(y1), y1, c[0] + x_at(y1), y1)))
    parts.append(detail(poly([(7.25, y1), (12, 8), (16.75, y1)])))
    parts.append(detail(poly([(3, 21), (7.25, y1), (12, 21), (16.75, y1), (21, 21)])))
    return parts


@icon("chinese-pavilion", CAT, "Open pavilion on round columns with a curved roof whose eaves turn upward",
      tags=["ting", "pavilion", "garden pavilion", "chinese garden", "gazebo", "kiosk"], aliases=["ting"])
def _(S):
    return [
        line(seg(12, 1.5, 12, 3.5)),
        shell("M2 10Q5 10 7 6.5L12 3.5L17 6.5Q19 10 22 10Z"),
        line(seg(5.5, 10, 5.5, 17.5)), line(seg(10, 10, 10, 17.5)),
        line(seg(14, 10, 14, 17.5)), line(seg(18.5, 10, 18.5, 17.5)),
        line(seg(5.5, 12.5, 18.5, 12.5)),
        shell(rect(3, 17.5, 18, 3.5, min(S.R, 1))),
    ]


@icon("colonnade", CAT, "Long row of evenly spaced columns under a flat beam, seen in perspective",
      tags=["columns", "portico", "peristyle", "stoa", "classical", "row of columns"], aliases=["peristyle"])
def _(S):
    top = lambda x: 4 + (x - 2) * 0.22
    bot = lambda x: 21 - (x - 2) * 0.22
    parts = [
        shell(poly([(2, 2), (22, 6.4), (22, 9), (2, 6.5)], closed=True, r=S.r * 0.3)),
        line(seg(2, 21, 22, 16.6)),
    ]
    for x in (4, 8.5, 12.5, 16, 19, 21.5):
        yt = 6.5 + (x - 2) * (9 - 6.5) / 20 + 1
        parts.append(line(seg(x, yt, x, bot(x) - 1)))
    return parts


@icon("arcade-walkway", CAT, "Row of repeated round arches on columns forming a covered walkway",
      tags=["arcade", "arches", "cloister", "loggia", "covered walkway", "portico"], )
def _(S):
    return [
        shell(rect(2, 3, 20, 3.5, min(S.R, 1))),
        line("M3 21V13A3 3 0 0 1 9 13V21M9 13A3 3 0 0 1 15 13V21M15 13A3 3 0 0 1 21 13V21"),
    ]


@icon("rose-window", CAT, "Large round window with petal-shaped tracery radiating from the centre",
      tags=["stained glass", "gothic window", "cathedral window", "church window", "tracery", "rosette"])
def _(S):
    parts = [shell(circle(12, 12, 9.5)), dot(12, 12, 1.5)]
    for i in range(6):
        a = math.radians(-90 + i * 60)
        p0 = (12 + 3.5 * math.cos(a), 12 + 3.5 * math.sin(a))
        p1 = (12 + 8 * math.cos(a), 12 + 8 * math.sin(a))
        if S.name == "line":
            parts.append(detail(f"M{fmt(p0[0])} {fmt(p0[1])}A3.2 3.2 0 0 1 {fmt(p1[0])} {fmt(p1[1])}"
                                f"A3.2 3.2 0 0 1 {fmt(p0[0])} {fmt(p0[1])}Z"))
        else:
            rot_deg = -90 + i * 60
            parts.append(detail(f"M{fmt(p0[0])} {fmt(p0[1])}A2.25 1.3 {fmt(rot_deg)} 1 1 {fmt(p1[0])} {fmt(p1[1])}"
                                f"A2.25 1.3 {fmt(rot_deg)} 1 1 {fmt(p0[0])} {fmt(p0[1])}Z"))
    return parts


@icon("barred-window", CAT, "Small window with vertical iron bars across it",
      tags=["window bars", "security bars", "jail window", "cell window", "grille", "burglar bars"],
      aliases=["window-bars"])
def _(S):
    return [
        shell(rect(4, 3, 16, 14.5, min(S.R, 2))),
        detail(seg(8, 3, 8, 17.5)), detail(seg(12, 3, 12, 17.5)), detail(seg(16, 3, 16, 17.5)),
        shell(rect(2.5, 19, 19, 2, L(S, 0, 1))),
    ]


@icon("leaded-window", CAT, "Window with a diamond lattice of lead lines between small panes",
      tags=["leaded glass", "lattice window", "diamond pane", "tudor window", "casement", "cottage window"],
      aliases=["lattice-window"])
def _(S):
    x0, y0, x1, y1 = 5, 3, 19, 21
    parts = [shell(rect(x0, y0, x1 - x0, y1 - y0, L(S, 1, 3.5)))]
    for c in (-9, -3, 3, 9):
        # lines y = x + c (down-right) clipped to the rectangle
        a = max(x0, y0 - c); b = min(x1, y1 - c)
        if b - a > 0.5:
            parts.append(detail(seg(a, a + c, b, b + c)))
        # lines y = -x + k (down-left), k = c + 24
        k = c + 24
        a = max(x0, k - y1); b = min(x1, k - y0)
        if b - a > 0.5:
            parts.append(detail(seg(a, k - a, b, k - b)))
    return parts


@icon("rolling-shutter", CAT, "Shop front with a ribbed roll-down shutter half lowered from its box",
      tags=["roller shutter", "roll up door", "security shutter", "shop shutter", "garage door", "roller door"],
      aliases=["roller-shutter"])
def _(S):
    return [
        shell(rect(2, 2.5, 20, 4, min(S.R, 1.5))),
        shell(rect(4, 6.5, 16, 7.5, 0)),
        detail(seg(4, 9, 20, 9)), detail(seg(4, 11.5, 20, 11.5)),
        line(seg(4, 14, 4, 21)), line(seg(20, 14, 20, 21)),
        line(seg(10.5, 15.5, 13.5, 15.5)),
    ]


@icon("fire-escape", CAT, "Zigzag metal stairs and railed landings on the side of a brick building",
      tags=["fire stairs", "emergency exit", "escape stairs", "apartment", "new york", "external stairs"],
      aliases=["fire-stairs"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 8.5, 18.5, min(S.R, 1))),
        win(5, 5.5, 3.5, 3), win(5, 12.5, 3.5, 3),
        line(seg(11, 8.5, 21.5, 8.5)), line(seg(11, 15.5, 21.5, 15.5)),
        line(seg(21.5, 5.5, 21.5, 15.5)),
        line(seg(13, 15.5, 19.5, 8.5)),
        line(seg(13, 21, 19.5, 15.5)),
    ]



# ============================================================================ roof types
# Walls are open strokes so the roof (a shell) carries the weight in every style.

def _walls(S, x0, x1, top, ground=21.0):
    return line(poly([(x0, top), (x0, ground), (x1, ground), (x1, top)], r=S.r * 0.5))


@icon("gable-roof", CAT, "House seen at an angle with a simple two-sided pitched roof over a triangular gable end",
      tags=["pitched roof", "gable", "roof", "roofing", "house", "apex roof"], aliases=["pitched-roof"])
def _(S):
    return [
        shell(poly([(2.5, 12), (7, 5.5), (17, 5.5), (21.5, 12)], closed=True, r=S.r * 0.3)),
        detail(seg(7, 5.5, 11.5, 12)),
        _walls(S, 4, 20, 13.5),
        line(seg(11.5, 13.5, 11.5, 21)),
        win(6.25, 15.5, 3, 2.5),
    ]


@icon("hip-roof", CAT, "House with a roof sloping down on all four sides to a short ridge",
      tags=["hipped roof", "hip", "roof", "roofing", "house", "four sided roof"], aliases=["hipped-roof"])
def _(S):
    return [
        shell(poly([(2.5, 12), (8.5, 5), (15.5, 5), (21.5, 12)], closed=True, r=S.r * 0.3)),
        detail(seg(8.5, 5, 6, 12)), detail(seg(15.5, 5, 18, 12)),
        _walls(S, 4, 20, 13.5),
        door(S, 10, 14, 16.5),
    ]


@icon("gambrel-roof", CAT, "Barn-style roof with two slopes on each side, steep below and shallow above",
      tags=["gambrel", "barn roof", "dutch roof", "roof", "roofing", "double pitch"], aliases=["barn-roof"])
def _(S):
    return [
        shell(poly([(2, 13), (3.5, 8), (7.5, 4), (11.5, 8), (13, 13)], closed=True, r=S.r * 0.3)),
        shell(poly([(7.5, 4), (18.5, 4), (21.5, 8), (21.5, 13), (13, 13), (11.5, 8)], closed=True,
                   r=S.r * 0.3)),
        detail(seg(11.5, 8, 21.5, 8)),
        _walls(S, 3.5, 20.5, 14.5),
        line(seg(11.5, 14.5, 11.5, 21)),
    ]


@icon("mansard-roof", CAT, "Roof with a steep lower slope pierced by dormer windows and a flat top",
      tags=["mansard", "french roof", "roof", "dormer", "second empire", "roofing"], aliases=["french-roof"])
def _(S):
    return [
        shell(poly([(2.5, 12.5), (5, 4), (19, 4), (21.5, 12.5)], closed=True, r=S.r * 0.3)),
        mark(poly([(6.5, 11), (6.5, 7.5), (8, 6.25), (9.5, 7.5), (9.5, 11)], closed=True)),
        mark(poly([(10.5, 11), (10.5, 7.5), (12, 6.25), (13.5, 7.5), (13.5, 11)], closed=True)),
        mark(poly([(14.5, 11), (14.5, 7.5), (16, 6.25), (17.5, 7.5), (17.5, 11)], closed=True)),
        _walls(S, 4, 20, 14),
        door(S, 10, 14, 16.5),
    ]


@icon("butterfly-roof", CAT, "Modern house whose two roof surfaces slope inward to a central V-shaped valley",
      tags=["butterfly", "v roof", "inverted roof", "modernist", "roof", "mid century"], aliases=["v-roof"])
def _(S):
    return [
        shell(poly([(2, 4), (12, 8.5), (22, 4), (22, 7), (12, 11.5), (2, 7)], closed=True, r=S.r * 0.3)),
        line(poly([(4, 8), (4, 21), (20, 21), (20, 8)], r=S.r * 0.5)),
        detail(poly([(7, 21), (7, 14.5), (17, 14.5), (17, 21)], r=S.r * 0.5)),
        detail(seg(12, 14.5, 12, 21)),
    ]


@icon("skillion-roof", CAT, "Modern house with a single sloping roof plane, high on one side",
      tags=["shed roof", "mono pitch", "lean to roof", "single slope", "modern house", "roof"],
      aliases=["shed-roof", "mono-pitch-roof"])
def _(S):
    return [
        shell(poly([(2, 10.5), (22, 3), (22, 5.75), (2, 13.25)], closed=True, r=S.r * 0.3)),
        line(poly([(4, 13), (4, 21), (20, 21), (20, 7)], r=S.r * 0.5)),
        win(13.5, 10.5, 3.5, 5),
        door(S, 7, 10.5, 16),
    ]


@icon("pyramid-roof", CAT, "Square building topped by four triangular roof faces meeting at a point",
      tags=["pyramid hip roof", "pavilion roof", "tented roof", "roof", "square roof", "roofing"],
      aliases=["pavilion-roof"])
def _(S):
    return [
        shell(poly([(2.5, 11), (12, 2.5), (21.5, 11), (11, 13.5)], closed=True, r=S.r * 0.3)),
        detail(seg(12, 2.5, 11, 13.5)),
        line(poly([(4, 12.5), (4, 18.5), (11, 21), (20, 18.5), (20, 12.5)], r=S.r * 0.5)),
        line(seg(11, 15, 11, 21)),
    ]


# ============================================================================ structure and planning

@icon("flying-buttress", CAT, "Half-arch strut leaning from an outer pier against a tall wall",
      tags=["buttress", "gothic", "cathedral", "arch support", "masonry", "structure"])
def _(S):
    return [
        shell(poly([(15.5, 21), (15.5, 5), (18.5, 2.5), (21.5, 5), (21.5, 21)], closed=True, r=S.r * 0.3)),
        shell(poly([(2.5, 21), (2.5, 10.5), (4.5, 7), (6.5, 10.5), (6.5, 21)], closed=True, r=S.r * 0.3)),
        shell("M6.5 11L15.5 7V11Q9.5 11.5 6.5 16Z"),
    ]


@icon("courtyard", CAT, "Top-down square ring of building wings around an open court with a tree",
      tags=["courtyard", "quadrangle", "atrium", "patio", "cloister", "site plan"], aliases=["quadrangle"])
def _(S):
    outer = "M2.5 2.5H21.5V21.5H2.5Z" if S.name == "line" else "M5 2.5H19A2.5 2.5 0 0 1 21.5 5V19A2.5 2.5 0 0 1 19 21.5H5A2.5 2.5 0 0 1 2.5 19V5A2.5 2.5 0 0 1 5 2.5Z"
    inner = "M7.5 7.5V16.5H16.5V7.5Z"
    return [
        shell(outer + inner),
        detail(seg(2.5, 2.5, 7.5, 7.5)), detail(seg(21.5, 2.5, 16.5, 7.5)),
        detail(seg(2.5, 21.5, 7.5, 16.5)), detail(seg(21.5, 21.5, 16.5, 16.5)),
        dot(12, 12, 2.25),
    ]


@icon("architectural-model", CAT, "Small house model on a square base with a scale bar beside it",
      tags=["scale model", "maquette", "architecture model", "design", "architect", "presentation"],
      aliases=["maquette"])
def _(S):
    return [
        line(seg(14, 4.5, 21.5, 4.5)),
        line(seg(14, 3, 14, 6)), line(seg(21.5, 3, 21.5, 6)), line(seg(17.75, 3.5, 17.75, 5.5)),
        shell(poly([(5, 16), (5, 10.5), (9.5, 6.5), (14, 10.5), (14, 16)], closed=True, r=S.r * 0.4)),
        shell(poly([(2.5, 21), (4.5, 17.5), (19.5, 17.5), (21.5, 21)], closed=True, r=S.r * 0.3)),
        dot(18, 14, 1.75),
    ]


@icon("building-cutaway", CAT, "Building cut open to show stacked floors connected by stairs",
      tags=["cross section", "section drawing", "floors", "stairs", "architecture", "building section"],
      aliases=["building-section"])
def _(S):
    return [
        shell(poly([(3, 21), (3, 9), (12, 2.5), (21, 9), (21, 21)], closed=True, r=S.r * 0.4)),
        detail(seg(3, 15, 21, 15)), detail(seg(3, 9, 21, 9)),
        detail(poly([(7, 21), (7, 19), (9, 19), (9, 17), (11, 17), (11, 15)])),
        detail(poly([(13, 15), (13, 13), (15, 13), (15, 11), (17, 11), (17, 9)])),
    ]


@icon("real-estate-sign", CAT, "Sign panel hanging from a post arm with a small house symbol on it",
      tags=["for sale sign", "property sign", "realtor", "estate agent", "house for sale", "to let"],
      aliases=["for-sale-sign"])
def _(S):
    return [
        line(poly([(5, 21), (5, 4.5), (20, 4.5)], r=S.r)),
        line(seg(10, 4.5, 10, 8)), line(seg(18, 4.5, 18, 8)),
        shell(rect(8.5, 8, 11, 8.5, min(S.R, 1.5))),
        detail(poly([(11.5, 14.5), (11.5, 12), (14, 10.25), (16.5, 12), (16.5, 14.5)], closed=True)),
        line(seg(2.5, 21, 9, 21)),
    ]



# ============================================================================ townscape and street furniture

@icon("city-skyline", CAT, "Row of mixed tall and short building silhouettes along a baseline",
      tags=["skyline", "cityscape", "downtown", "urban", "city", "metropolis"], aliases=["cityscape"])
def _(S):
    pts = [(2, 21), (2, 12), (5.5, 12), (5.5, 7), (9.5, 7), (9.5, 3.5), (11, 2), (12.5, 3.5), (12.5, 10), (15, 10),
           (15, 5.5), (19, 5.5), (19, 13.5), (22, 13.5), (22, 21)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.3)),
        win(6.5, 10, 2, 2), win(6.5, 15, 2, 2), win(10, 7, 2, 2),
        win(16, 8.5, 2, 2), win(16, 13.5, 2, 2), win(3, 15.5, 2, 2),
    ]


def _house(S, x0, x1, top, eave, ground=21.0):
    mid = (x0 + x1) / 2
    return shell(poly([(x0, ground), (x0, eave), (mid, top), (x1, eave), (x1, ground)], closed=True, r=S.r * 0.4))


@icon("suburb", CAT, "Row of small detached houses with a round tree between them",
      tags=["suburbs", "neighborhood", "neighbourhood", "residential", "housing", "homes"])
def _(S):
    return [
        _house(S, 2, 8, 10, 13.5),
        door(S, 4, 6, 17.5),
        shell(circle(12, 11.5, 2.25)),
        line(seg(12, 13.75, 12, 21)),
        _house(S, 16, 22, 10, 13.5),
        door(S, 18, 20, 17.5),
    ]


@icon("village", CAT, "Cluster of small houses around a church steeple on a gentle hill",
      tags=["hamlet", "small town", "rural", "countryside", "parish", "community"])
def _(S):
    return [
        line("M1.5 21.5Q12 17.5 22.5 21.5"),
        shell(poly([(2.5, 19.5), (2.5, 14.5), (5.25, 12), (8, 14.5), (8, 18.4)], closed=True, r=S.r * 0.4)),
        *cross_line(12, 1.5, 5, arm=1.25),
        shell(poly([(9.5, 17.8), (9.5, 10), (12, 6), (14.5, 10), (14.5, 17.8)], closed=True, r=S.r * 0.4)),
        dot(12, 12, 1),
        shell(poly([(16, 18.4), (16, 14.5), (18.75, 12), (21.5, 14.5), (21.5, 19.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("drinking-fountain", CAT, "Pedestal drinking fountain with an arc of water rising from its spout",
      tags=["water fountain", "bubbler", "drinking water", "water", "public fountain", "hydration"],
      aliases=["water-fountain", "bubbler"])
def _(S):
    return [
        line("M10 9C10 3.5 16.5 3 17 8.5"),
        shell(poly([(4.5, 9.5), (19.5, 9.5), (17.5, 13), (6.5, 13)], closed=True, r=S.r * 0.4)),
        shell(poly([(9.5, 13), (14.5, 13), (14, 18.5), (10, 18.5)], closed=True, r=S.r * 0.3)),
        shell(rect(7, 18.5, 10, 2.5, L(S, 0, 1))),
    ]


@icon("advertising-column", CAT, "Cylindrical pillar covered in posters with a domed cap on top",
      tags=["litfass column", "poster column", "morris column", "billboard", "posters", "street advertising"],
      aliases=["poster-column", "morris-column"])
def _(S):
    return [
        line(seg(12, 1.5, 12, 3.5)),
        shell("M6.5 7.5A5.5 4 0 0 1 17.5 7.5Z"),
        shell(rect(5.5, 7.5, 13, 2, L(S, 0, 1))),
        shell(rect(7, 9.5, 10, 9.5, 0)),
        mark(rect(8.75, 11.25, 3, 4)), mark(rect(12.75, 12.5, 2.5, 4.75)),
        shell(rect(6, 19, 12, 2, L(S, 0, 1))),
    ]


@icon("billboard", CAT, "Large rectangular sign board on tall legs with a narrow catwalk",
      tags=["hoarding", "advertising", "outdoor ad", "roadside sign", "marketing", "poster board"],
      aliases=["hoarding"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 10, min(S.R, 1.5))),
        detail(seg(6, 7, 13, 7)), detail(seg(6, 10, 10, 10)),
        line(seg(3.5, 15.5, 20.5, 15.5)),
        line(seg(8, 13, 8, 21)), line(seg(16, 13, 16, 21)),
    ]


@icon("clock-post", CAT, "Round two-faced street clock on top of an ornate post",
      tags=["street clock", "post clock", "town clock", "public clock", "pillar clock", "time"],
      aliases=["street-clock"])
def _(S):
    return [
        dot(12, 1.75, 1),
        shell(circle(12, 7.5, 5)),
        detail(poly([(12, 5.5), (12, 7.5), (13.75, 7.5)])),
        line(seg(9.5, 13.75, 14.5, 13.75)),
        line(seg(12, 14.75, 12, 18.5)),
        shell(poly([(8, 21), (9.5, 18.5), (14.5, 18.5), (16, 21)], closed=True, r=S.r * 0.3)),
    ]


@icon("phone-booth", CAT, "Tall telephone booth with a domed roof, a sign band and a paned glass door",
      tags=["telephone box", "phone box", "call box", "payphone", "telephone kiosk", "public phone"],
      aliases=["phone-box", "telephone-box"])
def _(S):
    return [
        shell("M5.5 7C5.5 4 8.5 2.5 12 2.5C15.5 2.5 18.5 4 18.5 7Z"),
        shell(rect(6, 7, 12, 14, L(S, 0, 1.5))),
        detail(seg(6, 10, 18, 10)),
        detail(seg(12, 10, 12, 21)),
        detail(seg(6, 14, 18, 14)), detail(seg(6, 17.5, 18, 17.5)),
    ]
