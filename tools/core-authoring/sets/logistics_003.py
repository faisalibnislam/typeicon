"""TypeIcon Core: logistics (batch 003, packaging, stock, rail and handling equipment).

Visual language:
  * Side-view freight vehicles face right and follow sets/vehicles_001.py: wheels are rings on y 18, the body
    outline is left open where a wheel crosses it (`body`), and in Filled the body is cut 1 px clear of solid
    wheels (`veh`).
  * Shipping containers are plain boxes with vertical corrugation details spaced 4 px apart, so the ribs stay
    readable in Filled.
  * Equipment and packaging are drawn as shells with `detail` lines; nothing is thinner than 2 px.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    rect, regular, seg, shell, solid,
)
from geometry import polar as pt_on, rotation, transform_path

CAT = "logistics"
FILL = Style("filled", "butt", "miter", R=2.0, r=0.0)  # pseudo-style: Line geometry for Filled designs


# --------------------------------------------------------------------------- helpers

def L(S, a, b):
    """Pick a value for Line/Filled (a) or Rounded (b)."""
    return b if S.name == "rounded" else a


def isF(S):
    return S.name == "filled"


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def rpt(p, deg, c=(12.0, 12.0)):
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a)


def rr(S, x, y, w, h, cap=2.0):
    """Rectangle with the style's container radius, capped for small shapes."""
    return rect(x, y, w, h, min(S.R, cap))


def rb(S, x, y, w, h):
    """Small container: square corners in Line, softly rounded in Rounded."""
    return rect(x, y, w, h, L(S, 0, 1.2))


def T(name, description, tags, aliases=()):
    """Register an icon whose Filled design is derived from its Line geometry."""
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases)(fn)
    return deco


def wheel(x, y=18.0, r=2.0):
    """Side-view wheel: a ring in Line/Rounded; a solid disc cut 1 px clear of the body in Filled."""
    p = shell(circle(x, y, r))
    p.wheel = (x, y, r)
    return p


def hub(x, y, r=1.0):
    p = dot(x, y, r)
    p.knock = True
    return p


def body(S, pts, ws, yb=None, r=None):
    """Side-view body. `pts` run clockwise from the bottom-left corner over the top to the bottom-right corner
    (both on y = yb); the bottom edge is left open where a wheel crosses it."""
    yb = ws[0][1] if yb is None else yb
    rr_ = S.r if r is None else r
    if isF(S):
        return [shell(poly(pts, closed=True))]
    gaps = []
    for x, y, wr in ws:
        dy = yb - y
        if abs(dy) < wr:
            h = math.sqrt(wr * wr - dy * dy)
            gaps.append((x - h, x + h))
    gaps.sort()
    if not gaps:
        return [shell(poly(pts, closed=True, r=rr_))]
    lo = min(gaps[0][0], pts[0][0])
    hi = max(gaps[-1][1], pts[-1][0])
    full = [(lo, yb)] + list(pts) + [(hi, yb)]
    dedup = [full[0]]
    for q in full[1:]:
        if abs(q[0] - dedup[-1][0]) > 1e-6 or abs(q[1] - dedup[-1][1]) > 1e-6:
            dedup.append(q)
    out = [shell(poly(dedup, r=rr_))]
    for a, b in zip(gaps, gaps[1:]):
        if b[0] - a[1] > 0.5:
            out.append(line(seg(a[1], yb, b[0], yb)))
    return out


def auto(S, pts, ws, *extra, yb=None, r=None):
    return body(S, pts, ws, yb, r) + [wheel(*w) for w in ws] + list(extra)


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
    """Register a wheeled vehicle whose Filled design cuts the wheels clear of the body."""
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=veh_filled(fn))(fn)
    return deco


def ribs(xs, y1, y2):
    """Vertical corrugation lines."""
    return [detail(seg(x, y1, x, y2)) for x in xs]


# =========================================================================== stock, packaging and labels

@T("reorder-point", "Falling stock level line above a dashed threshold with a solid marker where they meet",
   ["reorder level", "minimum stock", "replenishment", "inventory threshold", "low stock", "restock trigger"])
