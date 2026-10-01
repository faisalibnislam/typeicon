"""TypeIcon Core: logistics (batch 002, packaging, handling marks, shipping documents, warehouse flow and lifting gear).

Visual language follows sets/logistics_001.py: closed silhouettes are shells, inner lines are details so Filled can
knock them out, nothing is thinner than 2 px. Boxes are plain rectangles with a tape detail, documents are
portrait sheets, and hazard placards are diamonds.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    rect, regular, seg, shell, solid,
)
from geometry import rotation, transform_path

CAT = "logistics"
FILL = Style("filled", "butt", "miter", R=2.0, r=0.0)


def L(S, a, b):
    """Pick a value for Line/Filled (a) or Rounded (b)."""
    return b if S.name == "rounded" else a


def isF(S):
    return S.name == "filled"


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def rr(S, x, y, w, h, cap=2.0):
    return rect(x, y, w, h, min(S.R, cap))


def T(name, description, tags, aliases=()):
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases)(fn)
    return deco


def wheel(x, y=18.0, r=2.0):
    p = shell(circle(x, y, r))
    p.wheel = (x, y, r)
    return p


def hub(x, y, r=1.0):
    p = dot(x, y, r)
    p.knock = True
    return p


def veh_filled(fn):
    def f():
        parts = fn(FILL)
        wh = [p.wheel for p in parts if getattr(p, "wheel", None)]
        holes = [P(p.d) for p in parts if getattr(p, "knock", False)]
        rest = [p for p in parts if not getattr(p, "wheel", None) and not getattr(p, "knock", False)]
        out = filled_region(rest) if rest else None
        if wh:
            cut = U(*[P(circle(x, y, r + 2)) for x, y, r in wh])
            discs = U(*[P(circle(x, y, r + 1)) for x, y, r in wh])
            out = U(D(out, cut), discs) if out is not None else discs
        if holes:
            out = D(out, *holes)
        return out
    return f


def veh(name, description, tags, aliases=()):
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=veh_filled(fn))(fn)
    return deco


def diamond(S, cx=12, cy=12, r=10):
    return shell(poly([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], closed=True, r=S.r))


def sheetp(S, x=4, y=2, w=16, h=20):
    return shell(rr(S, x, y, w, h))


# =========================================================================== packaging and securing

@T("stacked-sacks", "Side view of three filled sacks stacked in a pyramid on a pallet line",
   ["sacks", "bags", "cement bags", "grain sacks", "palletized bags", "bulk goods", "stacked"])
def _(S):
    k = L(S, 2, 3.5)
    return [shell(union(rect(2, 10, 9, 8, k), rect(13, 10, 9, 8, k), rect(7.5, 3, 9, 7, k))),
            line(seg(2, 21, 22, 21))]


@T("shrink-hood", "Pallet load under a tight plastic hood with a heat gun blowing on its side",
   ["shrink wrap", "heat shrink", "pallet hood", "plastic hood", "heat gun", "load protection", "stretch hood"])
def _(S):
    return [shell(rr(S, 2, 4, 10, 14, 4)), detail(seg(2, 11, 12, 11)), line(seg(2, 21, 12, 21)),
            shell(rr(S, 17, 5, 5, 6, 1)), line(seg(19.5, 11, 19.5, 17)),
            line(seg(14, 7, 16, 7)), line(seg(14, 10, 16, 10))]


@T("pallet-cover", "Pallet load under a quilted insulated cover with a zip down one side",
   ["thermal cover", "insulated blanket", "pallet blanket", "cold chain", "zip cover", "temperature protection", "shroud"])
def _(S):
    return [shell(rr(S, 3, 3, 18, 16, 4)), detail(seg(3, 8, 13, 8)), detail(seg(3, 13, 13, 13)),
            detail(seg(17, 3, 17, 19)), dot(17, 9, 1.25), line(seg(2, 21.5, 22, 21.5))]


@T("banded-bundle", "Bundle of boards tied with two metal straps",
   ["strapped bundle", "lumber bundle", "timber pack", "steel banding", "boards", "strapping", "bound"])
def _(S):
    return [shell(rr(S, 2, 6, 20, 12, 4)), detail(seg(2, 10, 22, 10)), detail(seg(2, 14, 22, 14)),
            line(seg(7, 3, 7, 21)), line(seg(17, 3, 17, 21))]


@T("strapping-tensioner", "Hand tensioning tool with two lever handles gripping a strap around a box",
   ["strap tensioner", "strapping tool", "banding tool", "tie down", "strap tightener", "packing tool", "pliers"])
def _(S):
    return [shell(rr(S, 2, 12, 12, 9, 1)), detail(seg(8, 12, 8, 21)), shell(rr(S, 5, 6, 7, 6, 1)),
            line(seg(12, 8, 21, 3.5)), line(seg(12, 10.5, 21, 12))]


@T("strapping-coil", "Coil of flat strap on a core with a loose end lying along the bottom",
   ["strap roll", "banding coil", "plastic strapping", "pp strap", "packing strap", "roll of strap", "steel band"])
def _(S):
    return [shell(circle(11, 11, 8.5)), detail(circle(11, 11, 5)), dot(11, 11, 1.5),
            line(seg(11, 19.5, 22, 19.5))]


@T("carton-sealer", "Box passing under a machine frame whose tape head seals the top seam",
   ["case sealer", "box taping machine", "tape head", "packaging line", "tape applicator", "sealing machine", "carton taping"])
def _(S):
    return [line(poly([(3, 21), (3, 4), (21, 4), (21, 21)], r=S.r)), shell(rr(S, 9, 4, 6, 4, 1)),
            dot(12, 10.5, 1.5), shell(rr(S, 7, 13, 10, 6, 1)), detail(seg(12, 13, 12, 16))]


@T("tilt-indicator", "Sticker with a triangular channel and a small ball resting in one arm",
   ["tilt watch", "tip indicator", "tilt label", "handling monitor", "orientation sensor", "tipped over", "shipping label"])
def _(S):
    return [shell(rr(S, 2, 3, 20, 18)), detail(poly([(5.5, 18), (12, 7), (18.5, 18)], closed=True)),
            dot(10, 15.5, 1.25)]


@T("shock-indicator", "Small label with a capsule window holding a coloured bar that shows impact",
   ["impact indicator", "shock watch", "drop indicator", "impact label", "handling monitor", "fragile monitor", "g force"])
def _(S):
    return [shell(rr(S, 2, 6, 20, 12, 4)), detail(rect(5.5, 9, 13, 6, 3)), solid(rect(12, 10.5, 5, 3))]


@T("do-not-stack", "Box with a second box above it struck through by a diagonal line",
   ["no stacking", "do not stack", "stacking limit", "handling mark", "top load prohibited", "keep on top", "no pile"])
def _(S):
    return [shell(rr(S, 3, 14, 18, 7)), shell(rr(S, 7, 3, 10, 7)), detail(seg(4, 2, 20, 11.5))]


@T("un-number-panel", "Placard split into two rows each showing four digits",
   ["hazard panel", "kemler plate", "orange plate", "adr panel", "dangerous goods plate", "hazard id number", "tanker plate"])
def _(S):
    return [shell(rr(S, 2, 5, 20, 14, 4)), detail(seg(2, 12, 22, 12)),
            *[dot(x, 8.5, 1) for x in (6, 10, 14, 18)], *[dot(x, 15.5, 1) for x in (6, 10, 14, 18)]]


def _lq_filled():
    outer = [(12, 2), (22, 12), (12, 22), (2, 12)]
    body = U(P(poly(outer, closed=True)), ST(poly(outer, closed=True), 2.0, "butt", "miter", 4.0))
    band = P(poly([(5.6, 10.2), (18.4, 10.2), (19.4, 12), (18.4, 13.8), (5.6, 13.8), (4.6, 12)], closed=True))
    return D(body, band)


@icon("limited-quantity-mark", CAT, "Diamond outline with solid top and bottom triangles and an empty middle band",
      tags=["limited quantity", "lq mark", "dangerous goods", "small quantity", "hazard mark", "adr", "packaging mark"],
      filled=_lq_filled)
def _(S):
    return [shell(poly([(12, 2), (22, 12), (12, 22), (2, 12)], closed=True, r=S.r)),
            detail(seg(5, 9, 19, 9)), detail(seg(5, 15, 19, 15)),
            solid(poly([(12, 4), (17, 9), (7, 9)], closed=True)), solid(poly([(12, 20), (17, 15), (7, 15)], closed=True))]


@T("lithium-battery-label", "Square label with a battery carrying a flame inside",
   ["lithium battery", "battery hazard", "battery warning", "li-ion label", "fire risk", "cell shipping", "dangerous goods"])
def _(S):
    return [shell(rr(S, 2, 2, 20, 20)), detail(rect(7.5, 8.5, 9, 10, 1)), detail(seg(10.5, 6.5, 13.5, 6.5)),
            Part("dot", poly([(12, 11), (14, 14.5), (12, 17), (10, 14.5)], closed=True))]


@T("marine-pollutant-mark", "Diamond placard with a dead fish lying under bare branches",
   ["marine pollutant", "environmental hazard", "aquatic toxicity", "dead fish", "water pollution", "hazmat mark", "imdg"])
def _(S):
    return [diamond(S), detail("M12 10V6"), detail("M12 8L10 6.5"), detail("M12 8L14 6.5"),
            detail(ellipse(11, 14.5, 4, 2.5)), detail(poly([(14.5, 14.5), (17, 12.5), (17, 16.5)], closed=True)),
            dot(9.5, 14, 0.8)]


@T("magnetized-material-label", "Square label with a horseshoe magnet and field arcs beside it",
   ["magnetic material", "magnet label", "magnetized cargo", "compass deviation", "air cargo mark", "magnetic field", "iata label"])
def _(S):
    return [shell(rr(S, 2, 2, 20, 20)), detail("M8 17V11.5a4 4 0 0 1 8 0V17"), detail(seg(7, 17, 9.5, 17)),
            detail(seg(14.5, 17, 17, 17)), detail("M5 10a7 7 0 0 1 3-4"), detail("M19 10a7 7 0 0 0-3-4")]


def dp(pts, closed=True):
    """Small solid polygon: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", poly(pts, closed=closed))


