"""TypeIcon Core: furniture (batch furniture_001).

Original drawings of chairs, sofas, tables, desks and beds, in front, side or top view.
Simple silhouettes (shells) carry the mass; legs, frames and rockers are open strokes.
"""
import math

from dsl import D, P, ST, U, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from geometry import fmt, path_to_d, polar, rotation, transform_path  # noqa: F401

CAT = "furniture"


# --------------------------------------------------------------------------- local helpers

def L(S, a, b):
    """Value for Line (a) or Rounded (b)."""
    return a if S.name == "line" else b


def rr(S, cap=None):
    """Container corner radius for the style, optionally capped for small shapes."""
    if cap is None:
        return S.R
    return min(S.R, cap) if S.name == "rounded" else min(S.R, cap) * 0.4


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def mark(d) -> Part:
    return Part("dot", d)


def union(*ds):
    return path_to_d(U(*[P(d) for d in ds]))


def minus(a, *bs):
    return path_to_d(D(P(a), *[P(b) for b in bs]))


def flip(d):
    """Mirror a d-string across the vertical centre line."""
    return path_to_d(transform_path(P(d), (-1, 0, 0, 1, 24, 0)))


def top_round(x, y, w, h, rt, rb=0.0):
    """Rectangle with top corners of radius rt and bottom corners of radius rb."""
    return (f"M{fmt(x)} {fmt(y + h - rb)}V{fmt(y + rt)}A{fmt(rt)} {fmt(rt)} 0 0 1 {fmt(x + rt)} {fmt(y)}"
            f"H{fmt(x + w - rt)}A{fmt(rt)} {fmt(rt)} 0 0 1 {fmt(x + w)} {fmt(y + rt)}V{fmt(y + h - rb)}"
            + (f"A{fmt(rb)} {fmt(rb)} 0 0 1 {fmt(x + w - rb)} {fmt(y + h)}" if rb else "")
            + f"H{fmt(x + rb)}"
            + (f"A{fmt(rb)} {fmt(rb)} 0 0 1 {fmt(x)} {fmt(y + h - rb)}" if rb else "") + "Z")


def star_base(S, y0=18.5, y1=21):
    """Five-star swivel base seen from the front: a column foot splaying to two casters and a centre one."""
    return [line(poly([(4.5, y1), (12, y0), (19.5, y1)], r=S.r)), line(seg(12, y0, 12, y1))]


# ============================================================================ chairs

@icon("rocking-chair", CAT, "Rocking chair seen from the side on two curved rockers",
      tags=["rocker", "chair", "porch", "nursery", "relax", "furniture"], aliases=["rocker"])
def _(S):
    return [
        line(poly([(5.5, 2.5), (8, 13), (18.5, 13)], r=S.r)),
        line(poly([(6.8, 8.5), (16, 8.5), (16, 19)], r=S.r)),
        line(seg(9, 13, 9, 19.6)),
        line("M2.5 16Q12 24 21.5 16"),
    ]


@icon("office-chair", CAT, "Swivel office chair with a padded back and a five-star base",
      tags=["desk chair", "swivel chair", "office", "work", "seat", "furniture"], aliases=["desk-chair", "swivel-chair"])
def _(S):
    return [
        shell(rect(6.5, 2.5, 11, 8, rr(S, 3))),
        line(seg(12, 10.5, 12, 12.5)),
        shell(rect(4.5, 12.5, 15, 3.5, rr(S, 1.75))),
        line(seg(12, 16, 12, 18.5)),
        *star_base(S),
    ]


@icon("gaming-chair", CAT, "Racing-style gaming chair with a tall winged back and headrest",
      tags=["gamer chair", "racing chair", "gaming", "esports", "desk chair", "furniture"], aliases=["racing-chair"])
def _(S):
    body = [(8.5, 2.5), (15.5, 2.5), (15.5, 5), (18.5, 5.5), (17, 12.5), (19.5, 12.5), (19.5, 15.5),
            (4.5, 15.5), (4.5, 12.5), (7, 12.5), (5.5, 5.5), (8.5, 5)]
    return [
        shell(poly(body, closed=True, r=S.r * 0.5)),
        detail(seg(10, 7.5, 10, 12.5)), detail(seg(14, 7.5, 14, 12.5)),
        line(seg(12, 15.5, 12, 18.5)),
        *star_base(S),
    ]


@icon("folding-chair", CAT, "Folding chair seen from the side with crossed legs",
      tags=["fold up chair", "camping chair", "event seating", "portable", "chair", "furniture"])
def _(S):
    return [
        shell(poly([(5.5, 2.5), (10, 2.5), (11, 7), (6.5, 7)], closed=True, r=S.r * 0.5)),
        line(seg(8.75, 7, 16.5, 21)),
        line(seg(6, 21, 14, 12)),
        line(seg(5, 12, 19, 12) if S.name == "line" else seg(5.5, 12, 18.5, 12)),
    ]


@icon("deck-chair", CAT, "Folding deck chair with a sagging fabric sling",
      tags=["beach chair", "deckchair", "lawn chair", "beach", "summer", "furniture"], aliases=["beach-chair"])
def _(S):
    return [
        line(seg(5, 3, 15.5, 21)),
        line(seg(6, 21, 11, 14)),
        line(seg(19.5, 12, 19.5, 21)),
        shell("M5 3Q7.5 18 19.5 11Q10 13 5 3Z", stroke_miterlimit="2"),
    ]


@icon("director-chair", CAT, "Director's chair with a canvas back band and crossed legs",
      tags=["directors chair", "film set", "movie", "canvas chair", "folding chair", "furniture"])
def _(S):
    return [
        shell(rect(4.5, 3, 15, 4.5, rr(S, 1.5))),
        line(seg(6, 7.5, 6, 12)), line(seg(18, 7.5, 18, 12)),
        shell(rect(4.5, 12, 15, 3, rr(S, 1.5))),
        line(seg(6.5, 15, 17.5, 21)), line(seg(17.5, 15, 6.5, 21)),
    ]


@icon("wingback-chair", CAT, "Wingback armchair with a tall back and flared wings",
      tags=["wing chair", "armchair", "fireside chair", "living room", "chair", "furniture"], aliases=["wing-chair"])
def _(S):
    r = L(S, 0, 2)
    half = (f"M12 17H{20.5 - r}" + (f"A{r} {r} 0 0 0 20.5 {17 - r}" if r else "") +
            "V11.5C20.5 10.5 19.5 10 18.5 10C18.5 8 21 7 21 4.5C21 3 19.5 2.5 18 2.5H12")
    body = union(half + "Z", flip(half + "Z"))
    return [
        shell(body),
        detail(seg(7.5, 12, 7.5, 17)), detail(seg(16.5, 12, 16.5, 17)),
        detail(seg(7.5, 14.25, 16.5, 14.25)),
        line(seg(5.5, 17, 5.5, 21)), line(seg(18.5, 17, 18.5, 21)),
    ]


