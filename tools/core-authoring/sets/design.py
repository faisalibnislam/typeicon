"""TypeIcon Core: photo & design.

Design icons receive variant badges in the bottom-right (box 13–23), so identifying detail is kept in the
top and left of the canvas wherever the object allows. Long tools (brushes, pens, droppers) are drawn upright
and rotated 45° so their working end points to the bottom-left.
"""
from __future__ import annotations

import math

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.svgLib.path import parse_path

from dsl import (  # noqa: F401
    D, I, LINE, P, Part, ST, U, arc, circle, detail, dot, ellipse, filled_region, fmt, icon, line, path_to_d,
    poly, pt_on, rect, regular, rotation, seg, shell, solid,
)

CAT = "design"


# --------------------------------------------------------------------------- helpers

def rnd(S, line_val, rounded_val):
    return line_val if S.name == "line" else rounded_val


def xd(d: str, m) -> str:
    pen = SVGPathPen(None, ntos=fmt)
    parse_path(d, TransformPen(pen, m))
    return pen.getCommands()


def turn(parts, deg, cx=12.0, cy=12.0):
    m = rotation(deg, cx, cy)
    return [Part(p.kind, xd(p.d, m), dict(p.attrs)) for p in parts]


def rot_pt(p, deg, cx=12.0, cy=12.0):
    a = math.radians(deg)
    x, y = p[0] - cx, p[1] - cy
    return (cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a))


def soften(region, r):
    """Round the convex corners of a boolean region by radius r (morphological opening)."""
    if r <= 0:
        return region
    er = D(region, ST(path_to_d(region), 2 * r, "butt", "round"))
    return U(er, ST(path_to_d(er), 2 * r, "butt", "round"))


def mark(S, x, y, s=3.0):
    """Small solid point: square in Line (crisp), round in Rounded."""
    if S.name == "line":
        return solid(rect(x - s / 2, y - s / 2, s, s))
    return dot(x, y, s / 2 + 0.1)


def dashes(S, pts, n, dash=2.25):
    """n dashes centred at evenly spaced points on a straight run pts[0]→pts[1]. Dots in Rounded."""
    (x1, y1), (x2, y2) = pts
    out = []
    L = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / L, (y2 - y1) / L
    for i in range(n):
        t = L * (i + 0.5) / n
        cx, cy = x1 + ux * t, y1 + uy * t
        if S.name == "line":
            out.append(line(seg(cx - ux * dash / 2, cy - uy * dash / 2, cx + ux * dash / 2, cy + uy * dash / 2)))
        else:
            out.append(dot(cx, cy, 1.1))
    return out


def ridge(pts, S):
    return detail(poly(pts, r=S.r))


# ============================================================================ photos

@icon("images", CAT, "Two stacked photos; several images", tags=["photos", "pictures", "collection", "multiple", "album"])
def _(S):
    return [
        shell(rect(3, 8, 13, 13, min(S.R, 3))),
        line(poly([(8, 5), (8, 3), (21, 3), (21, 16), (19, 16)], r=S.r)),
        ridge([(3, 18), (7, 14), (13, 20)], S),
        dot(11.5, 12, 1.5),
    ]


@icon("gallery", CAT, "Large photo above a row of thumbnails; photo gallery", tags=["photos", "thumbnails", "pictures", "grid", "album", "browse"])
def _(S):
    th = [solid(rect(x, 18, 5, 3.5, rnd(S, 0, 1.25))) for x in (3, 9.5, 16)]
    return [
        shell(rect(3, 3, 18, 12, min(S.R, 3))),
        ridge([(3, 12.5), (8, 7.5), (13, 12.5)], S),
        dot(16.5, 7.5, 1.5),
        *th,
    ]


@icon("crop", CAT, "Two interlocking corner marks; crop an image", tags=["trim", "cut", "resize", "frame", "edit", "photo"])
def _(S):
    return [line(poly([(6.5, 2.5), (6.5, 17.5), (21.5, 17.5)], r=S.r)),
            line(poly([(2.5, 6.5), (17.5, 6.5), (17.5, 21.5)], r=S.r))]


@icon("rotate-image", CAT, "Picture with a curved arrow turning over it; rotate an image",
      tags=["rotate", "turn", "orientation", "photo", "edit", "picture"])
