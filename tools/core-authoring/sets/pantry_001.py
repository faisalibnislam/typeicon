"""TypeIcon Core: pantry (batch pantry_001): cans, tins, jars, boxes, bags, bottles and pantry packaging.

Containers are drawn in side view. Label pictures are small solid marks (knocked out of the Filled body)
placed between two rim lines so they stay readable at 24 px.
"""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, pt_on, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, path_to_d

CAT = "pantry"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def hole(d):
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


def ring(cx, cy, ro, ri):
    return minus(circle(cx, cy, ro), circle(cx, cy, ri))


def rot(pts, deg, cx, cy):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def thick(d, w):
    """Stroke a path into a solid shape of width w (for small label marks)."""
    return path_to_d(ST(d, w, "round", "round", 4))


def jar(S, x0=5, x1=19, top=3, neck=6, bottom=21, lid=(None, None), cap=4):
    """Jar: lid block over a body, one outline plus a detail line at the lid seam."""
    lx0, lx1 = lid if lid[0] is not None else (x0 + 1, x1 - 1)
    shape = union(rect(lx0, top, lx1 - lx0, neck - top + 1, L(S, 0, 1.2)),
                  rect(x0, neck, x1 - x0, bottom - neck, rr(S, cap)))
    return [shell(shape), detail(seg(lx0, neck, lx1, neck))]


def rell(cx, cy, rx, ry, deg, n=20):
    """Rotated ellipse as a polygon path (small label marks)."""
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + x * c - y * sn, cy + x * sn + y * c))
    return poly(pts, closed=True)


def can(S, x0=5, x1=19, y0=3, y1=21, ribs=True, cap=3):
    """Upright can with rim lines 3 px inside the top and bottom."""
    parts = [shell(rect(x0, y0, x1 - x0, y1 - y0, rr(S, cap if S.name == "rounded" else 1)))]
    if ribs:
        parts += [detail(seg(x0, y0 + 3, x1, y0 + 3)), detail(seg(x0, y1 - 3, x1, y1 - 3))]
    return parts


# ============================================================================ cans and tins

@icon("canned-tuna", CAT, "Short wide can with a pull ring on the lid and a fish on the label band",
      tags=["tuna can", "tinned fish", "canned fish", "seafood", "tin", "pantry", "pull tab"])
def _(S):
    return [shell(rect(3, 9, 18, 12, rr(S, 3))), detail(seg(3, 12, 21, 12)),
            line("M9.500 9a2.500 2.500 0 0 1 5 0"),
            hole(ellipse(10.5, 16.2, 3.6, 1.6)), hole(poly([(13.5, 16.2), (17.2, 14.2), (17.2, 18.2)], closed=True))]


@icon("canned-tomatoes", CAT, "Upright can with a tomato on the label band",
      tags=["tomato can", "tinned tomatoes", "chopped tomatoes", "passata", "pantry", "preserves"])
def _(S):
    return can(S) + [hole(circle(12, 13, 3.6)), hole(poly(regular(12, 8.8, 1.9, 5), closed=True))]


@icon("canned-corn", CAT, "Upright can with a corn cob and its husk leaves on the label band",
      tags=["sweetcorn can", "tinned corn", "maize", "canned vegetables", "pantry", "cob"])
def _(S):
    return can(S) + [hole(ellipse(12, 11.6, 1.9, 4)),
                     hole(poly([(12, 16.8), (8.4, 10.6), (9.2, 16.8)], closed=True)),
                     hole(poly([(12, 16.8), (15.6, 10.6), (14.8, 16.8)], closed=True))]


@icon("canned-beans", CAT, "Can with its lid peeled back and a heap of beans showing at the top",
      tags=["baked beans", "tinned beans", "open can", "pulses", "legumes", "pantry"])
def _(S):
    return [shell(rect(5, 10, 14, 11, rr(S, 3))), detail(seg(5, 18, 19, 18)),
            solid(ellipse(8, 7.6, 2.2, 1.5)), solid(ellipse(12, 6.4, 2.2, 1.5)), solid(ellipse(16, 7.6, 2.2, 1.5)),
            line("M19 10c1.500 0 2.500-1 2.500-3")]


@icon("canned-peaches", CAT, "Upright can with a halved peach and its pit on the label band",
      tags=["peach can", "tinned fruit", "canned fruit", "stone fruit", "pantry", "preserves", "syrup"])
def _(S):
    return can(S) + [hole(minus(union(circle(12, 13, 3.6), "M12 8.400L14.800 11.500H9.200Z"), circle(12, 13, 2.2))), hole(circle(12, 13, 1.1))]


@icon("canned-pineapple", CAT, "Upright can with a pineapple ring on the label band",
      tags=["pineapple can", "tinned pineapple", "pineapple rings", "canned fruit", "pantry", "tropical"])
def _(S):
    return can(S) + [hole(ring(12, 12, 4, 1.5))]


@icon("canned-soup", CAT, "Wide upright can with a steaming bowl on the label band",
      tags=["soup can", "tinned soup", "condensed soup", "broth", "pantry", "hot meal"])
def _(S):
    return can(S, 4, 20) + [hole("M8 12.300h8a4 4 0 0 1-8 0z"),
                            hole(rect(9, 8, 1.4, 3, 0.7)), hole(rect(11.3, 8, 1.4, 3, 0.7)), hole(rect(13.6, 8, 1.4, 3, 0.7))]


@icon("canned-coconut-milk", CAT, "Short can with a halved coconut and a milk drop on the label band",
      tags=["coconut milk", "coconut cream", "tinned coconut", "curry ingredient", "pantry", "dairy free"])
def _(S):
    return can(S, 4, 20, 5, 21, cap=2) + [
        hole(ring(9.5, 13.300, 3.2, 1.3)),
        hole("M16 10.500C14.600 12.300 14.300 13.300 14.300 14a1.700 1.700 0 0 0 3.400 0c0-.7-.3-1.700-1.700-3.500z")]


@icon("luncheon-meat-can", CAT, "Rounded tin with a key on its side and a loaf of meat sliding out of the open end",
      tags=["meat tin", "tinned meat", "canned meat", "meat loaf", "pull key", "pantry", "tin"])
def _(S):
    return [shell(rect(2, 8, 14, 13, rr(S, 3))), detail(seg(2, 11.500, 16, 11.500)),
            solid(rect(14, 11, 8, 8.500, rr(S, 2))), line("M6 8V4.500h5")]


@icon("corned-beef-tin", CAT, "Tapered tin with a winding key wrapped around a strip near the top",
      tags=["corned beef", "tinned meat", "key tin", "army ration", "canned meat", "pantry"])
def _(S):
    return [shell(poly([(7, 8), (17, 8), (21, 21), (3, 21)], closed=True, r=S.r), stroke_miterlimit="4"),
            detail(seg(5.800, 12, 18.200, 12)), line("M12 8V4.500"), line("M9 4.500h6")]


