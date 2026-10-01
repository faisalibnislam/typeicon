"""TypeIcon Core: furniture (batch furniture_005).

Original drawings of rooms and layouts, AR furniture preview, sizing, a hanging scroll and a blanket fort.
"""
from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar  # noqa: F401

CAT = "furniture"


def L(S, a, b):
    return a if S.name == "line" else b


def rr(S, cap=None):
    if cap is None:
        return S.R
    return min(S.R, cap) if S.name == "rounded" else min(S.R, cap) * 0.4


@icon("studio-apartment", CAT, "Floor plan of one open room with a bed, a sofa and a kitchenette along the wall.",
      tags=["studio flat", "bedsit", "one room", "floor plan", "small apartment", "housing", "rental"],
      aliases=["studio-flat"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 2.5))),
        detail(rect(5.5, 5.5, 6, 6, rr(S, 1))),
        detail(seg(5.5, 8, 11.5, 8)),
        detail(rect(16, 5.5, 2.5, 6, 0)),
        detail(rect(6, 16, 12, 2.5, 0)),
    ]


@icon("open-plan-office", CAT, "Two computer monitors on a shared desk, each with an office chair in front.",
      tags=["shared desks", "coworking", "workspace", "office", "team", "hot desk", "bullpen"],
      aliases=["coworking-desk"])
def _(S):
    return [
        shell(rect(3, 3, 8, 6, rr(S, 1.5))),
        shell(rect(13, 3, 8, 6, rr(S, 1.5))),
        line(seg(2.5, 12.5, 21.5, 12.5)),
        line(seg(4, 12.5, 4, 21)), line(seg(20, 12.5, 20, 21)),
        shell(rect(7, 16, 3.5, 5, rr(S, 1.5))),
        shell(rect(13.5, 16, 3.5, 5, rr(S, 1.5))),
    ]


@icon("view-in-room", CAT, "Smartphone screen showing an armchair placed in a room, for previewing furniture at home.",
      tags=["ar", "augmented reality", "preview", "try at home", "phone", "room view", "place furniture"],
      aliases=["view-in-your-room"])
def _(S):
    chair = U(P(rect(9, 6.5, 6, 5.5, 1.5)), P(rect(7, 10.5, 10, 5, 1.5)), P(rect(8, 15, 1.5, 2.5)), P(rect(14.5, 15, 1.5, 2.5)))
    return [
        shell(rect(4.5, 2.5, 15, 19, rr(S, 3))),
        Part("dot", path_to_d(chair)),
    ]


@icon("furniture-dimensions", CAT, "Sofa with measuring arrows along its width and its height.",
      tags=["size", "measure", "width", "height", "sofa size", "fit", "measurements"],
      aliases=["sofa-dimensions"])
def _(S):
    body = path_to_d(U(P(rect(4.5, 4.5, 10, 12, rr(S, 2))), P(rect(2.5, 9, 14, 7.5, rr(S, 2)))))
    return [
        shell(body),
        detail(seg(6.5, 12, 6.5, 16.5)), detail(seg(12.5, 12, 12.5, 16.5)),
        line(seg(2.5, 20.5, 16.5, 20.5)),
        line(poly([(5, 19), (2.5, 20.5), (5, 22)], r=S.r * 0.3)),
        line(poly([(14, 19), (16.5, 20.5), (14, 22)], r=S.r * 0.3)),
        line(seg(20.5, 4.5, 20.5, 16.5)),
        line(poly([(19, 7), (20.5, 4.5), (22, 7)], r=S.r * 0.3)),
        line(poly([(19, 14), (20.5, 16.5), (22, 14)], r=S.r * 0.3)),
    ]


@icon("hanging-scroll", CAT, "Tall painted scroll with a rod at the top and bottom, hung from a cord.",
      tags=["wall scroll", "kakejiku", "painting", "wall art", "asian art", "decor", "calligraphy"],
      aliases=["wall-scroll"])
def _(S):
    return [
        line(poly([(8, 6), (12, 2.5), (16, 6)], r=S.r * 0.5)),
        line(seg(4, 6, 20, 6)),
        line(seg(4, 20.5, 20, 20.5)),
        shell(rect(7, 6, 10, 14.5, 0)),
        detail(poly([(9.5, 17), (12, 12.5), (14.5, 17)], r=S.r * 0.6)),
        dot(14.5, 9.5, 1.25),
    ]


@icon("blanket-fort", CAT, "Blanket draped over two chairs to make a tent, with a pillow at the entrance.",
      tags=["pillow fort", "den", "kids", "play tent", "cushion fort", "childhood", "cozy"],
      aliases=["pillow-fort"])
def _(S):
    r = L(S, 0, 1.5)
    tent = f"M2.5 20.5L5 8.5Q12 12 19 8.5L21.5 20.5Z"
    return [
        shell(tent),
        detail(poly([(9, 20.5), (9, 15), (15, 15), (15, 20.5)], r=S.r * 0.6)),
        shell(rect(9.5, 17.5, 5, 3, 1.25)),
        dot(5, 5, 1.5), dot(19, 5, 1.5),
    ]
