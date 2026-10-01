"""TypeIcon Core: insects and small creatures (batch 003)."""
import math

from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import D, P, ST, U, fmt, path_to_d, rotation, transform_path

CAT = "insects"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def rot(d, deg, cx, cy):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


def flip(d):
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def thick(d, w, S):
    return path_to_d(ST(d, w, S.cap, S.join))


def mark(d):
    """Small solid mark: solid in stroke styles, knocked out of a Filled body."""
    return Part("dot", d)


def lp(S, pts):
    return line(poly(pts, r=S.r))


def mir(pts):
    return [(24 - x, y) for x, y in pts]


def sym(S, *legs):
    out = []
    for pts in legs:
        out.append(lp(S, pts))
        out.append(lp(S, mir(pts)))
    return out


def eo(cx, cy, rx, ry, deg):
    return rot(ellipse(cx, cy, rx, ry), deg, cx, cy)


def rpts(pts, deg, cx=12.0, cy=12.0):
    """Rotate points clockwise on screen about (cx, cy)."""
    a = math.radians(deg)
    c, sn = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * sn, cy + (x - cx) * sn + (y - cy) * c) for x, y in pts]


def leafd(cx, top, bottom, w):
    my = (top + bottom) / 2
    k = w * 0.66
    return (f"M{fmt(cx)} {fmt(top)}C{fmt(cx + k)} {fmt(top + (my - top) * 0.35)} {fmt(cx + k)} {fmt(bottom - (bottom - my) * 0.35)} {fmt(cx)} {fmt(bottom)}"
            f"C{fmt(cx - k)} {fmt(bottom - (bottom - my) * 0.35)} {fmt(cx - k)} {fmt(top + (my - top) * 0.35)} {fmt(cx)} {fmt(top)}Z")


# --------------------------------------------------------------------------- damage, signs and galls

@icon("bee-sting", CAT, "Barbed stinger left in a swollen bump of skin",
      tags=["sting", "bee", "wasp", "stinger", "swelling", "allergy", "first aid"])
def _(S):
    bump = L(S, "M2 21C2 16.5 6 14 12 14C18 14 22 16.5 22 21Z",
             "M2 19C2 16 6 14 12 14C18 14 22 16 22 19Q22 21 20 21H4Q2 21 2 19Z")
    return [shell(bump), solid(poly([(10.5, 2.5), (13.5, 2.5), (13.5, 8), (15.2, 7.4), (12, 17), (8.8, 7.4), (10.5, 8)], closed=True))]


@icon("insect-swarm", CAT, "Cloud of tiny buzzing specks in a loose round shape",
      tags=["swarm", "plague", "infestation", "gnats", "midges", "buzzing", "locusts"])
def _(S):
    parts = [dot(x, y, r) for x, y, r in [(12, 3.5, 1.3), (6.5, 6, 1.1), (18, 5, 1.5), (3.5, 12, 1.3), (20.5, 12.5, 1.1),
                                          (11, 12, 1.5), (7, 18.5, 1.3), (17, 19, 1.3), (12, 21, 1)]]
    parts += [lp(S, [(7.5, 10), (9.5, 8)]), lp(S, [(14, 8), (16, 6)]), lp(S, [(14.5, 16), (16.5, 14)]), lp(S, [(5.5, 15.5), (7.5, 13.5)])]
    return parts


@icon("chewed-leaf", CAT, "Leaf with bite marks along its edge and holes in the middle",
      tags=["leaf damage", "pest damage", "caterpillar", "plant pest", "garden", "eaten leaf"])
def _(S):
    base = rot(leafd(12, 1.5, 19, 13), 35, 12, 12)
    bites = [circle(18.4, 6.4, 2.2), circle(20, 11.5, 2.2), circle(17.5, 16.3, 2)]
    body = minus(base, *bites, circle(10.5, 8.5, 1.7), circle(11.5, 13.5, 1.5))
    return [shell(body), lp(S, [(5.5, 20.5), (8.5, 15.5)])]


@icon("leaf-miner", CAT, "Leaf with a pale winding tunnel trail across its surface",
      tags=["leaf miner", "larva tunnel", "plant pest", "garden pest", "leaf trail", "crop damage"])
def _(S):
    return [shell(rot(leafd(12, 1.5, 19, 13), 35, 12, 12)), lp(S, [(5.5, 20.5), (8.5, 15.5)]),
            detail("M9 15C8 12 12.5 12.5 12 10C11.5 7.5 15.5 8 15 5.5")]


@icon("butterfly-net", CAT, "Long-handled hoop net with a deep mesh bag",
      tags=["net", "catch", "collect", "butterfly", "insect catching", "entomology", "hobby"])
def _(S):
    pouch = "M8.5 6.5C8.5 14 11.5 19 15 19C18.5 19 21.5 14 21.5 6.5Z"
    return [shell(union(pouch, ellipse(15, 6.5, 6.5, 2.4))), lp(S, [(3, 21.5), (8.2, 8)]),
            detail("M15 9V17"), detail("M11.5 9.5C11.5 12 12.5 15 13 16.5"), detail("M18.5 9.5C18.5 12 17.5 15 17 16.5")]


@icon("bug-jar", CAT, "Glass jar with a lid holding a twig and a small bug",
      tags=["jar", "collect", "catch", "bug", "terrarium", "kids", "nature study"])
def _(S):
    body = union(rect(7.5, 7, 9, 4, 0.5), rect(5, 9, 14, 12, L(S, 2.5, 5)))
    return [shell(rect(7, 3, 10, 4, min(S.R, 1.5))), shell(body),
            detail(poly([(8.5, 19), (15.5, 13)], r=S.r)), detail(poly([(12.5, 16), (15, 17.5)], r=S.r)),
            mark(ellipse(14.6, 12, 1.6, 1.1))]


