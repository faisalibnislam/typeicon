"""TypeIcon Core: fashion (batch fashion_005).

Cropped garments, accessories, timepieces and needlecraft. Smooth shapes get an explicit Line versus
Rounded difference (sharp corners versus rounded corners, pointed versus round ends).
"""
import math

from dsl import D, I, P, Part, ST, U, arc, circle, detail, dot, ellipse, icon, line, poly, rect, seg, shell, solid, regular  # noqa: F401
from geometry import fmt, path_to_d, polar  # noqa: F401

CAT = "fashion"


@icon("capri-pants", CAT, "Slim trousers that end at mid calf with a waistband and a hem cuff.",
      tags=["cropped trousers", "three-quarter pants", "summer pants", "bottoms", "clothing", "leggings"])
def _(S):
    return [
        shell(poly([(7, 3), (17, 3), (18, 19.5), (13, 19.5), (12, 10), (11, 19.5), (6, 19.5)], closed=True, r=S.r)),
        detail(seg(7.2, 6.5, 16.8, 6.5)),
        detail(seg(6.2, 16.5, 10.8, 16.5)),
        detail(seg(13.2, 16.5, 17.8, 16.5)),
    ]


@icon("bolero-jacket", CAT, "Tiny open-front jacket with short sleeves that stops above the waist.",
      tags=["shrug", "cropped jacket", "short jacket", "cover-up", "dress jacket", "clothing"])
def _(S):
    pts = [(9, 4), (4.5, 6), (3, 11.5), (7, 12.5), (7, 18), (11, 18), (12, 10), (13, 18), (17, 18), (17, 12.5), (21, 11.5), (19.5, 6), (15, 4), (12, 9)]
    return [shell(poly(pts, closed=True, r=S.r))]


@icon("peep-toe-heel", CAT, "High-heeled pump in side view with a small round opening at the toe.",
      tags=["open toe pump", "stiletto", "high heel", "court shoe", "footwear", "evening shoe"])
def _(S):
    pts = [(3.5, 8), (8.5, 8), (10, 12.5), (14, 13.5), (19, 14.5), (21, 16.5), (21, 18.5), (14, 18.5), (9.5, 16), (8, 21.5), (6, 21.5), (4, 14)]
    return [
        shell(poly(pts, closed=True, r=S.r)),
        dot(18.3, 16.1, 1.0),
    ]


@icon("pince-nez", CAT, "Round glasses without arms joined by a spring bridge, with a cord hanging from one lens.",
      tags=["nose glasses", "clip-on glasses", "spectacles", "old fashioned eyewear", "vintage", "monocle"])
def _(S):
    if S.name == "rounded":
        bridge = "M10.4 9.5C11 7 13 7 13.6 9.5"
    else:
        bridge = poly([(10.4, 9.5), (12, 7), (13.6, 9.5)])
    return [
        shell(circle(6.5, 10.5, 4)),
        shell(circle(17.5, 10.5, 4)),
        line(bridge),
        line("M4.4 13.8C3.5 16.5 6.5 16.5 5.5 19.5"),
        dot(5.3, 21, 1.1),
    ]


@icon("maang-tikka", CAT, "Face with hair parted in the middle and a chain ending in a round pendant on the forehead.",
      tags=["mang tikka", "forehead jewelry", "bridal jewellery", "indian jewelry", "head ornament", "headpiece"],
      aliases=["mang-tikka"])
def _(S):
    return [
        shell(ellipse(12, 12, 7.5, 9)),
        detail("M12 4C9 4.5 6.5 8 6.5 12"),
        detail("M12 4C15 4.5 17.5 8 17.5 12"),
        detail(seg(12, 4, 12, 9.2)),
        dot(12, 11, 1.5),
        dot(9, 16, 0.9), dot(15, 16, 0.9),
    ]


@icon("armlet", CAT, "Upper arm wrapped by a curved band with a central medallion.",
      tags=["arm band", "bicep band", "arm bracelet", "jewelry", "upper arm cuff", "ornament"])
def _(S):
    return [
        line("M8.5 2V8"), line("M15.5 2V8"),
        line("M8 16V22"), line("M16 16V22"),
        shell("M6 8.5Q12 11 18 8.5V15.5Q12 18 6 15.5Z" if S.name == "rounded" else poly([(6, 8.5), (12, 10.5), (18, 8.5), (18, 15.5), (12, 17.5), (6, 15.5)], closed=True)),
        dot(12, 13.2, 1.5),
    ]


@icon("dive-watch", CAT, "Round wristwatch with a toothed rotating bezel, a dial with hands and short straps.",
      tags=["diver watch", "sports watch", "bezel watch", "wristwatch", "timepiece", "underwater watch"])
