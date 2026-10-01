"""TypeIcon Core: objects, batch 003 (household oddments)."""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401

CAT = "objects"


def rot(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


@icon("joss-paper", CAT, "Square sheet of paper with a foil square in the middle",
      tags=["ghost money", "spirit paper", "burning paper", "offering", "ritual", "foil"])
def _(S):
    return [
        shell(rect(4, 4, 16, 16, rr(S, 2))),
        Part("dot", rect(8.5, 8.5, 7, 7, 1 if S.name == "rounded" else 0)),
    ]


@icon("offering-bowl", CAT, "Footed bowl heaped with round fruit",
      tags=["fruit bowl", "offering", "altar", "shrine", "fruit", "ritual"])
def _(S):
    return [
        shell(poly([(4, 15), (20, 15), (17.5, 20), (6.5, 20)], closed=True, r=S.r)),
        line(seg(8.5, 21.5, 15.5, 21.5)),
        dot(8, 11, 2), dot(16, 11, 2), dot(12, 7.5, 2),
    ]


@icon("wind-spinner", CAT, "Twisted metal spiral hanging from a hook and spinning",
      tags=["garden spinner", "hanging spiral", "kinetic", "yard decor", "whirligig", "twister"])
def _(S):
    top = circle(12, 3.5, 1.5) if S.name == "rounded" else poly([(12, 2), (13.5, 3.5), (12, 5), (10.5, 3.5)], closed=True)
    return [
        shell(top),
        line("M12 6.5C5 9 5 12 12 14C19 16 19 19 12 21.5"),
        line("M12 6.5C19 9 19 12 12 14C5 16 5 19 12 21.5"),
    ]


@icon("mounted-antlers", CAT, "Pair of antlers fixed to a shield-shaped wall plaque",
      tags=["trophy", "hunting", "deer", "wall mount", "lodge", "cabin decor", "rack"])
def _(S):
    return [
        shell(poly([(6, 14.5), (18, 14.5), (18, 18)], closed=False) + "C18 20 15 21 12 22C9 21 6 20 6 18Z"),
        line("M10 14.5C9.5 10 7.5 7 4 4"),
        line("M8.8 9.2L4 10"),
        line("M14 14.5C14.5 10 16.5 7 20 4"),
        line("M15.2 9.2L20 10"),
    ]


@icon("push-plate", CAT, "Metal plate on a door with an arrow showing the push direction",
      tags=["door", "push", "entrance", "plate", "commercial door", "hardware", "shop door"])
def _(S):
    return [
        shell(rect(11, 3, 10, 18, rr(S, 2))),
        detail(rect(14, 8, 4, 8, rr(S, 1))),
        line("M2.5 12H8.5"),
        line(poly([(6, 9.5), (8.5, 12), (6, 14.5)], r=S.r)),
    ]


@icon("unpacking-box", CAT, "Open cardboard box with an item being lifted out of it",
      tags=["unboxing", "moving", "unpack", "cardboard", "parcel", "delivery", "open box"])
def _(S):
    return [
        shell(poly([(5, 12), (19, 12), (18, 21), (6, 21)], closed=True, r=S.r)),
        line(poly([(5, 12), (2.5, 8.5)], r=0)),
        line(poly([(19, 12), (21.5, 8.5)], r=0)),
        shell(rect(9, 3, 6, 5, rr(S, 1.5))),
    ]


@icon("fire-escape-ladder", CAT, "Folding chain ladder hooked over a window sill",
      tags=["emergency", "escape", "rope ladder", "window", "safety", "fire exit", "rescue"])
def _(S):
    return [
        shell(rect(3, 3, 18, 3, 1 if S.name == "rounded" else 0)),
        line("M8 6V21"),
        line("M16 6V21"),
        line("M8 10.5H16"),
        line("M8 15H16"),
        line("M8 19.5H16"),
    ]


@icon("tubular-bulb", CAT, "Long thin tube-shaped bulb with a small screw base at one end",
      tags=["tube light", "linear bulb", "t-bulb", "lamp", "light", "led tube", "showcase lamp"])
def _(S):
    return [
        shell(rect(9, 8, 13, 8, 4 if S.name == "rounded" else 2)),
        shell(rect(2.5, 9.5, 6, 5, rr(S, 1.5))),
        detail(seg(5.5, 9.5, 5.5, 14.5)),
    ]


@icon("toggle-latch", CAT, "Lever clamp latch on a box edge with a wire loop hooked on a catch",
      tags=["clamp latch", "draw latch", "toolbox latch", "case catch", "lever", "fastener", "hardware"])
def _(S):
    return [
        shell(rect(3, 2, 18, 5, rr(S, 3))),
        shell(rect(3, 13, 18, 8, rr(S, 3))),
        shell(rect(10, 5, 4, 10, rr(S, 2))),
    ]


@icon("christmas-tree-stand", CAT, "Round bowl stand with splayed legs and screw clamps gripping a tree trunk",
      tags=["tree holder", "xmas", "holiday", "pine", "fir", "trunk", "bowl stand", "winter"])
def _(S):
    return [
        line("M10 2V11"),
        line("M14 2V11"),
        shell(poly([(4, 11), (20, 11), (18, 16), (6, 16)], closed=True, r=S.r)),
        line("M9 16L5 21.5"),
        line("M15 16L19 21.5"),
        line("M12 16V21.5"),
    ]


@icon("junk-drawer", CAT, "Open drawer seen from above, jumbled with a key, a battery and a pen",
      tags=["clutter", "kitchen drawer", "odds and ends", "storage", "mess", "organise", "catch-all"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 3))),
        detail(circle(8, 8, 2)),
        detail(seg(9.5, 9.5, 12.5, 12.5)),
        detail(rect(14.5, 6, 3.5, 6, rr(S, 1))),
        detail(seg(6.5, 17, 16, 17)),
    ]


