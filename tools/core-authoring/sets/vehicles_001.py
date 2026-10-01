"""TypeIcon Core: vehicles (batch 001, road vehicles).

Visual language (shared with sets/transport.py so the two families sit together):
  * Side-view road vehicles face right. Wheels are rings on a common ground line (bottoms near y 20), the
    body outline is left open where it meets a wheel (`body`), and in Filled the body is cut 1 px clear of
    solid wheels (`veh`). Standard car wheels are r 2 at x 6.5 and 17.5 on y 18.
  * Bicycles, motorcycles and other open frames draw their wheels as rings in every style (Filled makes the
    strokes heavier), so frames stay readable.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    rect, regular, seg, shell, solid,
)
from geometry import rotation, transform_path

CAT = "vehicles"
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


def T(name, description, tags, aliases=()):
    """Register an icon whose Filled design is derived from its Line geometry."""
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases,
                    filled=lambda: filled_region(fn(FILL)))(fn)
    return deco


def wheel(x, y=18.0, r=2.0):
    """Side-view wheel: a ring in Line/Rounded; a solid disc cut 1 px clear of the body in Filled."""
    p = shell(circle(x, y, r))
    p.wheel = (x, y, r)
    return p


def hub(x, y, r=1.0):
    """Hub mark inside a big wheel: solid in Line/Rounded, a hole in the Filled disc."""
    p = dot(x, y, r)
    p.knock = True
    return p


def body(S, pts, ws, yb=None, r=None):
    """Side-view body. `pts` run clockwise from the bottom-left corner over the top to the bottom-right corner
    (both on y = yb); the bottom edge is left open where a wheel crosses it."""
    yb = ws[0][1] if yb is None else yb
    rr = S.r if r is None else r
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
        return [shell(poly(pts, closed=True, r=rr))]
    out = [shell(poly([(gaps[0][0], yb)] + list(pts) + [(gaps[-1][1], yb)], r=rr))]
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


W2 = [(6.5, 18, 2), (17.5, 18, 2)]  # standard car wheels


# =========================================================================== cars

@veh("hatchback", "Compact hatchback car with a steep rear hatch",
     ["hatch", "small car", "city car", "five door", "car", "compact"])
def _(S):
    pts = [(3, 18), (3, 12), (6.5, 6.5), (12.5, 6.5), (16, 10.5), (21, 11.5), (21, 18)]
    return auto(S, pts, W2, detail(seg(4.6, 10.5, 16, 10.5)), detail(seg(10.5, 6.5, 10.5, 10.5)))


@veh("station-wagon", "Estate car with a long flat roof and a square tailgate",
     ["estate car", "wagon", "family car", "shooting brake", "car", "tailgate"], aliases=["estate-car"])
def _(S):
    pts = [(3, 18), (3, 8), (13.5, 8), (16.5, 11.5), (21, 12.5), (21, 18)]
    return auto(S, pts, W2, detail(seg(3, 11.5, 16.5, 11.5)), detail(seg(7.5, 8, 7.5, 11.5)),
                detail(seg(11.5, 8, 11.5, 11.5)))


@veh("coupe", "Low two-door coupe with a fastback roof",
     ["two door", "sports coupe", "fastback", "car", "grand tourer", "gt"])
def _(S):
    pts = [(3, 18), (3, 13.5), (10, 8), (14, 8), (17.5, 11.5), (21, 12.5), (21, 18)]
    return auto(S, pts, W2, detail(seg(6.4, 11.5, 17.5, 11.5)))


@veh("suv", "Tall sport utility vehicle with roof rails and big wheels",
     ["sport utility vehicle", "4x4", "crossover", "car", "family car"], aliases=["sport-utility-vehicle"])
def _(S):
    ws = [(7, 18, 2.5), (17, 18, 2.5)]
    pts = [(3, 18), (3, 7.5), (14.5, 7.5), (17, 11), (21, 12), (21, 18)]
    return auto(S, pts, ws, detail(seg(3, 11, 17, 11)), detail(seg(9.5, 7.5, 9.5, 11)),
                line(poly([(5, 7.5), (5, 4.5), (12.5, 4.5), (12.5, 7.5)], r=S.r * 0.5)))


@veh("compact-car", "Short, tall city car with its wheels at the corners",
     ["city car", "small car", "mini", "microcar", "urban", "car"], aliases=["city-car"])
def _(S):
    ws = [(7.5, 18, 2), (16.5, 18, 2)]
    pts = [(4.5, 18), (4.5, 11), (7, 6), (13, 6), (16.5, 10.5), (19.5, 11.5), (19.5, 18)]
    return auto(S, pts, ws, detail(seg(5.2, 10.5, 16.5, 10.5)), detail(seg(11, 6, 11, 10.5)), r=L(S, 0, 2))


@veh("microcar", "Tiny egg-shaped bubble car",
     ["bubble car", "tiny car", "three wheeler", "retro car", "car"], aliases=["bubble-car"])
def _(S):
    ws = [(7.5, 18, 2), (16.5, 18, 2)]
    if isF(S):
        b = [shell("M4 18V13A8 7.5 0 0 1 20 13V18Z")]
    elif S.name == "line":
        b = [shell("M5.5 18H4V13A8 7.5 0 0 1 20 13V18H18.5"), line(seg(9.5, 18, 14.5, 18))]
    else:
        b = [shell("M5.5 18Q4 18 4 16.5V13A8 7.5 0 0 1 20 13V16.5Q20 18 18.5 18"), line(seg(9.5, 18, 14.5, 18))]
    return b + [wheel(*w) for w in ws] + [detail(seg(4, 12.5, 20, 12.5)), detail(seg(14, 6.3, 14, 12.5))]


@veh("limousine", "Stretched limousine with a long row of side windows",
     ["limo", "stretch limo", "luxury car", "chauffeur", "vip", "wedding car"], aliases=["limo"])
def _(S):
    ws = [(5, 18, 2), (19, 18, 2)]
    pts = [(2.5, 18), (2.5, 13), (4, 12.5), (5.5, 9), (17, 9), (18.5, 12.5), (21.5, 13), (21.5, 18)]
    return auto(S, pts, ws, detail(seg(4, 12.5, 18.5, 12.5)), detail(seg(8.5, 9, 8.5, 12.5)),
                detail(seg(12, 9, 12, 12.5)), detail(seg(15.5, 9, 15.5, 12.5)))


@veh("muscle-car", "Heavy muscle car with a hood scoop and wide rear tires",
     ["american muscle", "v8", "classic car", "hot car", "coupe", "drag"])
def _(S):
    ws = [(6.5, 17.5, 2.5), (17.5, 18, 2)]
    pts = [(3, 18), (3, 10.5), (6.5, 10.5), (8.5, 7.5), (12, 7.5), (14.5, 10.5), (16, 10.5), (16.5, 8.5), (19, 8.5),
           (19.5, 10.5), (21, 11), (21, 18)]
    return auto(S, pts, ws, detail(seg(6.5, 10.5, 14.5, 10.5)), yb=18)


@veh("vintage-car", "1920s car with an upright cabin, a short hood and spoked wheels",
     ["antique car", "classic car", "old car", "oldtimer", "retro"], aliases=["antique-car"])
def _(S):
    ws = [(6.5, 17.5, 3), (17.5, 17.5, 3)]
    pts = [(3.5, 15), (3.5, 4.5), (14, 4.5), (14, 9.5), (19.5, 9.5), (20, 15)]
    return auto(S, pts, ws, detail(seg(3.5, 9.5, 14, 9.5)), detail(seg(8.75, 4.5, 8.75, 9.5)),
                line(seg(2.5, 4.5, 15, 4.5)), hub(6.5, 17.5), hub(17.5, 17.5), yb=15)


@veh("lowrider", "Long lowrider sedan with small wheels, its front bouncing up",
     ["low rider", "hydraulics", "custom car", "bounce", "cruiser", "car culture"])
def _(S):
    deg = -9
    c = (5, 19.5)
    ws = [(5, 19.5, 1.5), (18.5, 17.4, 1.5)]
    raw = [(2.5, 19.5), (2.5, 15), (5, 14.2), (7.5, 10.5), (14, 10.5), (16.5, 14), (21.5, 15), (21.5, 19.5)]
    pts = [rpt(p, deg, c) for p in raw]
    fx, fy = rpt((18.5, 19.5), deg, c)
    ws = [(5, 19.5, 1.5), (fx, fy, 1.5)]
    if isF(S):
        b = [shell(poly(pts, closed=True))]
    else:
        h = 1.5
        a0 = (5 + h, 19.5)
        f0 = rpt((18.5 - h, 19.5), deg, c)
        f1 = rpt((18.5 + h, 19.5), deg, c)
        b = [shell(poly([(5 - h, 19.5)] + pts + [f1], r=S.r)), line(seg(*a0, *f0))]
    belt = [rpt(p, deg, c) for p in [(5, 14.2), (16.5, 14.2)]]
    return b + [wheel(*w) for w in ws] + [detail(seg(*belt[0], *belt[1])), line(seg(9, 21.5, 21, 21.5))]


@veh("rally-car", "Rally hatchback with a rear wing and dirt spraying from the wheel",
     ["rally", "motorsport", "gravel", "racing", "off road racing"], aliases=["rally-racing"])
def _(S):
    ws = [(9.5, 18, 2), (18, 18, 2)]
    pts = [(6.5, 18), (6.5, 12), (9, 7.5), (14, 7.5), (16.5, 11), (21, 12), (21, 18)]
    return auto(S, pts, ws, detail(seg(7.8, 11, 16.5, 11)),
                line(seg(5, 4.5, 10, 4.5)), line(seg(8.5, 4.5, 9.5, 7.5)),
                dot(3.5, 18.5, 1), dot(3, 14.75, 1), dot(4, 11, 1))


@veh("dragster", "Long drag racer with a needle nose, giant rear wheels and a high wing",
     ["drag racing", "top fuel", "drag strip", "quarter mile", "race car", "speed"])
def _(S):
    ws = [(6, 17, 4), (20, 19.5, 1.5)]
    pts = [(10, 17), (10, 12.5), (13, 12.5), (22, 16.5), (22, 17)]
    if isF(S):
        b = [shell(poly(pts + [(10, 18)], closed=True))]
    else:
        b = [shell(poly([(10, 18)] + pts[1:] + [(18.5, 17)], r=S.r * 0.5))]
    return b + [wheel(*ws[0]), wheel(*ws[1]), hub(6, 17, 1.25),
                line(seg(2.5, 4.5, 9, 4.5)), line(seg(6, 4.5, 6, 11)),
                dot(12, 10.5, 1.5)]


@veh("go-kart", "Low go-kart with a helmeted driver behind a steering wheel",
     ["karting", "kart", "go cart", "racing", "track", "amusement"], aliases=["kart"])
def _(S):
    ws = [(6, 19, 2), (18, 19, 2)]
    return [shell(rect(3, 15.5, 18, 2, L(S, 0.01, 1))), wheel(*ws[0]), wheel(*ws[1]),
            shell(circle(9, 6, 2.5)),
            line(poly([(9, 9.5), (8, 13.5), (13.5, 13.5)], r=S.r * 0.5)),
            line(seg(10, 11, 14, 11)), line(seg(16.5, 15.5, 14.5, 10))]


@veh("dune-buggy", "Open dune buggy with a tube roll cage and big rear tires",
     ["beach buggy", "sand rail", "buggy", "off road", "dunes", "desert"], aliases=["beach-buggy"])
def _(S):
    ws = [(6.5, 17.5, 3), (18, 18.5, 2)]
    pts = [(3, 17.5), (3, 13.5), (15, 13.5), (21, 15.5), (21, 17.5)]
    return auto(S, pts, ws, line(poly([(4.5, 13.5), (7, 4.5), (11.5, 4.5), (16.5, 13.5)], r=S.r)),
                line(seg(7, 4.5, 12, 13.5)), hub(6.5, 17.5), yb=17.5)


@veh("off-road-vehicle", "Boxy four-by-four with a spare wheel on the back and a snorkel",
     ["4x4", "four wheel drive", "off roader", "overland", "expedition", "4wd"], aliases=["four-by-four"])
def _(S):
    ws = [(8.5, 18, 2.5), (17.5, 18, 2.5)]
    pts = [(5.5, 18), (5.5, 5.5), (14, 5.5), (14, 10), (21, 10.5), (21, 18)]
    return auto(S, pts, ws, detail(seg(5.5, 10, 14, 10)), detail(seg(10, 5.5, 10, 10)),
                shell(rect(2.5, 8, 2.5, 7, L(S, 0.5, 1.25))), line(poly([(17.5, 10.5), (17.5, 4), (19.5, 4)], r=S.r * 0.5)))


@veh("self-driving-car", "Car with a sensor dome on the roof sending out signal arcs",
     ["autonomous car", "driverless", "robotaxi", "lidar", "autonomous vehicle", "av", "smart car"],
     aliases=["autonomous-car", "driverless-car"])
def _(S):
    pts = [(3, 18), (3, 14), (5, 13), (7, 10.5), (16, 10.5), (18, 13), (21, 14), (21, 18)]
    return auto(S, pts, [(6.5, 18, 2), (17.5, 18, 2)], detail(seg(11.5, 10.5, 11.5, 13)),
                solid("M9.75 10.5A1.75 1.75 0 0 1 13.25 10.5Z"),
                line(arc(11.5, 10.5, 4.5, 225, 315)), line(arc(11.5, 10.5, 7.5, 240, 300)))


@veh("hearse", "Long hearse with a closed rear compartment and a landau bar",
     ["funeral car", "funeral", "coffin car", "undertaker", "memorial", "mortuary"], aliases=["funeral-car"])
def _(S):
    ws = [(6, 18, 2), (18, 18, 2)]
    pts = [(2.5, 18), (2.5, 7), (14, 7), (16.5, 11), (21.5, 12), (21.5, 18)]
    return auto(S, pts, ws, detail(seg(11, 11, 16.5, 11)), detail(seg(11, 7, 11, 11)),
                detail("M4.5 12.5C7 12.5 6 9.5 8.5 9.5"))


@T("car-top-view", "Car seen from directly above with windscreen, roof and rear window",
   ["car from above", "top down car", "parking", "bird's eye view", "overhead car", "car"], aliases=["car-top-down"])
def _(S):
    k = L(S, 2.5, 4)
    return [shell(rect(6.5, 2.5, 11, 19, k)),
            detail("M8 9Q12 7.5 16 9"), detail("M8.5 16.5Q12 17.5 15.5 16.5"),
            solid(rect(4, 5, 2.5, 3.5, L(S, 0, 1))), solid(rect(17.5, 5, 2.5, 3.5, L(S, 0, 1))),
            solid(rect(4, 15.5, 2.5, 3.5, L(S, 0, 1))), solid(rect(17.5, 15.5, 2.5, 3.5, L(S, 0, 1)))]


# =========================================================================== trucks

@veh("semi-truck", "Big rig tractor unit pulling a long box trailer",
     ["semi", "big rig", "articulated lorry", "18 wheeler", "tractor trailer", "haulage", "hgv"],
     aliases=["big-rig", "tractor-trailer"])
def _(S):
    tr = [(2.5, 18.5), (2.5, 4.5), (12.5, 4.5), (12.5, 18.5)]
    cab = [(15, 18.5), (15, 7.5), (18.5, 7.5), (21, 11.5), (21, 18.5)]
    return (body(S, tr, [(4.75, 18.5, 1.5), (10, 18.5, 1.5)]) + body(S, cab, [(18, 18.5, 1.5)]) +
            [wheel(4.75, 18.5, 1.5), wheel(10, 18.5, 1.5), wheel(18, 18.5, 1.5),
             detail(poly([(17, 7.5), (17, 11.5), (21, 11.5)], r=S.r * 0.5)), line(seg(15.5, 7.5, 15.5, 4)),
             line(seg(12.5, 15.5, 15, 15.5))])


@veh("flatbed-truck", "Truck with a cab and an empty flat deck",
     ["flatbed", "flat deck", "platform truck", "stake truck", "haulage", "lorry"], aliases=["platform-truck"])
def _(S):
    pts = [(3, 18), (3, 13.5), (12, 13.5), (12, 5.5), (16.5, 5.5), (19.5, 10.5), (21, 11), (21, 18)]
    return auto(S, pts, W2, detail(poly([(14, 5.5), (14, 10.5), (19.5, 10.5)], r=S.r * 0.5)),
                line(seg(3, 13.5, 3, 10.5)), line(seg(7.5, 13.5, 7.5, 10.5)))


@veh("tanker-truck", "Truck pulling a long cylindrical tank with a hatch on top",
     ["tanker", "fuel truck", "oil tanker", "milk tanker", "tank truck", "petrol tanker"], aliases=["tank-truck"])
def _(S):
    tank = rect(3, 5.5, 11.5, 8.5, L(S, 3, 4.25))
    deck = [(3, 18), (3, 14), (14.5, 14), (14.5, 18)]
    cab = [(16.5, 18), (16.5, 8.5), (19, 8.5), (21, 12), (21, 18)]
    return (body(S, deck, [(6, 18, 1.75), (10.5, 18, 1.75)]) + body(S, cab, [(18.75, 18, 1.75)]) +
            [shell(tank), wheel(6, 18, 1.75), wheel(10.5, 18, 1.75), wheel(18.75, 18, 1.75),
             line(seg(8.75, 5.5, 8.75, 3)), line(seg(14.5, 15.5, 16.5, 15.5))])


@veh("refrigerated-truck", "Box truck with a cooling unit and a snowflake on the side",
     ["reefer", "refrigerated lorry", "cold chain", "chiller truck", "frozen delivery", "freezer truck"],
     aliases=["reefer-truck"])
def _(S):
    pts = [(3, 18), (3, 6.5), (14, 6.5), (14, 9), (18, 9), (21, 12.5), (21, 18)]
    arms = [seg(*a, *b) for a, b in [((9, 8.75), (9, 14.25)), ((6.6, 10.1), (11.4, 12.9)), ((6.6, 12.9), (11.4, 10.1))]]
    sf = [Part("dot", path_to_d(U(*[ST(a, 2, S.cap, S.join) for a in arms])))]
    return auto(S, pts, W2, detail(seg(14, 9, 14, 18)), detail(poly([(16, 9), (16, 12.5), (21, 12.5)], r=S.r * 0.5)),
                shell(rect(10, 3, 4, 3.5, L(S, 0.5, 1))), *sf)


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def cab(S, x0=16, top=8.5, wx=18.75, wr=1.75):
    """Small truck cab facing right, starting at x0, with its own wheel."""
    pts = [(x0, 18), (x0, top), (19, top), (21, top + 3.5), (21, 18)]
    return body(S, pts, [(wx, 18, wr)]) + [wheel(wx, 18, wr)]


@veh("logging-truck", "Logging truck carrying stacked logs between upright stakes",
     ["log truck", "timber lorry", "lumber", "forestry", "logs", "timber haulage"], aliases=["timber-truck"])
def _(S):
    deck = [(2.5, 18), (2.5, 15.5), (14.5, 15.5), (14.5, 18)]
    return (body(S, deck, [(5.5, 18, 1.75), (10.5, 18, 1.75)]) + cab(S) +
            [wheel(5.5, 18, 1.75), wheel(10.5, 18, 1.75), line(seg(14.5, 16, 16, 16)),
             line(seg(2.5, 15.5, 2.5, 6.5)), line(seg(14.5, 15.5, 14.5, 6.5)),
             dot(6, 12.25, 1.75), dot(11, 12.25, 1.75), dot(8.5, 8, 1.75)])


@veh("monster-truck", "Monster truck: a pickup body perched on giant tires",
     ["monster truck", "truck show", "giant wheels", "stunt truck", "4x4"])
def _(S):
    body_ = poly([(3, 11), (3, 7.5), (10.5, 7.5), (10.5, 3.5), (14.5, 3.5), (17, 7.5), (21, 8), (21, 11)],
                 closed=True, r=S.r * 0.5)
    return [shell(body_), wheel(6.75, 17.25, 3.75), wheel(17.25, 17.25, 3.75), hub(6.75, 17.25, 1.25),
            hub(17.25, 17.25, 1.25)]


@veh("ice-cream-truck", "Ice cream van with a serving window and a big cone on the roof",
     ["ice cream van", "soft serve", "summer", "dessert", "treat", "frozen treats"], aliases=["ice-cream-van"])
def _(S):
    pts = [(3, 18), (3, 11), (15, 11), (18, 13.5), (21, 14), (21, 18)]
    cone = poly([(6.5, 6.5), (12.5, 6.5), (9.5, 11)], closed=True, r=S.r * 0.3)
    return auto(S, pts, W2, detail(seg(5, 14.5, 12, 14.5)), shell(cone),
                shell("M6.5 6.5A3 3 0 0 1 12.5 6.5Z"), line(seg(9.5, 3.5, 9.5, 1.5)))


@veh("food-truck", "Food truck with an awning over its open serving window",
     ["street food", "food van", "catering truck", "takeaway", "mobile kitchen", "lunch truck"], aliases=["food-van"])
def _(S):
    pts = [(3, 18), (3, 5), (14, 5), (14, 8.5), (18, 8.5), (21, 12.5), (21, 18)]
    aw = ("M4.5 8H12.5V9.5A1.333 1.333 0 0 1 9.833 9.5A1.333 1.333 0 0 1 7.167 9.5"
          "A1.333 1.333 0 0 1 4.5 9.5Z")
    return auto(S, pts, W2, detail(seg(14, 8.5, 14, 18)), detail(poly([(16, 8.5), (16, 12.5), (21, 12.5)], r=S.r * 0.5)),
                Part("dot", aw), detail(seg(4.5, 14, 12.5, 14)))


@veh("mail-truck", "Boxy postal delivery truck with an envelope on the side",
     ["postal van", "mail van", "post truck", "mail delivery", "postman", "parcel"], aliases=["mail-van", "postal-truck"])
def _(S):
    pts = [(3, 18), (3, 4.5), (15.5, 4.5), (16.5, 10), (21, 11), (21, 18)]
    env = [detail(rect(5.5, 8.5, 7, 5, min(S.R, 1))), detail(poly([(5.5, 8.5), (9, 11.5), (12.5, 8.5)], r=S.r * 0.4))]
    return auto(S, pts, W2, detail(poly([(15, 4.5), (15, 10), (16.5, 10)], r=S.r * 0.3)), *env)


@veh("armored-truck", "Armored cash truck with slit windows and a padlock on the side",
     ["armoured truck", "cash in transit", "security van", "bank truck", "money transport", "secure transport"],
     aliases=["armoured-truck", "security-van"])
def _(S):
    pts = [(3, 18), (3, 5), (15, 5), (15.5, 8.5), (20.5, 9.5), (21, 13), (21, 18)]
    return auto(S, pts, W2, detail(seg(17, 11, 20, 11)),
                detail(rect(6, 11, 5.5, 4, min(S.R, 1))), detail(arc(8.75, 11, 1.75, 180, 360)))


@veh("snowplow", "Snowplow truck pushing snow with a big curved blade",
     ["snow plough", "snow plow", "winter maintenance", "gritter", "snow clearing", "road clearing"],
     aliases=["snow-plough"])
def _(S):
    pts = [(2.5, 18), (2.5, 10.5), (8, 10.5), (8, 5.5), (12, 5.5), (15, 10.5), (15, 18)]
    return (auto(S, pts, [(5.5, 18, 2), (12, 18, 2)], detail(poly([(10, 5.5), (10, 10.5), (14.4, 10.5)], r=S.r * 0.4))) +
            [line(seg(15, 15.5, 17, 15.5)), line("M18 10.5C21 13 21 17.5 18 20.5"),
             dot(21, 6.5, 1), dot(18.5, 7.5, 1)])


@veh("salt-spreader", "Gritting truck with a hopper spreading salt from the rear",
     ["gritter", "salt truck", "road salt", "winter", "de-icing", "grit spreader"], aliases=["gritter-truck"])
def _(S):
    hop = poly([(7, 5.5), (14.5, 5.5), (13.5, 12.5), (8, 12.5)], closed=True, r=S.r * 0.5)
    deck = [(7, 18), (7, 14.5), (14.5, 14.5), (14.5, 18)]
    return (body(S, deck, [(10.5, 18, 2)]) + cab(S) + [wheel(10.5, 18, 2), shell(hop),
            line(seg(14.5, 16, 16, 16)), dot(3.5, 11, 1), dot(3, 15, 1), dot(3.5, 19, 1)])


@veh("vacuum-truck", "Vacuum tanker truck with a thick suction hose hanging off the back",
     ["vacuum tanker", "septic truck", "sewer truck", "gully sucker", "suction truck", "drain cleaning"],
     aliases=["septic-truck"])
def _(S):
    tank = rect(5.5, 5.5, 10, 8.5, L(S, 3, 4.25))
    deck = [(5.5, 18), (5.5, 14), (15.5, 14), (15.5, 18)]
    return (body(S, deck, [(8.5, 18, 1.75), (12.75, 18, 1.75)]) + cab(S, x0=17, top=9, wx=19.25, wr=1.5) +
            [shell(tank), wheel(8.5, 18, 1.75), wheel(12.75, 18, 1.75),
             line("M5.5 9.5C2 9.5 2.5 14 3 21")])


@veh("mobile-library", "Library bus with book spines showing through its windows",
     ["bookmobile", "library van", "book bus", "mobile books", "outreach", "reading"], aliases=["bookmobile"])
def _(S):
    pts = [(3, 18), (3, 5), (18, 5), (21, 9), (21, 18)]
    books = [detail(seg(5.5, 8.5, 5.5, 13)), detail(seg(8.5, 8, 8.5, 13)), detail(seg(11.5, 9, 11.5, 13)),
             detail(seg(13.5, 13, 15.5, 8.5))]
    return auto(S, pts, W2, detail(poly([(18, 5), (18, 11), (21, 11)], r=S.r * 0.3)), *books)


# =========================================================================== buses and vans

@veh("school-bus", "School bus with a short hood, a row of windows and a fold-out stop sign",
     ["school", "yellow bus", "students", "kids bus", "pupil transport", "field trip"])
def _(S):
    ws = [(6.5, 18, 2), (18, 18, 2)]
    pts = [(3, 18), (3, 5), (16, 5), (16, 10.5), (20.5, 11), (21, 13), (21, 18)]
    return auto(S, pts, ws, detail(seg(3, 10, 16, 10)), detail(seg(6.5, 5, 6.5, 10)), detail(seg(10, 5, 10, 10)),
                detail(seg(13.5, 5, 13.5, 10)), solid(poly(regular(14, 14.25, 1.9, 8, -67.5), closed=True)))


@veh("articulated-bus", "Bendy bus made of two sections joined by a flexible bellows",
     ["bendy bus", "articulated", "rapid transit bus", "brt", "city bus", "tandem bus"], aliases=["bendy-bus"])
def _(S):
    a = [(2.5, 18), (2.5, 5.5), (10, 5.5), (10, 18)]
    b = [(14, 18), (14, 5.5), (19.5, 5.5), (21.5, 8), (21.5, 18)]
    return (body(S, a, [(6, 18, 1.75)]) + body(S, b, [(18, 18, 1.75)]) +
            [wheel(6, 18, 1.75), wheel(18, 18, 1.75), detail(seg(2.5, 10, 10, 10)), detail(seg(14, 10, 21.5, 10)),
             line(poly([(11, 7), (13, 9), (11, 11.5), (13, 14), (11, 16.5)], r=0))])


@veh("trolleybus", "Trolleybus with two roof poles reaching up to overhead wires",
     ["trolley bus", "electric bus", "trackless trolley", "overhead wire", "public transport", "city bus"],
     aliases=["trolley-bus"])
def _(S):
    pts = [(3, 18), (3, 9), (19, 9), (21, 11.5), (21, 18)]
    return auto(S, pts, W2, detail(seg(3, 12.5, 21, 12.5)), detail(seg(8, 9, 8, 12.5)), detail(seg(13, 9, 13, 12.5)),
                line(seg(11, 9, 7, 3)), line(seg(15.5, 9, 11.5, 3)), line(seg(3, 3, 21, 3)))


@veh("minibus", "High-roof minibus with a sliding door and three side windows",
     ["mini bus", "shuttle", "people mover", "van", "group transport", "airport shuttle"], aliases=["shuttle-bus"])
def _(S):
    pts = [(3, 18), (3, 5), (16, 5), (19, 10), (21, 11), (21, 18)]
    return auto(S, pts, W2, detail(seg(3, 10, 19, 10)), detail(seg(7, 5, 7, 10)), detail(seg(11.5, 5, 11.5, 10)),
                detail(seg(15.5, 5, 15.5, 10)), detail(seg(11.5, 10, 11.5, 15.5)))


@veh("police-van", "Police van with a light bar, a checkered stripe and barred rear windows",
     ["police wagon", "paddy wagon", "prisoner transport", "riot van", "law enforcement", "patrol van"],
     aliases=["paddy-wagon"])
def _(S):
    pts = [(3, 18), (3, 6.5), (15, 6.5), (18, 11), (21, 12), (21, 18)]
    return auto(S, pts, W2, detail(seg(3, 11, 18, 11)), detail(seg(12.5, 6.5, 12.5, 11)),
                detail(seg(6, 6.5, 6, 11)), detail(seg(9, 6.5, 9, 11)),
                solid(rect(7, 3, 6, 2.5, L(S, 0, 1))),
                sq(5, 13, 2, 2), sq(9, 13, 2, 2), sq(13, 13, 2, 2), sq(17, 13, 2, 2))


# =========================================================================== motorcycles and small motor vehicles

def ring(x, y, r):
    return line(circle(x, y, r))


@T("dirt-bike", "Tall off-road dirt bike with a high front mudguard and knobby tires",
   ["motocross", "enduro", "trail bike", "off road motorcycle", "mx", "scrambler"], aliases=["motocross-bike"])
def _(S):
    return [ring(5.5, 17.5, 3.5), ring(18.5, 17.5, 3.5), dot(5.5, 17.5, 1), dot(18.5, 17.5, 1),
            shell(poly([(3.5, 9), (10.5, 9), (14, 8), (14.5, 10), (11.5, 13), (8.5, 13)], closed=True, r=S.r * 0.4)),
            line(seg(5.5, 17.5, 9.5, 13)), line(seg(18.5, 17.5, 15.5, 5.5)), line(seg(13.5, 5, 17, 5)),
            line(seg(16.5, 11, 21, 11))]


@T("chopper-motorcycle", "Chopper motorcycle with a long raked fork and tall handlebars",
   ["chopper", "custom bike", "cruiser", "biker"], aliases=["chopper-bike"])
def _(S):
    return [ring(5, 17.5, 3), ring(19.5, 17.5, 2.5),
            shell(poly([(3, 12), (7.5, 12), (9, 10), (13, 10), (13.5, 12.5), (11, 15), (8.5, 15)], closed=True, r=S.r * 0.4)),
            line(seg(5, 17.5, 8.5, 15)), line(seg(19.5, 17.5, 13.5, 6.5)), line(poly([(13.5, 6.5), (12.5, 3), (15, 3)], r=S.r * 0.4))]


@T("touring-motorcycle", "Touring motorcycle with a front fairing, saddlebags and a top box",
   ["tourer", "touring bike", "motorbike", "road trip", "adventure bike", "long distance"], aliases=["tourer"])
def _(S):
    return [ring(5.5, 18, 2.75), ring(18.5, 18, 2.75),
            shell(poly([(2.5, 13.5), (2.5, 10.5), (9, 10.5), (13, 9), (15, 5), (17.5, 5), (17.5, 12), (13.5, 15), (8, 15)],
                       closed=True, r=S.r * 0.4)),
            shell(rect(2.5, 5, 4.5, 3.5, min(S.R, 1))), detail(seg(3, 13, 7, 13)),
            line(seg(17.5, 12, 18.5, 18))]


@T("police-motorcycle", "Police motorcycle with a windshield, saddlebags and a light on a rear pole",
   ["police bike", "motor officer", "patrol motorcycle", "traffic police", "law enforcement", "escort"],
   aliases=["police-bike"])
def _(S):
    return [ring(5.5, 18, 2.75), ring(18.5, 18, 2.75),
            shell(poly([(2.5, 13.5), (2.5, 10.5), (9, 10.5), (13, 9), (15, 5), (17.5, 5), (17.5, 12), (13.5, 15), (8, 15)],
                       closed=True, r=S.r * 0.4)),
            line(seg(4, 10.5, 4, 5.5)), solid(rect(2.5, 2, 3, 3, L(S, 0, 1))), detail(seg(3, 13, 7, 13)),
            line(seg(17.5, 12, 18.5, 18))]


@veh("sidecar-motorcycle", "Motorcycle with a bullet-shaped sidecar on its own wheel",
     ["sidecar", "motorbike and sidecar", "combination", "outfit", "vintage motorcycle", "passenger"],
     aliases=["sidecar-bike"])
def _(S):
    car_ = "M6 16.5V12H13C15.5 12 17 13.5 17.5 16.5Z"
    if S.name == "rounded":
        car_ = "M7.5 16.5A1.5 1.5 0 0 1 6 15V13.5A1.5 1.5 0 0 1 7.5 12H13C15.5 12 17 13.5 17.5 16.5Z"
    return [ring(4, 17.5, 2.5), ring(20, 17.5, 2.5), line(seg(20, 17.5, 17, 6.5)), line(seg(15.5, 6.5, 18.5, 6.5)),
            line(poly([(4, 17.5), (4, 9.5), (10, 9.5)], r=S.r * 0.5)), line(seg(13, 9.5, 16.4, 9.5)),
            shell(car_), wheel(11, 19.5, 1.75)]


@veh("quad-bike", "Quad bike with fat tires, a straddle seat and luggage racks",
     ["atv", "all terrain vehicle", "four wheeler", "quad", "off road", "farm quad"], aliases=["atv"])
def _(S):
    b = poly([(2.5, 13), (3.5, 10.5), (7.5, 10.5), (8.5, 8.5), (13, 8.5), (14, 10.5), (20.5, 10.5), (21.5, 13)],
             closed=True, r=S.r * 0.5)
    return [shell(b), wheel(6, 17.5, 3), wheel(18, 17.5, 3), line(poly([(15, 10.5), (15, 6), (17, 6)], r=S.r * 0.4)),
            line(seg(2.5, 7, 6.5, 7)), line(seg(18, 7.5, 21.5, 7.5))]


@veh("delivery-scooter", "Step-through scooter with a big delivery box behind the seat",
     ["delivery scooter", "food delivery", "courier", "moped", "takeaway", "rider"], aliases=["delivery-moped"])
def _(S):
    b = poly([(3, 16), (3.5, 13), (5.5, 12), (11.5, 12), (12.5, 15.5), (15.5, 15.5), (16.5, 8), (18.5, 8), (17.5, 16)],
             closed=True, r=S.r * 0.5)
    return [shell(b), shell(rect(3, 3.5, 7, 6.5, min(S.R, 1.5))), line(seg(17.5, 8, 17.5, 5)), line(seg(15.5, 5, 19.5, 5)),
            ring(6, 19, 2), ring(18, 19, 2)]


@veh("golf-cart", "Golf cart with a canopy roof and a golf bag on the back",
     ["golf buggy", "golf car", "course", "caddie", "electric cart", "resort cart"], aliases=["golf-buggy"])
def _(S):
    pts = [(2.5, 18), (2.5, 15), (8, 15), (8, 11), (11, 11), (11, 15), (21, 15), (21, 18)]
    return auto(S, pts, W2, line(seg(9, 11, 9, 4.5)), line(seg(18.5, 15, 16.5, 4.5)), line(seg(7.5, 4.5, 18, 4.5)),
                shell(rect(3, 9, 2.5, 6, L(S, 0.01, 1.25))), line(seg(3.5, 9, 3, 5.5)), line(seg(5, 9, 5.5, 6)))


@T("snowmobile", "Snowmobile with front skis, a rear track and handlebars",
   ["sled", "snow machine", "winter", "arctic", "snowsport"], aliases=["snow-machine"])
def _(S):
    b = poly([(3, 14.5), (3, 11.5), (9.5, 11.5), (13, 9.5), (16, 9.5), (20, 13.5), (18, 14.5)], closed=True, r=S.r * 0.5)
    return [shell(b), shell(rect(3, 16.5, 11, 4.5, L(S, 1.5, 2.25))), line(seg(13.5, 9.5, 12, 6)),
            line(seg(10.5, 6, 13, 6)),
            line(seg(17, 15, 17, 19.5)), line(poly([(13.5, 19.5), (20.5, 19.5), (21.5, 17.5)], r=S.r * 0.5))]


@T("snowcat", "Tracked snow groomer with a cab, a front blade and a rear tiller",
   ["snow groomer", "piste basher", "piste machine", "ski resort", "grooming", "snow tractor"],
   aliases=["snow-groomer"])
def _(S):
    tr = rect(5, 14.5, 12, 6.5, L(S, 2.5, 3.25))
    cab_ = poly([(7, 12.5), (7, 5), (13, 5), (15.5, 9), (15.5, 12.5)], closed=True, r=S.r * 0.5)
    return [shell(tr), dot(8.25, 17.75, 1.1), dot(13.75, 17.75, 1.1), shell(cab_), detail(seg(7, 9, 15.5, 9)),
            line("M19 12C21.5 14 21.5 18 19 20"), line(seg(17, 17.5, 19.5, 16)),
            shell(rect(2, 14, 1.5, 6, 0.01 if S.name == "line" else 0.75)), line(seg(3.5, 16, 5, 16))]


# =========================================================================== trailers

@veh("caravan-trailer", "Travel caravan with a door, a window and a tow hitch",
     ["caravan", "travel trailer", "camping trailer", "tourer", "holiday", "towing"], aliases=["travel-trailer"])
def _(S):
    pts = [(2.5, 17), (2.5, 5), (16, 5), (18, 9), (18, 17)]
    return (body(S, pts, [(10, 17, 2)], r=L(S, 1, 2.5)) + [wheel(10, 17, 2), detail(rect(5, 8, 5, 3.5, min(S.R, 1))),
            detail(seg(14, 8, 14, 17)), line(seg(18, 14.5, 21.5, 17)), line(seg(21.5, 17, 21.5, 20))])


@veh("teardrop-trailer", "Small teardrop camping trailer with a curved back and one wheel",
     ["teardrop", "mini camper", "tiny trailer", "camping", "overlanding", "trailer"], aliases=["teardrop-camper"])
def _(S):
    ws = [(9, 17.5, 2)]
    if isF(S):
        b = [shell("M2.5 17.5C2.5 10 6.5 6 11 6C14.5 6 17.5 11 17.5 15V17.5Z")]
    else:
        b = [shell("M7 17.5H2.5C2.5 10 6.5 6 11 6C14.5 6 17.5 11 17.5 15V17.5H11" if S.name == "line" else
                   "M7 17.5H4A1.5 1.5 0 0 1 2.5 16C2.5 10 6.5 6 11 6C14.5 6 17.5 11 17.5 15V16A1.5 1.5 0 0 1 16 17.5H11")]
    return b + [wheel(*ws[0]), detail(ellipse(10.5, 10.5, 2.5, 1.75)), line(seg(17.5, 15, 21.5, 17)),
                line(seg(21.5, 17, 21.5, 20))]


@veh("utility-trailer", "Small open box trailer with one wheel and a tow bar",
     ["box trailer", "cargo trailer", "car trailer", "hauling", "towing", "garden trailer"], aliases=["box-trailer"])
def _(S):
    pts = [(2.5, 17), (2.5, 10.5), (15.5, 10.5), (15.5, 17)]
    return (body(S, pts, [(9, 17, 2)]) + [wheel(9, 17, 2), line(seg(15.5, 15, 20.5, 16.5)), dot(20.5, 16.5, 1.5),
            line(seg(2.5, 10.5, 2.5, 8)), line(seg(15.5, 10.5, 15.5, 8))])


@veh("rooftop-tent", "Car with a tent pitched on its roof and a ladder to the ground",
     ["roof tent", "car camping", "overlanding", "camping", "tent", "road trip"], aliases=["roof-tent"])
def _(S):
    pts = [(7.5, 18.5), (7.5, 13.5), (16, 13.5), (18.5, 16), (21, 16.5), (21, 18.5)]
    ws = [(10.5, 18.5, 1.75), (18, 18.5, 1.75)]
    return (body(S, pts, ws, yb=18.5) + [wheel(*w) for w in ws] +
            [shell(poly([(8, 11), (12.5, 4), (17, 11)], closed=True, r=S.r * 0.5)), detail(seg(12.5, 7.5, 12.5, 11)),
             line(seg(6.5, 11, 3, 21)), line(seg(3.3, 17.5, 5.2, 17.5)), line(seg(4.5, 14, 6.4, 14))])


# =========================================================================== taxis, carts and personal movers

@veh("auto-rickshaw", "Three-wheeled auto rickshaw with a canvas roof, open sides and one front wheel",
     ["tuk tuk", "tuktuk", "autorickshaw", "three wheeler", "motor taxi", "trishaw", "baby taxi"], aliases=["tuk-tuk"])
def _(S):
    pts = [(3, 18), (3, 7.5), (5.5, 4.5), (15.5, 4.5), (16.5, 12), (20.5, 15.5), (20.5, 18)]
    ws = [(7.5, 18, 2), (17.5, 18.5, 1.75)]
    return auto(S, pts, ws, detail(poly([(3, 12.5), (10.5, 12.5), (10.5, 4.5)], r=S.r * 0.5)),
                detail(seg(10.5, 12.5, 16.4, 12.5)), yb=18)


@veh("cycle-rickshaw", "Cycle rickshaw with a hooded passenger bench and a rider's saddle in front",
     ["pedicab", "trishaw", "bike taxi", "becak", "cyclo", "pedal rickshaw"], aliases=["pedicab"])
def _(S):
    return [shell(poly([(2.5, 13.5), (2.5, 11), (10, 11), (10, 13.5)], closed=True, r=S.r * 0.5)),
            line("M2.5 11V9A6 6 0 0 1 8.5 3H9.5"), line(seg(2.5, 9, 7, 9)),
            wheel(6, 18, 3), hub(6, 18),
            line(poly([(10, 12.5), (14, 17.5), (17, 9)], r=S.r * 0.5)), line(seg(12, 9, 15, 9)),
            line(seg(13.5, 9, 13.8, 12)),
            ring(19, 18, 2.5), line(seg(19, 18, 17.5, 7)), line(seg(16.5, 7, 19, 7))]


@veh("rickshaw", "Hand-pulled rickshaw with a hooded seat, a big wheel and long pulling shafts",
     ["pulled rickshaw", "jinrikisha", "hand cart", "rickshaw taxi", "traditional transport", "puller"],
     aliases=["pulled-rickshaw"])
def _(S):
    seat = poly([(3, 13), (3, 10), (11, 10), (11, 13)], closed=True, r=S.r * 0.5)
    return [shell(seat), line("M3 10V8A5 5 0 0 1 8 3H9"), wheel(8, 16.5, 4), hub(8, 16.5, 1.25),
            line(seg(11, 12, 21.5, 17)), line(seg(21.5, 17, 21.5, 20))]


@veh("jeepney", "Jeepney: a long jeep-style bus with a row of windows and an open rear entrance",
     ["jeepney", "philippines", "shared taxi", "public utility jeep", "minibus", "puj"])
def _(S):
    pts = [(2.5, 18), (2.5, 5.5), (15, 5.5), (15, 10.5), (21, 11), (21.5, 18)]
    ws = [(6, 18, 2), (18, 18, 2)]
    return auto(S, pts, ws, detail(seg(2.5, 10, 15, 10)), detail(seg(5.5, 5.5, 5.5, 18)),
                detail(seg(9, 5.5, 9, 10)), detail(seg(12, 5.5, 12, 10)), line(seg(9, 3, 16, 3)))


@T("self-balancing-scooter", "Two-wheeled self-balancing transporter with a tall handlebar column",
   ["personal transporter", "balancing scooter", "gyro scooter", "stand up scooter", "two wheeler", "tour scooter"],
   aliases=["personal-transporter"])
def _(S):
    k = L(S, 1.5, 2.5)
    return [shell(rect(2.5, 12, 5, 9, k)), shell(rect(16.5, 12, 5, 9, k)), line(seg(7.5, 16.5, 16.5, 16.5)),
            line(seg(12, 16.5, 12, 5)), line(seg(8, 4, 16, 4))]


@T("electric-unicycle", "Electric unicycle: one wheel in a rounded shell with fold-out pedals and a handle",
   ["euc", "e-unicycle", "self balancing unicycle", "monowheel", "personal transporter", "one wheel"],
   aliases=["euc"])
def _(S):
    return [shell(rect(8, 7, 8, 14, 4 if S.name == "rounded" else 3)), detail(seg(12, 10, 12, 18)),
            line(seg(2.5, 16, 8, 16)), line(seg(16, 16, 21.5, 16)),
            line(poly([(10, 7), (10, 3.5), (14, 3.5), (14, 7)], r=S.r * 0.5))]


@T("unicycle", "Unicycle with one spoked wheel, pedals at the hub and a seat on a tall post",
   ["one wheel", "circus", "juggling", "balance", "monocycle", "street performer"], aliases=["monocycle"])
def _(S):
    return [ring(12, 16, 5), line(seg(12, 16, 12, 5)), shell(poly([(8.5, 4.5), (8.5, 3), (15.5, 3), (15.5, 4.5)],
            closed=True, r=S.r * 0.3)), line(seg(12, 16, 14.5, 19)), line(seg(13, 19, 16, 19))]


@veh("covered-wagon", "Pioneer covered wagon with a canvas cover on hoops and big wheels",
     ["prairie schooner", "conestoga", "wagon", "wild west", "pioneer", "settler"], aliases=["prairie-schooner"])
def _(S):
    cover = "M3 12V8.5C3 5 5 4 7 4H13C15 4 17 5 17 8.5V12Z" if S.name != "rounded" else \
        "M3.5 12A0.5 0.5 0 0 1 3 11.5V8.5C3 5 5 4 7 4H13C15 4 17 5 17 8.5V11.5A0.5 0.5 0 0 1 16.5 12Z"
    bed = rect(3, 12, 14, 3, min(S.R, 1))
    return [shell(cover), detail(seg(8, 4.5, 8, 12)), detail(seg(12, 4.5, 12, 12)), shell(bed),
            wheel(6, 18, 3), wheel(15, 18, 3), hub(6, 18), hub(15, 18), line(seg(17, 14, 21.5, 17))]


@veh("chariot", "Ancient two-wheeled chariot with a curved front guard and a draught pole",
     ["roman chariot", "ancient", "racing chariot", "war chariot", "gladiator", "antiquity"])
def _(S):
    guard = poly([(4, 12.5), (4, 9.5), (9, 9.5), (12, 5), (14, 5), (14, 12.5)], closed=True, r=S.r)
    return [shell(guard), ring(9, 17, 4), dot(9, 17, 1.25), line(seg(9, 13, 9, 21)), line(seg(5, 17, 13, 17)),
            line(seg(14, 11, 21.5, 8))]


# =========================================================================== bicycles

def frame(S, R, B, St, H, F, k=0.5):
    """Diamond frame: rear hub R, bottom bracket B, seat cluster St, head H, front hub F."""
    return [line(poly([R, St, H, B], closed=True, r=S.r * k)), line(seg(*B, *St)), line(seg(*F, *H))]


def saddle(x, y, w=3.5):
    return line(seg(x - w / 2, y, x + w / 2, y))


@T("road-bike", "Road racing bicycle with thin tires and curled drop handlebars",
   ["racing bike", "road bicycle", "drop bars", "cycling", "road cycling", "racer"], aliases=["racing-bike"])
def _(S):
    R, F, B, St, H = (6, 17), (18, 17), (11, 17), (9.5, 9.5), (15.5, 9.5)
    return [ring(*R, 3.5), ring(*F, 3.5), *frame(S, R, B, St, H, F), line(seg(*H, 15, 7)), saddle(9.25, 6.5),
            line(seg(*St, 9.25, 6.5)), line("M15 7H18A1.75 1.75 0 0 1 18 10.5H17")]


@T("mountain-bike", "Mountain bike with a sloping top tube, suspension fork and flat handlebar",
   ["mtb", "mountain biking", "trail bike", "off road bike", "cycling", "downhill"], aliases=["mtb"])
def _(S):
    R, F, B, St, H = (6, 17), (18, 17), (11, 17), (9.5, 11), (15.5, 8.5)
    fork = [shell(poly([(15.3, 8.2), (17.3, 7.7), (18.4, 12.2), (16.4, 12.7)], closed=True, r=S.r * 0.3)),
            line(seg(17.4, 12.5, 18, 17))]
    return [ring(*R, 3.5), ring(*F, 3.5), dot(*R, 1), dot(*F, 1),
            line(poly([R, St, H, B], closed=True, r=S.r * 0.5)), line(seg(*B, *St)), *fork,
            line(seg(15.3, 8.2, 15, 5.5)), line(seg(13, 5.5, 17, 5.5)), saddle(8.75, 7), line(seg(*St, 9, 7))]


@T("bmx-bike", "Small BMX bike with raised handlebars and pegs on the hubs",
   ["bmx", "stunt bike", "freestyle", "bike tricks", "dirt jump", "skatepark"], aliases=["bmx"])
def _(S):
    R, F, B, St, H = (6, 17.5), (18, 17.5), (11.5, 17.5), (9.5, 12), (15, 11)
    return [ring(*R, 3), ring(*F, 3), *frame(S, R, B, St, H, F), line(seg(*H, 14, 4.5)), line(seg(12, 4.5, 16.5, 4.5)),
            line(seg(12.5, 7, 15.5, 7)), saddle(9, 9.5, 3), line(seg(*St, 9.25, 9.5)),
            solid(rect(4, 16.5, 4, 2, L(S, 0, 1))), solid(rect(16, 16.5, 4, 2, L(S, 0, 1)))]


@T("tandem-bicycle", "Tandem bicycle with two saddles and two sets of handlebars",
   ["tandem", "bicycle built for two", "two seater bike", "couple cycling", "stoker", "double bike"],
   aliases=["tandem"])
def _(S):
    R, F = (4.5, 17.5), (19.5, 17.5)
    B1, B2, S1, S2, H = (8, 17.5), (13, 17.5), (7, 10.5), (12, 10.5), (17, 10.5)
    return [ring(*R, 3), ring(*F, 3),
            line(poly([R, S1, H, B2, B1, R], r=S.r * 0.5)), line(seg(*B1, *S1)), line(seg(*B2, *S2)),
            line(seg(*F, *H)), line(seg(*H, 16.5, 7.5)), line(seg(15.5, 7.5, 18.5, 7.5)),
            saddle(6.75, 7.5, 3), line(seg(*S1, 6.75, 7.5)), saddle(11.75, 7.5, 3), line(seg(*S2, 11.75, 7.5)),
            line(seg(12.5, 9, 14, 9))]


@T("penny-farthing", "Victorian penny-farthing bicycle with a huge front wheel and a tiny rear wheel",
   ["high wheeler", "ordinary bicycle", "victorian bike", "vintage bicycle", "old bike", "antique bike"],
   aliases=["high-wheeler"])
def _(S):
    return [ring(14, 14, 7), dot(14, 14, 1.25), ring(4.5, 19.5, 1.75), line(seg(14, 14, 13.5, 4)),
            line(seg(11.5, 4, 17, 4)), line("M12 4.5C6.5 5 3.5 12 4.5 17.75")]


@T("recumbent-bicycle", "Low recumbent bicycle with a reclined seat and pedals out in front",
   ["recumbent", "bent", "laid back bike", "reclined bike", "long wheelbase", "comfort bike"],
   aliases=["recumbent"])
def _(S):
    return [ring(5.5, 17, 3.5), ring(19, 18, 2.5),
            line(poly([(3, 7.5), (7, 13.5), (12, 13.5)], r=S.r * 0.5)),
            line(poly([(5.5, 17), (9.5, 13.5), (20.5, 10.5)], r=S.r * 0.5)), line(seg(19, 18, 17, 11.3)),
            dot(20.5, 10.5, 1.5), line(seg(12, 13.5, 12, 11)), line(seg(10.5, 11, 13.5, 11))]


@T("cargo-bike", "Cargo bike with a big open box in front of the handlebars",
   ["box bike", "long john", "bakfiets", "cargo bicycle", "family bike", "delivery bike"], aliases=["box-bike"])
def _(S):
    R, B = (4.5, 17.5), (8.5, 17.5)
    return [ring(*R, 3), ring(18, 19, 2),
            line(poly([R, (6.5, 10.5), (10.5, 10.5), B, R], r=S.r * 0.5)), line(seg(*B, 6.5, 10.5)),
            saddle(6, 8, 3), line(seg(6.5, 10.5, 6.25, 8)),
            line(seg(10.5, 10.5, 10.5, 6.5)), line(seg(9, 6.5, 12.5, 6.5)),
            line(seg(*B, 18, 19)), line(poly([(12.5, 8.5), (12.5, 14), (21.5, 14), (21.5, 8.5)], r=S.r * 0.5))]


@T("folding-bike", "Folding bike folded in half with both small wheels side by side",
   ["folding bicycle", "folded bike", "commuter bike", "compact bike", "fold up bike"],
   aliases=["folded-bike"])
def _(S):
    return [ring(8, 16.5, 4), ring(16, 16.5, 4), line(seg(12, 13, 12, 5)), saddle(12, 4.5, 4.5),
            line(poly([(16, 16.5), (19.5, 9.5), (21.5, 9.5)], r=S.r * 0.5))]


@T("beach-cruiser-bike", "Beach cruiser bicycle with a swooping frame and swept-back handlebars",
   ["cruiser", "beach bike", "comfort bike", "retro bicycle", "boardwalk", "balloon tire bike"],
   aliases=["beach-cruiser"])
def _(S):
    R, F, B, St, H = (6, 17), (18, 17), (11, 17), (9, 10), (16, 10)
    return [ring(*R, 3.5), ring(*F, 3.5), line(poly([R, St, B], closed=True, r=S.r * 0.5)),
            line("M16 10C12.5 10 13 16 11 17"), line(seg(*St, 16, 10)), line(seg(*F, *H)),
            line("M16 10L15.5 6.5C14 6.5 13 5.5 12.5 5"), saddle(8.5, 7.5, 4), line(seg(*St, 8.75, 7.5))]


def annulus(x, y, ro, ri):
    return path_to_d(D(P(circle(x, y, ro)), P(circle(x, y, ri))))


@T("fat-tire-bike", "Fat bike with extremely wide balloon tires",
   ["fat bike", "fatbike", "snow bike", "sand bike", "wide tires", "balloon tires"], aliases=["fat-bike"])
def _(S):
    R, F, B, St, H = (6.5, 16.5), (17.5, 16.5), (11.5, 16.5), (9.5, 10), (15, 9.5)
    return [solid(annulus(*R, 4.25, 1.75)), solid(annulus(*F, 4.25, 1.75)),
            *frame(S, R, B, St, H, F), line(seg(*H, 14.5, 6.5)), line(seg(12.5, 6.5, 16.5, 6.5)),
            saddle(9, 7), line(seg(*St, 9.25, 7))]


@T("time-trial-bike", "Aerodynamic time trial bike with a solid disc rear wheel and aero bars",
   ["tt bike", "triathlon bike", "aero bike", "time trial", "disc wheel", "triathlon"], aliases=["tt-bike"])
def _(S):
    R, F, B, St, H = (6, 17), (18, 17), (11, 17), (9, 10), (16, 9)
    return [solid(annulus(*R, 4.5, 1)), ring(*F, 3.5), *frame(S, R, B, St, H, F),
            line(seg(*H, 21.5, 9)), saddle(8.5, 7.5, 3), line(seg(*St, 8.75, 7.5))]


@T("handcycle", "Handcycle with a reclined rider turning hand cranks",
   ["hand bike", "handbike", "adaptive cycling", "para cycling", "wheelchair sport", "accessible bike"],
   aliases=["handbike"])
def _(S):
    return [ring(5.5, 17, 3.5), ring(19.5, 18.5, 2.5), shell(circle(6.5, 5.5, 2)),
            line(poly([(7.5, 8.5), (9.5, 14), (18.5, 14.5)], r=S.r * 0.5)), line(seg(8.5, 11, 14.5, 9.5)),
            dot(15, 9.5, 1.5), line(seg(15, 9.5, 19.5, 18.5)), line(seg(5.5, 17, 9.5, 14))]


@veh("velomobile", "Velomobile: a pedal vehicle enclosed in a smooth teardrop shell",
     ["velo", "enclosed bike", "pedal car", "human powered vehicle", "hpv", "recumbent trike"],
     aliases=["pedal-car"])
def _(S):
    ws = [(6.5, 18, 2), (17.5, 18, 2)]
    if isF(S):
        b = [shell("M2.5 16.5C2.5 12 6 9.5 11 9.5C16.5 9.5 21.5 12.5 21.5 16.5Z")]
    else:
        e = "M4.5 16.5H2.5" if S.name == "line" else "M4.5 16.5H3.5A1 1 0 0 1 2.5 15.5"
        b = [shell(e + ("V16.5" if S.name == "line" else "") + "C2.5 12 6 9.5 11 9.5C16.5 9.5 21.5 12.5 21.5 16.5H19.5"),
             line(seg(8.5, 16.5, 15.5, 16.5))]
    return b + [wheel(*w) for w in ws] + [shell(circle(9, 6, 2))]
