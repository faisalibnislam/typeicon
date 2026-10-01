"""TypeIcon Core: kids (batch 004).

Toys, crafts, baby gear, school bits and playground games. Figures follow the people and activities sets
(head dot r 2.25, 2 px limbs). Overlapping objects are drawn in layers (front first): back layers are cut
away around the front silhouette with a gap in every style so small scenes stay readable at 16 px.
"""
import math

from dsl import LINE, Part, arc, circle, detail, dot, ellipse, icon, line, poly, rect, regular, seg, shell, solid  # noqa: F401
from dsl import D, P, ST, U, filled_region
from geometry import fmt, path_to_d, polar

CAT = "kids"


# --------------------------------------------------------------------------- helpers

def pick(S, a, b):
    """Line value, Rounded value."""
    return a if S.name == "line" else b


def sq(x, y, w, h, rx=0.0) -> Part:
    """Small solid rectangle: solid in Line/Rounded, knocked out of a Filled shell."""
    return Part("dot", rect(x, y, w, h, rx))


def mark(d) -> Part:
    """Small solid mark of any shape (knocked out of a Filled shell)."""
    return Part("dot", d)


def cap(x0, y0, x1, y1, w=3.4):
    """Capsule region along a segment."""
    return ST(seg(x0, y0, x1, y1), w, "round", "round")


def bar(x0, y0, x1, y1, w=3.0):
    """Square-ended strip region along a segment."""
    return ST(seg(x0, y0, x1, y1), w, "butt", "miter")


def box(x, y, w, h, r=0.0):
    return P(rect(x, y, w, h, r))


def outline(*regions, **attrs):
    return shell(path_to_d(U(*regions)), **attrs)


def minus(a, *bs):
    return path_to_d(D(a, *bs))


def drop(cx, top, r):
    """Water drop: pointed top, round bottom of radius r."""
    cy = top + r * 2.2
    a = polar(cx, cy, r, -150)
    b = polar(cx, cy, r, -30)
    return (f"M{fmt(cx)} {fmt(top)}L{fmt(b[0])} {fmt(b[1])}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(a[0])} {fmt(a[1])}Z")


def star_pts(cx, cy, ro, ri, n=5, start=-90.0):
    pts = []
    for i in range(2 * n):
        rr = ro if i % 2 == 0 else ri
        pts.append(polar(cx, cy, rr, start + i * 180 / n))
    return pts


def tilted_ellipse(cx, cy, rx, ry, deg):
    """Ellipse whose ry axis points along deg (0 = right, 90 = down)."""
    a = math.radians(deg)
    ux, uy = math.cos(a), math.sin(a)
    p1 = (cx + ry * ux, cy + ry * uy)
    p2 = (cx - ry * ux, cy - ry * uy)
    return (f"M{fmt(p1[0])} {fmt(p1[1])}A{fmt(ry)} {fmt(rx)} {fmt(deg)} 1 0 {fmt(p2[0])} {fmt(p2[1])}"
            f"A{fmt(ry)} {fmt(rx)} {fmt(deg)} 1 0 {fmt(p1[0])} {fmt(p1[1])}Z")


def gear(cx, cy, ro, ri, n, S, frac=0.5):
    """Toothed gear outline: n teeth between radius ri (root) and ro (tip)."""
    pts = []
    step = 360 / n
    tw = step * frac / 2
    for i in range(n):
        a = -90 + i * step
        pts += [polar(cx, cy, ri, a - tw - step * 0.12), polar(cx, cy, ro, a - tw * 0.8),
                polar(cx, cy, ro, a + tw * 0.8), polar(cx, cy, ri, a + tw + step * 0.12)]
    return poly(pts, closed=True, r=S.r * 0.25)


# ---- layering: back parts are cut away around the front silhouette (all styles)

def _paint(parts, S):
    regs = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        else:
            regs.append(ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4))))
    return U(*regs)


def _sil(parts, S):
    regs = []
    for p in parts:
        if p.kind in ("dot", "solid"):
            regs.append(P(p.d))
        elif p.kind == "shell":
            regs.append(U(P(p.d), ST(p.d, 2.0, S.cap, S.join, float(p.attrs.get("stroke_miterlimit", 4)))))
        else:
            regs.append(ST(p.d, 2.0, S.cap, S.join))
    return U(*regs)


def _grow(region, g):
    if g <= 0:
        return region
    return U(region, ST(path_to_d(region), 2 * g, "round", "round"))


def _stroke_layers(S, layers, gap):
    out = list(layers[0])
    cover = _grow(_sil(layers[0], S), gap)
    for layer in layers[1:]:
        if not layer:
            continue
        vis = D(_paint(layer, S), cover)
        if abs(vis.area) > 0.01:
            out.append(solid(path_to_d(vis)))
        cover = U(cover, _grow(_sil(layer, S), gap))
    return out


def _filled_layers(layers, gap):
    result = filled_region(layers[0])
    cover = _grow(result, gap)
    for layer in layers[1:]:
        if not layer:
            continue
        f = filled_region(layer)
        result = U(result, D(f, cover))
        cover = U(cover, _grow(f, gap))
    return result


def scene(name, desc, tags, aliases=(), gap=1.5):
    """Register an icon drawn as layers: fn(S) -> [front layer, layer behind, ...]."""
    def deco(fn):
        icon(name, CAT, desc, tags=tags, aliases=aliases,
             filled=lambda: _filled_layers(fn(LINE), gap))(lambda S: _stroke_layers(S, fn(S), gap))
        return fn
    return deco


# ============================================================================ chunk 1

@icon("umbrella-stroller", CAT, "A lightweight folding stroller in side view with a hooked handle and small wheels.",
      tags=["stroller", "buggy", "pushchair", "baby", "travel", "folding"])
def _(S):
    return [
        line("M3.5 5.5A1.75 1.75 0 0 1 7 5.5L17 19"),
        line(seg(12, 12, 7.5, 19)),
        line(poly([(7.5, 9), (9.5, 14.5), (16.5, 14.5)], r=S.r)),
        shell(circle(6.5, 20, 1.75)),
        shell(circle(17.5, 20, 1.75)),
    ]


@scene("bath-visor", "A small face wearing a wide ring brim that keeps bath water out of the eyes.",
       tags=["bath visor", "shampoo shield", "bath time", "hair wash", "baby", "toddler"])
def _(S):
    brim = [shell(ellipse(12, 8.5, 10, 2.75))]
    drops = [mark(drop(4.5, 1.5, 1.1)), mark(drop(19.5, 1.5, 1.1))]
    face = [shell(circle(12, 14, 6.5)), dot(9.5, 15, 1.1), dot(14.5, 15, 1.1), detail(arc(12, 16, 2.5, 30, 150))]
    return [brim + drops, face]