@icon("specimen-box", CAT, "Shallow glass-topped case holding pinned insects",
      tags=["collection", "entomology", "mounted insects", "display case", "butterflies", "museum", "pinned"])
def _(S):
    bf = union(eo(7, 10, 3.3, 1.8, -35), eo(7, 10, 3.3, 1.8, 35))
    return [shell(rect(2.5, 4.5, 19, 15, S.R)), detail("M12 7V17"),
            mark(bf), mark(ellipse(17, 9, 1.5, 2.3)), mark(circle(7, 15.5, 1)), mark(circle(17, 15, 1))]


@icon("firefly-jar", CAT, "Jar with glowing fireflies inside",
      tags=["fireflies", "lightning bugs", "glow", "jar", "summer night", "lantern", "night"])
def _(S):
    body = union(rect(7.5, 7, 9, 4, 0.5), rect(5, 9, 14, 12, L(S, 2.5, 5)))
    return [shell(rect(7, 3, 10, 4, min(S.R, 1.5))), shell(body),
            mark(circle(9.5, 16.5, 1.4)), mark(circle(14.5, 13, 1.4)), mark(circle(14.5, 18, 1.1))]


@icon("cricket-cage", CAT, "Small domed bamboo cage with a ring handle",
      tags=["cage", "cricket", "pet insect", "chirping", "bamboo", "dome", "handle"])
def _(S):
    dome = "M4 18.5C4 10.5 7.5 6.5 12 6.5C16.5 6.5 20 10.5 20 18.5Z"
    return [shell(dome), detail("M8 8V18.5"), detail("M12 6.5V18.5"), detail("M16 8V18.5"),
            line("M9.5 6.5C9.5 2 14.5 2 14.5 6.5"), line("M3 21.5H21")]


@icon("butterfly-house", CAT, "Tall narrow box on a post with thin slots and a pitched roof",
      tags=["shelter", "butterfly box", "garden", "habitat", "nesting box", "wildlife garden", "post"])
def _(S):
    return [shell(rect(7, 8, 10, 10, min(S.R, 2))), shell(poly([(5, 8.5), (12, 2.5), (19, 8.5)], closed=True, r=S.r)),
            detail("M10 11V15.5"), detail("M14 11V15.5"), line("M12 18V22")]


@icon("spider-catcher", CAT, "Long pole with a cup at the end closing around a spider",
      tags=["spider", "catch and release", "reach pole", "humane", "pest", "grabber", "cup"])
def _(S):
    return [shell(rect(13, 2.5, 9, 9, L(S, 2, 4.5))), lp(S, [(3, 21.5), (13, 11.5)]),
            detail(poly([(15.3, 4.8), (19.7, 9.2)])), detail(poly([(15.3, 9.2), (19.7, 4.8)])), dot(17.5, 7, 1.5)]


@icon("flypaper", CAT, "Curled sticky strip hanging from a ceiling with flies stuck to it",
      tags=["fly strip", "sticky strip", "fly trap", "pest control", "catch flies", "hanging trap", "kitchen"])
def _(S):
    strip = thick("M9.5 5V14C9.5 18.5 14 19.5 16.5 17C18 15.5 17.3 13.5 15.5 13.5", 5, S)
    return [line("M4 2.5H20"), shell(strip), mark(circle(9.5, 8, 0.9)), mark(circle(9.5, 12, 0.9))]


@icon("mosquito-net", CAT, "Bell-shaped net canopy hanging over a bed",
      tags=["bed net", "canopy", "malaria", "travel", "insect protection", "sleeping", "bednet"])
def _(S):
    canopy = "M12 3.5C12 9 6 12 3.5 18H20.5C18 12 12 9 12 3.5Z"
    return [shell(union(canopy, rect(2.5, 17.5, 19, 4.5, L(S, 0.5, 2)))), detail("M12 7C11 11 9.5 14 8 17.5"),
            detail("M12 7C13 11 14.5 14 16 17.5"), dot(12, 2.2, 0.01) if False else line("M12 2V3.5")]


@icon("mosquito-racket", CAT, "Electric racket swatter with a mesh face and a spark",
      tags=["bug zapper", "swatter", "electric", "zap", "fly swatter", "mosquito killer", "racket"])
def _(S):
    head = rot(rect(6, 1.5, 12, 13.5, L(S, 4.5, 6)), 45, 12, 12)
    T = 45
    mesh = [poly(rpts([(12, 4.5), (12, 12)], T)), poly(rpts([(8.3, 8.6), (15.7, 8.6)], T))]
    return [shell(head), *[detail(m) for m in mesh], lp(S, rpts([(12, 15), (12, 22)], T)),
            lp(S, [(5.5, 2), (3.2, 5.5), (5.8, 5.5), (3.5, 9)])]


@icon("mosquito-fogger", CAT, "Handheld fogging machine with a long nozzle blowing a cloud",
      tags=["fogging", "fumigation", "thermal fogger", "spray", "pest control", "smoke", "vector control"])
def _(S):
    return [shell(rect(2.5, 9, 8.5, 10, L(S, 2, 3.5))), line("M4.5 9V5.5H9V9"), shell(rect(11, 12, 6, 3.4, 0.5)),
            dot(19.5, 8, 1.3), dot(21, 12.5, 1.6), dot(19, 16.5, 1.3)]


