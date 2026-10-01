"""TypeIcon Core: business (batch 004).

Retail, trade, 2D codes, accounting, personal finance, insurance, law and property concepts drawn from the
objects themselves. Insurance icons reuse the batch 003 umbrella canopy (y 2.5 to 8.5) with the insured object
below it (y 11 to 21.5). Objects that sit in front of another are cut out of it with a 2 px gap (see `cut`).
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "business"


# ============================================================================ helpers

def rr(S, cap=None):
    """Container corner radius for the style, optionally capped for small shapes."""
    return S.R if cap is None else min(S.R, cap)


def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def cut(d, *keep, gap=2.0):
    """Closed shape d with the closed shapes in keep removed, leaving a stroke gap around them."""
    w = 2 * (gap + 2.0)
    region = U(*[U(P(k), ST(k, w, "round", "round")) for k in keep])
    return path_to_d(D(P(d), region))


def turn(d, deg, cx, cy):
    """Path d turned clockwise by deg about (cx, cy)."""
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rot(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def head(tip, deg, size=2.25):
    """Open arrowhead points at tip, pointing in direction deg (0 = right, 90 = down)."""
    a = polar(tip[0], tip[1], size * math.sqrt(2), deg + 180 - 45)
    b = polar(tip[0], tip[1], size * math.sqrt(2), deg + 180 + 45)
    return [a, tip, b]


def house(S, x0, x1, ytop, ybot, eave=None):
    """Pentagon house outline: walls x0..x1, roof peak at ytop, floor at ybot."""
    cx = (x0 + x1) / 2
    e = eave if eave is not None else ytop + (x1 - x0) / 2
    return poly([(x0, ybot), (x0, e), (cx, ytop), (x1, e), (x1, ybot)], closed=True, r=S.r * 0.6)


def bust(S, cx, cy, hr, bw, top, bottom=21.0):
    """Head circle and a rounded-top body shell of half width bw from y=top to bottom."""
    r = min(bw, bottom - top)
    body = (f"M{fmt(cx - bw)} {fmt(bottom)}V{fmt(top + r)}A{fmt(bw)} {fmt(r)} 0 0 1 {fmt(cx + bw)} {fmt(top + r)}"
            f"V{fmt(bottom)}Z")
    return [shell(circle(cx, cy, hr)), shell(body)]


def canopy_d():
    """Umbrella canopy with a domed top and three scallops along its lower edge (y 2.5 to 8.5)."""
    top = "M2.5 8.5A9.5 6 0 0 1 21.5 8.5"
    sc = "A3.17 1.9 0 0 0 15.17 8.5A3.17 1.9 0 0 0 8.83 8.5A3.17 1.9 0 0 0 2.5 8.5Z"
    return top + sc


def insured(S, *parts):
    return [shell(canopy_d(), stroke_miterlimit="8" if S.name == "line" else "4")] + list(parts)


# ============================================================================ retail and trade

@icon("planogram", CAT, "Shelf diagram with three rows of product blocks of different widths",
      tags=["shelf plan", "merchandising", "retail", "shelf layout", "product placement", "store"])
def _(S):
    k = L(S, 0, 0.75)
    return [
        shell(rect(3, 3, 18, 18, rr(S, 2.5))),
        detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15)),
        sq(6, 5, 5, 3, k), sq(13, 6, 3, 2, k),
        sq(6, 12, 2.5, 2, k), sq(10.5, 11, 7.5, 3, k),
        sq(6, 17, 7, 3, k), sq(15, 18, 3, 2, k),
    ]


def _bottle_top(cx, y0):
    """Closed outline of a bottle's shoulders and neck rising from the wrap at y0."""
    return poly([(cx - 3, y0), (cx - 3, 8.5), (cx - 1.25, 6.5), (cx - 1.25, 3), (cx + 1.25, 3), (cx + 1.25, 6.5),
                 (cx + 3, 8.5), (cx + 3, y0)], closed=True)


@icon("multipack", CAT, "Pack of bottles held together in shrink wrap",
      tags=["six pack", "bottle pack", "bundle", "bulk buy", "drinks", "shrink wrap", "retail"])
def _(S):
    return [
        shell(_bottle_top(7.5, 11)), shell(_bottle_top(16.5, 11)),
        shell(rect(3, 11, 18, 10, rr(S, 3))),
        detail(seg(3, 15.5, 21, 15.5)),
    ]