def _(S):
    return [line(poly([(3, 3), (3, 21), (21, 21)], r=S.r)),
            line(seg(6, 5, 19, 18)), solid(rect(12, 11, 4, 4)),
            line(seg(6, 13, 9, 13)), line(seg(18, 13, 21, 13))]


@T("dead-stock", "Box on a shelf with a cobweb stretched across the corner above it",
   ["obsolete inventory", "unsold stock", "slow moving", "idle inventory", "dusty box", "write-off"])
def _(S):
    return [line(seg(3, 3, 3, 11)), line(seg(3, 3, 11, 3)), line(seg(3, 3, 9, 9)), line(arc(3, 3, 5.5, 0, 90)),
            shell(rb(S, 10, 12, 12, 8)), detail(seg(10, 16, 22, 16)),
            line(seg(2, 21.5, 22, 21.5))]


@T("mailroom", "Wall of pigeonhole cubbies holding letters and parcels above a counter",
   ["post room", "mail sorting", "pigeonholes", "mail cubbies", "parcel room", "internal mail"])
def _(S):
    return [shell(rb(S, 2, 2, 20, 12)), detail(seg(8.7, 2, 8.7, 14)), detail(seg(15.3, 2, 15.3, 14)),
            detail(seg(2, 8, 22, 8)),
            shell(rb(S, 2, 17, 20, 4))]


@T("packaging-hierarchy", "Single small box, a larger case and a tall pallet stack in a row of growing size",
   ["packaging levels", "unit case pallet", "each inner carton", "pack hierarchy", "case pack", "pallet load"])
def _(S):
    return [shell(rb(S, 2, 16, 4, 5)),
            shell(rb(S, 8.5, 11, 5, 10)), detail(seg(8.5, 15, 13.5, 15)),
            shell(rb(S, 17, 3, 5, 18)), detail(seg(17, 9, 22, 9)), detail(seg(17, 15, 22, 15))]


@T("lead-time", "Two vertical ticks joined by a double-headed arrow with a parcel box above the span",
   ["turnaround time", "delivery time", "order to delivery", "waiting time", "duration", "supply delay"])
def _(S):
    return [shell(rb(S, 8, 3, 8, 8)), detail(seg(12, 3, 12, 7)),
            line(seg(3, 14, 3, 20)), line(seg(21, 14, 21, 20)), line(seg(3, 17, 21, 17)),
            line(poly([(6, 14.5), (3.5, 17), (6, 19.5)], r=S.r)), line(poly([(18, 14.5), (20.5, 17), (18, 19.5)], r=S.r))]


@T("box-sizes", "Row of three boxes growing from small to large with a ruler line beneath",
   ["carton sizes", "small medium large", "packaging sizes", "box dimensions", "size chart", "shipping box sizes"])
def _(S):
    return [shell(rb(S, 2, 12, 4, 5)), shell(rb(S, 8.5, 8, 5, 9)), shell(rb(S, 17, 3, 5, 14)),
            line(seg(2, 21, 22, 21)), line(seg(2, 19.5, 2, 22.5)), line(seg(22, 19.5, 22, 22.5))]


@veh("axle-load", "Side view of a truck with arrows pressing down on its axles",
     ["axle weight", "load limit", "weighbridge", "overweight", "gross weight", "truck weight", "road load"])
def _(S):
    ws = [(5, 18, 1.5), (10, 18, 1.5), (19, 18, 1.5)]
    pts = [(2, 16), (2, 10), (14, 10), (14, 12), (18, 12), (22, 15), (22, 16)]
    arrows = []
    for x in (5, 10, 19):
        arrows += [line(seg(x, 2, x, 6.5)), line(poly([(x - 2, 4.5), (x, 7), (x + 2, 4.5)], r=S.r))]
    return auto(S, pts, ws, *arrows, yb=16)


@T("cotton-bale", "Square bale with slightly bulging sides bound by horizontal wire bands",
   ["cotton", "baled fibre", "textile raw material", "fiber bale", "wool bale", "compressed bale", "hay bale"])