@icon("recliner", CAT, "Recliner seen from the side with the back tilted and the footrest raised",
      tags=["reclining chair", "lounger", "armchair", "relax", "tv chair", "furniture"], aliases=["reclining-chair"])
def _(S):
    body = [(2.5, 5), (6, 3.5), (10.5, 11), (16, 11), (20, 7.5), (21.5, 10), (17, 15), (17, 18), (6.5, 18), (6.5, 14)]
    return [
        shell(poly(body, closed=True, r=S.r * 0.6)),
        detail(seg(10.5, 14.5, 17, 14.5)),
        line(seg(8.5, 18, 8.5, 21)), line(seg(15, 18, 15, 21)),
    ]


@icon("chaise-longue", CAT, "Chaise longue with one raised scrolled end and a long seat",
      tags=["chaise lounge", "daybed", "fainting couch", "lounge", "sofa", "furniture"], aliases=["chaise-lounge"])
def _(S):
    body = union(top_round(3, 4, 6, 13, 3, 0), rect(3, 12, 18, 5, rr(S, 1.5)))
    return [
        shell(body),
        detail("M9 8A2 2 0 1 0 6 9.75"),
        line(seg(5, 17, 5, 20.5)), line(seg(19, 17, 19, 20.5)),
    ]


@icon("bean-bag", CAT, "Slouched bean bag chair with a dent in the seat",
      tags=["beanbag", "bean bag chair", "lounge", "kids room", "soft seat", "furniture"], aliases=["beanbag"])
def _(S):
    t = L(S, 0.0, 1.2)
    body = (f"M8.5 {3 + t * 0.5}C{5 - t} 3 3 12 3 16.5C3 20 6 21 12 21C18 21 21 20 21 16.5"
            f"C21 12.5 17 10.5 13.5 12C12.5 7 {11 + t} 3 8.5 {3 + t * 0.5}Z")
    return [
        shell(body),
        detail("M7 14.5Q11.5 18 16.5 13.5"),
    ]


@icon("papasan-chair", CAT, "Papasan chair: a wide round bowl seat on a short base",
      tags=["papasan", "bowl chair", "wicker chair", "rattan", "boho", "furniture"], aliases=["papasan"])
def _(S):
    return [
        line("M4 9Q12 3.5 20 9"),
        shell("M2.5 9H21.5A9.5 5.5 0 0 1 2.5 9Z"),
        shell(poly([(8.5, 18), (15.5, 18), (16.5, 21), (7.5, 21)], closed=True, r=S.r * 0.5)),
    ]


@icon("hanging-chair", CAT, "Egg-shaped hanging chair with an open front, hung from a hook",
      tags=["egg chair", "swing chair", "hanging egg chair", "pod chair", "rattan", "furniture"], aliases=["egg-chair"])
def _(S):
    return [
        line(seg(12, 2, 12, 5.5)),
        shell(ellipse(12, 13.5, 7, 8)),
        detail("M8 16.5A4 5 0 0 1 16 16.5Z" if S.name == "line" else poly([(8, 16.5), (8, 14), (10, 11.25), (14, 11.25), (16, 14), (16, 16.5)], closed=True, r=1.5)),
    ]


@icon("windsor-chair", CAT, "Windsor chair with a curved top rail over thin spindles",
      tags=["spindle chair", "wooden chair", "dining chair", "farmhouse", "chair", "furniture"])
def _(S):
    a, b = polar(12, 13, 9, 243), polar(12, 13, 9, 297)
    return [
        line(arc(12, 13, 9, 218, 322)),
        line(seg(8, 13, a[0], a[1])), line(seg(12, 13, 12, 4)), line(seg(16, 13, b[0], b[1])),
        line(seg(3, 13, 21, 13) if S.name == "line" else seg(3.5, 13, 20.5, 13)),
        line(seg(5.5, 13, 4.5, 21)), line(seg(18.5, 13, 19.5, 21)),
    ]


@icon("ladder-back-chair", CAT, "Ladder-back chair with three horizontal back slats",
      tags=["ladderback", "slat back chair", "wooden chair", "country chair", "chair", "furniture"], aliases=["ladderback-chair"])
def _(S):
    return [
        line(seg(7, 2.5, 7, 14)), line(seg(17, 2.5, 17, 14)),
        line(seg(7, 4.5, 17, 4.5)), line(seg(7, 8, 17, 8)), line(seg(7, 11.5, 17, 11.5)),
        shell(rect(3.5, 14, 17, 3, rr(S, 1.5))),
        line(seg(5, 17, 5, 21)), line(seg(19, 17, 19, 21)),
    ]


@icon("cross-back-chair", CAT, "Dining chair with a large X across the back frame",
      tags=["x back chair", "bistro chair", "dining chair", "farmhouse", "chair", "furniture"], aliases=["x-back-chair"])
def _(S):
    return [
        shell(rect(6, 3, 12, 9.5, rr(S, 1.5))),
        detail(seg(6, 3, 18, 12.5)), detail(seg(18, 3, 6, 12.5)),
        line(seg(7, 12.5, 7, 21)), line(seg(17, 12.5, 17, 21)),
        line(seg(4, 15.5, 20, 15.5)),
    ]


@icon("bentwood-chair", CAT, "Bentwood cafe chair with a looped back, round seat and a leg ring",
      tags=["cafe chair", "bistro chair", "bent wood", "vienna chair", "chair", "furniture"])
def _(S):
    return [
        line("M7.5 12.5V7.5A4.5 4.5 0 0 1 16.5 7.5V12.5"),
        line("M10.25 12.5V9A1.75 1.75 0 0 1 13.75 9V12.5"),
        shell(rect(4.5, 12.5, 15, 2.5, 1.25)),
        line("M6.5 15C6.5 17.5 6 19.5 5 21"), line("M17.5 15C17.5 17.5 18 19.5 19 21"),
        line("M5.5 18.5Q12 20.5 18.5 18.5" if S.name == "line" else "M6 18.25Q12 20.25 18 18.25"),
    ]


@icon("cantilever-chair", CAT, "Cantilever chair made from one bent tube with no back legs",
      tags=["tubular chair", "bauhaus chair", "steel chair", "modern chair", "chair", "furniture"])
def _(S):
    return [
        line(poly([(6.5, 2.5), (7.5, 12.5), (16.5, 12.5), (17.5, 21), (5, 21)], r=L(S, 2, 3.5))),
        shell(rect(9, 9, 7, 2.5, 1.25) if S.name == "rounded" else rect(9, 9, 7, 2.5)),
    ]


@icon("adirondack-chair", CAT, "Adirondack chair with a fan of back slats and wide flat arms",
      tags=["muskoka chair", "garden chair", "lawn chair", "patio", "outdoor", "furniture"], aliases=["muskoka-chair"])