@icon("canned-ham", CAT, "Pear-shaped flat tin seen from above with a rolled rim and a key tab at the narrow end",
      tags=["ham tin", "tinned ham", "tinned meat", "pear tin", "canned meat", "pantry"])
def _(S):
    body = poly([(9, 3.5), (15, 3.5), (17, 8), (21, 15), (21, 19), (19, 21), (5, 21), (3, 19), (3, 15), (7, 8)],
                closed=True, r=L(S, 0, 2.5))
    return [shell(body), detail(ellipse(12, 15, 5, 3.3)), hole(circle(12, 6.6, 1.2))]


@icon("stacked-cans", CAT, "Pyramid of six cans seen end on, three at the bottom, two above and one on top",
      tags=["can stack", "canned goods", "food drive", "tinned food", "supermarket display", "food bank"])
def _(S):
    parts = []
    for i, n in enumerate((1, 2, 3)):
        y = 6.8 + 5.72 * i
        for j in range(n):
            x = 12 + (j - (n - 1) / 2) * 6.6
            parts.append(shell(circle(x, y, 2.2) if S.name == "rounded" else poly(regular(x, y, 2.3, 8, -67.5), closed=True)))
    return parts


@icon("dented-can", CAT, "Upright can with a crumpled dent in its side and a warning mark beside it",
      tags=["damaged can", "bad can", "botulism", "food safety", "dented tin", "discard", "warning"])
def _(S):
    body = poly([(4, 3), (16, 3), (16, 9.500), (13, 12), (16, 14.500), (16, 21), (4, 21)], closed=True, r=L(S, 0, 1.2))
    return [shell(body), detail(seg(4, 6.500, 16, 6.500)), detail(seg(4, 17.500, 16, 17.500)),
            line(seg(20, 4.500, 20, 12)), dot(20, 16.300, 1.4)]


@icon("can-rack", CAT, "Slanted shelf rack with cans lying along it and a stop bar at the low end",
      tags=["can dispenser", "can organizer", "first in first out", "pantry shelf", "canned goods", "storage"])
def _(S):
    parts = [line("M2 13L20.500 18.500"), line("M21.500 14V21.500")]
    for cx in (7, 15):
        cy = 13 + (cx - 2) * 0.297 - 4
        pts = rot([(cx - 4, cy - 3.3), (cx + 4, cy - 3.3), (cx + 4, cy + 3.3), (cx - 4, cy + 3.3)], 16.5, cx, cy)
        parts.append(shell(poly(pts, closed=True, r=S.r * 0.7)))
    return parts


@icon("golden-syrup-tin", CAT, "Round tin with a lever lid pried half open and a thick drip running down the side",
      tags=["syrup tin", "treacle", "molasses", "golden syrup", "sweetener", "baking", "pantry"])
def _(S):
    return [shell(rect(4, 10, 16, 11, rr(S, 3))),
            shell(poly([(4, 10), (19, 10), (21, 6), (5, 6.500)], closed=True, r=S.r * 0.8)),
            hole("M13.200 11V17.500a1.600 1.600 0 0 0 3.200 0V11z")]


# ============================================================================ jars and barrels

@icon("baby-food-jar", CAT, "Small squat jar with a wide lid, a bib on the label and a spoon beside it",
      tags=["baby puree", "infant food", "weaning", "toddler food", "small jar", "spoon", "pantry"])
def _(S):
    return jar(S, 3, 16, 7, 10, 21, cap=3) + [
        hole(minus(rect(7, 13, 5.500, 5.500, 1.500), circle(9.750, 13, 1.400))),
        line(seg(19.500, 21, 19.500, 14)), solid(ellipse(19.500, 11.300, 1.700, 2.500))]


@icon("olive-jar", CAT, "Glass jar with a lid and round olives stuffed with red pimento inside",
      tags=["olives", "green olives", "pickled olives", "antipasto", "preserved", "mediterranean", "pimento"])
def _(S):
    return jar(S, 5, 19, 3, 6, 21) + [
        hole(minus(ellipse(9.500, 11.800, 2.500, 2), circle(9.500, 11.800, 0.800))), hole(ellipse(14.800, 12.500, 2.500, 2)),
        hole(ellipse(9.300, 17.300, 2.500, 2)), hole(minus(ellipse(14.500, 17.800, 2.500, 2), circle(14.500, 17.800, 0.800)))]


@icon("salsa-jar", CAT, "Wide jar with a lid, a chili pepper and diced pieces on the label",
      tags=["salsa", "tomato salsa", "dip", "hot sauce jar", "chili", "mexican", "pantry"])
def _(S):
    return jar(S, 3, 21, 3, 6.500, 21) + [
        hole("M6 10.500C10.500 9.800 13.500 12 14.300 16.500c.2 1.200-.4 2-1.300 2.100C11 17 8 14.300 6 13.500z"), hole(rect(4.600, 10.500, 1.600, 1.600, 0.4)), hole(rect(15, 11, 2.500, 2.500, 0.4)),
        hole(rect(15.500, 15.500, 2.500, 2.500, 0.4))]


@icon("pesto-jar", CAT, "Small jar with a lid, a filled band of sauce and a basil leaf on the label",
      tags=["basil sauce", "pesto", "green sauce", "pasta sauce", "italian", "herb", "pantry"])
def _(S):
    return jar(S, 5, 19, 4, 7, 21) + [detail(seg(5, 10.500, 19, 10.500)),
                                      hole("M12 19C8.300 18 8.300 14 10.300 12.500C14 13 15.500 16 12 19Z")]


@icon("pasta-sauce-jar", CAT, "Tall jar with a lid and a label showing a tomato beside a fork of spaghetti",
      tags=["tomato sauce", "marinara", "spaghetti sauce", "bolognese", "jarred sauce", "italian", "pantry"])
def _(S):
    return jar(S, 4, 20, 2.500, 5.500, 21.500) + [
        hole(circle(9.500, 15, 3)), hole(poly(regular(9.500, 10.800, 1.600, 5), closed=True)),
        hole(thick("M14.600 10.500v3.200a1.600 1.600 0 0 0 3.200 0v-3.200", 1.300)), hole(thick("M16.200 15.300V19", 1.300))]


@icon("chocolate-spread-jar", CAT, "Round-shouldered jar with no lid, a knife standing in the spread and a hazelnut on the label",
      tags=["chocolate spread", "hazelnut spread", "chocolate hazelnut", "breakfast spread", "knife", "sweet", "pantry"])
def _(S):
    body = union(rect(7, 6.500, 10, 3, L(S, 0, 1)), rect(4, 9, 16, 12, rr(S, 5)))
    return [shell(body), line(seg(16.500, 2.500, 13, 10)), detail(seg(7, 9.500, 17, 9.500)),
            hole(ellipse(10, 16.300, 2.300, 2.700)), hole(rect(7.900, 12.600, 4.200, 1.200, 0.5))]