@T("fragile-tape", "Roll of tape with a strip unrolled beneath it printed with repeating glass bowls",
   ["fragile tape", "handle with care tape", "warning tape", "packing tape", "glass tape", "breakable", "printed tape"])
def _(S):
    return [shell(circle(8, 8.5, 6)), detail(circle(8, 8.5, 2)), shell(rr(S, 2, 15, 20, 7, 4)),
            dp([(4.5, 17.5), (8.5, 17.5), (6.5, 20.5)]), dp([(10.5, 17.5), (14.5, 17.5), (12.5, 20.5)]),
            dp([(16.5, 17.5), (20.5, 17.5), (18.5, 20.5)])]


def plane(S, cx, cy):
    return [detail(seg(cx, cy - 4, cx, cy + 4)), detail(poly([(cx - 4.5, cy + 0.5), (cx, cy - 2), (cx + 4.5, cy + 0.5)], r=S.r)),
            detail(poly([(cx - 2, cy + 4.5), (cx, cy + 3), (cx + 2, cy + 4.5)], r=S.r))]


@T("air-waybill", "Document sheet with a small plane at the top and a barcode strip along the bottom",
   ["awb", "air cargo document", "airway bill", "air freight paperwork", "shipping document", "consignment note", "flight cargo"])
def _(S):
    return [sheetp(S), *plane(S, 12, 8.5), detail(seg(8, 16, 8, 19)), detail(seg(12, 16, 12, 19)),
            detail(seg(16, 16, 16, 19))]


@T("certificate-of-origin", "Landscape certificate with a globe and a round seal with two ribbons",
   ["origin certificate", "trade document", "export paperwork", "country of origin", "customs document", "globe certificate", "made in"])
def _(S):
    return [shell(rr(S, 2, 3, 20, 13)), detail(circle(8.5, 9.5, 3.5)), detail(seg(5, 9.5, 12, 9.5)),
            shell(circle(17, 16, 3)), line(seg(16, 19, 15, 22)), line(seg(18, 19, 19, 22))]


@T("delivery-note", "Sheet with a small truck at the top, an item line and a signature squiggle",
   ["delivery docket", "proof of delivery", "goods received note", "packing slip", "pod", "signed delivery", "dispatch note"])
def _(S):
    return [sheetp(S), detail(rect(6.5, 5, 5.5, 4)), detail("M12 6.5h2.5l1.5 2v0.5H12"), dot(9, 10.2, 1),
            dot(14.5, 10.2, 1), detail(seg(7, 13.5, 17, 13.5)), detail("M7 18c1.3-2.5 2.2-2.5 3.2 0s2 2.5 3 0")]


@T("dangerous-goods-declaration", "Document with a diamond hazard placard at the top right and form lines",
   ["dgd", "shipper declaration", "hazmat paperwork", "hazard form", "dangerous cargo form", "adr document", "iata declaration"])