def _(S):
    c, r, a0, a1 = (12, 11), 7.0, 215, -5
    tip = pt_on(*c, r, a1)
    t = (-math.sin(math.radians(a1)), math.cos(math.radians(a1)))
    n = (-t[1], t[0])
    h = 2.75
    back = (tip[0] - t[0] * h, tip[1] - t[1] * h)
    head = [(back[0] + n[0] * h, back[1] + n[1] * h), tip, (back[0] - n[0] * h, back[1] - n[1] * h)]
    return [
        shell(rect(3, 12, 10, 9, min(S.R, 2.5))),
        ridge([(3, 18.5), (6.5, 15), (11.5, 20)], S),
        line(arc(*c, r, a0, a1)),
        line(poly(head, r=S.r * 0.6)),
    ]


def _flip_h(S):
    return [
        shell(poly([(8.5, 5), (8.5, 19), (2.5, 19)], closed=True, r=S.r * 0.35)),
        shell(poly([(15.5, 5), (15.5, 19), (21.5, 19)], closed=True, r=S.r * 0.35)),
        *dashes(S, [(12, 2.5), (12, 21.5)], 4),
    ]


@icon("reflect-horizontal", CAT, "Two mirrored triangles either side of a vertical axis; flip horizontally",
      tags=["mirror", "flip", "reflect", "horizontal", "transform", "edit"], aliases=["flip-horizontal"])
def _(S):
    return _flip_h(S)


@icon("reflect-vertical", CAT, "Two mirrored triangles above and below a horizontal axis; flip vertically",
      tags=["mirror", "flip", "reflect", "vertical", "upside down", "transform"], aliases=["flip-vertical"])
def _(S):
    return turn(_flip_h(S), -90)


@icon("aspect-ratio", CAT, "Frame with two opposite inner corners; aspect ratio", tags=["ratio", "proportion", "resize", "dimensions", "format", "frame"])
def _(S):
    return [
        shell(rect(2.5, 5, 19, 14, min(S.R, 3))),
        detail(poly([(6, 11.5), (6, 8.5), (9.5, 8.5)], r=S.r * 0.5)),
        detail(poly([(18, 12.5), (18, 15.5), (14.5, 15.5)], r=S.r * 0.5)),
    ]


# ============================================================================ painting and drawing tools

def _palette_region():
    cx, cy, rx, ry = 12, 11.5, 9.5, 8.5
    body = P(ellipse(cx, cy, rx, ry))
    a = math.radians(122)
    nx, ny = cx + rx * math.cos(a), cy + ry * math.sin(a)
    return D(body, P(circle(nx + 0.6, ny - 0.4, 3.4)))


@icon("palette", CAT, "Artist's paint palette with a thumb notch and paint dabs",
      tags=["paint", "colors", "colours", "art", "theme", "painting"], aliases=["paint-palette"])
def _(S):
    reg = _palette_region()
    if S.name == "rounded":
        reg = soften(reg, 1.5)
    return [shell(path_to_d(reg)), dot(7.5, 10.5, 1.6), dot(10.5, 6.75, 1.6), dot(15, 6.75, 1.6), dot(17.25, 11, 1.6)]


@icon("brush", CAT, "Wide decorator's brush with a handle, ferrule and bristles",
      tags=["paint", "decorate", "wall", "painter", "bristles", "diy"])
def _(S):
    body = [(10, 2.5), (14, 2.5), (14, 8.5), (18, 8.5), (18, 21), (6, 21), (6, 8.5), (10, 8.5)]
    return [
        shell(poly(body, closed=True, r=S.r)),
        detail(seg(6, 12.5, 18, 12.5)),
        detail(seg(10, 16, 10, 21)), detail(seg(14, 16, 14, 21)),
    ]


@icon("paintbrush", CAT, "Artist's paintbrush with a pointed tip", tags=["paint", "art", "brush", "artist", "painting", "draw"])
def _(S):
    tip = ("M9.5 14.5C9.5 18 10.7 20.5 12 23C13.3 20.5 14.5 18 14.5 14.5Z" if S.name == "line" else
           "M9.5 14.5C9.5 18 10.5 20.5 11.3 22.2Q12 23.4 12.7 22.2C13.5 20.5 14.5 18 14.5 14.5Z")
    parts = [
        line(seg(12, 1, 12, 9.5)),
        shell(rect(9.5, 9.5, 5, 5, rnd(S, 0, 1))),
        shell(tip),
    ]
    return turn(parts, 45)