@icon("instant-coffee-jar", CAT, "Squat glass jar with a wide lid and a steaming cup printed on the label",
      tags=["coffee granules", "instant coffee", "freeze dried", "coffee jar", "hot drink", "breakfast", "pantry"])
def _(S):
    return jar(S, 4, 20, 3, 7, 21, lid=(4.500, 19.500)) + [
        hole("M7.500 13.500h7v1.800a3.500 3.500 0 0 1-7 0z"), hole(thick("M14.500 14.300h1a1.300 1.300 0 0 1 0 2.600h-1.400", 1.300)),
        hole(thick("M9.500 12.500c-.9-1 .9-1.700 0-2.800", 1.200)), hole(thick("M12.500 12.500c-.9-1 .9-1.700 0-2.800", 1.200))]


@icon("chili-oil-jar", CAT, "Small jar with a layer of oil over a thick bed of chili flakes and a spoon handle sticking out",
      tags=["chilli oil", "chili crisp", "hot oil", "spicy condiment", "chili flakes", "asian", "pantry"])
def _(S):
    body = union(rect(7, 4.500, 10, 3.500, L(S, 0, 1)), rect(5, 8, 14, 13, rr(S, 4)))
    return [shell(body), detail(seg(5, 11.500, 19, 11.500)), line(seg(15, 16, 18.500, 2)),
            dot(9, 15, 1.1), dot(12.500, 17.800, 1.1), dot(9.500, 18.500, 1.1), dot(13, 14.300, 1.1)]


@icon("ghee-jar", CAT, "Squat jar with a lid, a smooth golden fill line and a single drop on the label",
      tags=["clarified butter", "butter oil", "desi ghee", "indian cooking", "fat", "dairy", "pantry"])
def _(S):
    return jar(S, 4, 20, 5, 8, 21) + [detail(seg(4, 11.500, 20, 11.500)),
                                      hole("M12 13.500C10.300 15.500 10 16.500 10 17.200a2 2 0 0 0 4 0c0-.7-.3-1.700-2-3.700z")]


@icon("coconut-oil-jar", CAT, "Wide short jar with a lid and a half coconut on the label",
      tags=["virgin coconut oil", "coconut fat", "cooking oil", "hair oil", "solid oil", "vegan", "pantry"])
def _(S):
    return jar(S, 3, 21, 5, 8, 21) + [hole(minus(circle(12, 15, 4.200), circle(12, 15, 1.800)))]


@icon("onggi-jar", CAT, "Round-bellied earthenware jar with a narrow base and a wide flat lid",
      tags=["korean crock", "kimchi pot", "fermentation jar", "clay jar", "earthenware", "kimchi", "pottery"])
def _(S):
    return [shell(rect(7, 2.500, 10, 3, L(S, 0, 1.2))),
            shell("M9 5.500C4 6.800 2.500 10.500 3 14c.4 3.500 2 5.500 4.500 7h9c2.500-1.500 4.100-3.500 4.500-7 .5-3.500-1-7.200-6-8.500z"),
            detail("M6.500 9.500c3.500 1.500 7.500 1.500 11 0")]


@icon("pickle-barrel", CAT, "Open wooden barrel with metal hoops and pickles sticking out above the brine",
      tags=["pickles", "brine", "cracker barrel", "deli", "cucumbers", "preserved vegetables", "wooden cask"])
def _(S):
    body = "M5.500 9.500C4 13 4 17.500 5.500 21h13c1.500-3.500 1.500-8 0-11.500z"
    return [shell(body), detail("M4.600 13h14.800"), detail("M4.700 17.500h14.600"),
            solid(ellipse(9, 6, 1.600, 3.400)), solid(ellipse(13, 5.500, 1.600, 3.400)), solid(ellipse(16.200, 6.700, 1.600, 3))]


@icon("airlock-fermenting-jar", CAT, "Wide-mouth jar of chopped vegetables with a curved airlock valve on the lid",
      tags=["fermentation", "sauerkraut", "kimchi jar", "pickling", "probiotic", "gut health", "airlock"])
def _(S):
    return jar(S, 4, 20, 7, 10, 21) + [line("M12 7V4a2 2 0 0 1 4 0v1.500"),
                                        hole(rect(7, 13, 2.600, 2.600, 0.4)), hole(rect(12, 12.500, 2.600, 2.600, 0.4)),
                                        hole(rect(15.500, 16, 2.600, 2.600, 0.4)), hole(rect(8.500, 17, 2.600, 2.600, 0.4))]


@icon("water-bath-canning", CAT, "Tall pot with side handles holding three jars on a rack with bubbles rising above the water",
      tags=["home canning", "preserving", "canning pot", "mason jars", "jam making", "boiling", "preserves"])
def _(S):
    jr = lambda x: union(rect(x, 13.500, 3.600, 5.500, 0.8), rect(x + 0.6, 12.300, 2.400, 1.800, 0.3))
    return [shell(rect(4, 9, 16, 12, rr(S, 3))), line(seg(4, 12, 2, 12)), line(seg(20, 12, 22, 12)),
            hole(jr(6)), hole(jr(10.200)), hole(jr(14.400)),
            dot(8, 5.500, 1.200), dot(13, 3.800, 1.200), dot(17, 6, 1.200)]


@icon("broth-carton", CAT, "Tall brick carton with a screw cap on the sloped top and a steaming bowl on the front",
      tags=["stock carton", "soup stock", "bone broth", "liquid stock", "soup base", "chicken stock", "pantry"])
def _(S):
    body = poly([(6, 21), (6, 9), (9.500, 3), (14.500, 3), (18, 9), (18, 21)], closed=True, r=L(S, 0, 1.500))
    return [shell(body), detail(seg(6, 9, 18, 9)), hole(circle(13.500, 5.800, 1)),
            hole("M8.500 15.500h7a3.500 3.500 0 0 1-7 0z"), hole(thick("M12 13c-1.100-1 1.100-1.800 0-3", 1.300))]


# ============================================================================ tins, boxes and canisters

@icon("coffee-can", CAT, "Tall wide can with a snap-on lid and a coffee bean on the label",
      tags=["coffee tin", "ground coffee", "coffee canister", "beans", "caffeine", "brew", "pantry"])
def _(S):
    return jar(S, 4, 20, 3, 6.500, 21, lid=(3.500, 20.500), cap=3) + [
        hole(minus(ellipse(12, 14.500, 3.300, 4.600), thick("M12 10.500c-2 1.600 2 2.800 0 4.500s2 2.800 0 4", 1.100)))]


@icon("cooking-spray", CAT, "Slim aerosol can with a nozzle cap spraying a fan of mist and an oil drop on the label",
      tags=["oil spray", "spray oil", "aerosol", "non stick spray", "baking", "greasing", "mist"])
