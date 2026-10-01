"""TypeIcon Core: automotive (batch 003): chassis and body parts, tire wear, garage tools, dashboard pictograms.

Objects are drawn flat from the front or side. Side-view cars face right with wheels on one ground line.
"""
from __future__ import annotations

import math

from dsl import (  # noqa: F401
    D, P, ST, U, Part, Style, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d, poly,
    rect, regular, seg, shell, solid,
)
from geometry import polar

CAT = "automotive"


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def knock(d):
    return Part("dot", d)


def head(tip, deg, size=2.6, spread=40):
    a = polar(tip[0], tip[1], size, deg + 180 - spread)
    b = polar(tip[0], tip[1], size, deg + 180 + spread)
    return [a, tip, b]


def drop(cx, cy, s=1.0):
    return (f"M{fmt(cx)} {fmt(cy - 2.6 * s)}C{fmt(cx)} {fmt(cy - 2.6 * s)} {fmt(cx - 2.2 * s)} {fmt(cy)} {fmt(cx - 2.2 * s)} {fmt(cy + 1.0 * s)}"
            f"A{fmt(2.2 * s)} {fmt(2.2 * s)} 0 0 0 {fmt(cx + 2.2 * s)} {fmt(cy + 1.0 * s)}C{fmt(cx + 2.2 * s)} {fmt(cy)} {fmt(cx)} {fmt(cy - 2.6 * s)} {fmt(cx)} {fmt(cy - 2.6 * s)}Z")


def rot(pts, deg=-45, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c) for x, y in pts]


def rp(pts, closed=True, r=0.0, deg=-45):
    return poly(rot(pts, deg), closed=closed, r=r)


def rseg(x1, y1, x2, y2, deg=-45):
    (a, b), (c, d) = rot([(x1, y1), (x2, y2)], deg)
    return seg(a, b, c, d)


def A_(name, description, tags, aliases=()):
    def deco(fn):
        return icon(name, CAT, description, tags=tags, aliases=aliases)(fn)
    return deco


# =========================================================================== chunk 1

@A_("ladder-frame-chassis", "Top view of two long steel rails joined by crossmembers like a ladder",
    ["chassis", "frame", "truck frame", "rails", "crossmember", "underbody", "body on frame"])
def _(S):
    return [line(poly([(8, 2.5), (6, 7), (6, 21.5)], r=S.r)), line(poly([(16, 2.5), (18, 7), (18, 21.5)], r=S.r)),
            line(seg(6.5, 9, 17.5, 9)), line(seg(6.5, 14, 17.5, 14)), line(seg(6.5, 19, 17.5, 19)),
            line(seg(7.2, 4.5, 16.8, 4.5))]


@A_("racing-roll-cage", "Side view of a tubular steel cage shaped like a car cabin with diagonal braces",
    ["roll cage", "roll bar", "safety cage", "motorsport", "tubular frame", "race car", "rollover protection"])
def _(S):
    return [shell(poly([(3, 20), (6, 8), (11, 4), (17, 4), (21, 11), (21, 20)], closed=True, r=S.r)),
            detail(seg(6.5, 20, 17, 4)), detail(seg(12.5, 4, 12.5, 20))]


@A_("bucket-seat", "Side view of a deep racing seat with a tall backrest and harness slots",
    ["racing seat", "sport seat", "car seat", "harness seat", "bolster", "motorsport", "driver seat"])
def _(S):
    return [shell(poly([(7, 2.5), (17, 2.5), (18, 11), (21, 13), (21, 21.5), (3, 21.5), (3, 13), (6, 11)], closed=True, r=S.r)),
            detail(seg(10, 5.5, 10, 9)), detail(seg(14, 5.5, 14, 9)), detail(seg(6.5, 16, 17.5, 16))]


@A_("air-suspension", "Rubber air spring with two rolled lobes between top and bottom plates and an air line",
    ["air spring", "air ride", "bellows", "air bag suspension", "airbag", "ride height", "truck suspension"])
def _(S):
    return [line(seg(7, 3, 17, 3)), line(seg(7, 21, 17, 21)),
            shell(union(ellipse(12, 9, 6, 3), ellipse(12, 15.5, 6, 3))),
            line(poly([(17, 3), (21, 3), (21, 9)], r=S.r))]


