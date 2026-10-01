"""TypeIcon Core: hardware (batch 007): metalworking, woodworking joints and workshop gear.

Drawn from the objects themselves in side or front view.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar

CAT = "hardware"


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def mark(d) -> Part:
    """Small solid mark: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", d)


# ============================================================================ metalworking: forge and machines

@icon("blacksmith-forge", CAT, "Forge with a hood over a hearth holding a fire",
      tags=["forge", "blacksmith", "smithy", "hearth", "metalworking", "fire", "hot metal"])
def _(S):
    flame = "M12 14C15 16.2 15.4 18 14 19.4H10C8.6 18 9 16.2 12 14Z"
    return [
        shell(poly([(3.5, 8), (8, 3), (16, 3), (20.5, 8)], closed=True, r=S.r)),
        shell(rect(3, 12, 18, 9, rr(S, 2))),
        mark(flame),
    ]

@icon("blacksmith-tongs", CAT, "Long crossed tongs with curved jaws gripping a short bar",
      tags=["forge tongs", "smithing", "blacksmith", "hot metal", "gripping", "pincers", "metalworking"])
def _(S):
    return [
        line(poly([(7, 21.5), (12, 12), (16, 7.5), (14, 4)], r=S.r * 0.8)),
        line(poly([(17, 21.5), (12, 12), (8, 7.5), (10, 4)], r=S.r * 0.8)),
        solid(rect(10.5, 2, 3, 5.5)),
    ]

@icon("tap-and-die", CAT, "Threaded tap beside a round die with a centre hole",
      tags=["thread cutting", "threading", "machinist", "metalworking", "screw thread", "tool set"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 3, 4.5, L(S, 0, 1))),
        shell(poly([(4.5, 9), (9.5, 9), (9.5, 17), (7, 21.5), (4.5, 17)], closed=True, r=S.r * 0.6)),
        detail(seg(4.5, 13, 9.5, 13)),
        shell(circle(17, 13, 5.5)),
        detail(circle(17, 13, 1.75)),
    ]


@icon("tap-wrench", CAT, "T-shaped wrench with a chuck holding a thread cutting tap",
      tags=["tap handle", "thread cutting", "machinist", "metalworking", "t-handle", "threading"])
def _(S):
    return [
        shell(rect(2, 3.5, 20, 4, rr(S, 2))),
        shell(rect(9.5, 6.5, 5, 6, rr(S, 1.5))),
        shell(poly([(10.5, 14), (13.5, 14), (13.5, 18), (12, 21.5), (10.5, 18)], closed=True, r=S.r * 0.5)),
    ]


@icon("die-stock", CAT, "Round die held in a ring with two long straight handles",
      tags=["die handle", "die wrench", "thread cutting", "threading", "machinist", "rod threading"])
def _(S):
    return [
        line(seg(2, 12, 7, 12)),
        line(seg(17, 12, 22, 12)),
        shell(circle(12, 12, 5.25)),
        detail(circle(12, 12, 1.75)),
    ]


@icon("metal-lathe", CAT, "Metal lathe with a headstock and chuck, a workpiece and a tool carriage on the bed",
      tags=["lathe", "machining", "turning", "machine shop", "metalworking", "workshop machine"])
def _(S):
    return [
        shell(poly([(2, 4), (10, 4), (10, 14.5), (22, 14.5), (22, 20), (2, 20)], closed=True, r=S.r)),
        shell(rect(11.5, 5.5, 2.5, 6, L(S, 0, 1))),
        line(seg(14, 8.5, 21, 8.5)),
        shell(rect(16, 11.5, 4, 3, L(S, 0, 1))),
    ]

@icon("milling-machine", CAT, "Milling machine with a column, a spindle head with a cutter and a flat table",
      tags=["mill", "machining", "machine shop", "cutter", "metalworking", "workshop machine"])
def _(S):
    return [
        shell(rect(3, 2.5, 5, 19, rr(S, 2))),
        shell(rect(7.5, 4.5, 10, 4, rr(S, 1.5))),
        line(seg(13, 8.5, 13, 13)),
        shell(rect(7.5, 15.5, 14.5, 5, rr(S, 1.5))),
    ]

@icon("cnc-router", CAT, "Gantry over a flat bed with a spindle and bit hanging from the crossbeam",
      tags=["cnc", "router", "gantry", "milling", "woodworking machine", "carving", "digital fabrication"])
def _(S):
    return [
        line(poly([(4, 16.5), (4, 4.5), (20, 4.5), (20, 16.5)], r=S.r * 0.6)),
        shell(rect(9.5, 5, 5, 7, rr(S, 2))),
        line(seg(12, 12, 12, 15)),
        shell(rect(2, 16.5, 20, 4, rr(S, 2))),
    ]