def _(S):
    body = union(rect(9.500, 3.500, 5, 6, rr(S, 1.500)), poly([(8, 21), (8, 12.500), (9.500, 9), (14.500, 9), (16, 12.500), (16, 21)],
                                                               closed=True, r=L(S, 0, 1.200)))
    return [shell(body), detail(seg(9.500, 9, 14.500, 9)), line(seg(6.500, 4.500, 2.500, 3)), line(seg(6.500, 6.500, 2, 6.500)),
            line(seg(6.500, 8.500, 2.500, 10)), hole("M12 14.500C10.600 16.300 10.300 17 10.300 17.600a1.700 1.700 0 0 0 3.400 0c0-.6-.3-1.300-1.700-3.100z")]


@icon("baking-powder", CAT, "Small round tin with its lid off beside it and bubbles rising above the powder",
      tags=["raising agent", "leavening", "self raising", "baking tin", "rise", "powder", "cake baking"])
def _(S):
    return [shell(rect(3, 11.500, 13, 9.500, rr(S, 3))), solid("M4.500 11.500C5.500 8.500 7.500 7 9.500 7s4 1.500 5 4.500z"),
            shell(rect(17.500, 18, 4.500, 3, rr(S, 1))), dot(6.500, 4.500, 1.200), dot(11, 3.300, 1), dot(13.500, 6, 1.100)]


@icon("cocoa-powder", CAT, "Round tin with a spoon resting across a heap of dark powder and a cocoa pod on the label",
      tags=["cacao", "hot chocolate", "baking cocoa", "chocolate powder", "spoon", "pod", "pantry"])
def _(S):
    return [shell(rect(4, 11.500, 16, 9.500, rr(S, 3))), solid("M6 11.500C7 8.500 9.500 7 12 7s5 1.500 6 4.500z"),
            line(seg(3, 3, 12.500, 7.500)), solid(ellipse(15.500, 6.800, 2.300, 1.500)),
            hole(minus(rell(12, 16.300, 2.300, 3.300, 0), thick("M12 13.200v6.200", 0.9)))]


@icon("olive-oil-tin", CAT, "Tall rectangular tin with a small spout on one shoulder and an olive sprig on the front",
      tags=["oil can", "olive oil", "extra virgin", "cooking oil tin", "mediterranean", "cold pressed", "pantry"])
def _(S):
    body = union(poly([(5, 21), (5, 9), (8.500, 6), (16, 6), (19, 9), (19, 21)], closed=True, r=L(S, 0, 1.500)),
                 rect(14.500, 2.500, 3, 4, L(S, 0, 0.8)))
    return [shell(body), detail(seg(5, 9, 19, 9)), hole(thick("M9.500 19.200c.4-2.700 1.500-4.800 2.600-6.400", 1.100)),
            hole(rell(10, 14.300, 2.200, 1, -40)), hole(rell(14.300, 14.500, 2.200, 1, 35)), hole(circle(14.800, 18.300, 1.600))]


@icon("cereal-box", CAT, "Tall narrow box standing upright with a bowl of flakes and a spoon on the front",
      tags=["breakfast cereal", "cornflakes", "muesli", "granola box", "breakfast", "flakes", "pantry"])
def _(S):
    return [shell(rect(5.500, 2.500, 13, 19, L(S, 0.5, 2))), detail(seg(5.500, 6, 18.500, 6)),
            hole("M8 15.500h8a4 4 0 0 1-8 0z"), hole(rell(10.200, 13.500, 1.300, 0.900, 15)), hole(rell(13, 13, 1.300, 0.900, -20)),
            hole(thick("M16.500 10.500L14.800 13.500", 1.100))]


@icon("pasta-box", CAT, "Long box with a clear window on the front showing short tube pasta inside",
      tags=["penne box", "macaroni", "dried pasta", "window box", "italian", "noodles", "pantry"])
def _(S):
    return [shell(rect(5, 2.500, 14, 19, L(S, 0.5, 2.500))), detail(rect(8, 6.500, 8, 11, L(S, 0.5, 1.200))),
            hole(thick("M10.500 11.800l1.200-2", 1.500)), hole(thick("M13.200 12.500l1.200-2", 1.500)),
            hole(thick("M10.800 15.600l1.200-2", 1.500)), hole(thick("M13.500 16l1-1.800", 1.500))]


@icon("cake-mix-box", CAT, "Rectangular box with a layered cake slice on the front and a whisk in the corner",
      tags=["baking mix", "cake mix", "boxed mix", "sponge", "whisk", "layers", "pantry"])
def _(S):
    return [shell(rect(3, 3.500, 18, 17.500, rr(S, 2.500))), detail(seg(3, 7.500, 21, 7.500)),
            hole(minus(poly([(5.800, 18), (14.800, 18), (14.800, 11), (5.800, 14)], closed=True), rect(5, 14.200, 11, 1)))
            if False else hole(minus(poly([(5.800, 18.300), (14.500, 18.300), (14.500, 11.500), (5.800, 14.500)], closed=True),
                                     rect(5, 15.800, 11, 0.900))),
            hole(minus(circle(18, 13, 2), circle(18, 13, 0.900))), hole(rect(17.500, 9.500, 1, 2.600))]


@icon("baking-soda-box", CAT, "Small upright box with the pour flap opened at the top and a few grains spilling out",
      tags=["bicarbonate of soda", "bicarb", "sodium bicarbonate", "cleaning powder", "baking", "powder", "pantry"])
def _(S):
    return [shell(rect(5.500, 8, 12, 13, rr(S, 2))), line("M5.500 8l2.200-4.500H15.300L17.500 8"),
            dot(20, 11, 1.200), dot(21, 15, 1.200), dot(19.300, 18.700, 1.200)]


@icon("oatmeal-canister", CAT, "Tall round cardboard canister with a flat lid and oat flakes on the label",
      tags=["porridge oats", "rolled oats", "oats tin", "breakfast", "cardboard tube", "porridge", "pantry"])
def _(S):
    return jar(S, 5, 19, 2.500, 5.500, 21.500, cap=1.500) + [
        hole(thick("M12 19.500V9.500", 1.100)), hole(rell(9.800, 16, 1.100, 1.900, 35)), hole(rell(14.200, 13.600, 1.100, 1.900, -35)),
        hole(rell(9.800, 11.800, 1.100, 1.900, 35)), hole(rell(12, 8.300, 1, 1.700, 0))]


@icon("stock-cube", CAT, "Small foil-wrapped cube with one side unfolded to show the crumbly cube inside",
      tags=["bouillon cube", "stock pot", "seasoning cube", "flavouring", "soup", "gravy", "pantry"])
def _(S):
    body = union(rect(3, 8, 12, 12, rr(S, 2)), poly([(15, 8), (21, 5.500), (21, 16.500), (15, 20)], closed=True, r=L(S, 0, 1)))
    return [shell(body), detail(seg(15, 8, 15, 20)), solid(poly([(5.500, 11), (8.200, 11.500), (6.500, 13.500)], closed=True)),
            solid(poly([(10.500, 14), (12.500, 16), (9.800, 16.800)], closed=True)),
            solid(poly([(5.800, 16), (7.500, 17.800), (5.300, 18.200)], closed=True))]