def _(S):
    return [shell("M6 4H18Q18.6 12 18 20H6Q5.4 12 6 4Z"),
            line(seg(3.5, 8, 20.5, 8)), line(seg(3.5, 12, 20.5, 12)), line(seg(3.5, 16, 20.5, 16))]


SPIRAL = [(12.0, 8.3), (12.23, 8.22), (12.49, 8.19), (12.77, 8.22), (13.05, 8.31), (13.33, 8.45), (13.58, 8.66), (13.8, 8.93), (13.97, 9.25), (14.08, 9.61), (14.12, 10.01), (14.08, 10.42), (13.96, 10.83), (13.76, 11.23), (13.48, 11.6), (13.12, 11.92), (12.69, 12.18), (12.2, 12.35), (11.68, 12.44), (11.12, 12.43), (10.57, 12.31), (10.03, 12.09), (9.52, 11.75), (9.07, 11.32), (8.7, 10.81), (8.43, 10.21), (8.26, 9.56), (8.21, 8.87), (8.3, 8.17), (8.51, 7.47), (8.86, 6.82), (9.33, 6.22), (9.91, 5.71), (10.6, 5.3), (11.36, 5.02), (12.18, 4.88), (13.03, 4.89), (13.88, 5.06), (14.7, 5.39), (15.46, 5.87), (16.13, 6.5)]


@T("steel-coil", "Wide roll of steel sheet standing on a cradle, with spiral layers around its hollow core",
   ["coil", "sheet metal coil", "strip steel", "metal roll", "rolled steel", "mill coil", "wound steel"])
def _(S):
    sp = "M" + "L".join(f"{x} {y}" for x, y in SPIRAL)
    return [shell(circle(12, 9.5, 7.5)), detail(sp),
            shell(poly([(4, 21), (20, 21), (18, 19), (6, 19)], closed=True, r=S.r))]

@T("serial-number-plate", "Small riveted metal plate with a barcode strip between two rivets",
   ["serial number", "rating plate", "nameplate", "data plate", "asset tag", "id plate", "machine label"])
def _(S):
    return [shell(rb(S, 2, 5, 20, 14)), dot(5.5, 8.5, 1), dot(18.5, 8.5, 1), dot(5.5, 15.5, 1), dot(18.5, 15.5, 1),
            detail(seg(9, 8.5, 9, 15.5)), detail(seg(12, 8.5, 12, 15.5)), detail(seg(15, 8.5, 15, 15.5))]


@T("freezer-bag", "Flat plastic bag with a double zipper track across the top and a snowflake below it",
   ["frozen food bag", "zip bag", "zipper bag", "food storage bag", "freezer safe", "ziplock", "cold storage"])
def _(S):
    sf = [detail(seg(12, 11, 12, 17)), detail(seg(8.7, 12.6, 15.3, 15.4)), detail(seg(15.3, 12.6, 8.7, 15.4))]
    return [shell(rb(S, 4, 3, 16, 18)), detail(seg(4, 7, 20, 7)), *sf]


@T("pillow-box", "Small gift box with bowed edges and two rounded ends that bulge out like a pillow",
   ["gift box", "curved box", "favor box", "jewellery box", "pillow pack", "retail packaging", "small parcel"])
def _(S):
    return [shell("M5 5Q12 8 19 5Q22 12 19 19Q12 16 5 19Q2 12 5 5Z"), detail("M8.5 6.6Q6.5 12 8.5 17.4")]


@T("spout-pouch", "Flexible standing pouch with a screw-cap spout fitted at its sloped top corner",
   ["stand up pouch", "liquid pouch", "doypack", "squeeze pouch", "refill pouch", "baby food pouch", "spouted bag"])
def _(S):
    body = poly([(3, 21), (3, 8), (12, 8), (18, 14), (18, 21)], closed=True, r=S.r)
    spout = rot(union(rect(13.5, 8, 3, 3), rect(12.5, 5, 5, 3)), 45, 15, 11)
    return [shell(union(body, spout)), detail(seg(3, 17, 18, 17))]