@icon("pen-tool", CAT, "Pen nib with a slit; vector pen tool", tags=["pen", "nib", "vector", "path", "draw", "bezier", "illustrator"])
def _(S):
    nib = [(8, 7), (16, 7), (18, 12), (12, 22), (6, 12)]
    parts = [
        shell(rect(9, 2, 6, 3, rnd(S, 0, 1))),
        shell(poly(nib, closed=True, r=S.r)),
        detail(seg(12, 15.5, 12, rnd(S, 22, 19.5))),
        dot(12, 12.75, 1.6),
    ]
    return turn(parts, 45)


@icon("ruler", CAT, "Straight ruler with measuring ticks", tags=["measure", "scale", "length", "dimensions", "straightedge", "units"])
def _(S):
    parts = [
        shell(rect(3, 9, 18, 6, rnd(S, 0, 2))),
        detail(seg(7.5, 9, 7.5, 11.5)), detail(seg(12, 9, 12, 12.5)), detail(seg(16.5, 9, 16.5, 11.5)),
    ]
    return turn(parts, -45)


@icon("eyedropper", CAT, "Eyedropper pipette; pick a colour", tags=["color picker", "colour picker", "pipette", "sample", "dropper", "pick"],
      aliases=["color-picker", "pipette"])
def _(S):
    body = ("M9.5 8V4.5A2.5 2.5 0 0 1 14.5 4.5V8H17V10.5H14V17.5L12 21L10 17.5V10.5H7V8Z" if S.name == "line" else
            "M9.5 8V4.5A2.5 2.5 0 0 1 14.5 4.5V8H16A1 1 0 0 1 17 9V9.5A1 1 0 0 1 16 10.5H14V17.5L12.8 19.6Q12 21 11.2 19.6L10 17.5V10.5H8A1 1 0 0 1 7 9.5V9A1 1 0 0 1 8 8Z")
    return turn([shell(body), detail(seg(10, 14.5, 14, 14.5))], 45)


def transform_region(reg, m):
    return P(xd(path_to_d(reg), m))


_PIV = (6.75, 17.75)


def _grow(reg, g):
    return U(reg, ST(path_to_d(reg), 2 * g, "butt", "round"))


@icon("color-swatch", CAT, "Fan of colour swatch cards", tags=["swatches", "colors", "colours", "samples", "palette", "paint chips"],
      aliases=["colour-swatch"])
def _(S):
    rr = rnd(S, 0.5, 2)
    c1 = P(rect(3.5, 2.5, 6.5, 19, rr))
    m2 = rotation(38, *_PIV)
    c2 = transform_region(P(rect(3.5, 2.5, 6.5, 17, rr)), m2)
    v2 = D(c2, _grow(c1, 1))
    bands = [xd(seg(8.5, y, 10, y), m2) for y in (7.5, 12.5)]
    return [shell(path_to_d(c1)), shell(path_to_d(v2)),
            detail(seg(3.5, 7.5, 10, 7.5)), detail(seg(3.5, 12.5, 10, 12.5)), dot(*_PIV, 1.5)] + [detail(d) for d in bands]


# ============================================================================ structure

@icon("layers", CAT, "Three stacked sheets seen at an angle; layers", tags=["stack", "levels", "arrange", "overlay", "sheets", "depth"])
def _(S):
    return [
        shell(poly([(12, 3), (21, 7.5), (12, 12), (3, 7.5)], closed=True, r=S.r)),
        line(poly([(3, 12), (12, 16.5), (21, 12)], r=S.r)),
        line(poly([(3, 16.5), (12, 21), (21, 16.5)], r=S.r)),
    ]


@icon("card-stack", CAT, "Stack of cards seen from the front", tags=["pile", "cards", "deck", "collection", "group", "arrange", "stack"])
def _(S):
    return [shell(rect(3, 11, 18, 10, min(S.R, 3))), line(seg(5, 7.5, 19, 7.5)), line(seg(7.5, 4, 16.5, 4))]


@icon("shapes", CAT, "Triangle, circle and square together; shapes", tags=["geometry", "objects", "elements", "draw", "insert", "figures"])
def _(S):
    return [
        shell(poly([(7, 3), (11.5, 10.5), (2.5, 10.5)], closed=True, r=S.r * 0.6)),
        shell(circle(16.75, 7, 4.25)),
        shell(rect(3, 13.5, 7.5, 7.5, rnd(S, 0, 1.5))),
    ]


@icon("vector", CAT, "Curved path between two square anchor points; vector graphics", tags=["path", "anchor", "nodes", "svg", "illustration", "curve"])
def _(S):
    rr = rnd(S, 0, 1.25)
    return [shell(rect(3, 15, 6, 6, rr)), shell(rect(15, 3, 6, 6, rr)), line("M6 15C6 9.5 9.5 6 15 6")]


