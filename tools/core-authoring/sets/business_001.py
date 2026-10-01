"""TypeIcon Core: business (batch 001): money, payments, banking and markets.

Generic objects only: no bank, card network, payment provider, exchange or cryptocurrency logo.
Coins are circles with a centre mark, banknotes are landscape rectangles with a round emblem, matching the
finance and commerce categories.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "business"


# ============================================================================ helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def mark(d) -> Part:
    """Small solid mark of any shape (knocked out of a Filled shell)."""
    return Part("dot", d)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def grow(d, g):
    return path_to_d(U(P(d), ST(d, 2 * g, "round", "round")))


def cut(back, *fronts, g=3.2):
    """Back shape with a clean gap cut around the front shapes."""
    return minus(back, *[grow(f, g) for f in fronts])


def cutline(d, *fronts, g=2.2, S=None):
    """Open stroke d as a filled outline with the front shapes (plus a gap) removed."""
    cap = S.cap if S else "butt"
    join = S.join if S else "miter"
    return path_to_d(D(ST(d, 2, cap, join), *[P(grow(f, g)) for f in fronts]))


def rot_pts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rot_d(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def move(d, dx, dy):
    return path_to_d(transform_path(P(d), (1, 0, 0, 1, dx, dy)))


def flip(d, axis=12.0):
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 2 * axis, 0)))


def head(tip, deg, size=2.5):
    """Open arrowhead at tip; deg is the direction the arrow points (0 = right, 90 = down)."""
    a = polar(tip[0], tip[1], size * math.sqrt(2), deg + 180 - 45)
    b = polar(tip[0], tip[1], size * math.sqrt(2), deg + 180 + 45)
    return [a, tip, b]


def arrowhead(S, tip, deg, size=2.5):
    return line(poly(head(tip, deg, size), r=S.r * 0.5))


def heart(cx, cy, s):
    """Heart of half-width s centred on (cx, cy)."""
    pts = [(0, 0.9), (-0.6, 0.45), (-1, 0.05), (-1, -0.35), (-1, -0.65), (-0.75, -0.85), (-0.45, -0.85),
           (-0.25, -0.85), (-0.08, -0.75), (0, -0.55), (0.08, -0.75), (0.25, -0.85), (0.45, -0.85),
           (0.75, -0.85), (1, -0.65), (1, -0.35), (1, 0.05), (0.6, 0.45), (0, 0.9)]
    q = [f"{fmt(cx + x * s)} {fmt(cy + y * s)}" for x, y in pts]
    return f"M{q[0]}C{q[1]} {q[2]} {q[3]}C{q[4]} {q[5]} {q[6]}C{q[7]} {q[8]} {q[9]}C{q[10]} {q[11]} {q[12]}C{q[13]} {q[14]} {q[15]}C{q[16]} {q[17]} {q[18]}Z"


def dollar(cx, cy, k=1.0):
    """Dollar sign as detail strokes: an S (height 6k) with short bars above and below."""
    def p(x, y):
        return f"{fmt(cx + x * k)} {fmt(cy + y * k)}"
    s = (f"M{p(2.2, -2)}C{p(1.8, -2.6)} {p(1, -3)} {p(0, -3)}C{p(-1.3, -3)} {p(-2.2, -2.3)} {p(-2.2, -1.4)}"
         f"C{p(-2.2, 0.6)} {p(2.2, -0.6)} {p(2.2, 1.4)}C{p(2.2, 2.3)} {p(1.3, 3)} {p(0, 3)}"
         f"C{p(-1, 3)} {p(-1.8, 2.6)} {p(-2.2, 2)}")
    return [detail(s), detail(seg(cx, cy - 3 * k, cx, cy - 4.5 * k)), detail(seg(cx, cy + 3 * k, cx, cy + 4.5 * k))]


def percent(S, cx, cy, k=1.0):
    """Percent sign as detail strokes: a slash with a small ring above left and below right."""
    return [detail(seg(cx + 2.5 * k, cy - 3 * k, cx - 2.5 * k, cy + 3 * k)),
            dot(cx - 2 * k, cy - 2 * k, 1.15 * k), dot(cx + 2 * k, cy + 2 * k, 1.15 * k)]


def coin(S, cx, cy, r, centre=True):
    parts = [shell(circle(cx, cy, r))]
    if centre:
        parts.append(dot(cx, cy, 1.25 if r >= 4 else 1) if S.name == "rounded" or r < 3.5 else
                     sq(cx - 1.1, cy - 1.1, 2.2, 2.2))
    return parts


def note(S, x, y, w, h, emblem=True):
    parts = [shell(rect(x, y, w, h, rr(S, 2.5)))]
    if emblem:
        parts.append(detail(circle(x + w / 2, y + h / 2, min(w, h) / 2 - 2.25)))
    return parts


def soft(a, p, b, r):
    """Corner at p (from a, towards b): sharp for r == 0, softened with a quadratic otherwise."""
    if r <= 0:
        return f"L{fmt(p[0])} {fmt(p[1])}"
    la = math.hypot(a[0] - p[0], a[1] - p[1])
    lb = math.hypot(b[0] - p[0], b[1] - p[1])
    t = min(r, la / 2, lb / 2)
    s = (p[0] + (a[0] - p[0]) * t / la, p[1] + (a[1] - p[1]) * t / la)
    e = (p[0] + (b[0] - p[0]) * t / lb, p[1] + (b[1] - p[1]) * t / lb)
    return f"L{fmt(s[0])} {fmt(s[1])}Q{fmt(p[0])} {fmt(p[1])} {fmt(e[0])} {fmt(e[1])}"


def capsule(x1, y1, x2, y2, w):
    """Filled stadium (finger, tube) of width w between two centre points."""
    return path_to_d(ST(seg(x1, y1, x2, y2), w, "round", "round"))


# ============================================================================ cash and coins

@icon("money-bag", CAT, "Cloth money sack tied at the neck with a dollar sign on its belly",
      tags=["money sack", "sack of money", "loot", "wealth", "funds", "cash bag"])
def _(S):
    r = L(S, 0, 1.5)
    d = ("M10.5 7.5" + soft((10.5, 7.5), (8.5, 3), (15.5, 3), r) + soft((8.5, 3), (15.5, 3), (13.5, 7.5), r)
         + "L13.5 7.5C18.2 9.6 20.5 13.2 20.5 16.5C20.5 19.5 18.5 21 15.5 21H8.5C5.5 21 3.5 19.5 3.5 16.5"
         "C3.5 13.2 5.8 9.6 10.5 7.5Z")
    return [shell(d), line(seg(8.5, 7.5, 15.5, 7.5)), *dollar(12, 14.75, 0.95)]


@icon("cash-bundle", CAT, "Stack of banknotes with a paper band wrapped round the middle",
      tags=["bundle of cash", "wad", "stack of money", "banknotes", "bankroll", "brick of cash"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 10, rr(S, 2.5))),
        dot(6.25, 8, 1.25), dot(17.75, 8, 1.25),
        line(poly([(2.5, 15), (2.5, 16.5), (21.5, 16.5), (21.5, 15)], r=S.r * 0.5)),
        line(poly([(2.5, 18.5), (2.5, 20), (21.5, 20), (21.5, 18.5)], r=S.r * 0.5)),
        mark(rect(10.25, 2, 3.5, 19, L(S, 0, 0.75))),
    ]


@icon("cash-briefcase", CAT, "Briefcase full of cash, marked with a large dollar sign",
      tags=["briefcase of money", "ransom", "payoff", "cash case", "suitcase of cash", "deal"])
def _(S):
    return [
        line(poly([(9, 7), (9, 4), (15, 4), (15, 7)], r=S.r)),
        shell(rect(3, 7, 18, 14, rr(S))),
        *dollar(12, 14, 0.95),
    ]


def _wing():
    return ("M7.5 10.5C6.5 7 4.5 4.8 2 4.5C1.9 6.3 2.3 7.6 3.1 8.5C2.4 9 2.2 9.8 2.4 10.6"
            "C3.2 11.3 4.2 11.6 5.2 11.5C5.3 12.4 6 13.1 7.5 13.5Z")


@icon("money-with-wings", CAT, "Banknote flying away with a feathered wing on each side",
      tags=["flying money", "money flying away", "spending", "expense", "losing money", "cash"])
def _(S):
    n = rect(7, 10.5, 10, 7, rr(S, 2))
    wing = ("M7.5 12.5C6.8 8.5 4.8 5.6 2 5C1.8 7 2.2 8.4 3 9.3C2.3 9.8 2.1 10.7 2.4 11.5"
            "C3.2 12.2 4.3 12.5 5.3 12.4C5.5 13.4 6.3 14.2 7.5 14.5Z")
    k = -10
    wing = move(wing, 0.6, 0.5)
    return [
        shell(rot_d(cut(wing, n, g=2.2), k), stroke_miterlimit="2"),
        shell(rot_d(cut(flip(wing), n, g=2.2), k), stroke_miterlimit="2"),
        shell(rot_d(n, k)), dot(12, 14, 1.25),
    ]


FLAME = ("M16.5 2.5C19 5 20.5 7.3 20.5 9.8A4 4 0 0 1 12.5 9.8C12.5 8.2 13.2 7 14.3 6C14.5 7 15 7.7 15.7 8"
         "C15.5 6.2 15.8 4.3 16.5 2.5Z")


@icon("burning-money", CAT, "Banknote with a flame burning at its corner and a wisp of smoke",
      tags=["money to burn", "wasting money", "burn rate", "loss", "expense", "cash on fire"])
def _(S):
    n = rect(3, 11, 15, 9, rr(S, 2.5))
    return [
        shell(cut(n, FLAME, g=3)),
        detail(circle(8.5, 15.5, 1.75)),
        shell(FLAME if S.name == "line" else FLAME.replace("M16.5 2.5C19 5", "M16.5 2.5Q16.8 2.6 17.1 3.1C19.2 5.4")),
        line("M7 2.5C5.8 4 8.2 5.5 7 7.5"),
    ]


@icon("money-tree", CAT, "Potted tree whose branches carry coins instead of leaves",
      tags=["money grows", "investment growth", "passive income", "wealth", "prosperity", "returns"])
def _(S):
    return [
        shell(poly([(7.5, 16.5), (16.5, 16.5), (15, 21.5), (9, 21.5)], closed=True, r=S.r)),
        line(poly([(12, 16.5), (12, 8)], r=S.r)),
        line(poly([(12, 13.5), (8.5, 11.5)], r=S.r)),
        line(poly([(12, 12), (15.5, 10)], r=S.r)),
        *coin(S, 5.5, 10, 2.5, False), *coin(S, 18.5, 8.5, 2.5, False), *coin(S, 12, 4.5, 2.5, False),
    ]


CLOUD_SMALL = "M6.5 11H17A3.2 3.2 0 0 0 17.4 4.6A4.8 4.8 0 0 0 8.3 5.3A2.9 2.9 0 0 0 6.5 11Z"
CLOUD_SMALL_LINE = "M4.5 11H19.3A3.2 3.2 0 0 0 17.6 5A4.8 4.8 0 0 0 8.1 5.6A2.8 2.8 0 0 0 4.5 11Z"


@icon("money-rain", CAT, "Small cloud with a banknote and coins falling from it",
      tags=["raining money", "cash rain", "windfall", "bonus", "money shower", "jackpot"])
def _(S):
    return [
        shell(CLOUD_SMALL_LINE if S.name == "line" else CLOUD_SMALL),
        *coin(S, 5.5, 17.5, 2.25, False),
        shell(rot_d(rect(9.5, 14.5, 5.5, 7, rr(S, 1.5)), -15, 12.25, 18)),
        *coin(S, 18.5, 16, 2.25, False),
    ]


@icon("money-pit", CAT, "Dark hole in the ground with coins tumbling down into it",
      tags=["sinking money", "money sink", "bad investment", "waste", "loss", "black hole"])
def _(S):
    return [
        shell(ellipse(12, 18, 9, 3.5)),
        solid(ellipse(12, 18.3, 5.5, 1.4)),
        *coin(S, 11, 9, 3.5),
        *coin(S, 18.5, 4, 2, False),
        line(seg(4.5, 7, 4.5, 10.5)), line(seg(17, 9.5, 17, 12.5)),
    ]


def _magnet_pts(pts, origin=(8, 8)):
    return [(origin[0] + x * 0.7071 - y * 0.7071, origin[1] + x * 0.7071 + y * 0.7071) for x, y in pts]


@icon("money-magnet", CAT, "Horseshoe magnet pulling coins toward its poles",
      tags=["attract money", "attract customers", "lead magnet", "wealth", "income", "magnet"])
def _(S):
    n = 24
    arc_pts = [(5 * math.cos(math.radians(90 + 180 * i / n)), 5 * math.sin(math.radians(90 + 180 * i / n))) for i in range(n + 1)]
    centre = [(5.5, 5)] + arc_pts + [(5.5, -5)]
    band = path_to_d(ST(poly(_magnet_pts(centre)), 4, "butt", "miter"))
    return [
        shell(band),
        detail(poly(_magnet_pts([(3, -7), (3, -3)]))), detail(poly(_magnet_pts([(3, 3), (3, 7)]))),
        *coin(S, 17.5, 14.5, 2.25, False), *coin(S, 14.5, 19.5, 2.25, False),
    ]


@icon("cash-flow", CAT, "Coin circled by two curved arrows chasing each other",
      tags=["cashflow", "money flow", "circulation", "revenue cycle", "working capital", "finance"])
def _(S):
    return [
        *coin(S, 12, 12, 4),
        line(arc(12, 12, 8.5, 200, 325)), arrowhead(S, polar(12, 12, 8.5, 330), 330 + 90, 2.25),
        line(arc(12, 12, 8.5, 20, 145)), arrowhead(S, polar(12, 12, 8.5, 150), 150 + 90, 2.25),
    ]


MOTH = ("M17 6C15.5 3.5 13.2 2 11 2.2C11.2 4.5 12.6 6.2 14.6 6.8C13.6 7.6 13.2 8.6 13.5 9.6"
        "C15 9.6 16.4 8.6 17 7.3C17.6 8.6 19 9.6 20.5 9.6C20.8 8.6 20.4 7.6 19.4 6.8C21.4 6.2 22.8 4.5 23 2.2"
        "C20.8 2 18.5 3.5 17 6Z")


@icon("empty-wallet", CAT, "Open empty wallet with a moth fluttering out",
      tags=["broke", "no money", "empty purse", "out of cash", "poor", "insufficient funds"])
def _(S):
    return [
        shell(rect(2.5, 12, 18, 9.5, rr(S, 3))),
        detail(poly([(20.5, 14.75), (16, 14.75), (16, 18.75), (20.5, 18.75)], r=S.r * 0.5)),
        mark(move(MOTH, -1.5, 0)),
    ]


@icon("donation-box", CAT, "Donation box with a heart on the front and a coin dropping into the slot on top",
      tags=["donate", "donation", "charity box", "give", "contribution", "collection box"])
def _(S):
    return [
        *coin(S, 12, 4.5, 2.5, False),
        shell(rect(3, 9.5, 18, 12, rr(S, 2.5))),
        mark(heart(12, 17, 3)),
    ]


@icon("charity-collection-tin", CAT, "Round collection tin with a coin slot in the lid and a heart label",
      tags=["collection tin", "charity tin", "donation can", "fundraiser", "donate", "coin can"])
def _(S):
    bottom = ellipse(12, 19, 7, 2.5) if S.name == "rounded" else rect(5, 16, 14, 5.5)
    body = union(ellipse(12, 6, 7, 3), rect(5, 6, 14, 13), bottom)
    return [
        shell(body),
        detail("M5 6A7 3 0 0 0 19 6"),
        mark(rect(10, 4.6, 4, 1.5, L(S, 0, 0.75))),
        mark(heart(12, 14, 3.2)),
    ]


@icon("crowdfunding", CAT, "Group of three people with a large coin above them",
      tags=["crowd funding", "crowdsourcing", "backers", "pledge", "community funding", "fundraise"])
def _(S):
    front_body = "M7.5 21.5A4.5 4.5 0 0 1 16.5 21.5Z" if S.name == "line" else "M9 21.5H15A1.5 1.5 0 0 0 16.5 20A4.5 4.5 0 0 0 7.5 20A1.5 1.5 0 0 0 9 21.5Z"
    side_l = "M1.5 21.5A3.75 3.75 0 0 1 9 21.5Z"
    side_r = "M15 21.5A3.75 3.75 0 0 1 22.5 21.5Z"
    return [
        shell(circle(12, 13.5, 2.25)), shell(front_body),
        shell(cut(circle(5.25, 14.5, 1.75), circle(12, 13.5, 2.25), front_body, g=2.2)),
        shell(cut(circle(18.75, 14.5, 1.75), circle(12, 13.5, 2.25), front_body, g=2.2)),
        shell(cut(side_l, front_body, g=2.2)), shell(cut(side_r, front_body, g=2.2)),
        *coin(S, 12, 5.25, 3),
    ]


@icon("coin-sorter", CAT, "Coin sorting machine with a hopper on top and four coin tubes of different widths",
      tags=["coin counter", "coin sorting", "change sorter", "coin machine", "bank", "counting coins"])
def _(S):
    body = union(rect(3, 8.5, 18, 5.5, rr(S, 2)), poly([(5, 2.5), (19, 2.5), (15, 8.5), (9, 8.5)], closed=True))
    return [
        shell(body),
        detail(seg(9, 11.25, 15, 11.25)),
        *[mark(rect(x, y, w, 21.5 - y, L(S, 0, 0.6))) for x, w, y in ((3.5, 2, 18), (7.5, 2.5, 17), (12, 3, 16.5), (17, 3.5, 16))],
    ]


@icon("cash-drawer", CAT, "Open till drawer seen from above with note compartments and a row of coin cups",
      tags=["till drawer", "cash register drawer", "money drawer", "cash tray", "point of sale", "till"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 14, rr(S, 2.5))),
        detail(seg(2.5, 11.5, 21.5, 11.5)),
        detail(seg(9, 3, 9, 11.5)), detail(seg(15, 3, 15, 11.5)),
        *[dot(x, 14.25, 1.1) for x in (6, 10, 14, 18)],
        shell(rect(2, 19, 20, 2.5, L(S, 0, 1.25))),
    ]


def _pig(S):
    body = ellipse(11, 11, 7.5, 5.5)
    snout = rect(17, 8.5, 4, 5, L(S, 0, 1.5))
    ear = poly([(11.5, 6.5), (14, 2.5), (16, 7)], closed=True)
    return union(body, snout, ear)


@icon("broken-piggy-bank", CAT, "Piggy bank split in two by a jagged crack with coins spilling out below",
      tags=["broken savings", "smashed piggy bank", "savings spent", "financial loss", "emergency fund", "piggy"])
def _(S):
    zig = path_to_d(ST(poly([(11.5, 1.5), (13.5, 6), (10.5, 9), (13, 12.5), (11, 17.5)]), 2.75, "butt", "miter"))
    return [
        shell(minus(_pig(S), zig)),
        dot(16.75, 10.5, 1),
        mark(ellipse(9, 20.5, 3.25, 1.1)), mark(ellipse(16.5, 19.25, 2.5, 1)),
    ]


SACK_SMALL = ("M6.5 5L5.5 2.5H9.5L8.5 5C10.5 6 11.5 7.5 11.5 9.2C11.5 10.8 10.5 11.5 9 11.5H6"
              "C4.5 11.5 3.5 10.8 3.5 9.2C3.5 7.5 4.5 6 6.5 5Z")
JUG = ("M15.5 12.5H18.5V14.2C20.3 15 21.5 16.4 21.5 18.2C21.5 20.2 20 21.5 18 21.5H16"
       "C14 21.5 12.5 20.2 12.5 18.2C12.5 16.4 13.7 15 15.5 14.2Z")


@icon("barter", CAT, "Sack of grain and a jug with two curved arrows swapping them",
      tags=["trade", "swap goods", "exchange", "bartering", "trade goods", "goods for goods"])
def _(S):
    return [
        shell(SACK_SMALL, stroke_miterlimit="2"),
        shell(JUG),
        line(poly([(14, 4.5), (17, 4.5), (19, 6.5), (19, 9)], r=S.r * 1.5)), arrowhead(S, (19, 10), 90, 2),
        line(poly([(10, 19.5), (7, 19.5), (5, 17.5), (5, 15)], r=S.r * 1.5)), arrowhead(S, (5, 14), -90, 2),
    ]


@icon("uv-currency-detector", CAT, "Small lamp box shining rays down onto a banknote to check it",
      tags=["counterfeit detector", "uv lamp", "fake money checker", "banknote checker", "forgery", "money tester"])
def _(S):
    return [
        shell(poly([(3, 7.5), (5, 3), (19, 3), (21, 7.5)], closed=True, r=S.r * 0.6)),
        line(seg(8, 10, 7.5, 11.5)), line(seg(12, 10, 12, 11.5)), line(seg(16, 10, 16.5, 11.5)),
        *note(S, 4, 14, 16, 7.5),
    ]


def _square_coin_filled():
    return D(U(P(circle(12, 12, 10))), P(rect(8.5, 8.5, 7, 7)), P(circle(12, 6, 1)), P(circle(12, 18, 1)),
             P(circle(6, 12, 1)), P(circle(18, 12, 1)))


@icon("square-holed-coin", CAT, "Round coin with a square hole through the middle and four marks around it",
      tags=["chinese coin", "cash coin", "ancient coin", "holed coin", "lucky coin", "feng shui"],
      filled=_square_coin_filled)
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(rect(9.5, 9.5, 5, 5, L(S, 0, 1))),
        dot(12, 6, 1), dot(12, 18, 1), dot(6, 12, 1), dot(18, 12, 1),
    ]


@icon("bimetallic-coin", CAT, "Two-metal coin with an outer ring around a separate inner disc marked with a number",
      tags=["two tone coin", "bimetal coin", "coin ring", "euro coin", "pound coin", "currency"])
def _(S):
    return [
        shell(circle(12, 12, 9)),
        detail(circle(12, 12, 5.5)),
        detail(poly([(10.5, 10.25), (12.5, 8.75), (12.5, 15.5)], r=S.r * 0.4)),
    ]


@icon("sycee-ingot", CAT, "Boat-shaped ingot with curled ends and a rounded dome in the middle",
      tags=["yuanbao", "gold ingot", "chinese ingot", "lunar new year", "prosperity", "treasure"])
def _(S):
    boat = ("M2.5 8C4.5 9.5 6.5 11 12 11C17.5 11 19.5 9.5 21.5 8C21.5 13.5 19 19 15 19H9C5 19 2.5 13.5 2.5 8Z"
            if S.name == "line" else
            "M3 8.2C5 9.6 6.8 11 12 11C17.2 11 19 9.6 21 8.2Q21.5 8 21.5 8.6C21.3 13.8 18.8 19 15 19H9"
            "C5.2 19 2.7 13.8 2.5 8.6Q2.5 8 3 8.2Z")
    dome = "M8 11A4 4 0 0 1 16 11Z"
    return [shell(union(boat, dome)), detail("M5.5 13.5C8 14.8 16 14.8 18.5 13.5")]


@icon("money-printer", CAT, "Printing machine with two rollers feeding out a sheet of banknotes",
      tags=["printing money", "money printing", "quantitative easing", "currency press", "print cash", "mint"])
def _(S):
    return [
        line(poly([(7, 6), (7, 2.5), (17, 2.5), (17, 6)], r=S.r)),
        shell(rect(3, 6, 18, 8.5, rr(S, 2.5))),
        detail(seg(3, 10.25, 21, 10.25)),
        dot(7, 12.25, 0.9), dot(17, 12.25, 0.9),
        shell(rect(5.5, 16.5, 13, 5.5, rr(S, 1.5))),
        dot(12, 19.25, 1.25),
    ]


@icon("loan-shark", CAT, "Shark fin cutting through the water next to a floating coin",
      tags=["predatory lending", "usury", "illegal lender", "payday loan", "debt trap", "extortion"])
def _(S):
    fin = ("M2.5 15.5C4.5 10 8 5.5 13.5 4C11 7 10.5 11.5 13 15.5Z" if S.name == "line" else
           "M3.3 15.5C5.3 10.2 8.5 6 12.8 4.3Q13.6 4.1 13.1 4.8C11 7.6 10.8 11.6 12.6 14.9Q12.9 15.5 12.2 15.5Z")
    return [
        shell(fin),
        *coin(S, 18.5, 11.5, 3),
        line("M2 19.5Q4.5 17.5 7 19.5T12 19.5T17 19.5T22 19.5"),
    ]


@icon("pawn-ticket", CAT, "Paper pawn ticket with a string through a hole at one end, a perforation line and a numbered stub",
      tags=["pawn shop ticket", "pawn receipt", "claim ticket", "pledge ticket", "stub", "pawnshop"])
def _(S):
    return [
        shell(minus(rect(3.5, 8, 17, 11.5, rr(S, 2.5)), circle(13.25, 8, 1.75), circle(13.25, 19.5, 1.75))),
        dot(7.5, 13.75, 1.25),
        line("M7.5 13.75C3.5 11.5 3 6 7.5 3"),
        *[dot(13.25, y, 0.85) for y in (11.5, 13.75, 16)],
        detail(seg(16.25, 11.5, 18.25, 11.5)), detail(seg(16.25, 16, 18.25, 16)),
    ]


def _cow(S):
    body = rect(2.5, 9, 14.5, 7.5, L(S, 1, 2.5))
    head = rect(15.5, 6.5, 6, 8, L(S, 1, 2.5))
    return union(body, head)


@icon("cash-cow", CAT, "Cow in profile with spots, horns and an udder, a coin dropping onto its back",
      tags=["profit maker", "revenue stream", "moneymaker", "steady income", "profitable product", "cow"])
def _(S):
    return [
        shell(_cow(S)),
        *coin(S, 8, 3.75, 2.25, False),
        line(seg(5, 16.5, 5, 21)), line(seg(13, 16.5, 13, 21)),
        line(seg(17.5, 6.5, 17, 4)),
        mark(ellipse(7.5, 12.5, 2.25, 1.5)),
        mark(ellipse(9, 18, 1.6, 1.25)),
        dot(19.5, 10, 0.9),
    ]


# ============================================================================ banking

@icon("checkbook", CAT, "Checkbook lying open with a check on top and a stub column on the left",
      tags=["chequebook", "check book", "cheque book", "bank checks", "write a check", "payment"],
      aliases=["chequebook"])
def _(S):
    return [
        shell(rect(2, 4.5, 20, 12.5, rr(S, 2.5))),
        detail(seg(7.5, 4.5, 7.5, 17)),
        detail(seg(10.5, 8.5, 15.5, 8.5)),
        detail("M11 13.5C12 11.8 13 11.8 13.5 13C14 14.2 15 14.2 16 12.8"),
        line(poly([(2, 18.5), (2, 20.5), (22, 20.5), (22, 18.5)], r=S.r * 0.5)),
        dot(4.75, 8.5, 1), dot(4.75, 12.75, 1),
    ]


@icon("teller-window", CAT, "Bank counter window with vertical grille bars, a small arched opening and a pen on the counter",
      tags=["bank teller", "cashier window", "bank counter", "teller", "banking hall", "service window"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 15, rr(S, 2))),
        *[detail(seg(x, 2.5, x, 11)) for x in (7.75, 12, 16.25)],
        detail("M8.5 17.5V14.5A3.5 3.5 0 0 1 15.5 14.5V17.5" if S.name == "rounded" else "M8.5 17.5V12.5H15.5V17.5"),
        line(seg(2, 20.5, 22, 20.5)),
    ]


@icon("pawnbroker-sign", CAT, "Bracket bar with three balls hanging below it; the pawnbroker's sign",
      tags=["pawn shop", "pawnshop", "pawnbroker", "three balls", "shop sign", "loan shop"])
def _(S):
    return [
        line(poly([(3, 2), (3, 7)])), line(seg(3, 4, 21, 4)),
        line(seg(7.5, 4, 7.5, 7.5)), line(seg(16.5, 4, 16.5, 7.5)),
        shell(circle(7.5, 11, 2.5)), shell(circle(16.5, 11, 2.5)), shell(circle(12, 18.75, 2.5)),
    ]


@icon("mobile-check-deposit", CAT, "Phone held sideways with its camera screen framing a paper check beside a shutter button",
      tags=["mobile deposit", "remote deposit", "deposit check", "scan check", "cheque deposit", "banking app"])
def _(S):
    return [
        shell(rect(2, 5.5, 20, 13, rr(S, 2.5))),
        detail(rect(5, 8.5, 11, 7, L(S, 0, 1))),
        detail("M7.5 13.25C8.25 11.25 9.25 11.25 9.75 12.75C10.25 14.25 11.25 14.25 12.5 12"),
        detail(circle(19, 12, 1.25)),
    ]


def _mini_bank(S, x):
    return [
        shell(poly([(x - 3.5, 14.5), (x - 3.5, 13.5), (x, 11.5), (x + 3.5, 13.5), (x + 3.5, 14.5)], closed=True, r=S.r * 0.4)),
        line(seg(x - 2, 16.5, x - 2, 19)), line(seg(x + 2, 16.5, x + 2, 19)),
        line(seg(x - 3.5, 21, x + 3.5, 21)),
    ]


@icon("wire-transfer", CAT, "Long arrow arcing from one bank building to another",
      tags=["bank transfer", "wire", "send money", "interbank transfer", "payment"])
def _(S):
    return [
        *_mini_bank(S, 5.5), *_mini_bank(S, 18.5),
        line(arc(12, 11.5, 7, 200, 335)), arrowhead(S, polar(12, 11.5, 7, 340), 340 + 100, 2.25),
    ]


@icon("money-remittance", CAT, "Globe with a banknote travelling over its top along a curved arrow",
      tags=["remittance", "send money abroad", "international transfer", "money transfer", "overseas payment", "global payment"])
def _(S):
    n = rect(8.5, 2.5, 7, 4.5, L(S, 0.5, 1.5))
    return [
        shell(circle(12, 16, 5.5)),
        detail(seg(6.5, 16, 17.5, 16)), detail(ellipse(12, 16, 2.25, 5.5)),
        line(arc(12, 14, 9, 195, 245)),
        line(arc(12, 14, 9, 295, 335)), arrowhead(S, polar(12, 14, 9, 340), 340 + 100, 2.25),
        shell(n), dot(12, 4.75, 1),
    ]


def _phone(S, x, y, w, h):
    return shell(rect(x, y, w, h, rr(S, 2)))


@icon("p2p-payment", CAT, "Two smartphones with a coin passing between them along a curved arrow",
      tags=["peer to peer payment", "send money", "pay a friend", "mobile transfer", "money app", "instant payment"])
def _(S):
    return [
        _phone(S, 2.5, 11, 7, 10.5), detail(seg(5, 18.5, 7, 18.5)),
        _phone(S, 14.5, 11, 7, 10.5), detail(seg(17, 18.5, 19, 18.5)),
        line(arc(12, 11, 7.5, 200, 243)), line(arc(12, 11, 7.5, 297, 333)),
        arrowhead(S, polar(12, 11, 7.5, 338), 338 + 100, 2),
        *coin(S, 12, 3.75, 2.25, False),
    ]


@icon("emv-chip", CAT, "Payment card chip: a rounded square of six contact pads",
      tags=["card chip", "chip card", "smart card", "chip and pin", "contact chip", "credit card chip"])
def _(S):
    return [
        shell(rect(3, 4.5, 18, 15, rr(S, 3))),
        detail(seg(9, 4.5, 9, 19.5)), detail(seg(15, 4.5, 15, 19.5)),
        detail(seg(3, 9.5, 9, 9.5)), detail(seg(3, 14.5, 9, 14.5)),
        detail(seg(15, 9.5, 21, 9.5)), detail(seg(15, 14.5, 21, 14.5)),
    ]


@icon("card-swipe", CAT, "Payment card sliding through the slot of a swipe reader with motion lines",
      tags=["swipe card", "magstripe reader", "card reader", "swipe to pay", "magnetic stripe", "payment"])
def _(S):
    reader = rect(2.5, 15, 19, 6, rr(S, 2))
    card = rot_d(rect(8, 3, 11, 15, rr(S, 2)), 20, 13.5, 10.5)
    return [
        shell(reader), detail(seg(6, 18, 18, 18)),
        shell(cut(card, reader, g=2.2)),
        detail(rot_d(seg(10.5, 3, 10.5, 12), 20, 13.5, 10.5)),
        line(seg(2.5, 6, 5.5, 6)), line(seg(2.5, 10, 4.5, 10)),
    ]


def _bead_curve(p0, c, p1, n):
    out = []
    for i in range(n):
        t = i / (n - 1)
        out.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1]))
    return out


@icon("chained-pen", CAT, "Counter pen standing in a small base with a bead chain looping down to it",
      tags=["bank pen", "counter pen", "pen on a chain", "tethered pen", "sign here", "reception desk"])
def _(S):
    k = L(S, 0, 1.2)
    pen = poly([(14.5, 3), (18, 3), (18, 13), (16.25, 16), (14.5, 13)], closed=True, r=k)
    pen = rot_d(pen, 20, 16.25, 16)
    beads = _bead_curve((13, 4.5), (2.5, 6), (6.5, 18), 6)
    return [
        shell(rect(10, 18.5, 11.5, 3, rr(S, 1.5))),
        shell(pen),
        *[dot(x, y, 0.9) for x, y in beads],
    ]


@icon("seed-phrase", CAT, "Recovery card with numbered blank slots for a wallet seed phrase",
      tags=["recovery phrase", "mnemonic", "backup phrase", "secret words", "wallet backup", "crypto wallet"])
def _(S):
    parts = [shell(rect(2.5, 4, 19, 16, rr(S, 2.5)))]
    for y in (8, 12, 16):
        for x in (5.5, 13.5):
            parts += [dot(x, y, 1), detail(seg(x + 2, y, x + 5.5, y))]
    return parts


@icon("coin-mining", CAT, "Pickaxe swinging down onto a large coin with small chips flying off",
      tags=["crypto mining", "mining", "proof of work", "mine coins", "blockchain", "miner"])
def _(S):
    H = (9.5, 9.5)
    ux, uy = 0.7071, 0.7071
    nx, ny = 0.7071, -0.7071
    a = (H[0] + nx * 7.5 - ux * 1.5, H[1] + ny * 7.5 - uy * 1.5)
    b = (H[0] - nx * 7.5 - ux * 1.5, H[1] - ny * 7.5 - uy * 1.5)
    c1 = (H[0] + ux * 6.5, H[1] + uy * 6.5)
    c2 = (H[0] + ux * 1.5, H[1] + uy * 1.5)
    headd = (f"M{fmt(a[0])} {fmt(a[1])}Q{fmt(c1[0])} {fmt(c1[1])} {fmt(b[0])} {fmt(b[1])}"
             f"Q{fmt(c2[0])} {fmt(c2[1])} {fmt(a[0])} {fmt(a[1])}Z")
    handle = path_to_d(ST(seg(2.5, 2.5, H[0], H[1]), 2.5, S.cap, S.join))
    return [
        *coin(S, 17, 17, 4.5),
        shell(headd, stroke_miterlimit="2"),
        shell(handle),
        dot(21, 10.5, 0.9), dot(10.5, 21, 0.9),
    ]


@icon("qr-payment", CAT, "Smartphone showing a QR code with a coin beside it",
      tags=["scan to pay", "qr code payment", "mobile payment", "contactless", "pay by phone", "qr pay"])
def _(S):
    c = circle(18, 17.5, 3.5)
    return [
        shell(cut(rect(3, 2.5, 12, 19, rr(S, 2.5)), c, g=3)),
        *[sq(x, y, 2.5, 2.5, L(S, 0, 0.6)) for x, y in ((5.5, 5), (10, 5), (5.5, 9.5))],
        sq(10.25, 9.75, 2, 2),
        *coin(S, 18, 17.5, 3.5),
    ]


@icon("online-payment", CAT, "Browser window with a payment card on the page and a pay button below",
      tags=["web payment", "online checkout", "pay online", "ecommerce payment", "card payment", "internet banking"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, rr(S, 2.5))),
        detail(seg(2, 7, 22, 7)),
        detail(rect(6, 9.5, 12, 6.5, L(S, 0, 1.25))),
        detail(seg(6, 12, 18, 12)),
        mark(rect(8.5, 17.75, 7, 1.5, L(S, 0, 0.75))),
    ]


# ============================================================================ payments and rates

@icon("installment-payment", CAT, "Coin inside a ring split into four segments with the first segment filled in",
      tags=["pay in installments", "instalment", "buy now pay later", "payment plan", "pay in 4", "split payment"])
def _(S):
    gap = 14
    segs = [arc(12, 12, 8.5, -90 + gap / 2 + 90 * i, -90 - gap / 2 + 90 * (i + 1)) for i in range(4)]
    first = path_to_d(ST(segs[0], 3.5, S.cap, S.join))
    return [
        *coin(S, 12, 12, 4),
        shell(first),
        *[line(d) for d in segs[1:]],
    ]


@icon("split-bill", CAT, "Long receipt cut down the middle by a dashed line with a coin on each half",
      tags=["split the bill", "split check", "go dutch", "share costs", "divide bill", "group payment"])
def _(S):
    zig = [(20, 21.5)]
    for i in range(4):
        x = 20 - 4 * i
        zig += [(x - 2, 19.5), (x - 4, 21.5)]
    body = poly([(4, 2.5), (20, 2.5)] + zig, closed=True, r=S.r * 0.3)
    return [
        shell(body, stroke_miterlimit="2"),
        *[dot(12, y, 0.85) for y in (5, 8.25, 11.5, 14.75)],
        detail(seg(6.5, 6, 9.5, 6)), detail(seg(14.5, 6, 17.5, 6)),
        *coin(S, 8, 13, 1.75, False), *coin(S, 16, 13, 1.75, False),
    ]


@icon("cashback", CAT, "Coin inside a single circular arrow that loops back around it",
      tags=["cash back", "money back", "rebate", "refund", "reward", "cashback offer"])
def _(S):
    return [
        *coin(S, 12, 12, 4.5),
        line(arc(12, 12, 8.5, -60, 225)), arrowhead(S, polar(12, 12, 8.5, -60), -60 - 90 + 180 + 180, 2.5),
    ]


@icon("credit-score", CAT, "Half circle gauge in three segments with a needle, above a small payment card",
      tags=["credit rating", "credit report", "credit check", "score meter", "creditworthiness"])
def _(S):
    return [
        line(arc(12, 12, 8.5, 180, 235)), line(arc(12, 12, 8.5, 245, 295)), line(arc(12, 12, 8.5, 305, 360)),
        line(seg(12, 12, 16.5, 7)), dot(12, 12, 1.75),
        shell(rect(6, 16, 12, 5.5, rr(S, 1.5))),
    ]


@icon("interest-rate", CAT, "Coin with a percent sign on its face and an up arrow beside it",
      tags=["interest", "rate", "apr", "percentage rate", "savings rate", "loan rate"])
def _(S):
    return [
        shell(circle(9.5, 13, 7)),
        *percent(S, 9.5, 13, 1.0),
        line(seg(19.5, 20.5, 19.5, 4)), arrowhead(S, (19.5, 3.5), -90, 2.5),
    ]


@icon("currency-exchange-booth", CAT, "Small kiosk with a service window under a board of exchange rate rows",
      tags=["bureau de change", "money changer", "exchange booth", "forex kiosk", "currency kiosk", "travel money"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 8.5, rr(S, 1.5))),
        dot(5.5, 5, 0.9), detail(seg(7.5, 5, 18.5, 5)),
        dot(5.5, 8.5, 0.9), detail(seg(7.5, 8.5, 18.5, 8.5)),
        line(poly([(4.5, 21.5), (4.5, 13), (19.5, 13), (19.5, 21.5)], r=S.r * 0.6)),
        line(poly([(8, 21.5), (8, 16), (16, 16), (16, 21.5)], r=S.r * 0.6)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("live-shopping", CAT, "Smartphone showing a presenter on screen with a shopping bag beside it and a live dot",
      tags=["live commerce", "livestream shopping", "shoppable video", "live sale", "social selling", "stream shop"])
def _(S):
    bag = rect(13.5, 12, 8, 9.5, rr(S, 1.5))
    phone = rect(2.5, 2.5, 12, 19, rr(S, 2.5))
    return [
        shell(cut(phone, bag, g=2.2)),
        dot(5.5, 5.5, 1.25),
        detail(circle(8.5, 9.5, 2)),
        detail("M5.5 16A3 3 0 0 1 11.5 16"),
        shell(bag),
        line("M15.5 12V10.5A2 2 0 0 1 19.5 10.5V12"),
    ]


@icon("dividend", CAT, "Pie with one wedge lifted out and a coin sitting on that wedge",
      tags=["dividends", "shareholder payout", "profit share", "yield", "income", "stock payout"])
def _(S):
    c, r = (10, 14), 7.5
    pie = (f"M{fmt(c[0])} {fmt(c[1])}L{fmt(c[0])} {fmt(c[1] - r)}A{r} {r} 0 1 0 {fmt(c[0] + r)} {fmt(c[1])}Z")
    o = (2.5, -2.5)
    wedge = (f"M{fmt(c[0] + o[0])} {fmt(c[1] + o[1])}L{fmt(c[0] + r + o[0])} {fmt(c[1] + o[1])}"
             f"A{r} {r} 0 0 0 {fmt(c[0] + o[0])} {fmt(c[1] - r + o[1])}Z")
    return [
        shell(pie, stroke_miterlimit="2"),
        shell(wedge, stroke_miterlimit="2"),
        *coin(S, 18.5, 4.5, 2.25, False),
    ]


@icon("inflation", CAT, "Round balloon inflating with a price tag hanging from its string",
      tags=["rising prices", "cost of living", "price increase", "inflation rate", "cpi", "economy"])
def _(S):
    tag = poly([(17.5, 14.5), (20, 17), (20, 22), (15, 22), (15, 17)], closed=True, r=S.r * 0.5)
    return [
        shell(ellipse(9.5, 8, 6.5, 6.25) if S.name == "rounded" else
              "M9.5 14.25C5.5 13 3 10.8 3 8A6.5 6.25 0 0 1 16 8C16 10.8 13.5 13 9.5 14.25Z"),
        detail(arc(9.5, 8, 3.5, 200, 250)),
        solid(poly([(8.5, 16), (10.5, 16), (9.5, 14)], closed=True)),
        line("M9.5 16C9.5 18.5 12 19.5 15.5 17.5"),
        shell(tag),
        dot(17.5, 17.75, 0.9),
    ]


# ============================================================================ machines and cash handling

@icon("money-roll", CAT, "Banknotes rolled into a cylinder and held with a band, the spiral of the roll visible on one end",
      tags=["roll of cash", "rolled bills", "wad of cash", "bankroll", "cash roll", "rubber band"])
def _(S):
    body = union(ellipse(7, 12, 3.5, 6), rect(7, 6, 10, 12), L(S, rect(17, 6, 3.5, 12), ellipse(17, 12, 3.5, 6)))
    return [
        shell(body),
        detail(ellipse(7, 12, 3.5, 6)),
        dot(7, 12, 1.1),
        detail(seg(14, 6.5, 14, 17.5)),
    ]


@icon("coin-roll", CAT, "Paper-wrapped roll of coins lying on its side with the coin rims showing at the crimped ends",
      tags=["rolled coins", "coin wrapper", "bank coin roll", "change roll", "coins", "rolled change"])
def _(S):
    body = union(rect(5.5, 7, 13, 10, rr(S, 1.5)), rect(2.5, 9, 4, 6, L(S, 0, 1)), rect(17.5, 9, 4, 6, L(S, 0, 1)))
    return [
        shell(body),
        detail(seg(9, 7.5, 9, 16.5)), detail(seg(15, 7.5, 15, 16.5)),
    ]


@icon("fundraising-thermometer", CAT, "Tall goal thermometer with tick marks on both sides, filled most of the way up to the bulb",
      tags=["goal thermometer", "fundraiser progress", "donation goal", "campaign goal", "funding progress", "target tracker"])
def _(S):
    tube = "M9 14.15V5A3 3 0 0 1 15 5V14.15A4.5 4.5 0 1 1 9 14.15Z"
    return [
        shell(tube),
        mark(rect(11, 8.5, 2, 9, L(S, 0, 1))), mark(circle(12, 17.5, 2)),
        *[line(seg(x0, y, x0 + 3, y)) for y in (4.5, 8.5, 12.5) for x0 in (3, 18)],
    ]


@icon("coin-changer", CAT, "Belt-worn coin dispenser with four upright coin tubes side by side and thumb levers on top",
      tags=["coin dispenser", "change dispenser", "bus conductor", "coin holder", "change maker", "coin belt"])
def _(S):
    return [
        shell(rect(3, 10, 18, 11.5, rr(S, 2))),
        *[detail(seg(x, 10, x, 21.5)) for x in (7.5, 12, 16.5)],
        *[line(seg(cx, 10, cx + 1.25, 4.5)) for cx in (5.25, 9.75, 14.25, 18.75)],
        *[dot(cx, 18, 1) for cx in (5.25, 9.75, 14.25, 18.75)],
    ]


@icon("change-machine", CAT, "Upright wall machine with a banknote slot, a small display and a coin cup at the bottom",
      tags=["bill changer", "note changer", "coin exchange machine", "laundromat change", "arcade change", "currency changer"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 2.5))),
        mark(rect(8, 5.5, 8, 1.5, L(S, 0, 0.75))),
        detail(rect(8, 10, 8, 3.5, L(S, 0, 1))),
        mark(rect(8, 16.25, 8, 2.5, L(S, 0, 1))),
    ]


@icon("bank-deposit-bag", CAT, "Flat zipper pouch with a lock tab on the zip and a clear window pocket",
      tags=["money bag", "cash pouch", "night deposit bag", "zippered bank bag", "security bag", "takings bag"])
def _(S):
    return [
        shell(rect(2.5, 5, 19, 14, rr(S, 2.5))),
        detail(seg(2.5, 9.5, 21.5, 9.5)),
        mark(rect(15, 7.25, 4.5, 4.5, L(S, 0, 1))),
        detail(rect(6, 13, 8, 3, L(S, 0, 0.75))),
    ]


@icon("coin-minting-press", CAT, "Screw press with a weighted top bar driving a die down onto a coin blank",
      tags=["mint", "minting", "coin press", "coin stamping", "coin maker", "die strike"])
def _(S):
    return [
        line(seg(4, 4.5, 20, 4.5)), dot(3.5, 4.5, 1.75), dot(20.5, 4.5, 1.75),
        line(seg(12, 4.5, 12, 13)),
        line(poly([(6, 21), (6, 8.5), (18, 8.5), (18, 21)], r=S.r)),
        mark(rect(9, 12.5, 6, 3, L(S, 0, 0.75))),
        mark(rect(8.5, 17.5, 7, 2, L(S, 0, 1))),
        line(seg(3, 21.5, 21, 21.5)),
    ]


@icon("night-deposit-box", CAT, "Wall-mounted deposit chute with a slot above a pull-down drawer handle",
      tags=["night drop", "drop box", "after hours deposit", "deposit chute", "bank drop", "depository"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, rr(S, 2.5))),
        mark(rect(7, 5.25, 10, 1.75, L(S, 0, 0.85))),
        detail(rect(7, 10.5, 10, 7, L(S, 0, 1))),
        mark(rect(9.5, 13, 5, 1.5, L(S, 0, 0.75))),
    ]


@icon("card-imprinter", CAT, "Manual card imprinter with a card on its bed and a sliding roller bar across it",
      tags=["zip zap machine", "knuckle buster", "credit card imprinter", "manual card machine", "card press", "imprint machine"])
def _(S):
    return [
        shell(rect(2.5, 11, 19, 10.5, rr(S, 2.5))),
        detail(rect(5.5, 14, 10, 4.5, L(S, 0, 1))),
        shell(rect(2.5, 3, 15, 5, rr(S, 2))),
        line(seg(17.5, 5.5, 21.5, 5.5)), dot(20, 8.5, 1),
    ]


@icon("mobile-card-reader", CAT, "Smartphone with a small square card reader attached and a card inserted in it",
      tags=["phone card reader", "mobile pos", "card dongle", "tap to pay", "mpos", "pay by phone"])
def _(S):
    reader = rect(13.5, 13.5, 8, 8, rr(S, 1.5))
    return [
        shell(cut(rect(3, 2.5, 11, 19, rr(S, 2.5)), reader, g=2.2)),
        detail(seg(7.5, 18.5, 9.5, 18.5)),
        shell(reader),
        line(poly([(15.5, 13.5), (15.5, 5), (19.5, 5), (19.5, 13.5)], r=S.r * 0.5)),
    ]


# ============================================================================ markets

def tri_up(cx, cy, w, h):
    return poly([(cx - w / 2, cy + h / 2), (cx, cy - h / 2), (cx + w / 2, cy + h / 2)], closed=True)


def tri_down(cx, cy, w, h):
    return poly([(cx - w / 2, cy - h / 2), (cx, cy + h / 2), (cx + w / 2, cy - h / 2)], closed=True)


@icon("bond-certificate", CAT, "Bond certificate with a title line and seal, and a row of tear-off coupons along the bottom",
      tags=["bond", "government bond", "debenture", "fixed income", "coupon", "share certificate"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 2.5))),
        detail(seg(2.5, 15.5, 21.5, 15.5)),
        detail(seg(8.75, 15.5, 8.75, 21.5)), detail(seg(15.25, 15.5, 15.25, 21.5)),
        detail(seg(7.5, 6.25, 16.5, 6.25)),
        dot(12, 10.75, 1.75),
    ]


@icon("stock-exchange", CAT, "Columned exchange building with a ticker board across the top and three columns below",
      tags=["bourse", "stock market", "trading floor", "securities exchange", "wall street", "equity market"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 7, rr(S, 1.5))),
        mark(tri_up(6.5, 6, 3.5, 3)), mark(tri_down(12, 6, 3.5, 3)), mark(rect(15.5, 5.25, 3.5, 1.5, L(S, 0, 0.75))),
        line(seg(6, 12.5, 6, 18.5)), line(seg(12, 12.5, 12, 18.5)), line(seg(18, 12.5, 18, 18.5)),
        line(seg(2.5, 21.5, 21.5, 21.5)),
    ]


@icon("stock-ticker", CAT, "Long horizontal LED strip showing an up triangle, a down triangle and a number block",
      tags=["ticker tape", "price ticker", "market ticker", "stock prices", "quote board", "scrolling quotes"])
def _(S):
    return [
        shell(rect(1.5, 7.5, 21, 9, rr(S, 2.5))),
        mark(tri_up(6, 12, 3.5, 3)), mark(tri_down(11.5, 12, 3.5, 3)), mark(rect(15.5, 11.25, 4, 1.5, L(S, 0, 0.75))),
    ]


def _bull_head(S):
    face = poly([(5, 8), (13, 8), (14.5, 13.5), (12.5, 20), (5.5, 20), (3.5, 13.5)], closed=True, r=L(S, 0, 1.5))
    return face


@icon("bull-market", CAT, "Bull head with forward-curving horns and an up arrow beside it",
      tags=["bullish", "rising market", "stock market rally", "uptrend", "optimism", "market boom"])
def _(S):
    return [
        shell(_bull_head(S)),
        line("M5 8.5C2.5 8.5 2 6 2.5 3.5"), line("M13 8.5C15.5 8.5 16 6 15.5 3.5"),
        dot(6.5, 12.5, 0.95), dot(11.5, 12.5, 0.95),
        mark(ellipse(9, 17, 2.25, 1.1)),
        line(seg(20.5, 20, 20.5, 5)), arrowhead(S, (20.5, 4.5), -90, 2.5),
    ]


@icon("bear-market", CAT, "Bear head with round ears and a down arrow beside it",
      tags=["bearish", "falling market", "stock market decline", "downtrend", "pessimism", "market slump"])
def _(S):
    return [
        shell(union(circle(9, 13.5, 6.5), circle(3.75, 6.5, 2.5), circle(14.25, 6.5, 2.5))),
        dot(6.5, 12.5, 0.95), dot(11.5, 12.5, 0.95),
        detail(ellipse(9, 16.25, 2.25, 1.6)) if S.name == "line" else mark(ellipse(9, 16.25, 2.25, 1.5)),
        line(seg(20.5, 5, 20.5, 20)), arrowhead(S, (20.5, 20.5), 90, 2.5),
    ]


@icon("market-crash", CAT, "Line chart that climbs to a peak and then drops away in a steep plunge",
      tags=["stock crash", "crash", "market collapse", "sell-off", "black monday", "recession"])
def _(S):
    return [
        line(poly([(2.5, 2.5), (2.5, 21.5), (21.5, 21.5)])),
        line(poly([(6, 16.5), (9, 11.5), (11.5, 13.5), (14, 5)], r=S.r * 0.5)),
        line(seg(14, 5, 19, 16.5)), arrowhead(S, (19.75, 18.25), 66, 2.5),
    ]


@icon("market-bubble", CAT, "Soap bubble with a rising line chart inside, popping at its upper edge",
      tags=["bubble", "asset bubble", "speculation", "dot-com bubble", "overvalued", "burst"])
def _(S):
    cx, cy = 10, 14.5
    def burst(a, r0, r1):
        p0, p1 = polar(cx, cy, r0, a), polar(cx, cy, r1, a)
        return line(seg(p0[0], p0[1], p1[0], p1[1]))
    return [
        shell(circle(cx, cy, 7.5)),
        detail(poly([(6, 17.5), (9, 13.5), (11.5, 15.25), (14.5, 11)], r=S.r * 0.5)),
        burst(-75, 10.5, 12.5), burst(-45, 10.5, 12.75), burst(-15, 10.5, 12.5),
    ]


@icon("order-book", CAT, "Two side-by-side columns of horizontal bars growing outward from the centre of a frame",
      tags=["market depth", "bids and asks", "depth chart", "limit orders", "trading book", "level 2"])
def _(S):
    rows = [(5.5, 3, 2.5), (9.5, 5, 4.5), (13.5, 6, 6), (17.5, 7.5, 7.5)]
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 2.5))),
        *[mark(rect(9.5 - a, y, a, 2, L(S, 0, 0.5))) for y, a, b in rows],
        *[mark(rect(14.5, y, b, 2, L(S, 0, 0.5))) for y, a, b in rows],
    ]


@icon("trading-desk", CAT, "Three monitors on a desk, the centre one showing candlestick bars",
      tags=["trader workstation", "multi-monitor setup", "trading station", "broker desk", "day trading", "trading floor"])
def _(S):
    return [
        line(poly([(6, 6.5), (2.5, 6.5), (2.5, 14), (6, 14)], r=S.r * 0.5)),
        line(poly([(18, 6.5), (21.5, 6.5), (21.5, 14), (18, 14)], r=S.r * 0.5)),
        shell(rect(6.5, 3, 11, 11, rr(S, 2))),
        mark(rect(9, 8, 2, 4)), mark(rect(13, 5.5, 2, 5)),
        line(seg(12, 14, 12, 17.5)),
        line(seg(8, 18, 16, 18)),
        line(seg(2.5, 21.5, 21.5, 21.5)),
    ]


@icon("financial-leverage", CAT, "Long lever on a small fulcrum with a tall stack of coins on one end and a single coin on the other",
      tags=["leverage", "gearing", "borrowed money", "margin", "debt financing", "amplify returns"])
def _(S):
    return [
        shell(poly([(8, 17.25), (5, 21.5), (11, 21.5)], closed=True, r=S.r * 0.4)),
        line(seg(2.5, 15.25, 21.5, 19.75)),
        shell(rect(3, 5, 5.5, 8.5, rr(S, 1.5))),
        detail(seg(3, 8.25, 8.5, 8.25)), detail(seg(3, 11, 8.5, 11)),
        *coin(S, 18.5, 14.75, 2.5, False),
    ]


@icon("liquidity", CAT, "Large water drop with a coin floating inside its round lower half",
      tags=["liquid assets", "cash equivalents", "liquidity ratio", "fluid capital", "convertible to cash", "cash on hand"])
def _(S):
    body = ("M12 2.5C9 7 4.5 10.5 4.5 15A7.5 7.5 0 0 0 19.5 15C19.5 10.5 15 7 12 2.5Z" if S.name == "line" else
            "M12.8 3.1Q12 2.2 11.2 3.1C8.5 7.3 4.5 10.8 4.5 15A7.5 7.5 0 0 0 19.5 15C19.5 10.8 15.5 7.3 12.8 3.1Z")
    return [
        shell(body),
        *coin(S, 12, 15, 3.25),
    ]


@icon("angel-investor", CAT, "Coin with a small halo above it and a feathered wing on each side",
      tags=["seed investor", "early stage funding", "startup funding", "business angel", "venture backer", "seed money"])
def _(S):
    wing = move(("M7.5 12.5C6.8 8.5 4.8 5.6 2 5C1.8 7 2.2 8.4 3 9.3C2.3 9.8 2.1 10.7 2.4 11.5"
                 "C3.2 12.2 4.3 12.5 5.3 12.4C5.5 13.4 6.3 14.2 7.5 14.5Z"), 0, 2.5)
    c = circle(12, 14, 5.25)
    return [
        shell(cut(wing, c, g=2.2), stroke_miterlimit="2"),
        shell(cut(flip(wing), c, g=2.2), stroke_miterlimit="2"),
        *coin(S, 12, 14, 5.25),
        line(ellipse(12, 3.75, 3.5, 1.25)),
    ]


@icon("hockey-stick-chart", CAT, "Chart line running flat along the bottom and then curving sharply upward at the right",
      tags=["exponential growth", "j curve", "growth chart", "sudden growth", "startup growth", "take-off"])
def _(S):
    return [
        line(poly([(2.5, 2.5), (2.5, 21.5), (21.5, 21.5)])),
        line("M6.5 17.5H11.5C16 17.5 17.5 13 19.25 5.5"),
        dot(19.25, 5.5, 1.5),
    ]


@icon("bell-curve", CAT, "Smooth symmetrical bell-shaped curve over a baseline with a flat baseline",
      tags=["normal distribution", "gaussian", "standard deviation", "distribution curve", "statistics", "probability"])
def _(S):
    return [
        line("M2.5 18.75C7 18.75 8.5 4.5 12 4.5C15.5 4.5 17 18.75 21.5 18.75"),
        line(seg(2.5, 21.5, 21.5, 21.5)),
    ]


@icon("hype-cycle", CAT, "Curve that spikes to a sharp peak, drops into a trough and then climbs gently to a plateau",
      tags=["adoption curve", "technology adoption", "peak of expectations", "trough of disillusionment", "innovation cycle", "hype curve"])
def _(S):
    return [
        line(poly([(2.5, 2.5), (2.5, 21.5), (21.5, 21.5)])),
        line("M6.5 19L9 5C10 10.5 11.5 16 14 16C16.5 16 17.5 11.5 21.5 11.5"),
    ]


@icon("product-life-cycle", CAT, "Sales curve that rises through launch and growth, levels off at maturity and then declines",
      tags=["product lifecycle", "introduction growth maturity decline", "plc", "sales curve", "lifecycle stages", "market stages"])
def _(S):
    return [
        line(poly([(2.5, 2.5), (2.5, 21.5), (21.5, 21.5)])),
        line("M6 18.5C8 18.5 8.5 7 11.25 7H13.25C16 7 17.5 15.5 20.5 18.5"),
    ]


@icon("tax-brackets", CAT, "Rising staircase of bars with a percent sign above the tallest step",
      tags=["income tax", "tax bands", "tax rates", "progressive tax", "tax tiers", "tax rate table"])
def _(S):
    steps = poly([(2.5, 21.5), (2.5, 18), (8, 18), (8, 14.5), (13.5, 14.5), (13.5, 11), (21.5, 11), (21.5, 21.5)],
                 closed=True, r=S.r * 0.6)
    return [
        shell(steps),
        *percent(S, 17.5, 5.5, 0.8),
    ]