def smooth(pts):
    """Catmull-Rom style smooth path through points (list of (x, y))."""
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(len(pts) - 1):
        p0 = pts[max(0, i - 1)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(len(pts) - 1, i + 2)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(p2[0])} {fmt(p2[1])}"
    return d


# =========================================================================== handling, equipment and documents

@T("labeling-parcel", "Box with a shipping label stuck on its front, one corner peeling away from the backing sheet",
   ["label application", "stick label", "shipping label", "apply label", "parcel labelling", "address label", "packing"])
def _(S):
    return [shell(rb(S, 2, 8, 15, 13)),
            detail(poly([(5, 12), (11, 12), (14, 15), (14, 18), (5, 18)], closed=True)),
            line("M14 11Q20 10 21 4")]


@T("milk-run-logistics", "Closed loop route with three stops around it and an arrow showing the direction of travel",
   ["milk run", "round trip route", "collection loop", "supplier pickup", "circular route", "multi stop route", "loop delivery"])
def _(S):
    out = []
    stops = [-90, 30, 150]
    for a in stops:
        x, y = pt_on(12, 12, 7.5, a)
        out.append(shell(rb(S, x - 2, y - 2, 4, 4)))
    for a in stops:
        out.append(line(arc(12, 12, 7.5, a + 22, a + 98)))
    th = math.radians(-30)
    ax, ay = pt_on(12, 12, 7.5, -30)
    tx, ty = -math.sin(th), math.cos(th)
    nx, ny = math.cos(th), math.sin(th)
    tip = (ax + tx * 1.4, ay + ty * 1.4)
    a1 = (ax - tx * 1.6 + nx * 2.4, ay - ty * 1.6 + ny * 2.4)
    a2 = (ax - tx * 1.6 - nx * 2.4, ay - ty * 1.6 - ny * 2.4)
    out.append(line(poly([a1, tip, a2], r=S.r)))
    return out


@T("inventory-count-tag", "Tall paper tag with a hole at the top and a perforated tear-off stub at the bottom",
   ["stock take tag", "count tag", "stocktake", "physical inventory", "tear off tag", "audit tag", "counted item"])
def _(S):
    tag = poly([(9, 2), (15, 2), (18, 5), (18, 21), (6, 21), (6, 5)], closed=True, r=S.r)
    return [shell(tag), dot(12, 6, 1.25), detail(seg(9, 10, 15, 10)),
            detail(seg(6, 16, 9, 16)), detail(seg(11, 16, 13, 16)), detail(seg(15, 16, 18, 16))]


@T("wrist-mounted-terminal", "Small screen computer strapped to a forearm with barcode bars on its display",
   ["wearable scanner", "wrist computer", "arm mounted terminal", "warehouse wearable", "wearable computer", "picker wearable"])
def _(S):
    return [line(seg(8, 2, 8, 8)), line(seg(16, 2, 16, 8)), line(seg(8, 16, 8, 22)), line(seg(16, 16, 16, 22)),
            shell(rb(S, 4, 8, 16, 8)), detail(seg(9, 10.5, 9, 13.5)), detail(seg(12, 10.5, 12, 13.5)),
            detail(seg(15, 10.5, 15, 13.5))]


def wedge(cx, cy, r, a1, a2):
    x1, y1 = pt_on(cx, cy, r, a1)
    x2, y2 = pt_on(cx, cy, r, a2)
    return f"M{fmt(cx)} {fmt(cy)}L{fmt(x1)} {fmt(y1)}A{fmt(r)} {fmt(r)} 0 0 1 {fmt(x2)} {fmt(y2)}Z"


@veh("radiation-portal-monitor", "Two tall pillars either side of a lane with a radiation trefoil above a passing truck",
     ["radiation detector", "rpm gate", "border monitor", "nuclear detection", "customs security", "scanner portal", "trefoil"])