@icon("sheet-metal-brake", CAT, "Bending brake with a clamped bed and a hinged leaf with a handle",
      tags=["metal brake", "bending", "sheet metal", "fabrication", "flashing", "metalworking"])
def _(S):
    return [
        shell(rect(2, 10, 13, 11, rr(S, 2))),
        detail(seg(2, 14, 15, 14)),
        shell(poly([(15, 13), (18, 13), (22, 4.5), (19, 4.5)], closed=True, r=S.r * 0.5)),
    ]


@icon("welding-machine", CAT, "Welder box with a dial and terminals and two cables, one ending in a clamp",
      tags=["welder", "arc welder", "power source", "metalworking", "fabrication", "weld"])
def _(S):
    return [
        shell(rect(2.5, 4, 13.5, 16, rr(S, 2))),
        detail(seg(2.5, 13.5, 16, 13.5)),
        mark(circle(7, 8.75, 1.75)),
        mark(circle(7, 17, 1.25)),
        mark(circle(11.5, 17, 1.25)),
        line(poly([(16, 7), (20, 7), (20, 10.5)], r=S.r * 0.6)),
        shell(rect(18, 10.5, 4, 4.5, rr(S, 1))),
        line(seg(16, 19, 22, 19)),
    ]


@icon("welding-clamp", CAT, "Ground clamp with two tapered jaws on a hinge body and a cable",
      tags=["ground clamp", "earth clamp", "alligator clamp", "welding", "cable clamp", "clip"])
def _(S):
    return [
        shell(poly([(15, 4.5), (2, 7), (2, 10), (15, 10)], closed=True, r=S.r * 0.4)),
        shell(poly([(15, 14), (2, 14), (2, 17), (15, 19.5)], closed=True, r=S.r * 0.4)),
        shell(rect(14, 4.5, 4.5, 15, rr(S, 2))),
        line(seg(18.5, 12, 22, 12)),
    ]



# ============================================================================ foundry

@icon("crucible", CAT, "Deep tapered crucible holding molten metal with heat rising above it",
      tags=["melting pot", "molten metal", "foundry", "casting", "smelting", "metalworking", "heat"])
def _(S):
    return [
        line(seg(9.5, 2, 9.5, 5)),
        line(seg(14.5, 2, 14.5, 5)),
        shell(poly([(4.5, 8), (19.5, 8), (16.5, 21), (7.5, 21)], closed=True, r=S.r)),
        detail("M7.5 13C9.5 11.5 10.5 14.5 12.5 13C14.5 11.5 15.5 14.5 16.5 13"),
    ]


@icon("casting-mold", CAT, "Two part mold box with a pour funnel on top and a cavity in the lower half",
      tags=["foundry mould", "metal casting", "pour", "sprue", "cope and drag", "foundry", "mould"])
def _(S):
    return [
        shell(poly([(8, 2.5), (16, 2.5), (14.5, 7.5), (9.5, 7.5)], closed=True, r=S.r * 0.5)),
        shell(rect(3, 7.5, 18, 13.5, rr(S, 2))),
        detail(seg(3, 13.5, 21, 13.5)),
        mark(rect(7.5, 16, 9, 2, L(S, 0, 1))),
    ]


@icon("quench-bucket", CAT, "Bucket of water with steam rising as a hot bar is dipped in",
      tags=["quenching", "hardening", "hot steel", "blacksmith", "cooling", "water", "metalworking"])
def _(S):
    return [
        line("M6 7C5 5.5 7 4.5 6 2.5"),
        line(seg(20, 2.5, 13.5, 10)),
        shell(poly([(4, 10), (20, 10), (17.5, 21.5), (6.5, 21.5)], closed=True, r=S.r)),
        detail("M6 15C8 13.5 9.5 16.5 12 15C14.5 13.5 16 16.5 18 15"),
    ]


# ============================================================================ woodworking joints and jigs

def _dovetail_path():
    pts = [(9, 3)]
    for c in (8, 16):
        pts += [(9, c - 1.25), (15, c - 2.5), (15, c + 2.5), (9, c + 1.25)]
    pts.append((9, 21))
    return pts


@icon("dovetail-joint", CAT, "Two boards locked together by interlocking fan shaped pins and tails",
      tags=["dovetail", "woodworking joint", "carpentry", "joinery", "drawer joint", "cabinetmaking", "interlocking"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, rr(S, 2))),
        detail(poly(_dovetail_path())),
    ]


@icon("mortise-and-tenon", CAT, "Board with a square tongue ready to slot into a hole in another board",
      tags=["tenon", "mortise", "woodworking joint", "carpentry", "joinery", "timber frame", "furniture"])