def _crescent():
    return ("M3 18A9.9 9.9 0 0 1 21 18L16 18A5.4 5.4 0 0 0 8 18Z")


@A_("brake-shoe", "Curved crescent brake shoe with a friction lining along its outer edge and spring holes",
    ["drum brake shoe", "brake lining", "friction", "brake pad", "drum brake", "brake part", "crescent"])
def _(S):
    return [shell(_crescent()), detail(arc(12, 13.9, 7.4, 222, 318)), dot(5.5, 16.4, 0.9), dot(18.5, 16.4, 0.9)]


@A_("washer-fluid-reservoir", "Plastic tank with a flip cap marked with a windshield spray symbol and a hose at its base",
    ["washer fluid", "wiper fluid", "windshield washer", "screenwash", "fluid tank", "windscreen washer", "coolant tank"])
def _(S):
    return [shell(rect(3, 8, 13, 13, rr(S, 3))), shell(rect(5, 3.5, 5, 4.5, 0.5)),
            knock(drop(9.5, 14, 1.4)),
            line(poly([(16, 17), (20, 17), (20, 12)], r=S.r))]


@A_("run-flat-tire", "Tire with a stiff inner support ring holding up a deflated, flattened tread",
    ["runflat", "run flat tyre", "self supporting tire", "deflated tire", "tire", "tyre", "puncture proof"])
def _(S):
    return [shell("M7.25 19.7A9.5 9.5 0 1 1 16.75 19.7Z"), detail(poly(regular(12, 11, 5, 6), closed=True, r=S.r * 1.6)), dot(12, 11, 1.3)]


@A_("aquaplaning", "Tire rolling on a film of water with spray fanning out from its sides and a wavy water line",
    ["hydroplaning", "wet road", "aquaplane", "skid", "water on road", "rain driving", "loss of grip"])
def _(S):
    return [shell(circle(12, 9, 5)), dot(12, 9, 1.2),
            line(seg(19, 7, 21.5, 5)), line(seg(19.5, 10.5, 22, 10.5)),
            line(seg(5, 7, 2.5, 5)), line(seg(4.5, 10.5, 2, 10.5)),
            line("M2.5 19.5q2.4-2.5 4.75 0t4.75 0 4.75 0 4.75 0")]


@A_("worn-tire", "Tire tread section with grooves fading away into a smooth bald patch",
    ["bald tire", "tread wear", "tyre wear", "tread depth", "worn tyre", "tire replacement", "tire inspection"])
def _(S):
    return [shell(poly([(2.5, 20), (2.5, 5), (6, 5), (6, 10), (9, 10), (9, 8), (12, 8), (12, 10), (21.5, 10), (21.5, 20)],
                       closed=True, r=S.r * 0.4)),
            detail(seg(5, 15, 19, 15))]


@A_("grit-guard-bucket", "Wash bucket with a grid insert near the bottom and a carry handle",
    ["wash bucket", "car wash bucket", "detailing bucket", "dirt trap", "two bucket wash", "pail", "car cleaning"])
def _(S):
    return [shell(poly([(3.5, 9), (5.5, 21), (18.5, 21), (20.5, 9)], closed=True, r=S.r)),
            line("M4 9C4 2.5 20 2.5 20 9"), detail(seg(6, 15.5, 18, 15.5)), detail(seg(9, 15.5, 9, 21)),
            detail(seg(15, 15.5, 15, 21))]


@A_("ceramic-coating", "Car paint panel with round water beads sitting on its glossy coated surface",
    ["nano coating", "paint protection", "hydrophobic", "water beading", "car detailing", "gloss", "sealant"])
def _(S):
    return [shell(union(rect(2.5, 14, 19, 7, rr(S, 2)), circle(6.5, 14, 2.5), circle(12.5, 14, 3.2), circle(18, 14, 2))),
            line(seg(5, 18, 9, 18))]


@A_("paint-scratch", "Car door panel with a long jagged scratch across its painted surface",
    ["scratched paint", "car scratch", "paint damage", "key scratch", "dent repair", "body shop", "scuff"])
def _(S):
    return [shell(rect(2.5, 4.5, 19, 15, rr(S, 3))),
            line(poly([(5.5, 17), (8.5, 14), (11, 16.5), (14, 13.5), (16, 16), (19, 12.5)])), detail(seg(14, 8.5, 19, 8.5))]