@icon("bug-spray", CAT, "Aerosol can spraying a mist with a small bug on its label",
      tags=["insect repellent", "aerosol", "pest spray", "bug killer", "insecticide", "repel", "mist"])
def _(S):
    return [shell(rect(3.5, 9.5, 9, 12, L(S, 2, 3.5))), shell(rect(5.5, 5, 5, 4.5, 0.5)),
            mark(ellipse(8, 16, 1.6, 2.2)),
            lp(S, [(12, 6.2), (15, 6.2)]), lp(S, [(17, 3), (20, 2.2)]), lp(S, [(17.5, 6.2), (21.5, 6.2)]), lp(S, [(17, 9.4), (20, 10.2)]),
            dot(15, 12.5, 1)]


@icon("citronella-candle", CAT, "Bucket candle with a flame and scent curls rising beside it",
      tags=["candle", "mosquito repellent", "outdoor", "patio", "scented", "tiki", "bug repellent"])
def _(S):
    return [shell(poly([(5, 11.5), (19, 11.5), (17, 21), (7, 21)], closed=True, r=S.r)),
            shell("M12 2.5C14.6 5.2 14.8 7.4 12 9.4C9.2 7.4 9.4 5.2 12 2.5Z" if S.name == "rounded" else "M12 2.5C15 5.2 15.2 7.4 12 9.4C8.8 7.4 9 5.2 12 2.5Z"),
            detail("M6 16H18"), line("M20.5 3.5C19 5.5 21.5 7 20 9"), line("M3.5 3.5C2 5.5 4.5 7 3 9")]


@icon("ant-bait-station", CAT, "Round disc trap with entrance gaps and an ant walking in",
      tags=["ant trap", "bait", "poison bait", "pest control", "ants", "disc", "kitchen"])
def _(S):
    arcs = [line(arc(12, 12, 9, a + 18, a + 72)) for a in (0, 90, 180, 270)]
    return [*arcs, dot(9, 15, 1.3), dot(12, 12, 1.5), dot(15.2, 8.8, 1.3),
            lp(S, [(10.8, 8.2), (9.8, 7)]), lp(S, [(13.5, 14.5), (14.8, 15.6)])]


@icon("roach-trap", CAT, "Small house-shaped cardboard trap with open door ends",
      tags=["cockroach", "sticky trap", "pest control", "glue trap", "box trap", "household pest", "kitchen"])
def _(S):
    return [shell(poly([(3, 20), (12, 4.5), (21, 20)], closed=True, r=S.r)), detail("M9 20C9 15 15 15 15 20"),
            mark(ellipse(12, 18.3, 1.2, 0.001) if False else circle(12, 18, 0.9))]


@icon("wasp-trap", CAT, "Hanging bottle trap with a funnel entrance and liquid bait",
      tags=["hornet", "yellow jacket", "bottle trap", "bait", "garden", "pest control", "hanging"])
def _(S):
    bottle = poly([(9.5, 6), (14.5, 6), (14.5, 8), (18, 11), (18, 20), (6, 20), (6, 11), (9.5, 8)], closed=True, r=S.r)
    return [line("M12 2V6"), shell(bottle), detail(poly([(8.5, 20), (10.5, 15), (13.5, 15), (15.5, 20)])), mark(circle(12, 11.5, 1.1))]


@icon("sticky-trap", CAT, "Grid-printed sticky card on a stake with a few bugs stuck to it",
      tags=["yellow card", "glue board", "greenhouse", "whitefly", "aphid trap", "monitoring", "garden"])
def _(S):
    return [shell(rect(3.5, 1.5, 17, 14, min(S.R, 2))), detail("M12 3.5V13.5"), detail("M5.5 8.5H18.5"),
            line("M12 15.5V22"), mark(circle(7.8, 5.8, 1)), mark(circle(16.2, 11.6, 1))]


@icon("insecticide-sprayer", CAT, "Pump pressure sprayer tank with a hose and a long wand",
      tags=["pesticide", "garden sprayer", "pump sprayer", "spray tank", "pest control", "farm", "knapsack"])
def _(S):
    return [shell(rect(2.5, 8.5, 10.5, 12.5, L(S, 2, 4))), line("M5 8.5V5.5H10.5V8.5"),
            lp(S, [(13, 14), (16.5, 14), (19.5, 7)]), dot(21.5, 3.5, 1), dot(21.8, 7.2, 1)]


@icon("fumigation-tent", CAT, "House fully covered by a striped tarp tent for pest treatment",
      tags=["termite treatment", "tenting", "pest control", "house", "tarp", "fumigate", "exterminator"])
def _(S):
    return [shell(poly([(2.5, 21), (2.5, 11), (12, 3), (21.5, 11), (21.5, 21)], closed=True, r=S.r)),
            detail("M7.5 9V21"), detail("M12 5.5V21"), detail("M16.5 9V21")]


@icon("flea-collar", CAT, "Pet collar ring with a buckle and a small bug tag",
      tags=["pet", "tick collar", "flea treatment", "dog", "cat", "parasite", "anti flea"])
def _(S):
    ring = minus(circle(12, 9, 7.5), circle(12, 9, 3.5))
    return [shell(ring), shell(rect(9, 17, 6, 5, L(S, 0.8, 2.5))), mark(ellipse(12, 19.5, 1.1, 1.4)), detail("M12 1.5V5.5")]


@icon("lice-comb", CAT, "Fine-toothed comb with long closely spaced teeth",
      tags=["nit comb", "head lice", "hair", "grooming", "parasite", "school nurse", "fine tooth"])
