"""TypeIcon Core: kitchen (batch kitchen_005): baking stone, egg coddler, sugar tongs, asparagus steamer, fry cutter.

Objects are drawn in side view; the pizza stone uses a shallow 3/4 view so its round flat top and
thickness both read.
"""
from dsl import Part, circle, detail, dot, ellipse, icon, line, poly, rect, seg, shell, solid  # noqa: F401
from geometry import D, P, U, fmt, path_to_d

CAT = "kitchen"


def L(S, a, b):
    """Pick a value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    return S.R if cap is None else min(S.R, cap)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


# ============================================================================ icons

@icon("pizza-stone", CAT, "Round flat baking stone with a speckled top resting on a wire oven rack",
      tags=["baking stone", "pizza", "oven stone", "bread baking", "oven rack", "cordierite"])
def _(S):
    # stone: top ellipse, 2.5 px thick side, front edge of the top as a detail
    top = ellipse(12, 6.5, 9.5, 3.5)
    stone = union(top, rect(2.5, 6.5, 19, 2), ellipse(12, 8.5, 9.5, 3.5))
    out = [shell(stone), detail("M2.5 6.5A9.5 3.5 0 0 0 21.5 6.5")]
    for x, y in ((7.5, 6.7), (12, 6.2), (16.5, 6.7)):
        out.append(dot(x, y, 0.9))
    # rack in perspective: back rail, front rail, wires between
    out += [line(seg(4, 15.5, 20, 15.5)), line(seg(2, 20.5, 22, 20.5))]
    for xb, xf in ((6, 4.5), (10, 9.5), (14, 14.5), (18, 19.5)):
        out.append(line(seg(xb, 15.5, xf, 20.5)))
    return out


@icon("egg-coddler", CAT, "Small rounded porcelain egg coddler cup with a screw-on metal lid and a wire ring on top",
      tags=["coddled egg", "egg cup", "egg cooker", "porcelain", "breakfast", "poached egg"])
def _(S):
    cup = "M6.5 11.5H17.5V14A5.5 7 0 0 1 6.5 14Z"
    lid = rect(5, 8, 14, 3.5, rr(S, 1))
    ring = "M9.5 8V6.5A2.5 2.5 0 0 1 14.5 6.5V8" if S.name == "rounded" else "M9.5 8V4H14.5V8"
    return [shell(union(cup, lid)), detail(seg(5, 11.5, 19, 11.5)), line(ring)]


def _cat(*ds):
    """Join open d-strings into one path (later pieces continue from the previous end point)."""
    out = ds[0]
    for d in ds[1:]:
        out += "L" + d[1:] if d.startswith("M") else d
    return out


@icon("sugar-tongs", CAT, "Small U-shaped sugar tongs with claw tips holding a sugar cube",
      tags=["sugar cube", "tongs", "tea service", "sugar nips", "tableware", "afternoon tea"])
def _(S):
    left = [(8.5, 21.5), (8.5, 18.5), (4.5, 15), (9.5, 7), (9.5, 5.5)]
    right = [(24 - x, y) for x, y in reversed(left)]
    tongs = _cat(poly(left, r=S.r), "A2.5 2.5 0 0 1 14.5 5.5", poly(right, r=S.r))
    return [line(tongs), solid(rect(10, 17.5, 4, 4, L(S, 0, 1)))]


def _spear(S, x, y):
    """Asparagus spear tip: pointed bud with its top at (x, y)."""
    if S.name == "line":
        return poly([(x, y), (x + 1.5, y + 2.5), (x + 1.5, y + 4.5), (x - 1.5, y + 4.5), (x - 1.5, y + 2.5)], closed=True)
    return (f"M{fmt(x)} {fmt(y)}C{fmt(x + 1.3)} {fmt(y + 1)} {fmt(x + 1.5)} {fmt(y + 2.5)} {fmt(x + 1.5)} {fmt(y + 3.7)}"
            f"A1.5 0.8 0 0 1 {fmt(x - 1.5)} {fmt(y + 3.7)}C{fmt(x - 1.5)} {fmt(y + 2.5)} {fmt(x - 1.3)} {fmt(y + 1)} {fmt(x)} {fmt(y)}Z")


@icon("asparagus-steamer", CAT, "Tall narrow pot with a raised inner basket of upright asparagus spears",
      tags=["asparagus pot", "steamer", "tall pot", "vegetable steamer", "cookware", "asparagus"])
def _(S):
    pot = union(rect(7, 12.5, 10, 9, rr(S, 2)), rect(5.5, 12.5, 13, 2.5, rr(S, 1)),
                rect(8.5, 10, 7, 3, L(S, 0, 1)))
    out = [shell(pot), detail(seg(7, 15, 17, 15))]
    for x, y in ((9.75, 2), (14.25, 3)):
        out.append(solid(_spear(S, x, y)))
        out.append(line(seg(x, y + 4, x, 10)))
    return out


@icon("fry-cutter", CAT, "Plunger with a T-handle pressing a potato down onto a square cutting grid",
      tags=["french fry cutter", "chip cutter", "potato cutter", "fries", "chips", "potato slicer"])
def _(S):
    return [line(seg(8, 2.5, 16, 2.5)), line(seg(12, 2.5, 12, 6)),
            shell(ellipse(12, 8.5, 6, 2.5)),
            shell(rect(3.5, 14, 17, 7.5, rr(S, 2))),
            detail(seg(9.2, 14, 9.2, 21.5)), detail(seg(14.8, 14, 14.8, 21.5)),
            detail(seg(3.5, 17.75, 20.5, 17.75))]