def _(S):
    return [
        shell(poly([(2, 6), (8, 6), (8, 9), (12, 9), (12, 15), (8, 15), (8, 18), (2, 18)], closed=True, r=S.r * 0.6)),
        shell(rect(16, 4, 6, 16, rr(S, 2))),
        mark(rect(18, 9, 2, 6)),
    ]


@icon("finger-joint", CAT, "Two boards joined at a corner by interlocking square fingers",
      tags=["box joint", "woodworking joint", "carpentry", "joinery", "interlocking", "drawer", "square fingers"])
def _(S):
    return [
        shell(rect(2, 3, 20, 18, S.R)),
        detail(poly([(9, 3), (9, 9), (15, 9), (15, 15), (9, 15), (9, 21)], r=S.r)),
    ]


@icon("pocket-hole-jig", CAT, "Small block jig with an angled drill guide clamped over a board",
      tags=["pocket screw", "drill guide", "woodworking", "carpentry", "joinery", "diy", "jig"])
def _(S):
    return [
        shell(rect(2, 15, 20, 6, rr(S, 2))),
        shell(rect(5, 3.5, 10, 11.5, rr(S, 2))),
        detail(seg(8.5, 6.5, 12, 12.5)),
        line(poly([(15, 8), (19, 8), (19, 15)], r=S.r * 0.6)),
    ]


@icon("sawdust-pile", CAT, "Small mound of sawdust with a saw blade edge above it",
      tags=["wood dust", "sawing", "woodworking", "workshop", "mess", "cleanup", "carpentry"])
def _(S):
    return [
        line(poly([(3, 6), (5.5, 3), (8, 6), (10.5, 3), (13, 6), (15.5, 3), (18, 6), (20.5, 3)], r=S.r * 0.3)),
        shell("M3 21C5 15 8.5 11 12 11C15.5 11 19 15 21 21Z"),
        mark(circle(12, 16, 1.1)),
        mark(circle(8.5, 19, 1.1)),
        mark(circle(15.5, 19, 1.1)),
    ]


@icon("wood-shavings", CAT, "Curly spiral ribbons of wood planed off a board",
      tags=["wood curls", "planer shavings", "woodworking", "plane", "carpentry", "workshop", "curl"])
def _(S):
    return [
        line("M3 20C3 20 10 21 15 17C19 13.5 17 8 12.5 8C9 8 8 12 11 12.5C13 12.8 14 11 13.3 10"),
        line("M3 12C3 7 6 3.5 10.5 3.5C13.5 3.5 14 6.5 12 7"),
        line("M17.5 20C20 19 21 17 21 15"),
    ]


# ============================================================================ sawmill and splitting

@icon("bandsaw-mill", CAT, "Band saw head with two wheels and a blade cutting a long log into planks",
      tags=["sawmill", "portable sawmill", "lumber", "timber", "log milling", "planks", "woodworking machine"])
def _(S):
    return [
        shell(circle(6.5, 6, 3.5)),
        shell(circle(17.5, 6, 3.5)),
        line(seg(6.5, 2.5, 17.5, 2.5)),
        line(seg(6.5, 9.5, 17.5, 9.5)),
        shell(rect(2, 12.5, 20, 8.5, rr(S, 3))),
        detail(seg(7, 16.75, 20, 16.75)),
    ]


@icon("log-splitter", CAT, "Horizontal beam with a hydraulic ram pushing a log toward a splitting wedge",
      tags=["wood splitter", "firewood", "hydraulic ram", "logs", "splitting", "forestry", "timber"])
def _(S):
    return [
        shell(rect(2, 10, 5.5, 7.5, rr(S, 1.5))),
        line(seg(7.5, 13.75, 9.5, 13.75)),
        line(seg(9.5, 7.5, 9.5, 18.5)),
        shell(rect(11.5, 6, 6, 11.5, rr(S, 1.5))),
        shell(poly([(19.5, 17.5), (22, 17.5), (22, 5.5)], closed=True, r=S.r * 0.3)),
        line(seg(2, 21.5, 22, 21.5)),
    ]

# ============================================================================ garage and vehicle workshop

@icon("screw-extractor", CAT, "Short tapered bit with reverse spiral flutes for removing stripped screws",
      tags=["easy out", "stripped screw", "broken bolt", "removal", "repair", "drill bit", "extraction"])