@icon("spiral-drawing-gears", CAT, "A toothed gear with pen holes rolling inside a drawing ring, used for spiral pattern art.",
      tags=["spiral art", "drawing gears", "pattern drawing", "craft", "art toy", "geometric"])
def _(S):
    return [
        line(circle(12, 12, 9.5)),
        shell(gear(13, 13, 5.6, 3.9, 6, S, 0.5)),
        dot(11.2, 11.8, 1.1),
        dot(14.8, 14.2, 1.1),
    ]


@icon("bubble-machine", CAT, "A small box with a fan grille on the front blowing out a stream of bubbles.",
      tags=["bubbles", "bubble blower", "party", "garden toy", "outdoor play", "fan"])
def _(S):
    return [
        shell(rect(2.5, 11, 11, 10, min(S.R, 3))),
        detail(circle(8, 16, 2.5)),
        line(poly([(5.5, 11), (5.5, 8.5), (10.5, 8.5), (10.5, 11)], r=S.r * 0.6)),
        line(circle(17.5, 12, 2.5)),
        line(circle(19.5, 5, 2)),
        line(circle(13.5, 4.5, 1.5)),
    ]


@icon("jumping-jack-toy", CAT, "A flat jointed puppet with arms and legs raised and a pull string hanging below.",
      tags=["jumping jack", "pull string puppet", "wooden toy", "jointed toy", "puppet", "traditional toy"])
def _(S):
    return [
        shell(circle(12, 4.5, 2.5)),
        shell(rect(9.5, 8.5, 5, 6.5, min(S.R, 1.5))),
        line(poly([(9.5, 10), (4, 5), (3, 6.5)], r=S.r * 0.5)),
        line(poly([(14.5, 10), (20, 5), (21, 6.5)], r=S.r * 0.5)),
        line(poly([(10.5, 15), (5.5, 18), (5, 20)], r=S.r * 0.5)),
        line(poly([(13.5, 15), (18.5, 18), (19, 20)], r=S.r * 0.5)),
        line(seg(12, 15, 12, 19)),
        dot(12, 21, 1.5),
    ]


@scene("water-slide-mat", "A child sliding belly first along a long wet mat with water drops above.",
       tags=["slip and slide", "water slide", "summer", "garden play", "sprinkler", "splash"])
def _(S):
    mat = [shell(rect(2, 18, 20, 3.5, min(S.R, 1.75)))]
    kid = [dot(5, 13.5, 2.25),
           line(seg(8.5, 14.5, 15, 15.5)),
           line(poly([(15, 15.5), (18.5, 13.5), (21, 14)], r=S.r * 0.5)),
           line(seg(8.5, 14.5, 7, 11))]
    drops = [mark(drop(9, 3, 1.3)), mark(drop(14, 5, 1.3)), mark(drop(19, 3, 1.3))]
    return [kid, mat + drops]


@icon("hall-pass", CAT, "A wooden paddle pass with a short handle and a door symbol on its face.",
      tags=["hall pass", "bathroom pass", "school", "permission", "classroom", "corridor"])
def _(S):
    return [
        outline(P(rect(4.5, 2.5, 15, 12.5, min(S.R, 3))), P(rect(9.5, 13, 5, 8.5, min(S.R, 1.5)))),
        detail(poly([(9.5, 15), (9.5, 6), (14.5, 6), (14.5, 15)], r=S.r * 0.4)),
        dot(13, 10.5, 0.9),
    ]


@icon("alphabet-poster", CAT, "A classroom wall poster with a large letter A, a small apple and rows of letters.",
      tags=["alphabet", "abc", "letters", "classroom poster", "phonics", "learning to read"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 17, 19, min(S.R, 3))),
        detail(poly([(6.5, 12), (9, 5.5), (11.5, 12)], r=S.r * 0.3)),
        detail(seg(7.7, 9.5, 10.3, 9.5)),
        mark(circle(16, 9.5, 2.5)),
        detail(seg(16, 5.5, 17, 5)),
        detail(seg(7, 15.5, 17, 15.5)),
        detail(seg(7, 18.5, 13, 18.5)),
    ]


@icon("magnetic-letters", CAT, "Chunky magnetic letters A and B stuck on a fridge door beside its handle.",
      tags=["fridge magnets", "alphabet magnets", "letters", "spelling", "abc", "learning"])
def _(S):
    return [
        shell(rect(3, 2, 18, 20, min(S.R, 3))),
        detail(seg(6.5, 5, 6.5, 9)),
        detail(poly([(6.5, 19), (9, 12), (11.5, 19)], r=S.r * 0.3)),
        detail(seg(7.6, 16.5, 10.4, 16.5)),
        detail(pick(S, "M14.5 12H16.8A1.75 1.75 0 0 1 16.8 15.5H14.5M14.5 15.5H17A1.75 1.75 0 0 1 17 19H14.5V12",
                    "M14.5 19V12H16.8A1.75 1.75 0 0 1 16.8 15.5H14.5M14.5 15.5H17A1.75 1.75 0 0 1 17 19H14.5")),
    ]


@scene("tummy-time", "A baby lying on its belly on a mat, pushing up on its arms and lifting its head.",
       tags=["tummy time", "baby development", "infant", "play mat", "newborn", "milestone"])
def _(S):
    baby = [shell(circle(6.5, 9, 3.25)),
            outline(cap(11, 15, 18.5, 17.5, 5)),
            line(poly([(20.5, 18), (21.5, 13.5)], r=S.r)),
            line(poly([(9.5, 13), (9, 18), (5, 18)], r=S.r))]
    mat = [line(seg(2, 21.5, 22, 21.5))]
    return [baby, mat]


@scene("construction-kit", "Two perforated metal strips bolted together at an angle, from a building set.",
       tags=["building set", "metal construction toy", "nuts and bolts", "engineering", "stem", "model building"])
def _(S):
    k = cap if S.name != "line" else bar
    front = [outline(k(3.5, 17.5, 20.5, 17.5, 5))] + [dot(x, 17.5, 0.9) for x in (6, 10, 14, 18)]
    back = [outline(k(6, 15, 16.5, 4.5, 5))] + [dot(x, y, 0.9) for x, y in ((12.5, 8), (15.5, 5))]
    return [front, back]


@icon("merit-badge", CAT, "A round embroidered patch with a stitched border and a small tent in the middle.",
      tags=["merit badge", "scout badge", "patch", "achievement", "award", "camping"])
