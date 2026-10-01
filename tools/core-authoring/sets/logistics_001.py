"""TypeIcon Core: logistics (batch 001, freight vehicles, containers, warehouse and packing equipment).

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
from geometry import rotation, transform_path

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


def mark(d):
    """Small mark: solid in the stroke styles, knocked out of a Filled body."""
    return Part("dot", d)


def pallet(yt=17.0, x0=2.0, x1=22.0):
    """Wooden pallet seen from the side: top board, bottom board and three blocks (a 4 px tall pallet at yt)."""
    xm = (x0 + x1) / 2
    return [line(seg(x0, yt, x1, yt)), line(seg(x0, yt + 4, x1, yt + 4)),
            solid(rect(x0, yt + 1, 3, 3)), solid(rect(xm - 1.5, yt + 1, 3, 3)), solid(rect(x1 - 3, yt + 1, 3, 3))]


def ribs(xs, y1, y2):
    """Vertical corrugation lines."""
    return [detail(seg(x, y1, x, y2)) for x in xs]


# =========================================================================== containers and trucks

@T("reefer-container", "Shipping container with corrugated walls and a refrigeration unit at one end",
   ["refrigerated container", "cold chain", "reefer", "cold storage", "freight", "cooled cargo"],
   aliases=["refrigerated-container"])
def _(S):
    return [shell(rr(S, 2, 6, 20, 12)), *ribs([6, 10], 9, 15), detail(seg(14, 6, 14, 18)), dot(18, 12, 2)]




@T("flat-rack-container", "Container base with tall end walls and a strapped crate on the open platform",
   ["flat rack", "heavy lift", "project cargo", "open sided container", "freight", "platform container"])
def _(S):
    base = rect(2, 16, 20, 4, L(S, 0, 1))
    crate = rr(S, 7, 8, 10, 8, 1)
    return [shell(union(base, crate)), detail(seg(12, 8, 12, 16)),
            line(seg(3, 4, 3, 16)), line(seg(21, 4, 21, 16))]


@T("container-doors", "Rear view of a shipping container with two doors and vertical locking bars",
   ["container end", "cargo door", "locking bar", "freight", "shipping container", "doors"])
def _(S):
    return [shell(rr(S, 4, 3, 16, 18)), detail(seg(12, 3, 12, 21)), detail(seg(8, 6, 8, 18)),
            detail(seg(16, 6, 16, 18))]


@veh("container-truck", "Semi truck cab pulling a chassis loaded with a shipping container",
     ["container lorry", "haulage", "drayage", "intermodal", "port truck", "freight", "shipping"])
def _(S):
    cab = [(17, 18), (17, 9), (19.5, 9), (22, 13), (22, 18)]
    return (body(S, cab, [(19.5, 18, 2)]) +
            [shell(rr(S, 2, 4, 13, 10, 1)), *ribs([6, 10], 7, 11),
             wheel(5, 18, 1.5), wheel(11, 18, 1.5), wheel(19.5, 18, 2)])


@T("container-spreader", "Crane spreader frame hanging from a trolley bar above a container, with twistlock legs at the corners",
   ["spreader", "container crane", "twistlock", "port crane", "lifting frame", "gantry", "hoist"])
def _(S):
    return [line(seg(4, 3, 20, 3)), line(seg(8, 3, 8, 9)), line(seg(16, 3, 16, 9)), line(seg(2, 9, 22, 9)),
            line(seg(4, 9, 4, 13)), line(seg(20, 9, 20, 13)),
            shell(rr(S, 2, 13, 20, 8, 1)), *ribs([8, 12, 16], 16, 18)]


@veh("terminal-tractor", "Short yard truck with a tall cab and a raised fifth wheel plate behind it",
     ["yard truck", "yard tractor", "shunter", "port tractor", "hostler", "yard dog", "terminal truck"],
     aliases=["yard-truck"])
def _(S):
    ws = [(7, 18, 2), (17, 18, 2)]
    pts = [(2, 18), (2, 13), (11, 13), (11, 4), (21, 4), (21, 18)]
    return auto(S, pts, ws, detail(poly([(14, 7), (19, 7), (19, 11), (14, 11)], closed=True)),
                line(seg(3, 10, 9, 10)))


@T("swap-body", "Truck box body standing on four folding steel legs with no truck underneath",
   ["swap container", "demountable body", "box body", "support legs", "freight"])
def _(S):
    return [shell(rr(S, 2, 4, 20, 11)), *ribs([7, 12, 17], 7, 12),
            line(seg(5, 15, 5, 21)), line(seg(19, 15, 19, 21))]


@T("x-ray-cargo-scanner", "Arched scanning gantry over a cargo truck with scan beams passing down onto the load",
   ["cargo scanning", "customs inspection", "border security", "x-ray gantry", "truck scanner", "screening"],
   aliases=["cargo-scanner"])
def _(S):
    truck = poly([(6, 12), (13, 12), (13, 14), (15.5, 14), (17.5, 16), (17.5, 18), (6, 18)], closed=True, r=S.r * 0.5)
    return [line(poly([(3, 21), (3, 3), (21, 3), (21, 21)], r=S.r)),
            line(seg(8, 6, 8, 9)), line(seg(12, 6, 12, 9)), line(seg(16, 6, 16, 9)),
            shell(truck), dot(9, 20, 1.25), dot(15, 20, 1.25)]


@T("container-yard", "Top view of two long rows of stacked containers with a gantry bridge across the top",
   ["container terminal", "port yard", "stacking area", "container stacks", "freight", "terminal"])
def _(S):
    return [shell(rr(S, 3, 8, 18, 5, 1)), *ribs([9, 15], 8, 13), shell(rr(S, 3, 16, 18, 5, 1)), *ribs([9, 15], 16, 21),
            line(seg(2, 3, 22, 3))]


@veh("well-car", "Low railcar with a dropped centre well carrying two stacked containers",
     ["double stack", "intermodal railcar", "container train", "rail freight", "well wagon", "flatcar"],
     aliases=["double-stack-car"])
def _(S):
    return [line(poly([(2, 15), (5, 15), (5, 18), (19, 18), (19, 15), (22, 15)], r=S.r)),
            shell(rr(S, 7, 3, 10, 11, 1)), detail(seg(7, 8.5, 17, 8.5)),
            wheel(4.5, 19.5, 1.5), wheel(19.5, 19.5, 1.5)]


@veh("gondola-railcar", "Open-top railcar with ribbed sides and a heap of scrap above the rim",
     ["gondola", "coal car", "open wagon", "rail freight", "bulk rail", "scrap car"])
def _(S):
    return [shell(rr(S, 2, 9, 20, 7, 1)), *ribs([6, 10, 14, 18], 11, 14),
            line(poly([(5, 9), (7, 6), (10, 7), (13, 4), (16, 6.5), (19, 9)], r=S.r)),
            wheel(6.5, 18.5, 1.5), wheel(17.5, 18.5, 1.5)]


@veh("curtainsider-truck", "Truck with a fabric curtain side shown in vertical folds and a buckled strap below",
     ["curtain side", "curtain trailer", "haulage", "lorry", "freight", "strap buckles"])
def _(S):
    ws = [(6.5, 18, 2), (18.5, 18, 2)]
    pts = [(2, 18), (2, 4), (15, 4), (15, 9), (18.5, 9), (21.5, 13), (21.5, 18)]
    return auto(S, pts, ws, *ribs([6, 10.5], 6.5, 11), detail(seg(2, 13.5, 15, 13.5)))


@veh("road-train", "Truck cab pulling a long chain of three trailers",
     ["triple trailer", "long haul", "outback truck", "lorry train", "freight", "cab and trailers"])
def _(S):
    cab = [(17.5, 18), (17.5, 9), (19.5, 9), (22, 13), (22, 18)]
    return (body(S, cab, [(19.5, 18, 1.5)]) +
            [shell(rr(S, 2, 8, 13, 8, 1)), *ribs([6.3, 10.7], 8, 16), wheel(4.15, 18, 1.0), wheel(8.5, 18, 1.0),
             wheel(12.85, 18, 1.0), wheel(19.5, 18, 1.5)])


@veh("dry-bulk-trailer", "Tanker trailer with a rounded tank and V-shaped hopper cones hanging under it",
     ["bulk tanker", "powder tanker", "hopper trailer", "cement tanker", "grain trailer", "pneumatic tanker"],
     aliases=["bulk-tanker"])
def _(S):
    tank = rect(2, 3, 20, 7, 3.5)
    h1 = poly([(2.5, 9), (8.5, 9), (7, 16), (4, 16)], closed=True)
    h2 = poly([(10, 9), (16, 9), (14.5, 16), (11.5, 16)], closed=True)
    return [shell(union(tank, h1, h2)), wheel(19.5, 18.5, 1.75)]

# =========================================================================== handling trucks and vehicles

@veh("tail-lift-truck", "Box truck with its lift platform lowered to the ground at the rear and a box on it",
     ["tail lift", "liftgate", "lift gate", "loading platform", "delivery", "hydraulic lift", "box truck"],
     aliases=["liftgate-truck"])
def _(S):
    pts = [(9, 17), (9, 5), (15.5, 5), (15.5, 9.5), (18.5, 9.5), (21.5, 13), (21.5, 17)]
    ws = [(12.5, 17, 1.75), (18.5, 17, 1.75)]
    return auto(S, pts, ws, line(seg(2, 19.5, 9, 19.5)), shell(rr(S, 3, 13, 4.5, 4.5, 1)))


@veh("truck-mounted-forklift", "Truck with a compact forklift carried on the back of its bed",
     ["piggyback forklift", "delivery forklift", "off-loading", "truck", "hauling"],
     aliases=["piggyback-forklift"])
def _(S):
    pts = [(4, 18), (4, 14), (13, 14), (13, 8), (17, 8), (19.5, 12), (21.5, 12.5), (21.5, 18)]
    ws = [(8, 18, 2), (17.5, 18, 2)]
    return auto(S, pts, ws, line(seg(8, 3, 8, 14)), shell(rr(S, 4.5, 9, 4, 5, 1)),
                line(seg(2, 12, 2, 14)))


@veh("knuckle-boom-truck", "Flatbed truck with a jointed crane arm behind the cab lifting a crate",
     ["loader crane", "truck crane", "articulated crane", "lorry loader", "crane truck"],
     aliases=["loader-crane-truck"])
def _(S):
    pts = [(4, 18), (4, 15), (13, 15), (13, 9), (17, 9), (19.5, 13), (21.5, 13.5), (21.5, 18)]
    ws = [(8, 18, 2), (17.5, 18, 2)]
    return auto(S, pts, ws, line(poly([(11, 15), (11, 9), (8, 4), (6, 4)], r=S.r)), line(seg(6, 4, 6, 7)),
                shell(rr(S, 3, 7, 6, 4, 1)))


@veh("oversize-load", "Truck carrying a load wider than itself, with a flag at each end of the load",
     ["wide load", "abnormal load", "heavy haulage", "escort", "special transport", "flags"],
     aliases=["wide-load"])
def _(S):
    pts = [(6, 18), (6, 14.5), (14, 14.5), (14, 10), (17.5, 10), (20, 13.5), (21.5, 14), (21.5, 18)]
    ws = [(9, 18, 2), (17, 18, 2)]
    return auto(S, pts, ws, shell(rr(S, 2.5, 8.5, 12, 6, 1)),
                line(seg(3.5, 8.5, 3.5, 2.5)), solid(poly([(3.5, 2.5), (7.5, 4), (3.5, 5.5)], closed=True)),
                line(seg(14.5, 8.5, 14.5, 2.5)), solid(poly([(14.5, 2.5), (18.5, 4), (14.5, 5.5)], closed=True)))


@T("tachograph", "In-dash recorder unit with a round dial, two display lines and a driver card slot",
   ["driver card", "digital tachograph", "driving hours", "speed recorder", "fleet compliance", "truck dashboard"],
   aliases=["digital-tachograph"])
def _(S):
    return [shell(rr(S, 2, 3, 20, 18)), detail(circle(9, 10, 2.5)), detail(seg(14.5, 8.5, 18, 8.5)),
            detail(seg(14.5, 12, 18, 12)), detail(seg(7, 17, 17, 17))]


@veh("cargo-dolly", "Airport cargo dolly: a flat roller platform on small wheels with a tow bar",
   ["uld dolly", "baggage dolly", "air cargo", "airport ground handling", "roller deck", "tow bar"],
   aliases=["uld-dolly"])
def _(S):
    return [shell(rr(S, 3, 11, 16, 4, 1.5)), dot(6.5, 8, 1.25), dot(11, 8, 1.25), dot(15.5, 8, 1.25),
            line(seg(19, 13, 22, 13)), line(seg(19, 13, 22, 19)),
            wheel(6.5, 18.5, 1.5), wheel(15.5, 18.5, 1.5)]


@veh("handcart", "Two-wheeled pushcart with a flat bed, a long handle and a pile of sacks on it",
     ["pushcart", "barrow", "sack truck", "market cart", "hand truck", "hauling", "porter"])
def _(S):
    return [line(seg(2, 14.5, 17, 14.5)), line(seg(17, 14.5, 22, 5)), line(seg(17, 14.5, 17, 20)),
            shell(union(rr(S, 3, 8, 10, 6.5, 3), rr(S, 8, 3, 7, 5.5, 2.5))), wheel(9, 18, 3)]


@veh("reach-truck", "Narrow electric lift truck with a tall mast, forks forward and a stand-up operator cage",
   ["stand-up forklift", "narrow aisle truck", "warehouse lift truck", "racking truck", "pallet mover", "forklift"])
def _(S):
    return [line(poly([(7, 3), (7, 15), (2, 15)], r=S.r)), line(seg(2, 20, 9, 20)),
            shell(rr(S, 9, 11, 12, 8, 1.5)), line(poly([(12, 11), (12, 4), (19, 4), (19, 11)], r=S.r)),
            dot(15.5, 8, 1.25), wheel(14, 19.5, 1.5)]


@T("order-picker", "Tall lift truck with the operator platform raised high beside a pallet shelf",
   ["picker truck", "man-up truck", "warehouse lift", "high level picking", "rack", "operator platform"])
def _(S):
    return [shell(rr(S, 2, 16, 9, 5, 1.5)), line(seg(5, 3, 5, 16)), line(seg(5, 11, 11, 11)),
            dot(8, 7.5, 1.4), line(seg(8, 9, 8, 11)),
            line(seg(21, 3, 21, 21)), line(seg(14, 9, 21, 9)), line(seg(14, 16, 21, 16)),
            solid(rect(16, 5, 4, 3)), solid(rect(16, 12, 4, 3))]


@T("walkie-stacker", "Pedestrian pallet stacker with a mast, raised forks carrying a pallet load and a long steering tiller",
   ["pedestrian stacker", "pallet stacker", "manual stacker", "walk behind stacker", "lift truck", "pallet lifter"])
def _(S):
    return [line(seg(12, 3, 12, 20)), line(seg(2, 12, 12, 12)), line(seg(2, 20, 12, 20)),
            shell(rr(S, 3, 5, 7, 5, 1)), shell(rr(S, 12, 14, 7, 6, 1.5)), line(seg(17, 14, 22, 4))]


@T("warehouse-robot", "Squat round-edged drive robot lifting a four-legged storage pod from underneath",
   ["amr", "autonomous mobile robot", "shelf robot", "fulfillment robot", "goods to person", "automation"],
   aliases=["drive-robot"])
def _(S):
    return [shell(rr(S, 3, 3, 18, 9)), detail(seg(3, 7.5, 21, 7.5)),
            line(seg(4, 12, 4, 20)), line(seg(20, 12, 20, 20)),
            shell(rect(8, 16, 8, 4, 2)), line(seg(10, 14, 14, 14))]


@T("palletizing-robot", "Industrial robot arm with a suction gripper setting a box onto a stack on a pallet",
   ["palletiser", "palletizer", "robot arm", "end of line", "depalletizing", "suction gripper", "automation"],
   aliases=["palletizer"])
def _(S):
    return [shell(rr(S, 2, 17, 8, 4, 1)), line(poly([(6, 17), (6, 5), (15, 5), (15, 9)], r=S.r)),
            line(seg(12, 9, 18, 9)), shell(rr(S, 12, 11, 6, 4, 1)),
            shell(rr(S, 13, 17.5, 8, 3.5, 0.5))]


@T("vertical-lift-module", "Tall storage cabinet with a service window and a parts tray pulled out in front",
   ["vlm", "automated storage", "tray storage", "parts picking", "warehouse automation", "storage and retrieval"],
   aliases=["vlm"])
def _(S):
    return [shell(union(rr(S, 4, 2, 16, 20), rect(2, 14, 20, 5))), detail(rr(S, 7, 4.5, 10, 5, 1)), detail(seg(2, 14, 22, 14)),
            solid(rect(8, 10.5, 3, 2)), solid(rect(13, 11, 3, 1.5))]

# =========================================================================== racking, docks and conveying

@T("carton-flow-rack", "Side view of a shelf with sloped roller lanes and cartons waiting at the low picking end",
   ["flow rack", "gravity flow", "carton flow", "picking face", "roller lanes", "fifo storage", "order picking"],
   aliases=["flow-rack"])
def _(S):
    return [line(seg(3, 3, 3, 21)), line(seg(21, 3, 21, 21)),
            line(seg(3, 5, 21, 8)), line(seg(3, 11, 21, 14)), line(seg(3, 17, 21, 20)),
            solid(rect(14, 3, 4, 3)), solid(rect(14, 9, 4, 3)), solid(rect(14, 15, 4, 3))]


@T("cantilever-rack", "Side view of a central upright column with long arms reaching out both ways carrying pipes",
   ["cantilever racking", "long goods storage", "lumber rack", "pipe storage", "timber rack", "arms"],
   aliases=["cantilever-racking"])
def _(S):
    return [line(seg(12, 2, 12, 20)), line(seg(6, 21, 18, 21)),
            line(poly([(3, 5), (3, 9), (12, 9)], r=S.r * 0.5)), line(poly([(21, 5), (21, 9), (12, 9)], r=S.r * 0.5)),
            line(poly([(3, 13), (3, 17), (12, 17)], r=S.r * 0.5)), line(poly([(21, 13), (21, 17), (12, 17)], r=S.r * 0.5)),
            dot(7, 6, 1.6), dot(10.5, 6, 1.6) if False else dot(7, 14, 1.6), dot(17, 6, 1.6), dot(17, 14, 1.6)]


@T("warehouse-mezzanine", "Raised steel platform on columns with a handrail above and pallets stored underneath",
   ["mezzanine", "raised platform", "mezzanine floor", "storage platform", "warehouse upgrade", "two level storage"],
   aliases=["mezzanine"])
def _(S):
    return [line(seg(2, 10, 22, 10)), line(poly([(3, 10), (3, 5), (21, 5), (21, 10)], r=S.r * 0.5)),
            line(seg(12, 5, 12, 10)), line(seg(3, 10, 3, 21)), line(seg(21, 10, 21, 21)),
            shell(rr(S, 8, 14, 8, 7, 1)), detail(seg(8, 17.5, 16, 17.5))]


@T("picking-cart", "Wheeled cart with a push handle and two shelves holding labelled totes",
   ["order picking cart", "pick cart", "tote cart", "warehouse trolley", "fulfilment cart", "shelf trolley"])
def _(S):
    return [line(seg(4, 3, 4, 19)), line(seg(20, 4, 20, 19)), line(seg(2, 3, 6, 3)),
            line(seg(4, 10.5, 20, 10.5)), line(seg(4, 17, 20, 17)),
            shell(rr(S, 8, 4.5, 8, 5, 1)), shell(rr(S, 8, 11.5, 8, 5, 1)),
            dot(5, 21, 1.25), dot(19, 21, 1.25)]


@T("dock-leveler", "Side view of a hinged steel plate bridging a loading dock edge to the back of a trailer",
   ["loading dock", "dock plate", "bridge plate", "edge of dock", "trailer loading", "ramp plate"])
def _(S):
    dock = poly([(2, 9), (10, 9), (10, 21), (2, 21)], closed=True, r=S.r)
    return [shell(dock), line(seg(10, 9, 15, 13)), shell(rr(S, 15, 4, 7, 9, 3)), wheel(19, 18.5, 2)]


@T("dock-shelter", "Front view of a loading door framed by thick padded curtains on three sides",
   ["dock seal", "loading bay", "door surround", "truck dock", "weather seal", "padded frame"],
   aliases=["dock-seal"])
def _(S):
    return [shell(poly([(2, 21), (2, 3), (22, 3), (22, 21), (17, 21), (17, 9), (7, 9), (7, 21)], closed=True, r=S.r * 0.5)),
            line(seg(8, 13, 16, 13)), line(seg(8, 17, 16, 17))]


@T("dock-bumper", "Thick ribbed rubber block bolted to a wall plate to absorb truck impacts",
   ["loading dock bumper", "rubber bumper", "impact protection", "wall guard", "laminated bumper", "dock protection"])
def _(S):
    return [line(seg(4, 3, 4, 21)), shell(rr(S, 8, 6, 12, 12, 2)), detail(seg(8, 10, 20, 10)), detail(seg(8, 14, 20, 14))]


@T("yard-ramp", "Side view of a mobile steel ramp on wheels sloping up to the back of a trailer",
   ["mobile ramp", "loading ramp", "container ramp", "forklift ramp", "yard loading", "truck ramp"])
def _(S):
    return [shell(poly([(2.5, 19), (2.5, 17), (16, 9.5), (16, 19)], closed=True, r=S.r)), wheel(13, 18.5, 1.25),
            shell(rr(S, 17, 3, 4, 16, 1))]


@T("dock-plate", "Top view of a rectangular metal plate with a diamond tread and two lifting handle slots",
   ["loading plate", "bridge plate", "diamond plate", "checker plate", "truck ramp plate", "steel plate"])
def _(S):
    dm = lambda cx, cy: poly([(cx, cy - 1.75), (cx + 1.75, cy), (cx, cy + 1.75), (cx - 1.75, cy)], closed=True)
    return [shell(rr(S, 2, 5, 20, 14, 1.5)), detail(seg(5.5, 9, 9.5, 9)), detail(seg(14.5, 9, 18.5, 9)),
            mark(dm(7, 14.5)), mark(dm(12, 14.5)), mark(dm(17, 14.5))]




@T("ball-transfer-table", "Top view of a square table covered in a grid of small balls with a box resting on it",
   ["ball table", "omni directional table", "transfer table", "ball bearing deck", "conveyor", "sorting table"])
def _(S):
    dots = [dot(x, y, 1.1) for x in (6.5, 17.5) for y in (6.5, 17.5)] + [dot(12, 6.5, 1.1), dot(12, 17.5, 1.1),
                                                                         dot(6.5, 12, 1.1), dot(17.5, 12, 1.1)]
    return [shell(rr(S, 2, 2, 20, 20, 3)), *dots, shell(rr(S, 9.5, 9.5, 5, 5, 0.5))]


@T("parcel-sorter", "Top view of a conveyor line with angled branches splitting boxes toward several chutes",
   ["sortation", "diverter", "parcel sorting", "conveyor sorter", "sort centre", "sort center", "chute"])
def _(S):
    return [shell(rr(S, 2.5, 9.5, 5, 5, 1)), line(seg(8, 12, 22, 12)),
            line(poly([(10, 12), (14, 5), (22, 5)], r=S.r)), line(poly([(10, 12), (14, 19), (22, 19)], r=S.r))]


@T("drum-truck", "Two-wheeled hand truck with a curved cradle and a top hook holding a steel drum",
   ["drum dolly", "barrel truck", "drum handler", "barrel cart", "drum mover", "steel drum"])
def _(S):
    return [shell(rr(S, 4, 4, 9, 14, 2)), detail(seg(4, 8.5, 13, 8.5)), detail(seg(4, 13.5, 13, 13.5)),
            line(poly([(17, 19), (17, 3), (21, 3)], r=S.r * 0.5)), line(seg(3, 20, 17, 20)), line(seg(17, 7, 13, 7)),
            wheel(19.5, 18.5, 2.25)]


@T("furniture-dolly", "Low square moving platform with carpeted edges on casters, seen at three quarters",
   ["moving dolly", "piano dolly", "mover's dolly", "furniture mover", "casters", "moving platform"],
   aliases=["moving-dolly"])
def _(S):
    return [shell(poly([(7, 5), (22, 5), (22, 9), (17, 15), (2, 15), (2, 11)], closed=True, r=S.r * 0.5)),
            detail(seg(2, 11, 17, 11)), detail(seg(17, 11, 22, 5)),
            dot(5, 19.5, 1.5), dot(14.5, 19.5, 1.5), dot(20, 14, 1.25)]


@T("stair-climbing-hand-truck", "Hand truck with a three-wheeled triangular cluster at the bottom and a box strapped on",
   ["stair climber", "stair hand truck", "sack truck", "trolley", "delivery", "moving", "tri-wheel"],
   aliases=["stair-climber"])
def _(S):
    return [line(poly([(15, 18), (15, 3), (19, 3)], r=S.r * 0.5)), line(seg(2, 16, 15, 16)),
            shell(rr(S, 3, 5, 9, 9, 1)),
            wheel(18, 15, 1.5), wheel(15.5, 19.5, 1.5), wheel(20.5, 19.5, 1.5)]


# =========================================================================== pallets, cages and bulk packaging

@T("pallet-wrapper", "Turntable carrying a pallet load being wound with stretch film from a tall mast carriage",
   ["stretch wrapper", "pallet wrapping", "stretch film", "shrink wrap", "turntable wrapper", "load wrapping"],
   aliases=["stretch-wrapper"])
def _(S):
    return [shell(rr(S, 3, 4, 11, 13, 1)), detail(seg(3, 9, 14, 6.5)), detail(seg(3, 14.5, 14, 12)),
            line(seg(2, 20, 16, 20)), line(seg(21, 3, 21, 21)), shell(circle(18.5, 9, 1.5)), line(seg(17, 9, 14, 9))]


@T("pallet-stack", "Side view of five empty wooden pallets stacked neatly on top of each other",
   ["stacked pallets", "empty pallets", "wood pallets", "pallet pile", "skids", "pallet storage"],
   aliases=["stacked-pallets"])
def _(S):
    parts = []
    for k in range(5):
        parts += [line(seg(2, 3 + 4.5 * k, 22, 3 + 4.5 * k))]
    for k in range(4):
        y = 4 + 4.5 * k
        parts += [solid(rect(2, y, 3, 2.5)), solid(rect(10.5, y, 3, 2.5)), solid(rect(19, y, 3, 2.5))]
    return parts


@T("pallet-collar", "Wooden pallet with two hinged wooden frames stacked on top forming an open crate",
   ["pallet frame", "pallet box", "wooden collar", "stackable collar", "hinged collar", "bulk crate"])
def _(S):
    return [shell(rr(S, 3, 3, 18, 12, 1)), detail(seg(3, 9, 21, 9)), *pallet(17)]


@T("cage-pallet", "Steel wire mesh box on a pallet base with a fold-down front panel",
   ["roll cage", "wire mesh container", "stillage", "mesh cage", "storage cage", "post pallet"])
def _(S):
    return [shell(rr(S, 3, 2, 18, 13, 1)), *ribs([8, 12, 16], 4, 13), detail(seg(3, 8.5, 21, 8.5)), *pallet(17)]


@T("pallet-box", "Large corrugated box as wide as the pallet it sits on, with forklift openings visible below",
   ["bulk box", "pallet-size carton", "big box", "corrugated bin", "bulk container", "pallet carton"])
def _(S):
    return [shell(rr(S, 2, 2, 20, 14, 1)), detail(seg(12, 2, 12, 8)), detail(seg(2, 8, 22, 8)), *pallet(17)]


@T("octabin", "Large eight-sided corrugated bulk box with a chamfered top, standing on a pallet",
   ["octagonal bin", "bulk bin", "eight sided box", "bulk carton", "bulk bag box", "corrugated octagon"],
   aliases=["octagonal-bin"])
def _(S):
    body = poly([(3, 15), (3, 5), (7, 2), (17, 2), (21, 5), (21, 15)], closed=True, r=S.r * 0.5)
    return [shell(body), detail(seg(3, 5, 21, 5)), detail(seg(7, 5, 7, 15)), detail(seg(17, 5, 17, 15)), *pallet(17)]


@T("plastic-pallet", "Top view of a molded plastic pallet with a ribbed grid deck and nine blocky feet",
   ["plastic skid", "molded pallet", "hygienic pallet", "export pallet", "grid deck", "nestable pallet"])
def _(S):
    dots = [dot(x, y, 1) for x in (5.5, 12, 18.5) for y in (5.5, 12, 18.5)]
    return [shell(rr(S, 2, 2, 20, 20, 4)), detail(seg(9, 2, 9, 22)), detail(seg(15, 2, 15, 22)),
            detail(seg(2, 9, 22, 9)), detail(seg(2, 15, 22, 15)), *dots]


@T("edge-protector", "Box load with an angle strip fitted over its top corner to protect it from strapping",
   ["corner board", "angle board", "edge board", "corner protector", "load stabiliser", "pallet strapping"],
   aliases=["corner-board"])
def _(S):
    return [shell(rr(S, 3, 7, 13, 14, 1)), line(poly([(9, 3), (20, 3), (20, 14)], r=S.r))]


@T("pallet-scale", "Low weighing platform with a box on it and a digital readout on a post",
   ["floor scale", "pallet weighing", "platform scale", "weighbridge", "weigh station", "freight scale"])
def _(S):
    return [shell(rr(S, 2, 17, 17, 4, 1)), shell(rr(S, 4, 7, 11, 10, 1)), line(seg(20, 7, 20, 21)),
            shell(rr(S, 16.5, 2.5, 5, 4, 0.5)), dot(19, 4.5, 0.8) if False else detail(seg(3.5, 12, 12.5, 12))]


@T("spill-pallet", "Grated platform on a deep sump tray with two upright drums standing on it",
   ["spill containment", "drum pallet", "bunded pallet", "spill tray", "hazmat storage", "chemical storage"],
   aliases=["bunded-pallet"])
def _(S):
    return [shell(rr(S, 4, 3, 6, 11, 2)), shell(rr(S, 14, 3, 6, 11, 2)), detail(seg(4, 8.5, 10, 8.5)),
            detail(seg(14, 8.5, 20, 8.5)), shell(rr(S, 3, 15, 18, 6, 1)), detail(seg(7, 18, 17, 18))]


@T("strip-curtain", "Doorway hung with vertical clear plastic strips, one strip pushed aside",
   ["pvc strip door", "plastic curtain", "cold room door", "freezer curtain", "door strips", "dock door curtain"])
def _(S):
    return [line(seg(2, 4, 22, 4)), line(seg(5, 4, 5, 21)), line(seg(9, 4, 9, 21)), line(seg(13, 4, 13, 21)),
            line("M17 4C17 12 20.5 14 20.5 21")]


@T("louvered-bin-rack", "Wall panel with rows of horizontal louver slots holding small open-front parts bins",
   ["louver panel", "parts bins", "bin rack", "small parts storage", "hanging bins", "wall bin rack"],
   aliases=["louver-panel"])
def _(S):
    return [shell(rr(S, 2, 2, 20, 20, 4)), detail(seg(2, 11.5, 22, 11.5)),
            mark(poly([(5, 5), (11, 5), (10, 9), (6, 9)], closed=True)), mark(poly([(14, 5), (20, 5), (19, 9), (15, 9)], closed=True)),
            mark(poly([(5, 14.5), (11, 14.5), (10, 18.5), (6, 18.5)], closed=True)),
            mark(poly([(14, 14.5), (20, 14.5), (19, 18.5), (15, 18.5)], closed=True))]


@T("tote-dolly", "Square wheeled base with casters and a stack of plastic totes on top",
   ["tote cart", "crate dolly", "tote stack", "bin dolly", "rolling base", "storage tote"])
def _(S):
    a = poly([(3.5, 2), (20.5, 2), (19, 8.5), (5, 8.5)], closed=True)
    b = poly([(3.5, 8.5), (20.5, 8.5), (19, 15), (5, 15)], closed=True)
    return [shell(union(a, b)), line(seg(2, 17.5, 22, 17.5)), dot(5, 21, 1.25), dot(19, 21, 1.25)]


@T("collapsible-crate", "Plastic crate with its walls folded flat into the base and one wall half raised",
   ["folding crate", "foldable crate", "collapsible tote", "stackable bin", "flat pack crate", "reusable crate"])
def _(S):
    return [shell(rr(S, 2, 16, 20, 5, 1)), shell(poly([(3, 16), (5, 6), (19, 6), (21, 16)], closed=True, r=S.r * 0.5)),
            detail(seg(9, 10.5, 15, 10.5))]


@T("rfid-portal", "Doorway gate with antenna posts on both sides and radio wave arcs over a pallet passing through",
   ["rfid gate", "tag reader portal", "dock door reader", "radio frequency identification", "antenna gate", "inbound scanning"],
   aliases=["rfid-gate"])
def _(S):
    return [line(seg(3, 3, 3, 21)), line(seg(21, 3, 21, 21)), line(seg(3, 3, 21, 3)),
            line(arc(12, 14, 4, 205, 335)), line(arc(12, 14, 7.5, 215, 325)), shell(rr(S, 8, 15.5, 8, 5.5, 1))]


# =========================================================================== scanning and order fulfilment

@T("rfid-reader", "Handheld pistol-grip reader with a flat antenna paddle on top sending out radio waves",
   ["rfid scanner", "handheld reader", "tag scanner", "uhf reader", "inventory scanner", "radio frequency"],
   aliases=["rfid-scanner"])
def _(S):
    handle = poly([(6, 9), (12, 9), (11, 21), (6, 21)], closed=True, r=S.r)
    return [shell(union(rr(S, 2, 4, 12, 5, 1.5), handle)), detail(seg(8, 13, 9.5, 13)),
            line(arc(14, 6.5, 4, -55, 55)), line(arc(14, 6.5, 7.5, -50, 50))]


@T("ring-scanner", "Barcode scanner worn on a finger with a strap, sending a scan beam toward a small barcode",
   ["wearable scanner", "finger scanner", "hands free scanner", "barcode ring", "wearable barcode reader", "picking scanner"])
def _(S):
    return [shell(circle(6, 15.5, 3.5)), shell(rr(S, 8, 6, 7, 5, 1.5)),
            line(seg(15.5, 8.5, 17.5, 7)), line(seg(15.5, 8.5, 17.5, 10)),
            solid(rect(19, 5.5, 1.5, 8)), solid(rect(21.5, 5.5, 1, 8)) if False else solid(rect(21.5, 5.5, 0.5, 8))]


@T("voice-picking-headset", "Single-ear headset with a boom microphone beside a box on a shelf",
   ["voice picking", "warehouse headset", "pick by voice", "hands free picking", "boom mic", "audio picking"],
   aliases=["picking-headset"])
def _(S):
    return [shell(rr(S, 2, 9, 4.5, 8, 2)), line(arc(9, 11, 6.5, 180, 360)),
            line(poly([(4.25, 17), (4.25, 19), (6, 20.5), (9, 20.5)], r=S.r)), dot(10.5, 20.5, 1.5),
            line(seg(14, 21, 22, 21)), shell(rr(S, 16, 11, 5, 7, 1))]


@T("pick-to-light", "Shelf front with two bins, one marked by a lit button and the other by a number display",
   ["light directed picking", "pick light", "led picking", "order picking aid", "bin indicator", "lit button"])
def _(S):
    return [shell(rr(S, 3, 13, 6, 8, 1)), shell(rr(S, 14, 13, 6, 8, 1)), shell(rr(S, 3, 3, 6, 4.5, 1)),
            dot(17, 8.5, 1.4), line(seg(17, 2.5, 17, 4.5)), line(seg(13.5, 4, 14.5, 5.5)), line(seg(20.5, 4, 19.5, 5.5))]


@T("put-wall", "Grid of open cubbies with some small parcels inside and indicator lights above the top row",
   ["put to wall", "sorting wall", "order consolidation", "cubby wall", "pigeonhole", "sortation wall"])
def _(S):
    return [shell(rr(S, 2, 5, 20, 17, 4)), detail(seg(9, 5, 9, 22)), detail(seg(15, 5, 15, 22)),
            detail(seg(2, 11, 22, 11)), detail(seg(2, 16.5, 22, 16.5)),
            mark(rect(4.5, 7, 2, 2)), mark(rect(17.5, 12.5, 2, 2)), mark(rect(11, 18, 2, 2)), mark(rect(4.5, 18, 2, 2)),
            dot(5.5, 2.5, 1.25), dot(18.5, 2.5, 1.25)]


@T("freight-elevator", "Wide elevator car with vertical sliding gate bars and a loaded pallet inside",
   ["cargo lift", "goods lift", "service elevator", "industrial lift", "freight lift", "pallet lift"],
   aliases=["goods-lift"])
def _(S):
    return [shell(rr(S, 3, 2, 18, 20, 1)), *ribs([8, 12, 16], 4, 11), detail(rr(S, 6.5, 14, 11, 5, 1))]


@T("mailer-box", "Flat folded cardboard box with a hinged lid tucked into the front, lid slightly raised",
   ["shipping box", "e-commerce box", "tuck top box", "folding carton", "subscription box", "cardboard mailer"],
   aliases=["tuck-top-box"])
def _(S):
    body = poly([(2, 21), (2, 9), (4.5, 3.5), (19.5, 3.5), (22, 9), (22, 21)], closed=True, r=S.r * 0.5)
    return [shell(body), detail(seg(2, 9, 22, 9)), detail(poly([(9, 9), (9, 13.5), (15, 13.5), (15, 9)], r=S.r * 0.5))]


@T("poly-mailer", "Flat plastic shipping bag with a peel strip flap at the top and a label on the front",
   ["padded bag", "plastic mailer", "courier bag", "shipping bag", "envelope bag", "peel and seal"])
def _(S):
    return [shell(rr(S, 4, 2, 16, 20, 4)), detail(seg(4, 7.5, 20, 7.5)), detail(rr(S, 8, 11.5, 8, 6, 0.5))]


@T("paper-void-fill", "Open box with crumpled kraft paper balls bulging out of the top",
   ["packing paper", "crinkle paper", "kraft paper fill", "cushioning", "void filler", "eco packaging"])
def _(S):
    b1 = poly([(4, 12), (4.5, 8), (7, 5.5), (10, 6.5), (12, 9), (12, 12)], closed=True, r=S.r)
    b2 = poly([(11, 12), (12, 7), (15, 3.5), (18, 6), (20, 9), (20, 12)], closed=True, r=S.r)
    return [shell(union(rr(S, 3, 12, 18, 9, 1.5), b1, b2)), detail(poly([(7, 12), (8.5, 9.5), (10, 10)], r=0)),
            detail(poly([(15, 12), (16, 8.5), (18, 9)], r=0))]


@T("packing-list-pouch", "Clear adhesive envelope stuck on a box face with a folded document visible inside",
   ["invoice pouch", "document enclosed pouch", "shipping label pouch", "packing slip envelope", "waybill pouch", "paperwork"],
   aliases=["invoice-pouch"])
def _(S):
    return [shell(rr(S, 2, 2, 20, 20, 3)), detail(rr(S, 5.5, 6, 13, 11, 1)), detail(seg(9, 10, 15, 10)),
            detail(seg(9, 13.5, 13, 13.5))]


# =========================================================================== packaging materials

@T("returnable-tote", "Plastic tote box with a split lid folded shut and a hand hole at each end",
   ["reusable tote", "plastic tote", "lidded tote", "returnable container", "rpc", "attached lid container"])
def _(S):
    body = poly([(2, 3), (22, 3), (22, 8), (20, 21), (4, 21), (2, 8)], closed=True, r=S.r * 0.5)
    return [shell(body), detail(seg(2, 8, 22, 8)), detail(seg(12, 3, 12, 8)), detail(seg(6.5, 13.5, 9.5, 13.5)),
            detail(seg(14.5, 13.5, 17.5, 13.5))]


@T("flexitank", "Shipping container with its doors open showing a bulging liquid bladder filling the inside",
   ["flexi tank", "liquid bulk", "bulk liquid container", "bladder tank", "container liner tank", "liquid cargo"],
   aliases=["flexi-tank"])
def _(S):
    drop = "M12 9.5L14 12.5A2 2 0 1 1 10 12.5Z"
    return [shell(rr(S, 3, 2, 18, 20, 2)), detail(rr(S, 7, 7, 10, 10, 4)), mark(drop)]


@T("stand-up-pouch", "Flexible pouch standing upright on a gusseted base with a zip line near the top",
   ["spouted pouch", "food pouch", "resealable pouch", "flexible packaging", "zipper bag", "standing bag"])
def _(S):
    d = "M5 3H19L20.5 17C17 21.5 7 21.5 3.5 17Z" if S.name != "rounded" else \
        "M6.5 3H17.5Q19 3 19.1 4.5L20.5 17C17 21.5 7 21.5 3.5 17L4.9 4.5Q5 3 6.5 3Z"
    return [shell(d), detail(seg(5, 8, 19, 8)), detail(circle(12, 14, 2))]


@T("dry-ice", "Stack of frosty ice cubes with vapor curls rising off the top",
   ["cold pack", "frozen shipping", "co2 ice", "cold chain packing", "chilled cargo", "coolant"])
def _(S):
    cubes = union(rr(S, 3, 16, 18, 5, 1), rr(S, 7, 10, 10, 6, 1))
    return [shell(cubes), detail(seg(12, 16, 12, 21)), detail(seg(7, 16, 17, 16)),
            line("M10 7.5C8 5.5 12 4.5 10 2"), line("M14 7.5C12 5.5 16 4.5 14 2")]


@T("wardrobe-box", "Tall moving box with the top open, showing a hanging rail with two clothes hangers",
   ["garment box", "hanging box", "moving box", "clothes carton", "relocation box", "hanger rail"])
def _(S):
    return [shell(rr(S, 3, 10, 18, 11, 1)), line(seg(3, 3, 21, 3)), line(seg(8, 3, 8, 6)), line(seg(16, 3, 16, 6)),
            line(poly([(5, 9), (8, 6), (11, 9)], r=S.r * 0.5)), line(poly([(13, 9), (16, 6), (19, 9)], r=S.r * 0.5))]


@T("fiber-drum", "Tall cylindrical cardboard drum with a metal lid clamped down by a locking ring",
   ["fibre drum", "cardboard drum", "paper drum", "keg drum", "lever lock ring", "shipping drum"],
   aliases=["fibre-drum"])
def _(S):
    return [shell(union(rr(S, 4, 3, 16, 4, 1.5), rr(S, 5.5, 7, 13, 14, 1.5))), detail(seg(5.5, 14, 18.5, 14)),
            mark(rect(11, 4.5, 2, 1.5))]


@T("honeycomb-paper", "Sheet of kraft paper stretched into an open hexagon mesh",
   ["paper honeycomb", "expanded paper", "cell paper", "eco cushioning", "hexagon mesh", "protective wrap"])
def _(S):
    R = 3.3
    w = R * math.sqrt(3)
    cells = []
    for row, (y, xs) in enumerate([(6.3, [5.3, 5.3 + w, 5.3 + 2 * w]), (6.3 + 1.5 * R, [5.3 + w / 2, 5.3 + 1.5 * w]),
                                   (6.3 + 3 * R, [5.3, 5.3 + w, 5.3 + 2 * w])]):
        for x in xs:
            cells.append(line(poly([(x + R * math.cos(math.radians(a)), y + R * math.sin(math.radians(a)))
                                    for a in (-90, -30, 30, 90, 150, 210)], closed=True, r=S.r)))
    return cells


@T("foam-corner", "Block of protective foam with a stepped notch cut out to cradle the corner of a box",
   ["corner protector", "foam block", "packaging foam", "eps corner", "edge guard", "cushion corner"],
   aliases=["foam-corner-protector"])
def _(S):
    d = poly([(3, 3), (14, 3), (14, 10), (21, 10), (21, 21), (3, 21)], closed=True, r=S.r * 0.5)
    return [shell(d), mark(circle(7, 8, 1)), mark(circle(9, 15, 1)), mark(circle(16, 16, 1))]


@T("carton-divider", "Top view of an open box split into a grid of cells by cardboard partitions holding bottles",
   ["box partition", "cell divider", "bottle carton", "glass separator", "cardboard grid", "egg carton insert"])
def _(S):
    return [shell(rr(S, 2, 2, 20, 20, 4)), detail(seg(12, 2, 12, 22)), detail(seg(2, 12, 22, 12)),
            dot(7, 7, 2.25), dot(17, 7, 2.25), dot(7, 17, 2.25), dot(17, 17, 2.25)]


@T("bottle-shipper", "Molded pulp tray sleeve with bottle-shaped cavities holding two bottles",
   ["bottle carrier", "pulp tray", "wine shipper", "bottle sleeve", "molded fiber", "bottle packaging"])
def _(S):
    def bottle(x):
        return "M%s 2H%sV7Q%s 8.5 %s 12V21H%sV12Q%s 8.5 %s 7Z" % (x + 2, x + 5, x + 7, x + 7, x, x, x + 2)
    return [shell(union(bottle(3), bottle(14), rr(S, 2, 13, 20, 8, 1.5))), detail(seg(2, 13, 22, 13))]


