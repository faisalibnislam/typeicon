"""TypeIcon Core: automotive (batch 002): tire and wheel tools, washing and detailing, garage equipment, cabin and engine parts.

Objects are drawn flat from the front or side. Tools that are long are turned 45 degrees so the handle points to the
lower left. Side-view cars face right with their wheels on one ground line.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    rect, regular, seg, shell, solid,
)
from geometry import polar

CAT = "automotive"
FILL = Style("filled", "butt", "miter", R=2.0, r=0.0)


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def isF(S):
    return S.name == "filled"


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def knock(d):
    return Part("dot", d)


def rot(pts, deg=45, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rp(pts, closed=True, r=0.0, deg=45):
    return poly(rot(pts, deg), closed=closed, r=r)


def rseg(x1, y1, x2, y2, deg=45):
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg)
    return seg(a, b, c, d)


def head(tip, deg, size=2.6, spread=40):
    a = polar(tip[0], tip[1], size, deg + 180 - spread)
    b = polar(tip[0], tip[1], size, deg + 180 + spread)
    return [a, tip, b]


def gear_pts(cx, cy, ro, ri, n, hw_out=9.0, hw_in=12.0, start=0.0):
    pts = []
    for i in range(n):
        a = start + i * 360.0 / n
        for rad, off in ((ri, -hw_in), (ro, -hw_out), (ro, hw_out), (ri, hw_in)):
            pts.append(polar(cx, cy, rad, a + off))
    return pts


def drop(cx, cy, s=1.0):
    return (f"M{fmt(cx)} {fmt(cy - 2.6 * s)}C{fmt(cx)} {fmt(cy - 2.6 * s)} {fmt(cx - 2.2 * s)} {fmt(cy)} {fmt(cx - 2.2 * s)} {fmt(cy + 1.0 * s)}"
            f"A{fmt(2.2 * s)} {fmt(2.2 * s)} 0 0 0 {fmt(cx + 2.2 * s)} {fmt(cy + 1.0 * s)}C{fmt(cx + 2.2 * s)} {fmt(cy)} {fmt(cx)} {fmt(cy - 2.6 * s)} {fmt(cx)} {fmt(cy - 2.6 * s)}Z")


def wheel(x, y, r=2.0):
    p = shell(circle(x, y, r))
    p.wheel = (x, y, r)
    return p


def car_parts(S, pts, ws, yb=None, T=None, s=1.0):
    T = T or (lambda p: p)
    yb = ws[0][1] if yb is None else yb
    if isF(S):
        out = [shell(poly([T(p) for p in pts], closed=True))]
    else:
        gaps = []
        for x, y, wr in ws:
            dy = yb - y
            if abs(dy) < wr:
                h = math.sqrt(wr * wr - dy * dy)
                gaps.append((x - h, x + h))
        gaps.sort()
        out = [shell(poly([T((gaps[0][0], yb))] + [T(p) for p in pts] + [T((gaps[-1][1], yb))], r=S.r))]
        for a, b in zip(gaps, gaps[1:]):
            if b[0] - a[1] > 0.5:
                out.append(line(seg(*T((a[1], yb)), *T((b[0], yb)))))
    for x, y, r in ws:
        cx, cy = T((x, y))
        out.append(wheel(cx, cy, r * s))
    return out


def veh_filled(fn):
    def f():
        parts = fn(FILL)
        wh = [p.wheel for p in parts if getattr(p, "wheel", None)]
        rest = [p for p in parts if not getattr(p, "wheel", None)]
        out = filled_region(rest) if rest else None
        if wh:
            cut = U(*[P(circle(x, y, r + 2)) for x, y, r in wh])
            discs = U(*[P(circle(x, y, r + 1)) for x, y, r in wh])
            out = U(D(out, cut), discs) if out is not None else discs
        return out
    return f


def vcar(name, description, tags, aliases=()):
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=veh_filled(fn))(fn)
    return deco


def T_(name, description, tags, aliases=()):
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases, filled=lambda: filled_region(fn(FILL)))(fn)
    return deco


CAR = [(2.5, 17.5), (2.5, 13), (5.5, 11.5), (8, 6), (15, 6), (18.5, 11), (21.5, 12.5), (21.5, 17.5)]
CARW = [(7, 17.5, 2.5), (17, 17.5, 2.5)]


# =========================================================================== chunk 1: tire and wheel service, washing

@T_("portable-tire-inflator", "Compact handheld air compressor with a gauge dial and a coiled hose ending in a chuck",
    ["tire inflator", "air compressor", "tyre inflator", "pump", "car tyre pump", "gauge", "roadside"])
def _(S):
    return [shell(rect(2.5, 7, 11, 13.5, rr(S, 3))), detail(circle(8, 12.5, 2.4)),
            line(poly([(13.5, 10), (17.5, 10), (17.5, 16)], r=S.r)), shell(rect(15.5, 16, 4, 5, 0.5))]


@T_("tire-plug-kit", "T-handle insertion tool beside a rope plug strip for repairing a punctured tire",
    ["tyre repair kit", "puncture repair", "plug tool", "tire repair", "flat tire", "t handle", "roadside"])
def _(S):
    return [shell(rect(2.5, 3.5, 9, 3.5, rr(S, 1.5))), line(poly([(7, 7), (7, 18), (5.5, 21), (8.5, 21), (7, 18)], r=0)),
            shell(rect(15, 3.5, 5.5, 17, rr(S, 2))), detail(seg(15, 9, 20.5, 9)), detail(seg(15, 15, 20.5, 15))]


@T_("tire-sealant-can", "Aerosol can with a short hose ending in a valve connector for sealing a flat tire",
    ["tyre sealant", "flat tire repair", "tire inflator spray", "puncture sealant", "aerosol", "can", "roadside"])
def _(S):
    return [shell(rect(3.5, 9, 9, 12, rr(S, 2.5))), shell(rect(5.5, 5, 5, 4, 0.5)),
            line(poly([(10.5, 7), (16, 7), (16, 12)], r=S.r)),
            shell(rect(14, 12, 4, 5, 0.5)), detail(seg(3.5, 14, 12.5, 14))]


@T_("tire-changer-machine", "Workshop tire changer with a tire on a low turntable and a tall arm with a mount head above",
    ["tyre changer", "tire machine", "wheel service", "tire fitting", "garage", "mount head", "bead breaker"])
def _(S):
    return [shell(rect(2.5, 17, 19, 4, rr(S, 1.5))), shell(rect(3.5, 10.5, 11, 6.5, rr(S, 2.5))),
            line(poly([(19, 17), (19, 4), (11, 4), (11, 8)], r=S.r)), detail(seg(6, 13.75, 12, 13.75))]


@T_("wheel-balancer", "Wheel with a hub dot inside an arched hood on a wheel balancing machine",
    ["tire balancer", "wheel balancing", "tyre balancing", "garage", "wheel weights", "workshop", "vibration"])
def _(S):
    return [line(poly([(2.5, 21), (2.5, 13), (2.5, 12)], r=0)),
            line(arc(11, 13.5, 8.5, 180, 360)), line(seg(19.5, 13.5, 19.5, 21)),
            shell(circle(11, 14, 4.2)), dot(11, 14, 1.2)]


@T_("wheel-alignment", "Front view of a tilted tire on the ground with a vertical plumb line showing the camber angle",
    ["camber", "wheel angle", "tracking", "geometry", "suspension setup", "tire alignment", "tyre alignment"])
def _(S):
    tire = rot([(8.5, 3), (14.5, 3), (14.5, 18.5), (8.5, 18.5)], 10, 11.5, 10.5)
    return [shell(poly(tire, closed=True, r=S.r * 0.5)), line(seg(2.5, 21, 21.5, 21)),
            line(seg(18.5, 2.5, 18.5, 18))]


@T_("tire-rotation", "Top view of four tires at the corners with a circular arrow between them swapping their positions",
    ["tyre rotation", "rotate tires", "swap tires", "tire service", "car maintenance", "wheel rotation", "tire care"])
def _(S):
    out = [shell(rect(2.5, 2.5, 4, 6.5, rr(S, 1.5))), shell(rect(17.5, 2.5, 4, 6.5, rr(S, 1.5))),
           shell(rect(2.5, 15, 4, 6.5, rr(S, 1.5))), shell(rect(17.5, 15, 4, 6.5, rr(S, 1.5)))]
    out += [line(arc(12, 12, 3.8, 205, 330)), line(arc(12, 12, 3.8, 25, 150)),
            line(poly(head(polar(12, 12, 3.8, 330), 330 + 90, 2.4), r=0)), line(poly(head(polar(12, 12, 3.8, 150), 150 + 90, 2.4), r=0))]
    return out


@T_("off-road-tire", "Side view of a thick tire with large chunky tread blocks standing out around its edge",
    ["mud tire", "all terrain tire", "4x4 tyre", "knobby tire", "offroad", "tread blocks", "tyre"])
def _(S):
    return [shell(poly(gear_pts(12, 12, 10, 8, 10, 10, 14), closed=True, r=S.r * 0.3)),
            detail(circle(12, 12, 5)), dot(12, 12, 1.4)]


@T_("whitewall-tire", "Side view of a tire with a wide pale ring band on the sidewall around the hub",
    ["white wall tyre", "classic car tire", "vintage tyre", "white sidewall", "retro wheel", "tire", "wheel"])
def _(S):
    ring = path_to_d(D(P(circle(12, 12, 10)), P(circle(12, 12, 7.2))))
    return [solid(ring), shell(poly(regular(12, 12, 3.8, 6), closed=True, r=S.r)), dot(12, 12, 1.0)]


@T_("tire-puncture-nail", "Tire tread section with a nail stuck into it and small air lines escaping",
    ["flat tire", "puncture", "nail in tyre", "leak", "tire damage", "air leak", "tyre repair"])
def _(S):
    return [shell("M2.5 21V18a9.5 9.5 0 0 1 19 0V21Z"), line(seg(8.5, 3, 15.5, 3)),
            line(seg(12, 3, 12, 14)), line(seg(18.5, 6, 21, 3.5))]


@T_("car-wash-brush", "Long-handled washing brush with a bristle head and a hose connector at the handle end",
    ["car washing", "wash brush", "scrub brush", "vehicle cleaning", "soft brush", "hose brush", "detailing"])
def _(S):
    return [shell(rp([(7, 2.5), (17, 2.5), (17, 9.5), (7, 9.5)], r=S.r * 0.6)),
            detail(rseg(10, 2.5, 10, 9.5)), detail(rseg(14, 2.5, 14, 9.5)),
            line(rseg(12, 9.5, 12, 19)), shell(rp([(10.5, 19), (13.5, 19), (13.5, 22), (10.5, 22)]))]


@T_("foam-cannon", "Bottle on a pressure washer lance spraying a thick cloud of foam",
    ["snow foam", "foam lance", "car wash foam", "pressure washer", "soap sprayer", "detailing", "suds"])
def _(S):
    cloud = union(circle(17, 9, 3.2), circle(20, 13.5, 2.4), circle(15, 14, 2.6))
    return [shell(rect(2.5, 11, 7, 10, rr(S, 2.5))), shell(rect(4.5, 7.5, 3, 3.5, 0.5)),
            line(poly([(6, 7.5), (6, 4), (11, 4)], r=S.r)), shell(cloud)]


@T_("wash-mitt", "Chunky wash mitten with a thumb and a covering of fluffy chenille strands",
    ["microfiber mitt", "wash glove", "car washing", "sponge glove", "chenille mitt", "cleaning", "detailing"])
def _(S):
    return [shell(poly([(6, 21.5), (6, 15), (2.5, 12), (4.5, 9.5), (8, 12), (8, 6), (17.5, 6), (19, 9), (19, 21.5)], closed=True, r=S.r)),
            detail("M12 11v6"), detail("M15.5 11v6")]


@T_("drying-towel", "Folded microfiber towel with a fringed edge and a water drop above it",
    ["microfibre towel", "car drying", "chamois", "cloth", "dry cloth", "detailing", "wipe"])
def _(S):
    return [shell(rect(2.5, 9, 15, 11.5, rr(S, 2))), detail(seg(2.5, 14.5, 17.5, 14.5)),
            line(seg(17.5, 11.5, 21.5, 11.5)), line(seg(17.5, 15, 21.5, 15)), line(seg(17.5, 18.5, 21.5, 18.5)),
            knock(drop(18, 5.4, 0.9))]


@T_("car-wax", "Shallow round tin of paste wax with a foam applicator pad beside it",
    ["car polish", "paste wax", "carnauba", "wax tin", "paint protection", "detailing", "shine"])
def _(S):
    return [shell(rect(2.5, 11.5, 13, 8.5, rr(S, 2.5))), detail(ellipse(9, 11.5, 5.5, 2)),
            shell(rect(17.5, 12, 4, 8, rr(S, 1.5)))]


@T_("dual-action-polisher", "Handheld machine polisher with a top handle, a side handle and a round foam pad underneath",
    ["buffer", "orbital polisher", "car buffing", "paint polish", "da polisher", "detailing", "foam pad"])
def _(S):
    return [shell(rect(7, 10, 10, 7, rr(S, 2.5))), shell(rect(3, 17, 18, 4, rr(S, 1.5))),
            line(poly([(9.5, 10), (9.5, 5), (14.5, 5), (14.5, 10)], r=S.r)), line(seg(17, 13, 21.5, 13))]


@T_("clay-bar", "Flat clay bar resting on a paint panel line with a spray bottle beside it",
    ["detailing clay", "paint decontamination", "clay lube", "car prep", "paint cleaning", "detailing", "spray bottle"])
def _(S):
    return [shell(rect(2.5, 8, 10, 6, rr(S, 3))), line(seg(2.5, 18.5, 12.5, 18.5)),
            shell(rect(15, 12, 6.5, 9.5, rr(S, 2))), shell(rect(16.5, 8.5, 3.5, 3.5, 0.5)),
            line(seg(16.5, 8, 13.5, 8))]


@T_("tire-shine-applicator", "Foam pad wiping the curved sidewall of a tire with a shine sparkle",
    ["tyre dressing", "tire dressing", "sidewall shine", "applicator pad", "wheel care", "detailing", "gloss"])
def _(S):
    star = [(19.5, 8.5), (20.5, 11), (23, 12), (20.5, 13), (19.5, 15.5), (18.5, 13), (16, 12), (18.5, 11)]
    return [shell(rect(2.5, 8, 8.5, 8, rr(S, 2.5))), line(arc(23.5, 12, 10.5, 118, 242)), solid(poly(star, closed=True))]


def lamp_d(S, x0=2.5, x1=15.5, y0=5.0, y1=19.0):
    ym = (y0 + y1) / 2
    k = (x1 - x0) * 0.62
    return (f"M{fmt(x1)} {fmt(y0)}C{fmt(x1 - k)} {fmt(y0)} {fmt(x0)} {fmt(ym - 3.5)} {fmt(x0)} {fmt(ym)}"
            f"C{fmt(x0)} {fmt(ym + 3.5)} {fmt(x1 - k)} {fmt(y1)} {fmt(x1)} {fmt(y1)}Z")


@T_("headlight-restoration", "Car headlamp lens cloudy on the left half and clear on the right with a sparkle",
    ["headlamp polishing", "foggy headlights", "lens cleaning", "yellowed headlight", "detailing", "car lights", "restore"])
def _(S):
    star = [(11.5, 9.5), (12.3, 11.7), (14.5, 12.5), (12.3, 13.3), (11.5, 15.5), (10.7, 13.3), (8.5, 12.5), (10.7, 11.7)]
    return [shell(lamp_d(S)), dot(6.5, 10.5, 1.1), dot(6.5, 14.5, 1.1), knock(poly(star, closed=True)),
            line(seg(18.5, 7, 21.5, 6)), line(seg(18.5, 12, 21.5, 12)), line(seg(18.5, 17, 21.5, 18))]


@T_("antifreeze-jug", "Plastic jug with a handle, a cap and a snowflake on its label",
    ["coolant jug", "antifreeze", "radiator fluid", "engine coolant", "winter fluid", "snowflake", "car fluids"])
def _(S):
    return [shell(rect(4, 8, 12.5, 13.5, rr(S, 3))), shell(rect(7, 3.5, 6, 4.5, 0.5)),
            line(poly([(16.5, 11), (20.5, 11), (20.5, 17), (16.5, 17)], r=S.r)),
            detail(seg(10.25, 11.5, 10.25, 18)), detail(seg(7.2, 13.2, 13.3, 16.3)), detail(seg(13.3, 13.2, 7.2, 16.3))]


@T_("car-battery-charger", "Box charger with a gauge dial and two cables ending in positive and negative clamps",
    ["battery charger", "trickle charger", "car battery", "charging", "jump start", "clamps", "garage"])
def _(S):
    j1 = [(18, 7.5), (21.5, 7.5), (21.5, 11), (18, 10.2)]
    j2 = [(18, 14), (21.5, 14), (21.5, 17.5), (18, 16.7)]
    return [shell(rect(2.5, 6.5, 12, 13, rr(S, 2.5))), detail(circle(8.5, 11.5, 2.3)), detail(seg(5.5, 17, 11.5, 17)),
            line(seg(14.5, 9.5, 18, 9)), line(seg(14.5, 15.5, 18, 15.5)), solid(poly(j1, closed=True)), solid(poly(j2, closed=True))]


@T_("jump-starter-pack", "Compact battery pack with a carry handle, a bolt mark and a cable ending in jaw clamps",
    ["booster pack", "jump pack", "portable jump starter", "battery booster", "emergency start", "dead battery", "roadside"])
def _(S):
    bolt = [(10, 12), (7.5, 16), (9.5, 16), (8.5, 19), (12, 14.5), (10, 14.5)]
    jaw = [(17.5, 17), (21.5, 17), (19.5, 21.5)]
    return [shell(rect(2.5, 9, 13, 12, rr(S, 2.5))), line(poly([(5.5, 9), (5.5, 5), (12.5, 5), (12.5, 9)], r=S.r)),
            knock(poly(bolt, closed=True)), line(poly([(15.5, 12), (19.5, 12), (19.5, 17)], r=S.r)), solid(poly(jaw, closed=True))]


@T_("emissions-test", "Car tailpipe with a probe and hose leading up to a small analyzer unit",
    ["smog test", "exhaust test", "emission check", "co2 test", "vehicle inspection", "mot", "exhaust gas analyzer"])
def _(S):
    return [shell(rect(11, 3, 10.5, 8, rr(S, 2))), detail(poly([(13.5, 8), (15.5, 5.5), (17, 8), (19, 6)], r=0)),
            line(poly([(16, 11), (16, 16), (6, 16)], r=S.r)), shell(poly([(2.5, 13), (10, 13), (10, 19.5), (2.5, 19.5)], closed=True, r=S.r * 0.4))]


@T_("dent-puller", "Suction cup with a T handle pulling a small dent out of a body panel",
    ["suction dent puller", "dent repair", "panel beating", "bodywork", "dent removal", "pdr", "car body repair"])
def _(S):
    return [shell("M7.5 14.5a4.5 4.5 0 0 1 9 0Z"), line(seg(12, 10, 12, 4.5)), line(seg(8, 4, 16, 4)),
            line("M2.5 20H8Q12 13.5 16 20H21.5")]


@T_("slide-hammer", "Long steel rod with a sliding weight, an end stop and a hook tip",
    ["dent puller", "bodywork tool", "slide puller", "hammer puller", "garage tool", "rod", "hook"])
def _(S):
    return [shell(rp([(9, 2.5), (15, 2.5), (15, 5.5), (9, 5.5)], r=0)), shell(rp([(8.5, 8), (15.5, 8), (15.5, 13), (8.5, 13)], r=S.r * 0.5)),
            line(rseg(12, 5.5, 12, 8)), line(rseg(12, 13, 12, 18)),
            line(rp([(12, 18), (12, 21), (15.5, 21), (15.5, 18.5)], closed=False, r=S.r))]


@T_("auto-paint-booth", "Enclosed paint booth with a car outline inside and a spray gun misting from the wall",
    ["spray booth", "car painting", "body shop", "paint shop", "refinishing", "spray gun", "paintwork"])
def _(S):
    car = [(5, 17), (5, 14.5), (7, 13.5), (8.5, 10.5), (12, 10.5), (13.5, 13.5), (15.5, 14.5), (15.5, 17)]
    return [shell(rect(2.5, 3, 19, 18, rr(S, 2.5))), detail(poly(car, r=S.r * 0.4)),
            detail(seg(17.5, 7.5, 21, 7.5)), dot(14.5, 7.5, 0.9), dot(11.5, 7.5, 0.9)]


@T_("magnetic-parts-tray", "Round shallow steel dish holding a loose nut and bolt",
    ["parts tray", "bolt tray", "magnet dish", "screw tray", "mechanic tray", "garage", "nuts and bolts"])
def _(S):
    return [shell(poly([(2.5, 12), (21.5, 12), (19, 20), (5, 20)], closed=True, r=S.r)),
            shell(poly(regular(7.5, 7, 2.8, 6), closed=True, r=S.r * 0.3)),
            line(seg(14, 5, 14, 10)), line(seg(11.5, 5, 16.5, 5)), dot(19.5, 9, 1.1)]


@T_("fender-cover", "Padded cover draped over the curved front wing of a car with the wheel arch cut out",
    ["wing cover", "fender protector", "mechanic cover", "paint protection", "bonnet cover", "garage", "mat"])
def _(S):
    return [shell(poly([(2.5, 20), (2.5, 12), (7, 8), (17, 8), (21.5, 12), (21.5, 20)], closed=True, r=S.r)),
            detail(arc(12, 20, 5, 180, 360)),
            line(poly([(4, 5), (14, 2.5)], r=0))]


@T_("creeper-seat", "Low rolling stool with a padded seat, short legs, casters and a tool tray beneath",
    ["mechanic stool", "garage stool", "rolling seat", "workshop seat", "creeper stool", "tool tray", "wheeled stool"])
def _(S):
    return [shell(rect(3, 7.5, 18, 4.5, rr(S, 2))), line(seg(6, 12, 6, 18)), line(seg(18, 12, 18, 18)),
            line(seg(6, 15.5, 18, 15.5)), dot(6, 20, 1.5), dot(12, 20, 1.5), dot(18, 20, 1.5)]


@T_("scissor-car-lift", "Low scissor lift with crossed arms raising a flat platform that carries a car",
    ["car lift", "vehicle lift", "scissor lift", "garage lift", "hoist", "workshop", "wheel service"])
def _(S):
    car = [(4, 8.5), (4, 6.5), (6.5, 5.5), (8.5, 3), (14.5, 3), (16.5, 5.5), (20, 6.5), (20, 8.5)]
    return [shell(poly(car, closed=True, r=S.r * 0.5)), dot(7.5, 9.6, 1.3), dot(16.5, 9.6, 1.3),
            shell(rect(2.5, 11, 19, 2.5, S.R * 0.375)), shell(rect(2.5, 19.5, 19, 2.5, S.R * 0.375)),
            line(seg(7, 13.5, 17, 19.5)), line(seg(17, 13.5, 7, 19.5))]


# =========================================================================== chunk 3: garage equipment and tools

@T_("engine-stand", "Upright stand on casters with a rotating head plate holding an engine block",
    ["engine holder", "motor stand", "engine rebuild", "garage stand", "engine mount", "workshop", "block stand"])
def _(S):
    return [shell(rect(12.5, 4, 9, 12, rr(S, 2))), detail(seg(15.5, 7, 18.5, 7)), detail(seg(15.5, 10.5, 18.5, 10.5)),
            line(seg(10, 3, 10, 17)), line(seg(4.5, 10, 10, 10)), line(seg(4.5, 10, 4.5, 18.5)),
            line(seg(2.5, 18.5, 12, 18.5)), dot(3.8, 21, 1.3), dot(11, 21, 1.3)]


@T_("transmission-jack", "Tall telescoping hydraulic jack on casters with a wide cradle plate on top",
    ["gearbox jack", "transmission lift", "trans jack", "floor jack", "garage jack", "saddle", "workshop"])
def _(S):
    return [line(poly([(3, 5), (6, 8), (18, 8), (21, 5)], r=S.r)), line(seg(12, 8, 12, 11)),
            shell(rect(9.5, 11, 5, 8, rr(S, 1.5))), line(seg(3, 19, 21, 19)), dot(5, 21.3, 1.3), dot(19, 21.3, 1.3)]


@T_("impact-wrench", "Pistol-grip power tool with a square anvil drive and a socket on the front",
    ["air wrench", "power wrench", "lug nut gun", "pneumatic wrench", "socket gun", "garage tool", "tire change"])
def _(S):
    body = union(rect(3, 4.5, 12, 7.5, rr(S, 2.5)), rect(6.5, 10, 5, 11, rr(S, 1.5)))
    return [shell(body), line(seg(15, 8, 17.5, 8)), shell(rect(17.5, 5, 4, 6, rr(S, 1.5)))]


@T_("timing-light", "Pistol-shaped strobe light with a lead cable and a flash beam leaving its nozzle",
    ["strobe timing", "ignition timing", "engine timing", "timing gun", "tune up", "mechanic tool", "flash"])
def _(S):
    body = union(rect(8, 4, 12, 6.5, rr(S, 2.5)), rect(11, 9.5, 5, 8.5, rr(S, 1.5)))
    return [shell(body), line(seg(8, 7.25, 6, 7.25)), line(seg(2.5, 4.5, 5.5, 5.5)), line(seg(2.5, 10, 5.5, 9)),
            line(poly([(13.5, 18), (13.5, 21), (20.5, 21)], r=S.r))]


@T_("compression-tester", "Round pressure gauge on a hose ending in a threaded spark plug adapter",
    ["cylinder compression", "engine tester", "pressure gauge", "compression gauge", "spark plug tester", "diagnostic", "psi"])
def _(S):
    return [shell(circle(12, 8.5, 6)), detail(seg(12, 8.5, 15.2, 5.5)), dot(12, 8.5, 1.1),
            line(poly([(12, 14.5), (12, 16), (14, 19.5), (17, 19.5)], r=S.r)), shell(rect(17, 17, 4.5, 5, 0.5))]


@T_("inspection-pit", "Garage floor with a deep pit below a parked car and rungs of a ladder down into it",
    ["service pit", "garage pit", "mechanic pit", "under car access", "workshop", "oil change pit", "car maintenance"])
def _(S):
    return [line(poly([(2.5, 10), (6, 10), (6, 20.5), (18, 20.5), (18, 10), (21.5, 10)], r=S.r * 0.6)),
            line(seg(10, 4.5, 10, 19)), line(seg(14, 4.5, 14, 19)),
            line(seg(10, 12.5, 14, 12.5)), line(seg(10, 16, 14, 16))]


@T_("garage-parking-ball", "Ball hanging on a string from the garage ceiling just touching a car windshield",
    ["parking aid", "hanging ball", "tennis ball parking", "garage guide", "stop marker", "park assist", "ceiling string"])
def _(S):
    return [line(seg(2.5, 3, 12, 3)), line(seg(8, 3, 8, 7)), shell(circle(8, 9.5, 2.5)),
            shell(poly([(2.5, 21), (2.5, 16), (10.5, 15), (14.5, 8), (21.5, 8), (21.5, 21)], closed=True, r=S.r * 0.5))]


@T_("wheel-dolly", "Low square frame on four casters cradling a tire",
    ["tire dolly", "wheel mover", "wheel cart", "tyre trolley", "garage dolly", "tire moving", "wheel stand"])
def _(S):
    return [shell(circle(12, 8.5, 5.5)), dot(12, 8.5, 1.2), shell(rect(2.5, 15.5, 19, 3.5, S.R * 0.45)),
            dot(5.5, 21.3, 1.3), dot(18.5, 21.3, 1.3)]


@T_("tow-dolly", "Small two-wheel trailer with a tongue and a flat platform carrying the front end of a car",
    ["car dolly", "tow trailer", "vehicle trailer", "flat towing", "towing", "trailer", "car transport"])
def _(S):
    return [shell(poly([(8.5, 13), (8.5, 9), (12, 8), (14.5, 4.5), (21.5, 4.5), (21.5, 13)], closed=True, r=S.r * 0.5)),
            shell(rect(6, 14, 16, 3, S.R * 0.3)), line(seg(2.5, 15.5, 6, 15.5)), shell(circle(14, 19.7, 1.6))]


@T_("spring-compressor", "Two long threaded rods with hooked jaws clamping a coil spring between them",
    ["coil spring compressor", "strut spring tool", "suspension tool", "spring tool", "mechanic tool", "shock absorber", "garage tool"])
def _(S):
    return [line(seg(3.5, 3, 3.5, 21)), line(seg(20.5, 3, 20.5, 21)),
            line(seg(3.5, 5, 8, 5)), line(seg(3.5, 19, 8, 19)), line(seg(16, 5, 20.5, 5)), line(seg(16, 19, 20.5, 19)),
            line(poly([(8.5, 6), (15.5, 8.5), (8.5, 11), (15.5, 13.5), (8.5, 16), (15.5, 18)], r=S.r * 0.3))]


@T_("emergency-warning-triangle", "Reflective warning triangle standing on a small foot with a smaller triangle inside",
    ["breakdown triangle", "hazard triangle", "road triangle", "reflective triangle", "roadside safety", "car breakdown", "warning sign"])
def _(S):
    return [shell(poly([(12, 2.5), (21.5, 18), (2.5, 18)], closed=True, r=S.r)),
            detail(poly([(12, 8.5), (16.5, 15), (7.5, 15)], closed=True, r=0)),
            line(seg(6, 21, 18, 21))]


@T_("remote-engine-start", "Key fob with a button and a radio arc pointing toward a small car above it",
    ["remote start", "key fob", "car remote", "engine start", "fob", "wireless start", "pre heat car"])
def _(S):
    return [shell(rect(3, 3, 8.5, 18, rr(S, 3.5))), detail(arc(7.25, 12, 2.6, 300, 240)), detail(seg(7.25, 8, 7.25, 12)),
            line(arc(11.5, 8, 4.5, 305, 55)), line(arc(11.5, 8, 8, 305, 55))]


@T_("keyless-entry", "Smart key card with a signal arc beside a car door and its pull handle",
    ["smart key", "proximity key", "key card", "unlock car", "passive entry", "door handle", "car access"])
def _(S):
    return [shell(rect(2.5, 12, 7, 9.5, rr(S, 2.5))), detail(seg(5, 16.5, 7, 16.5)),
            shell(rect(13.5, 3.5, 8, 17, rr(S, 3))), knock(rect(15.5, 9, 4, 2.5, rr(S, 1.2))), line(arc(8.5, 9.5, 3.2, 270, 360))]


@T_("shark-fin-antenna", "Side view of a curved car roof with a small shark fin shaped antenna on top",
    ["roof antenna", "fin antenna", "car aerial", "gps antenna", "radio antenna", "roof mount", "car roof"])
def _(S):
    return [shell(poly([(2.5, 19), (4, 14.5), (9, 11.5), (19, 11.5), (21.5, 15), (21.5, 19)], closed=True, r=S.r)),
            shell("M19 11.5C16 10 13 7.5 11.5 3.5L10.5 11.5Z")]


@T_("car-windshield", "Front view of a trapezoid windshield with a wiper lying along its lower edge",
    ["windscreen", "front glass", "car glass", "wiper", "auto glass", "windshield repair", "car window"])
def _(S):
    return [shell(poly([(6.5, 5), (17.5, 5), (21.5, 18), (2.5, 18)], closed=True, r=S.r)),
            line(seg(6, 13.5, 16, 13.5)), line(seg(2.5, 21, 21.5, 21))]


# =========================================================================== chunk 4: interior, service and dashboard

def star4(cx, cy, r, k=0.28):
    return [(cx, cy - r), (cx + r * k, cy - r * k), (cx + r, cy), (cx + r * k, cy + r * k),
            (cx, cy + r), (cx - r * k, cy + r * k), (cx - r, cy), (cx - r * k, cy - r * k)]


def sm_car(S, dy=0.0, scale=1.0):
    T = lambda p: (2.5 + (p[0] - 2.5) * scale, 18.5 + dy - (17.5 - p[1]) * scale)  # noqa: E731
    return T


@T_("manual-gear-knob", "Round gear stick knob seen from above with an H shaped shift pattern marked on top",
    ["gear stick", "shift knob", "gear shifter", "manual transmission", "stick shift", "h pattern", "gearshift"])
def _(S):
    return [shell(rect(4.5, 2.5, 15, 13, S.R * 1.6)), detail(seg(9.5, 6, 9.5, 12)), detail(seg(14.5, 6, 14.5, 12)),
            detail(seg(9.5, 9, 14.5, 9)), line(seg(12, 15.5, 12, 21.5))]


@T_("car-seat-cover", "Side view of a car seat wrapped in a fitted cover with stitched seam lines",
    ["seat protector", "seat cover", "upholstery", "car interior", "seat slipcover", "leather seat", "cushion cover"])
def _(S):
    return [shell(poly([(5, 3), (10, 3), (11.5, 13), (20, 13.5), (21, 20), (4.5, 20)], closed=True, r=S.r)),
            detail(seg(7.2, 7, 8, 11)), detail(seg(13, 17, 18, 17))]


@T_("car-trunk-organizer", "Open box with dividers holding a bottle and small items for the trunk of a car",
    ["boot organiser", "trunk organiser", "cargo box", "car storage", "trunk tidy", "storage bin", "car boot"])
def _(S):
    return [shell(rect(2.5, 11, 19, 10, rr(S, 2.5))), detail(seg(9, 11, 9, 21)), detail(seg(15, 11, 15, 21)),
            shell(rect(4, 3.5, 3, 7.5, rr(S, 1))), shell(rect(10.5, 7, 3, 4, 0.5))]


@T_("car-trash-bin", "Small bin bag hanging by two straps from the top of a front headrest",
    ["car bin", "headrest bin", "litter bag", "car rubbish bag", "car trash bag", "hanging bin", "car interior"])
def _(S):
    return [shell(rect(5, 2.5, 14, 3.5, rr(S, 1.5))), line(seg(8.5, 6, 8.5, 9.5)), line(seg(15.5, 6, 15.5, 9.5)),
            shell(poly([(5.5, 9.5), (18.5, 9.5), (17, 21.5), (7, 21.5)], closed=True, r=S.r * 0.6)),
            detail(seg(10, 14, 14, 14))]


def mag(cx, cy, r, tail):
    return [shell(circle(cx, cy, r)), line(seg(cx + r * 0.72, cy + r * 0.72, cx + tail, cy + tail))]


@vcar("car-inspection", "Small side-view car with a magnifying glass held over its roof",
      ["vehicle inspection", "car check", "used car check", "pre purchase inspection", "car survey", "mot", "car examination"])
def _(S):
    T = sm_car(S, 0, 0.72)
    return car_parts(S, CAR, CARW, 17.5, T, 0.72) + [shell(circle(17, 7, 3.6)), line(seg(19.6, 9.6, 21.5, 11.5))]


@vcar("car-detailing", "Side-view car with sparkles shining above its polished paint",
      ["car polish", "car valet", "paint shine", "car cleaning", "car care", "auto detailing", "waxed car"])
def _(S):
    T = sm_car(S, 1, 0.9)
    return car_parts(S, CAR, CARW, 17.5, T, 0.9) + [solid(poly(star4(18, 5, 3.4), closed=True)), solid(poly(star4(6.5, 6, 2.2), closed=True))]


@vcar("used-car", "Side-view car with a price tag with a hole hanging above its hood",
      ["second hand car", "pre owned car", "car for sale", "car dealership", "price tag", "preowned vehicle", "secondhand car"])
def _(S):
    T = sm_car(S, 1, 0.9)
    tag = poly([(15, 2.5), (21, 2.5), (21, 8), (18, 10.5), (15, 8)], closed=True, r=S.r * 0.5)
    return car_parts(S, CAR, CARW, 17.5, T, 0.9) + [shell(tag), knock(circle(18, 5.3, 1.1))]


@T_("test-drive", "Steering wheel with three spokes beside a small checkered flag on a pole",
    ["trial drive", "drive test", "car demo", "dealership", "try before you buy", "steering wheel", "checkered flag"])
def _(S):
    return [shell(circle(9, 14, 6.8)), detail(seg(3, 14, 15, 14)), detail(seg(9, 14, 9, 20.5)), dot(9, 14, 1.8),
            line(seg(18, 3, 18, 12)), shell(rect(18, 3, 3.5, 5, 0.3)), solid(rect(18, 3, 1.75, 2.5)), solid(rect(19.75, 5.5, 1.75, 2.5))]


@vcar("car-overheating", "Side-view car with wavy steam lines rising from the front of its hood",
      ["overheat", "engine overheating", "steam", "radiator boiling", "temperature warning", "breakdown", "hot engine"])
def _(S):
    return car_parts(S, CAR, CARW, 17.5) + [line("M18 9c-1.5-1.2 1.5-2.3 0-3.5s1.5-2.3 0-3.5")]


@T_("engine-cooling-system", "Radiator and engine block joined by two hoses with arrows showing coolant flow",
    ["coolant circuit", "radiator hoses", "cooling loop", "coolant flow", "water pump system", "engine radiator", "cooling"])
def _(S):
    return [shell(rect(2.5, 6, 5.5, 12, rr(S, 1.5))), detail(seg(2.5, 10, 8, 10)), detail(seg(2.5, 14, 8, 14)),
            shell(rect(16, 6, 5.5, 12, rr(S, 2))), detail(seg(16, 12, 21.5, 12)),
            line(seg(8, 9, 16, 9)), line(poly(head((8, 9), 180, 2.2), r=0)),
            line(seg(8, 15, 16, 15)), line(poly(head((16, 15), 0, 2.2), r=0))]


@T_("engine-knock", "Piston inside a cylinder with a jagged burst in the chamber above it",
    ["detonation", "pinging", "engine pinging", "piston slap", "knock sensor", "engine noise", "combustion"])
def _(S):
    burst = []
    for i in range(12):
        burst.append(polar(12, 8.5, 4.6 if i % 2 == 0 else 2.2, -90 + i * 30))
    return [line(seg(4.5, 3.5, 4.5, 21)), line(seg(19.5, 3.5, 19.5, 21)), solid(poly(burst, closed=True)),
            shell(rect(8, 14, 8, 7, rr(S, 1.5))), detail(seg(8, 17, 16, 17))]


@T_("turbo-boost-gauge", "Round gauge with a small turbine ring at its base and a needle pointing into the boost range",
    ["boost gauge", "turbo gauge", "boost pressure", "turbocharger gauge", "psi gauge", "forced induction", "manifold pressure"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(seg(12, 12, 16.2, 7.8)), dot(12, 12, 1.4),
            detail(circle(12, 17.2, 2))]


@T_("voltmeter-gauge", "Round gauge with a small battery mark at its base and a needle swung left of center",
    ["battery gauge", "volt gauge", "voltage meter", "charging gauge", "dashboard meter", "alternator gauge", "volts"])
def _(S):
    return [shell(circle(12, 12, 9.5)), detail(seg(12, 11.5, 7.2, 7)), dot(12, 11.5, 1.4),
            knock(rect(8.5, 15.2, 7, 4, 0.6))]


@T_("windshield-washer-nozzle", "Small washer nozzle on the hood edge spraying two fans of fluid up at the windshield",
    ["washer jet", "screen wash", "windscreen washer", "spray nozzle", "washer fluid", "wiper wash", "windshield spray"])
def _(S):
    return [line(poly([(2.5, 19), (14.5, 19), (21, 4)], r=S.r * 0.4)), shell(rect(5, 14.5, 3.5, 3.5, 0.5)),
            line(seg(8.5, 13.5, 12, 7.5)), line(seg(9, 16, 14, 13.5))]


@T_("horn-button", "Round steering wheel center pad with a small horn speaker and sound arcs on it",
    ["car horn", "beep", "horn pad", "steering wheel horn", "honk", "klaxon", "airbag pad"])
def _(S):
    return [shell(poly([(3, 9.5), (8, 9.5), (19, 4), (19, 20), (8, 14.5), (3, 14.5)], closed=True, r=S.r)),
            detail(seg(8, 9.5, 8, 14.5)), line(seg(21.5, 9, 21.5, 15))]

# =========================================================================== chunk 5: cabin controls, modes and engine parts

def _swc_parts(S):
    out = [line(circle(12, 12, 9.5)), line(circle(12, 12, 4.8))]
    for k in range(8):
        a = k * 45 + 22.5
        p, q = polar(12, 12, 6.6, a), polar(12, 12, 7.9, a)
        out.append(line(seg(p[0], p[1], q[0], q[1])))
    return out


def _swc_filled():
    ring = D(P(circle(12, 12, 10.5)), P(circle(12, 12, 3.8)))
    cuts = []
    for k in range(8):
        a = k * 45 + 22.5
        p, q = polar(12, 12, 6.6, a), polar(12, 12, 7.9, a)
        cuts.append(ST(seg(p[0], p[1], q[0], q[1]), 1.2, "butt", "miter", 4))
    return D(ring, U(*cuts))


@icon("steering-wheel-cover", CAT, "Steering wheel rim wrapped in a cover with small stitch marks around it",
      tags=["wheel cover", "leather cover", "steering cover", "grip cover", "car interior", "stitching", "wheel wrap"],
      filled=_swc_filled)
def _(S):
    return _swc_parts(S)


@T_("ignition-switch", "Round ignition barrel with a tilted key slot in the middle and position ticks above it",
    ["ignition barrel", "key slot", "start switch", "key lock", "car key", "ignition", "start stop"])
def _(S):
    slot = poly(rot([(10.7, 9.5), (13.3, 9.5), (13.3, 18), (10.7, 18)], -30, 12, 13), closed=True)
    ticks = []
    for a in (215, 270, 325):
        p, q = polar(12, 12, 6.2, a), polar(12, 12, 8.2, a)
        ticks.append(detail(seg(p[0], p[1], q[0], q[1])))
    return [shell(rect(2.5, 2.5, 19, 19, S.R * 2.5)), knock(slot)] + ticks


@T_("wiper-stalk", "Lever arm sticking out of a steering column ending in a round tip with a wiper arc mark",
    ["wiper lever", "indicator stalk", "column stalk", "wiper control", "windshield wiper switch", "steering column", "turn signal lever"])
def _(S):
    return [shell(rect(2.5, 7.5, 6, 9, rr(S, 2))), line(seg(8.5, 12, 14, 12)), shell(circle(18, 12, 4)),
            detail(arc(18, 13.2, 2.2, 210, 330)), detail(seg(18, 13.2, 18, 10.5))]


@T_("sport-driving-mode", "Speedometer arc with its needle swung far to the right and a red zone mark",
    ["sport mode", "performance mode", "fast driving", "drive mode", "speed", "tachometer", "dynamic mode"])
def _(S):
    tip = polar(12, 13.5, 7, -22)
    return [line(arc(12, 13.5, 9.5, 150, 390)), line(seg(12, 13.5, tip[0], tip[1])), dot(12, 13.5, 1.6),
            line(arc(12, 13.5, 5.5, 335, 15)), line(seg(2.5, 20.5, 21.5, 20.5))]


@vcar("winter-driving-mode", "Side-view car with a snowflake floating above its roof",
      ["snow mode", "winter mode", "ice driving", "snow driving", "cold weather", "traction mode", "snowflake"])
def _(S):
    T = sm_car(S, 1, 0.9)
    fl = []
    for a in (90, 30, 150):
        p, q = polar(12, 4.3, 3.3, a), polar(12, 4.3, 3.3, a + 180)
        fl.append(line(seg(p[0], p[1], q[0], q[1])))
    return car_parts(S, CAR, CARW, 17.5, T, 0.9) + fl


@T_("cross-traffic-warning", "Car seen from above reversing with two arrows approaching from both sides behind it",
    ["rear cross traffic alert", "rcta", "reversing alert", "reverse warning", "blind spot", "parking sensor", "backing up"])
def _(S):
    return [shell(rect(7.5, 2.5, 9, 13.5, rr(S, 3.5))), detail(seg(9.5, 7, 14.5, 7)), detail(seg(9.5, 12.5, 14.5, 12.5)),
            line(seg(2.5, 20, 9, 20)), line(poly(head((9, 20), 0, 2.4), r=0)),
            line(seg(21.5, 20, 15, 20)), line(poly(head((15, 20), 180, 2.4), r=0))]


@T_("power-liftgate", "Side view of an SUV rear with its tailgate raised on a strut",
    ["tailgate", "electric tailgate", "hatchback open", "trunk lid", "boot lid", "rear door", "suv"])
def _(S):
    pts = [(2.5, 17.5), (2.5, 13), (5, 11.5), (8.5, 6), (17.5, 6), (17.5, 17.5)]
    return car_parts(S, pts, [(7, 17.5, 2.5), (13, 17.5, 2.5)], 17.5) + [line(seg(17.5, 6, 21.5, 1.8)), line(seg(17.5, 10, 20.5, 5.5))]


@T_("mirror-adjustment-knob", "Small round joystick knob with arrowheads pointing up, down, left and right around it",
    ["mirror control", "wing mirror switch", "side mirror adjust", "door mirror", "mirror joystick", "four way control", "door panel"])
def _(S):
    return [shell(circle(12, 12, 3.8)),
            line(poly([(9.8, 5.2), (12, 3), (14.2, 5.2)], r=S.r * 0.4)), line(poly([(9.8, 18.8), (12, 21), (14.2, 18.8)], r=S.r * 0.4)),
            line(poly([(5.2, 9.8), (3, 12), (5.2, 14.2)], r=S.r * 0.4)), line(poly([(18.8, 9.8), (21, 12), (18.8, 14.2)], r=S.r * 0.4))]


@T_("car-dome-light", "Oval ceiling lamp with a small switch and light rays shining down",
    ["interior light", "cabin light", "roof light", "map light", "courtesy light", "ceiling lamp", "car lamp"])
def _(S):
    return [shell(rect(3, 3.5, 18, 7.5, rr(S, 3.5))), knock(rect(10.3, 6, 3.4, 2.2, 1)),
            line(seg(7, 14.5, 5.5, 19)), line(seg(12, 14.5, 12, 20)), line(seg(17, 14.5, 18.5, 19))]


@T_("seat-memory-buttons", "Row of three small buttons marked with one, two and three dots beneath a tiny seat",
    ["memory seat", "seat position memory", "driver seat presets", "seat presets", "1 2 3 buttons", "seat control", "preset buttons"])
def _(S):
    return [shell(poly([(7.5, 2.5), (10.5, 2.5), (11.2, 7), (16.5, 7.5), (16.5, 9), (8, 9)], closed=True, r=S.r * 0.4)),
            shell(rect(3, 13, 4.2, 7.5, rr(S, 1.2))), shell(rect(9.9, 13, 4.2, 7.5, rr(S, 1.2))), shell(rect(16.8, 13, 4.2, 7.5, rr(S, 1.2))),
            knock(circle(5.1, 16.7, 0.65)), knock(circle(12, 15.5, 0.65)), knock(circle(12, 18, 0.65)),
            knock(circle(18.9, 15, 0.65)), knock(circle(18.9, 16.9, 0.65)), knock(circle(18.9, 18.8, 0.65))]


@T_("headrest-screen", "Back of a car headrest with a small video screen showing a play triangle",
    ["rear seat entertainment", "backseat screen", "headrest monitor", "car tv", "rear screen", "passenger screen", "in car video"])
def _(S):
    return [shell(rect(3, 2.5, 18, 15, rr(S, 5))), detail(rect(6.5, 6, 11, 8, 1)), knock(poly([(10.5, 8), (14, 10), (10.5, 12)], closed=True)),
            line(seg(8, 17.5, 8, 21.5)), line(seg(16, 17.5, 16, 21.5))]


@T_("car-grab-handle", "Curved grab handle mounted on the ceiling above a door window",
    ["assist handle", "roof handle", "ceiling grip", "passenger handle", "oh crap handle", "door grip", "car interior"])
def _(S):
    return [line(seg(2.5, 3, 21.5, 3)), line(poly([(6, 3), (6, 9), (18, 9), (18, 3)], r=S.r * 1.3)),
            shell(rect(3, 13.5, 18, 8, rr(S, 2.5)))]


@T_("window-tint", "Side window glass shaded with dense diagonal lines to show a tint film",
    ["tinted glass", "window film", "tinted windows", "privacy glass", "sun shade film", "car window", "darkened glass"])
def _(S):
    return [shell(poly([(3, 19.5), (6.5, 5), (17.5, 5), (21.5, 11.5), (21.5, 19.5)], closed=True, r=S.r)),
            detail(seg(8, 16.5, 12, 9)), detail(seg(13, 16.5, 17, 9)), detail(seg(18, 16.5, 20, 13))]


@T_("car-engine-bay", "Top view into an open engine compartment showing the engine, battery and fluid caps",
    ["engine compartment", "under the hood", "under the bonnet", "engine bay", "car engine", "open hood", "bonnet open"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, rr(S, 3))), detail(rect(8, 6, 8, 9, 1)), detail(rect(4.5, 16.5, 6, 2.5, 0.5)),
            dot(19.2, 6.5, 0.9), dot(19.2, 10.5, 0.9), dot(19.2, 14.5, 0.9)]


@T_("air-intake-snorkel", "Tall pipe running up the windshield pillar of an SUV with an angled scoop head at the top",
    ["snorkel", "raised air intake", "wading snorkel", "off road snorkel", "4x4 snorkel", "river crossing", "intake pipe"])
def _(S):
    return [shell(poly([(2.5, 21), (2.5, 15), (8, 14.5), (12, 8.5), (21.5, 8.5), (21.5, 21)], closed=True, r=S.r * 0.5)),
            line(seg(6.5, 14.5, 6.5, 5.5)), shell(poly([(3, 2.5), (9, 2.5), (9, 6.5), (3, 4.5)], closed=True, r=S.r * 0.2))]


@T_("cone-air-filter", "Pleated cone shaped performance air filter clamped onto the end of an intake pipe",
    ["performance air filter", "intake filter", "cold air intake", "pod filter", "k and n style filter", "air cleaner", "car tuning"])
def _(S):
    return [shell(rect(2.5, 9.5, 4.5, 5, rr(S, 1))),
            shell(poly([(8.5, 9.5), (21.5, 4), (21.5, 20), (8.5, 14.5)], closed=True, r=S.r * 0.4)),
            detail(seg(13, 9.5, 13, 14.5)), detail(seg(17.5, 8, 17.5, 16))]


@T_("nitrous-bottle", "Tall slim pressure bottle with a valve on top and a braided hose leading to the side",
    ["nos bottle", "nitrous oxide", "nos tank", "n2o bottle", "power adder", "drag racing", "gas cylinder"])
def _(S):
    return [shell(rect(6.5, 9, 9, 12.5, rr(S, 3.5))), detail(seg(6.5, 13, 15.5, 13)), shell(rect(9, 5.5, 4, 3.5, 0.5)),
            shell(rect(7.5, 2.5, 6, 3, 0.5)), line(poly([(13.5, 4), (19, 4), (19, 14)], r=S.r))]


def _ring(cy):
    import math as _m
    a1, a2 = _m.radians(25), _m.radians(-25)
    x1, y1 = 12 + 9.5 * _m.cos(a1), cy + 3 * _m.sin(a1)
    x2, y2 = 12 + 9.5 * _m.cos(a2), cy + 3 * _m.sin(a2)
    return f"M{fmt(x1)} {fmt(y1)}A9.5 3 0 1 1 {fmt(x2)} {fmt(y2)}"


@T_("piston-rings", "Three thin split rings stacked one above the other with a small gap in each ring",
    ["piston ring set", "compression rings", "oil control ring", "engine rebuild", "ring gap", "engine parts", "cylinder rings"])
def _(S):
    return [line(_ring(6)), line(_ring(12)), line(_ring(18))]


@T_("engine-thermostat", "Flat valve disc held by two arms over a coil spring and a wax pellet stem",
    ["coolant thermostat", "thermostat valve", "wax pellet", "cooling valve", "engine temperature", "coolant control", "radiator valve"])
def _(S):
    return [shell(rect(3.5, 2.5, 17, 3.5, rr(S, 1.5))),
            line(poly([(8.5, 7.5), (15.5, 9.5), (8.5, 11.5), (15.5, 13.5)], r=S.r * 0.3)),
            shell(rect(10, 15, 4, 6.5, rr(S, 1.5))),
            line(poly([(5, 6), (5, 17), (9, 17)], r=S.r * 0.5)), line(poly([(19, 6), (19, 17), (15, 17)], r=S.r * 0.5))]


@T_("hybrid-powertrain", "Engine block and battery both linked to an electric motor that drives a wheel",
    ["hybrid drivetrain", "hybrid system", "phev", "electric motor", "hybrid car", "engine and battery", "powertrain"])
def _(S):
    return [shell(rect(2.5, 3, 6.5, 7, S.R * 0.7)), shell(rect(2.5, 14, 6.5, 7, S.R * 0.7)),
            shell(circle(14, 12, 3)), line(poly([(9, 6.5), (14, 6.5), (14, 9)], r=S.r * 0.5)),
            line(poly([(9, 17.5), (14, 17.5), (14, 15)], r=S.r * 0.5)), line(seg(17, 12, 19.5, 12)),
            shell(rect(19.5, 6.5, 2.5, 11, rr(S, 1)))]