def _(S):
    l, r_ = polar(12, 11, 8.5, 205), polar(12, 11, 8.5, 335)
    back = f"M8 13L{fmt(l[0])} {fmt(l[1])}A8.5 8.5 0 0 1 {fmt(r_[0])} {fmt(r_[1])}L16 13Z"
    return [
        shell(back),
        detail(seg(10.6, 13, 9.4, 3.2)), detail(seg(13.4, 13, 14.6, 3.2)),
        shell(rect(2.5, 11, 4, 2.5, rr(S, 1.25))), shell(rect(17.5, 11, 4, 2.5, rr(S, 1.25))),
        line(seg(4.5, 13.5, 4.5, 21)), line(seg(19.5, 13.5, 19.5, 21)),
        line(seg(8, 16.5, 16, 16.5)),
    ]


@icon("butterfly-chair", CAT, "Butterfly chair: a triangular sling on a thin crossing frame",
      tags=["sling chair", "bkf chair", "canvas sling", "mid century", "chair", "furniture"], aliases=["sling-chair"])
def _(S):
    return [
        shell(poly([(3, 3.5), (12, 8), (21, 3.5), (15.5, 15), (8.5, 15)], closed=True, r=S.r * 0.6)),
        line(seg(8.5, 15, 4.5, 21)), line(seg(15.5, 15, 19.5, 21)),
        line(seg(7, 21, 12, 15.5) if S.name == "line" else seg(7.5, 20.5, 12, 15.5)),
        line(seg(17, 21, 12, 15.5) if S.name == "line" else seg(16.5, 20.5, 12, 15.5)),
    ]


@icon("peacock-chair", CAT, "Peacock chair with a huge fan-shaped wicker back",
      tags=["wicker chair", "rattan chair", "fan chair", "boho", "statement chair", "furniture"])
def _(S):
    a, b = polar(12, 11, 9, 200), polar(12, 11, 9, 340)
    fan = f"M10 14L{fmt(a[0])} {fmt(a[1])}A9 9 0 0 1 {fmt(b[0])} {fmt(b[1])}L14 14Z"
    skirt = poly([(7, 13.5), (17, 13.5), (13.5, 17.5), (17, 21), (7, 21), (10.5, 17.5)], closed=True, r=S.r * 0.6)
    rays = [seg(*polar(12, 12, 4.5, g), *polar(12, 12, 8, g)) for g in (228, 270, 312)]
    return [shell(union(fan, skirt)), *[detail(d) for d in rays]]


@icon("tub-chair", CAT, "Low barrel-shaped tub chair whose back and arms form one curve",
      tags=["barrel chair", "club chair", "armchair", "lounge chair", "chair", "furniture"], aliases=["barrel-chair"])
def _(S):
    r = L(S, 0, 2)
    body = (f"M3 {17 - r}V11C3 6 7 4 12 4C17 4 21 6 21 11V{17 - r}"
            + (f"A{r} {r} 0 0 1 {21 - r} 17" if r else "") + f"H{3 + r}"
            + (f"A{r} {r} 0 0 1 3 {17 - r}" if r else "") + "Z")
    return [
        shell(body),
        detail("M7 17V12C7 10 9 8.5 12 8.5C15 8.5 17 10 17 12V17"),
        line(seg(6, 17, 6, 20)), line(seg(18, 17, 18, 20)),
    ]


@icon("monobloc-chair", CAT, "One-piece plastic garden chair with a slotted back and molded arms",
      tags=["plastic chair", "garden chair", "patio chair", "resin chair", "stackable", "furniture"], aliases=["plastic-chair"])
def _(S):
    return [
        shell(top_round(6.5, 2.5, 11, 9, L(S, 3, 4.5), rr(S, 1.5))),
        detail(seg(9, 5.5, 15, 5.5)), detail(seg(9, 8.5, 15, 8.5)),
        line(poly([(6.5, 9.5), (3.5, 11), (3.5, 21)], r=S.r)), line(poly([(17.5, 9.5), (20.5, 11), (20.5, 21)], r=S.r)),
        line(seg(3.5, 14.5, 20.5, 14.5)),
        line(seg(8, 14.5, 7.5, 21)), line(seg(16, 14.5, 16.5, 21)),
    ]


def _tilted_pad(cx, cy, w, h, deg, rx):
    return path_to_d(transform_path(P(rect(cx - w / 2, cy - h / 2, w, h, rx)), rotation(deg, cx, cy)))


@icon("kneeling-chair", CAT, "Ergonomic kneeling chair with a slanted seat and a lower knee pad",
      tags=["kneeling stool", "ergonomic chair", "posture", "office", "back pain", "furniture"], aliases=["kneeling-stool"])
def _(S):
    return [
        shell(_tilted_pad(8, 7, 9, 3, 18, rr(S, 1.5))),
        shell(_tilted_pad(17, 14.5, 7, 3, 28, rr(S, 1.5))),
        line(poly([(8.5, 9.5), (11.5, 19), (15, 16.5)], r=S.r)),
        line(seg(3.5, 21, 20.5, 21) if S.name == "line" else seg(4, 21, 20, 21)),
        line(seg(11.5, 19, 11.5, 21)),
    ]


@icon("high-chair", CAT, "Baby high chair on tall splayed legs with a tray",
      tags=["highchair", "baby chair", "feeding chair", "toddler", "baby", "furniture"], aliases=["highchair"])
def _(S):
    return [
        shell(rect(7.5, 2.5, 9, 5.5, rr(S, 2))),
        shell(rect(4, 10, 16, 2.5, rr(S, 1.25))),
        line(seg(8, 12.5, 5, 21)), line(seg(16, 12.5, 19, 21)),
        line(seg(6.5, 17, 17.5, 17)),
    ]


@icon("throne", CAT, "Royal throne with a tall pointed back and arms on a step",
      tags=["king", "queen", "royal", "monarch", "power", "furniture"])
def _(S):
    back = "M7.5 13V8Q7.5 4.5 12 2Q16.5 4.5 16.5 8V13Z"
    arms = rect(3.5, 12, 17, 6, rr(S, 2))
    return [
        shell(union(back, arms)),
        dot(3.5, 9.5, 1.5), dot(20.5, 9.5, 1.5),
        mark(poly([(12, 5.5), (13.5, 7.5), (12, 9.5), (10.5, 7.5)], closed=True)),
        detail(seg(7.5, 15, 16.5, 15)),
        line(seg(2.5, 21, 21.5, 21) if S.name == "line" else seg(3, 21, 21, 21)),
    ]


@icon("floor-chair", CAT, "Legless floor chair with a cushion seat and an upright backrest",
      tags=["floor seat", "meditation chair", "gaming floor chair", "tatami chair", "legless chair", "furniture"])
