"""TypeIcon Core: furniture (batch furniture_003).

Original drawings of wall decor, windows, doors, stairs, fireplaces, rooms, and assorted home furnishings.
Simple silhouettes (shells) carry the mass; frames, panes and supports are open strokes or details.
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


# ============================================================================ wall decor

@icon("gallery-wall", CAT, "Cluster of three picture frames of different sizes hung together",
      tags=["picture wall", "frames", "photos", "wall art", "display", "decor"])
def _(S):
    return [
        shell(rect(3, 3, 9, 12, rr(S, 2))),
        detail(poly([(5, 12), (7.5, 8.5), (10, 12)], r=S.r * 0.3)),
        shell(rect(15, 3, 6, 6, rr(S, 1.5))),
        shell(rect(15, 12, 6, 9, rr(S, 1.5))),
        shell(rect(3, 18, 9, 3, rr(S, 1))),
    ]


@icon("ornate-frame", CAT, "Picture frame with a carved baroque border and scooped corners",
      tags=["baroque frame", "gilded frame", "antique frame", "picture frame", "portrait", "art"])
def _(S):
    c = 3
    outer = (f"M{3 + c} 3H{21 - c}A{c} {c} 0 0 0 21 {3 + c}V{21 - c}A{c} {c} 0 0 0 {21 - c} 21H{3 + c}"
             f"A{c} {c} 0 0 0 3 {21 - c}V{3 + c}A{c} {c} 0 0 0 {3 + c} 3Z")
    return [
        shell(outer),
        detail(rect(8, 8, 8, 8, L(S, 0, 2))),
        dot(12, 12, 1.25),
    ]


@icon("wall-poster", CAT, "Poster stuck to a wall with tape at the top corners and a curled bottom corner",
      tags=["poster", "print", "taped poster", "wall art", "dorm", "advertising"])
def _(S):
    body = [(4, 4), (20, 4), (20, 14), (14, 20), (4, 20)]
    return [
        shell(poly(body, closed=True, r=S.r * 0.4)),
        detail(poly([(14, 20), (14, 14), (20, 14)], r=S.r * 0.3)),
        detail(seg(7.5, 9, 16.5, 9)),
        line(seg(2, 6, 6, 2)),
        line(seg(18, 2, 22, 6)),
    ]


@icon("wall-mural", CAT, "Painted landscape on a wall with a paint roller below it",
      tags=["mural", "wall painting", "street art", "paint roller", "decorating", "art"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 9.5, rr(S, 2))),
        detail(poly([(5, 10), (9, 6), (13, 10)], r=S.r * 0.3)),
        dot(17.5, 7, 1.3),
        shell(rect(3, 15, 13, 3.5, rr(S, 1.5))),
        line(poly([(16, 16.75), (19.5, 16.75), (19.5, 21.5)], r=S.r)),
    ]


@icon("ship-in-bottle", CAT, "Sailing ship built inside a glass bottle lying on a cradle",
      tags=["bottle ship", "model ship", "miniature", "nautical", "craft", "souvenir"])
def _(S):
    bottle = ("M8 4H13C15 4 15.5 7 17 7H21.5V12H17C15.5 12 15 15 13 15H8A5.5 5.5 0 0 1 8 4Z")
    return [
        shell(bottle),
        detail(seg(9.5, 6.5, 9.5, 10)),
        mark(poly([(10.5, 6.5), (13, 10), (10.5, 10)], closed=True)),
        mark(poly([(6.5, 10.5), (13.5, 10.5), (12, 12.5), (8, 12.5)], closed=True)),
        line(seg(4.5, 21, 19.5, 21)),
        line(seg(8, 15, 8, 21)), line(seg(15, 15, 15, 21)),
    ]


def bulb_points():
    pts = []
    # left leg from apex to foot, right leg, crossbar
    n = 6
    for i in range(n + 1):
        t = i / n
        pts.append((12 - 7 * t, 3.5 + 17.5 * t))
    for i in range(1, n + 1):
        t = i / n
        pts.append((12 + 7 * t, 3.5 + 17.5 * t))
    for x in (9.4, 12, 14.6):
        pts.append((x, 14.5))
    return pts


@icon("marquee-letter", CAT, "Big letter A made of round light bulbs, like a carnival or cinema sign",
      tags=["light up letter", "marquee sign", "bulb letter", "carnival", "cinema", "decor"],
      filled=lambda: U(*[P(circle(x, y, 1.65)) for x, y in bulb_points()]))
def _(S):
    r = L(S, 1.1, 1.4)
    return [dot(x, y, r) for x, y in bulb_points()]


@icon("patchwork-quilt", CAT, "Quilt made of square patches with different simple patterns",
      tags=["quilt", "blanket", "patchwork", "bedspread", "sewing", "craft"])
def _(S):
    return [
        shell(rect(3, 4, 18, 16, rr(S, 2))),
        detail(seg(9, 4, 9, 20)), detail(seg(15, 4, 15, 20)), detail(seg(3, 12, 21, 12)),
        dot(6, 8, 1.2), dot(18, 8, 1.2), dot(12, 16, 1.2),
        detail(seg(10.5, 10.5, 13.5, 5.5)),
        detail(seg(4.5, 17.5, 7.5, 13.5)),
        detail(seg(16.5, 17.5, 19.5, 13.5)),
    ]


# ============================================================================ windows

@icon("sash-window", CAT, "Tall window with two sashes, the lower one slid up to leave a gap",
      tags=["sash", "double hung window", "sliding sash", "georgian", "victorian", "panes"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, rr(S, 2))),
        detail(seg(4.5, 9.5, 19.5, 9.5)),
        detail(seg(4.5, 16, 19.5, 16)),
        detail(seg(12, 3.5, 12, 16)),
    ]


@icon("casement-window", CAT, "Window frame with a side-hinged pane swung open toward the viewer",
      tags=["hinged window", "open window", "swing window", "cottage window", "ventilation", "frame"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 2))),
        detail(poly([(19.5, 4.5), (11, 7.5), (11, 16.5), (19.5, 19.5)], closed=True, r=S.r * 0.3)),
        detail(seg(11, 12, 19.5, 12)),
    ]


@icon("bay-window", CAT, "Bay window with a flat centre section and two angled side sections",
      tags=["bow window", "projecting window", "alcove", "window seat", "living room", "house"])
def _(S):
    outline = [(3, 3), (8.5, 5.5), (15.5, 5.5), (21, 3), (21, 21), (15.5, 18.5), (8.5, 18.5), (3, 21)]
    return [
        shell(poly(outline, closed=True, r=S.r * 0.4)),
        detail(seg(8.5, 5.5, 8.5, 18.5)),
        detail(seg(15.5, 5.5, 15.5, 18.5)),
    ]


@icon("arched-window", CAT, "Tall window with a semicircular top divided into panes",
      tags=["arch window", "round top window", "palladian", "church window", "panes", "house"])
def _(S):
    return [
        shell(top_round(5, 2.5, 14, 19, 7, L(S, 0, 2))),
        detail(seg(12, 3.5, 12, 21)),
        detail(seg(5, 12, 19, 12)),
    ]


@icon("round-window", CAT, "Circular porthole window with a thick frame and a cross bar",
      tags=["porthole", "circle window", "ship window", "oculus", "bullseye window", "nautical"])
def _(S):
    outer = poly(regular(12, 12, 9.6, 8, -22.5), closed=True) if S.name == "line" else circle(12, 12, 9)
    return [
        shell(outer),
        detail(circle(12, 12, 5.5)),
        detail(seg(12, 7, 12, 17)),
        detail(seg(7, 12, 17, 12)),
    ]


@icon("gothic-window", CAT, "Tall narrow window with a pointed arch top and stone tracery",
      tags=["pointed arch", "lancet window", "cathedral window", "church", "medieval", "tracery"])
def _(S):
    if S.name == "line":
        d = "M6.5 21.5V10C6.5 6.5 9.5 4 12 2C14.5 4 17.5 6.5 17.5 10V21.5Z"
    else:
        d = "M6.5 19.5A2 2 0 0 0 8.5 21.5H15.5A2 2 0 0 0 17.5 19.5V10C17.5 6.5 14 4.5 12 3.5C10 4.5 6.5 6.5 6.5 10Z"
    return [
        shell(d),
        detail(seg(12, 11, 12, 21)),
        detail(seg(6.5, 15.5, 17.5, 15.5)),
        dot(12, 7.5, 1.3),
    ]


@icon("dormer-window", CAT, "Small gabled window projecting from a sloping roof",
      tags=["roof window", "attic window", "gable", "loft", "roofline", "house"])
def _(S):
    return [
        line(poly([(1.5, 21.5), (5, 4.5), (19, 4.5), (22.5, 21.5)], r=S.r)),
        shell(poly([(8, 21), (8, 13), (12, 9.5), (16, 13), (16, 21)], closed=True, r=S.r * 0.5)),
        sq(10.5, 14, 3, 4),
    ]


@icon("stained-glass-window", CAT, "Arched window filled with coloured pieces held by lead lines",
      tags=["leaded glass", "church window", "mosaic glass", "cathedral", "coloured glass", "art glass"])
def _(S):
    return [
        shell(top_round(5, 2.5, 14, 19, 7, L(S, 0, 2))),
        detail(poly([(12, 7.5), (15.5, 12.5), (12, 17.5), (8.5, 12.5)], closed=True)),
        detail(seg(12, 3.5, 12, 7.5)),
        detail(seg(5, 12.5, 8.5, 12.5)),
        detail(seg(15.5, 12.5, 19, 12.5)),
        detail(seg(12, 17.5, 12, 21)),
    ]


@icon("louvered-window", CAT, "Window frame filled with angled glass slats like open louvers",
      tags=["louvre", "jalousie", "slatted window", "shutter", "vent", "tropical"])
def _(S):
    return [
        shell(rect(4.5, 2.5, 15, 19, rr(S, 2))),
        detail(seg(7.5, 8.5, 16.5, 6.5)),
        detail(seg(7.5, 13.5, 16.5, 11.5)),
        detail(seg(7.5, 18.5, 16.5, 16.5)),
    ]


@icon("double-glazing", CAT, "Window frame section with two parallel glass panes and a gas gap between them",
      tags=["double glazed", "insulated glass", "thermal window", "energy saving", "glass panes", "window"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 2))),
        detail(seg(9, 3.5, 9, 21)),
        detail(seg(15, 3.5, 15, 21)),
        dot(12, 8, 1), dot(12, 12, 1), dot(12, 16, 1),
    ]


# ============================================================================ doors

@icon("french-doors", CAT, "Pair of tall glazed doors with small panes meeting in the middle",
      tags=["patio doors", "double doors", "glass doors", "garden doors", "panes", "entrance"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 2))),
        detail(seg(12, 3.5, 12, 21)),
        detail(seg(3.5, 8, 20.5, 8)),
        detail(seg(3.5, 16, 20.5, 16)),
        dot(10, 12, 1), dot(14, 12, 1),
    ]


@icon("sliding-door", CAT, "Glass patio door with one panel slid over the other and a sideways arrow",
      tags=["patio door", "glass door", "slider", "balcony door", "track door", "entrance"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 2))),
        detail(seg(12, 3.5, 12, 21)),
        line(seg(5.5, 12, 9.5, 12)),
        line(poly([(8, 10), (10, 12), (8, 14)], r=S.r * 0.3)),
        detail(seg(16.5, 9, 16.5, 15)),
    ]


@icon("revolving-door", CAT, "Revolving door drum seen from above with its four glass panels",
      tags=["rotating door", "hotel entrance", "lobby", "turnstile door", "entrance", "building"])
def _(S):
    return [
        line(arc(12, 12, 9, 205, 335)),
        line(arc(12, 12, 9, 25, 155)),
        line(seg(7.4, 7.4, 16.6, 16.6)),
        line(seg(16.6, 7.4, 7.4, 16.6)),
    ]


@icon("saloon-doors", CAT, "Pair of swinging half doors hung between two posts, like in a western bar",
      tags=["swinging doors", "western", "cowboy", "bar doors", "wild west", "half doors"])
def _(S):
    return [
        line(seg(2.5, 3, 2.5, 21.5)), line(seg(21.5, 3, 21.5, 21.5)),
        shell(poly([(5.5, 7), (11.5, 8), (11.5, 17), (5.5, 18)], closed=True, r=S.r * 0.4)),
        shell(poly([(18.5, 7), (12.5, 8), (12.5, 17), (18.5, 18)], closed=True, r=S.r * 0.4)),
        detail(seg(7.5, 12.5, 11.5, 12.5)),
        detail(seg(16.5, 12.5, 12.5, 12.5)),
    ]


@icon("dutch-door", CAT, "Stable door split in two with the top half open and the bottom half closed",
      tags=["stable door", "half door", "split door", "farmhouse", "cottage", "entrance"])
def _(S):
    return [
        line(poly([(3.5, 21.5), (3.5, 2.5), (20.5, 2.5), (20.5, 21.5)], r=S.r)),
        shell(poly([(7, 4), (11, 6), (11, 10), (7, 12)], closed=True, r=S.r * 0.3)),
        shell(rect(7, 14, 10, 7.5, rr(S, 1.5))),
        dot(14.5, 17.5, 1),
    ]


@icon("screen-door", CAT, "Door with a thin frame and a fine mesh screen panel and handle",
      tags=["mesh door", "fly screen", "insect screen", "porch door", "flyscreen", "bug screen"])
def _(S):
    return [
        shell(rect(5, 2.5, 14, 19, rr(S, 2))),
        detail(seg(9.5, 4, 9.5, 14.5)),
        detail(seg(14.5, 4, 14.5, 14.5)),
        detail(seg(5.5, 8, 18.5, 8)),
        detail(seg(5.5, 14.5, 18.5, 14.5)),
        dot(16.5, 18, 1),
    ]


@icon("arched-door", CAT, "Heavy wooden door with a rounded top, vertical planks and iron studs",
      tags=["castle door", "round top door", "wooden door", "medieval", "cottage door", "entrance"])
def _(S):
    return [
        shell(top_round(4.5, 2.5, 15, 19, 7.5, L(S, 0, 2))),
        detail(seg(9.5, 7, 9.5, 21)),
        detail(seg(14.5, 7, 14.5, 21)),
        dot(7, 13, 0.9), dot(12, 13, 0.9), dot(17, 13, 0.9),
        dot(7, 18, 0.9), dot(12, 18, 0.9), dot(17, 18, 0.9),
    ]


@icon("trapdoor", CAT, "Square hatch in the floor with its lid propped open and a ring pull",
      tags=["hatch", "cellar door", "floor hatch", "attic hatch", "secret entrance", "basement"])
def _(S):
    return [
        shell(poly([(7.5, 4), (16.5, 4), (18, 12), (6, 12)], closed=True, r=S.r * 0.4)),
        dot(12, 8, 1.2),
        shell(poly([(6, 14.5), (18, 14.5), (21.5, 21), (2.5, 21)], closed=True, r=S.r * 0.4)),
    ]


@icon("door-knocker", CAT, "Round ring knocker hanging from a small plate on a door",
      tags=["knocker", "door ring", "entrance", "front door", "traditional", "hardware"])
def _(S):
    return [
        shell(rect(8.5, 2.5, 7, 6.5, rr(S, 3))),
        line(circle(12, 14.5, 5)),
        dot(12, 5.75, 1),
    ]


@icon("doorknob", CAT, "Round door knob on an upright rose plate with a keyhole below",
      tags=["door handle", "knob", "door hardware", "lock", "keyhole", "entry"])
def _(S):
    return [
        shell(rect(7, 2.5, 10, 19, rr(S, 5))),
        dot(12, 9, 3.3),
        dot(12, 15.5, 1.3),
        line(seg(12, 15.5, 12, 18.5)),
    ]


@icon("door-hinge", CAT, "Butt hinge with two flat leaves joined by a central pin and screw holes",
      tags=["hinge", "butt hinge", "door hardware", "pivot", "screws", "joint"])
def _(S):
    return [
        shell(rect(3, 3.5, 8, 17, rr(S, 1.5))),
        shell(rect(13, 3.5, 8, 17, rr(S, 1.5))),
        shell(rect(10, 2.5, 4, 19, rr(S, 2))),
        dot(6.5, 7, 1), dot(6.5, 12, 1), dot(6.5, 17, 1),
        dot(17.5, 7, 1), dot(17.5, 12, 1), dot(17.5, 17, 1),
    ]


@icon("house-number", CAT, "Small plaque showing a house number mounted beside a door frame",
      tags=["street number", "address plaque", "address number", "door number", "mailbox number", "house"])
def _(S):
    return [
        shell(rect(2.5, 6.5, 13, 11, rr(S, 2))),
        detail(seg(6.5, 9.5, 6.5, 14.5)),
        detail(poly([(9.5, 9.5), (12, 9.5), (12, 12), (9.5, 14.5), (12.5, 14.5)])),
        line(seg(19, 2.5, 19, 21.5)),
    ]


# ============================================================================ architecture inside the home

@icon("archway", CAT, "Rounded arch opening cut through a thick wall down to the floor",
      tags=["arch", "doorway", "arched opening", "passage", "entrance", "wall opening"])
def _(S):
    r = L(S, 0, 3)
    d = (f"M8 21H3V{3 + r}" + (f"A{r} {r} 0 0 1 {3 + r} 3" if r else "") + f"H{21 - r}"
         + (f"A{r} {r} 0 0 1 21 {3 + r}" if r else "") + "V21H16V12A4 4 0 0 0 8 12Z")
    return [shell(d)]


@icon("classical-column", CAT, "Classical column with a fluted shaft, a capital on top and a base",
      tags=["pillar", "greek column", "roman column", "ionic", "doric", "architecture"])
def _(S):
    return [
        shell(rect(4, 2.5, 16, 3.5, rr(S, 1.5))),
        shell(rect(7, 6, 10, 12)),
        detail(seg(10, 7, 10, 17)), detail(seg(14, 7, 14, 17)),
        shell(rect(4, 18, 16, 3.5, rr(S, 1.5))),
    ]


def vase(cx, y0=8, y1=17.5):
    m = (y0 + y1) / 2
    return solid(f"M{fmt(cx - 1)} {y0}H{fmt(cx + 1)}C{fmt(cx + 1)} {y0 + 2.2} {fmt(cx + 2.2)} {m - 1.5} {fmt(cx + 2.2)} {m + 0.5}"
                 f"C{fmt(cx + 2.2)} {m + 2.5} {fmt(cx + 1)} {y1 - 2.2} {fmt(cx + 1)} {y1}H{fmt(cx - 1)}"
                 f"C{fmt(cx - 1)} {y1 - 2.2} {fmt(cx - 2.2)} {m + 2.5} {fmt(cx - 2.2)} {m + 0.5}"
                 f"C{fmt(cx - 2.2)} {m - 1.5} {fmt(cx - 1)} {y0 + 2.2} {fmt(cx - 1)} {y0}Z")


@icon("balustrade", CAT, "Railing with a top handrail held up by turned vase-shaped balusters",
      tags=["baluster", "banister", "railing", "handrail", "stair rail", "terrace"])
def _(S):
    return [
        shell(rect(2.5, 3.5, 19, 3.5, rr(S, 1.75))),
        shell(rect(2.5, 17.5, 19, 3.5, rr(S, 1.75))),
        vase(6.5, 7.5, 17.5), vase(12, 7.5, 17.5), vase(17.5, 7.5, 17.5),
    ]


@icon("spiral-staircase", CAT, "Spiral staircase with wedge steps alternating left and right around a central pole",
      tags=["spiral stairs", "winding stairs", "helical stair", "loft access", "steps", "tower"])
def _(S):
    parts = [line(seg(12, 2.5, 12, 21.5))]
    for i, y in enumerate((5, 10, 15, 20)):
        if i % 2 == 0:
            pts = [(12, y - 0.5), (21.5, y - 1.8), (21.5, y + 1.8), (12, y + 1.5)]
        else:
            pts = [(12, y - 0.5), (2.5, y - 1.8), (2.5, y + 1.8), (12, y + 1.5)]
        parts.append(solid(poly(pts, closed=True, r=S.r * 0.5)))
    return parts


@icon("attic-ladder", CAT, "Folding ladder pulled down from a hatch in the ceiling",
      tags=["loft ladder", "pull down ladder", "folding stairs", "roof access", "hatch", "loft"])
def _(S):
    return [
        line(seg(2.5, 4.5, 6, 4.5)), line(seg(18, 4.5, 21.5, 4.5)),
        shell(rect(6, 2.5, 12, 4, rr(S, 1))),
        line(seg(8.5, 7, 7.5, 21.5)), line(seg(15.5, 7, 16.5, 21.5)),
        line(seg(8.2, 11.5, 15.8, 11.5)),
        line(seg(8, 16, 16, 16)),
    ]


@icon("library-ladder", CAT, "Rolling library ladder hooked on a top rail with a small wheel at each foot",
      tags=["rolling ladder", "bookshelf ladder", "step ladder", "bookcase", "reading", "library"])
def _(S):
    return [
        line(seg(2.5, 3, 21.5, 3)),
        line(seg(9, 3.5, 5, 19.5)), line(seg(16, 3.5, 12, 19.5)),
        line(seg(8, 8.5, 15, 8.5)), line(seg(7, 13, 14, 13)),
        dot(5, 20.5, 1.3), dot(12, 20.5, 1.3),
        line(seg(20.5, 6, 20.5, 21.5)),
    ]


@icon("mantelpiece", CAT, "Fireplace surround with a wide shelf holding a clock and two candles",
      tags=["mantel", "fireplace", "chimney breast", "shelf", "hearth", "living room"])
def _(S):
    return [
        shell(rect(2.5, 9.5, 19, 3, rr(S, 1.5))),
        shell(rect(4.5, 12.5, 15, 9, rr(S, 1.5))),
        detail(poly([(8.5, 21), (8.5, 16.5), (15.5, 16.5), (15.5, 21)])),
        shell(circle(12, 5.5, 2.5)),
        line(seg(5, 5, 5, 8.5)), dot(5, 2.6, 1),
        line(seg(19, 5, 19, 8.5)), dot(19, 2.6, 1),
    ]


FLAME = "M13 2.5C13 5.5 16 7 16 10A4 4 0 0 1 8 10C8 8.2 9 7 10 6C10.4 7.6 11 7.6 11.6 7C12.6 5.8 13 4.3 13 2.5Z"


@icon("fire-screen", CAT, "Three-panel mesh screen standing in front of a small fire",
      tags=["fireguard", "fireplace screen", "spark guard", "hearth", "safety", "fireplace"])
def _(S):
    return [
        shell(FLAME),
        shell(rect(3.5, 10, 17, 11, rr(S, 2))),
        detail(seg(9, 10.5, 9, 20.5)), detail(seg(15, 10.5, 15, 20.5)),
        detail(seg(4, 15.5, 20, 15.5)),
    ]


@icon("fireplace-tools", CAT, "Stand holding a poker, a shovel and a brush",
      tags=["poker", "fire tools", "hearth set", "fireplace set", "shovel", "tongs"])
def _(S):
    return [
        shell(rect(3.5, 15.5, 17, 6, rr(S, 2))),
        line(poly([(7, 16), (7, 5.5), (4.5, 3.5)], r=S.r)),
        line(seg(12, 16, 12, 9)), solid(rect(10.25, 3.5, 3.5, 5.5)),
        line(seg(17, 16, 17, 9)), solid(poly([(15.5, 9), (18.5, 9), (19.5, 3.5), (14.5, 3.5)], closed=True)),
    ]


@icon("firewood-rack", CAT, "Metal rack holding a stack of split logs",
      tags=["log rack", "wood stack", "log holder", "firewood", "logs", "fireplace"])
def _(S):
    return [
        line(poly([(3.5, 3.5), (3.5, 19.5), (20.5, 19.5), (20.5, 3.5)], r=S.r)),
        line(seg(3.5, 19.5, 3.5, 21.5)), line(seg(20.5, 19.5, 20.5, 21.5)),
        shell(circle(7.5, 15.5, 2.6)), shell(circle(12, 15.5, 2.6)), shell(circle(16.5, 15.5, 2.6)),
        shell(circle(9.75, 10, 2.6)), shell(circle(14.25, 10, 2.6)),
    ]


@icon("bellows", CAT, "Fireplace bellows with two boards, pleated leather sides and a nozzle",
      tags=["fire bellows", "blower", "air pump", "fireplace", "stoke fire", "hearth"])
def _(S):
    return [
        line(seg(2.5, 4, 16, 9.5)), line(seg(2.5, 20, 16, 14.5)),
        line(seg(16, 9.5, 16, 14.5)),
        line(seg(16, 12, 21.5, 12)),
        detail(seg(8, 6.8, 8, 17.2)),
        detail(seg(12, 8.2, 12, 15.8)),
    ]


@icon("chiminea", CAT, "Clay outdoor fireplace with a round belly, an arched fire opening and a tall chimney",
      tags=["patio heater", "clay fireplace", "outdoor fire", "garden fire", "terracotta", "chimney"])
def _(S):
    body = union("M10.5 4H13.5V8C18 9 20.5 11.5 20.5 15C20.5 18.8 17 21 12 21C7 21 3.5 18.8 3.5 15C3.5 11.5 6 9 10.5 8Z",
                 rect(8.5, 2.5, 7, 3, L(S, 0, 1.5)))
    return [
        shell(body),
        mark(top_round(9, 12.5, 6, 6.5, 3)),
    ]


@icon("fire-pit", CAT, "Round shallow fire bowl on three legs with flames rising from it",
      tags=["firepit", "campfire", "fire bowl", "patio fire", "backyard", "bonfire"])
def _(S):
    return [
        shell(FLAME),
        shell("M3 12.5H21C21 16.5 17 18.5 12 18.5C7 18.5 3 16.5 3 12.5Z"),
        line(seg(7, 18, 5, 21.5)), line(seg(17, 18, 19, 21.5)),
    ]


# ============================================================================ rooms

@icon("living-room", CAT, "Living room with a sofa, a picture on the wall and a floor lamp",
      tags=["lounge", "sitting room", "sofa", "couch", "family room", "interior"])
def _(S):
    return [
        shell(rect(5.5, 2.5, 7, 4.5, rr(S, 1.5))),
        shell(rect(4.5, 9.5, 10, 5, rr(S, 2))),
        shell(rect(2.5, 13.5, 14, 6, rr(S, 2))),
        line(seg(5, 19.5, 5, 21.5)), line(seg(14, 19.5, 14, 21.5)),
        solid(poly([(17, 3), (22, 3), (21.5, 8), (17.5, 8)], closed=True)),
        line(seg(19.5, 8, 19.5, 21.5)),
    ]


@icon("bedroom", CAT, "Bedroom with a bed, a window above it and a nightstand with a lamp",
      tags=["bed room", "sleeping room", "bed", "nightstand", "master bedroom", "interior"])
def _(S):
    return [
        shell(rect(5, 2.5, 8, 6, rr(S, 1.5))),
        detail(seg(9, 3.5, 9, 8)),
        line(seg(3, 11, 3, 21.5)),
        shell(rect(3, 14.5, 13, 4.5, rr(S, 1.5))),
        line(seg(16, 19, 16, 21.5)),
        solid(poly([(18.5, 9), (21.5, 9), (22, 12), (18, 12)], closed=True)),
        shell(rect(18, 14.5, 4, 7, rr(S, 1))),
    ]


@icon("dining-room", CAT, "Dining room with a table, two chairs and a pendant light above",
      tags=["dining area", "kitchen table", "eating room", "table and chairs", "meal", "interior"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 5)),
        solid(poly([(9, 8), (15, 8), (13.5, 5), (10.5, 5)], closed=True)),
        shell(rect(7, 12, 10, 2.5, rr(S, 1.25))),
        line(seg(8.5, 14.5, 8.5, 21.5)), line(seg(15.5, 14.5, 15.5, 21.5)),
        line(poly([(2.5, 9), (2.5, 16), (5, 16), (5, 21.5)], r=S.r)),
        line(poly([(21.5, 9), (21.5, 16), (19, 16), (19, 21.5)], r=S.r)),
    ]


@icon("home-office", CAT, "Home office with a desk, a monitor, an office chair and a wall shelf",
      tags=["study", "workspace", "work from home", "remote work", "desk setup", "interior"])
def _(S):
    return [
        line(seg(14, 4, 21.5, 4)),
        shell(rect(3, 5.5, 9, 6.5, rr(S, 1.5))),
        line(seg(7.5, 12, 7.5, 14)),
        shell(rect(2.5, 14, 13, 2.5, rr(S, 1.25))),
        line(seg(4, 16.5, 4, 21.5)), line(seg(14, 16.5, 14, 21.5)),
        line(poly([(19, 8), (19, 16.5), (22, 16.5)], r=S.r)),
        line(seg(19.5, 16.5, 19.5, 21.5)),
    ]


@icon("nursery", CAT, "Baby nursery with a crib and a mobile hanging above it",
      tags=["baby room", "crib", "cot", "infant", "mobile", "kids room"])
def _(S):
    return [
        line(seg(12, 2.5, 12, 5)),
        line(seg(6.5, 5, 17.5, 5)),
        line(seg(6.5, 5, 6.5, 7)), dot(6.5, 8.3, 1.3),
        line(seg(17.5, 5, 17.5, 7)), dot(17.5, 8.3, 1.3),
        shell(rect(3, 12, 18, 6.5, rr(S, 2))),
        detail(seg(8, 12.5, 8, 18)), detail(seg(12, 12.5, 12, 18)), detail(seg(16, 12.5, 16, 18)),
        line(seg(5, 18.5, 5, 21.5)), line(seg(19, 18.5, 19, 21.5)),
    ]


@icon("attic", CAT, "Triangular roof space with a small round window and a box under the slope",
      tags=["loft", "roof space", "garret", "storage", "top floor", "house"])
def _(S):
    return [
        shell(poly([(2.5, 21), (12, 3.5), (21.5, 21)], closed=True, r=S.r)),
        dot(12, 12, 2),
        sq(14.5, 15.5, 3.5, 3.5),
    ]


@icon("basement", CAT, "House above the ground line with a room below ground and a stairway down",
      tags=["cellar", "underground room", "lower level", "below ground", "storage", "house"])
def _(S):
    return [
        line(poly([(6, 10), (6, 7), (12, 3), (18, 7), (18, 10)], r=S.r)),
        line(seg(2.5, 10.5, 21.5, 10.5)),
        shell(rect(4.5, 13.5, 15, 8, rr(S, 2))),
        mark(poly([(6.5, 20), (6.5, 16.5), (9.5, 16.5), (9.5, 18.3), (12.5, 18.3), (12.5, 20)], closed=True)),
    ]


@icon("hallway", CAT, "Corridor in one-point perspective with doors on the side walls",
      tags=["corridor", "passage", "entrance hall", "vanishing point", "perspective", "interior"])
def _(S):
    return [
        shell(rect(3, 3, 18, 18, rr(S, 2))),
        detail(rect(9, 9, 6, 6)),
        detail(seg(4, 4, 9, 9)), detail(seg(20, 4, 15, 9)),
        detail(seg(4, 20, 9, 15)), detail(seg(20, 20, 15, 15)),
    ]


@icon("walk-in-closet", CAT, "Closet with a shelf, a rail of hanging clothes and shoes on the floor",
      tags=["dressing room", "wardrobe room", "clothes storage", "closet", "hangers", "bedroom"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 19, rr(S, 2))),
        detail(seg(3.5, 5.5, 20.5, 5.5)),
        detail(seg(3.5, 9, 20.5, 9)),
        mark(poly([(5, 10), (8, 10), (8.5, 16), (4.5, 16)], closed=True)),
        mark(poly([(10.5, 10), (13.5, 10), (14, 16), (10, 16)], closed=True)),
        mark(poly([(16, 10), (19, 10), (19.5, 16), (15.5, 16)], closed=True)),
        sq(5, 18, 4, 1.8), sq(14, 18, 4, 1.8),
    ]


@icon("reading-nook", CAT, "Cosy armchair beside a tall floor lamp arching over it",
      tags=["book corner", "cozy corner", "armchair", "lamp", "reading corner", "relax"])
def _(S):
    return [
        shell(rect(3.5, 7, 10, 7, rr(S, 2))),
        shell(rect(2.5, 12.5, 12, 6.5, rr(S, 2))),
        line(seg(5, 19, 5, 21.5)), line(seg(12, 19, 12, 21.5)),
        line(poly([(19.5, 21.5), (19.5, 5), (15.5, 3.5)], r=S.r)),
        line(seg(17, 21.5, 22, 21.5)),
        solid(poly([(14, 2.5), (17.5, 2.5), (18, 5), (13.5, 5)], closed=True)),
    ]


@icon("waiting-room", CAT, "Row of three joined chairs on a shared beam below a wall clock",
      tags=["waiting area", "lobby seating", "reception", "clinic", "airport seating", "chairs"])
def _(S):
    return [
        line(circle(12, 5.5, 2.6)),
        shell(rect(3, 10.5, 18, 5.5, rr(S, 2))),
        detail(seg(9, 11, 9, 16)), detail(seg(15, 11, 15, 16)),
        line(seg(2.5, 18.5, 21.5, 18.5)),
        line(seg(5, 18.5, 5, 21.5)), line(seg(19, 18.5, 19, 21.5)),
    ]


@icon("playroom", CAT, "Children's playroom with stacked toy blocks and an open toy box with a star",
      tags=["kids room", "toys", "toy box", "blocks", "nursery", "play area"])
def _(S):
    star = [polar(16, 7, 3.6 if i % 2 == 0 else 1.6, -90 + 36 * i) for i in range(10)]
    return [
        shell(rect(2.5, 15, 6, 6.5, rr(S, 1.5))),
        shell(rect(3.5, 9.5, 4, 4.5, rr(S, 1))),
        shell(rect(11, 14, 11, 7.5, rr(S, 2))),
        detail(seg(11.5, 17.5, 21.5, 17.5)),
        solid(poly(star, closed=True)),
    ]


@icon("entryway", CAT, "Entryway with a front door, a coat on a stand beside it and a doormat below",
      tags=["foyer", "entrance hall", "front door", "coat rack", "mudroom", "doormat"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 10, 16.5, rr(S, 2))),
        dot(11, 11.5, 1.1),
        solid(rect(2.5, 19.5, 12, 2)),
        line(seg(19, 3, 19, 21.5)), line(seg(16, 21.5, 22, 21.5)),
        solid(poly([(16.5, 8), (21.5, 8), (22, 16), (16, 16)], closed=True)),
    ]


@icon("empty-room", CAT, "Isometric empty room with two walls, a floor and a door",
      tags=["vacant room", "blank room", "unfurnished", "bare room", "to let", "real estate"])
def _(S):
    hexa = [(12, 3.5), (21, 8), (21, 18), (12, 22.5), (3, 18), (3, 8)]
    return [
        shell(poly(hexa, closed=True, r=S.r * 0.6)),
        detail(poly([(3, 18), (12, 13.5), (21, 18)])),
        detail(seg(12, 13.5, 12, 4)),
        detail(poly([(15.5, 15.5), (15.5, 9), (18.5, 10.5), (18.5, 17)], closed=True)),
    ]


@icon("floor-area", CAT, "Square floor plan with measuring arrows along two sides",
      tags=["room size", "square footage", "square meters", "measurement", "dimensions", "floor plan"])
def _(S):
    return [
        shell(rect(3, 3, 13, 13, rr(S, 1.5))),
        line(seg(3, 20, 16, 20)),
        line(poly([(5.5, 18), (3.3, 20), (5.5, 22)], r=S.r * 0.3)),
        line(poly([(13.5, 18), (15.7, 20), (13.5, 22)], r=S.r * 0.3)),
        line(seg(20, 3, 20, 16)),
        line(poly([(18, 5.5), (20, 3.3), (22, 5.5)], r=S.r * 0.3)),
        line(poly([(18, 13.5), (20, 15.7), (22, 13.5)], r=S.r * 0.3)),
    ]


def fan_lines(px, py, length, angles):
    out = []
    for a in angles:
        ex, ey = px + length * math.sin(math.radians(a)), py - length * math.cos(math.radians(a))
        out.append(line(seg(px, py, ex, ey)))
    return out


@icon("interior-design", CAT, "Armchair beside a fan of colour swatches",
      tags=["decorating", "home decor", "colour palette", "swatches", "styling", "furnishing"])
def _(S):
    return [
        shell(rect(2.5, 6, 7.5, 7, rr(S, 2))),
        shell(rect(2.5, 11.5, 9.5, 6.5, rr(S, 2))),
        line(seg(4.5, 18, 4.5, 21.5)), line(seg(10, 18, 10, 21.5)),
        *fan_lines(15.5, 21, 9.5, (-6, 18, 42)),
    ]


@icon("flat-pack-furniture", CAT, "Flat box printed with a chair next to a hex key",
      tags=["self assembly", "assemble", "diy furniture", "hex key", "allen key"])
def _(S):
    return [
        shell(rect(2.5, 6, 12, 15.5, rr(S, 2))),
        detail(poly([(5, 9), (6.5, 14), (12, 14)])),
        detail(seg(6.5, 14, 5.5, 18.5)), detail(seg(12, 14, 13, 18.5)),
        line(poly([(22, 4.5), (19, 4.5), (19, 21)], r=S.r)),
    ]


@icon("upholstery", CAT, "Armchair with a curved upholstery needle beside it",
      tags=["reupholster", "sewing furniture", "fabric", "needle", "chair repair", "craft"])
def _(S):
    return [
        shell(rect(2.5, 5, 10, 7, rr(S, 2))),
        shell(rect(2.5, 10.5, 12, 7, rr(S, 2))),
        line(seg(5, 17.5, 5, 21.5)), line(seg(12, 17.5, 12, 21.5)),
        line(arc(16.5, 13, 5.5, -85, 95)),
        dot(16.5, 6.5, 1),
    ]


@icon("wallpaper", CAT, "Roll of patterned wallpaper partly unrolled down a wall",
      tags=["wall covering", "decorating", "redecorate", "pattern", "roll", "home improvement"])
def _(S):
    return [
        shell(rect(3, 2.5, 18, 5, rr(S, 2))),
        detail(seg(7, 3, 7, 7)),
        shell(rect(6, 9, 12, 12.5, rr(S, 1))),
        dot(9.5, 13, 1.1), dot(14.5, 13, 1.1), dot(12, 17.5, 1.1),
    ]


@icon("parquet-floor", CAT, "Wooden floor laid in a herringbone parquet pattern",
      tags=["herringbone", "hardwood floor", "wood flooring", "planks", "floorboards", "tiles"])
def _(S):
    rows = []
    for k in range(3):
        y0 = 5.6 + k * 5.4
        rows.append(detail(poly([(3, y0 + 3.4), (7.5, y0), (12, y0 + 3.4), (16.5, y0), (21, y0 + 3.4)])))
    return [shell(rect(3, 3, 18, 18, rr(S, 2))), *rows]


# ============================================================================ seats and small furniture

@icon("saddle-stool", CAT, "Stool with a saddle-shaped seat on a gas-lift column and a star base on casters",
      tags=["saddle chair", "adjustable stool", "salon stool", "dentist stool", "rolling stool", "clinic"])
def _(S):
    return [
        shell("M3 6.5C6 6.5 8 9.5 12 9.5C16 9.5 18 6.5 21 6.5C21 10 18 12.5 12 12.5C6 12.5 3 10 3 6.5Z"),
        line(seg(12, 12.5, 12, 18)),
        line(poly([(4.5, 20), (12, 18), (19.5, 20)], r=S.r)),
        dot(4.5, 21, 1.2), dot(19.5, 21, 1.2),
    ]


@icon("storage-bench", CAT, "Low bench with a padded top and two open cubbies holding shoes and a basket",
      tags=["shoe bench", "entryway bench", "hall bench", "cubby bench", "mudroom", "seat"])
def _(S):
    return [
        shell(rect(2.5, 5, 19, 4.5, rr(S, 2))),
        shell(rect(3.5, 9.5, 17, 11.5, rr(S, 1.5))),
        detail(seg(12, 10, 12, 20.5)),
        mark(poly([(5.5, 19), (5.5, 15.5), (8, 16.5), (10, 19)], closed=True)),
        mark(rect(14, 15.5, 5, 3.5)),
    ]


@icon("rocking-horse", CAT, "Wooden toy horse with a mane and tail standing on curved rockers",
      tags=["toy horse", "hobby horse", "nursery toy", "kids toy", "playroom", "ride on"])
def _(S):
    body = [(3.5, 8.5), (14, 8.5), (15, 5), (18.5, 3), (21.5, 5.5), (21, 8), (18.5, 7.5), (18, 11.5), (14, 13),
            (7, 13), (4.5, 11.5)]
    return [
        shell(poly(body, closed=True, r=S.r * 0.6)),
        line(seg(6.5, 13, 5.5, 18)), line(seg(14.5, 13, 15.5, 18)),
        line("M2.5 18.5Q12 23.5 21.5 18.5"),
        dot(19.3, 5.3, 0.8),
    ]


@icon("folding-stool", CAT, "Small stool with a fabric seat stretched across two crossed X-shaped legs",
      tags=["camp stool", "portable stool", "fold up seat", "camping", "fishing stool", "seat"])
def _(S):
    return [
        shell(rect(4, 5.5, 16, 3.5, rr(S, 1.75))),
        line(seg(6.5, 9, 17.5, 21)),
        line(seg(17.5, 9, 6.5, 21)),
    ]


@icon("auditorium-seats", CAT, "Row of three joined theater seats with armrests and the middle seat folded up",
      tags=["theatre seats", "cinema seats", "stadium seating", "lecture hall", "tip up seat", "audience"])
def _(S):
    return [
        shell(rect(3, 3, 18, 9, rr(S, 2))),
        detail(seg(9, 3.5, 9, 11.5)), detail(seg(15, 3.5, 15, 11.5)),
        shell(rect(3.5, 14.5, 5, 3.5, rr(S, 1.5))),
        shell(rect(10.5, 13.5, 3, 5.5, rr(S, 1))),
        shell(rect(15.5, 14.5, 5, 3.5, rr(S, 1.5))),
        line(seg(2.5, 21, 21.5, 21)),
    ]


@icon("baby-bouncer", CAT, "Low reclined baby seat on a curved wire frame with a toy bar arching over it",
      tags=["baby seat", "infant rocker", "bouncy chair", "baby chair", "newborn", "nursery"])
def _(S):
    return [
        shell("M4.5 6L8 5.5C10 9.5 13 12 19 13.5V17.5H8.5C5.5 17.5 4 12.5 4.5 6Z"),
        line("M3 19.5Q12 24 21 19.5"),
        line("M10 4.5C13 1 20 3 21 10"),
        dot(17, 4.6, 1.2),
    ]


@icon("ball-chair", CAT, "Large exercise ball sitting in a low frame on casters with a short backrest",
      tags=["yoga ball chair", "balance chair", "stability ball", "active sitting", "office chair", "fitness"])
def _(S):
    return [
        shell(circle(10.5, 10.5, 7)),
        line(poly([(21, 5), (21, 14), (18, 17)], r=S.r)),
        line(seg(3.5, 19.5, 20.5, 19.5)),
        line(seg(5, 19.5, 5, 21.5)), line(seg(19, 19.5, 19, 21.5)),
    ]


@icon("tray-table", CAT, "Small folding table with a rimmed tray top on tall crossed X legs",
      tags=["butler tray", "serving table", "snack table", "bed tray", "folding tray", "side table"])
def _(S):
    return [
        line(poly([(3, 4), (3, 8.5), (21, 8.5), (21, 4)], r=S.r)),
        line(seg(7, 8.5, 17, 21)),
        line(seg(17, 8.5, 7, 21)),
    ]


@icon("washstand", CAT, "Antique stand with a basin and a water jug on top and a shelf below",
      tags=["wash basin stand", "vanity stand", "jug and bowl", "antique", "ewer", "bathroom"])
def _(S):
    return [
        shell("M3.5 5.5H12.5C12.5 8.5 10.5 9.5 8 9.5C5.5 9.5 3.5 8.5 3.5 5.5Z"),
        shell("M15.5 9.5C15 7 16 6 16.5 3.5H19.5C20 6 21 7 20.5 9.5Z"),
        shell(rect(2.5, 10.5, 19, 2.5, rr(S, 1.25))),
        line(seg(4.5, 13, 4.5, 21.5)), line(seg(19.5, 13, 19.5, 21.5)),
        shell(rect(4.5, 17, 15, 2.5, rr(S, 1.25))),
    ]


@icon("floor-table", CAT, "Very low table with short legs and a square floor cushion on each side",
      tags=["low table", "japanese table", "chabudai", "floor seating", "cushions", "tea table"])
def _(S):
    return [
        shell(rect(8, 9.5, 8, 3, rr(S, 1.5))),
        line(seg(9.5, 12.5, 9.5, 20)), line(seg(14.5, 12.5, 14.5, 20)),
        shell(rect(2, 14.5, 4, 5.5, rr(S, 1.5))),
        shell(rect(18, 14.5, 4, 5.5, rr(S, 1.5))),
        line(seg(2, 21.5, 22, 21.5)),
    ]


@icon("apothecary-cabinet", CAT, "Cabinet front divided into a grid of small drawers, each with a tiny knob",
      tags=["drawer cabinet", "chinese medicine cabinet", "spice drawers", "card catalog", "small drawers", "chest"])
def _(S):
    parts = [shell(rect(3, 3, 18, 18, rr(S, 2))),
             detail(seg(9, 3.5, 9, 20.5)), detail(seg(15, 3.5, 15, 20.5)),
             detail(seg(3.5, 9, 20.5, 9)), detail(seg(3.5, 15, 20.5, 15))]
    for x in (6, 12, 18):
        for y in (6, 12, 18):
            parts.append(dot(x, y, 0.9))
    return parts


# ============================================================================ lighting and soft furnishings

@icon("cluster-pendant", CAT, "Three globe bulbs hanging from one ceiling canopy on cords of different lengths",
      tags=["pendant lights", "globe lights", "hanging lamps", "chandelier", "ceiling light", "bulbs"])
def _(S):
    return [
        shell(rect(9.5, 2, 5, 2.5, rr(S, 1.25))),
        line(seg(12, 4, 6, 7)), line(seg(12, 4, 12, 13)), line(seg(12, 4, 18, 9.5)),
        shell(circle(6, 10, 3)), shell(circle(12, 16.5, 3)), shell(circle(18, 12.5, 3)),
    ]


@icon("linear-pendant", CAT, "Long slim bar light hung from two thin wires, lighting the table below it",
      tags=["bar light", "kitchen island light", "billiard light", "suspended light", "dining light", "ceiling lamp"])
def _(S):
    return [
        line(seg(6, 2.5, 6, 7)), line(seg(18, 2.5, 18, 7)),
        shell(rect(2.5, 7.5, 19, 3.5, rr(S, 1.75))),
        line(seg(8, 14, 8, 16.5)), line(seg(12, 14, 12, 16.5)), line(seg(16, 14, 16, 16.5)),
        line(seg(3, 21, 21, 21)),
    ]


def sparkle(cx, cy, r=2.2):
    k = r * 0.35
    return solid(poly([(cx, cy - r), (cx + k, cy - k), (cx + r, cy), (cx + k, cy + k), (cx, cy + r),
                       (cx - k, cy + k), (cx - r, cy), (cx - k, cy - k)], closed=True))


@icon("star-projector", CAT, "Small dome night light throwing star shapes onto the space around it",
      tags=["night light", "galaxy projector", "starry sky", "constellation lamp", "kids room", "bedtime"])
def _(S):
    return [
        shell("M6 20.5C6 15 8.5 12.5 12 12.5C15.5 12.5 18 15 18 20.5Z"),
        sparkle(12, 4.5, 2.4), sparkle(4.5, 9, 2), sparkle(19.5, 8, 2),
        sparkle(4, 17, 1.6), sparkle(20, 17, 1.6),
    ]


@icon("lamp-post", CAT, "Classic post lamp with a lantern head on a tall pole and a flared base",
      tags=["street lamp", "garden lamp", "lantern post", "lamppost", "park light", "outdoor light"])
def _(S):
    return [
        shell(poly([(7, 6.5), (12, 2.5), (17, 6.5)], closed=True, r=S.r * 0.6)),
        shell(rect(8.5, 7.5, 7, 6, rr(S, 1.5))),
        line(seg(12, 13.5, 12, 19)),
        shell(poly([(9.5, 19), (14.5, 19), (17.5, 21.5), (6.5, 21.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("half-moon-rug", CAT, "Semicircular rug with a flat back edge, a patterned border and fringe",
      tags=["semicircle rug", "door mat", "carpet", "floor covering", "runner", "hall rug"])
def _(S):
    return [
        shell("M2.5 17.5H21.5A9.5 9.5 0 0 0 2.5 17.5Z"),
        detail("M7 17.5A5 5 0 0 1 17 17.5"),
        dot(12, 13.5, 1.2),
        line(seg(4.5, 18.5, 4.5, 21.5)), line(seg(9.5, 18.5, 9.5, 21.5)),
        line(seg(14.5, 18.5, 14.5, 21.5)), line(seg(19.5, 18.5, 19.5, 21.5)),
    ]


@icon("window-valance", CAT, "Short gathered fabric panel across the top of a window above the glass",
      tags=["curtain valance", "pelmet", "window treatment", "swag", "drapery", "curtains"])
def _(S):
    return [
        shell("M3 3.5H21V9Q18 13 15 9Q12 13 9 9Q6 13 3 9Z"),
        detail(seg(7.5, 4.5, 7.5, 8)), detail(seg(12, 4.5, 12, 9)), detail(seg(16.5, 4.5, 16.5, 8)),
        shell(rect(5, 15, 14, 6.5, rr(S, 1.5))),
        detail(seg(12, 15.5, 12, 21)),
    ]