def _(S):
    stitches = [detail(arc(12, 12, 7, a, a + 16)) for a in range(0, 360, 30)]
    return [shell(circle(12, 12, 9.5))] + stitches + [
        detail(poly([(8.5, 15), (12, 8.8), (15.5, 15)], closed=True, r=S.r * 0.3)),
    ]


@icon("window-guard", CAT, "A window with vertical safety bars fitted across its lower half.",
      tags=["window guard", "window bars", "child safety", "fall prevention", "babyproofing", "childproof"])
def _(S):
    return [
        shell(rect(3, 2, 18, 20, min(S.R, 3))),
        detail(seg(3, 10, 21, 10)),
        detail(seg(3, 13.5, 21, 13.5)),
        detail(seg(8, 13.5, 8, 22)),
        detail(seg(12, 13.5, 12, 22)),
        detail(seg(16, 13.5, 16, 22)),
    ]


@scene("door-pinch-guard", "A door held ajar by a C shaped foam guard clipped over its edge.",
       tags=["door stopper", "finger pinch guard", "childproofing", "babyproofing", "door guard", "safety"])
def _(S):
    c = cap if S.name != "line" else bar
    k = "round" if S.name != "line" else "butt"
    guard = [outline(ST(arc(14.5, 11, 3.6, -135, 135), 3.2, k, "miter"))]
    door = [shell(rect(2.5, 2, 9, 20, min(S.R, 1.5))), dot(5.5, 12, 1.1)]
    jamb = [line(seg(21, 2, 21, 22))]
    return [guard, door, jamb]


# ============================================================================ chunk 2

@icon("play-tent", CAT, "A house shaped play tent with a triangular doorway flap and a pennant flag on top.",
      tags=["play tent", "playhouse", "indoor tent", "indoor play", "den", "hideout"])
def _(S):
    return [
        shell(poly([(4.5, 21.5), (4.5, 13.5), (2.5, 14.5), (12, 6.5), (21.5, 14.5), (19.5, 13.5), (19.5, 21.5)],
                   closed=True, r=S.r * 0.5)),
        detail(poly([(8.5, 21.5), (12, 13.5), (15.5, 21.5)], r=S.r * 0.4)),
        line(seg(12, 6.5, 12, 2)),
        solid(poly([(12.5, 2), (17, 3.5), (12.5, 5)], closed=True, r=S.r * 0.2)),
    ]


@scene("gear-board", "Three interlocking toy gears of different sizes, the largest turned by a crank handle.",
       tags=["gear toy", "gears", "cogs", "stem toy", "cause and effect", "busy board", "crank"])
def _(S):
    big = [shell(gear(8.5, 15, 6.5, 4.6, 7, S, 0.5)), detail(seg(8.5, 15, 8.5, 11.5)), dot(8.5, 15, 1.2)]
    mid = [shell(gear(17, 6.5, 4.8, 3.3, 6, S, 0.5))]
    small = [shell(gear(18.5, 18, 3.6, 2.4, 5, S, 0.55))]
    return [big, mid, small]


@scene("paper-helicopter", "A paper strip with two blades bent in opposite directions, a paper clip weight and a spin arrow.",
       tags=["paper helicopter", "paper spinner", "whirligig", "science experiment", "craft", "falling"])
def _(S):
    clip = [line("M11 17V20.5A1.5 1.5 0 0 0 14 20.5V18")]
    body = [shell(rect(10, 9.5, 4, 10, min(S.R, 1))),
            shell(poly([(10, 9.5), (2.5, 11), (2.5, 13.5), (10, 12)], closed=True, r=S.r * 0.4)),
            shell(poly([(14, 9.5), (21.5, 8), (21.5, 10.5), (14, 12)], closed=True, r=S.r * 0.4)),
            line(arc(12, 8.5, 6, 205, 320)),
            solid(poly([(19.1, 5.3), (16, 6.2), (18.3, 2.9)], closed=True))]
    return [clip, body]


@scene("magic-hat", "An upturned top hat with rabbit ears popping out and a magic wand beside the brim.",
       tags=["magic trick", "magician", "rabbit in hat", "top hat", "conjuring", "magic show", "illusion"])
def _(S):
    brim = [shell(ellipse(11, 12, 8.5, 2))]
    wand = [line(seg(16.5, 9.5, 21.5, 4)), solid(circle(21.5, 4, 1.5))]
    back = [shell(poly([(5.5, 12), (16.5, 12), (15, 21.5), (7, 21.5)], closed=True, r=S.r)),
            shell(tilted_ellipse(8.5, 6.5, 1.8, 4.5, -80)),
            shell(tilted_ellipse(13, 6.5, 1.8, 4.5, -100))]
    return [brim, wand, back]


@icon("pregnancy-pillow", CAT, "A long U shaped body pillow seen from above with a seam along its middle.",
      tags=["pregnancy pillow", "maternity pillow", "body pillow", "u pillow", "sleep", "bump support"])
def _(S):
    u = "M6.5 5.5V14A5.5 5.5 0 0 0 17.5 14V5.5"
    body = U(ST(u, 7, "round", "round"))
    return [shell(path_to_d(body)), detail(pick(S, "M6.5 7V14A5.5 5.5 0 0 0 17.5 14V7", u))]


@icon("toddler-sleep-trainer", CAT, "A rounded bedside clock with a sleeping face and a small moon, standing on short legs.",
      tags=["sleep trainer", "okay to wake clock", "toddler clock", "bedtime", "night", "sleep routine"])
def _(S):
    return [
        shell(rect(3, 3, 18, 15, pick(S, 4, 6.5))),
        detail(arc(8.5, 10.5, 1.8, 20, 160)),
        detail(arc(15.5, 10.5, 1.8, 20, 160)),
        detail(arc(12, 13, 1.5, 30, 150)),
        mark("M13.2 5.6A2 2 0 1 0 13.2 8.4A1.6 1.6 0 1 1 13.2 5.6Z"),
        line(seg(7, 18, 6, 21.5)),
        line(seg(17, 18, 18, 21.5)),
    ]


@icon("bedside-crib", CAT, "A small barred crib attached level with the side of an adult bed.",
      tags=["bedside crib", "co sleeper", "bedside sleeper", "bassinet", "newborn", "baby bed"])
def _(S):
    return [
        line(seg(2.5, 8, 2.5, 21.5)),
        shell(rect(2.5, 13, 11, 3.5, min(S.R, 1.5))),
        shell(rect(4.5, 9.5, 5, 3.5, min(S.R, 1.5))),
        line(seg(12, 16.5, 12, 21.5)),
        shell(rect(15, 13, 6.5, 3.5, min(S.R, 1.5))),
        line(poly([(15, 13), (15, 6.5), (21.5, 6.5), (21.5, 13)], r=S.r)),
        line(seg(18.25, 6.5, 18.25, 13)),
        line(seg(18.25, 16.5, 18.25, 21.5)),
    ]