@icon("bezier", CAT, "Curve with an anchor and two control handles; Bézier curve", tags=["curve", "handles", "anchor", "path", "control points", "vector"],
      aliases=["bezier-curve"])
def _(S):
    rr = rnd(S, 0, 1.25)
    return [
        shell(rect(9.5, 5.5, 5, 5, rr)),
        line(seg(4.5, 8, 9.5, 8)), line(seg(14.5, 8, 19.5, 8)),
        dot(3.5, 8, 1.75), dot(20.5, 8, 1.75),
        line("M4 21C4 15.5 6.5 11.5 9.5 10.5"), line("M20 21C20 15.5 17.5 11.5 14.5 10.5"),
    ]


@icon("grid-lines", CAT, "Square divided into a three-by-three grid; guides or rule of thirds",
      tags=["guides", "rule of thirds", "table", "composition", "layout", "grid"])
def _(S):
    return [shell(rect(3, 3, 18, 18, min(S.R, 3))),
            detail(seg(9, 3, 9, 21)), detail(seg(15, 3, 15, 21)), detail(seg(3, 9, 21, 9)), detail(seg(3, 15, 21, 15))]


@icon("frame", CAT, "Picture frame with a mount, hanging from a cord", tags=["picture frame", "photo", "wall", "art", "hang", "border"],
      aliases=["picture-frame"])
def _(S):
    return [line(poly([(8, 5.5), (12, 2.5), (16, 5.5)], r=S.r * 0.5)),
            shell(rect(3, 6.5, 18, 14.5, min(S.R, 3))),
            detail(rect(7, 10.5, 10, 6.5, rnd(S, 0, 1.5)))]


@icon("focus-frame", CAT, "Viewfinder corners around a centre cross; camera focus", tags=["focus", "viewfinder", "autofocus", "scan", "camera", "target"])
def _(S):
    k = [(3, 8), (3, 3), (8, 3)]
    br = [line(poly(k, r=S.r))]
    for m in ((-1, 0, 0, 1, 24, 0), (1, 0, 0, -1, 0, 24), (-1, 0, 0, -1, 24, 24)):
        br.append(line(xd(poly(k, r=S.r), m)))
    return br + [line(seg(12, 8.5, 12, 15.5)), line(seg(8.5, 12, 15.5, 12))]


def _aperture_blades(ext):
    V = [pt_on(12, 12, 4.25, -90 + i * 60) for i in range(6)]
    out = []
    for i in range(6):
        a, b = V[i - 1], V[i]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        # ray from a along u to the circle r = 9
        ox, oy = a[0] - 12, a[1] - 12
        bq = ox * ux + oy * uy
        t = -bq + math.sqrt(bq * bq - (ox * ox + oy * oy - 81))
        out.append(seg(b[0], b[1], a[0] + ux * t, a[1] + uy * t))
    return V, out


@icon("aperture", CAT, "Camera iris with six blades around a hexagonal opening", tags=["iris", "camera", "f-stop", "lens", "photography", "shutter"])
def _(S):
    V, blades = _aperture_blades(0)
    return [shell(circle(12, 12, 9)), detail(poly(V, closed=True, r=S.r * 0.6))] + [detail(d) for d in blades]


@icon("lens", CAT, "Round glass lens with a reflection", tags=["glass", "optics", "camera lens", "magnify", "photography", "focus"])
def _(S):
    return [shell(circle(12, 12, 9)), detail(arc(12, 12, 5.25, 190, 265)), detail(arc(12, 12, 5.25, 10, 30))]


@icon("shutter", CAT, "Closed camera shutter with curved blades meeting at the centre", tags=["camera", "iris", "shutter speed", "photography", "capture", "blades"])
def _(S):
    blades = []
    for i in range(6):
        a = -90 + i * 60
        p0 = pt_on(12, 12, 2.2, a + 60)
        p1 = pt_on(12, 12, 9, a)
        blades.append(detail(f"M{fmt(p0[0])} {fmt(p0[1])}A6.5 6.5 0 0 0 {fmt(p1[0])} {fmt(p1[1])}"))
    return [shell(circle(12, 12, 9))] + blades