def _(S):
    tri = [solid(wedge(12, 7.5, 4.2, a - 28, a + 28)) for a in (-90, 30, 150)]
    truck = [shell(poly([(7, 18), (7, 13), (13, 13), (13, 15), (16, 15), (17, 18)], closed=True)),
             dot(9, 19, 1.3), dot(14.5, 19, 1.3)]
    return [shell(rb(S, 2, 3, 3, 18)), shell(rb(S, 19, 3, 3, 18)), *tri, dot(12, 7.5, 1.0), *truck]


@T("strapping-machine", "Table machine with an arch frame over a box and a strap band wrapped around the box",
   ["strapper", "banding machine", "packaging line", "strap applicator", "bundle strapping", "box banding", "end of line packing"])
def _(S):
    return [line(poly([(3, 21), (3, 3), (21, 3), (21, 21)], r=S.r)), line(seg(12, 3, 12, 11)),
            shell(rb(S, 7, 11, 10, 8)), detail(seg(12, 11, 12, 19)), line(seg(2, 21, 22, 21))]


@veh("coil-railcar", "Flat railcar carrying round steel coils under two rounded hood covers",
     ["coil car", "steel coil transport", "covered coil wagon", "rail freight", "metal coils", "hooded railcar"])
def _(S):
    hood = "M{0} 14V10.5Q{0} 6 {1} 6H{2}Q{3} 6 {3} 10.5V14Z"
    h1 = hood.format(3, 6.5, 7.5, 11)
    h2 = hood.format(13, 16.5, 17.5, 21)
    return [shell(union(rect(2, 14, 20, 3, L(S, 0, 1)), h1, h2)), detail(circle(7, 11, 2)), detail(circle(17, 11, 2)),
            wheel(6.5, 19.5, 1.5), wheel(17.5, 19.5, 1.5)]


@veh("sideloader-forklift", "Low flat truck with a tall mast mounted at its side carrying long pipes across the deck",
     ["side loader", "long load truck", "pipe handling", "timber handling", "sideways forklift", "multidirectional forklift"])
def _(S):
    ws = [(5, 19, 1.5), (19, 19, 1.5)]
    pts = [(2, 18), (2, 14), (22, 14), (22, 18)]
    cab = shell(rb(S, 2, 7, 6, 7))
    pipes = [shell(circle(15, 11.5, 1.5)), shell(circle(19, 11.5, 1.5)), shell(circle(17, 8, 1.5))]
    return auto(S, pts, ws, cab, line(seg(11, 2, 11, 14)), *pipes, yb=18)


@T("customs-carnet", "Small booklet with a globe on the cover and perforated vouchers stacked beside it",
   ["ata carnet", "temporary import", "customs booklet", "passport for goods", "duty free export", "customs document", "trade permit"])
def _(S):
    return [shell(rb(S, 3, 3, 12, 18)), detail(circle(9, 10, 3.5)), detail(seg(5.5, 10, 12.5, 10)), detail(seg(6, 17, 12, 17)),
            shell(rb(S, 17, 5, 5, 4)), shell(rb(S, 17, 11, 5, 4)), shell(rb(S, 17, 17, 5, 4))]


@T("bulk-container", "Shipping container with three round loading hatches on its roof and a discharge flap at the end",
   ["dry bulk container", "grain container", "bulk cargo", "roof hatches", "powder container", "hopper container", "loose cargo"])
def _(S):
    roof = union(rect(2, 8, 20, 11, L(S, 0, 1.2)), rect(4.5, 4.5, 3.5, 3.5, 1.2), rect(10.25, 4.5, 3.5, 3.5, 1.2),
                 rect(16, 4.5, 3.5, 3.5, 1.2))
    return [shell(roof), detail(seg(9, 12, 9, 16)), detail(poly([(16, 19), (16, 13), (22, 13)])), ]


@T("letter-of-credit", "Document with a bank building at the top, a small ship below it and a signature line",
   ["documentary credit", "trade finance", "bank guarantee", "import export payment", "lc document", "payment undertaking", "bank document"])
def _(S):
    return [shell(rb(S, 3, 2, 18, 20)),
            detail(poly([(7, 8), (12, 5), (17, 8)], closed=True)), detail(seg(7, 10.5, 17, 10.5)),
            detail(poly([(7, 14), (17, 14), (15.5, 16.5), (8.5, 16.5)], closed=True)), detail(seg(12, 12, 12, 14)),
            detail(seg(7, 19, 12, 19))]