@scene("leaf-rubbing", "A sheet of paper with a leaf pattern rubbed onto it and a crayon lying across.",
       tags=["leaf rubbing", "crayon rubbing", "nature craft", "texture art", "autumn craft", "outdoor learning"])
def _(S):
    crayon = [shell(poly([(11.5, 19.5), (18, 13), (20.5, 15.5), (14, 22)], closed=True, r=S.r * 0.4)),
              solid(poly([(18.8, 12.2), (21.8, 11.2), (21.3, 14.2)], closed=True))]
    paper = [shell(rect(2.5, 2.5, 13.5, 17.5, min(S.R, 2))),
             detail("M6 15.5C5.5 10.5 8 6.5 12.5 5C13 10 11 14 6 15.5Z"),
             detail(seg(6, 15.5, 10.5, 8.5))]
    return [crayon, paper]


@icon("potato-stamp", CAT, "Half a potato with a star carved into its cut face and two stamped stars beside it.",
      tags=["potato print", "potato stamp", "stamping", "printing craft", "vegetable print", "art"])
def _(S):
    return [
        shell(tilted_ellipse(9, 13, 6.5, 8, -15)),
        detail(poly(star_pts(9, 13, 4, 1.8), closed=True, r=S.r * 0.2)),
        solid(poly(star_pts(19.5, 6, 2.6, 1.15), closed=True, r=S.r * 0.15)),
        solid(poly(star_pts(19.5, 16, 2.6, 1.15), closed=True, r=S.r * 0.15)),
    ]


@icon("paper-plate-mask", CAT, "A round paper plate mask with a fluted rim, two eye holes, a smile and a stick handle.",
      tags=["paper plate mask", "craft mask", "dress up", "kids craft", "face mask craft", "pretend play"])
def _(S):
    n = 16
    bumps = [P(circle(*polar(11, 10, 7.2, i * 360 / n), 1.4)) for i in range(n)]
    plate = U(P(circle(11, 10, 7.2)), *bumps)
    return [
        shell(path_to_d(plate)),
        dot(8.3, 8.8, 1.4), dot(13.7, 8.8, 1.4),
        detail(arc(11, 10.5, 3.5, 30, 150)),
        line(seg(16.5, 17, 20.5, 21.5)),
    ]


@scene("scratch-art", "A dark scratch card with rainbow lines scratched into it and a wooden stylus.",
       tags=["scratch art", "scratch paper", "scratchboard", "rainbow paper", "kids craft", "drawing"])
def _(S):
    stylus = [line(seg(13.5, 13, 21.5, 21)), solid(poly([(12, 11.5), (14.8, 12.6), (12.6, 14.8)], closed=True))]
    card = [shell(rect(2.5, 3, 16, 16, min(S.R, 3))),
            detail(arc(10.5, 19, 9, 205, 290)),
            detail(arc(10.5, 19, 5, 190, 300))]
    return [stylus, card]


@icon("calm-down-jar", CAT, "A sealed bottle of water with glitter specks swirling inside.",
      tags=["calm down jar", "glitter jar", "sensory bottle", "mindfulness", "calm", "emotions", "time out"])
def _(S):
    return [
        shell(rect(8.5, 2, 7, 3, min(S.R, 1))),
        shell(rect(5.5, 6.5, 13, 15.5, pick(S, 3, 5))),
        detail("M5.5 10.5C8 9 10 12 12.5 10.5S16 9.5 18.5 10.5"),
        dot(9, 14.5, 1), dot(14.5, 13.5, 1), dot(12, 17.5, 1), dot(15.5, 18.5, 0.9), dot(8.5, 19, 0.9),
    ]


@icon("visual-schedule", CAT, "A vertical strip of picture cards with check marks beside the finished ones.",
      tags=["visual schedule", "picture schedule", "daily routine", "first then", "autism support", "routine chart"])
def _(S):
    rr = min(S.R, 1.5)
    return [
        shell(rect(3, 2.5, 10, 5, rr)), mark(circle(8, 5, 1.3)),
        shell(rect(3, 9.5, 10, 5, rr)), mark(poly([(6.5, 13.3), (8, 10.7), (9.5, 13.3)], closed=True)),
        shell(rect(3, 16.5, 10, 5, rr)), sq(6.8, 17.8, 2.4, 2.4, pick(S, 0, 0.6)),
        line(poly([(15.5, 5), (17.2, 6.7), (21, 3)], r=S.r * 0.4)),
        line(poly([(15.5, 12), (17.2, 13.7), (21, 10)], r=S.r * 0.4)),
        line(seg(16, 19, 20.5, 19)),
    ]


# ============================================================================ chunk 3

def cyl(x, w, top, bottom, ry=1.75):
    """Upright cylinder outline (stump, soft block): straight sides, round top and bottom."""
    rx = w / 2
    cx = x + rx
    return (f"M{fmt(x)} {fmt(top)}A{fmt(rx)} {fmt(ry)} 0 0 1 {fmt(x + w)} {fmt(top)}V{fmt(bottom)}"
            f"A{fmt(rx)} {fmt(ry)} 0 0 1 {fmt(x)} {fmt(bottom)}Z"), f"M{fmt(x)} {fmt(top)}A{fmt(rx)} {fmt(ry)} 0 0 0 {fmt(x + w)} {fmt(top)}", cx


@scene("tube-slide", "An enclosed tube slide curving down from a platform to an open end at the bottom.",
       tags=["tube slide", "tunnel slide", "enclosed slide", "playground", "play area", "slide"])
def _(S):
    path = "M8 10C14 10 13.5 18.5 18.5 18.5"
    tube = [shell(path_to_d(ST(path, 5.5, "butt", "miter"))), shell(ellipse(19.5, 18.5, 1.75, 2.75))]
    tower = [line(seg(3.5, 5, 3.5, 21.5)), line(seg(8, 12.5, 8, 21.5)), line(seg(2.5, 7.5, 8, 7.5)),
             line(poly([(2.5, 4), (5.75, 2), (9, 4)], r=S.r * 0.5))]
    return [tube, tower]


@icon("pass-the-parcel", CAT, "A wrapped parcel with a ribbon and bow and a music note beside it, for the party game.",
      tags=["pass the parcel", "party game", "birthday party", "musical game", "wrapped gift", "layers"])