@icon("property-investment", CAT, "Small house sitting on top of a stack of coins",
      tags=["real estate investment", "property", "buy to let", "real estate", "house value", "investing"])
def _(S):
    k = L(S, 1, 2)
    body = union(house(S, 6.5, 17.5, 2.5, 13.5, eave=8), rect(3, 13, 15.5, 4.5, k), rect(5.5, 17, 15.5, 4.5, k))
    return [
        shell(body),
        detail(seg(6.5, 13, 17.5, 13)),
        detail(seg(5.5, 17.25, 18.5, 17.25)),
        detail(poly([(10.5, 13), (10.5, 9.5), (13.5, 9.5), (13.5, 13)], r=S.r * 0.4)),
    ]


@icon("mediation", CAT, "Two people facing each other with a smaller third person between them",
      tags=["mediator", "dispute resolution", "conflict", "negotiation", "arbitration", "third party"])
def _(S):
    return bust(S, 4.5, 6, 2.25, 2.5, 12) + bust(S, 19.5, 6, 2.25, 2.5, 12) + bust(S, 12, 11.5, 1.75, 2, 17)


@icon("royalty-payment", CAT, "Coin with a small crown floating above it",
      tags=["royalties", "licensing fee", "royalty", "income", "payment", "crown"])
def _(S):
    crown = poly([(7.5, 8), (7, 3), (9.75, 5.5), (12, 2.5), (14.25, 5.5), (17, 3), (16.5, 8)], closed=True, r=S.r * 0.4)
    return [
        shell(crown, stroke_miterlimit="3"),
        shell(circle(12, 16, 4.75)),
        dot(12, 16, 1.5),
    ]


def _flag_pole(S, sgn):
    """Flag on a pole, designed upright and leaned outward by 16 degrees about the crossing point."""
    x = 12.0
    flag = poly([(x, 3), (x - sgn * 6.5, 3), (x - sgn * 6.5, 8.5), (x, 8.5)], closed=True, r=S.r * 0.4)
    parts = [
        shell(turn(flag, -16 * sgn, 12, 18)),
        line(poly(rot([(x, 8.5), (x, 21.5)], -16 * sgn, 12, 18))),
    ]
    return parts


@icon("crossed-flags", CAT, "Two blank flags on poles crossed near their bases",
      tags=["flags", "diplomacy", "partnership", "alliance", "international", "trade agreement"])
def _(S):
    return _flag_pole(S, 1) + _flag_pole(S, -1)


@icon("trade-embargo", CAT, "Shipping container with a heavy chain across its doors",
      tags=["embargo", "sanctions", "trade ban", "blocked shipment", "import ban", "export ban"])
def _(S):
    parts = [shell(rect(2.5, 3, 19, 18, rr(S, 2.5)))]
    for x in (7, 12, 17):
        parts += [detail(seg(x, 3, x, 6.75)), detail(seg(x, 17.25, x, 21))]
    for cx in (5.5, 12, 18.5):
        parts.append(detail(ellipse(cx, 12, 2.5, 2.25)))
    parts += [detail(seg(7, 12, 10.5, 12)), detail(seg(13.5, 12, 17, 12))]
    return parts


@icon("wheelbarrow-of-cash", CAT, "Wheelbarrow heaped high with bundles of banknotes",
      tags=["lots of money", "cash", "wealth", "windfall", "money pile", "rich"])
def _(S):
    load = union(
        poly([(2.5, 12), (17.5, 12), (15, 17), (5.5, 17)], closed=True),
        rect(3.5, 8, 13, 4.5), rect(6.5, 4, 7, 4.5),
    )
    if S.name == "rounded":
        load = union(
            poly([(2.5, 12), (17.5, 12), (15, 17), (5.5, 17)], closed=True, r=1.5),
            rect(3.5, 8, 13, 4.5, 1.5), rect(6.5, 4, 7, 4.5, 1.5),
        )
    return [
        shell(load),
        detail(seg(2.5, 12, 17.5, 12)),
        detail(seg(6.5, 8, 13.5, 8)),
        detail(seg(10, 4, 10, 12)),
        line(seg(16, 14.5, 21.5, 12.5) if S.name == "line" else seg(16.5, 14.5, 21, 13)),
        line(seg(14, 17, 15, 21.5)),
        shell(circle(6.5, 20, 1.75)),
    ]