def _(S):
    return [
        shell(rect(9, 2.5, 6, 4.5, L(S, 0, 1))),
        shell(poly([(8.5, 8.5), (15.5, 8.5), (12, 20)], closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
        detail(seg(9.5, 11, 14.5, 14)),
    ]


@icon("breaker-bar", CAT, "Long straight bar with a square drive head at one end",
      tags=["socket wrench", "long handle", "leverage", "lug nut", "garage", "mechanic", "ratchet"])
def _(S):
    return [
        shell(rect(9, 10, 13, 4, rr(S, 2))),
        shell(rect(2, 7.5, 8, 9, rr(S, 3))),
        mark(rect(4.5, 10.5, 3, 3)),
    ]


@icon("nut-driver", CAT, "Screwdriver style handle with a shaft ending in a hex socket",
      tags=["hex driver", "socket driver", "nut", "hose clamp", "hand tool", "mechanic", "electrician"])
def _(S):
    return [
        shell(poly(regular(12, 5.75, 4.25, 6, start=0), closed=True, r=S.r * 0.6)),
        mark(circle(12, 5.75, 1.4)),
        line(seg(12, 9.5, 12, 12.5)),
        shell(rect(8, 12.5, 8, 9, rr(S, 3))),
        detail(seg(12, 15.5, 12, 19)),
    ]


@icon("oil-filter-wrench", CAT, "Band loop wrapped around a round oil filter with a handle",
      tags=["strap wrench", "filter removal", "oil change", "car maintenance", "garage", "mechanic", "band wrench"])
def _(S):
    return [
        line(circle(10, 14, 7.5)),
        shell(circle(10, 14, 3.5)),
        shell(poly([(10, 3), (22, 3), (22, 7.5), (10, 7.5)], closed=True, r=S.r * 1.2)),
    ]


@icon("oil-funnel", CAT, "Wide cone funnel with a long bent spout for pouring oil",
      tags=["funnel", "pouring", "engine oil", "fluids", "garage", "car maintenance", "refill"])
def _(S):
    return [
        shell(poly([(3, 3), (21, 3), (14, 11), (10, 11)], closed=True, r=S.r)),
        line(poly([(12, 11), (12, 15), (18, 21)], r=S.r * 0.6)),
    ]


@icon("drip-pan", CAT, "Wide shallow tray under a falling drop with a puddle inside",
      tags=["oil pan", "catch pan", "spill", "leak", "drain pan", "garage", "car maintenance"])
def _(S):
    return [
        solid("M12 2.5C14 5 14.5 6 14.5 7C14.5 8.4 13.4 9.5 12 9.5C10.6 9.5 9.5 8.4 9.5 7C9.5 6 10 5 12 2.5Z"),
        shell(poly([(2, 13), (22, 13), (19.5, 20.5), (4.5, 20.5)], closed=True, r=S.r)),
        mark(ellipse(12, 17.5, 4.5, 1)),
    ]


@icon("mechanic-creeper", CAT, "Flat padded board with a raised headrest rolling on small caster wheels",
      tags=["creeper", "garage", "under car", "mechanic", "lying", "rolling board", "auto repair"])
def _(S):
    return [
        shell(poly([(2, 7.5), (7.5, 7.5), (8, 11.5), (22, 11.5), (22, 15.5), (2, 15.5)], closed=True, r=S.r * 0.8)),
        shell(circle(6, 19.5, 2.25)),
        shell(circle(18, 19.5, 2.25)),
    ]


@icon("parts-washer", CAT, "Basin on a stand with an open lid and a flexible hose nozzle",
      tags=["degreaser", "solvent tank", "cleaning parts", "garage", "workshop", "mechanic", "sink"])
def _(S):
    return [
        shell(poly([(2.5, 9.5), (5, 3.5), (15, 3.5), (17.5, 9.5)], closed=True, r=S.r * 0.6)),
        shell(rect(2.5, 9.5, 15, 6, rr(S, 2))),
        line(seg(5, 15.5, 5, 21.5)),
        line(seg(15, 15.5, 15, 21.5)),
        line(poly([(17.5, 12.5), (21.5, 12.5), (21.5, 6)], r=S.r * 0.8)),
    ]


@icon("wheel-chock", CAT, "Wedge shaped block wedged against the front of a tyre",
      tags=["wheel stop", "tire chock", "parking", "safety", "vehicle", "garage", "wedge"])
def _(S):
    return [
        line(arc(21, 11.5, 8.5, 90, 270)),
        shell(poly([(2.5, 20), (17, 20), (2.5, 9.5)], closed=True, r=S.r * 0.5)),
        detail(seg(5.5, 15.5, 8, 17.5)),
    ]


@icon("traffic-delineator-post", CAT, "Tall thin flexible post with two reflective bands on a round base",
      tags=["bollard", "flexible post", "road marker", "traffic", "reflective", "lane divider", "roadway"])
def _(S):
    return [
        shell(poly([(9.5, 2.5), (14.5, 2.5), (15.5, 17), (8.5, 17)], closed=True, r=S.r * 0.6)),
        detail(seg(9.5, 7, 14.5, 7)),
        detail(seg(9.5, 12, 14.5, 12)),
        shell(rect(3.5, 17, 17, 4.5, rr(S, 2))),
    ]