@A_("car-rust", "Lower car door panel with blotchy rust patches and small holes",
    ["rusty car", "corrosion", "rust spots", "body rot", "oxidation", "rust repair", "car body damage"])
def _(S):
    return [shell(poly([(2.5, 5), (21.5, 5), (21.5, 19), (18.5, 17), (15.5, 19.5), (12, 17.5), (9, 19.5), (5.5, 17.5), (2.5, 19)],
                       closed=True, r=S.r * 0.5)),
            dot(7, 10, 1.6), dot(13, 11.5, 2), dot(18, 9.5, 1.2)]


@A_("oil-change-sticker", "Small square windshield sticker with an oil can symbol and a date line",
    ["service sticker", "oil change reminder", "maintenance sticker", "service due", "oil service", "next service", "windshield label"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, rr(S, 3))), knock(drop(12, 9.5, 1.5)),
            detail(seg(6, 18, 18, 18))]


@A_("tire-recycling", "Tire standing upright inside a loop of three recycling arrows",
    ["tyre recycling", "tire disposal", "rubber recycling", "reuse tires", "circular economy", "tire waste", "recycle"])
def _(S):
    out = [shell(circle(12, 12, 4.3)), dot(12, 12, 1.2)]
    for a0 in (-75, 45, 165):
        a1 = a0 + 80
        out.append(line(arc(12, 12, 9, a0, a1)))
        out.append(line(poly(head(polar(12, 12, 9, a1), a1 + 90, 2.6), r=0)))
    return out


# =========================================================================== chunk 2

@A_("scrap-car", "Flattened crushed car block stacked on top of another crushed block",
    ["crushed car", "car crusher", "junkyard", "salvage", "wrecked car", "end of life vehicle", "scrapyard"])
def _(S):
    return [shell(rect(3, 13, 18, 8.5, rr(S, 2))), shell(rect(6, 3, 12, 8, rr(S, 2))),
            detail(poly([(6, 18), (9, 15.5), (12, 18), (15, 15.5), (18, 18)])), detail(seg(9, 7, 15, 7))]


@A_("car-turntable", "Car on a round rotating floor platform in a showroom or garage",
    ["rotating platform", "car display", "showroom", "vehicle turntable", "revolving stage", "car rotation", "garage floor"])
def _(S):
    return [shell(ellipse(12, 19, 9.5, 2.5)),
            shell(poly([(4, 13.5), (4, 10.5), (7, 9), (9, 5), (15, 5), (17.5, 9), (20, 10.5), (20, 13.5)], closed=True, r=S.r)),
            dot(8, 14, 1.6), dot(16, 14, 1.6)]


@A_("exhaust-extraction-hose", "Flexible ceiling hose hanging down and clamped over a car tailpipe",
    ["exhaust fume extractor", "garage ventilation", "tailpipe hose", "fume removal", "workshop exhaust", "emissions test", "ceiling hose"])
def _(S):
    return [line(seg(3, 3, 13, 3)), line("M8 3C8 11 14 8 14 14"), shell(rect(11, 14, 6, 5, rr(S, 1.5))),
            line(seg(17, 16.5, 20, 16.5)), line(seg(20, 11, 20, 22))]


@A_("oil-drain-plug", "Hex-head drain bolt with a crush washer and a threaded shaft",
    ["sump plug", "drain bolt", "oil pan plug", "crush washer", "engine oil", "oil change", "sump"])
def _(S):
    return [shell(rect(6, 2.5, 12, 5.5, rr(S, 1.5))), line(seg(5, 10.5, 19, 10.5)), shell(rect(8.5, 12.5, 7, 9)),
            detail(seg(8.5, 15.5, 15.5, 15.5)), detail(seg(8.5, 18.5, 15.5, 18.5))]


@A_("bodywork-hammer", "Panel beating hammer with a round face beside a curved steel dolly block",
    ["panel beater", "dolly", "body hammer", "dent repair", "auto body", "metalwork", "hammer and dolly"])
def _(S):
    return [shell(rect(2.5, 3.5, 8, 5.5, rr(S, 2))), line(seg(6.5, 9, 6.5, 21.5)),
            shell("M13.5 21.5V14Q13.5 8.5 17.75 8.5Q22 8.5 22 14V21.5Z")]


