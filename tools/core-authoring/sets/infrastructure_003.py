"""TypeIcon Core: infrastructure 003 (road signs, signals, roadside equipment, charging points).

Signs are drawn as a closed outline (the sign face) with a solid pictogram made of `dot` parts, so the Filled
style reads as a solid sign with a knocked-out symbol. Pictogram pieces use 1.4 to 1.7 px strokes because they
sit inside a 14 px window.
"""
import math
import re

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "infrastructure"


# --------------------------------------------------------------------------- helpers

def K(S):
    """Small corner radius for pictogram polygons (0 in Line, 1.2 in Rounded)."""
    return 0.8 * S.r


def sk(d, S, w=1.6):
    """Pictogram stroke: a stroked path turned into a solid region (knocked out in Filled)."""
    return Part("dot", path_to_d(ST(d, w, S.cap, S.join)))


def bl(pts, S, r=None):
    """Solid pictogram polygon."""
    return Part("dot", poly(pts, closed=True, r=K(S) if r is None else r))


def bc(cx, cy, r):
    return Part("dot", circle(cx, cy, r))


def br(x, y, w, h, rx=0.0):
    return Part("dot", rect(x, y, w, h, rx))


def ring_sign(S):
    return shell(circle(12, 12, 9))


def tri_sign(S, dy=0.0):
    return shell(poly([(12, 4 + dy), (21.5, 20 + dy), (2.5, 20 + dy)], closed=True, r=S.r))


def person(S, cx, top, h=10.0, w=1.5):
    """Walking pictogram figure (side view), top of head at `top`."""
    k = h / 10.0
    hx, hy = cx + 0.5 * k, top + 1.3 * k
    neck = (cx + 0.3 * k, top + 3.1 * k)
    hip = (cx - 0.2 * k, top + 6.2 * k)
    d = (f"M{fmt(neck[0])} {fmt(neck[1])}L{fmt(hip[0])} {fmt(hip[1])}"
         f"M{fmt(hip[0])} {fmt(hip[1])}L{fmt(cx - 2.3 * k)} {fmt(top + h)}"
         f"M{fmt(hip[0])} {fmt(hip[1])}L{fmt(cx + 2.0 * k)} {fmt(top + h - 0.3 * k)}"
         f"M{fmt(cx + 0.2 * k)} {fmt(top + 4.0 * k)}L{fmt(cx - 1.9 * k)} {fmt(top + 5.6 * k)}"
         f"M{fmt(cx + 0.2 * k)} {fmt(top + 4.0 * k)}L{fmt(cx + 2.4 * k)} {fmt(top + 5.6 * k)}")
    return [bc(hx, hy, 1.3 * k), sk(d, S, w)]


def bike(S, cx, cy, w=1.25, k=1.0):
    """Side-view bicycle about 12 k wide and 6 k tall, wheel hubs at cy."""
    def q(dx, dy):
        return (cx + dx * k, cy + dy * k)
    rh, fh, bb, seat, hd = q(-3.9, 0), q(3.9, 0), q(-0.2, 0), q(-1.7, -3.3), q(2.3, -3.3)
    wheels = "".join(circle(p[0], p[1], 2.3 * k) for p in (rh, fh))
    frame = (f"M{fmt(rh[0])} {fmt(rh[1])}L{fmt(seat[0])} {fmt(seat[1])}L{fmt(hd[0])} {fmt(hd[1])}"
             f"L{fmt(bb[0])} {fmt(bb[1])}L{fmt(rh[0])} {fmt(rh[1])}M{fmt(bb[0])} {fmt(bb[1])}L{fmt(seat[0])} {fmt(seat[1])}"
             f"M{fmt(hd[0])} {fmt(hd[1])}L{fmt(fh[0])} {fmt(fh[1])}M{fmt(hd[0] - 0.8 * k)} {fmt(hd[1] - 1.0 * k)}H{fmt(hd[0] + 1.0 * k)}"
             f"M{fmt(seat[0] - 0.8 * k)} {fmt(seat[1] - 1.0 * k)}H{fmt(seat[0] + 0.8 * k)}")
    return [sk(wheels, S, w), sk(frame, S, w)]


def head(S, tip, deg, ln=3.2, half=1.9):
    """Solid arrowhead with its tip at `tip`, pointing along `deg` (0 = right, 90 = down)."""
    a = math.radians(deg)
    dx, dy = math.cos(a), math.sin(a)
    bx, by = tip[0] - ln * dx, tip[1] - ln * dy
    px, py = -dy * half, dx * half
    return bl([tip, (bx + px, by + py), (bx - px, by - py)], S, 0.3 * S.r)


def car_pts(x, y, w=6.4, h=3.6):
    u = w / 6.4
    v = h / 3.6
    pts = [(0, 3.6), (0, 2.4), (1.5, 2.0), (2.3, 0.3), (4.2, 0.3), (5.2, 2.0), (6.4, 2.4), (6.4, 3.6)]
    return [(x + px * u, y + py * v) for px, py in pts]


def car_side(S, x, y, w=6.4, h=3.6):
    """Solid car silhouette (body plus two wheels) in a w x (h + 1.3) box at (x, y)."""
    u = w / 6.4
    body = poly(car_pts(x, y, w, h), closed=True, r=K(S))
    if w >= 8:
        v = h / 3.6
        win = poly([(x + 2.3 * u, y + 2.0 * v), (x + 2.8 * u, y + 0.85 * v), (x + 4.1 * u, y + 0.85 * v),
                    (x + 4.5 * u, y + 2.0 * v)], closed=True)
        body = path_to_d(D(P(body), P(win)))
    return [Part("dot", body), bc(x + 1.6 * u, y + h, 1.1), bc(x + 4.8 * u, y + h, 1.1)]


def car_out(S, x, y, w=6.4, h=3.6, sw=1.2):
    """Outlined car silhouette with solid wheels."""
    u = w / 6.4
    return [sk(poly(car_pts(x, y, w, h), closed=True), S, sw), bc(x + 1.6 * u, y + h, 1.1), bc(x + 4.8 * u, y + h, 1.1)]


def slash(S, a=(6.5, 6.5), b=(17.5, 17.5)):
    return detail(seg(a[0], a[1], b[0], b[1]))