@icon("meal-kit-box", CAT, "Open cardboard box holding a carrot, a spice pot and a recipe card standing up at the back",
      tags=["recipe box", "meal delivery", "subscription box", "ingredients", "cooking kit", "dinner kit", "weekly box"])
def _(S):
    return [shell(rect(3, 12, 18, 9.500, L(S, 0.5, 3))), line("M14 12V3.500h5V12"),
            solid(poly([(5, 12), (9, 12), (7, 6.500)], closed=True)), solid(rect(10.500, 7.500, 2.500, 4.500, 0.5)),
            solid(rect(11, 6, 1.500, 1, 0.3)), solid(poly([(6, 6), (5, 3.500), (7.500, 4.500)], closed=True))]


@icon("animal-crackers-box", CAT, "Small box shaped like a circus wagon with bars on the side, wheels and a string loop on top",
      tags=["circus crackers", "cookie box", "biscuit box", "wagon", "cage", "snack box", "kids snack"])
def _(S):
    body = union("M3 10V9c0-2.500 4-4 9-4s9 1.500 9 4v1z", rect(3.500, 10, 17, 8, L(S, 0, 1.500)))
    return [shell(body), detail(seg(9, 10, 9, 18)), detail(seg(15, 10, 15, 18)), line("M10.500 5.300C10.500 2 13.500 2 13.500 5.300"),
            dot(7.500, 20.500, 1.800), dot(16.500, 20.500, 1.800)]


# ============================================================================ tubs, blocks, pouches and bags

@icon("margarine-tub", CAT, "Wide shallow tub with a smooth spread on top and a knife resting across it",
      tags=["butter tub", "spread", "plant butter", "dairy free", "breakfast", "knife", "toast"])
def _(S):
    tub = union(rect(2.500, 10.500, 19, 2.500, L(S, 0, 1.200)), poly([(4, 13), (20, 13), (18.500, 21), (5.500, 21)], closed=True, r=L(S, 0, 1.500)))
    return [shell(tub), solid("M5 10.500C6 7.800 9 6.800 12 6.800s6 1 7 3.700z"), line(seg(9, 3.500, 19, 8))]


@icon("pudding-cup", CAT, "Small cup with its foil lid peeled halfway back and a spoon dipping into the pudding",
      tags=["custard pot", "dessert cup", "snack pack", "pudding", "chocolate pudding", "lunchbox", "spoon"])
def _(S):
    return [shell(poly([(5, 10), (19, 10), (17, 21), (7, 21)], closed=True, r=L(S, 0, 1.500))), detail(seg(5.800, 14, 18.200, 14)),
            line("M19 10c2.500 0 3-3 1.500-5"), line(seg(9, 3, 11.500, 13.500)), hole(rell(12.300, 16.500, 1.500, 2.300, 15))]


@icon("clay-yogurt-pot", CAT, "Round unglazed clay pot with a wide mouth and set yogurt with a thin skin on top",
      tags=["terracotta", "curd pot", "dahi", "set yogurt", "earthenware", "traditional dairy", "clay"])
def _(S):
    body = union(rect(3, 4.500, 18, 3, L(S, 0, 1.200)),
                 "M4.500 7.500C4.500 14 6 18.500 8.500 20.500c.4.300.8.500 1.400.5h4.200c.6 0 1-.2 1.400-.5 2.500-2 4-6.500 4-13z")
    return [shell(body), detail("M5 12c2-1.300 3 1.300 5 0s3 1.300 5 0 3 1.300 4 0")]


@icon("miso-paste", CAT, "Rectangular plastic tub with its lid lifted at one corner and a swirl of thick paste on the front",
      tags=["soybean paste", "fermented paste", "japanese pantry", "doenjang", "soup base", "umami", "tub"])
def _(S):
    tub = union(rect(3, 11, 18, 10, L(S, 0.5, 3)), poly([(3, 11), (3, 7), (20, 9), (20, 11)], closed=True, r=L(S, 0, 1)))
    return [shell(tub), detail(seg(3, 11, 20, 11)), hole(thick("M7 16.500c2-2 3.500 1.800 5.500 0s3.500-1.500 4.500 0", 1.500))]


@icon("tofu", CAT, "Soft rounded block of tofu sitting in a shallow tray of water",
      tags=["bean curd", "soy", "vegan protein", "soybean", "plant based", "asian food", "silken tofu"])
def _(S):
    return [shell(rect(6, 3.500, 12, 10, rr(S, 3))), line("M2.500 11L5 20.500h14L21.500 11"),
            detail("M6 16.500c2-1.200 3 1.200 5 0s3 1.200 5 0 2.500 1 2.500 0")]


@icon("tempeh", CAT, "Flat rectangular cake of pressed beans seen from above with one corner cut away",
      tags=["fermented soy", "indonesian", "vegan protein", "soybean cake", "plant based", "beans", "slice"])
def _(S):
    cake = poly([(3, 5), (21, 5), (21, 12), (15, 12), (15, 19), (3, 19)], closed=True, r=L(S, 0, 1.500))
    return [shell(cake), dot(6.500, 9, 1.200), dot(10.500, 9, 1.200), dot(14.500, 9, 1.200), dot(18, 9, 1.200),
            dot(8.500, 13, 1.200), dot(12.500, 13.500, 1.200), dot(6.500, 16, 1.200), dot(10.800, 16.500, 1.200)]


@icon("milk-pouch", CAT, "Soft sealed pillow bag of milk with one corner snipped off and a milk drop on the front",
      tags=["bagged milk", "milk bag", "liquid pouch", "dairy", "milk", "canadian milk", "snipped corner"])
def _(S):
    body = poly([(5, 4), (14, 4), (19, 9), (19, 20.500), (5, 20.500)], closed=True, r=L(S, 0, 2))
    return [shell(body), detail(seg(5, 7.500, 12, 7.500)), detail(seg(5, 17.500, 19, 17.500)), dot(19.500, 3.500, 1.200),
            hole("M12 10.300C10.300 12.300 10 13.300 10 14a2 2 0 0 0 4 0c0-.7-.3-1.700-2-3.700z")]


@icon("instant-noodle-packet", CAT, "Pillow-shaped packet with crimped seals and a block of wavy dried noodles on the front",
      tags=["ramen packet", "noodle pack", "instant ramen", "quick meal", "dried noodles", "student food", "pantry"])
def _(S):
    return [shell(rect(4, 3, 16, 18, L(S, 1, 3))), detail(seg(4, 6, 20, 6)), detail(seg(4, 18, 20, 18)),
            hole(minus(rect(7, 8.500, 10, 7, L(S, 0.8, 2)), thick("M6 11.300c2-1.300 3.500 1.300 6 0s4 1.300 6 0", 0.9),
                       thick("M6 13.400c2-1.300 3.500 1.300 6 0s4 1.300 6 0", 0.9)))]