@A_("vehicle-registration", "Folded document with a small solid car silhouette",
    ["car registration", "vehicle papers", "logbook", "title document", "car documents", "license papers", "dmv paperwork"])
def _(S):
    return [shell(poly([(5, 2.5), (14, 2.5), (19, 7.5), (19, 21.5), (5, 21.5)], closed=True, r=S.r)),
            detail(poly([(14, 2.5), (14, 7.5), (19, 7.5)])),
            knock(poly([(7.5, 17), (7.5, 14.5), (9, 12), (15, 12), (16.5, 14.5), (16.5, 17)], closed=True))]


@A_("vin-plate", "Small metal plate with rivets and a row of code characters",
    ["vin", "vehicle identification number", "chassis number", "id plate", "serial plate", "car identity", "data plate"])
def _(S):
    return [shell(rect(2.5, 7, 19, 10, rr(S, 2))), detail(seg(9, 10.5, 9, 13.5)), detail(seg(12, 10.5, 12, 13.5)),
            detail(seg(15, 10.5, 15, 13.5)), dot(5.5, 12, 0.9), dot(18.5, 12, 0.9)]


@A_("oil-leak", "Underside of a car with a drip falling onto a puddle on the ground",
    ["leaking oil", "fluid leak", "drip", "puddle", "engine leak", "car problem", "garage floor stain"])
def _(S):
    return [shell(poly([(3, 9), (3, 6), (7, 3.5), (17, 3.5), (21, 6), (21, 9)], closed=True, r=S.r)),
            knock(drop(12, 14.2, 1.2)), solid(ellipse(12, 20, 7.5, 1.8))]


def _car(S, ox=0.0):
    return poly([(2.5 + ox, 16), (2.5 + ox, 13), (4.5 + ox, 12), (6 + ox, 9), (10 + ox, 9), (11.5 + ox, 12), (13 + ox, 13), (13 + ox, 16)],
                closed=True, r=S.r)


@A_("trailer-connected-light", "Dashboard pictogram of a small car towing a box trailer behind it",
    ["trailer light", "towing indicator", "tow hitch warning", "caravan connected", "trailer plugged in", "dashboard symbol", "towbar"])
def _(S):
    return [shell(_car(S)), dot(5.5, 17, 1.6), dot(10.5, 17, 1.6), line(seg(13, 14.5, 15.5, 14.5)),
            shell(rect(15.5, 8.5, 6, 8, rr(S, 1.5))), dot(18.5, 17.5, 1.6)]


@A_("ev-ready-light", "Dashboard pictogram of a side-view car with a double-headed arrow beneath it",
    ["electric vehicle ready", "ev ready", "ready to drive", "electric car indicator", "ready light", "dashboard symbol", "vehicle on"])
def _(S):
    return [shell(poly([(3, 14), (3, 11), (6, 9.5), (8, 5.5), (16, 5.5), (19, 9.5), (21, 11), (21, 14)], closed=True, r=S.r)),
            dot(7.5, 15, 1.8), dot(16.5, 15, 1.8), line(seg(4, 20.5, 20, 20.5)),
            line(poly(head((3.5, 20.5), 180, 2.4), r=0)), line(poly(head((20.5, 20.5), 0, 2.4), r=0))]


@A_("seat-recline", "Side view of a car seat with the backrest tilting back and a curved arrow beside it",
    ["reclining seat", "seat tilt", "seat adjustment", "backrest angle", "seat lever", "lie back", "power seat"])
def _(S):
    return [shell(poly([(5, 3), (9.5, 3.5), (10.5, 13), (17.5, 13), (17.5, 20), (3.5, 20)], closed=True, r=S.r)),
            line(arc(14, 9, 5.5, -100, -10)), line(poly(head(polar(14, 9, 5.5, -10), 80, 2.4), r=0))]


@A_("window-regulator", "Scissor arm mechanism inside a door outline lifting the bottom edge of a window pane",
    ["window lift", "power window mechanism", "door glass lifter", "window winder", "scissor lift", "car door", "window motor"])
