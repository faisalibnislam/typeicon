"""TypeIcon Core: hospitality (batch 003)."""
from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import polar

CAT = "hospitality"


def chair(S, x, y):
    """Small top-down chair mark: square in Line, round in Rounded."""
    if S.name == "line":
        return solid(rect(x - 1, y - 1, 2, 2))
    return dot(x, y, 1.1)


@icon("chair-cover-sash", CAT, "Chair fully covered in fabric with a wide sash tied around its back.",
      tags=["chair cover", "sash", "wedding", "event", "banquet", "bow", "linen"])
def _(S):
    return [
        shell(poly([(8, 3), (16, 3), (16, 11), (19, 11), (19, 21), (5, 21), (5, 11), (8, 11)], closed=True, r=S.r)),
        detail(seg(8, 7, 16, 7)),
        dot(12, 7, 1.6),
        detail(seg(9, 15, 9, 18)),
        detail(seg(15, 15, 15, 18)),
    ]


@icon("stacked-chairs", CAT, "Several identical chairs stacked on top of each other, seen from the side.",
      tags=["chairs", "stack", "storage", "event", "furniture", "banquet"])
def _(S):
    parts = []
    for y in (9, 14, 19):
        parts.append(line(poly([(3, y - 5), (5, y), (17, y)], r=S.r)))
    parts.append(line(seg(17, 9, 17, 21)))
    return parts


@icon("folding-partition", CAT, "Tall hinged wall panels folded in a zigzag to divide a room.",
      tags=["room divider", "accordion wall", "movable wall", "partition", "banquet", "meeting room"])
def _(S):
    return [
        shell(poly([(3, 5), (7.5, 3), (12, 5), (16.5, 3), (21, 5), (21, 21), (16.5, 19), (12, 21), (7.5, 19), (3, 21)],
                   closed=True, r=S.r)),
        detail(seg(7.5, 3, 7.5, 19)),
        detail(seg(12, 5, 12, 21)),
        detail(seg(16.5, 3, 16.5, 19)),
    ]


@icon("interpretation-headset", CAT, "Single ear headphone with a small receiver box on a cord.",
      tags=["interpreter", "translation", "conference", "earpiece", "receiver", "language channel"])
def _(S):
    return [
        line("M5.5 9C5.5 2.5 18.5 2.5 18.5 9"),
        shell(rect(3, 9, 5, 7, min(S.R, 2))),
        line("M5.5 16V19H11"),
        shell(rect(11, 16, 10, 6, min(S.R, 2))),
        dot(16, 19, 1.2),
    ]


@icon("banquet-hall", CAT, "Large room with a chandelier at the top and round tables below.",
      tags=["ballroom", "function room", "event hall", "reception", "wedding venue", "chandelier"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, S.R)),
        detail(seg(12, 4, 12, 7)),
        detail(poly([(8, 11), (8, 9.5), (16, 9.5), (16, 11)], r=S.r)),
        dot(10, 12, 0.9),
        dot(14, 12, 0.9),
        detail(circle(7, 17, 1.5)),
        detail(circle(17, 17, 1.5)),
    ]


def seat_row(S, y, xs):
    return [chair(S, x, y) for x in xs]


@icon("theater-style-seating", CAT, "Top down layout of rows of chairs all facing a stage bar.",
      tags=["theatre seating", "auditorium layout", "room setup", "conference", "rows", "seating plan"])
def _(S):
    parts = [line(seg(4, 4.5, 20, 4.5))]
    for y in (11.5, 15.5, 19.5):
        parts += seat_row(S, y, (4, 8, 12, 16, 20))
    return parts


@icon("u-shape-seating", CAT, "Top down layout of tables in a U with chairs around the outside facing a screen.",
      tags=["u shape", "room setup", "meeting layout", "training", "seating plan", "workshop"])
def _(S):
    parts = [line(seg(8, 3, 16, 3)), line(poly([(7, 7), (7, 17), (17, 17), (17, 7)], r=S.r))]
    for y in (9, 14):
        parts += [chair(S, 3, y), chair(S, 21, y)]
    parts += [chair(S, 9.5, 21), chair(S, 14.5, 21)]
    return parts


@icon("boardroom-seating", CAT, "Top down layout of one long table with chairs along both sides and ends.",
      tags=["boardroom", "meeting table", "room setup", "conference table", "seating plan", "board meeting"])
