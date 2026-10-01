"""TypeIcon Core: cosmetics (batch 002): beard and hair styling tools."""
import math

from geometry import P, path_to_d, rotation, transform_path
from dsl import Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401

CAT = "cosmetics"


def rpts(pts, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    return [(cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c) for x, y in pts]


def rot(d, deg, cx=12.0, cy=12.0):
    return path_to_d(transform_path(P(d), rotation(deg, cx, cy)))


@icon("beard-comb", CAT, "Small wide-tooth comb with a curved spine and long teeth, tilted as if drawn through a beard.",
      tags=["beard", "comb", "grooming", "facial hair", "barber", "beard care", "men"])
def _(S):
    sp = shell("M4 9C4 6 7 5 12 5C17 5 20 6 20 9Z" if S.name == "line" else "M4 9C4 5.5 7 4.5 12 4.5C17 4.5 20 5.5 20 9Z")
    teeth = []
    for x in (6.5, 10.5, 14.5, 18):
        (x1, y1), (x2, y2) = rpts([(x, 9), (x, 17.5)], -30)
        teeth.append(line(seg(x1, y1, x2, y2)))
    return [Part(sp.kind, rot(sp.d, -30), sp.attrs)] + teeth


@icon("beard-shaper", CAT, "Curved crescent template that follows the line of the jaw, used as a guide when shaping a beard.",
      tags=["beard", "shaping tool", "template", "stencil", "grooming", "line up", "barber"])
def _(S):
    return [
        shell("M3 5C3 13 7 20 12 20C17 20 21 13 21 5H16.5C16.5 11 14.5 15.5 12 15.5C9.5 15.5 7.5 11 7.5 5Z" if S.name == "line"
              else "M3 6C3 13 7 20 12 20C17 20 21 13 21 6Q21 5 20 5H17.5Q16.5 5 16.5 6C16.5 11 14.5 15.5 12 15.5C9.5 15.5 7.5 11 7.5 6Q7.5 5 6.5 5H4Q3 5 3 6Z"),
        dot(12, 8, 1.1),
    ]


@icon("heatless-curling-rod", CAT, "Long soft rod with hair strands wrapped around it and hanging in waves from both ends.",
      tags=["heatless curls", "curling", "satin rod", "overnight curls", "hair", "no heat", "styling"])
def _(S):
    return [
        shell(rect(2.5, 4.5, 19, 5, 2.5 if S.name == "rounded" else 1)),
        detail(seg(8, 4.5, 6.5, 9.5)), detail(seg(17.5, 4.5, 16, 9.5)),
        line("M5 9.5C3 12 7 14 5 17C4 18.5 4.5 20 5.5 21"),
        line("M19 9.5C17 12 21 14 19 17C18 18.5 18.5 20 19.5 21"),
    ]


@icon("hot-comb", CAT, "Comb with widely spaced teeth on a long handle, with heat lines above the teeth.",
      tags=["pressing comb", "heat", "straightening", "hair", "salon", "styling tool", "metal comb"])
def _(S):
    return [
        shell(rect(2, 11, 8, 4, 2 if S.name == "rounded" else 1)),
        shell(rect(10, 11, 12, 3.5, 1.5 if S.name == "rounded" else 0)),
        line(seg(12.5, 14.5, 12.5, 20.5)), line(seg(16, 14.5, 16, 20.5)), line(seg(19.5, 14.5, 19.5, 20.5)),
        line("M13 8C12 6.5 14 5.5 13 4"), line("M17 8C16 6.5 18 5.5 17 4"), line("M21 8C20 6.5 22 5.5 21 4"),
    ]


@icon("u-shaped-hairpin", CAT, "Thin wire pin bent into an open U shape with slightly wavy legs.",
      tags=["hair pin", "bobby pin", "updo", "wire pin", "hair accessory", "bun", "hair clip"])
def _(S):
    return [
        line("M8 2.5C10 5 6.5 8 8 11.5V15A4 4 0 0 0 16 15V11.5C14.5 8 18 5 16 2.5"),
    ]