def _(S):
    return [
        shell(rect(3, 11, 12, 10.5, min(S.R, 2))),
        shell(rect(2, 8, 14, 3, min(S.R, 1))),
        detail(seg(9, 8, 9, 21.5)),
        line("M9 8C7 4 3.5 5 5.5 8M9 8C11 4 14.5 5 12.5 8"),
        line(poly([(21, 13), (21, 4), (22, 5.5)], r=S.r * 0.3)),
        dot(19.3, 13.5, 2),
    ]


@icon("birthday-badge", CAT, "A round rosette badge with two ribbon tails and a number 5 in the middle.",
      tags=["birthday badge", "birthday rosette", "age badge", "birthday boy", "birthday girl", "party"])
def _(S):
    n = 14
    bumps = [P(circle(*polar(12, 9, 6.2, i * 360 / n), 1.6)) for i in range(n)]
    rosette = U(P(circle(12, 9, 6.2)), *bumps)
    k = S.r * 0.3
    return [
        shell(path_to_d(rosette)),
        detail(pick(S, "M14 5.8H10.8L10.4 9.2C11.2 8.6 14.2 8.4 14.2 10.7C14.2 12.9 11.3 13 10.3 12",
                    "M14 5.8H10.8L10.4 9.2C11.2 8.6 14.2 8.4 14.2 10.7C14.2 12.9 11.3 13 10.3 12")),
        shell(poly([(8, 16), (5.5, 21.5), (7.5, 20.5), (8.5, 22), (10.5, 17)], closed=True, r=k)),
        shell(poly([(16, 16), (18.5, 21.5), (16.5, 20.5), (15.5, 22), (13.5, 17)], closed=True, r=k)),
    ]


@icon("leapfrog", CAT, "A child leaping with legs spread wide over another child crouching below.",
      tags=["leapfrog", "leap frog", "playground game", "jumping", "vaulting", "kids game"])
def _(S):
    return [
        shell("M5 21.5A7 6 0 0 1 19 21.5Z"),
        dot(12, 3, 2.25),
        line(seg(12, 6.5, 12, 10)),
        line(poly([(8.5, 13.5), (12, 7), (15.5, 13.5)], r=S.r)),
        line(poly([(3, 7), (12, 10), (21, 7)], r=S.r)),
    ]


@scene("double-dutch", "A jumper in mid air between two jump ropes swinging in opposite arcs.",
       tags=["double dutch", "jump rope", "skipping rope", "skipping", "playground game", "rope jumping"])
def _(S):
    kid = [dot(12, 6.5, 2.25),
           line(seg(12, 9.5, 12, 13.5)),
           line(poly([(8.5, 8.5), (12, 10.5), (15.5, 8.5)], r=S.r * 0.5)),
           line(poly([(12, 13.5), (9.5, 15), (10.5, 17.5)], r=S.r * 0.5)),
           line(poly([(12, 13.5), (14.5, 15), (13.5, 17.5)], r=S.r * 0.5))]
    ropes = [line("M2.5 13C4 2 20 2 21.5 13"), line("M2.5 11C4 23 20 23 21.5 11")]
    return [kid, ropes]


@scene("soft-play-blocks", "A padded cube, a wedge and a cylinder grouped together as soft play shapes.",
       tags=["soft play", "foam blocks", "soft blocks", "toddler play", "climbing shapes", "play gym"])
def _(S):
    body, top, _ = cyl(4, 8, 4, 9.5, 1.5)
    rr = pick(S, 1.5, 3)
    return [[shell(rect(2.5, 12.5, 9, 9, rr)),
             shell(poly([(13.5, 21.5), (21.5, 21.5), (21.5, 12.5)], closed=True, r=pick(S, 0.5, 2)))],
            [shell(body), detail(top)]]


@scene("rolling-backpack", "A school backpack with a pull up trolley handle and two small wheels.",
       tags=["rolling backpack", "trolley bag", "wheeled backpack", "school bag", "back to school", "luggage"])
def _(S):
    body = ("M5 17V12A7 7 0 0 1 19 12V17Z" if S.name == "line" else
            "M5 15V12A7 7 0 0 1 19 12V15A2 2 0 0 1 17 17H7A2 2 0 0 1 5 15Z")
    bag = [shell(body), detail(poly([(8, 17), (8, 13), (16, 13), (16, 17)], r=S.r * 0.5)),
           mark(circle(8, 20.4, 1.6)), mark(circle(16, 20.4, 1.6))]
    handle = [line(poly([(6.5, 9), (6.5, 2.5), (17.5, 2.5), (17.5, 9)], r=S.r))]
    return [bag, handle]


@scene("lost-and-found-box", "An open box with a question mark on the front and a mitten and a cap sticking out.",
       tags=["lost and found", "lost property", "found items", "school office", "missing items", "box"])
def _(S):
    box_ = [shell(rect(2.5, 11.5, 19, 10, min(S.R, 2))),
            detail("M10 15A2 2 0 1 1 12 17V17.5"), dot(12, 19.8, 1)]
    mitten = [outline(cap(7, 6, 7, 12, 5), cap(3.8, 9.5, 4.5, 11, 2.6))]
    hat = [shell("M13 11.5A4.5 4.5 0 0 1 22 11.5Z" if S.name == "line" else "M13 11.5A4.5 4.5 0 0 1 22 11.5Z"),
           line(seg(17.5, 7, 17.5, 5.5))]
    return [box_, mitten + hat]


# ============================================================================ chunk 4

@icon("dreidel", CAT, "A four sided spinning top with a short handle, a pointed base and a letter on its face.",
      tags=["dreidel", "spinning top", "hanukkah", "chanukah", "game", "top"])
def _(S):
    return [
        shell(poly([(6, 7.5), (18, 7.5), (18, 15), (12, 21.5), (6, 15)], closed=True, r=S.r * 0.6)),
        shell(rect(10.5, 2.5, 3, 3.5, min(S.R, 1))),
        detail(poly([(9, 9.5), (9.5, 13.5), (14.5, 13.5), (15, 9.5)], r=S.r * 0.3)),
        detail(seg(12, 9.5, 12, 13.5)),
    ]


@icon("clacker-balls", CAT, "Two balls on strings hanging from a finger ring and knocking together.",
      tags=["clackers", "clacker balls", "knocker balls", "retro toy", "string toy", "click clack"])
def _(S):
    return [
        shell(circle(12, 4, 2)),
        line(seg(10.9, 5.9, 8.2, 13.3)),
        line(seg(13.1, 5.9, 15.8, 13.3)),
        shell(circle(7.25, 17.5, 3.25)),
        shell(circle(16.75, 17.5, 3.25)),
    ]