@icon("stick-pack", CAT, "Long thin single-serve sachet with a torn zigzag top and powder pouring out",
      tags=["sachet", "single serve", "powder packet", "drink mix", "instant coffee stick", "sugar stick", "travel pack"])
def _(S):
    return [shell(poly([(8.500, 22), (8.500, 9), (10.500, 7), (12, 9), (13.500, 7), (15.500, 9), (15.500, 22)], closed=True, r=S.r * 0.4)),
            detail(seg(8.500, 12.500, 15.500, 12.500)), dot(10.500, 4, 1.100), dot(13.500, 2.800, 1.100), dot(16.500, 4.800, 1)]


@icon("chip-bag", CAT, "Puffy snack bag with crimped top and bottom seals and a wavy chip on the front",
      tags=["crisps", "potato chips", "snack bag", "junk food", "crisp packet", "party snack", "pantry"])
def _(S):
    body = poly([(6, 3.500), (18, 3.500), (19.500, 12), (18, 20.500), (6, 20.500), (4.500, 12)], closed=True, r=L(S, 0, 3))
    return [shell(body), detail(seg(6, 6.500, 18, 6.500)), detail(seg(6, 17.500, 18, 17.500)),
            hole(minus(rell(12, 12, 4.200, 3, -20), thick("M7 12.300c2-1.500 3.500 1.500 5.500 0s3-1 4.500-2", 0.9)))]


@icon("rice-sack", CAT, "Woven sack tied at the top with a heap of rice grains printed on the front panel",
      tags=["rice bag", "grain sack", "burlap sack", "bulk rice", "basmati", "staple food", "flour sack"])
def _(S):
    sack = poly([(7, 3.500), (17, 3.500), (16.400, 6.500), (20, 15.500), (18, 21), (6, 21), (4, 15.500), (7.600, 6.500)],
                closed=True, r=L(S, 0, 3))
    return [shell(sack), detail(seg(7.300, 6.500, 16.700, 6.500)), hole("M7.500 18C8.500 14.500 10 13 12 13s3.500 1.500 4.500 5z")]


@icon("bread-clip", CAT, "Small flat plastic tag with a notched slot on one side, the kind that closes bread bags",
      tags=["bag clip", "bread tag", "bread tab", "bag closer", "bag seal", "kitchen organizing", "quick lock"])
def _(S):
    return [shell(minus(rect(4.500, 6, 15, 12, rr(S, 3)), union(rect(10.500, 12.500, 3, 6, 0), circle(12, 12.500, 1.500))))]


@icon("twist-tie", CAT, "Short wire tie twisted around the gathered neck of a bag",
      tags=["bag tie", "wire tie", "bread tie", "cable tie", "garbage bag tie", "seal", "gathered bag"])
def _(S):
    bag = poly([(4.500, 21), (4.500, 17), (10, 11), (10, 8.500), (14, 8.500), (14, 11), (19.500, 17), (19.500, 21)], closed=True, r=L(S, 0, 2.500))
    return [shell(bag), line("M8.500 6l1.500 2.500M15.500 6L14 8.500"), line(seg(9, 10, 15, 12.700)), line(seg(9, 12.700, 15, 10)),
            line("M15.500 12l2-2.500")]


@icon("microwave-popcorn-bag", CAT, "Flat paper bag puffed up in the middle with steam lines above and popped kernels on the front",
      tags=["popcorn bag", "microwave snack", "movie night", "popped corn", "steam", "kernels", "snack"])
def _(S):
    bag = "M5.500 21C4.500 16 4.500 11 6 8h12c1.500 3 1.500 8 .5 13z"
    return [shell(bag), detail(seg(5.800, 11, 18.200, 11)),
            hole(union(circle(10.300, 17, 1.800), circle(13.700, 17, 1.800), circle(12, 14.800, 1.800))),
            line("M9 6c-1.500-1 1.500-2 0-3.500"), line("M15 6c-1.500-1 1.500-2 0-3.500")]


@icon("popcorn-kernels", CAT, "Small heap of pointed unpopped kernels with one popped fluffy kernel beside it",
      tags=["unpopped corn", "popping corn", "maize kernels", "dried corn", "seeds", "popcorn", "cinema snack"])
def _(S):
    ks = [(5.500, 18.300, 10), (9, 19, -15), (12.500, 18.300, 20), (7, 14.500, -25), (10.800, 14.800, 20), (8.800, 10.800, 5)]
    parts = [solid(rell(x, y, 1.500, 2.300, r)) for x, y, r in ks]
    cloud = union(circle(15.200, 10, 2.600), circle(19, 10, 2.600), circle(17.100, 6.800, 2.600), circle(17.100, 13, 2.300))
    return parts + [shell(cloud)]


@icon("vacuum-sealed-bag", CAT, "Flat bag with a sealed strip across the top and plastic shrunk tightly around a steak",
      tags=["vacuum pack", "sous vide bag", "sealed meat", "food storage", "steak", "shrink wrap", "freezer bag"])
def _(S):
    steak = "M6.500 15c0-3.200 3-5 6-5s5.500 1.800 5.500 5-2 5-5.500 5-6-1.800-6-5z"
    return [shell(rect(3, 3.500, 18, 17.500, rr(S, 2.500))), detail(seg(3, 7, 21, 7)),
            hole(minus(steak, circle(14, 15.500, 1.200)))]


@icon("ice-bag", CAT, "Plastic bag of ice tied at the neck with a snowflake on the front",
      tags=["bagged ice", "ice cubes", "party ice", "cooler", "frozen", "crushed ice", "snowflake"])
def _(S):
    bag = poly([(5.500, 21), (5.500, 16), (9.500, 10.500), (9.500, 6.500), (14.500, 6.500), (14.500, 10.500), (18.500, 16), (18.500, 21)],
               closed=True, r=L(S, 0, 2.500))
    flake = union(thick("M12 13.300V19.700", 1.200), thick("M9.230 14.650L14.770 18.350", 1.200), thick("M14.770 14.650L9.230 18.350", 1.200))
    return [shell(bag), line("M8 4l1.500 2.500M16 4l-1.500 2.500"), hole(flake)]


@icon("grocery-bag", CAT, "Upright paper bag with a baguette and a leek sticking out of the top",
      tags=["shopping bag", "groceries", "supermarket", "paper bag", "food shopping", "baguette", "leek"])
def _(S):
    return [shell(rect(4.500, 10, 15, 11, rr(S, 2))), detail(seg(4.500, 13.500, 19.500, 13.500)),
            solid(thick("M9 10L6.500 3.500", 2.600)), line(seg(15.500, 10, 15.500, 5.500)), line("M15.500 7L18.500 3.500M15.500 7L13.500 3.500")]