def _(S):
    return [shell(rect(3, 2.5, 18, 6.5, L(S, 2, 3))), *[line(seg(x, 9, x, 21)) for x in (4, 8, 12, 16, 20)],
            mark(ellipse(12, 5.7, 2.3, 1.2))]


@icon("tick-remover", CAT, "Small forked hook tool for twisting a tick out",
      tags=["tick twister", "parasite", "lyme disease", "hiking", "first aid", "tweezers", "tick"])
def _(S):
    return [shell(rect(8.5, 12, 7, 10, L(S, 2, 3.5))), lp(S, [(9.8, 12), (8.6, 5), (10.8, 3)]), lp(S, [(14.2, 12), (15.4, 5), (13.2, 3)]),
            dot(12, 7, 1.3)]


# --------------------------------------------------------------------------- beetles, ants, bugs and flies

@icon("hercules-beetle", CAT, "Side view of a beetle with a very long upper horn curving over a shorter lower horn",
      tags=["beetle", "rhinoceros beetle", "horned beetle", "giant insect", "tropical", "strongest", "horn"])
def _(S):
    body = union(ellipse(14.5, 14.5, 6.5, 4.3), ellipse(8, 13.3, 3.2, 3))
    return [shell(body), line("M9.5 10.8C8.5 5 5 3.3 2.5 7"), lp(S, [(5.5, 12.5), (3.2, 11.3)]),
            *[lp(S, p) for p in ([(9, 17), (8.5, 20)], [(15, 18.5), (15, 21)], [(19, 17.5), (20.5, 20)])]]


@icon("rove-beetle", CAT, "Side view of a slim beetle with short wing covers and its tail curled over its back",
      tags=["staphylinid", "devil's coach horse", "beetle", "curled tail", "insect", "predator", "bug"])
def _(S):
    tube = thick("M7 15H17C21 15 21.5 9.5 18 8.5", 3.4, S)
    body = union(tube, circle(4.6, 14.6, 2.2))
    return [shell(body), detail(seg(14, 13.3, 14, 16.7)), detail(seg(17.4, 13.5, 17.4, 16.5)),
            *[lp(S, p) for p in ([(7.5, 16), (6.5, 19.5)], [(10.5, 16.5), (10, 20)], [(13, 16.5), (13.5, 20)])],
            lp(S, [(3.5, 13), (1.8, 10.5)])]


@icon("trap-jaw-ant", CAT, "Top view of an ant with two long straight jaws snapped wide open across its head",
      tags=["ant", "mandibles", "jaws", "snap", "predator ant", "insect", "fast bite"])
def _(S):
    body = union(ellipse(12, 8.5, 3.2, 2.8), ellipse(12, 13.5, 2, 2.3), ellipse(12, 18.6, 3, 2.9))
    return [shell(body), lp(S, [(9.8, 7), (2.5, 4.3)]), lp(S, [(14.2, 7), (21.5, 4.3)]),
            *sym(S, [(10.2, 12.5), (6, 10.5), (4.5, 12.5)], [(10.2, 14.5), (5.5, 16), (4.5, 19)])]


@icon("katydid", CAT, "Side view of a green bush cricket with leaf wings, long hind legs and thread antennae",
      tags=["bush cricket", "long-horned grasshopper", "insect", "leaf mimic", "chirp", "antennae", "green"])
def _(S):
    wing = L(S, "M7 9.5C11 5.5 18 7.5 21.5 12.5C17 15 10 14.5 7 9.5Z", eo(14.3, 10.7, 7.6, 3.4, 18))
    return [shell(union(wing, circle(4.6, 10.6, 2.2))), detail(poly([(8.5, 10), (19, 12)])),
            line("M3.5 8.8C2.5 5.5 4.5 3 9 2.8"),
            *[lp(S, p) for p in ([(6, 13), (5, 19.5)], [(9.5, 14), (10.5, 20)], [(15, 14), (20, 18.5), (22, 22)])]]


@icon("springtail", CAT, "Side view of a tiny plump wingless hexapod with a forked spring tail tucked under it",
      tags=["collembola", "soil insect", "tiny", "jumping", "hexapod", "compost", "springtails"])
def _(S):
    return [shell(union(ellipse(13.5, 10, 7.5, 5.3), circle(5.2, 10.5, 2.4))), dot(5, 9.8, 0.8),
            *[lp(S, p) for p in ([(6.5, 14.5), (5.5, 18)], [(19.5, 14.5), (17, 19.5), (12, 19.5)],
                                 [(12, 19.5), (9.8, 17.8)], [(12, 19.5), (9.8, 21.5)])],
            lp(S, [(4, 8.5), (2.3, 6)])]


@icon("scorpionfly", CAT, "Side view of a slim winged fly with a long beak face and a bulb tail curled like a stinger",
      tags=["mecoptera", "scorpion", "insect", "curled tail", "beak", "wings", "bug"])
def _(S):
    return [shell(circle(6.2, 13, 2.1)), line("M8.3 13.3H15.5C20 13.5 21 9.5 19.2 7"), dot(19, 5.8, 1.7),
            lp(S, [(5, 14.3), (2.3, 17.5)]), shell(eo(12, 8, 5.5, 2, -10)),
            *[lp(S, p) for p in ([(9.5, 14.5), (8.5, 19)], [(12.5, 14.5), (13, 19.5)], [(15.5, 14.5), (17.5, 19)])]]


@icon("zebra-longwing", CAT, "Top view of a butterfly with long narrow striped wings",
      tags=["butterfly", "heliconius", "stripes", "tropical butterfly", "zebra", "wings", "lepidoptera"])
