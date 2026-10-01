"""TypeIcon Core: business, batch 003 (insurance, property, law, civic life, money and marketing).

Generic objects and signs only: no company, card network, party or government emblem.
Insurance icons share one umbrella canopy (y 2.5 to 8.5) with the insured object below it (y 11 to 21.5).
Objects that sit in front of another are cut out of it with a 2 px gap (see `cut`).
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "business"


# ============================================================================ helpers

def rr(S, cap=None):
    """Container corner radius for the style, optionally capped for small shapes."""
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def mark(x, y, S, r=1.25):
    """Small marker: a square in Line, a disc in Rounded."""
    if S.name == "rounded":
        return dot(x, y, r)
    return sq(x - r, y - r, 2 * r, 2 * r)


def cut(d, *keep, gap=2.0):
    """Closed shape d with the closed shapes in keep removed, leaving a stroke gap around them."""
    w = 2 * (gap + 2.0)
    region = U(*[U(P(k), ST(k, w, "round", "round")) for k in keep])
    return path_to_d(D(P(d), region))


def head(tip, deg, size=2.5):
    """Open arrowhead points at tip; deg is the direction the arrow points (0 = right, 90 = down)."""
    a = polar(tip[0], tip[1], size * math.sqrt(2), deg + 180 - 45)
    b = polar(tip[0], tip[1], size * math.sqrt(2), deg + 180 + 45)
    return [a, tip, b]


def arrow(S, x0, y0, x1, y1, size=2.5):
    deg = math.degrees(math.atan2(y1 - y0, x1 - x0))
    return [line(seg(x0, y0, x1, y1)), line(poly(head((x1, y1), deg, size), r=S.r * 0.5))]


def rot(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def house(S, x0, x1, ytop, ybot, eave=None):
    """Pentagon house outline: walls x0..x1, roof peak at ytop, floor at ybot."""
    cx = (x0 + x1) / 2
    e = eave if eave is not None else ytop + (x1 - x0) / 2
    return poly([(x0, ybot), (x0, e), (cx, ytop), (x1, e), (x1, ybot)], closed=True, r=S.r * 0.6)


def door(S, cx, w, ytop, ybot):
    return detail(poly([(cx - w / 2, ybot), (cx - w / 2, ytop), (cx + w / 2, ytop), (cx + w / 2, ybot)], r=S.r * 0.5))


# ---------------------------------------------------------------------------- insurance umbrella

def canopy_d(S):
    """Umbrella canopy with a domed top and three scallops along its lower edge (y 2.5 to 8.5)."""
    top = "M2.5 8.5A9.5 6 0 0 1 21.5 8.5"
    sc = "A3.17 1.9 0 0 0 15.17 8.5A3.17 1.9 0 0 0 8.83 8.5A3.17 1.9 0 0 0 2.5 8.5Z"
    return top + sc


def umbrella(S):
    return [shell(canopy_d(S), stroke_miterlimit="8" if S.name == "line" else "4")]


def insured(S, *parts):
    return umbrella(S) + list(parts)


# ============================================================================ shipping and retail

@icon("international-shipping", CAT, "Globe with a parcel box in front of its lower right side",
      tags=["global shipping", "worldwide delivery", "overseas", "export", "parcel", "freight"])
def _(S):
    box = rect(12.5, 12.5, 9, 9, rr(S, 1.5))
    globe = cut(circle(9.5, 9.5, 7.5), box)
    return [
        shell(globe),
        detail(seg(2, 9.5, 17, 9.5)),
        detail("M9.5 2A3.75 7.5 0 0 0 9.5 17"),
        detail("M9.5 2A3.75 7.5 0 0 1 13.25 9.5"),
        shell(box),
        detail(seg(17, 12.5, 17, 16)),
    ]


@icon("delivery-signature", CAT, "Handheld courier scanner with a signature scribbled on its screen and a stylus",
      tags=["proof of delivery", "sign for parcel", "courier", "e-signature", "handheld", "package received"])
def _(S):
    scribble = "M6 12.5C6.5 9 8 8 8.5 9.5C9 11 7.5 13.5 9.5 12C11 10.8 11 9.5 12 10.5C12.5 11 12.5 12 13 11.5"
    return [
        shell(rect(3, 3, 13, 18.5, rr(S, 2.5))),
        detail(scribble),
        detail(seg(6, 16, 13, 16)),
        mark(9.5, 18.5, S, 1),
        line(seg(19.5, 3, 19.5, 15.5)),
        solid(poly([(18.5, 17), (20.5, 17), (19.5, 21)], closed=True)),
    ]


SOLE = ("M15.5 2.5C18.6 2.5 20.5 5.5 20.5 9.5C20.5 12.5 19.2 14.2 19.2 16.5C19.2 19.5 17.8 21.5 15.5 21.5"
        "C13.2 21.5 12 19.8 12 17.5C12 14.8 11 12.5 11 9.5C11 5 12.8 2.5 15.5 2.5Z")


@icon("shoe-size-measure", CAT, "Foot sole standing beside a ruler with a scale of ticks, for measuring shoe size",
      tags=["foot measure", "shoe fitting", "foot size", "shoe shop", "measure feet", "sizing"])
def _(S):
    return [
        shell(rect(3, 2.5, 5, 19, rr(S, 1.5))),
        detail(seg(3, 6.5, 5.5, 6.5)), detail(seg(3, 10.5, 5.5, 10.5)),
        detail(seg(3, 14.5, 5.5, 14.5)), detail(seg(3, 18.5, 5.5, 18.5)),
        shell(SOLE),
    ]


@icon("shop-door-bell", CAT, "Small shop bell hanging from a curled spring bracket",
      tags=["shop bell", "door chime", "entrance bell", "customer arrival", "store bell", "ring"])
def _(S):
    return [
        line(seg(3, 2.5, 3, 7.5)),
        line("M3 5H12.5A2 2 0 0 1 12.5 9H11.5"),
        line(seg(14.5, 5, 14.5, 9.5) if S.name == "line" else seg(14.5, 6, 14.5, 9.5)),
        shell("M9 18.5C9 13.5 10.8 11.5 14.5 11.5C18.2 11.5 20 13.5 20 18.5Z" if S.name == "rounded" else
              "M9 18.5L9.6 14C10 12.5 11.5 11.5 14.5 11.5C17.5 11.5 19 12.5 19.4 14L20 18.5Z"),
        dot(14.5, 21, 1.4),
    ]


@icon("import-export", CAT, "Shipping container with two opposite arrows above it",
      tags=["trade", "customs", "imports", "exports", "cargo", "global trade", "freight"])
def _(S):
    parts = [shell(rect(2.5, 13, 19, 8.5, rr(S, 1.5)))]
    parts += [detail(seg(x, 15.5, x, 19)) for x in (7, 12, 17)]
    parts += arrow(S, 4, 3.5, 19.5, 3.5)
    parts += arrow(S, 20, 8.5, 4.5, 8.5)
    return parts


@icon("yard-sale", CAT, "Folding table covered with assorted items and a small sign on a stake beside it",
      tags=["garage sale", "car boot sale", "rummage sale", "second hand", "flea market", "sale sign"])
def _(S):
    return [
        line(seg(2.5, 13, 15.5, 13)),
        line(seg(4.5, 13, 13.5, 21.5)), line(seg(13.5, 13, 4.5, 21.5)),
        shell(rect(3.5, 7.5, 5, 5.5, rr(S, 1))),
        shell(circle(12, 10, 3)),
        shell(rect(17, 2.5, 5, 6, rr(S, 1.5))),
        line(seg(19.5, 8.5, 19.5, 21.5)),
    ]


# ============================================================================ insurance

@icon("home-insurance", CAT, "House sheltered under an open umbrella",
      tags=["homeowners insurance", "property insurance", "house cover", "home cover", "protection", "policy"])
def _(S):
    return insured(S, shell(house(S, 6, 18, 11.5, 21.5)), door(S, 12, 3, 17, 21.5))


@icon("life-insurance", CAT, "Two adults and a child sheltered under an open umbrella",
      tags=["family protection", "life cover", "life policy", "family", "beneficiary", "protection"])
def _(S):
    def body(x0, x1, y0, y1):
        r = (x1 - x0) / 2
        if S.name == "rounded":
            return solid(f"M{x0} {y1}V{y0 + r}A{r} {r} 0 0 1 {x1} {y0 + r}V{y1}Z")
        k = r * 0.55
        return solid(poly([(x0, y1), (x0, y0 + k), (x0 + k, y0), (x1 - k, y0), (x1, y0 + k), (x1, y1)], closed=True))
    return insured(
        S,
        dot(5.25, 13, 1.75), body(2.5, 8, 16, 21.5),
        dot(18.75, 13, 1.75), body(16, 21.5, 16, 21.5),
        dot(12, 15.5, 1.4), body(10, 14, 18.25, 21.5),
    )


HEART = "M12 21.5C8 18.8 6 16.5 6 14.3C6 12.5 7.3 11.2 9 11.2C10.3 11.2 11.3 11.9 12 13C12.7 11.9 13.7 11.2 15 11.2C16.7 11.2 18 12.5 18 14.3C18 16.5 16 18.8 12 21.5Z"
HEART_L = "M12 21.5L6.6 16C5.3 14.5 5.8 11.7 8.3 11.2C10 10.9 11.3 11.8 12 13C12.7 11.8 14 10.9 15.7 11.2C18.2 11.7 18.7 14.5 17.4 16Z"


@icon("health-insurance", CAT, "Heart with a medical cross sheltered under an open umbrella",
      tags=["medical insurance", "health cover", "health plan", "healthcare", "medical cover", "policy"])
def _(S):
    return insured(S, shell(HEART_L if S.name == "line" else HEART, stroke_miterlimit="8"),
                   detail(seg(12, 14.25, 12, 18.25)), detail(seg(10, 16.25, 14, 16.25)))


def wave(x0, x1, y, amp=1.0, n=None):
    n = n or int(round((x1 - x0) / 4))
    step = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        xa = x0 + i * step
        sgn = -1 if i % 2 == 0 else 1
        d += f"Q{fmt(xa + step / 2)} {fmt(y + sgn * amp * 2)} {fmt(xa + step)} {fmt(y)}"
    return d


@icon("flood-insurance", CAT, "House standing in wavy water lines under an open umbrella",
      tags=["flood cover", "water damage", "flooding", "natural disaster", "home insurance", "storm"])
def _(S):
    return insured(S, shell(house(S, 7, 17, 11, 17.5, eave=14.5)), line(wave(3, 21, 20.75, 0.75, 5)))


FLAME = ("M18.5 21.5C16.4 21.5 15.3 20.1 15.3 18.5C15.3 17 16 16 16.6 14.8C17.1 15.8 17.6 16.3 18.2 16.5"
         "C18.2 14.8 18.9 13.3 20 12C20.4 14.3 21.7 16 21.7 18.5C21.7 20.1 20.6 21.5 18.5 21.5Z")


@icon("fire-insurance", CAT, "House with a small flame beside it under an open umbrella",
      tags=["fire cover", "fire damage", "house fire", "property insurance", "hazard", "blaze"])
def _(S):
    return insured(S, shell(house(S, 3.5, 13, 11.5, 21.5)), door(S, 8.25, 2.5, 17.5, 21.5),
                   shell(FLAME, stroke_miterlimit="8"))


@icon("business-insurance", CAT, "Briefcase sheltered under an open umbrella",
      tags=["commercial insurance", "liability insurance", "company cover", "business protection", "work", "policy"])
def _(S):
    return insured(S, line(poly([(9, 14), (9, 11.75), (15, 11.75), (15, 14)], r=S.r * 0.5)),
                   shell(rect(5, 14, 14, 7.5, rr(S, 2))), detail(seg(5, 17.5, 19, 17.5)))


@icon("crop-insurance", CAT, "Ear of wheat sheltered under an open umbrella",
      tags=["farm insurance", "agriculture", "harvest", "farming", "crop cover", "wheat"])
def _(S):
    def grain(cx, cy, deg):
        pts = rot([(cx, cy - 1.6), (cx + 1.1, cy), (cx, cy + 1.6), (cx - 1.1, cy)], deg, cx, cy)
        if S.name == "rounded":
            return solid(_ell(cx, cy, 1.15, 1.7, deg))
        return solid(poly(pts, closed=True))
    return insured(
        S,
        line(seg(12, 13, 12, 21.5)),
        grain(12, 11.9, 0),
        grain(9.8, 14.2, -35), grain(14.2, 14.2, 35),
        grain(9.8, 17.4, -35), grain(14.2, 17.4, 35),
    )


def _ell(cx, cy, rx, ry, deg):
    """Ellipse centred on (cx, cy), turned clockwise by deg."""
    from geometry import transform_path
    a = math.radians(deg)
    c, s_ = math.cos(a), math.sin(a)
    return path_to_d(transform_path(P(ellipse(0, 0, rx, ry)), (c, s_, -s_, c, cx, cy)))


TOOTH = ("M8.8 11.5C10 11.5 10.8 12 12 12C13.2 12 14 11.5 15.2 11.5C17.2 11.5 18 13 18 14.8C18 17 17 18.5 16.5 21"
         "C16.3 21.7 15.5 21.8 15.2 21.1L13.8 18C13.4 17.2 10.6 17.2 10.2 18L8.8 21.1C8.5 21.8 7.7 21.7 7.5 21"
         "C7 18.5 6 17 6 14.8C6 13 6.8 11.5 8.8 11.5Z")


@icon("dental-insurance", CAT, "Tooth sheltered under an open umbrella",
      tags=["dental cover", "dental plan", "dentist", "teeth", "oral health", "policy"])
def _(S):
    return insured(S, shell(TOOTH))


@icon("device-insurance", CAT, "Smartphone sheltered under an open umbrella",
      tags=["phone insurance", "gadget insurance", "mobile cover", "screen protection", "electronics", "warranty"])
def _(S):
    return insured(S, shell(rect(8, 11.5, 8, 10, rr(S, 1.5))), detail(seg(11, 19, 13, 19)))


@icon("insurance-claim", CAT, "Clipboard form with a cracked glass mark in its top section",
      tags=["claim form", "file a claim", "damage report", "accident", "insurance", "paperwork"])
def _(S):
    spikes = [(-95, 4), (-40, 3), (5, 3.8), (60, 2.8), (110, 3.6), (160, 2.7), (205, 3.8)]
    burst = []
    for i, (a, r) in enumerate(spikes):
        nxt = spikes[(i + 1) % len(spikes)][0] + (360 if i == len(spikes) - 1 else 0)
        burst += [polar(12, 10.5, r, a), polar(12, 10.5, 1.3, (a + nxt) / 2)]
    return [
        shell(rect(4, 4, 16, 17.5, rr(S, 2.5))),
        shell(rect(9, 2.5, 6, 3, rr(S, 1))),
        Part("dot", poly(burst, closed=True)),
        detail(seg(7.5, 16.5, 16.5, 16.5)),
    ]


# ============================================================================ accidents and property

def car_side(S, deg, cx, cy, flip=False):
    """Side-view car (9 x 5) centred on (cx, cy), facing right (or left when flipped), turned clockwise by deg."""
    body = [(-5, 1.5), (-5, -1), (-3.25, -1.5), (-2, -4.5), (1.5, -4.5), (2.75, -1.5), (5, -0.75), (5, 1.5)]
    wheels = [(-2.5, 1.75), (2.5, 1.75)]
    if flip:
        body = [(-x, y) for x, y in body][::-1]
        wheels = [(-x, y) for x, y in wheels]
    pts = rot([(cx + x, cy + y) for x, y in body], deg, cx, cy)
    ws = rot([(cx + x, cy + y) for x, y in wheels], deg, cx, cy)
    return [shell(poly(pts, closed=True, r=S.r * 0.5)), *[dot(x, y, 1.5) for x, y in ws]]


@icon("car-collision", CAT, "Two small cars meeting nose to nose at an angle with a starburst at the point of impact",
      tags=["car accident", "crash", "collision", "auto insurance", "motor claim", "fender bender"])
def _(S):
    burst = [polar(12, 5, 3 if i % 2 == 0 else 1.4, -90 + i * 45) for i in range(8)]
    return [
        *car_side(S, -8, 6.5, 16.5),
        *car_side(S, 8, 17.5, 16.5, flip=True),
        shell(poly(burst, closed=True, r=S.r * 0.2), stroke_miterlimit="8"),
    ]


@icon("property-value", CAT, "House with a small rising bar chart beside it",
      tags=["home value", "property valuation", "house price growth", "appreciation", "real estate market", "appraisal"])
def _(S):
    return [
        shell(house(S, 2.5, 10, 9, 21.5)),
        line(seg(13.5, 21.5, 13.5, 16.5) if S.name == "line" else seg(13.5, 21, 13.5, 17)),
        line(seg(17.25, 21.5, 17.25, 12) if S.name == "line" else seg(17.25, 21, 17.25, 12.5)),
        line(seg(21, 21.5, 21, 7) if S.name == "line" else seg(21, 21, 21, 7.5)),
    ]


@icon("house-price-tag", CAT, "House with a price tag hanging from the corner of its roof",
      tags=["house for sale", "home price", "property price", "real estate", "asking price", "listing"])
def _(S):
    tag = [(19, 12), (21.5, 14.5), (21.5, 21.5), (16.5, 21.5), (16.5, 14.5)]
    return [
        shell(house(S, 3.5, 14.5, 4, 21.5, eave=10.5)),
        line(poly([(15, 10), (19, 12)], r=0)),
        shell(poly(tag, closed=True, r=S.r * 0.5)),
        dot(19, 15.25, 1),
        door(S, 9, 3, 16.5, 21.5),
    ]


@icon("housing-estate", CAT, "Three identical small houses in a row along a curved street",
      tags=["housing development", "subdivision", "neighbourhood", "neighborhood", "residential estate", "suburb"])
def _(S):
    parts = []
    for cx, top in ((4.5, 7), (12, 4), (19.5, 7)):
        parts.append(shell(house(S, cx - 2.5, cx + 2.5, top, top + 9)))
    parts.append(line("M2 21.5Q12 16.5 22 21.5"))
    return parts


@icon("gated-community", CAT, "Two small houses behind a closed double gate between two pillars",
      tags=["gated estate", "private estate", "security gate", "residential", "gatehouse", "exclusive"])
def _(S):
    return [
        shell(cut(house(S, 5.5, 11, 2.5, 16), rect(2.5, 13.5, 19, 8))),
        shell(cut(house(S, 13, 18.5, 2.5, 16), rect(2.5, 13.5, 19, 8))),
        shell(rect(2, 12.5, 3, 9, rr(S, 1))),
        shell(rect(19, 12.5, 3, 9, rr(S, 1))),
        line(seg(5, 15.5, 19, 15.5)),
        line(seg(8.5, 15.5, 8.5, 21.5)), line(seg(12, 15.5, 12, 21.5)), line(seg(15.5, 15.5, 15.5, 21.5)),
    ]


@icon("zoning-map", CAT, "Street grid of four city blocks, each marked with a different fill pattern",
      tags=["zoning", "land use", "planning map", "urban planning", "city blocks", "district map"])
def _(S):
    k = rr(S, 1.5)
    return [
        shell(rect(3, 3, 7.5, 7.5, k)), sq(5, 5, 3.5, 3.5, 0 if S.name == "line" else 1),
        shell(rect(13.5, 3, 7.5, 7.5, k)), detail(seg(13.5, 10.5, 21, 3)),
        shell(rect(3, 13.5, 7.5, 7.5, k)), detail(seg(3, 17.25, 10.5, 17.25)),
        shell(rect(13.5, 13.5, 7.5, 7.5, k)),
    ]


@icon("eviction-notice", CAT, "Front door with a sheet of paper taped to its centre",
      tags=["eviction", "notice to quit", "tenant", "landlord", "lease termination", "rental"])
def _(S):
    return [
        line(poly([(5, 21.5), (5, 2.5), (19, 2.5), (19, 21.5)], r=S.r)),
        line(seg(2, 21.5, 22, 21.5) if S.name == "line" else seg(2.5, 21.5, 21.5, 21.5)),
        shell(rect(8.5, 6.5, 7, 8.5, rr(S, 1))),
        detail(seg(10.5, 9.5, 13.5, 9.5)), detail(seg(10.5, 12.5, 13.5, 12.5)),
        mark(16.25, 18, S, 1),
    ]


@icon("virtual-tour", CAT, "House inside a circular 360 degree orbit arrow",
      tags=["360 tour", "virtual viewing", "3d tour", "online viewing", "walkthrough", "real estate"])
def _(S):
    tip = polar(12, 12, 9.5, 245)
    return [
        line(arc(12, 12, 9.5, -45, 245)),
        line(poly(head(tip, 335, 2.5), r=S.r * 0.5)),
        shell(house(S, 8, 16, 7, 16.5)),
        mark(12, 13.75, S, 1),
    ]


@icon("property-listing", CAT, "Listing card with a house photo on top and a price and details below",
      tags=["real estate listing", "home for sale", "rental listing", "property ad", "house listing", "realtor"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 2.5))),
        detail(house(S, 8.5, 15.5, 5, 11.5)),
        detail(seg(7.5, 15, 13, 15)),
        detail(seg(7.5, 18.5, 16.5, 18.5)),
    ]


@icon("open-house", CAT, "House with its front door open and a small balloon tied beside it",
      tags=["open house", "viewing", "house showing", "real estate event", "welcome", "home tour"])
def _(S):
    return [
        shell(house(S, 2.5, 15, 5, 21.5)),
        sq(6.5, 14, 4.5, 7.5, 0 if S.name == "line" else 1),
        shell(ellipse(19.25, 6.5, 2.75, 3.5)),
        line("M19.25 10Q18 14 19.25 17.5T19.25 21.5"),
    ]


@icon("home-equity", CAT, "House outline with a shaded pie wedge inside it",
      tags=["home equity", "equity loan", "heloc", "ownership share", "mortgage", "property value"])
def _(S):
    return [
        shell(house(S, 3, 21, 3, 21.5, eave=10)),
        detail(circle(12, 15, 3.75)),
        Part("dot", f"M12 15V11.25A3.75 3.75 0 0 1 15.75 15Z"),
    ]


@icon("home-inspection", CAT, "House with a clipboard in front of its lower right corner",
      tags=["home inspection", "property survey", "building inspection", "house check", "surveyor", "checklist"])
def _(S):
    board = rect(13, 12.5, 8.5, 9, rr(S, 1.5))
    return [
        shell(cut(house(S, 2.5, 17.5, 2.5, 21, eave=10), board, rect(15, 11, 4.5, 2.5))),
        shell(board),
        shell(rect(15, 11, 4.5, 2.5, rr(S, 1))),
        detail(poly([(15, 17), (16.5, 18.5), (19.5, 15.5)], r=S.r * 0.3)),
    ]


# ============================================================================ law and justice

def pan(cx, y, S):
    """Hanging scale pan: two cords to a bowl."""
    return [
        line(poly([(cx - 3, y), (cx, y - 7), (cx + 3, y)], r=S.r * 0.3)),
        shell(f"M{fmt(cx - 3.5)} {fmt(y)}H{fmt(cx + 3.5)}A3.5 3 0 0 1 {fmt(cx - 3.5)} {fmt(y)}Z"),
    ]


@icon("scales-of-justice", CAT, "Balance scale with two hanging pans on a tall centre post and a round base",
      tags=["justice", "law", "legal", "balance", "fairness", "court"])
def _(S):
    return [
        dot(12, 3.5, 1.5),
        line(seg(12, 5, 12, 18.5)),
        line(seg(5.5, 6.5, 18.5, 6.5)),
        *pan(5.5, 13.5, S), *pan(18.5, 13.5, S),
        shell("M7.5 21.5A4.5 3 0 0 1 16.5 21.5Z"),
    ]


@icon("judge-bench", CAT, "Raised courtroom bench with a panelled front and a high backed chair behind it",
      tags=["judge's bench", "courtroom", "court", "magistrate", "tribunal", "legal"])
def _(S):
    return [
        shell(cut("M8.5 16V5A3.5 3 0 0 1 15.5 5V16Z" if S.name == "rounded" else
                  poly([(8.5, 16), (8.5, 3.5), (12, 2), (15.5, 3.5), (15.5, 16)], closed=True), rect(2, 13.5, 20, 8))),
        shell(rect(2, 13.5, 20, 8, rr(S, 1.5))),
        detail(seg(2, 16, 22, 16)),
        detail(seg(8.5, 16, 8.5, 21.5)), detail(seg(15.5, 16, 15.5, 21.5)),
        shell(rect(18, 6.5, 4, 3, rr(S, 1))), line(seg(17.5, 11.5, 22, 11.5) if S.name == "line" else seg(18, 11.5, 21.5, 11.5)),
    ]


@icon("jury-box", CAT, "Railed jury box with two staggered rows of heads behind the rail",
      tags=["jury", "jurors", "courtroom", "trial", "peers", "verdict"])
def _(S):
    parts = [dot(x, 4.5, 1.75) for x in (7, 12, 17)]
    parts += [dot(x, 9, 1.75) for x in (4.5, 9.5, 14.5, 19.5)]
    parts += [shell(rect(2, 13, 20, 8.5, rr(S, 3))), detail(seg(2, 16, 22, 16))]
    parts += [detail(seg(x, 16, x, 21.5)) for x in (7, 12, 17)]
    return parts


@icon("witness-stand", CAT, "Enclosed witness box with a railing, a chair back and a microphone on a gooseneck",
      tags=["witness box", "testimony", "courtroom", "trial", "testify", "court"])
def _(S):
    return [
        dot(8, 4.5, 2.25),
        shell(cut("M3.5 12V11A4.5 3.5 0 0 1 12.5 11V12Z", rect(2, 13, 20, 8.5))),
        shell(rect(2, 13, 20, 8.5, rr(S, 1.5))),
        detail(seg(2, 16, 22, 16)),
        line("M17 13V10C17 8 15.5 7.5 15.5 5.5" if S.name == "rounded" else "M17 13V9.5L15.5 7.5V5.5"),
        shell(ellipse(15.5, 3.75, 1.75, 1.75) if S.name == "rounded" else rect(13.75, 2, 3.5, 3.5, 0.5)),
    ]


def band(p0, p1, w):
    """Straight strip of width w from p0 to p1 (a closed rectangle d)."""
    a = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    nx, ny = -math.sin(a) * w / 2, math.cos(a) * w / 2
    return poly([(p0[0] + nx, p0[1] + ny), (p1[0] + nx, p1[1] + ny), (p1[0] - nx, p1[1] - ny), (p0[0] - nx, p0[1] - ny)],
                closed=True)


def stripes(p0, p1, w, n, clear=None):
    """Diagonal solid stripes along a strip (knocked out of it in Filled)."""
    out = []
    a = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    L = math.dist(p0, p1)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    h = (w - 2) / 2 - 0.2
    for i in range(n):
        t = L * (i + 0.5) / n
        cx, cy = p0[0] + ux * t, p0[1] + uy * t
        q = [(cx + nx * h - ux * 0.2, cy + ny * h - uy * 0.2), (cx + nx * h + ux * 1.6, cy + ny * h + uy * 1.6),
             (cx - nx * h + ux * 0.2, cy - ny * h + uy * 0.2), (cx - nx * h - ux * 1.6, cy - ny * h - uy * 1.6)]
        d = poly(q, closed=True)
        if clear is not None:
            if abs(D(P(d), clear).area) < abs(P(d).area) * 0.999:
                continue
        out.append(Part("dot", d))
    return out


@icon("crime-scene-tape", CAT, "Two crossing strips of striped barrier tape",
      tags=["police tape", "barrier tape", "caution tape", "do not cross", "crime scene", "investigation"])
def _(S):
    a0, a1, w = (3.2, 3.2), (20.8, 20.8), 5
    b0, b1 = (3.2, 20.8), (20.8, 3.2)
    top = band(b0, b1, w)
    under = cut(band(a0, a1, w), top, gap=1.0)
    keep = U(P(top), ST(top, 4, "round", "round"))
    return [
        shell(under), *stripes(a0, a1, w, 7, clear=keep),
        shell(top), *stripes(b0, b1, w, 7),
    ]


@icon("pillory", CAT, "Pillory: a post holding a hinged board with a large head hole between two small wrist holes",
      tags=["stocks", "punishment", "medieval", "public shaming", "history", "justice"])
def _(S):
    return [
        shell(rect(2, 5, 20, 7, rr(S, 1.5))),
        detail(seg(2, 8.5, 22, 8.5)),
        Part("dot", circle(12, 8.5, 2.25)),
        Part("dot", circle(5.5, 8.5, 1.1)), Part("dot", circle(18.5, 8.5, 1.1)),
        line(seg(12, 12, 12, 21.5)),
        line(seg(7, 21.5, 17, 21.5) if S.name == "line" else seg(7.5, 21.5, 16.5, 21.5)),
        line(seg(12, 2, 12, 5)),
    ]



# ============================================================================ police

@icon("sheriff-badge", CAT, "Six pointed star badge with a small ball on the tip of each point",
      tags=["sheriff", "marshal", "lawman", "star badge", "western", "deputy"])
def _(S):
    star = []
    for i in range(6):
        star += [polar(12, 12, 8, -90 + i * 60), polar(12, 12, 3.9, -60 + i * 60)]
    parts = [shell(poly(star, closed=True, r=S.r * 0.3), stroke_miterlimit="8")]
    parts += [solid(circle(*polar(12, 12, 8.5, -90 + i * 60), 1.6)) for i in range(6)]
    parts.append(dot(12, 12, 1.25))
    return parts


SHIELD = "M12 2.5L19.5 5.5V11C19.5 16 16.5 19.5 12 21.5C7.5 19.5 4.5 16 4.5 11V5.5Z"
SHIELD_R = "M11.3 2.8Q12 2.5 12.7 2.8L18.5 5.1Q19.5 5.5 19.5 6.6V11C19.5 16 16.5 19.5 12 21.5C7.5 19.5 4.5 16 4.5 11V6.6Q4.5 5.5 5.5 5.1Z"


@icon("police-badge", CAT, "Shield shaped badge with a star in the centre and a banner across its lower part",
      tags=["police", "officer", "law enforcement", "badge", "cop", "security"])
def _(S):
    ban = rect(2.5, 14, 19, 4, rr(S, 1))
    star = [polar(12, 9.25, 3.2 if i % 2 == 0 else 1.35, -90 + i * 36) for i in range(10)]
    return [
        shell(cut(SHIELD if S.name == "line" else SHIELD_R, ban, gap=0.01)),
        Part("dot", poly(star, closed=True)),
        shell(ban),
    ]


@icon("police-cap", CAT, "Peaked police cap with a stiff visor and a badge on the front band",
      tags=["police hat", "officer cap", "peaked cap", "uniform", "cop", "patrol"])
def _(S):
    outline = ("M3 10C3 6.5 7 4 12 4C17 4 21 6.5 21 10L18 11V15.5C19 16 19.5 17 19.5 17.5C19.5 19.5 16 20.5 12 20.5"
               "C8 20.5 4.5 19.5 4.5 17.5C4.5 17 5 16 6 15.5V11Z")
    if S.name == "line":
        outline = ("M3 10C3 6.5 7 4 12 4C17 4 21 6.5 21 10L18 11V15.5L19.5 17.5C19.5 19.5 16 20.5 12 20.5"
                   "C8 20.5 4.5 19.5 4.5 17.5L6 15.5V11Z")
    return [
        shell(outline, stroke_miterlimit="8"),
        detail(seg(6, 11, 18, 11)),
        detail("M6 15.5C9.5 16.7 14.5 16.7 18 15.5"),
        mark(12, 8, S, 1.25),
    ]


# ============================================================================ documents and crime

@icon("contract-redline", CAT, "Contract page with some lines struck through and a pen writing in the margin",
      tags=["redline", "track changes", "markup", "contract review", "edit", "legal draft"])
def _(S):
    page = [(3, 2.5), (11, 2.5), (15, 6.5), (15, 21.5), (3, 21.5)]
    return [
        shell(poly(page, closed=True, r=S.r)),
        detail(seg(6, 9.5, 12, 9.5)),
        detail(poly([(5.5, 15), (7.5, 12), (9, 15), (11, 12), (12.5, 15)], r=S.r * 0.3), stroke_miterlimit="8"),
        detail(seg(6, 17.5, 10, 17.5)),
        shell(poly(rot([(18.25, 3), (20.75, 3), (20.75, 15.5), (19.5, 18.5), (18.25, 15.5)], 0, 19.5, 12), closed=True,
                   r=S.r * 0.4)),
        detail(seg(18.25, 6, 20.75, 6)),
    ]


@icon("bribery", CAT, "Envelope with a banknote peeking out, sliding under the edge of a table",
      tags=["bribe", "corruption", "under the table", "kickback", "payoff", "fraud"])
def _(S):
    env = rect(9.5, 12.5, 11, 7.5, rr(S, 1.5))
    note = rect(11.5, 9, 7, 6)
    return [
        line(seg(2, 5, 22, 5) if S.name == "line" else seg(2.5, 5, 21.5, 5)),
        line(seg(19.5, 5, 19.5, 9)),
        shell(cut(note, env)),
        shell(env),
        detail(poly([(9.5, 12.5), (15, 16.5), (20.5, 12.5)], r=S.r * 0.5)),
        line(seg(2.5, 14, 6.5, 14)), line(seg(4, 18.5, 6.5, 18.5)),
    ]


@icon("money-laundering", CAT, "Front loading washing machine with a banknote tumbling in its drum",
      tags=["laundering", "dirty money", "financial crime", "fraud", "illicit funds", "aml"])
def _(S):
    note = [(9.5, 12), (15.5, 13.5), (14.5, 17.5), (8.5, 16)]
    return [
        shell(rect(3.5, 2.5, 17, 19, rr(S, 3))),
        detail(seg(3.5, 6.5, 20.5, 6.5)),
        dot(16.5, 4.5, 1),
        detail(circle(12, 14.5, 5.5)),
        Part("dot", poly(note, closed=True)),
    ]


def _pyramid_filled():
    out = []
    for row, xs in ((0, (12,)), (1, (8.25, 15.75)), (2, (4.5, 12, 19.5))):
        for cx in xs:
            y = 3.5 + row * 7
            out += [P(circle(cx, y, 1.9)), P(f"M{fmt(cx - 2.75)} {fmt(y + 5.75)}V{fmt(y + 5)}A2.75 2.75 0 0 1 {fmt(cx + 2.75)} {fmt(y + 5)}V{fmt(y + 5.75)}Z")]
    return U(*out)


@icon("pyramid-scheme", CAT, "Pyramid built from rows of small people, with one person at the top",
      tags=["ponzi scheme", "mlm", "multi level marketing", "fraud", "scam", "recruitment"], filled=_pyramid_filled)
def _(S):
    def person(cx, y):
        r = 2.5
        body = (f"M{fmt(cx - r)} {fmt(y + 5.5)}V{fmt(y + 5)}A{r} {r} 0 0 1 {fmt(cx + r)} {fmt(y + 5)}V{fmt(y + 5.5)}Z"
                if S.name == "rounded" else
                poly([(cx - r, y + 5.5), (cx - r, y + 4), (cx - 1.25, y + 2.75), (cx + 1.25, y + 2.75), (cx + r, y + 4),
                      (cx + r, y + 5.5)], closed=True))
        return [dot(cx, y, 1.5), solid(body)]
    parts = []
    for row, xs in ((0, (12,)), (1, (8.25, 15.75)), (2, (4.5, 12, 19.5))):
        for x in xs:
            parts += person(x, 3.5 + row * 7)
    return parts



# ============================================================================ retail and logistics (2)

@icon("product-lightbox", CAT, "Cube shaped photo tent seen from the open front, with a product box standing inside",
      tags=["photo tent", "light tent", "product photography", "light box", "studio", "ecommerce photo"])
def _(S):
    k = S.r * 0.3
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 1.5))),
        detail(seg(2.5, 2.5, 7, 7)), detail(seg(21.5, 2.5, 17, 7)),
        detail(seg(2.5, 21.5, 7, 17)), detail(seg(21.5, 21.5, 17, 17)),
        detail(poly([(7, 17), (7, 7), (17, 7), (17, 17)], r=k)),
        sq(9.75, 12.5, 4.5, 4.5, 0 if S.name == "line" else 1),
    ]


def factory(S, x0, x1, ybot, ytop):
    """Small factory: saw-tooth roof of three teeth over a wide block."""
    w = (x1 - x0) / 3
    pts = [(x0, ybot), (x0, ytop + 3)]
    for i in range(3):
        pts.append((x0 + w * (i + 1), ytop))
        if i < 2:
            pts.append((x0 + w * (i + 1), ytop + 3))
    pts.append((x1, ybot))
    return poly(pts, closed=True, r=S.r * 0.4)


@icon("supply-chain", CAT, "Factory and shop linked by an arrow that carries goods from one to the other",
      tags=["supply chain", "logistics", "distribution", "manufacturer to retailer", "sourcing", "fulfilment"])
def _(S):
    shop = [(14, 21.5), (14, 14), (22, 14), (22, 21.5)]
    return [
        shell(factory(S, 2, 10.5, 21.5, 13)),
        shell(poly(shop, closed=True, r=S.r * 0.5)),
        detail(seg(16.75, 21.5, 16.75, 17.5) if S.name == "line" else seg(16.75, 21.5, 16.75, 18)),
        line(seg(13.5, 11, 22.5, 11) if S.name == "line" else seg(14, 11, 22, 11)),
        line(arc(12, 11, 6.25, 200, 335)),
        line(poly(head(polar(12, 11, 6.25, 335), 60, 2.25), r=S.r * 0.5)),
    ]


# ============================================================================ law (2)

@icon("lady-justice", CAT, "Robed figure of justice with a blindfold, raising scales in one hand and holding a sword down in the other",
      tags=["lady justice", "justitia", "justice", "law", "court", "impartial", "blind justice"])
def _(S):
    robe = [(11.5, 9), (14.5, 9), (17, 21.5), (9, 21.5)]
    return [
        shell(circle(13, 4.5, 2.25)),
        line(seg(10.5, 4, 15.5, 4)),
        shell(poly(robe, closed=True, r=S.r * 0.6)),
        line(seg(11.5, 10, 6, 6)),
        line(seg(2.5, 6, 9.5, 6)),
        line(seg(3.5, 6, 3.5, 8)), line(seg(8.5, 6, 8.5, 8)),
        solid("M2 8.5H5A1.5 1.5 0 0 1 2 8.5Z"), solid("M7 8.5H10A1.5 1.5 0 0 1 7 8.5Z"),
        line(seg(14.5, 10, 20, 12)),
        line(seg(20, 11, 20, 21.5)),
        line(seg(18.5, 13.5, 21.5, 13.5)),
    ]


# ============================================================================ elections and civic life

@icon("voting-booth", CAT, "Voting booth with a tick on its top panel and a short curtain with a voter's legs showing below",
      tags=["polling booth", "voting station", "election", "polling place", "ballot", "vote"])
def _(S):
    curtain = ("M7.5 9H16.5V14.5A1.5 1.5 0 0 1 13.5 14.5A1.5 1.5 0 0 1 10.5 14.5A1.5 1.5 0 0 1 7.5 14.5Z")
    return [
        shell(rect(2.5, 2.5, 19, 6.5, rr(S, 1.5))),
        detail(poly([(9.5, 6), (11, 7.25), (14, 4.75)], r=S.r * 0.3)),
        line(seg(4, 9, 4, 21.5)), line(seg(20, 9, 20, 21.5)),
        shell(curtain),
        line(seg(10.5, 18, 10.5, 21.5)), line(seg(13.5, 18, 13.5, 21.5)),
    ]


@icon("mail-in-ballot", CAT, "Envelope with a ballot paper partly pulled out, showing a tick",
      tags=["postal vote", "absentee ballot", "vote by mail", "postal ballot", "election", "ballot paper"])
def _(S):
    env = rect(2.5, 11.5, 19, 10, rr(S, 1.5))
    paper = rect(6, 2.5, 12, 12, rr(S, 1))
    return [
        shell(cut(paper, env)),
        detail(poly([(8.5, 6.5), (10.5, 8.5), (15, 4.5)], r=S.r * 0.3)),
        shell(env),
        detail(poly([(2.5, 21.5), (12, 15), (21.5, 21.5)], r=S.r * 0.5)),
    ]


@icon("electronic-voting-machine", CAT, "Touchscreen voting unit on a stand with a privacy hood around the screen",
      tags=["evm", "e-voting", "voting terminal", "touchscreen vote", "election", "ballot machine"])
def _(S):
    hood = [(2.5, 3), (21.5, 3), (18.5, 15), (5.5, 15)]
    return [
        shell(poly(hood, closed=True, r=S.r * 0.6)),
        detail(rect(7.5, 6, 9, 6, rr(S, 1))),
        line(seg(12, 15, 12, 20)),
        line(seg(7, 21, 17, 21) if S.name == "line" else seg(7.5, 21, 16.5, 21)),
    ]


@icon("residence-permit", CAT, "Identity card with a small globe on the left and text lines on the right",
      tags=["residence card", "resident permit", "immigration", "visa", "green card", "id card"])
def _(S):
    return [
        shell(rect(2, 4.5, 20, 15, rr(S, 2.5))),
        detail(circle(7.75, 12, 3)),
        detail(seg(4.75, 12, 10.75, 12)),
        detail(seg(13.5, 10, 18.5, 10)), detail(seg(13.5, 14, 17, 14)),
    ]


@icon("public-notice-board", CAT, "Notice board on two legs under a small roof with papers pinned to it",
      tags=["notice board", "bulletin board", "community board", "announcements", "public notice", "information board"])
def _(S):
    return [
        line(poly([(2.5, 7), (12, 2.5), (21.5, 7)], r=S.r * 0.6)),
        shell(rect(4, 9, 16, 8.5, rr(S, 1.5))),
        sq(7, 11.5, 4, 4, 0 if S.name == "line" else 1),
        sq(13, 11.5, 4, 2.5, 0 if S.name == "line" else 0.75),
        line(seg(7, 17.5, 7, 21.5)), line(seg(17, 17.5, 17, 21.5)),
    ]


@icon("treaty", CAT, "Document with two round wax seals with ribbons side by side at the bottom",
      tags=["treaty", "agreement", "accord", "pact", "diplomacy", "signed document"])
def _(S):
    k = S.r * 0.2
    s1, s2 = circle(8.5, 15.5, 2.5), circle(15.5, 15.5, 2.5)
    page = rect(4, 2.5, 16, 15, rr(S, 2))

    def ribbon(x):
        return solid(poly([(x - 1.75, 17), (x + 1.75, 17), (x + 1.75, 21.5), (x, 20.25), (x - 1.75, 21.5)], closed=True, r=k))
    return [
        shell(cut(page, s1, s2)),
        detail(seg(7.5, 6.5, 16.5, 6.5)), detail(seg(7.5, 9.5, 13.5, 9.5)),
        ribbon(8.5), ribbon(15.5),
        shell(s1), shell(s2),
    ]


@icon("mayoral-chain", CAT, "Linked chain of office hanging in a U with a large round medallion at the bottom",
      tags=["chain of office", "mayor", "livery collar", "civic regalia", "ceremony", "council"])
def _(S):
    parts = [line("M4 2.5C4 9 7.5 12.5 12 12.5C16.5 12.5 20 9 20 2.5")]
    for t in (0.12, 0.34, 0.66, 0.88):
        x = (1 - t) ** 3 * 4 + 3 * (1 - t) ** 2 * t * 4 + 3 * (1 - t) * t ** 2 * 7.5 + t ** 3 * 12
        y = (1 - t) ** 3 * 2.5 + 3 * (1 - t) ** 2 * t * 9 + 3 * (1 - t) * t ** 2 * 12.5 + t ** 3 * 12.5
        parts += [dot(x, y, 1.6), dot(24 - x, y, 1.6)]
    parts += [shell(circle(12, 17, 4.5)), dot(12, 17, 1.4)]
    return parts


def debater(S, cx, mic_dx):
    """Person standing behind a lectern, with a microphone arm reaching towards the middle."""
    lect = [(cx - 3.5, 13), (cx + 3.5, 13), (cx + 2.5, 21.5), (cx - 2.5, 21.5)]
    lectern = poly(lect, closed=True, r=S.r * 0.5)
    shoulders = f"M{fmt(cx - 3.5)} 13V12.5A3.5 3.5 0 0 1 {fmt(cx + 3.5)} 12.5V13Z"
    mx = cx + mic_dx
    return [
        dot(cx, 5, 2.25),
        solid(path_to_d(D(P(shoulders), U(P(lectern), ST(lectern, 4, "round", "round"))))),
        shell(lectern),
        line(f"M{fmt(cx + mic_dx * 0.45)} 13L{fmt(mx)} 9.5"),
        solid(circle(mx, 8.75, 1.4)),
    ]


@icon("debate-podiums", CAT, "Two speakers behind lecterns facing each other, each with a microphone",
      tags=["debate", "podiums", "lecterns", "election debate", "candidates", "discussion"])
def _(S):
    return debater(S, 5.5, 4.5) + debater(S, 18.5, -4.5)


@icon("summit-round-table", CAT, "Round table with small national flag stands in a row along its top",
      tags=["summit", "round table", "negotiation", "diplomacy", "international meeting", "conference"])
def _(S):
    parts = [shell(ellipse(12, 15, 9.5, 3.5)), line(seg(12, 18.5, 12, 21.5))]
    for x in (4.5, 11, 17.5):
        parts += [line(seg(x, 14, x, 4.5)),
                  solid(poly([(x + 1, 4), (x + 4.5, 6), (x + 1, 8)], closed=True, r=S.r * 0.3))]
    return parts


@icon("census-form", CAT, "Form with a small house at the top and rows of tick boxes below",
      tags=["census", "household survey", "population count", "questionnaire", "government form", "survey"])
def _(S):
    k = 0 if S.name == "line" else 0.6
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 2))),
        detail(poly([(9, 10.5), (9, 7.5), (12, 5), (15, 7.5), (15, 10.5)], closed=True, r=S.r * 0.3)),
        sq(7, 13, 2.5, 2.5, k), detail(seg(11.5, 14.25, 17, 14.25)),
        sq(7, 17, 2.5, 2.5, k), detail(seg(11.5, 18.25, 15.5, 18.25)),
    ]


def _perforated():
    body = P(rect(3, 3, 18, 18))
    holes = []
    for i in range(6):
        t = 3 + 18 * (i + 0.5) / 6
        holes += [P(circle(t, 3, 1)), P(circle(t, 21, 1)), P(circle(3, t, 1)), P(circle(21, t, 1))]
    return path_to_d(D(body, U(*holes)))


CROWN = [(8, 16), (8, 9.5), (10, 12), (12, 8.5), (14, 12), (16, 9.5), (16, 16)]


def _stamp_filled():
    holes = []
    for i in range(6):
        t = 2 + 20 * (i + 0.5) / 6
        holes += [P(circle(t, 2, 1.5)), P(circle(t, 22, 1.5)), P(circle(2, t, 1.5)), P(circle(22, t, 1.5))]
    return D(D(P(rect(2, 2, 20, 20)), U(*holes)), P(poly(CROWN, closed=True)))


@icon("tax-stamp", CAT, "Perforated revenue stamp with a crown in its centre",
      tags=["revenue stamp", "duty stamp", "excise", "stamp duty", "tax", "postage stamp"], filled=_stamp_filled)
def _(S):
    return [
        shell(_perforated()),
        Part("dot", poly(CROWN, closed=True, r=S.r * 0.25)),
    ]


@icon("food-bank-box", CAT, "Open donation box filled with a can and a loaf of bread, with a heart on its side",
      tags=["food bank", "food donation", "charity", "donation box", "food drive", "pantry"])
def _(S):
    box = rect(3, 12, 18, 9.5, rr(S, 1.5))
    loaf = "M12.5 12V9.5C12.5 7.5 14 6.5 16 6.5C18 6.5 19.5 7.5 19.5 9.5V12Z"
    heart = ("M12 20C10 18.7 9 17.6 9 16.5C9 15.6 9.7 15 10.5 15C11.2 15 11.7 15.4 12 15.9"
             "C12.3 15.4 12.8 15 13.5 15C14.3 15 15 15.6 15 16.5C15 17.6 14 18.7 12 20Z")
    return [
        shell(cut(rect(5.5, 5, 5, 8, rr(S, 1)), box)),
        shell(cut(loaf, box)),
        shell(box),
        Part("dot", heart),
    ]


@icon("krona-sign", CAT, "Krona currency abbreviation: the lowercase letters k and r",
      tags=["sek", "nok", "dkk", "isk", "krone", "kronor", "currency"], modifiers="none")
def _(S):
    return [
        line(seg(4.5, 3.5, 4.5, 20.5) if S.name == "line" else seg(4.5, 4, 4.5, 20)),
        line(poly([(11, 10), (5, 15.5)], r=0)), line(poly([(7.5, 13.5), (11.5, 20.5)], r=0) if S.name == "line" else seg(7.5, 13.5, 11.25, 20)),
        line(seg(15, 10, 15, 20.5) if S.name == "line" else seg(15, 10.5, 15, 20)),
        line("M15 15C15 12 17 10.25 20 10.25"),
    ]


@icon("ringgit-sign", CAT, "Malaysian ringgit abbreviation: the capital letters R and M",
      tags=["myr", "malaysia", "ringgit", "rm", "currency", "money"], modifiers="none")
def _(S):
    return [
        line(poly([(3, 20), (3, 4), (6.5, 4)], r=S.r * 0.5) + "A3.75 3.75 0 0 1 6.5 11.5H3"),
        line(seg(6, 11.5, 10, 20)),
        line(poly([(13, 20), (13, 4), (17, 13.5), (21, 4), (21, 20)], r=S.r * 0.4), stroke_miterlimit="2"),
    ]


@icon("rupiah-sign", CAT, "Indonesian rupiah abbreviation: a capital R followed by a lowercase p",
      tags=["idr", "indonesia", "rupiah", "rp", "currency", "money"], modifiers="none")
def _(S):
    return [
        line(poly([(3.5, 18), (3.5, 3.5), (7, 3.5)], r=S.r * 0.5) + "A3.75 3.75 0 0 1 7 11H3.5"),
        line(seg(6.5, 11, 10.5, 18)),
        line(seg(14, 9, 14, 21.5) if S.name == "line" else seg(14, 9.5, 14, 21)),
        shell(ellipse(17.25, 13.5, 3.25, 3.75) if S.name == "rounded" else
              "M14 10H17A3.5 3.5 0 0 1 17 17H14Z"),
    ]


@icon("dirham-sign", CAT, "Dirham sign: a capital D with two horizontal bars crossing its left side",
      tags=["aed", "uae", "dirham", "emirates", "currency", "money"], modifiers="none")
def _(S):
    return [
        line("M7 4H10.5A7.5 8 0 0 1 10.5 20H7Z" if S.name == "line" else "M8 4H10.5A7.5 8 0 0 1 10.5 20H8Q7 20 7 19V5Q7 4 8 4Z"),
        line(seg(3, 10, 13, 10) if S.name == "line" else seg(3.5, 10, 12.5, 10)),
        line(seg(3, 14, 13, 14) if S.name == "line" else seg(3.5, 14, 12.5, 14)),
    ]


def _trading_filled():
    phone = rect(4, 1, 16, 22, 3)
    knock = U(*[ST(seg(x, y0, x, y1), 2, "butt", "miter") for x, y0, y1 in ((8, 9, 15.5), (12, 6.5, 13), (16, 4, 10.5))],
              *[P(rect(x - 1.5, y0, 3, 3.5)) for x, y0 in ((8, 10.5), (12, 8), (16, 5.5))],
              ST(seg(9, 18.5, 15, 18.5), 2, "round", "round"))
    return D(P(phone), knock)


@icon("trading-app", CAT, "Smartphone showing rising candlestick bars above a buy button",
      tags=["trading app", "stock app", "investing app", "brokerage", "mobile trading", "candlestick"], filled=_trading_filled)
def _(S):
    k = 0 if S.name == "line" else 0.5
    parts = [shell(rect(5, 2, 14, 20, rr(S, 3)))]
    for x, y0, y1, b in ((8, 9, 15.5, 10.5), (12, 6.5, 13, 8), (16, 4, 10.5, 5.5)):
        parts += [detail(seg(x, y0 + 0.5, x, y1 - 0.5) if S.name == "rounded" else seg(x, y0, x, y1)),
                  Part("dot", rect(x - 1.5, b, 3, 3.5, k))]
    parts.append(detail(seg(9, 18.5, 15, 18.5)))
    return parts


@icon("debt-snowball", CAT, "Snowball with coins pressed into it rolling down a slope, a smaller ball above it",
      tags=["debt snowball", "pay off debt", "debt payoff", "snowball method", "momentum", "personal finance"])
def _(S):
    # slope y = 7 + 0.55 (x - 2)
    ang = math.atan(0.55)
    nx, ny = math.sin(ang), -math.cos(ang)

    def on_slope(x, r):
        y = 7 + 0.55 * (x - 2)
        return x + nx * (r + 1), y + ny * (r + 1)
    bx, by = on_slope(14.5, 5.5)
    sx, sy = on_slope(5, 1.6)
    return [
        line(seg(2, 7, 22, 18)),
        shell(circle(bx, by, 5.5)),
        dot(bx - 1.75, by - 1.5, 1.25), dot(bx + 1.75, by + 1.5, 1.25),
        dot(sx, sy, 1.6),
    ]


@icon("cut-credit-card", CAT, "Scissors cutting a payment card in two, the halves pulling apart",
      tags=["cancel card", "cut up card", "close account", "debt free", "credit card", "stop spending"])
def _(S):
    def half(x0, x1, deg, px):
        body = poly(rot([(x0, 13), (x1, 13), (x1, 21.5), (x0, 21.5)], deg, px, 21.5), closed=True, r=S.r * 0.5)
        stripe = seg(*rot([(x0, 16.25)], deg, px, 21.5)[0], *rot([(x1, 16.25)], deg, px, 21.5)[0])
        return [shell(body), detail(stripe)]
    return [
        *half(2.5, 10.5, -8, 10.5), *half(13.5, 21.5, 8, 13.5),
        shell(circle(8.5, 4.5, 2)), shell(circle(15.5, 4.5, 2)),
        line(seg(10, 6, 13.25, 12.5)), line(seg(14, 6, 10.75, 12.5)),
    ]


@icon("golden-parachute", CAT, "Open parachute canopy with a coin hanging from its lines",
      tags=["golden parachute", "severance", "executive payout", "exit package", "bonus", "compensation"])
def _(S):
    canopy = "M2.5 10A9.5 7.5 0 0 1 21.5 10A3.17 1.5 0 0 0 15.17 10A3.17 1.5 0 0 0 8.83 10A3.17 1.5 0 0 0 2.5 10Z"
    return [
        shell(canopy),
        line(seg(3, 11, 10, 16.5)), line(seg(21, 11, 14, 16.5)),
        shell(circle(12, 18.5, 3)),
    ]


@icon("salary-bands", CAT, "Chart of three staggered horizontal bars stacked upward, each marked at its midpoint",
      tags=["pay bands", "salary range", "pay scale", "pay grade", "compensation", "salary structure"])
def _(S):
    k = 0.5 if S.name == "line" else 1.75
    parts = []
    for x0, y in ((2.5, 17.75), (7.5, 10.25), (12.5, 2.75)):
        parts += [shell(rect(x0, y, 9, 3.5, k)), detail(seg(x0 + 4.5, y, x0 + 4.5, y + 3.5))]
    return parts


@icon("pay-equity", CAT, "Level balance with a person standing on each end, equal in weight",
      tags=["pay equity", "equal pay", "pay gap", "fair pay", "gender pay", "equality"])
def _(S):
    def person(cx):
        return [dot(cx, 7, 2.25),
                solid(f"M{fmt(cx - 3.5)} 14.5V13.5A3.5 3.5 0 0 1 {fmt(cx + 3.5)} 13.5V14.5Z" if S.name == "rounded" else
                      poly([(cx - 3.5, 14.5), (cx - 3.5, 12), (cx - 2, 10.5), (cx + 2, 10.5), (cx + 3.5, 12), (cx + 3.5, 14.5)], closed=True))]
    return [
        *person(6), *person(18),
        line(seg(2, 16.5, 22, 16.5) if S.name == "line" else seg(2.5, 16.5, 21.5, 16.5)),
        shell(poly([(12, 18.5), (15, 21.5), (9, 21.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("candidate-shortlist", CAT, "Clipboard listing three candidates, one of them ticked",
      tags=["shortlist", "candidates", "hiring", "recruitment", "applicants", "selection"])
def _(S):
    return [
        shell(rect(3.5, 4, 17, 17.5, rr(S, 2.5))),
        shell(rect(8.5, 2.5, 7, 3, rr(S, 1))),
        dot(7.5, 9.5, 1.4), detail(seg(10.5, 9.5, 16.5, 9.5)),
        detail(poly([(6, 13.5), (7.25, 14.75), (9.5, 12.25)], r=S.r * 0.3)), detail(seg(11.5, 13.75, 16.5, 13.75)),
        dot(7.5, 18, 1.4), detail(seg(10.5, 18, 16.5, 18)),
    ]


@icon("employee-handbook", CAT, "Closed book with a person figure and two text lines on its cover",
      tags=["staff handbook", "employee manual", "company policies", "onboarding", "hr handbook", "code of conduct"])
def _(S):
    shoulders = ("M10.5 13.5V12.75A2.75 2.75 0 0 1 16 12.75V13.5Z" if S.name == "rounded" else
                 poly([(10.5, 13.5), (10.5, 11.75), (11.75, 10.5), (14.75, 10.5), (16, 11.75), (16, 13.5)], closed=True))
    return [
        shell(rect(4, 2.5, 16, 19, rr(S, 2))),
        detail(seg(7.5, 2.5, 7.5, 21.5)),
        dot(13.25, 7, 1.75), Part("dot", shoulders),
        detail(seg(10.5, 17, 16, 17)),
    ]


@icon("brand-guidelines", CAT, "Open book with colour swatches on the left page and a logo mark on the right page",
      tags=["brand book", "style guide", "brand guide", "brand identity", "design system", "visual identity"])
def _(S):
    book = ("M12 5.5C10 4 6 3.5 2.5 4V19.5C6 19 10 19.5 12 21C14 19.5 18 19 21.5 19.5V4C18 3.5 14 4 12 5.5Z")
    if S.name == "line":
        book = "M12 5.5L2.5 4V19.5L12 21L21.5 19.5V4Z"
    k = 0 if S.name == "line" else 0.75
    return [
        shell(book, stroke_miterlimit="8"),
        detail(seg(12, 5.5, 12, 21)),
        Part("dot", rect(5, 8, 4.5, 3.5, k)), Part("dot", rect(5, 13.5, 4.5, 3.5, k)),
        detail(circle(16.75, 12.5, 2.25)),
    ]


@icon("search-ad", CAT, "Browser window with a search field and a first result marked with a small ad tag",
      tags=["search ads", "paid search", "ppc", "sponsored result", "sem", "pay per click"])
def _(S):
    k = 0 if S.name == "line" else 0.75
    return [
        shell(rect(2.5, 3, 19, 18, rr(S, 2.5))),
        detail(seg(2.5, 7, 21.5, 7)),
        detail(rect(5.5, 10, 13, 3, rr(S, 1.5))),
        Part("dot", rect(5.5, 15.5, 4, 3, k)), detail(seg(12, 17, 18.5, 17)),
    ]


@icon("sms-marketing", CAT, "Smartphone with a message bubble on its screen and a megaphone in front of it",
      tags=["sms marketing", "text marketing", "bulk sms", "text campaign", "mobile marketing", "promotion"])
def _(S):
    cone = [(3, 9.5), (6.5, 9.5), (18.5, 4), (18.5, 20), (6.5, 14.5), (3, 14.5)]
    handle = [(8.5, 15.5), (9.5, 20.5), (12.5, 20.5), (12, 17.2)]
    raw = rot(cone + handle, -18, 12, 13)
    x1, y1 = max(p[0] for p in raw), max(p[1] for p in raw)

    def m(pts):
        return [(21.5 + (x - x1) * 0.6, 19.5 + (y - y1) * 0.6) for x, y in rot(pts, -18, 12, 13)]
    c_d = poly(m(cone), closed=True, r=S.r * 0.4)
    h_d = poly(m(handle), r=S.r * 0.4)
    phone = rect(2.5, 2.5, 9, 19, rr(S, 2.5))
    return [
        shell(cut(phone, c_d)),
        Part("dot", poly([(4.75, 6), (9.25, 6), (9.25, 9.5), (6.5, 9.5), (4.75, 11.25)], closed=True, r=S.r * 0.3)),
        shell(c_d),
        line(h_d),
    ]


@icon("shelf-wobbler", CAT, "Shelf edge with a round promotional sign sticking out on a thin strip",
      tags=["shelf wobbler", "shelf talker", "point of sale", "pos display", "promotion", "in store sign"])
def _(S):
    return [
        shell(rect(2.5, 3, 19, 4.5, rr(S, 1.5))),
        line(seg(12, 7.5, 12, 10)),
        shell(circle(12, 15.5, 5.5)),
        detail(seg(10, 18.5, 14, 12.5)),
        dot(10, 13.5, 1), dot(14, 17.5, 1),
    ]


def carton(S, x0, x1, y0, y1):
    return [shell(rect(x0, y0, x1 - x0, y1 - y0, rr(S, 1.5))),
            detail(seg((x0 + x1) / 2, y0, (x0 + x1) / 2, y0 + 3.5))]


@icon("buy-one-get-one", CAT, "Two identical boxes side by side with a plus sign above them",
      tags=["bogo", "buy one get one free", "two for one", "2 for 1", "deal", "offer"])
def _(S):
    return [
        *carton(S, 2.5, 10.5, 12.5, 21.5), *carton(S, 13.5, 21.5, 12.5, 21.5),
        line(seg(8, 6, 16, 6) if S.name == "line" else seg(8.5, 6, 15.5, 6)),
        line(seg(12, 2, 12, 10) if S.name == "line" else seg(12, 2.5, 12, 9.5)),
    ]


@icon("trade-in", CAT, "Old phone and new phone side by side with two swap arrows above them",
      tags=["trade in", "part exchange", "upgrade", "device swap", "exchange", "recycle phone"])
def _(S):
    return [
        *arrow(S, 5, 3.5, 19.5, 3.5, 2.25), *arrow(S, 19, 8, 4.5, 8, 2.25),
        shell(rect(2.5, 12.5, 7, 9, rr(S, 1.5))), detail(seg(2.5, 17, 9.5, 17)),
        shell(rect(14.5, 11.5, 7, 10, rr(S, 2))), detail(seg(16.5, 19, 19.5, 19)),
    ]


@icon("pink-slip", CAT, "Envelope with a paper slip sticking out of its top carrying a short line of text",
      tags=["dismissal notice", "layoff", "termination letter", "fired", "job loss", "redundancy", "notice"])
def _(S):
    return [
        line(poly([(6.5, 12.5), (6.5, 2.5), (17.5, 2.5), (17.5, 12.5)], r=S.r * 0.6)),
        detail(seg(9.5, 6.75, 14.5, 6.75)),
        shell(rect(2.5, 12.5, 19, 9, rr(S, 2))),
        detail(poly([(3, 13.5), (12, 18.5), (21, 13.5)], r=S.r * 0.4)),
    ]


@icon("campaign-button", CAT, "Round pin-back campaign button with a solid star in the centre",
      tags=["campaign pin", "election badge", "political button", "rosette", "pinback", "rally", "support badge"])
def _(S):
    star = []
    for i in range(10):
        star.append(polar(12, 12.5, 5.6 if i % 2 == 0 else (2.3 if S.name == "line" else 3.0), -90 + i * 36))
    return [
        shell(circle(12, 12, 9)),
        Part("dot", poly(star, closed=True, r=S.r * 0.6)),
    ]


@icon("inked-finger", CAT, "Fist with the index finger raised and a dark ink mark on the fingertip",
      tags=["voted", "election ink", "indelible ink", "ballot cast", "voting proof", "finger ink", "polling station"])
def _(S):
    body = ("M7.75 13V5.5A3.25 3.25 0 0 1 14.25 5.5V9.5H18A2.5 2.5 0 0 1 20.5 12V16.5A5 5 0 0 1 15.5 21.5H11.5"
            "A4.5 4.5 0 0 1 8 19.7L3.8 14.8A1.7 1.7 0 0 1 6.5 12.7L7.75 14Z")
    if S.name == "line":
        body = "M7.75 13V2.5H14.25V9.5H20.5V16.5L15.5 21.5H11.5A4.5 4.5 0 0 1 8 19.7L3.8 14.8A1.7 1.7 0 0 1 6.5 12.7L7.75 14Z"
    return [
        shell(body),
        Part("dot", rect(7.75, 2.5, 6.5, 4.5) if S.name == "line" else circle(11, 5.5, 2.0)),
    ]

