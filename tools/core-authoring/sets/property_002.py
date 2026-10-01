"""TypeIcon Core: property (batch 2).

Housing, ownership, rental and plot icons drawn from the objects themselves (front, side or plan views).
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "property"


def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


def mark(d) -> Part:
    return Part("dot", d)


def house(S, x0, x1, ytop, ybot, eave=None, k=0.6):
    """Closed house outline: walls x0..x1, roof peak at ytop, eave height, floor at ybot."""
    cx = (x0 + x1) / 2
    e = eave if eave is not None else ytop + (x1 - x0) / 2
    return poly([(x0, ybot), (x0, e), (cx, ytop), (x1, e), (x1, ybot)], closed=True, r=S.r * k)


def roofline(S, x0, x1, ytop, eave, base, k=0.6):
    """Open house: two walls and a roof, no floor."""
    cx = (x0 + x1) / 2
    return poly([(x0, base), (x0, eave), (cx, ytop), (x1, eave), (x1, base)], r=S.r * k)


def head(tip, deg, size=2.25):
    a = polar(tip[0], tip[1], size * math.sqrt(2), deg + 180 - 45)
    b = polar(tip[0], tip[1], size * math.sqrt(2), deg + 180 + 45)
    return [a, tip, b]


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def person(cx, top, bottom, hr=2.0):
    """Standing person: head, torso and legs. Returns parts; the shoulder point is (cx, top + 2 * hr + 1.5)."""
    t0 = top + 2 * hr + 1.2
    mid = t0 + (bottom - t0) * 0.5
    return [shell(circle(cx, top + hr, hr)), line(seg(cx, t0, cx, mid)),
            line(poly([(cx - 2.5, bottom), (cx, mid), (cx + 2.5, bottom)]))]


def outline_region(d, miter=4.0):
    return U(P(d), ST(d, 2.0, "butt", "miter", miter))


def coin_stack(S, x, y, w, n, h=2.5):
    """Stack of n flat coins (rounded bars) with the base at y."""
    return [shell(rect(x, y - h * (i + 1), w, h, min(S.R, h / 2))) for i in range(n)]


# ============================================================================ moving and portfolios

@icon("moving-in", CAT, "Person carrying a box towards an open front door",
      tags=["move in", "moving day", "new home", "carrying box", "relocation", "doorway"])
def _(S):
    return [
        *person(4.5, 3, 21),
        line(seg(4.5, 9.5, 8.5, 12)),
        shell(rect(8.5, 10, 6, 6, rr(S, 1))),
        line(poly([(17, 21), (17, 3.5), (21.5, 3.5), (21.5, 21)])),
    ]


@icon("home-downsizing", CAT, "Large house and a small house with an arrow pointing from big to small",
      tags=["downsize", "smaller home", "scale down", "retirement move", "less space", "moving smaller"])
def _(S):
    return [
        shell(house(S, 2.5, 12, 4, 21, eave=9.5)),
        shell(house(S, 15, 21.5, 13.5, 21, eave=16.5)),
        line("M13.5 4.5H16A3 3 0 0 1 19 7.5V9"),
        line(poly(head((19, 10), 90, 2), r=S.r * 0.5)),
    ]


@icon("house-relocation", CAT, "House carried on a flatbed trailer behind a truck cab",
      tags=["moving a house", "house move", "transport house", "flatbed", "relocate building", "trailer"])
def _(S):
    return [
        shell(house(S, 3, 13.5, 3, 14.5, eave=7.5)),
        line(seg(2, 16.5, 15.5, 16.5)),
        shell(poly([(15.5, 16.5), (15.5, 10.5), (18.5, 10.5), (21.5, 14), (21.5, 16.5)], closed=True, r=S.r * 0.6)),
        shell(circle(7, 19.75, 1.5)), shell(circle(18, 19.75, 1.5)),
    ]


@icon("portable-storage-unit", CAT, "Tall container box with ribbed roll-up door on a driveway beside a house",
      tags=["pod", "moving container", "storage pod", "portable storage", "self storage", "driveway container"])
def _(S):
    return [
        shell(rect(2.5, 5, 11.5, 14, rr(S, 2))),
        detail(seg(2.5, 9.5, 14, 9.5)), detail(seg(2.5, 13, 14, 13)), detail(seg(2.5, 16.5, 14, 16.5)),
        line(roofline(S, 16.5, 21.5, 11, 14.5, 19)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("property-chain", CAT, "Three small houses in a row with interlocked chain links beneath",
      tags=["chain", "buyer chain", "linked sales", "house sale chain", "dependent sales", "housing market"])
def _(S):
    def h(x):
        return solid(poly([(x, 10.5), (x, 6.5), (x + 2.75, 3.5), (x + 5.5, 6.5), (x + 5.5, 10.5)], closed=True))
    return [
        h(2.5), h(9.25), h(16),
        *[line(rect(x, 15.5, 9, 5, L(S, 1.5, 2.5))) for x in (2, 7.5, 13)],
    ]


@icon("property-portfolio", CAT, "Open folder with three houses rising out of it",
      tags=["real estate portfolio", "holdings", "investments", "landlord", "properties owned", "folder"])
def _(S):
    def h(x, w, top, eave):
        return solid(poly([(x, 13), (x, eave), (x + w / 2, top), (x + w, eave), (x + w, 13)], closed=True))
    return [
        shell(rect(2.5, 12.5, 19, 8.5, S.R)),
        h(2.5, 4.5, 5.5, 8), h(9, 6, 2.5, 5.5), h(17, 4.5, 5.5, 8),
    ]


@icon("property-ladder", CAT, "Ladder with a small house on the lower side and a larger house above",
      tags=["getting on the ladder", "first home", "step up", "housing ladder", "upgrade home", "buying"])
def _(S):
    return [
        line(seg(3.5, 3, 3.5, 21)), line(seg(9, 3, 9, 21)),
        line(seg(3.5, 7, 9, 7)), line(seg(3.5, 12, 9, 12)), line(seg(3.5, 17, 9, 17)),
        shell(house(S, 12, 21.5, 3, 10, eave=6)),
        shell(house(S, 12, 17, 15, 21, eave=17.5)),
    ]


@icon("housing-bubble", CAT, "House floating in a round soap bubble with a shine mark",
      tags=["property bubble", "market bubble", "overpriced homes", "housing crash", "speculation", "burst"])
def _(S):
    return [
        shell(circle(12, 12, 9.5)),
        detail(house(S, 8, 16, 8, 17, eave=11.5)),
        line(arc(12, 12, 6.7, 190, 235)),
    ]


@icon("school-catchment-area", CAT, "School at the centre of a dashed circle with small houses inside it",
      tags=["school zone", "school district", "catchment", "enrolment zone", "school boundary", "nearby homes"])
def _(S):
    dashes = [line(arc(12, 12, 9, a, a + 28)) for a in range(0, 360, 45)]

    def h(x, y):
        return solid(poly([(x - 1.5, y + 1.5), (x - 1.5, y - 0.25), (x, y - 1.5), (x + 1.5, y - 0.25), (x + 1.5, y + 1.5)], closed=True))
    return [*dashes, shell(house(S, 9.5, 14.5, 6.5, 16, eave=9.5)), h(5.6, 12.2), h(18.4, 12.2)]


@icon("house-rules", CAT, "Framed notice with a small house at the top and lines of text below",
      tags=["rules of the house", "tenant rules", "house policy", "do and dont", "notice", "guidelines"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 2))),
        detail(poly([(8.5, 10), (8.5, 7.5), (12, 5.5), (15.5, 7.5), (15.5, 10)], closed=True)),
        detail(seg(8, 13.5, 16, 13.5)), detail(seg(8, 16.5, 16, 16.5)), detail(seg(8, 19, 13, 19)),
    ]


@icon("key-envelope", CAT, "Envelope with a window showing a key inside",
      tags=["keys by post", "key handover", "mail keys", "spare key", "key delivery", "envelope"])
def _(S):
    return [
        shell(rect(2, 4.5, 20, 15, rr(S, 2))),
        detail(poly([(5, 8), (19, 8), (19, 16), (5, 16)], closed=True, r=S.r * 1.5)),
        dot(8.5, 12, 1.5), mark(rect(10, 11.25, 6.5, 1.5)), mark(rect(13.5, 11.25, 1.5, 3)),
    ]


@icon("key-tag", CAT, "Key with a round paper tag tied to its bow by a string loop",
      tags=["keyring tag", "property key tag", "label key", "key fob tag", "labelled key", "agent key"])
def _(S):
    return [
        shell(circle(6.5, 6.5, 3.5)),
        line(seg(10, 6.5, 21.5, 6.5)),
        line(seg(17.5, 6.5, 17.5, 10)), line(seg(21, 6.5, 21, 9.5)),
        line("M6.5 10Q6.5 15.5 12 15.5"),
        shell(rect(11.5, 13, 10, 8, rr(S, 3))),
        dot(14.5, 17, 1),
    ]


@icon("mortgage-rate", CAT, "House with a large percent sign inside it",
      tags=["interest rate", "home loan rate", "apr", "lending rate", "percent", "borrowing cost"])
def _(S):
    return [
        shell(house(S, 2.5, 21.5, 2.5, 21.5, eave=10)),
        dot(9.5, 13.5, 1.5), dot(14.5, 18, 1.5),
        mark(poly([(14.2, 12), (15.4, 12.8), (9.8, 19.5), (8.6, 18.7)], closed=True)),
    ]


def _calc_filled():
    body = outline_region(rect(4, 2.5, 16, 19, 3))
    body = D(body, P(rect(7, 5.5, 10, 5)))
    for y in (14, 18):
        for x in (8.5, 12, 15.5):
            body = D(body, P(circle(x, y, 1)))
    return U(body, P(poly([(10, 9.5), (10, 8), (12, 6.5), (14, 8), (14, 9.5)], closed=True)))


@icon("mortgage-calculator", CAT, "Calculator with a small house shown on its display",
      tags=["mortgage payment calculator", "home loan calculator", "affordability", "repayment", "budget", "estimate"],
      filled=_calc_filled)
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 3))),
        detail(rect(7, 5.5, 10, 5, 0)),
        solid(poly([(10, 9.5), (10, 8), (12, 6.5), (14, 8), (14, 9.5)], closed=True)),
        *[dot(x, y, 1) for y in (14, 18) for x in (8.5, 12, 15.5)],
    ]


@icon("refinance-home", CAT, "House surrounded by two circular refresh arrows",
      tags=["remortgage", "refinancing", "new loan", "switch mortgage", "renew", "loan swap"])
def _(S):
    return [
        line(arc(12, 12, 9.5, 195, 315)), line(poly(head(polar(12, 12, 9.5, 315), 45, 2.25), r=S.r * 0.5)),
        line(arc(12, 12, 9.5, 15, 135)), line(poly(head(polar(12, 12, 9.5, 135), 225, 2.25), r=S.r * 0.5)),
        shell(house(S, 8, 16, 7.5, 16.5, eave=11)),
    ]


# ============================================================================ money and ownership

@icon("home-savings-jar", CAT, "Glass jar with a lid, a small house on its label and a coin at the bottom",
      tags=["house fund", "deposit savings", "saving for a home", "piggy jar", "first home fund", "down payment savings"])
def _(S):
    return [
        shell(rect(7, 2.5, 10, 3, min(S.R, 1))),
        shell(rect(4.5, 6.5, 15, 15, S.R)),
        detail(poly([(8.5, 14), (8.5, 11), (12, 8.5), (15.5, 11), (15.5, 14)], closed=True)),
        detail(seg(8.5, 18, 15.5, 18)),
    ]


@icon("down-payment", CAT, "House outline with two stacked coins filling its lower part",
      tags=["deposit", "initial payment", "first payment", "home purchase", "equity", "cash upfront"])
def _(S):
    return [
        shell(house(S, 2.5, 21.5, 2.5, 21.5, eave=10)),
        mark(rect(8, 11.5, 8, 2.5, 1.25)), mark(rect(7, 14.75, 10, 2.5, 1.25)), mark(rect(6, 18, 12, 2, 1)),
    ]


@icon("bridge-loan", CAT, "Two small houses joined by an arched bridge with a coin between the arch and the deck",
      tags=["bridging finance", "short term loan", "interim loan", "buy before sell", "gap financing", "property loan"])
def _(S):
    return [
        shell(house(S, 2, 6.5, 11, 20.5, eave=14)),
        shell(house(S, 17.5, 22, 11, 20.5, eave=14)),
        line(seg(6.5, 18, 17.5, 18)),
        line("M8 18C8.5 8.5 15.5 8.5 16 18"),
        mark(circle(12, 14.5, 1.75)),
    ]


@icon("rent-due", CAT, "Calendar page with a small house and a coin on it",
      tags=["rent day", "payment due", "monthly rent", "rent reminder", "rental payment", "tenant bill"])
def _(S):
    return [
        shell(rect(3, 4.5, 18, 17, rr(S, 3))),
        detail(seg(3, 9.5, 21, 9.5)),
        line(seg(8, 2.5, 8, 6.5)), line(seg(16, 2.5, 16, 6.5)),
        detail(poly([(6, 18.5), (6, 15.5), (8.5, 13), (11, 15.5), (11, 18.5)], closed=True)),
        shell(circle(16, 16, 2.25)),
    ]


@icon("security-deposit", CAT, "Stack of two coins with a key lying on top",
      tags=["tenant deposit", "bond", "rental deposit", "damage deposit", "refundable", "key money"])
def _(S):
    return [
        shell(circle(7, 7.5, 2.75)),
        line(seg(9.75, 7.5, 21, 7.5)),
        line(seg(17, 7.5, 17, 10.5)), line(seg(20.5, 7.5, 20.5, 10)),
        shell(rect(3, 12.5, 18, 4, L(S, 1.5, 2))),
        shell(rect(3, 16.5, 18, 4, L(S, 1.5, 2))),
    ]


@icon("rental-income", CAT, "House with coins falling from it into an open hand",
      tags=["rent received", "landlord income", "passive income", "buy to let", "rent money", "yield"])
def _(S):
    return [
        shell(house(S, 6, 18, 2.5, 11, eave=6.5)),
        dot(10, 14, 1.25), dot(14, 15.5, 1.25),
        line(poly([(2.5, 18), (7, 18), (10.5, 21), (17.5, 21), (21.5, 18)], r=S.r)),
    ]


@icon("shared-ownership", CAT, "House split down the middle with one half solid and a person beneath each half",
      tags=["part buy part rent", "co-ownership", "joint ownership", "equity share", "affordable housing", "partial purchase"])
def _(S):
    return [
        shell(house(S, 4, 20, 2.5, 13, eave=8.5)),
        detail(seg(12, 3.5, 12, 13)),
        mark(poly([(5, 12), (5, 8.9), (11, 4.6), (11, 12)], closed=True)),
        dot(7.5, 16.75, 1.5), line("M4.75 22v-1a2.75 2.75 0 0 1 5.5 0v1"),
        dot(16.5, 16.75, 1.5), line("M13.75 22v-1a2.75 2.75 0 0 1 5.5 0v1"),
    ]


@icon("landlord", CAT, "Person holding a large ring of keys beside a small house",
      tags=["property owner", "lessor", "rental owner", "letting", "keyholder", "owner"])
def _(S):
    return [
        *person(4.5, 3, 21),
        line(seg(4.5, 10, 8.5, 13)),
        shell(circle(11, 14, 2.5)),
        line(seg(9.75, 16.5, 9.75, 21)), line(seg(12.25, 16.5, 12.25, 20)),
        shell(house(S, 16, 22, 12, 21, eave=15)),
    ]


@icon("property-manager", CAT, "Person holding a clipboard in front of an apartment block",
      tags=["building manager", "estate agent", "letting agent", "caretaker", "facilities", "inspection"])
def _(S):
    return [
        shell(rect(14.5, 3, 7.5, 18.5, rr(S, 1.5))),
        *[dot(x, y, 0.9) for y in (7, 11) for x in (17, 19.5)],
        sq(17.25, 16, 2.5, 5.5),
        *person(4, 3, 21),
        shell(rect(7, 10, 5, 7, rr(S, 1))),
    ]


@icon("roommates", CAT, "Two people standing side by side under a single roof outline",
      tags=["flatmates", "housemates", "shared house", "co-living", "house share", "room sharing"])
def _(S):
    return [
        line(poly([(2, 10), (12, 3), (22, 10)], r=S.r * 0.6)),
        shell(circle(7.5, 13.5, 2.25)), line("M3.5 21.5v-1.5a4 4 0 0 1 8 0v1.5"),
        shell(circle(16.5, 13.5, 2.25)), line("M12.5 21.5v-1.5a4 4 0 0 1 8 0v1.5"),
    ]


# ============================================================================ outdoor and architecture

@icon("juliet-balcony", CAT, "Tall French window with a shallow railing fixed across its lower half",
      tags=["french balcony", "balconette", "window railing", "faux balcony", "balustrade", "french doors"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 1.5))),
        detail(seg(12, 3.5, 12, 14)),
        line(seg(2.5, 14.5, 21.5, 14.5)),
        line(seg(7.5, 14.5, 7.5, 21)), line(seg(16.5, 14.5, 16.5, 21)),
        dot(10, 8.5, 0.9), dot(14, 8.5, 0.9),
    ]


@icon("roof-terrace", CAT, "Flat building roof with a patio umbrella and a lounge chair on top",
      tags=["rooftop terrace", "roof deck", "roof garden", "penthouse terrace", "sun deck", "patio"])
def _(S):
    return [
        shell(rect(2.5, 16.5, 19, 5, rr(S, 1.5))),
        shell("M2.5 10.5A4.75 5.5 0 0 1 12 10.5Z"),
        line(seg(7.25, 10.5, 7.25, 16.5)),
        line(poly([(14.5, 8.5), (17.5, 14), (21.5, 14)], r=S.r * 0.6)),
        line(seg(20.5, 14, 20.5, 16.5)),
    ]


@icon("privacy-fence", CAT, "Tall solid fence of tight vertical boards with a flat cap rail along the top",
      tags=["wooden fence", "garden fence", "solid fence", "boundary fence", "fence boards", "screen fence"])
def _(S):
    return [
        line(seg(2, 3.5, 22, 3.5)),
        shell(rect(3.5, 6.5, 17, 15, rr(S, 1))),
        detail(seg(8.5, 7.5, 8.5, 21)), detail(seg(12, 7.5, 12, 21)), detail(seg(15.5, 7.5, 15.5, 21)),
    ]


@icon("outdoor-kitchen", CAT, "Built-in outdoor grill counter with a sink under a small canopy roof",
      tags=["bbq area", "patio kitchen", "grill station", "barbecue counter", "alfresco", "outdoor cooking"])
def _(S):
    return [
        shell(poly([(2, 7.5), (12, 2.5), (22, 7.5)], closed=True, r=S.r * 0.4)),
        line(seg(4, 7.5, 4, 14.5)), line(seg(20, 7.5, 20, 14.5)),
        shell(rect(3, 14.5, 18, 7, rr(S, 1.5))),
        line(arc(9, 14.5, 3, 180, 360)),
        line("M16 14.5V11.5H18.5"),
    ]


@icon("two-car-garage", CAT, "Garage building with two side-by-side garage doors",
      tags=["double garage", "car garage", "garage doors", "parking garage", "carport", "home garage"])
def _(S):
    return [
        shell(house(S, 2.5, 21.5, 3, 21.5, eave=8.5)),
        detail(rect(5.5, 12, 5.5, 9.5)), detail(rect(13, 12, 5.5, 9.5)),
        detail(seg(5.5, 16.5, 11, 16.5)), detail(seg(13, 16.5, 18.5, 16.5)),
    ]


@icon("driveway", CAT, "House with a garage door and a driveway strip widening down to the road",
      tags=["drive", "garage access", "parking pad", "car entrance", "home access", "paving"])
def _(S):
    return [
        shell(house(S, 2.5, 21.5, 2.5, 13, eave=6.5)),
        detail(rect(5.5, 8, 5.5, 5)), detail(rect(16, 8, 3, 5)),
        shell(poly([(5.5, 15.5), (11, 15.5), (13.5, 21.5), (3, 21.5)], closed=True)),
    ]


@icon("backyard", CAT, "Rear of a house with a fenced lawn and a round tree",
      tags=["back garden", "yard", "garden fence", "lawn", "outdoor space", "tree"])
def _(S):
    return [
        shell(house(S, 2.5, 11.5, 3.5, 14.5, eave=8)),
        line(seg(2, 17, 22, 17)),
        line(seg(5, 17, 5, 21.5)), line(seg(11, 17, 11, 21.5)), line(seg(17, 17, 17, 21.5)),
        shell(circle(17, 8.5, 4.25)),
        line(seg(17, 13, 17, 15)),
    ]


@icon("front-walkway", CAT, "Stepping stone path crossing a lawn to a front door",
      tags=["garden path", "stepping stones", "entrance path", "front path", "curb appeal", "pathway"])
def _(S):
    return [
        shell(house(S, 4.5, 19.5, 2.5, 12.5, eave=7)),
        detail(rect(10.5, 7.5, 3, 5)),
        sq(10, 14.5, 4, 1.75, 0.75), sq(8.75, 17.5, 6.5, 2, 0.75), sq(7, 20.25, 10, 1.75, 0.75),
    ]


@icon("pet-friendly-home", CAT, "House with a paw print inside it",
      tags=["pets allowed", "pet policy", "dogs welcome", "cats welcome", "paw", "animal friendly housing"])
def _(S):
    return [
        shell(house(S, 2.5, 21.5, 2.5, 21.5, eave=10)),
        mark(ellipse(12, 17.5, 3.25, 2.5)),
        dot(7.75, 14.25, 1.3), dot(10.5, 11.5, 1.3), dot(13.5, 11.5, 1.3), dot(16.25, 14.25, 1.3),
    ]


@icon("furnished-home", CAT, "House outline with a sofa and a floor lamp drawn inside it",
      tags=["furnished rental", "fully furnished", "ready to move in", "furniture included", "sofa", "lamp"])
def _(S):
    return [
        shell(house(S, 2.5, 21.5, 2.5, 21.5, eave=10)),
        mark(rect(5.5, 16, 9.5, 4, 1)), mark(rect(6.5, 12.5, 7.5, 4, 1)),
        line(seg(18, 20.5, 18, 14)),
        mark(poly([(16, 14), (20, 14), (19, 10.5), (17, 10.5)], closed=True)),
    ]


@icon("storage-locker", CAT, "Wire mesh storage cage with a padlocked door and boxes stacked inside",
      tags=["storage cage", "self storage unit", "mesh locker", "padlock", "basement storage", "storage room"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 2))),
        detail(seg(8, 3.5, 8, 9)), detail(seg(12, 3.5, 12, 9)), detail(seg(16, 3.5, 16, 9)),
        mark(rect(5.5, 13.5, 6, 6.5, 0.5)),
        shell(rect(14, 14, 4.5, 4, 0.75)), line("M15.25 14V12.5a1 1 0 0 1 2 0V14"),
    ]


@icon("loggia", CAT, "Building front with a recessed balcony behind two wide arches under an upper floor slab",
      tags=["arcade", "arches", "covered balcony", "italian loggia", "colonnade", "open gallery"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, S.R)),
        detail(seg(3.5, 9.5, 20.5, 9.5)),
        detail("M5.5 21V16.25A3.25 3.25 0 0 1 12 16.25V21"),
        detail("M12 16.25A3.25 3.25 0 0 1 18.5 16.25V21"),
        dot(7, 6, 0.9), dot(12, 6, 0.9), dot(17, 6, 0.9),
    ]


@icon("wraparound-porch", CAT, "House with a covered porch on posts running along both sides of its front",
      tags=["veranda", "front porch", "covered porch", "porch posts", "farmhouse porch", "deck porch"])
def _(S):
    return [
        line(roofline(S, 6.5, 17.5, 2.5, 6.5, 10)),
        shell(poly([(2, 14), (5, 10.5), (19, 10.5), (22, 14)], closed=True, r=S.r * 0.4)),
        line(seg(4, 14, 4, 21.5)), line(seg(20, 14, 20, 21.5)),
        line(seg(12, 15.5, 12, 21.5)),
    ]


@icon("front-stoop", CAT, "Short flight of steps with a railing leading up to a townhouse door",
      tags=["entry steps", "stairs to door", "brownstone steps", "front steps", "entrance stairs", "townhouse"])
def _(S):
    return [
        shell(rect(13.5, 2.5, 8, 8.5, rr(S, 3))),
        shell(poly([(2.5, 21.5), (2.5, 18.5), (6, 18.5), (6, 15.5), (9.5, 15.5), (9.5, 12.5), (21.5, 12.5), (21.5, 21.5)], closed=True, r=S.r * 0.4)),
        line(poly([(3.5, 14), (10, 8.5)])),
    ]


@icon("rural-acreage", CAT, "Wide fenced field with a small house far in the distance on the horizon",
      tags=["farmland", "country land", "acreage", "lot of land", "paddock", "countryside property"])
def _(S):
    return [
        shell(house(S, 9.5, 14.5, 4.5, 11, eave=7.5)),
        line(seg(2, 11, 9.5, 11)), line(seg(14.5, 11, 22, 11)),
        line(seg(2, 16, 22, 16)), line(seg(2, 20, 22, 20)),
        line(seg(4, 14, 4, 21.5)), line(seg(12, 14, 12, 21.5)), line(seg(20, 14, 20, 21.5)),
    ]


@icon("rooftop-pool", CAT, "Tall apartment tower with a small swimming pool on its flat roof",
      tags=["pool on roof", "sky pool", "penthouse pool", "apartment amenities", "infinity pool", "high rise"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 6.5, rr(S, 2))),
        detail("M6 5.75q1.5-1.5 3 0t3 0t3 0t3 0"),
        shell(rect(5, 12, 14, 9.5, rr(S, 1.5))),
        *[dot(x, y, 0.9) for y in (15, 18.5) for x in (9, 12, 15)],
    ]


@icon("queenslander-house", CAT, "Timber house raised on stumps with a wide verandah under a pitched iron roof",
      tags=["raised house", "stilted house", "verandah", "highset house", "australian house", "timber house"])
def _(S):
    return [
        line(poly([(2, 10), (12, 3), (22, 10)], r=S.r * 0.6)),
        line(seg(3.5, 10.5, 3.5, 15.5)), line(seg(20.5, 10.5, 20.5, 15.5)),
        line(seg(8, 10.5, 8, 15.5)),
        line(seg(2, 15.5, 22, 15.5)),
        line(seg(5, 17, 5, 21.5)), line(seg(12, 17, 12, 21.5)), line(seg(19, 17, 19, 21.5)),
    ]


# ============================================================================ documents, fixtures and plots

@icon("property-tax-bill", CAT, "Bill sheet with a small house at the top and a percent mark in the lower corner",
      tags=["council tax", "rates notice", "real estate tax", "tax statement", "assessment", "homeowner bill"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 2))),
        detail(poly([(7.5, 10), (7.5, 7.5), (10.5, 5.5), (13.5, 7.5), (13.5, 10)], closed=True)),
        detail(seg(7.5, 13.5, 11.5, 13.5)),
        dot(12.5, 15.5, 1.2), dot(16.5, 19, 1.2),
        mark(poly([(16.4, 14.3), (17.4, 15.2), (12.6, 20.2), (11.6, 19.3)], closed=True)),
    ]


@icon("escrow", CAT, "Small locked padlock box between a hand holding a house and a hand holding a coin",
      tags=["escrow account", "held funds", "neutral third party", "closing", "secure transaction", "deposit holding"])
def _(S):
    return [
        shell(rect(9, 12, 6, 6.5, rr(S, 1))),
        line("M10.5 12V10.25a1.5 1.5 0 0 1 3 0V12"),
        line(seg(2, 18.5, 6.5, 18.5)), line(seg(17.5, 18.5, 22, 18.5)),
        shell(house(S, 2.5, 6.5, 8, 16, eave=10.5)),
        shell(circle(19.75, 14.75, 2)),
    ]


def _trefoil(cx, cy, r):
    parts = []
    for a in (-90, 30, 150):
        p0 = polar(cx, cy, r, a - 30)
        p1 = polar(cx, cy, r, a + 30)
        parts.append(mark(f"M{fmt(cx)} {fmt(cy)}L{fmt(p0[0])} {fmt(p0[1])}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(p1[0])} {fmt(p1[1])}Z"))
    return parts


@icon("radon-detector", CAT, "Small wall-mounted monitor box with a digital display and a radiation trefoil",
      tags=["radon gas", "radon monitor", "gas detector", "radiation alarm", "air quality", "home safety"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 3))),
        sq(6.5, 6, 11, 3, 0.5),
        *_trefoil(12, 15.25, 3.75),
    ]


@icon("double-vanity", CAT, "Bathroom vanity with two basins on the counter under a wide mirror",
      tags=["bathroom vanity", "his and hers sinks", "two sinks", "washbasin", "bathroom cabinet", "master bath"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 5, rr(S, 1.5))),
        line("M4.5 9.5V10.5A3 3 0 0 0 10.5 10.5V9.5"),
        line("M13.5 9.5V10.5A3 3 0 0 0 19.5 10.5V9.5"),
        shell(rect(2.5, 14.5, 19, 3, min(S.R, 1.5))),
        line(seg(5, 17.5, 5, 21.5)), line(seg(19, 17.5, 19, 21.5)),
    ]


@icon("farmhouse-sink", CAT, "Deep apron-front sink under a counter slab with a tall gooseneck tap",
      tags=["apron sink", "kitchen sink", "belfast sink", "country kitchen", "gooseneck faucet", "countertop"])
def _(S):
    return [
        shell(rect(2.5, 10.5, 19, 3, min(S.R, 1.5))),
        shell(rect(6, 13.5, 12, 8, rr(S, 2.5))),
        line(seg(3.5, 13.5, 3.5, 21.5)), line(seg(20.5, 13.5, 20.5, 21.5)),
        line("M16 10.5V5.25A3 3 0 0 0 10 5.25V7"),
    ]


@icon("waterfront-lot", CAT, "Plan view of a plot whose back edge runs along wavy water lines with a small dock",
      tags=["lakefront", "beachfront lot", "riverfront", "shoreline property", "lakeside land", "water view plot"])
def _(S):
    return [
        shell(poly([(3, 4), (20, 2.5), (21, 12.5), (2.5, 13)], closed=True, r=S.r * 0.5)),
        mark(rect(16, 13, 2.5, 7)),
        line("M2 17q2.5-2 5 0t5 0"),
        line("M2 21q2.5-2 5 0t5 0"),
    ]


@icon("wooded-lot", CAT, "Plan view of a plot marked by corner stakes with two trees inside",
      tags=["forested land", "tree covered lot", "woodland plot", "timber land", "trees on property", "land parcel"])
def _(S):
    return [
        line("M2.5 7.5V2.5H7.5"), line("M16.5 2.5H21.5V7.5"), line("M21.5 16.5V21.5H16.5"), line("M7.5 21.5H2.5V16.5"),
        shell(circle(9, 9, 3)), line(seg(9, 12, 9, 14.5)),
        shell(circle(15, 13, 3)), line(seg(15, 16, 15, 18.5)),
    ]


@icon("office-park", CAT, "Two low office blocks with a tree between them on a shared lawn",
      tags=["business park", "corporate campus", "commercial estate", "office complex", "employment site", "campus"])
def _(S):
    return [
        shell(rect(2.5, 10, 7, 11, rr(S, 1.5))), shell(rect(14.5, 5, 7, 16, rr(S, 1.5))),
        dot(5, 13.5, 0.9), dot(7, 13.5, 0.9), dot(5, 17, 0.9), dot(7, 17, 0.9),
        dot(17, 9, 0.9), dot(19, 9, 0.9), dot(17, 13, 0.9), dot(19, 13, 0.9),
        mark(circle(12, 15, 1.8)), line(seg(12, 16.5, 12, 21)),
    ]


@icon("industrial-estate", CAT, "Row of two joined low industrial units with sawtooth roofs and roller shutter doors",
      tags=["industrial park", "warehouse units", "trading estate", "light industrial", "factory units", "business units"])
def _(S):
    return [
        shell(poly([(2.5, 21.5), (2.5, 10), (12, 4.5), (12, 10), (21.5, 4.5), (21.5, 21.5)], closed=True, r=S.r * 0.4)),
        detail(seg(12, 10.5, 12, 21)),
        detail(rect(4.5, 13.5, 5, 8)), detail(rect(14.5, 13.5, 5, 8)),
    ]


@icon("mortgage-debt", CAT, "House chained to a heavy solid iron ball",
      tags=["home loan burden", "owing on house", "negative equity", "debt weight", "ball and chain", "loan"])
def _(S):
    return [
        shell(house(S, 2.5, 12, 2.5, 11.5, eave=6.5)),
        dot(13.5, 13, 1), dot(15, 14.75, 1),
        solid(circle(17.5, 17.5, 4)),
    ]


@icon("doorknob-lockbox", CAT, "Key lockbox with a U-shaped shackle hooked over a round door knob",
      tags=["key safe", "realtor lockbox", "key holder", "spare key box", "combination lock", "access box"])
def _(S):
    return [
        line(seg(2.5, 2.5, 2.5, 21.5)),
        shell(circle(6.5, 18, 2.5)),
        shell(rect(11, 11.5, 10, 9, rr(S, 2))),
        line("M14 11.5V8A3.75 3.75 0 0 0 6.5 8V14"),
        dot(13.5, 16, 0.9), dot(16, 16, 0.9), dot(18.5, 16, 0.9),
    ]


@icon("lap-pool", CAT, "Plan view of a long narrow swimming pool with one lane line down its centre",
      tags=["swimming lane", "exercise pool", "narrow pool", "swim lane", "fitness pool", "backyard pool"])
def _(S):
    return [
        shell(rect(2.5, 7, 19, 10, rr(S, 2))),
        detail(seg(7, 12, 17, 12)),
        dot(5.25, 12, 0.9),
        dot(18.75, 12, 0.9),
    ]


@icon("floating-home", CAT, "Boxy house standing on a flat pontoon platform above wave lines",
      tags=["houseboat", "water home", "pontoon house", "floating house", "flood resilient", "waterfront living"])
def _(S):
    return [
        shell(rect(6, 4.5, 12, 8.5, rr(S, 1.5))),
        sq(8.5, 7, 3, 3, 0.5), sq(14, 8.5, 2.5, 4.5),
        shell(rect(3, 14, 18, 3, min(S.R, 1.5))),
        line("M2 21q2.5-2 5 0t5 0t5 0t5 0"),
    ]


@icon("room-scan", CAT, "Phone held up to a room corner with the walls outlined on its screen",
      tags=["lidar scan", "3d room scan", "floor plan scan", "measure room", "augmented reality", "capture space"])
def _(S):
    return [
        shell(rect(6.5, 2.5, 11, 19, rr(S, 3))),
        detail(poly([(9, 7), (12, 8.75), (15, 7)])),
        detail(seg(12, 8.75, 12, 14.5)),
        detail(poly([(9, 16.5), (12, 14.5), (15, 16.5)])),
        line("M3.5 8.5Q2 12 3.5 15.5"), line("M20.5 8.5Q22 12 20.5 15.5"),
    ]


@icon("shared-driveway", CAT, "Plan view of one driveway leaving the street and forking toward two neighbouring houses",
      tags=["common drive", "joint driveway", "neighbour access", "easement", "access road", "fork"])
def _(S):
    h = lambda x: solid(poly([(x, 9), (x, 5.5), (x + 3.5, 2.5), (x + 7, 5.5), (x + 7, 9)], closed=True))
    return [
        h(2.5), h(14.5),
        line(poly([(12, 21.5), (12, 15.5), (6, 11.5)], r=S.r)), line(poly([(12, 15.5), (18, 11.5)], r=S.r)),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("attached-garage", CAT, "House with a single garage joined to its side under one continuous roof line",
      tags=["integral garage", "garage attached", "car port home", "garage door", "house and garage", "parking at home"])
def _(S):
    return [
        shell(poly([(2.5, 21.5), (2.5, 10), (10, 3), (21.5, 10), (21.5, 21.5)], closed=True, r=S.r * 0.5)),
        detail(seg(13.5, 7.5, 13.5, 21)),
        detail(rect(6, 13.5, 3.5, 8)), detail(rect(16, 13.5, 3.5, 8)),
    ]


@icon("equestrian-property", CAT, "House beside a fenced paddock with a horse head looking over the rail",
      tags=["horse property", "stables", "paddock", "ranch", "horse farm", "riding estate"])
def _(S):
    horse = poly([(16.5, 3), (18, 6.5), (21, 8), (21, 16), (16.5, 16), (16, 13.5), (14.5, 14.5), (12.5, 13.5),
                  (12.5, 11), (14.5, 7)], closed=True, r=S.r * 0.4)
    return [
        shell(house(S, 2.5, 9.5, 6, 15, eave=9.5)),
        shell(horse), dot(16.25, 8.5, 0.8),
        line(seg(2, 18, 22, 18)),
        line(seg(4, 16.5, 4, 21.5)), line(seg(12, 18, 12, 21.5)), line(seg(20, 18, 20, 21.5)),
    ]


@icon("golf-course-home", CAT, "House standing beside a putting green with a hole flag",
      tags=["golf community", "fairway home", "golf property", "putting green", "country club home", "links"])
def _(S):
    return [
        shell(house(S, 2.5, 11, 5, 17, eave=9.5)),
        shell(ellipse(15, 19, 6.5, 2.5)),
        line(seg(16.5, 18, 16.5, 8)),
        solid(poly([(16.5, 8), (21.5, 10), (16.5, 12)], closed=True)),
    ]


@icon("porte-cochere", CAT, "Roof slab on two columns over a driveway with a car parked beneath",
      tags=["covered entrance", "carriage porch", "drive-through canopy", "car canopy", "covered drive", "entrance canopy"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 3.5, min(S.R, 1.5))),
        line(seg(4.5, 6.5, 4.5, 21.5)), line(seg(19.5, 6.5, 19.5, 21.5)),
        shell(rect(6.5, 14.5, 11, 4, rr(S, 2))),
        line(poly([(8.5, 14.5), (10, 11.5), (14, 11.5), (15.5, 14.5)], r=S.r * 0.4)),
        solid(circle(9.5, 19, 1.5)), solid(circle(14.5, 19, 1.5)),
    ]


@icon("laundry-chute", CAT, "Square hatch in a wall opening onto a shaft with a shirt dropping down inside it",
      tags=["clothes chute", "linen chute", "laundry hatch", "washing drop", "utility room", "hamper shaft"])
def _(S):
    tee = poly([(9.5, 12.5), (11, 12.5), (12, 13.5), (13, 12.5), (14.5, 12.5), (17, 14.5), (15.5, 16.5), (14.5, 15.75),
                (14.5, 20), (9.5, 20), (9.5, 15.75), (8.5, 16.5), (7, 14.5)], closed=True)
    return [
        shell(rect(5.5, 2.5, 13, 7, rr(S, 1.5))),
        dot(12, 6, 1),
        line(seg(5.5, 9.5, 5.5, 21.5)), line(seg(18.5, 9.5, 18.5, 21.5)),
        solid(tee),
    ]


@icon("end-of-terrace-house", CAT, "Row of three joined gabled houses with only the house at one end filled in",
      tags=["terraced house", "end terrace", "row house", "townhouse row", "semi attached", "corner house"])
def _(S):
    return [
        shell(poly([(2, 21.5), (2, 10.5), (5.3, 6.5), (8.7, 10.5), (12, 6.5), (15.3, 10.5), (18.7, 6.5), (22, 10.5), (22, 21.5)], closed=True, r=S.r * 0.4)),
        detail(seg(8.7, 11, 8.7, 21)), detail(seg(15.3, 11, 15.3, 21)),
        mark(poly([(16.8, 20), (16.8, 12), (18.7, 9.5), (20.6, 12), (20.6, 20)], closed=True)),
    ]


@icon("maisonette", CAT, "Apartment block with one unit spanning two floors and a small stair drawn inside it",
      tags=["duplex flat", "two storey flat", "split level apartment", "apartment with stairs", "flat", "two floor unit"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 2))),
        detail(seg(12, 3.5, 12, 21)),
        detail(seg(3.5, 15.5, 20.5, 15.5)), detail(seg(12.5, 9, 20.5, 9)),
        line(poly([(5.5, 13), (5.5, 11), (7.5, 11), (7.5, 9), (9.5, 9), (9.5, 7)])),
        dot(16.5, 5.75, 0.9), dot(16.5, 12.25, 0.9), dot(16.5, 18.5, 0.9), dot(7.5, 18.5, 0.9),
    ]


@icon("rent-to-own", CAT, "House above a coin and a key joined by a curved arrow running from the coin to the key",
      tags=["lease option", "lease purchase", "rent then buy", "path to ownership", "instalment buying", "own home"])
def _(S):
    return [
        shell(house(S, 6.5, 17.5, 2.5, 9, eave=5.5)),
        shell(circle(5.5, 18.5, 2.75)),
        line("M5.5 14Q5.5 11.75 10.5 11.75T15.5 14"), line(poly(head((15.5, 14.5), 90, 1.75), r=S.r * 0.4)),
        shell(circle(15.5, 18.5, 2.25)), line(seg(17.75, 18.5, 22, 18.5)), line(seg(20.5, 18.5, 20.5, 21)),
    ]