def _(S):
    return [sheetp(S, 3, 2, 18, 20), detail(poly([(14.5, 4.5), (18, 8), (14.5, 11.5), (11, 8)], closed=True, r=S.r)),
            detail(seg(6, 6, 8, 6)), detail(seg(6, 10, 8, 10)), detail(seg(6, 15, 18, 15)), detail(seg(6, 18.5, 14, 18.5))]


@T("customs-tariff", "Parcel box beside a hanging tag showing a percent sign",
   ["duty rate", "import duty", "tariff rate", "customs tax", "vat", "tax tag", "duties and taxes"])
def _(S):
    return [shell(rr(S, 2, 11, 9, 10, 1)), detail(seg(6.5, 11, 6.5, 14)),
            shell(poly([(18, 3), (22, 6.5), (22, 17), (14, 17), (14, 6.5)], closed=True, r=S.r)),
            dot(16.5, 10.2, 1), dot(19.5, 14, 1), detail(seg(19.5, 9.5, 16.5, 14.5))]


@T("bonded-warehouse", "Warehouse building with a padlock on its front",
   ["bonded store", "customs warehouse", "duty suspended", "locked warehouse", "secure storage", "under bond", "customs hold"])
def _(S):
    return [shell(poly([(2, 21), (2, 9), (12, 3), (22, 9), (22, 21)], closed=True, r=S.r)),
            detail(rect(8, 14, 8, 6, 1)), detail("M9.5 14v-1.5a2.5 2.5 0 0 1 5 0V14"), dot(12, 17, 1)]


@T("nothing-to-declare", "Hanging airport sign showing an arrow toward an empty suitcase outline",
   ["green channel", "customs exit", "nothing to declare", "airport customs", "arrival sign", "no goods", "border crossing"])
def _(S):
    return [shell(rr(S, 2, 6, 20, 13)), line(seg(6, 2, 6, 6)), line(seg(18, 2, 18, 6)),
            detail(seg(5, 12.5, 10, 12.5)), detail("M8 10l-3 2.5L8 15"), detail(rect(13, 10.5, 6, 5, 1)),
            detail("M14.5 10.5V9h3v1.5")]


@T("sniffer-dog", "Dog with its nose down beside a suitcase and sniff lines curling up",
   ["detection dog", "customs dog", "k9", "drug dog", "security dog", "baggage search", "inspection dog"])
def _(S):
    return [shell(union(rect(2, 6, 9, 6.5, 3.2), poly([(9, 7), (13, 7), (17, 12), (17, 14.5), (14, 14.5), (9, 11)], closed=True, r=S.r))),
            line(seg(4, 12.5, 4, 19)), line(seg(9, 12.5, 9, 19)), shell(rr(S, 18.5, 14, 3.5, 6, 1)),
            line("M14 2.5c1.5 1 1.5 2.5 0 3.5"), line("M18 2.5c1.5 1 1.5 2.5 0 3.5"), dot(13.5, 9, 0.8)]


@T("parcel-pickup-point", "Map pin holding a small parcel box",
   ["pickup location", "click and collect", "parcel locker", "collection point", "drop off point", "service point", "parcel shop"])
def _(S):
    return [shell("M12 22L5.8 14A7 7 0 1 1 18.2 14Z"), detail(rect(8.5, 6, 7, 6, L(S, 0, 2))), detail(seg(8.5, 8.5, 15.5, 8.5))]


@T("parcel-drop-box", "Freestanding metal box with a drop hatch on its front and a keyhole below",
   ["parcel box", "package drop", "mailbox", "drop off locker", "secure drop box", "return box", "parcel depot"])
def _(S):
    return [shell(rr(S, 5, 2, 14, 19, 3)), detail(rect(8, 5.5, 8, 5, 1)), dot(12, 8, 1),
            dot(12, 15, 1.25), line(seg(7, 22, 7, 23)), line(seg(17, 22, 17, 23))]


@T("delivery-photo", "Smartphone screen with corner brackets framing a box resting on a mat",
   ["proof of delivery photo", "parcel photo", "doorstep photo", "delivery proof", "camera frame", "drop photo", "package picture"])
def _(S):
    return [shell(rr(S, 4, 2, 16, 20, 3)), detail("M7.5 8V5.5H10"), detail("M16.5 8V5.5H14"), detail("M7.5 13V15.5H10"),
            detail("M16.5 13V15.5H14"), detail(rect(9.5, 8, 5, 5)), detail(seg(8, 18.5, 16, 18.5))]


@T("shipment-timeline", "Horizontal line with four stops, three filled and the last empty, and a truck above the third",
   ["tracking progress", "delivery progress", "shipment status", "order tracking", "transit stages", "parcel journey", "delivery steps"])
def _(S):
    return [line(seg(4, 18, 20, 18)), dot(4, 18, 2), dot(9.3, 18, 2), dot(14.7, 18, 2), shell(circle(20, 18, 2.2)),
            shell(poly([(10, 6), (16, 6), (16, 8.5), (19, 8.5), (21, 11.5), (21, 13), (10, 13)], closed=True, r=S.r)),
            dot(13, 13.5, 1.2), dot(18, 13.5, 1.2)]


@T("delivery-date", "Calendar page with a parcel box in the middle of the grid",
   ["expected delivery", "arrival date", "eta", "schedule delivery", "delivery day", "parcel calendar", "shipping date"])
def _(S):
    return [shell(rr(S, 3, 4, 18, 17, 4)), detail(seg(3, 9, 21, 9)), line(seg(8, 2, 8, 6)), line(seg(16, 2, 16, 6)),
            detail(rect(8.5, 12, 7, 6, 1)), detail(seg(8.5, 14.5, 15.5, 14.5))]


@T("contactless-delivery", "Parcel on the ground, a person stepping back and a two-headed distance arrow between",
   ["no contact delivery", "leave at door", "safe drop", "social distance delivery", "doorstep drop", "touchless delivery", "distanced handoff"])
def _(S):
    return [shell(rr(S, 2, 15, 7, 6, 1)), detail(seg(5.5, 15, 5.5, 17.5)),
            line(seg(4, 10, 14, 10)), line("M6.5 7.5L4 10l2.5 2.5"), line("M11.5 7.5L14 10l-2.5 2.5"),
            shell(circle(19.5, 5.5, 2)), line(seg(19.5, 8, 19.5, 15)), line("M19.5 15l-2 5.5"), line("M19.5 15l2 5.5")]