def _(S):
    return [
        shell(poly([(3.5, 4.5), (7.5, 4), (9, 13.5), (20.5, 13.5), (20.5, 18), (3.5, 18)], closed=True, r=S.r)),
        detail(seg(9, 13.5, 9, 18)),
        line(seg(2.5, 21, 21.5, 21) if S.name == "line" else seg(3, 21, 21, 21)),
    ]


@icon("piano-bench", CAT, "Padded piano bench beside the keyboard of an upright piano",
      tags=["piano stool", "keyboard bench", "music", "piano", "bench", "furniture"], aliases=["piano-stool"])
def _(S):
    piano = [(16, 2.5), (21, 2.5), (21, 21), (16, 21), (16, 11.5), (13, 11.5), (13, 9), (16, 9)]
    return [
        shell(poly(piano, closed=True, r=S.r * 0.6)),
        shell(rect(2.5, 13.5, 9, 3, rr(S, 1.5))),
        line(seg(4, 16.5, 4.5, 21)), line(seg(10, 16.5, 9.5, 21)),
    ]


@icon("church-pew", CAT, "Long wooden church pew with a high back between two end panels",
      tags=["pew", "church bench", "chapel", "worship", "bench", "furniture"], aliases=["pew"])
def _(S):
    ends = [top_round(2.5, 3.5, 4, 17.5, 2), top_round(17.5, 3.5, 4, 17.5, 2)]
    back = rect(5.5, 6.5, 13, 6)
    return [
        shell(union(*ends, back)),
        line(seg(6.5, 16, 17.5, 16)),
    ]


# ============================================================================ sofas, benches and soft seating

@icon("window-seat", CAT, "Cushioned bench built into a window recess",
      tags=["window bench", "reading nook", "bay window", "built in seat", "nook", "furniture"], aliases=["window-bench"])
def _(S):
    return [
        line(seg(3, 2.5, 3, 14)), line(seg(21, 2.5, 21, 14)),
        shell(rect(7, 2.5, 10, 8.5, rr(S, 1.5))),
        detail(seg(12, 2.5, 12, 11)), detail(seg(7, 6.75, 17, 6.75)),
        shell(rect(2.5, 14, 19, 7, rr(S, 2))),
        detail(seg(2.5, 17, 21.5, 17)),
    ]


@icon("loveseat", CAT, "Compact two-seat sofa with rolled arms and two back cushions",
      tags=["love seat", "two seater", "small sofa", "settee", "couch", "furniture"], aliases=["two-seater"])
def _(S):
    body = union(top_round(3.5, 9, 4.5, 8, 2.25, L(S, 0, 1)), top_round(16, 9, 4.5, 8, 2.25, L(S, 0, 1)),
                 top_round(6, 5, 12, 12, rr(S, 2.5)))
    return [
        shell(body),
        detail(seg(8, 11, 8, 17)), detail(seg(16, 11, 16, 17)),
        detail(seg(8, 13.5, 16, 13.5)), detail(seg(12, 5, 12, 13.5)),
        line(seg(5.5, 17, 5.5, 20)), line(seg(18.5, 17, 18.5, 20)),
    ]


@icon("chesterfield-sofa", CAT, "Chesterfield sofa with a button-tufted back and high rolled arms",
      tags=["chesterfield", "tufted sofa", "leather sofa", "couch", "classic", "furniture"], aliases=["chesterfield"])
def _(S):
    body = union(rect(4, 6, 16, 11, rr(S, 1.5)), circle(4.75, 7.25, 2.25), circle(19.25, 7.25, 2.25),
                 rect(2.5, 7.25, 4.5, 9.75, L(S, 0, 1.5)), rect(17, 7.25, 4.5, 9.75, L(S, 0, 1.5)))
    return [
        shell(body),
        dot(9.5, 8.5, 1), dot(14.5, 8.5, 1), dot(12, 10.75, 1),
        detail(seg(7, 10, 7, 17)), detail(seg(17, 10, 17, 17)), detail(seg(7, 13.75, 17, 13.75)),
        line(seg(4.5, 17, 4.5, 20)), line(seg(19.5, 17, 19.5, 20)),
    ]


@icon("sectional-sofa", CAT, "L-shaped corner sectional sofa seen from above",
      tags=["sectional", "corner sofa", "l shaped sofa", "modular sofa", "couch", "furniture"], aliases=["corner-sofa"])
def _(S):
    return [
        shell(poly([(3, 4), (21, 4), (21, 20), (14, 20), (14, 12.5), (3, 12.5)], closed=True, r=S.r)),
        detail(poly([(5.5, 12.5), (5.5, 7.5), (17.5, 7.5), (17.5, 20)], r=S.r)),
        detail(seg(11, 7.5, 11, 12.5)), detail(seg(14, 14.5, 17.5, 14.5)),
    ]


@icon("camelback-sofa", CAT, "Camelback sofa whose back rises in a single hump",
      tags=["camel back sofa", "hump back", "traditional sofa", "couch", "settee", "furniture"], aliases=["camel-back-sofa"])
def _(S):
    back = "M4.5 17V9.5C9 9.5 8.5 3.5 12 3.5C15.5 3.5 15 9.5 19.5 9.5V17Z"
    body = union(back, top_round(2.5, 10.5, 4.5, 6.5, 2.25, L(S, 0, 1)), top_round(17, 10.5, 4.5, 6.5, 2.25, L(S, 0, 1)))
    return [
        shell(body),
        detail(seg(7, 12.5, 7, 17)), detail(seg(17, 12.5, 17, 17)), detail(seg(7, 14.5, 17, 14.5)),
        line(seg(4.5, 17, 4.5, 20)), line(seg(19.5, 17, 19.5, 20)),
    ]


@icon("curved-sofa", CAT, "Curved crescent sofa seen from above with a low back",
      tags=["crescent sofa", "round sofa", "curved couch", "lounge", "modern sofa", "furniture"], aliases=["crescent-sofa"])
def _(S):
    c, ro, ri = (12, 20), 10, 4
    a0, a1 = 195, 345
    p0, p1 = polar(*c, ro, a0), polar(*c, ro, a1)
    q1, q0 = polar(*c, ri, a1), polar(*c, ri, a0)
    body = (f"M{fmt(p0[0])} {fmt(p0[1])}A{ro} {ro} 0 0 1 {fmt(p1[0])} {fmt(p1[1])}"
            f"L{fmt(q1[0])} {fmt(q1[1])}A{ri} {ri} 0 0 0 {fmt(q0[0])} {fmt(q0[1])}Z")
    return [
        shell(body, stroke_miterlimit="2"),
        detail(arc(*c, 7, a0 + 4, a1 - 4)),
    ]


@icon("sofa-bed", CAT, "Sofa with its seat pulled out into a flat mattress and pillow",
      tags=["sleeper sofa", "pull out bed", "futon", "guest bed", "convertible sofa", "furniture"], aliases=["sleeper-sofa"])
