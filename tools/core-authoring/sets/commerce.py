"""TypeIcon Core: shopping & commerce.

Generic retail objects only: no payment network, bank or shop logo. Commerce takes the full
variant badge set in the bottom-right (box 13–23), so identifying details sit top/left where the
object allows. Weight and size follow the v0.1 `cart` and `tag` icons in icons.py.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import SCALE, fmt, path_to_d, polar

CAT = "commerce"


# ============================================================================ helpers

def rr(S, cap=None):
    """Container corner radius for the style, optionally capped for small shapes."""
    return S.R if cap is None else min(S.R, cap)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def pct(cx, cy, k=3.0, r=1.25):
    """Percent sign: two dots and a slash, sized so the dots clear the slash by 2 px."""
    a = k + 0.75
    return [dot(cx - k, cy - k, r), dot(cx + k, cy + k, r), detail(seg(cx + a, cy - a, cx - a, cy + a))]


def arc_outside(cx, cy, r, ox, oy, rmin, step=0.5):
    """Longest arc of circle (cx, cy, r) whose points lie at least rmin from (ox, oy)."""
    n = int(360 / step)
    ok = [math.dist(polar(cx, cy, r, i * step), (ox, oy)) >= rmin for i in range(n)]
    best, start = (0, 0), None
    for i in range(2 * n):
        if ok[i % n]:
            start = i if start is None else start
            if i - start > best[1] - best[0]:
                best = (start, i)
        else:
            start = None
    return arc(cx, cy, r, best[0] * step, best[1] * step)


def arc_avoid(cx, cy, r, keep_out, step=0.5):
    """Longest arc of circle (cx, cy, r) whose points lie outside a pathops region (grid units)."""
    n = int(360 / step)
    ok = [not keep_out.contains(tuple(v * SCALE for v in polar(cx, cy, r, i * step))) for i in range(n)]
    best, start = (0, 0), None
    for i in range(2 * n):
        if ok[i % n]:
            start = i if start is None else start
            if i - start > best[1] - best[0]:
                best = (start, i)
        else:
            start = None
    return arc(cx, cy, r, best[0] * step, best[1] * step)


def head(tip, deg, size=2.5):
    """Open arrowhead at tip; deg is the direction the arrow points (0 = right, 90 = down)."""
    a = polar(tip[0], tip[1], size * math.sqrt(2), deg + 180 - 45)
    b = polar(tip[0], tip[1], size * math.sqrt(2), deg + 180 + 45)
    return [a, tip, b]


def union_d(*ds):
    """Outline of the union of closed shapes (grid-unit d-strings)."""
    return path_to_d(U(*(P(d) for d in ds)))


def notched(x0, y0, x1, y1, nr, cr):
    """Rectangle with semicircular notches in the middle of both short sides (ticket/coupon)."""
    my = (y0 + y1) / 2
    a = f"A{fmt(cr)} {fmt(cr)} 0 0 1 "
    n = f"A{fmt(nr)} {fmt(nr)} 0 0 0 "
    if cr <= 0:
        return (f"M{fmt(x0)} {fmt(y0)}H{fmt(x1)}V{fmt(my - nr)}{n}{fmt(x1)} {fmt(my + nr)}V{fmt(y1)}"
                f"H{fmt(x0)}V{fmt(my + nr)}{n}{fmt(x0)} {fmt(my - nr)}Z")
    return (f"M{fmt(x0 + cr)} {fmt(y0)}H{fmt(x1 - cr)}{a}{fmt(x1)} {fmt(y0 + cr)}V{fmt(my - nr)}{n}{fmt(x1)} {fmt(my + nr)}"
            f"V{fmt(y1 - cr)}{a}{fmt(x1 - cr)} {fmt(y1)}H{fmt(x0 + cr)}{a}{fmt(x0)} {fmt(y1 - cr)}"
            f"V{fmt(my + nr)}{n}{fmt(x0)} {fmt(my - nr)}V{fmt(y0 + cr)}{a}{fmt(x0 + cr)} {fmt(y0)}Z")


# ============================================================================ carrying and paying

@icon("basket", CAT, "Hand-held shopping basket with a carry handle and woven sides",
      tags=["shopping basket", "groceries", "buy", "store", "market", "shop"], aliases=["shopping-basket"])
def _(S):
    return [
        line(poly([(7, 10), (9.5, 4), (14.5, 4), (17, 10)], r=S.r)),
        line(seg(3, 10, 21, 10)),
        shell(poly([(4.5, 10), (19.5, 10), (18, 20), (6, 20)], closed=True, r=S.r)),
        detail(seg(10, 13, 10, 17)), detail(seg(14, 13, 14, 17)),
    ]


@icon("shopping-bag", CAT, "Paper shopping bag with two loop handles",
      tags=["bag", "shopping", "purchase", "buy", "store", "retail"], aliases=["paper-bag"])
def _(S):
    return [
        shell(rect(4, 7, 16, 14, rr(S, 3))),
        line("M8.5 10.5V6.5A3.5 3.5 0 0 1 15.5 6.5V10.5"),
    ]


_BARS = [(2, 2), (6, 3), (11, 2), (15, 2), (19, 3)]


def _barcode_filled():
    return U(*(P(rect(x, 4, w, 16)) for x, w in _BARS))


@icon("barcode", CAT, "Barcode of vertical bars in different widths",
      tags=["product code", "upc", "ean", "scan", "sku", "label"], aliases=["bar-code"], filled=_barcode_filled)
def _(S):
    return [sq(x, 5, w, 14, 0 if S.name == "line" else 1) for x, w in _BARS]


@icon("qr-code", CAT, "QR code with three corner finder squares and data modules",
      tags=["qr", "scan", "matrix code", "2d barcode", "link", "code"], aliases=["qr"])
def _(S):
    parts = []
    for x, y in ((3, 3), (14, 3), (3, 14)):
        parts += [shell(rect(x, y, 7, 7, 0 if S.name == "line" else 2)), sq(x + 2.5, y + 2.5, 2, 2)]
    parts += [sq(13, 13, 3, 3), sq(18, 13, 3, 3), sq(15.5, 16, 3, 3), sq(13, 19, 3, 3), sq(18, 19, 3, 3)]
    return parts


@icon("credit-card", CAT, "Payment card with a magnetic stripe",
      tags=["card", "payment", "debit card", "bank card", "pay", "plastic"], aliases=["debit-card", "bank-card"])
def _(S):
    return [
        shell(rect(3, 5, 18, 14, rr(S, 3))),
        detail(seg(3, 9.5, 21, 9.5)),
        detail(seg(6.5, 15, 10.5, 15)),
    ]


@icon("cash", CAT, "Two banknotes stacked; cash money",
      tags=["money", "banknotes", "bills", "notes", "payment", "pay"], aliases=["money"])
def _(S):
    return [
        shell(rect(3, 9, 14, 10, rr(S, 2.5))),
        dot(10, 14, 2),
        line(poly([(6.5, 9), (6.5, 5), (21, 5), (21, 15), (17, 15)], r=S.r)),
    ]


@icon("coins", CAT, "Stack of two coins with a third coin standing behind",
      tags=["money", "change", "coin", "currency", "savings", "cents"])
def _(S):
    keep_out = P(rect(-1, 10, 17, 15, 3))
    return [
        shell(rect(3, 13, 10, 8, rr(S))),
        detail(seg(3, 17, 13, 17)),
        line(arc_avoid(15.5, 8, 5.5, keep_out)),
        dot(15.5, 8, 1.75),
    ]


@icon("banknote", CAT, "Single banknote with a round emblem",
      tags=["bill", "note", "money", "cash", "paper money", "currency"])
def _(S):
    return [
        shell(rect(3, 5, 18, 14, rr(S, 2.5))),
        detail(circle(12, 12, 2.5)),
        dot(6.75, 8.75, 1), dot(17.25, 8.75, 1),
    ]


def _pig_body(S):
    body = ellipse(11, 12.5, 7.5, 5.5)
    snout = rect(17, 10, 4, 5, 0 if S.name == "line" else 1.5)
    ear = poly([(11.5, 8), (14, 4), (16, 8.5)], closed=True)
    return union_d(body, snout, ear)


@icon("piggy-bank", CAT, "Piggy bank with a coin slot on its back",
      tags=["savings", "save", "money box", "pig", "deposit", "budget"], aliases=["piggybank"])
def _(S):
    return [
        shell(_pig_body(S)),
        detail(seg(7, 10.5, 10.5, 10.5)),
        dot(15.25, 11.25, 1),
        line(seg(7, 17.5, 7, 21.5)), line(seg(14.5, 17.5, 14.5, 21.5)),
    ]


@icon("gift-card", CAT, "Payment card tied with a ribbon and bow",
      tags=["gift voucher", "voucher", "present", "store credit", "card", "gift"], aliases=["gift-voucher"])
def _(S):
    bow_l = "M8 8C6.5 4.5 3.5 4 3.5 6C3.5 7.4 5.5 8 8 8Z"
    bow_r = "M8 8C9.5 4.5 12.5 4 12.5 6C12.5 7.4 10.5 8 8 8Z"
    return [
        shell(rect(3, 8, 18, 12, rr(S, 3))),
        detail(seg(8, 8, 8, 20)),
        shell(bow_l, stroke_miterlimit="2"), shell(bow_r, stroke_miterlimit="2"),
    ]


@icon("coupon", CAT, "Coupon with notched sides and a percent sign",
      tags=["voucher", "discount code", "promo", "offer", "deal", "percent"], aliases=["voucher"])
def _(S):
    return [shell(notched(3, 5, 21, 19, 2, 0 if S.name == "line" else 2.5)), *pct(12, 12)]


@icon("discount", CAT, "Starburst sticker with a percent sign",
      tags=["percent off", "reduction", "promotion", "offer", "deal", "markdown"], aliases=["percent-off"])
def _(S):
    pts = [polar(12, 12, 9.5 if i % 2 == 0 else 7.75, -90 + i * 15) for i in range(24)]
    return [shell(poly(pts, closed=True, r=S.r * 0.3)), *pct(12, 12)]


@icon("sale", CAT, "Hanging shop sign with a percent sign",
      tags=["sale sign", "clearance", "offer", "discount", "shop sign", "promotion"])
def _(S):
    return [
        line(poly([(6.5, 7), (12, 3.5), (17.5, 7)], r=S.r)),
        shell(rect(3, 7, 18, 14, rr(S, 3))),
        *pct(12, 14),
    ]


# ============================================================================ shipping

@icon("delivery-truck", CAT, "Box delivery truck with a cab and two wheels",
      tags=["delivery", "truck", "van", "courier", "shipping", "transport"], aliases=["box-truck"])
def _(S):
    body = [(3, 4), (14, 4), (14, 8), (18, 8), (21, 11), (21, 14), (3, 14)]
    return [
        shell(poly(body, closed=True, r=S.r)),
        detail(seg(14, 8, 14, 14)),
        shell(circle(7.5, 19, 2)), shell(circle(17, 19, 2)),
    ]


@icon("shipping", CAT, "Parcel moving fast with speed lines",
      tags=["fast delivery", "express", "dispatch", "parcel", "courier", "send"], aliases=["express-shipping"])
def _(S):
    return [
        shell(rect(10, 5, 11, 14, rr(S, 2.5))),
        detail(seg(10, 9.5, 21, 9.5)),
        detail(seg(15.5, 5, 15.5, 9.5)),
        line(seg(4, 8, 7, 8)), line(seg(3, 12, 7, 12)), line(seg(4.5, 16, 7, 16)),
    ]


@icon("return-box", CAT, "Parcel with an arrow turning back to the left; a product return",
      tags=["return", "refund", "send back", "parcel", "exchange", "reverse logistics"], aliases=["product-return"])
def _(S):
    return [
        shell(rect(3, 14, 18, 7, rr(S, 2.5))),
        detail(seg(12, 14, 12, 17)),
        line(poly([(18.5, 11), (18.5, 6), (5.5, 6)], r=S.r * 2)),
        line(poly(head((5, 6), 180, 3), r=S.r)),
    ]


# ============================================================================ in the shop

@icon("cash-register", CAT, "Cash register with a customer display, sloped keypad and a cash drawer",
      tags=["till", "checkout", "point of sale", "register", "cashier", "shop"], aliases=["till"])
def _(S):
    return [
        shell(rect(12.5, 3, 7, 5.5, rr(S, 2.5))),
        shell(poly([(6, 8.5), (18, 8.5), (20, 16), (4, 16)], closed=True, r=S.r)),
        dot(8, 12.5, 1), dot(11.5, 12.5, 1), dot(15, 12.5, 1),
        shell(rect(3, 16, 18, 5, rr(S, 2.5))),
    ]


@icon("pos-terminal", CAT, "Handheld card terminal with a chip card inserted at the top",
      tags=["card reader", "card machine", "payment terminal", "point of sale", "pay", "chip and pin"],
      aliases=["card-terminal", "card-reader"])
def _(S):
    return [
        line(poly([(7, 9), (7, 3), (17, 3), (17, 9)], r=S.r)),
        sq(9.5, 5, 3, 2.5, 0 if S.name == "line" else 0.75),
        shell(rect(5, 9, 14, 12, rr(S, 3))),
        detail(seg(8.5, 12.5, 15.5, 12.5)),
        dot(8.5, 16.5, 1), dot(12, 16.5, 1), dot(15.5, 16.5, 1),
    ]


@icon("shop-scale", CAT, "Shop weighing scale with a bowl on top and a display",
      tags=["weighing scale", "scales", "weight", "grocery", "kilogram", "produce"], aliases=["weighing-scale"])
def _(S):
    bowl = "M4 5H20C20 7.5 16.5 9 12 9C7.5 9 4 7.5 4 5Z"
    return [
        shell(bowl if S.name == "line" else "M5 4.5H19A1 1 0 0 1 20 5.5C19.6 7.7 16.2 9 12 9C7.8 9 4.4 7.7 4 5.5A1 1 0 0 1 5 4.5Z"),
        line(seg(12, 9, 12, 12)),
        shell(poly([(5, 12), (19, 12), (20.5, 21), (3.5, 21)], closed=True, r=S.r)),
        detail(seg(9, 16.5, 15, 16.5)),
    ]


def _shopfront(S):
    """Striped awning over a shop body (walls x 5–19), matching the buildings `store` icon."""
    return [
        shell(poly([(3, 9), (5, 3), (19, 3), (21, 9)], closed=True, r=S.r)),
        detail(seg(9.67, 3, 9, 9)), detail(seg(14.33, 3, 15, 9)),
        shell(poly([(5, 9), (5, 21), (19, 21), (19, 9)], closed=True, r=S.r)),
        detail(seg(3, 9, 21, 9)),
    ]


@icon("store-open", CAT, "Shop front with its door standing open",
      tags=["open", "opening hours", "shop", "store", "welcome", "business hours"], aliases=["shop-open"])
def _(S):
    return [
        *_shopfront(S),
        detail(poly([(9, 21), (9, 13), (15, 13), (15, 21)], r=S.r * 0.5)),
        Part("dot", poly([(9, 13), (12, 14.5), (12, 20), (9, 21)], closed=True)),
    ]


@icon("store-closed", CAT, "Shop front with its shutter pulled down",
      tags=["closed", "shutter", "shop", "store", "out of hours", "business hours"], aliases=["shop-closed"])
def _(S):
    return [*_shopfront(S), detail(seg(5, 13, 19, 13)), detail(seg(5, 17, 19, 17))]


@icon("product", CAT, "A bottle and a box side by side; retail goods",
      tags=["item", "goods", "merchandise", "catalog", "sku", "groceries"], aliases=["goods"])
def _(S):
    bottle = [(5, 3), (8, 3), (8, 7), (10, 9.5), (10, 21), (3, 21), (3, 9.5), (5, 7)]
    return [
        shell(poly(bottle, closed=True, r=S.r * 0.66)),
        detail(seg(3, 13, 10, 13)),
        shell(rect(13, 10, 8, 11, rr(S, 2.5))),
        detail(seg(13, 14, 21, 14)),
    ]


@icon("inventory", CAT, "Three cardboard boxes stacked in a pyramid",
      tags=["stock", "boxes", "warehouse", "storage", "goods", "supply"], aliases=["stock"])
def _(S):
    return [
        shell(rect(7, 5, 10, 8, rr(S, 2.5))),
        shell(rect(3, 13, 18, 8, rr(S, 2.5))),
        detail(seg(12, 13, 12, 21)),
        detail(seg(12, 5, 12, 8.5)),
        detail(seg(7.5, 13, 7.5, 16.5)), detail(seg(16.5, 13, 16.5, 16.5)),
    ]


@icon("warehouse-shelf", CAT, "Warehouse racking with boxes on two shelves",
      tags=["racking", "shelving", "storage", "warehouse", "stock", "pallet rack"], aliases=["racking"])
def _(S):
    return [
        line(poly([(3, 3), (3, 21), (21, 21), (21, 3)], r=S.r)),
        line(seg(3, 12, 21, 12)),
        shell(rect(6.5, 5.5, 5, 6.5, rr(S, 1))), shell(rect(14, 8, 4, 4, rr(S, 1))),
        shell(rect(6.5, 15, 4, 6, rr(S, 1))), shell(rect(13, 16, 5, 5, rr(S, 1))),
    ]


@icon("order", CAT, "Clipboard holding a parcel; a purchase order",
      tags=["purchase order", "orders", "sales order", "clipboard", "fulfilment", "parcel"], aliases=["purchase-order"])
def _(S):
    return [
        shell(poly([(8.5, 4), (5, 4), (5, 21.5), (19, 21.5), (19, 4), (15.5, 4)], r=S.R)),
        shell(rect(8.5, 2.5, 7, 4, min(S.R, 1.5))),
        detail(rect(8.5, 10.5, 7, 6.5, 0 if S.name == "line" else 1.5)),
        detail(seg(12, 10.5, 12, 13)),
    ]


@icon("checkout", CAT, "Shopping cart with an arrow inside; proceed to checkout",
      tags=["pay", "proceed", "cart", "purchase", "buy now", "complete order"], aliases=["proceed-to-checkout"])
def _(S):
    return [
        line(poly([(2, 3), (4.5, 3), (5, 5.5)], r=S.r)),
        shell(poly([(5, 5.5), (21, 5.5), (19, 15.5), (7, 15.5)], closed=True, r=S.r)),
        detail(seg(8.5, 10.5, 14.5, 10.5)),
        detail(poly(head((15, 10.5), 0, 2.5), r=S.r)),
        shell(circle(9, 19.5, 1.5)), shell(circle(17.5, 19.5, 1.5)),
    ]


def _tick(x, y):
    return [(x, y), (x + 1.25, y + 1.25), (x + 3.5, y - 1.25)]


@icon("shopping-list", CAT, "Spiral notepad with ticked items",
      tags=["grocery list", "checklist", "to buy", "notepad", "list", "errands"], aliases=["grocery-list"])
def _(S):
    return [
        shell(rect(5, 4, 14, 17, rr(S, 2.5))),
        line(seg(8.5, 2.5, 8.5, 5.5)), line(seg(12, 2.5, 12, 5.5)), line(seg(15.5, 2.5, 15.5, 5.5)),
        detail(poly(_tick(7.5, 10.5), r=S.r * 0.4)), detail(seg(13, 10, 16, 10)),
        detail(poly(_tick(7.5, 15.5), r=S.r * 0.4)), detail(seg(13, 15, 16, 15)),
    ]


def _heart(cx, cy, s):
    """The v0.1 heart outline scaled by s about (12, 12), then moved to centre (cx, cy)."""
    pts = {"b": (12, 20), "l": (4.4, 12.6), "tl": (11, 6.3), "m": (12, 7.3), "tr": (13, 6.3), "r": (19.6, 12.6)}
    q = {k: (cx + (x - 12) * s, cy + (y - 12.8) * s) for k, (x, y) in pts.items()}
    rr_ = 4.6 * s
    f = lambda k: f"{fmt(q[k][0])} {fmt(q[k][1])}"  # noqa: E731
    return (f"M{f('b')}L{f('l')}A{fmt(rr_)} {fmt(rr_)} 0 0 1 {f('tl')}L{f('m')}L{f('tr')}"
            f"A{fmt(rr_)} {fmt(rr_)} 0 0 1 {f('r')}Z")


@icon("wishlist", CAT, "Sheet with a heart and a list line; saved items",
      tags=["wish list", "saved items", "favourites", "want", "gift ideas", "heart"], aliases=["wish-list"])
def _(S):
    return [
        shell(rect(5, 3, 14, 18, rr(S, 3))),
        detail(_heart(12, 9, 0.46)),
        detail(seg(8.5, 16.5, 15.5, 16.5)),
    ]


def _star(cx, cy, ro, ri):
    return [polar(cx, cy, ro if i % 2 == 0 else ri, -90 + i * 36) for i in range(10)]


@icon("loyalty-card", CAT, "Membership card with a star; a loyalty or rewards card",
      tags=["rewards", "membership", "points", "member card", "vip", "customer loyalty"], aliases=["rewards-card"])
def _(S):
    return [
        shell(rect(3, 5, 18, 14, rr(S, 3))),
        Part("dot", poly(_star(8.5, 12.3, 3.6, 1.6), closed=True, r=0 if S.name == "line" else 0.4)),
        detail(seg(13.5, 10, 17.5, 10)), detail(seg(13.5, 14, 16, 14)),
    ]


@icon("trolley", CAT, "Platform trolley with stacked boxes, a push handle and two wheels",
      tags=["hand truck", "dolly", "platform cart", "moving", "warehouse", "delivery"], aliases=["hand-truck", "dolly"])
def _(S):
    return [
        line(poly([(2.5, 3), (4.5, 3), (4.5, 16), (21, 16)], r=S.r)),
        shell(rect(8, 10, 12, 6, rr(S, 2))), detail(seg(14, 10, 14, 12.5)),
        shell(rect(8, 4, 7, 6, rr(S, 2))), detail(seg(11.5, 4, 11.5, 6.5)),
        shell(circle(8, 19.5, 1.5)), shell(circle(17.5, 19.5, 1.5)),
    ]