@T("un-packaging-symbol", "Circle containing a lowercase u above a lowercase n, the mark for certified dangerous goods packaging",
   ["un mark", "dangerous goods packaging", "hazmat certified", "un approved packaging", "united nations marking", "adr marking", "certified packaging"])
def _(S):
    ring = circle(12, 12, 9) if S.name == "line" else circle(12, 12, 9)
    return [shell(ring), detail("M9.5 6V8A2.5 2.5 0 0 0 14.5 8V6"), detail("M9.5 18V16A2.5 2.5 0 0 1 14.5 16V18")]


@T("robotic-grid-storage", "Top view of a square grid of storage cells with two small robots riding on the grid rails",
   ["grid storage", "cube storage", "automated storage", "warehouse robots", "storage grid", "asrs", "top view grid"])
def _(S):
    g = [line(poly([(3, 3), (21, 3), (21, 21), (3, 21)], closed=True, r=S.r))]
    g += [line(seg(9, 3, 9, 21)), line(seg(15, 3, 15, 21)), line(seg(3, 9, 21, 9)), line(seg(3, 15, 21, 15))]
    g += [solid(rect(7, 7, 4, 4)), solid(rect(13, 13, 4, 4))]
    return g


@T("bullwhip-effect", "Small box at the left with a wavy line trailing right whose swings grow larger and larger",
   ["demand amplification", "supply chain swings", "order variability", "forecast distortion", "inventory oscillation", "demand wave"])
def _(S):
    wave = smooth([(8, 12), (10, 10.5), (12.5, 13.5), (15, 8), (18, 16.5), (20.5, 5), (22, 12)])
    return [shell(rb(S, 2, 9, 4, 6)), line(wave)]


@T("pallet-pattern", "Top view of a square pallet covered in rectangular boxes laid in an interlocking brick pattern",
   ["pallet layer", "stacking pattern", "brick pattern", "palletizing pattern", "load pattern", "box layout", "interlocking layer"])
def _(S):
    return [shell(rb(S, 2, 2, 20, 20)), detail(seg(2, 9, 22, 9)), detail(seg(2, 15, 22, 15)),
            detail(seg(9, 2, 9, 9)), detail(seg(15, 9, 15, 15)), detail(seg(9, 15, 9, 22))]


@veh("converter-dolly", "Single-axle wheeled frame with a round fifth-wheel plate on top and a long A-shaped drawbar",
     ["dolly", "a dolly", "trailer dolly", "fifth wheel dolly", "b train", "drawbar", "road train link"])
def _(S):
    frame = union(rect(11, 9, 11, 3, L(S, 0, 1)), rect(13, 12, 7, 4))
    bar = poly([(2, 19), (13, 14), (13, 18)], closed=True, r=S.r)
    return [shell(union(frame, bar)), wheel(16.5, 19, 2)]


@T("double-boxed-parcel", "Small taped box nested inside a larger open box with padding either side of it",
   ["box in box", "protective packaging", "fragile parcel", "cushioned parcel", "extra padding", "secure packing", "nested box"])
def _(S):
    return [line(poly([(3, 10), (3, 21), (21, 21), (21, 10)], r=S.r)),
            shell(rb(S, 8, 4, 8, 11)), detail(seg(12, 4, 12, 8)),
            dot(5.5, 14, 1), dot(18.5, 14, 1), dot(5.5, 18, 1), dot(18.5, 18, 1)]


@T("cutout-foam-insert", "Thick foam slab with a precisely cut cavity shaped like a camera body and lens",
   ["foam insert", "custom foam", "protective foam", "case insert", "packaging foam", "camera case foam", "shaped foam"])
def _(S):
    cavity = union(rect(6, 9, 9, 7), rect(7.5, 7, 3, 2), circle(16, 12.5, 2.5))
    return [shell(rb(S, 2, 3, 20, 18)), detail(cavity)]