def _(S):
    return [shell(rect(3.5, 3.5, 17, 17, rr(S, 2.5))), detail(seg(3.5, 8.5, 20.5, 8.5)),
            detail(seg(7.5, 8.5, 16.5, 20.5)), detail(seg(16.5, 8.5, 7.5, 20.5)), dot(12, 14.5, 1.3)]


@A_("gas-strut", "Slim gas spring cylinder with a thinner rod and ball joint ends",
    ["gas spring", "tailgate strut", "bonnet strut", "hood lifter", "lift support", "shock", "damper"])
def _(S):
    return [shell(rp([(7, 9.5), (15, 9.5), (15, 14.5), (7, 14.5)], r=S.r * 0.4)),
            line(rseg(3.8, 12, 7, 12)), line(rseg(15, 12, 20, 12)),
            dot(*rot([(3.2, 12)])[0], 1.7), dot(*rot([(21, 12)])[0], 1.7)]


@A_("torque-converter", "Round housing with a hex hub in the center and a ring of bolt studs around its face",
    ["automatic transmission", "fluid coupling", "converter", "transmission part", "stall speed", "drivetrain", "flexplate"])
def _(S):
    out = [shell(circle(12, 12, 9.5)), shell(poly(regular(12, 12, 3.2, 6), closed=True, r=S.r * 1.2))]
    for i in range(6):
        x, y = polar(12, 12, 6.5, 30 + i * 60)
        out.append(dot(x, y, 0.9))
    return out


@A_("cvt-transmission", "Two cone pulleys facing opposite ways linked by a steel belt",
    ["continuously variable transmission", "variable pulleys", "belt drive", "gearbox", "drivetrain", "automatic gearbox", "pulley cones"])
def _(S):
    return [shell(poly([(2.5, 4), (9.5, 8), (9.5, 16), (2.5, 20)], closed=True, r=S.r)),
            shell(poly([(14.5, 8), (21.5, 4), (21.5, 20), (14.5, 16)], closed=True, r=S.r)),
            line(seg(9.5, 8.5, 14.5, 8.5)), line(seg(9.5, 15.5, 14.5, 15.5))]


# =========================================================================== chunk 3

def _autogas_filled():
    body = U(P(circle(12, 13.5, 9.5)), P(poly([(8.5, 2.5), (15.5, 2.5), (14.5, 8), (9.5, 8)], closed=True)))
    return D(body, P(circle(12, 13.5, 3)))


@icon("autogas-tank", CAT, "Donut shaped toroidal fuel tank lying flat with a valve block on its top edge",
      tags=["lpg tank", "toroidal tank", "propane tank", "autogas", "spare wheel tank", "gas cylinder", "fuel tank"],
      filled=_autogas_filled)
def _(S):
    return [shell(union(circle(12, 13.5, 8.5), poly([(9, 3), (15, 3), (14, 8), (10, 8)], closed=True, r=S.r))),
            shell(poly(regular(12, 13.5, 3.2, 8, start=22.5), closed=True, r=S.r * 1.6))]


@A_("wheel-bolt-pattern", "Wheel hub face with five evenly spaced stud holes around a center hub",
    ["bolt circle", "lug pattern", "pcd", "wheel fitment", "stud holes", "lug nuts", "rim size"])
def _(S):
    out = [shell(circle(12, 12, 9.5)), shell(poly(regular(12, 12, 2.4, 6), closed=True, r=S.r))]
    for i in range(5):
        x, y = polar(12, 12, 5.8, -90 + i * 72)
        out.append(dot(x, y, 1.2))
    return out


@A_("tire-snow-sock", "Tire wrapped in a fitted fabric sock with a woven zigzag over the tread",
    ["snow sock", "textile chain", "traction cover", "winter tire cover", "snow chains alternative", "ice grip", "tyre sock"])
def _(S):
    pts = []
    for i in range(18):
        pts.append(polar(12, 12, 5.2 if i % 2 else 7.2, i * 20))
    return [shell(circle(12, 12, 9.5)), detail(poly(pts, closed=True)), dot(12, 12, 1.5)]


@A_("tire-patch", "Round rubber repair patch with a short plug stem standing up from its center",
    ["mushroom plug", "puncture repair", "tyre patch", "tire repair", "rubber patch", "flat repair", "plug patch"])
def _(S):
    return [shell(union(ellipse(12, 17.5, 9.5, 3.5), rect(10, 3, 4, 14))), detail(seg(6, 17.5, 18, 17.5))]