@icon("toy-gyroscope", CAT, "A spinning disc on an axle inside a round frame, balanced on a point.",
      tags=["gyroscope", "spinning toy", "physics toy", "balance", "science toy", "spin"])
def _(S):
    return [
        line(circle(12, 10.5, 7.5)),
        shell(ellipse(12, 10.5, 4.5, 1.75)),
        line(seg(12, 3, 12, 8)),
        line(seg(12, 13, 12, 20.5)),
        line(seg(8, 21.5, 16, 21.5)),
    ]


@scene("picture-reel-viewer", "A binocular style toy viewer with a picture disc slotted into the top.",
       tags=["picture viewer", "slide viewer", "3d viewer", "reel viewer", "retro toy", "stereoscope"])
def _(S):
    viewer = [shell(rect(2.5, 11, 19, 9.5, min(S.R, 3))),
              detail(circle(8, 15.75, 2.25)), detail(circle(16, 15.75, 2.25))]
    disc = [shell(circle(12, 8.5, 6.5))] + [mark(circle(*polar(12, 8.5, 4, a), 0.9)) for a in (-150, -90, -30)]
    return [viewer, disc]


@icon("doctor-play-kit", CAT, "A toy doctor bag with a cross on the front and a stethoscope hanging out.",
      tags=["doctor kit", "toy doctor", "pretend play", "role play", "medical kit", "stethoscope"])
def _(S):
    return [
        shell(rect(2.5, 9, 14, 12.5, min(S.R, 2.5))),
        line(poly([(6.5, 9), (6.5, 5.5), (12.5, 5.5), (12.5, 9)], r=S.r)),
        detail(seg(9.5, 12.5, 9.5, 18)),
        detail(seg(6.75, 15.25, 12.25, 15.25)),
        line("M14.5 9C14.5 5.5 20 5.5 20 9.5V15.5"),
        shell(circle(20, 18.3, 1.8)),
    ]


@icon("pool-dive-rings", CAT, "Weighted dive rings resting on a pool floor under the water surface with bubbles rising.",
      tags=["dive rings", "pool toys", "diving toys", "swimming", "sink toys", "pool game"])
def _(S):
    return [
        line("M2 4Q4.5 2 7 4T12 4T17 4T22 4"),
        line(circle(7, 15.5, 3)),
        line(circle(17, 15.5, 3)),
        line(seg(2, 21.5, 22, 21.5)),
        dot(8, 9, 1.1), dot(15.5, 8, 0.9), dot(17.5, 10, 1.1),
    ]


@scene("toy-lawn-mower", "A push toy lawn mower with a long handle, big wheels and bubbles puffing from the top.",
       tags=["toy mower", "bubble mower", "push toy", "toddler toy", "garden play", "pretend play"])
def _(S):
    wheels = [shell(circle(5.5, 19.5, 2.5)), shell(circle(13.5, 19.5, 2.5))]
    body = [shell(pick(S, "M2.5 16.5V15A6.5 5 0 0 1 15.5 15V16.5Z", "M2.5 16.5A6.5 6 0 0 1 15.5 16.5Z")),
            line(poly([(14.5, 12), (20, 4), (22, 5.5)], r=S.r * 0.5))]
    bubbles = [line(circle(6.5, 5, 2)), line(circle(11.5, 3, 1.25))]
    return [wheels, body, bubbles]


@icon("toy-cutting-fruit", CAT, "A toy apple cut into two halves with seeds on the cut faces and a leaf on its stem.",
      tags=["cutting fruit", "toy food", "pretend kitchen", "play food", "wooden toy", "role play"])
def _(S):
    return [
        shell(pick(S, "M10 9C8 7.5 3 7.5 3 13.5C3 18.5 6 21.5 10 20.5Z",
                   "M10 9.5C8 7.5 3 7.5 3 13.5C3 18.5 6 21.5 9 21A1 1 0 0 0 10 20Z")),
        shell(pick(S, "M13 9C15 7.5 20 7.5 20 13.5C20 18.5 17 21.5 13 20.5Z",
                   "M13 9.5C15 7.5 20 7.5 20 13.5C20 18.5 17 21.5 14 21A1 1 0 0 1 13 20Z")),
        dot(7.5, 14.5, 1.1), dot(15.5, 14.5, 1.1),
        line(seg(11.5, 7, 11.5, 3)),
        shell(tilted_ellipse(15.5, 3.5, 1.3, 3, -15)),
    ]


@icon("class-photo", CAT, "A framed group photo with two rows of small heads and shoulders.",
      tags=["class photo", "school photo", "group photo", "yearbook", "classmates", "picture day"])
def _(S):
    parts = [shell(rect(2.5, 3, 19, 18, min(S.R, 2.5)))]
    for x, y in ((9.25, 7.5), (14.75, 7.5), (6.5, 13), (12, 13), (17.5, 13)):
        parts += [dot(x, y, 1.4), detail(f"M{fmt(x - 2)} {fmt(y + 4)}A2 1.8 0 0 1 {fmt(x + 2)} {fmt(y + 4)}")]
    return parts


@icon("bottle-teat", CAT, "A single feeding bottle teat with a rounded tip and a wide flat flange at the base.",
      tags=["bottle teat", "bottle nipple", "baby bottle", "feeding", "newborn", "silicone teat"])
def _(S):
    teat = pick(S, "M10.5 6V4H13.5V6C13.5 9 17 10 17 14V15.5H7V14C7 10 10.5 9 10.5 6Z",
                "M10.5 4.5A1.5 1.5 0 0 1 13.5 4.5V7C13.5 9 17 10 17 14V15.5H7V14C7 10 10.5 9 10.5 7Z")
    return [
        outline(P(teat), P(rect(3, 15.5, 18, 3.5, pick(S, 0.5, 1.75)))),
        detail(seg(7, 15.5, 17, 15.5)),
    ]


@icon("shoulder-ride", CAT, "An adult carrying a small child sitting on their shoulders.",
      tags=["shoulder ride", "piggyback", "carrying child", "parent and child", "family", "dad"])
def _(S):
    return [
        dot(12, 3, 2.25),
        line(poly([(12, 7), (7.5, 8), (7.5, 13)], r=S.r * 0.5)),
        line(poly([(12, 7), (16.5, 8), (16.5, 13)], r=S.r * 0.5)),
        dot(12, 11.5, 2.25),
        line(pick(S, "M4.5 22V18A2.5 2.5 0 0 1 7 15.5H17A2.5 2.5 0 0 1 19.5 18V22",
                  "M4.5 22V19A3.5 3.5 0 0 1 8 15.5H16A3.5 3.5 0 0 1 19.5 19V22")),
    ]