@T("shelf-scanning-robot", "Slim wheeled robot with a tall camera mast rolling past a store shelf, scan lines reaching the products",
   ["inventory robot", "shelf scanner", "stock checking robot", "retail robot", "store audit robot", "shelf audit", "autonomous scanner"])
def _(S):
    return [shell(rb(S, 2, 15, 7, 6)), line(seg(5.5, 3, 5.5, 15)), solid(rect(3.5, 4, 4, 3)),
            line(seg(9, 5.5, 14, 5.5)), line(seg(9, 10, 14, 10)),
            shell(rb(S, 15, 3, 7, 18)), detail(seg(15, 9, 22, 9)), detail(seg(15, 15, 22, 15))]


@T("trailer-unloading-robot", "Wheeled robot base with a jointed arm reaching into the open back of a trailer to pull out a box",
   ["truck unloader", "container unloading", "unloading robot", "carton unloader", "dock robot", "automated unloading", "robotic arm"])
def _(S):
    return [line(poly([(11, 4), (22, 4), (22, 18), (11, 18)], r=S.r)), shell(rb(S, 14, 10, 6, 6)),
            shell(rb(S, 2, 15, 7, 5)), line(poly([(5.5, 15), (5.5, 10), (12, 10)], r=S.r)), dot(5.5, 10, 1.6)]


@T("pallet-shuttle", "Side view of a pallet rack lane with a flat low robot carrying a pallet along the rails inside it",
   ["shuttle system", "pallet rack shuttle", "satellite shuttle", "deep lane storage", "rack robot", "automated storage", "asrs shuttle"])
def _(S):
    return [shell(rb(S, 2, 3, 20, 18)), detail(rect(5, 7, 9, 5)), detail(seg(2, 15, 22, 15)),
            dot(6, 17.6, 1), dot(12, 17.6, 1)]


@T("art-shipping-crate", "Open wooden crate with foam blocks in its corners cradling a framed painting",
   ["artwork crate", "painting crate", "museum shipping", "fine art transport", "framed picture crate", "gallery packing", "fragile art"])
def _(S):
    return [shell(rb(S, 2, 3, 20, 18)), detail(rect(7, 8, 10, 8)),
            detail(seg(3.5, 4.5, 6.5, 7.5)), detail(seg(20.5, 4.5, 17.5, 7.5)),
            detail(seg(3.5, 19.5, 6.5, 16.5)), detail(seg(20.5, 19.5, 17.5, 16.5))]


@T("heavy-parcel", "Taped box with a heavy weight block sitting on top of it",
   ["heavy package", "overweight parcel", "weight surcharge", "heavy item", "kilogram", "oversize weight", "lift with care"])
def _(S):
    return [shell(rb(S, 3, 11, 18, 10)), detail(seg(12, 11, 12, 15)),
            shell(poly([(8, 10), (10, 3), (14, 3), (16, 10)], closed=True, r=S.r))]


@T("bulk-stockpile", "Inclined conveyor belt dropping loose material onto the peak of a large cone-shaped pile",
   ["material heap", "aggregate pile", "coal pile", "conveyor stacker", "loose material", "sand heap", "stockyard"])
def _(S):
    return [line(seg(2, 15, 12, 5)), dot(13.2, 8, 0.9), dot(14.2, 10.2, 0.9),
            shell(poly([(4, 20), (14, 12), (21, 20)], closed=True, r=S.r))]


@T("tank-farm", "Cluster of squat round storage tanks of different sizes behind a low wall, joined by pipes",
   ["tank park", "storage tanks", "oil terminal", "bulk liquid storage", "bund wall", "fuel depot", "petrochemical storage"])
def _(S):
    def tank(x, w, top):
        return shell(f"M{x} 17V{top + 2}Q{x} {top} {x + 2} {top}H{x + w - 2}Q{x + w} {top} {x + w} {top + 2}V17Z")
    return [tank(3, 5, 8), tank(10, 5, 4), tank(17, 4, 9),
            line(poly([(2, 15), (2, 21), (22, 21), (22, 15)], r=S.r))]