@A_("brake-bleeder", "Catch bottle with a clear hose running up to a bleed nipple on a brake caliper",
    ["brake bleeding", "bleed kit", "brake fluid", "hydraulic brake service", "catch bottle", "caliper bleed", "brake service"])
def _(S):
    return [shell(union(rect(3, 12, 8, 9.5, rr(S, 2.5)), rect(5.5, 9, 3, 4))), knock(circle(7, 17, 1.3)),
            line("M7 9V6.5Q7 4.5 9 4.5H14.5"), shell(rect(14.5, 2.5, 7, 10, rr(S, 2.5)))]


@A_("headlight-aimer", "Boxy optical aiming unit on a wheeled pole stand facing a car headlamp",
    ["headlamp aligner", "beam setter", "headlight alignment", "light beam test", "mot test", "optical unit", "headlight adjust"])
def _(S):
    return [shell(rect(2.5, 3, 11, 9, rr(S, 2))), dot(8, 7.5, 2), line(seg(7.5, 12, 7.5, 18.5)),
            line(seg(3.5, 18.5, 11.5, 18.5)), dot(4.5, 21, 1.1), dot(10.5, 21, 1.1), shell(circle(19, 8, 2.6))]


@A_("grease-nipple", "Small hex base grease fitting with a rounded ball tip",
    ["zerk fitting", "grease fitting", "lubrication point", "grease point", "chassis lube", "fitting", "lubricate"])
def _(S):
    return [shell(union(circle(12, 6, 3.2), rect(10.3, 6, 3.4, 6))), shell(poly([(4.5, 14.5), (7.5, 12), (16.5, 12), (19.5, 14.5), (16.5, 17), (7.5, 17)], closed=True, r=S.r)),
            shell(rect(8.5, 17.5, 7, 4))]


@A_("mechanics-stethoscope", "Two earpieces joined to a long metal probe rod instead of a chest piece",
    ["engine stethoscope", "noise finder", "listen to engine", "diagnostic probe", "mechanic tool", "sound detector", "garage diagnosis"])
def _(S):
    return [dot(7, 3.5, 1.4), dot(17, 3.5, 1.4), line("M7 5V9Q7 13 12 13"), line("M17 5V9Q17 13 12 13"),
            line(seg(12, 13, 12, 15)),
            shell(poly([(9.5, 15), (14.5, 15), (14.5, 18.5), (12, 22), (9.5, 18.5)], closed=True, r=S.r))]


@A_("ac-manifold-gauge", "Two round pressure gauges side by side on a manifold block with two hoses hanging below",
    ["air conditioning gauges", "refrigerant gauges", "hvac gauge set", "ac service", "pressure gauge", "recharge", "manifold set"])
def _(S):
    return [shell(circle(6.5, 8, 4)), shell(circle(17.5, 8, 4)), shell(rect(3, 14.5, 18, 3.5, rr(S, 1.5))),
            detail(seg(6.5, 8, 8.2, 6.4)), detail(seg(17.5, 8, 15.8, 6.4)),
            line(seg(7, 18, 7, 22)), line(seg(17, 18, 17, 22))]


@A_("refrigerant-can", "Squat pressure can with a tap valve on top and a short charging hose",
    ["ac recharge can", "freon can", "coolant gas", "air conditioning refill", "r134a", "charging hose", "aerosol can"])
def _(S):
    return [shell(rect(3.5, 10.5, 11, 11, rr(S, 2.5))), line(seg(6, 6.5, 12, 6.5)), line(seg(9, 6.5, 9, 10.5)),
            line(poly([(14.5, 14), (19, 14), (19, 17.5)], r=S.r)), shell(rect(17, 17.5, 4, 4, 0.5)),
            detail(seg(9, 13.5, 9, 18.5)), detail(seg(6.5, 16, 11.5, 16))]


@A_("car-rotisserie", "Car body shell held between two stands that let it rotate on a central axis",
    ["body rotisserie", "car restoration", "body spit", "rotating stand", "chassis stand", "restoration shop", "classic car build"])