# digits on a 3.6 x 6.4 cell, drawn as strokes
_DIG = {
    "0": "M0 0H3.6V6.4H0Z",
    "5": "M3.6 0H0.2L0 2.9H2.4Q3.6 2.9 3.6 4.4V4.9Q3.6 6.4 2.4 6.4H0",
    "7": "M0 0H3.6L1.4 6.4",
    "3": "M0 0H3.4L1.6 2.8Q3.6 2.8 3.6 4.6Q3.6 6.4 1.8 6.4H0",
    "4": "M2.6 6.4V0L0 4.4H3.8",
    "2": "M0 1.2Q0.4 0 1.8 0Q3.4 0 3.4 1.6Q3.4 2.6 2.4 3.6L0 6.4H3.6",
}


def _xf(d, x, y, sc):
    out = []
    for cmd, args in re.findall(r"([MLHVQZ])([^MLHVQZ]*)", d):
        nums = [float(n) for n in re.findall(r"-?\d*\.?\d+", args)]
        if cmd == "H":
            nums = [x + nums[0] * sc]
        elif cmd == "V":
            nums = [y + nums[0] * sc]
        else:
            nums = [(x + n * sc) if i % 2 == 0 else (y + n * sc) for i, n in enumerate(nums)]
        out.append(cmd + " ".join(fmt(n) for n in nums))
    return "".join(out)


def digits(S, text, x, y, gap=1.6, w=1.5, scale=1.0):
    """Stroked digits, left edge x, top y."""
    out = []
    cx = x
    for ch in text:
        out.append(sk(_xf(_DIG[ch], cx, y, scale), S, w))
        cx += 3.6 * scale + gap
    return out


# =========================================================================== charging

@icon("wallbox-charger", CAT, "A small charger box mounted on a wall with a coiled cable and a plug.",
      tags=["ev", "home charger", "wall charger", "electric car", "plug", "garage"])
def _(S):
    return [shell(rect(3, 2.5, 10, 12, min(S.R, 3))),
            bl([(8.5, 5), (5.5, 9.2), (7.7, 9.2), (6.8, 12.2), (10.5, 7.6), (8.3, 7.6), (9.5, 5)], S, 0),
            line("M8 14.5V16.75a3 3 0 0 0 3 3H16"),
            shell(rect(16, 17.5, 5, 4.5, min(S.R, 1.5)))]


@icon("fast-charger", CAT, "A tall charging pillar with a lightning bolt and a hose ending in a plug.",
      tags=["dc fast charging", "rapid charger", "ev", "electric car", "supercharger", "pillar"])
def _(S):
    return [shell(rect(3.5, 2.5, 10, 19, min(S.R, 3))),
            bl([(8.6, 5.5), (5.6, 11.2), (8, 11.2), (6.8, 17), (11.4, 9.6), (9, 9.6), (10.2, 5.5)], S, 0),
            line("M13.5 8h3.5a2.5 2.5 0 0 1 2.5 2.5V16"),
            shell(rect(18, 16, 3, 5.5, min(S.R, 1.5)))]


@icon("wireless-car-charging", CAT, "A car above a charging pad on the ground with waves rising between them.",
      tags=["inductive charging", "ev", "electric car", "pad", "parking", "contactless"])
def _(S):
    return [shell(poly([(2.5, 8.5), (2.5, 7), (4.5, 7), (7, 2.5), (17, 2.5), (19.5, 7), (21.5, 7), (21.5, 8.5)],
                       closed=True, r=S.r)),
            bc(7, 9, 1.8), bc(17, 9, 1.8),
            sk("M8 16.2c-1.5-1.2 1.5-2.4 0-3.8M12 16.2c-1.5-1.2 1.5-2.4 0-3.8M16 16.2c-1.5-1.2 1.5-2.4 0-3.8", S, 1.4),
            shell(rect(3, 18, 18, 3, min(S.R, 1.5)))]


@icon("battery-swap-station", CAT, "A station frame with a battery inside and swap arrows above it.",
      tags=["battery exchange", "ev", "electric car", "swap", "replace battery", "charging"])
def _(S):
    return [line("M2.5 21V3.5h19V21"),
            shell(rect(5.5, 13, 11, 7, min(S.R, 1.5))), br(17.8, 14.8, 1.6, 3.4),
            sk("M7 7.2H16M14.2 5.4L16.2 7.2L14.2 9", S, 1.4), sk("M17 10.6H8M9.8 8.8L7.8 10.6L9.8 12.4", S, 1.4)]


@icon("yield-sign", CAT, "An inverted triangle sign on a post telling drivers to give way.",
      tags=["give way", "priority", "traffic sign", "road sign", "triangle", "junction"])
def _(S):
    return [shell(poly([(3, 4), (21, 4), (12, 17.5)], closed=True, r=S.r)),
            bl([(8.2, 7.4), (15.8, 7.4), (12, 12.8)], S),
            line("M12 17.5V21.5")]


@icon("no-entry-sign", CAT, "A round sign with a solid bar across the middle closing a road to traffic.",
      tags=["do not enter", "traffic sign", "road sign", "one way", "wrong way", "forbidden"])
def _(S):
    return [ring_sign(S), br(5.5, 10.3, 13, 3.4, 1.7 if S.name == 'rounded' else 0)]


@icon("one-way-sign", CAT, "A rectangular sign on a post with a long arrow showing the only allowed direction.",
      tags=["direction", "traffic sign", "road sign", "arrow", "street", "single direction"])
def _(S):
    return [shell(rect(2.5, 3, 19, 11, min(S.R, 2))),
            bl([(5.5, 7.4), (13.5, 7.4), (13.5, 5.2), (18.5, 8.5), (13.5, 11.8), (13.5, 9.6), (5.5, 9.6)], S),
            line("M12 14v7.5")]


@icon("speed-limit-sign", CAT, "A round sign with the number 50 showing the maximum allowed speed.",
      tags=["speed", "maximum speed", "traffic sign", "road sign", "50", "limit", "kmh"])
def _(S):
    return [ring_sign(S)] + digits(S, "50", 6.95, 8.3, gap=1.8, w=1.6, scale=1.15)


@icon("no-parking-sign", CAT, "A round sign with a letter P crossed by a diagonal slash.",
      tags=["parking ban", "traffic sign", "road sign", "forbidden", "car park", "prohibited"])
def _(S):
    return [ring_sign(S), sk("M9.8 17V7H13.3a3 3 0 0 1 0 6H9.8", S, 1.8), slash(S)]