def _(S):
    sofa = [(3, 12), (3, 6.5), (6, 6.5), (6, 3.5), (18, 3.5), (18, 6.5), (21, 6.5), (21, 12)]
    return [
        shell(poly(sofa, closed=True, r=S.r * 0.6)),
        detail(seg(6, 6.5, 6, 12)), detail(seg(18, 6.5, 18, 12)),
        shell(poly([(5, 14.5), (19, 14.5), (21.5, 20.5), (2.5, 20.5)], closed=True, r=S.r * 0.6)),
        mark(rect(7, 16.25, 5, 2.5, L(S, 0.5, 1.25))),
    ]


@icon("daybed", CAT, "Daybed framed on three sides with a mattress and bolster",
      tags=["day bed", "guest bed", "lounge bed", "trundle", "sofa bed", "furniture"], aliases=["day-bed"])
def _(S):
    return [
        line(poly([(3, 12.5), (3, 4), (21, 4), (21, 12.5)], r=S.r)),
        line(seg(3, 8, 21, 8)),
        shell(rect(2.5, 12.5, 19, 4.5, rr(S, 1.5))),
        dot(6.5, 14.75, 1.25),
        line(seg(3.5, 17, 3.5, 21)), line(seg(20.5, 17, 20.5, 21)),
    ]


@icon("ottoman", CAT, "Upholstered square ottoman footstool with a button-tufted top",
      tags=["footstool", "footrest", "pouffe", "hassock", "stool", "furniture"], aliases=["footstool", "hassock"])
def _(S):
    return [
        shell(rect(3, 6.5, 18, 11, rr(S, 2))),
        detail(seg(3, 10.5, 21, 10.5)),
        dot(8, 14, 1), dot(12, 14, 1), dot(16, 14, 1),
        line(seg(5.5, 17.5, 5.5, 20.5)), line(seg(18.5, 17.5, 18.5, 20.5)),
    ]


@icon("pouf", CAT, "Round pouf floor cushion shaped like a squat drum",
      tags=["pouffe", "floor pouf", "footstool", "moroccan pouf", "cushion", "furniture"], aliases=["pouffe"])
def _(S):
    b = L(S, 0, 1)
    body = f"M3 8.5C3 4.5 21 4.5 21 8.5C{21 + b} 11 {21 + b} 13 21 15.5C21 19.5 3 19.5 3 15.5C{3 - b} 13 {3 - b} 11 3 8.5Z"
    return [
        shell(body),
        detail("M3 8.5C3 11.5 21 11.5 21 8.5"),
        detail("M3.3 13C4 16 20 16 20.7 13"),
    ]


@icon("porch-swing", CAT, "Porch swing bench with a slatted back hanging from chains on a beam",
      tags=["swing bench", "porch", "veranda", "garden swing", "outdoor", "furniture"], aliases=["swing-bench"])
def _(S):
    return [
        line(seg(2.5, 3, 21.5, 3) if S.name == "line" else seg(3, 3, 21, 3)),
        *[(dot(x, y, 1) if S.name == "rounded" else sq(x - 0.9, y - 0.9, 1.8, 1.8)) for x in (4, 20) for y in (6, 9, 12)],
        shell(rect(7, 6.5, 10, 5, rr(S, 1.5))),
        detail(seg(10.33, 6.5, 10.33, 11.5)), detail(seg(13.67, 6.5, 13.67, 11.5)),
        shell(rect(2.5, 13.5, 19, 3, rr(S, 1.5))),
    ]


@icon("sun-lounger", CAT, "Sun lounger with a raised backrest and slatted bed on legs",
      tags=["lounger", "sunbed", "pool lounger", "beach", "chaise", "furniture"], aliases=["sunbed", "pool-lounger"])
def _(S):
    return [
        shell(poly([(2.5, 6), (5, 5), (9, 12.5), (21.5, 12.5), (21.5, 15.5), (7.5, 15.5)], closed=True, r=S.r * 0.5)),
        detail(seg(12.5, 12.5, 12.5, 15.5)), detail(seg(16, 12.5, 16, 15.5)),
        line(seg(9, 15.5, 9, 20)), line(seg(20, 15.5, 20, 20)),
    ]


@icon("bistro-set", CAT, "Bistro set: a small round cafe table between two chairs",
      tags=["cafe table", "patio set", "bistro table", "outdoor dining", "balcony", "furniture"], aliases=["cafe-set"])
def _(S):
    chair = line(poly([(5, 3.5), (3, 6), (3, 21)], r=S.r))
    seatl = line(poly([(3, 13), (6.5, 13), (6.5, 21)], r=S.r))
    return [
        chair, seatl,
        line(flip(poly([(5, 3.5), (3, 6), (3, 21)], r=S.r))), line(flip(poly([(3, 13), (6.5, 13), (6.5, 21)], r=S.r))),
        shell(ellipse(12, 10.5, 3.5, 1.5) if S.name == "rounded" else rect(8.5, 9, 7, 3)),
        line(seg(12, 12, 12, 21)),
        line(seg(9.5, 21, 14.5, 21)),
    ]


@icon("tree-swing", CAT, "Plank swing hanging from two ropes tied to a tree branch",
      tags=["rope swing", "swing", "garden", "backyard", "playground", "childhood"], aliases=["rope-swing"])
def _(S):
    return [
        shell(circle(6.5, 6.5, 4)),
        line(seg(6.5, 10.5, 6.5, 21)),
        line(poly([(6.5, 14), (11, 10), (21.5, 9)], r=S.r)),
        line(seg(12.5, 10, 12.5, 17)), line(seg(19.5, 9.2, 19.5, 17)),
        shell(rect(10.5, 17, 11, 2.5, rr(S, 1.25))),
    ]


# ============================================================================ tables and desks

@icon("coffee-table", CAT, "Long low coffee table with a lower shelf holding a book",
      tags=["cocktail table", "living room table", "low table", "center table", "table", "furniture"], aliases=["cocktail-table"])
def _(S):
    return [
        shell(rect(2.5, 7.5, 19, 3, rr(S, 1.5))),
        line(seg(4.5, 10.5, 4.5, 20)), line(seg(19.5, 10.5, 19.5, 20)),
        line(seg(4.5, 17, 19.5, 17)),
        mark(rect(8, 13, 7, 3, L(S, 0, 1))),
    ]


@icon("console-table", CAT, "Narrow console table with a lower shelf and a lamp on top",
      tags=["hall table", "entryway table", "sofa table", "foyer", "table", "furniture"], aliases=["hall-table"])