def _(S):
    return [shell(poly([(7.5, 15), (7.5, 12), (9, 10.5), (10, 7.5), (14, 7.5), (15, 10.5), (16.5, 12), (16.5, 15)], closed=True, r=S.r)),
            line(seg(3.5, 11, 7.5, 11)), line(seg(16.5, 11, 20.5, 11)),
            line(seg(3.5, 11, 3.5, 21.5)), line(seg(20.5, 11, 20.5, 21.5)),
            line(seg(2.5, 21, 7, 21)), line(seg(17, 21, 21.5, 21))]


@A_("car-show", "Car silhouette on a low podium with two spotlight beams shining down on it",
    ["auto show", "car exhibition", "motor show", "showroom display", "spotlight", "concours", "car meet"])
def _(S):
    return [shell(rect(3, 17, 18, 4.5, rr(S, 2))),
            shell(poly([(6, 14.5), (6, 12), (8, 10.5), (9.5, 8), (14.5, 8), (16.5, 10.5), (18, 12), (18, 14.5)], closed=True, r=S.r)),
            line(seg(3, 3, 7, 7)), line(seg(21, 3, 17, 7))]


@A_("shift-lights", "Row of small round lights across the top of a steering wheel rim lighting up in sequence",
    ["rpm lights", "shift indicator", "racing wheel", "rev lights", "steering wheel leds", "motorsport", "upshift light"])
def _(S):
    out = [shell(rect(2.5, 3.5, 19, 17, S.R * 1.5)), detail(seg(2.5, 14, 21.5, 14))]
    for k in range(5):
        out.append(dot(6.5 + k * 2.75, 8, 1.0))
    return out


@A_("fan-speed-knob", "Round climate knob with a three blade fan symbol and ticks growing taller around its edge",
    ["blower speed", "fan control", "ventilation knob", "air flow dial", "hvac knob", "dashboard control", "blower"])
def _(S):
    out = [shell(circle(12, 13.5, 5.5)), dot(12, 13.5, 1)]
    for ang in (270, 30, 150):
        x, y = polar(12, 13.5, 3.2, ang)
        out.append(detail(seg(12, 13.5, x, y)))
    for k, ang in enumerate((200, 235, 270, 305, 340)):
        r0 = 7.9
        r1 = r0 + 0.8 + 0.35 * k
        a = polar(12, 13.5, r0, ang)
        b = polar(12, 13.5, r1, ang)
        out.append(line(seg(a[0], a[1], b[0], b[1])))
    return out


@A_("climate-temperature-knob", "Round climate knob with a pointer and an arc running from a cold plus to a hot flame drop",
    ["temperature dial", "heater knob", "hot cold control", "ac temperature", "hvac dial", "dashboard control", "thermostat knob"])
def _(S):
    return [shell(circle(12, 12, 5.2)), detail(seg(12, 12, 12, 8.5)), line(arc(12, 12, 9.2, 180, 360)),
            line(seg(4, 15.5, 4, 20)), line(seg(2, 17.75, 6, 17.75)), knock(drop(20, 17, 1.2))]


@A_("off-road-light-bar", "Long bar of small LED cells mounted above a four by four windshield",
    ["led light bar", "roof light bar", "4x4 lights", "driving lights", "spot lights", "overland", "truck accessories"])
def _(S):
    return [shell(rect(3, 3, 18, 5, rr(S, 1.5))), dot(6.5, 5.5, 0.9), dot(10, 5.5, 0.9), dot(14, 5.5, 0.9),
            dot(17.5, 5.5, 0.9), shell(poly([(3, 21.5), (6, 12), (18, 12), (21, 21.5)], closed=True, r=S.r))]


@A_("high-lift-jack", "Tall perforated steel bar with a sliding lifting nose and a long lever",
    ["farm jack", "off road jack", "hi lift", "bumper jack", "lifting jack", "recovery jack", "4x4 recovery"])
def _(S):
    return [shell(rect(7, 2.5, 5, 19, rr(S, 1.5))), dot(9.5, 6, 0.8), dot(9.5, 10, 0.8), dot(9.5, 14, 0.8),
            shell(rect(12, 9, 7, 3.5, rr(S, 1))), line(seg(12, 5.5, 21.5, 3)), shell(rect(3, 19.5, 13, 2, 0.5))]


@A_("vehicle-awning", "Side view of an SUV with a fabric awning rolled out from its roof on a pole",
    ["car awning", "roof rack awning", "camping shade", "overland awning", "4x4 camping", "suv shade", "vehicle shelter"])