@icon("no-stopping-sign", CAT, "A round sign with two crossing diagonal slashes forbidding any stopping.",
      tags=["no standing", "clearway", "traffic sign", "road sign", "forbidden", "red cross"])
def _(S):
    return [ring_sign(S), detail(seg(7, 7, 17, 17)), detail(seg(17, 7, 7, 17))]


@icon("no-overtaking-sign", CAT, "A round sign with two cars side by side, one outlined and one solid.",
      tags=["no passing", "overtake", "traffic sign", "road sign", "cars", "prohibited"])
def _(S):
    return [ring_sign(S)] + car_out(S, 4.9, 9.2, 6.2, 4.0) + car_side(S, 12.9, 9.2, 6.2, 4.0)


@icon("no-u-turn-sign", CAT, "A round sign with a U-shaped arrow crossed by a diagonal slash.",
      tags=["u turn", "turn around", "traffic sign", "road sign", "forbidden", "prohibited"])
def _(S):
    return [ring_sign(S), sk("M9.5 17V10.5a2.75 2.75 0 0 1 5.5 0V13.5", S, 1.6),
            bl([(12.8, 13.4), (17.2, 13.4), (15, 17)], S), slash(S, (6.6, 6.6), (17.4, 17.4))]


@icon("no-pedestrians-sign", CAT, "A round sign with a walking figure in a ring closing a road to people on foot.",
      tags=["no walking", "no foot traffic", "traffic sign", "road sign", "person", "prohibited"])
def _(S):
    return [ring_sign(S)] + person(S, 12, 6.3, 11.4, 1.6)


@icon("no-cycling-sign", CAT, "A round sign with a bicycle in a ring closing a road to cyclists.",
      tags=["no bikes", "no bicycles", "traffic sign", "road sign", "bike", "prohibited"])
def _(S):
    return [ring_sign(S)] + bike(S, 12, 13.6, 1.3)


@icon("no-trucks-sign", CAT, "A round sign with a truck in side view closing a road to heavy goods vehicles.",
      tags=["no lorries", "no hgv", "heavy vehicles", "traffic sign", "road sign", "prohibited"])
def _(S):
    return [ring_sign(S), br(5.3, 8.2, 7.4, 5.8, 0.4 * S.r),
            bl([(13.4, 9.6), (16.4, 9.6), (18.7, 12.3), (18.7, 14), (13.4, 14)], S),
            bc(8.2, 14.9, 1.35), bc(15.6, 14.9, 1.35)]


# =========================================================================== more order signs

@icon("no-motor-vehicles-sign", CAT, "A round sign with a car above a motorcycle closing a road to motor traffic.",
      tags=["no cars", "no motorcycles", "traffic sign", "road sign", "vehicles", "prohibited"])
def _(S):
    wheels = circle(8.8, 15.1, 1.9) + circle(15.2, 15.1, 1.9)
    return ([ring_sign(S)] + car_side(S, 7.2, 5.4, 9.6, 3.0)
            + [sk(wheels, S, 1.3), sk("M8.8 15.1L10.4 12.8M14.2 12.4L15.2 15.1M14.2 12.4L13.6 11.2H15.6", S, 1.3),
               bl([(9.6, 13.2), (11, 11.8), (13.8, 11.8), (14.2, 13.2), (12.8, 14.8), (10.8, 14.8)], S, 0.6)])


@icon("no-horn-sign", CAT, "A round sign with a bulb horn crossed by a diagonal slash asking drivers to stay quiet.",
      tags=["no honking", "quiet zone", "silence", "traffic sign", "road sign", "prohibited", "noise"])
def _(S):
    return [ring_sign(S), bc(7.9, 12, 2.5), br(9.8, 10.9, 2.4, 2.2),
            bl([(11.6, 10.4), (17, 7.6), (17, 16.4), (11.6, 13.6)], S), slash(S, (6.2, 6.2), (17.8, 17.8))]


@icon("height-limit-sign", CAT, "A round sign with two triangles pointing at each other above and below a number.",
      tags=["max height", "low bridge", "clearance", "vertical limit", "traffic sign", "road sign"])
def _(S):
    return ([ring_sign(S), bl([(9.7, 5.4), (14.3, 5.4), (12, 8.6)], S, 0.3 * S.r), bl([(9.7, 18.6), (14.3, 18.6), (12, 15.4)], S, 0.3 * S.r)]
            + digits(S, "3", 10.6, 9.4, w=1.4, scale=0.85))


@icon("width-limit-sign", CAT, "A round sign with two triangles pointing at each other either side of a number.",
      tags=["max width", "narrow road", "clearance", "horizontal limit", "traffic sign", "road sign"])
def _(S):
    return ([ring_sign(S), bl([(5.4, 9.7), (5.4, 14.3), (8.6, 12)], S, 0.3 * S.r), bl([(18.6, 9.7), (18.6, 14.3), (15.4, 12)], S, 0.3 * S.r)]
            + digits(S, "3", 10.6, 9.4, w=1.4, scale=0.85))


@icon("weight-limit-sign", CAT, "A round sign with the number 5 and a small letter t for the maximum weight in tonnes.",
      tags=["max weight", "tonnes", "tons", "load limit", "bridge", "traffic sign", "road sign"])
def _(S):
    t = "M1 -0.2V4.3Q1 5.4 2.2 5.4H2.9M-0.1 1.7H2.6"
    return ([ring_sign(S)] + digits(S, "5", 6.4, 8.8, w=1.6)
            + [sk(_xf(t, 12.4, 10.1, 1.0), S, 1.5)])


@icon("priority-road-sign", CAT, "A diamond sign with a smaller solid diamond inside marking a road with right of way.",
      tags=["right of way", "main road", "traffic sign", "road sign", "diamond", "yellow diamond"])
def _(S):
    return [shell(poly([(12, 2.5), (21.5, 12), (12, 21.5), (2.5, 12)], closed=True, r=S.r)),
            bl([(12, 7.3), (16.7, 12), (12, 16.7), (7.3, 12)], S)]


@icon("roundabout-sign", CAT, "A round sign with three arrows chasing each other around a circle.",
      tags=["traffic circle", "rotary", "gyratory", "traffic sign", "road sign", "circulation"])