@icon("bagged-salad", CAT, "Pillow bag with crimped seals and a clear window showing mixed salad leaves inside",
      tags=["salad kit", "mixed leaves", "lettuce bag", "greens", "washed salad", "rocket", "supermarket"])
def _(S):
    leaf = lambda x, y: hole(f"M{x} {y}c0-2.600 1.800-3.500 3.800-3.500 0 2.600-1.200 3.500-3.800 3.500z")
    return [shell(rect(3, 3, 18, 18, rr(S, 3))), detail(seg(3, 6, 21, 6)), detail(seg(3, 18, 21, 18)),
            detail(rect(6.500, 8.500, 11, 7, L(S, 0.8, 1.500))), leaf(8, 14), leaf(12.500, 14)]


@icon("boil-in-bag", CAT, "Perforated pouch of rice dipping into a pot of water with bubbles rising around it",
      tags=["boil in the bag rice", "cooking pouch", "ready rice", "easy cook", "simmer", "rice pot", "quick meal"])
def _(S):
    return [shell(rect(4, 11, 16, 10, rr(S, 3))), line(seg(4, 13.500, 2, 13.500)), line(seg(20, 13.500, 22, 13.500)),
            line("M6.500 14.500V5.500a1.500 1.500 0 0 1 1.500-1.500h8a1.500 1.500 0 0 1 1.500 1.500v9"),
            detail("M6 16.500c2-1.300 3 1.300 6 0s4 1.300 6 0"), dot(10, 19, 0.900), dot(15, 19, 0.900), dot(3.500, 7, 1), dot(20.500, 7, 1), dot(19.500, 3.800, 0.900)]


@icon("frozen-vegetables", CAT, "Bag with crimped seals, peas and carrot cubes on the front and a snowflake in one corner",
      tags=["frozen peas", "frozen veg", "freezer aisle", "mixed vegetables", "frozen food", "snowflake", "bag"])
def _(S):
    flake = union(thick("M17.500 8.300V12.700", 1.100), thick("M15.600 9.200L19.400 11.800", 1.100), thick("M19.400 9.200L15.600 11.800", 1.100))
    return [shell(rect(3.500, 3, 17, 18, rr(S, 3))), detail(seg(3.500, 6, 20.500, 6)), detail(seg(3.500, 18, 20.500, 18)),
            hole(circle(7.700, 10.500, 1.300)), hole(circle(11, 9.500, 1.300)), hole(circle(8.500, 14, 1.300)),
            hole(rect(12.500, 13, 2.600, 2.600, 0.4)), hole(flake)]


@icon("frozen-pizza", CAT, "Flat square box with a sliced pizza on the front and a snowflake in the corner",
      tags=["freezer pizza", "frozen meal", "pizza box", "ready meal", "snowflake", "frozen food", "supper"])
def _(S):
    pizza = minus(circle(11, 13.500, 5), thick("M11 8V19", 0.9), thick("M6.500 11.200L15.500 15.800", 0.9), thick("M15.500 11.200L6.500 15.800", 0.9))
    flake = union(thick("M18 4.700V8.300", 1), thick("M16.500 5.500L19.500 7.500", 1), thick("M19.500 5.500L16.500 7.500", 1))
    return [shell(rect(3, 3, 18, 18, rr(S, 2.500))), hole(pizza), hole(flake)]


@icon("field-ration", CAT, "Flat military meal pouch with tear notches at the sides and a fork and knife printed on the front",
      tags=["mre", "army food", "emergency food", "survival meal", "camping food", "military", "meal pouch"])
def _(S):
    return [shell(rect(4, 3, 16, 18, L(S, 1, 3))), detail(seg(4, 6, 20, 6)), detail(seg(4, 18, 20, 18)),
            hole(thick("M9.300 9v2.600a1.400 1.400 0 0 0 2.800 0V9", 1.200)), hole(thick("M10.700 12.800V17", 1.200)),
            hole("M14.400 17V9.300c2 .3 3 2 3 4.200v.800h-3z")]


@icon("fruit-leather", CAT, "Flat fruit strip partly rolled up into a spiral on a sheet of backing paper",
      tags=["fruit roll", "dried fruit", "fruit strip", "snack", "kids snack", "roll up", "dehydrated fruit"])
def _(S):
    shape = union(circle(8, 13.500, 5), rect(8, 12, 13, 6, L(S, 0, 1.500)))
    return [shell(shape), hole(thick("M8 13.500a1 1 0 1 1 1.100 1a2.300 2.300 0 1 1-2.300-2.300", 1.100)), line(seg(3, 21.500, 21, 21.500))]


@icon("water-bottle-case", CAT, "Shrink-wrapped pack of bottled water with a carry handle on top",
      tags=["bottled water", "six pack", "water pack", "drinks multipack", "hydration", "bulk water", "carry handle"])
def _(S):
    b = lambda x: hole(union(rect(x, 12.500, 4, 7, 1), rect(x + 1, 10.500, 2, 2.200, 0.3)))
    return [shell(rect(3, 9, 18, 12, rr(S, 2.500))), line("M8 9C8 3.500 16 3.500 16 9"), b(5), b(10), b(15)]


@icon("sesame-oil", CAT, "Small squat bottle with a short neck and sesame seeds on the round label",
      tags=["toasted sesame", "asian cooking oil", "seed oil", "sesame seeds", "dressing", "stir fry", "condiment"])
def _(S):
    body = union(rect(10, 2.500, 4, 4, L(S, 0, 1)),
                 "M8.500 9c0-1.500 1.500-2.500 3.500-2.500s3.500 1 3.500 2.500c2 .8 3.500 2.500 3.500 4.500V19c0 1.200-.8 2-2 2H7.500c-1.200 0-2-.8-2-2v-5.500c0-2 1.500-3.700 3-4.500z")
    seed = lambda x, y, d: rell(x, y, 0.900, 0.500, d)
    return [shell(body), hole(minus(circle(12, 15, 3.700), seed(11, 14, 30), seed(13.400, 15.500, -30), seed(11.300, 17, -20)))]


@icon("fish-sauce", CAT, "Tall slender bottle with a narrow neck and a small fish on the label",
      tags=["nam pla", "thai sauce", "anchovy sauce", "asian condiment", "seafood sauce", "umami", "bottle"])
def _(S):
    body = poly([(10.500, 2.500), (13.500, 2.500), (13.500, 7), (16, 10), (16, 21.500), (8, 21.500), (8, 10), (10.500, 7)], closed=True, r=L(S, 0, 2))
    return [shell(body), hole(ellipse(11.800, 15.500, 2.600, 1.400)), hole(poly([(14, 15.500), (16, 13.800), (16, 17.200)], closed=True))
            if False else hole(poly([(13.800, 15.500), (15.800, 13.900), (15.800, 17.100)], closed=True))]