# ============================================================================ 2D codes

_DM = [  # 6 x 6 data matrix, 3 px modules; row 0 is the top
    "X.X.X.",
    "XX.XXX",
    "X.X...",
    "XXX.XX",
    "X..X..",
    "XXXXXX",
]


def _dm_cells():
    cells = []
    for j, row in enumerate(_DM):
        for i, c in enumerate(row):
            if c == "X" and i > 0 and j < 5:
                cells.append((3 + 3 * i, 3 + 3 * j))
    return cells


def _dm_filled():
    parts = [P(rect(x - 0.25, y - 0.25, 3.5, 3.5)) for x, y in _dm_cells()]
    parts.append(P(rect(2.75, 2.75, 3.5, 18.5)))
    parts.append(P(rect(2.75, 17.75, 18.5, 3.5)))
    return U(*parts)


@icon("data-matrix", CAT, "Square 2D code with a solid L shaped border and blocks inside",
      tags=["2d barcode", "datamatrix", "matrix code", "scan", "label", "product code"], filled=_dm_filled)
def _(S):
    k = L(S, 0, 1)
    ell = poly([(3, 3), (6, 3), (6, 18), (21, 18), (21, 21), (3, 21)], closed=True, r=L(S, 0, 1))
    return [solid(ell)] + [sq(x, y, 3, 3, k) for x, y in _dm_cells()]


@icon("aztec-barcode", CAT, "Square 2D code with a nested square bullseye at its center",
      tags=["aztec code", "2d barcode", "ticket code", "boarding pass", "scan", "matrix code"])
def _(S):
    k = L(S, 0, 0.75)
    return [
        shell(rect(7.5, 7.5, 9, 9, rr(S, 1.5))),
        sq(10.75, 10.75, 2.5, 2.5, k),
        sq(3, 3, 6, 2.5, k), sq(11, 3, 2.5, 2.5, k), sq(15.5, 3, 5.5, 2.5, k),
        sq(18.5, 7.5, 2.5, 6, k), sq(18.5, 16, 2.5, 5, k),
        sq(3, 18.5, 2.5, 2.5, k), sq(7.5, 18.5, 8.5, 2.5, k),
        sq(3, 9, 2.5, 7, k),
    ]


_PDF_ROWS = [
    [(8, 3), (13, 2), (17, 1.5)],
    [(8, 1.5), (11.5, 4), (17.5, 1)],
    [(8, 4), (14, 1.5), (17.5, 1)],
]


def _pdf_rects(grow=0.0):
    out = [(2 - grow, 5 - grow, 3 + 2 * grow, 14 + 2 * grow), (19.5 - grow, 5 - grow, 2.5 + 2 * grow, 14 + 2 * grow)]
    for j, row in enumerate(_PDF_ROWS):
        y = 5 + j * 5
        for x, w in row:
            out.append((x - 0.5 - grow, y - grow, w + 0.5 + 2 * grow, 4 + 2 * grow))
    return out


def _pdf_filled():
    return U(*(P(rect(*r)) for r in _pdf_rects(0.35)))


@icon("pdf417-barcode", CAT, "Wide stacked barcode made of rows of short bars with thick start and stop bars",
      tags=["pdf417", "stacked barcode", "2d barcode", "driver license code", "id barcode", "scan"], filled=_pdf_filled)
def _(S):
    k = L(S, 0, 1)
    return [sq(x, y, w, h, min(k, w / 2)) for x, y, w, h in _pdf_rects()]


def _maxi_dots():
    pts = []
    step = 4.0
    dy = step * math.sqrt(3) / 2
    for j in range(6):
        y = 3.5 + j * dy
        off = 0 if j % 2 == 0 else step / 2
        for i in range(6):
            x = 3.5 + off + i * step
            if x > 21 or y > 21:
                continue
            if math.hypot(x - 12, y - 12) < 7.75:
                continue
            pts.append((x, y))
    return pts


@icon("maxicode", CAT, "Square field of small hexagon dots with a bullseye of rings at its center",
      tags=["maxicode", "2d barcode", "shipping label", "parcel code", "bullseye code", "scan"])