def _(S):
    def axis(cx, cy, r, deg):
        a = math.radians(deg)
        return poly([(cx - r * math.cos(a), cy - r * math.sin(a)), (cx + r * math.cos(a), cy + r * math.sin(a))])
    fore = eo(7.6, 7.2, 6.4, 2.4, 45)
    hind = eo(8, 16.6, 4.8, 2.3, -35)
    wings = union(fore, hind, flip(fore), flip(hind))
    return [shell(wings), detail(axis(7.6, 7.2, 4.4, 45)), detail(axis(16.4, 7.2, 4.4, -45)),
            detail(axis(8, 16.6, 2.8, -35)), detail(axis(16, 16.6, 2.8, 35)),
            line("M12 8.5V18.5"), lp(S, [(11, 7.5), (9.5, 4)]), lp(S, [(13, 7.5), (14.5, 4)])]


@icon("fruit-fly", CAT, "Tiny fly with big round eyes perched on the cut end of a banana",
      tags=["drosophila", "vinegar fly", "kitchen pest", "banana", "tiny fly", "gnat", "compost"])
def _(S):
    return [shell(union(ellipse(13.5, 6.5, 5, 3), circle(8, 6, 2.6))),
            shell(poly([(12, 12.5), (21, 21), (3, 21)], closed=True, r=L(S, 2, 4))),
            lp(S, [(14, 4.5), (19, 2.2), (21.5, 3.6)]), lp(S, [(11.3, 9.5), (10.5, 12.3)]), lp(S, [(15.5, 9.5), (16, 12)]),
            mark(circle(12, 17.5, 0.9)), mark(circle(7.9, 5.7, 0.8))]


@icon("giant-water-bug", CAT, "Top view of a flat oval water bug with grasping front legs and eggs on its back",
      tags=["toe biter", "belostomatid", "aquatic insect", "pond", "eggs", "predator", "water bug"])
def _(S):
    return [shell(union(ellipse(12, 14, 5.3, 7), circle(12, 6.2, 2.5))),
            *[mark(circle(x, y, 0.9)) for x, y in [(10.2, 11.5), (13.8, 11.5), (10.2, 14.8), (13.8, 14.8), (12, 18)]],
            *sym(S, [(9.5, 7), (5.5, 5), (4.5, 2.5)], [(7.3, 12), (3, 12)], [(7.5, 16.5), (3, 19)], [(9.5, 19.8), (7, 22)])]


@icon("house-centipede", CAT, "Top view of a short centipede fringed by very long thin legs and long antennae",
      tags=["centipede", "arthropod", "many legs", "household pest", "creepy crawly", "scutigera", "bug"])
def _(S):
    legs = []
    for y, kx, ky, ex, ey in [(9.5, 6.5, 6.5, 2.5, 7.5), (13, 6, 11, 2, 13.5), (16.5, 6.5, 15.5, 3.5, 20.5)]:
        legs += sym(S, [(10.5, y), (kx, ky), (ex, ey)])
    return [shell(ellipse(12, 12.5, 2.1, 5.5)), *legs, *sym(S, [(11.3, 7.3), (9, 2.5)], [(11.3, 18), (10, 22)])]


@icon("varroa-mite", CAT, "Top view of a honeybee with a small round mite stuck on its back",
      tags=["bee parasite", "beekeeping", "honeybee", "mite", "hive pest", "apiary", "bee disease"])
def _(S):
    body = union(ellipse(12, 14.3, 4.6, 6.6), circle(12, 6.3, 2.5), eo(6.3, 10.3, 3.6, 1.7, -50), eo(17.7, 10.3, 3.6, 1.7, 50))
    return [shell(body), detail(seg(8.3, 16.3, 15.7, 16.3)), detail(seg(9, 19, 15, 19)), mark(ellipse(12, 12.3, 2.3, 1.8)),
            lp(S, [(11, 4.5), (9.5, 2)]), lp(S, [(13, 4.5), (14.5, 2)])]


@icon("mealworm", CAT, "Side view of a golden segmented larva with tiny legs near the head",
      tags=["larva", "beetle larva", "feed", "bait", "insect protein", "worm", "grub"])
def _(S):
    return [shell(rect(3, 8, 18, 7.5, L(S, 2.5, 3.75))), detail(seg(8.5, 8, 8.5, 15.5)), detail(seg(12.5, 8, 12.5, 15.5)),
            detail(seg(16.5, 8, 16.5, 15.5)), dot(5.8, 11.3, 0.9),
            *[lp(S, p) for p in ([(5.5, 15.5), (4.5, 19)], [(8.5, 15.5), (8.5, 19.5)], [(11.5, 15.5), (12.5, 19)])]]


@icon("brown-recluse", CAT, "Top view of a slender long-legged spider with a violin mark on its front body",
      tags=["spider", "violin spider", "venomous", "recluse", "arachnid", "loxosceles", "bite"])
def _(S):
    body = union(circle(12, 8.3, 3.8), ellipse(12, 16, 4.1, 4.7))
    return [shell(body), mark(union(circle(12, 7, 1), ellipse(12, 9.4, 1.4, 1.2))),
            *sym(S, [(9, 6.5), (5, 3), (2.5, 5)], [(8.3, 8.5), (3, 8)], [(8.3, 10.5), (3.5, 13), (2.5, 16.5)], [(9.3, 12.5), (6.5, 17), (5.5, 21.5)])]


# --------------------------------------------------------------------------- nests, webs and homes

@icon("spittlebug-foam", CAT, "Frothy blob of bubbles clinging to a plant stem with a tiny bug inside",
      tags=["cuckoo spit", "froghopper", "froth", "bubbles", "plant pest", "stem", "garden"])