def _(S):
    out = [ring_sign(S)]
    for a0 in (-90, 30, 150):
        out.append(sk(arc(12, 12, 4.8, a0, a0 + 62), S, 1.5))
        tip = polar(12, 12, 4.8, a0 + 62 + 24)
        out.append(head(S, tip, a0 + 62 + 24 + 90 - 8, 3.0, 1.9))
    return out


@icon("pass-either-side-sign", CAT, "A round sign with a stem splitting into two arrows that pass either side.",
      tags=["keep left or right", "island", "obstacle", "traffic sign", "road sign", "split", "divide"])
def _(S):
    return [ring_sign(S), sk("M12 6V10.5M12 10.5L8.6 13.4M12 10.5L15.4 13.4", S, 1.6),
            head(S, (7.3, 16.2), 130, 3.4, 2.0), head(S, (16.7, 16.2), 50, 3.4, 2.0)]


# =========================================================================== warning signs

@icon("pedestrian-crossing-sign", CAT, "A triangle warning sign with a walking figure above zebra stripes.",
      tags=["zebra crossing", "crosswalk", "warning sign", "road sign", "pedestrian", "people crossing"])
def _(S):
    return ([tri_sign(S)] + person(S, 12, 9.4, 6.4, 1.3)
            + [br(7.3, 16.7, 2, 1.8), br(11, 16.7, 2, 1.8), br(14.7, 16.7, 2, 1.8)])


@icon("children-crossing-sign", CAT, "A triangle warning sign with two small running figures, one carrying a bag.",
      tags=["school", "kids", "warning sign", "road sign", "children", "playground", "watch for children"])
def _(S):
    return (person(S, 9.6, 11.6, 6.6, 1.3) + person(S, 14.6, 12.4, 5.8, 1.2)
            + [tri_sign(S), br(16.3, 15.6, 1.7, 1.7)])


@icon("cyclist-warning-sign", CAT, "A triangle warning sign with a bicycle in side view.",
      tags=["cyclists", "bike lane", "warning sign", "road sign", "bicycle", "watch for cyclists"])
def _(S):
    return [tri_sign(S)] + bike(S, 12, 16.4, 1.2, 0.8)


@icon("deer-crossing-sign", CAT, "A triangle warning sign with a leaping deer with antlers.",
      tags=["wildlife", "animal crossing", "warning sign", "road sign", "stag", "game", "watch for deer"])
def _(S):
    return [tri_sign(S), sk("M6.7 16.4L11.7 15.4", S, 2.4), sk("M11.7 15.4L13.2 12.9", S, 1.7), bc(14, 12.3, 1.0),
            sk("M13.2 11.3L12.6 9.8M13.5 11L14.6 10.3", S, 1.1),
            sk("M11.2 15.6L13.8 17.8M7 16.8L5.7 18.6", S, 1.4)]


@icon("cattle-crossing-sign", CAT, "A triangle warning sign with a cow in side view.",
      tags=["livestock", "farm animals", "warning sign", "road sign", "cow", "bull", "watch for cattle"])
def _(S):
    return [tri_sign(S), br(8.4, 13.6, 7.2, 3.2, 0.8 * S.r),
            bl([(6.6, 13.8), (8.6, 13.8), (8.6, 16.8), (7.2, 16.8), (6.6, 15.4)], S),
            sk("M6.9 13.6L6.4 12.3M8.3 13.6L8.8 12.4", S, 1.0),
            sk("M9.4 16.6V18.7M14.6 16.6V18.7", S, 1.5), sk("M15.6 14L16.6 15.6", S, 1.0)]


@icon("horse-rider-sign", CAT, "A triangle warning sign with a person riding a horse.",
      tags=["equestrian", "riders", "bridleway", "warning sign", "road sign", "horse", "watch for horses"])
def _(S):
    return [tri_sign(S), bc(11.6, 9.9, 1.0), sk("M11.6 11.2L11.2 13.8M11.6 12L14 12.9", S, 1.3),
            br(7.6, 13.8, 7.4, 2.6, 0.8 * S.r),
            bl([(13.8, 14.2), (14.6, 12.4), (16.8, 13.2), (16.8, 14.2), (15.4, 14.6)], S, 0.3 * S.r),
            sk("M8.6 16V18.7M14 16V18.7", S, 1.4), sk("M7.8 14.2L6.4 16", S, 1.0)]


@icon("elderly-crossing-sign", CAT, "A triangle warning sign with two bent figures, one walking with a cane.",
      tags=["seniors", "older people", "retirement", "warning sign", "road sign", "care home", "walking stick"])
def _(S):
    def bent(cx, top):
        return [bc(cx + 1.0, top + 1.0, 1.0),
                sk(f"M{fmt(cx + 0.4)} {fmt(top + 2.4)}L{fmt(cx - 0.8)} {fmt(top + 4.8)}"
                   f"M{fmt(cx - 0.8)} {fmt(top + 4.8)}L{fmt(cx - 1.7)} {fmt(top + 7.3)}"
                   f"M{fmt(cx - 0.8)} {fmt(top + 4.8)}L{fmt(cx + 0.8)} {fmt(top + 7.3)}"
                   f"M{fmt(cx + 0.2)} {fmt(top + 3.2)}L{fmt(cx + 1.6)} {fmt(top + 4.3)}", S, 1.3)]
    return [tri_sign(S)] + bent(9.2, 11.3) + bent(15, 11.6) + [sk("M12 14.2V18.8", S, 1.1)]


@icon("slippery-road-sign", CAT, "A triangle warning sign with a car seen from behind and two wavy skid marks below it.",
      tags=["skid", "wet road", "ice", "warning sign", "road sign", "low grip", "aquaplaning"])
def _(S):
    return [tri_sign(S),
            bl([(9.2, 14.4), (9.2, 12.4), (10, 12.2), (10.6, 10.3), (13.4, 10.3), (14, 12.2), (14.8, 12.4), (14.8, 14.4)], S),
            sk("M9.8 15.2C8.3 16.2 11.3 17 9.8 18.4M14.2 15.2C12.7 16.2 15.7 17 14.2 18.4", S, 1.3)]


@icon("falling-rocks-sign", CAT, "A triangle warning sign with a steep slope and rocks tumbling down it.",
      tags=["rockfall", "landslide", "boulders", "warning sign", "road sign", "cliff", "debris"])
def _(S):
    return [tri_sign(S), sk("M7.6 13.8L17.4 18.6", S, 1.6), bc(11.4, 11.4, 1.3), bc(14.4, 14.3, 1.1), bc(10.7, 14.3, 0.9)]