def _(S):
    parts = [shell(circle(12, 12, 3.75)), dot(12, 12, 1.25)]
    for x, y in _maxi_dots():
        if S.name == "line":
            parts.append(Part("dot", poly(regular(x, y, 1.35, 6), closed=True)))
        else:
            parts.append(dot(x, y, 1.15))
    return parts


# ============================================================================ planning and investing

@icon("business-plan", CAT, "Binder with a light bulb and a small bar chart on its cover",
      tags=["business plan", "strategy", "startup", "proposal", "plan", "report"])
def _(S):
    return [
        shell(rect(3.5, 2, 17, 20, rr(S, 2.5))),
        detail(seg(7.5, 2, 7.5, 22)),
        detail("M12.5 11V9.9A3 3 0 1 1 16.5 9.9V11"),
        detail(seg(12.75, 13.5, 16.25, 13.5)),
        detail(seg(11.5, 22, 11.5, 19)), detail(seg(14.5, 22, 14.5, 17)), detail(seg(17.5, 22, 17.5, 18)),
    ]


@icon("index-fund", CAT, "Basket holding three bars of a bar chart",
      tags=["index fund", "etf", "diversification", "basket of stocks", "investing", "portfolio"])
def _(S):
    body = poly([(2.5, 11), (21.5, 11), (21.5, 14.5), (20, 14.5), (18.5, 21), (5.5, 21), (4, 14.5), (2.5, 14.5)],
                closed=True, r=S.r * 0.5)
    return [
        shell(body),
        detail(seg(4, 14.5, 20, 14.5)),
        detail(seg(8.5, 14.5, 8.5, 21)), detail(seg(12, 14.5, 12, 21)), detail(seg(15.5, 14.5, 15.5, 21)),
        line(seg(7.5, 10, 7.5, 6)), line(seg(12, 10, 12, 3)), line(seg(16.5, 10, 16.5, 7.5)),
    ]


# ============================================================================ accounting and budgeting

def _slip(S, x0, x1, ytop, deg):
    """Receipt slip: open outline with a torn zigzag top, standing on the box rim (y 14); turned clockwise by deg."""
    step = (x1 - x0) / 2
    pts = [(x0, 14.5), (x0, ytop)]
    for i in range(2):
        pts += [(x0 + step * (i + 0.5), ytop - 1.75), (x0 + step * (i + 1), ytop)]
    pts.append((x1, 14.5))
    cx = (x0 + x1) / 2
    body = poly(rot(pts, deg, cx, 14.5), r=S.r * 0.3)
    txt = seg(*rot([(x0 + 1.6, ytop + 4), (x1 - 1.6, ytop + 4)], deg, cx, 14.5)[0],
              *rot([(x0 + 1.6, ytop + 4), (x1 - 1.6, ytop + 4)], deg, cx, 14.5)[1])
    return body, txt


@icon("shoebox-of-receipts", CAT, "Open shoebox stuffed with paper receipts sticking out of the top",
      tags=["receipts", "tax records", "paperwork", "expenses", "bookkeeping", "record keeping"])
def _(S):
    a, ta = _slip(S, 4, 10, 5, -6)
    b, tb = _slip(S, 14, 20, 3.5, 6)
    return [
        line(a, stroke_miterlimit="3"), line(ta),
        line(b, stroke_miterlimit="3"), line(tb),
        shell(rect(2.5, 14, 19, 7.5, rr(S, 2.5))),
    ]


@icon("account-reconciliation", CAT, "Two columns of rows with straight lines linking the matching rows",
      tags=["reconcile", "bank reconciliation", "matching", "bookkeeping", "accounting", "balance check"])
def _(S):
    k = L(S, 0.5, 2)
    parts = []
    for y in (3, 10, 17):
        parts += [shell(rect(2.5, y, 6, 4, k)), shell(rect(15.5, y, 6, 4, k))]
    parts += [line(seg(8.5, 5, 15.5, 12)), line(seg(8.5, 12, 15.5, 5)), line(seg(8.5, 19, 15.5, 19))]
    return parts