@icon("camera-flash", CAT, "Lightning bolt with rays of light; camera flash", tags=["flash", "strobe", "bolt", "light", "photography", "speedlight"])
def _(S):
    bolt = [(11.5, 2.5), (4, 13), (9.5, 13), (8, 21.5), (16, 10), (10.5, 10)]
    rays = [seg(*pt_on(12, 10, 6.5, a), *pt_on(12, 10, 9, a)) for a in (-50, -10, 30)]
    return [shell(poly(bolt, closed=True, r=S.r * 0.4))] + [line(d) for d in rays]


def sparkle(cx, cy, r, k=0.16):
    """Four-point sparkle with concave sides."""
    pts = [(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)]
    ctl = [(cx + r * k, cy - r * k), (cx + r * k, cy + r * k), (cx - r * k, cy + r * k), (cx - r * k, cy - r * k)]
    d = f"M{fmt(pts[0][0])} {fmt(pts[0][1])}"
    for i in range(4):
        c, p = ctl[i], pts[(i + 1) % 4]
        d += f"Q{fmt(c[0])} {fmt(c[1])} {fmt(p[0])} {fmt(p[1])}"
    return d + "Z"


@icon("magic-wand", CAT, "Magic wand with sparkles at its tip", tags=["magic", "auto", "enhance", "wizard", "select", "sparkle"],
      aliases=["wand"])
def _(S):
    return [line(seg(3.5, 20.5, 13, 11)), shell(sparkle(17, 7, 4.75)),
            line(seg(8, 3, 8, 7)), line(seg(6, 5, 10, 5))]


@icon("sparkles", CAT, "Three sparkling stars; magic, AI or something new", tags=["magic", "ai", "new", "shine", "stars", "clean"])
def _(S):
    return [shell(sparkle(10, 13.5, 7.5)), shell(sparkle(18.25, 5.75, 3.75)), solid(sparkle(4.5, 4.5, 2.5, 0.2))]


@icon("stamp", CAT, "Rubber stamp above its print line", tags=["rubber stamp", "approve", "seal", "mark", "print", "official"])
def _(S):
    handle = U(P(circle(12, 6, 3.25)), P(poly([(10.5, 8), (13.5, 8), (15, 12), (9, 12)], closed=True)))
    if S.name == "rounded":
        handle = soften(handle, 0.8)
    return [shell(path_to_d(handle)), shell(rect(4, 12, 16, 4.5, min(S.R, 1.5))), line(seg(4, 20, 20, 20))]


@icon("scissors", CAT, "Open scissors; cut", tags=["cut", "trim", "clip", "snip", "craft", "tailor"])
def _(S):
    piv = (12, 10)
    parts = []
    for side in (-1, 1):
        c = (12 + side * 4.25, 17)
        ux, uy = piv[0] - c[0], piv[1] - c[1]
        L = math.hypot(ux, uy)
        ux, uy = ux / L, uy / L
        start = (c[0] + ux * 2.5, c[1] + uy * 2.5)
        tip = (piv[0] + ux * 8, piv[1] + uy * 8)
        parts += [shell(circle(*c, 2.5)), line(seg(*start, *tip))]
    return turn(parts, 45)


@icon("sticker", CAT, "Smiling square sticker with a peeling corner", tags=["decal", "label", "emoji", "peel", "badge", "stick"])
def _(S):
    body = [(3, 3), (13, 3), (21, 11), (21, 21), (3, 21)]
    return [shell(poly(body, closed=True, r=rnd(S, 0, 2.5))),
            detail("M13 3C13 8 15.5 11 21 11" if S.name == "line" else "M13 3.5C13.5 8 16 10.5 20.5 11"),
            dot(7.5, 10, 1.4), dot(12, 10, 1.4),
            detail(arc(10, 13, 4.25, 30, 150))]


@icon("spray-can", CAT, "Aerosol spray can with a mist of paint", tags=["spray paint", "aerosol", "graffiti", "paint", "airbrush", "can"],
      aliases=["spray-paint"])
def _(S):
    return [shell(rect(4, 9.5, 9, 12, min(S.R, 2.5))),
            shell(rect(5.5, 4.5, 6, 5, rnd(S, 0, 1))),
            detail(seg(4, 14, 13, 14)),
            dot(15.5, 6, 1.1), dot(18.5, 3.5, 1.1), dot(18.5, 8.5, 1.1), dot(21, 6, 1.1)]


@icon("bucket-fill", CAT, "Tipped paint bucket pouring a drop; fill tool", tags=["paint bucket", "fill", "color fill", "flood fill", "pour", "paint"],
      aliases=["paint-bucket"])