def _(S):
    parts = [shell(rect(7, 8, 10, 8, S.R))]
    for x in (8.5, 12, 15.5):
        parts += [chair(S, x, 4), chair(S, x, 20)]
    parts += [chair(S, 3, 12), chair(S, 21, 12)]
    return parts


@icon("cabaret-seating", CAT, "Top down layout of round tables with chairs on the side facing a stage.",
      tags=["cabaret", "room setup", "event layout", "round tables", "stage", "seating plan"])
def _(S):
    parts = [shell(rect(4, 2.5, 16, 2, min(S.R, 1)))]
    for cx in (7, 17):
        parts.append(shell(circle(cx, 14, 2.6)))
        for a in (-125, -90, -55):
            x, y = polar(cx, 14, 7, a)
            parts.append(chair(S, x, y))
    return parts


@icon("banquet-style-seating", CAT, "Top down layout of a grid of round tables with chairs all the way around each.",
      tags=["banquet", "round tables", "room setup", "wedding layout", "gala", "seating plan"])
def _(S):
    parts = []
    for cx in (7, 17):
        for cy in (7, 17):
            parts.append(shell(circle(cx, cy, 1.8)))
            for a in (45, 135, 225, 315):
                x, y = polar(cx, cy, 4.9, a)
                parts.append(chair(S, x, y))
    return parts


@icon("pizza-delivery-bag", CAT, "Square insulated bag with a zip on three sides and a carry strap.",
      tags=["pizza bag", "food delivery", "insulated bag", "takeaway", "courier", "hot food"])
def _(S):
    return [
        line("M8 7V4H16V7"),
        shell(rect(3, 7, 18, 14, S.R)),
        detail(poly([(7, 18), (7, 11), (17, 11), (17, 18)], r=S.r)),
    ]


@icon("dumbwaiter", CAT, "Wall hatch with a raised door showing a covered plate and a pull rope.",
      tags=["food lift", "service hatch", "kitchen lift", "hatch", "serving", "pulley"])
def _(S):
    return [
        shell(rect(3, 3, 13, 18, S.R)),
        detail(seg(3, 8, 16, 8)),
        shell(poly([(6, 17), (6, 15.5), (13.5, 15.5), (13.5, 17)], closed=True) if False else
              "M6 17A3.75 3.75 0 0 1 13.5 17Z"),
        line(seg(20, 3, 20, 13)),
        dot(20, 16, 1.5),
    ]


@icon("kitchen-swing-doors", CAT, "Pair of double swinging doors each with a round porthole window.",
      tags=["service doors", "restaurant kitchen", "saloon doors", "double doors", "porthole", "entrance"])
def _(S):
    return [
        shell(rect(3, 3, 7.5, 18, S.R)),
        shell(rect(13.5, 3, 7.5, 18, S.R)),
        detail(circle(6.75, 10, 1.3)),
        detail(circle(17.25, 10, 1.3)),
    ]


@icon("hot-holding-cabinet", CAT, "Tall wheeled cabinet with a handle and a small temperature dial.",
      tags=["warming cabinet", "food warmer", "catering", "heated cabinet", "kitchen equipment", "proofer"])
def _(S):
    return [
        shell(rect(5, 2, 14, 15, S.R)),
        detail(circle(10, 7, 1.5)),
        detail(seg(16, 9, 16, 14)),
        dot(8, 20.7, 1.3),
        dot(16, 20.7, 1.3),
    ]


@icon("table-skirt", CAT, "Table seen from the front with pleated fabric hanging to the floor.",
      tags=["table cover", "linen", "pleated skirting", "banquet table", "event", "tablecloth"])
def _(S):
    return [
        shell(rect(3, 4, 18, 3, min(S.R, 1.5))),
        shell("M6 7H18V18A2 2 0 0 1 14 18A2 2 0 0 1 10 18A2 2 0 0 1 6 18Z"),
        detail(seg(10, 10, 10, 16)),
        detail(seg(14, 10, 14, 16)),
    ]


@icon("cup-sleeve", CAT, "Paper coffee cup with a lid and a cardboard band around its middle.",
      tags=["coffee sleeve", "cup holder", "takeaway cup", "cafe", "paper cup", "heat guard"])
def _(S):
    return [
        shell(rect(5, 3, 14, 4, 1)),
        shell(poly([(6, 7), (18, 7), (16, 21), (8, 21)], closed=True, r=S.r)),
        detail(seg(6.7, 11.5, 17.3, 11.5)),
        detail(seg(7.3, 16.5, 16.7, 16.5)),
    ]