def _(S):
    k = L(S, 0, 0.3)
    foam = union(circle(9.3, 12, 3.1 + k), circle(14.7, 12, 3.1 + k), circle(12, 8.8, 3 + k), circle(12, 15.3, 3 + k), circle(7.5, 16, 2.1), circle(16.7, 8, 2))
    return [shell(foam), line("M12 2V5.6"), line("M12 18.4V22"), mark(ellipse(12, 12, 1.3, 0.9))]


@icon("funnel-web", CAT, "Flat sheet of web draped over a surface and narrowing into a funnel tunnel",
      tags=["spider web", "funnel weaver", "sheet web", "tunnel", "spider", "cobweb", "lair"])
def _(S):
    funnel = poly([(8, 9), (10.5, 21), (13.5, 21), (16, 9)], closed=True, r=S.r)
    return [shell(union(ellipse(12, 8, 9.5, 4), funnel)), detail("M5.5 6.5L10 9"), detail("M18.5 6.5L14 9"), detail("M12 4.5V8"),
            mark(ellipse(12, 12.5, 1, 1.8))]


@icon("ballooning-spider", CAT, "Tiny spider floating through the air on a fan of silk threads",
      tags=["spider", "silk", "parachute", "floating", "gossamer", "drifting", "migration"])
def _(S):
    return [lp(S, [(12, 12), (5, 2.5)]), lp(S, [(12, 12), (12, 2.5)]), lp(S, [(12, 12), (19, 2.5)]), line("M12 12V16"),
            dot(12, 18.3, 2),
            *sym(S, [(10.2, 17.3), (7.5, 15.8)], [(10.2, 19.3), (7.5, 21)])]


@icon("weaver-ant-nest", CAT, "Round ball of leaves stitched with silk hanging from a branch",
      tags=["ant nest", "leaf nest", "tree", "weaver ants", "silk", "tropical", "hanging nest"])
def _(S):
    ball = poly(regular(12, 14.5, 7.3, 8, -22.5), closed=True, r=L(S, 0, 3))
    return [line("M2.5 3.5H21.5"), line("M12 3.5V7.2"), shell(ball), detail("M12 9C8.5 11 8.5 18 12 20"),
            detail("M12 9C15.5 11 15.5 18 12 20")]


@icon("mud-dauber-nest", CAT, "Row of long mud tubes side by side like organ pipes stuck to a wall",
      tags=["wasp nest", "mud tubes", "organ pipe", "dirt dauber", "wall", "pest", "nest"])
def _(S):
    parts = [line("M2 3H22")]
    for x, h in [(3, 14), (10, 17), (17, 11)]:
        parts.append(shell(rect(x, 4.5, 4, h, L(S, 1, 2))))
        parts.append(mark(circle(x + 2, 4.5 + h - 2.3, 0.8)))
    return parts


@icon("paper-wasp-nest", CAT, "Open umbrella comb of hexagon cells hanging from a stalk under a beam",
      tags=["wasp", "paper nest", "honeycomb", "cells", "hexagon", "hanging nest", "beam"])
def _(S):
    comb = poly(regular(12, 14, 8, 6, 0), closed=True, r=L(S, 0, 3))
    cells = [(12, 14), (8.4, 14), (15.6, 14), (10.2, 10.9), (13.8, 10.9), (10.2, 17.1), (13.8, 17.1)]
    return [line("M2.5 2.5H21.5"), line("M12 2.5V7.2"), shell(comb),
            *[mark(poly(regular(x, y, 1.25, 6, 0), closed=True)) for x, y in cells]]


@icon("tent-caterpillar-nest", CAT, "Silky web tent filling the fork of a branch with caterpillars crawling on it",
      tags=["webworm", "caterpillar", "silk tent", "tree pest", "web", "orchard", "nest"])
def _(S):
    web = L(S, "M4.5 12.5C2.5 8.5 5.5 4.5 9.5 5C10.5 2.5 15 2.5 16.3 5C20 5 21.8 9 19.5 12.5C17 15 7 15 4.5 12.5Z",
            "M5 12.3C3 8.7 6 5 9.8 5.4C11 3 14.8 3 16 5.4C19.5 5.4 21.2 9 19 12.3C17 14.8 7 14.8 5 12.3Z")
    return [line("M12 22V16"), line("M12 16L8 12.5"), line("M12 16L16 12.5"), shell(web),
            mark(ellipse(10, 9.2, 1.4, 0.8)), mark(ellipse(14.8, 8.2, 1.4, 0.8)), mark(ellipse(12.5, 11.7, 1.3, 0.7))]


@icon("moth-eaten-sweater", CAT, "Sweater with ragged holes and a small moth fluttering beside it",
      tags=["clothes moth", "holes", "knitwear", "wardrobe", "pest damage", "wool", "damaged clothes"])
def _(S):
    sw = poly([(8, 5), (2.5, 11.5), (2.5, 16.5), (5.5, 16.5), (7, 14), (7, 21.5), (15.5, 21.5), (15.5, 14), (17, 16.5), (20, 16.5), (20, 11.5), (14.5, 5)],
              closed=True, r=S.r)
    body = minus(sw, circle(10.6, 12, 1.6), circle(12.6, 17.5, 1.5))
    moth = union(eo(17.3, 4.6, 2.3, 1.2, -25), eo(21, 4.6, 2.3, 1.2, 25))
    return [shell(body), detail("M8.5 5C9.5 7.5 13 7.5 14 5"), mark(moth)]


