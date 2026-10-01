"""TypeIcon Core: materials 001 (woods, boards, metals, glass, plastics, textiles).

Material samples drawn as swatches, boards and cut-away views. Textures are inner details so that
Filled knocks them out of the solid body.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, polar

CAT = "materials"


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def sdot(x, y, rx, ry) -> Part:
    """Small solid ellipse."""
    return Part("dot", ellipse(x, y, rx, ry))


def box(S, x=3, y=3, w=18, h=18, cap=None):
    return shell(rect(x, y, w, h, S.R if cap is None else min(S.R, cap)))


# ============================================================================ wood

@icon("pine-plank", CAT, "Pine board with wavy grain lines and two dark knots",
      tags=["pine", "softwood", "board", "lumber", "timber", "wood grain", "knot"])
def _(S):
    return [
        box(S, 2, 5, 20, 14),
        detail("M3 10a3 3 0 0 1 5 -1a3 3 0 0 0 5 0"),
        detail("M13 16a3 3 0 0 1 5 -1a3 3 0 0 0 4 0"),
        sdot(17, 10.5, 1.8, 1.2),
        sdot(7, 15, 1.4, 1),
    ]


@icon("oak-plank", CAT, "Oak board with nested arch grain rising from the bottom edge",
      tags=["oak", "hardwood", "board", "lumber", "cathedral grain", "wood grain", "plank"])
def _(S):
    return [
        box(S, 2, 3, 20, 18),
        detail("M6 21V14a6 6 0 0 1 12 0V21"),
        detail("M10 21V14a2 2 0 0 1 4 0V21"),
    ]


@icon("zebrawood-plank", CAT, "Board marked with bold parallel dark stripes",
      tags=["zebrawood", "striped wood", "exotic wood", "hardwood", "veneer", "board", "stripes"])
def _(S):
    return [
        box(S, 2, 5, 20, 14),
        detail(poly([(7, 5), (6, 19)])),
        detail(poly([(12, 5), (12, 19)])),
        detail(poly([(17, 5), (18, 19)])),
    ]


@icon("burl-wood", CAT, "Rounded wood slab with swirling grain and small eyes",
      tags=["burl", "burr", "burled wood", "knotty", "swirl grain", "slab", "exotic wood"])
def _(S):
    return [
        shell(ellipse(12, 12, 10, 8) if S.name == "rounded" else poly([(2, 12), (6, 5), (18, 4), (22, 12), (18, 20), (6, 19)], closed=True, r=2)),
        detail(ellipse(10.5, 12, 4.5, 2.6)),
        sdot(17.5, 8.5, 1.2, 1.2),
        sdot(17.5, 15.5, 1.2, 1.2),
    ]


@icon("spalted-wood", CAT, "Board crossed by thin irregular dark lines like a map",
      tags=["spalted", "spalting", "fungus lines", "zone lines", "figured wood", "maple", "board"])
def _(S):
    return [
        box(S, 2, 5, 20, 14),
        detail(poly([(2, 16), (8, 12), (13, 15), (22, 9)])),
        detail(poly([(8, 12), (10, 5)])),
        detail(poly([(13, 15), (15, 19)])),
    ]


@icon("balsa-sheet", CAT, "Thin flat wood sheet in perspective with a strip cut along its top face",
      tags=["balsa", "model making", "lightweight wood", "sheet", "craft wood", "hobby", "thin wood"])
def _(S):
    return [
        shell(poly([(2, 14), (7, 7), (22, 7), (22, 12), (17, 19), (2, 19)], closed=True, r=S.r)),
        detail(poly([(2, 14), (17, 14), (22, 7)])),
        detail(seg(17, 14, 17, 19)),
        detail(seg(13, 7, 10, 14)),
    ]


@icon("charred-wood", CAT, "Board covered in cracked scale-like blocks with a small flame at one corner",
      tags=["charred", "shou sugi ban", "burnt wood", "yakisugi", "alligator char", "fire", "burnt timber"])
def _(S):
    return [
        box(S, 2, 10, 20, 11),
        detail(poly([(8, 10), (8, 15), (12, 21)])),
        detail(poly([(2, 16), (8, 15), (15, 16), (15, 21)])),
        detail(poly([(15, 10), (15, 16), (22, 15)])),
        shell("M16 9C13.5 8 13.5 5 16 2.5C16 4.5 19 5 19 7C19 8 18 9 16 9Z", stroke_miterlimit="2"),
    ]


@icon("reclaimed-wood", CAT, "Weathered board with rough split ends and three old nail holes in a row",
      tags=["reclaimed", "salvaged wood", "barn wood", "weathered", "rustic", "nail holes", "recycled timber"])
def _(S):
    return [
        shell(poly([(3, 6), (21, 6), (19, 10), (22, 13), (21, 18), (3, 18), (5, 14), (2, 10)], closed=True, r=S.r * 0.4)),
        dot(8.5, 12, 1.1),
        dot(12, 12, 1.1),
        dot(15.5, 12, 1.1),
    ]


@icon("wood-veneer-sheet", CAT, "Thin sheet of wood with one corner curling up off a thick board",
      tags=["veneer", "wood veneer", "thin wood", "laminate", "marquetry", "edge banding", "peeling"])
def _(S):
    return [
        box(S, 2, 12, 20, 9),
        detail("M5 17h6"),
        line("M2 12H14C18 12 20 10 20 6"),
    ]


@icon("osb-board", CAT, "Square panel made of overlapping wood strands at random angles",
      tags=["osb", "oriented strand board", "sheathing", "engineered wood", "panel", "strands", "flakeboard"])
def _(S):
    return [
        box(S),
        detail(poly([(5, 8), (11, 6)])),
        detail(poly([(14, 6), (19, 9)])),
        detail(poly([(5, 13), (10, 11)])),
        detail(poly([(13, 12), (19, 13)])),
        detail(poly([(6, 18), (12, 17)])),
        detail(poly([(15, 17), (18, 20)])),
    ]


@icon("particle-board", CAT, "Panel seen edge-on with a speckled core between two smooth faces",
      tags=["particleboard", "chipboard", "engineered wood", "flat pack", "furniture board", "core", "panel edge"])
def _(S):
    return [
        box(S, 2, 5, 20, 14),
        detail(seg(2, 8.5, 22, 8.5)),
        detail(seg(2, 15.5, 22, 15.5)),
        dot(6, 12, 1),
        dot(10, 11.5, 1),
        dot(14, 12.5, 1),
        dot(18, 12, 1),
    ]


@icon("mdf-board", CAT, "Stack of two smooth flat panels in perspective with plain edges",
      tags=["mdf", "medium density fibreboard", "fiberboard", "engineered wood", "panel", "stack", "smooth board"])
def _(S):
    k = S.r * 2
    return [
        shell(poly([(2, 10), (6, 5), (22, 5), (22, 16), (18, 21), (2, 21)], closed=True, r=k)),
        detail(poly([(2, 10), (18, 10), (22, 5)])),
        detail(seg(18, 10, 18, 21)),
        detail(poly([(2, 15.5), (18, 15.5), (22, 10.5)])),
    ]


@icon("glulam-beam", CAT, "Beam end view with thin laminated layers glued together",
      tags=["glulam", "glued laminated timber", "laminated beam", "engineered timber", "layers", "structural beam"])
def _(S):
    return [
        box(S),
        detail(seg(3, 8, 21, 8)),
        detail(seg(3, 12, 21, 12)),
        detail(seg(3, 16, 21, 16)),
    ]


@icon("cross-laminated-timber", CAT, "Panel end with three layers, outer layers lengthwise and the middle layer end-on",
      tags=["clt", "mass timber", "cross laminated", "engineered timber", "panel", "layers", "plywood"])
def _(S):
    return [
        box(S),
        detail(seg(3, 9, 21, 9)),
        detail(seg(3, 15, 21, 15)),
        dot(7.5, 12, 1),
        dot(12, 12, 1),
        dot(16.5, 12, 1),
    ]


@icon("dimensional-lumber", CAT, "Square-cut stud in perspective with a growth ring arc on its end face",
      tags=["lumber", "stud", "two by four", "2x4", "timber", "framing", "growth rings", "construction wood"])
def _(S):
    return [
        shell(poly([(2, 9), (8, 3), (22, 3), (22, 15), (16, 21), (2, 21)], closed=True, r=S.r * 2)),
        detail(poly([(2, 9), (16, 9), (22, 3)])),
        detail(seg(16, 9, 16, 21)),
        detail(arc(2, 21, 6, -90, 0)),
    ]


@icon("hardwood-flooring", CAT, "Long floor planks laid in staggered running rows",
      tags=["hardwood floor", "wood floor", "planks", "parquet", "flooring", "boards", "laminate floor"])
def _(S):
    return [
        box(S),
        detail(seg(3, 9, 21, 9)),
        detail(seg(3, 15, 21, 15)),
        detail(seg(15, 3, 15, 9)),
        detail(seg(8, 9, 8, 15)),
        detail(seg(15, 15, 15, 21)),
    ]


@icon("wood-knot", CAT, "Grain lines flowing around a single dark oval knot",
      tags=["knot", "wood grain", "knothole", "lumber defect", "timber", "grain", "board"])
def _(S):
    return [
        box(S),
        detail("M9 3C6.5 8 6.5 16 9 21"),
        detail("M15 3C17.5 8 17.5 16 15 21"),
        sdot(12, 12, 1.5, 3.2),
    ]


# ============================================================================ metal

@icon("diamond-plate-metal", CAT, "Square metal plate with raised short bars set diagonally in alternating directions",
      tags=["diamond plate", "tread plate", "checker plate", "anti slip", "steel plate", "floor plate", "aluminium"])
def _(S):
    return [
        box(S),
        detail(seg(6, 10, 10, 6)),
        detail(seg(14, 6, 18, 10)),
        detail(seg(6, 14, 10, 18)),
        detail(seg(14, 18, 18, 14)),
    ]


@icon("perforated-metal-sheet", CAT, "Metal sheet with a grid of round holes and one folded corner",
      tags=["perforated", "punched metal", "holes", "sheet metal", "steel sheet", "speaker grille", "screen"])
def _(S):
    parts = [
        shell(poly([(3, 3), (15, 3), (21, 9), (21, 21), (3, 21)], closed=True, r=S.r)),
        detail(poly([(15, 3), (15, 9), (21, 9)])),
    ]
    for x, y in [(6.5, 8), (11, 8), (6.5, 12.5), (11, 12.5), (15.5, 13), (6.5, 17), (11, 17), (15.5, 17.5)]:
        parts.append(dot(x, y, 1.2))
    return parts


@icon("expanded-metal-mesh", CAT, "Sheet of stretched diamond openings in a staggered lattice",
      tags=["expanded metal", "mesh", "lattice", "diamond mesh", "grating", "steel mesh", "fence panel"])
def _(S):
    parts = [box(S)]
    for cx, cy in [(8, 8), (16, 8), (12, 12), (8, 16), (16, 16)]:
        parts.append(Part("dot", poly([(cx - 3, cy), (cx, cy - 2.2), (cx + 3, cy), (cx, cy + 2.2)], closed=True)))
    return parts


@icon("brushed-metal", CAT, "Metal plate with fine parallel brush lines and a diagonal shine",
      tags=["brushed", "brushed steel", "brushed aluminium", "satin finish", "metal finish", "texture", "stainless"])
def _(S):
    return [
        box(S),
        detail(seg(3, 9, 10, 9)),
        detail(seg(3, 13, 12, 13)),
        detail(seg(3, 17, 17, 17)),
        detail(seg(15, 5, 19, 9)),
    ]


@icon("hammered-metal", CAT, "Metal plate covered in overlapping round hammer dimples",
      tags=["hammered", "dimpled", "planished", "beaten metal", "copper", "craft metal", "texture"])
def _(S):
    return [
        box(S),
        detail(circle(8, 8, 3)),
        detail(circle(16, 8, 3)),
        detail(circle(8, 16, 3)),
        detail(circle(16, 16, 3)),
    ]


@icon("copper-patina", CAT, "Metal sheet smooth on one half and speckled where green patina spreads",
      tags=["patina", "verdigris", "oxidized copper", "corrosion", "weathered metal", "aged", "green copper"])
def _(S):
    return [
        box(S),
        detail("M11 3C9 7 13 9 11 12S13 17 11 21"),
        dot(15, 8, 1.2),
        dot(18.5, 11, 1.2),
        dot(15.5, 14, 1.2),
        dot(18.5, 17.5, 1.2),
        dot(14.5, 18, 1),
    ]


@icon("steel-channel", CAT, "Length of C-channel steel bar in perspective showing its squared U profile",
      tags=["channel", "c channel", "steel section", "structural steel", "u channel", "profile", "bar"])
def _(S):
    return [
        shell(poly([(2, 9), (6, 9), (6, 16), (10, 16), (10, 9), (14, 9), (14, 22), (2, 22)], closed=True, r=S.r * 0.4)),
        line(poly([(2, 9), (8, 3), (20, 3), (20, 16), (14, 22)])),
        line(seg(14, 9, 20, 3)),
    ]


@icon("square-steel-tube", CAT, "Hollow square tube in perspective with a visible square opening at the near end",
      tags=["steel tube", "box section", "square tubing", "hollow section", "shs", "structural steel", "pipe"])
def _(S):
    return [
        shell(poly([(2, 8), (8, 2), (22, 2), (22, 16), (16, 22), (2, 22)], closed=True, r=S.r * 2)),
        detail(poly([(2, 8), (16, 8), (22, 2)])),
        detail(seg(16, 8, 16, 22)),
        sq(6, 12, 6, 6, S.R * 0.7),
    ]


@icon("round-bar-stock", CAT, "Bundle of three solid round metal bars seen end-on",
      tags=["round bar", "bar stock", "rod", "steel rod", "bundle", "metal stock", "rebar"])
def _(S):
    parts = [shell(circle(7, 16, 4)), shell(circle(17, 16, 4)), shell(circle(12, 8, 4))]
    if S.name == "rounded":
        parts += [dot(7, 16, 1), dot(17, 16, 1), dot(12, 8, 1)]
    return parts


@icon("metal-shavings", CAT, "Tight curly spiral metal chip with two small loose pieces",
      tags=["shavings", "swarf", "chips", "turnings", "machining", "metal waste", "curls", "lathe"])
def _(S):
    return [
        line("M11 10A1 1 0 0 1 13 10A3 3 0 0 1 7 10A5 5 0 0 1 17 10A7 7 0 0 1 3 10"),
        dot(19.5, 19.5, 1.4),
        dot(6, 20.5, 1.2),
    ]


@icon("damascus-steel", CAT, "Knife blade filled with flowing wavy layered pattern lines",
      tags=["damascus", "pattern welded", "layered steel", "blade", "knife", "forged", "wavy pattern"])
def _(S):
    return [
        shell("M8 6H22C20 14 14 17 8 17Z", stroke_miterlimit="3"),
        shell(rect(2, 9, 6, 6, min(S.R, 2))),
        detail("M10 10a2 2 0 0 1 3 0a2 2 0 0 0 3 0"),
        detail("M10 14a2 2 0 0 1 3 0a2 2 0 0 0 3 0"),
    ]


# ============================================================================ glass

@icon("tempered-glass", CAT, "Glass pane broken into a mosaic of small square cubes",
      tags=["tempered", "toughened glass", "safety glass", "shattered", "cubes", "car window", "dice"])
def _(S):
    return [
        box(S),
        detail(seg(8, 3, 8, 21)),
        detail(seg(12, 3, 12, 16)),
        detail(seg(16, 8, 16, 21)),
        detail(seg(3, 8, 16, 8)),
        detail(seg(8, 12, 21, 12)),
        detail(seg(3, 16, 21, 16)),
    ]


@icon("laminated-glass", CAT, "Cracked glass pane held together by an inner layer, with a spider web crack",
      tags=["laminated", "safety glass", "windscreen", "spider crack", "cracked", "windshield", "interlayer"])
def _(S):
    return [
        box(S),
        detail(poly([(12, 12), (12, 3)])),
        detail(poly([(12, 12), (21, 8)])),
        detail(poly([(12, 12), (20, 21)])),
        detail(poly([(12, 12), (6, 21)])),
        detail(poly([(12, 12), (3, 9)])),
        detail(poly([(12, 6.5), (17, 9.5), (16, 16), (9, 17), (7, 10), (12, 6.5)])),
    ]


@icon("wired-glass", CAT, "Glass pane with a diamond wire mesh embedded in it",
      tags=["wired glass", "fire rated", "wire mesh", "safety glass", "embedded wire", "pane", "diamond mesh"])
def _(S):
    return [
        box(S),
        detail(seg(3, 9, 15, 21)),
        detail(seg(9, 3, 21, 15)),
        detail(seg(3, 15, 15, 3)),
        detail(seg(9, 21, 21, 9)),
    ]


@icon("reeded-glass", CAT, "Glass panel with vertical rounded ribs",
      tags=["reeded", "fluted glass", "ribbed glass", "textured glass", "privacy glass", "cabinet door", "vertical ribs"])
def _(S):
    return [
        box(S),
        detail(seg(7.5, 7, 7.5, 17)),
        detail(seg(12, 7, 12, 17)),
        detail(seg(16.5, 7, 16.5, 17)),
    ]


@icon("glass-block", CAT, "Thick square glass brick with an inner square and a wavy line across the face",
      tags=["glass brick", "glass block", "block window", "translucent", "bathroom window", "wall block", "pavers"])
def _(S):
    return [
        box(S),
        detail(rect(7, 7, 10, 10, S.R * 0.5)),
        detail("M9 12a1.5 1.5 0 0 1 3 0a1.5 1.5 0 0 0 3 0"),
    ]


@icon("glass-cullet", CAT, "Heap of broken angular glass pieces",
      tags=["cullet", "broken glass", "glass shards", "recycled glass", "glass recycling", "shards", "crushed glass"])
def _(S):
    return [
        shell(poly([(2, 21), (5, 15), (9, 16), (12, 8), (15, 13), (19, 12), (22, 21)], closed=True, r=S.r * 0.5)),
        detail(poly([(9, 16), (10, 21)])),
        detail(poly([(12, 8), (13, 15), (15, 21)])),
        detail(poly([(19, 12), (18, 21)])),
    ]


@icon("smart-glass", CAT, "Window pane frosted on one side and clear on the other with a lightning bolt beside it",
      tags=["smart glass", "switchable glass", "electrochromic", "privacy glass", "frosted", "smart window", "pdlc"])
def _(S):
    return [
        box(S, 2, 3, 14, 18),
        detail(seg(9, 3, 9, 21)),
        dot(5.5, 8, 1),
        dot(5.5, 12.5, 1),
        dot(5.5, 17, 1),
        line(poly([(21, 6), (18, 12), (21, 12), (18, 18)])),
    ]


# ============================================================================ plastics

@icon("plastic-pellets", CAT, "Small round plastic pellets spilling from a scoop",
      tags=["pellets", "granules", "resin", "nurdles", "plastic beads", "raw plastic", "masterbatch"])
def _(S):
    parts = [shell(poly([(13, 2), (22, 2), (20, 10), (15, 10)], closed=True, r=S.r))]
    for x, y in [(17.5, 14.5), (12, 15), (6.5, 14), (9, 19.5), (15.5, 19.5), (20, 19)]:
        parts.append(dot(x, y, 1.5))
    return parts


@icon("plastic-flakes", CAT, "Scattered irregular flat shredded plastic chips of mixed sizes",
      tags=["flakes", "regrind", "shredded plastic", "plastic chips", "recycled plastic", "granulate", "scrap"])
def _(S):
    return [
        shell(poly([(2, 4), (9, 3), (8, 10)], closed=True, r=S.r * 0.5)),
        shell(poly([(14, 3), (21, 6), (16, 10), (13, 8)], closed=True, r=S.r * 0.5)),
        shell(poly([(3, 14), (10, 13), (9, 20), (4, 19)], closed=True, r=S.r * 0.5)),
        shell(poly([(14, 14), (21, 15), (18, 21)], closed=True, r=S.r * 0.5)),
    ]


@icon("acrylic-sheet", CAT, "Clear slanted sheet with a corner of its protective film peeling away",
      tags=["acrylic", "perspex", "plexiglass", "clear plastic", "protective film", "peeling", "pmma"])
def _(S):
    return [
        shell(poly([(2, 20), (7, 9), (22, 9), (17, 20)], closed=True, r=S.r)),
        line("M7 9C7 5 11 3 15 4"),
        detail(seg(10, 16, 12, 12)),
    ]


@icon("polystyrene-foam", CAT, "Foam block in perspective with small packed round beads on its face",
      tags=["polystyrene", "styrofoam", "eps", "foam block", "packaging foam", "insulation", "beads"])
def _(S):
    return [
        shell(poly([(2, 9), (8, 3), (22, 3), (22, 15), (16, 21), (2, 21)], closed=True, r=S.r * 2)),
        detail(poly([(2, 9), (16, 9), (22, 3)])),
        detail(seg(16, 9, 16, 21)),
        dot(6, 14, 1.2),
        dot(11.5, 14, 1.2),
        dot(8.5, 18, 1.2),
    ]


@icon("twinwall-polycarbonate", CAT, "Panel end showing two thin walls joined by evenly spaced vertical ribs",
      tags=["twin wall", "polycarbonate", "multiwall", "greenhouse panel", "roofing sheet", "ribs", "glazing"])
def _(S):
    return [
        box(S, 2, 5, 20, 14),
        detail(seg(2, 9, 22, 9)),
        detail(seg(2, 15, 22, 15)),
        detail(seg(7.5, 9, 7.5, 15)),
        detail(seg(12, 9, 12, 15)),
        detail(seg(16.5, 9, 16.5, 15)),
    ]


@icon("printer-filament-spool", CAT, "Round spool wound with filament and one loose strand trailing off",
      tags=["filament", "3d printing", "spool", "pla", "abs", "printer filament", "reel"])
def _(S):
    return [
        shell(circle(11, 10, 7.5)),
        detail(circle(11, 10, 3.8)),
        dot(11, 10, 1.1),
        line("M11 17.5C11 21 16 21.5 21 20.5"),
    ]


@icon("injection-mold", CAT, "Two mold halves apart with a small molded part between and a nozzle feeding from the top",
      tags=["injection molding", "mould", "moulding", "plastic manufacturing", "tooling", "nozzle", "die"])
def _(S):
    return [
        shell(rect(2, 7, 5, 14, min(S.R, 2))),
        shell(rect(17, 7, 5, 14, min(S.R, 2))),
        sq(10, 13, 4, 5),
        shell(poly([(9, 2), (15, 2), (14, 7), (10, 7)], closed=True, r=S.r * 0.5)),
    ]


@icon("bioplastic", CAT, "Plastic bottle outline with a leaf inside its body",
      tags=["bioplastic", "biodegradable", "compostable", "plant based plastic", "pla", "eco bottle", "green plastic"])
def _(S):
    return [
        shell(poly([(10, 3), (14, 3), (14, 6), (17, 9), (17, 21), (7, 21), (7, 9), (10, 6)], closed=True, r=S.r)),
        Part("dot", "M12 19C9 17.5 9 13 14 12C15.5 15.5 14.5 18 12 19Z"),
    ]


@icon("plastic-free", CAT, "Bag inside a circle with a leaf where its handle would be",
      tags=["plastic free", "no plastic", "zero waste", "eco bag", "reusable", "bag", "sustainable"])
def _(S):
    return [
        shell(circle(12, 12, 10)),
        detail(poly([(8, 10), (16, 10), (17, 18), (7, 18)], closed=True, r=S.r)),
        Part("dot", "M12 9.5C9.5 8.5 9.5 5.5 12.5 4.5C14 7 13.5 8.5 12 9.5Z"),
    ]


@icon("memory-foam", CAT, "Thick foam slab in perspective with a deep dent in its top that holds its shape",
      tags=["memory foam", "viscoelastic", "mattress", "foam", "pillow", "cushion", "dent"])
def _(S):
    return [
        shell(poly([(2, 12), (7, 5), (22, 5), (22, 15), (17, 21), (2, 21)], closed=True, r=S.r * 2)),
        detail(poly([(2, 12), (17, 12), (22, 5)])),
        detail(seg(17, 12, 17, 21)),
        sdot(12, 8.7, 3.5, 1.3),
    ]


@icon("powder-coating", CAT, "Spray gun puffing a dotted powder cloud onto a hanging metal plate",
      tags=["powder coat", "powder coating", "spray gun", "paint finish", "coating", "electrostatic", "metal finish"])
def _(S):
    return [
        shell(rect(2, 5, 8, 5, 1)),
        shell(rect(3.5, 10, 3, 8, 1)),
        dot(13, 6.5, 1),
        dot(14.5, 10.5, 1),
        dot(12.5, 14.5, 1),
        dot(14.5, 18, 1),
        shell(rect(18, 6, 4, 14, 1)),
        line("M20 2V6"),
    ]


@icon("sandblasting", CAT, "Nozzle blasting a cone of grit onto a surface that is clean where the spray hits",
      tags=["sandblasting", "abrasive blasting", "grit blasting", "surface prep", "rust removal", "shot blasting", "nozzle"])
def _(S):
    return [
        shell(rect(2, 10, 6, 4, 1)),
        line("M9 11L17 5"),
        line("M9 13L17 19"),
        dot(12.5, 12, 1),
        dot(15.5, 9.5, 1),
        dot(15.5, 14.5, 1),
        line("M21 2L19.5 4L21 6V18L19.5 20L21 22"),
    ]


# ============================================================================ textiles (weaves and structure)

@icon("plain-weave", CAT, "Close-up of threads passing over and under one at a time like a checkerboard",
      tags=["plain weave", "tabby", "weave", "checkerboard", "woven fabric", "cotton", "loom", "thread"])
def _(S):
    parts = [box(S)]
    for r in range(4):
        for c in range(4):
            if (r + c) % 2 == 0:
                parts.append(sq(4 + c * 4, 4 + r * 4, 4, 4))
    return parts


@icon("twill-weave", CAT, "Close-up weave whose diagonal ribs step across the cloth",
      tags=["twill", "diagonal weave", "denim", "chino", "drill", "herringbone", "woven fabric"])
def _(S):
    return [
        box(S),
        detail(seg(3, 9, 15, 21)),
        detail(seg(3, 3, 21, 21)),
        detail(seg(9, 3, 21, 15)),
    ]


@icon("satin-weave", CAT, "Smooth glossy cloth with long floating threads and sweeping shine curves",
      tags=["satin", "sateen", "glossy fabric", "sheen", "smooth cloth", "weave", "lustrous"])
def _(S):
    return [
        box(S),
        detail("M6 18C11 18 16 13 18 6"),
        detail("M11 20C16 19 20 15 20 10"),
    ]


@icon("houndstooth-fabric", CAT, "Fabric square filled with rows of the broken-check pointed tooth pattern",
      tags=["houndstooth", "dogstooth", "check", "tweed pattern", "suit fabric", "pattern", "textile"])
def _(S):
    return [
        box(S),
        detail(poly([(3, 9), (7.5, 5), (12, 9), (16.5, 5), (21, 9)])),
        detail(poly([(3, 17), (7.5, 13), (12, 17), (16.5, 13), (21, 17)])),
    ]


@icon("seersucker-fabric", CAT, "Fabric square with flat stripes alternating with puckered crinkled stripes",
      tags=["seersucker", "puckered", "crinkle", "summer fabric", "striped cotton", "pucker stripes", "textile"])
def _(S):
    def vwave(x):
        d = f"M{x} 3"
        for i in range(6):
            d += f"a1.5 1.5 0 0 {1 if i % 2 == 0 else 0} 0 3"
        return d
    return [box(S), detail(vwave(8.5)), detail(vwave(15.5))]


@icon("corduroy-fabric", CAT, "Fabric square with raised vertical rounded ridges called wales",
      tags=["corduroy", "wale", "ribbed fabric", "cord", "ridges", "pants fabric", "textile"])
def _(S):
    return [
        box(S),
        detail(seg(7, 3, 7, 21)),
        detail(seg(12, 3, 12, 21)),
        detail(seg(17, 3, 17, 21)),
    ]


@icon("velvet-fabric", CAT, "Draped cloth with a soft pile edge and deep folds",
      tags=["velvet", "velour", "plush", "pile fabric", "drape", "luxury fabric", "curtain"])
def _(S):
    return [
        shell("M3 3H21V18C18 21 15 15 12 18S6 21 3 18Z"),
        detail("M9 3C8 8 10 13 9 18"),
        detail("M15 3C14 8 16 13 15 17"),
    ]


@icon("terry-cloth", CAT, "Fabric edge showing rows of small raised loops",
      tags=["terry cloth", "terrycloth", "towel", "looped pile", "bath towel", "loops", "toweling"])
def _(S):
    top = "M3 12" + "a2.25 2.25 0 0 1 4.5 0" * 4
    mid = "M3 17" + "a2.25 2.25 0 0 1 4.5 0" * 4
    return [box(S, 3, 12, 18, 9), line(top), detail(mid)]


@icon("waffle-weave-fabric", CAT, "Fabric square with a grid of recessed square pockets",
      tags=["waffle weave", "waffle cloth", "honeycomb", "towel", "pockets", "grid", "textured fabric"])
def _(S):
    return [
        box(S),
        detail(seg(9, 3, 9, 21)),
        detail(seg(15, 3, 15, 21)),
        detail(seg(3, 9, 21, 9)),
        detail(seg(3, 15, 21, 15)),
    ]


@icon("damask-fabric", CAT, "Fabric square with a large symmetrical floral medallion",
      tags=["damask", "jacquard", "medallion", "brocade", "ornate fabric", "floral pattern", "upholstery"])
def _(S):
    return [
        box(S),
        sdot(12, 7, 1.8, 2.4),
        sdot(12, 17, 1.8, 2.4),
        sdot(7, 12, 2.4, 1.8),
        sdot(17, 12, 2.4, 1.8),
        dot(12, 12, 1.3),
    ]


@icon("burlap-fabric", CAT, "Coarse open weave square with thick threads and visible gaps",
      tags=["burlap", "hessian", "jute", "sackcloth", "coarse weave", "rustic fabric", "open weave"])
def _(S):
    parts = [box(S)]
    for y in (6.5, 12, 17.5):
        for x in (6.5, 12, 17.5):
            parts.append(sq(x - 1.5, y - 1.5, 3, 3))
    return parts


@icon("tweed-fabric", CAT, "Fabric square with a rough woven texture of flecks and short dashes",
      tags=["tweed", "harris", "wool", "flecks", "country fabric", "herringbone", "jacket fabric"])
def _(S):
    return [
        box(S),
        detail(seg(6, 7, 9, 7)),
        dot(15, 7, 1),
        dot(18, 11, 1),
        detail(seg(6, 12, 8.5, 12)),
        detail(seg(12, 12, 14, 12)),
        dot(7, 17, 1),
        detail(seg(12, 17, 16, 17)),
    ]


@icon("quilted-fabric", CAT, "Puffy fabric square with diamond stitching and a button knot in the middle",
      tags=["quilted", "quilting", "padded", "stitched", "diamond stitch", "puffer", "bedspread"])
def _(S):
    return [
        box(S),
        detail(poly([(12, 3), (21, 12), (12, 21), (3, 12)], closed=True)),
        dot(12, 12, 1.4),
    ]


@icon("tie-dye-fabric", CAT, "Fabric square with a spiral burst of dyed bands",
      tags=["tie dye", "tie-dye", "spiral", "dyed", "hippie", "batik dye", "colourful fabric"])
def _(S):
    return [
        box(S),
        detail("M11.5 12.5A1 1 0 0 1 13.5 12.5A3 3 0 0 1 7.5 12.5A5 5 0 0 1 17.5 12.5"),
    ]


@icon("batik-fabric", CAT, "Fabric square with crackled wax-resist lines and a small flower",
      tags=["batik", "wax resist", "crackle", "javanese", "indonesian fabric", "dyed cloth", "flower"])
def _(S):
    return [
        box(S),
        detail(poly([(3, 8), (7, 9), (9, 13)])),
        detail(poly([(7, 9), (9, 5)])),
        sdot(16, 12, 1.4, 1.4),
        sdot(16, 8.5, 1.3, 1.8),
        sdot(16, 15.5, 1.3, 1.8),
        sdot(12.5, 12, 1.8, 1.3),
        sdot(19.5, 12, 1.3, 1.3),
    ]


@icon("ikat-fabric", CAT, "Fabric square with a diamond motif whose edges are broken into feathered dashes",
      tags=["ikat", "resist dyed", "blurred edge", "diamond motif", "woven pattern", "tribal fabric", "textile"])
def _(S):
    return [
        box(S),
        detail(seg(13.75, 6.75, 17.25, 10.25)),
        detail(seg(17.25, 13.75, 13.75, 17.25)),
        detail(seg(10.25, 17.25, 6.75, 13.75)),
        detail(seg(6.75, 10.25, 10.25, 6.75)),
        Part("dot", poly([(12, 9.5), (14.5, 12), (12, 14.5), (9.5, 12)], closed=True)),
    ]


@icon("mudcloth-fabric", CAT, "Fabric square with bold hand painted rows of dots, crosses and zigzags",
      tags=["mudcloth", "bogolan", "african textile", "mali", "tribal pattern", "hand painted", "dots and crosses"])
def _(S):
    return [
        box(S),
        dot(7, 7, 1.2),
        dot(12, 7, 1.2),
        dot(17, 7, 1.2),
        detail(poly([(5, 13), (8, 10.5), (11, 13), (14, 10.5), (17, 13), (19, 11.5)])),
        detail(seg(6, 17, 10, 17)),
        detail(seg(8, 15, 8, 19)),
        detail(seg(14, 17, 18, 17)),
        detail(seg(16, 15, 16, 19)),
    ]


@icon("tapa-cloth", CAT, "Bark cloth square with stamped geometric bands and triangles",
      tags=["tapa", "bark cloth", "pacific textile", "polynesian", "kapa", "stamped pattern", "triangles"])
def _(S):
    return [
        box(S),
        detail(seg(3, 8, 21, 8)),
        detail(seg(3, 16, 21, 16)),
        Part("dot", poly([(5, 14), (8, 10.5), (11, 14)], closed=True)),
        Part("dot", poly([(13, 14), (16, 10.5), (19, 14)], closed=True)),
    ]


@icon("mesh-fabric", CAT, "Fabric square with a regular pattern of open hexagonal holes",
      tags=["mesh", "net fabric", "breathable", "sportswear", "hexagon holes", "athletic mesh", "ventilated"])
def _(S):
    parts = [box(S)]
    for x, y in [(7.5, 7), (13.5, 7), (10.5, 12.5), (16.5, 12.5), (7.5, 18), (13.5, 18)]:
        parts.append(Part("dot", poly(regular(x, y, 2.4, 6), closed=True)))
    return parts


@icon("faux-fur", CAT, "Fabric swatch with a flat backing and a row of long fluffy strands along the top",
      tags=["faux fur", "fake fur", "fur fabric", "fluffy", "plush", "synthetic fur", "pile"])
def _(S):
    return [
        box(S, 3, 11, 18, 10),
        line("M5 11C5 9 6.5 8 7 5"),
        line("M9.5 11C9.5 9 11 8 11.5 4"),
        line("M14 11C14 9 15.5 8 16 5"),
        line("M18.5 11C18.5 9.5 19.5 9 20 7"),
    ]


@icon("tulle-fabric", CAT, "Gathered fabric ruffle with a zigzag edge and a fine hexagon net texture",
      tags=["tulle", "netting", "veil", "ballet tutu", "bridal fabric", "sheer", "ruffle"])
def _(S):
    return [
        shell(poly([(3, 6), (7.5, 3), (12, 6), (16.5, 3), (21, 6), (21, 18), (16.5, 21), (12, 18), (7.5, 21), (3, 18)], closed=True, r=S.r * 1.3)),
        Part("dot", poly(regular(12, 9.5, 1.7, 6), closed=True)),
        Part("dot", poly(regular(8.7, 14.5, 1.7, 6), closed=True)),
        Part("dot", poly(regular(15.3, 14.5, 1.7, 6), closed=True)),
    ]


@icon("non-woven-fabric", CAT, "Fabric square filled with random crossing curved fibers and no grid",
      tags=["non woven", "nonwoven", "felt", "fibre web", "interfacing", "spunbond", "random fibers"])
def _(S):
    return [
        box(S),
        detail("M3 8C8 4 12 11 21 7"),
        detail("M3 14C9 12 14 17 21 13"),
        detail("M5 21C9 17 15 20 19 17"),
    ]


@icon("selvedge", CAT, "Fabric edge with a tight woven border band and a column of small pin holes",
      tags=["selvedge", "selvage", "self edge", "fabric edge", "denim edge", "tenter holes", "woven border"])
def _(S):
    return [
        box(S),
        detail(seg(9, 3, 9, 21)),
        dot(6, 7, 0.9),
        dot(6, 12, 0.9),
        dot(6, 17, 0.9),
        detail(seg(9, 9, 21, 9)),
        detail(seg(9, 15, 21, 15)),
    ]


@icon("floral-print-fabric", CAT, "Fabric square with a scattered repeat of small flowers and leaves",
      tags=["floral print", "flower pattern", "ditsy", "chintz", "botanical fabric", "printed cotton", "flowers"])
def _(S):
    parts = [box(S)]
    for cx, cy in [(8, 8), (16.5, 13), (7.5, 17)]:
        parts += [dot(cx - 1.7, cy, 1.1), dot(cx + 1.7, cy, 1.1), dot(cx, cy - 1.7, 1.1), dot(cx, cy + 1.7, 1.1)]
    parts += [sdot(16, 6.5, 1.8, 1), sdot(18.5, 18, 1, 1.8)]
    return parts


@icon("fair-isle-pattern", CAT, "Knitted band with rows of small star and diamond motifs between stripe lines",
      tags=["fair isle", "knitting", "knitwear", "jumper pattern", "sweater", "nordic", "colourwork"])
def _(S):
    return [
        box(S, 2, 6, 20, 12),
        detail(seg(2, 9, 22, 9)),
        detail(seg(2, 15, 22, 15)),
        Part("dot", poly([(4, 12), (6.5, 10.4), (9, 12), (6.5, 13.6)], closed=True)),
        Part("dot", poly([(10.8, 12), (12, 10.4), (13.2, 12), (12, 13.6)], closed=True)),
        Part("dot", poly([(15, 12), (17.5, 10.4), (20, 12), (17.5, 13.6)], closed=True)),
    ]


@icon("linen-fabric", CAT, "Slightly uneven fabric square with wavy slubby thread lines",
      tags=["linen", "flax", "slub", "natural fabric", "wrinkled cloth", "uneven weave", "summer fabric"])
def _(S):
    return [
        box(S),
        detail("M3 8C7 7 10 9 15 8"),
        detail("M9 13C14 12 17 14 21 13"),
        detail("M3 18C8 17 12 19 18 18"),
    ]


@icon("silk-fabric", CAT, "Flowing wavy cloth with a smooth fold running through it",
      tags=["silk", "silky", "flowing fabric", "scarf", "satin sheen", "drape", "smooth cloth"])
def _(S):
    return [
        shell("M3 8C7 4 11 12 15 8S19 5 21 6V16C17 20 13 12 9 16S5 18 3 17Z"),
        detail("M10 8C11 11 9 13 10 16"),
    ]


@icon("plied-yarn", CAT, "Two strands twisting around each other into one thick yarn",
      tags=["yarn", "plied", "twisted yarn", "thread", "wool", "knitting", "spun fibre"])
def _(S):
    return [
        line("M3 7C7 7 8 17 12 17S17 7 21 7"),
        line("M3 17C7 17 8 7 12 7S17 17 21 17"),
    ]


@icon("hemp-fiber", CAT, "Bundle of long straight coarse fibers splaying from a tie at the middle",
      tags=["hemp", "fiber", "fibre", "natural fibre", "bast fibre", "rope fibre", "bundle"])
def _(S):
    return [
        line("M4 3L8.5 9"),
        line("M12 3V9"),
        line("M20 3L15.5 9"),
        line("M4 21L8.5 15"),
        line("M12 21V15"),
        line("M20 21L15.5 15"),
        shell(rect(6, 9, 12, 6, min(S.R, 2))),
    ]