def _(S):
    return [
        shell(poly([(13, 3), (18, 3), (19.5, 7.5), (11.5, 7.5)], closed=True, r=S.r * 0.5)),
        line(seg(15.5, 7.5, 15.5, 11)),
        line(seg(2.5, 12, 21.5, 12) if S.name == "line" else seg(3, 12, 21, 12)),
        line(seg(4.5, 12, 4.5, 21)), line(seg(19.5, 12, 19.5, 21)),
        line(seg(4.5, 17, 19.5, 17)),
        shell(rect(6, 7.5, 3, 4.5, L(S, 0.5, 1.5))),
    ]


@icon("nesting-tables", CAT, "Two nesting side tables, the smaller tucked under the larger",
      tags=["nest of tables", "side tables", "stacking tables", "occasional tables", "table", "furniture"], aliases=["nest-of-tables"])
def _(S):
    return [
        shell(rect(2.5, 5, 14, 2.5, rr(S, 1.25))),
        line(seg(4, 7.5, 4, 21)), line(seg(15, 7.5, 15, 10.5)),
        shell(rect(9, 11.5, 12.5, 2.5, rr(S, 1.25))),
        line(seg(11, 14, 11, 21)), line(seg(19.5, 14, 19.5, 21)),
    ]


@icon("drop-leaf-table", CAT, "Drop-leaf table with one hinged leaf hanging down at the side",
      tags=["gateleg table", "folding leaf", "space saving table", "dining table", "table", "furniture"], aliases=["gateleg-table"])
def _(S):
    return [
        shell(rect(3, 6, 13.5, 2.5, rr(S, 1.25))),
        shell(rect(17.5, 6, 2.5, 10, rr(S, 1.25))),
        line(seg(5, 8.5, 5, 21)), line(seg(14.5, 8.5, 14.5, 21)),
        line(seg(5, 15, 14.5, 15)),
    ]


@icon("pedestal-table", CAT, "Round pedestal table on a single column with a flared foot",
      tags=["round table", "tulip table", "bistro table", "dining table", "table", "furniture"], aliases=["tulip-table"])
def _(S):
    return [
        shell(rect(2.5, 5, 19, 2.5, rr(S, 1.25))),
        line(seg(12, 7.5, 12, 16.5)),
        shell(poly([(10.5, 16.5), (13.5, 16.5), (18.5, 21), (5.5, 21)], closed=True, r=S.r * 0.6)),
    ]


@icon("trestle-table", CAT, "Trestle table: a long plank top on two A-frame legs with a stretcher",
      tags=["farmhouse table", "refectory table", "sawhorse table", "dining table", "table", "furniture"], aliases=["refectory-table"])
def _(S):
    return [
        shell(rect(2.5, 5, 19, 2.5, rr(S, 1.25))),
        line(poly([(3.5, 21), (6, 7.5), (8.5, 21)], r=S.r)),
        line(poly([(15.5, 21), (18, 7.5), (20.5, 21)], r=S.r)),
        line(seg(7.3, 14, 16.7, 14)),
    ]


@icon("folding-table", CAT, "Folding table with angled fold-out legs and braces",
      tags=["fold up table", "trestle", "event table", "camping table", "portable", "furniture"])
def _(S):
    return [
        shell(rect(2.5, 6, 19, 2.5, rr(S, 1.25))),
        line(seg(5.5, 8.5, 3.5, 21)), line(seg(18.5, 8.5, 20.5, 21)),
        line(seg(4.7, 14, 10, 8.5)), line(seg(19.3, 14, 14, 8.5)),
    ]


@icon("picnic-table", CAT, "Picnic table seen from the end with crossed legs and a bench each side",
      tags=["picnic bench", "park table", "outdoor table", "camping", "bbq", "furniture"], aliases=["picnic-bench"])
def _(S):
    return [
        shell(rect(5.5, 4, 13, 2.5, rr(S, 1.25))),
        line(seg(8, 6.5, 17, 21)), line(seg(16, 6.5, 7, 21)),
        shell(rect(2.5, 13, 5, 2.5, rr(S, 1.25))), shell(rect(16.5, 13, 5, 2.5, rr(S, 1.25))),
        line(seg(7.5, 14.25, 16.5, 14.25)),
    ]


@icon("bar-table", CAT, "Tall high-top bar table on a single pole with a bar stool beside it",
      tags=["high top table", "pub table", "cocktail table", "bistro", "bar", "furniture"], aliases=["high-top-table"])
def _(S):
    return [
        shell(rect(10, 4, 11.5, 2.5, rr(S, 1.25))),
        line(seg(15.75, 6.5, 15.75, 21)),
        line(seg(12.5, 21, 19, 21)),
        shell(rect(2.5, 10, 6.5, 2.5, rr(S, 1.25))),
        line(seg(4, 12.5, 3, 21)), line(seg(7.5, 12.5, 8.5, 21)),
        line(seg(3.6, 17, 7.9, 17)),
    ]


@icon("kitchen-island", CAT, "Kitchen island with cabinet doors and a stool under the counter overhang",
      tags=["island", "breakfast bar", "kitchen counter", "worktop", "kitchen", "furniture"], aliases=["breakfast-bar"])
def _(S):
    return [
        shell(rect(2.5, 6, 19, 2.5, rr(S, 1.25))),
        shell(rect(3.5, 10.5, 10, 10.5, rr(S, 1.5))),
        detail(seg(8.5, 10.5, 8.5, 21)),
        dot(7, 13.5, 1), dot(10, 13.5, 1),
        shell(rect(15.5, 12.5, 5, 2.5, rr(S, 1.25))),
        line(seg(16.5, 15, 16, 21)), line(seg(19.5, 15, 20, 21)),
    ]


@icon("dressing-table", CAT, "Dressing table with an oval mirror, drawers and a stool",
      tags=["vanity table", "makeup table", "dresser", "bedroom", "mirror", "furniture"], aliases=["vanity-table"])
def _(S):
    return [
        shell(ellipse(12, 6, 4.5, 3.5) if S.name == "rounded" else rect(7.5, 2.5, 9, 7)),
        line(seg(12, 9.5, 12, 11)),
        shell(rect(2.5, 11, 19, 4.5, rr(S, 1.5))),
        detail(seg(8, 11, 8, 15.5)), detail(seg(16, 11, 16, 15.5)),
        line(seg(4, 15.5, 4, 21)), line(seg(20, 15.5, 20, 21)),
        shell(rect(8.5, 17.5, 7, 2, 1)),
        line(seg(9.5, 19.5, 9.5, 21)), line(seg(14.5, 19.5, 14.5, 21)),
    ]


@icon("standing-desk", CAT, "Height-adjustable standing desk with a screen and an up-down arrow",
      tags=["sit stand desk", "adjustable desk", "ergonomic", "office", "desk", "furniture"], aliases=["sit-stand-desk"])