def car_side(S, cx, cy, k=1.0):
    """Side view car about 10 x 5.5 centred on (cx, cy), facing right."""
    body = [(-5, 1.5), (-5, -1), (-3.25, -1.5), (-2, -4.5), (1.5, -4.5), (2.75, -1.5), (5, -0.75), (5, 1.5)]
    pts = [(cx + x * k, cy + y * k) for x, y in body]
    return [shell(poly(pts, closed=True, r=S.r * 0.5)), dot(cx - 2.5 * k, cy + 1.75 * k, 1.5 * k),
            dot(cx + 2.5 * k, cy + 1.75 * k, 1.5 * k)]


@icon("depreciation", CAT, "Small car below a line that steps down from left to right",
      tags=["depreciation", "loss of value", "asset value", "write down", "declining value", "car value"])
def _(S):
    steps = [(3, 3.5), (9.5, 3.5), (9.5, 8), (15.5, 8), (15.5, 12.5), (20.5, 12.5), (20.5, 21)]
    return [
        line(poly(steps, r=S.r * 0.6)),
        line(poly(head((20.5, 21), 90, 2), r=S.r * 0.5)),
        *car_side(S, 8, 18, 1.0),
    ]


def _note_half(S, x0, deg, px):
    return shell(turn(rect(x0, 14.5, 9.5, 6.5, rr(S, 1.5)), deg, px, 17.75))


@icon("budget-cut", CAT, "Open scissors cutting a banknote into two halves",
      tags=["budget cut", "cost cutting", "spending cut", "austerity", "reduce costs", "savings"])
def _(S):
    return [
        shell(circle(8, 4.5, 2.25)), shell(circle(16, 4.5, 2.25)),
        line(poly([(9.75, 6.25), (12, 8.75), (14, 12)], r=S.r * 0.5)),
        line(poly([(14.25, 6.25), (12, 8.75), (10, 12)], r=S.r * 0.5)),
        _note_half(S, 1.5, -12, 11), _note_half(S, 13, 12, 13),
        dot(5.5, 17.25, 1.25), dot(18.5, 17.25, 1.25),
    ]


@icon("damaged-parcel", CAT, "Cardboard box with a dented lid and a crushed, torn corner at the lower right",
      tags=["damaged package", "broken parcel", "delivery damage", "shipping claim", "crushed box", "returns"])
def _(S):
    body = poly([(3, 4.5), (21, 4.5), (21, 12.5), (17, 14), (19.5, 16.5), (15.5, 18), (17, 21.5), (3, 21.5)],
                closed=True, r=S.r * 0.4)
    return [
        shell(body, stroke_miterlimit="4"),
        detail(seg(3, 9.5, 14.5, 9.5)),
        detail(seg(9, 4.5, 9, 9.5)),
    ]


@icon("store-layout", CAT, "Top down shop floor plan with rows of aisle shelves and a checkout counter by the door",
      tags=["floor plan", "shop layout", "store map", "aisles", "retail design", "checkout"])
def _(S):
    walls = poly([(9.5, 21), (3, 21), (3, 3), (21, 3), (21, 21), (15, 21)], r=S.r)
    parts = [line(walls)]
    for x in (7, 12, 17):
        parts.append(line(seg(x, 6.5, x, 13) if S.name == "line" else seg(x, 7, x, 12.5)))
    parts.append(line(poly([(6.5, 16.5), (10, 16.5), (10, 18.5)], r=S.r * 0.5)))
    return parts


# ============================================================================ insurance

@icon("earthquake-insurance", CAT, "House above a jagged crack in the ground under an open umbrella",
      tags=["earthquake cover", "quake insurance", "seismic", "natural disaster", "home insurance", "tremor"])
def _(S):
    ground = [(2.5, 20), (9, 20), (10.5, 22), (12, 19.5), (13.5, 22), (15, 20), (21.5, 20)]
    return insured(S, shell(house(S, 7, 17, 11.5, 17, eave=13.5)),
                   line(poly(ground, r=S.r * 0.3), stroke_miterlimit="3"))


@icon("cyber-insurance", CAT, "Laptop with a keyhole on its screen under an open umbrella",
      tags=["cyber cover", "data breach insurance", "cyber security", "hacking", "online risk", "policy"])
def _(S):
    return insured(
        S,
        shell(rect(5.5, 11.5, 13, 7.5, rr(S, 1.5))),
        line(seg(3, 21, 21, 21) if S.name == "line" else seg(3.5, 21, 20.5, 21)),
        dot(12, 14.25, 1.25),
        Part("dot", poly([(11.3, 14.5), (12.7, 14.5), (13.1, 17), (10.9, 17)], closed=True)),
    )