def _(S):
    pail = [
        shell("M6.5 8L8.5 18.5A4.5 1.75 0 0 0 17.5 18.5L19.5 8A6.5 2.25 0 0 0 6.5 8Z" if S.name == "line" else
              "M6.5 8L8.3 17.6Q8.5 18.6 9.4 19.1C10.5 19.6 11.7 19.9 13 19.9C14.3 19.9 15.5 19.6 16.6 19.1Q17.5 18.6 17.7 17.6L19.5 8A6.5 2.25 0 0 0 6.5 8Z"),
        detail("M6.5 8A6.5 2.25 0 0 0 19.5 8"),
        line("M7.5 11A5.5 7.5 0 0 1 18.5 11"),
    ]
    drop = ("M3.5 14.5C3.5 14.5 1.75 16.9 1.75 18.3A1.75 1.75 0 0 0 5.25 18.3C5.25 16.9 3.5 14.5 3.5 14.5Z" if S.name == "line" else
            "M3.5 14.5C3 15.2 1.75 17 1.75 18.3A1.75 1.75 0 0 0 5.25 18.3C5.25 17 4 15.2 3.5 14.5Z")
    return turn(pail, -35, 13, 12) + [shell(drop)]


@icon("gradient", CAT, "Square shading from solid to fine dots; colour gradient", tags=["fade", "blend", "transition", "ombre", "shading", "fill"])
def _(S):
    R = min(S.R, 3)
    band = I(P(rect(3, 3, 18, 18, R)), P(rect(3, 3, 6, 18)))
    return [shell(rect(3, 3, 18, 18, R)), solid(path_to_d(band)),
            dot(12.5, 6.5, 1.5), dot(12.5, 12, 1.5), dot(12.5, 17.5, 1.5),
            dot(17, 9.25, 1), dot(17, 14.75, 1)]


def _contrast_filled():
    return D(P(circle(12, 12, 10)), P("M12 5A7 7 0 0 0 12 19Z"))


@icon("contrast", CAT, "Circle with one half solid; contrast", tags=["contrast", "dark light", "invert", "adjust", "half", "tone"],
      filled=_contrast_filled)
def _(S):
    half = P("M12 6A6 6 0 0 1 12 18Z")
    if S.name == "rounded":
        half = soften(half, 1.25)
    return [shell(circle(12, 12, 9)), solid(path_to_d(half))]


def _rays(r0, r1):
    return [seg(*pt_on(12, 12, r0, a), *pt_on(12, 12, r1, a)) for a in range(0, 360, 45)]


def _brightness_filled():
    core = D(P(circle(12, 12, 5.5)), P("M12 9.5A2.5 2.5 0 0 0 12 14.5Z"))
    return U(core, *[ST(d, 2.5) for d in _rays(8, 10.25)])


@icon("brightness", CAT, "Half-filled sun; brightness setting", tags=["brightness", "light", "display", "screen", "adjust", "luminance"],
      filled=_brightness_filled)
def _(S):
    return [shell(circle(12, 12, 4.5)), solid("M12 7.5A4.5 4.5 0 0 1 12 16.5Z")] + [line(d) for d in _rays(7.75, 10)]


@icon("exposure", CAT, "Square split diagonally with plus and minus; exposure compensation",
      tags=["exposure", "plus minus", "ev", "camera", "adjust", "brightness"])
def _(S):
    R = min(S.R, 3)
    o = R * (1 - math.sqrt(0.5))
    return [shell(rect(3, 3, 18, 18, R)), detail(seg(3 + o, 21 - o, 21 - o, 3 + o)),
            detail(seg(5.5, 8.5, 11.5, 8.5)), detail(seg(8.5, 5.5, 8.5, 11.5)), detail(seg(13, 16, 18.5, 16))]


def _blur_dots(kind):
    out = []
    for i in range(-2, 3):
        for j in range(-2, 3):
            d2 = i * i + j * j
            if d2 > 4:
                continue
            s = {0: 3.75, 1: 2.9, 2: 2.4, 4: 2.0}[d2]
            x, y = 12 + 4.5 * i, 12 + 4.5 * j
            if kind == "line":
                out.append(solid(rect(x - s / 2, y - s / 2, s, s)))
            elif kind == "rounded":
                out.append(dot(x, y, s / 2 + 0.15))
            else:
                out.append(P(circle(x, y, s / 2 + 0.45)))
    return out


@icon("blur", CAT, "Dots fading out from the centre; blur effect", tags=["soften", "defocus", "bokeh", "effect", "filter", "fuzzy"],
      filled=lambda: U(*_blur_dots("filled")))
def _(S):
    return _blur_dots(S.name)