def _(S):
    return [shell(poly([(9.5, 20), (9.5, 12.5), (11, 10.5), (12.5, 7), (18, 7), (21.5, 11), (21.5, 20)], closed=True, r=S.r)),
            dot(13, 20, 1.6), dot(19, 20, 1.6),
            shell(poly([(12, 5.5), (2.5, 8), (2.5, 10.5), (12, 8.5)], closed=True, r=S.r * 0.4)),
            line(seg(3.5, 10.5, 3.5, 21.5))]


@A_("insect-splatter", "Windshield outline with splat marks of squashed bugs on the glass",
    ["bug splatter", "bug splat", "dirty windshield", "windscreen", "insects on glass", "car cleaning", "summer driving"])
def _(S):
    return [shell(poly([(5.5, 4.5), (18.5, 4.5), (21.5, 19.5), (2.5, 19.5)], closed=True, r=S.r)),
            dot(8, 10, 1.6), dot(10.5, 8.5, 0.7), dot(5.8, 12.5, 0.7), dot(8.8, 13.5, 0.7),
            dot(16, 14.5, 1.8), dot(18.5, 12, 0.7), dot(13.5, 16.5, 0.7), dot(16.5, 10, 0.8)]


@A_("dual-exhaust-tips", "Rear bumper edge with two round exhaust tips poking out side by side beneath it",
    ["twin exhaust", "tailpipes", "exhaust tips", "performance exhaust", "tail pipes", "rear bumper", "sports exhaust"])
def _(S):
    return [shell(rect(2.5, 3, 19, 5, S.R)),
            shell(poly(regular(7, 16, 3.6, 8, start=22.5), closed=True, r=S.r * 1.6)),
            shell(poly(regular(17, 16, 3.6, 8, start=22.5), closed=True, r=S.r * 1.6))]


@A_("hood-scoop", "Side view of a car hood with a raised open air scoop bulging up from its middle",
    ["bonnet scoop", "air intake", "muscle car", "engine air scoop", "hood vent", "performance hood", "cowl induction"])
def _(S):
    return [shell(poly([(2.5, 19.5), (2.5, 14), (8, 14), (9, 8.5), (16, 8.5), (17, 14), (21.5, 14), (21.5, 19.5)], closed=True, r=S.r)),
            knock(rect(10.5, 10, 5, 2.4, 0.5))]


@A_("skid-plate", "Flat metal plate with bolt holes and pressed ribs fitted under the front of a 4x4",
    ["bash plate", "underbody guard", "sump guard", "underbody protection", "armor plate", "off road protection", "4x4 accessory"])
def _(S):
    return [shell(poly([(5, 18), (2.5, 6.5), (21.5, 6.5), (19, 18)], closed=True, r=S.r)),
            detail(seg(10, 9.5, 10, 15)), detail(seg(14, 9.5, 14, 15)), dot(5.5, 9.5, 0.9), dot(18.5, 9.5, 0.9)]


@A_("chassis-dynamometer", "Side view of a car with its drive wheels sitting on a pair of rollers set into the floor",
    ["dyno", "rolling road", "power test", "horsepower test", "dynamometer", "tuning", "engine test"])
def _(S):
    return [shell(poly([(3, 14), (3, 11), (6, 9.5), (8, 6), (16, 6), (19, 9.5), (21, 11), (21, 14)], closed=True, r=S.r)),
            dot(7.5, 14.5, 2), dot(16.5, 14.5, 2), dot(5.5, 20, 1.4), dot(9.5, 20, 1.4), dot(14.5, 20, 1.4), dot(18.5, 20, 1.4)]


@A_("hand-driving-controls", "Steering wheel with a push pull hand lever mounted below it for accelerator and brake",
    ["adaptive driving", "hand controls", "disabled driver", "accessible vehicle", "wheelchair driver", "brake lever", "adapted car"])
def _(S):
    return [shell(circle(13, 8.5, 6)), detail(seg(7, 8.5, 19, 8.5)), detail(seg(13, 8.5, 13, 14.5)),
            line(seg(13, 15, 13, 17)), line(seg(13, 17, 7, 21)), dot(6.5, 21, 1.6)]