def wave(x0, x1, y, amp=0.6, n=5):
    step = (x1 - x0) / n
    d = f"M{fmt(x0)} {fmt(y)}"
    for i in range(n):
        xa = x0 + i * step
        sgn = -1 if i % 2 == 0 else 1
        d += f"Q{fmt(xa + step / 2)} {fmt(y + sgn * amp * 2)} {fmt(xa + step)} {fmt(y)}"
    return d


@icon("marine-insurance", CAT, "Cargo ship on waves under an open umbrella",
      tags=["cargo insurance", "shipping insurance", "marine cover", "freight", "hull insurance", "ocean"])
def _(S):
    ship = union(poly([(3, 14.5), (21, 14.5), (18.5, 18), (5.5, 18)], closed=True, r=S.r * 0.5),
                 rect(7, 11.5, 10, 3.5, L(S, 0, 1)))
    return insured(S, shell(ship), detail(seg(12, 11.5, 12, 14.5)), line(wave(3, 21, 20.75, 0.5, 5)))


# ============================================================================ law and documents

@icon("nda-document", CAT, "Document with two lines of text above a zipper pulled shut across the page",
      tags=["non disclosure agreement", "nda", "confidentiality", "secret", "contract", "privacy"])
def _(S):
    return [
        shell(rect(4, 2, 16, 20, rr(S, 2.5))),
        detail(seg(8, 6.5, 16, 6.5)), detail(seg(8, 10, 13, 10)),
        detail(seg(4, 16, 13.5, 16)),
        detail(seg(7.5, 14, 7.5, 18)), detail(seg(10, 14, 10, 18)),
        detail(rect(13.5, 14.25, 4, 3.5, L(S, 0, 1.25))),
    ]


@icon("voter-id-card", CAT, "ID card with a portrait on the left and a tick mark over a line on the right",
      tags=["voter card", "voter registration", "election id", "polling card", "identity", "ballot"])
def _(S):
    return [
        shell(rect(2, 4, 20, 16, rr(S, 2.5))),
        detail(circle(8, 9.5, 1.75)),
        detail("M5 16.5A3 3 0 0 1 11 16.5"),
        detail(poly([(13.75, 10.5), (15.75, 12.5), (19.25, 8.5)], r=S.r * 0.5)),
        detail(seg(14, 16.5, 19.5, 16.5)),
    ]


# ============================================================================ banking and personal finance

@icon("open-banking", CAT, "Bank building and a smartphone joined by a connecting link",
      tags=["open banking", "bank api", "connected accounts", "fintech", "account linking", "mobile banking"])
def _(S):
    return [
        shell(poly([(2, 8.5), (6, 3.5), (10, 8.5)], closed=True, r=S.r * 0.4), stroke_miterlimit="3"),
        line(seg(3.75, 11, 3.75, 16)), line(seg(8.25, 11, 8.25, 16)),
        line(seg(2, 19, 10, 19)),
        line(seg(10, 13.5, 15.5, 13.5)),
        shell(rect(15.5, 3, 6.5, 14, rr(S, 2))),
        detail(seg(17.75, 14, 19.75, 14)),
    ]


@icon("joint-account", CAT, "Two people side by side above one shared payment card",
      tags=["joint account", "shared account", "couple finances", "shared card", "partners", "household money"])
def _(S):
    return [
        *bust(S, 7, 4.25, 2, 3.5, 7.5, 10),
        *bust(S, 17, 4.25, 2, 3.5, 7.5, 10),
        shell(rect(3, 13.5, 18, 8, rr(S, 2.5))),
        detail(seg(3, 17, 21, 17)),
        sq(6, 19, 4, 1.5),
    ]


@icon("debt-consolidation", CAT, "Three small coins with lines converging into one large coin",
      tags=["debt consolidation", "combine loans", "merge debts", "single payment", "refinance", "loan"])