# --------------------------------------------------------------------------- gear, habitats and small scenes

@icon("mantis-egg-case", CAT, "Rounded foamy egg case with ridged layers glued along a twig",
      tags=["ootheca", "praying mantis", "eggs", "twig", "egg sac", "overwintering", "garden"])
def _(S):
    return [line("M2 21C8 20 15 19.5 22 17"), shell(rect(6.5, 3.5, 11, 15.5, L(S, 4, 5.5))),
            detail(poly([(7, 8), (17, 8)])), detail(poly([(7, 11.5), (17, 11.5)])), detail(poly([(7, 15), (17, 15)]))]


@icon("insect-aspirator", CAT, "Small jar whose lid has two tubes, one to suck and one to collect bugs",
      tags=["pooter", "bug catcher", "entomology", "collect insects", "suction", "field work", "tubes"])
def _(S):
    return [shell(rect(5, 9, 14, 12, L(S, 2.5, 5))), shell(rect(7.5, 5.5, 9, 3.5, 0.8)),
            line("M10 5.5V3.5C10 2.5 9 2.5 8 2.5H3"), line("M14 5.5V3.5C14 2.5 15 2.5 16 2.5H21"), mark(ellipse(12, 16.5, 1.7, 1.1))]


@icon("bug-viewer", CAT, "Small clear box with a round magnifying lens in its lid and a bug inside",
      tags=["magnifier", "bug box", "observation", "kids science", "nature study", "lens", "insect box"])
def _(S):
    return [shell(rect(3, 11, 18, 10.5, L(S, 2, 3.5))), shell(circle(12, 6.5, 4.5)), detail("M9.8 5C10.4 4 11.3 3.6 12.3 3.6"),
            mark(ellipse(12, 16.5, 3, 1.7))]


@icon("insect-terrarium", CAT, "Glass tank with a mesh lid and a branch with a mantis or stick insect on it",
      tags=["vivarium", "pet insect", "praying mantis", "stick insect", "enclosure", "glass tank", "habitat"])
def _(S):
    return [shell(rect(2.5, 9, 19, 12.5, L(S, 2, 3.5))), shell(rect(2.5, 4, 19, 5, L(S, 1, 2))),
            detail(poly([(5.5, 19.5), (10, 15.5), (15, 13.5), (19, 11)], r=S.r)), mark(ellipse(14.2, 12.2, 2.2, 0.9)),
            mark(circle(7, 6.5, 0.7)), mark(circle(12, 6.5, 0.7)), mark(circle(17, 6.5, 0.7))]


@icon("amber-insect", CAT, "Drop of amber with a small winged insect trapped inside and a shine highlight",
      tags=["fossil", "resin", "prehistoric", "trapped insect", "jurassic", "gem", "specimen"])
def _(S):
    drop = L(S, "M12 2.5C17 8 20.5 12 20.5 16C20.5 19.5 16.5 21.5 12 21.5C7.5 21.5 3.5 19.5 3.5 16C3.5 12 7 8 12 2.5Z",
             "M12 3C14 4.5 20.5 12 20.5 16C20.5 19.5 16.5 21.5 12 21.5C7.5 21.5 3.5 19.5 3.5 16C3.5 12 10 4.5 12 3Z")
    bug = union(ellipse(12, 15, 1.3, 3), eo(9.7, 13.5, 2.3, 1, -40), eo(14.3, 13.5, 2.3, 1, 40))
    return [shell(drop), mark(bug), detail("M7.2 17C6.8 15.2 7.3 13.6 8.3 12.4")]


@icon("mosquito-plug-in", CAT, "Wall plug-in repellent device with a vapor wisp and a mosquito flying away",
      tags=["repellent", "electric", "outlet", "vaporizer", "mosquito", "anti mosquito", "bedroom"])
def _(S):
    mosq = union(ellipse(19, 12.5, 2.6, 1.1), eo(18, 9.8, 2.3, 0.9, -55), eo(20.3, 9.8, 2.3, 0.9, 55))
    return [shell(rect(3.5, 9.5, 10.5, 9, L(S, 2, 3.5))), shell(rect(6.5, 6.5, 4.5, 3, 0.5)), line("M6.5 18.5V22"), line("M11 18.5V22"),
            line("M8.8 4.8C7.5 3.8 10.1 3 8.8 2"), mark(mosq)]


@icon("insect-screen", CAT, "Window frame filled with fine mesh and a fly resting on it",
      tags=["fly screen", "window screen", "mesh", "mosquito screen", "window", "protection", "wire mesh"])
def _(S):
    return [shell(rect(2.5, 2.5, 19, 19, L(S, 2, 4))), detail("M8.5 4.5V19.5"), detail("M15.5 4.5V19.5"),
            detail("M4.5 8.5H19.5"), detail("M4.5 15.5H19.5"), mark(ellipse(12, 12, 2, 1.4)), mark(eo(10.8, 10.3, 1.6, 0.7, -30))]


@icon("slug-trap", CAT, "Cup sunk into the soil under a small rain cover with a slug heading toward it",
      tags=["slug", "snail", "garden", "beer trap", "pest control", "cup", "vegetable patch"])
def _(S):
    return [line("M2 14.5H7"), line("M17 14.5H22"), shell(rect(7.5, 14.5, 9, 7, L(S, 1.5, 3))), detail(poly([(9.5, 17.5), (14.5, 17.5)])),
            shell(rect(5, 5, 14, 3.5, L(S, 1, 1.75))), line("M7 8.5V12"), line("M17 8.5V12"),
            mark(ellipse(4.2, 12.2, 2.4, 1.1)), lp(S, [(2.5, 11.4), (1.8, 9.5)])]