def _(S):
    return [
        shell(rect(8, 2.5, 8, 5, rr(S, 1))),
        shell(rect(2.5, 9, 19, 2.5, rr(S, 1.25))),
        line(seg(5, 11.5, 5, 21)), line(seg(19, 11.5, 19, 21)),
        line(seg(12, 13.5, 12, 20)),
        line(poly([(9.5, 16), (12, 13.5), (14.5, 16)], r=S.r * 0.5)),
        line(poly([(9.5, 17.5), (12, 20), (14.5, 17.5)], r=S.r * 0.5)),
    ]


@icon("corner-desk", CAT, "L-shaped corner desk seen from above with a monitor and chair",
      tags=["l shaped desk", "workstation", "home office", "office", "desk", "furniture"], aliases=["l-desk"])
def _(S):
    return [
        shell(poly([(3, 3), (21, 3), (21, 21), (15, 21), (15, 9), (3, 9)], closed=True, r=S.r)),
        detail(seg(16, 5, 19, 8)),
        shell(circle(9.5, 15.5, 3)),
        line("M5 20A5.5 5.5 0 0 0 10 21"),
    ]


@icon("roll-top-desk", CAT, "Roll-top desk with a curved slatted cover and a drawer pedestal",
      tags=["rolltop desk", "bureau", "writing desk", "antique desk", "desk", "furniture"], aliases=["rolltop-desk"])
def _(S):
    cover = "M20.5 12.5V3H12A7 7 0 0 0 5 10V12.5Z"
    body = union(cover, rect(2.5, 12.5, 19, 2.5, rr(S, 1)), rect(13.5, 15, 7, 6, L(S, 0, 1.5)))
    slats = [seg(*polar(12, 10, 3.5, g), *polar(12, 10, 7, g)) for g in (200, 235)]
    return [
        shell(body),
        *[detail(d) for d in slats], detail(seg(12, 3, 12, 6.5)),
        detail(seg(13.5, 18, 20.5, 18)),
        line(seg(4, 15, 4, 21)),
    ]


@icon("secretary-desk", CAT, "Secretary desk with its front flap folded down as a writing surface",
      tags=["secretaire", "bureau", "writing desk", "drop front desk", "desk", "furniture"], aliases=["secretaire"])
def _(S):
    body = union(poly([(4, 2.5), (9.5, 2.5), (14, 10), (14, 21), (4, 21)], closed=True, r=S.r * 0.6),
                 rect(12, 10, 9.5, 2.5, L(S, 0, 1.25)))
    return [
        shell(body),
        detail(seg(4, 15, 14, 15)), detail(seg(4, 18.25, 14, 18.25)),
        line(seg(19.5, 12.5, 14, 17)),
    ]


@icon("school-desk", CAT, "Classroom desk joined to its chair by one metal frame",
      tags=["student desk", "classroom", "school", "desk chair combo", "pupil", "furniture"], aliases=["student-desk"])
def _(S):
    return [
        line(seg(3, 4.5, 3.5, 12)),
        shell(rect(2.5, 12, 7.5, 2.5, rr(S, 1.25))),
        shell(rect(11, 7, 10.5, 2.5, rr(S, 1.25))),
        line(seg(6, 14.5, 6, 21)), line(seg(18, 9.5, 18, 21)),
        line(seg(6, 18, 18, 18)),
    ]


@icon("tv-stand", CAT, "Low media cabinet with a flat-screen television on top",
      tags=["tv unit", "media console", "entertainment center", "television", "living room", "furniture"], aliases=["tv-unit", "media-console"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 9.5, rr(S, 1.5))),
        line(seg(12, 12, 12, 14)),
        shell(rect(2.5, 14, 19, 5, rr(S, 1.5))),
        detail(seg(9, 14, 9, 19)), detail(seg(15, 14, 15, 19)),
        line(seg(4.5, 19, 4.5, 21)), line(seg(19.5, 19, 19.5, 21)),
    ]


def _chair_mark(S, cx, cy, w=2.5, h=2.5):
    return sq(cx - w / 2, cy - h / 2, w, h, L(S, 0, min(w, h) / 2))


@icon("conference-table", CAT, "Long oval conference table seen from above with chairs around it",
      tags=["meeting table", "boardroom", "meeting room", "office", "meeting", "furniture"], aliases=["boardroom-table"])
def _(S):
    chairs = [(x, y) for x in (8.5, 12, 15.5) for y in (4.5, 19.5)] + [(3.5, 12), (20.5, 12)]
    return [
        shell(rect(6.5, 8.5, 11, 7, L(S, 2, 3.5))),
        *[_chair_mark(S, x, y) for x, y in chairs],
    ]


@icon("reception-desk", CAT, "Reception counter with a raised front ledge and a monitor behind",
      tags=["front desk", "reception", "check in", "lobby", "concierge", "furniture"], aliases=["front-desk"])
def _(S):
    return [
        shell(rect(11.5, 2.5, 8, 5.5, rr(S, 1))),
        line(seg(15.5, 8, 15.5, 11)),
        shell(poly([(2.5, 21), (2.5, 14), (9, 14), (9, 11), (21.5, 11), (21.5, 21)], closed=True, r=S.r * 0.6)),
        detail(seg(9, 14, 21.5, 14)),
    ]


def _tilted(cx, cy, w, h, deg, rx):
    return path_to_d(transform_path(P(rect(cx - w / 2, cy - h / 2, w, h, rx)), rotation(deg, cx, cy)))


@icon("lectern", CAT, "Standing lectern with a slanted reading top on a column",
      tags=["reading stand", "speaker stand", "pulpit", "presentation", "speech", "furniture"], aliases=["reading-stand"])
def _(S):
    return [
        shell(_tilted(12, 6, 16, 3, -14, rr(S, 1.5))),
        shell(rect(10, 10, 4, 9, L(S, 0.5, 1.5))),
        shell(rect(5.5, 19, 13, 2.5, rr(S, 1.25))),
    ]


@icon("book-stand", CAT, "Open book resting on an angled book stand with a ledge",
      tags=["book holder", "cookbook stand", "reading stand", "book rest", "reading", "furniture"], aliases=["book-holder"])
def _(S):
    page = poly([(3, 4), (11.5, 6), (11.5, 15), (3, 13)], closed=True, r=S.r * 0.5)
    return [
        shell(page), shell(flip(page)),
        line(seg(2.5, 17.5, 21.5, 17.5) if S.name == "line" else seg(3, 17.5, 21, 17.5)),
        line(seg(6, 17.5, 4, 21)), line(seg(18, 17.5, 20, 21)),
    ]


@icon("kotatsu", CAT, "Kotatsu: a low table with a thick quilt draped to the floor",
      tags=["heated table", "japanese table", "quilt table", "winter", "low table", "furniture"])