def _(S):
    pts = []
    for i in range(32):
        r = 8.6 if (i // 2) % 2 == 0 else 7.6
        pts.append(polar(12, 12, r, -90 + (i // 2) * 22.5 + (i % 2) * 11.25 - 5.6 + (0 if i % 2 == 0 else 0)))
    return [
        line("M9.5 4.4V2"), line("M14.5 4.4V2"),
        line("M9.5 19.6V22"), line("M14.5 19.6V22"),
        shell(poly(pts, closed=True)),
        detail(circle(12, 12, 4.2)),
        detail("M12 12V9.8"), detail("M12 12L13.6 13"),
    ]


@icon("fob-watch", CAT, "Small pocket watch hanging upside down from a short strap and a clip bar.",
      tags=["pocket watch", "nurse watch", "lapel watch", "pin watch", "brooch watch", "timepiece"])
def _(S):
    return [
        shell(rect(6.5, 2, 11, 3.5, 1.75 if S.name == "rounded" else 0.6)),
        line("M12 5.5V9"),
        shell(circle(12, 15.5, 6.5)),
        detail("M12 15.5V12.6"), detail("M12 15.5L14.3 16.8"),
        dot(12, 19.6, 0.8),
    ]


@icon("trucker-cap", CAT, "Baseball cap in side view with a solid front panel and a mesh back panel.",
      tags=["mesh cap", "snapback", "baseball cap", "foam cap", "headwear", "hat"])
def _(S):
    if S.name == "rounded":
        body = ("M3.5 15.5C3.5 9 7.5 5 12 5C16 5 18.3 8 18.8 12L21.8 14C22.6 14.6 22.2 16.5 21 16.5H5.5"
                "A2 2 0 0 1 3.5 14.5Z")
    else:
        body = ("M3.5 16.5V14C3.5 9 7.5 5 12 5C16 5 18.3 8 18.8 12L22 14V16.5Z")
    return [
        shell(body),
        detail("M11.6 5.4C11.2 8 11.2 12 11.6 16"),
        dot(6.3, 12.5, 0.95), dot(8.4, 9.3, 0.95), dot(8.6, 13.6, 0.95),
    ]


@icon("wristlet", CAT, "Small zip pouch with a short loop strap for the wrist.",
      tags=["wrist purse", "clutch", "zip pouch", "wrist bag", "small bag", "accessories"])
def _(S):
    return [
        shell(rect(3, 10, 15, 11, S.R)),
        detail(seg(3, 13.5, 18, 13.5)),
        dot(15, 17, 1.0),
        line("M14 10C14 3 21.5 3 21.5 9.5C21.5 12 19 13 18 13.2"),
    ]


@icon("necklace-display", CAT, "Neck-shaped jewellery stand with a necklace draped over it and a pendant.",
      tags=["jewelry bust", "neck form", "jewellery stand", "necklace stand", "retail display", "velvet bust"])
def _(S):
    return [
        shell(poly([(9, 3), (15, 3), (15, 9.5), (20, 12.5), (20, 21), (4, 21), (4, 12.5), (9, 9.5)], closed=True, r=S.r)),
        detail("M8 12.5Q12 18.5 16 12.5"),
        dot(12, 16.3, 1.3),
    ]


@icon("knitting-loom", CAT, "Round knitting loom with pegs along its top edge and yarn wound around them.",
      tags=["loom knitting", "peg loom", "ring loom", "hat loom", "yarn craft", "knit"])
def _(S):
    return [
        shell(rect(3.5, 13, 17, 7.5, min(S.R, 3))),
        line("M7 4V13"), line("M12 4V13"), line("M17 4V13"),
        line("M4.5 8.5L19.5 8.5" if S.name == "rounded" else "M4.5 8.5H19.5"),
    ]


@icon("yarn-bowl", CAT, "Bowl with a curled slot in its side and a yarn ball inside feeding a strand out.",
      tags=["knitting bowl", "yarn holder", "crochet bowl", "wool bowl", "yarn craft", "pottery"])
def _(S):
    return [
        shell("M3 13H21C21 18 17 21.5 12 21.5C7 21.5 3 18 3 13Z"),
        detail("M17 13V16.5C17 18.5 14.5 18.5 14 17"),
        line("M5.5 13A4.5 4.5 0 0 1 14.5 13"),
        line("M12.5 9C15.5 6.5 19.5 8 20 13"),
    ]


@icon("fashion-sketch", CAT, "Paper sheet with a slim figure in a dress sketched on it and a pencil beside it.",
      tags=["design sketch", "croquis", "fashion illustration", "dress drawing", "designer", "pattern drawing"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 13, 19, min(S.R, 2))),
        dot(9, 7, 1.3),
        detail(poly([(9, 9.5), (6.5, 17.5), (11.5, 17.5)], closed=True)),
        shell(poly([(19.3, 3.8), (21.3, 5), (18.6, 16.5), (16.4, 20.8), (15.9, 17)], closed=True)),
    ]


@icon("jabot", CAT, "Lace frill cascading from a collar in layered scalloped ruffles.",
      tags=["lace frill", "ruffle", "cravat", "frilled collar", "victorian", "neck ruffle", "historical costume"])
def _(S):
    return [
        shell("M9.5 3H14.5L18.5 18A3 3 0 0 1 12.5 18A3 3 0 0 1 6 18Z" if False else "M9.5 3H14.5L18.5 18A3 3 0 0 1 12.5 18A3 3 0 0 1 5.5 18Z"),
        detail("M8.3 9.5Q12 12.5 15.7 9.5"),
        detail("M7 14Q12 17 17 14"),
    ]