def rpts(pts, deg, c):
    a = math.radians(deg)
    return [(c[0] + (x - c[0]) * math.cos(a) - (y - c[1]) * math.sin(a),
             c[1] + (x - c[0]) * math.sin(a) + (y - c[1]) * math.cos(a)) for x, y in pts]


def box_pts(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


# =========================================================================== warehouse flow


@T("restocking", "Box on the floor with a curved arrow rising to a box on a shelf plank",
   ["replenishment", "restock shelf", "refill stock", "put away", "inventory refill", "stock up", "replenish"])
def _(S):
    return [shell(rr(S, 2, 14, 7, 7, 1)), detail(seg(5.5, 14, 5.5, 16.5)), line("M5.5 11C5.5 6.5 8 4.5 12 4.5"),
            line("M10 2.5L12.5 4.5L10 6.5"), shell(rr(S, 15, 4, 6, 8, 1)), line(seg(13, 12, 22, 12))]


@T("overstock", "Shelf row of crowded boxes with an extra box tipping over the edge on top",
   ["excess inventory", "too much stock", "surplus stock", "overfull shelf", "overloaded shelf", "overcapacity", "stock glut"])
def _(S):
    tilt = poly(rpts(box_pts(14, 4, 6, 7), 24, (17, 11)), closed=True, r=S.r * 0.6)
    return [shell(rr(S, 2, 11, 9, 8, 1)), shell(rr(S, 13, 11, 9, 8, 1)), shell(rr(S, 3, 3, 6, 8, 1)),
            shell(tilt), line(seg(1.5, 21.5, 22.5, 21.5))]


@T("fifo-lane", "Lane with two boxes, an arrow entering at the back and an arrow leaving at the front",
   ["first in first out", "fifo", "queue lane", "flow rack", "stock rotation", "gravity lane", "carton flow"])
def _(S):
    return [line(seg(2, 20, 22, 20)), shell(rr(S, 6, 11, 5, 7, 1)), shell(rr(S, 13, 11, 5, 7, 1)),
            line(seg(2, 6, 8, 6)), line("M5.5 3.5L8 6L5.5 8.5"), line(seg(16, 6, 22, 6)), line("M19.5 3.5L22 6L19.5 8.5")]


@T("stock-transfer", "Two small warehouses with a box and an arrow passing between them",
   ["inter warehouse transfer", "branch transfer", "move stock", "stock movement", "internal transfer", "relocation", "warehouse to warehouse"])
def _(S):
    return [shell(poly([(2, 21), (2, 13), (5, 10), (8, 13), (8, 21)], closed=True, r=S.r)),
            shell(poly([(16, 21), (16, 13), (19, 10), (22, 13), (22, 21)], closed=True, r=S.r)),
            shell(rr(S, 10, 13, 4, 4, 1)), line(seg(9, 7, 15, 7)), line("M12.8 4.5L15.3 7L12.8 9.5")]


@T("kanban-bin", "Two parts bins side by side, one with a card standing out of its label slot",
   ["kanban", "parts bin", "two bin system", "reorder card", "lean supply", "replenishment signal", "storage bin"])
def _(S):
    return [shell(rr(S, 2, 9, 9, 11, 2)), shell(rr(S, 13, 9, 9, 11, 2)), detail(seg(4.5, 16, 8.5, 16)),
            detail(seg(15.5, 16, 19.5, 16)), line("M16 13V3.5h4V13")]


@T("dropshipping", "Factory and house joined by a dashed arrow carrying a box above a small shop",
   ["drop shipping", "direct ship", "supplier to customer", "fulfilment without stock", "ecommerce model", "third party shipping", "bypass shop"])
def _(S):
    return [shell(poly([(2, 21), (2, 12), (5, 14.5), (5, 12), (8, 14.5), (8, 21)], closed=True, r=S.r)),
            shell(poly([(16, 21), (16, 15), (19, 12), (22, 15), (22, 21)], closed=True, r=S.r)),
            shell(rr(S, 10.5, 16, 3, 5, 1)), line(seg(2, 6, 5, 6)), shell(rr(S, 8, 3.5, 6, 5, 1)),
            line(seg(17, 6, 21, 6)), line("M18.5 3.5L21 6L18.5 8.5")]


@T("shipment-consolidation", "Three small boxes with lines converging into one large box",
   ["consolidation", "combine shipments", "groupage", "merge parcels", "lcl", "bundle orders", "many to one"])
def _(S):
    return [shell(rr(S, 2, 2.5, 5, 5, 1)), shell(rr(S, 2, 9.5, 5, 5, 1)), shell(rr(S, 2, 16.5, 5, 5, 1)),
            line(seg(8.5, 5, 12.5, 10)), line(seg(8.5, 12, 12.5, 12)), line(seg(8.5, 19, 12.5, 14)),
            shell(rr(S, 14, 6.5, 8, 11, 1)), detail(seg(18, 6.5, 18, 10))]


@T("load-plan", "Top view of a trailer outline packed with box rectangles of different sizes",
   ["loading plan", "trailer load", "cube planning", "stowage plan", "truck loading", "cargo layout", "load diagram"])
def _(S):
    return [shell(rr(S, 2, 5, 20, 14, 4)), detail(seg(8.5, 5, 8.5, 19)), detail(seg(8.5, 12, 15.5, 12)),
            detail(seg(15.5, 5, 15.5, 19)), detail(seg(15.5, 14, 22, 14))]


@T("goods-receiving", "Open dock door with a box on an arrow heading in and a tick above the doorway",
   ["inbound", "receiving dock", "goods in", "delivery check in", "unloading", "receive stock", "inbound dock"])
def _(S):
    return [shell(poly([(10, 21), (10, 9), (16, 4), (22, 9), (22, 21)], closed=True, r=S.r)),
            detail(rect(13, 13, 6, 8)), shell(rr(S, 2, 14, 5, 6, 1)), line(seg(2, 10.5, 7, 10.5)),
            line("M4.8 8L7.3 10.5L4.8 13"), detail("M13.8 8.5L15.6 10.3L18.4 7.2")]


@T("pallet-put-away", "Forklift raising a loaded pallet on its mast toward a tall rack with an empty slot",
   ["put away", "rack loading", "pallet storage", "racking", "forklift lift", "store pallet", "high bay"])
def _(S):
    return [line(seg(17, 2, 17, 22)), line(seg(22, 2, 22, 22)), line(seg(17, 8, 22, 8)), line(seg(17, 15, 22, 15)),
            shell(rr(S, 2, 14, 6, 5, 1)), line(seg(10, 3, 10, 19)), line(seg(10, 10, 15, 10)),
            shell(rr(S, 10.5, 4, 4.5, 4.5, 0.5)), wheel(4, 20.5, 1.5), wheel(9, 20.5, 1.5)]


@T("order-picking", "Shelf of four slots with a box leaving one on an arrow into a tote below",
   ["pick", "picking", "order fulfilment", "pick and pack", "warehouse picking", "pick from shelf", "tote picking"])
def _(S):
    return [shell(rr(S, 2, 2, 12, 11, 1)), detail(seg(8, 2, 8, 13)), detail(seg(2, 7.5, 14, 7.5)),
            line("M18 3V9"), line("M15.5 7L18 9.5L20.5 7"),
            shell(poly([(9, 16), (22, 16), (20, 22), (11, 22)], closed=True, r=S.r))]


@T("packing-station", "Workbench with a tape roll and an open box with its flaps up on top",
   ["pack bench", "packing table", "packing area", "pack out", "boxing station", "wrapping table", "fulfilment bench"])
def _(S):
    return [line(seg(2, 16, 22, 16)), line(seg(4, 16, 4, 22)), line(seg(20, 16, 20, 22)),
            shell(circle(5, 12, 2.5)), shell(rr(S, 11, 10, 9, 6, 1)), line("M11 10L9.5 6.5"), line("M20 10L21.5 6.5")]


@T("cross-docking", "Warehouse outline with a straight arrow running through it from side to side",
   ["cross dock", "flow through", "transshipment", "direct transfer", "no storage", "through dock", "transfer hub"])
def _(S):
    return [shell(rr(S, 6, 4, 10, 16, 2)), detail(seg(2, 12, 21, 12)), detail("M18 9l3 3-3 3")]


@T("cold-storage-warehouse", "Warehouse building with a large snowflake on its front",
   ["cold store", "frozen storage", "freezer warehouse", "chilled warehouse", "refrigerated storage", "cold chain hub", "cold room"])
def _(S):
    return [shell(poly([(2, 21), (2, 9), (12, 3), (22, 9), (22, 21)], closed=True, r=S.r)),
            detail(seg(12, 10, 12, 18)), detail(seg(8.5, 12, 15.5, 16)), detail(seg(8.5, 16, 15.5, 12))]


@T("walk-in-freezer", "Heavy insulated door with a large latch lever and a thermometer beside it",
   ["walk in cooler", "cold room door", "freezer door", "cold storage door", "insulated door", "chill room", "freezer room"])
def _(S):
    return [shell(rr(S, 2, 2, 13, 20, 2)), detail(rect(5, 5, 7, 14)), detail(seg(8, 12, 11, 12)),
            shell(union(rect(18.5, 3, 3, 12, 1.5), circle(20, 17.5, 2.5))), dot(20, 17.5, 1)]


def lean(a, b, t, side=1):
    """Quad for a thin sheet along a->b, offset t to one side."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    nx, ny = -dy / n * side, dx / n * side
    return [a, b, (b[0] + nx * t, b[1] + ny * t), (a[0] + nx * t, a[1] + ny * t)]


# =========================================================================== load securing and handling equipment


@T("lashing-bar", "Long rod with an eye at the top and a turnbuckle in the middle braced diagonally in a container corner",
   ["lashing rod", "container lashing", "securing rod", "cargo lashing", "turnbuckle", "sea fastening", "brace bar"])
def _(S):
    tb = poly(rpts(box_pts(8.75, 11.4, 6, 3.2), 131.3, (11.75, 13)), closed=True, r=S.r * 0.5)
    return [line(poly([(22, 2), (22, 21), (2, 21)], r=S.r)), shell(circle(19.2, 5.5, 2)),
            line(seg(17.8, 7.2, 13.7, 10.7)), shell(tb), line(seg(9.8, 15.3, 6, 19.5))]


@veh("high-loader", "Scissor lift vehicle raising a cargo deck with a box level with an aircraft door",
     ["air cargo loader", "cargo loader", "scissor lift truck", "aircraft loader", "ground handling", "uld loader", "catering lift"])
def _(S):
    return [shell(rr(S, 2, 15, 14, 3, 1)), wheel(6, 20.5, 1.5), wheel(12.5, 20.5, 1.5),
            line(seg(5, 15, 13, 9.5)), line(seg(5, 9.5, 13, 15)), shell(rr(S, 3, 7, 12, 2.5, 1)),
            shell(rr(S, 5, 2, 7, 5, 3)), shell(rr(S, 18, 3, 4.5, 12, 2))]


@veh("piggyback-railcar", "Flat railcar carrying a truck trailer whose wheels rest on the deck",
     ["trailer on flatcar", "rail trailer", "intermodal rail", "rolling highway", "trailer train", "tofc", "rail freight"])
def _(S):
    return [shell(rr(S, 2, 16, 20, 2, 1)), wheel(6, 20.5, 1.5), wheel(18, 20.5, 1.5),
            shell(rect(3, 4, 18, 9, L(S, 0, 2))), detail(seg(9, 4, 9, 13)), line(seg(5, 13, 5, 16)),
            dot(15, 14.3, 1.4), dot(19, 14.3, 1.4)]


@veh("centerbeam-flatcar", "Flat railcar with a tall central lattice wall and lumber bundles stacked on both sides",
     ["center beam", "lumber car", "bulkhead flatcar", "timber railcar", "rail freight", "lumber bundles", "centre beam wagon"])
def _(S):
    return [shell(rr(S, 2, 16, 20, 2, 1)), wheel(6, 20.5, 1.5), wheel(18, 20.5, 1.5),
            shell(rr(S, 10, 2, 4, 14, 0.5)), detail(seg(10, 7, 14, 7)), detail(seg(10, 11.5, 14, 11.5)),
            shell(rr(S, 2.5, 8, 5.5, 8, 3)), shell(rr(S, 16, 8, 5.5, 8, 3)),
            detail(seg(2.5, 12, 8, 12)), detail(seg(16, 12, 21.5, 12))]


@veh("hook-lift-truck", "Truck with a bent hook arm pulling an open roll-off bin onto its frame",
     ["roll off truck", "skip lorry", "hooklift", "skip loader", "container hook", "waste bin truck", "dumpster truck"])
def _(S):
    return [shell(poly([(2, 7), (15, 7), (14, 15), (3, 15)], closed=True, r=S.r)),
            shell(poly([(16, 15), (16, 9), (19, 9), (22, 12.5), (22, 15)], closed=True, r=S.r)),
            wheel(6, 19, 2), wheel(11, 19, 2), wheel(19, 19, 2),
            line("M15.5 14L15.5 3.5H7"), line("M7 3.5V7")]


@veh("glass-transport-truck", "Truck with an A-frame rack on its bed holding large glass panes leaning on both sides",
     ["glass truck", "a frame truck", "pane transport", "window delivery", "glazier truck", "sheet glass", "glass rack"])
def _(S):
    return [shell(poly([(2, 17), (2, 16), (16, 16), (16, 10), (19, 10), (22, 13), (22, 17)], closed=True, r=S.r * 0.5)),
            shell(poly([(4, 16), (9, 3), (14, 16)], closed=True, r=S.r)), detail(seg(9, 8, 9, 16)),
            wheel(6, 19.5, 1.5), wheel(12, 19.5, 1.5), wheel(19, 19.5, 1.5)]


@veh("modular-transporter", "Long flat platform on many small wheels carrying a large cylindrical tank",
     ["spmt", "heavy haulage", "self propelled modular transporter", "oversize load", "tank carrier", "wide load", "heavy transport"])
def _(S):
    return [shell(rr(S, 2, 14, 20, 3, 1)), shell(rr(S, 4, 4, 16, 9, 4)), detail(seg(8, 4, 8, 13)),
            detail(seg(16, 4, 16, 13)), dot(4.5, 20.3, 1.5), dot(9, 20.3, 1.5), dot(13.5, 20.3, 1.5),
            dot(18, 20.3, 1.5)]


@T("chain-binder", "Lever load binder with a long handle and two hooks pulling chain links together",
   ["load binder", "ratchet binder", "chain tensioner", "lever binder", "tie down", "flatbed securing", "chain tightener"])
def _(S):
    return [shell(ellipse(3.5, 17, 2.5, 1.75)), shell(ellipse(20.5, 17, 2.5, 1.75)), line(seg(6, 17, 9, 17)),
            line(seg(15, 17, 18, 17)), shell(rr(S, 9, 14, 6, 6, 3)), line(seg(12, 14, 18.5, 3)), dot(18.5, 3.5, 1.4)]


@T("load-bar", "Telescoping bar with rubber end pads wedged across a trailer in front of two boxes",
   ["cargo bar", "load lock", "trailer bar", "decking beam", "cargo restraint", "shoring bar", "truck load bar"])
def _(S):
    return [line(seg(2, 3, 2, 21)), line(seg(22, 3, 22, 21)), shell(rr(S, 3.5, 5.5, 2.5, 7, 1)),
            shell(rr(S, 18, 5.5, 2.5, 7, 1)), line(seg(6, 9, 18, 9)), detail(seg(12, 7, 12, 11)),
            shell(rr(S, 4.5, 14, 6, 7, 1)), shell(rr(S, 13.5, 14, 6, 7, 1))]


@T("dunnage-bag", "Inflated air bag with a valve squeezed between two stacks of boxes",
   ["air bag", "void fill", "cargo airbag", "inflatable dunnage", "load stabiliser", "gap filler", "air cushion"])
def _(S):
    return [shell(rr(S, 2, 6, 5, 15, 1)), detail(seg(2, 13.5, 7, 13.5)), shell(rr(S, 17, 6, 5, 15, 1)),
            detail(seg(17, 13.5, 22, 13.5)), shell(rect(9.5, 8, 5, 11, L(S, 2, 2.5))), line(seg(12, 8, 12, 3)), dot(12, 3, 1.25)]


@T("tie-down-ring", "Folding D-shaped ring hinged to a square floor plate with four bolt holes",
   ["d ring", "lashing ring", "anchor point", "cargo ring", "floor anchor", "tie down point", "trailer anchor"])
def _(S):
    return [shell(rr(S, 2, 2, 20, 20, 3)), dot(5.5, 5.5, 1.25), dot(18.5, 5.5, 1.25), dot(5.5, 18.5, 1.25),
            dot(18.5, 18.5, 1.25), detail("M7.5 16V11a4.5 4.5 0 0 1 9 0V16Z")]


@T("rack-guard", "Steel foot guard around a rack upright with diagonal hazard stripes",
   ["upright protector", "column guard", "rack protector", "pallet rack guard", "impact guard", "forklift bumper", "rack foot guard"])
def _(S):
    return [shell(rr(S, 9.5, 2, 5, 12, 1)), shell(rr(S, 5, 13, 14, 8, 2)),
            detail(seg(8, 20, 10.5, 14)), detail(seg(12.5, 20, 15, 14)), line(seg(2, 22.5, 22, 22.5))]


@veh("clamp-forklift", "Forklift with two large flat pads in place of forks squeezing a stack of boxes",
     ["clamp truck", "carton clamp", "appliance clamp", "box clamp", "paper roll clamp", "lift truck clamp", "clamp attachment"])
def _(S):
    return [shell(rr(S, 2, 12, 8, 5, 1)), line(seg(3, 12, 3, 6)), wheel(5, 19.5, 1.5), wheel(9, 19.5, 1.5),
            line(seg(11.5, 3, 11.5, 18)), line(seg(14, 6, 14, 16)), line(seg(22, 6, 22, 16)), line(seg(14, 6, 22, 6)),
            shell(rr(S, 16, 8, 4, 4, 0.5)), shell(rr(S, 16, 12.5, 4, 4, 0.5))]


@T("forklift-safety-cage", "Mesh work cage with a grid of wire on forks raised part way up a mast",
   ["work platform", "man basket", "personnel cage", "forklift platform", "lift basket", "access cage", "order picker cage"])
def _(S):
    return [line(seg(3, 2, 3, 21)), line(seg(3, 18.5, 21, 18.5)), shell(rr(S, 7, 5, 14, 11, 1)),
            detail(seg(12, 5, 12, 16)), detail(seg(16.5, 5, 16.5, 16)), detail(seg(7, 10.5, 21, 10.5))]


@T("mobile-racking", "Row of tall shelving units on floor rails, the end one with a three-spoke crank wheel",
   ["mobile shelving", "compact shelving", "movable racking", "rolling shelves", "high density storage", "archive shelving", "sliding racks"])
def _(S):
    return [shell(rr(S, 2, 3, 5, 15, 1)), shell(rr(S, 9, 3, 5, 15, 1)), shell(rr(S, 16, 3, 6, 15, 1)),
            detail(seg(2, 10.5, 7, 10.5)), detail(seg(9, 10.5, 14, 10.5)), detail(circle(19, 10.5, 2.25)),
            line(seg(2, 20.5, 22, 20.5))]


@T("panel-cart", "Wheeled A-frame cart carrying large flat sheets leaning on one side",
   ["sheet cart", "plywood cart", "drywall cart", "board trolley", "a frame trolley", "panel trolley", "glass cart"])
def _(S):
    return [line(seg(12, 4, 3, 17)), line(seg(12, 4, 21, 17)), shell(poly(lean((3.5, 16.5), (11.5, 5.5), 3.5), closed=True, r=S.r * 0.4)),
            line(seg(2, 17, 22, 17)), wheel(6, 20, 1.5), wheel(18, 20, 1.5)]


@veh("machine-skates", "Pair of low roller skates with swivel plates carrying a heavy machine block",
     ["machinery skates", "roller skates for machines", "heavy load skates", "equipment mover", "moving skates", "load skates", "rigging rollers"])
def _(S):
    return [shell(rr(S, 3, 4, 18, 9, 4)), detail(seg(3, 8.5, 21, 8.5)), shell(rr(S, 3, 13.5, 7, 3, 1)),
            shell(rr(S, 14, 13.5, 7, 3, 1)), dot(5, 19.7, 1.4), dot(8.5, 19.7, 1.4), dot(15.5, 19.7, 1.4), dot(19, 19.7, 1.4)]


@T("checkweigher", "Short conveyor with a box on a weighing section and a display on a post above",
   ["weigh conveyor", "inline scale", "weight check", "parcel scale", "dynamic scale", "weighing station", "scale conveyor"])
def _(S):
    return [shell(rr(S, 2, 16, 20, 4, 2)), dot(6, 18, 0.9), dot(18, 18, 0.9), shell(rr(S, 4, 9, 7, 7, 1)),
            line(seg(18, 8, 18, 16)), shell(rr(S, 13.5, 2.5, 8, 5.5, 1)), detail(seg(16, 5.25, 19, 5.25))]


@T("pocket-sorter", "Overhead rail with a row of hanging pouch bags, two of them holding small parcels",
   ["pouch sorter", "hanging sorter", "overhead sorter", "garment sorter", "parcel sorter", "e-commerce sorter", "bag sorter"])
def _(S):
    return [line(seg(2, 3, 22, 3)), line(seg(4.5, 3, 4.5, 6)), line(seg(12, 3, 12, 6)), line(seg(19.5, 3, 19.5, 6)),
            shell(rr(S, 2.25, 6, 4.5, 14, 1.5)), shell(rr(S, 9.75, 6, 4.5, 14, 1.5)), shell(rr(S, 17.25, 6, 4.5, 14, 1.5)),
            dp([(10.75, 12), (13.25, 12), (13.25, 14.5), (10.75, 14.5)]), dp([(18.25, 14), (20.75, 14), (20.75, 16.5), (18.25, 16.5)])]


@T("pick-path", "Top view of three shelf bars with a dotted route snaking down one aisle and up the next",
   ["picking route", "warehouse route", "pick route", "route optimisation", "aisle path", "walking path", "pick walk"])
def _(S):
    return [line(seg(3, 2.5, 3, 17.5)), line(seg(12, 2.5, 12, 17.5)), line(seg(21, 2.5, 21, 17.5)),
            dot(7.5, 4, 1.25), dot(7.5, 8, 1.25), dot(7.5, 12, 1.25), dot(7.5, 16, 1.25), dot(12, 20.5, 1.25),
            dot(16.5, 16, 1.25), dot(16.5, 12, 1.25), dot(16.5, 8, 1.25), dot(16.5, 4, 1.25)]


@T("inventory-drone", "Small quadcopter beside a tall pallet rack with scan lines reaching a box label",
   ["warehouse drone", "stock counting drone", "scanning drone", "cycle count", "uav inventory", "aerial inventory", "rfid drone"])
def _(S):
    return [shell(rr(S, 17, 2, 5, 20, 1)), detail(seg(17, 8.5, 22, 8.5)), detail(seg(17, 15.5, 22, 15.5)),
            shell(rr(S, 4, 8, 5, 3, 1)), line(seg(4, 8, 2.8, 6.3)), line(seg(9, 8, 10.2, 6.3)),
            line(seg(1, 5.5, 4.5, 5.5)), line(seg(8.5, 5.5, 12, 5.5)),
            line(seg(8, 12, 15, 10.5)), line(seg(8, 12, 15, 14.5)), dot(19.5, 12, 1)]


@T("pallet-label", "Tall label with a text line above three stacked barcodes of uneven bars",
   ["pallet tag", "sscc label", "shipping label", "pallet barcode", "license plate label", "logistics label", "gs1 label"])
def _(S):
    bars = []
    for y in (10.5, 14, 17.5):
        for x, w in ((7, 1.5), (9.5, 1), (11.5, 2), (14.5, 1), (16, 1)):
            bars.append(dp(box_pts(x, y, w, 2.5)))
    return [shell(rr(S, 4, 2, 16, 20, 4)), detail(seg(7, 5.5, 17, 5.5))] + bars


# =========================================================================== containers, lifting gear and handling marks


@T("open-side-container", "Shipping container with its long side opened on raised and lowered hinged panels, boxes inside",
   ["side opening container", "full side access", "open side", "side door container", "freight container", "sea box", "panel container"])
def _(S):
    return [shell(rr(S, 4, 7, 16, 10, 1)), detail(rect(6.5, 10, 4, 5)), detail(rect(12, 9, 5.5, 6)),
            line("M4 7L2.5 3.5H21.5L20 7"), line("M4 17L2.5 20.5H21.5L20 17")]


@T("shelf-ready-tray", "Cardboard tray with a zigzag torn front showing a row of tall cans standing inside",
   ["shelf ready packaging", "retail tray", "display tray", "srp", "tear off tray", "cans tray", "retail ready"])
def _(S):
    return [shell(poly([(2, 21), (2, 13), (4.5, 15), (7, 13), (9.5, 15), (12, 13), (14.5, 15), (17, 13), (19.5, 15), (22, 13), (22, 21)],
                       closed=True, r=S.r * 0.5)),
            shell(rr(S, 3.5, 2, 4.5, 11, 2)), shell(rr(S, 9.75, 2, 4.5, 11, 2)), shell(rr(S, 16, 2, 4.5, 11, 2)),
            detail(seg(3.5, 5.5, 8, 5.5)), detail(seg(9.75, 5.5, 14.25, 5.5)), detail(seg(16, 5.5, 20.5, 5.5))]


@T("vacuum-tube-lifter", "Flexible hose hanging from an overhead arm with a suction pad and handle holding a box",
   ["vacuum lifter", "tube lifter", "suction lifter", "lift assist", "vacuum hoist", "manipulator", "ergonomic lift"])
def _(S):
    return [line(seg(2, 3, 22, 3)), line("M12 3V5C9.5 6 14.5 7.5 12 9V10"), shell(rr(S, 8.5, 10, 7, 2.5, 1)),
            line("M16 11H20V7"), shell(rr(S, 6, 14.5, 12, 7, 1))]


@T("c-hook", "C shaped lifting hook on a crane cable with a steel coil sitting on its lower arm",
   ["coil hook", "coil lifter", "steel coil hook", "crane hook", "overhead crane", "coil handling", "c hook lifter"])
def _(S):
    return [line(seg(12, 2, 12, 6.5)), line(poly([(5, 6.5), (19, 6.5), (19, 21), (5, 21)], r=S.r)),
            shell(circle(11.5, 14, 4)), dp([(10.4, 12.9), (12.6, 12.9), (12.6, 15.1), (10.4, 15.1)])]


@T("lever-hoist", "Compact hoist with a long lever handle, a ring at the top and a chain running to a ring below",
   ["lever block", "ratchet hoist", "chain hoist", "come along", "manual hoist", "rigging hoist", "chain lever hoist"])
def _(S):
    return [shell(circle(12, 4.25, 2.25)), shell(rr(S, 7.5, 8, 9, 6, 3)), line(seg(16, 10, 22, 3.5)),
            line(seg(12, 14, 12, 17)), shell(circle(12, 19.75, 2.25))]


@T("moving-blanket", "Thick quilted pad with diamond stitching lying over the top of a dresser",
   ["furniture pad", "removal blanket", "packing blanket", "quilted pad", "moving pad", "furniture wrap", "padded cover"])
def _(S):
    return [shell(rr(S, 4, 14, 16, 8, 1)), shell(rr(S, 2, 2.5, 20, 13.5, 4)), detail(seg(11, 2.5, 2, 11.5)),
            detail(seg(19, 2.5, 5.5, 16)), detail(seg(5, 2.5, 18.5, 16)), detail(seg(13, 2.5, 22, 11.5))]


@T("miscellaneous-hazard-label", "Diamond placard with vertical stripes in its top half and the number nine below",
   ["class 9", "miscellaneous dangerous goods", "hazard class nine", "lithium class", "dangerous goods label", "hazmat 9", "adr class 9"])
def _(S):
    return [diamond(S), detail(seg(2, 12, 22, 12)), detail(seg(8, 6, 8, 11)), detail(seg(12, 3, 12, 11)),
            detail(seg(16, 6, 16, 11)), detail("M13.8 15.4a1.9 1.9 0 1 0-3.8 0 1.9 1.9 0 0 0 3.8 0c0 2-1 3-2.3 3.3")]


@T("keep-away-from-sunlight", "Box under a small sun whose rays fall toward it, the handling mark for protect from heat",
   ["protect from heat", "keep away from heat", "heat sensitive", "sun exposure", "handling mark", "shade only", "no direct sun"])
def _(S):
    rays = []
    for ang in (0, 45, 90, 135, 180):
        a = math.radians(ang)
        rays.append(line(seg(12 + 4.2 * math.cos(a), 5.5 + 4.2 * math.sin(a), 12 + 5.9 * math.cos(a), 5.5 + 5.9 * math.sin(a))))
    return [shell(circle(12, 5.5, 2.25)), *rays, shell(rr(S, 6, 14.5, 12, 7, 2))]


@T("temperature-limits", "Thermometer with two short limit bars marking an upper and a lower temperature",
   ["temperature range", "keep between", "min max temperature", "storage temperature", "cold chain limits", "handling mark", "thermal limits"])
def _(S):
    return [shell(union(rect(10.5, 2.5, 3, 14, 1.5), circle(12, 18.5, 3))), dot(12, 18.5, 1.25),
            line(seg(16, 6, 21, 6)), line(seg(16, 14, 21, 14))]


@T("phytosanitary-certificate", "Certificate sheet with a leaf at the top and a round inspection stamp below",
   ["plant health certificate", "export plants", "agricultural inspection", "quarantine certificate", "produce export", "leaf certificate", "ippc"])
def _(S):
    return [sheetp(S), detail("M8.5 11C7.5 7 10 5 15.5 5C15.5 9.5 13 11.5 8.5 11Z"), detail(seg(8, 12, 12.5, 8)),
            detail(circle(12, 16.3, 2.6))]


@T("neighbor-delivery", "Two small houses with a box riding a curved arrow from one to the other",
   ["neighbour delivery", "leave with neighbour", "safe place delivery", "next door", "delivery to neighbor", "alternate address", "redirect parcel"])
def _(S):
    return [shell(poly([(2, 21), (2, 15), (6, 12), (10, 15), (10, 21)], closed=True, r=S.r)),
            shell(poly([(14, 21), (14, 15), (18, 12), (22, 15), (22, 21)], closed=True, r=S.r)),
            line("M6 9.5C7 6 8.5 4.5 10 4.2"), line("M14 4.2C15.5 4.5 17 6 18 9.5"), line("M16 9L18 10.5L19.5 8"),
            shell(rr(S, 10, 2.5, 4, 4, 0.5))]


@T("white-glove-delivery", "Armchair carried by two gloved hands with cuffs at the bottom corners",
   ["premium delivery", "room of choice", "furniture delivery", "installation delivery", "carry in service", "luxury delivery", "gloved hands"])
def _(S):
    return [shell(rr(S, 8, 2, 8, 8, 3)), shell(rr(S, 4.5, 9, 15, 7, 3)), detail(seg(8, 10, 8, 16)),
            detail(seg(16, 10, 16, 16)), shell(rr(S, 2, 17.5, 7, 4, 2)), shell(rr(S, 15, 17.5, 7, 4, 2))]


@T("backorder", "Parcel box beside a small hourglass with sand running to the lower half",
   ["back order", "out of stock", "awaiting stock", "delayed shipment", "pending restock", "waiting for supply", "on order"])
def _(S):
    return [shell(rr(S, 2, 8, 10, 11, 1)), detail(seg(7, 8, 7, 12)),
            shell(poly([(15, 3), (22, 3), (22, 6), (19.5, 12), (22, 18), (22, 21), (15, 21), (15, 18), (17.5, 12), (15, 6)],
                       closed=True, r=S.r * 0.6)), dp([(16.8, 19), (20.2, 19), (18.5, 15.5)])]