@icon("infused-oil", CAT, "Tall glass bottle closed with a cork, a rosemary sprig and a chili floating inside",
      tags=["herb oil", "chili oil bottle", "rosemary oil", "flavoured oil", "gift bottle", "olive oil", "homemade"])
def _(S):
    body = poly([(10, 5), (14, 5), (14, 9), (18, 13), (18, 20.500), (6, 20.500), (6, 13), (10, 9)], closed=True, r=L(S, 0, 2.500))
    return [shell(body), solid(rect(10, 2, 4, 3, L(S, 0, 0.8))),
            hole(thick("M9.500 18.500L11.800 12.500", 1)), hole(rell(9.700, 14.500, 1.400, 0.700, 25)), hole(rell(13.200, 13.800, 1.400, 0.700, -25)),
            hole(rell(10.800, 16.500, 1.400, 0.700, 25)),
            hole("M14.500 18.500c.6-2.500 1.500-4 2-5 .3 1 .2 3-.6 5.200z")]


@icon("salad-dressing", CAT, "Bottle with a flip cap and two separated liquid layers with herb flecks in the lower one",
      tags=["vinaigrette", "oil and vinegar", "italian dressing", "salad sauce", "condiment", "shake bottle", "herbs"])
def _(S):
    body = union(rect(9, 2.500, 6, 4, L(S, 0, 1.200)), rect(5.500, 6.500, 13, 14.500, rr(S, 4)))
    return [shell(body), detail(seg(9, 6.500, 15, 6.500)), detail(seg(5.500, 12.500, 18.500, 12.500)),
            dot(9, 16, 1), dot(13, 18, 1), dot(15.500, 15.500, 1), dot(8.800, 19, 0.800)]


@icon("worcestershire-sauce", CAT, "Slim bottle with a long neck and its body wrapped in paper folded at the shoulders",
      tags=["steak sauce", "brown sauce", "condiment", "english sauce", "marinade", "savoury", "wrapped bottle"])
def _(S):
    body = poly([(10.500, 2), (13.500, 2), (13.500, 7), (17, 9), (17, 21.500), (7, 21.500), (7, 9), (10.500, 7)], closed=True, r=L(S, 0, 1.500))
    return [shell(body), detail("M7 9l5 3.500 5-3.500"), hole(rect(9.500, 15.500, 5, 3.500, L(S, 0.3, 1)))]


@icon("cooking-oil-jug", CAT, "Large plastic jug with a molded handle on the side, a screw cap and an oil drop on the label",
      tags=["vegetable oil", "sunflower oil", "frying oil", "canola", "bulk oil", "oil bottle", "5 litre"])
def _(S):
    jug = minus(union(rect(7, 2.500, 5, 3.500, L(S, 0, 0.8)), rect(4, 6, 13, 15, rr(S, 3)), rect(14.500, 7.500, 6.500, 10, rr(S, 2.500))),
                rect(17.300, 10.300, 1.900, 4.400, 0.9))
    return [shell(jug), detail(seg(4, 9.500, 14.500, 9.500)),
            hole("M10.500 12.300C8.700 14.300 8.400 15.300 8.400 16a2.100 2.100 0 0 0 4.200 0c0-.7-.3-1.700-2.100-3.700z")]


@icon("curry-block", CAT, "Block of roux divided into a grid of snap-off squares with one square broken away",
      tags=["curry roux", "japanese curry", "stock block", "chocolate bar style", "cooking block", "snap off", "cube"])
def _(S):
    block = poly([(3, 5.500), (21, 5.500), (21, 12), (15, 12), (15, 19.500), (3, 19.500)], closed=True, r=L(S, 0, 1.500))
    return [shell(block), detail(seg(9, 5.500, 9, 19.500)), detail(seg(15, 5.500, 15, 12)), detail(seg(3, 12.500, 15, 12.500)),
            solid(rect(17, 15.500, 3.500, 3.500, 0.6))]


@icon("yeast-packet", CAT, "Strip of three small connected sachets with dotted perforations between them and granules on the front",
      tags=["dried yeast", "baking yeast", "active dry yeast", "bread baking", "sachets", "rise", "granules"])
def _(S):
    return [shell(rect(2.500, 6.500, 19, 11, L(S, 0.5, 2.500))),
            detail(seg(9, 6.500, 9, 10)), detail(seg(9, 14, 9, 17.500)), detail(seg(15.500, 6.500, 15.500, 10)),
            detail(seg(15.500, 14, 15.500, 17.500)), dot(5.800, 12, 1), dot(12.300, 12, 1), dot(18.700, 12, 1)]


@icon("fresh-yeast", CAT, "Small crumbly block of fresh yeast with a ragged top edge and crumbs falling off one corner",
      tags=["compressed yeast", "cake yeast", "baker's yeast", "bread making", "crumbs", "foil wrapper", "dough"])
def _(S):
    block = poly([(4, 8), (10, 8), (11.500, 9.800), (14, 8.500), (16, 10.500), (16, 20), (4, 20)], closed=True, r=L(S, 0, 1.200))
    return [shell(block), detail(seg(10, 20, 16, 14.500)), dot(7, 13, 1), dot(11, 16.500, 1), dot(18.500, 7.800, 1.100), dot(20, 11.300, 1.100), dot(18.300, 14.500, 1)]


@icon("vanilla-extract", CAT, "Small amber bottle with a dropper cap and a vanilla pod with a flower on the label",
      tags=["vanilla essence", "vanilla flavouring", "baking extract", "vanilla bean", "dropper bottle", "pastry", "flavour"])
def _(S):
    body = union(rect(10, 2, 4, 4.500, L(S, 0, 1.800)), rect(9, 6.500, 6, 3, 0), rect(5.500, 9.500, 13, 11.500, rr(S, 4)))
    flower = union(*[circle(16 + 1.200 * math.cos(math.radians(a)), 16.300 + 1.200 * math.sin(math.radians(a)), 1) for a in (-90, -18, 54, 126, 198)])
    return [shell(body), detail(seg(9, 9.500, 15, 9.500)), hole(thick("M8.500 18.300C10.500 17 12.500 14.500 13.800 12.300", 1.300)), hole(flower)]


@icon("food-coloring", CAT, "Row of small dropper bottles with pointed tips, one tilted and releasing a drop",
      tags=["food dye", "cake colouring", "icing color", "baking dye", "dropper", "gel color", "tint"])
def _(S):
    def bottle(bx, deg=0, base=21.5):
        pts = [(-1.800, 0), (-1.800, -6), (-0.700, -7.500), (-0.700, -10), (0, -12.300), (0.700, -10), (0.700, -7.500), (1.800, -6), (1.800, 0)]
        pts = [(bx + x, base + y) for x, y in pts]
        if deg:
            pts = rot(pts, deg, bx, base)
        return shell(poly(pts, closed=True, r=S.r * 0.4))
    return [bottle(5), bottle(11.300, 0), bottle(18, 22), dot(21.500, 13.500, 1.100)]