@scene("reading-together", "An adult and a child sitting side by side sharing an open book.",
       tags=["reading together", "story time", "bedtime story", "parent and child", "reading", "book"])
def _(S):
    book = [shell(poly([(6.5, 15), (12, 16.5), (17.5, 15), (17.5, 20.5), (12, 22), (6.5, 20.5)], closed=True, r=S.r * 0.3)),
            detail(seg(12, 16.5, 12, 22))]
    people = [dot(6.5, 5, 2.5), shell(pick(S, "M2 22V12.5A2.5 2.5 0 0 1 4.5 10H8.5A2.5 2.5 0 0 1 11 12.5V22Z",
                                             "M2 22V13.5A3.5 3.5 0 0 1 5.5 10H7.5A3.5 3.5 0 0 1 11 13.5V22Z")),
              dot(17.5, 9, 2), shell(pick(S, "M14 22V16A2 2 0 0 1 16 14H19A2 2 0 0 1 21 16V22Z",
                                           "M14 22V17A3 3 0 0 1 17 14H18A3 3 0 0 1 21 17V22Z"))]
    return [book, people]


@icon("nest-swing", CAT, "A round net dish swing hanging from ropes that meet at one point.",
      tags=["nest swing", "saucer swing", "web swing", "playground", "swing", "outdoor play"])
def _(S):
    dish = (pick(S, "M2.5 17.5H21.5A9.5 4 0 0 1 2.5 17.5Z", ellipse(12, 18, 9.5, 3.25)))
    return [
        shell(circle(12, 3, 1.5)),
        line(seg(11, 4.5, 3.5, 16)),
        line(seg(13, 4.5, 20.5, 16)),
        shell(dish),
        detail(pick(S, seg(7, 19, 17, 19), ellipse(12, 17.75, 5.5, 1))),
    ]


@icon("hook-a-duck", CAT, "A toy duck floating on water with a hook on a pole reaching for the loop on its head.",
      tags=["hook a duck", "fairground game", "fun fair", "duck game", "carnival", "fishing game"])
def _(S):
    duck = U(P("M2.5 14.5H16C16 18.5 13.5 20 9.5 20S2.5 18.5 2.5 14.5Z"), P(circle(9, 11.5, 2.75)),
             P(poly([(11, 10.5), (14, 11.5), (11, 12.5)], closed=True)))
    return [
        shell(path_to_d(duck)),
        dot(8.5, 11, 0.8),
        line("M21.5 11L13 2.5"),
        line(pick(S, "M13 2.5V6A2 2 0 0 1 9 6", "M13 2.5V6A2 2 0 0 1 9 6")),
        line("M2 22Q4.5 20.5 7 22T12 22T17 22T22 22"),
    ]


# ============================================================================ chunk 5

@scene("coconut-shy", "A coconut sitting in a cup on top of a post with a ball flying toward it.",
       tags=["coconut shy", "fairground game", "fun fair", "throwing game", "carnival", "fete"])
def _(S):
    nut = [shell(circle(8.5, 6, 3.5))]
    post = [shell(poly([(4.5, 9.5), (12.5, 9.5), (11, 12.5), (6, 12.5)], closed=True, r=S.r * 0.3)),
            line(seg(8.5, 12.5, 8.5, 21.5)), line(seg(4.5, 21.5, 12.5, 21.5))]
    ball = [dot(16.5, 8.5, 2.25), line(seg(20, 7, 22, 7)), line(seg(20, 10.5, 22, 10.5))]
    return [nut, post, ball]


@icon("can-toss", CAT, "A pyramid of six stacked tin cans with a ball flying toward it.",
      tags=["can toss", "tin can alley", "knock down cans", "fairground game", "throwing game", "carnival"])
def _(S):
    rr = pick(S, 0, 0.75)
    stack = U(P(rect(2.5, 16, 15, 5.5, rr)), P(rect(5, 10.5, 10, 5.5, rr)), P(rect(7.5, 5, 5, 5.5, rr)))
    return [
        shell(path_to_d(stack)),
        detail(seg(7.5, 16, 7.5, 21.5)), detail(seg(12.5, 16, 12.5, 21.5)), detail(seg(10, 10.5, 10, 16)),
        detail(seg(5, 16, 15, 16)), detail(seg(7.5, 10.5, 12.5, 10.5)),
        shell(circle(19.5, 5, 2)),
    ]


@icon("beanbag-toss", CAT, "A slanted toss board with a round hole near the top and a beanbag flying toward it.",
      tags=["beanbag toss", "bean bag game", "toss board", "garden game", "throwing game", "party game"])
def _(S):
    return [
        shell(poly([(6.5, 8), (15.5, 8), (20, 21.5), (2, 21.5)], closed=True, r=S.r * 0.5)),
        detail(ellipse(11, 13, 2.75, 2)),
        shell(rect(17.5, 2, 4.5, 3.5, pick(S, 0.5, 1.5))),
    ]


@icon("handlebar-streamers", CAT, "A bike handlebar grip with long ribbon streamers flowing back from its end.",
      tags=["handlebar streamers", "bike tassels", "bike streamers", "kids bike", "bicycle", "ribbons"])
def _(S):
    return [
        line(seg(10, 5.5, 22, 5.5)),
        shell(rect(3.5, 3, 6.5, 5, min(S.R, 2))),
        line("M4 10.5C5 16 8 19 12 21.5"),
        line("M7 10.5C9 15 12.5 17 17 18"),
        line("M10 10.5C12.5 13 16 13.5 21 13"),
    ]


@icon("skating-aid", CAT, "A penguin shaped skating frame with a handle bar that a child pushes along the ice.",
      tags=["skating aid", "skate helper", "ice skating", "learn to skate", "penguin", "rink"])
def _(S):
    return [
        line(poly([(4.5, 12), (4.5, 3), (15, 3)], r=S.r)),
        shell("M11 6C8 6 7 9 7 13.5C7 18 8.5 20 11.5 20S16.5 18 16.5 13.5C16.5 11 16 9.5 15 8.5C14.5 7 13 6 11 6Z"),
        solid(poly([(16, 8.5), (20, 9.75), (16.5, 11)], closed=True)),
        detail(ellipse(12.5, 15, 2, 3)),
        dot(12.5, 9.25, 1),
        line(seg(4, 21.5, 20, 21.5)),
    ]


@icon("snow-saucer", CAT, "A round dish sled with two handle slots and snow spraying up behind it.",
      tags=["snow saucer", "saucer sled", "disc sled", "sledging", "sledding", "winter"])
