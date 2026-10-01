"""TypeIcon Core: retail and e-commerce (batch 001).

Product options, price tags, carts and checkout, point-of-sale hardware, payments, loyalty and promotions.
Generic objects only: no brand, bank, card network or shop logo.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import SCALE, fmt, path_to_d, polar

CAT = "retail"


# ============================================================================ helpers

def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def mark(d) -> Part:
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def sq(x, y, w, h, rx=0.0) -> Part:
    return Part("dot", rect(x, y, w, h, rx))


def head(tip, deg, size=2.5):
    a = polar(tip[0], tip[1], size * math.sqrt(2), deg + 180 - 45)
    b = polar(tip[0], tip[1], size * math.sqrt(2), deg + 180 + 45)
    return [a, tip, b]


def bolt_pts(cx, cy, k=1.0):
    base = [(1.5, -4.5), (-3, 1), (-0.5, 1), (-1.5, 4.5), (3, -1), (0.5, -1)]
    return [(cx + x * k, cy + y * k) for x, y in base]


def bolt(cx, cy, k=1.0) -> Part:
    return mark(poly(bolt_pts(cx, cy, k), closed=True))


def spark(cx, cy, r) -> Part:
    pts = [(0, -r), (r * .3, -r * .3), (r, 0), (r * .3, r * .3), (0, r), (-r * .3, r * .3), (-r, 0), (-r * .3, -r * .3)]
    return mark(poly([(cx + x, cy + y) for x, y in pts], closed=True))


def star_pts(cx, cy, ro, ri, n=5):
    return [polar(cx, cy, ro if i % 2 == 0 else ri, -90 + i * 180 / n) for i in range(2 * n)]


def pct(cx, cy, k=3.0, r=1.25):
    a = k + 0.75
    return [dot(cx - k, cy - k, r), dot(cx + k, cy + k, r), detail(seg(cx + a, cy - a, cx - a, cy + a))]


def tick(x, y):
    return [(x, y), (x + 1.25, y + 1.25), (x + 3.5, y - 1.25)]


def shirt_pts(cx, cy, s):
    base = [(8, 3), (3, 6), (5, 10), (7, 9), (7, 21), (17, 21), (17, 9), (19, 10), (21, 6), (16, 3)]
    return [(cx + (x - 12) * s, cy + (y - 12) * s) for x, y in base]


def shirt(S, cx, cy, s, neck=True):
    parts = [shell(poly(shirt_pts(cx, cy, s), closed=True, r=S.r * s))]
    if neck:
        x1, y1 = cx - 4 * s, cy - 9 * s
        parts.append(detail(f"M{fmt(x1)} {fmt(y1)}a{fmt(4 * s)} {fmt(4 * s)} 0 0 0 {fmt(8 * s)} 0"))
    return parts


def swing_pts(cx, top, w, h, cut=3.0):
    x0, x1 = cx - w / 2, cx + w / 2
    return [(x0 + cut, top), (x1 - cut, top), (x1, top + cut), (x1, top + h), (x0, top + h), (x0, top + cut)]


def swing(S, cx, top, w, h, cut=3.0, hole=True, k=1.0):
    """Hang tag with clipped top corners and a string hole."""
    parts = [shell(poly(swing_pts(cx, top, w, h, cut), closed=True, r=S.r * k))]
    if hole:
        parts.append(dot(cx, top + 3.0, 1.0))
    return parts


def diag_tag_pts(dx=0.0, dy=0.0, k=1.0):
    base = [(3, 3), (11, 3), (21, 13), (13, 21), (3, 11)]
    return [(12 + (x - 12) * k + dx, 12 + (y - 12) * k + dy) for x, y in base]


def box(S, x, y, w, h, tape=True, cap=2.5):
    parts = [shell(rect(x, y, w, h, rr(S, cap)))]
    if tape:
        parts.append(detail(seg(x + w / 2, y, x + w / 2, y + min(h * 0.4, 3))))
    return parts


def coin_parts(S, cx, cy, r, inner=True):
    parts = [shell(circle(cx, cy, r))]
    if inner:
        parts.append(detail(seg(cx - r * 0.35, cy, cx + r * 0.35, cy)))
    return parts


def card(S, x, y, w, h, stripe=True):
    parts = [shell(rect(x, y, w, h, rr(S, 3)))]
    if stripe:
        parts.append(detail(seg(x, y + 4, x + w, y + 4)))
    return parts


def phone(S, x, y, w, h):
    return [shell(rect(x, y, w, h, rr(S, 3)))]


def cart_parts(S, dx=0.0, dy=0.0):
    """Cart outline: handle, basket and two wheels (v0.1 cart proportions)."""
    basket = [(2, 3.5), (5, 3.5), (7.5, 15), (19, 15), (21, 7), (5.9, 7)]
    basket = [(x + dx, y + dy) for x, y in basket]
    return [line(poly(basket, r=S.r)), shell(circle(9 + dx, 19.5 + dy, 1.5)), shell(circle(18 + dx, 19.5 + dy, 1.5))]


def bag(S, x, y, w, h):
    cx = x + w / 2
    return [shell(rect(x, y, w, h, rr(S, 3))),
            line(f"M{fmt(cx - w * 0.28)} {fmt(y + 3.5)}V{fmt(y - 0.5)}A{fmt(w * 0.28)} {fmt(w * 0.28)} 0 0 1 {fmt(cx + w * 0.28)} {fmt(y - 0.5)}V{fmt(y + 3.5)}")]


def awning(S, x0, x1, y0, y1):
    return [shell(poly([(x0, y1), (x0 + 1.5, y0), (x1 - 1.5, y0), (x1, y1)], closed=True, r=S.r))]


def building(S, cx, top, w, h):
    """Bank: pediment, columns hint, base."""
    x0, x1 = cx - w / 2, cx + w / 2
    return [shell(poly([(x0, top + 4), (cx, top), (x1, top + 4)], closed=True, r=S.r * 0.5)),
            shell(rect(x0 + 1, top + 4, w - 2, h - 4, 0)),
            detail(seg(cx, top + 4, cx, top + h))]


# ============================================================================ product options and sizing

@icon("product-variants", CAT, "T-shirt beside three colour swatches; colour options for a product",
      tags=["colour options", "color options", "variants", "swatches", "product options", "shirt"])
def _(S):
    return [*shirt(S, 8.8, 12, 0.8),
            dot(20, 6.5, 1.9), dot(20, 12, 1.9), dot(20, 17.5, 1.9)]


@icon("size-guide", CAT, "T-shirt above a ruler with tick marks; a clothing size guide",
      tags=["sizing", "size chart", "measurements", "ruler", "fit", "clothing size"])
def _(S):
    return [*shirt(S, 12, 8.3, 0.66),
            shell(rect(3, 16.5, 18, 5, 0 if S.name == "line" else 1.5)),
            detail(seg(7, 16.5, 7, 19)), detail(seg(12, 16.5, 12, 19)), detail(seg(17, 16.5, 17, 19))]


@icon("size-selector", CAT, "Segmented selector with three options and the middle one selected; choose a size",
      tags=["size picker", "choose size", "options", "small medium large", "variant", "select"])
def _(S):
    return [shell(rect(2.5, 7, 19, 10, rr(S, 4))),
            detail(seg(9, 7, 9, 17)), detail(seg(15, 7, 15, 17)),
            sq(9, 7, 6, 10)]


def _shoe(S, x, y, k):
    pts = [(0, 0), (3, 0), (4, 2.5), (7, 3.5), (7, 5), (0, 5)]
    return shell(poly([(x + a * k, y + b * k) for a, b in pts], closed=True, r=S.r * 0.4))


@icon("fit-scale", CAT, "Slider with a knob in the middle and a small shoe above each end; how a product fits",
      tags=["fit", "runs small", "runs large", "true to size", "sizing", "slider"])
def _(S):
    return [_shoe(S, 2.5, 5, 0.85), _shoe(S, 14.5, 3.5, 1.15),
            line(seg(3, 18, 21, 18)), shell(circle(12, 18, 2.25))]


@icon("virtual-try-on", CAT, "Pair of glasses inside camera corner brackets with a sparkle; try products on virtually",
      tags=["try on", "augmented reality", "ar", "glasses", "fitting", "camera"], aliases=["try-on"])
def _(S):
    return [
        line(poly([(2.5, 8), (2.5, 3), (7.5, 3)], r=S.r)), line(poly([(16.5, 3), (21.5, 3), (21.5, 8)], r=S.r)),
        line(poly([(2.5, 16), (2.5, 21), (7.5, 21)], r=S.r)), line(poly([(16.5, 21), (21.5, 21), (21.5, 16)], r=S.r)),
        shell(circle(8, 14, 2.75)), shell(circle(16, 14, 2.75)), line(seg(10.5, 13, 13.5, 13)),
        spark(12, 6.5, 2.6),
    ]


@icon("digital-product", CAT, "Open box with a download arrow dropping into it; a downloadable product",
      tags=["download", "software", "ebook", "digital goods", "licence", "file"])
def _(S):
    return [
        line(poly([(3, 12), (3, 21), (21, 21), (21, 12)], r=S.r)),
        line(seg(3, 12, 7.5, 12)), line(seg(16.5, 12, 21, 12)),
        line(seg(12, 2.5, 12, 14)), line(poly(head((12, 15.5), 90, 3), r=S.r)),
    ]


@icon("print-on-demand", CAT, "T-shirt under a printer head on a rail with a square design on the chest",
      tags=["custom print", "merch", "custom apparel", "printing", "made to order", "dropshipping"])
def _(S):
    return [
        line(seg(2.5, 4.5, 8, 4.5)), line(seg(16, 4.5, 21.5, 4.5)),
        shell(rect(8, 2, 8, 5, rr(S, 1.5))),
        *shirt(S, 12, 15.8, 0.64, neck=False),
        sq(10.25, 13.5, 3.5, 3.5),
    ]


@icon("wholesale", CAT, "Pyramid of boxes on a pallet with a small hanging price tag at the corner; buying in bulk",
      tags=["bulk", "trade", "pallet", "b2b", "supplier", "cases"])
def _(S):
    return [
        shell(rect(2.5, 12, 7.5, 7, rr(S, 2))), shell(rect(10, 12, 7.5, 7, rr(S, 2))),
        shell(rect(6.25, 4.5, 7.5, 7.5, rr(S, 2))),
        detail(seg(6.25, 12, 6.25, 14.5)), detail(seg(13.75, 12, 13.75, 14.5)),
        line(seg(2.5, 21.5, 17.5, 21.5)),
        shell(poly([(20, 3), (22, 5), (22, 11), (18, 11), (18, 5)], closed=True, r=S.r * 0.4)),
        dot(20, 6.2, 0.7),
    ]


@icon("marketplace", CAT, "Market stall with a scalloped striped awning over a counter; many sellers in one place",
      tags=["market", "stalls", "vendors", "multi-vendor", "sellers", "bazaar"])
def _(S):
    w = 19 / 3
    c = 0 if S.name == "line" else 1.5
    scal = "".join(f"a{fmt(w / 2)} {fmt(w / 2)} 0 0 1 {fmt(-w)} 0" for _ in range(3))
    d = (f"M{fmt(2.5 + c)} 3H{fmt(21.5 - c)}" + (f"A{c} {c} 0 0 1 21.5 {fmt(3 + c)}" if c else "")
         + f"V8.5" + scal + (f"V{fmt(3 + c)}A{c} {c} 0 0 1 {fmt(2.5 + c)} 3" if c else "V3") + "Z")
    return [
        shell(d),
        detail(seg(2.5 + w, 3, 2.5 + w, 8.5)), detail(seg(2.5 + 2 * w, 3, 2.5 + 2 * w, 8.5)),
        shell(rect(4, 15.5, 16, 5.5, rr(S, 4))),
    ]


@icon("delivery-slot", CAT, "Calendar with one grid square holding a small parcel; pick a delivery time",
      tags=["delivery date", "time slot", "schedule delivery", "booking", "calendar", "parcel"])
def _(S):
    return [
        shell(rect(3, 4, 18, 17, rr(S, 3))),
        detail(seg(3, 9, 21, 9)),
        line(seg(8, 2, 8, 5.5)), line(seg(16, 2, 16, 5.5)),
        dot(7, 13, 1), dot(12, 13, 1), dot(7, 17.5, 1), dot(12, 17.5, 1),
        shell(rect(14.5, 12, 5, 6, 0)),
    ]


# ============================================================================ price tags and labels

@icon("sort-by-price", CAT, "Price tag beside a pair of up and down sort arrows; sort products by price",
      tags=["order by price", "price low to high", "price high to low", "filter", "sort", "cost"])
def _(S):
    return [
        *swing(S, 8.5, 3, 11, 18, cut=3),
        detail(seg(6, 15, 11, 15)),
        line(seg(19, 10.5, 19, 4.5)), line(poly(head((19, 3.5), 270, 2.25), r=S.r)),
        line(seg(19, 13.5, 19, 19.5)), line(poly(head((19, 20.5), 90, 2.25), r=S.r)),
    ]


@icon("pre-order", CAT, "Parcel box with a clock beside it; order now for a later release",
      tags=["preorder", "coming soon", "reserve", "upcoming release", "advance order", "waiting"], aliases=["preorder"])
def _(S):
    return [
        shell(rect(2.5, 14, 13, 7.5, rr(S, 2.5))), detail(seg(9, 14, 9, 17)),
        shell(circle(16.5, 7, 4.5)),
        detail(poly([(16.5, 4.8), (16.5, 7), (18.2, 8)], r=0)),
    ]


@icon("sold-out-sign", CAT, "Sign hanging from two strings with a heavy diagonal band across it; out of stock",
      tags=["sold out", "out of stock", "unavailable", "no stock", "hanging sign", "closed sign"])
def _(S):
    return [
        line(poly([(7.5, 8), (12, 3), (16.5, 8)], r=S.r * 0.5)),
        shell(rect(3, 8, 18, 12, rr(S, 3))),
        mark(poly([(6, 10.5), (9.5, 10.5), (18, 17.5), (14.5, 17.5)], closed=True)),
    ]


@icon("new-arrival-tag", CAT, "Hang tag on a looped string with a burst star on its face; a new arrival",
      tags=["new", "just in", "new product", "latest", "fresh stock", "new in"])
def _(S):
    return [
        line(circle(12, 5.2, 2.2)),
        shell(poly(swing_pts(12, 8, 14, 13.5, 3), closed=True, r=S.r)),
        mark(poly(star_pts(12, 15, 3.5, 1.7, 8), closed=True)),
    ]


@icon("bestseller-ribbon", CAT, "Round rosette with two ribbon tails and a rising trend line; a bestseller",
      tags=["best seller", "top seller", "popular", "award", "top rated", "trending"], aliases=["best-seller"])
def _(S):
    return [
        shell(poly([(8.5, 13.5), (6.5, 21.5), (9.5, 19.5), (11.5, 21.5), (12.5, 15)], closed=True, r=S.r * 0.4)),
        shell(poly([(15.5, 13.5), (17.5, 21.5), (14.5, 19.5), (12.5, 21.5), (11.5, 15)], closed=True, r=S.r * 0.4)),
        shell(circle(12, 9.5, 7)),
        detail(poly([(8.7, 11.5), (11, 9), (12.8, 10.8), (15.3, 7.7)], r=S.r * 0.5)),
    ]


@icon("limited-edition", CAT, "Scalloped round seal with a number one above a short line; limited edition",
      tags=["limited", "exclusive", "numbered", "rare", "collector", "special edition"])
def _(S):
    pts = [polar(12, 12, 9.75 if i % 2 == 0 else 8.5, -90 + i * 15) for i in range(24)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.3)),
        detail(poly([(10, 9), (12.2, 7.5), (12.2, 13.5)], r=S.r * 0.4)),
        detail(seg(9.5, 16.5, 14.5, 16.5)),
    ]


@icon("strikethrough-price", CAT, "Hang tag with a crossed-out price and a smaller new price below; was and now pricing",
      tags=["was price", "old price", "reduced", "markdown", "sale price", "crossed out"], aliases=["was-now-price"])
def _(S):
    return [
        *swing(S, 12, 2.5, 16, 19, cut=3),
        detail(seg(8.5, 9.5, 15.5, 9.5)),
        detail(seg(7, 12.5, 17, 6.5)),
        detail(seg(9.5, 17.5, 14.5, 17.5)),
    ]


@icon("price-drop", CAT, "Hang tag with a bold downward arrow at its lower corner; a price reduction",
      tags=["price cut", "reduced", "cheaper", "lower price", "markdown", "decrease"], aliases=["price-cut"])
def _(S):
    return [
        *swing(S, 9, 2.5, 12, 18.5, cut=3),
        mark(poly([(18, 11), (21, 11), (21, 15.5), (22.5, 15.5), (19.5, 20.5), (16.5, 15.5), (18, 15.5)], closed=True)),
    ]


@icon("price-match", CAT, "Two hang tags with an equals sign between them; we match competitor prices",
      tags=["match price", "price promise", "same price", "equal price", "price guarantee", "competitor price"])
def _(S):
    return [
        *swing(S, 5.25, 3.5, 6, 16, cut=2, k=0.5),
        *swing(S, 18.75, 3.5, 6, 16, cut=2, k=0.5),
        line(seg(10, 10.5, 14, 10.5)), line(seg(10, 14.5, 14, 14.5)),
    ]


@icon("unit-price-label", CAT, "Shelf label split in two with a large price on the left and a small per-unit price on the right",
      tags=["shelf label", "price per kilo", "price per unit", "per kg", "shelf edge", "grocery price"])
def _(S):
    return [
        shell(rect(2.5, 6, 19, 12, rr(S, 3))),
        detail(seg(14.5, 6, 14.5, 18)),
        sq(6, 10.5, 5, 3),
        detail(seg(16.5, 10, 19.5, 10)) if False else detail(seg(17, 10.2, 19, 10.2)),
        detail(seg(17, 13.8, 19, 13.8)),
    ]


@icon("price-sticker", CAT, "Round price sticker with price bars and its lower right edge peeling back",
      tags=["label", "sticker", "price label", "peel", "adhesive", "price gun"])
def _(S):
    cx, cy, r = 11.5, 11.5, 8.5
    A = polar(cx, cy, r, -5)
    B = polar(cx, cy, r, 105)
    main = (f"M{fmt(B[0])} {fmt(B[1])}A{r} {r} 0 1 1 {fmt(A[0])} {fmt(A[1])}Z")
    flap = f"M{fmt(A[0])} {fmt(A[1])}A{r} {r} 0 0 0 {fmt(B[0])} {fmt(B[1])}"
    return [shell(main), detail(flap), detail(seg(7, 8.5, 14.5, 8.5)), detail(seg(7, 12.5, 10.5, 12.5))]


@icon("security-spider-wrap", CAT, "Box wrapped with crossing cables that meet at a small square lock",
      tags=["anti-theft", "security wrap", "shoplifting", "protected product", "cable lock", "loss prevention"],
      aliases=["spider-wrap"])
def _(S):
    hexa = [(12, 2.5), (21, 7.5), (21, 16.5), (12, 21.5), (3, 16.5), (3, 7.5)]
    return [
        shell(poly(hexa, closed=True, r=S.r)),
        detail(seg(3, 7.5, 21, 7.5)), detail(seg(12, 2.5, 12, 21.5)),
        sq(9.5, 5, 5, 5, 0 if S.name == "line" else 1.25),
    ]


@icon("full-cart", CAT, "Shopping cart with a box and a bottle piled above the basket rim",
      tags=["cart full", "loaded cart", "shopping", "items in cart", "groceries", "trolley full"])
def _(S):
    return [
        *cart_parts(S, 0, 2),
        shell(rect(8, 2.5, 5, 6, rr(S, 1.5))),
        shell(poly([(16, 2.5), (18, 2.5), (18, 4.5), (19.5, 6), (19.5, 9), (14.5, 9), (14.5, 6), (16, 4.5)],
                   closed=True, r=S.r * 0.4)),
    ]


@icon("one-click-buy", CAT, "Rounded button with a mouse pointer pressing it and a lightning bolt beside the pointer",
      tags=["buy now", "instant purchase", "quick buy", "click to buy", "button", "fast checkout"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 8.5, rr(S, 4))),
        detail(seg(7, 6.75, 13, 6.75)),
        shell(poly([(8, 12.5), (8, 21), (10.5, 18.8), (12.4, 22), (14.2, 21), (12.4, 17.8), (15.5, 17.8)], closed=True, r=S.r * 0.4)),
        bolt(19.5, 17, 0.9),
    ]


@icon("express-checkout", CAT, "Shopping cart with a lightning bolt in the basket and speed lines behind it",
      tags=["fast checkout", "quick checkout", "speedy", "cart", "instant", "buy fast"])
def _(S):
    return [
        *cart_parts(S, 0.5, 0),
        bolt(13.5, 11, 0.6),
        line(seg(1.5, 10, 4, 10)), line(seg(1.5, 14, 4.5, 14)),
    ]


# ============================================================================ checkout and carts

def _dashed_circle(cx, cy, r, n=4, frac=0.5, phase=0.0):
    step = 360 / n
    return [line(arc(cx, cy, r, phase + i * step, phase + i * step + step * frac)) for i in range(n)]


@icon("guest-checkout", CAT, "Dashed outline of a head and shoulders beside a small shopping cart; buy without an account",
      tags=["guest", "no account", "anonymous", "checkout as guest", "visitor", "continue without signing in"])
def _(S):
    parts = _dashed_circle(7.5, 7.5, 3.5, 4, 0.6, -60)
    parts += [line(arc(7.5, 21, 6, 195, 229)), line(arc(7.5, 21, 6, 252, 286)), line(arc(7.5, 21, 6, 309, 343))]
    ck = [(13, 8), (15, 8), (16, 14.5), (21, 14.5), (22, 10.5), (15.4, 10.5)]
    parts += [line(poly(ck[:], r=S.r * 0.5)), dot(17, 18.5, 1.25), dot(21, 18.5, 1.25)]
    return parts


@icon("order-summary", CAT, "Receipt with two item lines and a heavy total line above a torn zigzag edge",
      tags=["receipt", "order total", "basket summary", "invoice", "bill", "checkout"])
def _(S):
    pts = [(5, 2.5), (19, 2.5), (19, 21.5), (16.33, 19.5), (13.67, 21.5), (11, 19.5), (8.33, 21.5), (5, 19.5)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.4)),
        detail(seg(8.5, 6.5, 15.5, 6.5)), detail(seg(8.5, 10.5, 13, 10.5)),
        sq(8.5, 14, 7, 2.5),
    ]


@icon("buy-button", CAT, "Wide pill button with a small shopping bag on the left and a text bar on the right",
      tags=["add to cart", "purchase button", "call to action", "cta", "buy now", "button"])
def _(S):
    return [
        shell(rect(2, 4.5, 20, 15, rr(S, 7.5) if S.name == "rounded" else 3)),
        mark(poly([(4.5, 10.5), (11.5, 10.5), (12.5, 17), (3.5, 17)], closed=True)),
        detail("M5.75 10.5V9.75A2.25 2.25 0 0 1 10.25 9.75V10.5"),
        detail(seg(14.5, 12, 19, 12)),
    ]


@icon("car-shaped-shopping-cart", CAT, "Shopping cart basket above a toy car body with a headlight and two wheels",
      tags=["kids cart", "toy car cart", "car cart", "children's trolley", "family shopping", "ride on cart"])
def _(S):
    return [
        line(poly([(2, 3), (5, 3)], r=0)),
        shell(poly([(5, 3), (21, 3), (19.5, 9.5), (6.5, 9.5)], closed=True, r=S.r)),
        shell(poly([(2, 19), (2, 16), (5, 13), (19, 13), (22, 16), (22, 19)], closed=True, r=S.r)),
        shell(circle(7, 19.5, 1.75)), shell(circle(17, 19.5, 1.75)),
        dot(4.6, 16.2, 0.9),
    ]


@icon("flatbed-cart", CAT, "Low flat platform cart on casters with an upright handle frame at one end and long boards on top",
      tags=["platform cart", "lumber cart", "warehouse cart", "hardware store", "trolley", "boards"])
def _(S):
    return [
        line(poly([(4, 3), (4, 16)], r=0)), line(seg(4, 3, 7.5, 3)),
        shell(rect(4, 15.5, 18, 2.5, 0)),
        shell(rect(8, 10.5, 14, 3.5, 0)), shell(rect(8, 5.5, 14, 3.5, 0)),
        dot(7, 21, 1.5), dot(19, 21, 1.5),
    ]


def _cart_line(S, k, dx, dy):
    basket = [(2, 3.5), (5, 3.5), (7.5, 15), (19, 15), (21, 7), (5.9, 7)]
    return line(poly([(2 + (x - 2) * k + dx, 3.5 + (y - 3.5) * k + dy) for x, y in basket], r=S.r * 0.6))


@icon("stacked-shopping-carts", CAT, "Three shopping carts nested into each other in a row, seen from the side",
      tags=["nested carts", "cart return", "trolley bay", "cart corral", "carts", "trolleys"])
def _(S):
    k = 0.64
    return [
        _cart_line(S, k, 6.6, 1.0), _cart_line(S, k, 3.3, 3.7), _cart_line(S, k, 0, 6.4),
        dot(6.5, 20.3, 1.25), dot(12.2, 20.3, 1.25),
    ]


@icon("cart-token", CAT, "Round token with a hole at the top attached to a key ring; a deposit token for trolleys",
      tags=["trolley coin", "cart coin", "deposit coin", "key ring", "token", "trolley token"], aliases=["trolley-token"])
def _(S):
    return [
        line(arc(7, 7, 4.25, 80, 370)),
        shell(circle(14.5, 14.5, 6.75)),
        dot(10.6, 10.6, 1.1),
        detail(seg(13, 17, 17.5, 17)),
    ]


@icon("checkout-divider-bar", CAT, "Upright divider bar on a conveyor belt between two small items",
      tags=["conveyor divider", "separator bar", "next customer", "checkout belt", "grocery divider", "lane"],
      aliases=["customer-divider"])
def _(S):
    return [
        shell(rect(2, 18, 20, 3.5, 0 if S.name == "line" else 1.75)),
        shell(rect(2.5, 12, 4.5, 6, 0 if S.name == "line" else 2)),
        shell(poly([(10, 18), (10, 9.5), (12, 6.5), (14, 9.5), (14, 18)], closed=True, r=S.r)),
        shell(rect(17, 12, 4.5, 6, 0 if S.name == "line" else 2)),
    ]


@icon("bagging-area", CAT, "Shopping bag standing on a flat platform with a small arrow pointing down at it",
      tags=["bag scale", "bagging", "place item", "self checkout", "weigh bag", "bagging station"])
def _(S):
    return [
        shell(poly([(3, 9.5), (13, 9.5), (14, 18), (2, 18)], closed=True, r=S.r * 0.6)),
        line("M5.5 9.5V8.5A2.5 2.5 0 0 1 10.5 8.5V9.5"),
        shell(rect(2, 18, 20, 3.5, rr(S, 1.75))),
        line(seg(18, 3.5, 18, 10)), line(poly(head((18, 12.5), 90, 2.5), r=S.r)),
    ]


def _three():
    """Digit 3 built from two stacked arcs, centred on x=12 and spanning y 6 to 14.5."""
    return [detail(arc(12, 8.25, 2.25, -150, 90)), detail(arc(12, 12.75, 2.25, -90, 150))]


@icon("express-lane-sign", CAT, "Sign on a pole above a counter showing the number ten; an express checkout lane",
      tags=["express checkout", "ten items or fewer", "quick lane", "fast lane", "checkout lane", "10 items"],
      aliases=["ten-items-sign"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 11, rr(S, 3))),
        detail(seg(8, 6, 8, 10)),
        detail(rect(11.5, 6, 5.5, 4, 0)) if S.name == "line" else detail(rect(11.5, 6, 5.5, 4, 1.5)),
        line(seg(12, 13.5, 12, 18)),
        shell(rect(3, 18, 18, 3.5, rr(S, 1.75))),
    ]


@icon("checkout-lane-number", CAT, "Slim pole topped with a lit box showing the number three and light rays around it",
      tags=["lane number", "register number", "checkout number", "till light", "open lane", "number 3"])
def _(S):
    return [
        shell(rect(6.5, 6, 11, 10, rr(S, 3))),
        detail(arc(12, 9.4, 1.6, -150, 90)), detail(arc(12, 12.6, 1.6, -90, 150)),
        line(seg(12, 16, 12, 21.5)),
        line(seg(12, 1.5, 12, 3)), line(seg(3.5, 6, 5, 7)), line(seg(20.5, 6, 19, 7)),
    ]


@icon("pole-display", CAT, "Small two line customer display on top of a thin pole with a round base",
      tags=["customer display", "price display", "vfd", "register screen", "pos", "line display"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 10, rr(S, 2.5))),
        detail(seg(6.5, 6, 17.5, 6)), detail(seg(6.5, 9.2, 13, 9.2)),
        line(seg(12, 12.5, 12, 19)),
        shell(rect(6, 18.5, 12, 3, rr(S, 1.5))),
    ]


@icon("change-tray", CAT, "Shallow tray holding a coin and a banknote; change returned to the customer",
      tags=["cash tray", "coin dish", "tip tray", "change dish", "counter", "money tray"])
def _(S):
    return [
        shell(circle(7.5, 8.5, 3.25)),
        shell(rect(13, 4.5, 8.5, 6.5, rr(S, 1.5))), dot(17.25, 7.75, 1),
        shell(poly([(3, 13), (21, 13), (18.5, 20.5), (5.5, 20.5)], closed=True, r=S.r)),
    ]


@icon("tipping-screen", CAT, "Tablet screen with a percent sign and three option buttons below it; add a tip",
      tags=["gratuity", "tip prompt", "add tip", "tip percentage", "customer screen", "payment terminal"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        *pct(12, 8.5, 2.2, 1.0),
        sq(5, 14.5, 3.5, 4.5), sq(10.25, 14.5, 3.5, 4.5), sq(15.5, 14.5, 3.5, 4.5),
    ]


@icon("tablet-pos-stand", CAT, "Tablet on a swivel stand with a small square card reader beside it",
      tags=["tablet register", "ipad pos", "countertop pos", "card reader", "point of sale", "kiosk stand"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 13, 13, rr(S, 2.5))),
        line(seg(9, 15.5, 9, 19)),
        shell(rect(4.5, 19, 9, 2.5, rr(S, 1.25))),
        shell(rect(17.5, 7, 4.5, 8, rr(S, 1.5))), dot(19.75, 9.5, 0.8),
    ]


# ============================================================================ more helpers

def dashes(pts, on=2.5, off=2.0, closed=True, start=0.0):
    """Dashed outline of a polygon as separate open strokes."""
    pts = list(pts) + ([pts[0]] if closed else [])
    out = []
    carry = start
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        t = carry
        while t < L:
            a = t
            b = min(t + on, L)
            if b - a > 0.6:
                out.append(line(seg(x1 + ux * a, y1 + uy * a, x1 + ux * b, y1 + uy * b)))
            t += on + off
        carry = t - L
    return out


def cloud(cx, cy, k=1.0) -> str:
    """Small cloud outline centred near (cx, cy)."""
    pts = f"M{fmt(cx - 3.5 * k)} {fmt(cy + 3 * k)}h{fmt(6.5 * k)}a{fmt(2.2 * k)} {fmt(2.2 * k)} 0 0 0 {fmt(.2 * k)} {fmt(-4.4 * k)}a{fmt(3.3 * k)} {fmt(3.3 * k)} 0 0 0 {fmt(-6.3 * k)} {fmt(-.5 * k)}a{fmt(2.45 * k)} {fmt(2.45 * k)} 0 0 0 {fmt(-.4 * k)} {fmt(4.9 * k)}z"
    return pts


def arrow_h(x1, y1, x2, y2, S, size=2.25):
    """Straight arrow from (x1,y1) to (x2,y2) with an open head."""
    deg = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return [line(seg(x1, y1, x2, y2)), line(poly(head((x2, y2), deg, size), r=S.r))]


def bank(S, cx, top, w, h):
    return building(S, cx, top, w, h)


# ============================================================================ point of sale and payments

@icon("pos-workstation", CAT, "Monitor above a cash drawer with a small receipt printer beside it; a checkout workstation",
      tags=["checkout counter", "till", "cash register", "pos terminal", "point of sale", "register station"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 13, 9, rr(S, 2.5))),
        line(seg(9, 11.5, 9, 14)),
        shell(rect(2.5, 14, 13, 7, rr(S, 2))),
        detail(seg(6.5, 17.5, 11.5, 17.5)),
        shell(rect(17.5, 11, 4.5, 10, rr(S, 1.5))),
        detail(seg(17.5, 14.5, 22, 14.5)),
        line(seg(19.75, 11, 19.75, 6.5)),
    ]


@icon("wrist-payment", CAT, "Smartwatch on a strap with contactless wave arcs coming out of its face",
      tags=["watch pay", "tap to pay", "contactless", "smartwatch payment", "wearable payment", "nfc"])
def _(S):
    return [
        line(seg(5, 7.5, 5, 2.5)), line(seg(9, 7.5, 9, 2.5)),
        line(seg(5, 16.5, 5, 21.5)), line(seg(9, 16.5, 9, 21.5)),
        shell(rect(2.5, 7.5, 9, 9, rr(S, 3))),
        dot(7, 12, 1.1),
        line(arc(12.5, 12, 4.5, -45, 45)),
        line(arc(12.5, 12, 8.5, -45, 45)),
    ]


@icon("virtual-card", CAT, "Payment card drawn with a dashed outline and a small cloud inside; a digital-only card",
      tags=["digital card", "online card", "card number", "disposable card", "one time card", "cloud payment"])
def _(S):
    pts = [(2.5, 5), (21.5, 5), (21.5, 19), (2.5, 19)]
    return dashes(pts, 3.2, 2.4, True, 0.5) + [line(cloud(12, 12, 1.0))]


@icon("layaway", CAT, "Parcel box on a shelf next to a calendar page; pay over time and collect later",
      tags=["lay-by", "lay away", "reserve item", "pay in installments", "hold item", "instalment plan"])
def _(S):
    return [
        shell(rect(12.5, 2.5, 9, 8, rr(S, 2))),
        detail(seg(12.5, 5.5, 21.5, 5.5)),
        dot(17, 8.2, 0.9),
        shell(rect(2.5, 12.5, 11, 9, rr(S, 2))), detail(seg(8, 12.5, 8, 16)),
    ]


@icon("split-tender", CAT, "Half a payment card beside half a banknote with a dashed line between them; pay with two methods",
      tags=["split payment", "mixed payment", "card and cash", "two payment methods", "part cash part card", "tender"])
def _(S):
    return [
        shell(rect(2.5, 6, 7, 12, rr(S, 2.5))), detail(seg(2.5, 10.5, 9.5, 10.5)),
        *dashes([(12, 3.5), (12, 20.5)], 2.6, 1.8, False, 0.0),
        shell(rect(14.5, 6, 7, 12, rr(S, 2.5))), dot(18, 12, 1.6),
    ]


@icon("card-charge-slip", CAT, "Narrow paper slip with a card number line, a heavy amount bar and a signature squiggle",
      tags=["credit card slip", "sales slip", "charge receipt", "merchant copy", "signature slip", "card receipt"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, rr(S, 2))),
        detail(seg(8, 6.5, 16, 6.5)),
        sq(8, 9.5, 8, 2.5),
        detail("M8 17c1.2-3 2.2-3 2.8-1s1.6 1.6 2.3-.4S14.8 14.5 16 17"),
    ]


@icon("mobile-wallet", CAT, "Smartphone with a wallet shape and a card peeking out of it on the screen",
      tags=["digital wallet", "phone wallet", "pay with phone", "e-wallet", "wallet app", "mobile pay"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, rr(S, 3))),
        detail(seg(9, 6.5, 15, 6.5)),
        detail("M8 11V10.5A1.5 1.5 0 0 1 9.5 9h5a1.5 1.5 0 0 1 1.5 1.5V11"),
        detail(rect(7, 12.5, 10, 6, rr(S, 1.5))),
    ]


@icon("payment-gateway", CAT, "Payment card, an arch shaped gate and a bank building in a row with an arrow below",
      tags=["payment processor", "online payments", "card processing", "checkout payments", "psp", "merchant account"])
def _(S):
    return [
        shell(rect(1.5, 9, 7, 6, rr(S, 1.5))),
        line("M13 21V10a4.75 4.75 0 0 1 9.5 0v11"),
        *arrow_h(9.5, 15.5, 19, 15.5, S, 2.25),
    ]


@icon("chargeback", CAT, "Payment card with a curved arrow looping over it from the right edge back to the left edge",
      tags=["card dispute", "reversal", "payment dispute", "reverse charge", "disputed transaction", "refund to card"])
def _(S):
    return [
        shell(rect(3, 11.5, 18, 10, rr(S, 3))),
        detail(seg(3, 15.5, 21, 15.5)),
        line("M19.5 8.5A7.5 5.5 0 0 0 4.5 8.5"),
        line(poly(head((4.5, 9), 90, 2.25), r=S.r)),
    ]


@icon("payment-methods", CAT, "Payment card, banknote and smartphone shown together; accepted ways to pay",
      tags=["accepted payments", "ways to pay", "pay options", "cash card mobile", "payment types", "checkout options"])
def _(S):
    return [
        shell(rect(2.5, 3, 13, 8, rr(S, 2.5))), detail(seg(2.5, 6.5, 15.5, 6.5)),
        shell(rect(2.5, 13, 13, 8, rr(S, 2.5))), dot(9, 17, 1.6),
        shell(rect(17.5, 3, 4.5, 18, rr(S, 2))), dot(19.75, 18, 0.7),
    ]


@icon("partial-refund", CAT, "Coin with its right half solid and a return arrow wrapping around the empty left half",
      tags=["part refund", "refund some", "money back", "reimburse", "return part of payment", "credit back"])
def _(S):
    p240 = polar(13, 12, 9, 240)
    p120 = polar(13, 12, 9, 120)
    return [
        shell(circle(13, 12, 5.5)),
        mark("M13 6.5A5.5 5.5 0 0 1 13 17.5Z"),
        line(f"M{fmt(p240[0])} {fmt(p240[1])}A9 9 0 0 0 {fmt(p120[0])} {fmt(p120[1])}"),
        line(poly(head(p120, 30, 2.25), r=S.r)),
    ]


@icon("merchant-payout", CAT, "Shop with an awning on the left, an arrow, and a bank building on the right; money paid to a seller",
      tags=["seller payout", "transfer to bank", "settlement", "withdraw earnings", "vendor payment", "disbursement"])
def _(S):
    return [
        shell(rect(1.5, 4, 7.5, 4.5, rr(S, 1))),
        shell(rect(2.5, 8.5, 5.5, 11.5, 0)),
        *arrow_h(10, 14, 13.5, 14, S, 2),
        shell(poly([(14.5, 10), (18, 5), (21.5, 10)], closed=True, r=S.r * 0.4)),
        shell(rect(15.5, 10, 5, 10, 0)),
        detail(seg(18, 10, 18, 20)),
    ]


@icon("sales-commission", CAT, "Open hand palm up under a coin marked with a percent sign; earnings paid per sale",
      tags=["commission", "sales bonus", "referral fee", "affiliate payout", "percentage fee", "earn per sale"])
def _(S):
    return [
        shell(circle(12, 7, 5)),
        dot(10.3, 5.3, 0.9), dot(13.7, 8.7, 0.9), detail(seg(13.6, 5, 10.4, 9)),
        shell(rect(2, 14.5, 4, 7, rr(S, 1))),
        line("M6 16.5l3.5-1.5H15a1.75 1.75 0 0 1 0 3.5H11.5"),
        line("M6 20h8l6-3.5a1.5 1.5 0 0 0-1.8-2.4L15 16.5"),
    ]


@icon("round-up-donation", CAT, "Coin and an upward arrow above a donation box with a heart on its front; round up your total to give",
      tags=["donate at checkout", "charity", "round up", "add a donation", "give change", "fundraising"])
def _(S):
    return [
        shell(circle(8.5, 6, 3.5)),
        *arrow_h(18, 9, 18, 3, S, 2.25),
        shell(rect(3, 12.5, 18, 9, rr(S, 2.5))),
        mark("M12 20L8.4 16.6A2.1 2.1 0 0 1 12 14.8 2.1 2.1 0 0 1 15.6 16.6Z"),
    ]


@icon("multi-currency-pricing", CAT, "Price tag beside two coins stacked one above the other, each with a different currency mark",
      tags=["currencies", "foreign currency", "local prices", "currency switch", "international pricing", "exchange"])
def _(S):
    return [
        *swing(S, 7, 2.5, 9, 18, cut=2.5),
        detail(seg(4.5, 14.5, 9.5, 14.5)),
        shell(circle(17.5, 6.5, 3.75)), detail(seg(16, 5.5, 19, 5.5)), detail(seg(16, 7.8, 19, 7.8)),
        shell(circle(17.5, 17, 3.75)), dot(17.5, 17, 0.9),
    ]


@icon("bill-acceptor", CAT, "Front panel with a wide slot, a banknote half inserted and a small status light",
      tags=["banknote reader", "note validator", "cash slot", "kiosk cash input", "vending cash", "self service payment"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 19, rr(S, 3))),
        sq(6.5, 7, 11, 2.5, 0),
        line(poly([(8.5, 9.5), (8.5, 17.5), (15.5, 17.5), (15.5, 9.5)], r=S.r * 0.5)),
        dot(12, 13.5, 1.25),
        dot(18.5, 5, 0.8),
    ]


@icon("cash-only-sign", CAT, "Hanging sign with a large banknote on its face; cash payments only",
      tags=["no cards", "cash payments only", "we do not accept cards", "cash sign", "no credit cards", "cash accepted"])
def _(S):
    return [
        line(poly([(7.5, 5), (12, 2), (16.5, 5)], r=S.r * 0.5)),
        shell(rect(2.5, 5, 19, 16.5, rr(S, 3))),
        detail(rect(5.5, 8.5, 13, 8, rr(S, 1))),
        dot(12, 12.5, 1.5),
    ]


@icon("loyalty-punch-card", CAT, "Card with two rows of four marks, the first six punched out; a stamp card toward a reward",
      tags=["stamp card", "punch card", "buy ten get one free", "rewards card", "coffee card", "frequent buyer"])
def _(S):
    ps = [(6.75 + 3.5 * i, 9) for i in range(4)] + [(6.75 + 3.5 * i, 15) for i in range(4)]
    parts = [shell(rect(2.5, 4, 19, 16, rr(S, 3)))]
    for i, (x, y) in enumerate(ps):
        parts.append(dot(x, y, 1.15 if i < 6 else 0.6))
    return parts


@icon("loyalty-tiers", CAT, "Three solid bars growing wider from top to bottom with a small crown above the top bar",
      tags=["membership levels", "vip tiers", "bronze silver gold", "status levels", "rewards levels", "customer ranks"])
def _(S):
    return [
        shell(poly([(7.5, 9), (7, 3.5), (9.8, 5.8), (12, 2.5), (14.2, 5.8), (17, 3.5), (16.5, 9)], closed=True, r=S.r * 0.3)),
        line(seg(9, 13, 15, 13)),
        line(seg(6, 17, 18, 17)),
        line(seg(3, 21, 21, 21)),
    ]


@icon("redeem-points", CAT, "Coin with a star, a curved arrow, and a wrapped gift box; spend points on a reward",
      tags=["points to reward", "spend points", "claim reward", "cash in points", "rewards store", "loyalty redemption"])
def _(S):
    return [
        shell(circle(6.5, 6.5, 4)),
        mark(poly(star_pts(6.5, 6.5, 2.3, 1.0, 5), closed=True)),
        line("M12 4.5Q17 4 17 8.5"),
        line(poly(head((17, 9.8), 90, 2), r=S.r)),
        shell(rect(10.5, 12, 12, 3, 0)),
        shell(rect(11.5, 15, 10, 6.5, 0)),
        detail(seg(16.5, 12, 16.5, 21.5)),
    ]


@icon("loyalty-key-tag", CAT, "Small rounded tag with a barcode and a hole at one end, threaded on a key ring",
      tags=["keyring card", "fob card", "membership tag", "barcode tag", "mini loyalty card", "shopper key fob"])
def _(S):
    return [
        line(circle(8, 8, 4.5)),
        shell(rect(7, 11.5, 15, 10, rr(S, 3))),
        dot(10.5, 16.5, 1.1),
        detail(seg(14, 14.5, 14, 18.5)), detail(seg(16.5, 14.5, 16.5, 18.5)), detail(seg(19, 14.5, 19, 18.5)),
    ]


@icon("double-points", CAT, "Coin with a star beside a bold multiplication sign and the number two; earn twice the points",
      tags=["2x points", "bonus points", "points multiplier", "double rewards", "extra points", "points promotion"])
def _(S):
    return [
        shell(circle(6.5, 12, 4.5)),
        mark(poly(star_pts(6.5, 12, 2.4, 1.1, 5), closed=True)),
        line(seg(12.5, 10.5, 15.5, 13.5)), line(seg(15.5, 10.5, 12.5, 13.5)),
        line("M17.5 9.5a2.25 2.25 0 0 1 4.5 0c0 2.2-2.5 3.2-4.5 6.5H22.25"),
    ]


@icon("gift-with-purchase", CAT, "Shopping bag with a small wrapped gift box and a bow sitting on top of it",
      tags=["free gift", "bonus gift", "gwp", "freebie", "gift offer", "complimentary gift"])
def _(S):
    return [
        *bag(S, 2.5, 9.5, 11, 12),
        shell(rect(15, 6.5, 7, 6, 0)),
        line("M18.5 6.5C17.5 4 16 4.5 16.8 5.7M18.5 6.5C19.5 4 21 4.5 20.2 5.7"),
        dot(18.5, 9.5, 0.8),
    ]


@icon("free-sample-tray", CAT, "Serving tray holding three tiny paper cups with toothpicks standing in them",
      tags=["tasting", "samples", "taster", "sample table", "food sampling", "free taste"])
def _(S):
    parts = [shell(poly([(2, 16.5), (22, 16.5), (19, 21), (5, 21)], closed=True, r=S.r))]
    for c in (5.5, 12, 18.5):
        parts.append(solid(poly([(c - 2.5, 10.5), (c + 2.5, 10.5), (c + 1.8, 15), (c - 1.8, 15)], closed=True)))
        parts.append(line(seg(c, 10.5, c + 1.3, 4.5)))
    return parts


@icon("perfume-tester-strip", CAT, "Thin paper strip with scent waves rising above it beside a small spray bottle",
      tags=["fragrance sample", "scent strip", "blotter", "smell test", "cologne tester", "perfume sample card"])
def _(S):
    return [
        line("M4.5 6.5C5.7 5 3.3 3.8 4.5 2"), line("M7.5 6.5C8.7 5 6.3 3.8 7.5 2"),
        shell(poly([(3, 21.5), (3, 12), (6, 8.5), (9, 12), (9, 21.5)], closed=True, r=S.r * 0.4)),
        shell(rect(12.5, 12.5, 9.5, 9, rr(S, 2.5))),
        shell(rect(15, 9.5, 4.5, 3, 0)),
        line(poly([(17.25, 9.5), (17.25, 6.5), (20, 6.5)], r=0)),
    ]


@icon("flash-sale", CAT, "Hang tag with a large lightning bolt across its face; a limited time sale",
      tags=["lightning deal", "limited time offer", "quick sale", "sale event", "hurry", "time limited discount"])
def _(S):
    return [
        *swing(S, 12, 2.5, 15, 19, cut=3.5),
        bolt(12, 14.5, 1.15),
    ]


@icon("promo-starburst", CAT, "Jagged starburst sticker shape with a percent sign in the middle; a promotion badge",
      tags=["sale badge", "discount burst", "percent off", "promo sticker", "special offer", "deal badge"])
def _(S):
    pts = [polar(12, 12, 10 if i % 2 == 0 else 7.2, -90 + i * 15) for i in range(24)]
    return [shell(poly(pts, closed=True, r=S.r * 0.3), stroke_miterlimit="3")] + pct(12, 12, 2.6, 1.2)


@icon("bulk-discount", CAT, "Three boxes stacked in a column with a percent tag beside them; a discount for buying in quantity",
      tags=["quantity discount", "buy more save more", "volume pricing", "multi buy", "case price", "bulk pricing"])
def _(S):
    return [
        shell(rect(2.5, 3, 11.5, 6, rr(S, 1.5))),
        shell(rect(2.5, 9, 11.5, 6, rr(S, 1.5))),
        shell(rect(2.5, 15, 11.5, 6, rr(S, 1.5))),
        line(seg(14, 6, 16.5, 6)),
        shell(poly(swing_pts(18.5, 8, 7, 13, 2.5), closed=True, r=S.r * 0.7)),
        *pct(18.5, 14.5, 1.5, 0.75),
    ]


@icon("mail-in-rebate", CAT, "Envelope below a coin with a curved return arrow; money sent back after you mail a form",
      tags=["rebate", "cash back by mail", "mail rebate", "send form for refund", "post in rebate", "reimbursement"])
def _(S):
    return [
        shell(circle(7.5, 5.5, 3.3)),
        line("M12.5 4Q18 3 18 8"),
        line(poly(head((18, 9.2), 90, 2), r=S.r)),
        shell(rect(2.5, 11.5, 19, 10, rr(S, 2.5))),
        detail(poly([(3, 12.5), (12, 18), (21, 12.5)], r=0)),
    ]


@icon("daily-deal", CAT, "Calendar page with a small price tag hanging inside it below the binder rings; a deal of the day",
      tags=["deal of the day", "today only", "offer of the day", "one day offer", "daily offer", "today's special"])
def _(S):
    return [
        line(seg(7.5, 2.5, 7.5, 6.5)), line(seg(16.5, 2.5, 16.5, 6.5)),
        shell(rect(3, 4.5, 18, 17, rr(S, 3))),
        detail(seg(3, 9, 21, 9)),
        shell(poly(swing_pts(12, 11.5, 8, 7, 2), closed=True, r=S.r * 0.4)),
    ]


@icon("giveaway", CAT, "Gift box with its lid lifted and confetti and sparks bursting out of the top",
      tags=["free gift", "prize", "contest", "surprise", "freebie", "gift draw"])
def _(S):
    return [
        line(seg(8, 8, 5.5, 4.5)), line(seg(12, 7, 12, 2.5)), line(seg(16, 8, 18.5, 4.5)),
        dot(3.5, 8, 1), dot(20.5, 8, 1),
        shell(rect(3, 10.5, 18, 3.5, rr(S, 1.5))),
        shell(rect(4.5, 14, 15, 7.5, rr(S, 2))),
        detail(seg(12, 14, 12, 21.5)),
    ]


@icon("coupon-booklet", CAT, "Small booklet with a perforated dashed edge and a coupon strip tearing off beside it",
      tags=["coupon book", "voucher book", "tear off coupons", "savings book", "perforated", "vouchers"])
def _(S):
    return [
        shell(rect(2.5, 3, 11, 18, rr(S, 2))),
        detail(seg(5.5, 8, 10.5, 8)), detail(seg(5.5, 12, 10.5, 12)),
        *dashes([(16.5, 5.5), (16.5, 18.5)], 2.6, 1.8, False, 0.0),
        line(poly([(16.5, 5.5), (21.5, 5.5), (21.5, 18.5), (16.5, 18.5)], r=S.r * 0.5)),
    ]


@icon("price-freeze", CAT, "Hang tag with a snowflake on its face; the price is held and will not rise",
      tags=["price lock", "price hold", "fixed price", "frozen price", "price guarantee", "no price increase"])
def _(S):
    cx, cy, r = 12, 14.25, 4.4
    arms = [detail(seg(*polar(cx, cy, r, a), *polar(cx, cy, r, a + 180))) for a in (0, 60, 120)]
    return [*swing(S, 12, 2.5, 16, 19, cut=3.5)] + arms


@icon("satisfaction-guarantee", CAT, "Scalloped round seal with a smiling face in the centre; satisfaction guaranteed",
      tags=["money back guarantee", "happy customer", "quality seal", "customer satisfaction", "approved", "guarantee badge"])
def _(S):
    pts = [polar(12, 12, 9.75 if i % 2 == 0 else 8.5, -90 + i * 15) for i in range(24)]
    return [
        shell(poly(pts, closed=True, r=S.r * 0.3)),
        dot(9.5, 10, 1.1), dot(14.5, 10, 1.1),
        detail(arc(12, 11.5, 4, 35, 145)),
    ]


@icon("buyer-protection", CAT, "Shield outline with a small shopping bag drawn inside it; purchases are covered",
      tags=["purchase protection", "secure shopping", "safe checkout", "order guarantee", "shopper safety", "money back cover"])
def _(S):
    shield = [(12, 2.5), (20, 5.5), (20, 12), (16.5, 18), (12, 21.5), (7.5, 18), (4, 12), (4, 5.5)]
    return [
        shell(poly(shield, closed=True, r=S.r * 1.5)),
        detail(poly([(8.5, 10), (15.5, 10), (16.5, 16.5), (7.5, 16.5)], closed=True, r=0)),
        detail("M9.5 10V9a2.5 2.5 0 0 1 5 0v1"),
    ]


@icon("trial-size", CAT, "Small travel sized bottle standing beside a full sized bottle of the same shape",
      tags=["travel size", "mini bottle", "sample size", "miniature", "small bottle", "try before you buy"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 5, 3.5, 0)),
        shell(rect(6.5, 6, 3, 3, 0)),
        shell(rect(2.5, 9.5, 11, 12, rr(S, 3))),
        shell(rect(17, 12.5, 3, 3, 0)),
        shell(rect(15.5, 15.5, 6, 6, rr(S, 2))),
    ]


@icon("value-pack", CAT, "Large box beside a smaller box with a solid burst star at the top corner; a bundle deal",
      tags=["multipack", "bundle", "family pack", "economy pack", "bonus pack", "combo deal"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 10, 16, rr(S, 2))), detail(seg(7.5, 5.5, 7.5, 9.5)),
        shell(rect(14, 13, 7.5, 8.5, rr(S, 2))),
        solid(poly(star_pts(17.5, 6.5, 4.4, 2.6, 8), closed=True)),
    ]


@icon("featured-product", CAT, "Product box on a low stand with three spotlight rays shining down on it",
      tags=["spotlight", "highlight", "promoted product", "hero product", "staff pick", "showcase"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 7)), line(seg(6.5, 3, 4.5, 7.5)), line(seg(17.5, 3, 19.5, 7.5)),
        shell(rect(7, 10.5, 10, 7, rr(S, 2))), detail(seg(12, 10.5, 12, 13.5)),
        shell(rect(3.5, 18, 17, 3.5, rr(S, 1.5))),
    ]


@icon("mobile-coupon", CAT, "Smartphone with a ticket shaped coupon with notched sides on its screen",
      tags=["digital coupon", "phone voucher", "e-coupon", "app offer", "redeem on phone", "wallet coupon"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, rr(S, 3))),
        detail(poly([(6.5, 9), (8, 7.5), (16, 7.5), (17.5, 9), (17.5, 14), (16, 15.5), (8, 15.5), (6.5, 14)], closed=True, r=0)),
        dot(10.2, 10.2, 0.8), dot(13.8, 12.8, 0.8), detail(seg(13.2, 9.8, 10.8, 13.2)),
        dot(12, 18.4, 0.6),
    ]


@icon("endcap-display", CAT, "Short shelf unit with a wide header sign on top and boxes sitting on two shelves",
      tags=["end of aisle", "promo display", "store shelf", "retail display", "merchandising", "gondola end"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 4, rr(S, 1))),
        line(seg(4.5, 6.5, 4.5, 21.5)), line(seg(19.5, 6.5, 19.5, 21.5)),
        line(seg(4.5, 14, 19.5, 14)), line(seg(4.5, 21.5, 19.5, 21.5)),
        solid(rect(7.5, 8.5, 4, 4)), solid(rect(13.5, 9.5, 3.5, 3)),
        solid(rect(7.5, 16, 5, 4)), solid(rect(14.5, 17, 3, 3)),
    ]