@icon("butterfly-feeder", CAT, "Round dish hanging on three strings holding orange slices",
      tags=["feeder", "nectar", "fruit", "garden", "hanging", "orange slices", "butterfly garden"])
def _(S):
    dish = L(S, "M2.5 13H21.5C21.5 18.5 17.5 21 12 21C6.5 21 2.5 18.5 2.5 13Z", "M2.5 13.5C2.5 13.1 3 13 4 13H20C21 13 21.5 13.1 21.5 13.5C21.5 18.5 17.5 21 12 21C6.5 21 2.5 18.5 2.5 13.5Z")
    return [line("M10.4 4A1.6 1.6 0 1 1 13.6 4"), lp(S, [(11, 5.4), (3, 13)]), line("M12 5.6V13"), lp(S, [(13, 5.4), (21, 13)]),
            shell(dish), mark("M6.2 13.5A2.7 2.7 0 0 1 11.6 13.5Z"), mark("M12.4 13.5A2.7 2.7 0 0 1 17.8 13.5Z")]


@icon("bee-bath", CAT, "Shallow dish of water with pebbles poking above the surface and a bee drinking",
      tags=["pollinator", "water dish", "garden", "bee drinking", "wildlife", "pebbles", "save the bees"])
def _(S):
    dish = L(S, "M2.5 12.5H21.5C21.5 18 17.5 20.5 12 20.5C6.5 20.5 2.5 18 2.5 12.5Z", "M2.5 13C2.5 12.6 3 12.5 4 12.5H20C21 12.5 21.5 12.6 21.5 13C21.5 18 17.5 20.5 12 20.5C6.5 20.5 2.5 18 2.5 13Z")
    bee = union(ellipse(16.5, 8.8, 2.4, 1.6), eo(15.6, 6.2, 1.7, 0.9, -35), circle(14.2, 9.3, 1.1))
    return [shell(dish), detail("M6 16.5C7.5 15.3 9 15.3 10.5 16.5S13.5 17.7 15 16.5S17.5 15.5 18.5 16.5"),
            mark(ellipse(6.8, 12.2, 2, 1.1)), mark(ellipse(11.3, 12.2, 1.6, 1)), mark(bee)]


@icon("butterfly-migration", CAT, "Three butterflies flying along a long curved arrow",
      tags=["monarch", "migrate", "journey", "flight path", "seasonal", "butterflies", "travel"])
def _(S):
    def bf(x, y):
        return mark(union(circle(x - 1.9, y - 0.7, 1.9), circle(x + 1.9, y - 0.7, 1.9), circle(x - 1.3, y + 1.7, 1.3), circle(x + 1.3, y + 1.7, 1.3)))
    return [line("M3 21C11 21.5 19.5 16 21 8.5"), lp(S, [(17.6, 11), (21, 7.7), (22.6, 11.7)]),
            bf(5, 13.5), bf(10.5, 9), bf(16, 4.8)]


@icon("leech-jar", CAT, "Old apothecary jar with a lid and side handles holding wriggling leeches",
      tags=["leeches", "apothecary", "medical history", "bloodletting", "worms", "glass jar", "antique"])
def _(S):
    return [shell(rect(6.5, 8, 11, 13.5, L(S, 2.5, 5))), shell(rect(8, 3.5, 8, 3.5, L(S, 0.8, 1.5))), line("M6.5 11.5C3.5 11.5 3.5 16.5 6.5 16.5"),
            line("M17.5 11.5C20.5 11.5 20.5 16.5 17.5 16.5"),
            detail("M9 13C10 11.6 11 11.6 12 13S14 14.4 15 13"), detail("M9 17.5C10 16.1 11 16.1 12 17.5S14 18.9 15 17.5")]


@icon("rotifer", CAT, "Tiny vase-shaped animal with a ciliated crown on top and a forked foot below",
      tags=["microscope", "plankton", "microorganism", "wheel animal", "pond life", "biology", "freshwater"])
def _(S):
    body = L(S, "M6.5 6.5H17.5C16 10 15.5 14 14 17H10C8.5 14 8 10 6.5 6.5Z", "M7 6.8H17C15.8 10 15.5 14 14 17H10C8.5 14 8.2 10 7 6.8Z")
    return [shell(body), dot(8.2, 3.3, 0.9), dot(12, 2.8, 0.9), dot(15.8, 3.3, 0.9), line("M12 17V19.5"),
            lp(S, [(12, 19.5), (9.5, 22)]), lp(S, [(12, 19.5), (14.5, 22)]), mark(circle(12, 11.5, 1.2))]


@icon("anthill", CAT, "Cone-shaped soil mound with an entrance hole at the top and two ants walking on it",
      tags=["ants", "mound", "colony", "nest", "soil", "entrance", "insects"])
def _(S):
    mound = L(S, "M2 20.5C6 20 8.8 17 9.8 12L11 8.5Q12 7.5 13 8.5L14.2 12C15.2 17 18 20 22 20.5Z",
              "M2.5 20.5C6 20 8.8 17 9.8 12Q10.6 8.8 12 8.8Q13.4 8.8 14.2 12C15.2 17 18 20 21.5 20.5Z")
    def ant(x, y, d):
        return mark(union(circle(x, y, 0.9), circle(x + d * 1.8, y - 0.2, 1), circle(x + d * 3.7, y - 0.4, 1.3)))
    return [shell(mound), mark(ellipse(12, 12.2, 1.1, 1)), ant(6.3, 18, 1), ant(17.7, 17.5, -1)]