@icon("sharpen", CAT, "Triangle nested inside a triangle; sharpen", tags=["sharpness", "detail", "clarity", "crisp", "edges", "enhance"])
def _(S):
    return [shell(poly([(12, 3), (21, 19.5), (3, 19.5)], closed=True, r=S.r * 0.6)),
            detail(poly([(12, 10), (15.75, 16.5), (8.25, 16.5)], closed=True, r=S.r * 0.4))]


# ============================================================================ photo prints and film

@icon("photo-album", CAT, "Bound photo album with a picture on the cover", tags=["album", "photos", "scrapbook", "memories", "book", "collection"])
def _(S):
    return [shell(rect(4, 2.5, 16, 19, min(S.R, 2.5))), detail(seg(8, 2.5, 8, 21.5)),
            detail(rect(11, 6.5, 5.5, 5.5, rnd(S, 0, 1.25)))]


@icon("polaroid", CAT, "Instant photo print with a wide bottom border", tags=["instant photo", "print", "snapshot", "photo", "picture", "retro"],
      aliases=["instant-photo"])
def _(S):
    return [shell(rect(4, 2.5, 16, 19, min(S.R, 2))), detail(rect(7, 5.5, 10, 10, rnd(S, 0, 1))),
            detail(poly([(7, 13.5), (10.5, 10), (14, 13.5)], r=S.r * 0.5))]


_HOLES = [(x, y) for x in (5, 9.67, 14.33, 19) for y in (6.5, 17.5)]


def _film_filled():
    body = filled_region([shell(rect(2, 4, 20, 16, 2)), detail(rect(5, 9, 6, 6)), detail(rect(13, 9, 6, 6))])
    return D(body, *[P(rect(x - 1.1, y - 1.1, 2.2, 2.2, 0.4)) for x, y in _HOLES])


@icon("film-strip", CAT, "Horizontal strip of film with sprocket holes and frames", tags=["film", "negative", "movie", "frames", "reel", "35mm"],
      aliases=["filmstrip"], filled=_film_filled)
def _(S):
    parts = [shell(rect(2, 4, 20, 16, min(S.R, 2))),
             detail(rect(5, 9, 6, 6, rnd(S, 0, 1))), detail(rect(13, 9, 6, 6, rnd(S, 0, 1)))]
    for x in (5, 9.67, 14.33, 19):
        parts += [mark(S, x, 6.5, 2), mark(S, x, 17.5, 2)]
    return parts


# ============================================================================ tools and workspace

@icon("selection-tool", CAT, "Dashed marquee with a pointer; selection tool", tags=["select", "marquee", "selection", "cursor", "pointer", "area"])
def _(S):
    L = S.r * 0.5
    parts = [line(poly([(3, 6.5), (3, 3), (6.5, 3)], r=L)), line(poly([(13.5, 3), (17, 3), (17, 6.5)], r=L)),
             line(poly([(3, 13.5), (3, 17), (6.5, 17)], r=L)),
             line(seg(8.5, 3, 11.5, 3)), line(seg(3, 8.5, 3, 11.5))]
    tip, k = (10.5, 10.5), 0.85
    cur = [(0, 0), (0, 10.5), (3, 8), (5, 12), (7, 11), (5, 7.2), (8.7, 7.2)]
    return parts + [shell(poly([(tip[0] + x * k, tip[1] + y * k) for x, y in cur], closed=True, r=S.r * 0.4))]


@icon("artboard", CAT, "Frame outlined by crossing guide lines; artboard or frame tool", tags=["canvas", "frame tool", "board", "page", "workspace", "crop marks"])
def _(S):
    return [line(seg(7, 3, 7, 21)), line(seg(17, 3, 17, 21)), line(seg(3, 7, 21, 7)), line(seg(3, 17, 21, 17))]


@icon("mockup", CAT, "Wireframe of a page with an image block and text lines; mockup", tags=["wireframe", "prototype", "layout", "template", "ui design", "page"],
      aliases=["wireframe"])
def _(S):
    return [shell(rect(2.5, 3.5, 19, 17, min(S.R, 2.5))), detail(seg(2.5, 8, 21.5, 8)),
            detail(rect(6, 11.5, 5, 5.5, rnd(S, 0, 1))), detail(seg(14, 12, 18, 12)), detail(seg(14, 16.5, 17, 16.5))]