@icon("steep-hill-sign", CAT, "A triangle warning sign with a slope wedge and a small percent sign.",
      tags=["gradient", "incline", "descent", "warning sign", "road sign", "hill", "slope"])
def _(S):
    return [tri_sign(S), bl([(6.4, 18.4), (17.6, 18.4), (17.6, 14.2)], S),
            bc(10.4, 11.2, 0.8), bc(13.2, 13.2, 0.8), sk("M13 10.8L10.6 13.6", S, 1.0)]


@icon("curve-ahead-sign", CAT, "A triangle warning sign with a single road arrow bending sharply to the right.",
      tags=["bend", "turn", "corner", "warning sign", "road sign", "right curve", "arrow"])
def _(S):
    return [tri_sign(S), sk("M8.4 18.7V15.6Q8.4 13.7 10.4 13.7H12.6", S, 1.8), head(S, (16, 13.7), 0, 3.2, 2.0)]


@icon("double-bend-sign", CAT, "A triangle warning sign with an S-shaped road arrow.",
      tags=["s bend", "winding road", "chicane", "warning sign", "road sign", "bends", "curves"])
def _(S):
    return [tri_sign(S), sk("M9 18.7C9 15.4 14.4 16.4 14.4 13.6", S, 1.8), head(S, (14.4, 10.3), -90, 3.4, 1.8)]


@icon("road-narrows-sign", CAT, "A triangle warning sign with two road edges pinching inward toward the top.",
      tags=["narrow road", "lane reduction", "carriageway", "warning sign", "road sign", "squeeze", "bottleneck"])
def _(S):
    return [tri_sign(S), sk("M6.4 18.6L10.6 11", S, 1.7), sk("M17.6 18.6L13.4 11", S, 1.7)]


@icon("two-way-traffic-sign", CAT, "A triangle warning sign with one arrow pointing up and one pointing down side by side.",
      tags=["oncoming traffic", "dual direction", "warning sign", "road sign", "opposite lanes", "arrows"])
def _(S):
    return [tri_sign(S), sk("M9.8 18.6V13", S, 1.6), head(S, (9.8, 10.6), -90, 3.4, 1.9),
            sk("M14.2 11.4V16.2", S, 1.6), head(S, (14.2, 18.8), 90, 3.4, 1.9)]


@icon("traffic-signals-sign", CAT, "A triangle warning sign with a small upright three-lamp traffic light.",
      tags=["traffic lights", "stoplight", "ahead", "warning sign", "road sign", "junction", "signals ahead"])
def _(S):
    return [tri_sign(S), sk(rect(9.6, 10.6, 4.8, 8.2, 0.8 * S.r), S, 1.3),
            bc(12, 12.6, 0.85), bc(12, 14.7, 0.85), bc(12, 16.8, 0.85)]


@icon("uneven-road-sign", CAT, "A triangle warning sign with a bumpy road profile line.",
      tags=["bumps", "rough surface", "potholes", "warning sign", "road sign", "damaged road", "washboard"])
def _(S):
    return [tri_sign(S), sk("M5.6 17.8H8.4Q9.6 13.8 11 17.8H13Q13.9 15.4 14.8 17.8H18.4", S, 1.7)]


@icon("speed-bump-sign", CAT, "A triangle warning sign with a single rounded hump on a base line.",
      tags=["speed hump", "traffic calming", "sleeping policeman", "warning sign", "road sign", "ramp", "slow down"])
def _(S):
    return [tri_sign(S), Part("dot", "M7.4 17.4Q12 9.8 16.6 17.4Z"), sk("M5.8 18H18.2", S, 1.4)]


@icon("crosswind-sign", CAT, "A triangle warning sign with a windsock streaming sideways from a pole.",
      tags=["strong wind", "gusts", "windsock", "warning sign", "road sign", "weather", "bridge exposed"])
def _(S):
    return [tri_sign(S), sk("M8.6 18.7V11.8", S, 1.4),
            bl([(9.3, 12.2), (9.3, 15.4), (15.6, 14.6), (15.6, 13)], S, 0.4 * S.r)]