@icon("ice-melt", CAT, "Bag of rock salt with a snowflake on the front and crystals spilling out",
      tags=["rock salt", "de-icer", "snow", "winter", "driveway", "salt bag", "thaw"])
def _(S):
    parts = [shell(poly([(4, 4.5), (16, 4.5), (16, 20.5), (4, 20.5)], closed=True, r=S.r))]
    c = (10, 12.5)
    for a in (90, 30, 150):
        x = 3.2 * math.cos(math.radians(a)); y = 3.2 * math.sin(math.radians(a))
        parts.append(detail(seg(c[0] - x, c[1] - y, c[0] + x, c[1] + y)))
    parts += [dot(19.5, 15.5, 1.25), dot(20, 19.5, 1.25), dot(19, 10.5, 1.25)]
    return parts


@icon("cedar-block", CAT, "Round cedar wood block hanging from a hook with grain lines",
      tags=["moth repellent", "closet", "hanger", "wood", "aromatic", "clothes", "cedar ring"])
def _(S):
    return [
        line("M12 9V6.5A2.5 2.5 0 1 1 14.5 4"),
        shell(circle(12, 15.5, 6.5)),
        detail(circle(12, 15.5, 2.5)),
    ]


@icon("tape-strip", CAT, "Short strip of adhesive tape with zigzag torn ends, stuck on at an angle",
      tags=["sticky tape", "adhesive", "masking tape", "scotch", "sellotape", "stick", "repair"])
def _(S):
    pts = [(5, 8), (3.5, 10), (5, 12), (3.5, 14), (5, 16), (19, 16), (20.5, 14), (19, 12), (20.5, 10), (19, 8)]
    return [
        shell(poly(rot(pts, -30), closed=True, r=S.r * 0.4), stroke_miterlimit="2"),
        detail(poly(rot([(9, 12), (15, 12)], -30))),
    ]