@icon("typography-design", CAT, "Capital and small letter A; typography and type design", tags=["type", "font", "text", "letters", "typeface", "aa"])
def _(S):
    return [line(poly([(2, 20), (7, 4), (12, 20)], r=S.r)), line(seg(4.2, 13.5, 9.8, 13.5)),
            line(circle(17.25, 16.75, 3.25)), line(seg(20.5, 12.5, 20.5, 20))]


def _wheel_spokes(w=2.0):
    return U(*[ST(seg(12, 12, *pt_on(12, 12, 10.5, a)), w) for a in range(-90, 270, 45)])


def _wheel_blades():
    out = []
    for k in range(0, 8, 2):
        a0 = -90 + 45 * k
        p0, p1 = pt_on(12, 12, 7, a0), pt_on(12, 12, 7, a0 + 45)
        out.append(P(f"M12 12L{fmt(p0[0])} {fmt(p0[1])}A7 7 0 0 1 {fmt(p1[0])} {fmt(p1[1])}Z"))
    return U(*out)


@icon("color-wheel", CAT, "Colour wheel: a ring around alternating solid segments",
      tags=["colour wheel", "hue", "spectrum", "color picker", "palette", "rgb"], aliases=["colour-wheel"],
      filled=lambda: D(P(circle(12, 12, 10)), P(circle(12, 12, 2.25)), _wheel_spokes(1.75)))
def _(S):
    blades = _wheel_blades()
    if S.name == "rounded":
        blades = soften(blades, 1)
    return [shell(circle(12, 12, 9)), solid(path_to_d(blades))]


@icon("paint-roller", CAT, "Paint roller with a bent handle", tags=["roller", "paint", "decorate", "wall", "diy", "painter"])
def _(S):
    return [shell(rect(3, 3, 15, 6, min(S.R, 2))), line(poly([(18, 6), (21, 6), (21, 12), (12, 12), (12, 14)], r=S.r)),
            shell(rect(10, 14, 4, 7.5, rnd(S, 0, 1.5)))]


@icon("easel", CAT, "Artist's easel holding a canvas", tags=["canvas", "painting", "art", "studio", "artist", "stand"])
def _(S):
    return [line(seg(12, 1.5, 12, 4)), shell(rect(4, 4, 16, 10.5, min(S.R, 2))),
            line(seg(8, 14.5, 5, 21.5)), line(seg(16, 14.5, 19, 21.5)), line(seg(12, 14.5, 12, 19))]


@icon("sculpture", CAT, "Classical bust on a small pedestal; sculpture", tags=["statue", "bust", "museum", "art", "gallery", "classical"],
      aliases=["statue"])
def _(S):
    bust = P("M5.5 17C5.5 14 7.5 12.3 10 12L10.5 10.5H13.5L14 12C16.5 12.3 18.5 14 18.5 17C16.5 16.5 14 16.8 12 17.8C10 16.8 7.5 16.5 5.5 17Z")
    if S.name == "rounded":
        bust = soften(bust, 1)
    ped = [(9.5, 17.8), (14.5, 17.8), (16, 21.5), (8, 21.5)]
    return [shell(ellipse(12, 6.25, 3.5, 4)), shell(path_to_d(bust)), shell(poly(ped, closed=True, r=S.r * 0.5))]


def _mosaic(kind):
    tiles = []
    ang = [8, -6, 0, -4, 10, -8, 0, 6, -10]
    k = 0
    for j in range(3):
        for i in range(3):
            cx, cy = 5.5 + 6.5 * i, 5.5 + 6.5 * j
            s = 4.25 if kind != "filled" else 5
            r = {"line": 0, "rounded": 1.25, "filled": 0.75}[kind]
            tiles.append(xd(rect(cx - s / 2, cy - s / 2, s, s, r), rotation(ang[k], cx, cy)))
            k += 1
    return tiles


@icon("mosaic", CAT, "Irregular square tiles set in a grid; mosaic", tags=["tiles", "tessellation", "pattern", "pixel", "art", "collage"],
      filled=lambda: U(*[P(d) for d in _mosaic("filled")]))
def _(S):
    return [solid(d) for d in _mosaic(S.name)]


@icon("origami", CAT, "Folded paper boat; origami", tags=["paper boat", "fold", "paper", "craft", "folding", "japanese"])
def _(S):
    boat = [(2.5, 12.5), (7.5, 12.5), (12, 3.5), (16.5, 12.5), (21.5, 12.5), (17.5, 19.5), (6.5, 19.5)]
    return [shell(poly(boat, closed=True, r=S.r * 0.5)), detail(seg(2.5, 12.5, 21.5, 12.5))]