def _(S):
    return [
        shell(circle(4.25, 4.5, 2)), shell(circle(4.25, 12, 2)), shell(circle(4.25, 19.5, 2)),
        line(seg(7, 5.5, 10, 11)), line(seg(7.25, 12, 10, 12)), line(seg(7, 18.5, 10, 13)),
        line(poly(head((11, 12), 0, 1.75), r=S.r * 0.5)),
        shell(circle(17.5, 12, 4.25)),
        dot(17.5, 12, 1.5),
    ]


def _pie(S, cx, cy):
    r = 3.5
    return [shell(circle(cx, cy, r)), detail(poly([(cx, cy - r), (cx, cy), (cx + r, cy)], r=0))]


@icon("portfolio-rebalancing", CAT, "Level balance beam with a small pie chart hanging from each end",
      tags=["rebalancing", "asset allocation", "portfolio", "balance", "diversification", "investing"])
def _(S):
    return [
        dot(12, 3.5, 1.5),
        line(seg(12, 5, 12, 19)),
        line(seg(3.5, 6.5, 20.5, 6.5) if S.name == "line" else seg(4, 6.5, 20, 6.5)),
        line(seg(5.5, 6.5, 5.5, 9)), line(seg(18.5, 6.5, 18.5, 9)),
        *_pie(S, 5.5, 13), *_pie(S, 18.5, 13),
        shell("M7.5 21.5A4.5 3 0 0 1 16.5 21.5Z" if S.name == "rounded" else "M7.5 21.5L9 19H15L16.5 21.5Z"),
    ]


@icon("passive-income", CAT, "Coin resting in a hammock slung between two posts",
      tags=["passive income", "earn while you sleep", "dividends", "residual income", "relax", "money"])
def _(S):
    net = "M3 9C7 21 17 21 21 9C17 14 7 14 3 9Z"
    coin = circle(12, 8.75, 3.75)
    return [
        line(seg(3, 3, 3, 21.5)), line(seg(21, 3, 21, 21.5)),
        shell(cut(net, coin), stroke_miterlimit="8" if S.name == "line" else "4"),
        shell(coin),
        dot(12, 8.75, 1.25),
    ]


@icon("deflation", CAT, "Party balloon on a short string with a long arrow pointing down beside it",
      tags=["deflation", "falling prices", "price drop", "economy", "cheaper", "prices"])
def _(S):
    body = "M8.5 3C5.25 3 3 5.5 3 8.75C3 12 5.5 14 8.5 14C11.5 14 14 12 14 8.75C14 5.5 11.75 3 8.5 3Z"
    knot = poly([(7, 16.25), (10, 16.25), (8.5, 14.25)], closed=True, r=L(S, 0, 0.6))
    return [
        shell(body),
        solid(knot),
        line("M8.5 16.25C7 17.5 10 19 8.5 21"),
        detail("M6 7.5C7 6.5 7.75 6.25 8.75 6.25"),
        line(seg(19, 4, 19, 19.5)),
        line(poly(head((19, 21), 90, 2.25), r=S.r * 0.5)),
    ]


# ============================================================================ property

@icon("house-hunting", CAT, "Small house above a pair of binoculars",
      tags=["house hunting", "home search", "property search", "looking for a home", "real estate", "moving"])
def _(S):
    k = rr(S, 2)

    def barrel(x0):
        return union(rect(x0, 17, 8, 4.5, k), rect(x0 + 1.5, 13.5, 5, 4.5, L(S, 0, 1)))
    return [
        shell(house(S, 7, 17, 2.5, 10, eave=6.25)),
        shell(barrel(2.5)), shell(barrel(13.5)),
        line(seg(10.5, 16, 13.5, 16)),
    ]


@icon("house-swap", CAT, "Two small houses with two curved arrows swapping them",
      tags=["home exchange", "house exchange", "swap homes", "holiday swap", "home swap", "trade places"])
def _(S):
    return [
        shell(house(S, 2.5, 11, 2.5, 11, eave=6.5)),
        shell(house(S, 13, 21.5, 13, 21.5, eave=17)),
        line("M14 4.5H16A3 3 0 0 1 19 7.5V9.5"),
        line(poly(head((19, 10.5), 90, 2), r=S.r * 0.5)),
        line("M10 19.5H8A3 3 0 0 1 5 16.5V14.5"),
        line(poly(head((5, 13.5), -90, 2), r=S.r * 0.5)),
    ]