def _(S):
    return [
        shell(rect(2.5, 5.5, 19, 2.5, rr(S, 1.25))),
        shell(poly([(4.5, 10), (19.5, 10), (21.5, 20.5), (2.5, 20.5)], closed=True, r=S.r)),
        detail(seg(9, 10, 8, 20.5)), detail(seg(15, 10, 16, 20.5)),
    ]


@icon("plant-stand", CAT, "Tall three-legged plant stand holding a potted plant",
      tags=["plant holder", "flower stand", "pot stand", "houseplant", "indoor garden", "furniture"], aliases=["flower-stand"])
def _(S):
    leaf = "M11.25 7.5C8 7.5 5.5 5.5 5.5 2.5C8.5 2.5 11.25 4.5 11.25 7.5Z"
    return [
        shell(leaf), shell(flip(leaf)),
        shell(poly([(8, 9.5), (16, 9.5), (15, 13.5), (9, 13.5)], closed=True, r=S.r * 0.5)),
        line(seg(7, 15.5, 17, 15.5)),
        line(seg(8.5, 15.5, 6, 21)), line(seg(15.5, 15.5, 18, 21)), line(seg(12, 15.5, 12, 21)),
    ]


@icon("display-pedestal", CAT, "Tall square display plinth with a small vase on top",
      tags=["plinth", "display stand", "museum", "gallery", "exhibit", "furniture"], aliases=["plinth"])
def _(S):
    vase = "M10.5 2.5H13.5L13 4C15.5 4.5 15.5 8 14 8H10C8.5 8 8.5 4.5 11 4Z"
    return [
        shell(vase),
        shell(union(rect(6, 10, 12, 2.5, L(S, 0, 1)), rect(7.5, 12, 9, 7.5), rect(6, 19, 12, 2.5, L(S, 0, 1)))),
        detail(seg(7.5, 12.5, 16.5, 12.5)), detail(seg(7.5, 19, 16.5, 19)),
    ]


@icon("table-for-two", CAT, "Small square table seen from above with a chair on each side",
      tags=["table for 2", "two seats", "reservation", "restaurant", "date night", "furniture"], aliases=["table-for-2"])
def _(S):
    return [
        shell(rect(7, 8, 10, 8, rr(S, 2))),
        shell(rect(8.5, 2.5, 7, 3, rr(S, 1.5))), shell(rect(8.5, 18.5, 7, 3, rr(S, 1.5))),
    ]


@icon("table-for-four", CAT, "Rectangular table seen from above with two chairs on each long side",
      tags=["table for 4", "four seats", "reservation", "restaurant", "family", "furniture"], aliases=["table-for-4"])
def _(S):
    return [
        shell(rect(3, 8, 18, 8, rr(S, 2))),
        *[shell(rect(x, y, 5, 3, rr(S, 1.5))) for x in (5, 14) for y in (2.5, 18.5)],
    ]


# ============================================================================ beds

@icon("four-poster-bed", CAT, "Four-poster bed with tall corner posts and a draped canopy",
      tags=["canopy bed", "poster bed", "bedroom", "luxury bed", "bed", "furniture"], aliases=["canopy-bed"])
def _(S):
    return [
        dot(3.5, 2.75, 1.25), dot(20.5, 2.75, 1.25),
        line(seg(3.5, 4, 3.5, 12.5)), line(seg(20.5, 4, 20.5, 12.5)),
        line(seg(3.5, 5, 20.5, 5)),
        line("M3.5 5Q12 11 20.5 5"),
        shell(rect(2.5, 12.5, 19, 4.5, rr(S, 1.5))),
        line(seg(3.5, 17, 3.5, 21)), line(seg(20.5, 17, 20.5, 21)),
    ]


@icon("loft-bed", CAT, "Loft bed raised on a tall frame with a ladder and a desk underneath",
      tags=["high sleeper", "loft", "raised bed", "kids room", "dorm", "furniture"], aliases=["high-sleeper"])
def _(S):
    return [
        line(seg(3, 2.5, 3, 21)),
        line(seg(3, 3, 12, 3)),
        shell(rect(2.5, 5.5, 19, 3.5, rr(S, 1.5))),
        line(seg(17, 9, 17, 21)), line(seg(21, 9, 21, 21)),
        line(seg(17, 13, 21, 13)), line(seg(17, 17, 21, 17)),
        line(seg(3, 14, 13, 14)), line(seg(12, 14, 12, 21)),
    ]


@icon("wall-bed", CAT, "Wall bed folding down out of a tall cabinet on its hinge",
      tags=["murphy bed", "fold down bed", "hidden bed", "space saving", "studio apartment", "furniture"], aliases=["murphy-bed"])
def _(S):
    return [
        line(poly([(3, 21), (3, 2.5), (11, 2.5), (11, 9)], r=S.r)),
        shell(_tilted(12.5, 14.5, 17, 3.5, -38, rr(S, 1.5))),
        line(seg(2.5, 21, 21.5, 21) if S.name == "line" else seg(3, 21, 21, 21)),
    ]


@icon("trundle-bed", CAT, "Single bed with a second low mattress pulled out on wheels beneath",
      tags=["pull out bed", "guest bed", "sleepover", "trundle", "kids room", "furniture"], aliases=["pull-out-bed"])
def _(S):
    return [
        line(seg(3, 3, 3, 14)),
        shell(rect(5.5, 3, 5, 2.5, rr(S, 1.25))),
        shell(rect(3, 7.5, 15, 4, rr(S, 1.5))),
        line(seg(16, 11.5, 16, 14)),
        shell(rect(7, 14, 14.5, 3.5, rr(S, 1.5))),
        dot(9.5, 20, 1.5), dot(19, 20, 1.5),
    ]


@icon("camp-bed", CAT, "Folding camp bed with fabric stretched over crossed legs",
      tags=["cot", "camping cot", "army cot", "folding bed", "camping", "furniture"], aliases=["camping-cot"])
def _(S):
    return [
        shell(rect(2.5, 8, 19, 2.5, rr(S, 1.25))),
        line(seg(4, 10.5, 9, 20.5)), line(seg(9, 10.5, 4, 20.5)),
        line(seg(15, 10.5, 20, 20.5)), line(seg(20, 10.5, 15, 20.5)),
    ]


@icon("mattress", CAT, "Thick mattress in perspective with quilted stitch dots",
      tags=["bed mattress", "sleep", "bedding", "memory foam", "bedroom", "furniture"])
def _(S):
    body = [(6, 6), (21.5, 6), (21.5, 12), (18, 18), (2.5, 18), (2.5, 12)]
    return [
        shell(poly(body, closed=True, r=S.r * 0.6)),
        detail(poly([(2.5, 12), (18, 12), (21.5, 6)])), detail(seg(18, 12, 18, 18)),
        dot(9, 9, 1), dot(13, 9, 1), dot(17, 9, 1),
        dot(6.5, 15, 1), dot(10.5, 15, 1), dot(14.5, 15, 1),
    ]