def _(S):
    return [
        shell(ellipse(11, 15.5, 9, 4.5)),
        detail(pick(S, "M5 14.5H17", ellipse(11, 14.5, 5.5, 1.5))),
        dot(3.5, 9.5, 1.1), dot(7, 7, 1.1), dot(4, 5, 0.9), dot(10, 8, 0.9),
    ]


@icon("sticker-book", CAT, "A closed book with a star sticker on the cover and a square sticker peeling at one corner.",
      tags=["sticker book", "sticker album", "stickers", "reward", "activity book", "collecting"])
def _(S):
    return [
        shell(rect(3.5, 2.5, 16, 19, min(S.R, 2.5))),
        detail(seg(7.5, 2.5, 7.5, 21.5)),
        mark(poly(star_pts(13.75, 8, 3, 1.3), closed=True, r=S.r * 0.15)),
        detail(poly([(10.5, 17.5), (10.5, 13.5), (17, 13.5), (17, 16), (14.5, 18.5)], r=S.r * 0.3)),
        detail(poly([(17, 16), (14.5, 16), (14.5, 18.5)], r=S.r * 0.3)),
    ]


@icon("felt-board", CAT, "A felt board on an easel with a cut out sun and house stuck to it.",
      tags=["felt board", "flannel board", "storytelling board", "preschool", "felt shapes", "classroom"])
def _(S):
    return [
        shell(rect(2.5, 2.5, 19, 14, min(S.R, 2))),
        mark(circle(7, 7, 2)),
        mark(poly([(11, 13.5), (11, 10), (14.5, 6.5), (18, 10), (18, 13.5)], closed=True, r=S.r * 0.3)),
        line(seg(7, 16.5, 5, 22)),
        line(seg(17, 16.5, 19, 22)),
    ]


@icon("sensory-bin", CAT, "A shallow tub heaped with rice, with a small scoop stuck in it.",
      tags=["sensory bin", "sensory play", "rice bin", "tactile play", "preschool", "messy play"])
def _(S):
    return [
        shell(poly([(2.5, 13), (21.5, 13), (19.5, 21.5), (4.5, 21.5)], closed=True, r=S.r * 0.5)),
        line("M4 11C6 7 13 7 16 11"),
        dot(7, 10, 0.8), dot(10, 9.8, 0.8), dot(13, 10.3, 0.8),
        line(seg(15.5, 9, 20, 3)),
    ]


@icon("kids-camera", CAT, "A chunky toy camera with a big lens and a round grip handle on each side.",
      tags=["kids camera", "toy camera", "childrens camera", "photography", "first camera", "digital camera"])
def _(S):
    return [
        shell(rect(5, 6, 14, 13, min(S.R, 3.5))),
        detail(circle(12, 12.5, 3.25)),
        shell(rect(7.5, 3, 4, 3, min(S.R, 1))),
        line("M5 9.5A3 3 0 0 0 5 15.5"),
        line("M19 9.5A3 3 0 0 1 19 15.5"),
    ]


@icon("cups-and-balls", CAT, "Upside down cups in a row, the middle one lifted to show a small ball underneath.",
      tags=["cups and balls", "shell game", "magic trick", "find the ball", "guessing game", "sleight of hand"])
def _(S):
    def cup(cx, top, b):
        return shell(poly([(cx - 2.75, b), (cx + 2.75, b), (cx + 1.75, top), (cx - 1.75, top)], closed=True, r=S.r * 0.4))
    return [cup(4.5, 14.5, 21.5), cup(19.5, 14.5, 21.5), cup(12, 5.5, 12.5), dot(12, 19.5, 2)]


@scene("floor-piano-mat", "A floor mat printed with big piano keys and a foot pressing one of them.",
       tags=["piano mat", "floor piano", "musical mat", "dance mat", "music toy", "keyboard mat"])
def _(S):
    foot = [shell(poly([(11, 2), (14.5, 2), (14.5, 6.5), (18.5, 8), (19.5, 10.5), (11, 10.5)], closed=True, r=S.r * 0.6))]
    mat = [shell(rect(2.5, 12, 19, 9.5, min(S.R, 2)))]
    for x in (6.3, 10.1, 13.9, 17.7):
        mat += [detail(seg(x, 17, x, 21.5)), sq(x - 1, 12, 2, 5, pick(S, 0, 0.5))]
    return [foot, mat]


# ============================================================================ chunk 6

@scene("stepping-stumps", "Three tree stumps of rising height standing close together for stepping across.",
       tags=["stepping stumps", "tree stumps", "balance", "playground", "natural play", "obstacle course"])
def _(S):
    def stump(x, w, top, b):
        rx = w / 2
        body = f"M{fmt(x)} {fmt(top)}A{fmt(rx)} 1.75 0 0 1 {fmt(x + w)} {fmt(top)}V{fmt(b)}H{fmt(x)}Z"
        rim = f"M{fmt(x)} {fmt(top)}A{fmt(rx)} 1.75 0 0 0 {fmt(x + w)} {fmt(top)}"
        return [shell(body), detail(rim)]
    return [stump(2.5, 7, 14.5, 21.5), stump(8.75, 7, 10, 21.5), stump(15, 7, 5.5, 21.5)]


@icon("airplane-spoon", CAT, "A baby spoon with two swept wings flying to the right, used to coax a child to eat.",
      tags=["airplane spoon", "feeding", "baby food", "weaning", "mealtime", "here comes the plane"])
def _(S):
    return [
        shell(ellipse(18, 12, 4, 2.75)),
        line(seg(2.5, 12, 14, 12)),
        shell(poly([(11, 10.5), (7.5, 10.5), (4.5, 3.5)], closed=True, r=S.r * 0.4)),
        shell(poly([(11, 13.5), (7.5, 13.5), (4.5, 20.5)], closed=True, r=S.r * 0.4)),
    ]


@icon("holding-hands-child", CAT, "A tall adult and a small child standing side by side and holding hands.",
      tags=["holding hands", "parent and child", "walking together", "crossing the road", "family", "safety"])
def _(S):
    return [
        dot(6.5, 4.5, 2.25),
        line(poly([(3.5, 14), (6.5, 9.5), (13.5, 13.5)], r=S.r * 0.5)),
        line(seg(6.5, 9.5, 6.5, 15.5)),
        line(poly([(3.5, 22), (6.5, 15.5), (9.5, 22)], r=S.r * 0.5)),
        dot(17.5, 9, 1.85),
        line(poly([(13.5, 13.5), (17.5, 12.5), (20.5, 16)], r=S.r * 0.5)),
        line(seg(17.5, 12.5, 17.5, 17.5)),
        line(poly([(15, 22), (17.5, 17.5), (20, 22)], r=S.r * 0.5)),
    ]