@icon("room-rental", CAT, "House outline with a single bed drawn inside it",
      tags=["room to rent", "room rental", "lodging", "spare room", "house share", "bed and board"])
def _(S):
    return [
        shell(house(S, 3, 21, 2.5, 21.5, eave=10)),
        detail(seg(7, 12.5, 7, 18.5)),
        detail(poly([(7, 16), (17, 16), (17, 18.5)], r=S.r * 0.5)),
        detail(seg(10, 13.5, 13, 13.5)),
    ]


@icon("check-bounce", CAT, "Paper check with a U-turn arrow above it bouncing it back",
      tags=["bounced check", "bounced cheque", "returned check", "insufficient funds", "nsf", "rejected payment"])
def _(S):
    return [
        shell(rect(2.5, 11, 19, 10.5, rr(S, 3))),
        detail(seg(6, 14.5, 11, 14.5)), detail(seg(14, 14.5, 18, 14.5)),
        detail(seg(6, 18, 13, 18)),
        line("M17.5 8.5V6.5A3.5 3.5 0 0 0 14 3H7.5"),
        line(poly(head((6.5, 3), 180, 2), r=S.r * 0.5)),
    ]


# ============================================================================ additions

@icon("bond-ladder", CAT, "Ladder whose three rungs are flat coins seen edge on",
      tags=["bond ladder", "laddered bonds", "maturities", "fixed income", "investing", "staggered savings"])
def _(S):
    parts = [line(seg(4.5, 2.5, 4.5, 21.5)), line(seg(19.5, 2.5, 19.5, 21.5))]
    for y in (5.5, 12, 18.5):
        parts += [line(seg(4.5, y, 7.5, y)), line(seg(16.5, y, 19.5, y)),
                  shell(rect(7.5, y - 2.25, 9, 4.5, 2.25))]
    return parts


@icon("drachma-sign", CAT, "Drachma sign: a capital D joined to a small raised lowercase r",
      tags=["grd", "greece", "greek currency", "drachma", "old currency", "money"], modifiers="none")
def _(S):
    d = ("M4 6H8A5.5 7 0 0 1 8 20H4Z" if S.name == "line" else
         "M4 8Q4 6 6 6H8A5.5 7 0 0 1 8 20H6Q4 20 4 18Z")
    return [
        shell(d),
        line(seg(17.25, 4.5, 17.25, 11) if S.name == "line" else seg(17.25, 5, 17.25, 10.5)),
        line("M17.25 8.25C17.25 6.5 18.5 5.25 21 5.25"),
    ]


@icon("rial-sign", CAT, "Rial sign: a flowing script glyph with two tall strokes at the right and a long tail to the left",
      tags=["irr", "omr", "yer", "qar", "iran", "oman", "currency", "money"], modifiers="none")
def _(S):
    return [
        line(seg(20, 4.5, 20, 14.5)), line(seg(16, 4.5, 16, 14.5)),
        line("M20 14.5C20 16 19 17 17 17H11C8 17 6 18 4.5 20.5"),
        line("M14 14.5C12 14.5 10 15 8 15.5"),
        dot(11.5, 20.5, 1.1),
    ]


@icon("cease-and-desist", CAT, "Document with lines of text and a stop sign overlapping its lower corner",
      tags=["legal notice", "stop order", "demand letter", "lawsuit", "warning letter", "legal document"])
def _(S):
    stop = poly(regular(16.25, 16.25, 6, 8, start=-90 + 22.5), closed=True, r=S.r * 0.4)
    doc = rect(2.5, 2.5, 14.5, 19, rr(S, 2.5))
    return [
        shell(cut(doc, stop)),
        detail(seg(6.5, 7, 13, 7)), detail(seg(6.5, 11, 10.5, 11)),
        shell(stop),
        detail(seg(13.25, 16.25, 19.25, 16.25)),
    ]


@icon("debt-free", CAT, "Coin above a chain whose two halves have come apart",
      tags=["debt free", "no debt", "paid off", "broken chain", "freedom", "loan repaid"])
def _(S):
    return [
        shell(circle(12, 6.25, 4)),
        dot(12, 6.25, 1.5),
        line("M9.5 14.75H6.5A3 3 0 0 0 6.5 20.75H9.5"),
        line("M14.5 14.75H17.5A3 3 0 0 1 17.5 20.75H14.5"),
    ]