def rot_pts(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


@icon("low-flying-aircraft-sign", CAT, "A triangle warning sign with an aeroplane seen from above.",
      tags=["airport nearby", "aircraft", "plane", "warning sign", "road sign", "runway", "flight path"])
def _(S):
    return [tri_sign(S), sk("M12 10.6V18.2", S, 1.7),
            bl([(12, 13), (17.4, 16.4), (17.4, 17.6), (12, 15.8), (6.6, 17.6), (6.6, 16.4)], S, 0.3 * S.r),
            bl([(12, 16.8), (14.4, 18.8), (9.6, 18.8)], S, 0.3 * S.r)]


@icon("tram-crossing-sign", CAT, "A triangle warning sign with the front of a tram and its overhead pole.",
      tags=["streetcar", "light rail", "trolley", "warning sign", "road sign", "tram tracks", "trams ahead"])
def _(S):
    return [tri_sign(S), sk(rect(8.8, 12.4, 6.4, 5.8, 0.8 * S.r), S, 1.3), sk("M9.4 14.6H14.6", S, 1.2),
            bc(10.6, 16.3, 0.7), bc(13.4, 16.3, 0.7), sk("M12 12.4V10.4", S, 1.2)]


@icon("level-crossing-sign", CAT, "A triangle warning sign with an old steam locomotive in side view.",
      tags=["railway crossing", "train", "rail", "warning sign", "road sign", "steam engine", "railroad"])
def _(S):
    return [tri_sign(S), br(7.6, 13.8, 6.4, 3.2, 0.6 * S.r), br(9.2, 11.9, 1.6, 2.2), br(13.4, 12.6, 2.4, 4.4, 0.5 * S.r),
            bc(9.2, 17.8, 1.2), bc(12.4, 17.8, 1.2), bc(15, 17.8, 1.0)]


@icon("quayside-sign", CAT, "A triangle warning sign with a car tipping off a quay edge into waves.",
      tags=["waterfront", "dock edge", "harbour", "warning sign", "road sign", "pier", "water ahead"])
def _(S):
    car = rot_pts(car_pts(9.4, 10.6, 6, 2.8), 28, 12.4, 12)
    return [tri_sign(S), sk("M7.4 14.4H10.6V18.6", S, 1.5), bl(car, S),
            sk("M12.4 17.6Q13.4 16.6 14.4 17.6T16.4 17.6", S, 1.2)]


@icon("loose-gravel-sign", CAT, "A triangle warning sign with a car flicking up small stones behind it.",
      tags=["loose chippings", "stones", "debris", "warning sign", "road sign", "gravel road", "flying stones"])
def _(S):
    return ([tri_sign(S)] + car_side(S, 10, 14.2, 7, 3)
            + [bc(8.4, 14.4, 0.7), bc(7.8, 17, 0.65), bc(9.4, 18.3, 0.6), bc(9.6, 12.7, 0.6)])


@icon("icy-road-sign", CAT, "A triangle warning sign with a large snowflake.",
      tags=["ice", "frost", "snow", "winter", "warning sign", "road sign", "freezing", "black ice"])
def _(S):
    return [tri_sign(S), sk("M12 11.2V18.8M8.6 13.1L15.4 16.9M15.4 13.1L8.6 16.9", S, 1.4)]


@icon("queues-likely-sign", CAT, "A triangle warning sign with three cars seen from behind in a row.",
      tags=["traffic jam", "congestion", "tailback", "warning sign", "road sign", "slow traffic", "queue"])
def _(S):
    def rear(x):
        return bl([(x - 1.6, 18.6), (x - 1.6, 16.6), (x - 0.9, 14.6), (x + 0.9, 14.6), (x + 1.6, 16.6), (x + 1.6, 18.6)],
                  S, 0.3 * S.r)
    return [tri_sign(S), rear(8.4), rear(12), rear(15.6)]


@icon("merging-traffic-sign", CAT, "A triangle warning sign with a straight road and a side road joining at an angle.",
      tags=["merge", "slip road", "junction", "warning sign", "road sign", "side road", "on ramp"])
def _(S):
    return [tri_sign(S), sk("M10.4 18.8V10.8", S, 1.8), sk("M16 18.8L10.8 13.8", S, 1.8)]


@icon("lane-ends-sign", CAT, "A triangle warning sign with two lanes where the right lane bends into the left.",
      tags=["lane closure", "lane reduction", "merge left", "warning sign", "road sign", "carriageway narrows"])
def _(S):
    return [tri_sign(S), sk("M8.6 18.8V11.4", S, 1.7), sk("M15.4 18.8V16L10.4 11.6", S, 1.7)]


@icon("opening-bridge-sign", CAT, "A triangle warning sign with a bascule bridge raised in the middle.",
      tags=["drawbridge", "lifting bridge", "swing bridge", "warning sign", "road sign", "canal", "bridge opens"])
def _(S):
    return [tri_sign(S), sk("M5.8 18.6H8.6M15.4 18.6H18.2", S, 1.5),
            bl([(8.8, 18.6), (10.3, 12.2), (11.5, 12.2), (11, 18.6)], S, 0.3 * S.r),
            bl([(15.2, 18.6), (13.7, 12.2), (12.5, 12.2), (13, 18.6)], S, 0.3 * S.r)]


# =========================================================================== information signs

def sq_sign(S):
    return shell(rect(3, 3, 18, 18, S.R))


@icon("dead-end-sign", CAT, "A square sign with a T shape showing a road with no through route.",
      tags=["no through road", "cul de sac", "road ends", "traffic sign", "road sign", "blind alley", "no exit"])
def _(S):
    return [sq_sign(S), bl([(7.6, 7), (16.4, 7), (16.4, 9.6), (13.3, 9.6), (13.3, 17.4), (10.7, 17.4), (10.7, 9.6), (7.6, 9.6)], S, 0)]


@icon("motorway-sign", CAT, "A square sign showing a road running under a bridge in perspective.",
      tags=["highway", "freeway", "expressway", "traffic sign", "road sign", "overpass", "underpass", "autobahn"])
def _(S):
    return [sq_sign(S), br(6.2, 6.8, 11.6, 2.4, 0.5 * S.r), sk("M6.6 18L10.4 10.6M17.4 18L13.6 10.6", S, 1.7)]


@icon("pedestrian-zone-sign", CAT, "A round sign with an adult and a child walking hand in hand.",
      tags=["walking area", "car free", "traffic sign", "road sign", "family", "foot street", "shopping street"])
def _(S):
    return ([ring_sign(S)] + person(S, 9.2, 7.6, 9.6, 1.5) + person(S, 15, 11.4, 6.2, 1.3)
            + [sk("M11 12.6L14 13.8", S, 1.1)])


@icon("shared-path-sign", CAT, "A round sign split by a line with a walking figure on one half and a bicycle on the other.",
      tags=["shared use", "cycle and foot path", "greenway", "traffic sign", "road sign", "pedestrians and cyclists"])
def _(S):
    return ([ring_sign(S), detail(seg(12, 3.5, 12, 20.5))] + person(S, 7.9, 8, 8.6, 1.3)
            + bike(S, 16.6, 13.8, 1.0, 0.5))


@icon("bicycle-route-sign", CAT, "A rectangular sign with a bicycle and a small route number.",
      tags=["cycle route", "bike path", "cycleway", "traffic sign", "road sign", "national cycle network", "bike lane"])
def _(S):
    return [shell(rect(2.5, 4, 19, 16, S.R))] + bike(S, 9, 13.6, 1.3, 0.75) + digits(S, "7", 15.4, 9.9, w=1.4, scale=0.85)


@icon("hospital-sign", CAT, "A square sign with a bold letter H and a small bed below it.",
      tags=["medical", "emergency room", "healthcare", "traffic sign", "road sign", "clinic", "hospital ahead"])
def _(S):
    return [sq_sign(S), sk("M8.4 6.2V13M15.6 6.2V13M8.4 9.6H15.6", S, 2.0),
            sk("M6.4 14.8V18.2M6.4 16.8H17.6V18.2", S, 1.4), bc(8.6, 15.4, 0.9)]


@icon("detour-sign", CAT, "A rectangular sign with a bent arrow and a bar standing for the word DETOUR.",
      tags=["diversion", "alternative route", "temporary route", "traffic sign", "road sign", "roadworks", "redirect"])
def _(S):
    return [shell(rect(2.5, 4, 19, 16, S.R)), sk("M7 14.2V11.2Q7 9 9.2 9H13", S, 1.8), head(S, (17.6, 9), 0, 3.4, 2.1),
            br(6.4, 16, 11.2, 1.6, 0.5 * S.r)]


@icon("road-closed-sign", CAT, "A rectangular sign on a barricade with bars standing for the words ROAD CLOSED.",
      tags=["road closure", "barrier", "no through traffic", "traffic sign", "road sign", "barricade", "roadworks"])
def _(S):
    return [shell(rect(2.5, 2.8, 19, 8.2, min(S.R, 2))), br(6, 5.4, 12, 1.4, 0.4 * S.r), br(6, 7.8, 8, 1.2, 0.4 * S.r),
            shell(rect(4, 14.4, 16, 4, min(S.R, 1.5))), line("M7.4 11V14.4M16.6 11V14.4M7.4 18.4V21.6M16.6 18.4V21.6")]


@icon("speed-camera-sign", CAT, "A square sign with an old box camera silhouette.",
      tags=["radar", "enforcement", "photo enforced", "traffic sign", "road sign", "speeding", "camera ahead"])
def _(S):
    return [sq_sign(S), sk(rect(6.6, 9.4, 10.8, 7, 1 if S.name == "rounded" else 0), S, 1.4), bc(12, 12.9, 1.9),
            br(9.4, 6.6, 2.6, 1.8), br(14.4, 6.8, 1.8, 1.6)]


@icon("chevron-alignment-sign", CAT, "A rectangular sign with three bold chevrons pointing one way.",
      tags=["sharp bend marker", "direction markers", "curve guidance", "traffic sign", "road sign", "arrows", "chevrons"])
def _(S):
    return [shell(rect(2.5, 4, 19, 16, S.R)), sk("M5.8 8L9.6 12L5.8 16M10 8L13.8 12L10 16M14.2 8L18 12L14.2 16", S, 1.7)]


@icon("exit-number-sign", CAT, "A rectangular highway sign with a small tab on top and a two digit exit number.",
      tags=["junction number", "slip road", "highway", "traffic sign", "road sign", "interchange", "off ramp"])
def _(S):
    return ([shell(poly([(2.5, 7), (8, 7), (8, 3.6), (16, 3.6), (16, 7), (21.5, 7), (21.5, 20.4), (2.5, 20.4)],
                        closed=True, r=S.r))]
            + digits(S, "24", 7.2, 10.6, w=1.6, scale=1.1))


@icon("route-shield", CAT, "A shield shaped highway marker with a route number in the middle.",
      tags=["highway number", "route marker", "road number", "traffic sign", "road sign", "interstate", "road shield"])
def _(S):
    return ([shell(poly([(4, 5.4), (12, 2.8), (20, 5.4), (20, 13.6), (12, 21.2), (4, 13.6)], closed=True, r=S.r))]
            + digits(S, "25", 7.4, 7.6, w=1.6, scale=1.05))


@icon("school-zone-sign", CAT, "A pentagon shaped sign with two small walking children.",
      tags=["school crossing", "kids", "traffic sign", "road sign", "children", "education", "school ahead"])
def _(S):
    return ([shell(poly([(12, 2.8), (21, 8.6), (21, 20.4), (3, 20.4), (3, 8.6)], closed=True, r=S.r))]
            + person(S, 9.4, 9.8, 7.4, 1.3) + person(S, 14.8, 10.8, 6.4, 1.3))


@icon("low-emission-zone-sign", CAT, "A round sign with a car and a small leaf inside a ring.",
      tags=["clean air zone", "green zone", "eco", "traffic sign", "road sign", "pollution", "ulez"])
def _(S):
    return ([ring_sign(S)] + car_side(S, 5.6, 11.8, 8.4, 3.2)
            + [Part("dot", "M13.4 11.2Q12.8 6.2 18.4 5.8Q19 11.4 13.4 11.2Z") if S.name == "rounded"
               else bl([(13.2, 11.4), (13.2, 8), (16.2, 5.8), (18.8, 5.8), (18.8, 8.6), (16.4, 11.4)], S, 0)])


# =========================================================================== signals and roadside equipment

def head_box(S, x=6.5, y=2.5, w=11, h=19):
    return shell(rect(x, y, w, h, min(S.R, 3)))


@icon("variable-message-sign", CAT, "An overhead electronic panel on legs with a warning triangle and rows of dotted text.",
      tags=["vms", "matrix sign", "electronic sign", "motorway sign", "roadside display", "traffic information", "led board"])
def _(S):
    dots = [bc(x, y, 0.8) for y in (8.4, 11.6) for x in (13.6, 15.8, 18)]
    return ([shell(rect(2.5, 3.5, 19, 12.5, min(S.R, 2))), bl([(9, 6.8), (11.6, 11.6), (6.4, 11.6)], S, 0.3 * S.r),
             line("M7 16V21.5M17 16V21.5")] + dots)


@icon("direction-gantry", CAT, "An overhead steel frame spanning a road holding two direction boards with arrows.",
      tags=["sign gantry", "overhead sign", "highway sign", "motorway", "lane guidance", "road directions", "sign bridge"])
def _(S):
    return [line("M3 21.5V4H21V21.5"), shell(rect(5.4, 8, 5.6, 6, 0.8 * S.r)), shell(rect(13, 8, 5.6, 6, 0.8 * S.r)),
            bl([(8.2, 9.4), (9.6, 11), (8.9, 11), (8.9, 12.6), (7.5, 12.6), (7.5, 11), (6.8, 11)], S, 0),
            bl([(17.6, 11), (16.2, 12.4), (16.2, 11.7), (14, 11.7), (14, 10.3), (16.2, 10.3), (16.2, 9.6)], S, 0)]


@icon("exit-countdown-markers", CAT, "Three roadside posts with three, two and one diagonal stripes.",
      tags=["exit markers", "countdown bars", "slip road warning", "motorway", "highway", "road posts", "exit ahead"])
def _(S):
    out = []
    for x, n in ((2.6, 3), (9.6, 2), (16.6, 1)):
        post = rect(x, 3, 4.8, 17, 0.8 * S.r)
        cuts = [P(poly([(x - 1, y + 1.7), (x + 5.8, y - 1.7), (x + 5.8, y - 0.1), (x - 1, y + 3.3)], closed=True))
                for y in (17, 12.2, 7.4)[:n]]
        out.append(Part("dot", path_to_d(D(P(post), *cuts))))
    return out + [line("M2 21.5H22")]


@icon("pedestrian-signal", CAT, "A signal head with a standing figure in the top lamp and a walking figure in the lower lamp.",
      tags=["walk signal", "crossing light", "pedestrian light", "traffic light", "green man", "red man", "crosswalk"])
def _(S):
    return ([head_box(S), bc(12, 5.5, 1.0), sk("M12 7.2V10.2M10.1 8.5H13.9M12 10.2L10.8 12.2M12 10.2L13.2 12.2", S, 1.2)]
            + person(S, 12, 14.2, 6.4, 1.3))


@icon("cyclist-signal", CAT, "A small signal head with a bicycle shape in the lit lamp.",
      tags=["bike signal", "cycle light", "bicycle traffic light", "traffic light", "cycle lane", "junction", "bike crossing"])
def _(S):
    return [head_box(S, 6.5, 3, 11, 18), bc(12, 7, 1.3)] + bike(S, 12, 15, 1.1, 0.72)


@icon("tram-signal", CAT, "A signal head with a vertical white bar lamp that controls trams.",
      tags=["tram light", "streetcar signal", "light rail", "traffic light", "rail priority", "bar signal", "tramway"])
def _(S):
    return [head_box(S, 7, 2.5, 10, 19), br(10.8, 5.6, 2.4, 12.8, 0.5 * S.r)]


@icon("countdown-signal", CAT, "A signal head beside a small display showing a two digit countdown number.",
      tags=["crossing timer", "walk timer", "pedestrian countdown", "traffic light", "seconds remaining", "crosswalk timer"])
def _(S):
    return ([head_box(S, 2.5, 3, 8, 18)] + person(S, 6.5, 7.6, 6.6, 1.2)
            + [shell(rect(13.5, 7.5, 8, 9, min(S.R, 2)))] + digits(S, "25", 15.3, 10.6, gap=0.9, w=1.0, scale=0.6))


@icon("lane-control-signal", CAT, "An overhead row of square lamps showing a cross and a downward arrow.",
      tags=["lane signal", "smart motorway", "red x", "overhead lamp", "lane closed", "variable lane", "gantry signal"])
def _(S):
    return [line("M2.5 3.5H21.5M7 3.5V8M17 3.5V8"), shell(rect(2.5, 8, 19, 12, min(S.R, 2))),
            detail(seg(12, 9.4, 12, 18.6)), sk("M4.9 11.4L9.6 16.6M9.6 11.4L4.9 16.6", S, 1.5),
            sk("M17 10.8V14", S, 1.5), head(S, (17, 17.4), 90, 3.4, 2.0)]


@icon("flashing-beacon", CAT, "A round amber lamp on top of a striped pole with light rays around it.",
      tags=["warning light", "belisha beacon", "hazard lamp", "amber light", "crossing beacon", "pole light", "flashing lamp"])
def _(S):
    return [shell("M7.6 14A4.4 4.4 0 0 1 16.4 14Z"), shell(rect(9, 14.6, 6, 7, min(S.R, 1.5))),
            detail(seg(8.6, 20.6, 15.4, 16.6)),
            line("M12 3V5.4M5.8 5.6L7.4 7.2M18.2 5.6L16.6 7.2M3.4 11.6H5.4M20.6 11.6H18.6")]


@icon("crossing-push-button", CAT, "A box on a pole with a round button and a small walking figure above it.",
      tags=["pedestrian button", "request to cross", "call button", "traffic signal", "crosswalk button", "wait to cross"])
def _(S):
    return ([shell(rect(6.5, 2.5, 11, 13, min(S.R, 3)))] + person(S, 12, 4.4, 5, 1.1)
            + [bc(12, 12.2, 1.6), line("M12 15.5V21.5")])


@icon("traffic-camera", CAT, "A camera on a tall pole with an arm, looking down at the road.",
      tags=["cctv", "surveillance", "road monitoring", "traffic monitoring", "pole camera", "security camera", "roadside"])
def _(S):
    return [line("M5.6 21.6V4.5H14"), shell(rect(11, 7.4, 9.5, 4.8, min(S.R, 1.6))), bc(17.6, 9.8, 1.2),
            sk("M13.4 15.4L11 21.6M19.6 15.4L22 21.6", S, 1.3)]


@icon("speed-camera", CAT, "A boxy roadside camera on a post with a flash unit above the lens.",
      tags=["radar", "enforcement", "speeding", "gatso", "roadside camera", "flash", "traffic enforcement"])
def _(S):
    return [shell(rect(3.5, 8.6, 17, 7, min(S.R, 2.5))), bc(9.2, 12.1, 2.3), br(14.2, 10.8, 3.6, 2.6, 0.5 * S.r),
            br(13.6, 3.6, 4.6, 2.6, 0.5 * S.r), line("M12 15.6V21.6")]


@icon("arrow-board", CAT, "A trailer mounted panel of lamps forming a large arrow.",
      tags=["road works", "lane closure", "warning trailer", "flashing arrow", "construction", "traffic management", "arrow panel"])
def _(S):
    dots = [bc(x, 9.6, 0.9) for x in (6.6, 9.6, 12.6)] + [bc(15.4, 6.9, 0.9), bc(15.4, 12.3, 0.9), bc(17.4, 9.6, 0.9)]
    return ([shell(rect(2.5, 3.5, 19, 12, min(S.R, 2)))] + dots
            + [line("M3.5 18.4H20.5"), bc(8.4, 20.4, 1.4), bc(15.6, 20.4, 1.4)])


@icon("bollard", CAT, "A short thick round post with a reflective band near the top.",
      tags=["post", "traffic post", "street furniture", "barrier post", "parking post", "safety post", "pillar"])
def _(S):
    return [shell(rect(8, 4.5, 8, 15.5, S.R)), detail(seg(8, 9.6, 16, 9.6)), line("M4 21.4H20")]


@icon("retractable-bollard", CAT, "A short post rising out of a round ground plate with up arrows beside it.",
      tags=["rising bollard", "pop up post", "access control", "hydraulic bollard", "vehicle barrier", "security post", "pedestrian zone"])
def _(S):
    return [shell(rect(9.5, 4.5, 5, 14, min(S.R, 2))), shell(ellipse(12, 19.8, 8, 1.6)),
            sk("M4.6 15.4V10", S, 1.5), head(S, (4.6, 6.6), -90, 3.4, 1.9),
            sk("M19.4 15.4V10", S, 1.5), head(S, (19.4, 6.6), -90, 3.4, 1.9)]
